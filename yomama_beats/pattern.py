"""Patterns: drum parts written as text grids.

A pattern file looks like this:

    # boom bap
    bpm: 90
    swing: 0.0

    kick   x . . . . . . x . . x . . . . .
    snare  . . . . x . . . . . . . x . . .
    hat    x . x . x . x . x . x . x . x .

Each row is one track: a name, then one cell per sixteenth note.
`x` is a hit and `.` is a rest. Lines starting with `#` are comments.
"""

from dataclasses import dataclass, field
from pathlib import Path

HIT = "x"
REST = "."


@dataclass
class Pattern:
    name: str
    bpm: float = 90.0
    swing: float = 0.0
    tracks: dict[str, list[bool]] = field(default_factory=dict)

    @property
    def steps(self) -> int:
        return max((len(cells) for cells in self.tracks.values()), default=0)


class PatternError(ValueError):
    pass


def parse(text: str, name: str = "untitled") -> Pattern:
    pattern = Pattern(name=name)
    for number, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip().lower()
            if key == "bpm":
                pattern.bpm = float(value)
            elif key == "swing":
                pattern.swing = float(value)
            else:
                raise PatternError(f"line {number}: unknown setting {key!r}")
            continue
        track, *cells = line.split()
        bad = [c for c in cells if c not in (HIT, REST)]
        if bad:
            raise PatternError(f"line {number}: {bad[0]!r} is not {HIT!r} or {REST!r}")
        pattern.tracks[track] = [c == HIT for c in cells]
    return pattern


def load(path: str | Path) -> Pattern:
    path = Path(path)
    return parse(path.read_text(), name=path.stem)


def dump(pattern: Pattern) -> str:
    width = max((len(t) for t in pattern.tracks), default=0)
    lines = [f"bpm: {pattern.bpm:g}", f"swing: {pattern.swing:g}", ""]
    for track, cells in pattern.tracks.items():
        grid = " ".join(HIT if hit else REST for hit in cells)
        lines.append(f"{track.ljust(width)}  {grid}")
    return "\n".join(lines) + "\n"
