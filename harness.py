#!/usr/bin/env python3

import argparse
from importlib import import_module
import timeit

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('problem', type=str, help='the problem to run')
    parser.add_argument('-i', '--input', type=str, help='the input file to run with')
    args = parser.parse_args()
    if args.input is None:
        args.input = f'inputs/{args.problem}.in'

    mod = import_module(f'problems.{args.problem}')

    with open(args.input, 'r') as f:
        base_input = f.readlines()

    parsed_input = mod.parse_input(base_input)
    
    print('Running part 1:')
    start = timeit.default_timer()
    result = mod.part1(parsed_input)
    taken = timeit.default_timer() - start
    print(f'Result ({taken:.6f}s): {result}')

    print('Running part 2:')
    start = timeit.default_timer()
    result = mod.part2(parsed_input)
    taken = timeit.default_timer() - start
    print(f'Result ({taken:.6f}s): {result}')
    