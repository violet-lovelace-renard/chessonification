import random
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from knight_grammar import Branch, KnightMotif, FAMILIES, MAX_DEPTH

class KnightGrammarTests(unittest.TestCase):
    def test_vectors_and_inversion(self):
        self.assertEqual(len(FAMILIES), 8)
        for (dx, dy), (family, sign) in FAMILIES.items():
            self.assertEqual(FAMILIES[-dx, -dy], (family, -sign))
            a = KnightMotif(dx, dy, 3, 8, random.Random(7))
            b = KnightMotif(-dx, -dy, 3, 8, random.Random(7))
            for _ in range(8):
                self.assertEqual([x[:2] for x in a.notes()], [x[:2] for x in b.notes()])
                a.develop(); b.develop()
                self.assertEqual([(l.interval, l.duration) for r in a.roots for l in r.leaves()],
                                 [(l.interval, l.duration) for r in b.roots for l in r.leaves()])

    def test_budget_depth_and_range(self):
        for seed in range(40):
            motif = KnightMotif(1, -2, 0, 8, random.Random(seed))
            for _ in range(30):
                notes = motif.notes()
                self.assertEqual(sum(n[1] for n in notes), 16)
                self.assertTrue(all(n[1] >= 1 and 55 <= n[2] <= 88 for n in notes))
                self.assertTrue(all(b.depth <= MAX_DEPTH for r in motif.roots for b in r.branches()))
                motif.develop()

    def test_expand_and_prune(self):
        motif = KnightMotif(1, 2, 0, 8, random.Random(4))
        other = motif.roots[1:]
        self.assertTrue(motif.roots[0].expand(motif.rng))
        self.assertEqual(motif.roots[1:], other)
        self.assertEqual(sum(b.duration for b in motif.roots[0].leaves()), 6)
        motif.roots[0].children = []
        self.assertEqual(len(motif.notes()), 4)

    def test_landing_notes_and_widening_range(self):
        for column, pitch in enumerate((60, 62, 64, 65, 67, 69, 71, 72)):
            self.assertEqual(KnightMotif(1, 2, column, 4).notes()[0][2], pitch)
        early = KnightMotif(2, 1, 0, 4, move_count=1)
        later = KnightMotif(2, 1, 0, 4, move_count=5)
        self.assertLess(max(n[2] for n in early.notes()), max(n[2] for n in later.notes()))

if __name__ == '__main__':
    unittest.main()
