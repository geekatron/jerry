# RUNBOOK-002: WORKTRACKER Decomposition

> **ID**: RUNBOOK-002
> **Version**: 1.0
> **Created**: 2026-01-11
> **Author**: Claude Opus 4.5
> **Source**: DOC-001-synthesis
> **Validated**: Pending

---

## Purpose

This runbook provides step-by-step instructions for decomposing a monolithic WORKTRACKER.md file into a multi-file hub-and-spoke architecture. The pattern addresses **Context Rot** - the phenomenon where LLM performance degrades as context windows fill.

---

## When to Use This Runbook

### Trigger Criteria

| Trigger | Threshold | Action |
|---------|-----------|--------|
| **Soft Trigger** | WORKTRACKER.md > 500 lines | Consider decomposition |
| **Hard Trigger** | WORKTRACKER.md > 800 lines | Decomposition required |
| **Pain Indicator** | Difficulty finding active work | Decomposition recommended |
| **Compaction Failure** | Lost state after context compaction | Decomposition urgent |

### Pre-Conditions

Before starting, verify:

- [ ] File exceeds size threshold (>500 soft, >800 hard)
- [ ] At least 3 distinct phases or categories exist
- [ ] Some phases are completed (can be archived minimally)
- [ ] Active work is clearly identified

---

## Pre-Flight Checklist

Before decomposition:

- [ ] Backup current WORKTRACKER.md (git commit)
- [ ] Identify all phase boundaries
- [ ] Identify cross-cutting categories (BUGS, TECHDEBT, DISCOVERY)
- [ ] Confirm active work phase(s)
- [ ] Note current line counts per section
- [ ] Ensure clean git working directory

```bash
# Verify clean state
git status

# Create backup commit
git add WORKTRACKER.md
git commit -m "docs: backup WORKTRACKER.md before decomposition"
```

---

## Execution Steps

### Step 1: Analyze Existing Structure

**Input**: Monolithic WORKTRACKER.md
**Output**: List of phases, categories, and their boundaries

```bash
# Count total lines
wc -l WORKTRACKER.md

# Find phase headers
grep -n "^## Phase" WORKTRACKER.md

# Find category sections
grep -n "^## Bug\|^## Tech Debt\|^## Discovery" WORKTRACKER.md
```

Document findings:

| Section | Start Line | End Line | Status | Lines |
|---------|------------|----------|--------|-------|
| Phase 1 | | | | |
| Phase 2 | | | | |
| ... | | | | |
| Bugs | | | | |
| Tech Debt | | | | |

### Step 2: Create work/ Directory

```bash
mkdir -p {project_path}/work/
```

### Step 3: Create Phase Files (Sequential)

For each numbered phase, create a file using this template:

**Filename**: `work/PHASE-{NN}-{NAME}.md`

```markdown
# Phase N: {Title}

> **Status**: {STATUS_EMOJI} {STATUS} ({PERCENT}%)
> **Goal**: {One-line goal description}

---

## Navigation

| Link | Description |
|------|-------------|
| [<- WORKTRACKER](../WORKTRACKER.md) | Back to index |
| [<- Phase N-1](PHASE-{N-1}-{NAME}.md) | Previous phase |
| [Phase N+1 ->](PHASE-{N+1}-{NAME}.md) | Next phase |

---

## Task Summary

| Task ID | Title | Status | Subtasks | Output |
|---------|-------|--------|----------|--------|

---

## {TASK-ID}: {Task Title} {STATUS_EMOJI}

{Migrate full task details from monolithic file}

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
| {TODAY} | {AGENT} | Initial decomposition from WORKTRACKER.md |
```

### Step 4: Create Category Files (Cross-Cutting)

For BUGS, TECHDEBT, DISCOVERY, create files using this template:

**Filename**: `work/PHASE-{CATEGORY}.md`

```markdown
# Phase {CATEGORY}: {Title}

> **Status**: {STATUS}
> **Purpose**: Track {category} discovered during project development

---

## {Category} Summary

| ID | Title | Severity/Priority | Status | Phase Found |
|----|-------|-------------------|--------|-------------|

---

## {ID}: {Title} {STATUS_EMOJI}

> **Status**: {STATUS}
> **Priority**: {PRIORITY}
> **Source**: {Where discovered}

### Description
{What is the issue?}

### Impact
{What happens if not addressed?}

### Resolution
{How to fix?}

---

## Template

### {CATEGORY}-{NNN}: {Title}

> **Status**: TODO
> **Priority**: {HIGH|MEDIUM|LOW}
> **Source**: Phase {N}

### Description
{Description}

### Impact
{Impact}

### Resolution
{Resolution steps}
```

### Step 5: Transform WORKTRACKER.md into Navigation Hub

Replace detailed content with navigation-only structure:

