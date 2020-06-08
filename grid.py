from node import Node

class Grid:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = self.createGrid(width, height)

    def __repr__(self):
        return str(self.__dict__)

    def __eq__(self, other) : 
        if self.__class__ != other.__class__:
            return False
        return self.__dict__ == other.__dict__

    def createGrid(self, width, height):
        # Battlesnake coordinate system starts from the bottom left corner, flip the y values
        # This will help programming later
        return [[Node(True, i, width - 1 - j) for i in range(width)] for j in reversed(range(height))]

    def printGrid(self):
        print('\n'.join([''.join([" . " if item.safe else " x " for item in row]) for row in reversed(self.grid)]))

    def printGridCertainty(self):
        print('\n'.join([''.join([ f'{item.certainty:6}' for item in row]) for row in reversed(self.grid)]))

    def insert_snakes(self, snakes):
        """
        Given a list of snakes, change the grid to show that
        the space is not safe.
        """
        for snake in snakes:
            for segment in snake["body"]:
                self.grid[segment["y"]][segment["x"]].safe = False
                self.grid[segment["y"]][segment["x"]].certainty = -100
        
        print(f"Current board:")
        self.printGrid()

    def insert_path(self, path):
        """
        Given a list of nodes, change the grid to show that
        the space has more certainty.
        """
        for node in path:
            self.grid[node.y][node.x].certainty += 0.1
        
        print(f"Current certainty:")
        self.printGridCertainty()

    def get_neighbours(self, node):
        neighbours = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                if x == 0 and y == 0 or y == x or y == -x or -y == x:
                    continue

                # Make sure our neighbours acutally exist on the grid
                neighbour_x = node.x + x
                neighbour_y = node.y + y

                if neighbour_x >= 0 and neighbour_x < self.width and neighbour_y >= 0 and neighbour_y < self.height:
                    print(f'Neighbour at "x" : {neighbour_x}, "y" : {neighbour_y}')
                    neighbours.append(self.grid[neighbour_y][neighbour_x])
        
        return neighbours