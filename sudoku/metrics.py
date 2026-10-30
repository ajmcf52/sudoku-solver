
class SearchMetrics:
    def __init__(self):
        """
        constructor for SearchMetrics object.
        all attributes are counters that are 
        tallied while an algorithm is solving 
        a given puzzle.

        """
        self.placements = 0 # valid placement of a number in a cell
        self.solver_calls = 0 # recursive function calls + 1
        self.backtracks = 0 # number of times the function removes a placement
        self.max_depth = 0 # recursive call depth
        self.elapsed_sec = 0.0 # time