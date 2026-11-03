from tkinter import *
from tkinter import ttk
from sudoku.solvers import solve, solve_mrv, solve_backtracking
from sudoku.puzzle_library import PuzzleLibrary, Puzzle
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


class SudokuApp:
    def __init__(self, root: Tk, puzzle: Puzzle, library: PuzzleLibrary):
        self.playback_speed_index = 0
        self.playback_speed = speed_selections[self.playback_speed_index]
        self.puzzle_library = library
        self.puzzle = puzzle
        self.display_board = [row[:] for row in self.puzzle.board]
        self.root = root
        self.events = []
        self.event_index = 0
        self.solver = solve_backtracking

        self.setup_dropdowns()

        self.canvas = Canvas(self.root, width=465,height=465)
        self.canvas.pack()

        draw_board(self.canvas)
        self.id_grid = draw_initial_numbers(self.canvas, self.puzzle)
        self.setup_buttons()
        self.playback_state = "Unrecorded"
        self.step_id = None

    def check_solution(self) -> bool:
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
            self.puzzle = self.puzzle_library.puzzles[puzzle_index]
        solver_index = self.solver_dropdown.current()
        if solver_index != -1:
            self.solver = solver_options[self.solver_dropdown.get()]

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

    def handle_record(self):
        if self.playback_state != "Unrecorded":
            return
        self.events = record_solution(self.puzzle.board,self.solver)
        self.playback_state = "Ready"

    def start_playback(self):
        if self.playback_state != "Ready" and self.playback_state != "Paused":
            return
        self.playback_state = "Playing"
        self.step()

    def pause_playback(self):
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

        for puzzle in self.puzzle_library.puzzles:
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

    def step(self):
        self.step_id = None

        for i in range(self.playback_speed.events_per_tick):

            if self.playback_state != "Playing":
                return

            if self.event_index >= len(self.events):
                # all events processed; check solution.
                solved = self.check_solution()
                if solved:
                    print("puzzle solved correctly")
                else:
                    print("puzzle does not match solution")
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

tile_offset = (450 - 15) / 9 # px width of each tile


def record_solution(board: list[list[int]],solver=solve_backtracking) -> list:
    """
    runs the actual solver algorithm. This will be
    solved at full-speed, whereas the playback will
    show solver events at 4-5 events/second.
    """

    cells = [row[:] for row in board]
    events = []
    def on_placement(row, col, digit):
        events.append(("place",row,col,digit))
    def on_removal(row,col):
        events.append(("remove",row,col,0))
    solve(cells, on_placement, on_removal,solver)
    
    return events

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
    puzzle_library = PuzzleLibrary()
    puzzle_library.load_puzzle_library()
    app = SudokuApp(root, puzzle_library.puzzles[0],puzzle_library)
    root.mainloop()



if __name__ == "__main__":
    main()

