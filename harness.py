#!/usr/bin/env python3

import argparse
from copy import deepcopy
from glob import glob
from importlib import import_module
from prettytable import PrettyTable
import timeit
from typing import List


def run_part(mod, part_num: int, input_data):
    part_name = f'part{part_num}'
    f = getattr(mod, part_name)
    start = timeit.default_timer()
    result = f(input_data)
    time_taken = timeit.default_timer() - start 
    return (part_name, result, time_taken)


def run(input_file: str, parts: List[int]):
    with open(input_file, 'r') as f:
        base_input = f.readlines()

    parsed_input = mod.parse_input(base_input)

    results = []
    for part in parts:
        part_input = deepcopy(parsed_input)
        print(f'Executing part {part}... ')
        results.append(run_part(mod, part, part_input))
        print('[Done]')

    return results


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
    parser.add_argument('-p', '--part', type=int, nargs='+', help='run only the specified part(s) of the problem')
    args = parser.parse_args()

    mod = import_module(f'problems.{args.problem}')

    inputs = []
    if args.input:
        inputs = args.input
    elif args.test:
        inputs = glob(f'./test_inputs/{args.problem}_*.in')
    else:
        inputs = [f'inputs/{args.problem}.in']

    parts = []
    if args.part:
        parts = args.part
    else:
        parts = [1, 2]

    for i in inputs:
        print(f'Running with input {i}:')
        results = run(i, parts)
        print_results(results)
    