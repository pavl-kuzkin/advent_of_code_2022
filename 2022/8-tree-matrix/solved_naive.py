class Matrix:
    def __init__(self):
        self.data = read_input()
        self.size = len(self.data)

    def get(self, x: int, y: int):
        return self.data[y][x]

    def is_visible(self, x: int, y: int):
        val = self.get(x, y)
        visible = {
            "left": True,
            "right": True,
            "up": True,
            "down": True
        }
        # check left
        for xi in range(x):
            if self.get(xi, y) >= val:
                visible["left"] = False
        # check right
        for xi in range(x + 1, self.size):
            if self.get(xi, y) >= val:
                visible["right"] = False
        # check up
        for yi in range(y):
            if self.get(x, yi) >= val:
                visible["up"] = False
        # check down
        for yi in range(y + 1, self.size):
            if self.get(x, yi) >= val:
                visible["down"] = False
        return any(visible.values())

    def how_many_visible(self):
        total = 2 * self.size + 2 * self.size - 4
        print("is visible", self.is_visible(2, 2))

        for xi in range(1, self.size - 1):
            for yi in range(1, self.size - 1):
                if self.is_visible(xi, yi):
                    total += 1
        return total

    def visibility_score(self, x: int, y: int):
        score = 1
        val = self.get(x, y)
        # print("== calc ", x, y, val)
        # check left
        left_score = 0
        for xi in reversed(range(x)):
            left_score += 1
            if self.get(xi, y) >= val:
                break
        # check right
        right_score = 0
        for xi in range(x + 1, self.size):
            right_score += 1
            if self.get(xi, y) >= val:
                break
        # check up
        up_score = 0
        for yi in reversed(range(y)):
            up_score += 1
            if self.get(x, yi) >= val:
                break
        # check down
        down_score = 0
        for yi in range(y + 1, self.size):
            down_score += 1
            if self.get(x, yi) >= val:
                break
        return left_score * right_score * up_score * down_score

    def best_visibility_score(self):
        best = 0
        for yi in range(1, self.size - 1):
            for xi in range(1, self.size - 1):
                best = max(best, self.visibility_score(xi, yi))
        return best


def read_input():
    matrix = []
    for line in open("./input.txt", "r"):
        row = []
        for char in line.strip():
            row.append(int(char))
        matrix.append(row)
    return matrix


def solution():
    matrix = Matrix()
    # for x in matrix.data:
    #     print(x)
    # print("P1 answer", matrix.how_many_visible())
    print("P2 answer", matrix.best_visibility_score())


solution()
