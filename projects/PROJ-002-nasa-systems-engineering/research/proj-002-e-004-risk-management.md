# NASA Risk Management Framework Research

> **PS ID:** proj-002 | **Entry ID:** e-004
> **Topic:** NASA Risk Management Framework
> **Researcher:** ps-researcher (Claude)
> **Date:** 2026-01-09
> **Status:** COMPLETE

---

## Executive Summary

NASA's Risk Management (RM) framework is a comprehensive system for identifying, analyzing, planning, tracking, controlling, and communicating risks across all Agency activities. The framework is anchored by two complementary processes: **Risk-Informed Decision Making (RIDM)** and **Continuous Risk Management (CRM)**. This research documents the procedural requirements from NPR 8000.4C, technical risk management from NPR 7123.1D, and implementation guidance from the NASA Risk Management Handbook.

---

## L0: Quick Reference Card

### Core Documents
| Document | Title | Purpose |
|----------|-------|---------|
| NPR 8000.4C | Agency Risk Management Procedural Requirements | Policy and requirements |
| NPR 7123.1D | NASA Systems Engineering Processes and Requirements | Process 14: Technical Risk Management |
| NASA/SP-2011-3422 | NASA Risk Management Handbook | Implementation guidance |
| NASA/SP-2010-576 | NASA RIDM Handbook | Decision-making guidance |

### Risk Definition
> "Risk is the potential for shortfalls with respect to achieving explicitly established and stated objectives."

### Risk Characterization Components
1. **Scenarios** - Pathways from risk sources to degraded performance
2. **Likelihood** - Probability of occurrence (qualitative or quantitative)
3. **Consequence** - Severity of performance degradation

### Five Performance Domains
1. Safety
2. Mission Success (Technical)
3. Physical Security and Cybersecurity
4. Cost
5. Schedule

### Risk Statement Format
```
Given [CONDITION], there is possibility of [DEPARTURE] adversely impacting [ASSET],
thereby leading to [CONSEQUENCE].
```

### CRM Six-Step Process
**I-A-P-T-C-C**: Identify > Analyze > Plan > Track > Control > Communicate

### Risk Disposition Options
- **Accept** - Document rationale, monitor
- **Mitigate** - Reduce likelihood or consequence
- **Watch** - Monitor without active mitigation
- **Research** - Gather more information
- **Elevate** - Escalate to higher authority
- **Close** - Risk no longer applicable

---

## L1: Detailed Framework

### 1. Risk-Informed Decision Making (RIDM)

RIDM is the process for informing decision-making through better use of risk and uncertainty information when selecting alternatives and establishing baseline performance commitments.

#### RIDM Three-Phase Process

```
+---------------------------+      +---------------------------+      +---------------------------+
|   PHASE 1: IDENTIFY       |      |   PHASE 2: ANALYZE        |      |   PHASE 3: SELECT         |
|   ALTERNATIVES            | ---> |   ALTERNATIVES            | ---> |   ALTERNATIVE             |
+---------------------------+      +---------------------------+      +---------------------------+
| - Formulate objectives    |      | - Conduct integrated risk |      | - Deliberate using        |
| - Develop performance     |      |   analysis for each option|      |   complete performance    |
|   measures                |      | - Develop technical basis |      |   data                    |
| - Compile decision        |      |   for deliberation        |      | - Select alternative      |
|   alternatives            |      | - Quantify performance    |      | - Document rationale with |
| - Recognize risks and     |      |   measures with           |      |   risk acceptance         |
|   opportunities           |      |   uncertainty             |      | - Establish baseline      |
+---------------------------+      +---------------------------+      +---------------------------+
```

#### RIDM Application Triggers
- Mission concept development
- Architecture selection
- Technology investment decisions
- Major milestone decisions
- Contract award decisions
- Significant design changes

### 2. Continuous Risk Management (CRM)

CRM is the ongoing process for managing risks during activity execution, applied once decisions are made through RIDM.

#### CRM Six-Step Cycle

```
                    +-------------+
                    |  IDENTIFY   |
                    |  Step 1     |
                    +------+------+
                           |
                           v
+-------------+     +------+------+     +-------------+
|  COMMUNICATE| <-- |   ANALYZE   | --> |    PLAN     |
|  Step 6     |     |   Step 2    |     |   Step 3    |
+-------------+     +-------------+     +------+------+
      ^                                        |
      |                                        v
      |            +-------------+      +------+------+
      +----------- |   CONTROL   | <--- |    TRACK    |
                   |   Step 5    |      |   Step 4    |
                   +-------------+      +-------------+
```

