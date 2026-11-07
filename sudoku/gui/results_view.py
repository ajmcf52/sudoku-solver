from tkinter.ttk import Treeview
from tkinter import Toplevel, Tk
from sudoku.metrics.benchmark import BenchmarkResult

METRICS_LABELS = ["Solver name",
                  "Puzzle name",
                  "Valid Solution",
                  "Elapsed time (sec)",
                  "Placements",
                  "Backtracks",
                  "Max depth",
                  "Solver calls"
                  ]
COL_WIDTHS = [120,
              85,
              90,
              115,
              75,
              75,
              75,
              75]

class ResultsView:
    def __init__(self, root: Tk, results: list[BenchmarkResult]):
        self.data = results
        self.row_count = len(self.data)
        self.col_count = len(METRICS_LABELS)
        self.root = root
        self.top_level = None
        self.col_labels = [label for label in METRICS_LABELS]
        self.tree = None

        self.draw_window()
        self.draw_table()

    def draw_window(self):
        """
        window drawing function.
        """

        self.top_level = Toplevel(self.root)
        self.top_level.title('Benchmark Results')

    def setup_headings(self):
        """
        insert text for each heading
        according to assigned ID.
        """
        i = 0
        for id_text in self.col_labels:
            self.tree.heading(id_text,text=id_text)
            self.tree.column(id_text,anchor='e',width=COL_WIDTHS[i])
            i += 1
    
    def draw_table(self):
        """
        drawing our data grid that
        will display everything we
        collected on our solvers.
        """

        self.tree = Treeview(self.top_level,columns=self.col_labels,
                             show='headings')
        self.tree.grid()
        self.setup_headings()

        for row in self.data:
            """
            need to parse attributes for
            every given metric label.
            """
            d = row.data
            col_values = []

            col_values.append(row.solver_name)
    
            col_values.append(d.puzzle_name)
            col_values.append(row.is_valid)
            col_values.append("{:.4f}".format(d.elapsed_sec))
            col_values.append(d.placements)
            col_values.append(d.backtracks)
            col_values.append(d.max_depth)
            col_values.append(d.solver_calls)
            self.tree.insert('','end',values=col_values)