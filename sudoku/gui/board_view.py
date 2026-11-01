from tkinter import *
import tkinter.font
from sudoku.solvers import solve

class SudokuApp:
    def __init__(self, root):
        self.root = root
        self.events = []
        self.event_index = 0
        self.canvas = Canvas(root, width=465,height=465)
        self.canvas.pack()
        draw_board(self.canvas)
        self.id_grid = draw_initial_numbers(self.canvas)
        self.setup_buttons(root)

    def handle_record(self):
        self.events = record_solution(solvable_medium)

    def start_playback(self):
        self.step()

    def setup_buttons(self, root: Tk):

        controls = Frame(root)
        controls.pack(pady=10)

        play_button = Button(controls, text="Start", command=self.start_playback)
        play_button.pack(pady=10, side=LEFT)

        record_button = Button(controls, text="Record", command=self.handle_record)
        record_button.pack(pady=10, side=LEFT, padx=10)

    def step(self):
        if self.event_index >= len(self.events):
            return
        event_i = self.events[self.event_index]
        event_type,row,col,digit = event_i
        
        if (event_type == "place"):
            self.canvas.itemconfigure(self.id_grid[row][col], text=digit)
        else:
            self.canvas.itemconfigure(self.id_grid[row][col], text="")
        self.event_index += 1
        self.root.after(20, self.step)

solvable_medium = [[2,0,0,6,0,0,0,3,0],
                      [0,7,0,0,0,4,0,0,6],
                      [0,0,0,0,1,8,4,0,0],
                      [6,0,0,1,0,0,0,0,0],
                      [0,0,9,0,3,5,0,0,0],
                      [0,0,0,0,0,0,9,5,0],
                      [0,3,0,8,0,0,7,0,0],
                      [0,0,7,0,0,6,0,4,0],
                      [0,0,1,0,0,0,0,6,8]]

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

def draw_initial_numbers(canvas: Canvas) -> list[list[int]]:
    """
    return a 9x9 grid of text IDs for each
    number that is drawn, so the text can
    be re-configured easily at a later time.
    """
    id_grid = []
    for i in range(0,9):
        id_grid.append([])
        for j in range(0,9):
            
            if solvable_medium[i][j] != 0:
                cell_text = solvable_medium[i][j]
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
    app = SudokuApp(root)
    root.mainloop()



if __name__ == "__main__":
    main()

