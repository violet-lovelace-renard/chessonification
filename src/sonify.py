"""
Sonification methods used by the program.

Usage:
    from sonify import Sonifier
"""

import chess
from pygame import midi
from constants import DICT_CHANNELS, DICT_INSTRUMENTS, DICT_PAWN_DRUMS, FRAMES_OF_EIGHTH
from knight_grammar import KnightMotif

def player_coordinates(square: chess.Square, color: chess.Color) -> tuple[int, int]:
    """Return column and row indexes (0–7) from the player's perspective."""
    column = chess.square_file(square)
    row = chess.square_rank(square)
    return (column, row) if color == chess.WHITE else (7 - column, 7 - row)

class Sonifier:
    """
    Class providing sonification methods.
    """

    def __init__(self) -> None:
        midi.init()

        self.ticks = 0
        self.step = -1
        self.active_notes = []
        self.knights = {}
        self.knight_schedule = []
        self.player = midi.Output(0)  # Device id 0 = the computer

        self.player.set_instrument(DICT_INSTRUMENTS["N"], DICT_CHANNELS["N"])
        self.player.set_instrument(DICT_INSTRUMENTS["n"], DICT_CHANNELS["n"])

    def move_knight(self, move: chess.Move, board: chess.Board) -> None:
        previous = self.knights.pop(move.from_square, None)
        move_count = previous.move_count + 1 if previous else 1
        dx = chess.square_file(move.to_square) - chess.square_file(move.from_square)
        dy = chess.square_rank(move.to_square) - chess.square_rank(move.from_square)
        # Geometric destinations, excluding squares occupied by friendly pieces.
        mobility = sum(1 for square in chess.SquareSet(chess.BB_KNIGHT_ATTACKS[move.to_square])
                       if not board.piece_at(square) or board.color_at(square) != chess.WHITE)
        self.knights[move.to_square] = KnightMotif(dx, dy, chess.square_file(move.to_square),
                                                  mobility, move_count=move_count)

    def tick(self, board: chess.Board) -> None:
        self.ticks += 1

        remaining = []
        for end_tick, pitch, channel in self.active_notes:
            if self.ticks >= end_tick:
                self.player.note_off(pitch, 0, channel)
            else:
                remaining.append((end_tick, pitch, channel))
        self.active_notes = remaining

        self.knights = {square: motif for square, motif in self.knights.items()
                        if board.piece_at(square) == chess.Piece(chess.KNIGHT, chess.WHITE)}
        sixteenth = FRAMES_OF_EIGHTH // 2
        measure_frame = (self.ticks - 1) % (sixteenth * 16)
        if measure_frame == 0:
            self.knight_schedule = []
            for square, motif in self.knights.items():
                self.knight_schedule.extend((square, *note) for note in motif.notes())
                motif.develop()
        if measure_frame % sixteenth == 0:
            for square, offset, duration, pitch, velocity in self.knight_schedule:
                if square in self.knights and offset == measure_frame // sixteenth:
                    channel = DICT_CHANNELS["N"]
                    self.player.note_on(pitch, velocity, channel)
                    self.active_notes.append((self.ticks + max(1, duration * sixteenth - 1), pitch, channel))

        if (self.ticks - 1) % FRAMES_OF_EIGHTH == 0:
            self.step = (self.step + 1) % 8
            for square in board.pieces(chess.PAWN, chess.WHITE):
                column, row = player_coordinates(square, chess.WHITE)
                drum = DICT_PAWN_DRUMS.get(row + 1)
                if column == self.step and drum is not None:
                    channel = DICT_CHANNELS["P"]
                    self.player.note_on(drum, 100, channel)
                    self.active_notes.append((self.ticks + 6, drum, channel))
