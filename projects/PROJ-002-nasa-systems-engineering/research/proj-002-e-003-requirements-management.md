# NASA Requirements Management and Traceability Research

> **PS ID:** proj-002
> **Entry ID:** e-003
> **Topic:** NASA Requirements Management and Traceability
> **Date:** 2026-01-09
> **Status:** COMPLETE

---

## L0: Executive Summary

NASA's requirements management framework ensures all stakeholder needs are systematically captured, decomposed into verifiable "shall" statements, allocated to system elements, and traced through verification. The process is governed by **NPR 7123.1D** (Processes 2 and 11), supported by **NASA-HDBK-1009A** for modeling work products, and documented in **NASA/SP-2016-6105 Rev2** (Systems Engineering Handbook). Key artifacts include the **Verification Cross-Reference Matrix (VCRM)** and **bidirectional traceability matrices**. Requirements use the **TADI** verification methods (Test, Analysis, Demonstration, Inspection) and follow the **EARS** (Easy Approach to Requirements Syntax) or INCOSE guidelines for "shall" statement construction.

---

## L1: Structured Overview

### 1. Governing Documents

| Document | Purpose | Primary Focus |
|----------|---------|---------------|
| NPR 7123.1D | NASA Procedural Requirements | Process 2 (Technical Requirements Definition), Process 11 (Requirements Management) |
| NASA-HDBK-1009A | Systems Modeling Handbook | SysML modeling for SE work products |
| NASA/SP-2016-6105 Rev2 | Systems Engineering Handbook | Comprehensive SE guidance |
| INCOSE SE Handbook v5.0 | Industry standard | Requirements analysis and traceability |
| EARS Notation | Requirements syntax | Structured "shall" statement patterns |

### 2. Requirements Lifecycle

```
Stakeholder Expectations
        |
        v
Technical Requirements Definition (Process 2)
        |
        v
Requirements Decomposition & Allocation
        |
        v
Requirements Baselining (SRR)
        |
        v
Requirements Management (Process 11)
        |
        v
Verification (TADI) & Validation
```

### 3. Key Concepts

- **Shall Statements**: Mandatory, verifiable requirements using specific syntax
- **Bidirectional Traceability**: Links requirements upward (to stakeholder needs) and downward (to design/verification)
- **VCRM**: Verification Cross-Reference Matrix linking requirements to verification activities
- **TADI**: Test, Analysis, Demonstration, Inspection verification methods
- **CCB**: Configuration Control Board for change management

### 4. Stakeholders

| Role | Responsibility |
|------|----------------|
| Requirements Engineer | Elicits, writes, and manages requirements |
| Systems Engineer | Ensures requirements decomposition and allocation |
| Verification Engineer | Plans and executes TADI activities |
| Configuration Manager | Maintains baselines and change control |
| CCB Chair | Approves/rejects requirement changes |

---

## L2: Comprehensive Research

### 1. NPR 7123.1D: Technical Requirements Definition (Process 2)

#### 1.1 Purpose and Scope

The Technical Requirements Definition Process transforms stakeholder expectations into measurable technical requirements. Program/Project Managers must identify and implement an Engineering Technical Authority (ETA)-approved process customized for their product layer.

#### 1.2 Key Activities

The process converts baselined stakeholder expectations into "shall" statements that are:
- **Quantitative**: Expressed in measurable terms
- **Measurable**: Can be objectively verified
- **Unique**: Each requirement has a single interpretation
- **Well-formed**: Complete, consistent, individually verifiable

#### 1.3 Process Outputs

| Output | Description |
|--------|-------------|
| Technical Requirements | "Shall" statements derived from stakeholder expectations |
| Measures of Performance (MOPs) | Quantitative measures of system performance |
| Technical Performance Measures (TPMs) | Key technical parameters tracked throughout lifecycle |
| Requirements Documents | SRD (System Requirements Document), PRD (Product Requirements Document), IRD (Interface Requirements Document) |

#### 1.4 Cybersecurity Integration

NPR 7123.1D incorporates cybersecurity requirements derived from NPR 2810.1, ensuring security considerations are embedded in technical requirements from the start.

