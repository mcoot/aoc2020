from typing import Set, Tuple


def parse_input(lines):
    state = set()
    for y, line in enumerate(lines):
        for x, c in enumerate(line.strip()):
            if c == '#':
                state.add((x, y, 0, 0))
    return state


def get_neighbours_active(board: Set[Tuple[int, int, int, int]], x: int, y: int, z: int, w: int) -> int:
    count = 0
    for x_o in [-1, 0, 1]:
        for y_o in [-1, 0, 1]:
            for z_o in [-1, 0, 1]:
                for w_o in [-1, 0, 1]:
                    if x_o == 0 and y_o == 0 and z_o == 0 and w_o == 0:
                        continue
                    if (x + x_o, y + y_o, z + z_o, w + w_o) in board:
                        count += 1
    return count


def find_extents(board: Set[Tuple[int, int, int, int]]) -> Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int], Tuple[int, int]]:
    # Find the x, y and z extents of active cells in the board
    xs = sorted([x for (x, _, _, _) in board])
    ys = sorted([y for (_, y, _, _) in board])
    zs = sorted([z for (_, _, z, _) in board])
    ws = sorted([w for (_, _, _, w) in board])

    return (xs[0], xs[-1]), (ys[0], ys[-1]), (zs[0], zs[-1]), (ws[0], ws[-1])


def step_cycle_pt1(board: Set[Tuple[int, int, int, int]]) -> Set[Tuple[int, int, int, int]]:
    new_board = set()

    # Find things to activate or deactivate
    (x_min, x_max), (y_min, y_max), (z_min, z_max), _ = find_extents(board)
    for x in range(x_min - 1, x_max + 2):
        for y in range(y_min - 1, y_max + 2):
            for z in range(z_min - 1, z_max + 2):
                count = get_neighbours_active(board, x, y, z, 0)
                if (x, y, z, 0) in board:
                    # Currently active, stay active if 2 or 3 neighbours active
                    if count == 2 or count == 3:
                        new_board.add((x, y, z, 0))
                else:
                    # Currently inactive, become active if exactly three neighbours active
                    if count == 3:
                        new_board.add((x, y, z, 0))

    return new_board


def part1(board: Set[Tuple[int, int, int, int]]):
    for i in range(6):
        board = step_cycle_pt1(board)
    return len(board)
    

def step_cycle_pt2(board: Set[Tuple[int, int, int, int]]) -> Set[Tuple[int, int, int, int]]:
    new_board = set()

    # Find things to activate or deactivate
    (x_min, x_max), (y_min, y_max), (z_min, z_max), (w_min, w_max) = find_extents(board)
    for x in range(x_min - 1, x_max + 2):
        for y in range(y_min - 1, y_max + 2):
            for z in range(z_min - 1, z_max + 2):
                for w in range(w_min - 1, w_max + 2):
                    count = get_neighbours_active(board, x, y, z, w)
                    if (x, y, z, w) in board:
                        # Currently active, stay active if 2 or 3 neighbours active
                        if count == 2 or count == 3:
                            new_board.add((x, y, z, w))
                    else:
                        # Currently inactive, become active if exactly three neighbours active
                        if count == 3:
                            new_board.add((x, y, z, w))

    return new_board


def part2(board: Set[Tuple[int, int, int, int]]):
    for i in range(6):
        board = step_cycle_pt2(board)
    return len(board)