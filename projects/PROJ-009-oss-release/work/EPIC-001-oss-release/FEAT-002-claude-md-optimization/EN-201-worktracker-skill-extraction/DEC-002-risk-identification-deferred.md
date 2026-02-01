# EN-201:DEC-002: Risk Identification Deferred to EN-202

<!--
TEMPLATE: Decision
VERSION: 1.0.0
SOURCE: worktracker.md (Decision File), ADR/MADR best practices
CREATED: 2026-02-01 (EN-201 QG-1)
PURPOSE: Document decision to defer explicit risk documentation
-->

> **Type:** decision
> **Status:** ACCEPTED
> **Priority:** medium
> **Created:** 2026-02-01T13:00:00Z
> **Parent:** EN-201
> **Owner:** Claude
> **Related:** EN-202

---

## Summary

During EN-201 QG-1, the nse-qa audit noted that the extracted content lacks explicit risk identification (NCR-008/NCR-009 findings). We decided to defer explicit risk documentation to the EN-202 content rewrite phase, as EN-201's extraction scope doesn't include content authorship.

**Decisions Captured:** 1

**Key Outcomes:**
- EN-201 extraction scope preserved
- Risk documentation requirement noted for EN-202
- NPR 7123.1D 6.4.6 (Technical Risk Management) addressed via deferral

---

## Decision Context

### Background

The nse-qa QG-1 audit evaluated extracted content against NPR 7123.1D requirements. Section 6.4.6 (Technical Risk Management) requires identification of risks. The extracted worktracker content doesn't explicitly document risks - it describes behavior rules but not "what could go wrong."

The auditor noted this as a PARTIAL compliance finding with the recommendation to address during EN-202.

### Constraints

- EN-201 scope is extraction (verbatim content transfer)
- Adding risk documentation would be content authorship
- EN-202 is the content rewrite/improvement phase
- NPR 7123.1D compliance is desirable but extraction-scoped

### Stakeholders

| Stakeholder | Role | Interest |
|-------------|------|----------|
| Claude | Implementer | Scope clarity |
| nse-qa | Auditor | NPR 7123.1D compliance |
| User | Requester | Quality documentation |

---

## Decisions

### D-001: Risk Documentation Deferred to EN-202

**Date:** 2026-02-01T13:00:00Z
**Participants:** Claude, nse-qa (audit)

#### Question/Context

During QG-1, nse-qa noted the extracted content lacks explicit risk identification per NPR 7123.1D 6.4.6. Should EN-201 add risk documentation, or defer to EN-202?

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | Add risk documentation in EN-201 | Higher compliance score | Scope creep, not extraction |
| **B** | Defer to EN-202 | Clean extraction scope | Temporary compliance gap |
| **C** | Create separate enabler for risks | Explicit tracking | Over-engineering |

#### Decision

**We decided:** Option B - Defer explicit risk documentation to EN-202 content rewrite.

#### Rationale

1. **Scope Preservation**: EN-201 is "extraction" - adding risk documentation is content authorship, which belongs in EN-202 "rewrite".
2. **Documented Deferral**: The decision is explicitly documented, creating accountability.
3. **Practical Impact**: The extracted content still functions; risks are implicit in behavior rules.
4. **Compliance Path**: EN-202 acceptance criteria should include risk documentation.

#### Implications

- **Positive:** Clean extraction scope, clear EN-202 requirements
- **Negative:** Temporary NPR 7123.1D partial compliance
- **Follow-up required:** EN-202 should add "Add explicit risk identification" to acceptance criteria

---

## Decision Summary

| ID | Decision | Date | Status |
|----|----------|------|--------|
| D-001 | Defer risk documentation to EN-202 | 2026-02-01 | ACCEPTED |

---

## Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Parent | [EN-201](./EN-201-worktracker-skill-extraction.md) | Parent enabler |
| Target | [EN-202](../EN-202-claude-md-rewrite/EN-202-claude-md-rewrite.md) | Content rewrite enabler |
| Evidence | quality-gates/qg-1/nse-qa-audit-v3.md | NPR 6.4.6 partial compliance |

---

## NPR 7123.1D Reference

### Section 6.4.6: Technical Risk Management

The extracted worktracker content provides behavior rules but doesn't explicitly document:
- What could go wrong if rules aren't followed
- Likelihood and impact of violations
- Mitigation strategies

**Suggested additions for EN-202:**

| Rule | Risk if Violated | Mitigation |
|------|------------------|------------|
| WORKTRACKER.md is SSOT | Inconsistent tracking | Validation scripts |
| Template usage mandatory | Format drift | Template checks |
| Folder structure required | Lost artifacts | CI validation |

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-02-01T14:30:00Z | Claude | Created decision document |

---

## Metadata

```yaml
id: "EN-201:DEC-002"
parent_id: "EN-201"
work_type: DECISION
title: "Risk Identification Deferred to EN-202"
status: ACCEPTED
priority: MEDIUM
created_by: "Claude"
created_at: "2026-02-01T13:00:00Z"
updated_at: "2026-02-01T14:30:00Z"
decided_at: "2026-02-01T13:00:00Z"
participants: [Claude, nse-qa]
tags: [risk, npr-7123, compliance, deferral]
decision_count: 1
superseded_by: null
supersedes: null
```
