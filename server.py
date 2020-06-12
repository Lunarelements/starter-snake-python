import os
import random
import cherrypy
import battlesnake
from node import Node
from grid import Grid
import pathfinding


"""
This is a simple Battlesnake server written in Python.
For instructions see https://github.com/BattlesnakeOfficial/starter-snake-python/README.md
"""


class Battlesnake(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        # This function is called when you register your Battlesnake on play.battlesnake.com
        # It controls your Battlesnake appearance and author permissions.
        # TIP: If you open your Battlesnake URL in browser you should see this data.
        return {
            "apiversion": "1",
            "author": "Lunarelements",  # Battlesnake username
            "color": "#13807C",  # Battlesnake color
            "head": "evil",  # Battlesnake head
            "tail": "hook",  # Battlesnake tail
        }

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def start(self):
        # This function is called everytime your snake is entered into a game.
        # cherrypy.request.json contains information about the game that's about to be played.
        data = cherrypy.request.json

        print(f"START OF NEW GAME {data['game']['id']}")
        return "ok"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        # This function is called on every turn of a game. It's how your snake decides where to move.
        # Valid moves are "up", "down", "left", or "right".
        data = cherrypy.request.json

        # Data structure holds head, body, then tail
        your_body = data["you"]["body"]
        your_head = data["you"]["head"]
        board = data["board"]
        snakes = board["snakes"]
        print(f"Data in move is: {data}")

        # Create a grid of nodes for to represent the map
        board_grid = Grid(board["width"], board["height"])

        # Insert the snakes so that we know where we can't go
        board_grid.insert_snakes(snakes)

        rooms = []
        food_paths = []

        # Run pathfinding algorith on every food point and pick the shortest one
        # if data["you"]["health"] < 30:
        for food in board["food"]:
            path = pathfinding.find_path(board_grid, board_grid.grid[your_head["y"]][your_head["x"]], board_grid.grid[food["y"]][food["x"]])
            if path is not None:
                food_paths.append(path)
        
        board_grid.insert_paths(food_paths)
        print(f"Current certainty after food:")
        board_grid.printGridCertainty()

        moves = battlesnake.generate_possible_moves(your_body, board["width"], board["height"])
        for move in moves:
            rooms.append(pathfinding.find_room(board_grid, board_grid.grid[move.y][move.x], []))

        board_grid.insert_rooms(rooms)
        print(f"Current certainty after room:")
        board_grid.printGridCertainty()

        best_node = board_grid.pick_move(board_grid.grid[your_head["y"]][your_head["x"]])
        
        final_move = best_node.get_direction(your_head)
        print(f"FINAL MOVE: {final_move}")

        return {"move": final_move, "shout": "All your base are belong to us."}


    @cherrypy.expose
    @cherrypy.tools.json_in()
    def end(self):
        # This function is called when a game your snake was in ends.
        # It's purely for informational purposes, you don't have to make any decisions here.

        print("END OF GAME")
        return "ok"


if __name__ == "__main__":
    server = Battlesnake()
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update(
        {"server.socket_port": int(os.environ.get("PORT", "8080")),}
    )
    print("Starting Battlesnake Server...")
    cherrypy.quickstart(server)
