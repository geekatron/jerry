# Phase 3: Agent/Skill Updates

> **Status**: ✅ COMPLETED (100%)
> **Goal**: Update agent and skill definitions for project isolation

---

## Navigation

| Link | Description |
|------|-------------|
| [← WORKTRACKER](../WORKTRACKER.md) | Back to index |
| [← Phase 2](PHASE-02-CORE-UPDATES.md) | Previous phase |
| [Phase 4 →](PHASE-04-GOVERNANCE.md) | Next phase |

---

## Task Summary

| Task ID | Title | Status | Subtasks | Files Changed |
|---------|-------|--------|----------|---------------|
| UPDATE-004 | Update agents/TEMPLATE.md | ✅ DONE | 2/2 | `.claude/agents/TEMPLATE.md` |
| UPDATE-005 | Update worktracker SKILL.md | ✅ DONE | 3/3 | `skills/worktracker/SKILL.md` |
| UPDATE-006 | Update ORCHESTRATION.md | ✅ DONE | 1/1 | `skills/problem-solving/docs/ORCHESTRATION.md` |
| UPDATE-007 | Update ps-reporter.md | ✅ DONE | 2/2 | `skills/problem-solving/agents/ps-reporter.md` |

---

## UPDATE-004: Update .claude/agents/TEMPLATE.md ✅

> **Status**: COMPLETED
> **File**: `.claude/agents/TEMPLATE.md`

### Subtasks

| ID | Task | Status | Change |
|----|------|--------|--------|
| 004.1 | Update WORKTRACKER.md path reference | ✅ | `projects/${JERRY_PROJECT}/WORKTRACKER.md` |
| 004.2 | Update Integration Points section | ✅ | Project-centric paths |

### Changes Made

```markdown
# Before
Integration Points:
- WORKTRACKER.md: docs/WORKTRACKER.md

# After
Integration Points:
- WORKTRACKER.md: projects/${JERRY_PROJECT}/WORKTRACKER.md
```

### Acceptance Criteria

- [x] WORKTRACKER path updated
- [x] Integration points documented
- [x] Template usable for new agents

---

## UPDATE-005: Update skills/worktracker/SKILL.md ✅

> **Status**: COMPLETED
> **File**: `skills/worktracker/SKILL.md`

### Subtasks

| ID | Task | Status | Change |
|----|------|--------|--------|
| 005.1 | Update Storage section paths | ✅ | Project-relative storage |
| 005.2 | Add project context to commands | ✅ | Commands reference project |
| 005.3 | Update data directory reference | ✅ | `.jerry/data/items/` |

### Changes Made

```markdown
# Storage Section
## Before
Storage: docs/WORKTRACKER.md
Data: .jerry/data/items/

## After
Storage: projects/${JERRY_PROJECT}/WORKTRACKER.md
Data: projects/${JERRY_PROJECT}/.jerry/data/items/
```

### Commands Updated

| Command | Change |
|---------|--------|
| `list` | Lists items from active project |
| `add` | Adds to active project |
| `complete` | Updates active project tracker |

### Acceptance Criteria

- [x] Storage paths updated
- [x] Commands reference project
- [x] Data directory correct

---

## UPDATE-006: Update ORCHESTRATION.md ✅

> **Status**: COMPLETED
> **File**: `skills/problem-solving/docs/ORCHESTRATION.md`

### Subtasks

| ID | Task | Status | Change |
|----|------|--------|--------|
| 006.1 | Update WORKTRACKER.md reference | ✅ | Project-relative path |

### Changes Made

```markdown
# Before
Agents update: docs/WORKTRACKER.md

# After
Agents update: projects/${JERRY_PROJECT}/WORKTRACKER.md
```

### Acceptance Criteria

- [x] WORKTRACKER reference updated
- [x] Diagram accurate

---

## UPDATE-007: Update ps-reporter.md ✅

> **Status**: COMPLETED
> **File**: `skills/problem-solving/agents/ps-reporter.md`

### Subtasks

| ID | Task | Status | Change |
|----|------|--------|--------|
| 007.1 | Update WORKTRACKER.md grep example | ✅ | New path in example |
| 007.2 | Update task status query reference | ✅ | Project-relative query |

### Changes Made

```bash
# Before
grep "IN PROGRESS" docs/WORKTRACKER.md

# After
grep "IN PROGRESS" projects/${JERRY_PROJECT}/WORKTRACKER.md
```

### Acceptance Criteria

- [x] Grep example updated
- [x] Query references updated
- [x] Examples work with new structure

---

## Phase Completion Evidence

| File | Changes | Verification |
|------|---------|--------------|
| `.claude/agents/TEMPLATE.md` | Path updates | Integration points correct |
| `skills/worktracker/SKILL.md` | Storage paths | Commands work |
| `skills/problem-solving/docs/ORCHESTRATION.md` | Reference | Diagram accurate |
| `skills/problem-solving/agents/ps-reporter.md` | Examples | Grep works |

---

## Session Context

### For Resuming Work

If resuming after this phase:
1. Phase 3 is complete - no remaining work
2. Proceed to [Phase 4: Governance Updates](PHASE-04-GOVERNANCE.md)
3. All agents/skills now support project isolation

### Key Changes to Know

| Component | Change |
|-----------|--------|
| Agent template | Uses project paths |
| Worktracker skill | Scoped to active project |
| PS agents | Output to project directories |
| Reporter | Queries project WORKTRACKER |

---

## Document History

| Date | Author | Changes |
|------|--------|---------|
| 2026-01-09 | Claude | Initial completion |
| 2026-01-09 | Claude | Added detailed task breakdowns |
