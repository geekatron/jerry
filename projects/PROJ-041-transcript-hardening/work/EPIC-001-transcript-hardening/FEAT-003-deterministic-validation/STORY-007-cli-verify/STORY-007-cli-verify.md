# STORY-007: `jerry transcript verify <packet>` CLI subcommand

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
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Children Tasks](#children-tasks) | Task breakdown |
| [Related Items](#related-items) | Links and dependencies |
| [History](#history) | Status changes |

---

## User Story

**As a** developer, agent, or CI job,
**I want** `jerry transcript verify <packet>` to mechanically reconcile declared substrate against walked truth,
**So that** I can detect drift in <1 second instead of 30 minutes of manual adversary review.

---

## CLI Surface

```
jerry transcript verify <packet-path> [--json] [--rule <RULE_ID>]... [--fail-fast]

Exit codes:
  0  All rules pass
  1  One or more rules fail
  2  Invalid packet (sidecar files missing or malformed)
  3  Sandbox refusal (subprocess sandbox rejected a pattern — manual review needed)
  64 Usage error
```

Default output: human-readable Markdown report listing pass/fail per rule with evidence.
`--json` flag: machine-readable structured output for CI consumption.
`--rule RULE_ID`: validate specific rule(s) only (e.g., `--rule ANCHOR-002`).
`--fail-fast`: stop on first failure (default: report all failures).

CLI lives at `src/jerry/transcript/validation/interface/cli.py`. A thin shim at `skills/transcript/scripts/validate_packet.py` provides the entrypoint.

---

## Acceptance Criteria

- [ ] `jerry transcript verify <packet>` runs and produces pass/fail report per rule.
- [ ] `--json` flag produces machine-readable output validated against a JSON Schema.
- [ ] `--rule RULE_ID` repeatable flag scopes execution to specific rules.
- [ ] `--fail-fast` stops on first failure.
- [ ] Exit codes match the CLI surface above.
- [ ] Reproduces the audit's iter-9 drift detection on the original packet.
- [ ] Catches the iter-9 regression class in ~300ms (target performance per audit comment 1).
- [ ] Hexagonal architecture (H-07) enforced: command in interface/, handler in application/, schema loading in infrastructure/.
- [ ] Test coverage ≥90% on CLI module.
- [ ] `/adversary` C4 ≥0.95 phase gate.

---

## Children Tasks

| ID | Title | Status |
|----|-------|--------|
| TASK-001 | Author CLI command parser (argparse or click) | pending |
| TASK-002 | Wire CLI to PacketValidator service | pending |
| TASK-003 | Author MarkdownReportRenderer adapter | pending |
| TASK-004 | Author JsonReportRenderer adapter | pending |
| TASK-005 | Add CLI shim at skills/transcript/scripts/validate_packet.py | pending |
| TASK-006 | Author CLI tests (test via entrypoint, not internal API) | pending |
| TASK-007 | Performance test: ~300ms target on standard packet | pending |
| TASK-008 | Run /adversary C4 review | pending |

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-003](../FEAT-003-deterministic-validation.md)

### Dependencies

| Type | Item | Description |
|------|------|-------------|
| Blocked By | STORY-003..STORY-006 | Validators must exist for CLI to invoke |
| Blocks | STORY-009 | post-render hook calls this CLI |
| Blocks | STORY-012 | CI workflow calls this CLI |

### Source

- [#273 comment 1](https://github.com/geekatron/jerry/issues/273#issuecomment-4339264545) — gist proposal item 1

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-04-28 | adam.nowak (via Claude scaffold) | pending | Story created. |
