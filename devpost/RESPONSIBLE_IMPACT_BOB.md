# Responsible AI Considerations

Sentinel AI watches people and can pick up a phone, so we treated responsibility as an architecture problem rather than a policy page. Our rule from day one: models describe, code decides, and anything irreversible sits behind independent checks.

SAFETY: no single model can trigger an outside action
- Every call has to pass four independent layers. (1) Calibrated thresholds: the vision model's confidence comes from token log-probabilities, not a number it types, and only "severe" (≥ 0.80) incidents escalate. (2) Hard-coded guardrails: one call per incident, a rolling hourly cap, and a global kill switch. (3) IBM Granite Guardian on watsonx: an independent model judges whether the incident is actually harmful. (4) An IBM BeeAI workflow combines the rules and Guardian's verdict into an allow-or-block decision.
- The system fails closed. If Guardian or BeeAI errors or times out, the call is blocked, not allowed.
- The dialer cannot reach real emergency services in this build. It hard-rejects 911, 112, 999, 988 and other emergency numbers, rejects short codes, and only ever calls one allowlisted, verified number. That's enforced in code, not in a config comment.
- Humans keep the final say on the console. Officers can confirm or dismiss any incident, and the kill switch stops every outbound call instantly.

INACCURATE AI OUTPUTS: grounded answers or no answer
- The model never supplies a location. Addresses and place names come from a fixed camera map, so a hallucination can't send responders to the wrong building.
- On the call, Sentinel answers counts, weapons and movement from what the cameras show at that second. When it can't verify something, it says so: "I don't see the person now; this is their last confirmed camera", "I can't verify their medical condition from this camera."
- A cheap first pass is tuned for recall and an expensive model for precision, so the system doesn't make expensive decisions on cheap evidence.
- We're honest about current limits. Small handguns aren't yet detected reliably live, so the demo replays labelled weapon boxes, and we disclose that everywhere.

PRIVACY: move the computer to the video, not the video to the cloud
- All video analysis runs on one on-campus workstation. Frames never leave the building.
- Only short text goes out: a one-line incident summary to watsonx, and the sentences Sentinel speaks to ElevenLabs. Plus call audio.
- No face recognition, no identity database, no matching against student records. Sentinel describes clothing and actions ("a man in a red polo shirt with a handgun"), never who someone is.

FAIRNESS AND BIAS
- Sentinel doesn't infer identity, ethnicity or any protected attribute, and doesn't use them in any decision. Escalation is driven by objects (weapons) and motion (falls, running), not by who a person is.
- We know detection quality can vary with lighting, camera angle, clothing and skin tone, and we haven't measured that yet. Before any real deployment we'll report precision and recall broken down by camera and condition, and review every dismissed alert for patterns.
- Inclusive by design: it runs on cameras campuses already own and one local GPU, with no per-camera cloud subscription, so schools priced out of commercial systems can use it.

TRANSPARENCY AND ACCOUNTABILITY
- Every decision is visible and recorded: an incident timeline (created → alerted → dispatched → tracked → resolved), the full call transcript, and a System page showing every model, where it runs, its live status, and token use.
- Every IBM review is logged with Guardian's verdict and BeeAI's reason. The incident history is stored for audit and replay.
- We publish what's live, what's pre-computed and what's staged in our README and demo notes.

ACCESSIBILITY
- The console has light and dark themes, respects the operating system's reduced-motion setting, and uses labelled controls.
- Alerts never rely on color alone: severity is written out ("Severe", "Dispatched") next to the color.
- For dispatchers, Sentinel speaks short, plain sentences in a natural voice and repeats or clarifies on request.


# Real-World Impact & Feasibility

WHO BENEFITS
- Campus security teams: a few officers responsible for hundreds of screens get one trustworthy alert instead of a wall of unwatched video.
- Students, staff and visitors: their emergencies get noticed while they're happening, not found in footage the next day.
- 911 dispatchers: they get a calm caller with facts (location, how many people, what weapons, where they're moving) instead of panicked, partial reports.
- Under-resourced schools: community colleges and K-12 districts that can't afford per-camera cloud subscriptions can run it on cameras they already own.

THE IMPACT
- Minutes become seconds. Today the chain is someone notices, then someone calls, then dispatch locates. Sentinel removes the "someone notices" step entirely and starts the call immediately with verified facts.
- Responders know where to go. Camera-to-camera tracking turns "somewhere in the building" into "the east corridor, heading toward the stairwell," updated live on the call.
- Compute scales with incidents, not cameras. The cheap first pass screens every frame and the large model runs only on escalations, so adding cameras doesn't mean adding GPUs at the same rate.

EVIDENCE AND ASSUMPTIONS
- The need: U.S. colleges reported about 23,400 on-campus crimes in 2021 (NCES), with roughly 2.1 sworn officers per 1,000 students (BJS), while 93% of public schools already use cameras (NCES). The cameras are in place. The attention isn't. Industry estimates put alarm false-alarm rates around 94–98%, which is why existing alerts get ignored.
- Our prototype measurements, on one workstation: a 13–14 fps live camera wall with detection, about 160 ms to the first word of speech on the call, and weapon labels aligned on 640 of 649 frames. The full loop runs end to end: detection, tracking, Qwen classification, the IBM review, the call, and live handoff updates.
- Assumptions we state openly: that campuses can expose existing cameras over RTSP; that one GPU workstation can serve a building's worth of cameras (we've demonstrated 3 under full analysis plus 3 background feeds, not hundreds); and that dispatch centers will accept automated, fact-based calls, which needs partnership and regulatory approval.

