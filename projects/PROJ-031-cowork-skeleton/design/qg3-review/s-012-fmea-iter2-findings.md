# FMEA Report: PROJ-031 Phase-3 Design — Iteration 2 Re-Check

**Strategy:** S-012 FMEA (Failure Mode and Effects Analysis)
**Deliverable:** `design/phase3-skeleton-generation-design.md`, `design/phase3-ci-workflow-design.md`, `design/phase3-attestation-provenance-design.md`
**Criticality:** C4
**Date:** 2026-06-30
**Reviewer:** adv-executor (S-012 FMEA, iteration 2)
**Focus:** Verify the 6 iter-1 Critical remediations (ROOT-1..6); probe new mechanics for fresh failure modes
**H-16 Compliance:** S-003 Steelman and prior tournament strategies applied in iter-1 sequence (confirmed by orchestrator context)
**Elements Analyzed:** 6 | **Failure Modes Identified:** 7 | **Total RPN:** 1,299

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment and ROOT soundness verdict |
| [ROOT Soundness Verdicts](#root-soundness-verdicts) | Explicit pass/fail on each iter-1 Critical fix |
| [Findings Table](#findings-table) | All 7 failure modes with S/O/D/RPN |
| [Detailed Findings](#detailed-findings) | Critical and Major findings with evidence and corrective actions |
| [Minor Findings](#minor-findings) | RPN < 80 — improvement opportunities |
| [Recommendations](#recommendations) | Prioritized corrective actions |
| [Scoring Impact](#scoring-impact) | S-014 dimension mapping |
| [Execution Statistics](#execution-statistics) | Counts and protocol completion |

---

## Summary

This iteration-2 FMEA targets the remediated Phase-3 design documents produced after the iter-1 tournament. The 6 ROOT fixes were loaded from the design documents independently (per the blindness constraint — iter-1 finding files were not read). Six elements were decomposed: the D7 digest-based monitor (ROOT-1), GIT_*_DATE propagation (ROOT-2), version sentinel placement (ROOT-3), bundle round-trip (ROOT-4), D8 pattern catalog spec (ROOT-5), and the auto-revert circuit breaker (ROOT-6). Seven failure modes were identified.

**ROOT-2, ROOT-3, ROOT-4, and ROOT-5 are SOUNDLY FIXED.** ROOT-1 is architecturally correct but introduces one Critical failure mode in the shallow-fetch byte-idempotency assumption. ROOT-6 is mostly correct but introduces one Critical failure mode in the `advance-last-good-validated` suppressed-path logic.

Three Critical failure modes remain: **FM-001-i2** (annotated-tag tagger-date null → persistent freshness failures, RPN 343), **FM-002-i2** (runner-image git version drift → digest false alarms, RPN 336), and **FM-003-i2** (freshness suppression advances `last-good-validated` to an unverified/failing tag, RPN 280). All three are design-level defects requiring correction before Phase-6. Two Major modes address race conditions in the label-based revert counter.

**Recommendation: REVISE** — targeted corrections to three design-level defects; no fundamental architecture rework.

---

## ROOT Soundness Verdicts

| ROOT | Fix | Verdict | Rationale |
|------|-----|---------|-----------|
| ROOT-1 / DA-001 | Digest-based D7 monitor: download attested tar → `gh attestation verify --signer-workflow` → sha256 compare → freshness | **MOSTLY SOUND — 1 residual (FM-002-i2)** | The architectural fix (digest comparison replaces broken SLSA-predicate SHA comparison) is correct. The `--signer-workflow` defense-in-depth is valuable. Residual: the byte-idempotency of `shallow-fetch + git archive` is acknowledged as CI-G-007 but runner image pinning is not mandated as a design constraint. |
| ROOT-2 / FM-007 | GIT_*_DATE must reach commit process via same-step inline or `$GITHUB_ENV`; bare cross-step `export` FORBIDDEN | **SOUND** | The constraint is correctly specified in both gen-design §2/§3(a) and ci-design §G6. The two valid mechanics (same-step inline and `$GITHUB_ENV`) are unambiguous. The idempotency check (two-run same-tag → same SHA) provides a reliable detection backstop. |
| ROOT-3 / FM-020 | Version sentinel placed under `projects/`; both injected files inside D6 `:!projects/` allow-list; G7 pins `projects/ == {README.md, .jerry-skeleton-version}` | **SOUND** | The dual-gate mechanism is elegant: D6 excludes `projects/` wholesale, G7 independently asserts exactly two members. An unexpected file under `projects/` fails G7 even though D6 wouldn't see it. The `.claude/` false-positive from iter-1 is fully resolved. |
| ROOT-4 / FM-037 | Bundle round-trip: `git checkout refs/remotes/bundle/HEAD` + RESTORED_SHA == COMMIT_SHA assertion in Job C | **SOUND** | The HEAD-repositioning step and SHA assertion correctly address "Job C pushes source-repo HEAD instead of G6_SHA." Pending Phase-6 empirical confirmation (CI-G-001), which the design correctly flags. |
| ROOT-5 / PM-003 | D8 pattern catalog path specified (`runbooks/content-safety-patterns.md`); fail-closed on absent/empty catalog (`CI-G-003` Phase-5 BLOCKER) | **CORRECTLY DEFERRED** | The catalog path is pinned in the design, the fail-closed guard is sound, and the content (C1–C6 patterns) is legitimately an eng-architect deliverable. The Phase-5 BLOCKER gate is the right governance mechanism. |
| ROOT-6 / PM-004 | Auto-revert circuit breaker: MAX_AUTO_REVERTS=3; label-tracked per source tag; cap exceeded → CRITICAL human-escalation; freshness suppression via `generation-failure-escalation:${tag}` label | **PARTIALLY SOUND — 1 critical defect (FM-003-i2)** | The circuit breaker logic itself is correct. The freshness suppression intent is correct. However, in the suppressed path the `advance-last-good-validated` step uses `${latest_src_tag}` (the generation-failing, undeployed tag) instead of `${deployed_release_version}` (the digest-verified deployed version). This creates a self-reinforcing failure loop. |

---

## Findings Table

| ID | Element | Failure Mode | S | O | D | RPN | Severity | Corrective Action Summary | Dimension |
|----|---------|-------------|---|---|---|-----|----------|--------------------------|-----------|
| FM-001-i2 | D7 Monitor Step 8 freshness check | `jq -r '.committer.date'` returns null for annotated git tags; `parse_time(null)` yields a very large elapsed → persistent freshness-CRITICAL false alarms | 7 | 7 | 7 | 343 | **Critical** | Fix jq path: use `.tagger.date` for tag objects, `.committer.date` for commit objects; add null guard | Methodological Rigor |
| FM-002-i2 | D7 Monitor Step 5 (shallow-fetch git archive) | `ubuntu-latest` git binary version can change between CI generation run and subsequent D7 monitor runs; different git versions produce different pax headers in `git archive` output → `ATTESTED_DIGEST ≠ LIVE_DIGEST` → false CRITICAL tamper alarms | 8 | 6 | 7 | 336 | **Critical** | Mandate `ubuntu-24.04` (pinned OS image) for BOTH the generation step and D7 monitor; make this a design constraint, not a Phase-6 suggestion | Evidence Quality |
| FM-003-i2 | M1 `advance-last-good-validated` during freshness suppression | When suppression fires (`escalation_open > 0`), execution falls through to `advance-last-good-validated ${latest_src_tag}`; `latest_src_tag` is the generation-failing, undeployed tag → next auto-revert dispatches the failing tag → self-reinforcing failure loop | 8 | 5 | 7 | 280 | **Critical** | In the suppressed path, skip `advance-last-good-validated` entirely OR use `${deployed_release_version}` (the digest-verified, deployed tag) | Internal Consistency |
| FM-004-i2 | M2 auto-revert label counter | Human maintainer closes an open `auto-revert:${tag}` issue (believing stale) → `count_open_issues` drops below MAX_AUTO_REVERTS → next M2 dispatch proceeds beyond design-intent cap without triggering human escalation | 6 | 5 | 6 | 180 | **Major** | Label issues with a permanent `auto-revert-attempt:${tag}:${N}` label in addition to the open-issue count; count all labeled issues (open or closed) for cap enforcement | Methodological Rigor |
| FM-005-i2 | M2 auto-revert label counter (race) | Two concurrent monitor runs (scheduled + manual `workflow_dispatch`) both read REVERT_ATTEMPT_COUNT = 2 (< MAX=3), both dispatch, both open a label issue → 4 total reverts dispatched for a 3-attempt cap; TOCTOU gap — GitHub issue labels are not transactional | 6 | 4 | 7 | 168 | **Major** | Add workflow-level concurrency group to `cowork-monitor.yml` (`cancel-in-progress: false`, `group: cowork-monitor`) to serialize M1/M2 execution; document the race as a known residual if concurrency is rejected | Methodological Rigor |
| FM-006-i2 | M2 `last-good-validated` bootstrap | `last-good-validated` is undefined at initial deployment; first generation failure correctly escalates to human per design ("IF last_good_tag is undefined: escalate") but no auto-revert baseline exists | 4 | 8 | 2 | 64 | **Minor** | Document in runbooks/org-registration.md that the first successful deploy MUST manually tag `last-good-validated`; add a post-deploy step in Job C to initialize it | Completeness |
| FM-007-i2 | D8 scanner scope | `hooks/` (Python session-start scripts) is excluded from D8's retained-markdown scan scope; a malicious Python payload in hooks/ bypasses D8 | 5 | 3 | 2 | 30 | **Minor** | Acknowledged known residual (design explicitly bounds this to D5 + REQ-051 two-reviewer); add a clarifying comment to the D8 scope spec noting the hooks/ decision rationale | Completeness |

---

## Detailed Findings

### FM-001-i2: Annotated Tag Tagger-Date Null in Freshness Check

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | `phase3-ci-workflow-design.md` — Job M1, Step m1-8-freshness-check |
| **RPN** | 343 (S=7, O=7, D=7) |
| **Strategy Step** | Step 2 (Failure Mode Enumeration) and Step 3 (Rating) |

**Evidence:**
```
STEP m1-8-freshness-check:
  latest_src_tag_time = gh api repos/geekatron/jerry/git/refs/tags/${latest_src_tag} \
    | jq -r '.object.url' | xargs gh api | jq -r '.committer.date'   # annotated tag tagger date
```

The comment says "annotated tag tagger date" but the code uses `.committer.date`. For annotated tags, `git/refs/tags/${tag}` returns `{type: "tag", object: {url: "…/git/tags/{tag_sha}"}}`. Dereferencing `.object.url` yields the **tag object**, which has `{tagger: {date: "…"}}` but **no** `committer` field. `jq -r '.committer.date'` returns `null`. For lightweight tags the same dereferencing yields the commit directly, which has `.committer.date`. GitHub's conventional `gh release create` produces **annotated** tags. Jerry's `version-bump.yml` almost certainly creates annotated release tags.

**Analysis:** `parse_time("null")` behavior is implementation-dependent. The most common outcome is Unix epoch (0) or script failure. If epoch is returned, `elapsed = now() - 0 ≈ 1,750,000,000+ seconds >> 2 hours`, triggering freshness CRITICAL on **every monitor run** for every annotated tag. This would fire the auto-revert circuit breaker up to 3 times per tag, permanently escalating to human for each release even when the pipeline is healthy. It makes the D7 monitor a source of alert-fatigue and undermines operator trust.

**Root Cause:** The jq path was written assuming a specific tag type without conditional handling. The GitHub REST API returns different response shapes for annotated vs. lightweight tags.

**Recommendation:** Replace the single `jq -r '.committer.date'` with a conditional extraction that handles both annotated and lightweight tags:
```bash
latest_src_tag_time = gh api repos/geekatron/jerry/git/refs/tags/${latest_src_tag} \
  | jq -r '.object.url' | xargs gh api \
  | jq -r 'if .tagger then .tagger.date elif .committer then .committer.date else error("no date field") end'
```
Add a null-guard: if the resolved date is empty or "null", exit 1 (FAIL-CLOSED) with a diagnostic message. This prevents silent false freshness failures.

**Acceptance Criteria:** Freshness check correctly resolves tag creation time for both `type: tag` (annotated) and `type: commit` (lightweight) API responses; synthetic test with an annotated tag does not yield null elapsed time.

**Post-Correction RPN Estimate:** S=7, O=2, D=3 → RPN=42. The jq conditional is straightforward to verify.

---

### FM-002-i2: Runner Image Git Version Drift Breaks Shallow-Fetch Digest Match

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | `phase3-ci-workflow-design.md` — Step m1-5-shallow-fetch-live-tar; `phase3-attestation-provenance-design.md` §3.3 CI-G-007 |
| **RPN** | 336 (S=8, O=6, D=7) |
| **Strategy Step** | Step 2 (Failure Mode Enumeration) and Step 3 (Rating) |

**Evidence:**

From `phase3-ci-workflow-design.md` Pending Validation table (CI-G-007):
> "Shallow-fetch + git archive byte-idempotency: git fetch --depth=1 + git archive --format=tar ${G6_SHA} on ubuntu-latest produces byte-identical output to the original CI git archive step for the same commit SHA; no unexpected mtime injection from runner git version"

From `phase3-attestation-provenance-design.md` §3.3:
> "PHASE-6 RESIDUAL (P-222): shallow-fetch + git archive byte-idempotency vs. original CI git archive must be empirically confirmed on ubuntu-latest (see Pending Validation CI-G-007)."
> "consider pinning ubuntu-24.04 to prevent runner image drift"

The word "consider" is a SOFT recommendation, not a design constraint. The generation step and monitor step both use `ubuntu-latest` (inferred from the design; no explicit runner specification). GitHub Actions updates `ubuntu-latest` periodically, changing the bundled git binary version (e.g., git 2.43.x → 2.45.x). `git archive --format=tar` produces pax extended headers that embed the commit hash and may differ between git versions in format or field ordering.

**Analysis:** The CI generation run (Job A) uses `ubuntu-latest` at tag-push time (e.g., git 2.43). The D7 monitor run happens ≤6 hours later but on an updated image (git 2.45). The shallow-fetch + `git archive` in Step 5 produces bytes that differ from the original CI artifact by the pax header format. `LIVE_DIGEST ≠ ATTESTED_DIGEST` → every monitor run fires `[CRITICAL] Tree-digest mismatch` → three auto-reverts → human escalation required for every release — while the pipeline was perfectly healthy.

O=6 (runner images update quarterly; `ubuntu-latest` is frequently refreshed; the gap between a release and the next monitor run is ≤6 hours, so most releases would be fine, but image updates can happen at any time). D=7 (the failure is non-obvious; the digest mismatch looks identical to a genuine tamper detection).

The design's "consider pinning ubuntu-24.04" is insufficient. This is a design constraint that must be MANDATED, not optional.

**Recommendation:** The design must explicitly mandate `ubuntu-24.04` (or an equivalent pinned image identifier) for:
1. Job A (generate-and-gate), specifically the `g9-produce-deterministic-artifact` step that runs `git archive`
2. Job M1 (integrity-and-freshness), specifically Step 5 (shallow-fetch git archive)

Add to the design (gen-design §3(b) and ci-design CI-G-007) the requirement: "The runner image MUST be pinned to a specific OS image identifier (e.g., `ubuntu-24.04`) for all steps that produce or re-derive the deterministic TAR. Using `ubuntu-latest` is FORBIDDEN for these steps as it couples digest correctness to an externally-controlled image update cycle."

**Acceptance Criteria:** Two independent workflow runs for the same release tag using the pinned image produce bit-identical artifacts; the Phase-6 two-run idempotency test (CI-G-007) MUST use the same pinned image in both the generation job and the monitor verification.

**Post-Correction RPN Estimate:** S=8, O=2, D=3 → RPN=48. Image pinning makes drift controllable.

---

### FM-003-i2: Freshness Suppression Advances last-good-validated to Generation-Failing Tag

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | `phase3-ci-workflow-design.md` — Step m1-8-freshness-check + advance-last-good-validated interaction |
| **RPN** | 280 (S=8, O=5, D=7) |
| **Strategy Step** | Step 2 (Failure Mode Enumeration) and Step 3 (Rating) |

**Evidence:**

From `phase3-ci-workflow-design.md` Step m1-8-freshness-check:
```
IF escalation_open > 0:
    emit_to_GITHUB_STEP_SUMMARY("[INFO] D7 freshness: stale but generation-failure escalation open — suppressed")
    # Do NOT exit 1 here; proceed to advance-last-good-validated only if digest check passed
```

From `advance-last-good-validated` step:
```
STEP advance-last-good-validated:
  # Only on full PASS (all above steps succeeded):
  git tag -f last-good-validated ${latest_src_tag}
```

The comment in the suppression block says "proceed to advance-last-good-validated only if digest check passed." The digest check (Step 7) verified the **deployed** release version (`${LATEST_TAG}` = `${deployed_release_version}`). However, `advance-last-good-validated` advances to `${latest_src_tag}`, which is the **newer source tag that failed generation and has not been deployed to the dedicated repo**.

**Analysis — Self-Reinforcing Failure Loop:**

Scenario:
1. v1.0.5 fails generation → `generation-failure-escalation:v1.0.5` issue opened
2. Deployed version is v1.0.4 (digest-verified: ATTESTED_DIGEST == LIVE_DIGEST for v1.0.4)
3. Freshness suppression fires: v1.0.5 stale, escalation open → no exit 1
4. `advance-last-good-validated v1.0.5` executes → last-good-validated now points to v1.0.5 (the generation-failing tag, never deployed)
5. Next M1 run: digest for v1.0.4 still passes; freshness still suppressed (escalation still open)
6. M1 exits 0 (no digest mismatch, suppressed freshness) — but last-good-validated is wrong
7. If a SECOND failure triggers M2: `last_good_tag = last-good-validated = v1.0.5`
8. M2 dispatches `cowork-skeleton.yml --field target_tag=v1.0.5` — the failing tag
9. Generation fails again → revert-attempt-count incremented → revert cap burns down
10. Cap hit → human escalation — but auto-revert never had a chance to succeed

The `${latest_src_tag}` in `advance-last-good-validated` is the wrong variable in the suppressed path. It should be `${deployed_release_version}` (the version whose digest was verified in Step 7), OR the advance should be skipped entirely during suppression.

**Recommendation:** Fix the suppression path: when `escalation_open > 0`, do NOT advance `last-good-validated`. Add an explicit guard:
```python
# In the suppressed path:
IF escalation_open > 0:
    emit_to_GITHUB_STEP_SUMMARY("[INFO] freshness suppressed — skipping last-good-validated advancement")
    # Do NOT advance last-good-validated: latest_src_tag is unverified (generation failed)
    # last-good-validated remains at the previously-validated version
    exit 0  # or continue to summary step
# (advance-last-good-validated is NOT reached via this path)
```

If the design intent is to advance on successful digest check regardless of freshness, use `${deployed_release_version}` instead of `${latest_src_tag}`:
```bash
git tag -f last-good-validated ${deployed_release_version}  # the version actually verified
```

**Acceptance Criteria:** Synthetic test: (a) trigger freshness suppression (open a `generation-failure-escalation` issue, arrange v_stale != v_deployed, digest passes); (b) verify `last-good-validated` tag does NOT advance to `v_stale`; (c) verify subsequent M2 auto-revert targets the previously-validated deployed version, not the failing new tag.

**Post-Correction RPN Estimate:** S=8, O=2, D=3 → RPN=48.

---

### FM-004-i2: Human-Closed Revert Issue Defeats Auto-Revert Cap

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | `phase3-ci-workflow-design.md` — Job M2, auto-revert step (a) and (b) |
| **RPN** | 180 (S=6, O=5, D=6) |
| **Strategy Step** | Step 2 (Failure Mode Enumeration) and Step 3 (Rating) |

**Evidence:**
```
# (a) Revert attempt cap — tracked via GitHub Issue labels per source tag:
MAX_AUTO_REVERTS = 3
REVERT_ATTEMPT_COUNT = count_open_issues(label="auto-revert:${LATEST_SRC_TAG}")

# (b) Circuit breaker: cap exceeded → halt auto-revert:
IF REVERT_ATTEMPT_COUNT >= MAX_AUTO_REVERTS:
    open_github_issue(title="[CRITICAL] auto-revert cap exceeded ...")
    exit 1
```

`count_open_issues` counts **open** issues with the `auto-revert:${tag}` label. A human maintainer reviewing the alert board may close one or more `auto-revert:${tag}` issues as "handled" or "stale" (common practice during incident management). After close, `count_open_issues` drops from 3 to 2. The next M2 run reads 2 < 3, dispatches another revert, opens another issue. This can continue indefinitely, bypassing the cap.

**Analysis:** The auto-revert cap is a critical safety mechanism per ROOT-6. Its failure mode (cap bypass via issue closure) is the exact scenario it was designed to prevent. The consequence is unbounded revert dispatches, alert fatigue, and potential instability if the reverted version itself has issues.

**Recommendation:** Track revert attempts using a counter that is **not reversible by closing issues**. Two options:
- Option A: Count ALL labeled issues (open AND closed): `count_all_issues(label="auto-revert-attempt:${tag}")`. The label is added at dispatch time and never removed.
- Option B: Use a dedicated, append-only tag (e.g., `revert-count-v1.0.5-3`) on the source repo whose existence (not open/closed state) is the counter. `git ls-remote --tags | grep "revert-count-${LATEST_SRC_TAG}" | wc -l`.

Option A is simpler and uses existing GitHub Issues infrastructure. Add a note in runbooks/org-registration.md that `auto-revert-attempt:${tag}` labels must NEVER be removed; closing issues is safe.

**Post-Correction RPN Estimate:** S=6, O=2, D=4 → RPN=48.

---

### FM-005-i2: TOCTOU Race on Auto-Revert Label Counter

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | `phase3-ci-workflow-design.md` — cowork-monitor.yml triggers + Job M2 |
| **RPN** | 168 (S=6, O=4, D=7) |
| **Strategy Step** | Step 2 (Failure Mode Enumeration) and Step 3 (Rating) |

**Evidence:**

`cowork-monitor.yml` trigger:
```yaml
on:
  schedule:
    - cron: '0 */6 * * *'   # Every 6 hours
  workflow_dispatch:           # Manual trigger for testing and recovery
```

M2 auto-revert logic:
```
REVERT_ATTEMPT_COUNT = count_open_issues(label="auto-revert:${LATEST_SRC_TAG}")
IF REVERT_ATTEMPT_COUNT >= MAX_AUTO_REVERTS: ... exit 1
# else: dispatch gh workflow run ...
open_github_issue(labels=["auto-revert:${LATEST_SRC_TAG}"])
```

Two concurrent monitor runs (scheduled run + operator-triggered `workflow_dispatch` during an incident) both reach M2. Both execute `count_open_issues` and read `REVERT_ATTEMPT_COUNT = 2`. Both conclude 2 < 3 = MAX. Both dispatch `cowork-skeleton.yml`. Both open a label issue. Total: 4 dispatches for a 3-attempt cap.

**Analysis:** GitHub Issues are not transactional; there is no atomic read-increment-write. The TOCTOU window is small (seconds) but achievable in incident scenarios where operators manually trigger monitor runs. The consequence is one extra revert dispatch beyond the cap before human escalation triggers. Not catastrophic but undermines the reliability guarantee of ROOT-6.

**Recommendation:** Add a `concurrency` group to `cowork-monitor.yml`:
```yaml
concurrency:
  group: cowork-monitor
  cancel-in-progress: false   # Serialize; do not drop in-flight runs
```
This ensures only one monitor workflow execution runs at a time, serializing M1+M2. The `workflow_dispatch` trigger will queue behind the scheduled run, eliminating the TOCTOU window. Document this in the workflow design as a safety requirement.

**Post-Correction RPN Estimate:** S=6, O=2, D=4 → RPN=48.

---

## Minor Findings

### FM-006-i2: last-good-validated Undefined at Initial Deployment

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **RPN** | 64 (S=4, O=8, D=2) |
| **Section** | `phase3-ci-workflow-design.md` — M2 auto-revert, `IF last_good_tag is undefined` |

**Evidence:** The design correctly handles this: `IF last_good_tag is undefined: escalate to human, no dispatch`. However, `last-good-validated` is only initialized by a passing monitor run, which requires at least one successful generation. The first generation failure (before any successful monitor cycle) cannot auto-revert. O=8 (certain: every first deployment starts without a baseline).

**Recommendation (Minor):** Add to `runbooks/org-registration.md` §Initial Deployment: "After the first successful force-push to `geekatron/jerry-cowork`, manually initialize: `git tag last-good-validated ${first_tag} && git push origin last-good-validated`." Alternatively, add an initialization step to Job C on first push (detect absent `last-good-validated` and create it). Post-correction RPN: S=4, O=2, D=2 → 16.

---

### FM-007-i2: D8 Scan Scope Excludes Python Execution Surface (hooks/)

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **RPN** | 30 (S=5, O=3, D=2) |
| **Section** | `phase3-ci-workflow-design.md` — Step d8-content-safety-scan |

**Evidence:** `SCOPE: retained markdown surface only — skills/ commands/ .claude/ .context/`. The `hooks/` directory (containing Python scripts that execute at session start) is explicitly excluded from D8 scope. The design notes: "semantic/implicit injection is a KNOWN UNMITIGATED RESIDUAL bounded (not closed) by two-reviewer peer review (REQ-051)."

**Analysis:** This is a known, intentional design boundary, not a defect. D6 faithful-derivative covers hooks/ (any modification against TAG fails D6). The content-safety concern for hooks/ is code execution (Python), not prompt injection (markdown), which is outside D8's threat model. Bounded by D5 (tag-on-main) + REQ-051 (two-reviewer).

**Recommendation (Minor):** Add a comment to the D8 scope specification: "hooks/ is excluded from D8 (prompt-injection pattern scanner) by design — Python execution payloads are a separate threat model bounded by D5 provenance gate and REQ-051 two-reviewer merge policy. If a future threat model identifies hooks/ as a prompt-injection vector, expand scope here." This prevents scope creep arguments and documents the decision rationale. Post-correction RPN: no RPN change needed; D=1 after documentation.

---

## Recommendations

### Priority 1 — Critical (Resolve before Phase-6 YAML is written)

| ID | Action | Owner | Acceptance Criteria |
|----|--------|-------|---------------------|
| FM-001-i2 | Replace `jq -r '.committer.date'` with conditional: `.tagger.date` (annotated) or `.committer.date` (lightweight); add null guard | eng-devsecops | Synthetic test with annotated tag produces non-null elapsed time; freshness check correctly passes for a healthy recent deployment |
| FM-002-i2 | Add design constraint: mandate `ubuntu-24.04` (pinned) for G9 `git archive` step AND D7 monitor Step 5 shallow-fetch; forbid `ubuntu-latest` for these steps | eng-devsecops + eng-infra (design-level; Phase-6 implements) | Phase-6 idempotency test (CI-G-007) must use same pinned image; two-run same-tag produces identical digests |
| FM-003-i2 | In the freshness suppression path: either (a) skip `advance-last-good-validated` entirely, or (b) use `${deployed_release_version}` (digest-verified) instead of `${latest_src_tag}` | eng-devsecops | Synthetic test: suppression fires → `last-good-validated` does NOT advance to the failing/undeployed tag |

### Priority 2 — Major (Resolve before G-monitor gate)

| ID | Action | Owner | Acceptance Criteria |
|----|--------|-------|---------------------|
| FM-004-i2 | Change revert counter to count ALL labeled issues (open+closed) using `auto-revert-attempt:${tag}:${N}` labels; document in runbooks that these labels must not be removed | eng-devsecops | Human closure of a revert issue does not reduce the dispatch count; cap enforces correctly after 3 dispatches |
| FM-005-i2 | Add `concurrency: group: cowork-monitor, cancel-in-progress: false` to `cowork-monitor.yml` | eng-devsecops | Concurrent scheduled+manual trigger serializes; second trigger queues, does not duplicate M2 dispatch |

### Priority 3 — Minor (Resolve before go-live)

| ID | Action | Owner |
|----|--------|-------|
| FM-006-i2 | Add `last-good-validated` bootstrap step to Job C (first push) and document in runbooks | eng-devsecops |
| FM-007-i2 | Add scope rationale comment to D8 spec | eng-devsecops |

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| **Completeness** | 0.20 | Negative (FM-001-i2, FM-006-i2) | FM-001-i2: annotated tag handling is missing from the freshness check; FM-006-i2: bootstrap procedure for `last-good-validated` is absent from the design |
| **Internal Consistency** | 0.20 | Negative (FM-003-i2) | FM-003-i2: the suppressed-path comment ("proceed only if digest check passed") is inconsistent with the `advance-last-good-validated ${latest_src_tag}` implementation which uses the wrong variable (unverified source tag, not verified deployed version) |
| **Methodological Rigor** | 0.20 | Negative (FM-002-i2, FM-004-i2, FM-005-i2) | FM-002-i2: "consider pinning" is not a rigorously specified design constraint; FM-004-i2 and FM-005-i2: the label-counter mechanism has known reliability holes (issue closure, TOCTOU) that undermine the ROOT-6 circuit breaker's correctness claim |
| **Evidence Quality** | 0.15 | Positive (ROOT-1, ROOT-2, ROOT-3, ROOT-4) | The four soundly-fixed ROOTs are well-evidenced with specific pseudocode, prohibition lists, and interaction analysis. The P-222 claim-status convention is applied consistently and rigorously. |
| **Actionability** | 0.15 | Positive (ROOT-5, detailed corrective actions) | ROOT-5 correctly defers D8 catalog content with a Phase-5 BLOCKER gate. Corrective actions for all five Critical+Major findings are specific, small-scope, and implementable by a single engineer. |
| **Traceability** | 0.10 | Positive (ROOT-3, G7+D6 dual-gate) | The `projects/` placement fix and G7 pin are precisely traced to FM-020-QG3 and D6 REQ-022. All ROOT fixes carry forward-traces to the iter-1 failure modes they address. |

**Net assessment:** Three correctable Critical defects and two correctable Major defects against a largely sound architectural remediation. Completeness and Internal Consistency are the primary score-drag dimensions. Post-correction the design has no fundamental architectural issues; ROOT-2, ROOT-3, and ROOT-4 are clean fixes.

---

## Execution Statistics

- **Total Findings:** 7
- **Critical:** 3 (FM-001-i2, FM-002-i2, FM-003-i2)
- **Major:** 2 (FM-004-i2, FM-005-i2)
- **Minor:** 2 (FM-006-i2, FM-007-i2)
- **Protocol Steps Completed:** 5 of 5
- **Total RPN (all findings):** 1,299
- **Highest RPN:** FM-001-i2 — 343 (Annotated tag tagger-date null in freshness check)
- **Elements Analyzed:** D7 digest monitor (E1), auto-revert circuit breaker (E2), bundle round-trip (E3), determinism contract (E4), D8 scanner (E5), D6 allow-list gate (E6)
- **ROOTs assessed:** ROOT-1 (mostly sound), ROOT-2 (sound), ROOT-3 (sound), ROOT-4 (sound), ROOT-5 (correctly deferred), ROOT-6 (partially sound — FM-003-i2)

---

*S-010 Self-Review applied per H-15 before persistence. Findings based on direct evidence from the three design documents; iter-1 finding files not read (blindness constraint honored). No sub-agents spawned (P-003). Evidence cited by section and pseudocode block for every finding (P-011). Severity not minimized (P-022).*
