from sudoku.generator.generator import check_unique, generate_board
from sudoku.board import is_valid

def test_check_unique_true():
    med_board_unsolved = [[2,0,0,6,0,0,0,3,0],
                     [0,7,0,0,0,4,0,0,6],
                     [0,0,0,0,1,8,4,0,0],
                     [6,0,0,1,0,0,0,0,0],
                     [0,0,9,0,3,5,0,0,0],
                     [0,0,0,0,0,0,9,5,0],
                     [0,3,0,8,0,0,7,0,0],
                     [0,0,7,0,0,6,0,4,0],
                     [0,0,1,0,0,0,0,6,8]]
    board_copy = [row[:] for row in med_board_unsolved]
    assert check_unique(med_board_unsolved,0) == 1
    assert board_copy == med_board_unsolved

def test_check_unique_ambiguous():
    ambiguous_board = [[0,0,3,4,5,6,7,8,9],
                       [4,5,6,7,8,9,0,0,3],
                       [7,8,9,0,0,3,4,5,6],
                       [0,3,4,5,6,7,8,9,0],
                       [5,6,7,8,9,0,0,3,4],
                       [8,9,0,0,3,4,5,6,7],
                       [3,4,5,6,7,8,9,0,0],
                       [6,7,8,9,0,0,3,4,5],
                       [9,0,0,3,4,5,6,7,8]]

    board_copy = [row[:] for row in ambiguous_board]
    assert check_unique(ambiguous_board,0) >= 2
    assert board_copy == ambiguous_board

def test_generate_puzzle():
    puzzle, solution, clue_count = generate_board()
    assert check_unique(puzzle,0) == 1
    assert is_valid(solution)
    for i in range(len(puzzle)):
        for j in range(len(puzzle[i])):
            if puzzle[i][j] == 0:
                continue
            assert puzzle[i][j] == solution[i][j]