# BUG-005: H-36 governance ruling [REM-05]

> **Type:** bug
> **Status:** pending
> **Priority:** critical
> **Impact:** high
> **Severity:** critical
> **Created:** 2026-08-07T11:30:00Z
> **Found In:** PR #269 head bda64202 (branch proj-0039-nuclear-engineer)
> **GitHub Issue:** [#354](https://github.com/geekatron/jerry/issues/354)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Defect, disposition, findings consumed, affected files |
| [Steps to Reproduce](#steps-to-reproduce) | How to observe the defect concretely |
| [Acceptance Criteria](#acceptance-criteria) | Conditions required to close this bug |
| [Related Items](#related-items) | Register, parent story, GitHub issue |

## Summary

The H-36 governance ruling that decides whether sop-verifier even exists lapsed on 2026-06-15 (~53 days before review) with no ruling artifact on the branch, no TASK-0039-H36-RULING worktracker entity, and no H-32 GitHub-issue twin — the operative status of the C3+ verification-mode HARD rule cannot be determined from the shipped files.
NS-H-08 mandates 4-hop mode for C3+ "remains as written" until revised, while SKILL.md/PLAYBOOK mandate the opposite default (automatic reversion to 3-hop, sop-verifier eliminated) with a different deadline anchor — two contradictory mandatory instructions, and the default is fail-open: governance inaction removes a safety mechanism for all criticality levels, inverting the skill's own conservative-decision principle (E-2).
This was the review's highest-RPN failure mode (FMEA RPN 648).
Disposition: DEFER-REWORK — the defect is a missing governance decision, not a missing edit; whichever branch a maintainer picked, they would silently be making the ruling, which itself depends on the REM-01 hop-model redesign.
Source findings consumed: P1-018, S-001-05, S-007-04, S-010-06, S-011-07, S-012-01, S-013-05, S-002-06, S-003-02, S-004-03, P2-005.
Affected files: `skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md`, `skills/nuclear-sop/SKILL.md`, `skills/nuclear-sop/PLAYBOOK.md`, worktracker (missing TASK-0039-H36-RULING entity), GitHub issues (missing H-32 twin).

## Steps to Reproduce

1. On PR #269 head `bda64202`, read NS-H-08 in `skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md`: 4-hop verification mode for C3+ "remains as written" until revision, with the deadline anchored to skill registration (2026-06-15).
2. Read `skills/nuclear-sop/SKILL.md` and `skills/nuclear-sop/PLAYBOOK.md`: they state automatic reversion to 3-hop with sop-verifier eliminated, anchored to "Phase 1 delivery" — the opposite fallback semantics.
3. Grep the repo for `TASK-0039-H36-RULING` and search GitHub issues: only the rules file matches itself; no ruling artifact, worktracker entity, or issue exists, and the deadline lapsed ~53 days before the 2026-08-07 review with the shipped files still asserting 4-hop in unqualified present tense.

## Acceptance Criteria

- [ ] Contributor redesign answers the register's REM-05 redesign question:
  - Obtain the actual H-36 ruling (blocked on REM-01's hop-model definition): C3+ retains 4-hop mode with sop-verifier, or reverts to 3-hop and eliminates it.
  - Encode exactly one fallback semantics and one anchor date across NS-H-08, SKILL.md, and PLAYBOOK.md; remove or re-justify the fail-open 60-day default (the conservative default is fail-closed); create the TASK-0039-H36-RULING worktracker entity with an H-32 GitHub issue and a real deadline.
- [ ] Re-review passes before merge.

Both criteria remain unchecked by design; this bug stays open until contributor rework lands and is re-reviewed.

## Related Items

- Remediation register (REM-05): [remediation-register.md](../EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-004-remediation/remediation-register.md#rem-05-h-36-governance-ruling)
- Parent story: [STORY-004](../EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-004-remediation/STORY-004-remediation.md)
- GitHub Issue: [#354](https://github.com/geekatron/jerry/issues/354)
