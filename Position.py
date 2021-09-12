#experimental changes
class Position:
    def __init__(self, y, x):
        self.y = y
        self.x = x
        
    def add(self, y, x):
        return Position(self.y + y, self.x + x)
    
    def middle(self, other):
        return Position(int((self.y+other.y)/2), int((self.x+other.x)/2))
    # Optimization
    # An alternative change
