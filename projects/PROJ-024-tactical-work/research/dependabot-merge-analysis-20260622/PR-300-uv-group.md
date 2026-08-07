# PR #300 Analysis — `deps: bump the uv-minor-patch group across 1 directory with 12 updates`

> Read-only release-engineering analysis of dependabot PR #300 (`geekatron/jerry`). All version claims cite the actual `gh pr diff 300` lines and real upstream changelogs / release notes. No repository modifications were made.

## Navigation

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | One-paragraph verdict and headline findings |
| [PR Metadata](#pr-metadata) | Branch, base, mergeability |
| [Package Update Table](#package-update-table) | All 12 declared bumps with semver class |
| [Declared-Constraint (pyproject.toml) Changes](#declared-constraint-pyprojecttoml-changes) | The constraint-floor edits |
| [Transitive Lock Churn (uv.lock)](#transitive-lock-churn-uvlock) | The httpx2/httpcore2/truststore/idna swap |
| [Flagged Packages — Real Release Notes](#flagged-packages--real-release-notes) | Breaking-change analysis per flagged package |
| [Critical Coordination Check: ruff & commitizen](#critical-coordination-check-ruff--commitizen) | Consistency with PR #299 / #291 |
| [CI Status](#ci-status) | Matrix vs. CI Success / Security Scan |
| [Risk Verdict](#risk-verdict) | LOW/MEDIUM/HIGH + pre-merge cautions |
| [Evidence Index](#evidence-index) | Sources cited |

---

## Summary

PR #300 bumps **12 declared packages** in the `uv-minor-patch` dependabot group. **Zero are MAJOR semver bumps** — all are minor or patch. The runtime-facing direct dependencies (`tiktoken`, `markdown-it-py`, `mdit-py-plugins`, `requests`, `pymdown-extensions`, `filelock`) move only by patch/minor with no documented breaking changes that affect this repo. The most material change is **transitive, not in the 12-package table**: `bump-my-version` 1.3.0 → 1.4.1 switched its HTTP dependency from `httpx` to **`httpx2`** (Pydantic's official maintained continuation of httpx, Tom Christie / Pydantic Services), which cascaded into `httpcore` → `httpcore2`, a new `truststore` 0.10.4, and `idna` 3.11 → 3.18. Because `bump-my-version` is **release/dev tooling only** (not imported at runtime or in the test suite), the blast radius of that swap is confined to local version-bumping operations. `ruff` **is** in this group (0.15.11 → 0.15.18) — relevant to PR #299's separate ruff pre-commit-hook bump — while `commitizen` **is NOT** in this group. All 9 `Test uv (...)` matrix jobs **pass**; the `CI Success` and `Security Scan` failures are unrelated to the dependency changes (separately under investigation). **Risk verdict: LOW.**

---

## PR Metadata

| Field | Value |
|-------|-------|
| Number | #300 |
| Title | `deps: bump the uv-minor-patch group across 1 directory with 12 updates` |
| Base branch | `main` |
| Files changed | `pyproject.toml`, `uv.lock` |
| Dependabot group | `uv-minor-patch` (grouped update, 12 members) |

---

## Package Update Table

All twelve members of the group. Semver class is computed from the From→To pair in the PR body and confirmed against the `uv.lock` resolved `version =` lines.

| # | Package | Old | New | Semver class | Direct / Transitive | Runtime-critical? |
|---|---------|-----|-----|--------------|---------------------|-------------------|
| 1 | tiktoken | 0.12.0 | 0.13.0 | minor (0.x) | Direct (runtime `dependencies`) | Yes — token counting / chunking (EN-026) |
| 2 | filelock | 3.28.0 | 3.29.4 | minor | Direct (runtime + dev) | Moderate — file locking |
| 3 | markdown-it-py | 4.0.0 | 4.2.0 | minor | Direct (runtime, pinned `<5.0.0`) | Yes — markdown parsing |
| 4 | mdit-py-plugins | 0.5.0 | 0.6.1 | minor (0.x) | Direct (runtime) | Yes — markdown plugin layer |
| 5 | requests | 2.33.1 | 2.34.2 | minor | Direct (runtime) | Yes — HTTP client |
| 6 | pymdown-extensions | 10.21.2 | 10.21.3 | patch | Direct (runtime) | Moderate — markdown extensions |
| 7 | ruff | 0.15.11 | 0.15.18 | patch (0.15.x) | Direct (dev + dependency-groups.dev) | Yes — lint/format tooling |
| 8 | pytest | 9.0.3 | 9.1.1 | minor | Direct (test + dependency-groups.dev) | Yes — test framework |
| 9 | bump-my-version | 1.3.0 | 1.4.1 | minor | Direct (dependency-groups.dev) | Release tooling only |
| 10 | pip-audit | 2.10.0 | 2.10.1 | patch | Direct (dependency-groups.dev) | Security tooling |
| 11 | pre-commit | 4.5.1 | 4.6.0 | minor | Direct (dependency-groups.dev) | Dev tooling |
| 12 | pyright | 1.1.408 | 1.1.410 | patch | Direct (dependency-groups.dev) | Yes — active type checker |

> **MAJOR bumps: NONE.** Every change is minor or patch. (`tiktoken` 0.12→0.13 and `mdit-py-plugins` 0.5→0.6 are minor under 0.x semver, where minor *can* carry breaking changes — analyzed below and found benign for this repo.)

---

## Declared-Constraint (pyproject.toml) Changes

Source: `gh pr diff 300 -- pyproject.toml`. The constraint **floors** change as follows. Note several floors jump further than the group "From" version (dependabot raised the minimum to the resolved version):

```
[project] dependencies:
  tiktoken            >=0.5.0      -> >=0.13.0     # floor raised well past old 0.12.0
  filelock            >=3.28.0     -> >=3.29.4
  markdown-it-py      >=4.0.0,<5.0.0 -> >=4.2.0,<5.0.0   # upper cap <5.0.0 preserved
  mdit-py-plugins     >=0.4.0      -> >=0.6.1      # floor raised past old 0.5.0
  requests            >=2.33.1     -> >=2.34.2
  pymdown-extensions  >=10.21.2    -> >=10.21.3

[project.optional-dependencies] dev:
  ruff                >=0.15.11    -> >=0.15.18
  filelock            >=3.28.0     -> >=3.29.4

[project.optional-dependencies] test:
  pytest              >=8.0.0      -> >=9.1.1      # large floor jump (8.0.0 -> 9.1.1)

[dependency-groups] dev:
  bump-my-version     >=1.2.7      -> >=1.4.1
  pip-audit           >=2.10.0     -> >=2.10.1
  pre-commit          >=4.5.1      -> >=4.6.0
  pyright             >=1.1.408    -> >=1.1.410
  pytest              >=9.0.3      -> >=9.1.1
  ruff                >=0.15.11    -> >=0.15.18
```

Unchanged floors of note: `mypy>=1.20.1` (not bumped; pyright is the active checker), `pytest-archon>=0.0.6`, `pytest-bdd>=8.0.0`, `pytest-cov>=7.1.0` (no pytest **plugin** versions changed — only pytest core), `mdformat>=1.0.0,<2.0.0`, `pygments>=2.19.3`.

---

## Transitive Lock Churn (uv.lock)

These changes appear in `uv.lock` but are **NOT** in the 12-package PR table — they are second-order effects. Source: `gh pr diff 300` uv.lock hunks.

| Transitive change | Old | New | Driver | Risk |
|-------------------|-----|-----|--------|------|
| `httpx` → **`httpx2`** (package rename/successor) | 0.28.1 | 2.4.0 | `bump-my-version` 1.4.1 switched dep `{ name = "httpx" }` → `{ name = "httpx2" }` | Low (dev-only tool) |
| `httpcore` → **`httpcore2`** | 1.0.9 | 2.4.0 | Pulled by httpx2 | Low |
| **`truststore`** (new package) | — | 0.10.4 | New dep of httpx2/httpcore2 (SSL verification) | Low |
| `idna` | 3.11 | 3.18 | Re-resolved by httpx2 tree | Low |
| `certifi` | dropped from httpx2/httpcore2 dep lists | — | httpx2 uses `truststore` instead | Low |

**What `httpx2` is (verified):** Per PyPI (`pypi.org/project/httpx2`), httpx2 is **not a hostile fork** — it is the maintained continuation of `httpx`: "Pydantic is picking up stewardship under the HTTPX2 name so that users have a reliably maintained path forward." Owner: Pydantic; Author: Tom Christie; Maintainer: Pydantic Services Inc. v2.4.0 (2026-06-11) added `HTTPXDeprecationWarning`, capped chained content-encoding decoders at 5, and fixed digest-auth / IDNA decoding. It depends on httpcore2 + truststore + anyio + idna.

**Why the blast radius is small:** The only package that pulls `httpx2` into the tree is `bump-my-version` (release-version tooling). It is declared in `[dependency-groups] dev`, is **not** in `[project] dependencies`, and is **not** imported by `src/` or by the test suite. It executes only during version-bump operations. `requests` (not httpx) remains the runtime/test HTTP client and is unaffected by the httpx2 swap.

---

## Flagged Packages — Real Release Notes

Per task instructions, every MAJOR bump (none here) and every tooling/runtime-critical package is examined against its actual upstream changelog/release notes covering the old→new range.

### ruff 0.15.11 → 0.15.18 (lint/format — FLAGGED) — coordination with PR #299
Source: `github.com/astral-sh/ruff/releases`. Six patch releases (0.15.12–0.15.18).
- **No default-rule enablements, no formatter behavior shifts, no breaking changes** affecting existing projects across the entire range.
- New rules added in the window (`AIR202`, `RUF074`, `RUF075`, `ASYNC119`, `PLW0717`) are **preview-only / not enabled by default** — they will not fire under this repo's `[tool.ruff.lint]` config without opting into preview.
- 0.15.17: `UP007`/`UP045` can now auto-add `from __future__ import annotations` — relevant only if those rules are enabled with `--fix`.
- 0.15.18: `PYI033` renamed to `legacy-type-comment` (cosmetic rule rename).
- **Verdict: benign.** Static Analysis CI job passes.

### pytest 9.0.3 → 9.1.1 (test framework — FLAGGED)
Source: `github.com/pytest-dev/pytest/releases/tag/9.1.0`.
- **One behavior change:** with `--doctest-modules`, inline autouse fixtures (module/package/session scope defined *inside* test modules, not conftest/plugins) "will now possibly execute twice." Mitigation: move such fixtures to `conftest.py`.
- **Deprecations (warnings now, removal in pytest 10 — not breaking yet):** class-scoped fixtures as instance methods without `@classmethod`; `request.getfixturevalue()` for not-already-requested fixtures during teardown; non-Collection iterables in `parametrize`; private `config.inicfg`; `baseid`/`nodeid` params; hook config via markers; `--pastebin`; `pytest.console_main`.
- New features (additive): `pytest.register_fixture()`, `--max-warnings`, `assertion_text_diff_style`, datetime/timedelta in `pytest.approx`.
- **Verdict: low risk.** Deprecations may add warnings but do not fail tests; all 9 matrix jobs pass. Declared test-extra floor jumps `>=8.0.0`→`>=9.1.1` (consistent with the dependency-groups.dev floor; no pre-9 install path remains).

### pytest plugins (pytest-archon, pytest-bdd, pytest-cov) — UNCHANGED
Confirmed: no `pytest-*` version lines changed in the diff. Only pytest core moved.

### pyright 1.1.408 → 1.1.410 (active type checker — FLAGGED)
Source: `github.com/RobertCraigie/pyright-python/releases`. Release bodies are auto-generated titles only ("Pyright NPM Package update to 1.1.410", "...1.1.409 Update Version") with **no published behavioral changelog** on the pyright-python side; these are thin wrappers around bundled pyright NPM versions 1.1.409 and 1.1.410. Two patch increments of the upstream pyright binary. Possible (undocumented) new diagnostics are the only theoretical risk. **Verdict: low risk** — Static Analysis CI job passes, indicating no new type errors surfaced on this codebase.

### requests 2.33.1 → 2.34.2 (runtime HTTP — FLAGGED)
Source: `github.com/psf/requests/blob/main/HISTORY.md`.
- 2.34.0: inline type annotations replace typeshed; Python 3.14/3.15b1 support; **security:** digest auth hashing now passes `usedforsecurity=False`; fixed `Response.history` self-reference loop; fixed greedy `no_proxy` domain matching; fixed duplicate-leading-slash URI stripping (needs urllib3 ≥2.7.0).
- 2.34.1: widened/narrowed several **type annotations** (json input, headers, `Response.reason` → `str`).
- 2.34.2: the changelog labels a "Breaking Change," but it is **type-annotation only** — `headers` input type moved back to `Mapping` to avoid `MutableMapping` invariance issues. Callers using `Request.headers.update()` may need annotation tweaks; **no runtime behavior change.**
- **Verdict: low runtime risk** (mostly typing + a security hardening).

### markdown-it-py 4.0.0 → 4.2.0 (runtime markdown parser — FLAGGED)
Source: `github.com/executablebooks/markdown-it-py/blob/master/CHANGELOG.md`.
- 4.1.0: new `gfm-like2` preset, plugin inline-terminator registration, CLI `--stdin`, quadratic-complexity fix in `fragments_join`/`text_join`. **No breaking changes.**
- 4.2.0: added `make_fence_rule()` factory. **No breaking changes / no parsing-behavior changes.**
- Upper cap `<5.0.0` preserved, so no accidental v5 jump. **Verdict: benign.**

### mdit-py-plugins 0.5.0 → 0.6.1 (runtime markdown plugins — FLAGGED, 0.x minor)
Source: `github.com/executablebooks/mdit-py-plugins/blob/master/CHANGELOG.md`.
- 0.6.0: new additive plugins (GFM autolink, composite GFM, superscript); **requires markdown-it-py ≥4.1.0** (satisfied — markdown-it-py goes to 4.2.0 in the same PR). **No breaking changes documented.**
- 0.6.1: bug fix — field lists inside indented containers no longer nest recursively (regression fix; output now correct siblings).
- **Verdict: benign**, and the co-bump satisfies the new ≥4.1.0 requirement.

### bump-my-version 1.3.0 → 1.4.1 (release tooling — FLAGGED for the httpx2 swap)
Source: `github.com/callowayproject/bump-my-version/releases`.
- 1.4.0: "Update tests to mock `httpx2` instead of `httpx` for download URL functionality" (this is the source of the transitive httpx→httpx2 swap). **Security-relevant default change:** "Disable shell hooks in configuration defaults and models" (#407). No documented breaking changes to config format, CLI, or bump behavior.
- 1.4.1: patch on top of 1.4.0.
- **Verdict: low risk**; the changed default (shell hooks off) is a hardening, and this repo uses `bump-my-version` for multi-file version sync (per `[tool.commitizen]` comment in pyproject) — not shell-hook-dependent.

### pip-audit 2.10.0 → 2.10.1 (security tooling — FLAGGED)
Source: `github.com/pypa/pip-audit/blob/main/CHANGELOG.md`. `[2.10.1]` — bug-fix only: fixes a `KeyError` crash when an OSV record's `affected` entry omits the optional `ranges` field. **No dependency, CLI, or breaking changes.** **Verdict: pure bug fix.**

### pre-commit 4.5.1 → 4.6.0 (dev tooling — FLAGGED)
Source: `github.com/pre-commit/pre-commit/blob/main/CHANGELOG.md`. `4.6.0` — feature: `--hook-dir` becomes optional in `pre-commit hook-impl` (git 2.54+ integration); fix keeping `--hook-type` required. **No breaking changes.** **Verdict: benign.**

### tiktoken 0.12.0 → 0.13.0 (runtime token counting — FLAGGED, 0.x minor)
Source: PR body changelog (sourced from tiktoken's CHANGELOG). v0.13.0: fancy-regex perf update; "branch byte pair encoding to fix performance on unusual input"; "Fix AttributeError caused by incomplete redaction of experimental code"; pyo3 and optional `blobfile` version updates. These are perf/internal fixes — **no API or encoding-output changes** that would alter token counts. **Verdict: benign.**

---

## Critical Coordination Check: ruff & commitizen

This is the explicit cross-PR consistency check requested.

| Package (Python dist) | In PR #300 group? | Version in #300 | Related separate PR | Action |
|-----------------------|-------------------|-----------------|---------------------|--------|
| **ruff** | **YES** | `0.15.11` → **`0.15.18`** | **PR #299** bumps the ruff **pre-commit hook** | Confirm #299 pins the ruff hook `rev` to **v0.15.18** so the pre-commit hook and the `pyproject.toml`/`uv.lock` ruff match. A mismatch (e.g. #299 lands a different rev) would mean `pre-commit run ruff` and `uv run ruff` use different binaries — inconsistent lint/format results. |
| **commitizen** | **NO** | n/a (not bumped here) | **PR #291** bumps the commitizen **pre-commit hook** | No coordination needed *from #300* — commitizen is not a Python dependency in this repo's resolved tree for the group bump (it is configured under `[tool.commitizen]` for commit-message linting via the pre-commit hook only; version bumping is handled by `bump-my-version`, per the in-file comment). #291 can be evaluated independently. |

**Exact ruff version to cross-check against #299:** `ruff 0.15.18` (sdist `ruff-0.15.18.tar.gz`, sha256 `2698a964c70e8bf402dcb99c8810472d270d141e7aa8c4e13599fd52033a2f33`, upload-time 2026-06-18). The pre-commit hook `rev` in #299 should equal **v0.15.18** for consistency.

---

## CI Status

Source: `gh pr checks 300`.

| Check | Result | Notes |
|-------|--------|-------|
| CI Success | **fail** (3s) | Aggregate/gate job — fails fast (3s); not a test failure. Under separate investigation. |
| Security Scan | **fail** (25s) | Separate security workflow; not caused by these version bumps per the dependency analysis. Under separate investigation. |
| Static Analysis | pass | ruff + pyright clean on new versions |
| CLI Integration Tests | pass | |
| Changelog Entry | pass | |
| Plugin Validation | pass | |
| Validation Checks | pass | |
| Test uv (Python 3.11, ubuntu) | **pass** | |
| Test uv (Python 3.12, ubuntu) | **pass** | |
| Test uv (Python 3.13, ubuntu / macos / windows) | **pass** | |
| Test uv (Python 3.14, ubuntu / macos / windows) | **pass** | |

**Determination:** Every `Test uv (...)` matrix job passes across Python 3.11–3.14 on Linux/macOS/Windows. **The dependency changes themselves caused no test failure.** The `CI Success` (3s) and `Security Scan` (25s) failures are independent of the dependency upgrades (the test matrix that actually exercises the upgraded packages is green) and are being handled by another agent. The 3-second `CI Success` failure time strongly indicates a gating/orchestration job failing on a non-test condition rather than a code/test regression from the bumps.

---

## Risk Verdict

**LOW.**

All twelve updates are minor/patch with **no MAJOR bumps** and **no documented breaking changes that affect this repository**. Runtime-facing direct dependencies (`tiktoken`, `markdown-it-py`, `mdit-py-plugins`, `requests`, `pymdown-extensions`, `filelock`) carry only additive features, perf fixes, type-annotation changes, and one self-consistent co-bump (`mdit-py-plugins` 0.6.x's new ≥markdown-it-py 4.1.0 requirement is satisfied by the same PR). The lone eyebrow-raiser — the transitive `httpx → httpx2` / `httpcore → httpcore2` / new `truststore` swap — is driven solely by `bump-my-version` (release-only dev tooling, not imported by `src/` or tests), and `httpx2` is the **legitimate Pydantic-stewarded continuation** of httpx, so its impact is confined to local version-bump operations. The complete `Test uv` matrix passes on Python 3.11–3.14 across three OSes, empirically confirming the upgrades do not break the build, tests, or runtime. The failing `CI Success` and `Security Scan` checks are non-test gating jobs unrelated to these version changes (separately investigated).

### Pre-merge cautions
1. **ruff/#299 consistency (primary):** Before/at merge, confirm PR #299 pins the ruff **pre-commit hook `rev` to v0.15.18** to match `pyproject.toml`/`uv.lock`. If #299 targets a different rev, align them so hook-based and `uv run` ruff produce identical results.
2. **CI Success + Security Scan gates:** Do not merge until the separately-investigated `CI Success` and `Security Scan` failures are explained/cleared — they are merge-blocking gates even though they are not test regressions from these bumps.
3. **`bump-my-version` shell-hook default:** 1.4.0 disabled shell hooks in config defaults. If any local release workflow relied on bump-my-version shell hooks, re-verify the release/version-bump path once (this repo's usage is multi-file version sync, which is unaffected).
4. **pytest 9.1 deprecations:** Expect possible new deprecation warnings (class-scoped fixtures without `@classmethod`, `parametrize` with generators, etc.). Non-blocking now, but worth a follow-up cleanup before pytest 10 removes them. Also note the `--doctest-modules` double-execution behavior change if doctests are added later.
5. **commitizen (#291):** Independent — no coordination required from #300; commitizen is not part of this group's resolved dependency set.

---

## Evidence Index

| Claim area | Source |
|------------|--------|
| 12-package table, From→To | `gh pr view 300 --json body` (dependabot-generated table) |
| Declared-constraint floor edits | `gh pr diff 300 -- pyproject.toml` |
| Resolved versions + transitive swap (httpx2/httpcore2/truststore/idna), driver = bump-my-version | `gh pr diff 300` (uv.lock hunks); bump-my-version block shows `{ name = "httpx" }` → `{ name = "httpx2" }` |
| ruff 0.15.12–0.15.18 notes | `github.com/astral-sh/ruff/releases` |
| pytest 9.1.0 notes | `github.com/pytest-dev/pytest/releases/tag/9.1.0` |
| requests 2.34.0–2.34.2 notes | `github.com/psf/requests/blob/main/HISTORY.md` |
| markdown-it-py 4.1.0/4.2.0 | `github.com/executablebooks/markdown-it-py/blob/master/CHANGELOG.md` |
| mdit-py-plugins 0.6.0/0.6.1 | `github.com/executablebooks/mdit-py-plugins/blob/master/CHANGELOG.md` |
| bump-my-version 1.4.0 (httpx2 + shell-hook default) | `github.com/callowayproject/bump-my-version/releases` |
| pip-audit 2.10.1 | `github.com/pypa/pip-audit/blob/main/CHANGELOG.md` |
| pre-commit 4.6.0 | `github.com/pre-commit/pre-commit/blob/main/CHANGELOG.md` |
| pyright 1.1.409/1.1.410 (titles only) | `github.com/RobertCraigie/pyright-python/releases` |
| httpx2 identity (Pydantic stewardship) | `pypi.org/project/httpx2/` |
| tiktoken 0.13.0 | PR #300 body changelog (sourced from tiktoken CHANGELOG) |
| CI matrix vs. gates | `gh pr checks 300` |

---

*Analysis date: 2026-06-22. Analyst: release-engineering agent (read-only). No files modified, merged, or pushed.*
