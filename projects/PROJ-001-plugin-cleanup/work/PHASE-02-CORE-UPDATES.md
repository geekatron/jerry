# Phase 2: Core File Updates

> **Status**: ✅ COMPLETED (100%)
> **Goal**: Update core configuration files for multi-project support

---

## Navigation

| Link | Description |
|------|-------------|
| [← WORKTRACKER](../WORKTRACKER.md) | Back to index |
| [← Phase 1](PHASE-01-INFRASTRUCTURE.md) | Previous phase |
| [Phase 3 →](PHASE-03-AGENT-UPDATES.md) | Next phase |

---

## Task Summary

| Task ID | Title | Status | Subtasks | Files Changed |
|---------|-------|--------|----------|---------------|
| UPDATE-001 | Update CLAUDE.md | ✅ DONE | 4/4 | `CLAUDE.md` |
| UPDATE-002 | Update .claude/settings.json | ✅ DONE | 2/2 | `.claude/settings.json` |
| UPDATE-003 | Update architect.md | ✅ DONE | 3/3 | `.claude/commands/architect.md` |

---

## UPDATE-001: Update CLAUDE.md ✅

> **Status**: COMPLETED
> **File**: `CLAUDE.md`

### Subtasks

| ID | Task | Status | Change |
|----|------|--------|--------|
| 001.1 | Update "Working with Jerry" section | ✅ | Added project-based workflow |
| 001.2 | Add JERRY_PROJECT environment variable docs | ✅ | New section |
| 001.3 | Update path references to projects/ convention | ✅ | Changed `docs/PLAN.md` → `projects/${JERRY_PROJECT}/PLAN.md` |
| 001.4 | Add project lifecycle instructions | ✅ | Create/activate/archive docs |

### Changes Made

```diff
# Before
- PLAN.md located at docs/PLAN.md
- WORKTRACKER.md located at docs/WORKTRACKER.md

# After
+ PLAN.md located at projects/${JERRY_PROJECT}/PLAN.md
+ WORKTRACKER.md located at projects/${JERRY_PROJECT}/WORKTRACKER.md
+ JERRY_PROJECT environment variable required
```

### Sections Updated

| Section | Change |
|---------|--------|
| Working with Jerry | Added project-based workflow |
| Before Starting Work | Added JERRY_PROJECT check |
| During Work | Updated path references |
| Creating a New Project | New section added |

### Acceptance Criteria

- [x] JERRY_PROJECT documented
- [x] Path references updated
- [x] Project lifecycle documented
- [x] No broken references

---

## UPDATE-002: Update .claude/settings.json ✅

> **Status**: COMPLETED
> **File**: `.claude/settings.json`

### Subtasks

| ID | Task | Status | Change |
|----|------|--------|--------|
| 002.1 | Update `context.load_on_demand` paths | ✅ | Project-relative paths |
| 002.2 | Update command description for architect | ✅ | Reflects new behavior |

### Changes Made

```json
{
  "context": {
    "load_on_demand": [
      "projects/${JERRY_PROJECT}/PLAN.md",
      "projects/${JERRY_PROJECT}/WORKTRACKER.md"
    ]
  }
}
```

### Acceptance Criteria

- [x] Paths use project-relative format
- [x] Settings file is valid JSON
- [x] Command descriptions accurate

---

## UPDATE-003: Update .claude/commands/architect.md ✅

> **Status**: COMPLETED
> **File**: `.claude/commands/architect.md`

### Subtasks

| ID | Task | Status | Change |
|----|------|--------|--------|
| 003.1 | Update PLAN file creation path | ✅ | `projects/${JERRY_PROJECT}/PLAN.md` |
| 003.2 | Add JERRY_PROJECT resolution logic | ✅ | Check env var, prompt if missing |
| 003.3 | Update examples | ✅ | Show new path convention |

### Changes Made

```markdown
# Before
Create PLAN.md at docs/PLAN.md

# After
1. Check JERRY_PROJECT environment variable
2. If not set, prompt user to select or create project
3. Create PLAN.md at projects/${JERRY_PROJECT}/PLAN.md
```

### JERRY_PROJECT Resolution Logic

```
1. Check JERRY_PROJECT env var
   │
   ├── Set? → Use that project
   │
   └── Not set? → Prompt user
       │
       ├── Select existing project
       └── Create new project (auto-generate ID)
```

### Acceptance Criteria

- [x] PLAN path uses project convention
- [x] JERRY_PROJECT resolution documented
- [x] Examples updated
- [x] Prompt message included

---

## Phase Completion Evidence

| File | Changes | Verification |
|------|---------|--------------|
| `CLAUDE.md` | +50 lines | `grep 'JERRY_PROJECT' CLAUDE.md` |
| `.claude/settings.json` | Path updates | JSON valid |
| `.claude/commands/architect.md` | +30 lines | Examples updated |

---

## Session Context

### For Resuming Work

If resuming after this phase:
1. Phase 2 is complete - no remaining work
2. Proceed to [Phase 3: Agent/Skill Updates](PHASE-03-AGENT-UPDATES.md)
3. Core files now support project isolation

### Key Changes to Know

| Change | Impact |
|--------|--------|
| JERRY_PROJECT required | Must set env var before work |
| Paths changed | All refs use `projects/${JERRY_PROJECT}/` |
| Architect updated | Creates PLAN in project dir |

---

## Document History

| Date | Author | Changes |
|------|--------|---------|
| 2026-01-09 | Claude | Initial completion |
| 2026-01-09 | Claude | Added detailed task breakdowns |
