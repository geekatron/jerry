# Bootstrap Guide

> How to set up Jerry's context distribution after cloning.

> **Who needs this?** Bootstrap is for developers contributing to Jerry's behavioral rules. If you installed Jerry as a plugin via `/plugin marketplace add`, you do not need to run bootstrap — skills and hooks work without it. Bootstrap is only needed when you're editing `.context/rules/` and want changes to auto-propagate to `.claude/rules/`.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Overview](#overview) | What bootstrap does and why |
| [Quick Start](#quick-start) | Get set up in 30 seconds |
| [How It Works](#how-it-works) | Architecture of .context/ and .claude/ |
| [Platform Notes](#platform-notes) | macOS, Linux, Windows differences |
| [Troubleshooting](#troubleshooting) | Common issues and fixes |
| [Rollback](#rollback) | How to undo the bootstrap |
| [Command Reference](#command-reference) | Bootstrap command options |

---

## Overview

Jerry stores its behavioral rules and pattern catalog in `.context/` (the canonical source). Claude Code reads them from `.claude/rules/` and `.claude/patterns/`. The bootstrap process syncs the two using platform-aware linking.

**Why two directories?**

- `.context/` is the **canonical source** — version-controlled, auditable, and distributable across worktrees and forks. Keeping the source of truth outside `.claude/` ensures rules can be reviewed, diffed, and governed independently of Claude Code's internal structure.
- `.claude/` is where **Claude Code looks** for auto-loaded rules and settings. Claude Code reads from this directory at session start — it cannot be redirected to `.context/` directly.
- Symlinks connect them so edits in either location propagate instantly. This gives developers a single editing surface while maintaining the separation needed for auditability and stable distribution.

---

## Quick Start

After cloning the repository:

```bash
# Full setup (includes bootstrap)
make setup

# Or bootstrap only
uv run python scripts/bootstrap_context.py

# Verify it worked
uv run python scripts/bootstrap_context.py --check
```

You should see:

```
Checking Jerry context sync status...

  rules: linked -> /path/to/jerry/.context/rules
  patterns: linked -> /path/to/jerry/.context/patterns

Status: OK
```

---

## How It Works

```
.context/                          .claude/
├── rules/  ──── symlink ────►    ├── rules/
├── patterns/ ── symlink ────►    ├── patterns/
└── templates/                     ├── agents/    (untouched)
                                   ├── commands/  (untouched)
                                   └── settings.json (untouched)
```

The bootstrap script (`scripts/bootstrap_context.py`) uses a platform-aware strategy:

| Platform | Linking Method | Notes |
|----------|---------------|-------|
| macOS | Relative symlinks | Instant, auto-propagating |
| Linux | Relative symlinks | Same as macOS |
| Windows (Developer Mode) | Symlinks | Requires Developer Mode enabled |
| Windows (standard) | Junction points | No admin required, directories only |
| Fallback | File copy | Works everywhere, requires re-sync on changes |

---

## Platform Notes

### macOS / Linux

Symlinks work out of the box. No special configuration needed.

### Windows

The script tries symlinks first (works with Developer Mode enabled), then falls back to junction points. Junction points:

- Work without admin privileges
- Only work for directories (which is all we need)
- Must be on the same drive as the source
- Propagate changes instantly, like symlinks

**To enable Developer Mode** (for symlinks): Settings > Update & Security > For developers > Developer Mode

### Git Worktrees

When using git worktrees, run bootstrap in each worktree:

```bash
cd ../my-worktree
uv run python scripts/bootstrap_context.py
```

---

## Troubleshooting

**"Could not find Jerry project root"**

You're not in the Jerry repository directory, or `CLAUDE.md` / `.context/` is missing. Make sure you cloned the full repo and are running from the project root.

**"already linked"**

You're already set up. Run `--check` to verify, or `--force` to re-link.

**"drift detected"**

Files in `.claude/rules/` don't match `.context/rules/`. This happens with file-copy setups (no symlinks). Re-run the bootstrap to re-sync:

```bash
uv run python scripts/bootstrap_context.py --force
```

**Windows junction point fails**

Ensure you're on the same drive as the repository. If that doesn't work, try running from an elevated prompt.

---

## Rollback

To undo the bootstrap and restore `.claude/rules/` and `.claude/patterns/` as regular directories:

```bash
# 1. Remove the symlinks/junctions
rm .claude/rules .claude/patterns        # macOS/Linux
# On Windows: rmdir .claude\rules .claude\patterns

# 2. Copy files back
cp -r .context/rules .claude/rules
cp -r .context/patterns .claude/patterns
```

To fully reverse the restructure (move canonical source back to `.claude/`):

```bash
# Remove symlinks
rm .claude/rules .claude/patterns

# Move canonical files back
mv .context/rules .claude/rules
mv .context/patterns .claude/patterns
```

After rollback, Claude Code will still read rules from `.claude/rules/` as before.

---

## Command Reference

| Command | What It Does |
|---------|-------------|
| `uv run python scripts/bootstrap_context.py` | Full bootstrap |
| `uv run python scripts/bootstrap_context.py --check` | Verify sync status |
| `uv run python scripts/bootstrap_context.py --force` | Re-sync (overwrites existing) |
| `uv run python scripts/bootstrap_context.py --quiet` | Minimal output (for CI) |
