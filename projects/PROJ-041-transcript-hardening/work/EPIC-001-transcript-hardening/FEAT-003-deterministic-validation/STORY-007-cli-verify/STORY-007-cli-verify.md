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
| [Summary](#summary) | What this story delivers |
| [CLI Surface](#cli-surface) | Command shape and exit codes |
| [Agent Assignment](#agent-assignment) | Specific skill+agent mappings |
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

## Summary

Build the `jerry transcript verify <packet>` CLI subcommand. Mechanically reconciles declared substrate against walked truth in <1 second instead of 30 minutes of manual adversary review. Hexagonal architecture per H-07 (interface/application/infrastructure layers).

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

## Agent Assignment

| Step | Skill | Agent | Purpose |
|------|-------|-------|---------|
| 1 | `/eng-team` | `eng-backend` | Implement CLI command parser, wire to PacketValidator service per H-07 (interface/cli.py + skills/transcript/scripts/validate_packet.py shim) |
| 2 | `/eng-team` | `eng-backend` | Author MarkdownReportRenderer + JsonReportRenderer adapters (infrastructure layer) |
| 3 | `/eng-team` | `eng-qa` | CLI integration tests via entrypoint; performance test (~300ms target); JSON output schema validation |
| 4 | `/problem-solving` | `ps-validator` | Verify reproduces audit's iter-9 drift detection |
| 5 | `/adversary` | `adv-executor` + `adv-scorer` | C4 ≥0.95 review |
| 6 | `/worktracker` | `wt-verifier` | Validate AC; close |

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

| ID | Title | Owner | Status |
|----|-------|-------|--------|
| [TASK-101](./TASK-101-author-cli-command-parser.md) | Author CLI command parser (argparse or click) | `eng-backend` | pending |
| [TASK-102](./TASK-102-wire-cli-to-packet-validator.md) | Wire CLI to PacketValidator service | `eng-backend` | pending |
| [TASK-103](./TASK-103-author-report-renderers.md) | Author MarkdownReportRenderer + JsonReportRenderer adapters (infrastructure) | `eng-backend` | pending |
| [TASK-104](./TASK-104-add-cli-shim.md) | Add CLI shim at skills/transcript/scripts/validate_packet.py | `eng-backend` | pending |
| [TASK-105](./TASK-105-cli-tests-via-entrypoint-and-perf.md) | CLI integration tests via entrypoint; performance test ~300ms target | `eng-qa` | pending |
| [TASK-106](./TASK-106-verify-reproduces-audit-iter-9-drift.md) | Verify reproduces audit's iter-9 drift detection | `ps-validator` | pending |
| [TASK-212](./TASK-212-run-adversary-c4-review.md) | Run /adversary C4 review | `adv-executor` | pending |
| [TASK-213](./TASK-213-validate-ac-and-close-story-007.md) | Validate STORY-007 AC and close | `wt-verifier` | pending |

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
