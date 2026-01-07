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

## Available Agents

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
