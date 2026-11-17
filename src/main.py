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
        self.hoveredSquare: tuple[int, int] | None = None
        self.selectedSquare: tuple[int, int] | None = None
        self.selectedPiece: chess.Piece | None = None

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
                case pygame.MOUSEBUTTONDOWN:
                    self._handleClick()

        self.hoveredSquare = self._squareOfPoint(pygame.mouse.get_pos())

    def render(self) -> None:
        """Draw a new frame containing the background and board state."""

        self.screen.fill(COLOR_BACKGROUND)
        [self._drawSquare((r, c)) for r in range(8) for c in range(8)]
        [self._drawPiece(piece.symbol(),
                         self._pointOfChessSquare(square))
                         for square, piece in self.board.piece_map().items()]

        self._drawSelectedPiece()
        self._drawTargetPiece()

        self._setCursor()

    def close(self) -> None:
        """Frees resources held by this app instance."""

        pygame.quit()

    def _handleClick(self) -> None:
        if not self.selectedSquare:
            square = self._squareOfPoint(pygame.mouse.get_pos())
            if not square:
                return
    
            piece = self.board.piece_at(chess.square(square[1], 7 - square[0]))
            if not piece:
                return
    
            self.selectedSquare = square
            self.selectedPiece = piece
        else:
            square = self._squareOfPoint(pygame.mouse.get_pos())
            if not square:
                self.selectedSquare = None
                self.selectedPiece = None
                return

            # TODO: account for promotion
            tryMove = chess.Move(from_square=self._chessSquareOfPoint(self.selectedSquare),
                                 to_square=self._chessSquareOfPoint(square))
            if self.board.is_legal(tryMove):
                self.board.push(tryMove)

            self.selectedSquare = None
            self.selectedPiece = None

    def _getPieceAt(self, rowCol: tuple[int, int]) -> chess.Piece | None:
        return self.board.piece_at(chess.square(rowCol[1], 7 - rowCol[0]))


    def _chessSquareOfPoint(self, rowCol: tuple[int, int]) -> chess.Square:
        r, c = rowCol
        return chess.square(rank_index=7 - r, file_index=c)

    def _pointOfChessSquare(self, square: chess.Square) -> tuple[float, float]:
        file, rank = chess.square_file(square), chess.square_rank(square)
        return (self.screen.width // 2 + (file - 4) * SQUARE_SIZE,
                self.screen.height // 2 + ((7 - rank) - 4) * SQUARE_SIZE)

    def _pointOfRowCol(self, rowCol: tuple[int, int]) -> tuple[float, float]:
        row, col = rowCol
        return (self.screen.width // 2 + (col - 4) * SQUARE_SIZE,
                self.screen.height // 2 + (row - 4) * SQUARE_SIZE)

    def _squareOfPoint(self, xY: tuple[float, float]) -> tuple[int, int] | None:
        x, y = xY
        r, c = (int((y - self.screen.height // 2) // SQUARE_SIZE + 4),
                  int((x - self.screen.width // 2) // SQUARE_SIZE + 4))
        return None if r < 0 or r >= 8 or c < 0 or c >= 8 else (r, c)

    def _drawSquare(self, rowCol: tuple[int, int], transparent: bool=False) -> None:
        row, col = rowCol
        match (row + col) % 2 == 0, transparent:
            case True, True:
                s = SURFACE_LIGHT_SQUARE_TRANSPARENT
            case True, False:
                s = SURFACE_LIGHT_SQUARE
            case False, True:
                s = SURFACE_DARK_SQUARE_TRANSPARENT
            case False, False:
                s = SURFACE_DARK_SQUARE

        self.screen.blit(s, self._pointOfRowCol((row, col)))

    def _drawPiece(self, piece: str, xY: tuple[float, float]) -> None:
        x, y = xY
        self.screen.blit(DICT_PIECES[piece], (x, y))

    def _drawSelectedPiece(self) -> None:
        if not self.selectedSquare:
            return

        self._drawSquare(self.selectedSquare, transparent=True)

    def _drawTargetPiece(self) -> None:
        if not self.selectedPiece:
            return

        x, y = pygame.mouse.get_pos()
        self._drawPiece(self.selectedPiece.symbol(), (x, y))

    def _setCursor(self) -> None:
        if not self.selectedPiece and\
            not (self.hoveredSquare and self._getPieceAt(self.hoveredSquare)):
            pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))
        else:
            pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))


def main() -> None:
    """The entry point. Launches the game, GUI, and starts sonifying."""

    App().mainloop().close()

if __name__ == "__main__":
    main()
