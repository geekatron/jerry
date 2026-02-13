# EN-401: Deep Research: Enforcement Vectors & Best Practices

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-12 (Claude)
PURPOSE: Comprehensive research on all enforcement vectors available for Claude Code
-->

> **Type:** enabler
> **Status:** in_progress
> **Priority:** critical
> **Impact:** critical
> **Enabler Type:** exploration
> **Created:** 2026-02-12
> **Due:** —
> **Completed:** —
> **Parent:** FEAT-005
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

Comprehensive research on ALL enforcement vectors available for Claude Code: hooks (UserPromptSubmit, PreToolUse, SessionStart, Stop), rules (.claude/rules/), prompt engineering patterns, session start context injection, pre-commit checks. Include LLM guardrail frameworks, industry best practices, and prior art with authoritative citations.

## Problem Statement

Jerry's quality framework requires enforcement mechanisms to ensure agents follow coding standards, architecture rules, and workflow processes. Without a thorough understanding of all available enforcement vectors, their capabilities, limitations, and trade-offs, we risk implementing suboptimal or incomplete enforcement. This research enabler establishes the knowledge foundation for all subsequent enforcement decisions and implementations.

## Technical Approach

1. **Systematic vector enumeration** - Catalog every enforcement mechanism available in Claude Code (hooks, rules, prompt engineering, context injection, pre-commit).
2. **Framework survey** - Research industry LLM guardrail frameworks (Guardrails AI, NeMo Guardrails, LangChain guardrails) for patterns and prior art.
3. **Effectiveness assessment** - For each vector, document capabilities, limitations, reliability, and failure modes.
4. **Platform portability analysis** - Assess which vectors are Claude Code-specific vs. portable to other LLM platforms.
5. **Adversarial validation** - Apply Devil's Advocate and Red Team patterns to stress-test findings.
6. **Synthesis** - Produce a unified enforcement vector catalog with authoritative citations.

## Children (Tasks)

| ID | Title | Status | Activity | Agents |
|----|-------|--------|----------|--------|
| TASK-001 | Research Claude Code hooks API and capabilities | done | RESEARCH | ps-researcher |
| TASK-002 | Research LLM guardrail frameworks (Guardrails AI, NeMo Guardrails, LangChain guardrails) | done | RESEARCH | ps-researcher |
| TASK-003 | Research .claude/rules/ enforcement patterns and effectiveness | pending | RESEARCH | ps-researcher |
| TASK-004 | Research prompt engineering enforcement patterns | pending | RESEARCH | ps-researcher |
| TASK-005 | Explore alternative/emerging enforcement approaches | pending | RESEARCH | nse-explorer |
| TASK-006 | Platform portability assessment for each vector | pending | RESEARCH | ps-analyst |
| TASK-007 | Synthesize all research into unified enforcement vector catalog | pending | RESEARCH | ps-synthesizer |
| TASK-008 | Adversarial review iteration 1 (Devil's Advocate + Red Team) | pending | TESTING | ps-critic |
| TASK-009 | Creator revision based on critic feedback | pending | DEVELOPMENT | ps-researcher |
| TASK-010 | Adversarial review iteration 2 | pending | TESTING | ps-critic |
| TASK-011 | Final validation | pending | TESTING | ps-validator |

### Task Dependencies

```
TASK-001 ──┐
TASK-002 ──┤
TASK-003 ──┼──► TASK-007 ──► TASK-008 ──► TASK-009 ──► TASK-010 ──► TASK-011
TASK-004 ──┤
TASK-005 ──┤
TASK-006 ──┘
```

## Acceptance Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| 1 | All Claude Code hook types (UserPromptSubmit, PreToolUse, SessionStart, Stop) are documented with capabilities and limitations | [ ] |
| 2 | .claude/rules/ enforcement patterns are cataloged with effectiveness ratings | [ ] |
| 3 | At least 3 industry LLM guardrail frameworks are surveyed with key findings | [ ] |
| 4 | Prompt engineering enforcement patterns are documented with examples | [ ] |
| 5 | Platform portability assessment completed for each vector | [ ] |
| 6 | Unified enforcement vector catalog produced with authoritative citations | [ ] |
| 7 | Adversarial review completed with at least 2 iterations | [ ] |
| 8 | All findings have authoritative citations (documentation, papers, or verified sources) | [ ] |

## Agent Assignments

| Agent | Skill | Role | Phase |
|-------|-------|------|-------|
| ps-researcher | problem-solving | Creator (primary research) | Research, Revision |
| ps-critic | problem-solving | Adversarial reviewer (Devil's Advocate + Red Team) | Review |
| nse-explorer | nasa-se | Alternative approach exploration | Research |
| ps-analyst | problem-solving | Platform portability assessment | Research |
| ps-synthesizer | problem-solving | Research synthesis | Synthesis |
| ps-validator | problem-solving | Final validation | Validation |

## Related Items

### Hierarchy
- **Parent Feature:** [FEAT-005](../FEAT-005-enforcement-mechanisms.md)

### Dependencies
| Type | Item | Description |
|------|------|-------------|
| — | — | No dependencies. This is the entry point for FEAT-005. |

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-12 | Claude | pending | Enabler created with task decomposition. |
| 2026-02-12 | Claude | in_progress | Research started. TASK-001 (Claude Code hooks) and TASK-002 (LLM guardrail frameworks) launched in parallel. |
