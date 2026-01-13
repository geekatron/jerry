# PLAN: Multi-Project Support Cleanup

**ID**: PROJ-001-plugin-cleanup
**Status**: IN PROGRESS
**Author**: Claude (Distinguished Systems Engineer)
**Created**: 2026-01-09
**Branch**: cc/task-subtask

---

## Executive Summary

Refactor Jerry Framework to support isolated multi-project workspaces. Each project gets its own `PLAN.md` and `WORKTRACKER.md` in `projects/PROJ-{nnn}-{slug}/`, enabling clean context switching between concurrent work streams.

---

## 1. Problem Statement (5W1H Analysis)

### WHO is affected?
- Users managing multiple concurrent projects/initiatives
- Claude Code instances needing to switch context between work streams
- Future maintainers navigating project history

### WHAT problem are we solving?
- Single `docs/PLAN.md` and `docs/WORKTRACKER.md` creates confusion when switching projects
- Hard to archive completed projects without breaking references
- No clear project isolation or lifecycle management

### WHERE does the problem manifest?
- Root `docs/` folder becoming cluttered with mixed project artifacts
- References to PLAN.md/WORKTRACKER.md scattered across 11+ files
- Context rot when loading wrong project's state

### WHEN does it occur?
- When starting new initiatives while others are in progress
- When archiving completed work
- When resuming work after context compaction

### WHY does it matter?
- Clean context isolation directly addresses context rot
- Enables parallel project tracking
- Simplifies project lifecycle (create → work → archive)

### HOW will we solve it?
- New directory convention: `projects/PROJ-{nnn}-{slug}/`
- Environment variable `JERRY_PROJECT` for active project selection
- Update all 11 files referencing old paths
- Create projects registry in `projects/README.md`

---

## 2. Current State Analysis

### Files Requiring Updates (11 identified)

| File | Impact | References |
|------|--------|------------|
| `CLAUDE.md` | HIGH | Main instructions, `docs/plans/` |
| `.claude/settings.json` | HIGH | `PLAN.md`, `docs/plans/*.md` |
| `.claude/commands/architect.md` | HIGH | `docs/plans/PLAN_{slug}.md` |
| `.claude/agents/TEMPLATE.md` | MEDIUM | `docs/WORKTRACKER.md` |
| `docs/governance/JERRY_CONSTITUTION.md` | MEDIUM | `WORKTRACKER.md` |
| `docs/governance/BEHAVIOR_TESTS.md` | LOW | `WORKTRACKER.md` |
| `skills/problem-solving/docs/ORCHESTRATION.md` | MEDIUM | `WORKTRACKER.md` |
| `skills/problem-solving/agents/ps-reporter.md` | LOW | `WORKTRACKER.md` |
| `skills/worktracker/SKILL.md` | HIGH | `data/worktracker/` |

### Existing Structure
```
jerry/
├── docs/
│   ├── PLAN.md           # Was here (deleted/archived)
│   └── WORKTRACKER.md    # Was here (deleted/archived)
└── projects/
    └── archive/          # Already exists with old files
```

---

## 3. Proposed Solution

### Target Directory Structure
```
projects/
├── README.md                        # Projects registry
├── PROJ-001-plugin-cleanup/         # This project
│   ├── PLAN.md                      # Project plan
│   ├── WORKTRACKER.md               # Work tracking
│   └── .jerry/
│       └── data/
│           └── items/               # Future: work item JSON
└── archive/                         # Archived projects
    ├── PLAN.md
    └── WORKTRACKER.md
```

### Project ID Convention
- Format: `PROJ-{nnn}-{slug}`
- Example: `PROJ-001-plugin-cleanup`, `PROJ-002-task-subtask`
- Sequential numbering for ordering
- Slug for human readability

### Active Project Resolution
1. Check `JERRY_PROJECT` environment variable
2. If not set, prompt user to specify project
3. Resolve path: `projects/${JERRY_PROJECT}/`

### Path Variables
All references use consistent variable substitution:
- `${JERRY_PROJECT}` → Project ID (e.g., `PROJ-001-plugin-cleanup`)
- `projects/${JERRY_PROJECT}/PLAN.md` → Project plan
- `projects/${JERRY_PROJECT}/WORKTRACKER.md` → Work tracker

---

## 4. Implementation Steps

### Phase 1: Infrastructure Setup
- [x] SETUP-001: Create project directory structure
- [ ] SETUP-002: Create PLAN.md (this file)
- [ ] SETUP-003: Create WORKTRACKER.md
- [ ] SETUP-004: Create projects/README.md registry

### Phase 2: Core File Updates
- [ ] UPDATE-001: Update CLAUDE.md with new conventions
- [ ] UPDATE-002: Update .claude/settings.json
- [ ] UPDATE-003: Update .claude/commands/architect.md

### Phase 3: Agent/Skill Updates
- [ ] UPDATE-004: Update .claude/agents/TEMPLATE.md
- [ ] UPDATE-005: Update skills/worktracker/SKILL.md
- [ ] UPDATE-006: Update skills/problem-solving/docs/ORCHESTRATION.md
- [ ] UPDATE-007: Update skills/problem-solving/agents/ps-reporter.md

### Phase 4: Governance Updates
- [ ] UPDATE-008: Update docs/governance/JERRY_CONSTITUTION.md
- [ ] UPDATE-009: Update docs/governance/BEHAVIOR_TESTS.md

### Phase 5: Validation & Commit
- [ ] VALID-001: Verify all references updated
- [ ] VALID-002: Test environment variable detection
- [ ] COMMIT-001: Commit and push changes

---

## 5. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Missed reference | Medium | Medium | Grep verification before commit |
| Env var not set | High | Low | Prompt user when not detected |
| Archive link breakage | Low | Low | Archive is historical, no updates |

---

## 6. Success Criteria

- [ ] All 11 files updated with new path convention
- [ ] `JERRY_PROJECT` env var documented and functional
- [ ] projects/README.md serves as registry
- [ ] Can create new project with clean isolation
- [ ] Archived projects remain intact

---

## 7. References

- Jerry Framework: `CLAUDE.md`
- Archived work: `projects/archive/WORKTRACKER.md`
- Context Rot: [Chroma Research](https://research.trychroma.com/context-rot)

---

*Document Version: 1.0*
*Last Updated: 2026-01-09*
