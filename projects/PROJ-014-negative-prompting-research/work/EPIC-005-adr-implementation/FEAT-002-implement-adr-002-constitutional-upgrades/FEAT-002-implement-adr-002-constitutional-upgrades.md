# FEAT-002: Implement ADR-002: Constitutional Triplet and High-Framing Upgrades

> **Type:** feature
> **Status:** in_progress
> **Priority:** medium
> **Impact:** medium
> **Created:** 2026-02-28
> **Parent:** EPIC-005
> **Owner:** —

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Feature description and value |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Children Stories/Enablers](#children-storiesenablers) | Task inventory |
| [Progress Summary](#progress-summary) | Overall progress |
| [Related Items](#related-items) | Dependencies and links |
| [History](#history) | Status changes |

---

## Summary

Implement ADR-002 (Constitutional Triplet and High-Framing Upgrades) in two phases. Phase 5A (immediate): update agent-development-standards.md guardrails template from NPT-014 to NPT-009 format and add forbidden_action_format tracking field to governance schema. Phase 5B (conditional on TASK-025 A/B testing results): full adoption or contingency for NPT-013 constitutional triplet in all 13 SKILL.md files.

**Value Proposition:**
- New agents automatically follow NPT-009 format through updated template
- Migration visibility via forbidden_action_format schema tracking field
- Consequence documentation in guardrails improves auditability

---

## Acceptance Criteria

### Definition of Done

- [x] Phase 5A: agent-development-standards.md guardrails template updated to NPT-009 format
- [x] Phase 5A: forbidden_action_format enum field added to agent-governance-v1.schema.json
- [x] Phase 5A: Schema description field recommendation added for forbidden_actions format
- [ ] Phase 5B: Conditional implementation based on TASK-025 A/B testing results

### Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | Guardrails template minimum example uses NPT-009 format with VIOLATION label | [x] |
| AC-2 | Governance schema has optional forbidden_action_format enum field | [x] |
| AC-3 | Existing agent files still validate against updated schema | [x] |

---

## Children Stories/Enablers

### Task Inventory

| ID | Title | Status | Priority |
|----|-------|--------|----------|
| TASK-033 | Phase 5A: Update guardrails template to NPT-009 format | completed | high |
| TASK-034 | Phase 5A: Add forbidden_action_format field to governance schema | completed | high |
| TASK-035 | Phase 5B: Full adoption or contingency (blocked by A/B testing) | pending | low |

### Task Links

- [TASK-033: Update guardrails template](./TASK-033-guardrails-template-upgrade.md)
- [TASK-034: Governance schema update](./TASK-034-governance-schema-update.md)
- [TASK-035: Phase 5B conditional adoption](./TASK-035-phase5b-conditional-adoption.md)

---

## Progress Summary

| Metric | Value |
|--------|-------|
| **Total Tasks** | 3 |
| **Completed Tasks** | 2 |
| **Completion %** | 67% |

---

## Related Items

### Hierarchy

- **Parent Epic:** [EPIC-005: ADR Implementation](../EPIC-005-adr-implementation.md)

### References

- ADR-002: `orchestration/neg-prompting-20260227-001/phase-5/ADR-002-constitutional-upgrades.md`

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-28 | Claude | pending | Feature created |
| 2026-02-28 | Claude | in_progress | TASK-033 + TASK-034 (Phase 5A) completed. TASK-035 blocked by A/B testing. |
