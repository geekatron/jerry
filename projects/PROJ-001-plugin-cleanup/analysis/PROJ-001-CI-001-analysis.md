# CI/CD Implementation Analysis

> **Document ID**: PROJ-001-CI-001-analysis
> **PS ID**: PROJ-001
> **Entry ID**: CI-001.A
> **Date**: 2026-01-10
> **Author**: ps-analyst agent v2.0.0 (Claude Opus 4.5)
> **Source**: `research/PROJ-001-CI-001-research.md`

---

## Analysis Summary

This document analyzes the research findings for CI/CD implementation and maps them to Jerry's specific requirements.

---

## Gap Analysis: Research vs. Jerry Requirements

### Current State

| Component | Current | Required | Gap |
|-----------|---------|----------|-----|
| Pre-commit hooks | None | Full pipeline | **MISSING** |
| GitHub Actions | None | CI workflow | **MISSING** |
| Linting | Configured (ruff) | Pre-commit + GHA | Needs integration |
| Type checking | Configured (pyright) | Pre-commit + GHA | Needs integration |
| Test suite | 1330 tests exist | Run on commit + push | Needs automation |
| Coverage | pytest-cov installed | Reports on PRs | Needs workflow |

### Jerry-Specific Requirements

Based on the research and Jerry's architecture:

| Requirement | Research Finding | Jerry Application |
|-------------|------------------|-------------------|
| Python version | 3.11-3.14 matrix | Jerry uses 3.14 (latest) |
| Test framework | pytest | Already using pytest |
| Linter | ruff | Already configured in pyproject.toml |
| Type checker | pyright | Already configured in pyproject.toml |
| Hook framework | pre-commit | Needs installation |
| CI platform | GitHub Actions | Needs workflow files |

---

## Configuration Decisions Required

### Decision 1: Pre-commit Test Execution Stage

**Question**: Should the full test suite run on `pre-commit` or `pre-push`?

| Option | Pros | Cons |
|--------|------|------|
| **pre-commit** (default) | Maximum protection, catches all issues | Slower commits (~30s for 1330 tests) |
| pre-push | Faster commits | Issues caught later, may have multiple bad commits |

**Recommendation**: `pre-commit` with documented override for fast iteration.

### Decision 2: Python Version Matrix

**Question**: Which Python versions should be tested in GitHub Actions?

| Option | Rationale |
|--------|-----------|
| 3.11 only | Minimum supported |
| 3.11-3.14 | Full compatibility matrix |
| **3.14 only** | Jerry's target version, faster CI |

**Recommendation**: Start with 3.14 only (faster), expand if compatibility issues arise.

### Decision 3: Coverage Threshold

**Question**: Should CI fail if coverage drops below a threshold?

| Option | Value | Rationale |
|--------|-------|-----------|
| No threshold | - | Flexibility, no false failures |
| **80%** | Recommended | Industry standard, enforces quality |
| 90% | WORKTRACKER goal | Aspirational, may cause friction |

**Recommendation**: 80% threshold, configurable for increase over time.

### Decision 4: PR Status Checks

**Question**: Which checks should be required for PR merge?

| Check | Required | Rationale |
|-------|----------|-----------|
| Lint | Yes | Fast, catches obvious issues |
| Type check | Yes | Catches type errors |
| Tests | Yes | Prevents regressions |
| Coverage | No (reporting only) | Avoid blocking on coverage dips |

**Recommendation**: Lint + Type + Tests required; Coverage as informational.

---

## Jerry-Specific Adaptations

### Adaptation 1: Virtual Environment Path

Research examples use system Python. Jerry uses `.venv/`:

```yaml
# Jerry-specific pre-commit hook entry
entry: .venv/bin/python -m pytest
```

### Adaptation 2: pytest.ini Already Exists

Jerry already has `pytest.ini` with:
- `pythonpath = src`
- `testpaths = tests`
- `addopts = --import-mode=importlib`

No changes needed - configuration is compatible.

### Adaptation 3: pyproject.toml Integration

Jerry already has ruff and pyright configured. Pre-commit hooks should use these configs:

```yaml
args: [--config=pyproject.toml]
```

### Adaptation 4: Source Directory

Jerry uses `src/` layout. Coverage and type checking should target `src/`:

```yaml
pytest --cov=src
pyright src/
```

---

## Risk Analysis

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Slow commits frustrate developers | Medium | High | Document fast-mode, make configurable |
| Flaky tests block CI | Low | High | Mark known slow tests, add retries |
| Pre-commit bypass | Medium | Medium | GHA catches bypasses |
| Configuration drift | Low | Medium | Single source of truth in pyproject.toml |

---

## Implementation Checklist

Based on analysis, the implementation should:

- [ ] Create `.pre-commit-config.yaml` with:
  - [ ] Standard hooks (whitespace, YAML, merge conflict)
  - [ ] Ruff check + format
  - [ ] Pyright type checking (local hook)
  - [ ] Pytest (local hook, configurable stage)
- [ ] Create `.github/workflows/ci.yml` with:
  - [ ] Lint job (ruff)
  - [ ] Type-check job (pyright)
  - [ ] Test job (pytest + coverage)
  - [ ] Coverage comment on PRs
- [ ] Update documentation with:
  - [ ] Installation instructions
  - [ ] Fast-mode configuration
  - [ ] Bypass instructions for emergency

---

## Recommendations for ADR

The ADR should capture these decisions:

1. **Context**: No CI/CD exists; 1330 tests run manually
2. **Decision**: Layered approach (pre-commit + GitHub Actions)
3. **Consequences**:
   - Slower commits (configurable)
   - Zero-regression guarantee
   - Clean PR status checks
4. **Trade-offs accepted**:
   - Commit time vs. safety (chose safety)
   - Single Python version vs. matrix (chose single for speed)

---

## PS Integration

```yaml
analyst_output:
  ps_id: "PROJ-001"
  entry_id: "CI-001.A"
  artifact_path: "projects/PROJ-001-plugin-cleanup/analysis/PROJ-001-CI-001-analysis.md"
  summary: "CI/CD analysis complete - 4 decisions required, Jerry-specific adaptations identified"
  gaps_identified: 4
  confidence: "high"
  next_agent_hint: "Create ADR-CI-001 to formalize decisions"
```

---

## Document History

| Date | Author | Changes |
|------|--------|---------|
| 2026-01-10 | Claude Opus 4.5 | Initial analysis document |
