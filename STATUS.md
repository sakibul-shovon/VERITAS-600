# VERITAS-600: Project Execution & Agent Continuity Tracker

> **Notice to All Coding Agents (Cursor, Claude Code, Codex, Antigravity, etc.):**
> This file is the **Single Source of Truth** for current project state.
> Whenever you start a session, **read this file first** to determine where to resume work.
> Whenever you complete a sub-task or phase, **update this file immediately** before ending your turn.

---

## 🚦 Current Project Status at a Glance

| Attribute | Current Value |
| :--- | :--- |
| **Current Phase** | **Phase 11 Adversarial Red-Team Remediation ✅ [COMPLETED & VERIFIED] on `main`** |
| **Overall Progress** | **Phases 0–11 complete & verified. All 19 security findings from red-team audit remediated. 58/58 pytest suite green. Next.js 15 production build passes cleanly.** |
| **Active Task** | Complete & Verified. Zero open security issues. |
| **Last Updated** | 2026-10-24 |
| **Next Action Item** | **Production deployment & hackathon submission review.** |

```
[CORE PHASES 0–8: COMPLETE & VERIFIED] [PHASE 9: VERIFIED] [PHASE 10: COMPLETE 46/46 PYTEST] [PHASE 11: REMEDIATED 58/58 PYTEST & VERIFIED]
```

---

## 👉 WHERE TO START NEXT (For the Next Agent)

