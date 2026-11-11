from tkinter import *
from tkinter import ttk, messagebox, Toplevel, Scrollbar, Listbox
from pathlib import Path
import queue
import threading
import time
from sudoku.metrics.metrics import SearchMetrics
from sudoku.solvers import solve, solve_mrv, solve_backtracking, solve_hidden_single
from sudoku.puzzle_library import PuzzleLibrary, Puzzle
from sudoku.metrics.benchmark import run_benchmark, process_summary_statistics, save_benchmark_data
from sudoku.config import speed_selections, solver_options
from sudoku.gui.results_view import ResultsView

class SudokuApp:
    def __init__(self, root: Tk, puzzle: Puzzle, samples: PuzzleLibrary, generated: PuzzleLibrary):
        self.playback_speed_index = 0
        self.playback_speed = speed_selections[self.playback_speed_index]
        self.samples_library = samples
        self.generated_library = generated
        self.benchmark_queue = queue.Queue()
        self.puzzle = puzzle
        self.display_board = [row[:] for row in self.puzzle.board]
        self.root = root
        self.events = []
        self.event_index = 0
        self.solver = solve_backtracking
        self.solver_name = "Basic Backtracking"
        self.metrics = None
        self.valid_metrics = True
        self.setup_dropdowns()

        self.canvas = Canvas(self.root, width=465,height=465)
        self.canvas.pack()

        draw_board(self.canvas)
        self.id_grid = draw_initial_numbers(self.canvas, self.puzzle)
        self.setup_buttons()
        self.playback_state = "Unrecorded"
        self.step_id = None

    def display_benchmark_stats(self):
        """
        called to display benchmark data
        once it has been collected.
        """

        try:
            payload = self.benchmark_queue.get_nowait()
        except queue.Empty:
            self.root.after(1000, self.display_benchmark_stats)
            return

        self.benchmark_button.config(state='normal')
        if payload[0] == 'error':
            print(payload[1])
            return

        msg, results, summary_stats = payload
        print(msg)

        print(f"REP COUNT={self.rep_count}")
        
        for r in results:
            display_metrics(r.solver_name, r.data, r.is_valid)
                
        # open a new ResultsView and pass in the data.
        results_view = ResultsView(self.root,results,summary_stats)
                
        save_data = messagebox.askyesno(title="Save Benchmark",
                                        message="Save benchmark data (data/results/)")
        if save_data:
            save_benchmark_data(results, summary_stats, 
                                self.generated_library.puzzles[0].batch_index,
                                self.rep_count)

    def perform_benchmark(self):
        """
        once a batch has been
        selected and loaded,
        this function is called
        to initialize the benchmark.
        """
        try:
            reps_text = self.benchmark_reps.get()
            if reps_text != "":
                self.rep_count = max(int(reps_text),1)
            else:
                self.rep_count = 1

            results = run_benchmark(self.generated_library,self.rep_count)
            summary_stats = process_summary_statistics(results)

            self.benchmark_queue.put(("success", results, summary_stats))
        except Exception as error:
            self.benchmark_queue.put(("error", error))

    def display_metrics(self):
        """
        prints recorded metrics of a given
        solver to the console once playback
        has finished.

        calls another function with 'self' attributes.
        """

        display_metrics(self.solver_name,self.metrics,self.valid_metrics)


    def check_display_solution(self) -> bool:
        """
        compare self.display_board with
        self.puzzle.solution and return
        whether it was properly solved.
        """
        
        for i in range(len(self.display_board)):
            for j in range(len(self.display_board[i])):
                if self.display_board[i][j] != self.puzzle.solution[i][j]:
                    return False
        return True

    def load_configuration(self):
        """
        loads a selected puzzle and solver
        into the FOV, restarting the app's
        solver logic and UI while doing so.
        """

        puzzle_index = self.puzzle_dropdown.current()
        if puzzle_index != -1:
            self.puzzle = self.samples_library.puzzles[puzzle_index]
        solver_index = self.solver_dropdown.current()
        if solver_index != -1:
            self.solver_name = self.solver_dropdown.get()
            self.solver = solver_options[self.solver_name]

        if self.step_id is not None:
            self.root.after_cancel(self.step_id)
            self.step_id = None
        self.event_index = 0
        self.events.clear()

        self.playback_state = "Unrecorded"
        self.display_board = [row[:] for row in self.puzzle.board]
        self.reset_display_numbers()

    def toggle_speed_change(self):
        """
        button handler for changing
        playback speed.
        """

        self.playback_speed_index = (self.playback_speed_index + 1) % len(speed_selections)
        self.playback_speed = speed_selections[self.playback_speed_index]
        self.speed_button.configure(text=f"Speed: {self.playback_speed.name}")
    
    def reset_playback(self):
        """
        reset playback of the 
        sudoku solver--actual
        events are kept the same,
        we are just playing them
        over again.
        """

        if self.playback_state not in ("Playing", "Paused", "Finished"):
            return
        
        if self.step_id is not None:
            self.root.after_cancel(self.step_id)
            self.step_id = None

        self.event_index = 0
        self.display_board = [row[:] for row in self.puzzle.board]
        self.reset_display_numbers()
        self.playback_state = "Ready"

    def reset_display_numbers(self):
        """
        return grid back to initial puzzle state.
        different from initializing the board state,
        as the cells have already been assigned item
        IDs.
        """
        
        for i in range(len(self.display_board)):
            for j in range(len(self.display_board[i])):
                if self.display_board[i][j] == 0:
                    cell_text = ""
                else:
                    cell_text = self.display_board[i][j]
                self.canvas.itemconfigure(self.id_grid[i][j], text=cell_text)

    def cancel_batch_selection(self):
        """
        action handler for 'Cancel' in the
        batch loading window, which backs
        out of a batch loading process,
        and also the benchmark.
        """

        self.batch_select.destroy()
        self.generated_library = None

    def start_load_batch_selection(self):
        """
        threaded function that performs batch loading
        and benchmarking on a separate thread to
        keep the main UI responsive during the 
        process.
        """
        self.benchmark_button.config(state="disabled")

        #TODO optional.. create a label that displays benchmark status while it's running.

        worker = threading.Thread(target=self.load_selected_batch, daemon=True)
        worker.start()
        self.root.after(1000,self.display_benchmark_stats)

    def load_selected_batch(self):
        """
        button action handler that
        upon being activated, retrieves
        the selected batch and loads it
        into the app puzzle library to
        be benchmarked.
        """
        selected_tag = self.batch_list.curselection()[0]
        selected_batch = self.batch_lookup[selected_tag]

        print("loading batch: ", selected_batch)

        self.generated_library.load_generated_puzzles(selected_batch)

        # once batch is loaded, initialize benchmark
        self.perform_benchmark()

    def handle_benchmark_batch_select(self):
        """
        creates a window that allows the user
        to select their puzzle batch for the
        upcoming benchmark.
        """

        batch_puzzle_counts = {}
        batch_names = {}
        gen_folder = Path("./data/generated")
        batch_files = gen_folder.glob("gen_batch_*.txt")
        self.batch_lookup = {}

        for batch in batch_files:
            # get batch name + index from filepath
            batch_name = batch.stem
            batch_name_args = batch_name.split('_')
            index = int(batch_name_args[len(batch_name_args) - 1])

            self.batch_lookup[index] = batch
            batch_names[index] = batch
            puzzle_count = 0
            with open(batch, mode='r', encoding='utf-8') as file:

                for line in file.readlines():
                    for ch in line:
                        if ch == '_':
                            puzzle_count += 1
                            break
                        elif ch == ' ':
                            break
                batch_puzzle_counts[index] = puzzle_count

        self.batch_select = Toplevel(self.root)
        self.batch_select.title('Select Benchmark Puzzle Batch')
        self.batch_select.protocol("WM_DELETE_WINDOW",self.cancel_batch_selection)

        self.batch_list = Listbox(self.batch_select, selectmode='single')
        self.batch_list.pack(side=LEFT,fill=BOTH)

        scrollbar = Scrollbar(self.batch_select)
        scrollbar.pack(side=RIGHT,fill=BOTH)

        for index, name in batch_names.items():
            tag = f"{name.stem} -- {batch_puzzle_counts[index]} puzzles"
            self.batch_list.insert(END, tag)

        for key,value in self.batch_lookup.items():
            print("batch info: ", key, value)

        self.batch_list.select_set(0)

        self.batch_list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.batch_list.yview)

        button_panel = Frame(self.batch_select)
        button_panel.pack(anchor='s')

        ok_button = Button(button_panel, text='OK', command=self.start_load_batch_selection)
        ok_button.pack(side=RIGHT,padx=10,pady=10)

        cancel_button = Button(button_panel, text='Cancel', command=self.cancel_batch_selection)
        cancel_button.pack(side=RIGHT,padx=10,pady=10)

    def handle_record(self):
        """
        handles "Record" button presses,
        passing the action along to a
        function that returns the playback
        events.
        """

        if self.playback_state != "Unrecorded":
            return
        self.events = self.record_solution()
        self.playback_state = "Ready"

    def start_playback(self):
        """
        start/resume work of the solver
        working (playback)
        """

        if self.playback_state != "Ready" and self.playback_state != "Paused":
            return
        self.playback_state = "Playing"
        self.step()

    def pause_playback(self):
        """
        pauses visualization of the 
        solver working (playback).
        """

        if self.playback_state != "Playing":
            return
        
        self.playback_state = "Paused"
        if self.step_id is not None:
            self.root.after_cancel(self.step_id)
            self.step_id = None

    def setup_dropdowns(self):
        """
        dropdown menu setup.
        controls for puzzle 
        and solver selection.
        """

        dropdowns = Frame(self.root)
        dropdowns.pack(pady=10)

        puzzle_names = []
        easy_count = 0
        medium_count = 0
        hard_count = 0

        for puzzle in self.samples_library.puzzles:
            if puzzle.difficulty == "Easy":
                easy_count += 1
                puzzle_names.append(puzzle.difficulty + " " +  str(easy_count))
            elif puzzle.difficulty == "Medium":
                medium_count += 1
                puzzle_names.append(puzzle.difficulty + " " + str(medium_count))
            else:
                hard_count += 1
                puzzle_names.append(puzzle.difficulty + " " + str(hard_count))

        self.puzzle_dropdown = ttk.Combobox(dropdowns, state="readonly", values=puzzle_names)
        self.puzzle_dropdown.pack(pady=10, side=LEFT)
        self.puzzle_dropdown.current(0) # set puzzle dropdown to match current selection

        self.solver_dropdown = ttk.Combobox(dropdowns, state="readonly", values=list(solver_options))
        self.solver_dropdown.pack(pady=10,padx=10,side=LEFT)
        self.solver_dropdown.current(0)

    def setup_buttons(self):
        """
        control interface setup.
        """

        controls = Frame(self.root)
        controls.pack(pady=10)

        play_button = Button(controls, text="Start", command=self.start_playback)
        play_button.pack(pady=10, side=LEFT)

        record_button = Button(controls, text="Record", command=self.handle_record)
        record_button.pack(pady=10, side=LEFT, padx=10)

        pause_button = Button(controls, text="Pause", command=self.pause_playback)
        pause_button.pack(pady=10, side=LEFT)

        reset_button = Button(controls, text="Reset", command=self.reset_playback)
        reset_button.pack(pady=10, side=LEFT, padx=10)

        self.speed_button = Button(controls, text=f"Speed: {self.playback_speed.name}", command=self.toggle_speed_change)
        self.speed_button.pack(pady=10, side=LEFT)

        load_button = Button(controls, text="Load", command=self.load_configuration)
        load_button.pack(padx=10, pady=10, side=LEFT)

        benchmark_controls = Frame(controls)
        benchmark_controls.pack(pady=10)

        reg = benchmark_controls.register(validate_positive_int)

        self.benchmark_button = Button(benchmark_controls, text="Benchmark", 
                                  command=self.handle_benchmark_batch_select)
        self.benchmark_button.pack(pady=10,side=LEFT)

        self.benchmark_reps = Entry(benchmark_controls,validate="key",validatecommand=(reg,"%P"))
        self.benchmark_reps.pack(pady=10,side=LEFT)

    def step(self):
        self.step_id = None

        for i in range(self.playback_speed.events_per_tick):

            if self.playback_state != "Playing":
                return

            if self.event_index >= len(self.events):
                # all events processed; check solution.
                solved = self.check_display_solution()
                if solved:
                    print("puzzle solved correctly")
                    self.valid_metrics = True
                else:
                    print("puzzle does not match solution")
                    self.valid_metrics = False
                
                self.display_metrics()
                self.playback_state = "Finished"
                return
            
            event_i = self.events[self.event_index]
            event_type,row,col,digit = event_i
        
            if (event_type == "place"):
                self.canvas.itemconfigure(self.id_grid[row][col], text=digit)
                self.display_board[row][col] = digit
            else:
                self.canvas.itemconfigure(self.id_grid[row][col], text="")
                self.display_board[row][col] = 0
            self.event_index += 1
        # end for-loop

        self.step_id = self.root.after(self.playback_speed.delay_ms, self.step)

    def record_solution(self) -> list:
        """
        runs the actual solver algorithm. This will be
        solved at full-speed, whereas the playback will
        show solver events at 4-5 events/second.
        """

        cells = [row[:] for row in self.puzzle.board]
        events = []
        def on_placement(row, col, digit):
            events.append(("place",row,col,digit))
        def on_removal(row,col):
            events.append(("remove",row,col,0))
        solved, metrics = solve(cells, on_placement, on_removal,self.solver)

        metrics.puzzle_name = self.puzzle.name
        self.metrics = metrics
        
        return events

