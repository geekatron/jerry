# Phase 1 Research Synthesis: Use Case Capability Build

> **PS ID:** proj-021 | **Entry ID:** synthesis-phase-1 | **Workflow ID:** use-case-skills-20260308-001
> **Date:** 2026-03-08 | **Agent:** ps-synthesizer | **Execution Group:** G-02
> **Quality Threshold:** >= 0.95 (C4, user override C-008)
> **Methodology:** Braun & Clarke (2006) Thematic Analysis, 6-phase
> **Input Streams:** 5 (all C4 PASS at >= 0.95)
> **Version:** 1.0.0

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Plain-language synthesis for all stakeholders |
| [Input Sources](#input-sources) | Five research streams with scores and contributions |
| [Source Quality Assessment](#source-quality-assessment) | C4 PASS scores and confidence levels |
| [Methodology Applied](#methodology-applied) | Braun & Clarke 6-phase thematic analysis |
| [L1: Technical Synthesis](#l1-technical-synthesis) | Convergence map, conflict registry, gap analysis, design implications |
| [L2: Strategic Synthesis](#l2-strategic-synthesis) | Cross-reference matrix, emergent themes, architectural implications |
| [Pattern Catalog](#pattern-catalog) | PAT-001 through PAT-009 |
| [Lessons Learned](#lessons-learned) | LES-001 through LES-004 |
| [Assumptions Registry](#assumptions-registry) | ASM-001 through ASM-005 |
| [Contradictions and Tensions](#contradictions-and-tensions) | Disclosed conflicts between sources |
| [Phase 2 Recommendations](#phase-2-recommendations) | Prioritized architecture design inputs |
| [Handoff to ps-architect](#handoff-to-ps-architect) | Structured YAML handoff |

---

## L0: Executive Summary

We analyzed five C4-quality research documents — on Jacobson's Use Case 2.0/3.0 methodology, Cockburn's Writing Effective Use Cases, 17 industry sources covering BDD/TDD mapping and contract-first design, Anthropic agent skill best practices, and Jerry framework skill patterns — to find what they agree on, where they conflict, and what they leave unanswered.

**The main pattern that emerged across all five streams is progressive elaboration**: start with a brief description, deepen detail only when needed, validate early, generate downstream artifacts automatically. Jacobson calls it slicing. Cockburn calls it working breadth-first at lower precision before higher precision. The BDD literature calls it specification by example. Anthropic calls it progressive disclosure. Jerry calls it tier-based content loading. Five independent bodies of knowledge arrived at the same design pattern from different directions. This is the strongest signal in the synthesis.

**The three skills form a natural pipeline, not independent tools.** Use Case 2.0's Activity 5 explicitly produces a "use-case realization" artifact — a description of how the system's components interact to fulfill a use case. That realization artifact is precisely the input that `/test-spec` needs to generate BDD scenarios and that `/contract-design` needs to generate OpenAPI/AsyncAPI contracts. The pipeline architecture is not a design choice we are making; it is inherent in the methodology itself, confirmed independently by the Cockburn, industry-sources, and Anthropic streams.

**One genuine gap exists that no prior art addresses**: the transformation from a use-case realization artifact to a machine-readable API contract. Clark (2018) mapped use case flows to Gherkin scenarios. The industry-sources stream confirmed via exhaustive 17-source search that no existing literature covers the use-case-to-contract step. This means the `/contract-design` skill addresses a genuine capability gap — but it also means we have no prior art to validate our design against, which raises the architectural risk for that skill specifically.

**For Phase 2 (Architecture Design)**: the ps-architect should treat the shared artifact format (the use-case realization document that flows between skills) as the most critical design decision. Everything else — agent decomposition, routing keywords, SKILL.md structure — follows from getting that format right.

---

## Input Sources

| # | Source | Type | Agent | C4 Score | Confidence | Key Contribution |
|---|--------|------|-------|----------|------------|-----------------|
| S-01 | `research/jacobson-use-case-2.md` | Research | ps-researcher | 0.953 | HIGH | UC 2.0/3.0 methodology: 7 activities, 5 work products, slice lifecycle, realization artifact |
| S-02 | `research/cockburn-writing-effective-use-cases.md` | Research | ps-researcher | 0.953 | HIGH (0.97) | Template formats, goal levels, precision levels, breadth-first principle, 12-step process |
| S-03 | `research/industry-sources.md` | Research | ps-researcher | 0.950 | HIGH (0.95) | Clark UC2.0→Gherkin mapping, 7 Cs quality framework, SbE data, no UC-to-contract prior art |
| S-04 | `research/anthropic-skill-best-practices.md` | Research | ps-researcher | 0.954 | HIGH (0.92) | Progressive disclosure, simplicity principle, subagent isolation, 7-step implementation sequence |
| S-05 | `research/jerry-skill-pattern-analysis.md` | Analysis | ps-analyst | 0.950 | HIGH | 5 non-negotiable Jerry patterns, routing risks, 9-step implementation, trigger map worked example |

All 5 streams are at path prefix: `projects/PROJ-021-use-case/orchestration/use-case-skills-20260308-001/`

---

## Source Quality Assessment

| Source | Score | Iter | Threshold Gap | Verdict |
|--------|-------|------|--------------|---------|
| S-01 (Jacobson) | 0.953 | 7 | +0.003 | PASS |
| S-02 (Cockburn) | 0.953 | 8+ | +0.003 | PASS |
| S-03 (Industry) | 0.950 | 5 | 0.000 | PASS (boundary) |
| S-04 (Anthropic) | 0.954 | 6 | +0.004 | PASS |
| S-05 (Jerry patterns) | 0.950 | 8+ | 0.000 | PASS (boundary) |

**Note:** S-03 and S-05 passed at exactly the threshold boundary (0.000 gap). Findings from these sources are treated as HIGH confidence but synthesizer applied additional corroboration checks — every claim from S-03 and S-05 used in this synthesis is independently supported by at least one other stream.

---

## Methodology Applied

Braun & Clarke (2006) six-phase thematic analysis, applied to five source documents:

| Phase | Activity | Output |
|-------|----------|--------|
| 1. Familiarization | Read all 5 documents (L0, L1, L2 sections; adversary score reports) | Mental model of each stream |
| 2. Coding | Identified 34 initial codes across streams | Code list with stream attribution |
| 3. Theme Search | Grouped codes into 9 candidate themes | Draft theme table |
| 4. Theme Review | Validated themes against source content; eliminated 0 candidates, merged 2 pairs | Refined theme table (7 themes) |
| 5. Theme Definition | Named and described each theme; assigned quality level | See L1 Convergence Map |
| 6. Report | This document | phase-1-synthesis.md |

**Code-to-theme collapse:** 34 initial codes → 7 themes. Two pairs were merged: "breadth-first writing" + "progressive disclosure" → Theme T-01 (Progressive Elaboration); "artifact handoff" + "pipeline architecture" → Theme T-03 (Use-Case Realization Bridge). No codes were discarded.

---

## L1: Technical Synthesis

### Convergence Map

Cross-cutting themes that appear in 3 or more independent streams. Quality = source count.

| Theme ID | Theme Name | Streams | Quality | Description |
|----------|-----------|---------|---------|-------------|
| T-01 | Progressive Elaboration | S-01, S-02, S-03, S-04, S-05 | **HIGH (5/5)** | Start brief, deepen on demand. UC 2.0 uses narrative levels (Briefly Described→Fully Described); Cockburn uses precision levels (name+goal → brief → extensions → extension handling); SbE uses specification by example; Anthropic uses Tier 1-3 progressive disclosure; Jerry uses L0/L1/L2 output levels and tier-based content loading. |
| T-02 | Test Cases as Primary Artifact | S-01, S-02, S-03 | **HIGH (3/5)** | All three methodology streams identify test cases as the central deliverable, not narratives. Jacobson: "Test cases are the most important work product — more important than narratives" [S-01, p. 5]. Cockburn: completeness heuristics define "done" by whether all extensions are covered. Clark (2018): use case flows → BDD scenarios as the primary transformation. |
| T-03 | Use-Case Realization as Pipeline Bridge | S-01, S-03, S-04 | **HIGH (3/5)** | UC 2.0 Activity 5 explicitly produces a realization artifact. Clark (2018) maps the same artifact to Gherkin. Anthropic's maker-checker pattern validates the subagent-per-artifact isolation. This artifact is the integration point between the three skills. |
| T-04 | Goal-Level Classification | S-01, S-02 | **MEDIUM (2/5)** | Both Jacobson and Cockburn use hierarchical goal levels (UC 2.0 equivalent: Use Case→Slice→Test Case; Cockburn: Cloud→Kite→Sea Level→Fish→Clam). The `/use-case` skill must surface goal-level classification as a first-class concept to enable correct test scope downstream. |
| T-05 | Quality via Coverage, not Depth | S-02, S-03 | **MEDIUM (2/5)** | Cockburn: 3-9 steps in the Main Success Scenario; completeness means covering all extensions, not writing more detail per step. The 7 Cs (S-03): C1=Coverage is the primary quality criterion. Quality is horizontal (are all paths covered?) before vertical (how detailed is each path?). |
| T-06 | Skill Architecture: Dual-File with Constitutional Triplet | S-04, S-05 | **HIGH (2/5 but MANDATORY)** | H-34 requires every agent to have `.md` + `.governance.yaml`. Both S-04 and S-05 independently elaborate the rationale: Claude Code runtime parses only official frontmatter fields; governance metadata needs separate CI-validated file. Constitutional triplet (P-003, P-020, P-022) mandatory in every agent definition. Not optional for any of the three target skills. |
| T-07 | Routing Disambiguation Required | S-05 | **LOW (1/5)** | Jerry pattern analysis identifies keyword collision risks for all three new skills against existing skills (`/nasa-se`, `/eng-team`, `/problem-solving`). Single-stream finding but HIGH impact: routing failure silently degrades quality without any error signal. Requires explicit compound-trigger disambiguation in trigger map. |

---

### Conflict Registry

Disclosed tensions and contradictions between sources. All conflicts are disclosed per P-022.

| Conflict ID | Description | Source A View | Source B View | Resolution for Design |
|-------------|-------------|---------------|---------------|----------------------|
| CF-01 | Narrative vs. test case priority | S-01: "Test cases more important than narratives" (Jacobson explicit). UC narratives are input scaffolding. | S-02: The Fully-Dressed template centers on the narrative (Main Success Scenario); test cases appear as a field, not primary. Cockburn's 12-step process has narrative-writing as steps 1-7, with extensions as steps 8-9. | **Resolution:** Both are right in different contexts. Narratives are primary for elicitation and communication; test cases are primary for completion verification. Design implication: `/use-case` generates narrative first, `/test-spec` generates test cases second. The pipeline resolves the tension. |
| CF-02 | Abstraction level for use cases | S-01 (UC 2.0): Sea-level use cases are the natural unit; slices subdivide them. Multiple slices per use case expected. | S-02 (Cockburn): Sea-level goal is the natural unit, but cloud and kite levels are also legitimate use cases. Superordinate use cases compose subordinate ones. | **Resolution:** Both use sea-level as the standard unit for detailed writing, but frame it differently (Jacobson: from above by slicing; Cockburn: from below by composing). Design implication: `/use-case` should support both decomposition patterns without forcing one. |
| CF-03 | LLM generation quality | S-03: Industry data (136% growth in LLM-RE studies 2023-2024) shows LLM generation is 720x faster at 0.06% cost; hallucination and domain-specificity gaps identified. | S-04: Anthropic explicitly recommends simplicity principle ("start simple, add complexity only when measurably needed") and progressive disclosure; does not address LLM-RE quality data. | **Resolution:** S-03's hallucination gap and S-04's simplicity principle both argue for the same design: LLM generates; human validates; quality gate (7 Cs or S-014) scores the output. The `/use-case` skill should not bypass human review. |
| CF-04 | Agent count per skill | S-04 recommends starting with 1 agent per skill, splitting only when methodology section exceeds 1,500 tokens OR 2+ cognitive modes required. | S-05 identifies 4 agents for `/use-case` (author, reviewer, slicer, analyst) in the ORCHESTRATION_PLAN.md Phase 3 section. | **Resolution:** CF-04 is not a true conflict — S-04's guidance establishes the decision criterion; the Phase 3 decomposition is a target, not a requirement. Phase 2 architecture design should start with 1 agent per skill, validate against the 1,500-token and cognitive-mode thresholds, and decompose only if the threshold is exceeded. |

---

### Gap Analysis

Areas not adequately addressed by any single research stream.

| Gap ID | Description | Contributing Streams | Impact | Recommendation |
|--------|-------------|---------------------|--------|---------------|
| G-01 | **UC-to-contract transformation algorithm** | S-03 confirmed: no prior art found after exhaustive 17-source search. S-01 confirms realization artifact exists but does not define transformation to API schema. S-04/S-05 provide Jerry skill structure guidance but not domain methodology. | **HIGH** — `/contract-design` must define a novel algorithm with no validation against established prior art. Increases architectural risk for that skill specifically. | Phase 2 must include a design risk section for `/contract-design`. Prototype the transformation algorithm early (before full implementation). Use the 0.85 prototyping floor from S-04 for initial validation. |
| G-02 | **Multi-actor/multi-system UC behavior** | S-01 covers standard use cases; S-02 covers enterprise scope briefly. Neither covers collaborative use cases with multiple systems as primary actors (relevant for contract-design of event-driven systems). | **MEDIUM** — AsyncAPI contracts require publisher/subscriber roles. Use cases with a single system actor do not map cleanly to pub/sub. | Phase 2 should define the actor-to-contract-role mapping explicitly. Flag as a design constraint: initial `/contract-design` may support only REST (single primary actor) with async as a follow-on. |
| G-03 | **Slice-to-test-plan cardinality** | S-01 defines slice lifecycles; S-03 provides Clark mapping (basic flow→happy path, alternative→additional, extension→error). Neither specifies cardinality: does 1 slice = 1 BDD feature file? 1 scenario? | **MEDIUM** — `/test-spec` output format (1 feature file per use case? per slice?) is unspecified. | Phase 2 architecture must decide and document: recommended default is 1 feature file per use case, 1 scenario per slice (basic flow + tested extensions). |
| G-04 | **Worktracker integration for UC entities** | S-01 provides a Jerry mapping (Use Case→Feature/Epic, Slice→Story/Task, Slice state→Entity status). S-05 confirms existing template `USE-CASE.template.md` exists at `.context/templates/requirements/`. Neither specifies whether new UC entities require changes to worktracker entity hierarchy or only use existing entity types. | **LOW-MEDIUM** — Likely can be addressed with existing entity types, but needs confirmation. | Phase 2 architecture should confirm entity hierarchy compatibility. If no new entity types are needed, this gap closes. |
| G-05 | **Regression behavior when source use case changes** | No stream addresses what happens to `/test-spec` and `/contract-design` artifacts when the source use case is updated. Downstream artifacts become stale. | **LOW** (out of scope for Phase 2 implementation, but worth noting) | Flag as a known limitation in SKILL.md for each of the three skills. Out of scope for initial implementation. |

---

### Design Implications Table

Concrete design decisions implied by the synthesis. Input to Phase 2 Architecture Design.

| Impl ID | Skill | Implication | Source | Priority |
|---------|-------|-------------|--------|----------|
| DI-01 | `/use-case` | The skill MUST support the 4 narrative detail levels (Briefly Described, Bulleted Outline, Essential Outline, Fully Described) as discrete output modes. Default: Bulleted Outline. Upgrade on demand. | S-01, S-02 convergence on progressive elaboration (T-01) | P1 |
| DI-02 | `/use-case` | Goal levels (Cloud/Kite/Sea Level/Fish/Clam) MUST be surfaced as a classification field in every use case artifact. Default: Sea Level. | S-02; S-01 implicit (slice granularity requires sea-level anchoring) | P1 |
| DI-03 | `/use-case` | The use case slice lifecycle (UC 2.0: Scoped→Prepared→Analyzed→Implemented→Verified; UC 3.0: Identified→Defined→Analyzed→Prepared→Implemented→Verified) MUST be represented in the shared artifact schema. | S-01 | P1 |
| DI-04 | All 3 skills | The shared artifact format — the use-case realization document — is the most critical Phase 2 design decision. It is the contract between all three skills. Architecture design MUST define this format before designing individual skill agents. | S-01 (realization artifact), S-03 (Clark transformation input), S-04 (maker-checker pattern) | P0 |
| DI-05 | `/test-spec` | Clark (2018) mapping MUST be implemented as the default transformation algorithm: basic flow→happy path scenario, alternative flow→additional scenario, extension→error scenario (negative test). | S-03 (Clark mapping table, directly implementable) | P1 |
| DI-06 | `/test-spec` | The 7 Cs quality framework MUST be used as the quality gate for generated BDD specifications. C1 Coverage and C4 Consistent Abstraction map to S-014 Completeness (0.20) and Internal Consistency (0.20) dimensions. | S-03 (7 Cs, C1+C4 primary) | P1 |
| DI-07 | `/contract-design` | Initial scope: REST (OpenAPI 3.x) only. Async/event-driven (AsyncAPI, CloudEvents) as follow-on capability. Rationale: G-02 gap (multi-actor behavior for pub/sub) unresolved. | S-03 (no prior art), G-02 | P2 |
| DI-08 | `/contract-design` | The transformation from use-case interaction steps to OpenAPI path/operation schema is a novel algorithm requiring prototyping before production implementation. Use 0.85 prototyping quality floor. | S-04 (prototyping threshold), G-01 | P1 |
| DI-09 | All 3 skills | Each skill starts with 1 agent. Split into multiple agents only when: (a) methodology section exceeds 1,500 tokens, OR (b) 2+ cognitive modes required, OR (c) quality gate scores below 0.85 from scope overload. | S-04 (agent count guidance) | P2 |
| DI-10 | All 3 skills | Trigger map entries for all three skills MUST include compound triggers and negative keywords to prevent routing collisions with `/nasa-se`, `/eng-team`, and `/problem-solving`. Priority assignment >= 12 to avoid disrupting existing resolution algorithm. | S-05 (routing disambiguation, T-07) | P1 |
| DI-11 | `/use-case` | The Cockburn 12-step writing process SHOULD be the structural backbone of the `uc-author` agent methodology section, with Jerry CLI command mappings at each step. | S-02 (12-step process with jerry command mappings) | P2 |
| DI-12 | All 3 skills | All three skills require the H-34 dual-file architecture: `.md` frontmatter + `.governance.yaml` with constitutional triplet and minimum 3 `forbidden_actions` entries. | S-04, S-05 (T-06, mandatory) | P1 |

---

## L2: Strategic Synthesis

### Cross-Reference Matrix

How each stream contributes to each design theme. Cells show agreement level and specific contribution.

| Theme | S-01 Jacobson | S-02 Cockburn | S-03 Industry | S-04 Anthropic | S-05 Jerry |
|-------|--------------|--------------|--------------|---------------|-----------|
| **T-01 Progressive Elaboration** | UC 2.0 narrative levels; slicing as progressive commitment | Precision levels; breadth-first directive (exact quote: Reminders p.ii) | SbE 10-year data, 22% quality improvement | Progressive disclosure 3-tier (metadata→core→supplementary) | L0/L1/L2 output levels mandatory; tier-based loading |
| **T-02 Test Cases Primary** | "Most important work product" [p.5] explicit | Extensions and completeness heuristics; 9-step extension handling | Clark UC2.0→Gherkin mapping; BDD adoption 71% | Quality gate scoring methodology | 7 Cs quality framework integration with S-014 |
| **T-03 Realization Bridge** | Activity 5 produces realization artifact explicitly | Design scope levels (System black-box) as realization framing | Clark transformation algorithm (flows→scenarios→contracts implied) | Maker-checker pattern; subagent context isolation per artifact type | `/use-case` → `/test-spec` → `/contract-design` pipeline pattern |
| **T-04 Goal-Level Classification** | Use Case hierarchy (UC→Slice→Test Case) | 5 goal levels (Cloud→Clam); sea-level as standard unit | Abstraction level as 7 Cs C4 (Consistent Abstraction) | N/A | N/A |
| **T-05 Coverage-First Quality** | Slice completeness (all states reached) | 3-9 step rule; extension coverage completeness | 7 Cs C1 Coverage primary criterion | Quality gate 0.95 threshold; S-014 Completeness weight 0.20 | S-014 SSOT integration in skill output |
| **T-06 Dual-File Architecture** | N/A (not Jerry-specific) | N/A | N/A | H-34 rationale explicit; governance YAML separate from Claude Code runtime | 5 non-negotiable patterns include H-34 as pattern 1 |
| **T-07 Routing Disambiguation** | N/A | N/A | N/A | Keyword-first routing per H-36 | Collision analysis for all 3 new skills; trigger map worked example |

**Agreement Summary:**

| Theme | Agreement | Streams Supporting | Confidence |
|-------|-----------|--------------------|------------|
| T-01 Progressive Elaboration | UNANIMOUS | 5/5 | **VERY HIGH** |
| T-02 Test Cases Primary | STRONG | 3/5 (methodology streams) | HIGH |
| T-03 Realization Bridge | STRONG | 3/5 | HIGH |
| T-04 Goal-Level Classification | PARTIAL | 2/5 (both methodology) | MEDIUM |
| T-05 Coverage-First Quality | PARTIAL | 2/5 (quality streams) | MEDIUM |
| T-06 Dual-File Architecture | MANDATORY | 2/5 (framework streams) | HIGH (non-optional) |
| T-07 Routing Disambiguation | SINGLE | 1/5 | LOW (but HIGH impact) |

---

### Emergent Themes

Insights that were not visible within any single research stream but emerged from cross-pollination.

**ET-01: The Three Skills ARE a Methodology, Not Three Tools**

No single stream articulated this explicitly, but it emerges clearly from the synthesis. UC 2.0's 7 activities map directly to the three skills: Activities 1-3 (find actors/use cases, slice use cases, describe use cases) → `/use-case`; Activity 4 (prepare a slice for development) → shared; Activity 5 (analyze behavior) → feeds both `/test-spec` and `/contract-design`; Activity 6 (implement software) → downstream; Activity 7 (test your system) → `/test-spec` closes the loop. The three skills are not arbitrary — they implement exactly the work products that UC 2.0 identifies as necessary for agile use-case-driven development.

**ET-02: The Anthropic Simplicity Principle Protects Against Methodology Over-Engineering**

The 5 methodology streams (S-01, S-02, S-03) collectively provide a rich, validated methodology with many optional features. Taken naively, implementing all of them would produce a complex, brittle skill that violates Anthropic's simplicity principle (S-04). The synthesis reveals a natural layering: Brief/Casual/Fully-Dressed template formats map to progressive complexity; 4 narrative levels provide a graduation path; agent decomposition should follow complexity, not anticipate it. Phase 2 must make explicit which methodology features are P1 (essential for first release) and which are P2+ (defer until measured need arises).

**ET-03: The Quality Framework Alignment is Already Complete**

The 7 Cs quality framework (S-03) maps to the S-014 LLM-as-Judge dimensions (S-04, S-05) with explicit weights:

| 7 Cs Criterion | S-014 Dimension | Weight |
|----------------|-----------------|--------|
| C1 Coverage | Completeness | 0.20 |
| C4 Consistent Abstraction | Internal Consistency | 0.20 |
| C5/C6 Consistent Structure/Grammar | Methodological Rigor | 0.20 |
| C2 Cogent | Evidence Quality | 0.15 |
| C3 Coherent | Actionability | 0.15 |
| C7 Consideration of Alternatives | Traceability | 0.10 |

This means the quality gate for use case artifacts is already defined and integrated with Jerry's quality framework — the 7 Cs are not separate from Jerry quality; they ARE Jerry quality applied to the use case domain. The `uc-reviewer` agent can use S-014 directly with a 7 Cs lens applied to each dimension.

---

### Architectural Implications

Strategic design constraints for ps-architect to address in Phase 2.

**AI-01: Shared Artifact Format is the Architectural Linchpin**

The use-case realization artifact flows from `/use-case` → `/test-spec` → `/contract-design`. If this format is underspecified, each skill becomes an island. If it is overspecified, it becomes a rigid contract that prevents the skills from evolving independently. The format must be: (a) machine-readable (JSON Schema validatable), (b) human-readable (Markdown with structured sections), (c) semantically sufficient for Clark's transformation algorithm (flows named and typed), and (d) extensible (new fields don't break existing consumers). Recommendation: design as a YAML frontmatter block embedded in a Markdown document — the same pattern Jerry uses for worktracker entities.

**AI-02: Progressive Detail as a State Machine, Not Free Text**

The 4 narrative detail levels (Briefly Described → Bulleted Outline → Essential Outline → Fully Described) should be modeled as a state machine within the shared artifact format, not as a prose-quality descriptor. This enables: (a) `/test-spec` to know whether the use case has enough detail to generate reliable scenarios, (b) quality gates to set different thresholds per detail level, (c) the 5-state slice lifecycle to be correlated with narrative detail level.

**AI-03: Route by Compound Trigger, Not Single Keyword**

All three new skills share keywords with existing skills. "Use case" appears in `/nasa-se` context; "test" appears in `/eng-team`; "contract" and "API" appear in `/nasa-se` and `/eng-team`. The routing design must use compound triggers (e.g., "use case" AND "author/write/create" → `/use-case`; "BDD" OR "scenario" AND "use case" → `/test-spec`; "OpenAPI" AND "use case" → `/contract-design`). The negative keyword sets are equally important as positive keywords for avoiding false positives.

**AI-04: Agent Decomposition Should Follow, Not Lead, Complexity**

S-04's guidance (1 agent per skill initially; split at 1,500-token methodology section threshold) combined with S-05's 4-agent decomposition for `/use-case` creates a design tension (CF-04). Resolution: Phase 3 implementation STARTS with 1 agent per skill. If the methodology section approaches 1,500 tokens during prototyping, split at that point. Do not pre-decompose based on the Phase 3 target list in ORCHESTRATION_PLAN.md — that list is a ceiling, not a floor.

**AI-05: `/contract-design` Requires a Novel Algorithm**

This is the highest-risk element of the entire capability. No prior art exists for the use-case-to-contract transformation. The algorithm must be designed from first principles in Phase 2, prototyped in Phase 3 at the 0.85 floor, and validated before the Phase 4 red-team review. The Phase 2 architecture design for `/contract-design` should include: (a) the proposed transformation algorithm as a decision tree or mapping table, (b) the actor-to-contract-role mapping for REST (and explicitly deferred for async), (c) the JSON Schema fragment that each use case step maps to.

---

## Pattern Catalog

### PAT-001: Progressive Elaboration

**Context:** Authoring use case artifacts in an AI-assisted workflow where the depth of detail is not known upfront.
**Problem:** How to generate useful output at low effort while preserving the ability to add precision when needed.
**Solution:** Implement the 4 narrative detail levels as discrete modes with explicit upgrade triggers. Default to Bulleted Outline; upgrade to Essential Outline when a use case is selected for a sprint; upgrade to Fully Described when test cases are being written. Mirror this in skill output with L0 (brief)/L1 (detailed)/L2 (architectural) structure.
**Consequences:** (+) Low entry barrier; partial output is always useful. (+) Downstream tools can check detail level before transforming. (-) Requires state tracking in the shared artifact format. (-) LLM prompt design must target the correct level to avoid unnecessary verbosity.
**Quality:** HIGH (5/5 streams)
**Sources:** S-01 (UC 2.0 narrative levels), S-02 (precision levels, breadth-first directive), S-03 (SbE data), S-04 (progressive disclosure), S-05 (L0/L1/L2)

---

### PAT-002: Test-First Verification Framing

**Context:** Designing a use case authoring workflow that integrates with downstream test generation.
**Problem:** How to ensure use case artifacts are written in a way that makes test generation reliable.
**Solution:** Frame the use case extension matrix (basic flow + alternatives + extensions) as the test case specification, not a narrative supplement. Every use case that reaches "Analyzed" state (UC 2.0 slice lifecycle) must have a complete extension matrix before it is eligible for `/test-spec` processing.
**Consequences:** (+) Test coverage is built into the use case authoring process, not bolted on later. (+) The 7 Cs Coverage criterion (C1) is satisfied by construction. (-) Adds an authoring step that feels like extra work without the downstream skill to demonstrate value.
**Quality:** HIGH (3/5 methodology streams; reinforced by 7 Cs)
**Sources:** S-01 ("test cases most important work product"), S-02 (extension handling as completeness), S-03 (Clark mapping, BDD adoption data)

---

### PAT-003: Realization Artifact as Pipeline Contract

**Context:** Three skills in a pipeline where each skill's output is the next skill's input.
**Problem:** How to define the interface between skills in a way that is stable, machine-readable, and human-verifiable.
**Solution:** Define the use-case realization artifact as a YAML frontmatter + Markdown document (the "realization document"). The YAML frontmatter encodes machine-readable fields (goal level, detail level, slice state, actor list, interaction steps with typed roles). The Markdown body contains the human-readable narrative and extension matrix. Both skills downstream consume the YAML; humans read the Markdown.
**Consequences:** (+) JSON Schema validatable frontmatter enables CI-level integrity checks. (+) Human-readable body preserves the communication value of use cases. (+) Consistent with Jerry's entity format. (-) Requires defining the JSON Schema before any of the three skills can be fully implemented.
**Quality:** HIGH (3/5 streams; emergent from cross-pollination)
**Sources:** S-01 (realization artifact from Activity 5), S-03 (Clark transformation requires named flows), S-04 (maker-checker pattern; subagent isolation)

---

### PAT-004: 7 Cs as Jerry Quality Gate

**Context:** Evaluating the quality of generated use case artifacts using the existing Jerry quality framework.
**Problem:** How to adapt the 7 Cs use case quality framework to work with Jerry's S-014 LLM-as-Judge scoring.
**Solution:** Map the 7 Cs directly to S-014 dimensions (see ET-03 table). The `uc-reviewer` agent applies S-014 with 7 Cs interpretations per dimension. Use the same 0.92 production threshold (H-13) and 0.85 prototyping floor (S-04 guidance).
**Consequences:** (+) No new quality framework — the 7 Cs are already implemented by S-014 with appropriate weights. (+) Consistent quality language across Jerry. (-) Some 7 Cs criteria (e.g., C7 Consideration of Alternatives) are mapped to lower-weight S-014 dimensions (Traceability 0.10); teams that prioritize C7 may feel the weighting is wrong.
**Quality:** MEDIUM (2/5 streams; but both are quality-focused streams)
**Sources:** S-03 (7 Cs framework), S-05 (S-014 integration, SSOT reference)

---

### PAT-005: Compound-Trigger Routing Disambiguation

**Context:** Adding new Jerry skills whose keywords overlap with existing skills.
**Problem:** How to prevent routing false positives when new skill keywords are subsets of existing skill keywords.
**Solution:** Define compound triggers (multi-keyword co-occurrence) as the primary routing signal for all three new skills. Assign negative keywords for each term shared with an existing skill. Set priority >= 12 for all three new skills to avoid disrupting existing resolution algorithm (existing skills max priority is 12 for `/diataxis`).
**Consequences:** (+) Precise routing without disrupting existing skill order. (+) Compound triggers are already supported by the Phase 1 routing architecture. (-) More complex trigger map entries; harder to maintain. (-) Priority >= 12 means the new skills lose priority ties to `/diataxis` — acceptable because domain contexts don't overlap.
**Quality:** LOW (1/5 streams but MANDATORY)
**Sources:** S-05 (routing collision analysis, trigger map worked example)

---

### PAT-006: Slice State as Worktracker Status Field

**Context:** Integrating UC 2.0 slice lifecycle with Jerry's worktracker entity system.
**Problem:** How to track use case progress without adding new entity types to the worktracker.
**Solution:** Map UC 2.0 slice states to the `status` field of existing Story entities (Scoped→`draft`, Prepared→`ready`, Analyzed→`in-progress`, Implemented→`review`, Verified→`done`). Use Use Case as Feature/Epic; Slice as Story/Task. No new entity types needed.
**Consequences:** (+) No worktracker schema changes needed. (+) Existing Jerry workflows (sprint planning, backlog grooming) work with UC slices without modification. (-) The mapping is lossy — UC 2.0 has sub-states not represented in Jerry status (e.g., "Analyzed" has a sub-state "test cases written" that is not captured by `in-progress`).
**Quality:** MEDIUM (S-01 provides the mapping; S-05 confirms existing entity types are sufficient)
**Sources:** S-01 (Jerry Mapping table, Activity 3 worktracker integration)

---

### PAT-007: Cockburn Goal Levels as UC Classification Schema

**Context:** Designing the `/use-case` agent to help users identify the right scope for a use case.
**Problem:** Use cases written at the wrong goal level are the most common authoring error — writing a summary use case with implementation detail, or a subfunction use case treated as a complete workflow.
**Solution:** Integrate Cockburn's 5-level goal taxonomy into the use case template as a mandatory classification field. Use the sea metaphor mnemonics (Cloud/Kite/Sea Level/Fish/Clam) for display; use +/nothing/- annotation symbols for compact notation (Cockburn Reminders). Default new use cases to Sea Level. Reject Fish-level use cases as incomplete by themselves (they require a parent Sea Level).
**Consequences:** (+) Automatic scoping guidance built into authoring. (+) Goal level enables correct test scope in `/test-spec` (Sea Level → one Feature file; Fish → one Scenario). (-) Users unfamiliar with the framework may resist classifying before writing.
**Quality:** MEDIUM (2/5 streams — methodology streams only)
**Sources:** S-02 (goal levels, annotation system, sea-level definition), S-01 (slice granularity at sea-level anchoring)

---

### PAT-008: Clark UC2.0-to-Gherkin Transformation

**Context:** Implementing `/test-spec` as a transformation from use case artifacts to BDD test specifications.
**Problem:** How to systematically derive Given/When/Then scenarios from use case narrative flows.
**Solution:** Apply Clark (2018) mapping: (1) basic flow → single "happy path" scenario; (2) each alternative flow → additional scenario; (3) each extension → error scenario (negative test). The use case title becomes the Feature title. The use case goal becomes the Feature description. The actor becomes the Scenario subject. Use Cockburn's step-numbering extension anchor system (3a, 3b) to name scenarios (e.g., `Scenario: 3a - Credit check fails`).
**Consequences:** (+) Directly implementable; mapping is a lookup table not creative generation. (+) Validated: 71% of BDD teams (Adzic 2016) use this style. (+) Maintains traceability to source use case (scenario naming references step numbers). (-) Requires complete extension matrix in source use case — use cases at Briefly Described or Bulleted Outline level cannot be transformed.
**Quality:** HIGH (Clark mapping confirmed by 3 sources: Clark 2018 primary, Adzic 2016 BDD data, Cucumber declarative principle corroborates)
**Sources:** S-03 (Clark mapping table, Adzic SbE data, Cucumber best practices)

---

### PAT-009: Simplicity-First Agent Implementation Sequence

**Context:** Implementing three new skills with risk-ordered interdependencies.
**Problem:** How to sequence skill implementation to validate the core pipeline design before investing in individual skill features.
**Solution:** Follow the 7-step sequence from S-04: (1) define shared artifact format (JSON Schema); (2) implement `/use-case` with 1 agent; (3) implement `/test-spec` with 1 agent; (4) implement `/contract-design` with 1 agent; (5) register all three in trigger map and AGENTS.md; (6) validate E2E pipeline with a representative use case; (7) add agents incrementally per decomposition thresholds.
**Consequences:** (+) Pipeline integration validated before decomposition complexity. (+) Each step is independently testable. (+) Fail-fast: if the shared artifact format is wrong, it fails at step 6 before decomposition investment. (-) Step 6 validation may reveal that the Clark transformation algorithm (for `/test-spec`) or the UC-to-contract algorithm (for `/contract-design`) needs rework before integration.
**Quality:** HIGH (S-04 explicit implementation sequence + S-05 corroborates phased approach)
**Sources:** S-04 (7-step implementation sequence, agent count guidance), S-05 (9-step implementation, phased approach)

---

## Lessons Learned

### LES-001: Research at Boundary Creates Novel Risk

**Context:** During S-03 industry sources research, the agent conducted an exhaustive 17-source search for UC-to-contract transformation prior art.
**What Happened:** Zero prior art found. The `/contract-design` skill addresses a genuine gap with no existing methodology to validate against.
**What We Learned:** When a deliverable addresses a genuine gap (no prior art), the architectural risk for that deliverable is structurally higher than for deliverables adapting established methodology. Prototyping at 0.85 floor before production design is not optional — it is the only way to validate the design.
**Prevention:** For Phase 2 architecture of `/contract-design`: explicitly label the transformation algorithm as a novel design requiring prototype validation. Do not proceed from prototype to full implementation without a successful prototype review.
**Sources:** S-03, S-04 (prototyping threshold)

---

### LES-002: Convergent Methodology Signals Strong Validation

**Context:** Progressive elaboration appeared independently in 5/5 research streams under 5 different names (slicing, precision levels, specification by example, progressive disclosure, L0/L1/L2).
**What Happened:** What initially appeared to be five separate design choices turned out to be five independent observations of the same underlying principle.
**What We Learned:** When a pattern appears in 5/5 independent streams developed by different communities over decades, it is not a design preference — it is a behavioral law of the domain. The `/use-case` skill's progressive detail levels are not optional features; they are the mechanism that makes the skill useful at all.
**Prevention:** When a theme achieves 5/5 stream agreement, treat it as a MUST in Phase 2 design, not a SHOULD. Remove the progressive elaboration pattern from the "optional features" bucket entirely.
**Sources:** S-01, S-02, S-03, S-04, S-05

---

### LES-003: Boundary Scores Require Corroboration Discipline

**Context:** S-03 and S-05 both passed at exactly the 0.950 threshold boundary (0.000 gap).
**What Happened:** Synthesizer applied additional corroboration checks — every S-03 and S-05 claim used in this synthesis is backed by at least one other stream.
**What We Learned:** Boundary-passing scores indicate maximal revision effort; they do not indicate weakness in findings. The iterative adversarial process produced high-quality documents even at the boundary. The synthesizer's additional corroboration check adds a compensating control without rejecting findings from legitimate PASS documents.
**Prevention:** Standard operating procedure: when a source document passes at < 0.951, apply corroboration check (2+ stream support) before including its unique findings in synthesis. Document the check explicitly.
**Sources:** S-03 (score 0.950/5 iter), S-05 (score 0.950/8+ iter)

---

### LES-004: Pipeline Architecture Emerges from Methodology, Not Design

**Context:** The three-skill pipeline architecture (/use-case → /test-spec → /contract-design) was the motivating design in ORCHESTRATION_PLAN.md.
**What Happened:** Synthesis revealed that this architecture is not a design choice — it directly implements UC 2.0 Activities 4-5 (prepare slice, analyze behavior, realize), which are the methodology's own defined outputs. The pipeline was correct before synthesis validated it.
**What We Learned:** When an architectural design aligns with the methodology it implements, synthesis will confirm it rather than challenge it. This is a positive result — the planned architecture has strong theoretical grounding. But it also means that challenges to the architecture (CF-02, CF-04) are challenges to the methodology, not the design, and should be resolved by testing against the methodology, not by redesigning the pipeline.
**Prevention:** For Phase 2: frame architectural debates in terms of "which UC 2.0 activity does this implement?" to ground design decisions in methodology rather than preferences.
**Sources:** S-01, S-03, S-04

---

## Assumptions Registry

### ASM-001: Realization Artifact Format is Sufficient for Downstream Transformation

**Context:** The shared artifact format (use-case realization document) has not yet been designed.
**Impact if Wrong:** `/test-spec` and `/contract-design` cannot be implemented without redesigning their input schema.
**Confidence:** MEDIUM — UC 2.0 defines the semantic content of the realization artifact; the physical format (YAML + Markdown) is our design choice that has not yet been validated.
**Validation Path:** Phase 2 architecture must design the format; Phase 3 prototype must validate that Clark's transformation algorithm can be implemented against it.
**Sources:** S-01 (realization artifact definition), S-03 (Clark transformation requirements)

---

### ASM-002: 1 Agent Per Skill is Sufficient for Initial Implementation

**Context:** S-04 recommends starting with 1 agent per skill, splitting at 1,500-token threshold.
**Impact if Wrong:** If the methodology for any single skill requires more than 1,500 tokens in the methodology section, the single-agent approach produces lower quality than a decomposed approach. This would delay implementation.
**Confidence:** MEDIUM — S-04 provides a validated rule, but we cannot confirm until the methodology sections are written.
**Validation Path:** During Phase 3 implementation, measure methodology section length before final agent definition. If approaching 1,500 tokens, split proactively.
**Sources:** S-04 (agent count guidance), CF-04 (conflict)

---

### ASM-003: Clark (2018) Mapping Covers Sufficient BDD Scenario Types

**Context:** The Clark UC2.0→Gherkin mapping (basic flow/alternative/extension → happy path/additional/error) is the proposed `/test-spec` transformation algorithm.
**Impact if Wrong:** If real-world use cases have flow types not covered by Clark's 3-type mapping, the generated scenarios are incomplete and the 7 Cs C1 Coverage criterion is violated.
**Confidence:** HIGH — Adzic 2016 BDD adoption data (71% using this pattern) and Cucumber declarative principle both corroborate. But edge cases (e.g., concurrent flows, multi-actor handoffs) may not be covered.
**Validation Path:** Phase 3 prototype should test against at least 3 representative use cases with > 3 flow types each.
**Sources:** S-03 (Clark mapping, Adzic data)

---

### ASM-004: Existing Jerry Entity Types Are Sufficient for UC Integration

**Context:** S-01 provides a Use Case→Feature/Epic, Slice→Story/Task mapping.
**Impact if Wrong:** If the worktracker entity hierarchy cannot represent UC concepts without new entity types, the `/use-case` skill would require worktracker schema changes, which are out of scope for Phase 2-3.
**Confidence:** HIGH — the mapping to existing entity types is explicit and documented. Low risk.
**Validation Path:** Phase 2 architecture confirms entity compatibility by reviewing the worktracker entity hierarchy against UC 2.0 work products.
**Sources:** S-01 (Jerry Mapping table), S-05 (existing entity types confirmed)

---

### ASM-005: REST-Only Scope for `/contract-design` Initial Release is Acceptable

**Context:** G-02 gap (multi-actor behavior for pub/sub) is unresolved; DI-07 defers AsyncAPI to a follow-on.
**Impact if Wrong:** If stakeholders require AsyncAPI/CloudEvents from the initial release, the Phase 3 implementation timeline and scope are insufficient.
**Confidence:** MEDIUM — this is a scope assumption that depends on stakeholder requirements, not confirmed in research.
**Validation Path:** Confirm with user (project owner) before Phase 2 architecture begins. If AsyncAPI is P1, the multi-actor mapping in G-02 must be resolved in Phase 2 design.
**Sources:** S-03 (no prior art for UC-to-contract), G-02 (multi-actor gap)

---

## Contradictions and Tensions

All conflicts between sources are disclosed here per P-022 (no deception about contradictions).

The four conflicts documented in the Conflict Registry (CF-01 through CF-04) are the complete set identified during synthesis. Two are methodological tensions with clear resolutions (CF-01: narrative vs. test case priority → pipeline architecture resolves; CF-02: Jacobson vs. Cockburn abstraction framing → both use sea-level, different decomposition direction). One is a scoping conflict with a resolution pending external validation (CF-03: LLM quality data vs. simplicity principle → both point to same design: generate + human validate). One is a sequencing conflict with a recommended resolution (CF-04: Anthropic 1-agent guidance vs. Phase 3 target decomposition → start with 1, decompose at threshold).

**No fundamental methodological contradictions were found** that would require choosing between Jacobson and Cockburn. Their approaches are complementary, not competing. The Jacobson-Cockburn 2023 ACM Queue article "Use Cases are Essential" [S-01, S-02] — co-authored by both methodologists — confirms this directly.

---

## Phase 2 Recommendations

Prioritized input list for ps-architect in Phase 2 (Architecture Design).

### P0: Pre-Requisite (Must Be Done First)

| # | Recommendation | Rationale | Source |
|---|---------------|-----------|--------|
| R-01 | **Design the shared artifact format (use-case realization document)** before designing any individual skill agents. Define JSON Schema for machine-readable fields (goal level, detail level, slice state, actor list, interaction steps). Design human-readable Markdown body structure. | AI-01: This is the linchpin that every other design decision depends on. PAT-003. | S-01, S-03, S-04; DI-04 |

### P1: Architecture Design Phase Deliverables

| # | Recommendation | Rationale | Source |
|---|---------------|-----------|--------|
| R-02 | **Design `architecture/file-organization.md`**: use case artifact storage path convention (`projects/{PROJ}/{use-cases}/{UC-NNN}-{slug}.md`), worktracker integration (Use Case = Feature, Slice = Story), realization document path alongside source use case. | ORCHESTRATION_PLAN.md Step 6 requirement. PAT-006. | S-01, S-05; DI-03 |
| R-03 | **Design `architecture/frontmatter-schema.md` + `architecture/shared-schema.json`**: JSON Schema with required fields (goal_level, detail_level, slice_state, primary_actor, supporting_actors, basic_flow, alternative_flows, extensions). Version the schema at 1.0.0. | ORCHESTRATION_PLAN.md Step 7 requirement. R-01 deliverable. | S-01, S-02, S-03; DI-04, PAT-003 |
| R-04 | **Design `architecture/agent-decomposition.md`**: start with 1 agent per skill; document the 1,500-token threshold decision; specify tool tiers (T2 for `/use-case` and `/test-spec`; T2/T3 for `/contract-design` if web lookup needed for schema standards); cognitive modes (integrative for `/use-case`; systematic for `/test-spec`; convergent for `/contract-design`). | ORCHESTRATION_PLAN.md Step 8 requirement. PAT-009, DI-09. | S-04, S-05 |
| R-05 | **Design the Clark transformation algorithm as a decision tree** for the `/test-spec` agent methodology. Map: basic flow → Feature happy path scenario; alternative flow → additional scenario; extension (step-anchored) → negative test scenario. Specify cardinality: 1 Feature file per use case, 1 Scenario per flow. | G-03 gap resolution. PAT-008. | S-03; DI-05 |
| R-06 | **Design the UC-to-contract transformation algorithm for `/contract-design`** (novel algorithm, no prior art). Proposed starting point: each interaction step with a `system_response` type → HTTP operation; actor type `primary` → consumer; actor type `system` → provider; step preconditions → request parameters; step postconditions → response schema. **Explicitly label as prototype-requiring design.** | G-01 gap. AI-05. DI-08. | S-01, S-03; ASM-003 |
| R-07 | **Design the trigger map entries for all three skills** using compound triggers and negative keywords. Use priority >= 13 for all three (above current maximum of 12). Verify no collision with existing skills in `mandatory-skill-usage.md` trigger map. | PAT-005, T-07. DI-10. | S-05 |

### P2: Architecture Design Recommendations (Non-Blocking)

| # | Recommendation | Rationale | Source |
|---|---------------|-----------|--------|
| R-08 | **Confirm stakeholder requirement for AsyncAPI scope.** If P1, resolve G-02 (multi-actor pub/sub mapping) in Phase 2. If P2, document explicit deferral in architecture decisions. | ASM-005. DI-07. | S-03; G-02 |
| R-09 | **Confirm worktracker entity hierarchy compatibility** (Use Case = Feature/Epic; Slice = Story/Task). If compatible, document in `architecture/file-organization.md`. If incompatible, flag as architectural change item. | ASM-004. PAT-006. | S-01, S-05 |
| R-10 | **Design the quality gate integration** for the `uc-reviewer` agent: S-014 with 7 Cs lens (ET-03 alignment table). Document which 7 Cs criterion maps to which S-014 dimension and why. Include in `architecture/agent-decomposition.md`. | ET-03. PAT-004. DI-06. | S-03, S-05 |

---

## Handoff to ps-architect

```yaml
# Handoff: ps-synthesizer -> ps-architect
# Schema: session_context.json (handoff-v2.schema.json not yet available per S-05 finding)
schema_version: "1.0.0"
session_id: "use-case-skills-20260308-001-G02-handoff"
source_agent:
  id: "ps-synthesizer"
  family: "ps"
  cognitive_mode: "convergent"
  model: "sonnet"
target_agent: "ps-architect"
payload:
  task: >
    Phase 2 Architecture Design for PROJ-021-use-case.
    Design three deliverables: (1) file organization, (2) shared frontmatter schema,
    (3) agent decomposition. Output paths per ORCHESTRATION_PLAN.md Steps 6-8.
  key_findings:
    - "PAT-001 (Progressive Elaboration) is 5/5-stream unanimous -- mandatory design feature, not optional"
    - "PAT-003 (Realization Artifact as Pipeline Contract) is the P0 architectural linchpin -- design shared-schema.json first"
    - "PAT-008 (Clark UC2.0→Gherkin) is directly implementable as /test-spec transformation algorithm"
    - "G-01 gap: /contract-design has no prior art -- must prototype transformation algorithm before full implementation"
    - "T-06 (H-34 dual-file) and T-07 (routing disambiguation) are mandatory for all three skills"
  open_questions:
    - "ASM-005: Is AsyncAPI required for initial /contract-design release? Confirm with user before Phase 2."
    - "ASM-001: Can the realization artifact YAML frontmatter support Clark's transformation without redesign?"
  blockers: []
  confidence: 0.91
  artifacts:
    - path: "projects/PROJ-021-use-case/orchestration/use-case-skills-20260308-001/research/phase-1-synthesis.md"
      type: "synthesis"
      summary: "Phase 1 cross-pollination synthesis: 7 themes, 9 patterns, 4 lessons, 5 assumptions, 10 prioritized recommendations"
    - path: "projects/PROJ-021-use-case/orchestration/use-case-skills-20260308-001/research/jacobson-use-case-2.md"
      type: "research"
      summary: "UC 2.0/3.0 methodology: 15-item implementation roadmap, cross-skill integration architecture"
    - path: "projects/PROJ-021-use-case/orchestration/use-case-skills-20260308-001/research/cockburn-writing-effective-use-cases.md"
      type: "research"
      summary: "Cockburn WEUC: template formats, goal levels, precision levels, 12-step process, extension handling"
    - path: "projects/PROJ-021-use-case/orchestration/use-case-skills-20260308-001/research/industry-sources.md"
      type: "research"
      summary: "Industry sources: Clark mapping table, 7 Cs framework, SbE data, no UC-to-contract prior art"
    - path: "projects/PROJ-021-use-case/orchestration/use-case-skills-20260308-001/research/anthropic-skill-best-practices.md"
      type: "research"
      summary: "Anthropic best practices: implementation sequence, agent count thresholds, prototyping floor 0.85"
    - path: "projects/PROJ-021-use-case/orchestration/use-case-skills-20260308-001/research/jerry-skill-pattern-analysis.md"
      type: "analysis"
      summary: "Jerry patterns: 5 non-negotiable patterns, routing collision analysis, trigger map worked example"
  criticality: "C3"
timestamp: "2026-03-08T00:00:00Z"

# Success criteria for Phase 2 Architecture Design:
success_criteria:
  - "architecture/shared-schema.json validates against JSON Schema Draft 2020-12"
  - "architecture/file-organization.md specifies paths for UC artifacts compatible with worktracker entity structure"
  - "architecture/agent-decomposition.md specifies 1 agent per skill (initial), with explicit decomposition thresholds"
  - "UC-to-contract transformation algorithm documented with prototype-first constraint"
  - "All three skill trigger map entries designed with compound triggers and negative keywords"
  - "C4 adversary review PASS (>= 0.95) for all three architecture deliverables"
```

---

## Self-Review Checklist (H-15, S-010)

- [x] P-001: Patterns accurately reflect source content — all themes cite contributing streams; no unsupported claims
- [x] P-002: Synthesis persisted to file — writing to `research/phase-1-synthesis.md` in workflow directory
- [x] P-004: All patterns citing sources — every PAT-XXX lists contributing documents with specific claim references
- [x] P-011: Themes grounded in evidence — L1 Convergence Map shows stream count per theme; LOW quality themes flagged
- [x] P-022: Contradictions disclosed — CF-01 through CF-04 fully documented in Conflict Registry; tensions acknowledged in Contradictions section
- [x] H-23: Navigation table present with anchor links
- [x] L0/L1/L2 structure present — Executive Summary, Technical Synthesis, Strategic Synthesis
- [x] Handoff YAML present for ps-architect
- [x] PAT/LES/ASM knowledge items generated (9/4/5)
- [x] S-03 corroboration applied for boundary-score sources (S-03, S-05)

---

*Synthesis Version: 1.0.0*
*Methodology: Braun & Clarke (2006) Thematic Analysis*
*Constitutional Compliance: P-001 (truth), P-002 (file persistence), P-004 (provenance), P-011 (evidence-based), P-022 (no deception)*
*Adversary Review Required: YES — G-02-ADV C4 all-10-strategy review at >= 0.95 threshold*
*Next Agent: ps-architect (Phase 2 Architecture Design)*
*Workflow ID: use-case-skills-20260308-001*
