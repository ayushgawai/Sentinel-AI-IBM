# Sentinel AI: Devpost submission

Copy each section into the matching Devpost field. Lines marked **[FILL]** need your input.

---

## Project title

**Sentinel AI**

**Elevator pitch** (188 of 200 characters):

> AI that watches every campus camera, spots a weapon, checks it with IBM Granite Guardian and BeeAI, then calls 911 by itself with facts it can see, and follows the threat camera to camera.

**Thumbnail:** `thumbnail.jpg` (3:2, 3000×2000, 0.7 MB)

## Team

- **Team name:** [FILL]
- **Members:** Ayush Gawai · Naman [FILL last name] · Rahil [FILL last name] · Vraj [FILL last name]
  (Every member must also join the Devpost project from their own account.)

## Short summary

Campuses have thousands of cameras and almost no one watching them. Sentinel AI watches every feed on a local workstation. When it sees a weapon, it checks the threat with IBM Granite Guardian, lets an IBM BeeAI agent decide whether to act, then calls for help by itself. On the call it answers the dispatcher's questions from what the cameras see, and gives live updates as the person moves from camera to camera.

---

## Detailed description

### The problem

Cameras record everything, but people can't watch everything. U.S. colleges reported about 23,400 on-campus crimes in 2021, with roughly 2.1 sworn officers per 1,000 students, and 93% of public schools already use security cameras. The cameras are there. The eyes are not. Footage usually becomes evidence after the fact instead of help during it.

### Who experiences it

- **Campus security teams**, a handful of officers responsible for hundreds of screens.
- **Students, staff and visitors**, who are on camera when something goes wrong but get no faster help because of it.
- **911 dispatchers**, who get panicked, partial reports and have to piece together where a threat is and where it's going.

### What Sentinel AI does

1. **Watches** every camera feed, every second.
2. **Detects and tracks.** It finds every person, flags weapons, falls and running, and keeps a stable ID on each person.
3. **Understands.** A local vision-language model reviews a short clip and classifies it (weapon, fight, theft, running, medical, or benign), then describes the people involved.
4. **Checks and decides.** For a severe weapon incident, IBM Granite Guardian on watsonx checks a text summary of the incident, and an IBM BeeAI workflow combines that with hard local rules to allow or block the call.
5. **Acts.**
   - **Calls for help by itself.** It answers the dispatcher's questions ("How many people?", "What weapons?", "Where are they now?") only from facts the cameras show. Addresses come from a fixed camera map, never from the model.
   - **Follows the threat.** As people move between cameras, it extends a red path on the live campus map and says "Update: they have moved from the lobby into the east corridor" on the call.
   - **Alerts the security console** and offers a one-click shelter-in-place broadcast to the security team.
   - **Keeps a full record**: incident timeline, full call transcript, and every model's activity and token use.

Humans stay in control: one call per incident, an hourly cap, a kill switch, and officers can confirm or dismiss any incident from the console.

### How AI contributes

AI does the watching, understanding and talking. Plain code makes the safety-critical decisions.

| Job | AI used | Why it fits |
|---|---|---|
| Find and follow people | **YOLO26s-pose** + **ByteTrack** | Fast enough to screen every frame on one GPU; stable IDs make camera-to-camera handoff possible. |
| Spot unusual activity | **CLIP ViT-B/16** (VadCLIP-style scoring) | Cheap anomaly score on cropped people, so only interesting moments escalate. |
| Understand the scene | **Qwen3-VL-30B-A3B (FP8)**, served locally | A 30B mixture-of-experts model that activates only ~3B parameters per step: smart enough to classify a clip and describe people, small enough to run on campus. Video never leaves the building. |
| Check the threat | **IBM Granite Guardian** on **IBM watsonx** | A purpose-built safety/risk classifier gives an independent yes/no on whether the incident is harmful before anything outside the building happens. |
| Decide to call | **IBM BeeAI** framework workflow | A small, auditable agent workflow that combines the local rules with Guardian's verdict. No call is placed without it. |
| Hear the dispatcher | **faster-whisper** (base.en, local) | Low-latency speech-to-text on the box. |
| Speak on the call | **ElevenLabs** (eleven_flash_v2_5) | Natural voice with ~160 ms to first audio, streamed straight onto the phone line. |

### Technologies, tools and datasets

- **AI / ML:** IBM Granite Guardian (granite-guardian-3-8b), IBM watsonx, IBM BeeAI framework, Qwen3-VL-30B-A3B-Instruct-FP8, Ultralytics YOLO26s-pose, ByteTrack, OpenCLIP ViT-B/16, faster-whisper, ElevenLabs TTS, PyTorch
- **Backend:** Python 3.12, asyncio (hand-written HTTP + WebSocket server, no framework), SQLite, OpenCV, FFmpeg, NumPy, Pillow
- **Calling:** SignalWire (voice call, two-way media stream, SMS)
- **Frontend:** plain JavaScript ES modules, HTML, CSS, SVG/Canvas (no framework, no build step), OpenStreetMap static map
- **Infra:** Docker Compose, Make, a local GPU workstation, local OpenAI-compatible model runtime
- **Data:** US Mock Attack / Seville campus CCTV clips with hand-drawn weapon labels (used to replay weapon boxes in the demo)

### Impact

