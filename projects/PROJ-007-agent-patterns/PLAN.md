# PROJ-007: Agent Patterns — Project Plan

> Research Claude Code agent and agent routing/trigger best practices to develop rules, patterns, and guides for building agents.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Objective](#objective) | What this project aims to achieve |
| [Scope](#scope) | What's in and out of scope |
| [Phases](#phases) | High-level execution phases |
| [Success Criteria](#success-criteria) | How we measure completion |

---

## Objective

Develop comprehensive rules, patterns, and guides for building Claude Code agents within the Jerry framework. Research best practices for agent routing, trigger design, prompt architecture, and tool usage to codify reusable patterns.

## Scope

**In scope:**
- Claude Code agent architecture and capabilities research
- Agent routing and trigger best practices
- Prompt design patterns for agents
- Tool selection and usage patterns
- Jerry-specific agent development guides
- Rules and standards for agent quality

**Out of scope:**
- Multi-model agent orchestration (covered by PROJ-006)
- Agent SDK/API development
- Production deployment patterns

## Phases

| Phase | Description | Status |
|-------|-------------|--------|
| 1. Research | 4 agents (3 PS + 1 NSE): Survey Claude Code agent capabilities, routing mechanisms, community patterns, external frameworks | DONE |
| 2. Analysis | 6 agents (3 PS + 3 NSE): Synthesize findings into pattern families, requirement sets, integration patterns | DONE |
| 3. Synthesis & Design | 5 agents (3 PS + 2 NSE): Unified pattern taxonomy, ADRs, V&V plan, integration patterns | DONE |
| 4. Codification | 4 agents (2 PS + 2 NSE): Rule files, config baseline, constitutional validation, QA audit | DONE |
| 5. Review & Quality Gate | 5 agents (3 PS + 2 NSE): Design review, quality scoring, CDR gate, C4 tournament (10 strategies) | DONE |
| 6. Gap Closure & Publication | EN-003: Close 3 Anthropic best practice gaps (PM-M-001, ET-M-001, FC-M-001) + publish comparison | IN PROGRESS |

### Phase 6 Details (EN-003)

Comparison of Jerry Framework against Anthropic's official Claude Code best practices revealed:
- **Perfect alignment** on 9 core areas (P-003 subagent depth, context rot, hooks, CLAUDE.md, tools, H-31 ambiguity)
- **12+ innovations** beyond what Anthropic documents (quality gate, adversarial strategies, FMEA, etc.)
- **3 gaps** where Anthropic recommends practices not yet codified (plan mode, extended thinking, fresh context review)

All gaps closed as MEDIUM standards (no HARD rule ceiling impact, no L2 budget impact).

## Success Criteria

- Documented agent architecture patterns applicable to Jerry skills
- Routing/trigger decision framework with clear selection criteria
- Agent development guide with templates and examples
- Rules integrated into `.context/rules/` for enforcement
- Comparison artifact documenting Jerry-vs-Anthropic alignment and innovations
