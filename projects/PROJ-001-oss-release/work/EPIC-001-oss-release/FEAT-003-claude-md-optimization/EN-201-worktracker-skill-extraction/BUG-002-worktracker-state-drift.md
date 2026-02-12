# BUG-002: Worktracker State Drift

<!--
TEMPLATE: Bug
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-01 (Claude)
PURPOSE: Document process failure where completed work was not reflected in worktracker
-->

> **Type:** bug
> **Status:** FIXED
> **Severity:** major
> **Priority:** high
> **Created:** 2026-02-01T21:00:00Z
> **Fixed:** 2026-02-01T21:00:00Z
> **Parent:** EN-201
> **Owner:** Claude

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What happened - state drift between completed work and tracking |
| [Root Cause](#root-cause) | Why it happened - background agents completed without updates |
| [Impact](#impact) | Consequences - confusion, duplicate work risk |
| [Resolution](#resolution) | How it was fixed - state reconciliation + new rules |
| [Prevention](#prevention) | New WTI rules to prevent recurrence |

---

## Summary

**What Happened:**
TASK-002 through TASK-005 were completed by background agents, but the EN-201 worktracker file was never updated to reflect completion. When asked about open tasks, the worktracker showed 6/7 tasks pending when actually only 2/7 were pending.

**Symptom:**
- EN-201 showed: 14% complete (1/7 tasks)
- Reality: 71% complete (5/7 tasks)
- Files existed but status was stale

---

## Root Cause

### Primary Cause
Background agent tasks completed work but the orchestrating agent (main context) failed to update worktracker state after agent completion.

### Contributing Factors

| Factor | Description |
|--------|-------------|
| Session boundaries | Context compaction lost awareness of agent completions |
| No enforcement rule | No HARD rule requiring immediate state updates |
| Trust in signals | Assumed agent completion signals were sufficient |
| No verification step | Did not verify file existence before reporting status |

### Anti-Pattern Identified
Marking work as "done" based on agent signals without verifying deliverables exist and updating tracking documents.

---

## Impact

| Impact Type | Description | Severity |
|-------------|-------------|----------|
| **Confusion** | User asked about open tasks, got wrong answer | Medium |
| **Duplicate Work Risk** | Could have re-executed completed tasks | High |
| **Trust Erosion** | Worktracker no longer single source of truth | High |
| **Planning Errors** | Progress tracking showed 14% instead of 71% | Medium |

---

## Resolution

### Immediate Fix

1. **Verified deliverables** - Confirmed all 4 rule files exist:
   - `worktracker-entity-hierarchy.md` (104 lines)
   - `worktracker-system-mappings.md` (92 lines)
   - `worktracker-behavior-rules.md` (148 lines)
   - `worktracker-directory-structure.md` (81 lines)

2. **Updated EN-201 state** - Corrected task status from pending to DONE

3. **Updated progress metrics** - Changed from 14% to 71%

4. **Added evidence** - Populated Technical Verification table with proof

### Systemic Fix

Added **Worktracker Integrity Rules (WTI-001 through WTI-006)** to `worktracker-behavior-rules.md`:

| Rule | Enforcement | Description |
|------|-------------|-------------|
| WTI-001 | HARD | Real-time state updates immediately after completing work |
| WTI-002 | HARD | No closure without verifying ALL acceptance criteria |
| WTI-003 | HARD | State must be truthful, accurate, honest, verifiable |
| WTI-004 | HARD | Synchronize/verify before reporting status |
| WTI-005 | MEDIUM | Atomic updates (task + parent in same operation) |
| WTI-006 | HARD | Evidence section must be populated before closure |

---

## Prevention

### New Behavioral Rules

These rules are now documented in `skills/worktracker/rules/worktracker-behavior-rules.md` and will be loaded with the `/worktracker` skill.

### Key Safeguards

1. **WTI-001**: Update state IMMEDIATELY after work completes
2. **WTI-002**: NEVER close without verifying AC met
3. **WTI-004**: ALWAYS verify file system before reporting

### Process Changes

| Before | After |
|--------|-------|
| Trust agent completion signals | Verify deliverables exist |
| Update state "later" | Update state immediately |
| Assume progress is tracked | Verify tracking matches reality |

---

## Evidence

| Evidence | Description |
|----------|-------------|
| Files exist | `wc -l skills/worktracker/rules/*.md` shows 551 total lines |
| State corrected | EN-201 now shows 71% (5/7 tasks) |
| Rules added | WTI-001 through WTI-006 in behavior-rules.md |

---

## Related Items

- **Parent:** [EN-201](./EN-201-worktracker-skill-extraction.md)
- **Similar:** [BUG-001](./BUG-001-deleted-user-files-without-review.md) - Another process failure
- **Rule Created:** `skills/worktracker/rules/worktracker-behavior-rules.md` (WTI rules)

---

## Lessons Learned

1. **Trust but verify** - Agent completion signals are not enough
2. **Immediate updates** - State drift compounds over time
3. **Systemic fixes** - Add rules to prevent recurrence, not just fix symptoms
4. **Evidence-based** - Always verify deliverables exist before marking complete

---

*Bug Version: 1.0.0*
*Created: 2026-02-01*
*Fixed: 2026-02-01*
