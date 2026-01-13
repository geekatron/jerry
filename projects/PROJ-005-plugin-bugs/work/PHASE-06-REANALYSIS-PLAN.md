# PHASE-06 Re-Analysis Orchestration Plan

**Project:** PROJ-005-plugin-bugs
**Date:** 2026-01-13
**Trigger:** User feedback invalidating stdlib-only approach
**Status:** READY FOR EXECUTION

---

## Context

### Original Analysis (Now Invalidated)

The original PHASE-06 analysis recommended **Option B: Simplified Plugin Mode** (stdlib-only, ~80 lines). This was based on an incorrect assumption that plugins cannot have Python dependencies.

**User Feedback:**
> "I do not agree with your previous assessment... If python libraries etc were not meant to be used along with package managers in Claude Code plugins that would make the power of the plugins very weak."

### New Requirements

| ID | Requirement | Source |
|----|-------------|--------|
| REQ-001 | MUST use Hexagonal Architecture CLI implementation | User explicit |
| REQ-002 | MUST research uv or alternatives | User explicit |
| REQ-003 | MUST restore previous functionality | User explicit |
| REQ-004 | MUST implement testing strategies | User explicit |
| REQ-005 | Artifacts MUST follow ps-* naming convention | DISC-004 |

### Completed Research

| Document | Status | Findings |
|----------|--------|----------|
| PROJ-005-e-008-uv-dependency-management.md | COMPLETE | uv + PEP 723 recommended |

---

## Re-Analysis Strategy: "Ultrathink" Orchestration

### Approach: Incremental Re-Analysis

Rather than re-running ALL ps-* agents from scratch, we will:
1. **Preserve valid artifacts** - Functional requirements (e-006) remain valid
2. **Update constraints** - Remove stdlib-only constraint from patterns (e-007)
3. **Re-run trade-off analysis** - New options with uv (a-001)
4. **Create new ADR** - Supersede ADR-PROJ005-001
5. **Re-validate** - With new constraints and testing requirements (a-002)

### ps-* Agent Pipeline

```
                     ┌────────────────────────────┐
                     │  PHASE-06 RE-ANALYSIS      │
                     └────────────┬───────────────┘
                                  │
    ┌─────────────────────────────┼─────────────────────────────┐
    │                             │                             │
    ▼                             ▼                             ▼
┌───────────┐            ┌───────────────┐            ┌────────────────┐
│ PRESERVE  │            │   UPDATE      │            │    NEW         │
│           │            │               │            │                │
│ e-006 FRs │            │ e-007 Patterns│            │ e-008 uv       │
│ (valid)   │            │ (remove HC)   │            │ research       │
└───────────┘            └───────┬───────┘            └────────┬───────┘
                                 │                             │
                                 └──────────────┬──────────────┘
                                                │
                                                ▼
                                   ┌────────────────────┐
                                   │   ps-analyst       │
                                   │                    │
                                   │ Re-analyze options │
                                   │ WITH uv approach   │
                                   │                    │
                                   │ e-009-tradeoffs    │
                                   └─────────┬──────────┘
                                             │
                                             ▼
                                   ┌────────────────────┐
                                   │   ps-architect     │
                                   │                    │
                                   │ Create new ADR     │
                                   │ Supersede ADR-001  │
                                   │                    │
                                   │ e-010-adr-uv-hook  │
                                   └─────────┬──────────┘
                                             │
                                             ▼
                                   ┌────────────────────┐
                                   │   ps-validator     │
                                   │                    │
                                   │ Validate solution  │
                                   │ + Testing strategy │
                                   │                    │
                                   │ e-011-validation   │
                                   └─────────┬──────────┘
                                             │
                                             ▼
                                   ┌────────────────────┐
                                   │   IMPLEMENTATION   │
                                   │                    │
                                   │ BUG-007 Fix        │
                                   │ Using new ADR      │
                                   └────────────────────┘
```

---

## Execution Plan

### Step 1: Update Pattern Document (Manual)

**Task:** Update e-007 to remove stdlib-only hard constraint.

**Changes to PROJ-005-e-007-plugin-patterns.md:**
- HC-001 "Python stdlib only" → REMOVED (replaced by uv management)
- Add new pattern: P-011 "uv + PEP 723 Dependency Declaration"

### Step 2: ps-analyst - Trade-off Re-Analysis

**Trigger:** Problem-Solving skill with analyst directive
**Input:**
- e-006 Functional Requirements (unchanged)
- e-007 Updated Patterns (stdlib constraint removed)
- e-008 uv Research (new)
- REQ-001 to REQ-005 (new user requirements)

**Output:** `e-009-tradeoffs.md`

**Analysis Dimensions:**
| Dimension | Weight | Notes |
|-----------|--------|-------|
| Hexagonal Architecture Preservation | HIGH | Must use full implementation |
| User System Requirements | MEDIUM | uv installation acceptable |
| Regression Prevention | HIGH | Must have tests |
| Maintenance Burden | MEDIUM | Prefer simpler approaches |
| Performance | LOW | 10s timeout is generous |

**Expected Options to Analyze:**
| Option | Description |
|--------|-------------|
| Option A | uv + PEP 723 inline metadata (from e-008) |
| Option B | uv run wrapper with fallback |
| Option C | sys.path manipulation (no uv) |
| Option D | PYTHONPATH in hooks.json |

### Step 3: ps-architect - New ADR

**Trigger:** Problem-Solving skill with architect directive
**Input:**
- e-009 Trade-off Analysis (recommended option)
- e-008 uv Research
- Original ADR-PROJ005-001 (to supersede)

**Output:** `e-010-adr-uv-session-start.md`

