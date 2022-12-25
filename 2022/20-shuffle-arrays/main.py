from collections import deque

INPUT_FILE = "ez-input.txt"


def read_input():
    lines = open(INPUT_FILE, "r").readlines()
    code = deque()
    for line in lines:
        code.append(int(line))
    print("input", code)
    return code


def shuffle(q: deque):
    val_order = deque()
    length = len(q)
    for (idx, val) in enumerate(q):
        # add original index to diff duplicates apart.
        val_order.append((val, idx))
    shuffled = deque(val_order)
    if len(val_order) > len(set(val_order)):
        raise Exception("duplicates where they should not be")
    for vi in val_order:
        (val, original_index) = vi
        if val == 0:
            continue
        old_idx = shuffled.index(vi)
        next_idx = (old_idx+val)
        if next_idx == 0:
            next_idx = length
        elif next_idx > length:
            next_idx = next_idx % length + 1
        elif next_idx < 0:
            next_idx = (next_idx + 5000 * length) % length - 1
        shuffled.remove(vi)
        shuffled.insert(next_idx, vi)

        print(vi[0], "moves from {} to {}".format(old_idx, next_idx))
        print(just_nums(shuffled), '\n')
    return just_nums(shuffled)

def just_nums(shuffled):
    just_nums = []
    for (val, idx) in shuffled:
        just_nums.append(val)
    return just_nums


def problem_one():
    code = read_input()
    shuffled = shuffle(code)
    zero_idx = shuffled.index(0)
    length = len(shuffled)
    print("shuffled", shuffled)
    v1000 = shuffled[(zero_idx + 1000) % length]
    v2000 = shuffled[(zero_idx + 2000) % length]
    v3000 = shuffled[(zero_idx + 3000) % length]
    print("1000th {} 2000th {} 3000 {}".format(v1000, v2000, v3000))
    print("\nP1 ans", v1000 + v2000 + v3000)


problem_one()

# problem_two()
