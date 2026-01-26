# Acceptance Criteria: Software Architecture Domain

<!--
DOCUMENT: acceptance-criteria.md
VERSION: 1.0.0
DOMAIN: software-architecture
TASK: TASK-038 (Phase 3)
STATUS: DESIGN COMPLETE
-->

---

## Acceptance Criteria Matrix

| ID | Criterion | Verification Method | Status |
|----|-----------|---------------------|--------|
| **SA-AC-001** | Entity definitions cover: architectural_decision, alternative, quality_attribute, component, technical_debt | Schema validation | ✅ Pass |
| **SA-AC-002** | Each entity has ≥4 meaningful attributes | Manual review | ✅ Pass |
| **SA-AC-003** | Extraction rules align with ADR terminology (Nygard format) | Domain expert review | ✅ Pass |
| **SA-AC-004** | Patterns capture decision rationale and alternatives | Pattern analysis | ✅ Pass |
| **SA-AC-005** | Prompt template supports ADR generation workflow | Workflow review | ✅ Pass |
| **SA-AC-006** | Quality attributes list covers ISO 25010 categories | Standard compliance | ✅ Pass |
| **SA-AC-007** | Output format supports downstream ADR document generation | Schema validation | ✅ Pass |
| **SA-AC-008** | Validation criteria defined for transcript testing | Checklist review | ✅ Pass |

---

## Detailed Verification

### SA-AC-001: Entity Coverage

**Criterion:** Entity definitions cover 5 types

**Evidence:**
```yaml
entities:
  architectural_decision: ✓ Defined with 6 attributes
  alternative: ✓ Defined with 5 attributes
  quality_attribute: ✓ Defined with 5 attributes
  component: ✓ Defined with 5 attributes
  technical_debt: ✓ Defined with 5 attributes
```

**Result:** ✅ Pass (5/5 entities defined)

---

### SA-AC-002: Attribute Completeness

**Criterion:** Each entity has ≥4 meaningful attributes

**Evidence:**

| Entity | Attribute Count | Attributes |
|--------|-----------------|------------|
| architectural_decision | 6 | title, context, decision, consequences, status, adr_number |
| alternative | 5 | title, description, pros, cons, rejection_reason |
| quality_attribute | 5 | attribute, requirement, priority, trade_offs, measurement |
| component | 5 | name, responsibility, interfaces, constraints, technology |
| technical_debt | 5 | description, impact, remediation, priority, cost |

**Result:** ✅ Pass (all entities have ≥4 attributes)

---

### SA-AC-003: ADR Terminology Alignment

**Criterion:** Extraction rules align with ADR terminology (Nygard format)

**Evidence:**

| ADR Section | Extraction Support |
|-------------|-------------------|
| Title | ✓ `title` attribute in architectural_decision |
| Context | ✓ `context` attribute captures problem statement |
| Decision | ✓ `decision` attribute captures response |
| Status | ✓ `status` with ADR states (proposed/accepted/etc.) |
| Consequences | ✓ `consequences` with positive/negative split |

**Result:** ✅ Pass (Nygard format fully supported)

---

### SA-AC-004: Rationale and Alternatives

**Criterion:** Patterns capture decision rationale and alternatives

**Evidence:**

| Pattern Type | Count | Examples |
|--------------|-------|----------|
| Decision + rationale | 2 | "We chose {X} because {Y}" |
| Alternatives | 6 | "We considered", "Another option", "We rejected" |
| Rejection reasons | 2 | "rejected because", "ruled out" |

**Result:** ✅ Pass (rationale and alternatives captured)

---

### SA-AC-005: ADR Generation Workflow

**Criterion:** Prompt template supports ADR generation workflow

**Evidence:**

- ✓ Extraction instructions map to ADR sections
- ✓ Output schema includes `adr_draft` section
- ✓ ADR-specific variant prompt provided
- ✓ Guidelines mention ADR alignment

**Result:** ✅ Pass (ADR workflow supported)

---

### SA-AC-006: ISO 25010 Coverage

**Criterion:** Quality attributes list covers ISO 25010 categories

**Evidence:**

| ISO 25010 Category | Covered |
|--------------------|---------|
| Performance Efficiency | ✓ |
| Security | ✓ |
| Maintainability | ✓ |
| Reliability | ✓ |
| Compatibility | ✓ |
| Usability | ✓ |
| Portability | ✓ |
| Functional Suitability | ✓ |

**Result:** ✅ Pass (all 8 categories covered)

---

### SA-AC-007: ADR Document Generation

**Criterion:** Output format supports downstream ADR document generation

**Evidence:**

- ✓ `adr_draft` section in output schema
- ✓ Structured consequences (positive/negative)
- ✓ Alternatives with pros/cons/rejection_reason
- ✓ Status field with ADR states

**Result:** ✅ Pass (ADR generation supported)

---

### SA-AC-008: Validation Criteria

**Criterion:** Validation criteria defined for transcript testing

**Evidence:**

This document defines validation criteria. Transcript testing criteria for FEAT-002:

| Test ID | Test Description | Expected Result |
|---------|------------------|-----------------|
| TT-SA-001 | Extract decisions from architecture review | ≥80% recall |
| TT-SA-002 | Extract alternatives with rejection reasons | ≥75% recall |
| TT-SA-003 | Quality attribute categorization | ≥85% accuracy |
| TT-SA-004 | ADR draft generation | Nygard-compliant output |

**Result:** ✅ Pass (validation criteria defined)

---

## Summary

| Category | Criteria | Passed | Failed |
|----------|----------|--------|--------|
| Design Criteria | 8 | 8 | 0 |
| Testing Criteria | 4 | Deferred | Deferred |

**Overall Status:** ✅ Design Complete (8/8 criteria passed)

---

*Document ID: VAL-SA-001*
*Domain: software-architecture*
*Task: TASK-038*
*Status: DESIGN COMPLETE*
