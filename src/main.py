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

    def __init__(self) -> None:
        """Create a new app instance."""
        pygame.init()

        self.screen: pygame.Surface = pygame.display.set_mode(flags=pygame.FULLSCREEN)
        self.clock: pygame.Clock = pygame.time.Clock()

        self.board = chess.Board()
        self.cursor = self.Cursor(self)

    def mainloop(self) -> App:
        """
        Run the app. Blocks until the app is quit (e.g., by clicking the "X"
        close window button). Returns `self` for method chaining.
        """

        self.running = True
        while self.running:
            self.render()
            self.handleEvents()
    
            pygame.display.flip()
            self.clock.tick(60)

        return self

    def handleEvents(self) -> None:
        """Handle controls and OS-level app interactions."""
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def _pointOfCoords(self, row: int, col: int) -> tuple[float, float]:
        return (self.screen.width // 2 + (col - 4) * SQUARE_LENGTH,
                self.screen.height // 2 + (row - 4) * SQUARE_LENGTH)

    def render(self) -> None:
        """Draw a new frame containing the background and board state."""

        def drawSquare(row: int, col: int) -> None:
            if (row + col) % 2 == 0:
                self.screen.blit(SURFACE_LIGHT_SQUARE, self._pointOfCoords(row, col))
            else:
                self.screen.blit(SURFACE_DARK_SQUARE, self._pointOfCoords(row, col))

        def drawPiece(piece: str, row: int, col: int) -> None:
            self.screen.blit(DICT_PIECES[piece], self._pointOfCoords(row, col))

        self.screen.fill(COLOR_BACKGROUND)
        [drawSquare(r, c) for r in range(8) for c in range(8)]
        [drawPiece(piece.symbol(),
                   7 - chess.square_rank(square), chess.square_file(square))
         for square, piece in self.board.piece_map().items()]
        self.cursor.drawSelf()

    def close(self) -> None:
        """Frees resources held by this app instance."""

        pygame.quit()

    class Cursor:
        def __init__(self, appInstance: App) -> None:
            self.row = 0
            self.col = 0
            self.appInstance = appInstance

        def drawSelf(self) -> None:
            nwX, nwY = self.appInstance._pointOfCoords(self.row, self.col)
            nwX, nwY = nwX - CURSOR_OUTSET, nwY - CURSOR_OUTSET
            otherSide = SQUARE_LENGTH - CURSOR_SIZE + 2 * CURSOR_OUTSET

            screen = self.appInstance.screen
            screen.blit(SURFACE_CURSOR_NW, (nwX,             nwY))
            screen.blit(SURFACE_CURSOR_NE, (nwX + otherSide, nwY))
            screen.blit(SURFACE_CURSOR_SE, (nwX + otherSide, nwY + otherSide))
            screen.blit(SURFACE_CURSOR_SW, (nwX,             nwY + otherSide))


def main() -> None:
    """The entry point. Launches the game, GUI, and starts sonifying."""

    App().mainloop().close()

if __name__ == "__main__":
    main()
