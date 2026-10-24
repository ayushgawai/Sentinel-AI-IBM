"""Fixed on-screen 911 call for the three-camera demo.

The visual demo has one known 339.8-second camera timeline. Keeping this
transcript on that same clock makes the dialogue repeatable and prevents
frame-level detector changes from changing what the call says.
"""

from __future__ import annotations

# The final video frame is at 339.8 seconds. Entries are absolute seconds
# from scenario start and coincide with the camera handoffs in the media.
DURATION = 339.8
DEMO_CALL: list[tuple[float, str, str]] = [
    (0.0, "dispatcher", "911, what's your emergency?"),
    (3.5, "sentinel", "Hi, this is Sentinel AI at San Jose State."),
    (8.5, "sentinel", "I'm reporting armed people inside MacQuarrie Hall, One Washington Square."),
    (15.0, "sentinel", "One moment."),
    (18.5, "sentinel", "Armed people inside MacQuarrie Hall at San Jose State University."),
    (24.5, "sentinel", "I see four handguns and one knife in the ground-floor lobby."),
    (32.0, "dispatcher", "Okay, how many people do you see?"),
    (35.5, "sentinel", "Give me a moment."),
    (39.5, "sentinel", "Seven of them appear armed."),
    (60.0, "sentinel", "Update: they have moved from the ground-floor lobby into the east corridor on the ground floor."),
    (117.0, "sentinel", "Update: they have moved from the east corridor into the west corridor."),
    (216.6, "sentinel", "Update: they are returning through the west corridor."),
    (230.2, "sentinel", "Update: they have moved from the west corridor into the east corridor."),
    (267.8, "sentinel", "Update: they have returned to the ground-floor lobby."),
]


def line_waits() -> list[tuple[float, str, str]]:
    """Seconds to wait after the preceding transcript event."""
    waits: list[tuple[float, str, str]] = []
    previous = 0.0
    for index, (at_s, speaker, text) in enumerate(DEMO_CALL):
        waits.append((0.0 if index == 0 else round(at_s - previous, 3), speaker, text))
        previous = at_s
    return waits


def _check() -> None:
    banned = ("ibm", "simulat", "psap", "deterministic", "never emergency", "never-emergency")
    assert DURATION == 339.8
    assert DEMO_CALL[0] == (0.0, "dispatcher", "911, what's your emergency?")
    assert DEMO_CALL[-1][0] < DURATION
    assert all(next_at > at_s for (at_s, _, _), (next_at, _, _) in zip(DEMO_CALL, DEMO_CALL[1:]))
    blob = " ".join(text for _, _, text in DEMO_CALL).lower()
    assert not any(word in blob for word in banned)
    assert (60.0, "sentinel", "Update: they have moved from the ground-floor lobby into the east corridor on the ground floor.") in DEMO_CALL
    assert (117.0, "sentinel", "Update: they have moved from the east corridor into the west corridor.") in DEMO_CALL
    assert (230.2, "sentinel", "Update: they have moved from the west corridor into the east corridor.") in DEMO_CALL
    assert (267.8, "sentinel", "Update: they have returned to the ground-floor lobby.") in DEMO_CALL


if __name__ == "__main__":
    _check()
    for wait, speaker, text in line_waits():
        print(f"{wait:5.2f}s  {speaker:10}  {text}")
    print(f"demo timeline {DURATION:.1f}s OK")
