# VERITAS-600: Project Execution & Agent Continuity Tracker

> **Notice to All Coding Agents (Cursor, Claude Code, Codex, Antigravity, etc.):**
> This file is the **Single Source of Truth** for current project state.
> Whenever you start a session, **read this file first** to determine where to resume work.
> Whenever you complete a sub-task or phase, **update this file immediately** before ending your turn.

---

## 🚦 Current Project Status at a Glance

| Attribute | Current Value |
| :--- | :--- |
| **Current Phase** | **Phase 1: Sponsor Preflight, Data Seeding & Zetaris Federation** |
| **Overall Progress** | **20% Complete** (Phase 0 100% Complete & Verified, Phase 1 Underway) |
| **Active Task** | Generate `hs_benchmarks.parquet`, `watchlist_entities.json`, and `seed_scenarios.py` |
| **Last Updated** | 2026-10-22 |
| **Next Action Item** | **Seed Phase 1 data files and implement `apps/api/zetaris/client.py`** |

```
[████░░░░░░░░░░░░░░░░] 20% (Phase 0 Complete, Phase 1 Underway)
```

---

## 👉 WHERE TO START NEXT (For the Next Agent)

1. **Step 1:** Create `apps/api/db/seed_scenarios.py` to seed:
   - Data files: `data/customs_parquet/hs_benchmarks.parquet` and `data/opensanctions/watchlist_entities.json`.
   - The 3 Golden Scenarios (`LC-2026-8841`, `LC-2026-9104`, `LC-2026-9920`) and 7 eval cases into PostgreSQL/DuckDB.
2. **Step 2:** Implement `apps/api/zetaris/client.py` with dual-mode execution (`LIVE_ZETARIS` vs. `LOCAL_DUCKDB_FALLBACK`).
3. **Step 3:** Run Verification Gate 1: `.venv\Scripts\pytest.exe apps/api/tests/test_zetaris_sql.py -v`.

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

### Phase 1: Sponsor Preflight, Data Seeding & Join-Safe Zetaris Federation ⏳ [IN PROGRESS]
- [x] Create `docker-compose.yml` (Postgres 16 on port 5432, Redis 7 on port 6379).
- [x] Create `apps/api/` FastAPI project skeleton (`requirements.txt`, `config.py`).
- [x] Implement `apps/api/db/schema.sql` (Tables: `lc_master`, `lc_amendments`, `examination_audit_log`).
- [x] Write `apps/api/zetaris/sql/federated_check.sql` with CTE pre-aggregation.
- [ ] Create synthetic benchmark dataset `data/customs_parquet/hs_benchmarks.parquet` (HS-8481.80, HS-8501.10, HS-5205.12).
- [ ] Create watchlist dataset `data/opensanctions/watchlist_entities.json` (Sanctioned vessels, parent companies).
- [ ] Implement `apps/api/db/seed_scenarios.py` with the 3 Golden Scenarios + 7 eval cases.
- [ ] Implement `apps/api/zetaris/client.py` (Zetaris API client + DuckDB local standby).
- [ ] **Verification Gate 1:** `pytest apps/api/tests/test_zetaris_sql.py` passes (guarantees exactly 1 row per LC, execution < 1.5s).

---

### Phase 2: Stateful Amendment Memory & Deterministic UCP 600 Engine ⬜ [PENDING]
- [ ] Implement `apps/api/memory/amendment_memory.py`:
  - Parses MT700 base terms and MT707 amendments.
  - Enforces **UCP 600 Art. 10(c) & 10(e)** state transitions:
    - Merges `ACCEPTED` amendments into active baseline.
    - Quarantines `UNACCEPTED_PENDING` amendments; validates whether presentation implicitly accepts the whole amendment or adheres to pre-amendment terms.
    - Flags prohibited partial acceptance.
- [ ] Implement `apps/api/engines/ucp600_deterministic.py`:
  - Temporal: Expiry date (**Art. 6(d)(i)**), 21-day presentation window (**Art. 14(c)**), effective shipment date (**Art. 20(a)(ii)**).
  - Financial: Invoice amount $\le$ Credit limit (**Art. 18(b)**), $\pm 5\%$ quantity tolerance (**Art. 30(b)**).
  - Insurance: Reject Cover Notes (**Art. 28(c)**), Effective date $\le$ Shipment date (**Art. 28(e)**), Minimum $110\%$ coverage of CIF/CIP (**Art. 28(f)(ii)**).
  - Reconciliation: Gross/net weight matching between Invoice, B/L, and Packing List (**Art. 14(d)**).
- [ ] **Verification Gate 2:** `pytest apps/api/tests/test_deterministic.py` and `test_amendment_memory.py` pass 100%. Verify `LC-2026-9104` catches exact $9,600 insurance shortfall.

---

### Phase 3: Meterless Integration, Nemotron Extraction & Legal Adjudicator ⬜ [PENDING]
- [ ] Implement `apps/api/inference/meterless_router.py`:
  - Context routing, token usage telemetry, and stateful memory ledger.
- [ ] Implement `apps/api/inference/nim_client.py`:
  - Connect to NVIDIA NIM (`https://integrate.api.nvidia.com/v1`).
  - Dynamic model slug verification, 25 RPM token-bucket rate limiter, SHA-256 response cache.
- [ ] Implement `apps/api/engines/document_extractor.py`:
  - Live Nemotron VLM / OCR extraction from rendered invoice/BL images into structured JSON with bounding boxes.
- [ ] Implement `apps/api/engines/ucp600_legal_adjudicator.py`:
  - Adjudicates lexical differences using structured JSON schema.
  - Cites **ISBP 745 Para A23** for harmless typos.
  - Cites **UCP 600 Art. 14(e)** for general B/L descriptions.
  - Enforces **Hard Invariant Rule** (neural verdict never overrides a failed deterministic check).
- [ ] **Verification Gate 3:** Verify `"Mashine"` returns `COMPLIANT_PROTECTED` (A23) and `"Industrial Servo Motors"` on B/L returns `COMPLIANT_PROTECTED` (14(e)).

---

### Phase 4: Bank Decision Engine, SWIFT MT734 & AML Generator + SSE API ⬜ [PENDING]
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
