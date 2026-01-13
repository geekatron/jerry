---
name: worktracker-decomposition
description: |
  This skill should be used when the user asks to "decompose task",
  "break down work", "create subtasks", or mentions task breakdown.
version: 1.0.0
allowed-tools:
  - Read
  - Write
  - Edit
---

# WORKTRACKER Decomposition Skill

> Transform monolithic WORKTRACKER files into multi-file hub-and-spoke architectures for surviving context rot.

---

## Purpose

The WORKTRACKER Decomposition skill provides automated analysis and transformation of large, monolithic work tracking files into a **Hub and Spoke architecture**. This pattern addresses **Context Rot** - the phenomenon where LLM performance degrades as context windows fill.

### The Problem

As work tracking files grow beyond ~500 lines:
- **Context consumption** increases (less room for actual work)
- **Navigation** becomes difficult (finding active work requires scrolling)
- **Compaction vulnerability** increases (key state lost after context compaction)
- **Parallel work blocked** (single file means sequential updates only)

### The Solution

The Hub and Spoke pattern:
- **Hub** (`WORKTRACKER.md`): <150 line navigation index with status dashboard
- **Spokes** (`work/*.md`): Detailed phase files, each self-contained
- **Progressive Detail**: Active work gets maximum detail, completed work stays minimal

---

## Commands

### Analyze WORKTRACKER

Analyze a WORKTRACKER file to assess whether decomposition is needed.

```
@worktracker-decompose analyze <path>
```

**Arguments:**
- `path`: Path to WORKTRACKER.md file (required)

**Example:**
```
@worktracker-decompose analyze projects/PROJ-002/WORKTRACKER.md
```

**Output:**
```
WORKTRACKER Analysis Report
===========================

File: projects/PROJ-002/WORKTRACKER.md
Size: 847 lines

Trigger Status:
  [X] HARD TRIGGER: Size exceeds 800 lines (847)
  [X] SOFT TRIGGER: Size exceeds 500 lines
  [ ] Pain indicators detected

Structure Detected:
  - 6 numbered phases found
  - 2 cross-cutting categories (BUGS, TECHDEBT)
  - 3 phases completed, 1 in progress

Phase Breakdown:
  | Phase | Lines | Status |
  |-------|-------|--------|
  | Phase 1 | 120 | DONE |
  | Phase 2 | 145 | DONE |
  | Phase 3 | 98 | DONE |
  | Phase 4 | 234 | IN_PROGRESS |
  | Phase 5 | 45 | PENDING |
  | Phase 6 | 30 | PENDING |
  | BUGS | 75 | - |
  | TECHDEBT | 100 | - |

RECOMMENDATION: Decomposition recommended
  - File exceeds hard trigger threshold
  - Multiple completed phases can be archived minimally
  - Active phase will benefit from dedicated file

Run '@worktracker-decompose execute <path>' to proceed.
```

---

### Execute Decomposition

Execute the decomposition process, transforming the monolithic file into hub-and-spoke structure.

```
@worktracker-decompose execute <path> [--dry-run] [--backup]
```

**Arguments:**
- `path`: Path to WORKTRACKER.md file (required)
- `--dry-run`: Preview changes without writing files (default: false)
- `--backup`: Create backup commit before decomposition (default: true)

**Example:**
```
@worktracker-decompose execute projects/PROJ-002/WORKTRACKER.md
```

