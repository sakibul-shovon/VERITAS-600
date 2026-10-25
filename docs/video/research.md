# VERITAS-600 launch-film research

Research completed 25 October 2026, before production. Scope: sources available on the research date; this is not an exhaustive claim to have tested every commercial tool or watched every reference film. The direct request to begin making the video after research supersedes the pasted brief's older stop-for-approval instructions.

## 1. Evidence and creative references

| Official reference | What was inspected | Production implication |
|---|---|---|
| [Apple: The all-new MacBook Neo](https://www.youtube.com/watch?v=bg3iEHHTGtQ), [launch editorial](https://www.apple.com/uk/newsroom/2026/03/say-hello-to-macbook-neo/) | Official film metadata, launch imagery and editorial hierarchy. Full audiovisual playback was not available through the research tools. | Use a small number of precise hero compositions, a coherent material palette, and a single concrete idea per shot. These are creative recommendations, not claimed shot-by-shot observations of the film. |
| [Google: New Home](https://www.youtube.com/watch?v=Z1yGy9fELtE), [Gemini demo collection, May 2026](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-omni-3-5-videos/), [Material motion](https://m3.material.io/styles/motion) | Official descriptions and physics-based motion specifications. | Begin with a recognizable human problem; use movement to preserve cause and effect. Standard, minimally overshooting springs suit a bank tool better than exuberant bounce. |
| [Stripe Sessions 2026](https://stripe.com/sessions/2026) | Official event, product keynote and demonstration structure. No precise soundtrack/timing analysis claimed. | Introduce system complexity with a visual argument, then prove it with a real workflow. Avoid borrowing Stripe's brand gradients or implying sponsorship endorsement. |
| [Linear: Introducing Initiatives](https://linear.app/changelog/2024-06-25-introducing-initiatives) | Official embedded MP4 sampled at 0, 5, 10, 15, 20 and 25 seconds; contact sheet retained in this folder. | The opening is an explicit title followed by a restrained light UI walkthrough and presenter inset. Its product clarity is useful. Its long unchanging framing is unsuitable for this brief's cinematic opening. Do not describe this reference as a cinematic launch spectacle. |
| [Vercel Ship recap](https://vercel.com/blog/vercel-ship-2025-recap), [new v0 launch](https://vercel.com/blog/introducing-the-new-v0) | Official launch narratives, imagery and product arguments. | Explain the architectural difference through a concrete before/after consequence. A keynote's feature-list density will not fit a three-minute film. |

### First 5–10 seconds, rhythm, typography and sound

The strongest opening for this product is an interrupted act of documentary acceptance: beautiful papers align, a single insurance number prevents the chain from closing. This establishes a question without a logo introduction. By second five, 108% and the 110% requirement must be legible. This is our original proposed opening, not a description of an unseen reference.

Use contrasting editorial scales: 80–120 px display text, 30–44 px explanatory text, and restrained monospaced labels at 1080p. Alternate wide contextual views, readable detail crops, and diagrams. Give a newly introduced number at least two seconds. Use short silence at the failed check, then a harmonic lift at the product reveal. Full audiovisual access was unavailable for several references, so no claims are made about their exact music, camera paths, cut intervals, or opening timecodes.

World-class work differs from an ordinary demo through authored attention: a visual cause, a consequence, a satisfying resolution, unified materials, readable hierarchy, sound tied to meaningful motion, and enough restraint to let an important fact land. Adding more transitions is not equivalent to production quality.

## 2. Production technology comparison

| Approach | Verified capability / primary source | Decision for this project |
|---|---|---|
| React + Remotion | [Frame-based composition](https://www.remotion.dev/docs/idea), [renderer API](https://www.remotion.dev/docs/api), [determinism guidance](https://www.remotion.dev/docs/flickering) | Primary compositor. Exact frame control, captions, SVG, camera transforms, local repeatable rendering. All animation must derive from frame number. |
| GSAP | [Timeline](https://gsap.com/docs/v3/GSAP/Timeline/), [seek](https://gsap.com/docs/v3/GSAP/Timeline/seek%28%29/) | Excellent authoring/sequencing, but an additional realtime clock is unnecessary. Use Remotion interpolation and springs directly. |
| Motion / Framer Motion | [Official React guide](https://motion.dev/docs/react) | Strong interactive layout and gesture animation. Not the film timeline: browser time cannot independently drive concurrent frame rendering. |
| Three.js / React Three Fiber | [Three.js docs](https://threejs.org/docs/), [Remotion ThreeCanvas](https://www.remotion.dev/docs/three-canvas) | Appropriate for true geometric lighting. For flat documents, CSS perspective and SVG provide sharper text with less GPU risk on this machine. |
| WebGL / WebGPU | Three.js renderer documentation above | Powerful but hardware-dependent. WebGPU is not assumed to be experimentally necessary or inherently superior. Excluded from the critical path. |
| SVG / Lottie | [Lottie](https://lottie.airbnb.tech/), [Remotion components](https://www.remotion.dev/docs/components) | SVG used for evidence paths, seals, shape reveals and diagrams. Lottie adds little without an existing vector animation asset. |
| Blender | [Cycles capabilities](https://www.blender.org/features/rendering/) | Real lighting, depth of field, PBR and camera motion blur are verified. Installing a DCC and long path-traced shots would not improve the clarity of mostly typographic evidence in this environment. Reserve for a later studio pass. |
| After Effects / Resolve | [Adobe After Effects](https://www.adobe.com/products/aftereffects.html), [Fairlight](https://www.blackmagicdesign.com/products/davinciresolve/fairlight) | Mature art direction and audio tools. Not available as an established automated local pipeline. A manual operator would make these stronger options; there is no claim the code compositor universally outperforms them. |
| Browser capture | Actual Next.js/FastAPI runtime inspected locally, screenshots in qa/ | Real UI pixels are the evidence. Capture interactions, state changes, and detail crops; composite them instead of reconstructing invented functionality. |
| FFmpeg | [Filters and loudnorm](https://ffmpeg.org/ffmpeg-filters.html) | Mastering, muxing, metadata checks, sample-frame extraction and defect scans. |
| Generative video | [Runway Gen-4](https://runway.com/research/introducing-runway-gen-4), Google demo collection above | Useful for evocative non-product imagery. Model-maker consistency claims are not proof of exact legal text or financial data fidelity. Exclude generated UI and disconnected stock-like clips. |
| Generative images | Potentially useful for matte plates and textures | Not required here: the product's paper geometry is best built with native vector/code assets. |

Recommendation: actual app captures + deterministic React/SVG/CSS-depth motion + locally synthesized female speech + audio-derived phrase captions + procedural score + FFmpeg master. Complexity earns its place by improving the viewer's understanding. Installed versions are pinned in package-lock.json, not guessed from research snippets.

## 3. Female narration and alignment

| Option | Verified strengths | Limits / practical choice |
|---|---|---|
| ElevenLabs | [Model catalogue](https://elevenlabs.io/docs/overview/models), [forced alignment](https://elevenlabs.io/docs/api-reference/forced-alignment/create?explorer=true) document expressive synthesis and character/word timings. | A leading commercial audition candidate; naturalness is subjective and has not been independently ranked here. No paid credentials assumed. |
| Kokoro-82M | [Official model card](https://huggingface.co/hexgrad/Kokoro-82M), [ONNX implementation](https://github.com/thewh1teagle/kokoro-onnx) | Local, controllable, Apache-2.0 model. Use a female voice, render short phrases and inspect durations. Less expressive than a directed actor; label the narration as synthesized. |
| Operating-system voices | Locally available synthesis can provide scratch timing | Not an acceptable substitute for the requested polished final voice without an explicit limitation. |

Use Kokoro for the actual production. Do not assert that a free voice is objectively the world's best. Narration is the quality risk most likely to benefit from a later actor or commercial voice audition.

[Faster Whisper](https://github.com/SYSTRAN/faster-whisper) can provide word timestamps from recorded audio. True forced alignment is distinct from transcription. For this edit, synthesize individually captioned phrases, use their measured sample lengths and silence boundaries, and retain the exact script. That produces audio-derived phrase alignment without estimated words-per-minute cues. Each complete phrase is its own recorded file; no cue is timed from text length. Export SRT/VTT and caption JSON. Word highlighting is optional and must not be invented from equal word spacing.

Music is an original procedural score, with changing harmony, a restrained pulse, tonal paper/relay accents and reveal chimes. Voice is foremost. Target master -14 LUFS integrated with true peak <= -1 dBTP; verify the rendered result, not only the configured filter.

## 4. Mandatory root reference analysis

Read in full: H:/Projects/VERITAS-600/video prompt.txt (the separate-project reference). Strong ideas: problem-first structure, real software footage, deterministic capture, local speech, original score, explicit fallback states, captions, QA, and a reproducible workspace. Applicable: Remotion + browser capture + audio-derived cues + FFmpeg. Reject: its exploit/attack storyline, rigid nine-act timings, 3–4 minute duration, and arbitrary feature examples. Improve: protect readability, shorten the setup, connect every scene with one evidence-path motif, and avoid spending a minute on architectural preamble. Originality: a physical evidence ledger that becomes the real examination system; the same copper line remains open until the human authority gate.

## 5. Product truth and design inspection

Reviewed STATUS.md first, AGENTS.md, full docs/plan.md, graphify scoped queries, repomix inventory/compressed modules, and current code for all three routes, seven workspaces, intake, document viewer, amendments, rules, federation, decisions, audit, API contracts and evaluation. Repomix is older than the latest intake/mission-control code; current files and runtime take precedence when they differ. No application implementation changes are required for this film.

Runtime research screenshots: qa/research-landing.png and qa/research-examine.png. Landing class: landing-shell without landing-dark. Examination theme explicitly stored as light; exam-dark absent. Existing light design includes intentional forest sidebar and accent panels. Do not confuse those brand surfaces with activation of dark mode. Film backgrounds remain pale.

Palette: paper #f3f0e7, surface #fffdf7, ink #17201e, forest #123d38, copper #a24d2c, danger #a23232, success #0b684e. Georgia editorial display, neutral sans body, monospaced evidence. Physical paper layers, soft ambient shadows, embossed rule lines. No neon, dark set, random particles, or unrelated glass spheres.

Audience: documentary credit examiners. Real problem: distinguish legally harmless wording, non-negotiable calculations, and external regulatory exposure, while maintaining traceable human authority. No unverified market-size, bank-loss or production-accuracy claims.

Observed/runtime limits: Zetaris LOCAL_DUCKDB_FALLBACK; NIM CACHED_REPLAY; Meterless LOCAL_MARKOVIAN_ROUTER, token counts estimated by code. Text PDFs use PDF_TEXT_LAYER; vision is not represented as live. Final actions remain proposed; external dispatch is not connected. No real bank sign-off is performed in the film.

Code discrepancies relevant to portrayal: federation UI uses an above-4 explanation while the backend uses >=3.0; show the actual +23.10 sample without claiming that UI threshold is authoritative. SQL drawer contains a display copy, not a verified live execution trace of the latest backend SQL. Evaluation uses synthetic cases, local/replay baselines and some fixed summary fields; do not promote fixed savings/latency fields as measured external evidence. Avoid a general '100% accurate' headline. The film can show measured case counts with explicit scope.

Research status: complete. Proceed to production under the user's direct instruction.