#### Step Details

| Step | Activities | Outputs |
|------|------------|---------|
| **1. IDENTIFY** | Determine performance shortfall contributors; document risks using structured statements | Risk statements, risk register entries |
| **2. ANALYZE** | Estimate probability and consequence; assess uncertainty; prioritize risks | Likelihood/consequence ratings, aggregate risk characterization |
| **3. PLAN** | Select risk disposition; develop mitigation and contingency plans; establish triggers | Risk handling plans, trigger thresholds |
| **4. TRACK** | Monitor performance observables; track mitigation effectiveness; collect data | Status reports, metrics, updated risk data |
| **5. CONTROL** | Verify mitigation success; execute contingency plans if triggered; adjust plans | Corrective actions, updated plans |
| **6. COMMUNICATE** | Document all activities; share risk information with stakeholders | Reports, briefings, lessons learned |

### 3. The 5x5 Risk Matrix

#### Likelihood Levels (Y-Axis)

| Level | Descriptor | Probability Range | Description |
|-------|------------|-------------------|-------------|
| **5** | Near Certainty | >80% | Expected to occur multiple times; virtually certain |
| **4** | Highly Likely | 60-80% | Will probably occur; more likely than not |
| **3** | Likely | 40-60% | May occur; about even odds |
| **2** | Not Very Likely | 20-40% | Unlikely but possible; can reasonably be expected |
| **1** | Not Likely | <20% | Improbable; would be surprising if it occurred |

#### Consequence Levels (X-Axis)

| Level | Technical | Cost | Schedule | Safety |
|-------|-----------|------|----------|--------|
| **5 - Very High** | Loss of mission; cannot meet minimum requirements | >25% budget overrun | >12 months slip; misses critical window | Loss of life; permanent disability |
| **4 - High** | Major degradation; significant capability loss | 15-25% budget overrun | 6-12 months slip | Severe injury; long-term health effects |
| **3 - Moderate** | Moderate degradation; some capability loss | 5-15% budget overrun | 3-6 months slip | Minor injury; temporary health effects |
| **2 - Low** | Minor degradation; meets minimum requirements | 1-5% budget overrun | 1-3 months slip | First aid treatment only |
| **1 - Very Low** | Negligible impact | <1% budget overrun | <1 month slip | No injury |

#### Risk Matrix Color Zones

```
     |  1  |  2  |  3  |  4  |  5  |   Consequence
-----+-----+-----+-----+-----+-----+
  5  | MED |HIGH |HIGH |VHGH |VHGH |
-----+-----+-----+-----+-----+-----+
  4  | LOW |MED  |HIGH |HIGH |VHGH |
-----+-----+-----+-----+-----+-----+
L 3  | LOW |MED  |MED  |HIGH |HIGH |
-----+-----+-----+-----+-----+-----+
  2  |VLOW | LOW |MED  |MED  |HIGH |
-----+-----+-----+-----+-----+-----+
  1  |VLOW |VLOW | LOW |MED  |MED  |
-----+-----+-----+-----+-----+-----+

Legend:
VLOW (Green)  = Watch list; monitor only
LOW  (Green)  = Research; develop mitigation plan
MED  (Yellow) = Active mitigation; continuous assessment
HIGH (Orange) = Escalate internally; assign significant resources
VHGH (Red)    = Critical attention; consider plan restructuring
```

### 4. Risk Statement Structure

#### Standard Format
```
Given [CONDITION], there is possibility of [DEPARTURE] adversely impacting [ASSET],
thereby leading to [CONSEQUENCE].
```

#### Components

| Component | Description | Example |
|-----------|-------------|---------|
| **CONDITION** | Current state, fact, or circumstance (root cause) | "Given that vendor X has limited experience with rad-hard components" |
| **DEPARTURE** | Undesired event or deviation | "there is possibility of delayed component delivery" |
| **ASSET** | What is affected (mission, system, schedule, budget) | "adversely impacting integration schedule" |
| **CONSEQUENCE** | Impact on objectives | "thereby leading to 3-month launch slip" |

#### Example Risk Statements

**Technical Risk:**
> Given that the new propulsion system design has not been flight-tested, there is possibility of unexpected performance degradation during orbital insertion, adversely impacting delta-v margin, thereby leading to failure to achieve target orbit.

