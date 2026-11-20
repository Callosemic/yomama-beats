"""Drum sounds made from math alone: no samples, no dependencies.

Each voice returns a list of floats in [-1, 1] at SAMPLE_RATE.
"""

import math
import random

SAMPLE_RATE = 22050


def _decay(n: int, length: int, curve: float = 6.0) -> float:
    """Exponential fade from 1 toward 0 over `length` samples."""
    return math.exp(-curve * n / length)


def kick(length: float = 0.35) -> list[float]:
    """A sine wave that drops in pitch, 808 style."""
    total = int(length * SAMPLE_RATE)
    out, phase = [], 0.0
    for n in range(total):
        freq = 45 + 110 * math.exp(-30 * n / SAMPLE_RATE)
        phase += 2 * math.pi * freq / SAMPLE_RATE
        out.append(math.sin(phase) * _decay(n, total, 5.0))
    return out


def snare(length: float = 0.18) -> list[float]:
    """A noise burst over a short tone."""
    rng = random.Random(7)
    total = int(length * SAMPLE_RATE)
    out = []
    for n in range(total):
        tone = math.sin(2 * math.pi * 185 * n / SAMPLE_RATE) * _decay(n, total, 12.0)
        noise = rng.uniform(-1, 1) * _decay(n, total, 7.0)
        out.append(0.4 * tone + 0.6 * noise)
    return out


def hat(length: float = 0.05) -> list[float]:
    """Very short noise, with the low end taken off."""
    rng = random.Random(11)
    total = int(length * SAMPLE_RATE)
    out, last = [], 0.0
    for n in range(total):
        noise = rng.uniform(-1, 1)
        out.append((noise - last) * 0.35 * _decay(n, total, 8.0))
        last = noise
    return out
