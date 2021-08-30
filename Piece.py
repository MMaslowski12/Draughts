class Piece:

    def __init__(self, white, king, y, x):
        self.white = white
        self.king = king
        self.x = x
        self.y = y



    @staticmethod
    def whitePiece(y, x, king=False):
        return Piece(True, king, y, x)

    @staticmethod
    def blackPiece(y, x, king=False):
        return Piece(False, king, y, x)

    def changeColour(self):
        self.white = not self.white

    def move_symmetrically(self):
        self.x = 9 - self.x
        self.y = 9 - self.y



    def crown(self):
        self.king = True