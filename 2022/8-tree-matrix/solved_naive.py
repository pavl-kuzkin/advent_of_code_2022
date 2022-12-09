class Matrix:
    def __init__(self):
        self.data = read_input()
        self.size_x = len(self.data[0])
        self.size_y = len(self.data)

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
        for xi in range(x + 1, self.size_x):
            if self.get(xi, y) >= val:
                visible["right"] = False
        # check up
        for yi in range(y):
            if self.get(x, yi) >= val:
                visible["up"] = False
        # check down
        for yi in range(y + 1, self.size_y):
            if self.get(x, yi) >= val:
                visible["down"] = False
        return any(visible.values())

    def how_many_visible(self):
        total = 2 * self.size_x + 2 * self.size_y - 4
        print("is visible", self.is_visible(2, 2))

        for xi in range(1, self.size_x - 1):
            for yi in range(1, self.size_y - 1):
                if self.is_visible(xi, yi):
                    total += 1
        return total

    def visibility_score(self, x: int, y: int):
        score = 1
        val = self.get(x, y)
        print(" calc ", x, y, val)
        # check left
        for xi in range(x):
            if self.get(xi, y) >= val:
                view = abs(x - xi)
                print("left", view)
                score *= view
                break
        # check right
        for xi in range(x + 1, self.size_x):
            if self.get(xi, y) >= val:
                view = abs(x - xi)
                print("right", view)
                score *= view
                break
        # check up
        for yi in range(y):
            if self.get(x, yi) >= val:
                view = abs(y - yi)
                print("up", view)
                score *= view
                break
        # check down
        for yi in range(y + 1, self.size_y):
            if self.get(x, yi) >= val:
                view = abs(y - yi)
                print("down", view)
                score *= view
                break
        return score

    def best_visibility_score(self):
        best = 0
        for xi in range(1, self.size_x - 1):
            for yi in range(1, self.size_y - 1):
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
    print("P1 answer", matrix.how_many_visible())
    print("P2 answer", matrix.best_visibility_score())


solution()
