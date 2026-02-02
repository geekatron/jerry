# NPR 7123.1D Common Technical Processes Guide

> Quick reference for NASA's 17 Common Technical Processes

---

## Document Information

| Field | Value |
|-------|-------|
| Document ID | NSE-KB-PROC-001 |
| Version | 1.0.0 |
| Date | 2026-01-09 |
| Source | NPR 7123.1D Chapter 3 |

---

## Process Categories Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                    17 COMMON TECHNICAL PROCESSES                     │
├─────────────────────┬──────────────────────┬────────────────────────┤
│  SYSTEM DESIGN (4)  │ PRODUCT REALIZATION  │ TECHNICAL MANAGEMENT   │
│                     │        (5)           │         (8)            │
├─────────────────────┼──────────────────────┼────────────────────────┤
│ 1. Stakeholder Exp  │ 5. Implementation    │ 10. Technical Planning │
│ 2. Tech Req Def     │ 6. Integration       │ 11. Requirements Mgmt  │
│ 3. Logical Decomp   │ 7. Verification      │ 12. Interface Mgmt     │
│ 4. Design Solution  │ 8. Validation        │ 13. Risk Management    │
│                     │ 9. Transition        │ 14. Config Management  │
│                     │                      │ 15. Data Management    │
│                     │                      │ 16. Tech Assessment    │
│                     │                      │ 17. Decision Analysis  │
└─────────────────────┴──────────────────────┴────────────────────────┘
```

---

## System Design Processes

### Process 1: Stakeholder Expectations Definition

**Purpose:** Identify stakeholders and capture their expectations, needs, and constraints.

**Key Activities:**
1. Identify all stakeholders
2. Elicit stakeholder expectations
3. Define operational scenarios
4. Document constraints
5. Establish stakeholder requirements baseline

**Inputs:**
- Mission objectives
- Programmatic constraints
- Regulatory requirements
- User feedback

**Outputs:**
- Stakeholder requirements document
- Concept of Operations (ConOps)
- Operational scenarios
- Constraints document

**NSE Agent:** `nse-requirements`

**Key Questions:**
- Who are the stakeholders?
- What do they need the system to do?
- What constraints exist?
- What is the operational context?

---

### Process 2: Technical Requirements Definition

**Purpose:** Transform stakeholder expectations into technical requirements.

**Key Activities:**
1. Analyze stakeholder requirements
2. Derive technical requirements
3. Define requirement attributes (rationale, verification method)
4. Establish requirement hierarchy
5. Baseline requirements

**Inputs:**
- Stakeholder requirements
- ConOps
- Constraints
- Standards and regulations

**Outputs:**
- System requirements specification
- Derived requirements
- Requirements traceability matrix
- TBD/TBR list

**NSE Agent:** `nse-requirements`

**Requirement Quality Criteria:**
- **Necessary:** Contributes to mission/system need
- **Unambiguous:** Single interpretation
- **Measurable:** Can be verified objectively
- **Achievable:** Technically feasible
- **Traceable:** Linked to higher-level need
- **Complete:** Sufficient detail for implementation

**Requirement Format:**
```
[System/Item] SHALL [action] [measurable outcome] [under condition].
```

---

### Process 3: Logical Decomposition

**Purpose:** Define the functional architecture - what the system does.

**Key Activities:**
1. Identify system functions
2. Decompose functions hierarchically
3. Define functional interfaces
4. Allocate functions to logical elements
5. Define operational modes and states

**Inputs:**
- Technical requirements
- ConOps
- Interface requirements

**Outputs:**
- Functional architecture
- Functional flow diagrams (FFBD)
- N² diagram (functional)
- Function allocation matrix
- Mode/state diagrams

**NSE Agent:** `nse-architecture`

**Decomposition Levels:**
```
System Function
├── Subsystem Function 1
│   ├── Component Function 1.1
│   └── Component Function 1.2
└── Subsystem Function 2
    └── Component Function 2.1
