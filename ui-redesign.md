# VERITAS-600 UI/UX Redesign Blueprint

> **Planning document only — no redesign has been implemented.**  
> Research and repository review completed 23 October 2026 (Asia/Dhaka).  
> Primary theme: light. Secondary theme: purpose-built dark.  
> Target: Open Agent Hackathon 2026, Track 03 — Reasoning Architecture.

## How to read this document

- **Verified** means confirmed in the repository or an accessible primary/public source on 23 October 2026.
- **Recommendation** means a design or engineering decision proposed for implementation.
- **Hypothesis** means a claim that needs validation with documentary-credit examiners or judges.
- This plan preserves the current FastAPI contracts, legal logic, three decisions, sponsor telemetry, and mandatory human sign-off. It does not authorize a backend rewrite.

---

## 1. Executive Design Vision

VERITAS-600 should become an **evidence-carrying decision room**: an examiner can see a documentary presentation, the exact evidence extracted from it, the deterministic and semantic rules applied, the provenance of cross-silo risk signals, the resulting bank action, and the human authorization that releases that action.

The central visual idea is **The Evidence Ledger**. The product borrows from documentary-credit packets, bank control sheets, legal marginalia, cargo manifests, and cryptographic seals—not from generic AI chat products. Warm paper surfaces, deep registry ink, fine ruled lines, editorial serif headings, compact monospaced evidence, and a restrained copper action color make the product feel institutional without feeling old. A living “decision spine” connects five real execution stages:

```text
ACTIVE TERMS → FEDERATED RISK → DETERMINISTIC RULES → SEMANTIC LAW → BANK ACTION
      memory          data             proof               judgment       human gate
```

The interface must communicate four truths in under five seconds:

1. This is a high-stakes bank examination, not a chatbot.
2. Python owns math, dates, thresholds, and locked failures.
3. Nemotron handles bounded semantic interpretation and cannot overrule deterministic failures.
4. No operational action is dispatched until a human examiner signs it.

Success is not “looks premium.” Success is that a first-time judge can correctly explain the architecture and outcome after a 90-second interaction, while an examiner can work quickly without spectacle obstructing evidence.

### Design principles

1. **Evidence before explanation.** Show the source field and computed value before prose rationale.
2. **Authority is visible.** Every finding declares who decided it: Python, Nemotron, Zetaris, amendment memory, or human examiner.
3. **Failures stay honest.** Loading, fallback, cache, fixture, interruption, and error states are named plainly.
4. **The decision has a chain of custody.** Evidence hashes, active-term hash, federation receipt, decision hash, Merkle root, and signer receipt are linked—not scattered as decoration.
5. **Quiet by default, expressive at transitions.** The workspace is fast and stable; motion is reserved for state changes, evidence linking, and approval.
6. **Legal density without visual noise.** Progressive disclosure keeps the primary task readable while retaining inspectable detail.

---

## 2. Repository Analysis and Product Understanding

### 2.1 Actual product purpose

**Verified.** VERITAS-600 is a specialized decision-control plane for an examining bank’s documentary-credit desk. It evaluates presentations under ICC UCP 600 and ISBP 745, synthesizes documentary compliance and regulatory risk, produces one of three operational artifacts, and requires human authorization before dispatch.

It addresses three expensive failure classes:

- wrongful dishonor caused by strict textual matching of harmless variations;
- erroneous honour caused by an LLM smoothing over objective math/date failures;
- regulatory leakage when facially compliant documents hide TBML pricing anomalies or sanctions relationships outside the document packet.

The product is not autonomous in the sense of uncontrolled execution. It automates evidence preparation and recommends an action; authority remains with the examiner.

### 2.2 What makes the architecture distinctive

**Verified from code.**

- `UCP600DeterministicEngine` performs expiry, presentation-window, shipment-date, drawing-limit, invoice arithmetic, cover-note, insurance coverage/date, and cross-document weight checks.
- `UCP600LegalAdjudicator` uses Nemotron responses for bounded lexical/legal questions and then enforces the hard invariant: a deterministic failure locks the final verdict to `DISCREPANT`.
- `AmendmentMemoryEngine` resolves accepted, rejected, pending, implicitly accepted, and partially accepted MT707 amendments under UCP 600 Art. 10(c)/(e), producing an active-terms SHA-256 fingerprint.
- `ZetarisFederationClient` performs a join-safe query over LC/amendment data, customs Parquet benchmarks, and OpenSanctions data, returning exactly one row and a federation receipt. It truthfully identifies `LIVE_ZETARIS` or `LOCAL_DUCKDB_FALLBACK`.
- `MeterlessRouter` creates six focused context packets and a measurable token-routing manifest.
- `DocumentExtractor` returns typed fields, confidence, normalized bounding boxes, source digests, and one of `LIVE_NEMOTRON_VLM`, `CACHED_REPLAY`, or `STRUCTURED_FIXTURE`.
- `BankDecisionEngine` selects exactly one of `APPROVE_HONOUR`, `ISSUE_MT734_REFUSAL`, or `COMPLIANCE_HOLD_AML`.
- `ArtifactGenerator` emits a settlement voucher, SWIFT MT734, or AML escalation dossier.
- Merkle, canonical JSON, hash-chain, evidence, money, and decision-receipt modules provide cryptographic audit primitives.

### 2.3 Current data and execution sequence

```text
Scenario JSON / documents
        │
        ├─ Stage 1: resolve MT700 + MT707 active terms; route six context chunks
        ├─ Stage 2: query PostgreSQL + Parquet + OpenSanctions through federation
        ├─ Stage 3: calculate deterministic UCP checks
        ├─ Stage 4: perform bounded legal-semantic adjudication + extraction
        └─ Stage 5: select action, generate artifact, hash evidence and decision
                                      │
                                      ▼
                           PENDING_HUMAN_SIGN_OFF
                                      │
                          examiner approves action
                                      ▼
                    signed receipt + dispatched status
```

### 2.4 Present implementation truth and limitations

These findings govern what the redesign may claim.

| Finding | Verified reality | UX consequence |
|---|---|---|
| Authentication | No sign-in route, session, RBAC, or authenticated identity exists. The approval endpoint accepts a free-text examiner name. | Do not design or claim sign-in as current functionality. Label identity entry as a demo examiner attestation. Production authentication is a future backend prerequisite. |
| Persistence/history | Examination state is held in `_RUN_STORE` in process memory; schema includes an audit table, but the current endpoint path does not persist runs to it. | Do not add a functional case-history route. A run summary may exist only for the current session. |
| Extraction mode | `DocumentExtractor` currently reports `STRUCTURED_FIXTURE`; the UI button says “Live Nemotron OCR.” | Rename to “Extract document fields,” and show the returned execution mode at the point of evidence. Never imply live VLM use when fixture-backed. |
| Bounding boxes | Backend returns normalized boxes; current viewer does not render document images or boxes. | A coordinate overlay is a valid presentation-layer enhancement, but only if the source document visual is available. Otherwise show a field-location schematic labeled as structured evidence. |
| Sponsor health | Header health is configuration-derived; actual per-run execution mode is returned later in stage events/receipts. | Separate “configured/ready” from “observed this run.” The latter owns the authoritative badge. |
| Preclusion clock | Current values begin at hard-coded `3d 14h 42m` and decrement minutes; no banking calendar is exposed. | Label as “demo countdown / estimate,” or replace with static legal deadline context until a bank calendar source exists. Never present it as authoritative. |
| Error handling | Most frontend failures are logged to the console. | Add visible, recoverable inline errors and preserve completed stages on retry. |
| SSE lifecycle | The EventSource is returned but not retained/cancelled on case changes or unmount. | Refactor frontend stream ownership; abort stale runs and prevent cross-case updates. Backend contract stays unchanged. |
| Evals fallback | `/evals` contains bundled fallback rows when the API is unavailable. | Clearly label results as “observed run” or “bundled reference dataset.” Never blend the two. |
| Theme | Root forces `.dark`; no light mode or theme persistence exists. | Implement light-first tokens plus explicit dark/system selection without changing product behavior. |
| Mobile | One-column CSS is present, but `h-screen`, `overflow-hidden`, and pane heights make narrow-screen work fragile. | Replace with task-based mobile navigation and normal document flow. |

### 2.5 Baseline verification

**Observed 23 October 2026.**

- Backend: `33 passed in 5.57s` using `.\.venv\Scripts\pytest.exe apps/api/tests/ -q`.
- Frontend: production build completed successfully on Next.js `15.5.28`.
- Static routes: `/`, `/_not-found`, `/evals`.
- First-load JavaScript reported by the build: `/` 120 kB, `/evals` 115 kB.

These are migration regression baselines, not post-redesign targets.

---

## 3. Existing Functionality Inventory

### 3.1 User-facing routes

| Route | Current role | Data source | Primary actions | Important states |
|---|---|---|---|---|
| `/` | Three-pane examination terminal | health, scenarios, scenario detail, extraction, SSE examination, approval | choose scenario; extract fields; examine; inspect rules/amendments/federation; inspect artifact; sign off; open SQL drawer | initial fetch, scenario loading, idle, extracting, five streaming stages, decision ready, approval pending, approving, approved; errors currently console-only |
| `/evals` | Three-architecture benchmark comparison | cached API result or bundled fallback; POST run | filter dataset; run benchmark; return to workbench | loading current result, reference fallback, running, success, failure fallback |

No landing, auth, onboarding, settings, history, admin, upload, or queue route exists today. **Redesign recommendation:** make `/` the new public landing page and relocate the preserved terminal UI to `/examine`; keep `/evals` unchanged. This is a route migration, not a claim that the landing page already exists. Authentication and the other unsupported product areas remain out of scope.

### 3.2 API contracts to preserve

| Method and path | Function | UI consumer |
|---|---|---|
| `GET /api/v1/health` | API and sponsor configuration telemetry | global status rail |
| `GET /api/v1/scenarios` | three scenario summaries | case selector |
| `GET /api/v1/scenarios/{lc_id}` | full LC packet | evidence workspace |
| `POST /api/v1/extract/{lc_id}` | document field extraction | evidence viewer |
| `GET` or `POST /api/v1/examine/{lc_id}?stream=true` | five-stage SSE examination | decision spine and workbench |
| `POST /api/v1/examine/{lc_id}/approve-action` | examiner attestation and receipt | sign-off gate |
| `GET /api/v1/evidence/sponsors/{lc_id}` | sponsor receipts and stage manifest | provenance drawer |
| `POST /api/v1/evals/run` | execute ten-scenario comparison | evaluation page |
| `GET /api/v1/evals/results` | retrieve/cache comparison | evaluation page |

### 3.3 Existing component map

| File/component | Preserved capability | Redesign issue |
|---|---|---|
| `HeaderBar.tsx` | identity, scenario selector, clock, sponsor badges, eval link | overcrowded; hard-coded cases; configured and observed status conflated; synthetic clock |
| `DocumentViewerPane.tsx` | five document tabs, packet fields, amendments, extraction request | no visible extraction result, provenance, box linking, empty/error states, or true document canvas |
| `AdjudicationMatrixPane.tsx` | deterministic/legal findings, amendment snapshot, federation risk | pipeline stage progress and evidence relationships are weak; tabs hide the causal chain |
| `DecisionActionPane.tsx` | decision, advisory, artifact, copy, sign-off, receipt | action and proof compete vertically; no confirmation step; failure silent; comments are not editable in UI |
| `ZetarisDrawer.tsx` | architecture explanation and query inspection | no dialog semantics/focus trap; SQL is duplicated static text instead of using receipt/query response |
| `evals/page.tsx` | KPIs, filters, row comparison, architecture explanation | data provenance ambiguous; table overload on mobile; visual hierarchy resembles generic SaaS cards |

### 3.4 Golden scenarios

| Case | What the user must understand | Result |
|---|---|---|
| `LC-2026-8841` | accepted amendment becomes active; pending amendment stays quarantined; “Mashine” is protected by ISBP 745 A23; general B/L description is allowed by Art. 14(e) | `APPROVE_HONOUR` |
| `LC-2026-9104` | insurance is 108%, failing the 110% threshold by $9,600; packing/B/L weight conflict; cure economics save $11,100 | `ISSUE_MT734_REFUSAL` |
| `LC-2026-9920` | paper documents pass, but customs-price anomaly and sanctions match outrank documentary compliance | `COMPLIANCE_HOLD_AML` |

### 3.5 State inventory and recovery contract

Every major module must implement the following common state vocabulary:

| State | Required behavior |
|---|---|
| Default | clear primary action and source status; no placeholder data masquerading as results |
| Hover | subtle border/underline or elevation; never the only cue |
| Focus-visible | 2 px high-contrast outline with 2 px offset; not clipped by panes |
| Pressed | 1–2 px optical depression or background shift; no scale below 0.98 |
| Selected | persistent shape + icon/text, not color alone |
| Loading | skeleton that preserves layout; label the real operation |
| Streaming | stage-local pulse and live region; completed evidence stays stable |
| Success | concise status plus next action; preserve receipt/provenance |
| Warning | describe consequence and available intervention |
| Failure | name failed operation, retain completed work, offer retry |
| Empty | explain why empty and what creates content |
| Disabled | visible reason via adjacent text/tooltip; no unexplained low opacity |
| Interrupted | show last completed stage and restart semantics |
| Retry | retry only the safe client operation where possible; a new examination creates a visibly new run |

---

## 4. Hackathon Context and Verified Requirements

### 4.1 Publicly verified event facts

As of 23 October 2026, the public event page verifies:

- fully online, teams of 1–5, build window 22–27 October 2026;
- submission deadline 27 October 2026 at 23:45 UTC;
- Track 03 asks entrants to turn data, knowledge, memory, and reasoning into reliable decisions and actions;
- scoring: Impact 30, Technical 20, Innovation 15, Demo 15, Product & UX 10, Sponsor Tech 10;
- public Academy guidance describes a production-oriented agent, not another chatbot;
- public Academy guidance identifies Zetaris, Cursor, Meterless, and NVIDIA Nemotron as sponsor technologies;
- public Academy FAQ calls for a 1–4 minute demo video, slide deck, GitHub repository/README, and sponsor-technology explanation.

The authenticated “How the Week Runs” lesson and any materials not publicly exposed were not accessed. Their detailed contents must not be represented as verified.

### 4.2 Design implications of scoring

| Criterion | UI proof to surface |
|---|---|
| Impact, 30 | preclusion risk, wrongful-dishonor prevention, $9,600 shortfall, $11,100 demurrage savings, AML freeze |
| Technical, 20 | hard invariant, one-row federation, stage receipts, execution mode, Merkle/decision hashes |
| Innovation, 15 | evidence-carrying neuro-symbolic split and amendment-state resolution |
| Demo, 15 | three cases, each with one unmistakable reveal and no setup dead time |
| Product & UX, 10 | examiner-first hierarchy, keyboard operation, error recovery, light/dark quality |
| Sponsor Tech, 10 | contribution and observed mode for each sponsor—not logos alone |

---

## 5. Track Selection and Rationale

### 5.1 Weighted fit comparison

Scores are out of 5; weights reflect this product’s evidence, not official scoring weights.

| Dimension | Weight | Track 02: Explain Why | Track 03: Reasoning Architecture |
|---|---:|---:|---:|
| Match to implemented multi-stage architecture | 30% | 4.0 | 5.0 |
| Decision/action outcome | 20% | 3.5 | 5.0 |
| Memory/state differentiation | 15% | 3.5 | 5.0 |
| Evidence/provenance strength | 15% | 5.0 | 4.5 |
| Sponsor integration narrative | 10% | 4.5 | 5.0 |
| Demo distinctiveness | 10% | 4.0 | 5.0 |
| **Weighted score** | **100%** | **4.05** | **4.93** |

### 5.2 Recommendation

Submit to **Track 03 — Reasoning Architecture**. The application does explain why, but explanation is a property of its deeper contribution: state is resolved, data is federated, deterministic and neural authorities are separated, a decision lattice selects an operational action, and a human authorizes it. Track 02 would understate the system as an answer-with-sources product.

The interface should nevertheless borrow Track 02’s strongest standard: every conclusion must remain traceable to evidence and provenance.

---

## 6. Contemporary UI/UX Research (Through October 2026)

### 6.1 Research synthesis

**Verified research directions, translated rather than copied:**

- Award platforms still reward bold typography, immersive storytelling, and distinctive interaction, but the strongest transferable lesson is coherence between interaction and product promise. Cyera AI Guardian, for example, makes security claims tangible through task-specific interactions; its reported keyboard-focus gaps are also a warning against spectacle without access.
- Linear’s 2026 changes continue to emphasize scanability, keyboard access, live agent status, visible attribution, and version history. The transferable lesson is dense productivity with state clarity.
- Vercel Observability treats complex execution as queryable event streams. The transferable lesson is that system state becomes understandable when events, sources, latency, and relationships share one visual grammar.
- Palantir documentation foregrounds lineage and controls that travel with data. The transferable lesson is persistent provenance, not its visual styling.
- Microsoft HAX recommends setting capability expectations, exposing controls, scoping behavior when uncertain, and making reasons available. It also warns that explanations can create automation bias.
- Google PAIR recommends progressive disclosure, trust calibration, and explanations optimized for understanding rather than completeness.
- Figma’s 2026 material reinforces that AI accelerates production but a coherent point of view and design-system grounding prevent divergence.

### 6.2 Product-level conclusions

1. The primary unit is a **case**, not a conversation.
2. The primary visualization is a **decision chain**, not an animated neural network.
3. Confidence is useful only for semantic findings and must include the meaning of the number; deterministic checks use pass/fail plus computed values.
4. Sponsor status needs two layers: service readiness and observed run execution.
5. Explanation should open beside the affected evidence, not in a detached “AI reasoning” wall of text.
6. The most expressive motion belongs in the demo prelude and decision transition; the examination workspace remains still enough for legal review.
7. Light mode is particularly appropriate for documents, annotation, and courtroom/ledger associations. Dark mode is an operational night shift, not a color inversion.

### 6.3 Research limitations

- Award galleries show presentation craft, not evidence that a pattern works for bank examiners.
- Public trade-finance interfaces expose little about internal examiner workflows.
- No direct interviews or contextual inquiries with documentary-credit examiners were performed for this plan.
- The proposed hierarchy therefore combines code-derived task analysis with general human–AI evidence. It must be validated with real practitioners.

---

## 7. Reference Study With Links

