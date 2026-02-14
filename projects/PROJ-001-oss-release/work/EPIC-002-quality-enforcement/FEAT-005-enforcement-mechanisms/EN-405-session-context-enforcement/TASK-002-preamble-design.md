# TASK-002: Quality Framework Preamble Design

<!--
DOCUMENT-ID: FEAT-005:EN-405:TASK-002
TEMPLATE: Architecture Design
VERSION: 1.0.0
AGENT: ps-architect-405 (Claude Opus 4.6)
DATE: 2026-02-14
PARENT: EN-405 (Session Context Enforcement Injection)
FEATURE: FEAT-005 (Quality Framework Enforcement Mechanisms)
EPIC: EPIC-002 (Quality Framework Enforcement)
PROJECT: PROJ-001-oss-release
QUALITY-TARGET: >= 0.92
REQUIREMENTS-COVERED: FR-405-001 through FR-405-022, SR-405-001 through SR-405-005
-->

> **Version:** 1.0.0
> **Agent:** ps-architect-405 (Claude Opus 4.6)
> **Status:** COMPLETE
> **Created:** 2026-02-14
> **Primary Reference:** EN-403 TASK-004 (SessionStart Design)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Design Intent](#design-intent) | Why this preamble exists and what it achieves |
| [Content Structure](#content-structure) | The 4 XML sections and their roles |
| [Section 1: Quality Gate](#section-1-quality-gate) | Quality threshold, scoring, cycle requirements |
| [Section 2: Constitutional Principles](#section-2-constitutional-principles) | HARD constraints and environment rules |
| [Section 3: Adversarial Strategies](#section-3-adversarial-strategies) | All 10 strategies with concise descriptions |
| [Section 4: Decision Criticality](#section-4-decision-criticality) | C1-C4 framework with auto-escalation |
| [Token Budget Analysis](#token-budget-analysis) | Per-section token estimates and total |
| [Per-Criticality Strategy Activation Sets](#per-criticality-strategy-activation-sets) | Strategy sets from barrier-2 per C1-C4 |
| [L1-L2 Coordination Design](#l1-l2-coordination-design) | How SessionStart and UserPromptSubmit interact |
| [Content Design Principles](#content-design-principles) | Rationale for language and formatting choices |
| [Traceability](#traceability) | Requirements coverage |
| [References](#references) | Source documents |

---

## Design Intent

The quality framework preamble is a structured XML block injected into Claude's context window at session start. Its purpose is to establish the enforcement baseline -- the quality gate threshold, constitutional principles, available adversarial strategies, and decision criticality framework -- before any work begins.

**Why session start is the right injection point:**
- The context window is clean; attention is maximal
- One-time comprehensive context is affordable (vs. per-prompt budget constraint)
- Priming at session start shapes all subsequent behavior
- L2 (UserPromptSubmit) subsequently reinforces the most critical elements on every prompt

**What the preamble does NOT do:**
- It does NOT select strategies at runtime (that is the decision tree's job)
- It does NOT enforce compliance (that is L2/L3/L5/Process enforcement)
- It does NOT replace `.claude/rules/` files (it complements them with quality framework context)

---

## Content Structure

The preamble is wrapped in a top-level XML tag and contains exactly 4 subsections:

```xml
<quality-framework version="1.0">
  <quality-gate>        <!-- Section 1: Scoring threshold + cycle + leniency bias -->
  </quality-gate>

  <constitutional-principles>  <!-- Section 2: HARD constraints (P-003, P-020, P-022, UV) -->
  </constitutional-principles>

  <adversarial-strategies>     <!-- Section 3: All 10 strategies with descriptions -->
  </adversarial-strategies>

  <decision-criticality>       <!-- Section 4: C1-C4 + auto-escalation rules -->
  </decision-criticality>
</quality-framework>
```

**Why 4 sections:**
1. Maps to the 4 enforcement dimensions: quality targets, behavioral constraints, review tools, and complexity classification
2. Each section is independently parseable by Claude (REQ-403-094)
3. Maps to the EN-403 TASK-004 design specification exactly
4. Enables section-level trimming if token budget tightens (PR-405-004)

---

## Section 1: Quality Gate

### Content Specification

```xml
<quality-gate>
  Target: >= 0.92 for all deliverables.
  Scoring: Use S-014 (LLM-as-Judge) with dimension-level rubrics.
  Known bias: S-014 has leniency bias. Score critically -- 0.92 means genuinely excellent.
  Cycle: Creator -> Critic -> Revision (minimum 3 iterations). Do not bypass.
  Pairing: Steelman (S-003) before Devil's Advocate (S-002) -- canonical review protocol.
</quality-gate>
```

### Design Rationale

| Element | Why Included | Source |
|---------|-------------|--------|
| >= 0.92 threshold | Central quality requirement; HARD rule H-13 | SRC-004 (H-13) |
| S-014 as scoring mechanism | Scoring backbone spanning all C1-C4 | SRC-003 (S-014 as Scoring Backbone) |
| Leniency bias note | R-014-FN known risk; calibration critical | SRC-003 (Quality Gate and Scoring) |
| Creator-Critic-Revision | HARD rule H-14; minimum 3 iterations | SRC-004 (H-14) |
| SYN #1 pairing (S-003 before S-002) | "Canonical Jerry review protocol" per barrier-2 | SRC-003 (Strategy Pairings, SYN #1) |

### Token Estimate: ~90 tokens

---

## Section 2: Constitutional Principles

### Content Specification

```xml
<constitutional-principles>
  HARD constraints (cannot be overridden):
  - P-003: No recursive subagents. Max ONE level: orchestrator -> worker.
  - P-020: User authority. User decides. Never override. Ask before destructive ops.
  - P-022: No deception. Never deceive about actions, capabilities, or confidence.
  Python: UV only. Never use python/pip directly. Use 'uv run'.
</constitutional-principles>
```

### Design Rationale

| Element | Why Included | Source |
|---------|-------------|--------|
| P-003 | HARD rule H-01; ~95% compliance in current form | SRC-004 (H-01); SRC-005 (Evidence Base) |
| P-020 | HARD rule H-02; foundational user authority | SRC-004 (H-02) |
| P-022 | HARD rule H-03; no deception principle | SRC-004 (H-03) |
| UV-only Python | HARD rules H-05/H-06; ~95% compliance | SRC-004 (H-05, H-06); SRC-005 (Evidence Base) |

**Selection criteria:** Only principles with "HARD" enforcement level and highest bypass-impact scores are included. These 4 items represent the non-negotiable behavioral baseline.

### Token Estimate: ~65 tokens

---

## Section 3: Adversarial Strategies

### Content Specification

```xml
<adversarial-strategies>
  Available strategies for quality enforcement:
  - S-014 (LLM-as-Judge): Rubric-based scoring. Use for all deliverables.
  - S-007 (Constitutional AI): Principle-by-principle review. Check .claude/rules/.
  - S-010 (Self-Refine): Self-review before presenting outputs. Apply always.
  - S-003 (Steelman): Charitable reconstruction before critique.
  - S-002 (Devil's Advocate): Strongest counterargument to prevailing conclusion.
  - S-013 (Inversion): Ask 'how could this fail?' before proposing.
  - S-004 (Pre-Mortem): 'Imagine it failed -- why?' for planning tasks.
  - S-012 (FMEA): Systematic failure mode enumeration for architecture.
  - S-011 (CoVe): Factual verification for claims and documentation.
  - S-001 (Red Team): Adversary simulation for security-sensitive work.
</adversarial-strategies>
```

### Strategy Ordering Rationale

The strategies are ordered by their role prominence in the quality framework, not by strategy ID:

| Order | Strategy | Rationale for Position |
|-------|----------|----------------------|
| 1 | S-014 (LLM-as-Judge) | Scoring backbone; spans C1-C4; Ultra-Low cost (2,000 tokens) |
| 2 | S-007 (Constitutional AI) | HARD rule H-18; foundational compliance check |
| 3 | S-010 (Self-Refine) | HARD rule H-15; universal baseline; most resilient under ENF-MIN |
| 4 | S-003 (Steelman) | HARD rule H-16; part of canonical SYN #1 pair |
| 5 | S-002 (Devil's Advocate) | MEDIUM encoding; required at C2+; SYN #1 pair complement |
| 6 | S-013 (Inversion) | MEDIUM encoding; ultra-low cost; feasible under ENF-MIN |
| 7 | S-004 (Pre-Mortem) | C3+ required; Process delivery; infeasible under ENF-MIN |
| 8 | S-012 (FMEA) | C3+ required; Process/L5 delivery; infeasible under ENF-MIN |
| 9 | S-011 (CoVe) | C3 recommended, C4 required; verification backbone |
| 10 | S-001 (Red Team) | C3+ optional, C4 required; most expensive (7,000 tokens) |

### Token Estimate: ~120 tokens

---

## Section 4: Decision Criticality

### Content Specification

```xml
<decision-criticality>
  Assess every task's criticality:
  - C1 (Routine): Reversible, < 3 files, no external deps -> Self-Check only
  - C2 (Standard): Reversible within 1 day, 3-10 files -> Standard Critic
  - C3 (Significant): > 1 day to reverse, > 10 files, API changes -> Deep Review
  - C4 (Critical): Irreversible, architecture/governance changes -> Tournament Review
  AUTO-ESCALATE: Any change to docs/governance/, .context/rules/, or .claude/rules/ is C3 or higher.
</decision-criticality>
```

### Per-Criticality Strategy Mapping (Reference)

This mapping is NOT injected into the preamble (too many tokens), but the preamble primes Claude with the C1-C4 framework that drives this mapping:

| Level | Required Strategies | Token Budget | Quality Threshold |
|-------|--------------------|-------------|-------------------|
| C1 | S-010 | 2,000 | Self-review (no formal score) |
| C2 | S-007, S-002, S-014 (+ recommended S-003, S-010) | 14,600-18,200 | >= 0.92 |
| C3 | S-007, S-002, S-014, S-004, S-012, S-013 (+ recommended S-003, S-010, S-011) | 31,300-38,900 | >= 0.92 |
| C4 | All 10 strategies | ~50,300 | >= 0.92 (target >= 0.96) |

### Auto-Escalation Rules in Context

The preamble includes the consolidated auto-escalation rule. The full rule set from Barrier-2 (AE-001 through AE-006) is:

| Rule | Condition | Effect |
|------|-----------|--------|
| AE-001 | Artifact modifies `docs/governance/JERRY_CONSTITUTION.md` | Escalate to C3 minimum |
| AE-002 | Artifact modifies `.claude/rules/` | Escalate to C3 minimum |
| AE-003 | Artifact is a new or modified ADR | Escalate to C3 minimum |
| AE-004 | Artifact modifies existing baselined ADR | Escalate to C4 |
| AE-005 | Artifact modifies security-relevant code | Escalate to C3 minimum |
| AE-006 | Token budget EXHAUST and criticality C3+ | Add mandatory human escalation flag |

The preamble consolidates AE-001/AE-002 into the single `AUTO-ESCALATE` line. AE-003 through AE-006 are reference-level detail available in the decision tree (EN-303 TASK-004) and quality-enforcement.md (when created).

### Token Estimate: ~85 tokens

---

## Token Budget Analysis

### Per-Section Budget

| Section | Content | Estimated Tokens |
|---------|---------|-----------------|
| `<quality-gate>` | Threshold + scoring + bias + cycle + SYN #1 pairing | ~90 |
| `<constitutional-principles>` | P-003 + P-020 + P-022 + UV-only | ~65 |
| `<adversarial-strategies>` | 10 strategies with one-line descriptions | ~120 |
| `<decision-criticality>` | C1-C4 definitions + auto-escalation | ~85 |
| XML wrapper (`<quality-framework>` + version) | Opening/closing tags | ~10 |
| **Total** | | **~370 tokens** |

### Budget Comparison

| Component | Tokens | % of L1 Budget (12,476) |
|-----------|--------|------------------------|
| Quality context (this preamble) | ~370 | 3.0% |
| Existing project context | ~150 | 1.2% |
| Pre-commit warning (when present) | ~80 | 0.6% |
| **Total SessionStart contribution** | **~520-600** | **4.2-4.8%** |
| Remaining for .claude/rules/ files | ~11,876-11,956 | ~95.2-95.8% |

The ~370 token estimate is within the ~360 token target from EN-403 TASK-004. The 10-token variance is due to the addition of the SYN #1 pairing line (~15 tokens) partially offset by minor wording compression.

### Degradation Priority (PR-405-004)

If budget requires trimming:

| Priority | Action | Tokens Saved | Remaining |
|----------|--------|-------------|-----------|
| 1 | Remove full strategy list | ~120 | ~250 |
| 2 | Condense criticality to single line | ~65 | ~185 |
| 3 | Minimum viable: quality-gate + constitutional only | ~185 | ~155 |

---

## Per-Criticality Strategy Activation Sets

This section documents the strategy activation sets from the Barrier-2 handoff. These sets inform the `<decision-criticality>` and `<adversarial-strategies>` preamble sections.

### C1: Routine

| Category | Strategies |
|----------|-----------|
| Required | S-010 (Self-Refine) |
| Optional | S-003 (Steelman), S-014 (LLM-as-Judge) |
| Quality Target | ~0.60 to ~0.80 |

### C2: Significant (Target Operating Layer)

| Category | Strategies |
|----------|-----------|
| Required | S-007 (Constitutional AI), S-002 (Devil's Advocate), S-014 (LLM-as-Judge) |
| Recommended | S-003 (Steelman), S-010 (Self-Refine) |
| Quality Target | ~0.80 to ~0.92+ |
| Phase Modifier | PH-EXPLORE downgrades to C1 (unless auto-escalated via PR-001) |
| Team Modifier | TEAM-SINGLE replaces S-002 with S-010 (self-DA is weak) |

### C3: Major (Deep Review)

| Category | Strategies |
|----------|-----------|
| Required | S-007, S-002, S-014, S-004 (Pre-Mortem), S-012 (FMEA), S-013 (Inversion) |
| Recommended | S-003, S-010, S-011 (CoVe) |
| Quality Target | ~0.92 to ~0.96 |
| Note | TEAM-SINGLE not recommended; escalate to TEAM-MULTI or TEAM-HIL |

### C4: Critical (Tournament)

| Category | Strategies |
|----------|-----------|
| Required | ALL 10 strategies |
| Quality Target | ~0.96+ |
| Note | TEAM-SINGLE not permitted. TEAM-HIL required. Human involvement mandatory. |

### Creator-Critic-Revision Cycle Strategy Assignments

| Iteration | Role | C1 | C2 | C3 | C4 |
|-----------|------|----|----|----|----|
| 1: Create | Creator + self-review | S-010 | S-010 | S-010 | S-010 |
| 2: Critique | Adversarial review | S-014 | S-003 + S-002 + S-007 + S-014 | S-003 + S-002 + S-007 + S-004 + S-012 + S-013 + S-014 | All 10 |
| 3: Revise | Revision + scoring | S-010 + S-014 | S-010 + S-014 | S-010 + S-014 + S-011 | S-010 + S-014 + S-011 |

---

## L1-L2 Coordination Design

### How SessionStart (L1) and UserPromptSubmit (L2) Work Together

| Aspect | SessionStart (L1) | UserPromptSubmit (L2) |
|--------|-------------------|----------------------|
| Fires | Once per session | Every prompt |
| Token budget | ~370 tokens (one-time) | ~600 tokens (per-prompt, amortized) |
| Content depth | Comprehensive (full strategy list, detailed criteria) | Ultra-compact (key reminders only) |
| Context rot | VULNERABLE (degrades over session) | IMMUNE (re-injected every prompt) |
| Purpose | Establish baseline understanding | Sustain critical rules |

### Content Overlap (Intentional)

Some content appears in BOTH SessionStart and UserPromptSubmit:
- **0.92 quality threshold:** SessionStart explains context; L2 reinforces the number
- **Constitutional principles (P-003, P-020, P-022):** SessionStart lists; L2 reminds
- **Self-review (S-010):** SessionStart lists as available; L2 reminds to apply

This overlap is the defense-in-depth design. L1 content degrades; L2 keeps critical elements alive.

### Content Non-Overlap

**SessionStart only (too large for L2 budget):**
- Full 10-strategy listing with descriptions (~120 tokens)
- C1-C4 framework with detailed criteria (~85 tokens)
- SYN #1 pairing guidance
- Scoring methodology (S-014 rubric reference)

**UserPromptSubmit only (relevant when active):**
- Leniency bias calibration for active scoring
- Steelman reminder when review is expected
- Deep-review escalation at C3+

---

## Content Design Principles

1. **Imperative voice.** All directives use "Score", "Assess", "Apply", "Check" -- not "it is recommended" or "you might consider". Per EN-404 TASK-004, imperative voice achieves ~90% compliance vs ~40% for passive advisory.

2. **Reference-oriented.** Points Claude to `.claude/rules/` for full details rather than duplicating content. The preamble provides the framework; the rules provide the specifics.

3. **Structured with XML tags.** Each section is independently parseable (REQ-403-094). Claude can reference `<quality-gate>` without reading the full block.

4. **Ordered by salience.** Within the strategy list, scoring backbone (S-014) comes first. Within the preamble, quality-gate comes first. Highest-enforcement-value content has the best position for surviving context rot.

5. **Binary constraints.** "Do not bypass" (not "try to complete"). "Cannot be overridden" (not "should generally be followed"). Per EN-404 TASK-004, binary rules have highest compliance.

---

## Traceability

### Requirements Covered

| Requirement | Coverage |
|-------------|----------|
| FR-405-001 | Section 1 `<quality-gate>` includes >= 0.92 threshold |
| FR-405-002 | Section 2 `<constitutional-principles>` includes P-003, P-020, P-022, UV |
| FR-405-003 | Section 3 `<adversarial-strategies>` lists all 10 strategies |
| FR-405-004 | Section 4 `<decision-criticality>` includes C1-C4 + auto-escalation |
| FR-405-005 | Section 1 `<quality-gate>` includes 3-iteration cycle requirement |
| FR-405-006 | Section 1 `<quality-gate>` includes leniency bias note |
| FR-405-007 | Section 4 `<decision-criticality>` includes AUTO-ESCALATE rule |
| FR-405-010 | Top-level `<quality-framework version="1.0">` wrapper |
| FR-405-011 | Exactly 4 XML subsections defined |
| FR-405-012 | Each section independently parseable |
| FR-405-013 | All content uses imperative voice |
| FR-405-020 | All 10 strategies listed in Section 3 |
| FR-405-021 | Per-criticality strategy activation sets documented |
| FR-405-022 | Auto-escalation rules documented (consolidated in Section 4) |
| SR-405-001 | Awareness-only content (not runtime selection) |
| SR-405-002 | Strategy ordering by role prominence |
| SR-405-003 | No per-strategy token costs in preamble |
| SR-405-004 | No ENF-MIN content in preamble |
| SR-405-005 | SYN #1 pairing in quality-gate section |

---

## References

| # | Document | Content Used |
|---|----------|--------------|
| 1 | EN-403 TASK-004 (SessionStart Design) | Primary reference: XML format, content spec, token budget, integration |
| 2 | Barrier-2 ADV-to-ENF Handoff | Per-criticality strategy sets, decision tree, auto-escalation rules |
| 3 | EN-404 TASK-003 (Tiered Enforcement) | HARD rules H-13 through H-19, SSOT designation |
| 4 | EN-404 TASK-004 (HARD Language Patterns) | Enforcement language hierarchy, compliance rates |
| 5 | EN-303 TASK-004 (Decision Tree) | Strategy activation per criticality, creator-critic-revision cycle |
| 6 | TASK-001 (this enabler's requirements) | FR-405-xxx, IR-405-xxx, PR-405-xxx, SR-405-xxx |

---

*Agent: ps-architect-405 (Claude Opus 4.6)*
*Date: 2026-02-14*
*Parent: EN-405 Session Context Enforcement Injection*
*Quality Target: >= 0.92*
*Token Budget: ~370 tokens (4 sections)*
