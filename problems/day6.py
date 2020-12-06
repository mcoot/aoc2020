from functools import reduce
from typing import List, Set

def parse_input(lines):
    groups = []
    cur_group = []
    for line in lines:
        if line.strip() == '':
            groups.append(cur_group)
            cur_group = []
        else:
            cur_group.append({c for c in line.strip()})
    groups.append(cur_group)
    return groups


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