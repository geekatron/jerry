# Project Workflow Rules

> Operational guidance for Jerry project-based work sessions.
> **SSOT:** `/worktracker` skill rules are the authoritative source for project structure, entity hierarchy, and worktracker integrity. This file provides session-start orientation and H-04 enforcement.

## Document Sections

| Section | Purpose |
|---------|---------|
| [HARD Rule Reference](#hard-rule-reference) | H-04 active project requirement |
| [Workflow Phases](#workflow-phases) | Before, during, after work |
| [Project Orientation](#project-orientation) | Minimal structural context for session start |
| [Project Resolution](#project-resolution) | How to handle missing project context |

---

## HARD Rule Reference

> H-04: Active project REQUIRED. MUST NOT proceed without `JERRY_PROJECT` set. See CLAUDE.md.

---

## Workflow Phases

| Phase | Actions |
|-------|---------|
| **Before** | Set `JERRY_PROJECT` env var. Check `PLAN.md`. Review `WORKTRACKER.md`. Read relevant `docs/knowledge/`. Invoke `/worktracker` for structural guidance. |
| **During** | Persist state to `WORKTRACKER.md` per WTI-001 through WTI-007. Update `PLAN.md`. Document decisions in `docs/design/`. |
| **After** | Update completion status. Capture learnings in `docs/experience/`. Commit with semantic messages. |

> **Integrity enforcement (HARD):** All worktracker operations MUST follow WTI-001 through WTI-007. See `skills/worktracker/rules/worktracker-behavior-rules.md` for full definitions.

---

## Project Orientation

Projects follow `projects/PROJ-{NNN}-{slug}/` with `PLAN.md`, `WORKTRACKER.md`, and `work/` decomposition into Epics, Features, Enablers, Stories, and Tasks. This is the project-based placement pattern; a repository-based pattern also exists (see `skills/worktracker/rules/worktracker-directory-structure.md` for both).

> **Authoritative source:** `skills/worktracker/rules/worktracker-directory-structure.md` defines both placement patterns, the full directory hierarchy, naming conventions (`{EntityId}-{slug}`), and entity containment rules. `skills/worktracker/rules/worktracker-entity-hierarchy.md` defines entity types, classification, and parent-child constraints. Invoke `/worktracker` for full structural guidance.

---

## Project Resolution

When `<project-required>` or `<project-error>` is received from SessionStart hook:

1. Parse available projects from hook output.
2. Present options via AskUserQuestion (list projects + "Create new" option).
3. If existing: instruct user to set `JERRY_PROJECT`. Invoke `/worktracker` for structural guidance if needed.
4. If new: invoke `/worktracker` for structural guidance, then auto-generate ID using `PROJ-{NNN}-{slug}` format (next available number from `projects/README.md`), create directory structure per `skills/worktracker/rules/worktracker-directory-structure.md`, and update `projects/README.md`.

See `quality-enforcement.md` for decision criticality levels (C1-C4).
