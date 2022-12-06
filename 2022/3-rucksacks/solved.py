def item_priority(char):
    if char.islower():
        return ord(char) - ord('a') + 1;
    else:
        return ord(char) - ord('A') + 27;


def solution_part1():
    f = open("./input.txt", "r")
    total = 0
    for x in f:
        line = x.strip()
        first_half = line[:len(line) // 2]
        second_half = line[len(line) // 2:]
        item_in_both = (set(first_half) & set(second_half)).pop()
        total += item_priority(item_in_both)
    print('part 1 answer', total)


solution_part1()
