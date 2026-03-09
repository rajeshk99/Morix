import socket

HOST = "127.0.0.1"
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

while True:
    message = client.recv(1024).decode()

    if not message:
        break

    print(message)

    if "Place piece" in message or "Move piece" in message:
        move = input()
        client.send(move.encode())
