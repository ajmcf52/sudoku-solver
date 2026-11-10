from sudoku.board import can_place, find_empty, is_valid
from sudoku.metrics.metrics import SearchMetrics
from time import perf_counter
from collections.abc import Callable
import random

def digit_search_box(board: list[list[int]], box: int, digit: int) -> bool:
    """
    return True if digit is found in box,
    False otherwise
    """
    start_i = (box // 3) * 3
    start_j = (box % 3) * 3

    for i in range(start_i,start_i + 3):
        for j in range(start_j,start_j + 3):
            if board[i][j] == digit:
                return True
    return False

def digit_search_col(board: list[list[int]], col: int, digit: int) -> bool:
    """
    return True if digit is found in col,
    False otherwise.
    """

    for i in range(len(board)):
        if board[i][col] == digit:
            return True
    return False

def digit_search_row(board: list[list[int]], row: int, digit: int) -> bool:
    """
    return True if digit already exists in row,
    False otherwise
    """
    
    for i in range(len(board[row])):
        if board[row][i] == digit:
            return True
    return False

def get_box(i: int, j: int) -> int:
    """
    returns an int from 0-8
    indicating which box (i,j)
    is pointing to, where i and 
    j are row and column, respectively.
    """
    return (i // 3) * 3 + (j // 3)

def init_search_units(rows: dict, cols: dict, boxes: dict):
    """
    init data structures to hold counts for digits 1-9
    for rows/cols/boxes 0-8, as well as last valid coordinate.
    """
    for i in range(0,9):
        rows[i] = {}
        cols[i] = {}
        boxes[i] = {}
        for k in range(1,10):
            rows[i][k] = (0,None)
            cols[i][k] = (0,None)
            boxes[i][k] = (0,None)

def solve_hidden_single(board: list[list[int]], metrics: SearchMetrics, depth: int, on_placement: Callable[[int,int,int],None] | None = None,
                    on_removal: Callable[[int,int],None] | None = None) -> bool:
    """
    MRV solver with single hidden constraint attached.
    search each row, column and box for digits that
    have only one single legal cell in its respective
    unit of search.

    if we find a cell with no legal digits, we backtrack.
    
    similarly, finding a digit that can't be placed and 
    also isn't already present in its row/col/box also
    forces a backtrack.

    if there are no "dead ends", we look for a count==1
    for a digit in a row, column, or box. That signifies
    a hidden single. We force placement on that and recurse.

    If there are no hidden singles, proceed with MRV.
    """

    metrics.solver_calls += 1
    metrics.max_depth = max(depth, metrics.max_depth)

    rows = {}
    cols = {}
    boxes = {}
    init_search_units(rows,cols,boxes)

    for i in range(len(board)):
        for j in range(len(board[i])):
            legal_cell = False
            if board[i][j] != 0: continue
            for k in range(1,10):
                if not can_place(board,i,j,k): continue
                legal_cell = True
                rows[i][k] = (rows[i][k][0] + 1, (i,j))
                cols[j][k] = (cols[j][k][0] + 1, (i,j))
                box = get_box(i,j)
                boxes[box][k] = (boxes[box][k][0] + 1, (i,j))
            if not legal_cell:
                return False
    to_place = None

    for ik,iv in rows.items():
        for k in range(1,10):
            if rows[ik][k][0] == 0 and not digit_search_row(board,ik,k):
                return False
            if rows[ik][k][0] == 1 and to_place is None:
                to_place = (k,rows[ik][k][1])
    for ij,iv in cols.items():
        for k in range(1,10):
            if cols[ij][k][0] == 0 and not digit_search_col(board,ij,k):
                return False
            if to_place is None and cols[ij][k][0] == 1:
                to_place = (k,cols[ij][k][1])
    for bi,bv in boxes.items():
        for k in range(1,10):
            if boxes[bi][k][0] == 0 and not digit_search_box(board,bi,k):
                return False
            if to_place is None and boxes[bi][k][0] == 1:
                to_place = (k,boxes[bi][k][1])

    if to_place is not None:
        i,j = to_place[1]
        board[i][j] = to_place[0]
        metrics.placements += 1
        if on_placement is not None:
            on_placement(i,j,to_place[0])
        if solve_hidden_single(board,metrics,depth+1,on_placement,on_removal):
            return True
        board[i][j] = 0
        metrics.backtracks += 1
        if on_removal is not None:
            on_removal(i,j)
    else:
    # if we have no hidden singles, proceed with MRV.
    
        heur = find_mrv(board)
        # getting None here means we have no empty cells left.
        if heur is None:
            return True
        
        row,col,digits = heur
        for digit in digits:
            board[row][col] = digit
            metrics.placements += 1
            if on_placement is not None:
                on_placement(row,col,digit)
            if solve_hidden_single(board,metrics,depth+1,on_placement,on_removal):
                return True
            board[row][col] = 0
            metrics.backtracks += 1
            if on_removal is not None:
                on_removal(row,col)

    # if either branch gets here, we backtrack.
    return False
                    
def solve_random_mrv(board: list[list[int]], metrics: SearchMetrics, depth: int, on_placement: Callable[[int,int,int], None] | None = None,
                     on_removal: Callable[[int,int], None] | None = None) -> bool:
    """
    MRV backtracking solver that attempts to place digits in a randomized order.
    Used specifically for puzzle solution generation.
    """

    mrv_cell = find_mrv(board)
    if mrv_cell is None:
        return True

    row,col,digits = mrv_cell
    if len(digits) == 0:
        return False
    random.shuffle(digits)

    for digit in digits:
        board[row][col] = digit
        if solve_random_mrv(board,metrics,depth+1,on_placement,on_removal):
            return True
        board[row][col] = 0
    return False
    
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