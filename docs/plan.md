# VERITAS-600: Lean Master Architecture & Engineering Execution Plan (v2 — Domain & SQL Hardened)

> **Target coding agents:** Cursor Agent, Claude Code, OpenAI Codex
> **Competition:** Open Agent Hackathon 2026 (GenAI.Works)
> **Primary track:** Track 03 — Reasoning Architecture ("turn data, knowledge, memory, and reasoning into reliable decisions and actions").
> **Target Persona:** **Examining Bank Trade Finance Officer** (specifically the Documentary Credit Examination & Trade Compliance Desk at an Issuing or Nominated Bank).
> **Engineering standard:** Production-grade reliability on a tightly scoped, deeply solved operational problem. Exact ICC UCP 600 / ISBP 745 legal citations, join-safe SQL federation, explicit live vs. fallback telemetry, deterministic math where math is required, and surgical LLM reasoning with human-in-the-loop sign-off.

**How to use this file:** Read it completely, then execute Section 7 phase by phase. Verify every phase with automated tests before moving to the next.

---

## 1. System Vision & Operational Problem

### 1.1 Target User & The High-Stakes Problem

**The User:** A Senior Documentary Credit Examiner at an Issuing Bank examining incoming export presentations under irrevocable Letters of Credit (SWIFT MT700) and amendments (MT707).

When a presentation (Commercial Invoice, Ocean Bill of Lading, Packing List, Insurance Policy/Certificate, Certificate of Origin) arrives at the bank's counter, the examiner is governed by **ICC UCP 600** and **ISBP 745**. They face three operational traps that neither rigid rule engines nor naive RAG/LLM pipelines handle reliably:

1. **The 5-Banking-Day Preclusion Cliff (UCP 600 Art. 14(b) & Art. 16):**
   - Under **Art. 14(b)**, the examining bank has a maximum of **5 banking days** following the day of presentation to determine whether a presentation is complying.
   - If the bank decides to refuse, it must issue a **single Notice of Refusal (SWIFT MT734)** under **Art. 16(c)** stating *all* discrepancies and the exact disposition of documents under **Art. 16(c)(iii)**.
   - Under **Art. 16(f)**, if the bank fails to act within 5 banking days or fails to state a valid discrepancy in that single notice, it is **legally precluded** from claiming the documents do not constitute a complying presentation ($100K–$10M+ balance-sheet exposure).

2. **The Wrongful Dishonor vs. Genuine Discrepancy Trap (UCP 600 Art. 14(d), 14(e), 14(j), Art. 18(c) & ISBP 745 Para A23):**
   - Naive regex/rule checks flag harmless typographical errors (e.g., `"Industrial AC Servo Mashine"` instead of `"Industrial AC Servo Machine"`). Under **ISBP 745 Para A23**, a misspelling or typing error that does not affect the meaning of the word or the sentence in which it occurs does *not* make a document discrepant. Refusing payment on this basis exposes the bank to **wrongful dishonor** litigation.
   - Under **UCP 600 Art. 14(e)**, in documents *other than* the commercial invoice, the description of the goods may be in general terms not conflicting with their description in the credit (e.g., `"Industrial Servo Motors"` on the Bill of Lading vs. the full model specification on the Commercial Invoice under **Art. 18(c)**).
   - Conversely, under **UCP 600 Art. 14(j)**, while addresses of the beneficiary and applicant need not be the same as those stated in the credit, when the applicant's address appears as part of the *Consignee* or *Notify Party* details on a transport document, it **must be the same as that stated in the credit**.

3. **Stateful Amendment Ambiguity (UCP 600 Art. 10(c) & 10(e)) & Cross-Silo Blindness:**
   - Under **Art. 10(c)**, the terms and conditions of the original credit remain in force for the beneficiary until the beneficiary communicates its acceptance of the amendment, or presents documents that comply with the credit and with the not-yet-accepted amendment. Under **Art. 10(e)**, partial acceptance of an amendment is not allowed and will be deemed a notification of rejection. Standard RAG dumps both original terms and unaccepted amendments into the context window, causing LLMs to enforce unaccepted terms.
   - Finally, documentary compliance is distinct from **Financial Crime / Sanctions / TBML compliance**. A presentation may be 100% compliant on its face under UCP 600 (Art. 4 & Art. 5 separate documents from goods/underlying fraud), yet exhibit severe **Trade-Based Money Laundering (TBML)** unit-price inflation or a sanctioned parent entity—requiring an immediate **Compliance Hold & AML Escalation** rather than a standard UCP 600 documentary refusal.

---

## 2. Mandatory Sponsor Stack (Transparent, Load-Bearing Integration)

Every sponsor integration solves a concrete bottleneck and exposes honest runtime telemetry (explicitly badging `LIVE ENDPOINT` vs. `LOCAL FALLBACK` so judges always see ground-truth execution).

### 2.1 Zetaris: In-Situ Federated Data Layer

**Architectural Role:** Executes a join-safe, single-query federation across three distinct data silos without ETL during every examination.

| Silo | Source Identifier | Purpose in Bank Examination |
| --- | --- | --- |
| **Silo 1 (Operational DB)** | `postgres_trade` (PostgreSQL) | Stores `lc_master` (SWIFT MT700 baseline terms), `lc_amendments` (MT707 history with acceptance state), and `examination_audit_log`. |
| **Silo 2 (Lakehouse / Parquet)** | `parquet_customs` (Parquet / CSV) | Stores 6-digit HS-code historical unit-price distributions (mean, std dev, 5th/95th percentiles) to compute real-time TBML price anomaly $Z$-scores. |
| **Silo 3 (Watchlist / API)** | `opensanctions_entities` (JSON / REST view) | Stores sanctioned vessels (IMO numbers), shippers, notify parties, and parent-subsidiary corporate links derived from OpenSanctions data. | **Implementation & Transparency Pattern:**
- Implements `ZetarisFederationClient` in `apps/api/zetaris/client.py` following the official `zetaris/getting-started` patterns (`ZETARIS_BASE_URL`, `ZETARIS_API_KEY`).
- Includes a local DuckDB + PostgreSQL standby mode for offline resilience, **explicitly surfaced in the UI Header and SQL Drawer** as either `[ZETARIS: LIVE CLOUD]` or `[ZETARIS: LOCAL DUCKDB FALLBACK]`.

