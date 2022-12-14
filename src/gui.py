import time
from copy import deepcopy
import pygame
import src.utils as utils

pygame.init()
pygame.font.init()

TILE_COUNT = 9
TILE_WIDTH = 70
TILE_HEIGHT = TILE_WIDTH
BOARD_WIDTH = TILE_COUNT * TILE_WIDTH
BOARD_HEIGHT = BOARD_WIDTH
WINDOW_WIDTH = BOARD_WIDTH
WINDOW_HEIGHT = BOARD_HEIGHT + 50
SUBMITTED_FONT_SIZE = 40
TEMP_FONT_SIZE = 25
SUBMITTED_FONT = pygame.font.SysFont('avenir', SUBMITTED_FONT_SIZE)
TEMP_FONT = pygame.font.SysFont('avenir', TEMP_FONT_SIZE)

COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_GREY = (133, 136, 140)
COLOR_WHITE = (255, 255, 255)

MAIN_LINE_COLOR = (159, 162, 166)
SELECT_OPEN_COLOR = (247, 255, 105)
SELECT_CLOSED_COLOR = (200, 204, 201)
TEMP_NUM_COLOR = (115, 115, 111)

STANDARD_THICKNESS = 1
SUBGRID_THICKNESS = 2
SELECT_THICKNESS = 4

SOLVE_SPEED_DELAY_DICT = {
    1: 100,
    2: 50,
    3: 10
}
solver_speed = None

BOARD_FILENAME = 'board.txt'

KEY_DICT = {
    pygame.K_1: 1,
    pygame.K_2: 2,
    pygame.K_3: 3,
    pygame.K_4: 4,
    pygame.K_5: 5,
    pygame.K_6: 6,
    pygame.K_7: 7,
    pygame.K_8: 8,
    pygame.K_9: 9
}