```

---

### Process 4: Design Solution Definition

**Purpose:** Define the physical architecture - how the system is built.

**Key Activities:**
1. Generate design alternatives
2. Conduct trade studies
3. Select design solution
4. Define physical interfaces
5. Allocate requirements to design elements

**Inputs:**
- Functional architecture
- Technical requirements
- Constraints (cost, schedule, technology)

**Outputs:**
- Physical architecture
- Trade study reports
- Design descriptions
- Interface definitions
- Requirements allocation matrix

**NSE Agent:** `nse-architecture`

**Trade Study Elements:**
1. Evaluation criteria (weighted)
2. Alternatives description
3. Scoring matrix
4. Sensitivity analysis
5. Recommendation with rationale

---

## Product Realization Processes

### Process 5: Product Implementation

**Purpose:** Build, code, or procure the product.

**Key Activities:**
1. Develop detailed designs
2. Fabricate hardware / code software
3. Conduct peer reviews
4. Document as-built configuration
5. Prepare for integration

**Inputs:**
- Design documentation
- Interface specifications
- Build/coding standards

**Outputs:**
- Hardware/software products
- As-built documentation
- Unit test results
- Manufacturing records

**NSE Agent:** (Implementation typically outside NSE scope)

---

### Process 6: Product Integration

**Purpose:** Assemble components into a functioning system.

**Key Activities:**
1. Plan integration sequence
2. Prepare integration environment
3. Assemble components
4. Verify interfaces
5. Conduct integration testing

**Inputs:**
- Integration plan
- Verified components
- ICDs

**Outputs:**
- Integrated system
- Integration test results
- Interface verification records

**NSE Agent:** `nse-integration`

**Integration Approaches:**
- **Bottom-up:** Integrate lowest levels first
- **Top-down:** Start with system level stubs
- **Incremental:** Add components progressively
- **Big bang:** Integrate all at once (not recommended)

---

### Process 7: Product Verification

**Purpose:** Prove the product meets requirements.

**Key Activities:**
1. Develop verification procedures
2. Conduct verification activities (A/D/I/T)
3. Document results
4. Analyze failures
5. Update VCRM

**Inputs:**
- Requirements baseline
- Verification procedures
- Product to be verified

**Outputs:**
- Verification results
- Test reports
- Anomaly reports
- Updated VCRM

**NSE Agent:** `nse-verification`

**Verification Methods (ADIT):**
| Method | Description | Best For |
|--------|-------------|----------|
| **A**nalysis | Calculation, modeling | Performance predictions |
| **D**emonstration | Show capability works | Operational scenarios |
| **I**nspection | Visual/physical exam | Physical attributes |
| **T**est | Execute and measure | Quantitative requirements |

---

### Process 8: Product Validation

**Purpose:** Prove the product meets stakeholder needs and intended use.

**Key Activities:**
1. Develop validation plan
2. Define success criteria
3. Conduct validation activities
4. Collect stakeholder feedback
5. Document results

**Inputs:**
- Stakeholder requirements
- Validation plan
- Operational system

**Outputs:**
- Validation results
- Stakeholder acceptance
- Operational qualification

**NSE Agent:** `nse-verification`

**Verification vs Validation:**
- **Verification:** "Did we build the product right?" (meets requirements)
- **Validation:** "Did we build the right product?" (meets needs)

---

### Process 9: Product Transition

**Purpose:** Transition product to operations and sustaining.

**Key Activities:**
1. Prepare operations documentation
2. Train operators and maintainers
3. Transfer technical data
4. Establish support infrastructure
5. Handover to operations

**Inputs:**
- Validated product
- Operations procedures
- Training materials

**Outputs:**
- Operational system
- Trained personnel
- Support infrastructure
- Transition records

**NSE Agent:** (Transition typically outside NSE scope)

---

## Technical Management Processes

### Process 10: Technical Planning

**Purpose:** Plan and organize SE activities.

**Key Activities:**
1. Develop SE Management Plan (SEMP)
2. Identify SE tasks and schedule
3. Allocate resources
4. Define metrics
5. Integrate with project plan

**Inputs:**
- Project requirements
- Resource constraints
- Organizational standards

**Outputs:**
- SEMP
- SE schedule
- Resource allocation
- SE metrics plan

**NSE Agent:** (Planning typically user-driven)

---

### Process 11: Requirements Management

**Purpose:** Maintain the requirements baseline.

**Key Activities:**
1. Establish requirements baseline
2. Control changes to requirements
3. Maintain traceability
4. Manage TBDs/TBRs
5. Track requirements status

**Inputs:**
- Approved requirements
- Change requests
- Status updates

**Outputs:**
- Current requirements baseline
- Traceability matrix
- TBD/TBR status
- Requirements status reports

**NSE Agent:** `nse-requirements`

**Requirements States:**
- **Proposed:** Under review
- **Approved:** Baselined
- **Implemented:** In design/code
- **Verified:** Verification complete
- **Deleted:** Removed from baseline

---

### Process 12: Interface Management

**Purpose:** Identify and control interfaces.

**Key Activities:**
1. Identify interfaces
2. Document interface requirements
3. Develop ICDs
4. Control interface changes
5. Verify interface compatibility

**Inputs:**
- System architecture
- Interface requirements
- Integration plans

**Outputs:**
- Interface list
- ICDs
- N² diagram
- Interface verification records

**NSE Agent:** `nse-integration`

**Interface Types:**
- **Physical:** Mechanical, electrical connections
- **Functional:** Data, commands, services
- **Environmental:** Thermal, EMI, vibration

---

### Process 13: Technical Risk Management

**Purpose:** Identify and mitigate technical risks.

**Key Activities:**
1. Identify risks
2. Analyze likelihood and consequence
3. Plan risk mitigations
4. Monitor risk status
5. Report and escalate

**Inputs:**
- Technical assessments
- Schedule/cost data
- Historical data

**Outputs:**
- Risk register
- Risk reports
- Mitigation plans
- Risk trends

**NSE Agent:** `nse-risk`

**Risk Process Flow:**
```
Identify → Analyze → Plan → Track → Control → Close
```

---

### Process 14: Configuration Management

**Purpose:** Control product and documentation baselines.

**Key Activities:**
1. Identify configuration items
2. Establish baselines
3. Control changes
4. Record configuration status
5. Verify configuration

**Inputs:**
- Products and documents
- Change requests
- Baseline definitions

**Outputs:**
- CI list
- Baselines
- Change records
- CM audit results

**NSE Agent:** `nse-configuration`

**Baseline Types:**
| Baseline | Content | Established At |
|----------|---------|----------------|
| Functional | Requirements | SRR |
| Allocated | Design allocation | PDR |
| Product | As-built design | CDR/TRR |

---

### Process 15: Technical Data Management

**Purpose:** Plan and control technical documentation.

**Key Activities:**
1. Identify required documents
2. Develop documentation
3. Control document versions
4. Distribute documents
5. Archive records

**Inputs:**
- Documentation requirements
- Technical content
- Distribution needs

**Outputs:**
- Document tree
- Controlled documents
- Distribution records
- Archives

**NSE Agent:** `nse-configuration`

---

### Process 16: Technical Assessment

**Purpose:** Assess technical health and progress.

**Key Activities:**
1. Measure technical performance
2. Assess progress against plans
3. Evaluate risk status
4. Identify issues
5. Report status

**Inputs:**
- Technical metrics
- Schedule/cost data
- Risk data

**Outputs:**
- Status reports
- Technical assessments
- Issue tracking
- Recommendations

**NSE Agent:** `nse-reporter`

**Assessment Metrics:**
- Requirements stability
- Verification progress
- Risk trends
- Technical performance measures (TPMs)
- Schedule/cost performance

---

### Process 17: Decision Analysis

**Purpose:** Support technical decision making.

**Key Activities:**
1. Define decision criteria
2. Identify alternatives
3. Evaluate alternatives
4. Perform sensitivity analysis
5. Document decision rationale

**Inputs:**
- Decision statement
- Alternatives
- Evaluation criteria

**Outputs:**
- Trade study report
- Decision record
- Sensitivity analysis

**NSE Agent:** `nse-architecture`

**Decision Methods:**
- Kepner-Tregoe
- Analytical Hierarchy Process (AHP)
- Pugh Matrix
- Weighted scoring matrix

---

## Process Interactions

```
          STAKEHOLDER              SYSTEM                PRODUCT
          NEEDS                    DEFINITION            REALIZATION
              │                        │                      │
              ▼                        ▼                      ▼
        ┌─────────┐            ┌──────────────┐        ┌────────────┐
        │Process 1│───────────▶│  Process 2   │───────▶│ Process 5  │
        │Stkhlder │            │  Tech Req    │        │ Implement  │
        │  Exp    │            │  Definition  │        │            │
        └─────────┘            └──────────────┘        └────────────┘
                                      │                      │
                                      ▼                      ▼
                               ┌──────────────┐        ┌────────────┐
                               │  Process 3   │        │ Process 6  │
                               │  Logical     │───────▶│ Integration│
                               │  Decomp      │        │            │
                               └──────────────┘        └────────────┘
                                      │                      │
                                      ▼                      ▼
                               ┌──────────────┐        ┌────────────┐
                               │  Process 4   │        │ Process 7  │
                               │  Design      │───────▶│ Verifica-  │
                               │  Solution    │        │ tion       │
                               └──────────────┘        └────────────┘
                                                             │
                                                             ▼
                                                       ┌────────────┐
                                                       │ Process 8  │
                                                       │ Validation │
                                                       └────────────┘
                                                             │
                                                             ▼
                                                       ┌────────────┐
                                                       │ Process 9  │
                                                       │ Transition │
                                                       └────────────┘

        ◄──────────── Technical Management (10-17) supports all ────────────►
