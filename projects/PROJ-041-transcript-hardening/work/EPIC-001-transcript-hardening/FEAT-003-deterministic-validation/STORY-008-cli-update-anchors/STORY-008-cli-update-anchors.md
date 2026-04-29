# STORY-008: `jerry transcript update-anchors <packet>` CLI subcommand

> **Type:** story
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Created:** 2026-04-28T00:00:00Z
> **Parent:** FEAT-003
> **Owner:** adam.nowak
> **Effort:** 3

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [User Story](#user-story) | As a / I want / So that |
| [CLI Surface](#cli-surface) | Command shape and exit codes |
| [Agent Assignment](#agent-assignment) | Specific skill+agent mappings |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Children Tasks](#children-tasks) | Task breakdown |
| [Related Items](#related-items) | Links and dependencies |
| [History](#history) | Status changes |

---

## User Story

**As a** `ts-formatter` agent or developer fixing an audited packet,
**I want** `jerry transcript update-anchors <packet>` to walk the declared patterns and write the walked counts back into `_anchors.json`,
**So that** declared counts become a cache of walked truth — never a hand-maintained assertion that can drift.

---

## CLI Surface

```
jerry transcript update-anchors <packet-path> [--dry-run] [--bucket <BUCKET>]...

Exit codes:
  0  Updated successfully (or no changes needed in --dry-run)
  1  Drift detected and updated (informational; not a failure)
  2  Invalid packet
  3  Sandbox refusal
  64 Usage error
```

`--dry-run`: report what would change without writing.
`--bucket BUCKET`: scope to specific buckets (e.g., `--bucket spk_links --bucket disc_links`).

After this Story, the iter-9 regression class **cannot occur**: the substrate is mechanically derived at every write rather than hand-attested.

---

## Agent Assignment

| Step | Skill | Agent | Purpose |
|------|-------|-------|---------|
| 1 | `/eng-team` | `eng-backend` | Implement UpdateAnchorsService (application layer); atomic-write infrastructure adapter (temp file + rename pattern) |
| 2 | `/eng-team` | `eng-backend` | Wire CLI command in interface/cli.py with `--dry-run` and `--bucket` flags; add `last_walked_at` audit trail |
| 3 | `/eng-team` | `eng-security` | Code review on atomic-write semantics; verify no partial-write window |
| 4 | `/red-team` | `red-exploit` | Probe for race condition / partial-write window via concurrent write simulation |
| 5 | `/eng-team` | `eng-qa` | Test suite: dry-run, scoped buckets, atomicity under concurrent write simulation |
| 6 | `/adversary` | `adv-executor` + `adv-scorer` | C4 ≥0.95 review |
| 7 | `/worktracker` | `wt-verifier` | Validate AC; close |

---

## Acceptance Criteria

- [ ] `jerry transcript update-anchors <packet>` walks declared patterns through SubprocessSandbox and writes walked counts back to `_anchors.json`.
- [ ] `--dry-run` reports changes without writing (use case: pre-flight check before commit).
- [ ] `--bucket` scopes to specific buckets.
- [ ] Atomic write: no partial updates on failure (use temp file + rename pattern).
- [ ] Audit trail: each `_anchors.json` write updates a `last_walked_at` timestamp.
- [ ] STORY-014 (`arithmetic_invariants`) compatibility: `update-anchors` also updates `arithmetic_invariants.computed` field where present.
- [ ] STORY-016 (`audit_basis`) compatibility: optionally writes audit_basis field to `extraction-report.json` at the same write moment, keeping the two sidecars in lock-step.
- [ ] Test coverage ≥90%.
- [ ] `/red-team` validates atomicity (no race condition / partial-write window).
- [ ] `/adversary` C4 ≥0.95 phase gate.

---

## Children Tasks

| ID | Title | Status |
|----|-------|--------|
| TASK-001 | Author UpdateAnchorsService (application layer) | pending |
| TASK-002 | Author atomic-write infrastructure adapter | pending |
| TASK-003 | Wire CLI command in interface/cli.py | pending |
| TASK-004 | Add --dry-run mode | pending |
| TASK-005 | Add --bucket scoping | pending |
| TASK-006 | Add audit trail (last_walked_at) | pending |
| TASK-007 | Test atomicity (concurrent write simulation) | pending |
| TASK-008 | Run /red-team validation on atomicity | pending |
| TASK-009 | Run /adversary C4 review | pending |

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-003](../FEAT-003-deterministic-validation.md)

### Dependencies

| Type | Item | Description |
|------|------|-------------|
| Blocked By | EN-003 | SubprocessSandbox |
| Blocked By | STORY-005 | ANCHOR-* validators provide the walking primitive |
| Blocks | STORY-010 | write pipeline integration |
| Cooperates | FEAT-004 STORY-014, STORY-016 | Schema additions extend update behavior |

### Source

- [#273 comment 1](https://github.com/geekatron/jerry/issues/273#issuecomment-4339264545) — gist proposal items 1 + 3

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-04-28 | adam.nowak (via Claude scaffold) | pending | Story created. |
