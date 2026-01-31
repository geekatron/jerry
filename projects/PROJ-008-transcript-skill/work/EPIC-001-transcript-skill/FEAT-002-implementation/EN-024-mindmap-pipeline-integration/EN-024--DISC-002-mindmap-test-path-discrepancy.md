# EN-024:DISC-002: Mindmap Test Path Discrepancy

<!--
TEMPLATE: Discovery
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.8
-->

---

## Frontmatter

```yaml
id: "EN-024:DISC-002"
work_type: DISCOVERY
title: "Mindmap Test Path Discrepancy"
description: |
  During EN-024 live skill invocation testing, discovered that mindmap-tests.yaml
  references 07-mindmap/ directory path but ADR-006/DISC-001 corrected this to 08-mindmap/.
classification: ENABLER
status: DOCUMENTED
priority: MEDIUM
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-30T00:00:00Z"
updated_at: "2026-01-30T00:00:00Z"
parent_id: "EN-024"
tags:
  - discovery
  - test-update
  - path-correction
  - mindmap
discovered_during: "TASK-244 live skill invocation"
impact_level: LOW
resolution_required: true
```

---

## Discovery Summary

### What Was Found

During EN-024 live skill invocation testing (TASK-244), the following discrepancy was discovered:

**File:** `skills/transcript/test_data/validation/mindmap-tests.yaml`

**Current Paths (INCORRECT):**
- `07-mindmap/mindmap.mmd` (line 28)
- `07-mindmap/mindmap.ascii.txt` (line 165)
- `07-mindmap/` directory references (lines 437, 450, 465-466, 518)

**Correct Paths (Per ADR-006/DISC-001):**
- `08-mindmap/mindmap.mmd`
- `08-mindmap/mindmap.ascii.txt`
- `08-mindmap/` directory

### Root Cause

The `mindmap-tests.yaml` file was created in EN-009 before DISC-001 identified the artifact numbering discrepancy. When ADR-006 and SKILL.md were updated to use `08-mindmap/`, the test file was not updated.

### Impact

| Impact Area | Severity | Description |
|-------------|----------|-------------|
| Test Execution | Low | Tests will fail path assertions |
| CI/CD | Low | Automated tests would fail |
| Development | Low | Confusing for developers |

---

## Resolution

### Required Changes

Update `skills/transcript/test_data/validation/mindmap-tests.yaml`:

1. Line 28: `07-mindmap/mindmap.mmd` → `08-mindmap/mindmap.mmd`
2. Line 165: `07-mindmap/mindmap.ascii.txt` → `08-mindmap/mindmap.ascii.txt`
3. Line 437: `07-mindmap/mindmap.mmd` → `08-mindmap/mindmap.mmd`
4. Line 450: `07-mindmap/mindmap.ascii.txt` → `08-mindmap/mindmap.ascii.txt`
5. Lines 465-466: Update both file paths
6. Line 518: `07-mindmap/` → `08-mindmap/`

### Blocking Status

- **Does NOT block** TASK-244 (orchestration documentation complete)
- **Does block** TASK-246 (integration tests) - tests need correct paths

### Remediation

Create follow-up task or include in TASK-246 scope.

---

## Related Items

- Parent: [EN-024: Mindmap Pipeline Integration](./EN-024-mindmap-pipeline-integration.md)
- Reference: [DISC-001: Mindmap Directory Numbering](./EN-024--DISC-001-mindmap-directory-numbering-discrepancy.md)
- Reference: [ADR-006](../../../../../docs/adrs/ADR-006-mindmap-pipeline-integration.md)
- Affected File: `skills/transcript/test_data/validation/mindmap-tests.yaml`

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-30 | DOCUMENTED | Discovered during TASK-244 live skill invocation testing |
