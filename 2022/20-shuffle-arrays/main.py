from collections import deque

INPUT_FILE = "ez-input.txt"


class Node:
    def __init__(self, v: int):
        self.val = v
        self.nxt = None
        self.prev = None

    def set_nxt(self, n: 'Node'):
        self.nxt = n
        n.prev = self

    def __str__(self):
        return "{}->{}".format(self.val, self.nxt if self.nxt is None else self.nxt.val)


    def mix(self):
        steps = self.val
        if steps > 0:
            for i in range(steps):
                self.switch_forward()

    def switch_forward(self):
        # before
        # n1 - n2 - n3 - n4
        # after n2 goes step right
        # n1 - n3 - n2 - n4
        n1 = self.prev
        n2 = self
        n3 = self.nxt
        n4 = n3.next
        n2.set_nxt(n4)
        n3.set_nxt(n2)
        n1.set_nxt(n3)






    def pprint(self):
        s = ["{} ->".format(self.val)]
        sib = self.nxt
        while sib is not None and sib is not self:
            s.append("{} ->".format(sib.val))
            if sib.nxt is self:
                s.append("loop to begin")
            sib = sib.nxt
        print(' '.join(s))


def read_input():
    lines = open(INPUT_FILE, "r").readlines()
    code = deque()
    for line in lines:
        code.append(int(line))
    print("input", code)
    return code


def shuffle(q: deque):
    val_order = deque()
    length = len(q)
    for (idx, val) in enumerate(q):
        # add original index to diff duplicates apart.
        val_order.append((val, idx))
    shuffled = deque(val_order)
    if len(val_order) > len(set(val_order)):
        raise Exception("duplicates where they should not be")
    for vi in val_order:
        (val, original_index) = vi
        if val == 0:
            continue
        old_idx = shuffled.index(vi)
        next_idx = (old_idx + val)
        if next_idx == 0:
            next_idx = length
        elif next_idx > length:
            next_idx = next_idx % length + 1
        elif next_idx < 0:
            next_idx = (next_idx + 5000 * length) % length - 1
        shuffled.remove(vi)
        shuffled.insert(next_idx, vi)

        print(vi[0], "moves from {} to {}".format(old_idx, next_idx))
        print(just_nums(shuffled), '\n')
    return just_nums(shuffled)


def just_nums(shuffled):
    just_nums = []
    for (val, idx) in shuffled:
        just_nums.append(val)
    return just_nums


def linked_list(code):
    nodes = [Node(v) for v in code]
    tail = nodes[len(nodes) - 1]
    head = nodes[0]
    tail.set_nxt(head)
    for i in range(len(nodes) - 1):
        n1 = nodes[i]
        n2 = nodes[i + 1]
        n1.set_nxt(n2)
    return nodes


def problem_one():
    code = read_input()
    nodes = linked_list(code)
    head = nodes[0]
    head.pprint()

    # shuffled = shuffle(code)
    # zero_idx = shuffled.index(0)
    # length = len(shuffled)
    # print("shuffled", shuffled)
    # v1000 = shuffled[(zero_idx + 1000) % length]
    # v2000 = shuffled[(zero_idx + 2000) % length]
    # v3000 = shuffled[(zero_idx + 3000) % length]
    # print("1000th {} 2000th {} 3000 {}".format(v1000, v2000, v3000))
    # print("\nP1 ans", v1000 + v2000 + v3000)


problem_one()

# problem_two()