**Output:**
```
WORKTRACKER Decomposition
=========================

Pre-Flight Checks:
  [X] Backup created: git commit abc123f
  [X] Phase boundaries identified
  [X] Cross-cutting categories identified
  [X] Active work phase confirmed

Creating Structure:
  [X] Created: work/
  [X] Created: work/PHASE-01-SETUP.md (98 lines)
  [X] Created: work/PHASE-02-IMPLEMENTATION.md (112 lines)
  [X] Created: work/PHASE-03-TESTING.md (76 lines)
  [X] Created: work/PHASE-04-DEPLOYMENT.md (189 lines) <- ACTIVE
  [X] Created: work/PHASE-05-MONITORING.md (42 lines)
  [X] Created: work/PHASE-06-DOCUMENTATION.md (28 lines)
  [X] Created: work/PHASE-BUGS.md (62 lines)
  [X] Created: work/PHASE-TECHDEBT.md (85 lines)

Transforming Hub:
  [X] Replaced: WORKTRACKER.md (847 -> 109 lines)
  [X] Added: Navigation Graph
  [X] Added: Quick Status Dashboard
  [X] Added: Session Resume Protocol

Post-Decomposition:
  [X] All navigation links verified
  [X] Session context sections added to active files
  [X] Git commit created: "docs: restructure WORKTRACKER to multi-file format"

Summary:
  Before: 1 file, 847 lines
  After: 9 files, 801 total lines (109 hub + 692 spokes)
  Hub reduction: -87%
```

---

### Validate Decomposition

Validate an existing decomposed structure for completeness and correctness.

```
@worktracker-decompose validate <path>
```

**Arguments:**
- `path`: Path to project directory containing WORKTRACKER.md and work/ folder

**Example:**
```
@worktracker-decompose validate projects/PROJ-002/
```

**Output:**
```
WORKTRACKER Validation Report
=============================

Hub Validation (WORKTRACKER.md):
  [X] Size under limit: 109 lines (< 150)
  [X] Navigation graph present
  [X] Quick status dashboard present
  [X] Session resume protocol present
  [X] All phase links valid

Spoke Validation (work/):
  [X] PHASE-01-SETUP.md
      - Navigation section: OK
      - Task summary: OK
      - Back link: OK
  [X] PHASE-02-IMPLEMENTATION.md
      - Navigation section: OK
      - Task summary: OK
      - Back link: OK
  ...

Cross-References:
  [X] Hub -> Spoke links: 8/8 valid
  [X] Spoke -> Hub links: 8/8 valid
  [X] Spoke -> Spoke links: 12/12 valid

Session Context:
  [X] Active phase (PHASE-04) has session context section
  [!] Warning: PHASE-05-MONITORING.md missing session context (pending phase, optional)

Result: VALID (1 warning)
```

---

### Add Phase

Add a new phase file to an existing decomposed structure.

```
@worktracker-decompose add-phase <path> --name "<Phase Name>" [--number N]
```

**Arguments:**
- `path`: Path to project directory (required)
- `--name`: Name of the new phase (required)
- `--number`: Phase number (default: next sequential number)

**Example:**
```
@worktracker-decompose add-phase projects/PROJ-002/ --name "Security Audit"
```

**Output:**
```
Adding Phase: Phase 7 - Security Audit
======================================

Created: work/PHASE-07-SECURITY-AUDIT.md
  - Template populated
  - Navigation links added
  - Empty task summary ready

Updated: WORKTRACKER.md
  - Added to quick status dashboard
  - Navigation graph unchanged (auto-discovered)

Updated: work/PHASE-06-DOCUMENTATION.md
  - Added "Phase 7 ->" navigation link

Ready for use. Add tasks with @worktracker create --phase 7
```

---

### Add Category

Add a new cross-cutting category file.

```
@worktracker-decompose add-category <path> --name "<Category Name>"
```

**Arguments:**
- `path`: Path to project directory (required)
- `--name`: Name of the category (required, e.g., SECURITY, PERFORMANCE)

**Example:**
```
@worktracker-decompose add-category projects/PROJ-002/ --name "Security"
```

**Output:**
```
Adding Category: SECURITY
=========================

Created: work/PHASE-SECURITY.md
  - Template populated for security issues
  - Navigation to hub added
  - Empty summary table ready

Updated: WORKTRACKER.md
  - Added to quick status dashboard under "Support" section

Ready for use. Add security items manually or with @worktracker create --type security
```

---

## Trigger Criteria

