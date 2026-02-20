# TASK-003: Update All References to Renamed Files

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

After TASK-002 renames the 4 colon-delimited files to double-dash, update all references across the repository that point to the old filenames. This includes markdown links, path references in orchestration artifacts, and cross-references within the files themselves.

### Files Requiring Updates

| File | Reference Type | Count |
|------|---------------|-------|
| `projects/PROJ-003-je-ne-sais-quoi/WORKTRACKER.md` | Markdown links (Discoveries + Decisions tables) | 4 links |
| `projects/.../FEAT-002-saucer-boy-skill/FEAT-002-saucer-boy-skill.md` | Markdown links (Related Items section) | 2 links |
| `projects/.../EPIC-001:DEC-001-feat002-progressive-disclosure.md` | Internal cross-references to DISC-001, DISC-002 | 2 refs |
| `projects/.../orchestration/.../ps-researcher-002-research.md` | Path references in table | 2 refs |
| `projects/.../orchestration/.../synth-001-epic001-final-synthesis.md` | YAML-style path references | 4 refs |
| `projects/.../ORCHESTRATION_PLAN.md` | Path references in table | 3 refs |

### Steps

1. Update WORKTRACKER.md: Replace `EPIC-001:DISC-` with `EPIC-001--DISC-` and `EPIC-001:DEC-` with `EPIC-001--DEC-` in all link paths
2. Update FEAT-002-saucer-boy-skill.md: Replace colon paths in Related Items
3. Update DEC-001 internal cross-references: Replace `EPIC-001:DISC-` with `EPIC-001--DISC-`
4. Update orchestration artifacts: Replace colon paths in research and synthesis docs
5. Verify: `grep -r 'EPIC-001:D' projects/PROJ-003-je-ne-sais-quoi/` returns only content references (headings, IDs inside files), not file path references

### Acceptance Criteria

- [ ] All markdown links updated to use `--` separator
- [ ] All path references in orchestration artifacts updated
- [ ] No broken links remain (file paths with `:` that reference renamed files)
- [ ] `grep -r 'EPIC-001:D' projects/PROJ-003-je-ne-sais-quoi/ | grep -v '\.md:'` returns no path references with colons

### Dependencies

- Blocked by: TASK-002 (files must be renamed first)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Updated WORKTRACKER.md | Code | `projects/PROJ-003-je-ne-sais-quoi/WORKTRACKER.md` |
| Updated FEAT-002 | Code | `projects/.../FEAT-002-saucer-boy-skill.md` |
| Updated orchestration refs | Code | Multiple orchestration files |

### Verification

- [ ] Acceptance criteria verified
- [ ] No broken markdown links

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-20 | pending | Task created. ~17 references across 6 files need updating. Blocked by TASK-002. |
| 2026-02-20 | done | All references updated across 5 files (WORKTRACKER.md, FEAT-002, ps-researcher-002, synth-001, ORCHESTRATION_PLAN). Verified via grep. |
