# consider the signal strength (the cycle number multiplied by the value of the X register)
# during the 20th cycle and every 40 cycles after that
# (that is, during the 20th, 60th, 100th, 140th, 180th, and 220th cycles).
def check_signal(cycle: int):
    return (cycle - 20) % 40 == 0


def p1():
    X = 1
    signal_history = {}
    cycle_number = 1
    command_idx = 0
    lines = open("ez_input.txt", "r").readlines()
    while command_idx < len(lines):

        tokens = lines[command_idx].strip().split()
        # addx V takes two cycles to complete.
        if tokens[0] == "addx":
            cycle_number += 2
        # noop takes one cycle to complete. It has no other effect.
        elif tokens[0] == "noop":
            cycle_number += 1

        # check signal before adding to X
        if check_signal(cycle_number):
            print("------", cycle_number, X)
            signal_history[cycle_number] = X * cycle_number

        # After two cycles, the X register is increased by the value V. (V can be negative.)
        if tokens[0] == "addx":
            X += int(tokens[1])
        command_idx += 1
    print(signal_history)


p1()
