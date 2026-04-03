# BUG-021-002: cd-generator Accepts Malformed Interaction Descriptions

> **Type:** bug
> **Status:** in_progress
> **Priority:** high
> **Impact:** high
> **Severity:** major
> **Created:** 2026-03-11T00:00:00Z
> **Due:** 2026-03-12T00:00:00Z
> **Completed:**
> **Parent:** EPIC-021-001
> **Owner:** claude
> **Found In:** 1.0.0
> **Fix Version:** 1.0.1

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description |
| [Steps to Reproduce](#steps-to-reproduce) | How to trigger the bug |
| [Environment](#environment) | Where the bug occurs |
| [Root Cause Analysis](#root-cause-analysis) | Investigation |
| [Acceptance Criteria](#acceptance-criteria) | Fix verification |
| [Related Items](#related-items) | Dependencies |
| [History](#history) | Status changes |

---

## Summary

cd-generator accepts a semantically malformed $.interactions block where all 7 required fields are present but contain placeholder text (e.g., "TBD", "TODO"). It produces a structurally valid but semantically incorrect OpenAPI contract. The x-prototype: true label is the only safety gate; no pre-validation of description quality exists.

**Key Details:**
- **Symptom:** Generated OpenAPI contract has meaningless operation descriptions derived from placeholder interaction text
- **Frequency:** Occurs when uc-slicer produces interactions with placeholder descriptions
- **Workaround:** x-prototype: true flag signals the contract is not production-ready

---

## Steps to Reproduce

### Prerequisites

- Use case artifact with interactions[] where request_description = "TBD"
- cd-generator invoked on this artifact

### Steps to Reproduce

1. Create a use case artifact with realization_level: INTERACTION_DEFINED
2. Set interactions[0].request_description to "TBD" and response_description to "placeholder"
3. Invoke cd-generator on this artifact
4. Observe the generated OpenAPI contract

### Expected Result

cd-generator rejects the input or warns about low-quality interaction descriptions

### Actual Result

cd-generator accepts the input and produces an OpenAPI contract with placeholder-derived operation descriptions

---

## Environment

| Attribute | Value |
|-----------|-------|
| **Framework** | Jerry Framework v0.24.0 |
| **Agent** | cd-generator v1.0.0 |
| **Schema** | use-case-realization-v1.schema.json |

---

## Root Cause Analysis

### Root Cause

The input validation in cd-generator only checks structural presence (all 7 required fields exist, minLength: 1) but does not validate semantic quality of request_description and response_description fields.

### Contributing Factors

- Schema uses minLength: 1 which accepts single-character strings
- No quality heuristic for interaction description text
- x-prototype flag is a downstream safety net, not an input gate

---

## Acceptance Criteria

- [ ] cd-generator input validation rejects descriptions shorter than 10 characters
- [ ] cd-generator input validation rejects descriptions containing only placeholder terms (TBD, TODO, placeholder, N/A)
- [ ] cd-generator SKILL.md documents description quality requirements
- [ ] Governance YAML input_validation includes description quality check
- [ ] Adversary quality score >= 0.95

---

## Related Items

- **Parent:** [EPIC-021-001](../EPIC-021-001-use-case-capability-build.md)
- **Source Finding:** IN-001 in adversary-skill-findings.md
- **Depends On:** ps-architect design decision for validation criteria

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-11T00:00:00Z | claude | in_progress | Created from adversary finding IN-001 |
