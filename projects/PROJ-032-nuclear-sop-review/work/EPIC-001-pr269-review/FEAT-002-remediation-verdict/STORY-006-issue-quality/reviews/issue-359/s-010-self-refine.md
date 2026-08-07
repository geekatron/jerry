# S-010 Self-Refine — Issue #359 (BUG-010: agent schema conformance)

## Header

| Field | Value |
|-------|-------|
| Strategy | S-010 Self-Refine |
| Deliverable | GitHub issue #359 (geekatron/jerry) — `issue-359.md` snapshot |
| Criticality | C4 (tournament) |
| Date | 2026-08-07 |
| Reviewer | adv-executor (self-refine pass) |
| Iteration | 1 of 1 |

## Summary

The issue is accurate on every load-bearing claim I could fact-check against the remediation register, the commit evidence pack, and the verdict doc: the branch name, commit SHA, CI run link, the two schema-error counts (4 and 2), the unparseable-YAML line reference, and the "8 of 8 files valid" headline all check out against source. The one real defect is a factual overstatement in the "What the fix changed" paragraph — it says output locations were declared for all four agents, but the diff shows `sop-verifier.governance.yaml` deliberately declares **no** location (`output.required: false`, T1 agent, no file artifact). Two Minor gaps round out the findings: an incomplete-but-not-wrong description of the `reasoning_effort` fix, and a "How to verify" step that only lets a reader reproduce half of the "8 of 8" claim. Not ready for external posting as-is — the Major finding should be fixed before this counts as ready; the Minors are optional polish.

## Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| S-010-01 | "output locations declared for all four agents" overstates the fix — sop-verifier gets none | Major | `sop-verifier.governance.yaml` diff: `+  # AD-M-011: no file output declared -- sop-verifier is T1 (read-only)...` `required: false`, no `location:` key added | Evidence Quality / Internal Consistency |
| S-010-02 | "reasoning_effort: high added to the executor" is true but incomplete — sop-brief and sop-capture got the identical addition; sop-verifier's default was a documented choice | Minor | Diff shows `+reasoning_effort: high` in `sop-brief.governance.yaml` and `sop-capture.governance.yaml` too, plus an explicit "intentionally omitted (default)" comment in `sop-verifier.governance.yaml` | Completeness |
| S-010-03 | "How to verify" only reproduces the governance-schema half of the "8 of 8 files valid" claim; no step confirms the 4 `composition/*.agent.yaml` files | Minor | Register fix spec #8: validation requires both `agent-governance-v1.schema.json` (4 files) AND separate YAML-parse + canonical-schema checks for the 4 composition files | Actionability |

## Finding Details

### S-010-01: Output-location claim overstates scope

- **Severity:** Major
- **Affected Dimension:** Evidence Quality / Internal Consistency
- **Evidence:** Issue text: "project-anchored output locations declared for all four agents." Ground truth diff for `sop-verifier.governance.yaml`: the `output:` block changes from `required: true` to `required: false` with the comment "no file output declared -- sop-verifier is T1 (read-only) and cannot write files. The IV report is returned as Task tool response content." No `location:` key is added anywhere in that file.
- **Impact:** An external contributor or their agent trying to verify this line by grepping `sop-verifier.governance.yaml` for a project-anchored `location:` field will find none — and could reasonably conclude the fix is incomplete or the issue is wrong, when in fact the correct, intended fix for that agent was to declare no file output at all. This is exactly the "send the agent down a wrong path" failure mode the mission calls out.
- **Recommendation:** Replace the clause with: "project-anchored output locations declared for the three file-producing agents (sop-brief, sop-executor, sop-capture); sop-verifier's `output.required` was set to `false` since it returns its report as agent response content rather than writing a file." Verify by re-reading the fix and confirming no residual `location:` key exists in `sop-verifier.governance.yaml`.

## Recommendations

1. **Fix S-010-01** (Major) — reword the output-location sentence in "What the fix changed" to distinguish the three agents that got a declared location from sop-verifier's "no file output" resolution. This is the only change needed before the issue is safe to treat as fully accurate.
2. **Fix S-010-02** (Minor, optional) — broaden "reasoning_effort: high added to the executor" to name sop-brief and sop-capture as also receiving it, or drop the specificity and say "reasoning_effort declarations added/confirmed across the four agents per their quality-gate tier" to avoid implying only one agent changed.
3. **Fix S-010-03** (Minor, optional) — add a second verification bullet: "and confirm the four `composition/*.agent.yaml` files parse as valid YAML and pass their own agent schema" so the reader can reproduce "8 of 8," not just 4 of 8.

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | All major claims traced to source; S-010-02/03 are minor omissions, not gaps in coverage |
| Internal Consistency | 0.20 | Negative | S-010-01 states a claim contradicted by the cited evidence for one of the four agents |
| Methodological Rigor | 0.20 | Neutral | No shortcuts detected; every checkable number (4, 2, 8/8, line 9, CI run) verified against source |
| Evidence Quality | 0.15 | Negative | S-010-01's overstatement is an evidence-quality defect specifically |
| Actionability | 0.15 | Negative | S-010-03 leaves the reader unable to fully reproduce the "8/8" claim from the stated verification step alone |
| Traceability | 0.10 | Positive | Worktracker path, register section (REM-10), and CI run link all resolve correctly |

## Decision

**Outcome:** Needs revision (one Major fix) before ready for external posting.

**Rationale:** The issue is substantively accurate and well-sourced — no fabricated facts, no unresolved paths, no wrong severity framing. The single Major finding (S-010-01) is a scope overstatement, not a fabrication, but it is exactly the kind of claim an acting agent would try to mechanically verify and could misread as a broken fix. The two Minor findings are polish, not blockers.

**Next Action:** Apply the S-010-01 reword; Minors are optional. No further S-010 iteration needed — proceed to comparison against other strategies' findings for this issue.
