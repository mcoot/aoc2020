from functools import reduce
import math

# Implementation of CRT from https://rosettacode.org/wiki/Chinese_remainder_theorem#Python


def chinese_remainder(bus_ids_with_offsets):
    s = 0
    prod = reduce(lambda a, b: a*b, (b[1] for b in bus_ids_with_offsets))
    for a_i, n_i in bus_ids_with_offsets:
        p = prod // n_i
        s += a_i * mul_inv(p, n_i) * p
        print(s)
    return s % prod
 
 
 
def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a%b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1


def parse_input(lines):
    earliest_timestamp = int(lines[0].strip())
    bus_ids = [int(s) if s.isdigit() else None for s in lines[1].strip().split(',') ]
    return (earliest_timestamp, bus_ids)


def part1(i):
    earliest_timestamp = i[0]
    bus_ids = i[1]
    
    best = None
    best_bus = None
    for bus in bus_ids:
        if bus is None:
            continue
        first_bus = bus * math.ceil(earliest_timestamp / bus)
        if best is None or first_bus < best:
            best = first_bus
            best_bus = bus
    
    return best_bus * (best - earliest_timestamp)


def part2(i):
    bus_ids = i[1]
    bus_ids_with_offsets = [(-idx, bus_id) for idx, bus_id in enumerate(bus_ids) if bus_id is not None]
    return chinese_remainder(bus_ids_with_offsets)
