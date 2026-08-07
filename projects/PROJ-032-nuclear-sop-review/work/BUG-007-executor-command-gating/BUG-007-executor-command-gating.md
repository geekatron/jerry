# BUG-007: Executor command gating and injection screening [REM-07]

> **Type:** bug
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Severity:** major
> **Created:** 2026-08-07T11:30:00Z
> **Found In:** PR #269 head bda64202 (branch proj-0039-nuclear-engineer)
> **GitHub Issue:** [#356](https://github.com/geekatron/jerry/issues/356)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Defect, disposition, findings consumed, affected files |
| [Steps to Reproduce](#steps-to-reproduce) | How to observe the defect concretely |
| [Acceptance Criteria](#acceptance-criteria) | Conditions required to close this bug |
| [Related Items](#related-items) | Register, parent story, GitHub issue |

## Summary

The executor's Bash guard is a static substring denylist (curl, wget, ssh, scp, git push, sudo, chmod 777, rm -rf /) with no principle-based catch-all: nc/ncat, `python -m http.server`, base64 exfiltration, `chmod -R 777 path`, `rm -rf ./dir`, and package-manager code execution all pass without [USER-HOLD], and H-05 (uv-only Python) is never surfaced.
SEC-001 injection screening covers only WARNING/CAUTION annotation content while Action, Target, Expected Result, Sign-off Criterion, Hold Reason, and Sections 2/3/9 prose are equally attacker-controlled and directly drive tool calls; detected payloads are echoed verbatim into the execution log sop-capture later reads (a second-order injection channel), and PLAYBOOK overstates machine-side coverage by naming SEC-001/002 "the primary mitigations" when SR-06 human review is the actual primary control.
The whole construct is a bespoke, weaker prompt-level copy of the repo's deterministic SecurityEnforcementEngine (82 tests) with no integration or reference; sop-brief and sop-capture also hold full Bash for needs other tools already cover.
Disposition: DEFER-REWORK — choosing the gating model and the injection-screening scope are security-architecture decisions; a maintainer bolting more substrings onto the denylist would reproduce the exact anti-pattern the findings identify.
Source findings consumed: P2-026, S-001-06, S-013-08, P2-027, S-004-12.
Affected files: `skills/nuclear-sop/agents/sop-executor.md`, `skills/nuclear-sop/agents/sop-brief.md`, `skills/nuclear-sop/agents/sop-capture.md`, `skills/nuclear-sop/PLAYBOOK.md`, `skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md`.

## Steps to Reproduce

1. On PR #269 head `bda64202`, read the Bash guard in `skills/nuclear-sop/agents/sop-executor.md` and test candidate commands (`nc`, `python -m http.server`, `chmod -R 777 ./x`, `rm -rf ./dir`) against the denylist: none match, so none would trigger [USER-HOLD].
2. Read SEC-001's declared scope: only WARNING/CAUTION annotation content is screened, while the other definition-sourced fields that drive tool calls are unscreened; on detection, the executor logs the payload verbatim.
3. Read the Bash grants in `agents/sop-brief.md` and `agents/sop-capture.md` against their declared needs (read-only interrogation, timestamps, file counts): other granted tools already cover them; the read-only restriction is prose only.
4. Compare with the repo's deterministic SecurityEnforcementEngine (82 tests): the skill neither integrates with nor references it.

## Acceptance Criteria

- [ ] Contributor redesign answers the register's REM-07 redesign question:
  - A specified command-gating model (allowlist per agent, category-based gating with mandatory [USER-HOLD], and/or delegation to the SecurityEnforcementEngine).
  - Injection-screening scope defined across all definition-sourced fields that drive tool calls (or the narrower scope justified); payload echo into logs neutralized (hash/excerpt); H-05 surfaced in executor constraints; sop-brief/sop-capture Bash grants dropped or narrowed; PLAYBOOK's mitigation hierarchy corrected to name SR-06 human review as primary.
- [ ] Re-review passes before merge.

Both criteria remain unchecked by design; this bug stays open until contributor rework lands and is re-reviewed.

## Related Items

- Remediation register (REM-07): [remediation-register.md](../EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-004-remediation/remediation-register.md#rem-07-executor-command-gating-and-injection-screening)
- Parent story: [STORY-004](../EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-004-remediation/STORY-004-remediation.md)
- GitHub Issue: [#356](https://github.com/geekatron/jerry/issues/356)
