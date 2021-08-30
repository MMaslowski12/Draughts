from PIL import Image, ImageColor
import IPython.display

from Board import Board


# TODO: add draws
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
            print("Move not allowed: " + ve.args[0])
            raise ve

        self.board = new_board
        self.white_moves = not self.white_moves

        if self.board.white_lost():
            winner = "black" if self.white_moves else "white"
            self.game_finished = True
            print(winner + " won!")

        return self.board


class Game:
    def __init__(self, white, black):
        self.engine = Engine()
        self.white = white
        self.black = black
        self.continue_game = True


    def bot_move(self, bot, is_white, draw_board=True):
        move = bot.make_move(self.engine.board)

        try:
            self.engine.make_move(move)
        except ValueError as ve:
            print("Move not allowed - BLACK WINS" if is_white else "Move not allowed - WHITE WINS")
            print(ve.args[0])
            print(ve.args[2])
            ve.args[1].show()
            self.continue_game = False

        if draw_board:
            IPython.display.clear_output()
            self.engine.board.show(is_white)

        if (self.engine.board.white_lost()):
            print("WHITE WINS" if is_white else "BLACK WINS")
            self.continue_game = False


    def human_move(self, is_white, draw_board):
        correct_move_entered = False
        while not correct_move_entered:
            pre_move = input("Your move").split()
            move = []
            for i in range(int(len(pre_move) / 2)):
                move += [{'y': int(pre_move[2*i]), 'x': int(pre_move[2*i+1])}]

            if not is_white:
                for i in range(len(move)):
                    move[i] = {'y': 9 - move[i]['y'], 'x': 9 - move[i]['x']}

            try:
                self.engine.make_move(move)
                correct_move_entered = True
            except ValueError as ve:
                print("Move not allowed: " + ve.args[0])
                print(ve.args[2])

        if draw_board:
            IPython.display.clear_output()
            self.engine.board.show(is_white)

        if (self.engine.board.white_lost()):
            print("WHITE WINS" if is_white else "BLACK WINS")
            self.continue_game = False


    def play_bots(self, draw_board=True):
        self.continue_game = True

        while self.continue_game:
            self.bot_move(self.white, True, draw_board)
            if not self.continue_game:
                break
            self.bot_move(self.black, False, draw_board)


    def play_human(self, bot_white, draw_board=True):
        self.continue_game = True
        if bot_white:
            self.bot_move(self.white, bot_white, draw_board)

        while self.continue_game:
            self.human_move(not bot_white, draw_board)
            if not self.continue_game:
                break
            self.bot_move(self.white, bot_white, draw_board)
