---
name: Bootstrap
description: This skill should be used when the user says "bootstrap", "set up Jerry", "configure guardrails", "initialize Jerry", or asks how to get started with Jerry. Sets up Jerry's context distribution by syncing behavioral rules and patterns.
version: 1.0.0
allowed-tools:
  - Read
  - Write
  - Bash
activation-keywords:
  - "bootstrap"
  - "set up Jerry"
  - "configure guardrails"
  - "initialize Jerry"
  - "context distribution"
  - "sync rules"
  - "get started"
---

# Bootstrap Skill

> **Version:** 1.0.0
> **Framework:** Jerry Bootstrap
> **Constitutional Compliance:** Jerry Constitution v1.0

Let's get your bindings adjusted so you don't have any Jerry moments.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Purpose](#purpose) | What this skill does |
| [When to Use This Skill](#when-to-use-this-skill) | Activation triggers |
| [What This Does](#what-this-does) | How context distribution works |
| [Quick Start](#quick-start) | Getting started commands |
| [How It Works](#how-it-works) | Architecture of the sync mechanism |
| [Options](#options) | CLI flags and arguments |
| [Troubleshooting](#troubleshooting) | Common issues and solutions |
| [For Contributors](#for-contributors) | Adding new rules and patterns |
| [Available Agents](#available-agents) | Agent registry for this skill |
| [Constitutional Compliance](#constitutional-compliance) | Principle mapping |
| [Integration with Other Skills](#integration-with-other-skills) | Cross-skill dependencies |
| [Templates](#templates) | Template usage |
| [References](#references) | Canonical sources |

---

## Document Audience (Triple-Lens)

This SKILL.md serves multiple audiences:

| Level | Audience | Sections to Focus On |
|-------|----------|---------------------|
| **L0 (ELI5)** | New users, contributors | [What This Does](#what-this-does), [Quick Start](#quick-start), [How It Works](#how-it-works) |
| **L1 (Engineer)** | Developers setting up Jerry | [Quick Start](#quick-start), [Options](#options), [Troubleshooting](#troubleshooting) |
| **L2 (Architect)** | Framework maintainers | [How It Works](#how-it-works), [For Contributors](#for-contributors), [Constitutional Compliance](#constitutional-compliance) |

---

## Purpose

The Bootstrap skill sets up Jerry's context distribution system by synchronizing behavioral rules and patterns from the canonical source (`.context/`) to Claude Code's read location (`.claude/`). This ensures that Claude Code always has access to the latest framework rules.

### Key Capabilities

- **Platform-Aware Linking** - Uses the best available strategy per platform (symlinks, junction points, or file copy)
- **Drift Detection** - Identifies when copied files are out of sync with the source
- **Idempotent Setup** - Safe to run multiple times; won't overwrite unless `--force` is used
- **Validation Mode** - Check existing setup without making changes (`--check`)

---

## When to Use This Skill

Activate when:

- First time setting up the Jerry repository
- After pulling updates that modify `.context/rules/` or `.context/patterns/`
- Troubleshooting Claude Code not seeing the latest rules
- Migrating Jerry to a new machine
- Verifying that context distribution is working correctly

---

## What This Does

Jerry's behavioral rules and patterns live in `.context/` (the canonical source). Claude Code reads them from `.claude/rules/` and `.claude/patterns/`. This skill syncs the two using platform-aware linking:

- **macOS/Linux**: Symlinks (instant, auto-propagating)
- **Windows with Developer Mode**: Symlinks
- **Windows without Developer Mode**: Junction points (no admin required)
- **Fallback**: File copy with drift detection

---

## Quick Start

Run the bootstrap script to set up context distribution:

```bash
# Full setup
uv run python scripts/bootstrap_context.py

# Check if you're already set up
uv run python scripts/bootstrap_context.py --check

# Force re-sync (overwrites existing)
uv run python scripts/bootstrap_context.py --force
```

---

## How It Works

```
.context/                          .claude/
├── rules/  ──── symlink ────►    ├── rules/
├── patterns/ ── symlink ────►    ├── patterns/
└── templates/                     ├── agents/    (stays)
                                   ├── commands/  (stays)
                                   └── settings.json (stays)
```

The script (`scripts/bootstrap_context.py`) handles:

1. **Platform detection** - Picks the right linking strategy
2. **Existing setup check** - Won't overwrite unless `--force`
3. **Fallback chain** - Symlink -> junction point -> file copy
4. **Drift detection** - `--check` verifies sync integrity

---

## Options

| Flag | What It Does |
|------|-------------|
| (none) | Full bootstrap with friendly output |
| `--check` | Verify existing setup without changes |
| `--force` | Overwrite existing links/copies |
| `--quiet` | Minimal output (for CI/scripts) |

---

## Troubleshooting

**"Source not found"** - You're not in the Jerry repo root, or `.context/` is missing. Make sure you cloned the full repo.

**"Already linked"** - You're good! Run `--check` to verify, or `--force` to re-link.

**Windows junction point fails** - Try running from an elevated prompt, or ensure you're on the same drive as the repo.

**Drift detected** - Files in `.claude/rules/` don't match `.context/rules/`. This happens with file-copy setups. Run without `--check` to re-sync.

---

## For Contributors

If you add new rules to `.context/rules/` or patterns to `.context/patterns/`, they'll automatically appear in `.claude/` for anyone using symlinks/junctions. File-copy users need to re-run bootstrap.

### Adding New Rules

1. Create the rule file in `.context/rules/{rule-name}.md`
2. Follow the markdown navigation standards (H-23/H-24) - include navigation table
3. Use tier vocabulary (HARD/MEDIUM/SOFT) per `quality-enforcement.md`
4. Add an L2-REINJECT comment if the rule is critical
5. Test that symlink users see the new rule immediately
6. Document in release notes that file-copy users should re-bootstrap

---

## Available Agents

This skill does not use agent-based workflows. It provides a single bootstrap script that handles all setup operations.

**Invocation:** Run the bootstrap script directly via `uv run python scripts/bootstrap_context.py`

---

## Constitutional Compliance

The Bootstrap skill adheres to the **Jerry Constitution v1.0**:

| Principle | Requirement | Implementation |
|-----------|-------------|----------------|
| P-002: File Persistence | State persisted to filesystem | Symlinks/junctions or file copies created on disk |
| P-022: No Deception | Transparent about actions | Script reports exactly what it does (link/copy/skip) |
| H-05: UV Only | Use uv for Python execution | Script invoked via `uv run python` |

**Self-Critique Checklist (Before Response):**
- [ ] P-002: Are symlinks/copies persisted to disk?
- [ ] P-022: Does script output clearly state what happened?
- [ ] H-05: Did we use `uv run` instead of `python` directly?

---

## Integration with Other Skills

The bootstrap skill is foundational and does not integrate with other skills. However, it enables all other skills by ensuring that:

- `.context/rules/quality-enforcement.md` is accessible for adversarial quality mode
- `.context/rules/architecture-standards.md` is accessible for hexagonal architecture validation
- `.context/rules/coding-standards.md` is accessible for type hints and docstring enforcement
- `.context/patterns/` is accessible for CQRS, event sourcing, and other patterns

---

## Templates

The bootstrap skill does not use templates. It operates directly on the `.context/` directory structure.

---

## References

- Bootstrap script: `scripts/bootstrap_context.py`
- Source directory: `.context/rules/`, `.context/patterns/`
- Target directory: `.claude/rules/`, `.claude/patterns/`
- Jerry Constitution: `docs/governance/JERRY_CONSTITUTION.md`
- Platform-specific linking: Windows junction points, Unix/macOS symlinks

---

*Skill Version: 1.0.0*
*Constitutional Compliance: Jerry Constitution v1.0*
*Created: 2026-02-12*
*Last Updated: 2026-02-16*
