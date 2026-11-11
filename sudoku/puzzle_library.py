from pathlib import Path
from sudoku.board import find_empty, is_valid
from sudoku.config import parse_format

class Puzzle:
    def __init__(self):
        self.board = []
        self.solution = []
        self.difficulty = ""
        self.batch_index = -1
        self.name = ""

class PuzzleLibrary:
    def __init__(self):
        self.puzzles = []

    def load_puzzle_library(self):
        self.load_puzzles("./data/easy.txt","Easy")
        self.load_puzzles("./data/medium.txt","Medium")
        self.load_puzzles("./data/expert.txt","Expert")

    def load_puzzle(self,puzzle_string: str,solution_string: str,difficulty: str,index:int | str) -> Puzzle:
        """
        load a single puzzle, given the puzzle
        and solution representative strings from
        the .txt dataset file, as well as the
        difficulty.

        this parser expects 9 whitespace-separated rows per line
        in order to build a legitimate puzzle board/solution.
        """
        puzzle = Puzzle()
        puzzle.difficulty = difficulty
        puzzle.name = f"{difficulty}_{index}"

        if type(index) == str:
            puzzle.batch_index = int(index.split('_')[0])
        else:
            puzzle.batch_index = -1
            
        # forming puzzle
        for puzzle_row in puzzle_string.split():
            grid_row = []
            for ch_digit in puzzle_row:
                grid_row.append(int(ch_digit))
            puzzle.board.append(grid_row)

        # forming solution
        for solution_row in solution_string.split():
            grid_row = []
            for ch_digit in solution_row:
                grid_row.append(int(ch_digit))
            puzzle.solution.append(grid_row)

        return puzzle

    def load_generated_puzzles(self,filepath):
        """
        intended for use with puzzles created
        by generator.py, where each puzzle is
        represented by 3 lines instead of 2,
        the 1st line being a puzzle tag ID.
        """

        with open(filepath, encoding='utf-8') as file:
            while True:
                tag_id = file.readline()
                if tag_id == "":
                    break
                puzzle_str = file.readline()
                if puzzle_str == "":
                    raise ValueError(f"no puzzle provided for generated puzzle {tag_id}")
                solution_str = file.readline()
                if solution_str == "":
                    raise ValueError(f"no solution provided (gen puzzle {tag_id})")

                puzzle = self.load_puzzle(puzzle_str,solution_str,"Generated",tag_id)
                self.validate_loaded_puzzle(puzzle)

                self.puzzles.append(puzzle)
                
    def load_puzzles(self,filepath,difficulty):
        """
        reading two lines at a time
        to gather a puzzle and its solution.
        start with "easy.txt", then "medium.txt",
        then "hard.txt".
        """

        with open(filepath, encoding="utf-8") as file:

            puzzle_index = 1
            while True:    
                puzzle_string = file.readline()
                if puzzle_string == "":
                    break
                solution_string = file.readline()
                if solution_string == "":
                    raise ValueError(f"solution not provided for puzzle ({filepath})")

                puzzle = self.load_puzzle(puzzle_string,solution_string,difficulty,puzzle_index)
                # validating new puzzle
                self.validate_loaded_puzzle(puzzle)
                
                self.puzzles.append(puzzle)
                puzzle_index += 1
                

    def validate_loaded_puzzle(self,puzzle: Puzzle):
        """
        validates a given Puzzle, either sample or
        generated. raises an error if something
        problematic is found.
        """

        if not is_valid(puzzle.board):
            raise ValueError(f"malformed puzzle board ({puzzle.name})")
        if not is_valid(puzzle.solution) or find_empty(puzzle.solution) is not None:
            raise ValueError(f"malformed puzzle solution ({puzzle.name})")

        # checking puzzle board is consistent with the solution
        for i in range(len(puzzle.board)):
            for j in range(len(puzzle.board[0])):
                if puzzle.board[i][j] == 0:
                    continue
                if puzzle.board[i][j] != puzzle.solution[i][j]:
                    raise ValueError(f"inconsistency between board and solution ({puzzle.name})")
            
