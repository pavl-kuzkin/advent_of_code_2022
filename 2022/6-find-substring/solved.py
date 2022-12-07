def solution_part1():
    f = open("./input.txt", "r")
    for line in f:
        last_four = []
        print(line)
        for idx, char in enumerate(line):
            if len(last_four) == 4:
                del last_four[0]
            last_four.append(char)
            size = len(set(last_four))
            # print(idx+1, size, last_four)
            if size == 4:
                print('part 1 answer', idx+1)
                return




solution_part1()
# solution_part2()