```markdown
# Work Tracker - {PROJECT_ID}

**Last Updated**: {TIMESTAMP}
**Project ID**: {PROJECT_ID}

---

## Navigation Graph

```
              +-------------------------------------+
              |           WORKTRACKER.md            |
              |              (INDEX)                |
              +-----------------+-------------------+
                                |
      +-----------------+-------+-------+
      |                 |               |
      v                 v               v
COMPLETED         IN PROGRESS      SUPPORT
Phases 1-N        Phase X          BUGS, TECHDEBT
```

---

## Quick Status Dashboard

| Phase | File | Status | Progress |
|-------|------|--------|----------|
| 1 | [PHASE-01-{NAME}](work/PHASE-01-{NAME}.md) | DONE | 100% |
| ... | ... | ... | ... |
| BUGS | [PHASE-BUGS](work/PHASE-BUGS.md) | {STATUS} | - |
| TD | [PHASE-TECHDEBT](work/PHASE-TECHDEBT.md) | {STATUS} | - |

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

---

## Enforced Principles

1. Update WORKTRACKER.md timestamp after each work session
2. Mark tasks complete only with evidence
3. Capture bugs, tech debt, discoveries immediately
4. Test before marking implementation complete

---

## Document History

| Date | Author | Changes |
|------|--------|---------|
| {TODAY} | {AGENT} | Restructured to multi-file hub-and-spoke format |
```

**Target**: < 150 lines

### Step 6: Update Cross-References

- [ ] Verify all navigation links work
- [ ] Update any external references to point to new locations
- [ ] Add "Session Context" sections to active phase files
- [ ] Test navigation from hub to all spokes and back

```bash
# Find broken links (requires markdown link checker)
find work/ -name "*.md" -exec grep -l "\[.*\](.*\.md)" {} \;
```

### Step 7: Commit Atomically

```bash
git add WORKTRACKER.md work/
git commit -m "$(cat <<'EOF'
docs({project}): restructure WORKTRACKER to multi-file graph format

Restructured work tracking for multi-session and parallel work:

- WORKTRACKER.md is now an index with navigation graph
- Created work/ directory with per-phase files
- {Active phase} has detailed breakdown for active tasks
- Added subtask IDs with dependencies
- Added session context for compaction survival

Structure:
  work/PHASE-01-{NAME}.md ({status})
  work/PHASE-02-{NAME}.md ({status})
  ...
  work/PHASE-BUGS.md ({status})
  work/PHASE-TECHDEBT.md ({status})

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
)"
```

---

## Validation Criteria

After decomposition, verify:

- [ ] WORKTRACKER.md < 150 lines
- [ ] All navigation links work (hub → spoke, spoke → hub, spoke → spoke)
- [ ] Session Context sections present in all active files
- [ ] Quick Status Dashboard complete and accurate
- [ ] Git commit has proper message format
- [ ] No content lost during decomposition

```bash
# Verify hub size
wc -l WORKTRACKER.md  # Should be < 150

# Verify all files created
ls -la work/

# Test a navigation link
head -50 work/PHASE-01-*.md | grep WORKTRACKER
```

---

## Post-Decomposition Maintenance

### When to Update Phase Files

- Add new tasks to the relevant phase file
- Update task status in both phase file AND WORKTRACKER.md dashboard
- Expand active work with subtasks, tests, acceptance criteria

### When to Archive Phase Content

- When a phase completes, reduce detail to summaries
- Move detailed implementation notes to `/reports/` or `/synthesis/`
- Keep enough context for future reference

### When to Re-Decompose

- If a phase file exceeds 1,000 lines
- If a new cross-cutting category emerges
- If parallel work creates merge conflicts

---

## Rollback Procedure

If decomposition fails or causes issues:

```bash
# Option 1: Git revert (if committed)
git revert HEAD

# Option 2: Restore from backup commit
git checkout HEAD~1 -- WORKTRACKER.md
rm -rf work/
git add .
git commit -m "revert: restore monolithic WORKTRACKER.md"
```

### Rollback Decision Criteria

- Navigation links broken beyond quick fix
- Critical content lost during decomposition
- Structure doesn't match project's actual workflow

---

## References

- **Source Synthesis**: `projects/PROJ-001-plugin-cleanup/synthesis/DOC-001-synthesis.md`
- **Pattern Origin**: Commit `4882948` in PROJ-001
- **Research Artifacts**: DOC-001-R1, DOC-001-R2, DOC-001-R3
- **Related**: RUNBOOK-001 (Domain Refactoring)

---

## Document History

| Date | Version | Author | Changes |
|------|---------|--------|---------|
| 2026-01-11 | 1.0 | Claude Opus 4.5 | Initial runbook created from DOC-001 synthesis |
