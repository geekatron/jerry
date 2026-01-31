# Orchestration Plan: FEAT-005 Skill Compliance

> **Workflow ID:** feat-005-compliance-20260130-001
> **Version:** 1.0.0
> **Status:** ACTIVE
> **Created:** 2026-01-30T22:00:00Z
> **Framework:** Jerry Orchestration v2.1.0

---

## Executive Summary (L0)

This orchestration plan coordinates **parallel execution** of FEAT-005 skill compliance work using agents from `/problem-solving` and `/nasa-se` skills. The plan implements:

- **Two parallel tracks** running simultaneously
- **Adversarial critic feedback loops** on each deliverable (quality gates)
- **Cross-pollination barriers** where outputs inform other tracks
- **Estimated 4-6 days** total (vs 8+ days sequential)

---

## Workflow Diagram

```
FEAT-005 SKILL COMPLIANCE ORCHESTRATION
═══════════════════════════════════════

                            ┌────────────────────────────────────────┐
                            │           WORKFLOW START               │
                            │    feat-005-compliance-20260130-001    │
                            └────────────────────┬───────────────────┘
                                                 │
                     ┌───────────────────────────┴───────────────────────────┐
                     │                                                       │
                     ▼                                                       ▼
    ╔════════════════════════════════════╗          ╔════════════════════════════════════╗
    ║     TRACK A: SEQUENTIAL CHAIN      ║          ║    TRACK B: MODEL SELECTION        ║
    ║         (ps pipeline)              ║          ║        (nse pipeline)              ║
    ║     Alias: "compliance"            ║          ║     Alias: "model-sel"             ║
    ╚════════════════════════════════════╝          ╚════════════════════════════════════╝
                     │                                                       │
                     ▼                                                       ▼
    ┌────────────────────────────────────┐          ┌────────────────────────────────────┐
    │  PHASE 1: EN-027 Agent Compliance  │          │  PHASE 1: Requirements Analysis    │
    │  ─────────────────────────────────│          │  ─────────────────────────────────│
    │  ps-researcher → Gap analysis      │          │  nse-requirements → SHALLs         │
    │  ps-analyst → Impact assessment    │          │  nse-architecture → Design         │
    │  ps-architect → Schema design      │          │  ps-researcher → Industry scan     │
    │                                    │          │                                    │
    │  ┌──────────────────────────────┐ │          │  ┌──────────────────────────────┐ │
    │  │    🔄 ps-critic GATE         │ │          │  │    🔄 ps-critic GATE         │ │
    │  │    Score >= 0.90 required    │ │          │  │    Score >= 0.90 required    │ │
    │  └──────────────────────────────┘ │          │  └──────────────────────────────┘ │
    │  Effort: 10h | 5 Tasks            │          │  Effort: 12h | 3 Tasks            │
    └────────────────────┬───────────────┘          └────────────────────┬───────────────┘
                         │                                               │
                         └─────────────────────┬─────────────────────────┘
                                               │
                                               ▼
                         ╔═════════════════════════════════════════════════╗
                         ║               BARRIER 1                          ║
                         ║    Cross-Pollination: Schema → Requirements     ║
                         ║    compliance → model-sel: YAML schema inform   ║
                         ║    model-sel → compliance: API patterns inform  ║
                         ╚═════════════════════════════════════════════════╝
                                               │
                     ┌─────────────────────────┴─────────────────────────┐
                     │                                                   │
                     ▼                                                   ▼
    ┌────────────────────────────────────┐          ┌────────────────────────────────────┐
    │  PHASE 2: EN-028 SKILL.md Update   │          │  PHASE 2: Design & Implementation  │
    │  ─────────────────────────────────│          │  ─────────────────────────────────│
    │  ps-analyst → Section mapping      │          │  ps-architect → CLI ADR            │
    │  ps-architect → ADR compliance     │          │  nse-integration → Agent updates   │
    │  ps-synthesizer → Pattern merge    │          │  ps-validator → Constraint check   │
    │                                    │          │                                    │
    │  ┌──────────────────────────────┐ │          │  ┌──────────────────────────────┐ │
    │  │    🔄 ps-critic GATE         │ │          │  │    🔄 nse-qa GATE            │ │
    │  │    Score >= 0.90 required    │ │          │  │    NASA V&V verification     │ │
    │  └──────────────────────────────┘ │          │  └──────────────────────────────┘ │
    │  Effort: 9h | 5 Tasks             │          │  Effort: 16h | 4 Tasks            │
    └────────────────────┬───────────────┘          └────────────────────┬───────────────┘
                         │                                               │
                         └─────────────────────┬─────────────────────────┘
                                               │
                                               ▼
                         ╔═════════════════════════════════════════════════╗
                         ║               BARRIER 2                          ║
                         ║    Cross-Pollination: Documentation Ready       ║
                         ║    compliance → model-sel: SKILL.md patterns    ║
                         ║    model-sel → compliance: Model config format  ║
                         ╚═════════════════════════════════════════════════╝
                                               │
                     ┌─────────────────────────┴─────────────────────────┐
                     │                                                   │
                     ▼                                                   ▼
    ┌────────────────────────────────────┐          ┌────────────────────────────────────┐
    │  PHASE 3: EN-029 Documentation     │          │  PHASE 3: Testing & Integration    │
    │  ─────────────────────────────────│          │  ─────────────────────────────────│
    │  ps-researcher → Pattern library   │          │  nse-verification → Test matrix    │
    │  ps-synthesizer → Anti-pattern doc │          │  ps-reviewer → Code review         │
    │  ps-validator → Trace verify       │          │  nse-qa → Validation               │
    │                                    │          │                                    │
    │  ┌──────────────────────────────┐ │          │  ┌──────────────────────────────┐ │
    │  │    🔄 ps-critic GATE         │ │          │  │    🔄 ps-critic GATE         │ │
    │  │    Score >= 0.90 required    │ │          │  │    Score >= 0.90 required    │ │
    │  └──────────────────────────────┘ │          │  └──────────────────────────────┘ │
    │  Effort: 9h | 5 Tasks             │          │  Effort: 16h | 4 Tasks            │
    └────────────────────┬───────────────┘          └────────────────────┬───────────────┘
                         │                                               │
                         └─────────────────────┬─────────────────────────┘
                                               │
                                               ▼
                         ╔═════════════════════════════════════════════════╗
                         ║               BARRIER 3                          ║
                         ║    Cross-Pollination: Quality Gates Passed      ║
                         ║    Both tracks: ps-critic >= 0.90              ║
                         ╚═════════════════════════════════════════════════╝
                                               │
                     ┌─────────────────────────┴─────────────────────────┐
                     │                                                   │
                     ▼                                                   ▼
    ┌────────────────────────────────────┐          ┌────────────────────────────────────┐
    │  PHASE 4: EN-030 Polish (Optional) │          │  PHASE 4: Documentation            │
    │  ─────────────────────────────────│          │  ─────────────────────────────────│
    │  ps-reviewer → Final review        │          │  ps-synthesizer → User guide       │
    │  ps-synthesizer → Integration doc  │          │  nse-reporter → V&V report         │
    │                                    │          │                                    │
    │  ┌──────────────────────────────┐ │          │  ┌──────────────────────────────┐ │
    │  │    🔄 ps-critic GATE         │ │          │  │    🔄 ps-critic GATE         │ │
    │  │    Score >= 0.95 (final)     │ │          │  │    Score >= 0.90 required    │ │
    │  └──────────────────────────────┘ │          │  └──────────────────────────────┘ │
    │  Effort: 5h | 5 Tasks             │          │  Effort: 8h | 3 Tasks             │
    └────────────────────┬───────────────┘          └────────────────────┬───────────────┘
                         │                                               │
                         └─────────────────────┬─────────────────────────┘
                                               │
                                               ▼
                         ┌─────────────────────────────────────────────────┐
                         │              SYNTHESIS PHASE                    │
                         │  ─────────────────────────────────────────────│
                         │  ps-synthesizer → Final compliance synthesis    │
                         │  ps-reporter → Feature completion report        │
                         │  nse-reporter → NASA SE compliance report       │
                         │                                                 │
                         │  ┌─────────────────────────────────────────┐   │
                         │  │    🔄 FINAL ps-critic GATE              │   │
                         │  │    Aggregate score >= 0.90 required     │   │
                         │  └─────────────────────────────────────────┘   │
                         └────────────────────┬────────────────────────────┘
                                              │
                                              ▼
                         ┌─────────────────────────────────────────────────┐
                         │              WORKFLOW COMPLETE                  │
                         │    FEAT-005 at 95%+ Compliance                  │
                         └─────────────────────────────────────────────────┘

LEGEND:
═══════
┌────┐  Phase/work unit
║    ║  Barrier (sync point)
🔄     Adversarial critic feedback loop
→      Agent invocation
```

