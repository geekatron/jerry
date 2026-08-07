# S-010 Self-Refine — Issue #355 (BUG-006 / REM-06: OE feedback-loop design)

| Field | Value |
|-------|-------|
| Strategy | S-010 Self-Refine |
| Deliverable | GitHub issue #355 (final snapshot, `snapshots/final/issue-355.md`) |
| Criticality | C4 (tournament) |
| Iteration | 1 of 1 (adapted, compact) |
| Objectivity check | Low attachment (fresh review, no authorship investment) — proceeding |

## Summary

The issue is factually accurate on every checked claim (synthesis-entry-type/schema gap, per-workflow_type STOP ratchet, cross-criticality injection channel, provenance false-fire after `work/` cleanup — all verified against the register, the rules file, and `sop-capture.md`/`sop-brief.md` on the PR worktree) and is honestly framed (Major, "not maintainer-fixable," correct worktracker/register paths verified to exist, branch confirmed live on GitHub). One actionability gap: the design question compresses two distinct required design elements from the source register into one ambiguous phrase. Ready for external review after one targeted edit.

## Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| S-010-01 | Design question conflates "retention surviving cleanup" and "injection trust model" into one phrase | Major | Body's 3rd clause names a distinct problem (provenance false-fire after `work/` cleanup) but the design question's closing clause — "a provenance/trust model for a corpus shared across risk levels" — reads as one ask, matching only the cross-criticality injection problem (2nd clause) | Actionability |
| S-010-02 | Register reference is a path+branch pair, not a clickable URL | Minor | "`remediation-register.md` in `...STORY-004-remediation/` on branch `feat/proj-032-nuclear-sop-review`" requires the reader to hand-assemble a `blob` URL | Actionability |
| S-010-03 | Title stacks two unexplained internal IDs before the plain-language description | Minor | Title: "PROJ-032/BUG-006: nuclear-sop — lessons-learned loop can't work as specified..." — a reader with zero repo-governance context cannot tell what "BUG-006" denotes from the title alone (only the Tracking footer clarifies it) | Completeness (self-containedness) |

## Finding Details

**S-010-01: Design question under-specifies the retention/archival ask**
- **Severity:** Major
- **Affected Dimension:** Actionability
- **Evidence:** Register REM-06's own redesign question separates the ask into distinct items: "...a provenance mechanism that survives `work/` cleanup (or an archival rule), and an injection trust model for the corpus (guard labels on every interpolated field...)." The issue collapses these into: "...and a provenance/trust model for a corpus shared across risk levels." The body's own third clause ("the provenance flags false-fire after routine cleanup of the work directory") names the retention problem explicitly, but the design question at the end does not ask for a fix to it by name — a contributor could satisfy "provenance/trust model... shared across risk levels" with only an injection-guard improvement and never address why every legitimate entry goes permanently `[PROVENANCE-UNVERIFIED]` after routine cleanup.
- **Impact:** A design that ships a synthesis schema + safe thresholds + injection guards but no retention/archival rule would look complete against this issue's stated design question while leaving one of the issue's own three named defects (provenance false-fire) unresolved — exactly the kind of silent gap H-31 (clarify before acting) exists to prevent.
- **Recommendation:** Split the closing clause into two explicit asks, e.g.: "...thresholds that cannot deadlock unrelated executions, a retention/archival rule so provenance survives routine `work/` cleanup, and an injection-trust model for a corpus shared across risk levels."

## Recommendations

1. **Split the retention/archival ask out of the design question** (resolves S-010-01) — mirrors the body's own three-clause structure so all three named defects are explicitly assigned to a fix.
2. **Turn the register reference into a clickable link** (resolves S-010-02) — e.g. `[remediation-register.md](https://github.com/geekatron/jerry/blob/feat/proj-032-nuclear-sop-review/projects/PROJ-032-nuclear-sop-review/work/EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-004-remediation/remediation-register.md#rem-06-oe-feedback-loop-design)`.
3. **Move/trim the internal ID stack in the title** (resolves S-010-03) — e.g. lead with the plain description and keep `PROJ-032/BUG-006` as a trailing tag, or drop it from the title entirely since the Tracking line already carries it.

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | Title ID stack (S-010-03) is a minor self-containedness nit; substance is complete |
| Internal Consistency | 0.20 | Positive | No contradictions found between issue text and any ground-truth source |
| Methodological Rigor | 0.20 | Positive | Fact-checked against register, verdict, rules file, and PR worktree source files directly |
| Evidence Quality | 0.15 | Positive | Every claim in the issue traced to a specific register clause or source-file line |
| Actionability | 0.15 | Negative | S-010-01 (Major): design question drops one of three named problems from its explicit ask |
| Traceability | 0.10 | Positive | Worktracker path and register path both verified to exist on disk; branch verified live on GitHub |

## Decision

**Outcome:** Needs one targeted revision (S-010-01), then ready for external review.

**Rationale:** No Critical findings — all factual claims verified true against ground truth, paths resolve, branch is live, severity/disposition framing is honest, and length (~230 words) is appropriately concise. The single Major finding is an actionability gap, not a factual error: the design question as worded could let a contributor's fix pass a self-check while leaving the provenance-retention defect open.

**Next Action:** Apply Recommendation 1 (and 2/3 if time permits), then this issue is ready for the S-014 tournament composite scoring pass.
