from sudoku.board import can_place

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