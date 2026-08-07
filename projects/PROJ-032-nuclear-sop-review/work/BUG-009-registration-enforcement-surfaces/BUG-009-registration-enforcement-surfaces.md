# BUG-009: Registration enforcement surfaces [REM-09]

> **Type:** bug
> **Status:** completed
> **Priority:** critical
> **Impact:** high
> **Severity:** critical
> **Created:** 2026-08-07T11:30:00Z
> **Completed:** 2026-08-07T13:30:00Z
> **Found In:** PR #269 head bda64202 (branch proj-0039-nuclear-engineer)
> **GitHub Issue:** [#358](https://github.com/geekatron/jerry/issues/358)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Defect, disposition, findings consumed, affected files |
| [Steps to Reproduce](#steps-to-reproduce) | How to observe the defect concretely |
| [Acceptance Criteria](#acceptance-criteria) | Observable outcomes of the fix |
| [Related Items](#related-items) | Register, parent story, GitHub issue |

## Summary

/nuclear-sop is the only trigger-mapped skill absent from both the H-22 rule sentence and the L2-REINJECT comment in `.context/rules/mandatory-skill-usage.md`, so the context-rot-immune per-prompt enforcement never covers it — it routes only via the rot-vulnerable L1 trigger map, even though the PR's own phase-6 artifact (registration-trigger-map-row.md) prescribed the exact missing sentence.
The documented activation keyword "nuclear workflow" deterministically misroutes to /orchestration ("workflow" positive at priority 1; no "nuclear" negative; no such compound trigger exists), and the phase-6 collision analysis falsely claims a compound trigger covers it.
AGENTS.md was never updated for the 4 new agents: no nav-table entry, no Agent Summary row, Total still 89 (correct: 93), stale "Last verified: 2026-03-09", and sop-* absent from the MCP "Not included (by design)" note.
Disposition: FIX-NOW — registration-surface gaps and registry bookkeeping are mechanical edits with exact prescribed content.
Source findings consumed: P1-019, S-007-06, S-011-02, S-012-03, P1-020, S-003-05, S-003-06, S-007-07, S-012-10.
Affected files: `.context/rules/mandatory-skill-usage.md`, `AGENTS.md`, phase-6 collision-analysis artifact under «PR projects tree»/PROJ-0039-nuclear-engineer.

## Steps to Reproduce

1. On PR #269 head `bda64202`, run `grep -n "nuclear-sop" .context/rules/mandatory-skill-usage.md`: present in the trigger-map row but absent from the H-22 rule sentence and the L2-REINJECT comment.
2. Simulate routing of "nuclear workflow" per the routing algorithm in `.context/rules/agent-routing-standards.md`: "workflow" matches /orchestration (priority 1), no "nuclear" negative keyword or compound trigger exists, so Step 3 resolves priority 1 over 16 — deterministic misroute.
3. Read `AGENTS.md`: no "Nuclear SOP Skill Agents" nav-table entry or Agent Summary row; Total = 89 while 4 sop-* agents ship in the PR (correct: 93); "Last verified: 2026-03-09"; sop-* missing from the MCP exclusion note.

## Acceptance Criteria

- [x] H-22 rule cell in `.context/rules/mandatory-skill-usage.md` contains the /nuclear-sop sentence (exact wording from registration-trigger-map-row.md), inserted after the /contract-design clause. (verified 2026-08-07)
- [x] The L2-REINJECT comment enumeration in the same file includes /nuclear-sop. (verified 2026-08-07)
- [x] The /nuclear-sop trigger row's Compound Triggers extended with `"nuclear workflow" OR "nuclear sop" (phrase match)`; the /orchestration row untouched; the phase-6 collision-analysis artifact annotated as corrected/superseded. (verified 2026-08-07)
- [x] AGENTS.md updated: "Nuclear SOP Skill Agents" nav-table entry with anchor link; Agent Summary row (Nuclear SOP | 4 agents); Total 89 → 93; "Last verified" updated to the fix date; sop-* appended to the MCP "Not included (by design)" note with file-based-persistence-per-P-002 wording mirroring wt-*/eng-*/red-*. (verified 2026-08-07)
- [x] Validation passes: grep confirms "nuclear-sop" in the H-22 sentence, L2-REINJECT comment, and trigger row; simulated routing of "nuclear workflow" resolves to /nuclear-sop via compound trigger; AGENTS.md total equals the count of registered agents; every `##` heading in AGENTS.md appears in its nav table. (verified 2026-08-07)
- [x] Fix commit pushed to proj-0039-nuclear-engineer and referenced here. — commit c07033ce
- [x] PR #269 CI green at post-fix head. — 15/15, run 31174766440

## Related Items

- Remediation register (REM-09): [remediation-register.md](../EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-004-remediation/remediation-register.md#rem-09-registration-enforcement-surfaces)
- Parent story: [STORY-004](../EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-004-remediation/STORY-004-remediation.md)
- GitHub Issue: [#358](https://github.com/geekatron/jerry/issues/358)
