# Inversion Report: GitHub Issue #359 (REM-10 / BUG-010)

**Strategy:** S-013 Inversion Technique (adapted for a ~300-word communication artifact)
**Deliverable:** `issue-359.md` snapshot — text of `geekatron/jerry#359`
**Criticality:** C4 (tournament)
**H-16 note:** Executed within a tournament sequence where S-003 Steelman has run per orchestrator context.

## Summary

Goals: (1) an external contributor/agent with zero repo-governance knowledge can understand the defect and the fix from this text alone; (2) every factual claim and reference is verifiable and resolvable. Stress-testing the assumption "every claim in the text matches the ground-truth register/diff" found **two claims that invert against the evidence**: the pre-fix "none declared output location" framing overstates the actual (mixed) pre-fix state, and the post-fix "declared for all four agents" claim is directly falsified by `sop-verifier.governance.yaml`, which intentionally has no `output.location`. Recommendation: **REVISE** — two factual corrections and one verification gap, otherwise the text is accurate and well-scoped.

## Findings Table

| ID | Assumption Stress-Tested | Confidence | Severity | Evidence | Affected Dimension |
|----|---------------------------|------------|----------|----------|---------------------|
| S-013-01 | "none of the four agents declared where its output files go" is literally true pre-fix | Low | Major | Pre-fix `sop-brief.governance.yaml` diff shows `location: "brief/pre-job-brief.md"` already present; register text (REM-10 G6) says sop-brief/sop-capture/sop-executor had partial/malformed declarations, only sop-verifier "has none at all" | Evidence Quality |
| S-013-02 | "project-anchored output locations declared for all four agents" is true post-fix | Low | Critical | `sop-verifier.governance.yaml` (post-fix, verified in worktree): `output.required: false`, no `location` field at all, by design (T1 agent returns report as Task response) — directly contradicts "declared for all four" | Evidence Quality / Internal Consistency |
| S-013-03 | The "How to verify" instructions let a reader independently confirm the "8 of 8 files valid" claim | Medium | Major | Verify section only names re-validating governance files against `agent-governance-v1.schema.json` (4 files); the other 4 are `composition/*.agent.yaml`, which per their own header validate against `agent-canonical-v1.schema.json` — no verification method given for that half of the claim | Actionability |
| S-013-04 | "its review tier" is self-explanatory to a reader with no framework context | Medium | Minor | No definition given for "review tier" (= declared quality-gate tier under ET-M-001); low actionability impact since text states "nothing for you to do" | Completeness |
| S-013-05 | "capability language" vs "concrete tool calls" is self-explanatory without an example | Medium | Minor | Term pair given with no illustrative before/after; reader cannot infer the actual textual change | Completeness |

## Finding Details

### S-013-01: Pre-fix "none declared output files" overstates the defect [MAJOR]

**Original claim:** "none of the four agents declared where its output files go."
**Inversion:** Ground truth shows sop-brief already declared `location: "brief/pre-job-brief.md"`, sop-capture declared a (malformed) dual location string, and sop-executor referenced an (undefined) `{execution_dir}` — only sop-verifier had zero declaration. The real defect is "not project-anchored / malformed / undefined variable," not "absent."
**Consequence:** A contributor or agent spot-checking the pre-fix file for "no location field" would find one in 3 of 4 files and could conclude the issue text is wrong about the defect itself, undermining trust in the rest of the report.
**Mitigation:** Reword to: "none of the four agents anchored its output under the active project directory as the repo standard requires — three had non-anchored or malformed location declarations, one (sop-verifier) had none."

### S-013-02: Post-fix "declared for all four agents" is factually wrong [CRITICAL]

**Original claim:** "project-anchored output locations declared for all four agents."
**Inversion:** `sop-verifier.governance.yaml` at the current head has `output.required: false` and no `location` key whatsoever — by deliberate design, since sop-verifier is a T1 read-only agent that returns its report as Task response content rather than writing a file.
**Consequence:** This is the single most directly checkable claim in the issue (open one file, grep for `location:`) and it fails. An agent tasked with confirming "the fix is complete" against this text would flag a false discrepancy on sop-verifier, or conversely trust the issue and never notice sop-verifier's genuinely different (correct) output contract.
**Mitigation:** Reword to: "project-anchored output locations declared for sop-brief, sop-capture, and sop-executor; sop-verifier declares no file output by design (T1 agent, returns its report as response content, not a written artifact)."

### S-013-03: "8 of 8 files valid" claim is only half-verifiable from the text [MAJOR]

**Original claim (verify section):** re-validate governance files against `docs/schemas/agent-governance-v1.schema.json` — zero errors.
**Inversion:** The "8 of 8" figure spans 4 governance files (validated against `agent-governance-v1.schema.json`) plus 4 `composition/*.agent.yaml` files (which self-declare a different schema, `agent-canonical-v1.schema.json`, per their own file header). The verify instructions only cover the first 4.
**Consequence:** A contributor's agent following the instructions literally would validate 4 files, get "zero errors," and have no path to independently reproduce the "8 of 8" number — or might mistakenly point the governance schema at the composition files and get spurious errors.
**Mitigation:** Add: "...and confirm the four `composition/*.agent.yaml` files parse and validate against `docs/schemas/agent-canonical-v1.schema.json` (see each file's own header)."

### S-013-04 / S-013-05: Unglossed internal shorthand [MINOR]

"Review tier" and "capability language" are used without a one-clause gloss. Given the issue explicitly tells the reader there is nothing to do, this is low-actionability-impact, but it is the one remaining self-containedness gap in an otherwise plain-language issue.
**Mitigation:** "its review tier" -> "its declared review rigor level (C3)"; "capability language" -> "capability wording (e.g., 'read-only inspection' instead of naming Glob/Grep directly)."

## Recommendations

- **MUST fix (Critical):** S-013-02 — correct the false "all four agents" claim; this is directly falsifiable by opening one file.
- **SHOULD fix (Major):** S-013-01 (pre-fix framing), S-013-03 (complete the verify instructions for all 8 files claimed valid).
- **MAY fix (Minor):** S-013-04, S-013-05 — brief glosses for "review tier" and "capability language."

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Evidence Quality | 0.15 | Negative | S-013-01, S-013-02: two claims contradicted by the cited/underlying artifacts |
| Actionability | 0.15 | Negative | S-013-03: verification instructions don't cover the full claim they're meant to substantiate |
| Internal Consistency | 0.20 | Negative | S-013-02: "for all four agents" is inconsistent with sop-verifier's documented (and correct) no-output design stated elsewhere in the same register cluster |
| Completeness | 0.20 | Neutral-to-Negative | S-013-04/05 minor gloss gaps only |
| Methodological Rigor | 0.20 | Neutral | Fix scope (REM-10 only) correctly bounded; no scope creep |
| Traceability | 0.10 | Positive | Commit SHA, CI run link, register section, and worktracker path all resolve correctly |
