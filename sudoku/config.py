from sudoku.solvers import solve_backtracking, solve_mrv
from typing import NamedTuple

class SpeedPreset(NamedTuple):
    name: str
    delay_ms: int
    events_per_tick: int


speed_selections = [SpeedPreset("Study", 500, 1),
                    SpeedPreset("Slow", 200, 1),
                    SpeedPreset("Normal", 50, 1),
                    SpeedPreset("Fast", 20, 1),
                    SpeedPreset("Fast-forward", 20, 10)]

solver_options = {
    "Basic Backtracking" : solve_backtracking,
    "MRV Backtracking" : solve_mrv
}
