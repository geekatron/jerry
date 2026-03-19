# FEAT-001: README & Doc Module — GitHub #148

> **Type:** feature
> **Status:** in_progress
> **Priority:** high
> **Impact:** high
> **Created:** 2026-03-08T00:00:00Z
> **Due:**
> **Completed:**
> **Parent:** EPIC-001
> **Owner:**
> **Target Sprint:**

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and value proposition |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Children Stories/Enablers](#children-storiesenablers) | Story inventory and tracking |
| [Progress Summary](#progress-summary) | Overall feature progress |
| [Related Items](#related-items) | Hierarchy and dependencies |
| [History](#history) | Status changes and key events |

---

## Summary

Update Jerry's README.md to accurately reflect the current framework state (13 skills, 58 agents) and design an auto-documentation module that prevents documentation drift by generating README sections from SKILL.md and agent definition frontmatter.

**Value Proposition:**
- Users and contributors see accurate capability information in the README
- Documentation stays current automatically as skills/agents are added or modified

---

## Acceptance Criteria

### Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | README skills table lists all skills with SKILL.md files | [ ] |
| AC-2 | README agent count matches AGENTS.md verified count | [ ] |
| AC-3 | ADR documents the selected auto-documentation approach | [ ] |
| AC-4 | Implementation spec covers parsing, rendering, and drift detection | [ ] |
| AC-5 | Threat model addresses doc generation pipeline security | [ ] |

---

## Children Stories/Enablers

| ID | Type | Title | Status | Priority |
|----|------|-------|--------|----------|
| [ST-001](./ST-001-update-readme/ST-001-update-readme.md) | Story | Update README.md to reflect current skills, agents, and repository state | in_progress | high |
| [ST-002](./ST-002-auto-doc-module/ST-002-auto-doc-module.md) | Story | Design and implement auto-documentation module for skills and agents | pending | high |

---

## Progress Summary

| Metric | Value |
|--------|-------|
| **Total Stories** | 2 |
| **Completed Stories** | 0 |
| **Completion %** | 0% |

---

## Related Items

### Hierarchy

- **Parent Epic:** [EPIC-001: Documentation & Auto-Documentation](../EPIC-001-documentation.md)
- **GitHub Issue:** [#148](https://github.com/geekatron/jerry/issues/148)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-08 | Claude | in_progress | Feature created with ST-001, ST-002 |
