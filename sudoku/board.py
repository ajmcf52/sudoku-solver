

def can_place(board: list[list[int]], row: int, col: int, digit: int) -> bool:
    """
    checking if a digit can be placed at a specific place on the Sudoku board.
    We assume the board, row/col coordinates, and digit are all valid.
    """

    if row < 0 or row > 8 or col < 0 or col > 8:
        return False
    if digit > 9 or digit < 1 or board[row][col] != 0:
        return False
    

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