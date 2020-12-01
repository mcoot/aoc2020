#!/usr/bin/env python3

def parse_input(lines):
    return set(int(r.strip()) for r in lines)

def calc_part1(report, target):
    for e in report:
        if target - e in report:
            return e * (target - e)
    return None

def part1(report):
    return calc_part1(report, 2020)

def part2(report):
    # Create a set of 2020 - e for e in the original set
    report_minus = set(2020 - e for e in report)    
    for target in report_minus:
        # First number, from our original set
        e1 = 2020 - target
        # Now try to find a second and third number by applying the logic from part1
        res = calc_part1(report, target)
        if res != None:
            return e1 * res
    return None