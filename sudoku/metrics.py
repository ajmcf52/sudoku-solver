
class SearchMetrics:
    def __init__(self):
        """
        constructor for SearchMetrics object.
        all attributes are counters that are 
        tallied while an algorithm is solving 
        a given puzzle.

        """
        self.placements = 0
        self.solver_calls = 0
        self.backtracks = 0
        self.max_depth = 0