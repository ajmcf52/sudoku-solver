from typing import NamedTuple
from statistics import mean, median
import datetime as dt
from sudoku.config import solver_options
from sudoku.solvers import solve
from sudoku.puzzle_library import PuzzleLibrary
from sudoku.metrics.metrics import SearchMetrics

class BenchmarkResult(NamedTuple):
    solver_name: str
    data: SearchMetrics
    is_valid: bool

def save_benchmark_data(results: list[BenchmarkResult],
                        summary_stats: dict,
                        batch_index: int,
                        rep_count: int = 1):
    """
    writes benchmark data to a file in 'data/results/',
    summary data detailed at the top of the file
    """
    timestamp = dt.datetime.now().strftime('%d%m%y_%H%M%S')
    
    file_name = f"data/results/batch_{batch_index}_{timestamp}_data.txt"
    puzzle_count = len(results) / (len(solver_options))
    with open(file_name, mode='w', encoding='utf-8') as file:

        file.write(f"# BATCH {batch_index} DATA\n")
        file.write(f"PUZZLE_COUNT={puzzle_count}\n")
        file.write(f"REP_COUNT={rep_count}\n")
        file.write("--- --- --- --- ---\n")
        file.write("# BENCHMARK SUMMARY\n")
        file.write("Elapsed solve time\t\tMean (ms)\t\tMedian (ms)\n")

        for solver_name in solver_options.keys():
            mean_time_ms = "{:.2f}".format(summary_stats[solver_name][0] * 1000)
            median_time_ms = "{:.2f}".format(summary_stats[solver_name][1] * 1000)
            file.write(f"{solver_name}\t\t{mean_time_ms}\t\t{median_time_ms}\n")

        file.write("--- --- --- --- ---\n")
        file.write("# RAW DATA\n")
        file.write("# format: [solver_id],[puzzle_id],[valid_solve?],[elapsed(ms)]," \
        "[placements],[backtracks],[max_depth],[solver_calls]\n\n")

        for result in results:
            file.write(get_raw_data_line(result))

def get_raw_data_line(result: BenchmarkResult) -> str:
    """
    returns the raw data CSV representation of
    the given BenchmarkResult.
    """
    r = result
    elapsed_ms = r.data.elapsed_sec * 1000
    return f"{r.solver_name},{r.data.puzzle_name},{r.data.valid},{elapsed_ms}," \
    f"{r.data.placements},{r.data.backtracks},{r.data.max_depth},{r.data.solver_calls}\n"

def process_summary_statistics(results: list[BenchmarkResult]) -> dict:
        """
        parse data results to get mean/median
        statistics for solving time on each solver.
        """

        summary_buckets = {}

        for solver_name, solver_fn in solver_options.items():
            summary_buckets[solver_name] = []
        for result in results:
            summary_buckets[result.solver_name].append(result.data.elapsed_sec)

        summary_stats = {}
        for solver_name, time_data in summary_buckets.items():
            summary_stats[solver_name] = (mean(time_data), median(time_data))
        return summary_stats

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