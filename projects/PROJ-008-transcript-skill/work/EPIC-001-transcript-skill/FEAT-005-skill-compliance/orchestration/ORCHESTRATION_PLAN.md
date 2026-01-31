# Orchestration Plan: FEAT-005 Skill Compliance

> **Workflow ID:** feat-005-compliance-20260130-001
> **Version:** 2.0.0
> **Status:** ACTIVE
> **Created:** 2026-01-30T22:00:00Z
> **Location:** FEAT-005-skill-compliance/orchestration/

---

## Executive Summary (L0)

This orchestration plan coordinates **execution** of the 25 pre-designed tasks for FEAT-005 skill compliance. The design and analysis work is complete (work-026). This plan focuses on:

- **Task execution tracking** across 5 enablers
- **Parallel execution** of Track A (EN-027→EN-030) and Track B (EN-031)
- **Quality gates** using ps-critic validation at enabler completion
- **Cross-pollination** where Track B discoveries inform Track A

**Note:** Research and analysis phases are NOT included - that work is already done and documented in the task files.

---

## Workflow Diagram

```
FEAT-005 SKILL COMPLIANCE EXECUTION
═══════════════════════════════════

                        ┌─────────────────────────────────┐
                        │        WORKFLOW START           │
                        │   feat-005-compliance-20260130  │
                        └───────────────┬─────────────────┘
                                        │
              ┌─────────────────────────┴─────────────────────────┐
              │                                                   │
              ▼                                                   ▼
╔═══════════════════════════════════════╗   ╔═══════════════════════════════════════╗
║  TRACK A: SEQUENTIAL COMPLIANCE       ║   ║  TRACK B: MODEL SELECTION (PARALLEL)  ║
║  EN-027 → EN-028 → EN-029 → EN-030    ║   ║  EN-031 (Independent)                 ║
║  33 hours sequential                  ║   ║  34 hours                             ║
╚═══════════════════════════════════════╝   ╚═══════════════════════════════════════╝
              │                                                   │
              ▼                                                   ▼
┌─────────────────────────────────────┐   ┌─────────────────────────────────────┐
│  EN-027: Agent Definition (10h)     │   │  EN-031 Phase 1: Validation         │
│  ───────────────────────────────────│   │  ───────────────────────────────────│
│  TASK-400: Add identity section     │   │  TASK-419: Validate Task tool model │
│  TASK-401: Add capabilities section │   │            parameter                │
│  TASK-402: Add guardrails section   │   │                                     │
│  TASK-403: Add validation section   │   │  Effort: 2h                         │
│  TASK-404: Add constitution section │   └──────────────────┬──────────────────┘
│  TASK-405: Add session_context      │                      │
│  TASK-406: Validate compliance      │                      ▼
│                                     │   ┌─────────────────────────────────────┐
│  ┌───────────────────────────────┐  │   │  EN-031 Phase 2: Implementation     │
│  │ 🔄 ps-critic GATE (>= 0.90)   │  │   │  ───────────────────────────────────│
│  └───────────────────────────────┘  │   │  TASK-420: Add CLI model params     │
└──────────────────┬──────────────────┘   │  TASK-421: Update SKILL.md docs     │
                   │                      │  TASK-422: Update agent definitions │
                   ▼                      │  TASK-423: Implement profiles       │
┌─────────────────────────────────────┐   │                                     │
│  EN-028: SKILL.md Compliance (9h)   │   │  Effort: 24h                        │
│  ───────────────────────────────────│   └──────────────────┬──────────────────┘
│  TASK-407: Add invoking section     │                      │
│  TASK-408: Enhance state passing    │                      ▼
│  TASK-409: Add persistence section  │   ┌─────────────────────────────────────┐
│  TASK-410: Add self-critique        │   │  EN-031 Phase 3: Testing            │
│  TASK-411: Restructure persona      │   │  ───────────────────────────────────│
│                                     │   │  TASK-424: Integration testing      │
│  ┌───────────────────────────────┐  │   │                                     │
│  │ 🔄 ps-critic GATE (>= 0.90)   │  │   │  Effort: 8h                         │
│  └───────────────────────────────┘  │   │                                     │
└──────────────────┬──────────────────┘   │  ┌───────────────────────────────┐  │
                   │                      │  │ 🔄 ps-critic GATE (>= 0.90)   │  │
                   ▼                      │  └───────────────────────────────┘  │
┌─────────────────────────────────────┐   └──────────────────┬──────────────────┘
│  EN-029: Documentation (9h)         │                      │
│  ───────────────────────────────────│                      │
│  TASK-412: Add L2 architect section │                      │
│  TASK-413: Create anti-patterns     │                      │
│  TASK-414: Declare pattern refs     │                      │
│  TASK-415: Add constraints section  │                      │
│                                     │                      │
│  ┌───────────────────────────────┐  │                      │
│  │ 🔄 ps-critic GATE (>= 0.90)   │  │                      │
│  └───────────────────────────────┘  │                      │
└──────────────────┬──────────────────┘                      │
                   │                                         │
                   ▼                                         │
┌─────────────────────────────────────┐                      │
│  EN-030: Documentation Polish (5h)  │                      │
│  ───────────────────────────────────│                      │
│  TASK-416: Add tool examples        │                      │
│  TASK-417: Add design rationale     │                      │
│  TASK-418: Add cross-skill refs     │                      │
│                                     │                      │
│  ┌───────────────────────────────┐  │                      │
│  │ 🔄 ps-critic GATE (>= 0.95)   │  │                      │
│  └───────────────────────────────┘  │                      │
└──────────────────┬──────────────────┘                      │
                   │                                         │
                   └─────────────────┬───────────────────────┘
                                     │
                                     ▼
                   ╔═════════════════════════════════════════╗
                   ║         FINAL QUALITY GATE              ║
                   ║    ps-critic aggregate >= 0.90          ║
                   ║    All 25 tasks complete                ║
                   ║    Compliance score >= 95%              ║
                   ╚═════════════════════════════════════════╝
                                     │
                                     ▼
                   ┌─────────────────────────────────────────┐
                   │          WORKFLOW COMPLETE              │
                   │     FEAT-005 at 95%+ Compliance         │
                   └─────────────────────────────────────────┘

LEGEND:
═══════
🔄  ps-critic quality gate (adversarial validation)
→   Sequential dependency
```

