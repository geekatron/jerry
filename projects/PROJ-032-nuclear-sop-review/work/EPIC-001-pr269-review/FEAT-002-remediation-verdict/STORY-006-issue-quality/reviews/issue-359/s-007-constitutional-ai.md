# Constitutional Compliance Report: GitHub issue #359 (BUG-010 / REM-10)

**Strategy:** S-007 Constitutional AI Critique (adapted for a communication artifact)
**Deliverable:** `snapshots/final/issue-359.md`
**Criticality:** C4 (tournament)
**Date:** 2026-08-07
**Reviewer:** adv-executor (S-007)
**Constitutional lens applied:** P-001 (truth/accuracy), P-022 (no deception), self-containedness, actionability, honest severity framing — evaluated against remediation-register.md REM-10, evidence-c07033ce.md, remediation-log.md, BUG-010 entity.

## Summary

PARTIAL compliance: 1 Major (factual overstatement of the output-location defect), 2 Minor (unexplained cross-reference code; dense unstructured "what was wrong" paragraph). All checkable facts (commit SHA, branch, CI run link, error counts, schema path, git-diff syntax, worktracker path, "8/8 valid" claim) verified TRUE against ground truth. No Critical findings. Score: 0.93 (PASS). Recommend one targeted wording fix; no blocking issues.

## Findings Table

| ID | Principle | Tier | Severity | Evidence | Affected Dimension |
|----|-----------|------|----------|----------|--------------------|
| S-007-01 | P-001 factual accuracy | MEDIUM | Major | "none of the four agents declared where its output files go" | Internal Consistency |
| S-007-02 | Self-containedness (no unexplained internal codes) | SOFT | Minor | "register section REM-10" in Tracking footer | Completeness |
| S-007-03 | Actionability / resolvable verification | SOFT | Minor | `git diff` scoped to `agents/` + `composition/` also surfaces REM-11/12/13 hunks bundled in the same commit | Actionability |
| S-007-04 | Concision / scannability | SOFT | Minor | "What was wrong" packs 5 distinct defects into one run-on paragraph | Completeness |

## Finding Details

### S-007-01: Output-location defect overstated [MAJOR]

**Location:** Line 7, "none of the four agents declared where its output files go"
**Ground truth (REM-10 G6):** "sop-executor's `{execution_dir}` is never defined; **sop-capture's location is non-resolvable prose**; sop-verifier has none at all." The pre-fix diff confirms sop-brief and sop-capture *did* carry an `output.location` string (`"brief/pre-job-brief.md"`, `"capture/oe-entry-{entry_id}.yaml and docs/experience/{entry_id}.yaml"`) — the defect is that these were not anchored under `projects/${JERRY_PROJECT}/` (AD-M-011), not that the field was absent. Only sop-verifier truly had none.
**Impact:** Misstates the nature of the fixed defect. Not actionable-consequential (issue says "nothing for you to do"), but a reader/agent auditing the fix against the stated defect will find the "what was wrong" description doesn't match the diff.
**Remediation:** Replace with: "none of the four agents declared a *project-anchored* output location (the repo standard requires paths under the active project directory) — one agent had none at all, the others used non-conformant or undefined paths."

### S-007-02: Unexplained internal cross-reference [MINOR]

**Location:** Tracking footer, "register section REM-10 in `remediation-register.md`"
**Impact:** "REM-10" is an internal cluster code with no gloss; harmless since it's a footer pointer, not required for understanding the fix, but breaks the otherwise clean avoidance of internal jargon used everywhere else in the body.
**Remediation:** "(remediation register, item 10)" or drop the code and keep only the resolvable path.

### S-007-03: Verification diff scope broader than the defect [MINOR]

**Location:** "How to verify," `git diff c07033ce^ c07033ce -- skills/nuclear-sop/agents/ skills/nuclear-sop/composition/`
**Ground truth:** commit `c07033ce` bundles fixes for REM-08 through REM-14 (7 clusters); REM-11, REM-12, and REM-13 also touch files under `agents/` and `composition/` (confirmed in evidence-c07033ce.md diff stat and remediation-register.md affected-files lists). The command is correct and will run, but will show hunks unrelated to this issue's schema/YAML/output-location defect (e.g., OE `.yaml` extension fixes, state-machine transition fixes, composition-drift restoration) interleaved with the relevant ones.
**Remediation:** Either narrow the path list to the exact REM-10 files (`agents/sop-{brief,verifier,executor,capture}.governance.yaml agents/sop-{brief,verifier,executor}.md composition/sop-verifier.agent.yaml composition/sop-brief.agent.yaml`) or add one clause: "note this diff also includes fixes tracked by sibling issues #360-#362."

### S-007-04: Dense, unstructured defect list [MINOR]

**Location:** "What was wrong" paragraph
**Impact:** Five distinct, independently-fixable defects (unparseable YAML; 4-error schema failure; 2-error schema failure; section-number contradiction; missing output locations; tool-call language; missing reasoning-effort — actually seven) are run together in one long sentence chain. A skim-reading contributor deciding whether to object to any one fix has to parse the whole block to separate items.
**Remediation:** Convert to a short bullet list, one defect per line, keeping the same content.

## Remediation Plan

**P1 (Major):** S-007-01 — correct the output-location claim to match the actual pre-fix state (some agents had non-conformant locations; only one had none).
**P2 (Minor):** S-007-02 — gloss or drop "REM-10"; S-007-03 — narrow or caveat the verification diff scope; S-007-04 — bullet the "what was wrong" list.

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative (minor) | S-007-02, S-007-04 reduce scannability/self-containment slightly |
| Internal Consistency | 0.20 | Negative | S-007-01: stated defect doesn't match the diff it describes |
| Methodological Rigor | 0.20 | Neutral | No findings |
| Evidence Quality | 0.15 | Positive | All quantitative claims (error counts, CI 15/15, 8/8, SHA, branch) verified true |
| Actionability | 0.15 | Negative (minor) | S-007-03: verification command noisier than necessary |
| Traceability | 0.10 | Positive | Worktracker path, register section, and issue number all resolve correctly |

**Constitutional Compliance Score:** 1.00 − (1 × 0.05 + 3 × 0.02) = **0.93** → **PASS** (≥ 0.92 threshold)

**Threshold Determination:** PASS. One Major wording fix recommended before merge/close of the issue-quality tracking, but no Critical blocker.
