# TD-002: CI Test Coverage Gap

> **Technical Debt ID:** TD-002
> **Feature:** FT-002-plugin-loading-fix
> **Project:** PROJ-007-jerry-bugs
> **Status:** DOCUMENTED
> **Priority:** Medium
> **Created:** 2026-01-14
> **Target Version:** v0.3.0+

---

## Summary

The CI pipeline tests plugin hook execution differently than how hooks actually run in production. This creates a gap where CI passes but actual hooks fail.

---

## Evidence

| Source | Finding |
|--------|---------|
| `.github/workflows/ci.yml:126` | CI uses `PYTHONPATH="."` with relative paths |
| `hooks/hooks.json:10` | Hooks use `PYTHONPATH="${CLAUDE_PLUGIN_ROOT}"` with absolute paths |
| disc-002 | Documented discrepancy in detail |

---

## Root Cause

**CI Environment:**
```bash
PYTHONPATH="." uv run src/interface/cli/session_start.py
```
- Runs from repository root
- Uses relative path "."
- Working directory is repo root

**Production Hook Environment:**
```bash
PYTHONPATH="${CLAUDE_PLUGIN_ROOT}" uv run ${CLAUDE_PLUGIN_ROOT}/src/interface/cli/session_start.py
```
- Runs from arbitrary directory (wherever Claude is launched)
- Uses absolute paths
- Working directory is NOT repo root

---

## Impact

- **CI passes but hooks fail in production**
- Regressions can be introduced without detection
- False confidence in test coverage

---

## Proposed Fix

Create a CI test that mimics the actual hook execution environment:

```yaml
- name: Test hook from non-root directory
  run: |
    cd /tmp
    PYTHONPATH="${GITHUB_WORKSPACE}" uv run ${GITHUB_WORKSPACE}/src/interface/cli/session_start.py
```

---

## Work Items

| Type | ID | Description | Version |
|------|-----|-------------|---------|
| UoW | UoW-002 | Fix CI test coverage gap | v0.3.0+ |

---

## Related Artifacts

| Type | Reference |
|------|-----------|
| Discovery | disc-002 (CI vs Hook Environment Discrepancy) |
| CI Config | `.github/workflows/ci.yml` |
| Hook Config | `hooks/hooks.json` |

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-14 | TD-002 created from disc-002 findings | Claude |
