# EN-014:DISC-007: TDD Validation Implementation Gap

<!--
TEMPLATE: Discovery
VERSION: 1.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9, worktracker.md (Discovery File)
CREATED: 2026-01-29 (EN-014 Schema Extension Workflow)
PURPOSE: Document gap in TDD regarding validation tool implementation details
TRIGGER: User review and ps-critic/nse-qa quality assessments identified missing implementation specifics
-->

> **Type:** discovery
> **Status:** DOCUMENTED
> **Priority:** HIGH
> **Impact:** HIGH
> **Created:** 2026-01-29T12:30:00Z
> **Completed:** 2026-01-29T12:30:00Z
> **Parent:** EN-014
> **Owner:** Claude
> **Source:** User review, ps-critic MINOR-003, nse-qa NC-m-002

---

## Frontmatter

```yaml
id: "EN-014:DISC-007"
work_type: DISCOVERY
title: "TDD Validation Implementation Gap"

classification: TECHNICAL

status: DOCUMENTED
resolution: null

priority: HIGH
impact: HIGH

assignee: "Claude"
created_by: "Claude"

created_at: "2026-01-29T12:30:00Z"
updated_at: "2026-01-29T12:30:00Z"
completed_at: "2026-01-29T12:30:00Z"

parent_id: "EN-014"

tags:
  - "validation"
  - "implementation-gap"
  - "ajv"
  - "jsonschema"
  - "semantic-validation"
  - "tdd-improvement"

finding_type: GAP
confidence_level: HIGH
source: "User review, ps-critic MINOR-003, nse-qa NC-m-002"
research_method: "Quality review analysis"

validated: true
validation_date: "2026-01-29T12:30:00Z"
validated_by: "User + Claude"
```

---

## State Machine

**Current State:** `DOCUMENTED`

```
PENDING → IN_PROGRESS → DOCUMENTED
                            ↑
                       (completed)
```

---

## Summary

**Core Finding:** The TDD-EN014-domain-schema-v2.md references validation tools (ajv, jsonschema) and defines 6 semantic validation rules (SV-001 through SV-006), but **does not specify HOW these validators will be implemented**. The document lacks:

1. **Technology Selection** - No decision on JavaScript (ajv) vs Python (jsonschema) implementation
2. **Script/Module Location** - No specification of where validation code will reside
3. **Execution Context** - No definition of when/how validators are invoked in the pipeline
4. **Algorithm Details** - Complex rules like SV-006 (circular relationship detection) lack implementation approach

**Key Findings:**
1. TDD Section 5.2 defines semantic validation rules SV-001 through SV-006 as "Custom Validators" without implementation details
2. Performance estimates (5ms to 8ms) are not benchmarked, making implementation planning uncertain
3. The gap between WHAT to validate and HOW to validate creates risk for implementation tasks

**Validation:** Confirmed by user review, ps-critic MINOR-003, nse-qa NC-m-002

---

## Context

### Background

During the final adversarial review preparation (TASK-168), the user identified that the TDD references validation tools and rules but does not explain how they will be implemented. The ps-critic review (TASK-167, score 0.93) and nse-qa review (score 0.91) both flagged related minor issues:

- **ps-critic MINOR-003:** "Missing Semantic Validator Implementation Reference - While semantic validation rules SV-001 through SV-006 are documented, there is no reference to where the custom validators will be implemented"
- **nse-qa NC-m-002:** "Semantic validation rule SV-006 (circular relationship detection) lacks implementation details"

### Research Question

**What implementation details are missing from TDD Section 5.2 that would enable developers to implement the semantic validation rules?**

### Investigation Approach

1. Read TDD Section 5.2 (Semantic Validation)
2. Identify gaps between rule specification and implementation guidance
3. Document the specific missing elements
4. Link to related quality review findings

---

## Finding

### Gap 1: Technology Selection Not Documented

**Source:** TDD Section 5.1, 5.2, 8 (References)

The TDD references two validation libraries:
- `ajv` (JavaScript) - Reference #4 in TDD
- `jsonschema` (Python) - Reference #5 in TDD

