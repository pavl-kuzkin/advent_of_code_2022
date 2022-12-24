import re
from collections import deque
from functools import cmp_to_key

INPUT_FILE = "ez-input.txt"
ELF = '#'
NORTH, SOUTH, WEST, EAST = 'N', 'S', 'W', 'E'
MOVE_ORDER = [NORTH, SOUTH, WEST, EAST]
MOVES = {
    NORTH: [(0, 1), (1, 1), (-1, 1)],
    SOUTH: [(0, -1), (1, -1), (-1, -1)],
    WEST: [(-1, 0), (-1, 1), (-1, -1)],
    EAST: [(1, 0), (1, 1), (1, -1)]
}


def pprint_elves(elves: set):
    x1, x2, y1, y2 = 0, 0, 0, 0
    for elf in elves:
        x, y = elf
        x1, x2, y1, y2 = min(x1, x), max(x2, x), min(y1, y), max(y2, y)
    for y in reversed(range(y1-1, y2+2)):
        # print('Z' if y == 0 else y%10, end=' ')
        print("{:02d}".format(y), end='')
        for x in range(x1-1, x2+2):
            c = ELF if (x, y) in elves else '.'
            print(c, end='  ')
        print()
    print(' ', end=' ')
    for x in range(x1-1, x2+2):
        print("{:02d}".format(x), end=' ')
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
        return 0, 0
    # Otherwise, the Elf looks in each of four directions in the following
    # order and proposes moving one step in the first valid direction:
    for direction in direction_order:
        if not has_neighbor(elf, all_elves, [direction]):
            return MOVES[direction][0]


def problemOne():
    elves = read_input()
    direction_order = deque(MOVE_ORDER)
    pprint_elves(elves)
    for elf in elves:
        proposed = propose_moves(elf, elves, direction_order)
        print("elf", elf, "proposed", proposed)
    print("P1", 0)


problemOne()

# def problemTwo():
#
#
# problemTwo()
