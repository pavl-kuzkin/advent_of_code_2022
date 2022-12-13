import math

lines_per_monkey = 7


class Monkey:
    def __init__(self, commands):
        self.false_monkey = None
        self.true_monkey = None
        self.inspect_count = 0
        print(commands)

        #  Starting items: 79, 98
        items_command = commands[1].strip()[16:].split(", ")
        self.items = list(map(lambda x: int(x), items_command))
        print(self.items)

        #  Operation: new = old * 19
        op_tokens = commands[2].strip()[17:].split()
        print(op_tokens)
        if op_tokens[1] == "*":
            if op_tokens[2] == "old":
                self.operation = lambda old: old * old
            else:
                self.operation = lambda old: old * int(op_tokens[2])
        elif op_tokens[1] == "+":
            if op_tokens[2] == "old":
                self.operation = lambda old: old + old
            else:
                self.operation = lambda old: old + int(op_tokens[2])
        else:
            raise Exception("Unexpected op token " + op_tokens[1])

        #  Test: divisible by 23
        self.divisible_by = int(commands[3].strip()[19:])
        print(self.divisible_by)

        #   If true: throw to monkey 2
        self.true_pass = int(commands[4].strip()[25:])
        print(self.true_pass)

        #   If false: throw to monkey 3
        self.false_pass = int(commands[5].strip()[26:])
        print(self.false_pass)

    def set_true_false_monkeys(self, li: list):
        self.true_monkey = li[self.true_pass]
        self.false_monkey = li[self.false_pass]

    def catch(self, item: int):
        self.items.append(item)

    def throw(self):
        self.items.pop(0)

    def handle_next_item(self):
        # Monkey inspects an item with a worry level of 79.
        next_item = self.items.pop(0)
        # Worry level is multiplied by 19 to 1501.
        inspected = self.operation(next_item)
        # Monkey gets bored with item. Worry level is divided by 3 to 500.
        bored = inspected // 3
        # Current worry level is not divisible by 23.
        test_result = bored % self.divisible_by == 0
        # Item with worry level 500 is thrown to monkey 3.
        if test_result:
            self.true_monkey.catch(bored)
        else:
            self.false_monkey.catch(bored)
        self.inspect_count += 1

    def do_turn(self):
        while len(self.items) > 0:
            self.handle_next_item()



rounds = 20

def p1():
    # set up
    lines = open("p1_input.txt", "r").readlines()
    monkeys = []
    for i in range(len(lines) // lines_per_monkey + 1):
        #  sample input for 1 monkey:
        # Monkey 0:
        #  Starting items: 79, 98
        #  Operation: new = old * 19
        #  Test: divisible by 23
        #   If true: throw to monkey 2
        #   If false: throw to monkey 3
        commands = lines[i * lines_per_monkey:(i + 1) * lines_per_monkey]
        monkeys.append(Monkey(commands))
    for m in monkeys:
        m.set_true_false_monkeys(monkeys)

    # do rounds
    for round in range(rounds):
        print("round", round)
        for m in monkeys:
            m.do_turn()
        for m in monkeys:
            print(m.items)

    # check results
    inspect_counts = []
    for m in monkeys:
        inspect_counts.append(m.inspect_count)
    inspect_counts.sort()
    print("P1", math.prod(inspect_counts[-2:]))

p1()