| Reference | What to learn | What not to copy |
|---|---|---|
| [Open Agent Hackathon event](https://hackathon.genai.works/event/open-agent-hackathon-2026) | explicit track language, judging weights, demo constraints | sponsor-logo theater |
| [Microsoft HAX Guidelines](https://www.microsoft.com/en-us/haxtoolkit/ai-guidelines/) | capability setting, control, recovery, explanations | explanation as automatic proof of correctness |
| [Google PAIR Explainability + Trust](https://pair.withgoogle.com/guidebook-v2/chapter/explainability-trust/) | progressive disclosure and calibrated reliance | unexplained confidence percentages |
| [Linear changelog](https://linear.app/changelog) | dense scanability, keyboard-first interaction, agent status and attribution | monochrome imitation or issue-tracker IA |
| [Vercel Observability](https://vercel.com/docs/observability) | event/source/latency relationships | generic infrastructure charts unrelated to legal work |
| [Palantir data lineage](https://www.palantir.com/docs/foundry/data-lineage/overview) | provenance as a persistent property | military visual language or black-box “ontology” branding |
| [Cyera AI Guardian award study](https://www.designrush.com/best-designs/websites/cyera-ai-guardian-website-design) | product claim made tangible through interaction | continuous WebGL, game mechanics, or inaccessible canvas controls in the examiner workspace |
| [CSS Design Awards](https://www.cssdesignawards.com/) | current craft bar and the separation of UI, UX, innovation | novelty without task relevance |
| [Radix accessibility guidance](https://www.radix-ui.com/primitives/docs/overview/accessibility) | accessible behavior and focus management in unstyled primitives | default visual identity |
| [Motion for React](https://motion.dev/docs/react) | layout continuity, restrained state motion, reduced-motion hook | animating every card entrance |
| [WCAG 2.2](https://www.w3.org/TR/WCAG22/) | normative accessibility target | treating automated checks as complete conformance |
| [Core Web Vitals](https://web.dev/articles/vitals) | measurable loading, interactivity, and stability thresholds | optimizing lab scores while ignoring demo reliability |

All links accessed 23 October 2026.

---

## 8. Common AI-Generated Design Patterns to Avoid

### Anti-Generic-AI checklist

- [ ] No centered gradient headline floating above interchangeable bento cards.
- [ ] No purple-blue neon field, glowing orb, particle fog, or decorative neural lattice.
- [ ] No chatbot as the primary control for a case-based workflow.
- [ ] No sparkle icon as a universal synonym for AI; use it only if it conveys a bounded semantic operation, preferably not at all.
- [ ] No glassmorphism over high-density legal content.
- [ ] No identical rounded cards for every information type.
- [ ] No meaningless animated graphs or fabricated real-time telemetry.
- [ ] No “100% confidence” treatment for deterministic correctness or system trust.
- [ ] No status communicated by color alone.
- [ ] No sponsor logos without an inspectable contribution/receipt.
- [ ] No streaming “thoughts” that suggest private chain-of-thought. Show stage events, inputs, outputs, rules, and evidence actually returned by the system.
- [ ] No fake upload, auth, history, or admin experiences.
- [ ] No fixed desktop screenshot masquerading as responsive design.
- [ ] No animation that delays examination, approval, or error recovery.
- [ ] No vague copy such as “AI-powered insights.” Name the rule, source, computation, and authority.

### Approved recurring motifs

- ruled ledger lines representing ordered evidence;
- registration marks and folio numbering for document identity;
- a single vertical decision spine for execution state;
- legal marginalia for citations;
- seals only for cryptographically bound receipts;
- cargo-route geometry only when it encodes document or data-source relationships.

---

## 9. Target Users and UX Research

### 9.1 Primary persona: senior documentary-credit examiner

**Evidence-supported profile.** Works under deadline, compares fields across multiple documents, needs exact citations, and remains accountable for refusal/honour. Likely expert in trade finance but not interested in model internals.

- Goal: reach a defensible disposition quickly.
- Needs first: case deadline, high-risk blockers, source evidence, applicable rule, operational next step.
- Frustrations: duplicate review, amendment ambiguity, noisy alerts, weak provenance, and opaque AI language.
- Trust concern: an apparently fluent system can still be wrong on arithmetic or legal authority.

### 9.2 Secondary persona: compliance/AML officer

- Goal: establish why a facially compliant transaction was held.
- Needs first: sanctions entity, relationship, price anomaly basis, data sources, execution mode, and a non-MT734 escalation artifact.
- Trust concern: false positives, source recency, fallback data, and leakage of sensitive case information.

### 9.3 Secondary persona: desk head / authorizer

- Goal: review high-severity evidence and approve the operational action.
- Needs first: decision, blocking facts, immutable hashes, artifact preview, and what approval will dispatch.
- Trust concern: signing a stale run or an action whose evidence changed.

### 9.4 Secondary persona: hackathon judge

- Goal: determine novelty, truthfulness, sponsor use, and product viability within minutes.
- Needs first: one real problem, visible architecture, one dramatic but credible edge case, and proof the system is not a scripted chatbot.

### 9.5 Jobs to be done

1. When documents arrive, resolve the legally active credit terms.
2. Compare objective fields without arithmetic or date ambiguity.
3. Interpret only the lexical/legal divergences that require semantic judgment.
4. check external regulatory context the document packet cannot reveal.
5. produce the right operational artifact and preserve all discrepancies in a single refusal.
6. authorize or stop the action with an accountable human record.

### 9.6 Research hypotheses to validate

- Examiners may prefer a document-first split view over a pipeline-first overview.
- Expert users may want citations always visible while novices prefer progressive disclosure.
- A confidence number may add less value than evidence strength and source mode.
- Mobile is likely review-only rather than full examination, but the app must remain functional.

### 9.7 Measurable usability goals

- 90% of first-time users identify the three action outcomes within 30 seconds.
- 90% correctly state that deterministic failures cannot be overridden after one case run.
- An examiner locates the source evidence for a failed check within 10 seconds.
- A user can complete examination and sign-off using keyboard only.
- No participant confuses fallback/fixture data with a live sponsor call.
- A judge can explain all four sponsor contributions after the 90-second journey.

---

## 10. Information Architecture and User Journeys

### 10.1 Proposed information architecture

```text
VERITAS-600
├── Product Story (/)
│   ├── Evidence-to-action hero
│   ├── Failure problem
│   ├── Hard invariant
│   ├── Guided LC-2026-9104 demonstration
│   ├── Five-stage architecture
│   ├── Three possible bank actions
│   └── Proof, benchmark, and entry CTA
├── Case Room (/examine)
│   ├── Case switcher
│   ├── Evidence desk
│   ├── Decision spine
│   ├── Findings ledger
│   ├── Action docket
│   ├── Source & sponsor receipt drawer
│   └── Human sign-off dialog
└── Architecture Evals (/evals)
    ├── Benchmark summary
    ├── Architecture comparison
    ├── Scenario ledger
    └── Run benchmark
```

The new `/examine` route is required because `/` becomes the first-impression story. Move the existing terminal composition; do not fork or duplicate its logic. A legacy bookmark to `/` now reaches a clear `Open examination` CTA in one action. There is still no fake onboarding or account flow.

### 10.2 Primary examiner journey

```text
Select case → verify packet identity → start examination → watch stages settle
      → open blocker → inspect field + computation + citation
      → review recommended action and artifact → attest identity/comments
      → confirm dispatch → preserve signed receipt on screen
```

Context preservation rules:

- Selecting a finding highlights its evidence without switching the user to an unrelated route.
- Changing document tabs retains the selected finding.
- Opening provenance uses a non-destructive side sheet; closing it returns focus to the trigger.
- A stream interruption leaves completed stages and provides “Start new run,” never silently resumes as if continuous.
- Changing case cancels/ignores the old stream and resets case-bound approval state.

### 10.3 First-time judge journey

The landing page offers a 90-second path: complete the predefined guided demonstration, then choose `Open this case in the terminal`. The terminal receives `?case=LC-2026-9104&tour=1`; prompts advance only when the relevant real action occurs.

### 10.4 Returning-user continuity

With no server history, continuity is limited to browser-local presentation preferences: theme, pane sizes, reduced-density choice, last open evidence tab, and dismissed tour. Never store case documents, decisions, examiner names, or receipts in local storage.

---

## 11. Three Creative Directions

### Direction A — Evidence Ledger

- **Concept:** a contemporary documentary-credit register where evidence, rules, and authorization occupy one continuous chain of custody.
- **Personality:** precise, editorial, calm, institutional, quietly tactile.
- **Color:** warm mineral paper, deep green-black ink, oxidized copper action, restrained legal blue, semantic red/amber/green.
- **Typography:** Newsreader for high-level decisions and citations; Inter for UI; IBM Plex Mono for fields, hashes, SQL, and money.
- **Layout:** asymmetric evidence desk with a narrow decision spine and a stable action docket; fine rules replace card grids.
- **Motion:** ink-line draws, evidence-link travel, paper-layer shifts, and seal confirmation; no ambient animation.
- **Agentic metaphor:** a ledger entry progressing from evidence to authorized action.
- **Strengths:** domain-specific, light-mode native, explains provenance, credible for banks, memorable without novelty overload.
- **Weaknesses:** can feel conservative if typography and motion lack craft.
- **Originality:** high for an AI product because identity comes from banking evidence rather than “AI.”
- **UX risk:** overusing document metaphors may reduce density.
- **Accessibility:** strong; generous contrast and stable surfaces are natural.
- **Hackathon fit:** excellent; technical proof reads clearly on camera.

### Direction B — Port Control Nightwatch

- **Concept:** a maritime operations room that treats cases like vessel movements through checkpoints.
- **Personality:** cinematic, urgent, operational, dark-first.
- **Color:** midnight navy, radar green, signal amber, hazard red, phosphor cyan.
- **Typography:** condensed grotesk headings, neutral sans body, technical mono.
- **Layout:** panoramic map-like workspace and horizontal stage checkpoints.
- **Motion:** sweep lines, tracking brackets, scanning reveals, route traces.
- **Agentic metaphor:** cargo passes through inspection gates.
- **Strengths:** dramatic demo; strong tie to shipping documents and sanctions.
- **Weaknesses:** dark-first conflicts with brief; can resemble defense software or cyber dashboards.
- **Originality:** medium-high, but radar/control-room tropes are common.
- **UX risk:** visual urgency can exaggerate routine states and fatigue examiners.
- **Accessibility:** harder color and motion calibration.
- **Hackathon fit:** high spectacle, weaker day-to-day credibility.

### Direction C — Cryptographic Codex

- **Concept:** a modern legal codex where each rule, evidence leaf, and signature forms a verifiable folio.
- **Personality:** cerebral, austere, archival, premium.
- **Color:** ivory, carbon, vermilion, ultramarine, metallic foil accents.
- **Typography:** dominant serif with monospaced annotations.
- **Layout:** page spreads, marginal notes, collapsible proof trees.
- **Motion:** page turns, proof-tree assembly, emboss/seal transitions.
- **Agentic metaphor:** an illuminated rulebook that compiles a case.
- **Strengths:** beautiful citation and proof treatment; highly differentiated.
- **Weaknesses:** weaker operational speed and data density.
- **Originality:** very high.
- **UX risk:** book mechanics can become ornamental; mobile page spreads are awkward.
- **Accessibility:** page-turn motion and reading order require careful alternatives.
- **Hackathon fit:** memorable, but may obscure sponsor execution.

### 11.4 Weighted decision framework

| Criterion | Weight | Evidence Ledger | Port Control | Cryptographic Codex |
|---|---:|---:|---:|---:|
| Examiner usability | 25% | 4.8 | 4.0 | 3.7 |
| Architectural legibility | 20% | 4.9 | 4.3 | 4.2 |
| Distinctiveness | 15% | 4.6 | 4.2 | 4.9 |
| Light/dark parity | 10% | 5.0 | 3.5 | 4.7 |
| Accessibility | 10% | 4.8 | 3.7 | 4.0 |
| Performance feasibility | 10% | 4.8 | 3.7 | 4.1 |
| Demo impact | 10% | 4.7 | 4.8 | 4.4 |
| **Weighted total / 5** | **100%** | **4.80** | **4.06** | **4.20** |

**Selected:** Direction A, Evidence Ledger. Do not dilute it with radar visuals or page-turn navigation. Borrow only the Codex’s restraint for proof details and the Nightwatch’s sense of consequence for AML states.

---

## 12. Selected Art Direction and Design Rationale

The Evidence Ledger converts the architecture into one recognizable product grammar:

- **Evidence** appears on paper-like source surfaces with folio numbers.
- **Rules** appear as margin annotations attached to the exact field/computation.
- **Authority** appears as a squared origin stamp: `PYTHON`, `NEMOTRON`, `ZETARIS`, `MEMORY`, `HUMAN`.
- **State** moves down a vertical spine and never resets completed stages to a spinner.
- **Decisions** appear as a docket with a plain-language action first and system enum second.
- **Cryptographic proof** appears only after the evidence exists, and the seal appears only after human sign-off.

This language is product-specific, supports the light-first requirement, works at high information density, and remains implementable with HTML, CSS, SVG, and one small motion library.

### Signature moment

When the decision becomes ready, no confetti or glow appears. The five stage marks align into one rule; the decisive evidence rows gain a shared left edge; the action docket slides into its fixed place. On approval, a thin circular seal draws once around the receipt fingerprint, then becomes static. Reduced motion replaces both with immediate state changes.

### Copy voice

- Use active, literal sentences: “Insurance is $9,600 below the required minimum.”
- Put legal citation after the fact, not before it.
- Use “system recommends” until human authorization; use “authorized” only after receipt creation.
- Use “observed in this run,” “cached replay,” “structured fixture,” and “local fallback” exactly.
- Avoid “intelligent,” “smart,” “magic,” “autonomous approval,” and “100% trustworthy.”

---

## 13. Brand and Visual Identity

### Product position

**VERITAS-600 is an evidence-led examination terminal for documentary trade finance.** It is not a generic AI workspace and must not visually imitate a chat product. The identity should communicate legal precision, operational calm, provenance, and human accountability.

### Naming hierarchy

- Product mark: `VERITAS—600`, set as a compact wordmark with an em-rule representing the evidence chain.
- Descriptor: `Documentary Credit Examination Terminal`.
- Case identifier: always `LC-YYYY-NNNN`; it is the primary locator in every view.
- Action language: human-readable label first—“Approve honour,” “Issue refusal,” “Place compliance hold”—with the exact machine enum beneath or beside it.
- Sponsor names remain service/source labels, never decorative endorsements.

### Mark and favicon

Create a code-native SVG monogram from a `V`, a vertical rule, and three aligned evidence ticks. The mark must remain legible at 16 px, use `currentColor`, and have a one-color form. Do not generate a raster logo, shield, robot, scales-of-justice cliché, or bank-building icon. The favicon may reduce to the vertical rule and two ticks.

### Typography

Use self-hosted variable fonts to avoid third-party runtime requests. Confirm licenses before committing font files.

| Role | Family | Use | Rules |
|---|---|---|---|
| Editorial/display | **Newsreader** | Product name, case title, decision heading, sparse section titles | 500–650 weight; never below 22 px; no all-caps paragraphs |
| Interface | **Inter** | Navigation, controls, narrative copy, tables | 400/500/600; optical sizing enabled where supported |
| Evidence/data | **IBM Plex Mono** | IDs, amounts, dates, hashes, SQL, telemetry, legal refs | 400/500; tabular numerals; hashes may wrap at safe delimiters |

Fallback stacks must render safely before fonts load: `Georgia, Cambria, serif`; `Inter, ui-sans-serif, system-ui, sans-serif`; and `"IBM Plex Mono", ui-monospace, SFMono-Regular, Consolas, monospace`. Subset to Latin if the shipped scenarios remain Latin-only; add glyph coverage only when product data requires it.

### Iconography

Retain Lucide React because it is already installed. Standardize on 16, 18, and 20 px icons with 1.75 px strokes. Icons clarify action or status but never carry meaning alone. Legal references, source origin, and statuses use text plus shape. Avoid mixed filled/outline families and avoid decorative icons in every heading.

### Imagery and texture

The primary texture is structural, not illustrative: 1 px ledger rules, restrained folio marks, and a subtle paper grain rendered as a tiny local CSS/data texture at less than 2% opacity. Document previews use their real extracted source surfaces when available. Do not use stock photography, glassmorphism, generated legal imagery, animated gradients, or a background grid behind all content.

### Sonic and haptic identity

None in v1. A compliance workflow should not play success sounds, and browser haptics are inconsistent. Visual and assistive announcements are sufficient.

---

## 14. Complete Light/Dark Design System

### 14.1 Theme tokens

Implement semantic CSS custom properties on `:root` and `[data-theme="dark"]`. These are design targets; run automated and manual contrast checks against the final rendered fonts and sizes before accepting them.

| Token | Light | Dark | Intended use |
|---|---|---|---|
| `--canvas` | `#F3F0E7` | `#0D1413` | Application background |
| `--surface` | `#FFFDF7` | `#131C1A` | Primary work surfaces |
| `--surface-raised` | `#FFFFFF` | `#192421` | Popovers, drawers, focused docket |
| `--surface-subtle` | `#EAE7DD` | `#202C29` | Quiet grouped areas |
| `--ink` | `#17201E` | `#F2F0E8` | Primary text |
| `--ink-muted` | `#56615D` | `#AEB8B2` | Secondary text |
| `--rule` | `#CBD0C8` | `#34413D` | Dividers and field borders |
| `--rule-strong` | `#929D97` | `#61706B` | Focused structural rules |
| `--registry` | `#123D38` | `#8FD5C5` | Product/nav primary |
| `--registry-ink` | `#FFFFFF` | `#07120F` | Text on registry |
| `--copper` | `#A24D2C` | `#DF8B64` | Human action/sign-off accent |
| `--info` | `#245F86` | `#7DB8DE` | Informational state |
| `--success` | `#0B684E` | `#70C7A7` | Compliant/complete |
| `--warning` | `#8A5A00` | `#E7B85C` | Advisory/pending |
| `--danger` | `#A23232` | `#F28B82` | Discrepancy/refusal |
| `--neural` | `#684B78` | `#C3A4D0` | Semantic/LLM authority |
| `--focus` | `#005FCC` | `#9CCBFF` | Keyboard focus ring |

Rules:

- Light is the default and first paint. Dark is a full semantic mapping, not color inversion.
- `color-scheme: light dark` follows the selected theme so native controls match.
- Status backgrounds are light tints; text uses the strongest status token. Never place light token text on a light tint without contrast verification.
- Deterministic and neural checks must differ by label and icon in addition to color.
- Local fallback and replay modes use a diagonal hatch or outlined badge, not a warning-red treatment unless they cause an actual failure.

### 14.2 Type scale

| Token | Size / line-height | Typical use |
|---|---|---|
| `display` | `clamp(2rem, 3vw, 3.5rem) / 1.02` | Judge prelude only |
| `h1` | `clamp(1.75rem, 2.2vw, 2.5rem) / 1.08` | Case/decision title |
| `h2` | `1.5rem / 1.2` | Major workbench section |
| `h3` | `1.125rem / 1.3` | Panel heading |
| `body` | `0.9375rem / 1.55` | Primary copy |
| `small` | `0.8125rem / 1.45` | Metadata |
| `micro` | `0.6875rem / 1.35` | Uppercase source labels only |
| `data` | `0.8125rem / 1.45` mono | IDs, amounts, telemetry |

Do not reduce body copy below 14 px on any viewport. Use `font-variant-numeric: tabular-nums` for money, percentages, elapsed time, and table columns.

### 14.3 Spacing, geometry, and elevation

- Base spacing unit: 4 px. Core sequence: 4, 8, 12, 16, 24, 32, 48, 64.
- Workbench gutters: 16 px phone, 24 px tablet, 32 px desktop, 48 px wide desktop.
- Reading width: 68–76 characters for narrative; evidence tables may use the available column width.
- Radii: 2 px for stamps, 4 px for controls, 8 px for drawers/dockets. No 20–32 px “friendly SaaS” cards.
- Borders: 1 px default, 2 px selected/decisive. Horizontal ledger rules do most grouping.
- Shadow: only raised transient layers: `0 12px 40px rgb(12 22 19 / 14%)`; dark equivalent at 35%. Static panels use borders, not floating card shadows.
- Minimum target: 44×44 CSS px on touch; compact desktop table controls may be 36 px only when an adjacent accessible alternative exists.

### 14.4 Layout primitives

- `AppFrame`: masthead, route rail, telemetry strip, main landmark.
- `CaseMasthead`: case switcher, parties/amount, deadline, current recommendation.
- `DecisionSpine`: five sequential agent stages and their evidence lineage.
- `EvidenceFolio`: document/source area with page, source, extraction mode, and digest.
- `RuleMatrix`: deterministic and semantic findings grouped by authority.
- `DecisionDocket`: recommendation, decisive reasons, action consequences, approval gate.
- `ProofDrawer`: federation query/receipt, sponsor telemetry, or cryptographic chain.
- `NoticeRegion`: errors, completion notices, and assistive live updates.

At 1440 px and above, the terminal uses a 12-column grid: evidence 5 columns, decision spine 3, docket 4. At 1024–1439 px: evidence 5, combined reasoning 7 with a sticky docket section. Below 1024 px, one content column plus tabs/segmented navigation prevents unusable horizontal compression.

### 14.5 Component specification

| Component | Visual/behavioral contract | Required states | Accessibility/mobile |
|---|---|---|---|
| Primary action | Copper fill only for the human-gated final action | idle, hover, focus, pending, success, disabled | Verb-led label; pending remains readable; 44 px target |
| Secondary action | Ink outline, surface fill | same plus selected | Never compete with approval action |
| Destructive action | Danger outline/fill only where consequence is destructive | idle, confirm, pending, error | Confirmation names the exact consequence |
| Theme toggle | Sun/moon icon plus accessible name | system, light, dark | Three-state menu; selection persists locally |
| Telemetry badge | Source stamp + explicit mode string | live, cached, fallback, unavailable | Tooltip expands meaning; text remains visible |
| Authority stamp | Square icon, source label, optional model/version | Python, Nemotron, Zetaris, Meterless, Human | Not color-dependent |
| Stage row | Index, name, status, duration, summary | queued, active, complete, warning, error | `aria-current="step"`; textual status; mobile accordion |
| Rule row | Fact, expected value, observed value, citation, authority | compliant, discrepant, advisory, unavailable | Table semantics on wide; definition list on narrow |
| Evidence anchor | Box/page reference and source digest | idle, hover/focus, selected, unavailable | Keyboard selects and scrolls source into view |
| Citation chip | Exact article label | default, selected | Opens local explanatory popover; not external legal advice |
| Decision docket | Recommendation and invariant explanation | waiting, recommended, blocked, authorized | Heading receives focus when state changes |
| Human approval form | Examiner name/sign-off statement and consequence | pristine, invalid, pending, accepted, rejected | Real labels, inline errors, summary, no placeholder-only fields |
| Receipt seal | Static proof mark after authorization | absent, drawing, complete | Reduced motion shows complete immediately; digest selectable |
| Drawer/dialog | Right-side proof inspection | opening, open, closing | Proper dialog name, focus trap, Escape, focus return |
| Toast/notice | Non-blocking state update | info, success, error | `role=status` except urgent errors use `alert`; never sole error location |
| Skeleton | Reserves known layout | loading | No shimmer under reduced motion; not used after SSE has begun |
| Empty state | Explains why and next available action | no selection, no result, unavailable | No decorative illustration required |

### 14.6 Status grammar

| State | Shape | Icon | Example language |
|---|---|---|---|
| Queued | Open circle | Clock | “Waiting for prior stage” |
| Active | Half-filled circle | Loader, rotates only with motion allowed | “Federating evidence” |
| Complete | Filled circle | Check | “5 deterministic checks complete” |
| Advisory | Diamond | Info | “Potential demurrage exposure” |
| Discrepant | Square | X | “Insurance cover is below 110%” |
| Blocked | Octagon | Hand | “Human authorization required” |
| Authorized | Double-ring seal | Signature/check | “Authorized by examiner” |
| Unavailable | Dashed circle | Minus | “Source unavailable” |

### 14.7 Content rules

- Sentence case everywhere except source stamps and exact enums.
- Never truncate the decisive discrepancy or legal citation.
- Pair an amount with currency and grouping: `$1,056,000`, not `1056000`.
- Pair percentages with their base: “108% of LC amount ($950,400).”
- Display dates as `23 Oct 2026` in prose and ISO `2026-10-23` in data/export contexts.
- Long hashes show first 12 and last 8 characters visually, while copy exposes the complete value.
- Tooltips supplement visible labels; they never contain essential evidence.

### 14.8 Focus, selection, loading, and error behavior

- Focus ring: 2 px `--focus` plus 2 px surface offset; visible on every interactive element.
- Selected evidence uses a 2 px left rule and `aria-selected`; focus and selection are distinct.
- Preserve completed SSE stages during later failures. Never revert the whole workbench to a generic spinner.
- Show an error at the failed stage, in the notice region, and beside the affected action. Include retry only when retry is safe.
- Switching cases while a stream runs first cancels/closes the prior stream, then clears case-scoped state. Do not allow late events into the newly selected case.
- Offline or API-unavailable benchmark rows must be visibly marked `BUNDLED DEMO DATA`; never silently merge them with live results.

---

## 15. Page-by-Page Redesign Specifications

The two verified experiences are preserved and a new public landing route is added. Authentication, onboarding, case history, settings, administration, and document upload remain out of scope until backend capabilities exist.

### 15.1 Global shell

The masthead has three horizontal zones:

1. Product mark and descriptor.
2. Route navigation: `Home`, `Examination`, and `Architecture benchmark`.
3. Global controls: theme, API state, and “About this evidence” disclosure.

A second, quieter telemetry strip shows the current run modes only when a case or evaluation has produced them. Before a run it says `Execution mode not yet observed`, preventing configuration-derived claims from appearing as run facts.

On mobile, the product name remains visible. The public landing uses a compact navigation drawer because it combines section anchors and route links; the application routes use a three-item inline route menu. Telemetry becomes a disclosure and never appears on the public landing before an observed run.

### 15.2 `/examine` — Examination terminal

#### Goal

Allow an examiner or judge to select a verified scenario, observe the agent pipeline, inspect decisive evidence, understand why a recommendation is bounded, and perform the explicit human-gated action.

#### Initial state

- Fetch scenario metadata from `GET /api/v1/scenarios`; do not hard-code selector options.
- Show the selected case masthead with parties, amount/currency, and concise scenario context.
- Main evidence area shows a neutral folio placeholder and available fixture/extraction facts.
- Decision spine shows all five stages as queued.
- Docket says “No recommendation yet” and describes the next action: “Run examination.”
- The primary pre-run button is `Run examination`. If extraction remains a separate supported call, expose `Inspect extraction` as a secondary action—not “Live Nemotron OCR,” because the current implementation reports `STRUCTURED_FIXTURE`.

#### Running state

- Keep the masthead and already-known evidence stable.
- Stream five stage events into the `DecisionSpine` in backend order.
- Each event adds its real telemetry, summary, and evidence anchors. Avoid simulated typing and artificial delays.
- The active stage expands; completed stages collapse to a one-line summary but remain inspectable.
- An unobtrusive elapsed timer may run, but it must be labeled wall-clock elapsed time, not the UCP banking-day deadline.
- Disable final action until the backend recommendation exists. Case switching remains available but invokes the stream-cancellation behavior.

#### Completed state

The layout rebalances around the result rather than showing a transient overlay:

- Evidence folio highlights the decisive document fields.
- Rule matrix orders findings by consequence: locked deterministic discrepancies, sanctions/TBML signals, semantic observations, advisories, then compliant checks.
- Decision docket names the recommended outcome, cites the decisive rules, shows operational impact, and states “Human authorization required.”
- Sponsor/source mode appears at point of use and in the proof drawer.

#### Case-specific narrative

**LC-2026-8841 — recommend honour**

- Lead: “Documents comply after accepted amendment context.”
- Show ISBP 745 Para A23 beside the non-material typographical difference.
- Show UCP 600 Art. 14(e) beside the general goods description accepted on the non-invoice document.
- The amendment ledger must distinguish accepted vs pending amendments under UCP 600 Art. 10(c) and 10(e).
- Final action: `Approve honour` / `APPROVE_HONOUR`.

**LC-2026-9104 — recommend refusal**

- Lead: “Insurance cover is $9,600 below the required minimum.”
- The calculation row must show required 110%, observed 108%, values, delta, deterministic `DISCREPANT`, and UCP 600 Art. 28(f)(ii).
- Weight mismatch is shown as a separate discrepancy, not collapsed into the insurance failure.
- `$11,100 potential demurrage avoided` remains advisory and cannot affect the legal verdict.
- Refusal evidence points to UCP 600 Art. 16(c)(iii); clock context references Art. 14(b) and Art. 16(f), while explicitly labeling any current demo countdown as illustrative until backed by a banking calendar.
- Final action: `Issue MT734 refusal` / `ISSUE_MT734_REFUSAL`.

**LC-2026-9920 — recommend AML hold**

- Lead: “Documents comply; external risk signals require compliance review.”
- Keep documentary compliance and AML/TBML risk as parallel lanes so users do not infer that sanctions heuristics rewrite UCP compliance.
- Show the watchlist/federated provenance and each actual risk signal; avoid implying a confirmed sanctions match when the data indicates a risk or hit requiring review.
- Final action: `Place compliance hold` / `COMPLIANCE_HOLD_AML`.

#### Human sign-off state

Selecting the final action opens a named modal or anchored docket expansion that includes:

- exact action and case;
- decisive reason summary;
- consequence statement;
- examiner name/sign-off input supported by the API;
- explicit acknowledgement checkbox if implemented in UI state (do not invent a backend field);
- cancel and authorize controls.

After `POST /api/v1/examine/{lc_id}/approve-action`, replace the form with the real receipt: action, signer, timestamp, dispatch status, relevant digests/Merkle proof, and backend execution modes. Do not show a seal before a successful response.

#### Error/empty cases

- Scenarios unavailable: retain shell, show endpoint failure and retry.
- SSE disconnect: preserve stages received, mark stream interrupted, allow safe rerun.
- Approval error: keep entered sign-off locally and show the server error beside authorize.
- No evidence box: show the extracted field text/source reference rather than a blank document simulator.

#### Desktop wireframe

```text
┌ VERITAS—600 ─ Examination | Architecture benchmark ─ theme · API ┐
├ LC-2026-9104  APPLICANT → BENEFICIARY  USD 880,000  [case ▾]       ┤
├─────────────────────┬──────────────────┬───────────────────────────┤
│ EVIDENCE FOLIO      │ DECISION SPINE   │ DECISION DOCKET           │
│ Insurance cert. 1/1 │ 1 Amendment  ✓   │ ISSUE MT734 REFUSAL       │
│                     │ 2 Federation ✓   │ Human authorization req.  │
│ [cover: 108%] ◀─────┼─3 Rules       ✓──┼ $9,600 insurance shortfall│
│ amount / weight     │ 4 Legal       ✓  │ UCP 600 Art. 28(f)(ii)    │
│ source · digest     │ 5 Decision    ✓  │ [Review evidence]         │
│                     │ stage details ▾  │ [Issue MT734 refusal]      │
├─────────────────────┴──────────────────┴───────────────────────────┤
│ RULE MATRIX · deterministic first · semantic · advisory            │
└────────────────────────────────────────────────────────────────────┘
```

#### Mobile wireframe

```text
┌ VERITAS—600       theme ┐
│ LC-2026-9104       [▾]  │
│ ISSUE MT734 REFUSAL     │
├ Evidence | Stages | Docket ┤
│ 3 / 5 Rules complete    │
│ ■ Insurance DISCREPANT  │
│ Required 110%           │
│ Observed 108%           │
│ UCP 600 Art. 28(f)(ii)  │
│ [Inspect source]        │
└─────────────────────────┘
```

The segmented control changes visible regions but keeps all content in the DOM only when doing so does not cause excessive hidden rendering; focus moves to the region heading after user activation.

### 15.3 `/evals` — Architecture benchmark

#### Goal

Demonstrate why the hybrid system is safer than neural-only and rule-only baselines without turning the page into a marketing chart.

#### Structure

1. **Benchmark brief:** dataset size, scenario mix, last observed source/mode, and `Run benchmark` action.
2. **Architecture comparison ledger:** three columns—Neural-only, Rules-only, VERITAS hybrid—and rows for legal accuracy, deterministic override safety, semantic coverage, evidence provenance, and human gating.
3. **Scenario matrix:** one row per evaluation with expected outcome, each architecture outcome, pass/fail, and expandable evidence.
4. **Why outcomes diverge:** concrete examples tied to real cases; no invented model thought process.
5. **Runtime/provenance footer:** whether results came from the API or bundled demo data, timestamp, and sponsor telemetry.

Use bars only for comparable bounded metrics. Show exact numerator/denominator beside any percentage. Never use a decorative radar chart. If `GET /api/v1/evals/results` fails and the current bundled fallback is used, place `BUNDLED DEMO DATA — API unavailable` at the top of the results and disable language implying a fresh run.

#### Benchmark run behavior

- `POST /api/v1/evals/run` enters a pending state with a stable table skeleton.
- Results replace row values without reordering the architectures.
- Focus moves to the results heading and an `aria-live="polite"` summary announces completion.
- Error leaves prior results visible with their original provenance and timestamp.

#### Responsive behavior

At 1024 px+, preserve comparison columns. At smaller widths, each metric becomes a row with three labeled values; never require horizontal page scrolling. Scenario details become disclosure panels. Sticky first columns are allowed only when scroll affordance is obvious and keyboard operation remains intact.

### 15.4 Proof drawers and dialogs

These are overlays within existing routes, not new routes:

- **Federated evidence:** real SQL/query receipt, sources queried, row cardinality, execution mode, and duration if present. Avoid duplicating a static SQL string that can drift from the backend.
- **Amendment context:** ordered amendments, acceptance state, active terms, source, and Art. 10 explanation.
- **Model/extraction evidence:** model/mode, cache state, structured result, source boxes/digests where returned; do not expose chain-of-thought.
- **Cryptographic proof:** canonical decision digest, Merkle root/proof data, and dispatch receipt.

Use the WAI-ARIA modal dialog pattern: programmatic name, contained tab sequence, Escape close unless an irreversible submission is in flight, and focus return to the invoker. A non-modal persistent inspector may be used on wide screens, but its semantics must change accordingly.

### 15.5 Judge handoff inside the terminal

The landing page carries the full product orientation. When `?tour=1` is present on `/examine`, a compact, dismissible handoff banner can orient hackathon judges in under 10 seconds:

> Evidence in. Rules lock. AI interprets. Humans authorize.

The banner confirms that the user has entered the real examination terminal and names the selected case. `Run examination` focuses the primary action. Store only banner dismissal locally; returning examiners skip it. The masthead `How VERITAS decides` link returns to the relevant landing-page section.

---

# LANDING PAGE — CREATIVE DIRECTION & IMPLEMENTATION BLUEPRINT

This chapter is a **design and engineering recommendation**, not implemented behavior. It adds one route to the redesign: `/` becomes the public product story, the complete existing examination workflow moves to `/examine`, and `/evals` remains unchanged. The landing page uses the same Evidence Ledger identity and never claims authentication, production deployments, customers, or live sponsor execution that the repository cannot prove.

## LP-1. Landing-Page Objectives and Target Audience

### Objectives

Within five seconds, the page must communicate:

1. VERITAS-600 examines documentary credits and recommends a bank action.
2. Objective failures are calculated and locked; semantic AI cannot waive them.
3. Evidence and external risk signals remain inspectable from source to receipt.
4. A human examiner must authorize every consequential action.

Within 90 seconds, a hackathon judge should be able to explain the five-stage architecture, the value of the hard invariant, all three possible outcomes, and the role of Zetaris, Meterless, NVIDIA NIM, and deterministic Python. A trade-finance user should be able to bypass the story immediately and enter the terminal.

### Audiences and desired next action

| Audience | Arrives asking | Must see first | Desired action |
|---|---|---|---|
| Hackathon judge | “What is novel, real, and technically defensible?” | Hard invariant and evidence-to-action preview | Trace the demo, then open the same case in the terminal |
| Documentary-credit examiner | “Will this help without taking authority away?” | Source evidence, exact rule, human gate | Open examination directly |
| Compliance/risk reviewer | “Does it separate documentary compliance from AML risk?” | Parallel compliance/risk outcomes and provenance | Inspect the three outcomes and federation proof |
| Technical evaluator | “Are the integrations substantive and observable?” | Five owners/stages and honest runtime modes | Open architecture benchmark or terminal proof drawer |
| Sponsor reviewer | “Where does our technology materially contribute?” | Stage-level responsibility, not a logo wall | Inspect the architecture sequence |

### Measurable landing outcomes

- At least 90% of test participants can state “AI cannot override a failed deterministic check” after the hero and invariant section.
- Median time to identify the product domain and primary benefit is below five seconds.
- The first meaningful CTA is keyboard reachable in three `Tab` presses or fewer after the skip link.
- At least 80% of first-time participants can correctly identify which preview is predefined and which route runs the real examination.
- No participant mistakes `CACHED_REPLAY`, `STRUCTURED_FIXTURE`, or `LOCAL_DUCKDB_FALLBACK` for live cloud execution.
- Mobile users reach the examination route without traversing the full narrative.

## LP-2. Research Findings and References

All references in this subsection were accessed **23 October 2026**. They are principle sources, not visual templates.

| Reference | Verified observation | Principle adopted | What VERITAS must not copy |
|---|---|---|---|
| [Awwwards Sites of the Day](https://www.awwwards.com/websites/sites_of_the_day/) and [Cyera AI Guardian design profile](https://www.designrush.com/best-designs/websites/cyera-ai-guardian-website-design) | Award ecosystems value art direction, interaction, content, and usability; the Cyera profile makes an abstract security role tangible through interaction | Give VERITAS one recognizable metaphor and one functional signature interaction | Portfolio navigation, long preloaders, cursor gimmicks, or effects that outrank evidence |
| [Stripe: Connect front-end experience](https://stripe.com/blog/connect-front-end-experience) | Stripe explicitly describes using a unique landing-page story to express complex capability while keeping the surface light and simple | Stage complexity progressively and make the real product UI the visual evidence | Stripe gradients, diagonal brand geometry, or decorative financial illustrations |
| [Stripe Checkout](https://stripe.com/payments/checkout) | A clear promise is paired with an operable product demonstration | Let a visitor manipulate one bounded, real scenario rather than watch a fake video | Unverifiable conversion statistics or customer logos |
| [Linear: A calmer interface for a product in motion](https://linear.app/now/behind-the-latest-design-refresh) | The 2026 refresh prioritizes task content, predictable structure, quieter supporting chrome, and fewer unnecessary icons | Let the decisive evidence carry contrast; recede navigation and supporting marks | Linear’s dark gradient/blur brand language or issue-tracker composition |
| [Linear: Change for the better](https://linear.app/change) | A 2026 editorial product narrative develops one problem coherently instead of repeating feature cards | Write the page as a continuous argument: risk → invariant → proof → action | Long poetic copy that delays the product explanation |
| [Vercel Design Engineer Principles](https://vercel.com/design/engineer) and [Design Engineering at Vercel](https://vercel.com/blog/design-engineering-at-vercel) | Usefulness, constraints, edge states, performance, cross-browser input, preferences, and accessibility are treated as design craft | Make production quality part of the creative standard, not a cleanup phase | Black-and-white developer branding, dot grids, or code-window decoration |
| [Apple MacBook Air product page](https://www.apple.com/macbook-air/) | Product communication uses large type, controlled pacing, progressive detail, and hardware-in-use imagery | Use one idea per viewport and let scale/pacing clarify the chain of custody | Scroll-jacking, cinematic media weight, or product spins unrelated to VERITAS |
| [Microsoft Human-AI Guidelines](https://www.microsoft.com/en-us/haxtoolkit/ai-guidelines/) | AI systems should set expectations, explain relevant behavior, and support correction/control | Clearly label predefined demonstrations and keep final authority human | Anthropomorphic agent copy or concealed uncertainty |
| [WCAG 2.2](https://www.w3.org/TR/WCAG22/) and [Web Vitals](https://web.dev/articles/vitals) | Accessibility and performance have measurable success criteria | Set AA, reduced-motion, LCP/INP/CLS, reflow, and input requirements before animation | “Award quality” as permission to degrade basic access |

### Research synthesis

The strongest reference pattern is not a particular aesthetic. It is the alignment of claim, demonstration, and interaction: one crisp promise, a product-specific visual that proves it, progressive technical detail, and a low-friction next action. VERITAS should combine editorial pacing with an operable evidence chain. It should reject award-site conventions—ambient WebGL, custom cursors, forced horizontal scroll, audio, and blocking introductions—that weaken bank-grade trust.

## LP-3. Three Alternative Creative Concepts

### Concept A — The Living Evidence Ledger

- **Metaphor:** a documentary-credit control sheet comes alive as evidence passes through authoritative checkpoints.
- **Composition:** warm paper field, asymmetrical folios, vertical registry rule, decisive copper docket.
- **Narrative:** raw packet → active terms → cross-silo context → locked rules → bounded interpretation → human action.
- **Signature:** selecting any conclusion traces a single continuous rule back to its source field.
- **Strength:** most faithful to the selected application identity and naturally light-first.
- **Risk:** can feel archival unless typography scale and spatial motion are contemporary.

### Concept B — Documentary X-Ray

- **Metaphor:** a stack of trade documents is inspected layer by layer; each layer reveals structured fields, legal constraints, and external risk.
- **Composition:** large central document silhouette with translucent but non-glass overlays, marginal annotations, and an x-ray scan line controlled by scroll.
- **Narrative:** what a human sees → what deterministic checks measure → what semantic review interprets → what federation reveals.
- **Signature:** drag a vertical divider between “document packet” and “decision evidence.”
- **Strength:** immediately explains extraction and hidden risk.
- **Risk:** source document images are not currently available for a truthful polished canvas; simulated imagery could be mistaken for live OCR.

### Concept C — The Decision Assembly

- **Metaphor:** evidence is mechanically aligned into a final action docket, like precision typesetting or a secure print register.
- **Composition:** modular strips, typographic plates, hash marks, and a central assembly rail.
- **Narrative:** independent authorities contribute pieces; only policy assembly and human sign-off produce an action.
- **Signature:** stages lock into place, while an invalid neural “compliant” plate visibly cannot fit over a deterministic discrepancy.
- **Strength:** expressive, technical, and memorable; visually demonstrates the hard invariant.
- **Risk:** mechanical animation can become theatrical and requires more bespoke choreography.

### Concept comparison

| Criterion | Weight | Living Evidence Ledger | Documentary X-Ray | Decision Assembly |
|---|---:|---:|---:|---:|
| Product truth | 25% | 5.0 | 4.0 | 4.6 |
| Five-second clarity | 20% | 4.8 | 4.7 | 4.1 |
| Continuity with application | 15% | 5.0 | 3.8 | 4.3 |
| Distinctiveness | 15% | 4.6 | 4.5 | 4.9 |
| Accessibility | 10% | 4.8 | 3.8 | 4.0 |
| Performance feasibility | 10% | 4.9 | 3.7 | 4.0 |
| Light/dark parity | 5% | 5.0 | 4.2 | 4.5 |
| **Weighted score / 5** | **100%** | **4.87** | **4.15** | **4.44** |

**Selected concept:** The Living Evidence Ledger. Borrow the Assembly’s moment of a failed override being physically blocked, but implement it as semantic HTML/SVG rather than a mechanical scene. Do not use X-Ray transparency without real document imagery.

## LP-4. Three Hero Concepts and Comparison

### Hero A — The Evidence Gate (selected)

**Headline:** “Every document. Every rule. One defensible decision.”

**Support:** “VERITAS-600 turns documentary-credit evidence into a traceable bank action—locking objective UCP 600 checks, constraining semantic AI, and requiring human authorization.”

The visual is a compact three-part evidence gate: an insurance field showing `108%`, the deterministic requirement `≥ 110%`, and an `ISSUE MT734 REFUSAL` docket marked `Human authorization required`. A five-stage rule connects them. Hover/focus/tap exposes authority and citation. It is labeled `Guided preview · predefined LC-2026-9104 evidence`.

### Hero B — The Rule That Cannot Be Overruled

**Headline:** “AI can interpret the documents. It cannot change the math.”

The visual splits the hero between a semantic review that accepts a harmless typo and a deterministic insurance check that fails. Attempting to move the semantic verdict across the boundary is visibly rejected.

**Advantage:** the hard invariant is instantly memorable. **Weakness:** it narrows the first impression to a negative/technical constraint and under-explains federation, action, and human control.

### Hero C — Three Outcomes, One Chain of Custody

**Headline:** “Honour. Refuse. Hold. Every outcome carries its evidence.”

Three action dockets radiate from a central evidence seal; selecting one reveals its seed scenario and decisive proof.

**Advantage:** communicates breadth and all golden cases. **Weakness:** three equal branches increase cognitive load and resemble a feature selector before the visitor understands the product.

### Hero decision matrix

| Criterion | Weight | Evidence Gate | Cannot Be Overruled | Three Outcomes |
|---|---:|---:|---:|---:|
| Domain/value clarity | 25% | 4.9 | 4.5 | 4.1 |
| Architecture clarity | 20% | 4.8 | 4.9 | 4.0 |
| CTA support | 15% | 4.9 | 4.3 | 4.4 |
| Visual originality | 15% | 4.7 | 4.8 | 4.4 |
| Mobile legibility | 10% | 4.7 | 4.4 | 3.8 |
| Honest implementation | 10% | 5.0 | 4.8 | 4.8 |
| Performance | 5% | 4.9 | 4.8 | 4.5 |
| **Weighted score / 5** | **100%** | **4.85** | **4.61** | **4.19** |

## LP-5. Selected Visual Direction and Rationale

The selected landing direction is **Living Evidence Ledger with the Evidence Gate hero**. It converts the product architecture into the page’s form rather than decorating generic marketing sections.

- The warm paper canvas makes a light-first experience feel native, not secondary.
- A continuous evidence rule begins in the hero and reappears through every section, becoming the signed receipt line at the end.
- Headlines use editorial scale; structured evidence stays dense, precise, and mono.
- Copper is reserved for human-controlled actions and the final receipt, so the CTA color itself reinforces governance.
- Deterministic Python, bounded Nemotron, Zetaris federation, Meterless context, and human authority use the same stamps as the terminal.
- Motion shows state and custody: align, reveal, lock, trace, authorize. Nothing “thinks,” floats, pulses, or glows.

The landing page is premium because every compositional decision is tied to domain meaning. It should feel like a contemporary legal-financial instrument opened to the public, not an AI startup skin laid over a dashboard.

## LP-6. Complete Section-by-Section Content Architecture

The page is one coherent argument. Each section inherits the evidence rule from the previous section; none is a reusable “feature grid.”

| # / anchor | Purpose and exact message | Content hierarchy and composition | Interaction, motion, and transition | Mobile and accessibility | Dependencies |
|---|---|---|---|---|---|
| 0. Masthead | Orient and offer immediate application entry | Wordmark; anchors `Why`, `Trace a decision`, `Architecture`, `Proof`; `Benchmark`; theme; copper `Open examination` | Starts transparent over canvas, gains surface/rule after 48 px; active anchor uses a small folio index; CTA arrow moves 2 px on hover | Skip link first; anchors collapse into named modal drawer under 768 px; CTA remains visible; no hover-only state | Server markup, theme control, Radix Dialog only for mobile menu if adopted |
| 1. `#top` Evidence Gate hero | “Every document. Every rule. One defensible decision.” | Eyebrow; 8–11 word headline; 2-line support; primary `Open examination`; secondary `Trace a decision`; guided preview; proof footnote `Predefined case—not a live run` | Headline reveals by line; evidence rule draws; three gate nodes settle; selection links evidence/check/action; next section continues the same rule | Natural block order; visual becomes vertical; all preview nodes are buttons with visible labels; reduced motion starts complete | CSS, inline SVG, Motion for small entrance/selection |
| 2. `#why` Failure triad | Explain why naïve systems fail | Three consecutive editorial statements, not cards: strict matching wrongfully refuses; unconstrained LLMs can waive facts; document-only review misses external risk | As each statement enters, one margin annotation changes from `TEXT ONLY` → `MODEL ONLY` → `SILOED`; no pinned scroll on mobile | Ordered list with complete text; icons redundant; no alarming looping animation | CSS and IntersectionObserver/Motion viewport events |
| 3. `#invariant` Hard invariant | State the differentiator: “Interpretation may add context. It cannot erase a failed calculation.” | Full-width 108% vs 110% calculation; exact UCP 600 Art. 28(f)(ii); neural observation above a locked deterministic verdict | User toggles `Show attempted override`; semantic `COMPLIANT` label approaches the boundary, stops, and resolves to `BLOCKED BY DETERMINISTIC CHECK`; one-time 320 ms | Toggle is a button with expanded text result; reduced motion swaps instantly; calculation is real text, not canvas | Shared `StatusMark`, `AuthorityStamp`, `LegalCitation`; Motion optional |
| 4. `#trace` Guided decision | Let visitors operate one representative story | Predefined LC-2026-9104; five selectable stages; evidence folio; stage explanation; final refusal docket; CTA `Open this case in the terminal` | Click/keyboard steps or `Next evidence`; source-to-action line updates; no autoplay after initial static state; transition turns preview docket into architecture spine | On mobile, stepper becomes ordered accordion; all content remains reachable without drag; `aria-current=step`; live region announces stage selection only | Static typed story data cross-checked against fixture; SVG connector; no SSE |
| 5. `#architecture` Five accountable owners | Show how hybrid reasoning works | Five oversized numbered rows: Meterless/memory, Zetaris, Python, Nemotron, policy/human gate; input/output/mode for each | Desktop uses sticky left thesis while rows pass; active row extends the evidence rule; no scroll hijack or mandatory pin | Natural document flow under 1024 px; owner/output text always visible; reduced motion removes rule travel | CSS sticky, Motion viewport detection; no GSAP required |
| 6. `#outcomes` Three bank actions | Show breadth without presenting an autonomous action engine | Three stacked dockets: Honour (8841), Refuse (9104), AML Hold (9920); each names decisive reason and `Human sign-off required` | Selecting a docket expands evidence summary and collapses the prior one; action color appears only inside selected human-gate line | Native disclosure pattern; first remains expanded; no carousel; status not color-only | Shared docket/disclosure primitives; seeded presentation copy |
| 7. `#proof` Trust is observable | Explain provenance, fallback honesty, and receipt | Chain-of-custody line: source digest → active-terms hash → federation receipt → decision hash → Merkle root → examiner receipt; exact telemetry pairs | Focus/hover traces upstream/downstream relationships; sample hash is explicitly labeled `Example from predefined demo`; rule becomes circular receipt seal | Text list is primary; SVG is decorative enhancement; full hashes copyable; no tooltip-only meaning | Inline SVG, copy control; no external graph library |
| 8. `#benchmark` Evidence of value | Show why hybrid outperforms two baselines using verified local evaluation results | Compact three-row comparison: strict rules, single-prompt model, hybrid; exact metric names and denominator; link to full benchmark | Rows reveal together; hybrid is not animated to “win”; `View architecture benchmark` goes to `/evals` | Semantic table becomes definition rows; source/provenance label remains adjacent | Server/static summary synchronized with eval fixture or read-only results; no chart library |
| 9. `#enter` Final invitation | Convert understanding into action | “Inspect the evidence. Then make the call.”; primary `Open examination`; secondary `View benchmark`; small statement of human authority; product footer | Evidence rule closes into a static receipt seal; CTA gets focusable underline/arrow feedback; no confetti | Compact vertical CTA; seal hidden if it crowds text; legal/product links only if real | CSS/SVG only |

### Narrative transitions

- Hero to problem: the hero’s evidence line exits the result docket and becomes a redaction-like margin rule beside the three failure modes.
- Problem to invariant: three failure annotations align into the deterministic boundary.
- Invariant to demo: the `108%` failing field becomes the selected field in the guided case.
- Demo to architecture: the five demo tabs expand vertically into five accountable owners.
- Architecture to outcomes: five inputs converge into three allowed recommendations, never directly into dispatch.
- Outcomes to proof: the selected outcome remains `PENDING_HUMAN_SIGN_OFF`; proof appears only after the explanatory human gate.
- Proof to CTA: the lineage rule resolves into the receipt-seal mark used across the app.

## LP-7. Desktop and Mobile Wireframe Specifications

### Desktop, 1440 px reference

```text
┌ VERITAS—600      Why  Trace  Architecture  Proof   Benchmark   ◐ [Open examination] ┐
│                                                                                     │
│  DOCUMENTARY CREDIT EXAMINATION                                                     │
│  Every document. Every rule.          ┌ EVIDENCE GATE · PREDEFINED DEMO ─────────┐  │
│  One defensible decision.             │ Insurance certificate  108%             │  │
│                                       │             │ PYTHON requires ≥110%      │  │
│  Traceable UCP 600 decisions with     │             ▼                            │  │
│  locked calculations and human        │ ISSUE MT734 REFUSAL                      │  │
│  authorization.                       │ Human authorization required             │  │
│  [Open examination] [Trace decision]  └──────────────────────────────────────────┘  │
│                                     predefined LC-2026-9104 · not a live run         │
├────────────────────────────────── continuous evidence rule ─────────────────────────┤
│  WHY EXISTING APPROACHES FAIL        oversized editorial statements                 │
├──────────────────────────────────────────────────────────────────────────────────────┤
│  INTERPRETATION CANNOT CHANGE MATH   108%  ┃  REQUIRED 110%  [Show attempted override]│
├──────────────────────────────────────────────────────────────────────────────────────┤
│  TRACE ONE DECISION                  folio  │ five stages │ refusal docket             │
├──────────────────────────────────────────────────────────────────────────────────────┤
│  FIVE ACCOUNTABLE OWNERS             sticky thesis │ 01 … 05                         │
├──────────────────────────────────────────────────────────────────────────────────────┤
│  HONOUR / REFUSE / HOLD              stacked action dockets                         │
├──────────────────────────────────────────────────────────────────────────────────────┤
│  EVIDENCE → HASH → RECEIPT           lineage proof                                  │
├──────────────────────────────────────────────────────────────────────────────────────┤
│  HYBRID BENCHMARK                    semantic comparison table                       │
├──────────────────────────────────────────────────────────────────────────────────────┤
│  Inspect the evidence. Then make the call.                 [Open examination]         │
└──────────────────────────────────────────────────────────────────────────────────────┘
```

Desktop content width caps at 1728 px. Hero minimum height is `min(860px, calc(100svh - header))`, but content always determines final height. Copy occupies five grid columns and the gate occupies seven. No section is forced to exactly 100vh after the hero.

### Mobile, 390 px reference

```text
┌ VERITAS—600              [Open] [Menu] ┐
│ DOCUMENTARY CREDIT EXAMINATION         │
│ Every document.                       │
│ Every rule.                           │
│ One defensible decision.              │
│                                       │
│ [Open examination]                    │
│ [Trace a decision ↓]                  │
├ GUIDED PREVIEW · PREDEFINED CASE ─────┤
│ Insurance cover                       │
│ Observed 108%                         │
│ ────────────────                      │
│ Required ≥110%                        │
│ UCP 600 Art. 28(f)(ii)                │
│ ■ ISSUE MT734 REFUSAL                 │
│ Human authorization required          │
├ WHY ──────────────────────────────────┤
│ 01 Strict text can wrongfully refuse  │
│ 02 AI cannot waive objective facts    │
│ 03 Siloed review can miss external risk│
└ natural document flow continues ──────┘
```

At mobile sizes, text precedes the interactive visual in DOM and layout. The preview is not a horizontally scrolling mini-dashboard. Each section uses 24 px horizontal padding, 64–88 px vertical separation, and normal browser scrolling. A persistent bottom CTA is not used because it would obscure evidence; the compact header CTA remains available.

## LP-8. Hero Composition and Interactive Behavior

### Exact hierarchy

1. Eyebrow: `DOCUMENTARY CREDIT EXAMINATION · UCP 600`.
2. `h1`: `Every document. Every rule. One defensible decision.`
3. Support sentence from Hero A, limited to 62 characters per line on desktop.
4. Primary CTA: `Open examination` → `/examine?case=LC-2026-9104`.
5. Secondary action: `Trace a decision` → `#trace`, using native smooth scroll only when motion preference allows.
6. Proof line: `Deterministic checks locked · Semantic review bounded · Human sign-off required`.
7. Guided Evidence Gate with a persistent `Predefined demonstration` label.

### Evidence Gate interaction

- Default selection is `Insurance certificate · Coverage 108%`.
- Three focusable nodes—source, rule, recommendation—form a logical DOM sequence.
- Activating a node updates a 1–2 sentence explanation and visibly highlights the other two related nodes.
- The rule node shows operands: LC amount/base if included in the verified fixture, required coverage, observed coverage, and `$9,600` shortfall.
- The semantic owner remains present as `No semantic finding can alter this failed calculation`; it is not staged as an LLM making a fresh request.
- The final docket remains `PENDING HUMAN SIGN-OFF`; no CTA inside the landing preview can authorize it.
- `Open this case` navigates to `/examine?case=LC-2026-9104&tour=1`; it does not start an examination in the background.

### Initial entrance

- Server-render all copy and the complete static gate so first paint conveys the message without JavaScript.
- At hydration, if motion is allowed: eyebrow opacity 0→1 over 180 ms; headline lines rise at most 8 px over 360 ms with 55 ms stagger; support/CTAs fade over 220 ms; gate rule draws over 420 ms; three nodes settle sequentially at 70 ms intervals.
- Total authored entrance completes within 900 ms and never blocks input.
- Do not animate the LCP text from invisible for more than one frame; the no-JS/server state is fully visible.
- Reduced motion and repeat visits show the final composition immediately.

## LP-9. Guided Product Demonstration Concept

### Chosen model: one evidence chain, not a miniature application

The landing demo uses **predefined LC-2026-9104 evidence** to explain the architecture without reproducing the three-pane terminal. It is an educational walkthrough, not an examination request and not a video.

| Step | Visible fact | Owner/output | Visitor learns |
|---|---|---|---|
| 1. Active terms | Required insurance terms after amendment context | `METERLESS / MEMORY` | The system first determines which terms actually govern |
| 2. Federated context | Customs/watchlist context and source receipt summary | `ZETARIS` | External evidence can be queried without pretending it came from the document |
| 3. Locked calculation | Required 110%, observed 108%, `$9,600` shortfall | `PYTHON · DISCREPANT` | Objective failure is calculated and immutable |
| 4. Bounded interpretation | Semantic checks remain separate; no override | `NEMOTRON · BOUNDED` with actual replay/live terminology only in the terminal | AI handles language, not arithmetic authority |
| 5. Recommendation | `ISSUE_MT734_REFUSAL` and `Human authorization required` | `POLICY ENGINE → HUMAN` | Recommendation is not dispatch |

### Data and truth contract

- Put demo content in a typed `landing-story.ts` presentation fixture whose values are copied from and tested against the golden scenario/evaluation expectations.
- Label it on every viewport: `Guided demonstration · predefined LC-2026-9104 evidence · not a live run`.
- Never display `LIVE_ZETARIS`, `LIVE_UNCACHED`, or a current timestamp inside the predefined walkthrough.
- A network-free demo is intentional for instant rendering and reliable judging. The real terminal owns SSE, actual execution modes, errors, and human authorization.
- If product values change, a contract test must fail until the story is updated.
- Do not expose chain-of-thought. Step summaries describe observable input, authority, output, and invariant.

### Interaction model

- Desktop: a five-item vertical index and one stable evidence canvas; click/focus a stage to update the canvas.
- Keyboard: `Tab` enters the stage list; arrow keys move among tabs if implemented as ARIA tabs; `Home`/`End` jump; content panel is programmatically associated.
- Mobile: ordered accordion, first stage open; `Next evidence` is optional redundancy, not the only navigation.
- Deep link: `/#trace?` is not valid; use `/#trace` and preserve standard fragment behavior.
- Completion: after stage 5, focus does not move automatically. The nearby CTA reads `Open this case in the terminal`.

## LP-10. Detailed Scroll and Motion Choreography

### Global rules

- Use native document scrolling. No scroll hijacking, inertial scroll library, snap points, or blocking intro.
- Animate only transform and opacity for entrances; SVG stroke changes are allowed for the evidence line. Avoid layout-affecting top/left/height animation.
- Intersection-triggered sequences play once per visit. Interactive state changes remain replayable.
- Desktop sticky storytelling is limited to the architecture section and releases before the next section. At viewport height below 700 px or width below 1024 px, disable sticky behavior.
- Motion tokens inherit Section 17. Landing-specific maximums: 420 ms for entrance, 320 ms for state transition, 55 ms text stagger, 20 px maximum parallax differential.

### Section choreography

| Section | Entrance / scroll behavior | Interaction feedback | Reduced-motion/mobile behavior |
|---|---|---|---|
| Masthead | Surface and bottom rule appear after 48 px using 160 ms transition | Anchor underline travels no more than text width; CTA arrow 2 px | Immediate state change; no translucent backdrop in forced colors |
| Hero | Sequence defined in LP-8; evidence line ends at next-section boundary | Related gate nodes tint and connect over 180 ms | Fully composed first frame; vertical static connector |
| Failure triad | Each statement fades/rises 8 px as it crosses 75% viewport; annotation swaps once | Focus reveals one sentence of remediation | All statements visible; annotations static |
| Invariant | Calculation operands align; boundary rule thickens; optional attempted-override movement stops at rule | Button toggles complete explanatory state | Instant before/after swap; no collision animation |
| Guided demo | Evidence connector morphs between fixed SVG paths; panel content crossfades 160 ms | Selected stage rule and authority stamp update | Accordion opens without transform; connector omitted |
| Architecture | Active stage changes as rows cross a center observer; left thesis stays sticky | Hover/focus traces input→output for that row | Natural flow; no observer-driven active state required |
| Outcomes | Docket expands 180 ms; its human-gate rule enters last | Selected docket gains 2 px copper rule | Native disclosure with instant or 50 ms transition |
| Proof | Line draws source→receipt once over 420 ms; seal does not animate because no real approval occurred | Focus shows upstream/downstream labels | Ordered text list; SVG decorative/hidden |
| Benchmark | Rows reveal simultaneously; values never count up | Row focus exposes metric definition/source | Static semantic rows |
| Final CTA | Receipt outline settles as section enters; no loop | Underline/arrow and focus ring only | Static mark and controls |

### Optional parallax decision

A maximum 20 px differential may be used on two decorative folio edges in the hero at desktop widths above 1280 px. It must be pointer-independent, disabled for reduced motion/coarse pointers/low-power mode where detectable, and removed if it creates compositing or text rasterization issues. No content-bearing layer moves at a different rate from the page.

## LP-11. Typography, Color, Spacing, and Visual Assets

The landing page uses Section 14’s tokens rather than creating a marketing-only brand. Scale and whitespace change; semantics do not.

### Landing type system

| Role | Desktop | Mobile | Family / behavior |
|---|---|---|---|
| Hero display | `clamp(3.75rem, 7.2vw, 7.5rem) / .94` | `clamp(2.75rem, 13vw, 4.25rem) / .96` | Newsreader 540–600; max 11 words; balanced wrapping with authored fallback |
| Section thesis | `clamp(2.5rem, 4.8vw, 5.25rem) / .98` | `2.25rem / 1.02` | Newsreader 520; 2–4 lines maximum |
| Section heading | `clamp(1.75rem, 2.5vw, 2.75rem) / 1.08` | `1.75rem / 1.08` | Newsreader 560 |
| Lead | `clamp(1.125rem, 1.4vw, 1.375rem) / 1.5` | `1.0625rem / 1.5` | Inter 400; max 62 characters per line |
| Body | `1rem / 1.6` | `0.9375rem / 1.6` | Inter 400; max 70 characters per line |
| Evidence | `0.8125–0.9375rem / 1.45` | same | IBM Plex Mono; tabular numerals |
| Eyebrow | `0.6875rem / 1.3`, letter spacing `.12em` | same | IBM Plex Mono 500; short uppercase only |

Do not outline text, mask video through glyphs, or split words into inaccessible spans. Line-level hero reveal uses wrappers around complete text lines with the accessible heading left intact.

### Color use

- `--canvas` fills the page; `--surface` appears only under interactive evidence.
- `--registry` is the main ink/structural accent.
- `--copper` is reserved for `Open examination`, human-gate lines, and receipt motifs.
- `--danger` appears only on the actual discrepancy and refusal state, never as a general dramatic background.
- `--neural` marks bounded semantic interpretation; it never dominates the deterministic rule.
- Sponsor brands do not introduce their marketing colors into the narrative.

### Spacing and composition

- Global max width: 1728 px; text/story column max 720 px.
- Page gutters: 24 px at 320–639, 32 px at 640–1023, 48 px at 1024–1439, 64 px at 1440+.
- Hero top/bottom: 96/80 px mobile, 128/112 px desktop after masthead.
- Narrative section block padding: 88 px mobile, 144 px desktop; invariant and guided demo may use 176 px desktop.
- Use intentional negative space around one thesis. Do not place more than two independent focal elements in a viewport.
- Fine rules establish rhythm at 1 px; a 2 px rule means selection, decisive evidence, or human control.

### Visual asset inventory

| Asset | Format | Production rule |
|---|---|---|
| VERITAS monogram | inline SVG | `currentColor`, single-color, recognizable at 16 px |
| Continuous evidence rule | inline SVG/CSS border | Decorative paths `aria-hidden`; never sole relationship representation |
| Folio edges and register ticks | CSS / small SVG | No raster paper scans; opacity ≤ 4% |
| Authority/status marks | shared Lucide + CSS shapes | Same components as terminal |
| Receipt outline | inline SVG | Static on landing because no real approval occurs |
| Product UI preview | semantic HTML/CSS | Not a screenshot; accessible and responsive |
| Open Graph image | generated at build with Next image route or committed optimized asset | Static composition; no sensitive data; include headline and Evidence Gate |

No stock photo, generated banker portrait, globe, cargo ship hero, 3D coin, floating sphere, neural mesh, or looping background video is needed.

## LP-12. Light and Dark Theme Specifications

### Light, primary

- Canvas `#F3F0E7` reads as mineral paper without sepia nostalgia.
- Hero type uses `--ink`; selected evidence uses `--registry`; the human CTA uses `--copper` with verified foreground contrast.
- Surfaces remain mostly flat. The guided demo uses one white/elevated folio and ruled internal divisions.
- The continuous evidence line is `--rule-strong` at rest and assumes semantic color only in the selected segment.
- Paper grain is optional, local, and below 2% opacity; remove it on lower-density displays if it causes banding.

### Dark, equivalent—not inverted

- Canvas `#0D1413`, surface `#131C1A`, raised folio `#192421`.
- Large text uses `#F2F0E8`; muted text `#AEB8B2`; rules become `#34413D`/`#61706B`.
- Copper brightens to `#DF8B64`; deterministic success/danger/neural use their Section 14 dark mappings.
- Grain is disabled; subtle 1 px rules provide texture.
- Avoid luminous gradients, bloom, and white-on-black cinematic overexposure.

### Theme behavior

- Server default is light. `system` and explicit dark follow the same `data-theme` architecture as the terminal.
- The theme toggle preserves position and does not replay section entrances.
- Theme transition is 120 ms on color/border only; initial hydration and reduced motion have no transition.
- Every landing section and all Evidence Gate states require light/dark visual snapshots. Contrast is measured in rendered context, not inferred from token values.

## LP-13. Navigation and CTA Strategy

### Desktop navigation

Left: mark + `VERITAS—600`. Center: `Why`, `Trace a decision`, `Architecture`, `Proof`. Right: `Benchmark`, theme control, `Open examination`.

- Section links use fragments and native browser history; route links use Next `Link`.
- The active section indicator is optional progressive enhancement from `IntersectionObserver`; it never changes the URL on scroll.
- Header height: 64 px desktop, 56 px mobile. Sticky from the start; avoid a hide-on-scroll pattern that makes re-entry unpredictable.
- `Benchmark` goes to `/evals`. The product mark on other routes goes to `/`.

### Mobile navigation

Keep wordmark, compact `Open` CTA, and a labeled `Menu` button. The menu opens an accessible modal sheet listing anchors first and application routes second. Selecting an anchor closes the sheet, navigates, and focuses the section heading without an unexpected animation. Avoid a full-screen experimental menu.

### CTA hierarchy and copy

| Level | Copy | Destination | Use |
|---|---|---|---|
| Primary | `Open examination` | `/examine` or case-specific query | Hero, masthead, final invitation |
| Contextual | `Open this case in the terminal` | `/examine?case=LC-2026-9104&tour=1` | Guided demo completion |
| Secondary | `Trace a decision` | `#trace` | Hero only |
| Secondary route | `View architecture benchmark` | `/evals` | Benchmark and final section |
| Text link | `How VERITAS decides` | `/#architecture` | Terminal masthead/help |

Never use `Get started`, `Try AI`, `Start for free`, `Book a demo`, or `Sign in`; those flows do not exist. Do not claim the predefined preview is “live.”

### Micro-interactions

- Primary CTA fills copper at rest; on hover, the internal arrow translates 2 px and the border darkens. On press, translate 0–1 px; never scale the whole button below 0.98.
- Text links use an underline that grows from the reading direction; forced-colors uses native underline.
- Focus always uses the shared 2 px focus ring and offset.
- Scroll-progress decoration is a 2 px evidence line beneath the masthead only if it passes performance and does not compete with browser scrollbars; omit on mobile/reduced motion.

## LP-14. Landing-to-Application Transitions

### Route contract

| Route | Role after redesign | Migration behavior |
|---|---|---|
| `/` | Public landing and product story | Replaces the current root composition only after `/examine` parity is verified |
| `/examine` | Full existing examination workflow, redesigned | Receives the moved root composition and all current state/actions |
| `/examine?case=<lc_id>` | Preselect a real available scenario | Validate against fetched scenario list; unknown values fall back visibly, never crash |
| `/examine?case=LC-2026-9104&tour=1` | Judge/demo handoff | Select case and show compact handoff banner; does not auto-run |
| `/evals` | Architecture benchmark | Remains stable; nav labels update only |

### Visual continuity

- Root layout, wordmark, theme, fonts, tokens, authority stamps, evidence rule, and CTA grammar are shared.
- On CTA activation, navigate immediately. Do not hold the click for an outro.
- If browser View Transitions are later adopted, use progressive enhancement for a ≤220 ms wordmark/header continuity only. Navigation must be correct without it.
- The terminal lands at its case masthead with the requested case selected and `Run examination` focused only when `tour=1`; normal navigation begins at the page heading.
- Theme preference persists; scroll position and landing animation state do not transfer.
- Back returns to the previous landing scroll position through normal browser restoration.

### Authentication and onboarding truth

There is no authentication or onboarding route. The transition is direct. The examiner-name field remains a sign-off attestation inside the terminal, not a login identity. If authenticated access is added later, insert it after the CTA through a separately designed backend-supported flow; do not build a decorative sign-in screen now.

## LP-15. Recommended Animation Libraries and Tools

| Tool | Landing decision | Exact use | Why / constraint |
|---|---|---|---|
| CSS transitions/keyframes | **Use first** | Link/CTA feedback, color, simple line/loader states | Zero runtime; easiest reduced-motion and first-paint behavior |
| Motion for React | **Use selectively** | Hero node entrance, presence/crossfade in guided demo, disclosure/layout continuity, viewport activation | Matches Section 18; one shared motion system; lazy feature bundle |
| Inline SVG | **Use** | Evidence line, connectors, receipt outline | Scalable and semantic-adjacent; text relationships remain in DOM |
| `IntersectionObserver` | **Use natively** | Active narrative section and play-once triggers | No scroll listener loop; progressive enhancement |
| CSS `position: sticky` | **Use conditionally** | Architecture thesis above 1024 px and sufficient height | Native spatial continuity; automatically disabled for constrained viewports |
| GSAP + ScrollTrigger/Flip | **Reject for this plan** | None | Motion/CSS covers the designed sequences; a second animation runtime and licensing/governance review are unjustified |
| Three.js / React Three Fiber / WebGL | **Reject** | None | No 3D concept improves evidence comprehension; high accessibility/GPU/bundle cost |
| Lenis | **Reject** | None | Native scroll preserves keyboard, fragments, restoration, and user settings |
| Rive / Lottie | **Reject** | None | No authored character/illustration sequence; state must remain data/DOM driven |
| View Transitions API | **Optional progressive enhancement** | Short header continuity between `/` and `/examine` | Browser support and focus/history behavior must be tested; no polyfill dependency |

Implementation tooling from Section 19—Playwright, axe-core, Chrome DevTools, and optional visual regression—also covers the landing route. No Sites publication workflow is part of this local planning task.

## LP-16. React Component Architecture

### Proposed tree

```text
app/page.tsx (server: metadata + LandingPage)
└─ LandingPage (server composition)
   ├─ LandingMasthead (server)
   │  ├─ LandingNav (server links)
   │  ├─ MobileNavDialog (client)
   │  └─ ThemeMenu (client, shared)
   ├─ HeroSection (server)
   │  └─ EvidenceGate (client island)
   ├─ FailureSection (server)
   ├─ InvariantSection (server)
   │  └─ InvariantDemonstration (client island)
   ├─ GuidedDecisionSection (server shell)
   │  └─ GuidedDecisionDemo (client island)
   ├─ ArchitectureSection (server shell)
   │  └─ ArchitectureObserver (client enhancement)
   ├─ OutcomesSection (server)
   │  └─ OutcomeDisclosures (client or native details)
   ├─ ProofSection (server)
   ├─ BenchmarkTeaser (server)
   ├─ FinalInvitation (server)
   └─ ProductFooter (server)
```

### Server/client policy

- All meaningful copy, links, labels, tables, and default preview content render on the server.
- Client islands own only selection, disclosures, section observation, theme, mobile menu, and motion.
- A JavaScript failure leaves a complete, navigable story with all facts visible in natural order.
- Do not wrap the landing page in a single client component.
- Lazy-load `GuidedDecisionDemo` enhancement below the fold, but server-render its default semantic content.
- Reuse `AuthorityStamp`, `StatusMark`, `LegalCitation`, CTA, theme, and formatting primitives from the app.

### Proposed landing files

```text
apps/web/src/app/page.tsx
apps/web/src/app/examine/page.tsx
apps/web/src/app/opengraph-image.tsx
apps/web/src/components/landing/LandingMasthead.tsx
apps/web/src/components/landing/HeroSection.tsx
apps/web/src/components/landing/EvidenceGate.tsx
apps/web/src/components/landing/FailureSection.tsx
apps/web/src/components/landing/InvariantDemonstration.tsx
apps/web/src/components/landing/GuidedDecisionDemo.tsx
apps/web/src/components/landing/ArchitectureSection.tsx
apps/web/src/components/landing/OutcomesSection.tsx
apps/web/src/components/landing/ProofSection.tsx
apps/web/src/components/landing/BenchmarkTeaser.tsx
apps/web/src/components/landing/FinalInvitation.tsx
apps/web/src/components/landing/ProductFooter.tsx
apps/web/src/lib/landing-story.ts
apps/web/src/lib/landing-motion.ts
```

Do not create a parallel landing-only token sheet or component library. Landing-specific files consume shared semantic foundations.

## LP-17. Accessibility and Performance Requirements

### Accessibility

- Meet WCAG 2.2 AA and all Section 21 requirements.
- Provide a first-focus skip link to landing main content; a second optional link may jump directly to `Open examination`.
- One `h1`; section headings form a coherent `h2` hierarchy. Decorative folio labels are not headings.
- Fragment targets use `scroll-margin-top` for the sticky header and receive programmatic focus only after user-initiated mobile-menu navigation where needed.
- Evidence Gate and guided demo expose names, selected state, instructions, and relationships in text. SVG lines are redundant.
- Do not auto-advance the demo, move focus on scroll, or announce viewport section changes.
- The attempted-override control announces its resulting locked state in a polite live region.
- Reduced motion removes entrance transforms, path drawing, parallax, sticky activation effects, and smooth scrolling.
- At 400% zoom, narrative content reflows into one column and the header menu remains operable.
- Support keyboard, touch, mouse, screen reader, forced colors, high contrast, and coarse pointer.

### Performance budgets

- LCP target ≤2.5 s, INP ≤200 ms, CLS ≤0.1 at p75 when field measurement exists.
- Landing first-load JS target **≤130 kB gzipped in the Next build report**, with an aspirational target below the current terminal’s 120 kB baseline where shared chunks allow.
- Landing-only client JS target ≤35 kB gzipped; no charting, WebGL, video, or second animation library.
- HTML server response contains hero and default Evidence Gate; the LCP is text, not a delayed client canvas.
- Initial font payload target ≤100 kB: preload only the UI/body font and the one display subset required above fold; mono can load later.
- Inline SVG total target ≤25 kB uncompressed; simplify paths and avoid filters.
- Open Graph imagery does not load in the page.
- Reserve dimensions for the masthead, hero gate, and font fallback; use size-adjusted fallbacks to limit CLS.
- Below-fold client islands hydrate on visibility/idle where compatible with Next architecture; navigation and content never wait for hydration.
- Test four-times CPU slowdown and slow 4G. Remove optional parallax before relaxing budgets.

### SEO and metadata

- Unique title: `VERITAS-600 — Evidence-led UCP 600 examination`.
- Description accurately mentions deterministic checks, bounded semantic review, federated evidence, and human authorization without claiming regulatory certification.
- Canonical `/`, Open Graph image, theme colors, and crawlable headings/body copy.
- `SoftwareApplication` JSON-LD is optional; include only properties provable from the repository. No ratings, customers, pricing, organization claims, or fabricated FAQs.
- Add sitemap/robots only if the deployment model needs them; do not index local/demo URLs blindly.

## LP-18. Functional Integration Constraints

1. **No decision on the landing page.** The predefined demo cannot call approval, create artifacts, or display an authorized receipt.
2. **No frontend adjudication.** Copy may state verified expected results; it may not calculate a new verdict from visitor input.
3. **Hard invariant remains explicit.** A neural state can never visually pass through or replace a deterministic `DISCREPANT` result.
4. **Truthful modes.** The predefined story shows no live/fallback badge. Actual telemetry appears only after a real terminal run.
5. **No hidden SSE.** Landing load and hero interactions do not start examination requests, consume NIM quota, or warm sponsor calls.
6. **Safe case query.** `/examine?case=` accepts only scenario IDs returned by `GET /api/v1/scenarios`; unknown/unavailable cases produce a visible fallback.
7. **No auth fiction.** CTA enters the current public terminal; examiner sign-off is not login.
8. **No sensitive persistence.** Landing stores only theme and optional motion/tour preferences; never scenario payloads or signatory data.
9. **Exact legal reference.** The hero/invariant uses UCP 600 Art. 28(f)(ii) for ≥110% insurance and no paraphrased article number.
10. **Evaluation provenance.** Benchmark teaser is labeled with test-case count/source and links to full results; if values are static, name the baseline snapshot date.
11. **Backend unchanged.** This landing plan requires no new API endpoint or database mutation.
12. **Existing routes remain usable.** Do not switch `/` until `/examine` has complete functional parity and all internal links/tests are updated.

## LP-19. Visual and Interaction Testing Strategy

### Automated coverage

| Test | Required assertions |
|---|---|
| Route/SEO | `/` returns landing; metadata/canonical correct; `/examine` renders terminal; `/evals` unchanged |
| No-JS | Hero, narrative, default demo facts, CTAs, and legal reference remain visible/usable |
| Hero | Correct copy; predefined label visible; source/rule/action selection; CTA query target |
| Invariant | Override attempt ends locked; no control can mark discrepancy compliant |
| Guided demo | All five stages keyboard operable; content matches typed fixture; no examination/approval network request |
| Navigation | Fragments, sticky offset, mobile dialog focus/escape/return, route links, browser back restoration |
| Themes | First paint and all interactive states in light/dark/system without hydration mismatch |
| Motion | Reduced-motion snapshot contains no transform/path-draw/parallax/smooth-scroll behavior |
| Accessibility | axe smoke tests for initial, mobile menu, invariant toggled, demo final step, outcome disclosure |
| Performance | Route JS budget, Lighthouse/DevTools trace, no CLS from fonts/hero, no long animation tasks |

### Visual matrix

- Viewports: 320×568, 390×844, 768×1024, 1024×768, 1440×900, 1920×1080.
- Themes: light and dark; system test at least once.
- States: hero initial, every Evidence Gate selection, mobile menu, override attempted, demo steps 1/3/5, three outcome disclosures, proof focus, final CTA.
- Environment: normal motion, reduced motion, forced colors, 200% zoom, 400% reflow.
- Browsers: current Chromium, Firefox, WebKit/Safari where available; test iOS viewport and Windows keyboard/High Contrast.

### Human review

- Five-second comprehension test with no narration.
- “Explain the invariant” recall after the hero and after the guided demo.
- Ask users whether the demo is live or predefined; any uncertainty is a copy failure.
- Ask an examiner to validate article citation, insurance calculation wording, outcome labels, and authority boundaries.
- Ask a hackathon judge to identify all four sponsor contributions without a sponsor-logo prompt.
- Conduct an anti-generic critique: remove any section that could belong unchanged to an unrelated AI product.
- Review at 60 Hz and low-end emulation for dropped frames, but prioritize task clarity over animation smoothness.

## LP-20. Exact Implementation Sequence and Acceptance Criteria

### Sequence

1. **Route safety:** copy/move the existing root terminal composition to `/examine`; update internal links; add route parity tests; keep `/` terminal until parity passes.
2. **Static landing skeleton:** introduce semantic server-rendered sections at `/`, exact copy, metadata, fragments, and CTAs with no animation or client demo.
3. **Shared visual foundation:** apply the approved fonts/tokens, masthead, theme, focus, responsive gutters, Evidence Ledger rules, and footer.
4. **Hero and invariant:** implement static Evidence Gate and hard-invariant demonstration; verify source text, calculation, legal citation, and predefined label.
5. **Guided demo:** add typed landing story, contract test, stage selection, mobile accordion, and case-specific handoff URL.
6. **Remaining narrative:** implement failure, architecture, outcomes, proof, benchmark, and final invitation sections.
7. **Progressive interaction:** add mobile navigation, disclosures, evidence linking, and optional section observation.
8. **Motion:** add only LP-10 recipes with reduced-motion equivalents; measure before/after bundle and frame behavior.
9. **Quality pass:** execute LP-19 visual/interaction/a11y/performance matrix; domain review; copy/SEO validation.
10. **Cutover:** switch `/` to landing only after `/examine` parity, update README/demo paths and `STATUS.md`, run full backend/frontend/E2E gates, then `graphify update .` because code changed.

### Landing acceptance criteria

- [ ] `/` communicates domain, benefit, hard invariant, and human authority within the hero without scrolling.
- [ ] Three hero actions work: open terminal, trace demo, and reach benchmark through navigation.
- [ ] Every interactive illustration is labeled predefined and makes no live-execution claim.
- [ ] The 108% vs 110% check and `$9,600` shortfall match the verified LC-2026-9104 scenario and cite UCP 600 Art. 28(f)(ii).
- [ ] The attempted neural override cannot visually or programmatically produce compliance.
- [ ] The guided demo exposes all five real stages and never sends an examination or approval request.
- [ ] `/examine` preserves all former `/` functionality, states, API calls, telemetry, and human sign-off.
- [ ] `/evals` remains fully functional and is linked from the landing narrative.
- [ ] Light is the first render; dark/system are complete and share product tokens.
- [ ] The page works without animation and remains meaningful without client JavaScript.
- [ ] Keyboard, screen-reader, reduced-motion, forced-color, zoom/reflow, touch, and error checks pass.
- [ ] LCP/INP/CLS and route bundle meet LP-17 budgets; no WebGL, video, or unnecessary animation dependency ships.
- [ ] No invented customer, certification, deployment, accuracy, live-mode, authentication, or autonomy claim appears.
- [ ] Desktop/mobile screenshots show a coherent narrative—not a hero followed by repetitive cards.
- [ ] A five-second user test and 90-second judge rehearsal meet LP-1 comprehension goals.

---

## 16. Agentic Interaction and Reasoning Visualization

### 16.1 Observable contract, not theatrical autonomy

The UI visualizes facts the system actually returns: stage identity, stage status, structured summaries, source mode, cached/live state, deterministic findings, legal references, recommendation, and approval receipt. It must not render hidden chain-of-thought, invented sub-agent dialogue, fake confidence, or animated “thinking” text.

### 16.2 Five-stage decision spine

| Stage | Owner label | Inputs shown | Output shown | Failure handling |
|---|---|---|---|---|
| 1. Amendment context | `METERLESS / MEMORY` | LC ID, amendment count | accepted/pending state and effective terms | Keep raw LC terms; mark context unavailable |
| 2. Federated evidence | `ZETARIS` | named source silos | one-row LC evidence, customs/watchlist provenance, actual `LIVE_ZETARIS` or `LOCAL_DUCKDB_FALLBACK` | Stop claims about live federation; permit backend-defined continuation only |
| 3. Deterministic rules | `PYTHON` | amounts, dates, percentages, thresholds | immutable compliant/discrepant checks with calculations | A failed check remains locked; surface affected action |
| 4. Semantic/legal review | `NEMOTRON` | scoped evidence and applicable issue | structured semantic findings with exact citations and `LIVE_UNCACHED` or `CACHED_REPLAY` | Preserve deterministic findings; mark semantic result unavailable |
| 5. Decision assembly | `POLICY ENGINE` | all locked checks and risk signals | one of three recommendations plus artifact preview | No final action without valid recommendation and human gate |

The visual connector between stages is directional, but it must not imply all stages are LLM agents. The owner label makes the hybrid architecture explicit.

### 16.3 Evidence lineage interaction

Selecting a decision reason highlights its upstream rule, calculation, and document/source anchor. Selecting a source field highlights downstream checks that consume it. Implement this as explicit IDs in UI normalization (`evidenceId`, `checkId`, `stageId`) derived from response data or stable local mapping—not DOM position.

```text
Source field → deterministic/semantic check → decisive reason → recommended action
     │                    │                       │
   digest              authority             human gate → receipt
```

If a link cannot be proven from current payloads, show adjacent sections without drawing a connector. Do not invent causality. A future backend schema may expose first-class evidence IDs, but this plan does not require changing the API for the initial redesign.

### 16.4 Recommendation state machine

```text
IDLE
  └─ run ─→ STREAMING(stage 1…5)
                ├─ interruption ─→ INTERRUPTED ── retry ─→ STREAMING
                ├─ failure ─────→ FAILED
                └─ recommendation ─→ RECOMMENDED
                                          └─ open gate ─→ AWAITING_SIGNOFF
                                                               ├─ cancel → RECOMMENDED
                                                               ├─ error  → SIGNOFF_ERROR
                                                               └─ success → AUTHORIZED
```

Case changes cancel the current stream and return to the selected case’s `IDLE` or locally cached completed presentation. `AUTHORIZED` can only follow a successful approve-action response. Frontend animation never advances the state machine.

### 16.5 Confidence and uncertainty

- Do not invent numeric confidence scores.
- Deterministic results say `Calculated` and expose operands.
- Semantic findings say `Model-assessed` and expose scope, citation, and execution mode.
- Unavailable evidence says exactly what was unavailable.
- Cached replay is provenance, not a quality downgrade; render it neutrally and visibly.
- A semantic judgement can be “not assessed” without weakening a locked deterministic discrepancy.

### 16.6 Current truth versus future enhancement

| Current verified capability | UI now | Future only if backend supports it |
|---|---|---|
| Structured fixture extraction with boxes/digests | Label `STRUCTURED_FIXTURE`; show returned fields and anchors | Live uploaded-document OCR workflow |
| In-memory run state | Keep state for the active browser session; disclose refresh limitation where relevant | Persistent case history and resumable approvals |
| Free-text examiner sign-off | Validate and label as examiner sign-off | Authenticated identity/RBAC/e-signature |
| Demo countdown | Label illustrative elapsed/deadline context | Banking-calendar-aware Art. 14(b) clock |
| Health/config mode plus per-run mode | Pre-run unknown; per-run observed telemetry | Historical availability/SLA dashboard |
| Three seeded scenarios | Fetch and show the available three | Queue/search/pagination for production cases |

---

## 17. Motion Design Language

Motion communicates state transition, lineage, and spatial continuity. It never implies work that the backend did not perform.

### 17.1 Motion tokens

| Token | Value | Use |
|---|---:|---|
| `instant` | 0 ms | Reduced motion, critical status swap |
| `fast` | 120 ms | Hover/focus/color |
| `base` | 180 ms | Disclosure, selection, small layout shift |
| `slow` | 260 ms | Drawer/panel entrance |
| `seal` | 420 ms | One-time receipt seal stroke |
| `ease-out` | `cubic-bezier(.16,1,.3,1)` | Enter/reveal |
| `ease-in` | `cubic-bezier(.7,0,.84,0)` | Exit |
| `ease-standard` | `cubic-bezier(.2,0,0,1)` | Reposition/state |
| `spring-panel` | stiffness 420, damping 36, mass 0.8 | Docket/panel spatial move only |

Stagger stage-row reveals by no more than 35 ms and only when multiple results arrive in the same event. Do not replay stagger when reopening a completed stage.

### 17.2 Interaction recipes

- **Stage complete:** 120 ms icon crossfade and 180 ms rule extension. Text updates immediately.
- **Evidence focus:** 120 ms background tint plus a non-animated 2 px left rule.
- **Docket arrival:** 260 ms translate of at most 12 px with opacity; no overshoot.
- **Drawer:** transform/opacity for 260 ms; backdrop 180 ms. Maintain focus semantics independent of animation.
- **Receipt seal:** SVG stroke draws once for 420 ms only after server success, then remains static.
- **Theme change:** colors transition up to 120 ms; disable transition on initial hydration and under reduced motion.
- **Numbers:** update as text. Do not count up monetary or legal values.
- **SSE active:** a restrained rotating loader may identify only the active stage; no indefinite full-page pulse.

### 17.3 Reduced motion

Honor `prefers-reduced-motion: reduce` globally and provide an application-level motion preference only if user research supports it. Under reduction:

- durations become 0–50 ms;
- remove transforms, parallax, smooth scrolling, shimmer, loader rotation, and stroke drawing;
- preserve state through static icon/text changes;
- never use motion as the sole indication of progress.

This follows WCAG 2.2 animation guidance and CSS technique C39. Focus movement and announcements still occur.

### 17.4 Prohibited motion

No cursor-follow effects, kinetic typography, document-page flips, auto-scrolling timelines, particle fields, animated gradients, looping seals, shaking error panels, or 3D camera movement. These obscure evidence, add vestibular risk, and offer no product value.

---

## 18. Animation and Visualization Technology Decisions

### Chosen stack

1. **CSS transitions/keyframes** for focus, hover, color, and simple loader states.
2. **Motion for React** (`motion`) for layout continuity, drawers, presence, and reduced-motion-aware variants.
3. **Inline SVG** for the wordmark, lineage connectors, status shapes, and one-time receipt seal.

Motion’s React API, `AnimatePresence`, layout animation, and `useReducedMotion` cover the required interactions while preserving React ownership. Add it only during implementation and lazy-load feature bundles where practical. Pin and review the then-current version rather than assuming this research snapshot forever.

### Evaluated alternatives

| Technology | Decision | Reason |
|---|---|---|
| GSAP 3.15 | Reject for v1 | Excellent timeline control, but the product has no complex choreographed sequence that justifies a second imperative animation model or added governance review |
| Three.js / React Three Fiber | Reject | WebGL adds bundle, GPU, accessibility, and fallback cost without making evidence clearer |
| Lenis | Reject | Native scrolling is preferable for keyboard, reduced motion, and evidence anchoring |
| Lottie | Reject | No exported illustration sequence is required; state should remain code/data-driven |
| Rive | Reject | Runtime and authoring workflow are unnecessary for the restrained product language |
| Canvas | Reject | DOM/SVG offers better text semantics, selection, responsiveness, and testability |

### Acceptance gate

The redesign should still be fully understandable with JavaScript animation disabled. A motion dependency is acceptable only if the production route remains within the performance budget in Section 22 and its license/security review is current at installation time.

---

## 19. Recommended Libraries and MCP Servers

This is an evaluation and adoption plan, not authorization to install anything. Recheck versions, licenses, advisories, bundle size, and React 19/Next 15 compatibility on the implementation date.

### 19.1 Runtime library decision table

| Candidate | Snapshot researched 23 Oct 2026 | Role | Decision | Integration / project-specific use | Cost, license, and risk notes |
|---|---|---|---|---|---|
| Existing React + Next.js | Repo uses React 19 / Next 15 | Rendering, routing, server/client split | **Keep** | Add the landing at `/`, move terminal composition to `/examine`, preserve `/evals`; use App Router metadata and server layout | Already shipped; current `next build` is the compatibility baseline |
| Existing Tailwind CSS | Repo uses Tailwind 3.4 | Utility styling | **Keep, reduce ad hoc use** | Map semantic CSS variables into Tailwind and component classes; do not require a framework migration for the redesign | Already shipped; avoid generated arbitrary-value sprawl |
| Existing Lucide React | Current dependency | Icons | **Keep** | Standardize evidence/status/action icon sizes and accessible names | Open-source; already in bundle; tree-shake imports |
| [Motion for React](https://motion.dev/docs/react) | npm reported 14.5.0 | Presence/layout animation | **Add—essential for specified polish** | Decision docket placement, drawers, one-time receipt seal, reduced-motion variants | MIT in researched release; open-source/no required service. Added JS; use lazy features and bundle check |
| [Radix Dialog](https://www.radix-ui.com/primitives/docs/components/dialog) | `@radix-ui/react-dialog` 1.3.1 | Accessible approval/proof dialogs | **Add selectively** | Replace the hand-built drawer/modal behavior; style from scratch in Evidence Ledger language | MIT in researched release; no service fee. Test focus, portals, and React 19 behavior |
| [next-themes](https://github.com/pacocoursey/next-themes) | npm reported 0.4.6 | Theme persistence and no-flash script | **Add—small utility** | Light default, dark/system preference, hydration-safe root attribute | MIT in researched release; localStorage/privacy impact is minimal but document it |
| React Aria Components | npm reported 1.21.1 | Accessible component primitives | **Do not mix in v1** | Valid alternative to Radix if the team standardizes on it before implementation | Apache-2.0 in researched release. Mixing primitive systems raises interaction/test cost |
| `@visx/xychart` | npm reported 4.0.0 | Charts | **Reject initially** | Evals needs simple bars/tables that semantic HTML/CSS can express | MIT; avoid dependency cost until several real chart types exist |
| GSAP | npm reported 3.15.0 | Complex timelines | **Reject for v1** | No required timeline exceeds Motion/CSS capability | Standard no-charge terms were available; legal review still required for future commercial use |
| Three.js / R3F | Current packages vary | WebGL/3D | **Reject** | No evidence-clarity use case | Bundle/GPU/testing/accessibility cost |
| Lenis | Current package varies | Smooth scrolling | **Reject** | Native anchor/focus scrolling is more reliable | Can interfere with native and assistive navigation |
| Lottie / Rive | Current packages vary | Authored animation | **Reject** | No decorative illustration runtime needed | Asset pipeline and accessibility fallback cost |

Use [Radix accessibility guidance](https://www.radix-ui.com/primitives/docs/overview/accessibility) as a baseline, not as proof that the composed product is automatically accessible. If Radix is not approved, implement the [WAI-ARIA dialog pattern](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/) directly and test it thoroughly.

### 19.2 Development and validation tooling

| Tool | Priority | What it contributes | Integration complexity | Cost / licensing / data handling |
|---|---|---|---|---|
| [Playwright](https://playwright.dev/docs/next/accessibility-testing) + `@axe-core/playwright` | **Essential** | Route, SSE fixture, sign-off, keyboard, theme, and automated accessibility regression tests | Medium: deterministic network fixtures and three case journeys | Open-source packages; runs locally/CI. Automated accessibility is partial, so retain manual testing |
| [Storybook accessibility testing](https://storybook.js.org/docs/writing-tests/accessibility-testing) | Optional phase 2 | Isolated states for RuleRow, StageRow, Docket, dialog, themes | Medium/high because Storybook is not present | Open-source core; additional config and maintenance |
| [Chromatic visual tests](https://www.chromatic.com/docs/visual-tests-addon/) | Optional | Hosted cross-browser visual diffs for components/pages | Medium; requires external service and uploads rendered snapshots | Paid tiers/third-party data handling may apply; obtain approval before use |
| Lighthouse / Chrome DevTools | **Essential** | Core Web Vitals lab checks, accessibility and bundle observations | Low | Browser tooling; lab measurements are not field data |
| `next build` bundle output | **Essential** | Route JS and build regression | Low | Existing workflow |
| Existing pytest suite | **Essential** | Confirms the UI effort has not destabilized backend contracts | Low | Existing workflow; 33 tests currently pass |

### 19.3 MCP server evaluation

MCP servers are optional implementation aids; none are runtime dependencies and none are required to use the finished product.

| MCP server | Recommendation | Precise use in this project | Setup / permissions | Cost, privacy, and risk |
|---|---|---|---|---|
| [Microsoft Playwright MCP](https://github.com/microsoft/playwright-mcp) | **Use during implementation if the environment permits** | Navigate all three routes, operate the landing demo/scenario selector, inspect accessibility snapshots, exercise sign-off and capture viewport evidence | Node 18+, browser install, local server. Grant access only to local app URLs | Apache-2.0 at research time. Browser sessions can expose local app content; do not connect production banking data |
| [Chrome DevTools MCP](https://github.com/ChromeDevTools/chrome-devtools-mcp) | **Use for performance diagnostics** | Trace LCP/INP/CLS, inspect network requests and console errors, validate CPU/mobile behavior | Local Chrome debugging access | Open-source at research time; debugging sessions can expose page data. Use seeded scenarios only |
| [Figma official MCP](https://developers.figma.com/docs/figma-mcp-server/local-server-installation/) | **Optional, only if a maintained Figma file is created** | Read variables/component context or send implementation screenshots; prevent design-code token drift | Figma desktop local server or remote setup; account and file access required | Figma plan/account terms apply; shared files may contain sensitive annotations. No need for this plan alone |
| Deque Axe MCP | **Do not require** | Advanced guided/remediation testing if the team already licenses it | Axe DevTools bundle/license and data-sharing review | Commercial license; advanced workflows may transmit data to Deque. Use local `axe-core` first |

Do not install an MCP solely for novelty. Pin server/package versions, inspect requested permissions, restrict URLs/files, and never send real trade documents, credentials, secrets, or personal data to a remote service. The official [Figma MCP tools reference](https://developers.figma.com/docs/figma-mcp-server/tools-and-prompts/) and each server repository must be reviewed again at setup time.

### 19.4 Dependency policy

- Every dependency must map to a named behavior in this plan.
- Prefer one primitive system and one animation system.
- Commit lockfile changes and record license/version in the PR.
- Run `npm audit` as a signal, then assess exploitability; do not make blind breaking upgrades.
- No dependency may obscure telemetry, legal evidence, or the human gate.
- No hosted analytics, fonts, images, or UI services are necessary for v1.

---

## 20. Frontend Architecture and Component System

### 20.1 Target component hierarchy

```text
RootLayout (server)
├─ ThemeBootstrap (small client boundary)
├─ SkipLink
└─ route content
   ├─ LandingPage (/; server composition)
   │  ├─ LandingMasthead / narrative sections
   │  └─ EvidenceGate + GuidedDecisionDemo (client islands)
   └─ AppShell (/examine and /evals; server where possible)
      ├─ ProductMasthead
      │  ├─ PrimaryNav
      │  ├─ ThemeMenu (client)
      │  └─ ApiHealthIndicator (client)
      ├─ ExaminationPage
      │  └─ ExaminationWorkbench (client state owner)
      │     ├─ JudgeHandoff
      │     ├─ CaseMasthead / ScenarioSelect
      │     ├─ RunTelemetryStrip
      │     ├─ EvidenceFolio
      │     ├─ DecisionSpine / StageRow
      │     ├─ RuleMatrix / RuleRow
      │     ├─ DecisionDocket
      │     ├─ HumanApprovalDialog
      │     └─ ProofDrawer
      └─ EvalsPage
         └─ BenchmarkWorkbench (client state owner)
            ├─ BenchmarkBrief
            ├─ ArchitectureLedger
            ├─ ScenarioResults
            └─ ProvenanceFooter
```

### 20.2 Server/client boundaries

- Keep route metadata, landing narrative, static masthead structures, fonts, and route shells server-rendered.
- Use client components only for fetch/SSE state, theme choice, dialogs, drawers, and interactive evidence linking.
- Do not place the entire root layout behind `"use client"`.
- The existing backend stays the source of truth. Do not replicate decision rules in TypeScript.
- Seeded scenario copy can be presentation metadata, but outcomes and evidence must come from API responses.
- The predefined landing walkthrough is the sole exception: it is a clearly labeled, typed presentation fixture cross-checked against golden-case expectations and never presented as a live run.

### 20.3 Data access layer

Extract the current page-local fetch logic into typed functions:

```text
getHealth()
getScenarios()
getScenario(lcId)
inspectExtraction(lcId)
openExaminationStream(lcId, handlers)
approveAction(lcId, payload)
getSponsorEvidence(lcId)
runEvaluations()
getEvaluationResults()
```

Define a normalized `ApiError` with endpoint, HTTP status, user-safe message, and retryability. Keep raw error detail in development logs only; never expose secrets or upstream credentials.

### 20.4 Examination reducer

One reducer owns case-scoped UI state to make event ordering explicit:

```ts
type ExaminationState = {
  lcId: string;
  phase: "idle" | "streaming" | "interrupted" | "failed" |
         "recommended" | "awaiting_signoff" | "signoff_error" | "authorized";
  stages: Record<StageId, StageState>;
  result: ExaminationResult | null;
  receipt: ApprovalReceipt | null;
  selectedEvidenceId: string | null;
  activeInspector: "federation" | "amendments" | "model" | "proof" | null;
  error: ApiError | null;
};
```

Reducer actions include `CASE_SELECTED`, `RUN_STARTED`, `STAGE_RECEIVED`, `STREAM_INTERRUPTED`, `RUN_FAILED`, `RECOMMENDATION_RECEIVED`, `SIGNOFF_OPENED`, `SIGNOFF_FAILED`, and `AUTHORIZED`. Ignore events whose captured `lcId` or run token does not match current state.

### 20.5 SSE lifecycle

- Retain the `EventSource`/stream handle in a ref.
- Close it on case switch, rerun, unmount, terminal event, or unrecoverable error.
- Generate a local run token; handlers check the token before dispatch.
- Model reconnect behavior explicitly. If native `EventSource` retry could duplicate stages, deduplicate by stable stage identity.
- Do not fabricate stage timing. Display backend duration/timestamps when provided; otherwise display order only.
- Announce milestones politely, not every token or minor update.

### 20.6 Type model

Create separate types for:

- `ScenarioSummary` and `ScenarioDetail`;
- `StageEvent` discriminated by real event type;
- `DeterministicCheck` versus `SemanticFinding`;
- `ExecutionTelemetry` with Zetaris and NIM enums;
- `DecisionRecommendation` restricted to the three exact action enums;
- `ApprovalReceipt` including hashes/Merkle/dispatch fields actually returned;
- `EvaluationResult` and its provenance.

Avoid a universal `any` event shape. Runtime-validate critical action and telemetry enums at the network boundary with small type guards; a schema library is optional and not justified solely for these responses.

### 20.7 Theme architecture

- Default server output to light.
- Apply a tiny pre-hydration theme script through `next-themes` or an equivalent reviewed implementation to avoid flash.
- Support `light`, `dark`, and `system`; persist only this preference.
- Keep all component colors semantic. Never branch JSX solely for a color theme.
- Test browser auto-fill, native form controls, focus rings, code blocks, and status tints in both modes.

### 20.8 Error and observability design

- A top-level error boundary protects each workbench, while stage/action errors remain local.
- Development logging may include event type and case ID, not document content or credentials.
- Client telemetry, if later introduced, requires a separate privacy/security decision. This plan adds none.
- UI labels must distinguish configured availability, endpoint health, and observed run mode.

---

## 21. Responsive and Accessibility Strategy

### 21.1 Breakpoints by behavior

| Range | Layout behavior |
|---|---|
| `< 640 px` | Single-column workbench; three-region segmented navigation; compact masthead; full-width bottom-safe primary action |
| `640–767 px` | Single column with wider evidence rows; approval remains full-screen dialog |
| `768–1023 px` | Two-region tablet layout or tabs; drawers may use 80vw; no fixed viewport-height trap |
| `1024–1279 px` | Evidence plus combined reasoning/docket; sticky docket only within available viewport |
| `1280–1599 px` | Full three-column 5/3/4 grid |
| `≥ 1600 px` | Same grid capped near 1728 px; add breathing room, not more tiny columns |

Support 320 CSS px width without page-level horizontal scroll. Use `min-height: 100dvh`, allow document scrolling, and avoid the current `h-screen` + `overflow-hidden` constraint. Respect safe-area insets for mobile controls.

### 21.2 Keyboard model

- First focusable item is a skip link to `main`.
- Logical order follows masthead → case → run → evidence → stages → docket; CSS visual rearrangement must not scramble DOM order.
- Native buttons/selects/links are preferred.
- `Tab` moves between controls; arrow keys are reserved for documented composite widgets such as tabs.
- `Enter`/`Space` activate controls; `Escape` closes dialogs/drawers and returns focus.
- Evidence-to-check links are real buttons or anchors, not clickable `div`s.
- No single-key shortcuts in v1. If added later, they need discovery and remapping/disable controls.

### 21.3 Screen-reader semantics

- Landmarks: `header`, `nav`, one `main`, and named complementary inspector where appropriate.
- One route-level `h1`; headings form a hierarchy without skipped levels.
- Stage sequence is an ordered list; active item uses `aria-current="step"`.
- Wide rule matrix uses a real table with headers; mobile transformation uses a definition list or preserves accessible table semantics.
- Status uses visible text; icons are hidden when redundant.
- SSE announcements are concise in a polite live region: “Deterministic checks complete. Two discrepancies.”
- Approval failures use field-linked error messages and an error summary.
- Hashes, enum strings, and citation labels remain copyable and pronounceable; provide expanded labels where abbreviations are ambiguous.

### 21.4 Visual accessibility

- Target WCAG 2.2 AA: 4.5:1 normal text, 3:1 large text, 3:1 meaningful UI graphics/components.
- Focus indicators must meet WCAG 2.2 focus appearance requirements in context.
- 200% zoom must not lose content or function; 400% reflow is tested at 1280 px viewport equivalent.
- Never communicate compliant/discrepant/live/fallback using hue alone.
- Avoid fully justified text, long uppercase strings, and low-contrast decorative rules behind text.
- Tooltips remain available by keyboard and do not obscure the trigger.
- Forced-colors mode gets visible borders, native system colors, and no background-image-dependent status.

### 21.5 Cognitive and operational accessibility

- Put the observed fact before the citation.
- Keep exact terminology stable across stages, matrix, and docket.
- Separate documentary compliance from AML risk.
- Explain fallback/replay modes without alarmist wording.
- Confirmation states state what will happen, not merely “Are you sure?”
- Preserve user-entered examiner text after a recoverable error.
- Do not time out or auto-dismiss decisive evidence or errors.

### 21.6 Touch and mobile details

- Minimum 44×44 targets and 8 px separation for adjacent critical actions.
- No hover-only evidence. Tap selects; second explicit action opens detail.
- Approval dialog uses a scrollable body and sticky action footer above the safe area.
- Long source IDs/hashes wrap or use a dedicated copy control; never force horizontal viewport overflow.
- Test portrait and landscape with software keyboard open.

### 21.7 Required manual accessibility checks

Automated checks cannot establish full conformance. Manually test:

1. Keyboard-only journeys for all three decisions.
2. NVDA + Chrome on Windows; VoiceOver + Safari if hardware is available.
3. 200% zoom and 400% reflow.
4. Windows High Contrast/forced colors.
5. Light/dark contrast in all statuses.
6. Reduced-motion behavior.
7. Dialog focus containment/return and SSE announcements.
8. Error recovery without losing sign-off text.

---

## 22. Performance Engineering Strategy

The current production build is the baseline: the present terminal at `/` reports approximately 120 kB first-load JS and `/evals` approximately 115 kB in the verified build on 23 Oct 2026. After migration, compare that terminal baseline to `/examine`; the new `/` landing follows the tighter LP-17 budget. The redesign must not turn this focused three-route product into a showcase bundle.

### 22.1 User-facing budgets

At the 75th percentile in field measurement when real-user monitoring becomes available, target the [Core Web Vitals](https://web.dev/articles/vitals) “good” thresholds:

- LCP ≤ 2.5 s;
- INP ≤ 200 ms;
- CLS ≤ 0.1.

Local CI lab guardrails on a representative mid-tier mobile profile:

- initial shell LCP ≤ 2.5 s against mocked/local API;
- no layout shift when fonts, scenario metadata, or stages arrive;
- user input response ≤ 100 ms before network work begins;
- drawer/dialog open animation maintains 60 fps where measurable;
- no long task above 200 ms caused by UI animation/chart code.

### 22.2 Asset and bundle budgets

- Keep each route’s first-load JS at or below **150 kB gzipped as reported by the same Next build methodology**, with a preferred target near the current baseline.
- New initial-route JS attributable to motion/theme/dialog packages: target ≤ 25 kB gzipped; validate actual tree-shaken output.
- No WebGL, video, remotely hosted hero asset, or raster decorative background.
- Self-hosted font payload target ≤ 160 kB total for initial Latin subsets; preload only the UI font needed above the fold. Editorial/mono may load without blocking.
- Above-the-fold local image/document preview target ≤ 200 kB; use intrinsic dimensions and modern formats where source fidelity permits.
- Inline critical icons/SVG; no icon sprite request for a handful of marks.

### 22.3 Runtime practices

- Reserve stable dimensions for masthead, stage rows, and document surface.
- Lazy-load proof drawers and optional motion features.
- Virtualization is unnecessary for the current three scenarios/small matrices; add it only when measured row counts justify it.
- Avoid polling when SSE already carries progress.
- Abort/close obsolete requests and streams.
- Cache static fonts/assets with immutable fingerprints; never cache approval mutations.
- Display stale/bundled data provenance explicitly rather than hiding latency with fabricated results.

### 22.4 Reliability targets

- UI remains navigable when health, extraction, federation evidence, or eval endpoints fail independently.
- Completed stages and received evidence survive a stream interruption within the current page session.
- Duplicate/reordered SSE messages do not duplicate stage rows or authorize an action.
- An approval button is single-flight and idempotency behavior is not assumed unless the backend provides it.
- No optimistic `AUTHORIZED` state.

---

## 23. Hackathon Judge Experience

### 23.1 Ninety-second primary journey

| Time | Action | What the judge understands |
|---:|---|---|
| 0–10 s | Read the landing hero and select the `108%` evidence node | This is documentary-credit examination, not a chatbot |
| 10–22 s | Trigger `Show attempted override`; the deterministic boundary blocks it | AI may interpret but cannot erase failed math under UCP 600 Art. 28(f)(ii) |
| 22–32 s | Advance the predefined guided demo to stage 5, then choose `Open this case in the terminal` | Five accountable owners lead to a recommendation, not autonomous dispatch |
| 32–45 s | Run LC-2026-9104 in `/examine`; point to the live five-stage spine | The landing story maps directly to the working product |
| 45–58 s | Federation completes; show honest live/fallback receipt | Three data silos are joined with observable execution provenance |
| 58–70 s | Show the locked 108% vs 110% result and separate demurrage advisory | Python owns the fact; advisories do not alter the legal verdict |
| 70–82 s | Open sign-off gate and authorize MT734 refusal | The system recommends; a human performs the final action |
| 82–90 s | Show receipt digest, then open the benchmark teaser/full `/evals` route | The outcome is auditable and the architecture is empirically compared |

Never depend on a live sponsor API during the only demo path. If fallback/cached modes are active, name them plainly and frame them as reproducible evidence—not as live cloud execution.

### 23.2 Five-minute expanded journey

1. Use the landing Evidence Gate and attempted override to establish the product and hard invariant.
2. Follow the guided-case handoff into `/examine` and run LC-2026-9104.
3. Show amendment memory and semantic tolerance on LC-2026-8841, including accepted vs pending terms.
4. Show LC-2026-9920 to prove documentary compliance can coexist with an AML hold.
5. Inspect the join-safe federation receipt and per-run sponsor telemetry.
6. Authorize one action and inspect cryptographic proof.
7. Open the benchmark page and explain the neural-only/rules-only/hybrid deltas.
8. Toggle dark mode only after the product story; theme is polish, not the pitch.

### 23.3 Failure-ready demo path

- Preflight `/api/v1/health`, all three scenario calls, one examination, and eval results.
- Warm only legitimate caches; never relabel replay as uncached.
- If NIM is unavailable, use `CACHED_REPLAY` and say so.
- If Zetaris is unavailable, use `LOCAL_DUCKDB_FALLBACK` and say so.
- If the API is fully unavailable, `/evals` may show clearly labeled bundled demo data; do not perform a fake fresh run.
- Keep a screen recording as an event contingency, not as a claim of current runtime.

### 23.4 Product UX alignment with judging

The official rubric weights Impact 30%, Technical Implementation 20%, Innovation 15%, Demo 15%, Product/UX 10%, and Sponsor Technology 10%. The interface should therefore spend its visual emphasis in the same order: consequential decision, reliable architecture, differentiating invariant, crisp demonstration, then visual flourish. Sponsor telemetry is made legible at the evidence point, not multiplied into logo walls.

---

## 24. File-by-File Implementation Blueprint

This blueprint is deliberately frontend-focused. Backend code and contracts remain unchanged unless a separately approved task addresses a verified gap. “New” means proposed in a future implementation PR, not created by this planning task.

### 24.1 Existing files

| File | Planned change | Responsibility after redesign |
|---|---|---|
| `apps/web/src/app/layout.tsx` | Refactor | Server root, global metadata defaults, self-hosted font variables, light-first theme bootstrap, skip link; route groups choose landing or app shell |
| `apps/web/src/app/globals.css` | Replace visual layer carefully | Semantic tokens, typography, reset, focus, forced colors, reduced motion, reusable ledger primitives |
| `apps/web/src/app/page.tsx` | Replace after parity gate | Server-rendered landing composition described in the dedicated Landing Page chapter |
| `apps/web/src/app/evals/page.tsx` | Decompose | Benchmark route composition, provenance-aware fetching, responsive semantic comparison |
| `apps/web/src/components/HeaderBar.tsx` | Refactor/rename | Application masthead for `/examine` and `/evals`; configured health separated from observed run mode |
| `apps/web/src/components/DocumentViewerPane.tsx` | Refactor | Evidence folio using returned extraction fields/boxes/digests; honest fixture label |
| `apps/web/src/components/AdjudicationMatrixPane.tsx` | Refactor | Rule matrix with deterministic/semantic distinction, legal refs, evidence selection |
| `apps/web/src/components/DecisionActionPane.tsx` | Refactor | Decision docket and explicit human approval workflow; no premature success |
| `apps/web/src/components/ZetarisDrawer.tsx` | Refactor/rename | Accessible proof inspector driven by backend evidence rather than drifting static SQL |
| `apps/web/tailwind.config.js` | Extend minimally | Semantic colors/fonts/spacing aliases; no duplicated hex values |
| `apps/web/package.json` | Future dependency change | Add only reviewed Motion, Radix Dialog, and next-themes packages if approved |
| `apps/web/package-lock.json` | Generated in implementation | Lock exact reviewed versions |
| `apps/web/next.config.js` | Review | Font/image/build settings only where required; retain safe defaults |
| `apps/web/tsconfig.json` | Keep strict | Add path aliases only if they materially clarify imports |

### 24.2 Proposed new files

| File | Purpose |
|---|---|
| `apps/web/src/app/examine/page.tsx` | New home of the complete terminal composition formerly rendered at `/` |
| `apps/web/src/app/opengraph-image.tsx` | Static, non-sensitive Evidence Gate social image |
| `apps/web/src/components/shell/AppShell.tsx` | Shared masthead/nav/main layout |
| `apps/web/src/components/shell/ThemeMenu.tsx` | Light/dark/system control |
| `apps/web/src/components/shell/TelemetryStrip.tsx` | Observed per-run modes and provenance |
| `apps/web/src/components/examination/ExaminationWorkbench.tsx` | Client state owner and layout composition |
| `apps/web/src/components/examination/CaseMasthead.tsx` | API-backed case selector and case facts |
| `apps/web/src/components/examination/DecisionSpine.tsx` | Five-stage ordered visualization |
| `apps/web/src/components/examination/StageRow.tsx` | One stage’s accessible states/details |
| `apps/web/src/components/examination/EvidenceFolio.tsx` | Document/extraction/source surface |
| `apps/web/src/components/examination/RuleMatrix.tsx` | Grouped check/finding list |
| `apps/web/src/components/examination/RuleRow.tsx` | Calculation, authority, citation, evidence link |
| `apps/web/src/components/examination/DecisionDocket.tsx` | Recommendation and bounded rationale |
| `apps/web/src/components/examination/HumanApprovalDialog.tsx` | Human gate, sign-off form, error and receipt transition |
| `apps/web/src/components/examination/ApprovalReceipt.tsx` | Signed action, digest/Merkle, dispatch status |
| `apps/web/src/components/examination/ProofDrawer.tsx` | Accessible amendment/federation/model/proof inspection |
| `apps/web/src/components/examination/JudgeHandoff.tsx` | Compact case/tour handoff shown only for `tour=1` |
| `apps/web/src/components/landing/LandingMasthead.tsx` | Public section/route navigation and compact mobile menu |
| `apps/web/src/components/landing/HeroSection.tsx` | Server-rendered headline, CTAs, proof line, and gate shell |
| `apps/web/src/components/landing/EvidenceGate.tsx` | Small client island linking predefined source, rule, and action |
| `apps/web/src/components/landing/FailureSection.tsx` | Three real failure modes in editorial sequence |
| `apps/web/src/components/landing/InvariantDemonstration.tsx` | Interactive but predetermined hard-invariant explanation |
| `apps/web/src/components/landing/GuidedDecisionDemo.tsx` | Five-step, predefined LC-2026-9104 walkthrough |
| `apps/web/src/components/landing/ArchitectureSection.tsx` | Five accountable owners/stages and progressive activation |
| `apps/web/src/components/landing/OutcomesSection.tsx` | Honour/refuse/AML-hold disclosures |
| `apps/web/src/components/landing/ProofSection.tsx` | Chain-of-custody and honest telemetry explanation |
| `apps/web/src/components/landing/BenchmarkTeaser.tsx` | Compact verified-baseline comparison linking to `/evals` |
| `apps/web/src/components/landing/FinalInvitation.tsx` | Final human-authority statement and route CTAs |
| `apps/web/src/components/landing/ProductFooter.tsx` | Product navigation and factual project context |
| `apps/web/src/components/evals/BenchmarkWorkbench.tsx` | Evals client state owner |
| `apps/web/src/components/evals/ArchitectureLedger.tsx` | Semantic three-architecture comparison |
| `apps/web/src/components/evals/ScenarioResults.tsx` | Per-scenario results and evidence disclosure |
| `apps/web/src/components/ui/AuthorityStamp.tsx` | Consistent owner/source labeling |
| `apps/web/src/components/ui/StatusMark.tsx` | Shape/icon/text status grammar |
| `apps/web/src/components/ui/LegalCitation.tsx` | Exact citation rendering and explanation |
| `apps/web/src/components/ui/NoticeRegion.tsx` | Visible and assistive status/error messages |
| `apps/web/src/lib/api.ts` | Typed backend calls and error normalization |
| `apps/web/src/lib/sse.ts` | Stream lifecycle, parsing, run-token and dedupe logic |
| `apps/web/src/lib/types.ts` | API/event/result discriminated unions |
| `apps/web/src/lib/examination-reducer.ts` | Explicit state machine reducer |
| `apps/web/src/lib/presentation.ts` | Non-decisional labels/grouping and evidence mappings |
| `apps/web/src/lib/legal-citations.ts` | Exact approved citation labels; no decision logic |
| `apps/web/src/lib/motion.ts` | Shared variants/tokens and reduced-motion helpers |
| `apps/web/src/lib/format.ts` | Money/date/percent/hash formatting |
| `apps/web/src/lib/theme.ts` | Theme constants/storage key |
| `apps/web/src/lib/landing-story.ts` | Typed, clearly labeled demo copy cross-checked with golden-case expectations |
| `apps/web/src/lib/landing-motion.ts` | Landing-specific variants built from shared motion tokens |
| `apps/web/src/app/error.tsx` | Route error boundary with recovery |
| `apps/web/src/app/loading.tsx` | Stable shell loading state if routing needs it |
| `apps/web/e2e/examination.spec.ts` | Three case journeys and stream lifecycle |
| `apps/web/e2e/evals.spec.ts` | Live vs bundled provenance and benchmark behavior |
| `apps/web/e2e/landing.spec.ts` | Landing content, predefined demo, route handoff, no-live-call, theme, and responsive behavior |
| `apps/web/e2e/accessibility.spec.ts` | Axe smoke tests and key keyboard assertions |

### 24.3 Files that must remain decision authorities

- `apps/api/engines/ucp600_deterministic.py`: all math, date, tolerance, and threshold verdicts.
- `apps/api/engines/ucp600_legal_adjudicator.py`: scoped semantic/legal adjudication under the hard invariant.
- `apps/api/engines/decision_engine.py`: recommendation assembly.
- `apps/api/engines/artifact_generator.py`: MT734/AML/action artifacts.
- `apps/api/memory/amendment_memory.py`: amendment state.
- `apps/api/zetaris/sql/federated_check.sql`: join-safe, exactly-one-row federation.
- `apps/api/main.py`: endpoint/SSE/approval contracts.

The frontend may format or group their outputs, but it must never recalculate a legal verdict, upgrade a status, or synthesize an action that the backend did not return.

---

## 25. Functional Preservation and Migration Strategy

### 25.1 Non-negotiable preservation matrix

| Capability | Existing contract | Redesign obligation |
|---|---|---|
| Health | `GET /api/v1/health` | Show reachability/config separately from observed run telemetry |
| Scenario discovery | `GET /api/v1/scenarios` | Populate selector from API; retain all three golden scenarios |
| Scenario detail | `GET /api/v1/scenarios/{lc_id}` | Preserve all available case facts and robust missing-data states |
| Extraction | `POST /api/v1/extract/{lc_id}` | Show returned mode, records, boxes/digests; call it fixture when response says fixture |
| Examination stream | GET and POST `/api/v1/examine/{lc_id}` with stream behavior | Preserve five stages, order, fields, errors, and real mode telemetry |
| Human action | `POST /api/v1/examine/{lc_id}/approve-action` | Keep action blocked until recommendation; require explicit examiner sign-off; show only server receipt |
| Sponsor proof | `GET /api/v1/evidence/sponsors/{lc_id}` | Surface real federation receipt/source modes without drifting duplicate claims |
| Evaluation run | `POST /api/v1/evals/run` | Preserve fresh-run behavior and pending/error states |
| Evaluation results | `GET /api/v1/evals/results` | Preserve all baseline metrics and label bundled fallback visibly |
| Decision enums | Three exact actions | Never rename the machine values or add an unsupported action |
| Hard invariant | Deterministic failure is locked | Visual order and wording reinforce; frontend never overrides |
| Join safety | One federation row per LC | UI may display receipt/cardinality but never alters SQL |
| Telemetry | Exact live/fallback and live/cache modes | Use exact enums at point of use and in receipt |
| Current root terminal | Complete examination UI at `/` | Move intact to `/examine`, prove parity before root cutover, and update all internal/demo links |
| Public landing | No current route | Add at `/` as server-rendered product story; no new backend mutation or unsupported capability |

### 25.2 Incremental migration

1. Capture current route screenshots, API fixture payloads, keyboard behavior, build sizes, and the 33-test/backend baseline.
2. Move the unchanged terminal composition to `/examine`, add route-parity tests, and keep `/` on the terminal until those tests pass.
3. Add semantic tokens and light/dark theme behind the existing component structure; do not change data flow yet.
4. Build the server-rendered landing skeleton, honest predefined demonstration, and route handoff; cut `/` over only after step 2.
5. Extract typed API/SSE/state utilities with characterization tests while rendering the existing terminal UI.
6. Build the new shell and workbench primitives alongside existing panes.
7. Migrate one vertical slice first: LC-2026-9104 run → discrepancy → refusal sign-off → receipt.
8. Add LC-2026-8841 amendment/semantic cases and LC-2026-9920 AML dual-lane case.
9. Migrate `/evals`, including unmistakable fallback provenance.
10. Add motion only after static behavior, keyboard order, and state semantics pass.
11. Remove obsolete pane code only after landing, examination, and evaluation route tests pass.

Avoid a long-lived parallel “v2” route: it risks divergent contracts and a demo switch. Short-lived component-level feature flags are acceptable only if they are removed before submission.

### 25.3 Data compatibility

- Normalize optional/missing fields without inventing values.
- Preserve unknown enum values as visible `Unknown: <value>` diagnostics and disable affected irreversible actions.
- Use presentation mappings only for labels/order; never transform check outcomes.
- Keep exact raw enum/source data accessible in proof details.
- If the API schema changes during implementation, update typed fixtures and tests before visuals.

### 25.4 Rollback strategy

Implement in small commits by foundation, terminal, evals, and polish. Because no database migration is required, rollback is a frontend deploy/revert. Do not delete the previous components until the new journeys pass production build, automated smoke tests, and manual sign-off. Preserve the lockfile for deterministic dependency rollback.

---

## 26. Testing and Acceptance Criteria

### 26.1 Required command gates

Run from repository root unless noted:

```powershell
.\.venv\Scripts\pytest.exe apps/api/tests/ -v
Set-Location apps/web
npm run build
```

When the future Playwright setup exists, also run its pinned project command (recommended `npm run test:e2e`). Do not mark the redesign complete if any existing backend test or the production build regresses.

### 26.2 Functional acceptance matrix

| Journey | Acceptance criteria |
|---|---|
| Landing comprehension | Hero states domain/value/invariant/human gate; all demonstrations say predefined; no examination call occurs |
| Landing handoff | `/examine?case=LC-2026-9104&tour=1` selects a valid real case without auto-running; normal and browser-back navigation work |
| Scenario discovery | Selector is API-backed; loading, empty, error, and all three seeded results are operable |
| Run lifecycle | Stages appear once, in correct order; completed work stays visible; obsolete stream is closed on switch/rerun |
| 8841 honour | Amendment states and semantic allowances are legible; exact citations; honour remains human-gated |
| 9104 refusal | 108%/110%/$9,600 calculation is locked discrepant; advisory never changes verdict; MT734 action is gated |
| 9920 AML | Documentary compliance and risk signals are separate; compliance hold is gated |
| Approval | No pre-response authorized state; double-submit prevented; errors preserve input; real receipt fields render |
| Telemetry | Zetaris and NIM execution enums exactly match response; pre-run health is not mislabeled as observed run mode |
| Extraction | `STRUCTURED_FIXTURE` is visible when returned; source anchors/boxes/digests degrade gracefully |
| Evals | Fresh and bundled results cannot be confused; percentages show numerator/denominator where available |
| Theme | Light first paint; dark/system persist; no hydration flash or unreadable native controls |

### 26.3 Automated test layers

- **Unit:** reducer transitions, stale run-token rejection, event dedupe, formatters, presentation mapping, enum guards.
- **Component:** stage/status variants, rule table semantics, decision docket, approval validation/error, dialog focus behavior, both themes.
- **Route E2E:** landing demo/handoff/no-live-call; three examination journeys; interrupted SSE; scenario switch during stream; failed approval; eval API failure/bundled label; deep keyboard sequence.
- **Accessibility automation:** axe checks for all three routes, both themes, landing interactive states, and examination initial/running/completed/dialog states. Treat violations as failures; document genuine false positives narrowly.
- **Visual regression:** 360×800, 768×1024, 1024×768, 1440×900, and 1920×1080; light and dark; landing hero/demo/proof/final CTA; all three final decisions; approval dialog/receipt; eval fallback label.
- **Performance:** build size comparison and Lighthouse/DevTools trace on `/`, `/examine` initial/running/completed, and `/evals` results.

### 26.4 Manual acceptance

- Review every legal citation against the approved rule list.
- Verify deterministic failure cannot be visually or interactively changed.
- Inspect actual network payload against every displayed telemetry badge.
- Run keyboard/screen-reader/zoom/forced-colors/reduced-motion checks from Section 21.
- Throttle network and CPU; confirm progress does not look frozen or falsely complete.
- Test API down, NIM replay, Zetaris fallback, and malformed/unknown enum states.
- Have a trade-finance subject-matter reviewer validate terminology, priority, and action consequence copy.
- Rehearse 90-second and five-minute demo paths without developer narration filling UI gaps.

### 26.5 Definition of done

The redesign is done only when:

- all existing capabilities and contracts in Section 25 pass;
- no source-mode or authorization claim is misleading;
- both themes and specified viewports pass visual/accessibility review;
- backend tests and frontend production build pass;
- performance budgets are met or a documented exception is approved;
- no P0/P1 accessibility or functional defects remain;
- `STATUS.md`, README screenshots/demo guidance, and graphify output (after code changes) are current.

---

## 27. Implementation Phases and Dependency Order

### Phase A — Contract lock and characterization (0.5–1 day)

- Save representative responses for health, scenarios, extraction, all SSE stages, approval receipt, sponsor evidence, and evals.
- Add/confirm frontend test harness and current-root route smoke tests.
- Record current screenshots and bundle output.
- Resolve any payload ambiguity before component work.

**Exit:** fixtures reflect real backend, all current tests/build green.

### Phase B — Route safety and foundations (1–1.5 days)

- Move the current root terminal composition to `/examine`; establish parity before changing `/`.
- Add semantic tokens, self-hosted fonts, light/dark/system theme, focus/reduced-motion foundations.
- Refactor the shared shell, navigation, and truthful health/telemetry distinction.
- Add core `StatusMark`, `AuthorityStamp`, `LegalCitation`, and notice components.

**Depends on:** Phase A. **Exit:** `/examine` passes old-root functional parity; shell passes two-theme, keyboard, and responsive smoke tests.

### Phase C — Landing product story (1.5–2 days)

- Build the server-rendered landing, metadata, Evidence Gate hero, hard-invariant section, and exact CTA architecture.
- Add the typed predefined walkthrough, five-stage interactions, responsive/mobile navigation, and no-JS state.
- Complete remaining narrative sections, route handoff, landing tests, and static accessibility review before motion.

**Depends on:** B. **Exit:** LP-20 functional criteria pass; `/` can cut over without affecting `/examine` or `/evals`.

### Phase D — State and data architecture (1–1.5 days)

- Extract typed API functions, critical runtime guards, SSE manager, and examination reducer.
- Implement cancellation, dedupe, stale-event protection, and local error handling.
- Keep old panes rendering through adapters until parity is demonstrated.

**Depends on:** A/B. Can overlap C after route safety. **Exit:** reducer/SSE unit tests pass.

### Phase E — Examination vertical slice (2–3 days)

- Build Case Masthead, Decision Spine, Evidence Folio, Rule Matrix, and Docket.
- Complete LC-2026-9104 from run through receipt.
- Add accessible proof inspectors and approval dialog.
- Add 8841 and 9920 presentations without special-case decision logic.

**Depends on:** B and D. **Exit:** all three E2E decisions and manual invariant review pass.

### Phase F — Benchmark route (1 day)

- Build comparison ledger, scenario results, provenance states, and responsive transformation.
- Clearly label bundled fallback and preserve prior result provenance on errors.

**Depends on:** B and API utilities from D. **Exit:** eval E2E and accessibility tests pass.

### Phase G — Motion, proof polish, and performance (1 day)

- Add Motion only to approved landing and application recipes after static parity.
- Implement one-time receipt seal, lineage highlighting, and reduced-motion variants.
- Tune fonts/assets/code-splitting against budgets.

**Depends on:** C/E/F. **Exit:** no motion-dependent meaning; landing and app bundle/performance gates pass.

### Phase H — Cross-browser QA and demo hardening (1–2 days)

- Execute full test matrix, domain copy review, failure drills, and judge rehearsals.
- Update screenshots/readme/status; run `graphify update .` because code changed.
- Freeze dependency and visual changes before recording.

**Depends on:** all prior phases. **Exit:** definition of done and demo contingency checklist complete.

### Suggested priority if time compresses

Ship A–C for the truthful landing and safe route split, then D–E for terminal robustness, then F. Motion is the first scope to reduce; never reduce truthful demo labeling, telemetry, human gating, responsive basics, error states, or accessibility to preserve decorative polish.

---

## 28. Risks, Tradeoffs, and Mitigations

| Risk | Likelihood / impact | Mitigation |
|---|---|---|
| UI overstates “live” sponsor execution | Medium / critical credibility | Use observed response enums at point of use; pre-run says unknown; test payload-to-badge mapping |
| Frontend accidentally becomes a decision authority | Low / critical safety | Type/group only; no verdict calculations; invariant-focused E2E/domain review |
| Free-text sign-off looks authenticated | High / high | Label “examiner sign-off,” not identity verification; document current limitation; no avatar/RBAC fiction |
| In-memory run state loses receipt on restart | High / medium | Do not promise persistent history; show receipt in session and describe prototype limitation |
| Demo countdown implies banking-calendar accuracy | High / high | Label illustrative or replace with non-legal elapsed time until backend calendar exists |
| Fixture extraction is presented as live OCR | High / high | Render exact extraction mode and remove misleading button copy |
| Evidence lineage payload lacks stable IDs | Medium / medium | Map only provable links; omit connectors where causality is ambiguous; propose future schema separately |
| Three-column density fails on laptop/mobile | Medium / high | Behavioral breakpoints, single-column regions below 1024 px, real viewport testing |
| Light theme weakens “command center” drama | Low / medium | Use editorial authority, decisive typography, rules, and controlled copper—not dark-only spectacle |
| Motion delays evidence or causes vestibular issues | Low / high | Small durations, reduced-motion parity, static-first implementation, reject scroll/3D effects |
| New dependencies inflate bundle/supply-chain surface | Medium / medium | Three narrowly scoped additions maximum, pin/review/lazy-load, enforce 150 kB route budget |
| Automated a11y creates false confidence | High / medium | Manual AT, zoom, forced-color, keyboard, and reduced-motion checks |
| Benchmark fallback is mistaken for fresh empirical run | High / high | Persistent `BUNDLED DEMO DATA` provenance and disabled “fresh” claim |
| Exact ICC text/citations are mishandled | Medium / high | Use approved citation labels; avoid reproducing copyrighted rule text; domain reviewer gate |
| Sponsor/reference sites or package terms change | Medium / medium | Date every source and recheck official docs/licenses at implementation |
| Visual redesign consumes demo preparation time | Medium / high | Vertical-slice order, strict scope, freeze date, motion as removable final phase |

### Accepted trade-offs

- The initial redesign supports three known cases rather than inventing a production queue.
- It favors semantic DOM and SVG over cinematic WebGL.
- It uses a small set of high-value primitives rather than a comprehensive design-system package.
- It presents explainable structured outputs, not hidden model reasoning.
- It keeps backend limitations visible rather than cosmetically masking them.

---

## 29. Final Design Quality Checklist

### Product truth

- [ ] `/` is the truthful public story, `/examine` preserves the full terminal, and `/evals` preserves the benchmark.
- [ ] Root cutover occurs only after `/examine` passes parity with the former `/` terminal.
- [ ] Scenario selector is fetched from the API.
- [ ] Exact three action enums are preserved.
- [ ] Deterministic discrepancies are immutable in UI.
- [ ] Documentary compliance and AML risk remain distinct.
- [ ] Sign-off is never described as authenticated unless authentication is added.
- [ ] Demo deadline/countdown is not presented as an authoritative banking calendar.

### Landing page

- [ ] Hero states the product domain, benefit, hard invariant, and human gate without scrolling.
- [ ] The Evidence Gate and guided case are always labeled predefined—not live.
- [ ] Landing interactions never trigger SSE, sponsor calls, artifacts, or approval.
- [ ] `Open this case` hands LC-2026-9104 into `/examine` without auto-running it.
- [ ] All nine narrative sections add distinct substance; no repeated feature-card filler remains.
- [ ] Landing and application share tokens, typography, authority stamps, motion, and theme state.
- [ ] Hero, invariant, guided demo, architecture, outcomes, proof, benchmark, and final CTA work without animation.
- [ ] Metadata, canonical URL, Open Graph asset, fragments, and no-JS content are correct.
- [ ] Landing-specific bundle and Core Web Vitals budgets pass.

### Telemetry and evidence

- [ ] `LIVE_ZETARIS` and `LOCAL_DUCKDB_FALLBACK` display exactly when observed.
- [ ] `LIVE_UNCACHED`/live NIM mode and `CACHED_REPLAY` display exactly as returned.
- [ ] `STRUCTURED_FIXTURE` is visible where applicable.
- [ ] Configured health and observed run mode are separate.
- [ ] Federation receipt/cardinality and source provenance are inspectable.
- [ ] No chain-of-thought or fake confidence is shown.

### Human action

- [ ] Final action is disabled before a backend recommendation.
- [ ] Dialog names case, action, reason, and consequence.
- [ ] Examiner sign-off has a real label and validation.
- [ ] Pending action prevents double-submit.
- [ ] `AUTHORIZED` appears only after successful server response.
- [ ] Receipt fields, digest/Merkle, and dispatch state are real response data.

### Design system

- [ ] Light is the first/default theme; dark and system work without flash.
- [ ] Semantic tokens replace component hex values.
- [ ] Typography, status shapes, authority stamps, rules, and evidence folios are consistent.
- [ ] No generic gradient hero, glass card grid, chatbot surface, or stock legal imagery.
- [ ] Both themes meet contrast requirements.
- [ ] All states exist: loading, empty, running, partial, error, complete, authorized, unavailable.

### Responsive and accessibility

- [ ] No page-level horizontal scroll at 320 px.
- [ ] All targets meet touch-size requirements.
- [ ] Keyboard order matches reading order.
- [ ] Skip link, landmarks, headings, labels, and table semantics are correct.
- [ ] Dialog focus trap/Escape/return work.
- [ ] SSE announcements are concise and non-disruptive.
- [ ] 200% zoom, 400% reflow, forced colors, and reduced motion pass.
- [ ] Status is never color-only.

### Performance and quality

- [ ] Route JS stays at or below the 150 kB build budget.
- [ ] Core Web Vitals lab/field targets are measured with methodology recorded.
- [ ] Fonts and optional motion are subset/lazy where appropriate.
- [ ] Obsolete streams/requests close on case switch and unmount.
- [ ] Backend suite and production frontend build pass.
- [ ] Three route E2E journeys, eval provenance, axe checks, and visual viewports pass.
- [ ] Legal/domain copy receives subject-matter review.
- [ ] `STATUS.md`, README/demo artifacts, and graphify output are updated after implementation.

---

## 30. Source References and Research Notes

All external sources below were accessed **23 October 2026**. Product/repository claims elsewhere in this document are verified from the local repository at commit/worktree state inspected on that date. Package versions are a time-stamped research snapshot, not an instruction to install without revalidation.

### 30.1 Hackathon and track evidence

- [Open Agent Hackathon 2026 event page](https://hackathon.genai.works/event/open-agent-hackathon-2026) — verified event dates, online format, team size, Track 02/03 descriptions, judging weights, and sponsor context.
- [Open Agent Hackathon 2026 Academy details](https://academy.genai.works/courses/open-agent-hackathon-2026/details) — verified public framing around production-oriented agents and sponsor technologies. Authenticated lesson content was not available in this research; no claim in this plan depends on it.

### 30.2 Sponsor and platform sources

- [Zetaris Meta Data Lakehouse](https://www.zetaris.com/zetaris-meta-data-lakehouse) — federated querying and zero-data-movement positioning.
- [Zetaris SQL Guide](https://kbase.zetaris.com/knowledge/sql-guide) — SQL capability reference.
- [Meterless Engines](https://meterless.ai/engines.html) and [Meterless GitHub](https://github.com/Meterless/Meterless) — public engine/memory/routing descriptions, including H-MEM, World Model, Markovian, and Scout references.
- [NVIDIA NIM function calling](https://docs.nvidia.com/nim/large-language-models/latest/function-calling.html) and [NIM offerings](https://docs.nvidia.com/nim/large-language-models/latest/about-nim-llm/nim-offerings.html) — structured/tool-capable OpenAI-compatible API context and model offering reference.
- [Cursor Rules documentation](https://cursor.com/docs/rules) — project rules and `AGENTS.md` support.

### 30.3 Human–AI interaction and explainability

- [Microsoft Guidelines for Human-AI Interaction](https://www.microsoft.com/en-us/haxtoolkit/ai-guidelines/) — expectation setting, context-aware behavior, correction, and user control.
- [Make clear why the system did what it did](https://www.microsoft.com/en-us/haxtoolkit/guideline/make-clear-why-the-system-did-what-it-did/) — rationale for visible evidence/reason links.
- [Scope services when in doubt](https://www.microsoft.com/en-us/haxtoolkit/guideline/scope-services-when-in-doubt/) — basis for restrained capability claims and safe fallbacks.
- [Google PAIR Guidebook: Explainability + Trust](https://pair.withgoogle.com/guidebook-v2/chapter/explainability-trust/) and [PAIR Patterns](https://pair.withgoogle.com/guidebook-v2/patterns) — uncertainty, mental models, feedback, and explanation patterns.

### 30.4 Accessibility and performance standards

- [WCAG 2.2 Recommendation](https://www.w3.org/TR/WCAG22/) and [What’s New in WCAG 2.2](https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/) — normative accessibility target and new criteria context.
- [Understanding Animation from Interactions](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions) and [Technique C39](https://www.w3.org/WAI/WCAG22/Techniques/css/C39) — reduced-motion requirements/technique.
- [WAI-ARIA APG Modal Dialog Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/) — focus, naming, keyboard, and modal semantics.
- [web.dev Web Vitals](https://web.dev/articles/vitals) — LCP, INP, and CLS “good” thresholds used in Section 22.
- [axe-core repository](https://github.com/dequelabs/axe-core) — automated accessibility engine and its documented limits; automation supplements manual review.

### 30.5 Product and visual references

- [Awwwards Sites of the Day](https://www.awwwards.com/websites/sites_of_the_day/) — current award-gallery survey for art direction, interaction, content, and usability; treated as inspiration, not evidence that heavy effects are appropriate.
- [Stripe: Connect front-end experience](https://stripe.com/blog/connect-front-end-experience) — primary account of telling a complex product story through a distinct but light surface.
- [Stripe Checkout](https://stripe.com/payments/checkout) — reference for pairing concise benefit copy with an operable, product-specific demonstration.
- [Linear: A calmer interface for a product in motion](https://linear.app/now/behind-the-latest-design-refresh) — 2026 reference for task emphasis, restrained chrome, consistent structure, and deliberate icon reduction.
- [Linear: Change for the better](https://linear.app/change) — October 2026 editorial product narrative reference; informs continuity of argument, not its visual styling or copy.
- [Vercel Design Engineer Principles](https://vercel.com/design/engineer) and [Design Engineering at Vercel](https://vercel.com/blog/design-engineering-at-vercel) — references for usefulness, full-state ownership, inclusive input, performance, and interaction craft.
- [Apple MacBook Air](https://www.apple.com/macbook-air/) — reference for large-scale typographic pacing and progressive product detail; the plan explicitly rejects its media weight and scroll spectacle for VERITAS.
- [Linear changelog](https://linear.app/changelog) — reference for dense scanability, keyboard quality, explicit agent attribution/status, and version history; not a palette/template to copy.
- [Vercel Observability](https://vercel.com/docs/observability) — reference for compact source/event/latency relationships.
- [Palantir Foundry data lineage overview](https://www.palantir.com/docs/foundry/data-lineage/overview) — reference for upstream/downstream evidence navigation.
- [Cyera AI Guardian design profile](https://www.designrush.com/best-designs/websites/cyera-ai-guardian-website-design) — award-recognized example of making an abstract product claim tangible through interaction; not a visual template.
- [CSS Design Awards](https://www.cssdesignawards.com/) — contemporary award-gallery survey used to identify and then reject portfolio-style excess for this operational product.
- [Figma Blog](https://www.figma.com/blog/) — current design-system, accessibility, and agent-assisted workflow context.

### 30.6 Framework, library, and tooling sources

- [Next.js App Router](https://nextjs.org/docs/app) — current routing/server-client architecture reference.
- [Motion for React](https://motion.dev/docs/react) and [Motion reduced-motion hook](https://motion.dev/docs/react-use-reduced-motion) — chosen animation API and accessibility support.
- [GSAP installation](https://gsap.com/docs/v3/Installation/) — evaluated animation alternative.
- [Radix accessibility](https://www.radix-ui.com/primitives/docs/overview/accessibility) and [Radix Dialog](https://www.radix-ui.com/primitives/docs/components/dialog) — selected primitive guidance.
- [next-themes repository](https://github.com/pacocoursey/next-themes) — proposed theme utility.
- [Playwright MCP](https://github.com/microsoft/playwright-mcp), [Chrome DevTools MCP](https://github.com/ChromeDevTools/chrome-devtools-mcp), and [Figma MCP installation](https://developers.figma.com/docs/figma-mcp-server/local-server-installation/) — optional implementation assistants reviewed in Section 19.
- [Playwright accessibility testing](https://playwright.dev/docs/next/accessibility-testing), [Storybook accessibility testing](https://storybook.js.org/docs/writing-tests/accessibility-testing), and [Chromatic visual tests](https://www.chromatic.com/docs/visual-tests-addon/) — proposed validation options.

### 30.7 Research classification and unresolved hypotheses

**Verified:** current routes, components, dependencies, API paths, response concepts, seeded scenarios, fallback behavior, deterministic/legal engines, test counts, build output, and the limitations listed in Section 2 were inspected in the repository. Official-event, sponsor, standards, and library claims are tied to the dated sources above.

**Recommendations:** Evidence Ledger direction, the new `/` landing and `/examine` route split, tokens, component system, Motion/Radix/next-themes adoption, frontend decomposition, budgets, responsive behavior, test strategy, and phased delivery are design/engineering proposals—not descriptions of implemented behavior.

**Hypotheses to validate with users:** examiners will scan decisive evidence faster with a folio/spine/docket structure; light-first editorial styling will feel more authoritative than the current dark terminal; the landing Evidence Gate will explain the hard invariant within five seconds; the guided predefined case will improve judge comprehension without being mistaken for live execution; and evidence-linked explanation will increase appropriate trust. Validate with at least three representative users or domain reviewers using task completion, time-to-decisive-evidence, incorrect action attempts, demo-provenance recall, explanation accuracy, and qualitative trust calibration.

### Final design mandate

Make the system’s strongest architectural idea impossible to miss: **evidence is federated, deterministic rules are locked, semantic AI is scoped, and a human authorizes the consequence.** Every visual decision should make that chain faster to inspect and harder to misinterpret.
