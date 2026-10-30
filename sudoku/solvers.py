from sudoku.board import can_place, find_empty, is_valid
from sudoku.metrics import SearchMetrics
from time import perf_counter

def solve(board: list[list[int]]) -> tuple[bool,SearchMetrics]:
    
    metrics = SearchMetrics()
    if not is_valid(board):
        return (False,metrics)

    start = perf_counter()
    finished = solve_backtracking(board, metrics, 0)
    elapsed = perf_counter() - start
    metrics.elapsed_sec = elapsed

    return (finished,metrics)

def solve_backtracking(board: list[list[int]], metrics: SearchMetrics, depth: int) -> bool:
    """
    solve recursively in-place; returns whether a solution is found.
    """

    # verify depth; increment recursive call count
    metrics.solver_calls += 1
    metrics.max_depth = max(metrics.max_depth, depth)

    next_empty = find_empty(board)

    if next_empty is None:
        return True

    row, col = next_empty

    for i in range(1,10):
        if can_place(board, row, col, i):
            
            # placing digit i at (row,col)
            board[row][col] = i
            metrics.placements += 1

            # making a recursive call; depth increases by one.
            
            if solve_backtracking(board, metrics, depth + 1):
                return True

            # back tracking at (row,col)
            metrics.backtracks += 1
            board[row][col] = 0

    return False