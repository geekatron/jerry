# BUG-002: USER-HOLD mechanism and runtime execution model [REM-02]

> **Type:** bug
> **Status:** pending
> **Priority:** critical
> **Impact:** high
> **Severity:** critical
> **Created:** 2026-08-07T11:30:00Z
> **Found In:** PR #269 head bda64202 (branch proj-0039-nuclear-engineer)
> **GitHub Issue:** [#351](https://github.com/geekatron/jerry/issues/351)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Defect, disposition, findings consumed, affected files |
| [Steps to Reproduce](#steps-to-reproduce) | How to observe the defect concretely |
| [Acceptance Criteria](#acceptance-criteria) | Conditions required to close this bug |
| [Related Items](#related-items) | Register, parent story, GitHub issue |

## Summary

USER-HOLD — the skill's sole P-020/H-02 user-authority mechanism — requires AskUserQuestion, a tool absent from the agent's grant, absent from every T1-T5 tier, and used by zero of 89 shipped agents, while governance forbids all fallbacks ("NEVER simulate. NEVER auto-approve."); sop-brief has the identical defect at all six interactive STOP gates.
The runtime execution model is never pinned: SKILL.md diagrams all four agents as worker subagents, which cannot pause mid-run to converse with the user, and each candidate model (subagent vs main-context persona) breaks a different declared guarantee.
Further: USER-HOLD has no timeout/unattended policy, SR-02 permits a fully autonomous C4 irreversible workflow as WARNING-only, NS-H-01's STAR-before-every-Write is non-terminating as written, and the context budget (6 tool calls/step, O(corpus) briefs, checkpoint-at-80% with no measurement step, tight step ceilings) is asserted without a token model.
Disposition: DEFER-REWORK — pinning the runtime model and making the interactive gates real under it is architecture work with cascading effects on the rules, baselines, and all four agents.
Source findings consumed: P1-002, P2-015, S-004-10, S-001-07, P2-002, P2-019, S-004-08, S-004-09.
Affected files: `skills/nuclear-sop/agents/sop-executor.md`, `skills/nuclear-sop/agents/sop-executor.governance.yaml`, `skills/nuclear-sop/agents/sop-brief.md`, `skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md`, `skills/nuclear-sop/behavioral-baselines/` (bb-001, bb-002), `skills/nuclear-sop/SKILL.md`, `skills/nuclear-sop/templates/PRE_JOB_BRIEF.template.md`.

## Steps to Reproduce

1. On PR #269 head `bda64202`, read the USER-HOLD section of `skills/nuclear-sop/agents/sop-executor.md`: AskUserQuestion is declared "the sole mechanism" with all fallbacks forbidden.
2. Read the same file's tool grant and the T1-T5 tier table in `.context/rules/agent-development-standards.md`: AskUserQuestion appears in neither; grep `skills/*/agents/*.md` — zero of 89 shipped agents use it.
3. Read the SKILL.md architecture diagrams: all four agents run as worker subagents, which cannot pause mid-run to converse with the user; bb-002's forbidden-pattern table makes every conceivable run a violation.
4. Read NS-H-01 against NS-H-10 in `rules/nuclear-sop-behavior-rules.md`: recording STAR is itself a Write and NS-H-10 mandates a state Edit per step, so STAR-before-every-Write never terminates; bb-001 silently exempts bookkeeping writes, contradicting the HARD rule's plain text.

## Acceptance Criteria

- [ ] Contributor redesign answers the register's REM-02 redesign question:
  - Pin the runtime execution model; make USER-HOLD real under it (return-to-orchestrator protocol with statuses and resume semantics, or re-justified tool-tier enforcement and verifier isolation under persona mode).
  - Rewrite NS-H-01 with a terminating scope and re-align bb-001; give USER-HOLD a timeout/unattended policy; decide whether SR-02 at C3+ escalates to STOP; publish a token/context model justifying step limits, brief size, and a concrete checkpoint mechanism.
- [ ] Re-review passes before merge.

Both criteria remain unchecked by design; this bug stays open until contributor rework lands and is re-reviewed.

## Related Items

- Remediation register (REM-02): [remediation-register.md](../EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-004-remediation/remediation-register.md#rem-02-user-hold-mechanism-and-runtime-execution-model)
- Parent story: [STORY-004](../EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-004-remediation/STORY-004-remediation.md)
- GitHub Issue: [#351](https://github.com/geekatron/jerry/issues/351)
