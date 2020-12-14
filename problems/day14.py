from dataclasses import dataclass
import re
from typing import Dict, List


MEM_RE = re.compile(r'^mem\[(\d+)\]$')


@dataclass
class Instr:
    pass


@dataclass
class SetMaskInstr(Instr):
    mask: List[int]


@dataclass
class SetValueInstr(Instr):
    address: int
    value: int


@dataclass
class State:
    program: List[Instr]
    pc: int
    mask: List[int]
    values: Dict[int, int]


def parse_input(lines):
    program = []
    for line in lines:
        sections = [seg.strip() for seg in line.split('=')]
        val = sections[1]
        command = sections[0]
        if command == 'mask':
            program.append(SetMaskInstr([-1 if c == 'X' else int(c) for c in val]))
        else:
            m = MEM_RE.match(command)
            if not m:
                raise ValueError(f'Failed to match {command}')
            program.append(SetValueInstr(int(m.group(1)), int(val)))
    return program


def initial_state(program: List[Instr]) -> State:
    return State(program, 0, [-1] * 36, dict())


def apply_mask_part1(mask: List[int], value: int) -> int:
    or_mask = int(''.join(['1' if bit == 1 else '0' for bit in mask]), base=2)
    and_mask = int(''.join(['0' if bit == 0 else '1' for bit in mask]), base=2)
    return (value | or_mask) & and_mask


def apply_set_value_part1(state: State, instr: SetValueInstr):
    state.values[instr.address] = apply_mask_part1(state.mask, instr.value)


def step_program(state: State, apply_set_value):
    if state.pc >= len(state.program):
        return

    instr = state.program[state.pc]
    if isinstance(instr, SetMaskInstr):
        state.mask = instr.mask
    elif isinstance(instr, SetValueInstr):
        apply_set_value(state, instr)

    state.pc += 1


def run_program(state: State, apply_set_value):
    while state.pc < len(state.program):
        step_program(state, apply_set_value)
    return state


def part1(program: List[Instr]):
    state = initial_state(program)
    run_program(state, apply_set_value_part1)
    return sum(state.values.values())


def apply_mask_part2(mask: List[int], address: int) -> List[int]:
    # Apply 1 overwrite
    starting_address = address | int(''.join(['1' if bit == 1 else '0' for bit in mask]), base=2)
    # Calculate floating addresses
    resulting_addresses = [starting_address]
    for idx, bit in enumerate(mask):
        pos = len(mask) - idx - 1
        if bit != -1:
            continue
        new_addresses = []
        for addr in resulting_addresses:
            # 0 case
            new_addresses.append(addr & (0xFFFFFFFFF ^ (1 << pos)))
            # 1 case
            new_addresses.append(addr | (1 << pos))
        resulting_addresses = new_addresses
    return resulting_addresses


def apply_set_value_part2(state: State, instr: SetValueInstr):
    addrs_to_write_to = apply_mask_part2(state.mask, instr.address)
    for addr in addrs_to_write_to:
        state.values[addr] = instr.value


def part2(program: List[Instr]):
    state = initial_state(program)
    run_program(state, apply_set_value_part2)
    return sum(state.values.values())