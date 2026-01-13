# WORKTRACKER: PROJ-005-plugin-bugs

> **Project:** Plugin Installation Bugs
> **Status:** IN PROGRESS
> **Last Updated:** 2026-01-13T12:30:00Z

---

## Current State Summary

| Phase | Status | Progress |
|-------|--------|----------|
| PHASE-01: Project Setup | COMPLETED | 4/4 tasks |
| PHASE-02: Fix plugin.json | COMPLETED | 5/5 tasks |
| PHASE-03: Fix marketplace.json | COMPLETED | 4/4 tasks |
| PHASE-04: Verification | IN PROGRESS | 0/2 tasks |

---

## PHASE-01: Project Setup

**Status:** COMPLETED
**Started:** 2026-01-13
**Completed:** 2026-01-13

### Task 1.1: Create project directory structure

**Status:** COMPLETED
**Completed:** 2026-01-13

#### Work Done
- Created `projects/PROJ-005-plugin-bugs/` directory
- Created `.jerry/data/items/` subdirectory for work item state

#### Evidence
- Command executed: `mkdir -p projects/PROJ-005-plugin-bugs/.jerry/data/items`
- Verification: Directory exists at expected path

---

### Task 1.2: Create PLAN.md

**Status:** COMPLETED
**Completed:** 2026-01-13

#### Work Done
- Created comprehensive PLAN.md with:
  - Project overview and problem statement
  - Phase breakdown
  - Evidence sources with Context7 references
  - Success criteria

#### Evidence
- File created: `projects/PROJ-005-plugin-bugs/PLAN.md`

---

### Task 1.3: Create WORKTRACKER.md

**Status:** COMPLETED
**Completed:** 2026-01-13

#### Work Done
- Created detailed WORKTRACKER.md with:
  - Phase and task breakdowns
  - Evidence tables with citations
  - Bugs & Discoveries log
  - Technical Debt log
  - Change log

#### Evidence
- File created: `projects/PROJ-005-plugin-bugs/WORKTRACKER.md`

---

### Task 1.4: Update projects/README.md registry

**Status:** COMPLETED
**Completed:** 2026-01-13

#### Work Done
- Added PROJ-005-plugin-bugs to Active Projects table
- Recorded branch as `cc/jerry-plugin-bugs`
- Set status to IN PROGRESS

#### Acceptance Criteria
- [x] PROJ-005-plugin-bugs added to Active Projects table
- [x] Branch name recorded as `cc/jerry-plugin-bugs`
- [x] Status set to IN PROGRESS

#### Evidence
- File modified: `projects/README.md` line 14
- Entry: `| PROJ-005-plugin-bugs | Plugin Installation Bugs | 🔄 IN PROGRESS | cc/jerry-plugin-bugs | 2026-01-13 |`

---

## PHASE-02: Fix plugin.json

**Status:** COMPLETED
**Started:** 2026-01-13
**Completed:** 2026-01-13

### Task 2.1: Remove unrecognized keys

**Status:** COMPLETED

#### Work Done
Removed 6 invalid fields from plugin.json:
- `$schema`
- `engines`
- `main`
- `configuration`
- `dependencies`
- `capabilities`

#### Evidence

| Source | Reference | Citation |
|--------|-----------|----------|
| Error Message | Installation output | `Unrecognized keys: "$schema", "engines", "main", "configuration", "dependencies", "capabilities"` |
| Context7 | manifest-reference.md | "Complete Plugin Configuration" example shows only: name, version, description, author, homepage, repository, license, keywords, commands, agents, hooks, mcpServers |

---

### Task 2.2: Fix skills format

**Status:** COMPLETED

#### Work Done
Changed skills from array of SKILL.md file paths to directory path:

**Before:**
```json
"skills": [
  "skills/worktracker/SKILL.md",
  "skills/architecture/SKILL.md",
  "skills/problem-solving/SKILL.md"
]
```

**After:**
```json
"skills": "./skills/"
```

#### Evidence

| Source | Reference | Citation |
|--------|-----------|----------|
| Context7 | skill-development/SKILL.md | "Skills are auto-discovered from the skills/ directory and do not require separate packaging" |
| Context7 | plugin-structure/SKILL.md | "Path rules require them to be relative to the plugin root, start with `./`" |
| Error Message | Installation output | `skills: Invalid input` (value format wrong, not unrecognized key) |

---

### Task 2.3: Fix commands path format

**Status:** COMPLETED

#### Work Done
Added `./` prefix to command paths:

**Before:**
```json
"commands": [
  "commands/architect.md",
  "commands/release.md"
]
```

**After:**
```json
"commands": [
  "./commands/architect.md",
  "./commands/release.md"
]
```

