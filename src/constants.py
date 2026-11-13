import pygame

COLOR_BACKGROUND = pygame.Color.from_hex("#323232")
COLOR_LIGHT_SQUARE = pygame.Color.from_hex("#b97bfc")
COLOR_DARK_SQUARE = pygame.Color.from_hex("#5d17a8")

SURFACE_LIGHT_SQUARE = pygame.Surface((50, 50))
SURFACE_LIGHT_SQUARE.fill(COLOR_LIGHT_SQUARE)

SURFACE_DARK_SQUARE = pygame.Surface((50, 50))
SURFACE_DARK_SQUARE.fill(COLOR_DARK_SQUARE)
