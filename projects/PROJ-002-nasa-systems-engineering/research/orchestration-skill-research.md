# Orchestration Skill Architecture Research

> **Document ID:** PROJ-002-RESEARCH-ORCH-SKILL
> **Date:** 2026-01-10
> **Researcher:** Claude (Distinguished NASA SE / Software Architecture)
> **Status:** COMPLETE
> **Classification:** Research Findings

---

## L0: Executive Summary

Research validates creating a dedicated `orchestration` skill rather than overloading CLAUDE.md. Industry best practices from Anthropic, Microsoft, LangGraph, and CrewAI strongly support modular skill-based architecture with progressive disclosure. The Jerry framework already follows this pattern with 4 existing skills. The orchestration skill will contain templates, agents, and detailed instructions for multi-agent workflow management.

---

## L1: Research Methodology

### Sources Consulted

| Source | Type | Authority | Key Contribution |
|--------|------|-----------|------------------|
| [Anthropic Engineering Blog](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) | Primary | High (Official) | Agent Skills architecture, progressive disclosure |
| [Claude Code Skills Docs](https://code.claude.com/docs/en/skills) | Primary | High (Official) | SKILL.md format, YAML frontmatter, activation |
| [First Principles Deep Dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/) | Secondary | Medium (Community Expert) | Layered context loading, token efficiency |
| [Skills vs System Prompts](https://skywork.ai/blog/ai-agent/claude-skills-vs-system-prompts-2025-comparison/) | Secondary | Medium (Industry) | When to use skills vs prompts |
| [Microsoft AI Agent Patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns) | Primary | High (Official) | Orchestration patterns taxonomy |
| [Microsoft Semantic Kernel](https://github.com/microsoft/semantic-kernel) | Primary | High (Official) | Plugin architecture, agent coordination |
| [LangGraph Documentation](https://langchain-ai.github.io/langgraph/) | Primary | High (Official) | State checkpointing, workflow persistence |
| [CrewAI Flows](https://docs.crewai.com/concepts/flows) | Primary | High (Official) | Flow state management, routing |
| [NASA NPR 7123.1D](https://nodis3.gsfc.nasa.gov/displayDir.cfm?Internal_ID=N_PR_7123_001D_) | Primary | High (Official) | SE Engine, technical review gates |
| Jerry Framework Skills | Internal | High (Authoritative) | Existing skill pattern analysis |

---

## L1: Key Findings

### 1. Progressive Disclosure Pattern (Anthropic)

Anthropic's Agent Skills architecture employs **three-layer progressive disclosure**:

```
Layer 1: YAML Frontmatter (~30-50 tokens/skill)
         - Loaded at startup for ALL skills
         - Contains: name, description, version
         - Purpose: Skill discovery/matching

Layer 2: SKILL.md Content (loaded on activation)
         - Full instructions and context
         - Loaded only when skill is relevant
         - Purpose: Primary skill execution

Layer 3: Helper Assets (loaded on demand)
         - References, templates, scripts
         - Loaded during execution as needed
         - Purpose: Unbounded context expansion
```

**Citation:** "Skills let Claude load information only as needed... like a well-organized manual that starts with a table of contents, then specific chapters, and finally a detailed appendix." — [Anthropic Engineering](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

### 2. Skills vs System Prompts (Industry Consensus)

| Aspect | Skills | System Prompts |
|--------|--------|----------------|
| Structure | Modular, versioned capsules | Monolithic instruction blob |
| Loading | On-demand, progressive | Always loaded |
| Token Impact | ~30-50 tokens/skill (metadata only) | Full context always consumed |
| Reusability | Highly reusable, portable | Single-use, context-specific |
| Maintenance | Independent versioning | Requires full rewrite |
| Use Case | Domain-specific procedures | Core agent behavior |

**Citation:** "Skills = structured, reusable capabilities with routing and progressive disclosure; system prompts = one monolithic instruction blob." — [SkyWork AI](https://skywork.ai/blog/ai-agent/claude-skills-vs-system-prompts-2025-comparison/)

### 3. SKILL.md Format (Official Standard)

```yaml
---
name: skill-name
description: Brief, action-oriented summary (used for matching)
allowed-tools: "Read,Write,Bash"  # Comma-separated, supports wildcards
model: "inherit"                   # or specific model
version: "1.0.0"
license: "Optional"
activation-keywords:               # Jerry extension
  - "keyword1"
  - "keyword2"
---

# Skill Name

## Purpose
1-2 sentences on what the skill does.

## When to Use
Clear activation criteria.

## Instructions
Step-by-step guidance.

## Output Format
Expected deliverables.

## Examples
Concrete usage examples.
```

**Best Practices:**
- Keep SKILL.md under 5,000 words
- Use `{baseDir}` for portable paths
- Explicitly state activation criteria in description
- Separate references into `/references/` directory

### 4. Orchestration Patterns (Microsoft)

The [Microsoft AI Agent Design Patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns) document defines 5 orchestration patterns:

| Pattern | Description | Use When |
|---------|-------------|----------|
| **Sequential** | Linear pipeline, each agent builds on previous | Clear dependencies, progressive refinement |
| **Concurrent** | Multiple agents process same input in parallel | Diverse perspectives, time-sensitive |
| **Group Chat** | Managed conversation thread with coordinator | Consensus-building, quality control |
| **Handoff** | Dynamic delegation to specialists | Emerging requirements, capability-based routing |
| **Magentic** | Manager builds task ledger through collaboration | Open-ended problems, plan generation |

### 5. State Management Patterns

**LangGraph Approach:**
- Checkpointing at every superstep
- Thread-based multi-tenant isolation
- Time-travel debugging via checkpoint_id
- Write-ahead logging for durability

**CrewAI Approach:**
- Flow state as Pydantic BaseModel
- @start, @listen, @router decorators
- Conditional routing based on state
- Memory persistence across sessions

**Jerry Approach (Current):**
- File-based state persistence (P-002)
- State keys reference artifact paths
- No in-memory state sharing
- Recovery via artifact files

### 6. Existing Jerry Skill Pattern

Analysis of `skills/problem-solving/`:

```
skills/problem-solving/
├── SKILL.md              # Main entry point (266 lines)
├── PLAYBOOK.md           # User workflow guide
├── agents/               # Agent definitions
│   ├── PS_AGENT_TEMPLATE.md
│   ├── ps-researcher.md
│   ├── ps-analyst.md
│   └── ... (8 agents)
└── docs/
    └── ORCHESTRATION.md  # Technical orchestration guide (487 lines)
```

**Key Pattern Elements:**
- YAML frontmatter with activation-keywords
- Version tracking
- Constitutional compliance matrix
- Agent registry with output locations
- Orchestration patterns (Sequential, Fan-Out, Fan-In)
- State passing via artifact references

---

## L2: Strategic Recommendations

### Recommendation 1: Create Dedicated Orchestration Skill

**Rationale:**
1. **Context Efficiency:** Skills cost ~30-50 tokens when dormant vs monolithic CLAUDE.md
2. **Separation of Concerns:** Orchestration is specialized capability, not core behavior
3. **Reusability:** Skill can be used across all projects
4. **Versioning:** Independent evolution from CLAUDE.md
5. **Pattern Alignment:** Matches existing Jerry skill structure

**Evidence:** Anthropic's official guidance: "This is not prompt engineering. This is systems design."

### Recommendation 2: Skill Structure

```
skills/orchestration/
├── SKILL.md                    # Main entry point
├── PLAYBOOK.md                 # User workflow guide
├── templates/                  # Artifact templates
│   ├── ORCHESTRATION_PLAN.md   # Strategic context template
│   ├── ORCHESTRATION_WORKTRACKER.md  # Tactical state template
│   └── ORCHESTRATION.yaml      # Machine-readable state template
├── agents/                     # Orchestration agents
│   ├── orch-planner.md         # Creates orchestration plan
│   ├── orch-tracker.md         # Manages execution state
│   └── orch-synthesizer.md     # Final synthesis
└── docs/
    ├── PATTERNS.md             # Orchestration patterns guide
    └── STATE_SCHEMA.md         # YAML schema documentation
```

### Recommendation 3: CLAUDE.md Light Reference

Add minimal section to CLAUDE.md:

```markdown
## Multi-Agent Orchestration

For complex multi-agent workflows requiring:
- Cross-pollinated pipelines
- Parallel agent execution
- Sync barriers and checkpoints
- State tracking across sessions

Invoke the **orchestration** skill: `skills/orchestration/SKILL.md`

All projects requiring orchestration should create:
- `ORCHESTRATION_PLAN.md` - Strategic context
- `ORCHESTRATION_WORKTRACKER.md` - Tactical state
- `ORCHESTRATION.yaml` - Machine-readable state (SSOT)
```

### Recommendation 4: Template Variables

Templates should use portable variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `{project_id}` | Project identifier | PROJ-002 |
| `{workflow_id}` | Workflow identifier | SAO-PIPELINE |
| `{baseDir}` | Project base directory | projects/PROJ-002/ |
| `{timestamp}` | ISO-8601 timestamp | 2026-01-10T09:30:00Z |

---

## L2: Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Skill overhead adds complexity | Low | Low | Progressive disclosure minimizes context |
| Template drift from ORCHESTRATION.yaml | Medium | Medium | YAML is SSOT, docs regenerated |
| Skill not activated when needed | Low | Medium | Clear activation-keywords, CLAUDE.md reference |
| Cross-project inconsistency | Medium | Low | Templates enforce structure |

---

## Conclusion

**Decision: Create `skills/orchestration/` skill with templates and light CLAUDE.md reference.**

This approach:
1. Aligns with Anthropic's official Agent Skills architecture
2. Follows established Jerry skill patterns
3. Enables progressive disclosure (minimal token cost when not used)
4. Provides comprehensive templates for consistent orchestration
5. Supports evidence-based state management with ORCHESTRATION.yaml

---

## References

1. Anthropic. (2025). *Equipping agents for the real world with Agent Skills*. https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
2. Anthropic. (2025). *Agent Skills - Claude Code Docs*. https://code.claude.com/docs/en/skills
3. Lee, H. (2025). *Claude Agent Skills: A First Principles Deep Dive*. https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/
4. SkyWork AI. (2025). *Claude Skills vs System Prompts*. https://skywork.ai/blog/ai-agent/claude-skills-vs-system-prompts-2025-comparison/
5. Microsoft. (2025). *AI Agent Orchestration Patterns*. https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns
6. Microsoft. (2025). *Semantic Kernel Agent Framework*. https://github.com/microsoft/semantic-kernel
7. LangChain. (2025). *LangGraph Documentation*. https://langchain-ai.github.io/langgraph/
8. CrewAI. (2025). *Flows Documentation*. https://docs.crewai.com/concepts/flows
9. NASA. (2024). *NPR 7123.1D Systems Engineering Processes and Requirements*. https://nodis3.gsfc.nasa.gov/

---

*Research Document: PROJ-002-RESEARCH-ORCH-SKILL*
*Date: 2026-01-10*
*Status: COMPLETE*