def display_metrics(solver_name: str, metrics: SearchMetrics, valid_metrics:bool):
        """
        prints recorded metrics of a given
        solver to the console once playback
        has finished.
        """

        metrics_msg = f"\t{solver_name}\n"
        metrics_msg += f"puzzle name: \t{metrics.puzzle_name}\n"

        if not valid_metrics:
            metrics_msg += f"\tInvalid metrics object. Solver failed.\n"
        else:
            metrics_msg += f"time (s): \t{metrics.elapsed_sec}\n"
            metrics_msg += f"solver calls: \t{metrics.solver_calls}\n"
            metrics_msg += f"placements: \t{metrics.placements}\n"
            metrics_msg += f"backtracks: \t{metrics.backtracks}\n"
            metrics_msg += f"max_depth: \t{metrics.max_depth}\n"

        print(metrics_msg)

def validate_positive_int(char:str) -> bool:
    """
    validation function for text input
    into the reps text field
    """
    if (char.isdigit() and int(char) > 0) or char == "":
        return True
    else:
        return False

tile_offset = (450 - 15) / 9 # px width of each tile

def draw_initial_numbers(canvas: Canvas, puzzle: Puzzle) -> list[list[int]]:
    """
    return a 9x9 grid of text IDs for each
    number that is drawn, so the text can
    be re-configured easily at a later time.
    """
    id_grid = []
    for i in range(0,9):
        id_grid.append([])
        for j in range(0,9):
            
            if puzzle.board[i][j] != 0:
                cell_text = puzzle.board[i][j]
            else:
                cell_text = ""
            text_id = canvas.create_text(15 + (j + 0.5) * tile_offset, 15 + (i + 0.5) * tile_offset,
                                text=cell_text, font=("Helvetica", 24))
            id_grid[i].append(text_id)
            
    return id_grid

def draw_board(canvas: Canvas):
    """
    GUI drawing geometry of the sudoku board,
    just the grid.
    """

    canvas.create_rectangle(15, 15, 450,450,width=3)

    for i in range(1,9):
        if i == 3 or i == 6:
            line_width = 3
        else:
            line_width = 1
        canvas.create_line(15 + tile_offset * i, 15, 15 + tile_offset * i, 450, width=line_width)

    for i in range(1,9):
        if i == 3 or i == 6:
            line_width = 3
        else:
            line_width = 1
        canvas.create_line(15, 15 + tile_offset * i, 450, 15 + tile_offset * i, width=line_width)

def main():

    root = Tk()
    root.title("Sudoku Solver")
    samples_library = PuzzleLibrary()
    samples_library.load_puzzle_library()
    generated_library = PuzzleLibrary()
    generated_library.load_generated_puzzles("./data/generated/gen_batch_1.txt")
    app = SudokuApp(root, samples_library.puzzles[0],samples_library,generated_library)
    root.mainloop()



if __name__ == "__main__":
    main()

