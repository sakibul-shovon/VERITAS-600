# Graph Report - VERITAS-600  (2026-10-27)

## Corpus Check
- 106 files · ~110,682 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 11 file(s) not represented in the graph (top: (none) 6, .example 1, .css 1)

## Summary
- 1430 nodes · 2249 edges · 133 communities (108 shown, 25 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 193 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `732b56e2`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- AmendmentMemoryEngine
- Category P0: Correctness & Logic Bugs
- ArtifactGenerator
- output
- package.json
- BaselineComparisonSuite
- UCP600DeterministicEngine
- DocumentExtractor
- test_audit_fixes.py
- compilerOptions
- test_document_intake.py
- .compute_telemetry
- seed_scenarios.py
- canonicalize_json
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
- STATUS.md
- TokenBucketRateLimiter
- 5. Concrete Implementation Plan
- types.ts
- 15.2 `/examine` — Examination terminal
- MerkleTree
- LANDING PAGE — CREATIVE DIRECTION & IMPLEMENTATION BLUEPRINT
- NvidiaNimClient
- lucide-react
- ucp600_rules.py
- 📋 Comprehensive Phase Roadmap & Task Checklist
- 🔴 VERITAS-600 — Security & Robustness Red-Team Report
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
- env
- main.py
- 16. Agentic Interaction and Reasoning Visualization
- 26. Testing and Acceptance Criteria
- 3. Existing Functionality Inventory
- TestClient
- 💡 Project Description & Platform Write-Up
- Phase P0 — Demo integrity and truthfulness
- 2. Detailed Stack Components
- VERITAS-600: Comprehensive Technology Stack Specification
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
- 7. Phase-by-Phase Execution Plan
- 2.2 Verifiable Domain Models & Cryptographic Proof Chain (Phase P1)
- 24. File-by-File Implementation Blueprint
- VERITAS-600
- LP-17. Accessibility and Performance Requirements
- LP-1. Landing-Page Objectives and Target Audience
- LP-14. Landing-to-Application Transitions
- LP-19. Visual and Interaction Testing Strategy
- LP-9. Guided Product Demonstration Concept
- Phase P1 — Verifiable state, audit, and authorization
- LP-8. Hero Composition and Interactive Behavior
- LP-10. Detailed Scroll and Motion Choreography
- MissionControl.tsx
- postgres
- 5. Track Selection and Rationale
- VERITAS-600 Security Red Team Remediation Report
- 2. Detailed Stack Components
- evals/page.tsx
- 2. Repository Analysis and Product Understanding
- api.ts
- 12. Selected Art Direction and Design Rationale
- 2. Detailed Technical Implementations
- .accept_evidence
- 2. Mandatory Sponsor Stack (Transparent, Load-Bearing Integration)
- Phase P3 — Federated risk and sponsor proof
- Phase P2 — Rule coverage and zero-hallucination controls
- LP-12. Light and Dark Theme Specifications
- ⚡ Quickstart (Local Development)
- 6. Contemporary UI/UX Research (Through October 2026)
- schema.sql
- BankDecisionEngine
- LP-16. React Component Architecture
- get_settings
- 2. Detailed Remediations by Vulnerability
- 3. Core Technical Differentiation (The 3 Pillars)
- .load
- parse_date
- 14. Complete Light/Dark Design System
- VERITAS-600 — Competition deck research
- The Weight of Evidence
- VERITAS-600 launch-film research
- 7. Phase-by-Phase Execution Plan
- VERITAS-600: Project Execution & Agent Continuity Tracker
- Launch film delivery
- 4.2 Visual system
- 3. Core Technical Differentiation (The 3 Pillars)
- QA.md

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
- `3.16. Durable Case Authorization Storage` --references--> `CaseStore`  [INFERRED]
  AUDIT_CORRECTNESS_REPORT.md → apps/api/cases/store.py
- `P2-6 & P2-8 & P2-11: Concurrency & Fault Tolerance` --references--> `CaseStore`  [INFERRED]
  SECURITY_REMEDIATION_REPORT.md → apps/api/cases/store.py
- `7. Fix roadmap (ordered, cheapest first)` --references--> `ActionType`  [INFERRED]
  SECURITY_RED_TEAM_REPORT.md → apps/api/domain/decisions.py
- `1. What the system does (one paragraph)` --references--> `BankDecisionEngine`  [INFERRED]
  SECURITY_RED_TEAM_REPORT.md → apps/api/engines/decision_engine.py
- `P0-2. Neural layer fails OPEN: NIM unavailable ⇒ verdict “COMPLIANT” on whatever was presented 🟢 VERIFIED` --references--> `BankDecisionEngine`  [INFERRED]
  SECURITY_RED_TEAM_REPORT.md → apps/api/engines/decision_engine.py

## Import Cycles
- None detected.

## Communities (133 total, 25 thin omitted)

### Community 0 - "AmendmentMemoryEngine"
Cohesion: 0.09
Nodes (13): AmendmentMemoryEngine, AmendmentResolution, memory_engine(), test_art_10_c_full_implicit_acceptance(), test_art_10_e_partial_acceptance_prohibition(), test_scenario_1_amendment_lifecycle(), det_engine(), memory_engine() (+5 more)

### Community 1 - "Category P0: Correctness & Logic Bugs"
Cohesion: 0.07
Nodes (27): 1. Executive Summary, 2. Inviolable Architectural Invariants Checklist, 3.10. Settlement Voucher Pre-Signoff Status, 3.11. UI Dispatch Status Transparency, 3.12. Honest Health & Telemetry Reporting, 3.17. CI DuckDB Pre-Seeding, 3.18. Unmasked Ruff Lint Verification, 3.19. Automated Audit Regression Test Suite (+19 more)

### Community 2 - "ArtifactGenerator"
Cohesion: 0.17
Nodes (6): ArtifactGenerator, sanitize_swift_text(), BankDecision, test_settlement_voucher_pending_vs_authorized_status(), test_sanitize_swift_text_strips_delimiters_and_tags(), P2-3: SWIFT Block & Tag Sanitization

### Community 3 - "output"
Cohesion: 0.11
Nodes (18): ignore, customPatterns, useGitignore, include, output, compress, filePath, parsableStyle (+10 more)

### Community 4 - "package.json"
Cohesion: 0.08
Nodes (32): dependencies, clsx@^2.1.1, lucide-react@^1.16.0, react@^19.0.0, react-dom@^19.0.0, tailwind-merge@^2.6.0, devDependencies, autoprefixer@^10.4.20 (+24 more)

### Community 5 - "BaselineComparisonSuite"
Cohesion: 0.14
Nodes (10): ArchitectureResult, BaselineComparisonSuite, main(), ScenarioBenchmarkRow, get_evals_results(), run_evals_benchmark(), test_baseline_suite_loads_all_10_scenarios(), test_regex_baseline_failure_modes() (+2 more)

### Community 6 - "UCP600DeterministicEngine"
Cohesion: 0.12
Nodes (9): normalize_trade_text(), UCP600DeterministicEngine, test_cif_basis_not_overridden_by_larger_credit_limit(), test_dynamic_demurrage_advisory_text(), test_no_silent_pass_on_unextracted_zero_weights(), test_cover_note_prohibition_art_28_c(), test_late_presentation_art_14_c(), test_cyrillic_homoglyph_cover_note_rejected() (+1 more)

### Community 7 - "DocumentExtractor"
Cohesion: 0.09
Nodes (20): DocumentExtractionResult, DocumentExtractor, ExtractedField, test_document_extractor_bounding_boxes(), 2.1 What is already unusually strong, 2.2 Critical findings: fix before presenting the system as live, 2.3 Architectural bottlenecks, 2.4 Real examiner workflow: what the product must support (+12 more)

### Community 8 - "test_audit_fixes.py"
Cohesion: 0.16
Nodes (9): AuditVerifier, ActionType, AuthorityLevel, DecisionReceipt, DispatchStatus, approve_human_action(), test_keyed_hmac_decision_receipt_and_verifier(), test_decision_receipt_cryptographic_verification() (+1 more)

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

### Community 13 - "canonicalize_json"
Cohesion: 0.13
Nodes (7): _canonical_default(), canonical_sha256(), canonicalize_json(), ChainEvent, RunHashChain, test_canonical_json_determinism(), test_event_hash_chain_tamper_detection()

### Community 22 - "load_presentation_data"
Cohesion: 0.07
Nodes (18): accept_case_evidence(), CaseCreateRequest, create_case(), EvidenceAcceptanceRequest, extract_documents(), get_case_document_content(), get_scenario_details(), get_sponsor_evidence() (+10 more)

### Community 28 - "examine/page.tsx"
Cohesion: 0.22
Nodes (16): ExaminationPage(), HeaderBar(), NewCaseDialog(), NoticeRegion(), NoticeRegionProps, ZetarisDrawer(), approveHumanAction(), createExaminationCase() (+8 more)

### Community 29 - "VERITAS-600: Lean Master Architecture & Engineering Execution Plan (v2 — Domain & SQL Hardened)"
Cohesion: 0.06
Nodes (33): 1.1 Target User & The High-Stakes Problem, 1. High-Level Architecture Overview, 1. System Vision & Operational Problem, 2.1 Frontend & User Experience, 2.1 Zetaris: In-Situ Federated Data Layer, 2.2 Backend & Core Services, 2.2 Meterless: Context Routing, Stateful Memory & Inference Control, 2.3 Mandatory Sponsor Integrations (+25 more)

### Community 30 - "VERITAS-600: Lean Master Architecture & Engineering Execution Plan (v2 — Domain & SQL Hardened)"
Cohesion: 0.15
Nodes (13): 1.1 Target User & The High-Stakes Problem, 1. System Vision & Operational Problem, 2.1 Zetaris: In-Situ Federated Data Layer, 2.2 Meterless: Context Routing, Stateful Memory & Inference Control, 2.3 NVIDIA Nemotron: Multimodal Extraction & Legal Adjudication, 2.4 Cursor: AI-Native Development Workflow, 2. Mandatory Sponsor Stack (Transparent, Load-Bearing Integration), 4. The 3 Flagship Golden Scenarios (Realistic, Deeply Verifiable Data) (+5 more)

### Community 31 - "VERITAS-600: Lean Master Architecture & Engineering Execution Plan (v2 — Domain & SQL Hardened)"
Cohesion: 0.25
Nodes (8): 1.1 Target User & The High-Stakes Problem, 1. System Vision & Operational Problem, 4. The 3 Flagship Golden Scenarios (Realistic, Deeply Verifiable Data), 5. Repository Structure, 6.1 PostgreSQL Schema (`apps/api/db/schema.sql`), 6.2 Join-Safe Zetaris 3-Silo Federated Query (`apps/api/zetaris/sql/federated_check.sql`), 6. Database & Join-Safe Federated Query Specifications, VERITAS-600: Lean Master Architecture & Engineering Execution Plan (v2 — Domain & SQL Hardened)

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
Cohesion: 0.12
Nodes (12): DeterministicCheckResult, DeterministicEvaluation, LegalFinding, UCP600LegalAdjudicator, test_safe_parse_json_markdown_stripping(), adjudicator(), extractor(), router() (+4 more)

### Community 37 - "4. The Palantir-Grade Visual Blueprint"
Cohesion: 0.14
Nodes (14): 4.1 Design principles, 4.3 Information architecture, 4.4 Synchronized document viewer, 4.5 Dynamic reasoning matrix, 4.6 Decision pane and tactile authorization, 4.7 Motion and micro-interactions, 4.8 Demo choreography: 150 seconds, 4. The Palantir-Grade Visual Blueprint (+6 more)

### Community 38 - "STATUS.md"
Cohesion: 0.24
Nodes (4): Submission checklist and evidence map, Presenter guide, Competition presentation delivery, Participant clarification and execution claim audit

### Community 39 - "TokenBucketRateLimiter"
Cohesion: 0.20
Nodes (6): TokenBucketRateLimiter, 3.13. CORS Configuration Hardening, 3.14. Thread-Safe Token Bucket Rate Limiting, 3.16. Durable Case Authorization Storage, Category P2: Security & Production Readiness, Phase 10: Codebase Correctness & Telemetry Hardening Audit ✅ [COMPLETED & VERIFIED]

### Community 40 - "5. Concrete Implementation Plan"
Cohesion: 0.22
Nodes (9): 5.1 Verification matrix, 5.2 Repository commands and CI policy, 5.3 Definition of “commercial-grade” for this project, 5. Concrete Implementation Plan, Frontend foundation, New components, Phase P4 — Examiner-grade UX, Phase P5 — Production controls and independent evaluation (+1 more)

### Community 41 - "types.ts"
Cohesion: 0.21
Nodes (12): AdjudicationMatrixPaneProps, DecisionActionPaneProps, ExaminationAction, ExaminationPhase, ExaminationState, initialExaminationState, BankDecision, DeterministicCheck (+4 more)

### Community 42 - "15.2 `/examine` — Examination terminal"
Cohesion: 0.11
Nodes (19): 15.1 Global shell, 15.2 `/examine` — Examination terminal, 15.3 `/evals` — Architecture benchmark, 15.4 Proof drawers and dialogs, 15.5 Judge handoff inside the terminal, 15. Page-by-Page Redesign Specifications, Benchmark run behavior, Case-specific narrative (+11 more)

### Community 43 - "MerkleTree"
Cohesion: 0.14
Nodes (5): MerkleTree, examine_presentation_sse(), event_generator(), test_merkle_tree_root_and_inclusion_proof(), P1-1. Event-loop blocking: sync LLM calls + `time.sleep` inside async SSE → whole-server stall

### Community 44 - "LANDING PAGE — CREATIVE DIRECTION & IMPLEMENTATION BLUEPRINT"
Cohesion: 0.10
Nodes (20): 18. Animation and Visualization Technology Decisions, 28. Risks, Tradeoffs, and Mitigations, Acceptance gate, Accepted trade-offs, Chosen stack, Desktop, 1440 px reference, Evaluated alternatives, Landing acceptance criteria (+12 more)

### Community 45 - "NvidiaNimClient"
Cohesion: 0.13
Nodes (5): NvidiaNimClient, test_benign_word_omitted_does_not_falsely_trigger_discrepancy(), test_divergent_goods_fail_closed_offline_replay(), test_nemotron_lru_cache_bounded_at_max_entries(), 2. Executive verdict

### Community 46 - "lucide-react"
Cohesion: 0.17
Nodes (10): DemoStage, outcomeCards, stages, HeaderBarProps, INITIAL_FORM, NewCaseDialogProps, ZetarisDrawerProps, LCScenarioSummary (+2 more)

### Community 47 - "ucp600_rules.py"
Cohesion: 0.29
Nodes (5): get_rule(), LegalRule, RuleCategory, RuleSeverity, test_rules_registry_lookup()

### Community 48 - "📋 Comprehensive Phase Roadmap & Task Checklist"
Cohesion: 0.18
Nodes (11): 📋 Comprehensive Phase Roadmap & Task Checklist, Phase 0: Repository Foundation & Standards ✅ [COMPLETED & VERIFIED], Phase 12: Cinematic Launch Film — First Review Cut Complete, Phase 13: Competition Presentation — Complete, Phase 1: Sponsor Preflight, Data Seeding & Join-Safe Zetaris Federation ✅ [COMPLETED & VERIFIED], Phase 2: Stateful Amendment Memory & Deterministic UCP 600 Engine ✅ [COMPLETED & VERIFIED], Phase 3: Meterless Integration, Nemotron Extraction & Legal Adjudicator ✅ [COMPLETED & VERIFIED], Phase 4: Bank Decision Engine, SWIFT MT734 & AML Generator + SSE API ✅ [COMPLETED & VERIFIED] (+3 more)

### Community 49 - "🔴 VERITAS-600 — Security & Robustness Red-Team Report"
Cohesion: 0.17
Nodes (11): 1. What the system does (one paragraph), 3. P0 — Critical findings, 5. P2 — Medium findings, 6. P3 — Hardening notes, 7. Fix roadmap (ordered, cheapest first), 8. Appendix — Re-running the proof battery, P0-1. “Human-in-the-loop” is authorization theater — no authentication exists anywhere 🟢 VERIFIED, P0-2. Neural layer fails OPEN: NIM unavailable ⇒ verdict “COMPLIANT” on whatever was presented 🟢 VERIFIED (+3 more)

### Community 50 - "27. Implementation Phases and Dependency Order"
Cohesion: 0.20
Nodes (10): 27. Implementation Phases and Dependency Order, Phase A — Contract lock and characterization (0.5–1 day), Phase B — Route safety and foundations (1–1.5 days), Phase C — Landing product story (1.5–2 days), Phase D — State and data architecture (1–1.5 days), Phase E — Examination vertical slice (2–3 days), Phase F — Benchmark route (1 day), Phase G — Motion, proof polish, and performance (1 day) (+2 more)

### Community 51 - "ZetarisFederationClient"
Cohesion: 0.18
Nodes (6): test_join_safe_single_row_guarantee(), test_scenario_1_wrongful_dishonor_amendment_quarantine(), test_scenario_2_cotton_yarn_benchmark(), test_scenario_3_tbml_price_anomaly_and_sanctions_freeze(), zetaris_client(), ZetarisFederationClient

### Community 52 - "VERITAS-600 UI/UX Redesign Blueprint"
Cohesion: 0.17
Nodes (11): 1. Executive Design Vision, 4.1 Publicly verified event facts, 4.2 Design implications of scoring, 4. Hackathon Context and Verified Requirements, 7. Reference Study With Links, 8. Common AI-Generated Design Patterns to Avoid, Anti-Generic-AI checklist, Approved recurring motifs (+3 more)

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

### Community 61 - "env"
Cohesion: 0.05
Nodes (42): name, runs-on, services, steps, POSTGRES_DB, POSTGRES_HOST, POSTGRES_PASSWORD, POSTGRES_PORT (+34 more)

### Community 63 - "16. Agentic Interaction and Reasoning Visualization"
Cohesion: 0.29
Nodes (7): 16.1 Observable contract, not theatrical autonomy, 16.2 Five-stage decision spine, 16.3 Evidence lineage interaction, 16.4 Recommendation state machine, 16.5 Confidence and uncertainty, 16.6 Current truth versus future enhancement, 16. Agentic Interaction and Reasoning Visualization

### Community 64 - "26. Testing and Acceptance Criteria"
Cohesion: 0.33
Nodes (6): 26.1 Required command gates, 26.2 Functional acceptance matrix, 26.3 Automated test layers, 26.4 Manual acceptance, 26.5 Definition of done, 26. Testing and Acceptance Criteria

### Community 65 - "3. Existing Functionality Inventory"
Cohesion: 0.33
Nodes (6): 3.1 User-facing routes, 3.2 API contracts to preserve, 3.3 Existing component map, 3.4 Golden scenarios, 3.5 State inventory and recovery contract, 3. Existing Functionality Inventory

### Community 66 - "TestClient"
Cohesion: 0.21
Nodes (4): client(), test_health_reports_fallback_on_placeholder_key(), test_signoff_idempotence_rejects_duplicate_approval(), test_signoff_requires_api_key_when_configured()

### Community 67 - "💡 Project Description & Platform Write-Up"
Cohesion: 0.18
Nodes (10): 1. Inspiration & The High-Stakes Problem, 2. What VERITAS-600 Does (Solution & Core Features), 3. The 3 Flagship Demonstration Scenarios, 4. Sponsor Technologies Integration, 5. Technical Stack & Clean Architecture, 6. Transparent Disclosures & Limitations, 💡 Project Description & Platform Write-Up, 📌 Quick Summary / Elevator Pitch (1–2 sentences) (+2 more)

### Community 68 - "Phase P0 — Demo integrity and truthfulness"
Cohesion: 0.22
Nodes (9): `apps/api/engines/document_extractor.py`, `apps/api/evals/compare_baselines.py`, `apps/api/inference/meterless_router.py`, `apps/api/inference/nim_client.py`, `apps/api/main.py`, `apps/web/src/components/DocumentViewerPane.tsx`, `apps/web/src/lib/api.ts`, P0 acceptance gates (+1 more)

### Community 69 - "2. Detailed Stack Components"
Cohesion: 0.20
Nodes (9): 1. High-Level Architecture Overview, 2.1 Frontend & User Experience, 2.2 Backend & Core Services, 2.3 Mandatory Sponsor Integrations, 2.4 Deterministic & Symbolic Engines (Python), 2. Detailed Stack Components, 3. Environment & Deployment Footprint, 8. Definition of Done (Pre-Submission Checklist) (+1 more)

### Community 70 - "VERITAS-600: Comprehensive Technology Stack Specification"
Cohesion: 0.29
Nodes (4): 1. High-Level Architecture Overview, 3. Environment & Deployment Footprint, 8. Definition of Done (Pre-Submission Checklist), VERITAS-600: Comprehensive Technology Stack Specification

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

### Community 82 - "7. Phase-by-Phase Execution Plan"
Cohesion: 0.29
Nodes (7): 7. Phase-by-Phase Execution Plan, Phase 1: Sponsor Preflight, Data Seeding & Join-Safe Zetaris Federation, Phase 2: Stateful Amendment Memory & Deterministic UCP 600 Engine, Phase 3: Meterless Integration, Nemotron Live Extraction & Legal Adjudicator, Phase 4: Bank Decision Engine, MT734 / AML Generators & FastAPI SSE Backend, Phase 5: High-Craft 3-Pane Bank Examiner Terminal (Next.js), Phase 6: Honest Empirical Baseline Comparison & Final Polish

### Community 83 - "2.2 Verifiable Domain Models & Cryptographic Proof Chain (Phase P1)"
Cohesion: 0.14
Nodes (5): BoundingBox, EvidenceManifest, EvidenceRecord, 2.2 Verifiable Domain Models & Cryptographic Proof Chain (Phase P1), Phase 7: World-Class Elevation & Demo Integrity ✅ [COMPLETED & VERIFIED]

### Community 84 - "24. File-by-File Implementation Blueprint"
Cohesion: 0.50
Nodes (4): 24.1 Existing files, 24.2 Proposed new files, 24.3 Files that must remain decision authorities, 24. File-by-File Implementation Blueprint

### Community 85 - "VERITAS-600"
Cohesion: 0.29
Nodes (7): 🏛️ Executive Summary, 📄 License & Team, 📊 Live Baselines Evaluation, 🏆 Mandatory Sponsor Integrations & Verification Guide, 📐 System Architecture, 🎯 The 3 Flagship Golden Scenarios, VERITAS-600

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

### Community 91 - "Phase P1 — Verifiable state, audit, and authorization"
Cohesion: 0.33
Nodes (6): `apps/api/db/schema.sql` plus migrations, Formal state specification, New audit modules, New domain modules, Phase P1 — Verifiable state, audit, and authorization, Property-based tests

### Community 92 - "LP-8. Hero Composition and Interactive Behavior"
Cohesion: 0.50
Nodes (4): Evidence Gate interaction, Exact hierarchy, Initial entrance, LP-8. Hero Composition and Interactive Behavior

### Community 93 - "LP-10. Detailed Scroll and Motion Choreography"
Cohesion: 0.50
Nodes (4): Global rules, LP-10. Detailed Scroll and Motion Choreography, Optional parallax decision, Section choreography

### Community 94 - "MissionControl.tsx"
Cohesion: 0.18
Nodes (18): AdjudicationMatrixPane(), DecisionActionPane(), DocumentViewerPane(), DocumentViewerPaneProps, AgentNetwork(), AGENTS, AuditWorkspace(), CalculationBoard() (+10 more)

### Community 95 - "postgres"
Cohesion: 0.07
Nodes (31): resources, POSTGRES_DB, POSTGRES_PASSWORD, POSTGRES_USER, interval, retries, test, timeout (+23 more)

### Community 96 - "5. Track Selection and Rationale"
Cohesion: 0.67
Nodes (3): 5.1 Weighted fit comparison, 5.2 Recommendation, 5. Track Selection and Rationale

### Community 97 - "VERITAS-600 Security Red Team Remediation Report"
Cohesion: 0.33
Nodes (6): 1. Executive Summary, 3. Verification & Test Evidence, 4. Conclusion, Automated Backend Test Suite, Frontend Production Build, VERITAS-600 Security Red Team Remediation Report

### Community 100 - "2. Detailed Stack Components"
Cohesion: 0.40
Nodes (5): 2.1 Frontend & User Experience, 2.2 Backend & Core Services, 2.3 Mandatory Sponsor Integrations, 2.4 Deterministic & Symbolic Engines (Python), 2. Detailed Stack Components

### Community 101 - "evals/page.tsx"
Cohesion: 0.19
Nodes (9): next@^15.1.0, EvaluationRow, EvaluationsPage(), runBenchmark(), FEATURED_CASES, metadata, fetchEvalsResults(), runEvalsBenchmark() (+1 more)

### Community 102 - "2. Repository Analysis and Product Understanding"
Cohesion: 0.40
Nodes (5): 2.1 Actual product purpose, 2.3 Current data and execution sequence, 2.4 Present implementation truth and limitations, 2.5 Baseline verification, 2. Repository Analysis and Product Understanding

### Community 103 - "api.ts"
Cohesion: 0.39
Nodes (7): DOCUMENT_OPTIONS, EvidenceIntake(), EvidenceIntakeProps, fieldValue(), acceptCaseEvidence(), caseDocumentUrl(), uploadCaseDocument()

### Community 104 - "12. Selected Art Direction and Design Rationale"
Cohesion: 0.67
Nodes (3): 12. Selected Art Direction and Design Rationale, Copy voice, Signature moment

### Community 105 - "2. Detailed Technical Implementations"
Cohesion: 0.20
Nodes (9): 1. Executive Summary, 2.1 Demo Integrity & Runtime Truthfulness (Phase P0), 2.3 Official Legal Rule Registry (Phase P2), 2.4 Federated Risk & Multi-Sponsor Telemetry (Phase P3), 2.5 Examiner Terminal UI & Verification Display (Phase P4), 2. Detailed Technical Implementations, 3. Verification & Compliance Matrix, 4. Key Upgraded Files (+1 more)

### Community 107 - ".accept_evidence"
Cohesion: 0.25
Nodes (8): 4. P1 — High findings, P1-2. Unbounded memory growth — unauthenticated 🔴 VERIFIED (cache), P1-4. Date format ambiguity with no contract (deterministic core) 🔴 VERIFIED, P1-5. Missing data silently removes mandatory checks 🔴 VERIFIED, P1-6. Unicode homoglyph evades Art. 28(c) cover-note prohibition 🔴 VERIFIED, P1-7. Type/NaN poisoning of reviewed evidence 🔴 VERIFIED (A5, A11, F1), P1-8. Unhandled Zetaris/SQL failure path → examine dies with 500 🔴 VERIFIED (A6), P1-7: Type & NaN Poisoning Prevention

### Community 108 - "2. Mandatory Sponsor Stack (Transparent, Load-Bearing Integration)"
Cohesion: 0.40
Nodes (5): 2.1 Zetaris: In-Situ Federated Data Layer, 2.2 Meterless: Context Routing, Stateful Memory & Inference Control, 2.3 NVIDIA Nemotron: Multimodal Extraction & Legal Adjudication, 2.4 Cursor: AI-Native Development Workflow, 2. Mandatory Sponsor Stack (Transparent, Load-Bearing Integration)

### Community 109 - "Phase P3 — Federated risk and sponsor proof"
Cohesion: 0.40
Nodes (5): `apps/api/zetaris/client.py`, `apps/api/zetaris/sql/federated_check.sql`, Data-quality layer, Phase P3 — Federated risk and sponsor proof, Sponsor evidence page

### Community 110 - "Phase P2 — Rule coverage and zero-hallucination controls"
Cohesion: 0.40
Nodes (5): Deterministic engine, Legal validation gate, Phase P2 — Rule coverage and zero-hallucination controls, Rule registry, Semantic adjudicator

### Community 111 - "LP-12. Light and Dark Theme Specifications"
Cohesion: 0.50
Nodes (4): Dark, equivalent—not inverted, Light, primary, LP-12. Light and Dark Theme Specifications, Theme behavior

### Community 112 - "⚡ Quickstart (Local Development)"
Cohesion: 0.40
Nodes (5): 1. Clone & Configure, 2. Start PostgreSQL & Redis, 3. Run Automated Tests, 4. Start Development Servers, ⚡ Quickstart (Local Development)

### Community 113 - "6. Contemporary UI/UX Research (Through October 2026)"
Cohesion: 0.50
Nodes (4): 6.1 Research synthesis, 6.2 Product-level conclusions, 6.3 Research limitations, 6. Contemporary UI/UX Research (Through October 2026)

### Community 114 - "schema.sql"
Cohesion: 0.53
Nodes (5): examination_audit_log, idx_audit_log_lc_id, idx_lc_amendments_lc_id, lc_amendments, lc_master

### Community 116 - "LP-16. React Component Architecture"
Cohesion: 0.50
Nodes (4): LP-16. React Component Architecture, Proposed landing files, Proposed tree, Server/client policy

### Community 118 - "2. Detailed Remediations by Vulnerability"
Cohesion: 0.22
Nodes (9): 2. Detailed Remediations by Vulnerability, P0-1: Human Sign-Off Gate Hardening & Evidence Binding, P0-2: Neural Fail-Closed Architecture, P0-3 & P2-9: Cryptographic Receipts & Constant-Time Verification, P0-4: Prompt Fencing & Legal Citation Whitelist, P1-2: Bounded LRU Cache Against Memory Exhaustion, P1-3: Upload & Decompression Bomb Protection, P1-8: Federated SQL Positional Parameter Binding (+1 more)

### Community 120 - "3. Core Technical Differentiation (The 3 Pillars)"
Cohesion: 0.50
Nodes (4): 3. Core Technical Differentiation (The 3 Pillars), Pillar 1: Strict Neuro-Symbolic Split (Hard Invariant Rule), Pillar 2: Stateful Amendment Memory (Art. 10(c) & 10(e) Quarantine), Pillar 3: Cross-Silo Risk & Bank-Officer Action Engine (With Human-in-the-Loop Gate)

### Community 122 - "parse_date"
Cohesion: 0.25
Nodes (4): parse_date(), test_permissive_date_parser_formats(), P2-10: Stateful Amendment Memory Date Parsing, Phase 11: Adversarial Red-Team Audit & Security Remediation ✅ [COMPLETED & VERIFIED]

### Community 123 - "14. Complete Light/Dark Design System"
Cohesion: 0.25
Nodes (8): 14.1 Theme tokens, 14.2 Type scale, 14.3 Spacing, geometry, and elevation, 14.5 Component specification, 14.6 Status grammar, 14.7 Content rules, 14.8 Focus, selection, loading, and error behavior, 14. Complete Light/Dark Design System

### Community 124 - "VERITAS-600 — Competition deck research"
Cohesion: 0.29
Nodes (7): Judging strategy, Official competition requirements, Source and evaluation audit, Sponsor research and implementation truth, Submission readiness boundary, VERITAS-600 — Competition deck research, Visual direction

### Community 125 - "The Weight of Evidence"
Cohesion: 0.29
Nodes (7): Creative direction, Critical evaluation and QA contract, Design and motion system, Feature coverage matrix, Technical architecture and production phases, The Weight of Evidence, Timed storyboard and camera grammar

### Community 126 - "VERITAS-600 launch-film research"
Cohesion: 0.29
Nodes (7): 1. Evidence and creative references, 2. Production technology comparison, 3. Female narration and alignment, 4. Mandatory root reference analysis, 5. Product truth and design inspection, First 5–10 seconds, rhythm, typography and sound, VERITAS-600 launch-film research

### Community 127 - "7. Phase-by-Phase Execution Plan"
Cohesion: 0.29
Nodes (7): 7. Phase-by-Phase Execution Plan, Phase 1: Sponsor Preflight, Data Seeding & Join-Safe Zetaris Federation, Phase 2: Stateful Amendment Memory & Deterministic UCP 600 Engine, Phase 3: Meterless Integration, Nemotron Live Extraction & Legal Adjudicator, Phase 4: Bank Decision Engine, MT734 / AML Generators & FastAPI SSE Backend, Phase 5: High-Craft 3-Pane Bank Examiner Terminal (Next.js), Phase 6: Honest Empirical Baseline Comparison & Final Polish

### Community 128 - "VERITAS-600: Project Execution & Agent Continuity Tracker"
Cohesion: 0.40
Nodes (5): 📝 Agent Protocol (Follow Every Turn), 🚦 Current Project Status at a Glance, 🔒 Invariant Engineering Rules (Do Not Violate), VERITAS-600: Project Execution & Agent Continuity Tracker, 👉 WHERE TO START NEXT (For the Next Agent)

### Community 129 - "Launch film delivery"
Cohesion: 0.50
Nodes (4): Launch film delivery, Outputs, Truth and remaining review, Verification

### Community 130 - "4.2 Visual system"
Cohesion: 0.50
Nodes (4): 4.2 Visual system, Accessibility, Palette, Typography

### Community 131 - "3. Core Technical Differentiation (The 3 Pillars)"
Cohesion: 0.50
Nodes (4): 3. Core Technical Differentiation (The 3 Pillars), Pillar 1: Strict Neuro-Symbolic Split (Hard Invariant Rule), Pillar 2: Stateful Amendment Memory (Art. 10(c) & 10(e) Quarantine), Pillar 3: Cross-Silo Risk & Bank-Officer Action Engine (With Human-in-the-Loop Gate)

## Knowledge Gaps
- **25 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `VERITAS-600 UI/UX Redesign Blueprint` connect `VERITAS-600 UI/UX Redesign Blueprint` to `5. Track Selection and Rationale`, `3. Existing Functionality Inventory`, `2. Repository Analysis and Product Understanding`, `10. Information Architecture and User Journeys`, `11. Three Creative Directions`, `12. Selected Art Direction and Design Rationale`, `15.2 `/examine` — Examination terminal`, `6. Contemporary UI/UX Research (Through October 2026)`, `13. Brand and Visual Identity`, `9. Target Users and UX Research`, `14. Complete Light/Dark Design System`?**
  _High betweenness centrality (0.241) - this node is a cross-community bridge._
- **Are the 16 inferred relationships involving `ZetarisFederationClient` (e.g. with `BaselineComparisonSuite` and `test_join_safe_single_row_guarantee()`) actually correct?**
  _`ZetarisFederationClient` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Should `AmendmentMemoryEngine` be split into smaller, more focused modules?**
  _Cohesion score 0.0946969696969697 - nodes in this community are weakly interconnected._
- **Why does `2. Repository Analysis and Product Understanding` connect `2. Repository Analysis and Product Understanding` to `AmendmentMemoryEngine`, `VERITAS-600 UI/UX Redesign Blueprint`?**
  _High betweenness centrality (0.221) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `CaseStore` (e.g. with `3.16. Durable Case Authorization Storage` and `5. P2 — Medium findings`) actually correct?**
  _`CaseStore` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Should `Category P0: Correctness & Logic Bugs` be split into smaller, more focused modules?**
  _Cohesion score 0.07142857142857142 - nodes in this community are weakly interconnected._
- **Why does `2.2 What makes the architecture distinctive` connect `AmendmentMemoryEngine` to `ArtifactGenerator`, `test_legal_adjudicator.py`, `UCP600DeterministicEngine`, `DocumentExtractor`, `2. Repository Analysis and Product Understanding`, `.compute_telemetry`, `BankDecisionEngine`, `ZetarisFederationClient`?**
  _High betweenness centrality (0.215) - this node is a cross-community bridge._