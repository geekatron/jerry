---
id: sao-init-008
title: "Agent & Skill Enhancement via Self-Orchestration"
type: initiative_index
status: IN_PROGRESS
parent: "../../WORKTRACKER.md"
children:
  - wi-sao-046.md
  - wi-sao-047.md
  - wi-sao-048.md
  - wi-sao-049.md
  - wi-sao-050.md
  - wi-sao-051.md
  - wi-sao-052.md
  - wi-sao-053.md
  - wi-sao-054.md
  - wi-sao-055.md
  - wi-sao-056.md
  - wi-sao-057.md
  - wi-sao-058.md
  - wi-sao-059.md
  - wi-sao-060.md
  - wi-sao-061.md
  - wi-sao-062.md
  - wi-sao-063.md
  - wi-sao-064.md
  - wi-sao-065.md
  - wi-sao-066.md
  - wi-sao-067.md
related:
  - plan.md
  - ../sao-init-007-triple-lens-playbooks/_index.md
created: "2026-01-12"
last_updated: "2026-01-12"
source: "User request - Meta-improvement using own pipelines"
rationale: "Use Jerry's own orchestration patterns to systematically enhance all agent definitions, skills, and playbooks using latest authoritative sources."
work_items_total: 22
work_items_complete: 0
work_items_in_progress: 0
token_estimate: 2500
---

# SAO-INIT-008: Agent & Skill Enhancement via Self-Orchestration

> **Status:** 🔄 IN_PROGRESS (0/22 work items complete)
> **Created:** 2026-01-12
> **Detailed Plan:** [plan.md](plan.md)

---

## Rationale

Jerry has mature orchestration patterns (8 documented) and agent pipelines (ps-*, nse-*), but the agent definitions and skill documentation themselves have not been systematically enhanced using these capabilities. This initiative applies Jerry's own pipelines to improve Jerry - a meta-improvement approach.

**Key Insight:** We eat our own dog food. If our patterns work, they should improve our own documentation.

**Sources to Leverage:**
- External: Context7 (Claude Code docs), Anthropic research, NASA SE Handbook, INCOSE standards
- Internal: PROJ-001/PROJ-002 synthesis docs, 23+ research documents

---

## Strategy: 4-Phase Pipeline

```
╔═══════════════════════════════════════════════════════════════════════════════════════╗
║                    SAO-INIT-008: SELF-ORCHESTRATION PIPELINE                           ║
╠═══════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                       ║
║  PHASE 1: RESEARCH (Pattern 3 + 4: Fan-Out/Fan-In)                                   ║
║  ─────────────────────────────────────────────────                                    ║
║                                                                                       ║
║       ┌──────────────────┬──────────────────┬──────────────────┐                     ║
║       │  EXTERNAL        │  EXTERNAL        │  INTERNAL        │                     ║
║       │  Context7 +      │  NASA/INCOSE     │  PROJ-001/002    │                     ║
║       │  Anthropic       │  Standards       │  Knowledge       │                     ║
║       └────────┬─────────┴────────┬─────────┴────────┬─────────┘                     ║
║                │                  │                  │                               ║
║                └──────────────────┼──────────────────┘                               ║
║                                   │                                                   ║
║                          ╔════════▼════════╗                                         ║
║                          ║  SYNC BARRIER   ║                                         ║
║                          ╚════════╤════════╝                                         ║
║                                   │                                                   ║
║                          ┌────────▼────────┐                                         ║
║                          │  SYNTHESIZE     │                                         ║
║                          │  RESEARCH       │                                         ║
║                          └─────────────────┘                                         ║
║                                                                                       ║
║  PHASE 2: ANALYSIS (Pattern 2: Sequential + Pattern 7: Review Gate)                  ║
║  ───────────────────────────────────────────────────────────────────                 ║
║                                                                                       ║
║       ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                         ║
║       │ GAP         │───►│ COMPLIANCE  │───►│ CREATE      │                         ║
║       │ ANALYSIS    │    │ CHECK       │    │ RUBRIC      │                         ║
║       └─────────────┘    └─────────────┘    └─────────────┘                         ║
║                                                                                       ║
║  PHASE 3: ENHANCEMENT (Pattern 8: Generator-Critic Loop)                             ║
║  ───────────────────────────────────────────────────────                             ║
║                                                                                       ║
║       P0 AGENTS              P1 AGENTS              P2 AGENTS                        ║
║       ─────────              ─────────              ─────────                        ║
║       ┌────────────┐         ┌────────────┐         ┌────────────┐                  ║
║       │orchestrator│         │ps-architect│         │ps-validator│                  ║
║       │ps-researcher│        │ps-synthesizr│        │nse-qa     │                  ║
║       │ps-analyst  │         │nse-require │         │nse-risk   │                  ║
║       │ps-critic   │         │nse-reviewer│         │orch-*     │                  ║
║       └─────┬──────┘         └─────┬──────┘         └─────┬──────┘                  ║
║             │                      │                      │                          ║
║             ▼                      ▼                      ▼                          ║
║       [Gen-Critic Loop]     [Gen-Critic Loop]     [Gen-Critic Loop]                 ║
║       max_iter=3            max_iter=3            max_iter=3                        ║
║       threshold=0.85        threshold=0.85        threshold=0.85                    ║
║                                                                                       ║
║       + SKILLS & PLAYBOOKS + PATTERN DOCS                                            ║
║                                                                                       ║
║  PHASE 4: VALIDATION (Pattern 7: Review Gate + Pattern 5: Cross-Pollinated)          ║
║  ──────────────────────────────────────────────────────────────────────             ║
║                                                                                       ║
║       ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                         ║
║       │ BEFORE/     │───►│ RUBRIC      │───►│ FINAL       │                         ║
║       │ AFTER TEST  │    │ SCORING     │    │ REVIEW      │                         ║
║       └─────────────┘    └─────────────┘    └─────────────┘                         ║
║                                                                                       ║
╚═══════════════════════════════════════════════════════════════════════════════════════╝
```