### 2.2 Meterless: Context Routing, Stateful Memory & Inference Control

**Architectural Role:** Implements stateful amendment memory and routes tasks across inference tiers while tracking token usage and latency.

1. **Verify Official Meterless Primitives First:**
   - During Phase 1 preflight, inspect the official Meterless documentation/repo provided in HackOS (`METERLESS_BASE_URL`, `METERLESS_API_KEY`) and wire directly to the live Meterless gateway/SDK primitives.
2. **Stateful Amendment Memory & Conflict Resolver (`apps/api/memory/amendment_memory.py`):**
   - Decomposes MT700 base clauses and MT707 amendments into structured atomic state tuples `(field_key, value, source_doc, status, timestamp)`.
   - Applies **UCP 600 Art. 10(c) & 10(e)** state transition rules *before* LLM prompting:
     - `ACCEPTED` amendments supersede the baseline value and archive the old value in an immutable audit lineage.
     - `UNACCEPTED_PENDING` amendments are quarantined into a conditional evaluation branch so the model checks whether the presented documents implicitly accept the whole amendment or adhere to the unamended credit.

### 2.3 NVIDIA Nemotron: Multimodal Extraction & Legal Adjudication

**Architectural Role:** Executes vision/OCR field extraction on rendered shipping documents and performs UCP 600 / ISBP 745 legal semantic adjudication via NVIDIA NIM (`https://integrate.api.nvidia.com/v1`).

- **Configurable Model Slugs (verified dynamically against `/v1/models` on startup):**
  - `NEMOTRON_VISION_MODEL` (e.g., `nvidia/llama-3.2-nv-embedqa` / available Nemotron VL or VLM endpoint on NIM): Extracts structured fields and bounding boxes from at least one real rendered document image/PDF in the live pipeline (with pre-extracted structured JSON available for instant comparison).
  - `NEMOTRON_REASONING_MODEL` (default: `nvidia/llama-3.3-nemotron-super-49b-v1` or `nvidia/llama-3.1-nemotron-ultra-253b-v1`): Powers the **UCP 600 / ISBP 745 Legal Adjudicator**, resolving lexical discrepancies, evaluating Art. 14(e) vs. Art. 18(c) descriptions, and generating cited explanations.
  - `NEMOTRON_FAST_MODEL` (default: `nvidia/llama-3.1-nemotron-nano-8b-v1`): Performs fast field normalization.
- **Reliability Guardrails:** Built-in token-bucket rate limiter (25 RPM, safely below the 40 RPM NIM free tier limit) and an optional SHA-256 response cache with a UI toggle (`Live Uncached NIM Call` vs. `Cached Instant Replay`).

### 2.4 Cursor: AI-Native Development Workflow

**Architectural Role:** Primary development environment configured with `.cursorrules` and `AGENTS.md` enforcing strict separation between deterministic math engines and neural legal judgment.

---

## 3. Core Technical Differentiation (The 3 Pillars)

### Pillar 1: Strict Neuro-Symbolic Split (Hard Invariant Rule)

LLMs should never do calendar math or percentage tolerances; rule engines should never judge semantic typos. VERITAS-600 enforces a **Hard Invariant Rule**: *A neural LLM verdict can never override a failed deterministic check.*

1. **Deterministic Symbolic Engine (`ucp600_deterministic.py`):**
   - **Temporal checks:** Presentation date $\le$ Expiry date (**Art. 6(d)(i)**); Presentation date $\le$ Shipment date $+ 21\text{ calendar days}$ (**Art. 14(c)**); On-board date $\le$ Effective latest shipment date (**Art. 20(a)(ii)**); 5-banking-day examination clock (**Art. 14(b)**).
   - **Financial & quantity math:** Invoice amount $\le$ Available LC credit amount (**Art. 18(b)**); Currency identity check (**Art. 18(a)(iii)** & **Art. 28(f)(i)**); Quantity tolerance within $\pm 5\%$ where permitted (**Art. 30(b)**).
   - **Insurance coverage & document type (Art. 28(c), 28(e) & 28(f)(ii)):**
     - **Art. 28(c):** Rejects `Cover Notes` (must be an Insurance Policy or Insurance Certificate under an open cover).
     - **Art. 28(e):** $\text{InsuranceEffectiveDate} \le \text{ShipmentDate}$ (unless it explicitly states cover is effective from a date not later than the date of shipment).
     - **Art. 28(f)(ii):** Minimum insured amount must be at least $110\%$ of the CIF or CIP value of the goods (or, if CIF/CIP cannot be determined from the documents, $110\%$ of the greater of the amount for which honor/negotiation is requested or the gross value of the goods shown on the commercial invoice):
       $$\text{InsuredValue} \ge 1.10 \times \max(\text{CIF\_CIP\_Value},\ \text{RequestedDrawingAmount},\ \text{InvoiceGrossValue})$$
   - **Cross-document physical reconciliation (Art. 14(d)):** Net and gross weight consistency across Commercial Invoice, Packing List, and Bill of Lading (data in a document must not conflict with data in any other stipulated document).

