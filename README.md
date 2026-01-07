# Jerry Framework

> A framework for behavior and workflow guardrails with knowledge accrual.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Architecture: Hexagonal](https://img.shields.io/badge/Architecture-Hexagonal-green.svg)](https://alistair.cockburn.us/hexagonal-architecture/)

## Problem Statement

**Context Rot** is the phenomenon where LLM performance degrades as the context window fills,
even well within technical limits. Jerry addresses this through structured knowledge management
and persistent work tracking.

> "The effective context window where models perform optimally is often <256k tokens,
> far below advertised limits."
> — [Chroma Research](https://research.trychroma.com/context-rot)

## Features

- **Work Tracker**: Local Azure DevOps/JIRA equivalent for persistent task management
- **Skills System**: Natural language interfaces to domain capabilities
- **Agent Governance**: Hooks, rules, and sub-agent coordination
- **Knowledge Accrual**: Structured documentation for wisdom capture
- **Hexagonal Architecture**: Clean separation of concerns with ports and adapters

## Architecture

```
jerry/
├── .claude/                    # Agent Governance Layer
│   ├── agents/                 # Sub-agent personas
│   ├── commands/               # Slash commands
│   ├── hooks/                  # Event-driven orchestration
│   └── rules/                  # Persistent constraints
│
├── skills/                     # Interface Layer (Natural Language)
│   ├── worktracker/            # Task management skill
│   ├── architecture/           # System design skill
│   └── problem-solving/        # Domain use case skill
│
├── src/                        # Hexagonal Core (Python)
│   ├── domain/                 # Pure business logic (no deps)
│   ├── application/            # Use cases (CQRS)
│   ├── infrastructure/         # Adapters (persistence, messaging)
│   └── interface/              # Primary adapters (CLI, API)
│
├── scripts/                    # Execution Layer (CLI shims)
└── docs/                       # Knowledge Repository
```

## Installation

```bash
# Clone the repository
git clone https://github.com/geekatron/jerry.git
cd jerry

# Install with uv (recommended)
uv pip install -e .

# Or with pip
pip install -e .
```

## Quick Start

```bash
# Run Jerry CLI
jerry --help

# Or invoke scripts directly
python scripts/invoke_use_case.py <command>
```

## Design Principles

1. **Zero-Dependency Core**: Domain layer uses Python stdlib only
2. **Hexagonal Architecture**: Ports define contracts, adapters implement them
3. **CQRS**: Commands for writes, queries for reads
4. **Evidence-Based**: All decisions require citations and references
5. **Knowledge Capture**: Learnings persist in structured documentation

## Documentation

| Document | Purpose |
|----------|---------|
| [CLAUDE.md](./CLAUDE.md) | Root context for Claude Code sessions |
| [AGENTS.md](./AGENTS.md) | Registry of available sub-agents |
| [GOVERNANCE.md](./GOVERNANCE.md) | Protocols for planning and handoffs |
| [docs/research/](./docs/research/) | Research artifacts with citations |

## Technology Stack

- **Language**: Python 3.11+ (zero-dependency core)
- **Architecture**: Hexagonal (Ports & Adapters)
- **Persistence**: SQLite (stdlib), Markdown files
- **CLI**: argparse (stdlib)
- **Testing**: unittest (stdlib)

See [docs/research/TECHNOLOGY_STACK_ANALYSIS.md](./docs/research/TECHNOLOGY_STACK_ANALYSIS.md) for the full analysis.

## Contributing

1. Read [GOVERNANCE.md](./GOVERNANCE.md) for protocols
2. Create a PLAN file for significant changes
3. Follow coding standards in `.claude/rules/`
4. Ensure all quality gates pass

## References

- Cockburn, A. (2005). "[Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/)"
- Anthropic. (2025). "[Effective Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)"
- Chroma. "[Context Rot Research](https://research.trychroma.com/context-rot)"

## License

MIT
