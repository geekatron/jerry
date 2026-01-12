# Jerry Framework Installation Guide

> Jerry is a Claude Code Plugin for behavior and workflow guardrails.

---

## Prerequisites

- **Claude Code** (CLI) installed and configured
- **Python 3.11+** (for development/testing)
- **Git** (for version control integration)

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

For development or contributing:

```bash
# Clone the repository
git clone https://github.com/geekatron/jerry.git
cd jerry

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate  # Windows

# Install in development mode
pip install -e ".[dev,test]"

# Verify installation
jerry --help
```

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

3. **"Python version mismatch"**

   Jerry requires Python 3.11+. Check your version:

   ```bash
   python3 --version
   ```

4. **"Dependencies not found"**

   Install development dependencies:

   ```bash
   pip install -e ".[dev,test]"
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
