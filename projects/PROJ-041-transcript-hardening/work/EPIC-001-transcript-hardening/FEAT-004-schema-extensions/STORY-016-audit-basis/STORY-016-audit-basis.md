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
| [Schema Addition](#schema-addition) | What gets added |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Children Tasks](#children-tasks) | Task breakdown |
| [Related Items](#related-items) | Links and dependencies |
| [History](#history) | Status changes |

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

## Acceptance Criteria

- [ ] Schema field added: `provenance.audit_basis` in extraction-report.json v1.2.
- [ ] Field is optional.
- [ ] FEAT-003 STORY-008 (`update-anchors`) optionally writes `audit_basis` to extraction-report.json at the same write moment as _anchors.json updates, keeping the two sidecars in lock-step.
- [ ] At least one golden packet has populated audit_basis.
- [ ] Schema validation passes against packets with and without the field.
- [ ] `/adversary` C4 ≥0.95 phase gate.

---

## Children Tasks

| ID | Title | Status |
|----|-------|--------|
| TASK-001 | Author audit_basis schema field | pending |
| TASK-002 | Update extraction-report.json schema | pending |
| TASK-003 | Wire FEAT-003 STORY-008 to update audit_basis | pending |
| TASK-004 | Add golden packet | pending |
| TASK-005 | Run /adversary C4 review | pending |

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
