# EN-206:TASK-005: Integration Testing and Platform Verification

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
CREATED: 2026-02-02 (Claude)
PURPOSE: Verify sync mechanism across all target platforms - identified by QG-1 review
TRIGGER: nse-qa-002-tasks-audit.md identified missing integration testing
-->

> **Type:** task
> **Status:** pending
> **Priority:** critical
> **Impact:** critical
> **Created:** 2026-02-02T09:00:00Z
> **Due:** 2026-02-14T00:00:00Z
> **Completed:** -
> **Parent:** EN-206
> **Owner:** Claude
> **Effort:** 5

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task objective - verify platform compatibility |
| [Test Matrix](#test-matrix) | Platforms and scenarios to test |
| [Test Procedures](#test-procedures) | Step-by-step verification |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |

---

## Summary

Execute end-to-end integration tests for the sync mechanism across all target platforms. This task was identified as a critical gap in the QG-1 adversarial review - the research claims platform compatibility but lacks verification evidence.

**Verification Methods from Requirements Traceability:**
- VM-001: Test sync on macOS, Linux, Windows
- VM-002: Test on Windows without admin, without Dev Mode
- VM-004: Modify source, verify target reflects change
- VM-005: Force symlink failure, verify copy fallback
- VM-006: Test platform detection on all environments
- VM-007: Test in WSL1, WSL2, Cygwin, Git Bash

---

## Test Matrix

### Platform Coverage

| Platform | OS Version | Strategy Expected | Priority |
|----------|------------|-------------------|----------|
| macOS (Intel) | Sonoma 14.x | Symlink | HIGH |
| macOS (Apple Silicon) | Sonoma 14.x | Symlink | HIGH |
| Ubuntu | 22.04 LTS | Symlink | HIGH |
| Ubuntu | 24.04 LTS | Symlink | MEDIUM |
| Windows 10 Pro | 22H2 | Junction (no Dev Mode) | CRITICAL |
| Windows 10 Home | 22H2 | Junction | HIGH |
| Windows 11 Pro | 23H2 | Junction | HIGH |
| Windows (Dev Mode ON) | 10/11 | Symlink | MEDIUM |
| WSL1 | Ubuntu 22.04 | Symlink | MEDIUM |
| WSL2 | Ubuntu 22.04 | Symlink | HIGH |
| Git Bash | MSYS2/MinGW | Junction or Copy | MEDIUM |
| Cygwin | Latest | Cygwin symlink | LOW |

### Scenario Coverage

| Scenario | Description | Priority |
|----------|-------------|----------|
| S-001 | Fresh bootstrap on clean system | CRITICAL |
| S-002 | Re-run bootstrap (idempotency) | HIGH |
| S-003 | Bootstrap with existing .claude/rules/ (real dir) | HIGH |
| S-004 | Source modification propagates to target | HIGH |
| S-005 | Bootstrap with --force flag | MEDIUM |
| S-006 | Bootstrap on network drive | MEDIUM |
| S-007 | Bootstrap with .context/ collision | MEDIUM |
| S-008 | Symlink failure triggers junction fallback | HIGH |
| S-009 | Junction failure triggers copy fallback | HIGH |
| S-010 | Bootstrap with Controlled Folder Access enabled | MEDIUM |

---

## Test Procedures

### Test Template

```markdown
## Platform: [Platform Name]

**Test Date:** YYYY-MM-DD
**Tester:** [Name]

**Environment:**
- OS: [Name] [Version] [Build]
- File System: [NTFS/APFS/ext4/etc.]
- User Type: [Admin/Standard]
- Developer Mode: [Enabled/Disabled/N/A]
- Antivirus: [Product Name]

**Pre-conditions:**
- [ ] No existing .claude/rules/ or .claude/patterns/
- [ ] .context/rules/ and .context/patterns/ exist with test files
- [ ] Test user has standard (non-admin) permissions

**Test Execution:**

| Step | Action | Expected | Actual | Status |
|------|--------|----------|--------|--------|
| 1 | Run platform detection | Correct platform identified | | |
| 2 | Run strategy detection | [symlink/junction/copy] selected | | |
| 3 | Execute /bootstrap | Completes without error | | |
| 4 | Verify .claude/rules/ exists | Directory present | | |
| 5 | Verify content accessible | Can read rule files | | |
| 6 | Modify source file | Target reflects change (if symlink/junction) | | |
| 7 | Re-run /bootstrap | Idempotent (no error) | | |

**Evidence:**
- Console output: [paste or screenshot]
- Directory listing: [paste]
- Strategy used: [symlink/junction/copy]

**Notes:**
[Any observations or issues]
```

### Critical Test Cases

#### TC-001: Windows 10 Standard User, No Dev Mode

**Purpose:** Verify junction points work without admin
**Expected:** Junction strategy selected and succeeds

```
Steps:
1. Log in as standard user (not admin)
2. Verify Developer Mode is OFF
3. Run: python -c "from sync import detect_best_strategy; print(detect_best_strategy(...))"
4. Expect: "junction"
5. Run: /bootstrap
6. Verify: .claude/rules/ is a junction point (dir /aL shows <JUNCTION>)
7. Verify: Content accessible
8. Modify .context/rules/test.md
9. Verify: .claude/rules/test.md reflects change immediately
```

#### TC-002: Git Bash Platform Detection

**Purpose:** Verify Git Bash is detected correctly
**Expected:** Detected as MSYS, uses Windows strategy

```
Steps:
1. Open Git Bash
2. Run: python -c "import platform; print(platform.system())"
3. Expected output: MINGW64_NT-* (NOT Windows, NOT Linux)
4. Run: python -c "from sync import detect_platform; print(detect_platform())"
5. Verify: is_msys = True
6. Run: /bootstrap
7. Verify: Junction or copy used (NOT Linux symlink)
```

#### TC-003: Symlink Failure Triggers Junction Fallback

**Purpose:** Verify fallback mechanism works
**Expected:** Graceful degradation to junction

```
Steps:
1. Windows 10 standard user, Dev Mode OFF
2. Temporarily block symlink creation (or use known failing config)
3. Run: /bootstrap
4. Observe: "Couldn't create symlink, trying junction..." message
5. Verify: Junction created successfully
6. Verify: Content accessible
```

---

## Acceptance Criteria

### Definition of Done

- [ ] All CRITICAL priority platforms tested and passing
- [ ] All HIGH priority platforms tested and passing
- [ ] Test evidence documented for each platform
- [ ] No blockers identified for any target platform
- [ ] Fallback mechanisms verified working
- [ ] Test results added to research artifact

### Technical Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| TC-1 | macOS symlinks work | [ ] |
| TC-2 | Linux symlinks work | [ ] |
| TC-3 | Windows junction without admin works | [ ] |
| TC-4 | Windows symlink with Dev Mode works | [ ] |
| TC-5 | WSL symlinks work | [ ] |
| TC-6 | Git Bash detection correct | [ ] |
| TC-7 | Fallback from symlink to junction works | [ ] |
| TC-8 | Fallback from junction to copy works | [ ] |
| TC-9 | Re-run is idempotent | [ ] |
| TC-10 | Source changes propagate (symlink/junction) | [ ] |

---

## Related Items

### Hierarchy

- **Parent:** [EN-206: Context Distribution Strategy](./EN-206-context-distribution-strategy.md)

### Dependencies

- **Depends On:** TASK-002 (sync mechanism implementation)
- **Enables:** TASK-004 (can document verified behavior)

### Traceability

- **Addresses:** NC-002 (unverified platform claims) from nse-qa audit
- **Verifies:** VM-001 through VM-007 from requirements traceability matrix

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-02T09:00:00Z | Claude | pending | Task created from QG-1 gap analysis |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | Task |
| **SAFe** | Task |
| **JIRA** | Task |
