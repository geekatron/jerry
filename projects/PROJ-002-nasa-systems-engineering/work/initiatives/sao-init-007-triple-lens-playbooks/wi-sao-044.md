---
id: wi-sao-044
title: "Document @ symbol agent invocation"
status: OPEN
parent: "_index.md"
initiative: sao-init-007
children: []
depends_on: []
blocks: []
created: "2026-01-12"
last_updated: "2026-01-12"
priority: P2
estimated_effort: "2h"
entry_id: sao-044
token_estimate: 400
---

# WI-SAO-044: Document @ Symbol Agent Invocation

> **Status:** 📋 OPEN
> **Priority:** P2 (MEDIUM)

---

## Description

Users need documentation on how to invoke agents using the @ symbol convention. This is a common pattern in Claude Code and other agent frameworks but is not documented in our playbooks.

**Gap:** No playbook mentions how to use `@ps-researcher`, `@nse-requirements`, etc.

---

## Acceptance Criteria

1. [ ] @ symbol syntax documented in each playbook
2. [ ] Examples of @ invocation for each agent family
3. [ ] Comparison: @ invocation vs Task tool invocation
4. [ ] When to use @ vs explicit Task tool
5. [ ] Updated SKILL.md files with @ syntax

---

## Tasks

### T-044.1: Research
- [ ] **T-044.1.1:** Research @ symbol convention in Claude Code
- [ ] **T-044.1.2:** Verify if @ symbol works with our agent definitions
- [ ] **T-044.1.3:** Document syntax: `@{agent-name} {prompt}`
- [ ] **T-044.1.4:** Test @ invocation with ps-* and nse-* agents

### T-044.2: Documentation
- [ ] **T-044.2.1:** Add "Agent Invocation" section to problem-solving PLAYBOOK.md
- [ ] **T-044.2.2:** Add "Agent Invocation" section to nasa-se PLAYBOOK.md
- [ ] **T-044.2.3:** Add "Agent Invocation" section to orchestration PLAYBOOK.md
- [ ] **T-044.2.4:** Update problem-solving SKILL.md with @ syntax
- [ ] **T-044.2.5:** Update nasa-se SKILL.md with @ syntax

### T-044.3: Examples
- [ ] **T-044.3.1:** Create quick reference table of @ invocations
- [ ] **T-044.3.2:** Add inline examples in playbooks
- [ ] **T-044.3.3:** Document when @ is preferred over Task tool

---

## Verification

| Evidence ID | Type | Description | Status |
|-------------|------|-------------|--------|
| E-044-001 | Research | @ syntax verified | ⏳ |
| E-044-002 | Content | Playbooks updated with @ documentation | ⏳ |
| E-044-003 | Content | SKILL.md files updated | ⏳ |

---

## Proposed Documentation Structure

```markdown
## Agent Invocation Methods

### Method 1: @ Symbol (Quick Invocation)

Use the @ symbol for simple, direct agent invocations:

```
@ps-researcher Research event sourcing patterns for task management
@ps-analyst Analyze the trade-offs between options A and B
@nse-requirements Define requirements for the authentication module
```

**Syntax:** `@{agent-name} {natural language prompt}`

### Method 2: Task Tool (Structured Invocation)

Use the Task tool for:
- Complex prompts with multiple parameters
- Workflow orchestration
- When you need explicit control over agent configuration

```python
Task(
    description="ps-researcher: Research event sourcing",
    subagent_type="general-purpose",
    prompt="..."
)
```

### When to Use Which

| Scenario | Recommended Method |
|----------|-------------------|
| Quick question | @ symbol |
| Single-agent task | @ symbol |
| Multi-agent workflow | Task tool |
| Custom parameters | Task tool |
| Structured output | Task tool |
```

---

## Research Questions

1. Does @ symbol work natively in Claude Code?
2. Do we need to configure anything for @ to work with our agents?
3. Is @ invocation different from slash commands (/architect, /commit)?
4. What are the limitations of @ invocation?

---

*Source: DISCOVERY-012 (GAP-012-004)*
*Created: 2026-01-12*
