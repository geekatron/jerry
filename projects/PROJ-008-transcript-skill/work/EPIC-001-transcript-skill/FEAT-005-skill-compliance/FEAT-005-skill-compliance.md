# FEAT-005: Skill Compliance

<!--
TEMPLATE: Feature
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.4
CREATED: 2026-01-30 per work-026 analysis and synthesis
PURPOSE: Bring transcript skill to 95%+ compliance with Jerry skill patterns
-->

> **Type:** feature
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Created:** 2026-01-30T16:00:00Z
> **Due:** TBD
> **Completed:** -
> **Parent:** EPIC-001
> **Owner:** Claude
> **Target Sprint:** -

---

## Summary

Bring the transcript skill to 95%+ compliance with Jerry's universal skill patterns as documented in problem-solving, nasa-se, and orchestration skills. Currently at 52% compliance with 30 identified gaps.

**Value Proposition:**
- Enable cross-skill integration (transcript ↔ problem-solving ↔ orchestration)
- Standardize agent metadata for consistent orchestration behavior
- Improve maintainability through pattern adherence
- Enable future skill composition capabilities

**Origin Documents:**
- [work-026-e-001: Jerry Skill Patterns Research](../../../../docs/research/work-026-e-001-jerry-skill-patterns.md)
- [work-026-e-002: Transcript Skill Gap Analysis](../../../../docs/analysis/work-026-e-002-transcript-skill-gap-analysis.md)
- [work-026-e-003: Jerry Skill Compliance Framework](../../../../docs/synthesis/work-026-e-003-jerry-skill-compliance-framework.md)

---

## Benefit Hypothesis

**We believe that** standardizing transcript skill agents and documentation to match Jerry's universal patterns

**Will result in** seamless cross-skill integration, improved orchestration capabilities, and reduced maintenance overhead

**We will know we have succeeded when** compliance score reaches 95%+ on the Master Agent Definition and SKILL.md checklists from work-026-e-003

---

## Acceptance Criteria

### Definition of Done

- [ ] All 5 agent definitions compliant with PAT-AGENT-001 (Universal Agent Metadata Schema)
- [ ] SKILL.md compliant with PAT-SKILL-001 (Universal SKILL.md Structure)
- [ ] PLAYBOOK.md compliant with PAT-PLAYBOOK-001 (Triple-Lens Playbook)
- [ ] Anti-pattern catalog documented (4+ anti-patterns)
- [ ] Model selection capability implemented
- [ ] ps-critic validation passes with >= 0.90 score
- [ ] All acceptance criteria verified

### Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | Agent YAML frontmatter includes all required sections (identity, persona, capabilities, guardrails, output, validation, constitution, session_context) | [ ] |
| AC-2 | SKILL.md includes "Invoking an Agent" section with 3 methods | [ ] |
| AC-3 | State passing schema includes session_context reference and versioning | [ ] |
| AC-4 | PLAYBOOK.md includes anti-pattern catalog with ASCII diagrams | [ ] |
| AC-5 | Model selection configurable via CLI parameters | [ ] |

### Non-Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| NFC-1 | Backward compatibility maintained for existing pipelines | [ ] |
| NFC-2 | Documentation follows Triple-Lens format (L0/L1/L2) | [ ] |
| NFC-3 | All changes validated via live transcript pipeline test | [ ] |

---

## MVP Definition

### In Scope (MVP)

- Agent YAML frontmatter standardization (Phase 1 CRITICAL gaps)
- SKILL.md section additions (Phase 2 HIGH gaps)
- Anti-pattern catalog (Phase 3 MEDIUM)
- Model selection capability

### Out of Scope (Future)

- Automated compliance scoring tool
- Schema JSON files (session_context.json, index.schema.json)
- Cross-skill orchestration examples
- Integration tests for cross-skill handoffs

---

## Children (Enablers)

### Enabler Inventory

| ID | Type | Title | Status | Priority | Effort | Dependencies |
|----|------|-------|--------|----------|--------|--------------|
| EN-027 | Enabler | Agent Definition Compliance | pending | critical | 10h | None |
| EN-028 | Enabler | SKILL.md Compliance | pending | high | 9h | EN-027 |
| EN-029 | Enabler | Documentation Compliance | pending | medium | 9h | EN-028 |
| EN-030 | Enabler | Documentation Polish | pending | low | 5h | EN-029 |
| EN-031 | Enabler | Model Selection Capability | pending | medium | 32-48h | None |

### Work Item Links

- [EN-027: Agent Definition Compliance](./EN-027-agent-definition-compliance/EN-027-agent-definition-compliance.md) - Phase 1 CRITICAL
- [EN-028: SKILL.md Compliance](./EN-028-skill-md-compliance/EN-028-skill-md-compliance.md) - Phase 2 HIGH
- [EN-029: Documentation Compliance](./EN-029-documentation-compliance/EN-029-documentation-compliance.md) - Phase 3 MEDIUM
- [EN-030: Documentation Polish](./EN-030-documentation-polish/EN-030-documentation-polish.md) - Phase 4 LOW
- [EN-031: Model Selection Capability](./EN-031-model-selection-capability/EN-031-model-selection-capability.md) - Model configuration

