# Configuration Item List: [PROJECT_NAME]

> **Document ID:** CI-[PROJECT_ID]-001
> **Version:** 0.1
> **Date:** [DATE]
> **Baseline:** [BASELINE_ID] ([BASELINE_NAME])
> **Author:** [AUTHOR_NAME]

---

## Document Control

| Role | Name | Date | Signature |
|------|------|------|-----------|
| CM Manager | [CM_MANAGER_NAME] | [DATE] | |
| Technical Lead | [TECH_LEAD_NAME] | | |
| Project Authority | [PA_NAME] | | |

---

## L0: Executive Summary

**Total CIs:** [N]
**Controlled:** [N] ([N]%)
**Pending:** [N] ([N]%)
**Current Baseline:** [BASELINE_ID] ([DATE])

[Brief description of what this CI list covers and its purpose within the project.]

---

## L1: Configuration Items

### CI Classification

| Type | Code | Description | Example |
|------|------|-------------|---------|
| HW | HW | Hardware item | Flight computer |
| SW | SW | Software item | Flight software |
| FW | FW | Firmware item | FPGA code |
| DOC | DOC | Documentation | Requirements spec |
| PROC | PROC | Procedure | Test procedure |
| TOOL | TOOL | Tool/GSE | Test equipment |
| DATA | DATA | Data product | Calibration data |
| COTS | COTS | Commercial off-the-shelf | Operating system |

### CI Selection Criteria

Items are selected for configuration control based on:
- [ ] Required for system operation or mission success
- [ ] Subject to change during lifecycle
- [ ] Multiple systems or components depend on it
- [ ] Has significant safety or reliability impact
- [ ] Required for verification or validation
- [ ] Contractually or programmatically required

---

### CI Registry

| CI ID | Name | Type | Description | Owner | Version | Baseline | Status |
|-------|------|------|-------------|-------|---------|----------|--------|
| CI-001 | [CI_NAME] | [HW/SW/...] | [DESCRIPTION] | [OWNER] | [VERSION] | [BL-XXX] | [Controlled/Pending] |
| CI-002 | [CI_NAME] | [TYPE] | [DESCRIPTION] | [OWNER] | [VERSION] | [BL-XXX] | [Status] |
| CI-003 | [CI_NAME] | [TYPE] | [DESCRIPTION] | [OWNER] | [VERSION] | [BL-XXX] | [Status] |
| CI-004 | [CI_NAME] | [TYPE] | [DESCRIPTION] | [OWNER] | [VERSION] | [BL-XXX] | [Status] |
| CI-005 | [CI_NAME] | [TYPE] | [DESCRIPTION] | [OWNER] | [VERSION] | [BL-XXX] | [Status] |

---

### CI Status Summary

| Status | Count | % |
|--------|-------|---|
| Controlled | [N] | [N]% |
| Pending | [N] | [N]% |
| Draft | [N] | [N]% |
| Obsolete | [N] | [N]% |
| **Total** | **[N]** | **100%** |

### CI by Type

| Type | Count | % |
|------|-------|---|
| HW (Hardware) | [N] | [N]% |
| SW (Software) | [N] | [N]% |
| FW (Firmware) | [N] | [N]% |
| DOC (Documentation) | [N] | [N]% |
| PROC (Procedure) | [N] | [N]% |
| TOOL (Tool/GSE) | [N] | [N]% |
| DATA (Data) | [N] | [N]% |
| COTS (Commercial) | [N] | [N]% |
| **Total** | **[N]** | **100%** |

---

## L2: CM Strategy

### Baseline Definition: [BASELINE_ID] ([BASELINE_NAME])

| Attribute | Value |
|-----------|-------|
| Baseline ID | [BL-XXX] |
| Baseline Name | [DESCRIPTIVE_NAME - e.g., "Functional Baseline", "Allocated Baseline", "Product Baseline"] |
| Baseline Type | [Functional / Allocated / Product / Operational] |
| Date Established | [DATE] |
| CI Count | [N] |
| Approver | [APPROVER_NAME/ROLE] |
| Reference Documents | [REQ-XXX, ICD-XXX, etc.] |

### Baseline Contents

| CI ID | Name | Version | Location | Size/Lines |
|-------|------|---------|----------|------------|
| CI-001 | [NAME] | [VERSION] | [FILE_PATH or LOCATION] | [SIZE] |
| CI-002 | [NAME] | [VERSION] | [FILE_PATH or LOCATION] | [SIZE] |

### Baseline Strategy (Lifecycle)

| Baseline | Phase | Contents | Purpose | Approval Authority |
|----------|-------|----------|---------|-------------------|
| BL-001 | Requirements | System requirements | Functional baseline | [AUTHORITY] |
| BL-002 | Design | Design documents, ICDs | Allocated baseline | [AUTHORITY] |
| BL-003 | Implementation | Code, procedures | Product baseline | [AUTHORITY] |
| BL-004 | Operations | Operational docs | Operational baseline | [AUTHORITY] |

---

### Change Control Process

| Change Type | Authority | Process | Turnaround |
|-------------|-----------|---------|------------|
| Administrative | CM Manager | Direct update | 1 day |
| Minor (no impact) | Technical Lead | Expedited review | 3 days |
| Significant | CCB | Formal review | 2 weeks |
| Major (cost/schedule) | Project Authority | Full review + approval | 4 weeks |

### Change Request (CR) Template

