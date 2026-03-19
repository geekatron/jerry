# PROJ-0037-doc-module: Documentation & Auto-Documentation - Work Tracker

> Global Manifest for PROJ-0037-doc-module. Tracks Epics, Bugs, Decisions, Discoveries, and Impediments.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Project metadata |
| [Epics](#epics) | Strategic work items |
| [Bugs](#bugs) | Defect tracking |
| [Decisions](#decisions) | Key decisions |
| [Discoveries](#discoveries) | Findings during work |
| [History](#history) | Change log |

---

## Summary

| Field | Value |
|-------|-------|
| **Project ID** | PROJ-0037-doc-module |
| **Status** | IN_PROGRESS |
| **Created** | 2026-03-08 |
| **GitHub Issue** | [#148](https://github.com/geekatron/jerry/issues/148) |

---

## Epics

| ID | Title | Status | Priority |
|----|-------|--------|----------|
| [EPIC-001](./work/EPIC-001-documentation/EPIC-001-documentation.md) | Documentation & Auto-Documentation — GitHub #148 | in_progress | high |

---

## Bugs

| ID | Title | Status | Severity | Blocks |
|----|-------|--------|----------|--------|
| [BUG-001](./work/EPIC-001-documentation/FEAT-001-readme-doc-module/ST-002-auto-doc-module/BUG-001-frontmatter-reader-mismatch.md) | AstFrontmatterReader parses blockquote, not YAML frontmatter | completed | critical/blocking | ST-001, ST-002, FEAT-001 |
| [BUG-002](./work/EPIC-001-documentation/FEAT-001-readme-doc-module/ST-002-auto-doc-module/BUG-002-template-path-not-anchored.md) | Template path not anchored to repo root | completed | minor | — |
| [BUG-003](./work/EPIC-001-documentation/FEAT-001-readme-doc-module/ST-002-auto-doc-module/BUG-003-truncate-safe-strips-all-brackets.md) | truncate_safe macro strips all bracket characters | completed | minor | — |

---

## Decisions

_None._

---

## Discoveries

| # | Finding | Date | Impact |
|---|---------|------|--------|
| D-001 | Research incorrectly assumed `jerry ast frontmatter` parses `---`-delimited YAML. It parses blockquote `> **Key:** Value` only. No code execution verification was performed before implementation. | 2026-03-11 | BUG-001. All 27 skills skipped. |
| D-002 | Skill count grew from 13 to 27 and agents from 58 to 83 after rebase from main (pm-pmm UX skills merged). Research counts are stale. | 2026-03-11 | `skill-examples.yaml` and `features.yaml` need updating for new skills. |

---

## History

| Date | Author | Action | Notes |
|------|--------|--------|-------|
| 2026-03-08 | Claude | Created | Project worktracker initialized with EPIC-001, FEAT-001, ST-001, ST-002 |
| 2026-03-10 | Claude | Updated | TASK-001 through TASK-006 created under ST-002. Implementation pipeline started. |
| 2026-03-11 | Claude | Updated | TASK-001 through TASK-006 marked completed. BUG-001 filed (blocking). ST-002 status: blocked. Discoveries D-001, D-002 recorded. |
