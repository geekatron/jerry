# FMEA Report: GitHub Issue #363 (PROJ-032/BUG-014 — nuclear-sop navigation tables)

**Strategy:** S-012 FMEA (adapted for a ~300-word communication artifact)
**Deliverable:** `.../STORY-006-issue-quality/snapshots/final/issue-363.md` (live text of GitHub issue #363)
**Criticality:** C4 (tournament)
**H-16 Compliance:** N/A for this compact single-strategy execution (blind tournament slot)
**Elements Analyzed:** 6 | **Failure Modes Identified:** 4 | **Total RPN:** 552

## Summary

The issue's core claims (defect, commit `c07033ce`, CI 15/15, tracking to BUG-014/REM-14, "23/25 templates" precedent) check out against the remediation register and the commit diff. The most consequential defect is a specific, checkable overstatement: `WORKFLOW_DEFINITION.template.md` is described as "read by the brief agent on every run," but it is loaded only inside sop-brief's *optional* Step 0 (natural-language workflow generation) — verified false against `agents/sop-brief.md`. A second finding shows the prescribed verify command mixes REM-14's nav-table diff with unrelated hunks from other remediation clusters in the same three files. Recommendation: **REVISE** (targeted correction, not a rewrite).

## Findings Table

| ID | Element | Failure Mode | S | O | D | RPN | Severity | Corrective Action | Affected Dimension |
|----|---------|-------------|---|---|---|-----|----------|-------------------|--------------------|
| S-012-01 | "What was wrong" para | Overstates operational criticality: `WORKFLOW_DEFINITION.template.md` is called "read by the brief agent on every run," but `agents/sop-brief.md` STEP 0 (the only step that loads it) is explicitly **Optional**. The category label "three long **runtime-consumed** files" is also inaccurate for `HOLD_POINT_LOG.template.md`, which no agent methodology step ever `Load`s (it appears only in reference/file-structure tables). | 6 | 6 | 5 | 180 | Major | Drop the parenthetical frequency claim; state instead: "loaded by sop-brief when generating a workflow definition from natural language (Step 0)." Replace "runtime-consumed" with "long files the skill ships as templates/examples" or verify + correct per-file. | Evidence Quality |
| S-012-02 | "How to verify" para | The prescribed command `git diff c07033ce^ c07033ce -- skills/nuclear-sop/templates/ skills/nuclear-sop/examples/ skills/nuclear-sop/SKILL.md skills/nuclear-sop/PLAYBOOK.md skills/nuclear-sop/docs/reference.md` is syntactically valid and the CI link resolves, but SKILL.md/PLAYBOOK.md/reference.md each carry substantial unrelated edits from REM-04/REM-08/REM-09/REM-12 in the same commit (C3+ status withdrawal, registration status, execution-directory section, etc.). A reader following the instruction to "verify this fix" will see a much larger diff than the nav-table change this issue describes, with no guidance on which hunks are in scope. | 5 | 7 | 4 | 140 | Major | Narrow the command to the templates/examples paths only (which *are* nav-table-exclusive), or add one sentence: "SKILL.md/PLAYBOOK.md/reference.md diffs include unrelated fixes from other issues in this batch — look for the added 'Document Sections' / nav rows only." | Actionability |
| S-012-03 | Title | Title packs two unexplained internal identifiers ("PROJ-032", "BUG-014") that are never defined anywhere in the issue body — the reader can act on the issue without them, but cannot independently resolve what they refer to (project code, bug-tracker ID) from the text alone. | 3 | 6 | 4 | 72 | Minor | Either drop the codes from the title (they add no actionable information) or append a one-clause gloss, e.g. "(internal tracking: PROJ-032/BUG-014 — no action needed on your end)." | Completeness |
| S-012-04 | "What was wrong" opening sentence | Paraphrases H-23 as "this repo requires every long markdown file that **agents consume at runtime**" — the actual rule (`.context/rules/markdown-navigation-standards.md` H-23) covers "all Claude-consumed markdown files over 30 lines," a broader and simpler bar than "runtime-consumed by agents." Not load-bearing for this reader (no action required either way), but it's an avoidable inaccuracy about the rule that justifies the fix. | 3 | 5 | 6 | 90 | Minor→Major boundary | Reword to "this repo requires every long markdown file to open with a navigation table" — drop the "agents consume at runtime" qualifier, which is not the actual trigger condition. | Internal Consistency |

**Finding ID Format:** `S-012-{NN}` per orchestrator instruction (execution scoped to issue-363/s-012-fmea.md).

## Finding Details

**S-012-01 (Major).** Effect: an AI agent or human triager reading "read on every run" could misjudge this template's blast radius (e.g., prioritize it as a hot-path file for testing) when it is in fact loaded only in an optional generation path. Verified via `Grep` on `agents/sop-brief.md` and `composition/sop-brief.prompt.md`: the only `Load` reference to `WORKFLOW_DEFINITION.template.md` is inside "STEP 0 (Optional): Workflow Definition Generation from Natural Language." Post-correction RPN estimate: ~40 (drop O and S once the claim is scoped correctly).

**S-012-02 (Major).** Effect: forces the verifier to do extra triage work the issue promised to save them ("How to verify" implies a clean, scoped diff). Confirmed against `evidence-c07033ce.md`: the SKILL.md hunk alone spans STAR Validation status rewrite, SEC-008 status, Registration Content, and a new Execution Directory section — none of which is a navigation table. Post-correction RPN estimate: ~50 (scoping sentence resolves the ambiguity without changing the command).

## Recommendations (priority order)

1. **S-012-01** — Correct or remove the "read ... on every run" claim; correct the "runtime-consumed" category label. (RPN 180)
2. **S-012-02** — Add one scoping sentence to "How to verify" so the reader knows the SKILL.md/PLAYBOOK.md/reference.md diffs are not nav-table-exclusive. (RPN 140)
3. **S-012-04** — Reword the H-23 paraphrase to match the actual rule trigger (file length, not "agent runtime consumption"). (RPN 90)
4. **S-012-03** — Drop or gloss the unexplained "PROJ-032"/"BUG-014" codes in the title. (RPN 72)

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | S-012-03: title codes left undefined |
| Internal Consistency | 0.20 | Negative | S-012-04: rule paraphrase doesn't match H-23's actual trigger condition |
| Methodological Rigor | 0.20 | Neutral | Fix specification traced correctly to REM-14/BUG-014/#363 |
| Evidence Quality | 0.15 | Negative | S-012-01: "every run" / "runtime-consumed" claims fail verification against `agents/sop-brief.md` |
| Actionability | 0.15 | Negative | S-012-02: verify command scope not isolated to the claimed defect |
| Traceability | 0.10 | Positive | Commit, CI run, worktracker path (`BUG-014-navigation-tables`), and register section (REM-14) all resolve correctly |

---
*Executed blind to other strategies' reviews of issue-363 per orchestrator instruction.*
