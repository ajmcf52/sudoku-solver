from sudoku.solvers import solve_backtracking, solve_mrv, solve_hidden_single
from typing import NamedTuple

class SpeedPreset(NamedTuple):
    name: str
    delay_ms: int
    events_per_tick: int

# intended for use by solver visual playback
# args -- [speed_label, tick_delay, events_per_tick]
speed_selections = [SpeedPreset("Study", 500, 1),
                    SpeedPreset("Slow", 200, 1),
                    SpeedPreset("Normal", 50, 1),
                    SpeedPreset("Fast", 20, 1),
                    SpeedPreset("Fast-forward", 20, 10)]

"""
in the .txt /data files that hold puzzles,
generated puzzles are 3 lines each
[puzzle tag, puzzle, solution],
whereas banked hand-supplied puzzles are
only two lines [puzzle, solution].
"""
parse_format = ['TWO_LINE', 
                'THREE_LINE']

# Our three solver options
solver_options = {
    "Basic Backtracking" : solve_backtracking,
    "MRV Backtracking" : solve_mrv,
    "'Hidden Single' MRV": solve_hidden_single
}
