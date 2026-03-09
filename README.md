# Morix — Online 3 Men's Morris
Real-time multiplayer Three Men's Morris game built with Python, WebSockets, and JavaScript.


Morrion — Online 3 Men's Morris
Morrion is a real-time multiplayer implementation of the classic strategy game Three Men's Morris. The game allows two players to connect using a room code and compete online with instant board updates using WebSocket communication.
The project demonstrates concepts from network programming, real-time communication, and game logic implementation.
Game Overview
Three Men's Morris is played on a 3 × 3 grid.
The game consists of two phases:
Placement Phase
Players take turns placing their three pieces on empty positions of the board.
Movement Phase
After all six pieces are placed, players move their pieces to adjacent positions.
Objective
The goal is to form a straight line of three pieces before the opponent.
Features
Real-time multiplayer gameplay
Room-based matchmaking system
Interactive SVG game board
Turn-based synchronization
Win detection system
Host and join functionality using a room code
Technologies Used
Python – WebSocket server
JavaScript – Client-side game logic
HTML & CSS – User interface
WebSockets – Real-time communication protocol

How to Run Locally
1.Install dependencies:
$pip install websockets

2.Run the server:
$python ws_server.py

Open the game in a browser and start playing.
