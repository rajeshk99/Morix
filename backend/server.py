import socket
from game.game_engine import GameEngine

HOST = "127.0.0.1"
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()

print("3 Men's Morris Server Started")
print("Waiting for players...")

game = GameEngine()

conn1, addr1 = server.accept()
print("Player 1 connected:", addr1)

conn2, addr2 = server.accept()
print("Player 2 connected:", addr2)

print("Both players connected. Game starting...")

conn1.send("Game starting. You are Player X\n".encode())
conn2.send("Game starting. You are Player O\n".encode())


def send_board():
    board_text = game.board_to_string()
    conn1.send((board_text + "\n").encode())
    conn2.send((board_text + "\n").encode())


# ---------- Phase 1 : Placement ----------
def placement_phase():

    for i in range(3):

        # Player X
        while True:
            conn1.send("Place piece: ".encode())
            move = conn1.recv(1024).decode()

            if not move:
                print("Player X disconnected")
                return True

            try:
                pos = int(move)
            except:
                conn1.send("Enter a number between 1 and 9\n".encode())
                continue

            if game.place_piece(pos, "X"):
                send_board()

                if game.check_win("X"):
                    conn1.send("You win!\n".encode())
                    conn2.send("You lose!\n".encode())
                    return True

                break
            else:
                conn1.send("Invalid move\n".encode())

        # Player O
        while True:
            conn2.send("Place piece: ".encode())
            move = conn2.recv(1024).decode()

            if not move:
                print("Player O disconnected")
                return True

            try:
                pos = int(move)
            except:
                conn2.send("Enter a number between 1 and 9\n".encode())
                continue

            if game.place_piece(pos, "O"):
                send_board()

                if game.check_win("O"):
                    conn2.send("You win!\n".encode())
                    conn1.send("You lose!\n".encode())
                    return True

                break
            else:
                conn2.send("Invalid move\n".encode())

    return False


# ---------- Phase 2 : Movement ----------
def movement_phase():

    while True:

        # Player X
        while True:
            conn1.send("Move piece (from to): ".encode())
            move = conn1.recv(1024).decode()

            if not move:
                print("Player X disconnected")
                return

            try:
                from_pos, to_pos = map(int, move.split())
            except:
                conn1.send("Invalid format. Use: from to\n".encode())
                continue

            if game.move_piece(from_pos, to_pos, "X"):
                send_board()

                if game.check_win("X"):
                    conn1.send("You win!\n".encode())
                    conn2.send("You lose!\n".encode())
                    return

                break
            else:
                conn1.send("Invalid move\n".encode())

        # Player O
        while True:
            conn2.send("Move piece (from to): ".encode())
            move = conn2.recv(1024).decode()

            if not move:
                print("Player O disconnected")
                return

            try:
                from_pos, to_pos = map(int, move.split())
            except:
                conn2.send("Invalid format. Use: from to\n".encode())
                continue

            if game.move_piece(from_pos, to_pos, "O"):
                send_board()

                if game.check_win("O"):
                    conn2.send("You win!\n".encode())
                    conn1.send("You lose!\n".encode())
                    return

                break
            else:
                conn2.send("Invalid move\n".encode())


# ---------- Run Game ----------
send_board()

game_over = placement_phase()

if not game_over:
    conn1.send("Movement phase begins\n".encode())
    conn2.send("Movement phase begins\n".encode())

    movement_phase()

conn1.close()
conn2.close()
server.close()
