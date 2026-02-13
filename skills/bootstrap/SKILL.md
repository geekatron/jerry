---
name: Bootstrap
description: This skill should be used when the user says "bootstrap", "set up Jerry", "configure guardrails", "initialize Jerry", or asks how to get started with Jerry. Sets up Jerry's context distribution by syncing behavioral rules and patterns.
version: 1.0.0
---

# Bootstrap Skill

> Let's get your bindings adjusted so you don't have any Jerry moments.

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

---

*Skill Version: 1.0.0*
*Created: 2026-02-12*
