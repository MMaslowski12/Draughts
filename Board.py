import math
import copy
import numpy as np
from PIL import Image, ImageColor
import IPython.display

from Piece import Piece
from Position import Position
from Graphics import draw_circle

#final cleanup
#experimental changes
#more radnom changes
# White is the player, who moves next (this makes implementation easier - we don't have to if everywhere whose move it is)
# Rows are represented by 'y' axis, columns by 'x' axis. Both are indexed from 0 to 9. (0, 0) is the left-uppermost square
class Board:
    def newWhite(self, y, x, king=False):
        white = Piece.whitePiece(y, x, king)
        self.whites += [white]
        return white
    
    def newBlack(self, y, x, king=False):
        black = Piece.blackPiece(y, x, king)
        self.blacks += [black]
        return black
    
#     check, if a given position is on the board
    def on_board(self, where):
        return 0 <= where.y and where.y < 10 and 0 <= where.x and where.x < 10
    
#     check, if the given position is on the board and is occupied by a white piece
    def isWhite(self, where):
        if not self.on_board(where):
            return False
        if self.world[where.y][where.x] is None:
            return False
        return self.world[where.y][where.x].white
    
#     check, if the given position is on the board and is occupied by a black piece
    def isBlack(self, where):
        if not self.on_board(where):
            return False
        if self.world[where.y][where.x] is None:
            return False
        return not self.world[where.y][where.x].white
    
#     check, if the given position is on the board and is not occupied
    def isEmpty(self, where):
        if not self.on_board(where):
            return False
        return self.world[where.y][where.x] is None
    
#     check, if the white cannot make any move and therefore lost
    def white_lost(self):
        if len(self.whites) == 0:
            return True
        if self.capture_possible():
            return False
        if self.normal_move_possible():
            return False
        return True
    
#     check, if it is possible for the white player to capture an opponent's piece
    def capture_possible(self, debug=False):
#         iterate over all the white pieces
        for white in self.whites:
            if not white.king:
                for i in [-1, 1]:
                    if self.isBlack(white.position().add(1, i)):
                        if self.isEmpty(white.position().add(2, 2*i)):
                            if debug:
                                print(str(white.position().y) + ", " + str(white.position().x) + " -> " + str(white.position().add(2, 2*i).y) + ", " + str(white.position().add(2, 2*i).x))
                            return True
                        
            else:
#             iterate over possible directions of movement
                for xi in [-1, 1]:
                    for yi in [-1, 1]:
                        where = white.position().add(yi, xi)
#                     go in that direction, until an occuppied field is found
                        while (self.isEmpty(where)):
                            where = where.add(yi, xi)
                        if self.isBlack(where) and self.isEmpty(where.add(yi, xi)):
                            return True
        return False
    
#     check, if a non-capturing move is possible
    def normal_move_possible(self):
        for white in self.whites:
            for i in [-1, 1]:
                if self.isEmpty(white.position().add(1, i)):
                    return True
                if white.king and self.isEmpty(white.position().add(-1, i)):
                    return True
        return False
    
    
#     initializes the board to a starting configuration
    def __init__(self):
        self.whites = []
        self.blacks = []
        
        self.world = [[(self.newWhite(y, x) if y < 3 else self.newBlack(y, x))
                           if ((x + y) % 2 == 0 and (y < 3 or y > 6)) else None 
                    for x in range(10)]
                    for y in range(10)]
    
    
    @staticmethod
    def empty_board():
        to_return = Board()
        to_return.whites = []
        to_return.blacks = []
        to_return.world = [[None for x in range(10)] for y in range(10)]
        return to_return
    
    
#     returns a safe copy of the board
    def copy(self):
        new_board = Board.empty_board()
        new_board.whites = []
        new_board.blacks = []
        
        for white in self.whites:
            new_board.world[white.y][white.x] = new_board.newWhite(white.y, white.x, white.king)
            
        for black in self.blacks:
            new_board.world[black.y][black.x] = new_board.newBlack(black.y, black.x, black.king)
            
        return new_board
        
        
