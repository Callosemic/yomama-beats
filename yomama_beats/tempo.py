"""Timing: where each sixteenth note falls, in seconds."""


def step_length(bpm: float) -> float:
    """Length of one sixteenth note at `bpm`."""
    return 60 / bpm / 4


def step_times(steps: int, bpm: float, swing: float = 0.0) -> list[float]:
    """Start time of each step.

    Swing pushes the off-beat sixteenths late by `swing` of a step
    (0.0 is straight, 0.5 is a heavy shuffle).
    """
    step = step_length(bpm)
    return [i * step + swing * step for i in range(steps)]