- **Minutes become seconds.** From first sighting to a 911 call, with no human needing to notice the right screen first.
- **Dispatchers get facts, not panic.** Location, count, weapons and live movement, from what the cameras actually see.
- **Responders know where to go.** Camera-to-camera tracking tells them where the threat is and where it's heading.
- **Privacy by design.** Video analysis happens on campus. Only short text (an incident summary, the words to speak) and call audio go to cloud services.
- **Works with the cameras campuses already have.** No new hardware on the walls.

### Results so far (measured on our demo workstation)

- Live camera wall with detection boxes: **13–14 fps**
- ElevenLabs time to first audio: **157–160 ms**
- Weapon labels aligned to the demo footage: **640 of 649 frames**

### Limitations (honest)

- **The demo is staged.** Camera feeds are recorded clips played back as live cameras.
- **Weapon boxes are pre-computed.** Small handguns in 960×540 footage weren't detected reliably live, so the demo replays the dataset's hand-drawn weapon boxes by clip time. Person detection, tracking, handoffs and Qwen classification run live.
- **The 911 call in the video is a recording-mode conversation.** In recording mode the dispatcher's side and Sentinel's answers are scripted to the clip (Sentinel's counts and weapons are read from the scene data at that second), the voices were added in editing, and this mode skips the Granite Guardian / BeeAI review. In live mode, a vision-detected weapon goes through Guardian and BeeAI, and the call goes over SignalWire to a verified teammate's phone. **It never dials real 911.**
- **Accuracy is not yet measured.** Thresholds are demo settings, not tuned on labelled data.
- **Cross-camera re-identification is a stub.** Handoffs rely on camera timing and an appearance hash, not a trained re-ID model yet.
- **The call voice and Guardian need the internet.** If they're down, a local backup voice speaks, and dispatch is blocked rather than allowed.

### Next steps

- Train or fine-tune a small-weapon detector so weapon detection is fully live.
- Add a real re-ID model (e.g. OSNet) for robust cross-camera tracking.
- Measure precision/recall on labelled campus footage and tune thresholds.
- Run Granite Guardian locally so the whole decision path stays on campus.
- Pilot with a campus security team, with a human-confirmation step before any real emergency call, and work with dispatch centers on an approved integration.
- Bias and privacy review: no face recognition, clear retention limits, and audit logs for every decision.

---

## Demonstration

- **Video (2:33):** [FILL: upload `sentinel_final_demo.mp4` to YouTube/Vimeo as *Unlisted* or *Public*, paste the link, and test it in a private window]
- **Live app:** not publicly hosted (it needs a local GPU workstation). We'll demo it live at judging.

## Technical work

- **Repository:** https://github.com/ayushgawai/Sentinel-AI-IBM (public). The README has setup and run instructions under "For developers", and the Windows setup is in `docs/WINDOWS_DEMO_SETUP.md`.
- **Image gallery:** upload `overview.png` (how it works), `technical.png` (architecture), and the screenshots in `gallery/` (live operations, camera handoff, west-corridor tracking, site-plan tracking, broadcast, incident timeline, call console, system models).

## Use of AI

**AI inside the product:** see "How AI contributes" above. Each model was chosen for one job: fast detectors screen every frame, a local vision-language model reasons only about escalated moments, IBM Granite Guardian provides an independent safety check, and an IBM BeeAI workflow plus plain-code guardrails decide whether to call. The model never decides alone, and never supplies an address.

**AI development tools:** we used four, and we reviewed and tested everything they produced.

- **IBM Bob:** our planning and design partner, in one long session before we wrote code. It used the IBM documentation tools to ground its answers, and it changed our design in specific places:
  - **Problem framing:** from "detect incidents" to "produce an alert a human will actually believe". With industry false-alarm rates around 94–98%, the bottleneck is trust, not detection.
  - **Tiered pipeline:** a cheap first pass on every frame, tuned for **recall** because a false positive there costs only milliseconds of GPU time, and the expensive vision model only on what it flags.
  - **Calibrated confidence:** don't ask the model to type a confidence number. Read **token logprobs** and calibrate them, and get the label and the person description as two completions from one encoded clip (we built this as Completion A and Completion B).
  - **Fall detection without training data:** a temporal pose rule across frames, since a person bending down and a person collapsing look the same in a single frame.
  - **IBM safety gate:** chose **Granite Guardian** and **BeeAI** as a real gate before any outside action, not a log after the fact.
  - **Where we disagreed:** Bob argued that a human should confirm every dispatch. We chose an automatic call gated by Granite Guardian, BeeAI and hard-coded guardrails (one call per incident, hourly cap, kill switch), and in this build it only ever calls a verified teammate's phone. Not every Bob design made it in: its groundedness check on each spoken sentence is a next step, and our Guardian check today is a single harm check.
- **Claude Code (Anthropic):** implementation and debugging (for example the recording-mode call script and its tests), the demo video edit and voice-over, the architecture diagrams, the README and this write-up.
- **Codex (OpenAI):** implementation and debugging.
- **Cursor:** coding assistant in the editor.

Our team reviewed, tested and validated all AI-assisted work, and we're responsible for everything we submit.

---

## Final checklist

- [ ] Every team member is listed and has joined the Devpost project
- [ ] Video link works in a private/incognito window
- [ ] Repo is public and the README setup steps are current
- [ ] No API keys, phone numbers or `.env` values anywhere in the submission
- [ ] Both diagrams are uploaded to the gallery
- [ ] Description matches what you built (the limitations above are part of that)
