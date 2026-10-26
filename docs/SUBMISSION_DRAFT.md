# VERITAS-600 — Hackathon Submission Form Package

> **Event:** Open Agent Hackathon 2026 (GenAI.Works)  
> **Track:** Track 03: Reasoning Architecture  
> **Participant / Team:** Plan_C — Sakibul Hassan Shovon (Solo Builder)  
> **Repository:** `https://github.com/sakibul-shovon/VERITAS-600.git`  
> **Submission Deadline:** 27 October 2026, 23:45 UTC (28 October 2026, 05:45 Asia/Dhaka)

---

## 📌 Quick Summary / Elevator Pitch (1–2 sentences)

**VERITAS-600** is an autonomous trade finance adjudication engine designed for bank documentary credit examiners. It replaces brittle regex checks and hallucinatory LLMs with a neuro-symbolic reasoning architecture that enforces ICC UCP 600 and ISBP 745 standards, prevents multi-million dollar wrongful dishonors, and surfaces hidden TBML financial crimes across federated data silos.

---

## 🔗 Submission Assets & Verification Links

* **Source Code Repository:** [github.com/sakibul-shovon/VERITAS-600](https://github.com/sakibul-shovon/VERITAS-600)
* **Demo Video (1080p, 2m 54s):**
  * Local path: `H:/Projects/VERITAS-600-video/out/VERITAS-600-launch-1080p.mp4`
  * Duration: 174 seconds (within the 1–4 minute competition rule)
  * Burned-in captions + `.srt` and `.vtt` subtitles included
* **Slide Deck (Required, 21 slides):**
  * PPTX: `H:/Projects/VERITAS-600-presentation/output/VERITAS-600-Plan_C-Deck.pptx`
  * PDF: `H:/Projects/VERITAS-600-presentation/output/VERITAS-600-Plan_C-Deck.pdf`
  * Native editable tables, embedded chart workbook, and complete speaker notes.

---

## 💡 Project Description & Platform Write-Up

### 1. Inspiration & The High-Stakes Problem

In international trade, **Letters of Credit (LCs)** move over \$3 trillion annually under the governing framework of **ICC UCP 600** and **ISBP 745**. When shipping documents arrive at an issuing or confirming bank, documentary credit examiners face extreme operational constraints:

1. **The 5-Banking-Day Preclusion Cliff (UCP 600 Art. 14(b) & Art. 16):** Banks have only 5 banking days from presentation to review documents. If the bank fails to state all discrepancies in a single **SWIFT MT734 Notice of Refusal**, it is legally precluded from refusing payment—absorbing total financial liability on defective cargo.
2. **The Wrongful Dishonor Trap:** Legacy rule-based/regex checkers flag innocuous typographical errors (e.g., spelling `"Machine"` as `"Mashine"`). Under **ISBP 745 Para A23**, misspellings that do not alter commercial meaning are legally compliant. A wrongful refusal triggers costly international litigation and reputational damage.
3. **Stateful Amendment Confusion (UCP 600 Art. 10(c)/(e)):** Standard flat-prompt LLMs confuse original MT700 clauses with unaccepted MT707 amendments, or allow illegal partial acceptance.
4. **Cross-Silo TBML Blindness:** Shipping documents can be 100% compliant on paper while disguising **Trade-Based Money Laundering (TBML)**—such as a 500% unit-price markup ($Z > +5.0$) or a vessel owned by a sanctioned entity hidden across separate customs and watchlists. Issuing a standard MT734 refusal in these cases violates anti-money laundering regulations; it legally requires a **Regulatory Compliance Hold & AML Freeze**.

---

### 2. What VERITAS-600 Does (Solution & Core Features)

VERITAS-600 acts as an intelligent co-pilot and automated adjudication terminal for bank examiners:

* **Multimodal Intake & Spatial Grounding:** Ingests raw PDFs and scans of Commercial Invoices, Ocean Bills of Lading, Packing Lists, and Insurance Certificates, extracting verified fields and rendering interactive spatial bounding boxes `[ymin, xmin, ymax, xmax]`.
* **Stateful Amendment Memory (Art. 10):** Parses base MT700 contracts and incoming MT707 amendments. Automatically merges `ACCEPTED` amendments into an active baseline with SHA-256 fingerprints, while strictly quarantining `UNACCEPTED_PENDING` terms and blocking prohibited partial acceptances.
* **Join-Safe Federated Risk Screening (Zetaris):** In a single CTE-bounded query across three disparate data silos (OLTP Postgres + Parquet Customs Benchmarks + OpenSanctions Watchlist), VERITAS-600 detects cross-border TBML anomalies without requiring expensive or risky ETL data movement.
* **Neuro-Symbolic Legal Adjudication (NVIDIA Nemotron):** Enforces ICC UCP 600 and ISBP 745 legal standards with exact citations (`ISBP 745 Para A23` for protected typos, `Art. 14(e)` for general B/L descriptions, `Art. 14(j)` for address mutations, `Art. 28(f)(ii)` for 110% CIF insurance).
* **The Hard Invariant Rule:** A neural LLM verdict can *never* override a failed deterministic check. If math or dates fail in Python, the check is permanently locked as `DISCREPANT`.
* **Bank Decision Studio & Automated Artifacts:** Generates compliant SWIFT MT734 refusal notices, AML escalation dossiers, and settlement authorization vouchers.
* **Mandatory Human-in-the-Loop Sign-Off:** No funds are released and no SWIFT notice is dispatched without cryptographic digital authorization from a certified bank examiner (`POST /api/v1/examine/{lc_id}/approve-action`).

---

### 3. The 3 Flagship Demonstration Scenarios

| Scenario | Challenge | Flawed Baseline Outcome | VERITAS-600 Outcome |
| :--- | :--- | :--- | :--- |
| **`LC-2026-8841`**<br>*(Wrongful Dishonor Trap)* | Invoice contains harmless typo (`"Industrial AC Servo Mashine"`), B/L uses general description (`"Servo Motors"`), shipment follows Accepted Amendment #1. | **Regex Baseline:** Wrongfully dishonors due to typo.<br>**Flat RAG:** Rejects shipment date due to unaccepted amendment confusion. | **`APPROVE_HONOUR`**: Adjudicates typo as compliant under **ISBP 745 Para A23** and general description under **Art. 14(e)**, protecting the bank from litigation. |
| **`LC-2026-9104`**<br>*(Curable Shortfall & Demurrage Save)* | Insurance coverage is 108% CIF (minimum 110% required under **Art. 28(f)(ii)**) + packing gross weight mismatch. 11 days remain in presentation window. | **Pure LLM Baseline:** Hallucinates math or cites wrong articles. | **`ISSUE_MT734_REFUSAL`**: Computes exact \$9,600 shortfall. Attaches Demurrage Advisory showing quantifiable \$11,100 port savings if cured within 48 hours. |
| **`LC-2026-9920`**<br>*(TBML & Sanctions Freeze)* | Paper documents are 100% compliant on face. Unit price is 5x market distribution ($Z = +23.1\sigma$) and vessel owner is on OFAC/sanctions list. | **Document-Only Agent:** Marks compliant, missing financial crime. | **`COMPLIANCE_HOLD_AML`**: Zetaris federation flags price anomaly and sanctions hit. Freezes payment and issues AML Escalation Dossier. |

---

### 4. Sponsor Technologies Integration

| Sponsor | Architectural Role | Exact Implementation Details |
| :--- | :--- | :--- |
| **Zetaris** | Federated Data Virtualization | Implemented in `apps/api/zetaris/client.py` and `sql/federated_check.sql`. Queries 3 disparate silos (PostgreSQL trade DB + Parquet customs distributions + OpenSanctions JSON) in a single join-safe CTE query returning 1 row per LC. Includes automatic DuckDB fallback when cloud endpoints are offline. |
| **Meterless** | Context Routing & State Memory | Implemented in `apps/api/inference/meterless_router.py` and `apps/api/memory/amendment_memory.py`. Enforces a 6-stage Markovian pipeline routing tailored context packets to each stage, eliminating prompt clutter and managing stateful MT707 transitions under Art. 10(c)/(e). |
| **NVIDIA Nemotron** | Multimodal OCR & Legal Reasoning | Integrated via NVIDIA NIM (`apps/api/inference/nim_client.py` & `apps/api/engines/ucp600_legal_adjudicator.py`) using `nemotron-super-49b` and vision models. Features 25 RPM token-bucket rate limiting and SHA-256 deterministic response caching. |
| **Cursor** | AI-Native Development Governance | Governed by `.cursorrules` and `AGENTS.md` enforcing the 5 Inviolable Architectural Invariants and strict domain boundaries between symbolic calculations and neural reasoning. |

---

### 5. Technical Stack & Clean Architecture

* **Backend:** FastAPI (Python 3.11+), Pydantic v2 domain schemas, PyMuPDF for PDF rendering, DuckDB for local virtualization, SQLite/JSON case storage.
* **Frontend:** Next.js 15 (App Router), React 19, TypeScript, Tailwind CSS, Lucide icons, JetBrains Mono font.
* **Security & Integrity:** HMAC-SHA256 decision digests (`V600-SIG-...`), Merkle audit trees, homoglyph normalization against prompt injection, constant-time signature verification, and zero wildcard CORS.
* **Test Verification:** 58/58 passing automated Pytest tests, 100% clean Ruff linter checks, and clean Next.js production build with static pre-rendering.

---

### 6. Transparent Disclosures & Limitations

In accordance with honest hackathon presentation standards:
* **Telemetry Truthfulness:** The UI and API explicitly display runtime status badges (`LOCAL_DUCKDB_FALLBACK` vs. `LIVE_ZETARIS`, `CACHED_REPLAY` vs. `LIVE_UNCACHED`, `PDF_TEXT_LAYER` vs. `LIVE_NEMOTRON_VLM`).
* **Human-in-the-Loop:** VERITAS-600 provides decision recommendations; final settlement or refusal dispatch requires explicit authorization from a human examiner (`AUTHORIZED_NOT_DISPATCHED`).
* **Evaluation Baseline:** The 10-scenario benchmark suite illustrates architectural trade-offs using dynamic algorithmic baselines and synthetic golden test cases.
