# FEAT-025: Go Public (Repository Visibility & Community Health)

<!--
TEMPLATE: Feature
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.3
CREATED: 2026-02-18 (Claude)
PURPOSE: Flip Jerry repository from private to public with all community health files
-->

> **Type:** feature
> **Status:** in_progress
> **Priority:** high
> **Impact:** high
> **Created:** 2026-02-18
> **Due:** --
> **Completed:** ---
> **Parent:** EPIC-001-oss-release
> **Owner:** --

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this feature delivers |
| [Enablers](#enablers) | Implementation work items |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Progress Summary](#progress-summary) | Tracking |
| [History](#history) | Change log |

---

## Summary

Flip the Jerry framework repository (`geekatron/jerry`) from private to public. This includes creating missing community health files (SECURITY.md, CODE_OF_CONDUCT.md, PR template), configuring repository metadata (description, homepage, topics), running a pre-public security audit, and performing the visibility flip with post-verification.

**Key Objectives:**
- Create community health files (SECURITY.md, CODE_OF_CONDUCT.md, PR template)
- Configure repo metadata (description, homepage, topics, disable wiki)
- Verify no secrets, credentials, or PII will be exposed
- Flip repo to public and verify anonymous access

**Criticality:** C3 (irreversible visibility change)

---

## Enablers

| ID | Title | Status | Priority | Effort |
|----|-------|--------|----------|--------|
| EN-951 | Community Health Files | pending | high | 3 |
| EN-952 | Repository Metadata & Configuration | pending | high | 2 |
| EN-953 | Pre-Public Security Audit | pending | critical | 2 |
| EN-954 | Visibility Flip & Post-Public Verification | pending | critical | 1 |

### Enabler Links

- [EN-951: Community Health Files](./EN-951-community-health-files/EN-951-community-health-files.md)
- [EN-952: Repository Metadata & Configuration](./EN-952-repo-metadata-config/EN-952-repo-metadata-config.md)
- [EN-953: Pre-Public Security Audit](./EN-953-pre-public-security-audit/EN-953-pre-public-security-audit.md)
- [EN-954: Visibility Flip & Post-Public Verification](./EN-954-visibility-flip/EN-954-visibility-flip.md)

### Execution Order

```
EN-953 (Security Audit)          <- FIRST: must pass before anything else
    |
    +-- EN-951 (Community Files)  <- After audit passes
    +-- EN-952 (Repo Metadata)    <- Parallel with EN-951
    |
    +-- EN-954 (Visibility Flip)  <- LAST: after all prep done
```

---

## Acceptance Criteria

| ID | Criterion | Status |
|----|-----------|--------|
| AC-1 | SECURITY.md exists at root with responsible disclosure policy | pending |
| AC-2 | CODE_OF_CONDUCT.md exists at root (Contributor Covenant v2.1) | pending |
| AC-3 | .github/pull_request_template.md exists with checklist | pending |
| AC-4 | Repository description, homepage, topics set correctly | pending |
| AC-5 | No secrets, credentials, or PII in codebase or git history | pending |
| AC-6 | Repository visibility is `public` | pending |
| AC-7 | Anonymous clone succeeds | pending |
| AC-8 | Docs site accessible at jerry.geekatron.org | pending |

---

## Progress Summary

| Metric | Value |
|--------|-------|
| **Total Enablers** | 4 |
| **Completed Enablers** | 0 |
| **Total Effort** | 8 |
| **Completion %** | 0% |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-18 | Claude | in_progress | Feature created. 4 enablers (EN-951 through EN-954). |
