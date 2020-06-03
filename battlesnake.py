"""
Code used to make battlesnake move decisions. To be
used by the server.py code. Modified based on Aurora Walker's code 
https://github.com/aurorawalker/starter-snake-python
"""
import random

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
        # Moving left means decreasing x by 1, right increase by 1
        future_head["x"] = current_head["x"] + MOVE_LOOKUP[next_move]
    elif next_move in ["up", "down"]:
        # moving up means increasing y by 1, down decrease by 1
        future_head["y"] = current_head["y"] + MOVE_LOOKUP[next_move]
    return future_head


def predict_all_future_positions(current_head):
    """
    Given the current snake head position,
    returns a list of all possible snake head positions.
    """

    positions = []

    for move in POSSIBLE_MOVES:
        positions.append(predict_future_position(current_head, move))

    return positions


def can_avoid_wall(future_head, board):
    """
    Return True if the proposed future_head avoids a wall, False if it means
    you will hit a wall.
    """
    result = True

    x = int(future_head["x"])
    y = int(future_head["y"])

    if x < 0 or y < 0 or x > (board["width"] - 1) or y > (board["height"] - 1):
        result = False
    return result


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
    TODO - and on that note, what about anticipating another snakes head, and
    if you are destined to occupy the same square another snake is about to?
    That might be logic for somwhere else - I'll have to think about that.
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
        # Check to see if move will hit a future head position of another snake
        # TODO - remove dependance on hardcoded name
        if snake["name"] != "BabySnek":
            # TODO - allow move if longer than snake
            all_future_positions = predict_all_future_positions(snake["body"][0])
            if future_head in all_future_positions:
                print(f'Future head {future_head} collides with future move of {snake["name"]}: {all_future_positions}')
                return False

    return True


def validate_move(your_body, board, snakes, next_move):
    """
    Basic set of logical checks that only prevent disaster. This function is not
    responsible for picking a move, it is responsible for saying if that move
    if safe.
    Return True if safe, False if not (and another move is needed).
    """
    current_head = your_body[0]
    future_head = predict_future_position(current_head, next_move)
    print(f"Future head on a {next_move} is as follows: {future_head}")

    safe_wall = can_avoid_wall(future_head, board)
    safe_body = can_avoid_snakes(future_head, snakes)

    print(f"future_head {future_head}: safe_wall {safe_wall}, safe_body {safe_body}")
    is_valid_move = safe_wall and safe_body

    return is_valid_move


def choose_move_chaos(data):
    """
    The chaos strategy relies on randomly choosing a next move, any move, to
    keep the competition guessing!
    return a potential future_head of the snake as a dict {'x': 1, 'y': 1}
    """

    move = random.choice(POSSIBLE_MOVES)
    return move