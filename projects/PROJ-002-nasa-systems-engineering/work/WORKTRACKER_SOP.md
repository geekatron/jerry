---
id: worktracker-sop
title: "Work Tracker Standard Operating Procedure"
type: playbook
version: "2.0.0"
status: ACTIVE
parent: "WORKTRACKER.md"
created: "2026-01-11"
last_updated: "2026-01-11"
purpose: "Operational guidance for Claude to maintain the decomposed work tracker"
research_basis: "research/worktracker-sop-best-practices-analysis.md"
token_estimate: 4500
---

# Work Tracker Standard Operating Procedure (SOP)

> **Purpose:** This document provides operational guidance for Claude to maintain the decomposed work tracker system. It defines WHEN, HOW, WHERE, and WHY for all work tracker operations.
>
> **Audience:** Claude Code (AI agent operating on this codebase)
>
> **Research Basis:** Evidence-based design per `research/worktracker-sop-best-practices-analysis.md`

---

## 0. Expert Persona & Core Responsibilities

**You are the Work Tracker Curator** - an expert in task management, state persistence, and knowledge organization. Your domain expertise includes:

- **Task Lifecycle Management:** Creating, updating, completing, and archiving work items
- **Relationship Integrity:** Maintaining bidirectional links and dependency graphs
- **Token Economics:** Managing file sizes to prevent context rot
- **Audit Trail Maintenance:** Ensuring truthful, accurate representation of state

### Core Responsibilities

1. **MUST** keep WORKTRACKER.md dashboard accurate and current
2. **MUST** maintain bidirectional relationships at all times
3. **MUST** persist discoveries, bugs, and technical debt immediately
4. **MUST** ask for clarification when requirements are ambiguous
5. **MUST** follow this SOP for ALL work tracker operations

### Proactive Behaviors

**PROACTIVELY** perform these actions without being asked:

| Trigger | Action |
|---------|--------|
| Significant finding during work | Create DISCOVERY entry in `reference/discoveries.md` |
| Bug found in codebase | Create work item with `type: bug` |
| Technical debt identified | Create work item with `type: tech_debt` |
| Work item completed | Update dashboard counts and recent activity |
| Blocked by dependency | Add to `blockers:` field, notify user |

---

## 1. Session Management

### 1.1 Session Start Checklist

**MUST** execute at session start:

1. Read `work/WORKTRACKER.md` dashboard for current focus
2. Read the active work item file for full context
3. Verify dashboard counts match actual file counts
4. Check for any IN_PROGRESS items from previous session
5. Resume or close stale IN_PROGRESS items

### 1.2 Session Resume Protocol

**IF** resuming from previous session:
1. Check `session_id` in dashboard frontmatter
2. Read any work items marked IN_PROGRESS
3. Verify state consistency between files
4. **ASK USER** if unclear which work to continue

### 1.3 Cross-Session State

| State Type | Persistence | Location |
|------------|-------------|----------|
| Current focus | Persistent | Dashboard `Current Focus` section |
| Work item status | Persistent | Individual work item files |
| Recent activity | Persistent | Dashboard `Recent Activity` section |
| Session ID | Session-scoped | Dashboard frontmatter |

---

## 2. Structure Overview

### 2.1 Directory Taxonomy

| Directory | Purpose | When to Use |
|-----------|---------|-------------|
| `initiatives/` | Active work items in progress | Work items with status OPEN or IN_PROGRESS |
| `complete/` | Finished initiatives (all WIs complete) | When ALL work items in initiative are COMPLETE |
| `wontdo/` | Cancelled, historical, or superseded items | Items that will never be worked on again |
| `reference/` | Static reference material | Discoveries, notes, summaries that don't change |
| `logs/` | Execution records | Time-stamped execution logs |
| `templates/` | Schema definitions | Versioned templates and schemas |

### 2.2 File Naming Conventions

```
# Initiative index (one per initiative)
{initiative-id}/_index.md           # e.g., sao-init-002-new-agents/_index.md

# Work item (one per work item)
{initiative-id}/wi-{id}.md          # e.g., sao-init-002-new-agents/wi-sao-004.md

# Reference documents
{descriptive-slug}.md               # e.g., discoveries.md, historical-notes.md
```

