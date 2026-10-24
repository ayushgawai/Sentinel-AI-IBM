"""On-screen 911 conversation for demo recordings. No phone is dialed.

Copied from the recorded call in sentinel_old_demo.mp4, word for word. The opening keeps that call's timing (seconds after the
call connects). Later lines are keyed to the clip second the camera wall is
showing, so each "they have moved" update lands on the camera handoff.
Sentinel's counts and weapons are scene.answer at the second they are said,
the same wording as the recording, so they always match the picture.
"""

from __future__ import annotations

from typing import Callable, Union

from . import scene

WPM = 240  # fastest line in the recorded call (Sentinel TTS)
PLACE = "MacQuarrie Hall"
# Clip second the old recording connected at (its first update fell on the
# 60 s handoff 27.7 s in). Used when there is no clip clock.
DEFAULT_START_CLIP = 32.3

Text = Union[str, Callable[[float], str]]


def answer(question: str, fallback: str) -> Callable[[float], str]:
    """Sentinel's answer to `question` at clip second t, from the scene script."""
    return lambda t: scene.answer(question, t) or fallback


# (seconds after the call connects, speaker, text): video 22.48 s is 0.
OPENING: list[tuple[float, str, Text]] = [
    (0.00, "sentinel", "Hi, this is Sentinel AI at San Jose State."),
    (3.12, "sentinel", f"I'm reporting armed people inside {PLACE}, One Washington Square."),
    (7.62, "dispatcher", "911, what's your emergency?"),
    (10.70, "sentinel", "One moment."),
    (11.50, "sentinel", f"Armed people inside {PLACE} at San Jose State University."),
    (16.20, "sentinel", answer("What weapons do they have?", "I see handguns and a knife in the ground-floor lobby.")),
    (19.02, "dispatcher", "Okay, how many people do you see?"),
    (21.58, "sentinel", "Give me a moment."),
    (23.14, "sentinel", answer("How many people do you see?", "Eight people in the ground-floor lobby; six of them armed.")),
]

# (clip second, speaker, text). The 117 s exchange keeps the old call's
# spacing before its update.
ON_CLIP: list[tuple[float, str, Text]] = [
    (59.0, "sentinel", "One moment."),
    (105.0, "dispatcher", "Okay, what weapons do they have?"),
    (106.6, "sentinel", "Let me check that."),
    (107.6, "sentinel", answer("What weapons do they have?", "I see a handgun and a rifle in the east corridor on the ground floor.")),
    (113.0, "dispatcher", "Where are they now?"),
    (114.6, "sentinel", "They're in the east corridor on the ground floor."),
] + [(float(t), "sentinel", scene.update_line(a, b)) for t, a, b in scene.moves(10_000)]
ON_CLIP.sort(key=lambda line: line[0])


def speak_s(text: str) -> float:
    """Seconds to speak `text` at WPM. One word is the minimum."""
    return max(1, len(text.split())) * 60.0 / WPM


def schedule(start_clip: float) -> list[tuple[float, str, str]]:
    """Every line as seconds after the call connects at clip `start_clip`.

    Clip lines already behind the wall are dropped. A line never starts
    before the previous one is spoken, so a late dispatch slides them.
    """
    # ponytail: assumes the wall plays in real time from start_clip; read the clock per line if it ever pauses.
    if start_clip < 1:
        start_clip = DEFAULT_START_CLIP
    lines = OPENING + [(t - start_clip, who, text) for t, who, text in ON_CLIP if t > start_clip]
    lines.sort(key=lambda line: line[0])
    out: list[tuple[float, str, str]] = []
    free = 0.0
    for at_s, who, text in lines:
        at_s = round(max(at_s, free), 3)
        said = text if isinstance(text, str) else text(start_clip + at_s)
        out.append((at_s, who, said))
        free = at_s + speak_s(said)
    return out


DEMO_CALL = schedule(DEFAULT_START_CLIP)
DURATION = round(DEMO_CALL[-1][0] + speak_s(DEMO_CALL[-1][2]), 3)


def _check() -> None:
    banned = ("simulat", "psap", "deterministic", "never emergency", "never-emergency", "ibm")
    for start in (0.0, 2.0, 8.0, DEFAULT_START_CLIP, 50.0, 110.0, 331.5):
        lines = schedule(start)
        blob = " ".join(text for _, _, text in lines).lower()
        assert PLACE.lower() in blob and not any(word in blob for word in banned)
        assert lines[0] == OPENING[0], lines[0]
        for (a, _, text), (b, _, _) in zip(lines, lines[1:]):
            assert b + 0.01 >= a + speak_s(text), (start, a, b, text)
    # Updates land on the handoff second when dispatch is on time.
    t_of = {text: at_s + DEFAULT_START_CLIP for at_s, _, text in DEMO_CALL}
    for t, a, b in scene.moves(10_000):
        assert abs(t_of[scene.update_line(a, b)] - t) < 0.01, (t, a, b)
    # Same wording as the recording, numbers from the footage at that second.
    assert scene.answer("What weapons do they have?", 24) == "I see four handguns and one knife in the ground-floor lobby."
    assert scene.answer("What weapons do they have?", 107.6) == "I see one handgun and one rifle in the east corridor on the ground floor."
    assert scene.answer("How many people do you see?", 31).startswith("Eight people in the ground-floor lobby;")
    assert len(schedule(331.5)) == len(OPENING)  # past the last handoff: opening only


if __name__ == "__main__":
    _check()
    for start in (8.0, DEFAULT_START_CLIP):
        print(f"--- call connects at clip {start}s")
        for at_s, speaker, text in schedule(start):
            print(f"{at_s:7.2f}s  clip {at_s + start:6.1f}  {speaker:10}  {text}")
    print(f"demo call {DURATION:.1f}s OK")
