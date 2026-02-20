# TASK-002: Rename Colon-Delimited Files to Double-Dash

<!--
TEMPLATE: Task (DRAFT)
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 0.1.0
CREATED: 2026-02-20 (Claude)
-->

> **Type:** task
> **Status:** done
> **Priority:** high
> **Created:** 2026-02-20
> **Completed:** 2026-02-20
> **Parent:** BUG-001

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Content](#content) | Description and acceptance criteria |
| [Evidence](#evidence) | Deliverables and verification |
| [History](#history) | Status changes |

---

## Content

### Description

Rename 4 files that use `:` (colon) as a separator between Epic ID and Discovery/Decision ID. Colons are reserved characters on Windows (used for drive letters like `C:`), causing `git checkout` to fail on Windows CI runners.

**Rename pattern:** `EPIC-001:` -> `EPIC-001--` (double dash, matching PROJ-001 convention)

### Files to Rename

| Current Name | New Name |
|-------------|----------|
| `EPIC-001:DEC-001-feat002-progressive-disclosure.md` | `EPIC-001--DEC-001-feat002-progressive-disclosure.md` |
| `EPIC-001:DISC-001-progressive-disclosure-skill-decomposition.md` | `EPIC-001--DISC-001-progressive-disclosure-skill-decomposition.md` |
| `EPIC-001:DISC-002-training-data-research-errors.md` | `EPIC-001--DISC-002-training-data-research-errors.md` |
| `EPIC-001:DISC-003-supplemental-citation-pipeline.md` | `EPIC-001--DISC-003-supplemental-citation-pipeline.md` |

### Steps

1. `git mv` each file from colon name to double-dash name
2. Verify no files with `:` remain: `git ls-files | grep ':'` returns empty

> **Note:** Internal headings and frontmatter `id:` fields intentionally kept with `:` — these are semantic identifiers (e.g., `EPIC-001:DISC-001`), not filesystem paths. Colons are only invalid in filenames on Windows.

### Acceptance Criteria

- [x] All 4 files renamed from `:` to `--` separator
- [x] `git ls-files | grep ':'` returns empty
- [x] Internal semantic IDs preserved (headings and `id:` fields unchanged)

### Dependencies

- TASK-003 must run after this task (updates references to renamed files)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Renamed DEC-001 | File | `work/EPIC-001-je-ne-sais-quoi/EPIC-001--DEC-001-feat002-progressive-disclosure.md` |
| Renamed DISC-001 | File | `work/EPIC-001-je-ne-sais-quoi/EPIC-001--DISC-001-progressive-disclosure-skill-decomposition.md` |
| Renamed DISC-002 | File | `work/EPIC-001-je-ne-sais-quoi/EPIC-001--DISC-002-training-data-research-errors.md` |
| Renamed DISC-003 | File | `work/EPIC-001-je-ne-sais-quoi/EPIC-001--DISC-003-supplemental-citation-pipeline.md` |

### Verification

- [ ] Acceptance criteria verified
- [ ] `git ls-files | grep ':'` returns empty

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-20 | pending | Task created. 4 files with Windows-incompatible colons in filenames. |
| 2026-02-20 | done | All 4 files renamed via `git mv`. `git ls-files | grep ':'` returns empty. |
