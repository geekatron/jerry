---
name: work-tracker
description: Generate and track work items with phases, tasks, sub-tasks, and verification criteria. Use when starting new work, tracking progress, reviewing remaining work, or syncing work state across sessions. Integrates with ECW workflow for full traceability. (user)
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(python scripts/:*), TodoWrite
version: "2.0.0"
activation-keywords:
  - "track"
  - "track work"
  - "work items"
  - "task list"
  - "project status"
  - "where were we"
  - "what's remaining"
  - "resume"
  - "continue work"
  - "show my work"
  - "list work"
  - "what's done"
  - "mark complete"
  - "update progress"
  - "new project"
  - "start project"
---

# Work Tracker Skill

> **Template Version:** 2.0.0
> **ECW Compatible:** v2.1.0+
> **Persistence:** File-based (works in both local and web Claude Code)

## Purpose

Generate structured work tracking that survives session compaction and enables full progress tracking with:

- **Phases:** High-level milestones
- **Tasks:** Actionable work items within phases
- **Sub-tasks:** Granular steps within tasks
- **Verification Criteria:** How to confirm completion

## When to Use This Skill

Activate when:

- Starting a new project or feature
- Tracking work items ("track this work", "create a project")
- Tracking progress ("what's remaining", "show status", "update progress")
- Reviewing work state ("where are we", "what's done")
- Resuming after session break (recovery verification)
- Syncing state for cross-session continuity
- User says "show my work" or selects a work item by number/name

## Session Integration Flow

At session start, the SessionStart hook:

1. Calls `detect_work_state.py --write-state` to analyze all work items
2. Writes state to `.ecw/work-state.json`
3. Displays work context in session output

When this skill activates, it should:

### 1. Read Work State

```bash
cat .ecw/work-state.json
```

Or use the script directly:

```bash
python .claude/skills/work-tracker/scripts/detect_work_state.py --format json
```

### 2. Handle Based on State

**State: `none`** (No work items exist)

- Suggest: "No work items found. Want to create one? Say 'new project' or describe your work."
- If user provides context, generate work tracker using `generate_tracker.py`

**State: `single_active`** (One active work item)

- Display: "Active work: {title} at {progress}%"
- Display: "Current task: {task_id} - {task_desc}"
- Ask: "Resume this work, or start something new?"
- If resume: Load work to TodoWrite, show progress summary
- If new: Proceed to new work flow

**State: `multiple`** (Multiple work items)

- Display numbered list of all work items with status and progress
- Ask: "Which work item to focus on? (1/2/3 or 'new' for fresh start)"
- Accept number or name as selection
- Load selected work to TodoWrite

**State: `error`** (Detection failed)

- Display: "Unable to auto-detect work state."
- Offer: "1. New Project, 2. Load from file, 3. Repair"

### 3. Sync to TodoWrite

When loading work, sync current phase tasks to TodoWrite:

```bash
python .claude/skills/work-tracker/scripts/load_from_file.py \
  --work docs/plans/*.md \
  --to-todowrite
```

## Environment Compatibility

| Feature                   | Local CLI          | Web (Research Preview) |
| ------------------------- | ------------------ | ---------------------- |
| Work generation           | ✅                 | ✅                     |
| Status updates            | ✅                 | ✅                     |
| File sync (`.ecw/plans/`) | ✅                 | ✅                     |
| Progress tracking         | ✅                 | ✅                     |
| SessionStart integration  | ✅                 | ✅                     |
| MCP Memory Keeper         | ✅ (if configured) | ❌ (not available)     |

**Detection:** Use `$CLAUDE_CODE_REMOTE` to detect environment (see `docs/guides/claude-code-capabilities.md`)

## Command Framework (Initiative 12 CQRS)

The work-tracker skill now includes a complete CQRS command framework with 21 command classes and natural language interface.

### Working Directory & Invocation

**CRITICAL:** The wt.py script must be invoked correctly to avoid path resolution errors.

#### Recommended: Invoke from Project Root

Always invoke wt.py from the **project root** using the full relative path:

```bash
# From project root (recommended)
cd /path/to/ecw-skills
python3 .claude/skills/work-tracker/scripts/wt.py --tracker docs/plans/project.md "mark task 1.1 complete"
```

#### Alternative: Invoke from Skill Directory

If running from the skill directory, use `scripts/` prefix:

```bash
# From skill directory
cd /path/to/ecw-skills/.claude/skills/work-tracker
python3 scripts/wt.py --tracker ../../../docs/plans/project.md "mark task 1.1 complete"
```

**Note:** Tracker paths must be relative to your current working directory, NOT the script location.

#### Path Resolution Rules

| Working Directory | wt.py Path | Tracker Path |
|-------------------|------------|--------------|
| Project root | `.claude/skills/work-tracker/scripts/wt.py` | `docs/plans/project.md` |
| Skill root (`.claude/skills/work-tracker/`) | `scripts/wt.py` | `../../../docs/plans/project.md` |
| Any directory | Full absolute path | Absolute or relative to CWD |

#### Common Errors & Troubleshooting

**Error:** `FileNotFoundError: docs/plans/project.md not found`
- **Cause:** Running from skill directory but using project-root-relative path
- **Fix:** Either `cd` to project root OR use relative path from current directory

**Error:** `ModuleNotFoundError: No module named 'commands'`
- **Cause:** Python can't find the commands package
- **Fix:** Run from skill directory OR ensure PYTHONPATH includes skill root

**Error:** `JSON file not found: .ecw/plans/project.json`
- **Cause:** JSON SSOT not initialized or path resolution issue
- **Fix:** Run `python3 scripts/sync_to_file.py --plan <tracker_path>` first

**Error:** `Invalid task ID format`
- **Cause:** Task ID doesn't match X.Y pattern (e.g., using "1" instead of "1.1")
- **Fix:** Use full task ID like "1.1", "2.3", etc.

#### Diagnosing Path Issues

If you encounter path errors, use this checklist:

```bash
# 1. Check your current working directory
pwd

# 2. Verify the tracker file exists from your location
ls -la docs/plans/project.md  # For project root
ls -la ../../../docs/plans/project.md  # For skill directory

# 3. Check if JSON SSOT exists
ls -la .ecw/plans/  # For project root
ls -la ../../../.ecw/plans/  # For skill directory

# 4. Verify Python can find modules
python3 -c "import sys; print('\n'.join(sys.path))"

# 5. Test with absolute paths (always works)
python3 /full/path/to/scripts/wt.py --tracker /full/path/to/tracker.md "show progress"
```

#### Quick Debugging Reference

| Symptom | Most Likely Cause | Quick Fix |
|---------|-------------------|-----------|
| "file not found" | Wrong working directory | `cd` to project root |
| "module not found" | Python path issue | Run from skill directory |
| "JSON not found" | SSOT not synced | Run sync_to_file.py |
| Command works but no changes | Using wrong tracker | Check --tracker path |

#### CLAUDE.md Integration

The CLAUDE.md file specifies wt.py usage (SOP-WT.0). All examples in CLAUDE.md assume **project root** as working directory:

```bash
# CLAUDE.md examples (from project root)
python3 .claude/skills/work-tracker/scripts/wt.py --tracker docs/plans/wt-skill-dev/19-sop-remediation.md "mark task 5.3 complete"
```

