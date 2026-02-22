# TASK-018: Generate agent-definition JSON Schema

> **Type:** task
> **Status:** pending
> **Priority:** medium
> **Impact:** medium
> **Criticality:** C2
> **Created:** 2026-02-21T23:59:00Z
> **Parent:** EN-001
> **Owner:** --
> **Effort:** 2
> **Activity:** development

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

Generate `docs/schemas/agent-definition-v1.schema.json` from the agent definition specification in ADR-PROJ007-001. This JSON Schema is required for H-32 (JSON Schema validation of agent definitions). The schema must validate against existing agent definition files in `skills/*/agents/*.md` YAML frontmatter.

### Steps

1. Read ADR-PROJ007-001 (installed by TASK-014) to extract the agent definition specification
2. Identify the required and optional fields for agent definition YAML frontmatter
3. Generate a JSON Schema (draft-07 or later) covering all specified fields
4. Verify the schema validates correctly against existing agent files in `skills/*/agents/`
5. Write to `docs/schemas/agent-definition-v1.schema.json`
6. Create `docs/schemas/` directory if it does not exist

---

## Acceptance Criteria

- [ ] AC-1: `agent-definition-v1.schema.json` exists at `docs/schemas/agent-definition-v1.schema.json`
- [ ] AC-2: Schema is valid JSON Schema (draft-07 or later)
- [ ] AC-3: Schema validates correctly against existing agent definition files in `skills/*/agents/*.md`
- [ ] AC-4: Schema is referenced by H-32 in `quality-enforcement.md` (confirm cross-reference after TASK-016)

---

## Implementation Notes

### Files to Create

| File | Action |
|------|--------|
| `docs/schemas/` | Create directory if absent |
| `docs/schemas/agent-definition-v1.schema.json` | Generate from ADR-PROJ007-001 specification |

### Validation Approach

Scan existing agent files under `skills/*/agents/` and extract YAML frontmatter. Run schema validation against each file. All existing agents must pass — the schema must be backwards-compatible.

### Dependency

TASK-014 (install ADR-PROJ007-001) should complete first so the specification is available. If ADR-001 is not yet installed, use the source orchestration artifact directly.

---

## Related Items

- **Parent:** [EN-001](../EN-001.md)
- **Specification source:** `docs/design/ADR-PROJ007-001-agent-design.md` (installed by TASK-014)
- **Required by:** H-32 in `quality-enforcement.md` (added by TASK-016)
- **Validates:** All agent definitions in `skills/*/agents/`

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-21 | pending | Created — depends on ADR-PROJ007-001 installation (TASK-014) |
