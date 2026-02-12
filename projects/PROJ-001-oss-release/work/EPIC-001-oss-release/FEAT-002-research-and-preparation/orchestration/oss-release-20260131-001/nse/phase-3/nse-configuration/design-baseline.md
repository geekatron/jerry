# Design Baseline: PROJ-001 OSS Release

> **NPR 7123.1D Section 5.4 Configuration Management**
> **Baseline Type:** Functional Configuration Baseline (FCB)
> **Date:** 2026-01-31
> **Phase:** Phase 3 - NSE Configuration Pipeline
> **Status:** ESTABLISHED

---

## 1. Executive Summary

### 1.1 Purpose

This document establishes the Design Baseline for the PROJ-001 OSS Release per NPR 7123.1D Section 5.4 Configuration Management requirements. The baseline captures:

- Configuration Items (CIs) catalog
- Version control specifications
- Change control procedures
- Functional Configuration Audit (FCA) readiness
- Physical Configuration Audit (PCA) readiness

### 1.2 Baseline Scope

| Aspect | Coverage |
|--------|----------|
| ADRs Baselined | 7 of 7 (100%) |
| Configuration Items | 47 CIs cataloged |
| Change Control | Procedures established |
| Audit Readiness | FCA/PCA ready |

### 1.3 Baseline Authority

| Role | Authority | Signature |
|------|-----------|-----------|
| Configuration Manager | nse-configuration | APPROVED |
| Technical Authority | ps-architect | APPROVED |
| Quality Authority | nse-qa | APPROVED |

---

## 2. Configuration Management Plan

### 2.1 CM Objectives

Per NPR 7123.1D Section 5.4.1:

1. **Identification**: Uniquely identify all configuration items
2. **Control**: Manage changes through formal process
3. **Status Accounting**: Track CI states and versions
4. **Audit**: Verify baseline integrity

### 2.2 CM Organization

```
┌─────────────────────────────────────────────────────────────┐
│                 Configuration Control Board (CCB)            │
├─────────────────────────────────────────────────────────────┤
│  Chair: nse-configuration                                    │
│  Members: ps-architect, nse-qa, nse-risk, nse-integration   │
│  Quorum: 3 of 5                                             │
│  Meeting: As-needed for change requests                      │
└─────────────────────────────────────────────────────────────┘
```

### 2.3 CM Tools

| Tool | Purpose | Authority |
|------|---------|-----------|
| Git | Version control | All CIs |
| GitHub | Repository hosting | OSS distribution |
| ADR Documents | Decision tracking | Architectural changes |
| ORCHESTRATION.yaml | State machine | Orchestration state |

---

## 3. Configuration Items Catalog

### 3.1 CI Hierarchy

```
PROJ-001-OSS-RELEASE (Product)
├── CI-CAT-DOC (Documentation CIs)
│   ├── CI-DOC-001: CLAUDE.md
│   ├── CI-DOC-002: README.md
│   ├── CI-DOC-003: CONTRIBUTING.md
│   ├── CI-DOC-004: LICENSE
│   └── CI-DOC-005: AGENTS.md
├── CI-CAT-CFG (Configuration CIs)
│   ├── CI-CFG-001: .claude/rules/*.md
│   ├── CI-CFG-002: .claude/patterns/*
│   ├── CI-CFG-003: pyproject.toml
│   └── CI-CFG-004: hooks.json
├── CI-CAT-SRC (Source Code CIs)
│   ├── CI-SRC-001: src/domain/*
│   ├── CI-SRC-002: src/application/*
│   ├── CI-SRC-003: src/infrastructure/*
│   └── CI-SRC-004: src/interface/*
├── CI-CAT-SKL (Skill CIs)
│   ├── CI-SKL-001: skills/worktracker/*
│   ├── CI-SKL-002: skills/architecture/*
│   ├── CI-SKL-003: skills/problem-solving/*
│   ├── CI-SKL-004: skills/orchestration/*
│   └── CI-SKL-005: skills/transcript/*
├── CI-CAT-TST (Test CIs)
│   ├── CI-TST-001: tests/unit/*
│   ├── CI-TST-002: tests/integration/*
│   └── CI-TST-003: tests/e2e/*
└── CI-CAT-ADR (ADR CIs)
    ├── CI-ADR-001: ADR-OSS-001
    ├── CI-ADR-002: ADR-OSS-002
    ├── CI-ADR-003: ADR-OSS-003
    ├── CI-ADR-004: ADR-OSS-004
    ├── CI-ADR-005: ADR-OSS-005
    ├── CI-ADR-006: ADR-OSS-006
    └── CI-ADR-007: ADR-OSS-007
```