### Natural Language Interface (wt.py)

```bash
# Phase operations
python scripts/wt.py "add phase 9 called Integration Testing"
python scripts/wt.py "update phase 3 to complete"
python scripts/wt.py "delete phase 7"
python scripts/wt.py "reorder phases"

# Task operations
python scripts/wt.py "add task to phase 9 called Create BDD tests"
python scripts/wt.py "mark task 5.3 complete"
python scripts/wt.py "update task 2.1 status in_progress"
python scripts/wt.py "move task 5.3 to phase 6"
python scripts/wt.py "delete task 4.2"

# Subtask operations
python scripts/wt.py "add subtask to task 9.1 called Test hooks"
python scripts/wt.py "check subtask 1.1.4"
python scripts/wt.py "complete subtask 3.2.5"
python scripts/wt.py "delete subtask 2.3.1"

# Evidence operations
python scripts/wt.py "attach evidence to task 2.3"
python scripts/wt.py "verify evidence for task 1.1"

# Progress and display
python scripts/wt.py "show progress"
python scripts/wt.py "what's remaining"

# Markdown generation
python scripts/wt.py "regenerate markdown"
python scripts/wt.py "regenerate enhanced"
```

### Available Commands (21 Classes)

#### Phase Commands
- **AddPhaseCommand** - Add new phase with title, target date
- **UpdatePhaseCommand** - Update phase status/properties
- **DeletePhaseCommand** - Remove phase and its tasks
- **ReorderPhasesCommand** - Change phase sequence

#### Task Commands
- **AddTaskCommand** - Add task to specific phase
- **UpdateTaskCommand** - Update task status/verification
- **DeleteTaskCommand** - Remove task from phase
- **MoveTaskCommand** - Move task between phases

#### Subtask Commands
- **AddSubtaskCommand** - Add subtask to task
- **UpdateSubtaskCommand** - Check/uncheck subtasks
- **DeleteSubtaskCommand** - Remove subtask
- **BulkSubtaskCommand** - Bulk check/uncheck operations

#### Work Tracker Commands
- **UpdateWorkTrackerCommand** - Recalculate all progress
- **AttachEvidenceCommand** - Add evidence to tasks/subtasks
- **VerifyEvidenceCommand** - Mark evidence as verified

#### Initiative Commands
- **CreateInitiativeCommand** - Start new initiative
- **UpdateInitiativeMetadataCommand** - Update metadata
- **SetInitiativeProgressCommand** - Set overall progress
- **LinkPlanCommand** - Link plans together

#### Markdown Generation
- **FullFidelityMarkdownGenerator** - Lossless round-trip markdown (recommended)
- ~~EnhancedMarkdownGenerator~~ - DEPRECATED (loses data)
- ~~MarkdownGenerator~~ - DEPRECATED (loses data)

### Command Execution Flow

```
User Input → Natural Language → Dispatcher → Command → ScriptBridge → Scripts → Fingerprint
```

This ensures:
- ✅ Skill fingerprints maintained (wt-v2.0.0-*)
- ✅ Sync logs show skill attribution
- ✅ JSON properly synced to `.claude/docs/.ecw/plans/`
- ✅ Main branch compatibility preserved

## Quick Workflow

> **D-040 IMPORTANT:** All operations MUST use `wt.py`. See [CLI Reference](docs/cli-reference.md) for all 27 commands.

### 1. Create New Work Tracker

```bash
# Use generate_tracker.py for new trackers
python scripts/generate_tracker.py \
  --title "Authentication" \
  --output docs/plans/authentication.md
```

### 2. Build Tracker Structure

```bash
# Use wt.py for ALL operations (D-040)
TRACKER="docs/plans/authentication.md"

# Add phases
python scripts/wt.py --tracker $TRACKER "add phase Implementation"
python scripts/wt.py --tracker $TRACKER "add phase Testing"

# Add tasks to phases
python scripts/wt.py --tracker $TRACKER "add task to phase 1: Write unit tests"
python scripts/wt.py --tracker $TRACKER "add task to phase 1: Implement auth module"

# Add subtasks
python scripts/wt.py --tracker $TRACKER "add subtask to task 1.1: Test login function"
python scripts/wt.py --tracker $TRACKER "add subtask to task 1.1: Test logout function"
```

### 3. Track Progress

```bash
# Mark tasks in progress
python scripts/wt.py --tracker $TRACKER "mark task 1.1 in progress"

# Check subtasks as you complete them
python scripts/wt.py --tracker $TRACKER "check subtask 1.1.1"
python scripts/wt.py --tracker $TRACKER "check subtask 1.1.2"

# Mark tasks complete
python scripts/wt.py --tracker $TRACKER "mark task 1.1 complete"

# View progress
python scripts/wt.py --tracker $TRACKER "show progress"
```

### 4. Manage Evidence (D-040 - Use wt.py!)

```bash
# Attach evidence (command output)
python scripts/wt.py --tracker $TRACKER \
  'attach evidence to task 1.1: command_output "pytest tests/ - 25 passed"'

# Attach evidence (file reference)
python scripts/wt.py --tracker $TRACKER \
  'attach evidence to task 1.2: file_reference "docs/screenshots/feature.png"'

# Attach evidence (manual note)
python scripts/wt.py --tracker $TRACKER \
  'attach evidence to task 1.3: manual_note "Manually verified login flow"'
```

### Documentation Links

| Document | Purpose |
|----------|---------|
| [CLI Reference](docs/cli-reference.md) | All 27 commands with examples |
| [Architecture](docs/architecture.md) | Hexagonal layers, JSON SSOT |
| [Migration API](docs/migration-tools-api.md) | Schema migration functions |
| [Playbooks](docs/playbooks-runbooks.md) | Migration guides, troubleshooting |

### 5. Session Management

```bash
# Sync to JSON for persistence
python scripts/sync_to_file.py \
  --work docs/plans/project.md

# Load work state at session start
python scripts/load_from_file.py \
  --all --format sessionstart

# Verify integrity
python scripts/verify_recovery.py \
  --work docs/plans/project.md
```

### 6. Export and Report

```bash
# Export to proposal format
python scripts/export_work.py \
  --work docs/plans/project.md \
  --to-proposal docs/proposals/

# Generate enhanced documentation
python scripts/wt.py "regenerate enhanced"
```

## Persistence Architecture

### Universal (Works Everywhere)

```
┌─────────────────────────────────────────────────────┐
│                 FILE-BASED PERSISTENCE               │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌─────────────────────┐    ┌─────────────────────┐ │
│  │  docs/plans/*.md     │    │  .ecw/plans/*.json   │ │
│  │  (Primary/Human)    │    │  (Secondary/Fast)   │ │
│  │  Git-tracked        │    │  Machine-readable   │ │
│  └──────────┬──────────┘    └──────────┬──────────┘ │
│             │                          │            │
│             └──────────┬───────────────┘            │
│                        │                            │
│             ┌──────────▼──────────┐                 │
│             │   sync_to_file.py   │                 │
│             │   load_from_file.py │                 │
│             └─────────────────────┘                 │
│                                                      │
│  ✅ Works in Local CLI                               │
│  ✅ Works in Web (Research Preview)                  │
│  ✅ Works in Hooks (subprocess context)              │
│                                                      │
└─────────────────────────────────────────────────────┘
```