#     returns a new board which is this board turned around with all the pieces colours reversed.
#     We need this function at the end of each move, so that in the
#     internal representation the player who is about to move is white
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
        
        
#     Make a full move and return a state of board after it
    def make_move(self, moves):
        if len(moves) < 2:
            raise ValueError("You have to move to a new position", self, moves)
            
        new_board = self.copy()
        for i in range(len(moves) - 1):
            new_board = new_board.make_single_move(
                moves[i], moves[i+1], moves,
                must_capture=(i > 0 or self.capture_possible()), first_move=(i == 0))

#             if a piece ends its move on the end of a board, it is crowned
        piece = new_board.world[moves[-1].y][moves[-1].x]
        if piece.y == 9:
            piece.king = True

#             Revert board at the end of a move, so that the player who moves is white in Board's internal representation
        return new_board.revert()
        
    
#     Make a single move from one position to another (i. e., a single capture or a single step)
    def make_single_move(self, old, new, move, must_capture=False, first_move=True):
        new_board = self.copy()
        piece = new_board.world[old.y][old.x]
        yi = np.sign(new.y - old.y)
        xi = np.sign(new.x - old.x)
        
        moves_log = {
            'move': [{'y': old.y, 'x': old.x}, {'y': new.y, 'x': new.x}],
            'must_capture': must_capture, 'first_move': first_move}
        if not self.isWhite(old):
            raise ValueError("You have to move your own piece", self, moves_log)
        if not self.isEmpty(new):
            raise ValueError("You have to move to an empty field", self, moves_log)
        
        
        if must_capture:
            if not piece.king:
#                 if len(move) > 3:
#                     if move[0].y == 3 and move[2].x == 5 and move[2].y == 3 and move[3].y == 5 and move[3].x == 3: 
#                         self.show()
                if abs(new.y - old.y) != 2 or abs(new.x - old.x) != 2 or (first_move and new.y - old.y != 2):
                    print(self.capture_possible(True))
                    raise ValueError("You have to capture", self, moves_log)
                if not self.isBlack(old.middle(new)):
                    haha = [[s.y, s.x] for s in move]
                    print(haha)
#                     self.show()
                    raise ValueError("You have to capture an enemy", self, moves_log)

#             update the new_board after this move - remove the captured black piece
                for black in new_board.blacks:
                    if black.y == old.middle(new).y and black.x == old.middle(new).x:
                        new_board.blacks.remove(black)
                        break
                new_board.world[old.middle(new).y][old.middle(new).x] = None
                
            else:
                if abs(new.y - old.y) != abs(new.x - old.x):
                    raise ValueError("You cannot move there - too far", self, moves)
                
#                 check if there is a black piece captures
                where = old.add(yi, xi)
                captured = []
                while where.y != new.y:
                    if self.isBlack(where):
                        captured += [where]
                        if not self.isEmpty(where.add(yi, xi)):
                            raise ValueError("You cannot capture more than one piece at one!", self, moves_log)
                    if self.isWhite(where):
                        raise ValueError("You cannot move over your own piece!", self, moves_log)
                    where = where.add(yi, xi)
                    
                if len(captured) == 0:
                    raise ValueError("You have to capture an enemy's piece", self, moves_log)
                
#             update the new_board after this move - remove the captured black piece
                for captured_position in captured:
                    for black in new_board.blacks:
                        if black.y == captured_position.y and black.x == captured_position.x:
                            new_board.blacks.remove(black)
                            break
                    new_board.world[captured_position.y][captured_position.x] = None
                
        
        else:
            if not piece.king:
                if new.y - old.y != 1 or abs(new.x - old.x) != 1:
                    raise ValueError("The position is inaccessible for this piece", self, moves_log)
            else:
                if abs(new.y - old.y) != abs(new.x - old.x):
                    raise ValueError("You can only move diagonally", self, moves_log)
                
                where = old.add(yi, xi)
                while where.y != new.y:
                    if not self.isEmpty(where):
                        raise ValueError("You cannot move over this square", self, moves_log)
                    where = where.add(yi, xi)
                
                if not self.isEmpty(where):
                    raise ValueError("You cannot move to this square", self, moves_log)
        
        
#       update the new_board after this move - the white piece who moved
        for white in new_board.whites:
            if white.y == old.y and white.x == old.x:
                white.x = new.x
                white.y = new.y
        new_board.world[new.y][new.x] = new_board.world[old.y][old.x]
        new_board.world[old.y][old.x] = None
        
        return new_board
    
    
#     display the board
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