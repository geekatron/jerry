# Jerry Framework Installation Guide

> Jerry is a Claude Code Plugin for behavior and workflow guardrails.

---

## Prerequisites

- **Claude Code** (CLI) installed and configured
- **Python 3.11+** (required - see [Python Version Requirements](#python-version-requirements))
- **Git** (for version control integration)
- **uv** (required for plugin mode - see [uv Requirements](#uv-requirements))

### Python Version Requirements

Jerry requires **Python 3.11 or later**. This is enforced in `pyproject.toml`:

```toml
requires-python = ">=3.11"
```

**Why Python 3.11+?**
- Enhanced type hints (Self, TypeVarTuple)
- Performance improvements (10-60% faster)
- Better error messages
- tomllib in stdlib (PEP 680)

**Verify your Python version:**

```bash
python3 --version
# Should show Python 3.11.x or later

# On macOS, system Python is 3.9.6 (too old)
# Install via Homebrew or uv:
brew install python@3.14
# or
uv python install 3.14
```

**Supported versions:**
| Version | Status | Notes |
|---------|--------|-------|
| 3.14 | Supported | Latest, recommended |
| 3.13 | Supported | Stable |
| 3.12 | Supported | LTS-like stability |
| 3.11 | Supported | Minimum version |
| 3.10 | Not supported | Missing required features |

### uv Requirements

Jerry's plugin hooks use [uv](https://docs.astral.sh/uv/) to run Python scripts with automatic dependency resolution. This is **required** for plugin mode (when installed via Claude Code's plugin system).

**Why uv is required:**
- The SessionStart hook uses `uv run` to execute Python scripts
- uv automatically resolves dependencies using PEP 723 inline script metadata
- No manual `pip install -e .` required after installation
- Works immediately on fresh clones

**Install uv:**

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Verify installation
uv --version
```

**Note:** For development (git clone), you can use either uv or pip. For plugin mode (installed via Claude Code marketplace), uv is required.

---

## Installation Methods

### Method 1: GitHub Release (Recommended)

1. **Download the release archive** from [GitHub Releases](https://github.com/geekatron/jerry/releases)

   ```bash
   # Download the latest release
   curl -LO https://github.com/geekatron/jerry/releases/latest/download/jerry-plugin-X.Y.Z.tar.gz
   ```

2. **Verify the download** (optional but recommended)

   ```bash
   curl -LO https://github.com/geekatron/jerry/releases/latest/download/checksums.sha256
   sha256sum -c checksums.sha256
   ```

3. **Extract to your project directory**

   ```bash
   # Extract to current directory
   tar -xzf jerry-plugin-X.Y.Z.tar.gz

   # Or extract to a specific location
   tar -xzf jerry-plugin-X.Y.Z.tar.gz -C /path/to/your/project
   ```

4. **Verify installation**

   ```bash
   # Check that CLAUDE.md exists
   ls -la CLAUDE.md

   # Check plugin structure
   ls -la .claude/ skills/ src/
   ```

### Method 2: Git Clone (Development)

For development or contributing, you have two options: **uv (recommended)** or **standard pip**.

#### Option A: Using uv (Recommended)

[uv](https://docs.astral.sh/uv/) is a fast Python package manager that creates standard virtual environments.

```bash
# Clone the repository
git clone https://github.com/geekatron/jerry.git
cd jerry

# Install uv if you don't have it
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Sync dependencies (creates .venv automatically)
uv sync

# Run tests
uv run pytest

# Run Jerry CLI
uv run jerry --help
```

**Why uv?**
- 10-100x faster than pip ([benchmark](https://realpython.com/uv-vs-pip/))
- Creates PEP 405 compliant virtual environments
- Built-in Python version management
- Single binary, no Python dependency to install uv itself

#### Option B: Using Standard pip/venv

If you prefer the standard Python tools or don't have uv:

```bash
# Clone the repository
git clone https://github.com/geekatron/jerry.git
cd jerry

# Create virtual environment (Python 3.11+ required)
python3 -m venv .venv

# Activate the environment
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements-test.txt  # Test dependencies
pip install -e .                       # Install jerry in editable mode

# Verify installation
pytest
jerry --help
```

**Requirements files available:**
| File | Contents |
|------|----------|
| `requirements.txt` | Core dependencies (minimal) |
| `requirements-dev.txt` | Development tools (mypy, ruff) |
| `requirements-test.txt` | Testing tools (pytest, coverage) |

---

## Directory Structure

After installation, your project should have:

```
your-project/
├── .claude/                 # Claude Code hooks and configuration
│   ├── settings.json        # Claude Code settings
│   ├── hooks/               # SessionStart, PreToolUse, etc.
│   ├── agents/              # Agent definitions
│   └── rules/               # Coding standards, principles
├── .claude-plugin/          # Plugin manifest (optional)
├── skills/                  # Natural language interfaces
│   ├── worktracker/         # Work tracking skill
│   ├── architecture/        # Architecture guidance skill
│   └── problem-solving/     # Problem solving skill
├── src/                     # Hexagonal core (Python)
│   ├── domain/              # Pure business logic
│   ├── application/         # Use cases (CQRS)
│   ├── infrastructure/      # Adapters
│   └── interface/           # Primary adapters (CLI)
├── docs/                    # Documentation
├── CLAUDE.md                # Context for Claude Code
├── AGENTS.md                # Agent registry
└── GOVERNANCE.md            # Governance principles
```

---

## Configuration

### Project Setup

Jerry uses project-based workflows. To start working on a project:

1. **Set the project environment variable**

   ```bash
   export JERRY_PROJECT=PROJ-001-my-project
   ```

2. **Create the project directory** (if new)

   ```bash
   mkdir -p projects/PROJ-001-my-project/.jerry/data/items
   ```

3. **Create project files**

   - `projects/PROJ-001-my-project/PLAN.md` - Implementation plan
   - `projects/PROJ-001-my-project/WORKTRACKER.md` - Work tracking

### Verify Configuration

Use the Jerry CLI to verify your setup:

```bash
# Check project context
jerry init

# List available projects
jerry projects list

# Validate a project
jerry projects validate PROJ-001-my-project
```

---

## Using Jerry with Claude Code

Once installed, Jerry enhances your Claude Code experience:

### Skills

Skills provide natural language interfaces:

```
# In Claude Code conversation
/worktracker add "Implement user authentication"
/architecture review "src/domain/user.py"
/problem-solving analyze "Why is the test failing?"
```

### Hooks

Hooks run automatically at key points:

- **SessionStart**: Loads project context
- **PreToolUse**: Validates tool usage
- **PostToolUse**: Updates work tracking

### Agents

Agents handle specialized tasks:

- **Orchestrator**: Coordinates multi-step workflows
- **QA Engineer**: Test validation
- **Security Auditor**: Security review

---

## Troubleshooting

### Common Issues

1. **"JERRY_PROJECT not set"**

   ```bash
   export JERRY_PROJECT=PROJ-001-my-project
   ```

2. **"Project not found"**

   ```bash
   # List available projects
   jerry projects list

   # Create the project directory
   mkdir -p projects/PROJ-XXX-name/.jerry/data/items
   ```

3. **"Python version mismatch" or "requires-python>=3.11"**

   Jerry requires Python 3.11+. Check your version:

   ```bash
   python3 --version
   # If below 3.11, install a newer version:

   # macOS (Homebrew)
   brew install python@3.14

   # Or using uv
   uv python install 3.14
   ```

4. **"Dependencies not found" (pip)**

   Install dependencies using requirements files:

   ```bash
   pip install -r requirements-test.txt
   pip install -e .
   ```

5. **"uv: command not found"**

   Install uv:

   ```bash
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Add to PATH (if needed)
   export PATH="$HOME/.cargo/bin:$PATH"
   ```

6. **"ModuleNotFoundError: No module named 'src'"**

   The package isn't installed in editable mode. Fix:

   ```bash
   # With uv
   uv pip install -e .

   # With pip
   pip install -e .
   ```

7. **Tests fail with import errors**

   Ensure you're using the virtual environment:

   ```bash
   # Check which Python is being used
   which python
   # Should show .venv/bin/python

   # If not, activate the environment
   source .venv/bin/activate
   ```

### Getting Help

- **GitHub Issues**: [github.com/geekatron/jerry/issues](https://github.com/geekatron/jerry/issues)
- **Documentation**: `docs/` directory
- **Claude Code**: `/help` for built-in help

---

## Upgrading

To upgrade to a new version:

1. **Download the new release**

   ```bash
   curl -LO https://github.com/geekatron/jerry/releases/latest/download/jerry-plugin-X.Y.Z.tar.gz
   ```

2. **Backup your projects** (optional)

   ```bash
   cp -r projects/ projects.backup/
   ```

3. **Extract over existing installation**

   ```bash
   tar -xzf jerry-plugin-X.Y.Z.tar.gz --overwrite
   ```

4. **Verify upgrade**

   ```bash
   jerry --version
   ```

---

## Uninstallation

To remove Jerry:

1. **Remove plugin files**

   ```bash
   rm -rf .claude/ .claude-plugin/ skills/ src/ docs/ scripts/ hooks/
   rm -f CLAUDE.md AGENTS.md GOVERNANCE.md pyproject.toml pytest.ini
   ```

2. **Keep your projects** (optional)

   The `projects/` directory contains your work and is not part of the plugin.

---

## License

Jerry Framework is open source. See the LICENSE file for details.