### Local-Only Enhancement (Optional)

```
┌─────────────────────────────────────────────────────┐
│           MCP MEMORY KEEPER (LOCAL ONLY)             │
├─────────────────────────────────────────────────────┤
│                                                      │
│  If $CLAUDE_CODE_REMOTE != "true" AND MCP configured:│
│                                                      │
│  ┌─────────────────────────────────────────────────┐│
│  │  work:{id}:meta     → Work metadata             ││
│  │  work:{id}:phase:{n} → Phase status             ││
│  │  work:{id}:task:{n.m} → Task details            ││
│  │  work:{id}:progress  → Progress summary         ││
│  └─────────────────────────────────────────────────┘│
│                                                      │
│  ❌ NOT available in Web (Research Preview)          │
│  ❌ NOT available in Hooks (subprocess isolation)    │
│                                                      │
└─────────────────────────────────────────────────────┘
```

## Sync Protocol

### Primary (File-Based - Always Used)

```python
# On work creation/update
1. Write markdown to docs/plans/*.md
2. Parse work structure
3. Write JSON to .ecw/plans/*.json (sync_to_file.py)
4. Update TodoWrite for active tasks

# On session resume
1. SessionStart calls load_from_file.py
2. Display active work with progress
3. Show current task context
```

### Secondary (MCP - Local CLI Only)

```python
# Only if $CLAUDE_CODE_REMOTE != "true"
# AND Memory Keeper MCP is configured

# On sync request
1. Check environment: if remote, skip MCP
2. Store structured data in Memory Keeper
3. Keys: work:{id}:meta, work:{id}:phase:*, etc.
```

## Recovery Verification

```bash
python .claude/skills/work-tracker/scripts/verify_recovery.py \
  --work docs/plans/project-name.md
```

**What it verifies:**

1. Work file exists on disk
2. Checksum is valid (content integrity)
3. Progress summary matches task statuses
4. JSON sync file exists and matches

**On mismatch:**

- Disk is source of truth
- JSON is regenerated from disk
- Issue is reported

## Work Structure (ECW Full v2.0.0)

```markdown
# Work Tracker: {Title}

> **Version:** 2.0.0
> **Template:** ECW Full v2.0.0
> **Status:** Active | Complete | On Hold
> **Created:** YYYY-MM-DD
> **Updated:** YYYY-MM-DD
> **Session:** {session-id}
> **Work ID:** {slug}-{date}

---

## Overview

{Brief description of the project goal}

---

## Phases

### Phase 1: {Phase Name}

> **Status:** Pending | In Progress | Complete

#### Tasks

| ID  | Task | Status  | Verification |
| --- | ---- | ------- | ------------ |
| 1.1 | ...  | Pending | ...          |

#### Sub-tasks

- [ ] 1.1.1: ...

---

## Progress Summary

| Phase | Tasks | Done | Remaining | % Complete |
| ----- | ----- | ---- | --------- | ---------- |

---

## Recovery Checksum
```

{16-char-hex-checksum}

