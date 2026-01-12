# Trade-off Analysis: Agent Composition Options for Worktracker

**PS ID:** init-wt-skills
**Entry ID:** e-006
**Date:** 2026-01-11
**Author:** ps-analyst agent (v2.0.0)
**Topic:** Agent Composition Options for Worktracker Skill Enhancement

---

## L0: Executive Summary (ELI5)

Imagine you're opening a new restaurant. You have three options:

**Option A (Monolithic Skill)** is like training one head chef to do everything - cooking, baking, grilling. It's simple to start, but that chef becomes overwhelmed as the menu grows, and if they get sick, the whole kitchen stops.

**Option B (Cloned Hierarchy)** is like hiring separate chefs for everything - a prep cook, a grill chef, a pastry chef - but each one only knows how to make dishes for YOUR restaurant. If you open a second restaurant, you need to train entirely new chefs.

**Option C (Composed Architecture)** is like hiring specialists who can work at ANY restaurant - a prep cook who knows knife skills, a sauce maker who knows all mother sauces. They bring expertise that's reusable, and you just tell them what dish you're making today.

**RECOMMENDATION: Option C (Composed Architecture)** is the best choice for Jerry Framework because:
1. It maximizes reuse - problem-solving agents work across ALL skills, not just worktracker
2. It fights context rot most effectively - specialized agents load only relevant knowledge
3. It aligns with industry standards from Anthropic, Google, and OpenAI
4. It fully complies with Jerry Constitution (especially P-003's single-level nesting rule)

The implementation path requires 4-6 weeks and creates a foundation that benefits all future Jerry skills.

---

## L1: Technical Analysis (Software Engineer)

### 1.1 Option Definitions

#### Option A: Monolithic Skill

Expand the existing `skills/worktracker/SKILL.md` with inline agent behaviors embedded directly in the skill definition.

```
skills/worktracker/
├── SKILL.md              # Contains ALL agent behaviors inline
│   ├── # Work Analysis Section
│   ├── # Work Decomposition Section
│   ├── # Work Reporting Section
│   └── # Work Validation Section
└── scripts/              # CLI shims
```

**Characteristics:**
- Single file contains all intelligence
- No separate agent definitions
- All behaviors loaded at skill activation
- Implicit delegation within skill instructions

#### Option B: Cloned Hierarchy

Create a parallel set of `wt-*` agents mirroring the `ps-*` structure with worktracker-specific specializations.

```
skills/worktracker/
├── SKILL.md              # Entry point, routes to agents
├── agents/
│   ├── wt-analyzer.md    # Work item root cause analysis
│   ├── wt-decomposer.md  # Epic → Story → Task breakdown
│   ├── wt-reporter.md    # Work status reporting
│   ├── wt-validator.md   # Work item constraint checking
│   └── wt-synthesizer.md # Cross-work-item pattern extraction
└── scripts/
```

**Characteristics:**
- Separate agent definitions per role
- Each agent is worktracker-specific
- Template copied from ps-* agents
- Independent evolution from ps-* agents

#### Option C: Composed Architecture

Create thin `wt-*` wrapper agents that COMPOSE with existing `ps-*` agents, adding worktracker-specific context.

```
skills/worktracker/
├── SKILL.md              # Entry point
├── agents/
│   ├── wt-coordinator.md # Routes to ps-* agents with WT context
│   ├── wt-context.md     # Context injection for ps-* agents
│   └── wt-adapters/
│       ├── ps-analyst.yaml    # ps-analyst + WT domain
│       └── ps-reporter.yaml   # ps-reporter + WT domain
└── scripts/
```

**Characteristics:**
- wt-coordinator invokes ps-* agents with worktracker context
- Domain knowledge injected via adapters/context
- ps-* agents do the heavy lifting
- wt-* agents provide domain translation

### 1.2 Evaluation Criteria

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Complexity | 20% | Implementation and maintenance burden |
| Reusability | 25% | Component sharing across skills |
| Context Efficiency | 25% | Token usage and context rot mitigation |
| Standards Alignment | 15% | Industry best practices compliance |
| Constitution Compliance | 15% | Jerry Constitution adherence |

### 1.3 Detailed Evaluation

#### Criterion 1: Complexity (Weight: 20%)

| Option | Initial Complexity | Ongoing Maintenance | Score (1-10) |
|--------|-------------------|---------------------|--------------|
| **A: Monolithic** | LOW - single file | HIGH - all changes in one place | 6 |
| **B: Cloned** | MEDIUM - 5+ files | HIGH - sync with ps-* updates | 4 |
| **C: Composed** | MEDIUM - coordination layer | LOW - ps-* agents maintained centrally | 7 |

**Analysis:**

**Option A:** Simple to start, but complexity compounds. SKILL.md becomes a "god file" over time. Changes risk breaking unrelated behaviors. No separation of concerns.

**Option B:** Initial overhead to create 5+ agent files. Ongoing burden to keep wt-* agents synchronized with ps-* agent improvements. Leads to "fork drift" where wt-* agents diverge from ps-* standards.

**Option C:** Upfront investment in coordination layer, but ongoing maintenance is minimal. When ps-analyst improves, wt-* automatically benefits. Clear separation: ps-* owns methodology, wt-* owns domain.

**Score: A=6, B=4, C=7**

---

#### Criterion 2: Reusability (Weight: 25%)

| Option | Cross-Skill Reuse | Component Reuse | Score (1-10) |
|--------|-------------------|-----------------|--------------|
| **A: Monolithic** | NONE - locked in skill | N/A | 2 |
| **B: Cloned** | NONE - wt-specific | Template only | 3 |
| **C: Composed** | HIGH - ps-* agents shared | Adapters reusable | 9 |

**Analysis:**

**Option A:** All intelligence is trapped inside worktracker skill. If another skill needs analysis capabilities, it must duplicate the code. Zero reuse potential.

**Option B:** wt-* agents are worktracker-specific. While they follow the ps-* template, they cannot be invoked by other skills. If `skills/architecture/` needs analysis, it would need its own `arch-analyzer.md`.

**Option C:** ps-* agents remain general-purpose. The adaptation layer (wt-context) is the only worktracker-specific part. Future skills can create their own thin adapters: `arch-context.md`, `security-context.md`, etc.

**Industry Support:** Anthropic's Agent Skills standard explicitly recommends "modular, composable agents" (e-002, L1). Google ADK patterns favor "coordinator/specialist" over monolithic agents.

**Score: A=2, B=3, C=9**

---

#### Criterion 3: Context Efficiency (Weight: 25%)

| Option | Token Load at Activation | Progressive Disclosure | Score (1-10) |
|--------|-------------------------|----------------------|--------------|
| **A: Monolithic** | HIGH - entire skill | NONE | 3 |
| **B: Cloned** | MEDIUM - per agent | Partial | 6 |
| **C: Composed** | LOW - only needed agents | Full | 9 |

**Analysis:**

**Option A:** Entire SKILL.md loads at activation. If worktracker skill grows to include analysis, reporting, validation, and decomposition behaviors (estimated 8,000-12,000 tokens), all of it loads even for simple `@worktracker list` commands.

**Option B:** Each wt-* agent loads independently (~2,000-3,000 tokens each). Improvement over Option A, but still loads worktracker-specific definitions that duplicate ps-* knowledge.

**Option C:** Only the thin wt-coordinator (~500 tokens) plus the needed ps-* agent (~2,500 tokens) loads. The ps-* agent's general methodology is already optimized for context efficiency per progressive disclosure pattern (e-002, L1 Section 1).

**Context Rot Impact:**

Per Chroma research (e-002, L2), LLM performance degrades 20-50% from 10k to 100k tokens. Minimizing loaded context is critical.

| Option | Estimated Context for Work Analysis Task |
|--------|------------------------------------------|
| A | ~12,000 tokens (entire skill + domain) |
| B | ~5,500 tokens (wt-analyst + domain) |
| C | ~3,000 tokens (ps-analyst + wt-context) |

**Score: A=3, B=6, C=9**

---

#### Criterion 4: Standards Alignment (Weight: 15%)

| Standard | Option A | Option B | Option C |
|----------|----------|----------|----------|
| Anthropic Agent Skills | Partial | Partial | Full |
| Google ADK Patterns | None | Partial | Full |
| OpenAI Handoff Patterns | None | None | Full |
| MCP Compatibility | N/A | N/A | N/A |

**Analysis:**

**Anthropic Agent Skills (December 2025):**
- Skills should be "modular knowledge packages" with progressive disclosure
- Option A violates modularity (monolithic)
- Option B follows template but duplicates knowledge
- Option C aligns fully: skills = domain context, agents = methodology

**Google ADK Patterns:**
- Coordinator/Specialist pattern: "Central LlmAgent manages specialized sub_agents"
- Option A: No coordination, no specialists
- Option B: Specialists exist but isolated
- Option C: wt-coordinator routes to ps-* specialists

**OpenAI Handoff Patterns:**
- "Agent-as-Tool" pattern: "Expose one agent as callable tool for another"
- Option A: N/A
- Option B: N/A
- Option C: ps-* agents exposed as tools for wt-coordinator

**Score: A=3, B=5, C=9**

---

#### Criterion 5: Constitution Compliance (Weight: 15%)

| Principle | Option A | Option B | Option C |
|-----------|----------|----------|----------|
| P-002 (Persistence) | PASS | PASS | PASS |
| P-003 (No Recursion) | PASS* | RISK | PASS |
| P-004 (Provenance) | PARTIAL | PASS | PASS |

**Analysis:**

**P-002 (File Persistence):**
All options can comply by persisting outputs. No differentiation.

**P-003 (No Recursive Subagents):**
- **Option A:** PASS - No subagents spawned (but also no specialization)
- **Option B:** RISK - If wt-* agents spawn ps-* agents, creates nesting. Must explicitly forbid.
- **Option C:** PASS - wt-coordinator is the ONLY agent level. ps-* agents are invoked directly, not through wt-* intermediaries.

**Critical P-003 Consideration:**

Option B creates risk of:
```
User → wt-analyzer → ps-researcher (2 levels = VIOLATION)
```

Option C avoids this:
```
User → wt-coordinator → ps-analyst (1 level = COMPLIANT)
```

**P-004 (Provenance):**
- **Option A:** PARTIAL - Single file, harder to trace which "behavior" produced output
- **Option B:** PASS - Clear agent provenance
- **Option C:** PASS - Clear agent provenance with explicit context injection

**Score: A=7, B=6, C=9**

### 1.4 Scoring Matrix

| Criterion | Weight | Option A | Option B | Option C |
|-----------|--------|----------|----------|----------|
| Complexity | 20% | 6 (1.2) | 4 (0.8) | 7 (1.4) |
| Reusability | 25% | 2 (0.5) | 3 (0.75) | 9 (2.25) |
| Context Efficiency | 25% | 3 (0.75) | 6 (1.5) | 9 (2.25) |
| Standards Alignment | 15% | 3 (0.45) | 5 (0.75) | 9 (1.35) |
| Constitution Compliance | 15% | 7 (1.05) | 6 (0.9) | 9 (1.35) |
| **TOTAL** | 100% | **3.95** | **4.70** | **8.60** |

### 1.5 Decision

**RECOMMENDATION: Option C (Composed Architecture)**

Option C scores 8.60/10, significantly outperforming Option B (4.70) and Option A (3.95).

**Key Differentiators:**
1. **83% higher reusability** than Option B (9 vs 3)
2. **200% better context efficiency** than Option A (9 vs 3)
3. **Full compliance** with all industry standards and Jerry Constitution

---

## L2: Architectural Implications (Principal Architect)

### 2.1 Composition Architecture Design

#### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          WORKTRACKER SKILL LAYER                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐     ┌─────────────────────────────────────────────┐   │
│  │   SKILL.md      │────▶│            wt-coordinator.md                │   │
│  │   (Entry Point) │     │  - Domain context injection                 │   │
│  └─────────────────┘     │  - Route to appropriate ps-* agent          │   │
│                          │  - Transform output for WT domain           │   │
│                          └─────────────────────────────────────────────┘   │
│                                          │                                  │
│                          ┌───────────────┼───────────────┐                  │
│                          ▼               ▼               ▼                  │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐               │
│  │ wt-adapters/    │ │ wt-adapters/    │ │ wt-adapters/    │               │
│  │ ps-analyst.yaml │ │ ps-reporter.yaml│ │ ps-validator.yaml│              │
│  │ (domain context)│ │ (domain context)│ │ (domain context)│               │
│  └────────┬────────┘ └────────┬────────┘ └────────┬────────┘               │
│           │                   │                   │                         │
└───────────┼───────────────────┼───────────────────┼─────────────────────────┘
            │                   │                   │
            ▼                   ▼                   ▼
┌───────────────────────────────────────────────────────────────────────────┐
│                      PROBLEM-SOLVING AGENT LAYER                          │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐           │
│  │   ps-analyst    │  │   ps-reporter   │  │   ps-validator  │           │
│  │   (5 Whys,      │  │   (Status,      │  │   (Constraints, │           │
│  │    FMEA,        │  │    Metrics,     │  │    RTM,         │           │
│  │    Trade-offs)  │  │    Dashboards)  │  │    Pass/Fail)   │           │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘           │
│                                                                           │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐           │
│  │   ps-researcher │  │   ps-synthesizer│  │   ps-architect  │           │
│  │   (5W1H,        │  │   (Patterns,    │  │   (ADRs,        │           │
│  │    Context7)    │  │    Lessons)     │  │    C4 Models)   │           │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘           │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘
```

#### wt-coordinator Responsibilities

1. **Context Injection:** Add worktracker-specific domain context to ps-* agent invocations
2. **Route Selection:** Determine which ps-* agent(s) handle the request
3. **Output Transformation:** Adapt ps-* output format for worktracker domain
4. **State Management:** Pass worktracker state to/from ps-* agents

#### Adapter Format (YAML)

```yaml
# skills/worktracker/agents/wt-adapters/ps-analyst.yaml
---
base_agent: skills/problem-solving/agents/ps-analyst.md
domain_context:
  entities:
    - WorkItem
    - Epic
    - Story
    - Task
    - Bug
    - Spike
  relationships:
    - parent_of
    - blocked_by
    - depends_on
  states:
    - pending
    - in_progress
    - blocked
    - completed
  analysis_focus:
    - blocked_work_root_cause
    - overdue_work_patterns
    - dependency_cycles
output_location: "projects/${JERRY_PROJECT}/analysis/wt-{entry_id}-{topic_slug}.md"
---
```

### 2.2 Implementation Path

#### Phase 1: Foundation (Week 1-2)

**Deliverables:**
1. `skills/worktracker/agents/wt-coordinator.md` - Main routing agent
2. `skills/worktracker/agents/wt-adapters/` directory structure
3. Update `skills/worktracker/SKILL.md` to reference coordinator

**Tasks:**
- [ ] Create wt-coordinator agent definition following PS_AGENT_TEMPLATE.md
- [ ] Define adapter YAML schema
- [ ] Create initial ps-analyst adapter for blocked work analysis
- [ ] Create initial ps-reporter adapter for work status reporting
- [ ] Update SKILL.md with new invocation patterns

**Risk Mitigation:**
- P-003 compliance verified by explicit single-level invocation in coordinator
- Progressive disclosure maintained by loading only needed adapters

#### Phase 2: Core Adapters (Week 3-4)

**Deliverables:**
1. `wt-adapters/ps-analyst.yaml` - Work item root cause analysis
2. `wt-adapters/ps-reporter.yaml` - Work status reporting
3. `wt-adapters/ps-validator.yaml` - Work item constraint checking
4. `wt-adapters/ps-synthesizer.yaml` - Cross-work-item pattern extraction

**Tasks:**
- [ ] Define domain context for each adapter
- [ ] Create output templates for WT-specific artifacts
- [ ] Implement state passing between coordinator and ps-* agents
- [ ] Test each adapter with sample work items

#### Phase 3: Integration (Week 5-6)

**Deliverables:**
1. Updated `@worktracker` command handlers to use composed agents
2. Documentation for composed agent invocation
3. Behavioral tests for P-003 compliance

**Tasks:**
- [ ] Integrate wt-coordinator with existing worktracker commands
- [ ] Add `@worktracker analyze <id>` command (uses ps-analyst)
- [ ] Add `@worktracker report` command (uses ps-reporter)
- [ ] Add `@worktracker validate` command (uses ps-validator)
- [ ] Create behavioral tests per BEHAVIOR_TESTS.md

### 2.3 Extension Points

#### Future Skill Integration

The composed architecture enables rapid adoption for other skills:

```
skills/architecture/agents/
├── arch-coordinator.md
└── arch-adapters/
    ├── ps-architect.yaml    # ADR generation with arch context
    └── ps-reviewer.yaml     # Design review with arch context

skills/security/agents/
├── sec-coordinator.md
└── sec-adapters/
    ├── ps-reviewer.yaml     # Security review with OWASP context
    └── ps-investigator.yaml # Security incident RCA
```

**Time to Adopt:** With composed architecture established, new skills can add agent capabilities in 1-2 days rather than 1-2 weeks.

#### Cross-Skill Agent Sharing

Once multiple skills adopt composed architecture, advanced patterns become possible:

```
┌────────────────────────────────────────────────────────────────────────┐
│                    CROSS-SKILL AGENT SHARING                          │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│   wt-coordinator ──────┐                                               │
│                        │                                               │
│   arch-coordinator ────┼──────▶ ps-reviewer (shared analysis)          │
│                        │                                               │
│   sec-coordinator ─────┘                                               │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

### 2.4 Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| P-003 violation via accidental nesting | Low | High | Explicit coordinator-only invocation, behavioral tests |
| Context bloat from adapter overhead | Low | Medium | Adapter YAML is <100 tokens, negligible |
| ps-* agent changes break adapters | Medium | Low | Adapters reference agent by path; changes are additive |
| Coordination overhead delays response | Low | Low | Coordinator is thin routing layer, <500ms overhead |

### 2.5 Alternative Considered: Hybrid B+C

A hybrid approach was considered: clone SOME agents (wt-reporter for custom dashboards) while composing others (ps-analyst for methodology).

**Decision:** Rejected in favor of pure Option C.

**Rationale:**
- Inconsistency creates cognitive load for maintainers
- "When in doubt, compose" provides clear guidance
- If wt-reporter needs customization, extend the adapter layer rather than clone

### 2.6 Success Criteria

| Metric | Target | Measurement |
|--------|--------|-------------|
| Context token reduction | 50%+ vs Option A | Measure token count for work analysis task |
| New skill adoption time | <2 days | Time to add agent capabilities to new skill |
| P-003 compliance | 100% | All behavioral tests pass |
| Reuse ratio | >60% | % of agent code from ps-* vs wt-specific |

---

## References

### Input Documents

1. `projects/PROJ-001-plugin-cleanup/research/init-wt-skills-e-001-ps-agent-portfolio.md`
   - Key insight: 8 ps-* agents follow consistent template with clear upstream/downstream relationships

2. `projects/PROJ-001-plugin-cleanup/research/init-wt-skills-e-002-agent-skills-standards.md`
   - Key insight: Industry consensus on composable agents with progressive disclosure

### Jerry Framework Documents

3. `docs/governance/JERRY_CONSTITUTION.md`
   - Key insight: P-003 (Hard) - Maximum ONE level of agent nesting

4. `skills/problem-solving/agents/PS_AGENT_TEMPLATE.md`
   - Key insight: Template v2.0 includes state management for agent composition

5. `skills/worktracker/SKILL.md`
   - Key insight: Current skill has no agent layer, commands are simple CRUD

### Industry Sources

6. [Anthropic Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) - "Modular, composable agents"
7. [Google ADK Multi-Agent Patterns](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/) - Coordinator/Specialist pattern
8. [OpenAI Agent Guide](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) - Agent-as-Tool pattern
9. [Chroma Context Rot Research](https://research.trychroma.com/context-rot) - 20-50% degradation at high token counts

---

## PS Integration

**Artifact Location:** `projects/PROJ-001-plugin-cleanup/analysis/init-wt-skills-e-006-tradeoff-analysis.md`

**State Output:**
```yaml
analyst_output:
  ps_id: "init-wt-skills"
  entry_id: "e-006"
  artifact_path: "projects/PROJ-001-plugin-cleanup/analysis/init-wt-skills-e-006-tradeoff-analysis.md"
  summary: "Recommend Option C (Composed Architecture) with 8.60/10 score - maximizes reusability and context efficiency while ensuring P-003 compliance"
  recommendation: "Option C: Composed Architecture"
  confidence: "high"
  next_agent_hint: "ps-architect (for ADR if decision approved)"
```

---

*Generated by ps-analyst agent v2.0.0*
*Constitutional Compliance: Jerry Constitution v1.0*
*Analysis completed: 2026-01-11*
