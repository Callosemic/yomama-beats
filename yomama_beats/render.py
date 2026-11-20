"""Turning a pattern into something you can see or hear."""

import struct
import wave
from pathlib import Path

from . import kit, synth, tempo
from .pattern import Pattern

COLUMNS_PER_STEP = 4


def grid(pattern: Pattern, bpm: float | None = None, swing: float | None = None) -> str:
    """Draw the pattern on a fine time grid, so swing shows as uneven spacing.

    Each sixteenth note gets COLUMNS_PER_STEP columns; a hit is drawn
    where its start time actually falls.
    """
    bpm = pattern.bpm if bpm is None else bpm
    swing = pattern.swing if swing is None else swing
    step = tempo.step_length(bpm)
    times = tempo.step_times(pattern.steps, bpm, swing)
    width = pattern.steps * COLUMNS_PER_STEP
    label = max((len(t) for t in pattern.tracks), default=0)

    ruler = [" "] * width
    for beat in range(pattern.steps // 4):
        ruler[beat * 4 * COLUMNS_PER_STEP] = str(beat + 1)
    lines = [" " * label + "  " + "".join(ruler).rstrip()]

    for track, cells in pattern.tracks.items():
        row = ["."] * width
        for i, hit in enumerate(cells):
            if hit:
                column = round(times[i] / step * COLUMNS_PER_STEP)
                if column < width:
                    row[column] = "x"
        lines.append(f"{track.ljust(label)}  {''.join(row)}")
    return "\n".join(lines)


def mix(pattern: Pattern, bars: int = 2, bpm: float | None = None,
        swing: float | None = None) -> list[float]:
    """Render `bars` loops of the pattern to samples."""
    bpm = pattern.bpm if bpm is None else bpm
    swing = pattern.swing if swing is None else swing
    bar_length = tempo.step_length(bpm) * pattern.steps
    times = tempo.step_times(pattern.steps, bpm, swing)
    out = [0.0] * int((bar_length * bars + 0.5) * synth.SAMPLE_RATE)

    for track, cells in pattern.tracks.items():
        sound = kit.voice(track)()
        for bar in range(bars):
            for i, hit in enumerate(cells):
                if not hit:
                    continue
                start = int((bar * bar_length + times[i]) * synth.SAMPLE_RATE)
                for n, sample in enumerate(sound[: len(out) - start]):
                    out[start + n] += sample
    return out


def write_wav(samples: list[float], path: str | Path) -> Path:
    """Save samples as a 16-bit mono WAV, normalized to avoid clipping."""
    path = Path(path)
    peak = max((abs(s) for s in samples), default=0.0) or 1.0
    scale = 0.9 * 32767 / max(peak, 1.0)
    frames = b"".join(struct.pack("<h", int(s * scale)) for s in samples)
    with wave.open(str(path), "wb") as out:
        out.setnchannels(1)
        out.setsampwidth(2)
        out.setframerate(synth.SAMPLE_RATE)
        out.writeframes(frames)
    return path
