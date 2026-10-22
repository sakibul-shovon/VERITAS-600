# VERITAS-600: World-Class Architecture, Product, and Hackathon Elevation Blueprint

> Evidence snapshot: 22 October 2026
> Target: Open Agent Hackathon 2026 — Track 03, Reasoning Architecture
> Audience: hackathon judges, trade-finance product leaders, bank engineering teams, compliance leaders, and implementers
> Scope: evidence-backed critique and implementation specification; this document does not claim that proposed capabilities already exist

---

## Executive verdict

VERITAS-600 has a genuinely strong core idea: it treats documentary-credit examination as a constrained decision system rather than as a chatbot. Its neuro-symbolic separation, amendment-state concept, join-safe cross-silo query, explicit compliance-hold branch, and human sign-off gate are all well chosen for Track 03.

The current repository is nevertheless an advanced scripted prototype, not yet a commercial-grade bank control. The automated baseline suite passes 27/27 tests and the Next.js production build succeeds, but those checks do not validate several important runtime claims. In particular:

- The browser opens the examination stream with `EventSource`, which issues a GET, while the API exposes the SSE examination route only as POST. The central demo path is therefore not browser-valid as implemented.
- The document extractor ignores its document input and returns scenario-specific fixtures. Merely configuring an NVIDIA key changes the label to `LIVE_NEMOTRON_VLM` even though no vision request occurs.
- The Meterless router creates six local Python packets but never invokes Meterless primitives or a Meterless endpoint. Its token reduction is a modeled estimate based on repeating the full context six times, not measured model usage.
- The “single-prompt LLM” and regex baselines are scripted outcomes keyed by scenario ID, with synthetic latency offsets. The displayed 100% versus 40% versus 40% comparison is therefore a demonstration fixture, not an empirical model evaluation.
- Human sign-off returns `APPROVED_AND_EXECUTED` for any LC ID without authentication, maker-checker separation, decision binding, persistence, idempotency, or downstream dispatch.
- The SHA-256 value is a snapshot digest of active terms, not an append-only evidence chain or Merkle proof.

These are fixable. The winning path is not to add more visual spectacle first. It is to make every visible claim inspectable and true, then expose that truth through an exceptional examiner experience.

The target product should be positioned as:

> **A verifiable decision control plane for documentary-credit examination: every fact is source-linked, every deterministic failure is non-overridable, every semantic judgment is schema-constrained, every state transition is reproducible, and every external action requires authenticated dual control.**

---

# 1. Hackathon and Sponsor Strategy Matrix

## 1.1 Official Track 03 framing and scoring

The official Track 03 challenge is to demonstrate a novel ability to turn **data, knowledge, memory, and reasoning into reliable decisions and actions**. The event uses one published 100-point rubric for all primary tracks; it does not publish four separate sponsor-specific judging rubrics.

| Official criterion | Points | What the official rubric asks | What VERITAS-600 should prove in the demo |
|---|---:|---|---|
| Impact | 30 | Meaningful real-world problem and fit to intended users | A real examiner workflow; quantified exposure and cycle-time metrics; evidence that the action changes because of legal, document, and risk context |
| Technical | 20 | Implementation quality, reliability, and architecture | Hard invariants, typed contracts, live integrations, replayable evidence, failure handling, tests beyond golden fixtures, and authenticated sign-off |
| Innovation | 15 | Originality and creativity of the approach | The decision lattice, atomic amendment state machine, evidence-bound neural judgment, and cross-silo risk branch—not merely an LLM wrapper |
| Demo | 15 | Clarity of functionality and value | One coherent 1–4 minute story with a visible input, reasoning transition, evidence trace, decision, human approval, and receipt |
| Product & UX | 10 | Intuitive, accessible, easy to use | An examiner-first queue and workspace, linked evidence, keyboard flow, legible information density, uncertainty handling, and accessible status semantics |
| Sponsor technology | 10 | Effective sponsor use that improves the product | Inspectable Zetaris execution, Meterless conformance and measured context savings, live/schema-constrained Nemotron, and auditable Cursor workflow evidence |

