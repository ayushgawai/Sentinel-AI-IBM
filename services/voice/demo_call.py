"""On-screen 911 conversation for demo recordings. No phone is dialed.

Each line is held for the time it takes to say it at about 150 words per
minute. A change of speaker adds one second of silence before the next line.
"""

from __future__ import annotations

WPM = 120
BEAT_S = 1.8
PLACE = "Spartan Complex"

# (speaker, text). Timestamps are derived; do not hand-tune them.
_LINES: list[tuple[str, str]] = [
    ("dispatcher", "911, what's your emergency?"),
    ("sentinel", f"This is Sentinel AI, the camera system at {PLACE}. I see armed people in the ground-floor lobby."),
    ("dispatcher", "Okay, how many people do you see?"),
    ("sentinel", "Eight people are visible. Six appear armed."),
    ("dispatcher", "What weapons can you see?"),
    ("sentinel", "I can see handguns, a knife, and a long firearm."),
    ("dispatcher", "Okay. Keep monitoring them and tell me if they move."),
    ("sentinel", "Understood."),
]


def speak_s(text: str) -> float:
    """Seconds to speak `text` at WPM. One word is the minimum."""
    words = [w for w in text.split() if w]
    return max(1, len(words)) * 60.0 / WPM


def paced(lines: list[tuple[str, str]]) -> list[tuple[float, str, str]]:
    """Absolute start time for each line. The next line starts only after this one is spoken."""
    t = 0.0
    out: list[tuple[float, str, str]] = []
    prev = ""
    for speaker, text in lines:
        if prev and speaker != prev:
            t += BEAT_S
        out.append((round(t, 3), speaker, text))
        t += speak_s(text)
        prev = speaker
    return out


DEMO_CALL: list[tuple[float, str, str]] = paced(_LINES)
DURATION = round(DEMO_CALL[-1][0] + speak_s(DEMO_CALL[-1][2]), 3)


def line_waits() -> list[tuple[float, str, str]]:
    """Seconds the player waits after the previous line before showing this one."""
    waits: list[tuple[float, str, str]] = []
    prev_t = 0.0
    for i, (at_s, speaker, text) in enumerate(DEMO_CALL):
        waits.append((0.0 if i == 0 else round(at_s - prev_t, 3), speaker, text))
        prev_t = at_s
    return waits


def _check() -> None:
    banned = ("simulat", "psap", "deterministic", "never emergency", "never-emergency", "ibm")
    assert DEMO_CALL[0][0] == 0.0
    assert DEMO_CALL[-1][0] < DURATION
    blob = " ".join(text for _, _, text in DEMO_CALL).lower()
    assert PLACE.lower() in blob
    assert not any(word in blob for word in banned)
    prev_t, prev_speaker, prev_text = DEMO_CALL[0]
    for at_s, speaker, text in DEMO_CALL[1:]:
        gap = at_s - prev_t
        need = speak_s(prev_text) + (BEAT_S if speaker != prev_speaker else 0.0)
        assert gap + 1e-6 >= need, (gap, need, prev_text)
        assert at_s > prev_t
        prev_t, prev_speaker, prev_text = at_s, speaker, text


if __name__ == "__main__":
    _check()
    for wait, speaker, text in line_waits():
        print(f"{wait:5.2f}s  {speaker:10}  {text}")
    print(f"demo call {DURATION:.1f}s OK")
