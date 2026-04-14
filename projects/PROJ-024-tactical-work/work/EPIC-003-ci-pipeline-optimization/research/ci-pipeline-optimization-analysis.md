# CI Pipeline Optimization Analysis

> Analyst: ps-analyst | PS ID: work-ci | Entry ID: e-001 | Type: gap/impact
> Source: /tmp/ci-yml-main.txt (707 lines, 29 jobs)
> Date: 2026-04-13

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Plain-language finding and recommendation |
| [L1: Technical Analysis](#l1-technical-analysis) | Job inventory, dependency graph, redundancy map, cost model |
| [L2: Architectural Implications](#l2-architectural-implications) | Structural patterns, strategic trade-offs |
| [Proposed Target Structure](#proposed-target-structure) | Optimized job layout with rationale |
| [Evidence Summary](#evidence-summary) | Cited evidence table |
| [Assumptions and Limitations](#assumptions-and-limitations) | Explicit uncertainty |

---

## L0: Executive Summary

The Jerry CI pipeline has 29 jobs and wastes approximately 7-9 minutes of pure runner startup time per run on small jobs that each boot their own Python environment. Six jobs do essentially the same setup (checkout + uv install + Python install + uv sync) just to run a single script. Two parallel test matrices (`test-pip` and `test-uv`) run the same test suite twice across the same OS/Python grid — the pip matrix exists for portability testing but conflicts with Jerry's own H-05 rule that mandates uv-only. Three quality tool jobs (lint, type-check, security) each install Python independently using pip rather than uv.

The recommended action is to consolidate the six single-script validation jobs into one `validations` job, eliminate the `test-pip` matrix or reduce it to a targeted portability smoke test, and migrate lint/type-check/security to use uv. This would cut the job count from 29 to approximately 17, reduce estimated overhead by 5-7 minutes per run, and resolve the H-05 violation in three jobs.

---

## L1: Technical Analysis

### 1. Job Inventory (all 29 jobs)

| # | Job Name | Runner Setup | Install Method | Primary Work | Notes |
|---|----------|-------------|----------------|--------------|-------|
| 1 | lint | Python 3.14 via setup-python | `pip install ruff` | `ruff check`, `ruff format` | Uses pip; H-05 violation |
| 2 | type-check | Python 3.14 via setup-python | `pip install pyright`, `pip install -e .` | `pyright src/` | Uses pip; H-05 violation |
| 3 | security | Python 3.14 via setup-python | `pip install pip-audit` + manual dep list | pip-audit + yaml grep | Uses pip; H-05 violation |
| 4 | lockfile-check | uv only | `uv lock --check` | One command | Single-step job |
| 5 | plugin-validation | uv + Python 3.14 | `uv sync --frozen --extra dev` | 4 validation scripts | Multi-step, worthwhile |
| 6 | template-validation | uv + Python 3.14 | `uv sync --frozen` | `validate_templates.py` | Single-script job |
| 7 | frontmatter-validation | uv + Python 3.14 | `uv sync --frozen` | `jerry agents validate-frontmatter` | Single-script job |
| 8 | license-headers | uv + Python 3.14 | `uv sync --frozen` | `check_spdx_headers.py` | Single-script job |
| 9 | cli-integration | uv + Python 3.14 | `uv sync --frozen --extra dev --extra test` | pytest subprocess + e2e + help/version | Multi-step, worthwhile |
| 10-17 | test-pip (8 matrix cells) | Python matrix via setup-python | `pip install -r requirements-test.txt` + `pip install -e .` | Full pytest with coverage | pip; same tests as test-uv |
| 18-25 | test-uv (8 matrix cells) | uv + Python matrix | `uv sync --frozen --extra test` | Full pytest with coverage | uv; excludes subprocess tests |
| 26 | coverage-report | uv | download artifact | PR comment only | PR-only; no install needed |
| 27 | version-sync | uv + Python 3.14 | `uv sync --frozen` | `sync_versions.py --check` | Single-script job |
| 28 | hard-rule-ceiling | uv + Python 3.14 | `uv sync --frozen` | `check_hard_rule_ceiling.py` | Single-script job |
| 29 | changelog-check | git only | none | `git diff` grep | PR-only; no Python needed |
| (gate) | ci-success | none | none | needs-check logic only | Gate job |

**Effective job count in gate:** 15 real jobs + 1 gate + 1 coverage-report (PR-only) + 1 changelog-check (PR-only) = **18 jobs on PRs, 16 on push**.

### 2. Dependency Graph

All jobs in the current pipeline are independent (no `needs:` links) except:

```
lockfile-check    lint    type-check    security
      |             |         |            |
plugin-validation  |         |            |
template-validation|         |            |
frontmatter-valid  |         |            |
license-headers    |         |            |
cli-integration    |         |            |
      |             \        |           /
      |              \       |          /
test-pip (8 cells) ----+--test-uv (8 cells)
      \                          /
       \                        /
        --> coverage-report (PR)
              \
               +-> ci-success (needs all 14 above + changelog-check)
```

**Key observation:** Every job starts from zero — no shared caching, no shared venv. The 13 independent jobs run fully in parallel, which is the pipeline's main performance mechanism. However, many of those 13 slots are occupied by single-script jobs that do not justify their startup overhead.

### 3. Parallelism Assessment

**Already parallel (correct):**
- All 13 non-dependent jobs run concurrently.
- test-pip and test-uv matrix cells run concurrently.

**Unnecessarily serialized:** None — the pipeline is actually too parallel in the wrong direction (too many jobs, not too few parallel lanes).

**Under-parallelized within jobs:**
- `security` runs pip-audit then yaml grep sequentially; could be concurrent steps but this is minor.
- `plugin-validation` runs 5 validation steps sequentially; some could be parallel (py_compile checks) but the overhead is trivial.

**Critical path (longest chain, start to ci-success):**
The critical path is any of the matrix test jobs, which each take:
- ~30s startup (checkout + uv install + Python install + uv sync)
- Estimated 2-5 min test execution (depending on matrix cell)
- Total: ~3-6 min

The ci-success gate adds ~5s.

Estimated **critical path: 3-6 minutes** for a typical push. PRs add coverage-report (~30s after test jobs complete).

### 4. Redundant Work Analysis

#### Finding R-01: test-pip violates H-05 and duplicates test-uv

`test-pip` and `test-uv` run the same pytest suite across the same OS/Python matrix (ubuntu/windows/macos x 3.11/3.12/3.13/3.14 with the same exclusions). The only difference:

| Dimension | test-pip | test-uv |
|-----------|----------|---------|
| Installer | pip | uv |
| Extra markers excluded | `not llm` | `not llm and not subprocess` |
| HTML report | yes | no (noted as incomplete) |
| Coverage flags | `flags: pip` | `flags: uv` |

The pip matrix installs mkdocs-material explicitly and runs subprocess tests; uv skips subprocess tests because mkdocs-material is not in `--extra test`. This is an accidental asymmetry, not a purposeful testing split.

**H-05 violation (explicit):** `test-pip` uses `python -m pip install --upgrade pip` and `pip install -r requirements-test.txt`. H-05 states: "MUST use `uv run` for all Python execution. NEVER use `python`, `pip`, or `pip3` directly."

**Cost:** The pip matrix runs 8 cells (same count as uv matrix). Each cell duplicates: checkout + Python install + pip install + full pytest. Estimated 8 x (30s overhead + 3-5 min test) = **25-45 min of compute per push** for test-pip alone.

**Assessment:** test-pip should be eliminated or replaced by a targeted pip portability smoke test (install check only, no full test run). The subprocess/mkdocs asymmetry should be fixed in test-uv by adding mkdocs-material to the test extra.

#### Finding R-02: Six single-script jobs with identical setup overhead

The following jobs each perform: checkout (~5s) + uv install (~10s) + Python install (~15s) + `uv sync --frozen` (~20-30s) just to run one script:

| Job | Script | Estimated script runtime |
|-----|--------|------------------------|
| lockfile-check | `uv lock --check` | < 5s |
| template-validation | `validate_templates.py` | < 10s |
| frontmatter-validation | `jerry agents validate-frontmatter` | < 30s |
| license-headers | `check_spdx_headers.py` | < 10s |
| version-sync | `sync_versions.py --check` | < 5s |
| hard-rule-ceiling | `check_hard_rule_ceiling.py` | < 5s |

Total script work: ~65s. Total job overhead (6 x 50-60s setup): **~5-6 min of pure overhead**.

All six use identical setup sequences and have no `needs:` dependencies. They can be consolidated into one `validations` job without losing any signal — each script still runs, failures are still visible by step name.

Note: `lockfile-check` does not need `uv sync --frozen` (it only needs uv itself), making it even lighter. It currently spins up a full Python environment unnecessarily.

#### Finding R-03: lint, type-check, security use pip in a uv codebase

Three jobs install Python tools via pip rather than uv:

- `lint`: `pip install "ruff==0.14.11"` — ruff is already a dev dependency; `uv run ruff` would use the lockfile version.
- `type-check`: `pip install "pyright==1.1.408"` + `pip install -e ".[dev]"` — again, installs the full project via pip.
- `security`: `pip install pip-audit` + manual pinned list of deps — installs a separate audited dependency set outside the uv lockfile.

The lint and type-check cases are straightforward: switch to `uv sync --frozen --extra dev` + `uv run ruff` / `uv run pyright`. This removes H-05 violations and ensures version parity with the lockfile.

The security job is more nuanced: pip-audit by design installs deps outside uv to audit them against the PyPI advisory database. However, the current approach installs a hand-maintained pinned list (`filelock`, `mypy`, `ruff`) rather than the actual project dependencies, which means the audit scope is incomplete. This warrants a separate discussion (see L2).

#### Finding R-04: `uv sync --frozen` repeated independently in 8 jobs

Eight separate jobs (template-validation, frontmatter-validation, license-headers, version-sync, hard-rule-ceiling, plugin-validation, cli-integration, and coverage-report indirectly) each run `uv sync --frozen` independently. GitHub Actions does not share virtual environments between jobs. uv's cache action (`astral-sh/setup-uv` with cache enabled) can cache the download cache but not the installed venv. This is inherent to GitHub Actions job isolation — not a bug — but it reinforces the case for consolidation: fewer jobs = fewer redundant syncs.

### 5. Cost Analysis (Relative Estimates)

Assumptions: 30s startup overhead per job (checkout + uv install + Python install + uv sync), GitHub-hosted runner billed per minute, matrix cells count as individual jobs.

| Job Group | Job Count | Est. Overhead | Est. Work | Est. Total |
|-----------|-----------|---------------|-----------|------------|
| lint + type-check + security | 3 | 1.5 min | 2-3 min | 3.5-4.5 min |
| 6 single-script validation jobs | 6 | 5-6 min | ~1 min total | 6-7 min |
| test-pip matrix (8 cells) | 8 | 4 min | 24-40 min | 28-44 min (parallel: 3-6 min wall clock) |
| test-uv matrix (8 cells) | 8 | 4 min | 24-40 min | 28-44 min (parallel: 3-6 min wall clock) |
| plugin-validation + cli-integration | 2 | 1 min | 3-5 min | 4-6 min |
| coverage-report + changelog-check | 2 | ~15s total | ~30s | ~45s |
| ci-success | 1 | ~5s | ~5s | ~10s |
| **Total compute (sequential equivalent)** | **29** | **~16 min overhead** | **55-90 min** | **71-106 min** |
| **Wall-clock (parallel)** | — | — | — | **~6-10 min** |

The critical path (wall-clock) is dominated by the test matrices. The single-script jobs do not extend wall-clock time because they run in parallel with other jobs. However, they consume **compute minutes** (billed time) and **runner slots** (scarcity on busy repos).

**Overhead reduction from consolidation:**
- Merging 6 single-script jobs into 1 `validations` job: saves 5 x 30s = **2.5 min compute** per run (not wall-clock, since they run in parallel).
- Eliminating test-pip entirely: saves 8 x (3-6 min) = **24-48 min compute** per run (wall-clock unchanged for matrix cells that overlap with test-uv).
- Merging lint + type-check into one `static-analysis` job: saves 1 x 30s = **0.5 min compute**.

**Total estimated compute savings from all recommendations: 27-51 min per run** (primarily from eliminating test-pip matrix).

### 6. H-05 Violation Inventory

| Job | Violation | Line(s) |
|-----|-----------|---------|
| lint | `pip install "ruff==0.14.11"` | 40 |
| type-check | `python -m pip install --upgrade pip` + `pip install "pyright==..."` + `pip install -e ".[dev]"` | 63-66 |
| security | `python -m pip install --upgrade pip` + `pip install "pip-audit==..."` + `pip install ...` | 90-96 |
| test-pip | `python -m pip install --upgrade pip` + `pip install -r requirements-test.txt` + `pip install -e .` | 341-344 |

Total: 4 jobs with H-05 violations; test-pip is a structural H-05 violation (the whole job is pip-based by design).

---

## L2: Architectural Implications

### Pattern: The "Validation Sprawl" Anti-Pattern

The pipeline exhibits what can be called validation sprawl: each new governance check added over time became its own job rather than a step in an existing job. This is understandable operationally (clear job names, easy to identify which check failed) but creates a structural cost: the startup overhead grows linearly with the number of governance scripts.

The correct architectural pattern is a tiered validation structure:
1. Fast, stateless checks (grep, file existence, one-liner scripts) → consolidated `validations` job
2. Package-level static analysis (ruff, pyright, pip-audit) → `static-analysis` job
3. Integration-level validation (plugin manifests, CLI commands) → `integration` job (existing `cli-integration`)
4. Full test suites → test matrix jobs

The current pipeline conflates tiers 1 and 2 with tier 3, and runs tier 1 work in isolated jobs.

### The test-pip Question: Portability vs. H-05 Alignment

This is the highest-impact decision. There are two legitimate positions:

**Position A (eliminate test-pip):** Jerry mandates uv-only (H-05). The pip matrix validates an installation method that the framework itself forbids users from using internally. The portability signal from pip installation is low-value for a tool that explicitly requires uv. Eliminate test-pip entirely; the uv matrix is sufficient for coverage.

**Position B (reduce test-pip to smoke test):** pip installation of Jerry is documented (docs/INSTALLATION.md per line 306 comment) and may be a supported user-facing installation path distinct from the internal developer tooling H-05 governs. In this case, keep one pip smoke test (ubuntu + latest Python only) that verifies `pip install -e .` succeeds and `jerry --help` runs — but does not run the full test suite. This reduces compute from 8 cells to 1.

The analysis favors Position B with a caveat: the distinction between "pip as user installation method" and "pip as CI test mechanism" is valid, but running the full 80% coverage suite via pip adds no coverage signal that test-uv does not already provide. A smoke test suffices.

### Security Job Architecture: Incomplete Audit Scope

The security job audits a hand-maintained list of three packages (`filelock`, `mypy`, `ruff`) rather than the full project dependency graph. This creates a false sense of security: if a transitive dependency of Jerry (not in that hand-maintained list) has a known CVE, pip-audit will not catch it. The correct approach is to audit against `uv export --format requirements-txt` output or use `uv run pip-audit --requirement <(uv export --format requirements-txt)`. This is a correctness issue independent of the optimization work.

### Cost Model: When Consolidation Helps vs. When Parallel Wins

Consolidation helps when: jobs share identical setup, run quickly, and do not independently extend the critical path.

Consolidation hurts when: jobs are slow enough that their parallel execution saves wall-clock time, or when a job's failure should block different downstream behavior than its siblings.

For the single-script validation jobs: all run < 30s of actual work, all have the same failure consequence (block ci-success), and all share identical setup. Consolidation is clearly beneficial.

For lint vs. type-check: these are fast (~1 min each) and share setup. Consolidation saves compute. The developer experience argument for keeping them separate (clear failure signal) is addressed by named steps within one job.

---

## Proposed Target Structure

### Current State: 29 jobs (15 independent, 14 matrix cells, 1 gate)

### Target State: ~17 jobs (8 independent, 8 matrix cells, 1 gate)

| Proposed Job | Replaces | Rationale |
|-------------|----------|-----------|
| `static-analysis` | lint, type-check | Same setup; step names preserve failure signal; H-05 compliant via uv |
| `security` (modified) | security | Keep as separate job (pip-audit requires pip); fix audit scope to full deps |
| `validations` | lockfile-check, template-validation, frontmatter-validation, license-headers, version-sync, hard-rule-ceiling | Identical setup; 6 steps in 1 job; saves 5x startup overhead |
| `plugin-validation` | plugin-validation | Keep as-is; multi-step, justified isolation |
| `cli-integration` | cli-integration | Keep as-is; multi-step, justified isolation |
| `test-uv` (8 cells) | test-uv (8 cells) | Keep as-is; primary test matrix |
| `test-pip-smoke` (1 cell) | test-pip (8 cells) | ubuntu + 3.14 only; verify install + `jerry --help`; no full test run |
| `coverage-report` | coverage-report | Keep as-is; PR-only |
| `changelog-check` | changelog-check | Keep as-is; PR-only, no Python needed |
| `ci-success` | ci-success | Update needs list to new job names |

**Jobs eliminated: 12** (lint, type-check, lockfile-check, template-validation, frontmatter-validation, license-headers, version-sync, hard-rule-ceiling, 7 test-pip matrix cells)

**Jobs added: 2** (static-analysis, validations)

**Net reduction: 10 jobs** (29 → ~19, accounting for the pip-smoke replacement of 8 pip cells)

### `validations` Job Step Ordering

Within the consolidated `validations` job, steps should be ordered fastest-first to fail quickly:

1. `uv lock --check` (lockfile freshness, < 5s)
2. `uv run python scripts/check_hard_rule_ceiling.py` (< 5s)
3. `uv run python scripts/sync_versions.py --check` (< 5s)
4. `uv run python scripts/check_spdx_headers.py` (< 10s)
5. `uv run python scripts/validate_templates.py --verbose` (< 10s)
6. `uv run jerry agents validate-frontmatter` (< 30s, most expensive, last)

Note: `lockfile-check` currently does not call `uv sync --frozen`. In the consolidated job, it runs after `uv sync --frozen` completes — this is fine; `uv lock --check` still works in a synced environment.

### `static-analysis` Job

```yaml
static-analysis:
  name: Static Analysis
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@...
    - name: Install uv
      uses: astral-sh/setup-uv@...
    - name: Set up Python
      run: uv python install 3.14
    - name: Install dependencies
      run: uv sync --frozen --extra dev
    - name: Lint (ruff check)
      run: uv run ruff check . --config=pyproject.toml
    - name: Format check (ruff format)
      run: uv run ruff format --check . --config=pyproject.toml
    - name: Type check (pyright)
      run: uv run pyright src/
```

This requires ruff and pyright in the dev extra of pyproject.toml (likely already true for ruff; pyright may need to be added).

---

## Evidence Summary

| Evidence ID | Type | Source | Relevance |
|-------------|------|--------|-----------|
| E-001 | Code | ci-yml-main.txt:40 | lint uses `pip install ruff` — H-05 violation |
| E-002 | Code | ci-yml-main.txt:63-66 | type-check uses `pip install` x3 — H-05 violation |
| E-003 | Code | ci-yml-main.txt:90-96 | security uses `pip install` x3 — H-05 violation |
| E-004 | Code | ci-yml-main.txt:341-344 | test-pip uses `pip install` x3 — H-05 violation + structural |
| E-005 | Code | ci-yml-main.txt:120-133 | lockfile-check: checkout + uv install + one command |
| E-006 | Code | ci-yml-main.txt:186-205 | template-validation: full uv setup + one script |
| E-007 | Code | ci-yml-main.txt:213-230 | frontmatter-validation: full uv setup + one script |
| E-008 | Code | ci-yml-main.txt:238-254 | license-headers: full uv setup + one script |
| E-009 | Code | ci-yml-main.txt:541-559 | version-sync: full uv setup + one script |
| E-010 | Code | ci-yml-main.txt:565-584 | hard-rule-ceiling: full uv setup + one script |
| E-011 | Code | ci-yml-main.txt:304-407 | test-pip matrix: 8 cells, same OS/Python grid as test-uv |
| E-012 | Code | ci-yml-main.txt:414-507 | test-uv matrix: 8 cells, same grid |
| E-013 | Code | ci-yml-main.txt:90-96 | security audits 3 hand-picked packages, not full dependency graph |
| E-014 | Code | ci-yml-main.txt:649 | ci-success needs list: 14 jobs (all independent) |
| E-015 | Rule | .context/rules/quality-enforcement.md:H-05 | "MUST use `uv run` for all Python execution. NEVER use `python`, `pip`, or `pip3`" |

---

## Assumptions and Limitations

| ID | Assumption | Confidence | Impact if Wrong |
|----|------------|------------|-----------------|
| A-01 | ruff and pyright are already (or can be added) to the dev extra in pyproject.toml | High | static-analysis job needs minor adjustment |
| A-02 | `pip install jerry` is a documented user-facing installation path distinct from internal H-05 scope | Medium | If pip installation is unsupported, eliminate test-pip entirely (Position A) rather than keeping smoke test |
| A-03 | 30s startup overhead per job is a reasonable estimate for GitHub Actions ubuntu-latest runners | Medium | Actual overhead varies; cost savings estimates are proportional, not absolute |
| A-04 | The six single-script validation jobs have no order dependency on each other | High | All six are currently independent with no `needs:` links (confirmed from YAML) |
| A-05 | Consolidating jobs does not reduce the developer-visible failure signal because step names within a job are visible in the Actions UI | High | GitHub Actions shows step-level failures; job-level grouping does not hide them |
| A-06 | The pip matrix exclusions (windows 3.11/3.12, macos 3.11/3.12) match the uv matrix exclusions exactly | High | Confirmed identical exclude blocks (lines 317-325 vs 426-432) |

**Limitation:** This analysis is based solely on the YAML file. Actual runtimes, flakiness rates, and developer workflow preferences were not available. The cost estimates are relative, not measured from actual CI telemetry.
