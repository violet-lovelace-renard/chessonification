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

        self.board: chess.Board = chess.Board()
        self.hovered: tuple[int, int] | None = None

    def mainloop(self) -> App:
        """
        Run the app. Blocks until the app is quit (e.g., by clicking the "X"
        close window button). Returns `self` for method chaining.
        """

        self.running = True
        while self.running:
            self.update()
            self.render()
    
            pygame.display.flip()
            self.clock.tick(60)

        return self

    def update(self) -> None:
        """Handle controls and OS-level app interactions."""
        
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.running = False
                    return

        self.hovered = self._squareOfPoint(*pygame.mouse.get_pos())

    def render(self) -> None:
        """Draw a new frame containing the background and board state."""

        self.screen.fill(COLOR_BACKGROUND)
        [self._drawSquare(r, c) for r in range(8) for c in range(8)]
        [self._drawPiece(piece.symbol(),
                         7 - chess.square_rank(square), chess.square_file(square))
                         for square, piece in self.board.piece_map().items()]

        if self.hovered is not None:
            self._drawCursor(*self._pointOfSquare(*self.hovered))

    def close(self) -> None:
        """Frees resources held by this app instance."""

        pygame.quit()

    def _pointOfSquare(self, row: int, col: int) -> tuple[float, float]:
        return (self.screen.width // 2 + (col - 4) * SQUARE_SIZE,
                self.screen.height // 2 + (row - 4) * SQUARE_SIZE)

    def _squareOfPoint(self, x: float, y: float) -> tuple[int, int] | None:
        r, c = (int((y - self.screen.height // 2) // SQUARE_SIZE + 4),
                  int((x - self.screen.width // 2) // SQUARE_SIZE + 4))
        return None if r < 0 or r >= 8 or c < 0 or c >= 8 else (r, c)

    def _drawSquare(self, row: int, col: int) -> None:
        s = SURFACE_LIGHT_SQUARE if (row + col) % 2 == 0\
                else SURFACE_DARK_SQUARE
        self.screen.blit(s, self._pointOfSquare(row, col))

    def _drawPiece(self, piece: str, row: int, col: int) -> None:
        self.screen.blit(DICT_PIECES[piece], self._pointOfSquare(row, col))

    def _drawCursor(self, x: float, y: float) -> None:
        nwX, nwY = x, y
        nwX, nwY = nwX - CURSOR_OUTSET, nwY - CURSOR_OUTSET
        otherSide = SQUARE_SIZE - CURSOR_SIZE + 2 * CURSOR_OUTSET

        self.screen.blit(SURFACE_CURSOR_NW, (nwX,             nwY))
        self.screen.blit(SURFACE_CURSOR_NE, (nwX + otherSide, nwY))
        self.screen.blit(SURFACE_CURSOR_SE, (nwX + otherSide, nwY + otherSide))
        self.screen.blit(SURFACE_CURSOR_SW, (nwX,             nwY + otherSide))


def main() -> None:
    """The entry point. Launches the game, GUI, and starts sonifying."""

    App().mainloop().close()

if __name__ == "__main__":
    main()
