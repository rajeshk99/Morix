import asyncio
import websockets
import json
import random
import string
import os
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'game'))
from game_engine import GameEngine
from aiohttp import web
# rooms[code] = { "game": GameEngine, "players": [ws, ws], "turn": "X", "placed": 0 }
rooms = {}


def generate_code():
    while True:
        code = ''.join(random.choices(string.digits, k=4))
        if code not in rooms:
            return code


async def broadcast_board(room):
    board = room["game"].board
    for p in room["players"]:
        await p.send(json.dumps({
            "type": "board",
            "board": board,
            "turn": room["turn"]
        }))


async def handler(websocket):
    code = None
    player_symbol = None

    try:
        raw = await asyncio.wait_for(websocket.recv(), timeout=30)
        msg = json.loads(raw)
        action = msg.get("action")

        # -------- HOST --------
        if action == "host":
            code = generate_code()
            rooms[code] = {
                "game": GameEngine(),
                "players": [websocket],
                "turn": "X",
                "placed": 0
            }
            player_symbol = "X"
            print(f"Room {code} created")
            await websocket.send(json.dumps({"type": "hosted", "code": code, "symbol": "X"}))
            await websocket.send(json.dumps({"type": "wait"}))

        # -------- JOIN --------
        elif action == "join":
            code = msg.get("code", "").strip()
            if code not in rooms:
                await websocket.send(json.dumps({"type": "error", "message": "Room not found. Check the code and try again."}))
                return
            room = rooms[code]
            if len(room["players"]) >= 2:
                await websocket.send(json.dumps({"type": "error", "message": "Room is already full."}))
                return
            room["players"].append(websocket)
            player_symbol = "O"
            print(f"Player O joined room {code}")
            await websocket.send(json.dumps({"type": "joined", "symbol": "O"}))
            for p in room["players"]:
                await p.send(json.dumps({"type": "start"}))
            await broadcast_board(room)

        else:
            await websocket.send(json.dumps({"type": "error", "message": "Invalid action."}))
            return

        room = rooms[code]

        while True:
            message = await websocket.recv()

            if player_symbol != room["turn"]:
                continue

            # Placement phase
            if room["placed"] < 6:
                try:
                    pos = int(json.loads(message))
                    if room["game"].place_piece(pos, player_symbol):
                        room["placed"] += 1
                        if room["game"].check_win(player_symbol):
                            for p in room["players"]:
                                await p.send(json.dumps({"type": "win", "player": player_symbol}))
                            del rooms[code]
                            return
                        room["turn"] = "O" if room["turn"] == "X" else "X"
                        await broadcast_board(room)
                except (ValueError, TypeError, KeyError) as e:
                    print(f"Placement error in room {code}: {e}")
                continue

            # Movement phase
            try:
                move = json.loads(message)
                from_pos = move["from"]
                to_pos = move["to"]
                if room["game"].move_piece(from_pos, to_pos, player_symbol):
                    if room["game"].check_win(player_symbol):
                        for p in room["players"]:
                            await p.send(json.dumps({"type": "win", "player": player_symbol}))
                        del rooms[code]
                        return
                    room["turn"] = "O" if room["turn"] == "X" else "X"
                    await broadcast_board(room)
            except (ValueError, KeyError, json.JSONDecodeError) as e:
                print(f"Movement error in room {code}: {e}")

    except websockets.exceptions.ConnectionClosed:
        print(f"Player {player_symbol} disconnected from room {code}")
        if code and code in rooms:
            room = rooms[code]
            for p in room["players"]:
                if p != websocket:
                    try:
                        await p.send(json.dumps({"type": "error", "message": "Your opponent disconnected."}))
                    except:
                        pass
            del rooms[code]

    except asyncio.TimeoutError:
        print("Connection timed out waiting for host/join message")
async def index(request):
    base = os.path.dirname(os.path.abspath(__file__))
    return web.FileResponse(os.path.join(base, '..', 'frontend', 'index.html'))

async def main():
    port = int(os.environ.get("PORT", 5000))

    async def websocket_handler(request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        
        class WSAdapter:
            async def recv(self): 
                msg = await ws.receive()
                return msg.data
            async def send(self, data): 
                await ws.send_str(data)
            @property
            def closed(self): 
                return ws.closed

        await handler(WSAdapter())
        return ws

    app = web.Application()
    app.router.add_get('/', index)
    app.router.add_get('/ws', websocket_handler)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"Server running on port {port}")
    await asyncio.Future()int(f"HTTP on :{port}, WS on :8765")
    await asyncio.Future()
asyncio.run(main())
