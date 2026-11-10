from sudoku.solvers import solve, solve_random_mrv
from sudoku.board import can_place,find_empty
import random
from pathlib import Path
import argparse

def check_unique(board:list[list[int]], solutions: int) -> int:
    """
    backtracking solver that tracks possible
    solutions as it goes. If it arrives at
    a solution, unwinds to exhaust all other
    possibilities in search of another.
    """

    next_empty = find_empty(board)
    if next_empty is None:
        solutions += 1
        return solutions

    row,col = next_empty

    for i in range(1,10):
        if can_place(board,row,col,i):

            board[row][col] = i
            solutions = check_unique(board,solutions)
            board[row][col] = 0

            if solutions == 2:
                return solutions

    return solutions

def generate_board() -> tuple[list[list[int]], list[list[int]], int]:
    """
    method for generating a new puzzle board
    """
    
    board = [[0] * 9 for _ in range(9)]
    solved, metrics = solve(board,solver=solve_random_mrv)
    if not solved:
        raise ValueError("Unable to solve board during puzzle generation")
    
    solution = [row[:] for row in board]

    positions = []
    for i in range(0,9):
        for j in range(0,9):
            positions.append((i,j))

    random.shuffle(positions)

    for pos in positions:
        digit = board[pos[0]][pos[1]]
        board[pos[0]][pos[1]] = 0
        solutions = check_unique(board, 0)
        if solutions >= 2:
            board[pos[0]][pos[1]] = digit

    clue_count = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] != 0:
                clue_count += 1

    return (board, solution, clue_count)

def get_board_str(board: list[list[int]]) -> str:
    """
    returns a one-line str
    representation of a sudoku board.

    9 digits represents a row, where
    rows are separated by a single space.
    """

    result = ""
    for i in range(len(board)):
        for j in range(len(board[i])):
            result += str(board[i][j])
        result += " "
    return result

def generate_puzzle_batch(batch_size: int):
    """
    generates a new batch of puzzles,
    saving them to a .txt file in
    /generated.
    """

    # determine our filename
    generated_folder = Path("./data/generated")
    matches = generated_folder.glob("gen_batch_*.txt")
    highest_index = -1
    for match in matches:
        print(match, match.stem)
        components = str(match.stem).split("_")
        highest_index = max(highest_index,int(components[len(components) - 1]))

    file_path = f"./data/generated/gen_batch_{highest_index + 1}.txt"
    with open(file_path, mode='w', encoding='utf-8') as file:

        i = 0
        while i < batch_size:
            board, solution, clue_count = generate_board()
            puzzle_tag = f'{highest_index + 1}_{i}_cc{clue_count}_sudoku'
            file.write(puzzle_tag + '\n')
            board_str = get_board_str(board)
            solution_str = get_board_str(solution)
            file.write(board_str + '\n')
            file.write(solution_str + '\n')
            i += 1

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("batch_size", type=int,
                        help="number of desired puzzles within generated batch")
    
    args = parser.parse_args()
    generate_puzzle_batch(args.batch_size)

    
if __name__ == "__main__":
    main()