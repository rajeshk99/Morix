# Morix — Online 3 Men's Morris

Morix is a real-time multiplayer implementation of the classic strategy board game **Three Men's Morris**. Two players can host or join a game using a room code and play online in real time.

## Features

- Real-time multiplayer gameplay
- Room code system for hosting and joining games
- Interactive browser-based board
- Turn-based gameplay
- Win detection system

## Technologies Used

- Python
- WebSockets
- JavaScript
- HTML
- CSS

## How to Run Locally

Install dependencies:

```bash
pip install websockets
```

Run the server:

```bash
python ws_server.py
```

Open the game in your browser and start playing.

## Project Structure

```
Morix
│
├── ws_server.py
├── game_engine.py
├── index.html
└── requirements.txt
```

## Game Rules

Three Men's Morris is played on a **3×3 board**.

1. Each player has **three pieces**.
2. Players place their pieces on empty positions.
3. After all pieces are placed, players move pieces to **adjacent positions**.
4. The first player to form a **straight line of three pieces** wins.