```

## Status Indicators

| Status      | Meaning               | Icon |
| ----------- | --------------------- | ---- |
| Pending     | Not started           | ⏳   |
| In Progress | Currently working     | 🔄   |
| Blocked     | Waiting on dependency | 🔴   |
| Complete    | Verified done         | ✅   |
| Deferred    | Postponed             | ⏸️   |

## Hierarchical Status Taxonomy

Work Tracker v2.0.0+ implements a **hierarchical status taxonomy** that provides granular progress tracking through workflow zones.

### Status Format

Statuses follow the format: `Zone.Phase.Step` or `Zone.Status`

Examples:
- `Discovery.Created` - Simple zone status
- `Development.Work.SliceStarted` - Full hierarchical (Zone.Phase.Step)
- `Review.Code.Approved` - Multi-level hierarchy

### Status Zones (6 Lifecycle Zones)

Work items progress through these zones in sequence:

```
Discovery → Design → Development → Review → Consent → Terminal
```

| Zone | Purpose | Entry Status | Exit Status |
|------|---------|--------------|-------------|
| **Discovery** | Problem exploration, requirements gathering | `Discovery.Created` | `Discovery.ReadyForDesign` |
| **Design** | Domain modeling, architecture decisions | `Design.Domain.Modeling` | `Design.ReadyForDevelopment` |
| **Development** | Implementation (Work→Right→Fast) | `Development.Work.SliceStarted` | `Development.ReadyForReview` |
| **Review** | Code, design, evidence validation | `Review.Code.Requested` | `Review.AllApproved` |
| **Consent** | User approval workflow (SOP-WT.2) | `Consent.Awaiting` | `Consent.Granted` |
| **Terminal** | Final states (completed/cancelled) | Any terminal status | N/A |

### Zone-Specific Status Enums

#### Discovery Zone (`DiscoveryStatus`)

| Status | Value | Purpose |
|--------|-------|---------|
| CREATED | `Discovery.Created` | Initial state |
| EXPLORING | `Discovery.Exploring` | Active exploration |
| REQUIREMENTS_GATHERING | `Discovery.Requirements.Gathering` | Collecting requirements |
| REQUIREMENTS_CLARIFYING | `Discovery.Requirements.Clarifying` | Refining requirements |
| USECASE_ANALYZING | `Discovery.UseCase.Analyzing` | Analyzing use cases |
| USECASE_SLICING | `Discovery.UseCase.Slicing` | Breaking into slices |
| READY_FOR_DESIGN | `Discovery.ReadyForDesign` | Zone exit status |

#### Design Zone (`DesignStatus`)

| Status | Value | Purpose |
|--------|-------|---------|
| DOMAIN_MODELING | `Design.Domain.Modeling` | Creating domain model |
| DOMAIN_COMPLETED | `Design.Domain.Completed` | Domain model done |
| ARCHITECTURE_DRAFTING | `Design.Architecture.Drafting` | Architecture design |
| ARCHITECTURE_VALIDATED | `Design.Architecture.Validated` | Architecture approved |
| CONTRACTS_DEFINING | `Design.Contracts.Defining` | API/Interface contracts |
| CONTRACTS_AGREED | `Design.Contracts.Agreed` | Contracts finalized |
| READY_FOR_DEVELOPMENT | `Design.ReadyForDevelopment` | Zone exit status |

#### Development Zone (`DevelopmentStatus`) - Kent Beck Phases

Development follows Kent Beck's "Make it Work → Make it Right → Make it Fast":

**Make it Work (Work Phase)**
| Status | Value | Purpose |
|--------|-------|---------|
| WORK_SLICE_STARTED | `Development.Work.SliceStarted` | Started implementation |
| WORK_IMPLEMENTING | `Development.Work.Implementing` | Writing code |
| WORK_INTEGRATING | `Development.Work.Integrating` | Integration work |
| WORK_SLICE_WORKS | `Development.Work.SliceWorks` | Basic functionality works |

**Make it Right (Right Phase)**
| Status | Value | Purpose |
|--------|-------|---------|
| RIGHT_REFACTORING | `Development.Right.Refactoring` | Code cleanup |
| RIGHT_EDGE_CASES | `Development.Right.EdgeCases` | Handling edge cases |
| RIGHT_TEST_HARDENING | `Development.Right.TestHardening` | Improving test coverage |
| RIGHT_SLICE_CLEAN | `Development.Right.SliceClean` | Code is clean |

**Make it Fast (Fast Phase)**
| Status | Value | Purpose |
|--------|-------|---------|
| FAST_PROFILING | `Development.Fast.Profiling` | Performance profiling |
| FAST_OPTIMIZING | `Development.Fast.Optimizing` | Optimization work |
| FAST_LOAD_TESTING | `Development.Fast.LoadTesting` | Load testing |
| FAST_SLICE_OPTIMIZED | `Development.Fast.SliceOptimized` | Performance acceptable |

**Exit Status**
| Status | Value | Purpose |
|--------|-------|---------|
| READY_FOR_REVIEW | `Development.ReadyForReview` | Zone exit status |

#### Review Zone (`ReviewStatus`)

| Category | Statuses |
|----------|----------|
| **Code Review** | `Review.Code.Requested`, `Review.Code.InReview`, `Review.Code.ChangesRequested`, `Review.Code.Approved` |
| **Design Review** | `Review.Design.Requested`, `Review.Design.InReview`, `Review.Design.ChangesRequested`, `Review.Design.Approved` |
| **Evidence Review** | `Review.Evidence.Requested`, `Review.Evidence.InReview`, `Review.Evidence.ChangesRequested`, `Review.Evidence.Approved` |
| **Security Review** | `Review.Security.Requested`, `Review.Security.InReview`, `Review.Security.ChangesRequested`, `Review.Security.Approved` |
| **Exit** | `Review.AllApproved` |

#### Consent Zone (`ConsentStatus`)

| Status | Value | Purpose |
|--------|-------|---------|
| AWAITING_CONSENT | `Consent.Awaiting` | Waiting for user approval |
| CONSENT_GRANTED | `Consent.Granted` | User approved (zone exit) |
| CONSENT_DENIED | `Consent.Denied` | User rejected |

#### Terminal Zone (`TerminalStatus`)

| Status | Value | Purpose |
|--------|-------|---------|
| COMPLETE | `Terminal.Complete` | Successfully completed |
| MERGED | `Terminal.Merged` | Code merged to main |
| SUPERSEDED | `Terminal.Superseded` | Replaced by another work item |
| CANCELLED | `Terminal.Cancelled` | Work cancelled |
| REJECTED | `Terminal.Rejected` | Work rejected |
| ARCHIVED | `Terminal.Archived` | Archived for reference |

### Cross-Zone Statuses

These statuses can apply regardless of current zone:

#### Deferred Status (`DeferredStatus`)

| Status | Value | Resumable | Priority |
|--------|-------|-----------|----------|
| NEXT_SPRINT | `Deferred.NextSprint` | Yes | High |
| NEXT_PHASE | `Deferred.NextPhase` | Yes | Medium |
| BACKLOG | `Deferred.Backlog` | Yes | Low |
| INDEFINITELY | `Deferred.Indefinitely` | No (explicit) | None |

#### Blocking Status (`BlockingStatus`)

| Status | Value | Description |
|--------|-------|-------------|
| TECHNICAL_ISSUE | `Blocked.TechnicalIssue` | Technical blocker |
| WAITING_DEPENDENCY | `Blocked.WaitingDependency` | Waiting on another work item |
| WAITING_RESOURCE | `Blocked.WaitingResource` | Resource unavailable |
| WAITING_APPROVAL | `Blocked.WaitingApproval` | Waiting for approval |
| WAITING_CLARIFICATION | `Blocked.WaitingClarification` | Need more information |
| WAITING_EXTERNAL | `Blocked.WaitingExternal` | External dependency |

### Backtrack Triggers

When work needs to return to an earlier zone, a **backtrack trigger** must be specified:

#### Discovery Backtrack Triggers
- `SCOPE_CREEP` - Requirements expanded beyond original
- `WRONG_PROBLEM` - Solving wrong problem
- `STAKEHOLDER_CHANGE` - Stakeholder requirements changed
- `REQUIREMENTS_UNCLEAR` - Requirements need clarification
- `MARKET_SHIFT` - Market conditions changed

#### Design Backtrack Triggers
- `ENTITY_MISSING` - Domain model incomplete
- `RELATIONSHIP_WRONG` - Incorrect entity relationships
- `CONTRACT_INVALID` - API contract doesn't work
- `ARCHITECTURE_FLAW` - Architecture issue discovered
- `PERFORMANCE_CONSTRAINT` - Can't meet performance with current design

#### Development Backtrack Triggers
- `NEEDS_MORE_WORK` - Implementation incomplete
- `ALGORITHM_CHOICE_WRONG` - Wrong algorithm selected
- `MISSING_TESTS` - Test coverage insufficient
- `INTEGRATION_FAILED` - Integration issues

### Status Transitions

**Forward Transitions (Normal Flow)**
```
Discovery → Design → Development → Review → Consent → Terminal
```

**Backtrack Transitions (Require Trigger)**
```
Development → Design (trigger: ENTITY_MISSING)
Development → Discovery (trigger: SCOPE_CREEP)
Review → Development (trigger: NEEDS_MORE_WORK)
```

**Cross-Zone Transitions**
```
Any Zone → Deferred (preserves previous zone)
Any Zone → Blocked (preserves previous zone)
Deferred → Previous Zone (resume)
Blocked → Previous Zone (unblock)
```

### Status History Tracking

Each status change is recorded with:
- `from_status` - Previous status
- `to_status` - New status
- `timestamp` - When change occurred
- `is_backtrack` - Boolean flag for backtracks
- `is_zone_change` - Boolean flag for zone transitions
- `reason` - Backtrack trigger (if applicable)

### Using Hierarchical Status

```bash
# Update task with hierarchical status
python scripts/wt.py --tracker docs/plans/project.md "update task 1.1 status to Development.Work.Implementing"

# Mark task for backtrack to Discovery
python scripts/wt.py --tracker docs/plans/project.md "update task 1.1 status to Discovery.Exploring"
# System will prompt for backtrack trigger

# Defer a task
python scripts/wt.py --tracker docs/plans/project.md "update task 1.1 status to Deferred.NextSprint"

# Block a task
python scripts/wt.py --tracker docs/plans/project.md "update task 1.1 status to Blocked.WaitingDependency"
```

## Evidence Tracking

Work Tracker supports **evidence tracking** to provide verifiable proof of task completion. Evidence can be recorded at **task-level** or **sub-task-level** based on work complexity.

### Evidence Levels

Evidence can be one of three levels:

| Level            | Description                                    | Use When                                |
| ---------------- | ---------------------------------------------- | --------------------------------------- |
| `command_output` | Shell command execution with output            | Tests passed, builds succeeded          |
| `file_reference` | Reference to artifact file                     | Screenshots, logs, generated files      |
| `manual_note`    | Human verification note                        | Manual testing, stakeholder approval    |

### Recording Evidence

Use `update_status.py` with evidence arguments when marking tasks complete:

**Command Output Evidence:**

```bash
python scripts/update_status.py \
  --plan docs/work/my-work.md \
  --task 1.1 \
  --status complete \
  --evidence-level command_output \
  --evidence-command "pytest tests/" \
  --evidence-output "===== 25 passed ====="
