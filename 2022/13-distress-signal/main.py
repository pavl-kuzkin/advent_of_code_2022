import json
from functools import cmp_to_key

INPUT_FILE = "input.txt"


def compare(left, right, depth=0):
    # print("-" * depth, "Compare", left, right)
    depth += 1
    if type(left) == int and type(right) == int:
        return right - left
    elif type(left) == list and type(right) == list:
        for i in range(min(len(left), len(right))):
            child_correct = compare(left[i], right[i], depth)
            if child_correct != 0:
                return child_correct
        return len(right) - len(left)
    elif type(left) == list:
        return compare(left, [right], depth)
    elif type(right) == list:
        return compare([left], right, depth)
    raise Exception("Unexpected inputs left type {0} right type {1}".format(type(left), type(right)))


def p1():
    lines = open(INPUT_FILE, "r").readlines()
    correct_list = []
    pair_idx = 0
    for x in range(0, len(lines), 3):
        pair_idx += 1
        # print("== Pair {0} ==".format(pair_idx))
        left = json.loads(lines[x].strip())
        right = json.loads(lines[x + 1].strip())
        correct = compare(left, right)
        # print("Correct", correct > 0, "\n")
        if correct > 0:
            correct_list.append(pair_idx)
    print("P1 ans", sum(correct_list))

def p2():
    lines = open(INPUT_FILE, "r").readlines()
    signals = [[[2]], [[6]]]
    for x in range(0, len(lines), 3):
        left = json.loads(lines[x].strip())
        right = json.loads(lines[x + 1].strip())
        signals.append(left)
        signals.append(right)
    index_prod = 1
    for idx, sig in enumerate(reversed(sorted(signals, key=cmp_to_key(compare)))):
        print(sig)
        if sig == [[2]] or sig == [[6]]:
            index_prod *= idx + 1
    print("P2 ans", index_prod)


p1()
p2()
