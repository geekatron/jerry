# TASK-034: Phase 5A — Add forbidden_action_format Field to Governance Schema

> **Type:** task
> **Status:** completed
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

Add an optional `forbidden_action_format` enum field to the agent governance schema (`agent-governance-v1.schema.json`) and a schema description field recommendation for forbidden_actions format. Provides upgrade-path visibility for the 30+ agent migration.

---

## Content

### Description

ADR-002 Sub-Decision 2 (D-003, REC-YAML-001) and Sub-Decision 3 (D-006, REC-YAML-002). Add an optional `forbidden_action_format` enum field with values `NPT-009-complete`, `NPT-009-partial`, `NPT-014` to the governance schema. Also add a pattern recommendation to the schema `$comment` or description field for `forbidden_actions` items. Both are additive changes that do not break existing agent file validation. This is an immediate Phase 5A change.

### Acceptance Criteria

- [ ] `forbidden_action_format` enum field added to `agent-governance-v1.schema.json` as optional
- [ ] Enum values: `NPT-009-complete`, `NPT-009-partial`, `NPT-014`
- [ ] Schema description/comment recommendation added for forbidden_actions format
- [ ] All existing .governance.yaml files still validate against updated schema
- [ ] agent-development-standards.md updated to document the new field

### Related Items

- Parent: [FEAT-002: Implement ADR-002](./FEAT-002-implement-adr-002-constitutional-upgrades.md)
- References: ADR-002 Sub-Decisions 2 and 3 (D-003, D-006)
- References: `docs/schemas/agent-governance-v1.schema.json`

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Updated governance schema | Schema modification | `docs/schemas/agent-governance-v1.schema.json` |
| Updated agent-development-standards.md | Rule file modification | `.context/rules/agent-development-standards.md` |

### Verification

- [ ] Acceptance criteria verified

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-28 | Created | Initial creation |
