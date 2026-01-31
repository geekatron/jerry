# TASK-173: Add Semantic Validator Implementation Reference

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
ENABLER: EN-014 (Domain Context Files Implementation)
WORKFLOW: EN-014--WORKFLOW-schema-extension.md
ISSUE: ps-critic MINOR-003, DISC-007
-->

---

## Frontmatter

```yaml
id: "TASK-173"
work_type: TASK
title: "Add Semantic Validator Implementation Reference"
description: |
  Address ps-critic MINOR-003 and DISC-007: Add reference in TDD Section 5.2 or 7
  indicating where semantic validators will be implemented (module location,
  technology choice, integration approach).

classification: ENABLER
status: DONE
resolution: COMPLETED
priority: HIGH
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-29T12:30:00Z"
updated_at: "2026-01-29T12:30:00Z"

parent_id: "EN-014"

tags:
  - "tdd-improvement"
  - "validation"
  - "implementation"
  - "ps-critic-minor-003"
  - "disc-007"

effort: 2
acceptance_criteria: |
  - TDD Section 5.2 or 7 updated with validator implementation reference
  - Technology approach documented (Python jsonschema recommended)
  - Module location specified (e.g., src/domain/validation/)
  - Integration point in pipeline clarified
  - ps-critic MINOR-003 addressed
  - DISC-007 IMPL-001, IMPL-002, IMPL-003 partially addressed

due_date: null

activity: DOCUMENTATION
original_estimate: 2
remaining_work: 0
time_spent: 2
```

---

## State Machine

**Current State:** `DONE`

```
BACKLOG → IN_PROGRESS → DONE
              ↓
           BLOCKED
```

---

## Content

### Description

This task addresses ps-critic MINOR-003 from the TASK-167 quality review and DISC-007:

> **MINOR-003: Missing Semantic Validator Implementation Reference**
>
> While semantic validation rules SV-001 through SV-006 are documented, there is no
> reference to where the custom validators will be implemented (e.g., Python module,
> JavaScript plugin).
>
> **Recommendation:** Add note in Section 5.2 or Section 7 indicating that semantic
> validators will be implemented as part of TASK-170 or a subsequent enabler.

### Required Changes

**Location:** `docs/design/TDD-EN014-domain-schema-v2.md` Section 5.2 or Section 7

**Content to Add:**

```markdown
### 5.2.1 Implementation Approach

Semantic validators will be implemented as a Python module integrated into the
domain context loading pipeline:

| Aspect | Specification |
|--------|---------------|
| **Language** | Python 3.11+ |
| **Library** | `jsonschema` (Python) for structural, custom code for semantic |
| **Module Location** | `skills/transcript/validation/semantic_validator.py` |
| **Integration Point** | After structural JSON Schema validation, before context injection |

#### Validation Pipeline Flow

```
Domain YAML File
      │
      ▼
┌─────────────────┐
│ JSON Schema     │  ← Structural validation (jsonschema library)
│ Validation      │
└────────┬────────┘
         │ PASS
         ▼
┌─────────────────┐
│ Semantic        │  ← Custom validators (SV-001 through SV-006)
│ Validation      │
└────────┬────────┘
         │ PASS
         ▼
┌─────────────────┐
│ Context         │  ← Inject into agent prompt
│ Injection       │
└─────────────────┘
```

#### Validator Function Signatures

```python
# skills/transcript/validation/semantic_validator.py

def validate_semantic(domain_data: dict) -> ValidationResult:
    """Run all semantic validation rules."""
    ...

def sv001_required_entities(domain_data: dict) -> list[ValidationError]:
    """SV-001: Required entities must exist in entity_definitions."""
    ...

def sv006_circular_relationships(domain_data: dict) -> list[ValidationError]:
    """SV-006: Detect circular relationships using DFS."""
    ...
```

**Note:** Full implementation details will be specified in a future implementation
enabler. This TDD defines WHAT to validate; implementation enabler will define HOW.
```

### Technology Selection Rationale

| Option | Pros | Cons | Recommendation |
|--------|------|------|----------------|
| Python (`jsonschema`) | Native to Jerry framework, no runtime dependency | Slower than ajv | **RECOMMENDED** |
| JavaScript (`ajv`) | Faster validation | Requires Node.js runtime | Not recommended |

**Rationale:** Jerry framework is Python-based. Adding JavaScript dependency for validation would:
1. Introduce runtime complexity
2. Break architectural consistency
3. Complicate deployment

### Dependencies

**Blocked By:** None

**Blocks:**
- TASK-170: TDD Adversarial Review (must address minor issues first)

### Related Discoveries

This task partially addresses DISC-007 gaps:
- **IMPL-001 (Technology Selection):** Documented Python/jsonschema choice
- **IMPL-002 (Validator Location):** Specified module path
- **IMPL-003 (Execution Context):** Specified pipeline integration point

### Acceptance Criteria

- [ ] TDD Section 5.2 or 7 updated with implementation reference
- [ ] Technology choice documented (Python/jsonschema)
- [ ] Module location specified
- [ ] Pipeline integration point defined
- [ ] Validator function signatures outlined
- [ ] ps-critic MINOR-003 addressed

### Related Items

- Parent: [EN-014: Domain Context Files Implementation](./EN-014-domain-context-files.md)
- Issue Source: [en014-task167-iter1-critique.md](./critiques/en014-task167-iter1-critique.md) MINOR-003
- Discovery: [DISC-007: TDD Validation Implementation Gap](./EN-014--DISC-007-tdd-validation-implementation-gap.md)
- Blocks: [TASK-170: TDD Adversarial Review](./TASK-170-tdd-adversarial-review.md)

---

## Time Tracking

| Metric            | Value    |
|-------------------|----------|
| Original Estimate | 2 hours  |
| Remaining Work    | 2 hours  |
| Time Spent        | 0 hours  |

---

## Evidence

### Deliverables

| Deliverable | Type | Link | Status |
|-------------|------|------|--------|
| TDD Implementation Reference | Markdown | docs/design/TDD-EN014-domain-schema-v2.md | DONE |

### Verification

- [ ] Implementation approach documented
- [ ] Technology choice justified
- [ ] Module location specified
- [ ] Pipeline diagram added
- [ ] Reviewed by: (self-review)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-29 | Created | Created per DISC-007 and ps-critic MINOR-003 |
| 2026-01-29 | DONE | Added Section 5.2.1 Semantic Validator Implementation with Python/jsonschema reference, module location, pipeline diagram, and implementation skeleton. ps-critic MINOR-003 and DISC-007 IMPL-001/002/003 addressed. |