---

## Agent Mapping (L1)

### Problem-Solving Agents Used

| Agent | Role in FEAT-005 | Phases |
|-------|------------------|--------|
| `ps-researcher` | Research patterns, industry best practices, gap identification | 1, 3 |
| `ps-analyst` | Impact assessment, section mapping, constraint analysis | 1, 2 |
| `ps-architect` | Schema design, ADR creation, decision documentation | 1, 2 |
| `ps-critic` | **ADVERSARIAL GATE** - Quality score >= 0.90 on every deliverable | ALL |
| `ps-validator` | Constraint verification, traceability, compliance check | 2, 3 |
| `ps-synthesizer` | Pattern merge, anti-pattern docs, integration synthesis | 2, 3, 4, FINAL |
| `ps-reviewer` | Code review, documentation review, final polish | 3, 4 |
| `ps-reporter` | Status reports, completion metrics | FINAL |

### NASA SE Agents Used

| Agent | Role in FEAT-005 | Phases |
|-------|------------------|--------|
| `nse-requirements` | SHALL statements, model selection requirements | 1 (Track B) |
| `nse-architecture` | Technical design, interface specifications | 1 (Track B) |
| `nse-integration` | Agent updates, system integration | 2 (Track B) |
| `nse-verification` | Test matrix, V&V planning | 3 (Track B) |
| `nse-qa` | **ADVERSARIAL GATE** - NASA-grade V&V validation | 2, 3 (Track B) |
| `nse-reporter` | V&V completion report, compliance summary | 4, FINAL |

