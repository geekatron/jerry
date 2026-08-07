# Verification Report: STORY-027

> **Type:** verification-report
> **Generated:** 2026-08-05T00:00:00Z
> **Agent:** wt-verifier
> **Scope:** full (acceptance criteria + evidence + entity-file bookkeeping)

---

## Navigation

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Verdict at a glance |
| [Acceptance Criteria Verification](#acceptance-criteria-verification) | Per-AC evidence mapping |
| [Blocking Issues](#blocking-issues) | What prevents closure right now |
| [Recommendations](#recommendations) | Required and optional follow-ups |
| [Ready for Closure](#ready-for-closure) | Overall verdict and rationale |
| [Evidence Summary](#evidence-summary) | Artifact and test evidence inventory |
| [Detailed Verification](#detailed-verification) | Per-AC deep dive |
| [Entity-File Bookkeeping Findings](#entity-file-bookkeeping-findings) | Discrepancies between reality and the tracked entity file |
| [Corrections to Task-Provided Evidence](#corrections-to-task-provided-evidence) | Factual correction (P-022/WTI-003) |
| [Appendix: WTI Rule Compliance](#appendix-wti-rule-compliance) | Rule-by-rule compliance table |

---

## Summary

| Metric | Value |
|--------|-------|
| **Work Item** | STORY-027 — CVE accept-list |
| **Current Status (entity file)** | `in_progress` |
| **Evidence-Based AC Score** | 5 / 5 (100%) |
| **Entity-File Checkbox Score** | 0 / 5 (0%) |
| **Verdict (technical/substance)** | PASS — all 5 acceptance criteria are met by concrete, reproducible evidence |
| **Verdict (closure readiness)** | **NOT_READY** — blocked solely by stale entity-file bookkeeping, not by missing work |

---

## Acceptance Criteria Verification

| # | Criterion | Verified | Evidence |
|---|-----------|----------|----------|
| 1 | A checked-in CVE accept-list file exists with a documented schema (package, CVE ID, expiry date, rationale fields) | ✅ | [`.github/security/audit-allowlist.yml`](../../../../../../.github/security/audit-allowlist.yml) (50 lines) — header comment documents `id`, `package`, `reason`, `accepted_by`, `accepted_on`, `review_by`, `ticket` |
| 2 | The shared composite action (from STORY-026) reads the accept-list and suppresses listed CVEs from the audit failure output | ✅ | [`.github/actions/security-audit/action.yml`](../../../../../../.github/actions/security-audit/action.yml) step `Parse accept-list and check expiry` (id: `allowlist`) invokes `scripts/security/audit_allowlist.py`, captures `IGNORE_FLAGS`; step `Run pip-audit` (id: `audit`) passes `$IGNORE_FLAGS` to `pip-audit --ignore-vuln ...` |
| 3 | A CI check or scan step fails with a clear error message if any accept-list entry's expiry date has passed | ✅ | `scripts/security/audit_allowlist.py` lines 179–189: `if today >= review_by:` → `::error::{entry_label}: expired (review_by: {review_by}, today: {today})...`, exit 1. `action.yml` step wraps this: non-zero exit → `::error::CVE accept-list check failed (exit $ALLOWLIST_EXIT)...`, `exit 1`. Confirmed live: `verification-evidence-20260805.md` Claim C-1 and Claim E |
| 4 | At least one entry in the accept-list is validated end-to-end (entry added, suppression confirmed, expiry breach detected when date is set to past) | ✅ | `tests/security/test_audit_allowlist.py::TestValidUnexpiredEntry` (entry added, `--ignore-vuln` flag emitted, exit 0, verified via both direct `main()` call and full `subprocess` invocation of the real script) + `TestExpiryBoundary::test_main_exits_one_when_expired` / `test_subprocess_expired_exits_one` (same entry mechanics, `review_by` set to today → exit 1). Corroborated manually in `verification-evidence-20260805.md` Claims C-1/C-2/C-3 and Smoke-test |
| 5 | The accept-list schema and governance process are documented in the repository | ✅ (minor optional gap) | Documented in 3 checked-in locations: (a) inline SCHEMA + WORKFLOW header of `audit-allowlist.yml`, (b) `projects/PROJ-024-tactical-work/decisions/ADR-secscan-hardening-001.md` §D2 (schema, expiry semantics, approval flow), (c) module docstring of `audit_allowlist.py` (exit-code contract). Governance enforced via `.github/CODEOWNERS` (`.github/security/ @geekatron`). Gap: the ADR's own file-change plan flagged `.github/security/README.md` as "optional but recommended" — it was **not** created. Not a blocking gap since the ADR itself scoped it as optional and the schema/process are documented elsewhere in the repo. |

**Verification Score Calculation:**
- Total criteria: 5
- Verified (evidence-based): 5
- Score: 100% (5 / 5 × 100)

**Threshold:** 80% required for closure — **met** on an evidence basis.

---

## Blocking Issues

### Critical Blockers

1. **Entity-file acceptance-criteria checkboxes not updated** (all 5 ACs)
   - Impact: `STORY-027-cve-accept-list.md` still shows `- [ ]` (unchecked) for all 5 criteria despite all 5 being independently verified as met. Per WTI-002, closure requires the tracked checkbox state to reflect verified completion — the file's own signal currently reads 0%.
   - Remediation: Check all 5 acceptance-criteria boxes in the entity file, citing this report as evidence.
   - Estimated effort: 5 minutes (editorial only).

2. **`Status` frontmatter field stale** (`in_progress`)
   - Impact: Entity is functionally complete but frontmatter does not reflect it.
   - Remediation: Update `Status:` to `done`/`completed` per project status vocabulary once the AC checkboxes are updated.
   - Estimated effort: 1 minute.

3. **Delivery Evidence table note is factually stale**
   - Impact: The note "pending merge — close on merge + AC verification" against PR #302 is inaccurate — PR #302 merged to `main` on 2026-06-23T16:37:26Z (commit `81c7c61c`, confirmed on `main` via `git merge-base --is-ancestor`), roughly six weeks before this verification. Leaving this note as-is risks a false "still pending" signal (WTI-003 truthful state).
   - Remediation: Update the note to reflect merged status and link this verification report + `verification-evidence-20260805.md`.
   - Estimated effort: 2 minutes.

> **None of the above blockers reflect missing engineering work.** All three are editorial/bookkeeping corrections to the entity file. This verifier does not modify entity files (P-020); the corrections must be applied by the requesting agent/human.

---

## Recommendations

### Required (for closure)

1. Update `STORY-027-cve-accept-list.md`: check all 5 AC boxes, set `Status: done`, correct the Delivery Evidence note, and add a `History` row for the verification date (2026-08-05) referencing this report.
2. Reference this report (`wt-verifier-STORY-027-20260805.md`) and `verification-evidence-20260805.md` from the entity's Delivery Evidence table as the AC-verification artifact.

### Optional Improvements

1. **Add `.github/security/README.md`** — The ADR (line 631) recommended this as "optional but recommended" so future maintainers don't have to reconstruct the accept-list/approval workflow from the ADR or the YAML header comment. Priority: Low.
2. **Add an explicit PyYAML dev dependency** — `scripts/security/audit_allowlist.py` currently relies on PyYAML being present transitively via `mkdocs-material` (see the script's own `NOTE`/`RECOMMENDED FOLLOW-UP` comment, referencing GitHub issue #301). Priority: Low — not an AC-027 requirement, but a latent fragility the story's own code flags.
3. **Populate the `Children (Tasks)` table** — currently a placeholder row ("tasks to be decomposed during implementation"); since implementation is done, either remove the placeholder or note that no task-level decomposition was needed. Priority: Cosmetic.

---

## Ready for Closure

**NOT_READY** — All 5 acceptance criteria are substantively satisfied by strong, reproducible evidence (composite-action wiring, fail-closed parser behavior, automated pytest suite with subprocess-level end-to-end coverage, and multi-location documentation). However, the entity file itself has not been updated to reflect that verified state: all 5 AC checkboxes remain unchecked, `Status` remains `in_progress`, and the Delivery Evidence table's merge note is stale by roughly six weeks. Per WTI-001 (Real-Time State) and WTI-002 (No Closure Without Verification, checkbox-based signal), the entity file's own tracked state — not just external evidence — must reflect completion before a DONE/COMPLETED transition. This is a purely editorial gap; **no further engineering, testing, or documentation work is required** to close this story. Once the entity file is updated per [Blocking Issues](#blocking-issues) items 1–3, the story is immediately READY_FOR_CLOSURE.

**Closure Criteria Assessment:**

| Criterion | Met? | Details |
|-----------|------|---------|
| 80%+ acceptance criteria verified (evidence basis) | ✅ Yes | 5/5 (100%) — see [Acceptance Criteria Verification](#acceptance-criteria-verification) |
| 80%+ acceptance criteria verified (entity-file checkbox basis) | ❌ No | 0/5 (0%) — checkboxes not updated in the tracked file |
| Evidence section has ≥1 link | ✅ Yes | Delivery Evidence table cites PR #302 / commit `81c7c61c`; this report and `verification-evidence-20260805.md` add further verifiable evidence |
| All child items completed | ✅ N/A | No child tasks were decomposed (placeholder row only); nothing outstanding |
| No blocking impediments | ✅ Yes | No impediment entity found referencing STORY-027 |

---

## Work Item Details

**ID:** STORY-027

**Title:** Add Owner-Governed CVE Accept-List with Mandatory Expiry/Re-Review

**Type:** story

**Current Status:** `in_progress` (entity file) — functionally complete per evidence

**Parent:** FEAT-002 — Security-scan pipeline hardening

**Children:** 0 (placeholder row only, no task decomposition performed)

---

## Evidence Summary

**Total Evidence Links:** 3 primary sources + 4 artifact files + 1 automated test suite

**Evidence Quality:** High. Evidence spans three independent layers: (1) source code inspection of the delivered artifacts, (2) an automated, repeatable pytest suite (50/50 passing, including subprocess-level invocation of the real script against real temp files — not mocked), and (3) an independent local manual verification pass (`verification-evidence-20260805.md`) that exercises the same behaviors via direct CLI invocation with concrete stdout/stderr transcripts. All three layers agree.

**Evidence Links:**
- `.github/security/audit-allowlist.yml` (50 lines, confirmed present on `main` at HEAD)
- `.github/actions/security-audit/action.yml` (277 lines; allowlist-parsing and pip-audit steps inspected directly)
- `scripts/security/audit_allowlist.py` (282 lines; fail-closed parser, confirmed via direct source read)
- `tests/security/test_audit_allowlist.py` (485 lines; `TestValidUnexpiredEntry`, `TestMissingRequiredField`, `TestMalformedYaml`, `TestNinetyDayCap`, `TestExpiryBoundary`, `TestEmptyAllowlist` — all classes read and cross-checked against ACs 1–4)
- `pytest tests/security/` — 50 passed (re-confirmed present in `verification-evidence-20260805.md`; test source independently inspected in this pass)
- `projects/PROJ-024-tactical-work/decisions/ADR-secscan-hardening-001.md` §D2 (schema/governance documentation, AC-5)
- `.github/CODEOWNERS` (confirms `.github/security/ @geekatron` governance gate)
- Commit `81c7c61c` — confirmed present on `main` via `git merge-base --is-ancestor 81c7c61c origin/main` (YES)
- PR **#302** (not #304 — see [Corrections to Task-Provided Evidence](#corrections-to-task-provided-evidence)) — `state: MERGED`, `mergedAt: 2026-06-23T16:37:26Z`

---

## Detailed Verification

### AC-1: Checked-in accept-list file with documented schema

`.github/security/audit-allowlist.yml` is present at the expected path and is currently checked in with `accepted: []` (empty by design — the story's own header comment explains that the 9 known CVEs at delivery time all had upstream fixes and therefore none were added to the list; this is consistent with STORY-030's remediation scope). The header comment documents a `SCHEMA:` block enumerating all 7 required fields (`id`, `package`, `reason`, `accepted_by`, `accepted_on`, `review_by`, `ticket`) with type and semantics for each, satisfying "package, CVE ID, expiry date, rationale fields" (mapped to `package`, `id`, `review_by`, `reason` respectively) plus additional governance fields (`accepted_by`, `accepted_on`, `ticket`) beyond the AC's minimum bar.

**Verdict:** PASS.

### AC-2: Composite action reads accept-list and suppresses listed CVEs

`action.yml` step `id: allowlist` runs `uv run python scripts/security/audit_allowlist.py --allowlist ${{ inputs.allowlist-path }}`, captures stdout as `IGNORE_FLAGS`, and exports it via `$GITHUB_OUTPUT`. The subsequent `id: audit` step interpolates `IGNORE_FLAGS="${{ steps.allowlist.outputs.ignore_flags }}"` directly into the `pip-audit` invocation (`... $IGNORE_FLAGS ...`), which is exactly the `--ignore-vuln <id>` mechanism `pip-audit` uses natively to suppress specific, matched vulnerability IDs from its failure output.

**Verdict:** PASS.

### AC-3: CI check fails with clear error message on expiry breach

`audit_allowlist.py::_validate_entries` computes `today >= review_by` (inclusive semantics, matching ADR D2's decision and STORY-027's own off-by-one fix, see AC-4/Claim E) and appends `::error::{entry_label}: expired (review_by: {review_by}, today: {today}). ...` to the error list; `main()` prints these to stderr and returns 1. `action.yml`'s `allowlist` step treats any non-zero exit from the script as fatal: `echo "::error::CVE accept-list check failed (exit $ALLOWLIST_EXIT) — see errors above. Action halted."` followed by `exit 1`. This produces GitHub Actions-native `::error::` annotations at both the granular (per-entry) and step (summary) level — a "clear error message" by GitHub Actions convention.

**Verdict:** PASS.

### AC-4: End-to-end validation of at least one entry (add → suppress → expire)

The production `audit-allowlist.yml` ships empty (`accepted: []`) by design, so there is no *live, checked-in* production entry exercising the full lifecycle. However, the AC's requirement — "entry added, suppression confirmed, expiry breach detected when date is set to past" — is satisfied, and satisfied more rigorously than a single manual pass would provide, via the automated test suite:

- `TestValidUnexpiredEntry::test_main_exits_zero` / `test_main_prints_ignore_flag` — a synthetic entry (`CVE-2099-00001`) is written to a real temp YAML file and parsed via `main()`; exit 0 and `--ignore-vuln CVE-2099-00001` in stdout confirm suppression.
- `TestValidUnexpiredEntry::test_subprocess_exit_zero_and_flag_present` — the *same* scenario re-run as a full `subprocess.run([...python..., SCRIPT_PATH, --allowlist, f])` invocation of the actual on-disk script (not an in-process import), i.e., the real CI invocation path.
- `TestExpiryBoundary::test_main_exits_one_when_expired` / `test_subprocess_expired_exits_one` — the same entry shape with `review_by` set to `date.today()` (boundary case, inclusive expiry) is re-validated via both `main()` and the real subprocess path; both exit 1.

This constitutes an entry being added, its suppression being confirmed, and its expiry breach being detected when the date is set to (on/into) the past — executed twice (in-process and subprocess) and independently corroborated by the manual local run recorded in `verification-evidence-20260805.md` (Claims C-1/C-2/C-3, E).

**Verdict:** PASS — satisfied via automated, repeatable tests rather than a manually-added production entry; this is stronger evidence (reproducible in CI on every run) than a one-off manual edit to the production file would have been, and is a reasonable interpretation of "validated end-to-end" for a fail-closed security control.

### AC-5: Schema and governance process documented in the repository

Three independent, checked-in documentation surfaces exist:

1. `audit-allowlist.yml` header — `SCHEMA:` (field-by-field) and `WORKFLOW:` (5-step CVE-appears → verify-fix → add-entry → open-tracking-issue → re-assess-at-`review_by`) sections.
2. `ADR-secscan-hardening-001.md` §D2 ("Owner Accept-List for Transitive CVEs") — schema table, expiry semantics (`review_by <= today` → expired), and the "code-owner PR" approval flow, at ADR-level rigor (~100 lines of design rationale).
3. `audit_allowlist.py` module docstring — documents the fail-closed exit-code contract (0 = valid, 1 = any error class) and the exact invocation pattern used by the composite action.
4. `.github/CODEOWNERS` — `.github/security/ @geekatron` operationalizes the "governance process" (edits require maintainer review), corroborated by the ADR's explicit call-out that this entry is load-bearing for the approval guarantee.

**Gap (non-blocking):** The ADR's own File-Change Plan (line 631) listed `.github/security/README.md` as "New doc (**optional but recommended**)" to spare future maintainers from reconstructing the process from the ADR. This file does not exist. Since the ADR itself scoped it as optional, and the schema/process are substantively documented in three other checked-in locations, this is a recommendation, not a blocker for AC-5.

**Verdict:** PASS (with a noted optional-doc gap, tracked as a recommendation, not a blocker).

### Child Item Status

No child tasks exist under STORY-027; the `Children (Tasks)` table contains only a placeholder row ("tasks to be decomposed during implementation"). Since implementation is complete without task-level decomposition having occurred, there is nothing outstanding here. N/A for closure gating.

### Impediments Check

No impediment entity referencing STORY-027 was found under `projects/PROJ-024-tactical-work/work/`. No blocking impediments identified.

### Evidence Validation

All cited evidence resolves to files/commits that exist:
- `.github/security/audit-allowlist.yml` — exists, read directly.
- `.github/actions/security-audit/action.yml` — exists, read directly (relevant sections).
- `scripts/security/audit_allowlist.py` — exists, read directly (282 lines confirmed via `wc -l`).
- `tests/security/test_audit_allowlist.py` — exists, read directly; 6 test classes confirmed.
- Commit `81c7c61c` — confirmed present on `main` (`git merge-base --is-ancestor` → true).
- PR #302 — confirmed `MERGED` via `gh pr view 302` (`mergedAt: 2026-06-23T16:37:26Z`).
- `verification-evidence-20260805.md` — exists at the cited path, content cross-checked against source rather than taken at face value.

No placeholder links (`TODO`, `TBD`, `#`) found in any cited evidence.

---

## Entity-File Bookkeeping Findings

| Field | Entity File Currently Shows | Actual State | Discrepancy |
|-------|------------------------------|---------------|--------------|
| `Status` | `in_progress` | Functionally complete, all 5 ACs verified | Stale — not updated post-merge |
| AC checkboxes (all 5) | `- [ ]` (unchecked) | All 5 independently verified PASS | Stale — 0% vs. 100% evidence-based |
| Delivery Evidence note (PR #302 row) | "CVE accept-list implemented; pending merge — close on merge + AC verification" | PR #302 merged 2026-06-23T16:37:26Z (≈6 weeks before this verification) | Stale — merge already happened; note not updated |
| History table | Last entry 2026-06-23 (`in_progress`) | Verification performed 2026-08-05 | Missing entry for the verification event |

---

## Corrections to Task-Provided Evidence

Per P-022 (no deception) / WTI-003 (truthful state), this section documents a factual correction found during verification:

- The verification task's "Evidence available" section states: *"Delivered on main via PR #304 commit 81c7c61c."* This is **incorrect**. `gh pr view` confirms commit `81c7c61c` ("ci: harden dependency security-scan pipeline (#301)") was delivered via **PR #302** (`MERGED`, `mergedAt: 2026-06-23T16:37:26Z`, merge commit `f0152808ed07...`), which matches the entity file's own Delivery Evidence table. **PR #304** is a separate, later PR ("docs(proj-024): security-scan hardening — ADR, worktracker, analysis & adversarial reviews (3/3)", `MERGED`, `mergedAt: 2026-06-28T18:00:46Z`) that delivered documentation/worktracker artifacts, not the accept-list code itself. This does not change any AC verdict — it is a citation correction only, recorded here so it is not silently propagated into the closure record.

---

## Verification Timeline

| Timestamp | Event |
|-----------|-------|
| 2026-08-05T00:00:00Z | `verification-evidence-20260805.md` local manual verification pass completed (prior artifact, read as input evidence) |
| 2026-08-05 (this session) | Entity file read; 5 ACs extracted |
| 2026-08-05 (this session) | Source inspection: `audit-allowlist.yml`, `action.yml`, `audit_allowlist.py`, `test_audit_allowlist.py` |
| 2026-08-05 (this session) | `git`/`gh` cross-checks: commit ancestry on `main`, PR #302 and #304 state |
| 2026-08-05 (this session) | Per-AC verdicts rendered; this report generated |

---

## Next Actions

### If Approved for Closure

1. Update `STORY-027-cve-accept-list.md`: check all 5 AC boxes.
2. Update `Status:` frontmatter to `done`/`completed`.
3. Correct the Delivery Evidence table note (merged, not pending) and add this report + `verification-evidence-20260805.md` as citations.
4. Add a `History` row for 2026-08-05 documenting the verification and closure.
5. Archive this verification report (already at its intended path).

### If Rejected

Not applicable — no AC is rejected. The only outstanding items are the entity-file bookkeeping updates listed above.

---

## Appendix: WTI Rule Compliance

| Rule | Status | Notes |
|------|--------|-------|
| WTI-001: Real-Time State | ❌ Not met | Entity file (`Status`, checkboxes, Delivery Evidence note) has not been updated to reflect the merge (2026-06-23) or the verification (2026-08-05); state has drifted from reality for ~6 weeks |
| WTI-002: No Closure Without Verification | ⚠️ Partially met | Evidence-based AC score is 100% (5/5); entity-file checkbox score is 0% (0/5). The rule's checkbox-based signal fails; the underlying evidentiary bar is met |
| WTI-003: Truthful State | ❌ Not met (entity file) / ✅ Met (this report) | Entity file's "pending merge" note is now false. This report corrects the record and flags a PR-number discrepancy found in the verification task's own evidence input |
| WTI-005: Atomic State Updates | ✅ N/A | No partial/concurrent update conflict observed |
| WTI-006: Evidence-Based Closure | ✅ Met | ≥1 verifiable evidence link present (PR #302, commit `81c7c61c`, `verification-evidence-20260805.md`); all links resolve to real, non-placeholder artifacts |

---

*Report generated by wt-verifier v1.0.0*
*WTI Rules Enforced: WTI-001, WTI-002, WTI-003, WTI-006*
*Constitutional Compliance: P-001, P-002, P-003, P-004, P-020, P-022*
*Entity file NOT modified by this verification pass, per P-020 guardrail.*
