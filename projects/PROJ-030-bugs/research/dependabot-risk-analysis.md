# Dependabot Grouping Risk Analysis

> Risk analysis for issue #188: Risk-tiered Dependabot configuration for Jerry Framework.
> Analysis type: risk (FMEA)
> Project: PROJ-030-bugs

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Plain-language findings for stakeholders |
| [L1: Technical Analysis](#l1-technical-analysis) | Dependency classification, grouping risk, FMEA |
| [L2: Architectural Implications](#l2-architectural-implications) | Strategic patterns and systemic considerations |
| [Evidence Summary](#evidence-summary) | All cited evidence |

---

## L0: Executive Summary

**What was analyzed:** Jerry's Dependabot configuration currently creates one PR per dependency update. This produced 13 simultaneous open PRs — including a gherkin-official 29-to-39 bump that broke compatibility with pytest-bdd and had to be closed as issue #190. The question is whether to group updates by risk tier (patch+minor together, major individual, security individual) and what risks that grouping introduces.

**Key finding:** The proposed grouping strategy is sound. The main risk is not "grouped PRs are harder to debug" — CI passes or fails at the PR level, and Jerry's test matrix (8 OS/Python combinations) provides strong breakage detection. The real risk is **transitive dependency conflicts within a group**: a bump to package A can break package B if they share a transitive dep with conflicting version constraints, and the failure message may not immediately reveal which update caused it. This is exactly what happened with gherkin-official/pytest-bdd.

**Recommended action:** Implement risk-tiered grouping with one important refinement — group `test` extras separately from `runtime` extras so transitive conflicts within the test framework (gherkin-official class of incident) are isolated from runtime dependency issues. Security updates should never be grouped; they need individual fast-path review. Major updates should remain individual for both pip and GitHub Actions ecosystem.

---

## L1: Technical Analysis

### 1. Dependency Risk Classification

Evidence source: `pyproject.toml` (direct deps), `requirements-test.txt` (transitive test deps), `requirements-dev.txt` (transitive dev deps).

#### Runtime Dependencies (shipped with plugin, affect users)

These are in `[project].dependencies` in `pyproject.toml`. Breakage here produces runtime failures for end users.

| Dependency | Constraint | Blast Radius | Transitive Deps | Notes |
|------------|-----------|--------------|-----------------|-------|
| `jsonschema[test]>=4.26.0` | minor floor | HIGH: schema validation failures at runtime | `attrs`, `rpds-py`, `referencing` (from uv.lock) | Used in `src/agents/infrastructure/adapters/claude_code_adapter.py`; validates agent governance schemas |
| `webvtt-py>=0.5.1` | minor floor | MEDIUM: transcript parsing failures | None significant | VTT/SRT parsing in transcript bounded context |
| `tiktoken>=0.5.0` | minor floor | MEDIUM: token counting failures | `regex`, `requests` (BPE encoder download) | EN-026: chunking for BUG-001 fix; breaks `jerry ci chunk` command |
| `filelock>=3.20.3` | minor floor | LOW-MEDIUM: session locking failures | None | Cross-session state management |
| `markdown-it-py>=4.0.0,<5.0.0` | minor+major bounded | MEDIUM: markdown parsing failures | `mdurl` | Bounded `<5.0.0` — major bump blocked by constraint |
| `mdformat>=1.0.0,<2.0.0` | minor+major bounded | LOW: formatting output changes | `markdown-it-py`, `mdit-py-plugins` | Bounded `<2.0.0`; also has transitive dep on `markdown-it-py` |
| `mdit-py-plugins>=0.4.0` | minor floor | LOW: markdown plugin failures | `markdown-it-py` | Shared transitive dep with mdformat |
| `pyyaml>=6.0` | minor floor | HIGH: YAML parsing failures across entire codebase | None | EN-005: used in StalenessDetector; also used in nearly all hook scripts |

**Runtime dep assessment:** `jsonschema` and `pyyaml` have the highest blast radius — a breaking change in either affects core framework behavior. `tiktoken` has binary wheels that may not build on all Python/OS combinations, making major bumps higher risk than the version floor suggests.

#### Dev-Only Dependencies (test/lint/build, affect only CI)

These are in `[project.optional-dependencies].dev`, `[project.optional-dependencies].test`, `[dependency-groups].dev`.

| Dependency | Constraint | Blast Radius | Category |
|------------|-----------|--------------|----------|
| `pytest>=8.0.0` (test extras) / `>=9.0.2` (dep-groups) | minor floor | CI-only: test suite failures | Test runner |
| `pytest-bdd>=8.0.0` | minor floor | CI-only: BDD test failures | BDD framework — INCIDENT HISTORY (PR #190) |
| `pytest-cov>=4.0.0` (test) / `>=7.0.0` (dep-groups) | minor floor | CI-only: coverage reporting | Coverage |
| `pytest-archon>=0.0.6` | minor floor | CI-only: architecture test failures | Architecture enforcement |
| `mypy>=1.8.0` | minor floor | CI-only: type check failures | Type checker |
| `ruff>=0.1.0` (dev) / `>=0.14.11` (dep-groups) | minor floor | CI-only: lint failures | Linter/formatter |
| `mkdocs-material>=9.7.2` | minor floor | CI-only: docs build failures | Docs builder |
| `pip-audit>=2.10.0` | minor floor | CI-only: security scan failures | Security scanner |
| `pre-commit>=4.5.1` | minor floor | CI-only: hook failures | Git hooks |
| `pyright>=1.1.408` | minor floor | CI-only: type check failures | Type checker |
| `pip-licenses>=5.5.1` | minor floor | CI-only: license scan failures | License checker |

**Dev dep assessment:** No dev-only dep break produces a user-visible failure. All dev dep failures surface as CI failures on the Dependabot PR itself, which is the correct place for them to surface.

#### Build System

| Dependency | Location | Blast Radius |
|------------|----------|--------------|
| `hatchling` | `[build-system].requires` | HIGH at release time: build failures prevent packaging |

Hatchling is tracked by the pip ecosystem in Dependabot. It is build-only (not installed at runtime), but a major bump breaking the build would block releases. Treat as individual for major bumps.

---

### 2. Grouping Risk Assessment (FMEA)

The following failure modes are assessed for each proposed group. S = Severity (1-10), O = Occurrence probability (1-10), D = Detection difficulty (1-10), RPN = S x O x D.

#### Group A: pip patch+minor (all dev deps)

**Proposed behavior:** One PR batches all minor and patch updates for pytest, pytest-bdd, pytest-cov, pytest-archon, mypy, ruff, mkdocs-material, pip-audit, pre-commit, pyright.

| Failure Mode | Effect | Cause | S | O | D | RPN | Action |
|---|---|---|---|---|---|---|---|
| pytest-bdd minor bump breaks gherkin-official transitive dep | CI fails: BDD test suite cannot parse feature files | gherkin-official 29→39 breaks BDD parser (INCIDENT: PR #190) | 5 | 6 | 4 | 120 | Separate test-framework deps into own group (see Recommendation R-3) |
| ruff minor bump introduces new lint rules that fail | CI fails: lint job | New ruff release adds rules that flag existing code | 3 | 7 | 1 | 21 | Fix lint violations; trivial to isolate (ruff output names the rule) |
| mypy minor bump tightens type inference | CI fails: type-check job | New mypy strictness catches previously-allowed patterns | 4 | 5 | 1 | 20 | Fix type annotations; trivial to isolate |
| Two deps both bump, interact via shared transitive | CI fails: unclear which dep caused it | e.g., pytest + pytest-cov share `coverage`; conflicting pin | 5 | 3 | 6 | 90 | Separate test-framework group reduces dep count per group |
| mkdocs-material minor bump changes theme behavior | CI fails or docs render incorrectly | Theme API change breaks MkDocs config | 2 | 3 | 2 | 12 | Acceptable; MkDocs build failure is obvious |

**RPN > 100:** pytest-bdd/gherkin-official transitive conflict (120). This is the demonstrated incident, not a theoretical one.

**Isolation difficulty rating (4/10):** When a grouped PR fails, the CI log shows which job failed and which test assertions failed, but the commit history shows N dependency bumps simultaneously. The maintainer must read the pip resolver output or bisect manually to identify which bump introduced the conflict. This is the core cost of grouping.

**Rollback strategy:** Close the grouped PR, revert to the previous group state (Dependabot will re-open individual PRs on the next scheduled run), or manually cherry-pick the failing dependency out of the group using Dependabot's "rebase" comment.

---

#### Group B: pip major (individual PRs, no grouping)

**Proposed behavior:** Each major version bump gets its own PR.

| Failure Mode | Effect | Cause | S | O | D | RPN | Action |
|---|---|---|---|---|---|---|---|
| Major bump breaks API used in src/ | CI fails: tests + type-check | Runtime dep removes/changes public API | 8 | 4 | 2 | 64 | Individual PR makes isolation trivial (one dep, one PR) |
| Major bump changes transitive deps (lockfile diff) | CI fails: lockfile diff guard in version-bump.yml warns | Breaking change pulls in new transitive deps or bumps existing ones | 6 | 5 | 2 | 60 | Lockfile diff guard (lines 187-192 of version-bump.yml) already detects this |

**RPN assessment:** All RPNs below 100. Individual PR strategy correctly isolates failures.

---

#### Group C: GitHub Actions patch+minor+major (all updates in one group)

The existing CI assessment (`dependabot-grouping-ci-assessment.md`, Assessment 3) already analyzes this. Key FMEA entries:

| Failure Mode | Effect | Cause | S | O | D | RPN | Action |
|---|---|---|---|---|---|---|---|
| actions/checkout major bump changes checkout behavior | CI fails: unexpected file state | Changed default fetch-depth, checkout path, or token behavior | 5 | 2 | 2 | 20 | CI jobs catch this; isolation from failure message |
| astral-sh/setup-uv version bump breaks uv invocation | CI fails: setup-uv job | New major changes CLI interface or version syntax | 5 | 2 | 2 | 20 | Direct mapping: setup-uv failure -> setup-uv action |
| Third-party Action (e.g., codecov, MishaKav) major bump | CI fails or silent behavioral change | API change in Action inputs/outputs | 5 | 3 | 3 | 45 | Third-party Actions have higher risk (see R-4 below) |

**Evidence:** Jerry uses `actions/checkout`, `actions/setup-python`, `actions/upload-artifact`, `actions/download-artifact`, `astral-sh/setup-uv`, `codecov/codecov-action`, `MishaKav/pytest-coverage-comment`, `actions/github-script`, `softprops/action-gh-release`. SHA pinning (EN-001) means the actual behavior is controlled by the hash, not the version tag. Isolation when Actions fail is straightforward: the failing job names the action.

**RPN assessment:** All RPNs below 100. Grouping Actions is safe.

---

#### Group D: Security updates (individual, fast-path)

| Failure Mode | Effect | Cause | S | O | D | RPN | Action |
|---|---|---|---|---|---|---|---|
| Security update grouped with routine update; conflict delays merge | Vulnerability window extended | Group CI failure from an unrelated dep blocks the security fix | 9 | 3 | 2 | 54 | Never group security updates |
| Security update for transitive dep conflicts with parent package | CI fails: incompatible versions | e.g., security update bumps a transitive dep past what a direct dep allows | 7 | 4 | 5 | 140 | Individual security PRs make this visible immediately; grouping would obscure it |

**Critical finding (RPN 140):** The highest-risk failure mode in the entire analysis is a security update for a transitive dep that conflicts with its parent. This happened with gherkin-official (a transitive dep of pytest-bdd with its own version constraint). If that bump had been a security patch, grouping it would have obscured the conflict. Individual security PRs are mandatory.

---

### 3. Transitive Dependency Risk

**The gherkin-official incident (PR #190) is the canonical evidence.**

From `requirements-test.txt`:
```
gherkin-official==29.0.0
    # via pytest-bdd
```

Dependabot bumped `gherkin-official` to version 39 (a major bump). This was a transitive dep of `pytest-bdd`. Dependabot does not honor the constraints that `pytest-bdd` places on `gherkin-official` — it tracks the package's upstream latest version independently. The result: `gherkin-official 39` was incompatible with `pytest-bdd 8.x`, causing PR #190 to be closed.

**Which runtime deps pin their transitive deps tightly:**

| Direct Dep | Known Tight Transitive Pins | Risk |
|------------|----------------------------|------|
| `pytest-bdd>=8.0.0` | `gherkin-official` (pinned to a specific range per version) | HIGH: demonstrated incident |
| `markdown-it-py>=4.0.0,<5.0.0` + `mdformat>=1.0.0,<2.0.0` | Both share `markdown-it-py` as a transitive dep; `mdformat` pins to a range | MEDIUM: cross-dependency conflict if `markdown-it-py` bumps past `mdformat`'s constraint |
| `tiktoken>=0.5.0` | `regex`, `requests` | LOW: tiktoken uses these for BPE downloads; these are stable |
| `jsonschema[test]>=4.26.0` | `attrs`, `referencing`, `rpds-py` | LOW: attrs and referencing have loose constraints |

**Should transitive-only deps be excluded from Dependabot?**

Assessment: Yes, with qualification. Dependabot tracking transitive deps independently of their parents produces exactly the class of failure seen in #190. For the `pip` ecosystem, the correct approach is:

1. Do not group `gherkin-official` with pytest updates. The `requirements-test.txt` shows it as `# via pytest-bdd` — it should not be tracked at all by Dependabot if pytest-bdd manages its own version of gherkin-official. The safe option is to add `gherkin-official` to an `ignore` list in `dependabot.yml` and let pytest-bdd's own release manage it.
2. Similarly, `mako` and `markupsafe` (via pytest-bdd's mako dependency) should be excluded.
3. `six`, `parse`, `parse-type` (via pytest-bdd) should be excluded.

The pattern: if a package only appears under `# via pytest-bdd` or `# via [other-direct-dep]` in `requirements-test.txt`, and its version is determined by that parent package's own requirements, exclude it from Dependabot updates. It cannot be safely bumped independently.

---

### 4. Security Update Risk

**Should security updates ever be grouped?**

No. The trade-off analysis:

| Factor | Merge Fast (grouped) | Review Carefully (individual) |
|--------|---------------------|-------------------------------|
| Vulnerability window | Short (merged with routine updates) | Potentially longer (individual review cycle) |
| Conflict visibility | Obscured — CI failure may be from a co-grouped update | Visible — only one dep in the PR |
| Transitive conflict detection | Harder | Easy — lockfile diff shows only security update's transitive changes |
| Supply chain verification | Harder to audit | Straightforward — one diff to review |

**Security-specific failure mode (from Section 2, RPN 140):** A security update for a transitive dep — e.g., a patched CVE in `gherkin-official` — grouped with a routine pytest minor bump would obscure whether the CI failure was caused by the security patch or the routine update. This could delay merging a CVE fix while the routine update is debugged separately.

**Recommendation:** Security updates are always individual, regardless of whether they are patch, minor, or major bumps. Dependabot's `open-pull-requests-limit` for security updates should not be set below the number of potentially vulnerable deps (effectively unlimited). Configure `insecure-external-code-execution: deny` and set security updates as a separate configuration block if Dependabot allows it.

---

### Recommended Grouping Configuration

Based on the FMEA, the following grouping structure minimizes risk:

```yaml
groups:
  # Group 1: GitHub Actions — all updates (patch, minor, major)
  # Rationale: SHA pinning, CI gatekeeper, first-party publishers
  # Risk: All RPNs < 50
  actions-all:
    patterns: ["*"]

  # Group 2: pip dev tools (linters, type checkers, build tools)
  # Rationale: Independent tools; failures are isolated by job name
  # Risk: Low (RPN < 30 for each tool independently)
  pip-dev-tools:
    dependency-type: "development"
    patterns: ["mypy", "ruff", "pyright", "pre-commit", "pip-audit", "pip-licenses",
               "mkdocs-material"]
    update-types: ["minor", "patch"]

  # Group 3: pip test framework (pytest ecosystem only, NOT gherkin-official)
  # Rationale: Separate from dev tools to isolate transitive conflicts in BDD framework
  # Excludes gherkin-official and other pytest-bdd transitive deps (see ignore list)
  # Risk: Moderate if not separated (RPN 120 for transitive conflict)
  pip-test-framework:
    dependency-type: "development"
    patterns: ["pytest", "pytest-cov", "pytest-archon", "pytest-bdd"]
    update-types: ["minor", "patch"]

  # NOTE: No group for pip runtime minor/patch.
  # Runtime deps have individual PRs for all update types.
  # Rationale: Runtime blast radius (user-facing), tight version constraints
  # (markdown-it-py and mdformat share transitive deps).
```

**Ignore list additions (transitive deps managed by parent packages):**

```yaml
ignore:
  - dependency-name: "gherkin-official"
    update-types: ["version-update:semver-major"]
  - dependency-name: "mako"
    update-types: ["version-update:semver-major"]
  - dependency-name: "markupsafe"
    update-types: ["version-update:semver-major"]
  - dependency-name: "six"
    update-types: ["version-update:semver-major"]
  - dependency-name: "parse"
    update-types: ["version-update:semver-major"]
  - dependency-name: "parse-type"
    update-types: ["version-update:semver-major"]
```

---

## L2: Architectural Implications

### Systemic Pattern: The Transitive Dep Trust Problem

The gherkin-official incident reveals a systemic tension in Dependabot's design: it tracks packages in the resolved dependency tree independently, without honoring the constraint relationships between them. When `pytest-bdd` declares `gherkin-official >=29,<30` in its own requirements, Dependabot ignores that constraint and proposes `gherkin-official 39` because the upstream package released a new version.

This is not a Dependabot bug — it is by design. Dependabot treats each listed package as independently upgradeable. The architectural implication for Jerry is:

**The dependency manifest (`requirements-test.txt`) should be regenerated from the authoritative source (`pyproject.toml` + `uv.lock`) on every PR merge, not treated as a static file that Dependabot can update piecemeal.**

If `requirements-test.txt` is regenerated from `uv.lock` (which records the fully resolved, constraint-consistent tree), Dependabot's bump of `gherkin-official` to version 39 would have been blocked at lockfile resolution time — `uv` would have refused to resolve it given `pytest-bdd 8.x`'s constraints.

**Strategic recommendation:** The long-term fix is not grouping configuration — it is ensuring that `requirements-test.txt` is always a derived artifact from `uv.lock`, not an independently editable file. If Dependabot cannot propose a bump that satisfies `uv`'s resolver, the incompatibility surfaces before it reaches CI.

---

### Grouping vs. Merge Queue

The existing research file `merge-queue-vs-dependabot-grouping.md` in this project already explores this trade-off. The complementary architectural view: these are not alternatives — they address different failure modes.

- **Dependabot grouping** reduces PR volume by batching low-risk updates. It does not prevent individual update conflicts; it only reduces the number of PRs a maintainer must review.
- **Merge queue** (GitHub's built-in or a custom tool) ensures that no PR merges until it has been rebased against HEAD and passed CI. This prevents the class of "PR A and PR B both pass CI independently but conflict when both merge" failure.

For Jerry's scale (one primary maintainer, ~10-15 Dependabot PRs per week without grouping), grouping is the correct primary tool. A merge queue adds operational overhead that is not justified at this scale.

---

### PR Volume Reduction: Quantitative Projection

Current state (13 simultaneous PRs, no grouping):

| Category | Current PRs | With Proposed Grouping |
|----------|------------|------------------------|
| GitHub Actions | ~10 | 1 (grouped) |
| pip dev tools (minor/patch) | ~2 | 1 (grouped) |
| pip test framework (minor/patch) | ~1 | 1 (grouped) |
| pip runtime (minor/patch) | ~2 | individual (not grouped) |
| pip major (any ecosystem) | ~0-1 | individual (by design) |
| Security updates | ~0-1 | individual (by design) |
| **Total** | **13** | **4-6** |

The reduction in PR volume (from 13 to ~5) directly addresses the maintainer burden that issue #188 describes. The proposed grouping achieves approximately 62% reduction in PR count under steady-state weekly cadence.

---

### Supply Chain Security Posture (AE-005 Alignment)

This change touches CI infrastructure and therefore triggers AE-005 (security-relevant code, Auto-C3 minimum). The relevant risk profile:

**SHA pinning (EN-001) provides baseline protection.** GitHub Actions are SHA-pinned, meaning Dependabot PRs for Actions updates propose new SHAs that have been cryptographically verified by GitHub. A malicious actor cannot retroactively change what a SHA points to. This makes Actions grouping lower risk than it would be for tag-pinned Actions.

**Pip packages are not SHA-pinned.** A pip package on PyPI can be yanked and replaced (rare, but possible). The `pip-audit` job in CI mitigates this by checking for known CVEs. The lockfile (`uv.lock`) provides hash verification per-wheel, which `uv sync --frozen` enforces. This is sufficient protection.

**The security update individual PR requirement is non-negotiable.** If a CVE is disclosed against a runtime dependency (e.g., `pyyaml`, `tiktoken`, `jsonschema`), the security update must be individually reviewed with attention to: (a) what the CVE is, (b) whether the fix version is compatible, (c) whether the fix introduces new transitive deps.

---

### Long-Term Configuration Hygiene

The proposed `ignore` list entries for transitive deps are a maintenance debt item: every time `pytest-bdd` or another parent dep is major-bumped, the ignore list should be reviewed because the new major version may change its transitive dep constraints. Document this in a comment within `dependabot.yml`.

Additionally, the two version constraints for some deps (e.g., `pytest` appears in both `[project.optional-dependencies].test` and `[dependency-groups].dev` with different floor versions: `>=8.0.0` vs `>=9.0.2`) should be reconciled. Dependabot will track both and may propose different version updates for each, creating apparent duplicates. Consolidating to a single source of truth in `pyproject.toml` is the correct fix.

---

## Evidence Summary

| Evidence ID | Type | Source | Relevance |
|-------------|------|--------|-----------|
| E-001 | Config | `/pyproject.toml` lines 31-59 | Direct dependency classification: runtime vs. dev vs. test extras |
| E-002 | Config | `/requirements-test.txt` | Transitive dep tree for test group; shows gherkin-official as `# via pytest-bdd` |
| E-003 | Config | `/requirements-dev.txt` | Transitive dep tree for dev group; shows mypy-extensions, pathspec via mypy |
| E-004 | Config | `/.github/dependabot.yml` | Current Dependabot configuration: no grouping, individual PRs |
| E-005 | Config | `/.github/workflows/ci.yml` | CI pipeline: 12 jobs, SHA-pinned Actions; test matrix 3 OS x 4 Python versions |
| E-006 | Research | `/projects/PROJ-030-bugs/research/dependabot-grouping-ci-assessment.md` | Prior architecture assessment: commit prefix resolution, open-PR-limit interaction, transition behavior |
| E-007 | Incident | Issue #190 (referenced in task description) | gherkin-official 29→39 bump incompatible with pytest-bdd; PR closed as incompatible |
| E-008 | Config | `/.github/workflows/ci.yml` lines 555-558 | changelog-check exempts dependabot[bot] — Dependabot PRs do not need changelog entries |
| E-009 | Config | `/.github/workflows/version-bump.yml` lines 187-192 | Lockfile diff guard: warns when uv.lock changes beyond version field |
| E-010 | Grep | All `uses:` lines in `.github/workflows/*.yml` | GitHub Actions inventory: actions/checkout, setup-python, upload-artifact, download-artifact, astral-sh/setup-uv, codecov/codecov-action, MishaKav/pytest-coverage-comment, actions/github-script, softprops/action-gh-release |
| E-011 | Config | `/pyproject.toml` lines 195-205 | `[dependency-groups].dev` has separate version pins from `[project.optional-dependencies].dev` — potential source of Dependabot duplicate PRs |

---

## Conclusions

1. **The proposed grouping strategy is sound** with one critical refinement: separate test-framework deps (pytest, pytest-bdd, pytest-cov, pytest-archon) into their own group, isolated from dev tools (ruff, mypy, etc.). The gherkin-official incident demonstrates that pytest-bdd transitive dep conflicts are real, not theoretical.

2. **Transitive-only deps should be excluded from Dependabot** for the pytest-bdd ecosystem: gherkin-official, mako, markupsafe, six, parse, parse-type. Confidence level: HIGH (E-002, E-007 confirm the specific failure mode).

3. **Runtime deps should not be grouped for minor/patch**. With 7 runtime deps and tight cross-constraints (markdown-it-py / mdformat / mdit-py-plugins form a connected component), the isolation benefit of individual PRs outweighs the overhead of ~2-3 PRs per week. Confidence: MEDIUM (inferred from constraint analysis; no incident evidence for runtime grouping failure).

4. **Security updates are always individual**. The RPN 140 failure mode (transitive dep security update grouped with routine update obscures conflict) is the highest risk in this analysis. Confidence: HIGH (analytical).

5. **GitHub Actions can be grouped including majors**. SHA pinning and CI gatekeeper provide sufficient detection with low isolation difficulty. All RPNs below 50. Confidence: HIGH (E-006 corroborates, E-010 confirms publisher trust level).

---

## Recommendations

| ID | Recommendation | Priority | Rationale |
|----|---------------|----------|-----------|
| R-1 | Group all GitHub Actions updates (patch, minor, major) | HIGH | SHA pinning + CI gatekeeper; all RPNs < 50 |
| R-2 | Group pip dev tools (ruff, mypy, pyright, pre-commit, pip-audit, pip-licenses, mkdocs-material) minor+patch | HIGH | Independent tools, isolated failure signals, low transitive conflict risk |
| R-3 | Group pytest ecosystem (pytest, pytest-bdd, pytest-cov, pytest-archon) minor+patch in a SEPARATE group from dev tools | HIGH | Isolates gherkin-official class of incident; RPN 120 reduced to near-zero by separation |
| R-4 | Do NOT group runtime deps (jsonschema, webvtt-py, tiktoken, filelock, markdown-it-py, mdformat, mdit-py-plugins, pyyaml) | HIGH | User-facing blast radius; tight cross-constraints in markdown family |
| R-5 | Exclude transitive deps of pytest-bdd from Dependabot ignore list | HIGH | Eliminates recurrence of PR #190 class incident |
| R-6 | Security updates always individual — add `open-pull-requests-limit: 0` override or separate security block | CRITICAL | RPN 140 failure mode; vulnerability window vs. conflict visibility trade-off |
| R-7 | Reconcile duplicate pytest/ruff/filelock/jsonschema entries between `[project.optional-dependencies]` and `[dependency-groups]` | MEDIUM | Prevents Dependabot duplicate PR confusion |
| R-8 | Add comment in dependabot.yml: review ignore list when pytest-bdd major is bumped | LOW | Maintenance debt; ignore list may need to change when parent dep changes transitive constraints |

---

*Analysis conducted: 2026-03-12*
*Agent: ps-analyst*
*Project: PROJ-030-bugs*
*PS Context: Issue #188*
*Analysis type: risk (FMEA)*
*Confidence: HIGH for grouping recommendations; MEDIUM for runtime dep individual PR recommendation*
