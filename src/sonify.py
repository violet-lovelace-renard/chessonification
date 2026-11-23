"""
Sonification methods used by the program.

Usage:
    from sonify import Sonifier
"""

import music21 as m21
import pygame
from pygame import midi

class Sonifier:
    """
    Class providing sonification methods.
    """

    def __init__(self) -> None:
        midi.init()

        self.ticks = 0
        self.player = midi.Output(0)  # Device id 0 = the computer

    def tick(self) -> None:
        self.ticks += 1

        if self.ticks % 60 == 0:
            self.player.note_on(60, 127, 1)
        elif self.ticks % 60 == 30:
            self.player.note_off(60, 127, 1)