2. **Neural Legal Adjudication Engine (`ucp600_legal_adjudicator.py`):**
   - Invoked *only* on semantic/lexical divergences between documents.
   - Evaluates whether a divergence is:
     - **Protected under ISBP 745 Para A23:** A misspelling or typing error that does not affect the meaning of the word or the sentence in which it occurs (e.g., `"Industrial AC Servo Mashine"`).
     - **Protected under UCP 600 Art. 14(e):** A general goods description on a non-invoice document (e.g., `"Industrial Servo Motors"` on the Bill of Lading vs. `"Industrial AC Servo Machine Model X-200"` on the Commercial Invoice) that does not conflict with the LC description.
     - **A Material Discrepancy under Art. 18(c) or Art. 14(j):** A conflicting or omitted specification on the Commercial Invoice (**Art. 18(c)**), or a mutated applicant address inside the Consignee/Notify Party box of a transport document (**Art. 14(j)**).

### Pillar 2: Stateful Amendment Memory (Art. 10(c) & 10(e) Quarantine)

Before running any check, `amendment_memory.py` builds an **Active Term Snapshot** and an **Audit Lineage Graph**:
- If Amendment #1 (`latest_shipment_date` extended from Oct 10 to Oct 18) is marked `ACCEPTED`, the active state updates to Oct 18.
- If Amendment #2 (`port_of_discharge` changed and `unit_price` reduced) is `UNACCEPTED_PENDING`, the memory engine evaluates whether the beneficiary's presented documents conform to *all* changes in Amendment #2 (implicit acceptance under Art. 10(c)) or adhere strictly to the pre-Amendment #2 state. Under **Art. 10(e)**, partial adherence to an amendment is flagged as a rejection/discrepancy.

### Pillar 3: Cross-Silo Risk & Bank-Officer Action Engine (With Human-in-the-Loop Gate)

1. **Zetaris Federated Risk Check:** Joins the active LC against `parquet_customs` to compute the HS-code unit price $Z$-score:
   $$Z = \frac{\text{InvoiceUnitPrice} - \mu_{\text{HS6}}}{\sigma_{\text{HS6}}}$$
   and checks all presentation parties and the carrying vessel IMO against `opensanctions_entities` (including parent company ownership).
2. **Bank-Officer Action Engine (`decision_engine.py`):**
   Produces one of three bank-side actions—always gated by a **"Human Examiner Approve & Sign"** button before finalizing:
   - **Action 1 — Honor / Approve Settlement:** All UCP 600 deterministic and neural checks pass, and Sanctions/TBML checks are clear (even if harmless ISBP 745 Para A23 typos exist).
   - **Action 2 — Issue MT734 Notice of Refusal with Cure/Waiver Advisory (Art. 16(c)(iii)(a) or (b)):** Documentary discrepancies exist (e.g., Art. 28(f)(ii) insurance at $108\%$ and Art. 14(d) weight conflict), Sanctions Risk $= 0$, and 11 days remain in the 21-day presentation window. The bank issues a formal SWIFT MT734 stating all discrepancies, holds the documents under **Art. 16(c)(iii)(a)/(b)**, and attaches a **Pre-Expiry Re-Presentation / Applicant Waiver Cost Comparison** showing that beneficiary re-presentation of corrected insurance/packing documents within 48 hours saves $\$11,100$ in port demurrage compared to a 6-day applicant waiver cycle.
   - **Action 3 — Compliance Hold & AML/Sanctions Escalation (Non-MT734 Freeze):** When documents comply on their face under UCP 600, but Zetaris detects a severe TBML price anomaly ($Z > 4.0$) or an OFAC/OpenSanctions parent-entity hit. Because sanctions/TBML are regulatory blocks rather than UCP 600 documentary discrepancies, the system **blocks settlement**, places a **Compliance Hold**, and generates a **Financial Crime Escalation Dossier (SAR/OFAC Hold)** rather than an invalid MT734 documentary refusal.

---

## 4. The 3 Flagship Golden Scenarios (Realistic, Deeply Verifiable Data)

Each scenario ships with a complete 5-document presentation packet (SWIFT MT700, MT707 Amendments, Commercial Invoice, Ocean Bill of Lading, Packing List, Insurance Policy/Certificate, Certificate of Origin) in both rendered visual format (with live OCR/Vision extraction support) and structured JSON.

