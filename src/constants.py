import pygame

COLOR_BACKGROUND = pygame.Color.from_hex("#323232")
COLOR_LIGHT_SQUARE = pygame.Color.from_hex("#debfff")
COLOR_DARK_SQUARE = pygame.Color.from_hex("#8128e0")

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
