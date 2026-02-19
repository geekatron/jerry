# Jerry Framework Installation Guide

> Jerry is a Claude Code plugin for behavior and workflow guardrails.

> **Platform Note:** Jerry is primarily developed and tested on macOS. Linux is expected to work — CI runs on Ubuntu for every job, and uv/git tooling is cross-platform. Windows support is in progress — skills and core functionality work, but hooks that use symlinks or path-sensitive operations may behave differently. Known Windows limitations: bootstrap uses junction points instead of symlinks, and paths in Claude Code commands must use forward slashes. See [Platform Support](index.md#platform-support) for details. Report Windows issues via the [Windows compatibility template](https://github.com/geekatron/jerry/issues/new?template=windows-compatibility.yml).

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Prerequisites](#prerequisites) | What you need before installing |
| [Quick Install (Most Users)](#quick-install-most-users) | Two commands — no clone, no build tools |
| [Enable Hooks (Recommended)](#enable-hooks-recommended) | Optional uv install for session context and quality enforcement |
| [Capability Matrix](#capability-matrix) | What works with and without uv |
| [Alternative: Local Clone Install](#alternative-local-clone-install) | For offline use, version pinning, or network-restricted environments |
| [Configuration](#configuration) | Post-installation setup |
| [Verification](#verification) | How to confirm installation succeeded |
| [Using Jerry](#using-jerry) | Getting started with skills |
| [Developer Setup](#developer-setup) | Contributing and development environment |
| [Troubleshooting](#troubleshooting) | Common issues and solutions |
| [Uninstallation](#uninstallation) | How to remove Jerry |
| [Getting Help](#getting-help) | Support resources and documentation |
| [License](#license) | Open source license information |

---

## Prerequisites

| Software | Required? | Purpose |
|----------|-----------|---------|
| [Claude Code](https://code.claude.com) 1.0.33+ | **Yes** | The AI coding assistant Jerry extends |
| [uv](https://docs.astral.sh/uv/) | Recommended | Enables hooks (session context, quality enforcement) |

That's it. You do **not** need Git, Python, or a local clone to install and use Jerry's skills.

> **Don't have Claude Code?** Follow the [Setup Guide](https://code.claude.com/docs/en/setup) to install it first, then return here.

> **Version note:** The `/plugin` command and its Installed/Discover/Errors tabs are available in Claude Code 1.0.33+. If `/plugin` is not recognized, update Claude Code first.

---

## Quick Install (Most Users)

Jerry is a public Claude Code plugin hosted on [GitHub](https://github.com/geekatron/jerry). The repository contains the required `.claude-plugin/marketplace.json` and `.claude-plugin/plugin.json` manifests that Claude Code reads to register and install the plugin. This method requires internet access to GitHub and that the repository is accessible (it is public). Install it with two commands in Claude Code:

**Step 1: Add the marketplace**

```
/plugin marketplace add https://github.com/geekatron/jerry
```

This registers Jerry's plugin catalog with Claude Code by pointing it to the GitHub repository. A marketplace is like an app store — it tells Claude Code what plugins are available. No plugins are installed yet.

> **Shorthand:** You can also use `geekatron/jerry` — Claude Code resolves `owner/repo` to GitHub automatically.

**Step 2: Install the plugin**

```
/plugin install jerry@geekatron-jerry
```

This downloads and activates Jerry's skills. The install command uses the format `<plugin>@<marketplace>` — `jerry` is the plugin name (from `plugin.json`) and `geekatron-jerry` is the marketplace name (derived from the GitHub `owner/repo` path).

> **Verify the marketplace name:** After Step 1, run `/plugin marketplace list` to confirm the marketplace was registered and to see its name. Use that name as the `@suffix` in the install command. If the name differs from `geekatron-jerry`, adjust accordingly: `/plugin install jerry@<your-marketplace-name>`.

**Verify it worked:**

1. Run `/plugin` in Claude Code
2. Go to the **Installed** tab
3. Confirm `jerry` appears in the list

**Test a skill:**

```
/problem-solving
```

You should see the problem-solving skill activate.

### Installation Scope

During install, Claude Code asks which scope to use:

| Scope | Effect | Use Case |
|-------|--------|----------|
| **User** (default) | Installs for you across all projects | Personal use |
| **Project** | Added to `.claude/settings.json` (version-controlled) | Team-wide — all collaborators get Jerry |
| **Local** | Only you, only this repository | Testing |

**Recommendation:** Use **User** for personal use. Use **Project** when you want your whole team to have Jerry available automatically — the `.claude/settings.json` file is committed to version control, so new team members get Jerry active as soon as they clone the repository.

**Alternative: Interactive Installation**

1. Run `/plugin`
2. Go to the **Discover** tab
3. Find `jerry`
4. Press Enter and select your installation scope

> **Remote install not working?** If the marketplace add or plugin install commands fail, use the [Local Clone Install](#alternative-local-clone-install) below instead. The local clone method is verified and always works. If you encounter issues with the remote path, please [file a GitHub issue](https://github.com/geekatron/jerry/issues) so we can improve these instructions.

---

## Enable Hooks (Recommended)

Jerry's skills work immediately after the Quick Install. However, Jerry also ships four hooks that provide session context auto-loading, per-prompt quality reinforcement, pre-tool-use validation, and subagent enforcement. These hooks require [uv](https://docs.astral.sh/uv/) (a fast Python package manager) to execute.

### What hooks provide

| Hook | What It Does |
|------|-------------|
| SessionStart | Auto-loads project context, rules, and quality framework at session start |
| UserPromptSubmit | Re-injects critical rules every prompt to combat context rot (L2 enforcement) |
| PreToolUse | AST-based validation before tool calls execute (L3 enforcement) |
| SubagentStop | Enforces single-level subagent hierarchy (P-003) |

### Install uv

**macOS / Linux:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

After installing, **restart your terminal** (close and reopen), then verify:

```bash
uv --version
# Should output: uv 0.x.x
```

That's it. Once uv is installed, hooks activate automatically the next time you start Claude Code.

> **Note:** You do NOT need Python installed separately. The uv installer handles Python automatically.

> **Early access caveat:** Hook enforcement is under active development. Some hooks may have schema validation issues that cause them to fail silently (fail-open behavior — skills always work, but enforcement may not fire). If hooks don't appear to be working after installing uv, check [GitHub Issues](https://github.com/geekatron/jerry/issues) for the latest status.

---

## Capability Matrix

| Feature | Without uv | With uv |
|---------|-----------|---------|
| Skills (`/problem-solving`, `/worktracker`, etc.) | Yes | Yes |
| Session context auto-loading | No | Yes |
| Per-prompt quality reinforcement (L2) | No | Yes |
| Pre-tool-use AST validation (L3) | No | Yes |
| Subagent hierarchy enforcement | No | Yes |

Without uv, hooks fail silently (fail-open) — skills still work, but you lose the automated guardrail enforcement that makes Jerry most effective.

---

## Alternative: Local Clone Install

Use this method if you:

- Are in a **network-restricted environment** that blocks GitHub marketplace access
- Need **offline** access to Jerry's source
- Want to **pin a specific version** (e.g., `git clone --branch v1.0.0`)

### Step 1: Clone the repository

**macOS / Linux:**

```bash
mkdir -p ~/plugins
git clone https://github.com/geekatron/jerry.git ~/plugins/jerry
```

**Windows (PowerShell):**

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\plugins"
git clone https://github.com/geekatron/jerry.git "$env:USERPROFILE\plugins\jerry"
```

> **Important:** The clone path must not contain spaces. Claude Code's `/plugin marketplace add` command does not support paths with spaces.

### Step 2: Add the local marketplace

```
/plugin marketplace add ~/plugins/jerry
```

**Windows (Claude Code):** Use forward slashes: `/plugin marketplace add C:/Users/YOUR_USERNAME/plugins/jerry`

> **Tip (Windows):** To get the exact forward-slash path, run this in PowerShell:
> ```powershell
> (Get-Item "$env:USERPROFILE\plugins\jerry").FullName -replace '\\','/'
> ```

### Step 3: Install the plugin

```
/plugin install jerry@jerry-framework
```

### Advanced: SSH clone

If you prefer SSH over HTTPS (e.g., you already have an SSH key configured with GitHub):

```bash
git clone git@github.com:geekatron/jerry.git ~/plugins/jerry
```

All subsequent steps remain the same. See [GitHub's SSH documentation](https://docs.github.com/en/authentication/connecting-to-github-with-ssh) for SSH key setup.

### Version pinning

To pin Jerry to a specific release:

```bash
git clone --branch v1.0.0 https://github.com/geekatron/jerry.git ~/plugins/jerry
```

See [releases](https://github.com/geekatron/jerry/releases) for available tags.

---

## Configuration

### Project Setup (Optional)

Jerry uses project-based workflows for organizing work. To set up a project:

1. **Set the project environment variable:**

   ```bash
   # macOS/Linux
   export JERRY_PROJECT=PROJ-001-my-project

   # Windows PowerShell
   $env:JERRY_PROJECT = "PROJ-001-my-project"
   ```

   > **Note:** The project name follows the format `PROJ-{NNN}-{slug}`. Choose any slug that describes your work (e.g., `PROJ-001-my-api`). The number prefix helps Jerry track multiple projects. Your first project is typically `PROJ-001`.

2. **Create project structure:**

   ```bash
   # macOS/Linux
   mkdir -p projects/PROJ-001-my-project/.jerry/data/items

   # Windows PowerShell
   New-Item -ItemType Directory -Force -Path "projects\PROJ-001-my-project\.jerry\data\items"
   ```

The SessionStart hook will automatically load project context when you start Claude Code.

---

## Verification

### Quick Install verification

1. In Claude Code, run `/plugin`
2. Go to the **Installed** tab
3. Verify `jerry` appears in the list

### Hooks verification

If you installed uv, start a new Claude Code session. The SessionStart hook fires automatically. You should see project context loading in the session output.

### Skill test

Run a simple skill to verify everything works:

```
/problem-solving
```

You should see the problem-solving skill activate with information about available agents.

> **Note:** Most skills require an active project (`JERRY_PROJECT` environment variable set). If you skipped Configuration, use `/help` instead to verify skill availability without a project.

### Check for errors

1. Run `/plugin`
2. Go to the **Errors** tab
3. Verify no errors related to `jerry`

---

## Using Jerry

> **New to Jerry?** Follow the [Getting Started runbook](runbooks/getting-started.md) for a guided walkthrough from installation to your first persisted skill output.

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
| Adversary | `/adversary` | Adversarial quality reviews and tournament scoring |

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
| Critiques | `docs/critiques/` |
| Decisions (ADRs) | `docs/decisions/` |
| Investigations | `docs/investigations/` |
| Reviews | `docs/reviews/` |
| Reports | `docs/reports/` |
| Synthesis | `docs/synthesis/` |

These files survive context compaction and session boundaries, building your project's knowledge base over time.

---

## Developer Setup

> **This section is for contributors to the Jerry codebase.** If you installed Jerry as a plugin, you do not need anything below.

### Prerequisites

- [uv](https://docs.astral.sh/uv/) (manages Python automatically — no separate Python install needed)
- Git

### Development Environment

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

> **Note:** Windows does not have `make` by default. Use the `uv run` commands directly. See [CONTRIBUTING.md](https://github.com/geekatron/jerry/blob/main/CONTRIBUTING.md) for the full Make target equivalents table.

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

> **Who needs this?** Bootstrap is for developers editing `.context/rules/` who want changes to auto-propagate to `.claude/rules/`. If you installed Jerry as a plugin, you do not need to run bootstrap — skills and hooks work without it.

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

See [CONTRIBUTING.md](https://github.com/geekatron/jerry/blob/main/CONTRIBUTING.md) for detailed contribution guidelines, Windows-specific notes, and coding standards.

---

## Troubleshooting

### Quick Install Issues

**Marketplace not found**

**Symptom:** `/plugin marketplace add https://github.com/geekatron/jerry` returns an error

**Solutions:**
1. Verify Claude Code is version 1.0.33+: update with `brew upgrade claude-code` (macOS) or `npm update -g @anthropic-ai/claude-code`
2. Check your internet connection — the command needs GitHub access
3. If behind a corporate proxy, use the [Local Clone Install](#alternative-local-clone-install) instead

**Plugin not found after adding marketplace**

**Symptom:** `/plugin install jerry@...` returns "plugin not found"

**Solutions:**
1. Run `/plugin marketplace list` to see the actual marketplace name — the `@suffix` in the install command must match exactly
2. Remote installs (`geekatron/jerry`): marketplace name is `geekatron-jerry` — use `/plugin install jerry@geekatron-jerry`
3. Local clone installs (`~/plugins/jerry`): marketplace name is `jerry-framework` — use `/plugin install jerry@jerry-framework`
4. Refresh the marketplace: `/plugin marketplace update <marketplace-name>`

### Hook Issues

**uv: command not found**

**Symptom:** Hooks fail with "uv: command not found"

**Solution (macOS/Linux):**
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
- macOS/Linux: `export PATH="$HOME/.local/bin:$PATH"` (add to `~/.zshrc` or `~/.bashrc`)
- Windows: Add `%USERPROFILE%\.local\bin` to System PATH

**Hooks not firing**

**Symptom:** SessionStart hook doesn't run, no project context loaded

**Solutions:**
1. Verify uv is installed: `uv --version`
2. Restart Claude Code completely (close and reopen)
3. Check `/plugin` > **Errors** tab for hook-related errors
4. For local clone installs, verify hooks exist in the `.claude-plugin/hooks/` directory

### Skill Issues

**Skills not appearing**

**Symptom:** `/problem-solving` doesn't work

**Solutions:**
1. Check the **Errors** tab in `/plugin`
2. Clear the plugin cache:
   - macOS: `rm -rf ~/.claude/plugins/cache`
   - Windows: `Remove-Item -Recurse -Force "$env:USERPROFILE\.claude\plugins\cache"`
3. Restart Claude Code
4. Reinstall: `/plugin uninstall jerry` then re-run the install command for your method (see [Quick Install](#quick-install-most-users) or [Local Clone](#alternative-local-clone-install))

### Project Issues

**`<project-required>` or `<project-error>`**

**Symptom:** Skills show XML-tagged output instead of the expected response

**Cause:** `JERRY_PROJECT` is not set, points to a non-existent project, or the directory structure is incomplete.

**Solutions:**
1. Set the variable: `export JERRY_PROJECT=PROJ-001-my-project` (macOS/Linux) or `$env:JERRY_PROJECT = "PROJ-001-my-project"` (Windows)
2. Verify the directory exists: `ls projects/$JERRY_PROJECT/` — it should contain `PLAN.md` and `WORKTRACKER.md`
3. If you haven't created a project, follow the [Configuration](#configuration) section
4. Use `/help` to verify Jerry is installed — this works without a project

### Path Issues on Windows

**Symptom:** "path not found" when adding local marketplace

**Solutions:**
- Use forward slashes in Claude Code: `C:/Users/name/plugins/jerry`
- Avoid backslashes or environment variables in the Claude Code command

---

## Uninstallation

### Remove the Plugin

```
/plugin uninstall jerry
```

### Remove the Marketplace

```
/plugin marketplace remove geekatron-jerry
```

> **Not sure of the name?** Run `/plugin marketplace list` to see your marketplace name. Local clone users will see `jerry-framework` instead.

### Delete Local Files (Optional)

Only applicable if you used the local clone method:

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
- **Documentation:** [jerry.geekatron.org](https://jerry.geekatron.org)
- **Claude Code Help:** Run `/help` in Claude Code

---

## License

Jerry Framework is open source under the [Apache License 2.0](https://github.com/geekatron/jerry/blob/main/LICENSE).