---

## Task Inventory by Enabler

### EN-027: Agent Definition Compliance (7 tasks, 10h)

| Task ID | Title | Effort | Description |
|---------|-------|--------|-------------|
| TASK-400 | Add identity section | 1h | Add identity YAML to all 5 agents (role, expertise, cognitive_mode) |
| TASK-401 | Add capabilities section | 1.5h | Add capabilities YAML (allowed_tools, forbidden_actions) |
| TASK-402 | Add guardrails section | 3h | Add guardrails YAML (input_validation, output_filtering) |
| TASK-403 | Add validation section | 2h | Add validation YAML (post_completion_checks) |
| TASK-404 | Add constitution section | 1h | Add constitution YAML (principles_applied) |
| TASK-405 | Add session_context section | 1h | Add session_context YAML (schema, on_receive, on_send) |
| TASK-406 | Validate agent compliance | 0.5h | Run Agent Compliance Checklist, verify >= 90% |

**Quality Gate:** ps-critic validates all 5 agent files against PAT-AGENT-001

### EN-028: SKILL.md Compliance (5 tasks, 9h)

| Task ID | Title | Effort | Description |
|---------|-------|--------|-------------|
| TASK-407 | Add invoking section | 1h | Add "Invoking an Agent" with 3 methods |
| TASK-408 | Enhance state passing | 2h | Add session_context schema to state passing |
| TASK-409 | Add persistence section | 1h | Add "Mandatory Persistence (P-002)" section |
| TASK-410 | Add self-critique | 1h | Add self-critique checklist to Constitutional Compliance |
| TASK-411 | Restructure persona/output | 2h | Move persona to top-level, add output sections |

