# NASA Systems Engineering Standards Summary

> Quick reference guide to key NASA SE standards and handbooks

---

## Document Information

| Field | Value |
|-------|-------|
| Document ID | NSE-KB-STD-001 |
| Version | 1.0.0 |
| Date | 2026-01-09 |
| Purpose | Reference summary for NSE agents |

---

## Primary Standards

### NPR 7123.1D: NASA SE Processes and Requirements

**Full Title:** NASA Systems Engineering Processes and Requirements

**Authority:** NASA Procedural Requirements (mandatory for NASA programs)

**Current Version:** Revision D (supersedes 7123.1C)

**Key Content:**

| Chapter | Topic | Key Elements |
|---------|-------|--------------|
| 1 | Introduction | Purpose, applicability, tailoring |
| 2 | Responsibilities | SE roles throughout lifecycle |
| 3 | Common Technical Processes | 17 processes defined below |
| 4 | Technical Reviews | Review objectives and criteria |
| 5 | Technical Planning | SE planning requirements |

**17 Common Technical Processes:**

| # | Process | Category | Purpose |
|---|---------|----------|---------|
| 1 | Stakeholder Expectations Definition | System Design | Capture and document stakeholder needs |
| 2 | Technical Requirements Definition | System Design | Transform needs into requirements |
| 3 | Logical Decomposition | System Design | Define functional architecture |
| 4 | Design Solution Definition | System Design | Create physical architecture |
| 5 | Product Implementation | Product Realization | Build/code the product |
| 6 | Product Integration | Product Realization | Assemble and connect components |
| 7 | Product Verification | Product Realization | Prove requirements are met |
| 8 | Product Validation | Product Realization | Prove product meets intended use |
| 9 | Product Transition | Product Realization | Deploy to operations |
| 10 | Technical Planning | Technical Management | Plan SE activities |
| 11 | Requirements Management | Technical Management | Control requirements baseline |
| 12 | Interface Management | Technical Management | Control interfaces |
| 13 | Technical Risk Management | Technical Management | Identify and mitigate risks |
| 14 | Configuration Management | Technical Management | Control baselines |
| 15 | Technical Data Management | Technical Management | Control documentation |
| 16 | Technical Assessment | Technical Management | Assess technical health |
| 17 | Decision Analysis | Technical Management | Support decisions |

**Appendices:**
- Appendix A: Tailoring guidance
- Appendix B: SEMP content
- Appendix C: Work product descriptions
- Appendix D: SE technical review descriptions
- Appendix G: Technical review entrance/exit criteria

**URL:** https://nodis3.gsfc.nasa.gov/displayDir.cfm?Internal_ID=N_PR_7123_001D_

---

### NASA/SP-2016-6105 Rev2: NASA SE Handbook

**Full Title:** NASA Systems Engineering Handbook

**Authority:** Special Publication (guidance, not mandatory)

**Current Version:** Revision 2 (2016, reprinted 2020)

**Key Content:**

| Chapter | Topic | Key Elements |
|---------|-------|--------------|
| 1 | Introduction | SE overview, handbook purpose |
| 2 | Fundamentals | SE principles, lifecycle models |
| 3 | System Design | Concept development to detail design |
| 4 | Product Realization | Implementation through transition |
| 5 | Cross-Cutting Topics | Risk, CM, software, human factors |
| 6 | Special Topics | MBSE, system of systems, commercial |
| 7 | Applying SE | Tailoring for missions |

**Key Figures:**
- Figure 1.1: NASA Project Lifecycle
- Figure 2.5: Technical Processes and Products
- Figure 3.1: System Design Process Flow
- Figure 4.1: V-Model for Verification

**URL:** https://www.nasa.gov/reference/systems-engineering-handbook/

---

### NPR 8000.4C: Risk Management

**Full Title:** Agency Risk Management Procedural Requirements

**Authority:** NASA Procedural Requirements (mandatory)

**Key Content:**

| Section | Topic | Key Elements |
|---------|-------|--------------|
| 1 | Purpose | Risk management framework |
| 2 | Applicability | All NASA programs/projects |
| 3 | Risk Process | Identification through closure |
| 4 | Risk Categories | Technical, cost, schedule, safety |
| 5 | Risk Assessment | 5x5 matrix methodology |
| 6 | Reporting | Risk reporting requirements |

**5x5 Risk Matrix:**

