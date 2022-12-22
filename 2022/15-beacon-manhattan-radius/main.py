import re
from collections import defaultdict

INPUT_FILE = "input.txt"
Y_LINE = 10 if INPUT_FILE.startswith("ez-") else 2000000

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
    # for y in range(center_y - r, center_y + r + 1):
    #     # |dx| + |dy| = r, thus |dx| = r - |dy|
    #     dy = abs(y - center_y)
    #     dx = abs(r-dy)
    #     for x in range(center_x - dx, center_x + dx + 1):
    #         points.append((x, y))
    dy = abs(center_y - Y_LINE)
    for x in range(center_x-r, center_x+r+1):
        dx = abs(center_x - x)
        if dx + dy <= r:
            points.append((x, Y_LINE))
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
    print([x for x in range(xmin, xmax)])
    for y in range(ymin, ymax):
        row = [str(y+500), ": "]
        for x in range(xmin, xmax):
            row.append(signal_map[(x, y)])
        print("  ".join(row))

# i  i  i  i  B  g  g  g  g  g  g  g  g  g  d  g  g  l  j  j  j  j  j  j  j  j  j
# i  i  i  i  B  g  g  g  g  g  g  g  g  g  d  g  g  l  j  j  j  j  j  j  j  j  j  .
# #  #  #  #  B  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
# #  #  #  #  B  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #

def problemOne():

    # Note y-axis is inverted rocks start at 500,0 and fall "down" to 500,1 etc
    lines = open(INPUT_FILE, "r").readlines()
    signal_map = defaultdict(lambda: '.')
    signal_map2 = defaultdict(lambda: '.')
    xmin, xmax = 0, 0
    c = 'a'
    for line in lines:
        points = decypher_line(line.strip())
        # print(c, points, " <- ", line.strip())
        xs, ys, xb, yb = points[0], points[1], points[2], points[3]
        beacon = (xb, yb)
        sensor = (xs, ys)
        signal_map[beacon] = 'B'
        signal_map[sensor] = 'S'
        # signal_map2[beacon] = 'B'
        # signal_map2[sensor] = 'S'
        d = distance(sensor, beacon)
        coverage = circle_area(sensor, d)
        print("getting #s")
        for point in coverage:
            if signal_map[point] == '.':
                signal_map[point] = '#'
                # signal_map2[point] = c
                xmin = min(xmin, point[0])
                xmax = max(xmax, point[0])
        c = chr(ord(c)+1)

    print("alg range", xmin, xmax)
    # pprint(signal_map)
    # pprint(signal_map2)

    count_not_beacon = 0
    for x in range(xmin, xmax+10):
        if signal_map[(x, Y_LINE)] == '#':
            count_not_beacon += 1

    print("P1 ans", count_not_beacon)


problemOne()


def problemTwo():
    print("P2 ans", 0)


problemTwo()