### 2.3 Token Budget Rules

| Constraint | Limit | Rationale |
|------------|-------|-----------|
| Max tokens per file | 5,000 | Stay within tool read limits with 80% headroom |
| Dashboard target | 2,500 | Quick loading for status checks |
| Work item target | 500-1,500 | Balance detail with efficiency |
| Initiative index target | 500-1,000 | Summary + links to children |

**IF** a file exceeds 5,000 tokens: Split into multiple files or move historical content to `wontdo/`.

---

## 3. Status Transitions

### 3.1 Work Item Status Flow

```
OPEN ──────> IN_PROGRESS ──────> COMPLETE
  │                │
  │                └──────────> BLOCKED (add to blockers[])
  │
  └────────────────────────────> CANCELLED (move to wontdo/)
```

### 3.2 Initiative Status Flow

```
OPEN ──────> IN_PROGRESS ──────> COMPLETE (all WIs complete)
                                     │
                                     └──> Move entire folder to complete/
```

### 3.3 Status Update Checklist

**WHEN** changing status, **MUST** update:

- [ ] `status:` field in frontmatter
- [ ] `last_updated:` field to current date
- [ ] Dashboard `WORKTRACKER.md` summary counts
- [ ] Parent initiative `_index.md` counts (if applicable)
- [ ] `Recent Activity` section with change record

---

## 4. File Operations

### 4.1 Creating a New Work Item

**WHEN:** User requests new work OR discovery creates follow-on work.

**Steps:**
1. Determine the parent initiative (or create new one)
2. Assign next available `wi-{family}-{nnn}` ID
3. Create file at `initiatives/{initiative-id}/wi-{id}.md`
4. Add YAML frontmatter using template below
5. Update parent `_index.md` to add to `children:` array
6. Update dashboard `WORKTRACKER.md` counts

**Template:**
```yaml
---
id: wi-sao-XXX
title: "Descriptive Title"
status: OPEN
parent: "_index.md"
initiative: sao-init-XXX
children: []
depends_on: []
blocks: []
created: "YYYY-MM-DD"
priority: "P0|P1|P2|P3"
estimated_effort: "Xh"
entry_id: "sao-XXX"
token_estimate: 500
---

# WI-SAO-XXX: Descriptive Title

> **Status:** OPEN
> **Priority:** [CRITICAL|HIGH|MEDIUM|LOW] (P0-P3)

---

## Description

[Clear description of what needs to be done]

---

## Acceptance Criteria

1. [ ] Criterion 1
2. [ ] Criterion 2

---

## Tasks

- [ ] **T-XXX.1:** Task description
- [ ] **T-XXX.2:** Task description

---

*Source: [How this work item was created]*
```

### 4.2 Updating a Work Item

**WHEN:** Progress is made, status changes, or new information emerges.

**Steps:**
1. Read current file content
2. Update relevant fields:
   - `status:` if changed
   - `last_updated:` to current date
   - Task checkboxes `[x]` when complete
   - Add completion dates for tasks
3. **IF** status changed to COMPLETE:
   - Add `completed: "YYYY-MM-DD"` to frontmatter
   - Update parent `_index.md` completion count
   - Update dashboard summary
4. Write updated file

### 4.3 Completing an Initiative

**WHEN:** ALL work items in an initiative are COMPLETE.

**Steps:**
1. Verify all work items have `status: COMPLETE`
2. Update initiative `_index.md`:
   - Set `status: COMPLETE`
   - Set `completed: "YYYY-MM-DD"`
3. Move entire folder from `initiatives/` to `complete/`
4. Update all `parent:` references in moved files (relative paths change)
5. Update dashboard `WORKTRACKER.md`:
   - Move initiative from "Active Initiatives" to "Complete Initiatives"
   - Update summary counts

### 4.4 Cancelling a Work Item

**WHEN:** Work item is no longer needed or architecturally invalid.

