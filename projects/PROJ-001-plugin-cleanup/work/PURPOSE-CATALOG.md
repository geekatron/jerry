# PURPOSE-CATALOG: Work Folder File Registry

> **ID**: PURPOSE-CATALOG
> **Version**: 1.0
> **Created**: 2026-01-11
> **Author**: Claude Opus 4.5
> **Source**: DOC-001-synthesis, Section 6.2

---

## Purpose

This catalog documents **why each file exists** in the `work/` folder structure. It serves as a reference for:
- Understanding the decomposed WORKTRACKER architecture
- Creating new files with correct naming and purpose
- Onboarding new agents or sessions

---

## Navigation

| Link | Description |
|------|-------------|
| [<- WORKTRACKER](../WORKTRACKER.md) | Back to navigation hub |
| [RUNBOOK-002](../runbooks/RUNBOOK-002-worktracker-decomposition.md) | Decomposition runbook |

---

## File Type Taxonomy

### 1. Navigation Hub

| File | Purpose | When Created | Owner |
|------|---------|--------------|-------|
| `../WORKTRACKER.md` | Navigation hub and session resume point. Contains status dashboard, navigation graph, and resume protocol. Target: <150 lines. | Project start | Project Lead |

### 2. Sequential Phase Files

| Pattern | Purpose | When Created | Owner |
|---------|---------|--------------|-------|
| `PHASE-{NN}-{NAME}.md` | Track work for numbered project phases. Contains task summaries, detailed breakdowns, session context, and document history. | During decomposition | Phase Owner |

**Current Files**:

| File | Phase | Status | Purpose |
|------|-------|--------|---------|
| `PHASE-01-INFRASTRUCTURE.md` | Phase 1 | DONE | Infrastructure setup (directory structure, CLAUDE.md) |
| `PHASE-02-CORE-UPDATES.md` | Phase 2 | DONE | Core file updates (prompts, skills, rules) |
| `PHASE-03-AGENT-UPDATES.md` | Phase 3 | DONE | Agent configuration updates |
| `PHASE-04-GOVERNANCE.md` | Phase 4 | DONE | Governance documents (Jerry Constitution) |
| `PHASE-05-VALIDATION.md` | Phase 5 | DONE | Validation (behavior tests, health checks) |
| `PHASE-06-ENFORCEMENT.md` | Phase 6 | IN PROGRESS | Enforcement mechanisms and automation |
| `PHASE-07-DESIGN-SYNTHESIS.md` | Phase 7 | DONE | Design synthesis and documentation archaeology |

### 3. Cross-Cutting Category Files

| Pattern | Purpose | When Created | Owner |
|---------|---------|--------------|-------|
| `PHASE-{CATEGORY}.md` | Track items that span multiple phases. Categories are not numbered because they exist outside the sequential flow. | As needed | All Agents |

**Current Files**:

| File | Category | Purpose |
|------|----------|---------|
| `PHASE-BUGS.md` | BUGS | Track bugs discovered during development. Includes severity, source phase, and resolution status. |
| `PHASE-TECHDEBT.md` | TECHDEBT | Track technical debt identified during development. Includes priority, impact assessment, and remediation plan. |
| `PHASE-DISCOVERY.md` | DISCOVERY | Track discoveries and insights that emerge during work. Includes source context and applicability notes. |

### 4. Initiative Files

| Pattern | Purpose | When Created | Owner |
|---------|---------|--------------|-------|
| `INITIATIVE-{NAME}.md` | Complex multi-phase orchestration for work that spans multiple phases or requires its own lifecycle management. | For large initiatives | Initiative Lead |

**Current Files**:

| File | Initiative | Purpose |
|------|------------|---------|
| `INITIATIVE-DEV-SKILL.md` | DEV-SKILL | Tracks the development of Jerry skills (like worktracker-decomposition). Contains skill specification, implementation tasks, and validation criteria. |

### 5. Implementation Domain Files