| Scenario ID | Title | What Happens in the Documents | Why Baselines Fail | How VERITAS-600 Wins |
| --- | --- | --- | --- | --- |
| **`LC-2026-8841`** | **The Wrongful Dishonor Trap** ($240,000 Industrial Servo Machines) | 1) Commercial Invoice says `"Industrial AC Servo Mashine Model X200"` (harmless typo).<br>2) B/L says `"Industrial Servo Motors"` (general non-conflicting term).<br>3) Shipment is Oct 16 (violates Original LC Oct 10, complies with Accepted Amendment #1 Oct 18; adheres to original port/price, ignoring Unaccepted Amendment #2). | **Regex/Rule Baseline:** Rejects due to `"Mashine"` typo and B/L general description.<br>**Flat RAG Baseline:** Confused by Original Oct 10 vs. Unaccepted Amendment #2 and flags false discrepancy. | **COMPLIANT — APPROVE HONOUR:** Amendment Memory isolates Accepted Amendment #1 and confirms Unaccepted Amendment #2 is uninvoked per **Art. 10(c)**; Nemotron cites **ISBP 745 Para A23** for the typo and **UCP 600 Art. 14(e)** for the B/L description. Prevents wrongful dishonor. |
| **`LC-2026-9104`** | **The Curable Discrepancy & Demurrage Save** ($480,000 Cotton Yarn CIF) | 1) Insurance Certificate covers $\$518,400$ ($108\%$ of CIF value, violating **Art. 28(f)(ii)** $110\%$ minimum $= \$528,000$).<br>2) Packing List gross weight ($24,500\text{ kg}$) conflicts with B/L ($24,050\text{ kg}$) under **Art. 14(d)**.<br>3) 11 days remain in the **Art. 14(c)** 21-day presentation window. | **Pure LLM Baseline:** Misses the $108\%$ vs. $110\%$ arithmetic shortfall or cites the wrong UCP article (`28(c)` instead of `28(f)(ii)`). | **DISCREPANT — ISSUE MT734 + RE-PRESENTATION ADVISORY:** Deterministic engine catches the exact $\$9,600$ insurance shortfall under **Art. 28(f)(ii)** and $450\text{ kg}$ weight conflict under **Art. 14(d)**; generates the formal **SWIFT MT734** (`HOLD` disposition per **Art. 16(c)(iii)(a)**) and quantifies the $\$11,100$ demurrage savings if the beneficiary re-presents cured documents within the remaining 11-day window. |
| **`LC-2026-9920`** | **The Cross-Silo TBML & Sanctions Freeze** ($675,000 Precision Valves) | All dates, weights, insurance ($110\%$), and descriptions match the LC on their face. However, unit price is $\$450/\text{unit}$ (customs HS-8481.80 benchmark mean is $\$92/\text{unit}$) and the Notify Party's parent company is on an OpenSanctions watchlist. | **Document-Only Agent:** Marks the presentation 100% compliant and releases payment because it only inspects the PDFs and cannot query customs lakehouse or watchlist graphs. | **REGULATORY FREEZE — COMPLIANCE HOLD & AML ESCALATION:** Zetaris federated query exposes a $Z = +5.4$ TBML price anomaly across Silo 2 and a parent-entity sanctions match in Silo 3. Correctly distinguishes regulatory freeze from UCP 600 documentary refusal and generates an **AML/Sanctions Escalation Dossier**. | ---

## 5. Repository Structure

```text
veritas-600/
├── .cursorrules                  # Architectural rules & neuro-symbolic boundaries
├── AGENTS.md                     # Instructions for coding agents
├── README.md                     # Setup, architecture diagram, sponsor verification guide
├── docker-compose.yml            # PostgreSQL 16 + Redis 7 (lightweight)
├── .env.example                  # ZETARIS_*, METERLESS_*, NVIDIA_API_KEY, PG*, REDIS*
│
├── apps/
│   ├── api/                      # FastAPI (Python 3.11+) Backend
│   │   ├── requirements.txt
│   │   ├── main.py               # FastAPI endpoints + SSE real-time step streaming
│   │   ├── config.py             # Pydantic settings (configurable model slugs & keys)
│   │   ├── db/
│   │   │   ├── schema.sql        # PostgreSQL tables for LCs, amendments, audit logs
│   │   │   └── seed_scenarios.py # Seeds the 3 Golden Scenarios + 10-case eval suite
│   │   ├── zetaris/
│   │   │   ├── client.py         # Zetaris REST/JDBC client + explicit DuckDB fallback telemetry
│   │   │   └── sql/
│   │   │       └── federated_check.sql  # Join-safe 3-silo CTE query (1 row per LC)
│   │   ├── memory/
│   │   │   └── amendment_memory.py      # Art. 10(c)/(e) stateful amendment resolver & ledger
│   │   ├── inference/
│   │   │   ├── meterless_router.py      # Meterless API routing, memory hooks & token telemetry
│   │   │   └── nim_client.py            # NVIDIA Nemotron VLM/LLM client + 25 RPM limiter + cache toggle
│   │   ├── engines/
│   │   │   ├── document_extractor.py    # Live Nemotron VLM/OCR extraction on rendered invoice/B/L
│   │   │   ├── ucp600_deterministic.py  # Dates, tolerances, Art. 28(c)/(e)/(f)(ii) insurance, weights
│   │   │   ├── ucp600_legal_adjudicator.py # Nemotron ISBP A23 / Art. 14(e) / Art. 14(j) judge
│   │   │   ├── decision_engine.py       # Honour vs. MT734 Refusal vs. AML Compliance Hold
│   │   │   └── artifact_generator.py    # Generates SWIFT MT734 & AML/Sanctions Escalation Dossier
│   │   ├── evals/
│   │   │   └── compare_baselines.py     # Empirically runs Rule-Only vs. Prompted-LLM vs. VERITAS-600
│   │   └── tests/
│   │       ├── test_zetaris_sql.py
│   │       ├── test_deterministic.py
│   │       ├── test_amendment_memory.py
│   │       └── test_end_to_end.py
│   │
│   └── web/                      # Next.js (App Router, TypeScript, Tailwind, Lucide)
│       ├── package.json
│       └── src/
│           ├── app/
│           │   ├── layout.tsx
│           │   ├── page.tsx      # Main 3-Pane Bank Examiner Terminal
│           │   └── evals/page.tsx # Empirical 3-Baseline Comparison View
│           ├── components/
│           │   ├── HeaderBar.tsx           # 5-Day Preclusion Clock + Live/Fallback Sponsor Badges
│           │   ├── DocumentViewerPane.tsx  # Left Pane: Rendered docs + Live OCR button + Bounding Boxes
│           │   ├── AdjudicationMatrixPane.tsx # Center Pane: Step stream, Det vs. Neural badges
│           │   ├── ZetarisDrawer.tsx       # Expandable live SQL & 3-silo result inspector
│           │   └── DecisionActionPane.tsx  # Right Pane: MT734 / AML Hold preview + Human Sign-Off button
│           └── lib/
│               ├── api.ts
│               └── types.ts
│
└── data/
    ├── presentations/            # Rendered PNG/HTML/PDF + JSON for LC-2026-8841, 9104, 9920 + 7 eval cases
    ├── customs_parquet/          # hs_benchmarks.parquet (6-digit HS unit price stats)
    └── opensanctions/            # watchlist_entities.json (vessels & corporate parent links)
```

