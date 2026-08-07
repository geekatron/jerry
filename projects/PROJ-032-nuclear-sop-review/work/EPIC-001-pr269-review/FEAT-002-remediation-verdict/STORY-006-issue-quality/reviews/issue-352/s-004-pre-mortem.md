# Pre-Mortem Report: GitHub Issue #352 (BUG-003 / REM-03)

**Strategy:** S-004 Pre-Mortem Analysis (adapted for a ~300-word communication artifact)
**Deliverable:** `projects/PROJ-032-nuclear-sop-review/work/EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-006-issue-quality/snapshots/final/issue-352.md`
**Criticality:** C4
**Date:** 2026-08-07
**Failure scenario declared:** It is six months from now. The PR #269 contributor read issue #352, addressed exactly what it explicitly asked, closed it as resolved — and the review team later discovered the underlying defect was only partially closed, and one of the two supporting links in the issue 404'd on first click, costing the contributor (and their AI agent) a wasted round-trip before they found the right branch.

## Summary

Issue #352's factual content checks out against ground truth: the verifier authority-inversion claim (criteria/paths/criticality all sourced from the untrusted workflow definition), the "no SHA-256 tamper mechanism implemented anywhere" claim, and the "resumes past every pause point" claim are all still true at the post-remediation commit `c07033ce` (confirmed by diff: no `state_hash` computation added anywhere, and the RESUME-trust-on-`status`-field logic in `sop-executor.md` is untouched by the fix). No Critical (factually-wrong) findings. Three Major actionability/completeness gaps and one Minor terminology risk. **Recommendation: ACCEPT with targeted revision** — the text is honest and correctly scoped; it needs one added sentence and one path fix.

## Findings

| ID | Finding | Category | Severity |
|----|---------|----------|----------|
| S-004-01 | Design question omits explicit ask to close the RESUME-past-holds gap | Completeness/Actionability | Major |
| S-004-02 | Worktracker path is missing both filename and branch qualifier | Traceability | Major |
| S-004-03 | No affected-file pointer forces a lookup before any redesign work can start | Actionability | Major |
| S-004-04 | "declared risk level" vs. "severity critical" terminology overlap | Clarity | Minor |

### S-004-01: Design question drops the RESUME-past-holds sub-question [MAJOR]

**Evidence:** Body states as background fact: "a hand-edited state file resumes cleanly past every pause point" — but "The design question to answer" only asks about (1) criteria/paths/criticality provenance and (2) whether tamper evidence will be implemented. It never poses the RESUME-past-holds problem as something the contributor must also answer.
**Why this fails:** A contributor who answers exactly the two posed questions (e.g., pins criteria to a signed brief, implements a real hash) can plausibly close this issue while a poisoned `IN-PROGRESS` state file still steers execution past every hold type, because closing that gap was never asked for.
**Fix:** Append to the design question: "...and how is a hand-edited or poisoned state file prevented from resuming past a pause point *before* execution continues, not just detected after the fact?"

### S-004-02: Worktracker path lacks filename and branch [MAJOR]

**Evidence:** "Worktracker: `projects/PROJ-032-nuclear-sop-review/work/BUG-003-trust-boundary-state-tamper`" — a directory, not a file, and unlike the adjacent `remediation-register.md` reference in the same sentence group, it carries no `on branch ...` qualifier. Verified: this path exists only under `work/BUG-003-trust-boundary-state-tamper/BUG-003-trust-boundary-state-tamper.md` on branch `feat/proj-032-nuclear-sop-review`; it is not expected to be present on the repo's default branch.
**Why this fails:** An external agent resolving this path via the GitHub API/UI without an explicit ref defaults to the base branch and gets a 404, or must first discover which branch holds it — exactly the "resolvable references" failure mode this review is scored against.
**Fix:** `Worktracker: projects/PROJ-032-nuclear-sop-review/work/BUG-003-trust-boundary-state-tamper/BUG-003-trust-boundary-state-tamper.md (on branch feat/proj-032-nuclear-sop-review; register section REM-03).`

### S-004-03: No inline pointer to the affected source files [MAJOR]

**Evidence:** Ground truth (remediation-register.md REM-03) names six concrete files the redesign touches (`agents/sop-verifier.md`, `agents/sop-brief.md`, `agents/sop-executor.md`, `templates/PROCEDURE_STATE.template.yaml`, `docs/reference.md`, `rules/nuclear-sop-behavior-rules.md`). None appear in the issue body.
**Why this fails:** A contributor cannot start scoping the redesign from the issue text alone — they must first open the linked register (itself requiring the branch-qualified path from S-004-02) purely to learn where the affected code lives. This is a forced lookup the issue could eliminate in one clause.
**Fix:** Add one clause to the "Tracking" line: "Affected: `skills/nuclear-sop/agents/sop-verifier.md`, `sop-brief.md`, `sop-executor.md`, `templates/PROCEDURE_STATE.template.yaml`."

### S-004-04: "risk level" vs. issue "severity" terminology overlap [MINOR]

**Evidence:** Body uses "the workflow's declared risk level" (= the workflow's self-declared C1–C4 criticality) while the Tracking line separately uses "severity critical" (= this issue's own priority). Both use risk/severity vocabulary for two unrelated axes.
**Fix:** Reword the body to "the workflow's declared criticality level" to keep it visually distinct from the issue's own "severity critical" tag.

## Scoring Impact (S-014 dimensions, qualitative)

| Dimension | Impact | Rationale |
|-----------|--------|-----------|
| Completeness | Negative | S-004-01: one sub-defect (RESUME-past-holds) isn't posed as a question to answer |
| Actionability | Negative | S-004-02, S-004-03: two forced lookups before work can begin |
| Traceability | Negative | S-004-02: one of two references is branch-ambiguous |
| Evidence Quality | Positive | Core factual claims verified true against `c07033ce` diff and register |
| Internal Consistency | Neutral | No contradictions found within the issue text itself |

## H-15 Self-Review

All four findings were checked against the live diff (`evidence-c07033ce.md`) and `remediation-register.md` REM-03 before being recorded; no finding asserts a fact not traceable to a cited source. No H-16 gate applies to S-004 execution order in this single-strategy invocation context.
