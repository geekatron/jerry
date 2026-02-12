# EN-206:TASK-006: Rollback and Recovery Documentation

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
CREATED: 2026-02-02 (Claude)
PURPOSE: Document rollback procedures for sync mechanism - identified by QG-1 review
TRIGGER: nse-qa-002-tasks-audit.md identified missing reversibility documentation
-->

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Created:** 2026-02-02T09:30:00Z
> **Due:** 2026-02-14T00:00:00Z
> **Completed:** -
> **Parent:** EN-206
> **Owner:** Claude
> **Effort:** 2

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task objective - document rollback procedures |
| [Rollback Scenarios](#rollback-scenarios) | Situations requiring rollback |
| [Recovery Procedures](#recovery-procedures) | Step-by-step recovery for each strategy |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |

---

## Summary

Create comprehensive rollback and recovery documentation for the sync mechanism. This task was identified as a critical gap in the QG-1 adversarial review - the implementation needs clear guidance for users when things go wrong, enabling graceful recovery without data loss.

**Addresses:**
- NC-005 from nse-qa audit: Insufficient reversibility documentation
- GAP-006 from ps-critic: Bootstrap script complexity underestimated (error handling)

---

## Rollback Scenarios

### Scenario Matrix

| Scenario | Trigger | Severity | Documentation Required |
|----------|---------|----------|------------------------|
| S-001 | Bootstrap fails mid-execution | HIGH | Full rollback procedure |
| S-002 | Sync mechanism corrupts target | CRITICAL | Data recovery steps |
| S-003 | User wants to uninstall Jerry | MEDIUM | Clean removal guide |
| S-004 | Junction/symlink becomes stale | LOW | Refresh procedure |
| S-005 | Platform strategy mismatch | MEDIUM | Strategy switch guide |
| S-006 | Source directory missing | HIGH | Recovery from backup |
| S-007 | Antivirus blocks operation | MEDIUM | Exception/bypass guide |

---

## Recovery Procedures

### Required Documentation

#### 1. Pre-Bootstrap Backup Guide
- How to backup existing `.claude/` before bootstrap
- What to preserve vs what can be regenerated
- Recommended backup location and naming

#### 2. Mid-Execution Failure Recovery
```markdown
## If Bootstrap Fails Mid-Execution

### Symptom
Bootstrap exits with error before completion

### Recovery Steps
1. Check for partial `.claude/rules/` or `.claude/patterns/`
2. If junction/symlink exists but is broken:
   - Windows: `rmdir .claude\rules`
   - macOS/Linux: `rm .claude/rules`
3. Re-run `/bootstrap --force`

### If Still Failing
1. Run `/bootstrap --copy` (fallback to file copy)
2. Report issue with platform info
```

#### 3. Full Uninstallation
```markdown
## Removing Jerry Bootstrap Results

### Windows (Junction Points)
rmdir .claude\rules
rmdir .claude\patterns

### macOS/Linux (Symlinks)
rm .claude/rules
rm .claude/patterns

### Verify Removal
# Should show "cannot find" or "No such file"
ls -la .claude/rules
```

#### 4. Strategy Migration
- How to switch from junction → copy
- How to switch from symlink → copy
- How to upgrade from copy → symlink (when permissions allow)

---

## Acceptance Criteria

### Definition of Done

- [ ] Pre-bootstrap backup guide documented
- [ ] Mid-execution failure recovery documented
- [ ] Full uninstallation procedure documented
- [ ] Strategy migration guide documented
- [ ] Platform-specific commands tested
- [ ] Integrated into user documentation (TASK-004)

### Technical Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| TC-1 | Backup procedure preserves user data | [ ] |
| TC-2 | Junction removal works on Windows | [ ] |
| TC-3 | Symlink removal works on macOS/Linux | [ ] |
| TC-4 | --force flag cleanly overwrites | [ ] |
| TC-5 | Documentation is user-friendly | [ ] |

---

## Related Items

### Hierarchy

- **Parent:** [EN-206: Context Distribution Strategy](./EN-206-context-distribution-strategy.md)

### Dependencies

- **Depends On:** TASK-002 (sync mechanism must exist to document rollback)
- **Enables:** TASK-004 (rollback docs integrate into user documentation)

### Traceability

- **Addresses:** NC-005 (reversibility documentation) from nse-qa audit
- **Addresses:** GAP-006 (error handling specification) from ps-critic review

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-02T09:30:00Z | Claude | pending | Task created from QG-1 gap analysis |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | Task |
| **SAFe** | Task |
| **JIRA** | Task |
