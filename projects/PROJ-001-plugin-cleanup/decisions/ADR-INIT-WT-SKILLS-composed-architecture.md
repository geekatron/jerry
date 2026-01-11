# ADR-INIT-WT-SKILLS: Composed Architecture for Worktracker Skills

**PS ID:** init-wt-skills
**Entry ID:** e-008
**Status:** ACCEPTED
**Date:** 2026-01-11
**Decision Makers:** INIT-WT-SKILLS orchestration, ps-architect agent equivalent

---

## Context

The Jerry Framework has two worktracker skills (`skills/worktracker/` and `skills/worktracker-decomposition/`) that lack agent infrastructure. Research revealed a significant capability asymmetry:

| Metric | problem-solving | worktracker (both) | Gap |
|--------|-----------------|-------------------|-----|
| Total lines | 5,129 | 776 | -4,353 lines |
| Agents | 8 | 0 | -8 agents |
| Playbooks | 1 | 0 | -1 file |
| Orchestration docs | 1 | 0 | -1 file |

The question: **How should we add agent capabilities to worktracker skills?**

Three architectural approaches were evaluated as part of the INIT-WT-SKILLS research initiative.

---

## Decision

**ADOPT OPTION C: COMPOSED ARCHITECTURE**

Create thin wt-coordinator agent that routes to existing ps-* agents, injecting worktracker-specific domain context via adapters.

```
skills/worktracker/
├── SKILL.md              # Entry point
├── agents/
│   ├── wt-coordinator.md # Routes to ps-* agents with WT context
│   ├── wt-context.md     # Context injection for ps-* agents
│   └── wt-adapters/
│       ├── ps-analyst.yaml    # ps-analyst + WT domain
│       ├── ps-reporter.yaml   # ps-reporter + WT domain
│       └── ps-validator.yaml  # ps-validator + WT domain
└── scripts/
```

**Architecture Pattern:**
```
User -> wt-coordinator -> ps-analyst (1 level = P-003 compliant)
```

---

## Rationale

### Quantitative Scoring (from e-006)

| Criterion (Weight) | Option A: Monolithic | Option B: Cloned | Option C: Composed |
|--------------------|---------------------|------------------|-------------------|
| Complexity (20%) | 6 | 4 | 7 |
| Reusability (25%) | 2 | 3 | **9** |
| Context Efficiency (25%) | 3 | 6 | **9** |
| Standards Alignment (15%) | 3 | 5 | **9** |
| Constitution Compliance (15%) | 7 | 6 | **9** |
| **WEIGHTED TOTAL** | **3.95** | **4.70** | **8.60** |

Option C scored **83% higher** than Option B and **118% higher** than Option A.

### Key Differentiators

1. **Reusability (9 vs 3):** ps-* agents serve ALL skills, not just worktracker. Future skills (architecture, security) can create thin adapters without duplicating agent code.

2. **Context Efficiency (9 vs 3):** Composed architecture loads ~3,000 tokens (ps-analyst + wt-context) vs ~12,000 tokens (entire monolithic skill). This directly addresses context rot.

3. **Standards Alignment (9 vs 3):** Matches industry best practices:
   - Anthropic Agent Skills: "modular, composable agents"
   - Google ADK: Coordinator/Specialist pattern
   - OpenAI: Agent-as-Tool pattern

4. **P-003 Compliance (9 vs 7):** wt-coordinator is the ONLY agent level. Workers (ps-*) cannot spawn sub-workers, ensuring Hard enforcement of single-level nesting.

---

## Consequences

### Positive

1. **Immediate Benefits:**
   - 60%+ code reuse from ps-* agents
   - 50%+ context token reduction vs monolithic
   - ps-* improvements automatically benefit worktracker

2. **Long-Term Benefits:**
   - New skills adopt agents in 1-2 days (not 1-2 weeks)
   - Constitutional compliance enforced at agent layer
   - Single methodology codebase to maintain

3. **Framework Evolution:**
   - Establishes PAT-008: Composed Agent Architecture as Jerry standard
   - Creates foundation for skills/architecture/, skills/security/, etc.

### Negative

