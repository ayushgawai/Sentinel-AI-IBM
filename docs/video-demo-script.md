# IBM Sentinel AI recording plan

Record the live three-camera console. Read the spoken script on that recording. This file is the script to approve before anyone edits the picture.

Spoken timecodes are the camera-file clock. The route is already synchronized:

| File time | Camera | Place |
| --- | --- | --- |
| 00:00.0 to 01:00.0 | CAM-01 | Lobby and entrance |
| 01:00.0 to 01:57.0 | CAM-02 | East hallway |
| 01:57.0 to 03:36.6 | CAM-03 | West hallway |
| 03:36.6 to 03:50.2 | CAM-03 | West hallway, return |
| 03:50.2 to 04:27.8 | CAM-02 | East hallway, return |
| 04:27.8 to 05:39.8 | CAM-01 | Lobby exit |

Handoffs: 60.0, 117.0, 216.6, 230.2, 267.8. End: 339.8.

Console, already running: `http://127.0.0.1:8090/?ws=ws://127.0.0.1:8080/ws`

## The file on disk

`sentinel_final.mp4` is a finished composite, 2 minutes 6.07 seconds, 1920×1080, 30 fps, H.264, AAC stereo 48 kHz. The mix is loud (about -19 dB average, peaks near -1 dB), with speech and music in one stereo track. Silence is only the opening three seconds, a five-second hold near 1:26, and the last three seconds.

What the frames show, in order:

- A black open, then a title card: Sentinel AI, "Real-time threat detection, tracking and response," with an SJSU banner and an HP footer.
- A screen recording of an older console. The hero is labeled CAM5. Four small views sit underneath (hallway, parking lot, exterior). A site map and an emergency-call transcript share the right side. Captions are burned in.
- A close view of people in a lobby, red boxes on the figures, then the full console again with a group in that lobby.
- A split layout: the console on the left, a person on stairs labeled "911 DISPATCHER" on the right, and a spoken call about San Jose State and MacQuarrie Hall.
- A map graphic titled "CROSS-CAMERA TRACKING," with small camera tiles around a campus map.
- A dark hold, then the console again on a yellow hallway, then a broadcast dialog, then a phone showing an SMS. A phone number is burned into that shot.
- A models panel, a usage chart, and an end card: "From first sighting to help on the way, in seconds."

The assembly is tight: one branded frame, consistent captions, a choreographed cursor, and a clean end card. That finish is the reason to leave it alone. The locked route is 5:39.8, and this file never reaches the handoffs at 60.0, 117.0, 216.6, 230.2, or 267.8. The picture is CAM5 plus extra views, a dispatcher insert, a campus map, sponsor marks, a 911 banner, and a phone number. Voice and music share one stereo track. There is no clean plate of the current Live Operations wall (CAM-01, CAM-02, CAM-03). A new screen recording is the master.

## Record today

Do this in order. The recorder starts at step 7. Everything before that is setup.

1. Use the machine where the console is already open. Stay on localhost. Record the browser window.
2. Set the window to 1920×1080, zoom 100 percent, bookmarks bar hidden. The viewport stays at least 1800 pixels wide so Live Operations keeps three columns: incidents (left), the camera (center), site plan and call (right).
3. Open `http://127.0.0.1:8090/?ws=ws://127.0.0.1:8080/ws`. You land on Live Operations. The splash runs about six seconds. Click it, or press Space, once it accepts a click.
4. Confirm the wall before you roll. Three tiles only: CAM-01 lobby, CAM-02 east hallway, CAM-03 west hallway. Each tile reads PLAYBACK. The header reads IBM Sentinel AI. One person, on one tile. The other two tiles hold a still from their own rooms.
5. Prop a phone at the right of the monitor, screen awake, message thread open, brightness up. Cover the number with tape or a card before you roll. The message body stays readable.
6. Leave the hero on auto-follow. After the incident opens, keep your hands off the camera tiles. A click pins a camera and the hero stops following the handoffs.

Slate, then the take:

