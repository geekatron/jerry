# S-010 Self-Refine — Execution Report: GitHub Issue #363

| Field | Value |
|-------|-------|
| Strategy | S-010 Self-Refine |
| Deliverable | GitHub issue #363 (PROJ-032/BUG-014: nuclear-sop nav tables) — `snapshots/final/issue-363.md` |
| Criticality | C4 (tournament) |
| Iteration | 1 of 1 |

## Summary

The issue's core factual claims (commit SHA, branch, 3+3 file split, exact pre-fix line counts of 250/76/559, the 23-of-25 and 3-of-5 template-conformance figures, CI run link, tracking paths) all verify exactly against the evidence pack and worktree. The deliverable is accurate on its central claims and requires no reader action, which is honestly and clearly stated. Two Major gaps remain: one factual overstatement about *when* a file is read, and a "How to verify" command whose scope silently pulls in unrelated fixes. Ready for external review after two small edits; not blocked from tournament proceeding.

## Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| S-010-01 | "read by the brief agent on every run" is false | Major | `agents/sop-brief.md:141` loads this template only inside optional Step 0 (natural-language generation) | Evidence Quality |
| S-010-02 | Verify command's file/dir scope mixes in unrelated fixes | Major | `templates/` also contains `PROCEDURE_STATE.template.yaml` and `POST_JOB_BRIEF.template.md`, both changed in the same commit for REM-11/REM-12 (extension + state-machine fixes), not nav tables; SKILL.md/PLAYBOOK.md/reference.md diffs likewise carry large REM-08/REM-12 content | Actionability |
| S-010-03 | No clickable commit/diff link provided | Minor | Only a local `git diff` command is given; a GitHub compare/commit URL (e.g. `https://github.com/geekatron/jerry/commit/c07033ce`) would let a reader or agent verify without a local checkout | Actionability |
| S-010-04 | "What was wrong" paragraph is dense | Minor | Single ~110-word sentence enumerates 6 files with parenthetical line counts and roles | Traceability (readability) |

## Finding Details

### S-010-01: False "every run" claim about WORKFLOW_DEFINITION.template.md

- **Severity:** Major
- **Affected Dimension:** Evidence Quality
- **Evidence:** Issue text: "`skills/nuclear-sop/templates/WORKFLOW_DEFINITION.template.md` (250 lines, read by the brief agent on every run)". Ground truth `agents/sop-brief.md` line 141 shows this template is loaded only under "STEP 0 (Optional): Workflow Definition Generation from Natural Language" — i.e., only when no workflow definition exists yet and the user opts into natural-language generation. No other unconditional load site exists in `agents/sop-brief.md` or `composition/sop-brief.prompt.md` (both reference the same optional Step 0).
- **Impact:** Overstates the file's runtime criticality; a careful reader (or their AI agent) checking the claim against the agent file will find a discrepancy that undermines confidence in the rest of the issue's technical claims, even though the underlying point (this file needed a nav table) is unaffected.
- **Recommendation:** Replace with an accurate qualifier, e.g., "(250 lines, loaded by the brief agent when generating a workflow definition from natural language, Step 0)."

### S-010-02: "How to verify" command scope includes unrelated fixes

- **Severity:** Major
- **Affected Dimension:** Actionability
- **Evidence:** Suggested command: `git diff c07033ce^ c07033ce -- skills/nuclear-sop/templates/ skills/nuclear-sop/examples/ skills/nuclear-sop/SKILL.md skills/nuclear-sop/PLAYBOOK.md skills/nuclear-sop/docs/reference.md`. The same commit `c07033ce` also modifies, in these same paths: `templates/PROCEDURE_STATE.template.yaml` (state-machine/transition fixes, REM-12) and `templates/POST_JOB_BRIEF.template.md` (`.md`→`.yaml` extension fix, REM-11); `SKILL.md` (registration-status and C3+-withdrawal rewrite, REM-08); `PLAYBOOK.md` (registration/derived-artifact and C3+ text, REM-08/REM-13). None of this is nav-table content.
- **Impact:** A contributor or their agent running the literal command will see a much larger diff than "nav tables added/rows fixed" and may misattribute unrelated REM-08/11/12 changes to this issue, or conversely dismiss real nav-table changes as noise.
- **Recommendation:** Either scope the diff to just the added `## Document Sections` hunks (e.g., `git diff c07033ce^ c07033ce -- skills/nuclear-sop/templates/WORKFLOW_DEFINITION.template.md skills/nuclear-sop/templates/HOLD_POINT_LOG.template.md skills/nuclear-sop/examples/c3-adr-workflow-definition.md` plus `grep -A4 "## Document Sections"` on SKILL.md/PLAYBOOK.md/reference.md), or add one sentence noting the shared files also carry unrelated fixes tracked in sibling issues #357–#362.

## Recommendations

1. **Fix S-010-01** — correct the WORKFLOW_DEFINITION.template.md read-frequency claim. (Critical to Evidence Quality; resolves S-010-01)
2. **Fix S-010-02** — scope or annotate the verify command. (resolves S-010-02)
3. Add a plain commit/diff URL alongside the CI run link. (resolves S-010-03)
4. Optionally split the "What was wrong" sentence into a short lead-in plus a list of the 6 files. (resolves S-010-04)

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | All required facts present (commit, branch, files, CI, tracking) |
| Internal Consistency | 0.20 | Neutral | No contradictions within the text itself |
| Methodological Rigor | 0.20 | Neutral | N/A to a communication artifact |
| Evidence Quality | 0.15 | Negative | S-010-01: one claim contradicted by the cited agent file |
| Actionability | 0.15 | Negative | S-010-02/03: verify path is noisy and link-free |
| Traceability | 0.10 | Negative | S-010-04: minor scannability gap |

## Decision

**Outcome:** Needs targeted revision (not a blocker to proceed with tournament; no unresolved Critical findings).

**Rationale:** Two Major findings are narrow, single-sentence fixes; all headline facts (SHA, line counts, template-conformance ratios, CI link, tracking paths) verified correct against ground truth.

**Next Action:** Apply S-010-01/02 fixes to `issue-363.md`; proceed to remaining tournament strategies (self-refine does not gate other strategies per H-16 N/A).