---

## 6. Database & Join-Safe Federated Query Specifications

### 6.1 PostgreSQL Schema (`apps/api/db/schema.sql`)

```sql
CREATE TABLE lc_master (
    lc_id VARCHAR(32) PRIMARY KEY,
    swift_mt700_raw TEXT NOT NULL,
    issuing_bank VARCHAR(128) NOT NULL,
    applicant_name VARCHAR(128) NOT NULL,
    applicant_address_strict VARCHAR(256) NOT NULL,
    beneficiary_name VARCHAR(128) NOT NULL,
    currency VARCHAR(8) NOT NULL DEFAULT 'USD',
    amount NUMERIC(15, 2) NOT NULL,
    tolerance_pct NUMERIC(5, 2) NOT NULL DEFAULT 0.00,
    incoterm VARCHAR(16) NOT NULL,
    hs_code_6 VARCHAR(10) NOT NULL,
    goods_description_strict TEXT NOT NULL,
    unit_price NUMERIC(12, 2) NOT NULL,
    quantity INTEGER NOT NULL,
    port_of_loading VARCHAR(128) NOT NULL,
    port_of_discharge VARCHAR(128) NOT NULL,
    latest_shipment_date DATE NOT NULL,
    expiry_date DATE NOT NULL,
    presentation_period_days INTEGER NOT NULL DEFAULT 21,
    insurance_min_pct NUMERIC(6, 2) NOT NULL DEFAULT 110.00, -- UCP 600 Art. 28(f)(ii)
    daily_demurrage_usd NUMERIC(10, 2) NOT NULL DEFAULT 1850.00
);

CREATE TABLE lc_amendments (
    amendment_id VARCHAR(32) PRIMARY KEY,
    lc_id VARCHAR(32) REFERENCES lc_master(lc_id),
    sequence_no INTEGER NOT NULL,
    amended_field VARCHAR(64) NOT NULL,
    old_value TEXT NOT NULL,
    new_value TEXT NOT NULL,
    beneficiary_acceptance_status VARCHAR(24) NOT NULL CHECK (
        beneficiary_acceptance_status IN ('ACCEPTED', 'REJECTED', 'UNACCEPTED_PENDING')
    ),
    effective_date DATE NOT NULL
);

CREATE TABLE examination_audit_log (
    run_id VARCHAR(64) PRIMARY KEY,
    lc_id VARCHAR(32) NOT NULL,
    executed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    active_terms_sha256 VARCHAR(64) NOT NULL,
    zetaris_execution_mode VARCHAR(32) NOT NULL, -- 'LIVE_ZETARIS' or 'LOCAL_DUCKDB_FALLBACK'
    zetaris_query_ms INTEGER NOT NULL,
    deterministic_result JSONB NOT NULL,
    neural_adjudication_result JSONB NOT NULL,
    recommended_action VARCHAR(48) NOT NULL,     -- 'APPROVE_HONOUR', 'ISSUE_MT734_REFUSAL', 'COMPLIANCE_HOLD_AML'
    human_approved_by VARCHAR(128) NULL,
    human_approved_at TIMESTAMPTZ NULL,
    generated_artifact_text TEXT NULL
);
```

### 6.2 Join-Safe Zetaris 3-Silo Federated Query (`apps/api/zetaris/sql/federated_check.sql`)

To prevent row multiplication when an LC has multiple amendments or multiple watchlist matches, amendments and sanctions hits are pre-aggregated in CTEs before joining to `lc_master`. This guarantees **exactly 1 row per `lc_id`**.

```sql
WITH accepted_shipment_amd AS (
    SELECT
        lc_id,
        new_value AS effective_shipment_date
    FROM postgres_trade.lc_amendments
    WHERE amended_field = 'latest_shipment_date'
      AND beneficiary_acceptance_status = 'ACCEPTED'
    ORDER BY sequence_no DESC
    LIMIT 1
),
unaccepted_amendments_agg AS (
    SELECT
        lc_id,
        COUNT(*) AS quarantined_count,
        STRING_AGG(amended_field || '=' || new_value, '; ') AS quarantined_amendments_summary
    FROM postgres_trade.lc_amendments
    WHERE beneficiary_acceptance_status = 'UNACCEPTED_PENDING'
    GROUP BY lc_id
),
sanctions_hits_agg AS (
    SELECT
        COUNT(*) AS hit_count,
        MAX(risk_score) AS max_risk_score,
        STRING_AGG(
            matched_name || ' (Parent: ' || COALESCE(parent_company_name, 'N/A') || ' | ' || sanction_program || ')',
            '; '
        ) AS sanctions_summary
    FROM opensanctions_entities.watchlist
    WHERE lookup_name IN (:beneficiary_name, :vessel_name, :notify_party_name)
)
SELECT
    lc.lc_id,
    lc.applicant_name,
    lc.beneficiary_name,
    lc.amount AS lc_amount,
    lc.unit_price AS lc_unit_price,
    lc.latest_shipment_date AS original_shipment_date,
    COALESCE(amd_acc.effective_shipment_date, CAST(lc.latest_shipment_date AS VARCHAR)) AS effective_shipment_date,
    COALESCE(amd_unacc.quarantined_count, 0) AS quarantined_amendment_count,
    amd_unacc.quarantined_amendments_summary,
    -- Silo 2: Parquet Customs HS-Code Unit Price Benchmark
    cust.hs_code_6,
    cust.description AS hs_description,
    cust.mean_unit_price_usd,
    cust.stddev_unit_price_usd,
    ROUND((:invoice_unit_price - cust.mean_unit_price_usd) / NULLIF(cust.stddev_unit_price_usd, 0), 2) AS tbml_price_zscore,
    -- Silo 3: Aggregated OpenSanctions Watchlist Hits
    COALESCE(sanc.hit_count, 0) AS sanction_hit_count,
    COALESCE(sanc.max_risk_score, 0.0) AS sanction_max_risk_score,
    sanc.sanctions_summary
FROM postgres_trade.lc_master lc
LEFT JOIN accepted_shipment_amd amd_acc
    ON lc.lc_id = amd_acc.lc_id
LEFT JOIN unaccepted_amendments_agg amd_unacc
    ON lc.lc_id = amd_unacc.lc_id
LEFT JOIN parquet_customs.hs_benchmarks cust
    ON lc.hs_code_6 = cust.hs_code_6
CROSS JOIN sanctions_hits_agg sanc
WHERE lc.lc_id = :lc_id;
```

