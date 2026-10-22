# Graph Report - VERITAS-600  (2026-10-22)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 377 nodes · 684 edges · 28 communities (13 shown, 15 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 77 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a0cae1db`
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

## God Nodes (most connected - your core abstractions)
1. `BaselineComparisonSuite` - 24 edges
2. `AmendmentMemoryEngine` - 18 edges
3. `ZetarisFederationClient` - 16 edges
4. `NvidiaNimClient` - 16 edges
5. `compilerOptions` - 16 edges
6. `UCP600LegalAdjudicator` - 15 edges
7. `UCP600DeterministicEngine` - 14 edges
8. `MeterlessRouter` - 13 edges
9. `DocumentExtractor` - 13 edges
10. `DeterministicEvaluation` - 10 edges

## Surprising Connections (you probably didn't know these)
- `BaselineComparisonSuite` --uses--> `UCP600DeterministicEngine`  [INFERRED]
  apps/api/evals/compare_baselines.py → apps/api/engines/ucp600_deterministic.py
- `BaselineComparisonSuite` --uses--> `AmendmentMemoryEngine`  [INFERRED]
  apps/api/evals/compare_baselines.py → apps/api/memory/amendment_memory.py
- `BaselineComparisonSuite` --uses--> `MeterlessRouter`  [INFERRED]
  apps/api/evals/compare_baselines.py → apps/api/inference/meterless_router.py
- `router()` --uses--> `MeterlessRouter`  [INFERRED]
  apps/api/tests/test_legal_adjudicator.py → apps/api/inference/meterless_router.py
- `BaselineComparisonSuite` --uses--> `BankDecisionEngine`  [INFERRED]
  apps/api/evals/compare_baselines.py → apps/api/engines/decision_engine.py

## Import Cycles
- None detected.

## Communities (28 total, 15 thin omitted)

### Community 0 - "AmendmentMemoryEngine"
Cohesion: 0.09
Nodes (14): parse_date(), UCP600DeterministicEngine, AmendmentMemoryEngine, memory_engine(), test_art_10_c_full_implicit_acceptance(), test_art_10_e_partial_acceptance_prohibition(), test_scenario_1_amendment_lifecycle(), det_engine() (+6 more)

### Community 1 - "app/page.tsx"
Cohesion: 0.08
Nodes (17): EVALUATION_DATASET, EvaluationRow, metadata, TerminalPage(), AdjudicationMatrixPane(), AdjudicationMatrixPaneProps, DecisionActionPane(), DecisionActionPaneProps (+9 more)

### Community 2 - "main.py"
Cohesion: 0.10
Nodes (4): get_settings(), Settings, AmendmentResolution, TermRecord

### Community 3 - "test_legal_adjudicator.py"
Cohesion: 0.11
Nodes (12): BankDecisionEngine, DeterministicCheckResult, DeterministicEvaluation, LegalAdjudicationResult, LegalFinding, UCP600LegalAdjudicator, adjudicator(), extractor() (+4 more)

### Community 4 - "package.json"
Cohesion: 0.06
Nodes (33): dependencies, clsx, lucide-react, next, react, react-dom, tailwind-merge, devDependencies (+25 more)

### Community 5 - "BaselineComparisonSuite"
Cohesion: 0.14
Nodes (10): ArchitectureResult, BaselineComparisonSuite, main(), ScenarioBenchmarkRow, get_evals_results(), run_evals_benchmark(), test_baseline_suite_loads_all_10_scenarios(), test_regex_baseline_failure_modes() (+2 more)

### Community 6 - "ZetarisFederationClient"
Cohesion: 0.13
Nodes (6): test_join_safe_single_row_guarantee(), test_scenario_1_wrongful_dishonor_amendment_quarantine(), test_scenario_2_cotton_yarn_benchmark(), test_scenario_3_tbml_price_anomaly_and_sanctions_freeze(), zetaris_client(), ZetarisFederationClient

### Community 7 - "NvidiaNimClient"
Cohesion: 0.15
Nodes (5): DocumentExtractionResult, DocumentExtractor, ExtractedField, NvidiaNimClient, test_document_extractor_bounding_boxes()

### Community 8 - "examine_presentation_sse"
Cohesion: 0.11
Nodes (7): approve_human_action(), examine_presentation_sse(), get_scenario_details(), health_check(), HumanSignOffRequest, list_scenarios(), load_presentation_data()

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

## Knowledge Gaps
- **10 isolated node(s):** `autoprefixer`, `clsx`, `postcss`, `react-dom`, `tailwind-merge` (+5 more)
  These have ≤1 connection - possible missing edges. (Counts symbols only; 201 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ZetarisFederationClient` connect `ZetarisFederationClient` to `AmendmentMemoryEngine`, `main.py`, `BaselineComparisonSuite`?**
  _High betweenness centrality (0.059) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `BaselineComparisonSuite` (e.g. with `BankDecisionEngine` and `UCP600DeterministicEngine`) actually correct?**
  _`BaselineComparisonSuite` has 9 INFERRED edges - model-reasoned connections that need verification._
- **What connects `autoprefixer`, `clsx`, `postcss` to the rest of the system?**
  _10 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `AmendmentMemoryEngine` be split into smaller, more focused modules?**
  _Cohesion score 0.08902439024390243 - nodes in this community are weakly interconnected._
- **Why does `BaselineComparisonSuite` connect `BaselineComparisonSuite` to `AmendmentMemoryEngine`, `main.py`, `test_legal_adjudicator.py`, `ZetarisFederationClient`, `NvidiaNimClient`, `MeterlessRouter`?**
  _High betweenness centrality (0.058) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `AmendmentMemoryEngine` (e.g. with `BaselineComparisonSuite` and `memory_engine()`) actually correct?**
  _`AmendmentMemoryEngine` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Should `app/page.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.08292682926829269 - nodes in this community are weakly interconnected._