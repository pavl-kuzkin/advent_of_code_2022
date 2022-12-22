INPUT_FILE = "input.txt"

START = (500, 0)
X_MAX = 800
Y_MAX = 175
ROCK = '#'
SAND = 'O'
EMPTY = '.'



def pprint_2d(two_d_list, title=""):
    print(title)
    for line in two_d_list:
        if type(line) == list and type(line[0]) == str:
            print("".join(line))
        else:
            print(line)


def get_range(point1: tuple, point2: tuple):
    min_x, max_x = min(point1[0], point2[0]), max(point1[0], point2[0]) + 1
    min_y, max_y = min(point1[1], point2[1]), max(point1[1], point2[1]) + 1
    # print("range for", point1, point2)
    q = [(x, y) for x in range(min_x, max_x) for y in range(min_y, max_y)]
    return q


def point(pointStr: str):
    xy = pointStr.split(',')
    return int(xy[0]), int(xy[1])

def sand_fall(sand_map, rock_range, floor):
    rx_min, rx_max, ry_min, ry_max = rock_range
    print("Rock range", rx_min, rx_max, ry_min, ry_max)
    # pprint_2d(sand_map)
    sand_count = 0
    while True:
        # print("count", sand_count)
        x, y = START
        falling = True
        if sand_map[y][x] == SAND:
            # P2 ans here
            # pprint_2d(sand_map, "map")
            return sand_count
        while falling:
            if y+1 == floor:
                sand_map[y][x] = SAND
                falling = False
            elif y > ry_max:
                # P1 answer here
                return sand_count
            elif sand_map[y+1][x] == EMPTY:
                y += 1
            elif sand_map[y+1][x-1] == EMPTY:
                y += 1
                x -= 1
            elif sand_map[y+1][x+1] == EMPTY:
                y += 1
                x += 1
            else:
                sand_map[y][x] = SAND
                falling = False
        sand_count += 1
        # pprint_2d(sand_map, "map")
    return sand_count


def problemOne():
    # Note y-axis is inverted rocks start at 500,0 and fall "down" to 500,1 etc
    lines = open(INPUT_FILE, "r").readlines()
    sand_map = [['.'] * X_MAX for i in range(Y_MAX)]
    # rock 2D range. once out of range game over
    rx_min, rx_max, ry_min, ry_max = X_MAX, 0, 0, 0

    for line in lines:
        coordinates = line.strip().split(" -> ")
        for i in range(len(coordinates) - 1):
            p1 = point(coordinates[i])
            p2 = point(coordinates[i + 1])
            ry_max = max(ry_max, p1[1], p2[1])
            rx_max = max(rx_max, p1[0], p2[0])
            rx_min = min(rx_min, p1[0], p2[0])
            for (x,y) in get_range(p1, p2):
                sand_map[y][x] = ROCK
    ans = sand_fall(sand_map, (rx_min, rx_max, ry_min, ry_max), ry_max+100)
    print("P1 ans", ans)


problemOne()

def problemTwo():
    # Note y-axis is inverted rocks start at 500,0 and fall "down" to 500,1 etc
    lines = open(INPUT_FILE, "r").readlines()
    sand_map = [['.'] * X_MAX for i in range(Y_MAX)]
    # rock 2D range. once out of range game over
    rx_min, rx_max, ry_min, ry_max = X_MAX, 0, 0, 0

    for line in lines:
        coordinates = line.strip().split(" -> ")
        for i in range(len(coordinates) - 1):
            p1 = point(coordinates[i])
            p2 = point(coordinates[i + 1])
            ry_max = max(ry_max, p1[1], p2[1])
            rx_max = max(rx_max, p1[0], p2[0])
            rx_min = min(rx_min, p1[0], p2[0])
            for (x,y) in get_range(p1, p2):
                sand_map[y][x] = ROCK
    ans = sand_fall(sand_map, (rx_min, rx_max, ry_min, ry_max), ry_max+2)
    print("P2 ans", ans)


problemTwo()
