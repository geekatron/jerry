# Quick Reference Checklists

> **Purpose:** Action checklists for common ECW operations
> **Usage:** Reference before/during/after specific activities

---

## Before Writing Code (Rule 9 - TDD)

- [ ] Task exists in `docs/proposals/`?
- [ ] Contract exists in `docs/contracts/`?
- [ ] Plan Mode used for complex work?
- [ ] **Test written FIRST and failing? (RED)**

---

## When Uncertain

- [ ] Log assumption to `docs/knowledge/assumptions.md`?
- [ ] ASK clarifying question?

---

## After Significant Debugging (Rule 10 - Lessons)

- [ ] Debugging >30 min? → Log to `docs/knowledge/lessons.md`
- [ ] Backtrack/retry? → Consider capturing lesson
- [ ] User correction? → Consider capturing lesson

---

## After Completing Work

- [ ] Tests passing? (GREEN → REFACTOR)
- [ ] Update task status in `docs/proposals/`
- [ ] Run `/checkpoint` or say "save checkpoint"

---

## After Completing a Phase (LES-011)

- [ ] All tasks marked done in proposal?
- [ ] Git commit exists with deliverables?
- [ ] Run `/phase-complete N` or say "mark phase N complete"
- [ ] Create checkpoint with phase name

---

## Before Creating a New Phase Proposal (Rule 14 + Rule 15)

- [ ] Check: `ls docs/proposals/phase-NN-*` - no existing file with that number
- [ ] Check `docs/proposals/_index.md` for allocated phase numbers
- [ ] If collision: use next available number
- [ ] **Hook will BLOCK (not warn) on collision** (LES-020)
- [ ] Header block includes: Status, Created, Priority, ECW Version, Session
- [ ] If from Plan Mode: transform plan content before saving (use `plan_to_proposal.py`)

### Proposal Header Template (LES-013)

```markdown
# Phase NN: Title

> **Status:** Proposed | In Progress | Complete
> **Created:** YYYY-MM-DD
> **Completed:** YYYY-MM-DD (if complete)
> **Commit:** `hash` (if complete)
> **Priority:** Low | Medium | High | BLOCKING
> **ECW Version:** v2.X.X
> **Session:** {session-id}
```

---

## Before ANY Code Changes (Rule 13 - LES-009)

- [ ] On a feature branch? `git branch --show-current`
- [ ] If on main: `git checkout -b feature/your-feature`
- [ ] Never push directly to main - always use PR

---

## Before First Commit in Session (LES-008)

- [ ] Git email set? `git config user.email`
- [ ] Email is repo-specific? `git config --local user.email`
- [ ] If not set: `git config user.email "your-email@example.com"`

---

## When Implementing File-Creating Automation (LES-016, PAT-039)

- [ ] What commits this file? (auto-commit / manual / checkpoint)
- [ ] Is the path in `.gitignore`? (intentional or accidental?)
- [ ] End-to-end test: create → commit → reset → file survives?
- [ ] Stop hook warns if uncommitted? (add path to IMPORTANT_PATHS in stop.sh)

---

## Before Implementing Features with External Dependencies (Rules 20-22)

### Rule 20: Architectural Feasibility Review

- [ ] Can execution context access required dependencies?
- [ ] Draw data flow diagram showing process boundaries
- [ ] Identify dependency access requirements (MCP, network, filesystem, etc.)
- [ ] Verify execution context can satisfy dependencies
- [ ] If uncertain, build proof-of-concept FIRST

**Context Access Examples:**
- ❌ Hook needs MCP access → Hooks run as subprocesses (no MCP context)
- ❌ Hook needs database connection → May not have credentials in hook context
- ✅ Hook uses filesystem → Always available to subprocess
- ✅ Hook uses git commands → Available if in git repo

### Rule 21: E2E Tests Required for Integration

- [ ] E2E test proves X actually calls feature
- [ ] Test runs in production-like environment (not mocked)
- [ ] Test validates expected outcome occurs
- [ ] No mocks for critical path validation

**Anti-pattern:**
```
Unit tests with mocks ≠ integration works
"Integrated into notification hook" without E2E test = Phase 32.G failure
```

**Required for "integrated" claims:**
```gherkin
Given real hook script (not mocked)
When hook fires in production environment
Then expected side effects occur
And no mocks used for critical path
```

### Rule 22: Integration Claims Require Execution Proof

- [ ] File/function that calls the integration exists
- [ ] E2E test shows integration executes
- [ ] Manual test confirms integration fires
- [ ] `git grep` shows integration referenced in X's code

**Evidence required before commit:**
- Hook file exists: `ls .claude/hooks/X.sh`
- Hook registered: `grep X .claude/settings.json`
- Integration called: `grep -r "integration_function" .claude/hooks/X.sh`
- E2E test passes: `pytest tests/integration/test_X_integration.py`

---

## Lesson from Phase 32.G (LES-030)

> "Integrated auto-checkpoint into notification hook" commit, but notification hook doesn't call auto-checkpoint AND can't access MCP anyway (architectural impossibility). Tests passed via mocks. Feature never worked.

**Prevention:**
- "Integrated" means "X calls Y and it works" (verified via E2E test)
- NOT "Y exists and could be called" (unit tests with mocks)