7. Start the screen recording of that 1920×1080 window.
8. Slate, six seconds, header "IBM Sentinel AI" filling the frame. Say: "Slate. IBM Sentinel AI. Take one." Clap once in the lower left, inside the frame. That clap is the sync spike.
9. Reload the page. Click the splash as soon as it accepts the click. Spoken 00:00.0 is the first frame of the lobby entrance on CAM-01, with CAM-02 and CAM-03 still. If the splash covers the entrance, stop and reload. Begin again from the slate.
10. Read the spoken script from 00:00.0 through 05:39.8. The click cues below are silent. Read the script over them.
11. At about 00:16, the weapon and guard moment. The red box is on the person in the lobby, and the left card reads Weapon. Hero plus both thumbnails stay in frame. Hold that picture. Then click **Call for help** on the incident card. In the dialog, click **Call for help** again. The right column shows the call: a running timer and the transcript. That column stays visible for the rest of the take.
12. Hands off at 01:00.0 and 01:57.0. At each handoff the hero changes room, the previous camera becomes a still thumbnail, and all three labels remain. The person is on one picture.
13. At about 02:20, during the west hallway, click **Broadcast**. Click **Security team**. Type: `Shelter in place. Armed person in the west hallway.` Click **Send broadcast**. Leave the result up until the dialog closes. If the phone shows that message, slide it into the lower right for five seconds, number still covered, then set it aside before 03:30.
14. Hands off at 03:36.6, 03:50.2, and 04:27.8. Same rule: one moving picture, two stills, call timer still readable.
15. At 05:39.8 hold two seconds on the lobby. Stop the recording.

Stay on Live Operations for the whole take. The call column on the right is the phone call. The broadcast result, and the phone if it lights up, is the SMS.

## Spoken script

Read this. Short sentences. Pause at the periods.

**00:00.0.** IBM Sentinel AI watches one campus building. Three cameras. The lobby. The east hallway. The west hallway.

**00:08.** A person comes through the entrance. The lobby camera has them. The other two cameras stay on their own rooms.

**00:16.** The box turns red. A weapon is in the lobby. This is the guard's screen. The same doors. The same person. The same alert.

**00:28.** IBM Sentinel AI calls campus security. The place is the lobby. The person is in view. Help is on the line.

**00:44.** One incident. One call. The guard sees it as it happens.

**01:00.0.** They step into the east hallway. IBM Sentinel AI follows. The lobby camera returns to its own room.

**01:18.** The call stays open. Security hears the new place. East hallway.

**01:36.** The map moves with them. Campus security has the path, and the picture to match it.

**01:57.0.** They enter the west hallway. The call updates. Security knows where they are.

**02:14.** Same person. Same incident. The picture and the call agree.

**02:28.** A message reaches the security team. Shelter in place. An armed person is in the west hallway.

**02:42.** The text is in their hands. Every guard knows where to look.

**03:05.** IBM Sentinel AI holds the west hallway. The incident stays open. The call stays open.

**03:36.6.** They turn back on the same camera. West hallway, heading toward the east side.

**03:50.2.** East hallway again. Security hears they are on the way back.

**04:12.** One person. One path through the building. Each camera keeps its own room.

**04:27.8.** They are back in the lobby, walking toward the doors they came through.

**04:52.** The lobby camera has them. The call still has them.

**05:18.** They reach the entrance.

**05:32.** From the first step in, to the last step out, campus security had the picture and the place.

**05:39.8.** IBM Sentinel AI. From the first sighting to help on the way.

## Later edit

These notes are for the edit after the new recording exists. They are idle until then.

- Cut on the five handoffs and on the weapon box. Hold the lobby detection for a full breath before the first trim. Leave each hallway up long enough to hear the place name.
- Lower thirds: place only. "Lobby." "East hallway." "West hallway." IBM blue `#0f62fe` on the carbon console. Keep them clear of the red box, the incident card, and the call timer.
- Music sits under the walk, quiet enough that every sentence stays forward. Drop it out for the call, the text, and each handoff line. The slate and the clap stay dry.
- One second of quiet after each handoff sentence. Two seconds of room tone after the last line, then the end card.
- End card: the shield, "IBM Sentinel AI," and "From the first sighting to help on the way." Hold four seconds.

## Wait for the new recording

Opus, ChatGPT, and Gemini edits wait until the user supplies the new recording. `sentinel_final.mp4` stays as it is.