1. **Security & Audit Reports:**
   - [SECURITY_REMEDIATION_REPORT.md](file:///h:/Projects/VERITAS-600/SECURITY_REMEDIATION_REPORT.md) — Comprehensive technical documentation of all 19 remediated vulnerabilities and verification proofs.
   - [SECURITY_RED_TEAM_REPORT.md](file:///h:/Projects/VERITAS-600/SECURITY_RED_TEAM_REPORT.md) — Original red-team attack vectors and verification logs.
   - [AUDIT_CORRECTNESS_REPORT.md](file:///h:/Projects/VERITAS-600/AUDIT_CORRECTNESS_REPORT.md) — Phase 10 correctness verification.
2. **Verification Baseline:**
   - Backend: `pytest apps/api/tests/ -v` (58/58 tests passing in ~5.5s).
   - Code Style: `ruff check apps/api` (0 errors, 100% clean).
   - Frontend: `cd apps/web && npm run build` (Next.js 15.5.28 clean build, static page generation 6/6).
3. **Repository State:** All changes merged and verified on `main`. Zero breaking changes to the 5 architectural invariants.

---

## 📋 Comprehensive Phase Roadmap & Task Checklist

### Phase 0: Repository Foundation & Standards ✅ [COMPLETED & VERIFIED]
- [x] Initialize Git repository (`main` branch) and configure remote `https://github.com/sakibul-shovon/VERITAS-600.git`.
- [x] Relocate and structure master architecture in [docs/plan.md](file:///h:/Projects/VERITAS-600/docs/plan.md) and [doc/plan.md](file:///h:/Projects/VERITAS-600/doc/plan.md).
- [x] Create comprehensive `.gitignore`, `.env.example`, and `LICENSE` (Apache-2.0).
- [x] Create [AGENTS.md](file:///h:/Projects/VERITAS-600/AGENTS.md) and [.cursorrules](file:///h:/Projects/VERITAS-600/.cursorrules) defining domain boundaries & agent handoff protocols.
- [x] Configure automated CI workflow in [.github/workflows/ci.yml](file:///h:/Projects/VERITAS-600/.github/workflows/ci.yml) and PR template.
- [x] Create master [README.md](file:///h:/Projects/VERITAS-600/README.md) with architecture diagram, sponsor badges, and quickstart instructions.
- [x] Setup Python 3.11 environment via `uv`, configure `.venv`, and install all 56 backend dependencies.
- [x] Configure application settings in [apps/api/config.py](file:///h:/Projects/VERITAS-600/apps/api/config.py) (Pydantic v2).
- [x] Create lightweight [docker-compose.yml](file:///h:/Projects/VERITAS-600/docker-compose.yml) (PostgreSQL 16 + Redis 7).
- [x] Push clean initialization to GitHub `origin/main`.

---

### Phase 1: Sponsor Preflight, Data Seeding & Join-Safe Zetaris Federation ✅ [COMPLETED & VERIFIED]
- [x] Create `docker-compose.yml` (Postgres 16 on port 5432, Redis 7 on port 6379).
- [x] Create `apps/api/` FastAPI project skeleton (`requirements.txt`, `config.py`, `pyproject.toml`).
- [x] Implement `apps/api/db/schema.sql` (Tables: `lc_master`, `lc_amendments`, `examination_audit_log`).
- [x] Write `apps/api/zetaris/sql/federated_check.sql` with CTE pre-aggregation.
- [x] Create synthetic benchmark dataset `data/customs_parquet/hs_benchmarks.parquet` (HS-8481.80, HS-8501.10, HS-5205.12).
- [x] Create watchlist dataset `data/opensanctions/watchlist_entities.json` (Sanctioned vessels, parent companies).
- [x] Implement `apps/api/db/seed_scenarios.py` with the 3 Golden Scenarios + 7 eval cases.
- [x] Implement `apps/api/zetaris/client.py` (Zetaris API client + DuckDB local standby).
- [x] **Verification Gate 1:** `pytest apps/api/tests/test_zetaris_sql.py` passes (guarantees exactly 1 row per LC, execution < 1.5s).

---

### Phase 2: Stateful Amendment Memory & Deterministic UCP 600 Engine ✅ [COMPLETED & VERIFIED]
- [x] Implement `apps/api/memory/amendment_memory.py`:
  - Parses MT700 base terms and MT707 amendments.
  - Enforces **UCP 600 Art. 10(c) & 10(e)** state transitions:
    - Merges `ACCEPTED` amendments into active baseline with SHA-256 audit fingerprint.
    - Quarantines `UNACCEPTED_PENDING` amendments.
    - Blocks prohibited partial acceptance under Art. 10(e).
    - Recognizes full implicit acceptance via documents under Art. 10(c).
- [x] Implement `apps/api/engines/ucp600_deterministic.py`:
  - Temporal: Expiry date (**Art. 6(d)(i)**), 21-day presentation window (**Art. 14(c)**), effective shipment date (**Art. 20(a)(ii)**).
  - Financial: Invoice amount $\le$ Credit limit (**Art. 18(b)**), unit price math consistency.
  - Insurance: Reject Cover Notes (**Art. 28(c)**), Effective date $\le$ Shipment date (**Art. 28(e)**), Minimum $110\%$ coverage of CIF/CIP (**Art. 28(f)(ii)**) with exact shortfall calculation ($9,600 shortfall on LC-2026-9104).
  - Reconciliation: Gross weight cross-checks between Packing List and Bill of Lading (**Art. 14(d)**).
  - Demurrage Advisory: Calculates quantifiable demurrage savings ($11,100 saved on LC-2026-9104) for 48h re-presentation.
- [x] **Verification Gate 2:** `pytest apps/api/tests/test_deterministic.py` and `test_amendment_memory.py` pass 100%.

---

### Phase 3: Meterless Integration, Nemotron Extraction & Legal Adjudicator ✅ [COMPLETED & VERIFIED]
- [x] Implement `apps/api/inference/meterless_router.py`:
  - Context routing across 6 Markovian stages, token telemetry tracking, ~86% token savings estimation.
- [x] Implement `apps/api/inference/nim_client.py`:
  - Connect to NVIDIA NIM (`https://integrate.api.nvidia.com/v1`), 25 RPM token bucket rate limiter, SHA-256 response cache with fallback toggle.
- [x] Implement `apps/api/engines/document_extractor.py`:
  - Multimodal VLM field extraction with spatial bounding boxes [ymin, xmin, ymax, xmax] for Commercial Invoice, Ocean B/L, Packing List, and Insurance Certificate.
- [x] Implement `apps/api/engines/ucp600_legal_adjudicator.py`:
  - Resolves harmless typographical errors under **ISBP 745 Para A23** (`"Mashine"` protected).
  - Resolves general non-conflicting goods descriptions on B/L under **UCP 600 Art. 14(e)** (`"Servo Motors"` protected).
  - Catches address mutations in transport document Consignee/Notify box under **UCP 600 Art. 14(j)**.
  - Strictly enforces the **Hard Invariant Rule** in code (deterministic failure blocks compliant verdict).
- [x] **Verification Gate 3:** `pytest apps/api/tests/test_legal_adjudicator.py` passes 100%.

---

### Phase 4: Bank Decision Engine, SWIFT MT734 & AML Generator + SSE API ✅ [COMPLETED & VERIFIED]
- [x] Implement `apps/api/engines/decision_engine.py`:
  - Action 1: `APPROVE_HONOUR` (clean or protected).
  - Action 2: `ISSUE_MT734_REFUSAL` (discrepancy found, includes demurrage savings re-presentation advisory).
  - Action 3: `COMPLIANCE_HOLD_AML` (regulatory freeze due to TBML price anomaly or watchlist match).
- [x] Implement `apps/api/engines/artifact_generator.py`:
  - Generates raw SWIFT MT734 Refusal notice with fields `:20:`, `:21:`, `:32A:`, `:77J:`, `:77B:` `HOLD`.
  - Generates Financial Crime / AML Escalation Dossier.
  - Generates Settlement Authorization Voucher.
- [x] Implement `apps/api/main.py`:
  - `GET /api/v1/health` (Sponsor health & telemetry).
  - `GET /api/v1/scenarios` (Scenario discovery list).
  - `POST /api/v1/examine/{lc_id}` (Real-time SSE step streaming across 5 pipeline stages).
  - `POST /api/v1/examine/{lc_id}/approve-action` (Human examiner digital sign-off).
- [x] **Verification Gate 4:** `pytest apps/api/tests/test_end_to_end.py` passes 100%.

---

### Phase 5: High-Craft 3-Pane Bank Examiner Terminal (Next.js) ✅ [COMPLETED & VERIFIED]
- [x] Set up `apps/web/` using Next.js 15 (App Router, Tailwind CSS, Lucide React, JetBrains Mono).
- [x] Implement `HeaderBar.tsx`:
  - Scenario switcher, 5-banking-day preclusion clock, 21-day presentation window indicator, sponsor telemetry badges (`LIVE` vs `FALLBACK`).
- [x] Implement `DocumentViewerPane.tsx` (Left Pane):
  - Document tabs (MT700, Invoice, B/L, Packing List, Insurance Cert), live OCR button, interactive bounding boxes.
- [x] Implement `AdjudicationMatrixPane.tsx` (Center Pane):
  - Live execution stream, deterministic vs neural check badges, expandable Amendment Memory timeline, expandable Zetaris SQL Drawer.
- [x] Implement `DecisionActionPane.tsx` (Right Pane):
  - Bank examiner verdict card, generated MT734 or AML Dossier preview, interactive **Human Examiner Sign-Off** button.
- [x] Implement `/evals` page (`apps/web/src/app/evals/page.tsx`) with empirical 3-baseline benchmark dashboard and scenario comparison.
- [x] **Verification Gate 5:** Next.js production build (`npm run build`) succeeded with 0 errors, prerendering all terminal and evaluation routes.

---

### Phase 6: Empirical Baseline Comparison Suite & Final Polish ✅ [COMPLETED & VERIFIED]
- [x] Implement `apps/api/evals/compare_baselines.py`:
  - Evaluates 10 test cases across 3 real pipelines:
    1. Strict Deterministic / Regex Baseline (40.0% accuracy, 30% wrongful dishonor).
    2. Single-Prompt LLM (Nemotron) Baseline (40.0% accuracy, 10% hallucinatory flattery, 100% silo blindness).
    3. VERITAS-600 Neuro-symbolic synthesis (100.0% accuracy, 0% wrongful dishonor, 0% regulatory leakage).
- [x] Implement REST endpoints `POST /api/v1/evals/run` and `GET /api/v1/evals/results` in `apps/api/main.py`.
- [x] Implement `/evals` page on frontend displaying empirical accuracy, latency, and false positive rates.
- [x] Create automated evaluation test suite `apps/api/tests/test_evals_baseline.py` (5/5 tests passing).
- [x] Complete backend test suite passes: 27/27 tests green in 2.92s.
- [x] Production Next.js build passes with 0 errors (`npm run build`).

---

### Phase 7: World-Class Elevation & Demo Integrity ✅ [COMPLETED & VERIFIED]
- [x] Complete evidence-backed Track 03, sponsor, architecture, reasoning, UX, and implementation audit in `HACKATHON_ARCHITECTURE_ELEVATION.md`.
- [x] **P0:** Repair browser SSE method mismatch: enabled both GET and POST routes on `/api/v1/examine/{lc_id}`.
- [x] **P0:** Replace scenario-keyed extraction with input-derived, schema-validated evidence with spatial bounding boxes.
- [x] **P0:** Expose observed per-run execution telemetry (`LIVE_NEMOTRON_VLM`, `CACHED_REPLAY`, `STRUCTURED_FIXTURE`).
- [x] **P0:** Integrate Meterless Markovian 6-chunk context manifest and measured token savings telemetry.
- [x] **P0:** Replace scripted baseline outcomes and synthetic latency with actual dynamic field-evaluating baseline algorithms.
- [x] **P0:** Persist examination runs in memory store and bind authenticated approval to immutable decision and Merkle hashes.
- [x] **P1:** Add typed domain models (`Money`, `BoundingBox`, `EvidenceRecord`, `DecisionReceipt`) and audit cryptography (`canonical_json`, `merkle`, `hash_chain`, `verifier`).
- [x] **P2:** Expand legal rule coverage with 19 official rules in `apps/api/rulepacks/ucp600_rules.py`.
- [x] **P3:** Harden live federation with structured `federation_receipt` in `ZetarisFederationClient` and `/api/v1/evidence/sponsors/{lc_id}` endpoint.
- [x] **P4:** Implement cryptographic receipt seal (`V600-SIG-...`) and Merkle root visualization in `DecisionActionPane.tsx`.
- [x] **P5:** Full test suite passes 33/33 tests; Next.js 15 production build passes with 0 errors. Detailed report in `docs/PHASE_7_ELEVATION_REPORT.md`.

---

### Phase 8: Evidence Ledger UI/UX Redesign

- [x] **Planning:** Complete repository-grounded, contemporary UI/UX research and the 30-section implementation blueprint in [ui-redesign.md](file:///h:/Projects/VERITAS-600/ui-redesign.md).
- [x] **Landing planning:** Add the dedicated `LANDING PAGE — CREATIVE DIRECTION & IMPLEMENTATION BLUEPRINT` chapter with 20 implementation-grade subsections, three creative concepts, three hero concepts, a predefined case demonstration, responsive/motion specifications, and route migration gates.
- [x] **Landing MVP (current request):** Move the existing terminal from `/` to `/examine`; implement the light-first Evidence Ledger landing at `/` with responsive navigation, dark toggle, predefined LC-2026-9104 evidence gate, hard-invariant demonstration, guided five-stage walkthrough, architecture/outcomes/proof/benchmark narrative, terminal handoff, and purpose-built CSS motion.
- [x] **Landing verification:** `npm run build` succeeds on Next.js 15.5.28; `/` is 6.49 kB / 115 kB first load after motion polish and `/examine` preserves the terminal at 11.5 kB / 120 kB first load.
- [x] **Benchmark MVP (current request):** Redesign `/evals` as an interactive Evidence Ledger casebook with architecture lanes, selectable case evidence, a theme toggle, transparent fresh-versus-bundled provenance, and the existing benchmark API action preserved.
- [x] **Benchmark verification:** `npm run build` succeeds on Next.js 15.5.28; `/evals` is 4.03 kB / 112 kB first load after the casebook redesign.
- [x] **Workbench visual MVP (current request):** Restyle `/examine` as an active Evidence Ledger workbench with pane choreography, live audit pulse, responsive layout, and motion-safe interaction feedback while preserving the existing API/SSE examination flow and mandatory human sign-off.
- [x] **Workbench verification:** `npm run build` succeeds on Next.js 15.5.28; `/examine` is 11.8 kB / 120 kB first load after the visual-motion redesign.
- [x] **Full visual design pass (current request):** Complete a consistent Evidence Ledger visual system across all three routes, including responsive visual hierarchy, interactive state feedback, reduced-motion-safe choreography, explicit benchmark provenance, workbench active-case context, and visible keyboard focus states without changing decision authority or API contracts.
- [x] **Full visual verification:** `npm run build` succeeds on Next.js 15.5.28; local `/`, `/evals`, and `/examine` all return HTTP 200 after a clean dev-server restart.
- [x] **Core resilience implementation (current request):** Add a reducer-owned examination lifecycle with stale-stream cancellation, completed-evidence preservation on interruption, visible API/recovery notices, dynamic API-backed case selection, approval validation/error preservation, route error/loading states, a skip link, and responsive workbench scrolling.
- [x] **Resilience verification:** Full backend suite passes 33/33; Next.js 15.5.28 production build succeeds and local `/`, `/evals`, and `/examine` all return HTTP 200.
- [x] **Agentic workbench redesign:** Replace the dark terminal visual language with the landing-aligned light Evidence Ledger palette and expose the real five-owner orchestration (`Meterless / Memory → Zetaris → Python → Nemotron → Policy / Human`) with SSE-driven pending, active, and completed handoff states; rename the core regions to Evidence Folio, Agentic Decision Trace, and Decision Docket & Human Gate.
- [x] **Agentic workbench verification:** Next.js 15.5.28 production build succeeds; `/examine` remains below the 150 kB route budget at 122 kB first load.
- [x] **Federation proof inspector redesign:** Replace the legacy full-width dark SQL overlay with a landing-aligned light right-side evidence drawer, honest observed runtime/source telemetry, compact three-silo provenance, a visible join-safe invariant, collapsible SQL, Escape/backdrop dismissal, focus restoration, and responsive/reduced-motion behavior.
- [x] **Federation proof verification:** Next.js 15.5.28 production build succeeds; `/examine` remains at 122 kB first load with the accessible proof drawer included.
- [x] **A+C hybrid Mission Control redesign:** Replace the single-page three-pane composition with seven explicit clickable workspaces (Overview, Evidence Room, Agent Run, Rule Analysis, Federation, Decision Studio, Audit Receipt), a persistent application navigation rail, and a dominant run command while preserving the existing API/SSE lifecycle.
- [x] **Agentic knowledge graph and motion:** Add SSE-state-driven five-agent nodes, animated evidence packets, active-stage orbit/pulse feedback, structured event ledger, backend-computed calculation cards, three-silo federation map, immutable hard-invariant lock, and cryptographic audit-seal transition with reduced-motion parity.
- [x] **A+C responsive verification:** Next.js 15.5.28 production build succeeds with `/examine` at 128 kB first-load JS (below the 150 kB budget); desktop 1440×1000 and mobile 390×844 visual QA completed.
- [x] **Planning verification:** Confirm the blueprint preserves all routes/API contracts, the five architectural invariants, all three decisions, honest telemetry, and explicit human sign-off.
- [x] **Regression baseline:** Backend suite passes 33/33 tests; Next.js 15.5.28 production build succeeds before redesign implementation.
- [x] **Phase 8A — Contract lock and characterization:** Preserved all 8 FastAPI endpoints, verified SSE stream lifecycle, and locked regression baseline (33/33 pytest passing).
- [x] **Phase 8B — Route safety and foundations:** Preserved terminal at `/examine`, established Evidence Ledger design tokens, Georgia editorial serif headings, JetBrains Mono telemetry, and high-contrast dark theme toggle.
- [x] **Phase 8C — Landing product story:** Server-rendered Evidence Ledger product story at `/` with interactive Evidence Gate, hard invariant live demonstration, and 5-stage agentic orchestration.
- [x] **Phase 8D — State and data:** Reducer-driven SSE stream management in `examination-reducer.ts`, graceful error recovery with `NoticeRegion`, and honest telemetry modes.
- [x] **Phase 8E — Examination vertical slice:** Three golden scenarios verified end-to-end with spatial bounding boxes `[ymin, xmin, ymax, xmax]`, UCP 600 citations, and Merkle-sealed human authorization.
- [x] **Phase 8F — Benchmark route:** Interactive Casebook at `/evals` with architecture comparison lanes and fresh-versus-bundled dataset provenance.
- [x] **Phase 8G — Motion and performance:** Restrained 120ms-420ms CSS keyframe motion with strict `prefers-reduced-motion` compliance. Next.js 15 production build clean (all routes < 125 kB first-load JS).
- [x] **Phase 8H — Verification & Git branch:** Created and switched to `feat/ui-redesign`, backend tests 33/33 green in 2.66s, Next.js build passes cleanly with 0 errors.

---

### Phase 9: Real Examiner Intake, OCR Truthfulness & Explainable UX ✅ [COMPLETED & VERIFIED]

- [x] Replace the preselected sample-first experience with a clean start screen offering a primary real-case flow and a separately labelled sample sandbox.
- [x] Add durable user-created cases and real multipart PDF/PNG/JPEG/WebP evidence storage under ignored runtime data.
- [x] Parse text-layer PDFs directly; render scanned PDFs through PyMuPDF or PDFium and route scans/images to NVIDIA vision when credentials are configured.
- [x] Never substitute fixture evidence for failed OCR; expose `PDF_TEXT_LAYER`, `LIVE_NEMOTRON_VLM`, `CACHED_REPLAY`, or `OCR_UNAVAILABLE` truthfully.
- [x] Add editable extraction review, required-document completeness, examiner acceptance, evidence versioning, source SHA-256 digests, and examination gating.
- [x] Feed accepted PDF values into the real presentation object and enable new LC IDs in the join-safe local three-silo federation through a non-mutating runtime master overlay.
- [x] Remove fake countdown/token-savings UI, expose observed stage duration and routing inputs, explain extraction confidence and TBML Z-score thresholds, and show deterministic calculation details.
- [x] Add persistent light/dark mode, larger readable controls, explicit clickable states, four-step examiner guidance, responsive layout, and mobile overflow hardening.
- [x] Bind human authorization to the exact run ID, decision digest, and expected action; explicitly report `AUTHORIZED_NOT_DISPATCHED` because external dispatch is not connected.
- [x] **Real-PDF verification:** generated and uploaded four actual PDF documents; extracted/persisted invoice `$240,000`, insurance `$264,000`, shipment `2026-11-12`, and weight `12,500`; downstream deterministic coverage computed `110.0%`.
- [x] **Regression verification:** backend suite 38/38 passes; Next.js 15.5.28 production build succeeds with `/examine` at 134 kB first-load JS.

---

### Phase 10: Codebase Correctness & Telemetry Hardening Audit ✅ [COMPLETED & VERIFIED]

- [x] **P0 Correctness:** Fixed Zetaris SQL cross-LC CTE pollution by adding `AND lc_id = :lc_id` in `federated_check.sql`.
- [x] **P0 Correctness:** Implemented robust multi-format trade date parser (`%Y-%m-%d`, `%d/%m/%Y`, `%m/%d/%Y`, `%d-%m-%Y`, `%d.%m.%Y`, ISO 8601) in `ucp600_deterministic.py`.
- [x] **P0 Correctness:** Handled empty/null B/L on-board date safely under **UCP 600 Art. 20(a)(ii)** without raising unhandled 500 exceptions.
- [x] **P0 Correctness:** Corrected minimum insurance calculation basis under **UCP 600 Art. 28(f)(ii)** to `invoice_amount if invoice_amount > 0 else lc_amount` (eliminating false penalties when invoice < credit).
- [x] **P0 Correctness:** Aligned insurance date evaluation under **UCP 600 Art. 28(e)** to prioritize `insurance_effective_date` / `insurance_date` over issue date.
- [x] **P0 Correctness:** Fixed gross weight cross-reconciliation under **UCP 600 Art. 14(d)** (requires weight > 0, permits 0.1% / 0.5kg commercial rounding tolerance).
- [x] **P0 Correctness:** Dynamic presentation window demurrage savings advisory calculation replacing hardcoded text.
- [x] **P0 Correctness:** Added `_safe_parse_json` stripping markdown code blocks and recovering JSON objects from conversational model outputs in `ucp600_legal_adjudicator.py`.
- [x] **P0 Correctness:** Standardized TBML unit price anomaly threshold to `z_score >= 3.0` across all modules matching Wolfsberg standard deviation rules.
- [x] **P1 Telemetry:** Marked pre-signoff vouchers as `SETTLEMENT STATUS: PROPOSED - PENDING HUMAN EXAMINER AUTHORIZATION` and `DISPATCH STATUS: AWAITING SIGN-OFF (NOT DISPATCHED)`.
- [x] **P1 Telemetry:** Replaced misleading `EXECUTED` badges with honest `AUTHORIZED (NOT DISPATCHED)` / `AUTHORIZED_NOT_DISPATCHED`.
- [x] **P1 Telemetry:** Hardened `/api/v1/health` to dynamically report live vs DuckDB standby and Meterless key presence.
- [x] **P2 Security:** Removed wildcard CORS (`*` + credentials); restricted to explicit localhost origins.
- [x] **P2 Security:** Thread-safe `TokenBucketRateLimiter` using `threading.Lock()` in `nim_client.py`.
- [x] **P2 Security:** HMAC-SHA256 signature keying with `SETTINGS.ZTRV_HMAC_SECRET` in `DecisionReceipt` and `AuditVerifier`.
- [x] **P2 Security:** Added `record_approval` in `CaseStore` to durably persist examiner digital signatures on disk.
- [x] **P3 Reproducibility:** Added `seed_scenarios.py` step to `.github/workflows/ci.yml` before pytest execution.
- [x] **P3 Reproducibility:** Removed `|| echo` mask from `ruff check apps/api` in CI workflow.
- [x] **P3 Reproducibility:** Fixed all 331 ruff lint issues in `apps/api/` (0 errors remaining).
- [x] **P3 Testing:** Created dedicated test suite `apps/api/tests/test_audit_fixes.py` (8 new tests).
- [x] **Comprehensive Verification:** 46/46 pytest tests pass in 4.91s; `ruff check apps/api` 0 errors; Next.js 15 production build succeeds cleanly. Complete report in `AUDIT_CORRECTNESS_REPORT.md`.

---

### Phase 11: Adversarial Red-Team Audit & Security Remediation ✅ [COMPLETED & VERIFIED]

- [x] **Full-codebase comprehension pass** of engines, audit chain, stores, inference and Zetaris layers.
- [x] **Live PoC battery** (8 attacks verified against real modules + TestClient); evidence and re-run steps in `SECURITY_RED_TEAM_REPORT.md` §8.
- [x] **P0-1 Remediated:** Implemented `EXAMINER_API_KEY` verification, sign-off idempotence (duplicate approval returns 409), decision digest integrity, and evidence version binding in `main.py`.
- [x] **P0-2 Remediated:** Neural layer strictly fails closed (`INDETERMINATE`, `is_discrepancy=True`). Offline replay goods matching catches non-conforming goods under Art. 18(c). Removed blunt `"omitted"` false positive.
- [x] **P0-3 & P2-9 Remediated:** Constant-time receipt verification via `hmac.compare_digest` in `verifier.py` preventing timing side-channel attacks.
- [x] **P0-4 Remediated:** Prompt injection neutralized via `<UNTRUSTED_CONTENT>` fencing and strict legal citation whitelisting (`VALID_CITATIONS`) in `ucp600_legal_adjudicator.py`.
- [x] **P1-2 Remediated:** Converted `NvidiaNimClient._cache` to bounded `OrderedDict` LRU cache (`MAX_CACHE_ENTRIES = 512`), preventing unauthenticated memory exhaustion.
- [x] **P1-3 Remediated:** Added `Image.MAX_IMAGE_PIXELS = 25_000_000`, 50 PDF page extraction cap, and 500,000 char cap against decompression/pixel bombs in `document_extractor.py`.
- [x] **P1-4 & P1-5 & P1-6 Remediated:** Strict trade date parsing contract, mandatory checks enforced across partial presentations, and NFKC + homoglyph normalization catching Cyrillic `с` in `сover note` under Art. 28(c).
- [x] **P1-7 Remediated:** `CaseStore.accept_evidence` enforces strict numeric validation, rejecting complex dictionaries, negative amounts, `NaN`, and `Infinity` with 422/ValueError.
- [x] **P1-8 Remediated:** `ZetarisFederationClient` migrated from string replacement to DuckDB positional `?` parameter binding with graceful `FALLBACK_ERROR` handling.
- [x] **P2-3 Remediated:** Added `sanitize_swift_text` escaping SWIFT block delimiters (`{`, `}`) and tag injection in MT734 messages; asserted template status replacement in settlement vouchers.
- [x] **P2-6 & P2-8 & P2-11 Remediated:** Thread-safe `CaseStore` file locking with `threading.Lock()`; evaluation suite concurrency lock with `asyncio.Lock()`; per-case fault tolerance in scenarios listing.
- [x] **P2-7 Remediated:** Honest telemetry in `/health` and sponsor evidence endpoints rejecting placeholder keys (`your_zetaris_api_key_here`).
- [x] **P2-10 Remediated:** `AmendmentMemoryEngine` parses dates via `parse_date` and blocks partial acceptance with conflicts under Art. 10(e).
- [x] **Dedicated Regression Suite:** Created `apps/api/tests/test_security_redteam_fixes.py` with 12 new automated security tests (58/58 backend tests passing).
- [x] **Comprehensive Documentation:** Created [SECURITY_REMEDIATION_REPORT.md](file:///h:/Projects/VERITAS-600/SECURITY_REMEDIATION_REPORT.md) detailing all root causes and verification proofs.

---

## 🔒 Invariant Engineering Rules (Do Not Violate)

1. **The Hard Invariant Rule:** A neural LLM verdict can NEVER override a failed deterministic check. If math or dates fail, the status is permanently `DISCREPANT`.
2. **Exact Legal Citations:** Never invent or guess UCP articles. Use exact citations:
   - `Art. 28(f)(ii)` for 110% CIF/CIP insurance calculation.
   - `Art. 28(c)` for Cover Note prohibition.
   - `ISBP 745 Para A23` for harmless typographical errors.
   - `Art. 14(e)` for general B/L goods description.
   - `Art. 10(c) & 10(e)` for amendment state & partial acceptance prohibition.
   - `Art. 16(c)(iii)` for single Notice of Refusal disposal status.
3. **Join-Safe SQL Rule:** Always pre-aggregate amendments and watchlist hits into CTEs before joining `lc_master` to guarantee exactly 1 row per LC.
4. **Transparent Telemetry:** Always badge whether sponsor APIs are running on live cloud endpoints or local fallbacks. Never fake a live connection.
5. **Human-in-the-Loop:** Final bank actions require an explicit human officer sign-off before dispatch.

---

## 📝 Agent Protocol (Follow Every Turn)

1. **Before writing code:** Read `STATUS.md` and check the active task in "WHERE TO START NEXT".
2. **While writing code:** Follow directory conventions and invariant rules.
3. **After completing a task:**
   - Run relevant automated tests.
   - Mark the completed item as `[x]` in `STATUS.md`.
   - Update `Current Phase`, `Overall Progress`, and `WHERE TO START NEXT`.
   - Commit changes with descriptive messages: `git commit -m "feat(phase-X): <description>"`.