Official sources: [Open Agent Hackathon 2026 event, tracks, rules, scoring, and submission requirements](https://hackathon.genai.works/event/open-agent-hackathon-2026) and [GenAI Academy event course](https://academy.genai.works/courses/open-agent-hackathon-2026/details).

### Submission constraints that materially affect architecture

The official rules require Zetaris and Meterless integration and require Cursor to be used for development. NVIDIA should be integrated where it contributes. The submission must include a 1–4 minute demo, a slide deck, a GitHub repository, and a clear explanation of sponsor usage and what is unique about it. Those requirements mean that sponsor proof cannot live only in source code; it must be visible in the running product and reproducible from the repository.

## 1.2 Sponsor strategy: published capability versus winning proof

The “evaluation lens” below is an evidence-based strategy inference, not a claim that each sponsor has published a separate scorecard.

| Sponsor | Published capability relevant to the project | Current repository evidence | Critical gap | Winning proof artifact |
|---|---|---|---|---|
| Zetaris | Query-in-place virtualization across files, logical databases, streams, and REST sources without conventional ETL | A join-safe SQL file and a DuckDB simulation over an OLTP standby, Parquet, and local watchlist JSON; explicit `LIVE_ZETARIS`/fallback mode | The live `/query` contract is assumed, not integration-tested; local fallback is not true in-situ federation; accepted-amendment selection is not partitioned by LC | A live, recorded three-source query with query ID, source plan, row counts, freshness, latency, and a fallback comparison showing identical output |
| Meterless | H-MEM, World Model, Markovian reasoning, and Scout Intent; official reference/conformance assets; modeled Markovian savings | Six locally constructed context packets and an estimated savings percentage | No Meterless engine invocation, durable H-MEM ledger, conformance run, signed execution contract, or measured provider token usage | Vendor reference implementation or conformance suite in CI; a per-stage context manifest; actual prompt token counts; cold/warm comparison; durable state lineage |
| NVIDIA Nemotron/NIM | OpenAI-compatible NIM endpoints and structured generation with JSON-schema constraints | A chat-completions call, rate limiter, local response cache, and deterministic semantic replay | Extraction is not a VLM call; JSON is prompt-requested rather than schema-constrained; model availability is not checked; synthetic fallback is labeled cached | A real document image sent to an available Nemotron vision model; guided JSON schema; model/version/request ID; raw-to-normalized provenance; cache keyed by model and prompt version |
| Cursor | Version-controlled rules and agentic development workflows; `AGENTS.md` is supported and `.cursorrules` is legacy | Strong root `AGENTS.md`, architecture invariants, `STATUS.md`, graph, Repomix context, and CI | `.cursorrules` is deprecated; there is no machine-readable record connecting rules, agent tasks, diffs, and verification | Migrate scoped rules to `.cursor/rules/*.mdc`, retain `AGENTS.md`, and show a concise build ledger: task → rule → changed files → tests → review |

Primary capability references: [Zetaris connection and source types](https://kbase.zetaris.com/knowledge/connect), [Zetaris query-in-place architecture](https://www.zetaris.com/zetaris-meta-data-lakehouse), [Meterless engine architecture and conformance references](https://github.com/Meterless/Meterless), [NVIDIA NIM structured generation](https://docs.nvidia.com/nim/large-language-models/1.14.0/structured-generation.html), and [Cursor Rules and AGENTS.md](https://docs.cursor.com/context/rules-for-ai).

## 1.3 Evidence-based readiness score

This is an internal code-evidence score, not a prediction of the judges’ score.

| Criterion | Current evidence score | Why it is not higher yet | Target after the roadmap |
|---|---:|---|---:|
| Impact | 24/30 | Strong problem and scenarios, but economic figures are assumptions rather than measured outcomes | 28–30 |
| Technical | 10/20 | Sound decomposition and passing unit tests, but critical browser, persistence, security, and live-integration gaps | 18–20 |
| Innovation | 11/15 | Excellent neuro-symbolic concept; proof-chain and formal-state claims are not implemented | 14–15 |
| Demo | 7/15 | Attractive screens, but the main SSE browser path and extraction interaction are not end-to-end valid | 14–15 |
| Product & UX | 6/10 | Good information architecture; weak accessibility, workflow state, evidence linkage, and exception handling | 9–10 |
| Sponsor technology | 4/10 | Zetaris/NIM have plausible clients; Meterless and VLM evidence are not live; telemetry overstates capability | 9–10 |
| **Total** | **62/100** | **Compelling architecture, insufficiently proven runtime** | **92–100** |

## 1.4 Five-second judge comprehension contract

Within five seconds, the screen should communicate three facts without narration:

1. **What is at risk?** `USD 480,000 presentation · 2 discrepancies · 2d 14h to refusal deadline`.
2. **Why is the answer trustworthy?** `Deterministic lock active · 8/10 checks passed · evidence-linked`.
3. **What happens next?** `Draft MT734 · human approval required · no message dispatched`.

Sponsor badges should be secondary evidence, never the hero. A badge must represent the observed execution of the current run, not merely the presence of an API key.

---

# 2. First-Principles Codebase Critique

## 2.1 What is already unusually strong

### The domain choice has real consequence

Documentary-credit examination has deadlines, conflicting state, formal documents, financial arithmetic, legal semantics, sanctions concerns, and irreversible external actions. It is therefore a materially better Track 03 demonstration than a generic research assistant.

### The neuro-symbolic boundary is directionally correct

The repository consistently expresses the central invariant: Python owns dates, arithmetic, tolerances, and cross-document numeric checks; the model handles semantic ambiguity. The hard lock in `ucp600_legal_adjudicator.py` ensures a neural result cannot turn a failed deterministic evaluation into a compliant verdict.

### The action model is better than a binary pass/fail

Separating `APPROVE_HONOUR`, `ISSUE_MT734_REFUSAL`, and `COMPLIANCE_HOLD_AML` demonstrates that documentary compliance and regulatory permission are different decision dimensions. The dominance of a regulatory hold over payment is a valuable architectural idea.

### The federation query is intentionally join-safe

Amendments and sanctions hits are aggregated before the final LC join. That reflects awareness of an easy-to-miss correctness failure: Cartesian row multiplication can inflate hit counts and duplicate an LC. The test asserting one row per LC is worth preserving and expanding.

### The repository is operationally legible

`AGENTS.md`, `STATUS.md`, the architecture plan, Graphify output, Repomix output, CI, and focused test modules give both humans and coding agents a coherent map. The current local verification result is:

- Backend: **27/27 tests passed** on Python 3.11.
- Frontend: **Next.js production build passed**, including type checking and static generation.

That is credible evidence of internal consistency. It is not yet evidence of production or live sponsor integration.

## 2.2 Critical findings: fix before presenting the system as live

| Severity | Finding | First-principles failure | Consequence |
|---|---|---|---|
| P0 | Frontend `EventSource` sends GET to a POST-only `/api/v1/examine/{lc_id}` route | Client/server transport contract is inconsistent | The primary “Examine Presentation” browser flow can fail with method-not-allowed despite API tests passing |
| P0 | `DocumentExtractor` ignores the supplied document/path and selects hardcoded values by `lc_id` | Output is not causally derived from input | “Live Nemotron OCR” is not a truthful claim; arbitrary documents cannot be examined |
| P0 | Extraction response fields are dictionaries, while the UI spreads them as arrays and reads nonexistent `field_name`/`extracted_value` keys | Typed contract is absent across the boundary | The extraction button can raise a client-side runtime error even though the TypeScript build passes because `any` hides it |
| P0 | Meterless is never called; health reports `active: true` regardless of configuration | Sponsor telemetry describes intent, not observed execution | Sponsor-use evidence is weak and the 86% badge is misleading |
| P0 | Baseline verdicts and latency are scripted by scenario ID | Evaluation knows the answer before inference | 40/40/100 results cannot be called empirical and are vulnerable to immediate judge challenge |
| P0 | Approval accepts an arbitrary examiner string and returns “executed” without authentication or persistence | A UI click is mistaken for an authorization control | The human gate is cosmetic; there is no non-repudiation, separation of duties, or recoverable audit record |
| P0 | Health infers “live” from key presence | Configuration is mistaken for successful service use | A bad key or unreachable endpoint can still produce a green live badge |
| P0 | Synthetic legal replay is labeled `CACHED_REPLAY` even when it was never produced by NIM | Cache provenance is false | A judge cannot tell a real replay from hand-authored rule output |
| P1 | Live NIM output is parsed with raw `json.loads` but no guided schema or validation | Prompt compliance is treated as a contract | Markdown fences, malformed JSON, unknown citations, or incompatible fields can crash or contaminate a decision |
| P1 | `accepted_shipment_amd` uses a global `ORDER BY ... LIMIT 1`, not one latest row per `lc_id` | The query is join-safe but not logically partition-safe | Additional accepted amendments can cause the wrong LC to miss its effective shipment date |
| P1 | Fallback SQL uses string replacement for names and LC IDs | Data values are treated as SQL syntax | Quotes can break the query and untrusted values create injection risk |
| P1 | Amendment grouping expects multiple clauses under one `amendment_id`, while the schema makes `amendment_id` the single-column primary key | Data model contradicts atomic-amendment logic | A multi-clause MT707 cannot be represented as intended; Art. 10(e) coverage is structurally incomplete |
| P1 | Partial-acceptance violation is displayed but is not converted into a locked decision check in the main pipeline | Detection is disconnected from enforcement | The system can know about an Art. 10(e) problem without making it action-determinative |
| P1 | Active-state date comparisons and unit prices are string comparisons | Representation leaks into semantics | Non-ISO dates, decimals such as `480` versus `480.00`, and locale formats can produce wrong transitions |
| P1 | The NIM rate limiter claims thread safety but has no lock and sleeps synchronously | Concurrency and async execution are not modeled | Concurrent requests can race or block the event loop/thread pool |
| P1 | Audit table exists, but examination and approval do not write to it | Schema is mistaken for auditability | Runs disappear on restart and approval cannot be tied to the exact decision shown |
| P1 | CORS allows all origins with credentials | Trust boundaries are undeclared | An institutional deployment would expose an unsafe browser security posture |
| P1 | The preclusion clock is a fixed UI counter, not a banking-calendar calculation | High-stakes time is decorative | The most important deadline can be wrong and does not account for bank holidays or place of performance |
| P2 | Tiny 10–11 px text dominates the terminal | Density is prioritized over legibility | Poor accessibility, scanning fatigue, and weak projection readability during judging |
| P2 | The document pane and findings are not actually linked | Evidence and conclusion remain separate | Examiners still perform visual reconciliation manually and cannot prove why a finding was raised |

## 2.3 Architectural bottlenecks

### Scenario coupling

Many engines branch on known LC IDs or known substrings. This produces a polished golden path but prevents generalization. A production design must be driven by document type, typed fields, rule packs, and evidence references—not by scenario identity.

### Missing domain boundary

The system passes broad dictionaries between layers. That makes it easy to confuse `amount`, `invoice_amount`, CIF basis, drawing amount, or normalized versus raw address. Typed domain objects are needed for money, quantity, date, party identity, document evidence, and rule results.

### “Fail open” semantic behavior

The deterministic replay returns a clean result by default. The legal adjudicator also supplies compliant defaults for missing model fields. In a high-stakes system, malformed or unknown semantic output must become `MANUAL_REVIEW_REQUIRED`; it must never silently become compliant.

### Outcome without provenance

Checks contain prose and computed values, but they do not carry immutable references to:

- the source document digest and page;
- the exact bounding box and OCR span;
- the normalized value and transformation history;
- the LC/amendment state version;
- the rule implementation/version;
- the model, prompt, schema, response, and cache origin;
- the federation query ID and data freshness.

Without these, the product can explain, but it cannot prove.

### Evaluation leakage

Ground-truth labels and handcrafted baseline failure behaviors live in the same repository and execution path. The correct next step is a blind, versioned test corpus with adjudicator-reviewed labels and actual baseline execution. Report confidence intervals, not only point accuracy.

## 2.4 Real examiner workflow: what the product must support

A documentary-credit examiner’s work is a controlled case workflow, not a single inference request:

1. Register the presentation, receipt channel, presenting party, timestamps, and document inventory.
2. Compute the governing banking-day deadline from the bank calendar and place of examination under **UCP 600 Art. 14(b)**; track refusal preclusion under **Art. 16(f)**.
3. Retrieve the issued credit, all amendments, acceptance evidence, prior drawings, and remaining availability.
4. Classify documents and verify originals/copies/signatures/issuers before field-level comparison.
5. Reconcile dates, amounts, quantities, shipment, insurance, parties, and descriptions.
6. Consolidate all documentary discrepancies into one proposed refusal notice and validate the document-disposal statement under **Art. 16(c)(iii)**.
7. Run sanctions, vessel, beneficial-ownership, AML/TBML, and bank-policy controls in a parallel but separately explained branch.
8. Route exceptions to the appropriate queue: document examiner, senior checker, sanctions officer, AML investigator, or applicant-waiver workflow.
9. Apply maker-checker approval, dispatch through an authorized channel, capture acknowledgment, and retain an immutable evidence package.

The current UI begins at step 4 and ends with a simulated step 9. A bank-indispensable product must own the entire case state while keeping final external authority with authenticated human officers.

## 2.5 Quantifying impact without overstating it

Use auditable formulas and label scenario assumptions:

| KPI | Defensible formula | Required evidence |
|---|---|---|
| Examination cycle time | `decision_ready_at - presentation_received_at` | Server timestamps from real runs; p50/p95 across cases |
| Preclusion headroom | `refusal_deadline - approved_notice_at` in banking time | Versioned holiday calendar and bank location |
| Wrongful-dishonor avoidance | Count of independently labeled compliant cases that a baseline refused and VERITAS correctly honored | Blind labels, reviewer agreement, no scenario-ID branching |
| Discrepancy recall | Confirmed discrepancies detected / all confirmed discrepancies | Reviewer-labeled corpus and error analysis |
| Regulatory leakage | Cases with adjudicated sanctions/AML blocks that a pipeline would have released | Frozen watchlist snapshot and reviewer disposition |
| Modeled demurrage avoided | `max(0, waiver_days - cure_days) × daily_demurrage` | Contract/source for daily rate and labeled assumption for turnaround |
| Token reduction | `1 - routed_input_tokens / baseline_input_tokens` | Provider-returned usage for identical case/output conditions |
| Examiner effort saved | Active review minutes with and without assistance | Timed usability study; do not infer from model latency |

The current `$11,100` value is a useful scenario calculation—`(8 - 2) × $1,850`—but it should be shown as **modeled potential savings**, not realized savings or savings per every LC.

---

# 3. The Frontier Reasoning Upgrade

## 3.1 Target architecture: an evidence-carrying decision pipeline

```text
Presentation Intake
  └─ immutable source artifacts + receipt clock
       └─ document classification and extraction
            └─ normalized evidence graph
                 ├─ amendment state machine
                 ├─ deterministic rule engine
                 ├─ schema-constrained semantic adjudicator
                 └─ Zetaris federated risk evidence
                      └─ policy lattice / decision compiler
                           └─ human maker-checker authorization
                                └─ transactional outbox / SWIFT or case-system adapter
                                     └─ signed receipt + replayable audit bundle
```

Every arrow must pass typed data plus provenance. No stage may receive only a prose summary when an exact source field exists.

## 3.2 Evidence model and cryptographic proof chain

### Canonical evidence envelope

Create a domain-level `EvidenceRef` carried by every check:

```json
{
  "evidence_id": "ev_01J...",
  "artifact_sha256": "...",
  "document_type": "OCEAN_BILL_OF_LADING",
  "document_id": "MEDU987654321",
  "page": 1,
  "bbox_xyxy_normalized": [0.10, 0.47, 0.85, 0.53],
  "raw_text": "INDUSTRIAL SERVO MOTORS",
  "normalized_value": "industrial servo motors",
  "extraction_model": "nvidia/...",
  "model_revision": "...",
  "confidence": 0.96,
  "observed_at": "2026-10-22T...Z"
}
```

Use RFC 8785-style JSON canonicalization before hashing. Never hash Python’s incidental string representation.

### Append-only event chain

For event `n`:

```text
event_hash[n] = SHA-256(
  domain_separator ||
  event_hash[n-1] ||
  canonical_json(event_payload[n])
)
```

The payload contains the actor, action, decision/run ID, evidence hashes, rule-pack version, model request/response digest, federated query receipt, and timestamp from a trusted server clock. Updates are new events; previous events are never mutated.

### Merkle run root

Create leaves for source artifacts, extraction records, state transitions, rule results, model adjudications, federation results, decision, approval, and dispatch acknowledgment. Build a binary Merkle tree and store:

- `merkle_root` on the examination run;
- sibling paths for each visible finding;
- the canonicalization algorithm and tree version;
- a KMS/HSM-backed signature over `run_id || merkle_root || created_at`.

Expose `GET /api/v1/examinations/{run_id}/proof` and a standalone verifier. A verifier must be able to prove that a displayed discrepancy belonged to the signed run without receiving unrelated documents.

Reference standards: [RFC 8785 JSON Canonicalization Scheme](https://www.rfc-editor.org/rfc/rfc8785) and [RFC 9162 Merkle-tree inclusion/consistency proof design](https://www.rfc-editor.org/rfc/rfc9162).

### Threats the proof must and must not address

It proves post-commit tamper evidence and inclusion. It does not prove that OCR was correct, the source document was genuine, or a human was authorized. Those require extraction review, document-authenticity controls, identity, and policy enforcement.

## 3.3 Formal amendment state machine

Represent an amendment as one atomic object with multiple clauses:

```text
Amendment {
  amendment_id,
  credit_id,
  sequence,
  clauses[],
  advised_at,
  beneficiary_response,
  evidence_refs[],
  status
}
```

Recommended states:

```text
ADVISED_PENDING
  ├─ explicit full acceptance ──> ACCEPTED
  ├─ explicit rejection ────────> REJECTED
  ├─ documents match all clauses -> IMPLICITLY_ACCEPTED
  ├─ documents match no clauses -> REMAINS_PENDING / original terms apply
  └─ documents match a strict subset -> PARTIAL_ACCEPTANCE_REJECTED + discrepancy review
```

Key invariants:

1. An amendment’s clauses transition atomically under **UCP 600 Art. 10(c) & 10(e)**.
2. Only accepted or fully implicitly accepted amendments modify the active term snapshot.
3. Sequence order is total per credit and monotonic.
4. A state transition records evidence and the previous state hash.
5. A pending amendment never silently modifies deterministic checks.
6. Ambiguous or missing fields produce an unresolved branch, never assumed acceptance.
7. Partial-acceptance detection becomes a locked rule result consumed by the decision compiler.

Implement a PlusCal/TLA+ model or Alloy model for transition safety, then mirror those invariants in property-based tests. The formal model is most valuable for proving that no event sequence allows a pending clause to leak into the active baseline.

## 3.4 Deterministic kernel and legal rule registry

Create versioned rule packs instead of embedding citations and prose across engines:

```text
rulepacks/
  ucp600/2026.1/rules.yaml
  isbp745/2026.1/rules.yaml
  bank_policy/demo-bank/2026.1.yaml
```

Each rule defines:

- stable rule ID;
- exact citation from an allowlist;
- applicability predicate;
- required evidence fields;
- deterministic function or semantic adjudication schema;
- severity and whether it locks the result;
- remediation text;
- reviewer and approval metadata;
- unit, boundary, metamorphic, and counterexample tests.

Important correction: “invoice description must correspond” under **UCP 600 Art. 18(c)** should not become naïve byte equality. The deterministic layer should identify factual tokens and omissions; the semantic layer may assess correspondence, but only from source-bound evidence and an approved schema.

## 3.5 Fail-closed semantic adjudication

Use NVIDIA guided JSON rather than asking for JSON in prose. A minimal output contract:

```json
{
  "schema_version": "1.0",
  "candidate_verdict": "COMPLIANT_PROTECTED | DISCREPANT | INDETERMINATE",
  "citation_ids": ["ISBP745.A23"],
  "evidence_ids": ["ev_...", "ev_..."],
  "material_difference": "...",
  "reasoning_summary": "...",
  "confidence": 0.0
}
```

Enforcement rules:

- Reject citations outside the legal registry.
- Reject missing evidence references.
- Reject unparseable or schema-invalid output.
- Treat `INDETERMINATE`, low confidence, conflicting model samples, and missing evidence as `MANUAL_REVIEW_REQUIRED` workflow status.
- Keep the deterministic verdict lock outside the model-facing code path.
- Record model slug, model revision where available, prompt-template hash, schema hash, request ID, latency, usage, cache origin, and raw response digest.
- Run prompt-injection tests against document text. Document content is evidence, never trusted instruction.

NVIDIA explicitly supports JSON-schema-constrained structured generation and recommends guided JSON for reliable pipeline outputs: [NVIDIA NIM structured generation](https://docs.nvidia.com/nim/large-language-models/1.14.0/structured-generation.html).

## 3.6 Expanded legal and documentary edge-case matrix

Prioritize rule families by irreversible risk, not by visual novelty:

| Rule family | Deterministic responsibilities | Semantic responsibilities | Required adversarial cases |
|---|---|---|---|
| Transport documents, Arts. 19–25 | Required fields, dates, originals, signatures/capacity, ports/airports, transshipment flags | Capacity labels, apparent document character, conflicting route language | Multimodal Art. 19; B/L Art. 20; sea waybill Art. 21; charter-party B/L Art. 22; air Art. 23; road/rail/inland Art. 24; courier/post Art. 25 |
| Charter-party B/L, Art. 22 | Required indication, signing capacity, shipment/port facts | Whether wording evidences that the document is subject to a charter party | Named charter party absent, master/owner/agent signatures, ambiguous “freight payable as per C/P” wording |
| Partial drawings/shipments, Art. 31 | Aggregate quantity/amount, conveyance/date logic, prohibition in credit | Whether documents evidence one or multiple shipments | Same vessel/same journey with multiple B/Ls; different shipment dates; credit expressly prohibiting partial shipment |
| Instalments, Art. 32 | Schedule windows and missed instalment state | Exceptional wording interpretation | Missed first, middle, and final instalments; amendment to only one period |
| Amendments, Art. 10(c)/(e) | Atomic state transitions and sequence | Document-to-clause semantic equivalence | Full implicit acceptance, no acceptance, partial subset, conflicting evidence, out-of-order amendments |
| Originals/copies, Art. 17 | Counts, original markers, required copies | Apparent originality where not mechanically decidable | Digitally signed records, photocopy with original stamp, conflicting “copy/original” wording |
| Data consistency, Art. 14(d) | Numeric/date/identity normalization | Non-identical but non-conflicting text | Unit conversion, transliteration, abbreviations, near-match party names, swapped weights |
| Goods descriptions, Arts. 14(e) and 18(c) | Required attributes and invoice facts | General non-invoice description and invoice correspondence | Synonyms, model omission, added conflicting specification, typo changing meaning |
| Applicant address, Art. 14(j) | Structured address normalization and transport-document location | Materiality of wording where rules allow variation | Consignee vs notify party, postal-code mutation, branch address, applicant name without address |
| Insurance, Art. 28(c), 28(e), 28(f)(ii) | Type, date, currency, basis, percentage, signatures | Coverage wording and exclusions | Cover note, open-cover certificate, retrospective cover statement, CIF unavailable, multiple currencies |
| Amount/quantity tolerance, Art. 30 | Decimal-safe limits and applicability | Interpretation of credit wording | “About/approximately”, prohibited partial drawings, unit versus total tolerance, zero/negative values |
| Refusal, Art. 16(c)(iii), 16(f) | Deadline, complete discrepancy set, disposition option | Clear examiner-facing explanation | Late notice, second notice attempting new discrepancy, invalid disposition, waiver pending |

Every rule needs positive, negative, boundary, and mutation tests. Golden examples alone are inadequate.

## 3.7 Decision lattice: authority before convenience

Separate **analysis status** from **external action**:

```text
REGULATORY_BLOCK
    dominates
DOCUMENTARY_DISCREPANCY_LOCK
    dominates
SEMANTIC_DISCREPANCY
    dominates
COMPLIANT

Any missing/invalid/uncertain prerequisite -> MANUAL_REVIEW_REQUIRED
```

`MANUAL_REVIEW_REQUIRED` is not a fourth final bank action. It is a workflow stop that prevents the engine from recommending or dispatching any of the three final actions until an authorized reviewer resolves the uncertainty.

The final action compiler accepts only signed, versioned inputs. It never reads raw LLM prose.

## 3.8 Real Zetaris federation and anomaly intelligence

### Correct the current query first

Replace the global accepted-amendment `LIMIT 1` with a per-LC window:

```sql
ROW_NUMBER() OVER (PARTITION BY lc_id, amended_field ORDER BY sequence_no DESC) AS rn
```

Then filter `rn = 1`, pre-aggregate every one-to-many source, and assert uniqueness at both SQL and application boundaries. Bind all parameters; never interpolate names.

### Make each source genuinely distinct

- PostgreSQL: live LC master, drawings, amendments, and examination case state.
- Parquet/object store: versioned customs distributions with effective dates and corridor dimensions.
- REST/API virtual source: sanctions entities and relationships with source timestamp, list program, entity IDs, and match evidence.
- Optional fourth source for the frontier version: licensed AIS/port-call data for vessel route anomalies.

### Improve anomaly quality

A raw z-score on four synthetic rows is not a deployable TBML model. Add:

- unit-of-measure and currency normalization;
- Incoterm and freight/insurance normalization;
- origin/destination corridor and time-window cohorts;
- minimum sample-size gates;
- median/MAD or robust quantile scoring for skewed prices;
- HS-code hierarchy backoff when HS6 is sparse;
- separate over-invoicing and under-invoicing signals;
- explanation of peer group and contribution, not only a threshold;
- analyst feedback and false-positive monitoring;
- model/data version and freshness in the result.

For vessel risk, compare declared voyage against AIS port sequence, dark periods, ship-to-ship proximity, flag/ownership changes, and sanctioned-port exposure. These should create review evidence, not autonomous guilt determinations.

### Federation receipt

Every result should include:

```json
{
  "mode": "LIVE_ZETARIS",
  "query_id": "...",
  "sql_sha256": "...",
  "sources": [
    {"name": "trade_pg", "type": "postgres", "freshness": "...", "rows_scanned": 1},
    {"name": "customs", "type": "parquet", "snapshot": "...", "rows_scanned": 14250},
    {"name": "sanctions", "type": "rest", "observed_at": "...", "rows_scanned": 3}
  ],
  "result_rows": 1,
  "elapsed_ms": 214
}
```

The official Zetaris model is query-in-place with metadata registration and support for file, JDBC/logical, stream, and REST sources: [Zetaris connection overview](https://kbase.zetaris.com/knowledge/connect).

## 3.9 Real Meterless integration and measured efficiency

The official Meterless repository describes Markovian reasoning, H-MEM, World Model, Scout Intent, and conformance suites. Integrate against those shipped specifications rather than inventing a nominal gateway contract.

Recommended mapping:

- **Scout Intent:** classify document/check task, risk tier, required tools, and escalation policy.
- **World Model:** hold current examination state, outstanding evidence, deadline, and actor permissions.
- **H-MEM:** retain accepted amendment history and reviewer corrections with provenance and trust state.
- **Markovian:** pass the minimal state required for the next check rather than replaying the full case.

Token evidence must use provider usage or a pinned tokenizer. Run the same case, prompt template, model, and output schema in two lanes:

1. flat full-context baseline;
2. Meterless-routed context.

Report input/output tokens, cache reads, latency, output agreement, and any quality loss. Do not hardcode 86.4%; the official repository describes 86% as a modeled Markovian example, not as a universal product result: [Meterless architecture and efficiency references](https://github.com/Meterless/Meterless).

## 3.10 Human authorization and safe dispatch

Replace the current name field with institutional controls:

- OIDC/SAML identity and MFA/WebAuthn step-up;
- RBAC/ABAC: examiner, checker, sanctions officer, administrator;
- maker-checker separation for high-value or high-risk actions;
- approval bound to `decision_hash`, `artifact_hash`, amount, action, and expiry time;
- visible diff if any input changes after review;
- idempotency key and optimistic concurrency version;
- append-only approval event and signed receipt;
- transactional outbox for dispatch;
- downstream adapter acknowledgment before showing `DISPATCHED`;
- cancellation/revocation state where the rail permits it;
- break-glass path with enhanced logging.

The UI must say `APPROVED — QUEUED FOR DISPATCH` until an external system confirms delivery. Never claim core-banking or SWIFT dispatch when none occurred.

## 3.11 Reliability, security, and operations

- Replace global in-process clients and caches with request-safe dependencies and durable stores.
- Add structured logs, OpenTelemetry traces, correlation IDs, and redaction of document content.
- Use a secrets manager; remove production-like default secrets.
- Encrypt documents and evidence at rest; set retention and legal-hold policies.
- Restrict CORS to configured origins and require authenticated APIs.
- Add rate limits, payload limits, malware scanning, PDF sandboxing, and decompression-bomb protection.
- Pin models and schemas; implement a model-change evaluation gate.
- Define recovery objectives, backup/restore tests, and degradation modes.
- Make live/fallback behavior explicit per run and fail closed when a required risk source is stale or unavailable.
- Conduct threat modeling for prompt injection, OCR adversarial text, forged documents, entity-resolution poisoning, and approval replay.

---

# 4. The Palantir-Grade Visual Blueprint

## 4.1 Design principles

1. **Evidence before ornament.** Every conclusion is clickable to its source.
2. **Density with hierarchy.** Show many facts, but establish one dominant question per pane.
3. **Color carries status only.** Brand and decoration stay neutral; green, amber, red, and violet retain operational meaning.
4. **Progress is causal, not theatrical.** Animation shows state transitions or data movement, never fake processing time.
5. **Authority is tactile and slow.** High-risk actions require deliberate review and authenticated confirmation.
6. **Telemetry is observed.** Each badge belongs to the current run and includes a receipt/detail view.

## 4.2 Visual system

### Palette

```css
:root {
  --canvas: #06090E;
  --surface-1: #0B1119;
  --surface-2: #101925;
  --surface-3: #162231;
  --border-subtle: #223044;
  --text-primary: #F2F6FA;
  --text-secondary: #A8B4C3;
  --text-muted: #748196;
  --accent-cyan: #2DD4BF;
  --accent-blue: #60A5FA;
  --status-pass: #34D399;
  --status-review: #FBBF24;
  --status-fail: #FB7185;
  --status-regulatory: #C084FC;
  --focus-ring: #93C5FD;
}
```

Use subtle translucency only for elevated drawers and command surfaces. Avoid glass effects behind dense text. Shadows should establish layer depth, not neon ambience.

### Typography

- Inter Variable for interface text, loaded with `next/font`.
- JetBrains Mono for identifiers, SWIFT fields, hashes, values, and telemetry.
- Minimum body size 14 px; compact metadata 12 px; never use 10 px for essential evidence.
- Tabular numerals for dates, currency, countdowns, quantities, and z-scores.
- A 1.4–1.55 line height for reasoning prose.

### Accessibility

- Target WCAG 2.2 AA contrast.
- Never encode pass/fail by color alone; add icon, word, and shape.
- Full keyboard path: queue → document → finding → evidence → action.
- Visible focus states and logical focus restoration after drawers.
- `prefers-reduced-motion` disables pulses, path drawing, and spring transitions.
- Use `aria-live="polite"` for pipeline updates and `assertive` only for deadline/regulatory blocks.

## 4.3 Information architecture

### Global case queue

Add an examiner queue before the three-pane workspace:

```text
My Queue | Unassigned | Deadline Risk | Discrepant | Compliance Hold | Awaiting Checker
```

Each row shows LC ID, amount, presenting bank, received time, deadline headroom, document completeness, risk state, and assignee. This makes the product feel like an operating desk rather than a scenario selector.

### Workspace shell

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ Case identity · amount · deadline · observed integrations · command palette │
├───────────────────┬────────────────────────────────┬─────────────────────────┤
│ Evidence          │ Decision Graph                 │ Action & Authorization  │
│ 4/12 columns      │ 5/12 columns                   │ 3/12 columns            │
│                   │                                │                         │
│ Document canvas   │ Stage rail                     │ Recommendation          │
│ + credit compare  │ Rule matrix / dependency DAG   │ Consequences            │
│ + source metadata │ State & federation evidence    │ Artifact diff           │
│                   │                                │ Maker-checker gate      │
├───────────────────┴────────────────────────────────┴─────────────────────────┤
│ Audit timeline · proof root · keyboard hints · environment classification   │
└──────────────────────────────────────────────────────────────────────────────┘
```

On smaller screens, use a task-ordered sequence—Evidence → Findings → Action—rather than squeezing three columns.

## 4.4 Synchronized document viewer

### Core interaction

- Render the actual PDF/image page, not a reconstructed text card.
- Overlay SVG boxes with stable evidence IDs.
- Hovering a finding highlights both the source LC term and presented-document field.
- Clicking a box opens a compare popover: raw crop, OCR text, normalized value, confidence, source hash, and transformation trace.
- Use linked scroll and page navigation when a finding spans documents.
- Permit manual correction with reason, reviewer identity, and a new evidence event—never overwrite OCR silently.

### Visual semantics

- Cyan outline: extracted field.
- Green outline: reconciled/pass.
- Amber dashed outline: requires review.
- Rose solid outline: discrepancy.
- Violet outline: sanctions/AML evidence.

Bounding boxes remain thin until hover/focus. The current design’s dense cards should become a contextual overlay layer so the original artifact remains primary.

## 4.5 Dynamic reasoning matrix

Use a compact dependency graph rather than a decorative sequence:

```text
Receipt Clock ─┐
Amendment State ├─> Deterministic Kernel ─┐
Documents ──────┘                         ├─> Decision Lattice
Documents ─────────> Semantic Judge ──────┤
Federated Sources ─> Regulatory Risk ─────┘
```

Interaction details:

- Nodes transition `queued → running → pass/fail/review` based only on real events.
- Edges pulse once when a dependency resolves; no infinite animation.
- A failed deterministic node visibly closes the compliance gate and shows “non-overridable.”
- Expand a node to show inputs, output schema, duration, version, and proof links.
- “Why this action?” opens the smallest cut of the graph sufficient to justify the recommendation.
- “What would change it?” shows curable facts—useful for re-presentation and waiver analysis—but cannot edit source evidence.

## 4.6 Decision pane and tactile authorization

### Before approval

Show:

- recommended action and confidence category;
- decision basis grouped into documentary, semantic, and regulatory branches;
- unresolved evidence count;
- downstream consequences;
- exact artifact diff and recipients;
- explicit statement: `Nothing has been dispatched`.

### Approval ceremony

1. Reviewer clicks `Review & authorize`.
2. A full-screen confirmation summarizes action, amount, recipient/rail, deadline, decision hash, and artifact hash.
3. Required checklist items are backed by system state, not cosmetic checkboxes.
4. WebAuthn or enterprise step-up verifies identity.
5. A checker approves if policy requires dual control.
6. The system writes the approval event, queues the outbox item, and shows its signed receipt.
7. Status changes to `DISPATCHED` only after downstream acknowledgment.

For a regulatory hold, remove celebratory green visuals. Use calm violet/rose semantics, limit details according to role, and route to the compliance queue.

## 4.7 Motion and micro-interactions

- 120–180 ms for hover/focus changes.
- 220–320 ms for drawer or pane transitions.
- One-shot 400 ms edge trace when a reasoning dependency resolves.
- Deadline changes use a subtle numeral crossfade; no perpetual pulse until a configured critical threshold.
- Failed checks enter with a short border emphasis, not screen shake.
- Copy actions show a receipt toast containing the artifact hash, not only “Copied.”
- Every asynchronous action supports cancellation where safe, retry where idempotent, and an inspectable error state.

## 4.8 Demo choreography: 150 seconds

1. **0–15 s — Stakes:** Open the deadline-risk queue and select the `$480,000` presentation.
2. **15–35 s — Evidence:** Show the original insurance amount and packing/B/L weights with linked boxes.
3. **35–60 s — Reasoning:** Run the pipeline; the deterministic insurance and weight checks fail and visibly lock the verdict.
4. **60–80 s — Sponsor proof:** Open the Zetaris receipt showing three source types and the one-row invariant; show the Meterless context manifest and measured tokens; identify the actual Nemotron model/schema for the semantic lane.
5. **80–105 s — Action:** Reveal one consolidated MT734 draft with exact discrepancies and document disposition under **UCP 600 Art. 16(c)(iii)**.
6. **105–125 s — Value:** Show `$11,100 modeled potential demurrage savings`, its assumptions, and remaining re-presentation window.
7. **125–145 s — Control:** Perform authenticated approval and display the signed, hash-bound receipt; state that dispatch is queued or acknowledged truthfully.
8. **145–150 s — Thesis:** “Data, memory, deterministic rules, neural judgment, and human authority—one replayable decision.”

Keep the other two golden scenarios available as judge-driven branches: wrongful-dishonor prevention and regulatory hold.

---

# 5. Concrete Implementation Plan

Priorities are ordered by proof and risk dependency, not by hackathon time pressure.

## Phase P0 — Demo integrity and truthfulness

### `apps/api/main.py`

- Make SSE transport consistent: either expose a GET stream with safe parameters or use a POST streaming client instead of native `EventSource`.
- Create an examination record before processing and persist every stage result.
- Return per-run observed sponsor telemetry; never infer live status from key presence.
- Remove artificial sleeps.
- Validate LC/run state on approval and bind approval to the immutable decision/artifact hashes.
- Do not return `EXECUTED` until an outbox adapter acknowledges execution.
- Restrict CORS and add authentication dependencies.

### `apps/web/src/lib/api.ts`

- Replace `any` contracts with generated OpenAPI types.
- Align stream method/protocol with the backend and support reconnect via event IDs.
- Return the authoritative approval receipt and render backend state instead of locally fabricating approval time.

### `apps/api/engines/document_extractor.py`

- Remove all `lc_id`-specific branches.
- Accept bytes/object URI, compute a source digest, rasterize safely, invoke the configured vision endpoint, validate guided JSON, and return evidence-linked fields.
- Emit `LIVE_NEMOTRON_VLM`, `CACHED_REPLAY`, or explicit `STRUCTURED_FIXTURE` based on observed provenance. A configured key alone changes nothing.

### `apps/web/src/components/DocumentViewerPane.tsx`

- Consume the actual dictionary/object response shape or, preferably, the generated typed schema.
- Render real pages and SVG evidence boxes.
- Wire `highlightedField` and `onHighlightField` through the page so a finding can focus its evidence.
- Rename the button according to observed mode; never show “Live” before a live result returns.

### `apps/api/inference/nim_client.py`

- Add model discovery/startup validation and guided JSON schemas.
- Distinguish actual cached NIM responses from deterministic rule fallback.
- Add retry/backoff, circuit-breaker state, async I/O, concurrency-safe rate limiting, and request IDs.
- Fail closed to manual review for invalid output.

### `apps/api/inference/meterless_router.py`

- Implement official Markovian/Scout/H-MEM contracts or vendor reference code.
- Persist state and run the relevant conformance suite.
- Replace character estimates and the `raw_tokens × 6` assumption with actual, comparable usage.
- Expose a context manifest per stage.

### `apps/api/evals/compare_baselines.py`

- Remove scenario-ID verdict switches and synthetic latency additions.
- Execute each architecture against the same frozen input.
- Separate dataset, labels, runner, and metrics.
- Save raw outputs and environment metadata.
- Compute bootstrap confidence intervals and per-rule confusion matrices.

### P0 acceptance gates

```powershell
.\.venv\Scripts\pytest.exe apps/api/tests/ -v
Set-Location apps/web; npm run build
npx playwright test
```

Add Playwright coverage for the exact judge flow: load case, start stream, receive all stages, click a finding, highlight evidence, approve, and inspect receipt.

## Phase P1 — Verifiable state, audit, and authorization

### New domain modules

```text
apps/api/domain/
  money.py
  evidence.py
  documents.py
  amendments.py
  decisions.py
  telemetry.py
```

Use `Decimal` plus explicit currency for money, timezone-aware timestamps, enumerations for document and action types, and Pydantic models at all API boundaries.

### `apps/api/db/schema.sql` plus migrations

Add normalized tables for:

- `examination_runs`;
- `source_artifacts`;
- `evidence_records`;
- `amendments` and `amendment_clauses`;
- `rule_results`;
- `model_invocations`;
- `federation_receipts`;
- `decision_events`;
- `approval_events`;
- `outbox_messages` and `dispatch_receipts`;
- `audit_merkle_nodes`.

Use migrations rather than startup-only schema files. Enforce unique sequence numbers, foreign keys, immutable event semantics, and optimistic versions.

### New audit modules

```text
apps/api/audit/canonical_json.py
apps/api/audit/hash_chain.py
apps/api/audit/merkle.py
apps/api/audit/signatures.py
apps/api/audit/verifier.py
```

Add a CLI and API verification path that detects a one-byte mutation in any evidence or decision payload.

### Formal state specification

```text
formal/credit_amendments.tla
formal/credit_amendments.cfg
formal/README.md
```

Prove no pending/partially accepted amendment modifies the active snapshot and no action reaches dispatch without a valid approval transition.

### Property-based tests

Add Hypothesis tests that generate amendment sequences, missing fields, decimal formats, date formats, repeated approvals, and concurrent updates.

## Phase P2 — Rule coverage and zero-hallucination controls

### Rule registry

Create `apps/api/rulepacks/` with human-reviewed citations and applicability metadata. Update `ucp600_deterministic.py` and `ucp600_legal_adjudicator.py` to emit stable rule IDs and evidence IDs rather than free-form citations.

### Deterministic engine

- Decimal-safe monetary math.
- Banking-day service with jurisdiction calendar versions.
- Document inventory, originals/copies, signatures/capacity, transport-document families, partial shipments, and instalments.
- Explicit missing-data results rather than defaults to zero/today.
- A pure decision kernel with no network calls or wall-clock reads.

### Semantic adjudicator

- One approved schema per semantic task.
- Citation allowlist and evidence-bound output.
- Prompt-injection isolation.
- Model agreement or verifier pass for high-risk ambiguity.
- Manual-review branch for uncertainty.

### Legal validation gate

Before calling any artifact “bank-ready,” obtain review from qualified documentary-credit practitioners and compliance counsel. UCP rule application, SWIFT field usage, sanctions blocking, SAR confidentiality, and “tipping-off” obligations depend on facts, jurisdiction, and bank policy. The product should present policy configuration and reviewer attribution, not universal legal conclusions.

Official UCP text and the five-banking-day/preclusion framework are available through the [ICC Digital Library UCP 600 rules](https://library.iccwbo.org/content/tfb/RULES/tfb-ucp600-rules.htm?AGENT=ICC_FIN).

## Phase P3 — Federated risk and sponsor proof

### `apps/api/zetaris/sql/federated_check.sql`

- Partition latest amendments by LC and field.
- Filter CTEs by the target LC where possible.
- Pre-aggregate every one-to-many relationship.
- Use entity IDs/IMO numbers, not raw display-name equality alone.
- Return source freshness, match evidence, and one deterministic row per LC.

### `apps/api/zetaris/client.py`

- Use the verified official endpoint/SDK contract.
- Bind values safely.
- Validate the full response schema and exactly-one-row invariant in both modes.
- Record query ID, plan/receipt, source list, latency, error class, and fallback reason.
- Never swallow exceptions without telemetry.

### Data-quality layer

Add units, currencies, corridor cohorts, robust statistics, beneficial-ownership traversal, and freshness policy. Quarantine stale sources and display their effect on the decision.

### Sponsor evidence page

Build `/evidence/sponsors/{run_id}` with four cards:

- Zetaris query receipt and source plan;
- Meterless context/token comparison and conformance version;
- NVIDIA model/schema/request/cache provenance;
- Cursor development ledger and repository rules.

## Phase P4 — Examiner-grade UX

### Frontend foundation

- Add `next/font` Inter and JetBrains Mono.
- Replace ad hoc Tailwind colors with semantic design tokens.
- Increase essential text sizes and add accessible focus/reduced-motion behavior.
- Add typed error, empty, loading, stale, fallback, and offline states.

### New components

```text
apps/web/src/components/CaseQueue.tsx
apps/web/src/components/EvidenceCanvas.tsx
apps/web/src/components/EvidenceComparePopover.tsx
apps/web/src/components/DecisionGraph.tsx
apps/web/src/components/DeadlineClock.tsx
apps/web/src/components/AuthorizationDialog.tsx
apps/web/src/components/AuditReceipt.tsx
apps/web/src/components/SponsorEvidenceDrawer.tsx
```

### Refactor existing components

- `HeaderBar.tsx`: observed run telemetry and real banking calendar.
- `DocumentViewerPane.tsx`: source-first canvas and linked evidence.
- `AdjudicationMatrixPane.tsx`: dependency graph, manual-review states, rule/evidence drill-down.
- `DecisionActionPane.tsx`: consequences, artifact diff, WebAuthn/maker-checker approval, truthful dispatch status.
- `ZetarisDrawer.tsx`: render the actual executed query/receipt, not a hardcoded SQL string.
- `/evals`: disclose dataset version, actual model runs, sample size, confidence intervals, and failure examples.

## Phase P5 — Production controls and independent evaluation

- Browser E2E, contract, integration, chaos, load, accessibility, and security tests.
- Live sponsor smoke tests in a protected CI environment; fallback tests remain separate.
- At least 100 blind, mutation-generated, and practitioner-reviewed cases across rule families.
- Inter-rater agreement for disputed legal labels.
- Model/version regression gates.
- External penetration test and threat-model review.
- Disaster-recovery and audit-verifier drills.
- Usability study with documentary-credit examiners measuring review time, error interception, and trust calibration.

## 5.1 Verification matrix

| Risk | Required verification |
|---|---|
| Hard invariant | Unit tests plus property test proving no failed deterministic check yields a compliant decision |
| Amendment safety | TLA+/Alloy invariant check plus generated sequence tests |
| Join safety | SQL fixture/property tests with many amendments, aliases, ownership edges, and duplicate source rows |
| Sponsor truth | Live smoke test and visible observed receipt; separate fallback test |
| NIM structure | Guided-schema tests, malformed response tests, citation allowlist, prompt-injection corpus |
| Evidence integrity | Mutation tests for every leaf type and standalone proof verification |
| Human gate | Authentication, role, dual-control, stale-decision, replay, concurrency, and idempotency tests |
| Browser workflow | Playwright end-to-end test of SSE, evidence linking, approval, and receipt |
| Accessibility | Axe/WCAG automated checks plus keyboard and screen-reader manual pass |
| Performance | p50/p95 stage latency, concurrent cases, source timeout, retry, and degraded-mode tests |
| Evaluation claims | Frozen blind dataset, raw outputs, reproducible runner, confidence intervals, and error analysis |

## 5.2 Repository commands and CI policy

Existing verification:

```powershell
.\.venv\Scripts\pytest.exe apps/api/tests/ -v
Set-Location apps/web
npm run build
```

Add:

```powershell
ruff check apps/api
mypy apps/api
.\.venv\Scripts\pytest.exe apps/api/tests/property -v
.\.venv\Scripts\pytest.exe apps/api/tests/contract -v
.\.venv\Scripts\pytest.exe apps/api/tests/integration -v -m live_sponsors
Set-Location apps/web
npx playwright test
npx playwright test --grep accessibility
Set-Location ../..
graphify update .
```

CI must fail on lint errors; the current `ruff check ... || echo` pattern suppresses enforcement and should be removed.

## 5.3 Definition of “commercial-grade” for this project

Do not use “production-ready,” “bank-ready,” “live OCR,” “empirical,” “cryptographically signed,” or “dispatched” unless the corresponding acceptance condition is met:

| Claim | Minimum evidence |
|---|---|
| Production-ready | Security, resilience, observability, recovery, authorization, persistence, and deployment controls tested |
| Bank-ready | Practitioner/legal review, bank-policy configuration, SWIFT/channel validation, audit and access controls |
| Live OCR/VLM | Actual source artifact sent to an observed model endpoint with request/model provenance |
| Empirical benchmark | Actual architecture runs on a frozen blind dataset with raw outputs and reproducible metrics |
| Cryptographically signed | Private-key signature verified against trusted public-key identity; a timestamp-derived string is not a signature |
| Dispatched | Downstream adapter acknowledgment tied to an outbox message and artifact hash |
| Cached replay | Previously observed provider response with immutable provenance; a handcrafted fallback is not a cache |

---

# Recommended winning narrative

VERITAS-600 should not claim to replace the examiner. It should claim to make the examiner’s decision **faster to assemble, harder to corrupt, easier to challenge, and impossible to execute without accountable authority**.

The differentiator is not “we used four sponsors.” It is that each sponsor occupies a necessary architectural layer:

- Zetaris supplies governed, in-place evidence across fragmented data.
- Meterless supplies state, memory, and context discipline.
- NVIDIA Nemotron supplies constrained semantic judgment where rules alone are brittle.
- Cursor supplies the rule-governed engineering workflow that keeps those boundaries intact.

The system wins Track 03 when a judge can inspect one decision and answer all of these questions:

1. Which source fact caused it?
2. Which legal or policy rule consumed that fact?
3. Which computation was deterministic and which judgment was neural?
4. Could the neural result override a failed deterministic rule? **No.**
5. Which amendment state was active, and why?
6. Which external data sources were live, fresh, and actually queried?
7. What did the human approve, under which identity, and was anything dispatched?
8. Can the entire decision be replayed and cryptographically verified?

When all eight answers are visible and true, VERITAS-600 becomes more than an impressive prototype. It becomes a credible architecture for high-stakes, evidence-bound agentic decisioning.

---

## Source register

- [Open Agent Hackathon 2026 — event, Track 03, scoring, rules, and submission requirements](https://hackathon.genai.works/event/open-agent-hackathon-2026)
- [Open Agent Hackathon 2026 — GenAI Academy course](https://academy.genai.works/courses/open-agent-hackathon-2026/details)
- [Zetaris — connecting file, logical/JDBC, stream, and REST sources](https://kbase.zetaris.com/knowledge/connect)
- [Zetaris — query-in-place and zero-data-movement architecture](https://www.zetaris.com/zetaris-meta-data-lakehouse)
- [Meterless — official engine architecture, references, and conformance suites](https://github.com/Meterless/Meterless)
- [Meterless — local-first context architecture](https://github.com/Meterless/Meterless/blob/main/docs/architecture/local-first-agentic-context.md)
- [NVIDIA NIM — structured generation and guided JSON](https://docs.nvidia.com/nim/large-language-models/1.14.0/structured-generation.html)
- [NVIDIA NIM — OpenAI-compatible API reference](https://docs.nvidia.com/nim/large-language-models/1.12.0/api-reference.html)
- [Cursor — Rules, AGENTS.md, and legacy `.cursorrules`](https://docs.cursor.com/context/rules-for-ai)
- [ICC Digital Library — UCP 600 rules](https://library.iccwbo.org/content/tfb/RULES/tfb-ucp600-rules.htm?AGENT=ICC_FIN)
- [RFC 8785 — JSON Canonicalization Scheme](https://www.rfc-editor.org/rfc/rfc8785)
- [RFC 9162 — Merkle tree inclusion and consistency proofs](https://www.rfc-editor.org/rfc/rfc9162)
