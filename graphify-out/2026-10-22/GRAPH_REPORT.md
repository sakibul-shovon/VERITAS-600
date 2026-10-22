# Graph Report - VERITAS-600  (2026-10-22)

## Corpus Check
- 58 files · ~40,765 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 6, .example 1, .css 1)

## Summary
- 521 nodes · 832 edges · 34 communities (18 shown, 16 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 83 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `0e9ac83a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- AmendmentMemoryEngine
- app/page.tsx
- main.py
- test_legal_adjudicator.py
- package.json
- BaselineComparisonSuite
- ZetarisFederationClient
- NvidiaNimClient
- examine_presentation_sse
- compilerOptions
- test_end_to_end.py
- MeterlessRouter
- seed_scenarios.py
- BankDecision
- TokenBucketRateLimiter
- next.config.js
- VERITAS-600
- VERITAS-600: Lean Master Architecture & Engineering Execution Plan (v2 — Domain & SQL Hardened)
- VERITAS-600: Lean Master Architecture & Engineering Execution Plan (v2 — Domain & SQL Hardened)
- VERITAS-600: Lean Master Architecture & Engineering Execution Plan (v2 — Domain & SQL Hardened)
- AGENTS.md: Operational Instructions for Coding Agents
- pull_request_template.md

## God Nodes (most connected - your core abstractions)
1. `BaselineComparisonSuite` - 24 edges
2. `ZetarisFederationClient` - 22 edges
3. `AmendmentMemoryEngine` - 18 edges
4. `NvidiaNimClient` - 16 edges
5. `compilerOptions` - 16 edges
6. `UCP600LegalAdjudicator` - 15 edges
7. `UCP600DeterministicEngine` - 14 edges
8. `DocumentExtractor` - 13 edges
9. `MeterlessRouter` - 13 edges
10. `DeterministicEvaluation` - 10 edges

## Surprising Connections (you probably didn't know these)
- `2.1 Zetaris: In-Situ Federated Data Layer` --references--> `ZetarisFederationClient`  [INFERRED]
  doc/plan.md → apps/api/zetaris/client.py
- `2.3 Mandatory Sponsor Integrations` --references--> `ZetarisFederationClient`  [INFERRED]
  doc/plan.md → apps/api/zetaris/client.py
- `2.1 Zetaris: In-Situ Federated Data Layer` --references--> `ZetarisFederationClient`  [INFERRED]
  docs/plan.md → apps/api/zetaris/client.py
- `2.3 Mandatory Sponsor Integrations` --references--> `ZetarisFederationClient`  [INFERRED]
  docs/plan.md → apps/api/zetaris/client.py
- `2.1 Zetaris: In-Situ Federated Data Layer` --references--> `ZetarisFederationClient`  [INFERRED]
  plan.md → apps/api/zetaris/client.py

## Import Cycles
- None detected.

## Communities (34 total, 16 thin omitted)

### Community 0 - "AmendmentMemoryEngine"
Cohesion: 0.08
Nodes (14): parse_date(), UCP600DeterministicEngine, AmendmentMemoryEngine, AmendmentResolution, memory_engine(), test_art_10_c_full_implicit_acceptance(), test_art_10_e_partial_acceptance_prohibition(), det_engine() (+6 more)

### Community 1 - "app/page.tsx"
Cohesion: 0.08
Nodes (17): EVALUATION_DATASET, EvaluationRow, metadata, TerminalPage(), AdjudicationMatrixPane(), AdjudicationMatrixPaneProps, DecisionActionPane(), DecisionActionPaneProps (+9 more)

### Community 2 - "main.py"
Cohesion: 0.10
Nodes (4): get_settings(), Settings, TermRecord, test_scenario_1_amendment_lifecycle()

### Community 3 - "test_legal_adjudicator.py"
Cohesion: 0.11
Nodes (12): BankDecisionEngine, DeterministicCheckResult, DeterministicEvaluation, LegalAdjudicationResult, LegalFinding, UCP600LegalAdjudicator, adjudicator(), extractor() (+4 more)

### Community 4 - "package.json"
Cohesion: 0.06
Nodes (33): dependencies, clsx, lucide-react, next, react, react-dom, tailwind-merge, devDependencies (+25 more)

### Community 5 - "BaselineComparisonSuite"
Cohesion: 0.15
Nodes (10): ArchitectureResult, BaselineComparisonSuite, main(), ScenarioBenchmarkRow, get_evals_results(), run_evals_benchmark(), test_baseline_suite_loads_all_10_scenarios(), test_regex_baseline_failure_modes() (+2 more)

### Community 6 - "ZetarisFederationClient"
Cohesion: 0.13
Nodes (6): test_join_safe_single_row_guarantee(), test_scenario_1_wrongful_dishonor_amendment_quarantine(), test_scenario_2_cotton_yarn_benchmark(), test_scenario_3_tbml_price_anomaly_and_sanctions_freeze(), zetaris_client(), ZetarisFederationClient

### Community 7 - "NvidiaNimClient"
Cohesion: 0.15
Nodes (5): DocumentExtractionResult, DocumentExtractor, ExtractedField, NvidiaNimClient, test_document_extractor_bounding_boxes()

### Community 8 - "examine_presentation_sse"
Cohesion: 0.10
Nodes (8): approve_human_action(), examine_presentation_sse(), extract_documents(), get_scenario_details(), health_check(), HumanSignOffRequest, list_scenarios(), load_presentation_data()

### Community 9 - "compilerOptions"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 10 - "test_end_to_end.py"
Cohesion: 0.17
Nodes (6): client(), test_api_health_and_telemetry(), test_api_scenarios_list(), test_e2e_scenario_1_wrongful_dishonor_prevention(), test_e2e_scenario_2_curable_mt734_and_demurrage_save(), test_e2e_scenario_3_tbml_sanctions_freeze()

### Community 11 - "MeterlessRouter"
Cohesion: 0.21
Nodes (4): MeterlessContextPacket, MeterlessRouter, TokenTelemetry, test_meterless_router_markovian_chunks()

### Community 12 - "seed_scenarios.py"
Cohesion: 0.26
Nodes (4): main(), seed_customs_parquet(), seed_duckdb_standby(), seed_presentation_files()

### Community 28 - "VERITAS-600"
Cohesion: 0.05
Nodes (34): 1. High-Level Architecture Overview, 2.1 Frontend & User Experience, 2.2 Backend & Core Services, 2.3 Mandatory Sponsor Integrations, 2.4 Deterministic & Symbolic Engines (Python), 2. Detailed Stack Components, 3. Environment & Deployment Footprint, 8. Definition of Done (Pre-Submission Checklist) (+26 more)

### Community 29 - "VERITAS-600: Lean Master Architecture & Engineering Execution Plan (v2 — Domain & SQL Hardened)"
Cohesion: 0.06
Nodes (33): 1.1 Target User & The High-Stakes Problem, 1. High-Level Architecture Overview, 1. System Vision & Operational Problem, 2.1 Frontend & User Experience, 2.1 Zetaris: In-Situ Federated Data Layer, 2.2 Backend & Core Services, 2.2 Meterless: Context Routing, Stateful Memory & Inference Control, 2.3 Mandatory Sponsor Integrations (+25 more)

### Community 30 - "VERITAS-600: Lean Master Architecture & Engineering Execution Plan (v2 — Domain & SQL Hardened)"
Cohesion: 0.06
Nodes (33): 1.1 Target User & The High-Stakes Problem, 1. High-Level Architecture Overview, 1. System Vision & Operational Problem, 2.1 Frontend & User Experience, 2.1 Zetaris: In-Situ Federated Data Layer, 2.2 Backend & Core Services, 2.2 Meterless: Context Routing, Stateful Memory & Inference Control, 2.3 Mandatory Sponsor Integrations (+25 more)

### Community 31 - "VERITAS-600: Lean Master Architecture & Engineering Execution Plan (v2 — Domain & SQL Hardened)"
Cohesion: 0.08
Nodes (24): 1.1 Target User & The High-Stakes Problem, 1. System Vision & Operational Problem, 2.1 Zetaris: In-Situ Federated Data Layer, 2.2 Meterless: Context Routing, Stateful Memory & Inference Control, 2.3 NVIDIA Nemotron: Multimodal Extraction & Legal Adjudication, 2.4 Cursor: AI-Native Development Workflow, 2. Mandatory Sponsor Stack (Transparent, Load-Bearing Integration), 3. Core Technical Differentiation (The 3 Pillars) (+16 more)

### Community 32 - "AGENTS.md: Operational Instructions for Coding Agents"
Cohesion: 0.25
Nodes (7): 1. Prime Directive & Ground Truth, 2. Inviolable Architectural Invariants, 3. Repository Structure, 4. Verification & Testing Commands, 5. Sponsor Integration Standards, AGENTS.md: Operational Instructions for Coding Agents, graphify

## Knowledge Gaps
- **10 isolated node(s):** `clsx`, `react-dom`, `tailwind-merge`, `@types/node`, `@types/react` (+5 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 303 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **16 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ZetarisFederationClient` connect `ZetarisFederationClient` to `AmendmentMemoryEngine`, `main.py`, `BaselineComparisonSuite`, `VERITAS-600`, `VERITAS-600: Lean Master Architecture & Engineering Execution Plan (v2 — Domain & SQL Hardened)`, `VERITAS-600: Lean Master Architecture & Engineering Execution Plan (v2 — Domain & SQL Hardened)`, `VERITAS-600: Lean Master Architecture & Engineering Execution Plan (v2 — Domain & SQL Hardened)`?**
  _High betweenness centrality (0.326) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `BaselineComparisonSuite` (e.g. with `BankDecisionEngine` and `UCP600DeterministicEngine`) actually correct?**
  _`BaselineComparisonSuite` has 9 INFERRED edges - model-reasoned connections that need verification._
- **What connects `clsx`, `react-dom`, `tailwind-merge` to the rest of the system?**
  _10 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `AmendmentMemoryEngine` be split into smaller, more focused modules?**
  _Cohesion score 0.08367071524966262 - nodes in this community are weakly interconnected._
- **Why does `2.1 Zetaris: In-Situ Federated Data Layer` connect `VERITAS-600: Lean Master Architecture & Engineering Execution Plan (v2 — Domain & SQL Hardened)` to `ZetarisFederationClient`?**
  _High betweenness centrality (0.092) - this node is a cross-community bridge._
- **Are the 12 inferred relationships involving `ZetarisFederationClient` (e.g. with `BaselineComparisonSuite` and `test_join_safe_single_row_guarantee()`) actually correct?**
  _`ZetarisFederationClient` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Should `app/page.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.07862679955703211 - nodes in this community are weakly interconnected._