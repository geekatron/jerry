# Contributing to Jerry Framework

## Development Setup

### Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) package manager

### First-Time Setup (REQUIRED)

After cloning the repository or creating a new worktree:

```bash
make setup
```

This command:
1. Installs all dependencies via `uv sync`
2. Installs pre-commit hooks for automatic quality checks

**Important:** The pre-commit hooks ensure tests run before every commit. Skipping setup means tests won't run automatically, and broken code may be committed.

### Git Worktrees

This repository uses git worktrees for parallel development. When creating a new worktree:

```bash
# From main repo
git worktree add ../my-feature-branch feature/my-feature

# In the new worktree
cd ../my-feature-branch
make setup  # REQUIRED - hooks are shared but setup ensures deps are ready
```

Note: Pre-commit hooks are shared across all worktrees (they live in the main `.git/hooks/` directory). Running `make setup` once installs hooks for ALL worktrees.

## Development Workflow

### Running Tests

```bash
make test              # Full test suite (quick)
make test-verbose      # With detailed output
make test-cov          # With coverage report
make test-unit         # Unit tests only
make test-integration  # Integration tests only
make test-contract     # Contract tests only
```

### Code Quality

```bash
make lint              # Run linters (ruff + pyright)
make format            # Auto-format code
make check             # Run lint + test
make pre-commit        # Run all pre-commit hooks
```

### Pre-commit Hooks

The following checks run automatically before each commit:

| Hook | Purpose |
|------|---------|
| trailing-whitespace | Remove trailing whitespace |
| end-of-file-fixer | Ensure files end with newline |
| check-yaml | Validate YAML syntax |
| ruff | Python linting + auto-fix |
| ruff-format | Python formatting |
| pyright | Type checking |
| pytest | Full test suite |
| pip-audit | Security scan (pre-push only) |

To skip hooks in emergencies:
```bash
# Skip specific hook
SKIP=pytest git commit -m "message"

# Skip all hooks (use sparingly)
git commit --no-verify -m "message"
```

## Code Standards

- See `.claude/rules/coding-standards.md` for detailed standards
- Follow hexagonal architecture patterns in `.claude/patterns/`
- Use type hints on all public functions
- Write tests before implementation (TDD)

## Project Structure

```
jerry/
├── src/                  # Application code (hexagonal architecture)
│   ├── domain/           # Business logic (no external deps)
│   ├── application/      # Use cases (CQRS)
│   ├── infrastructure/   # Adapters
│   └── interface/        # CLI, API
├── tests/                # Test suites
│   ├── unit/             # Fast, isolated tests
│   ├── integration/      # Adapter tests
│   └── contract/         # Schema/API contract tests
├── skills/               # Natural language interfaces
└── docs/                 # Documentation
```

## Questions?

- Check `CLAUDE.md` for AI assistant context
- Review ADRs in `docs/design/` for architectural decisions
- Open an issue for questions or problems
