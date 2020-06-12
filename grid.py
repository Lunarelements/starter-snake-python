from node import Node
import random

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
        print('\n'.join([''.join([ f'{item.certainty:8.2f}' for item in row]) for row in reversed(self.grid)]))

    def insert_snakes(self, snakes):
        """
        Given a list of snakes, change the grid to show that
        the space is not safe.
        """
        for snake in snakes:
            for index, segment in enumerate(snake["body"]):
                # Ignore tail, it will have moved by next turn
                # TODO: Check if food is in front of snake, tail will not move
                if(index != len(snake["body"]) - 1):
                    self.grid[segment["y"]][segment["x"]].safe = False
                    self.grid[segment["y"]][segment["x"]].certainty = -100
        
        print(f"Current board:")
        self.printGrid()

    def insert_paths(self, paths):
        """
        Given a list of path, change the grid to show that
        the shortest path has more certainty.
        """
        if paths is None or not paths:
            return

        path_min_size = 0
        path_min_index = 0

        for index, path in enumerate(paths):
            if len(path) < path_min_size:
                path_min_size = len(path)
                path_min_index = index
        
        for node in paths[path_min_index]:
            self.grid[node.y][node.x].certainty += 0.5

    def insert_rooms(self, rooms):
        """
            Given a list of rooms, change the grid to show that
            the room with the most space.
        """
        if rooms is None or not rooms :
            return

        room_max_size = 0
        room_max_index = 0

        for index, room in enumerate(rooms):
            if len(room) > room_max_size:
                room_max_size = len(room)
                room_max_index = index
        
        for node in rooms[room_max_index]:
            self.grid[node.y][node.x].certainty += 0.2

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
                    # print(f'Neighbour at "x" : {neighbour_x}, "y" : {neighbour_y}')
                    neighbours.append(self.grid[neighbour_y][neighbour_x])
        
        return neighbours

    def pick_move(self, head):
        """
        Find the best move from the grid by certainty score. This is the move we
        would want our snake to take.
        Return the move with the best score.
        """

        neighbours = self.get_neighbours(head)
        # Give random order so that ties don't always go the same direction
        random.shuffle(neighbours)

        best_node = neighbours[0]

        # Find the node with the best score
        for node in neighbours:
            if node.certainty > best_node.certainty:
                best_node = node
        return best_node