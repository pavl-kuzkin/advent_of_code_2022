import re
from collections import deque

INPUT_FILE = "input.txt"
ELF = '#'
NORTH, SOUTH, WEST, EAST = 'N', 'S', 'W', 'E'
MOVE_ORDER = [NORTH, SOUTH, WEST, EAST]
MOVES = {
    NORTH: [(0, 1), (1, 1), (-1, 1)],
    SOUTH: [(0, -1), (1, -1), (-1, -1)],
    WEST: [(-1, 0), (-1, 1), (-1, -1)],
    EAST: [(1, 0), (1, 1), (1, -1)]
}


def smallest_rect(elves: set):
    x1, x2, y1, y2 = 0, 0, 0, 0
    for elf in elves:
        x, y = elf
        x1, x2, y1, y2 = min(x1, x), max(x2, x), min(y1, y), max(y2, y)
    return x1, x2, y1, y2


def pprint_elves(elves: set):
    x1, x2, y1, y2 = smallest_rect(elves)
    for y in reversed(range(y1 - 1, y2 + 2)):
        # print('Z' if y == 0 else y%10, end=' ')
        print("{:02d}".format(y), end='')
        for x in range(x1 - 1, x2 + 2):
            c = ELF if (x, y) in elves else '.'
            print(c, end=' ')
        print()
    print(' ', end=' ')
    for x in range(x1 - 1, x2 + 2):
        print("{:02d}".format(x), end='')
    print()


def p_add(a, b):
    xa, ya = a
    xb, yb = b
    return xa + xb, ya + yb


def distance(a, b):
    xa, ya = a
    xb, yb = b
    return abs(xb - xa) + abs(yb - ya)


def read_input():
    lines = open(INPUT_FILE, "r").readlines()
    elves = set()
    for (y, line) in enumerate(reversed(lines)):
        for (x, char) in enumerate(line):
            if char == ELF:
                elves.add((x, y))
    print(elves)
    return elves


def has_neighbor(elf: tuple, all_elves: set, directions: list):
    for direction in directions:
        moves = MOVES[direction]
        for move in moves:
            new_position = p_add(elf, move)
            if new_position in all_elves:
                return True
    return False


def propose_moves(elf: tuple, all_elves: set, direction_order: deque):
    if not has_neighbor(elf, all_elves, MOVE_ORDER):
        # If no other Elves are in one of those eight positions,
        # the Elf does not do anything
        return None
    # Otherwise, the Elf looks in each of four directions in the following
    # order and proposes moving one step in the first valid direction:
    for direction in direction_order:
        if not has_neighbor(elf, all_elves, [direction]):
            return MOVES[direction][0]
    return None


def plan_moves(elves: set, direction_order: deque):
    planned_moves = {}
    for elf in elves:
        move = propose_moves(elf, elves, direction_order)
        if move is not None:
            new_location = p_add(elf, move)
            if new_location in planned_moves:
                # more than one want this space so none ge tit
                planned_moves[new_location] = None
            else:
                planned_moves[new_location] = elf
        # print("elf", elf, "proposed", new_location)
    print("moves planned", planned_moves)
    if not planned_moves:
        print("Moving ended")
        raise Exception("we done")

    return planned_moves


def turn(elves: set, direction_order: deque):
    locs = plan_moves(elves, direction_order)
    for (new_loc, old_loc) in locs.items():
        if old_loc is None:
            continue
        elves.remove(old_loc)
        elves.add(new_loc)
    return elves


def calc_score(elves: set):
    # count the number of empty ground tiles contained by the smallest rectangle that contains every Elf.
    x1, x2, y1, y2 = smallest_rect(elves)
    return (x2 - x1 + 1) * (y2 - y1 + 1) - len(elves)


def problem_one():
    elves = read_input()
    direction_order = deque(MOVE_ORDER)
    print("initial")
    pprint_elves(elves)
    for i in range(10):
        elves = turn(elves, direction_order)
        print("-- round", i + 1, direction_order)
        direction_order.append(direction_order.popleft())
        pprint_elves(elves)

    print("P1 ans", calc_score(elves))


# problem_one()

def problemTwo():
    elves = read_input()
    direction_order = deque(MOVE_ORDER)
    print("initial")
    pprint_elves(elves)
    for i in range(4000):
        try:
            elves = turn(elves, direction_order)
        except:
            print("P2 ans", i + 1)
            return
        print("-- round", i + 1, direction_order)
        direction_order.append(direction_order.popleft())
        pprint_elves(elves)

    print("P2 ans", calc_score(elves))



problemTwo()
