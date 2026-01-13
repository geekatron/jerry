# FEATURE-WORKTRACKER: FT-003 SessionStart & CLI Integration Testing

> **Feature ID:** FT-003
> **Name:** SessionStart & CLI Integration Testing Infrastructure
> **Status:** IN PROGRESS
> **Parent:** [SE-002](../SOLUTION-WORKTRACKER.md)
> **Created:** 2026-01-13
> **Last Updated:** 2026-01-13

---

## Overview

This feature establishes comprehensive testing and validation infrastructure to prevent regressions in the plugin's SessionStart hook and CLI integration.

### Problem Statement

BUG-007 (SessionStart hook silent failure) was only discovered manually after deployment because:
1. No unit tests verified script execution
2. No integration tests validated CLI commands
3. No CI checks enforced standalone execution
4. No documentation guided detection/prevention

### Success Criteria

- [ ] Unit tests cover all 3 SessionStart output tag types (`<project-context>`, `<project-required>`, `<project-error>`)
- [ ] Tests verify script executes without `pip install -e .`
- [ ] Pre-commit hook validates plugin.json and hooks.json
- [ ] CI pipeline includes plugin integration tests
- [ ] Playbook documents regression detection/prevention/mitigation

---

## Enablers

| ID | Name | Status | Tasks | Description |
|----|------|--------|-------|-------------|
| [EN-004](./en-004.md) | Automated tests for session_start.py | PENDING | 0/? | Unit tests for all output scenarios |
| [EN-005](./en-005.md) | Pre-commit/CI hooks | PENDING | 0/? | Validation hooks for plugin artifacts |
| [EN-006](./en-006.md) | CLI integration test suite | PENDING | 0/? | Integration tests for jerry CLI |

---

## Units of Work

| ID | Name | Status | Tasks | Description |
|----|------|--------|-------|-------------|
| [WI-001](./wi-001.md) | Detection/prevention/mitigation playbook | PENDING | 0/? | Operational runbook for regression handling |

---

## Technical Debt Registry

| ID | Description | Status | Addressed By |
|----|-------------|--------|--------------|
| TD-001 | No automated tests for plugin hooks | OPEN | EN-004 |
| TD-002 | No CI validation of standalone execution | OPEN | EN-005 |
| TD-003 | No documented regression prevention | OPEN | WI-001 |

---

## Testing Strategy

### Test Pyramid for FT-003

```
                 ┌─────────────┐
                 │    E2E      │ ← Full plugin install + hook exec
                ┌┴─────────────┴┐
                │  Integration  │ ← CLI commands, hook output
               ┌┴───────────────┴┐
               │      Unit       │ ← session_start.py scenarios
               └─────────────────┘
```

### Coverage Targets

| Component | Target | Method |
|-----------|--------|--------|
| session_start.py | 100% | Unit tests (EN-004) |
| CLI commands | 80% | Integration tests (EN-006) |
| Plugin manifest | 100% | Pre-commit validation (EN-005) |

---

## Related Artifacts

| Type | Location | Description |
|------|----------|-------------|
| BUG-007 | [../SE-001/FT-002/bug-007.md](../SE-001/FT-002/bug-007.md) | Root cause analysis |
| ADR e-010 | [../../decisions/PROJ-005-e-010-adr-uv-session-start.md](../../decisions/PROJ-005-e-010-adr-uv-session-start.md) | Decision record |

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-13 | Created FT-003 for testing infrastructure | Claude |
| 2026-01-13 | Added EN-004, EN-005, EN-006, WI-001 | Claude |
