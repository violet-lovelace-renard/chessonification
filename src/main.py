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
        self.promoteMenu: tuple[chess.Color, tuple[int, int]] | None = None

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
            self.clock.tick(FPS)

        return self

    def update(self) -> None:
        """Handle controls and OS-level app interactions."""
        
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.running = False
                    return
                case pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        self._handleClick()
                    elif event.button == pygame.BUTTON_RIGHT:
                        self._handleRightClick()

        self.hoveredSquare = self._squareOfPoint(pygame.mouse.get_pos())

    def render(self) -> None:
        """Draw a new frame containing the background and board state."""

        self.screen.fill(COLOR_BACKGROUND)
        self.screen.blit(SURFACE_EXIT_BUTTON, EXIT_BUTTON_POSITION)

        [self._drawSquare((r, c)) for r in range(8) for c in range(8)]
        [self._drawPiece(piece.symbol(),
                         self._pointOfChessSquare(square))
                         for square, piece in self.board.piece_map().items()]

        self._drawSelectedPiece()
        self._drawTargetPiece()
        self._drawPromoteMenu()
        self._drawOverlay()
        self._drawTurnIndicator()

        self._setCursor()

    def close(self) -> None:
        """Frees resources held by this app instance."""

        pygame.quit()

    def _handleRightClick(self) -> None:
        # Deselect any held piece and cancel promotion.
        self.selectedSquare = None
        self.selectedPiece = None
        self.promoteMenu = None

    def _handleClick(self) -> None:
        mousePos = pygame.mouse.get_pos()

        if mousePos[0] > EXIT_BUTTON_POSITION[0] and\
                mousePos[0] < EXIT_BUTTON_POSITION[0] + EXIT_BUTTON_SIZE and\
                mousePos[1] > EXIT_BUTTON_POSITION[1] and\
                mousePos[1] < EXIT_BUTTON_POSITION[1] + EXIT_BUTTON_SIZE:
            self.running = False
            return

        if self.board.is_game_over():
            return

        if self.promoteMenu:
            choice = self._hoverPromotion()

            if choice is None:
                self.selectedSquare = None
                self.selectedPiece = None
                self.promoteMenu = None
                return

            _, square = self.promoteMenu
            choices = [chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT]

            assert(self.selectedSquare)
            tryMovePromote = chess.Move(from_square=self._chessSquareOfPoint(self.selectedSquare),
                                        to_square=self._chessSquareOfPoint(square),
                                        promotion=choices[choice])
            self.board.push(tryMovePromote)

            self.selectedSquare = None
            self.selectedPiece = None
            self.promoteMenu = None
            return

        if not self.selectedSquare:
            square = self._squareOfPoint(mousePos)
            if not square:
                return
    
            piece = self.board.piece_at(chess.square(square[1], 7 - square[0]))
            if not piece:
                return
    
            self.selectedSquare = square
            self.selectedPiece = piece
        else:
            square = self._squareOfPoint(mousePos)
            if not square:
                self.selectedSquare = None
                self.selectedPiece = None
                return

            tryMove = chess.Move(from_square=self._chessSquareOfPoint(self.selectedSquare),
                                 to_square=self._chessSquareOfPoint(square))
            tryMovePromote = chess.Move(from_square=self._chessSquareOfPoint(self.selectedSquare),
                                        to_square=self._chessSquareOfPoint(square),
                                        promotion=chess.QUEEN)
            if self.board.is_legal(tryMove):
                self.board.push(tryMove)
            # Easiest way to check if a promoting move is legal, since normal
            # movement of pawn to 8th rank is illegal.
            elif self.board.is_legal(tryMovePromote):
                self.promoteMenu = self.board.turn, square
                return

            self.selectedSquare = None
            self.selectedPiece = None

    def _getPieceAt(self, rowCol: tuple[int, int]) -> chess.Piece | None:
        return self.board.piece_at(chess.square(rowCol[1], 7 - rowCol[0]))

    def _chessSquareOfPoint(self, rowCol: tuple[int, int]) -> chess.Square:
        r, c = rowCol
        return chess.square(rank_index=7 - r, file_index=c)

    def _pointOfChessSquare(self, square: chess.Square) -> tuple[float, float]:
        file, rank = chess.square_file(square), chess.square_rank(square)
        return (self.screen.width / 2 + (file - 4) * SQUARE_SIZE,
                self.screen.height / 2 + ((7 - rank) - 4) * SQUARE_SIZE)

    def _pointOfRowCol(self, rowCol: tuple[int, int]) -> tuple[float, float]:
        row, col = rowCol
        return (self.screen.width / 2 + (col - 4) * SQUARE_SIZE,
                self.screen.height / 2 + (row - 4) * SQUARE_SIZE)

    def _squareOfPoint(self, xY: tuple[float, float]) -> tuple[int, int] | None:
        x, y = xY
        r, c = (int((y - self.screen.height // 2) // SQUARE_SIZE + 4),
                  int((x - self.screen.width // 2) // SQUARE_SIZE + 4))
        return None if r < 0 or r >= 8 or c < 0 or c >= 8 else (r, c)

    def _hoverPromotion(self) -> int | None:
        x, y = pygame.mouse.get_pos()
        if y < self.screen.height / 2 - SQUARE_SIZE / 2 or\
                y > self.screen.height / 2 + SQUARE_SIZE / 2:
            return None
        if x < self.screen.width / 2 - SQUARE_SIZE * 2 or\
                x > self.screen.width / 2 + SQUARE_SIZE * 2:
            return None

        return (x - self.screen.width // 2) // SQUARE_SIZE + 2

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

        if self.promoteMenu:
            return

        x, y = pygame.mouse.get_pos()
        self._drawPiece(self.selectedPiece.symbol(), (x, y))

    def _drawPromoteMenu(self) -> None:
        if not self.promoteMenu:
            return

        posX = self.screen.width / 2 - SURFACE_PROMOTE_MENU_WHITE.width / 2
        posY = self.screen.height / 2 - SURFACE_PROMOTE_MENU_WHITE.height / 2
        self.screen.blit(SURFACE_PROMOTE_MENU_WHITE
                         if self.board.turn == chess.WHITE
                         else SURFACE_PROMOTE_MENU_BLACK,
                         (posX, posY))

        pieces = ["Q", "R", "B", "N"]\
                if self.promoteMenu[0] == chess.WHITE else ["q", "r", "b", "n"]
        [self.screen.blit(DICT_PIECES[p],
                          (posX + SQUARE_SIZE * (0.25 + i),
                           posY + SQUARE_SIZE * 0.25)) for (i, p) in enumerate(pieces)]

    def _drawTurnIndicator(self) -> None:
        if self.board.is_game_over():
            posX = self.screen.width / 2
            posY = self.screen.height / 2 - RESULT_HEIGHT / 2

            match self.board.result():
                case "1-0":
                    posX -= TEXT_WHITE_WINS.width / 2
                    self.screen.blit(TEXT_WHITE_WINS, (posX, posY))
                case "0-1":
                    posX -= TEXT_BLACK_WINS.width / 2
                    self.screen.blit(TEXT_BLACK_WINS, (posX, posY))
                case _:
                    posX -= TEXT_DRAW.width / 2
                    self.screen.blit(TEXT_DRAW, (posX, posY))
            return

        posX = self.screen.width / 2 + 4 * SQUARE_SIZE + TURN_INDICATOR_MARGIN
        posY = self.screen.height / 2 - TURN_INDICATOR_SIZE / 2
        if self.board.turn == chess.WHITE:
            posY += SQUARE_SIZE / 2
        else:
            posY -= SQUARE_SIZE / 2

        self.screen.blit(SURFACE_TURN_INDICATOR, [posX, posY])

    def _drawOverlay(self) -> None:
        if not self.board.is_game_over():
            return

        self.screen.blit(SURFACE_BOARD_OVERLAY,
                        [self.screen.width / 2 - 4 * SQUARE_SIZE,
                        self.screen.height / 2 - 4 * SQUARE_SIZE])

    def _setCursor(self) -> None:
        def setHand() -> None:
            pygame.mouse.set_cursor(pygame.Cursor(pygame.SYSTEM_CURSOR_HAND))

        def setArrow() -> None:
            pygame.mouse.set_cursor(pygame.Cursor(pygame.SYSTEM_CURSOR_ARROW))

        mousePos = pygame.mouse.get_pos()
        if mousePos[0] > EXIT_BUTTON_POSITION[0] and\
                mousePos[0] < EXIT_BUTTON_POSITION[0] + EXIT_BUTTON_SIZE and\
                mousePos[1] > EXIT_BUTTON_POSITION[1] and\
                mousePos[1] < EXIT_BUTTON_POSITION[1] + EXIT_BUTTON_SIZE:
            setHand()
            return

        if self.promoteMenu:
            if self._hoverPromotion() is None:
                setArrow()
            else:
                setHand()
            return

        if self.board.is_game_over():
            setArrow()
            return
        
        if self.selectedPiece and self.hoveredSquare:
            setHand()
            return

        if not self.selectedPiece and self.hoveredSquare\
                and self._getPieceAt(self.hoveredSquare):
            setHand()
            return

        setArrow()


def main() -> None:
    """The entry point. Launches the game, GUI, and starts sonifying."""

    App().mainloop().close()

if __name__ == "__main__":
    main()