### Dependency Chain

```
                    ┌─────────────────────┐
                    │   EN-031 (32-48h)   │  (Independent - Model Selection)
                    │  Model Selection    │
                    └─────────────────────┘

    ┌───────────────────────────────────────────────────────────────────┐
    │                    SEQUENTIAL CHAIN (Phases 1-4)                  │
    │                                                                   │
    │   EN-027 (10h)    EN-028 (9h)     EN-029 (9h)    EN-030 (5h)     │
    │   CRITICAL   ───► HIGH       ───► MEDIUM    ───► LOW             │
    │   Agent YAML      SKILL.md        PLAYBOOK.md    Final polish    │
    │                                                                   │
    └───────────────────────────────────────────────────────────────────┘

Total Sequential: 33 hours (4.1 days)
Model Selection: 32-48 hours (4-6 days) - Can run in parallel
```

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                   FEATURE PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Enablers:  [....................] 0% (0/5 completed)             |
| Tasks:     [....................] 0% (0/25 completed)            |
+------------------------------------------------------------------+
| Overall:   [....................] 0%                             |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Enablers** | 5 |
| **Completed Enablers** | 0 |
| **Total Tasks** | 25 |
| **Completed Tasks** | 0 |
| **Total Effort (hours)** | 65-81 |
| **Completed Effort** | 0 |
| **Completion %** | 0% |

---

## Gap Coverage Mapping

| Phase | Gaps Addressed | Enabler | Status |
|-------|---------------|---------|--------|
| **Phase 1 CRITICAL** | GAP-A-001, GAP-A-004, GAP-A-007, GAP-A-009, GAP-Q-001 | EN-027 | pending |
| **Phase 2 HIGH** | GAP-S-001, GAP-S-003, GAP-A-002, GAP-A-005, GAP-A-006 | EN-028 | pending |
| **Phase 3 MEDIUM** | GAP-D-001, GAP-D-002, GAP-D-003, GAP-O-001 | EN-029 | pending |
| **Phase 4 LOW** | GAP-S-006, GAP-D-005, GAP-D-006 | EN-030 | pending |
| **Model Selection** | N/A (New capability) | EN-031 | pending |

**Reference:** work-026-e-002 Section "Gap Analysis" for gap definitions

---

## Related Items

### Hierarchy

- **Parent Epic:** [EPIC-001: Transcript Skill](../../EPIC-001-transcript-skill.md)

### Related Features

- [FEAT-002: Implementation](../FEAT-002-implementation/FEAT-002-implementation.md) - Core implementation (prerequisite)
- [FEAT-003: Future Enhancements](../FEAT-003-future-enhancements/FEAT-003-future-enhancements.md) - Related tech debt
- [FEAT-004: Hybrid Infrastructure](../FEAT-004-hybrid-infrastructure/FEAT-004-hybrid-infrastructure.md) - Parser infrastructure (completed)

### Analysis References

- [work-026-e-001: Jerry Skill Patterns Research](../../../../docs/research/work-026-e-001-jerry-skill-patterns.md)
- [work-026-e-002: Gap Analysis](../../../../docs/analysis/work-026-e-002-transcript-skill-gap-analysis.md)
- [work-026-e-003: Compliance Framework](../../../../docs/synthesis/work-026-e-003-jerry-skill-compliance-framework.md)
- [work-025-e-001: Model Selection Effort](../../../../docs/analysis/work-025-e-001-model-selection-effort.md)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-30T16:00:00Z | Claude | pending | Feature created per work-026 analysis. 5 enablers, 25 tasks. Based on gap analysis identifying 30 gaps at 52% current compliance. |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | Feature |
| **SAFe** | Feature (Program Backlog) |
| **JIRA** | Epic (or custom issue type) |

---

<!--
DESIGN RATIONALE:

This feature addresses compliance gaps discovered during work-026 skill pattern
analysis. The problem-solving skill was used to:
1. Research patterns across 3 Jerry skills (ps-researcher)
2. Analyze gaps in transcript skill (ps-analyst)
3. Synthesize a compliance framework (ps-synthesizer)

The 80/20 rule applies: Phases 1-2 (19 hours) will resolve 80% of impact.
Model selection is independent and can run in parallel.

PARETO ANALYSIS:
- 17 HIGH/CRITICAL gaps represent 20% of work
- Resolving these fixes 80% of compliance issues
- Total sequential effort: 33 hours (4 days)
- Model selection adds 4-6 days (parallel)

TRACE:
- work-026-e-001 → Pattern research
- work-026-e-002 → Gap analysis
- work-026-e-003 → Remediation plan → This feature
- work-025-e-001 → Model selection analysis
-->