---

## Work Items Summary

### Phase 1: Research (4 work items)

| Work Item | Status | Priority | Description |
|-----------|--------|----------|-------------|
| WI-SAO-046 | 📋 OPEN | P1 | External research: Context7 + Anthropic docs |
| WI-SAO-047 | 📋 OPEN | P1 | External research: NASA SE Handbook + INCOSE |
| WI-SAO-048 | 📋 OPEN | P1 | Internal research: PROJ-001/002 knowledge bases |
| WI-SAO-049 | 📋 OPEN | P1 | Synthesize research findings (barrier) |

### Phase 2: Analysis (3 work items)

| Work Item | Status | Priority | Description |
|-----------|--------|----------|-------------|
| WI-SAO-050 | 📋 OPEN | P1 | Gap analysis: Current docs vs best practices |
| WI-SAO-051 | 📋 OPEN | P1 | Compliance check: NASA/Anthropic standards |
| WI-SAO-052 | 📋 OPEN | P1 | Create enhancement evaluation rubric |

### Phase 3: Enhancement - P0 Agents (4 work items)

| Work Item | Status | Priority | Description |
|-----------|--------|----------|-------------|
| WI-SAO-053 | 📋 OPEN | P0 | Enhance orchestrator agent |
| WI-SAO-054 | 📋 OPEN | P0 | Enhance ps-researcher agent |
| WI-SAO-055 | 📋 OPEN | P0 | Enhance ps-analyst agent |
| WI-SAO-056 | 📋 OPEN | P0 | Enhance ps-critic agent |

### Phase 3: Enhancement - P1 Agents (4 work items)

| Work Item | Status | Priority | Description |
|-----------|--------|----------|-------------|
| WI-SAO-057 | 📋 OPEN | P1 | Enhance ps-architect agent |
| WI-SAO-058 | 📋 OPEN | P1 | Enhance ps-synthesizer agent |
| WI-SAO-059 | 📋 OPEN | P1 | Enhance nse-requirements agent |
| WI-SAO-060 | 📋 OPEN | P1 | Enhance nse-reviewer agent |

### Phase 3: Enhancement - P2 Agents (2 work items)

| Work Item | Status | Priority | Description |
|-----------|--------|----------|-------------|
| WI-SAO-061 | 📋 OPEN | P2 | Enhance remaining ps-* agents (4 agents) |
| WI-SAO-062 | 📋 OPEN | P2 | Enhance remaining nse-* + orch-* agents (12 agents) |

### Phase 3: Enhancement - Skills & Patterns (3 work items)

| Work Item | Status | Priority | Description |
|-----------|--------|----------|-------------|
| WI-SAO-063 | 📋 OPEN | P1 | Enhance problem-solving SKILL.md + PLAYBOOK.md |
| WI-SAO-064 | 📋 OPEN | P1 | Enhance nasa-se + orchestration SKILL.md + PLAYBOOK.md |
| WI-SAO-065 | 📋 OPEN | P2 | Enhance ORCHESTRATION_PATTERNS.md |

### Phase 4: Validation (2 work items)

| Work Item | Status | Priority | Description |
|-----------|--------|----------|-------------|
| WI-SAO-066 | 📋 OPEN | P1 | Before/after comparison + rubric scoring |
| WI-SAO-067 | 📋 OPEN | P1 | Final review and synthesis documentation |

---

## Dependencies

```
PHASE 1 (Parallel Research):
WI-SAO-046 ───┐
WI-SAO-047 ───┼──► WI-SAO-049 (Synthesis)
WI-SAO-048 ───┘

PHASE 2 (Sequential Analysis):
WI-SAO-049 ──► WI-SAO-050 ──► WI-SAO-051 ──► WI-SAO-052

PHASE 3 (Generator-Critic per agent):
WI-SAO-052 ──► WI-SAO-053 ──► WI-SAO-054 ──► WI-SAO-055 ──► WI-SAO-056  (P0)
           ──► WI-SAO-057 ──► WI-SAO-058 ──► WI-SAO-059 ──► WI-SAO-060  (P1)
           ──► WI-SAO-061 ──► WI-SAO-062                                 (P2)
           ──► WI-SAO-063 ──► WI-SAO-064 ──► WI-SAO-065                 (Skills)

PHASE 4 (Validation):
ALL PHASE 3 ──► WI-SAO-066 ──► WI-SAO-067
```

