# Verification Cross-Reference Matrix: [PROJECT_NAME]

> **Document ID:** VCRM-[PROJECT_ID]-001
> **Version:** 0.1
> **Date:** [DATE]
> **Status:** [DRAFT / IN PROGRESS / COMPLETE]
> **Reference:** REQ-[PROJECT_ID]-001

---

## Document Control

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Author | [AUTHOR_NAME] | [DATE] | |
| V&V Lead | [VV_LEAD_NAME] | | |
| Approver | [APPROVER_NAME] | | |

---

## 1. Verification Summary

| Metric | Count | Percentage |
|--------|-------|------------|
| Total Requirements | [N] | 100% |
| Verified | [N] | [N]% |
| In Progress | [N] | [N]% |
| Pending | [N] | [N]% |
| Failed | [N] | [N]% |
| Waived | [N] | [N]% |

**Overall Verification Status:** [STATUS - e.g., "75% Complete"]

---

## 2. Verification Methods

| Code | Method | Description | When Used |
|------|--------|-------------|-----------|
| A | Analysis | Mathematical, statistical, or simulation-based evaluation | Design analysis, performance prediction |
| D | Demonstration | Show capability through operation without quantitative measurement | Functional capabilities, interfaces |
| I | Inspection | Visual or physical examination of product or documentation | Configuration, workmanship, documentation |
| T | Test | Execute procedures, stimulate system, measure results quantitatively | Performance, environmental, stress testing |

---

## 3. VCRM Matrix

| Req ID | Requirement Title | V-Method | V-Level | V-Procedure | Success Criteria | Status | Evidence |
|--------|-------------------|----------|---------|-------------|------------------|--------|----------|
| REQ-[PROJECT_ID]-SYS-001 | [TITLE] | [A/D/I/T] | System | VER-001 | [CRITERIA] | [STATUS] | [EVIDENCE] |
| REQ-[PROJECT_ID]-SYS-002 | [TITLE] | [A/D/I/T] | System | VER-002 | [CRITERIA] | [STATUS] | [EVIDENCE] |
| REQ-[PROJECT_ID]-FUN-001 | [TITLE] | [A/D/I/T] | Component | VER-003 | [CRITERIA] | [STATUS] | [EVIDENCE] |
| REQ-[PROJECT_ID]-FUN-002 | [TITLE] | [A/D/I/T] | Component | VER-004 | [CRITERIA] | [STATUS] | [EVIDENCE] |
| REQ-[PROJECT_ID]-PER-001 | [TITLE] | T | System | VER-005 | [CRITERIA] | [STATUS] | [EVIDENCE] |
| REQ-[PROJECT_ID]-INT-001 | [TITLE] | D/T | Integration | VER-006 | [CRITERIA] | [STATUS] | [EVIDENCE] |

---

## 4. Verification Levels

| Level | Description | Integration State | Verification Scope |
|-------|-------------|-------------------|-------------------|
| Unit | Individual component | Standalone | Component specs |
| Component | Integrated subassembly | Partial integration | Subsystem requirements |
| Integration | Connected systems | Full hardware/software | Interface requirements |
| System | Complete system | End-to-end | System requirements |
| Acceptance | Delivered product | Operational config | Acceptance criteria |

---

## 5. Verification Procedures

### VER-001: [PROCEDURE_TITLE]

| Attribute | Value |
|-----------|-------|
| Procedure ID | VER-001 |
| Requirement | REQ-[PROJECT_ID]-[XXX] |
| Method | [A/D/I/T] |
| Level | [Unit/Component/Integration/System] |

**Objective:** [What this verification will confirm]

**Prerequisites:**
- [ ] [PREREQUISITE_1]
- [ ] [PREREQUISITE_2]
- [ ] [PREREQUISITE_3]

**Test Environment:**
| Element | Description |
|---------|-------------|
| Hardware | [HARDWARE_REQUIRED] |
| Software | [SOFTWARE_REQUIRED] |
| Facilities | [FACILITY_REQUIRED] |
| Personnel | [ROLES_REQUIRED] |

**Procedure Steps:**
1. [STEP_1]
2. [STEP_2]
3. [STEP_3]
4. [STEP_N]

**Pass Criteria:**
- [ ] [CRITERION_1]
- [ ] [CRITERION_2]

**Fail Criteria:**
- [CONDITION_THAT_CONSTITUTES_FAILURE]

**Data to Collect:**
| Data Item | Format | Storage Location |
|-----------|--------|------------------|
| [DATA_ITEM] | [FORMAT] | [LOCATION] |

**Result:** [PASS / FAIL / NOT RUN]

**Evidence:**
[Link to test report, log files, screenshots, etc.]

---

### VER-002: [PROCEDURE_TITLE]

| Attribute | Value |
|-----------|-------|
| Procedure ID | VER-002 |
| Requirement | REQ-[PROJECT_ID]-[XXX] |
| Method | [A/D/I/T] |
| Level | [Level] |

**Objective:** [Objective]

**Prerequisites:**
- [ ] [Prerequisites]

**Procedure Steps:**
1. [Steps]

**Pass Criteria:**
- [ ] [Criteria]

