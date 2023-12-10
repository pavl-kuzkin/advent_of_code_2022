import sys, os

INPUT_FILE = "input.txt"

def read_input():
    path = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), INPUT_FILE)
    parsed = []
    for line in open(path, "r").readlines():
        parsed.append(parse_line(line.strip()))
    return parsed

# Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
def parse_line(line: str):
    nums = line.split(': ')[1]
    [winning_nums, got_nums] = nums.split(' | ')

    return winning_nums.strip().split(' '), got_nums.strip().split(' ')

def solve():
    input = read_input()
    ans = 0
    for (winning_nums, got_nums) in input:
        # print(winning_nums, got_nums)
        ans += (count(winning_nums, got_nums))
    print("ans", ans)
        
def count(winning_nums: list, got_nums: list):
    count = {}
    for num in winning_nums:
        count[num] = 0
    for num in got_nums:
        if num in count:
            count[num] = 1
    # print(count)
    matches = sum(count.values())
    if matches == 0:
        return 0
    else:
        return pow(2, matches - 1)


solve()