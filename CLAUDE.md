# CLAUDE.md - Jerry Framework Root Context

> This file provides context to Claude Code at session start.
> It serves as **procedural memory** - loaded once, not maintained in context.

---

## Project Overview

**Jerry** is a framework for behavior and workflow guardrails that helps solve problems
while accruing a body of knowledge, wisdom, and experience.

### Core Problem: Context Rot

> "Context Rot is the phenomenon where an LLM's performance degrades as the context
> window fills up, even when total token count is well within the technical limit."
> — [Chroma Research](https://research.trychroma.com/context-rot)

Jerry addresses this through:
- **Filesystem as infinite memory** - Offload state to files
- **Work Tracker** - Persistent task state across sessions
- **Skills** - Compressed instruction interfaces
- **Structured knowledge** - `docs/` hierarchy for accumulated wisdom

---

## Architecture

```
jerry/
├── .claude/                    # Agent Governance Layer
├── .claude-plugin/             # Distribution Layer
├── skills/                     # Interface Layer (Natural Language)
├── scripts/                    # Execution Layer (CLI Shims)
├── src/                        # Hexagonal Core (Python)
│   ├── domain/                 # Pure Business Logic
│   ├── application/            # Use Cases (CQRS)
│   ├── infrastructure/         # Adapters (Persistence, Messaging)
│   └── interface/              # Primary Adapters (CLI, API)
└── docs/                       # Knowledge Repository
```

### Key Design Principles

1. **Hexagonal Architecture** (Ports & Adapters)
   - Domain has no external dependencies
   - Ports define contracts, adapters implement them
   - Dependency inversion: outer depends on inner

2. **Zero-Dependency Core**
   - Python stdlib only in domain/
   - Libraries allowed in infrastructure/ if pre-installed

3. **CQRS Pattern**
   - Commands: Write operations, return events
   - Queries: Read operations, return DTOs

---

## Working with Jerry

### Before Starting Work

1. Check `docs/plans/` for any active PLAN files
2. Review TODO state in Work Tracker skill
3. Read relevant `docs/knowledge/` for domain context

### During Work

1. Use Work Tracker to persist task state
2. Create PLAN files for complex changes
3. Document decisions in `docs/design/`

### After Completing Work

1. Update Work Tracker with completion status
2. Capture learnings in `docs/experience/` or `docs/wisdom/`
3. Commit with clear, semantic messages

---

## Skills Available

| Skill | Purpose | Location |
|-------|---------|----------|
| `worktracker` | Task/issue management | `skills/worktracker/SKILL.md` |
| `architecture` | System design guidance | `skills/architecture/SKILL.md` |
| `problem-solving` | Domain use case invocation | `skills/problem-solving/SKILL.md` |

---

## Agents Available

See `AGENTS.md` for the full registry. Key agents:

| Agent | Role | File |
|-------|------|------|
| Orchestrator | Conductor (Opus 4.5) | `.claude/agents/orchestrator.md` |
| QA Engineer | Test specialist | `.claude/agents/qa-engineer.md` |
| Security Auditor | Security review | `.claude/agents/security-auditor.md` |

---

## Code Standards

See `.claude/rules/coding-standards.md` for enforced rules.

Quick reference:
- Python 3.11+ with type hints
- 100 character line limit
- Domain layer: NO external imports
- All public functions: docstrings required

---

## Agent Governance (Jerry Constitution)

All agents operating within Jerry MUST adhere to the **Jerry Constitution v1.0**.

**Location:** `docs/governance/JERRY_CONSTITUTION.md`

### Core Principles (Quick Reference)

| ID | Principle | Enforcement |
|----|-----------|-------------|
| P-001 | Truth and Accuracy | Soft |
| P-002 | File Persistence | Medium |
| P-003 | No Recursive Subagents | **Hard** |
| P-010 | Task Tracking Integrity | Medium |
| P-020 | User Authority | **Hard** |
| P-022 | No Deception | **Hard** |

### Hard Principles (Cannot Override)

1. **P-003**: Maximum ONE level of agent nesting (orchestrator → worker)
2. **P-020**: User has ultimate authority; never override user decisions
3. **P-022**: Never deceive users about actions, capabilities, or confidence

### Self-Critique Protocol

Before finalizing significant outputs, agents SHOULD self-critique:

```
1. P-001: Is my information accurate and sourced?
2. P-002: Have I persisted significant outputs?
3. P-004: Have I documented my reasoning?
4. P-010: Is WORKTRACKER updated?
5. P-022: Am I being transparent about limitations?
```

### Behavioral Validation

Constitution compliance is validated via `docs/governance/BEHAVIOR_TESTS.md`:
- 14 test scenarios (golden dataset)
- LLM-as-a-Judge evaluation (industry standard per DeepEval, Datadog)
- Happy path, edge case, and adversarial coverage

**Industry Prior Art:**
- [Anthropic Constitutional AI](https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback)
- [OpenAI Model Spec](https://model-spec.openai.com/2025-12-18.html)
- [DeepEval G-Eval](https://deepeval.com/docs/metrics-llm-evals)

---

## References

- [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/) - Alistair Cockburn
- [Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) - Anthropic
- [Context Rot Research](https://research.trychroma.com/context-rot) - Chroma
