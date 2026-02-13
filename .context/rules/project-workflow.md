# Project Workflow Rules

> Operational guidance for working with Jerry projects.
> Follow these steps Before, During, and After work sessions.

---

## Project-Based Workflow

Jerry uses isolated project workspaces. Each project has its own `PLAN.md` and `WORKTRACKER.md`.

**Active Project Resolution:**
1. Set `JERRY_PROJECT` environment variable (e.g., `export JERRY_PROJECT=PROJ-001-plugin-cleanup`)
2. If not set, Claude will prompt you to specify which project to work on
3. See `projects/README.md` for the project registry

**Project Structure:**
```
projects/PROJ-{nnn}-{slug}/
├── PLAN.md              # Project implementation plan
├── WORKTRACKER.md       # Work tracking document
└── .jerry/data/items/   # Operational state (work items)
```

---

## Before Starting Work

1. Set `JERRY_PROJECT` environment variable for your target project
2. Check `projects/${JERRY_PROJECT}/PLAN.md` for current plan
3. Review `projects/${JERRY_PROJECT}/WORKTRACKER.md` for task state
4. Read relevant `docs/knowledge/` for domain context

---

## During Work

1. Use Work Tracker to persist task state to `projects/${JERRY_PROJECT}/WORKTRACKER.md`
2. Update PLAN.md as implementation progresses
3. Document decisions in `docs/design/`

---

## After Completing Work

1. Update Work Tracker with completion status
2. Capture learnings in `docs/experience/` or `docs/wisdom/`
3. Commit with clear, semantic messages

---

## Creating a New Project

1. Check `projects/README.md` for next project number
2. Create directory: `mkdir -p projects/PROJ-{nnn}-{slug}/.jerry/data/items`
3. Create `PLAN.md` and `WORKTRACKER.md`
4. Add entry to `projects/README.md`
5. Set `JERRY_PROJECT` environment variable

---

## Required AskUserQuestion Flow

When `<project-required>` or `<project-error>` is received, Claude **MUST**:

1. **Parse** the available projects from the hook output
2. **Present options** via `AskUserQuestion`:
   - List available projects (from `AvailableProjects`)
   - Offer "Create new project" option
3. **Handle response**:
   - If existing project selected → instruct user to set `JERRY_PROJECT`
   - If new project → guide through creation flow
4. **DO NOT** proceed with unrelated work until resolved

**Example AskUserQuestion structure:**
```yaml
question: "Which project would you like to work on?"
header: "Project"
options:
  - label: "PROJ-001-plugin-cleanup"
    description: "[ACTIVE] Plugin system cleanup and refactoring"
  - label: "PROJ-002-example"
    description: "[DRAFT] Example project description"
  - label: "Create new project"
    description: "Start a new project workspace"
```

---

## Project Creation Flow

When user selects "Create new project":

1. **Get project details** via AskUserQuestion:
   - Slug/name (required): e.g., "api-redesign"
   - Description (optional)

2. **Auto-generate ID** using `NextProjectNumber` from hook:
   - Format: `PROJ-{NNN}-{slug}`
   - Example: `PROJ-003-api-redesign`

3. **Create project structure**:
   ```
   projects/PROJ-003-api-redesign/
   ├── PLAN.md              # Implementation plan template
   ├── WORKTRACKER.md       # Work tracking document
   └── .jerry/data/items/   # Operational state
   ```

4. **Update registry**: Add entry to `projects/README.md`

5. **Instruct user**: Set `JERRY_PROJECT=PROJ-003-api-redesign`

---

## Quick Reference

| Phase | Key Actions |
|-------|-------------|
| **Before** | Set JERRY_PROJECT, check PLAN.md, review WORKTRACKER.md |
| **During** | Persist to WORKTRACKER.md, update PLAN.md, document decisions |
| **After** | Update completion status, capture learnings, commit |
