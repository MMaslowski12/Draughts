from Position import Position
from Board import Board

# This class holds a full state of the game: a board (as a Board class), an information wether it's the white player's move, and an information wether the game has already finished because one of the players lost

# If a player attempts to make a move which isn't allowed (e. g. move a piece outside of a board, capture more than two enemy's pieces at the same time, move not diagonally, etc., they loose
class Engine:
    def __init__(self):
        self.board = Board()
        self.white_moves = True
        self.game_finished = False
        self.boring_moves = 0
        self.limit_boring_moves = 25
        self.draw = False
    
    # Returns a safe copy of a board
    def get_board(self):
        return self.board.copy()
    
    # A player makes a move, update the game's state
    def make_move(self, moves):
        boring_move = False
        if len(moves) == 2:
            if self.board.world[moves[0].y][moves[0].x] != None:
                if self.board.world[moves[0].y][moves[0].x].king:
                    boring_move = True
          
        if boring_move:
            self.boring_moves += 1
            print(self.boring_moves)
        else:
            self.boring_moves = 0
            
        if self.boring_moves >= self.limit_boring_moves:
            winner = "draw"
            print("draw")
            self.game_finished = True
            self.draw = True
        
        
        new_board = self.board
        try:
            new_board = self.board.make_move(moves)
        except ValueError as ve:
            raise ve
        
        self.board = new_board
        self.white_moves = not self.white_moves

        if self.board.white_lost():
            winner = "black" if self.white_moves else "white"
            self.game_finished = True
            print(winner + " won!")

        return self.board