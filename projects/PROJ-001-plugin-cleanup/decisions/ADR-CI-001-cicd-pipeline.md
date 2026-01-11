# ADR-CI-001: CI/CD Pipeline Architecture

> **Status**: ACCEPTED
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

### D2: Python Version = 3.11-3.14 matrix

**Decision**: Test Python 3.11, 3.12, 3.13, and 3.14 in GitHub Actions.

**Rationale**: Jerry will be released for others to use. Matrix testing provides visibility into portability issues across Python versions.

**Trade-off accepted**: Slower CI (~4x parallel jobs) in exchange for compatibility assurance.

### D3: Coverage Threshold = 80% (blocking with escape hatch)

**Decision**: Fail CI if coverage drops below 80%. Provide escape hatch for refactoring.

**Rationale**: Quality enforcement requires teeth. 80% is industry standard minimum.

**Escape hatch**: For large refactoring PRs, add `[skip-coverage]` to commit message or use workflow dispatch to bypass.

**Trade-off accepted**: May block PRs during legitimate refactoring (mitigated by escape hatch).

### D4: Required PR Checks = Lint + Type + Test

**Decision**: PRs must pass lint, type-check, and test jobs to merge.

**Rationale**: These are the minimum quality gates. Coverage is not required (per D3).

---

## Consequences

### Positive
- **P-REGRESS enforced** - Every commit validated against 1330 tests
- **Clean PR workflow** - Status checks prevent broken merges
- **Developer feedback** - Issues caught immediately, not in review
- **Coverage enforced** - 80% minimum prevents quality drift
- **Portability assured** - Matrix testing catches Python version issues

### Negative
- **Slower commits** - ~30 seconds per commit (mitigated by SKIP option)
- **Slower CI** - 4x parallel jobs for Python matrix
- **Initial setup** - Developers must run `pre-commit install`
- **CI cost** - More GitHub Actions minutes consumed

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

**Considered but configurable**: Test stage is configurable. Default is full suite on commit, but developers can configure for fast tests when needed.

### Alternative 4: Single Python version (3.14 only)

**Rejected because**: Jerry will be released publicly. Matrix testing essential for portability assurance across Python 3.11-3.14.

### Alternative 5: Coverage as informational only

**Rejected because**: Quality enforcement requires teeth. Soft thresholds lead to drift. Escape hatch provided for legitimate refactoring scenarios.

---

## Review Checklist

User feedback incorporated (2026-01-10):

- [x] D1: Test-on-commit approved (configurable for fast tests)
- [x] D2: Python matrix 3.11-3.14 (changed from 3.14 only)
- [x] D3: Coverage blocking at 80% with escape hatch (changed from soft)
- [x] D4: Lint + Type + Test required (security scanning TBD)

---

## Document History

| Date | Author | Changes |
|------|--------|---------|
| 2026-01-10 | Claude Opus 4.5 | Initial ADR proposal |
| 2026-01-10 | User + Claude | User feedback: D2 changed to matrix, D3 changed to blocking |
| 2026-01-10 | Claude Opus 4.5 | ADR status changed to ACCEPTED |
