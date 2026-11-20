"""Tests for pattern.py: parsing, writing and rejecting pattern files."""

import pytest

from yomama_beats.pattern import PatternError, dump, parse

BOOM_BAP = """
# boom bap
bpm: 90
swing: 0.0

kick   x . . . . . . x . . x . . . . .
snare  . . . . x . . . . . . . x . . .
"""


def test_parse_reads_settings_and_tracks():
    """Settings and track rows are read from the grid."""
    p = parse(BOOM_BAP)
    assert p.bpm == 90
    assert p.steps == 16
    assert p.tracks["snare"][4] is True
    assert p.tracks["snare"][5] is False


def test_dump_round_trips():
    """Writing a pattern and reading it back gives the same tracks."""
    p = parse(BOOM_BAP)
    assert parse(dump(p)).tracks == p.tracks


def test_rejects_unknown_cells():
    """Cells other than x and . are an error."""
    with pytest.raises(PatternError):
        parse("kick x o x .")
