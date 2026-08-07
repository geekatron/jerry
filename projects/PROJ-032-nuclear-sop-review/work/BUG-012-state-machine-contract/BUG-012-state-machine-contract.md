# BUG-012: State machine and completion contract reconciliation [REM-12]

> **Type:** bug
> **Status:** in_progress
> **Priority:** critical
> **Impact:** high
> **Severity:** critical
> **Created:** 2026-08-07T11:30:00Z
> **Found In:** PR #269 head bda64202 (branch proj-0039-nuclear-engineer)
> **GitHub Issue:** [#361](https://github.com/geekatron/jerry/issues/361)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Defect, disposition, findings consumed, affected files |
| [Steps to Reproduce](#steps-to-reproduce) | How to observe the defect concretely |
| [Acceptance Criteria](#acceptance-criteria) | Observable outcomes of the fix |
| [Related Items](#related-items) | Register, parent story, GitHub issue |

## Summary

Three inconsistent state machines ship: rules/PLAYBOOK say IV-PENDING → IV-PASSED | IV-REJECTED, template comments say IV-PENDING → HELD on REJECT, IV-REJECTED is in the template's valid-status list with no transition, bb-002 requires outcome WAIVED while the template field allows only PASS | DEVIATION, and the template permits "Any state → RESUMING" against the rules' single successor — so SEC-003 checks fire on legitimate runs or get learned as noise.
The completion contract is self-contradictory and type-broken: the executor's Phase 2 sets COMPLETED before sop-capture exists (forbidden by NS-H-06) and sets execution_log_final to a path while sop-capture Step 1 requires it to be literally `true` and HALTs otherwise — a literal reading halts the mandatory OE-capture phase of every execution.
sop-verifier's Step 6 hold-point check uses an "if accessible" conditional that silently skips with no anomaly when PROCEDURE_STATE.yaml is absent — recorded OPEN, RPN-144, REMEDIATION REQUIRED, and a blocking condition for C3+ in the PR's own QG-E6 report, yet shipped unremediated in both copies (SEC-008).
Disposition: FIX-NOW — the rules file is the declared SSOT; aligning the template, completion contract, and fail-closed conditional to it are determinate text corrections, including the exact remediation the QG-E6 report already prescribed.
Source findings consumed: P2-004, P2-003, S-002-01.
Affected files: `skills/nuclear-sop/templates/PROCEDURE_STATE.template.yaml`, `skills/nuclear-sop/agents/sop-executor.md`, `sop-capture.md`, `sop-verifier.md`, `skills/nuclear-sop/composition/sop-verifier.prompt.md` (+ executor/capture composition twins), `skills/nuclear-sop/behavioral-baselines/` (bb-002).

## Steps to Reproduce

1. On PR #269 head `bda64202`, compare IV-PENDING transitions in `rules/nuclear-sop-behavior-rules.md`/`PLAYBOOK.md` (→ IV-PASSED | IV-REJECTED) with the comments in `templates/PROCEDURE_STATE.template.yaml` (→ HELD on REJECT); note IV-REJECTED in the valid-status list with no transition, the outcome field allowing only PASS | DEVIATION vs bb-002's required WAIVED, and "Any state → RESUMING".
2. Read `agents/sop-executor.md` Phase 2 (sets status COMPLETED and execution_log_final to a path) against NS-H-06 and `agents/sop-capture.md` Step 1 (requires execution_log_final literally `true`, else HALT).
3. Read `agents/sop-verifier.md` Step 6 and `composition/sop-verifier.prompt.md`: the "if accessible" conditional silently skips the hold-point check when PROCEDURE_STATE.yaml is absent, with no anomaly recorded (SEC-008 in the PR's own QG-E6 report).

## Acceptance Criteria

- [ ] Template transitions aligned to the rules SSOT: IV-PENDING → IV-PASSED | IV-REJECTED (HELD only as the documented consequence after IV-REJECTED, per the rules); IV-REJECTED added to the transitions section; outcome comment reads `PASS | DEVIATION | WAIVED`; "Any state → RESUMING" replaced with the rules' enumerated predecessors.
- [ ] Completion contract fixed: the executor never sets COMPLETED (leaves IN-PROGRESS, sets `execution_log_final: <path>`); sop-capture Step 1 HALTs unless execution_log_final is set and resolves to an existing file; sop-capture Step 4 remains the sole writer of COMPLETED; template comments and composition twins match.
- [ ] sop-verifier Step 6 (both copies) fail-closed: absent/unreadable state file → record `ANOMALY: STATE-FILE-UNAVAILABLE` in the verification report, and the disposition MUST NOT be unconditional ACCEPT; SEC-008 status updated wherever tracked (see BUG-008/REM-08 item 4).
- [ ] Validation passes: every status in the template's valid-status list appears in ≥1 transition; bb-002 patterns re-run clean against the template; `grep -n "execution_log_final" skills/nuclear-sop/` shows path semantics only; `grep -n "if accessible"` in both sop-verifier copies → 0 hits.
- [ ] Fix commit pushed to proj-0039-nuclear-engineer and referenced here.
- [ ] PR #269 CI green at post-fix head.

## Related Items

- Remediation register (REM-12): [remediation-register.md](../EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-004-remediation/remediation-register.md#rem-12-state-machine-and-completion-contract-reconciliation)
- Parent story: [STORY-004](../EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-004-remediation/STORY-004-remediation.md)
- GitHub Issue: [#361](https://github.com/geekatron/jerry/issues/361)
