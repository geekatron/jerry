# Exemplar: Risk Register

> Demonstrates proper NASA-style risk management format

---

## Document Information

| Field | Value |
|-------|-------|
| Example Type | Risk Register |
| Purpose | Show correct risk format per NPR 8000.4C |
| Based On | NPR 8000.4C, NPR 7123.1D Process 13 |

---

## Example System: Data Logger Subsystem (DLS)

*This is a fictional subsystem used to demonstrate proper risk format.*

---

## Risk Register Header

| Field | Value |
|-------|-------|
| Document ID | RISK-DLS-001 |
| Project | Example Mission System (EMS) |
| Subsystem | Data Logger Subsystem (DLS) |
| Version | 1.0 |
| Date | 2026-01-09 |
| Risk Manager | [Name] |
| Status | Active |

---

## Risk Summary Dashboard

| Level | Count | Change | Status |
|-------|-------|--------|--------|
| 🔴 RED (16-25) | 1 | ↔ | Mitigation in progress |
| 🟡 YELLOW (8-15) | 2 | ↓ | Monitoring |
| 🟢 GREEN (1-7) | 2 | ↔ | Accepted |
| **Total Active** | **5** | | |
| Closed | 1 | | |

---

## 5x5 Risk Matrix (Current State)

|  | **Consequence** |||||
|---|:---:|:---:|:---:|:---:|:---:|
| **Likelihood** | 1 (Min) | 2 (Low) | 3 (Mod) | 4 (High) | 5 (Max) |
| 5 (Very High) | | | | **R-003** | |
| 4 (High) | | | | | |
| 3 (Moderate) | | | R-002 | | |
| 2 (Low) | | R-005 | R-004 | | |
| 1 (Very Low) | R-001 | | | | |

---

## Active Risks

### R-001: Flight Processor Performance Margin

| Attribute | Value |
|-----------|-------|
| **ID** | R-001 |
| **Status** | 🟢 GREEN - Watch |
| **Category** | Technical |
| **Owner** | Software Lead |
| **Identified** | 2026-01-01 |
| **Last Updated** | 2026-01-09 |

**Risk Statement:**
> IF the flight processor load exceeds 80% during peak data acquisition,
> THEN the DLS may miss data samples, resulting in science data gaps.

**Context:**
Current processor load analysis shows 65% utilization during peak operations. Margin exists but needs monitoring as software matures.

| Factor | Score | Rationale |
|--------|-------|-----------|
| Likelihood | 1 (Very Low) | Current analysis shows 15% margin |
| Consequence | 3 (Moderate) | Would affect science return quality |
| **Risk Score** | **3** | 1 × 3 = 3 (GREEN) |

**Mitigation Plan:**
| # | Action | Owner | Due | Status |
|---|--------|-------|-----|--------|
| 1 | Monitor processor load weekly | SW Lead | Ongoing | Active |
| 2 | Implement load shedding algorithm | SW Lead | PDR | Planned |

**Trigger for Escalation:** Processor load exceeds 75%

---

### R-002: COTS Memory Component Obsolescence

| Attribute | Value |
|-----------|-------|
| **ID** | R-002 |
| **Status** | 🟡 YELLOW - Mitigate |
| **Category** | Technical / Schedule |
| **Owner** | Hardware Lead |
| **Identified** | 2025-12-15 |
| **Last Updated** | 2026-01-09 |

**Risk Statement:**
> IF the selected NAND flash memory component becomes obsolete before
> flight unit procurement, THEN a redesign may be required, resulting
> in schedule delay and cost increase.

**Context:**
Vendor has indicated end-of-life within 18 months. Flight procurement scheduled for month 14.

| Factor | Score | Rationale |
|--------|-------|-----------|
| Likelihood | 3 (Moderate) | EOL notice received, timing is tight |
| Consequence | 3 (Moderate) | Redesign would impact schedule 2-3 months |
| **Risk Score** | **9** | 3 × 3 = 9 (YELLOW) |

**Mitigation Plan:**
| # | Action | Owner | Due | Status |
|---|--------|-------|-----|--------|
| 1 | Identify alternate memory components | HW Lead | 2026-01-31 | In Progress |
| 2 | Qualify alternate component | HW Lead | PDR | Planned |
| 3 | Accelerate flight unit procurement | PM | 2026-02-15 | Evaluating |
| 4 | Establish lifetime buy if needed | Procurement | CDR | Contingency |

**Trigger for Escalation:** No qualified alternate by PDR

**Residual Risk (after mitigation):** Score 4 (L=2, C=2) - GREEN

---

### R-003: Radiation-Induced Single Event Upsets

| Attribute | Value |
|-----------|-------|
| **ID** | R-003 |
| **Status** | 🔴 RED - Immediate Action |
| **Category** | Technical / Safety |
| **Owner** | Systems Engineer |
| **Identified** | 2025-11-01 |
| **Last Updated** | 2026-01-09 |

**Risk Statement:**
> IF single event upsets (SEUs) occur in the DLS flight software at a higher
> rate than predicted, THEN data corruption and system resets may occur,
> resulting in loss of science data and potential safe mode entry.

**Context:**
Initial radiation analysis indicates higher SEU rate than heritage missions due to different orbit. Current EDAC implementation may be insufficient.

| Factor | Score | Rationale |
|--------|-------|-----------|
| Likelihood | 5 (Very High) | Analysis predicts 2× heritage SEU rate |
| Consequence | 4 (High) | Could cause data loss and safe mode |
| **Risk Score** | **20** | 5 × 4 = 20 (RED) |