| Pattern | Purpose | When Created | Owner |
|---------|---------|--------------|-------|
| `PHASE-IMPL-{DOMAIN}.md` | Detailed implementation tasks for a specific domain or subsystem. Used when implementation complexity warrants dedicated tracking. | During implementation phases | Implementor |

**Current Files**:

| File | Domain | Purpose |
|------|--------|---------|
| `PHASE-IMPL-DOMAIN.md` | DOMAIN | Tracks domain layer implementation (value objects, entities, aggregates) with detailed subtask breakdowns. |

---

## Naming Conventions

### Task ID Patterns

| ID Pattern | Example | Usage |
|------------|---------|-------|
| `{PREFIX}-{NNN}` | `SETUP-001` | Phase-level tasks (top-level work items) |
| `{PREFIX}-{NNN}.{N}` | `008d.1` | Subtasks (first-level breakdown) |
| `{PREFIX}-{NNN}.{N}.{N}` | `008d.1.1` | Sub-subtasks (detailed breakdown) |

### Work Phase Prefixes

| Prefix | Meaning | Example |
|--------|---------|---------|
| `R-` | Research phase | `R-008d.0` (Research before implementation) |
| `I-` | Implementation phase | `I-008d.1` (Core implementation) |
| `T-` | Test phase | `T-008d.1.3` (Testing a specific component) |
| `E-` | Evidence phase | `E-008d` (Validation evidence collection) |

### File Naming Rules

1. **Use kebab-case** for multi-word names: `PHASE-06-ENFORCEMENT.md`
2. **Two-digit phase numbers** for sorting: `PHASE-01`, `PHASE-02`, ... `PHASE-10`
3. **Category names are ALL CAPS**: `PHASE-BUGS.md`, `PHASE-TECHDEBT.md`
4. **Initiative names use descriptive slugs**: `INITIATIVE-DEV-SKILL.md`
5. **Implementation domains are singular**: `PHASE-IMPL-DOMAIN.md` (not `DOMAINS`)

---

## File Structure Templates

### Sequential Phase File

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
{Resume instructions}

### Key Files to Know
| File | Purpose |
|------|---------|

---

## Document History

| Date | Author | Changes |
|------|--------|---------|
```

### Cross-Cutting Category File

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
```

---

## When to Create New Files

### Create a New Phase File When:
- A new numbered phase is added to the project
- Decomposing an existing monolithic WORKTRACKER

### Create a New Category File When:
- A new cross-cutting concern emerges (e.g., SECURITY, PERFORMANCE)
- The existing category files don't fit the item type

### Create a New Initiative File When:
- Work spans multiple phases
- The initiative has its own lifecycle independent of phases
- Complexity warrants dedicated orchestration

### Create a New Implementation File When:
- Implementation requires >20 subtasks
- A specific domain/subsystem needs detailed tracking
- Parallel implementors need isolated work areas

---

## Maintenance Guidelines

### Adding Items to Existing Files
1. Add new task to the relevant phase/category file
2. Update the summary table at the top of the file
3. Update WORKTRACKER.md dashboard if status changes

### Archiving Completed Phases
1. Reduce completed task details to summaries
2. Keep task IDs and outputs for reference
3. Move detailed notes to `/reports/` or `/synthesis/`

### Updating This Catalog
1. Add new files as they are created
2. Update status when phases complete
3. Add new patterns as they emerge

---

## References

- **Source**: `projects/PROJ-001-plugin-cleanup/synthesis/DOC-001-synthesis.md`
- **Runbook**: `projects/PROJ-001-plugin-cleanup/runbooks/RUNBOOK-002-worktracker-decomposition.md`
- **Pattern Origin**: Commit `4882948` in PROJ-001

---

## Document History

| Date | Version | Author | Changes |
|------|---------|--------|---------|
| 2026-01-11 | 1.0 | Claude Opus 4.5 | Initial catalog created from DOC-001 synthesis |
