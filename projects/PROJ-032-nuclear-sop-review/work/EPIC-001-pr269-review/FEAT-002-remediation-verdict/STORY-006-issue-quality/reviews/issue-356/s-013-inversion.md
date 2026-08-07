# Inversion Report: GitHub Issue #356 (BUG-007 / REM-07 command gating)

**Strategy:** S-013 Inversion Technique
**Deliverable:** `snapshots/final/issue-356.md` (live text of geekatron/jerry issue #356)
**Criticality:** C4 (tournament)
**Goals inverted:** 3 (accurate scope, self-contained actionability, resolvable references)
**Assumptions mapped:** 4 | **Vulnerable assumptions:** 2

## Summary

The issue's core claims about the substring denylist and the duplicated security control are accurate and well-cited. Inversion finds one Critical vulnerability: the injection-screening gap is mischaracterized as spanning four separate document types rather than the actual gap — untreated prose fields *inside* the workflow definition itself — which risks the assignee re-scoping work already owned by two other open issues. One Major actionability gap (unnamed, pathless "deterministic security enforcement engine") and one Minor completeness gap round out the findings. Recommendation: REVISE (one text fix + one path addition) before this can be scored ACCEPT.

## Findings Table

| ID | Assumption / Anti-Goal | Type | Confidence | Severity | Evidence | Affected Dimension |
|----|------------------------|------|------------|----------|----------|--------------------|
| S-013-01 | "Injection-screening scope = 4 document types (workflow definitions, state files, lessons-learned entries, hold-point logs)" | Assumption (inverted: this claim is false) | High | Critical | register REM-07 G2; verdict.md L134; `sop-executor.md:142` | Completeness / Evidence Quality |
| S-013-02 | "Reader can identify 'the existing deterministic enforcement engine' from the text alone" | Assumption | High | Major | `src/infrastructure/internal/enforcement/security_enforcement_engine.py` not cited in issue | Actionability |
| S-013-03 | "Nothing can be done on this defect before the full redesign lands" | Anti-goal (unstated, but implied by omission) | Medium | Minor | register REM-07 parenthetical: interim Bash-grant narrowing available now | Completeness |

## Finding Details

### S-013-01: Injection-screening scope inverted from field-level to document-type-level [CRITICAL]

**Type:** Assumption (the issue asserts a specific scope for the injection-screening gap)
**Original claim (issue text):** "the skill's prompt-injection screening likewise covers only one of the several attacker-influenceable inputs (workflow definitions, state files, lessons-learned entries, hold-point logs) that end up driving tool calls."
**Inversion — what if this scope statement is wrong?** Ground truth (remediation-register.md REM-07 group G2, and verdict.md's own restatement of the design question — "injection-screening scope across *all* definition-sourced fields that drive tool calls") says the actual gap is: SEC-001 screens only the WARNING/CAUTION annotation text *inside the workflow-definition file* (confirmed directly in `sop-executor.md` line 142: "WARNING/CAUTION content authority scope (SEC-001 injection guard)"); it does not screen the Action, Target, Expected Result, Sign-off Criterion, Hold Reason, or Section 2/3/9 prose fields — all *within that same file*. There is no finding in REM-07 about screening state files, hold-point logs, or lessons-learned (OE) entries as separate channels.
**Plausibility:** Confirmed, not merely plausible — both the register and the actual agent source were checked directly.
**Consequence:** State-file tamper protection is a *different*, already-open defect (REM-03 / BUG-003 / issue #352 — "State-file poisoning steers execution past holds"), and OE/lessons-learned entry injection is governed by a *separate* control, SEC-002 (REM-06 / BUG-006 / issue #355). An external contributor or their agent reading only issue #356 will reasonably scope a fix across four document types, duplicating or conflicting with the redesign work already tracked in #352 and #355, while the actual unscreened fields (Action/Target/Expected Result/Sign-off Criterion/Hold Reason/Section 2-3-9 prose) go unmentioned and could be missed entirely.
**Dimension:** Completeness (the true scope is narrower and different) / Evidence Quality (claim not traceable to the cited source).
**Mitigation:** Replace the parenthetical with the field-level scope, e.g.: "...covers only the WARNING/CAUTION annotation text; it does not screen the Action, Target, Expected Result, Sign-off Criterion, Hold Reason, or narrative prose fields of the same workflow-definition file — all equally attacker-controlled and equally able to drive tool calls. (State-file and lessons-learned-entry injection are tracked separately in #352 and #355.)"
**Acceptance Criteria:** Revised sentence names only workflow-definition-internal fields as the screening gap, and either drops the state-file/lessons-learned/hold-point-log framing or explicitly cross-references #352/#355 to prevent scope collision.

### S-013-02: "Deterministic security enforcement engine" has no name or path [MAJOR]

**Type:** Assumption ("the repository already has a deterministic security enforcement engine" is discoverable without a pointer)
**Original claim:** "the repository already has a deterministic security enforcement engine this duplicates, weaker, at the prompt level" — mentioned twice (problem statement and design question) with no name or path.
**Inversion:** If the reader cannot locate this engine quickly, the delegation option in the design question ("delegation to the existing deterministic enforcement engine") is unevaluable without a repo-wide search.
**Consequence:** Verified: the class is `SecurityEnforcementEngine` at `src/infrastructure/internal/enforcement/security_enforcement_engine.py`, wired in via `src/interface/cli/hooks/hooks_pre_tool_use_handler.py`. Neither name nor path appears in the issue text, forcing a lookup the issue could eliminate in one clause.
**Dimension:** Actionability.
**Mitigation:** Add the path once, e.g.: "...duplicates, weaker, the repo's existing `SecurityEnforcementEngine` (`src/infrastructure/internal/enforcement/security_enforcement_engine.py`), at the prompt level."
**Acceptance Criteria:** Issue text names the class and file path at first mention.

## Recommendations

- **MUST mitigate (Critical):** S-013-01 — correct the injection-screening scope sentence per the mitigation above; this is a factual-accuracy defect, not a style issue.
- **SHOULD mitigate (Major):** S-013-02 — add the `SecurityEnforcementEngine` path.
- **MAY mitigate (Minor):** S-013-03 — the register notes an interim mitigation available today (narrow sop-brief/sop-capture's Bash grants; their declared needs are already covered by other tools) without waiting on the full gating redesign. One added sentence would give the reader a concrete near-term action alongside the long-term design question.

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | S-013-01: true scope (field-level, single file) is narrower and different from the stated scope (four document types) |
| Internal Consistency | 0.20 | Neutral | No internal contradiction within the issue text itself |
| Methodological Rigor | 0.20 | Neutral | N/A for a communication artifact |
| Evidence Quality | 0.15 | Negative | S-013-01: claim not traceable to the register it is (implicitly) drawn from |
| Actionability | 0.15 | Negative | S-013-02: delegation option unevaluable without a repo search |
| Traceability | 0.10 | Neutral | Tracking footer's paths and branch name verified accurate |

**Result:** 1 Critical, 1 Major, 1 Minor. The Critical finding is a scope-accuracy defect that could misdirect remediation into two unrelated open issues (#352, #355); it is the single highest-priority fix for this issue text.
