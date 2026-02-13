# EN-301: Deep Research: 15 Adversarial Strategies

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-12 (Claude)
PURPOSE: Research and catalog 15 adversarial review strategies from authoritative sources
-->

> **Type:** enabler
> **Status:** done
> **Resolution:** completed
> **Priority:** critical
> **Impact:** critical
> **Enabler Type:** exploration
> **Created:** 2026-02-12
> **Due:** —
> **Completed:** 2026-02-13
> **Parent:** FEAT-004
> **Owner:** —
> **Effort:** 13

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this enabler delivers |
| [Problem Statement](#problem-statement) | Why this work is needed |
| [Technical Approach](#technical-approach) | How we'll implement it |
| [Children (Tasks)](#children-tasks) | Task breakdown |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Agent Assignments](#agent-assignments) | Which agents are used |
| [Related Items](#related-items) | Dependencies |
| [History](#history) | Change log |

---

## Summary

Deep research into 15 adversarial review strategies from authoritative academic and industry sources. The catalog must cover the five foundational strategies -- Red Team, Blue Team, Devil's Advocate, Steelman, and Strawman -- plus 10 additional strategies drawn from peer-reviewed literature, industry practice, and emerging LLM-specific patterns. Each strategy entry requires: name, description, origin/author, authoritative citation (DOI or ISBN where available), strengths, weaknesses, and typical use contexts. This enabler is the entry point for the entire FEAT-004 research pipeline and all downstream enablers depend on the quality and completeness of this catalog.

## Problem Statement

Jerry's adversarial review capability currently lacks a rigorous, evidence-based foundation. Without a comprehensive catalog of adversarial strategies grounded in authoritative sources, any implementation risks being ad hoc, incomplete, or biased toward well-known techniques while missing more effective approaches. The research must span academic literature (formal argumentation theory, red teaming in cybersecurity, structured analytic techniques from intelligence analysis), industry practices (code review adversarial patterns, design review heuristics), and emerging LLM-specific adversarial patterns (prompt-based adversarial testing, constitutional AI critique methods). A shallow or incomplete catalog would compromise all downstream selection, mapping, and integration work.

## Technical Approach

1. **Academic Literature Review** -- Systematic search of argumentation theory, structured analytic techniques (Heuer & Pherson), red teaming methodology (DoD, RAND), and adversarial ML literature. Prioritize sources with formal definitions, empirical validation, or widespread adoption.
2. **Industry Practice Survey** -- Examine adversarial patterns from software engineering (code review), security (penetration testing, threat modeling), and AI safety (constitutional AI, RLHF critique). Focus on codified practices with documented outcomes.
3. **Emerging/Alternative Approaches** -- Explore less mainstream techniques: Pre-mortem analysis, Dialectical Inquiry, Socratic Method variants, Assumption-Based Planning, Delphi adversarial rounds, and LLM-specific patterns like chain-of-thought critique and multi-persona debate.
4. **Synthesis** -- Consolidate findings into a unified catalog with consistent structure per strategy. Apply two rounds of adversarial review (creator-critic cycle) to stress-test completeness and accuracy.
5. **Validation** -- Final validation pass ensuring all 15 strategies meet quality criteria: authoritative citation, clear differentiation from other strategies, and actionable description.

## Children (Tasks)

| ID | Title | Status | Activity | Agents |
|----|-------|--------|----------|--------|
| TASK-001 | Research academic literature on adversarial review | done | RESEARCH | ps-researcher |
| TASK-002 | Research industry practices and LLM-specific patterns | done | RESEARCH | ps-researcher |
| TASK-003 | Research alternative/emerging adversarial approaches | done | RESEARCH | nse-explorer |
| TASK-004 | Synthesize findings into unified 15-strategy catalog | done | RESEARCH | ps-synthesizer |
| TASK-005 | Adversarial review iteration 1 (Red Team + Devil's Advocate) | done | TESTING | ps-critic |
| TASK-006 | Creator revision based on critic feedback | done | DEVELOPMENT | ps-researcher |
| TASK-007 | Adversarial review iteration 2 | done | TESTING | ps-critic |
| TASK-008 | Final validation | done | TESTING | ps-validator |

### Task Dependencies

```
TASK-001 ──┐
TASK-002 ──┼──> TASK-004 ──> TASK-005 ──> TASK-006 ──> TASK-007 ──> TASK-008
TASK-003 ──┘
```

## Acceptance Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| 1 | Catalog contains exactly 15 distinct adversarial strategies | [x] |
| 2 | Red Team, Blue Team, Devil's Advocate, Steelman, and Strawman are included | [x] (Blue Team → R-6 per EN-301-DEV-001, ratified by user 2026-02-13; Strawman subsumed by Red Team; Pre-Mortem and Dialectical Inquiry substituted) |
| 3 | Each strategy has: name, description, origin/author, citation, strengths, weaknesses, use contexts | [x] |
| 4 | At least 10 of 15 strategies have authoritative citations (DOI, ISBN, or official publication) | [x] |
| 5 | Strategies span at least 3 domains (academic, industry, LLM/AI-specific) | [x] |
| 6 | No two strategies are redundant or insufficiently differentiated | [x] |
| 7 | Two adversarial review iterations completed with documented feedback and revisions | [x] (iter1: 0.89, iter2: 0.936) |
| 8 | Final validation pass confirms all criteria met | [x] (TASK-008: PASS 8/8) |

## Agent Assignments

| Agent | Skill | Role | Phase |
|-------|-------|------|-------|
| ps-researcher | /problem-solving | Creator -- primary research and revision | TASK-001, TASK-002, TASK-006 |
| ps-critic | /problem-solving | Adversarial -- Red Team + Devil's Advocate review | TASK-005, TASK-007 |
| ps-synthesizer | /problem-solving | Synthesis -- consolidate multi-source findings | TASK-004 |
| nse-explorer | /nasa-se | Alternative generation -- emerging approaches | TASK-003 |
| ps-validator | /problem-solving | Validation -- final quality gate | TASK-008 |

## Related Items

### Hierarchy
- **Parent Feature:** [FEAT-004](../FEAT-004-adversarial-strategy-research.md)

### Dependencies
| Type | Item | Description |
|------|------|-------------|
| blocks | EN-302 | Strategy selection depends on complete 15-strategy catalog |
| blocks | EN-303 | Situational mapping depends on strategy catalog |
| blocks | EN-304 | Skill enhancement depends on finalized strategies |

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-12 | Claude | pending | Enabler created with task decomposition. Entry point for FEAT-004 research pipeline. |
| 2026-02-12 | Claude | in_progress | Research execution started. TASK-001 (academic), TASK-002 (industry), TASK-003 (emerging) launched in parallel. |
| 2026-02-13 | Claude | in_progress | TASK-001, TASK-002, TASK-003 all complete. TASK-004 (synthesis) completed by ps-synthesizer: unified 15-strategy catalog produced. All task entity files rewritten to use official /worktracker TASK template. |
| 2026-02-13 | Claude | in_progress | Full pipeline complete: TASK-005 (iter1 review, 0.89), TASK-006 (revision, all 12 findings addressed), TASK-007 (iter2 review, 0.936 PASS), TASK-008 (final validation, 8/8 AC PASS). |
| 2026-02-13 | User | done | User ratified EN-301-DEV-001: Pre-Mortem/Dialectical Inquiry confirmed as active strategies. Blue Team added as Reserved Strategy R-6. Web validation of citations and S-015 experiments noted as follow-ups. EN-301 marked DONE. |
