from sudoku.solvers import solve_backtracking, find_mrv, solve_mrv
from sudoku.metrics.metrics import SearchMetrics

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
                [7,8,3,4,6,2,9,5,1],
                [5,3,6,8,0,1,7,2,9],
                [8,9,7,5,2,6,1,4,3],
                [4,2,1,9,7,3,5,6,8]]

med_board_unsolved = [[2,0,0,6,0,0,0,3,0],
                     [0,7,0,0,0,4,0,0,6],
                     [0,0,0,0,1,8,4,0,0],
                     [6,0,0,1,0,0,0,0,0],
                     [0,0,9,0,3,5,0,0,0],
                     [0,0,0,0,0,0,9,5,0],
                     [0,3,0,8,0,0,7,0,0],
                     [0,0,7,0,0,6,0,4,0],
                     [0,0,1,0,0,0,0,6,8]]

def test_solved_board():

    copied_board = [row[:] for row in solved_board]

    assert solve_backtracking(copied_board, SearchMetrics(), 0) is True
    assert copied_board == solved_board


def test_solvable_med_puzzle():
    solvable_medium = [[2,0,0,6,0,0,0,3,0],
                      [0,7,0,0,0,4,0,0,6],
                      [0,0,0,0,1,8,4,0,0],
                      [6,0,0,1,0,0,0,0,0],
                      [0,0,9,0,3,5,0,0,0],
                      [0,0,0,0,0,0,9,5,0],
                      [0,3,0,8,0,0,7,0,0],
                      [0,0,7,0,0,6,0,4,0],
                      [0,0,1,0,0,0,0,6,8]]

    assert solve_backtracking(solvable_medium, SearchMetrics(), 0) is True
    assert solvable_medium == solved_board


def test_valid_unsolvable():
    
    unsolvable_board = [row[:] for row in solved_board]

    unsolvable_board[0][0] = 1
    unsolvable_board[0][1] = 0
    unsolvable_board[0][2] = 0
    unsolvable_board[4][0] = 0
    unsolvable_board[4][1] = 0

    copied_unsolvable = [row[:] for row in unsolvable_board]

    assert solve_backtracking(unsolvable_board, SearchMetrics(), 0) is False
    assert copied_unsolvable == unsolvable_board

def test_find_mrv_solved():
    result = find_mrv(solved_board)
    assert result is None

def test_find_mrv_unsolvable():
    unsolvable_board = [row[:] for row in solved_board]
    unsolvable_board[0][0] = 1
    unsolvable_board[0][1] = 0
    unsolvable_board[0][2] = 0
    unsolvable_board[4][0] = 0
    unsolvable_board[4][1] = 0

    result = find_mrv(unsolvable_board)
    assert result[2] == []

def test_find_mrv_solvable():
    result = find_mrv(med_board_unsolved)

    assert result[0] == 0 and result[1] == 5
    assert result[2] == [7,9]

def test_mrv_solved():
    board_copy = [row[:] for row in solved_board]
    assert solve_mrv(board_copy,SearchMetrics(),0) is True
    assert board_copy == solved_board

def test_mrv_one_empty():
    board_copy = [row[:] for row in one_empty]
    assert solve_mrv(board_copy,SearchMetrics(),0) is True
    assert board_copy == solved_board

def test_mrv_med_unsolved():
    board_copy = [row[:] for row in med_board_unsolved]
    assert solve_mrv(board_copy,SearchMetrics(),0) is True
    assert board_copy == solved_board

def test_mrv_unsolvable():
    unsolvable_board = [row[:] for row in solved_board]
    unsolvable_board[0][0] = 1
    unsolvable_board[0][1] = 0
    unsolvable_board[0][2] = 0
    unsolvable_board[4][0] = 0
    unsolvable_board[4][1] = 0

    unsolvable_copy = [row[:] for row in unsolvable_board]
    assert solve_mrv(unsolvable_board, SearchMetrics(), 0) is False
    assert unsolvable_board == unsolvable_copy