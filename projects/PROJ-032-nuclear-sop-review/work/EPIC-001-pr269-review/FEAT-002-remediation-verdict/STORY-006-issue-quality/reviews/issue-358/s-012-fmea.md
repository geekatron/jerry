# FMEA Report: GitHub Issue #358 (BUG-009 / REM-09, nuclear-sop registration enforcement surfaces)

**Strategy:** S-012 FMEA (adapted for a ~300-word communication artifact)
**Deliverable:** `snapshots/final/issue-358.md` (live text of geekatron/jerry issue #358)
**Criticality:** C4 (tournament)
**Date:** 2026-08-07
**H-16 Compliance:** N/A for FMEA execution on a communication artifact (no S-003 dependency for this template application)
**Elements Analyzed:** 6 | **Failure Modes Identified:** 5 | **Total RPN:** ~567

## Summary

Decomposed the issue into 6 elements (title, "what this is," "what was wrong" 3-part claim, "what the fix changed," "how to verify," tracking footer) and fact-checked every claim against the remediation register (REM-09), remediation log, verdict, and the c07033ce diff. All substantive facts (branch name, commit SHA, CI run URL, 89→93 count, compound-trigger wording, git-diff paths) check out accurate — no Critical (invalidating) findings. Two Major gaps affect actionability/self-containedness: the verify command under-covers the actual fix scope, and unexplained internal routing jargon leaks into an audience-facing explanation. Recommendation: ACCEPT with two targeted line edits (REVISE-lite).

## Findings Table

| ID | Element | Failure Mode | S | O | D | RPN | Severity | Corrective Action |
|----|---------|-------------|---|---|---|-----|----------|-------------------|
| S-012-01 | How to verify | Insufficient — `git diff` command names only 2 of the 3 files the commit changed for REM-09; omits the phase-6 collision-analysis artifact that was annotated CORRECTED/SUPERSEDED | 6 | 6 | 5 | 180 | Major | Add the phase-6 path to the diff command or note it separately |
| S-012-02 | What was wrong (2) / What the fix changed | Ambiguous — "compound trigger," "priority," "routing algorithm" used with no inline gloss; audience has zero governance context | 5 | 6 | 6 | 180 | Major | Add a 6-8 word parenthetical gloss on first use |
| S-012-03 | Tracking footer / severity framing | Insufficient — issue never states this cluster was tracked as **Critical** severity in the register (only "mechanical fixes"), slightly undersells why the gap mattered | 4 | 5 | 5 | 100 | Major | Add one clause: "(tracked as a Critical-severity defect — the skill had zero enforcement coverage)" |
| S-012-04 | What this is (title) | Missing — title prefix "PROJ-032/BUG-009" is an opaque internal code with no legend for an external reader | 3 | 10 | 2 | 60 | Minor | Drop the prefix or append "(internal tracking ref)" |
| S-012-05 | What this is (closing sentence) | Insufficient — "Nothing for you to do unless you disagree with the fix" gives no channel for disagreeing (comment here? on the PR?) | 3 | 6 | 4 | 72 | Minor | Add "(reply on this issue or PR #269)" |

## Finding Details (Major)

### S-012-01: Verify command under-covers the fix

**Element:** "How to verify" paragraph.
**Failure Mode:** The commit `c07033ce` also touched `«PR projects tree»/PROJ-0039-nuclear-engineer/orchestration/nuclear-sop-build-20260325-001/eng/phase-6/eng-reviewer-001/registration-trigger-map-row.md` — adding a "CORRECTED / SUPERSEDED" note retracting the phase-6 claim that a compound trigger already existed (per remediation-register.md REM-09 fix spec item 3: "Annotate the phase-6 collision-analysis artifact as corrected/superseded"). The issue's verify command (`git diff c07033ce^ c07033ce -- .context/rules/mandatory-skill-usage.md AGENTS.md`) does not surface this.
**Effect:** An agent or reviewer who runs exactly the given command and concludes "verified" will not see that the original false collision-analysis claim was corrected — a secondary but real part of what REM-09 fixed.
**S/O/D Rationale:** S=6 (verification claim is incomplete, not wrong); O=6 (true as written, 100% of readers following literally miss it); D=5 (not discoverable without independently diffing the full commit).
**Corrective Action:** Extend the command to include the phase-6 path, or add one sentence: "The phase-6 collision-analysis artifact was also annotated as corrected/superseded — see the same commit."
**Acceptance Criteria:** Verify text lists all files materially relevant to the claim, or explicitly scopes to "the two enforcement-surface files" with a note that a third file was annotated separately.
**Post-Correction RPN estimate:** ~40.

### S-012-02: Unexplained routing jargon

**Element:** "What was wrong" item (2) and "What the fix changed."
**Failure Mode:** "no compound trigger existed to override it," "phrase matches beat numeric priority in the routing algorithm" — these terms come from `agent-routing-standards.md` (Routing Algorithm Step 2/3) and are not defined anywhere in the issue. The mission requires zero-governance-context comprehension.
**Effect:** The technical claim is verifiable only by a reader who already knows what "compound trigger" and "priority" mean in this repo's routing system; an external agent may correctly extract the outcome ("routes to /nuclear-sop now") but cannot independently verify the *mechanism* claim without extra lookup.
**S/O/D Rationale:** S=5 (doesn't block the top-line understanding, does block mechanism verification); O=6 (present in two places); D=6 (a reader with no repo governance context won't flag it as jargon — it reads as plausible prose).
**Corrective Action:** e.g., "no combined-phrase rule (a 'compound trigger') existed to override [X]'s numeric routing priority."
**Acceptance Criteria:** Every internal term load-bearing to the technical claim gets an inline 5-10 word gloss.
**Post-Correction RPN estimate:** ~60.

### S-012-03: Severity understated in framing

**Element:** Overall framing across "what this is" and tracking footer.
**Failure Mode:** remediation-register.md lists REM-09 as Cluster severity **Critical** (Cluster Index table), but the issue only ever calls this a "mechanical fix" / "registration-bookkeeping gap." True and not deceptive (the *fix* was mechanical), but the *defect* being fixed was rated Critical because the skill's mandatory-invocation enforcement had zero coverage — that context is absent.
**S/O/D Rationale:** S=4 (framing bias, not a factual error); O=5; D=5 (only detectable by cross-referencing the register).
**Corrective Action:** One clause noting the original severity and why (zero enforcement coverage), so the reader understands "easy to fix" is not the same as "low-impact."
**Acceptance Criteria:** Severity stated matches the register's Critical rating for the underlying defect, distinct from the (accurate) "mechanical to fix" characterization.
**Post-Correction RPN estimate:** ~40.

## Recommendations (priority order)

1. **S-012-01 (Major):** Extend or annotate the verify command to cover the phase-6 artifact correction.
2. **S-012-02 (Major):** Gloss "compound trigger" / "priority" / "routing algorithm" inline on first use.
3. **S-012-03 (Major):** Add one clause restoring the Critical severity context for the underlying defect.
4. **S-012-04 (Minor):** Drop or explain the "PROJ-032/BUG-009" title prefix.
5. **S-012-05 (Minor):** State where/how to register disagreement with the fix.

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | S-012-01: verify instructions omit a materially changed file |
| Internal Consistency | 0.20 | Neutral | No contradictions found between issue text and ground truth |
| Methodological Rigor | 0.20 | Neutral | Fix description accurately traces cause→fix→verification chain |
| Evidence Quality | 0.15 | Positive | Every checkable fact (SHA, branch, CI run, 89→93, diff paths) matches ground truth exactly |
| Actionability | 0.15 | Negative | S-012-02, S-012-05: jargon and missing disagreement channel add friction for a zero-context agent |
| Traceability | 0.10 | Negative | S-012-03: severity classification from the register is not carried into the issue |

---
*S-012 FMEA execution — adv-executor — blind to other strategies/reviews for issue-358*
