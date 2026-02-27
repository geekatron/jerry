# Jerry Framework Installation Guide

> Your AI coding partner just got guardrails, knowledge accrual, and a whole crew of specialized agents. Let's get you set up and shredding.

> **Platform Note:** Jerry is built and battle-tested on macOS. Linux works — CI runs Ubuntu on every job and the tooling is cross-platform. Windows support is in progress — skills and core functionality work, but hooks that use symlinks or path-sensitive operations may behave differently. Known Windows limitations: bootstrap uses junction points instead of symlinks, and paths in Claude Code commands must use forward slashes. See [Platform Support](index.md#platform-support) for details. Hit a wall? File it via the [Windows compatibility template](https://github.com/geekatron/jerry/issues/new?template=windows-compatibility.yml).

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Prerequisites](#prerequisites) | What you need before dropping in |
| [Which Install Method?](#which-install-method) | Four paths, one Jerry — pick the line that fits your setup |
| [Install from GitHub](#install-from-github) | Persistent install via Claude Code's plugin system (~2 min) |
| [Enable Hooks](#enable-hooks-early-access) | Session context and quality enforcement (early access — hooks may fail silently) |
| [Capability Matrix](#capability-matrix) | What works with and without uv |
| [Local Clone](#local-clone) | For offline use, version pinning, or locked-down networks |
| [Session Install](#session-install-plugin-dir-flag) | Session-only install — skills available immediately, no configuration |
| [Configuration](#configuration) | Project setup — required for skills to work |
| [Verification](#verification) | Confirm everything landed |
| [Using Jerry](#using-jerry) | Getting started with skills |
| [Developer Setup](#developer-setup) | Contributing to Jerry's codebase |
| [Troubleshooting](#troubleshooting) | When things don't land clean — common fixes |
| [Updating](#updating) | Pull latest changes — GitHub users vs local clone |
| [Uninstallation](#uninstallation) | Clean removal: plugin, source, and local files |
| [Getting Help](#getting-help) | Support and docs |
| [License](#license) | Apache 2.0 — use freely, attribution required |

> **First time here?** Start with [Which Install Method?](#which-install-method) to pick the right path in under a minute.

---

## Prerequisites

| Software | Required? | Purpose |
|----------|-----------|---------|
| [Claude Code](https://code.claude.com/docs/en/quickstart) 1.0.33+ | **Yes** | The AI coding assistant Jerry extends |
| SSH key configured for GitHub | **No** — [HTTPS alternative available](#install-from-github) | The `owner/repo` shorthand clones via SSH; HTTPS URL works without SSH |
| [uv](https://docs.astral.sh/uv/) | Recommended | Enables hooks (session context, quality enforcement) |

> **Network access:** The GitHub install method needs outbound access to `github.com` (and `raw.githubusercontent.com` for plugin discovery). If you install uv for hooks, the installer reaches `astral.sh`. The Local Clone method requires `github.com` only for the initial clone — after that, no network access is needed. For fully air-gapped environments, see [Air-gapped install](#air-gapped-install) under Local Clone.

> **Why does SSH come up?** When you add a plugin source using the `owner/repo` shorthand (e.g., `geekatron/jerry`), Claude Code clones the repository via SSH. Even though Jerry's repo is public, the `owner/repo` format defaults to SSH. If you don't have SSH keys configured for GitHub, you'll see "Permission denied (publickey)." The fix is simple: use the full HTTPS URL instead. Both commands do the same thing. See [Install from GitHub](#install-from-github) for both options side by side.

> **Don't have Claude Code yet?** No worries — install it first via Anthropic's [Claude Code quickstart](https://code.claude.com/docs/en/quickstart). Takes a few minutes. We'll be here when you get back.

> **Version check:** The `/plugin` command requires Claude Code 1.0.33+. Run `claude --version` to check. If `/plugin` is not recognized, update Claude Code first.

---

## Which Install Method?

Four install methods — all get you the same Jerry. Pick the line that fits your setup.

| Your Situation | Method | Time |
|----------------|--------|------|
| **Internet access + SSH key** configured for GitHub | [Install from GitHub (SSH)](#install-from-github) | ~2 minutes |
| **Internet access, no SSH key** — or you're not sure | [Install from GitHub (HTTPS)](#install-from-github) | ~2 minutes |
| **Offline or network-restricted** — corporate firewall, air-gapped, or version-pinned | [Local Clone](#local-clone) | ~5 minutes |
| **Session-only install** — skills available immediately, no configuration needed | [Session Install](#session-install-plugin-dir-flag) | ~3 minutes |

> **Not sure if you have SSH configured?** Run `ssh -T git@github.com` in your terminal. If you see `Hi <username>!` and `<username>` is your GitHub account, you have SSH set up. If the username is unexpected, or you see "Permission denied," use the HTTPS path — same result, same speed, no SSH needed.

Not sure which to pick? Start with [Install from GitHub](#install-from-github) using the HTTPS URL. It works for everyone.

---

## Install from GitHub

Jerry is a **community Claude Code plugin** hosted on [GitHub](https://github.com/geekatron/jerry). It is not part of the official Anthropic plugin catalog — you install it directly from the GitHub repository using Claude Code's built-in plugin system.

> **What does "marketplace" mean here?** Claude Code uses the word "marketplace" in its `/plugin marketplace` commands, but for community plugins like Jerry, it just means "register a plugin source." Any GitHub repository with a `.claude-plugin/marketplace.json` file can serve as a plugin source. Jerry's GitHub repository is its own marketplace. This is separate from the [official Anthropic marketplace](https://github.com/anthropics/claude-plugins-official), which is automatically available in Claude Code and contains Anthropic-curated plugins.

> **Where do I type these commands?** All `/plugin` commands are typed into Claude Code's chat input — the same text box where you send messages to the AI. Type the command and press Enter. These are not terminal commands.

> **Arriving from the HTTPS row in the table above?** Use the HTTPS command in Step 1 below (the second row in the table). It works without SSH keys.

**Step 1: Add the Jerry repository as a plugin source**

Pick whichever command matches your setup — all three do the same thing:

| Your Setup | Command |
|------------|---------|
| **SSH key configured** (shorthand) | `/plugin marketplace add geekatron/jerry` |
| **SSH key configured** (explicit URL) | `/plugin marketplace add git@github.com:geekatron/jerry.git` |
| **No SSH key (or not sure)** | `/plugin marketplace add https://github.com/geekatron/jerry.git` |

> The `owner/repo` shorthand resolves to SSH under the hood — it's equivalent to the explicit SSH URL. Both require an SSH key configured for GitHub. The HTTPS URL works without SSH keys.

This tells Claude Code where to find Jerry. Nothing is installed yet — you're just registering the source.

> **SSH authentication failed?** If you see "Permission denied (publickey)", use the HTTPS command from the table above. It clones over HTTPS — no SSH keys needed.

**Step 2: Verify the source registered**

Run this to confirm Jerry's marketplace source was added:

```
/plugin marketplace list
```

You should see `jerry-framework` in the output. This is the source name you'll use in the next step. If you don't see it, re-run Step 1.

> **Shortcut:** You can also type `/plugin market list` — Claude Code accepts `market` as shorthand for `marketplace`.

**Step 3: Install the plugin**

Use the source name from Step 2's output as the `@suffix`:

```
/plugin install jerry@<name-from-step-2>
```

If Step 2 showed `jerry-framework` (the default), the command is:

```
/plugin install jerry@jerry-framework
```

This downloads and activates Jerry's skills, agents, and hooks. The format is `plugin-name@source-name` — `jerry` is the plugin name and the part after `@` is the source name you verified in Step 2.

> **"Plugin not found"?** The source name must match exactly what `/plugin marketplace list` shows. Re-run Step 2 and copy the name from the output. The source name comes from Jerry's [`.claude-plugin/marketplace.json`](https://github.com/geekatron/jerry/blob/main/.claude-plugin/marketplace.json) — you can inspect it to verify.

**Step 4: Confirm it landed**

1. Run `/plugin` in Claude Code
2. Go to the **Installed** tab
3. Verify `jerry` appears in the list

If `jerry` appears, you're in. Head to [Configuration](#configuration) to set up your first project, then [Verification](#verification) to confirm everything's firing.

### Installation Scope

During install, Claude Code asks which scope to use:

| Scope | Effect | When to Use |
|-------|--------|-------------|
| **User** (default) | Installs for you across all projects | Personal use — this is what most people want |
| **Project** | Added to `.claude/settings.json` (version-controlled) | Team-wide — everyone who clones the repo gets Jerry |
| **Local** | Only you, only this repository | Testing a specific version |

**Recommendation:** Use **User** for personal use. Use **Project** when you want your whole team using Jerry — the settings file is committed to version control, so new team members get Jerry the moment they clone.

### Interactive Installation (after adding the source)

> **Important:** Jerry won't appear in the Discover tab until you complete [Step 1](#install-from-github) above (adding the plugin source via CLI). The Discover tab shows plugins from all registered marketplaces — Jerry is a community plugin, not part of the official Anthropic catalog, so it only appears after you add its source.

After completing [Step 1](#install-from-github), you can also install through the `/plugin` UI:

1. Run `/plugin`
2. Navigate to the **Discover** tab — Jerry will appear here because you registered its source
3. Find `jerry` and press Enter
4. Select your installation scope

> **Something not working?** If the GitHub path gives you trouble, the [Local Clone](#local-clone) method always works. Then [file an issue](https://github.com/geekatron/jerry/issues) so we can smooth the primary path.

---

## Enable Hooks (Early Access)

> **Early access caveat:** Hook enforcement is under active development. Some hooks may have schema validation issues that cause them to fail silently (fail-open behavior — skills always work, but enforcement may not fire). The most stable hooks are SessionStart and UserPromptSubmit. PreToolUse and SubagentStop may experience schema issues in some Claude Code versions. After installing uv:
> 1. Start a new Claude Code session and check whether the `<project-context>` tag appears (SessionStart hook)
> 2. If the tag is absent, check the `/plugin` **Errors** tab and [GitHub Issues tagged `hooks`](https://github.com/geekatron/jerry/issues?q=label%3Ahooks) for known issues

Skills work the moment you install. Hooks are the next level — they're what keep Jerry dialed across your entire session: auto-loading context at startup, reinforcing quality rules every prompt, catching state before compaction wipes it, and keeping the agent hierarchy honest. Think of hooks as Jerry's immune system — the skills are the muscles, but hooks keep everything running clean underneath.

They need [uv](https://docs.astral.sh/uv/). It takes 30 seconds.

### What hooks give you

| Hook | What It Does |
|------|-------------|
| SessionStart | Auto-loads project context, rules, and quality framework at session start |
| UserPromptSubmit | Re-injects critical rules every prompt to combat context rot (L2 enforcement) |
| PreCompact | Saves critical context before compaction — Jerry's defense against losing state when the context window fills |
| PreToolUse | AST-based validation and security guardrails before tool calls execute (L3 enforcement) |
| SubagentStop | Enforces single-level subagent hierarchy and captures orchestration handoffs (P-003) |
| Stop | Context stop gate — preserves session state on exit |

### Install uv

> **Security note:** The commands below download and execute a script from `astral.sh`. This is a standard pattern for developer tools (Rust, Homebrew, and others use it). If your organization requires script inspection before execution: on macOS/Linux, download first with `curl -LsSf https://astral.sh/uv/install.sh -o install-uv.sh`, review it, then run `sh install-uv.sh`; on Windows, download first with `Invoke-WebRequest https://astral.sh/uv/install.ps1 -OutFile install-uv.ps1`, review it, then run `.\install-uv.ps1`. Alternatively, install via [pip](https://docs.astral.sh/uv/getting-started/installation/#pip) or your system package manager.

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

Once uv is installed, hooks should activate automatically the next time you start Claude Code. Quick check: start a new session — if you see a `<project-context>` tag in the output, hooks are live. For the full checklist, see [Hooks verification](#hooks-verification) below.

> **Note:** You do NOT need Python installed separately. uv handles Python automatically.

---

## Capability Matrix

| Feature | Without uv | With uv |
|---------|-----------|---------|
| All 12 skills (see [Available Skills](#available-skills)) | Yes | Yes |
| Session context auto-loading | No | Yes |
| Per-prompt quality reinforcement (L2) | No | Yes |
| Pre-compaction context protection | No | Yes |
| Pre-tool-use guardrails (L3, fail-open — see [early access caveat](#enable-hooks-early-access)) | No | Yes |
| Subagent hierarchy enforcement | No | Yes |
| Session state preservation on exit | No | Yes |

Without uv, you get the skills but not the guardrails. Everything still works — but the enforcement architecture that keeps Jerry honest across long sessions stays dark. Install uv. It's worth the 30 seconds.

---

## Local Clone

Same Jerry, different delivery route. Use this method if you:

- Are in a **network-restricted environment** that blocks Claude Code's GitHub access
- Want **offline** access to Jerry's source
- Need to **pin a specific version** (e.g., `git clone --branch v0.21.0`)
- Want to **inspect the code** before installing

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

### Step 2: Add as a local plugin source

In Claude Code (all `/plugin` commands are typed into Claude Code's chat input, not your terminal):

```
/plugin marketplace add ~/plugins/jerry
```

**Windows (Claude Code):** Use forward slashes — `/plugin marketplace add C:/Users/YOUR_USERNAME/plugins/jerry`

Replace `YOUR_USERNAME` with your actual Windows username. To find the full path, run `echo $env:USERPROFILE` in PowerShell.

### Step 3: Verify and install

Run `/plugin marketplace list` to confirm the source registered, then install using the name from the list:

```
/plugin install jerry@<name-from-list>
```

If the list showed `jerry-framework` (the default), the command is `/plugin install jerry@jerry-framework`.

> **"Plugin not found"?** The source name must match exactly what `/plugin marketplace list` shows. See [Plugin not found](#plugin-not-found-after-adding-source) in Troubleshooting.

### Advanced: SSH clone

If you prefer SSH (e.g., you already have an SSH key configured with GitHub):

```bash
git clone git@github.com:geekatron/jerry.git ~/plugins/jerry
```

All subsequent steps are the same. See [GitHub's SSH documentation](https://docs.github.com/en/authentication/connecting-to-github-with-ssh) for key setup.

### Air-gapped install

For fully air-gapped environments where `github.com` is blocked entirely:

1. Clone the repository from a machine with GitHub access
2. Transfer the `jerry/` directory to the restricted machine via your organization's approved file transfer method
3. Proceed from [Step 2: Add as a local plugin source](#step-2-add-as-a-local-plugin-source) using the local path

> **uv in air-gapped environments:** The uv installer also requires network access (to `astral.sh`). For air-gapped uv installation, download a release binary from [uv GitHub releases](https://github.com/astral-sh/uv/releases) and place it in `~/.local/bin/` manually.

### Version pinning

To pin Jerry to a specific release:

```bash
git clone --branch v0.21.0 https://github.com/geekatron/jerry.git ~/plugins/jerry
```

See [releases](https://github.com/geekatron/jerry/releases) for available tags.

---

## Session Install (Plugin Dir Flag)

Want to try Jerry without any configuration? Clone the repo and point Claude Code at it directly — skills are available immediately, no plugin source setup needed:

```bash
# Clone if you haven't already
git clone https://github.com/geekatron/jerry.git ~/plugins/jerry

# Start Claude Code with Jerry loaded
claude --plugin-dir ~/plugins/jerry
```

Skills are available immediately — no `/plugin install` needed. Try `/problem-solving` in Claude Code's chat input to see what you're working with.

> **Note:** The `--plugin-dir` flag loads the plugin for that session only. It does not persist across sessions. For persistent installation, use the [Install from GitHub](#install-from-github) or [Local Clone](#local-clone) methods. For users who launch Claude Code from a consistent project directory, session-scoped loading can be a legitimate workflow — not just a trial run.

---

## Configuration

### Project Setup (Required for Skills)

This is where Jerry goes from installed to yours. Jerry organizes your work into projects — each one is a workspace where your research, decisions, and work items build up over time. It's how Jerry remembers what you're working on across sessions, even when the context window resets.

Most skills need an active project to operate. Without one, you'll see `<project-required>` messages instead of skill output. Four steps and you're set.

1. **Navigate to your repository** (the one where you want Jerry to work):

   ```bash
   cd /path/to/your/repo
   ```

2. **Set the project environment variable:**

   ```bash
   # macOS/Linux
   export JERRY_PROJECT=PROJ-001-my-project

   # Windows PowerShell
   $env:JERRY_PROJECT = "PROJ-001-my-project"
   ```

   > **Project naming:** The format is `PROJ-{NNN}-{slug}` and it matters — Jerry's CLI and hooks validate this pattern. If you use a different format (e.g., `my-project` instead of `PROJ-001-my-project`), you'll see `<project-error>` messages. Pick any slug that describes your work (e.g., `PROJ-001-my-api`). Your first project is typically `PROJ-001`.

3. **Make it persistent** (so you don't lose it when you close the terminal):

   ```bash
   # macOS/Linux — add to your shell profile
   echo 'export JERRY_PROJECT=PROJ-001-my-project' >> ~/.zshrc
   # Or ~/.bashrc if you use bash

   # Windows PowerShell — create profile if needed, then add
   if (!(Test-Path $PROFILE)) { New-Item -Path $PROFILE -Force }
   Add-Content $PROFILE '$env:JERRY_PROJECT = "PROJ-001-my-project"'
   ```

   > **Verify it stuck:** Open a new terminal (to load the updated profile), then run `echo $JERRY_PROJECT` (macOS/Linux) or `echo $env:JERRY_PROJECT` (Windows). If this prints your project ID, you're set. If it's empty, check that you saved the profile file and are using the correct shell.

   > **Launch order matters:** Claude Code inherits environment variables from the terminal it was launched from. Set `JERRY_PROJECT` first, then launch Claude Code. If Claude Code is already running, restart it from a terminal where the variable is set.

4. **Create project structure** (run this from your repository root):

   ```bash
   # macOS/Linux
   mkdir -p projects/PROJ-001-my-project/.jerry/data/items

   # Windows PowerShell
   New-Item -ItemType Directory -Force -Path "projects\PROJ-001-my-project\.jerry\data\items"
   ```

   > **Don't have a repository yet?** Jerry works in any directory. Create one: `mkdir my-project && cd my-project && git init`, then run the `mkdir` command above. Jerry doesn't require an existing codebase.

   > The `.jerry/` directory contains operational state and is gitignored — do not commit it. If you don't have a `.gitignore` yet: `echo '.jerry/' >> .gitignore`. Jerry auto-creates additional subdirectories (`work/`, `decisions/`, `orchestration/`) as skills produce output. You only need the base structure above.

The SessionStart hook auto-loads project context when you start Claude Code. If you skip this section, skills will prompt you to set up a project when you invoke them — you'll know because you'll see `<project-required>` in the output.

---

## Verification

### Plugin verification

1. In Claude Code, run `/plugin`
2. Go to the **Installed** tab
3. Verify `jerry` appears in the list

### Hooks verification

If you installed uv and set `JERRY_PROJECT`, start a new Claude Code session. The SessionStart hook fires automatically — you should see a `<project-context>` tag in the session output with your project name and loaded rules. If you see the tag, hooks are working — the SessionStart hook loaded your project context and quality rules. You're live.

> **No `<project-context>` tag?** Check the [early access caveat](#enable-hooks-early-access). Hooks may have failed silently. Look at the `/plugin` **Errors** tab for details.

### Skill test

```
/problem-solving
```

You should see the problem-solving skill activate — it'll describe itself and list its available agents (researcher, analyst, architect, and the rest of the crew). That's the whole crew reporting for duty. You're live.

> **Seeing `<project-required>`?** This is the most common post-install issue — Jerry installed fine, but no project is configured. Go to [Configuration](#configuration) and set `JERRY_PROJECT`. Make sure you ran the `mkdir` command from your **repository root**, not your home directory.

### Check for errors

1. Run `/plugin`
2. Go to the **Errors** tab
3. Verify no errors related to `jerry`

---

## Using Jerry

> **New to Jerry?** Start by trying `/problem-solving` on a question you're working on, or `/worktracker` to set up your first work items. Each skill guides you through what it needs. Let it rip.

### Available Skills

| Skill | Command | Purpose |
|-------|---------|---------|
| Problem-Solving | `/problem-solving` | Research, analysis, architecture decisions |
| Work Tracker | `/worktracker` | Task and work item management |
| NASA SE | `/nasa-se` | Systems engineering processes (NPR 7123.1D) |
| Orchestration | `/orchestration` | Multi-phase workflow coordination |
| Architecture | `/architecture` | Design decisions and ADRs |
| Transcript | `/transcript` | Meeting transcript parsing |
| Adversary | `/adversary` | Adversarial quality reviews and tournament scoring |
| Eng Team | `/eng-team` | Secure software engineering methodology |
| Red Team | `/red-team` | Offensive security testing methodology |
| Saucer Boy | `/saucer-boy` | McConkey personality for work sessions |
| AST | `/ast` | Markdown AST operations (parse, query, validate) |
| Saucer Boy Framework Voice | `/saucer-boy-framework-voice` | Internal: framework output voice quality gate |

### Persistent Artifacts

Skill outputs are persisted to your project's work directory and docs directory, building your knowledge base over time:

| Output Type | Location |
|-------------|----------|
| Work decomposition | `projects/{JERRY_PROJECT}/work/` |
| Decisions (ADRs) | `projects/{JERRY_PROJECT}/decisions/` or `docs/design/` |
| Research, analysis, reviews | `projects/{JERRY_PROJECT}/` subdirectories |
| Orchestration artifacts | `projects/{JERRY_PROJECT}/orchestration/` |

These files survive context compaction and session boundaries. That's Jerry's core value — your work persists even when the context window doesn't.

---

## Developer Setup

> **This section is for contributors to the Jerry codebase.** If you installed Jerry as a plugin, you're done — go build something great.

See [CONTRIBUTING.md](https://github.com/geekatron/jerry/blob/main/CONTRIBUTING.md) for full development setup, coding standards, and platform-specific notes.

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

### Pre-commit Hooks Failing or Not Running

**Symptom:** Commits succeed without running tests, or hooks fail with "python not found" / "No such file or directory"

**Cause:** The `pre-commit install` command stamps an absolute path to the Python interpreter into `.git/hooks/pre-commit`. This path goes stale when you:
- Create a **git worktree** (the new worktree doesn't have the venv at the stamped path)
- **Rebuild** the virtual environment (`rm -rf .venv && uv sync`)
- **Move** the repository to a different directory

**Solution:**
```bash
# macOS / Linux
make setup

# Windows
uv sync && uv run pre-commit install
```

This regenerates the hook file with the correct Python path. The Jerry session start hook will also warn you automatically if it detects a stale path.

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

**Windows:**
```bash
git clone https://github.com/geekatron/jerry.git
cd jerry
uv sync                        # Install dependencies
uv run pre-commit install      # Install pre-commit hooks
uv run pytest --tb=short -q    # Run test suite
```

---

## Troubleshooting

Installation has a few rough edges — most of them are SSH or project configuration. Here's how to get through the common ones. If something isn't covered here, [file an issue](https://github.com/geekatron/jerry/issues) and we'll add it.

### Project Issues

**`<project-required>` or `<project-error>`**

This is the most common post-install issue. It means Jerry installed successfully but no project is configured — the skills need somewhere to write their output.

**Cause:** `JERRY_PROJECT` is not set, points to a non-existent project, or the project directory was created in the wrong location.

**Fix:**

1. Set the variable: `export JERRY_PROJECT=PROJ-001-my-project` (macOS/Linux) or `$env:JERRY_PROJECT = "PROJ-001-my-project"` (Windows)
2. Verify the directory exists **relative to your repo root**: `ls projects/$JERRY_PROJECT/`
3. If the directory exists but in the wrong place (e.g., your home directory), move it under your repo's `projects/` folder
4. If you haven't created a project yet, follow the [Configuration](#configuration) section — it takes two minutes

### SSH Authentication Issues

**"Permission denied (publickey)" when adding plugin source**

This is the second most common issue. The `owner/repo` shorthand uses SSH by default, which needs an SSH key configured for GitHub.

**Fix (pick one):**

1. **Use the HTTPS URL** (fastest fix — no SSH needed):
   ```
   /plugin marketplace add https://github.com/geekatron/jerry.git
   ```

2. **Set up SSH keys** (if you use GitHub regularly):
   - Follow [GitHub's SSH key guide](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)
   - After setup, retry: `/plugin marketplace add geekatron/jerry`

3. **Configure Git to rewrite SSH to HTTPS globally** (fixes it for all Git operations):
   ```bash
   git config --global url."https://github.com/".insteadOf git@github.com:
   ```
   Then retry the original command.

4. **Use the [Local Clone](#local-clone) method** — clone with HTTPS yourself, then point Claude Code at the local directory.

### Plugin Install Issues

**`/plugin` command not recognized**

Plugins require Claude Code 1.0.33 or later. Check and update:

1. Check your version: `claude --version`
2. Update Claude Code:
   - **Homebrew:** `brew upgrade claude-code`
   - **npm:** `npm update -g @anthropic-ai/claude-code`
   - **Native installer:** Re-run the install from [Claude Code setup](https://code.claude.com/docs/en/setup)
3. Restart Claude Code after updating

**Plugin source add fails (non-SSH error)**

If you're seeing an error that isn't about SSH authentication, check these:

1. Internet connection — the command needs to reach GitHub
2. Claude Code version — must be 1.0.33+
3. Corporate proxy/firewall — if your network restricts GitHub access, use the [Local Clone](#local-clone) method instead

### Plugin not found after adding source

If `/plugin install jerry@jerry-framework` returns "plugin not found," the source name doesn't match what Claude Code registered. If you followed [Step 2](#install-from-github) and already ran `/plugin marketplace list`, use the name you saw there. Otherwise:

1. Run `/plugin marketplace list` to see the actual source name
2. Use that name: `/plugin install jerry@<actual-name-from-list>`
3. If the source doesn't appear at all, try removing and re-adding: `/plugin marketplace remove jerry-framework` then re-run the add command

The source name comes from Jerry's [`.claude-plugin/marketplace.json`](https://github.com/geekatron/jerry/blob/main/.claude-plugin/marketplace.json) and should be `jerry-framework`, but it may register differently depending on how the source was added.

### Hook Issues

**uv: command not found**

uv isn't on your PATH yet. Install it or fix the path:

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# Restart your terminal
```

**Windows:**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
# Close and reopen PowerShell
```

If still not found after restarting your terminal, add to PATH manually:
- macOS/Linux: `export PATH="$HOME/.local/bin:$PATH"` (add to `~/.zshrc` or `~/.bashrc`)
- Windows: Add `%USERPROFILE%\.local\bin` to System PATH

**Hooks not firing**

Hooks are in early access — some may fail silently. Here's how to diagnose:

1. Verify uv is installed: `uv --version`
2. Restart Claude Code completely (close and reopen)
3. Check `/plugin` **Errors** tab for any issues related to hooks
4. See the [early access caveat](#enable-hooks-early-access) for which hooks are most stable

### Skill Issues

**Skills not appearing**

1. Check `/plugin` **Errors** tab for error indicators
2. Clear the plugin cache:
   - macOS/Linux: `rm -rf ~/.claude/plugins/cache`
   - Windows: `Remove-Item -Recurse -Force "$env:USERPROFILE\.claude\plugins\cache"`
3. Restart Claude Code
4. Reinstall: `/plugin uninstall jerry` then re-run the install command

### Path Issues on Windows

If you see "path not found" when adding a local plugin source:

- Use forward slashes in Claude Code: `C:/Users/name/plugins/jerry`
- Avoid backslashes or environment variables in the Claude Code command

---

## Updating

### GitHub-installed users

Jerry updates when the source repository updates. To pull the latest:

```
/plugin marketplace update jerry-framework
```

> **Source name differs?** Use the name from `/plugin marketplace list`: `/plugin marketplace update <name-from-list>`.

> **Auto-updates:** Community marketplaces like Jerry have auto-update disabled by default. To enable automatic updates at startup: run `/plugin`, go to the **Marketplaces** tab, select your Jerry source, and enable auto-update.

### Local clone users

```bash
cd ~/plugins/jerry && git pull origin main
```

Then refresh in Claude Code:

```
/plugin marketplace update jerry-framework
```

> **Source name differs?** Use the name from `/plugin marketplace list`.

---

## Uninstallation

### Remove the Plugin

```
/plugin uninstall jerry@jerry-framework
```

> **Source name differs?** Use the name from `/plugin marketplace list`: `/plugin uninstall jerry@<name-from-list>`.

### Remove the Plugin Source

```
/plugin marketplace remove jerry-framework
```

> **Not sure of the source name?** Run `/plugin marketplace list` to check.
>
> **Note:** Removing a marketplace source will uninstall any plugins you installed from it.

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

That's it. Clean slate.

---

## Getting Help

If something's broken, file it. If something's confusing, file that too. The docs get better when you tell us where they fall short.

- **GitHub Issues:** [github.com/geekatron/jerry/issues](https://github.com/geekatron/jerry/issues)
- **Documentation:** [jerry.geekatron.org](https://jerry.geekatron.org)
- **Claude Code Help:** Run `/help` in Claude Code
- **Claude Code Plugin Docs:** [code.claude.com/docs/en/discover-plugins](https://code.claude.com/docs/en/discover-plugins)

---

## License

Jerry Framework is open source under the [Apache License 2.0](https://github.com/geekatron/jerry/blob/main/LICENSE).
