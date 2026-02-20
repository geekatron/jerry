# TASK-001: Rewrite project-workflow.md to Reference /worktracker Skill Rules as SSOT

> **Type:** task
> **Status:** done
> **Priority:** high
> **Created:** 2026-02-19
> **Parent:** BUG-011
> **Owner:** --
> **Effort:** 2
> **Activity:** documentation

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Description](#description) | What this task requires |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Implementation Notes](#implementation-notes) | Technical approach and constraints |
| [Related Items](#related-items) | Parent and related work |
| [Evidence](#evidence) | Deliverables and verification |
| [History](#history) | Status changes |

---

## Description

Rewrite `.context/rules/project-workflow.md` to eliminate competing definitions while retaining minimal structural orientation for session-start context. The file must reference the authoritative `/worktracker` skill rules as SSOT while preserving enough context for Claude Code to navigate projects without requiring explicit `/worktracker` invocation.

**Key principle (from DA-002 adversary finding):** The rewrite must NOT be a pure pointer-only file. Session-start rules auto-load; skill rules load on demand. A session can proceed without `/worktracker` ever being invoked. The rewritten file must retain a minimal orientation summary while clearly marking the worktracker rules as authoritative for full detail.

### Changes Required

1. **Project Structure** — Replace the inline 7-line directory tree (lines 34-43) with a brief orientation note (e.g., "Projects follow `projects/PROJ-{NNN}-{slug}/` with `WORKTRACKER.md`, `PLAN.md`, and `work/` decomposition") plus a reference to `skills/worktracker/rules/worktracker-directory-structure.md` as the authoritative source. No competing tree.

2. **Workflow Phases** — Retain the before/during/after table as a complementary high-level guide. Add a cross-reference note pointing to WTI-001 through WTI-007 in `skills/worktracker/rules/worktracker-behavior-rules.md` for integrity enforcement rules. Do NOT rewrite the workflow phases into a different format — they are complementary, not conflicting (per SR-004).

3. **Project Resolution** — Update the project creation logic (lines 49-62) to reference `skills/worktracker/rules/worktracker-directory-structure.md` for folder layout patterns and `skills/worktracker/rules/worktracker-entity-hierarchy.md` for ID format and containment.

4. **H-04 Preservation** — The H-04 active project requirement (lines 17-18) MUST remain unchanged as it is a HARD rule referenced by CLAUDE.md.

### Constraints

- **AE-002 applies**: This touches `.context/rules/` — auto-C3 minimum criticality. Execution requires C3 strategies (S-004 Pre-Mortem, S-012 FMEA, S-013 Inversion) beyond baseline C2.
- The rewritten file must still work as a session-start rule (auto-loaded via `.claude/rules/` hardlink)
- Minimal structural orientation MUST be retained (DA-002) — Claude needs basic project navigation context at session start
- File path references should resolve correctly from the repository root

---

## Acceptance Criteria

- [x] AC-1: No inline project directory tree — replaced with brief orientation note + reference to `worktracker-directory-structure.md`
- [x] AC-2: Workflow phases retain high-level before/during/after guide with cross-reference to WTI integrity rules
- [x] AC-3: Project creation logic references worktracker directory structure and entity hierarchy
- [x] AC-4: H-04 active project HARD rule unchanged
- [x] AC-5: No inline competing structural definitions remain (no code-block directory trees that redefine the worktracker structure)
- [x] AC-6: File path references resolve to existing files
- [x] AC-7: `/adversary` C3 review PASS — score 0.970 (threshold 0.92). Strategies: S-010, S-003, S-002, S-004, S-007, S-012, S-013, S-014. Two iterations: 0.860 (REVISE) → 0.970 (PASS).

---

## Implementation Notes

### Current File Structure (to be rewritten)

```
project-workflow.md (63 lines)
├── HARD Rule Reference (H-04) ........... KEEP AS-IS
├── Workflow Phases ...................... ADD cross-reference to WTI rules
├── Project Structure ................... REPLACE tree → orientation note + SSOT reference
└── Project Resolution .................. UPDATE → reference worktracker rules for layout + IDs
```

### Target File Structure

```
project-workflow.md
├── HARD Rule Reference (H-04) ........... UNCHANGED
├── Workflow Phases ...................... RETAINED with WTI cross-reference added
├── Project Structure ................... Brief orientation note + SSOT pointer
└── Project Resolution .................. UPDATED → references worktracker rules for layout + IDs
```

### Files to Modify

| File | Change |
|------|--------|
| `.context/rules/project-workflow.md` | Rewrite: replace inline definitions with SSOT references, retain minimal orientation |

### Files Referenced (read-only)

| File | Purpose |
|------|---------|
| `skills/worktracker/rules/worktracker-directory-structure.md` | Authoritative directory layout |
| `skills/worktracker/rules/worktracker-behavior-rules.md` | Authoritative WTI integrity rules |
| `skills/worktracker/rules/worktracker-entity-hierarchy.md` | Entity ID formats and containment |

---

## Related Items

- **Parent:** [BUG-011](./BUG-011-project-workflow-rule-conflict.md)
- **AE-002:** Fix touches `.context/rules/` (hardlink to `.claude/rules/`) — auto-C3 minimum
- **Adversary findings addressed:** DA-002 (session-start blind spot), SR-004 (workflow scope narrowed), SR-005/DA-004 (AC-5 replaced), SR-009 (C3 strategies noted)
- **GitHub Issue:** [#38](https://github.com/geekatron/jerry/issues/38)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Rewritten `project-workflow.md` | File | `.context/rules/project-workflow.md` |

### Verification

- [x] Acceptance criteria verified
- [x] No inline directory tree remains
- [x] References resolve to correct files
- [x] H-04 still enforced at session start
- [x] Minimal orientation context retained for sessions without /worktracker invocation

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-19 | Created | Rewrite project-workflow.md to reference worktracker skill rules. AE-002: auto-C3. |
| 2026-02-19 | Updated | /adversary C2 findings applied: DA-002 (retain minimal orientation, not pointers-only), SR-004 (workflow phases = add cross-ref, not rewrite), SR-005/DA-004 (AC-5 replaced with substantive criterion), SR-009 (C3 strategies noted in constraints). |
| 2026-02-19 | done | Rewrite complete. C3 adversary review: 8 strategies (S-010, S-003, S-002, S-004, S-007, S-012, S-013, S-014). Iteration 1: 0.860 (REVISE — 4 minor gaps). Iteration 2: 0.970 (PASS). All ACs verified. |

---
