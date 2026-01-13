# PROJ-002-E-005: NASA SE Document Templates and Standards

> **PS Context:** proj-002 | **Entry ID:** e-005
> **Research Topic:** NASA Systems Engineering Documentation Standards and Templates
> **Date:** 2026-01-09
> **Researcher:** ps-researcher (NASA SE Research Specialist)

---

## Executive Summary

This research artifact documents NASA's comprehensive systems engineering documentation standards and templates. NASA maintains a rigorous documentation framework that supports the entire system lifecycle, from concept through disposal. Key documents include the Systems Engineering Management Plan (SEMP), Concept of Operations (ConOps), System Requirements Document (SRD), Interface Control Document (ICD), and Verification & Validation Plan. These templates are governed by NPR 7123.1D (SE Processes and Requirements) and detailed in NASA/SP-2016-6105 Rev2 (SE Handbook).

---

## L0: Quick Reference (Executive Level)

### Key Document Types at Each Review Gate

| Review Gate | Required Documents |
|-------------|-------------------|
| **MCR** (Mission Concept Review) | ConOps (initial), Mission Needs Statement, Stakeholder Expectations |
| **SRR** (System Requirements Review) | SRD, ConOps (updated), Risk Management Plan, SEMP (draft) |
| **PDR** (Preliminary Design Review) | Preliminary Design Package, ICDs, V&V Plan (draft), Trade Study Reports |
| **CDR** (Critical Design Review) | Detailed Design Package, Updated ICDs, Test Plans, Safety Analysis |
| **SIR** (System Integration Review) | Integration Plans, Test Procedures, Configuration Audit Results |
| **FRR** (Flight Readiness Review) | Certification of Flight Readiness, Verification Closure Notices |

### Document Numbering Convention

NASA uses a hierarchical document identification system:
- **NASA-STD-XXXX**: Technical Standards (Agency-wide)
- **NASA-SPEC-XXXX**: Technical Specifications
- **NASA-HDBK-XXXX**: Handbooks (guidance)
- **NPR XXXX.XX**: NASA Procedural Requirements
- **NASA/SP-XXXX-XXXX**: Special Publications

### Primary Sources

