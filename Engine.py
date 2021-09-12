from PIL import Image, ImageColor
import IPython.display

from Position import Position
from Board import Board


# some random changes
# some random changes
# some random changes
# some random changes
class Engine:
    def __init__(self):
        self.board = Board()
        self.white_moves = True
        self.game_finished = False
    
    def get_board(self):
        return self.board.copy()
    
    def make_move(self, moves):
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

# For a single move (one step or one capture), a moves parameter for make_move should be an two-element array
# of Positions representing the starting position of a piece which you want to move and its position adfter the move.
# For complex moves (capturing more than one piece), the array should be longer.
# The first position should represent the starting position of the piece you want to move and the last element - the position where you want to finish your move.
# All the intermediate positions should represent 'checking points' during your moves, i. e. where you land just after capturing a piece.
# For instance, if you have a king standing at (0, 0) and want to capture an enemy's piece from (3, 3), then from (6, 6), then turn and capture one from (7, 5) and then slide and finish your move on (9, 3), you should pass as a move the following array:
# [Position(0, 0), Position(4, 4), Position(7, 7), Position(9, 3)]
class Game:
    def __init__(self, white, black):
        self.engine = Engine()
        self.white = white
        self.black = black
        self.continue_game = True
        self.result = {'moves': [], 'winner': ''}
    
    @staticmethod
    def move_to_dictionary(move):
        to_return = []
        for m in move:
            to_return += [{'y': m.y, 'x': m.x}]
        return to_return
    
    
    def bot_move(self, bot, is_white, draw_board=True):
        move = bot.make_move(self.engine.board)
        self.result['moves'] += [Game.move_to_dictionary(move)]
        
        try:
            self.engine.make_move(move)
        except ValueError as ve:
            print("Move not allowed - BLACK WINS" if is_white else "Move not allowed - WHITE WINS")
            self.result['winner'] = 'black' if is_white else 'white'
            print(ve.args[0])
            print(ve.args[2])
            ve.args[1].show()
            self.continue_game = False
            return
            
        if draw_board:
            IPython.display.clear_output()
            self.engine.board.show(is_white)

        if (self.engine.board.white_lost()):
            print("WHITE WINS" if is_white else "BLACK WINS")
            self.result['winner'] = 'white' if is_white else 'black'
            self.engine.board.show()
            self.continue_game = False
    
    
    def human_move(self, is_white, draw_board):
        correct_move_entered = False
        while not correct_move_entered:
            pre_move = input("Your move").split()
            move = []
            for i in range(int(len(pre_move) / 2)):
                move += [Position(int(pre_move[2*i]), int(pre_move[2*i+1]))]
            
            if not is_white:
                for i in range(len(move)):
                    move[i] = Position(9 - move[i].y, 9 - move[i].x)

            try:
                self.engine.make_move(move)
                self.result['moves'] += [Game.move_to_dictionary(move)]
                correct_move_entered = True
            except ValueError as ve:
                print("Move not allowed: " + ve.args[0])
                print(ve.args[2])
                return
            
        if draw_board:
            IPython.display.clear_output()
            self.engine.board.show(is_white)

        if (self.engine.board.white_lost()):
            print("WHITE WINS" if is_white else "BLACK WINS")
            self.result['winner'] = 'white' if is_white else 'black'
            self.engine.board.show()
            self.continue_game = False
    
    
    def play_bots(self, draw_board=True):
        self.continue_game = True
        self.result = {'moves': [], 'winner': ''}
        
        while self.continue_game:
            self.bot_move(self.white, True, draw_board)
            if not self.continue_game:
                break
            self.bot_move(self.black, False, draw_board)
        return self.result

    
    def play_human(self, bot_white, draw_board=True):
        self.continue_game = True
        self.result = {'moves': [], 'winner': ''}
        if bot_white:
            self.bot_move(self.white, bot_white, draw_board)
            
        while self.continue_game:
            self.human_move(not bot_white, draw_board)
            if not self.continue_game:
                break
            self.bot_move(self.white, bot_white, draw_board)
        return self.result
    
    
    
    
                
            