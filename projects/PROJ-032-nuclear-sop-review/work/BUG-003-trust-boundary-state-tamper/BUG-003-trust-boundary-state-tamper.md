# BUG-003: Trust-boundary integrity and state tamper protection [REM-03]

> **Type:** bug
> **Status:** pending
> **Priority:** critical
> **Impact:** high
> **Severity:** critical
> **Created:** 2026-08-07T11:30:00Z
> **Found In:** PR #269 head bda64202 (branch proj-0039-nuclear-engineer)
> **GitHub Issue:** [#352](https://github.com/geekatron/jerry/issues/352)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Defect, disposition, findings consumed, affected files |
| [Steps to Reproduce](#steps-to-reproduce) | How to observe the defect concretely |
| [Acceptance Criteria](#acceptance-criteria) | Conditions required to close this bug |
| [Related Items](#related-items) | Register, parent story, GitHub issue |

## Summary

sop-verifier's acceptance criteria and expected output paths both originate from the untrusted workflow definition — the skill's own named primary trust boundary TB-1 — so a crafted or maliciously Step-0-generated definition supplies criteria its own outputs trivially satisfy, voiding the skill's differentiating safety mechanism against its own primary threat actor.
Criticality is self-declared by the same untrusted artifact and de-rates every downstream protection, with no cross-check against the framework's auto-escalation table (AE-001/002/004/005).
The documented SHA-256 state_hash tamper-detection control is implemented nowhere (100% inert while documented as active — a P-022 concern), and even as specified a keyless self-computed hash is recomputable by the tampering actor; separately, a poisoned IN-PROGRESS state file resumes cleanly past all three hold types because the SEC-003 check fires only on status == HELD.
Disposition: DEFER-REWORK — inserting a real trust anchor changes the data flow between caller, orchestrator, and agents; a maintainer deleting the false state_hash claim would silently remove a promised safety control, and implementing it would be designing the control.
Source findings consumed: P2-022, P2-023, S-001-03, S-004-01, S-007-01, S-012-05, S-013-03, P2-024.
Affected files: `skills/nuclear-sop/agents/sop-verifier.md`, `skills/nuclear-sop/agents/sop-brief.md`, `skills/nuclear-sop/agents/sop-executor.md`, `skills/nuclear-sop/templates/PROCEDURE_STATE.template.yaml`, `skills/nuclear-sop/docs/reference.md`, `skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md`.

## Steps to Reproduce

1. On PR #269 head `bda64202`, read `skills/nuclear-sop/agents/sop-verifier.md` (SR-09): acceptance criteria and expected paths come from the workflow definition, "the authoritative source" — the same artifact the verifier is supposed to police.
2. Read `templates/PROCEDURE_STATE.template.yaml` and `docs/reference.md`: state_hash is documented as "computed after every state write, verified in STAR-STOP before every tool call".
3. Grep `skills/nuclear-sop/agents/` and `skills/nuclear-sop/composition/` for `state_hash`: no agent file contains any instruction to compute or verify it.
4. Trace the RESUME path in sop-executor: it trusts current_step/next_step/status, and the SEC-003 hold check fires only on status == HELD — a poisoned IN-PROGRESS file bypasses every hold, and sop-capture's SR-05 reconciliation runs only after the irreversible action the hold guarded.

## Acceptance Criteria

- [ ] Contributor redesign answers the register's REM-03 redesign question — an authority model in which no safety control derives from the artifact it polices:
  - (a) a trusted source for sop-verifier's acceptance criteria and expected paths (user-approved brief, orchestrator-supplied criteria, or signed/pinned copy);
  - (b) declared criticality cross-checked and auto-escalated against AE-001/002/004/005 signals;
  - (c) tamper evidence for PROCEDURE_STATE.yaml implemented for real or the claim withdrawn everywhere, with the RESUME-past-holds path closed pre-execution rather than post-hoc.
- [ ] Re-review passes before merge.

Both criteria remain unchecked by design; this bug stays open until contributor rework lands and is re-reviewed.

## Related Items

- Remediation register (REM-03): [remediation-register.md](../EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-004-remediation/remediation-register.md#rem-03-trust-boundary-integrity-and-state-tamper-protection)
- Parent story: [STORY-004](../EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-004-remediation/STORY-004-remediation.md)
- GitHub Issue: [#352](https://github.com/geekatron/jerry/issues/352)
