from typing import List, Tuple


CELL_EMPTY = 'L'
CELL_OCCUPIED = '#'
CELL_FLOOR = '.'


def parse_input(lines):
    return [[cell for cell in line.strip()] for line in lines]


def adjacent_occupied_count(board: List[List[str]], row: int, col: int) -> int:
    count = 0
    for row_offset in [-1, 0, 1]:
        cur_row = row + row_offset
        # Don't check the row if out of bounds
        if cur_row < 0 or cur_row >= len(board):
            continue
        for col_offset in [-1, 0, 1]:
            cur_col = col + col_offset
            # Don't check out of bounds columns
            if cur_col < 0 or cur_col >= len(board[cur_row]):
                continue
            # Check neighbours but not the central cell
            if row_offset == 0 and col_offset == 0:
                continue
            if board[cur_row][cur_col] == CELL_OCCUPIED:
                count += 1
    return count


def part1_rule(board: List[List[str]], row: int, col: int):
    if board[row][col] == CELL_EMPTY:
        if adjacent_occupied_count(board, row, col) == 0:
            return CELL_OCCUPIED
    elif board[row][col] == CELL_OCCUPIED:
        if adjacent_occupied_count(board, row, col) >= 4:
            return CELL_EMPTY
    return board[row][col]


def step(board: List[List[str]], rule) -> Tuple[List[List[str]], bool]:
    has_changed = False
    next_board = [r.copy() for r in board]
    for row in range(len(board)):
        for col in range(len(board[row])):
            next_board[row][col] = rule(board, row, col)
            if next_board[row][col] != board[row][col]:
                has_changed = True
    return next_board, has_changed


def total_occupied_seats(board: List[List[str]]) -> int:
    return sum([cell == CELL_OCCUPIED for row in board for cell in row])


def find_equilibrium(board: List[List[str]], rule) -> List[List[str]]:
    still_changing = True
    while still_changing:
        board, still_changing = step(board, rule)
    return board


def part1(board: List[List[str]]):
    return total_occupied_seats(find_equilibrium(board, part1_rule))


def is_first_visible_occupied(board: List[List[str]], row: int, col: int, move_vec: Tuple[int, int]) -> bool:
    while True:
        row = row + move_vec[0]
        col = col + move_vec[1]
        # Can't be occupied off the board
        if row < 0 or col < 0 or row >= len(board) or col >= len(board[row]):
            return False

        if board[row][col] == CELL_EMPTY:
            return False
        elif board[row][col] == CELL_OCCUPIED:
            return True



def visible_occupied_count(board: List[List[str]], row: int, col: int) -> int:
    return sum([is_first_visible_occupied(board, row, col, (row_dir, col_dir)) 
                for row_dir in [-1, 0, 1] 
                for col_dir in [-1, 0, 1]
                if row_dir != 0 or col_dir != 0])


def part2_rule(board: List[List[str]], row: int, col: int):
    if board[row][col] == CELL_EMPTY:
        if visible_occupied_count(board, row, col) == 0:
            return CELL_OCCUPIED
    elif board[row][col] == CELL_OCCUPIED:
        if visible_occupied_count(board, row, col) >= 5:
            return CELL_EMPTY
    return board[row][col]


def part2(board: List[List[str]]):
    return total_occupied_seats(find_equilibrium(board, part2_rule))