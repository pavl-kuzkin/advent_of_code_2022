from enum import Enum
from typing import Optional


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


class RopeNode:
    def __init__(self, rope_len: int):
        self.x = 0
        self.y = 0
        self.tail: Optional[RopeNode] = None
        if rope_len > 1:
            self.tail = RopeNode(rope_len - 1)

    def move(self, direction: Direction, steps: int, tail_history: list):
        for i in range(steps):
            self.step(direction, tail_history)
            # pprint(self)

    def step(self, direction: Direction, tail_history: list):
        if direction == Direction.LEFT:
            self.x -= 1
        elif direction == Direction.RIGHT:
            self.x += 1
        elif direction == Direction.UP:
            self.y += 1
        elif direction == Direction.DOWN:
            self.y -= 1
        if self.tail is not None:
            self.tail.follow(self, tail_history)

    def follow(self, head: "RopeNode", tail_history: list):
        dx = head.x - self.x
        dy = head.y - self.y
        if abs(dx) > 1:
            self.x += sign(dx)
            if abs(dy) > 0:
                self.y += sign(dy)
        elif abs(dy) > 1:
            self.y += sign(dy)
            if abs(dx) > 0:
                self.x += sign(dx)

        if self.tail is not None:
            self.tail.follow(self, tail_history)
        else:
            tail_history.append(str(self.x) + " " + str(self.y))


def pprint(node: RopeNode):
    size = 21
    buckets = [["." for _col in range(size)] for _row in range(size)]
    while node.tail is not None:
        buckets[node.y][node.x] = "X"
        node = node.tail
    for row in reversed(buckets):
        print(" ".join(row))
    print()


def solve(rope_len: int, input_file: str):
    rope_head = RopeNode(rope_len)
    tail_history = []

    for line in open(input_file, "r"):
        # print(line)
        tokens = line.split()
        direction: Direction = Direction(tokens[0])
        moves = int(tokens[1])
        rope_head.move(direction, moves, tail_history)
    # print("moves done, calculating tail positions")
    print(input_file, rope_len, len(set(tail_history)))


def p2():
    solve(10, "p2_input.txt")


def p1():
    solve(2, "p1_input.txt")


p1()
p2()
