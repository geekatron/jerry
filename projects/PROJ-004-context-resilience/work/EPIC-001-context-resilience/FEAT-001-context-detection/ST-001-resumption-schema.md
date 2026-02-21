# ST-001: Enhanced Resumption Schema + Update Protocol

> **Type:** story
> **Status:** done
> **Priority:** high
> **Impact:** high
> **Created:** 2026-02-19
> **Due:** --
> **Completed:** 2026-02-21
> **Parent:** FEAT-001
> **Owner:** --
> **Effort:** 2-3h

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Scope |
| [Acceptance Criteria](#acceptance-criteria) | BDD scenarios and checklist |
| [Dependencies](#dependencies) | Relationships |
| [History](#history) | Status changes |

---

## Summary

Replace the current 5-field resumption section in `skills/orchestration/templates/ORCHESTRATION.template.yaml` with the v2.0 schema: Recovery State (8 fields), Files to Read (structured with priority/purpose/sections), Quality Trajectory (7 fields), Defect Summary (5 fields), Decision Log (N entries), Agent Summaries (N entries), Compaction Events (2 + N entries). Update the orchestrator agent prompt with an explicit resumption update protocol. Add an L2-REINJECT marker to `quality-enforcement.md` for resumption update reminders (~25 tokens, rank ~9).

**Quality Gate:** C3 minimum per AE-002 (touches `.context/rules/`).

---

## Acceptance Criteria

### BDD Scenarios (pytest-bdd)

```gherkin
Feature: ORCHESTRATION.yaml v2.0 resumption schema

  Scenario: Template contains all 7 resumption sub-sections
    Given the ORCHESTRATION.template.yaml file
    When I parse the resumption section
    Then it should contain: recovery_state, files_to_read, quality_trajectory, defect_summary, decision_log, agent_summaries, compaction_events

  Scenario: Backward compatible with existing 5 fields
    Given an ORCHESTRATION.yaml with old 5-field resumption section
    When the v2.0 schema is applied
    Then the 5 original fields should be preserved within recovery_state

  Scenario: updated_at timestamp present
    Given an ORCHESTRATION.yaml with v2.0 resumption section
    Then the resumption section should contain an updated_at field in ISO 8601 format

  Scenario: L2-REINJECT marker within token budget
    Given quality-enforcement.md with existing L2-REINJECT markers
    When the new resumption update marker is added
    Then total L2-REINJECT content should be within 600 tokens
    And the new marker should have rank ~9 and ~25 tokens
```

### Acceptance Checklist

- [ ] ORCHESTRATION.yaml template has v2.0 resumption schema with all 7 sub-sections
- [ ] Backward compatible: existing 5 fields preserved in Recovery State
- [ ] Orchestrator prompt includes update protocol with 6 triggers
- [ ] L2-REINJECT marker in `quality-enforcement.md` within 600-token total budget
- [ ] `updated_at` ISO 8601 timestamp field present
- [ ] Quality gate: C3 per AE-002

---

## Dependencies

**Depends On:** Nothing

**Enables:**
- EN-003 (CheckpointData.resumption_state maps to this schema)
- EN-004 (ResumptionContextGenerator reads schema fields)
- EN-005 (staleness detection checks updated_at)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-19 | Claude | pending | Story created from CWI-04. |
