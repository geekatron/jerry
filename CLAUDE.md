# CLAUDE.md - Jerry Framework Root Context

> Procedural memory for Claude Code. Loaded once at session start.

## Identity

**Jerry** is a framework for behavior and workflow guardrails that helps solve problems while accruing knowledge, wisdom, and experience.

**Core Problem**: Context Rot - LLM performance degrades as context fills. See [Chroma Research](https://research.trychroma.com/context-rot).

**Core Solution**: Filesystem as infinite memory. Persist state to files; load selectively.

## Navigation

> Find information rather than reading it here. Auto-loaded content marked with (A).

| Need | Location |
|------|----------|
| Coding standards | `.claude/rules/` (A) |
| Work tracking | `/worktracker` skill |
| Problem solving | `/problem-solving` skill |
| Architecture | `/architecture` skill |
| NASA SE | `/nasa-se` skill |
| Orchestration | `/orchestration` skill |
| Transcript | `/transcript` skill |
| Templates | `.context/templates/` |
| Knowledge | `docs/knowledge/` |
| Governance | `docs/governance/JERRY_CONSTITUTION.md` |

**Key:** (A) = Auto-loaded. See `skills/{skill-name}/SKILL.md` for skill details.

## Active Project

Set `JERRY_PROJECT` environment variable: `export JERRY_PROJECT=PROJ-001-example`

The SessionStart hook (`scripts/session_start_hook.py`) provides context via XML tags:

| Tag | Meaning | Claude Action |
|-----|---------|---------------|
| `<project-context>` | Valid project active | Proceed with work |
| `<project-required>` | No project set | Use AskUserQuestion to select/create |
| `<project-error>` | Invalid project ID | Help user fix or select valid project |

**Hard Rule**: Claude MUST NOT proceed without active project context. See `projects/README.md`.

## Critical Constraints (HARD)

> These constraints CANNOT be overridden. Violations will be blocked.

| Principle | Constraint | Rule |
|-----------|------------|------|
| **P-003** | No Recursive Subagents | Max ONE level: orchestrator -> worker |
| **P-020** | User Authority | User decides. Never override. Ask before destructive ops |
| **P-022** | No Deception | Never deceive about actions, capabilities, or confidence |

### Python Environment (HARD)

**Python 3.11+ with UV only.** Never use `python`, `pip`, or `pip3` directly.

```bash
uv run pytest tests/     # CORRECT
uv run jerry <command>   # CORRECT
python script.py         # FORBIDDEN
```

**Reference**: `docs/governance/JERRY_CONSTITUTION.md`

## Quick Reference

**CLI** (v0.1.0): `jerry session start|end|status|abandon` | `jerry items list|show` | `jerry projects list|context|validate`

**Skills** (invoke proactively - see `skills/` for details):
| Skill | Purpose |
|-------|---------|
| `/worktracker` | Task/issue management |
| `/problem-solving` | Research, analysis, root cause |
| `/nasa-se` | Requirements, V&V, reviews |
| `/orchestration` | Multi-phase workflows |
| `/architecture` | Design decisions |
| `/transcript` | Transcription parsing |
