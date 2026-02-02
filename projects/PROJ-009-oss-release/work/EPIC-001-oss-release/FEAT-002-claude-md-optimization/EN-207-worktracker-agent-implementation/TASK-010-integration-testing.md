# TASK-010: Integration Testing

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-02-02T18:30:00Z
> **Parent:** EN-207
> **Owner:** -
> **Effort:** 2

---

## Summary

Execute integration tests to validate the worktracker agents work correctly in real scenarios. Test scenarios from synthesis document (VER-001 through AUD-005, INT-001 through INT-003).

## Acceptance Criteria

- [ ] VER-001 through VER-005 (wt-verifier scenarios) tested
- [ ] VIS-001 through VIS-005 (wt-visualizer scenarios) tested
- [ ] AUD-001 through AUD-005 (wt-auditor scenarios) tested
- [ ] INT-001 through INT-003 (integration scenarios) tested
- [ ] All 18 test scenarios documented in test report

## Test Scenarios

### wt-verifier Tests

| ID | Scenario | Pass Criteria |
|----|----------|---------------|
| VER-001 | Valid complete enabler | `passed: true`, all criteria checked |
| VER-002 | Incomplete enabler | `passed: false`, missing evidence listed |
| VER-003 | Missing acceptance criteria | Graceful failure, clear error message |
| VER-004 | Invalid file path | `error: file_not_found`, path echoed |
| VER-005 | Parent rollup verification | Child status aggregation correct |

### wt-visualizer Tests

| ID | Scenario | Pass Criteria |
|----|----------|---------------|
| VIS-001 | Feature hierarchy | Valid flowchart syntax, all enablers included |
| VIS-002 | Epic timeline | Valid gantt syntax, dates correct |
| VIS-003 | Status diagram | Valid stateDiagram-v2 syntax |
| VIS-004 | Deep hierarchy | Warning if truncated, depth honored |
| VIS-005 | Empty project | Graceful handling, "No work items" note |

### wt-auditor Tests

| ID | Scenario | Pass Criteria |
|----|----------|---------------|
| AUD-001 | Clean project | `passed: true`, zero errors |
| AUD-002 | Template violation | `passed: false`, template check failed |
| AUD-003 | Broken relationship | Orphan detected, parent suggested |
| AUD-004 | ID format violation | ID format error, correction suggested |
| AUD-005 | Full audit | All checks run, coverage > 95% |

### Integration Tests

| ID | Scenario | Agents Involved | Pass Criteria |
|----|----------|-----------------|---------------|
| INT-001 | Pre-closure workflow | wt-verifier -> MAIN | Block if failed, allow if passed |
| INT-002 | Status dashboard | wt-visualizer + wt-auditor | Combined reports generated |
| INT-003 | New contributor onboarding | wt-visualizer | Hierarchy diagram aids comprehension |

## Evidence

- Test report to be created at `EN-207-worktracker-agent-implementation/test-report.md`

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-02T18:30:00Z | pending | Task created |
