class Move:

    def __init__(self, direction, x, y, score=0):
        self.direction = direction
        self.x = x
        self.y = y
        self.score = score

    def __repr__(self):
        return str(self.__dict__)

    def __eq__(self, other) : 
        if self.__class__ != other.__class__:
            return False
        return self.__dict__ == other.__dict__

    def coordinates(self):
        return {'x': self.x, 'y': self.y}