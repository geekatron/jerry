# AGENTS.md - Registry of Available Specialists

> This file documents the sub-agent personas available for task delegation.
> Each agent has specialized capabilities and context isolation.

---

## Agent Philosophy

Jerry uses a **conductor pattern** where the Orchestrator agent coordinates
specialized sub-agents for specific tasks. This provides:

1. **Context Isolation** - Each agent has focused context
2. **Expertise Depth** - Specialists know their domain deeply
3. **Parallel Execution** - Multiple agents can work concurrently
4. **Quality Gates** - Handoffs enforce review checkpoints

---

## Agent Summary

| Category | Count | Scope |
|----------|-------|-------|
| Framework Agents | 3 | Global (available in all contexts) |
| Skill-Specific Agents | 8 | Local (problem-solving skill only) |
| **Total** | **11** | |

---

## Framework Agents (Global)

These agents are available across all Jerry contexts.

| Agent | File | Role |
|-------|------|------|
| Orchestrator | `.claude/agents/orchestrator.md` | Task decomposition, delegation, synthesis |
| QA Engineer | `.claude/agents/qa-engineer.md` | Test design and quality assurance |
| Security Auditor | `.claude/agents/security-auditor.md` | Security review and vulnerability assessment |

---

## Skill-Specific Agents

### Problem-Solving Skill Agents

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

## Framework Agent Details

### Orchestrator (Conductor)

**File**: `.claude/agents/orchestrator.md`
**Model**: Opus 4.5 (recommended)
**Role**: Task decomposition, delegation, and synthesis

**Responsibilities**:
- Analyze incoming requests
- Decompose into sub-tasks
- Delegate to appropriate specialists
- Synthesize results
- Maintain coherent narrative

**When to Use**: Complex multi-step tasks requiring coordination

---

### QA Engineer

**File**: `.claude/agents/qa-engineer.md`
**Model**: Sonnet (recommended)
**Role**: Test design, execution, and quality assurance

**Responsibilities**:
- Design test cases (unit, integration, e2e)
- Review code for testability
- Identify edge cases and failure modes
- Validate acceptance criteria
- Report defects with reproduction steps

**When to Use**: Before merging code, after significant changes

---

### Security Auditor

**File**: `.claude/agents/security-auditor.md`
**Model**: Sonnet (recommended)
**Role**: Security review and vulnerability assessment

**Responsibilities**:
- Review code for OWASP Top 10 vulnerabilities
- Assess authentication/authorization flows
- Identify injection risks (SQL, command, XSS)
- Review secrets management
- Recommend security improvements

**When to Use**: Before release, when handling sensitive data

---

## Skill-Specific Agent Details

### Problem-Solving Agents Overview

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
1. **Hook-based**: `subagent_stop.py` detects completion
2. **Explicit**: Orchestrator delegates via Task tool
3. **Rule-based**: Certain file types trigger specific agents

### Handoff Data

When handing off between agents, include:
```json
{
  "from_agent": "orchestrator",
  "to_agent": "qa-engineer",
  "context": {
    "task_id": "WORK-123",
    "files_changed": ["src/domain/aggregates/work_item.py"],
    "summary": "Implemented WorkItem.complete() method"
  },
  "request": "Design unit tests for the complete() method"
}
```

---

## Adding New Agents

1. Create agent file in `.claude/agents/{name}.md`
2. Define persona, responsibilities, and constraints
3. Register in this file (AGENTS.md)
4. Update orchestrator to know about the new agent
5. Add relevant hooks if needed

### Agent File Template

```markdown
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

## Future Agents (Planned)

| Agent | Role | Status |
|-------|------|--------|
| Documentation Writer | API docs, READMEs | Planned |
| Performance Analyst | Profiling, optimization | Planned |
| DevOps Engineer | CI/CD, deployment | Planned |
| Domain Expert | Business rule validation | Planned |
