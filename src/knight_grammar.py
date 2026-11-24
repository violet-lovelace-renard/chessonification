"""Persistent, bounded knight melodies. Durations are sixteenth notes."""
import random
from dataclasses import dataclass, field

FAMILIES = {
    (1, 2): ('RISE', 1), (-1, -2): ('RISE', -1),
    (2, 1): ('LEAP_RISE', 1), (-2, -1): ('LEAP_RISE', -1),
    (2, -1): ('EARLY_ARCH', 1), (-2, 1): ('EARLY_ARCH', -1),
    (1, -2): ('ARCH', 1), (-1, 2): ('ARCH', -1),
}
# Each cell starts with a contour interval; subdivisions develop that interval.
CONTOURS = {'RISE': (1, 1, 1, 1), 'LEAP_RISE': (3, 1, 3, 1),
            'EARLY_ARCH': (3, -1, -1, -1), 'ARCH': (1, 1, -1, -1)}
SCALE = (0, 2, 4, 5, 7, 9, 11)
MAX_DEPTH = 3
EXPAND_BASE = .1
EXPAND_PER_MOVE = .1
DEVELOP_MEASURES = 4
PRUNE_MEASURES = 3
INITIAL_RANGE = 2  # Scale degrees on either side of the landing note.
MAX_RANGE = 7

@dataclass
class Branch:
    duration: int
    interval: int
    depth: int = 0
    children: list = field(default_factory=list)

    def leaves(self):
        if not self.children:
            return [self]
        return [leaf for child in self.children for leaf in child.leaves()]

    def branches(self):
        return [self] + [branch for child in self.children for branch in child.branches()]

    def expand(self, rng):
        if self.children or self.duration < 2 or self.depth >= MAX_DEPTH:
            return False
        if self.duration == 6:
            durations = rng.choice(((4, 2), (2, 2, 2)))
        else:
            durations = (self.duration // 2, self.duration - self.duration // 2)
        # End on the original interval, preserving the branch's melodic goal.
        middle = rng.choice((-1, 1))
        intervals = [middle] + [0] * (len(durations) - 2) + [self.interval - middle]
        self.children = [Branch(d, i, self.depth + 1) for d, i in zip(durations, intervals)]
        return True

class KnightMotif:
    def __init__(self, dx, dy, start_degree, mobility, rng=None, move_count=1):
        self.family, self.inversion = FAMILIES[(dx, dy)]
        self.start_degree = start_degree
        self.mobility = mobility
        self.move_count = move_count
        self.rng = rng or random.Random()
        self.roots = [Branch(d, i) for d, i in zip((6, 2, 6, 2), CONTOURS[self.family])]
        self.measure = 0

    def develop(self):
        cycle = DEVELOP_MEASURES + PRUNE_MEASURES + 1
        phase = self.measure % cycle
        branches = [b for root in self.roots for b in root.branches()]
        if phase < DEVELOP_MEASURES:
            eligible = [b for b in branches if not b.children and b.duration >= 2 and b.depth < MAX_DEPTH]
            if eligible and self.rng.random() < EXPAND_BASE + EXPAND_PER_MOVE * self.mobility:
                self.rng.choice(eligible).expand(self.rng)
        elif phase < DEVELOP_MEASURES + PRUNE_MEASURES:
            eligible = [b for b in branches if b.children and all(not c.children for c in b.children)]
            if eligible:
                self.rng.choice(eligible).children = []
        else:
            for root in self.roots:
                root.children = []
        self.measure += 1

    def notes(self):
        """Return (sixteenth offset, duration, MIDI pitch, velocity)."""
        degree = self.start_degree
        offset = 0
        result = []
        for root in self.roots:
            for leaf in root.leaves():
                note_range = min(MAX_RANGE, INITIAL_RANGE + self.move_count - 1)
                bounded_degree = max(self.start_degree - note_range,
                                     min(self.start_degree + note_range, degree))
                octave, index = divmod(bounded_degree, 7)
                pitch = max(55, min(88, 60 + 12 * octave + SCALE[index]))
                result.append((offset, leaf.duration, pitch, 100 if offset in (0, 8) else 75))
                degree += leaf.interval * self.inversion
                offset += leaf.duration
        return result
