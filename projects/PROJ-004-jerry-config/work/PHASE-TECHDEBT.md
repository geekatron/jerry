# PHASE-TECHDEBT: Technical Debt

| Field | Value |
|-------|-------|
| **Phase ID** | PHASE-TECHDEBT |
| **Title** | Technical Debt |
| **Status** | ONGOING |
| **Purpose** | Track technical debt incurred during implementation |

---

## Active Technical Debt

| Debt ID | Title | Severity | Phase | Added | Resolved |
|---------|-------|----------|-------|-------|----------|
| TD-001 | TOML write needs tomli-w | LOW | PHASE-02 | 2026-01-12 | - |
| TD-002 | Windows locking needs filelock | MEDIUM | PHASE-02 | 2026-01-12 | - |
| TD-003 | pytest-cov not installed | LOW | PHASE-06 | 2026-01-12 | - |
| TD-004 | Ruff unpinned in CI | HIGH | PHASE-08 | 2026-01-13 | 2026-01-13 |

---

## Technical Debt Details

### TD-001: TOML Write Needs tomli-w

| Field | Value |
|-------|-------|
| **Severity** | LOW |
| **Phase** | PHASE-02 (Architecture & Design) |
| **Added** | 2026-01-12 |
| **Owner** | - |
| **Resolution Target** | Future iteration |

**Description**:
Python's stdlib `tomllib` only supports reading TOML files. To write TOML files (for `jerry config set`), we need the `tomli-w` package.

**Current Workaround**:
For MVP, config writes can output to stdout and user can manually update files. Or use simple key=value format.

**Proper Solution**:
Add `tomli-w` to dependencies in infrastructure layer.

**Risk if Unresolved**:
Users cannot modify config via CLI, must edit files manually.

---

### TD-002: Windows Locking Needs filelock

| Field | Value |
|-------|-------|
| **Severity** | MEDIUM |
| **Phase** | PHASE-02 (Architecture & Design) |
| **Added** | 2026-01-12 |
| **Owner** | - |
| **Resolution Target** | Phase 2 of implementation |

**Description**:
The `fcntl` module is Unix-only. Windows requires `msvcrt` for file locking, or the cross-platform `filelock` library.

**Current Workaround**:
Only support Unix platforms (macOS, Linux) in initial implementation.

**Proper Solution**:
Add `filelock` package to infrastructure layer for cross-platform support.

**Risk if Unresolved**:
Windows users cannot safely use Jerry with multiple processes.

---

### TD-003: pytest-cov Not Installed

| Field | Value |
|-------|-------|
| **Severity** | LOW |
| **Phase** | PHASE-06 (Testing & Validation) |
| **Added** | 2026-01-12 |
| **Owner** | - |
| **Resolution Target** | Future iteration |

**Description**:
The `pytest-cov` package is not installed in the current environment, preventing coverage measurement for AC-018.5.

**Current Workaround**:
Tests pass without coverage measurement. Coverage is not blocking for WI-018 completion.

**Proper Solution**:
Add `pytest-cov` to development dependencies in `pyproject.toml`.

**Risk if Unresolved**:
Cannot automatically enforce coverage thresholds in CI.

---

### TD-004: Ruff Unpinned in CI (RESOLVED)

| Field | Value |
|-------|-------|
| **Severity** | HIGH |
| **Phase** | PHASE-08 (Release Prep) |
| **Added** | 2026-01-13 |
| **Resolved** | 2026-01-13 |
| **Owner** | Claude |
| **Resolution** | Pinned ruff==0.14.11 in CI |

**Description**:
The CI workflow at `.github/workflows/ci.yml` used `pip install ruff` without a version pin. This caused version drift between local development (ruff 0.14.11 via uv) and CI (latest ruff), resulting in formatting check failures even though local checks passed.

**Symptoms**:
- Local `ruff format --check .` passed
- CI `ruff format --check .` failed with "10 files would be reformatted"
- Same code, different results due to version mismatch

**Root Cause**:
Ruff formatting rules changed between versions. Specifically:
- Slice spacing rules differed
- Multi-line expression collapse thresholds differed

**Resolution Applied**:
```yaml
# Changed from:
run: pip install ruff

# Changed to:
run: pip install "ruff==0.14.11"
```

**Commits**:
- `0c6ee80`: Pinned ruff version in CI
- `ac96baa`: Applied consistent formatting to all files

**Lesson Learned**:
All linter/formatter versions in CI must be pinned to match local development environment to ensure deterministic results.

---

## Technical Debt Template

When adding technical debt, use this template:

```markdown
### TD-{NNN}: {Title}

| Field | Value |
|-------|-------|
| **Severity** | CRITICAL / HIGH / MEDIUM / LOW |
| **Phase** | {Phase where debt was incurred} |
| **Added** | {date} |
| **Owner** | {who will resolve} |
| **Resolution Target** | {when it should be resolved} |

**Description**:
{Describe the technical debt}

**Current Workaround**:
{What we're doing instead}

**Proper Solution**:
{What the correct solution should be}

**Risk if Unresolved**:
{Consequences of not addressing this debt}
```

---

## Severity Definitions

| Severity | Definition | Resolution Timeline |
|----------|------------|---------------------|
| CRITICAL | Blocks functionality | Must resolve before release |
| HIGH | Significant limitation | Resolve within 1 iteration |
| MEDIUM | Known limitation | Resolve within 3 iterations |
| LOW | Nice to have | Resolve when convenient |

---

## Technical Debt Statistics

| Metric | Value |
|--------|-------|
| Total Debt Items | 4 |
| Critical | 0 |
| High | 0 (1 resolved) |
| Medium | 1 |
| Low | 2 |
| Resolved | 1 |

---

## Navigation

- **WORKTRACKER**: [../WORKTRACKER.md](../WORKTRACKER.md)
- **Bugs**: [PHASE-BUGS.md](PHASE-BUGS.md)
- **Discoveries**: [PHASE-DISCOVERY.md](PHASE-DISCOVERY.md)
