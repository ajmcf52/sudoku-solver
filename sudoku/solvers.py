from sudoku.board import can_place, find_empty, is_valid

def solve(board: list[list[int]]) -> bool:
    if not is_valid(board):
        return False
    return solve_backtracking(board)

def solve_backtracking(board: list[list[int]]) -> bool:
    """
    solve recursively in-place; returns whether a solution is found.
    """

    next_empty = find_empty(board)

    if next_empty is None:
        return True

    row, col = next_empty

    for i in range(1,10):
        if can_place(board, row, col, i):
            board[row][col] = i
            if solve_backtracking(board):
                return True
            board[row][col] = 0
    return False