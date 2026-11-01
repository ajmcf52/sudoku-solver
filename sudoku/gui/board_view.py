from tkinter import *
from sudoku.solvers import solve
from sudoku.puzzle_library import PuzzleLibrary, Puzzle

class SudokuApp:
    def __init__(self, root: Tk, puzzle: Puzzle):
        self.puzzle = puzzle
        self.display_board = [row[:] for row in self.puzzle.board]
        self.root = root
        self.events = []
        self.event_index = 0
        self.canvas = Canvas(root, width=465,height=465)
        self.canvas.pack()

        draw_board(self.canvas)
        self.id_grid = draw_initial_numbers(self.canvas, self.puzzle)
        self.setup_buttons(root)
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
        self.events = record_solution(self.puzzle.board)
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
    def setup_buttons(self, root: Tk):

        controls = Frame(root)
        controls.pack(pady=10)

        play_button = Button(controls, text="Start", command=self.start_playback)
        play_button.pack(pady=10, side=LEFT)

        record_button = Button(controls, text="Record", command=self.handle_record)
        record_button.pack(pady=10, side=LEFT, padx=10)

        pause_button = Button(controls, text="Pause", command=self.pause_playback)
        pause_button.pack(pady=10, side=LEFT)

        reset_button = Button(controls, text="Reset", command=self.reset_playback)
        reset_button.pack(pady=10, side=LEFT, padx=10)

    def step(self):
        if self.playback_state != "Playing":
            return
        self.step_id = None

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
        self.step_id = self.root.after(20, self.step)

# solvable_medium = [[2,0,0,6,0,0,0,3,0],
#                       [0,7,0,0,0,4,0,0,6],
#                       [0,0,0,0,1,8,4,0,0],
#                       [6,0,0,1,0,0,0,0,0],
#                       [0,0,9,0,3,5,0,0,0],
#                       [0,0,0,0,0,0,9,5,0],
#                       [0,3,0,8,0,0,7,0,0],
#                       [0,0,7,0,0,6,0,4,0],
#                       [0,0,1,0,0,0,0,6,8]]

tile_offset = (450 - 15) / 9 # px width of each tile


def record_solution(board: list[list[int]]) -> list:
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
    solve(cells, on_placement, on_removal)
    
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
    app = SudokuApp(root, puzzle_library.puzzles[0])
    root.mainloop()



if __name__ == "__main__":
    main()

