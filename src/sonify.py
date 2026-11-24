"""
Sonification methods used by the program.

Usage:
    from sonify import Sonifier
"""

import chess
import music21 as m21
from pygame import midi

from constants import *

class Sonifier:
    """
    Class providing sonification methods.
    """

    def __init__(self, board: chess.Board) -> None:
        midi.init()

        self.ticks = 0
        self.player = midi.Output(0)  # Device id 0 = the computer
        self.board = board
        self.measure, self.measureEvents = self._generateMeasure()

        for p in LIST_PIECES:
            self.player.set_instrument(DICT_INSTRUMENTS[p], DICT_CHANNELS[p])

    def tick(self) -> None:
        # Determine which note in the measure to play
        sixteenth = self.ticks // FRAMES_OF_16TH
        subsixteenth = self.ticks % FRAMES_OF_16TH

        if subsixteenth == 0:
            for event in self.measureEvents[sixteenth]:
                channel = DICT_CHANNELS[LIST_PIECES[event.pieceIndex]]
                if event.isOnset:
                    self.player.note_on(event.pitch, 127, channel)
                else:
                    self.player.note_off(event.pitch, 127, channel)

        self.ticks += 1

        # When done with this measure, end all notes and generate the next one
        if self.ticks == FRAMES_OF_16TH * 16:
            for event in self.measureEvents[-1]:
                channel = DICT_CHANNELS[LIST_PIECES[event.pieceIndex]]
                self.player.note_off(event.pitch, 127, channel)

            self.ticks = 0
            self.measure, self.measureEvents = self._generateMeasure()

    def _generateMeasure(self) -> tuple[Measure, list[list[Sonifier.Event]]]:
        m = self.Measure()
        for i in range(8):
            m.addNote(5, self.Note(42, i * 2, 1))
        return m, m.asEvents()

    class Note:
        """Always exists in the context of a particular instrument."""

        def __init__(self, pitch: int, onset: int,  duration: int) -> None:
            self.pitch = pitch
            self.onset = onset
            self.duration = duration

    class Event:
        """Always exists in the context of a particular time."""

        def __init__(self, pieceIndex: int, pitch: int, isOnset: bool) -> None:
            self.pieceIndex = pieceIndex
            self.pitch = pitch
            self.isOnset = isOnset

    class Measure:
        """Stores one measure of music, quantized to 16th notes."""

        def __init__(self) -> None:
            self.notesPerPiece: list[list[Sonifier.Note]] = [[] for _ in range(PIECES)]

        def addNote(self, pieceIndex: int, note: Sonifier.Note) -> None:
            self.notesPerPiece[pieceIndex].append(note)

        def asEvents(self) -> list[list[Sonifier.Event]]:
            """
            Return this Measure as a list of MIDI-style events for each time
            point in the measure. There is a 17th for the end of the measure.
            """

            result: list[list[Sonifier.Event]] = [[] for _ in range(17)]
            for piece in range(PIECES):
                for note in self.notesPerPiece[piece]:
                    result[note.onset].append(
                            Sonifier.Event(piece, note.pitch, isOnset=True))
                    result[note.onset + note.duration].append(
                            Sonifier.Event(piece, note.pitch, isOnset=False))
            return result