| | Consequence |||||
|---|:---:|:---:|:---:|:---:|:---:|
| **Likelihood** | 1 | 2 | 3 | 4 | 5 |
| 5 (Very High) | 5 | 10 | 15 | 20 | 25 |
| 4 (High) | 4 | 8 | 12 | 16 | 20 |
| 3 (Moderate) | 3 | 6 | 9 | 12 | 15 |
| 2 (Low) | 2 | 4 | 6 | 8 | 10 |
| 1 (Very Low) | 1 | 2 | 3 | 4 | 5 |

**Risk Levels:**
- **GREEN (1-7):** Acceptable, monitor
- **YELLOW (8-15):** Significant, mitigate
- **RED (16-25):** Critical, immediate action

**Risk Statement Format:**
```
IF [condition/event], THEN [consequence to project objective]
```

**URL:** https://nodis3.gsfc.nasa.gov/displayDir.cfm?t=NPR&c=8000&s=4C

---

### NASA-HDBK-1009A: SE Work Products Handbook

**Full Title:** NASA Systems Engineering Work Products Handbook

**Authority:** Handbook (guidance)

**Current Version:** Revision A (March 2025)

**Key Content:**

Defines standard content and format for SE work products:

| Work Product | Purpose | Key Sections |
|--------------|---------|--------------|
| SEMP | SE Management Plan | Planning, organization, processes |
| ConOps | Concept of Operations | Scenarios, modes, interfaces |
| System Spec | System Requirements | Functional, performance, interface |
| ICD | Interface Control Document | Physical, functional interfaces |
| VCRM | Verification Matrix | Requirements to verification map |
| Test Plan | Verification Planning | Test approach, resources, schedule |
| Risk Register | Risk Management | Risk list, scores, mitigations |

**URL:** https://standards.nasa.gov/

---

## Supporting Standards

### NASA-STD-8739.8: Software Assurance

**Purpose:** Software assurance and safety requirements

**Key Topics:**
- Software classification
- Software safety analysis
- Software verification and validation
- Software configuration management

### NASA-STD-7009A: Models and Simulations

**Purpose:** Standards for M&S credibility

**Key Topics:**
- M&S development process
- Verification, Validation, and Uncertainty Quantification (VVUQ)
- M&S credibility assessment

### NASA SWEHB: Software Engineering Handbook

**Purpose:** Comprehensive software engineering guidance

**Key Sections:**
- 7.9: Entrance and Exit Criteria (review gates)
- Software lifecycle phases
- Software quality assurance

**URL:** https://swehb.nasa.gov/

---

## External Standards (Referenced)

### INCOSE SE Handbook v5.0

**Full Title:** INCOSE Systems Engineering Handbook, Version 5.0

**Authority:** International Council on Systems Engineering (industry standard)

**Alignment:** ISO/IEC/IEEE 15288:2023

**Key Content:**
- SE principles and concepts
- SE processes (aligned with ISO 15288)
- SE methods and tools
- SE application guidance

**Note:** Copyrighted material - reference only, do not reproduce

### ISO/IEC/IEEE 15288:2023

**Full Title:** Systems and software engineering — System life cycle processes

**Authority:** International standard

**Key Content:**
- 30+ system life cycle processes
- Process outcomes and activities
- Tailoring guidance

---

## Quick Reference Matrix

| Standard | Type | Authority | Primary Use |
|----------|------|-----------|-------------|
| NPR 7123.1D | Procedural Req | Mandatory | SE processes, reviews |
| NASA/SP-2016-6105 | Handbook | Guidance | SE implementation |
| NPR 8000.4C | Procedural Req | Mandatory | Risk management |
| NASA-HDBK-1009A | Handbook | Guidance | Work products |
| NASA-STD-8739.8 | Standard | Mandatory | Software assurance |
| NASA-STD-7009A | Standard | Guidance | M&S credibility |
| NASA SWEHB | Handbook | Guidance | Software engineering |
| INCOSE v5.0 | Industry | Guidance | SE best practices |

---

## Citation Guidelines

When referencing NASA standards:

**Format:** [Document ID], Section [X.Y], "[Quote or paraphrase]"

**Examples:**
- NPR 7123.1D, Section 3.2.1, "Technical requirements shall be..."
- NASA/SP-2016-6105 Rev2, Chapter 4, describes the V-model approach
- Per NPR 8000.4C Section 5, risks scoring 16-25 are classified as RED

---

*DISCLAIMER: This summary is AI-generated based on publicly available NASA
documents. It is provided for reference only and may not reflect the most
current versions. Always consult official NASA sources for authoritative
guidance.*
