# Hard Rules - Full Reference

> **Purpose:** Behavioral gates that MUST be satisfied before proceeding
> **Enforcement:** Hooks actively block violations (Phase 34)

---

## Rule Details

### Rule 1: Code Requires Task
- **Gate:** Before writing code
- **Check:** Task exists in `docs/proposals/`
- **Enforcement:** PreToolUse hook blocks Edit/Write without task

### Rule 2: Task Requires Contract
- **Gate:** Before adding task
- **Check:** Contract exists in `docs/contracts/`
- **Rationale:** Tasks trace to contracts for alignment

### Rule 3: Phase Requires Approval
- **Gate:** Before starting phase
- **Check:** User said "approved" or "go ahead"
- **Rationale:** Prevents premature implementation

### Rule 4: Uncertainty Requires Questions
- **Gate:** When unclear
- **Check:** ASK, don't guess
- **Rationale:** Better to clarify than assume

### Rule 5: Complex Work Requires Planning
- **Gate:** Before multi-step work
- **Check:** Enter Plan Mode
- **Rationale:** Prevents unstructured changes

### Rule 6: Assumptions Require Logging
- **Gate:** When assuming
- **Check:** Log to `docs/knowledge/assumptions.md`
- **Format:** ASM-NNN with context, impact, confidence

### Rule 7: Memory Requires Sync
- **Gate:** Before session end
- **Check:** Update checkpoint
- **Rationale:** Preserve state across sessions

### Rule 8: Multi-Session Requires Isolation
- **Gate:** Before editing shared files
- **Check:** Check for concurrent sessions
- **Safeguards:** Append-only, unique IDs, channel isolation

### Rule 9: Implementation Requires Test (TDD)
- **Gate:** Before writing implementation
- **Check:** Test exists and fails (RED)
- **Lifecycle:** RED → GREEN → REFACTOR

### Rule 10: Failures Require Lessons
- **Gate:** After significant debugging (>30 min)
- **Check:** Log to `docs/knowledge/lessons.md`
- **Format:** LES-NNN with context, resolution, prevention

### Rule 11: Continuation Requires Context Check
- **Gate:** On session resume
- **Check:** Verify active sidequest, isolate memory
- **Prevents:** Context pollution across sidequests

### Rule 12: Phase Completion Requires Commit
- **Gate:** Before marking phase complete
- **Check:** Git commit with deliverables exists
- **Evidence:** Commit hash recorded in phase status

### Rule 13: Changes Require Branch
- **Gate:** Before any commit
- **Check:** Not on main/master, feature branch created
- **Pattern:** `cc/phase-{N}.{M}` or `feature/*`

### Rule 14: New Phase Requires Number Check
- **Gate:** Before creating phase-NN-*.md
- **Check:** `ls docs/proposals/phase-NN-*` shows no existing
- **Also:** Check `docs/proposals/_index.md`

### Rule 15: Phase Namespace Is Enforced
- **Gate:** On Write to phase-NN-*.md
- **Check:** Hook BLOCKS (not warns) on collision
- **Lesson:** LES-020

### Rule 16: Sync Protocol for Distribution
- **Gate:** On domain project session
- **Check:** Check `.ecw/sync/origin.json` for drift
- **Action:** Update or acknowledge drift

### Rule 17: Config Files Require Verification
- **Gate:** Before creating tool/platform config
- **Check:** Docs checked OR user confirmed
- **Prevents:** Invalid configuration files

### Rules 18-19: Reserved
- Reserved for future use

### Rule 20: Architectural Feasibility Required
- **Gate:** Before implementing features with dependencies
- **Check:** Can execution context access required dependencies?
- **Evidence:** Data flow diagram showing process boundaries

### Rule 21: E2E Tests Required for Integration
- **Gate:** Before claiming "integrated into X"
- **Check:** E2E test proves X calls feature and produces outcome
- **Anti-pattern:** Unit tests with mocks ≠ integration works

### Rule 22: Integration Claims Require Proof
- **Gate:** Before commit claiming "integrated"
- **Check:** Evidence that X actually invokes the integration
- **Evidence:** E2E test passes, manual test confirms

### Rule 23: Task Checkboxes Require Truthful State
- **Gate:** Before marking phase status
- **Check:** Checkbox state [x] matches actual completion
- **Prevents:** Completion theater

### Rule 24: Completion Requires 90% Threshold
- **Gate:** Before status "Complete"
- **Check:** ≥90% of task checkboxes marked [x]
- **Enforcement:** Pre-commit validates percentage

### Rule 25: Completion Theater Is Blocked
- **Gate:** On commit with "Complete" status
- **Check:** Pre-commit validates task completion percentage
- **Lesson:** Learned from false completion claims

### Rule 26: Design Review Requires Approval
- **Gate:** Before spawning sub-agents or creating artifacts
- **Check:** User said "approved", "proceed with approval", "approved and proceed", or explicit consent
- **Enforcement:** SOP-ENF provides HARD enforcement mechanism
- **Bypass:** "you don't need approval for this" or explicit scope-limited waiver
- **Protocol:**
  1. Present DESIGN SUMMARY to user
  2. List proposed artifacts and canonical locations
  3. Ask: "May I proceed?"
  4. WAIT for explicit written approval
  5. ONLY THEN spawn sub-agents or create artifacts
- **Violation:** If proceeded without approval, acknowledge violation and present for retroactive review
