from collections import deque, defaultdict
import re

INPUT_FILE = "input.txt"

WALL = '#'
TILE = '.'
CLOCKWISE = 'R'
COUNTERCLOCKWISE = 'L'
UP, DOWN, LEFT, RIGHT = '^', 'v', '<', '>'
FACING_POINTS = {
    RIGHT: 0,
    DOWN: 1,
    LEFT: 2,
    UP: 3
}
MOVES = {
    UP: (0, 1),
    DOWN: (0, -1),
    LEFT: (-1, 0),
    RIGHT: (1, 0)
}
TURN_COUNTERCLOCKWISE = {
    UP: RIGHT,
    RIGHT: DOWN,
    DOWN: LEFT,
    LEFT: UP
}
TURN_CLOCKWISE = {
    UP: LEFT,
    LEFT: DOWN,
    DOWN: RIGHT,
    RIGHT: UP
}

def p_add(a, b):
    xa, ya = a
    xb, yb = b
    return xa + xb, ya + yb


def read_input():
    lines = open(INPUT_FILE, "r").readlines()
    total = 0
    last_line = lines[len(lines) - 1]
    moves = re.split(r"(?=R)|(?=L)|(?<=R)|(?<=L)", last_line)
    print("moves", last_line, moves)
    # cache tiles and walls on board
    board = {}
    start = None
    # get dimensions of board
    max_x = 0
    max_y = len(lines) - 2
    for y in range(len(lines) - 1):
        line = lines[y][:-1]
        max_x = max(max_x, len(line))
        for x in range(len(line)):
            char = line[x]
            loc = (x + 1, y + 1)
            if char is WALL or char is TILE:
                # cache tiles and walls, ignore empty spaces
                board[loc] = char
                # first tile is the start position
                if start is None and char is not WALL:
                    start = loc

        print(line)
    print(board)
    print('board size', max_x, max_y)
    right_loop, left_loop, up_loop, down_loop = get_shortcuts(board, max_x, max_y)
    return start, moves, (board, right_loop, left_loop, up_loop, down_loop)


def pprint(board, steps_taken):
    xm = 16
    ym = 12
    print(" ---- board -----")
    for y in reversed(range(ym+1)):
        print("{:02d}".format(y), end='')
        for x in range(xm+1):
            p = (x, y)
            tile = board.get(p)
            if tile is None:
                tile = ' '
            if steps_taken.get(p) is not None:
                tile = steps_taken.get(p)
            print(tile, end='')
        print()
    print(" ----------------")

def get_shortcuts(board, xm, ym):
    # cache holds shortcuts to loop around the board
    right_loop = {}
    left_loop = {}
    up_loop = {}
    down_loop = {}

    for y in range(ym):
        for x in range(xm):
            loc = (x, y)
            if board.get(loc) is not None and right_loop.get(y) is None:
                right_loop[y] = loc

    for y in range(ym):
        for x in reversed(range(xm)):
            loc = (x, y)
            if board.get(loc) is not None and left_loop.get(y) is None:
                left_loop[y] = loc

    for x in range(xm):
        for y in range(ym):
            loc = (x, y)
            if board.get(loc) is not None and up_loop.get(x) is None:
                up_loop[x] = loc

    for x in range(xm):
        for y in reversed(range(ym)):
            loc = (x, y)
            if board.get(loc) is not None and down_loop.get(x) is None:
                down_loop[x] = loc
    return right_loop, left_loop, up_loop, down_loop




def walk(maps, from_loc, direction, steps):
    board, right_loop, left_loop, up_loop, down_loop = maps
    curr_loc = from_loc
    steps_taken = {}
    for i in range(steps):
        next_loc = p_add(curr_loc, MOVES[direction])
        if board.get(next_loc) is None:
            x, y = next_loc
            if direction is RIGHT:
                next_loc = right_loop[y]
            elif direction is LEFT:
                next_loc = left_loop[y]
            elif direction is UP:
                next_loc = up_loop[x]
            elif direction is DOWN:
                next_loc = down_loop[x]
        steps_taken[curr_loc] = direction
        if board.get(next_loc) == WALL:
            break
        steps_taken[next_loc] = direction
        curr_loc = next_loc
    return curr_loc, steps_taken



def problem_one():
    loc, moves, maps = read_input()
    direction = RIGHT
    all_steps_taken = {}
    print("INITIAL. printing board upside down so row 1 is at the bottom")
    pprint(maps[0], {loc: direction})
    for move in moves:
        # print(f' at {loc} moving {move}')
        if move is CLOCKWISE:
            direction = TURN_CLOCKWISE[direction]
            all_steps_taken[loc] = direction
        elif move is COUNTERCLOCKWISE:
            direction = TURN_COUNTERCLOCKWISE[direction]
            all_steps_taken[loc] = direction
        else:
            loc, steps_taken = walk(maps, loc, direction, int(move))
            all_steps_taken.update(steps_taken)
        # print(f'finished at {loc}')
        # pprint(maps[0], all_steps_taken)

    x, y = loc
    face = FACING_POINTS[direction]
    row, col = y, x
    ans = 1000 * row + 4 * col + face
    print(f"\nP1 ans row {row} col {col} face ({direction}). ans = {ans}")


problem_one()

# problem_two()
