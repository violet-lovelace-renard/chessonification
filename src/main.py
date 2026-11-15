"""
Entry point for the chessonification program.

Usage:
    python main.py
"""

import chess
import pygame

from sonify import Sonifier
from constants import *

class App:
    """
    Bundles everything going on in the app (game, sonification, bookkeeping,
    etc.).
    """

    def __init__(self):
        """Create a new app instance."""
        pygame.init()

        self.screen: pygame.Surface = pygame.display.set_mode(flags=pygame.FULLSCREEN)
        self.clock: pygame.Clock = pygame.time.Clock()

        self.board = chess.Board()

    def mainloop(self) -> App:
        """
        Run the app. Blocks until the app is quit (e.g., by clicking the "X"
        close window button). Returns `self` for method chaining.
        """

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
    
            self.render()
    
            pygame.display.flip()
            self.clock.tick(60)

        return self

    def render(self) -> None:
        """Draw a new frame containing the background and board state."""

        self.screen.fill(COLOR_BACKGROUND)

        def drawSquare(row, col) -> None:
            if (row + col) % 2 == 0:
                self.screen.blit(SURFACE_LIGHT_SQUARE,
                                 (self.screen.width // 2 + (col - 4) * SQUARE_LENGTH,
                                  self.screen.height // 2 + (row - 4) * SQUARE_LENGTH))
            else:
                self.screen.blit(SURFACE_DARK_SQUARE,
                                 (self.screen.width // 2 + (col - 4) * SQUARE_LENGTH,
                                  self.screen.height // 2 + (row - 4) * SQUARE_LENGTH))

        # Draw squares
        [drawSquare(r, c) for r in range(8) for c in range(8)]

        # Draw pieces
        for square, piece in self.board.piece_map().items():
            pass

    def close(self) -> None:
        """Frees resources held by this app instance."""

        pygame.quit()


def main() -> None:
    """The entry point. Launches the game, GUI, and starts sonifying."""

    App().mainloop().close()

if __name__ == "__main__":
    main()