---

## 7. Phase-by-Phase Execution Plan

Execute these 6 focused phases sequentially. Do not proceed to the next phase until the current phase passes its verification check.

### Phase 1: Sponsor Preflight, Data Seeding & Join-Safe Zetaris Federation
1. Inspect official HackOS documentation for **Zetaris** (`zetaris/getting-started`) and **Meterless** (`METERLESS_BASE_URL` / SDK primitives) so all integrations match the exact hackathon environment.
2. Set up the repo structure (`apps/api`, `apps/web`, `data/`) and `docker-compose.yml` (PostgreSQL + Redis).
3. Create `data/customs_parquet/hs_benchmarks.parquet` and `data/opensanctions/watchlist_entities.json`.
4. Build `apps/api/db/seed_scenarios.py` to seed:
   - The **3 Flagship Golden Scenarios** (`LC-2026-8841`, `LC-2026-9104`, `LC-2026-9920`) with complete 5-document presentation data and rendered HTML/PNG documents with bounding boxes.
   - **7 additional evaluation cases** (10 total) covering: (4) Art. 28(c) prohibited Cover Note rejection, (5) Art. 14(c) late presentation (>21 days after shipment), (6) Art. 14(j) Consignee address mismatch on B/L, (7) Art. 10(e) partial amendment acceptance (invalid), (8) Art. 30(b) quantity tolerance within $\pm 5\%$ (valid), (9) Art. 18(c) invoice missing mandatory model spec, and (10) clean compliant presentation with implicit Art. 10(c) amendment acceptance via documents.
5. Implement `apps/api/zetaris/client.py` supporting live Zetaris API execution and automatic local DuckDB + PostgreSQL federation fallback, returning `execution_mode: "LIVE_ZETARIS" | "LOCAL_DUCKDB_FALLBACK"`.
- **Verification Gate 1:** `pytest apps/api/tests/test_zetaris_sql.py` verifies that `federated_check.sql` returns **exactly 1 row per LC** (no duplicate row multiplication) across all scenarios in $< 1.5\text{s}$.

### Phase 2: Stateful Amendment Memory & Deterministic UCP 600 Engine
1. Implement `apps/api/memory/amendment_memory.py`:
   - Parses MT700 base fields and MT707 amendments.
   - Applies **Art. 10(c) & 10(e)** rules: merges `ACCEPTED` amendments, evaluates `UNACCEPTED_PENDING` amendments against presented documents (checking for full implicit acceptance vs. adherence to original terms vs. prohibited partial acceptance), and records an auditable SHA-256 state hash.
2. Implement `apps/api/engines/ucp600_deterministic.py`:
   - Checks expiry dates (**Art. 6(d)(i)**), 21-day presentation window (**Art. 14(c)**), effective shipment date (**Art. 20(a)(ii)**), invoice amount vs. credit limit (**Art. 18(b)**), $\pm 5\%$ quantity tolerance (**Art. 30(b)**), cover-note prohibition (**Art. 28(c)**), insurance date (**Art. 28(e)**), $110\%$ CIF/CIP insurance coverage (**Art. 28(f)(ii)**), and cross-document weight matching (**Art. 14(d)**).
- **Verification Gate 2:** `pytest apps/api/tests/test_deterministic.py` and `test_amendment_memory.py` pass $100\%$. Specifically verify that `LC-2026-9104` fails **UCP 600 Art. 28(f)(ii)** with an exact $\$9,600$ shortfall.

### Phase 3: Meterless Integration, Nemotron Live Extraction & Legal Adjudicator
1. Implement `apps/api/inference/nim_client.py` and `meterless_router.py`:
   - Connect to Meterless and NVIDIA NIM (`https://integrate.api.nvidia.com/v1`).
   - Verify available Nemotron model slugs dynamically on startup, enforce a 25 RPM token-bucket limiter, and support both live uncached execution and SHA-256 cached instant replay.
2. Implement `apps/api/engines/document_extractor.py`:
   - Uses NVIDIA NIM VLM / OCR (or structured extraction pipeline) to parse rendered Commercial Invoice and Bill of Lading images/HTML into structured fields so the demo includes real document ingestion rather than only pre-baked JSON.
3. Implement `apps/api/engines/ucp600_legal_adjudicator.py`:
   - Feeds lexical/field divergences into Nemotron with structured JSON schema output (`verdict`, `ucp_isbp_citation`, `legal_reasoning`, `confidence`).
   - Enforces the **Hard Invariant Rule** in code: if `deterministic_check.passed == False`, the final check status is locked to `DISCREPANT` regardless of any LLM output.
- **Verification Gate 3:** Test `ucp600_legal_adjudicator.py` on `"Industrial AC Servo Mashine"` (returns `COMPLIANT_PROTECTED` citing `ISBP 745 Para A23`), `"Industrial Servo Motors"` on a B/L (returns `COMPLIANT_PROTECTED` citing `UCP 600 Art. 14(e)`), and a mutated Consignee address on a B/L (returns `DISCREPANT` citing `UCP 600 Art. 14(j)`).