#### Evidence

| Source | Reference | Citation |
|--------|-----------|----------|
| Context7 | manifest-reference.md | "All paths must be relative with the `./` prefix" |
| Context7 | manifest-reference.md | "Fix Missing ./ Prefix in Plugin Path" - explicit correction example |

---

### Task 2.4: Fix hooks path format

**Status:** COMPLETED

#### Work Done
Added `./` prefix to hooks path:

**Before:**
```json
"hooks": "hooks/hooks.json"
```

**After:**
```json
"hooks": "./hooks/hooks.json"
```

#### Evidence

| Source | Reference | Citation |
|--------|-----------|----------|
| Context7 | manifest-reference.md | Example shows `"hooks": "./config/hooks.json"` with ./ prefix |
| Context7 | manifest-reference.md | "Fix Missing ./ Prefix" example: `"hooks": "hooks/hooks.json"` → `"hooks": "./hooks/hooks.json"` |

---

### Task 2.5: Verify final plugin.json

**Status:** COMPLETED

#### Final State
```json
{
  "name": "jerry",
  "version": "0.1.0",
  "description": "Framework for behavior and workflow guardrails with knowledge accrual",
  "author": {
    "name": "Jerry Framework Contributors",
    "url": "https://github.com/geekatron/jerry"
  },
  "license": "MIT",
  "repository": "https://github.com/geekatron/jerry",
  "keywords": ["jerry", "workflow", "guardrails", "knowledge-management", "problem-solving", "work-tracker", "hexagonal-architecture"],
  "skills": "./skills/",
  "commands": ["./commands/architect.md", "./commands/release.md"],
  "hooks": "./hooks/hooks.json"
}
```

#### Validation
- [x] Only recognized fields present
- [x] All paths use ./ prefix
- [x] Skills uses directory path format
- [x] JSON is valid

---

## PHASE-03: Fix marketplace.json

**Status:** COMPLETED
**Started:** 2026-01-13
**Completed:** 2026-01-13

### Task 3.1: Remove invalid 'skills' field

**Status:** COMPLETED
**Completed:** 2026-01-13

#### Work Done
Removed `skills` array from plugin entry in marketplace.json.

**Before:**
```json
{
  "name": "jerry-framework",
  "description": "...",
  "source": "./",
  "strict": false,
  "version": "0.1.0",
  "skills": [
    "skills/worktracker/SKILL.md",
    "skills/architecture/SKILL.md",
    "skills/problem-solving/SKILL.md"
  ]
}
```

**After:**
```json
{
  "name": "jerry-framework",
  "description": "...",
  "source": "./",
  "version": "0.1.0",
  "category": "productivity"
}
```

#### Acceptance Criteria
- [x] `skills` array removed from plugin entry
- [x] No validation errors related to skills field

#### Evidence

| Source | Reference | Citation |
|--------|-----------|----------|
| Context7 | "Configure Plugin Marketplace with JSON Schema" | Plugin entries show: name, description, source, category, version, author - NO skills field |
| Architectural Principle | Separation of Concerns | Marketplace defines WHERE plugins are; plugin.json defines WHAT plugins contain |

---

### Task 3.2: Remove invalid 'strict' field

**Status:** COMPLETED
**Completed:** 2026-01-13

#### Work Done
Removed `strict` field from plugin entry.

#### Acceptance Criteria
- [x] `strict` field removed from plugin entry
- [x] No validation warnings about unrecognized fields

#### Evidence

| Source | Reference | Citation |
|--------|-----------|----------|
| Context7 | All marketplace examples | No `strict` field shown in any marketplace plugin entry |
| Context7 | "Configure Plugin Marketplace with JSON Schema" | Complete example shows only: name, description, source, category, version, author |

---

### Task 3.3: Fix email typo

**Status:** COMPLETED
**Completed:** 2026-01-13

#### Work Done
Corrected email from `geekatron@gmial.com` to `geekatron@gmail.com`.

**Before:**
```json
"owner": {
  "name": "geekatron",
  "email": "geekatron@gmial.com"
}
```

**After:**
```json
"owner": {
  "name": "geekatron",
  "email": "geekatron@gmail.com"
}
```

#### Acceptance Criteria
- [x] Email corrected from `geekatron@gmial.com` to `geekatron@gmail.com`

#### Evidence
- Visual inspection: "gmial" is a typo of "gmail"
- Standard email domain validation: gmail.com is valid, gmial.com is not a standard provider

---

### Task 3.4: Add marketplace metadata

**Status:** COMPLETED
**Completed:** 2026-01-13

#### Work Done
Added recommended metadata fields:
- `version`: "1.0.0" at marketplace level
- `description`: "Local plugin marketplace for Jerry framework development" at marketplace level
- `category`: "productivity" on plugin entry

