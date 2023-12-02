INPUT_FILE = "input.txt"

def read_input():
    parsed = []
    for line in open(INPUT_FILE, "r").readlines():
        parsed.append(parse_line(line.strip()))
    return parsed

def parse_line(line: str):
    colon_split = line.split(':')
    game_count = colon_split[0].split()[1]
    draws = colon_split[1].split(';')
    color_maps = []
    for draw in draws:
        colors = draw.strip().split(', ')
        color_map = {}
        for color in colors:
            (count, color) = color.split()
            print(game_count, count, color)
            color_map[color] = int(count)
        color_maps.append(color_map)
        print()
    return color_maps


# game - [{'red': '18', 'blue': '2'}, {'red': '9', 'green': '5', 'blue': '4'}]
def minSet(game: list):
    minSet = {
        'red': 0,
        'green': 0,
        'blue': 0
    }
    for draw in game:
        for k, v in draw. items():
            minSet[k] = max(minSet[k], v)
    return minSet

def setPower(minSet: dict):
    res = 1
    for val in minSet.values():
        res = res * val
    return res
    

# For each game, find the minimum set of cubes that must have been present. 
# What is the sum of the power of these sets?
def solution():
    parsed_input = read_input()
    return sum(map(setPower(minSet), parsed_input))


ans = solution()
print("answer is ", ans) # 69110 for me