lose = 0
draw = 3
win = 6

round_result_code = {
    'X': lose,
    'Y': draw,
    'Z': win
}

opponent_move_code = {
    'A': 1,
    'B': 2,
    'C': 3
}

win_move_code = {
    1: 2,
    2: 3,
    3: 1
}

lose_move_code = {
    1: 3,
    2: 1,
    3: 2
}

def decrypt(line):
    chars = line.split()
    return opponent_move_code[chars[0]], round_result_code[chars[1]]


def calc_round(__opponent_move__, __round__):
    if __round__ == win:
        return win + win_move_code[__opponent_move__]
    elif __round__ == draw:
        return draw + __opponent_move__
    else:
        return lose + lose_move_code[__opponent_move__]


f = open("./input.txt", "r")
total = 0
for x in f:
    opponent, round = decrypt(x)
    if round == win:
        print("round", x.strip(), ", decrypt", opponent, round, ", result", calc_round(opponent, round))
    total = total + calc_round(opponent, round)
print("total", total)
