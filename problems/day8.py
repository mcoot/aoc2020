from dataclasses import dataclass
import re
from typing import List, Set

from .utils import parse_lines_regex


INSTRUCTION_RE = re.compile(r'(\w+) ([+\-]\d+)')


@dataclass
class Instruction:
    operation: str
    arg: int


@dataclass
class ProgramState:
    program: List[Instruction]
    pc: int
    accumulator: int

    def current_instruction(self):
        return self.program[self.pc] if self.pc < len(self.program) else None


def construct_instruction(m: re.Match):
    return Instruction(m.group(1), int(m.group(2)))


def parse_input(lines):
    return parse_lines_regex(lines, INSTRUCTION_RE, construct_instruction)


# ---------------


def initial_state(program: List[Instruction]) -> ProgramState:
    return ProgramState(program, 0, 0)


def execute_instruction(state: ProgramState):
    instr = state.current_instruction()
    if instr is None:
        return
    if instr.operation == 'acc':
        state.accumulator += instr.arg
        state.pc += 1
    elif instr.operation == 'jmp':
        state.pc += instr.arg
    elif instr.operation == 'nop':
        state.pc += 1


def execute_until_loop_or_termination(program: List[Instruction]) -> ProgramState:
    state = initial_state(program)
    visited_pcs: Set[int] = set()
    while state.pc not in visited_pcs and state.pc < len(state.program):
        visited_pcs.add(state.pc)
        execute_instruction(state)
    return state
    

def part1(program: List[Instruction]):
    return execute_until_loop_or_termination(program).accumulator


# ---------------


def part2(program):
    # Try flipping each jmp and nop
    resulting_acc = None
    for (idx, instr) in enumerate(program):
        modified_prog = program.copy()
        if instr.operation == 'jmp':
            modified_prog[idx] = Instruction('nop', instr.arg)
            result = execute_until_loop_or_termination(modified_prog)
        elif instr.operation == 'nop':
            modified_prog[idx] = Instruction('jmp', instr.arg)
            result = execute_until_loop_or_termination(modified_prog)
        else:
            continue
        if result.pc >= len(program):
            resulting_acc = result.accumulator
    
    return resulting_acc