```

---

## Quick Reference Card

| Process | What | NSE Agent | Key Output |
|---------|------|-----------|------------|
| 1 | Capture stakeholder needs | nse-requirements | ConOps |
| 2 | Define requirements | nse-requirements | Req Spec |
| 3 | Functional architecture | nse-architecture | FFBD, N² |
| 4 | Physical architecture | nse-architecture | Trade studies |
| 5 | Build product | - | Hardware/Software |
| 6 | Integrate system | nse-integration | Integrated system |
| 7 | Verify requirements | nse-verification | VCRM, test results |
| 8 | Validate for use | nse-verification | Validation results |
| 9 | Deploy to ops | - | Operational system |
| 10 | Plan SE work | - | SEMP |
| 11 | Control requirements | nse-requirements | Traceability |
| 12 | Control interfaces | nse-integration | ICDs |
| 13 | Manage risks | nse-risk | Risk register |
| 14 | Control configuration | nse-configuration | Baselines |
| 15 | Control documentation | nse-configuration | Doc tree |
| 16 | Assess status | nse-reporter | Status reports |
| 17 | Support decisions | nse-architecture | Trade studies |

---

*DISCLAIMER: This process guide is AI-generated based on NPR 7123.1D. It is
provided for reference only. Always consult official NASA documentation for
authoritative process definitions.*
