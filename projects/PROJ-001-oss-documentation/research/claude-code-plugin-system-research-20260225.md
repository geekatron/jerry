# Claude Code Plugin System Research

> **Date:** 2026-02-25
> **Purpose:** Verify claims in `docs/INSTALLATION.md` against official Claude Code plugin documentation
> **Sources:** [Official Plugin Docs](https://code.claude.com/docs/en/discover-plugins), [Claude Blog](https://claude.com/blog/claude-code-plugins), [Anthropic GitHub](https://github.com/anthropics/claude-code/blob/main/plugins/README.md), [Official Plugin Marketplace](https://github.com/anthropics/claude-plugins-official)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Key Findings](#key-findings) | Critical corrections for INSTALLATION.md |
| [Plugin System Architecture](#plugin-system-architecture) | How marketplaces, plugins, and scopes work |
| [Command Reference](#command-reference) | Verified command syntax |
| [Marketplace Terminology](#marketplace-terminology) | Official vs community marketplaces |
| [Discover Tab Behavior](#discover-tab-behavior) | What appears in the Discover tab and when |
| [Protocol Details](#protocol-details) | SSH vs HTTPS for marketplace add |
| [Official Marketplace Content](#official-marketplace-content) | What ships with Claude Code |
| [Corrections for INSTALLATION.md](#corrections-for-installationmd) | Specific claims to fix |

---

## Key Findings

1. **Jerry is NOT in the official Anthropic marketplace** — confirmed. Jerry is a community plugin. The official marketplace (`claude-plugins-official`) is maintained by Anthropic and includes only curated plugins (LSP servers, external integrations, dev workflows, output styles).

2. **The Discover tab shows ALL marketplaces** — after adding a marketplace source, its plugins appear in the Discover tab alongside official plugins. So the "Interactive Installation" section IS valid IF the user has already completed Step 1 (adding the marketplace source). The DA-001-it1 Critical finding partially overstated the issue.

3. **`/plugin marketplace add` uses `owner/repo` format by default** — this clones via git. The docs show both SSH and HTTPS URL formats work. The `owner/repo` shorthand likely uses the system's default git protocol.

4. **Marketplace name comes from `.claude-plugin/marketplace.json`** — confirmed. The `name` field in marketplace.json becomes the marketplace identifier. For Jerry, this is `jerry-framework`.

5. **Install syntax is `/plugin install plugin-name@marketplace-name`** — confirmed. Example: `/plugin install jerry@jerry-framework`.

6. **Scopes: User (default), Project, Local, Managed** — confirmed. User scope installs across all projects. Project scope adds to `.claude/settings.json` (version-controlled).

7. **Version requirement: Claude Code 1.0.33+** — confirmed. `/plugin` command requires this version.

8. **Auto-updates configurable per marketplace** — official marketplaces auto-update by default; third-party/community marketplaces do NOT auto-update by default.

9. **Removing a marketplace uninstalls its plugins** — important warning from official docs.

10. **Shortcuts available** — `/plugin market` works instead of `/plugin marketplace`; `rm` works instead of `remove`.

---

## Plugin System Architecture

### Two-Step Process

A marketplace is a catalog of plugins. Using one is a two-step process:
1. **Add the marketplace** — registers the catalog with Claude Code
2. **Install individual plugins** — browse the catalog and install what you want

Official docs analogy: "Think of it like adding an app store: adding the store gives you access to browse its collection, but you still choose which apps to download individually."

### Plugin Components

Plugins can contain:
- **Skills** — custom commands and context-aware prompts
- **MCP servers** — connections to external APIs
- **Hooks** — shell scripts that run on specific events
- **Agents** — specialized agent definitions

### Plugin Directory Structure

```
plugin-name/
.claude-plugin/
  plugin.json          # Plugin metadata (required)
  marketplace.json     # Marketplace catalog (for marketplace repos)
commands/              # Slash commands (optional)
agents/                # Agent definitions (optional)
skills/                # Skill definitions (optional)
hooks/                 # Event handlers (optional)
.mcp.json              # External tool configuration (optional)
README.md              # Documentation
```

---

## Command Reference

### Marketplace Management

| Command | Purpose |
|---------|---------|
| `/plugin marketplace add owner/repo` | Add GitHub marketplace via owner/repo shorthand |
| `/plugin marketplace add https://url.git` | Add marketplace via HTTPS URL |
| `/plugin marketplace add git@host:owner/repo.git` | Add marketplace via SSH URL |
| `/plugin marketplace add ./local/path` | Add local directory as marketplace |
| `/plugin marketplace add https://url.git#v1.0.0` | Add specific branch/tag |
| `/plugin marketplace list` | List all configured marketplaces |
| `/plugin marketplace update marketplace-name` | Refresh plugin listings |
| `/plugin marketplace remove marketplace-name` | Remove marketplace (uninstalls its plugins) |

**Shortcuts:** `/plugin market` = `/plugin marketplace`; `rm` = `remove`

### Plugin Management

| Command | Purpose |
|---------|---------|
| `/plugin install plugin-name@marketplace-name` | Install plugin (user scope by default) |
| `/plugin uninstall plugin-name@marketplace-name` | Remove plugin |
| `/plugin disable plugin-name@marketplace-name` | Disable without uninstalling |
| `/plugin enable plugin-name@marketplace-name` | Re-enable disabled plugin |
| `claude plugin install name@marketplace --scope project` | Install with specific scope (CLI) |

### Interactive UI

| Tab | Purpose |
|-----|---------|
| **Discover** | Browse available plugins from ALL added marketplaces |
| **Installed** | View and manage installed plugins (grouped by scope) |
| **Marketplaces** | Add, remove, or update marketplaces |
| **Errors** | View plugin loading errors |

---

## Marketplace Terminology

### Official Anthropic Marketplace
- Repository: `anthropics/claude-plugins-official`
- **Automatically available** — no `/plugin marketplace add` needed
- Auto-update enabled by default
- Maintained by Anthropic with quality/security standards
- Accepts third-party submissions via [submission form](https://clau.de/plugin-directory-submission)
- Contains: LSP plugins, external integrations (GitHub, Jira, Slack, etc.), dev workflow tools, output styles

### Community Marketplaces
- Any GitHub/GitLab/git repo with `.claude-plugin/marketplace.json`
- Must be added manually via `/plugin marketplace add`
- Auto-update disabled by default (can be enabled)
- No Anthropic quality review
- Jerry is a community marketplace

### Key Distinction
"Marketplace" in Claude Code means "a registered catalog of plugins." It is NOT an Anthropic-hosted app store. However, the official Anthropic marketplace IS automatically available and IS curated.

---

## Discover Tab Behavior

**Critical finding for INSTALLATION.md:**

The Discover tab shows plugins from ALL added marketplaces, not just the official one. After running `/plugin marketplace add geekatron/jerry`, Jerry's plugins WILL appear in the Discover tab.

This means the "Interactive Installation" section in INSTALLATION.md is NOT impossible — it just requires that Step 1 (adding the marketplace source) has already been completed. The section needs to clarify this prerequisite, not be removed entirely.

---

## Protocol Details

### SSH vs HTTPS

The docs show three formats for adding a marketplace:
1. **`owner/repo` shorthand** — for GitHub repos. Protocol depends on system git configuration.
2. **HTTPS URL** — `https://github.com/owner/repo.git` — works without SSH keys
3. **SSH URL** — `git@github.com:owner/repo.git` — requires SSH key configuration

The `owner/repo` shorthand for GitHub repos uses SSH by default (confirmed by the SSH error users encounter). HTTPS URL bypass is available.

### Branch/Tag Pinning

Append `#ref` to the URL: `/plugin marketplace add https://github.com/owner/repo.git#v1.0.0`

---

## Official Marketplace Content

The official Anthropic marketplace (`claude-plugins-official`) includes:

### Code Intelligence (LSP)
C/C++ (clangd), C# (csharp-ls), Go (gopls), Java (jdtls), Kotlin, Lua, PHP (intelephense), Python (pyright), Rust (rust-analyzer), Swift (sourcekit), TypeScript

### External Integrations
GitHub, GitLab, Atlassian (Jira/Confluence), Asana, Linear, Notion, Figma, Vercel, Firebase, Supabase, Slack, Sentry

### Development Workflows
commit-commands, pr-review-toolkit, agent-sdk-dev, plugin-dev

### Output Styles
explanatory-output-style, learning-output-style

**Jerry is NOT in this list** — it is a community plugin requiring manual marketplace addition.

---

## Corrections for INSTALLATION.md

### 1. Interactive Installation Section
**Current claim:** Navigate to Discover tab and find Jerry
**Correction:** This WORKS but ONLY after the user has already completed Step 1 (adding the marketplace source). The section must note this prerequisite. Without adding the source first, Jerry will NOT appear in Discover.

### 2. marketplace.json Description
**Current claim (in marketplace.json):** "8 specialized agents"
**Correction:** 54 agents across 12 skills. Must update.

### 3. Auto-Update Behavior
**Current claim:** "You can enable auto-updates for Jerry so it refreshes automatically at startup."
**Correction:** Community marketplaces have auto-update DISABLED by default (unlike official ones). The instruction to enable it is correct.

### 4. Marketplace Removal Warning
**Missing:** The official docs warn that "Removing a marketplace will uninstall any plugins you installed from it." The uninstallation section should note this.

### 5. SSH Default for owner/repo
**Current claim:** "Claude Code clones the repository using SSH"
**Correction:** Confirmed accurate. The `owner/repo` shorthand uses SSH by default. HTTPS URL is the bypass.

### 6. Version Requirement
**Current claim:** Claude Code 1.0.33+
**Correction:** Confirmed accurate.

### 7. Plugin Namespace
**Missing context:** Official docs note that "Plugin commands are namespaced by the plugin name" — e.g., `commit-commands` provides `/commit-commands:commit`. Jerry's skills don't use this namespace pattern (they use `/problem-solving`, not `/jerry:problem-solving`), which may be because Jerry uses the skills directory structure rather than the commands directory structure.

---

## Sources

- [Discover and install prebuilt plugins through marketplaces](https://code.claude.com/docs/en/discover-plugins) — Official Claude Code documentation
- [Customize Claude Code with plugins](https://claude.com/blog/claude-code-plugins) — Anthropic blog post
- [claude-code/plugins/README.md](https://github.com/anthropics/claude-code/blob/main/plugins/README.md) — Anthropic GitHub
- [claude-plugins-official](https://github.com/anthropics/claude-plugins-official) — Official Anthropic plugin marketplace
- [awesome-claude-code-plugins](https://github.com/ccplugins/awesome-claude-code-plugins) — Community curated list
