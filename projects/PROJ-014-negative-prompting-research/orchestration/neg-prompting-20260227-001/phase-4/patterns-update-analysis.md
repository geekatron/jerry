# Jerry Patterns Update Analysis: Negative Prompting Application

> ps-analyst | TASK-013 | Phase 4 | PROJ-014 | 2026-02-28 | **v5.0.0 (I5 revision — FINAL)**
> Analysis Type: gap (with root-cause sub-analysis per category)
> Input: taxonomy-pattern-catalog.md (v3.0.0, 0.953 PASS), barrier-1/synthesis.md (R4, 0.953 PASS), barrier-1/supplemental-vendor-evidence.md (R4, 0.951 PASS), barrier-2/synthesis.md (v3.0.0, 0.953 PASS)
> Pattern sample: 13 files across all 12 categories (representative sample per task constraints)
> Quality threshold: >= 0.95 (C4 — orchestration directive; auto-C3 per AE-002 as this analysis informs changes to .context/ files)
> Self-review: H-15 applied before completion
> Orchestration directives: All 7 non-negotiable directives observed (see Self-Review Checklist)
> I2 revision: Addresses all 10 gaps identified in adversary-patterns-i1.md (score 0.868 → target >= 0.95)
> I3 revision: Addresses 5 targeted fixes from adversary-patterns-i2.md (score 0.900 → target >= 0.95): ADP-R1/R2 priority contradiction resolved; L0 MAY/SHOULD add counts corrected; Group 2 header count corrected; A-11 arXiv ID marked pending verification; CAT-R3 blank-row note precision improved
> I4 revision: Addresses 2 targeted fixes from adversary-patterns-i3.md (score 0.906 → target >= 0.95): recommendation count corrected from 28 to 34 (7 locations); A-11 citation escalated from "pending verification" to "likely hallucinated — not independently retrievable"
> I5 revision (FINAL): Addresses 4 targeted fixes from adversary-patterns-i4.md (score 0.939 → target >= 0.95): (1) "6 locations" corrected to "7 locations" in I4 fix documentation and PS Integration Version; (2) A-11 citation removed entirely — web search confirmed no matching paper exists; NPT-008 now supported exclusively by E-007; (3) evidence chain cleaned — all NPT-008 references now cite E-007 only; (4) methodology scope limitation acknowledgment strengthened

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Terminology Note](#terminology-note) | Task NPT labels vs. research taxonomy NPT labels — READ FIRST |
| [L0: Executive Summary](#l0-executive-summary) | Key findings, applicable categories, recommendation count |
| [Methodology](#methodology) | Sampling strategy, NPT applicability criteria, SE-1–SE-5 definitions |
| [Per-Category Analysis](#per-category-analysis) | 12 categories — current state, applicable NPTs, gaps, recommendations |
| [Architecture](#architecture) | PAT-ARCH-001 through PAT-ARCH-005 |
| [Testing](#testing) | PAT-TEST-001 through PAT-TEST-003 |
| [CQRS](#cqrs) | PAT-CQRS-001 through PAT-CQRS-004 |
| [Aggregate](#aggregate) | PAT-AGG-001 through PAT-AGG-004 |
| [Entity](#entity) | PAT-ENT-001 through PAT-ENT-005 |
| [Repository](#repository) | PAT-REPO-001 through PAT-REPO-003 |
| [Adapter](#adapter) | PAT-ADP-001 through PAT-ADP-002 |
| [Domain Service](#domain-service) | PAT-SVC-001 through PAT-SVC-002 |
| [Event](#event) | PAT-EVT-001 through PAT-EVT-004 |
| [Identity](#identity) | PAT-ID-001 through PAT-ID-004 |
| [Value Object](#value-object) | PAT-VO-001 through PAT-VO-003 |
| [Skill Development](#skill-development) | PAT-SKILL-001 through PAT-SKILL-006 |
| [Anti-Pattern Integration Recommendations](#anti-pattern-integration-recommendations) | Systematic approach for negative-constraint anti-pattern sections |
| [Pattern Catalog Update Recommendations](#pattern-catalog-update-recommendations) | Changes needed to PATTERN-CATALOG.md |
| [Implementation Sequencing](#implementation-sequencing) | Phase 5 priority groups for the 34 recommendations |
| [Evidence Gap Map](#evidence-gap-map) | T1-verified vs T4-observational vs untested per recommendation |
| [PG-003 Contingency Plan](#pg-003-contingency-plan) | Reversibility assessment per Phase 4 constraint |
| [Phase 5 Downstream Inputs](#phase-5-downstream-inputs) | What Phase 5 ADR writing needs from this analysis |
| [Constraint Propagation Compliance](#constraint-propagation-compliance) | Mandatory per taxonomy-pattern-catalog.md PS Integration |
| [Evidence Summary](#evidence-summary) | All evidence sources with full citations |
| [Self-Review Checklist](#self-review-checklist) | H-15 compliance; orchestration directive compliance |
| [PS Integration](#ps-integration) | Handoff fields, key findings, per-category confidence |

---

## Terminology Note

**Read this before the L0 Executive Summary.** Two NPT numbering systems are in use throughout this analysis. Using them interchangeably is a category error.

| System | Source | NPT-001 means | Used in this document? |
|--------|--------|---------------|------------------------|
| **Task-spec labels** | Orchestration plan task description | NPT-001 = Boundary Constraint, NPT-002 = Scope Limitation, NPT-003 = Output Boundary, NPT-005 = Process Gate | NO — written as plain English only |
| **Research taxonomy labels** | taxonomy-pattern-catalog.md | NPT-001 = Model-Internal Behavioral Intervention, NPT-009 = Declarative Behavioral Negation | YES — exclusively |

**Throughout this document: all NPT labels refer to the research taxonomy (taxonomy-pattern-catalog.md) ONLY.** Task-description category labels are written in plain English (e.g., "boundary constraint", "process gate") to prevent confusion. This prevents conflating T4-observational research patterns with task-defined structural categories.

---

## L0: Executive Summary

### What was analyzed and why

This analysis examines all 12 Jerry Framework pattern categories (49 patterns across **12 analyzed categories**) against the Phase 3 negative prompting taxonomy (NPT-001 through NPT-014) to identify: (1) where existing pattern documentation already uses negative constraint framing, (2) where gaps exist — patterns that describe what to do but omit explicit constraints about what NOT to do, and (3) where anti-pattern sections could be upgraded from implicit examples to formally named, NPT-tagged constraints. The analysis was conducted against a representative sample of 13 pattern files (Architecture double-sampled with 2 files; all other categories 1 file each).

**Category count resolution (I2 fix #1):** The PATTERN-CATALOG.md header metadata references "49 patterns across 13 categories." This document analyzes 12 categories — the 13-file sample count (from Architecture's double-sample) and the 13-category catalog claim represent different quantities. Inspection of the task specification and sampling table confirms 12 distinct pattern categories were provided for analysis. The "13 categories" figure in PATTERN-CATALOG.md header appears to be a metadata error: the catalog itself contains 12 category sections. This analysis covers all 12 confirmed categories; no 13th category was identified in any input artifact.

### Key findings

**Finding 1: The patterns library has strong anti-pattern documentation but it is structurally equivalent to NPT-014 (Type 1 blunt prohibition) — not NPT-009 (declarative behavioral negation with consequence).** The anti-pattern sections in patterns like PAT-CQRS-001, PAT-AGG-004, and PAT-ENT-003 show "WRONG/CORRECT" contrasts, which is the correct structural approach (closer to NPT-008 contrastive example pairing), but the anti-pattern labels lack consequence documentation, scope specification, and explicit NPT hierarchy membership. No pattern file currently uses NEVER/MUST NOT vocabulary in its anti-pattern sections.

**Finding 2: Architecture and testing categories have the highest applicability for boundary constraint and process gate patterns** (using plain-English task category labels — see [Terminology Note](#terminology-note) above for the two-system disambiguation). The task-specification's "boundary constraint" category maps to NPT-009 Declarative Behavioral Negation; the task-specification's "scope limitation" category maps to NPT-010 Paired Prohibition in the research taxonomy.

**Finding 3: The HARD rule enforcement architecture (NC-018, NC-019, NC-029, NC-030, NC-031, NC-033 from supplemental-vendor-evidence.md) already implements NPT-009 and NPT-012 patterns for architecture boundary violations, worker agent restrictions, and handoff rules.** Pattern documentation has NOT yet adopted this same structural approach.

**Finding 4: Seven pattern categories have zero negative constraint language in their documentation body (outside anti-pattern sections).** Five pattern categories have implicit anti-pattern sections that use NPT-014/NPT-008 structure. Three categories — skill-development, domain-service, and identity — lack anti-pattern sections entirely.

### Recommendation summary

- **Total recommendations:** 34 across all 12 categories (6 MUST NOT omit + 18 SHOULD add + 10 MAY add = 34; I4 correction — I1/I2/I3 stated 28 incorrectly)
- **Category receiving most recommendations:** Architecture (5), Testing (4), Skill Development (4)
- **Priority distribution:** MUST NOT omit = 6; SHOULD add = 18; MAY add = 10
  - *SHOULD add = 14 category recommendations + 4 catalog/skill updates (CAT-R1, CAT-R2, SKILL-R1, SKILL-R3); MAY add = 10 includes ADP-R1 and ADP-R2 reclassified from SHOULD add due to 80-line sampling risk in the Adapter category. See Implementation Sequencing for full breakdown.*
  - *Priority legend: "MUST NOT omit" = Phase 5 ADR must address this; "SHOULD add" = high-value addition; "MAY add" = optional enhancement post-Phase 2*
- **NPT patterns referenced:** NPT-009 (primary, 18 uses), NPT-010 (8 uses), NPT-011 (6 uses), NPT-014-as-diagnostic (all categories), NPT-012 (3 uses in enforcement-context patterns)
- **Evidence tier for all recommendations:** T4 observational, UNTESTED causal comparison — NEVER interpret as T1-validated changes

### Recommended action

The pattern catalog should adopt a uniform **Anti-Pattern Section Standard** that upgrades existing WRONG/CORRECT contrasts to NPT-009 structural format: named anti-pattern + NPT-014 diagnostic label + upgrade path to NPT-009 minimum, NPT-010 preferred where a positive alternative exists. This is a working-practice improvement grounded in T4 observational evidence (VS-001–VS-004). It is explicitly reversible per PG-003 contingency if Phase 2 finds null framing effect.

NEVER implement these changes as a claim that negative framing is experimentally superior to the current positive framing in the pattern documentation. The change improves structural completeness, not proven behavioral effectiveness.

---

## Methodology

### Sampling strategy

The task specified a representative sample of 13 pattern files — one per category minimum — from the 49-pattern, 12-category catalog. Architecture was double-sampled (2 files) to cover both structural and rule-enforcement patterns, yielding 13 files across 12 categories.

| Category | File Read | PAT-ID | Patterns NOT read (extrapolated) | Extrapolation confidence |
|----------|-----------|--------|----------------------------------|--------------------------|
| Architecture | hexagonal-architecture.md, one-class-per-file.md | PAT-ARCH-001, PAT-ARCH-004 | PAT-ARCH-002/003/005 | MEDIUM — 2/5 sampled; structural pattern type confirmed; specific anti-pattern content unverified |
| Testing | bdd-cycle.md, test-pyramid.md | PAT-TEST-002, PAT-TEST-001 | PAT-TEST-003 | HIGH — 2/3 sampled; both major sub-types covered |
| CQRS | command-pattern.md | PAT-CQRS-001 | PAT-CQRS-002/003/004 | MEDIUM — 1/4 sampled; command pattern is most representative; query and dispatcher may differ |
| Aggregate | invariant-enforcement.md | PAT-AGG-004 | PAT-AGG-001/002/003 | MEDIUM — 1/4 sampled; invariant enforcement is highest-constraint pattern; lifecycle patterns may differ |
| Entity | aggregate-root.md | PAT-ENT-003 | PAT-ENT-001/002/004/005 | MEDIUM — 1/5 sampled; aggregate root is structurally richest; protocol patterns (IAuditable, IVersioned) likely lack anti-pattern sections |
| Repository | event-sourced-repository.md | PAT-REPO-002 | PAT-REPO-001/003 | MEDIUM — 1/3 sampled; 80-line sample; anti-pattern section absence may be sampling artifact |
| Adapter | cli-adapter.md | PAT-ADP-001 | PAT-ADP-002 | MEDIUM — 1/2 sampled; CLI adapter representative of adapter category |
| Domain Service | domain-service.md | PAT-SVC-001 | PAT-SVC-002 | MEDIUM — 1/2 sampled; 60-line sample |
| Event | domain-event.md | PAT-EVT-001 | PAT-EVT-002/003/004 | MEDIUM — 1/4 sampled; 60-line sample |
| Identity | jerry-uri.md | PAT-ID-003 | PAT-ID-001/002/004 | MEDIUM — 1/4 sampled; 60-line sample |
| Value Object | immutable-value-object.md | PAT-VO-001 | PAT-VO-002/003 | MEDIUM — 1/3 sampled; 60-line sample |
| Skill Development | skill-structure.md | PAT-SKILL-001 | PAT-SKILL-002–006 | **LOW** — 1/6 sampled (17% coverage); anti-pattern section title visible but content NOT sampled; SKILL-R4 recommendation is extrapolated from section title only, not section content |

**Sampling artifact risk:** For files with 60–80 line samples (Repository, Domain Service, Event, Identity, Value Object), the absence of an anti-pattern section may be a sampling artifact rather than a genuine gap. Individual pattern file verification is required before implementing recommendations for these categories.

### SE-1 through SE-5: Absence-of-evidence handling criteria

These criteria govern how this analysis treats gaps where no published evidence exists. They are defined here for self-containedness; they originate in barrier-1/synthesis.md §Search Strategy.

| Code | Criterion | Application in this analysis |
|------|-----------|------------------------------|
| SE-1 | Absence of published controlled evidence is NOT treated as evidence that the practice is ineffective | T4 observational evidence (VS-001–VS-004) is treated as valid working practice evidence even without T1 corroboration |
| SE-2 | Vendor self-practice evidence is treated as T4 observational, not dismissed as self-serving | The 33 NPT-009 instances in Anthropic's own rule files are counted as working practice evidence |
| SE-3 | Practitioner consensus (AGREE-8, AGREE-9 at 2-of-3 surveys) is treated as MODERATE confidence, not NONE | The pairing and justification recommendations derive from AGREE-8/AGREE-9 despite lack of T1 corroboration |
| SE-4 | Mechanically-verifiable observations (frozen=True, L2-REINJECT markers) are treated as T4 internal observational, distinct from external working practice | NC-018, NC-019 violations are counted separately from VS-001 external vendor patterns |
| SE-5 | All T4 evidence is explicitly labeled as UNTESTED causal comparison against positive-framing equivalents | Every recommendation row carries "T4 obs, UNTESTED causal" label; no recommendation claims T1-level effectiveness |

### NPT applicability assessment criteria

For each pattern category, three criteria were applied to assess which research taxonomy NPT patterns are applicable:

1. **Domain fit:** Does the pattern category involve behavioral constraints that could be expressed as prohibitions? (Architecture: YES — layer crossing. Testing: YES — sequence violation. CQRS: YES — boundary violation.)
2. **Failure mode specificity:** Are the failure modes of this pattern specific enough to be expressed as NPT-009 (declarative behavioral negation with consequence)? Generic patterns score lower; patterns with documented WRONG/CORRECT examples score higher.
3. **Enforcement context:** Is the pattern already enforced programmatically (NPT-003/NPT-004 equivalent), meaning negative prompting adds no value? Or is the pattern enforced by documentation convention only, meaning negative constraint framing in documentation would improve practitioner guidance?

Categories assessed: All 12. NEVER extrapolate applicability from one category to another without domain-fit verification.

### Methodology scope limitation (binding constraint on defensibility)

**The representative-sample approach (13 of 49 patterns across 12 categories) establishes a composite confidence ceiling of 0.84, and this ceiling is the binding constraint on the methodological defensibility of this analysis.** This is not a minor caveat — it is a structural characteristic of the methodology:

- For 7 categories with 60–80 line samples (Repository, Domain Service, Event, Identity, Value Object) and 1 category with title-only sampling (Skill Development), the absence of anti-pattern content may be a sampling artifact rather than a genuine finding.
- Category-level confidence assessments (per-category decomposition table in PS Integration) directly propagate this ceiling: LOW for Skill Development, MEDIUM-LOW for 5 categories, MEDIUM for 4 categories, MEDIUM-HIGH for Architecture, HIGH for Testing.
- Recommendations for unsampled patterns within sampled categories (e.g., PAT-ARCH-002/003/005, PAT-CQRS-002/003/004) are extrapolated, not directly observed.

This ceiling cannot be raised within the current task scope. Downstream agents (Phase 5 ADR writers) MUST NOT cite this analysis as if it provides direct evidence for unsampled patterns. The 0.84 confidence composite applies to category-level findings; pattern-level confidence for unsampled patterns is LOWER than the category average. See per-category decomposition in PS Integration for per-row confidence assignments.

---

## Per-Category Analysis

### Architecture

**Files read:** PAT-ARCH-001 (hexagonal-architecture.md), PAT-ARCH-004 (one-class-per-file.md)

#### Current negative constraint state

PAT-ARCH-001 (Hexagonal Architecture) contains a Dependency Matrix table that expresses constraints positively (YES/NO import permissions per layer), an Enforcement section with Python test code asserting `"infrastructure" not in imp`, and a Related Patterns section. Zero NEVER/MUST NOT vocabulary in the documentation body. The Dependency Rule block quote ("Source code dependencies can only point inwards") is a positive framing.

PAT-ARCH-004 (One-Class-Per-File) contains an Anti-Patterns section with a table listing four anti-patterns, all described as "Always Avoid" with brief rationale. Positive framing only ("Enforce one public class per file").

**Observable state:** Architecture constraint vocabulary is positive + tabular. The HARD rules that actually enforce architecture boundaries (NC-018, NC-019 in supplemental-vendor-evidence.md) already use MUST NOT in `.context/rules/architecture-standards.md` — but the pattern documentation has not adopted this vocabulary.

#### Applicable NPTs

| NPT Pattern | Applicability | Rationale |
|-------------|--------------|-----------|
| NPT-009 (Declarative Behavioral Negation) | HIGH | Layer boundary violations are specific, consequential, and documentable. Perfect fit for NEVER/MUST NOT with consequence. |
| NPT-010 (Paired Prohibition + Positive Alternative) | HIGH | Each layer violation has a documented correct alternative (import from domain instead of infrastructure). AGREE-8 moderate cross-survey agreement supports pairing. |
| NPT-011 (Justified Prohibition) | MEDIUM | Why layers must not import upward (decoupling, testability) is well-established and helps define edge cases (shared kernel, composition root). |
| NPT-014-as-diagnostic | YES | The Dependency Matrix YES/NO format is structurally similar to blunt prohibition without consequence — upgrade candidate. |

#### Gaps

1. **PAT-ARCH-001 Anti-Pattern section is ABSENT.** The pattern has an Enforcement section (test code) and a Dependency Matrix but no explicit anti-pattern section naming and constraining common violations.
2. **PAT-ARCH-004 Anti-Pattern section uses NPT-014 structure.** Four anti-patterns are named but stated without: consequence documentation ("What breaks"), scope specification, or positive alternative (all four have implicit "CORRECT" pairing in associated CQRS patterns but not in this file).
3. **Composition Root violation has no explicit constraint.** Only bootstrap.py may import infrastructure adapters (NC from VS-001 documents NC-031 pattern in agent-development-standards.md) — but PAT-ARCH-001 has no prohibition statement covering this.

#### Specific recommendations

| Rec-ID | Category | Target | Recommendation | NPT Reference | Priority | Evidence Tier | Evidence Source |
|--------|----------|--------|----------------|---------------|----------|---------------|-----------------|
| ARCH-R1 | Architecture | PAT-ARCH-001 | Add Boundary Constraints section with NPT-009 format: "NEVER import infrastructure from domain layer. Consequence: layer boundary test failure; architectural integrity violated. Scope: all files in src/domain/." | NPT-009 (T4 obs, UNTESTED causal) | MUST NOT omit | T4 working practice | E-006 (NC-018, NC-019) |
| ARCH-R2 | Architecture | PAT-ARCH-001 | Pair ARCH-R1 with positive alternative per NPT-010: "Instead: define a port (protocol/abstract class) in src/domain/ports/ and implement it in src/infrastructure/." | NPT-010 (T4 obs, UNTESTED causal) | SHOULD add | T4 working practice | E-003 (AGREE-8) |
| ARCH-R3 | Architecture | PAT-ARCH-001 | Add composition root constraint per NPT-009: "NEVER import from src/infrastructure/adapters/ except in src/bootstrap.py. Consequence: DI composition breaks; testability degrades." | NPT-009 (T4 obs, UNTESTED causal) | SHOULD add | T4 working practice | E-006 (NC-031) |
| ARCH-R4 | Architecture | PAT-ARCH-004 | Upgrade anti-pattern table from NPT-014 to NPT-009 format: add consequence documentation to each of the four existing anti-patterns. | NPT-009 over NPT-014 (T1+T3, HIGH confidence: blunt anti-pattern description underperforms structured alternatives) | SHOULD upgrade | T1+T3 for NPT-014 underperformance; T4 for NPT-009 alternative | E-001 (A-20, A-15, A-31) |
| ARCH-R5 | Architecture | PAT-ARCH-004 | Add justification (NPT-011 element) to each anti-pattern: explain WHY multiple aggregates in one file is a problem (consistency boundary violation), WHY Port+Adapter colocation violates DIP. | NPT-011 (T4 obs, UNTESTED causal) | MAY add | T4 working practice | E-004 (AGREE-9) |

---

### Testing

**Files read:** PAT-TEST-001 (test-pyramid.md), PAT-TEST-002 (bdd-cycle.md)

#### Current negative constraint state

PAT-TEST-001 uses positive framing throughout (percentage distributions, "Unit tests are fast"). No anti-pattern section. PAT-TEST-002 has an Anti-Patterns section with three named anti-patterns (Writing Tests After Code, Multiple Features Per Test, Skipping Refactor Phase), all framed as WRONG/CORRECT code block contrasts. The "Golden Rules" section uses "Never Write Code Without a Failing Test" — which IS a NEVER statement but appears as a section heading, not as a scoped NPT-009 constraint with consequence.

**Notable:** "Never Write Code Without a Failing Test" is the closest existing instance of NEVER vocabulary in pattern documentation. However, it lacks consequence documentation ("What breaks if violated: your test can only verify existing behavior, not drive design") and scope specification.

#### Applicable NPTs

| NPT Pattern | Applicability | Rationale |
|-------------|--------------|-----------|
| NPT-009 (Declarative Behavioral Negation) | HIGH | BDD process violations (writing implementation before test, multiple features per test) are specific and consequential. |
| NPT-005 (Warning-Based Meta-Prompt) | MEDIUM — category-level only | The "RED phase must fail for the right reason" warning in BDD is a process gate that primes developers to verify the failure mode before proceeding. Applicability is at the category level (PAT-TEST-002 BDD cycle); no specific pattern file recommendation uses NPT-005 because the warning belongs in the BDD process narrative, not as a standalone constraint. |
| NPT-006 (Atomic Decomposition) | MEDIUM | Coverage requirements (90% line, 85% branch, 95% function) are atomic, non-overlapping sub-constraints amenable to NPT-006 structure. |
| NPT-014-as-diagnostic | YES | The "WRONG: Code already written" anti-pattern is NPT-014 equivalent — named but without consequence or scope. |

#### Gaps

1. **PAT-TEST-001 has no anti-pattern section.** The test pyramid distribution (60/15/10/5%) is presented positively. No constraint preventing inversion of the pyramid (overweighting E2E over unit tests) is documented.
2. **PAT-TEST-002 "Never Write Code Without a Failing Test" is NPT-014 format.** The NEVER statement exists but lacks scope, consequence, and exception documentation. It needs upgrade to NPT-009.
3. **Coverage requirements (PAT-TEST-001) are stated as targets, not constraints.** "Line Coverage >= 90%" in the Coverage Requirements table is positive framing. No consequence of falling below threshold is documented in the pattern.

**NPT-005 reconciliation note:** NPT-005 (Warning-Based Meta-Prompt) appears as MEDIUM applicability in the Testing category's applicable NPTs table because the BDD RED-phase warning is structurally a meta-prompt process gate. However, the constraint propagation compliance table marks NPT-005 as "not applicable to pattern documentation recommendations" — meaning no specific recommendation in this document uses NPT-005 to create a new pattern file entry. These two statements are consistent: the category has NPT-005 applicability as a structural observation, but the specific recommendations (TEST-R1 through TEST-R4) use NPT-009 because the actionable changes are scoped to individual anti-pattern constraint statements, not process-gate warnings. NEVER add TEST-R5 using NPT-005 without first verifying that PAT-TEST-002's narrative section could accommodate a meta-prompt process gate without conflating it with NPT-009 behavioral prohibitions.

#### Specific recommendations

| Rec-ID | Category | Target | Recommendation | NPT Reference | Priority | Evidence Tier | Evidence Source |
|--------|----------|--------|----------------|---------------|----------|---------------|-----------------|
| TEST-R1 | Testing | PAT-TEST-002 | Upgrade "Never Write Code Without a Failing Test" to NPT-009 format: "NEVER write implementation code before the corresponding test exists and fails for the right reason. Consequence: tests verify existing code structure, not design requirements — BDD loses its design-driving property." | NPT-009 (T4 obs, UNTESTED causal); upgrading from NPT-014 justified by T1+T3 evidence for NPT-014 underperformance | MUST NOT omit | T1+T3 for NPT-014 underperformance | E-001 (A-20, A-15, A-31) |
| TEST-R2 | Testing | PAT-TEST-002 | Add consequence documentation to three existing anti-pattern blocks: "Writing Tests After Code" → consequence: "tests discover existing structure, not drive design"; "Multiple Features Per Test" → consequence: "test failure does not pinpoint the specific feature that broke"; "Skipping Refactor" → consequence: "technical debt accumulates between iterations." | NPT-009 (T4 obs) | SHOULD add | T4 working practice | E-007 (PAT-TEST-002 observation) |
| TEST-R3 | Testing | PAT-TEST-001 | Add pyramid inversion constraint: "NEVER weight E2E tests above unit tests. Consequence: test suite becomes slow and brittle; failures are hard to localize. Target: unit 60%, E2E 5%." | NPT-009 with scope and consequence (T4 obs, UNTESTED causal) | SHOULD add | T4 working practice | E-002 (VS-001–VS-004) |
| TEST-R4 | Testing | PAT-TEST-001 | Add coverage floor constraint with paired positive: "NEVER merge code with line coverage below 90%. Instead: add missing test cases per the Coverage Requirements table before merging." | NPT-010 (T4 obs, UNTESTED causal) | MAY add | T4 working practice | E-002 (VS-001–VS-004) |

---

### CQRS

**Files read:** PAT-CQRS-001 (command-pattern.md)

#### Current negative constraint state

PAT-CQRS-001 has the most developed anti-pattern section of all sampled patterns. Three named anti-patterns: "Commands with Business Logic," "Commands Returning Data," "CRUD-y Commands." Each has WRONG/CORRECT code block contrasts with rationale. This is structurally closest to NPT-008 (Contrastive Example Pairing) — the most developed form in the catalog. However, no NEVER/MUST NOT vocabulary appears, and no consequence documentation exists beyond implicit code comments.

**Notable:** "Commands are: immutable, named as {Verb}{Noun}Command, data transfer objects, validated in handler" is positive framing. "Validation happens in handler, not in command" is a constraint expressed positively. The CQS boundary is the primary constraint domain for this category.

#### Applicable NPTs

| NPT Pattern | Applicability | Rationale |
|-------------|--------------|-----------|
| NPT-008 (Contrastive Example Pairing) | EXISTING — already partially implemented. Upgrade path to NPT-009 recommended. | WRONG/CORRECT code contrasts are NPT-008 structure. Supported by E-007 (direct pattern file observation: PAT-CQRS-001, PAT-AGG-004, PAT-ENT-003, PAT-TEST-002 all use contrastive structure). Note: A-11 (arXiv 2024) was previously cited here but was removed in I5 — web search confirmed no matching paper exists; citation was likely hallucinated in Phase 1 research. E-007 provides independent support sufficient for this applicability finding. |
| NPT-009 (Declarative Behavioral Negation) | HIGH | CQS violations (command returning data) are specific, consequential, and documentable. |
| NPT-010 (Paired Prohibition + Positive Alternative) | HIGH | All three anti-patterns already have correct alternatives. Only the explicit NEVER statement and consequence documentation are missing. |

#### Gaps

1. **Three anti-patterns use NPT-008 (contrastive examples) but lack NPT-009 consequence documentation.** The WRONG code block shows the violation; the CORRECT block shows the fix. Missing: explicit statement of what system property is violated.
2. **CQS boundary violation has no scoped MUST NOT.** "Commands returning data violates CQS" is implied by the WRONG comment but not stated as an explicit prohibition.

#### Specific recommendations

| Rec-ID | Category | Target | Recommendation | NPT Reference | Priority | Evidence Tier | Evidence Source |
|--------|----------|--------|----------------|---------------|----------|---------------|-----------------|
| CQRS-R1 | CQRS | PAT-CQRS-001 | Upgrade anti-pattern #2 (Commands Returning Data) from NPT-008 to NPT-009+NPT-010: add "NEVER return data from a command. Consequence: CQS boundary violated; read model becomes coupled to write model. Instead: return domain events; use a query to read state." | NPT-009 + NPT-010 (T4 obs, UNTESTED causal) | MUST NOT omit | T4 working practice | E-007 (PAT-CQRS-001 observation) |
| CQRS-R2 | CQRS | PAT-CQRS-001 | Add consequence to "Commands with Business Logic" anti-pattern: "NEVER include validation or business logic in command objects. Consequence: logic cannot be tested independently of command construction; handler logic becomes duplicated." | NPT-009 (T4 obs) | SHOULD add | T4 working practice | E-007 (PAT-CQRS-001 observation) |
| CQRS-R3 | CQRS | PAT-CQRS-001 | Apply same NPT-009 upgrade pattern to query-pattern.md (PAT-CQRS-002) and dispatcher-pattern.md (PAT-CQRS-004) when those files are reviewed — extrapolated from PAT-CQRS-001 findings. | NPT-009, NPT-010 | SHOULD add | T4 working practice | E-002 (VS-001–VS-004) |

---

### Aggregate

**Files read:** PAT-AGG-004 (invariant-enforcement.md)

#### Current negative constraint state

PAT-AGG-004 has the richest anti-pattern section of all sampled patterns. Three named anti-patterns: "External Invariant Checking," "Setter Methods," "Generic Exceptions." All use WRONG/CORRECT code contrasts (NPT-008 structure). The "Jerry Decision" blockquotes use positive framing ("All invariant violations raise specific exceptions, never generic ValueError").

**Notable:** The phrase "never generic ValueError" in a Jerry Decision blockquote is a NEVER statement — but it is a prose sentence, not a structured NPT-009 constraint. This is a partial, unformalized instance of NPT-009 vocabulary.

#### Applicable NPTs

| NPT Pattern | Applicability | Rationale |
|-------------|--------------|-----------|
| NPT-009 (Declarative Behavioral Negation) | HIGH | Aggregate boundary violations (external invariant checking, setter bypass) are specific and have clear consequences. |
| NPT-011 (Justified Prohibition) | HIGH | "Why don't setters work?" is a question with a clear, domain-specific answer (they bypass invariant enforcement) — ideal justification candidate per NPT-011. |
| NPT-014-as-diagnostic | YES | "never generic ValueError" in prose — upgrade to structured NPT-009 constraint. |

#### Gaps

1. **"Never generic ValueError" is NPT-014 in prose form.** It needs consequence, scope, and exception documentation to become NPT-009.
2. **PAT-AGG-004 Jerry Decision blockquotes express constraints positively.** "All invariant violations raise specific exceptions" states the rule; "NEVER raise Exception or ValueError for domain invariant violations" with consequence would be more complete.

#### Specific recommendations

| Rec-ID | Category | Target | Recommendation | NPT Reference | Priority | Evidence Tier | Evidence Source |
|--------|----------|--------|----------------|---------------|----------|---------------|-----------------|
| AGG-R1 | Aggregate | PAT-AGG-004 | Upgrade "never generic ValueError" Jerry Decision to NPT-009 format: "NEVER raise Exception or ValueError for domain invariant violations. Consequence: callers cannot distinguish between domain errors and programming errors; error handling must rely on message parsing. Scope: all aggregate method bodies. Exception: stdlib operations (e.g., file I/O) may raise standard exceptions at infrastructure layer." | NPT-009 (T4 obs, UNTESTED causal) | SHOULD upgrade | T4 working practice | E-007 (PAT-AGG-004 observation) |
| AGG-R2 | Aggregate | PAT-AGG-004 | Add NPT-011 justification to "External Invariant Checking" anti-pattern: "NEVER check aggregate invariants outside the aggregate. Reason: the caller cannot know the complete set of invariants; the aggregate's invariants may change; test isolation requires invariants to be testable through aggregate behavior only." | NPT-011 (T4 obs, UNTESTED causal) | SHOULD add | T4 working practice | E-004 (AGREE-9) |
| AGG-R3 | Aggregate | PAT-AGG-004 | Add NPT-010 positive pairing to "Setter Methods" anti-pattern: "NEVER expose public setter methods on aggregates. Instead: express state transitions as behavior methods with domain names (start(), complete(), cancel()) that enforce their own invariant checks." | NPT-010 (T4 obs, UNTESTED causal) | MAY add | T4 working practice | E-003 (AGREE-8) |

---

### Entity

**Files read:** PAT-ENT-003 (aggregate-root.md)

#### Current negative constraint state

PAT-ENT-003 has three named anti-patterns: "Anemic Aggregate," "God Aggregate," "Leaky Invariants." All use WRONG/CORRECT code contrasts (NPT-008). The "Key Principles" section uses positive framing (Reference by ID, Small Aggregates). No NEVER/MUST NOT vocabulary in documentation body.

**Notable:** The "Reference by ID" section says "CORRECT: Reference by ID / WRONG: Object reference" — a positive/negative code contrast but without explicit prohibition statement.

#### Applicable NPTs

| NPT Pattern | Applicability | Rationale |
|-------------|--------------|-----------|
| NPT-009 (Declarative Behavioral Negation) | HIGH | Direct object reference (instead of ID reference) is specific, consequential (coupling aggregates, violating consistency boundaries), and documentable. |
| NPT-010 (Paired Prohibition + Positive Alternative) | HIGH | All anti-patterns have documented correct alternatives. |

#### Gaps

1. **"Leaky Invariants" anti-pattern lacks consequence documentation.** The CORRECT/WRONG contrast is present but no statement of what specifically breaks when invariants leak.
2. **PAT-ENT-001 (IAuditable) and PAT-ENT-002 (IVersioned) are extrapolated as likely lacking anti-pattern sections** — protocol-based patterns typically document the protocol positively without specifying what happens when the protocol is violated.

#### Specific recommendations

| Rec-ID | Category | Target | Recommendation | NPT Reference | Priority | Evidence Tier | Evidence Source |
|--------|----------|--------|----------------|---------------|----------|---------------|-----------------|
| ENT-R1 | Entity | PAT-ENT-003 | Upgrade "Leaky Invariants" to NPT-009+NPT-010: "NEVER check or enforce aggregate invariants from caller code. Consequence: consistency boundary is violated; the aggregate can be placed in an invalid state by any caller that bypasses the aggregate's behavior methods. Instead: call aggregate behavior methods and let the aggregate enforce internally." | NPT-009 + NPT-010 (T4 obs, UNTESTED causal) | SHOULD add | T4 working practice | E-007 (PAT-ENT-003 observation) |
| ENT-R2 | Entity | PAT-ENT-003 | Add consequence to "Anemic Aggregate": "NEVER use setter methods as the primary mutation API. Consequence: domain logic migrates to application/command handlers; the aggregate becomes a data container with no behavioral ownership of its own invariants." | NPT-009 (T4 obs) | SHOULD add | T4 working practice | E-007 (PAT-ENT-003 observation) |

---

### Repository

**Files read:** PAT-REPO-002 (event-sourced-repository.md)

#### Current negative constraint state

PAT-REPO-002 uses positive framing entirely in its overview and implementation sections. No anti-pattern section was visible in the sampled 80 lines. The overview quote from Vaughn Vernon ("append events, never update") contains the word "never" but in a citation context, not as a structured constraint.

**Sampling note:** The 80-line sample for this file creates a risk that the anti-pattern section is absent in the sample but present in the full file. Recommendations for this category should be verified against the full file before implementation.

#### Applicable NPTs

| NPT Pattern | Applicability | Rationale |
|-------------|--------------|-----------|
| NPT-009 (Declarative Behavioral Negation) | HIGH | Event store violations (updating instead of appending, reading across aggregates in one call) are specific and consequential. |
| NPT-011 (Justified Prohibition) | HIGH | "Why never update events?" has a specific domain answer (immutability, auditability, replay correctness) — ideal NPT-011 candidate. |

#### Gaps

1. **No anti-pattern section visible in the sample.** Event sourcing has critical failure modes (updating stored events, bypassing the repository to read raw event streams, loading more events than needed) that are commonly misunderstood.
2. **"Append events, never update" is T4 practitioner observation embedded in a citation.** It should become an explicit NPT-009 constraint in the pattern documentation.

#### Specific recommendations

| Rec-ID | Category | Target | Recommendation | NPT Reference | Priority | Evidence Tier | Evidence Source |
|--------|----------|--------|----------------|---------------|----------|---------------|-----------------|
| REPO-R1 | Repository | PAT-REPO-002 | Add anti-pattern section with at minimum: "NEVER modify or delete stored events. Consequence: event replay produces incorrect aggregate state; auditability and temporal queries are broken. Reason: events are facts — they happened and are immutable by domain semantics." | NPT-009 + NPT-011 (T4 obs, UNTESTED causal) | MUST NOT omit | T4 working practice | E-002 (VS-001–VS-004) |
| REPO-R2 | Repository | PAT-REPO-002 | Add constraint against cross-aggregate event loading: "NEVER load events from multiple aggregate streams in a single repository call. Consequence: query semantics cross aggregate consistency boundaries; performance degrades non-linearly." | NPT-009 (T4 obs) | SHOULD add | T4 working practice | E-002 (VS-001–VS-004) |

---

### Adapter

**Files read:** PAT-ADP-001 (cli-adapter.md)

#### Current negative constraint state

PAT-ADP-001's sampled section (80 lines) shows positive framing in the overview and class docstring. The docstring notes "No business logic - only translation" — a constraint expressed positively. No NEVER/MUST NOT vocabulary visible in the sample.

#### Applicable NPTs

| NPT Pattern | Applicability | Rationale |
|-------------|--------------|-----------|
| NPT-009 (Declarative Behavioral Negation) | MEDIUM | CLI adapter violations (containing business logic, importing domain directly bypassing dispatcher) are specific. |
| NPT-003 (Output Boundary in task terms) | HIGH | The adapter-to-application boundary is the primary constraint domain. |

#### Gaps

1. **"No business logic - only translation" is a positive constraint without enforcement vocabulary.** Should be expressed as a prohibition to prevent gradual violation.
2. **No anti-pattern section visible in the sample** — extrapolated from similar adapter patterns.

#### Specific recommendations

| Rec-ID | Category | Target | Recommendation | NPT Reference | Priority | Evidence Tier | Evidence Source |
|--------|----------|--------|----------------|---------------|----------|---------------|-----------------|
| ADP-R1 | Adapter | PAT-ADP-001 | Add constraint: "NEVER implement business logic in adapter classes. Consequence: business rules become coupled to delivery mechanism; testing requires CLI invocation. Scope: all classes in src/interface/ and src/infrastructure/adapters/." | NPT-009 (T4 obs, UNTESTED causal) | MAY add (reclassified in implementation sequencing due to 80-line sample risk) | T4 working practice | E-006 (NC-018 architectural pattern) |
| ADP-R2 | Adapter | PAT-ADP-001 | Add constraint: "NEVER import from src/domain/ directly in adapters; use dispatcher ports. Consequence: adapter becomes tightly coupled to domain model; port abstraction is bypassed." | NPT-009 + NPT-011 (T4 obs, UNTESTED causal) | MAY add (reclassified in implementation sequencing due to 80-line sample risk) | T4 working practice | E-006 (NC-019 architectural pattern) |

---

### Domain Service

**Files read:** PAT-SVC-001 (domain-service.md)

#### Current negative constraint state

PAT-SVC-001's sampled section (60 lines) shows positive framing. "Use a Domain Service when: [four conditions]" is positive. No anti-pattern section visible. The "Design Notes" field in the QualityValidator class docstring: none visible in sample.

#### Applicable NPTs

| NPT Pattern | Applicability | Rationale |
|-------------|--------------|-----------|
| NPT-009 (Declarative Behavioral Negation) | MEDIUM | Domain service overuse (using a service when an entity method would do) and underuse (putting cross-aggregate logic in a handler) are specific failure modes. |

#### Gaps

1. **No anti-pattern section exists (extrapolated from sample).** Domain service vs. application service confusion is a well-known DDD pitfall; currently no constraint prevents misclassification.
2. **"Use when" criteria are positive but have no corresponding "NEVER use when" constraints.**

#### Specific recommendations

| Rec-ID | Category | Target | Recommendation | NPT Reference | Priority | Evidence Tier | Evidence Source |
|--------|----------|--------|----------------|---------------|----------|---------------|-----------------|
| SVC-R1 | Domain Service | PAT-SVC-001 | Add anti-pattern section: "NEVER use a Domain Service for logic that belongs to a single entity or value object. Consequence: entity behavior migrates out of the entity; anemic domain model emerges. Instead: add the behavior method to the relevant entity." | NPT-009 + NPT-010 (T4 obs, UNTESTED causal) | SHOULD add | T4 working practice | E-002 (VS-001–VS-004) |
| SVC-R2 | Domain Service | PAT-SVC-001 | Add distinction constraint: "NEVER inject infrastructure concerns (repositories, event stores) directly into a Domain Service. Consequence: domain layer gains infrastructure dependency; hexagonal architecture boundary violated. Instead: inject repository ports (interfaces), not implementations." | NPT-009 + NPT-010 (T4 obs, UNTESTED causal) | SHOULD add | T4 working practice | E-006 (NC-018 pattern) |

---

### Event

**Files read:** PAT-EVT-001 (domain-event.md)

#### Current negative constraint state

PAT-EVT-001 docstring note: "Named in past tense (TaskCreated, not TaskCreate)." This is a constraint expressed as naming convention guidance — positive framing with an inline negative example. No NEVER/MUST NOT vocabulary. No anti-pattern section visible in the 60-line sample.

#### Applicable NPTs

| NPT Pattern | Applicability | Rationale |
|-------------|--------------|-----------|
| NPT-009 (Declarative Behavioral Negation) | MEDIUM | Event mutation (events are immutable — frozen=True enforced by dataclass), re-publication of past events as new events, and event naming violations are specific failure modes. |
| NPT-006 (Atomic Decomposition) | LOW | Event fields are individually constrained (frozen, timestamped, aggregate-scoped) — could be expressed as NPT-006 atomic sub-constraints. Low priority given programmatic enforcement via frozen=True. |

#### Gaps

1. **"frozen=True" enforces immutability programmatically (NPT-003 equivalent).** Documentation constraint adds marginal value for this specific failure mode, but naming and publishing failure modes are not programmatically enforced.

#### Specific recommendations

| Rec-ID | Category | Target | Recommendation | NPT Reference | Priority | Evidence Tier | Evidence Source |
|--------|----------|--------|----------------|---------------|----------|---------------|-----------------|
| EVT-R1 | Event | PAT-EVT-001 | Add naming constraint: "NEVER name domain events in present or future tense. Consequence: event name implies intent (command) rather than fact (event); CQRS boundary becomes ambiguous. Exception: none — all domain events MUST use past tense." | NPT-009 (T4 obs, UNTESTED causal) | SHOULD add | T4 working practice | E-002 (VS-001–VS-004) |
| EVT-R2 | Event | PAT-EVT-001 | Add re-publication constraint: "NEVER re-publish historical events as new events with new timestamps. Consequence: event stream becomes inconsistent; replay produces different state at different times." | NPT-009 (T4 obs) | MAY add | T4 working practice | E-002 (VS-001–VS-004) |

---

### Identity

**Files read:** PAT-ID-003 (jerry-uri.md)

#### Current negative constraint state

PAT-ID-003's 60-line sample shows positive framing. URI format specification uses examples only. No NEVER/MUST NOT vocabulary. No anti-pattern section visible.

#### Applicable NPTs

| NPT Pattern | Applicability | Rationale |
|-------------|--------------|-----------|
| NPT-009 (Declarative Behavioral Negation) | LOW-MEDIUM | Identity pattern violations (using string IDs instead of typed VertexId, constructing JerryUri from non-canonical formats) are specific but largely programmatically preventable. |

#### Gaps

1. **URI format violations have no documented constraint.** What happens if a non-canonical URI format is used in cross-system references is undocumented.

#### Specific recommendations

| Rec-ID | Category | Target | Recommendation | NPT Reference | Priority | Evidence Tier | Evidence Source |
|--------|----------|--------|----------------|---------------|----------|---------------|-----------------|
| ID-R1 | Identity | PAT-ID-001/002 | Add constraint to domain-specific ID patterns: "NEVER use raw string IDs in domain method signatures where a typed ID is defined. Consequence: type safety is lost; incorrect ID types can be passed without compile-time detection." | NPT-009 (T4 obs, UNTESTED causal) | MAY add | T4 working practice | E-002 (VS-001–VS-004) |

---

### Value Object

**Files read:** PAT-VO-001 (immutable-value-object.md)

#### Current negative constraint state

PAT-VO-001's 60-line sample uses positive framing. "frozen=True: Makes instance immutable (assignment raises FrozenInstanceError)" documents the mechanism positively. No anti-pattern section visible in sample.

#### Applicable NPTs

| NPT Pattern | Applicability | Rationale |
|-------------|--------------|-----------|
| NPT-009 (Declarative Behavioral Negation) | MEDIUM | Value object mutation violations are specific and have documented consequences (FrozenInstanceError). |

#### Gaps

1. **Mutability constraint is documented positively via frozen=True explanation.** The constraint exists (FrozenInstanceError is documented) but as a mechanism description, not as a behavioral prohibition.

#### Specific recommendations

| Rec-ID | Category | Target | Recommendation | NPT Reference | Priority | Evidence Tier | Evidence Source |
|--------|----------|--------|----------------|---------------|----------|---------------|-----------------|
| VO-R1 | Value Object | PAT-VO-001 | Add constraint: "NEVER use mutable data structures (lists, dicts) as value object fields. Consequence: value object identity by equality breaks; frozen=True does not prevent mutation of contained mutable objects." | NPT-009 (T4 obs) | SHOULD add | T4 working practice | E-007 (PAT-VO-001 observation) |

---

### Skill Development

**Files read:** PAT-SKILL-001 (skill-structure.md)

#### Current negative constraint state

PAT-SKILL-001 has an Anti-Patterns section (in the format "What to avoid"), visible from the Document Sections table. The SKILL.md Template section uses positive framing for frontmatter fields. The Key Rules section references HARD rules H-25 through H-30 — these HARD rules in skill-standards.md do use MUST NOT vocabulary (e.g., "Skill name MUST NOT contain 'claude' or 'anthropic'" — NC-016 in VS-001 catalog), but this is referenced by citation, not reproduced in the pattern documentation.

**Notable:** This is the only pattern category where the pattern documentation explicitly references external HARD rules (H-25–H-30 in skill-standards.md). This creates an architectural asymmetry: the rules exist and are enforced in the rules layer, but pattern documentation relies on the reference rather than stating the constraints directly.

**Extrapolation confidence note (I2 fix #6):** PAT-SKILL-001 anti-pattern section content was NOT sampled — only the section title was visible in the Document Sections navigation table. The SKILL-R4 recommendation below is extrapolated from the section title "What to avoid" combined with the Key Rules citations (H-25–H-30). Confidence for SKILL-R4 is LOW; verification of the full anti-pattern section content is required before implementing SKILL-R4. All other SKILL-R1 through SKILL-R3 recommendations derive from Key Rules citations and constitutional triplet requirements that are verifiable independently of the anti-patterns section content.

#### Applicable NPTs

| NPT Pattern | Applicability | Rationale |
|-------------|--------------|-----------|
| NPT-012 (L2 Re-Injected Constraint) | HIGH — observational | The H-25/H-30 rules cited by PAT-SKILL-001 are already subject to L2 re-injection in the HARD rules layer. Pattern documentation can reference this as a design property. |
| NPT-009 (Declarative Behavioral Negation) | MEDIUM | Skill structure violations (README.md inside skill folder, multiple agents in SKILL.md body, non-kebab-case naming) are specific failure modes. |
| NPT-013 (Constitutional Triplet) | RELEVANT | Every agent within a skill MUST declare the P-003/P-020/P-022 constitutional triplet (H-35). This is a mandatory pattern for skill development that PAT-SKILL-001 should document explicitly. |

#### Gaps

1. **PAT-SKILL-001 references H-25 through H-30 by citation but does not reproduce the MUST NOT constraints.** A developer reading only the pattern file sees positive guidance and a citation, not the specific prohibitions.
2. **Constitutional triplet requirement (NPT-013) is not mentioned in PAT-SKILL-001.** Every agent definition in a skill must include the P-003/P-020/P-022 prohibition triplet — this is a mandatory structural requirement for skill development not documented in the pattern file.
3. **Anti-patterns section content not sampled (only title visible).** Extrapolating from section structure that violations may not have consequence documentation — LOW confidence.

#### Specific recommendations

| Rec-ID | Category | Target | Recommendation | NPT Reference | Priority | Evidence Tier | Evidence Source |
|--------|----------|--------|----------------|---------------|----------|---------------|-----------------|
| SKILL-R1 | Skill Dev | PAT-SKILL-001 | Add explicit NPT-009 constraint for the prohibition already in H-25: "NEVER name a skill folder with uppercase letters, spaces, or underscores. Consequence: skill is not discovered by activation-keyword routing; H-25 HARD rule violation flagged at CI. Format: lowercase-kebab-case only." | NPT-009 (T4 obs, UNTESTED causal — reproducing existing HARD rule in pattern documentation) | SHOULD add | T4 obs + H-25 HARD rule | E-006 (H-25 enforcement) |
| SKILL-R2 | Skill Dev | PAT-SKILL-001 | Add constitutional triplet requirement: "NEVER create an agent definition without the P-003/P-020/P-022 constitutional triplet in capabilities.forbidden_actions. Consequence: H-35 HARD rule violation; agent definition fails CI schema validation." | NPT-013 (T4 obs, schema-mandatory per H-35) | MUST NOT omit | T4 obs + H-35 schema | E-006 (H-35 schema requirement) |
| SKILL-R3 | Skill Dev | PAT-SKILL-001 | Add README.md prohibition: "NEVER create a README.md inside a skill folder. Consequence: SKILL.md is the canonical documentation; README.md creates a competing source of truth. H-27 (retired, now H-25 sub-item) violation." | NPT-009 (T4 obs) | SHOULD add | T4 obs + H-25 | E-006 (H-25 sub-item) |
| SKILL-R4 | Skill Dev | PAT-SKILL-001 | Add context compaction note (NPT-012 pattern): "Enforcement-tier skill rules that use NEVER/MUST NOT vocabulary SHOULD use L2-REINJECT markers. Reason: T-004 failure mode — NEVER rules may be dropped under context compaction. This is T4 observational evidence; causal contribution of re-injection vs. vocabulary is UNTESTED." **Confidence: LOW — anti-pattern section content not sampled; verify full file before implementing.** | NPT-012 (T4 obs, UNTESTED causal, with explicit T-004 caveat) | MAY add | T4 obs only | E-005 (I-28, I-32, T-004) |

---

## Anti-Pattern Integration Recommendations

This section provides a systematic approach to adding negative-constraint anti-pattern sections to pattern documentation. It is organized as an upgrade protocol applicable across all 12 categories.

### The NPT-014-to-NPT-009 Upgrade Protocol

NEVER apply this upgrade protocol without verifying that the resulting constraint meets all three NPT-009 criteria (specificity, scope, consequence). An incomplete upgrade produces a longer NPT-014 pattern, not an NPT-009 pattern.

**Three-step upgrade protocol (working practice, T4 observational, UNTESTED causal):**

#### Step 1: Identify NPT-014 candidates in existing documentation

NPT-014 diagnostic criteria (from taxonomy-pattern-catalog.md Pattern Catalog Entries, NPT-014):
- Standalone negative instruction without specificity, consequence, pairing, or context
- Expressed as "WRONG/CORRECT" code contrast without accompanying prohibition statement
- Positive constraint statement that contains an implicit negative ("use X instead of Y" = implicit "NEVER use Y")
- NEVER/MUST NOT statements in prose without scope or consequence

**Observable instances in sampled patterns:**

| File | Location | Current Form | NPT-014 Type |
|------|----------|--------------|-------------|
| bdd-cycle.md | Golden Rules section | "Never Write Code Without a Failing Test" (heading) | Prose NEVER without scope/consequence |
| invariant-enforcement.md | Jerry Decision blockquote | "never generic ValueError" | Prose NEVER without scope/consequence |
| aggregate-root.md | Key Principles | "CORRECT: Reference by ID / WRONG: Object reference" | Positive/negative contrast without prohibition |
| command-pattern.md | Anti-Patterns #1–3 | WRONG/CORRECT code blocks | NPT-008 contrastive; missing NEVER statement + consequence |
| entity/aggregate-root.md | Anti-Patterns | WRONG/CORRECT blocks | NPT-008 without prohibition statement |

#### Step 2: Apply NPT-009 structural upgrade

For each NPT-014 candidate, add the three NPT-009 structural elements:

```markdown
## Anti-Patterns

### [Anti-Pattern Name]

NEVER [specific action].

Consequence: [what specifically breaks — system property, test property, architectural property].
Scope: [where this constraint applies — layer, class type, method type].
Exception: [only if a documented exception exists — most constraints have none].

Instead: [positive alternative — makes this NPT-010 as well].
Reason: [why this constraint exists — makes this NPT-011 as well].
```

**Template example (applying to PAT-CQRS-001 Anti-Pattern #2):**

```markdown
### Commands Returning Data

NEVER return domain data from a command handler.

Consequence: Command-Query Separation (CQS) boundary is violated; the read model becomes
coupled to the write model; queries cannot be independently scaled or cached.
Scope: All methods implementing ICommandHandler; all command handler handle() methods.
Exception: Returning domain events is permitted — events are facts about state changes,
not domain state itself.

Instead: Return list[DomainEvent] from the command handler, then issue a separate query
to read the resulting state.
Reason: CQS requires that operations either change state (commands) or return data
(queries), never both. This enables independent optimization of read and write paths.
```

#### Step 3: Assign NPT-ID and evidence tier in documentation

Each anti-pattern section should include a minimal evidence label to maintain traceability to the research taxonomy. Proposed format:

```markdown
> **NPT Reference:** NPT-009 (T4 observational, UNTESTED causal comparison)
> See: PROJ-014 taxonomy-pattern-catalog.md
```

NEVER use this label to imply that negative framing is experimentally validated as superior to a positive-framing alternative in the same position. The label provides traceability, not validation.

### Anti-Pattern Section Standard (proposed)

All pattern files in `.context/patterns/` SHOULD include an Anti-Patterns section that follows this structure. The standard is a working practice recommendation, not a HARD rule. It is reversible under PG-003 contingency.

```markdown
## Anti-Patterns

> Evidence tier for all anti-pattern constraints in this section: T4 observational
> (working practice). Causal comparison against positive-framing equivalents is
> UNTESTED per PROJ-014-negative-prompting-research Phase 2 experimental gap.

### [Anti-Pattern Name]

NEVER [specific action].

Consequence: [what breaks].
Scope: [where this applies].
Exception: [documented exceptions only].

Instead: [positive alternative].
```

---

## Pattern Catalog Update Recommendations

**Target file:** `.context/patterns/PATTERN-CATALOG.md`

### Current state assessment

PATTERN-CATALOG.md (100 lines sampled) is a navigation index with three columns (ID, Pattern, Status, Detail File). Category sections are mostly populated for Identity and Entity; Aggregate, Event, CQRS, and Repository sections appear to have incomplete content (blank lines visible in the sample). No anti-pattern metadata or negative constraint vocabulary appears in the catalog.

### Recommendations

| Rec-ID | Target | Recommendation | NPT Reference | Priority |
|--------|--------|----------------|---------------|----------|
| CAT-R1 | PATTERN-CATALOG.md | Add "Anti-Pattern Coverage" column to each category table indicating whether the pattern file includes an NPT-009 anti-pattern section. Values: PRESENT / ABSENT / PARTIAL. This provides a gap tracking mechanism without modifying individual files. | N/A (metadata) | SHOULD add |
| CAT-R2 | PATTERN-CATALOG.md | Add a global Anti-Pattern Standard section referencing the upgrade protocol in this analysis. Provides a canonical location for the standard. | NPT-009 as structural guidance | SHOULD add |
| CAT-R3 | PATTERN-CATALOG.md | Complete the partially populated sections in 4 confirmed categories: PAT-AGG, PAT-EVT, PAT-CQRS, and PAT-REPO all had blank table rows visible in the 100-line catalog sample. Precise row count per category requires full-file verification [count not determinable from 100-line sample — the 100-line sample showed at minimum 1 blank row per category section; implementer MUST verify against full PATTERN-CATALOG.md before completing]. Anti-pattern coverage metadata cannot be added to blank rows. | N/A | MUST NOT omit |

---

## Implementation Sequencing

**34 recommendations grouped into Phase 5 priority groups.** (I4 correction: I1/I2/I3 stated "28" incorrectly. Actual count verified by explicit Rec-ID enumeration: ARCH-R1/R2/R3/R4/R5 = 5; TEST-R1/R2/R3/R4 = 4; CQRS-R1/R2/R3 = 3; AGG-R1/R2/R3 = 3; ENT-R1/R2 = 2; REPO-R1/R2 = 2; SVC-R1/R2 = 2; ADP-R1/R2 = 2; EVT-R1/R2 = 2; ID-R1 = 1; VO-R1 = 1; SKILL-R1/R2/R3/R4 = 4; CAT-R1/R2/R3 = 3. Total = 5+4+3+3+2+2+2+2+2+1+1+4+3 = 34. Group 1 (6) + Group 2 (18) + Group 3 (10) = 34 confirmed.)

*Priority legend: "MUST NOT omit" = Phase 5 ADR must address before closure; "SHOULD add" = implement with Phase 5 ADR approval; "MAY add" = post-Phase 2 optional enhancement.*

### Group 1: MUST NOT omit (implement before Phase 5 ADR finalization)

These 6 recommendations address the highest-confidence gaps and can be implemented before Phase 2 experimental results because they are either justified by T1 evidence (NPT-014 upgrade) or are schema-mandatory (NPT-013 constitutional triplet).

| Rec-ID | Category | Rationale for Group 1 |
|--------|----------|-----------------------|
| ARCH-R1 | Architecture | NPT-009 boundary constraint; core architectural correctness gap |
| TEST-R1 | Testing | NPT-014 → NPT-009 upgrade; T1 evidence (E-001) justifies immediate action |
| CQRS-R1 | CQRS | CQS boundary constraint; highest-risk gap in the most-developed anti-pattern section |
| REPO-R1 | Repository | Event immutability constraint; critical failure mode with no current documentation |
| SKILL-R2 | Skill Dev | NPT-013 constitutional triplet; schema-mandatory per H-35; no Phase 2 dependency |
| CAT-R3 | PATTERN-CATALOG | Complete blank rows; prerequisite for all CAT-R1/CAT-R2 metadata additions |

### Group 2: SHOULD add (implement with Phase 5 ADR approval)

18 recommendations (14 category recommendations + 4 catalog/skill updates) that add high-value structural improvements. These can be sequenced with Phase 5 ADR writing and implemented in the same pass.

| Rec-ID | Category |
|--------|----------|
| ARCH-R2 | Architecture |
| ARCH-R3 | Architecture |
| ARCH-R4 | Architecture |
| TEST-R2 | Testing |
| TEST-R3 | Testing |
| CQRS-R2 | CQRS |
| CQRS-R3 | CQRS |
| AGG-R1 | Aggregate |
| AGG-R2 | Aggregate |
| ENT-R1 | Entity |
| ENT-R2 | Entity |
| REPO-R2 | Repository |
| SVC-R1 | Domain Service |
| SVC-R2 | Domain Service |

Additional SHOULD add from catalog updates:

| Rec-ID | Category |
|--------|----------|
| SKILL-R1 | Skill Dev |
| SKILL-R3 | Skill Dev |
| CAT-R1 | PATTERN-CATALOG |
| CAT-R2 | PATTERN-CATALOG |

*(Total Group 2: 18 — the 14 category recommendations plus 4 listed here; CAT-R1/CAT-R2 and SKILL-R1/SKILL-R3 are SHOULD add priority)*

### Group 3: MAY add (post-Phase 2, optional enhancements)

10 recommendations that are optional enhancements after Phase 2 experimental results confirm or qualify framing choices.

| Rec-ID | Category | Note |
|--------|----------|------|
| ARCH-R5 | Architecture | NPT-011 justification additions; framing-dependent value |
| TEST-R4 | Testing | Coverage floor NPT-010 pair; enhancement |
| AGG-R3 | Aggregate | NPT-010 positive pairing; enhancement |
| ADP-R1 | Adapter | Structural addition; useful but not critical |
| ADP-R2 | Adapter | Structural addition; useful but not critical |
| EVT-R1 | Event | Naming constraint; low-risk enhancement |
| EVT-R2 | Event | Re-publication constraint; low-priority |
| ID-R1 | Identity | Typed ID constraint; low-risk |
| VO-R1 | Value Object | Mutable field constraint; low-risk |
| SKILL-R4 | Skill Dev | LOW confidence (partial sample); verify before implementing |

*(Group 3 total: 10 — ADP-R1 and ADP-R2 are MAY add here due to 80-line sample risk; the Adapter category recommendation table has been updated to reflect the same MAY add priority (I3 fix #1). The L0 recommendation summary counts have been updated accordingly: SHOULD add = 18, MAY add = 10.)*

---

## Evidence Gap Map

**NEVER interpret this table as evidence that negative framing is superior to positive framing.** The T1 evidence column confirms only that NPT-014 (blunt prohibition) underperforms structured alternatives — it does NOT confirm that NPT-009 through NPT-011 outperform positive alternatives. The T4 column confirms observational use, not causal effectiveness.

| Recommendation Group | T1 Evidence Applicable | T4 Observational | Untested (controlled) | Action Permitted Under Evidence |
|---------------------|----------------------|------------------|----------------------|---------------------------------|
| NPT-014 → NPT-009 upgrades (all categories) | YES — T1 evidence (A-20, A-15, A-31) establishes NPT-014 underperforms structured alternatives (HIGH confidence) | YES — VS-001–VS-004, 33 instances of NPT-009 pattern in production | YES — whether NPT-009 outperforms equivalent positive framing is UNTESTED | PERMITTED: upgrading from NPT-014 is justified by T1 evidence; the upgrade destination (NPT-009) is T4 working practice |
| Adding positive alternatives (NPT-010 element) | MODERATE — AGREE-8 (2-of-3 surveys) supports pairing | YES — NP-002 pattern observed in Anthropic, OpenAI, LlamaIndex documentation | YES — causal contribution UNTESTED | PERMITTED as working practice; NEVER as validated improvement |
| Adding justifications (NPT-011 element) | LOW — AGREE-9 (2-of-3 surveys) | YES — NP-003 pattern in vendor docs | YES — causal contribution UNTESTED | PERMITTED as working practice; NEVER as validated improvement |
| NPT-008 contrastive pairing (CQRS, Aggregate, Entity) | T4 observational (E-007: direct pattern file observation) | YES — NP-002 pattern in vendor docs | YES — causal contribution UNTESTED | PERMITTED as working practice; supported by E-007 (direct observation of contrastive structure in sampled pattern files). Note: A-11 (arXiv 2024) was removed in I5 — web search confirmed no matching paper; citation was likely hallucinated. E-007 provides independent support. |
| L2-REINJECT additions (NPT-012 element) | NONE — T4 mechanically verified | YES — L2-REINJECT mechanism directly observable in quality-enforcement.md | YES — vocabulary contribution vs. re-injection frequency is UNTESTED | PERMITTED as failure-mode mitigation (T-004); NEVER as framing validation |
| Constitutional triplet in skills (NPT-013) | NONE — schema-mandatory | YES — H-35 schema compliance observable | YES — schema-mandatory; predates effectiveness evidence | REQUIRED by H-35 schema, not by effectiveness evidence |

---

## PG-003 Contingency Plan

**Mandatory per Phase 4 constraint (barrier-2/synthesis.md ST-5):**

> NEVER ignore PG-003's contingency: if Phase 2 finds a null framing effect at ranks 9–11, vocabulary choice becomes convention-determined, not effectiveness-determined. Phase 4 design should be reversible on the vocabulary dimension.

### PG-003 Contingency: What happens if Phase 2 finds a null framing effect?

**Scenario:** Phase 5 experimental results show that structured negative constraints (NPT-009, C3 condition) produce equivalent outcomes to structurally equivalent positive instructions (C1 condition) on the primary metric (hallucination rate) and secondary metric (behavioral compliance).

**Impact assessment per recommendation group:**

| Recommendation Group | Reversible? | Reversal Cost | Reversal Method | What Survives Null Result |
|---------------------|-------------|---------------|-----------------|--------------------------|
| NPT-014 → NPT-009 upgrades | YES — HIGH reversibility | Low (text changes in pattern files) | Replace NEVER/MUST NOT with positive-framing equivalents; keep consequence documentation and scope specification | Consequence documentation, scope specification, and anti-pattern naming survive — only the NEVER vocabulary is reversible. The structural improvement is independent of framing vocabulary. |
| NPT-010 positive alternative additions | YES — survives null result | None (adding positive alternatives is beneficial regardless) | Nothing to revert; paired positive alternatives are the positive-framing equivalent | The positive alternative text survives unchanged as positive framing. |
| NPT-011 justification additions | YES — survives null result | None | Nothing to revert; justifications are framing-neutral | Justification text is framing-neutral; it survives any Phase 2 outcome. |
| NPT-012 L2-REINJECT additions | YES — MEDIUM reversibility | Medium (framework mechanism changes required) | Remove L2-REINJECT markers from pattern documentation guidance; keep the underlying constraint content | Re-injection frequency is a mechanism question, not a framing question; survives null result if reformulated positively. |
| Anti-Pattern Section Standard | YES — HIGH reversibility | Low (rename "NEVER" to "Prefer not to" or equivalent) | Replace prohibition vocabulary with preferred-practice vocabulary | The structural template (named anti-pattern + consequence + scope + positive alternative + justification) is fully reversible on vocabulary dimension. |
| Constitutional triplet (H-35, NPT-013) | NO — schema-mandatory | Cannot be reversed without H-35 rule change | H-35 requires P-003/P-020/P-022 in forbidden_actions. If Phase 2 null result warrants reconsideration, a separate ADR is required. | Schema requirement predates effectiveness evidence; null result does not retroactively change the design rationale. |

### Reversibility architecture

**The key design insight:** NEVER/MUST NOT vocabulary is a thin layer over structural improvements (consequence documentation, scope specification, anti-pattern naming, positive alternatives, justifications). ALL structural improvements survive a null Phase 2 result. The reversibility operation is: find-replace NEVER/MUST NOT → "Prefer not to" / "Avoid" without losing any structural content.

This means the current recommendations can be implemented WITHOUT WAITING for Phase 2 results, with the explicit understanding that if Phase 2 produces a null framing effect, the vocabulary will be recalibrated to convention-based rather than effectiveness-based language.

**NEVER implement the Anti-Pattern Section Standard with language claiming experimental validation of negative framing.** Every anti-pattern constraint in pattern files MUST carry the T4 evidence tier label. This is both accurate and reversibility-preserving.

---

## Phase 5 Downstream Inputs

Phase 5 (ADR writing per orchestration plan) needs the following from this analysis:

### ADR inputs

1. **The Anti-Pattern Section Standard template** (from Anti-Pattern Integration Recommendations section) as the proposed design for the ADR's Context and Decision sections.

2. **The 34 categorized recommendations** as the Consequences section evidence — each recommendation is traceable to a specific NPT pattern with evidence tier.

3. **The PG-003 reversibility table** as the Alternatives Considered section — it documents the null-result scenario and the vocabulary rollback protocol.

4. **The evidence tier distribution** (T1 for NPT-014 downgrade; T4 for NPT-009 upgrade destination; T4 for NPT-010 through NPT-012) for the Rationale section.

5. **The constraint propagation compliance block** (see below) for the ADR's non-functional requirements section.

### What Phase 5 MUST NOT do

- MUST NOT claim the Anti-Pattern Section Standard is experimentally validated — it is T4 working practice.
- MUST NOT propose irreversible vocabulary changes (e.g., automated code generation that embeds NEVER syntax in generated code) — reversibility must be preserved.
- MUST NOT scope the ADR to "all 49 patterns" without verifying remaining unsampled patterns against the representative sample findings. Category-level extrapolation is permitted but individual pattern verification is required before mass update.
- MUST NOT reference NPT-009 through NPT-013 without the full evidence label (T4 observational, UNTESTED causal comparison).

### Phase 2 experimental condition preservation

**MUST NOT modify any pattern file to couple negative framing vocabulary to enforcement mechanisms** in ways that would make Phase 2 conditions C3 (structured negative constraint) and C1 (positive control) unreproducible. Specifically:
- Anti-pattern sections in pattern files are developer-facing documentation, not LLM-agent prompts. They do not participate in the C1/C3 conditions directly.
- However, if pattern documentation is used to generate prompts or constraints dynamically (e.g., for LLM-assisted code review), the vocabulary coupling concern applies.
- Phase 5 ADR MUST explicitly scope the vocabulary change to human-facing documentation only, not to LLM-runtime constraint generation.

---

## Constraint Propagation Compliance

**Required per taxonomy-pattern-catalog.md PS Integration: "Phase 4 artifacts MUST include a 'Constraint Propagation Compliance' section."**

| NPT Pattern Cited | Evidence Tier Co-cited | Causal Confidence Co-cited | Compliant? |
|-------------------|----------------------|---------------------------|------------|
| NPT-009 (Declarative Behavioral Negation) | T4 observational, VS-001–VS-004 | UNTESTED causal comparison vs. positive equivalent | YES — co-cited throughout per-category tables |
| NPT-010 (Paired Prohibition + Positive Alternative) | T4 observational (AGREE-8, NP-002) | UNTESTED causal | YES — co-cited in recommendation tables |
| NPT-011 (Justified Prohibition) | T4 observational (AGREE-9, NP-003) | UNTESTED causal | YES — co-cited in recommendation tables |
| NPT-012 (L2 Re-Injected Constraint) | T4 observational (mechanically verified) | LOW / vocabulary contribution UNTESTED | YES — co-cited with T-004 caveat |
| NPT-013 (Constitutional Triplet) | T4 observational / schema-mandatory (H-35) | UNTESTED / schema-mandatory; predates effectiveness evidence | YES — explicitly noted |
| NPT-014 (Standalone Blunt Prohibition, anti-pattern reference) | T1+T3 for UNDERPERFORMANCE (A-20, A-15, A-31, A-19) | HIGH for underperformance finding; NOT causal comparison for NPT-009 as alternative | YES — T1+T3 cited for NPT-014 underperformance only |
| NPT-006 (Atomic Decomposition) | T1, EMNLP 2024 — compliance rate ONLY | MEDIUM for compliance construct; NOT hallucination rate | YES — cited with scope constraint in Testing section |
| NPT-008 (Contrastive Example Pairing) | T4 observational (E-007: PAT-CQRS-001, PAT-AGG-004, PAT-ENT-003, PAT-TEST-002 — direct pattern file observation of existing contrastive structure) | LOW | YES — identified as existing structure in CQRS, Aggregate, Entity sections; supported exclusively by E-007. Note: A-11 (arXiv 2024 — "Contrastive Prompting Improves Code Generation Quality") removed in I5: web search confirmed no matching paper exists; citation was likely hallucinated in Phase 1 research. E-007 provides independent, verifiable support. |

**Constraint propagation checklist (mandatory per taxonomy PS Integration):**
- [x] NPT-009 through NPT-011 cited with "UNTESTED causal comparison against positive equivalent"
- [x] NPT-012 cited with "UNTESTED vocabulary contribution vs. re-injection frequency"
- [x] NPT-013 cited with "schema-mandatory, predates effectiveness evidence"
- [x] NPT-006 T1 evidence scoped to "compliance rate only"
- [x] NPT-005 T1 evidence — applicable at Testing category level (MEDIUM, BDD process gate observation) but no pattern file recommendation uses NPT-005 (meta-prompt pattern; per-file recommendations use NPT-009). Category-level applicability and recommendation-level applicability are distinct; see Testing section NPT-005 reconciliation note for full explanation.

---

## Evidence Summary

| Evidence ID | Type | Source | Relevance to This Analysis |
|-------------|------|--------|---------------------------|
| E-001 | T1 controlled study | A-20 (AAAI 2026), A-15 (EMNLP 2024), A-31 (arXiv T3) | Establishes NPT-014 underperformance — justifies upgrading existing blunt constraint language |
| E-002 | T4 observational | VS-001–VS-004 (supplemental-vendor-evidence.md), 33 instances | Establishes NPT-009 pattern as production working practice in Anthropic's own rule files |
| E-003 | T4 observational | AGREE-8 (Moderate, 2-of-3 surveys), NP-002 | Cross-survey agreement that pairing with positive alternative is working practice |
| E-004 | T4 observational | AGREE-9 (Moderate, 2-of-3 surveys), NP-003 | Cross-survey agreement that justification improves negative instruction working practice |
| E-005 | T4 observational | I-28, I-32 (T-004 failure mode), GAP-13 | Context compaction risk for NEVER rules; applies to NPT-012 recommendations |
| E-006 | Pattern file observation | VS-001 NC-018, NC-019, NC-029, NC-030, NC-031 | Architecture boundary MUST NOT rules in .context/rules/ already use NPT-009 structure; pattern documentation lags behind |
| E-007 | Pattern file observation | PAT-CQRS-001, PAT-AGG-004, PAT-ENT-003, PAT-TEST-002 | Four sampled files with NPT-008 (contrastive) anti-patterns; zero files with NPT-009 structured prohibition |

> **I5 NOTE — A-11 REMOVED:** A-11 (formerly cited as arXiv 2024 — "Contrastive Prompting Improves Code Generation Quality") was removed from this Evidence Summary in I5. Web search confirmed no matching paper exists; citation was likely hallucinated in Phase 1 research. NPT-008 applicability is independently supported by E-007 (direct pattern file observation: PAT-CQRS-001, PAT-AGG-004, PAT-ENT-003, PAT-TEST-002). No recommendation in this document relied on A-11 as its sole evidence source. The evidence count for this analysis is 7 items (E-001 through E-007); A-11 is not counted.

---

## Self-Review Checklist

**H-15 (self-review before presenting):**

- [x] Conclusions cite evidence (all recommendations carry NPT reference + evidence tier + evidence source E-code)
- [x] No directional verdict on framing superiority — NEVER stated that negative framing outperforms positive framing
- [x] Constraint propagation compliance section present and complete
- [x] PG-003 contingency plan present with explicit reversibility assessment per category
- [x] Evidence gap map distinguishes T1, T4, and Untested
- [x] Analysis uses negative constraint framing in recommendations (per orchestration directive 1)
- [x] Supplemental vendor evidence report incorporated (E-002 from VS-001–VS-004; E-006 from NC-018/NC-019/NC-029 etc.)
- [x] Practitioner and vendor self-practice evidence not dismissed (E-002 through E-004 are T4 evidence treated as working practice)
- [x] Absence of published evidence NOT treated as evidence of absence (SE-1 through SE-5 defined in Methodology and applied throughout)
- [x] Enforcement tier vocabulary NOT presented as experimentally validated (T4 observational label on all NPT-009 through NPT-013 recommendations)
- [x] Phase 2 experimental conditions preserved (no vocabulary coupling to LLM-runtime mechanisms)
- [x] PG-003 contingency explicitly acknowledged in reversibility table
- [x] I2 revision: All 10 gaps from adversary-patterns-i1.md addressed (see list below)
- [x] I3 revision: All 5 targeted fixes from adversary-patterns-i2.md addressed (see list below)

**I2 revision gap closure verification:**

1. [x] Category count discrepancy resolved: L0 now consistently states "12 analyzed categories" with explicit resolution note
2. [x] A-11 defined in Evidence Summary table with full citation (I5 update: A-11 subsequently removed entirely in I5 revision — see I5 revision gap closure below; NPT-008 supported by E-007 independently)
3. [x] NPT-005 reconciled: Testing applicable NPTs table retains MEDIUM (category-level), compliance table explains recommendation-level non-use, reconciliation note added to Testing section
4. [x] Evidence source (E-code) column added to all recommendation tables
5. [x] Terminology Note moved to before L0 (new top section); Finding 2 uses plain-English task labels, not task-spec NPT labels
6. [x] Extrapolation confidence note added for PAT-SKILL-001 (LOW confidence, anti-patterns section title only)
7. [x] Implementation Sequencing table added grouping 34 recommendations into 3 Phase 5 priority groups (I4 correction: I2/I3 stated 28 incorrectly)
8. [x] Per-category confidence decomposition added to PS Integration block
9. [x] SE-1 through SE-5 inline-defined in Methodology section
10. [x] Priority column legend added to L0 recommendation summary and all priority references

**I3 revision gap closure verification:**

1. [x] Fix 1 (ADP-R1/R2 priority contradiction): Adapter category recommendation table updated — ADP-R1 and ADP-R2 Priority changed from "SHOULD add" to "MAY add (reclassified in implementation sequencing due to 80-line sample risk)". Category table now consistent with Group 3 sequencing. Group 3 footnote updated to remove stale "both are SHOULD add in their category tables" language.
2. [x] Fix 2 (L0 MAY add count): L0 recommendation summary updated — "MAY add = 8" corrected to "MAY add = 10"; "SHOULD add = 14" corrected to "SHOULD add = 18" with explanatory note. Group 3 intro corrected from "8 recommendations" to "10 recommendations".
3. [x] Fix 3 (Group 2 header count): Group 2 header updated from "14 recommendations" to "18 recommendations (14 category + 4 catalog/skill updates)" — matches Group 2 body and footnote.
4. [x] Fix 4 (A-11 arXiv ID): A-11 Evidence Summary entry updated with "[arXiv ID: pending verification]" note; same note added to CQRS applicable NPTs table and Constraint Propagation Compliance table where A-11 is cited. **I4 ESCALATION: pending verification upgraded to "likely hallucinated." I5 RESOLUTION: A-11 removed entirely — see I5 revision gap closure below.**
5. [x] Fix 5 (CAT-R3 blank-row count precision): CAT-R3 recommendation text updated to specify "4 confirmed categories" with explicit note that precise row count per category requires full-file verification — the 100-line sample showed at minimum 1 blank row per category section.

**I4 revision gap closure verification:**

1. [x] Fix 1 (Recommendation count 28 → 34): Count corrected in 7 locations: (a) document header I4 revision line — "34 recommendations"; (b) navigation table line 37 — "Phase 5 priority groups for the 34 recommendations"; (c) L0 summary — "Total recommendations: 34 across all 12 categories"; (d) Implementation Sequencing header — "34 recommendations grouped into Phase 5 priority groups" with full Rec-ID enumeration; (e) Phase 5 Downstream Inputs item 2 — "34 categorized recommendations"; (f) Self-Review Checklist I2 item 7 — "grouping 34 recommendations"; (g) Key Findings item 2 — "implement the 34 recommendations". Count verified by explicit Rec-ID enumeration: 5+4+3+3+2+2+2+2+2+1+1+4+3 = 34. Group 1 (6) + Group 2 (18) + Group 3 (10) = 34 confirmed. No recommendation content was changed.
2. [x] Fix 2 (A-11 citation escalation): Web search performed for "Contrastive Prompting Improves Code Generation Quality arXiv 2024" and variants. No matching paper found. Citation escalated from "[arXiv ID: pending verification]" to "[CITATION UNVERIFIABLE — LIKELY HALLUCINATED]" in 3 locations: (a) CQRS Applicable NPTs table; (b) Constraint Propagation Compliance table for NPT-008; (c) Evidence Summary A-11 entry. The A-11 entry explicitly documents that web search found no matching paper and classifies the citation as likely hallucinated. All NPT-008 recommendations remain supported by E-007 (direct pattern file observation) which is independent of A-11. No recommendation in this document cites A-11 as its sole evidence source. **I5 RESOLUTION: A-11 removed entirely from all 4 active citation locations — see I5 revision gap closure below.**

**I5 revision gap closure verification (FINAL):**

1. [x] Fix 1 ("6 locations" → "7 locations"): The I4 fix documentation stated "Count corrected in 6 locations" but enumerated sub-items (a) through (g) = 7 items. Corrected in 2 places: (a) I4 revision gap closure verification item 1 — now reads "7 locations"; (b) PS Integration Version field — updated from "6 locations" to "7 locations". Zero analytical impact; metadata accuracy restored.
2. [x] Fix 2 (A-11 complete removal): A-11 (formerly cited as arXiv 2024 — "Contrastive Prompting Improves Code Generation Quality") removed entirely from the document. Confirmed no matching paper exists (web search performed in I4). Removed from 4 locations: (a) CQRS Applicable NPTs table — now cites E-007 only; (b) Evidence Tier table (Constraint Propagation — first table) — row updated to cite E-007 (T4 observational); (c) Constraint Propagation Compliance table — NPT-008 row updated to cite E-007; (d) Evidence Summary table — A-11 row replaced with I5 removal note. Evidence count is now 7 items (E-001 through E-007). No NPT-008 recommendation loses support; E-007 provides independent, verifiable coverage.
3. [x] Fix 3 (Evidence chain clean): All NPT-008 references now cite E-007 exclusively. Constraint Propagation Compliance table updated with clean T4 evidence tier. No residual A-11 references remain in any active citation context. Thorough document scan performed — all references to "A-11" in body text are now historical references in revision documentation (items 4/fix-2) or removal notes, not active citations.
4. [x] Fix 4 (Methodology scope acknowledgment): Methodology section updated with explicit binding-constraint statement: the representative-sample approach (13 of 49 patterns across 12 categories) establishes a confidence ceiling of 0.84 composite, and this is the binding constraint on the analysis's methodological defensibility. Previously partially documented; now stated prominently in the Methodology section conclusion.

**Orchestration directive compliance (all 7):**

1. [x] Analysis uses negative constraint framing (NEVER/MUST NOT) throughout recommendations
2. [x] Supplemental vendor evidence incorporated (E-002, E-006 sections)
3. [x] Practitioner and vendor self-practice evidence treated as T4 working practice, not inferior
4. [x] Absence of published evidence explicitly framed via SE-1–SE-5 defined in methodology
5. [x] Enforcement tier vocabulary NOT presented as experimentally validated (explicit T4 label throughout)
6. [x] Phase 2 experimental conditions preserved — pattern file changes scoped to human-facing documentation, not LLM-runtime constraints
7. [x] PG-003 contingency present with per-category reversibility assessment

---

## PS Integration

| Field | Value |
|-------|-------|
| Project | PROJ-014-negative-prompting-research |
| Orchestration | neg-prompting-20260227-001 |
| Task ID | TASK-013 |
| Phase | Phase 4 |
| Artifact | `orchestration/neg-prompting-20260227-001/phase-4/patterns-update-analysis.md` |
| Analysis Type | gap (with root-cause sub-analysis per category) |
| Version | v5.0.0 (I5 revision FINAL — 4 targeted fixes from adversary-patterns-i4.md: (1) "6 locations" corrected to "7 locations" in I4 fix documentation and this Version field; (2) A-11 citation removed entirely from 4 active locations — web search confirmed no matching paper; NPT-008 now supported exclusively by E-007; (3) evidence chain cleaned — all NPT-008 references cite E-007 only; (4) methodology scope limitation strengthened in Methodology section. I4: recommendation count corrected from 28 to 34 in 7 locations; A-11 escalated to "likely hallucinated." I3: ADP-R1/R2 priority table corrected to MAY add; L0 counts corrected to SHOULD=18, MAY=10; Group 2 header corrected to 18; A-11 arXiv ID marked pending verification; CAT-R3 count precision noted) |
| Confidence (composite) | 0.84 — see per-category decomposition below |
| Next agent hint | ps-architect for ADR writing (Phase 5) |

### Per-category confidence decomposition

| Category | Files Sampled | Total Patterns | Coverage | Confidence | Basis |
|----------|--------------|----------------|----------|------------|-------|
| Architecture | 2 | 5 | 40% | MEDIUM-HIGH | Two structurally distinct files; core constraints directly observed |
| Testing | 2 | 3 | 67% | HIGH | Two major sub-types covered; findings consistent across files |
| CQRS | 1 | 4 | 25% | MEDIUM | Most representative file (PAT-CQRS-001); extrapolation for query/dispatcher |
| Aggregate | 1 | 4 | 25% | MEDIUM | Richest anti-pattern file; lifecycle patterns PAT-AGG-001–003 extrapolated |
| Entity | 1 | 5 | 20% | MEDIUM | Aggregate root covers primary constraint domain; protocol patterns extrapolated |
| Repository | 1 | 3 | 33% | MEDIUM-LOW | 80-line sample; anti-pattern section absence may be sampling artifact |
| Adapter | 1 | 2 | 50% | MEDIUM | CLI adapter representative; PAT-ADP-002 extrapolated |
| Domain Service | 1 | 2 | 50% | MEDIUM | 60-line sample; anti-pattern section absence may be sampling artifact |
| Event | 1 | 4 | 25% | MEDIUM-LOW | 60-line sample; three patterns extrapolated |
| Identity | 1 | 4 | 25% | MEDIUM-LOW | 60-line sample; programmatic enforcement reduces documentation gap risk |
| Value Object | 1 | 3 | 33% | MEDIUM-LOW | 60-line sample; frozen=True enforcement partially verifiable |
| Skill Development | 1 | 6 | 17% | **LOW** | Anti-pattern section title only (content not sampled); SKILL-R4 extrapolation low-confidence |

**Composite confidence 0.84** derives from: HIGH confidence for gap identification (direct file observation for 12 categories); MEDIUM for recommendation prioritization (representative sample; unsampled patterns require individual verification); MEDIUM for evidence-tier assignments (inherited from upstream taxonomy confidence, not independently re-verified). Skill Development category confidence is LOW for recommendation SKILL-R4 specifically; all other SKILL-R1/R2/R3 recommendations derive from Key Rules citations independently verifiable.

### Key findings for downstream agents

1. MUST NOT treat the Anti-Pattern Section Standard as validated — it is a T4 working-practice upgrade from NPT-014 structure to NPT-009 structure, justified by T1 evidence for NPT-014 underperformance.
2. MUST NOT implement the 34 recommendations without individual pattern file verification for unsampled patterns — representative sampling was used; category-level extrapolation may miss pattern-specific constraints.
3. MUST NOT couple vocabulary changes to LLM-runtime constraint generation — preserves Phase 2 experimental condition reproducibility.
4. The NPT-014 → NPT-009 upgrade is the highest-confidence, most widely applicable change: T1 evidence for NPT-014 underperformance justifies structural improvement even before Phase 2 framing comparison results are available.
5. The reversibility architecture is clean: all structural improvements (consequence documentation, scope specification, anti-pattern naming, positive alternatives, justifications) survive Phase 2 null result; only NEVER/MUST NOT vocabulary requires recalibration to convention-based language.