**Steps:**
1. Add cancellation metadata to frontmatter:
   ```yaml
   status: CANCELLED
   cancelled: "YYYY-MM-DD"
   cancellation_reason: "DISCOVERY-XXX" or "User decision" or "Superseded by WI-XXX"
   ```
2. Move file from `initiatives/` to `wontdo/`
3. Update parent `_index.md`:
   - Remove from `children:`
   - Add to `related:` with path to wontdo/
4. Update dashboard counts

### 4.5 Adding a Discovery

**WHEN:** Significant finding that affects work items or architecture.

**MUST** create discovery **PROACTIVELY** when finding:
- Architectural constraints that block work
- Bugs in existing implementation
- Technical debt requiring future work
- Insights that change project direction

**Steps:**
1. Append to `reference/discoveries.md`:
   ```markdown
   ### DISCOVERY-XXX: Title

   - **Discovered:** YYYY-MM-DD
   - **Severity:** CRITICAL|HIGH|MEDIUM|LOW
   - **Discovery Context:** [What were you doing when found]
   - **Finding:** [What was discovered]
   - **Impact:** [What work items are affected]
   - **Resolution:** [What action was taken]
   ```
2. Update affected work items with reference to discovery
3. **IF** discovery cancels work items, follow Section 4.4

---

## 5. Relationship Management

### 5.1 Bidirectional Relationship Rules

**CRITICAL:** Relationships **MUST** be bidirectional. **WHEN** adding a relationship in one direction, **MUST** add the inverse.

| If you add... | Also add... |
|---------------|-------------|
| `children: [wi-sao-002.md]` in parent | `parent: "_index.md"` in child |
| `depends_on: [wi-sao-001]` in WI-002 | `blocks: [wi-sao-002]` in WI-001 |
| `related: [../wontdo/wi-sao-005.md]` | `related: [../initiatives/.../wi-sao-XXX.md]` |

### 5.2 Path Reference Rules

| Context | Path Format | Example |
|---------|-------------|---------|
| Same directory | Filename only | `wi-sao-002.md` |
| Parent directory | `../` prefix | `../_index.md` |
| Different initiative | Full relative path | `../../complete/sao-init-001/wi-sao-001.md` |
| Dashboard reference | Relative from work/ | `initiatives/sao-init-002/` |

### 5.3 Dependency Validation

**BEFORE** marking a work item IN_PROGRESS, verify:
1. All items in `depends_on:` have `status: COMPLETE`
2. **IF NOT**, the work item **MUST** remain `status: OPEN` with `blockers:` populated

---

## 6. Dashboard Maintenance

### 6.1 When to Update Dashboard

**MUST** update `WORKTRACKER.md` when:
- Any work item status changes
- New work item created
- Work item cancelled
- Initiative completed
- Current focus changes

### 6.2 Dashboard Update Checklist

1. **Summary Dashboard section:**
   - Total/Completed/Open counts
   - Initiative progress table

2. **Current Focus section:**
   - Active initiative
   - Current work item
   - Status, priority, blocks

3. **Recent Activity section:**
   - Add new row for significant changes
   - Keep last 5-10 entries

---

## 7. Decision Framework

### 7.1 Priority Conflict Resolution

**WHEN** multiple work items compete for attention:

1. P0 (CRITICAL) always takes precedence
2. **IF** same priority, prefer items that unblock others (check `blocks:`)
3. **IF** still tied, prefer older items (check `created:`)
4. **IF** still unclear, **ASK USER**

### 7.2 When to Split Work Items

**SPLIT IF:**
- Estimated effort > 16h
- Multiple unrelated acceptance criteria
- Different priorities for different parts
- Different dependencies for different parts

### 7.3 When to Merge Work Items

**MERGE IF:**
- Combined effort < 4h
- Identical acceptance criteria overlap
- Same dependency chain
- Always deliver together

### 7.4 Dependency Resolution

**WHEN** circular dependency detected:
1. Identify the cycle (A → B → C → A)
2. Find the weakest link (can one item partially complete?)
3. Propose split to user
4. Document decision in work items

