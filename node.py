class Node:

    def __init__(self, safe, x, y):
        self.safe = safe
        self.x = x
        self.y = y
        self.certainty = 0
        self.g_cost = 0
        self.h_cost = 0
        self.parent = None
    
    def __repr__(self):
        return str(self.__dict__)

    def __eq__(self, other) : 
        if self.__class__ != other.__class__:
            return False
        return self.__dict__ == other.__dict__

    def __hash__(self):
        return hash(f"{self.x}{self.y}")

    def f_cost(self):
        return self.g_cost + self.h_cost
    
    def coordinates(self):
        return {'x': self.x, 'y': self.y}

    def get_direction(self, head):
        if(head["x"] == self.x):
            return "up" if self.y - head["y"] > 0 else "down"
        return "right" if self.x - head["x"] > 0 else "left"