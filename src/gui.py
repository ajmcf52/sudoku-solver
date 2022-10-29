import pygame

TILE_COUNT = 9
TILE_WIDTH = 50
TILE_HEIGHT = TILE_WIDTH
BOARD_WIDTH = TILE_COUNT * TILE_WIDTH
BOARD_HEIGHT = BOARD_WIDTH
FONT_SIZE = 40
FONT = pygame.font.SysFont('newyork', FONT_SIZE)

COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_GREY = (133, 136, 140)

STANDARD_THICKNESS = 1
SUBGRID_THICKNESS = 3


game_board = Board()


def init(b: list[list[int]]):
    game_board.init_board(b)


class Board:
    '''a graphical sudoku board.'''

    def init_board(self, b: list[list[int]]):
        self.board = b

    def __init__(self, win: pygame.Surface):

        self.window = win
        self.board = None
        self.tiles = [[Tile(self.window, self.board[i][j], i *
                            TILE_HEIGHT, j * TILE_WIDTH) for j in range(TILE_COUNT)] for i in range(TILE_COUNT)]
        self.selected_tile = (-1, -1)

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

    def select_tile(self, r, c):
        '''selects a tile denoted by row and column.'''
        for i in range(TILE_COUNT):
            for j in range(TILE_COUNT):
                self.tiles[i][j].is_selected = False
        self.tiles[r][c].is_selected = True
        self.selected_tile = (r, c)

    def clear_selection(self):
        r, c = self.selected_tile

    def click_to_coord(self, pos: tuple(int)):
        '''translates a given mouse click position to a board coordinate.'''

        if pos[0] >= BOARD_HEIGHT or pos[0] < 0 or pos[1] >= BOARD_WIDTH or pos[1] < 0:
            return (-1, -1)
        else:
            spacing = BOARD_HEIGHT / TILE_COUNT
            # use floor division to get the correct tile.
            row = pos[0] // spacing
            col = pos[1] // spacing
            return (row, col)


class Tile:
    '''a graphical sudoku board tile.'''

    def __init__(self, num: int, x: int, y: int):
        self.temp = -1
        self.number = num
        self.x = x
        self.y = y
        self.shape = pygame.Rect(x, y, TILE_WIDTH, TILE_HEIGHT)
        self.is_selected = False

    def draw(self, win: pygame.Surface, c: tuple(int)):
        '''draws tile numbers.'''

        spacing = BOARD_HEIGHT / TILE_COUNT
        pos = (spacing * self.x, spacing * self.y)

        # for drawing a tile number that hasn't been submitted.
        if self.temp != -1 and self.number == 0:
            num_text = FONT.render(str(self.temp), True, COLOR_GREY)
            win.blit(text, (pos[0], pos[1]))
        # for drawing submitted numbers.
        elif self.value != 0:
            num_text = FONT.render(str(self.temp), True, COLOR_BLACK)
            win.blit(num_text, (pos[0] + (spacing / 2 -
                                          (num_text.get_width() / 2)), (pos[1] + (spacing / 2 - (num_text.get_width() / 2)))))

        num_text = FONT.render(str(self.number), True, c)
        win.blit(num_text, (self.x, self.y))

    def is_clicked(self, mouse_pos):
        if self.shape.collidepoint(mouse_pos):
            self.is_selected = True
        return self.is_selected


def run():
    pygame.init()
    print(pygame.font.get_fonts())
    screen = pygame.display.set_mode(([600, 600]))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
    pygame.quit()
