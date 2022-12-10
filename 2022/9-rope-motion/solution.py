from enum import Enum

x_idx = 0
y_idx = 1


class Direction(Enum):
    LEFT = "L"
    RIGHT = "R"
    UP = "U"
    DOWN = "D"


def sign(x):
    if x > 0:
        return 1
    elif x == 0:
        return 0
    else:
        return -1


class Rope:
    def __init__(self):
        self.head = [0, 0]
        self.tail = [0, 0]
        self.tail_history = []

    def pprint(self):
        size = max(self.head[x_idx], self.head[y_idx], self.tail[x_idx], self.tail[y_idx], 5) + 1
        for y in reversed(range(size)):
            line = ""
            for x in range(size):
                if [x, y] == self.head:
                    line += "H "
                elif [x, y] == self.tail:
                    line += "T "
                else:
                    line += ". "
        #     print(line)
        # print()
        # print(self.tail_history)
        # print()


    def dx(self):
        return self.head[x_idx] - self.tail[x_idx]

    def dy(self):
        return self.head[y_idx] - self.tail[y_idx]

    def tail_unique_pos(self):
        return len(set(self.tail_history))

    def step_tail(self):
        if abs(self.dx()) > 1:
            self.tail[x_idx] += sign(self.dx())
            if abs(self.dy()) > 0:
                self.tail[y_idx] += sign(self.dy())
        elif abs(self.dy()) > 1:
            self.tail[y_idx] += sign(self.dy())
            if abs(self.dx()) > 0:
                self.tail[x_idx] += sign(self.dx())
        self.tail_history.append(str(self.tail[0]) + " " + str(self.tail[1]))

    def step_head(self, direction: Direction):
        if direction == Direction.LEFT:
            self.head[0] -= 1
        elif direction == Direction.RIGHT:
            self.head[0] += 1
        elif direction == Direction.UP:
            self.head[1] += 1
        elif direction == Direction.DOWN:
            self.head[1] -= 1
        self.step_tail()

    def move(self, direction: Direction, steps: int):
        for i in range(steps):
            self.step_head(direction)
            self.pprint()

def read_input():
    rope = Rope()
    for line in open("./input.txt", "r"):
        # print(line)
        tokens = line.split()
        direction: Direction = Direction(tokens[0])
        moves = int(tokens[1])
        rope.move(direction, moves)
    print("P1", rope.tail_unique_pos())



def p1():
    read_input()


p1()
