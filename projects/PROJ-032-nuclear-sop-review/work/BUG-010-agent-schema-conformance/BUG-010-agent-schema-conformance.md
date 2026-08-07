# BUG-010: Agent definition schema and standards conformance [REM-10]

> **Type:** bug
> **Status:** completed
> **Priority:** critical
> **Impact:** high
> **Severity:** critical
> **Created:** 2026-08-07T11:30:00Z
> **Completed:** 2026-08-07T13:30:00Z
> **Found In:** PR #269 head bda64202 (branch proj-0039-nuclear-engineer)
> **GitHub Issue:** [#359](https://github.com/geekatron/jerry/issues/359)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Defect, disposition, findings consumed, affected files |
| [Steps to Reproduce](#steps-to-reproduce) | How to observe the defect concretely |
| [Acceptance Criteria](#acceptance-criteria) | Observable outcomes of the fix |
| [Related Items](#related-items) | Register, parent story, GitHub issue |

## Summary

Deterministic validator failures and standards-conformance defects across all four agents: `composition/sop-verifier.agent.yaml` is unparseable YAML (unquoted ": " in the line-9 description scalar → ScannerError); `sop-brief.governance.yaml` fails agent-governance-v1 with 4 errors (dict-style post_completion_checks where the schema requires strings); `sop-verifier.governance.yaml` fails with 2 (output.required true without location per AR-010, prose output.levels matching neither schema branch); `composition/sop-brief.agent.yaml` fails with 5.
Additional conformance defects: section-numbering contradictions vs the skill's own template (sections 4/5/9), missing AD-M-011 output-location declarations in all four agents (`{execution_dir}` never defined), hexagonal dependency-rule violations (concrete tool names and literal Glob()/Grep()/Read() syntax in domain-layer sections), and sop-executor's missing reasoning_effort despite quality_gate_tier C3 (ET-M-001).
Disposition: FIX-NOW — deterministic failures with exact known corrections; the compliant corpus (66 governance files, reference agents) defines the target form, and H-34's consequence is rejection at CI.
Source findings consumed: P1-003, P1-004, P2-018, P1-005, S-010-01, P1-007, P1-012, P1-013, P1-014, P1-021.
Affected files: `skills/nuclear-sop/agents/sop-brief.governance.yaml`, `sop-verifier.governance.yaml`, `sop-executor.governance.yaml`, `sop-capture.governance.yaml`, `agents/sop-brief.md`, `sop-verifier.md`, `sop-capture.md`, `sop-executor.md`, `composition/sop-verifier.agent.yaml`, `composition/sop-brief.agent.yaml`.

## Steps to Reproduce

1. On PR #269 head `bda64202`, run `uv run python -c "import yaml; yaml.safe_load(open('skills/nuclear-sop/composition/sop-verifier.agent.yaml'))"` → ScannerError from the unquoted ": " in the line-9 description.
2. Validate the four governance files against the schema, e.g. `uv run jsonschema -i skills/nuclear-sop/agents/sop-brief.governance.yaml docs/schemas/agent-governance-v1.schema.json` (via the repo validator): sop-brief reports 4 errors, sop-verifier 2, `composition/sop-brief.agent.yaml` 5 against its declared canonical schema.
3. Grep for `Glob(\|Grep(\|Read(` inside `<identity>`/`<purpose>`/`<methodology>`/`<guardrails>` of `skills/nuclear-sop/agents/sop-*.md` → hits violating the hexagonal dependency rule; confirm `sop-executor.governance.yaml` declares quality_gate_tier C3 with no reasoning_effort field.

## Acceptance Criteria

- [x] `composition/sop-verifier.agent.yaml` parses (block-scalar or quoted description) and output.levels uses `[L0, L1, L2]`; the same levels fix mirrored in `sop-verifier.governance.yaml`. (verified 2026-08-07)
- [x] post_completion_checks entries rewritten as plain strings in `sop-brief.governance.yaml` and `composition/sop-brief.agent.yaml`; on_send line 92 quoted. (verified 2026-08-07)
- [x] `sop-verifier.governance.yaml` sets `output.required: false`; sop-brief section-numbering corrected (.md Step 1.6, purpose, identity + domain_extensions A-3 of both YAMLs): sections 4/5/9 validated, 7-8 assigned to sop-executor. (verified 2026-08-07)
- [x] AD-M-011 output declarations added: sop-brief `projects/${JERRY_PROJECT}/`-anchored location + filename_pattern; `{execution_dir}` defined once in SKILL.md/rules and referenced by sop-executor; sop-capture's two explicit paths with documented MEDIUM-tier override justification; sop-verifier declares none. (verified 2026-08-07)
- [x] Domain-layer sections reworded to capability language with tool syntax relocated to `<capabilities>`; `reasoning_effort: high` added to sop-executor.governance.yaml, the other three set or documented per ET-M-001. (verified 2026-08-07)
- [x] Validation passes: 0 schema errors for all four governance files; yaml.safe_load succeeds on all four composition agent.yaml files; tool-name grep in domain sections → 0 hits. (verified 2026-08-07)
- [x] Fix commit pushed to proj-0039-nuclear-engineer and referenced here. — commit c07033ce
- [x] PR #269 CI green at post-fix head. — 15/15, run 31174766440

## Related Items

- Remediation register (REM-10): [remediation-register.md](../EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-004-remediation/remediation-register.md#rem-10-agent-definition-schema-and-standards-conformance)
- Parent story: [STORY-004](../EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-004-remediation/STORY-004-remediation.md)
- GitHub Issue: [#359](https://github.com/geekatron/jerry/issues/359)
