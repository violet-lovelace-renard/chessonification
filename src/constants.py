import pygame

COLOR_BACKGROUND = pygame.Color.from_hex("#323232")
COLOR_LIGHT_SQUARE = pygame.Color.from_hex("#debfff")
COLOR_DARK_SQUARE = pygame.Color.from_hex("#8128e0")
COLOR_CURSOR_BODY = pygame.Color.from_hex("#eeeeee")
COLOR_CURSOR_OUTLINE = pygame.Color.from_hex("#111111")
COLOR_NONE = pygame.Color.from_hex("#00000000")

SQUARE_SIZE = 96

SURFACE_LIGHT_SQUARE = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
SURFACE_LIGHT_SQUARE.fill(COLOR_LIGHT_SQUARE)

SURFACE_DARK_SQUARE = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
SURFACE_DARK_SQUARE.fill(COLOR_DARK_SQUARE)

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
CURSOR_SIZE = SQUARE_SIZE / 3
CURSOR_OUTSET = 10  # Outset cursor pieces from square corners

CURSOR_CORNER = 4
CURSOR_LEG = CURSOR_CORNER + CURSOR_CORNER * 1.41  # sqrt(2) for diagonal

SURFACE_CURSOR_NW = pygame.Surface((CURSOR_SIZE, CURSOR_SIZE), flags=pygame.SRCALPHA)
SURFACE_CURSOR_NW.fill(COLOR_NONE)
pygame.draw.polygon(SURFACE_CURSOR_NW, COLOR_CURSOR_OUTLINE,
                    [[0, 0], [CURSOR_SIZE, 0], [0, CURSOR_SIZE]])
pygame.draw.polygon(SURFACE_CURSOR_NW, COLOR_CURSOR_BODY,
                    [[CURSOR_CORNER, CURSOR_CORNER],
                     [CURSOR_SIZE - CURSOR_LEG, CURSOR_CORNER],
                     [CURSOR_CORNER, CURSOR_SIZE - CURSOR_LEG]])

SURFACE_CURSOR_NE = pygame.transform.flip(SURFACE_CURSOR_NW, flip_x=True, flip_y=False)
SURFACE_CURSOR_SE = pygame.transform.flip(SURFACE_CURSOR_NW, flip_x=True, flip_y=True)
SURFACE_CURSOR_SW = pygame.transform.flip(SURFACE_CURSOR_NW, flip_x=False, flip_y=True)
