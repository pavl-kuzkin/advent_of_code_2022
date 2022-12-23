import re
from collections import defaultdict
from functools import cmp_to_key

INPUT_FILE = "input.txt"
Y_LINE = 10 if INPUT_FILE.startswith("ez-") else 2000000
MIN = 0
MAX = 20 if INPUT_FILE.startswith("ez") else 4000000

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
    for x in range(center_x - r, center_x + r + 1):
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
        row = [str(y + 500), ": "]
        for x in range(xmin, xmax):
            row.append(signal_map[(x, y)])
        print("  ".join(row))


def read_input():
    lines = open(INPUT_FILE, "r").readlines()
    exclusion_zones = []
    for line in lines:
        points = decypher_line(line.strip())
        print(points, " <- ", line.strip())
        xs, ys, xb, yb = points[0], points[1], points[2], points[3]
        beacon = (xb, yb)
        sensor = (xs, ys)
        d = distance(sensor, beacon)
        exclusion_zones.append((sensor, beacon, d))
    return exclusion_zones


def problemOne():
    signal_map = defaultdict(lambda: '.')
    xmin, xmax = 0, 0

    exclusion_zones = read_input()
    for (sensor, beacon, radius) in exclusion_zones:
        signal_map[sensor] = 'S'
        signal_map[beacon] = 'B'
        print("calculating zone", sensor, radius)
        coverage = circle_area(sensor, radius)
        # print("getting #s")
        for point in coverage:
            if signal_map[point] == '.':
                signal_map[point] = '#'
                # signal_map2[point] = c
                xmin = min(xmin, point[0])
                xmax = max(xmax, point[0])

    print("alg range", xmin, xmax)
    # pprint(signal_map)
    # pprint(signal_map2)

    count_not_beacon = 0
    for x in range(xmin, xmax + 10):
        if signal_map[(x, Y_LINE)] == '#':
            count_not_beacon += 1

    print("P1 ans should be 5688618", count_not_beacon)


# problemOne()

def in_any_zone(x, y, exclusion_zones):
    for (sensor, beacon, radius) in exclusion_zones:
        d = distance((x, y), sensor)
        if d <= radius:
            return True
    return False


def can_combine(r1, r2):
    x1, y1 = r1
    x2, y2 = r2
    return x2 <= y1 <= y2 or x1 <= y2 <= y1 or (y1 < y2 and y1 + 1 == x2) or (y2 < y1 and y2 + 1 == x1)


def combine_range(r1, r2):
    x1, y1 = r1
    x2, y2 = r2
    return min(x1, x2), max(y1, y2)


def combine_range_recr(range_list):
    for i in range(len(range_list) - 1):
        r1 = range_list[i]
        r2 = range_list[i + 1]
        if can_combine(r1, r2):
            range_list[i + 1] = combine_range(r1, r2)
            range_list[i] = None

    return list(filter(lambda x: x is not None, range_list))


def sort_ranges(range_list):
    return list(reversed(sorted(range_list, key=cmp_to_key(lambda r1, r2: r2[0] - r1[0]))))


def find_x(exclusion_zones):
    for x in range(MIN, MAX):
        # figure out y-ranges for each zone
        print("x", x)
        ranges = [(0, 1)]
        for (sensor, beacon, radius) in exclusion_zones:
            cx, cy = sensor
            dx = abs(cx - x)
            if dx > radius:
                continue
            dy = radius - dx
            range_min, range_max = cy - dy, cy + dy
            new_range = (range_min, range_max)
            combined = False
            for (i, prev_r) in enumerate(ranges):
                if can_combine(prev_r, new_range):
                    combined = True
                    ranges[i] = combine_range(prev_r, new_range)
                    break
            if not combined:
                ranges.append(new_range)
                ranges = sort_ranges(ranges)

            # print("-zone", sensor, radius, "range", range_min, range_max)
            # print("ranges", ranges)
        # combine ranges into one
        ranges = combine_range_recr(ranges)
        if len(ranges) > 1:
            print("FOUND X", x)
            return x
        print("final ranges", ranges)


def find_y(exclusion_zones):
    for y in range(MIN, MAX):
        # figure out y-ranges for each zone
        print("y", y)
        ranges = [(0, 1)]
        for (sensor, beacon, radius) in exclusion_zones:
            cx, cy = sensor
            dy = abs(cy - y)
            if dy > radius:
                continue
            dx = radius - dy
            range_min, range_max = cx - dx, cx + dx
            new_range = (range_min, range_max)
            combined = False
            for (i, prev_r) in enumerate(ranges):
                if can_combine(prev_r, new_range):
                    combined = True
                    ranges[i] = combine_range(prev_r, new_range)
                    break
            if not combined:
                ranges.append(new_range)
                ranges = sort_ranges(ranges)

            # print("-zone", sensor, radius, "range", range_min, range_max)
            # print("ranges", ranges)
        # combine ranges into one
        ranges = combine_range_recr(ranges)
        if len(ranges) > 1:
            print("FOUND Y", y)
            return y
        print("final ranges", ranges)


def problemTwo():
    exclusion_zones = read_input()
    x = find_x(exclusion_zones)
    y = find_y(exclusion_zones)

    print("P2 (ans = 12625383204261)", x * 4000000 + y)

problemTwo()
