# Deprecated E2E Tests

> **Status:** DEPRECATED
> **Deprecated:** 2026-01-10
> **Reason:** WI-SAO-021 - Orchestration Folder Refactoring
> **Replacement:** See `tests/e2e/v2/` for updated tests with dynamic paths

---

## Why Deprecated

These tests were created using **hardcoded artifact paths** such as:
- `tests/e2e/artifacts/phase-a-output.md`
- `tests/e2e/artifacts/crosspoll/alpha-to-beta.md`

The orchestration skill v2.0 now uses **dynamic path resolution**:
- `orchestration/{workflow_id}/{pipeline_alias}/{phase}/`
- `orchestration/{workflow_id}/cross-pollination/{barrier}/{direction}/`

---

## Deprecated Contents

| Test | Type | Issue |
|------|------|-------|
| TEST-001-LINEAR-WORKFLOW.yaml | Workflow definition | Hardcoded artifact paths |
| TEST-001-EXECUTION-REPORT.md | Execution report | References hardcoded paths |
| TEST-002-PARALLEL-WORKFLOW.yaml | Workflow definition | Hardcoded artifact paths |
| TEST-002-EXECUTION-REPORT.md | Execution report | References hardcoded paths |
| TEST-003-CROSSPOLL-WORKFLOW.yaml | Workflow definition | Hardcoded artifact paths |
| TEST-003-EXECUTION-REPORT.md | Execution report | References hardcoded paths |
| artifacts/ | Test artifacts | Created with hardcoded structure |

---

## Migration Path

To run updated tests:

1. Use tests in `tests/e2e/v2/` directory
2. New tests use dynamic path scheme
3. Workflow ID is generated at runtime
4. Pipeline aliases are configurable

---

## Historical Reference

These tests remain for historical reference and to understand:
- Original test design patterns
- Expected output formats
- Workflow execution validation approach

**DO NOT USE** these tests for validating orchestration skill v2.0.

---

*Deprecated by WI-SAO-021*
*Work Item: Orchestration Folder Refactoring*
