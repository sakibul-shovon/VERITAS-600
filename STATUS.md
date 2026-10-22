# VERITAS-600: Project Execution & Agent Continuity Tracker

> **Notice to All Coding Agents (Cursor, Claude Code, Codex, Antigravity, etc.):**
> This file is the **Single Source of Truth** for current project state.
> Whenever you start a session, **read this file first** to determine where to resume work.
> Whenever you complete a sub-task or phase, **update this file immediately** before ending your turn.

---

## 🚦 Current Project Status at a Glance

| Attribute | Current Value |
| :--- | :--- |
| **Current Phase** | **Phase 4: Bank Decision Engine, SWIFT MT734 & AML Generator + SSE API** |
| **Overall Progress** | **65% Complete** (Phases 0-3 Complete & Verified, Phase 4 Underway) |
| **Active Task** | Implement `decision_engine.py`, `artifact_generator.py`, and `apps/api/main.py` with SSE streaming |
| **Last Updated** | 2026-10-22 |
| **Next Action Item** | **Implement 3-action bank decision engine, SWIFT MT734 generator, and FastAPI endpoints** |

```
[█████████████░░░░░░░] 65% (Phases 0-3 Complete, Phase 4 Underway)
```

---

## 👉 WHERE TO START NEXT (For the Next Agent)

1. **Step 1:** Implement [apps/api/engines/decision_engine.py](file:///h:/Projects/VERITAS-600/apps/api/engines/decision_engine.py):
   - Action 1: `APPROVE_HONOUR` (clean or protected under ISBP A23 / Art. 14(e)).
   - Action 2: `ISSUE_MT734_REFUSAL` (discrepancy found, includes demurrage advisory).
   - Action 3: `COMPLIANCE_HOLD_AML` (TBML Z-score > 4.0 or sanctions hit, blocks settlement without invalid MT734).
2. **Step 2:** Implement [apps/api/engines/artifact_generator.py](file:///h:/Projects/VERITAS-600/apps/api/engines/artifact_generator.py):
   - SWIFT MT734 Refusal notice with fields `:20:`, `:21:`, `:32A:`, `:77J:`, `:77B:` `HOLD`.
   - Financial Crime Escalation Dossier (SAR/OFAC Hold).
3. **Step 3:** Implement [apps/api/main.py](file:///h:/Projects/VERITAS-600/apps/api/main.py):
   - `GET /api/v1/scenarios` (health + scenario details).
   - `POST /api/v1/examine/{lc_id}` (real-time SSE streaming across the 5 pipeline stages).
   - `POST /api/v1/examine/{lc_id}/approve-action` (human examiner digital sign-off).
   - `POST /api/v1/evals/run` (empirical 3-baseline benchmark).
4. **Step 4:** Run Verification Gate 4: `.venv\Scripts\pytest.exe apps/api/tests/test_end_to_end.py -v`.

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

### Phase 4: Bank Decision Engine, SWIFT MT734 & AML Generator + SSE API ⏳ [IN PROGRESS]
- [ ] Implement `apps/api/engines/decision_engine.py`:
  - Action 1: `APPROVE_HONOUR` (clean or protected).
  - Action 2: `ISSUE_MT734_REFUSAL` (discrepancy found, Sanctions = 0, includes demurrage savings re-presentation advisory).
  - Action 3: `COMPLIANCE_HOLD_AML` (regulatory freeze due to TBML price anomaly or watchlist match).
- [ ] Implement `apps/api/engines/artifact_generator.py`:
  - Generates raw SWIFT MT734 Refusal notice with fields `:20:`, `:21:`, `:32A:`, `:77J:`, `:77B:` `HOLD`.
  - Generates Financial Crime / AML Escalation Dossier.
- [ ] Implement `apps/api/main.py`:
  - `GET /api/v1/scenarios` (Scenario list & sponsor health).
  - `POST /api/v1/examine/{lc_id}` (Real-time SSE step streaming).
  - `POST /api/v1/examine/{lc_id}/approve-action` (Human examiner digital sign-off).
  - `POST /api/v1/evals/run` (Empirical evaluation runner).
- [ ] **Verification Gate 4:** End-to-end API test succeeds across all 3 flagship scenarios and logs human sign-off.

---

### Phase 5: High-Craft 3-Pane Bank Examiner Terminal (Next.js) ⬜ [PENDING]
- [ ] Set up `apps/web/` using Next.js 15 (App Router, Tailwind CSS, Lucide React, JetBrains Mono).
- [ ] Implement `HeaderBar.tsx`:
  - Scenario switcher, 5-banking-day preclusion clock, 21-day presentation window indicator, sponsor telemetry badges (`LIVE` vs `FALLBACK`).
- [ ] Implement `DocumentViewerPane.tsx` (Left Pane):
  - Document tabs (MT700, Invoice, B/L, Packing List, Insurance Cert), live OCR button, interactive bounding boxes.
- [ ] Implement `AdjudicationMatrixPane.tsx` (Center Pane):
  - Live execution stream, deterministic vs neural check badges, expandable Amendment Memory timeline, expandable Zetaris SQL Drawer.
- [ ] Implement `DecisionActionPane.tsx` (Right Pane):
  - Bank examiner verdict card, generated MT734 or AML Dossier preview, interactive **Human Examiner Sign-Off** button.
- [ ] **Verification Gate 5:** Web terminal runs on `http://localhost:3000` with fluid live SSE streaming and human sign-off interaction.

---

### Phase 6: Empirical Baseline Comparison Suite & Final Polish ⬜ [PENDING]
- [ ] Implement `apps/api/evals/compare_baselines.py`:
  - Evaluates 10 test cases across 3 real pipelines:
    1. Strict Deterministic / Regex Baseline.
    2. Single-Prompt LLM (Nemotron) Baseline with full rules in context.
    3. VERITAS-600 (Neuro-symbolic + Amendment Memory + Zetaris Federation).
- [ ] Build `/evals` page on frontend displaying empirical accuracy, latency, and false positive rates.
- [ ] Record demo walk-through video and verify all pre-submission checklist criteria.

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
