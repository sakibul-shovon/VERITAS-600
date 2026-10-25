# The Weight of Evidence

VERITAS-600 / 174 seconds / 1920×1080 / 30 fps / light theme throughout.

## Creative direction

A document examination is a chain of consequences. Sheets of ivory paper glide into alignment above a bright drafting-table environment. A copper line tries to connect them; the insurance shortfall leaves the chain open. The papers converge into the actual product. The line then carries attention through intake, bounded reasoning, external risk and a human authority gate. The final shot resolves the opening's fragmented evidence into an orderly ledger, while the authority gate remains explicitly human.

The product is positioned as a traceable examination system with bounded AI, not autonomous banking or production-certified legal advice. Motion graphics are explanatory; every depicted product screen is captured from the running application.

## Feature coverage matrix

| Feature / user value | Current implementation | Demo evidence and timing | Priority / explanation |
|---|---|---|---|
| Product landing, evidence gate, interactive trace | app/page.tsx | Actual light hero, trace/invariant sections, 26–38 | Core; contextual reveal |
| Clean start, labelled samples and case selection | app/examine/page.tsx, HeaderBar | Start and synthetic sample selection, 38–48 | Supporting; visible action |
| Create user case / credit baseline | NewCaseDialog, POST /cases | Real form and new synthetic case, 38–48 | Core intake |
| PDF and image upload | EvidenceIntake, CaseStore | Actual PDF upload using generated synthetic documents, 48–60 | Core; four required document types |
| Text PDF extraction / OCR provenance | document_extractor.py | PDF_TEXT_LAYER badge, actual returned fields, 48–60 | Core; do not imply live VLM |
| Field review/edit, confidence, source hash, page boxes | EvidenceIntake | Real review form and hash crop, 48–60 | Core; confidence is extraction certainty |
| Required document completeness and acceptance gate | CaseStore/EvidenceIntake | Four-document accepted snapshot, 48–60 | Core; demonstrates gating |
| Five-stage SSE execution | main.py, MissionControl | Actual run and event ledger, 60–70 | Core; stage boundaries visible |
| Six bounded context packets and estimates | meterless_router.py | Actual stage telemetry + explanatory six-packet graphic, 60–70 | Supporting; local router, estimates |
| Accepted/pending amendment state, Art. 10(c)/(e) | amendment_memory.py, matrix | Actual amendment tab from sample 8841, 70–80 | Core; state lineage |
| Dates, limits, quantities, insurance, weights | ucp600_deterministic.py, CalculationBoard | Actual calculations, insurance crop and category montage, 80–95 | Core; 108% vs 110% |
| Semantic typo and non-invoice goods protection | adjudicator, Rules Matrix | Actual 8841 findings, 95–107 | Core; A23 and Art. 14(e) |
| Postgres/customs/watchlist federation | zetaris/client.py, FederationWorkspace | Actual 9920 map, local mode, 107–123 | Core; one-row output |
| SQL/provenance inspection | ZetarisDrawer, sponsor receipt endpoint | Actual drawer crop, 107–123 | Supporting; display SQL identified as inspectable UI |
| TBML and watchlist alerts | decision engine, 9920 sample | Actual +23.10 and watchlist match, 107–123 | Core; synthetic risk example |
| Honour / refusal / AML hold | DecisionActionPane | All three actual recommendations, 123–138 | Core; remain pending |
| Draft voucher / MT734 / AML dossier, copy | ArtifactGenerator / DecisionActionPane | Real generated artifacts in detail montage, 123–138 | Core; no dispatch |
| Cure/demurrage advisory | deterministic engine / decision pane | Actual scenario advisory, 123–138 | Supporting; scenario estimate, not measured bank saving |
| Examiner name/comments + explicit authority gate | DecisionActionPane, approve-action | Actual form, pending sign-off, 138–153 | Core; do not impersonate a human examiner |
| Terms hash, decision digest, Merkle evidence lineage | AuditWorkspace, audit modules | Actual audit receipt before sign-off, 138–153 | Core; signature still pending |
| Benchmark rerun, filters, case drilldown | /evals, compare_baselines.py | Actual server results and selected case, 153–164 | Supporting; ten synthetic cases, local/replay mode |
| Theme, route navigation, health badges, error states | HeaderBar, NoticeRegion | Theme verified each capture; badges retained across UI footage | Supporting; no dark-mode toggle demo |
| Authentication / external dispatch | No login/onboarding product journey; configured API-key approval gate; dispatch unconnected | State limits in plan and on-screen | Do not invent settings, authentication UI or live bank integration |