**Cost Risk:**
> Given that labor rate negotiations are ongoing, there is possibility of 15% labor cost increase, adversely impacting Phase C budget, thereby leading to scope reduction or schedule extension.

**Schedule Risk:**
> Given that critical heritage software requires significant modification, there is possibility of extended V&V cycles, adversely impacting delivery milestones, thereby leading to 6-month delay to CDR.

### 5. Risk Mitigation Strategies

| Strategy | Description | When to Use |
|----------|-------------|-------------|
| **Accept** | Document rationale; monitor; no active mitigation | Low impact/likelihood; cost of mitigation exceeds benefit |
| **Avoid** | Eliminate risk source; change approach | Risk is unacceptable; alternative approaches available |
| **Mitigate** | Reduce likelihood or consequence | High-priority risks; mitigation is cost-effective |
| **Transfer** | Shift risk ownership (insurance, contractor) | Risk is outside core competency; partner can manage better |
| **Watch** | Monitor indicators; no active mitigation | Uncertain risks; triggers will indicate if action needed |
| **Research** | Gather information to reduce uncertainty | Insufficient data for informed decision |

#### Mitigation Plan Elements
1. Risk ID and statement
2. Selected handling strategy
3. Mitigation actions with owners
4. Resources required
5. Schedule milestones
6. Success criteria
7. Trigger thresholds for contingency
8. Contingency actions if triggers hit

### 6. Risk Acceptance and Escalation

#### Acceptance Authority Hierarchy

```
+------------------+
| NASA Administrator |  <-- Agency-level risks; cross-program/cross-center
+--------+---------+
         |
+--------v---------+
| Mission Directorate |  <-- Multi-program risks; major technical decisions
+--------+---------+
         |
+--------v---------+
|  Program Manager   |  <-- Program-level risks; resource allocation
+--------+---------+
         |
+--------v---------+
|  Project Manager   |  <-- Project-level risks; day-to-day management
+------------------+
```

#### Escalation Triggers
- Risk exceeds authority threshold (defined in Risk Management Plan)
- Additional Agency resources needed for mitigation
- Cross-organizational coordination required
- Risk spans programmatic and institutional boundaries
- Technical Authority involvement required for safety/reliability
- Risk acceptance affects multiple stakeholders

#### Risk Acceptance Criteria (from NPR 8000.4C)
> "A rule for determining whether a given organizational unit has the authority to decide to accept a risk."

Key requirements:
- Single responsible individual (not committee) accountable
- Document rationale for acceptance
- Report acceptance one level up in hierarchy
- Technical Authority concurrence for safety-related risks

---

## L2: Implementation Details

### 7. NPR 8000.4C Requirements Summary

#### Chapter 1: Framework
- Defines risk as "potential for shortfalls with respect to achieving explicitly established and stated objectives"
- Establishes RIDM and CRM as complementary processes
- Covers all Agency activities: strategic planning, program/project management, institutional infrastructure, acquisition
- Effective: April 19, 2022; Expires: April 19, 2027

#### Chapter 3: Key Requirements

| Requirement Area | Key Points |
|-----------------|------------|
| **RIDM (3.3)** | Key decisions informed by Analysis of Alternatives; rigor matches significance; document rationale |
| **CRM (3.4.2)** | Full 6-step cycle; structured risk statements; periodic review of assumptions |
| **Risk Management Plan (3.2.2i)** | Risk tolerances; acceptance criteria; elevation protocols; communication protocols; stakeholder identification |
| **Reporting (3.5.5)** | Report risk acceptance decisions one level up; enable aggregate tracking |

#### Risk Categories Addressed
1. Safety
2. Mission Success (Technical Performance)
3. Physical Security and Cybersecurity
4. Cost
5. Schedule

#### Risk Sources Classification
| Source Type | Examples |
|-------------|----------|
| Internal Random | Component failure, software defect |
| Internal Intentional | Sabotage, neglect, shortcuts |
| External Random | Lightning, micrometeorite, solar flare |
| External Intentional | Cyber attack, adversarial interference |

### 8. NPR 7123.1D Process 14: Technical Risk Management

> Note: Technical Risk Management is **Process 14** in NPR 7123.1D (not Process 13, which is Interface Management).

#### Purpose
> "To make risk-informed decisions and examine, on a continuing basis, the potential for deviations from the program/project plan."

