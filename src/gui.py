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
FONT_SIZE = 30
FONT = pygame.font.SysFont('newyork', FONT_SIZE)

COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_GREY = (133, 136, 140)
COLOR_WHITE = (255, 255, 255)

STANDARD_THICKNESS = 1
SUBGRID_THICKNESS = 2
SELECT_THICKNESS = 4

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
        self.tiles = [[Tile(self.board[i][j], i *
                            TILE_HEIGHT, j * TILE_WIDTH) for j in range(TILE_COUNT)] for i in range(TILE_COUNT)]
        self.selected_tile = (-1, -1)

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
            line_thickness = SUBGRID_THICKNESS if i % 3 == 0 else STANDARD_THICKNESS
            pygame.draw.line(self.window, COLOR_BLACK, (i * spacing, 0),
                             (i * spacing, BOARD_WIDTH), line_thickness)
            pygame.draw.line(self.window, COLOR_BLACK,
                             (0, i * spacing), (BOARD_HEIGHT, i * spacing), line_thickness)

        # draw the tiles.
        for i in range(TILE_COUNT):
            for j in range(TILE_COUNT):
                self.tiles[i][j].draw(self.window, COLOR_BLACK)

    def select_tile(self, row: int, col: int):
        '''selects a tile denoted by row and column.'''

        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                try:
                    self.tiles[row][j].is_selected = False
                except TypeError as e:
                    print(e)
        self.tiles[int(row)][int(col)].is_selected = True
        self.selected_tile = (row, col)

    def clear_temp(self):
        '''clears temporary entry.'''

        r, c = self.selected_tile
        if self.tiles[r][c].number == 0:
            self.tiles[r][c].set_temp(0)

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
            self.tiles[row][col].set_temp(0)
            self.update_board()
            return False
        else:
            return True

    def place_temp(self, num: int):
        '''sets temp of the selected tile.'''

        row, col = self.selected_tile
        self.tiles[row][col].set_temp(num)


class Tile:
    '''a graphical sudoku board tile.'''

    def __init__(self, num: int, x: int, y: int):
        self.temp = None
        self.number = num
        self.x = x
        self.y = y
        self.shape = pygame.Rect(x, y, TILE_WIDTH, TILE_HEIGHT)
        self.is_selected = False

    def draw(self, win: pygame.Surface, c: tuple[int]):
        '''draws tile numbers.'''

        spacing = BOARD_HEIGHT / TILE_COUNT
        pos = (spacing * self.x, spacing * self.y)

        if self.number == 0 and self.temp == None:
            return

        # for drawing a tile number that hasn't been submitted.
        # if self.number != 0:
        #     num_text = FONT.render(str(self.temp), True, COLOR_GREY)
        #     win.blit(num_text, (pos[0], pos[1]))
        # for drawing submitted numbers.
        if self.number != 0:
            num_text = FONT.render(str(self.temp), True, COLOR_BLACK)
            win.blit(num_text, (pos[0] + (spacing / 2 -
                                          (num_text.get_width() / 2)), (pos[1] + (spacing / 2 - (num_text.get_width() / 2)))))

        num_text = FONT.render(str(self.number), True, c)
        win.blit(num_text, (self.x, self.y))

    def is_clicked(self, mouse_pos):
        if self.shape.collidepoint(mouse_pos):
            self.is_selected = True
        return self.is_selected

    def set_temp(self, t: int):
        self.temp = t

    def set_number(self, n: int):
        self.number = n


def get_timestamp(elapsed: float):
    seconds = elapsed % 60
    minutes = seconds // 60
    hours = minutes // 60
    stamp = time.strftime('%H:%M:%S', time.localtime())
    return stamp


def redraw(win: pygame.Surface, board: Board, timestamp: str, faults: int):
    '''main drawing method.'''
    win.fill(COLOR_WHITE)
    time_text = FONT.render(timestamp, True, COLOR_BLACK)
    win.blit(time_text, (WINDOW_WIDTH - 150, WINDOW_HEIGHT - 5))
    fault_text = FONT.render('X ' * faults, True, COLOR_RED)
    win.blit(fault_text, (10, WINDOW_HEIGHT - 10))
    board.draw()


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
    key_pressed = -1
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
                    if board.tiles[row][col].temp == 0:
                        continue
                    attempt = board.tiles[row][col].temp
                    is_good_placement = board.attempt_placement(attempt)
                    if is_good_placement:
                        print("Good.")
                    else:
                        print("Bad placement.")
                        faults += 1
                    key_pressed = -1
                    if utils.find_next_empty(board) == (-1, -1):
                        print("Game over, you won!")
                        running = False
                # used for removing a temp entry from a selected tile.
                elif event.key == pygame.K_BACKSPACE:
                    row, col = board.selected_tile
                    if (row, col) == (-1, -1) or board.tiles[row][col].number != 0 or board.tiles[row][col].temp == 0:
                        continue
                    board.tiles[row][col].set_temp(0)

                # used to quicksolve the board.
                elif event.key == pygame.K_SPACE:
                    # TODO fill this in!
                    pass
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                board_pos = board.click_to_coord(mouse_pos)
                if board_pos != (-1, -1):
                    board.select_tile(int(board_pos[0]), int(board_pos[1]))
                    key_pressed = -1
        if board.selected_tile != (-1, -1) and key_pressed != -1:
            board.place_temp(key_pressed)

        redraw(window, board, time_since_start, faults)
        pygame.display.update()


run()
pygame.quit()
