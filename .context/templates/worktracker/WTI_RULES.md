# Worktracker Integrity (WTI) Rules

> **Purpose:** Shared integrity rules for worktracker operations
> **Scope:** All worktracker agents and manual work item updates
> **Version:** 1.0
> **Last Updated:** 2026-02-02

---

## Navigation

| Previous | Up | Next |
|----------|----|----- |
| [WORKTRACKER Templates](.) | [.context/templates](../..) | [AUDIT_REPORT.md](AUDIT_REPORT.md) |

---

## Overview

These rules ensure worktracker integrity across all agents and manual updates. They define the minimum standards for work item state management, verification, and closure.

**Authority:** These rules override any conflicting agent-specific behaviors.

---

## WTI-001: Real-Time State

**Rule:** Work item files MUST reflect the actual state of work. Updates MUST be made immediately after work completion, not batched.

**Rationale:** Stale state leads to incorrect status reports and coordination failures in multi-agent workflows.

**Enforcement:**
- Agents MUST update work item files within the same tool call as completing work
- Status reports MUST read fresh state before generation
- No "TODO: update later" patterns allowed

**Violation Example:**
```markdown
# BAD: Agent completes work but doesn't update status
## Status
Status: IN_PROGRESS  <!-- Should be DONE -->
```

**Correct Example:**
```markdown
# GOOD: Agent updates status immediately
## Status
Status: DONE
Completed: 2026-02-02T14:30:00Z
```

---

## WTI-002: No Closure Without Verification

**Rule:** Work items MUST NOT transition to DONE/COMPLETED without:
- All acceptance criteria checked (80%+ verified)
- Evidence section populated with at least one link
- Child items all completed (if applicable)

**Rationale:** Premature closure creates technical debt and false progress signals.

**Enforcement:**
- wt-verifier agent validates before closure
- Manual closures require verification checklist
- CI checks enforce evidence links on DONE transitions

**Verification Checklist:**
```markdown
- [ ] 80%+ acceptance criteria verified
- [ ] Evidence section has ≥1 link (commit, PR, test result, doc)
- [ ] All child items completed (or none exist)
- [ ] No blocking impediments
```

**Violation Example:**
```markdown
# BAD: Marked DONE without evidence
## Status
Status: DONE

## Evidence
<!-- No evidence provided -->
```

**Correct Example:**
```markdown
# GOOD: Evidence supports closure
## Status
Status: DONE

## Evidence
- [Commit abc123](https://github.com/.../commit/abc123) - Implemented feature
- [PR #45](https://github.com/.../pull/45) - Reviewed and merged
- [Test results](./test-output.txt) - 100% passing
```

---

## WTI-003: Truthful State

**Rule:** Work items MUST NOT be marked complete if work is incomplete. Status MUST accurately reflect reality.

**Rationale:** False completion metrics undermine trust and decision-making.

**Enforcement:**
- wt-auditor checks for completion without evidence
- Status transitions require justification
- Disagreement resolution favors lower completion state

**Red Flags:**
- Status: DONE but acceptance criteria unchecked
- Status: DONE but no commits/PRs linked
- Status: DONE but child items IN_PROGRESS

**Resolution:**
- If evidence is missing → revert to IN_PROGRESS
- If criteria unmet → revert to IN_PROGRESS
- If children incomplete → BLOCKED status

---

## WTI-004: Synchronize Before Reporting

**Rule:** Before generating status reports, agents MUST read current worktracker state to avoid stale information.

**Rationale:** Cached or remembered state may be outdated due to concurrent updates.

**Enforcement:**
- All report generators MUST use Read tool before synthesis
- No reliance on memory from earlier in session
- Timestamp synchronization check

**Correct Pattern:**
```python
# Pseudo-code for agents
def generate_status_report(epic_id):
    # REQUIRED: Read fresh state
    epic_file = read_file(f"work/{epic_id}/{epic_id}.md")
    parse_current_state(epic_file)

    # Now generate report from fresh data
    return create_report(...)
```

