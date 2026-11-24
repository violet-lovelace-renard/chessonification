"""Write an audible MIDI example: four contours, inversions, and development."""
import random
import struct
from pathlib import Path
from knight_grammar import KnightMotif


def variable(value):
    result = [value & 127]
    value >>= 7
    while value:
        result.insert(0, (value & 127) | 128)
        value >>= 7
    return bytes(result)


def main():
    events = [(0, bytes([0xC0, 40]))]
    vectors = [(1, 2), (2, 1), (2, -1), (1, -2)]
    motifs = [KnightMotif(dx * sign, dy * sign, 3, 8, random.Random(4))
              for dx, dy in vectors for sign in (1, -1)]
    evolving = KnightMotif(1, -2, 3, 8, random.Random(8))
    motifs += [evolving] * 9
    for measure, motif in enumerate(motifs):
        for offset, duration, pitch, velocity in motif.notes():
            start = (measure * 16 + offset) * 120
            events.append((start, bytes([0x90, pitch, velocity])))
            events.append((start + duration * 120 - 1, bytes([0x80, pitch, 0])))
        if motif is evolving:
            motif.develop()
    events.sort(key=lambda event: event[0])
    track = bytearray(b'\x00\xff\x51\x03\x0a\x2c\x2b')  # 90 BPM
    previous = 0
    for tick, data in events:
        track.extend(variable(tick - previous) + data)
        previous = tick
    track.extend(b'\x00\xff\x2f\x00')
    path = Path('knight_demo.mid')
    path.write_bytes(b'MThd' + struct.pack('>IHHH', 6, 0, 1, 480)
                     + b'MTrk' + struct.pack('>I', len(track)) + track)
    print(f'Wrote {path.resolve()}')

if __name__ == '__main__':
    main()
