# EN-005: PreToolUse Staleness Detection

> **Type:** enabler
> **Status:** pending
> **Priority:** medium
> **Impact:** medium
> **Enabler Type:** infrastructure
> **Created:** 2026-02-19
> **Due:** --
> **Completed:** --
> **Parent:** FEAT-001
> **Owner:** --
> **Effort:** 1.5-2.5h

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Technical scope |
| [Acceptance Criteria](#acceptance-criteria) | BDD scenarios and checklist |
| [Dependencies](#dependencies) | Relationships |
| [History](#history) | Status changes |

---

## Summary

Add ORCHESTRATION.yaml `resumption.updated_at` staleness detection to the `jerry hooks pre-tool-use` CLI command handler. When a Write/Edit/MultiEdit targets ORCHESTRATION.yaml, check whether `updated_at` has been updated in the current phase. If stale, inject a staleness warning into the enforcement response.

**Staleness Logic:**
1. Parse tool call target path from stdin JSON
2. If path does not match `ORCHESTRATION.yaml`: passthrough
3. If matches: read `resumption.updated_at`
4. Compare against current phase start timestamp
5. If stale: inject warning into enforcement response
6. Fail-open: if ORCHESTRATION.yaml unparseable, passthrough

---

## Acceptance Criteria

### BDD Scenarios (pytest-bdd)

```gherkin
Feature: ORCHESTRATION.yaml staleness detection on pre-tool-use

  Scenario: Non-ORCHESTRATION.yaml tool call passes through
    Given a pre-tool-use payload targeting "src/context_monitoring/domain/value_objects/threshold_tier.py"
    When staleness detection runs
    Then no staleness warning should be emitted

  Scenario: Stale ORCHESTRATION.yaml triggers warning
    Given a pre-tool-use payload targeting "projects/PROJ-004/ORCHESTRATION.yaml"
    And resumption.updated_at is "2026-02-18T10:00:00Z"
    And the current phase started at "2026-02-19T08:00:00Z"
    When staleness detection runs
    Then a staleness warning should be injected into the response

  Scenario: Fresh ORCHESTRATION.yaml passes through
    Given a pre-tool-use payload targeting "ORCHESTRATION.yaml"
    And resumption.updated_at is "2026-02-19T09:30:00Z"
    And the current phase started at "2026-02-19T08:00:00Z"
    When staleness detection runs
    Then no staleness warning should be emitted

  Scenario: Unparseable ORCHESTRATION.yaml is fail-open
    Given a pre-tool-use payload targeting "ORCHESTRATION.yaml"
    And the ORCHESTRATION.yaml file contains invalid YAML
    When staleness detection runs
    Then no staleness warning should be emitted
    And no exception should propagate
```

### Acceptance Checklist

- [ ] Staleness detection logic in `src/context_monitoring/` (appropriate layer)
- [ ] Correct passthrough for non-ORCHESTRATION.yaml tool calls
- [ ] Correct staleness detection when `updated_at` predates current phase
- [ ] Warning format consistent with `PreToolEnforcementEngine` output
- [ ] Fail-open on YAML parse errors
- [ ] Unit tests: path matching, staleness calculation, passthrough, fail-open
- [ ] Integration with `jerry hooks pre-tool-use` handler (EN-006) verified

---

## Dependencies

**Depends On:**
- ST-001 (update protocol defines when updated_at changes)
- EN-006 (pre-tool-use CLI command exists)

**Enables:** Nothing directly

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-19 | Claude | pending | Enabler created from CWI-07. Redesigned from PostToolUse to PreToolUse. |
