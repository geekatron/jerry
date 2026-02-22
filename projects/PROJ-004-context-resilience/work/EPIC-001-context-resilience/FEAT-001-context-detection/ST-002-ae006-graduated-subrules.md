# ST-002: AE-006 Graduated Sub-Rules

> **Type:** story
> **Status:** completed
> **Priority:** high
> **Impact:** medium
> **Created:** 2026-02-19
> **Due:** --
> **Completed:** 2026-02-21
> **Parent:** FEAT-001
> **Owner:** --
> **Effort:** 1h

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

Replace the single AE-006 rule in `quality-enforcement.md` with 5 graduated sub-rules (AE-006a through AE-006e) mapping detection thresholds to escalation actions by criticality level. Add an L2-REINJECT marker (~35 tokens, rank ~8). The existing `PromptReinforcementEngine` picks up new L2-REINJECT markers automatically.

**Quality Gate:** C3 minimum per AE-002 (touches `.context/rules/`).

---

## Acceptance Criteria

### BDD Scenarios (pytest-bdd)

```gherkin
Feature: Graduated context exhaustion escalation rules

  Scenario: AE-006a through AE-006e defined
    Given quality-enforcement.md Auto-Escalation Rules table
    When I parse the table
    Then entries AE-006a, AE-006b, AE-006c, AE-006d, AE-006e should exist

  Scenario: Each sub-rule references ThresholdTier
    Given the AE-006 sub-rules
    Then AE-006a should reference NOMINAL/LOW tier
    And AE-006b should reference WARNING tier
    And AE-006c should reference CRITICAL tier
    And AE-006d should reference EMERGENCY tier
    And AE-006e should reference compaction event

  Scenario: L2-REINJECT budget maintained
    Given the new L2-REINJECT marker for AE-006 escalation
    When added to existing markers
    Then total L2-REINJECT token budget should be within 600 tokens
```

### Acceptance Checklist

- [ ] AE-006a through AE-006e defined in Auto-Escalation Rules table
- [ ] Each sub-rule: trigger condition, escalation action, enforcement mechanism
- [ ] L2-REINJECT marker present (rank ~8, ~35 tokens)
- [ ] Total L2-REINJECT budget within 600 tokens
- [ ] Quality gate: C3 per AE-002

---

## Dependencies

**Depends On:** EN-004 (ContextFillEstimator and ThresholdTier must exist)

**Enables:** Nothing directly

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-19 | Claude | pending | Story created from CWI-05. |
