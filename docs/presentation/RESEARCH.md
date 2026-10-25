# VERITAS-600 — Competition deck research

Research date: 25 October 2026. Research completed before slide authoring. This document distinguishes official requirements, design recommendations and unverified submission conditions.

Participant clarification after first delivery: **Plan_C**, solo participant **Sakibul Hassan Shovon**. The revised deck adds these credits and the supplied dual-execution framing. [The claim audit](TEAM_AND_EXECUTION.md) distinguishes AUTO fallback, local snapshots, six context packets and estimated telemetry from unverified zero-downtime, air-gap and official Scout/engine claims. No live sponsor-console link or execution receipt was supplied in that reply.

## Official competition requirements

Primary authority: [Open Agent Hackathon 2026 event and expanded rules](https://hackathon.genai.works/event/open-agent-hackathon-2026). All ten rule sections were opened in the live page and read, rather than relying on the collapsed web extract. The [Academy overview](https://academy.genai.works/courses/open-agent-hackathon-2026/details) was cross-checked. Where older project notes or Academy copy differ, use the current event's explicit rule text.

Rule 6.2 requires the deck to cover the problem, intended users, solution, agent workflow or architecture, technology stack, Zetaris and Meterless usage, distinctive sponsor use, product imagery and future enhancements. The event does not prescribe a slide count, deck theme, presentation duration, file format or sponsor-logo placement in the public rule text reviewed. Those remain design/submission-form choices, not invented official constraints.

Rules 5.1–5.2 require Zetaris and Meterless integration; Cursor development is optional; NVIDIA should be included where it contributes. Rule 6.4 asks for an explanation of those contributions and Cursor usage if applicable. Sponsor logos alone do not demonstrate integration.

Other submission assets under 6.1/6.3 are a 1–4 minute workflow video and a source repository with setup, usage and dependency documentation. The existing 174-second video is within the duration requirement. Colab links are needed only if the agents use Colab. Eligibility/account/team/build-window/IP obligations cannot be certified by a slide file. The submission platform and team declarations still need their own checks.

Deadline: 27 October 2026, 23:45 UTC = 28 October 2026, 05:45 Asia/Dhaka. Build window begins 22 October 00:00 UTC. One primary track; teams of 1–5; pre-existing product code must be declared. No form submission or eligibility declaration is performed in this task.

## Judging strategy

Published rubric: Impact 30, Technical 20, Innovation 15, Demo 15, Product & UX 10, Sponsor Tech 10. The story should therefore give more room to the examiner's problem and working decision evidence than to generic AI claims or sponsor branding. Track 03 emphasizes reliable decisions built from data, knowledge, memory and reasoning. This is the product's central argument.

Recommended structure: 16 main slides for a roughly 6–7 minute spoken walkthrough, followed by five reference slides for judge questions. This is a recommendation, not an official time or slide limit. The existing video carries the long workflow; the deck should make the design choices and evidence easy to assess.

[Y Combinator's deck-design guide](https://www.ycombinator.com/blog/how-to-design-a-better-pitch-deck/) supports large, simple, legible slides with one primary idea. Its investor Demo Day slide-count advice is not a hackathon rule. Do not import fundraising expectations such as fabricated traction, revenue, valuation or market size into a technical competition deck. A clear target user, concrete operational consequence, implemented workflow, measured test evidence and honest next steps are more relevant here.

## Sponsor research and implementation truth

| Technology | Primary capability reference | Actual repository/demo evidence | Claim boundary |
|---|---|---|---|
| Zetaris | [Virtualization-first connection types](https://kbase.zetaris.com/knowledge/connect) | Remote query client, join-safe CTE SQL, observed DuckDB fallback receipt over seed data | No verified live Zetaris run in the film assets; local fallback is not proof of live federation |
| Meterless | [Official repository](https://github.com/Meterless/Meterless), [engines](https://www.meterless.ai/engines.html) | Local six-packet Markovian router and amendment memory | No official engine/conformance invocation found in current router; integration requirement remains unverified |
| NVIDIA Nemotron | [Official API reference](https://docs.api.nvidia.com/nim/reference/llm-apis) | NIM text/vision client, 25 RPM limiter, cached or deterministic replay in observed run | Client capability does not prove live execution; show replay and text-PDF extraction honestly |
| Cursor | [Rules documentation](https://cursor.com/docs/rules) | Repository rules and instructions | Actual Cursor development usage should be declared by the team; rules files alone do not establish usage history |

The public Meterless documentation includes reference engines and conformance material. A locally named router must not be presented as verified use of that stack solely because its class or labels say Meterless. We will cover the required sponsor topics while explicitly recording evidence still needed before an eligibility claim.

## Source and evaluation audit

Reviewed current STATUS.md, scoped graphify queries, master architecture, the earlier hackathon strategy report, current Meterless/Zetaris/NIM and evaluation implementations, and the captured API results from the film production. The older strategy report is historical: current implementation and official rules take precedence.

Observed synthetic run modes: LOCAL_DUCKDB_FALLBACK, CACHED_REPLAY, LOCAL_MARKOVIAN_ROUTER and PDF_TEXT_LAYER. The three demonstration cases produce honour, refusal and AML-hold recommendations. Every action remains pending human authorization. External dispatch is not connected.

The ten-case local run returns 10/10 expected actions for the hybrid, 6/10 for the strict-rule baseline and 4/10 for the labelled single-prompt baseline. Source inspection shows that the last baseline is a scripted heuristic proxy, not a measured live model call. Latency offsets are present in the evaluation code. Therefore omit comparative latency, broad accuracy claims and claimed savings percentages. Label any count comparison as a synthetic regression demonstration with a scripted proxy. The main evidence slide will prioritize 58 passing tests and ten expected-action matches with visible scope.

The current AML sample returns +23.10 sigma, not the +4.12 in some older titles. The insurance example is USD 480,000 × 1.10 = 528,000 required versus 518,400 presented, a 9,600 shortfall. This case also has a weight discrepancy. The film's USD 11,100 cure advisory is scenario-based arithmetic, not measured customer savings. The deck omits this ROI amount rather than presenting it as realized savings.

Legal citations follow the repository's exact rule mapping. [ICC Switzerland's UCP 600 overview](https://icc-switzerland.ch/icc-practical-tools/publications/publication-categories/ucp-600-series/ucp-600-english-detail) supports the five-banking-day examination context. The copyrighted full ICC rulebook was not newly obtained in this session; legal excerpts are not reproduced at length. Cite Art. 28(f)(ii), Art. 10(c)/(e), Art. 14(e), ISBP 745 Para A23 and Art. 16(c)(iii) precisely in the relevant examples.

## Visual direction

Continue the approved film/product identity: warm paper, ivory, forest green, copper, Georgia display headings, Arial body and restrained Consolas evidence labels. Use a 16:9 canvas, large editable typography, generated editorial imagery and authentic product detail captures. Use varied flat compositions rather than repeated card grids. Quantitative charts and comparison tables remain native and editable. Decorative/illustrative assets are generated with Imagegen, not drawn in code. Sources and detailed evidence go into speaker notes, with limitations that affect interpretation kept visible on the slide.

## Submission readiness boundary

Deck-topic coverage can be completed now. Full competition compliance cannot honestly be certified from a deck: verified Zetaris/Meterless integration evidence, team/eligibility details, build-window/pre-existing-code declaration and successful platform submission remain external obligations. The deck and a separate checklist will make those conditions explicit. We will not modify the application or claim these gaps are solved merely to make the presentation look compliant.
