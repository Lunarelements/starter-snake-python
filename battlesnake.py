"""
Code used to make battlesnake move decisions. To be
used by the server.py code. Modified based on Aurora Walker's code:
https://github.com/aurorawalker/starter-snake-python
"""
import random
from move import Move

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


def can_avoid_wall(future_head, board):
    """
    Check to sees if the proposed future_head will hit the board wall.
    Return True if the proposed future_head avoids a wall, False if it means
    you will hit a wall.
    """
    x = future_head["x"]
    y = future_head["y"]

    if x < 0 or y < 0 or x > (board["width"] - 1) or y > (board["height"] - 1):
        return False
    return True


def can_avoid_snakes(future_head, snake_bodies):
    """
    Return True of the proposed move avoids running into any list of snakes,
    False if the next move exists in a snake body square.
    Recommend taking the default data from the board snakes as per the battlesnake
    API. Note that the list of board snakes includes yourself!
    TODO - this is basic, may want to add in a check to see if any heads are
    about to eat food, and may extend by a square! Does the tail grow first,
    or does the head grow? Find out what happens in the game and see if we need
    to check for if a snake suddenly grows.
    TODO - what about snake tails leaving in the next move? A tail may be a
    safe place to move into (assuming no food as in above scenario). In which
    case, this logic needs to be modified to exclude the tail, as that is a safe
    square to move into. LOOK INTO THIS LATER when implementing chicken snake
    approach, as that is a key concept with that!

    @:param: snake_bodies list of dictionary of snake bodies
        [
            {'id': 'abc', 'name': 'Snek' ... 'body': [{'x': 1, 'y': 2}, {'x': 1, 'y': 3}, {'x': 1, 'y': 4}]},
            {'id': 'efg', 'name': 'SNAKE' ...'body': [{'x': 4, 'y': 2}, {'x': 4, 'y': 3}, {'x': 4, 'y': 4}]},
            {'id': 'hij', 'name': 'you' ...'body': [{'x': 1, 'y': 10}, {'x': 1, 'y': 9}, {'x': 1, 'y': 8}]}
        ]
    """
    for snake in snake_bodies:
        # Check to see if move will hit a currently known coordinate
        if future_head in snake["body"]:
            return False

    return True


def validate_move(board, snakes, move):
    """
    Basic set of logical checks that only prevent disaster. This function is not
    responsible for picking a move, it is responsible for saying if that move
    is desireable by changing the moves certainty score.
    Return True if scored fully, False if not. (and move should be removed from list)
    """

    # Move hits a border and is never going to be a good choice. 
    # Return False so that it can be removed from the choices and to save compute time.
    avoided_walls = can_avoid_wall(move.coordinates(), board)
    print(f"future_head {move.coordinates()}: can_avoid_wall {avoided_walls}")
    if not avoided_walls:
        return False

    # Move hits yourself or another snake and is never going to be a good choice.
    # Return False so that it can be removed from the choices and to save compute time.
    avoided_snakes = can_avoid_snakes(move.coordinates(), snakes)
    print(f"future_head {move.coordinates()}: can_avoid_snakes {avoided_snakes}")
    if not avoided_snakes:
        return False

    # TODO REMOVE THIS WHEN ACTUAL SCORES EXIST
    move.score += 0.1

    return True


def predict_head():
    pass
     #   TODO - and on that note, what about anticipating another snakes head, and
    #if you are destined to occupy the same square another snake is about to?
    #That might be logic for somwhere else - I'll have to think about that.
        #     # Check to see if move will hit a future head position of another snake
        # # TODO - make the snake take a chance to hit other snake if the other moves run into wall or itself
        # # TODO - remove dependance on hardcoded name
        # if snake["name"] != "BabySnek":
        #     # TODO - allow move if longer than snake
        #     other_future_positions = predict_all_future_positions(snake["body"][0])
        #     if future_head in all_future_positions:
        #         print(f'Future head {future_head} collides with future move of {snake["name"]}: {other_future_positions}')
        #         return False


def generate_possible_moves(body):
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
        if future_position != neck:
            all_possible_moves.append(Move(next_move, future_position["x"], future_position["y"]))

        print(f"Possible moves to be evaluated: {all_possible_moves}")

    return all_possible_moves

def pick_move(moves):
    """
    Find the best move from the list by certainty score. This is the move we
    would want our snake to take.
    Return the move with the best score.
    """

    print(f"Final moves under consideration: {moves}")
    
    # Placeholder move and move to do by default if no moves are available
    best_move = Move("left", -1, -1)

    # Find the move with the best score
    for move in moves:
        if move.score > best_move.score:
            best_move = move
    return best_move