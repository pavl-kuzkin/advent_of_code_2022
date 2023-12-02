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

# draw - {'red': '18', 'blue': '2'}
def isDrawPossible(draw):
    max_color = {
        'red': 12,
        'green': 13,
        'blue': 14
    }
    for k, v in draw.items():
        if max_color[k] < v:
            return False
    return True


# game - {'red': '18', 'blue': '2'}, {'red': '9', 'green': '5', 'blue': '4'}
def isGamePossible(game): 
    return all(map(isDrawPossible, game))


def solution():
    parsed_input = read_input()
    ans = 0

    for (idx, game) in enumerate(parsed_input):
        if isGamePossible(game):
            print(idx, "is possible", game)
            ans += (idx + 1)

    return ans

    # The Elf would first like to know which games would have been possible 
    # if the bag contained only 12 red cubes, 13 green cubes, and 14 blue cubes?

ans = solution()
print("answer is ", ans) # 2810 for me