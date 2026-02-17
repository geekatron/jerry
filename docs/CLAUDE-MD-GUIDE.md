# CLAUDE.md Contributor Guide

> How Jerry's context loading works and how to modify it.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Context Architecture](#context-architecture) | How tiered loading works |
| [Modifying Rules](#modifying-rules) | Adding or editing behavioral rules |
| [Modifying Patterns](#modifying-patterns) | Adding or editing pattern files |
| [CLAUDE.md Constraints](#claudemd-constraints) | Why CLAUDE.md must stay small |
| [Adding Skills](#adding-skills) | Creating new skill files |

---

## Context Architecture

Jerry uses a **tiered hybrid loading strategy** to manage Claude Code's context window:

| Tier | Content | Loading | Size |
|------|---------|---------|------|
| 1 | `CLAUDE.md` | Always loaded at session start | ~80 lines |
| 2 | `.claude/rules/` | Auto-loaded by Claude Code | ~500 lines |
| 3 | `skills/*/SKILL.md` | On-demand via `/skill` invocation | ~1,500+ lines |
| 4 | Reference docs | Explicit file access when needed | Unlimited |

**Why this matters:** LLM performance degrades as context fills ([Context Rot](https://research.trychroma.com/context-rot)). By loading only what's needed, Jerry maintains high-quality responses across long sessions.

### File Locations

```
jerry/
├── CLAUDE.md                    # Tier 1 - Always loaded (~80 lines)
├── .context/                    # Canonical source (version-controlled)
│   ├── rules/                   # Behavioral rules
│   ├── patterns/                # Pattern catalog
│   └── templates/               # Worktracker templates
├── .claude/                     # Claude Code reads from here
│   ├── rules/ → .context/rules/    # Symlinked from .context/
│   ├── patterns/ → .context/patterns/ # Symlinked from .context/
│   ├── agents/                  # Agent definitions (not symlinked)
│   └── settings.json            # Claude Code settings
└── skills/                      # Tier 3 - On-demand
    ├── worktracker/SKILL.md
    ├── problem-solving/SKILL.md
    └── ...
```

---

## Modifying Rules

Rules in `.context/rules/` are auto-loaded by Claude Code via the `.claude/rules/` symlink.

**To add a new rule:**

1. Create the file in `.context/rules/your-rule.md`
2. It automatically appears in `.claude/rules/` via symlink
3. Claude Code will auto-load it at next session start

**To edit a rule:** Edit the file in `.context/rules/`. Changes propagate instantly through the symlink.

**Important:** Rules are loaded at every session start, so keep them concise and focused. Each rule file adds to the Tier 2 token cost.

---

## Modifying Patterns

Patterns in `.context/patterns/` provide architectural reference. They are auto-loaded by Claude Code but are reference material, not behavioral rules.

The pattern catalog is at `.context/patterns/PATTERN-CATALOG.md`.

---

## CLAUDE.md Constraints

CLAUDE.md MUST stay between **60-80 lines**. This is a hard constraint.

**What belongs in CLAUDE.md:**
- Identity and core mission (2-3 lines)
- Navigation table pointing to other locations
- Critical hard constraints (P-003, P-020, P-022)
- Python environment rule (UV only)
- Quick reference for CLI and skills

**What does NOT belong in CLAUDE.md:**
- Detailed coding standards (use `.context/rules/`)
- Entity hierarchies (use `/worktracker` skill)
- Pattern definitions (use `.context/patterns/`)
- Process documentation (use `skills/`)

---

## Adding Skills

Skills provide on-demand context loading (Tier 3).

**To create a new skill:**

1. Create `skills/your-skill/SKILL.md`
2. Add a frontmatter block with `name`, `description`, `version`
3. Add the skill to CLAUDE.md's Quick Reference table
4. Optionally add agents in `skills/your-skill/agents/`

See existing skills in `skills/` for examples.

---

## Bootstrap for New Contributors

After cloning, run the bootstrap to set up symlinks:

```bash
uv run python scripts/bootstrap_context.py
```

See [Bootstrap Guide](BOOTSTRAP.md) for full details.
