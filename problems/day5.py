from typing import Dict, List, NamedTuple, Set

class Pass(NamedTuple):
    row_bsp: List[bool]
    col_bsp: List[bool]


def bsp_char_to_bool(c: str) -> bool:
    return c == 'B' or c == 'R'


def parse_input(lines):
    res = []
    for line in lines:
        row_bsp = list(bsp_char_to_bool(c) for c in line.strip()[0:7])
        col_bsp = list(bsp_char_to_bool(c) for c in line.strip()[7:])
        res.append(Pass(row_bsp, col_bsp))
    return res


def resolve_bsp(bsp: List[bool], lower: int, upper: int):
    search_range = upper - lower

    if len(bsp) == 0:
        # End of specification
        # We're assuming out bsp was complete here
        return lower
    if bsp[0]:
        # Upper half
        return resolve_bsp(bsp[1:], lower + search_range // 2, upper)
    else:
        # Lower half
        return resolve_bsp(bsp[1:], lower, lower + search_range // 2)


def resolve_seat(p: Pass) -> complex:
    row = resolve_bsp(p.row_bsp, 0, 2**len(p.row_bsp))
    col = resolve_bsp(p.col_bsp, 0, 2**len(p.col_bsp))
    return complex(row, col)


def seat_id(seat: complex) -> int:
    return int(8 * seat.real + seat.imag)


def part1(passes):
    resolved = [resolve_seat(p) for p in passes]
    return max(seat_id(s) for s in resolved)


def find_lone_missing_seat(seat_ids: Set[int]) -> int:
    # Add -1 as an initial so we can catch missing seats at the start
    seats = [-1]
    seats.extend(sorted(seat_ids))

    for i in range(1, len(seats)):
        cur = seats[i]
        prev = seats[i - 1]
        missing_range = cur - prev - 1
        if prev != -1 and missing_range == 1:
            # Bingo, exactly one missing seat
            return cur - 1
    
    return None


def part2(passes):
    return find_lone_missing_seat(set(seat_id(resolve_seat(p)) for p in passes))