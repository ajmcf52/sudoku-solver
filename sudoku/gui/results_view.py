from tkinter.ttk import Treeview
from tkinter import Toplevel, Tk, Frame, Label
from sudoku.metrics.benchmark import BenchmarkResult
from sudoku.config import solver_options

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
              120,
              90,
              115,
              75,
              75,
              75,
              75]

class ResultsView:
    def __init__(self, root: Tk, results: list[BenchmarkResult], summary_stats: dict):
        self.data = results
        self.summary_stats = summary_stats
        self.row_count = len(self.data)
        self.col_count = len(METRICS_LABELS)
        self.root = root
        self.top_level = None
        self.col_labels = [label for label in METRICS_LABELS]
        self.tree = None

        self.draw_window()
        self.draw_table()
        self.draw_benchmark_summary()

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
        self.tree.pack()
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

    def draw_benchmark_summary(self):
        """
        displays a data summary of
        average and median runtimes
        between solvers.
        """
        self.summary_panel = Frame(self.top_level)
        self.summary_panel.pack(pady=15,anchor='s')

        average_title_label = Label(self.summary_panel,text='Average (ms)')
        average_title_label.grid(column=0,row=1,padx=15,pady=10)
        median_title_label = Label(self.summary_panel,text='Median (ms)')
        median_title_label.grid(column=0,row=2,padx=15,pady=10)

        solver_index = 1
        for solver_name, solver_fn in solver_options.items():
            solver_name_label = Label(self.summary_panel, text=solver_name)
            solver_name_label.grid(column=solver_index,row=0,padx=10,pady=10)

            """
            format elapsed mean/median solve time (s) to ms + 2 decimals
            """
            ss = self.summary_stats
            average_stat_text = "{:.2f}".format(ss[solver_name][0] * 1000)
            average_stat_label = Label(self.summary_panel,text=average_stat_text)
            average_stat_label.grid(row=1,column=solver_index,padx=10,pady=10)

            median_stat_text = "{:.2f}".format(ss[solver_name][1] * 1000)
            median_stat_label = Label(self.summary_panel,text=median_stat_text)
            median_stat_label.grid(row=2,column=solver_index,padx=10,pady=10)
            
            solver_index += 1
        