import math
import copy
import numpy as np
from PIL import Image, ImageColor
import IPython.display

from Piece import Piece
from Graphics import draw_circle


class Board:
    # From the board's percpective, always white moves
    def newWhite(self, y, x, king=False):
        white = Piece.whitePiece(y, x, king)
        self.whites += [white]
        return white

    def newBlack(self, y, x, king=False):
        black = Piece.blackPiece(y, x, king)
        self.blacks += [black]
        return black


    def on_board(self, y, x):
        return 0 <= y and y < 10 and 0 <= x and x < 10

    def isWhite(self, y, x):
        if not self.on_board(y, x):
            return False
        if self.world[y][x] is None:
            return False
        return self.world[y][x].white

    def isBlack(self, y, x):
        if not self.on_board(y, x):
            return False
        if self.world[y][x] is None:
            return False
        return not self.world[y][x].white

    def isEmpty(self, y, x):
        if not self.on_board(y, x):
            return False
        return self.world[y][x] is None


    def white_lost(self):
        if len(self.whites) == 0:
            return True
        if self.kill_possible():
            return False
        if self.normal_move_possible():
            return False
        return True

    def kill_possible(self):
        for white in self.whites:
            if not white.king:
                for i in [-1, 1]:
                    if self.isBlack(white.y + 1, white.x + i):
                        if self.isEmpty(white.y + 2, white.x + 2*i):
                            return True

            else:
                for yi in [-1, 1]:
                    for xi in [-1, 1]:
                        whereY = white.y + yi
                        whereX = white.x + xi
                        while self.isEmpty(whereY, whereX):
                            whereY += yi
                            whereX += xi
                        if self.isBlack(whereY, whereX) and self.isEmpty(whereY + yi, whereX + xi):
                            return True
        return False

    def normal_move_possible(self):
        for white in self.whites:
            for i in [-1, 1]:
                if self.isEmpty(white.y + 1, white.x + i):
                    return True
                if white.king and self.isEmpty(white.y - 1, white.x + i):
                    return True
        return False


    def copy(self):
        new_board = Board()
        new_board.whites = []
        new_board.blacks = []
        for y in range(10):
            for x in range(10):
                if self.world[y][x] is None:
                    new_board.world[y][x] = None
                else:
                    if self.world[y][x].white:
                        piece = Piece(True, self.world[y][x].king, y, x)
                        new_board.whites += [piece]
                        new_board.world[y][x] = piece
                    else:
                        piece = Piece(False, self.world[y][x].king, y, x)
                        new_board.blacks += [piece]
                        new_board.world[y][x] = piece
        return new_board


    def __init__(self):
        self.whites = []
        self.blacks = []

        self.world = [[(self.newWhite(y, x) if y < 3 else self.newBlack(y, x))
                           if ((x + y) % 2 == 0 and (y < 3 or y > 6)) else None
                    for x in range(10)]
                    for y in range(10)]

        self.debug = False


    def revert(self):
        new_board = self.copy()

        new_board.whites, new_board.blacks = new_board.blacks, new_board.whites
        for piece in new_board.whites + new_board.blacks:
            piece.changeColour()

        for piece in new_board.whites + new_board.blacks:
            piece.move_symmetrically()
        for x in range(10):
            for y in range(5):
                new_board.world[y][x], new_board.world[9 - y][9 - x] = new_board.world[9 - y][9 - x], new_board.world[y][x]

        return new_board


    def make_move(self, moves):

        if len(moves) < 2:
            raise ValueError("You have to move", self, moves)
        else:
            if self.kill_possible():
                origin = moves[0]
                dest = moves[1]
                yi = np.sign(dest['y'] - origin['y'])
                xi = np.sign(dest['x'] - origin['x'])
                

                if not self.world[origin['y']][origin['x']].king:
                    if (dest['y'] - origin['y']) != 2:
                        
                              
                        raise ValueError("You must kill (incorrect man move)", self, moves)
                else:
                    whereY = origin['y'] + yi
                    whereX = origin['x'] + xi
                    while self.isEmpty(whereY, whereX):
                        whereY += yi
                        whereX += xi
                    if not (self.isBlack(whereY, whereX) and self.isEmpty(whereY + yi, whereX + xi)):
                        raise ValueError("You must kill (incorrect king move)", self, moves)


            new_board = self.copy()
            just_killed = False
            for i in range(len(moves) - 1):
                if i > 0 and new_board.world[moves[i]['y']][moves[i]['x']].king:
                    if not just_killed:

                        if np.sign(moves[i+1]['y'] - moves[i]['y']) != np.sign(moves[i]['y'] - moves[i-1]['y']) or np.sign(moves[i+1]['x'] - moves[i]['x']) != np.sign(moves[i]['x'] - moves[i-1]['x']):
                            self.show()
                            raise ValueError("Can't change your direction here")

                        
                            
                new_board, just_killed = new_board.make_single_move(
                    moves[i]['y'], moves[i]['x'], moves[i+1]['y'], moves[i+1]['x'], must_kill=(i > 0 or self.kill_possible()))

            if moves[-1]['y'] == 9:
                for white in new_board.whites:
                    if white.y == moves[-1]['y'] and white.x == moves[-1]['x']:
                        white.king = True
                new_board.world[moves[-1]['y']][moves[-1]['x']].king = True

            return new_board.revert()


    def make_single_move(self, y, x, newY, newX, must_kill=False):
        new_board = self.copy()
        piece = new_board.world[y][x]
        direction = -1 if np.sign(newY - y) != np.sign(newX - x) else 1
        just_killed = False

        moves = [{'y': y, 'x': x}, {'y': newY, 'x': newX}]
        if not self.isWhite(y, x):
            raise ValueError("You have to move your own piece", self, moves)
        if not self.isEmpty(newY, newX):
            raise ValueError("You have to move to an empty field", self, moves)


        if must_kill:
            if not piece.king:
                if abs(newY - y) != 2 or abs(newX - x) != 2:
                    raise ValueError("You have to capture", self, moves)
                if not self.isBlack(int((y+newY)/2), int((x+newX)/2)):
                    raise ValueError("You have to capture an enemy", self, moves)

                for black in new_board.blacks:
                    if black.y == y+1 and black.x == int((x+newX)/2):
                        new_board.blacks.remove(black)
                        break
                new_board.world[int((y+newY)/2)][int((x+newX)/2)] = None

            else:
                if abs(newY - y) != abs(newX - x):
                    raise ValueError("You cannot move there - too far", self, moves)

                y_range = range(newY + 1, y) if newY < y else range(y + 1, newY)
                y_dir = -1 if newY < y else 1
                for y_temp in y_range:
                    x_temp = x + (y_temp - y) * direction
                    if self.isWhite(y_temp, x_temp):
                        raise ValueError("You cannot move over your piece", self, moves)
                    if self.isBlack(y_temp, x_temp):
                        if not self.isEmpty(y_temp + y_dir, x_temp + y_dir * direction):
                            raise ValueError("You cannot capture more than one pieces at once", self, moves)

                    if self.isBlack(newY - y_dir, newX - y_dir * direction):
                        just_killed = True

                    for black in new_board.blacks:
                        if black.y == y_temp and black.x == x_temp:
                            new_board.blacks.remove(black)
                            break
                    new_board.world[y_temp][x_temp] = None


        else:
            if not piece.king:
                if newY - y != 1 or abs(newX - x) != 1:
                    raise ValueError("You cannot move there - wrong destination", self, moves)
            else:
                if abs(newY - y) != abs(newX - x):
                    raise ValueError("You cannot move there - not diagonal", self, moves)

                y_range = range(newY + 1, y) if newY < y else range(y + 1, newY)
                for y_temp in y_range:
                    x_temp = x + (y_temp - y) * direction
                    if not self.isEmpty(y_temp, x_temp):
                        raise ValueError("You cannot move over a taken field", self, moves)

        for white in new_board.whites:
            if white.y == y and white.x == x:
                white.x = newX
                white.y = newY
        new_board.world[newY][newX] = new_board.world[y][x]
        new_board.world[y][x] = None

        return new_board, just_killed


    def show(self, black_moves = False):
        if black_moves:
            self.revert().show()
            return

        white = (200, 255, 200)
        black = (0, 100, 0)

        size = 40
        img = Image.new("RGB", (10 * size, 10 * size))

        arr = np.array(img)
        arr[:] = (255, 255, 255)

        indices = np.arange(10)
        col_num = np.repeat(indices, size)
        col_num = np.tile(col_num, (size*10, 1))
        row_num = np.transpose(col_num)
        is_black = (col_num + row_num) % 2 == 0
        arr[is_black] = (0, 0, 0)

        for piece in self.whites + self.blacks:
            draw_circle(arr, size*piece.y + size/2, size*piece.x + size/2, 12, white if piece.white else black)
            if piece.king:
                draw_circle(arr, size*piece.y + size/2, size*piece.x + size/2, 4, black if piece.white else white)

        out = Image.fromarray(arr)
        display(out)