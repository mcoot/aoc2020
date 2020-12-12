import cmath
from dataclasses import dataclass
import math
import re

from .utils import parse_lines_regex


LINE_RE = re.compile(r'^([A-Z])(\d+)$')


@dataclass(frozen=True)
class Action:
    command: str
    val: int


@dataclass
class State:
    pos: complex
    dir: int
    waypoint: complex


def parse_action(m: re.Match):
    return Action(m.group(1), int(m.group(2)))


def parse_input(lines):
    return parse_lines_regex(lines, LINE_RE, parse_action)


def manhattan_distance(pos: complex):
    return abs(pos.real) + abs(pos.imag)


def execute_action_part1(state: State, action: Action):
    if action.command == 'N':
        state.pos += complex(0, action.val)
    elif action.command == 'S':
        state.pos -= complex(0, action.val)
    elif action.command == 'E':
        state.pos += complex(action.val, 0)
    elif action.command == 'W':
        state.pos -= complex(action.val, 0)
    elif action.command == 'L':
        state.dir = (state.dir + action.val) % 360
    elif action.command == 'R':
        state.dir = (state.dir - action.val) % 360
    elif action.command == 'F':
        move_vec = cmath.rect(action.val, math.radians(state.dir))
        move_vec = complex(round(move_vec.real), round(move_vec.imag))
        state.pos += move_vec


def part1(actions):
    state = State(0 + 0j, 0, 0 + 0j)
    for action in actions:
        execute_action_part1(state, action)
    return manhattan_distance(state.pos)
    

def rotate_deg(vec: complex, deg: int):
    r, phi = cmath.polar(vec)
    phi += math.radians(deg)
    return cmath.rect(r, phi)


def execute_action_part2(state: State, action: Action):
    if action.command == 'N':
        state.waypoint += complex(0, action.val)
    elif action.command == 'S':
        state.waypoint -= complex(0, action.val)
    elif action.command == 'E':
        state.waypoint += complex(action.val, 0)
    elif action.command == 'W':
        state.waypoint -= complex(action.val, 0)
    elif action.command == 'L':
        state.waypoint = rotate_deg(state.waypoint, action.val)
    elif action.command == 'R':
        state.waypoint = rotate_deg(state.waypoint, -action.val)
    elif action.command == 'F':
        state.pos += action.val * state.waypoint


def part2(actions):
    state = State(0 + 0j, 0, 10 + 1j)
    for action in actions:
        execute_action_part2(state, action)
    return manhattan_distance(state.pos)