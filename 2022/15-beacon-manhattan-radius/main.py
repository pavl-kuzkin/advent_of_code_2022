import re
from collections import defaultdict

INPUT_FILE = "ez-input.txt"

regex = r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)"


def decypher_line(line):
    matches = re.finditer(regex, line, re.MULTILINE)
    res = []
    for m in matches:
        for g in m.groups():
            res.append(int(g))
    return res


def pprint_2d(two_d_list, title=""):
    print(title)
    for line in two_d_list:
        if type(line) == list and type(line[0]) == str:
            print("".join(line))
        else:
            print(line)


def distance(a, b):
    xa, ya = a
    xb, yb = b
    return abs(xb - xa) + abs(yb - ya)


def circle_area(center, r):
    center_x, center_y = center
    points = []
    for y in range(center_y - r, center_y + r + 1):
        # |dx| + |dy| = r, thus |dx| = r - |dy|
        dy = abs(y - center_y)
        dx = abs(r-dy)
        for x in range(center_x - dx, center_x + dx + 1):
            points.append((x, y))
    return points


def pprint(signal_map):
    # print(signal_map)
    xmin, xmax, ymin, ymax = 0, 0, 0, 0
    for (x, y) in signal_map.keys():
        xmin = min(xmin, x)
        xmax = max(xmax, x)
        ymin = min(ymin, y)
        ymax = max(ymax, y)
    print("dx", xmin, xmax, "dy", ymin, ymax)

    for y in range(ymin, ymax):
        row = [str(y+500), ": "]
        for x in range(xmin, xmax):
            row.append(signal_map[(x, y)])
        print(" ".join(row))



def problemOne():

    # Note y-axis is inverted rocks start at 500,0 and fall "down" to 500,1 etc
    lines = open(INPUT_FILE, "r").readlines()
    signal_map = defaultdict(lambda: '.')
    xmin, xmax = 0, 0
    for line in lines:
        points = decypher_line(line.strip())
        print(points, " <- ", line.strip())
        xs, ys, xb, yb = points[0], points[1], points[2], points[3]
        beacon = (xb, yb)
        sensor = (xs, ys)
        signal_map[beacon] = 'B'
        signal_map[sensor] = 'S'
        print("getting dist")
        d = distance(sensor, beacon)
        print("getting coverage")
        coverage = circle_area(sensor, d)
        print("getting #s")
        for point in coverage:
            if signal_map[point] == '.':
                signal_map[point] = '#'
                xmin = min(xmin, point[0])
                xmax = max(xmax, point[0])

    print("alg range", xmin, xmax)
    pprint(signal_map)

    # for (x, y) in signal_map.keys():
    #     xmin = min(xmin, x)
    #     xmax = max(xmax, x)

    count_not_beacon = 0
    ez_y = 10
    p1_y = 2000000
    for x in range(xmin, xmax):
        if signal_map[(x, ez_y)] == '#':
            count_not_beacon += 1

    print("P1 ans", count_not_beacon)


problemOne()


def problemTwo():
    print("P2 ans", 0)


problemTwo()
