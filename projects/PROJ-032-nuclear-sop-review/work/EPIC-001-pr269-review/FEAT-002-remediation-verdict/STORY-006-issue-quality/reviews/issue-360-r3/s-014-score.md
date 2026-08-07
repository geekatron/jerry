# Quality Score Report: GitHub Issue #360 — nuclear-sop OE artifact contract (REVISED DRAFT round 3)

## L0 Executive Summary
**Score:** 0.90/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Actionability (0.88)
**One-line assessment:** All 3 given Critical findings are stale — the flawed self-verifying grep was removed and replaced with an accurate, independently-verified mechanism — but the verify-checklist still covers only 2 of the 3 "what changed" claims, and the scoped diff still mixes one unrelated hunk into `sop-capture.md`, keeping composite just under threshold.

## Scoring Context
- **Deliverable:** `.../STORY-006-issue-quality/revised/issue-360.md` (round 3) | **Type:** Review-issue text | **Criticality:** C4
- **Ground truth used:** `remediation-register.md` REM-11, `evidence-c07033ce.md` (full commit diff + CI), worktracker `BUG-011-oe-artifact-contract` (existence confirmed)
- **SSOT:** quality-enforcement.md (weights, H-13), s-014-llm-as-judge.md (rubric) | **Scored:** 2026-08-07 | **Iteration:** 3

## Score Summary
| Metric | Value |
|---|---|
| Weighted Composite | **0.90** |
| Threshold (H-13) | 0.92 |
| Verdict | REVISE (0.85-0.91 band) |
| Strategy Findings Incorporated | Yes (9 strategies, ~28 findings) — most addressed/stale; 1 new gap found independently |
| Critical Findings Valid Against This Draft? | **No** |

## Dimension Scores
| Dimension | Weight | Score | Weighted | Evidence |
|---|---|---|---|---|
| Completeness | 0.20 | 0.89 | 0.178 | Covers what/why/changed/verify/tracking. Gaps: "confirm two things" names only 2 of 3 "What the fix changed" claims (retrieval-protocol fix in `sop-brief.md` has no named check); no cross-link to sibling issues (#357-#359/#361-#363) for the "seven fixes" claim (S-013-03, unaddressed). |
| Internal Consistency | 0.20 | 0.93 | 0.186 | Zero contradictions after full cross-check: "seven fixes"/"six unrelated" is arithmetically exact (REM-08..14 = 7 clusters, this is 1); retrieval-protocol fix correctly attributed to `sop-brief.md` only, not `sop-capture.md` (S-001-05 fixed); "three documents" count matches register G3 exactly. |
| Methodological Rigor | 0.20 | 0.90 | 0.180 | Every factual claim independently verified true against register/diff/CI: write path was already `.yaml` pre-fix; template+bb-003+worked-example each had `.md` at BOTH the local-capture and persistent-path mentions, now `.yaml`; AC-7 confirmed unsatisfiable pre-fix; 3-way retrieval-protocol drift confirmed (rules vs. sop-brief's workflow_type-only Glob vs. bb-003 B-24); Section 11 Attachments step confirmed added verbatim. Prior Critical grep defect (false-positive `experience/.*\.md`) fully remediated — see Verification section below. Residual: "sop-brief is the only agent retrieving OE entries" is an inference from REM-11's affected-files scope, not a direct read of `sop-executor.md`/`sop-verifier.md` (unavailable in this worktree); the scoped diff for `sop-capture.md` still mixes an unrelated REM-12 hunk, uncaveated (see New Finding). |
| Evidence Quality | 0.15 | 0.91 | 0.1365 | Commit hash, CI run URL (byte-for-byte match to evidence pack header, 15/15 green), 5 named files, and register section REM-11 all independently verifiable. Gap: no corroborating reference for the "seven fixes" count. |
| Actionability | 0.15 | 0.88 | 0.132 | Primary action ("nothing to do unless you disagree") is unambiguous. Verify steps are concrete and executable (fetch-if-needed + scoped diff + 2 named confirms), but an agent following the instructions literally is not directed to confirm the retrieval-protocol claim, and could mis-attribute the extra `execution_log_final` hunk in `sop-capture.md` to this fix. |
| Traceability | 0.10 | 0.92 | 0.092 | Commit hash, CI URL, register section, worktracker item path, and 5 named files all trace cleanly to ground truth artifacts. |
| **TOTAL** | **1.00** | | **0.9045 -> 0.90** | |

## Verification of Given Critical/Major Findings (independent re-check against round 3 text)
- **S-002-01 / S-003-01 / S-013-01 (Critical, grep false-positive on `experience/.*\.md`):** **STALE.** Round 3 removed this grep entirely, replacing it with a scoped `git diff` (5 named files) + 2 explicit manual confirms. Re-verified both confirms against `evidence-c07033ce.md`: (1) `POST_JOB_BRIEF.template.md`, `bb-003`, and `c3-adr-workflow-definition.md` each had BOTH `capture/oe-entry-{id}.md` and `docs/experience/{id}.md` corrected to `.yaml` — true; (2) `sop-capture.md` diff adds "Edit the workflow definition Section 11 (Attachments): append the OE entry reference `docs/experience/{entry_id}.yaml`" — true. **Not valid against this draft; does not block PASS.**
- **S-001-01 / S-007-01 (Major, unscoped diff):** Addressed — diff scoped to exactly the 5 relevant files, with a "six unrelated fixes" caveat added.
- **S-012-01 (Major, dead-end internal-branch pointer):** Addressed — footer now states "That branch is the maintainer's internal record; everything you need to act is above."
- **S-013-02 (fetch-first guidance):** Addressed. **S-003-02, S-010-02/03, S-001-05, S-011-03 (Minor phrasing/gloss issues):** all verified addressed in this draft. **S-013-03 (no sibling-issue cross-link):** still open.

## New Finding (identified independently, not in the 9-strategy set) — Minor
Even the scoped diff's `sop-capture.md` hunk mixes the REM-11 fix (Section 11 Attachments step) with an unrelated REM-12 change (`execution_log_final` boolean-to-path semantics). The caveat "(...an unscoped diff mixes them in)" implies the scoped diff avoids mixing; it only mostly does (file-level isolation achieved, one within-file mix remains).

## Required Edits to Reach PASS (>= 0.92)
1. In "How to verify," change `confirm two things:` to `confirm three things:` and append a third clause: `; and (3) agents/sop-brief.md Step 4 now searches by workflow_id first (Glob, then filter), applying workflow_type only as a post-read filter, never the initial search key.`
2. Extend the parenthetical to: `(the commit bundles six unrelated fixes; an unscoped diff mixes them in — even this scoped diff's sop-capture.md hunk includes one unrelated line on execution_log_final semantics, tracked separately).`
3. In "What this is," change `one of seven mechanical fixes` to `one of seven mechanical fixes (the other six: #357-#359, #361-#363)`.

## Leniency Bias Check
- [x] Each dimension scored independently before composite computed
- [x] Evidence cited per dimension from register/diff/CI, not impression
- [x] Uncertain scores resolved downward (0.9045 reported as 0.90; Actionability set at low end of its plausible range)
- [x] All 3 given Critical findings independently re-verified against ground truth rather than rubber-stamped or blindly trusted
- [x] No dimension scored > 0.95; one new gap identified beyond the supplied strategy findings
