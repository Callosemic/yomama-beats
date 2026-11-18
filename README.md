# Yomama Beats

A tiny drum machine in plain Python. It is also the demo repo for
[inSetu](https://github.com/Callosemic/insetu): the clips and tutorials patch it,
so it is always a little unfinished on purpose.

Patterns are text grids, one row per drum, one cell per sixteenth note:

```
bpm: 90
swing: 0.0

kick   x . . . . . . x . . x . . . . .
snare  . . . . x . . . . . . . x . . .
hat    x x x x x x x x x x x x x x x x
```

## Use it

No dependencies beyond the standard library.

```
python -m yomama_beats play boom_bap          # hear it
python -m yomama_beats show boom_bap          # see it
python -m yomama_beats play boom_bap --bpm 95 --swing 0.3
python -m yomama_beats play boom_bap --out beat.wav
```

`play` uses your system's player (`afplay`, `aplay`, `paplay` or `ffplay`),
or saves a WAV if it finds none. `show` draws each hit where it really
falls in time, so swing shows up as uneven spacing.

## Tests

```
pip install -e ".[test]"
pytest
```

## License

MIT. See [LICENSE](LICENSE).
