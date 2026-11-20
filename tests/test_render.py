"""Tests for render.py: the timing grid, mixing and WAV output."""

from yomama_beats import synth
from yomama_beats.pattern import parse
from yomama_beats.render import grid, mix, write_wav

HATS = parse("bpm: 120\nhat x . x . x . x .")


def test_grid_draws_straight_hits_evenly():
    """Straight hits land at even spacing on the fine grid."""
    assert grid(HATS).splitlines()[1] == "hat  x.......x.......x.......x......."


def test_mix_length_matches_bars():
    """The mix is as long as the bars asked for, plus a release tail."""
    samples = mix(HATS, bars=2)
    bar = 8 * 0.125
    assert len(samples) == int((2 * bar + 0.5) * synth.SAMPLE_RATE)


def test_write_wav(tmp_path):
    """A WAV file is written with audio in it."""
    path = write_wav(mix(HATS, bars=1), tmp_path / "hats.wav")
    assert path.stat().st_size > 44
