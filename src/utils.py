'''a combination of functions to be used as utilities for solving.'''

BOARD_WIDTH = 9
BOARD_HEIGHT = BOARD_WIDTH
SUBGRID_LEN = 3

THIN_HLINE = chr(9472)
THICK_HLINE = chr(9473)
THIN_VLINE = chr(9474)
THICK_VLINE = chr(9475)

CHOICE_RANGE = 9


def print_board(board: list[list[int]]):
    '''prints contents of the board in a readable format.'''

    result = ''
    for i in range(BOARD_WIDTH):
        result += ' ' + (3 * THICK_HLINE)
    result += '\n'

    for i in range(BOARD_HEIGHT):
        for j in range(BOARD_WIDTH):
            if j % SUBGRID_LEN == 0:
                result += THICK_VLINE + ' '
            else:
                result += THIN_VLINE + ' '
            result += str(board[i][j]) + ' '
        # end inner loop

        result += THICK_VLINE + '\n'
        if i % SUBGRID_LEN == 2:
            for k in range(BOARD_WIDTH):
                result += ' ' + (3 * THICK_HLINE)
        else:
            for k in range(BOARD_WIDTH):
                result += ' ' + (3 * THIN_HLINE)
        result += '\n'
    print(result)


def is_valid(board: list[list[int]], pos: tuple[int], num: int):
    '''tests whether or not a number at a given board position is valid or not.'''

    if pos[0] < 0 or pos[1] < 0 or pos[0] == len(board) or pos[1] == len(board[0]):
        return False
    for i in range(BOARD_HEIGHT):
        if board[i][pos[1]] == num and (i, pos[1]) != pos:
            return False
    for i in range(BOARD_WIDTH):
        if board[pos[0]][i] == num and (pos[0], i) != pos:
            return False

    subgrid = (pos[0] // SUBGRID_LEN, pos[1] // SUBGRID_LEN)
    for i in range(SUBGRID_LEN):
        x = subgrid[0] * SUBGRID_LEN + i
        for j in range(SUBGRID_LEN):
            y = subgrid[1] * SUBGRID_LEN + j
            if board[x][y] == num and (x, y) != pos:
                return False
    return True


def find_next_empty(board: list[list[int]]):
    '''returns the next empty location on the board.'''

    for i in range(BOARD_HEIGHT):
        for j in range(BOARD_WIDTH):
            if board[i][j] == 0:
                return (i, j)
    return (-1, -1)


def solve(board: list[list[int]]):
    '''recursive backtracking sudoku solver algorithm.'''

    pos = find_next_empty(board)

    # if next pos returned is (-1,-1) we know board is solved.
    if (pos == (-1, -1)):
        return True

    for i in range(CHOICE_RANGE):
        choice = i + 1
        if not is_valid(board, pos, choice):
            continue
        board[pos[0]][pos[1]] = choice

        # test the choice.
        is_good_choice = solve(board)
        if is_good_choice:
            return True

        # if invalid, unset choice and try the next one.
        board[pos[0]][pos[1]] = 0

    # if no choice is possible with given board config, backtrack.
    return False


def check_solution(board: list[list[int]]):
    '''
    checks whether or not a solution is correct.

    note that while the constraint for each number
    on the board is 3-fold, we only need to check
    one; if one constraint fails, naturally the 
    other two would as well.
    '''

    for i in range(BOARD_HEIGHT):
        nums = set()
        for j in range(BOARD_WIDTH):
            if board[i][j] in nums:
                return False
            nums.add(board[i][j])
        nums.clear()
    return True