HOW WE WOULD MEASURE SUCCESS
- Time to alert and time to call, from first sighting (target: under 10 seconds), compared with the campus's current baseline.
- Precision and recall on labelled campus footage, broken down by camera and lighting, plus false alerts per camera per day. That's the trust metric.
- Answer accuracy: the share of Sentinel's spoken answers that match the footage when reviewed afterwards (target: 100% for location, which comes from the map, not the model).
- Operator trust: the dismiss rate of alerts, and officer survey scores on usefulness.
- Efficiency: the share of frames escalated to the large model, and GPU cost per camera.

MAIN CHALLENGES BEYOND THE HACKATHON, AND OUR PLAN
1. Weapon detection accuracy. Small handguns in low-resolution CCTV are the hardest case. Plan: fine-tune a detector on CCTV weapon datasets and campus footage, and publish its precision and recall.
2. Legal and dispatch integration. Automated calls to public 911 raise liability and regulatory questions. Plan: pilot in stages. First alert-only to campus security, then human-confirmed calls to campus police dispatch, and only then an approved integration with a public dispatch center.
3. Privacy approval and community trust. Plan: a published privacy policy, no face recognition, data retention limits, an audit log open to campus governance, and a bias review before go-live.
4. Scale and integration. Plan: connect to existing video management systems over RTSP, move to a real cross-camera re-identification model, and size GPU servers per building.
5. Keeping the whole decision path on campus. Plan: run Granite Guardian locally so not even the incident text leaves the building.


# IBM Bob Usage

Yes. IBM Bob was our design partner before we wrote any code. We used it in one long planning session (more than 50 exchanges), and it searched the IBM documentation more than a dozen times to ground its answers. We asked it to poke holes rather than agree, and it changed our design in specific, traceable places:

PLANNING AND PROBLEM FRAMING
- It reframed the project from "detect incidents" to "produce an alert a human will actually believe." Starting from industry false-alarm rates of roughly 94–98%, it argued the bottleneck is trust, not detection. That became our whole product thesis.
- It stress-tested our privacy story. It caught that "video never leaves the building" seemed to contradict "the system places an outbound call," and we resolved it by sending only text and call audio out, never frames. It also checked our smoke-detector analogy for where a judge would push on it.

ARCHITECTURE AND IMPLEMENTATION
- Tiered inference: a cheap screen on every frame, and the large vision model only on what it flags. It convinced us to tune the cheap tier for recall, not accuracy, by working through the costs: a false positive costs milliseconds of GPU time, while a miss costs everything.
- Calibrated confidence: we had planned to let the model write a confidence number in its JSON. Bob explained why that's a token, not a probability, and steered us to token log-probabilities plus temperature scaling. We built that, along with Bob's idea of getting the class label and the person description from one encoded clip in two completions.
- One model for boxes and pose (we use YOLO26s-pose), and a fall rule that looks at a sequence of frames, because bending down and collapsing look identical in a single frame.
- GPU memory: it warned that one model server grabbing memory at startup would starve the others. We cap Qwen at 40% of the GPU so YOLO fits alongside it.
- The IBM safety gate: it pointed us to Granite Guardian and BeeAI as a real gate that runs before any action, rather than monitoring after the fact. That's now the dispatch review in our code.

DEBUGGING, TESTING AND DOCUMENTATION
- It shaped our test-the-gate thinking: "a gate that never closes is indistinguishable from no gate." That's why Guardian or BeeAI failing blocks the call, and why their status is shown live.
- It drafted planning documents for us: a build plan with parallel lanes for the team, a shared event contract, a model factsheet structure, and a first three-minute video script.
- It helped us decide on running the stack directly on the host with a startup script rather than Kubernetes, and what to avoid on the phone side to keep our cloud claims honest.

WHERE WE DISAGREED WITH BOB (and why we're telling you)
- Bob argued that a human should confirm every dispatch. We chose an automatic call, but only behind four layers (calibrated thresholds, hard guardrails, Granite Guardian and BeeAI), failing closed, and limited in code to one verified test number that can never be 911. A staged rollout with human confirmation is the first step of our real-world plan.
- Bob also proposed a second Guardian check on the groundedness of every sentence Sentinel speaks. We haven't built it yet. It's at the top of our next steps.

We also used Claude Code, Codex and Cursor for implementation, debugging and documentation. Bob was where the design was argued out. Our team reviewed and tested everything these tools produced.