**Violation:**
```python
# BAD: Using cached state from earlier
def generate_status_report(epic_id):
    # Uses self.cached_state from session start
    return create_report(self.cached_state)
```

---

## WTI-005: Atomic State Updates

**Rule:** When updating work item status, BOTH the item file AND parent reference MUST be updated atomically.

**Rationale:** Inconsistent parent-child state causes broken progress tracking.

**Enforcement:**
- Single Edit/Write operation updates both locations
- Rollback on partial failure
- wt-auditor detects parent-child mismatches

**Update Procedure:**
1. Read parent file
2. Read child file
3. Update child status section
4. Update parent's child reference
5. Write both files in sequence

**Correct Example:**
```markdown
# Child: EN-001-example.md
## Status
Status: DONE

# Parent: FEAT-001-example.md
## Enablers
- [x] EN-001: Example enabler - DONE ✅
```

**Violation Example:**
```markdown
# Child: EN-001-example.md
## Status
Status: DONE

# Parent: FEAT-001-example.md
## Enablers
- [ ] EN-001: Example enabler - IN_PROGRESS ❌ MISMATCH
```

---

## WTI-006: Evidence-Based Closure

**Rule:** The Evidence section MUST contain verifiable proof of completion before closure. Links to commits, PRs, test results, or documentation are required.

**Rationale:** Evidence enables auditability and prevents "looks done but isn't" syndrome.

**Enforcement:**
- wt-verifier requires ≥1 evidence link
- Evidence links MUST be resolvable (not broken)
- Evidence MUST relate to acceptance criteria

**Valid Evidence Types:**
1. **Git Commits:** `[Commit abc123](https://github.com/.../commit/abc123)`
2. **Pull Requests:** `[PR #45](https://github.com/.../pull/45)`
3. **Test Results:** `[Test output](./test-results.txt)`
4. **Documentation:** `[ADR-005](../decisions/ADR-005-example.md)`
5. **Screenshots:** `[Screenshot](./screenshot.png)` (for UI work)
6. **CI Logs:** `[CI Build](https://ci-system/build/123)`

**Minimum Requirement:**
- At least 1 verifiable link per work item
- Links MUST be accessible (relative paths valid, URLs reachable)
- Evidence MUST support acceptance criteria claims

**Red Flags:**
- Generic statements without links ("Implemented the feature")
- Broken links (404, file not found)
- Evidence unrelated to acceptance criteria

---

## Compliance Verification

### Automated Checks

**wt-auditor** enforces these rules via:
- File structure validation (WTI-005)
- Evidence link verification (WTI-006)
- Status consistency checks (WTI-003)
- Parent-child synchronization (WTI-005)

### Manual Review

Human reviewers SHOULD verify:
- Evidence quality (not just presence)
- Acceptance criteria interpretation
- Edge cases not covered by automation

---

## Violation Remediation

| Rule Violated | Severity | Remediation |
|---------------|----------|-------------|
| WTI-001 | HIGH | Immediate update required; report regeneration |
| WTI-002 | CRITICAL | Revert to IN_PROGRESS until verified |
| WTI-003 | CRITICAL | Revert to truthful state; investigate cause |
| WTI-004 | MEDIUM | Regenerate report from fresh state |
| WTI-005 | HIGH | Synchronize parent-child state; add consistency check |
| WTI-006 | HIGH | Add evidence links or revert to IN_PROGRESS |

---

## References

- **Design Source:** `synthesis-worktracker-agent-design.md` (lines 582-605)
- **Related Agents:** wt-verifier, wt-auditor
- **Templates:** AUDIT_REPORT.md, VERIFICATION_REPORT.md
- **Constitution:** P-010 (Task Tracking Integrity)

---

*Version History:*
- 1.0 (2026-02-02): Initial version from synthesis document
