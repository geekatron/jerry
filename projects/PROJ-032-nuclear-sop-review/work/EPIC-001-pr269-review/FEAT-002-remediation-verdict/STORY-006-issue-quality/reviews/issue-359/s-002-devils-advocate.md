# Devil's Advocate Report: GitHub Issue #359 (issue-359.md)

**Strategy:** S-002 Devil's Advocate
**Deliverable:** `projects/PROJ-032-nuclear-sop-review/work/EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-006-issue-quality/snapshots/final/issue-359.md`
**Criticality:** C4 (tournament)
**Date:** 2026-08-07
**Reviewer:** adv-executor (S-002)
**H-16 Compliance:** Orchestrator-level group sequencing places `self-refine -> steelman -> challenge` groups in order per the tournament design; this blind executor received no direct S-003 artifact reference. Proceeding on that basis; if the orchestrator did not in fact run a steelman pass before this challenge group, that is an H-16 process gap for the orchestrator to reconcile, not evidence found in the deliverable itself.

## Summary

Fact-checking against the remediation register, remediation log, and commit evidence confirms every load-bearing claim in issue #359 is accurate (branch, commit, error counts 4/2, "one YAML unparseable," 8/8 post-fix validity, 15/15 CI, tracking path). The strongest counter-argument is not about facts but about the "How to verify" instruction: the prescribed `git diff` command scopes to two directories that also carry three *other* remediation clusters' changes in the same commit, so following the instruction literally will not isolate evidence for this issue's claim. 4 counter-arguments identified (1 Major on verification precision, 3 Minor on concision/self-containedness). Recommend ACCEPT with minor revisions.

## Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| S-002-01 | "How to verify" diff command is scoped too broadly and will show unrelated fixes | Major | `git diff c07033ce^ c07033ce -- skills/nuclear-sop/agents/ skills/nuclear-sop/composition/` (line 11) | Actionability |
| S-002-02 | Body exceeds the ~300-word compact budget for this artifact type | Minor | Full body ≈ 330-340 words across 4 labeled paragraphs | Traceability/Concision |
| S-002-03 | Title prefix "PROJ-032/BUG-010" is an undecoded internal code at first read | Minor | Title line 1 | Completeness (self-containedness) |
| S-002-04 | "the repo standard anchors agent output under the active project directory" omits the concrete pattern | Minor | Line 7, parenthetical | Actionability |

## Finding Details

### S-002-01: Verification command mixes four remediation clusters into one diff [MAJOR]

**Claim Challenged:** "How to verify: on `proj-0039-nuclear-engineer`, run `git diff c07033ce^ c07033ce -- skills/nuclear-sop/agents/ skills/nuclear-sop/composition/`."

**Counter-Argument:** Commit `c07033ce` is a single combined commit implementing all seven FIX-NOW clusters (REM-08..14) at once (confirmed: remediation-log.md "Outcome" — "implements all seven FIX-NOW clusters"). Cross-referencing the register's per-cluster "Affected files" lists shows `skills/nuclear-sop/agents/` and `skills/nuclear-sop/composition/` are *also* touched by REM-11 (OE artifact contract — e.g. `agents/sop-brief.md` Step 4 OE-retrieval-protocol rewrite, `agents/sop-capture.md`) and REM-13 (composition drift — all 8 `composition/` files, plus `agents/sop-executor.md`, `agents/sop-brief.governance.yaml`), tracked as separate issues #360 and #362. The evidence pack's own diff of `agents/sop-brief.md` (evidence-c07033ce.md, Step 4 hunk) shows exactly this: the OE-search-mechanism rewrite (REM-11) and a new "OE INJECTION (SEC-002)" forbidden action (REM-13 forbidden-action parity) sit in the same file, same commit, same directory scope this issue tells the reader to diff.

**Evidence:** `evidence-c07033ce.md` full diff, `agents/sop-brief.md` hunks (Step 4 OE History Review rewrite; new forbidden action append); `remediation-register.md` REM-11 and REM-13 "Affected files" rows both list `skills/nuclear-sop/agents/` and/or `skills/nuclear-sop/composition/` paths overlapping REM-10's.

**Impact:** An external contributor or their AI agent following the literal instruction will see hunks unrelated to schema/standards conformance (OE retrieval protocol changes, SEC-001 guard restoration) inside the same diff output, with nothing in the issue distinguishing "this is REM-10's part" from "this is someone else's fix." They may either (a) over-attribute unrelated changes to this issue's fix, or (b) lose confidence in the issue's scope claim when the diff looks bigger/different than described.

**Dimension:** Actionability

**Response Required:** Narrow the verify command to file-level paths that are REM-10-exclusive, e.g. `git diff c07033ce^ c07033ce -- skills/nuclear-sop/agents/*.governance.yaml skills/nuclear-sop/composition/sop-verifier.agent.yaml skills/nuclear-sop/composition/sop-brief.agent.yaml`, or add one clause: "note: this diff also includes unrelated fixes tracked in #360/#362 — schema/standards changes are the `.governance.yaml` files and the two named `.agent.yaml` files."

