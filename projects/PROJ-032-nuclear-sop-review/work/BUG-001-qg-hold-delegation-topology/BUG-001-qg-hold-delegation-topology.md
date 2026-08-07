# BUG-001: QG-HOLD and mid-procedure delegation topology [REM-01]

> **Type:** bug
> **Status:** pending
> **Priority:** critical
> **Impact:** high
> **Severity:** critical
> **Created:** 2026-08-07T11:30:00Z
> **Found In:** PR #269 head bda64202 (branch proj-0039-nuclear-engineer)
> **GitHub Issue:** [#350](https://github.com/geekatron/jerry/issues/350)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Defect, disposition, findings consumed, affected files |
| [Steps to Reproduce](#steps-to-reproduce) | How to observe the defect concretely |
| [Acceptance Criteria](#acceptance-criteria) | Conditions required to close this bug |
| [Related Items](#related-items) | Register, parent story, GitHub issue |

## Summary

The QG-HOLD quality-gate steps in sop-executor are written as the agent's own first-person actions (including "Invoke ps-critic via /adversary S-014") while the same file declares Task ABSENT ("cannot invoke any other agent"), so the H-13 gate cannot fire as designed under H-01/P-003.
The flagship example additionally requires main-context Task calls to ps-researcher/ps-analyst/ps-architect mid-procedure with no suspend/resume protocol; the ps-critic/adv-scorer naming conflation repeats across ~8 files; the composed pattern reaches ~7 Task hops against the HARD H-36 3-hop ceiling; and the /adversary interface dependency carries no version pin or compatibility contract.
Disposition: DEFER-REWORK — choosing the delegation topology (QG-HOLD returns control to main context, orchestrator executes agent-invocation steps, or mid-procedure composition is dropped) is contributor design authority, not maintainer text repair.
Source findings consumed: P1-001, S-001-04, S-013-02, P2-001, S-004-04, S-010-05, S-007-03, S-012-04, S-011-06, S-012-07, S-004-11.
Affected files: `skills/nuclear-sop/agents/sop-executor.md`, `skills/nuclear-sop/composition/sop-executor.prompt.md`, `skills/nuclear-sop/composition/sop-executor.agent.yaml`, `skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md`, `skills/nuclear-sop/examples/c3-adr-workflow-definition.md`, `skills/nuclear-sop/templates/PROCEDURE_STATE.template.yaml`, `skills/nuclear-sop/templates/HOLD_POINT_LOG.template.md`, `skills/nuclear-sop/SKILL.md`, `skills/nuclear-sop/PLAYBOOK.md`, `skills/nuclear-sop/docs/reference.md`, `skills/nuclear-sop/docs/howto-guides.md`.

## Steps to Reproduce

1. On PR #269 head `bda64202`, read the QG-HOLD procedure in `skills/nuclear-sop/agents/sop-executor.md`: it lists "Invoke ps-critic via /adversary S-014" as the executor's own action.
2. In the same file, read the tool declarations: Task is ABSENT, and QG-HOLD has no return-to-main-context step (contrast the adjacent IV-HOLD, which correctly has one).
3. Read `skills/nuclear-sop/examples/c3-adr-workflow-definition.md` procedure Steps 2/4/5: they require main-context Task calls to ps-researcher/ps-analyst/ps-architect inside a sop-executor invocation, while `templates/PROCEDURE_STATE.template.yaml` has only IV-PENDING as a waiting-on-external-actor status.
4. Read the H-36 compliance analysis in `skills/nuclear-sop/SKILL.md` (scoped to the 4 internal agents only) and count Task hops in the composed pattern recommended by `docs/howto-guides.md`: ~7 vs the HARD 3-hop ceiling.

## Acceptance Criteria

- [ ] Contributor redesign answers the register's REM-01 redesign question:
  - Under H-01/P-003 and H-36, who invokes quality gates and external agents mid-procedure, and how does sop-executor suspend and resume place-keeping around them (candidate architectures a/b/c per the register)?
  - The chosen design names adv-scorer (not ps-critic) as the S-014 implementer everywhere, publishes a hop-count budget for the composed pattern, and declares the /adversary interface dependency.
- [ ] Re-review passes before merge.

Both criteria remain unchecked by design; this bug stays open until contributor rework lands and is re-reviewed.

## Related Items

- Remediation register (REM-01): [remediation-register.md](../EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-004-remediation/remediation-register.md#rem-01-qg-hold-and-mid-procedure-delegation-topology)
- Parent story: [STORY-004](../EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-004-remediation/STORY-004-remediation.md)
- GitHub Issue: [#350](https://github.com/geekatron/jerry/issues/350)
