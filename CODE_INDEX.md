# Yomama Beats Code Index

This index serves as the architectural map. It outlines the core directories and their operational purpose to maintain a clear mental model of the ecosystem, preventing cognitive overload and logic drift.

```text
yomama-beats/
├── CODE_INDEX.md                   # Yomama Beats Code Index
├── README.md                       # Yomama Beats
├── patterns/                       # Drum patterns as text grids, one row per drum and one cell per sixteenth note.
│   ├── README.md                   # Drum patterns as text grids, one row per drum and one cell per sixteenth note.
│   ├── boom_bap.txt                # [comment required]
│   └── four_on_the_floor.txt       # [comment required]
├── pyproject.toml                  # A tiny drum machine, and the demo repo for inSetu.
├── tests/                          # The pytest suite for Yomama Beats.
│   ├── README.md                   # The pytest suite for Yomama Beats.
│   ├── test_pattern.py             # Tests for pattern.py: parsing, writing and rejecting pattern files.
│   │   ├── def test_parse_reads_settings_and_tracks() # Settings and track rows are read from the grid.
│   │   ├── def test_dump_round_trips() # Writing a pattern and reading it back gives the same tracks.
│   │   └── def test_rejects_unknown_cells() # Any cell that is not a hit or a rest is an error.
│   ├── test_render.py              # Tests for render.py: the timing grid, mixing and WAV output.
│   │   ├── def test_grid_draws_straight_hits_evenly() # Straight hits land at even spacing on the fine grid.
│   │   ├── def test_mix_length_matches_bars() # The mix is as long as the bars asked for, plus a release tail.
│   │   └── def test_write_wav(tmp_path) # A WAV file is written with audio in it.
│   └── test_tempo.py               # Tests for tempo.py: step lengths, straight time and swing.
│       ├── def test_step_length_at_120_bpm() # A sixteenth at 120 bpm lasts 0.125 s.
│       ├── def test_straight_time_is_even() # Without swing, steps are evenly spaced.
│       └── def test_swing_only_moves_offbeats() # Swing pushes the off-beats late and leaves the on-beats alone.
└── yomama_beats/                   # Yomama Beats: a tiny drum machine, and the demo repo for inSetu.
    ├── __init__.py                 # Yomama Beats: a tiny drum machine, and the demo repo for inSetu.
    ├── __main__.py                 # Run the CLI with `python -m yomama_beats`.
    ├── cli.py                      # yomama-beats show | play
    │   ├── def find_pattern(name)  # Resolve a pattern name or path to a file, looking in ./patterns too.
    │   ├── def play_file(path)     # Play a WAV with the first system player found; False if there is none.
    │   └── def main(argv)          # Entry point for `yomama-beats show|play`.
    ├── kit.py                      # The drum kit: one synthesized voice per track name.
    │   └── def voice(track)        # The synth function for a track name; names the kit's drums if unknown.
    ├── pattern.py                  # Patterns: drum parts written as text grids.
    │   ├── class Pattern           # A drum pattern: tempo, swing, and one row of hits per track.
    │   ├── class PatternError(ValueError) # A pattern file that can't be read.
    │   ├── def parse(text, name)   # Read a pattern from its text-grid form.
    │   ├── def load(path)          # Read a pattern file; the file name becomes the pattern name.
    │   └── def dump(pattern)       # Write a pattern back out as a text grid.
    ├── render.py                   # Turning a pattern into something you can see or hear.
    │   ├── def grid(pattern, bpm, swing) # Draw the pattern on a fine time grid, so swing shows as uneven spacing.
    │   ├── def mix(pattern, bars, bpm, swing) # Render `bars` loops of the pattern to samples.
    │   └── def write_wav(samples, path) # Save samples as a 16-bit mono WAV, normalized to avoid clipping.
    ├── synth.py                    # Drum sounds made from math alone: no samples, no dependencies.
    │   ├── def kick(length)        # A sine wave that drops in pitch, 808 style.
    │   ├── def snare(length)       # A noise burst over a short tone.
    │   └── def hat(length)         # Very short noise, with the low end taken off.
    └── tempo.py                    # Timing: where each sixteenth note falls, in seconds.
        ├── def step_length(bpm)    # Length of one sixteenth note at `bpm`.
        └── def step_times(steps, bpm, swing) # Start time of each step.
```
