# 0123456789
#     [D]
# [N] [C]
# [Z] [M] [P]
#  1   2   3
#
# move 1 from 2 to 1
# move 3 from 1 to 3
# move 2 from 2 to 1
# move 1 from 1 to 2

# letters come in fixed indexes 1, 5, 9, etc

def parse_line(line, crates):
    idx = 1
    while idx < len(line):
        letter = line[idx]
        if letter != ' ':
            # print(idx, letter, idx // 4 + 1)
            stack_id = idx // 4 + 1
            crates[stack_id].append(letter)
        idx += 4


def solution_part1():
    crates = []
    for x in range(0, 10):
        crates.append([])
    f = open("./input.txt", "r")
    for x in f:
        if x.startswith(" 1   2   3"):
            # all stacks have been read in reverse order so reverse will get us the real order
            for stack in crates:
                stack.reverse()
        elif x.startswith("move"):
            moves = [int(s) for s in x.split() if s.isdigit()]
            # print(moves)
            item_count = moves[0]
            from_idx = moves[1]
            to_idx = moves[2]
            for idx in range(item_count):
                from_stack = crates[from_idx]
                to_stack = crates[to_idx]
                # print("from", from_stack, "to", to_stack)
                to_stack.append(from_stack.pop())
            # print(crates)
        else:
            # reading setup stacks from top to bottom
            parse_line(x, crates)

    answer = []
    for stack in crates:
        if len(stack) > 0:
            answer.append(stack.pop())
    print('part 1 answer', ''.join(answer))


def solution_part2():
    crates = []
    for x in range(0, 10):
        crates.append([])
    f = open("./input.txt", "r")
    for x in f:
        if x.startswith(" 1   2   3"):
            # all stacks have been read in reverse order so reverse will get us the real order
            for stack in crates:
                stack.reverse()
        elif x.startswith("move"):
            moves = [int(s) for s in x.split() if s.isdigit()]
            # print(moves)
            item_count = moves[0]
            from_idx = moves[1]
            to_idx = moves[2]
            from_stack = crates[from_idx]
            to_stack = crates[to_idx]
            to_stack.extend(from_stack[-1*item_count:])
            del from_stack[-1*item_count:]
        else:
            # reading setup stacks from top to bottom
            parse_line(x, crates)

    answer = []
    for stack in crates:
        if len(stack) > 0:
            answer.append(stack.pop())
    print('part 2 answer', ''.join(answer))

# solution_part1()
solution_part2()
