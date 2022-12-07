def solution(remember_length):
    f = open("./input.txt", "r")
    for line in f:
        last_four = []
        print(line)
        for idx, char in enumerate(line):
            if len(last_four) == remember_length:
                del last_four[0]
            last_four.append(char)
            size = len(set(last_four))
            # print(idx+1, size, last_four)
            if size == remember_length:
                print('part 1 answer', idx+1)
                return



# part 1
solution(4)
# part 2
solution(14)