class Board:
    '''a graphical sudoku board.'''

    def __init__(self, win: pygame.Surface, board_data: list[list[int]]):

        self.window = win
        self.board = board_data

        self.tiles = [[Tile(self.board[i][j], j * TILE_WIDTH, i *
                            TILE_HEIGHT) for j in range(TILE_COUNT)] for i in range(TILE_COUNT)]
        self.selected_tile = None

        # pre-solve board so we can easily check attempted placements.
        self.solution = deepcopy(self.board)
        utils.solve(self.solution)

    def update_board(self):
        '''updates board from tile data.'''

        self.board = [[self.tiles[i][j].number for j in range(
            TILE_COUNT)] for i in range(TILE_COUNT)]

    def draw(self):
        '''draws the sudoku game board.'''

        spacing = BOARD_WIDTH / TILE_COUNT
        # draw horizontal and vertical lines first.
        for i in range(TILE_COUNT + 1):
            line_thickness = None
            line_color = None
            if i % 3 == 0:
                line_thickness = SUBGRID_THICKNESS
                line_color = COLOR_BLACK
            else:
                line_thickness = STANDARD_THICKNESS
                line_color = MAIN_LINE_COLOR

            pygame.draw.line(self.window, line_color, (i * spacing, 0),
                             (i * spacing, BOARD_WIDTH), line_thickness)
            pygame.draw.line(self.window, line_color,
                             (0, i * spacing), (BOARD_HEIGHT, i * spacing), line_thickness)

        # draw the selected tile shading
        if self.selected_tile != None:
            sel_x, sel_y = self.selected_tile
            if self.tiles[sel_x][sel_y].number == 0:
                sel_tile_pos = (
                    sel_y * TILE_WIDTH + 3, sel_x * TILE_HEIGHT + 3)
                selected_rect = pygame.Rect(
                    sel_tile_pos[0], sel_tile_pos[1], TILE_WIDTH - 6, TILE_HEIGHT - 6)
                pygame.draw.rect(self.window, SELECT_OPEN_COLOR, selected_rect)

        # draw the tile numbers.
        for i in range(TILE_COUNT):
            for j in range(TILE_COUNT):
                self.tiles[i][j].draw(self.window)

    def select_tile(self, row: int, col: int):
        '''selects a tile denoted by row and column.'''

        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                try:
                    self.tiles[row][j].is_selected = False
                except TypeError as e:
                    print(e)
        self.tiles[row][col].is_selected = True
        self.selected_tile = (row, col)

    def clear_temp(self):
        '''clears temporary entry.'''

        r, c = self.selected_tile
        if self.tiles[r][c].number == 0:
            self.tiles[r][c].set_temp(None)

    def click_to_coord(self, pos: tuple[int]):
        '''translates a given mouse click position to a board coordinate.'''

        if pos[0] >= BOARD_HEIGHT or pos[0] < 0 or pos[1] >= BOARD_WIDTH or pos[1] < 0:
            return (-1, -1)
        else:
            spacing = BOARD_HEIGHT / TILE_COUNT
            # use floor division to get the correct tile.
            row = round(pos[0] // spacing)
            col = round(pos[1] // spacing)
            return (row, col)

    def attempt_placement(self, num: int):
        '''attempts to place a number at the selected board location.'''

        row, col = self.selected_tile
        # only attempt placements on tiles that haven't already been cemented.
        if self.board[row][col] != 0:
            return
        self.tiles[row][col].set_number(num)
        self.update_board()
        if self.board[row][col] != self.solution[row][col]:
            self.tiles[row][col].set_number(0)
            self.tiles[row][col].set_temp(None)
            self.update_board()
            return False
        else:
            return True

    def place_temp(self, num: int):
        '''sets temp of the selected tile.'''

        row, col = self.selected_tile
        self.tiles[row][col].set_temp(num)

    def speed_solve(self, timestamp: str, faults: int):
        '''visualization of the backtracking algorithm.'''

        global solver_speed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYUP and event.key == pygame.K_f:
                solver_speed = solver_speed % 3 + 1

        time_delay = SOLVE_SPEED_DELAY_DICT[solver_speed]
        next_spot = utils.find_next_empty(self.board)
        self.select_tile(next_spot[0], next_spot[1])
        if next_spot == (-1, -1):
            return True
        for i in range(1, 10):
            if utils.is_valid(self.board, next_spot, i):
                self.tiles[next_spot[0]][next_spot[1]].number = i
                self.update_board()
                pygame.time.delay(time_delay)
                redraw(self.window, self, timestamp, faults)

                if self.speed_solve(timestamp, faults):
                    return True

                self.tiles[next_spot[0]][next_spot[1]].number = 0
                self.update_board()
                pygame.time.delay(time_delay)
                redraw(self.window, self, timestamp, faults)


class Tile:
    '''a graphical sudoku board tile.'''

    def __init__(self, num: int, x: int, y: int):
        self.temp = None
        self.number = num
        self.x = x
        self.y = y
        self.shape = pygame.Rect(x, y, TILE_WIDTH, TILE_HEIGHT)
        self.is_selected = False

    def draw(self, win: pygame.Surface):
        '''draws tile numbers.'''

        spacing = BOARD_HEIGHT / TILE_COUNT
        pos = (spacing * self.x, spacing * self.y)

        if self.temp == 0 or (self.number == 0 and self.temp == None):
            return

        text_pos_x = None
        text_pos_y = None

        if self.number != 0:
            num_text = SUBMITTED_FONT.render(
                str(self.number), True, COLOR_BLACK)
            text_pos_x = self.x + (spacing / 2) - (num_text.get_width() / 2)
            text_pos_y = self.y + (spacing / 2) - (num_text.get_height() / 2)
        else:
            num_text = TEMP_FONT.render(str(self.temp), True, TEMP_NUM_COLOR)
            text_pos_x = self.x + 5
            text_pos_y = self.y + 5

        win.blit(num_text, (text_pos_x, text_pos_y))

    def is_clicked(self, mouse_pos):
        if self.shape.collidepoint(mouse_pos):
            self.is_selected = True
        return self.is_selected

    def set_temp(self, t: int):
        self.temp = t

    def set_number(self, n: int):
        self.number = n


def get_timestamp(elapsed: int):
    minutes, seconds = divmod(elapsed, 60)
    hours, minutes = divmod(minutes, 60)
    stamp = f'{hours:d}:{minutes:02d}:{seconds:02d}'
    return stamp


def redraw(win: pygame.Surface, board: Board, timestamp: str, faults: int):
    '''main drawing method.'''

    win.fill(COLOR_WHITE)
    time_text = SUBMITTED_FONT.render(timestamp, True, COLOR_BLACK)
    win.blit(time_text, (WINDOW_WIDTH - 140, WINDOW_HEIGHT - 45))

    if solver_speed != None:
        for i in range(solver_speed):
            p1 = (WINDOW_WIDTH - 260 + (i * 30), WINDOW_HEIGHT - 40)
            p2 = (WINDOW_WIDTH - 260 + (i * 30), WINDOW_HEIGHT - 10)
            p3 = (WINDOW_WIDTH - 230 + (i * 30), WINDOW_HEIGHT - 25)
            poly_coords = (p1, p2, p3)
            pygame.draw.polygon(win, COLOR_BLACK, poly_coords)

    fault_text = None
    if faults < 11:
        fault_text = SUBMITTED_FONT.render('X ' * faults, True, COLOR_RED)
    else:
        fault_text = SUBMITTED_FONT.render(str(faults), True, COLOR_RED)
    win.blit(fault_text, (10, WINDOW_HEIGHT - 45))
    board.draw()
    pygame.display.flip()


def run():
    '''main entry point of the program.'''

    window = pygame.display.set_mode(([WINDOW_WIDTH, WINDOW_HEIGHT]))
    pygame.display.set_caption("Sudoku!")
    # TODO set an icon for the display

    board_data = utils.build_board(BOARD_FILENAME)
    if board_data == None:
        return
    board = Board(window, board_data)

    running = True
    key_pressed = None
    time_start = time.time()
    faults = 0
    pygame.display.flip()

    while running:
        elapsed = round(time.time() - time_start)
        time_since_start = get_timestamp(elapsed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYUP:
                # true for pressing keys 1 through 9.
                if event.key > 48 and event.key < 58:
                    key_pressed = KEY_DICT[event.key]
                elif event.key == pygame.K_RETURN:
                    row, col = board.selected_tile

                    # if no temp value has been entered, disregard.
                    if board.tiles[row][col].temp == None:
                        continue
                    attempt = board.tiles[row][col].temp
                    is_good_placement = board.attempt_placement(attempt)
                    if is_good_placement:
                        print("Good one!")
                    else:
                        print("Bad placement.")
                        faults += 1
                    key_pressed = None
                    if utils.find_next_empty(board.board) == (-1, -1):
                        print("Game over, you won!")
                        running = False
                # used for removing a temp entry from a selected tile.
                elif event.key == pygame.K_BACKSPACE:
                    row, col = board.selected_tile
                    if (row, col) == (-1, -1) or board.tiles[row][col].number != 0 or board.tiles[row][col].temp == 0:
                        continue
                    board.tiles[row][col].set_temp(None)

                # quicksolves the board with a backtracking visualization.
                elif event.key == pygame.K_SPACE:
                    global solver_speed
                    solver_speed = 1
                    board.speed_solve(time_since_start, faults)
                    pygame.time.delay(1500)
                    running = False

            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                board_pos = board.click_to_coord(mouse_pos)

                # NOTE x and y are inverted here for 2d list indexing.
                if board_pos != (-1, -1):
                    board.select_tile(board_pos[1], board_pos[0])
                    key_pressed = None
        if board.selected_tile != None and key_pressed != None:
            board.place_temp(key_pressed)

        redraw(window, board, time_since_start, faults)


run()
pygame.quit()
