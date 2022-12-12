# consider the signal strength (the cycle number multiplied by the value of the X register)
# during the 20th cycle and every 40 cycles after that
# (that is, during the 20th, 60th, 100th, 140th, 180th, and 220th cycles).
def check_signal(cycle: int):
    return (cycle - 20) % 40 == 0


class CPU:
    def __init__(self):
        self.X = 1
        self.cycle_number = 0
        self.signal_history = {}

    def tik(self):
        self.cycle_number += 1
        if check_signal(self.cycle_number):
            self.signal_history[self.cycle_number] = self.X * self.cycle_number
            # print("---", self.cycle_number, self.X, self.signal_history[self.cycle_number])

    def addx(self, val: int):
        self.X += val

    def run(self, commands: list):
        for command in commands:
            # print(command.strip())
            tokens = command.strip().split()
            if tokens[0] == "addx":
                self.tik()
                self.tik()
                self.addx(int(tokens[1]))
            else:
                self.tik()
        # print(self.signal_history)
        print("P1", sum(self.signal_history.values()))


def p1():
    X = 1
    signal_history = {}
    cycle_number = 1
    command_idx = 0
    lines = open("input.txt", "r").readlines()
    cpu = CPU()
    cpu.run(lines)


p1()
