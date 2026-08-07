# Chain-of-Verification Report: GitHub Issue #358 (BUG-009 registration-enforcement-surfaces)

**Strategy:** S-011 Chain-of-Verification (adapted for a ~300-word communication artifact)
**Deliverable:** `snapshots/final/issue-358.md` (live text of GitHub issue #358, geekatron/jerry)
**Criticality:** C4
**Date:** 2026-08-07
**Reviewer:** adv-executor (blind, S-011 lane)
**Claims Extracted:** 9 | **Verified:** 8 | **Discrepancies:** 1 (incompleteness, not contradiction)

## Summary

Every factual assertion checked against ground truth (remediation-register.md REM-09, remediation-log.md, pr269-verdict.md, and the live PR worktree diff/state) is accurate: commit `c07033ce`, branch `proj-0039-nuclear-engineer`, the three registration defects, the fix content, the CI link, and the tracking path all match. The one substantive gap is the "How to verify" command, which omits one of the three files the REM-09 fix actually touched. Two Minor polish items would improve a zero-context reader's experience. **Recommendation: ACCEPT with one Major correction (verify command) and optional Minor polish.**

## Findings Table

| ID | Claim | Verification | Severity |
|----|-------|--------------|----------|
| S-011-01 | "How to verify: ... run `git diff c07033ce^ c07033ce -- .context/rules/mandatory-skill-usage.md AGENTS.md`" | Commit `c07033ce` also modified a third file within REM-09's own affected-files list (the phase-6 collision-analysis artifact, corrected/superseded per the register). The given command won't show it. | Major |
| S-011-02 | Title opens with `PROJ-032/BUG-009:` | Internal tracking codes precede any explanation; codes are only decoded later, in the "Tracking" footer. | Minor |
| S-011-03 | "one of seven mechanical fixes ... in commit `c07033ce`" | Correct (register: 7 FIX-NOW clusters, REM-08..14, all in `c07033ce`) but the other six issue numbers (#357, #359–#363) are never linked. | Minor |
| S-011-04 | "AGENTS.md gets the missing section link, a summary row, and the corrected total of 93" | Accurate but incomplete: the same diff also updates the "Last verified" date and appends `sop-*` to the MCP "Not included by design" note (both part of REM-09 group G3 / fix spec item 4). | Minor |

## Finding Details

### S-011-01: Verify command omits one of three changed files [MAJOR]

**Claim (from issue):** "How to verify: on `proj-0039-nuclear-engineer`, run `git diff c07033ce^ c07033ce -- .context/rules/mandatory-skill-usage.md AGENTS.md`."

**Source Document:** remediation-register.md, REM-09 "Affected files" list: `.context/rules/mandatory-skill-usage.md`, `AGENTS.md`, and the "phase-6 collision-analysis artifact under «PR projects tree»/PROJ-0039-nuclear-engineer". Confirmed in the full diff (evidence-c07033ce.md): the diff also touches `.../orchestration/nuclear-sop-build-20260325-001/eng/phase-6/eng-reviewer-001/registration-trigger-map-row.md`, adding a "CORRECTED / SUPERSEDED (2026-08-07, PROJ-032 remediation register REM-09)" note that directly documents the fix to claim (2) in the issue body (the "nuclear workflow" misroute).

**Discrepancy:** The verify command shows 2 of the 3 files this specific bug's fix touched. A reader who runs exactly the given command and stops there will not see the annotation that corrects the PR's own (inaccurate) collision-analysis claim — the very claim the issue says was false.

**Severity:** Major — the verify instruction is the artifact's single actionable payload; an incomplete verification command undercuts the "verify it yourself" promise on the specific claim most likely to be double-checked (the routing collision).

**Correction:** Append the third path to the command, e.g.:
`git diff c07033ce^ c07033ce -- .context/rules/mandatory-skill-usage.md AGENTS.md «PR projects tree»/PROJ-0039-nuclear-engineer/orchestration/nuclear-sop-build-20260325-001/eng/phase-6/eng-reviewer-001/registration-trigger-map-row.md`
(path taken from the branch's own tree, not this review repo).

### S-011-02: Title leads with undecoded internal codes [MINOR]

**Claim:** Title: "PROJ-032/BUG-009: nuclear-sop — skill missing from enforcement lists, ..."

**Discrepancy:** `PROJ-032` and `BUG-009` are the maintainer's internal project/bug identifiers. They are meaningful only after reading the "Tracking" line at the bottom of the issue, which already restates the same codes in context. A zero-context reader hits two unexplained tokens before the descriptive part of the title.

**Correction:** Drop the `PROJ-032/BUG-009:` prefix from the title (it is preserved in the "Tracking" footer already), or move it to a trailing parenthetical: "nuclear-sop: skill missing from enforcement lists, "nuclear workflow" misrouted, agent count wrong (fixed on your branch; internal ref BUG-009)".

## Recommendations

- **Major:** S-011-01 — extend the verify command to cover all three files the fix touched (correct value confirmed above from the full diff).
- **Minor (optional):** S-011-02 — de-emphasize/relocate the internal code prefix in the title.
- **Minor (optional):** S-011-03 — add "Sibling fixes in the same commit: #357, #359, #360, #361, #362, #363" so a reader auditing `c07033ce` has the full map.
- **Minor (optional):** S-011-04 — extend the "What the fix changed" AGENTS.md sentence to mention the refreshed "Last verified" date and the added `sop-*` MCP exclusion note, for a complete diff summary.

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | S-011-01: verify command covers 2/3 changed files; S-011-04: fix summary omits 2 of 5 changed AGENTS.md items |
| Internal Consistency | 0.20 | Neutral | No contradictions found in the claims verified |
| Methodological Rigor | 0.20 | Neutral | Claims about mechanism (priority routing, compound-trigger override) are correctly stated |
| Evidence Quality | 0.15 | Positive | All checked facts (commit, branch, CI link, counts) verified byte-for-byte against source |
| Actionability | 0.15 | Negative | S-011-01: the one actionable instruction in the issue is incomplete |
| Traceability | 0.10 | Negative | S-011-02: title codes precede their own definition |
