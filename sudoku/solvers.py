from sudoku.board import can_place, find_empty, is_valid
from sudoku.metrics import SearchMetrics
from time import perf_counter
from collections.abc import Callable

def solve_mrv(board: list[list[int]], metrics: SearchMetrics, depth: int, on_placement: Callable[[int,int,int], None] | None = None,
              on_removal: Callable[[int,int], None] | None = None) -> bool:
    """
    backtracking DFS with 
    Minimum Remaining Values (MRV)
    heuristic.
    """

    metrics.solver_calls += 1
    metrics.max_depth = max(metrics.max_depth, depth)

    # find next cell to investigate
    mrv_cell = find_mrv(board)
    if mrv_cell is None:
        return True

    row, col, digits = mrv_cell
    # if candidate list is empty, board state is dead end.
    if len(digits) == 0:
        return False
    
    for digit in digits:
        # already called can_place in find_mrv.
        board[row][col] = digit
        metrics.placements += 1
        if on_placement is not None:
            on_placement(row,col,digit)
        if solve_mrv(board,metrics,depth + 1,on_placement,on_removal):
            return True

        # if the path we chose isn't correct, backtrack.
        board[row][col] = 0
        metrics.backtracks += 1
        if on_removal is not None:
            on_removal(row,col)

    return False

def solve_backtracking(board: list[list[int]], metrics: SearchMetrics, depth: int, on_placement: Callable[[int,int,int],None] | None = None,
                        on_removal: Callable[[int,int], None] | None = None) -> bool:
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
            if on_placement is not None:
                on_placement(row,col,i)

            # making a recursive call; depth increases by one.
            
            if solve_backtracking(board, metrics, depth + 1, on_placement, on_removal):
                return True

            # back tracking at (row,col)
            board[row][col] = 0
            metrics.backtracks += 1
            if on_removal is not None:
                on_removal(row,col)

    return False

def solve(board: list[list[int]], 
          on_placement: Callable[[int,int,int],None] | None = None, 
          on_removal: Callable[[int,int],None] | None = None,
          solver: Callable = solve_backtracking) -> tuple[bool,SearchMetrics]:
    
    metrics = SearchMetrics()
    if not is_valid(board):
        return (False,metrics)

    start = perf_counter()
    finished = solver(board, metrics, 0, on_placement, on_removal)
    elapsed = perf_counter() - start
    metrics.elapsed_sec = elapsed

    return (finished,metrics)

def find_mrv(board: list[list[int]]) -> tuple[int, int, list[int]] | None:
    """
    find and return the (row, column)
    denoting the cells with the minimum
    # of replaceable values for it that
    are legal.
    heuristic for speeding up the sudoku
    solver.
    returns None if board is solved.
    """

    best = 10
    result = None
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] != 0:
                continue

            # found an empty cell.
            # check valid digits.
            candidates = []
            for k in range(1,10):
                if can_place(board,i,j,k):
                    candidates.append(k)

            # if we can't append any digits,
            # this indicates a dead end board.
            if len(candidates) == 0:
                return (i,j,[])
            # otherwise, if it tops the best
            # so far, save the result
            if len(candidates) < best:
                best = len(candidates)
                result = (i,j,candidates)
    return result