# EN-021-004: Governance YAML Behavioral Sync

> **Type:** enabler
> **Status:** in_progress
> **Priority:** high
> **Impact:** high
> **Enabler Type:** compliance
> **Created:** 2026-03-11T00:00:00Z
> **Due:** 2026-03-12T00:00:00Z
> **Completed:** —
> **Parent:** EPIC-021-001
> **Owner:** claude
> **Effort:** 3

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Technical scope |
| [Problem Statement](#problem-statement) | Why this enabler is needed |
| [Business Value](#business-value) | Features unlocked |
| [Technical Approach](#technical-approach) | Implementation plan |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable criteria |
| [Progress Summary](#progress-summary) | Tracking |
| [Related Items](#related-items) | Dependencies |
| [History](#history) | Status changes |

---

## Summary

Sync behavioral guardrails from agent .md system prompts into .governance.yaml machine-readable metadata. The adversary review found that cd-generator's cross-reference validation is documented in the .md guardrails section but incompletely represented in the governance YAML input_validation array.

**Technical Scope:**
- Audit all 6 PROJ-021 agent .governance.yaml files for behavioral/governance sync gaps
- Add missing input_validation entries that mirror .md guardrail constraints
- Establish a principled boundary rule (structural vs. semantic vs. behavioral)

---

## Problem Statement

Adversary finding FM-001 identified that cd-generator's critical cross-reference validation (source_step must exist in referenced flow) is defined in the system prompt but the governance YAML input_validation entry lacked the prerequisite about loading the full UC artifact. A programmatic CI gate reading only the governance YAML would miss this enforcement dependency.

---

## Business Value

### Features Unlocked

- CI-level governance enforcement can trust .governance.yaml as complete
- Agent routing infrastructure has accurate validation metadata
- Reduces dual-maintenance risk between .md and .governance.yaml

---

## Technical Approach

1. Audit all 6 agent pairs for governance/behavioral sync gaps
2. For each gap, determine if the constraint belongs in governance YAML (structural/input validation) or only in .md (semantic/behavioral)
3. Add missing entries per the boundary rule
4. Validate updated governance YAML against schema

---

## Acceptance Criteria

- [ ] All 6 agent .governance.yaml input_validation arrays include prerequisite dependencies for cross-reference checks
- [ ] Boundary rule documented: which constraints go in governance YAML vs. .md only
- [ ] Updated governance YAML files validate against agent-governance-v1.schema.json
- [ ] Adversary quality score >= 0.95

---

## Progress Summary

| Metric | Value |
|--------|-------|
| **Phase** | Batch 1 — Implementation (no design needed) |
| **Implementation** | In progress |
| **Security Review** | Blocked on implementation |
| **Quality Gate** | Blocked on security |

---

## Related Items

- **Parent:** [EPIC-021-001](../EPIC-021-001-use-case-capability-build.md)
- **Source Finding:** FM-001 in adversary-agent-findings.md
- **Analysis:** pm001-fm001-fm002-analysis.md

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-11T00:00:00Z | claude | in_progress | Created from adversary finding FM-001 |
