from functools import reduce
from typing import List, Set

from .utils import parse_paragraphs


def parse_line_func(line):
    return {c for c in line.strip()}


def parse_input(lines):
    return parse_paragraphs(lines, parse_line_func)


def part1(groups: List[Set[str]]):
    answered_qs = []
    for group in groups:
        answered_qs.append(reduce(lambda acc, s: acc.union(s), group))
    return sum(len(a) for a in answered_qs)


def part2(groups):
    answered_qs = []
    for group in groups:
        answered_qs.append(reduce(lambda acc, s: acc.intersection(s), group))
    return sum(len(a) for a in answered_qs)