### Phase 4: Bank Decision Engine, MT734 / AML Generators & FastAPI SSE Backend
1. Implement `apps/api/engines/decision_engine.py` and `artifact_generator.py`:
   - Selects between:
     - `APPROVE_HONOUR` (clean or protected by ISBP A23 / Art. 14(e)),
     - `ISSUE_MT734_REFUSAL` (generates a formal SWIFT MT734 with fields `:20:`, `:21:`, `:32A:`, `:77J:` discrepancies, `:77B:` `HOLD` disposal status per **Art. 16(c)(iii)(a)**, plus a quantifiable **Beneficiary Re-Presentation vs. Applicant Waiver Demurrage Analysis** when days remain in the Art. 14(c) window),
     - `COMPLIANCE_HOLD_AML` (generates a **Financial Crime / OFAC Sanctions & TBML Escalation Dossier** instead of an MT734 when documents match on their face but fail cross-silo regulatory checks).
2. Implement `apps/api/main.py`:
   - `GET /api/v1/scenarios`: Lists the scenarios and sponsor connection health.
   - `POST /api/v1/examine/{lc_id}`: Streams real-time Server-Sent Events (SSE) across the 5 stages.
   - `POST /api/v1/examine/{lc_id}/approve-action`: Records the **Human Examiner Sign-Off** (`human_approved_by`, timestamp) in `examination_audit_log` before releasing the settlement, MT734, or AML hold.
   - `POST /api/v1/evals/run`: Empirically executes the 10-case test suite across the 3 architectures and returns actual measured scores.
- **Verification Gate 4:** End-to-end API test on all 3 flagship scenarios completes cleanly and logs human sign-off.

### Phase 5: High-Craft 3-Pane Bank Examiner Terminal (Next.js)
Build a dark-mode (`#090D16` background, `#111827` cards, JetBrains Mono for SWIFT/SQL/financial numbers) 3-pane compliance workbench in `apps/web`:
1. **Top Bar (`HeaderBar.tsx`):**
   - Instant Scenario Switcher (`LC-2026-8841 Wrongful Dishonor Trap`, `LC-2026-9104 Curable Shortfall`, `LC-2026-9920 TBML & Sanctions Hit`).
   - Live **UCP 600 Art. 14(b) / Art. 16 5-Banking-Day Preclusion Clock** & **Art. 14(c) 21-Day Presentation Window** badge.
   - Honest Sponsor Telemetry Badges (`Zetaris: LIVE / LOCAL DUCKDB`, `Meterless: ACTIVE`, `NVIDIA NIM: LIVE / CACHED`).
2. **Left Pane (`DocumentViewerPane.tsx`):**
   - Tabs for `MT700 + Amendments`, `Commercial Invoice`, `Ocean B/L`, `Packing List`, and `Insurance Cert`.
   - Includes a **"Run Live Nemotron Extraction"** button and interactive bounding boxes that highlight the exact field when a check is clicked in the center pane.
3. **Center Pane (`AdjudicationMatrixPane.tsx`):**
   - Live execution stream showing which checks were solved by **Deterministic Python Math** vs. **Nemotron Legal Reasoning**.
   - Expandable **Amendment Memory Timeline** showing how Accepted Amendment #1 overrode the baseline while Unaccepted Amendment #2 was quarantined under **Art. 10(c)**.
   - Expandable **Zetaris SQL Drawer** showing the exact CTE-aggregated federated query and 1-row-per-LC result across Postgres, Parquet customs, and OpenSanctions.
4. **Right Pane (`DecisionActionPane.tsx`):**
   - Bank Examiner Verdict Card (`APPROVE HONOUR`, `ISSUE SWIFT MT734 REFUSAL (HOLD FOR RE-PRESENTATION)`, or `COMPLIANCE HOLD & AML ESCALATION`).
   - Preview of the generated **SWIFT MT734** or **AML Escalation Dossier**, gated by an interactive **"Examiner Sign-Off & Dispatch"** button for human-in-the-loop accountability.

### Phase 6: Honest Empirical Baseline Comparison & Final Polish
1. Implement `apps/api/evals/compare_baselines.py` evaluating the 10-case UCP 600 test suite against three fair, genuinely executed pipelines (no hardcoded numbers):
   - **Baseline 1 (Strict Deterministic / Regex):** Exact string matching + date/amount math.
   - **Baseline 2 (Well-Prompted Single-Call LLM with Full UCP 600 Rules Summary):** Fair single-prompt Nemotron baseline given all documents and UCP 600 rules in context, without external SQL federation or pre-pruned amendment state.
   - **VERITAS-600 (Neuro-Symbolic + Stateful Amendment Memory + Zetaris 3-Silo Federation).**
2. Record and display the actual empirical outputs, latencies, and failure breakdowns on `/evals`.

---
# VERITAS-600: Comprehensive Technology Stack Specification

> **Project:** VERITAS-600 (Lean Autonomous Trade Finance & UCP 600 Adjudication Engine)
> **Competition:** Open Agent Hackathon 2026 (GenAI.Works) — Track 03: Reasoning Architecture
> **Architecture Goal:** Strict Neuro-Symbolic Split + In-Situ Federated Data Layer + Meterless Context & Memory Routing + NVIDIA Nemotron Legal & Vision Inference.

---

## 1. High-Level Architecture Overview

