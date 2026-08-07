# Chain-of-Verification Report: GitHub issue #356 (BUG-007, REM-07)

**Strategy:** S-011 Chain-of-Verification
**Deliverable:** `.../STORY-006-issue-quality/snapshots/final/issue-356.md`
**Criticality:** C4 (tournament)
**H-16 Compliance:** No S-003 Steelman output supplied to this executor (indirect per S-011; proceeding per protocol)
**Claims Extracted:** 7 | **Verified:** 5 | **Discrepancies:** 2 (1 mischaracterization, 1 grouped omission pair)

## Summary

The issue's tracking metadata (severity Major, not-maintainer-fixable, worktracker path, branch, blocks-merge) all verify exactly against the remediation register and log. One factual claim materially mischaracterizes the source: the parenthetical list of "attacker-influenceable inputs" blends a within-document field-coverage gap with two other artifact-injection defects that are tracked as separate, independent issues. Two Major actionability gaps (unnamed control, unnamed file) force a lookup the linked register would otherwise resolve in one read. Recommendation: REVISE (1 Critical text fix; 2 Major additions).

## Findings

| ID | Claim | Discrepancy | Severity |
|----|-------|-------------|----------|
| S-011-01 | "prompt-injection screening ... covers only one of the several attacker-influenceable inputs (workflow definitions, state files, lessons-learned entries, hold-point logs)" | Register's actual gap (REM-07 G2) is that SEC-001 screens only WARNING/CAUTION annotations while *other fields in the same workflow-definition file* (Action, Target, Expected Result, Sign-off Criterion, Hold Reason, Section 2/3/9 prose) are unscreened — a single-document field-coverage gap, not four separate artifact *types*. "State files" (PROCEDURE_STATE.yaml tamper/poisoning) is a distinct defect tracked under a different cluster with its own sibling issue (#352); "lessons-learned entries" (OE-entry injection) is likewise a distinct defect with its own sibling issue (#355). Bundling them into this issue's scope misdirects the redesign work and risks duplicating or contradicting the other two issues. | Critical |
| S-011-02 | "the repository already has a deterministic security enforcement engine this duplicates, weaker, at the prompt level" | Accurate in substance (register: a deterministic engine with an existing test suite already provides this control) but the engine is never named in the issue text, so the reader must open the linked register before they can grep the codebase for it. | Major |
| S-011-03 | Denylist/screening problem described with no file reference | The issue never states which file(s) hold the denylist (the executor agent's definition file) or the Bash-grant scope on the two support agents, forcing a lookup in the linked register before edits can begin. | Major |

## Verified (no discrepancy)

- Severity "major" — matches register (REM-07 Severity: Major).
- "not maintainer-fixable (the gating model must be redesigned, not extended)" — matches register's "Why a maintainer patch is inappropriate" rationale and the remediation log's DEFER-REWORK disposition.
- Worktracker path `projects/PROJ-032-nuclear-sop-review/work/BUG-007-executor-command-gating` — directory exists.
- Register section "REM-07" and file location `.../STORY-004-remediation/` — both resolve; register confirms candidate designs (allowlist / category-based gating / delegation to the deterministic engine) are documented there.
- Branch `feat/proj-032-nuclear-sop-review` — matches active branch.
- "Blocks merge of PR #269" — matches remediation log ("block any merge recommendation").
- Command examples (`nc`, `python -m http.server`, base64-encoded exfiltration) that bypass the denylist — match register verbatim (nc/ncat, `python -m http.server`, base64 exfil all listed as passing).
- "echoes suspect payloads verbatim into logs" — matches register ("logs the payload verbatim into the execution log ... reads — a second-order injection channel").

## Recommendations

- **Critical (S-011-01):** Rewrite the parenthetical to describe the actual gap: e.g., "...covers only WARNING/CAUTION-annotation content; other attacker-controlled fields in the same workflow-definition file (Action, Target, Expected Result, Sign-off Criterion, Hold Reason, and general step prose) are not screened." Add one sentence noting that state-file tampering and lessons-learned-entry injection are tracked as separate issues (do not fold them into this one's redesign ask).
- **Major (S-011-02):** Name the control, e.g., "...duplicates, weaker, the repo's existing deterministic SecurityEnforcementEngine at the prompt level."
- **Major (S-011-03):** Add one line naming the primary file(s), e.g., "Primary location: the sop-executor agent's command-gating logic in `skills/nuclear-sop/agents/sop-executor.md`; Bash-grant scope also affects the sop-brief and sop-capture agent definitions."

## Scoring Impact

| Dimension | Impact | Rationale |
|-----------|--------|-----------|
| Evidence Quality | Negative | S-011-01 misstates the source finding's shape (fields-within-one-document vs. four artifact types) |
| Actionability | Negative | S-011-02/03 force a lookup before the fix location and reference control are known |
| Traceability | Negative | S-011-01 pulls in scope from two other tracked issues without citing them, breaking clean issue-to-issue separation |
| Completeness | Neutral | Core defect (denylist enumerability, redesign options) is present |
| Internal Consistency | Neutral | No self-contradiction within the issue text |
| Methodological Rigor | Neutral | Not applicable to this artifact type |