#### Key Activities
1. **Risk Identification** - Continuous identification including source, consequences, likelihood
2. **Risk Assessment** - Using both RIDM (strategic) and CRM (execution)
3. **Risk Planning** - Select risks for mitigation; establish triggers; develop contingency plans
4. **Risk Tracking** - Periodic monitoring; status reports to management boards and lifecycle reviews

#### Inputs
- Project Risk Management Plan
- Technical risk issues from design/development
- Status measurements
- Reporting requirements

#### Outputs
- Technical risk mitigation/contingency actions
- Risk status reports
- Lessons learned

#### Integration Requirements
- Use NPR 8000.4 as source document
- Coordinate with Technical Authority
- Include cybersecurity risks (update from NPR 7123.1C)

### 9. NASA Risk Management Handbook (NASA/SP-2011-3422)

#### Purpose
Provide guidance for implementing NPR 8000.4 requirements with focus on programs and projects.

#### Key Contributions
- Details RIDM implementation for Formulation phase
- Explains CRM application during Execution phase
- Provides risk analysis methods and examples
- Includes uncertainty characterization techniques

#### Version History
| Version | Date | Notes |
|---------|------|-------|
| 1.0 | November 2011 | Original (NASA/SP-2011-3422) |
| 2.0 Part 1 | 2024 | Updated alignment with NPR 8000.4C |
| 2.0 Part 2 | 2024 | Implementation examples |

#### Key Concepts Introduced

**Aggregate Risk**: Cumulative effect of multiple individual risks on objectives.

**Uncertainty Characterization**: Methods for expressing confidence in likelihood/consequence estimates.

**Performance Commitment**: The performance value corresponding to uniform risk tolerance, established during RIDM and managed via CRM.

### 10. Risk Register Structure

#### Required Fields
| Field | Description |
|-------|-------------|
| Risk ID | Unique identifier (e.g., R-001, PROJ-R-042) |
| Risk Title | Short descriptive name |
| Risk Statement | Full "Given...there is possibility..." statement |
| Category | Safety, Technical, Cost, Schedule, Security |
| Source | Internal/External, Random/Intentional |
| Likelihood (L) | 1-5 rating with rationale |
| Consequence (C) | 1-5 rating per category with rationale |
| Risk Score | L x C (or highest category) |
| Risk Owner | Individual accountable |
| Status | Active, Watch, Closed, Elevated |
| Handling Strategy | Accept, Mitigate, Watch, Research, Transfer |
| Mitigation Actions | Planned/in-progress actions |
| Target Closure Date | Expected resolution date |
| Trigger Thresholds | Conditions that activate contingency |
| Contingency Actions | Backup plan if triggers hit |
| Last Review Date | Most recent assessment |
| Trend | Increasing, Stable, Decreasing |

#### Example Risk Register Entry

```
Risk ID:        R-042
Title:          Heritage Software Reuse Risk
Statement:      Given that the heritage flight software was developed for a different
                processor architecture, there is possibility of unexpected integration
                issues during porting, adversely impacting software delivery schedule,
                thereby leading to 3-month slip to CDR.
Category:       Technical, Schedule
Source:         Internal Random
Likelihood:     3 (Likely - similar issues on prior projects)
Consequence:
  - Technical:  2 (Minor - workarounds available)
  - Schedule:   4 (High - 6-12 month potential slip)
  - Cost:       3 (Moderate - overtime required)
Risk Score:     12 (L3 x C4)
Owner:          FSW Lead
Status:         Active
Strategy:       Mitigate
Actions:
  1. Early porting prototype (Target: MCR+2mo)
  2. Automated regression test suite (Target: MCR+3mo)
  3. Reserve 2 FTEs for integration support
Trigger:        >15% test failures on prototype
Contingency:    Engage heritage software vendor for support
Last Review:    2026-01-09
Trend:          Stable
```

### 11. INCOSE SE Handbook Alignment

The INCOSE Systems Engineering Handbook v5.0 aligns with NASA's approach through ISO/IEC/IEEE 15288:2023 and ISO/IEC/IEEE 16085:2021.

#### Key INCOSE Risk Concepts

**Risk Definition (ISO 31073):**
> "Effect of uncertainty on objectives."

**Risk Characterization:**
- Probability (or likelihood) of failing to achieve outcome
- Consequences (or impact) of failing to achieve outcome