| Trigger | Threshold | Action |
|---------|-----------|--------|
| **Soft Trigger** | WORKTRACKER.md > 500 lines | Consider decomposition |
| **Hard Trigger** | WORKTRACKER.md > 800 lines | Decomposition required |
| **Pain Indicator** | Difficulty finding active work | Decomposition recommended |
| **Compaction Failure** | Lost state after context compaction | Decomposition urgent |

---

## File Types Created

| Type | Pattern | Purpose |
|------|---------|---------|
| **Sequential Phase** | `PHASE-{NN}-{NAME}.md` | Numbered phase work tracking |
| **Cross-Cutting Category** | `PHASE-{CATEGORY}.md` | Bugs, tech debt, discoveries |
| **Initiative** | `INITIATIVE-{NAME}.md` | Complex multi-phase work |
| **Implementation Domain** | `PHASE-IMPL-{DOMAIN}.md` | Detailed implementation tasks |

---

## Templates

### Phase File Template

```markdown
# Phase N: {Title}

> **Status**: {EMOJI} {STATUS} ({PERCENT}%)
> **Goal**: {One-line goal description}

---

## Navigation

| Link | Description |
|------|-------------|
| [<- WORKTRACKER](../WORKTRACKER.md) | Back to index |
| [<- Phase N-1](PHASE-{N-1}-*.md) | Previous phase |
| [Phase N+1 ->](PHASE-{N+1}-*.md) | Next phase |

---

## Task Summary

| Task ID | Title | Status | Subtasks | Output |
|---------|-------|--------|----------|--------|

---

## {TASK-ID}: {Task Title} {STATUS_EMOJI}

{Task details}

---

## Session Context

### For Resuming Work
1. Check task summary for current status
2. Read active task section for details
3. Check dependencies before starting

### Key Files to Know

| File | Purpose |
|------|---------|

---

## Document History

| Date | Author | Changes |
|------|--------|---------|
```

### Hub Template

```markdown
# Work Tracker - {PROJECT_ID}

**Last Updated**: {TIMESTAMP}
**Project ID**: {PROJECT_ID}

---

## Navigation Graph

{ASCII diagram of hub-and-spoke structure}

---

## Quick Status Dashboard

| Phase | File | Status | Progress |
|-------|------|--------|----------|

---

## Current Focus

**Active Phase**: Phase {X}
**Active Task**: {TASK-ID}
**Next Steps**: {Brief description}

---

## Session Resume Protocol

When resuming work on this project:

1. Check **Current Focus** (above) for active task
2. Navigate to the **Phase File** for detailed breakdown
3. Read **Session Context** section in phase file
4. Check **Dependencies** before starting work
5. Update this file's timestamp after each session
```

---

## Integration

### With Work Tracker Skill

The decomposition skill integrates with the main Work Tracker skill:

```
@worktracker create "New task" --phase 4    # Creates task in PHASE-04 file
@worktracker list --phase 4                 # Lists tasks from PHASE-04 file
```

### With Git

All decomposition operations create atomic commits:

```
docs({project}): restructure WORKTRACKER to multi-file graph format

Restructured work tracking for multi-session and parallel work:
- WORKTRACKER.md is now an index with navigation graph
- Created work/ directory with per-phase files
- Added session context for compaction survival

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

---

## References

- **Runbook**: `projects/PROJ-001-plugin-cleanup/runbooks/RUNBOOK-002-worktracker-decomposition.md`
- **Purpose Catalog**: `projects/PROJ-001-plugin-cleanup/work/PURPOSE-CATALOG.md`
- **Synthesis**: `projects/PROJ-001-plugin-cleanup/synthesis/DOC-001-synthesis.md`
- **Pattern Origin**: Commit `4882948` in PROJ-001-plugin-cleanup

---

## Best Practices

1. **Analyze before decomposing** - Ensure the file truly needs decomposition
2. **Create backup commits** - Always have a rollback point
3. **Use dry-run first** - Preview changes before executing
4. **Validate after decomposition** - Ensure all links work
5. **Add session context to active phases** - Enable context recovery
6. **Keep hub under 150 lines** - Maintain the purpose of the pattern
7. **Progressive detail** - Active work gets maximum detail, completed stays minimal
