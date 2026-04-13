# TASK-006: eng-team path remediation

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-03-31
> **Parent:** BUG-006
> **ADR:** [ADR-output-path-resolution-001](../../../docs/design/ADR-output-path-resolution-001.md)

---

## Summary

Implement the Unified Output Path Resolution Protocol (ADR-output-path-resolution-001) across 22 eng-team config files. This is not a simple path replacement — each file type requires different changes per the ADR migration guide.

## Changes Per File Category

| Category | Count | ADR Step | Changes Required |
|----------|-------|----------|-----------------|
| Agent governance YAML | 10 | Step 1 | Replace `output.location` with project-relative template; add `output.filename_pattern` field |
| Agent .md definitions | 10 | Step 2 | Add Output Path Resolution section to `<output>` block documenting P1/P2/P3/P4 chain |
| SKILL.md | 1 | Step 3 | Replace agent table output column; update P-002 section and examples |
| Templates | 1 | Step 4 | Replace `engagement-playbook.md` directory creation instruction |

**Line-level audit:** [BUG-006-eng-audit-detail.md](../research/BUG-006-eng-audit-detail.md)

## Governance YAML Changes (Step 1)

**Before:**
```yaml
output:
  location: "skills/eng-team/output/{engagement-id}/eng-architect-{topic-slug}.md"
```

**After:**
```yaml
output:
  location: "projects/${JERRY_PROJECT}/engagements/{engagement-id}/eng-architect-{topic-slug}.md"
  filename_pattern: "eng-architect-{topic-slug}.md"
```

## Agent Definition Changes (Step 2)

Add to each agent's `<output>` block:
```markdown
### Output Path Resolution

This agent follows the Unified Output Path Resolution Protocol (ADR-output-path-resolution-001):

1. **Explicit path** — If the caller provides a path in the P-002 block, write there
2. **Base path** — If the caller provides `OUTPUT CONTEXT.base_path`, append filename
3. **Project default** — `projects/${JERRY_PROJECT}/engagements/{engagement-id}/eng-{agent}-{topic-slug}.md`
4. **Fallback** — `work/eng-{agent}-{topic-slug}.md` with warning
```

## Acceptance Criteria

- [ ] Zero `grep -r 'skills/eng-team/output' skills/eng-team/` matches
- [ ] All 10 governance YAML files have `output.filename_pattern` field
- [ ] All 10 agent .md files have Output Path Resolution section
- [ ] SKILL.md agent table uses `projects/${JERRY_PROJECT}/engagements/` pattern
- [ ] All governance YAML files pass schema validation (requires TASK-015 schema update first)
- [ ] Engagement playbook updated per ADR Step 4
