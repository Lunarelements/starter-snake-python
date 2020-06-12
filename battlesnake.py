"""
Code used to make battlesnake move decisions. To be
used by the server.py code. Modified based on Aurora Walker's code:
https://github.com/aurorawalker/starter-snake-python
"""
import random
import sys
from node import Node

# Use a dictionary to avoid if/else when determining the change in position.
MOVE_LOOKUP = {"left": -1, "right": 1, "up": 1, "down": -1}

# List of all possible moves
POSSIBLE_MOVES = ["up", "down", "left", "right"]


def predict_future_position(current_head, next_move):
    """
    Given the current snake head position, and a proposed move,
    returns what the new snake head position would be.
    """
    # Get a clean copy, otherwise will modify the current head!
    future_head = current_head.copy()

    if next_move in ["left", "right"]:
        # Moving left means decreasing x by 1, right increase by 1.
        future_head["x"] = current_head["x"] + MOVE_LOOKUP[next_move]
    elif next_move in ["up", "down"]:
        # Moving up means increasing y by 1, down decrease by 1.
        future_head["y"] = current_head["y"] + MOVE_LOOKUP[next_move]
    return future_head

def validate_move(board, you, snakes, move):
    """
    Basic set of logical checks that only prevent disaster. This function is not
    responsible for picking a move, it is responsible for saying if that move
    is desireable by changing the moves certainty score.
    Return True if scored fully, False if not. (and move should be removed from list)
    """

    # Iterate through all the snakes and run collision and head to head validations
    for snake in snakes:

        # Don't need to run head prediction on yourself
        if(snake["name"] != you["name"]):
            move.score += predict_head(you, move.coordinates(), snake, board.width, board.height)

    return True


def predict_head(you, future_head, other, width, height):
    other_moves = generate_possible_moves(other["body"], width, height)
    print(f'Predicting head of {other["name"]}: {other_moves}')

    # Our snakes head will collide with other snakes possible move
    for move in other_moves:
        if future_head == move.coordinates():
            print(f'Future head {future_head} collides with future move of {other["name"]}: {other_moves}')
        
            # Their snake is shorter or equal to ours, this means death D:
            # TODO: Give score if equal because chances are their snake will want to avoid if equal
            # TODO: Look to see if food will affect this matchup
            if other["length"] >= you["length"]:
                # TODO - make the snake take a chance(score) to hit other snake if the other moves run into wall or itself
                print(f'Snake\'s length is {you["length"]}, theirs is {other["length"]}. This possible collision is last resort.')
                return -10
            return -0.5
    return 0


def generate_possible_moves(body, width, height):
    """
    Generates all possible next moves for a snake given its body. It will remove the
    move that runs into its own neck. It will not check any other conditions of
    validity for the moves. (This must be done by other parts of the program)
    Return a list containing the move objects for the possible next moves of the snake.
    """
    all_possible_moves = []
    head = body[0]
    neck = body[1]

    # Generate the coordinates for every possible next move
    for next_move in POSSIBLE_MOVES:
        future_position = predict_future_position(head, next_move)

        print(f"Future head on a {next_move} is as follows: {future_position}")

        # If the future position is not in the snake's own neck add it to the list of possible moves
        if future_position != neck and future_position["x"] >= 0 and future_position["x"] < width and future_position["y"] >= 0 and future_position["y"] < height:
            all_possible_moves.append(Node(True, future_position["x"], future_position["y"]))

    print(f"All possible moves to be evaluated: {all_possible_moves}")

    return all_possible_moves