**ADR Structure:**
- Status: Accepted (supersedes ADR-PROJ005-001)
- Context: Corrected understanding of plugin capabilities
- Decision: Selected option with implementation details
- Consequences: Including testing requirements

### Step 4: ps-validator - Final Validation

**Trigger:** Problem-Solving skill with validator directive
**Input:**
- e-010 New ADR
- e-006 Functional Requirements
- REQ-004 Testing Strategy requirement

**Output:** `e-011-validation.md`

**Validation Checklist:**
| Category | Tests |
|----------|-------|
| Hard Constraints | All original HCs (except stdlib) |
| Functional Requirements | FR-001 to FR-012 |
| User Requirements | REQ-001 to REQ-005 |
| Testing Strategy | Contract, Integration, Regression |

### Step 5: Implementation

**After validation passes:**
1. Modify `scripts/session_start.py` per ADR
2. Update `hooks/hooks.json` if needed
3. Add regression tests
4. Update documentation

---

## Artifact Naming (Corrected per DISC-004)

| Entry | Content | File |
|-------|---------|------|
| e-001 | Functional Requirements | (rename from e-006) |
| e-002 | Plugin Patterns | (rename from e-007) |
| e-003 | Trade-off Analysis v1 | (rename from a-001) |
| e-004 | ADR v1 | (rename from ADR-PROJ005-001) |
| e-005 | Validation v1 | (rename from a-002) |
| e-006 | SKIP (collision) | - |
| e-007 | SKIP (collision) | - |
| **e-008** | **uv Research** | **NEW (created)** |
| **e-009** | **Trade-off Analysis v2** | **TO CREATE** |
| **e-010** | **ADR v2 (uv approach)** | **TO CREATE** |
| **e-011** | **Validation v2** | **TO CREATE** |

**Note:** Due to DISC-004 (naming collision), new artifacts start at e-008 and will be renumbered after DISC-004 is resolved.

---

## ps-* Invocation Commands

### ps-analyst Invocation

```
Invoke ps-analyst to re-analyze trade-offs for BUG-007 session_start.py fix.

Context:
- Original stdlib-only constraint is REMOVED
- Must use Hexagonal Architecture CLI at src/interface/cli/session_start.py
- uv + PEP 723 research completed in PROJ-005-e-008-uv-dependency-management.md

Inputs:
1. investigations/PROJ-005-e-006-functional-requirements.md
2. research/PROJ-005-e-007-plugin-patterns.md (remove HC-001 stdlib constraint)
3. research/PROJ-005-e-008-uv-dependency-management.md (NEW)

New Requirements:
- REQ-001: Must use full Hexagonal Architecture implementation
- REQ-002: May require uv on user system (acceptable)
- REQ-003: Must restore previous functionality (regression fix)
- REQ-004: Must include testing strategy

Options to Analyze:
A. uv + PEP 723 inline metadata (direct shebang)
B. uv run wrapper with stdlib fallback
C. sys.path manipulation (no uv dependency)
D. PYTHONPATH environment variable in hooks.json

Output: PROJ-005-e-009-tradeoffs.md with recommendation
```

### ps-architect Invocation

```
Invoke ps-architect to create new ADR superseding ADR-PROJ005-001.

Context:
- Previous ADR recommended stdlib-only approach (REJECTED by user)
- New approach must use full Hexagonal Architecture
- uv + PEP 723 or alternative from trade-off analysis

Inputs:
1. analysis/PROJ-005-e-009-tradeoffs.md (recommended option)
2. research/PROJ-005-e-008-uv-dependency-management.md
3. decisions/ADR-PROJ005-001-standalone-session-start.md (to supersede)
4. src/interface/cli/session_start.py (full implementation reference)

Output: PROJ-005-e-010-adr-uv-session-start.md
```

### ps-validator Invocation

```
Invoke ps-validator to validate the new ADR against all requirements.

Context:
- Validates new uv-based approach
- Must include testing strategy validation
- GO/NO-GO recommendation for implementation

Inputs:
1. decisions/PROJ-005-e-010-adr-uv-session-start.md
2. investigations/PROJ-005-e-006-functional-requirements.md
3. research/PROJ-005-e-008-uv-dependency-management.md
4. User requirements REQ-001 to REQ-005

Validation Categories:
1. Functional Requirements (FR-001 to FR-012)
2. Updated Constraints (no stdlib requirement)
3. Testing Strategy (Contract, Integration, Regression)
4. User Requirements (REQ-001 to REQ-005)

Output: PROJ-005-e-011-validation.md with GO/NO-GO recommendation
```

---

## Success Criteria

### Re-Analysis Phase Complete When:

- [ ] e-008 uv research document created ✓
- [ ] e-009 trade-off analysis v2 complete
- [ ] e-010 new ADR created (supersedes ADR-PROJ005-001)
- [ ] e-011 validation passed with GO recommendation
- [ ] Testing strategy documented and approved

### Implementation Phase Complete When:

- [ ] scripts/session_start.py modified per ADR
- [ ] hooks/hooks.json updated (if needed)
- [ ] Regression tests added
- [ ] Integration tests passing
- [ ] Contract tests passing
- [ ] BUG-007 marked RESOLVED

---

## Risk Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| uv not installed on user system | MEDIUM | HIGH | Provide fallback; document in INSTALLATION.md |
| uv version incompatibility | LOW | MEDIUM | Specify minimum uv version |
| Claude Code changes hook execution | LOW | HIGH | Contract tests detect drift |
| Performance regression | LOW | LOW | 10s timeout is generous |

---

*Plan created: 2026-01-13*
*Ready for: ps-analyst invocation*
