# TASK-007: Add monitoring_ok Field to FillEstimate

> **Type:** task
> **Status:** done
> **Priority:** medium
> **Parent:** FEAT-001-context-detection

## Document Sections

| Section | Purpose |
|---------|---------|
| [Description](#description) | What this task addresses |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Context](#context) | Why this was deferred from TASK-006 |
| [History](#history) | Status changes |

---

## Description

Add a `monitoring_ok: bool = True` field to `FillEstimate` to distinguish
genuine NOMINAL readings from fail-open/disabled states. Currently the
`_FAIL_OPEN_ESTIMATE` sentinel is identical to a legitimate NOMINAL result,
which could suppress checkpoint behavior in production.

### Problem

When `estimate()` catches an exception or monitoring is disabled, it returns
`_FAIL_OPEN_ESTIMATE` with `tier=NOMINAL, fill=0.0, token_count=None`. This
is indistinguishable from a genuine healthy context reading at 0% fill.
Consumers (hooks, CLI) cannot tell if monitoring is working or broken.

### Solution

1. Add `monitoring_ok: bool = True` to `FillEstimate` dataclass
2. Set `monitoring_ok=False` on `_FAIL_OPEN_ESTIMATE` sentinel
3. Include `<monitoring-ok>` element in XML `<context-monitor>` tag
4. Update hooks to optionally log when `monitoring_ok=False`

---

## Acceptance Criteria

- [x] `FillEstimate.monitoring_ok` field exists with default `True`
- [x] `_FAIL_OPEN_ESTIMATE` has `monitoring_ok=False`
- [x] XML output includes `<monitoring-ok>` element
- [x] Unit tests distinguish genuine NOMINAL from fail-open NOMINAL
- [x] All existing tests continue to pass (backward-compatible default)

---

## Context

This task was identified during TASK-006 C4 adversarial review:
- **S-001 Red Team AV-004**: Fail-open abuse — deleted transcript returns NOMINAL indistinguishable from genuine healthy state
- **S-002 Devil's Advocate Challenge 2 (STRONG)**: Fail-open indistinguishable from NOMINAL
- **S-014 GAP-1**: Deferral requires formal tracking artifact

TOCTOU trade-off between `get_context_window_tokens()` and
`get_context_window_source()` is also documented here. See
`_detect_context_window()` docstring in `config_threshold_adapter.py`.

---

## History

| Date       | Status  | Notes                                    |
|------------|---------|------------------------------------------|
| 2026-02-20 | Created | Deferred from TASK-006 C4 adversarial review |
| 2026-02-20 | Done    | Implemented: field on FillEstimate, sentinel, XML tag, 9 tests |
