from collections import Counter
from typing import List


def parse_input(lines):
    return [int(line.strip()) for line in lines]


def part1(adaptors: List[int]):
    adaptors = sorted([0] + adaptors)
    diffs_count = Counter()
    for i in range(1, len(adaptors)):
        this_diff = adaptors[i] - adaptors[i-1]
        diffs_count[this_diff] += 1
    diffs_count[3] += 1
    return diffs_count[1] * diffs_count[3]


def joltage_combos(adaptors: List[int], i: int, cache):
    if i == len(adaptors) - 1:
        cache[i] = 1
        return 1
    
    next_choices = [j 
                    for (j, val) 
                    in enumerate(adaptors) 
                    if j > i and adaptors[j] - adaptors[i] <= 3]
    
    choices_from_here = 0
    for choice in next_choices:
        if choice not in cache:
            cache[choice] = joltage_combos(adaptors, choice, cache)
        choices_from_here += cache[choice]
    
    return choices_from_here


def part2(adaptors: List[int]):
    adaptors = sorted([0] + adaptors)

    combos = joltage_combos(adaptors, 0, dict())

    return combos