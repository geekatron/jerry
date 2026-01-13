---
id: wi-sao-044
title: "Document @ symbol agent invocation"
status: COMPLETE
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

> **Status:** ✅ COMPLETE
> **Priority:** P2 (MEDIUM)
> **Resolution:** Research clarified @ symbol is NOT an agent invocation method

---

## Description

Users need documentation on how to invoke agents using the @ symbol convention. This is a common pattern in Claude Code and other agent frameworks but is not documented in our playbooks.

**Gap:** No playbook mentions how to use `@ps-researcher`, `@nse-requirements`, etc.

## Research Finding (2026-01-12)

**@ Symbol is NOT for agent invocation in Claude Code.**

The @ symbol in Claude Code is used for **file mentions**, not agent invocation. Agent invocation in Jerry uses:

| Method | Syntax | Use Case |
|--------|--------|----------|
| Natural Language | "Research X", "Analyze Y" | Quick, keyword-activated |
| Explicit Request | "Use ps-researcher to X" | Specific agent selection |
| Task Tool | `Task(subagent_type=...)` | Programmatic workflows |

**Evidence:** Grep for `@ps-` and `@nse-` found zero usage in codebase. SKILL.md documents 3 invocation methods, none using @ symbol.

**Conclusion:** WI-SAO-044 gap is based on incorrect assumption. Documentation already covers agent invocation methods adequately in SKILL.md and PLAYBOOK.md.

---

## Acceptance Criteria

1. [x] Research @ symbol convention in Claude Code (Result: NOT for agents)
2. [x] Verify existing invocation documentation is adequate (SKILL.md covers 3 methods)
3. [x] Document finding that @ is for file mentions, not agent invocation
4. [N/A] @ syntax not applicable - use existing methods instead
5. [N/A] SKILL.md already documents correct invocation methods

---

## Tasks

### T-044.1: Research
- [x] **T-044.1.1:** Research @ symbol convention in Claude Code (@ is for file mentions)
- [x] **T-044.1.2:** Verify if @ symbol works with our agent definitions (it does not)
- [x] **T-044.1.3:** Grep codebase for @ps-* and @nse-* usage (0 results)
- [x] **T-044.1.4:** Review SKILL.md invocation methods (3 methods documented)

### T-044.2: Documentation (N/A - @ not applicable)
- [N/A] **T-044.2.1:** @ syntax not used - existing invocation docs adequate
- [N/A] **T-044.2.2:** PLAYBOOK.md already has "Invocation Methods" section
- [N/A] **T-044.2.3:** SKILL.md already documents correct methods

### T-044.3: Clarification
- [x] **T-044.3.1:** Document research finding in this work item
- [x] **T-044.3.2:** Clarify @ is for file mentions, not agent invocation
- [x] **T-044.3.3:** Close gap as "based on incorrect assumption"

---

## Verification

| Evidence ID | Type | Description | Status |
|-------------|------|-------------|--------|
| E-044-001 | Research | @ symbol researched - NOT for agents | ✅ Complete |
| E-044-002 | Research | Existing invocation docs verified adequate | ✅ Complete |
| E-044-003 | Finding | Gap based on incorrect assumption - closed | ✅ Complete |

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