**Before:**
```json
{
  "name": "saucer-boy",
  "owner": { ... },
  "plugins": [ ... ]
}
```

**After:**
```json
{
  "name": "saucer-boy",
  "version": "1.0.0",
  "description": "Local plugin marketplace for Jerry framework development",
  "owner": { ... },
  "plugins": [
    {
      "name": "jerry-framework",
      "description": "...",
      "source": "./",
      "version": "0.1.0",
      "category": "productivity"
    }
  ]
}
```

#### Acceptance Criteria
- [x] `version` field added at marketplace level
- [x] `description` field added at marketplace level
- [x] `category` field added to plugin entry

#### Evidence

| Source | Reference | Citation |
|--------|-----------|----------|
| Context7 | Marketplace schema example | Shows `"version": "1.0.0"`, `"description": "Collection of custom plugins"` at top level |
| Context7 | Plugin entry example | Shows `"category": "development"` and `"category": "productivity"` as valid values |

---

### Task 3.5: Verify final marketplace.json

**Status:** COMPLETED
**Completed:** 2026-01-13

#### Final State
```json
{
  "name": "saucer-boy",
  "version": "1.0.0",
  "description": "Local plugin marketplace for Jerry framework development",
  "owner": {
    "name": "geekatron",
    "email": "geekatron@gmail.com"
  },
  "plugins": [
    {
      "name": "jerry-framework",
      "description": "Adds problem solving capabilities with behavior and workflow guardrails, knowledge accrual, and work tracking.",
      "source": "./",
      "version": "0.1.0",
      "category": "productivity"
    }
  ]
}
```

#### Validation
- [x] Only documented fields present in plugin entry
- [x] Email corrected
- [x] Marketplace metadata added
- [x] JSON is valid

---

## PHASE-04: Verification & Testing

**Status:** IN PROGRESS
**Started:** 2026-01-13

### Task 4.1: Test plugin installation

**Status:** PENDING

#### Acceptance Criteria
- [ ] Plugin installs without errors
- [ ] No validation warnings

#### Instructions for User
Please attempt plugin installation again in the target repository using the local marketplace strategy. Report any errors or success.

---

### Task 4.2: Verify component discovery

**Status:** PENDING

#### Acceptance Criteria
- [ ] Skills discovered: worktracker, architecture, problem-solving, worktracker-decomposition
- [ ] Commands discovered: architect, release
- [ ] Hooks registered: SessionStart, PreToolUse, Stop

---

## Bugs & Discoveries Log

| ID | Type | Description | Status | Phase |
|----|------|-------------|--------|-------|
| BUG-001 | Bug | plugin.json had 6 unrecognized fields | FIXED | PHASE-02 |
| BUG-002 | Bug | plugin.json paths missing ./ prefix | FIXED | PHASE-02 |
| BUG-003 | Bug | plugin.json skills used file paths instead of directory | FIXED | PHASE-02 |
| BUG-004 | Bug | marketplace.json has invalid 'skills' field | FIXED | PHASE-03 |
| BUG-005 | Bug | marketplace.json has invalid 'strict' field | FIXED | PHASE-03 |
| BUG-006 | Bug | marketplace.json email typo (gmial) | FIXED | PHASE-03 |
| DISC-001 | Discovery | skills field in plugin.json IS valid (not unrecognized) but needs directory format | NOTED | PHASE-02 |
| DISC-002 | Discovery | marketplace.json plugin entries have different schema than plugin.json - do NOT duplicate fields | NOTED | PHASE-03 |

---

## Technical Debt Log

| ID | Description | Priority | Phase |
|----|-------------|----------|-------|
| TD-001 | Consider adding $schema for IDE support once official schema URL confirmed | LOW | Future |
| TD-002 | Document plugin.json vs marketplace.json field differences | MEDIUM | Future |
| TD-003 | Create validation script to check plugin/marketplace configs before installation | MEDIUM | Future |

---

## Change Log

| Date | Phase | Task | Change | Author |
|------|-------|------|--------|--------|
| 2026-01-13 | PHASE-03 | 3.1-3.5 | Fixed marketplace.json - removed invalid fields, fixed email, added metadata | Claude |
| 2026-01-13 | PHASE-01 | 1.4 | Added PROJ-005-plugin-bugs to projects/README.md registry | Claude |
| 2026-01-13 | PHASE-02 | 2.1-2.5 | Fixed plugin.json - removed invalid fields, fixed paths | Claude |
| 2026-01-13 | PHASE-01 | 1.1-1.3 | Created project structure, PLAN.md, WORKTRACKER.md | Claude |