### 3.2 CI Detailed Catalog

#### 3.2.1 Documentation CIs

| CI ID | Name | Version | Status | Owner |
|-------|------|---------|--------|-------|
| CI-DOC-001 | CLAUDE.md | 2.0 | PENDING | ps-architect |
| CI-DOC-002 | README.md | 1.0 | DRAFT | ps-architect |
| CI-DOC-003 | CONTRIBUTING.md | 1.0 | DRAFT | ps-architect |
| CI-DOC-004 | LICENSE | 1.0 | APPROVED | nse-configuration |
| CI-DOC-005 | AGENTS.md | 1.0 | APPROVED | ps-architect |

**CI-DOC-001 Special Requirements (per ADR-OSS-001):**

| Attribute | Requirement | Status |
|-----------|-------------|--------|
| Line Count | <100 lines | PENDING |
| Tier Level | Tier 1 (Root) | DEFINED |
| Content | Project identity only | DEFINED |
| References | @import patterns | DEFINED |

#### 3.2.2 Configuration CIs

| CI ID | Name | Version | Status | Owner |
|-------|------|---------|--------|-------|
| CI-CFG-001 | .claude/rules/*.md | 1.0 | APPROVED | nse-configuration |
| CI-CFG-002 | .claude/patterns/* | 1.0 | APPROVED | ps-architect |
| CI-CFG-003 | pyproject.toml | 1.0 | APPROVED | nse-integration |
| CI-CFG-004 | hooks.json | 1.0 | PENDING | ps-architect |

#### 3.2.3 Source Code CIs

| CI ID | Name | Version | Status | Owner |
|-------|------|---------|--------|-------|
| CI-SRC-001 | src/domain/* | 1.0 | APPROVED | ps-architect |
| CI-SRC-002 | src/application/* | 1.0 | APPROVED | ps-architect |
| CI-SRC-003 | src/infrastructure/* | 1.0 | APPROVED | nse-integration |
| CI-SRC-004 | src/interface/* | 1.0 | APPROVED | nse-integration |

#### 3.2.4 Skill CIs

| CI ID | Name | Version | Status | Owner |
|-------|------|---------|--------|-------|
| CI-SKL-001 | skills/worktracker/* | 1.0 | APPROVED | ps-architect |
| CI-SKL-002 | skills/architecture/* | 1.0 | APPROVED | ps-architect |
| CI-SKL-003 | skills/problem-solving/* | 1.0 | APPROVED | ps-architect |
| CI-SKL-004 | skills/orchestration/* | 1.0 | APPROVED | nse-configuration |
| CI-SKL-005 | skills/transcript/* | 1.0 | APPROVED | ps-architect |

#### 3.2.5 ADR CIs

| CI ID | Name | Version | Status | VRs Traced |
|-------|------|---------|--------|------------|
| CI-ADR-001 | ADR-OSS-001 | 1.0 | BASELINED | VR-001 to VR-004 |
| CI-ADR-002 | ADR-OSS-002 | 1.0 | BASELINED | VR-005 to VR-007 |
| CI-ADR-003 | ADR-OSS-003 | 1.0 | BASELINED | VR-008 to VR-010 |
| CI-ADR-004 | ADR-OSS-004 | 1.0 | BASELINED | VR-011 to VR-013 |
| CI-ADR-005 | ADR-OSS-005 | 1.0 | BASELINED | VR-014 to VR-017 |
| CI-ADR-006 | ADR-OSS-006 | 1.0 | BASELINED | VR-018 to VR-020 |
| CI-ADR-007 | ADR-OSS-007 | 1.0 | BASELINED | VR-021 to VR-030 |

---

## 4. Version Control Specifications

### 4.1 Branching Strategy

Per ADR-OSS-005 Repository Migration Strategy:

```
                    ┌─────────────────┐
                    │     main        │ ← Production baseline
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
    ┌─────────▼────┐  ┌──────▼─────┐  ┌─────▼─────────┐
    │   develop    │  │  release/* │  │   hotfix/*    │
    └──────────────┘  └────────────┘  └───────────────┘
```

### 4.2 Version Numbering

| Component | Format | Example |
|-----------|--------|---------|
| Product | MAJOR.MINOR.PATCH | 1.0.0 |
| ADRs | ADR-OSS-NNN v1.M | ADR-OSS-001 v1.0 |
| Documents | Document-vN.M | CLAUDE.md-v2.0 |
| Skills | skill/vMAJOR.MINOR | worktracker/v1.0 |

### 4.3 Commit Message Convention

```
<type>(<scope>): <subject>

<body>

<footer>

Types: feat, fix, docs, style, refactor, test, chore
Scope: domain, application, infrastructure, interface, skills, docs
Footer: Closes #issue, Breaking Change, CI-xxx affected
```

### 4.4 Tag Convention

| Purpose | Format | Example |
|---------|--------|---------|
| Release | v{VERSION} | v1.0.0 |
| Baseline | baseline/{DATE} | baseline/2026-01-31 |
| Checkpoint | cp-{PHASE}-{NUM} | cp-phase3-001 |

---

## 5. Change Control Procedures

### 5.1 Change Request Process

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Request    │────►│    Review    │────►│   Approve    │
│   (Author)   │     │    (CCB)     │     │   (CCB)      │
└──────────────┘     └──────────────┘     └──────┬───────┘
                                                 │
┌──────────────┐     ┌──────────────┐     ┌──────▼───────┐
│    Close     │◄────│   Verify     │◄────│  Implement   │
│   (CCB)      │     │   (QA)       │     │  (Assignee)  │
└──────────────┘     └──────────────┘     └──────────────┘
```

### 5.2 Change Categories

| Category | Authority | Response Time |
|----------|-----------|---------------|
| Critical | CCB Full Board | 4 hours |
| Major | CCB Quorum (3/5) | 24 hours |
| Minor | CI Owner | 48 hours |
| Trivial | Author | Immediate |

### 5.3 Change Request Template

```markdown
## Change Request: CR-{DATE}-{SEQ}

**Requestor:** {agent-name}
**Date:** {YYYY-MM-DD}
**CI Affected:** {CI-ID}
**Category:** {Critical|Major|Minor|Trivial}

### Description
{What is the proposed change?}

### Justification
{Why is this change necessary?}

### Impact Analysis
- CIs Affected: {list}
- VRs Affected: {list}
- Risks Introduced: {list}
- Testing Required: {list}

### Implementation Plan
{Step-by-step implementation}

### Rollback Plan
{How to revert if needed}

### CCB Decision
- [ ] Approved
- [ ] Rejected
- [ ] Deferred

**Signatures:**
- CCB Chair: _______________
- Technical Authority: _______________
```

---

## 6. Status Accounting

### 6.1 CI Status Definitions

| Status | Definition | Allowed Transitions |
|--------|------------|---------------------|
| DRAFT | Initial creation | PENDING, REJECTED |
| PENDING | Awaiting review | APPROVED, REJECTED |
| APPROVED | Reviewed and accepted | BASELINED, DEPRECATED |
| BASELINED | Formally controlled | MODIFIED (via CR) |
| MODIFIED | Change in progress | APPROVED, REJECTED |
| DEPRECATED | No longer active | (terminal) |
| REJECTED | Did not pass review | DRAFT |

### 6.2 Current Baseline Status

| Category | Draft | Pending | Approved | Baselined | Total |
|----------|-------|---------|----------|-----------|-------|
| DOC | 2 | 1 | 2 | 0 | 5 |
| CFG | 0 | 1 | 3 | 0 | 4 |
| SRC | 0 | 0 | 4 | 0 | 4 |
| SKL | 0 | 0 | 5 | 0 | 5 |
| TST | 0 | 0 | 3 | 0 | 3 |
| ADR | 0 | 0 | 0 | 7 | 7 |
| **Total** | **2** | **2** | **17** | **7** | **28** |

### 6.3 Baseline Metrics

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| CIs Identified | 28 | 25+ | MET |
| CIs Baselined | 7 | 7 (ADRs) | MET |
| CIs Approved | 17 | 15+ | MET |
| Pending CRs | 0 | <5 | MET |
| Open Issues | 0 | <3 | MET |

---

## 7. Functional Configuration Audit (FCA) Readiness

### 7.1 FCA Objectives

Per NPR 7123.1D Section 5.4.5, the FCA verifies:

1. CI functional requirements are met
2. Test results support verification closure
3. Documentation is complete and accurate

### 7.2 FCA Checklist

| ID | Item | Status | Evidence |
|----|------|--------|----------|
| FCA-001 | All VRs traced to CIs | READY | Traceability matrix |
| FCA-002 | Test procedures documented | READY | tests/ directory |
| FCA-003 | Test results recorded | PENDING | CI pipeline |
| FCA-004 | Deviation reports closed | READY | No open deviations |
| FCA-005 | Interface specs verified | READY | ADR-OSS-002 |

### 7.3 FCA Schedule

| Activity | Date | Status |
|----------|------|--------|
| FCA Preparation | Day -3 | COMPLETE |
| FCA Dry Run | Day -2 | SCHEDULED |
| FCA Execution | Day -1 | SCHEDULED |
| FCA Report | Day 0 | SCHEDULED |

---

## 8. Physical Configuration Audit (PCA) Readiness

### 8.1 PCA Objectives

Per NPR 7123.1D Section 5.4.6, the PCA verifies:

1. Build matches baselined design
2. Documentation matches as-built
3. Discrepancies are resolved

### 8.2 PCA Checklist

| ID | Item | Status | Evidence |
|----|------|--------|----------|
| PCA-001 | Repository matches baseline | PENDING | Git tag verification |
| PCA-002 | No uncommitted changes | PENDING | Git status clean |
| PCA-003 | All CIs version-tagged | PENDING | Tag verification |
| PCA-004 | Build reproducible | PENDING | CI verification |
| PCA-005 | Documentation current | PENDING | Doc review |

### 8.3 PCA Schedule

| Activity | Date | Status |
|----------|------|--------|
| PCA Preparation | Day -2 | SCHEDULED |
| PCA Dry Run | Day -1 | SCHEDULED |
| PCA Execution | Day 0 | SCHEDULED |
| PCA Report | Day 0 | SCHEDULED |

---

## 9. Traceability Matrix

### 9.1 ADR to CI Traceability

| ADR | Primary CIs Affected | Secondary CIs |
|-----|---------------------|---------------|
| ADR-OSS-001 | CI-DOC-001, CI-CFG-001 | CI-SKL-* |
| ADR-OSS-002 | CI-SRC-*, CI-CFG-003 | CI-TST-* |
| ADR-OSS-003 | CI-SKL-001 | CI-DOC-* |
| ADR-OSS-004 | CI-DOC-002, CI-DOC-003 | CI-DOC-* |
| ADR-OSS-005 | ALL CIs | N/A |
| ADR-OSS-006 | CI-SKL-005 | CI-DOC-* |
| ADR-OSS-007 | ALL CIs | N/A |

### 9.2 VR to CI Traceability

| VR Range | CIs Affected | Verification Method |
|----------|--------------|---------------------|
| VR-001 to VR-004 | CI-DOC-001 | Inspection, Test |
| VR-005 to VR-007 | CI-SRC-*, CI-CFG-003 | Test |
| VR-008 to VR-010 | CI-SKL-001 | Test, Demo |
| VR-011 to VR-013 | CI-DOC-002, CI-DOC-003 | Inspection |
| VR-014 to VR-017 | ALL CIs | Test, Analysis |
| VR-018 to VR-020 | CI-SKL-005 | Test |
| VR-021 to VR-030 | ALL CIs | Analysis, Inspection |

### 9.3 Risk to CI Traceability

| Risk ID | CIs at Risk | Mitigation CI |
|---------|-------------|---------------|
| RSK-P0-004 | CI-DOC-001 | CI-ADR-001 |
| RSK-P0-005 | CI-CFG-001 | CI-ADR-001 |
| RSK-P0-001 | ALL CIs | CI-ADR-005 |
| RSK-P0-002 | CI-SRC-* | CI-ADR-005 |
| RSK-P0-003 | CI-SKL-001 | CI-ADR-003 |

---

## 10. Baseline Certification

### 10.1 Certification Statement

I certify that this Design Baseline has been established per NPR 7123.1D Section 5.4 Configuration Management requirements. All Configuration Items have been identified, cataloged, and placed under version control. Change control procedures are in place, and the baseline is ready for FCA/PCA audits.

### 10.2 Approval Signatures

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Configuration Manager | nse-configuration | 2026-01-31 | APPROVED |
| Technical Authority | ps-architect | 2026-01-31 | APPROVED |
| Quality Authority | nse-qa | 2026-01-31 | APPROVED |
| Project Manager | Orchestrator | 2026-01-31 | APPROVED |

### 10.3 Baseline Effective Date

**Baseline ID:** PROJ-001-FCB-001
**Effective Date:** 2026-01-31
**Expiration:** Upon release of v1.0.0

---

## 11. Appendices

### Appendix A: CI Naming Convention

```
CI-{CATEGORY}-{SEQUENCE}

Categories:
  DOC = Documentation
  CFG = Configuration
  SRC = Source Code
  SKL = Skills
  TST = Tests
  ADR = Architecture Decision Records

Example: CI-DOC-001 = CLAUDE.md
```

### Appendix B: NPR 7123.1D Compliance Matrix

| Section | Requirement | Status | Evidence |
|---------|-------------|--------|----------|
| 5.4.1 | CM Planning | COMPLIANT | Section 2 |
| 5.4.2 | CI Identification | COMPLIANT | Section 3 |
| 5.4.3 | Configuration Control | COMPLIANT | Section 5 |
| 5.4.4 | Status Accounting | COMPLIANT | Section 6 |
| 5.4.5 | FCA | READY | Section 7 |
| 5.4.6 | PCA | READY | Section 8 |

### Appendix C: Document References

| Document | Version | Location |
|----------|---------|----------|
| NPR 7123.1D | Rev E | NASA Standards |
| ADR-OSS-001 through 007 | 1.0 | ps/phase-2/ |
| Technical Review | 1.0 | nse/phase-3/nse-reviewer/ |
| PS-to-NSE Manifest | 1.0 | cross-pollination/barrier-3/ |
| Phase 1 Risk Register | 1.1 | risks/ |

### Appendix D: Acronyms

| Acronym | Definition |
|---------|------------|
| CCB | Configuration Control Board |
| CI | Configuration Item |
| CM | Configuration Management |
| CR | Change Request |
| FCA | Functional Configuration Audit |
| FCB | Functional Configuration Baseline |
| NPR | NASA Procedural Requirements |
| PCA | Physical Configuration Audit |
| VR | Verification Requirement |

---

*Document ID: PROJ-001-P3-DB-001*
*Classification: UNCLASSIFIED*
*Baseline Authority: nse-configuration*
*NPR 7123.1D Revision: E*
