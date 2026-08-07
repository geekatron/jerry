# Pre-Mortem Report: GitHub Issue #350 (BUG-001 / REM-01, PR #269)

**Strategy:** S-004 Pre-Mortem Analysis
**Deliverable:** `snapshots/final/issue-350.md` (live text of geekatron/jerry issue #350)
**Criticality:** C4 (tournament)
**H-16 Compliance:** N/A for this compact executor invocation — issue text is a short communication artifact, not a design deliverable; treated as directly reviewable per task scope.
**Failure Scenario:** It is 2027-02-07. The PR #269 author read issue #350, spent an afternoon redesigning the QG-HOLD delegation topology, fixed it, closed the issue, and pinged the maintainer expecting the PR to merge — then discovered six more open blockers (#351–#356) plus an owner-level ruling plus a required independent re-review, none of which the issue text hinted at. Separately, their coding agent tried to `cat` the "Worktracker" path against the PR branch, got a 404, and flagged the issue as having a broken/fabricated reference.

## Summary

3 Minor and 2 Major failure causes identified. The core technical claim (QG-HOLD invokes an agent the same file says it cannot invoke; no return-to-orchestrator step; ~7 hops vs. the 3-hop ceiling) is **verified accurate** against `skills/nuclear-sop/agents/sop-executor.md` in the PR worktree — no critical/fact-invalidating risk found. Remaining risks are reference resolvability and expectation-setting. **Recommendation: ACCEPT with two Major mitigations.**

## Findings Table

| ID | Failure Cause | Category | Likelihood | Severity | Priority |
|----|---------------|----------|------------|----------|----------|
| S-004-01 | "Worktracker:" path has no branch qualifier; "Full analysis" path does | Technical | High | Major | P1 |
| S-004-02 | "Blocks merge of PR #269" implies closing this issue is sufficient; 6 sibling blockers + owner ruling + re-review are not mentioned | Process | Medium | Major | P1 |
| S-004-03 | Quoted fragment `"cannot invoke any other agent"` is not a verbatim substring of the source line | Evidence | Low | Minor | P2 |
| S-004-04 | No pointer to the adjacent IV-HOLD pattern in the same file, which already implements the correct return-to-orchestrator behavior the fix needs | Assumption | Medium | Minor | P2 |
| S-004-05 | Assignees line has no separator between two usernames and a trailing space | External | Low | Minor | P2 |

## Finding Details

### S-004-01: Worktracker path missing branch qualifier [MAJOR]

**Failure Cause:** The line reads: `Worktracker: projects/PROJ-032-nuclear-sop-review/work/BUG-001-qg-hold-delegation-topology (register section REM-01). Full analysis with candidate designs: remediation-register.md in .../STORY-004-remediation/ on branch feat/proj-032-nuclear-sop-review.` The second path states its branch explicitly; the first (Worktracker) path does not. Verified against the PR worktree (`proj-0039-nuclear-engineer` head): `projects/PROJ-032-nuclear-sop-review/` exists there but contains only `.jerry/data/events/*.jsonl` state files — no `work/BUG-001-...` directory. The Worktracker path is unresolvable on the PR branch and on `main`; it only exists on `feat/proj-032-nuclear-sop-review`.
**Likelihood:** High — any reader or agent that tries to open the Worktracker path without first noticing the branch name buried in the *next* sentence will 404.
**Severity:** Major — forces a lookup/guess; does not misstate the defect itself.
**Evidence:** `issue-350.md` line 12; confirmed absence via `Glob` of `projects/PROJ-032-nuclear-sop-review/**` in the PR worktree.
**Mitigation:** State the branch once, covering both paths: `Worktracker and full analysis (branch feat/proj-032-nuclear-sop-review): projects/.../BUG-001-... (register section REM-01); remediation-register.md in .../STORY-004-remediation/.`
**Acceptance Criteria:** Every file/directory path in the Tracking line carries an explicit branch qualifier or one shared qualifier unambiguously covers all of them.

### S-004-02: "Blocks merge" framing omits the other 6 concurrent blockers [MAJOR]

**Failure Cause:** The closing sentence "Blocks merge of PR #269" is true but incomplete: per the verdict, merge requires all seven BUG-001..007 blockers closed, an owner-issued H-36 ruling, and a fresh independent re-review scoring ≥0.92 — this issue is one of seven parallel, independent blockers, not a single gate.
**Likelihood:** Medium — a contributor working issues one at a time is likely to expect merge-readiness after closing the ones they see linked from their own PR thread.
**Severity:** Major — sets up a false completion expectation; wastes a status-check round-trip when discovered.
**Evidence:** `pr269-verdict.md` "Conditions for Merge After Rework" (5 conditions, of which this issue satisfies at most 1a of 7) and "The Rework Contract: Seven Open Blockers" table (issues #350–#356).
**Mitigation:** Change to: "Blocks merge of PR #269 together with 6 sibling issues (#351–#356); see PR #269 for the full merge-condition list."
**Acceptance Criteria:** The tracking line names or references the sibling issue range so the reader knows this is 1-of-N, not the final gate.

### S-004-03: Non-verbatim quotation [MINOR]

**Failure Cause:** Source line (`sop-executor.md`): "It cannot spawn subagents, delegate to sop-verifier, or invoke any other agent." The issue quotes `"cannot invoke any other agent"` — the words are present but not contiguous in that order as a standalone clause.
**Mitigation:** Either quote the full clause or state it unquoted: "...also states the agent has no Task tool and cannot invoke other agents."

### S-004-04: Missing pointer to the working analog pattern [MINOR]

**Failure Cause:** The same file's IV-HOLD block already does "return to the main context orchestrator" correctly (contrast case cited in the register). The issue asks the design question but doesn't note that a correct template already exists two sections away in the same file — the single highest-leverage actionability hint available without opening the linked register.
**Mitigation:** Append one clause: "(the adjacent verification hold in the same file already returns control to the orchestrator this way, and can serve as the model for a fix)."

### S-004-05: Assignee list formatting [MINOR]

**Failure Cause:** "Assignees: victorlau1 malcolm-x-evo " — no separator, trailing space. Cosmetic only; does not affect comprehension.
**Mitigation:** "Assignees: victorlau1, malcolm-x-evo"

## Recommendations

- **P1:** S-004-01 — add branch qualifier to the Worktracker path (or one shared qualifier for both paths).
- **P1:** S-004-02 — name the sibling issue range so this reads as 1-of-7, not the final merge gate.
- **P2:** S-004-03, S-004-04, S-004-05 — polish; apply opportunistically.

## Scoring Impact

| Dimension | Impact | Rationale |
|-----------|--------|-----------|
| Completeness | Negative | S-004-02: merge-condition scope not stated |
| Internal Consistency | Negative | S-004-01: branch qualifier applied to one path, not the sibling path in the same sentence |
| Methodological Rigor | Neutral | Core technical claim independently verified against source file |
| Evidence Quality | Negative | S-004-03: quotation marks over a non-contiguous paraphrase |
| Actionability | Negative | S-004-04: no pointer to the in-file working analog |
| Traceability | Neutral | Worktracker/register/GitHub triad is otherwise well-linked once branch is known |

**Result:** 0 Critical, 2 Major, 3 Minor. The defect description itself is factually sound and verified; failure modes are entirely in reference resolvability and completion-expectation framing.
