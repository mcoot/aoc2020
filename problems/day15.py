from collections import defaultdict
import sys
from typing import Dict, Set


def parse_input(lines):
    return [int(n) for n in lines[0].split(',')]


def apply_rule(seen, turn: int, last_num: int) -> int:
    if len(seen[last_num]) > 1:
        most_recent = seen[last_num][-1]
        second_most_recent = seen[last_num][-2]
        number_to_speak = most_recent - second_most_recent
    else:
        number_to_speak = 0
    seen[number_to_speak].append(turn)
    if len(seen[number_to_speak]) > 5:
        seen[number_to_speak] = seen[number_to_speak][-3:]
    return number_to_speak


def get_nth_number(starting_numbers, count: int) -> int:
    seen = defaultdict(list)
    most_recent = starting_numbers[-1]
    for i, n in enumerate(starting_numbers):
        seen[n].append(i)
    for turn in range(len(starting_numbers), count):
        most_recent = apply_rule(seen, turn, most_recent)
    return most_recent


def part1(starting_numbers):
    return get_nth_number(starting_numbers, 2020)


def part2(starting_numbers):
    return get_nth_number(starting_numbers, 30000000)