# TASK-010: Add output path MEDIUM standard to agent-development-standards.md

> **Type:** task
> **Status:** pending
> **Priority:** medium
> **Created:** 2026-03-31
> **Parent:** BUG-006
> **Depends On:** TASK-006, TASK-007, TASK-008
> **ADR:** [ADR-EPIC002-001](../../../docs/design/ADR-EPIC002-001-unified-output-path-resolution.md)

---

## Summary

Add AD-M-011 to `.context/rules/agent-development-standards.md` Agent Structure Standards table, codifying the Unified Output Path Resolution Protocol as a MEDIUM standard. The ADR provides the draft text (Step 5).

## Standard Text (from ADR)

Insert after AD-M-010 in the Agent Structure Standards table:

```markdown
| AD-M-011 | Agent output paths SHOULD follow the Unified Output Path Resolution Protocol (ADR-EPIC002-001). Agents SHOULD declare `output.location` as a project-relative default template using `projects/${JERRY_PROJECT}/` prefix, and SHOULD declare `output.filename_pattern` for base-path resolution. Agents SHOULD accept caller-provided explicit paths (Priority 1) or base paths (Priority 2) that override the default template. Agents SHOULD NOT hardcode output paths to `skills/*/output/` or any other skill-internal directory. Override requires documented justification per MEDIUM tier vocabulary. | Ensures agents work correctly in orchestration, worktracker, engagement, and standalone contexts. Prevents the skill-internal output path anti-pattern (BUG-006/GH #230). Reference architecture: `/problem-solving` agents. | ADR-EPIC002-001, BUG-006 |
```

## Acceptance Criteria

- [ ] AD-M-011 exists in agent-development-standards.md Agent Structure Standards table
- [ ] Uses SHOULD/SHOULD NOT language (MEDIUM tier, not HARD)
- [ ] References ADR-EPIC002-001 and `/problem-solving` as reference architecture
- [ ] AE-002 auto-escalation acknowledged (touches `.context/rules/`)
