# EN-706: SessionStart Quality Context Enhancement

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-14 (Claude)
PURPOSE: Enhance session start hook with quality framework preamble injection (L1 Static Context)
-->

> **Type:** enabler
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Enabler Type:** infrastructure
> **Created:** 2026-02-14
> **Due:** —
> **Completed:** —
> **Parent:** FEAT-008
> **Owner:** —
> **Effort:** 5

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this enabler delivers |
| [Problem Statement](#problem-statement) | Why this work is needed |
| [Business Value](#business-value) | How this enabler supports the parent feature |
| [Technical Approach](#technical-approach) | How we'll implement it |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Progress Summary](#progress-summary) | Completion status and metrics |
| [Evidence](#evidence) | Proof of completion |
| [Dependencies](#dependencies) | What this depends on |
| [History](#history) | Change log |

---

## Summary

Enhance `scripts/session_start_hook.py` to inject a quality framework preamble at session start (L1 Static Context). Implements the XML quality preamble from EN-405/TASK-006 with 4 sections: quality gate, constitutional principles, adversarial strategies, and decision criticality. Creates a `SessionQualityContextGenerator` class that produces the preamble content, keeping enforcement logic separated from hook infrastructure per hexagonal architecture. The preamble primes Claude to engage the quality framework from the first interaction of every session.

## Problem Statement

Claude's context window resets at each session start. While `.claude/rules/` files are auto-loaded, there is no mechanism to inject a concise, structured quality enforcement preamble that activates mandatory quality processes from the first interaction. The existing `scripts/session_start_hook.py` handles project context resolution but does not inject quality framework directives. Without this, Claude may begin work without activating the quality gate threshold (0.92), constitutional principles, adversarial strategy awareness, or decision criticality definitions. This creates a gap in L1 (Static Context) coverage that L2 (Per-Prompt Reinforcement via EN-705) must compensate for more aggressively.

## Business Value

Primes every new session with quality framework context from the first interaction, ensuring Claude engages quality gates, constitutional principles, and adversarial strategies without delay. This reduces L2 compensation burden and establishes quality awareness at session inception.

### Features Unlocked

- Structured XML quality preamble injection at session start with quality gate, constitutional, strategy, and criticality sections
- Reduced reliance on L2 per-prompt reinforcement for initial session quality

## Technical Approach

1. **Create `SessionQualityContextGenerator` class** -- Located in `src/infrastructure/internal/enforcement/session_quality_context_generator.py`. Responsible for assembling the XML quality preamble with 4 sections. Keeps enforcement logic separated from the session start hook infrastructure.

2. **Design XML quality preamble** -- Structured XML block containing:
   - **Quality Gate section:** 0.92 threshold, creator-critic-revision cycle (minimum 3 iterations), scoring rubric reference
   - **Constitutional Principles section:** P-003 (No Recursive Subagents), P-020 (User Authority), P-022 (No Deception)
   - **Adversarial Strategy Encodings section:** Strategy identifiers S-001 through S-014 with brief descriptions for reference
   - **Decision Criticality Definitions section:** C1 (Reversible, low impact) through C4 (Irreversible, high impact) with escalation rules

3. **Enforce token budget** -- Preamble must be under 700 tokens to avoid excessive L1 context consumption. The generator validates content length and trims if necessary.

4. **Integrate into `scripts/session_start_hook.py`** -- Add quality preamble injection after the existing project context output. Ensure no regression in project context resolution functionality. The quality preamble is emitted as a `<quality-context>` XML block.

5. **Testing** -- Unit tests for `SessionQualityContextGenerator` (content generation, token budget, XML structure). Verify integration with existing session start hook. Verify `uv run pytest` passes.

**Design Source:** EPIC-002 EN-403/TASK-004 (SessionStart design), EN-405/TASK-006 (preamble content)

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                   ENABLER PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Tasks:     [████████████████████] 100% (4/4 completed)           |
| Effort:    [████████████████████] 100% (5/5 points completed)    |
+------------------------------------------------------------------+
| Overall:   [████████████████████] 100%                            |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Tasks** | 4 |
| **Completed Tasks** | 4 |
| **Completion %** | 100% |

## Acceptance Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| 1 | `SessionQualityContextGenerator` class created in `src/infrastructure/internal/enforcement/session_quality_context_generator.py` | [ ] |
| 2 | XML preamble injected into session start output | [ ] |
| 3 | Contains quality gate section (0.92 threshold, creator-critic-revision cycle) | [ ] |
| 4 | Contains constitutional principles (P-003, P-020, P-022) | [ ] |
| 5 | Contains strategy encodings (S-001 through S-014) | [ ] |
| 6 | Contains criticality definitions (C1-C4) | [ ] |
| 7 | Preamble under 700 tokens | [ ] |
| 8 | Unit tests for generator | [ ] |
| 9 | No regression in existing session start hook functionality | [ ] |
| 10 | `uv run pytest` passes | [ ] |

## Evidence

### Deliverables

| Deliverable | Type | Description | Link |
|-------------|------|-------------|------|
| SessionQualityContextGenerator | Source Code | Quality preamble generator class | `src/infrastructure/internal/enforcement/session_quality_context_generator.py` |
| Enhanced session_start_hook.py | Hook Script | Session start hook with quality preamble injection | `scripts/session_start_hook.py` |
| Unit Tests | Test Suite | Generator and integration tests | `tests/` |

### Verification Checklist

- [x] All acceptance criteria verified
- [x] All tasks completed
- [x] Quality gate passed (>= 0.92)

## Dependencies

| Type | Item | Description |
|------|------|-------------|
| depends_on | EN-403 | Hook-based enforcement design (TASK-004: SessionStart design) |
| depends_on | EN-405 | Session context enforcement (TASK-006: preamble content design) |
| related_to | EN-705 | UserPromptSubmit hook (L2) compensates for L1 context rot including this preamble |
| parent | FEAT-008 | Quality Framework Implementation |

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-14 | Claude | pending | Enabler created. Enhances session start with L1 quality framework preamble. 4 sections: quality gate, constitutional principles, adversarial strategies, decision criticality. 700-token budget. Design sourced from EPIC-002 EN-403/TASK-004 and EN-405/TASK-006. |
