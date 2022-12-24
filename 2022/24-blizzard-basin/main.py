import re
from collections import deque, defaultdict

INPUT_FILE = "input.txt"
WALL = '#'
EMPTY = '.'
UP, DOWN, LEFT, RIGHT = '^', 'v', '<', '>'
WINDS = set([UP, DOWN, LEFT, RIGHT])
MOVES = [
    (0, 1),
    (0, -1),
    (-1, 0),
    (1, 0),
    (0, 0)
]


def p_add(a, b):
    xa, ya = a
    xb, yb = b
    return xa + xb, ya + yb


def smallest_rect(elves: set):
    x1, x2, y1, y2 = 0, 0, 0, 0
    for elf in elves:
        x, y = elf
        x1, x2, y1, y2 = min(x1, x), max(x2, x), min(y1, y), max(y2, y)
    return x1, x2, y1, y2


def p_add(a, b):
    xa, ya = a
    xb, yb = b
    return xa + xb, ya + yb


def distance(a, b):
    xa, ya = a
    xb, yb = b
    return abs(xb - xa) + abs(yb - ya)


def hash_game_state(game_state):
    location, winds, score = game_state
    hashes = [str(location)]
    if winds == -1:
        print("debug winds", winds)
    for k in winds:
        hashes.append(str(k))
    return "-".join(hashes)


def read_input():
    lines = open(INPUT_FILE, "r").readlines()
    height = len(lines) - 2  # minus new line and two #
    width = len(lines[0]) - 3  # minus new line and two #
    start = (0, height)
    end = (width - 1, -1)
    winds = []
    print("input:")
    for (y, line) in enumerate(reversed(lines)):
        print(y, end=' ')
        for x in range(len(line.strip())):
            char = line[x]
            print(char, end=' ')
            if char in WINDS:
                wind_pos = (x - 1, y - 1)
                winds.append((wind_pos, char))
        print()
    print("input cached:")
    print(winds)
    print("start", start, "end", end)
    print("pretty print wind locations")
    pprint_winds(winds, (width, height), start)
    print("custom hashing of game state check:", hash_game_state((start, winds, 0)))
    print()
    return winds, (width, height), start, end


def find_wind(location, winds):
    found = 0
    d = None
    for (wind_loc, dir) in winds:
        if wind_loc == location:
            found += 1
            d = dir
    if found == 1:
        return str(d)
    elif found == 0:
        return '.'
    else:
        return str(found)

def pprint_winds(winds: list, size: tuple, my_pos: tuple):
    sep = ' '
    x_max, y_max = size
    for y in reversed(range(-1, y_max+1)):
        print("{:02d}".format(y), end=' ')
        for x in range(-1, x_max+1):
            loc = (x, y)
            if loc == my_pos:
                print('E', end=sep)
            else:
                print(find_wind((x, y), winds), end=sep)
        print()
    print(' ', end=sep)
    for x in range(-1, x_max+1):
        if 0 <= x < 10:
            print(' ', end='')
            print(x, end='')
        else:
            print("{:02d}".format(x), end='')

    print()


def wind_loc(init_point: tuple, direction: str, minutes: int, cave_size: tuple):
    x, y = init_point
    x_max, y_max = cave_size
    if direction == UP:
        return x, (y + minutes) % y_max
    elif direction == DOWN:
        return x, (y - minutes) % y_max
    elif direction == LEFT:
        return (x - minutes) % x_max, y
    elif direction == RIGHT:
        return (x + minutes) % x_max, y


def winds_locs(init_winds: list, minutes: int, cave_size: tuple):
    current_winds = []
    for (loc, dir) in init_winds:
        current_loc = wind_loc(loc, dir, minutes, cave_size)
        current_winds.append((current_loc, dir))
    return current_winds




def count_wind(location, winds):
    found = 0
    for (wind_loc, dir) in winds:
        if wind_loc == location:
            found += 1
    return found

def valid_moves(location: tuple, winds: list, minutes: int, cave_size: tuple, start, end):
    valid = []
    new_winds = winds_locs(winds, minutes, cave_size)
    x_max, y_max = cave_size
    # pprint_winds(current_winds, cave_size)
    if location == end:
        return []
    for move in MOVES:
        new_loc = p_add(location, move)
        x, y = new_loc
        if new_loc == end:
            return [(new_loc, new_winds, minutes)]
        if new_loc != start and (x < 0 or y < 0 or y > y_max - 1 or x > x_max - 1):
            continue
        if count_wind(new_loc, new_winds) == 0:
            game_state = (new_loc, new_winds, minutes)
            valid.append(game_state)
    return valid


def bfs(initial_winds: list, cave_size: tuple, start, end):
    print("\n== BFS == \n")
    q = deque()
    # graph node is your location + wind location
    # graph edges are possible moves
    initial_game_state = (start, initial_winds, 0)
    q.append(initial_game_state)
    game_state_times = {hash_game_state(initial_game_state): 0}
    high_score = 1000
    count_iterations = 0
    while q:
        count_iterations += 1
        game_state = q.popleft()
        (location, winds, current_time) = game_state
        # print("Location", location, "time", best_time)
        # pprint_winds(winds, cave_size, location)
        if current_time >= high_score:
            print("- abandoning path because reached ", current_time)
            continue
        if location == end:
            print("-- REACHED END IN {} steps (mins) in {} iterations".format(current_time, count_iterations))
            high_score = min(high_score, current_time)
            continue
        d_end = distance(location, end)
        if d_end + current_time >= high_score:
            print("- abandoning path at {} because distance to end {} + current time {} > best time {}".format(location, d_end, current_time, high_score))
            continue
        if count_iterations % 500 == 0:
            print("iteration", count_iterations)
        next_time = current_time + 1
        # for (l, w) in valid_moves(location, initial_winds, next_time, cave_size, start, end):
        #     print(" - valid next move", l)
        for next_game_state in valid_moves(location, initial_winds, next_time, cave_size, start, end):
            hashed_game = hash_game_state(next_game_state)
            if hashed_game not in game_state_times:
                q.append(next_game_state)
                game_state_times[hashed_game] = next_time
    return high_score


def problem_one():
    winds, size, start, end = read_input()
    ans = bfs(winds, size, start, end)
    print("P1 ans", ans)


problem_one()

# def problem_two():
#
#
# problem_two()
