# TASK-033: Phase 5A — Update Guardrails Template to NPT-009 Format

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-02-28
> **Parent:** FEAT-002
> **Owner:** —
> **Activity:** IMPLEMENTATION

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description |
| [Content](#content) | Description and acceptance criteria |
| [Evidence](#evidence) | Deliverables and verification |
| [History](#history) | Status changes |

---

## Summary

Update the guardrails template minimum example in agent-development-standards.md from NPT-014 (bare prohibition) to NPT-009 (structured negation with consequence). Add VIOLATION label format guidance and tier-differentiated consequence guidance for T2+ agents.

---

## Content

### Description

ADR-002 Sub-Decision 1 (D-001, REC-F-001 through REC-F-003). The current guardrails template in agent-development-standards.md uses NPT-014 format for the forbidden_actions minimum example. Update to NPT-009 format with VIOLATION labels and consequence text. Add tier-differentiated guidance so T2+ agents include more specific consequence documentation. This is an immediate Phase 5A change that does not depend on A/B testing results.

### Acceptance Criteria

- [ ] Guardrails template minimum example updated from NPT-014 to NPT-009 format
- [ ] VIOLATION label format added (e.g., `{TYPE} VIOLATION: NEVER {action} -- Consequence: {impact}`)
- [ ] Tier-differentiated consequence guidance added for T2+ agents
- [ ] Existing agents not invalidated by template change (template is illustrative, not schema-enforced)

### Related Items

- Parent: [FEAT-002: Implement ADR-002](./FEAT-002-implement-adr-002-constitutional-upgrades.md)
- References: ADR-002 Sub-Decision 1 (D-001)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Updated agent-development-standards.md | Rule file modification | `.context/rules/agent-development-standards.md` |

### Verification

- [ ] Acceptance criteria verified

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-28 | Created | Initial creation |