**Result:** [PENDING]

---

## 6. Verification Status by Category

### System Requirements

| Req ID | Title | Status | Date | Notes |
|--------|-------|--------|------|-------|
| SYS-001 | [TITLE] | [STATUS] | [DATE] | |
| SYS-002 | [TITLE] | [STATUS] | [DATE] | |

### Functional Requirements

| Req ID | Title | Status | Date | Notes |
|--------|-------|--------|------|-------|
| FUN-001 | [TITLE] | [STATUS] | [DATE] | |
| FUN-002 | [TITLE] | [STATUS] | [DATE] | |

### Performance Requirements

| Req ID | Title | Status | Date | Notes |
|--------|-------|--------|------|-------|
| PER-001 | [TITLE] | [STATUS] | [DATE] | |

### Interface Requirements

| Req ID | Title | Status | Date | Notes |
|--------|-------|--------|------|-------|
| INT-001 | [TITLE] | [STATUS] | [DATE] | |

---

## 7. Verification Schedule

| Phase | Start Date | End Date | Requirements Covered | Status |
|-------|------------|----------|---------------------|--------|
| Unit Testing | [DATE] | [DATE] | [REQ_LIST] | [STATUS] |
| Integration Testing | [DATE] | [DATE] | [REQ_LIST] | [STATUS] |
| System Testing | [DATE] | [DATE] | [REQ_LIST] | [STATUS] |
| Acceptance Testing | [DATE] | [DATE] | [REQ_LIST] | [STATUS] |

---

## 8. Verification Traceability

```
STK-[PROJECT_ID]-001 (Stakeholder Need)
    |
    +-- REQ-[PROJECT_ID]-SYS-001 --> VER-001 [STATUS]
    |       |
    |       +-- REQ-[PROJECT_ID]-FUN-001 --> VER-003 [STATUS]
    |       +-- REQ-[PROJECT_ID]-FUN-002 --> VER-004 [STATUS]
    |
    +-- REQ-[PROJECT_ID]-SYS-002 --> VER-002 [STATUS]
    |
    +-- REQ-[PROJECT_ID]-PER-001 --> VER-005 [STATUS]
    |
    +-- REQ-[PROJECT_ID]-INT-001 --> VER-006 [STATUS]
```

---

## 9. Issues and Waivers

### Open Issues

| Issue ID | Req ID | Description | Impact | Resolution Plan | Due Date |
|----------|--------|-------------|--------|-----------------|----------|
| ISS-001 | [REQ_ID] | [ISSUE_DESCRIPTION] | [IMPACT] | [PLAN] | [DATE] |

### Waivers

| Waiver ID | Req ID | Justification | Approver | Date |
|-----------|--------|---------------|----------|------|
| WAV-001 | [REQ_ID] | [JUSTIFICATION] | [APPROVER] | [DATE] |

---

## 10. Verification Resources

### Test Equipment

| Equipment | Calibration Status | Calibration Due | Location |
|-----------|-------------------|-----------------|----------|
| [EQUIPMENT_NAME] | [CURRENT/EXPIRED] | [DATE] | [LOCATION] |

### Test Facilities

| Facility | Availability | Scheduled Use |
|----------|--------------|---------------|
| [FACILITY_NAME] | [AVAILABLE/BOOKED] | [DATES] |

### Test Personnel

| Role | Name | Qualification | Availability |
|------|------|--------------|--------------|
| V&V Lead | [NAME] | [QUALIFICATION] | [AVAILABILITY] |
| Test Engineer | [NAME] | [QUALIFICATION] | [AVAILABILITY] |

---

## 11. Verification Status Summary

| Category | Total | Verified | In Progress | Pending | Failed | Waived |
|----------|-------|----------|-------------|---------|--------|--------|
| System | [N] | [N] | [N] | [N] | [N] | [N] |
| Functional | [N] | [N] | [N] | [N] | [N] | [N] |
| Performance | [N] | [N] | [N] | [N] | [N] | [N] |
| Interface | [N] | [N] | [N] | [N] | [N] | [N] |
| **Total** | **[N]** | **[N]** | **[N]** | **[N]** | **[N]** | **[N]** |

---

## Appendix A: Verification Method Selection Rationale

| Req ID | Selected Method | Rationale | Alternatives Considered |
|--------|-----------------|-----------|------------------------|
| [REQ_ID] | [METHOD] | [WHY_SELECTED] | [OTHER_METHODS] |

---

## Appendix B: Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | [DATE] | [AUTHOR] | Initial draft |

---

## References

- NPR 7123.1D, NASA Systems Engineering Processes and Requirements
- NPR 7150.2D, NASA Software Engineering Requirements
- NASA/SP-2016-6105 Rev2, NASA Systems Engineering Handbook
- NASA-HDBK-2203, NASA Software Verification and Validation

---

*DISCLAIMER: This Verification Cross-Reference Matrix is AI-generated based on NASA Systems Engineering standards (NPR 7123.1D, NPR 7150.2D). It is advisory only and does not constitute official NASA guidance. All verification decisions require human review and professional engineering judgment. Verification procedures must be validated by qualified V&V Engineers before use in mission-critical applications.*
