# FEAT-003: Future Enhancements

<!--
TEMPLATE: Feature
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.4
CREATED: 2026-01-26 per DISC-002 decision
-->

> **Type:** feature
> **Status:** PLANNED
> **Priority:** low
> **Created:** 2026-01-26T23:00:00Z
> **Parent:** EPIC-001
> **Owner:** Claude

---

## Summary

Future enhancements for the Transcript Skill that are explicitly marked as "Above and Beyond" scope. These features are not required for MVP delivery but provide additional value.

**Origin:** [DISC-002: Future Scope Analysis](../FEAT-002-implementation/FEAT-002--DISC-002-future-scope-analysis.md)

---

## Scope

This feature captures functionality that was originally planned for FEAT-002 but was determined to be optional/future scope:

| Enabler | Original Location | Rationale for Deferral |
|---------|-------------------|------------------------|
| EN-012: Skill CLI Interface | FEAT-002 GATE-7 | Explicitly marked "Above and Beyond - LITERALLY LAST" |

**Future Candidates:**
- Real-time streaming support
- Custom entity extractors
- Team/organization context persistence
- Multi-language transcript support

---

## Enablers

### Moved from FEAT-002

| ID | Title | Status | Original Gate |
|----|-------|--------|---------------|
| [EN-012](./EN-012-skill-interface/EN-012-skill-interface.md) | Skill CLI Interface | pending | GATE-7 |

### Tech Debt (Created 2026-01-27)

| ID | Title | Status | Origin |
|----|-------|--------|--------|
| [EN-017](./EN-017-utf16-support/EN-017-utf16-support.md) | UTF-16 BOM Support | pending | EN-007:DEC-001 |
| [EN-018](./EN-018-task-renumbering/EN-018-task-renumbering.md) | FEAT-002 Task Renumbering | pending | Worktracker compliance |

### Interactive Visualization (Created 2026-01-30)

| ID | Title | Status | Origin |
|----|-------|--------|--------|
| [EN-019](./EN-019-d3js-interactive-visualization/EN-019-d3js-interactive-visualization.md) | D3.js Interactive Visualization | pending | DISC-001: Mermaid Limitation |

### Bug Fixes (Created 2026-01-30)

| ID | Title | Status | Origin |
|----|-------|--------|--------|
| [EN-026](./EN-026-token-based-chunking/EN-026-token-based-chunking.md) | Token-Based Chunking with tiktoken | pending | BUG-001: Chunk Token Overflow |

### Agent Enhancements (Created 2026-01-31)

| ID | Title | Status | Origin |
|----|-------|--------|--------|
| [EN-020](./EN-020-adversarial-critic-agents/EN-020-adversarial-critic-agents.md) | Adversarial Critic and Reviewer Agents | pending | FEAT-005: Quality Gate Requirements |

---

## Discoveries

| ID | Title | Status |
|----|-------|--------|
| [DISC-001](./FEAT-003--DISC-001-mermaid-static-visualization-limitation.md) | Mermaid Static Visualization Limitation | DOCUMENTED |
| [DISC-002](./FEAT-003--DISC-002-adversarial-prompting-protocol.md) | Adversarial Prompting Protocol for Quality Gates | DOCUMENTED |

---

## Dependencies

| Dependency | Description |
|------------|-------------|
| FEAT-002 | Core implementation must be complete |
| EN-016 | ts-formatter required for CLI integration |

---

## Timeline

**Planned Start:** After FEAT-002 GATE-6 approval
**Estimated Duration:** TBD based on FEAT-002 learnings

---

## Related Items

- **Parent Epic:** [EPIC-001: Transcript Skill](../../EPIC-001-transcript-skill.md)
- **Prerequisite:** [FEAT-002: Implementation](../FEAT-002-implementation/FEAT-002-implementation.md)
- **Decision Document:** [DISC-002: Future Scope Analysis](../FEAT-002-implementation/FEAT-002--DISC-002-future-scope-analysis.md)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-26 | Claude | PLANNED | Feature created per DISC-002 decision. EN-012 moved from FEAT-002. |
| 2026-01-27 | Claude | PLANNED | Added EN-017 (UTF-16 support) per EN-007:DEC-001 |
| 2026-01-27 | Claude | PLANNED | Added EN-018 (task renumbering) per worktracker compliance feedback |
| 2026-01-30 | Claude | PLANNED | Added DISC-001 (Mermaid limitation) and EN-019 (D3.js interactive visualization) |
| 2026-01-30 | Claude | PLANNED | Added EN-026 (Token-Based Chunking) to fix BUG-001 (chunk token overflow) |
| 2026-01-31 | Claude | PLANNED | Added EN-020 (Adversarial Critic Agents) and DISC-002 (Adversarial Prompting Protocol) per FEAT-005 requirements |