**Blocked By:** EN-027 (agent YAML must be standardized first)
**Quality Gate:** ps-critic validates SKILL.md against PAT-SKILL-001

### EN-029: Documentation Compliance (4 tasks, 9h)

| Task ID | Title | Effort | Description |
|---------|-------|--------|-------------|
| TASK-412 | Add L2 section | 3h | Add "L2 Architect" perspective to PLAYBOOK.md |
| TASK-413 | Create anti-patterns | 3h | Create anti-pattern catalog with 4+ anti-patterns |
| TASK-414 | Declare pattern refs | 2h | Add explicit pattern declarations (PAT-xxx) |
| TASK-415 | Add constraints section | 1h | Document constraint violations and consequences |

**Blocked By:** EN-028 (SKILL.md sections inform PLAYBOOK structure)
**Quality Gate:** ps-critic validates PLAYBOOK.md against PAT-PLAYBOOK-001

### EN-030: Documentation Polish (3 tasks, 5h)

| Task ID | Title | Effort | Description |
|---------|-------|--------|-------------|
| TASK-416 | Add tool examples | 2h | Add concrete tool invocation examples |
| TASK-417 | Add design rationale | 2h | Add design rationale to RUNBOOK.md |
| TASK-418 | Add cross-skill refs | 1h | Add cross-skill integration examples |

**Blocked By:** EN-029 (documentation structure must be complete)
**Quality Gate:** ps-critic final validation (threshold: 0.95)

### EN-031: Model Selection Capability (6 tasks, 34h) - PARALLEL TRACK

| Task ID | Title | Effort | Description |
|---------|-------|--------|-------------|
| TASK-419 | Validate Task tool model | 2h | Confirm Task tool model parameter works |
| TASK-420 | Add CLI model params | 8h | Add --model-* CLI parameters |
| TASK-421 | Update SKILL.md docs | 4h | Document model configuration |
| TASK-422 | Update agent definitions | 4h | Add model override capability to agents |
| TASK-423 | Implement profiles | 8h | Implement economy/balanced/quality profiles |
| TASK-424 | Integration testing | 8h | Test with different model combinations |

**Blocked By:** NONE (runs parallel to Track A)
**Quality Gate:** ps-critic validates implementation against requirements

---

## Execution Strategy

### Parallel Execution

```
Day 1-2:  Start BOTH tracks simultaneously
          ├── Track A: EN-027 tasks (TASK-400 through TASK-406)
          └── Track B: TASK-419 (validate Task tool model param)

Day 2-3:  Continue parallel
          ├── Track A: EN-027 completion + ps-critic gate
          └── Track B: TASK-420, TASK-421 (CLI + docs)

Day 3-4:  Continue parallel
          ├── Track A: EN-028 tasks (TASK-407 through TASK-411)
          └── Track B: TASK-422, TASK-423 (agent defs + profiles)

Day 4-5:  Continue parallel
          ├── Track A: EN-029 tasks (TASK-412 through TASK-415)
          └── Track B: TASK-424 (integration testing)

Day 5-6:  Track A completion
          ├── Track A: EN-030 tasks (TASK-416 through TASK-418)
          └── Track B: ps-critic validation

Day 6:    Final quality gate + workflow complete
```

**Efficiency Gain:** ~4-6 days parallel vs ~8 days sequential (25-40% improvement)

### Cross-Pollination Points

| Point | Trigger | Information Flow |
|-------|---------|------------------|
| CP-1 | TASK-419 complete | If Task tool model param works → informs agent definition updates |
| CP-2 | EN-027 complete | Agent YAML schema patterns → inform TASK-422 structure |
| CP-3 | TASK-420 complete | CLI parameter design → inform SKILL.md documentation |

---

