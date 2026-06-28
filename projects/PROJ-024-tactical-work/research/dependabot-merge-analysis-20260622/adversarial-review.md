# Adversarial Review — Dependabot Merge Plan (PRs #298/#300/#299/#291)

> Independent adversarial verification (devil's advocate + pre-mortem + chain-of-verification). READ-ONLY. Goal: falsify the plan's claims and surface anything that could break `main`. All findings cite concrete evidence (API output, diff lines, CI log lines, version numbers) gathered 2026-06-22.

## Navigation

| Section | Purpose |
|---------|---------|
| [Verdict Summary](#verdict-summary) | C1-C5 verdicts at a glance |
| [C1 — No Merge Conflicts](#c1--no-merge-conflicts) | Conflict simulation evidence |
| [C2 — Branch Protection](#c2--branch-protection) | What actually governs merge |
| [C3 — Red CI is Environmental](#c3--red-ci-is-environmental) | Refutation of stated form + confirmed conclusion |
| [C4 — No New Failures](#c4--no-new-failures) | Per-PR job status |
| [C5 — Does #300 Move CI Toward Green?](#c5--does-300-move-ci-toward-green) | Per-package FIXED/STILL-VULNERABLE resolution |
| [Pre-Mortem](#pre-mortem) | Top failure modes + mitigation status |
| [Final Verdict](#final-verdict) | Safe-to-merge vs turns-CI-green |
| [Evidence Appendix](#evidence-appendix) | Raw commands and outputs |

---

## Verdict Summary

| Claim | Verdict | One-line basis |
|-------|---------|----------------|
| C1 No merge conflicts among the 4 | **CONFIRMED** | `git merge-tree --write-tree` exits 0 for main+#299, main+#291, and sequential (main+#299)+#291. #299 edits line 42, #291 edits line 205; 163 lines apart. |
| C2 Branch protection = review only, no required status checks | **CONFIRMED (with correction)** | Ruleset has only `deletion`, `non_fast_forward`, `pull_request`. NO `required_status_checks`. BUT requires `required_approving_review_count: 1` AND `require_code_owner_review: true`. Red CI does not block; a CODEOWNER review does. |
| C3 Red CI is pre-existing CVEs already failing on main's lockfile | **REFUTED as stated / CONFIRMED in conclusion** | The vulnerable versions ARE on main, and the bumps neither cause nor fix them. BUT main's own ci.yml Security Scan was GREEN ("No known vulnerabilities found") at HEAD 750af52d. The red is **time-driven advisory-DB drift** (CVEs published after main last ran CI on 2026-04-21), not "already-failing-on-main." |
| C4 Merging all 4 introduces no new test/build failures | **CONFIRMED** | On every PR, only `Security Scan` + `CI Success` fail. All `Test uv` (3.11-3.14 x ubuntu/macos/windows), Static Analysis, CLI Integration, Plugin Validation, Validation, Changelog all pass. |
| C5 Merging #300 reduces CVE count / moves CI toward green | **REFUTED** | #300's uv.lock does NOT change any of the 5 flagged packages (mako, urllib3, msgpack, pydantic-settings, pip). After merging #300 (and all 4), ci.yml Security Scan stays **RED with the same 9 vulns in 5 packages**. |

---

## C1 — No Merge Conflicts

**Verdict: CONFIRMED.**

The only shared file is `.pre-commit-config.yaml` (#299 and #291). Both PRs branch from the identical base commit:

```
merge-base #299 vs main: 750af52d033d
merge-base #291 vs main: 750af52d033d
main HEAD:               750af52d033d
```

Diffs touch non-overlapping stanzas:
- **#299** (ruff): hunk `@@ -39,7 +39,7 @@`, changes the `rev:` on line 42 (`d1b833175... # v0.15.11` -> `77039ccbba... # v0.15.18`).
- **#291** (commitizen): hunk `@@ -202,7 +202,7 @@`, changes the `rev:` on line 205 (`b5d5040f7... # v4.13.10` -> `286da5488... # v4.16.3`).

163 lines apart. Definitive conflict simulation (modern git merge-tree):

```
main+#299 merge-tree exit: 0           (clean)
main+#291 merge-tree exit: 0           (clean)
(#299-merged-tree) + #291 exit: 0      (clean, sequential)  <- no CONFLICT markers
```

The sequential test (merge #299, then merge #291 against the resulting tree) is the realistic case and it is clean. #298 (workflow files) and #300 (pyproject.toml + uv.lock) share no files with any other PR.

**Falsification attempt:** I tried to find a conflict by merging #291 against the post-#299 tree rather than against bare main. Still exit 0. No conflict exists.

---

## C2 — Branch Protection

**Verdict: CONFIRMED, with a material correction the plan omits.**

`gh api repos/geekatron/jerry/rules/branches/main` returns three rule types only:

```json
["deletion", "non_fast_forward", "pull_request"]
```

The `pull_request` rule parameters:

```json
{
  "required_approving_review_count": 1,
  "dismiss_stale_reviews_on_push": false,
  "require_code_owner_review": true,
  "require_last_push_approval": false,
  "required_review_thread_resolution": false,
  "allowed_merge_methods": ["merge", "squash", "rebase"]
}
```

`gh api repos/geekatron/jerry/branches/main/protection` returns 404 (no classic branch protection; the repo uses rulesets).

**What governs merge:**
- There is **NO `required_status_checks` rule** -> red CI ("Security Scan" / "CI Success") does **NOT** block merge. The plan's C2 premise holds.
- **HOWEVER**, merge requires **1 approving review AND a CODEOWNERS review** (`require_code_owner_review: true`). The plan describes C2 as "REVIEW only"; that is correct but understates that a *code-owner* approval is mandatory. Dependabot cannot self-approve; a human code owner must approve each of the 4 PRs. This is the real gate, not CI.

**Implication:** "Red CI does not block merge" is TRUE. But these PRs are `mergeStateStatus: BLOCKED` today precisely because the required review has not been granted, not because of CI. Anyone executing the plan needs code-owner approval rights (or admin override).

---

## C3 — Red CI is Environmental

**Verdict: REFUTED as literally stated; CONFIRMED in its operative conclusion.**

The plan's C3 claims the red is `pip-audit --strict` flagging "pre-existing 2026 CVEs already in main's committed uv.lock ... NOT caused by the bumps" and asks me to "confirm the same CVEs are present on main's uv.lock."

**What is TRUE:**
1. The failing job is the `security` job in **`.github/workflows/ci.yml`** (NOT `security-scan.yml`, which is schedule-only). It runs:
   ```
   uv sync --frozen
   uv export --no-hashes --frozen --all-extras --no-emit-project > /tmp/requirements.txt
   uv run pip-audit --requirement /tmp/requirements.txt --strict --desc
   ```
2. The vulnerable versions ARE committed on main's uv.lock (verified from `origin/main:uv.lock`):
   `mako 1.3.10`, `urllib3 2.6.3`, `msgpack 1.1.2`, `pydantic-settings 2.13.1`, `pip 26.0`.
3. The bumps do NOT introduce these CVEs (#299/#291 touch only `.pre-commit-config.yaml`; #298 touches only workflow SHAs; #300 does not change any of the 5 flagged packages — see C5).
4. "CI Success" is a pure aggregator gate. Its script is `if [[ "$security" != "success" ]] ...; then echo "One or more jobs failed"`, with `security: failure` as the sole failing input. It fails in ~3s, not from any test/build regression.

**What is FALSE (the falsification):** The phrase "pre-existing CVEs already in main's committed uv.lock [failing]" implies main itself is/was red on these CVEs. It was **not**. Main's own ci.yml `security` job, at current HEAD `750af52d` (run 24699012054, job 72237998434, 2026-04-21), reported **"No known vulnerabilities found"** and the run conclusion was **success** (Security Scan: success, CI Success: success).

The CVEs (CVE-2026-44307 mako, PYSEC-2026-142/141 urllib3, GHSA-6v7p-g79w-8964 msgpack, GHSA-4xgf-cpjx-pc3j pydantic-settings, PYSEC-2026-196/CVE-2026-3219/CVE-2026-6357 pip) were **published into the advisory database between 2026-04-21 (main's last CI) and 2026-06-22 (today's PR CI)**. The red is therefore **time-driven advisory-DB drift against a static lockfile** — not a state where main was already failing.

**Practical consequence (why it still doesn't matter for "safe to merge"):** If `main`'s ci.yml were re-run today, it would also go red on the identical 9 vulns. So the red is genuinely independent of the 4 PRs. The conclusion "not caused by the bumps" is CONFIRMED; the mechanism is DB drift, not committed-and-already-failing.

**One more reconciliation (important nuance):** Today's *scheduled* scan (`security-scan.yml`, run 27938639670, 2026-06-22 08:14) installed the SAME versions (`mako==1.3.10`, `urllib3==2.6.3`, `msgpack==1.1.2`, `pydantic-settings==2.13.1`, `pip==26.0`) yet reported **"No known vulnerabilities found"** and exited 0. The difference is the invocation: scheduled runs `pip-audit --strict` against the *installed environment*; the PR's ci.yml runs `pip-audit --requirement requirements.txt --strict` against the *exported requirements file*. The two modes disagree TODAY on identical versions. This means: (a) the ci.yml red is real and reproducible for PRs, and (b) there is a latent CI inconsistency (two security jobs giving opposite results on the same lockfile) worth a follow-up — but it is orthogonal to merging these 4 PRs.

---

## C4 — No New Failures

**Verdict: CONFIRMED.**

`gh pr checks` for all four PRs shows an identical pattern: exactly two red checks (`CI Success`, `Security Scan`) and everything else green. Representative (#300):

| Check | Result |
|-------|--------|
| CI Success | fail (3s, aggregator) |
| Security Scan | fail (25s, pip-audit) |
| CLI Integration Tests | pass |
| Changelog Entry | pass |
| Plugin Validation | pass |
| Static Analysis | pass |
| Test uv (3.11/3.12/3.13/3.14 x ubuntu/macos/windows) | **9/9 pass** |
| Validation Checks | pass |

For #300 specifically — the only PR that changes runtime/test dependencies — the full `Test uv` matrix passes with **pytest 9.1.1** and **ruff 0.15.18** active, empirically demonstrating the upgrades do not break tests or static analysis. #298 (workflow SHA bump) and #299/#291 (single-line pre-commit rev bumps) cannot affect runtime; their `Test uv` jobs pass too. No substantive job regresses on any PR.

**Falsification attempt:** I checked whether the pytest 9.x or ruff 0.15.18 bump in #300 produced any test/static-analysis failure. It did not — Static Analysis and all 9 matrix jobs are green.

---

## C5 — Does #300 Move CI Toward Green?

**Verdict: REFUTED. Merging #300 does NOT reduce the CVE count and does NOT move CI toward green.**

### Per-package resolution (main vs #300 head vs CVE-fixed version)

Versions read directly from `origin/main:uv.lock` and `<#300 head>:uv.lock`. Fix versions from the pip-audit output captured in #300's own CI run (job 82622250086).

| Package | main uv.lock | #300 uv.lock | Changed by #300? | Fix version (advisory) | In #300's audit table? | Status after #300 |
|---------|-------------|--------------|------------------|------------------------|------------------------|-------------------|
| mako | 1.3.10 | 1.3.10 | **No** | 1.3.12 (CVE-2026-44307) | YES | **STILL VULNERABLE** |
| urllib3 | 2.6.3 | 2.6.3 | **No** | 2.7.0 (PYSEC-2026-142, PYSEC-2026-141) | YES (x2) | **STILL VULNERABLE** |
| msgpack | 1.1.2 | 1.1.2 | **No** | 1.2.1 (GHSA-6v7p-g79w-8964) | YES | **STILL VULNERABLE** |
| pydantic-settings | 2.13.1 | 2.13.1 | **No** | 2.14.2 (GHSA-4xgf-cpjx-pc3j) | YES | **STILL VULNERABLE** |
| pip | 26.0 | 26.0 | **No** | 26.1 / 26.1.2 (PYSEC-2026-196, CVE-2026-3219, CVE-2026-6357) | YES (x3) | **STILL VULNERABLE** |
| idna | 3.11 | **3.18** | Yes (bumped) | n/a — not flagged | NO | not vulnerable (no remediation needed) |
| pymdown-extensions | 10.21.2 | **10.21.3** | Yes (bumped) | n/a — not flagged | NO | not vulnerable (no remediation needed) |

Key correction to the prompt's premise: the prompt lists **idna and pymdown-extensions** as CVE-affected. They are **NOT** in pip-audit's 9-vuln table on either main or #300. #300 does bump them (idna 3.11->3.18, pymdown-extensions 10.21.2->10.21.3), but that is incidental — no advisory applies to them in this audit.

### What #300 actually changes (full list, from `git diff --text origin/main <head> -- uv.lock`)

bump-my-version 1.3.0->1.4.1, filelock 3.28.0->3.29.4, **httpcore->httpcore2 2.4.0** (rename), **httpx->httpx2 2.4.0** (rename), idna 3.11->3.18, markdown-it-py 4.0.0->4.2.0, mdit-py-plugins 0.5.0->0.6.1, pip-audit 2.10.0->2.10.1, pre-commit 4.5.1->4.6.0, pymdown-extensions 10.21.2->10.21.3, pyright 1.1.408->1.1.410, pytest 9.0.3->9.1.1, requests 2.33.1->2.34.2, ruff 0.15.11->0.15.18, tiktoken 0.12.0->0.13.0, +truststore 0.10.4 (new).

**None of the 5 flagged packages appear in this list.**

### CONCLUSION (GREEN vs RED after merge)

After merging **#300 alone**, the ci.yml `security` job audits a lockfile that still contains mako 1.3.10, urllib3 2.6.3, msgpack 1.1.2, pydantic-settings 2.13.1, pip 26.0 -> **STILL RED, "Found 9 known vulnerabilities in 5 packages"** (this is literally already what #300's own CI run reported: job 82622250086 -> `Found 9 known vulnerabilities in 5 packages`, exit code 1).

After merging **all 4** (#298 workflow SHAs, #299 ruff hook, #291 commitizen hook — none touch Python deps), the security audit set is unchanged from #300's -> **STILL RED, 9 vulns in 5 packages, exactly 9 remaining.**

**Number of CVEs remaining after all 4 merges: 9 (across 5 packages). Zero are remediated by any of the 4 PRs.**

To turn the ci.yml security job green requires a SEPARATE change bumping: mako >= 1.3.12, urllib3 >= 2.7.0, msgpack >= 1.2.1, pydantic-settings >= 2.14.2, pip >= 26.1.2. None of these 4 PRs do that.

---

## Pre-Mortem

Assume it is one week after merging all 4 in order #298 -> #300 -> #299 -> #291 and something broke. Top plausible failure modes:

| # | Failure mode | Plausibility | Does evidence show the plan mitigates it? |
|---|-------------|--------------|-------------------------------------------|
| (a) | **ruff 0.15.18 pre-commit hook starts failing for local contributors** (new lint rules flag existing code) | Low | **Mitigated.** #300 already runs ruff 0.15.18 via the dev dependency in the `Static Analysis` CI job, which passed. The pre-commit hook (#299) pins the same version. The 0.15.11->0.15.18 range is patch-level; prior report notes the only behavioral change is `UP007/UP045` possibly auto-adding `from __future__ import annotations` under `--fix`. Since Static Analysis is green on #300, the codebase is already clean under 0.15.18. Residual risk: a contributor with `--fix` enabled may see import additions; non-blocking. |
| (b) | **pytest 9.1 deprecations becoming errors in CI** | Low (this week) | **Mitigated for now.** All 9 `Test uv` jobs pass on pytest 9.1.1 today. Prior report confirms the 9.1 items are *deprecation warnings* (class-scoped fixtures w/o `@classmethod`, generator `parametrize`, etc.) with removal slated for pytest 10, not 9.x. No `-W error` escalation is configured that would convert them. Risk materializes only on a future pytest 10 bump, not from this merge. Recommend a follow-up cleanup task. |
| (c) | **httpx -> httpx2 swap breaks the release/version-bump workflow** | Low-Medium | **Largely mitigated, with a real residual.** The swap is transitive, driven solely by `bump-my-version` 1.3.0->1.4.1 (which declares httpx2/httpcore2/truststore as its deps — self-consistent resolution; uv.lock resolves cleanly and all matrix jobs pass). `httpx2` is the Pydantic-stewarded continuation of httpx (verified in prior report against PyPI), not a typosquat. `src/` and tests do not import httpx (grep of pyproject shows httpx only as a transitive dep of bump-my-version). RESIDUAL: the actual `version-bump.yml`/`release.yml` jobs are NOT exercised by PR CI (they run on tag/dispatch). So "all green" does NOT prove the release path works under bump-my-version 1.4.1 + httpx2. This is the single least-verified change. Recommend a manual `workflow_dispatch` dry-run of version-bump.yml after merge before the next real release. |
| (d) | **Lockfile resolution differs across the 3.11-3.14 matrix** | Very Low | **Mitigated.** uv.lock is a single resolved lockfile with environment markers (e.g., `typing-extensions` gated to `python_full_version < '3.13'`). All 9 matrix jobs (3.11/3.12/3.13/3.14) installed from `--frozen` and passed. No per-version resolution divergence observed. |
| (e) | **Being "1 commit behind main" causes a problem given C2** | Very Low | **Mitigated / N/A.** With no `required_status_checks` and no `require_last_push_approval`, GitHub does not force branch-up-to-date before merge. Merges are independent (only #299/#291 share a file, and they are conflict-free per C1). After each merge the others become "1 behind" but remain mergeable; dependabot will rebase on its schedule. The only ordering-sensitive pair (#299 before/after #291) is conflict-free in both orders. No "behind main" hazard. |

**Additional pre-mortem risk not in the prompt's list:**

| # | Failure mode | Mitigated? |
|---|-------------|------------|
| (f) | **Someone interprets "merge to turn CI green" (prior report rec #4 / line 221) and expects green after these 4** | **NOT mitigated by the plan — this is a documentation hazard.** None of the 4 PRs remediate any flagged CVE (C5). The ci.yml security job stays red after all 4. The prior report's suggestion that merging a "dependency-fix PR ... turn[s] CI green" does not apply to this batch. Reviewers must not block these PRs waiting for green, and must not assume green will follow. |

---

## Final Verdict

**SAFE TO MERGE (introduces no new breakage): YES.** All four PRs are safe to merge as-is. Evidence: no merge conflicts (C1), CI status checks do not gate merge (C2), the only red checks are environmental/time-driven and reproduce on no-op PRs (C3/C4), and #300's full test matrix passes with the upgraded pytest/ruff (C4).

**TURNS CI GREEN: NO.** This is the critical distinction the plan blurs. After merging all 4 in any order, the ci.yml `security` job remains **RED with 9 vulnerabilities in 5 packages** (mako, urllib3, msgpack, pydantic-settings, pip), because **none of the 4 PRs change any flagged package** (C5). "Safe to merge" and "turns CI green" are DIFFERENT here, and only the former is true.

**MUST-FIX-FIRST: None blocks merging.** There is no must-fix-first item for *merge safety*. However, to *achieve green CI*, a follow-up PR is required bumping mako>=1.3.12, urllib3>=2.7.0, msgpack>=1.2.1, pydantic-settings>=2.14.2, pip>=26.1.2. That work is out of scope of these 4 PRs and should be filed as a separate item (with H-32 GitHub Issue parity).

**ORDERING RECOMMENDATION: The proposed order #298 -> #300 -> #299 -> #291 is acceptable but the ordering is irrelevant to safety.** Rationale:
- The four PRs are mutually independent except the conflict-free #299/#291 pair (C1), so any order is safe.
- The stated rationale for ordering (e.g., "merge the dependency-fix PR first to turn CI green") is **invalid** — #300 fixes zero CVEs, so it does not green CI; ordering buys nothing.
- If a marginal preference is wanted: merge the lowest-risk, fully-verified changes first — **#298 (pinned-SHA action bump) and the two single-line pre-commit bumps #299/#291** are trivially safe. **#300 carries the only meaningful behavioral surface** (pytest 9.1, ruff 0.15.18, the bump-my-version/httpx2 transitive swap whose release-path is unverified per pre-mortem (c)). One defensible alternative order: **#298 -> #299 -> #291 -> #300**, merging the zero-runtime-impact changes first and the dependency lockfile change last so it is the most recent / easiest to revert if the next release surfaces a bump-my-version/httpx2 issue. Either order is safe; this is a preference, not a requirement.

**Net:** Approve and merge all 4 (subject to the required code-owner review per C2). Do not expect CI to go green. Open a separate PR for the 5 CVE-remediating bumps and a `workflow_dispatch` dry-run of version-bump.yml to close the one unverified residual.

---

## Evidence Appendix

**C1 conflict simulation:**
```
$ git merge-tree --write-tree origin/main pr-299-head; echo $?   -> 0
$ git merge-tree --write-tree origin/main pr-291-head; echo $?   -> 0
$ TREE299=$(merge main+#299); git merge-tree --write-tree --merge-base origin/main $TREE299 pr-291-head; echo $?  -> 0
#299 hunk: @@ -39,7 +39,7 @@  (rev line 42)
#291 hunk: @@ -202,7 +202,7 @@ (rev line 205)
```

**C2 ruleset:**
```
$ gh api repos/geekatron/jerry/rules/branches/main
types: ["deletion","non_fast_forward","pull_request"]
pull_request: required_approving_review_count=1, require_code_owner_review=true
$ gh api repos/geekatron/jerry/branches/main/protection  -> 404 Not Found
```

**C3 main was green; red is DB drift:**
```
main ci.yml run 24699012054 (sha 750af52d, 2026-04-21): conclusion=success
  Security Scan job 72237998434: "No known vulnerabilities found"
PR #300 ci.yml run 27923808261 (2026-06-22):
  Security Scan job 82622250086: "Found 9 known vulnerabilities in 5 packages", exit code 1
scheduled security-scan.yml run 27938639670 (2026-06-22 08:14): "No known vulnerabilities found", success
  (same versions installed: mako==1.3.10, urllib3==2.6.3, msgpack==1.1.2, pydantic-settings==2.13.1, pip==26.0)
```

**C3/C4 failing-job identity:**
```
ci.yml security job: uv sync --frozen; uv export --no-hashes --frozen --all-extras --no-emit-project > /tmp/requirements.txt; uv run pip-audit --requirement /tmp/requirements.txt --strict --desc
CI Success aggregator: needs: [static-analysis, security, validation, plugin-validation, cli-integration, test-uv, changelog-check]; fails because security: failure
```

**C5 lockfile comparison:**
```
$ for pkg in mako urllib3 idna msgpack pydantic-settings pymdown-extensions pip; do git show origin/main:uv.lock | grep -A1 name=\"$pkg\" | grep version; done
mako 1.3.10 | urllib3 2.6.3 | idna 3.11 | msgpack 1.1.2 | pydantic-settings 2.13.1 | pymdown-extensions 10.21.2 | pip 26.0
$ ... <#300 head>:uv.lock ...
mako 1.3.10 | urllib3 2.6.3 | idna 3.18 | msgpack 1.1.2 | pydantic-settings 2.13.1 | pymdown-extensions 10.21.3 | pip 26.0
#300 version bumps (none of the 5 flagged pkgs): bump-my-version, filelock, httpcore->httpcore2, httpx->httpx2, idna, markdown-it-py, mdit-py-plugins, pip-audit, pre-commit, pymdown-extensions, pyright, pytest, requests, ruff, tiktoken, +truststore
pip-audit fix versions (from #300 run): mako 1.3.12, urllib3 2.7.0, msgpack 1.2.1, pydantic-settings 2.14.2, pip 26.1.2/26.1
```

**C4 per-PR checks:** all four PRs (#298/#300/#299/#291) -> only `CI Success` + `Security Scan` red; `Test uv` 9/9 pass, Static Analysis/CLI Integration/Plugin Validation/Validation/Changelog pass.

---

*Adversarial reviewer. Evidence gathered 2026-06-22 against geekatron/jerry @ main 750af52d. READ-ONLY: no merge, modify, or push performed.*
