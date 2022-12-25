from collections import deque
from functools import cmp_to_key
import re

INPUT_FILE = "ez-input.txt"
regex = r"Valve (\w\w) has flow rate=(\d+); tunnels{0,1} leads{0,1} to valves{0,1} (.+)"
START = 'AA'
MAX_MINUTES = 30


def decypher_line(line):
    matches = re.finditer(regex, line, re.MULTILINE)
    res = []
    for m in matches:
        for g in m.groups():
            res.append(g)
    print("line (", line, ") | regex:", res)
    valve = res[0]
    flow_rate = int(res[1])
    next_valves = res[2].split(', ')
    return valve, flow_rate, next_valves


def read_input():
    lines = open(INPUT_FILE, "r").readlines()
    valve_config = {}
    for line in lines:
        valve, flow_rate, next_valves = decypher_line(line.strip())
        valve_config[valve] = (flow_rate, next_valves)
    return valve_config


# for type checking
def game_state(location: str, open_valves: set, total_flow_rate: int, minutes: int, points: int, path: str):
    return location, open_valves, total_flow_rate, minutes, points, path

def hash_state(gs):
    location, open_valves, total_flow_rate, minutes, points, path = gs
    hashes = [str(location), str(total_flow_rate), str(minutes)]
    for valve in open_valves:
        hashes.append(str(valve))
    return "-".join(hashes)
def next_nodes(gs, valve_config: dict):
    loc, open_valves, flow_rate, minutes, points, path = gs
    flow_here, next_valves = valve_config[loc]
    # print("next vals", next_valves)
    next_game_states = deque()
    next_points = points + flow_rate
    for valve in next_valves:
        next_game_states.append(game_state(valve, open_valves, flow_rate, minutes + 1, next_points, "{}->{}".format(path, valve)))
    if flow_here > 0 and loc not in open_valves:
        new_open_valves = set(open_valves)
        new_open_valves.add(loc)
        next_game_states.appendleft(game_state(loc, new_open_valves, flow_rate + flow_here, minutes + 1, next_points, "{}-open->{}".format(path, loc)))
    return next_game_states


def bfs(valve_config, start):
    q = deque()
    initial_state = game_state(start, set(), 0, 0, 0, start)
    q.append(initial_state)
    high_score = 13 * 30
    visited = set()
    visited.add(hash_state(initial_state))
    counter = 0
    while q:
        counter += 1
        gs = q.pop()
        location, open_valves, total_flow_rate, minutes, points, path = gs
        print("game state", gs)
        if counter == 200:
            return 0
        if counter % 500 == 0:
            print("iteration {} score {} minutes {}".format(counter, points, minutes))

        if minutes == MAX_MINUTES:
            if points > high_score:
                print("-- New high score {}".format(points))
            high_score = max(high_score, points)
            continue
        neighbors = next_nodes(gs, valve_config)
        for n in neighbors:
            print('-', n)
        for next in neighbors:
            next_hash = hash_state(next)
            if next_hash not in visited:
                q.append(next)
                visited.add(next_hash)
    return high_score


def sort_valve_config(vale_config: dict):
    sorted_config = {}
    for (k, v) in vale_config.items():
        flow, next_valves = v
        next_configs = sorted([(n, vale_config[n][0]) for n in next_valves], key=cmp_to_key(lambda c1, c2: c2[1] - c1[1]))
        print("next configs", next_configs)
        sorted_next_valves = [v[0] for v in next_configs]
        sorted_config[k] = (flow, sorted_next_valves)
    return sorted_config
def problem_one():
    valve_config = read_input()
    sorted_config = sort_valve_config(valve_config)
    print("valve config", valve_config)
    print("sorted config", sorted_config)
    ans = bfs(valve_config, START)
    print("P1 ans", ans)

problem_one()

# def problem_two():
#
#
# problem_two()
