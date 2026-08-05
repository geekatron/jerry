# Verification Report: BUG-008

> **Type:** verification-report
> **Generated:** 2026-08-05T00:00:00Z
> **Agent:** wt-verifier
> **Scope:** full (acceptance criteria + evidence + closure readiness)

---

## Navigation

| Previous | Up | Next |
|----------|----|----- |
| [verification-evidence-20260805.md](verification-evidence-20260805.md) | [EPIC-004-security-scan-hardening](../) | - |

---

## Summary

| Metric | Value |
|--------|-------|
| **Work Item** | BUG-008: Scheduled Security Scan Is False-Green — Audits Only the Local Project, Misses All Transitive CVEs |
| **Status (frontmatter)** | in_progress |
| **Verification Score** | 100% (4/4 acceptance criteria verified) |
| **Verdict** | PASSED |

---

## Acceptance Criteria Verification

| # | Criterion | Verified | Evidence |
|---|-----------|----------|----------|
| 1 | Scheduled scan detects at least the 9 known transitive CVEs that the CI scan detects (parity verified by running both workflows and comparing CVE lists) | ✅ (intent satisfied; see note) | GH Actions run [30934932209](https://github.com/geekatron/jerry/actions/runs/30934932209) (CI, push to main, 2026-08-04) and run [30983157958](https://github.com/geekatron/jerry/actions/runs/30983157958) (Scheduled, 2026-08-05) both report the byte-identical verdict `Found 1 known vulnerability in 1 package` / `click 8.3.1 PYSEC-2026-2132` and identical scope `104 packages in scope (floor: 20)`. Both workflows invoke the same composite action `.github/actions/security-audit/action.yml`, structurally guaranteeing parity. |
| 2 | Running the scheduled scan against the current codebase produces a non-zero exit code (audit fails due to open CVEs, not a false-green pass) | ✅ | `gh run list --workflow security-scan.yml` shows 13 consecutive daily scheduled runs (2026-07-23 → 2026-08-05), every one `conclusion: failure` (non-zero exit), driven by `fail-on-vuln: 'true'` in `security-scan.yml` plus the real click 8.3.1 CVE. Confirmed via `gh run view --log` on runs 30983157958 and 31039187847. |
| 3 | The log no longer contains `Dependency not found on PyPI: jerry` as the primary audit result | ✅ | `gh run view <id> --log \| grep -i "Dependency not found on PyPI"` returns empty for both the scheduled run (30983157958) and the CI run (30934932209). Root cause fixed structurally: `action.yml` exports via `uv export --no-hashes --frozen --all-extras --no-emit-project`, which excludes the local `jerry` package from the export entirely. |
| 4 | Silent-failure guard rejects a scheduled scan run that audits zero PyPI packages | ✅ | (a) Code review of `action.yml` "Run pip-audit" step confirms the D5 guard: asserts a recognizable verdict sentinel AND `REQ_COUNT >= MIN_PKGS` (floor 20), `exit 1` otherwise. (b) `verification-evidence-20260805.md` Claim G-1 (no verdict sentinel → exit 1) and Claim G-2 (2 packages < 20 floor → exit 1) directly exercised this failure path and confirmed rejection. (c) Every live run (13/13 scheduled, plus CI) logs `D5 guard passed: verdict found, 104 packages in scope (floor: 20)`, confirming the guard executes correctly on every real run. |

**Verification Score Calculation:**
- Total criteria: 4
- Verified: 4
- Score: 100% (4 / 4 × 100)

**Threshold:** 80% required for closure — **PASSED**

---

## Blocking Issues

None.

---

## Recommendations

### Non-blocking observations

1. **Stale "pending merge" note in Delivery Evidence.** The entity's Delivery Evidence table states the PR is "pending merge — close on merge + AC verification," but commit `81c7c61c` is confirmed to be an ancestor of `origin/main` (merged). AC verification is now complete per this report. Recommend updating the entity's status to `completed`/`done` and refreshing the Delivery Evidence note now that both conditions are satisfied.
2. **PR number discrepancy.** The entity's Delivery Evidence table cites PR #302 as the delivering PR; the task brief for this verification cited PR #304. Investigation confirms: PR #302 ("ci: harden dependency security-scan pipeline — unified audit + CVE accept-list (1/2)", merged 2026-06-23) is the PR whose title matches commit `81c7c61c`'s content; PR #304 (merged 2026-06-28) is a separate docs-only PR (ADR/worktracker/adversarial review docs). The entity's citation of #302 is the more accurate one; recommend no change needed to the entity beyond confirming this, but flagging in case #304 was intended to be referenced elsewhere.
3. **GitHub Issue #301 parity (H-31).** GH Issue #301 (linked in the entity's frontmatter) is still **OPEN**. Per H-31 GitHub Issue Parity, when BUG-008 is transitioned to `done`, issue #301 should be closed in the same session to keep worktracker and GitHub Issues in sync.
4. **Sibling entities still `in_progress`.** STORY-026, STORY-029, and STORY-030 (the "Fixed by" cross-links, not children) are all still marked `in_progress` in their own entity files, despite PR #302 and PR #303 both being merged and this verification's evidence confirming their delivered behavior works correctly. This does not block BUG-008's closure (BUG-008 has no `Children` section — only cross-links to sibling stories), but it is a related worktracker-integrity gap worth closing in the same pass.
5. **"9 known CVEs" framing in AC #1 is stale.** STORY-030 (PR #303, merged 2026-06-23) remediated the original 9 transitive CVEs; a new CVE (click 8.3.1 / PYSEC-2026-2132) was published after that remediation and is now the sole unfixed CVE. AC #1's literal "9 CVEs" scenario can no longer be reproduced (there are no longer 9 known CVEs in the tree). The AC's underlying intent — parity between scheduled and CI scan CVE detection — was verified directly against the current single-CVE state using live, contemporaneous workflow runs, which is stronger evidence than the originally specified reproduction scenario.

---

## Ready for Closure

**YES** - All 4 acceptance criteria are verified against concrete, current, and independently corroborating evidence: (a) direct code review of the fix (`.github/actions/security-audit/action.yml`, `security-scan.yml`, `ci.yml`), (b) the prior local verification evidence report (`verification-evidence-20260805.md`, Claims A/A-Contrast/G), and (c) live GitHub Actions run logs pulled fresh during this verification (13 consecutive daily scheduled runs all correctly RED; a same-week CI run independently corroborating identical CVE detection). The false-green defect described in the bug summary — `pip-audit .` silently auditing zero PyPI packages and exiting 0 — is structurally impossible under the fixed pipeline (`--no-emit-project` export + D5 guard), and this is proven both by static code inspection and by every observed live run.

**Closure Criteria Assessment:**

| Criterion | Met? | Details |
|-----------|------|---------|
| 80%+ acceptance criteria verified | ✅ Yes | 4/4 (100%) — see Acceptance Criteria Verification table |
| Evidence section has ≥1 link | ✅ Yes | Entity's Delivery Evidence table has 1 link (PR #302 / commit 81c7c61c); this report and `verification-evidence-20260805.md` add substantially more, including live GH Actions run URLs |
| All child items completed | ✅ N/A | BUG-008 has no `Children` section; "Fixed by" entries (STORY-026/029/030) are cross-links, not parent-child dependencies for closure purposes |
| No blocking impediments | ✅ Yes | None identified; see Recommendations for non-blocking cleanup items |

---

## Work Item Details

**ID:** BUG-008

**Title:** Scheduled Security Scan Is False-Green — Audits Only the Local Project, Misses All Transitive CVEs

**Type:** bug

**Current Status:** in_progress (per `jerry ast frontmatter`)

**Parent:** FEAT-002 - Security-scan pipeline hardening

**Children:** 0 (no Children section; cross-linked "Fixed by" items: STORY-026, STORY-029)

---

## Evidence Summary

**Total Evidence Links:** 1 in entity file + 2 supporting artifacts consulted during this verification

**Evidence Quality:**

Strong. Evidence spans three independent tiers: (1) static code review of the merged fix on `main` (composite action, both consuming workflows), (2) a prior structured local-verification report with 18 explicitly executed test claims, and (3) fresh live production evidence pulled directly from the GitHub Actions API during this verification session (not merely cited — independently re-fetched and grepped). All three tiers agree with no contradictions.

**Evidence Links:**

- [PR #302 (entity-cited)](https://github.com/geekatron/jerry/pull/302) — "ci: harden dependency security-scan pipeline — unified audit + CVE accept-list (1/2)", merged 2026-06-23, contains commit `81c7c61c`
- [Commit 81c7c61c](https://github.com/geekatron/jerry/commit/81c7c61cb74d184a951d2791a4c8a0b54daf193f) — confirmed ancestor of `origin/main` via `git merge-base --is-ancestor`
- `.github/actions/security-audit/action.yml` — composite action; D5 guard code inspected directly (lines implementing verdict sentinel + package-floor checks)
- `.github/workflows/security-scan.yml` — scheduled workflow; confirmed `fail-on-vuln: 'true'`, uses composite action
- `.github/workflows/ci.yml` — CI workflow; confirmed uses the same composite action with `fail-on-vuln: 'false'` (non-blocking by design)
- [Scheduled run 30983157958](https://github.com/geekatron/jerry/actions/runs/30983157958) (2026-08-05, schedule) — `conclusion: failure`, "Found 1 known vulnerability in 1 package", "D5 guard passed: verdict found, 104 packages in scope (floor: 20)", no "Dependency not found on PyPI" line
- [Manual dispatch run 31039187847](https://github.com/geekatron/jerry/actions/runs/31039187847) (2026-08-05, workflow_dispatch) — same verdict, same 104-package scope
- [CI run 30934932209](https://github.com/geekatron/jerry/actions/runs/30934932209) (2026-08-04, push to main) — Security Scan job independently reports the identical verdict and package count as the scheduled scan, proving live parity
- 13 consecutive daily scheduled-scan runs (2026-07-23 through 2026-08-05, `gh run list --workflow security-scan.yml`) — all `conclusion: failure` (correctly RED, no false-green)
- `projects/PROJ-024-tactical-work/work/EPIC-004-security-scan-hardening/verification/verification-evidence-20260805.md` — prior structured verification (Claim A, Claim A Contrast, Claim G-1, Claim G-2)

---

## Detailed Verification

### Acceptance Criteria Analysis

**AC #1 — Scheduled/CI parity on ≥9 CVEs:** The literal "9 CVEs" scenario no longer exists in the current dependency tree because STORY-030 (PR #303, merged 2026-06-23) remediated the original 9. A new CVE (click 8.3.1) surfaced afterward and is the sole current finding. Rather than treat this as unverifiable, this verification directly tested the AC's underlying intent — CI and scheduled scan agreement — using live, same-week runs of both workflows. Run 30934932209 (CI, 2026-08-04) and runs 30983157958/31039187847 (scheduled, 2026-08-05) report identical verdicts and identical package scope (104). Because both workflows call the same composite action (`./.github/actions/security-audit`), this parity is not incidental — it is structurally guaranteed by the DRY refactor that STORY-026 delivered. Verdict: satisfied.

**AC #2 — Non-zero exit on open CVEs:** Verified directly via `gh run list` (13/13 recent scheduled runs = `conclusion: failure`) and `gh run view --log` (explicit `::error::pip-audit found unfixed vulnerabilities (fail-on-vuln=true)` path in `action.yml`, confirmed exercised). Verdict: satisfied.

**AC #3 — No "Dependency not found on PyPI: jerry" as primary result:** Verified by grepping full logs of both a scheduled run and a CI run — zero matches. The `--no-emit-project` flag in the `uv export` step is the structural fix; `jerry` is excluded from the exported requirements file entirely, so `pip-audit` never encounters it. Verdict: satisfied.

**AC #4 — Silent-failure guard rejects zero-package audits:** Verified via three converging evidence sources: static code review (D5 guard logic in `action.yml`), direct unit-style test evidence in `verification-evidence-20260805.md` (Claims G-1 and G-2, which directly forced the guard's failure branches and confirmed `exit 1`), and observation that the guard's pass branch (`D5 guard passed: verdict found, 104 packages in scope (floor: 20)`) fires on every real run. The failure branch itself is not observable in production logs (a healthy audit will not have < 20 packages), which is expected and appropriate for a negative-path guard — its correctness was established via the targeted synthetic tests in the verification evidence report. Verdict: satisfied.

### Child Item Status

Not applicable — BUG-008 declares no `Children` section. The `Related Items` → `Cross-Links` entry lists STORY-026 and STORY-029 as "Fixed by," which are sibling delivery vehicles, not structural children subject to WTI-002 rollup. Both cross-linked stories' PRs (#302, #303) are confirmed merged and their behavior independently verified during this session, though their own entity files remain `in_progress` (see Recommendations #4).

### Impediments Check

No open blockers found. No `Impediments` or `Blockers` section exists in the entity file. No unresolved dependency, environment, or approval gate was identified during verification.

### Evidence Validation

All cited evidence resolves to real, currently-accessible artifacts: the GitHub PR (#302) and commit (`81c7c61c`) both exist and the commit is confirmed on `main`; the composite action and both consuming workflow files exist in the working tree at the expected paths; the GitHub Actions run IDs cited in the task brief were independently re-fetched via `gh run view` during this session and their log content matches the claims made (byte-for-byte on the verdict and package-count lines). No placeholder, dead, or unverifiable links were found.

---

## Verification Timeline

| Timestamp | Event |
|-----------|-------|
| 2026-08-05T00:00 | Read BUG-008 entity file; extracted 4 acceptance criteria |
| 2026-08-05T00:00 | Read `verification-evidence-20260805.md` (prior local verification, Claims A/A-Contrast/G) |
| 2026-08-05T00:00 | `jerry ast frontmatter` — confirmed entity Status = `in_progress` |
| 2026-08-05T00:00 | Reviewed `.github/workflows/security-scan.yml` and `.github/workflows/ci.yml` — confirmed both call the same composite action |
| 2026-08-05T00:00 | Reviewed `.github/actions/security-audit/action.yml` — confirmed `--no-emit-project` export and D5 guard logic |
| 2026-08-05T00:00 | `gh run view 30983157958 --log` and `31039187847 --log` — confirmed scheduled-scan verdict, package scope, absence of false-green string |
| 2026-08-05T00:00 | `gh run list --workflow security-scan.yml` — confirmed 13 consecutive RED daily runs |
| 2026-08-05T00:00 | `gh pr view 302` / `gh pr view 303` / `gh pr view 304` — resolved PR-number discrepancy and confirmed merge status |
| 2026-08-05T00:00 | `git merge-base --is-ancestor 81c7c61c origin/main` — confirmed fix commit is live on main |
| 2026-08-05T00:00 | `gh run view 30934932209 --log` (CI run) — confirmed independent CI/scheduled parity on click 8.3.1 |
| 2026-08-05T00:00 | `gh issue view 301` — confirmed linked GitHub Issue still OPEN (H-31 parity note) |
| 2026-08-05T00:00 | Verification report generated and persisted |

---

## Next Actions

### If Approved for Closure

1. Update BUG-008 status to `done`/`completed` in the entity file
2. Refresh the Delivery Evidence note (remove "pending merge" language; it is merged and verified)
3. Close GitHub Issue #301 (H-31 parity)
4. Consider closing STORY-026, STORY-029, STORY-030 in the same pass — their delivered behavior is independently confirmed by this same evidence, though this verification was scoped to BUG-008 only

### If Rejected

Not applicable — no rejection; see Ready for Closure = YES above.

---

## Appendix

### WTI Rule Compliance

| Rule | Status | Notes |
|------|--------|-------|
| WTI-001: Real-Time State | ⚠ Stale | Entity Status field (`in_progress`) and Delivery Evidence note ("pending merge") lag the actual merged/verified state; recommend update on closure |
| WTI-002: No Closure Without Verification | ✅ Met | 4/4 (100%) acceptance criteria verified with concrete evidence; exceeds 80% threshold |
| WTI-003: Truthful State | ✅ Met (by this report) | This report accurately reflects verified vs. unverified state; does not overstate confidence |
| WTI-005: Atomic State Updates | ✅ N/A | No state update performed by this agent (verification-only, entity file not modified) |
| WTI-006: Evidence-Based Closure | ✅ Met | Entity's Delivery Evidence table has 1 verifiable link; this verification independently corroborated it with 9 additional live/static evidence artifacts |

### Raw Verification Data

```json
{
  "work_item_id": "BUG-008",
  "verification_scope": "full",
  "timestamp": "2026-08-05T00:00:00Z",
  "passed": true,
  "score": 1.0,
  "acceptance_criteria": {
    "total_criteria": 4,
    "checked_criteria": 0,
    "verified_by_evidence": 4,
    "percentage": 1.0,
    "passed": true,
    "items": [
      {"id": "AC-1", "text": "Scheduled scan detects at least the 9 known transitive CVEs that the CI scan detects", "verified": true, "note": "intent-verified via live CI/scheduled parity on current single CVE (click 8.3.1); literal 9-CVE scenario no longer reproducible post-STORY-030 remediation"},
      {"id": "AC-2", "text": "Scheduled scan produces non-zero exit code on open CVEs", "verified": true},
      {"id": "AC-3", "text": "Log no longer contains 'Dependency not found on PyPI: jerry' as primary result", "verified": true},
      {"id": "AC-4", "text": "Silent-failure guard rejects zero-PyPI-package audit runs", "verified": true}
    ]
  },
  "evidence": {
    "total_links": 10,
    "valid_links": 10,
    "passed": true
  },
  "child_rollup": {
    "applicable": false,
    "total_children": 0
  },
  "blocking_issues": [],
  "recommendations": [
    "Update entity Status to done/completed and refresh Delivery Evidence note",
    "Close GitHub Issue #301 (H-31 parity)",
    "Consider closing STORY-026/029/030 given independently confirmed evidence",
    "AC-1 wording is stale relative to current CVE landscape; consider rewording for future audits"
  ]
}
```

---

*Report generated by wt-verifier (manual invocation).*
*Template: `.context/templates/worktracker/VERIFICATION_REPORT.md` v1.0*