| Field | Value |
|-------|-------|
| CR Number | CR-[PROJECT_ID]-[NNN] |
| Title | [CHANGE_TITLE] |
| Requestor | [NAME] |
| Date Submitted | [DATE] |
| Affected CIs | [CI-XXX, CI-YYY] |
| Change Description | [DETAILED_DESCRIPTION] |
| Justification | [WHY_CHANGE_IS_NEEDED] |
| Impact Assessment | |
| - Technical | [TECHNICAL_IMPACT] |
| - Schedule | [SCHEDULE_IMPACT] |
| - Cost | [COST_IMPACT] |
| - Safety | [SAFETY_IMPACT] |
| Priority | [Critical/High/Medium/Low] |
| Disposition | [Pending/Approved/Rejected/Deferred] |
| Approved By | [NAME] |
| Approval Date | [DATE] |

---

### CI Dependencies

| CI ID | Depends On | Depended By | Notes |
|-------|------------|-------------|-------|
| CI-001 | - | CI-002, CI-003 | [Parent CI] |
| CI-002 | CI-001 | CI-004 | |
| CI-003 | CI-001 | CI-005 | |
| CI-004 | CI-002 | - | |
| CI-005 | CI-003 | - | |

---

### Version Numbering Convention

| Level | Format | When Used |
|-------|--------|-----------|
| Major | X.0 | Significant functional changes |
| Minor | X.Y | Feature additions, non-breaking changes |
| Patch | X.Y.Z | Bug fixes, minor corrections |
| Build | X.Y.Z.B | Development builds |
| Pre-release | X.Y.Z-alpha/beta/rc | Pre-release versions |

---

### Configuration Status Accounting

| CI ID | Current Version | Previous Version | Change Date | Change Authority | CR Reference |
|-------|-----------------|------------------|-------------|------------------|--------------|
| CI-001 | [VERSION] | [PREV] | [DATE] | [AUTHORITY] | [CR-XXX] |

---

## Open Change Requests

| CR ID | Title | Affected CIs | Status | Priority | Due Date |
|-------|-------|--------------|--------|----------|----------|
| CR-001 | [TITLE] | [CI-XXX] | [Status] | [Priority] | [DATE] |

---

## Baseline Approval Record

| Role | Name | Date | Status |
|------|------|------|--------|
| CM Manager | [NAME] | [DATE] | [Recommended/Pending] |
| Technical Lead | [NAME] | [DATE] | [Recommended/Pending] |
| Quality Assurance | [NAME] | [DATE] | [Approved/Pending] |
| Project Authority | [NAME] | [DATE] | [Approved/Pending] |

---

## Change Log

| Date | Action | CI IDs | By | CR Reference | Notes |
|------|--------|--------|-------|--------------|-------|
| [DATE] | Initial baseline | All | [NAME] | - | [BASELINE_ID] established |

---

## Appendix A: CI Detailed Information

### CI-001: [CI_NAME]

| Attribute | Value |
|-----------|-------|
| CI ID | CI-001 |
| Full Name | [FULL_NAME] |
| Description | [DETAILED_DESCRIPTION] |
| Type | [TYPE] |
| Owner | [OWNER_NAME] |
| Current Version | [VERSION] |
| Location | [PATH/REPOSITORY/LOCATION] |
| Size | [SIZE] |
| Baseline(s) | [BASELINES] |
| Parent CI | [PARENT_CI or N/A] |
| Child CIs | [CHILD_CIs or N/A] |
| Requirements Traced | [REQ-XXX, REQ-YYY] |
| Verification Status | [Verified/Pending/N/A] |

---

## Appendix B: CM Tools and Repositories

| Purpose | Tool/System | Location | Access |
|---------|-------------|----------|--------|
| Version Control | [GIT/SVN/etc.] | [URL] | [ACCESS_INFO] |
| Issue Tracking | [TOOL] | [URL] | [ACCESS_INFO] |
| Document Control | [TOOL] | [URL] | [ACCESS_INFO] |
| Build System | [TOOL] | [URL] | [ACCESS_INFO] |

---

## Appendix C: CM Roles and Responsibilities

| Role | Responsibilities | Current Assignee |
|------|------------------|------------------|
| CM Manager | Maintain CM plan, manage baselines, run CCB | [NAME] |
| CI Owner | Maintain CI, submit change requests | [Various] |
| CCB Chair | Approve/reject changes | [NAME] |
| Quality Assurance | Audit CM processes | [NAME] |

---

## Appendix D: Acronyms

| Term | Definition |
|------|------------|
| BL | Baseline |
| CCB | Configuration Control Board |
| CI | Configuration Item |
| CM | Configuration Management |
| CR | Change Request |
| COTS | Commercial Off-The-Shelf |
| GSE | Ground Support Equipment |

---

## References

- NPR 7123.1D, NASA Systems Engineering Processes and Requirements (Process 14 - Configuration Management)
- NPR 7150.2D, NASA Software Engineering Requirements
- NASA/SP-2016-6105 Rev2, NASA Systems Engineering Handbook
- NASA-HDBK-1009A, NASA Systems Engineering Guidelines for Work Products
- [PROJECT_SPECIFIC_CM_PLAN]

---

*DISCLAIMER: This Configuration Item List is AI-generated based on NASA Systems Engineering standards (NPR 7123.1D). It is advisory only and does not constitute official NASA guidance. All configuration management decisions require human review and professional engineering judgment. CM practices must be validated by qualified Configuration Management professionals before use in mission-critical applications.*
