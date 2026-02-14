# Project Workflow Rules

> Operational guidance for Jerry project-based work sessions.

## Document Sections

| Section | Purpose |
|---------|---------|
| [HARD Rule Reference](#hard-rule-reference) | H-04 active project requirement |
| [Workflow Phases](#workflow-phases) | Before, during, after work |
| [Project Structure](#project-structure) | Directory layout |
| [Project Resolution](#project-resolution) | How to handle missing project context |

---

## HARD Rule Reference

> H-04: Active project REQUIRED. MUST NOT proceed without `JERRY_PROJECT` set. See CLAUDE.md.

---

## Workflow Phases

| Phase | Actions |
|-------|---------|
| **Before** | Set `JERRY_PROJECT` env var. Check `PLAN.md`. Review `WORKTRACKER.md`. Read relevant `docs/knowledge/`. |
| **During** | Persist state to `WORKTRACKER.md`. Update `PLAN.md`. Document decisions in `docs/design/`. |
| **After** | Update completion status. Capture learnings in `docs/experience/`. Commit with semantic messages. |

---

## Project Structure

```
projects/PROJ-{NNN}-{slug}/
  PLAN.md              # Implementation plan
  WORKTRACKER.md       # Work tracking
  .jerry/data/items/   # Operational state
  work/                # Phase documents
  research/            # Research artifacts
  synthesis/           # Synthesis documents
  decisions/           # ADRs
```

---

## Project Resolution

When `<project-required>` or `<project-error>` is received from SessionStart hook:

1. Parse available projects from hook output.
2. Present options via AskUserQuestion (list projects + "Create new" option).
3. If existing: instruct user to set `JERRY_PROJECT`.
4. If new: auto-generate ID from `NextProjectNumber`, create structure, update `projects/README.md`.

**Creating a new project:**
1. Get slug from user.
2. Generate `PROJ-{NNN}-{slug}` using next available number.
3. Create directory with `PLAN.md`, `WORKTRACKER.md`, `.jerry/data/items/`.
4. Add to `projects/README.md`.

See `quality-enforcement.md` for decision criticality levels (C1-C4).
