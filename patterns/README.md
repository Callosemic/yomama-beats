---
description: Drum patterns as text grids, one row per drum and one cell per sixteenth note.
---

# Patterns

One file per pattern. Settings first, then one row per drum:

```
bpm: 90
swing: 0.0

kick   x . . . . . . x . . x . . . . .
```

`x` is a hit, `.` a rest. Lines starting with `#` are comments. Play one
with `python -m yomama_beats play <name>`.
