# Contributing to Jerry Framework

## Development Setup

### Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) package manager
- [Git](https://git-scm.com/)

### First-Time Setup (REQUIRED)

After cloning the repository or creating a new worktree:

**macOS / Linux:**
```bash
make setup
```

**Windows (Git Bash or PowerShell):**
```bash
uv sync
uv run pre-commit install
```

This:
1. Installs all dependencies via `uv sync`
2. Installs pre-commit hooks for automatic quality checks

**Important:** The pre-commit hooks ensure tests run before every commit. Skipping setup means tests won't run automatically, and broken code may be committed.

### Windows-Specific Notes

Jerry's development tooling works on Windows via Git Bash (included with [Git for Windows](https://git-scm.com/download/win)). Here are the key differences:

| Topic | macOS/Linux | Windows |
|-------|-------------|---------|
| Setup | `make setup` | `uv sync && uv run pre-commit install` |
| Make targets | `make test`, `make lint`, etc. | Use the `uv run` commands directly (see table below) |
| Shell | bash/zsh | Git Bash (recommended) or PowerShell |
| Path separators | Forward slashes | Git Bash handles both; tests use `Path()` for portability |

**Make target equivalents for Windows:**

| Make Target | Direct Command |
|-------------|----------------|
| `make setup` | `uv sync && uv run pre-commit install` |
| `make test` | `uv run pytest --tb=short -q` |
| `make test-verbose` | `uv run pytest -v` |
| `make test-cov` | `uv run pytest --cov=src --cov-report=term-missing --cov-report=html` |
| `make test-unit` | `uv run pytest tests/unit/ tests/*/unit/ -v` |
| `make test-integration` | `uv run pytest tests/integration/ -v` |
| `make test-contract` | `uv run pytest tests/contract/ -v` |
| `make lint` | `uv run ruff check src/ tests/ && uv run pyright src/` |
| `make format` | `uv run ruff check --fix src/ tests/ && uv run ruff format src/ tests/` |
| `make pre-commit` | `uv run pre-commit run --all-files` |

**Installing uv on Windows:**

```powershell
# PowerShell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Close and reopen your terminal after installing. Verify with `uv --version`.

### Git Worktrees

This repository uses git worktrees for parallel development. When creating a new worktree:

```bash
# From main repo
git worktree add ../my-feature-branch feature/my-feature

# In the new worktree
cd ../my-feature-branch

# macOS/Linux
make setup

# Windows
uv sync && uv run pre-commit install
```

**Important:** Pre-commit hooks live in the main `.git/hooks/` directory (shared across worktrees), but `pre-commit install` stamps an **absolute path** to the Python interpreter inside the hook file. If you create a new worktree or rebuild the venv, the path goes stale and hooks will silently fail. **Always run `uv run pre-commit install`** (or `make setup`) after creating a worktree or rebuilding the virtual environment. The session start hook will warn you if it detects a stale path.

## Development Workflow

### Running Tests

**macOS / Linux:**
```bash
make test              # Full test suite (quick)
make test-verbose      # With detailed output
make test-cov          # With coverage report
make test-unit         # Unit tests only
make test-integration  # Integration tests only
make test-contract     # Contract tests only
```

**All platforms (direct commands):**
```bash
uv run pytest --tb=short -q           # Full test suite
uv run pytest -v                      # Verbose output
uv run pytest tests/unit/ -v          # Unit tests only
uv run pytest tests/integration/ -v   # Integration tests only
```

### Code Quality

**macOS / Linux:**
```bash
make lint              # Run linters (ruff + pyright)
make format            # Auto-format code
make check             # Run lint + test
make pre-commit        # Run all pre-commit hooks
```

**All platforms (direct commands):**
```bash
uv run ruff check src/ tests/         # Lint
uv run pyright src/                    # Type check
uv run ruff format src/ tests/        # Format
uv run pre-commit run --all-files     # All pre-commit hooks
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
| validate-plugin-manifests | JSON schema validation for plugin files |
| pip-audit | Security scan (pre-push only) |

To skip hooks in emergencies:
```bash
# Skip specific hook
SKIP=pytest git commit -m "message"

# Skip all hooks (use sparingly)
git commit --no-verify -m "message"
```

## Code Standards

- See `.context/rules/coding-standards.md` for detailed standards
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

## Reporting Windows Issues

If you encounter a problem that only occurs on Windows, please use the dedicated [Windows Compatibility issue template](https://github.com/geekatron/jerry/issues/new?template=windows-compatibility.yml). This helps the team triage platform-specific issues separately from general bugs.

**What to include:**
- Windows version and shell (PowerShell, Git Bash, CMD)
- `uv --version` and `claude --version` output
- Steps to reproduce the issue
- Error messages or unexpected behavior

Even minor issues are valuable — they help us identify portability gaps that automated testing may miss.

## Submitting Feature Requests

Have an idea for Jerry? Use the [Feature Request issue template](https://github.com/geekatron/jerry/issues/new?template=feature-request.yml) to submit it. The template fields map directly to our internal work tracking structure, so the more detail you provide, the faster we can evaluate and prioritize your request.

**Key fields:**

| Field | Purpose | Required |
|-------|---------|----------|
| Feature Title | A concise name for the feature | Yes |
| Summary | What does it do and why is it useful? | Yes |
| Problem or Use Case | What problem does this solve? | Yes |
| Expected Benefit | Frame as: "We believe [feature] will result in [outcome]" | No |
| Suggested Acceptance Criteria | Testable conditions for "done" | No |
| Suggested Priority | How important is this to your workflow? | Yes |

Feature requests are reviewed and, if accepted, added to the project backlog as tracked work items.

## Questions?

- Check `CLAUDE.md` for AI assistant context
- Review ADRs in `docs/design/` for architectural decisions
- Open an issue for questions or problems
