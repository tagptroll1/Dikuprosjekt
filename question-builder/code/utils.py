import os
from itertools import count


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def get_int_input(txt):
    while True:
        try:
            inp = int(input(txt))
        except ValueError:
            print("Not a number, try again")
        else:
            return inp


def get_multi_line_input(txt="", end=None):
    lines = []

    print(txt, "(Supports new lines, enter on a blank line to exit)", sep="")
    if end:
        print(end)

    for i in count(1):
        try:
            line = input(f"{i} |")
        except KeyboardInterrupt:
            return []

        if not line:  # line was blank
            break

        lines.append(line)

    return lines
