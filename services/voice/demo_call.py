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
    (3.5, "sentinel", "Hi, this is Sentinel AI. I'm reporting armed people in the ground-floor lobby."),
    (11.0, "sentinel", "One moment."),
    (14.5, "sentinel", "I can see handguns, a knife, and a long firearm in the ground-floor lobby."),
    (22.5, "dispatcher", "Okay, how many people do you see?"),
    (26.0, "sentinel", "Give me a moment."),
    (30.0, "sentinel", "Eight people are visible. Six appear armed."),
    (60.0, "sentinel", "Update: They have moved into the east corridor."),
    (63.5, "dispatcher", "Copy. I have the east-corridor update."),
    (117.0, "sentinel", "Update: They have moved into the west corridor."),
    (120.5, "dispatcher", "Copy. I have the west-corridor update."),
    (216.6, "sentinel", "Update: They are turning back toward the east corridor."),
    (220.0, "dispatcher", "Copy. I have the change in direction."),
    (230.2, "sentinel", "Update: They have moved back into the east corridor."),
    (233.7, "dispatcher", "Copy. I have the east-corridor update."),
    (267.8, "sentinel", "Update: They have returned to the lobby."),
    (271.3, "dispatcher", "Copy. I have the lobby update."),
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
    assert (60.0, "sentinel", "Update: They have moved into the east corridor.") in DEMO_CALL
    assert (117.0, "sentinel", "Update: They have moved into the west corridor.") in DEMO_CALL
    assert (230.2, "sentinel", "Update: They have moved back into the east corridor.") in DEMO_CALL
    assert (267.8, "sentinel", "Update: They have returned to the lobby.") in DEMO_CALL


if __name__ == "__main__":
    _check()
    for wait, speaker, text in line_waits():
        print(f"{wait:5.2f}s  {speaker:10}  {text}")
    print(f"demo timeline {DURATION:.1f}s OK")