**Mitigation Plan:**
| # | Action | Owner | Due | Status |
|---|--------|-------|-----|--------|
| 1 | Enhanced EDAC implementation | SW Lead | 2026-01-20 | In Progress |
| 2 | Memory scrubbing algorithm | SW Lead | 2026-02-01 | Planned |
| 3 | Radiation testing of updated design | Test Lead | PDR+30 | Planned |
| 4 | Safe mode recovery procedures | Ops Lead | CDR | Planned |

**Trigger for Escalation:** Already at RED - Weekly reporting to project

**Residual Risk (after mitigation):** Score 10 (L=2, C=5) - YELLOW
- Note: Consequence remains high (cannot reduce SEU effects), but likelihood of impact reduced through mitigation

**Escalation Actions:**
- ✅ Project manager notified
- ✅ Added to weekly status report
- ⏳ Review at next PMR

---

### R-004: Integration Schedule Compression

| Attribute | Value |
|-----------|-------|
| **ID** | R-004 |
| **Status** | 🟡 YELLOW - Mitigate |
| **Category** | Schedule |
| **Owner** | Integration Lead |
| **Identified** | 2026-01-05 |
| **Last Updated** | 2026-01-09 |

**Risk Statement:**
> IF hardware delivery is delayed by more than 2 weeks,
> THEN integration and test schedule will be compressed,
> resulting in reduced test coverage or schedule slip.

**Context:**
Current hardware delivery forecast shows 1 week margin. Supply chain issues have affected similar programs.

| Factor | Score | Rationale |
|--------|-------|-----------|
| Likelihood | 2 (Low) | 1 week margin currently exists |
| Consequence | 3 (Moderate) | Would require test prioritization |
| **Risk Score** | **6** | 2 × 3 = 6 (GREEN, borderline YELLOW) |

**Mitigation Plan:**
| # | Action | Owner | Due | Status |
|---|--------|-------|-----|--------|
| 1 | Weekly vendor status calls | Procurement | Ongoing | Active |
| 2 | Develop prioritized test plan | Test Lead | 2026-01-15 | In Progress |
| 3 | Identify parallel test opportunities | I&T Lead | 2026-01-20 | Planned |

**Trigger for Escalation:** Hardware delivery slips beyond 1 week

---

### R-005: Test Equipment Availability

| Attribute | Value |
|-----------|-------|
| **ID** | R-005 |
| **Status** | 🟢 GREEN - Watch |
| **Category** | Resource |
| **Owner** | Test Lead |
| **Identified** | 2025-12-01 |
| **Last Updated** | 2026-01-09 |

**Risk Statement:**
> IF the thermal vacuum chamber is not available during the scheduled
> test window, THEN environmental testing will be delayed, resulting
> in schedule slip.

**Context:**
Chamber scheduled for maintenance 2 weeks before our window. Backup chamber identified.

| Factor | Score | Rationale |
|--------|-------|-----------|
| Likelihood | 2 (Low) | Backup chamber available |
| Consequence | 2 (Low) | 1-2 week slip maximum |
| **Risk Score** | **4** | 2 × 2 = 4 (GREEN) |

**Mitigation Plan:**
| # | Action | Owner | Due | Status |
|---|--------|-------|-----|--------|
| 1 | Reserve backup chamber | Test Lead | 2026-01-10 | Complete |
| 2 | Confirm maintenance schedule | Facilities | 2026-01-15 | In Progress |

**Trigger for Escalation:** Maintenance extends into test window

---

## Closed Risks

### R-006: Requirements Stability (CLOSED)

| Attribute | Value |
|-----------|-------|
| **ID** | R-006 |
| **Status** | ✅ CLOSED |
| **Category** | Technical |
| **Owner** | Systems Engineer |
| **Identified** | 2025-10-01 |
| **Closed** | 2026-01-05 |

**Original Risk Statement:**
> IF stakeholder requirements continue to change after SRR,
> THEN design rework will be required, resulting in schedule and cost impact.

**Closure Rationale:**
Requirements baseline established and approved at SRR. Change control process implemented. No changes requested in 30 days post-SRR.

**Final Score at Closure:** 2 (L=1, C=2) - GREEN

---

## Risk Trends

| Period | RED | YELLOW | GREEN | Total | Exposure |
|--------|-----|--------|-------|-------|----------|
| 2026-01 | 1 | 2 | 2 | 5 | 42 |
| 2025-12 | 1 | 3 | 2 | 6 | 48 |
| 2025-11 | 2 | 2 | 1 | 5 | 55 |

*Exposure = Sum of all risk scores*

**Trend Analysis:**
- Overall exposure decreasing (55 → 42)
- One YELLOW closed, one RED remains
- Focus on R-003 mitigation completion

---

## Key Takeaways (Exemplar Notes)

### Correct Risk Statement Format
```
IF [condition/event that may occur],
THEN [consequence to project objective],
resulting in [impact to cost/schedule/technical/safety].
```

### Required Risk Attributes
- Unique ID
- Status (with color)
- Category (Technical/Cost/Schedule/Safety)
- Owner (accountable person)
- Dates (identified, updated)
- Likelihood and Consequence scores
- Mitigation plan with actions
- Triggers for escalation
- Residual risk (post-mitigation)

### Risk Scoring (5x5 Matrix)
- **Likelihood:** 1-5 (Very Low to Very High)
- **Consequence:** 1-5 (Minimal to Maximum)
- **Score:** L × C
- **Levels:** GREEN (1-7), YELLOW (8-15), RED (16-25)

### RED Risk Requirements
- Immediate escalation to project management
- Weekly status reporting
- Active mitigation in progress
- Review at major milestones

---

*DISCLAIMER: This is an AI-generated exemplar for demonstration purposes.
It does not represent actual NASA mission risks. Use as a format reference only.*