**What's Missing:**
- Decision on which library/language to use for implementation
- Rationale for technology choice given Jerry framework's Python base
- Whether JavaScript (ajv) would require Node.js runtime dependency

**Impact:**
- Implementation tasks cannot begin without technology decision
- Potential architectural inconsistency (Python framework + JavaScript validation)

### Gap 2: Semantic Validator Location Not Specified

**Source:** TDD Section 5.2, Section 7 (Implementation Notes)

The TDD documents 6 semantic validation rules but does not specify:
- File path for validator module (e.g., `src/domain/validation/semantic_validator.py`)
- Class/function structure for validators
- Integration point with schema validation pipeline

**Current TDD Content (Section 5.2):**
```
Semantic Validation (Custom Validators)
These rules require custom validation logic beyond JSON Schema:

| Rule | Description | Check Type |
|------|-------------|------------|
| SV-001 | Required entities must exist in entity_definitions | Cross-reference |
| SV-002 | Relationship target must be valid entity name | Cross-reference |
| SV-003 | Context rule entities must be defined | Cross-reference |
| SV-004 | extraction_threshold must be 0.0-1.0 | Range validation |
| SV-005 | quality_gate threshold must be 0.0-1.0 | Range validation |
| SV-006 | Circular relationship detection | Graph analysis |
```

**What's Missing:**
- Module/file location for implementation
- Function signatures for each validator
- Error handling approach

### Gap 3: Execution Context Not Defined

**Source:** TDD Section 7 (Implementation Notes)

Section 7 describes context injection pipeline updates but does not specify:
- When semantic validation runs (before/after schema validation?)
- Error handling for semantic validation failures
- Whether validation is blocking or warning-only

**Impact:**
- Pipeline integration unclear
- Risk of inconsistent validation behavior

### Gap 4: SV-006 Algorithm Not Specified

**Source:** TDD Section 5.2

SV-006 (Circular relationship detection) is documented as requiring "Graph analysis" but:
- No algorithm specified (DFS, topological sort, etc.)
- No pseudocode provided
- No complexity analysis
- No edge cases documented

**Impact:**
- Complex validation rule with no implementation guidance
- Risk of incorrect or inefficient implementation

---

## Evidence

### Source Documentation

| Evidence ID | Type | Description | Source | Date |
|-------------|------|-------------|--------|------|
| E-001 | TDD | TDD-EN014-domain-schema-v2.md Section 5.2 | docs/design/TDD-EN014-domain-schema-v2.md | 2026-01-29 |
| E-002 | Critique | ps-critic MINOR-003 finding | critiques/en014-task167-iter1-critique.md:250-258 | 2026-01-29 |
| E-003 | QA | nse-qa NC-m-002 finding | qa/en014-task167-iter1-qa.md:229-232 | 2026-01-29 |
| E-004 | User | User feedback on validation implementation gap | Session transcript | 2026-01-29 |

### Gap Summary Matrix

| Gap ID | Feature | TDD Documents | TDD Specifies Implementation | Gap Type |
|--------|---------|---------------|------------------------------|----------|
| IMPL-001 | Technology Selection | Tools referenced | ❌ No decision | Technology decision |
| IMPL-002 | Validator Location | Rules documented | ❌ No location | Architecture gap |
| IMPL-003 | Execution Context | Pipeline mentioned | ❌ No timing/integration | Pipeline gap |
| IMPL-004 | SV-006 Algorithm | Rule described | ❌ No algorithm | Algorithm gap |

---

## Implications

### Impact on Project

The validation implementation gap affects:

1. **TASK-170 (TDD Adversarial Review)** - Cannot achieve 0.95 score without addressing gaps
2. **TASK-168 (Final Adversarial Review)** - TDD improvements required before completion
3. **Future Implementation** - Implementation tasks will lack clear guidance

### Design Decisions Affected