Three-minute tradeoff: all major capabilities receive visual coverage; every edge-case test, individual field, error recovery branch and theme toggle cannot be taught as a tutorial. The feature inventory above is the coverage contract.

## Timed storyboard and camera grammar

| Time | Visual and motion | Purpose / sound |
|---|---|---|
| 0–3 | Extreme close view of insurance folio; papers slide through orthogonal planes, copper trace stalls at 108%. | Immediate fact, quiet paper movement |
| 3–8 | Pull back to threshold stencil at 110%; discrepancy cuts the trace. | Legible tension; brief near silence |
| 8–12 | Typographic document variance and objective calculation split into separate lanes. | Different kinds of judgement |
| 12–17 | External-risk source is outside the documentary stack; five-day examination context appears as five banking-day markers. | Stakes without a fake countdown |
| 17–21 | Paper planes register into one evidence path. | Release of tension, harmonic lift |
| 21–26 | Brand and thesis resolve, with a restrained geometric ledger mark. | Product reveal after the problem |
| 26–32 | Real light landing page in an ivory browser, shallow perspective settling to frontal view. | Product identity and readability |
| 32–38 | Landing interactive trace / invariant detail; line bridges to examination. | Promise becomes a workflow |
| 38–43 | Actual clean start, then real new-case form with credit fields. | Establish examiner action |
| 43–48 | Synthetic case opens; real upload controls. | Credit baseline and evidence room |
| 48–54 | Upload invoice and select the extracted PDF fields; crop to actual source and values. | Evidence is ingested, not invented |
| 54–60 | Four document types, human review and accepted snapshot. | Readiness is earned |
| 60–65 | Actual run animates five bounded stages. | Accountable orchestration |
| 65–70 | Real event ledger + six context packets, local/replay label. | Explain orchestration without unsupported efficiency claim |
| 70–75 | Accepted amendment enters active terms. | Stateful context |
| 75–80 | Pending amendment remains quarantined; fingerprint detail. | Art. 10(c)/(e) |
| 80–85 | Actual rule analysis, dates/amounts/weights category cadence. | Deterministic scope |
| 85–91 | Insurance values expand from real UI into an explicitly explanatory calculation: 480,000 × 1.10 = 528,000. | Exact numeric proof |
| 91–95 | 518,400 leaves a 9,600 shortfall; locked discrepancy. | No AI override |
| 95–101 | Actual 8841 findings: Mashine typo accepted. | ISBP 745 Para A23 |
| 101–107 | Non-invoice general goods description protected; honour recommendation still pending. | UCP 600 Art. 14(e) |
| 107–113 | Actual three-source federation; camera follows copper connection. | Context beyond documents |
| 113–118 | Actual +23.10 sample / watchlist match crop. | External risk example |
| 118–123 | SQL drawer detail, one-row provenance; local mode remains visible. | Inspectability |
| 123–128 | Actual honour and voucher crop. | Outcome one |
| 128–133 | Actual refusal and MT734/cure advisory. | Outcome two |
| 133–138 | Actual hold and AML dossier. | Outcome three |
| 138–144 | Examiner name/comments form; authority gate remains pending. | Human is final |
| 144–153 | Actual terms hash, decision hash and Merkle root; no signature is fabricated. | Explain lineage and no dispatch |
| 153–159 | Actual benchmark server result; ten synthetic cases, local/replay scope. | Reproducible evidence |
| 159–164 | Actual case detail/filter montage, measured count rather than universal claim. | Honest limits |
| 164–169 | Opening papers return, now ordered and linked; human-authority terminal remains the end of the line. | Visual resolution |
| 169–174 | Original ledger mark, product name, concise thesis and GitHub repository. Pale final hold. | Harmonic resolution, no black fade |

