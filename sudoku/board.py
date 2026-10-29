

def can_place(board: list[list[int]], row: int, col: int, digit: int) -> bool:
    """
    checking if a digit can be placed at a specific place on the Sudoku board.
    We assume the board, row/col coordinates, and digit are all valid.
    """

    box_row = row - (row % 3)
    box_col = col - (col % 3)

    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if board[i][j] == digit:
                return False

    for i in range(len(board)):
        if board[i][col] == digit:
            return False

    for j in range(len(board)):
        if board [row][j] == digit:
            return False

    return True



def find_empty(board: list[list[int]]) -> tuple[int, int] | None:
    """
    finds and returns the first empty cell that can be found
    while searching the board, row by row.

    we assume our board is a valid 9x9 square grid.
    """

    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == 0:
                return (i, j)
    
    return None


def is_valid(board: list[list[int]]) -> bool:

    if len(board) != 9:
        return False

    # checking row by row; also ensure all values are integers.
    for i in range(len(board)):
        if len(board[i]) != 9:
            return False
        seen = set()
        for j in range(len(board[i])):
            if board[i][j] == 0:
                continue
            if type(board[i][j]) != int:
                return False
            if board[i][j] < 0 or board[i][j] > 9 or board[i][j] in seen:
                return False
            seen.add(board[i][j])


    # checking column by column
    for j in range(len(board[j])):
        seen = set()
        for i in range(len(board)):
            if board[i][j] == 0:
                continue
            if board[i][j] < 0 or board[i][j] > 9 or board[i][j] in seen:
                return False
            seen.add(board[i][j])

    # checking subgrid by subgrid
    for mult_row in range(0,3):
        start_i = mult_row * 3
        for mult_col in range(0,3):
            start_j = mult_col * 3
            seen = set()
            for i in range(start_i, start_i + 3):
                for j in range(start_j, start_j + 3):
                    if board[i][j] == 0:
                        continue
                    if board[i][j] < 0 or board[i][j] > 9 or board[i][j] in seen:
                        return False
                    seen.add(board[i][j])

    return True