```

**File Reference Evidence:**

```bash
python scripts/update_status.py \
  --plan docs/work/my-work.md \
  --task 1.2 \
  --status complete \
  --evidence-level file_reference \
  --evidence-file "docs/screenshots/feature-complete.png"
```

**Manual Note Evidence:**

```bash
python scripts/update_status.py \
  --plan docs/work/my-work.md \
  --task 1.3 \
  --status complete \
  --evidence-level manual_note \
  --evidence-note "Feature reviewed and approved by product team"
```

### Enforcement Mode

Use `--enforce-evidence` to **require** evidence before marking tasks complete:

```bash
python scripts/update_status.py \
  --plan docs/work/my-work.md \
  --task 2.1 \
  --status complete \
  --enforce-evidence \
  --evidence-level command_output \
  --evidence-command "npm test" \
  --evidence-output "All tests passed"
```

Without evidence, the update will be **rejected**:

```
Error: Evidence enforcement failed - Task 2.1 requires at least 1 evidence entry
```

### Flexible Evidence

Evidence is **flexible** - you can choose the granularity:

- **Task-level only:** Evidence for overall task completion
- **Sub-task-level only:** Evidence for individual sub-tasks
- **Mixed:** Some tasks have task-level evidence, others have sub-task evidence
- **Combined:** Both task-level AND sub-task-level evidence for the same task

Example: Complex task with both levels

```
## Evidence

#### Task 1.1: Implement authentication

Evidence Entry (ID: abc123)
- Level: command_output
- Status: verified

Command: pytest tests/integration/
Output: ===== 50 integration tests passed =====

✅ VERIFIED: Integration tests passed for task 1.1

#### Task 1.1 / Sub-task 1.1.1: Unit tests

Evidence Entry (ID: def456)
- Level: file_reference
- Status: verified

File Reference: tests/unit/test_auth.py

✅ VERIFIED: Unit tests for authentication module
```

### Evidence Display

Evidence appears automatically in:

- **Progress reports:** `show_progress.py` shows evidence count per task
- **Work state:** `detect_work_state.py` includes evidence summary
- **SessionStart hook:** Shows evidence verification percentage

Example progress display:

```
PHASE 1: Implementation
Status: In Progress
Evidence: 5 entries, 80% verified

Tasks:
  ✅ 1.1: Authentication (2 evidence) ✅
  🔄 1.2: Authorization (1 evidence) ⏳
  ⏳ 1.3: Logging ○
```

Evidence indicators:
- ✅ = Has verified evidence
- ⏳ = Has pending (unverified) evidence
- ○ = No evidence yet

## Command Execution Patterns

### Natural Language Interface (wt.py)

The skill provides a natural language CLI for common operations:

```bash
# When user says "mark task 5.3 complete"
python scripts/wt.py "mark task 5.3 complete"

# When user says "add phase Testing"
python scripts/wt.py "add phase Testing"

# When user says "show progress"
python scripts/wt.py "show progress"

# When user says "update phase 2 to in progress"
python scripts/wt.py "update phase 2 to in progress"
```

### Direct Script Execution

For specific operations, use the appropriate scripts directly:

#### Status Updates
```bash
# Update task status
python scripts/update_status.py --plan {tracker} --task 1.2 --status complete

# Update phase status
python scripts/update_status.py --plan {tracker} --phase 2 --status "in_progress"

# Check off subtask
python scripts/update_status.py --plan {tracker} --subtask 1.2.3 --check
```

#### Progress and Display
```bash
# Show current progress
python scripts/show_progress.py --plan {tracker} --format compact

# Detect work state (for session start)
python scripts/detect_work_state.py

# Verify integrity
python scripts/verify_recovery.py --plan {tracker}
```

#### Tracker Management
```bash
# Generate new tracker
python scripts/generate_tracker.py --title "New Feature" --output {path}

# Sync markdown to JSON
python scripts/sync_to_file.py --plan {tracker}

# Load from file to TodoWrite
python scripts/load_from_file.py --plan {tracker}
```

### Command Routing

When the skill is activated via keywords:

1. **Parse intent from user message**
   - "mark X complete" → update_status command
   - "add phase Y" → phase management (future)
   - "show progress" → display command

2. **Execute appropriate command**
   ```bash
   # The skill determines which script to run based on intent
   if intent == "update_task":
       python scripts/wt.py "{user_message}"
   elif intent == "show_progress":
       python scripts/show_progress.py --plan {tracker}
   ```

3. **Capture and embed evidence**
   - Real command outputs are captured
   - Evidence is embedded in markdown
   - Fingerprints are maintained

### Important Notes

- **Always use scripts, never modify markdown directly**
- **The wt.py wrapper handles natural language → command translation**
- **Scripts maintain fingerprints and sync logs automatically**
- **Evidence is captured from actual command execution**

### Evidence Schema

Evidence entries in markdown follow this structure:

```markdown
**Evidence Entry (ID: {unique-id})** (YYYY-MM-DD HH:MM)
- **Level**: command_output | file_reference | manual_note
- **Status**: verified | pending

[Level-specific content]

✅ **VERIFIED**: Description
or
⏳ **PENDING**: Description
```

Evidence syncs to JSON with metadata:

```json
{
  "evidence": [
    {
      "id": "abc12345",
      "task_id": "1.1",
      "subtask_id": null,
      "timestamp": "2025-12-28T10:00:00",
      "level": "command_output",
      "verification_status": "verified",
      "command": "pytest tests/",
      "output": "===== 25 passed ====="
    }
  ]
}
```

### Best Practices

1. **Use command_output for automated verification:** Tests, builds, linters
2. **Use file_reference for artifacts:** Screenshots, logs, generated documentation
3. **Use manual_note sparingly:** Only when automated verification isn't possible
4. **Add evidence as you complete work:** Don't wait until the end
5. **Use --enforce-evidence for critical work:** Ensures nothing gets marked complete without proof
6. **Be specific in verification markers:** Explain what was verified and why

## Skill Fingerprinting

Work tracker artifacts include fingerprint headers for provenance tracking and migration support.

### Fingerprint Format

```

wt-v{version}-{8hex}

````

Example: `wt-v2.0.0-abc12345`

Components:
- `wt` - Work tracker prefix
- `v{version}` - Skill version (e.g., `v2.0.0`)
- `{8hex}` - 8-character hash of skill components (SKILL.md, scripts, templates)

### Artifact Headers

Work tracker artifacts include these provenance headers:

```markdown
> **Skill-Version:** 2.0.0
> **Skill-Fingerprint:** wt-v2.0.0-abc12345
````

### Drift Detection

Drift occurs when the skill version that created an artifact differs from the current skill version.

**Check for drift:**

```bash
python .claude/skills/work-tracker/scripts/verify_recovery.py \
  --work docs/plans/project.md \
  --check-drift
```

**Drift on status update:**

```bash
python .claude/skills/work-tracker/scripts/update_status.py \
  --work docs/plans/project.md \
  --task 1.1 \
  --status complete \
  --warn-drift
