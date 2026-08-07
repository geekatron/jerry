# S-010 Self-Refine — Issue #356 (BUG-007: executor command gating)

| Field | Value |
|-------|-------|
| Strategy | S-010 Self-Refine |
| Deliverable | GitHub issue #356 (`snapshots/final/issue-356.md`) |
| Criticality | C4 (tournament) |
| Date | 2026-08-07 |
| Reviewer | adv-executor (self-refine pass) |
| Iteration | 1 of 1 |

## Summary

The issue is well-written for an external, governance-blind audience — no unexplained internal codes, a clear one-sentence problem, a resolvable worktracker/register path, and a design question that (mostly) matches the register. One finding is Critical: the opening paragraph's parenthetical list of "attacker-influenceable inputs" pulls in two artifact categories (state files, lessons-learned/OE entries) that are actually the fully-owned scope of two *other* already-filed issues, creating a real risk of duplicated or misdirected rework. Two Minor polish items would improve actionability. Objectivity check: low attachment (fresh review, no prior investment in this text) — findings below are not leniency-adjusted upward.

## Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| S-010-01 | Injection-screening scope list conflates 3 separate remediation clusters into this issue | Critical | Body: "(workflow definitions, state files, lessons-learned entries, hold-point logs)" vs. design question: "definition-sourced fields" | Internal Consistency, Evidence Quality |
| S-010-02 | "Deterministic security enforcement engine" not named/pathed | Minor | Body: "the repository already has a deterministic security enforcement engine this duplicates" — no name or path | Actionability |
| S-010-03 | No mention of the available interim mitigation (narrowing Bash grants) while redesign is pending | Minor | Register REM-07 rationale notes sop-brief/sop-capture's Bash grants could be narrowed today without redesign; issue omits this | Completeness |

## Finding Details

### S-010-01: Injection-screening scope conflates three remediation clusters

- **Severity:** Critical
- **Affected Dimension:** Internal Consistency, Evidence Quality
- **Evidence:** Issue body says injection screening "covers only one of the several attacker-influenceable inputs (workflow definitions, state files, lessons-learned entries, hold-point logs) that end up driving tool calls." The issue's own "design question" paragraph, by contrast, correctly scopes the fix to "definition-sourced fields" — i.e., fields *within* the workflow definition (register REM-07 G2: "Action, Target, Expected Result, Sign-off Criterion, Hold Reason, and Sections 2/3/9 prose" — all fields of one file). Cross-checked against sibling issues in the same snapshot set: `issue-352.md` (BUG-003/REM-03) already owns "the execution-state file carries SHA-256 tamper detection; no such mechanism is implemented" (i.e., "state files"), and `issue-355.md` (BUG-006/REM-06) already owns "the store is also a prompt-injection channel (low-risk runs write files that high-risk runs read), mitigated only by a text label" (i.e., "lessons-learned entries" / OE corpus). Neither state-file tamper protection nor OE-entry injection screening is discussed anywhere in register section REM-07.
- **Impact:** An external contributor (or their agent) reading only this issue would reasonably conclude that fixing BUG-007 requires adding injection screening to state files and OE/lessons-learned entries — work that is separately scoped, tracked, and already has its own design question in issues #352 and #355. This risks duplicate design work, an over-scoped PR, or the contributor believing #352/#355 are subsumed here and skipping them. It also creates an internal contradiction: the body's implied scope (4 artifact types) does not match the design question's actual scope (fields within 1 artifact type), so a careful reader cannot tell which is authoritative without reading the linked register.
- **Recommendation:** Narrow the parenthetical to what REM-07 actually covers, e.g.: "...covers only the WARNING/CAUTION annotation field, while several other fields in the same workflow definition (the step's Action, Target, Expected Result, Sign-off Criterion, and Hold Reason, plus free-text prose sections) are equally attacker-controlled and drive tool calls directly." Optionally add one clause noting the boundary: "(state-file tampering and lessons-learned/OE injection are tracked separately as #352 and #355)."

### S-010-02: Security engine reference not resolvable

- **Severity:** Minor
- **Affected Dimension:** Actionability
- **Evidence:** "Meanwhile the repository already has a deterministic security enforcement engine this duplicates, weaker, at the prompt level." No module name or path given (verified the module exists at `src/infrastructure/internal/enforcement/security_enforcement_engine.py` in the PR worktree).
- **Impact:** A contributor evaluating the "delegate to the existing engine" option has to open the linked register just to learn what to delegate to, which is one extra hop for the single most concrete remediation option offered.
- **Recommendation:** Name it inline: "...a deterministic security enforcement engine (`src/infrastructure/internal/enforcement/security_enforcement_engine.py`, 82 tests) this duplicates, weaker, at the prompt level."

### S-010-03: Interim mitigation omitted

- **Severity:** Minor
- **Affected Dimension:** Completeness
- **Evidence:** Register REM-07 rationale: "(Interim mitigations a maintainer *could* take without redesign — narrowing sop-brief/sop-capture's Bash grants, since their declared needs are covered by other tools — are noted, but the cluster's resolution is the gating model.)" Not mentioned in the issue.
- **Impact:** Minor — a reader has no way to know a low-risk, non-blocking stopgap exists while the real redesign is pending; not knowing this doesn't send them the wrong way, it's just a missed opportunity.
- **Recommendation:** Optional one-clause addition to the Tracking line: "Interim step available without redesign: narrow sop-brief/sop-capture's Bash grants (their declared needs are already covered by other tools)."

## Recommendations (priority order)

1. **Fix S-010-01** — rescope the parenthetical to definition-internal fields and/or cross-reference #352/#355 to establish the scope boundary. (resolves S-010-01)
2. Name the security-engine module/path inline. (resolves S-010-02)
3. Optionally note the interim Bash-grant-narrowing mitigation. (resolves S-010-03)

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | S-010-03: interim mitigation option omitted |
| Internal Consistency | 0.20 | Negative | S-010-01: body scope contradicts design-question scope (Critical) |
| Methodological Rigor | 0.20 | Neutral | Register-to-issue narrowing otherwise followed correctly |
| Evidence Quality | 0.15 | Negative | S-010-01: parenthetical list not traceable to REM-07's own findings |
| Actionability | 0.15 | Negative | S-010-02: no resolvable path to the referenced existing engine |
| Traceability | 0.10 | Positive | Worktracker path, register path, and branch all verified to resolve on disk |

## Decision

**Outcome:** Needs revision before external posting readiness is re-confirmed.

**Rationale:** One Critical finding (S-010-01) is a genuine scope/accuracy defect that could misdirect implementation work across three different issues; the two Minor findings are low-cost actionability polish. This is a single, well-contained text; leniency bias was counteracted by explicitly cross-checking sibling issue snapshots (#352, #355) rather than accepting the parenthetical at face value.

**Next Action:** Apply the S-010-01 fix (rescope + optional cross-reference), then this deliverable is ready for the remaining tournament strategies' independent findings to be reconciled at the scoring stage.
