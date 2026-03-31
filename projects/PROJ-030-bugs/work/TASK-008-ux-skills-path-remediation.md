# TASK-008: UX skills path remediation — 11 sub-skills

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-03-31
> **Parent:** BUG-006
> **ADR:** [ADR-EPIC002-001](../../../docs/design/ADR-EPIC002-001-unified-output-path-resolution.md)

---

## Summary

Implement the Unified Output Path Resolution Protocol (ADR-EPIC002-001) across 60 config files in 11 UX sub-skills. Each file type requires different changes per the ADR migration guide.

**Full line-level audit:** [BUG-006-ux-audit-detail.md](../research/BUG-006-ux-audit-detail.md)

## Changes Per File Category

| Category | Count | ADR Step | Changes Required |
|----------|-------|----------|-----------------|
| Agent governance YAML | 11 | Step 1 | Replace `output.location`; add `output.filename_pattern` |
| Agent .md definitions | 11 | Step 2 | Add Output Path Resolution section to `<output>` block |
| SKILL.md | 11 | Step 3 | Replace agent table output column and examples |
| Templates | 12 | Step 4 | Replace `artifact_path` references |
| Rules | 15 | Step 3 | Replace output path refs in routing, wave-progression, CI checks, MCP runbooks, methodology rules |

## Files Per Sub-Skill

| Sub-Skill | Files |
|-----------|-------|
| user-experience (parent) | 7 |
| ux-heuristic-eval | 5 |
| ux-jtbd | 5 |
| ux-lean-ux | 7 |
| ux-heart-metrics | 3 |
| ux-kano-model | 6 |
| ux-atomic-design | 6 |
| ux-inclusive-design | 7 |
| ux-behavior-design | 5 |
| ux-design-sprint | 4 |
| ux-ai-first-design | 5 |
| **Total** | **60** |

## Key UX-Specific Concerns

- **UX orchestrator routing rules** (`skills/user-experience/rules/ux-routing-rules.md`) reference sub-skill output paths for wave signoff files — these must use the new pattern
- **Wave progression rules** (`skills/user-experience/rules/wave-progression.md`) reference signoff file paths
- **CI checks** (`skills/user-experience/rules/ci-checks.md`) validate output paths — must match new convention
- **Engagement ID pattern** (`UX-{NNNN}`) must be preserved in the new path structure

## Acceptance Criteria

- [ ] Zero `grep -rl 'skills/ux-.*output\|skills/user-experience.*output' skills/ux-*/ skills/user-experience/` matches
- [ ] All 11 governance YAML files have `output.filename_pattern` field
- [ ] All 11 agent .md files have Output Path Resolution section
- [ ] All 11 SKILL.md files use `projects/${JERRY_PROJECT}/engagements/` pattern
- [ ] Wave signoff paths updated in routing and wave-progression rules
- [ ] CI check rules updated to validate new path pattern
- [ ] All governance YAML files pass schema validation (requires TASK-015 schema update first)
