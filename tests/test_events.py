from sudoku.solvers import solve, solve_mrv

one_empty = [[2,1,4,6,9,7,8,3,5],
                [9,7,8,3,5,4,2,1,6],
                [3,6,5,2,1,8,4,9,7],
                [6,5,2,1,8,9,3,7,4],
                [1,4,9,7,3,5,6,8,2],
                [7,8,3,4,0,2,9,5,1],
                [5,3,6,8,4,1,7,2,9],
                [8,9,7,5,2,6,1,4,3],
                [4,2,1,9,7,3,5,6,8]]

solved_board = [[2,1,4,6,9,7,8,3,5],
                [9,7,8,3,5,4,2,1,6],
                [3,6,5,2,1,8,4,9,7],
                [6,5,2,1,8,9,3,7,4],
                [1,4,9,7,3,5,6,8,2],
                [7,8,3,4,6,2,9,5,1],
                [5,3,6,8,4,1,7,2,9],
                [8,9,7,5,2,6,1,4,3],
                [4,2,1,9,7,3,5,6,8]]


def test_one_empty():
    events = []
    def on_placement(row, col, digit):
        events.append((row,col,digit,"place"))
    def on_removal(row, col):
        events.append((row,col,"remove"))

    one_empty_copy = [row[:] for row in one_empty]
    solve(one_empty_copy, on_placement,on_removal)
    assert len(events) == 1
    assert events[0] == (5,4,6,"place")

def test_unsolvable():
    events = []
    def on_placement(row, col, digit):
        events.append((row,col,digit,"place"))
    def on_removal(row,col):
        events.append((row,col,"remove"))
    unsolvable_board = [row[:] for row in solved_board]
    unsolvable_board[0][0] = 1
    unsolvable_board[0][1] = 0
    unsolvable_board[0][2] = 0
    unsolvable_board[4][0] = 0
    unsolvable_board[4][1] = 0

    solve(unsolvable_board,on_placement,on_removal)

    assert len(events) == 2
    assert events[0] == (0,1,4,"place") 
    assert events[1] == (0,1,"remove")

def test_mrv_one_empty():
    events = []
    def on_placement(row,col,digit):
        events.append((row,col,digit,"place"))
    def on_removal(row,col):
        events.append((row,col,"remove"))
    one_empty_copy = [row[:] for row in one_empty]
    solve(one_empty_copy,on_placement,on_removal,solver=solve_mrv)
    assert len(events) == 1
    assert events[0] == (5,4,6,"place")

def test_mrv_unsolvable():
    events = []
    def on_placement(row,col,digit):
        events.append((row,col,digit,"place"))
    def on_removal(row,col):
        events.append((row,col,"remove"))
    unsolvable_board = [row[:] for row in solved_board]
    unsolvable_board[0][0] = 1
    unsolvable_board[0][1] = 0
    unsolvable_board[0][2] = 0
    unsolvable_board[4][0] = 0
    unsolvable_board[4][1] = 0

    solve(unsolvable_board,on_placement,on_removal,solver=solve_mrv)

    assert len(events) == 0