### Agent Invocation Pattern

```
MAIN CONTEXT (Claude) ← Orchestrator
    │
    ├──► Track A Workers (Sequential Chain)
    │    ├──► ps-researcher
    │    ├──► ps-analyst
    │    ├──► ps-architect
    │    ├──► ps-critic (gate)
    │    ├──► ps-synthesizer
    │    ├──► ps-validator
    │    └──► ps-reviewer
    │
    ├──► Track B Workers (Model Selection)
    │    ├──► nse-requirements
    │    ├──► nse-architecture
    │    ├──► ps-researcher (shared)
    │    ├──► nse-integration
    │    ├──► nse-verification
    │    └──► nse-qa (gate)
    │
    └──► Synthesis Workers
         ├──► ps-synthesizer
         ├──► ps-reporter
         └──► nse-reporter

COMPLIANCE: P-003 - Each is a WORKER. None spawn subagents.
```

---

## Adversarial Critic Feedback Loops (L2)

### Quality Gate Protocol

Every phase output goes through an adversarial critic feedback loop:

```
┌───────────────────────────────────────────────────────────────────────┐
│                 ADVERSARIAL CRITIC FEEDBACK LOOP                      │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│    ┌─────────────┐     ┌─────────────┐     ┌─────────────────────┐  │
│    │  DELIVERABLE │────►│  ps-critic  │────►│  SCORE >= 0.90?     │  │
│    │  (Phase N)   │     │  Evaluation │     │                     │  │
│    └─────────────┘     └─────────────┘     └──────────┬──────────┘  │
│                                                        │             │
│                                            ┌───────────┴───────────┐ │
│                                            │                       │ │
│                                     ┌──────▼──────┐         ┌──────▼──────┐
│                                     │    YES      │         │     NO      │
│                                     │  PROCEED    │         │  ITERATE    │
│                                     └─────────────┘         └──────┬──────┘
│                                                                    │     │
│                    ┌───────────────────────────────────────────────┘     │
│                    │                                                     │
│    ┌───────────────▼───────────────┐                                    │
│    │  REVISION CYCLE               │◄───────────────────────────────────┘
│    │  1. Review critique findings  │
│    │  2. Address specific issues   │
│    │  3. Re-submit to ps-critic    │
│    │  Max iterations: 3            │
│    └───────────────────────────────┘
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

### Critic Criteria per Phase

| Phase | Deliverables Evaluated | Critic Criteria | Threshold |
|-------|------------------------|-----------------|-----------|
| 1A | Agent YAML frontmatter | PAT-AGENT-001 compliance, 8 required sections | >= 0.90 |
| 1B | Requirements doc | SHALL clarity, traceability, completeness | >= 0.90 |
| 2A | SKILL.md updates | PAT-SKILL-001 compliance, 3 invocation methods | >= 0.90 |
| 2B | CLI ADR + agent updates | ADR quality, code integration | >= 0.90 |
| 3A | PLAYBOOK.md + anti-patterns | Triple-lens format, diagram quality | >= 0.90 |
| 3B | Test matrix + validation | Coverage, NASA V&V rigor | >= 0.90 |
| 4A | Final polish | Integration, no regressions | >= 0.95 |
| 4B | User documentation | Completeness, clarity | >= 0.90 |
| FINAL | Aggregate synthesis | Overall compliance >= 95%, all gaps closed | >= 0.90 |

### Escalation Protocol

```
IF ps-critic score < 0.90 after 3 iterations:
    1. Log as IMPEDIMENT
    2. Escalate to user for guidance
    3. Document in quality-review.md
    4. May proceed with documented exception if approved