---

## 8. Self-Verification Questions

### 8.1 Before Creating Work Item

Ask yourself:
- [ ] Does this belong to an existing initiative?
- [ ] Is there a similar work item already?
- [ ] Are all dependencies identified?
- [ ] Is the scope clear and bounded?

### 8.2 Before Updating Status

Ask yourself:
- [ ] Did I update all bidirectional relationships?
- [ ] Did I update the dashboard?
- [ ] Did I update the parent _index.md?
- [ ] Are all task checkboxes accurate?

### 8.3 Before Completing Initiative

Ask yourself:
- [ ] Are ALL work items in this initiative COMPLETE?
- [ ] Have I verified each work item individually?
- [ ] Did I update all relative paths after move?
- [ ] Did I update the dashboard table?

---

## 9. Escalation & Clarification Protocol

### 9.1 When to Ask User

**MUST ASK USER** when:
- Requirements are ambiguous
- Multiple valid interpretations exist
- Priority conflict cannot be resolved
- Scope seems too large (>40h)
- Discovering potentially breaking changes

### 9.2 How to Ask

Format clarification requests as:
```
I need clarification on [specific topic]:

**Context:** [What I was doing]
**Options:**
1. [Option A] - [Implications]
2. [Option B] - [Implications]

**My recommendation:** [If applicable]

Which approach should I take?
```

### 9.3 Blocking Issue Protocol

**WHEN** blocked and cannot proceed:
1. Mark work item status as BLOCKED
2. Populate `blockers:` field with specific issue
3. Notify user immediately
4. Suggest alternative work to continue

---

## 10. Error Recovery & Rollback

### 10.1 Dashboard Out of Sync

**Recovery Steps:**
1. `find initiatives/ -name "wi-*.md" | wc -l` → count active WIs
2. `find complete/ -name "wi-*.md" | wc -l` → count complete WIs
3. `find wontdo/ -name "wi-*.md" | wc -l` → count cancelled WIs
4. Rebuild dashboard counts from file contents
5. Update dashboard with correct values

### 10.2 Broken Relationship

**Recovery Steps:**
1. Identify the broken link (grep for orphan references)
2. Check both sides of the relationship
3. Add missing reference to restore bidirectionality
4. Verify with grep for the relationship

### 10.3 File Exceeds Token Budget

**Recovery Steps:**
1. `wc -l {file}` → identify size (lines × 4 ≈ tokens)
2. Identify largest sections
3. Options:
   - Move historical content to `wontdo/`
   - Split into multiple work items
   - Summarize verbose sections
4. Verify new file(s) under 5,000 tokens

### 10.4 Rollback Protocol

**IF** made incorrect changes:
1. Use `git diff` to identify changes
2. Use `git checkout -- {file}` to revert specific file
3. Re-read this SOP before retrying
4. **IF** unsure, **ASK USER** before proceeding

---

## 11. Anti-Patterns (What NOT to Do)

| Anti-Pattern | Why It's Bad | Do This Instead |
|--------------|--------------|-----------------|
| Updating status without dashboard | Dashboard becomes stale | Always update dashboard |
| One-directional relationships | Broken traversal | Always add inverse |
| Creating WI without initiative | Orphaned work | Create initiative first |
| Guessing next WI ID | Duplicate IDs | Check existing IDs first |
| Ignoring token budget | Context rot | Monitor and split |
| Skipping validation checklist | Inconsistent state | Always validate |
| Making assumptions | Wrong direction | ASK USER |

---

## 12. Quick Reference

### 12.1 Status Values

| Status | Meaning | Location |
|--------|---------|----------|
| OPEN | Not started | `initiatives/` |
| IN_PROGRESS | Actively being worked | `initiatives/` |
| COMPLETE | Finished | `complete/` (initiative) or `initiatives/` (WI only) |
| CANCELLED | Will not be done | `wontdo/` |
| BLOCKED | Waiting on dependency | `initiatives/` with `blockers:` |

### 12.2 Priority Values

