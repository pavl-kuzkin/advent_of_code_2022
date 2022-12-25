from collections import deque

INPUT_FILE = "input.txt"
FROM_SNAFU = {
    '=': -2,
    '-': -1,
    '0': 0,
    '1': 1,
    '2': 2
}
TO_SNAFU = {
    -2: '=',
    -1: '-',
    0: '0',
    1: '1',
    2: '2'
}


def read_input():
    lines = open(INPUT_FILE, "r").readlines()
    total = 0
    for line in lines:
        code = line.strip()
        val = to_decimal(code)
        print("{} -> {} -> {}".format(code, val, to_snafu(val)))
        total += val
    print("total", total)
    return total


def to_decimal(snafu: str):
    length = len(snafu)
    result = 0
    for i in range(length):
        char = snafu[length - i - 1]
        digit = FROM_SNAFU[char]
        result += digit * pow(5, i)
    return result


def to_snafu(decimal_number: int, base=5):
    n = decimal_number
    m = deque()
    while n > 0:
        shift = n + 2
        r = shift % base
        n = shift // base
        # snafu goes from -2 to 2 instead of 0 to 4
        m.appendleft(TO_SNAFU[r - 2])
    return ''.join(m)


def problem_one():
    total = read_input()
    print("\nP1 ans", to_snafu(total))


problem_one()

# problem_two()