1. **Adapter Maintenance:**
   - When ps-* agents change, adapters may need updates
   - Mitigation: Adapters reference by path; changes are additive

2. **Coordination Complexity:**
   - wt-coordinator must correctly inject domain context
   - Mitigation: Clear adapter schema, unit tests

3. **Debugging Indirection:**
   - Issues span two files (adapter + ps-* agent)
   - Mitigation: Explicit state management in adapter YAML

---

## Alternatives Considered

### Option A: Monolithic Skill

**Approach:** Embed all agent behaviors directly in `SKILL.md`.

**Rejected Because:**
- Context efficiency score: 3/10 (loads 12,000+ tokens for any task)
- Reusability score: 2/10 (all intelligence locked in one skill)
- Becomes "god file" as complexity grows
- Violates progressive disclosure pattern (PAT-003)

### Option B: Cloned Hierarchy

**Approach:** Create parallel wt-* agents mirroring ps-* structure.

**Rejected Because:**
- Reusability score: 3/10 (agents are worktracker-specific)
- Creates "fork drift" as wt-* diverges from ps-*
- Doubles maintenance burden (8 ps-* + 5 wt-* agents)
- If architecture skill needs agents, must create arch-* set too

---

## Compliance

### P-003: No Recursive Subagents (HARD - Critical)

**Status:** COMPLIANT

The composed architecture is explicitly designed for single-level nesting:

```
orchestrator (wt-coordinator) -> worker (ps-analyst)
                              -> worker (ps-reporter)
                              -> worker (ps-validator)
```

ps-* agents are terminal workers. They do NOT spawn subagents.

**Verification Method:** Behavioral tests (BHV-003) will validate:
- wt-coordinator invokes ps-* agents directly
- ps-* agents do not invoke other agents
- Maximum call depth is exactly 2 (user -> wt-coordinator -> ps-*)

### P-002: File Persistence (MEDIUM)

**Status:** COMPLIANT

All ps-* agents persist outputs to filesystem. wt-adapters specify output locations:
```yaml
output_location: "projects/${JERRY_PROJECT}/analysis/wt-{entry_id}.md"
```

### P-004: Explicit Provenance (SOFT)

**Status:** COMPLIANT

Adapters inject domain context with explicit provenance:
```yaml
domain_context:
  source: "skills/worktracker/agents/wt-adapters/ps-analyst.yaml"
  entities: [WorkItem, Epic, Story, Task, Bug, Spike]
```

### Other Principles

| Principle | Compliance | Notes |
|-----------|------------|-------|
| P-001 (Truth) | Compliant | ps-* agents cite sources |
| P-010 (Task Tracking) | Compliant | wt-coordinator updates WORKTRACKER |
| P-011 (Evidence) | Compliant | Research-backed decision |
| P-022 (No Deception) | Compliant | Gaps and risks documented |

---

## Implementation Notes

### Phase 1: Foundation (13 hours)
- Create WT_AGENT_TEMPLATE.md following PS_AGENT_TEMPLATE.md
- Create PLAYBOOK.md for both worktracker skills
- Extract inline templates from SKILL.md

### Phase 2: Core Agents (14 hours)
- Implement wt-coordinator.md
- Create adapters for ps-analyst, ps-reporter, ps-validator, ps-synthesizer

### Phase 3: Integration (16 hours)
- Create ORCHESTRATION.md
- Update @worktracker commands
- Implement behavioral tests for P-003
- Add compaction triggers

**Total Effort:** ~43 hours (~5.5 person-days)

---

## References

| Document | Entry ID | Contribution |
|----------|----------|--------------|
| Trade-off Analysis | e-006 | Scoring methodology and option evaluation |
| Unified Synthesis | e-007 | Implementation roadmap and recommendations |
| PS Agent Portfolio | e-001 | 8-agent structure reference |
| Industry Standards | e-002 | Anthropic/Google/OpenAI patterns |
| Context Rot Patterns | e-003 | Token reduction strategies |
| Gap Analysis | e-005 | Priority ranking and effort estimates |

---

*Generated as part of INIT-WT-SKILLS orchestration*
*Constitutional Compliance: Jerry Constitution v1.0*
*Decision accepted: 2026-01-11*
