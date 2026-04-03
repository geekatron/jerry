# BUG-003 Fix Review: UV_FROZEN=1 at Job Level

> eng-devsecops review of the one-line BUG-003 fix in `.github/workflows/version-bump.yml`.
> Reviewed: 2026-03-11
> File: `.github/workflows/version-bump.yml` lines 43–50

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Verdict and critical blockers |
| [L1 Technical Findings](#l1-technical-findings) | Per-question analysis with evidence |
| [L2 Strategic Implications](#l2-strategic-implications) | Residual risk and recommendation |

---

## L0 Executive Summary

**Verdict: CONDITIONAL PASS — one correctness risk, no blockers for the two commands that matter.**

The `UV_FROZEN: "1"` job-level env var correctly prevents `uv run` and `uv sync` from modifying `uv.lock`. Both commands that were the stated motivation for this fix (lines 125 and 193) are handled. Neither `uv tool install` nor `uv python install` are affected by `UV_FROZEN` — they do not read the project lockfile at all, so no breakage occurs. The one open question is whether `UV_FROZEN` is the right signal vs. `UV_LOCKED`; the fix uses the weaker of the two options, which is safe but does not provide the fail-fast guarantee `UV_LOCKED` would add. Job-level scope is correct.

---

## L1 Technical Findings

### Finding 1 — Does UV_FROZEN=1 prevent uv.lock modification for all uv subcommands?

**Status: YES for the commands that matter; N/A for the others.**

`UV_FROZEN` is the env-equivalent of `--frozen` (introduced in uv 0.4.25). Its documented behavior: "uv will run without updating the uv.lock file." The flag is explicitly accepted by:

- `uv sync` — skip lockfile staleness check, use existing lockfile as-is.
- `uv run` — same semantics; run the project command without re-resolving.
- `uv add` — skip lockfile update (not relevant here, not used in the workflow).

The workflow's two previously unflagged `uv run` calls (line 125: `uv run jerry ci detect-bump-type` and line 193: `uv run python scripts/sync_versions.py`) are now covered by the job-level env. The existing explicit `--frozen` on `uv sync` (lines 107 and 192) becomes redundant but harmless — the CLI flag and env var are additive and do not conflict.

**Residual concern:** `UV_FROZEN` uses the lockfile without checking whether it is current. If `uv.lock` itself drifts from `pyproject.toml` (e.g., a developer commits a pyproject.toml dependency change without running `uv lock`), CI silently installs a stale set of packages and does not fail. `UV_LOCKED` (env: `UV_LOCKED=1`) is the stricter alternative — it asserts that the lockfile is up-to-date and exits with an error if it is not. This is the fail-fast behavior that supply-chain hygiene prefers.

### Finding 2 — Does UV_FROZEN=1 break `uv tool install 'bump-my-version==1.2.7'`?

**Status: NO, no breakage.**

`uv tool install` manages tools in an isolated environment that is wholly separate from the project's `uv.lock`. The tool resolver reads PyPI (or the pinned version constraint) directly; it does not consult `uv.lock` at any point. `UV_FROZEN` is not documented as a flag for `uv tool install`, and community investigation (GitHub issue #5815) confirms the option is not wired into the tool install command. The isolated environment has no lockfile of its own to freeze or update.

**Practical test:** The fix has been in the workflow tree since the commit; if `uv tool install` were affected, the `bump-my-version==1.2.7` step would have failed. The exact version pin (`==1.2.7`) in the step also provides independent protection against supply-chain drift regardless of UV_FROZEN behavior.

### Finding 3 — Does UV_FROZEN=1 break `uv python install 3.14`?

**Status: NO, no breakage.**

`uv python install` downloads and registers a Python interpreter. It has no relationship to the project's `uv.lock` file — it does not resolve Python packages and does not perform dependency resolution. `UV_FROZEN` is a package-resolution concept; the Python installer subsystem ignores it entirely. There is no supported `--frozen` flag for `uv python install` in the CLI reference.

### Finding 4 — Is job-level env the right scope?

**Status: YES, job-level is correct. Step-level would be weaker.**

The problem this fix addresses is that `uv run` on lines 125 and 193 re-resolves the lockfile at the package resolution phase, which happens before the step's shell command body even executes. A step-level `env:` block is injected alongside the run command and is available to the process, so technically step-level would also work for a single step. However:

1. There are two affected `uv run` calls in different steps. Job-level covers both in one declaration.
2. Job-level is the minimal-scope setting that provides consistent lockfile protection for the entire job without requiring per-step auditing as new steps are added.
3. The comment in the workflow (lines 43–50) accurately documents why job-level was chosen over the original per-`uv sync` approach.

Step-level would be narrower and would require explicit annotation on every future `uv run` call added to the job — an error-prone maintenance burden. Job-level is the correct defensive choice here.

### Finding 5 — Any other uv commands affected?

**Inventory of all uv calls in the workflow:**

| Line | Command | UV_FROZEN applies? | Effect |
|------|---------|-------------------|--------|
| 83 | `uses: astral-sh/setup-uv@...` | Not a uv command — GitHub Action | None |
| 88 | `uv python install 3.14` | No (Python installer, not package resolver) | No effect |
| 94 | `uv tool install 'bump-my-version==1.2.7'` | No (isolated tool env, not project lock) | No effect |
| 107 | `uv sync --frozen` | Yes (redundant with env var, harmless) | Lockfile protected |
| 125 | `uv run jerry ci detect-bump-type --since-tag` | Yes (was missing --frozen before this fix) | Lockfile protected |
| 192 | `uv sync --frozen` | Yes (redundant, harmless) | Lockfile protected |
| 193 | `uv run python scripts/sync_versions.py --check` | Yes (was missing --frozen before this fix) | Lockfile protected |

No uv calls are broken. The `--frozen` flags on lines 107 and 192 are now redundant but cause no harm. They can be removed for clarity in a follow-up cleanup, or left in place as explicit documentation.

---

## L2 Strategic Implications

### Recommendation: Consider upgrading to UV_LOCKED=1

The current fix uses `UV_FROZEN` (permissive: use lockfile as-is, no validation). The stronger equivalent is `UV_LOCKED` (assertive: fail if lockfile is stale). For a CI pipeline that enforces `allow_dirty = false` and uses supply-chain controls like pinned tool versions, `UV_LOCKED` is the more appropriate signal:

- If a developer commits `pyproject.toml` changes without regenerating `uv.lock`, `UV_LOCKED` fails CI loudly. `UV_FROZEN` silently installs the stale environment.
- `UV_LOCKED` aligns with the spirit of the "Ensure clean working tree" guard already in the workflow (lines 138–148).
- The downside: `UV_LOCKED` requires that the lockfile be fully consistent with pyproject.toml before the job runs. This is already the expectation for any commit reaching `main`.

**Suggested change:** Replace `UV_FROZEN: "1"` with `UV_LOCKED: "1"` at the job level. Then remove the now-redundant `--frozen` flags from the two `uv sync` calls for cleanliness. This gives the workflow fail-fast semantics rather than silent-degrade semantics.

### Explicit --frozen flags on uv sync

Lines 107 and 192 each pass `--frozen` explicitly. With `UV_FROZEN: "1"` at job level, these are now redundant. They can remain as belt-and-suspenders documentation or be pruned. If the recommendation above is accepted (switch to `UV_LOCKED`), the explicit `--locked` flag on those two `uv sync` calls would similarly be redundant but readable.

### No false-positive risk from job-level scope

`uv python install` and `uv tool install` are structurally isolated from the project lockfile. Setting `UV_FROZEN` or `UV_LOCKED` at job level does not risk breaking these steps now or in any plausible future uv version, because the concept of "project lockfile" does not exist in the tool/python installer subsystems.

---

## Summary Table

| Review Question | Finding | Severity |
|----------------|---------|----------|
| Does UV_FROZEN cover uv sync and uv run? | Yes — both covered | PASS |
| Does it break uv tool install? | No — isolated env, unaffected | PASS |
| Does it break uv python install? | No — Python installer, unaffected | PASS |
| Is job-level scope correct? | Yes — preferred over step-level | PASS |
| Any other uv commands affected? | No undocumented interactions found | PASS |
| UV_FROZEN vs UV_LOCKED | UV_FROZEN is safe but weaker; UV_LOCKED preferred for CI | INFO |

---

*Agent: eng-devsecops | Project: PROJ-030-bugs | Standard: NIST SSDF PS.1, DevSecOps pipeline hygiene*
