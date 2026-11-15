import pygame

COLOR_BACKGROUND = pygame.Color.from_hex("#323232")
COLOR_LIGHT_SQUARE = pygame.Color.from_hex("#b97bfc")
COLOR_DARK_SQUARE = pygame.Color.from_hex("#5d17a8")

SQUARE_LENGTH = 96

SURFACE_LIGHT_SQUARE = pygame.Surface((SQUARE_LENGTH, SQUARE_LENGTH))
SURFACE_LIGHT_SQUARE.fill(COLOR_LIGHT_SQUARE)

SURFACE_DARK_SQUARE = pygame.Surface((SQUARE_LENGTH, SQUARE_LENGTH))
SURFACE_DARK_SQUARE.fill(COLOR_DARK_SQUARE)

DICT_PIECES = {
    "k": pygame.image.load_sized_svg("assets/bK.svg", (SQUARE_LENGTH, SQUARE_LENGTH)),
    "q": pygame.image.load_sized_svg("assets/bQ.svg", (SQUARE_LENGTH, SQUARE_LENGTH)),
    "r": pygame.image.load_sized_svg("assets/bR.svg", (SQUARE_LENGTH, SQUARE_LENGTH)),
    "b": pygame.image.load_sized_svg("assets/bB.svg", (SQUARE_LENGTH, SQUARE_LENGTH)),
    "n": pygame.image.load_sized_svg("assets/bN.svg", (SQUARE_LENGTH, SQUARE_LENGTH)),
    "p": pygame.image.load_sized_svg("assets/bP.svg", (SQUARE_LENGTH, SQUARE_LENGTH)),
    "K": pygame.image.load_sized_svg("assets/wK.svg", (SQUARE_LENGTH, SQUARE_LENGTH)),
    "Q": pygame.image.load_sized_svg("assets/wQ.svg", (SQUARE_LENGTH, SQUARE_LENGTH)),
    "R": pygame.image.load_sized_svg("assets/wR.svg", (SQUARE_LENGTH, SQUARE_LENGTH)),
    "B": pygame.image.load_sized_svg("assets/wB.svg", (SQUARE_LENGTH, SQUARE_LENGTH)),
    "N": pygame.image.load_sized_svg("assets/wN.svg", (SQUARE_LENGTH, SQUARE_LENGTH)),
    "P": pygame.image.load_sized_svg("assets/wP.svg", (SQUARE_LENGTH, SQUARE_LENGTH)),
}
