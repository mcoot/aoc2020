#!/usr/bin/env python3

import argparse
from glob import glob
from importlib import import_module
from prettytable import PrettyTable
import sys
import timeit


def run_part(mod, part_num: int, input_data):
    part_name = f'part{part_num}'
    f = getattr(mod, part_name)
    start = timeit.default_timer()
    result = f(input_data)
    time_taken = timeit.default_timer() - start 
    return (part_name, result, time_taken)


def run(input_file: str):
    with open(input_file, 'r') as f:
        base_input = f.readlines()

    parsed_input = mod.parse_input(base_input)
    
    sys.stdout.write('Executing part 1... ')
    part1 = run_part(mod, 1, parsed_input)
    print('[Done]')
    sys.stdout.write('Executing part 2... ')
    part2 = run_part(mod, 2, parsed_input)
    print('[Done]')

    return [part1, part2]


def print_results(results):
    table = PrettyTable(["Part", "Result", "Time"])
    table.add_rows(results)
    table.float_format = '.6'
    print(table)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('problem', type=str, help='the problem to run')
    parser.add_argument('-t', '--test', action='store_true', help='run the test inputs')
    parser.add_argument('-i', '--input', type=str, nargs='+', help='manually specify the input file(s) to run with')
    args = parser.parse_args()

    mod = import_module(f'problems.{args.problem}')

    inputs = []
    if args.input:
        inputs = args.input
    elif args.test:
        inputs = glob(f'./test_inputs/{args.problem}_*.in')
    else:
        inputs = [f'inputs/{args.problem}.in']

    for i in inputs:
        print(f'Running with input {i}:')
        results = run(i)
        print_results(results)
    