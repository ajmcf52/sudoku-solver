from sudoku.config import solver_options
from sudoku.solvers import solve
from sudoku.puzzle_library import PuzzleLibrary
from sudoku.metrics.metrics import SearchMetrics
from typing import NamedTuple
from statistics import median

class BenchmarkResult(NamedTuple):
    solver_name: str
    data: SearchMetrics
    is_valid: bool

def verify_benchmark_single(board: list[list[int]], solution: list[list[int]]) -> bool:
    """
    validates a given board against its solution.
    returns true if they match, false otherwise.
    """

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] != solution[i][j]:
                return False
    return True


def run_benchmark(puzzle_library: PuzzleLibrary, rep_count:int = 1) -> list[BenchmarkResult]:
        """
        compares runtime stats
        of all solvers.

        At this early stage, we are
        hardcoding which solvers that
        are being used. A more persistent
        version will support UI config
        for selecting solvers to compare.
        """
        results = []
        for puzzle in puzzle_library.puzzles:

            for solver_name, solver in solver_options.items():
                """
                metric counts should be deterministic;
                so for reps, we only track alotted time.
                """
                reps = 0
                times = []
                valid_metrics = True
                while True:
                    board_copy = [row[:] for row in puzzle.board]
                    solved, metrics = solve(board_copy,None,None,solver)

                    # verify each solution; display metrics before final break.
                    if not solved or not verify_benchmark_single(board_copy, puzzle.solution):
                        print(f"\nsolver {solver_name} failed for {puzzle.name} on Rep {reps}.")
                        valid_metrics = False
                    times.append(metrics.elapsed_sec)
                    reps += 1
                    if reps == rep_count:
                        metrics.puzzle_name = puzzle.name
                        metrics.elapsed_sec = median(times)
                        results.append(BenchmarkResult(solver_name,metrics,valid_metrics))
                        break
        return results