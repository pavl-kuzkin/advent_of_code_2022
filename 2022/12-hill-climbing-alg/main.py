from collections import deque


class Node:
    def __init__(self, x: int, y: int, height: str):
        self.x = x
        self.y = y
        self.h = ord(height)
        self.c = height

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return "{0} ({1}, {2})".format(chr(self.h), self.x, self.y)

    def neighbors(self, graph):
        left = self.neighbor(self.x - 1, self.y, graph)
        right = self.neighbor(self.x + 1, self.y, graph)
        top = self.neighbor(self.x, self.y + 1, graph)
        bot = self.neighbor(self.x, self.y - 1, graph)
        return [left, right, top, bot]

    def neighbor(self, x: int, y: int, graph):
        y_max = len(graph) - 1
        x_max = len(graph[0]) - 1
        if x < 0 or y < 0 or x > x_max or y > y_max:
            return None
        # print("self", self, "neighbor", x, y, "size", x_max, y_max)
        neighbor_h = graph[y][x]
        if neighbor_h == "E":
            neighbor_h = 'z'
        if neighbor_h == "S":
            neighbor_h = 'a'
        if ord(neighbor_h) - self.h < 2:
            return Node(x, y, neighbor_h)
        return None


def pprint(graph):
    for line in graph:
        if type(line) == list and type(line[0]) == str:
            print("".join(line))
        else:
            print(line)


def find_ends(lines):
    start = None
    end = None
    for y in range(len(lines)):
        line = lines[y].strip()
        for x in range(len(line)):
            char = line[x]
            if char == 'E':
                end = Node(x, y, 'z')
            elif char == 'S':
                start = Node(x, y, 'a')
    return start, end


def bfs(start: Node, end: Node, graph):
    queue = [start]
    graph_x_size = len(graph[0])
    graph_y_size = len(graph)
    # int for infinity
    inf = 10000
    print("bfs start", start, "end", end, "graph:")
    pprint(graph)
    distances = []
    visited = copy(graph)
    for y in range(graph_y_size):
        # set all distances to unachievable number
        row = [inf] * graph_x_size
        distances.append(row)
    # set start to 0
    distances[start.y][start.x] = 0
    distances[end.y][end.x] = 100001
    # pprint(distances)
    visited_nodes = deque()
    next_nodes = deque()
    next_nodes.append((start, 0))


    while len(next_nodes) > 0:
        node, dist = next_nodes.popleft()
        print("pop", node, dist)
        if node == end:
            print("found end", end, dist)
            return dist
        if str(node) in visited_nodes:
            print("skipping because visited", node)
            continue

        visited_nodes.append(str(node))
        visited[node.y][node.x] = node.c.capitalize()

        neighbors = node.neighbors(graph)
        for neighbor in neighbors:
            if neighbor is not None:
                next_nodes.append((neighbor, dist + 1))
                print("|-neighbor", neighbor, "new dist", dist+1)



        # pprint(visited)
        visited[node.y][node.x] = "."

    # pprint(visited)
    return distances[end.y][end.x]


def copy(nested_list):
    copy = []
    for y in nested_list:
        y_copy = []
        for x in y:
            y_copy.append(x)
        copy.append(y_copy)
    return copy


def p1():
    lines = open("input.txt", "r").readlines()
    graph = []
    for line in lines:
        graph.append(line.strip())
    start, end = find_ends(graph)
    # pprint(graph)
    ans = bfs(start, end, graph)
    print("P1 ans", ans)


p1()
