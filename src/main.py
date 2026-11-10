"""
Entry point for the chessonification program.

Usage:
    python main.py
"""

import pygame

from game import Game
from sonify import Sonifier

def main() -> None:
    """The entry point. Launches the game, GUI, and starts sonifying."""

    pygame.init()
    screen: pygame.Surface = pygame.display.set_mode((1280, 720))
    clock: pygame.Clock = pygame.time.Clock()
    running: bool = True

    # Create a game

    # Launch sonification

    # Game mainloop...
    pass

if __name__ == "__main__":
    main()
