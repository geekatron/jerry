# WI-008c: Analyze Skill/Agent Structure

| Field | Value |
|-------|-------|
| **ID** | WI-008c |
| **Title** | Analyze skill and agent structure |
| **Type** | Research |
| **Status** | PENDING |
| **Priority** | HIGH |
| **Phase** | PHASE-02 |
| **Parent** | WI-008 |
| **Agent** | ps-researcher |
| **Assignee** | WT-Main |
| **Created** | 2026-01-12 |
| **Completed** | - |

---

## Description

Analyze the current skill and agent structure in Jerry to understand:
- How skills are defined (SKILL.md format)
- How agents are defined within skills
- How skills interact with projects
- What configuration skills need

This research ensures the domain model properly represents skills.

---

## Agent Invocation

### ps-researcher Prompt

```
You are the ps-researcher agent (v2.0.0).

## PS CONTEXT (REQUIRED)
- **PS ID:** PROJ-004
- **Entry ID:** e-007
- **Topic:** Jerry Skill/Agent Structure Analysis

## MANDATORY PERSISTENCE (P-002)
Create file at: projects/PROJ-004-jerry-config/research/PROJ-004-e-007-skill-agent-structure.md

## RESEARCH TASK

Analyze the skill and agent structure in Jerry:

### 1. Skill Definition Format
- What is the SKILL.md structure?
- What metadata is defined? (name, version, description)
- How are capabilities listed?
- What is the skill configuration model?

### 2. Agent Definitions
- How are agents defined within skills?
- What is the agent markdown format?
- How do ps-researcher, ps-architect, ps-validator, etc. work?
- What context do agents receive?

### 3. Skill Discovery
- How are skills discovered at runtime?
- Is there a skill registry?
- How does "/problem-solving" invoke the skill?
- What is the Skill tool's role?

### 4. Skill-Project Interaction
- How do skills know which project is active?
- Where do skills write their output? (project-relative?)
- Do skills have project-specific configuration?
- Can skills be enabled/disabled per project?

### 5. Skill Configuration Needs
- What configuration do skills need?
- Output directories per skill
- Agent model preferences
- Skill-specific settings

## FILES TO ANALYZE
- skills/problem-solving/SKILL.md
- skills/problem-solving/agents/*.md
- skills/worktracker/SKILL.md
- skills/architecture/SKILL.md
- Any skill-related code in src/

## OUTPUT FORMAT
Use L0/L1/L2 explanation levels.
Include actual file content excerpts with analysis.
Document configuration requirements discovered.
```

---

## Acceptance Criteria

- [ ] AC-008c.1: SKILL.md format documented
- [ ] AC-008c.2: Agent definition format analyzed
- [ ] AC-008c.3: Skill discovery mechanism understood
- [ ] AC-008c.4: Skill-project interaction documented
- [ ] AC-008c.5: Skill configuration needs identified
- [ ] AC-008c.6: Research artifact created at specified path

---

## Evidence

| Criterion | Evidence | Source |
|-----------|----------|--------|
| AC-008c.1 | - | - |
| AC-008c.2 | - | - |
| AC-008c.3 | - | - |
| AC-008c.4 | - | - |
| AC-008c.5 | - | - |
| AC-008c.6 | - | - |

---

## Current Skills to Analyze

| Skill | Location | Purpose |
|-------|----------|---------|
| problem-solving | `skills/problem-solving/` | ps-* agent orchestration |
| worktracker | `skills/worktracker/` | Work item management |
| architecture | `skills/architecture/` | System design guidance |

---

## Progress Log

| Timestamp | Update | Actor |
|-----------|--------|-------|
| 2026-01-12T12:00:00Z | Work item created | Claude |

---

## Dependencies

| Type | Work Item | Relationship |
|------|-----------|--------------|
| Part Of | WI-008 | Parent work item |
| Parallel With | WI-008a, WI-008b | Can run simultaneously |
| Blocks | WI-008f | Skill aggregate design |

---

## Related Artifacts

- **Output**: `research/PROJ-004-e-007-skill-agent-structure.md`
- **Skills Directory**: `skills/`
