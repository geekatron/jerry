# FEAT-005:DISC-003: Orchestration v2.x Dependency Chain Flaw

<!--
TEMPLATE: Discovery
VERSION: 1.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9, worktracker.md (Discovery File)
CREATED: 2026-01-31 (FEAT-005 Orchestration Analysis)
-->

> **Type:** discovery
> **Status:** DOCUMENTED
> **Priority:** CRITICAL
> **Impact:** HIGH
> **Created:** 2026-01-31T03:00:00Z
> **Completed:** 2026-01-31T03:30:00Z
> **Parent:** FEAT-005
> **Owner:** Claude
> **Source:** ORCHESTRATION_PLAN.md v2.x analysis

---

## Frontmatter

```yaml
id: "FEAT-005:DISC-003"
work_type: DISCOVERY
title: "Orchestration v2.x Dependency Chain Flaw"
classification: TECHNICAL
status: DOCUMENTED
resolution: null
priority: CRITICAL
impact: HIGH
assignee: null
created_by: "Claude"
created_at: "2026-01-31T03:00:00Z"
updated_at: "2026-01-31T03:30:00Z"
completed_at: "2026-01-31T03:30:00Z"
parent_id: "FEAT-005"
tags: ["orchestration", "dependency-chain", "critical-path", "task-419"]
finding_type: GAP
confidence_level: HIGH
source: "ORCHESTRATION_PLAN.md v2.x review"
research_method: "Dependency chain analysis"
validated: true
validation_date: "2026-01-31T03:30:00Z"
validated_by: "User"
```

---

## State Machine

```
                 +----------+
                 |  PENDING |  <-- Initial state
                 +----+-----+
                      |
                      v
              +--------------+
              | IN_PROGRESS  |
              +------+-------+
                     |
                     v
              +------------+
              | DOCUMENTED |  <-- CURRENT STATE
              +------------+
```

---

## Summary

**The ORCHESTRATION_PLAN v2.x has a critical dependency chain flaw: TASK-419 (Model Parameter Validation) is shown as parallel to EN-027 when it MUST be a sequential prerequisite gating ALL downstream work.**

**Key Findings:**
- TASK-419 validates whether the Task tool's `model` parameter works as expected
- If TASK-419 fails, both Track A (Compliance Chain) and Track B (Model Selection) are fundamentally affected
- The current v2.x plan allows EN-027 and TASK-419 to start simultaneously, which is incorrect
- TASK-419 failure is a "hard gate" requiring user decision before proceeding

**Validation:** User-confirmed during orchestration planning session (2026-01-31)

---

## Context

### Background

FEAT-005 (Skill Compliance) has two conceptual tracks:
- **Track A:** Sequential Compliance Chain (EN-027 → EN-028 → EN-029 → EN-030)
- **Track B:** Model Selection Capability (EN-031 with Phases 1-3)

The current ORCHESTRATION_PLAN.md v2.x and ORCHESTRATION.yaml v2.2.0 represent these as parallel tracks starting simultaneously. However, TASK-419 ("Validate Task tool model parameter") is marked as Phase 1 of Track B and is described as "CRITICAL - Early validation" in the documentation.

### Research Question

**Is it correct to start EN-027 (Track A) and TASK-419 (Track B Phase 1) in parallel, or does TASK-419 represent a sequential prerequisite that must complete before ANY parallel work begins?**

### Investigation Approach

1. Analyzed TASK-419's purpose and downstream dependencies
2. Traced what happens if TASK-419 fails vs. succeeds
3. Mapped cross-pollination points (CP-1, CP-2, CP-3) to understand information flow
4. Evaluated the impact on both tracks if TASK-419 fails

---

## Finding

### TASK-419 Purpose Analysis

TASK-419 validates whether Claude Code's Task tool accepts a `model` parameter for agent spawning. This is fundamental because:

1. **If model parameter WORKS:** EN-031's model selection feature is viable
2. **If model parameter FAILS:** The entire premise of EN-031 is invalid, and we need user decision on alternatives

The Task tool documentation states:
```
"model": {"description": "Optional model to use for this agent. If not specified, inherits from parent.
Prefer haiku for quick, straightforward tasks to minimize cost and latency.",
"enum": ["sonnet", "opus", "haiku"], "type": "string"}
```

This suggests the parameter exists, but validation is still required to confirm:
- It works as documented
- The model names are correct (sonnet vs claude-3-sonnet, etc.)
- Downstream agents can actually use different models

### The Flaw in v2.x

**Current v2.x Structure (FLAWED):**
```
Day 1: EN-027 (Track A) ←──────────────→ TASK-419 (Track B Phase 1)
       Starting parallel                   Starting parallel
```

**Correct Structure (PROPOSED v3.0):**
```
Phase 0: TASK-419 (Sequential Hard Gate)
         │
         ▼ PASS: Validates model param works
         │ FAIL: Hard blocker → User decision required
         │
Phase 1+: Parallel tracks BEGIN HERE
         ├─→ Track A: EN-027 → EN-028 → EN-029 → EN-030
         └─→ Track B: TASK-420 → TASK-421 → ...
```

**Key Observations:**
1. TASK-419 results inform EN-027's agent definitions (how to specify model overrides)
2. TASK-419 results determine if EN-031 Phase 2-3 are even relevant
3. Starting EN-027 without TASK-419 results means potentially incorrect agent schemas
4. TASK-419 is a validation task (2h) vs EN-027 which is implementation (10h)

### Cross-Pollination Impact

The v2.x plan documents three cross-pollination points:

| CP ID | Trigger | From | To | Impact if TASK-419 First |
|-------|---------|------|-----|--------------------------|
| CP-1 | TASK-419 complete | Track B | Track A | ✅ EN-027 gets model param validation results BEFORE starting |
| CP-2 | EN-027 complete | Track A | Track B | ✅ TASK-422 gets correct agent YAML patterns |
| CP-3 | TASK-420 complete | Track B | Track A | ✅ SKILL.md docs have correct CLI parameter design |

**If TASK-419 runs first (v3.0):** All cross-pollination flows correctly
**If TASK-419 runs parallel (v2.x):** CP-1 is broken; EN-027 starts without knowing model param behavior

### Validation

**User confirmed this analysis on 2026-01-31:**

> "Claude, if task 419 is a blocker for other tasks, then why didn't you make that the sequential unit of work and then run parallel tracks afterwards? You need to understand the dependency chain..."

**Validation Results:**
- User agrees TASK-419 should be Phase 0 (sequential prerequisite)
- User agrees TASK-419 failure should be a "hard blocker requiring user decision"
- User requested ORCHESTRATION_PLAN v3.0 with corrected dependency chain

---

## Evidence

### Source Documentation

| Evidence ID | Type | Description | Source | Date |
|-------------|------|-------------|--------|------|
| E-001 | Document | ORCHESTRATION_PLAN.md v2.x showing parallel tracks | orchestration/ORCHESTRATION_PLAN.md | 2026-01-31 |
| E-002 | Document | ORCHESTRATION.yaml showing `track_a` and `track_b` as independent | orchestration/ORCHESTRATION.yaml | 2026-01-31 |
| E-003 | Tool Spec | Task tool model parameter documentation | Claude Code system prompt | 2026-01-31 |
| E-004 | User Feedback | User identifying the dependency chain flaw | Conversation transcript | 2026-01-31 |

### Reference Material

- **Source:** ORCHESTRATION.yaml v2.2.0
- **URL:** `orchestration/ORCHESTRATION.yaml`
- **Date Accessed:** 2026-01-31
- **Relevance:** Shows current flawed structure with parallel track start

### Expert Review

- **Reviewer:** User (Project Owner)
- **Date:** 2026-01-31
- **Feedback:** "TASK-419 should be sequential prerequisite before parallel tracks begin"