**Reference:** [NPR 7123.1D Chapter 3](https://nodis3.gsfc.nasa.gov/displayDir.cfm?Internal_ID=N_PR_7123_001D_&page_name=Chapter3)

---

### 2. NPR 7123.1D: Requirements Management (Process 11)

#### 2.1 Purpose and Scope

The Requirements Management Process oversees requirements throughout the system lifecycle. Organizations must establish an ETA-approved process tailored to their specific needs.

#### 2.2 Key Functions

The process performs three essential functions:

1. **Managing Product Requirements**: Identify, control, decompose, and allocate requirements at all WBS levels
2. **Ensuring Bidirectional Traceability**: Link requirements upward to stakeholder needs and downward to design/verification
3. **Controlling Baseline Changes**: Manage modifications through CCB approval throughout the system's lifecycle

#### 2.3 Process Activities

| Activity | Description |
|----------|-------------|
| Organize Requirements | Structure hierarchically from design processes |
| Record Traceability | Document parent-child relationships or mark as "self-derived" |
| Evaluate Changes | Route through CCB for impact assessment |
| Maintain Consistency | Ensure alignment between requirements, ConOps, and design |

#### 2.4 Change Management

Requirements changes require rigorous impact assessment across:
- Cost and schedule
- Interfaces and dependencies
- Higher/lower-level requirements
- Safety and performance

**Key Insight:** "The average project experiences about a twenty-five percent change in requirements after the requirements have been defined for the first system release, which causes at least a twenty-five percent schedule slip."

**Reference:** [NASA 6.2 Requirements Management](https://www.nasa.gov/reference/6-2-requirements-management/)

---

### 3. NASA-HDBK-1009A: Systems Modeling for SE Work Products

#### 3.1 Overview

NASA-HDBK-1009A (approved 2025-03-12) establishes how system modeling using Systems Modeling Language (SysML) integrates with NASA SE processes in NPR 7123.1.

#### 3.2 Work Products Covered

The handbook addresses SE products from these NASA SE Engine processes:

| Process | Work Products |
|---------|---------------|
| Stakeholder Expectation Definition | Stakeholder identification, expectations definition |
| Technical Requirements Definition | ConOps, MOE definition, Technical Requirements |
| Product Verification | MOP, TPM definition, V&V Requirements, Planning, Results |
| Product Validation | Validation requirements and results |

#### 3.3 Key Changes in Revision A (2025)

Expanded scope from baseline (2022-11-14) to include:
- Stakeholder identification and expectations definition
- Measures of Effectiveness (MOE) definition
- Measures of Performance (MOP)
- Technical Performance Measures (TPM)
- V&V Requirements, Planning, and Results

#### 3.4 Companion Model

A companion SysML model built using MagicDraw 2022x is available in NASA Teamwork Cloud, demonstrating metamodel elements and relationships.

**Reference:** [NASA-HDBK-1009A](https://standards.nasa.gov/standard/NASA/NASA-HDBK-1009)

---

### 4. "Shall" Statement Format and Best Practices

#### 4.1 Fundamental Syntax

The basic structure of a NASA requirement:

```
The <system name> shall <system response>.
```

**Key Rules:**
- Use "shall" for mandatory requirements
- Use "should" for goals (non-mandatory)
- Use "will" for statements of fact
- Never use "must," "are," "is," or "was" in requirements

#### 4.2 EARS (Easy Approach to Requirements Syntax)

EARS provides five patterns for structured requirements:

##### Pattern 1: Ubiquitous Requirements (Always Active)
```
The <system name> shall <system response>.
```
**Example:** "The mobile phone shall have a mass of less than 150 grams."

##### Pattern 2: State-Driven Requirements (While)
```
While <precondition(s)>, the <system name> shall <system response>.
```
**Example:** "While there is no card in the ATM, the ATM shall display 'insert card to begin'."

##### Pattern 3: Event-Driven Requirements (When)
```
When <trigger>, the <system name> shall <system response>.
```
**Example:** "When 'mute' is selected, the laptop shall suppress all audio output."

##### Pattern 4: Optional Feature Requirements (Where)
```
Where <feature is included>, the <system name> shall <system response>.
```
**Example:** "Where the car has a sunroof, the car shall have a sunroof control panel on the driver door."

##### Pattern 5: Unwanted Behavior Requirements (If/Then)
```
If <trigger>, then the <system name> shall <system response>.
```
**Example:** "If an invalid credit card number is entered, then the website shall display 'please re-enter credit card details'."

##### Complex Requirements (Combined Patterns)
```
While <precondition>, when <trigger>, the <system name> shall <system response>.
```
**Example:** "While the aircraft is on ground, when reverse thrust is commanded, the engine control system shall enable reverse thrust."

#### 4.3 Quality Characteristics

Good requirements must be:
- **Necessary**: Essential to meet stakeholder needs
- **Verifiable**: Can be verified by examination, analysis, test, or demonstration
- **Attainable**: Technically and economically achievable
- **Unambiguous**: Single interpretation possible
- **Complete**: Contains all necessary information
- **Consistent**: Does not conflict with other requirements
- **Traceable**: Linked to parent requirements and verification activities

#### 4.4 Terms to Avoid

| Avoid | Reason | Alternative |
|-------|--------|-------------|
| "support" (activity) | Vague | Specify concrete action |
| "easy," "user-friendly" | Subjective | Define measurable criteria |
| "minimize," "maximize" | Unbounded | Specify quantitative limits |
| "as applicable" | Ambiguous | Define specific conditions |
| "etc." | Incomplete | Enumerate all items |

**References:**
- [EARS by Alistair Mavin](https://alistairmavin.com/ears/)
- [INCOSE Guide for Writing Requirements](https://www.incose.org/docs/default-source/working-groups/requirements-wg/gtwr/incose_rwg_gtwr_v4_040423_final_drafts.pdf)

---

### 5. Verification Cross-Reference Matrix (VCRM)

#### 5.1 Definition and Purpose

The VCRM is the final output of acceptance testing, providing traceability between product requirements and related test plans and reports. It includes pass/fail status for each requirement.

#### 5.2 VCRM Structure

| Column | Content |
|--------|---------|
| Requirement ID | Unique identifier for each "shall" statement |
| Requirement Text | The "shall" statement being verified |
| Verification Method | TADI (Test, Analysis, Demonstration, Inspection) |
| Verification Level | Component, Subsystem, System, or Integration |
| Test/Analysis Reference | Document ID for verification procedure |
| Verification Status | Pass/Fail/Pending |
| Verification Date | When verification was completed |
| Evidence Location | Reference to test report or analysis |

#### 5.3 VCRM Usage

The VCRM serves multiple purposes:
- **Tracking**: Systems engineering tool for monitoring requirement completion
- **Allocation**: Documents which requirements are verified at which test levels
- **Traceability**: Links requirements to verification activities
- **Status Reporting**: Provides pass/fail summary for reviews

#### 5.4 Important Considerations

- The VCRM alone is insufficient to establish verification program intent
- Development of VCRM is the **last step** in the verification requirements process
- Should categorize requirements by function (mission performance, operational environments, reliability, safety, etc.)
- Document rationale for each requirement flow-down

**Reference:** [NASA Appendix D: Requirements Verification Matrix](https://www.nasa.gov/reference/appendix-d-requirements-verification-matrix/)

---

### 6. Bidirectional Traceability

#### 6.1 Definition

Bidirectional traceability is "the ability to trace any given requirement/expectation to its parent requirement/expectation and to its allocated children requirements/expectations."

#### 6.2 Trace Directions

| Direction | Purpose | Example |
|-----------|---------|---------|
| Upward (Backward) | Verify requirement justification | Component requirement -> System requirement -> Stakeholder need |
| Downward (Forward) | Verify requirement implementation | Stakeholder need -> System requirement -> Design element -> Test procedure |

#### 6.3 NASA Traceability Requirements

**SWE-052:** Bidirectional traceability between higher-level requirements and software requirements

**SWE-059:** Bidirectional traceability between software requirements and software design

**SWE-072:** Bidirectional traceability between software test procedures and software requirements

#### 6.4 Traceability Matrix Best Practices

- Create matrices early in project lifecycle
- Use unique identification systems conveying requirement hierarchy
- Capture requirement sources and parent relationships
- Maintain as electronic documents for easier updates
- Assign clear responsibility for matrix management
- Review at major project phases
- A single requirement may trace to multiple test procedures (and vice versa)

#### 6.5 Benefits

According to NASA's Safety Guidebook, traceability provides:
- Verification that all user needs are implemented and tested
- Confirmation of no "extra" system behaviors outside requirements
- Enhanced understanding of requirement change impacts
- Gap identification for dropped requirements
- Detection of undocumented functionality (scope creep)

**References:**
- [SWE-052 Bidirectional Traceability](https://swehb.nasa.gov/display/7150/SWE-052+-+Bidirectional+Traceability+Between+Higher+Level+Requirements+and+Software+Requirements)
- [SWE-047 Traceability Data](https://swehb.nasa.gov/display/7150/SWE-047+-+Traceability+Data)

---

### 7. Verification Methods: TADI

#### 7.1 Overview

TADI represents the four primary verification methods used in NASA systems engineering:

| Method | Description | When to Use |
|--------|-------------|-------------|
| **T**est | Physical testing measuring actual performance | Hardware/software requiring objective measurement |
| **A**nalysis | Mathematical models, simulations, analytical techniques | When testing is impractical or impossible |
| **D**emonstration | Showing system performs correctly through operation | Functional proof without detailed measurement |
| **I**nspection | Visual examination or review of documentation | Verification through artifact review |

#### 7.2 Method Selection Criteria

| Method | Advantages | Disadvantages |
|--------|-----------|---------------|
| Test | Highest confidence, direct measurement | Expensive, time-consuming |
| Analysis | Cost-effective for complex scenarios | Requires validated models |
| Demonstration | Simple to execute | May not catch subtle failures |
| Inspection | Low cost, quick execution | Limited to observable attributes |

#### 7.3 Verification Planning

- Qualification testing: Worst-case scenarios beyond operational parameters
- Acceptance testing: Within operational range
- Integration testing: Verify interfaces and interactions
- Regression testing: Verify no unintended changes

#### 7.4 Verification Hierarchy

```
Component-Level Verification
        |
        v
Subsystem-Level Verification
        |
        v
System-Level Verification
        |
        v
Integration Verification
        |
        v
Program-Level Verification
```

**Reference:** [NASA Appendix I: V&V Plan Outline](https://www.nasa.gov/reference/appendix-i-verification-and-validation-plan-outline/)

---

### 8. Requirements Decomposition and Flow-Down

#### 8.1 Overview

Logical decomposition utilizes functional analysis to create a system architecture and decompose top-level (parent) requirements, allocating them down to the lowest desired levels.

#### 8.2 Decomposition Hierarchy

```
Presidential Directives / Mission Directorates
        |
        v
Program Requirements
        |
        v
Project Requirements
        |
        v
System Requirements
        |
        v
Segment Requirements
        |
        v
Subsystem Requirements
        |
        v
Component Requirements
```

#### 8.3 Functional Analysis Steps

1. **Translate** top-level requirements into functions
2. **Decompose** and allocate functions to lower WBS levels
3. **Identify** and describe functional and subsystem interfaces

#### 8.4 Types of Technical Requirements

| Type | Description | Example |
|------|-------------|---------|
| Functional | What functions need to be performed | "The system shall transmit telemetry data" |
| Performance | How well the system must perform | "The system shall transmit at 1 Mbps minimum" |
| Interface | What connections must be made | "The system shall interface with ground station via S-band" |
| Environmental | Operating conditions | "The system shall operate in -40C to +85C" |
| Constraint | Design limitations | "The system shall weigh less than 50 kg" |

#### 8.5 Derived Requirements

Requirements that emerge from architecture and design decisions rather than flowing directly from stakeholder needs. These must still trace to parent requirements or be marked as "self-derived" with documented rationale.

#### 8.6 Validation at Each Level

"At each level of decomposition (system, subsystem, component, etc.), the total set of derived requirements must be validated against the stakeholder expectations or higher-level parent requirements before proceeding to the next level of decomposition."

**Reference:** [NASA 4.3 Logical Decomposition](https://www.nasa.gov/reference/4-3-logical-decomposition/)

---

### 9. Requirements Baselining and Change Control

#### 9.1 Baseline Types

NASA controls four distinct baselines representing different product lifecycle phases:

| Baseline | Established At | Content |
|----------|----------------|---------|
| Functional Baseline | System Design Review (SDR) | System performance requirements and verification methods |
| Allocated Baseline | Preliminary Design Review (PDR) | Requirements extended for design initiation |
| Product Baseline | Critical Design Review (CDR) | Production configuration and acceptance testing |
| As-Deployed Baseline | Operational Readiness Review (ORR) | Flight-ready design with incorporated changes |

#### 9.2 Configuration Control Board (CCB)

**Structure:**
- Chair: Person with program/project change authority
- Members: Stakeholder representatives with commitment authority
- Levels: Product CCB, Project CCB, Software Development CCB

**Functions:**
- Review and disposition proposed changes
- Assess impact on cost, schedule, interfaces, safety
- Approve/reject changes through formal voting
- Maintain baseline integrity

#### 9.3 Change Classification

| Type | Description | Authority |
|------|-------------|-----------|
| Major | Significant impact requiring retrofit or affecting specifications | Higher-level CCB |
| Minor | No impact on product interchangeability | Lower-level CCB |
| Waiver | Intentional release from specific requirements | Appropriate CCB |

#### 9.4 Change Management Process

1. **Document** change request with minimum data set
2. **Analyze** impact across cost, schedule, technical, safety
3. **Route** through appropriate CCB level
4. **Review** and assess by CCB members
5. **Approve/Reject** by CCB chair
6. **Implement** approved changes
7. **Verify** implementation correctness
8. **Update** all affected documentation

#### 9.5 Lessons Learned

NASA's Lewis spacecraft failure investigation identified "requirement changes without adequate resource adjustment" as a contributing factor, emphasizing the need for realistic planning when changes are approved.

**References:**
- [NASA 6.5 Configuration Management](https://www.nasa.gov/reference/6-5-configuration-management/)
- [SWE-053 Manage Requirements Changes](https://swehb.nasa.gov/display/7150/SWE-053+-+Manage+Requirements+Changes)
- [NASA-STD-0005 Configuration Management Standard](https://standards.nasa.gov/standard/NASA/NASA-STD-0005)

---

### 10. NASA DOORS Usage Patterns

#### 10.1 Overview

While NASA does not mandate specific tools, IBM DOORS (Dynamic Object-Oriented Requirements System) is commonly used for requirements management across NASA programs.

#### 10.2 Common Usage Patterns

| Pattern | Description |
|---------|-------------|
| Hierarchical Modules | Separate modules for each requirements level (L0, L1, L2, etc.) |
| Link Modules | Dedicated modules for traceability relationships |
| Attribute-Based Filtering | Custom attributes for status, verification method, owner |
| Baseline Comparison | Version comparison for change tracking |
| Views and Reports | Custom views for different stakeholder needs |

#### 10.3 Alternative Approaches

For small projects, NASA guidance acknowledges:
- Spreadsheets (Excel)
- Databases
- Document-based approaches
- Requirements management tools like JAMA, Polarion, Helix RM

The key requirement is maintaining electronic traceability data regardless of tool choice.

#### 10.4 NASA SBIR: Tracer Tool

NASA has funded development of the "Tracer" tool through SBIR, enabling:
- Bidirectional impact identification for requirement changes
- Integration with modern version control systems
- Support for AI-based systems requirements tracing

**Reference:** [NASA SBIR A2.02-4092](https://sbir.gsfc.nasa.gov/SBIR/abstracts/18/sbir/phase2/SBIR-18-2-A2.02-4092.html)

---

### 11. INCOSE Best Practices Integration

#### 11.1 INCOSE Systems Engineering Handbook v5.0

Published 2023, the INCOSE SE Handbook describes state-of-the-good-practice for systems engineering, including:
- Elaboration on ISO/IEC/IEEE 15288:2023 processes
- Requirements analysis ensuring "correct, complete, consistent, traceable, understandable, appropriate to level, verifiable/measurable, and feasible"
- System requirements traceable to mission/business and stakeholder requirements

#### 11.2 INCOSE Guide for Writing Requirements (v4.0)

41 rules for requirements quality, covering:
- Singular (one requirement per statement)
- Complete (necessary and sufficient)
- Consistent (no conflicts)
- Correct (accurate representation of need)
- Traceable (linked to source)
- Unambiguous (single interpretation)
- Verifiable (objective evidence possible)

#### 11.3 EARS Integration with INCOSE

EARS combined with INCOSE rules helps organizations produce high-quality, traceable, and testable requirements that:
- Improve communication among stakeholders
- Reduce project risks
- Enable consistent requirement structure
- Support non-native English speakers

**Reference:** [INCOSE Requirements Working Group](https://www.incose.org/communities/working-groups-initiatives/requirements)

---

## Application to Jerry Framework

### nse-requirements Agent Design

Based on this research, the `nse-requirements` agent should implement:

1. **Requirement Elicitation Interface**
   - Structured questions following 5W1H
   - Stakeholder identification
   - ConOps development support

2. **Shall Statement Generator**
   - EARS pattern templates
   - Quality validation against INCOSE rules
   - Automatic uniqueness checking

3. **Traceability Engine**
   - Bidirectional link management
   - Parent-child relationship tracking
   - Orphan detection

4. **VCRM Generator**
   - TADI method assignment
   - Verification level allocation
   - Status tracking

5. **Change Management**
   - Impact analysis support
   - CCB workflow integration
   - Baseline comparison

---

## References

### Primary Sources

1. **NPR 7123.1D** - NASA Systems Engineering Processes and Requirements
   - [Chapter 3](https://nodis3.gsfc.nasa.gov/displayDir.cfm?Internal_ID=N_PR_7123_001D_&page_name=Chapter3)

2. **NASA-HDBK-1009A** - NASA Systems Modeling Handbook for Systems Engineering
   - [NASA Standards](https://standards.nasa.gov/standard/NASA/NASA-HDBK-1009)
   - [PDF (2025-03-12)](https://standards.nasa.gov/system/files/tmp/2025-03-12-NASA-HDBK-1009A.pdf)

3. **NASA/SP-2016-6105 Rev2** - NASA Systems Engineering Handbook
   - [NASA Reference](https://www.nasa.gov/reference/systems-engineering-handbook/)
   - [PDF](https://www.nasa.gov/wp-content/uploads/2018/09/nasa_systems_engineering_handbook_0.pdf)
   - [NTRS](https://ntrs.nasa.gov/citations/20170001761)

4. **INCOSE SE Handbook v5.0** - Systems Engineering Handbook: A Guide for System Life Cycle Processes and Activities
   - [SEBoK Wiki](https://sebokwiki.org/wiki/INCOSE_Systems_Engineering_Handbook)
   - [Jama Software Overview](https://www.jamasoftware.com/blog/empowering-engineers-exploring-incose-systems-engineering-handbook-v5/)

5. **EARS Notation** - Easy Approach to Requirements Syntax
   - [Alistair Mavin EARS](https://alistairmavin.com/ears/)
   - [IEEE RE09 Paper](https://ieeexplore.ieee.org/document/5328509/)

### Secondary Sources

6. **NASA Software Engineering Handbook**
   - [SWE-047 Traceability Data](https://swehb.nasa.gov/display/7150/SWE-047+-+Traceability+Data)
   - [SWE-052 Bidirectional Traceability](https://swehb.nasa.gov/display/7150/SWE-052+-+Bidirectional+Traceability+Between+Higher+Level+Requirements+and+Software+Requirements)
   - [SWE-053 Manage Requirements Changes](https://swehb.nasa.gov/display/7150/SWE-053+-+Manage+Requirements+Changes)
   - [SWE-059 Requirements to Design Traceability](https://swehb.nasa.gov/display/7150/SWE-059+-+Bidirectional+Traceability+Between+Software+Requirements+and+Software+Design)
   - [SWE-072 Test to Requirements Traceability](https://swehb.nasa.gov/display/7150/SWE-072+-+Bidirectional+Traceability+Between+Software+Test+Procedures+and+Software+Requirements)

7. **NASA Technical References**
   - [6.2 Requirements Management](https://www.nasa.gov/reference/6-2-requirements-management/)
   - [6.5 Configuration Management](https://www.nasa.gov/reference/6-5-configuration-management/)
   - [4.3 Logical Decomposition](https://www.nasa.gov/reference/4-3-logical-decomposition/)
   - [Appendix D: Requirements Verification Matrix](https://www.nasa.gov/reference/appendix-d-requirements-verification-matrix/)
   - [Appendix I: V&V Plan Outline](https://www.nasa.gov/reference/appendix-i-verification-and-validation-plan-outline/)

8. **NASA Standards**
   - [NASA-STD-0005 Configuration Management Standard](https://standards.nasa.gov/standard/NASA/NASA-STD-0005)

9. **INCOSE Resources**
   - [INCOSE Requirements Working Group](https://www.incose.org/communities/working-groups-initiatives/requirements)
   - [Guide for Writing Requirements](https://www.incose.org/docs/default-source/working-groups/requirements-wg/gtwr/incose_rwg_gtwr_v4_040423_final_drafts.pdf)

10. **Academic/Industry Sources**
    - [MIT Requirements Flow Down](https://dspace.mit.edu/bitstream/handle/1721.1/103819/16-842-fall-2009/contents/lecture-notes/MIT16_842F09_lec03.pdf)
    - [FAA Requirements Engineering Report](https://www.faa.gov/sites/faa.gov/files/aircraft/air_cert/design_approvals/air_software/AR-08-34.pdf)

---

*Research compiled by ps-researcher agent for PROJ-002-nasa-systems-engineering*
*Last Updated: 2026-01-09*
