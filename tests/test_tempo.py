"""Tests for tempo.py: step lengths, straight time and swing."""

from yomama_beats.tempo import step_length, step_times


def test_step_length_at_120_bpm():
    """A sixteenth at 120 bpm lasts 0.125 s."""
    assert step_length(120) == 0.125


def test_straight_time_is_even():
    """Without swing, steps are evenly spaced."""
    times = step_times(4, bpm=120)
    assert times == [0.0, 0.125, 0.25, 0.375]


def test_swing_only_moves_offbeats():
    """Swing pushes the off-beats late and leaves the on-beats alone."""
    straight = step_times(16, bpm=120)
    swung = step_times(16, bpm=120, swing=0.5)
    for i, (s, w) in enumerate(zip(straight, swung)):
        if i % 2:
            assert w > s, f"off-beat {i} should be pushed late"
        else:
            assert w == s, f"on-beat {i} should not move"
