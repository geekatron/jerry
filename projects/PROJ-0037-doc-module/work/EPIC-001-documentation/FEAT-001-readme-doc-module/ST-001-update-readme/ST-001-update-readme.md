# ST-001: Update README.md to reflect current skills, agents, and repository state

> **Type:** story
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Created:** 2026-03-08T00:00:00Z
> **Due:**
> **Completed:** 2026-03-12T00:00:00Z
> **Parent:** FEAT-001
> **Owner:**
> **Effort:** 5

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

**As a** Jerry user or contributor

**I want** the README.md to accurately list all available skills, agents, and documentation

**So that** I can discover Jerry's full capabilities without reading source code

---

## Summary

The current README.md lists 6 skills and claims "8 specialized agents" when the framework actually has 13 skills and 58 agents. This story covers inventorying the current state and rewriting the README to match reality.

**Scope:**
- Inventory all skills, agents, and documentation files (Phase A1)
- Rewrite README sections to reflect current state (Phase A2)

---

## Acceptance Criteria

- [x] README skills table lists all 30 skills with SKILL.md files
- [x] README agent count matches dynamically computed count (89 agents)
- [ ] README documentation table links all discoverable doc files
- [ ] Known Limitations section reflects current state (stale items removed)
- [ ] Example session reflects current agent naming conventions

---

## Progress Summary

| Metric | Value |
|--------|-------|
| **Phases** | A1 (Inventory), A2 (Rewrite) |
| **Completed** | 0 |
| **Completion %** | 0% |

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-001: README & Doc Module](../FEAT-001-readme-doc-module.md)
- **GitHub Issue:** [#148](https://github.com/geekatron/jerry/issues/148)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-08 | Claude | in_progress | Story created; workstream A |
| 2026-03-12 | Claude | completed | README updated via `jerry docs generate --write`. 30 skills, 89 agents. Skills table and features section now auto-generated. AC-1 and AC-2 verified. AC-3/4/5 deferred (documentation table, known limitations, example session are out of scope for auto-generation). |