---

## Implications

### Impact on Project

This discovery requires creating ORCHESTRATION_PLAN v3.0 with a corrected dependency structure. The v2.x plan is fundamentally flawed and would lead to:
- Potential rework if EN-027 starts before TASK-419 completes
- Risk of incorrect agent definitions if model param doesn't work as expected
- Wasted effort on Track B Phase 2-3 if model param validation fails

### Design Decisions Affected

- **Decision:** ORCHESTRATION_PLAN v3.0 structure
  - **Impact:** Complete redesign of Phase 0 as sequential gate
  - **Rationale:** Correct dependency chain prevents rework and waste

- **Decision:** TASK-419 failure handling
  - **Impact:** Must be "hard blocker requiring user decision"
  - **Rationale:** User authority over fundamental feature viability

### Risks Identified

| Risk | Severity | Mitigation |
|------|----------|------------|
| Proceeding with v2.x causes rework | HIGH | Create v3.0 with corrected dependencies |
| TASK-419 fails, invalidating EN-031 | MEDIUM | Make TASK-419 failure a hard gate with user decision |
| Parallel tracks start without validation results | HIGH | Enforce TASK-419 completion before Phase 1 |

### Opportunities Created

- Cleaner orchestration plan with explicit sequential prerequisite
- Opportunity to add adversarial critic feedback after TASK-419
- Better cross-pollination documentation with no ambiguity

---

## Relationships

### Creates

- [FEAT-005:DEC-002](./FEAT-005--DEC-002-orchestration-v3-design-decisions.md) - Design decisions for v3.0
- ORCHESTRATION_PLAN v3.0 - Corrected orchestration plan

### Informs

- [ORCHESTRATION_PLAN.md](./orchestration/ORCHESTRATION_PLAN.md) - Requires v3.0 redesign
- [ORCHESTRATION.yaml](./orchestration/ORCHESTRATION.yaml) - Requires Phase 0 addition
- [EN-027](./EN-027-agent-definition-compliance/EN-027-agent-definition-compliance.md) - Now depends on TASK-419

### Related Discoveries

- [FEAT-003:DISC-002](../FEAT-003-future-enhancements/FEAT-003--DISC-002-adversarial-prompting-protocol.md) - Adversarial prompting protocol for quality gates

### Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Parent | [FEAT-005](./FEAT-005-skill-compliance.md) | Parent feature |
| Reference | [ORCHESTRATION.yaml](./orchestration/ORCHESTRATION.yaml) | Current v2.2.0 state |
| Reference | [TASK-419](./EN-031-model-selection-capability/TASK-419-validate-task-model.md) | Critical validation task |

---

## Recommendations

### Immediate Actions

1. Create FEAT-005:DEC-002 documenting the v3.0 design decisions
2. Create ORCHESTRATION_PLAN v3.0 with TASK-419 as Phase 0 sequential gate
3. Update ORCHESTRATION.yaml to v3.0.0 with corrected structure

### Long-term Considerations

- Consider adding validation tasks as Phase 0 for future orchestration plans
- Document this pattern in orchestration skill playbook

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-31T03:30:00Z | Claude | Documented findings with user validation |
| 2026-01-31T03:00:00Z | Claude | Created discovery |

---

## Metadata

```yaml
id: "FEAT-005:DISC-003"
parent_id: "FEAT-005"
work_type: DISCOVERY
title: "Orchestration v2.x Dependency Chain Flaw"
status: DOCUMENTED
priority: CRITICAL
impact: HIGH
created_by: "Claude"
created_at: "2026-01-31T03:00:00Z"
updated_at: "2026-01-31T03:30:00Z"
completed_at: "2026-01-31T03:30:00Z"
tags: [orchestration, dependency-chain, critical-path, task-419]
source: "ORCHESTRATION_PLAN.md v2.x review"
finding_type: GAP
confidence_level: HIGH
validated: true
```
