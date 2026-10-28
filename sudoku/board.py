

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