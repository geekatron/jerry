# ST-002: Design and implement auto-documentation module for skills and agents

> **Type:** story
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Created:** 2026-03-08T00:00:00Z
> **Due:**
> **Completed:** 2026-03-12T00:00:00Z
> **Parent:** FEAT-001
> **Owner:**
> **Effort:** 8

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [User Story](#user-story) | As a/I want/So that |
| [Summary](#summary) | Scope and context |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable criteria |
| [Progress Summary](#progress-summary) | Task tracking |
| [Related Items](#related-items) | Hierarchy and dependencies |
| [History](#history) | Status changes |

---

## User Story

**As a** Jerry framework maintainer

**I want** an auto-documentation module that generates README sections from SKILL.md and agent definition frontmatter

**So that** documentation stays accurate automatically as skills and agents are added or modified

---

## Summary

Research auto-documentation patterns, produce an ADR selecting the design approach, conduct a threat model review, and produce an implementation specification for the doc module.

**Scope:**
- Research doc generation patterns (Phase B1)
- Architecture decision for doc module design (Phase B2)
- Threat model for selected design (Phase B3)
- Implementation specification (Phase B4)

---

## Acceptance Criteria

- [x] ADR documents design decision for auto-documentation approach
- [x] Implementation spec covers input parsing, output rendering, and drift detection
- [x] Threat model addresses STRIDE analysis on doc generation pipeline
- [x] Design satisfies H-05 (uv-only) and H-33 (scope clarified: SKILL.md uses YAML, not blockquote)

---

## Progress Summary

| Metric | Value |
|--------|-------|
| **Orchestration** | impl-20260310-001 (C4) |
| **Tasks** | 6 (TASK-001 through TASK-006) |
| **Completed** | 6/6 tasks |
| **Completion %** | 100% |

### Children (Tasks)

| ID | Title | Status | Owner |
|----|-------|--------|-------|
| [TASK-001](TASK-001-foundation-implementation.md) | Implement DocsGenerator handler + SkillExtractor + adapters | completed | eng-backend-1 |
| [TASK-002](TASK-002-cli-bootstrap-wiring.md) | Wire CLI docs namespace to DocsGenerator via bootstrap.py | completed | eng-backend-3 |
| [TASK-003](TASK-003-test-suite.md) | Implement test suite (unit + integration + golden) | completed | eng-qa |
| [TASK-004](TASK-004-security-verification.md) | Security control verification M-1 through M-5 | completed | eng-architect |
| [TASK-005](TASK-005-attack-surface-analysis.md) | Attack surface analysis | completed | red-vuln |
| [TASK-006](TASK-006-final-compliance-gate.md) | Final architecture compliance and coverage gate | completed | eng-reviewer |
| [BUG-001](BUG-001-frontmatter-reader-mismatch.md) | AstFrontmatterReader parses blockquote, not YAML frontmatter | completed | — |

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-001: README & Doc Module](../FEAT-001-readme-doc-module.md)
- **GitHub Issue:** [#148](https://github.com/geekatron/jerry/issues/148)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-08 | Claude | pending | Story created; workstream B |
| 2026-03-10 | Claude | in_progress | Implementation pipeline started (impl-20260310-001) |
| 2026-03-11 | Claude | blocked | All 6 tasks complete. Pipeline barriers 1-4 PASS. BLOCKED by BUG-001: AstFrontmatterReader reads blockquote metadata (Format B) instead of YAML frontmatter (Format A). All 27 skills skipped. `jerry docs generate --check` exits 1. |
| 2026-03-12 | Claude | completed | BUG-001 resolved. YamlFrontmatterReader created. All ACs verified. 30 skills, 89 agents. `jerry docs generate --check` exits 0. |
