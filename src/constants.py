import pygame

pygame.font.init()

def _squareMaker(size: float, transparent: bool=False) -> pygame.Surface:
    return pygame.Surface((size, size),
                          flags=pygame.SRCALPHA if transparent else 0)

COLOR_BACKGROUND = pygame.Color.from_hex("#323232")
COLOR_LIGHT_SQUARE = pygame.Color.from_hex("#debfff")
COLOR_LIGHT_SQUARE_TRANSPARENT = pygame.Color.from_hex("#debfff80")
COLOR_DARK_SQUARE = pygame.Color.from_hex("#8128e0")
COLOR_DARK_SQUARE_TRANSPARENT = pygame.Color.from_hex("#8128e080")
COLOR_BOARD_OVERLAY_TRANSPARENT = pygame.Color.from_hex("#4A4A4B80")
COLOR_TURN_INDICATOR = pygame.Color.from_hex("#ae63ff")
COLOR_PROMOTE_MENU_WHITE = pygame.Color.from_hex("#260c42")
COLOR_PROMOTE_MENU_BLACK = pygame.Color.from_hex("#f9f4ff")
COLOR_TEXT = pygame.Color.from_hex("#ffffff")
COLOR_NONE = pygame.Color.from_hex("#00000000")

FONT_BODY = pygame.Font(size=100)

TEXT_WHITE_WINS = FONT_BODY.render("White wins!", antialias=True,
                                   color=COLOR_TEXT)
TEXT_BLACK_WINS = FONT_BODY.render("Black wins!", antialias=True,
                                   color=COLOR_TEXT)
TEXT_DRAW = FONT_BODY.render("Draw...", antialias=True,
                             color=COLOR_TEXT)
RESULT_HEIGHT = TEXT_WHITE_WINS.height

SQUARE_SIZE = 96

SURFACE_LIGHT_SQUARE = _squareMaker(SQUARE_SIZE)
SURFACE_LIGHT_SQUARE.fill(COLOR_LIGHT_SQUARE)
SURFACE_LIGHT_SQUARE_TRANSPARENT = _squareMaker(SQUARE_SIZE, transparent=True)
SURFACE_LIGHT_SQUARE_TRANSPARENT.fill(COLOR_LIGHT_SQUARE_TRANSPARENT)

SURFACE_DARK_SQUARE = _squareMaker(SQUARE_SIZE)
SURFACE_DARK_SQUARE.fill(COLOR_DARK_SQUARE)
SURFACE_DARK_SQUARE_TRANSPARENT = _squareMaker(SQUARE_SIZE, transparent=True)
SURFACE_DARK_SQUARE_TRANSPARENT.fill(COLOR_DARK_SQUARE_TRANSPARENT)

EXIT_BUTTON_SIZE = SQUARE_SIZE / 2
EXIT_BUTTON_CORNER_DISTANCE = 5
EXIT_BUTTON_PADDING = 10
EXIT_X_SIZE = EXIT_BUTTON_SIZE - 2 * EXIT_BUTTON_PADDING
EXIT_BUTTON_POSITION = [SQUARE_SIZE, SQUARE_SIZE]

SURFACE_EXIT_BUTTON = _squareMaker(EXIT_BUTTON_SIZE)
SURFACE_EXIT_BUTTON.fill(COLOR_DARK_SQUARE)
d = EXIT_BUTTON_CORNER_DISTANCE
s = EXIT_X_SIZE
xPoints = [[d, 0], [s/2, s/2-d], [s-d, 0],
           [s, d], [s/2+d, s/2], [s, s-d],
           [s-d, s], [s/2, s/2+d], [d, s],
           [0, s-d], [s/2-d, s/2], [0, d]]
xPoints = [(x + EXIT_BUTTON_PADDING, y + EXIT_BUTTON_PADDING)
                for [x, y] in xPoints]
pygame.draw.polygon(SURFACE_EXIT_BUTTON, COLOR_LIGHT_SQUARE, xPoints)

TURN_INDICATOR_SIZE = 30
TURN_INDICATOR_MARGIN = 30
SURFACE_TURN_INDICATOR = _squareMaker(TURN_INDICATOR_SIZE, transparent=True)
SURFACE_TURN_INDICATOR.fill(COLOR_NONE)
pygame.draw.circle(SURFACE_TURN_INDICATOR, COLOR_TURN_INDICATOR,
                   [TURN_INDICATOR_SIZE / 2, TURN_INDICATOR_SIZE / 2],
                   TURN_INDICATOR_SIZE / 2)

SURFACE_BOARD_OVERLAY = _squareMaker(SQUARE_SIZE * 8, True)
SURFACE_BOARD_OVERLAY.fill(COLOR_BOARD_OVERLAY_TRANSPARENT)

SURFACE_PROMOTE_MENU_WHITE = pygame.Surface((SQUARE_SIZE * 4.5, SQUARE_SIZE * 1.5))
SURFACE_PROMOTE_MENU_WHITE.fill(COLOR_PROMOTE_MENU_WHITE)
SURFACE_PROMOTE_MENU_BLACK = pygame.Surface((SQUARE_SIZE * 4.5, SQUARE_SIZE * 1.5))
SURFACE_PROMOTE_MENU_BLACK.fill(COLOR_PROMOTE_MENU_BLACK)

DICT_PIECES = {
    "k": pygame.image.load_sized_svg("assets/bK.svg", (SQUARE_SIZE, SQUARE_SIZE)),
    "q": pygame.image.load_sized_svg("assets/bQ.svg", (SQUARE_SIZE, SQUARE_SIZE)),
    "r": pygame.image.load_sized_svg("assets/bR.svg", (SQUARE_SIZE, SQUARE_SIZE)),
    "b": pygame.image.load_sized_svg("assets/bB.svg", (SQUARE_SIZE, SQUARE_SIZE)),
    "n": pygame.image.load_sized_svg("assets/bN.svg", (SQUARE_SIZE, SQUARE_SIZE)),
    "p": pygame.image.load_sized_svg("assets/bP.svg", (SQUARE_SIZE, SQUARE_SIZE)),
    "K": pygame.image.load_sized_svg("assets/wK.svg", (SQUARE_SIZE, SQUARE_SIZE)),
    "Q": pygame.image.load_sized_svg("assets/wQ.svg", (SQUARE_SIZE, SQUARE_SIZE)),
    "R": pygame.image.load_sized_svg("assets/wR.svg", (SQUARE_SIZE, SQUARE_SIZE)),
    "B": pygame.image.load_sized_svg("assets/wB.svg", (SQUARE_SIZE, SQUARE_SIZE)),
    "N": pygame.image.load_sized_svg("assets/wN.svg", (SQUARE_SIZE, SQUARE_SIZE)),
    "P": pygame.image.load_sized_svg("assets/wP.svg", (SQUARE_SIZE, SQUARE_SIZE)),
}
