# TASK-007: red-team path remediation

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-03-31
> **Parent:** BUG-006
> **ADR:** [ADR-EPIC002-001](../../../docs/design/ADR-EPIC002-001-unified-output-path-resolution.md)

---

## Summary

Implement the Unified Output Path Resolution Protocol (ADR-EPIC002-001) across 25 red-team config files. Each file type requires different changes per the ADR migration guide.

## Changes Per File Category

| Category | Count | ADR Step | Changes Required |
|----------|-------|----------|-----------------|
| Agent governance YAML | 11 | Step 1 | Replace `output.location` with project-relative template; add `output.filename_pattern` field |
| Agent .md definitions | 11 | Step 2 | Add Output Path Resolution section to `<output>` block documenting P1/P2/P3/P4 chain |
| SKILL.md | 1 | Step 3 | Replace agent table output column (lines 106-116); update examples (lines 188, 274, 521-528, 535) |
| Templates | 2 | Step 4 | Replace `engagement-playbook.md` (line 81) and `pentest-engagement.md` (line 151, 189-192) |

**Line-level audit:** [BUG-006-red-audit-detail.md](../research/BUG-006-red-audit-detail.md)

## Governance YAML Changes (Step 1)

**Before:**
```yaml
output:
  location: "skills/red-team/output/{engagement-id}/red-recon-{topic-slug}.md"
```

**After:**
```yaml
output:
  location: "projects/${JERRY_PROJECT}/engagements/{engagement-id}/red-recon-{topic-slug}.md"
  filename_pattern: "red-recon-{topic-slug}.md"
```

## Acceptance Criteria

- [ ] Zero `grep -r 'skills/red-team/output' skills/red-team/` matches
- [ ] All 11 governance YAML files have `output.filename_pattern` field
- [ ] All 11 agent .md files have Output Path Resolution section
- [ ] SKILL.md agent table and examples use `projects/${JERRY_PROJECT}/engagements/` pattern
- [ ] All governance YAML files pass schema validation (requires TASK-015 schema update first)
- [ ] Both template files updated per ADR Step 4
