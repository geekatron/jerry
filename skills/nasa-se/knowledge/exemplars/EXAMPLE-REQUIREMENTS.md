# Exemplar: Requirements Specification

> Demonstrates proper NASA-style requirements format

---

## Document Information

| Field | Value |
|-------|-------|
| Example Type | Requirements Specification |
| Purpose | Show correct requirement format and attributes |
| Based On | NPR 7123.1D Process 2, NASA-HDBK-1009A |

---

## Example System: Data Logger Subsystem

*This is a fictional subsystem used to demonstrate proper requirements format.*

---

## 1. Document Control

| Field | Value |
|-------|-------|
| Document ID | REQ-DLS-001 |
| Title | Data Logger Subsystem Requirements Specification |
| Version | 1.0 |
| Date | 2026-01-09 |
| Status | DRAFT |
| Classification | Unclassified |

---

## 2. Introduction

### 2.1 Purpose
This document specifies the technical requirements for the Data Logger Subsystem (DLS), a component of the Example Mission System (EMS).

### 2.2 Scope
The DLS shall acquire, timestamp, and store telemetry data from mission instruments. This specification covers functional, performance, interface, and environmental requirements.

### 2.3 Document Overview
- Section 3: System Requirements (top-level)
- Section 4: Functional Requirements
- Section 5: Performance Requirements
- Section 6: Interface Requirements
- Section 7: Environmental Requirements

---

## 3. System Requirements

### REQ-DLS-SYS-001: Primary Function
**Requirement:** The DLS SHALL acquire telemetry data from up to 16 instrument channels.

| Attribute | Value |
|-----------|-------|
| Priority | 1 (Critical) |
| Rationale | Mission requires multi-instrument data collection |
| Parent | STRQ-EMS-012 |
| Verification Method | Test |
| Status | Approved |
| TBD/TBR | None |

### REQ-DLS-SYS-002: Data Storage
**Requirement:** The DLS SHALL store a minimum of 72 hours of continuous telemetry data.

| Attribute | Value |
|-----------|-------|
| Priority | 1 (Critical) |
| Rationale | Supports ground contact gaps up to 48 hours with 50% margin |
| Parent | STRQ-EMS-015 |
| Verification Method | Analysis, Test |
| Status | Approved |
| TBD/TBR | None |

### REQ-DLS-SYS-003: Data Downlink
**Requirement:** The DLS SHALL provide stored data to the communication subsystem upon command.

| Attribute | Value |
|-----------|-------|
| Priority | 1 (Critical) |
| Rationale | Enables ground retrieval of science and housekeeping data |
| Parent | STRQ-EMS-018 |
| Verification Method | Demonstration |
| Status | Approved |
| TBD/TBR | None |

---

## 4. Functional Requirements

### REQ-DLS-FUN-001: Data Acquisition
**Requirement:** The DLS SHALL sample each instrument channel at a rate of 10 Hz ± 0.1 Hz.

| Attribute | Value |
|-----------|-------|
| Priority | 1 (Critical) |
| Rationale | Required for science data Nyquist compliance |
| Parent | REQ-DLS-SYS-001 |
| Verification Method | Test |
| Status | Approved |
| TBD/TBR | None |

### REQ-DLS-FUN-002: Timestamp Accuracy
**Requirement:** The DLS SHALL timestamp each data sample with an accuracy of ±1 millisecond relative to onboard time.

| Attribute | Value |
|-----------|-------|
| Priority | 2 (High) |
| Rationale | Enables data correlation across instruments |
| Parent | REQ-DLS-SYS-001 |
| Verification Method | Test |
| Status | Approved |
| TBD/TBR | None |

### REQ-DLS-FUN-003: Data Compression
**Requirement:** The DLS SHALL compress stored data using lossless compression with a minimum compression ratio of 2:1.

| Attribute | Value |
|-----------|-------|
| Priority | 2 (High) |
| Rationale | Reduces storage requirements and downlink time |
| Parent | REQ-DLS-SYS-002 |
| Verification Method | Test |
| Status | Approved |
| TBD/TBR | None |

### REQ-DLS-FUN-004: Data Integrity
**Requirement:** The DLS SHALL detect and report single-bit errors in stored data with a probability of detection ≥ 0.9999.

| Attribute | Value |
|-----------|-------|
| Priority | 1 (Critical) |
| Rationale | Space radiation environment requires error protection |
| Parent | REQ-DLS-SYS-002 |
| Verification Method | Analysis, Test |
| Status | Approved |
| TBD/TBR | None |

### REQ-DLS-FUN-005: Mode Transitions
**Requirement:** The DLS SHALL transition between operational modes within 100 milliseconds of receiving a mode command.

| Attribute | Value |
|-----------|-------|
| Priority | 3 (Medium) |
| Rationale | Supports timely response to mission events |
| Parent | STRQ-EMS-022 |
| Verification Method | Test |
| Status | Proposed |
| TBD/TBR | TBR-001: Verify 100ms is achievable with flight processor |

---

## 5. Performance Requirements

### REQ-DLS-PER-001: Data Rate
**Requirement:** The DLS SHALL process aggregate input data rates up to 2 Mbps continuously.

| Attribute | Value |
|-----------|-------|
| Priority | 1 (Critical) |
| Rationale | Worst-case 16 channels × 10 Hz × 12.5 kbits/sample |
| Parent | REQ-DLS-SYS-001 |
| Verification Method | Test |
| Status | Approved |
| TBD/TBR | None |

### REQ-DLS-PER-002: Storage Capacity
**Requirement:** The DLS SHALL provide a minimum of 8 GB of usable storage.

