# Work Tracker Skill

> Local Azure DevOps/JIRA alternative for surviving context rot in long-running sessions.

---

## Purpose

The Work Tracker skill provides persistent task management that survives context
compaction, session boundaries, and context rot. It serves as the "external memory"
for tracking what needs to be done, what's in progress, and what's completed.

### The Context Rot Problem

> "Context Rot is the phenomenon where an LLM's performance degrades as the context
> window fills up, even when total token count is well within the technical limit."
> — [Chroma Research](https://research.trychroma.com/context-rot)

Work Tracker mitigates this by:
- **Persisting state to filesystem** - Not dependent on context window
- **Providing compact summaries** - Load only what's needed
- **Enabling session continuity** - Pick up where you left off

---

## Commands

### Create Work Item

Create a new work item for tracking.

```
@worktracker create <title> [--type TYPE] [--priority PRIORITY] [--parent PARENT_ID]
```

**Arguments:**
- `title`: Short description of the work (required)
- `--type`: `feature`, `bug`, `task`, `spike`, `epic` (default: `task`)
- `--priority`: `critical`, `high`, `medium`, `low` (default: `medium`)
- `--parent`: Parent work item ID for hierarchy

**Example:**
```
@worktracker create "Implement user authentication" --type feature --priority high
```

**Output:**
```
Created: WORK-001 "Implement user authentication"
Type: feature | Priority: high | Status: pending
```

---

### List Work Items

List work items with optional filters.

```
@worktracker list [--status STATUS] [--type TYPE] [--priority PRIORITY] [--limit N]
```

**Arguments:**
- `--status`: `pending`, `in_progress`, `blocked`, `completed`, `all` (default: `pending,in_progress`)
- `--type`: Filter by type
- `--priority`: Filter by priority
- `--limit`: Maximum items to return (default: 20)

**Example:**
```
@worktracker list --status in_progress
```

**Output:**
```
Work Items (in_progress):
┌────────────┬──────────────────────────────┬──────────┬──────────┐
│ ID         │ Title                        │ Priority │ Type     │
├────────────┼──────────────────────────────┼──────────┼──────────┤
│ WORK-001   │ Implement user authentication│ high     │ feature  │
│ WORK-003   │ Fix login redirect bug       │ critical │ bug      │
└────────────┴──────────────────────────────┴──────────┴──────────┘
```

---

### Update Work Item

Update a work item's properties.

```
@worktracker update <id> [--status STATUS] [--priority PRIORITY] [--title TITLE] [--notes NOTES]
```

**Arguments:**
- `id`: Work item ID (required)
- `--status`: New status
- `--priority`: New priority
- `--title`: New title
- `--notes`: Add notes to the work item

**Example:**
```
@worktracker update WORK-001 --status in_progress --notes "Started implementation, defining domain entities"
```

**Output:**
```
Updated: WORK-001
Status: pending → in_progress
Notes added: "Started implementation, defining domain entities"
```

---

### Complete Work Item

Mark a work item as completed.

```
@worktracker complete <id> [--notes NOTES]
```

**Arguments:**
- `id`: Work item ID (required)
- `--notes`: Completion notes

**Example:**
```
@worktracker complete WORK-001 --notes "Implemented with JWT tokens, tests passing"
```

**Output:**
```
Completed: WORK-001 "Implement user authentication"
Duration: 2h 15m
Notes: "Implemented with JWT tokens, tests passing"
```

---

### Show Work Item Details

Show full details of a work item.

```
@worktracker show <id>
```

**Example:**
```
@worktracker show WORK-001
```

**Output:**
```
WORK-001: Implement user authentication
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Type:       feature
Status:     completed
Priority:   high
Created:    2026-01-07 10:30:00
Completed:  2026-01-07 12:45:00
Duration:   2h 15m

Description:
  Add JWT-based authentication to the API layer.

Notes:
  [2026-01-07 10:35] Started implementation, defining domain entities
  [2026-01-07 11:20] Domain layer complete, moving to infrastructure
  [2026-01-07 12:45] Implemented with JWT tokens, tests passing

Children:
  WORK-002: Create User entity (completed)
  WORK-003: Implement JWT adapter (completed)

References:
  - docs/design/AUTH_DESIGN.md
  - src/domain/aggregates/user.py
```

---

### Search Work Items

Search work items by text.

```
@worktracker search <query> [--include-completed]
```

**Arguments:**
- `query`: Search text (searches title, description, notes)
- `--include-completed`: Include completed items in search

**Example:**
```
@worktracker search "authentication"
```

---

### Session Summary

Get a summary for the current session context.

```
@worktracker summary [--since DURATION]
```

**Arguments:**
- `--since`: Time window (`1h`, `1d`, `1w`) (default: current session)

**Example:**
```
@worktracker summary --since 1d
```

**Output:**
```
Work Tracker Summary (last 24h)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Completed: 5 items
  - WORK-001: Implement user authentication
  - WORK-002: Create User entity
  - ...

In Progress: 2 items
  - WORK-006: Add rate limiting [high]
  - WORK-007: Write API documentation [medium]

Blocked: 1 item
  - WORK-008: Deploy to staging (waiting on infra)

Pending: 12 items (3 high priority)

Recommended Next:
  → WORK-006: Add rate limiting (high priority, in progress)
```

---

## Data Model

### Work Item Properties

| Property | Type | Description |
|----------|------|-------------|
| `id` | string | Unique identifier (WORK-NNN) |
| `title` | string | Short description |
| `description` | string | Detailed description |
| `type` | enum | feature, bug, task, spike, epic |
| `status` | enum | pending, in_progress, blocked, completed |
| `priority` | enum | critical, high, medium, low |
| `parent_id` | string | Parent work item ID |
| `created_at` | datetime | Creation timestamp |
| `updated_at` | datetime | Last update timestamp |
| `completed_at` | datetime | Completion timestamp |
| `notes` | list | Timestamped notes |
| `references` | list | Related files/docs |
| `tags` | list | Custom tags |

### Storage

Work items are stored in the active project's `.jerry/data/` directory:

```
projects/${JERRY_PROJECT}/.jerry/data/
├── items/
│   └── WORK-NNN.json    # Individual work item files
├── index.json           # Quick lookup index
└── sequences.json       # ID sequence tracking
```

> **Note**: `JERRY_PROJECT` environment variable must be set to identify the active project.
> If not set, the skill will prompt you to specify which project to use.

---

## Integration

### With TodoWrite Tool

Work Tracker complements the built-in TodoWrite tool:
- **TodoWrite**: Ephemeral, in-session task tracking
- **Work Tracker**: Persistent, cross-session work items

Sync pattern:
```
@worktracker sync-from-todo  # Import current todos as work items
@worktracker sync-to-todo    # Export work items to todos
```

### With PLAN Files

Work items can reference PLAN files:
```
@worktracker create "Implement caching layer" --plan docs/plans/PLAN_caching.md
```

### With Commits

Work items can be linked to commits:
```
git commit -m "feat(auth): implement JWT tokens

Closes: WORK-001, WORK-002"
```

---

## Execution

This skill invokes the domain use cases via CLI shim:

```bash
python scripts/invoke_use_case.py worktracker <command> [args]
```

The script routes to:
- `src/application/use_cases/commands/` for mutations
- `src/application/use_cases/queries/` for reads

---

## Best Practices

1. **Create work items before starting work** - Establishes tracking
2. **Update status promptly** - Accurate state for context reload
3. **Add notes during work** - Captures context for later
4. **Use hierarchy for complex tasks** - Epics → Features → Tasks
5. **Link references** - Connect to files, docs, commits
6. **Run summary at session start** - Orient to current state
