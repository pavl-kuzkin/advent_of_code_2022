import sys, os

INPUT_FILE = "ez-input.txt"

def read_input():
    path = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), INPUT_FILE)
    parsed = []
    for line in open(path, "r").readlines():
        parsed.append(parse_line(line.strip()))
    return parsed

def parse_line(line: str):
    return line

read_input()