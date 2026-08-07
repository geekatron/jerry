# Dependabot Merge Recommendation — 2026-06-22

> Consolidated, adversarially-verified recommendation for the 4 open dependabot PRs in `geekatron/jerry`.
> Produced via 3 parallel analysis agents + 1 adversarial verification agent (fresh-context pre-mortem + chain-of-verification).

## Document Sections

| Section | Purpose |
|---------|---------|
| [Bottom Line](#bottom-line) | The decision in three sentences |
| [PR Inventory](#pr-inventory) | The 4 PRs, what they touch, risk |
| [Recommended Merge Order](#recommended-merge-order) | Order + rationale |
| [Safe-to-Merge vs. CI-Green](#safe-to-merge-vs-ci-green) | The critical distinction |
| [The Real Blocker](#the-real-blocker) | Why everything is BLOCKED |
| [Post-Merge Actions](#post-merge-actions) | Dry-run + follow-up bugs |
| [Evidence / Provenance](#evidence--provenance) | Source agent reports |

---

## Bottom Line

All **4 dependabot PRs are safe to merge** — zero major bumps, no merge conflicts (proven with `git merge-tree`), and every substantive CI job passes (tests on Python 3.11–3.14 × Linux/macOS/Windows, static analysis, CLI/plugin/validation). The uniform red `Security Scan` / `CI Success` is **environmental** (advisory-DB drift: `pip-audit --strict` flagging pre-existing 2026 CVEs in the committed `uv.lock`), **not caused by any bump**, and is **not a required status check** — the actual gate is a required **code-owner review**. Merging these will **not** turn CI green; that needs a *separate* CVE-remediation PR.

---

## PR Inventory

| PR | Change | Files | Semver | Risk | Conflicts? |
|----|--------|-------|--------|------|-----------|
| **#298** | `astral-sh/setup-uv` action 8.1.0 → 8.2.0 | 5 workflow `.yml` (pinned-SHA bump, no logic) | minor | **LOW** | none |
| **#299** | `ruff-pre-commit` hook v0.15.11 → 0.15.18 | `.pre-commit-config.yaml` (line 42) | patch | **LOW** | none (≠ #291 line) |
| **#291** | `commitizen` hook 4.13.10 → 4.16.3 | `.pre-commit-config.yaml` (line 205) | minor | **LOW** | none (≠ #299 line) |
| **#300** | `uv-minor-patch` group, 12 Python deps | `pyproject.toml`, `uv.lock` | all minor/patch, **zero majors** | **LOW** | none |

**#300 group contents:** tiktoken, filelock, markdown-it-py, mdit-py-plugins, requests, pymdown-extensions, **ruff → 0.15.18**, pytest → 9.1.1, bump-my-version → 1.4.1, pip-audit, pre-commit, pyright. Notable transitive: `bump-my-version` 1.4.1 swaps `httpx → httpx2` (legitimate Pydantic-stewarded continuation; release-only tooling, not imported by `src/` or tests).

**Coordination note:** `ruff` is in both #300 (the package → 0.15.18) and #299 (the pre-commit hook → 0.15.18) — same version, so they stay consistent. `commitizen` is **not** in #300, so #291 is fully independent.

---

## Recommended Merge Order

**#298 → #299 → #291 → #300**

> Order is **not safety-critical** — the PRs are mutually independent (the only shared file, `.pre-commit-config.yaml`, is edited 163 lines apart by #299/#291, verified conflict-free in every ordering via `git merge-tree --write-tree` exit 0). The preference below is purely operational hygiene:

1. **#298** — pure CI-infra (workflow files), zero runtime impact. Get tooling current first.
2. **#299** — ruff hook, zero runtime impact (pre-commit runs in its own isolated env).
3. **#291** — commitizen hook, zero runtime impact, independent.
4. **#300** — the **only** PR that changes the installed/locked environment. Merge **last** so the lockfile change is the most-recent, easiest-to-revert-in-isolation commit if anything surfaces later.

> ⚠️ Rationale correction (from adversarial review): an earlier draft front-loaded #300 to "turn CI green." That rationale is **invalid** — #300 greens nothing (see below). Lockfile-last-for-revert is the correct rationale.

---

## Safe-to-Merge vs. CI-Green

These are **different** for this batch, and only the first is true.

- **Safe to merge (introduces no new breakage): YES** for all 4. Every real test/build job passes, including #300 with pytest 9.1.1 + ruff 0.15.18 active.
- **Turns CI green: NO.** #300 changes **none** of the CVE-flagged packages. Verified per-package (main `uv.lock` → #300 `uv.lock`):

  | Package | main → #300 | Status | Fixed in |
  |---------|-------------|--------|----------|
  | mako | 1.3.10 → 1.3.10 | **STILL VULNERABLE** | ≥ 1.3.12 |
  | urllib3 | 2.6.3 → 2.6.3 | **STILL VULNERABLE** | ≥ 2.7.0 |
  | msgpack | 1.1.2 → 1.1.2 | **STILL VULNERABLE** | ≥ 1.2.1 |
  | pydantic-settings | 2.13.1 → 2.13.1 | **STILL VULNERABLE** | ≥ 2.14.2 |
  | pip | 26.0 → 26.0 | **STILL VULNERABLE** | ≥ 26.1.2 |

  After merging all 4, `ci.yml`'s `security` job stays **RED** (≈9 vulns in 5 packages; the exact count drifts with the live advisory DB). **To green CI, file a separate PR** bumping the 5 packages to the fixed versions above. (Note: `main`'s CI was green at its last push 2026-04-21; the CVEs were published *after* that, so this is DB-drift, not a regression — `main` itself would go red if re-run today.)

---

## The Real Blocker

`main` is governed by a ruleset (rules: `deletion`, `non_fast_forward`, `pull_request`) with `required_status_checks: null`. So the red checks do **not** block. The `pull_request` rule requires:
- `required_approving_review_count: 1`
- `require_code_owner_review: true`

**That code-owner approval is why all 4 show `BLOCKED`.** Approve (as code owner) and merge — or admin-merge. The red X's are advisory, not gating.

---

## Post-Merge Actions

1. **Dry-run the release path after #300 merges.** The `httpx → httpx2` swap in `bump-my-version` only affects `release.yml` / `version-bump.yml`, which PR CI does not exercise. Trigger a `workflow_dispatch` dry-run to confirm.
2. **File: CVE-remediation PR** (greens CI) — bump mako ≥ 1.3.12, urllib3 ≥ 2.7.0, msgpack ≥ 1.2.1, pydantic-settings ≥ 2.14.2, pip ≥ 26.1.2.
3. **File: CI inconsistency bug** — the *scheduled* `security-scan.yml` runs `pip-audit` **without** a requirements file (audits effectively nothing — logs "Dependency not found on PyPI … jerry") and passes green, while `ci.yml`'s `security` job audits the real lockfile and goes red. A detection blind spot worth its own ticket. (Per H-32, both follow-ups need GitHub Issue + worktracker parity if actioned.)
4. **Watch (non-blocking):** pytest 9.1 emits new deprecation *warnings* (removal not until pytest 10).

---

## Evidence / Provenance

| Report | Scope |
|--------|-------|
| `PR-300-uv-group.md` | The 12-package group, per-package changelog review |
| `PR-299-291-precommit.md` | Pre-commit hooks, exact-line conflict analysis |
| `PR-298-and-ci-rootcause.md` | setup-uv + CI/Security-Scan root cause |
| `adversarial-review.md` | Fresh-context falsification of all claims + pre-mortem |

*Method: 3 parallel read-only analysis agents → consolidated synthesis → 1 adversarial verification agent (chain-of-verification + pre-mortem). All claims cite diffs, logs, `git merge-tree`, and `gh api` ruleset output.*