```

### Drift Types

| Type                | Meaning                       | Action                  |
| ------------------- | ----------------------------- | ----------------------- |
| `pre_fingerprint`   | Created before fingerprinting | Auto-migrated on update |
| `version_drifted`   | Skill version changed         | Consider re-sync        |
| `hash_drifted`      | Same version, scripts changed | Consider re-sync        |
| `migrated_artifact` | Previously migrated           | Recommend re-sync       |

### Migration

For pre-fingerprint artifacts:

```bash
python .claude/skills/work-tracker/scripts/migrate_artifacts.py \
  --scan docs/plans/      # Find artifacts needing migration
  --migrate docs/plans/   # Add fingerprint headers
  --verify docs/plans/    # Verify migration complete
```

### Sync Log Tracking

Status updates log the skill fingerprint:

```
| Time             | Action           | Source                             |
| ---------------- | ---------------- | ---------------------------------- |
| 2025-12-22 10:00 | Status update    | skill:work-tracker (wt-v2.0.0-abc) |
```

## TodoWrite Integration

Work Tracker v2.0.0+ includes bidirectional synchronization with Claude Code's TodoWrite tool.

### Overview

The integration provides:
- **Automatic initialization:** Session start populates TodoWrite from work-state.json
- **Status synchronization:** TodoWrite updates sync back to work-tracker
- **Conflict resolution:** Work-tracker is source of truth

### Architecture

```
work-state.json  ←→  TodoWriteAdapter  ←→  TodoWrite Tool
       ↑                                          ↓
       └──────── update_status.py ←───────────────┘
```

### Components

| Component | Location | Purpose |
|-----------|----------|---------|
| TodoWriteAdapter | `application/services/todowrite_sync.py` | Format conversion |
| WorkStateSyncService | `application/services/todowrite_sync.py` | Sync orchestration |
| SyncValidator | `application/services/todowrite_sync.py` | Integrity validation |
| ConflictResolver | `application/services/todowrite_sync.py` | Conflict handling |

### Status Mapping

| Work-Tracker | TodoWrite |
|--------------|-----------|
| Pending | pending |
| In Progress | in_progress |
| Complete | completed |
| Blocked | pending |
| Deferred | pending |

### Usage

**Initialize at session start:**
```python
from application.services import initialize_todowrite_from_work_state

result = initialize_todowrite_from_work_state()
# Returns: {"action": "initialize_todos", "todos": [...], "sync_enabled": True}
```

**Sync status update:**
```python
from application.services import WorkStateSyncService

sync = WorkStateSyncService()
result = sync.sync_todo_update(task_id="1.1", new_status="completed")
```

### Limitations

1. **Task-level only:** Subtasks not shown in TodoWrite (too granular)
2. **Session-bound:** TodoWrite resets each session (work-tracker persists)
3. **Single work item:** TodoWrite shows one active work item at a time
4. **No evidence:** Evidence tracking remains in work-tracker only

## Examples

### Example 1: Create New Work Tracker

User: "Let's track the work for adding authentication"
→ Generates work tracker with phases, syncs to `.ecw/plans/`

### Example 2: Check Progress

User: "What's remaining on the auth project?"
→ Loads from file, shows remaining tasks with progress

### Example 3: Mark Task Complete

User: "Mark task 2.3 as complete"
→ Updates markdown + JSON, recalculates progress

### Example 4: Resume After Break

User: (New session) "Where were we on the auth project?"
→ SessionStart shows active work context from `.ecw/plans/`

## Schema Migration (v1 to v2)

Work Tracker v2.0.0 includes migration support for upgrading legacy v1 trackers to the v2 schema.

### Migration Overview

| Feature | v1 (Legacy) | v2 (Current) |
|---------|-------------|--------------|
| Schema Version | None (implicit) | `schema_version: "2.0.0"` |
| Subtasks | Inline in tasks | Top-level `subtasks` array |
| Events | Not tracked | `events` array for audit trail |
| Evidence | Not tracked | `evidence` array for verification |
| Status Taxonomy | Basic (4 statuses) | Hierarchical (6 zones) |

### Using the SchemaMigrator

```python
from domain.migrations import SchemaMigrator

migrator = SchemaMigrator()

# Migrate in-memory data
result = migrator.migrate(v1_data)
if result.success:
    v2_data = result.data

# Migrate a file (with automatic backup)
result = migrator.migrate_file("docs/plans/old-tracker.json", backup=True)

# Dry run to preview changes
result = migrator.migrate(v1_data, dry_run=True)
print(result.preview)  # Shows planned changes
```

### Migration Features

- **Idempotent**: Safe to run multiple times
- **Data Preservation**: All original data preserved exactly
- **Backup**: Automatic backup before file modification
- **Event Logging**: `SchemaMigration` event recorded
- **Pure Function**: No side effects on input data

### Compatibility Checking

Use `CompatibilityChecker` to analyze trackers before migration:

```python
from domain.validators import CompatibilityChecker

checker = CompatibilityChecker()
result = checker.analyze("docs/plans/tracker.json")

print(f"Version: {result.detected_version}")
print(f"Compatible: {result.is_compatible}")
print(f"Needs Migration: {result.requires_migration}")

# Check for issues
for error in result.errors:
    print(f"ERROR: {error.code} - {error.message}")
for warning in result.warnings:
    print(f"WARN: {warning.code} - {warning.message}")
```

### Migration Command (wt.py)

```bash
# Check compatibility
python scripts/wt.py "check compatibility docs/plans/old-tracker.json"

# Migrate tracker
python scripts/wt.py "migrate docs/plans/old-tracker.json"

