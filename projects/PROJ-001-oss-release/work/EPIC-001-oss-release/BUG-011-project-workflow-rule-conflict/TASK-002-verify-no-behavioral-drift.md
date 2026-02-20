# TASK-002: Verify No Behavioral Drift After Rewrite

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-02-19
> **Parent:** BUG-011
> **Owner:** --
> **Effort:** 1
> **Activity:** testing

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Description](#description) | What this task requires |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Implementation Notes](#implementation-notes) | Technical approach and verification steps |
| [Related Items](#related-items) | Parent and related work |
| [Evidence](#evidence) | Deliverables and verification |
| [History](#history) | Status changes |

---

## Description

Verify that the rewritten `project-workflow.md` (TASK-001) does not change session-start behavior. The file is auto-loaded via `.claude/rules/` hardlink (same inode as `.context/rules/project-workflow.md`), so any structural change affects session-start context immediately.

### Verification Scope

1. **H-04 enforcement**: Confirm the active project requirement is still enforced — Claude Code must still reject sessions without `JERRY_PROJECT` set
2. **Project resolution flow**: Confirm `<project-required>` and `<project-error>` handling instructions are still present and functional
3. **Hardlink integrity**: Confirm `.claude/rules/project-workflow.md` and `.context/rules/project-workflow.md` share the same inode (hardlink, not symlink — per SR-001)
4. **Reference resolution**: Confirm file path references to `skills/worktracker/rules/` are valid and navigable
5. **Minimal orientation**: Confirm the rewritten file retains enough structural context for sessions where `/worktracker` is never explicitly invoked (DA-002)
6. **Test suite**: Confirm existing tests still pass — no regressions from the file change

---

## Acceptance Criteria

- [ ] AC-1: `.claude/rules/project-workflow.md` and `.context/rules/project-workflow.md` share the same inode (hardlink verification)
- [ ] AC-2: H-04 active project requirement text is present and unchanged in the rewritten file
- [ ] AC-3: Project resolution instructions (`<project-required>`, `<project-error>`) are present
- [ ] AC-4: All file path references in the rewritten file resolve to existing files
- [ ] AC-5: Full test suite passes (`uv run pytest tests/ -x`)
- [ ] AC-6: Rewritten file contains minimal structural orientation (project path pattern, key files) — not just pointers

---

## Implementation Notes

### Verification Steps

```bash
# 1. Hardlink integrity (SR-001: NOT a symlink)
stat -f "%i" .claude/rules/project-workflow.md
stat -f "%i" .context/rules/project-workflow.md
# Expected: identical inode numbers

# 2. H-04 text preserved
grep -c "H-04" .context/rules/project-workflow.md
# Expected: >= 1

# 3. Project resolution preserved
grep -c "project-required\|project-error" .context/rules/project-workflow.md
# Expected: >= 2

# 4. Reference paths resolve
# Extract file paths from the file and verify each exists

# 5. Tests
uv run pytest tests/ -x --timeout=60

# 6. Minimal orientation check
# Verify the file mentions PROJ-{NNN}-{slug}, WORKTRACKER.md, PLAN.md, work/
```

### Dependencies

- **Blocked by:** TASK-001 (must be completed first — nothing to verify until rewrite is done)

---

## Related Items

- **Parent:** [BUG-011](./BUG-011-project-workflow-rule-conflict.md)
- **Depends on:** [TASK-001](./TASK-001-rewrite-project-workflow-as-reference.md)
- **Adversary findings addressed:** SR-001 (hardlink not symlink), SR-006/DA-005 (removed vacuous ruff checks), DA-002 (added minimal orientation check)
- **GitHub Issue:** [#38](https://github.com/geekatron/jerry/issues/38)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Verification results | Test output | (populated on completion) |

### Verification

- [ ] Acceptance criteria verified
- [ ] Hardlink intact (same inode)
- [ ] All referenced files exist
- [ ] Test suite green

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-19 | Created | Verify no behavioral drift after TASK-001 rewrite. Blocked by TASK-001. |
| 2026-02-19 | Updated | /adversary C2 findings applied: SR-001 (fixed hardlink vs symlink — AC-1 now checks inode), SR-006/DA-005 (removed vacuous ruff checks AC-6/AC-7), DA-002 (added minimal orientation verification AC-6). |

---
