class GameEngine:
    def __init__(self):
        self.board = [None]*9

    winning_combinations = [
        [0,1,2],
        [3,4,5],
        [6,7,8],
        [0,3,6],
        [1,4,7],
        [2,5,8],
        [0,4,8],
        [2,4,6]
    ]
    adjacent_positions = {
        1: [2,4,5],
        2: [1,3,5],
        3: [2,6,5],
        4: [1,7,5],
        5: [1,2,3,4,6,7,8,9],
        6: [3,9,5],
        7: [4,8,5],
        8: [7,9,5],
        9: [6,8,5]
    }
    def board_to_string(self):
        rows = []
        for i in range(3):
            row = []
            for j in range(3):
                value = self.board[3*i + j]
                row.append(value if value else " ")
            rows.append(" | ".join(row))
        return "\n---------\n".join(rows)
    
    def display_board(self):
        for i in range(3):
            for j in range(3):
                value = self.board[3*i + j]
                print(value if value else " ", end=" ")
                if j < 2:
                    print("|", end=" ")
            print()
            if i < 2:
                print("---------")
                
    def place_piece(self,position, player):
        if position < 1 or position > 9:
            print("Position error")
            return False
        if self.board[position-1] is None:
            self.board[position-1] = player
            return True
        else:
            print(f"Cant move to {position} error from {player}")
            return False
            
    def check_win(self,player):
        for combo in self.winning_combinations:
            a = combo[0]
            b = combo[1]
            c = combo[2]
            if self.board[a] == player and self.board[b] == player and self.board[c] == player:
                return True
        return False

    def play_game(self):
        for i in range(6):
            if i % 2 == 0:
                player = "X"
            else:
                player = "O"
            print(f"Player {player} turn")
            while True:
                position = int(input("Enter position: "))
                if self.place_piece(position, player):
                    break
                else:
                    print("Try again")
            self.display_board()
            if self.check_win(player):
                print(f"Player {player} wins!")
                return
        current_player = "O" if i % 2 == 0 else "X"  # continue from last placement turn

        while True:
            self.display_board()
            print(f"Player {current_player} move")
            from_pos = int(input("Move from: "))
            to_pos = int(input("Move to: "))
            if self.move_piece(from_pos, to_pos, current_player):
                if self.check_win(current_player):
                    self.display_board()
                    print(f"Player {current_player} wins!")
                    break
                if current_player == "X":
                    current_player = "O"
                else:
                    current_player = "X"
            else:
                print("Invalid move, try again")
            
    def move_piece(self,from_pos, to_pos, player):
        if from_pos < 1 or from_pos > 9 or to_pos < 1 or to_pos > 9:
            print("Invalid position")
            return False
        if self.board[from_pos - 1] != player:
            print("You must move your own piece")
            return False
        if self.board[to_pos - 1] is not None:
            print("Destination not empty")
            return False
        if to_pos not in self.adjacent_positions[from_pos]:
            print("Move not allowed")
            return False
        self.board[from_pos - 1] = None
        self.board[to_pos - 1] = player
        return True