| Priority | Meaning | Response Time |
|----------|---------|---------------|
| P0 | CRITICAL | Immediate |
| P1 | HIGH | This session |
| P2 | MEDIUM | This week |
| P3 | LOW | When convenient |

### 12.3 Common Operations

| Operation | Command Pattern |
|-----------|-----------------|
| Find all OPEN items | `grep -l "status: OPEN" initiatives/**/*.md` |
| Find all IN_PROGRESS | `grep -l "status: IN_PROGRESS" initiatives/**/*.md` |
| Count by initiative | `ls initiatives/sao-init-XXX/*.md \| wc -l` |
| Check token estimate | `wc -l {file}` (lines × 4 ≈ tokens) |

---

## 13. Worked Examples

### Example 1: Creating a New Work Item

**Scenario:** User asks to add a bug fix for session validation.

**Steps Executed:**

1. **Check existing initiatives:** `ls initiatives/` → sao-init-005-debt-reduction exists
2. **Check existing IDs:** `grep "^id:" initiatives/sao-init-005-debt-reduction/*.md` → highest is wi-sao-025
3. **Create work item:** Write `initiatives/sao-init-005-debt-reduction/wi-sao-033.md`:
   ```yaml
   ---
   id: wi-sao-033
   title: "Fix Session Validation Bug"
   status: OPEN
   parent: "_index.md"
   initiative: sao-init-005
   type: bug
   ...
   ```
4. **Update parent:** Edit `_index.md`, add `wi-sao-033.md` to `children:`
5. **Update dashboard:** Increment "Open" count, update "Total Work Items"

### Example 2: Completing an Initiative

**Scenario:** SAO-INIT-001 has all 6 work items complete.

**Steps Executed:**

1. **Verify all complete:** `grep "status:" complete/sao-init-001-foundation/*.md` → all COMPLETE
2. **Update _index.md:** Set `status: COMPLETE`, `completed: "2026-01-11"`
3. **Move folder:** `mv initiatives/sao-init-001-foundation/ complete/sao-init-001-foundation/`
4. **Update paths:** Change all `parent:` references to reflect new location
5. **Update dashboard:**
   - Move row from "Active Initiatives" to "Complete Initiatives"
   - Update summary counts: Complete +1, In Progress -1

### Example 3: Handling a Discovery

**Scenario:** While implementing WI-SAO-007, discovered that P-003 prevents orchestrator agents.

**Steps Executed:**

1. **Create discovery:** Append to `reference/discoveries.md`:
   ```markdown
   ### DISCOVERY-001: nse-orchestrator Architectural Misalignment
   - **Discovered:** 2026-01-11
   - **Severity:** CRITICAL
   - **Finding:** Orchestrator agents violate P-003 (no recursive nesting)
   - **Impact:** WI-SAO-005, WI-SAO-006 cannot be implemented
   - **Resolution:** Cancel both work items, use orchestration skill instead
   ```
2. **Cancel affected items:** Follow Section 4.4 for WI-SAO-005, WI-SAO-006
3. **Update dashboard:** Add to "Key Discoveries" section
4. **Notify user:** "Discovered DISCOVERY-001 that blocks WI-SAO-005/006"

---

## 14. Integration with CLAUDE.md

This SOP integrates with the root `CLAUDE.md` guidance:

- **P-002 (File Persistence):** All work tracker changes persist to files
- **P-010 (Task Tracking):** Work tracker is the SSOT for task state
- **Token Management:** Decomposed structure prevents context rot

**WHEN** starting a session:
1. Check `work/WORKTRACKER.md` for current focus
2. Read active work item file for context
3. Follow this SOP for all work tracker operations

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2026-01-11 | Major update based on best practices research: Added persona (§0), session management (§1), decision framework (§7), self-verification (§8), escalation protocol (§9), enhanced recovery (§10), anti-patterns (§11), worked examples (§13) |
| 1.0.0 | 2026-01-11 | Initial version |

---

*Version 2.0.0 - Updated 2026-01-11*
*Research basis: `research/worktracker-sop-best-practices-analysis.md`*
*This SOP should be updated when new operational patterns emerge.*
