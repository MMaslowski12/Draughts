from Position import Position

# A class to keep a piece
# It stores its location, a boolean which us if its white and a boolean which tells us if it's a king
class Piece:
    def __init__(self, white, king, y, x):
        self.white = white
        self.king = king
        self.x = x
        self.y = y
    
    # Create a white piece on a given position
    @staticmethod
    def whitePiece(y, x, king=False):
        return Piece(True, king, y, x)
    # Create a black piece on a given position
    @staticmethod
    def blackPiece(y, x, king=False):
        return Piece(False, king, y, x)
    
    def changeColour(self):
        self.white = not self.white
        
    # Change position to one on the opposite side of a board
    def move_symmetrically(self):
        self.x = 9 - self.x
        self.y = 9 - self.y
    
    # Return piece's location as a Position class
    def position(self):
        return Position(self.y, self.x)
