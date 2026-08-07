# Chain-of-Verification Report: GitHub issue #363 (BUG-014 navigation tables)

**Strategy:** S-011 Chain-of-Verification
**Deliverable:** `.../STORY-006-issue-quality/snapshots/final/issue-363.md`
**Criticality:** C4 (tournament)
**Date:** 2026-08-07
**H-16 Compliance:** Not confirmed applied prior (blind to other strategy outputs); proceeding per indirect H-16 for CoVe.
**Claims Extracted:** 9 | **Verified:** 7 | **Discrepancies:** 1 Major (+1 Minor self-containedness gap, not a factual discrepancy)

## Summary

Nearly every checkable fact in this ~300-word issue is accurate against ground truth: commit hash, branch name, CI run link, "15/15 green," "one of seven mechanical fixes," the 3+3 file split, line counts (76, 559), the 23/25 and 3/5 template-format ratios, and the worktracker/register path all verify exactly. One claim is a mischaracterization of runtime behavior (CV-001, Major) that could give the reader a wrong mental model of the file's role. Recommendation: **REVISE** — one small text correction, otherwise ACCEPT.

## Findings Table

| ID | Claim | Source | Discrepancy | Severity | Affected Dimension |
|----|-------|--------|-------------|----------|--------------------|
| S-011-01 | "`WORKFLOW_DEFINITION.template.md` ... read by the brief agent on every run" | `agents/sop-brief.md` line 141 (STEP 0, marked **Optional**) | Template is loaded only in Step 0, which fires only when no workflow definition exists and natural-language generation is used — not on every sop-brief invocation | Major | Evidence Quality |
| S-011-02 | "Tracking: worktracker `projects/.../BUG-014-navigation-tables`" | N/A (internal jargon) | "worktracker" is unexplained internal terminology; violates the zero-governance-knowledge mission constraint (self-containedness), though it sits in a metadata footer, not the actionable body | Minor | Traceability |

## Finding Details

### S-011-01: "read by the brief agent on every run" overstates the template's runtime frequency [MAJOR]

**Claim (from deliverable):** "`skills/nuclear-sop/templates/WORKFLOW_DEFINITION.template.md` (250 lines, read by the brief agent on every run)"

**Source Document:** `skills/nuclear-sop/agents/sop-brief.md`, `### STEP 0 (Optional): Workflow Definition Generation from Natural Language` (line 141: `a. Load skills/nuclear-sop/templates/WORKFLOW_DEFINITION.template.md`). Grep of the full skill tree confirms this is the *only* runtime load site; all other references (`SKILL.md`, `PLAYBOOK.md`, `docs/howto-guides.md`) are documentation pointers or a manual `cp` example, not agent-executed reads.

**Independent Verification:** Step 0 is explicitly labeled Optional and is invoked only when Step 1 finds no workflow definition and the user selects natural-language generation (Option A). On the common path — caller supplies an existing workflow definition file — this template is never loaded.

**Discrepancy:** "read... on every run" claims unconditional, every-execution consumption; the actual behavior is conditional, optional-path consumption.

**Severity:** Major — an external contributor/agent reading this issue would form an incorrect model of how central this template is to the skill's hot path, which could misdirect effort if they go looking for why "every run" doesn't match what they observe in the code.

**Dimension:** Evidence Quality

**Correction:** Replace "(250 lines, read by the brief agent on every run)" with "(250 lines, loaded by the brief agent only in the optional Step 0 path — generating a workflow definition from a natural-language description when none is supplied)."

### S-011-02: unexplained "worktracker" term [MINOR]

**Claim:** "**Tracking:** worktracker `projects/PROJ-032-nuclear-sop-review/work/BUG-014-navigation-tables` ..."

**Discrepancy:** No gloss is given for "worktracker," an internal Jerry-framework term. Path and register-section-REM-14 references themselves resolve correctly and were verified accurate against `remediation-register.md` and `remediation-log.md`.

**Severity:** Minor — confined to the closing metadata line, does not block understanding the fix or the "nothing to do" instruction above it.

**Correction:** e.g. "**Tracking (this repo's internal work-item record, informational only):** ..."

## Claims Verified Clean (no discrepancy)

| Claim | Source | Result |
|---|---|---|
| Commit `c07033ce` on branch `proj-0039-nuclear-engineer` | evidence-c07033ce.md header | VERIFIED |
| "one of seven mechanical fixes" | remediation-log.md FIX-NOW Trace (REM-08..14, 7 rows, all commit `c07033ce`) | VERIFIED |
| 3 files with no nav table + 3 files with missing rows | remediation-register.md REM-14 G1/G2 | VERIFIED |
| `HOLD_POINT_LOG.template.md` 76 lines; `c3-adr-workflow-definition.md` 559 lines | REM-14 G1 (exact figures) | VERIFIED |
| "23 of the repo's 25 canonical templates ... 3 of the skill's own 5 templates" | REM-14 Rationale (verbatim ratio) | VERIFIED |
| CI "15/15 green," run 31174766440 | remediation-log.md Outcome + evidence-c07033ce.md header (both cite same run) | VERIFIED |
| Worktracker path `.../work/BUG-014-navigation-tables` + register section REM-14 | remediation-log.md FIX-NOW Trace relative link resolves to this path | VERIFIED |
| Branch `feat/proj-032-nuclear-sop-review` for the register location | matches current repo branch | VERIFIED |

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | No missing information; every fact needed to act is present |
| Internal Consistency | 0.20 | Neutral | No internal contradictions found |
| Methodological Rigor | 0.20 | Neutral | N/A to this artifact type |
| Evidence Quality | 0.15 | Negative | S-011-01: one mischaracterized runtime-frequency claim |
| Actionability | 0.15 | Positive | "Nothing to do" framing and verify command are precise and executable |
| Traceability | 0.10 | Negative (minor) | S-011-02: unexplained internal term in tracking footer |

## Recommendations

- **Major (SHOULD correct):** S-011-01 — reword the WORKFLOW_DEFINITION.template.md parenthetical to describe Step 0's optional, conditional load instead of "every run."
- **Minor (MAY correct):** S-011-02 — add a one-clause gloss for "worktracker" in the Tracking line.
