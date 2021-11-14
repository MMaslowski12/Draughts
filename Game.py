import time
from PIL import Image, ImageColor
import IPython.display

from Position import Position
from Board import Board
from Engine import Engine


# Your bot should be a class, which contains a function called make_move(self, board). It should return a move which a bot would make for a given state of board - board.
# It should return a list of Positions, representing the piece's move. Its first element should be a piece's starting Position and the next values should encode the piece's path:

# For a single move (one step or one capture), return a two-element array of Positions: the starting position of a piece which you want to move and its position adfter the move.
# For instane, if you have a pawn at (2, 0) and want to move it to (3, 1), return: [Position(2, 0), Position(3, 1)]
# If you have a piece at (4, 4) and want to move to (6, 6), capturing an opponent's piece at (5, 5), return: [Position(4, 4), Position(6, 6)]
# If you have a king at (0, 4) and want to move to (4, 0), capturing an opponent's piece at (3, 1), return: [Position(0, 4), Position(4, 0)]

# For complex moves (capturing more than one piece), the array should be longer.
# The first position should represent the starting position of the piece you want to move and the last element - the position where you want to finish your move.
# All the intermediate positions should represent 'checking points' during your moves, i. e. where you land just after capturing a piece.
# For instance, if you have a king standing at (0, 0) and want to capture an enemy's piece from (3, 3), then from (6, 6), then turn and capture one from (7, 5) and then slide and finish your move on (9, 3), you should pass as a move the following array:
# [Position(0, 0), Position(4, 4), Position(7, 7), Position(9, 3)]


class Game:
    # Initialise a new game with a starting board position and with the white player moving first
    # We store the history of the whole game (and the winner) in result
    # white, black are bots which we want to play either white or black
    def __init__(self, white, black):
        self.engine = Engine()
        self.white = white
        self.black = black
        self.continue_game = True
        self.result = {'moves': [], 'winner': ''}
        self.move_length = 1
    
    
    # Helping function to encode moves in a form in which we'll store them in result
    @staticmethod
    def move_to_dictionary(move):
        to_return = []
        for m in range (int(len(move))):
            print(move)
            print(move[m])
            to_return += [{'y': move[m].y, 'x': move[m].x}]
        return to_return
    
    
    # Ask a playing bot what move to make and make it
    def bot_move(self, bot, is_white, draw_board=True):
        move = bot.make_move(self.engine.board)
        self.result['moves'] += [Game.move_to_dictionary(move)]
        
        start_time = time.time()
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
        end_time = time.time()
        time_elapsed = end_time - start_time
        if time_elapsed < self.move_length:
            time.sleep(self.move_length - time_elapsed)
            
        if draw_board:
            IPython.display.clear_output()
            self.engine.board.show(is_white)

        if (self.engine.game_finished):
            if not self.engine.draw:
                print("WHITE WINS" if is_white else "BLACK WINS")
                self.result['winner'] = 'white' if is_white else 'black'
            else:
                print("DRAW")
            self.continue_game = False
    
    
    # Ask a human player what move to make and make it
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

        if (self.engine.game_finished):
            if not self.engine.draw:
                print("WHITE WINS" if is_white else "BLACK WINS")
                self.result['winner'] = 'white' if is_white else 'black'
            else:
                print("DRAW")
            self.continue_game = False
    
    
    # Run a game of two bots against each other
    def play_bots(self, draw_board=True):
        self.continue_game = True
        self.result = {'moves': [], 'winner': ''}
        
        while self.continue_game:
            self.bot_move(self.white, True, draw_board)
            if not self.continue_game:
                break
            self.bot_move(self.black, False, draw_board)
        return self.result

    
    # Run a game of a bot against a human. Variable bot_white should be true if we want the bot to play whites. If you want to draw a board after each move, variable draw_board should be true
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
