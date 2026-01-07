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

## References

- [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/) - Alistair Cockburn
- [Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) - Anthropic
- [Context Rot Research](https://research.trychroma.com/context-rot) - Chroma
