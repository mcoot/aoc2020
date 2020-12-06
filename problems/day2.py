import re
from typing import NamedTuple

from .utils import parse_lines_regex


class Row(NamedTuple):
    lowerBound: int
    upperBound: int
    requiredChar: str
    password: str

LINE_RE = re.compile(r'(\d+)-(\d+) (\w): (\w+)')


def construct_row(m: re.Match):
    return Row(lowerBound=int(m.group(1)), 
               upperBound=int(m.group(2)), 
               requiredChar=m.group(3), 
               password=m.group(4))


def parse_input(lines):
    return parse_lines_regex(lines, LINE_RE, construct_row)


def is_password_valid_pt1(row: Row):
    count = row.password.count(row.requiredChar)
    return count >= row.lowerBound and count <= row.upperBound

def is_password_valid_pt2(row: Row):
    pos_a = row.password[row.lowerBound - 1]
    pos_b = row.password[row.upperBound - 1]
    return (pos_a == row.requiredChar) ^ (pos_b == row.requiredChar)

def part1(rows):
    return sum(is_password_valid_pt1(r) for r in rows)

def part2(rows):
    return sum(is_password_valid_pt2(r) for r in rows)