| Document | Purpose |
|----------|---------|
| [NASA/SP-2016-6105 Rev2](https://ntrs.nasa.gov/citations/20170001761) | SE Handbook (primary guidance) |
| [NPR 7123.1D](https://nodis3.gsfc.nasa.gov/displayDir.cfm?t=NPR&c=7123&s=1D) | SE Processes & Requirements |
| [NASA-HDBK-1009A](https://standards.nasa.gov/standard/NASA/NASA-HDBK-1009) | Systems Modeling Handbook (MBSE) |
| [NASA-STD-7009A](https://standards.nasa.gov/standard/NASA/NASA-STD-7009) | Standard for Models and Simulations |

---

## L1: Detailed Reference (Technical Lead Level)

### 1. Systems Engineering Management Plan (SEMP)

**Purpose:** The SEMP is the foundational technical planning document that establishes the technical content of engineering work and represents the agreed-to tailoring of NPR 7123.1 requirements.

**Source:** [Appendix J: SEMP Content Outline](https://www.nasa.gov/reference/appendix-j-semp-content-outline/) | NPR 7123.1D Chapter 6

#### SEMP Structure

```
1.0 Purpose and Scope
    - Document intent, scope, organization

2.0 Applicable Documents
    - Standards, procedures, project-specific requirements

3.0 Technical Summary
    3.1 System Description
    3.2 System Structure
    3.3 Product Integration
    3.4 Planning Context
    3.5 Boundary of Technical Effort
    3.6 Cross References

4.0 Technical Effort Integration
    4.1 Responsibility and Authority
    4.2 Contractor Integration
    4.3 Analytical Tools Supporting Integration

5.0 Common Technical Processes Implementation
    - Tailored approaches for 17 common technical processes

6.0 Technology Insertion
    - Identification, assessment, insertion of new technologies

7.0 Additional SE Functions and Activities
    7.1 System Safety
    7.2 Engineering Methods and Tools
    7.3 Specialty Engineering
    7.4 Technical Performance Measures
    7.5 Heritage
    7.6 Other

8.0 Integration with Project Plan
    - Resource allocation coordination

9.0 Compliance Matrices
    - NPR 7123.1 compliance demonstration
```

**Key Characteristics:**
- Living document updated throughout lifecycle
- Contains compliance matrix (Appendix H.2 basis)
- Includes appendices for glossary, charts, technical plan summaries

---

### 2. Concept of Operations (ConOps)

**Purpose:** A communication tool that defines operational needs and expectations between stakeholders, capturing expected capabilities, behaviors, and operations of the envisioned system.

**Source:** [Appendix S: ConOps Annotated Outline](https://www.nasa.gov/reference/appendix-s-concept-of-operations-annotated-outline/)

#### ConOps Structure

```
1.0 Introduction
    1.1 Project Description
        1.1.1 Background
        1.1.2 Assumptions and Constraints
    1.2 Overview of the Envisioned System
        1.2.1 Overview
        1.2.2 System Scope

2.0 Documents
    2.1 Applicable Documents
    2.2 Reference Documents

3.0 Description of Envisioned System
    3.1 Needs, Goals and Objectives
    3.2 Overview of System and Key Elements
    3.3 Interfaces
    3.4 Modes of Operations
    3.5 Proposed Capabilities

4.0 Physical Environment
    - Development, integration, testing, operations environments

5.0 Support Environment
    - Maintenance, repair, sparing philosophy, upgrades

6.0 Operational Scenarios, Use Cases and Design Reference Missions
    6.1 Nominal Conditions
    6.2 Off-Nominal Conditions

7.0 Impact Considerations
    7.1 Environmental Impacts
    7.2 Organizational Impacts
    7.3 Scientific/Technical Impacts

8.0 Risks and Potential Issues
    - Development, operational, disposal risks

Appendix A: Acronyms
Appendix B: Glossary of Terms
```

---

### 3. System Requirements Document (SRD)

**Purpose:** Captures top-level functional and performance descriptions and defines interfaces necessary for integration.

**Source:** NASA DID-P200 | [NASA Software Documentation Standard](https://standards.nasa.gov/standard/NASA/NASA-STD-2100)

#### SRD Structure (NASA DID-P200)

```
Section 1: Introduction
    - Context and document position within project documentation

Section 2: Requirements Analysis Method
    - Methods used to establish and analyze requirements

Section 3: External Interfaces
    - External interface specifications

Section 4: Technical Requirements
    - Functional requirements
    - Required states and modes
    - External interface requirements
    - Internal interface requirements
    - Internal data requirements
    - Adaptation requirements
    - Safety requirements
    - Performance and timing requirements
    - Security and privacy requirements
    - Environment requirements
    - Computer hardware resource requirements
    - Computer software requirements
    - Computer communications requirements
    - Software quality characteristics
    - Design and implementation constraints
    - Packaging requirements
    - Precedence and criticality of requirements

Section 5: Traceability
    - Trace each requirement to source

Section 6: Phased Delivery Identification
    - Requirements per delivery phase

Sections 7-10: Appendices
    - Acronyms, terms, notes
```

**Requirement Format:**
- Requirement Number
- Requirement Title
- Requirement Text (using "shall" statements)
- Rationale (why requirement is needed)
- Verification Method

---

### 4. Interface Control Document (ICD)

**Purpose:** Specifies interface requirements to be met by participating systems, defines message structures, protocols, and data communication paths.

**Source:** [Appendix L: IRD Outline](https://www.nasa.gov/reference/appendix-l-interface-requirements-document-outline) | [Section 6.3: Interface Management](https://www.nasa.gov/reference/6-3-interface-management/)

#### ICD Structure

```
1.0 Introduction
    1.1 Purpose and Scope
    1.2 Precedence
    1.3 Responsibility and Change Authority

2.0 Documents
    2.1 Applicable Documents
    2.2 Reference Documents

3.0 Interfaces
    3.1 General
        3.1.1 Interface Description
        3.1.2 Interface Responsibilities
        3.1.3 Coordinate Systems
        3.1.4 Engineering Units, Tolerances, and Conversion

    3.2 Interface Requirements
        3.2.1 Mass Properties
        3.2.2 Structural/Mechanical
        3.2.3 Fluid
        3.2.4 Electrical (Power)
        3.2.5 Electronic (Signal)
        3.2.6 Software and Data
        3.2.7 Environments
        3.2.8 Other Unique Requirements

4.0 Qualification Methods
    - Demonstration
    - Test

5.0 Notes
6.0 Appendices

Signature Page (Required)
    - Minimum: managers from both interfacing systems
```

**Interface Documentation Hierarchy:**
1. **Interface Requirements Document (IRD)** - Captures interface needs
2. **Interface Control Document/Drawing (ICD)** - Maintains approved specifications
3. **Interface Definition Document (IDD)** - Defines interface details
4. **Interface Control Plan (ICP)** - Establishes management procedures

---

### 5. Verification and Validation Plan

**Purpose:** Identifies activities establishing compliance with requirements (verification) and establishing that the system meets customer expectations (validation).

**Source:** [Appendix I: V&V Plan Outline](https://www.nasa.gov/reference/appendix-i-verification-and-validation-plan-outline/)

#### V&V Plan Structure

```
1.0 Introduction
    1.1 Purpose and Scope
    1.2 Responsibility and Change Authority
    1.3 Definitions

2.0 Applicable and Reference Documents
    2.1 Applicable Documents
    2.2 Reference Documents
    2.3 Order of Precedence

3.0 System Description
    3.1 System Requirements Flowdown
    3.2 System Architecture
    3.3 End Item Architectures
    3.4 Ground Support Equipment
    3.5 Other Architecture Descriptions

4.0 Verification and Validation Process
    4.1 Management Responsibilities
    4.2 Verification Methods (AIDT)
        - Analysis
        - Inspection
        - Demonstration
        - Test
    4.3 Validation Methods
    4.4 Certification Process
    4.5 Acceptance Testing

5.0 V&V Implementation
    5.1 Design and V&V Flow
    5.2 Test Articles
    5.3 Support Equipment
    5.4 Facilities

6.0 End Item Verification and Validation
    - Per-item sections with developmental evaluations, verification, validation

7.0 System Verification and Validation
    7.1 End-Item Integration
    7.2 Complete System Integration

8.0 Program Verification and Validation
    8.1 Vehicle Integration
    8.2 End-to-End Integration
    8.3 On-Orbit V&V Activities

9.0 System Certification Products

Appendices
    A: Acronyms
    B: Definitions
    C: Requirements Verification Matrix
    D: Validation Matrix
```

#### Requirements Verification Matrix (Appendix D)

| Unique ID | Requirement Text | Source Doc | Verification Method | Status |
|-----------|------------------|------------|---------------------|--------|
| SYS-REQ-001 | "shall" statement | SRD v1.2 | Test | Verified |

**Note:** Only "shall" requirements are included in verification matrices.

---

### 6. Technical Performance Measures (TPM) Documentation

**Purpose:** Track critical technical parameters by comparing current actual achievement to anticipated values.

**Source:** [Section 6.7: Technical Assessment](https://www.nasa.gov/reference/6-7-technical-assessment/) | [NASA Common Leading Indicators](https://nodis3.gsfc.nasa.gov/OCE_docs/OCE_52.pdf)

#### TPM Attributes

| Attribute | Description |
|-----------|-------------|
| Achieved to Date | Current measured value |
| Current Estimate | Projected final value |
| Milestone | Target date |
| Planned Value | Baseline target |
| Planned Profile | Expected progression curve |
| Tolerance Band | Acceptable variance range |
| Threshold | Minimum acceptable value |
| Variance | Difference from plan |

#### TPM Reporting Best Practices

1. Maintain agreed-upon set of well-defined measures
2. Report in consistent format at all project levels
3. Maintain historical data for trend identification
4. Use color-coded (R/Y/G) alert zones
5. Display margins graphically (especially mass/power)

#### Example TPMs

- Vacuum/sea level specific impulse (Isp)
- Weight/mass margins
- Reliability (failure rate)
- Schedule variance
- Operability (turn-around time)
- Bandwidth
- Pointing accuracy
- Memory usage

---

### 7. Trade Study Report Format

**Purpose:** Document decision analysis for selecting among alternatives.

**Source:** [Survey of Trade Study Methods](https://www.nasa.gov/wp-content/uploads/2016/10/survey_of_trade_study_methods_-_baker.pdf) | [DOE Decision-Making Guidebook](https://extapps.ksc.nasa.gov/Reliability/Documents/Decision_Making_Guidebook_2002_Dept_of_Energy.pdf)

#### Trade Study Report Structure

```
1.0 Introduction/Purpose
    - Scope and objectives of the trade study

2.0 Requirements & Constraints
    - Driving requirements
    - External constraints

3.0 Alternatives Identification
    - Candidate solutions/options

4.0 Evaluation Criteria
    - Technical performance
    - Cost
    - Schedule
    - Risk
    - Reliability
    - Maintainability

5.0 Weighting Factors
    - Relative importance of criteria
    - Methodology (AHP, Pairwise, Linear)

6.0 Analysis & Scoring
    - Pugh matrices
    - Weighted scoring matrices
    - Analytic Hierarchy Process (AHP)

7.0 Sensitivity Analysis
    - Robustness testing

8.0 Recommendations
    - Preferred alternative with rationale

9.0 References & Supporting Data
```

#### Decision Analysis Methods

| Method | Description | Use Case |
|--------|-------------|----------|
| **Pugh Matrix** | Baseline comparison | Quick screening |
| **AHP** | Pairwise criteria comparison | Complex decisions |
| **Kepner-Tregoe** | Systematic evaluation | Risk-focused |
| **Weighted Scoring** | Direct weight assignment | Well-understood criteria |

---

### 8. Configuration Management Documentation

**Purpose:** Control baselines, process changes, track configuration items, conduct audits.

**Source:** [NASA-STD-0005](https://standards.nasa.gov/sites/default/files/standards/NASA/Baseline/0/nasa_std_0005_inactive_for_new_design_2015_03_09.pdf) | NPR 7120.5F

#### Baseline Types

| Baseline | Description | Timing |
|----------|-------------|--------|
| **Functional Baseline** | System-level requirements | SRR |
| **Allocated Baseline** | Subsystem requirements allocation | PDR |
| **Development Baseline** | Design control between allocated and product | Development |
| **Product Baseline** | Verified design documentation | CDR/Production |

#### Configuration Management Plan (CMP) Requirements

1. Configuration Identification procedures
2. Configuration Control processes (CCB)
3. Configuration Status Accounting
4. Configuration Verification and Audit
5. Baseline management
6. Document and data management
7. Interface control
8. Engineering Release System procedures

---

### 9. NASA-STD-7009A: Models and Simulations Documentation

**Purpose:** Establish uniform practices in M&S design, development, and use.

**Source:** [NASA-STD-7009A](https://standards.nasa.gov/standard/NASA/NASA-STD-7009) | [NASA-HDBK-7009A](https://standards.nasa.gov/standard/NASA/NASA-HDBK-7009)

#### M&S Documentation Requirements

| Requirement | Description |
|-------------|-------------|
| CM System | Maintain models and documentation in controlled CM |
| Computational Models | Document which models used (including revision) |
| Version Control | Document versions of M&S results |
| Input Data | Document data used as input, including pedigree |
| Computational Requirements | Document unique requirements (support software, hardware) |
| Verification | Document verification techniques and domain |
| Validation | Document validation techniques, experimental design, domain |

#### Credibility Assessment

NASA-STD-7009 defines credibility assessment products including:
- Development phase assessments
- Use phase assessments
- Risk categorization (Critical, Important, Routine)

---

### 10. MagicDraw/Cameo MBSE Integration

**Purpose:** Generate SE documentation from SysML models.

**Source:** [NASA-HDBK-1009A](https://standards.nasa.gov/standard/NASA/NASA-HDBK-1009) | [NASA NTRS MAV MBSE Paper](https://ntrs.nasa.gov/api/citations/20210026244/downloads/MAV%20MBSE%20IEEE%20Aerospace%20Conference%20March%202022%20Paper%20V4%20-%20Final%20Submission.pdf)

#### Model-to-Document Generation

NASA uses MagicDraw/Cameo Systems Modeler for MBSE with document generation via:
- **VTL scripts** in Report Wizard
- **Standard templates** using Word document bases
- **Diagram extraction** from SysML models

**Companion Model:** NASA-HDBK-1009A includes a companion MagicDraw model file (.mdzip) demonstrating the metamodel and SysML implementation.

#### Key MBSE Documentation Outputs

- ConOps Report
- Requirements Specifications
- V&V Plans
- System Architecture Views (SV-1, SV-4, etc.)
- Behavioral Diagrams (Activity, Sequence, State Machine)

---

### 11. Lessons Learned Integration

**Purpose:** Capture and apply knowledge from past projects.

**Source:** [NASA LLIS](https://llis.nasa.gov/) | NPR 7120.6

#### LLIS Integration Requirements

1. Content must be discoverable/searchable across Agency
2. Submissions undergo vetting and quality review
3. Integration with NEN (NASA Engineering Network)
4. Application through process updates, checklists, handbooks, policy

#### Lesson Learned Lifecycle

1. **Capture** - Document experience
2. **Review** - HDM (Handbook Data Manager) validation
3. **Curate** - Quality assurance, grammar, documentation
4. **Apply** - Infuse into NASA practice
5. **Close** - Transfer to corrective action tracking

---

## L2: Implementation Detail (Practitioner Level)

### Document Templates Quick Reference

#### Template Location Map

| Document | NASA SE Handbook Appendix | NPR Reference |
|----------|---------------------------|---------------|
| SEMP | Appendix J | NPR 7123.1D Ch. 6, App. D |
| ConOps | Appendix S | NPR 7123.1D |
| V&V Plan | Appendix I | NPR 7123.1D |
| IRD/ICD | Appendix L | NPR 7123.1D |
| RVM | Appendix D | NPR 7123.1D |
| Validation Matrix | Appendix E | NPR 7123.1D |

### Technical Review Gate Documentation Requirements

#### System Requirements Review (SRR)

**Entrance Criteria:**
- Mission concept approved
- Initial system requirements documented
- ConOps (initial) complete
- SEMP (draft) prepared

**Required Documents:**
- System Requirements Document (SRD)
- Concept of Operations (ConOps)
- Risk Management Plan
- SEMP (draft)
- Requirements Traceability Matrix
- Technical Resource Budget Estimates

**Success Criteria:**
- Requirements traceable to mission objectives
- Risks identified and categorized
- Technical approach feasible
- Cost/schedule estimates reasonable

---

#### Preliminary Design Review (PDR)

**Entrance Criteria:**
- SRR actions closed
- Preliminary design documentation ready
- Trade studies completed

**Required Documents:**
- Preliminary Design Package
- Interface Control Documents (draft)
- V&V Plan (draft)
- Trade Study Reports
- Updated Risk Register
- Updated SEMP
- Technical Performance Measures baseline

**Success Criteria:**
- Design approach sound
- Interfaces defined
- Schedule/cost realistic
- V&V approach viable

---

#### Critical Design Review (CDR)

**Entrance Criteria:**
- PDR actions closed
- Detailed design complete
- Prototype/breadboard testing complete

**Required Documents:**
- Detailed Design Package
- Updated ICDs (baselined)
- Test Plans
- Safety Analysis
- Failure Modes and Effects Analysis (FMEA)
- Updated V&V Plan
- Manufacturing Plans
- Configuration Management Plan

**Success Criteria:**
- Design mature for fabrication
- All interfaces baselined
- Test plans complete
- Safety hazards mitigated

---

### Version Control Conventions

#### Document Revision Tracking

```
[Document Number]-[Version].[Revision]

Examples:
- NASA-STD-7009A (Version A, no revision)
- KSC-DF-107 Rev F (Version baseline, Revision F)
- NPR 7123.1D (Version D)
```

#### Change Documentation

- **Corrected Copy**: Same number + "(Corrected Copy)"
- **Errata**: Original number + date of correction
- **Revision**: New letter/number designation

#### File Naming (MISR Example)

```
[Product]_[Version]nnnn_F[Format]nn

Where:
- nnnn = 4-digit version number
- F = format indicator
- nn = 2-digit format version
```

---

### Jerry Framework Integration Recommendations

Based on this research, the following document templates should be implemented in the nse-* agents:

1. **nse-requirements**: SRD template with requirement format and traceability
2. **nse-design**: Design document templates aligned with PDR/CDR
3. **nse-verification**: V&V Plan template with verification matrices
4. **nse-interfaces**: ICD template with interface categories
5. **nse-conops**: ConOps template following Appendix S
6. **nse-tradeoff**: Trade study template with scoring matrices
7. **nse-tpm**: TPM tracking template with R/Y/G indicators

**Skill Output Requirements:**
- All documents should use "shall" statements for requirements
- Include traceability sections
- Support export to standard formats (Markdown, Word, PDF)
- Integrate with MBSE model elements where applicable

---

## Sources

### Primary NASA Documents

- [NASA/SP-2016-6105 Rev2 - Systems Engineering Handbook](https://ntrs.nasa.gov/citations/20170001761)
- [NPR 7123.1D - Systems Engineering Processes and Requirements](https://nodis3.gsfc.nasa.gov/displayDir.cfm?t=NPR&c=7123&s=1D)
- [NASA-HDBK-1009A - Systems Modeling Handbook](https://standards.nasa.gov/standard/NASA/NASA-HDBK-1009)
- [NASA-STD-7009A - Standard for Models and Simulations](https://standards.nasa.gov/standard/NASA/NASA-STD-7009)
- [NASA-STD-0005 - Configuration Management Standard](https://standards.nasa.gov/sites/default/files/standards/NASA/Baseline/0/nasa_std_0005_inactive_for_new_design_2015_03_09.pdf)
- [KSC-DF-107 - Technical Documentation Style Guide](https://standards.nasa.gov/standard/KSC/KSC-DF-107)

### SE Handbook Appendices

- [Appendix D - Requirements Verification Matrix](https://www.nasa.gov/reference/appendix-d-requirements-verification-matrix/)
- [Appendix E - Validation Plan with Validation Requirements Matrix](https://www.nasa.gov/reference/appendix-e-creating-the-validation-plan-with-a-validation-requirements-matrix/)
- [Appendix I - V&V Plan Outline](https://www.nasa.gov/reference/appendix-i-verification-and-validation-plan-outline/)
- [Appendix J - SEMP Content Outline](https://www.nasa.gov/reference/appendix-j-semp-content-outline/)
- [Appendix L - Interface Requirements Document Outline](https://www.nasa.gov/reference/appendix-l-interface-requirements-document-outline/)
- [Appendix S - ConOps Annotated Outline](https://www.nasa.gov/reference/appendix-s-concept-of-operations-annotated-outline/)

### Supporting Resources

- [NASA Technical Standards System](https://standards.nasa.gov/)
- [NASA Lessons Learned Information System (LLIS)](https://llis.nasa.gov/)
- [Survey of Trade Study Methods](https://www.nasa.gov/wp-content/uploads/2016/10/survey_of_trade_study_methods_-_baker.pdf)
- [DOE Decision-Making Guidebook](https://extapps.ksc.nasa.gov/Reliability/Documents/Decision_Making_Guidebook_2002_Dept_of_Energy.pdf)
- [INCOSE SE Handbook v5](https://www.incose.org/publications/products/se-handbook-v4)

### Technical Reports

- [MBSE Applications for MSR MAV](https://ntrs.nasa.gov/api/citations/20210026244/downloads/MAV%20MBSE%20IEEE%20Aerospace%20Conference%20March%202022%20Paper%20V4%20-%20Final%20Submission.pdf)
- [NASA/SP-2016-6105-SUPPL - Expanded Guidance](https://ntrs.nasa.gov/api/citations/20170007238/downloads/20170007238.pdf)

---

*Document ID: PROJ-002-E-005*
*Version: 1.0*
*Last Updated: 2026-01-09*
