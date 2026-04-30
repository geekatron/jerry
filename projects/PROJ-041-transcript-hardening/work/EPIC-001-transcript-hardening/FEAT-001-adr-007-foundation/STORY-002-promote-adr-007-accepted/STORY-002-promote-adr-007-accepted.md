# STORY-002: Promote ADR-007 status PROPOSED → ACCEPTED

> **Type:** story
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Created:** 2026-04-28T00:00:00Z
> **Parent:** FEAT-001
> **Owner:** adam.nowak
> **Effort:** 2

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [User Story](#user-story) | As a / I want / So that |
| [Summary](#summary) | What needs to happen |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Agent Assignment](#agent-assignment) | Specific skill+agent mappings for execution |
| [Children Tasks](#children-tasks) | Task breakdown |
| [Related Items](#related-items) | Links and dependencies |
| [History](#history) | Status changes |

---

## User Story

**As a** `/transcript` agent or human reviewer,
**I want** ADR-007 to have status `ACCEPTED`,
**So that** the MUST/SHALL language in SKILL.md, ts-formatter.md, and ADR-007 §4 itself is no longer incoherent (it's incoherent today: "MUST follow this PROPOSED ADR").

---

## Summary

ADR-007 frontmatter currently says `Status: PROPOSED`. SKILL.md and agent specs reference its rules as MUST-USE. Resolve by changing status to `ACCEPTED` after FEAT-002 (the 5 contradictions) closes — so the baselined ADR-007 inherits no contradictions. (Audit Option B — "downgrade SKILL.md language to SHOULD/MAY" — is rejected: we want enforcement, not less of it.)

Per AE-004, modifying a baselined ADR is C4 — but we are *baselining* the ADR for the first time, which makes this story C3+. Still subject to `/adversary` C4 ≥0.95 phase gate.

---

## Acceptance Criteria

- [ ] `docs/adrs/ADR-007-output-template-specification.md` frontmatter shows `Status: ACCEPTED`.
- [ ] ADR-007 History section records the status transition with date, author, and rationale linking to this Story.
- [ ] All 5 Bugs in FEAT-002 are status `completed` before this Story moves to `in_progress`.
- [ ] Cross-references in SKILL.md and ts-formatter.md need no language change (MUST language remains coherent post-promotion).
- [ ] `/adversary` C4 ≥0.95 review on the ADR + dependent docs (governance change is C3+).

---

## Agent Assignment

| Step | Skill | Agent | Purpose |
|------|-------|-------|---------|
| 1 | `/worktracker` | `wt-auditor` | Verify all 5 FEAT-002 Bugs are status `completed` with delivery evidence before allowing this Story to start |
| 2 | `/problem-solving` | `ps-architect` | Update ADR-007 frontmatter `Status: PROPOSED` → `ACCEPTED`; add History entry with date/author/rationale |
| 3 | `/eng-team` | `eng-architect` | Architecture compliance review: confirm ADR-007 baselining inherits no contradictions and aligns with existing ADR-001..006. **Deliverable:** authors compliance memo at `projects/PROJ-041-transcript-hardening/work/EPIC-001-transcript-hardening/FEAT-001-adr-007-foundation/STORY-002-promote-adr-007-accepted/adr-007-baselining-compliance-memo.md` per ps-architect D-4.1 (AE-004 baselined-ADR review must produce written compliance evidence). |
| 4 | `/adversary` | `adv-selector` → `adv-executor` → `adv-scorer` | C4 ≥0.95 review (mandatory C4 per AE-004: modifying baselined ADR + project-wide stricter threshold) |
| 5 | `/worktracker` | `wt-verifier` | Validate AC; gate move to `completed` |

---

## Children Tasks

| ID | Title | Owner | Status |
|----|-------|-------|--------|
| [TASK-011](./TASK-011-verify-feat-002-bugs-completed.md) | Verify all 5 FEAT-002 Bugs are completed with delivery evidence | `wt-auditor` | pending |
| [TASK-012](./TASK-012-update-adr-007-status-to-accepted.md) | Update ADR-007 frontmatter Status PROPOSED → ACCEPTED | `ps-architect` | pending |
| [TASK-013](./TASK-013-add-history-entry-to-adr-007.md) | Add History entry to ADR-007 documenting promotion | `ps-architect` | pending |
| [TASK-014](./TASK-014-architecture-compliance-review-memo.md) | Architecture compliance review memo (per ps-architect D-4.1) | `eng-architect` | pending |
| [TASK-015](./TASK-015-run-adversary-c4-on-promotion.md) | Run /adversary C4 review on promotion (mandatory per AE-004) | `adv-executor` | pending |
| [TASK-016](./TASK-016-validate-ac-and-close-story-002.md) | Validate STORY-002 acceptance criteria and close | `wt-verifier` | pending |

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-001](../FEAT-001-adr-007-foundation.md)

### Dependencies

| Type | Item | Description |
|------|------|-------------|
| Blocked By | STORY-001 | Vendoring must complete |
| Blocked By | FEAT-002 (all 5 bugs) | Contradictions must be resolved before baselining |
| Blocks | FEAT-003 | Validators implementing PROPOSED ADR is incoherent |
| Blocks | EN-008 | Final tournament cannot pass while governance is incoherent |

### Source

- [#273 §C2](https://github.com/geekatron/jerry/issues/273)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-04-28 | adam.nowak (via Claude scaffold) | pending | Story created. P1 governance. Option A (promote) chosen over Option B (relax language). |
