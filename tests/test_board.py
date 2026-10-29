from sudoku.board import can_place, find_empty, is_valid


# Testing function 'can_place'

def test_can_place_row_conflict():
    board = [[0 for _ in range(9)] for _ in range(9)]
    board[0][3] = 5

    assert can_place(board, 0, 0, 5) is False


def test_can_place_col_conflict():
    board = [[0 for _ in range(9)] for _ in range(9)]
    board[8][1] = 7

    assert can_place(board, 1, 1, 7) is False


def test_can_place_subgrid_conflict():
    board = [[0 for _ in range(9)] for _ in range(9)]
    board[4][5] = 9

    assert can_place(board, 3, 3, 9) is False


def test_can_place_valid():
    board = [[0 for _ in range(9)] for _ in range(9)]

    assert can_place(board, 6, 6, 9) is True


# Testing function 'find_empty'

def test_find_empty_first():
    board = [[0 for _ in range(9)] for _ in range(9)]

    assert find_empty(board) == (0, 0)


def test_find_empty_deep():
    board = [[1 for _ in range(9)] for _ in range(9)]
    board[7][7] = 0

    assert find_empty(board) == (7, 7)


def test_find_empty_none():
    board = [[1 for _ in range(9)] for _ in range(9)]

    assert find_empty(board) is None


# Testing function 'is_valid'

solved_board = [[2,1,4,6,9,7,8,3,5],
                [9,7,8,3,5,4,2,1,6],
                [3,6,5,2,1,8,4,9,7],
                [6,5,2,1,8,9,3,7,4],
                [1,4,9,7,3,5,6,8,2],
                [7,8,3,4,6,2,9,5,1],
                [5,3,6,8,4,1,7,2,9],
                [8,9,7,5,2,6,1,4,3],
                [4,2,1,9,7,3,5,6,8]]

solvable_medium = [[2,0,0,6,0,0,0,3,0],
                      [0,7,0,0,0,4,0,0,6],
                      [0,0,0,0,1,8,4,0,0],
                      [6,0,0,1,0,0,0,0,0],
                      [0,0,9,0,3,5,0,0,0],
                      [0,0,0,0,0,0,9,5,0],
                      [0,3,0,8,0,0,7,0,0],
                      [0,0,7,0,0,6,0,4,0],
                      [0,0,1,0,0,0,0,6,8]]

def test_complete_board():
    assert is_valid(solved_board)

def test_valid_partial_board():
    assert is_valid(solvable_medium)

invalid_board_rows = [[2,0,0,6,0,0,0,3,0],
                      [0,7,0,0,0,4,0,0,6],
                      [0,0,0,0,1,8,4,0,0],
                      [6,0,0,1,0,0,0,0,0],
                      [0,0,9,0,3,5,0,0,0],
                      [0,0,0,0,0,0,9,5,0],
                      [0,3,0,8,0,0,7,0,0],
                      [0,0,7,0,0,6,0,4,0],
                      [0,0,1,0,0,0,0,6,8],
                      [0,0,0,0,0,0,0,0,0]]

def test_too_many_rows():
    assert not is_valid(invalid_board_rows)

invalid_board_cells = [[2,0,0,6,0,0,0,3,0],
                      [0,7,0,0,0,4,0,0,6],
                      [0,0,0,0,1,8,4,0,0],
                      [6,0,0,1,0,0,0,0,0],
                      [0,0,9,0,3,5,0,0,0,0],
                      [0,0,0,0,0,0,9,5,0],
                      [0,3,0,8,0,0,7,0,0],
                      [0,0,7,0,0,6,0,4,0],
                      [0,0,1,0,0,0,0,6,8]]

def test_too_many_cells():
    assert not is_valid(invalid_board_cells)

board_decimal_value = [[2,0,0,6,0,0,0,3,0],
                      [0,7,0,0,0,4,0,0,6],
                      [0,0,0,0,1,8,4,0,0],
                      [6,0,0,1,0,0,0,0,0],
                      [0,0,9,0,3,5,0,0,0],
                      [0,0,0,0,0,0,9.2,5,0],
                      [0,3,0,8,0,0,7,0,0],
                      [0,0,7,0,0,6,0,4,0],
                      [0,0,1,0,0,0,0,6,8]]

def test_decimal_value():
    assert not is_valid(board_decimal_value)

board_value_out_of_range = [[2,0,0,6,0,0,0,3,0],
                      [0,7,0,0,0,4,0,0,6],
                      [0,0,0,0,1,8,4,0,0],
                      [6,0,0,1,0,0,0,0,0],
                      [0,0,9,0,3,5,0,0,0],
                      [0,0,0,0,0,0,9,5,0],
                      [0,3,0,8,0,0,7,0,0],
                      [0,0,7,0,0,6,0,4,0],
                      [0,0,1,0,0,0,0,10,8]]

def test_value_out_of_range():
    assert not is_valid(board_value_out_of_range)

board_row_duplicate = [[2,1,4,6,9,7,8,3,5],
                [9,7,8,3,5,4,2,1,6],
                [3,6,5,2,1,8,4,9,7],
                [6,5,2,1,8,9,3,7,4],
                [1,4,9,7,3,5,6,8,2],
                [7,8,3,4,6,2,9,5,1],
                [5,3,6,8,4,1,7,5,9],
                [8,9,7,5,2,6,1,4,3],
                [4,2,1,9,7,3,5,6,8]]

def test_row_duplicate():
    assert not is_valid(board_row_duplicate)

board_column_duplicate = [[2,1,4,6,9,7,8,3,5],
                [9,7,8,3,5,4,2,1,6],
                [3,6,5,2,1,8,4,9,7],
                [6,5,2,1,8,9,3,7,4],
                [1,4,9,7,3,5,6,8,2],
                [7,8,3,4,6,2,9,5,1],
                [5,0,6,8,4,1,7,3,9],
                [8,9,7,5,2,6,1,4,0],
                [4,2,1,9,7,3,5,6,8]]

def test_col_duplicate():
    assert not is_valid(board_column_duplicate)

board_subgrid_duplicate = [[2,1,4,6,9,7,8,3,5],
                [9,7,8,3,5,4,2,1,6],
                [3,6,5,2,1,8,4,9,7],
                [6,5,2,1,8,9,3,7,4],
                [1,4,9,7,3,5,6,8,2],
                [0,8,3,4,6,2,9,5,1],
                [5,3,6,8,4,1,7,2,9],
                [8,9,7,5,2,6,1,4,3],
                [7,2,1,9,0,3,5,6,8]]

def test_subgrid_duplicate():
    assert not is_valid(board_subgrid_duplicate)