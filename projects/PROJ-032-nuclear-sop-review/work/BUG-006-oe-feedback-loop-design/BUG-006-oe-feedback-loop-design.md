# BUG-006: OE feedback-loop design [REM-06]

> **Type:** bug
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Severity:** major
> **Created:** 2026-08-07T11:30:00Z
> **Found In:** PR #269 head bda64202 (branch proj-0039-nuclear-engineer)
> **GitHub Issue:** [#355](https://github.com/geekatron/jerry/issues/355)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Defect, disposition, findings consumed, affected files |
| [Steps to Reproduce](#steps-to-reproduce) | How to observe the defect concretely |
| [Acceptance Criteria](#acceptance-criteria) | Conditions required to close this bug |
| [Related Items](#related-items) | Register, parent story, GitHub issue |

## Summary

The OE feedback loop cannot function as designed: `entry_type: synthesis` is not in the 18-field mandatory OE schema and sop-capture's all-fields-non-empty write-block rejects any entry lacking per-execution fields, while three files assign synthesis ownership three contradictory ways (sop-brief → sop-capture; PLAYBOOK → ps-synthesizer; NS-M-06 → a section in normal entries).
Because the accumulation threshold is keyed per workflow_type, 21 unsynthesized NOMINAL entries STOP every NOMINAL execution repo-wide — and since synthesis entries cannot be produced, the count monotonically approaches that STOP.
The OE corpus is also a cross-criticality persistence/injection channel (any C1 execution or direct repo write plants entries that all future same-type briefs, including C4, must load as MANDATORY CONTEXT) with SEC-002 guard labels on only 2 of the interpolated fields; and there is no retention/archival policy, so routine work/ cleanup makes every legitimate entry permanently [PROVENANCE-UNVERIFIED].
Disposition: DEFER-REWORK — requires schema design, threshold-policy design, and a trust/retention model for the corpus; these are decisions about how the skill's flagship feedback loop works.
Source findings consumed: P2-007, P2-025, S-013-07.
Affected files: `skills/nuclear-sop/agents/sop-brief.md`, `skills/nuclear-sop/agents/sop-capture.md`, `skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md`, `skills/nuclear-sop/PLAYBOOK.md`, `skills/nuclear-sop/behavioral-baselines/bb-003-oe-feedback-loop-integrity.md`.

## Steps to Reproduce

1. On PR #269 head `bda64202`, read the 18-field mandatory OE schema in `skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md`: `entry_type: synthesis` is not a permitted value, and sop-capture's write-block rejects entries lacking per-execution fields.
2. Compare synthesis ownership across `agents/sop-brief.md`, `PLAYBOOK.md`, and NS-M-06 in the rules file: three different owners are named.
3. Read the accumulation-threshold rule: it is keyed per workflow_type (3 values), so 21 unsynthesized NOMINAL entries STOP every NOMINAL execution repo-wide, with no way to reset the counter.
4. Read SEC-002 and bb-003: guard labels cover 2 interpolated fields; the SR-03 provenance cross-reference is forgeable (both artifacts unauthenticated); bb-003 tests one field.

## Acceptance Criteria

- [ ] Contributor redesign answers the register's REM-06 redesign question — the OE lifecycle end-to-end:
  - A synthesis artifact type sop-capture can actually write; exactly one synthesis owner; threshold scoping that cannot deadlock unrelated executions.
  - A provenance mechanism that survives work/ cleanup (or an archival rule); an injection trust model for the corpus (guard labels on every interpolated field, or explicit acceptance of residual risk given C1-writes-feed-C4-briefs).
- [ ] Re-review passes before merge.

Both criteria remain unchecked by design; this bug stays open until contributor rework lands and is re-reviewed.

## Related Items

- Remediation register (REM-06): [remediation-register.md](../EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-004-remediation/remediation-register.md#rem-06-oe-feedback-loop-design)
- Parent story: [STORY-004](../EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-004-remediation/STORY-004-remediation.md)
- GitHub Issue: [#355](https://github.com/geekatron/jerry/issues/355)
