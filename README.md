# VERITAS-600

> **Autonomous Trade Finance & UCP 600 Adjudication Engine**
> *Open Agent Hackathon 2026 (GenAI.Works) — Track 03: Reasoning Architecture*

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB.svg?logo=python&logoColor=white)](apps/api)
[![Next.js](https://img.shields.io/badge/Next.js-15-black.svg?logo=next.js&logoColor=white)](apps/web)
[![CI Pipeline](https://img.shields.io/badge/CI-Automated-success.svg)](.github/workflows/ci.yml)
[![Track](https://img.shields.io/badge/Track-03_Reasoning_Architecture-8A2BE2.svg)](#)

---

## 🏛️ Executive Summary

In global trade finance, **Letters of Credit (LCs)** govern billions of dollars daily under **ICC UCP 600** and **ISBP 745**. When shipping documents arrive, bank documentary credit examiners face high-stakes operational traps:

1. **The 5-Banking-Day Preclusion Cliff (UCP 600 Art. 14(b) & Art. 16):** Banks have only 5 banking days to audit documents. Failing to state all valid discrepancies in a single **SWIFT MT734 Notice of Refusal** legally precludes the bank from refusing payment ($100K–$10M+ balance-sheet loss).
2. **The Wrongful Dishonor Trap:** Rigid regex checks reject harmless typos (e.g., `"Industrial AC Servo Mashine"`). Under **ISBP 745 Para A23**, non-meaning-altering misspellings are legally protected. Wrongful refusals trigger massive litigation.
3. **Stateful Amendment Ambiguity & Cross-Silo TBML:** Standard LLMs confuse original terms with unaccepted amendments (**Art. 10(c)/(e)**). Furthermore, documents may look 100% compliant on paper while hiding **Trade-Based Money Laundering (TBML)** unit-price inflation ($Z > +5.0$) or sanctioned parent companies—requiring a **Regulatory AML Freeze**, not a documentary refusal.

**VERITAS-600** solves this with a production-grade **Neuro-Symbolic Reasoning Architecture**, combining deterministic Python math engines, stateful amendment memory, in-situ federated SQL queries, and multimodal NVIDIA Nemotron legal adjudication.

---

## 📐 System Architecture

```text
                                  ┌────────────────────────────────────────┐
                                  │      Next.js 15 Bank Examiner UI       │
                                  │  (5-Day Clock | 3-Pane Compliance Hub) │
                                  └───────────────────┬────────────────────┘
                                                      │ REST / SSE Streams
                                                      ▼
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                       FastAPI Core Backend Engine                                      │
├───────────────────────────────────┬───────────────────────────────────┬────────────────────────────────┤
│    Pillar 1: Deterministic Engine │   Pillar 2: Stateful Memory       │   Pillar 3: Federated Risk     │
│   (Pure Python - Math & Dates)    │    (Meterless + Art. 10 Rules)    │      (Zetaris In-Situ SQL)     │
├───────────────────────────────────┼───────────────────────────────────┼────────────────────────────────┤
│ • Presentation <= Expiry (Art 6d) │ • Active MT700 Clause Snapshot    │ • Silo 1: PostgreSQL Trade DB  │
│ • 21-Day Window (Art 14c)         │ • MT707 Amendment Lifecycle       │ • Silo 2: Parquet Customs (Z)  │
│ • Insured >= 110% (Art 28f ii)    │ • Accepted -> Merged to State     │ • Silo 3: OpenSanctions API    │
│ • Quantity +/-5% (Art 30b)        │ • Unaccepted -> Quarantined       │ • Join-Safe CTE (1 row / LC)   │
└─────────────────┬─────────────────┴─────────────────┬─────────────────┴────────────────┬───────────────┘
                  │                                   │                                  │
                  ▼                                   ▼                                  ▼
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              NVIDIA Nemotron Legal Adjudication Layer (NIM)                            │
│  • Vision Extraction: Multimodal OCR & Field Bounding Boxes (Invoice, B/L, Insurance Cert)            │
│  • Legal Adjudicator: ISBP 745 A23 (Typos), Art 14(e) (General Descriptions), Art 14(j) (Addresses)   │
│  • HARD INVARIANT: Neural verdict can NEVER override a failed deterministic check                      │
└──────────────────────────────────────────────────┬─────────────────────────────────────────────────────┘
                                                   │
                                                   ▼
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                Bank Officer Decision & Artifact Engine                                 │
│  [1] Approve & Honour    |    [2] Issue SWIFT MT734 Refusal    |    [3] Compliance Hold & AML Dossier  │
│                                                   │                                                    │
│                                                   ▼                                                    │
│                              🔒 MANDATORY HUMAN EXAMINER SIGN-OFF GATE                                │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🏆 Mandatory Sponsor Integrations & Verification Guide

For hackathon judges, every sponsor integration is **load-bearing, auditable, and transparently badged**:

| Sponsor | Architectural Role | Code Location | How Judges Can Verify |
| :--- | :--- | :--- | :--- |
| **Zetaris** | In-situ join across 3 silos (Postgres, Parquet, OpenSanctions) without ETL | `apps/api/zetaris/client.py`<br>`apps/api/zetaris/sql/federated_check.sql` | Run `pytest apps/api/tests/test_zetaris_sql.py`. Inspect live SQL drawer in UI header badge (`[LIVE ZETARIS]` vs `[LOCAL DUCKDB]`). |
| **Meterless** | Context routing, stateful amendment memory, Markovian pipeline | `apps/api/inference/meterless_router.py`<br>`apps/api/memory/amendment_memory.py` | Verify Art. 10(c)/(e) quarantine test via `pytest apps/api/tests/test_amendment_memory.py`. View token reduction in telemetry drawer. |
| **NVIDIA Nemotron** | Document VLM extraction & UCP 600 / ISBP 745 legal adjudication | `apps/api/inference/nim_client.py`<br>`apps/api/engines/ucp600_legal_adjudicator.py` | Run legal adjudicator test. Inspect bounding boxes in Document Viewer pane. Toggle live NIM call vs. SHA-256 cache. |
| **Cursor** | AI-native development environment with neuro-symbolic enforcement | `.cursorrules`<br>`AGENTS.md` | Inspect strict architectural boundaries ensuring zero neural overriding of arithmetic checks. |

---

## 🎯 The 3 Flagship Golden Scenarios

| Scenario | Challenge | Baseline Failure | VERITAS-600 Resolution |
| :--- | :--- | :--- | :--- |
| **`LC-2026-8841`**<br>*Wrongful Dishonor Trap* | Invoice has typo (`"Mashine"`), B/L uses general term (`"Servo Motors"`), shipment follows Accepted Amendment #1. | **Regex/Rule Baseline:** Rejects typo.<br>**Flat RAG:** Confuses unaccepted amendment dates. | **COMPLIANT — APPROVE HONOUR:** Cites **ISBP 745 Para A23** for typo and **Art. 14(e)** for general B/L term. Saves bank from wrongful dishonor litigation. |
| **`LC-2026-9104`**<br>*Curable Shortfall & Demurrage Save* | Insurance is $108\%$ of CIF ($110\%$ required by **Art. 28(f)(ii)**) + gross weight mismatch. 11 days remain in window. | **Pure LLM Baseline:** Hallucinates math or cites wrong article (e.g. 28(c)). | **DISCREPANT — ISSUE MT734 REFUSAL:** Catches exact $\$9,600$ shortfall. Attaches Demurrage Advisory showing $\$11,100$ saved via 48h re-presentation. |
| **`LC-2026-9920`**<br>*TBML & Sanctions Freeze* | Paper documents 100% compliant. Unit price is 5x benchmark ($Z = +5.4$) and parent company on watchlist. | **Document-Only Agent:** Marks compliant and releases funds. | **REGULATORY AML FREEZE:** Zetaris federated query catches cross-silo price anomaly and sanctions hit. Freezes funds and generates AML Dossier (no erroneous MT734). |

---

## ⚡ Quickstart (Local Development)

### 1. Clone & Configure
```bash
git clone https://github.com/sakibul-shovon/VERITAS-600.git
cd VERITAS-600
cp .env.example .env
```

### 2. Start PostgreSQL & Redis
```bash
docker compose up -d
```

### 3. Run Automated Tests
```bash
cd apps/api
pip install -r requirements.txt
pytest tests/ -v
```

### 4. Start Development Servers
```bash
# Terminal 1: Backend API (Port 8000)
cd apps/api && uvicorn main:app --reload --port 8000

# Terminal 2: Frontend Web Terminal (Port 3000)
cd apps/web && npm install && npm run dev
```
Open **`http://localhost:3000`** in your browser.

---

## 📊 Live Baselines Evaluation

To reproduce the empirical benchmark comparing Rule-Based vs. Single-Prompt LLM vs. VERITAS-600:
```bash
python apps/api/evals/compare_baselines.py
```
Or navigate to the **`/evals`** tab in the web interface.

---

## 📄 License & Team

* **License:** Apache 2.0 (See [LICENSE](LICENSE))
* **Architecture & Plan:** Complete details in [docs/plan.md](docs/plan.md)
* **Agent Continuity Tracker:** [STATUS.md](STATUS.md)
