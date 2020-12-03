from functools import reduce
import operator

def parse_input(lines):
    field = []
    for line in lines:
        field.append([c == '#' for c in line.strip()])
    return field

def trees_on_slope(field, slope):
    width = len(field[0])
    pos = 0 + 0j
    num_trees = 0
    while True:
        pos += slope
        if pos.imag >= len(field):
            break
        if field[int(pos.imag)][int(pos.real) % width]:
            num_trees += 1
    return num_trees

def part1(field):
    return trees_on_slope(field, 3 + 1j)

def part2(field):
    slopes = [
        1 + 1j,
        3 + 1j,
        5 + 1j,
        7 + 1j,
        1 + 2j,
    ]
    return reduce(operator.mul, (trees_on_slope(field, s) for s in slopes), 1)