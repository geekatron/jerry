# Jerry Framework Installation Guide

> Jerry is a Claude Code plugin for behavior and workflow guardrails.

---

## Table of Contents

| Section | Description |
|---------|-------------|
| [Prerequisites](#prerequisites) | What you need before installing |
| [Installation](#installation) | Platform-specific setup instructions |
| [Verification](#verification) | How to confirm installation succeeded |
| [Configuration](#configuration) | Post-installation setup |
| [Using Jerry](#using-jerry) | Getting started with skills |
| [Troubleshooting](#troubleshooting) | Common issues and solutions |
| [For Developers](#for-developers) | Contributing and development setup |
| [Uninstallation](#uninstallation) | How to remove Jerry |

---

## Prerequisites

### Required Software

| Software | Version | Purpose | Install Guide |
|----------|---------|---------|---------------|
| [Claude Code](https://code.claude.com) | Latest | The AI coding assistant Jerry extends | [Setup Guide](https://code.claude.com/docs/en/setup) |
| [Git](https://git-scm.com/) | 2.0+ | Clone the Jerry repository | [Download](https://git-scm.com/downloads) |
| [uv](https://docs.astral.sh/uv/) | Latest | Python dependency management for hooks | See platform instructions below |

> **Note:** You do NOT need Python installed to use Jerry as an end user. Python and uv are used internally by Jerry's hooks. The uv installer handles Python automatically.

### System Requirements

| Requirement | Minimum |
|-------------|---------|
| Disk Space | ~100 MB |
| Internet | Required for initial clone |

---

## Installation

Jerry is installed as a **Claude Code plugin** via a local marketplace. This is a two-step process:

1. **Add the marketplace** - Registers Jerry's plugin catalog with Claude Code
2. **Install the plugin** - Downloads and activates Jerry's skills

Choose your platform below:

---

### macOS

#### Step 1: Install uv

uv is required for Jerry's hooks to execute Python scripts with automatic dependency resolution.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Restart your terminal (close and reopen), then verify:

```bash
uv --version
# Should output: uv 0.x.x
```

#### Step 2: Clone Jerry

Clone the repository to a location on your system. We recommend `~/plugins/`:

```bash
mkdir -p ~/plugins
git clone https://github.com/geekatron/jerry.git ~/plugins/jerry
```

#### Step 3: Verify the Plugin Manifest

Confirm Jerry's plugin manifest exists:

```bash
cat ~/plugins/jerry/.claude-plugin/plugin.json
```

You should see JSON output with `"name": "jerry"`.

#### Step 4: Add the Local Marketplace

Open Claude Code and run:

```
/plugin marketplace add ~/plugins/jerry
```

This registers Jerry's plugin catalog. No plugins are installed yet—you're just adding the "app store."

#### Step 5: Install the Plugin

Install Jerry from the marketplace:

```
/plugin install jerry-framework@jerry
```

**Alternative: Interactive Installation**
1. Run `/plugin`
2. Go to the **Discover** tab
3. Find `jerry-framework`
4. Press Enter and select your installation scope:
   - **User** (recommended): Install for yourself across all projects
   - **Project**: Install for all collaborators on this repository
   - **Local**: Install for yourself in this repository only

---

### Windows

#### Step 1: Install uv

Open **PowerShell** (not Command Prompt) and run:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Important:** Close and reopen PowerShell to update your PATH.

Verify the installation:

```powershell
uv --version
# Should output: uv 0.x.x
```

If you see "command not found," ensure this path is in your system PATH:
```
%USERPROFILE%\.local\bin
```

#### Step 2: Clone Jerry

Clone the repository using PowerShell:

```powershell
# Create plugins directory
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\plugins"

# Clone Jerry
git clone https://github.com/geekatron/jerry.git "$env:USERPROFILE\plugins\jerry"
```

**Alternative using Git Bash:**
```bash
mkdir -p ~/plugins
git clone https://github.com/geekatron/jerry.git ~/plugins/jerry
```

#### Step 3: Verify the Plugin Manifest

Confirm Jerry's plugin manifest exists:

```powershell
Get-Content "$env:USERPROFILE\plugins\jerry\.claude-plugin\plugin.json"
```

You should see JSON output with `"name": "jerry"`.

#### Step 4: Add the Local Marketplace

Open Claude Code and run (note: use **forward slashes** in Claude Code):

```
/plugin marketplace add C:/Users/YOUR_USERNAME/plugins/jerry
```

Replace `YOUR_USERNAME` with your actual Windows username.

**Tip:** You can find your username by running `echo $env:USERNAME` in PowerShell.

#### Step 5: Install the Plugin

Install Jerry from the marketplace:

```
/plugin install jerry-framework@jerry
```

---

## Verification

### Check Plugin Installation

1. In Claude Code, run `/plugin`
2. Go to the **Installed** tab
3. Verify `jerry-framework` appears in the list

### Check for Errors

1. Run `/plugin`
2. Go to the **Errors** tab
3. Verify no errors related to `jerry-framework`

### Test a Skill

Run a simple skill to verify everything works:

```
/problem-solving
```

You should see the problem-solving skill activate with information about available agents.

---

## Configuration

### Installation Scopes Explained

When installing plugins, you choose a scope that determines where the plugin is available:

| Scope | Where Installed | Use Case |
|-------|-----------------|----------|
| **User** (default) | Your user settings | Personal use across all your projects |
| **Project** | `.claude/settings.json` | Shared with team—all collaborators get the plugin |
| **Local** | Your local repo config | Testing—only you, only this repo |

**Recommendation:** Use **User** scope for personal use. Use **Project** scope when you want your whole team to have Jerry available.

### Project Setup (Optional)

Jerry uses project-based workflows for organizing work. To set up a project:

1. **Set the project environment variable:**

   ```bash
   # macOS/Linux
   export JERRY_PROJECT=PROJ-001-my-project

   # Windows PowerShell
   $env:JERRY_PROJECT = "PROJ-001-my-project"
   ```

2. **Create project structure:**

   ```bash
   # macOS/Linux
   mkdir -p projects/PROJ-001-my-project/.jerry/data/items

   # Windows PowerShell
   New-Item -ItemType Directory -Force -Path "projects\PROJ-001-my-project\.jerry\data\items"
   ```

The SessionStart hook will automatically load project context when you start Claude Code.

---

## Using Jerry

### Available Skills

After installation, these skills are available via slash commands:

| Skill | Command | Purpose |
|-------|---------|---------|
| Problem-Solving | `/problem-solving` | Research, analysis, architecture decisions |
| Work Tracker | `/worktracker` | Task and work item management |
| NASA SE | `/nasa-se` | Systems engineering processes (NPR 7123.1D) |
| Orchestration | `/orchestration` | Multi-phase workflow coordination |
| Architecture | `/architecture` | Design decisions and ADRs |
| Transcript | `/transcript` | Meeting transcript parsing |

### Example Usage

**Research a topic:**
```
/problem-solving research OAuth2 implementation patterns for Python
```

**Create a work item:**
```
/worktracker add "Implement user authentication"
```

**Make an architecture decision:**
```
/architecture create ADR for choosing PostgreSQL over SQLite
```

### Persistent Artifacts

All skill outputs are saved to files in your project:

| Output Type | Location |
|-------------|----------|
| Research | `docs/research/` |
| Analysis | `docs/analysis/` |
| Decisions (ADRs) | `docs/decisions/` |
| Reviews | `docs/reviews/` |
| Reports | `docs/reports/` |

These files survive context compaction and session boundaries, building your project's knowledge base over time.

---

## Troubleshooting

### Plugin Command Not Recognized

**Symptom:** `/plugin` command not found or doesn't work

**Solution:** Update Claude Code to the latest version:
- **macOS (Homebrew):** `brew upgrade claude-code`
- **npm:** `npm update -g @anthropic-ai/claude-code`

Plugin support requires Claude Code version 1.0.33 or later.

### Plugin Not Found After Adding Marketplace

**Symptom:** `/plugin install jerry-framework@jerry` returns "plugin not found"

**Solutions:**
1. Verify the marketplace was added: `/plugin marketplace list`
2. Check the path is correct and Jerry was cloned successfully
3. Refresh the marketplace: `/plugin marketplace update jerry`
4. Verify the manifest exists: `cat ~/plugins/jerry/.claude-plugin/plugin.json`

### uv: command not found

**Symptom:** Hooks fail with "uv: command not found"

**Solution (macOS):**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# Restart your terminal
```

**Solution (Windows):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
# Close and reopen PowerShell
```

If still not found, add to PATH manually:
- macOS: `export PATH="$HOME/.local/bin:$PATH"` (add to `~/.zshrc`)
- Windows: Add `%USERPROFILE%\.local\bin` to System PATH

### Skills Not Appearing

**Symptom:** Installed plugin but `/problem-solving` doesn't work

**Solutions:**
1. Check the **Errors** tab in `/plugin`
2. Clear the plugin cache:
   - macOS: `rm -rf ~/.claude/plugins/cache`
   - Windows: `Remove-Item -Recurse -Force "$env:USERPROFILE\.claude\plugins\cache"`
3. Restart Claude Code
4. Reinstall the plugin: `/plugin uninstall jerry-framework@jerry` then `/plugin install jerry-framework@jerry`

### Path Issues on Windows

**Symptom:** "path not found" when adding marketplace

**Solutions:**
- Use forward slashes in Claude Code: `C:/Users/name/plugins/jerry`
- Or use short path: `~/plugins/jerry` (if using Git Bash paths)
- Avoid using backslashes or environment variables in the Claude Code command

---

## For Developers

If you want to contribute to Jerry development, you'll need Python 3.11+ and [uv](https://docs.astral.sh/uv/).

### Development Setup

**macOS / Linux:**
```bash
git clone https://github.com/geekatron/jerry.git
cd jerry
make setup    # Installs deps + pre-commit hooks
make test     # Run test suite
```

**Windows (Git Bash or PowerShell):**
```bash
git clone https://github.com/geekatron/jerry.git
cd jerry
uv sync                        # Install dependencies
uv run pre-commit install      # Install pre-commit hooks
uv run pytest --tb=short -q    # Run test suite
```

> **Note:** Windows does not have `make` by default. Use the `uv run` commands directly. See [CONTRIBUTING.md](../CONTRIBUTING.md) for the full Make target equivalents table.

### Common Developer Commands

| Task | macOS/Linux | Windows / All Platforms |
|------|-------------|------------------------|
| First-time setup | `make setup` | `uv sync && uv run pre-commit install` |
| Run tests | `make test` | `uv run pytest --tb=short -q` |
| Run linters | `make lint` | `uv run ruff check src/ tests/ && uv run pyright src/` |
| Format code | `make format` | `uv run ruff check --fix src/ tests/ && uv run ruff format src/ tests/` |
| All pre-commit hooks | `make pre-commit` | `uv run pre-commit run --all-files` |

### Context Distribution (Bootstrap)

Jerry's behavioral rules live in `.context/` (canonical source) and are synced to `.claude/` via symlinks. After cloning, run the bootstrap:

```bash
uv run python scripts/bootstrap_context.py        # Set up symlinks
uv run python scripts/bootstrap_context.py --check # Verify sync
```

See [Bootstrap Guide](BOOTSTRAP.md) for platform-specific details.

### Architecture Overview

Jerry follows hexagonal architecture:

```
src/
├── domain/           # Pure business logic (no external deps)
├── application/      # Use cases (CQRS commands/queries)
├── infrastructure/   # Adapters (persistence, messaging)
└── interface/        # Primary adapters (CLI)
```

See [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed contribution guidelines, Windows-specific notes, and coding standards.

---

## Uninstallation

### Remove the Plugin

```
/plugin uninstall jerry-framework@jerry
```

### Remove the Marketplace

```
/plugin marketplace remove jerry
```

### Delete Local Files (Optional)

**macOS/Linux:**
```bash
rm -rf ~/plugins/jerry
```

**Windows PowerShell:**
```powershell
Remove-Item -Recurse -Force "$env:USERPROFILE\plugins\jerry"
```

---

## Getting Help

- **GitHub Issues:** [github.com/geekatron/jerry/issues](https://github.com/geekatron/jerry/issues)
- **Documentation:** `docs/` directory in the repository
- **Claude Code Help:** Run `/help` in Claude Code

---

## License

Jerry Framework is open source under the MIT License.