# Dry run (preview only)
python scripts/wt.py "migrate docs/plans/old-tracker.json --dry-run"
```

## Scripts

| Script                 | Purpose                                        | Works In |
| ---------------------- | ---------------------------------------------- | -------- |
| `detect_work_state.py` | Detect all work items, write state JSON        | Both     |
| `generate_tracker.py`  | Create new work tracker                        | Both     |
| `update_status.py`     | Update task/phase status (with fingerprinting) | Both     |
| `sync_to_file.py`      | Sync to `.ecw/plans/*.json`                    | Both     |
| `load_from_file.py`    | Load for SessionStart                          | Both     |
| `export_work.py`       | Export to proposal format                      | Both     |
| `verify_recovery.py`   | Verify integrity (with drift detection)        | Both     |
| `show_progress.py`     | Display progress summary                       | Both     |
| `skill_fingerprint.py` | Compute/validate skill fingerprints            | Both     |
| `migrate_artifacts.py` | Migrate pre-fingerprint artifacts              | Both     |

## Domain Components

### Validators (`domain/validators/`)

| Component | Purpose |
|-----------|---------|
| `CompatibilityChecker` | Analyze tracker schema version and compatibility |
| `ProgressConsistencyChecker` | Verify phase/task progress consistency |
| `SyncIntegrityValidator` | Validate JSON/MD synchronization |

### Migrations (`domain/migrations/`)

| Component | Purpose |
|-----------|---------|
| `SchemaMigrator` | Migrate v1 trackers to v2 schema |
| `MigrationResult` | Result dataclass for migration operations |

## Self-Healing System

> **Initiative:** 19 - SOP Violation Remediation
> **Version:** 1.0.0
> **Test Coverage:** 590 tests (Unit, Integration, Contract, Architectural, E2E)

### Overview

The Work Tracker skill includes an automated self-healing system based on the **MAPE-K autonomic computing model** (Kephart & Chess, 2003). This system automatically detects, diagnoses, and recovers from errors during work tracking operations.

**Key Benefits:**
- Automatic retry for transient errors (network, timeouts)
- Circuit breaker protection against cascading failures
- Structured error classification and recovery
- Audit trail of all recovery attempts

### Quick Start (For All Users)

```bash
# Self-healing is enabled by default
python scripts/wt.py --tracker docs/plans/project.md "mark task 1.1 complete"

# Disable self-healing for debugging
python scripts/wt.py --no-self-healing --tracker docs/plans/project.md "mark task 1.1 complete"

# Verbose mode shows health status
python scripts/wt.py --verbose --tracker docs/plans/project.md "show progress"
```

### MAPE-K Control Loop

The self-healing system implements the IBM Autonomic Computing MAPE-K control loop:

```
┌─────────────────────────────────────────────────────────────────┐
│                     MAPE-K Control Loop                         │
│                 (Kephart & Chess, IBM 2003)                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐ │
│   │ Monitor  │───▶│ Analyze  │───▶│  Plan    │───▶│ Execute  │ │
│   └──────────┘    └──────────┘    └──────────┘    └──────────┘ │
│        │                                               │        │
│        │              ┌──────────┐                     │        │
│        └─────────────▶│Knowledge │◀────────────────────┘        │
│                       │   Base   │                              │
│                       └──────────┘                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

Components:
- Monitor: Tracks health metrics (success rate, latency, errors)
- Analyze: Classifies errors into categories (transient, permanent, etc.)
- Plan: Selects recovery strategy based on error type
- Execute: Applies recovery action (retry, escalate, circuit break)
- Knowledge: Records patterns for future decision-making
```

**Reference:** Kephart, J.O. & Chess, D.M. (2003). "The Vision of Autonomic Computing." *IEEE Computer*, 36(1), 41-50.

### Error Classification

The symptom analyzer classifies errors into recovery categories:

| Category | Examples | Recovery Strategy | Confidence |
|----------|----------|-------------------|------------|
| **Transient** | TimeoutError, ConnectionError | Retry with backoff | 0.9 |
| **Permanent** | FileNotFoundError, PermissionError | Escalate to user | 0.95 |
| **Validation** | ValueError, JSONDecodeError | Alternative input | 0.7 |
| **Resource** | MemoryError, DiskFull | Cleanup & retry | 0.8 |
| **Unknown** | Unclassified exceptions | Conservative retry | 0.5 |

### Retry Policies

```python
# Default policies (from domain/self_healing/value_objects.py)
RetryPolicy.default()        # max_retries=3, initial_delay=1.0s, backoff=2.0
RetryPolicy.aggressive()     # max_retries=5, initial_delay=0.5s, backoff=1.5
RetryPolicy.conservative()   # max_retries=2, initial_delay=2.0s, backoff=3.0
RetryPolicy.no_retry()       # max_retries=0 (immediate failure)
```

**Reference:** Nygard, M.T. (2007). *Release It! Design and Deploy Production-Ready Software*. Pragmatic Bookshelf. (Circuit Breaker pattern)

### Circuit Breaker

Prevents cascading failures when a service is degraded:

```
┌───────────────────────────────────────────────────────────────┐
│                   Circuit Breaker States                       │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│   ┌──────────┐   failure    ┌──────────┐   timeout  ┌──────┐ │
│   │  CLOSED  │──────────────▶│   OPEN   │───────────▶│ HALF │ │
│   │(normal)  │               │(blocking)│            │ OPEN │ │
│   └──────────┘               └──────────┘            └──────┘ │
│        ▲                                                 │    │
│        │                    success                      │    │
│        └─────────────────────────────────────────────────┘    │
│                                                               │
│   Thresholds: 5 failures → OPEN, 60s timeout → HALF_OPEN     │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

### Four-Level Enforcement Model

The self-healing system integrates with a four-level enforcement model for SOP compliance:

| Level | Mechanism | Behavior | Override |
|-------|-----------|----------|----------|
| **1. Advisory** | CLAUDE.md instructions | Provides recommendations, never blocks | Claude discretion |
| **2. Soft** | SKILL.md consent prompts | Prompts for consent | `--skip-consent` flag |
| **3. Medium** | Agent tool restrictions | Blocks subagents | `--parent-approved` flag |
| **4. HARD** | PreToolUse hook | Blocks tool calls | `--user-approved` flag |

#### Level 1: Advisory (CLAUDE.md)

Advisory enforcement provides recommendations without blocking:

```python
from domain.self_healing.enforcement import AdvisoryAdvisor

advisor = AdvisoryAdvisor()
symptom = Symptom(command="test", error=TimeoutError())
recommendation = advisor.advise(symptom)
# Returns: AdvisoryRecommendation(action="RETRY_WITH_BACKOFF", confidence=0.9)
```

#### Level 2: Soft (SKILL.md)

Soft enforcement requests user consent:

```python
from domain.self_healing.enforcement import ConsentManager

manager = ConsentManager()
if not manager.check_consent("self_healing"):
    request = manager.request_consent("self_healing")
    # Present request to user, await response
    manager.process_response("self_healing", "yes")  # or "always" for blanket
```

#### Level 3: Medium (Agent Restrictions)

Medium enforcement restricts subagent operations:

```python
from domain.self_healing.enforcement import AgentRestrictionEnforcer, AgentContext

enforcer = AgentRestrictionEnforcer.with_default_restrictions()
subagent = AgentContext(agent_type="subagent")

result = enforcer.check_operation("create_initiative", subagent)
# result.allowed = False (subagents cannot create initiatives)
```

**Reference:** SOP-IC (Initiative Consent) in CLAUDE.md

#### Level 4: HARD (Hook Enforcement)

HARD enforcement validates tool calls before execution:

```python
from domain.self_healing.enforcement import HookEnforcer

enforcer = HookEnforcer.for_initiative_consent()
decision = enforcer.check_tool_call(
    tool_name="Write",
    tool_input={"file_path": "docs/plans/99-new-initiative.md"},
)
# decision.proceed = False, decision.exit_code = 1
```

### Unified Four-Level Enforcer

For comprehensive enforcement across all levels:

```python
from domain.self_healing.enforcement import FourLevelEnforcer, EnforcementContext

# Create enforcer with default configurations
enforcer = FourLevelEnforcer.with_defaults()

# Check an operation against all levels
context = EnforcementContext.for_operation("create_initiative", agent_type="subagent")
result = enforcer.check(context)

if not result.allowed:
    print(f"Blocked at level: {result.blocking_level}")
    print(f"Advisory recommendation: {result.recommendation}")
```

### CLI Usage Examples

```bash
# Standard operation (self-healing enabled)
python scripts/wt.py --tracker docs/plans/project.md "mark task 1.1 complete"

# Disable self-healing for debugging
python scripts/wt.py --no-self-healing --tracker docs/plans/project.md "mark task 1.1 complete"

# Verbose output shows health metrics
python scripts/wt.py --verbose --tracker docs/plans/project.md "show progress"

# Combined flags
python scripts/wt.py --verbose --no-self-healing --tracker docs/plans/project.md "show progress"
```

### Domain Components

#### Self-Healing (`domain/self_healing/`)

| Component | Purpose |
|-----------|---------|
| `HealthMonitor` | Tracks success rate, latency, error counts |
| `SymptomAnalyzer` | Classifies errors into recovery categories |
| `RemediationPlanner` | Selects recovery strategy based on analysis |
| `ActionExecutor` | Executes recovery actions (retry, cleanup, etc.) |
| `KnowledgeBase` | Records patterns for adaptive recovery |
| `CircuitBreaker` | Prevents cascading failures |
| `SelfHealingDispatcher` | Integrates MAPE-K with command dispatch |

#### Enforcement (`domain/self_healing/enforcement/`)

| Component | Purpose |
|-----------|---------|
| `AdvisoryAdvisor` | Level 1: Recommendations without blocking |
| `ConsentManager` | Level 2: Consent tracking and prompts |
| `AgentRestrictionEnforcer` | Level 3: Agent-based restrictions |
| `HookEnforcer` | Level 4: Tool call validation |
| `FourLevelEnforcer` | Unified enforcement across all levels |

### Architecture Principles

The self-healing system follows these architectural principles:

1. **Domain-Driven Design (Evans, 2003):**
   - Value objects are immutable (`@dataclass(frozen=True)`)
   - Aggregates maintain consistency boundaries
   - Domain layer has no infrastructure dependencies

2. **Clean Architecture (Martin, 2017):**
   - Domain → Application → Infrastructure dependency flow
   - No circular dependencies between modules
   - Testable without external systems

3. **Resilience Patterns (Nygard, 2007):**
   - Circuit breaker prevents cascading failures
   - Retry with exponential backoff for transient errors
   - Bulkhead isolation between components

**References:**
- Evans, E. (2003). *Domain-Driven Design: Tackling Complexity in the Heart of Software*. Addison-Wesley.
- Martin, R.C. (2017). *Clean Architecture: A Craftsman's Guide to Software Structure and Design*. Prentice Hall.
- Nygard, M.T. (2007). *Release It! Design and Deploy Production-Ready Software*. Pragmatic Bookshelf.

### Test Coverage

The self-healing system has comprehensive test coverage:

| Test Level | Count | Purpose |
|------------|-------|---------|
| Unit | ~250 | Individual component behavior |
| Integration | 16 | Component interactions |
| Contract | 82 | API contracts and interfaces |
| Architectural | 14 | Dependency rules and patterns |
| E2E | 15 | Full CLI workflows |
| **Total** | **590** | **All levels combined** |

```bash
# Run all self-healing tests
python -m pytest tests/unit/test_self_healing/ tests/contract/test_self_healing/ \
  tests/integration/test_self_healing*.py tests/architectural/test_self_healing/ \
  tests/e2e/test_wt_self_healing_e2e.py -v
```

### Troubleshooting

**Self-healing not activating:**
1. Verify not using `--no-self-healing` flag
2. Check circuit breaker state (may be OPEN after failures)
3. Use `--verbose` to see health metrics

**Too many retries:**
1. Check if error is truly transient
2. Adjust retry policy in dispatcher configuration
3. Consider using `--no-self-healing` for debugging

**Consent prompts appearing unexpectedly:**
1. Check if consent state was cleared
2. Use `--skip-consent` for automated workflows
3. Verify blanket approval was granted if expected

## D-040 Migration Status

> **Initiative:** D-040 - Hexagonal Architecture Migration
> **Status:** In Progress (Phase 16)
> **Target:** ECW namespace under `src/ecw/`

### Overview

The work-tracker skill is being migrated to a standardized ECW (Evolving Claude Workflow) namespace
structure. This migration separates legacy pre-Hexagonal scripts from the modern Hexagonal Architecture.

### Current Package Structure (Legacy)

| Package | Location | Status |
|---------|----------|--------|
| commands | `commands/` | Active (will migrate to `src/ecw/skills/work_tracker/cli/`) |
| domain | `domain/` | Active (will migrate to `src/ecw/skills/work_tracker/domain/`) |
| infrastructure | `infrastructure/` | Active (will migrate to `src/ecw/skills/work_tracker/infrastructure/`) |
| application | `application/` | Active (will migrate to `src/ecw/skills/work_tracker/application/`) |
| scripts | `scripts/` | Active (remains at root, canonical entry points) |

### Target Package Structure (ECW Namespace)

```
src/
└── ecw/                           # ECW namespace root
    ├── common/                    # Shared cross-skill components
    │   ├── di/                    # Dependency injection
    │   ├── events/                # Event infrastructure
    │   ├── persistence/           # Generic persistence
    │   ├── validation/            # Shared validators
    │   └── cli/                   # CLI utilities
    └── skills/
        └── work_tracker/          # Work tracker skill
            ├── domain/            # Domain layer
            ├── application/       # Application layer
            ├── infrastructure/    # Infrastructure layer
            └── cli/               # CLI layer
```

### Legacy Isolation

Deprecated pre-Hexagonal scripts have been moved to `legacy/`:

```
legacy/
├── scripts/               # Deprecated scripts (DO NOT USE)
│   ├── update_status.py   # DEPRECATED - Use wt.py
│   ├── sync_to_file.py    # DEPRECATED - Bypasses JSON SSOT
│   ├── add_task.py        # DEPRECATED - Use wt.py
│   ├── add_phase.py       # DEPRECATED - Use wt.py
│   └── add_subtask.py     # DEPRECATED - Use wt.py
└── tests/                 # Tests for legacy scripts
    ├── unit/              # Unit tests using deprecated imports
    └── integration/       # Integration tests using deprecated imports
```

### Path Migration Reference

When migrating imports, use this mapping:

| Old Import | New Import (Future) |
|------------|---------------------|
| `from domain.entities import Task` | `from ecw.skills.work_tracker.domain.entities import Task` |
| `from application.use_cases import CreateTask` | `from ecw.skills.work_tracker.application.use_cases import CreateTask` |
| `from infrastructure.adapters import JsonFileAdapter` | `from ecw.skills.work_tracker.infrastructure.adapters import JsonFileAdapter` |
| `from commands.dispatcher import CommandDispatcher` | `from ecw.skills.work_tracker.cli.commands import CommandDispatcher` |

### Data Migration Tools

Schema migration utilities are available at `infrastructure/migration/`:

| Function | Purpose |
|----------|---------|
| `is_v1_schema(data)` | Detect V1 (legacy) schema |
| `is_v2_schema(data)` | Detect V2 (current) schema |
| `migrate_v1_to_v2(data)` | Migrate V1 data to V2 format |
| `validate_migration(original, migrated)` | Validate migration success |

### Canonical Entry Point

**All work tracker operations MUST use:**
```bash
python3 scripts/wt.py --tracker <path> "<command>"
```

This path (`scripts/wt.py`) is NOT changing during the migration.

## References

- `docs/guides/claude-code-capabilities.md` - Environment differences
- `references/ecw-patterns.md` - ECW integration details
- `references/completion-criteria.md` - Verification guidelines
- `templates/work-tracker.md` - Base template
- Kephart, J.O. & Chess, D.M. (2003). "The Vision of Autonomic Computing." *IEEE Computer*, 36(1), 41-50.
- Evans, E. (2003). *Domain-Driven Design*. Addison-Wesley.
- Martin, R.C. (2017). *Clean Architecture*. Prentice Hall.
- Nygard, M.T. (2007). *Release It!* Pragmatic Bookshelf.

```

```
