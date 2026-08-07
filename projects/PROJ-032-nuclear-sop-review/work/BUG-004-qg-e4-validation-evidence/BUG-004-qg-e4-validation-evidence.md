# BUG-004: QG-E4 validation evidence [REM-04]

> **Type:** bug
> **Status:** pending
> **Priority:** critical
> **Impact:** high
> **Severity:** critical
> **Created:** 2026-08-07T11:30:00Z
> **Found In:** PR #269 head bda64202 (branch proj-0039-nuclear-engineer)
> **GitHub Issue:** [#353](https://github.com/geekatron/jerry/issues/353)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Defect, disposition, findings consumed, affected files |
| [Steps to Reproduce](#steps-to-reproduce) | How to observe the defect concretely |
| [Acceptance Criteria](#acceptance-criteria) | Conditions required to close this bug |
| [Related Items](#related-items) | Register, parent story, GitHub issue |

## Summary

The "3/3 catch rate (100%), empirically validated" claim that lifted the C3+ restriction rests on a self-authored simulation walkthrough of a fixture that embeds its own answer key: each trap step carries a "TEST HARNESS — TRAP-NN EXPECTED STAR RESPONSE" block in the same file sop-executor loads into context at Phase 0, so the test measures repetition of nearby context, not blind deviation detection.
The evidence is further compromised by N=3 against a self-defined >=60% bar, an internally contradictory TRAP-01 (WARNING path vs ERROR TRAP/Target path), a literally unsatisfiable AC-7 (globs `.md`, capture writes `.yaml`), the sole evidence artifact living outside the shipped package, stale/contradictory gate status text, and five SD-* security-design decisions (SD-06/11/13/15/17) cited but never defined.
Disposition: DEFER-REWORK — a maintainer cannot manufacture evidence; re-validation is contributor work (interim text withdrawal of the C3+ claim is handled by BUG-008/REM-08).
Source findings consumed: S-001-02, S-011-04, S-002-03, S-011-03, S-004-07, S-012-09, S-002-04, CC-8, P2-006, S-012-11, S-012-12.
Affected files: `skills/nuclear-sop/examples/c3-adr-workflow-definition.md`, `skills/nuclear-sop/SKILL.md`, `skills/nuclear-sop/PLAYBOOK.md`, `skills/nuclear-sop/agents/sop-executor.governance.yaml`, plus star-validation-results.md and skill-integration-analysis.md under «PR projects tree»/PROJ-0039-nuclear-engineer.

## Steps to Reproduce

1. On PR #269 head `bda64202`, read `skills/nuclear-sop/examples/c3-adr-workflow-definition.md`: each trap step embeds a "TEST HARNESS — TRAP-NN EXPECTED STAR RESPONSE" block with the fully worked expected reasoning.
2. Compare TRAP-01's WARNING text (line 235, `projects/{JERRY_PROJECT}/decisions/ADR-NNN.md`) with its ERROR TRAP callout (line 242) and Target field (line 249, `docs/design/ADR-NNN.md`): the fixture contradicts itself about its own trap.
3. Read star-validation-results.md under «PR projects tree»/PROJ-0039-nuclear-engineer (outside the shipped `skills/nuclear-sop/` package): its own footer says "Empirical simulation — STAR walkthrough", authored by the same engineer who designed the traps; no live sop-executor invocation, transcript, or independent tester exists.
4. Check the fixture's AC-7: it globs `.md` while capture writes `.yaml` — unsatisfiable, so "3/3" cannot describe full acceptance-criteria coverage.

## Acceptance Criteria

- [ ] Contributor redesign answers the register's REM-04 redesign question — validation evidence that survives independent review:
  - Blind fixtures (answer-key blocks stripped, TRAP-01 contradiction fixed); actually-executed runs with transcripts/tool-call logs from live sop-executor invocations; independent trap authorship and scoring.
  - An N and pass bar with statistical footing; full acceptance-criteria coverage (including AC-7 after REM-11); evidence shipped inside or resolvably cited from the package; a shipped SD-01..18 security-design-decision register.
- [ ] Re-review passes before merge (C3+ approval claims remain withdrawn until then).

Both criteria remain unchecked by design; this bug stays open until contributor rework lands and is re-reviewed.

## Related Items

- Remediation register (REM-04): [remediation-register.md](../EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-004-remediation/remediation-register.md#rem-04-qg-e4-validation-evidence)
- Parent story: [STORY-004](../EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-004-remediation/STORY-004-remediation.md)
- GitHub Issue: [#353](https://github.com/geekatron/jerry/issues/353)
