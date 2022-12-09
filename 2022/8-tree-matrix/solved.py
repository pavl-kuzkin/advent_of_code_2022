from enum import Enum
from typing import Optional


class Direction(Enum):
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"


class Node:
    def __init__(self, height: int):
        self.neighbors = None
        self.visibility = {
            Direction.LEFT: None,
            Direction.RIGHT: None,
            Direction.DOWN: None,
            Direction.UP: None,
        }
        self.height: int = height

    def __str__(self):
        return f"{self.height}"

    def connect_to_neighbors(self, matrix: list[list()], x: int, y: int):
        self.neighbors = {
            Direction.LEFT: matrix[y][x - 1] if x > 0 else None,
            Direction.RIGHT: matrix[y][x + 1] if x < (len(matrix[0]) - 1) else None,
            Direction.DOWN: matrix[y - 1][x] if y > 0 else None,
            Direction.UP: matrix[y + 1][x] if y < len(matrix) - 1 else None,
        }

    def is_edge(self):
        return not any(self.neighbors.values())

    # Lazy load visibility and remember result
    def is_1d_visible(self, direction: Direction):
        if self.visibility[direction] is None:
            self.visibility[direction] = self.__is_1d_visible__(direction)
        return self.visibility[direction]

    def __is_1d_visible__(self, direction: Direction):
        neighbor = self.neighbors[direction]
        if neighbor is None:
            # if there is no neighbor this node is visible
            return True
        elif neighbor.height >= self.height:
            # if there is a taller neighbor this node is hidden
            return False
        else:
            # there is a neighbor and its shorter
            return neighbor.is_1d_visible(direction)

    def is_visible(self):
        return any([self.is_1d_visible(Direction.LEFT),
                    self.is_1d_visible(Direction.RIGHT),
                    self.is_1d_visible(Direction.DOWN),
                    self.is_1d_visible(Direction.UP)
                    ])


class Matrix:
    def __init__(self):
        data = read_input()
        self.nodes: list[list(Node)] = []
        for col in data:
            node_column = []
            self.nodes.append(node_column)
            for item in col:
                node_column.append(Node(item))

        for y in range(len(self.nodes)):
            for x in range(len(self.nodes)):
                node: Node = self.nodes[y][x]
                node.connect_to_neighbors(self.nodes, x, y)

    def __str__(self):
        stringified_rows = []
        for row in self.nodes:
            stringified_rows.append("".join(map(lambda x: str(x), row)))
        return "\n".join(stringified_rows)

    def count_visible(self):
        total = 0
        for y in range(len(self.nodes)):
            for x in range(len(self.nodes[0])):
                node: Node = self.nodes[y][x]
                if node.is_visible():

        return total


def read_input():
    matrix = []
    for line in open("./input.txt", "r"):
        row = []
        for char in line.strip():
            row.append(int(char))
        matrix.append(row)
    return matrix


def solution_part1():
    matrix = Matrix()
    # print(matrix)


# 1672
solution_part1()
