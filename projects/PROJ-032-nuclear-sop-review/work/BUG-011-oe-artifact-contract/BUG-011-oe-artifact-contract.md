# BUG-011: OE artifact contract alignment [REM-11]

> **Type:** bug
> **Status:** in_progress
> **Priority:** critical
> **Impact:** high
> **Severity:** critical
> **Created:** 2026-08-07T11:30:00Z
> **Found In:** PR #269 head bda64202 (branch proj-0039-nuclear-engineer)
> **GitHub Issue:** [#360](https://github.com/geekatron/jerry/issues/360)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Defect, disposition, findings consumed, affected files |
| [Steps to Reproduce](#steps-to-reproduce) | How to observe the defect concretely |
| [Acceptance Criteria](#acceptance-criteria) | Observable outcomes of the fix |
| [Related Items](#related-items) | Register, parent story, GitHub issue |

## Summary

The OE entry extension contradiction silently zeroes the feedback loop the skill names as its key capability: the authoritative chain writes and searches `docs/experience/{entry_id}.yaml` (rules, sop-capture, sop-brief Glob — 29 refs) while POST_JOB_BRIEF.template.md (lines 127-129), bb-003 (line 112, B-21/B-24), and the example (AC-7, Section 11, lines 480/518) use `.md` — entries written per the .md artifacts are permanently invisible to retrieval, and AC-7 is literally unsatisfiable (false-failing the QG-E4 fixture and bb-003).
The retrieval protocol also drifts across three variants (rules: workflow_id primary; sop-brief Step 4: workflow_type-only Glob; bb-003 B-24: a third form), and Section 11 "Attachments" is documented as "runtime-written by sop-capture" in three places while sop-capture's methodology never opens or edits the workflow definition.
Disposition: FIX-NOW — text corrections toward the unambiguous authoritative convention (`.yaml`, workflow_id-primary) already defined by the rules file and followed by the write path; the missing Section 11 step implements behavior three shipped documents already promise.
Source findings consumed: P1-015, S-002-05, S-003-01, S-004-05, S-007-02, S-010-03, S-011-05, S-012-06, S-013-04, P2-008, S-010-04.
Affected files: `skills/nuclear-sop/templates/POST_JOB_BRIEF.template.md`, `skills/nuclear-sop/behavioral-baselines/bb-003-oe-feedback-loop-integrity.md`, `skills/nuclear-sop/examples/c3-adr-workflow-definition.md`, `skills/nuclear-sop/agents/sop-brief.md`, `skills/nuclear-sop/agents/sop-capture.md` (+ governance/composition parity).

## Steps to Reproduce

1. On PR #269 head `bda64202`, run `grep -rn "experience/" skills/nuclear-sop/`: the rules file, sop-capture, and sop-brief reference `docs/experience/{entry_id}.yaml` while `templates/POST_JOB_BRIEF.template.md` lines 127-129, bb-003 line 112 and B-21/B-24, and the example lines 480/518 plus AC-7 use `.md`.
2. Read `agents/sop-brief.md` Step 4 (workflow_type-only Glob) against the rules' workflow_id-primary protocol and bb-003 B-24's third variant: three incompatible retrieval procedures.
3. Read the Section 11 "Attachments" promise in the template, example, and tutorial Step 4, then read `agents/sop-capture.md`'s methodology: no step opens or edits the workflow definition.

## Acceptance Criteria

- [ ] `templates/POST_JOB_BRIEF.template.md` lines 127-129 use `.yaml` for both paths (`capture/oe-entry-{entry_id}.yaml`, `docs/experience/{entry_id}.yaml`).
- [ ] bb-003 globs `docs/experience/*.yaml` (line 112, B-21/B-24), with B-24's retrieval rewritten to the rules' protocol (Glob `*.yaml`, then filter by workflow_id).
- [ ] Example glob patterns (lines 480/518), AC-7 (`docs/experience/adr-authoring-c3-001-*.yaml`), and the Section 11 reference all use `.yaml`.
- [ ] `agents/sop-brief.md` Step 4 uses the workflow_id-primary search protocol (workflow_type as post-read filter); composition twins mirrored.
- [ ] `agents/sop-capture.md` gains the explicit Section 11 append step (after OE write, before status COMPLETED) plus the matching output-artifacts row, mirrored in governance post_completion_checks and composition twins.
- [ ] Validation passes: `grep -rn "experience/.*\.md\|oe-entry-.*\.md" skills/nuclear-sop/` → 0 hits; bb-003 checks executable against a sample `.yaml` entry; AC-7 glob matches sop-capture's declared write path; sop-brief and rules describe the identical search protocol.
- [ ] Fix commit pushed to proj-0039-nuclear-engineer and referenced here.
- [ ] PR #269 CI green at post-fix head.

## Related Items

- Remediation register (REM-11): [remediation-register.md](../EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-004-remediation/remediation-register.md#rem-11-oe-artifact-contract-alignment)
- Parent story: [STORY-004](../EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-004-remediation/STORY-004-remediation.md)
- GitHub Issue: [#360](https://github.com/geekatron/jerry/issues/360)
