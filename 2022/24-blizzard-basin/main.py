from collections import deque

INPUT_FILE = "ez-input.txt"
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


# manhattan distance between two points a and b
def distance(a, b):
    xa, ya = a
    xb, yb = b
    return abs(xb - xa) + abs(yb - ya)


def hash_game_state(game_state):
    location, winds, score = game_state
    hashes = [str(location)]
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


# helper function for pprint
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


# pretty print game board for debugging
def pprint_winds(winds: list, size: tuple, my_pos: tuple):
    sep = ' '
    x_max, y_max = size
    for y in reversed(range(-1, y_max + 1)):
        print("{:02d}".format(y), end=' ')
        for x in range(-1, x_max + 1):
            loc = (x, y)
            if loc == my_pos:
                print('E', end=sep)
            else:
                print(find_wind((x, y), winds), end=sep)
        print()
    print(' ', end=sep)
    for x in range(-1, x_max + 1):
        if 0 <= x < 10:
            print(' ', end='')
            print(x, end='')
        else:
            print("{:02d}".format(x), end='')

    print()


# get location of a particular wind at given time
def wind_loc(init_point: tuple, direction: str, minutes: int, cave_size: tuple):
    # print(init_point)
    if init_point == 5:
        print("oops")
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


# get locations of all winds at a given time
def winds_locs(init_winds: list, minutes: int, cave_size: tuple):
    current_winds = []
    for (loc, dir) in init_winds:
        current_loc = wind_loc(loc, dir, minutes, cave_size)
        current_winds.append((current_loc, dir))
    return current_winds


# check if location has wind to calculate valid moves
def has_wind(location, winds):
    for (wind_loc, dir) in winds:
        if wind_loc == location:
            return True
    return False


# get all valid moves from location given location of winds
# current location of winds calculated as F(winds, time) = new_winds
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
        if not has_wind(new_loc, new_winds):
            game_state = (new_loc, new_winds, minutes)
            valid.append(game_state)
    return valid


# BFS on a cyclical bidriectional graph
# The nodes of the graph are the state of the board (your location and location and direction of each wind)
# The edges are all possible valid moves (1 move per 1 minute)
# Do a BFS and count best time aka move count
# Need to hash the game state to check that we've visited nodes before.
def bfs(initial_winds: list, cave_size: tuple, start, end):
    print("\n== BFS {} -> {} == \n".format(start, end))
    q = deque()
    # graph node is your location + wind location
    # graph edges are possible moves
    initial_game_state = (start, initial_winds, 0)
    q.append(initial_game_state)
    game_state_times = {hash_game_state(initial_game_state): 0}
    high_score = 600
    best_game_state = None
    count_iterations = 0
    while q:
        count_iterations += 1
        game_state = q.popleft()
        (location, winds, current_time) = game_state
        # print("Location", location, "time", best_time)
        # pprint_winds(winds, cave_size, location)
        if current_time >= high_score:
            # print("- abandoning path because reached ", current_time)
            continue
        if location == end:
            print("\n-- High Score: {} -> {} IN {} steps (mins) in {} iterations\n".format(start, end, current_time,
                                                                                           count_iterations))
            if current_time < high_score:
                best_game_state = game_state
            high_score = min(high_score, current_time)
            continue
        d_end = distance(location, end)
        if d_end + current_time >= high_score:
            print("- abandoning path at {} because distance to end {} + current time {} > best time {}".format(location,
                                                                                                               d_end,
                                                                                                               current_time,
                                                                                                               high_score))
            continue
        if count_iterations % 500 == 0:
            print("\rProcessing: {}".format(count_iterations), end="")
        next_time = current_time + 1
        # for (l, w) in valid_moves(location, initial_winds, next_time, cave_size, start, end):
        #     print(" - valid next move", l)
        for next_game_state in valid_moves(location, initial_winds, next_time, cave_size, start, end):
            hashed_game = hash_game_state(next_game_state)
            if hashed_game not in game_state_times:
                q.append(next_game_state)
                game_state_times[hashed_game] = next_time
    return high_score, best_game_state


def problem_one():
    winds, size, start, end = read_input()
    time, best_game_state = bfs(winds, size, start, end)
    print("P1 ans", time)


problem_one()


def problem_two():
    winds, size, start, end = read_input()
    # go to goal
    time, (loc0, game_state0, time0) = bfs(winds, size, start, end)
    # go back to start
    time1, (loc1, game_state1, time1) = bfs(game_state0, size, end, start)
    # go back to goal again
    time2, best_game_state2 = bfs(game_state1, size, start, end)
    print("P2 ans to goal {} back {} and goal {} for a total of {}".format(time, time1, time2, time + time1 + time2))


problem_two()
