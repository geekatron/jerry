# TASK-159: Validation - All 8 Domains Load Correctly

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
ENABLER: EN-014 (Domain Context Files Implementation)
DISCOVERY: DISC-005 (EN-006 Artifact Promotion Gap Analysis)
-->

---

## Frontmatter

```yaml
id: "TASK-159"
work_type: TASK
title: "Validation: All 8 Domains Load Correctly"
description: |
  Execute comprehensive validation that all 8 domain context files
  load correctly, pass schema validation, and integrate with the
  transcript skill pipeline.

classification: ENABLER
status: BACKLOG
resolution: null
priority: HIGH
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-28T21:30:00Z"
updated_at: "2026-01-28T21:30:00Z"

parent_id: "EN-014"

tags:
  - "validation"
  - "domain-context"
  - "en006-promotion"
  - "integration-test"
  - "DISC-005"

effort: 1
acceptance_criteria: |
  - All 8 domain YAML files exist and have valid syntax
  - All domain files pass JSON Schema validation (TASK-129, TASK-156)
  - SKILL.md lists all 8 domains correctly
  - Context injection loads each domain without error
  - All 6 SPEC documentation files accessible
  - Domain selection guide accessible
  - No missing file references

due_date: null

activity: TESTING
original_estimate: 2
remaining_work: 2
time_spent: 0
```

---

## State Machine

**Current State:** `BACKLOG`

---

## Content

### Description

Execute final validation that the complete EN-014 scope (original 3 domains + 6 EN-006 promotion domains) is fully integrated and functional. This task validates the entire domain context file infrastructure.

### Validation Matrix

| Test ID | Domain | File | Schema | SKILL.md | SPEC Doc | Status |
|---------|--------|------|--------|----------|----------|--------|
| VAL-001 | general | ✓ | ✓ | ✓ | N/A | [ ] |
| VAL-002 | transcript | ✓ | ✓ | ✓ | N/A | [ ] |
| VAL-003 | meeting | ✓ | ✓ | ✓ | N/A | [ ] |
| VAL-004 | software-engineering | ✓ | ✓ | ✓ | ✓ | [ ] |
| VAL-005 | software-architecture | ✓ | ✓ | ✓ | ✓ | [ ] |
| VAL-006 | product-management | ✓ | ✓ | ✓ | ✓ | [ ] |
| VAL-007 | user-experience | ✓ | ✓ | ✓ | ✓ | [ ] |
| VAL-008 | cloud-engineering | ✓ | ✓ | ✓ | ✓ | [ ] |
| VAL-009 | security-engineering | ✓ | ✓ | ✓ | ✓ | [ ] |
| VAL-010 | DOMAIN-SELECTION-GUIDE | N/A | N/A | ref | ✓ | [ ] |

### Validation Steps

1. **File Existence Check**
   ```
   contexts/
   ├── general.yaml                  ✓
   ├── transcript.yaml               ✓
   ├── meeting.yaml                  ✓
   ├── software-engineering.yaml     ✓
   ├── software-architecture.yaml    ✓
   ├── product-management.yaml       ✓
   ├── user-experience.yaml          ✓
   ├── cloud-engineering.yaml        ✓
   └── security-engineering.yaml     ✓
   ```

2. **Schema Validation**
   - Run JSON Schema validator (TASK-129) against each file
   - Verify no validation errors

3. **SKILL.md Registration**
   - Verify all 8 domains listed in `available_domains`
   - Verify each has `name`, `description`, `file`, and `spec` (where applicable)

4. **Documentation Check**
   - Verify all 6 SPEC-*.md files exist in `docs/domains/`
   - Verify DOMAIN-SELECTION-GUIDE.md exists
   - Verify flowchart renders correctly

5. **Integration Test**
   - Attempt to load each domain via context injection
   - Verify no errors during load
   - Verify template variables resolve

### Acceptance Criteria

- [ ] All 9 domain YAML files exist (including EN-014 original: general, transcript, meeting)
- [ ] All files pass YAML syntax validation
- [ ] All EN-006 domains pass JSON Schema validation (DOMAIN-SCHEMA.json)
- [ ] SKILL.md has all 8 domains in `available_domains`
- [ ] All 6 SPEC documentation files exist
- [ ] DOMAIN-SELECTION-GUIDE.md exists with flowchart
- [ ] Context injection can load each domain without error
- [ ] No broken file references
- [ ] Validation results documented in this file

### Related Items

- Parent: [EN-014: Domain Context Files Implementation](./EN-014-domain-context-files.md)
- Discovery: [DISC-005: EN-006 Artifact Promotion Gap](../FEAT-002--DISC-005-en006-artifact-promotion-gap.md)
- Blocked By: [TASK-158: SKILL.md Update](./TASK-158-skill-md-domain-update.md), [TASK-130: Original Schema Validation](./TASK-130-schema-validation.md)
- Validates: All EN-014 tasks (TASK-126..130, TASK-150..158)
- References: [integration-tests.yaml](../../../../../skills/transcript/test_data/validation/integration-tests.yaml)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Validation results | Evidence | (below) |
| Test execution log | Documentation | (in this file) |

### Test Results

```
[To be filled during task execution]

Domain                   | File Exists | YAML Valid | Schema Valid | In SKILL.md | SPEC Doc
-------------------------|-------------|------------|--------------|-------------|----------
general                  |             |            |              |             | N/A
transcript               |             |            |              |             | N/A
meeting                  |             |            |              |             | N/A
software-engineering     |             |            |              |             |
software-architecture    |             |            |              |             |
product-management       |             |            |              |             |
user-experience          |             |            |              |             |
cloud-engineering        |             |            |              |             |
security-engineering     |             |            |              |             |
```

### Verification

- [ ] All 9 domain files exist
- [ ] All files pass validation
- [ ] SKILL.md complete
- [ ] Documentation complete
- [ ] Integration test passes
- [ ] Reviewed by: (pending)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-28 | Created | Initial task creation per DISC-005 EN-006 artifact promotion |
