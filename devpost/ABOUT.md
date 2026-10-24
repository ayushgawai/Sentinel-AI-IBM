## Inspiration

Our campus has hundreds of security cameras, and almost nobody is watching them. When something happens, a fight, a weapon, someone collapsing in a stairwell, it's usually on camera. But the footage becomes evidence *after* the fact, not help *during* it.

The problem isn't a lack of cameras. It's a lack of eyes. U.S. colleges reported about **23,400** on-campus crimes in 2021, with roughly **2.1** sworn officers per 1,000 students, while **93%** of public schools already have cameras. And the alerts campuses do have are mostly ignored: industry false-alarm rates run around 94–98%, so nobody trusts them.

So we asked: what if one AI could watch every camera, and when it's sure something is wrong, **call for help itself**, with facts a dispatcher can use?

## What it does

**Sentinel AI** watches every campus camera on one local GPU workstation. Video never leaves the building.

1. **Watch.** Every feed, every second.
2. **Detect and track.** YOLO26s-pose finds every person, ByteTrack gives each one a stable ID, and rules flag weapons, falls and running.
3. **Understand.** A local Qwen3-VL model reviews a 16-frame clip, classifies it (weapon, fight, theft, running, medical, or nothing), and describes the people involved.
4. **Check and decide.** For a severe weapon incident, **IBM Granite Guardian on IBM watsonx** checks a text summary of the threat, and an **IBM BeeAI** workflow combines that verdict with hard rules to allow or block the call.
5. **Act.**
   - It **calls for help by itself** and answers the dispatcher's questions ("How many people?", "What weapons?", "Where are they now?") only from what the cameras show.
   - It **follows the threat camera to camera**. The live map extends a red path, and the call gets updates like *"they have moved from the ground-floor lobby into the east corridor."*
   - The security console gets the alert, a one-click shelter-in-place broadcast, and a full record: timeline, transcript, and every model's activity.

## How we built it

![Sentinel AI technical architecture](https://cdn.jsdelivr.net/gh/ayushgawai/Sentinel-AI-IBM@main/docs/assets/architecture-technical.png)

- **Vision router (Python):** OpenCV/FFmpeg decode → **YOLO26s-pose** → **ByteTrack** → temporal pose rules + **OpenCLIP ViT-B/16** anomaly scoring. It is tuned for **recall**: a false positive here costs a few milliseconds of GPU time, while a miss costs everything.
- **Brain:** escalated clips go to **Qwen3-VL-30B-A3B (FP8)** on a local OpenAI-compatible runtime. It's a 30B mixture-of-experts model with only about 3B parameters active per step, so it fits on one GPU next to YOLO.
- **Calibrated confidence:** we never ask the model to *type* a confidence number. We read the token log-probabilities of each class label and apply temperature scaling:

$$ p(c \mid \text{clip}) = \frac{e^{z_c / T}}{\sum_{k} e^{z_k / T}} $$

  The label and the person description come from two completions over the same encoded clip, so the expensive part is paid once.
- **Decisions in plain code, not the model:** severity thresholds (minor \\( \ge 0.55 \\), severe \\( \ge 0.80 \\)), an incident state machine, one call per incident, an hourly cap, and a kill switch.
- **IBM dispatch review:** `track_ai.py` sends only the incident text to **Granite Guardian** (`granite-guardian-3-8b`) on **watsonx**, then a **BeeAI** workflow makes the allow-or-block decision. If either one fails, the call is blocked, not allowed.
- **Voice:** **faster-whisper** transcribes the dispatcher locally. Answers come from a per-second scene script (people, weapons, place), and addresses come from a fixed camera map, never from the model. **ElevenLabs** speaks each line with about 160 ms to first audio, and **SignalWire** carries the call.
- **Console:** plain JavaScript modules over a hand-written asyncio WebSocket server, with no framework and no build step. Live camera wall, campus map with the tracked path, incidents, call console, and a system page showing every model live.
- **Planning with IBM Bob:** before writing code, we stress-tested the whole design with Bob. It reframed the problem from "detect incidents" to "produce an alert a human will believe", pushed us to logprob-based confidence, and steered us to Granite Guardian and BeeAI as a real gate rather than a log.

## Challenges we ran into

- **Small handguns are hard.** In 960×540 CCTV, handguns are a few pixels wide. Per-person CLIP, open-vocabulary YOLOE and per-crop Qwen were all unreliable live. For the demo we replay the dataset's hand-drawn weapon boxes by clip time, and say so openly. Detection, tracking, handoffs and Qwen classification run live.
- **One GPU, many models.** Running Qwen and CUDA YOLO together could exhaust GPU memory and lock up the machine. We capped Qwen at 40% of GPU memory and added a preflight check before starting.
- **"Video never leaves the building" vs. an outbound call.** Bob caught this contradiction early. We resolved it by sending only *text* out (the incident summary to watsonx, the words to speak to ElevenLabs) plus call audio, never frames.
- **Making the call sound real, and stay true.** Sentinel's answers have to match the picture at that exact second, and the "they have moved" updates have to land on the camera handoff. We keyed the conversation to the camera wall's clock instead of fixed delays, so every count, weapon and update matches what's on screen.
- **A gate that never closes proves nothing.** We made sure Guardian or BeeAI failing blocks the call, and show their status live on the System page.

## Accomplishments that we're proud of

- An end-to-end loop from first sighting to a natural-sounding call, with live updates as the threat moves.
- Answers grounded in what the cameras see, never invented, with addresses from a fixed map.
- IBM Granite Guardian and BeeAI in the actual decision path, not bolted on.
- Privacy by design: no face recognition, no identity database, no video in the cloud.
- A 13–14 fps live camera wall with boxes, on one workstation.

## What we learned

- **Trust beats accuracy.** Campuses don't lack alerts. They lack alerts people believe, and calibrated confidence plus an independent check matter more than one more point of accuracy.
- **Tune each tier for its own error.** Recall at the cheap first pass, precision at the expensive one.
- **Models describe. Code decides.** Every irreversible step (calling, broadcasting) sits behind deterministic rules and an independent safety model.
- **Be honest in the demo.** Saying clearly what's live, what's replayed and what's staged made the project stronger, not weaker.

## What's next for Sentinel AI

- A small-weapon detector trained for CCTV, so weapon detection is fully live
- A real cross-camera re-ID model (OSNet) instead of today's stub
- Granite Guardian **groundedness checks** on every sentence Sentinel speaks
- Running Guardian locally, so the whole decision path stays on campus
- Precision/recall measurement on labelled campus footage, and a bias and privacy review
- A pilot with a campus security team, with human confirmation before any real emergency call, and an approved dispatch-center integration
