"""yomama-beats show | play"""

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from . import pattern as patterns
from . import render

PLAYERS = (
    ["afplay"],
    ["aplay", "-q"],
    ["paplay"],
    ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet"],
)


def find_pattern(name: str) -> Path:
    candidates = [Path(name), Path("patterns") / f"{name}.txt",
                  Path(__file__).resolve().parent.parent / "patterns" / f"{name}.txt"]
    for path in candidates:
        if path.is_file():
            return path
    sys.exit(f"no pattern called {name!r} (looked in ./patterns)")


def play_file(path: Path) -> bool:
    for player in PLAYERS:
        if shutil.which(player[0]):
            subprocess.run([*player, str(path)], check=False)
            return True
    return False


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="yomama-beats")
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ("show", "play"):
        p = sub.add_parser(command)
        p.add_argument("pattern")
        p.add_argument("--bpm", type=float)
        p.add_argument("--swing", type=float)
        if command == "play":
            p.add_argument("--bars", type=int, default=2)
            p.add_argument("--out", help="save the WAV here instead of playing it")
    args = parser.parse_args(argv)

    beat = patterns.load(find_pattern(args.pattern))
    if args.command == "show":
        print(render.grid(beat, bpm=args.bpm, swing=args.swing))
        return

    samples = render.mix(beat, bars=args.bars, bpm=args.bpm, swing=args.swing)
    if args.out:
        print(render.write_wav(samples, args.out))
        return
    with tempfile.TemporaryDirectory() as tmp:
        path = render.write_wav(samples, Path(tmp) / f"{beat.name}.wav")
        if not play_file(path):
            saved = render.write_wav(samples, f"{beat.name}.wav")
            print(f"no audio player found; saved {saved}")


if __name__ == "__main__":
    main()
