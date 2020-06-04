import os
import random
import cherrypy
import battlesnake


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
            "head": "silly",  # Battlesnake head
            "tail": "bolt",  # Battlesnake tail
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
        snakes = data["board"]["snakes"]
        print(f"Data in move is: {data}")

        moves = battlesnake.generate_possible_moves(your_body)

        # Iterate over moves backwards so that we can remove from the array without affecting order
        for move in reversed(moves):
            validated = battlesnake.validate_move(data["board"], data["you"], snakes, move)

            # Remove move if it was not validated. This means the move would
            # destroy our snake
            if not validated:
                moves.remove(move)
                print(f"Removed move: {move}, it could not be validated. The moves left are {moves}")

        final_move = battlesnake.pick_move(moves)
        print(f"FINAL MOVE: {final_move}")

        return {"move": final_move.direction, "shout": "All your base are belong to us."}


    @cherrypy.expose
    @cherrypy.tools.json_in()
    def end(self):
        # This function is called when a game your snake was in ends.
        # It's purely for informational purposes, you don't have to make any decisions here.
        data = cherrypy.request.json

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
