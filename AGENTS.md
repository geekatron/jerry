# AGENTS.md - Registry of Available Specialists

> This file documents the sub-agent personas available for task delegation.
> Each agent has specialized capabilities and context isolation.

---

## Agent Philosophy

Jerry uses a **skill-based agent pattern** where specialized agents are scoped
to specific skills. This provides:

1. **Context Isolation** - Each agent has focused context
2. **Expertise Depth** - Specialists know their domain deeply
3. **Parallel Execution** - Multiple agents can work concurrently
4. **Quality Gates** - Handoffs enforce review checkpoints

---

## Agent Summary

| Category | Count | Scope |
|----------|-------|-------|
| Problem-Solving Agents | 8 | `/problem-solving` skill |
| **Total** | **8** | |

---

## Problem-Solving Skill Agents

These agents are scoped to the `problem-solving` skill and invoked via `/problem-solving`.

| Agent | File | Role |
|-------|------|------|
| ps-researcher | `skills/problem-solving/agents/ps-researcher.md` | Research Specialist |
| ps-analyst | `skills/problem-solving/agents/ps-analyst.md` | Analysis Specialist |
| ps-synthesizer | `skills/problem-solving/agents/ps-synthesizer.md` | Synthesis Specialist |
| ps-validator | `skills/problem-solving/agents/ps-validator.md` | Validation Specialist |
| ps-architect | `skills/problem-solving/agents/ps-architect.md` | Architecture Specialist |
| ps-reviewer | `skills/problem-solving/agents/ps-reviewer.md` | Review Specialist |
| ps-investigator | `skills/problem-solving/agents/ps-investigator.md` | Investigation Specialist |
| ps-reporter | `skills/problem-solving/agents/ps-reporter.md` | Reporting Specialist |

---

## Problem-Solving Agents Overview

The problem-solving skill provides 8 specialized agents for structured problem solving:

| Agent | Cognitive Mode | Primary Use Case |
|-------|---------------|------------------|
| ps-researcher | Divergent | Literature review, web research, source validation |
| ps-analyst | Convergent | Root cause analysis, trade-offs, gap analysis, risk |
| ps-synthesizer | Integrative | Pattern synthesis across multiple research outputs |
| ps-validator | Systematic | Constraint verification, design validation |
| ps-architect | Strategic | Architecture decisions, ADR production |
| ps-reviewer | Critical | Code review, design review, security review |
| ps-investigator | Forensic | Failure analysis, debugging, 5 Whys |
| ps-reporter | Communicative | Status reports, phase progress, summaries |

**Invocation**: Use `/problem-solving` skill which orchestrates these agents.

**Artifact Location**: `{project}/research/`, `{project}/analysis/`, `{project}/synthesis/`

---

## Agent Handoff Protocol

### Triggering Handoffs

Handoffs are triggered by:
1. **Hook-based**: `scripts/subagent_stop.py` detects completion
2. **Explicit**: Parent agent delegates via Task tool
3. **Skill-based**: Skill orchestrator routes to appropriate specialist

### Handoff Data

When handing off between agents, include:
```json
{
  "from_agent": "ps-researcher",
  "to_agent": "ps-analyst",
  "context": {
    "task_id": "WORK-123",
    "artifacts": ["research/proj-001-e-001-research.md"],
    "summary": "Completed initial research on architecture patterns"
  },
  "request": "Analyze findings and identify gaps"
}
```

---

## Adding New Agents

New agents should be added within their respective skill directory:

1. Create agent file in `skills/{skill-name}/agents/{agent-name}.md`
2. Define persona, responsibilities, and constraints
3. Register in this file (AGENTS.md) under the skill section
4. Update skill orchestrator to know about the new agent
5. Add relevant hooks if needed

### Agent File Template

```markdown
---
name: {agent-name}
description: |
  Use this agent when {trigger conditions}.
  <example>User: "{example prompt}"</example>
model: sonnet
tools:
  - Read
  - Grep
  - Glob
---

# {Agent Name}

## Persona
{One paragraph describing the agent's character and expertise}

## Responsibilities
- {Primary responsibility}
- {Secondary responsibility}
- ...

## Constraints
- {What this agent should NOT do}
- {Boundaries of authority}

## Input Format
{What information this agent needs to start work}

## Output Format
{What this agent produces when done}

## Handoff Triggers
{When this agent should hand off to another}
```

---

## Future Skills with Agents (Planned)

| Skill | Agents | Status |
|-------|--------|--------|
| documentation | doc-writer, api-documenter | Planned |
| performance | profiler, optimizer | Planned |
| devops | deployer, monitor | Planned |