The exact spoken script is voice/script.json. It is segmented into short phrases for measured-audio caption synchronization. Narration should average roughly 125–145 spoken words per minute, leaving visual rests. If a line exceeds its slot, edit the line or its synthesis speed modestly, never squeeze all speech to 180 seconds.

## Design and motion system

Paper #f3f0e7, warm white #fffdf7, forest #123d38, copper #a24d2c, ink #17201e. Georgia headlines, Arial/Segoe UI body, Consolas evidence labels. Full brightness does not remove contrast: use ink and forest for structure, copper for the moving evidence path, red only for failed facts. Headline at most two lines; one focus per frame; captions reserve the lower 120 px. No film graphics use dark full-frame backgrounds.

Spatial entry 18–30 frames, detail emphasis 12–18 frames, handoffs 18–24 frames. Strong damped easing, no rubbery bouncing financial figures. Camera translates to meaning, settles, then allows reading; perspective is modest for UI. Use layered cards, source-to-result lines, clipped detail windows, reversible depth moves and paper-edge match cuts. No time-based CSS animation in the final compositor. Any microtexture is deterministic.

## Technical architecture and production phases

A. Research and design: report, product truth, inventory, reference critique. Accepted when source access and unknowns are explicit. Complete before generated scenes.

B. Script and storyboard: 174-second coverage map, caption phrases and shot assignments. Accepted when every major feature has a timed location and every claim has evidence.

C. Assets and capture: synthetic PDFs, actual app interactions, lossless 2× screenshots and interaction clips, capture manifest with theme checks and modes. Accepted when no invented product pixels or dark theme appear. Paper documents in motion graphics are explanatory, not asserted to be screenshots.

D. Motion: React/Remotion scene system, SVG paths, CSS perspective paper choreography and composited real captures. Accepted by still-frame inspection and low-resolution motion previews before master rendering.

E. Full workflow: real intake/review and three sample outcomes, no production sign-off. Accepted when API evidence matches screen states.

F. Voice/audio: local female Kokoro voice, individual recorded caption phrases, original procedural soundtrack and restrained effects. Accepted when no line exceeds its visual slot and pronunciation is reviewed.

G. Captions: cue start/end from actual generated audio samples; burn in phrases and export SRT/VTT. Accepted when no overlap, missing spoken line, clipping or guessed WPM timing exists.

H. Master and QA: render 1080p30 H.264 yuv420p + AAC, bt709 signalling and faststart; inspect representative frames, all scene boundaries, runtime, audio loudness and decode integrity. Export contact sheet and QA JSON. Only call it final after checks pass; if quality remains uncertain, deliver as a review cut and name the limitation.

## Critical evaluation and QA contract

The highest attention risk is the 70–123 second architecture section. Interleave actual interface proof with numerical closeups rather than leaving diagrams on screen. The intake form is the least cinematic screen; hold only the credit fields and transition to source documents promptly. The benchmark can mislead unless its synthetic/local scope is visible. Do not amplify its fixed summary fields into claims. The voice may need a commercial audition in a later pass; local synthesis is not equivalent to an actor's performance.

Rendering risk: large full-page screenshots and soft shadows can exhaust GPU memory. Use cropped assets, bounded perspective and 1080p rather than pretending a 4K container adds source detail. Code-native paper depth is intentionally 2.5D; do not call it path-traced 3D. A single repeated evidence path gives continuity; vary its shot scale so it does not become a gimmick.

QA: runtime <=180s; light classes checked before every shot; no black intro/outro; source captures legible at 1080p; no layout overflow; captions within safe area and synchronized to actual audio; exact citations; no model override of failed check; all three actions pending human approval; no bank dispatch; local/replay badges visible; sample data labelled; no fabricated benchmark claims; no secrets; no borrowed music or footage in master; H.264/AAC decode; true peak <=-1 dBTP and integrated loudness around -14 LUFS; shot-boundary and representative-frame review; report any remaining limitation.

Final recommendation: spend the visual budget on the evidence chain, the product capture and the insurance proof. Those three choices explain why VERITAS exists, establish that it works, and give the film an identity rooted in the product rather than borrowed technology-brand styling.