---

## Success Criteria

### Quantitative Metrics

| Criterion | Target | Status |
|-----------|--------|--------|
| Research sources consulted | ≥5 external + ≥10 internal | 📋 Pending |
| Gap closure rate | 100% of identified gaps | 📋 Pending |
| Agent enhancement coverage | 22/22 agents + 3 orch-* | 📋 Pending |
| Skill enhancement coverage | 5/5 SKILL.md + 3/3 PLAYBOOK.md | 📋 Pending |
| Generator-Critic iterations | ≤3 per artifact (circuit breaker) | 📋 Pending |
| Quality threshold | ≥0.85 rubric score | 📋 Pending |

### Qualitative Metrics

| Criterion | Target | Status |
|-----------|--------|--------|
| L0/L1/L2 coverage | Every agent has all 3 lenses | 📋 Pending |
| Context engineering alignment | Follows Anthropic best practices | 📋 Pending |
| NASA SE compliance | Aligned with NPR 7123.1 | 📋 Pending |
| INCOSE alignment | Aligned with SE Handbook v5 | 📋 Pending |
| Before/after improvement | Measurable improvement on rubric | 📋 Pending |

---

## Scope

### In Scope

**Agent Definitions:**
- `.claude/agents/orchestrator.md`
- `.claude/agents/qa-engineer.md`
- `.claude/agents/security-auditor.md`
- `skills/problem-solving/agents/ps-*.md` (9 agents)
- `skills/nasa-se/agents/nse-*.md` (10 agents)
- `skills/orchestration/agents/orch-*.md` (3 agents)

**Skills:**
- `skills/problem-solving/SKILL.md`
- `skills/nasa-se/SKILL.md`
- `skills/orchestration/SKILL.md`
- `skills/architecture/SKILL.md`
- `skills/worktracker/SKILL.md`

**Playbooks:**
- `skills/problem-solving/PLAYBOOK.md`
- `skills/nasa-se/PLAYBOOK.md`
- `skills/orchestration/PLAYBOOK.md`

**Pattern Documentation:**
- `skills/shared/ORCHESTRATION_PATTERNS.md`

### Out of Scope

- Core framework code changes (src/)
- New agent creation (use existing agents)
- Plugin distribution changes (.claude-plugin/)
- Test suite modifications

---

## Risk Register

| Risk ID | Description | Likelihood | Impact | Mitigation |
|---------|-------------|------------|--------|------------|
| R-001 | Generator-Critic infinite loop | Medium | High | Circuit breaker: max 3 iterations |
| R-002 | Research scope creep | Medium | Medium | Time-box research phases |
| R-003 | Quality threshold not met | Low | Medium | Escalate to human review |
| R-004 | Context7 rate limits | Low | Low | Batch queries, cache results |
| R-005 | Breaking existing workflows | Medium | High | Before/after testing, staged rollout |

---

## Authoritative Sources

### External Sources

| Source | Domain | Usage |
|--------|--------|-------|
| Context7: Claude Code docs | Agent patterns | Context engineering best practices |
| Context7: Anthropic SDK | API patterns | Tool design, prompting |
| NASA NPR 7123.1 | SE processes | Review gates, V&V |
| NASA SE Handbook | SE practices | Requirements, architecture |
| INCOSE SE Handbook v5 | Industry SE | Cross-reference standards |

### Internal Sources

| Source | Domain | Usage |
|--------|--------|-------|
| PROJ-001 Architecture Canon | Framework patterns | Hexagonal, CQRS, Event Sourcing |
| PROJ-002 Synthesis Docs | Agent optimization | Gap analysis, trade studies |
| agent-research-001 to 007 | Agent theory | Persona, prompting, patterns |
| sao-042-generator-critic-* | Generator-Critic | Pattern implementation |
| ORCHESTRATION_PATTERNS.md | Orchestration | 8 patterns reference |

---

## Key Documents

| Document | Purpose |
|----------|---------|
| [plan.md](plan.md) | Detailed implementation plan |
| [../sao-init-007/_index.md](../sao-init-007-triple-lens-playbooks/_index.md) | Prior art: Triple-Lens framework |
| [../../research/agent-research-005-prompting-strategies.md](../../research/agent-research-005-prompting-strategies.md) | Prompting research |
| [../../../synthesis/skills-agents-optimization-synthesis.md](../../../synthesis/skills-agents-optimization-synthesis.md) | Optimization synthesis |

---

*Source: User request 2026-01-12*
*Strategy: Self-orchestration using Jerry's own pipelines*
*Pattern: Generator-Critic Loop with Fan-Out Research*