```text
[ Next.js 15 Terminal UI ] (Frontend - Port 3000)
         │  (REST / SSE Streams)
         ▼
[ FastAPI Backend API ] (Python 3.11+ - Port 8000)
         ├──> [ Deterministic Python Engines ] (UCP 600 Dates, Insur. Art 28(f)(ii), Tolerances)
         ├──> [ Meterless Core Primitives ] (Scout, World Model, H-MEM Trust Ledger, Markovian Engine)
         ├──> [ Zetaris Federation Client ] (Postgres OLTP + Parquet Customs + OpenSanctions REST)
         └──> [ NVIDIA NIM Client ] (nemotron-3.5-super-vl & nemotron-3-ultra via Rate Limiter & Cache)
```

---

## 2. Detailed Stack Components

### 2.1 Frontend & User Experience
* **Framework:** Next.js 15 (App Router, Server Actions, Client Components)
* **Language:** TypeScript (Strict mode enabled)
* **Styling & UI Components:** Tailwind CSS v3/v4, shadcn/ui patterns, Lucide React icons, JetBrains Mono (for MT700 swift fields, SQL, hashes, and code)
* **State & Data Fetching:** React Hooks, Server-Sent Events (SSE) for live streaming the 6-chunk Markovian examination pipeline and Zetaris telemetry.

### 2.2 Backend & Core Services
* **Language & Runtime:** Python 3.11+
* **Web Framework:** FastAPI (Async endpoints, Pydantic v2 validation, CORS, custom SSE middleware)
* **Database & State Store (OLTP):** PostgreSQL 16 (Stores `lc_master`, `lc_amendments`, `zero_trust_mandates`, audit logs)
* **Cache & Nonce Store:** Redis 7 (Token bucket rate limiting, ZTRV consume-once nonces, SHA-256 NIM response cache)

### 2.3 Mandatory Sponsor Integrations
* **Zetaris (Federated Data Layer):**
  * *Role:* In-situ single-query federation across 3 distinct data sources without ETL.
  * *Sources:* PostgreSQL (`postgres_trade`), Apache Parquet Lakehouse (`parquet_customs`), and OpenSanctions REST API (`rest_opensanctions`).
  * *Implementation:* `ZetarisFederationClient` supporting official remote REST/JDBC endpoints with an automatic local DuckDB/PostgreSQL hot-standby fallback.
* **Meterless (Context, Memory & Reasoning Stack):**
  * *Role:* Context routing, stateful amendment memory (UCP 600 Art. 10), and token efficiency.
  * *Primitives:* Scout Intent, World Model, H-MEM + Trust Ledger (MemTrim atomic evidence tuples), Markovian Engine (6-chunk examination yielding ~86% token reduction), and Task Router (`GET /v1/meterless/modes`).
* **NVIDIA Nemotron (Accelerated Inference Layer):**
  * *Vision & Extraction:* `nvidia/nemotron-3.5-super-vl-120b-a12b` (Multimodal MoE for parsing PDF/image document scans into structured JSON with bounding boxes).
  * *Legal Reasoning & CLEAR Adjudication:* `nvidia/nemotron-3-ultra-550b-a55b` (1M-context hybrid model for resolving ISBP 745 A23 typos vs. Art. 14(j) violations and multi-hop sanctions ownership).
  * *Fast Extraction:* `nvidia/nemotron-3.5-lightning-30b-a3b` (Agentic routing and sub-step normalization).
* **Cursor (AI-Native Development Environment):**
  * *Role:* Primary IDE configured with strict root rules (`.cursorrules`, `AGENTS.md`) ensuring strict separation between deterministic math engines and neural legal reasoning.

### 2.4 Deterministic & Symbolic Engines (Python)
* **Temporal & Arithmetic Verifier:** Pure Python engine executing UCP 600 calendar math, 5-banking-day preclusion clock, 21-day presentation window, $\pm 5\%$ quantity tolerances, and **Art. 28(f)(ii)** 110% insurance calculation ($\ge 110\% \times \max(\text{CIF/InvoiceGross}, \dots)$).
* **CLEAR Adjudication Guard:** Translates neural findings against strict legal boundaries (ISBP 745 A23, Art. 14(e), Art. 14(d), Art. 14(j)).
* **Zero-Trust Runtime Verifier (ZTRV):** HMAC-SHA256 consume-once mandate signing and nonce verification (`SETNX` in Redis/Postgres) blocking replay and context-redirect attacks.

---

## 3. Environment & Deployment Footprint
* **Containerization:** Docker Compose (`docker-compose.yml`) spinning up PostgreSQL 16 and Redis 7 under lightweight limits (<500MB RAM footprint).
* **Hosting / Runtime:** Local or lightweight cloud VPS / managed service deployment. Reproducible via single root command (`npm run dev` or `docker compose up`).
## 8. Definition of Done (Pre-Submission Checklist)

- [ ] All UCP 600 & ISBP 745 citations are legally accurate (`Art. 28(f)(ii)` for 110% insurance, `Art. 28(c)` for cover notes, `Art. 14(e)` for general B/L goods description, `ISBP 745 Para A23` for non-meaning-altering typos, `Art. 10(c)/(e)` for amendments, `Art. 16(c)(iii)` for MT734 disposition).
- [ ] Scenario 3 (`LC-2026-9920`) triggers a **Compliance Hold & AML Escalation Dossier** (not a documentary MT734 refusal).
- [ ] `federated_check.sql` uses CTE aggregation so it never produces duplicate rows when multiple amendments or sanctions hits exist.
- [ ] UI explicitly displays whether Zetaris and NIM are running against live cloud endpoints or local fallback/cache.
- [ ] At least one document supports live Nemotron extraction from its rendered view, and the UI clearly labels pre-structured vs. live-extracted fields.
- [ ] Every final bank action (`Approve Honour`, `Dispatch MT734`, `Place AML Hold`) requires clicking the **Human Examiner Sign-Off** button.
- [ ] `/evals` runs actual code against the 10-case suite and reports genuine empirical results rather than hardcoded claims.