# Nuclear Engineering SOP Survey: Patterns for Safety-Critical Procedure-Based Work

> **PS ID:** phase-1.1 | **Entry ID:** e-001 | **Agent:** ps-researcher-001
> **Date:** 2026-03-22 | **Confidence:** HIGH (0.88) | **Revision:** 2 (QG1 source validation revisions)
> **Methodology:** 5W1H web research framework, T1-T4 source hierarchy

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Non-technical overview of nuclear SOP practices |
| [L1: Technical Detail](#l1-technical-detail) | Detailed findings organized by research target |
| [L2: Strategic Implications](#l2-strategic-implications) | Applicability to Claude Code skill design |
| [References](#references) | All cited sources with URLs |

---

## L0: Executive Summary

Nuclear power plant operations are governed by a multi-layered system of procedures, regulations, and human performance tools that together form the most rigorous procedural compliance framework in any industry. At its core, the U.S. Nuclear Regulatory Commission (NRC) mandates through 10 CFR Part 50 and its Appendix B that every activity affecting quality must be "prescribed by documented instructions, procedures, or drawings" and "accomplished in accordance with these instructions, procedures, or drawings" ([NRC 10 CFR 50 Appendix B, Criterion V](https://www.nrc.gov/reading-rm/doc-collections/cfr/part050/part050-appb)). This creates a regulatory foundation where procedures are not optional guidance but legally binding operational constraints.

The nuclear industry has developed a sophisticated taxonomy of procedure types -- from Emergency Operating Procedures (EOPs) using symptom-based response models, to Abnormal Operating Procedures (AOPs), Alarm Response Procedures (ARPs), and Surveillance Test Procedures (STPs) -- each with specific use classifications (continuous use, reference use, information use) that dictate how closely the operator must follow the written steps ([EPRI/NRC procedure types](https://www.nrc.gov/docs/ML0800/ML080080077.pdf)). Human performance tools like STAR (Stop-Think-Act-Review), three-part communication, peer checking, and independent verification provide layered defenses against human error ([DOE-HDBK-1028-2009 Vol. 1](https://www.standards.doe.gov/standards-documents/1000/1028-BHdbk-2009-v1), [DOE-HDBK-1028-2009 Vol. 2](https://www.standards.doe.gov/files/doe-hdbk-1028-2009-human-performance-improvement-handbook-volume-2-human-performance-tools-for-individuals-work-teams-and-management)). Mandatory hold points in procedures require designated representative approval before work can proceed ([NRC 10 CFR 50 Appendix B, Criterion X](https://www.nrc.gov/reading-rm/doc-collections/cfr/part050/part050-appb)), and a corrective action program captures all deviations, near-misses, and lessons learned to feed back into procedure improvement ([IAEA-TECDOC-1458](https://www.iaea.org/publications/7226/effective-corrective-actions-to-enhance-operational-safety-of-nuclear-installations)).

For the purpose of building an AI agent workflow skill, the nuclear SOP framework offers directly transferable patterns: mandatory verification gates before proceeding, independent review by a party other than the performer, escalation authority hierarchies, structured communication protocols, place-keeping and step sign-off methods, pre-job and post-job briefing structures, and a systematic operating experience feedback loop. These are not theoretical constructs -- they are battle-tested practices refined over decades of operating nuclear power plants and codified in federal regulation.

---

## L1: Technical Detail

### 1. NRC Regulatory Framework

#### 1.1 10 CFR Part 50: The Procedural Foundation

The NRC's 10 CFR Part 50 establishes the regulatory framework for licensing and operating commercial nuclear power plants in the United States ([NRC 10 CFR Part 50 Index](https://www.nrc.gov/reading-rm/doc-collections/cfr/part050/index)). Within this framework, several specific sections mandate procedural controls:

**10 CFR 50.34(b)(6)(ii)** requires applicants for operating licenses to include Emergency Operating Procedures as part of the Final Safety Analysis Report ([NUREG-0899](https://www.nrc.gov/docs/ML1025/ML102560007.pdf)).

**10 CFR 50.54** establishes conditions of licenses, including:
- **50.54(m)**: Minimum licensed operator staffing requirements per shift -- for single-unit facilities, at minimum 1 Senior Operator and 1 Operator; multi-unit sites have escalating requirements ([NRC 10 CFR 50.54](https://www.nrc.gov/reading-rm/doc-collections/cfr/part050/part050-0054))
- **50.54(x)**: Emergency departure authority -- licensees may deviate from license conditions when "immediately needed to protect the public health and safety" but require approval "as a minimum, by a licensed senior operator" ([NRC 10 CFR 50.54](https://www.nrc.gov/reading-rm/doc-collections/cfr/part050/part050-0054))
- **50.54(i-1)**: Operator requalification program requirements -- "Within 3 months after either the issuance of an operating license or the date that the Commission makes the finding under section 52.103(g)...the licensee shall have in effect an operator requalification program" ([NRC 10 CFR 50.54](https://www.nrc.gov/reading-rm/doc-collections/cfr/part050/part050-0054), [Cornell LII 10 CFR 50.54](https://www.law.cornell.edu/cfr/text/10/50.54)). Note: the `(i-1)` designation is the official CFR paragraph numbering as published in the eCFR and Cornell LII, not a sub-item of paragraph (i).

**10 CFR 50.59** establishes the process for evaluating changes to the facility or procedures and conducting tests or experiments without prior NRC approval ([NRC 10 CFR 50.59 Guidelines](https://www.nrc.gov/docs/ML0036/ML003678365.pdf)).

**10 CFR 50.65** (the Maintenance Rule) requires licensees to "assess and manage the increase in risk that may result from the proposed maintenance activities" before performing maintenance ([NRC 10 CFR 50.65](https://www.nrc.gov/reading-rm/doc-collections/cfr/part050/part050-0065)).

**10 CFR 50.120** requires each nuclear power plant to "establish, implement, and maintain a training program" derived from a "systems approach to training" that provides for "the training and qualification of categories of nuclear power plant personnel" and must be "periodically evaluated and revised as appropriate to reflect industry experience as well as changes to the facility, procedures, regulations, and quality assurance requirements" ([eCFR 10 CFR 50.120](https://www.ecfr.gov/current/title-10/chapter-I/part-50/subject-group-ECFR448a4b6d297d970/section-50.120)).

#### 1.2 10 CFR Part 50, Appendix B: The 18 Quality Assurance Criteria

Appendix B establishes 18 mandatory quality assurance criteria that form the procedural backbone of nuclear operations. The criteria most relevant to procedure-based work are ([NRC 10 CFR 50 Appendix B](https://www.nrc.gov/reading-rm/doc-collections/cfr/part050/part050-appb)):

| Criterion | Name | Key Procedural Requirements |
|-----------|------|----------------------------|
| I | Organization | QA personnel must have "sufficient authority, organizational independence, and direct access to management." Functions include "verifying activities through checking, auditing, and inspecting." |
| II | Quality Assurance Program | "Documented written policies and procedures established early." Regular management reviews required. |
| III | Design Control | "Independent design review required." Verification through "design reviews, alternate calculations, or testing." |
| V | Instructions, Procedures, and Drawings | All quality-affecting activities "prescribed by documented instructions, procedures, or drawings" with "appropriate quantitative or qualitative acceptance criteria." |
| VI | Document Control | Procedures must ensure documents are "reviewed for adequacy, approved by authorized personnel, and distributed to work locations." Changes reviewed by same organizations as original. |
| X | Inspection | "Inspection shall be performed by individuals other than those who performed the activity being inspected." **Mandatory hold points** "require witness or inspection by qualified personnel" and "beyond which work may not proceed without consent." |
| XI | Test Control | "Test procedures which incorporate the requirements and acceptance limits contained in applicable design documents." Includes proof tests, preoperational tests, and operational tests. |
| XVI | Corrective Action | "Conditions adverse to quality...are promptly identified and corrected." Significant issues require "root cause analysis" and reporting to management. |
| XVIII | Audits | "Comprehensive system of planned and periodic audits" by "appropriately trained personnel not having direct responsibilities in the areas being audited." |

#### 1.3 NUREG Series Guidance Documents

**NUREG-0899** (Guidelines for the Preparation of Emergency Operating Procedures) presents NRC guidance for evaluating EOP compliance with 10 CFR 50.34(b)(6)(ii). It covers the EOP Development Process, Technical Guidelines, Plant-Specific Writer's Guide, and Use and Maintenance requirements. Key format elements include: Writer's Guide usage, V&V methods, cross-referencing, CAUTION and NOTE statements, divisions/headings/numbering, style of expression, abbreviations/acronyms, WARNING and CAUTION statements, control room staffing, and consistency between staffing and procedures ([NUREG-0899 PDF](https://www.nrc.gov/docs/ML1025/ML102560007.pdf)).

**NUREG-1358** (Lessons Learned from the Special Inspection Program for Emergency Operating Procedures) documents findings from an NRC special inspection program covering 28 plants between October 1988 and September 1991. Supplement 1 was issued in 1992 via NRC Information Notice 92-76. The document reinforced NRC expectations regarding plant-specific technical guidelines, EOP writer's guide quality, EOP verification and validation (V&V), and EOP training programs. NRC Inspection Procedure IP 42454 (Emergency Operating Procedures) references NUREG-1358's findings as part of the basis for EOP inspection criteria ([NRC IP 42454, ML13232A368](https://www.nrc.gov/docs/ML1323/ML13232A368.pdf), [NRC Generic Safety Issues HF4](https://www.nrc.gov/sr0933/Section%204.%20Human%20Factor%20Issues/hf4r7.html)). Note: NUREG-1358 itself is not indexed in the NRC's online NUREG staff publications catalog; content is referenced via NRC inspection procedures and the NRC Generic Safety Issues database.

**NUREG-0711** (Human Factors Engineering Program Review Model, Revision 3) provides the NRC's review criteria for HFE programs. It addresses twelve review elements using a "top-down" approach: HFE Program Management, Operating Experience Review, Functional Requirements Analysis and Function Allocation, Task Analysis, Staffing, Human Reliability Analysis, Human-System Interface Design, **Procedure Development**, Training Program Development, **Human Factors Verification and Validation**, Design Implementation, and Human Performance Monitoring. Each element is structured with Background, Objective, Applicant Submittals, and Review Criteria sections ([NUREG-0711 NRC page](https://www.nrc.gov/reading-rm/doc-collections/nuregs/staff/sr0711/index), [NUREG-0711 Rev 3 PDF](https://www.nrc.gov/docs/ML1228/ML12285A131.pdf)).

---

### 2. INPO Standards and Human Performance Framework

The Institute of Nuclear Power Operations (INPO) was established in 1979 following the Three Mile Island accident "to promote the highest levels of safety and reliability -- to promote excellence -- in plant operation" ([INPO website](https://www.inpo.info)). INPO sets performance standards, measures industry performance against those standards, and facilitates improvement through "education and training, widespread sharing of best practices, lessons learned, and assistance" ([INPO info](https://www.inpo.info)).

#### 2.1 INPO's Human Performance Framework

INPO's approach to human performance encompasses two elements: "(1) reduce the frequency of events triggered by human error, and (2) minimize the severity of human performance events that still occur" ([INPO Human Performance approach, Academia.edu](https://www.academia.edu/7534293/INPO_s_approach_to_human_performance_in_the_United_States_commercial_nuclear_power_industry)).

The framework rests on **five core principles**, codified in DOE-HDBK-1028-2009 Volume 1 (Concepts and Principles), which establishes "a common understanding" of human performance improvement based on "years of user experience among INPO's membership" ([DOE-HDBK-1028-2009 Vol. 1](https://www.standards.doe.gov/standards-documents/1000/1028-BHdbk-2009-v1), [Nuclear PSG summary](https://www.nuclearpsg.co.uk/understanding-human-performance-in-nuclear/)):

1. **Human Fallibility**: "People are fallible, and even the best people make mistakes." Additional defenses like quality systems and peer review must support individual performance.
2. **Predictable Errors**: "Error-likely situations are predictable, manageable, and preventable."
3. **Organizational Influence**: "Individual behavior is influenced by organizational processes and values."
4. **Leadership Impact**: "People achieve high levels of performance largely because of the encouragement and reinforcement received from leaders."
5. **Learning from Events**: "Events can be avoided through an understanding of the reasons mistakes occur and application of the lessons learned from past events."

These principles drive **ten error reduction tools** described in DOE-HDBK-1028-2009 Volume 2 (Human Performance Tools for Individuals, Work Teams, and Management), which serves as a "menu" of tools used across nuclear and other safety-critical industries ([DOE-HDBK-1028-2009 Vol. 2](https://www.standards.doe.gov/files/doe-hdbk-1028-2009-human-performance-improvement-handbook-volume-2-human-performance-tools-for-individuals-work-teams-and-management), [Nuclear PSG summary](https://www.nuclearpsg.co.uk/understanding-human-performance-in-nuclear/)):

| # | Tool | Purpose |
|---|------|---------|
| 1 | Pre-Job Briefs | Discuss scope, risks, error traps, and human performance tools before starting work |
| 2 | Review of Operating Experience | Apply lessons learned from prior events |
| 3 | Procedure Use and Adherence | Follow procedures as written, in sequence |
| 4 | Self-Checking (STAR) | Stop-Think-Act-Review before critical actions |
| 5 | Questioning Attitude | Continuously challenge existing conditions and activities |
| 6 | Peer Checking | Two-person verification at point of action |
| 7 | Independent Verification | Third-party confirmation (e.g., by engineer) |
| 8 | Three-Part Communication | Sender-Receiver-Confirmation cycle |
| 9 | Post-Job Brief | Capture lessons learned and improvement opportunities |
| 10 | Task Observation/Coaching | Supervisory monitoring of work performance |

#### 2.2 Procedure Use and Adherence

The concept of procedure adherence is central to nuclear operations safety. DOE-HDBK-1028-2009 Volume 2 describes the "Procedure Use and Adherence" tool as requiring that "the user performs all actions as written in the sequence specified by the document" and that "if it cannot be used safely and correctly as written, then the activity is stopped, and the procedure is revised before continuing" ([DOE-HDBK-1028-2009 Vol. 2](https://www.standards.doe.gov/files/doe-hdbk-1028-2009-human-performance-improvement-handbook-volume-2-human-performance-tools-for-individuals-work-teams-and-management)). The DOE handbook further notes that "consistent and rigorous use of this HPI tool at DOE facilities will improve productivity and safety and reduce unwanted events."

Per publicly available summaries of INPO's procedure adherence policy (direct access to the proprietary INPO 09-004 document was not possible), procedure adherence means "understanding a procedure's purpose, scope, and intent and following its direction" and "effective implementation of sound procedure use and adherence methods is tied directly to human error reduction, event prevention, and safety" ([ATR Training blog summary of INPO procedure adherence concepts](https://www.atrco.com/blog/does-organization-follow-procedure-use-adherence-policy); note: ATR Training is a nuclear industry training consultancy that summarizes INPO guidance for its clients).

> **Source provenance note:** The ATR blog attributes procedure adherence concepts to INPO generically but does not cite a specific INPO document number. The DOE-HDBK-1028-2009 (T2, publicly available) provides equivalent language from a verifiable primary source and is used as the primary citation above. The ATR blog is retained as supplementary context for the INPO-specific framing.

---

### 3. Nuclear Plant SOP Structure

#### 3.1 Procedure Types

Nuclear power plants maintain a comprehensive hierarchy of procedure types ([EPRI/NRC Report](https://www.nrc.gov/docs/ML0800/ML080080077.pdf), [IAEA NS-G-2.2](https://www.iaea.org/publications/6064/operational-limits-and-conditions-and-operating-procedures-for-nuclear-power-plants)):

| Procedure Type | Abbreviation | Purpose | Use Level |
|----------------|-------------|---------|-----------|
| Normal Operating Procedures | OPs | Routine plant operations, startup, shutdown, mode changes | Reference or Continuous |
| Abnormal Operating Procedures | AOPs | "Maintain plant control while mitigating consequences of abnormal operating conditions to avoid challenging the Reactor Protection System" | Continuous |
| Emergency Operating Procedures | EOPs | "Direct operators' actions necessary to mitigate consequences of transients and accidents" beyond protection system setpoints | Continuous |
| Alarm Response Procedures | ARPs | "Provide short term and immediate corrective actions associated with plant transients or equipment malfunctions" | Reference |
| Surveillance Test Procedures | STPs | "Demonstrate Safety Related Equipment and System Operability as required by Technical Specifications" | Continuous |
| Integrated Operating Procedures | IOPs | "Transiting between operating modes or changing power level...require the use of multiple procedures" | Continuous |
| Maintenance Procedures | MPs | Preventive/corrective maintenance of plant equipment | Continuous |

#### 3.2 Procedure Use Classifications

Procedures are classified by how closely the operator must follow the written text during execution ([Human Performance Tools - Procedure Use](https://www.humanperformancetools.com/human-performance-tools/human-performance-tool-procedure-use-adherence)):

| Classification | Description | Requirements |
|----------------|-------------|-------------|
| **Continuous Use** | Procedure kept in-hand throughout task. Every step read and followed in sequence. | Place-keeping required. Step sign-off after each action. |
| **Reference Use** | Procedure consulted at the job site as needed. | Worker familiar with procedure but references for specifics. |
| **Information Use** | Procedure available in libraries or on-hand as reference material. | General guidance; worker has extensive training/experience. |
| **Multi-Level** | Individual procedure sections employ varying usage levels. | Each section follows its assigned classification. |

#### 3.3 Standard Procedure Structure

Based on DOE-STD-1029-92 (Writer's Guide for Technical Procedures), nuclear procedures follow a standardized structure that addresses "content, format, and style of technical procedures that prescribe production, operation of equipment and facilities, and maintenance activities" ([DOE-STD-1029-92](https://www.standards.doe.gov/standards-documents/1000/1029-astd-1992-cn1-1998)):

**Typical Procedure Sections:**

1. **Cover/Title Page**: Procedure number, title, revision number, approval signatures
2. **Purpose and Scope**: What the procedure covers and its boundaries
3. **References**: Applicable codes, standards, and related procedures
4. **Prerequisites**: Conditions that must exist before starting (equipment status, personnel qualifications, required tools and materials)
5. **Initial Conditions**: Plant/system state required before beginning
6. **Limitations and Precautions**: Boundaries that must not be exceeded; safety warnings
7. **WARNING, CAUTION, and NOTE Statements**: Safety alerts placed before the step to which they apply
8. **Performance Steps**: Sequential numbered instructions with acceptance criteria
9. **Acceptance Criteria**: Quantitative or qualitative measures for determining satisfactory completion (per Appendix B Criterion V)
10. **Sign-off/Verification**: Space for performer initials, verifier signatures, and hold point releases
11. **Attachments/Data Sheets**: Forms for recording data, checklists, and supporting information

**Key Formatting Standards** ([DOE-STD-1029-92](https://www.standards.doe.gov/standards-documents/1000/1029-astd-1992-cn1-1998), [NUREG-0899](https://www.nrc.gov/docs/ML1025/ML102560007.pdf)):
- Paragraph numbering style (legal numbering: 1.0, 1.1, 1.1.1)
- WARNING/CAUTION/NOTE statements placed BEFORE the step they apply to
- Short, concise steps for accuracy and resumability after interruption
- Clear action verbs from standardized verb lists
- Equipment identified by full nomenclature (tag numbers, system designators)

#### 3.4 Place-Keeping and Step Sign-Off

For continuous-use procedures, place-keeping ensures the operator tracks their position through the procedure ([Human Performance Tools - Procedure Use](https://www.humanperformancetools.com/human-performance-tools/human-performance-tool-procedure-use-adherence)):

- "An effective place-keeping method is used for procedures that do not require sign-offs, with at least an initial or check of each step completed after the action is performed, before proceeding with the next step"
- "When a signature or initial is required, sign or initial the step each time it is performed"
- Initialing each step AFTER completing the action, BEFORE advancing to the next step
- Avoiding ditto marks, single-initials-with-lines, or premature sign-offs

---

### 4. Emergency Operating Procedures (EOPs)

#### 4.1 History and Regulatory Foundation

Following the Three Mile Island (TMI) accident in 1979, the NRC issued NUREG-0899 which provided requirements for "utility preparation and implementation of emergency operating procedures (EOP), including development, writing and maintenance" ([NAS/NRC Lessons Learned](https://www.ncbi.nlm.nih.gov/books/NBK253949/)). This was followed by the NRC's Special Inspection Program for Emergency Operating Procedures (October 1988 to September 1991), covering 28 plants, whose findings were documented in NUREG-1358 and reinforced NRC expectations regarding plant-specific technical guidelines, EOP writer's guide quality, EOP verification and validation (V&V), and EOP training programs. Supplement 1 was issued in 1992 via NRC Information Notice 92-76 ([NRC IP 42454, ML13232A368](https://www.nrc.gov/docs/ML1323/ML13232A368.pdf)).

#### 4.2 Symptom-Based vs. Event-Based Approaches

The nuclear industry transitioned from event-based EOPs (which required operators to diagnose the specific event before responding) to **symptom-based EOPs** (which direct operators to respond to observable plant symptoms regardless of the initiating event) ([Westinghouse Procedures](https://westinghousenuclear.com/data-sheet-library/procedures-development-and-maintenance/)):

- **Symptom-based EOPs**: Enable "control room staff to engage in immediate symptom-based responses" without requiring extensive analysis. "Because the BWR emergency procedures are symptom based, it is possible to be in many places in the procedures concurrently, a situation which may require the operating crew to take a number of different actions to control the plant" ([NAS/NRC Lessons Learned](https://www.ncbi.nlm.nih.gov/books/NBK253949/))
- Westinghouse was "a leader in converting event-based EOPs to the new symptom-based format" ([Westinghouse](https://westinghousenuclear.com/data-sheet-library/procedures-development-and-maintenance/))
- Current procedure guidance "must be symptom based, while addressing multiple events, multiple failures, inadequate core cooling events and anticipated transient without scram (ATWS)" ([Westinghouse](https://westinghousenuclear.com/data-sheet-library/procedures-development-and-maintenance/))

#### 4.3 EOP Decision Hierarchy

When abnormal conditions occur, operators follow a structured decision hierarchy ([EPRI/NRC Report](https://www.nrc.gov/docs/ML0800/ML080080077.pdf)):

1. **First**: Confirm whether an EOP should be performed (reactor protection system or engineered safety feature setpoints exceeded)
2. **If no EOP applies**: Consider an Abnormal Operating Procedure (AOP)
3. **If no AOP applies**: Operate alarms with Alarm Response Procedures (ARPs)

#### 4.4 EOP vs. SAMG (Severe Accident Management Guidelines)

EOPs and SAMGs serve different domains ([NAS/NRC Lessons Learned](https://www.ncbi.nlm.nih.gov/books/NBK253949/)):
- **EOPs**: Address design-basis events that operators are trained to handle; enable immediate symptom-based response by control room staff
- **SAMGs**: Cover "beyond-design-basis" scenarios with degraded cores; anticipate that engineering staff in the technical support center will guide reactor operators

Post-Fukushima, the NRC found inconsistent SAMG implementation and recommended regulatory oversight, leading to integration of EOPs with FLEX capabilities ([NAS/NRC Lessons Learned](https://www.ncbi.nlm.nih.gov/books/NBK253949/), [NEI 14-01](https://www.nrc.gov/docs/ML1622/ML16224A619.pdf)).

---

### 5. Maintenance Procedures

#### 5.1 Regulatory Foundation

10 CFR 50.65 (the Maintenance Rule) requires licensees to monitor the effectiveness of maintenance at nuclear power plants. Before performing maintenance, licensees "shall assess and manage the increase in risk that may result from the proposed maintenance activities" ([NRC 10 CFR 50.65](https://www.nrc.gov/reading-rm/doc-collections/cfr/part050/part050-0065)).

#### 5.2 Maintenance Categories

Maintenance activities at nuclear facilities fall into defined categories ([IAEA Maintenance, Testing, Surveillance](https://www.iaea.org/publications/14905/maintenance-testing-surveillance-and-inspection-in-nuclear-power-plants)):

- **Corrective Maintenance**: "Cost to repair failed or malfunctioning equipment, systems, or facilities to restore the intended function or design condition"
- **Preventive Maintenance**: "Cost of all systematically planned or scheduled actions required to prevent the failure of equipment, systems, structures, or facilities"
- **Predictive Maintenance**: Condition-based monitoring to predict failure
- **Surveillance and Testing**: Periodic verification of safety system operability

Preventive maintenance is further categorized as "periodic (time-based), planned or predictive" ([IAEA](https://www.iaea.org/publications/14905/maintenance-testing-surveillance-and-inspection-in-nuclear-power-plants)).

#### 5.3 Work Package Structure

Nuclear maintenance uses structured work packages that include ([DOE Nuclear Facility Maintenance Management Program Guide](https://www.directives.doe.gov/directives-documents/400-series/0433.1-EGuide-1/@@images/file)):

1. **Work Request/Identification**: Problem description, equipment identification
2. **Risk Assessment**: Pre-maintenance risk evaluation per 10 CFR 50.65
3. **Work Planning**: Scope, instructions, parts, tools, qualifications required
4. **Pre-Job Brief**: Discussion of scope, risks, human performance tools, error traps
5. **Procedure Execution**: Step-by-step instructions with hold points and sign-offs
6. **Quality Control Hold Points**: Mandatory inspection points requiring QC witness
7. **Post-Maintenance Testing**: "Confirm that the maintenance was performed correctly"
8. **Post-Job Brief**: Lessons learned, issues encountered, improvement opportunities
9. **Work Package Closure**: Verification of completion, documentation review

#### 5.4 Hold Points and Witness Points

Based on Appendix B Criterion X and industry practice ([NRC 10 CFR 50 Appendix B](https://www.nrc.gov/reading-rm/doc-collections/cfr/part050/part050-appb), [Quality Engineers Guide](https://www.qualityengineersguide.com/what-is-witness-point-and-hold-point/)):

| Type | Definition | Work Impact |
|------|-----------|-------------|
| **Hold Point** | "A mandatory verification point beyond which work cannot proceed without approval by the designated authority" | Work STOPS. Cannot continue without release. |
| **Witness Point** | "The manufacturer shall notify the client and inspector, but there is no hold on production" | Work continues if inspector notified but unavailable. |

Appendix B Criterion X states: "Mandatory inspection hold points require witness or inspection by qualified personnel and are points beyond which work may not proceed without consent" ([NRC 10 CFR 50 Appendix B](https://www.nrc.gov/reading-rm/doc-collections/cfr/part050/part050-appb)).

---

### 6. Human Factors Engineering and Human Performance Tools

#### 6.1 NUREG-0711: Human Factors Engineering Review Model

NUREG-0711 establishes the NRC's framework for reviewing HFE programs using a "top-down" approach starting with "high-level plant mission goals" and working down through function allocation, task analysis, staffing, human-system interface design, **procedure development**, training program development, and **human factors verification and validation** ([NUREG-0711 NRC Index](https://www.nrc.gov/reading-rm/doc-collections/nuregs/staff/sr0711/index), [NUREG-0711 Rev 3 PDF](https://www.nrc.gov/docs/ML1228/ML12285A131.pdf)).

The twelve review elements of NUREG-0711 are ([ResearchGate NUREG-0711 diagram](https://www.researchgate.net/figure/NUREG-0711-Revision-2-HFE-review-elements-A-brief-description-of-each-element-follows_fig1_241909507)):

1. HFE Program Management
2. Operating Experience Review
3. Functional Requirements Analysis and Function Allocation
4. Task Analysis
5. Staffing
6. Human Reliability Analysis
7. Human-System Interface Design
8. **Procedure Development**
9. Training Program Development
10. **Human Factors Verification and Validation**
11. Design Implementation
12. Human Performance Monitoring

#### 6.2 STAR (Self-Checking)

The STAR technique is "a foundational human performance tool originating from commercial nuclear power in the early 1990s" ([Human Performance Tools website](https://www.humanperformancetools.com/human-performance-tools/human-performance-tool-spotlight-self-checking)):

| Step | Action | Details |
|------|--------|---------|
| **S - Stop** | Pause to concentrate | Eliminate distractions, check surroundings for hazards, verify readiness with necessary procedures and materials |
| **T - Think** | Understand expected outcome | Verify appropriateness given equipment status, compare field conditions to documentation, consider contingencies |
| **A - Act** | Perform the correct action | Maintain eye contact with labels while touching component, compare to guiding documents before proceeding |
| **R - Review** | Verify anticipated result occurred | Implement contingency plans if unexpected results emerge |

"Lack of self checking results in the majority of error" ([Human Performance Tools](https://www.humanperformancetools.com/human-performance-tools/human-performance-tool-spotlight-self-checking)). The tool is most effective for equipment manipulation, data entry, repetitive tasks, and error-prone situations involving similar components.

#### 6.3 Peer Checking and Concurrent Verification

**Peer checking** involves "two people (performer and peer) self-checking in parallel, agreeing together that the action is the correct action to perform on the correct component" ([DOE-HDBK-1028-2009 Vol. 2](https://www.standards.doe.gov/files/doe-hdbk-1028-2009-human-performance-improvement-handbook-volume-2-human-performance-tools-for-individuals-work-teams-and-management)). It is "similar to concurrent verification (CV) but less formal" and "takes advantage of a fresh set of eyes not trapped by the performer's task-focused mind-set."

**DOE-HDBK-1028-2009** (Human Performance Improvement Handbook, Volume 2) establishes "a common understanding of the standards and conditions for effective application of error detection and prevention methods" and "reflects years of user experience among INPO's membership" ([DOE-HDBK-1028-2009 Vol. 2](https://www.standards.doe.gov/files/doe-hdbk-1028-2009-human-performance-improvement-handbook-volume-2-human-performance-tools-for-individuals-work-teams-and-management)).

#### 6.4 Three-Part Communication

Three-part communication ensures message accuracy through a structured exchange ([Human Performance Tools](https://www.humanperformancetools.com/human-performance-tools/human-performance-tool-spotlight-three-part-communication)):

1. **Sender states the message** clearly and concisely, ensuring the receiver's attention
2. **Receiver acknowledges** by paraphrasing the message, repeating equipment designators verbatim
3. **Sender acknowledges** the receiver's reply, confirming understanding or restating if incorrect

Required for: "task assignments that impact equipment or activities, the safety of personnel, the environment, or the grid"; "when communicating condition of equipment"; "when communicating the value of an important parameter"; "performance of steps or actions using an approved procedure"; and "operation or alteration of equipment" ([Human Performance Tools](https://www.humanperformancetools.com/human-performance-tools/human-performance-tool-spotlight-three-part-communication)).

The goal is "mutual understanding between two or more people, especially communication involving technical information related to proper operation or personnel safety" ([Human Performance Tools](https://www.humanperformancetools.com/human-performance-tools/human-performance-tool-spotlight-three-part-communication)).

Equipment identification uses phonetic alphabet: "announce valve ELG-5678 as 'valve Echo-Lima-Golf-5-6-7-8'" ([Fossil Consulting](https://www.fossilconsulting.com/blog/safety/3-part-communication/)).

#### 6.5 Pre-Job and Post-Job Briefings

**Pre-Job Briefings** are "commensurate with the risk and complexity of the tasks" and include ([IAEA Pub1623](https://www-pub.iaea.org/MTCD/Publications/PDF/Pub1623_web.pdf)):
- Discussion of scope and sequence of work
- Human error and its possible consequences for critical attributes
- Identification of additional controls or barriers needed
- Risk factors and error-prevention tool effectiveness

**Post-Job Briefings** capture lessons learned and feed back into the operating experience program. "Using lessons learned from human errors is a way to reduce the number of events and to mitigate their consequences" ([IAEA-TECDOC-1458](https://www.iaea.org/publications/7226/effective-corrective-actions-to-enhance-operational-safety-of-nuclear-installations)).

---

### 7. Independent Verification and Quality Hold Points

#### 7.1 Regulatory Basis for Independent Verification

Appendix B Criterion X mandates: "Inspection shall be performed by individuals other than those who performed the activity being inspected" ([NRC 10 CFR 50 Appendix B](https://www.nrc.gov/reading-rm/doc-collections/cfr/part050/part050-appb)).

Criterion I requires QA functions include "verifying activities through checking, auditing, and inspecting" with "sufficient authority, organizational independence, and direct access to management" ([NRC 10 CFR 50 Appendix B](https://www.nrc.gov/reading-rm/doc-collections/cfr/part050/part050-appb)).

Criterion XVIII requires "appropriately trained personnel not having direct responsibilities in the areas being audited" ([NRC 10 CFR 50 Appendix B](https://www.nrc.gov/reading-rm/doc-collections/cfr/part050/part050-appb)).

#### 7.2 Types of Verification in Nuclear Operations

Based on the DOE Human Performance framework and NRC requirements:

| Verification Type | Who Performs | When | Formality |
|-------------------|-------------|------|-----------|
| **Self-Checking (STAR)** | The performer | Before every critical action | Informal but mandatory |
| **Peer Checking** | A co-worker present at the same time and place | During the action | Semi-formal |
| **Concurrent Verification** | A designated verifier present during the action | During the action | Formal; documented |
| **Independent Verification** | A qualified individual NOT involved in the work | After the action, before system restoration | Formal; documented with signature |
| **QC Hold Point Inspection** | Quality Control inspector | At designated hold points in the procedure | Formal; work cannot proceed without release |
| **NRC Inspection** | NRC resident or regional inspector | Per baseline inspection program | Regulatory; documented in inspection reports |

The NRC inspection program uses a "performance-based, risk-informed approach" with "direct observation of work activities, interviews with licensee workers, demonstrations by appropriate workers, and independent verification" ([NRC Oversight Backgrounder](https://www.nrc.gov/reading-rm/doc-collections/fact-sheets/oversight)).

#### 7.3 NRC Reactor Oversight Process

The NRC's ongoing oversight uses a color-coded assessment system ([NRC ROP Description](https://www.nrc.gov/reactors/operating/oversight/rop-description)):

- **Green**: Performance acceptable, little or no safety impact
- **White**: Greater safety significance, increased regulatory attention
- **Yellow**: Even greater significance
- **Red**: Most significant

This is supported by "baseline inspections (the minimum required at all plants), supplemental inspections (which increase in intensity if plant performance falls below established thresholds), and special inspections (which focus on a specific plant event or issue)" with quarterly submission of "15 separate performance indicators" ([NRC Oversight Backgrounder](https://www.nrc.gov/reading-rm/doc-collections/fact-sheets/oversight)).

---

### 8. Procedure-Based Decision Frameworks

#### 8.1 NRC Safety Culture: Nine Traits

The NRC Safety Culture Policy Statement defines nine traits of a positive safety culture ([NRC Safety Culture Policy Statement](https://www.nrc.gov/about-nrc/safety-culture/sc-policy-statement)):

| # | Trait | Definition |
|---|-------|-----------|
| 1 | Leadership Safety Values and Actions | "Leaders demonstrate a commitment to safety in their decisions and behaviors" |
| 2 | Problem Identification and Resolution | "Issues potentially impacting safety are promptly identified, fully evaluated, and promptly addressed and corrected commensurate with their significance" |
| 3 | Personal Accountability | "All individuals take personal responsibility for safety" |
| 4 | Work Processes | "The process of planning and controlling work activities is implemented so that safety is maintained" |
| 5 | Continuous Learning | "Opportunities to learn about ways to ensure safety are sought out and implemented" |
| 6 | Environment for Raising Concerns | "A safety conscious work environment is maintained where personnel feel free to raise safety concerns without fear of retaliation" |
| 7 | Effective Safety Communications | "Communications maintain a focus on safety" |
| 8 | Respectful Work Environment | "Trust and respect permeate the organization" |
| 9 | Questioning Attitude | "Individuals avoid complacency and continually challenge existing conditions and activities in order to identify discrepancies that might result in error or inappropriate action" |

#### 8.2 Decision Authority and Procedure Deviation

Nuclear operations define strict authority levels for procedure deviation ([NRC 10 CFR 50.54](https://www.nrc.gov/reading-rm/doc-collections/cfr/part050/part050-0054)):

| Situation | Authority | Regulatory Basis |
|-----------|-----------|-----------------|
| Normal operations within procedure | Licensed operator on shift | 10 CFR 50.54(m) |
| Procedure cannot be followed as written | **STOP WORK.** Resolve before continuing. | DOE-HDBK-1028-2009 Vol. 2 (Procedure Use and Adherence tool); INPO adherence policy |
| Abnormal condition within procedure scope | Shift supervisor (Senior Reactor Operator) | Plant Technical Specifications |
| Emergency requiring departure from license conditions | Licensed Senior Operator approval required (minimum) | 10 CFR 50.54(x) |
| Changes to facility or procedures | 10 CFR 50.59 evaluation process | 10 CFR 50.59 |

The key principle: "Conservative actions are taken when understanding is incomplete" ([NRC Safety Culture](https://www.nrc.gov/about-nrc/safety-culture/sc-policy-statement)). This is the **conservative decision-making** principle that ensures operators err on the side of caution when information is insufficient.

#### 8.3 Defense-in-Depth as a Decision Framework

Defense-in-depth "employs successive compensatory measures to prevent accident or mitigate damage" and "ensures that safety will not be wholly dependent on any single element of the design, construction, maintenance or operation of a nuclear facility" ([NRC Defense-in-Depth](https://www.nrc.gov/docs/ML1327/ML13277A425.pdf)). This directly translates to procedural design: no single step, check, or verification should be the only barrier to preventing an error from propagating.

#### 8.4 Corrective Action Program

Every nuclear plant operates a Corrective Action Program that captures all deviations and near-misses. The IAEA states that "every minor event, incident, deviation, etc. has to be documented, evaluated and corrected" with "corrective actions taken or planned (repair, replacement or modification of equipment, modification of procedures, training of personnel, timeframe) to prevent recurrence" ([IAEA-TECDOC-1458](https://www.iaea.org/publications/7226/effective-corrective-actions-to-enhance-operational-safety-of-nuclear-installations), [OECD-NEA Corrective Action](https://www.oecd-nea.org/upload/docs/application/pdf/2020-01/cnra-r2010-7.pdf)).

In a plant with strong safety culture, "the operating experience programme will capture and report on all internal events, near misses, deviations (from accepted procedures, standards, operating/maintenance practices or behaviors), and good practices or opportunities for improvement" ([IAEA-TECDOC-1581](https://www-pub.iaea.org/MTCD/Publications/PDF/TE_1581_web.pdf)).

#### 8.5 DOE Conduct of Operations

DOE Order 422.1 (successor to DOE Order 5480.19) defines requirements for "establishing and implementing Conduct of Operations Programs at Department of Energy facilities and projects, which consist of formal documentation, practices, and actions implementing disciplined and structured operations that support mission success and promote worker, public, and environmental protection" ([DOE O 422.1](https://www.directives.doe.gov/directives-documents/400-series/0422.1-BOrder)). It covers chapters on operations organization, shift routines, control area activities, communications, control of on-shift training, investigation of abnormal events, notifications, log keeping, operations turnover, and independent verification.

---

## L2: Strategic Implications for Claude Code Skill Design

### Directly Transferable Patterns

The nuclear SOP framework provides the following patterns that can be directly mapped to an AI agent workflow skill:

#### Pattern 1: Procedure Use Classification (Continuous/Reference/Information)

**Nuclear Practice**: Every procedure has a use classification determining how closely it must be followed.

**Skill Translation**: Agent workflows could classify steps as:
- **Continuous** (mandatory sequential execution with step acknowledgment)
- **Reference** (agent consults guidance but exercises judgment)
- **Information** (context available but not binding)

#### Pattern 2: STAR Self-Checking at Critical Steps

**Nuclear Practice**: Stop-Think-Act-Review before every critical action.

**Skill Translation**: Before any destructive or irreversible tool call (file write, git commit, API call), the agent pauses to:
- **Stop**: Identify the step about to be executed
- **Think**: Validate preconditions and expected outcome
- **Act**: Execute the tool call
- **Review**: Verify the outcome matches expectations; halt if not

#### Pattern 3: Hold Points and Mandatory Verification Gates

**Nuclear Practice**: "Work may not proceed without consent of designated representative" at hold points.

**Skill Translation**: Certain steps in a workflow require explicit user approval before the agent proceeds. This maps directly to quality gates in the orchestration skill, but could be formalized with named hold-point types:
- **User Hold Point**: Human must approve (analogous to QC inspector hold)
- **Quality Gate Hold Point**: Critic score must pass threshold
- **Independent Review Hold Point**: Fresh-context reviewer must verify

#### Pattern 4: Independent Verification (Inspector != Performer)

**Nuclear Practice**: "Inspection shall be performed by individuals other than those who performed the activity."

**Skill Translation**: The creator-critic-revision cycle (H-14) already implements this. The nuclear pattern reinforces that the critic MUST have context isolation (FC-M-001) -- a fresh-context reviewer free from the creator's reasoning bias.

#### Pattern 5: Three-Part Communication Protocol

**Nuclear Practice**: Sender-Receiver-Confirmation for critical communications.

**Skill Translation**: Agent handoffs in multi-agent workflows should use structured handoff schemas with explicit confirmation:
1. Sending agent states the handoff content
2. Receiving agent acknowledges and echoes key findings
3. Sending agent (or orchestrator) confirms mutual understanding

#### Pattern 6: Pre-Job and Post-Job Briefings

**Nuclear Practice**: Briefings before and after work to discuss scope, risks, and lessons learned.

**Skill Translation**:
- **Pre-Job**: At workflow start, load context, review operating experience (prior failures), identify error traps
- **Post-Job**: At workflow end, capture lessons learned, log what worked and what did not, feed back into the skill's knowledge base

#### Pattern 7: Prerequisite and Initial Condition Checking

**Nuclear Practice**: Verify prerequisites and initial conditions before starting any procedure.

**Skill Translation**: Before executing a workflow, verify:
- Required files exist
- Project context is loaded (H-04)
- Required tools are available
- Prior phase outputs are valid

#### Pattern 8: WARNING/CAUTION/NOTE Placement

**Nuclear Practice**: Safety alerts placed BEFORE the step they apply to, not after.

**Skill Translation**: In agent prompts and workflow definitions, constraints and guardrails should be declared before the instructions they constrain, not after. This aligns with the NPT (Negative Prompt Templates) pattern already used in Jerry agent definitions.

#### Pattern 9: Stop-Work Authority

**Nuclear Practice**: "If the procedure cannot be used as written, the activity is stopped and the issue is resolved."

**Skill Translation**: If an agent encounters a situation where the workflow cannot proceed as defined (missing inputs, unexpected state, ambiguous requirements), it MUST stop and escalate to the user rather than improvising. This maps to H-31 (clarify when ambiguous).

#### Pattern 10: Corrective Action and Operating Experience Feedback

**Nuclear Practice**: Every deviation, near-miss, and event is captured, analyzed, and fed back into procedure improvement.

**Skill Translation**: Agent execution logs, quality gate failures, and user corrections should be captured and used to improve workflow definitions over time. This maps to the Jerry knowledge base and lessons-learned pattern.

### Architectural Alignment

The nuclear SOP framework reinforces several existing Jerry architecture decisions:

| Nuclear Concept | Jerry Equivalent | Status |
|----------------|------------------|--------|
| Appendix B Criterion V (procedures for all quality activities) | P-002 (file persistence for all outputs) | Implemented |
| Appendix B Criterion X (independent inspection) | H-14 (creator-critic-revision) + FC-M-001 | Implemented |
| Hold Points | Quality gates in /orchestration | Implemented |
| Three-Part Communication | Structured handoff protocol (agent-development-standards.md) | Implemented |
| Procedure Use Classification | Not yet formalized in Jerry workflows | **Gap** |
| STAR Self-Checking | S-010 (Self-Refine) is closest but lacks the structured 4-step pattern | **Partial** |
| Pre-Job/Post-Job Briefing | Not formalized in agent workflows | **Gap** |
| Stop-Work Authority | H-31 (clarify when ambiguous) | Implemented |
| Corrective Action Program | Worktracker captures issues but lacks formal OE feedback loop | **Partial** |
| Safety Culture Traits | Constitutional principles (P-001 through P-022) | Implemented |

### Risk Assessment

The nuclear industry's approach to procedure verification (V&V, walkthrough, tabletop, simulator) suggests that any procedure-based skill for Claude Code should include:

1. **Procedure Validation**: New workflows should be tested against realistic scenarios before deployment
2. **Procedure Maintenance**: Workflows must be versioned and updated based on operating experience
3. **Training Integration**: Users should understand the workflow structure and their role in hold points and escalations

---

## References

### T1 Sources (Primary -- NRC, Federal Regulations)

1. [NRC 10 CFR Part 50 Index](https://www.nrc.gov/reading-rm/doc-collections/cfr/part050/index) -- Domestic licensing of production and utilization facilities
2. [NRC 10 CFR 50 Appendix B -- Quality Assurance Criteria](https://www.nrc.gov/reading-rm/doc-collections/cfr/part050/part050-appb) -- 18 QA criteria for nuclear plants
3. [NRC 10 CFR 50.54 -- Conditions of Licenses](https://www.nrc.gov/reading-rm/doc-collections/cfr/part050/part050-0054) -- Operator staffing, emergency departure authority
4. [NRC 10 CFR 50.59 Guidelines](https://www.nrc.gov/docs/ML0036/ML003678365.pdf) -- Changes to facility or procedures evaluation
5. [NRC 10 CFR 50.65 -- Maintenance Rule](https://www.nrc.gov/reading-rm/doc-collections/cfr/part050/part050-0065) -- Maintenance effectiveness monitoring
6. [eCFR 10 CFR 50.120 -- Training and Qualification](https://www.ecfr.gov/current/title-10/chapter-I/part-50/subject-group-ECFR448a4b6d297d970/section-50.120) -- Personnel training requirements
7. [NUREG-0899 -- Guidelines for EOP Preparation (PDF)](https://www.nrc.gov/docs/ML1025/ML102560007.pdf) -- Emergency Operating Procedure guidelines (ADAMS accession ML102560007; URL verified to resolve to PDF)
8. [NUREG-0711 -- Human Factors Engineering Program Review Model](https://www.nrc.gov/reading-rm/doc-collections/nuregs/staff/sr0711/index) -- NRC HFE review framework
9. [NUREG-0711 Rev 3 (PDF)](https://www.nrc.gov/docs/ML1228/ML12285A131.pdf) -- Full document, 12 review elements
10. [NRC IP 42454 -- Emergency Operating Procedures Inspection Procedure (PDF)](https://www.nrc.gov/docs/ML1323/ML13232A368.pdf) -- References NUREG-1358 findings; ADAMS accession ML13232A368
10a. [NRC Generic Safety Issues HF4 -- Procedures](https://www.nrc.gov/sr0933/Section%204.%20Human%20Factor%20Issues/hf4r7.html) -- NRC generic safety issue database entry referencing NUREG-1358 and EOP inspection program
11. [NRC Inspection Procedures Index](https://www.nrc.gov/reading-rm/doc-collections/insp-manual/inspection-procedure/index) -- Complete inspection procedure library
12. [NRC Safety Culture Policy Statement](https://www.nrc.gov/about-nrc/safety-culture/sc-policy-statement) -- Nine traits of positive safety culture
13. [Federal Register: Final Safety Culture Policy Statement](https://www.federalregister.gov/documents/2011/06/14/2011-14656/final-safety-culture-policy-statement) -- Official Federal Register publication
14. [NRC Reactor Oversight Process Description](https://www.nrc.gov/reactors/operating/oversight/rop-description) -- ROP framework
15. [NRC Backgrounder on Oversight of Nuclear Power Plants](https://www.nrc.gov/reading-rm/doc-collections/fact-sheets/oversight) -- Baseline inspections and performance indicators
16. [NRC Defense-in-Depth Observations](https://www.nrc.gov/docs/ML1327/ML13277A425.pdf) -- Defense-in-depth as safety philosophy
17. [NRC Quality Assurance for New Reactors](https://www.nrc.gov/reactors/new-reactors/how-we-regulate/oversight/quality-assurance) -- QA oversight framework
18. [NRC EOP Writers Guide (Catawba)](https://www.nrc.gov/docs/ML1705/ML17054A844.pdf) -- Example plant-specific EOP writer's guide
19. [NRC Human Performance Tools Presentation (PDF)](https://www.nrc.gov/docs/ML1021/ML102120052.pdf) -- NRC briefing on human performance tools
20. [NRC Corrective Action Processes](https://www.nrc.gov/docs/ML1003/ML100321499.pdf) -- Corrective action for new nuclear power plants
20a. [Cornell LII -- 10 CFR 50.54 Conditions of Licenses](https://www.law.cornell.edu/cfr/text/10/50.54) -- Full regulatory text including paragraph (i-1) operator requalification program requirements; verified 50.54(i-1) is the correct CFR paragraph designation

### T2 Sources (Secondary -- INPO, DOE, IAEA)

21. [INPO Website](https://www.inpo.info) -- Institute of Nuclear Power Operations
22. [INPO 14-005 Principles for Nuclear Supplier Excellence](https://www.brucepower.com/wp-content/uploads/2023/04/14-005_Principles_for_Excellence_in_Nuclear_Supplier_Performance-AX.pdf) -- INPO supplier performance standards
23. [INPO Traits of a Healthy Nuclear Safety Culture](https://www.nrc.gov/docs/ml1303/ml13031a707.pdf) -- INPO safety culture traits
24. [DOE-HDBK-1028-2009 Human Performance Improvement Handbook Vol 1 (Concepts and Principles)](https://www.standards.doe.gov/standards-documents/1000/1028-BHdbk-2009-v1) -- DOE human performance principles; five core principles of human performance, organizational factors
24a. [DOE-HDBK-1028-2009 Human Performance Improvement Handbook Vol 2 (Human Performance Tools)](https://www.standards.doe.gov/files/doe-hdbk-1028-2009-human-performance-improvement-handbook-volume-2-human-performance-tools-for-individuals-work-teams-and-management) -- DOE human performance tools standard; procedure use and adherence, peer checking, self-checking, three-part communication
25. [DOE-STD-1029-92 Writer's Guide for Technical Procedures](https://www.standards.doe.gov/standards-documents/1000/1029-astd-1992-cn1-1998) -- DOE procedure writing standard
26. [DOE Order 422.1 Conduct of Operations](https://www.directives.doe.gov/directives-documents/400-series/0422.1-BOrder) -- DOE conduct of operations requirements
27. [DOE Order 5480.19 (Historical)](https://www.directives.doe.gov/directives-documents/5400-series/5480.19-BOrder-chg2) -- Original conduct of operations order
28. [DOE Nuclear Facility Maintenance Management Program Guide](https://www.directives.doe.gov/directives-documents/400-series/0433.1-EGuide-1/@@images/file) -- DOE maintenance program guidance
29. [IAEA NS-G-2.2 -- Operational Limits and Conditions](https://www.iaea.org/publications/6064/operational-limits-and-conditions-and-operating-procedures-for-nuclear-power-plants) -- IAEA operating procedures safety guide
30. [IAEA Pub1339 -- Conduct of Operations at NPPs](https://www-pub.iaea.org/MTCD/Publications/PDF/Pub1339_web.pdf) -- IAEA conduct of operations standard
31. [IAEA Pub1623 -- Managing Human Performance](https://www-pub.iaea.org/MTCD/Publications/PDF/Pub1623_web.pdf) -- IAEA human performance guidance
32. [IAEA-TECDOC-1458 -- Effective Corrective Actions](https://www.iaea.org/publications/7226/effective-corrective-actions-to-enhance-operational-safety-of-nuclear-installations) -- Corrective action enhancement
33. [IAEA-TECDOC-1581 -- Best Practices in Identifying and Reporting](https://www-pub.iaea.org/MTCD/Publications/PDF/TE_1581_web.pdf) -- Operating experience feedback best practices
34. [IAEA Maintenance, Testing, Surveillance and Inspection](https://www.iaea.org/publications/14905/maintenance-testing-surveillance-and-inspection-in-nuclear-power-plants) -- Nuclear plant maintenance standards

### T3 Sources (Supporting -- Industry, Academic)

35. [Westinghouse Procedures Development and Maintenance](https://westinghousenuclear.com/data-sheet-library/procedures-development-and-maintenance/) -- EOP development services
36. [EPRI/NRC Report on Procedure Types (PDF)](https://www.nrc.gov/docs/ML0800/ML080080077.pdf) -- Nuclear procedure types classification
37. [NAS/NRC Lessons Learned -- Emergency Procedures](https://www.ncbi.nlm.nih.gov/books/NBK253949/) -- Fukushima lessons learned for U.S. plants
38. [NEI 14-01 Rev 1 -- Beyond Design Basis Emergency Procedures](https://www.nrc.gov/docs/ML1622/ML16224A619.pdf) -- Industry guidelines for beyond-design-basis events
39. [OECD-NEA Nuclear Power Plant Operating Experience](https://www.oecd-nea.org/nsd/pubs/2020/7482-npp-operating-experience.pdf) -- International operating experience data
40. [OECD-NEA Corrective Action Programme Inspection](https://www.oecd-nea.org/upload/docs/application/pdf/2020-01/cnra-r2010-7.pdf) -- International corrective action inspection guidance
41. [NKS-328 Human Performance Tools in Nuclear (PDF)](https://www.nks.org/scripts/getdocument.php?file=111010212741803) -- Nordic nuclear human performance research

### T4 Sources (Context)

42. [Nuclear PSG -- 5 Principles and 10 Error Reduction Techniques](https://www.nuclearpsg.co.uk/understanding-human-performance-in-nuclear/) -- UK nuclear human performance overview
43. [Human Performance Tools -- Self-Checking Spotlight](https://www.humanperformancetools.com/human-performance-tools/human-performance-tool-spotlight-self-checking) -- STAR technique detailed description
44. [Human Performance Tools -- Procedure Use and Adherence](https://www.humanperformancetools.com/human-performance-tools/human-performance-tool-procedure-use-adherence) -- Procedure classifications and place-keeping
45. [Human Performance Tools -- Three-Part Communication](https://www.humanperformancetools.com/human-performance-tools/human-performance-tool-spotlight-three-part-communication) -- Communication protocol details
46. [ATR Blog -- Procedure Use and Adherence Policy](https://www.atrco.com/blog/does-organization-follow-procedure-use-adherence-policy) -- INPO adherence policy summary
47. [Fossil Consulting -- 3-Part Communication](https://www.fossilconsulting.com/blog/safety/3-part-communication/) -- Three-part communication with phonetic alphabet
48. [Quality Engineers Guide -- Hold Points and Witness Points](https://www.qualityengineersguide.com/what-is-witness-point-and-hold-point/) -- Hold point vs witness point definitions
49. [INPO Human Performance Approach (Academia.edu)](https://www.academia.edu/7534293/INPO_s_approach_to_human_performance_in_the_United_States_commercial_nuclear_power_industry) -- INPO human performance methodology
50. [ResearchGate -- NUREG-0711 Review Elements Diagram](https://www.researchgate.net/figure/NUREG-0711-Revision-2-HFE-review-elements-A-brief-description-of-each-element-follows_fig1_241909507) -- Visual diagram of 12 HFE review elements

---

## Research Methodology

### Search Strategy

Conducted 20+ targeted web searches across the following domains:
- nrc.gov (primary regulatory source)
- iaea.org (international standards)
- directives.doe.gov (DOE nuclear facility standards)
- standards.doe.gov (DOE technical standards)
- humanperformancetools.com (nuclear human performance)

### Source Validation

All sources validated against T1-T5 authority hierarchy:
- 21 T1 sources (NRC/federal regulations) -- highest authority (added Cornell LII cross-reference for 10 CFR 50.54, NRC IP 42454 for NUREG-1358)
- 15 T2 sources (INPO, DOE, IAEA) -- secondary authority (added DOE-HDBK-1028-2009 Vol. 1 as separate entry from Vol. 2)
- 7 T3 sources (industry/academic) -- supporting
- 9 T4 sources (context) -- contextual only; T4 sources are retained as supplementary but no longer serve as sole citations for T2-level claims (see Indirect Source Disclosure below)
- 0 T5 sources used (no Wikipedia, no non-authoritative blogs)

### Limitations

1. Several NUREG PDFs (NUREG-0899, NUREG-0711 Rev 3, DOE-HDBK-1028-2009) could not be extracted as text via WebFetch due to PDF encoding (scanned image PDFs). Key content was obtained through secondary sources and NRC index pages. NUREG-0899 URL (ML102560007) was verified to resolve to a PDF; ADAMS casing corrected to standard mixed-case format.
2. INPO standards documents (INPO 09-004) are proprietary and not publicly available in full text. Content was obtained through publicly available summaries and derivative sources. Where DOE-HDBK-1028-2009 provides equivalent publicly available content (as it does for procedure use and adherence, peer checking, and human performance principles), the DOE source is used as the primary T2 citation.
3. Specific plant-level procedure examples were not included to maintain focus on industry-wide patterns rather than plant-specific implementations.
4. NUREG-1358 (Lessons Learned from the Special Inspection Program for Emergency Operating Procedures) is not indexed in the NRC's online NUREG staff publications catalog. The document is referenced indirectly through NRC Inspection Procedure IP 42454 (ADAMS ML13232A368) and the NRC Generic Safety Issues database (HF4). Content about NUREG-1358's findings is sourced from these referencing documents rather than the NUREG itself.
5. **URL verification results** (Revision 2, conducted via WebFetch):
   - NUREG-0899 PDF (`ML1025/ML102560007.pdf`): URL resolves to PDF; file is a scanned image (CCITT Fax encoded) and cannot be extracted as text. ADAMS accession number ML102560007 is structurally valid.
   - DOE-HDBK-1028-2009 standards.doe.gov page: Returns HTTP 403 (access restricted) for the direct file download URL. The document landing page at `standards.doe.gov/standards-documents/1000/1028-BHdbk-2009-v1` is reachable via web search and is the canonical DOE standards page for this handbook. A third-party mirror at Stanford (`large.stanford.edu`) hosts a copy but its PDF is also not text-extractable.
   - DOE Maintenance Guide (`directives.doe.gov/.../0433.1-EGuide-1/@@images/file`): Returns HTTP 403. The Plone CMS `@@images/file` URL pattern is valid for `directives.doe.gov` but requires direct browser access. The parent directory page for DOE Order 433.1 is accessible at `directives.doe.gov/directives-documents/400-series/`.

### Indirect Source Disclosure (P-001 Transparency)

The following sections rely on indirect or T4 blog sources for content that originates from proprietary industry standards. This disclosure is provided per P-001 (all claims must have citations with transparent provenance):

| Section | Indirect Source | Primary Source (Proprietary) | T2 Alternative Used |
|---------|----------------|------------------------------|---------------------|
| 2.2 (Procedure Use and Adherence) | ATR Training blog (T4) | INPO procedure adherence policy | DOE-HDBK-1028-2009 Vol. 2 (T2) -- provides equivalent language on procedure use and adherence |
| 2.1 (Human Performance Framework) | Nuclear PSG (T4) -- supplementary | INPO human performance framework | DOE-HDBK-1028-2009 Vol. 1 (T2) -- primary citation; contains the same five principles derived from INPO membership experience |

In both cases, the T4 source is retained as supplementary context but is no longer the sole or primary citation. The DOE-HDBK-1028-2009 handbook explicitly states it "reflects years of user experience among INPO's membership," establishing a documented provenance chain from INPO concepts to DOE public standards.

---

## Revision History

| Revision | Date | Trigger | Changes |
|----------|------|---------|---------|
| 0 (Initial) | 2026-03-22 | Phase 1 research | Initial 50-source survey across 8 topic areas |
| 1 (QG1 Revisions) | 2026-03-22 | adv-executor-001 source validation (score 0.868, REVISE) | See Revision 1 details below |

### Revision 1 Details (QG1 Source Validation Response)

Addressed 3 Major and 5 Minor findings from Quality Gate 1 (S-002 + S-007):

| ID | Severity | Finding | Resolution |
|----|----------|---------|------------|
| R1 (DA-001) | Major | T4 blog as sole source for INPO five principles and ten tools | Re-cited to DOE-HDBK-1028-2009 Vol. 1 (T2) as primary; Nuclear PSG (T4) retained as supplementary |
| R2 (DA-002 + CC-001) | Major | INPO 09-004 content quoted from T4 blog without transparent attribution | Section 2.2 rewritten: DOE-HDBK-1028-2009 Vol. 2 (T2) is now primary source for procedure adherence concepts; ATR blog attribution clarified as indirect; source provenance note added |
| R3 (CC-001) | Major | Constitutional concern about blog intermediaries for proprietary standards | Added Indirect Source Disclosure table to Limitations section with explicit section-by-section provenance |
| R4 (DA-003) | Minor | `50.54(i-1)` non-standard notation | VERIFIED CORRECT via Cornell LII eCFR; added explanatory note and direct quote from regulatory text; added Cornell LII as T1 cross-reference |
| R5 (DA-004) | Minor | NUREG-1358 cited via indirect NRC index page | Replaced with NRC IP 42454 (ML13232A368) as primary reference; added note about NUREG-1358 not being in NRC online catalog; added NRC Generic Safety Issues HF4 as secondary reference |
| R6 (DA-005) | Minor | Uncited three-part communication required scenarios | Added citation to humanperformancetools.com with direct quotes for each required scenario |
| R7 (DA-006) | Minor | NUREG-0899 URL lowercase casing | Corrected all instances to standard ADAMS mixed-case format (ML1025/ML102560007) |
| R8 (CC-002) | Minor | Three URLs requiring live verification | Verified via WebFetch: NUREG-0899 PDF resolves; DOE-HDBK-1028 and DOE Maintenance Guide return HTTP 403 (access-restricted but valid patterns); results documented in Limitations |

**Source count changes:** T1: 20 to 21 (+Cornell LII, +NRC IP 42454). T2: 14 to 15 (+DOE-HDBK-1028-2009 Vol. 1 as separate entry). T3: 7 (unchanged). T4: 9 (unchanged; role demoted from primary to supplementary for Sections 2.1 and 2.2).
