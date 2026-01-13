# DISC-008: Test Execution Must Use uv, Not python3

> **Discovery ID:** DISC-008
> **Type:** Discovery (Process/Behavioral)
> **Status:** REQUIRES ACTION
> **Feature:** [FT-003](./FEATURE-WORKTRACKER.md)
> **Discovered:** 2026-01-13
> **Last Updated:** 2026-01-13

---

## Summary

During EN-004 Task 1, there was an attempt to run tests using `python3 -m pytest` instead of `uv run pytest`. This violates the core principle of SE-002 - validating the `uv run` execution model.

---

## Incident

### What Happened

```bash
# WRONG - Attempted command
python3 -m pytest tests/session_management/e2e/test_session_start.py

# CORRECT - Should have used
uv run pytest tests/session_management/e2e/test_session_start.py
```

### Why It Matters

1. **Purpose of SE-002**: Validate plugin works without `pip install -e .`
2. **uv run**: Manages dependencies via PEP 723 inline metadata
3. **python3 direct**: Bypasses dependency management, may use pip-installed packages
4. **Test validity**: Tests must run in same environment as production (uv)

---

## Root Cause

- Habit/muscle memory defaulting to `python3`
- No enforcement mechanism to prevent direct python execution
- Test infrastructure doesn't validate execution method

---

## Impact

| Impact | Severity | Description |
|--------|----------|-------------|
| False positives | HIGH | Tests could pass with python3 but fail with uv |
| False negatives | HIGH | Tests could fail with python3 but pass with uv |
| Incorrect validation | HIGH | Defeats purpose of SE-002 testing |

---

## Recommendations

### Immediate (EN-004)

1. Always use `uv run pytest` for test execution
2. Document in test file headers that tests must run via uv

### Future (EN-005)

1. **CI enforcement**: CI workflow must use `uv run pytest`
2. **Pre-commit hook**: Warn if pytest is invoked without uv
3. **Documentation**: Update CONTRIBUTING.md with test execution requirements

### Test File Header Addition

```python
"""
IMPORTANT: Tests must be run via uv to validate plugin execution model.

    uv run pytest tests/session_management/e2e/test_session_start.py

Do NOT use: python -m pytest (bypasses uv dependency management)
"""
```

---

## Action Items

| Action | Owner | Status |
|--------|-------|--------|
| Always use `uv run pytest` going forward | Claude | IN PROGRESS |
| Add header comment to test file | EN-004 | PENDING |
| Add CI enforcement | EN-005 | PENDING |

---

## Related Artifacts

| Type | Location | Description |
|------|----------|-------------|
| EN-004 | [./en-004.md](./en-004.md) | Test fix enabler |
| EN-005 | [./en-005.md](./en-005.md) | CI/pre-commit hooks |
| ADR e-010 | [../../../decisions/PROJ-005-e-010-adr-uv-session-start.md](../../../decisions/PROJ-005-e-010-adr-uv-session-start.md) | uv decision |

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-13 | Created DISC-008 after catching python3 vs uv mistake | Claude |
