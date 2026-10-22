# AGENTS.md: Operational Instructions for Coding Agents

> **Audience:** Cursor Agent, Claude Code, OpenAI Codex, Antigravity, and any automated AI coding assistant.
> **Repository:** VERITAS-600 (Lean Autonomous Trade Finance & UCP 600 Adjudication Engine)
> **Competition:** Open Agent Hackathon 2026 (GenAI.Works) — Track 03: Reasoning Architecture

---

## 1. Prime Directive & Ground Truth

1. **Check Status First:** At the beginning of every session, you MUST read [STATUS.md](file:///h:/Projects/VERITAS-600/STATUS.md). It tells you:
   - What phase is active.
   - What tasks are complete (`[x]`) vs. pending (`[ ]`).
   - The exact next task under **"WHERE TO START NEXT"**.
2. **Master Architecture:** The master architectural reference is [docs/plan.md](file:///h:/Projects/VERITAS-600/docs/plan.md). Never deviate from its design without explicit justification.
3. **Update Status Upon Completion:** When you finish a task, you MUST update [STATUS.md](file:///h:/Projects/VERITAS-600/STATUS.md) to reflect the new state, check off the item, and specify the next action.

---

## 2. Inviolable Architectural Invariants

You MUST adhere to these 5 invariant rules in every line of code you write:

1. **The Hard Invariant Rule (Neuro-Symbolic Split):**
   * *A neural LLM verdict can NEVER override a failed deterministic check.*
   * Python handles all math, dates, tolerances, and threshold validations.
   * If a deterministic check fails (e.g. insurance is 108% instead of 110%, or shipment date is past latest shipment date), the check status is locked to `DISCREPANT`. An LLM cannot mark it compliant.
   * LLMs are used *only* for semantic and lexical reasoning (e.g., judging typographical errors under ISBP 745 Para A23 or general goods descriptions under UCP 600 Art. 14(e)).
2. **Exact Legal Citations:**
   * Always cite the exact ICC UCP 600 or ISBP 745 article. Do not hallucinate or approximate citations.
   * Insurance $\ge 110\%$: **UCP 600 Art. 28(f)(ii)**.
   * Cover note prohibition: **UCP 600 Art. 28(c)**.
   * Typographical errors not altering meaning: **ISBP 745 Para A23**.
   * General goods description on non-invoice documents: **UCP 600 Art. 14(e)**.
   * Mandatory strict goods description on invoice: **UCP 600 Art. 18(c)**.
   * Mandatory strict applicant address in Consignee/Notify box of B/L: **UCP 600 Art. 14(j)**.
   * Amendment acceptance & partial acceptance prohibition: **UCP 600 Art. 10(c) & 10(e)**.
   * Single notice of refusal & document disposal: **UCP 600 Art. 16(c)(iii)**.
   * 5-banking-day examination clock: **UCP 600 Art. 14(b) & Art. 16(f)**.
3. **Join-Safe SQL Rule:**
   * In `apps/api/zetaris/sql/federated_check.sql`, never perform direct multi-table joins that cause Cartesian row multiplication. Always pre-aggregate amendments and watchlist hits into Common Table Expressions (CTEs) before joining `lc_master`. Exactly 1 row per `lc_id` must be returned.
4. **Honest Runtime Telemetry:**
   * Always expose ground-truth telemetry in API responses and UI badges:
     - Zetaris: `LIVE_ZETARIS` vs. `LOCAL_DUCKDB_FALLBACK`.
     - NVIDIA NIM: `LIVE_UNCACHED` vs. `CACHED_REPLAY`.
   * Never fake a cloud connection if running against local fallbacks.
5. **Human-in-the-Loop Sign-Off:**
   * Every final action (`APPROVE_HONOUR`, `ISSUE_MT734_REFUSAL`, `COMPLIANCE_HOLD_AML`) must be gated behind a human examiner sign-off step (`POST /api/v1/examine/{lc_id}/approve-action`).

---

## 3. Repository Structure

```text
veritas-600/
├── .cursorrules                  # Cursor IDE rules
├── AGENTS.md                     # This file (Agent instructions)
├── STATUS.md                     # Single source of truth for project state
├── README.md                     # Master hackathon presentation document
├── docker-compose.yml            # PostgreSQL 16 + Redis 7
├── .env.example                  # Environment configuration template
├── docs/                         # Master plans & domain documentation
│   └── plan.md                   # Complete architectural specification
├── doc/                          # Alias documentation directory
│   └── plan.md
│
├── apps/
│   ├── api/                      # FastAPI (Python 3.11+) Backend
│   │   ├── requirements.txt
│   │   ├── main.py               # Endpoints + SSE stream
│   │   ├── config.py             # Settings (Pydantic v2)
│   │   ├── db/
│   │   │   ├── schema.sql        # Database tables
│   │   │   └── seed_scenarios.py # Seed 3 golden scenarios + 7 evals
│   │   ├── zetaris/
│   │   │   ├── client.py         # Zetaris API + DuckDB fallback
│   │   │   └── sql/federated_check.sql # Join-safe CTE query
│   │   ├── memory/
│   │   │   └── amendment_memory.py # Art. 10 stateful resolver
│   │   ├── inference/
│   │   │   ├── meterless_router.py # Meterless routing & memory
│   │   │   └── nim_client.py     # NVIDIA NIM client + rate limiter
│   │   ├── engines/
│   │   │   ├── document_extractor.py    # VLM OCR extraction
│   │   │   ├── ucp600_deterministic.py  # Python math & date checks
│   │   │   ├── ucp600_legal_adjudicator.py # Nemotron legal judge
│   │   │   ├── decision_engine.py       # Honour vs MT734 vs AML Hold
│   │   │   └── artifact_generator.py    # SWIFT MT734 & AML Dossier
│   │   ├── evals/
│   │   │   └── compare_baselines.py     # 3-architecture evaluation
│   │   └── tests/
│   │       ├── test_zetaris_sql.py
│   │       ├── test_deterministic.py
│   │       ├── test_amendment_memory.py
│   │       └── test_end_to_end.py
│   │
│   └── web/                      # Next.js 15 (App Router, TypeScript, Tailwind)
│       ├── package.json
│       └── src/
│           ├── app/              # Terminal page & /evals page
│           ├── components/       # Header, DocumentViewer, Matrix, DecisionPane
│           └── lib/              # API clients & types
│
└── data/
    ├── presentations/            # Rendered docs + structured JSON
    ├── customs_parquet/          # HS-code benchmark distributions
    └── opensanctions/            # Watchlist entities & vessels
```

---

## 4. Verification & Testing Commands

Before marking any task as complete, run the corresponding verification command:

* **Zetaris SQL & Federation:**
  ```bash
  pytest apps/api/tests/test_zetaris_sql.py -v
  ```
* **Deterministic UCP 600 Math & Dates:**
  ```bash
  pytest apps/api/tests/test_deterministic.py -v
  ```
* **Stateful Amendment Memory (Art. 10):**
  ```bash
  pytest apps/api/tests/test_amendment_memory.py -v
  ```
* **Complete Backend Test Suite:**
  ```bash
  pytest apps/api/tests/ -v
  ```
* **Frontend Lint & Build:**
  ```bash
  cd apps/web && npm run build
  ```

---

## 5. Sponsor Integration Standards

1. **Zetaris:** Must demonstrate join across 3 distinct data silos (OLTP Postgres + Parquet Customs + OpenSanctions API) in a single query without ETL.
2. **Meterless:** Must implement context routing and stateful amendment memory using official SDK/gateway primitives.
3. **NVIDIA Nemotron:** Must use NIM endpoint (`https://integrate.api.nvidia.com/v1`) with rate limiting (25 RPM) and structured JSON outputs.
4. **Cursor:** Development environment adhering strictly to `.cursorrules`.

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

When the user types `/graphify`, use the installed graphify skill or instructions before doing anything else.

Rules:
- When graphify-out/graph.json exists, run `graphify query "<question>"` before your first grep, search or source-file read for a codebase question, and put this rule in every subagent prompt that explores code. Read raw files only for lines the graph or an earlier read already located. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- Dirty graphify-out/ files are expected after hooks or incremental updates; dirty graph files are not a reason to skip graphify. Only skip graphify if the task is about stale or incorrect graph output, or the user explicitly says not to use it.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
- A committed graphify-out/graph.json is rewritten whole on every build, so a large diff to it in a pull request is expected. Do not flag it as churn or suggest skipping the graph rebuild or its hooks.