## Quality Gates (ps-critic)

### Gate Protocol

Each enabler completion triggers a ps-critic quality gate:

```
┌────────────────────────────────────────────────────────────────┐
│                    ps-critic QUALITY GATE                      │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  INPUT:  Enabler deliverables (modified files)                 │
│  CRITERIA: Compliance checklist from work-026-e-003            │
│  THRESHOLD: >= 0.90 (0.95 for EN-030 final polish)            │
│                                                                │
│  PASS → Proceed to next enabler                                │
│  FAIL → Iterate (max 3 attempts) → Escalate if still failing  │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### Gate Criteria by Enabler

| Gate | Enabler | Threshold | Criteria Source |
|------|---------|-----------|-----------------|
| G-027 | EN-027 | 0.90 | Agent Compliance Checklist (A-001 through A-043) |
| G-028 | EN-028 | 0.90 | SKILL.md Compliance Checklist (S-001 through S-051) |
| G-029 | EN-029 | 0.90 | PLAYBOOK.md Triple-Lens Checklist |
| G-030 | EN-030 | 0.95 | Final polish - no regressions, integration complete |
| G-031 | EN-031 | 0.90 | Model selection requirements from EN-031 AC |
| G-FINAL | All | 0.90 | Aggregate compliance >= 95%, all 25 tasks complete |

---

## Checkpoints

| ID | Trigger | Recovery Point | Artifacts to Preserve |
|----|---------|----------------|----------------------|
| CP-001 | EN-027 complete | Pre-YAML state | Backup of original agent .md files |
| CP-002 | EN-028 complete | SKILL.md stable | SKILL.md backup |
| CP-003 | EN-029 complete | Docs structure done | PLAYBOOK.md, RUNBOOK.md backups |
| CP-004 | EN-030 complete | Track A done | All documentation |
| CP-005 | TASK-419 complete | Model validation done | Test results |
| CP-006 | EN-031 complete | Track B done | CLI + profiles |
| CP-FINAL | All complete | Workflow done | Full artifact set |

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Compliance Score | >= 95% | Checklist completion from work-026-e-003 |
| Tasks Complete | 25/25 | All TASK-4xx files marked complete |
| Quality Gates Passed | 6/6 | All ps-critic gates >= threshold |
| Parallel Efficiency | >= 25% | Days saved vs pure sequential |
| Backward Compatibility | 100% | Existing pipeline still works |

---

## Risk Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| TASK-419 fails (model param broken) | Medium | Critical | Early validation; fallback to hardcoded if needed |
| ps-critic rejection loop | Low | Medium | Max 3 iterations; escalate with documented gaps |
| Track A blocks Track B | Low | Low | Tracks are independent by design |
| Breaking existing pipelines | Medium | High | Checkpoint before each enabler; test after each |

---

## References

- [FEAT-005 Feature Definition](../FEAT-005-skill-compliance.md)
- [EN-027 Agent Definition Compliance](../EN-027-agent-definition-compliance/EN-027-agent-definition-compliance.md)
- [EN-028 SKILL.md Compliance](../EN-028-skill-md-compliance/EN-028-skill-md-compliance.md)
- [EN-029 Documentation Compliance](../EN-029-documentation-compliance/EN-029-documentation-compliance.md)
- [EN-030 Documentation Polish](../EN-030-documentation-polish/EN-030-documentation-polish.md)
- [EN-031 Model Selection](../EN-031-model-selection-capability/EN-031-model-selection-capability.md)
- [work-026-e-002 Gap Analysis](../../../../../docs/analysis/work-026-e-002-transcript-skill-gap-analysis.md)
- [work-026-e-003 Compliance Framework](../../../../../docs/synthesis/work-026-e-003-jerry-skill-compliance-framework.md)

---

*Orchestration Plan Version: 2.0.0*
*Status: Aligned with existing task files*
*Constitutional Compliance: P-002, P-003*
*Created: 2026-01-30*
