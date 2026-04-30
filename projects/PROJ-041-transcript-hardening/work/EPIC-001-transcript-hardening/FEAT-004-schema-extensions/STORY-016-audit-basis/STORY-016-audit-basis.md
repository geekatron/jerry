# STORY-016: Add `provenance.audit_basis` for cross-sidecar discoverability

> **Type:** story
> **Status:** pending
> **Priority:** low
> **Impact:** low
> **Created:** 2026-04-28T00:00:00Z
> **Parent:** FEAT-004
> **Owner:** adam.nowak
> **Effort:** 1

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [User Story](#user-story) | As a / I want / So that |
| [Summary](#summary) | What this story delivers |
| [Schema Addition](#schema-addition) | What gets added |
| [Agent Assignment](#agent-assignment) | Specific skill+agent mappings |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Children Tasks](#children-tasks) | Task breakdown |
| [Related Items](#related-items) | Links and dependencies |
| [History](#history) | Status changes |

---

## Summary

Add the optional `provenance.audit_basis` field (option (a) lighter touch per audit comment 2). A reader sees "audit basis: simple-cross-file-grep" and follows the breadcrumb to _anchors.json for full audit-methodology detail. update-anchors writes audit_basis at the same write moment as _anchors.json so the two sidecars stay in lockstep.

---

## User Story

**As a** reader consulting only `extraction-report.json` to understand a packet,
**I want** a single field naming the current audit methodology with breadcrumbs to `_anchors.json` for full detail,
**So that** the two metadata sidecars don't drift silently apart over a packet's lifetime.

---

## Schema Addition

Adds `provenance.audit_basis` (option (a) lighter touch per audit comment 2) to `extraction-report.json` schema v1.2.

```json
{
  "provenance": {
    "audit_basis": "string (e.g., 'simple-cross-file-grep')",
    "methodology_evolution": [
      {
        "method": "string",
        "valid_from_revision": "string",
        "valid_until_revision": "string (optional, ongoing if absent)"
      }
    ]
  }
}
```

A reader sees one line ("audit basis: simple-cross-file-grep") and follows the breadcrumb to `_anchors.json` for full detail.

(Option (b) — full mirroring — was rejected by the audit author as "more code paths to keep synchronized" for marginal benefit.)

---

## Agent Assignment

| Step | Skill | Agent | Purpose |
|------|-------|-------|---------|
| 1 | `/eng-team` | `eng-backend` | Add `provenance.audit_basis` field to extraction-report.json schema (option (a) lighter touch) |
| 2 | `/eng-team` | `eng-backend` | Wire FEAT-003 STORY-008 (update-anchors) to optionally write audit_basis at the same write moment, keeping sidecars in lock-step |
| 3 | `/eng-team` | `eng-qa` | Golden packet with populated audit_basis; schema validates with and without the field |
| 4 | `/adversary` | `adv-executor` + `adv-scorer` | C4 ≥0.95 review |
| 5 | `/worktracker` | `wt-verifier` | Validate AC; close |

---

## Acceptance Criteria

- [ ] Schema field added: `provenance.audit_basis` in extraction-report.json v1.2.
- [ ] Field is optional.
- [ ] FEAT-003 STORY-008 (`update-anchors`) optionally writes `audit_basis` to extraction-report.json at the same write moment as _anchors.json updates, keeping the two sidecars in lock-step.
- [ ] At least one golden packet has populated audit_basis.
- [ ] Schema validation passes against packets with and without the field.
- [ ] `/adversary` C4 ≥0.95 phase gate.

---

## Children Tasks

| ID | Title | Owner | Status |
|----|-------|-------|--------|
| [TASK-158](./TASK-158-add-audit-basis-field-to-schema.md) | Add provenance.audit_basis field to extraction-report.json schema (option (a) lighter touch) | `eng-backend` | pending |
| [TASK-159](./TASK-159-wire-update-anchors-write-audit-basis.md) | Wire FEAT-003 STORY-008 update-anchors to optionally write audit_basis to extraction-report.json | `eng-backend` | pending |
| [TASK-160](./TASK-160-golden-packet-with-audit-basis.md) | Golden packet with populated audit_basis | `eng-qa` | pending |
| [TASK-161](./TASK-161-run-adversary-review.md) | Run /adversary review | `adv-executor` | pending |
| [TASK-162](./TASK-162-validate-ac-and-close-story-016.md) | Validate STORY-016 AC and close | `wt-verifier` | pending |

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-004](../FEAT-004-schema-extensions.md)

### Dependencies

| Type | Item | Description |
|------|------|-------------|
| Blocked By | FEAT-001 STORY-001, STORY-002 | ADR-007 vendored + ACCEPTED |
| Cooperates | FEAT-003 STORY-008 | update-anchors writes the field |

### Source

- [#273 comment 2](https://github.com/geekatron/jerry/issues/273#issuecomment-4339392440)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-04-28 | adam.nowak (via Claude scaffold) | pending | Story created. Lower priority — discoverability concern, not correctness. |