```

---

## Cross-Pollination Points (L2)

### Barrier 1: Schema → Requirements

```yaml
barrier_1:
  trigger: Phase 1 complete in both tracks
  compliance_to_model_sel:
    - Agent YAML schema patterns
    - Metadata field requirements
    - Validation rules discovered
  model_sel_to_compliance:
    - API patterns from industry research
    - Model configuration approaches
    - CLI parameter conventions
```

### Barrier 2: Documentation Ready

```yaml
barrier_2:
  trigger: Phase 2 complete in both tracks
  compliance_to_model_sel:
    - SKILL.md section structure
    - State passing schema format
    - Agent invocation patterns
  model_sel_to_compliance:
    - Model selection CLI syntax
    - Configuration file format
    - Default model decisions
```

### Barrier 3: Quality Gates Passed

```yaml
barrier_3:
  trigger: Phase 3 complete with ps-critic >= 0.90
  compliance_to_model_sel:
    - Anti-pattern catalog (what to avoid)
    - Traceability matrix format
  model_sel_to_compliance:
    - Test matrix patterns
    - V&V checklist items
```

---

## Task-to-Agent Mapping

### Track A: Sequential Chain (EN-027 → EN-030)

| Enabler | Task ID | Task Title | Primary Agent | Critic Gate |
|---------|---------|------------|---------------|-------------|
| **EN-027** | TASK-134 | Analyze PAT-AGENT-001 | ps-researcher | - |
| | TASK-135 | Update ts-parser.md | ps-architect | - |
| | TASK-136 | Update ts-extractor.md | ps-architect | - |
| | TASK-137 | Update ts-formatter.md | ps-architect | - |
| | TASK-138 | Validate agent compliance | ps-critic | ✅ Gate 1A |
| **EN-028** | TASK-139 | Analyze PAT-SKILL-001 | ps-researcher | - |
| | TASK-140 | Add invocation section | ps-analyst | - |
| | TASK-141 | Add state passing schema | ps-architect | - |
| | TASK-142 | Add session context | ps-synthesizer | - |
| | TASK-143 | Validate SKILL.md | ps-critic | ✅ Gate 2A |
| **EN-029** | TASK-144 | Analyze PAT-PLAYBOOK-001 | ps-researcher | - |
| | TASK-145 | Add anti-pattern catalog | ps-synthesizer | - |
| | TASK-146 | Add triple-lens format | ps-analyst | - |
| | TASK-147 | Add ASCII diagrams | ps-architect | - |
| | TASK-148 | Validate documentation | ps-critic | ✅ Gate 3A |
| **EN-030** | TASK-149 | Section 6 improvements | ps-reviewer | - |
| | TASK-150 | Runbook examples | ps-synthesizer | - |
| | TASK-151 | Cross-references | ps-validator | - |
| | TASK-152 | Index generation | ps-analyst | - |
| | TASK-153 | Final review | ps-critic | ✅ Gate 4A |

### Track B: Model Selection (EN-031)

| Task ID | Task Title | Primary Agent | Critic Gate |
|---------|------------|---------------|-------------|
| TASK-154 | Requirements analysis | nse-requirements | - |
| TASK-155 | Architecture design | nse-architecture | - |
| TASK-156 | Industry pattern scan | ps-researcher | - |
| | | | ✅ Gate 1B (ps-critic) |
| TASK-157 | CLI ADR creation | ps-architect | - |
| TASK-158 | Agent definition updates | nse-integration | - |
| TASK-159 | SKILL.md parameters | ps-synthesizer | - |
| TASK-160 | Constraint validation | ps-validator | - |
| | | | ✅ Gate 2B (nse-qa) |
| TASK-161 | Test matrix creation | nse-verification | - |
| TASK-162 | Unit test implementation | ps-reviewer | - |
| TASK-163 | Integration testing | nse-qa | - |
| TASK-164 | V&V validation | ps-critic | ✅ Gate 3B |
| TASK-165 | User guide creation | ps-synthesizer | - |
| TASK-166 | V&V report | nse-reporter | - |
| TASK-167 | Final validation | ps-critic | ✅ Gate 4B |

---

## Execution Schedule

### Parallel Execution Timeline

```
Day 1-2:  Phase 1 (Both Tracks)
          ├── Track A: EN-027 Agent Compliance (TASK-134 to TASK-138)
          └── Track B: Requirements (TASK-154 to TASK-156)
          └── BARRIER 1 at end of Day 2

