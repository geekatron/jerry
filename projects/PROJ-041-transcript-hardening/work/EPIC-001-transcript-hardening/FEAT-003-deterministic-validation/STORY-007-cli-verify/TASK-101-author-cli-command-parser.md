# TASK-101: Author CLI command parser (argparse or click)

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** STORY-007
> **Owner:** eng-backend

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

CLI surface: `jerry transcript verify <packet> [--json] [--rule RULE_ID]... [--fail-fast]`. Hexagonal H-07: command in interface/cli.py.

---

## Acceptance Criteria

- [ ] CLI parser exists at src/jerry/transcript/validation/interface/cli.py
- [ ] Supports all flags from CLI surface spec
- [ ] Exit codes match spec (0 PASS, 1 FAIL, 2 invalid, 3 sandbox refusal, 64 usage)
