# DISC-009: Duplicate pytest Configuration

> **Discovery ID:** DISC-009
> **Type:** Technical Debt
> **Status:** DOCUMENTED
> **Feature:** [FT-003](./FEATURE-WORKTRACKER.md)
> **Discovered:** 2026-01-13
> **Last Updated:** 2026-01-13

---

## Summary

During EN-004 test execution, pytest emits a warning about ignoring configuration in `pyproject.toml`. Investigation reveals duplicate pytest configuration with conflicting settings.

---

## Evidence

### Warning Message

```
(WARNING: ignoring pytest config in pyproject.toml!)
```

### Configuration Files

**pytest.ini (takes precedence)**
```ini
[pytest]
pythonpath =
testpaths = tests
addopts = --import-mode=importlib
markers =
    happy-path: marks tests as happy path scenarios
    negative: marks tests as negative/error scenarios
    edge-case: marks tests as edge case scenarios
    boundary: marks tests as boundary value scenarios
```

**pyproject.toml (ignored)**
```toml
[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
markers = [
    "happy-path: marks tests as happy path scenarios",
    "negative: marks tests as negative/error scenarios",
    "edge-case: marks tests as edge case scenarios",
    "boundary: marks tests as boundary value scenarios",
]
```

### Key Conflict

| Setting | pytest.ini | pyproject.toml |
|---------|------------|----------------|
| `pythonpath` | (empty) | `["src"]` |
| `addopts` | `--import-mode=importlib` | (none) |

---

## Impact

| Impact | Severity | Description |
|--------|----------|-------------|
| Confusion | LOW | Developers may edit wrong file |
| Import behavior | MEDIUM | pythonpath differences could affect test imports |
| Maintenance | LOW | Two files to maintain |

---

## Recommendations

1. **Consolidate to single source**: Choose either `pytest.ini` OR `pyproject.toml`
2. **Prefer pyproject.toml**: Modern Python convention (PEP 517/518/621)
3. **Verify pythonpath setting**: Determine if `["src"]` is actually needed

### Proposed Resolution

Delete `pytest.ini` and keep `pyproject.toml` with merged settings:

```toml
[tool.pytest.ini_options]
pythonpath = []  # Tests use PYTHONPATH env var, not pytest pythonpath
testpaths = ["tests"]
addopts = "--import-mode=importlib"
markers = [
    "happy-path: marks tests as happy path scenarios",
    "negative: marks tests as negative/error scenarios",
    "edge-case: marks tests as edge case scenarios",
    "boundary: marks tests as boundary value scenarios",
]
```

---

## Related Artifacts

| Type | Location | Description |
|------|----------|-------------|
| pytest.ini | `pytest.ini` | Current active config |
| pyproject.toml | `pyproject.toml` | Ignored pytest config |
| EN-004 | [./en-004.md](./en-004.md) | Where discovery was made |
| DISC-005 | [../../SE-001/FT-002/disc-005.md](../../SE-001/FT-002/disc-005.md) | PYTHONPATH requirement |

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-13 | Created DISC-009 during EN-004 test execution | Claude |
