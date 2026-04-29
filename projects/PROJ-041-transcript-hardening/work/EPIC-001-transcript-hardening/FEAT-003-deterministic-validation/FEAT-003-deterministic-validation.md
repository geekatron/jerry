# FEAT-003: Deterministic Substrate Validation

<!--
TEMPLATE: Feature
PURPOSE: Replace LLM-judged ADR-007 §4 compliance with runnable validators wired into the ts-formatter write pipeline. The non-negotiable spirit of this Epic.
-->

> **Type:** feature
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Created:** 2026-04-28T00:00:00Z
> **Due:**
> **Completed:**
> **Parent:** EPIC-001
> **Owner:** adam.nowak

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this Feature delivers |
| [Bounded Context Design](#bounded-context-design) | Validation as operation within /transcript BC |
| [Children Stories/Enablers](#children-storiesenablers) | Decomposition |
| [Acceptance Criteria](#acceptance-criteria) | Feature-level acceptance |
| [Progress Summary](#progress-summary) | Overall progress |
| [Dependencies](#dependencies) | Inputs and downstream blocks |
| [Related Items](#related-items) | Hierarchy and references |
| [History](#history) | Status changes |

---

## Summary

ADR-007 §4 specifies 17 validation rule IDs (`FILE-001..003`, `CONTENT-001..003`, `ANCHOR-001..003`, `SCHEMA-001..008`). **No script implementation exists.** `ps-critic` relies on LLM interpretation, which is exactly what ADR-007 was authored to eliminate.

The author's external audit demonstrated that the convergent findings each `/adversary` iteration produced ("audit_breakdown arithmetic doesn't reconcile," "ASR convention applied inconsistently across narrative fields," "per-bucket link counts don't grep-reproduce") are **mechanically checkable** by walking the packet and comparing declared values to recounted values — no LLM judgment needed. The author shipped a working ~200-line stdlib Python prototype (gist linked in #273 comment 1) that catches in ~300ms what manual adversary review took 30 minutes to find — a 6,000× speedup that only matters because the substrate is invisibly machine-verifiable but currently treated as hand-maintained.

This Feature implements the validators, the CLI subcommands (`jerry transcript verify`, `jerry transcript update-anchors`), and the integration into the `ts-formatter` write pipeline, following DDD discipline + TDD Red/Green/Refactor.

---

## Bounded Context Design

Per user direction: **Skill is the bounded context, validation is an operation within `/transcript`.**

```
src/jerry/transcript/                        # /transcript bounded context
  ├── parsing/         (existing — VTT/SRT ingestion)
  ├── extraction/      (existing — speakers/topics/decisions)
  ├── formatting/      (existing — ts-formatter Markdown rendering)
  └── validation/      (NEW — operation we're adding)
       ├── domain/         (Packet, ValidationRule, ValidationResult — entities; RuleId VO)
       ├── application/    (PacketValidator service, RuleEngine port)
       ├── infrastructure/ (SubprocessSandbox adapter, FileReader adapter, JsonSchemaAdapter)
       └── interface/      (CLI: jerry transcript verify | update-anchors)

skills/transcript/scripts/                    # thin CLI shims importing from src/jerry/transcript/validation/
tests/transcript/validation/                  # TDD R/G/R, parameterized over test_data/ golden packets
```

Hexagonal architecture isolation per H-07: domain layer has no infra/interface imports; composition root only in `interface/` and tests.

---

## Children Stories/Enablers

| ID | Type | Title | Status | Priority |
|----|------|-------|--------|----------|
| EN-001 | Enabler | DDD scaffolding for transcript/validation operation | pending | high |
| EN-002 | Enabler | Test harness + golden packets in test_data/ | pending | high |
| EN-003 | Enabler | SubprocessSandbox port + adapter (security boundary) | pending | high |
| STORY-003 | Story | Implement FILE-001..003 validators | pending | high |
| STORY-004 | Story | Implement CONTENT-001..003 validators | pending | high |
| STORY-005 | Story | Implement ANCHOR-001..003 validators | pending | high |
| STORY-006 | Story | Implement SCHEMA-001..008 validators | pending | high |
| STORY-007 | Story | jerry transcript verify CLI subcommand | pending | high |
| STORY-008 | Story | jerry transcript update-anchors CLI subcommand | pending | high |
| STORY-009 | Story | Wire verify into ts-formatter post-render hook | pending | high |
| STORY-010 | Story | Wire update-anchors into ts-formatter write pipeline | pending | high |
| STORY-011 | Story | Update ts-critic-extension.md to consume validator output | pending | medium |
| STORY-012 | Story | CI workflow runs validators against golden packets | pending | high |

### Work Item Links

- Enablers: EN-001..EN-003 (subdirectories below)
- Stories: STORY-003..STORY-012 (subdirectories below)

---

## Progress Summary

```
Enablers: [....................]  0% (0/3 completed)
Stories:  [....................]  0% (0/10 completed)
Overall:  [....................]  0%
```

---

## Acceptance Criteria

- [ ] All 17 ADR-007 §4 rule IDs implemented as runnable, deterministic checks (return `(rule_id, severity, pass|fail, evidence)`).
- [ ] Validator runs against golden packets in `test_data/expected_output/` with structured JSON + Markdown report output and exit code 0/1.
- [ ] `jerry transcript verify <packet>` and `jerry transcript update-anchors <packet>` CLI subcommands exist, follow hexagonal architecture (H-07), and are tested via CLI entry point.
- [ ] `ts-formatter` post-render hook runs `verify` before reporting completion (catches regressions at agent exit, not 30 min later).
- [ ] `ts-formatter` write pipeline runs `update-anchors`; declared counts in `_anchors.json.audit_breakdown` are cache-of-walked-truth, never hand-maintained.
- [ ] `ts-critic-extension.md` references deterministic validator output as pre-LLM signal.
- [ ] CI workflow runs validators against golden packets on every PR.
- [ ] Test coverage ≥90% on `validation/` module per H-20.
- [ ] `/red-team` exit-criteria met for new subprocess execution surface (EN-003 closure).
- [ ] `/adversary` C4 ≥0.95 phase gate at Feature acceptance.

---

## Dependencies

| Type | Item | Description |
|------|------|-------------|
| Blocked By | FEAT-001 | ADR-007 must be readable + ACCEPTED before validators implement its rules |
| Blocked By | FEAT-002 | Rules must not contradict each other before validators encode them |
| Blocked By | EN-004 | Threat model on subprocess surface informs EN-003 SubprocessSandbox design |
| Blocks | EN-008 | Final tournament cannot pass without deterministic validation in place |

---

## Related Items

### Hierarchy

- **Parent Epic:** [EPIC-001](../EPIC-001-transcript-hardening.md)

### External

- Source: [#273 §C5](https://github.com/geekatron/jerry/issues/273) + [comment 1](https://github.com/geekatron/jerry/issues/273#issuecomment-4339264545)
- Author's prototype: https://gist.github.com/anowak-delinea/f6748192a6e32bb65c874cd0e5dde924

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-04-28 | adam.nowak (via Claude scaffold) | pending | Feature created. DDD bounded-context design captured. 3 Enablers + 10 Stories scaffolded. |
