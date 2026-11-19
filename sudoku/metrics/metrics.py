
class SearchMetrics:
    def __init__(self, puzzle_name:str = "", elapsed_sec:float = 0.0,
                 placements:int = 0, backtracks:int = 0, max_depth:int = 0,
                 solver_calls:int = 0):
        """
        constructor for SearchMetrics object.
        all attributes are counters that are 
        tallied while an algorithm is solving 
        a given puzzle.

        """
        self.placements = placements # valid placement of a number in a cell
        self.solver_calls = solver_calls # recursive function calls + 1
        self.backtracks = backtracks # number of times the function removes a placement
        self.max_depth = max_depth # recursive call depth
        self.elapsed_sec = elapsed_sec # time
        self.puzzle_name = puzzle_name