Day 2-3:  Phase 2 (Both Tracks)
          ├── Track A: EN-028 SKILL.md (TASK-139 to TASK-143)
          └── Track B: Design & Impl (TASK-157 to TASK-160)
          └── BARRIER 2 at end of Day 3

Day 3-4:  Phase 3 (Both Tracks)
          ├── Track A: EN-029 Documentation (TASK-144 to TASK-148)
          └── Track B: Testing (TASK-161 to TASK-164)
          └── BARRIER 3 at end of Day 4

Day 4-5:  Phase 4 (Both Tracks)
          ├── Track A: EN-030 Polish (TASK-149 to TASK-153)
          └── Track B: Documentation (TASK-165 to TASK-167)

Day 5-6:  Synthesis Phase
          └── Final integration, reports, compliance verification

Total: ~6 days parallel (vs 8+ days sequential)
       ~15-20% efficiency gain through parallelization
```

---

## Checkpoints

| Checkpoint | Trigger | Recovery Point | Artifacts |
|------------|---------|----------------|-----------|
| CP-001 | Phase 1 complete | Pre-YAML changes | Agent analysis docs |
| CP-002 | Barrier 1 complete | Cross-pollination done | Schema docs |
| CP-003 | Phase 2 complete | SKILL.md stable | SKILL.md backup |
| CP-004 | Barrier 2 complete | Documentation ready | All MD files |
| CP-005 | Phase 3 complete | Tests written | Test matrix |
| CP-006 | Barrier 3 complete | Quality verified | Critic reports |
| CP-007 | Phase 4 complete | Polish done | Final docs |
| CP-FINAL | Workflow complete | All deliverables | Synthesis report |

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Compliance Score | >= 95% | Checklist completion |
| ps-critic Gates Passed | 100% | All gates >= 0.90 |
| Parallel Efficiency | >= 15% | Days saved vs sequential |
| Gap Closure | 30/30 | All gaps from work-026-e-002 |
| Backward Compatibility | 100% | No regression in existing pipelines |

---

## Risk Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Critic rejection loop | Medium | High | Max 3 iterations, escalation protocol |
| Cross-pollination delay | Low | Medium | Async artifact sharing |
| Model selection complexity | High | High | Parallel track independence |
| Schema breaking changes | Medium | High | Checkpoint before each phase |

---

## Related Documents

- [FEAT-005 Feature Definition](../../work/EPIC-001-transcript-skill/FEAT-005-skill-compliance/FEAT-005-skill-compliance.md)
- [work-026-e-002 Gap Analysis](../../docs/analysis/work-026-e-002-transcript-skill-gap-analysis.md)
- [work-026-e-003 Compliance Framework](../../docs/synthesis/work-026-e-003-jerry-skill-compliance-framework.md)
- [Problem-Solving SKILL.md](../../../skills/problem-solving/SKILL.md)
- [NASA-SE SKILL.md](../../../skills/nasa-se/SKILL.md)
- [Orchestration SKILL.md](../../../skills/orchestration/SKILL.md)

---

*Orchestration Plan Version: 1.0.0*
*Constitutional Compliance: Jerry Constitution v1.0 (P-002, P-003)*
*Created: 2026-01-30T22:00:00Z*
