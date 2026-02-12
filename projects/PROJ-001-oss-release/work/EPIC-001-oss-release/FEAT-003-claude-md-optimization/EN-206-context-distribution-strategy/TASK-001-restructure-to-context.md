# EN-206:TASK-001: Restructure - Move Rules/Patterns to .context/

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
CREATED: 2026-02-02 (Claude)
PURPOSE: Move canonical rules and patterns from .claude/ to .context/
-->

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Created:** 2026-02-02T06:30:00Z
> **Due:** 2026-02-07T00:00:00Z
> **Completed:** -
> **Parent:** EN-206
> **Owner:** Claude
> **Effort:** 2

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task objective - move rules/patterns to .context/ |
| [Current State](#current-state) | Where rules/patterns live now |
| [Target State](#target-state) | Where they should live |
| [Implementation Steps](#implementation-steps) | Step-by-step execution |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |

---

## Summary

Move Jerry's behavioral rules and patterns from `.claude/` (project-level memory, not distributed) to `.context/` (version-controlled, distributable). This establishes `.context/` as the **canonical source** for all behavioral content.

**Scope:**
- Move `.claude/rules/` → `.context/rules/`
- Move `.claude/patterns/` → `.context/patterns/`
- Update references in CLAUDE.md, SKILL.md files, and documentation
- Ensure .context/ is tracked in git (not gitignored)

---

## Current State

```
.claude/
├── rules/
│   ├── architecture-standards.md
│   ├── coding-standards.md
│   ├── error-handling-standards.md
│   ├── file-organization.md
│   ├── mandatory-skill-usage.md
│   ├── markdown-navigation-standards.md
│   ├── project-workflow.md
│   ├── python-environment.md
│   ├── testing-standards.md
│   └── tool-configuration.md
├── patterns/
│   └── PATTERN-CATALOG.md (and subdirectories)
├── agents/
├── commands/
└── settings.json
```

**Problem:** This content is NOT distributed via plugin. Users don't get these rules automatically.

---

## Target State

```
.context/                        # NEW: Canonical source (version-controlled)
├── rules/
│   ├── architecture-standards.md
│   ├── coding-standards.md
│   ├── error-handling-standards.md
│   ├── file-organization.md
│   ├── mandatory-skill-usage.md
│   ├── markdown-navigation-standards.md
│   ├── project-workflow.md
│   ├── python-environment.md
│   ├── testing-standards.md
│   └── tool-configuration.md
├── patterns/
│   └── PATTERN-CATALOG.md (and subdirectories)
└── templates/                   # EXISTING: Already in .context/
    └── worktracker/

.claude/                         # Synced from .context/ (via chosen mechanism)
├── rules/ ──────────────────────► Synced from .context/rules/
├── patterns/ ───────────────────► Synced from .context/patterns/
├── agents/                      # Stays here (plugin component)
├── commands/                    # Stays here (plugin component)
└── settings.json                # Stays here (user config)
```

---

## Implementation Steps

### Step 1: Create .context/ Structure

```bash
mkdir -p .context/rules
mkdir -p .context/patterns
```

### Step 2: Move Rules

```bash
# Move all rule files
mv .claude/rules/*.md .context/rules/
```

### Step 3: Move Patterns

```bash
# Move pattern catalog and subdirectories
mv .claude/patterns/* .context/patterns/
```

### Step 4: Update References

Update paths in:
- [ ] CLAUDE.md - Navigation section
- [ ] Skill SKILL.md files that reference rules
- [ ] Documentation that references .claude/rules/

### Step 5: Set Up Initial Sync

Until TASK-002 implements the full sync mechanism:
```bash
# Temporary: symlink for development
ln -s ../.context/rules .claude/rules
ln -s ../.context/patterns .claude/patterns
```

### Step 6: Verify

- [ ] Claude Code still loads rules correctly
- [ ] All references resolve
- [ ] Git tracks .context/ (not gitignored)

---

## Acceptance Criteria

### Definition of Done

- [ ] `.context/rules/` contains all behavioral rules
- [ ] `.context/patterns/` contains pattern catalog
- [ ] `.claude/rules/` and `.claude/patterns/` are synced (symlink or copy)
- [ ] All references in documentation updated
- [ ] Claude Code session starts correctly with rules loaded
- [ ] Changes committed to git

### Technical Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| TC-1 | `.context/` is git-tracked | [ ] |
| TC-2 | All rule files moved | [ ] |
| TC-3 | All pattern files moved | [ ] |
| TC-4 | Claude Code rules loading works | [ ] |
| TC-5 | No broken references | [ ] |

---

## Related Items

### Hierarchy

- **Parent:** [EN-206: Context Distribution Strategy](./EN-206-context-distribution-strategy.md)

### Dependencies

- **Depends On:** SPIKE-001 (to understand sync mechanism options)
- **Enables:** TASK-002 (implement sync mechanism)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-02T06:30:00Z | Claude | pending | Task created |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | Task |
| **SAFe** | Task |
| **JIRA** | Task |
