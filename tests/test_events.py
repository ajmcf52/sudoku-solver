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


def test_mrv_med_ONE_unsolved():
    board = [[2,0,0,0,0,0,8,0,0],
             [0,0,0,6,0,0,0,0,0],
             [0,6,9,7,3,0,0,0,0],
             [0,0,0,5,8,0,0,0,0],
             [0,0,0,1,0,0,5,0,0],
             [0,1,7,0,6,0,0,0,0],
             [0,0,5,0,0,0,0,0,6],
             [6,0,3,0,4,0,0,8,0],
             [0,4,0,2,7,0,0,3,0]]
    board_solution = [[2,3,1,4,5,9,8,6,7],
                       [7,5,4,6,2,8,3,1,9],
                         [8,6,9,7,3,1,2,5,4],
                           [3,9,2,5,8,4,6,7,1],
                             [4,8,6,1,9,7,5,2,3],
                               [5,1,7,3,6,2,4,9,8],
                                 [9,2,5,8,1,3,7,4,6],
                                   [6,7,3,9,4,5,1,8,2],
                                     [1,4,8,2,7,6,9,3,5]]
    events= []
    board_copy = [row[:] for row in board]
    def on_placement(row,col,digit):
        events.append(("place",row,col,digit))
    def on_removal(row,col):
        events.append(("remove",row,col))

    solved, metrics = solve(board,on_placement,on_removal,solver=solve_mrv)
    removal_count = 0
    for event in events:
        if event[0] == "remove":
            removal_count += 1
    assert solved and board==board_solution and metrics.backtracks == removal_count and removal_count > 0

    for event in events:
        if event[0] == "remove":
            board_copy[event[1]][event[2]] = 0
        else:
            board_copy[event[1]][event[2]] = event[3]
    
    assert board_copy==board_solution
