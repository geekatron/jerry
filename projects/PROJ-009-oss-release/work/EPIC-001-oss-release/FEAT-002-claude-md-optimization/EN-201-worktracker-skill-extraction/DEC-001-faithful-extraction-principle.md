# EN-201:DEC-001: Faithful Extraction Preserves Source Defects

<!--
TEMPLATE: Decision
VERSION: 1.0.0
SOURCE: worktracker.md (Decision File), ADR/MADR best practices
CREATED: 2026-02-01 (EN-201 QG-1)
PURPOSE: Document decision to preserve source defects during extraction
-->

> **Type:** decision
> **Status:** ACCEPTED
> **Priority:** high
> **Created:** 2026-02-01T12:00:00Z
> **Parent:** EN-201
> **Owner:** Claude
> **Related:** EN-202

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overview of 2 decisions |
| [Decision Context](#decision-context) | Background, constraints, stakeholders |
| [Decisions](#decisions) | D-001 and D-002 detailed decisions |
| [Decision Summary](#decision-summary) | Quick reference table |
| [Related Artifacts](#related-artifacts) | Parent, bugs, evidence |
| [Document History](#document-history) | Change log |

---

## Summary

During EN-201 worktracker skill extraction, we decided that extraction should preserve source defects verbatim rather than fix them. Source defects are documented and deferred to the content rewrite phase (EN-202).

**Decisions Captured:** 2

**Key Outcomes:**
- Extraction maintains content fidelity (no silent changes)
- Source defects are explicitly documented
- Fixes are tracked in the appropriate enabler (EN-202)

---

## Decision Context

### Background

EN-201 extracted the `<worktracker>` section from CLAUDE.md into `skills/worktracker/` rule files. During extraction, multiple defects were discovered in the source CLAUDE.md:
- BUG-001: "relationships to to" typo
- BUG-002: {EnablerId} used for Story folders
- BUG-003: Template path inconsistency

The question arose: should extraction fix these defects, or preserve them?

### Constraints

- EN-201 scope is "extraction" not "rewrite"
- EN-202 is specifically for CLAUDE.md content rewrite
- Fixing during extraction could introduce errors
- Unfixed defects could propagate to skill users

### Stakeholders

| Stakeholder | Role | Interest |
|-------------|------|----------|
| Claude | Implementer | Clean extraction process |
| User | Requester | Quality outcome |
| nse-qa | Auditor | Traceability and compliance |

---

## Decisions

### D-001: Extraction Preserves Source Verbatim

**Date:** 2026-02-01T12:00:00Z
**Participants:** Claude, nse-qa (audit)

#### Question/Context

During QG-1 iteration 1, nse-qa identified defects in the extracted content. The question: should extraction fix these defects, or are they "faithful extraction" of source defects?

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | Fix defects during extraction | Clean extracted files | Scope creep, potential new errors, unclear source tracing |
| **B** | Preserve defects verbatim | Clear traceability, separation of concerns | Defects propagate temporarily |

#### Decision

**We decided:** Option B - Preserve source defects verbatim in extracted content.

#### Rationale

1. **Separation of Concerns**: EN-201 is "extraction", EN-202 is "rewrite". Mixing them violates single responsibility.
2. **Traceability**: Faithful extraction allows audit trail from source to extracted file.
3. **Risk Reduction**: Fixing during extraction could introduce new errors.
4. **Explicit Documentation**: Defects are explicitly documented as bugs for EN-202.

#### Implications

- **Positive:** Clear audit trail, clean separation of work
- **Negative:** Temporary defect propagation until EN-202
- **Follow-up required:** BUG-001, BUG-002, BUG-003 created for EN-202

---

### D-002: Defects Documented as Bugs for EN-202

**Date:** 2026-02-01T12:00:00Z
**Participants:** Claude, User

#### Question/Context

How should discovered source defects be tracked to ensure they get fixed?

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | Document in EN-201 only | Simple | May be forgotten |
| **B** | Create bugs in EN-202 | Explicit tracking, clear ownership | More artifacts |
| **C** | Create bugs in FEAT-002 | Feature-level visibility | Wrong granularity |

#### Decision

**We decided:** Option B - Create bug work items in EN-202 enabler folder.

#### Rationale

1. **Ownership**: EN-202 is responsible for CLAUDE.md content rewrite
2. **Traceability**: Bugs are linked to their fix location
3. **Visibility**: EN-202 task list will include these fixes
4. **Completeness**: EN-202 cannot be marked complete without addressing bugs

---

## Decision Summary

| ID | Decision | Date | Status |
|----|----------|------|--------|
| D-001 | Preserve source defects verbatim during extraction | 2026-02-01 | ACCEPTED |
| D-002 | Create bug work items in EN-202 for source defects | 2026-02-01 | ACCEPTED |

---

## Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Parent | [EN-201](./EN-201-worktracker-skill-extraction.md) | Parent enabler |
| Bug | [EN-202:BUG-001](../EN-202-claude-md-rewrite/BUG-001-relationships-typo.md) | Typo bug |
| Bug | [EN-202:BUG-002](../EN-202-claude-md-rewrite/BUG-002-story-folder-id-mismatch.md) | ID mismatch bug |
| Bug | [EN-202:BUG-003](../EN-202-claude-md-rewrite/BUG-003-template-path-inconsistency.md) | Path inconsistency bug |
| Evidence | quality-gates/qg-1/nse-qa-audit-v3.md | QG-1 audit documenting defects |

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-02-01T14:30:00Z | Claude | Created decision document |

---

## Metadata

```yaml
id: "EN-201:DEC-001"
parent_id: "EN-201"
work_type: DECISION
title: "Faithful Extraction Preserves Source Defects"
status: ACCEPTED
priority: HIGH
created_by: "Claude"
created_at: "2026-02-01T12:00:00Z"
updated_at: "2026-02-01T14:30:00Z"
decided_at: "2026-02-01T12:00:00Z"
participants: [Claude, User, nse-qa]
tags: [extraction, fidelity, defects]
decision_count: 2
superseded_by: null
supersedes: null
```
