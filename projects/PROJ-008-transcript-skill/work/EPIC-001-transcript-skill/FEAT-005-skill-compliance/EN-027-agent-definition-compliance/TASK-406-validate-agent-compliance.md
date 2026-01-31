# TASK-406: Validate agent compliance with checklist

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

---

## Frontmatter

```yaml
id: "TASK-406"
work_type: TASK
title: "Validate agent compliance with checklist"
status: BACKLOG
priority: HIGH
assignee: "Claude"
created_at: "2026-01-30T16:00:00Z"
parent_id: "EN-027"
effort: 0.5
activity: TESTING
```

---

## Description

Run the Master Agent Definition Compliance Checklist (from work-026-e-003) against all 5 updated agent definitions to verify >= 90% compliance score.

**Files to validate:**
- skills/transcript/agents/ts-parser.md
- skills/transcript/agents/ts-extractor.md
- skills/transcript/agents/ts-formatter.md
- skills/transcript/agents/ts-mindmap-mermaid.md
- skills/transcript/agents/ts-mindmap-ascii.md

---

## Acceptance Criteria

- [ ] All 5 agents score >= 90% on Agent Compliance Checklist
- [ ] All CRITICAL checkpoints (A-001 to A-004, A-005, A-007, etc.) pass
- [ ] Any failures documented with remediation plan
- [ ] Live pipeline test passes after changes

---

## Checklist to Apply

From work-026-e-003 Section 2.2 (57 total checkpoints):

### YAML Frontmatter: Basic Metadata (4)
- [ ] A-001: `name` matches agent ID
- [ ] A-002: `version` follows semver
- [ ] A-003: `description` is 2-3 sentences
- [ ] A-004: `model` specified

### Identity Section (4)
- [ ] A-005: `identity.role` defined
- [ ] A-006: `identity.expertise` has 3+ items
- [ ] A-007: `identity.cognitive_mode` is divergent|convergent
- [ ] A-008: Cognitive mode matches agent style

### Persona Section (3)
- [ ] A-009: `persona.tone` specified
- [ ] A-010: `persona.communication_style` specified
- [ ] A-011: `persona.audience_level` is "adaptive"

### Capabilities Section (6)
- [ ] A-012: `capabilities.allowed_tools` has 5+ tools
- [ ] A-013: `capabilities.output_formats` includes markdown
- [ ] A-014: `capabilities.forbidden_actions` has 3+ items
- [ ] A-015: Forbidden: P-003 (recursion)
- [ ] A-016: Forbidden: P-020 (override)
- [ ] A-017: Forbidden: P-002 (transient)

### Guardrails Section (4)
- [ ] A-018: `guardrails.input_validation` defined
- [ ] A-019: `guardrails.output_filtering` has 2+ filters
- [ ] A-020: `guardrails.fallback_behavior` specified
- [ ] A-021: Input validation includes format rules

### Output Section (4)
- [ ] A-022: `output.required` is true
- [ ] A-023: `output.location` is path template
- [ ] A-024: `output.template` references file (if applicable)
- [ ] A-025: `output.levels` is [L0, L1, L2]

### Validation Section (3)
- [ ] A-026: `validation.file_must_exist` is true
- [ ] A-027: `validation.post_completion_checks` has 3+ items
- [ ] A-028: Includes verify_file_created

### Constitution Section (7)
- [ ] A-029: `constitution.reference` points to Jerry Constitution
- [ ] A-030: `constitution.principles_applied` has 5+ principles
- [ ] A-031: Includes P-001
- [ ] A-032: Includes P-002
- [ ] A-033: Includes P-003
- [ ] A-034: Includes P-004 (for research agents)
- [ ] A-035: Includes P-022

### Session Context Section (6)
- [ ] A-038: `session_context.schema` defined
- [ ] A-039: `session_context.schema_version` is "1.0.0"
- [ ] A-040: `input_validation` is true
- [ ] A-041: `output_validation` is true
- [ ] A-042: `on_receive` has 4+ actions
- [ ] A-043: `on_send` has 4+ actions

---

## Scoring

**Compliance Score Calculation:**
- CRITICAL (22 items): × 0.50
- HIGH (23 items): × 0.35
- MEDIUM (12 items): × 0.15
- **Target: >= 90%**

---

## Related Items

- Parent: [EN-027: Agent Definition Compliance](./EN-027-agent-definition-compliance.md)
- Checklist: work-026-e-003 Section 2.2

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Compliance scores | Report | (To be documented) |
| Pipeline test results | Test | (Live test after changes) |

### Verification

- [ ] All agents score >= 90%
- [ ] Pipeline test passes

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-30 | Created | Initial creation per EN-027 |