| Decision | Impact | Required Action |
|----------|--------|-----------------|
| Validation technology | Not decided | Update ADR-EN014-001 OR create new ADR |
| Pipeline integration | Undefined | Update TDD Section 5.2 or 7 |

### Risks Identified

| Risk | Severity | Mitigation |
|------|----------|------------|
| Implementation tasks start without clear guidance | MEDIUM | Address in TDD before implementation phase |
| Wrong technology choice impacts architecture | MEDIUM | Document decision with rationale in ADR |
| SV-006 implemented incorrectly | LOW | Provide algorithm/pseudocode in TDD |

### Opportunities Created

- **Improved TDD Quality** - Addressing gaps will raise TDD quality score
- **Implementation Clarity** - Clear implementation guidance reduces implementation risk
- **Reusable Patterns** - Validation patterns can be reused for future schema extensions

---

## Relationships

### Creates

- [TASK-173](./TASK-173-semantic-validator-reference.md) - Add semantic validator implementation reference (addresses ps-critic MINOR-003)
- [TASK-175](./TASK-175-sv006-implementation-details.md) - Add SV-006 implementation details (addresses nse-qa NC-m-002)

### Informs

- [TASK-170](./TASK-170-tdd-adversarial-review.md) - TDD Adversarial Review (nse-reviewer)
- [TASK-168](./TASK-168-final-adversarial-review.md) - Final Adversarial Review

### Related Discoveries

- [EN-014:DISC-006](./EN-014--DISC-006-schema-gap-analysis.md) - Schema Gap Analysis (parent discovery)

### Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Parent | [EN-014-domain-context-files.md](./EN-014-domain-context-files.md) | Parent enabler |
| TDD | [TDD-EN014-domain-schema-v2.md](./docs/design/TDD-EN014-domain-schema-v2.md) | Document with gaps |
| Critique | [en014-task167-iter1-critique.md](./critiques/en014-task167-iter1-critique.md) | ps-critic findings |
| QA | [en014-task167-iter1-qa.md](./qa/en014-task167-iter1-qa.md) | nse-qa findings |

---

## Recommendations

### Immediate Actions

1. **TASK-173:** Add semantic validator implementation reference to TDD Section 5.2 or 7
2. **TASK-175:** Add SV-006 algorithm/pseudocode to TDD Section 5.2
3. **Consider ADR Update:** If technology selection decision is needed, update ADR-EN014-001

### Long-term Considerations

- **Validation Module Design:** When implementation phase begins, create dedicated validation module
- **Benchmark Suite:** Create validation performance benchmarks to verify estimates
- **Test Coverage:** Ensure semantic validators have comprehensive test coverage

---

## Open Questions

### Questions for Follow-up

1. **Q:** Should technology selection (ajv vs jsonschema) be added to ADR-EN014-001 or remain in TDD?
   - **Investigation Method:** Architectural review
   - **Priority:** HIGH - Affects TASK-173 content

2. **Q:** Is the 5ms to 8ms performance estimate acceptable, or should benchmarks be required before approval?
   - **Investigation Method:** Performance testing
   - **Priority:** MEDIUM - Addressed by TASK-174

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-29 | Claude | Created discovery document from user feedback and quality review findings |

---

## Metadata

```yaml
id: "EN-014:DISC-007"
parent_id: "EN-014"
work_type: DISCOVERY
title: "TDD Validation Implementation Gap"
status: DOCUMENTED
priority: HIGH
impact: HIGH
created_by: "Claude"
created_at: "2026-01-29T12:30:00Z"
updated_at: "2026-01-29T12:30:00Z"
completed_at: "2026-01-29T12:30:00Z"
tags: ["validation", "implementation-gap", "ajv", "jsonschema", "semantic-validation", "tdd-improvement"]
source: "User review, ps-critic MINOR-003, nse-qa NC-m-002"
finding_type: GAP
confidence_level: HIGH
validated: true
creates:
  - "TASK-173"
  - "TASK-175"
informs:
  - "TASK-170"
  - "TASK-168"
related_discoveries:
  - "EN-014:DISC-006"
```
