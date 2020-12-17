from dataclasses import dataclass
from functools import reduce
import re
from typing import Dict, List, Tuple


FIELD_DEF_RE = re.compile(r'^([\w\s]+): (\d+)-(\d+) or (\d+)-(\d+)$')


@dataclass
class FieldDef:
    name: str
    bounds: List[Tuple[int, int]]


@dataclass
class Data:
    field_defs: Dict[str, FieldDef]
    my_ticket: List[int]
    other_tickets: List[List[int]]


def parse_input(lines: List[str]):
    section = 0
    field_defs = dict()
    my_ticket = []
    other_tickets = []
    for line in lines:
        if line.strip() == '':
            continue
        elif line.strip().startswith('your ticket'):
            section = 1
        elif line.strip().startswith('nearby tickets'):
            section = 2
        elif section == 0:
            m = FIELD_DEF_RE.match(line.strip())
            if not m:
                raise ValueError(f'Failed to match {line}')
            field_name = m.group(1)
            field_bound1_lower = int(m.group(2))
            field_bound1_upper = int(m.group(3))
            field_bound2_lower = int(m.group(4))
            field_bound2_upper = int(m.group(5))
            field_defs[field_name] = FieldDef(field_name, 
                                              [(field_bound1_lower, field_bound1_upper), 
                                               (field_bound2_lower, field_bound2_upper)])
        elif section == 1:
            my_ticket = [int(x) for x in line.strip().split(',')]
        elif section == 2:
            other_tickets.append([int(x) for x in line.strip().split(',')])
    return Data(field_defs, my_ticket, other_tickets)


def does_value_fit_field(field: FieldDef, value: int) -> bool:
    for lower, upper in field.bounds:
        if value >= lower and value <= upper:
            return True
    return False


def invalid_values_in_ticket(fields: Dict[str, FieldDef], ticket: List[int]):
    invalid_values = []
    for value in ticket:
        found_fitting_field = False
        for field in fields.values():
            if does_value_fit_field(field, value):
                found_fitting_field = True
                break
        if not found_fitting_field:
            invalid_values.append(value)
    return invalid_values


def part1(data: Data):
    invalid_values = []
    for ticket in data.other_tickets:
        invalid_values.extend(invalid_values_in_ticket(data.field_defs, ticket))
    return sum(invalid_values)


def get_valid_tickets(data: Data) -> List[List[int]]:
    valid_tickets = []
    for ticket in data.other_tickets:
        if len(invalid_values_in_ticket(data.field_defs, ticket)) == 0:
            valid_tickets.append(ticket)
    return valid_tickets


def is_column_possible_for_field(field: FieldDef, col: int, tickets: List[List[int]]):
    for ticket in tickets:
        if not does_value_fit_field(field, ticket[col]):
            return False
    return True


def determine_field_mappings(field_defs: Dict[str, FieldDef], tickets: List[List[int]]) -> Dict[str, int]:
    result = dict()
    remaining_fields = field_defs.copy()
    possible_mappings = {f: list(range(len(tickets[0]))) for f in field_defs.keys()}

    for field in field_defs.values():
        possible_resulting_mappings = possible_mappings[field.name]
        for possible_col in possible_mappings[field.name]:
            if not is_column_possible_for_field(field, possible_col, tickets):
                possible_resulting_mappings.remove(possible_col)
        possible_mappings[field.name] = possible_resulting_mappings

    print({f: len(m) for f, m in possible_mappings.items()})

    # for col in range(len(tickets[0])):
    #     # Find the field that can hold all values across tickets in this column
    #     for field in remaining_fields.values():
    #         does_fit = True
    #         for ticket in tickets:
    #             if not does_value_fit_field(field, ticket[col]):
    #                 does_fit = False
    #                 break
    #         if does_fit:
    #             # fitting = [t[col] for t in tickets]
    #             # print(f'Found {field.name}->{col} because of {fitting}')
    #             result[field.name] = col
    #             del remaining_fields[field.name]
    #             break
    return result


def apply_mapping(mapping: Dict[str, int], ticket: List[int]) -> Dict[str, int]:
    return {f: ticket[col] for f, col in mapping.items()}


def part2(data: Data):
    valid_tickets = get_valid_tickets(data)
    mapping = determine_field_mappings(data.field_defs, valid_tickets)
    print(len(mapping))
    decoded_ticket = apply_mapping(mapping, data.my_ticket)
    print(decoded_ticket)
    departure_fields = {f: v for f, v in decoded_ticket.items() if f.startswith('departure')}
    return reduce(lambda a, b: a * b, departure_fields.values())
    
