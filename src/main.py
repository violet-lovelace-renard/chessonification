"""
Entry point for the chessonification program.

Usage:
    python main.py
"""

from collections.abc import Callable

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

        self.keyMap: dict[int, Callable[[], None]] = {
            pygame.K_w: self.cursor.moveUp,
            pygame.K_s: self.cursor.moveDown,
            pygame.K_a: self.cursor.moveLeft,
            pygame.K_d: self.cursor.moveRight,
            pygame.K_o: self.handleConfirm,
            pygame.K_p: self.handleCancel
        }
        self.holdableKeys = [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]
        self.keyHeldTicks: int | None = None
        self.keyHeld: int | None = None

        self.inMenu = False

    def mainloop(self) -> App:
        """
        Run the app. Blocks until the app is quit (e.g., by clicking the "X"
        close window button). Returns `self` for method chaining.
        """

        self.running = True
        while self.running:
            self.handleEvents()
            self.render()
    
            pygame.display.flip()
            self.clock.tick(60)

        return self

    def handleEvents(self) -> None:
        """Handle controls and OS-level app interactions."""
        
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.running = False
                    return
                
                case pygame.KEYDOWN:
                    k: int = event.key
                    if k in self.keyMap:
                        self.keyMap[k]()

                        if k in self.holdableKeys:
                            self.keyHeld = k
                            self.keyHeldTicks = 0

                case pygame.KEYUP:
                    k: int = event.key
                    if k == self.keyHeld:
                        self.keyHeld = None
                        self.keyHeldTicks = None

        # Handle holding keys down (repeated action)
        if self.keyHeld is not None and self.keyHeldTicks is not None:
            self.keyHeldTicks += 1
            ticks = self.keyHeldTicks - KEY_REPEAT_MINIMUM
            if ticks > 0 and ticks % KEY_REPEAT_PERIOD == 0:
                self.keyMap[self.keyHeld]()

    def handleConfirm(self) -> None:
        """
        Handle 'O' button press, which usually means to initiate or confirm
        some action.
        """

        if self.inMenu:
            self.inMenu = False

        else:
            self.inMenu = True

    def handleCancel(self) -> None:
        """
        Handle 'P' button press, which usually means to cancel the currently
        selected action.
        """

        if self.inMenu:
            self.inMenu = False

    def _pointOfCoords(self, row: int, col: int) -> tuple[float, float]:
        return (self.screen.width // 2 + (col - 4) * SQUARE_SIZE,
                self.screen.height // 2 + (row - 4) * SQUARE_SIZE)

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

        if self.inMenu:
            self.cursor.drawMenuCursor()
        else:
            self.cursor.drawCursor()

    def close(self) -> None:
        """Frees resources held by this app instance."""

        pygame.quit()

    class Cursor:
        def __init__(self, appInstance: App) -> None:
            self.appInstance = appInstance
            self.menuIndex = 0

            self.row = 0
            self.col = 0

        def moveUp(self) -> None:
            if self.appInstance.inMenu:
                self.menuIndex = (self.menuIndex + 1) % MENU_OPTIONS
            else:
                if self.row > 0:
                    self.row -= 1

        def moveDown(self) -> None:
            if self.appInstance.inMenu:
                self.menuIndex = (self.menuIndex - 1) % MENU_OPTIONS
            else:
                if self.row < 8 - 1:
                    self.row += 1

        def moveLeft(self) -> None:
            if not self.appInstance.inMenu and self.col > 0:
                self.col -= 1

        def moveRight(self) -> None:
            if not self.appInstance.inMenu and self.col < 8 - 1:
                self.col += 1

        def drawCursor(self) -> None:
            """Draw cursor to the chessboard (menu off)."""

            nwX, nwY = self.appInstance._pointOfCoords(self.row, self.col)
            nwX, nwY = nwX - CURSOR_OUTSET, nwY - CURSOR_OUTSET
            otherSide = SQUARE_SIZE - CURSOR_SIZE + 2 * CURSOR_OUTSET

            screen = self.appInstance.screen
            screen.blit(SURFACE_CURSOR_NW, (nwX,             nwY))
            screen.blit(SURFACE_CURSOR_NE, (nwX + otherSide, nwY))
            screen.blit(SURFACE_CURSOR_SE, (nwX + otherSide, nwY + otherSide))
            screen.blit(SURFACE_CURSOR_SW, (nwX,             nwY + otherSide))

        def drawMenuCursor(self) -> None:
            """Draw selector to the screen (menu on)."""

            point = self.appInstance._pointOfCoords(self.row, self.col)
            adjusted = [point[0] + SQUARE_SIZE - SELECTOR_SIZE,
                        point[1] + SQUARE_SIZE / 2 - SELECTOR_SIZE]
            self.appInstance.screen.blit(SURFACE_SELECTOR, adjusted)


def main() -> None:
    """The entry point. Launches the game, GUI, and starts sonifying."""

    App().mainloop().close()

if __name__ == "__main__":
    main()
