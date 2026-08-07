# BUG-008: Registration and status truth reconciliation [REM-08]

> **Type:** bug
> **Status:** completed
> **Priority:** critical
> **Impact:** high
> **Severity:** critical
> **Created:** 2026-08-07T11:30:00Z
> **Completed:** 2026-08-07T13:30:00Z
> **Found In:** PR #269 head bda64202 (branch proj-0039-nuclear-engineer)
> **GitHub Issue:** [#357](https://github.com/geekatron/jerry/issues/357)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Defect, disposition, findings consumed, affected files |
| [Steps to Reproduce](#steps-to-reproduce) | How to observe the defect concretely |
| [Acceptance Criteria](#acceptance-criteria) | Observable outcomes of the fix |
| [Related Items](#related-items) | Register, parent story, GitHub issue |

## Summary

SKILL.md's DEFERRED REGISTRATION NOTE ("NOT registered and NOT live-routable until QG-E6 passes and the user applies these entries") is false as shipped: the same PR registers the skill in CLAUDE.md:78, AGENTS.md, `.context/rules/mandatory-skill-usage.md` (priority-16 row), plugin.json:53-56, and CHANGELOG.md — and QG-E6 passed (0.934, 2026-04-14, qg-e6-score.md).
The "copy-ready" trigger row in SKILL.md (priority 12) diverges from the applied row (priority 16) and would regress the live routing table if re-applied; and PLAYBOOK.md (~line 677, "NOT available for C3+ ... restrict to C1-C2 only") directly contradicts SKILL.md (~lines 229/244, "C3+ APPROVED ... all criticality levels") on the package's most safety-relevant question.
Disposition: FIX-NOW — all defects are false or contradictory claims fixable by maintainer text correction on the contributor branch; the reconciliation direction is dictated by honesty plus REM-04 (registration is a fact: accept and document it; C3+ approval is not currently supportable: withdraw it pending re-validation).
Source findings consumed: S-001-01, S-002-02, S-004-02, S-007-05, S-011-01, S-012-02, S-013-01, P2-009, P1-016, S-003-03, S-010-02, P1-017, S-012-13.
Affected files: `skills/nuclear-sop/SKILL.md`, `skills/nuclear-sop/PLAYBOOK.md` (verify consistency: `CHANGELOG.md`).

## Steps to Reproduce

1. On PR #269 head `bda64202`, read `skills/nuclear-sop/SKILL.md` ~line 446 ("NOT registered and NOT live-routable"), then open CLAUDE.md:78, AGENTS.md, `.context/rules/mandatory-skill-usage.md`, and plugin.json:53-56 in the same PR: the registration entries are already applied.
2. Compare SKILL.md's ~line 476 copy-ready trigger row (priority 12, 9 negatives, 5 compounds) with the applied `.context/rules/mandatory-skill-usage.md` row (priority 16, expanded negatives, 8 compounds).
3. Read `skills/nuclear-sop/PLAYBOOK.md` ~line 677 against SKILL.md ~lines 229/244: the two entry-point documents give opposite answers on C3+ availability.

## Acceptance Criteria

- [x] SKILL.md's DEFERRED REGISTRATION NOTE replaced with a "REGISTRATION STATUS: APPLIED" note citing the applied surfaces and qg-e6-score.md (0.934 PASS, 2026-04-14) by resolvable path; all "NOT registered"/"NOT live-routable"/"user applies these entries" sentences removed. (verified 2026-08-07)
- [x] Stale priority-12 copy-ready trigger-row block deleted and replaced with a pointer naming `.context/rules/mandatory-skill-usage.md` as the live SSOT row (no second copy that can drift). (verified 2026-08-07)
- [x] C3+ status reconciled conservatively: SKILL.md states "C3+ status: WITHDRAWN pending re-validation ... Approved use: C1-C2 only"; "empirically validated ... 3/3 catch rate (100%)" reworded to "simulation walkthrough (desk-check); not independent execution evidence"; PLAYBOOK.md keeps the C1-C2 restriction citing the PROJ-032 invalidation; stale future-tense QG-E4 scaffolding removed from SKILL.md's gate table. (verified 2026-08-07)
- [x] SEC-008 noted as OPEN with remediation tracked in REM-12; no unconditional C1-C4 approval asserted anywhere. (verified 2026-08-07)
- [x] Validation greps pass: `grep -rn "NOT registered\|NOT live-routable\|priority.*12" skills/nuclear-sop/SKILL.md` → 0 hits; `grep -rn "approved for all criticality\|C1 through C4" skills/nuclear-sop/` → 0 unqualified hits; SKILL.md and PLAYBOOK.md state the same C1-C2 restriction. (verified 2026-08-07)
- [x] Fix commit pushed to proj-0039-nuclear-engineer and referenced here. — commit c07033ce
- [x] PR #269 CI green at post-fix head. — 15/15, run 31174766440

## Related Items

- Remediation register (REM-08): [remediation-register.md](../EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-004-remediation/remediation-register.md#rem-08-registration-and-status-truth-reconciliation)
- Parent story: [STORY-004](../EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-004-remediation/STORY-004-remediation.md)
- GitHub Issue: [#357](https://github.com/geekatron/jerry/issues/357)
