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
        # You count the pixels on the CRT: 40 wide and 6 high.
        self.pixels = arr = ["." for element in range(40 * 6)]

    def tik(self):
        self.cycle_number += 1
        # P1 keep track of signal
        if check_signal(self.cycle_number):
            self.signal_history[self.cycle_number] = self.X * self.cycle_number

        # P2 check pixel
        pixel_idx = self.cycle_number - 1
        if self.X-1 <= pixel_idx % 40 <= self.X+1:
            self.pixels[pixel_idx] = "#"


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
        print("P2")
        for i in range(6):
            row = self.pixels[40*i:40*(i+1)]
            print("".join(row))


def solve():
    cpu = CPU()
    cpu.run(open("input.txt", "r").readlines())


solve()
