# 1 point = A or X = Rock
rock = ['A', 'X']
# 2 point = B or Y = Paper
paper = ['B', 'Y']
# 3 point = C or Z = Scissors
scissors = ['C', 'Z']


def decrypt_char(char):
    if char in rock:
        return 1
    elif char in paper:
        return 2
    else:
        return 3


def decrypt(line):
    chars = line.split()
    return decrypt_char(chars[0]), decrypt_char(chars[1])


# 2>1, 3>2, 1>3, wins 2-1=1, 1-3=-2, 3-2=1  loses: 2-3=-1, 1-2=-1, 3-1=2
lose = 0
draw = 3
win = 6


def calc_round(opponent, player):
    if opponent == player:
        return draw + player
    if (player - opponent) % 3 == 1:
        return win + player
    else:
        return lose + player


f = open("./input.txt", "r")
total = 0
for x in f:
    opponent, player = decrypt(x)
    total += calc_round(opponent, player)
print(total)