**Acceptance Criteria:** Revised command (or added caveat) lets a reader distinguish REM-10 hunks from REM-11/REM-13 hunks without cross-referencing the register.

### S-002-02: Body length exceeds the compact-artifact budget [MINOR]

**Claim Challenged:** N/A — a structural observation, not a specific sentence.

**Counter-Argument:** The four labeled paragraphs total roughly 330-340 words (title/tracking excluded from the ~300-word target but included in reader effort). The "What was wrong" paragraph alone runs ~150 words and stacks four distinct standards-conformance defects (section numbering, output location, tool-name-in-prose, missing reasoning_effort) into one sentence chain separated only by semicolons, which is harder to scan than a short list.

**Evidence:** Line 7, "Beyond the validators: ... ; ... ; ... ; and ..." — four independent defects in one sentence.

**Impact:** Minor scan-friction; does not change correctness or actionability.

**Dimension:** Traceability/Concision (rubric's implicit concision criterion)

**Response Required:** Consider breaking the four "beyond the validators" items into a short bullet list or splitting into two sentences.

**Acceptance Criteria:** Not required to block acceptance; acknowledgment sufficient.

### S-002-03: Undecoded internal code in title [MINOR]

**Claim Challenged:** Title: "PROJ-032/BUG-010: nuclear-sop — agent metadata files failed schema validation..."

**Counter-Argument:** "PROJ-032" and "BUG-010" are internal worktracker codes. A reader with zero repo governance knowledge cannot decode them from the title alone; they are only implicitly resolvable later via the Tracking footer's path `projects/PROJ-032-nuclear-sop-review/work/BUG-010-agent-schema-conformance`. The title-level prefix adds no information the descriptive clause after the colon doesn't already carry, and it's the first thing an external contributor's triage bot or human eye sees.

**Evidence:** Title line 1 vs. Tracking line 14 (the decode only happens 13 lines later).

**Impact:** Low — the descriptive half of the title is fully self-contained on its own; the codes are inert prefix noise for this audience, not a blocker to understanding.

**Dimension:** Completeness (self-containedness)

**Response Required:** Optional: drop the `PROJ-032/BUG-010:` prefix from the issue title (keep it only in the Tracking footer where it's already explained), or keep for internal cross-referencing consistency across all 14 sibling issues — acknowledgment sufficient either way.

**Acceptance Criteria:** Acknowledgment sufficient; no block on acceptance.

### S-002-04: "active project directory" convention left unstated [MINOR]

**Claim Challenged:** "none of the four agents declared where its output files go (the repo standard anchors agent output under the active project directory)."

**Counter-Argument:** This parenthetical explains the standard in the abstract but never states the concrete path pattern that was actually applied (`projects/${JERRY_PROJECT}/nuclear-sop/{workflow_id}/...`, per the fix diff's `output.location` changes). Since this is a "what was wrong" / "what changed" narrative rather than a call to action, the omission doesn't block understanding, but a reader curious about the actual convention has no in-issue answer and must open the governance files themselves.

**Evidence:** Line 7 parenthetical vs. `evidence-c07033ce.md` diff showing `location: "projects/${JERRY_PROJECT}/nuclear-sop/{workflow_id}/brief/pre-job-brief.md"`.

**Impact:** Low — informational completeness gap only; nothing for the reader to act on incorrectly.

**Dimension:** Actionability

**Response Required:** Optional: name the pattern inline, e.g. "(the repo standard anchors agent output under `projects/${JERRY_PROJECT}/...`)."

**Acceptance Criteria:** Acknowledgment sufficient.

## Recommendations

- **P1 (Major — SHOULD resolve):** S-002-01 — narrow or caveat the verification diff scope so REM-10-specific evidence is distinguishable from REM-11/REM-13 changes sharing the same commit and directories.
- **P2 (Minor — MAY resolve):** S-002-02 (tighten "beyond the validators" sentence), S-002-03 (consider dropping title code prefix), S-002-04 (name the concrete output-path pattern inline).

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Slightly Negative | S-002-03: title codes undecoded until the footer |
| Internal Consistency | 0.20 | Neutral | No contradictions found; all facts cross-verified against register/log/evidence |
| Methodological Rigor | 0.20 | Neutral | N/A — this is a communication artifact, not a methodology document |
| Evidence Quality | 0.15 | Positive | Every substantive claim (branch, commit, error counts, 8/8, 15/15) independently confirmed against ground truth |
| Actionability | 0.15 | Negative | S-002-01: verify command will surface confusing, over-broad diff output |
| Traceability | 0.10 | Slightly Negative | S-002-02: dense paragraph reduces scanability of the four bundled defects |

**Overall assessment:** Proceed with minor revisions. The issue is factually sound and well-scoped in its claims; the one substantive gap is a verification instruction that doesn't match its own commit's actual file-change footprint.
