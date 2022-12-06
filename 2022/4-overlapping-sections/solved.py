def parse_range(range):
    bounds = range.split('-')
    return int(bounds[0]), int(bounds[1])

def parse_line(line):
    ranges = line.split(",")
    first = parse_range(ranges[0])
    second = parse_range(ranges[1])
    return first, second


def is_subrange(min1, max1, min2, max2):
    if min1 <= min2 and max1 >= max2:
        return True
    elif min2 <= min1 and max2 >= max1:
        return True
    else:
        return False

def solution_part1():
    f = open("./input.txt", "r")
    total = 0
    for x in f:
        first_range, second_range = parse_line(x.strip())
        min1, max1 = first_range
        min2, max2 = second_range
        subrage = is_subrange(min1, max1, min2, max2)
        # print(first_range, second_range, subrage)
        if subrage:
            total += 1
    print('part 1 answer', total)

solution_part1()