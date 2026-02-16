# TASK-003: Tiered Enforcement Strategy Design

<!--
DOCUMENT-ID: FEAT-005:EN-404:TASK-003
TEMPLATE: Task
VERSION: 1.1.0
AGENT: ps-architect (Claude Opus 4.6)
DATE: 2026-02-13
PARENT: EN-404 (Rule-Based Enforcement Enhancement)
FEATURE: FEAT-005 (Quality Framework Enforcement Mechanisms)
EPIC: EPIC-002 (Quality Framework Enforcement)
PROJECT: PROJ-001-oss-release
QUALITY-TARGET: >= 0.92
ACTIVITY: DESIGN
REQUIREMENTS-COVERED: FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-007, FR-008, FR-009, FR-013
TARGET-ACS: 2, 3, 4, 5, 9, 10
-->

> **Type:** task
> **Status:** complete
> **Agent:** ps-architect
> **Activity:** DESIGN
> **Created:** 2026-02-13
> **Parent:** EN-404

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Design Overview](#design-overview) | Three-tier enforcement architecture summary |
| [HARD Tier Definition](#hard-tier-definition) | Absolute constraints that cannot be overridden |
| [MEDIUM Tier Definition](#medium-tier-definition) | Standards that should be followed with documented exceptions |
| [SOFT Tier Definition](#soft-tier-definition) | Guidance and best practices |
| [Tier Classification Criteria](#tier-classification-criteria) | How to classify a rule into a tier |
| [Decision Criticality Integration](#decision-criticality-integration) | C1-C4 levels mapped to enforcement tiers |
| [Quality Layer Mapping](#quality-layer-mapping) | Review layers L0-L4 mapped to tiers and strategies |
| [Adversarial Strategy Encoding Map](#adversarial-strategy-encoding-map) | How each strategy maps to enforcement tiers + SSOT designation (M-006) |
| [Task Complexity Thresholds](#task-complexity-thresholds) | When enforcement escalates |
| [Enforcement Escalation Model](#enforcement-escalation-model) | How enforcement tightens with artifact maturity |
| [Token Budget Allocation](#token-budget-allocation) | Per-tier and per-file token budgets |
| [L2 Re-Injection Priorities](#l2-re-injection-priorities) | Which HARD rules need V-024 reinforcement (authoritative V-024 source, B-004) |
| [File Consolidation Plan](#file-consolidation-plan) | How current 10+1 files become 8 optimized files |
| [Traceability](#traceability) | Requirements coverage |
| [References](#references) | Source documents |

---

## Design Overview

The tiered enforcement strategy implements three enforcement tiers with distinct vocabulary, formatting, consequences, and token allocation. The tiers operate within a decision criticality framework (C1-C4) that determines which tiers are mandatory for each task.

### Core Design Principles

1. **Enforcement vocabulary is absolute.** Each tier has exclusive vocabulary. No term appears in more than one tier. (REQ-404-010 through REQ-404-015)
2. **HARD rules are scarce.** Maximum 25 HARD directives across all rule files. Scarcity preserves signal strength. (REQ-404-017)
3. **Consequences are explicit.** Every HARD rule states what happens on violation. (REQ-404-016)
4. **Single source of truth.** Each rule exists in exactly one file. Cross-references replace duplication. (REQ-404-027, REQ-404-062)
5. **Context rot awareness.** HARD rules appear first in every file. (REQ-404-060)

> **Methodology note (m-005, v1.1.0):** Compliance rates and bypass-impact assessments referenced throughout this document are derived from qualitative review of Jerry framework development sessions (PROJ-001-oss-release, Jan-Feb 2026). Rates are approximate and based on observed agent behavior across ~30 sessions. Formal quantitative measurement methodology (session sampling, compliance definition, inter-rater reliability) is deferred to post-implementation validation (EN-404 TASK-005+). See TASK-004 Evidence Base for detailed per-file compliance observations.

### Tier Summary

| Tier | Vocabulary | Consequence | Max Count | Token Budget | Visual |
|------|-----------|-------------|-----------|-------------|--------|
| **HARD** | MUST, SHALL, NEVER, FORBIDDEN, REQUIRED, CRITICAL | "Violations will be blocked / Build will fail / Session will not proceed" | <= 25 | ~4,000 | **Bold + (HARD)** label |
| **MEDIUM** | SHOULD, RECOMMENDED, PREFERRED, EXPECTED | "Override requires documented justification in commit message or PR" | Unlimited | ~4,500 | Normal text |
| **SOFT** | MAY, CONSIDER, OPTIONAL, SUGGESTED | None -- advisory only | Unlimited | ~2,000 | *Italic or parenthetical* |

---

## HARD Tier Definition

### Properties

- **Vocabulary:** MUST, SHALL, NEVER, FORBIDDEN, REQUIRED, CRITICAL
- **Override:** Cannot be overridden. No exception, no waiver within the session.
- **Consequence:** Every HARD directive includes a specific consequence statement.
- **Visual Format:** Bold text with explicit **(HARD)** label in rule files.
- **L2 Reinforcement:** All HARD rules are candidates for V-024 re-injection.
- **Context Rot Priority:** HARD rules MUST appear in the first 25% of each file.

### HARD Rule Inventory

The following is the authoritative inventory of HARD directives for all L1 rule files. Maximum 25.

#### Constitutional HARD Rules (from CLAUDE.md and quality-enforcement.md)

| # | Rule | Source | Consequence |
|---|------|--------|-------------|
| H-01 | **P-003: No Recursive Subagents.** Max ONE level of delegation: orchestrator -> worker. | Jerry Constitution | Agent hierarchy violation will be flagged and work product rejected. |
| H-02 | **P-020: User Authority.** User decides. NEVER override user intent. Ask before destructive operations. | Jerry Constitution | Unauthorized destructive operation will be blocked. |
| H-03 | **P-022: No Deception.** NEVER deceive about actions, capabilities, or confidence levels. | Jerry Constitution | Deceptive output will be flagged for rework. |
| H-04 | **Active Project REQUIRED.** Claude MUST NOT proceed with work without active project context. | CLAUDE.md | Session will not proceed. |

#### Python Environment HARD Rules (from python-environment.md)

| # | Rule | Source | Consequence |
|---|------|--------|-------------|
| H-05 | **UV Only.** MUST use `uv run` for all Python execution. NEVER use `python`, `pip`, or `pip3` directly. | python-environment.md | Command will fail; environment corruption risk. |
| H-06 | **UV for dependencies.** MUST use `uv add` for dependency management. NEVER use `pip install`. | python-environment.md | Build will break. |

#### Architecture HARD Rules (from architecture-standards.md)

| # | Rule | Source | Consequence |
|---|------|--------|-------------|
| H-07 | **Domain layer isolation.** `src/domain/` MUST NOT import from `application/`, `infrastructure/`, or `interface/`. Stdlib and `shared_kernel/` only. | architecture-standards.md | Architecture test will fail. CI will block merge. |
| H-08 | **Application layer boundary.** `src/application/` MUST NOT import from `infrastructure/` or `interface/`. | architecture-standards.md | Architecture test will fail. |
| H-09 | **Composition root exclusivity.** Only `src/bootstrap.py` SHALL instantiate infrastructure adapters. | architecture-standards.md | Architecture test will fail. |
| H-10 | **One class per file.** Each Python file SHALL contain exactly ONE public class or protocol. | file-organization.md | AST check will fail. |

#### Coding HARD Rules (from coding-standards.md)

| # | Rule | Source | Consequence |
|---|------|--------|-------------|
| H-11 | **Type hints REQUIRED.** All public functions and methods MUST have type annotations. | coding-standards.md | mypy will fail. CI will block merge. |
| H-12 | **Docstrings REQUIRED.** All public functions, classes, and modules MUST have docstrings. | coding-standards.md | AST check will fail. |

#### Quality Enforcement HARD Rules (from quality-enforcement.md -- NEW)

| # | Rule | Source | Consequence |
|---|------|--------|-------------|
| H-13 | **Quality threshold.** All deliverables at C2+ criticality MUST score >= 0.92 against defined rubrics (S-014). | Barrier-1 ADV-to-ENF; FR-006 | Deliverable will not be accepted. |
| H-14 | **Creator-critic-revision cycle.** C2+ decisions MUST undergo minimum 3 iterations (create-critique-revise). | Barrier-1 ADV-to-ENF; FR-010 | Deliverable rejected without cycle evidence. |
| H-15 | **Self-review before presenting.** MUST review own output for completeness, accuracy, and quality before presenting (S-010). | Barrier-1 ADV-to-ENF; FR-005 | Output quality degradation. |
| H-16 | **Steelman before critique.** Before criticizing any proposal, MUST first present the strongest version of the argument (S-003). | Barrier-1 ADV-to-ENF; FR-004 | Critique rejected as unfair. |
| H-17 | **Quality scoring REQUIRED.** All deliverables for C2+ decisions MUST include explicit quality scores against rubrics (S-014). | Barrier-1 ADV-to-ENF; FR-006 | Deliverable incomplete without score. |
| H-18 | **Constitutional compliance.** All outputs MUST be evaluated against applicable `.context/rules/` principles before presentation (S-007). | Barrier-1 ADV-to-ENF; FR-003 | Non-compliant output will be reworked. |
| H-19 | **Governance escalation.** Any artifact touching `docs/governance/`, `.context/rules/`, or `.claude/rules/` is automatically C3+ criticality. This CANNOT be overridden. | Barrier-1 ADV-to-ENF; FR-011 | Under-reviewed governance changes will be blocked. |

#### Testing HARD Rules (from testing-standards.md)

| # | Rule | Source | Consequence |
|---|------|--------|-------------|
| H-20 | **Test before implement.** NEVER write implementation before the test fails (BDD Red phase). | testing-standards.md | Untested code will be flagged. |
| H-21 | **90% line coverage REQUIRED.** Test suite MUST maintain >= 90% line coverage. | testing-standards.md | CI will block merge. |

#### Skill Usage HARD Rules (from mandatory-skill-usage.md)

| # | Rule | Source | Consequence |
|---|------|--------|-------------|
| H-22 | **Proactive skill invocation.** MUST invoke /problem-solving for research/analysis tasks. MUST invoke /nasa-se for requirements/design tasks. MUST invoke /orchestration for multi-phase workflows. | mandatory-skill-usage.md | Work quality degradation; rework required. |

> **M-005 Design Decision (v1.1.0):** H-22 is intentionally kept as a single compound rule rather than split into H-22a/H-22b/H-22c. Rationale: (1) All three skill obligations share the same consequence, source file, and enforcement mechanism (keyword trigger detection). Splitting would consume 3 of the 25-rule budget for what is operationally a single "use skills proactively" directive. (2) The 24-rule inventory is already near the 25-rule cap (REQ-404-017); splitting would require removing another HARD rule to stay within budget. (3) The compound form mirrors the source file (`mandatory-skill-usage.md`) which presents all three as a unified behavioral requirement. If a future iteration needs finer-grained enforcement (e.g., different consequences per skill), H-22 can be split at that time.

#### Navigation HARD Rules (from markdown-navigation-standards.md)

| # | Rule | Source | Consequence |
|---|------|--------|-------------|
| H-23 | **Navigation table REQUIRED** (NAV-001). All Claude-consumed markdown files over 30 lines MUST include a navigation table. | markdown-navigation-standards.md | Document rejected for non-compliance. |
| H-24 | **Anchor links REQUIRED** (NAV-006). Navigation table section names MUST use anchor links. | markdown-navigation-standards.md | Document rejected for non-compliance. |

**Total HARD directives: 24 (within the 25 maximum)**

---

## MEDIUM Tier Definition

### Properties

- **Vocabulary:** SHOULD, RECOMMENDED, PREFERRED, EXPECTED
- **Override:** Can be overridden with documented justification (in commit message, PR description, or inline comment explaining why).
- **Consequence:** Override without justification triggers a warning in adversarial review.
- **Visual Format:** Normal text without tier label (absence of HARD/SOFT label implies MEDIUM).
- **L2 Reinforcement:** Not tagged for V-024 re-injection (token budget reserved for HARD rules).

### MEDIUM Rule Categories

| Category | Example Rules | Source File |
|----------|--------------|-------------|
| Naming conventions | Snake_case for modules, PascalCase for classes RECOMMENDED | coding-standards.md |
| Import ordering | Grouped imports (stdlib, third-party, local) RECOMMENDED | coding-standards.md |
| Google-style docstrings | Google-style format PREFERRED over other formats | coding-standards.md |
| AAA test pattern | Arrange-Act-Assert structure RECOMMENDED for all tests | testing-standards.md |
| Test naming | `test_{scenario}_when_{condition}_then_{expected}` RECOMMENDED | testing-standards.md |
| BDD cycle | Red/Green/Refactor cycle SHOULD be followed for new features | testing-standards.md |
| Port naming | `I{Verb}Handler` for primary ports, `I{Noun}` for secondary RECOMMENDED | architecture-standards.md |
| Adapter naming | `{Tech}{Entity}Adapter` format RECOMMENDED | architecture-standards.md |
| CQRS file naming | `{verb}_{noun}_command.py` format RECOMMENDED | architecture-standards.md |
| Error hierarchy | DomainError hierarchy SHOULD be used for all domain exceptions | error-handling-standards.md |
| Error context | Error messages SHOULD include entity type, ID, and suggested action | error-handling-standards.md |
| Counterargument (S-002) | Before finalizing decisions, SHOULD consider and document strongest counterargument | quality-enforcement.md |
| Failure modes (S-013) | Before proposing solutions, SHOULD identify at least 3 failure modes | quality-enforcement.md |
| Navigation placement | Table SHOULD appear after frontmatter, before content (NAV-002) | markdown-navigation-standards.md |
| Section coverage | All major sections SHOULD be listed in navigation table (NAV-004) | markdown-navigation-standards.md |

---

## SOFT Tier Definition

### Properties

- **Vocabulary:** MAY, CONSIDER, OPTIONAL, SUGGESTED
- **Override:** No justification needed. These are best-practice guidance.
- **Consequence:** None.
- **Visual Format:** *Italic text* or parenthetical notes.
- **L2 Reinforcement:** Not tagged.

### SOFT Rule Examples

| Example | Source |
|---------|--------|
| Property-based testing MAY be used for edge case coverage | testing-standards.md |
| Module `__init__.py` files MAY explicitly export public API | file-organization.md |
| Pre-commit hooks SUGGESTED for local development | tool-configuration.md |
| Snapshot optimization OPTIONAL for aggregates with many events | architecture-standards.md |

---

## Tier Classification Criteria

### Decision Tree for Classifying a Rule

```
Is violation of this rule...
  ├── Architecturally destructive (corrupts boundaries, breaks invariants)?
  │   └── YES → HARD
  ├── A security/safety concern (data loss, deception, unauthorized action)?
  │   └── YES → HARD
  ├── A constitutional principle violation (P-003, P-020, P-022)?
  │   └── YES → HARD
  ├── A quality gate requirement (0.92 threshold, creator-critic cycle)?
  │   └── YES → HARD
  ├── Detectable by automated tools (CI, AST, linters)?
  │   └── YES → At least MEDIUM (HARD if architecturally critical)
  ├── A widely accepted best practice with measurable benefit?
  │   └── YES → MEDIUM
  └── A style preference or optimization suggestion?
      └── YES → SOFT
```

### Classification Validation Checklist

Before assigning a tier, verify:

- [ ] **HARD rules:** Is there a deterministic way to detect violation? Is the consequence real?
- [ ] **MEDIUM rules:** Is there a reasonable scenario where override is justified?
- [ ] **SOFT rules:** Would enforcing this as MEDIUM create unnecessary friction?

---

## Decision Criticality Integration

Decision criticality levels (C1-C4) determine which enforcement tiers and adversarial strategies are mandatory for a given task.

### C1: Routine

| Attribute | Value |
|-----------|-------|
| **Criteria** | Reversible within 1 session; fewer than 3 files; no external dependencies |
| **Examples** | Bug fixes, typo corrections, single-file refactors, documentation updates |
| **Default Review Layer** | L0 (Self-Check) |
| **Mandatory Strategies** | S-010 (Self-Refine) |
| **Optional Strategies** | None |
| **Enforcement Tiers Active** | HARD only (MEDIUM and SOFT are advisory) |
| **Quality Threshold** | No formal score required; self-review sufficient |

### C2: Standard

| Attribute | Value |
|-----------|-------|
| **Criteria** | Reversible within 1 day; 3-10 files changed; no API changes |
| **Examples** | Feature implementation, test suite additions, multi-file refactors |
| **Default Review Layer** | L2 (Standard Critic) |
| **Mandatory Strategies** | S-010 (Self-Refine), S-003 (Steelman), S-007 (Constitutional AI), S-002 (Devil's Advocate), S-014 (LLM-as-Judge) |
| **Optional Strategies** | S-013 (Inversion) |
| **Enforcement Tiers Active** | HARD + MEDIUM |
| **Quality Threshold** | >= 0.92 with 3-iteration creator-critic-revision cycle |

### C3: Significant

| Attribute | Value |
|-----------|-------|
| **Criteria** | More than 1 day to reverse; more than 10 files; API or interface changes |
| **Examples** | Architecture changes, new bounded contexts, public API design |
| **Default Review Layer** | L3 (Deep Review) |
| **Mandatory Strategies** | All C2 strategies + S-004 (Pre-Mortem), S-012 (FMEA), S-013 (Inversion) |
| **Optional Strategies** | S-001 (Red Team), S-011 (CoVe) |
| **Enforcement Tiers Active** | HARD + MEDIUM + SOFT as guidance |
| **Quality Threshold** | >= 0.92 with 3-iteration cycle + additional iterations until threshold met |

### C4: Critical

| Attribute | Value |
|-----------|-------|
| **Criteria** | Irreversible; architecture changes; governance changes; public release |
| **Examples** | Constitution changes, OSS release, rule file changes, ADR ratification |
| **Default Review Layer** | L4 (Tournament) |
| **Mandatory Strategies** | All C3 strategies + S-001 (Red Team), S-011 (CoVe) |
| **Optional Strategies** | None -- all 10 strategies mandatory |
| **Enforcement Tiers Active** | All tiers enforced at maximum |
| **Quality Threshold** | >= 0.92 with minimum 3 iterations; escalation to user review |

### Mandatory Escalation Rules

| Condition | Auto-Escalation | Source |
|-----------|----------------|--------|
| Artifact touches `docs/governance/JERRY_CONSTITUTION.md` | Auto-C4 | FR-011 |
| Artifact touches `.context/rules/` | Auto-C3 minimum | FR-011 |
| Artifact touches `.claude/rules/` | Auto-C3 minimum | FR-011 (symlink to `.context/rules/`; checked for completeness) |
| Artifact touches `CLAUDE.md` | Auto-C3 minimum | Extension of FR-011 |
| Artifact is an ADR | Auto-C3 minimum | ADR-EPIC002-001 precedent |
| Artifact is for public release | Auto-C4 | Jerry Constitution |

> **M-007 note (v1.1.0):** `.claude/rules/` is a symlink to `.context/rules/` in the Jerry repo. Both paths are listed here to align with EN-403 TASK-003's `_check_governance_escalation()` which checks both canonical and symlink paths. The constitution (`JERRY_CONSTITUTION.md`) is elevated to C4 per EN-403 TASK-003 alignment.

---

## Quality Layer Mapping

This table maps quality review layers to the adversarial strategies, enforcement tiers, and decision criticality levels.

| Layer | Name | Strategies | Tiers Enforced | Min. Criticality | Score Contribution |
|-------|------|-----------|----------------|------------------|-------------------|
| L0 | Self-Check | S-010 | HARD only | C1 | Floor: ~0.60 to ~0.75 |
| L1 | Light Review | S-010 + S-003 + S-014 | HARD only | C1 (enhanced) | ~0.75 to ~0.85 |
| L2 | Standard Critic | S-007 + S-002 + S-014 | HARD + MEDIUM | C2 | ~0.85 to ~0.92+ |
| L3 | Deep Review | L2 + S-004 + S-012 + S-013 | HARD + MEDIUM | C3 | ~0.92 to ~0.96 |
| L4 | Tournament | L3 + S-001 + S-011 | All tiers | C4 | ~0.96+ |

---

## Adversarial Strategy Encoding Map

Each of the six strategies from the Barrier-1 ADV-to-ENF handoff is mapped to an enforcement tier, a rule file location, and a compact encoding.

| Strategy | Tier | Rule File | Compact Encoding | Token Cost |
|----------|------|-----------|-----------------|------------|
| **S-007 (Constitutional AI)** | HARD | quality-enforcement.md | "All outputs MUST be evaluated against applicable `.context/rules/` principles before presentation." | ~25 |
| **S-003 (Steelman)** | HARD | quality-enforcement.md | "Before criticizing any proposal, MUST first present the strongest version of the argument." | ~20 |
| **S-010 (Self-Refine)** | HARD | quality-enforcement.md | "MUST review own output for completeness, accuracy, and quality before presenting." | ~18 |
| **S-014 (LLM-as-Judge)** | HARD | quality-enforcement.md | "All C2+ deliverables MUST include quality score against rubrics. Target: >= 0.92." | ~20 |
| **S-002 (Devil's Advocate)** | MEDIUM | quality-enforcement.md | "Before finalizing decisions, SHOULD consider and document the strongest counterargument." | ~18 |
| **S-013 (Inversion)** | MEDIUM | quality-enforcement.md | "Before proposing solutions, SHOULD identify at least 3 ways it could fail." | ~18 |
| **Total** | | | | **~119** |

### Why All Strategies Go in quality-enforcement.md

Per REQ-404-027 (no duplicate strategy encodings), all six strategies are encoded in the single authoritative file `quality-enforcement.md` rather than distributed across multiple files. This avoids:

1. **Duplication risk:** Strategy language appearing in multiple files with subtle differences
2. **Token waste:** Encoding the same strategy twice doubles cost
3. **Update fragility:** Changing a strategy requires updating multiple files

Other rule files reference `quality-enforcement.md` for quality framework definitions rather than restating them.

### Shared Enforcement Data Model (M-006 Resolution)

> **`quality-enforcement.md` is the SSOT (Single Source of Truth)** for all enforcement constants shared between EN-403 (Hook-Based) and EN-404 (Rule-Based). Both enablers MUST reference this file rather than defining enforcement concepts independently. See FM-CROSS-03 (RPN 210) mitigation.

The following concepts are authoritative in `quality-enforcement.md` only:

| Concept | Authoritative Definition | EN-403 Reference Approach |
|---------|-------------------------|---------------------------|
| Decision Criticality Levels (C1-C4) | quality-enforcement.md Decision Criticality section | EN-403 TASK-004 SessionStart generates context from quality-enforcement.md; EN-403 TASK-002 keyword mapping references the SSOT levels |
| Quality Gate Threshold (>= 0.92) | quality-enforcement.md H-13 | EN-403 content blocks reference the SSOT value |
| Adversarial Strategy Encodings (S-001 through S-014) | quality-enforcement.md Strategy Encoding table | EN-403 TASK-002 L2 content blocks are derived from SSOT encodings |
| Creator-Critic-Revision Cycle (3 iterations) | quality-enforcement.md H-14 | EN-403 content blocks reference the SSOT cycle count |
| HARD Rule Vocabulary (MUST/SHALL/NEVER/FORBIDDEN/REQUIRED/CRITICAL) | quality-enforcement.md Tier Definitions (this document, authoritative at design time) | Not directly referenced by EN-403 hooks |

Any change to these values MUST be made in `quality-enforcement.md` first, then propagated to any EN-403 hardcoded fallback content.

---

## Task Complexity Thresholds

### Automatic Criticality Classification

| Indicator | Classification | Rationale |
|-----------|---------------|-----------|
| Single file change, < 50 lines | C1 (Routine) | Trivially reversible |
| 2-3 files, < 200 lines total | C1 (Routine) | Still easily reversible |
| 3-10 files changed | C2 (Standard) | Cross-file coordination required |
| New test file required | C2 (Standard) | Quality infrastructure change |
| API or interface change | C3 (Significant) | External impact possible |
| > 10 files changed | C3 (Significant) | Broad system impact |
| Architecture boundary crossing | C3 (Significant) | Structural integrity at risk |
| Governance/constitution/rules change | C3+ (auto-escalated) | Mandatory escalation per FR-011 |
| Public release artifact | C4 (Critical) | Irreversible external commitment |
| New bounded context | C4 (Critical) | Fundamental architecture decision |

### Escalation-Only Principle

Criticality can only escalate during a task, never decrease. If a C1 task reveals it touches an API, it becomes C2+ immediately. The agent MUST NOT reclassify downward.

---

## Enforcement Escalation Model

Enforcement tightens as an artifact progresses through its lifecycle:

| Artifact Stage | Active Tiers | Active Strategies | Quality Gate |
|---------------|-------------|-------------------|-------------|
| **Draft** (first pass) | HARD only | S-010 (Self-Refine) | No formal score |
| **Review-ready** (submitted for critique) | HARD + MEDIUM | S-010, S-003, S-014 | Score >= 0.80 |
| **Post-critique** (after adversarial review) | All tiers | Full strategy set per criticality | Score >= 0.92 |
| **Final** (ready for merge/commit) | All tiers enforced | All mandatory strategies verified | Score >= 0.92 + evidence |

---

## Token Budget Allocation

### Per-File Token Budget

| File | Target Tokens | HARD Budget | MEDIUM Budget | SOFT Budget | New Content |
|------|-------------|-------------|---------------|-------------|-------------|
| CLAUDE.md | 2,000 | 600 (H-01 to H-06) | 200 | 0 | Navigation table |
| quality-enforcement.md (NEW) | 1,276 | 500 (H-13 to H-19) | 400 (S-002, S-013) | 100 | All new |
| architecture-standards.md | 1,800 | 300 (H-07 to H-09) | 800 | 200 | Tiers |
| coding-standards.md | 1,500 | 200 (H-11, H-12) | 700 | 200 | Tiers |
| testing-standards.md | 1,200 | 200 (H-20, H-21) | 600 | 200 | Tiers |
| mandatory-skill-usage.md | 1,200 | 200 (H-22) | 600 | 100 | Strategy triggers |
| python-environment.md | 600 | 400 (H-05, H-06) | 100 | 0 | Trim non-enforcement |
| markdown-navigation-standards.md | 800 | 200 (H-23, H-24) | 300 | 100 | Trim prose |
| project-workflow.md | 800 | 100 (H-04 ref) | 400 | 100 | C1-C4 ref |
| error-handling + file-org (consolidated into coding/arch) | 0 | 0 | 0 | 0 | Merged |
| tool-configuration (consolidated into testing) | 0 | 0 | 0 | 0 | Merged |
| **Total** | **~11,176** | **~2,700** | **~4,100** | **~1,000** | |

**Buffer:** 12,476 - 11,176 = 1,300 tokens available for adjustment during implementation.

### File Consolidation Impact

Current: 10 rule files + CLAUDE.md = ~30,160 tokens
Target: 7 rule files + 1 new + CLAUDE.md = ~13,176 tokens (including 1,300 buffer)
Reduction: 56.3%

---

## L2 Re-Injection Priorities

> **Authoritative V-024 Content Source (B-004 resolution).** The L2-REINJECT tag extraction strategy defined in this section and in TASK-004 is the **single authoritative** sourcing mechanism for V-024 re-injection content. EN-403 TASK-002's `PromptReinforcementEngine` SHALL extract content from `<!-- L2-REINJECT: ... -->` tags in `.context/rules/` files rather than maintaining hardcoded `ContentBlock` objects. Hardcoded content blocks in EN-403 serve as a **fallback only** if tag extraction fails (per fail-open design REQ-403-070). See also: FM-CROSS-01 (RPN 224) mitigation.

Content prioritized for V-024 re-injection (600 token budget per prompt submission, per REQ-403-015 v1.1.0), ranked by bypass impact if forgotten:

| Priority | Content | Source | Tokens | Rationale |
|----------|---------|--------|--------|-----------|
| 1 | Constitutional constraints (P-003, P-020, P-022) with consequences | CLAUDE.md H-01 to H-03 | ~80 | Foundational; highest bypass impact |
| 2 | Quality gate: >= 0.92 threshold + 3-iteration cycle for C2+ | quality-enforcement.md H-13, H-14 | ~90 | Central quality requirement |
| 3 | UV-only Python environment | python-environment.md H-05, H-06 | ~50 | Frequently violated |
| 4 | Domain layer isolation (no infra imports) | architecture-standards.md H-07 | ~60 | Core architecture invariant |
| 5 | Self-review before presenting (S-010) | quality-enforcement.md H-15 | ~30 | Universal quality baseline |
| 6 | Decision criticality: C1-C4 compact reference | quality-enforcement.md | ~100 | Prevents under-enforcement |
| 7 | One-class-per-file + type hints + docstrings required | coding-standards.md H-10, H-11, H-12 | ~60 | Frequently violated structural rules |
| 8 | Governance auto-escalation to C3+ | quality-enforcement.md H-19 | ~40 | Prevents governance bypass |
| **Total** | | | **~510** | Within 600-token budget |

### Re-Injection Tag Format (Authoritative)

> This format is the **single source of truth** for V-024 content encoding. EN-403's `PromptReinforcementEngine` SHALL parse these tags using the extraction algorithm defined in TASK-004 (Tag Extraction Algorithm section).

```markdown
<!-- L2-REINJECT: rank=1, tokens=80, content="P-003: No recursive subagents. P-020: User authority. P-022: No deception. Violations blocked." -->
```

Tags are HTML comments (zero visual impact) with machine-readable attributes for V-024 extraction. The `content` attribute contains the ultra-compact enforcement text injected into `additionalContext` by the UserPromptSubmit hook.

---

## File Consolidation Plan

### Files to Consolidate

| Current File | Action | Merge Into | Rationale |
|-------------|--------|-----------|-----------|
| error-handling-standards.md | MERGE | coding-standards.md | Error handling rules are coding standards; extract the 3-4 actual HARD/MEDIUM rules (~100 tokens) |
| file-organization.md | MERGE | architecture-standards.md | File organization is architecture; extract one-class-per-file rule + naming table (~200 tokens) |
| tool-configuration.md | MERGE | testing-standards.md | Tool config rules are testing infrastructure; extract 3-4 actual rules (~80 tokens) |

### Files to Create

| New File | Content | Token Budget |
|----------|---------|-------------|
| quality-enforcement.md | Enforcement tier definitions, quality gate thresholds, decision criticality levels, adversarial strategy encodings, L2 re-injection tags | 1,276 |

### Post-Consolidation File List

| # | File | Purpose | Est. Tokens |
|---|------|---------|-------------|
| 1 | CLAUDE.md | Root context, constitutional HARD rules, navigation | ~2,000 |
| 2 | quality-enforcement.md (NEW) | Enforcement framework, quality gates, criticality, strategies | ~1,276 |
| 3 | architecture-standards.md | Architecture HARD rules + MEDIUM conventions + file org rules | ~1,800 |
| 4 | coding-standards.md | Coding HARD rules + MEDIUM conventions + error handling rules | ~1,500 |
| 5 | testing-standards.md | Testing HARD rules + MEDIUM conventions + tool config rules | ~1,200 |
| 6 | mandatory-skill-usage.md | Skill invocation HARD rules + strategy triggers | ~1,200 |
| 7 | python-environment.md | UV-only HARD rules | ~600 |
| 8 | markdown-navigation-standards.md | Navigation HARD rules + MEDIUM conventions | ~800 |
| 9 | project-workflow.md | Workflow MEDIUM rules + C1-C4 reference | ~800 |
| | **Total** | | **~11,176** |

---

## Traceability

### Requirements Covered

| Requirement | Coverage |
|-------------|----------|
| FR-001 (Consistent enforcement tiers) | Tier definitions with exclusive vocabulary |
| FR-002 (Token budget) | Per-file allocations sum to 11,176 (under 12,476 target) |
| FR-003 (S-007 Constitutional AI) | H-18: HARD encoding in quality-enforcement.md |
| FR-004 (S-003 Steelman) | H-16: HARD encoding in quality-enforcement.md |
| FR-005 (S-010 Self-Refine) | H-15: HARD encoding in quality-enforcement.md |
| FR-006 (S-014 LLM-as-Judge) | H-13, H-17: HARD encoding in quality-enforcement.md |
| FR-007 (S-002 Devil's Advocate) | MEDIUM encoding in quality-enforcement.md |
| FR-008 (S-013 Inversion) | MEDIUM encoding in quality-enforcement.md |
| FR-009 (C1-C4 criticality) | Full criticality level definitions with strategy mapping |
| FR-013 (quality-enforcement.md creation) | File specified with 1,276 token budget |

### Acceptance Criteria Covered

| AC | Coverage |
|----|----------|
| AC-2 (Tiered enforcement + C1-C4) | Decision Criticality Integration section |
| AC-3 (HARD/MEDIUM/SOFT patterns) | Tier definitions with vocabulary, consequences, visual format |
| AC-4 (Adversarial strategy directives) | Adversarial Strategy Encoding Map section |
| AC-5 (Quality gate checkpoints) | Quality Layer Mapping + Decision Criticality sections |
| AC-9 (L2 re-injection tags) | L2 Re-Injection Priorities section |
| AC-10 (S-007 Constitutional AI) | H-18 in HARD Rule Inventory |

---

## References

| # | Document | Location | Content Used |
|---|----------|----------|--------------|
| 1 | ADR-EPIC002-002 (ACCEPTED) | `EN-402-enforcement-priority-analysis/TASK-005-enforcement-ADR.md` | 5-layer architecture, V-026, token budget, enforcement tier language |
| 2 | Barrier-1 ADV-to-ENF Handoff | `orchestration/epic002-crosspoll-20260213-001/cross-pollination/barrier-1/adv-to-enf/barrier-1-adv-to-enf-handoff.md` | Strategy encodings, quality gate integration, decision criticality escalation |
| 3 | EN-404 Enabler | `EN-404-rule-based-enforcement/EN-404-rule-based-enforcement.md` | FR/NFR requirements, task enrichment notes |
| 4 | TASK-001 Requirements | `EN-404-rule-based-enforcement/TASK-001-rule-requirements.md` | REQ-404-001 through REQ-404-064 |
| 5 | TASK-002 Rule Audit | `EN-404-rule-based-enforcement/TASK-002-rule-audit.md` | Per-file token counts, enforcement gaps, bypass vectors, optimization recommendations |

---

*Agent: ps-architect (Claude Opus 4.6)*
*Date: 2026-02-13*
*Parent: EN-404 Rule-Based Enforcement Enhancement*
*Quality Target: >= 0.92*
*HARD Rules: 24 (of 25 maximum)*
*MEDIUM Categories: 15*
*Files: 10 current -> 8 optimized (7 + 1 new)*
*Token Budget: ~11,176 allocated of 12,476 target (1,300 buffer)*