**Risk Management Process (Section 5.4):**
Consistent with CRM six-step cycle.

#### Goal of SE Activities
> "The goal of all SE activities is to manage risk, including the risk of not delivering what the acquirer wants and needs, the risk of late delivery, the risk of excess cost, and the risk of negative unintended consequences."

---

## Appendix A: Risk Management Zone Actions

| Zone | Color | Risk Score | Required Actions |
|------|-------|------------|------------------|
| **Very Low** | Dark Green | 1-2 | Watch list; re-assess periodically; no mitigation plan required |
| **Low** | Light Green | 3-4 | Research; develop mitigation plan; share with team |
| **Medium** | Yellow | 5-9 | Active mitigation; continuous assessment; assign resources |
| **High** | Orange | 10-16 | Escalate internally; significant resources; management attention |
| **Very High** | Red | 17-25 | Critical; consider plan restructuring; executive escalation |

## Appendix B: Risk Communication Templates

### Risk Status Briefing Format
1. New risks identified this period
2. Risks closed this period
3. Top 5 risks by score (with trends)
4. Risks approaching triggers
5. Mitigation progress summary
6. Elevated risks requiring decision

### Risk Acceptance Documentation
1. Risk ID and statement
2. Current likelihood/consequence with rationale
3. Mitigation attempted and results
4. Residual risk after mitigation
5. Acceptance rationale
6. Accepting authority signature
7. Technical Authority concurrence (if safety-related)
8. Date and review period

---

## References

### Primary Sources
1. [NPR 8000.4C - Agency Risk Management Procedural Requirements](https://nodis3.gsfc.nasa.gov/displayDir.cfm?t=NPR&c=8000&s=4C) (April 2022)
2. [NPR 7123.1D - NASA Systems Engineering Processes and Requirements](https://nodis3.gsfc.nasa.gov/displayDir.cfm?t=NPR&c=7123&s=1B)
3. [NASA Risk Management Handbook (NASA/SP-2011-3422)](https://www.nasa.gov/wp-content/uploads/2023/08/nasa-risk-mgmt-handbook.pdf)
4. [NASA RIDM Handbook (NASA/SP-2010-576)](https://ntrs.nasa.gov/citations/20100021361)
5. [Technical Risk Management - NASA SE Handbook](https://www.nasa.gov/reference/6-4-technical-risk-management/)

### Secondary Sources
6. [Development of Risk Assessment Matrix for NASA Engineering and Safety Center](https://ntrs.nasa.gov/citations/20050123548) (NESC 5x5 Matrix)
7. [NASA Risk Management Handbook Version 2.0](https://ntrs.nasa.gov/citations/20240014019) (2024 Update)
8. [INCOSE SE Handbook v5.0](https://www.incose.org) - Risk Management Chapter
9. [Managing Risk with the NASA Risk Matrix - Ness Labs](https://nesslabs.com/nasa-risk-matrix)
10. [SEBoK - Risk Management](https://sebokwiki.org/wiki/Risk_Management)

### Related Standards
11. ISO/IEC/IEEE 15288:2023 - Systems and software engineering - System life cycle processes
12. ISO/IEC/IEEE 16085:2021 - Life cycle processes - Risk management
13. ISO 31000:2018 - Risk management - Guidelines

---

## Jerry Framework Application Notes

### Skill Integration: nse-risk Agent

This research informs the implementation of the `nse-risk` agent within the Jerry Framework's NASA Systems Engineering skill set.

#### Key Behaviors to Implement
1. **Risk Statement Validation** - Enforce "Given...there is possibility..." format
2. **5x5 Matrix Scoring** - Automated likelihood/consequence rating
3. **Risk Register Management** - CRUD operations on risk items
4. **CRM Cycle Tracking** - Track risks through I-A-P-T-C-C cycle
5. **Escalation Alerts** - Flag risks exceeding threshold for elevation
6. **Trend Analysis** - Track risk score changes over time

#### Domain Model Entities
- `Risk` - Aggregate root
- `RiskStatement` - Value object (condition, departure, asset, consequence)
- `LikelihoodLevel` - Enum (1-5)
- `ConsequenceLevel` - Value object per category
- `RiskScore` - Calculated value
- `MitigationPlan` - Entity
- `RiskHistory` - Audit trail

---

*Research compiled from authoritative NASA sources for Jerry Framework PROJ-002.*
