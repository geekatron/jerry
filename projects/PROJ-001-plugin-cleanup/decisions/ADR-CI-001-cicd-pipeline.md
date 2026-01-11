# ADR-CI-001: CI/CD Pipeline Architecture

> **Status**: PROPOSED
> **Date**: 2026-01-10
> **Deciders**: User, Claude Opus 4.5
> **Sources**:
> - `research/PROJ-001-CI-001-research.md`
> - `analysis/PROJ-001-CI-001-analysis.md`

---

## Context

The Jerry framework has accumulated 1330 tests across multiple domains (session management, work tracking, project validation). Currently:

- **No CI/CD pipeline exists** - tests run only when manually invoked
- **No pre-commit hooks** - code quality issues caught late
- **No GitHub Actions** - no automated validation on push/PR
- **Risk of regressions** - changes may break existing functionality undetected

The WORKTRACKER enforces principle **P-REGRESS** (Zero regressions) which requires automated test execution to guarantee.

---

## Decision

We will implement a **layered CI/CD pipeline** with two components:

### Layer 1: Pre-commit Hooks (Local)

**What**: Pre-commit framework running ruff, pyright, and pytest before commits.

**Configuration**:
```yaml
# Default behavior: Full test suite on commit
stages: [pre-commit]

# Configurable: Add to .git/hooks/pre-commit.legacy for fast mode
# Or: SKIP=pytest git commit -m "message"
```

### Layer 2: GitHub Actions (Remote)

**What**: CI workflow running on all pushes and PRs to main branches.

**Triggers**:
- All pushes to any branch
- All pull requests to `main`, `master`, `claude/*`

**Jobs**:
1. **Lint** - ruff check + format verification
2. **Type-check** - pyright static analysis
3. **Test** - pytest with coverage (Python 3.14)
4. **Coverage** - PR comment with coverage report

---

## Decisions Made

### D1: Test Stage = pre-commit (not pre-push)

**Decision**: Run full test suite on commit, not push.

**Rationale**: P-REGRESS requires zero regressions. Running on commit catches issues immediately, preventing even a single bad commit.

**Trade-off accepted**: Commits take ~30 seconds. Documented escape hatch: `SKIP=pytest git commit`.

### D2: Python Version = 3.14 only (no matrix)

**Decision**: Test only Python 3.14 in GitHub Actions.

**Rationale**: Jerry targets 3.14. Matrix testing adds CI time without current benefit. Can expand if compatibility issues arise.

**Trade-off accepted**: Won't catch 3.11/3.12/3.13 compatibility issues automatically.

### D3: Coverage Threshold = 80% (soft)

**Decision**: Report coverage but don't fail CI on threshold.

**Rationale**: Avoid blocking PRs on coverage dips during refactoring. Coverage is informational, not a gate.

**Trade-off accepted**: Coverage may drift downward without enforcement.

### D4: Required PR Checks = Lint + Type + Test

**Decision**: PRs must pass lint, type-check, and test jobs to merge.

**Rationale**: These are the minimum quality gates. Coverage is not required (per D3).

---

## Consequences

### Positive
- **P-REGRESS enforced** - Every commit validated against 1330 tests
- **Clean PR workflow** - Status checks prevent broken merges
- **Developer feedback** - Issues caught immediately, not in review
- **Coverage visibility** - PR comments show coverage impact

### Negative
- **Slower commits** - ~30 seconds per commit (mitigated by SKIP option)
- **Initial setup** - Developers must run `pre-commit install`
- **CI cost** - GitHub Actions minutes consumed on every push

### Neutral
- **Configuration complexity** - Offset by single-source pyproject.toml
- **Tool upgrades** - Hook versions pinned, require manual updates

---

## Implementation

### Files to Create

1. **`.pre-commit-config.yaml`** - Pre-commit hook configuration
2. **`.github/workflows/ci.yml`** - GitHub Actions workflow
3. **`docs/contributing/ci.md`** (optional) - Developer documentation

### Developer Workflow

```bash
# One-time setup
pip install pre-commit
pre-commit install

# Normal workflow (hooks run automatically)
git add .
git commit -m "feat: add feature"  # Hooks run here

# Emergency bypass (use sparingly)
SKIP=pytest git commit -m "wip: work in progress"
# OR
git commit --no-verify -m "emergency fix"

# Run all hooks manually
pre-commit run --all-files
```

---

## Alternatives Considered

### Alternative 1: CI Only (no pre-commit)

**Rejected because**: Catches issues too late. Multiple bad commits accumulate before CI feedback.

### Alternative 2: Pre-push instead of pre-commit

**Rejected because**: P-REGRESS requires zero bad commits. Pre-push allows bad commits to exist locally.

### Alternative 3: Fast tests on commit, full on push

**Rejected because**: Complexity of maintaining test markers. Full suite is only ~30s.

---

## Review Checklist

Before accepting this ADR:

- [ ] User agrees with test-on-commit default
- [ ] User agrees with Python 3.14 only (no matrix)
- [ ] User agrees with 80% coverage threshold (non-blocking)
- [ ] User agrees with Lint + Type + Test as required checks

---

## Document History

| Date | Author | Changes |
|------|--------|---------|
| 2026-01-10 | Claude Opus 4.5 | Initial ADR proposal |
