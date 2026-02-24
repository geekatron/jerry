# TASK-020: Update mandatory-skill-usage.md trigger map

> **Type:** task
> **Status:** pending
> **Priority:** medium
> **Impact:** high
> **Criticality:** C3 (AE-002)
> **Created:** 2026-02-21T23:59:00Z
> **Parent:** EN-001
> **Owner:** --
> **Effort:** 1
> **Activity:** documentation

---

## Summary

Update the mandatory-skill-usage.md trigger map with agent-related keywords for routing.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Description](#description) | What this task requires |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Implementation Notes](#implementation-notes) | Technical approach and constraints |
| [Related Items](#related-items) | Parent and related work |
| [History](#history) | Status changes |

---

## Description

Add agent-related keywords to the Trigger Map in `.context/rules/mandatory-skill-usage.md` so that questions about agent development, agent routing, and skill routing are directed to the correct skills and rules. This operationalizes the routing decisions captured in ADR-PROJ007-002.

**AE-002 applies:** This task touches `.context/rules/` — auto-C3 minimum criticality. `mandatory-skill-usage.md` is auto-loaded at session start and governs proactive skill invocation (H-22).

### Keywords to Add

Based on ADR-PROJ007-002 and the installed routing standards, add triggers for:
- Agent development keywords: `agent definition, agent design, agent standards, define agent, create agent, agent frontmatter`
- Agent routing keywords: `skill routing, agent routing, routing hop, routing trigger, route to skill, which skill`
- Pattern taxonomy keywords: `agent pattern, pattern catalog, agent taxonomy`

### Steps

1. Read `.context/rules/mandatory-skill-usage.md` Trigger Map section
2. Add agent development keywords row pointing to `agent-development-standards.md` (and `/nasa-se` for design tasks)
3. Add agent routing keywords row pointing to `agent-routing-standards.md` (and `/orchestration` for pipeline questions)
4. Verify no duplicate or conflicting entries with existing trigger rows
5. Verify the updated trigger map does not break existing routing behavior

---

## Acceptance Criteria

- [ ] AC-1: Trigger Map includes agent development keywords with correct skill/rule routing
- [ ] AC-2: Trigger Map includes agent routing keywords with correct skill/rule routing
- [ ] AC-3: No duplicate or conflicting entries introduced
- [ ] AC-4: Existing trigger map rows are unchanged (no regressions)

---

## Implementation Notes

### Files to Modify

| File | Change |
|------|--------|
| `.context/rules/mandatory-skill-usage.md` | Add agent-related keyword rows to Trigger Map table |

### Trigger Map Row Format

Follow existing format in the trigger map table:
```
| detected keywords | skill |
```

Example:
```
| agent definition, agent design, define agent, create agent, agent frontmatter | agent-development-standards.md |
| skill routing, agent routing, routing hop, route to skill | agent-routing-standards.md |
```

### AE-002 Note

Touching `.context/rules/mandatory-skill-usage.md` is auto-C3. Self-review (S-010) required before marking done.

### Dependency

TASK-013 (install agent-routing-standards) should complete first so the routing target exists. TASK-015 (install ADR-PROJ007-002) provides the authoritative routing decisions.

---

## Related Items

- **Parent:** [EN-001](../EN-001.md)
- **AE-002:** Touches `.context/rules/mandatory-skill-usage.md` — auto-C3 minimum
- **Depends on:** TASK-013 (agent-routing-standards), TASK-015 (ADR-PROJ007-002)
- **Implements:** ADR-PROJ007-002 routing decisions in operational trigger map

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-21 | pending | Created — depends on TASK-013 and TASK-015 completing first |
