"""The drum kit: one synthesized voice per track name."""

from . import synth

KIT = {
    "kick": synth.kick,
    "snare": synth.snare,
    "hat": synth.hat,
}


def voice(track: str):
    """The synth function for a track name; names the kit's drums if unknown."""
    try:
        return KIT[track]
    except KeyError:
        known = ", ".join(sorted(KIT))
        raise KeyError(f"no drum called {track!r} (the kit has: {known})") from None
