from sudoku.metrics import SearchMetrics
from sudoku.solvers import solve

solved_board = [[2,1,4,6,9,7,8,3,5],
                [9,7,8,3,5,4,2,1,6],
                [3,6,5,2,1,8,4,9,7],
                [6,5,2,1,8,9,3,7,4],
                [1,4,9,7,3,5,6,8,2],
                [7,8,3,4,6,2,9,5,1],
                [5,3,6,8,4,1,7,2,9],
                [8,9,7,5,2,6,1,4,3],
                [4,2,1,9,7,3,5,6,8]]

one_empty = [[2,1,4,6,9,7,8,3,5],
                [9,7,8,3,5,4,2,1,6],
                [3,6,5,2,1,8,4,9,7],
                [6,5,2,1,8,9,3,7,4],
                [1,4,9,7,3,5,6,8,2],
                [7,8,3,4,0,2,9,5,1],
                [5,3,6,8,4,1,7,2,9],
                [8,9,7,5,2,6,1,4,3],
                [4,2,1,9,7,3,5,6,8]]

def test_one_empty_cell():
    is_complete, metrics = solve(one_empty)

    assert is_complete
    assert metrics.solver_calls == 2 and metrics.backtracks == 0 \
    and metrics.max_depth == 1 and metrics.placements == 1


def test_unsolvable():
    unsolvable_board = [row[:] for row in solved_board]
    
    unsolvable_board[0][0] = 1        
    unsolvable_board[0][1] = 0
    unsolvable_board[0][2] = 0
    unsolvable_board[4][0] = 0
    unsolvable_board[4][1] = 0

    completion, metrics = solve(unsolvable_board)

    assert not completion
    assert (metrics.placements == 1 and metrics.backtracks == 1
            and metrics.max_depth == 1 and metrics.solver_calls == 2)


def test_invalid_board():

    invalid_board_cells = [[2,0,0,6,0,0,0,3,0],
                      [0,7,0,0,0,4,0,0,6],
                      [0,0,0,0,1,8,4,0,0],
                      [6,0,0,1,0,0,0,0,0],
                      [0,0,9,0,3,5,0,0,0,0],
                      [0,0,0,0,0,0,9,5,0],
                      [0,3,0,8,0,0,7,0,0],
                      [0,0,7,0,0,6,0,4,0],
                      [0,0,1,0,0,0,0,6,8]]

    completion, metrics = solve(invalid_board_cells)

    assert not completion
    assert (metrics.solver_calls == 0 and metrics.max_depth == 0 
            and metrics.backtracks == 0 and metrics.placements == 0)


def test_already_solved():

    completion, metrics = solve(solved_board)

    assert completion
    assert (metrics.solver_calls == 1 and metrics.max_depth == 0 
            and metrics.backtracks == 0 and metrics.placements == 0)