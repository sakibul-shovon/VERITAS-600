# Graph Report - VERITAS-600  (2026-10-24)

## Corpus Check
- 92 files · ~100,522 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 10 file(s) not represented in the graph (top: (none) 6, .example 1, .css 1)

## Summary
- 1295 nodes · 2098 edges · 115 communities (92 shown, 23 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 207 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c281f0bd`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- AmendmentMemoryEngine
- Category P0: Correctness & Logic Bugs
- 2. Detailed Remediations by Vulnerability
- output
- package.json
- BaselineComparisonSuite
- BankDecisionEngine
- DocumentExtractor
- test_audit_fixes.py
- compilerOptions
- test_document_intake.py
- .compute_telemetry
- seed_scenarios.py
- hash_chain.py
- .execute_federated_check
- next.config.js
- load_presentation_data
- examine/page.tsx
- VERITAS-600: Lean Master Architecture & Engineering Execution Plan (v2 — Domain & SQL Hardened)
- VERITAS-600: Lean Master Architecture & Engineering Execution Plan (v2 — Domain & SQL Hardened)
- VERITAS-600: Lean Master Architecture & Engineering Execution Plan (v2 — Domain & SQL Hardened)
- AGENTS.md: Operational Instructions for Coding Agents
- pull_request_template.md
- HACKATHON_ARCHITECTURE_ELEVATION.md
- 3. The Frontier Reasoning Upgrade
- test_legal_adjudicator.py
- 4. The Palantir-Grade Visual Blueprint
- compare_baselines.py
- 2. Detailed Stack Components
- Phase P0 — Demo integrity and truthfulness
- types.ts
- 15.2 `/examine` — Examination terminal
- MerkleTree
- LANDING PAGE — CREATIVE DIRECTION & IMPLEMENTATION BLUEPRINT
- NvidiaNimClient
- 14. Complete Light/Dark Design System
- ucp600_rules.py
- Phase P1 — Verifiable state, audit, and authorization
- 2.1 What is already unusually strong
- 27. Implementation Phases and Dependency Order
- ZetarisFederationClient
- VERITAS-600 UI/UX Redesign Blueprint
- 20. Frontend Architecture and Component System
- 30. Source References and Research Notes
- 13. Brand and Visual Identity
- 21. Responsive and Accessibility Strategy
- 29. Final Design Quality Checklist
- 9. Target Users and UX Research
- Money
- CaseStore
- 2. Mandatory Sponsor Stack (Transparent, Load-Bearing Integration)
- main.py
- 16. Agentic Interaction and Reasoning Visualization
- 26. Testing and Acceptance Criteria
- 3. Existing Functionality Inventory
- Phase P3 — Federated risk and sponsor proof
- RunHashChain
- 7. Phase-by-Phase Execution Plan
- Phase P2 — Rule coverage and zero-hallucination controls
- 5. Concrete Implementation Plan
- 10. Information Architecture and User Journeys
- 11. Three Creative Directions
- 17. Motion Design Language
- 19. Recommended Libraries and MCP Servers
- 22. Performance Engineering Strategy
- 23. Hackathon Judge Experience
- 25. Functional Preservation and Migration Strategy
- LP-11. Typography, Color, Spacing, and Visual Assets
- LP-3. Three Alternative Creative Concepts
- LP-13. Navigation and CTA Strategy
- LP-4. Three Hero Concepts and Comparison
- VERITAS-600
- 2.2 Verifiable Domain Models & Cryptographic Proof Chain (Phase P1)
- 24. File-by-File Implementation Blueprint
- 2. Mandatory Sponsor Stack (Transparent, Load-Bearing Integration)
- LP-17. Accessibility and Performance Requirements
- LP-1. Landing-Page Objectives and Target Audience
- LP-14. Landing-to-Application Transitions
- LP-19. Visual and Interaction Testing Strategy
- LP-9. Guided Product Demonstration Concept
- lucide-react
- LP-8. Hero Composition and Interactive Behavior
- LP-10. Detailed Scroll and Motion Choreography
- MissionControl.tsx
- 4. Hackathon Context and Verified Requirements
- 5. Track Selection and Rationale
- test_security_redteam_fixes.py
- 2. Detailed Stack Components
- evals/page.tsx
- 2. Repository Analysis and Product Understanding
- api.ts
- 12. Selected Art Direction and Design Rationale
- AuditVerifier
- 2.1 What is already unusually strong
- ⚡ Quickstart (Local Development)
- VERITAS-600: Project Execution & Agent Continuity Tracker
- VERITAS-600 Security Red Team Remediation Report
- LP-12. Light and Dark Theme Specifications
- 3. Core Technical Differentiation (The 3 Pillars)
- 6. Contemporary UI/UX Research (Through October 2026)
- LP-16. React Component Architecture

## God Nodes (most connected - your core abstractions)
1. `LANDING PAGE — CREATIVE DIRECTION & IMPLEMENTATION BLUEPRINT` - 36 edges
2. `ZetarisFederationClient` - 29 edges
3. `CaseStore` - 26 edges
4. `DocumentExtractor` - 26 edges
5. `BaselineComparisonSuite` - 24 edges
6. `NvidiaNimClient` - 23 edges
7. `AmendmentMemoryEngine` - 23 edges
8. `UCP600LegalAdjudicator` - 22 edges
9. `UCP600DeterministicEngine` - 21 edges
10. `Money` - 19 edges

## Surprising Connections (you probably didn't know these)
- `P2-6 & P2-8 & P2-11: Concurrency & Fault Tolerance` --references--> `CaseStore`  [INFERRED]
  SECURITY_REMEDIATION_REPORT.md → apps/api/cases/store.py
- `7. Fix roadmap (ordered, cheapest first)` --references--> `ActionType`  [INFERRED]
  SECURITY_RED_TEAM_REPORT.md → apps/api/domain/decisions.py
- `1. What the system does (one paragraph)` --references--> `BankDecisionEngine`  [INFERRED]
  SECURITY_RED_TEAM_REPORT.md → apps/api/engines/decision_engine.py
- `2.2 Critical findings: fix before presenting the system as live` --references--> `DocumentExtractor`  [INFERRED]
  HACKATHON_ARCHITECTURE_ELEVATION.md → apps/api/engines/document_extractor.py
- `2.4 Present implementation truth and limitations` --references--> `DocumentExtractor`  [INFERRED]
  ui-redesign.md → apps/api/engines/document_extractor.py

## Import Cycles
- None detected.

## Communities (115 total, 23 thin omitted)

### Community 0 - "AmendmentMemoryEngine"
Cohesion: 0.06
Nodes (23): parse_date(), UCP600DeterministicEngine, AmendmentMemoryEngine, AmendmentResolution, memory_engine(), test_art_10_c_full_implicit_acceptance(), test_art_10_e_partial_acceptance_prohibition(), test_scenario_1_amendment_lifecycle() (+15 more)

### Community 1 - "Category P0: Correctness & Logic Bugs"
Cohesion: 0.06
Nodes (28): test_safe_parse_json_markdown_stripping(), 1. Executive Summary, 2. Inviolable Architectural Invariants Checklist, 3.10. Settlement Voucher Pre-Signoff Status, 3.11. UI Dispatch Status Transparency, 3.12. Honest Health & Telemetry Reporting, 3.17. CI DuckDB Pre-Seeding, 3.18. Unmasked Ruff Lint Verification (+20 more)

### Community 2 - "2. Detailed Remediations by Vulnerability"
Cohesion: 0.09
Nodes (17): ArtifactGenerator, sanitize_swift_text(), BankDecision, normalize_trade_text(), test_settlement_voucher_pending_vs_authorized_status(), test_sanitize_swift_text_strips_delimiters_and_tags(), 2. Detailed Remediations by Vulnerability, P0-1: Human Sign-Off Gate Hardening & Evidence Binding (+9 more)

### Community 3 - "output"
Cohesion: 0.11
Nodes (18): ignore, customPatterns, useGitignore, include, output, compress, filePath, parsableStyle (+10 more)

### Community 4 - "package.json"
Cohesion: 0.06
Nodes (33): dependencies, clsx, lucide-react, next, react, react-dom, tailwind-merge, devDependencies (+25 more)

### Community 5 - "BaselineComparisonSuite"
Cohesion: 0.09
Nodes (19): ArchitectureResult, BaselineComparisonSuite, main(), ScenarioBenchmarkRow, get_evals_results(), run_evals_benchmark(), test_baseline_suite_loads_all_10_scenarios(), test_regex_baseline_failure_modes() (+11 more)

### Community 7 - "DocumentExtractor"
Cohesion: 0.19
Nodes (5): DocumentExtractionResult, DocumentExtractor, ExtractedField, test_document_extractor_bounding_boxes(), P1-3. Upload bombs: PDF decompression + all-pages reads; PIL pixel bombs

### Community 8 - "test_audit_fixes.py"
Cohesion: 0.20
Nodes (7): ActionType, AuthorityLevel, DecisionReceipt, DispatchStatus, approve_human_action(), test_keyed_hmac_decision_receipt_and_verifier(), test_decision_receipt_cryptographic_verification()

### Community 9 - "compilerOptions"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 10 - "test_document_intake.py"
Cohesion: 0.09
Nodes (14): case_payload(), client(), make_text_pdf(), test_approval_rejects_missing_and_stale_run_bindings(), test_image_upload_never_falls_back_to_fixture_ocr(), test_real_pdf_evidence_flows_into_calculations(), test_scanned_pdf_is_rendered_for_vision_without_fixture_fallback(), test_user_case_acceptance_requires_complete_document_set() (+6 more)

### Community 11 - ".compute_telemetry"
Cohesion: 0.20
Nodes (4): MeterlessContextPacket, MeterlessRouter, TokenTelemetry, test_meterless_router_markovian_chunks()

### Community 12 - "seed_scenarios.py"
Cohesion: 0.26
Nodes (4): main(), seed_customs_parquet(), seed_duckdb_standby(), seed_presentation_files()

### Community 13 - "hash_chain.py"
Cohesion: 0.18
Nodes (5): _canonical_default(), canonical_sha256(), canonicalize_json(), ChainEvent, test_canonical_json_determinism()

### Community 22 - "load_presentation_data"
Cohesion: 0.07
Nodes (17): accept_case_evidence(), CaseCreateRequest, create_case(), EvidenceAcceptanceRequest, extract_documents(), get_case_document_content(), get_scenario_details(), get_sponsor_evidence() (+9 more)

### Community 28 - "examine/page.tsx"
Cohesion: 0.23
Nodes (13): ExaminationPage(), HeaderBar(), NewCaseDialog(), NoticeRegion(), NoticeRegionProps, ZetarisDrawer(), fetchHealth(), fetchScenarioDetails() (+5 more)

### Community 29 - "VERITAS-600: Lean Master Architecture & Engineering Execution Plan (v2 — Domain & SQL Hardened)"
Cohesion: 0.06
Nodes (33): 1.1 Target User & The High-Stakes Problem, 1. High-Level Architecture Overview, 1. System Vision & Operational Problem, 2.1 Frontend & User Experience, 2.1 Zetaris: In-Situ Federated Data Layer, 2.2 Backend & Core Services, 2.2 Meterless: Context Routing, Stateful Memory & Inference Control, 2.3 Mandatory Sponsor Integrations (+25 more)

### Community 30 - "VERITAS-600: Lean Master Architecture & Engineering Execution Plan (v2 — Domain & SQL Hardened)"
Cohesion: 0.13
Nodes (15): 1.1 Target User & The High-Stakes Problem, 1. System Vision & Operational Problem, 4. The 3 Flagship Golden Scenarios (Realistic, Deeply Verifiable Data), 5. Repository Structure, 6.1 PostgreSQL Schema (`apps/api/db/schema.sql`), 6.2 Join-Safe Zetaris 3-Silo Federated Query (`apps/api/zetaris/sql/federated_check.sql`), 6. Database & Join-Safe Federated Query Specifications, 7. Phase-by-Phase Execution Plan (+7 more)

### Community 31 - "VERITAS-600: Lean Master Architecture & Engineering Execution Plan (v2 — Domain & SQL Hardened)"
Cohesion: 0.17
Nodes (12): 1.1 Target User & The High-Stakes Problem, 1. System Vision & Operational Problem, 3. Core Technical Differentiation (The 3 Pillars), 4. The 3 Flagship Golden Scenarios (Realistic, Deeply Verifiable Data), 5. Repository Structure, 6.1 PostgreSQL Schema (`apps/api/db/schema.sql`), 6.2 Join-Safe Zetaris 3-Silo Federated Query (`apps/api/zetaris/sql/federated_check.sql`), 6. Database & Join-Safe Federated Query Specifications (+4 more)

### Community 32 - "AGENTS.md: Operational Instructions for Coding Agents"
Cohesion: 0.22
Nodes (8): 1. Prime Directive & Ground Truth, 2. Inviolable Architectural Invariants, 3. Repository Structure, 4. Verification & Testing Commands, 5. Sponsor Integration Standards, 6. Repomix Whole-Repository Context Compression, AGENTS.md: Operational Instructions for Coding Agents, graphify

### Community 34 - "HACKATHON_ARCHITECTURE_ELEVATION.md"
Cohesion: 0.18
Nodes (10): 1.1 Official Track 03 framing and scoring, 1.2 Sponsor strategy: published capability versus winning proof, 1.3 Evidence-based readiness score, 1.4 Five-second judge comprehension contract, 1. Hackathon and Sponsor Strategy Matrix, Executive verdict, Recommended winning narrative, Source register (+2 more)

### Community 35 - "3. The Frontier Reasoning Upgrade"
Cohesion: 0.10
Nodes (20): 3.10 Human authorization and safe dispatch, 3.11 Reliability, security, and operations, 3.1 Target architecture: an evidence-carrying decision pipeline, 3.2 Evidence model and cryptographic proof chain, 3.3 Formal amendment state machine, 3.4 Deterministic kernel and legal rule registry, 3.5 Fail-closed semantic adjudication, 3.6 Expanded legal and documentary edge-case matrix (+12 more)

### Community 36 - "test_legal_adjudicator.py"
Cohesion: 0.14
Nodes (10): DeterministicEvaluation, LegalFinding, UCP600LegalAdjudicator, adjudicator(), extractor(), router(), test_consignee_address_mutation_art_14_j(), test_hard_invariant_rule_enforcement() (+2 more)

### Community 37 - "4. The Palantir-Grade Visual Blueprint"
Cohesion: 0.11
Nodes (18): 4.1 Design principles, 4.2 Visual system, 4.3 Information architecture, 4.4 Synchronized document viewer, 4.5 Dynamic reasoning matrix, 4.6 Decision pane and tactile authorization, 4.7 Motion and micro-interactions, 4.8 Demo choreography: 150 seconds (+10 more)

### Community 39 - "2. Detailed Stack Components"
Cohesion: 0.20
Nodes (9): 1. High-Level Architecture Overview, 2.1 Frontend & User Experience, 2.2 Backend & Core Services, 2.3 Mandatory Sponsor Integrations, 2.4 Deterministic & Symbolic Engines (Python), 2. Detailed Stack Components, 3. Environment & Deployment Footprint, 8. Definition of Done (Pre-Submission Checklist) (+1 more)

### Community 40 - "Phase P0 — Demo integrity and truthfulness"
Cohesion: 0.22
Nodes (9): `apps/api/engines/document_extractor.py`, `apps/api/evals/compare_baselines.py`, `apps/api/inference/meterless_router.py`, `apps/api/inference/nim_client.py`, `apps/api/main.py`, `apps/web/src/components/DocumentViewerPane.tsx`, `apps/web/src/lib/api.ts`, P0 acceptance gates (+1 more)

### Community 41 - "types.ts"
Cohesion: 0.18
Nodes (14): AdjudicationMatrixPaneProps, DecisionActionPaneProps, HeaderBarProps, ExaminationAction, ExaminationPhase, ExaminationState, initialExaminationState, BankDecision (+6 more)

### Community 42 - "15.2 `/examine` — Examination terminal"
Cohesion: 0.11
Nodes (19): 15.1 Global shell, 15.2 `/examine` — Examination terminal, 15.3 `/evals` — Architecture benchmark, 15.4 Proof drawers and dialogs, 15.5 Judge handoff inside the terminal, 15. Page-by-Page Redesign Specifications, Benchmark run behavior, Case-specific narrative (+11 more)

### Community 43 - "MerkleTree"
Cohesion: 0.18
Nodes (5): MerkleTree, examine_presentation_sse(), event_generator(), test_merkle_tree_root_and_inclusion_proof(), P1-1. Event-loop blocking: sync LLM calls + `time.sleep` inside async SSE → whole-server stall

### Community 44 - "LANDING PAGE — CREATIVE DIRECTION & IMPLEMENTATION BLUEPRINT"
Cohesion: 0.10
Nodes (20): 18. Animation and Visualization Technology Decisions, 28. Risks, Tradeoffs, and Mitigations, Acceptance gate, Accepted trade-offs, Chosen stack, Desktop, 1440 px reference, Evaluated alternatives, Landing acceptance criteria (+12 more)

### Community 45 - "NvidiaNimClient"
Cohesion: 0.14
Nodes (5): NvidiaNimClient, test_benign_word_omitted_does_not_falsely_trigger_discrepancy(), test_divergent_goods_fail_closed_offline_replay(), test_nemotron_lru_cache_bounded_at_max_entries(), 2. Executive verdict

### Community 46 - "14. Complete Light/Dark Design System"
Cohesion: 0.25
Nodes (8): 14.1 Theme tokens, 14.2 Type scale, 14.3 Spacing, geometry, and elevation, 14.5 Component specification, 14.6 Status grammar, 14.7 Content rules, 14.8 Focus, selection, loading, and error behavior, 14. Complete Light/Dark Design System

### Community 47 - "ucp600_rules.py"
Cohesion: 0.29
Nodes (5): get_rule(), LegalRule, RuleCategory, RuleSeverity, test_rules_registry_lookup()

### Community 48 - "Phase P1 — Verifiable state, audit, and authorization"
Cohesion: 0.33
Nodes (6): `apps/api/db/schema.sql` plus migrations, Formal state specification, New audit modules, New domain modules, Phase P1 — Verifiable state, audit, and authorization, Property-based tests

### Community 49 - "2.1 What is already unusually strong"
Cohesion: 0.20
Nodes (10): 2.2 Critical findings: fix before presenting the system as live, 2.3 Architectural bottlenecks, 2.4 Real examiner workflow: what the product must support, 2.5 Quantifying impact without overstating it, 2. First-Principles Codebase Critique, Evaluation leakage, “Fail open” semantic behavior, Missing domain boundary (+2 more)

### Community 50 - "27. Implementation Phases and Dependency Order"
Cohesion: 0.20
Nodes (10): 27. Implementation Phases and Dependency Order, Phase A — Contract lock and characterization (0.5–1 day), Phase B — Route safety and foundations (1–1.5 days), Phase C — Landing product story (1.5–2 days), Phase D — State and data architecture (1–1.5 days), Phase E — Examination vertical slice (2–3 days), Phase F — Benchmark route (1 day), Phase G — Motion, proof polish, and performance (1 day) (+2 more)

### Community 51 - "ZetarisFederationClient"
Cohesion: 0.17
Nodes (6): test_join_safe_single_row_guarantee(), test_scenario_1_wrongful_dishonor_amendment_quarantine(), test_scenario_2_cotton_yarn_benchmark(), test_scenario_3_tbml_price_anomaly_and_sanctions_freeze(), zetaris_client(), ZetarisFederationClient

### Community 52 - "VERITAS-600 UI/UX Redesign Blueprint"
Cohesion: 0.22
Nodes (8): 1. Executive Design Vision, 7. Reference Study With Links, 8. Common AI-Generated Design Patterns to Avoid, Anti-Generic-AI checklist, Approved recurring motifs, Design principles, How to read this document, VERITAS-600 UI/UX Redesign Blueprint

### Community 53 - "20. Frontend Architecture and Component System"
Cohesion: 0.22
Nodes (9): 20.1 Target component hierarchy, 20.2 Server/client boundaries, 20.3 Data access layer, 20.4 Examination reducer, 20.5 SSE lifecycle, 20.6 Type model, 20.7 Theme architecture, 20.8 Error and observability design (+1 more)

### Community 54 - "30. Source References and Research Notes"
Cohesion: 0.22
Nodes (9): 30.1 Hackathon and track evidence, 30.2 Sponsor and platform sources, 30.3 Human–AI interaction and explainability, 30.4 Accessibility and performance standards, 30.5 Product and visual references, 30.6 Framework, library, and tooling sources, 30.7 Research classification and unresolved hypotheses, 30. Source References and Research Notes (+1 more)

### Community 55 - "13. Brand and Visual Identity"
Cohesion: 0.25
Nodes (8): 13. Brand and Visual Identity, Iconography, Imagery and texture, Mark and favicon, Naming hierarchy, Product position, Sonic and haptic identity, Typography

### Community 56 - "21. Responsive and Accessibility Strategy"
Cohesion: 0.25
Nodes (8): 21.1 Breakpoints by behavior, 21.2 Keyboard model, 21.3 Screen-reader semantics, 21.4 Visual accessibility, 21.5 Cognitive and operational accessibility, 21.6 Touch and mobile details, 21.7 Required manual accessibility checks, 21. Responsive and Accessibility Strategy

### Community 57 - "29. Final Design Quality Checklist"
Cohesion: 0.25
Nodes (8): 29. Final Design Quality Checklist, Design system, Human action, Landing page, Performance and quality, Product truth, Responsive and accessibility, Telemetry and evidence

### Community 58 - "9. Target Users and UX Research"
Cohesion: 0.25
Nodes (8): 9.1 Primary persona: senior documentary-credit examiner, 9.2 Secondary persona: compliance/AML officer, 9.3 Secondary persona: desk head / authorizer, 9.4 Secondary persona: hackathon judge, 9.5 Jobs to be done, 9.6 Research hypotheses to validate, 9.7 Measurable usability goals, 9. Target Users and UX Research

### Community 60 - "CaseStore"
Cohesion: 0.05
Nodes (37): CaseStore, TokenBucketRateLimiter, test_case_store_durable_approval_recording(), test_evidence_acceptance_rejects_dict_and_nan(), 3.13. CORS Configuration Hardening, 3.14. Thread-Safe Token Bucket Rate Limiting, 3.15. Cryptographic Signature Keying, 3.16. Durable Case Authorization Storage (+29 more)

### Community 61 - "2. Mandatory Sponsor Stack (Transparent, Load-Bearing Integration)"
Cohesion: 0.40
Nodes (5): 2.1 Zetaris: In-Situ Federated Data Layer, 2.2 Meterless: Context Routing, Stateful Memory & Inference Control, 2.3 NVIDIA Nemotron: Multimodal Extraction & Legal Adjudication, 2.4 Cursor: AI-Native Development Workflow, 2. Mandatory Sponsor Stack (Transparent, Load-Bearing Integration)

### Community 63 - "16. Agentic Interaction and Reasoning Visualization"
Cohesion: 0.29
Nodes (7): 16.1 Observable contract, not theatrical autonomy, 16.2 Five-stage decision spine, 16.3 Evidence lineage interaction, 16.4 Recommendation state machine, 16.5 Confidence and uncertainty, 16.6 Current truth versus future enhancement, 16. Agentic Interaction and Reasoning Visualization

### Community 64 - "26. Testing and Acceptance Criteria"
Cohesion: 0.33
Nodes (6): 26.1 Required command gates, 26.2 Functional acceptance matrix, 26.3 Automated test layers, 26.4 Manual acceptance, 26.5 Definition of done, 26. Testing and Acceptance Criteria

### Community 65 - "3. Existing Functionality Inventory"
Cohesion: 0.33
Nodes (6): 3.1 User-facing routes, 3.2 API contracts to preserve, 3.3 Existing component map, 3.4 Golden scenarios, 3.5 State inventory and recovery contract, 3. Existing Functionality Inventory

### Community 66 - "Phase P3 — Federated risk and sponsor proof"
Cohesion: 0.40
Nodes (5): `apps/api/zetaris/client.py`, `apps/api/zetaris/sql/federated_check.sql`, Data-quality layer, Phase P3 — Federated risk and sponsor proof, Sponsor evidence page

### Community 68 - "7. Phase-by-Phase Execution Plan"
Cohesion: 0.29
Nodes (7): 7. Phase-by-Phase Execution Plan, Phase 1: Sponsor Preflight, Data Seeding & Join-Safe Zetaris Federation, Phase 2: Stateful Amendment Memory & Deterministic UCP 600 Engine, Phase 3: Meterless Integration, Nemotron Live Extraction & Legal Adjudicator, Phase 4: Bank Decision Engine, MT734 / AML Generators & FastAPI SSE Backend, Phase 5: High-Craft 3-Pane Bank Examiner Terminal (Next.js), Phase 6: Honest Empirical Baseline Comparison & Final Polish

### Community 69 - "Phase P2 — Rule coverage and zero-hallucination controls"
Cohesion: 0.40
Nodes (5): Deterministic engine, Legal validation gate, Phase P2 — Rule coverage and zero-hallucination controls, Rule registry, Semantic adjudicator

### Community 70 - "5. Concrete Implementation Plan"
Cohesion: 0.22
Nodes (9): 5.1 Verification matrix, 5.2 Repository commands and CI policy, 5.3 Definition of “commercial-grade” for this project, 5. Concrete Implementation Plan, Frontend foundation, New components, Phase P4 — Examiner-grade UX, Phase P5 — Production controls and independent evaluation (+1 more)

### Community 71 - "10. Information Architecture and User Journeys"
Cohesion: 0.40
Nodes (5): 10.1 Proposed information architecture, 10.2 Primary examiner journey, 10.3 First-time judge journey, 10.4 Returning-user continuity, 10. Information Architecture and User Journeys

### Community 72 - "11. Three Creative Directions"
Cohesion: 0.40
Nodes (5): 11.4 Weighted decision framework, 11. Three Creative Directions, Direction A — Evidence Ledger, Direction B — Port Control Nightwatch, Direction C — Cryptographic Codex

### Community 73 - "17. Motion Design Language"
Cohesion: 0.40
Nodes (5): 17.1 Motion tokens, 17.2 Interaction recipes, 17.3 Reduced motion, 17.4 Prohibited motion, 17. Motion Design Language

### Community 74 - "19. Recommended Libraries and MCP Servers"
Cohesion: 0.40
Nodes (5): 19.1 Runtime library decision table, 19.2 Development and validation tooling, 19.3 MCP server evaluation, 19.4 Dependency policy, 19. Recommended Libraries and MCP Servers

### Community 75 - "22. Performance Engineering Strategy"
Cohesion: 0.40
Nodes (5): 22.1 User-facing budgets, 22.2 Asset and bundle budgets, 22.3 Runtime practices, 22.4 Reliability targets, 22. Performance Engineering Strategy

### Community 76 - "23. Hackathon Judge Experience"
Cohesion: 0.40
Nodes (5): 23.1 Ninety-second primary journey, 23.2 Five-minute expanded journey, 23.3 Failure-ready demo path, 23.4 Product UX alignment with judging, 23. Hackathon Judge Experience

### Community 77 - "25. Functional Preservation and Migration Strategy"
Cohesion: 0.40
Nodes (5): 25.1 Non-negotiable preservation matrix, 25.2 Incremental migration, 25.3 Data compatibility, 25.4 Rollback strategy, 25. Functional Preservation and Migration Strategy

### Community 78 - "LP-11. Typography, Color, Spacing, and Visual Assets"
Cohesion: 0.40
Nodes (5): Color use, Landing type system, LP-11. Typography, Color, Spacing, and Visual Assets, Spacing and composition, Visual asset inventory

### Community 79 - "LP-3. Three Alternative Creative Concepts"
Cohesion: 0.40
Nodes (5): Concept A — The Living Evidence Ledger, Concept B — Documentary X-Ray, Concept C — The Decision Assembly, Concept comparison, LP-3. Three Alternative Creative Concepts

### Community 80 - "LP-13. Navigation and CTA Strategy"
Cohesion: 0.40
Nodes (5): CTA hierarchy and copy, Desktop navigation, LP-13. Navigation and CTA Strategy, Micro-interactions, Mobile navigation

### Community 81 - "LP-4. Three Hero Concepts and Comparison"
Cohesion: 0.40
Nodes (5): Hero A — The Evidence Gate (selected), Hero B — The Rule That Cannot Be Overruled, Hero C — Three Outcomes, One Chain of Custody, Hero decision matrix, LP-4. Three Hero Concepts and Comparison

### Community 82 - "VERITAS-600"
Cohesion: 0.29
Nodes (7): 🏛️ Executive Summary, 📄 License & Team, 📊 Live Baselines Evaluation, 🏆 Mandatory Sponsor Integrations & Verification Guide, 📐 System Architecture, 🎯 The 3 Flagship Golden Scenarios, VERITAS-600

### Community 83 - "2.2 Verifiable Domain Models & Cryptographic Proof Chain (Phase P1)"
Cohesion: 0.13
Nodes (5): BoundingBox, EvidenceManifest, EvidenceRecord, 2.2 Verifiable Domain Models & Cryptographic Proof Chain (Phase P1), Phase 7: World-Class Elevation & Demo Integrity ✅ [COMPLETED & VERIFIED]

### Community 84 - "24. File-by-File Implementation Blueprint"
Cohesion: 0.50
Nodes (4): 24.1 Existing files, 24.2 Proposed new files, 24.3 Files that must remain decision authorities, 24. File-by-File Implementation Blueprint

### Community 85 - "2. Mandatory Sponsor Stack (Transparent, Load-Bearing Integration)"
Cohesion: 0.40
Nodes (5): 2.1 Zetaris: In-Situ Federated Data Layer, 2.2 Meterless: Context Routing, Stateful Memory & Inference Control, 2.3 NVIDIA Nemotron: Multimodal Extraction & Legal Adjudication, 2.4 Cursor: AI-Native Development Workflow, 2. Mandatory Sponsor Stack (Transparent, Load-Bearing Integration)

### Community 86 - "LP-17. Accessibility and Performance Requirements"
Cohesion: 0.50
Nodes (4): Accessibility, LP-17. Accessibility and Performance Requirements, Performance budgets, SEO and metadata

### Community 87 - "LP-1. Landing-Page Objectives and Target Audience"
Cohesion: 0.50
Nodes (4): Audiences and desired next action, LP-1. Landing-Page Objectives and Target Audience, Measurable landing outcomes, Objectives

### Community 88 - "LP-14. Landing-to-Application Transitions"
Cohesion: 0.50
Nodes (4): Authentication and onboarding truth, LP-14. Landing-to-Application Transitions, Route contract, Visual continuity

### Community 89 - "LP-19. Visual and Interaction Testing Strategy"
Cohesion: 0.50
Nodes (4): Automated coverage, Human review, LP-19. Visual and Interaction Testing Strategy, Visual matrix

### Community 90 - "LP-9. Guided Product Demonstration Concept"
Cohesion: 0.50
Nodes (4): Chosen model: one evidence chain, not a miniature application, Data and truth contract, Interaction model, LP-9. Guided Product Demonstration Concept

### Community 91 - "lucide-react"
Cohesion: 0.16
Nodes (11): DemoStage, outcomeCards, stages, DocumentViewerPane(), DocumentViewerPaneProps, INITIAL_FORM, NewCaseDialogProps, ZetarisDrawerProps (+3 more)

### Community 92 - "LP-8. Hero Composition and Interactive Behavior"
Cohesion: 0.50
Nodes (4): Evidence Gate interaction, Exact hierarchy, Initial entrance, LP-8. Hero Composition and Interactive Behavior

### Community 93 - "LP-10. Detailed Scroll and Motion Choreography"
Cohesion: 0.50
Nodes (4): Global rules, LP-10. Detailed Scroll and Motion Choreography, Optional parallax decision, Section choreography

### Community 94 - "MissionControl.tsx"
Cohesion: 0.23
Nodes (15): AdjudicationMatrixPane(), DecisionActionPane(), AgentNetwork(), AGENTS, AuditWorkspace(), CalculationBoard(), FederationWorkspace(), formatValue() (+7 more)

### Community 95 - "4. Hackathon Context and Verified Requirements"
Cohesion: 0.67
Nodes (3): 4.1 Publicly verified event facts, 4.2 Design implications of scoring, 4. Hackathon Context and Verified Requirements

### Community 96 - "5. Track Selection and Rationale"
Cohesion: 0.67
Nodes (3): 5.1 Weighted fit comparison, 5.2 Recommendation, 5. Track Selection and Rationale

### Community 97 - "test_security_redteam_fixes.py"
Cohesion: 0.21
Nodes (4): client(), test_health_reports_fallback_on_placeholder_key(), test_signoff_idempotence_rejects_duplicate_approval(), test_signoff_requires_api_key_when_configured()

### Community 100 - "2. Detailed Stack Components"
Cohesion: 0.20
Nodes (9): 1. High-Level Architecture Overview, 2.1 Frontend & User Experience, 2.2 Backend & Core Services, 2.3 Mandatory Sponsor Integrations, 2.4 Deterministic & Symbolic Engines (Python), 2. Detailed Stack Components, 3. Environment & Deployment Footprint, 8. Definition of Done (Pre-Submission Checklist) (+1 more)

### Community 101 - "evals/page.tsx"
Cohesion: 0.21
Nodes (8): EvaluationRow, EvaluationsPage(), runBenchmark(), FEATURED_CASES, metadata, fetchEvalsResults(), runEvalsBenchmark(), next

### Community 102 - "2. Repository Analysis and Product Understanding"
Cohesion: 0.40
Nodes (5): 2.1 Actual product purpose, 2.3 Current data and execution sequence, 2.4 Present implementation truth and limitations, 2.5 Baseline verification, 2. Repository Analysis and Product Understanding

### Community 103 - "api.ts"
Cohesion: 0.33
Nodes (10): DOCUMENT_OPTIONS, EvidenceIntake(), EvidenceIntakeProps, fieldValue(), acceptCaseEvidence(), approveHumanAction(), caseDocumentUrl(), createExaminationCase() (+2 more)

### Community 104 - "12. Selected Art Direction and Design Rationale"
Cohesion: 0.67
Nodes (3): 12. Selected Art Direction and Design Rationale, Copy voice, Signature moment

### Community 107 - "2.1 What is already unusually strong"
Cohesion: 0.33
Nodes (6): 2.1 What is already unusually strong, The action model is better than a binary pass/fail, The domain choice has real consequence, The federation query is intentionally join-safe, The neuro-symbolic boundary is directionally correct, The repository is operationally legible

### Community 108 - "⚡ Quickstart (Local Development)"
Cohesion: 0.40
Nodes (5): 1. Clone & Configure, 2. Start PostgreSQL & Redis, 3. Run Automated Tests, 4. Start Development Servers, ⚡ Quickstart (Local Development)

### Community 109 - "VERITAS-600: Project Execution & Agent Continuity Tracker"
Cohesion: 0.25
Nodes (5): 📝 Agent Protocol (Follow Every Turn), 🚦 Current Project Status at a Glance, 🔒 Invariant Engineering Rules (Do Not Violate), VERITAS-600: Project Execution & Agent Continuity Tracker, 👉 WHERE TO START NEXT (For the Next Agent)

### Community 110 - "VERITAS-600 Security Red Team Remediation Report"
Cohesion: 0.33
Nodes (6): 1. Executive Summary, 3. Verification & Test Evidence, 4. Conclusion, Automated Backend Test Suite, Frontend Production Build, VERITAS-600 Security Red Team Remediation Report

### Community 111 - "LP-12. Light and Dark Theme Specifications"
Cohesion: 0.50
Nodes (4): Dark, equivalent—not inverted, Light, primary, LP-12. Light and Dark Theme Specifications, Theme behavior

### Community 112 - "3. Core Technical Differentiation (The 3 Pillars)"
Cohesion: 0.50
Nodes (4): 3. Core Technical Differentiation (The 3 Pillars), Pillar 1: Strict Neuro-Symbolic Split (Hard Invariant Rule), Pillar 2: Stateful Amendment Memory (Art. 10(c) & 10(e) Quarantine), Pillar 3: Cross-Silo Risk & Bank-Officer Action Engine (With Human-in-the-Loop Gate)

### Community 113 - "6. Contemporary UI/UX Research (Through October 2026)"
Cohesion: 0.50
Nodes (4): 6.1 Research synthesis, 6.2 Product-level conclusions, 6.3 Research limitations, 6. Contemporary UI/UX Research (Through October 2026)

### Community 114 - "LP-16. React Component Architecture"
Cohesion: 0.50
Nodes (4): LP-16. React Component Architecture, Proposed landing files, Proposed tree, Server/client policy

## Knowledge Gaps
- **10 isolated node(s):** `clsx`, `react-dom`, `tailwind-merge`, `@types/node`, `@types/react` (+5 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 734 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **23 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `VERITAS-600 UI/UX Redesign Blueprint` connect `VERITAS-600 UI/UX Redesign Blueprint` to `5. Track Selection and Rationale`, `3. Existing Functionality Inventory`, `2. Repository Analysis and Product Understanding`, `10. Information Architecture and User Journeys`, `11. Three Creative Directions`, `12. Selected Art Direction and Design Rationale`, `15.2 `/examine` — Examination terminal`, `14. Complete Light/Dark Design System`, `6. Contemporary UI/UX Research (Through October 2026)`, `13. Brand and Visual Identity`, `9. Target Users and UX Research`, `4. Hackathon Context and Verified Requirements`?**
  _High betweenness centrality (0.271) - this node is a cross-community bridge._
- **Are the 16 inferred relationships involving `ZetarisFederationClient` (e.g. with `BaselineComparisonSuite` and `test_join_safe_single_row_guarantee()`) actually correct?**
  _`ZetarisFederationClient` has 16 INFERRED edges - model-reasoned connections that need verification._
- **What connects `clsx`, `react-dom`, `tailwind-merge` to the rest of the system?**
  _10 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `AmendmentMemoryEngine` be split into smaller, more focused modules?**
  _Cohesion score 0.05909090909090909 - nodes in this community are weakly interconnected._
- **Why does `2. Repository Analysis and Product Understanding` connect `2. Repository Analysis and Product Understanding` to `AmendmentMemoryEngine`, `VERITAS-600 UI/UX Redesign Blueprint`?**
  _High betweenness centrality (0.249) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `CaseStore` (e.g. with `3.16. Durable Case Authorization Storage` and `5. P2 — Medium findings`) actually correct?**
  _`CaseStore` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Should `Category P0: Correctness & Logic Bugs` be split into smaller, more focused modules?**
  _Cohesion score 0.06060606060606061 - nodes in this community are weakly interconnected._