| Attribute | Value |
|-----------|-------|
| Priority | 1 (Critical) |
| Rationale | 72 hours × 2 Mbps × 3600 s/hr ÷ 8 = 6.48 GB + margin |
| Parent | REQ-DLS-SYS-002 |
| Verification Method | Inspection |
| Status | Approved |
| TBD/TBR | None |

### REQ-DLS-PER-003: Downlink Rate
**Requirement:** The DLS SHALL output data to the communication subsystem at rates up to 5 Mbps.

| Attribute | Value |
|-----------|-------|
| Priority | 2 (High) |
| Rationale | Supports complete data downlink within ground contact window |
| Parent | REQ-DLS-SYS-003 |
| Verification Method | Test |
| Status | Approved |
| TBD/TBR | None |

### REQ-DLS-PER-004: Power Consumption
**Requirement:** The DLS SHALL consume no more than 15 Watts in operational mode.

| Attribute | Value |
|-----------|-------|
| Priority | 2 (High) |
| Rationale | Allocated power budget from EMS power subsystem |
| Parent | STRQ-EMS-045 |
| Verification Method | Test |
| Status | Approved |
| TBD/TBR | None |

---

## 6. Interface Requirements

### REQ-DLS-INT-001: Instrument Interface
**Requirement:** The DLS SHALL interface with instruments via RS-422 serial connections compliant with ICD-DLS-INS-001.

| Attribute | Value |
|-----------|-------|
| Priority | 1 (Critical) |
| Rationale | Standardized instrument interface |
| Parent | REQ-DLS-SYS-001 |
| Verification Method | Inspection, Test |
| Status | Approved |
| TBD/TBR | None |
| ICD Reference | ICD-DLS-INS-001 |

### REQ-DLS-INT-002: Communication Interface
**Requirement:** The DLS SHALL provide data to the communication subsystem via SpaceWire interface compliant with ICD-DLS-COM-001.

| Attribute | Value |
|-----------|-------|
| Priority | 1 (Critical) |
| Rationale | Common spacecraft data bus standard |
| Parent | REQ-DLS-SYS-003 |
| Verification Method | Test |
| Status | Approved |
| TBD/TBR | None |
| ICD Reference | ICD-DLS-COM-001 |

### REQ-DLS-INT-003: Command Interface
**Requirement:** The DLS SHALL accept commands from the command subsystem via the spacecraft data bus.

| Attribute | Value |
|-----------|-------|
| Priority | 1 (Critical) |
| Rationale | Ground control capability |
| Parent | STRQ-EMS-030 |
| Verification Method | Demonstration |
| Status | Approved |
| TBD/TBR | None |

---

## 7. Environmental Requirements

### REQ-DLS-ENV-001: Operating Temperature
**Requirement:** The DLS SHALL operate within specification over a temperature range of -20°C to +50°C.

| Attribute | Value |
|-----------|-------|
| Priority | 1 (Critical) |
| Rationale | Expected spacecraft thermal environment |
| Parent | STRQ-EMS-050 |
| Verification Method | Test |
| Status | Approved |
| TBD/TBR | None |

### REQ-DLS-ENV-002: Radiation Tolerance
**Requirement:** The DLS SHALL tolerate a total ionizing dose of 30 krad(Si) over the mission lifetime.

| Attribute | Value |
|-----------|-------|
| Priority | 1 (Critical) |
| Rationale | LEO mission radiation environment with margin |
| Parent | STRQ-EMS-055 |
| Verification Method | Analysis, Test |
| Status | Approved |
| TBD/TBR | None |

### REQ-DLS-ENV-003: Vibration
**Requirement:** The DLS SHALL survive launch vibration environments per GEVS Table 2.4-3.

| Attribute | Value |
|-----------|-------|
| Priority | 1 (Critical) |
| Rationale | Launch vehicle qualification requirements |
| Parent | STRQ-EMS-060 |
| Verification Method | Test |
| Status | Approved |
| TBD/TBR | None |

---

## 8. TBD/TBR Summary

| ID | Type | Description | Resolution Plan | Target Date |
|----|------|-------------|-----------------|-------------|
| TBR-001 | TBR | Verify 100ms mode transition is achievable | Prototype testing | PDR |

---

## 9. Traceability Summary

| System Req | Derived From | Derives To |
|------------|--------------|------------|
| REQ-DLS-SYS-001 | STRQ-EMS-012 | REQ-DLS-FUN-001, FUN-002, INT-001, PER-001 |
| REQ-DLS-SYS-002 | STRQ-EMS-015 | REQ-DLS-FUN-003, FUN-004, PER-002 |
| REQ-DLS-SYS-003 | STRQ-EMS-018 | REQ-DLS-INT-002, PER-003 |

---

## Key Takeaways (Exemplar Notes)

### Correct Requirement Format
- Uses "SHALL" for mandatory requirements
- Specific, measurable values (not "fast" but "100 milliseconds")
- Testable criteria

### Required Attributes
- Priority (1/2/3 or Critical/High/Medium)
- Rationale (why this requirement exists)
- Parent (traceability to higher-level requirement)
- Verification Method (A/D/I/T)
- Status (Proposed/Approved/Verified)
- TBD/TBR tracking

### Common Mistakes Avoided
- ❌ "The system should be fast" → ✅ "SHALL respond within 100 ms"
- ❌ No rationale → ✅ Clear rationale tied to mission need
- ❌ No parent → ✅ Traced to stakeholder requirement
- ❌ No verification method → ✅ ADIT method specified

---

*DISCLAIMER: This is an AI-generated exemplar for demonstration purposes.
It does not represent actual NASA mission requirements. Use as a format
reference only.*
