# WI-SAO-047: NASA SE + INCOSE Research

**Work Item:** WI-SAO-047
**Initiative:** SAO-INIT-008 (Agent/Skill Enhancement)
**Status:** COMPLETE
**Date:** 2026-01-12
**Researcher:** Claude Opus 4.5 (Subagent)

---

## Executive Summary

This research document compiles NASA Systems Engineering best practices and INCOSE standards applicable to agent documentation and workflow design. Key findings include:

1. **NASA's Gate-Based Review Process** provides a robust framework for technical review and decision-making that can inform agent validation workflows
2. **The SE Engine** (17 common technical processes) offers a reusable pattern for iterative development cycles
3. **RFA/RID Process** establishes a formal mechanism for capturing, tracking, and dispositioning review feedback - directly applicable to agent quality assurance
4. **INCOSE's Requirements Engineering** standards provide traceability and verification patterns suitable for agent capability documentation
5. **Model-Based Systems Engineering (MBSE)** principles align with Jerry's filesystem-as-memory approach for persistent state management

### Key Recommendations for Agent Enhancement

| NASA/INCOSE Pattern | Jerry Application |
|---------------------|-------------------|
| Technical Reviews (SRR/PDR/CDR) | Agent capability maturity gates |
| RFA/RID Process | Feedback capture and resolution tracking |
| SE Engine cycles | Iterative agent improvement workflow |
| Entry/Exit Criteria | Agent deployment readiness checklist |
| Standing Review Board | Multi-agent validation workflow |
| Requirements Traceability | Capability-to-test mapping |

---

## 1. NASA SE Lifecycle

### 1.1 Lifecycle Phases

NASA structures space flight programs into two major phases divided into seven incremental stages:

#### Formulation Phase
- **Pre-Phase A (Concept Studies):** Produce broad spectrum of ideas and alternatives for missions
- **Phase A (Concept & Technology Development):** Determine feasibility of suggested new system
- **Phase B (Preliminary Design):** Develop and define project requirements and cost/schedule basis

#### Implementation Phase
- **Phase C (Final Design & Fabrication):** Complete final system design and fabrication
- **Phase D (System Assembly, Integration, Test, Launch):** AI&T, verification, certification
- **Phase E (Operations & Sustainment):** Ensure certified system is ready for operations
- **Phase F (Closeout):** Dispose of system in responsible manner

**Applicability to Agent Enhancement:**
| NASA Phase | Agent Equivalent |
|------------|------------------|
| Pre-Phase A | Agent concept/need identification |
| Phase A | Capability feasibility assessment |
| Phase B | Agent design specification |
| Phase C | Implementation and unit testing |
| Phase D | Integration testing and deployment |
| Phase E | Production operation |
| Phase F | Agent deprecation/replacement |

### 1.2 Technical Reviews

NASA defines mandatory technical reviews with specific entrance and success criteria:

| Review | Name | Purpose |
|--------|------|---------|
| **MCR** | Mission Concept Review | Evaluate mission concept, objectives, and feasibility |
| **SRR** | System Requirements Review | Ensure requirements and concept satisfy mission |
| **SDR** | System Design Review | Examine proposed system architecture and design |
| **PDR** | Preliminary Design Review | Verify preliminary design meets requirements |
| **CDR** | Critical Design Review | Confirm design maturity for full-scale fabrication |
| **PRR** | Production Readiness Review | Validate manufacturing readiness |
| **TRR** | Test Readiness Review | Confirm readiness to begin formal testing |
| **ORR** | Operational Readiness Review | Verify system ready for operations |
| **FRR** | Flight Readiness Review | Final go/no-go for launch |

**Key Principle:** Each gate answers a simple question - "Are we ready to move to the next irreversible step with the right evidence?"

### 1.3 Entry/Exit Criteria

NASA NPR 7123.1 defines detailed entrance and success criteria for each review. Key elements include:

**Review Entrance Criteria:**
- All prerequisite documentation complete
- Design artifacts available to reviewers in advance
- Risk assessments current
- Previous review actions closed

**Review Success Criteria:**
- Agreement on disposition of all RIDs and RFAs
- Review board report and minutes complete
- Adequate plan for addressing identified issues
- Differences of opinion resolved or escalation plan exists

**Review Completion:**
Reviews are considered complete when:
1. All RIDs and RFAs dispositioned
2. Review board report distributed
3. Liens closed or closure plan exists
4. Report given to appropriate management

---

## 2. NPR 7123.1 Process Areas

### 2.1 Technical Management Processes

NPR 7123.1 defines the "SE Engine" - 17 common technical processes used throughout the lifecycle:

**Technical Management (Processes 10-17):**
1. Technical Planning
2. Requirements Development
3. Technical Assessment
4. Technical Control
5. Technical Decision Analysis
6. Technical Data Management
7. Configuration Management
8. Risk Management

### 2.2 Technical Planning

Key elements of technical planning per NPR 7123.1:

- **Systems Engineering Management Plan (SEMP):** Establishes technical content early in Formulation
- Updated throughout project lifecycle
- Describes what processes will be used
- Defines how project will be organized
- Establishes cost and schedule for activities

**SEMP Contents:**
- Technical approach and processes
- Organization structure
- Resource allocation
- Schedule and milestones
- Risk management approach

### 2.3 Requirements Development

NPR 7123.1 requirements approach emphasizes:

- **Systematic** - disciplined engineering approach
- **Quantifiable** - measurable and verifiable
- **Recursive** - applied at all hierarchical levels
- **Iterative** - refined through lifecycle phases
- **Repeatable** - consistent application across projects

**Requirements Artifacts:**
- Stakeholder expectations analysis
- Requirements allocation
- Requirements verification matrix
- Traceability documentation

### 2.4 Technical Assessment

Technical assessment processes include:

- **Product Verification:** Confirm products meet requirements
- **Product Validation:** Confirm products meet stakeholder needs
- **Technical Reviews:** Gate-based maturity assessment
- **Progress Measurement:** Track technical completion status

---

## 3. INCOSE Standards

### 3.1 SE Process Models

The INCOSE Systems Engineering Handbook (5th Edition, 2023) builds upon ISO/IEC/IEEE 15288:2023 with additional context and practical applications.

**Life Cycle Model Approaches:**
1. **Sequential Methods:** Traditional waterfall-style progression
2. **Incremental Methods:** Functionality delivered in increments
3. **Evolutionary Methods:** Progressive refinement based on feedback

**ISO/IEC/IEEE 15288:2023 Process Groups:**

| Process Group | Key Processes |
|---------------|---------------|
| Agreement | Acquisition, Supply |
| Organizational | Life Cycle Model Management, Infrastructure, Portfolio, HR, Quality, Knowledge Management |
| Technical Management | Planning, Assessment, Decision Management, Risk, Configuration |
| Technical | Stakeholder Needs, Requirements, Architecture, Design, Integration, Verification, Validation, Transition, Operation, Maintenance, Disposal |

### 3.2 Requirements Engineering

INCOSE Requirements Working Group (RWG) publications:

1. **Needs and Requirements Manual (NRM):** Comprehensive lifecycle coverage
2. **Guide to Needs and Requirements (GtNR):** Practical application
3. **Guide to Verification and Validation (GtVV):** V&V guidance
4. **Guide to Writing Requirements (GtWR):** Quality requirements

**Characteristics of Good Requirements (INCOSE):**

| Characteristic | Description |
|----------------|-------------|
| **Necessary** | Directly tied to stakeholder or system needs |
| **Clear** | Written in plain language, avoiding vague terms |
| **Feasible** | Technically and economically achievable |
| **Verifiable** | Measurable through inspection, analysis, demonstration, or testing |
| **Traceable** | Linked to higher-level requirements and downstream elements |

**Requirements Traceability:**
- Many standards require traceability across lifecycle
- Link requirements to design elements, test cases, verification activities
- Maintain bidirectional traceability (up and down)

### 3.3 V&V Patterns

**Verification vs. Validation (INCOSE):**

| Aspect | Verification | Validation |
|--------|--------------|------------|
| Focus | Form - did we build it right? | Fit - did we build the right thing? |
| Activity | Confirm products meet requirements | Confirm products meet stakeholder needs |
| Methods | Inspection, Analysis, Demonstration, Test | Prototyping, Reviews, User acceptance |

**Verification Methods:**
1. **Inspection:** Visual examination of artifacts
2. **Analysis:** Mathematical/analytical evaluation
3. **Demonstration:** Functional exercise of capability
4. **Test:** Controlled exercise with measurable results

**Validation Activities:**
- Requirements reviews for correctness, completeness, consistency
- Prototyping to confirm interpretations
- Concept of operations validation
- User acceptance testing

---

## 4. Review-Revise Pattern

### 4.1 RFA/RID Process

NASA uses Review Item Discrepancies (RIDs) and Requests for Action (RFAs) to capture and track review feedback.

**Definitions:**
- **RID (Review Item Discrepancy):** Item not compliant with requirement, objective, or design goal
- **RFA (Request for Action):** Action item requiring project response

**Process Flow:**
```
Review → Identify Issues → Create RID/RFA → Classify → Disposition → Close
                             ↑                          ↓
                             └──────── Iterate ─────────┘
```

**Classification Levels:**
| Level | Definition |
|-------|------------|
| **Mission Critical** | Failure to correct could cause mission failure |
| **Major** | Significant impact but unlikely to cause mission failure |
| **Minor** | Causes only minor impacts |

**Disposition Options:**
1. **Accept As-Is:** Issue is valid but no action required
2. **Accept with Modification:** Implement modified solution
3. **Reject:** Issue not valid or out of scope
4. **Defer:** Address in later phase

### 4.2 Gate-Based Reviews

NASA's TechSG process employs decision gates with four possible outcomes:

| Decision | Description |
|----------|-------------|
| **Continue** | Proceed to next phase as planned |
| **Redirect** | Proceed with modified approach |
| **Hold** | Pause until conditions met |
| **Terminate** | Stop development |

**Gate Review Principles:**
1. Management reviews and technical reviews support one another
2. Technical reviews completed before management decision gate
3. Reviews occur relative to technical maturity, not calendar milestones
4. Clear objectives and entrance/exit criteria established upfront

**Contrast with Iterative Approaches:**
- Gate-based: Linear progression with checkpoints
- Iterative: Cycles of development and feedback
- NASA uses both: Gates for major milestones, iteration within phases

### 4.3 Applicability to Agent Enhancement

**Mapping to Generator-Critic Pattern:**

| NASA Pattern | Generator-Critic Equivalent | Notes |
|--------------|----------------------------|-------|
| Generator produces artifact | Generator agent creates output | Same concept |
| Review board reviews | Critic agent evaluates | Multi-agent review possible |
| RID/RFA created | Feedback captured | Structured feedback format |
| Disposition decision | Iteration decision | Continue/Revise/Accept |
| Artifact baseline | Output finalized | Gate passage |

**Review-Revise as Alternative:**
The NASA Review-Revise pattern offers advantages over pure Generator-Critic:

1. **Structured Feedback:** RIDs capture specific issues with classification
2. **Decision Authority:** Clear ownership of disposition decisions
3. **Audit Trail:** Complete history of issues and resolutions
4. **Escalation Path:** Formal dissent process for disagreements

**Proposed Agent Review Workflow:**
```
┌─────────────────────────────────────────────────────────────┐
│                    AGENT REVIEW PROCESS                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐               │
│  │ Generate │───►│  Review  │───►│ Dispose  │               │
│  │ Artifact │    │ (Create  │    │ RIDs     │               │
│  └──────────┘    │  RIDs)   │    └────┬─────┘               │
│       ▲          └──────────┘         │                     │
│       │                               │                     │
│       │      ┌────────────────────────┘                     │
│       │      │                                              │
│       │      ▼                                              │
│       │  ┌───────────────────────────────────┐              │
│       │  │ Disposition Decision:              │              │
│       │  │ ┌─────────┐ ┌────────┐ ┌────────┐ │              │
│       │  │ │ Accept  │ │ Revise │ │ Reject │ │              │
│       │  │ └────┬────┘ └───┬────┘ └───┬────┘ │              │
│       │  └──────┼──────────┼──────────┼──────┘              │
│       │         │          │          │                     │
│       │         ▼          │          ▼                     │
│       │    ┌────────┐      │     ┌────────┐                 │
│       └────│ Update │◄─────┘     │  Log   │                 │
│            │Artifact│            │ Close  │                 │
│            └────────┘            └────────┘                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Applicability to Agent Documentation

### 5.1 Agent Capability Maturity Gates

Apply NASA technical reviews to agent development:

| Agent Gate | NASA Equivalent | Entry Criteria | Success Criteria |
|------------|-----------------|----------------|------------------|
| Concept Review | MCR | Need identified, stakeholders defined | Concept feasible, resources identified |
| Requirements Review | SRR | Capabilities documented | Requirements complete, verifiable |
| Design Review | PDR | Architecture defined | Design meets requirements |
| Implementation Review | CDR | Code complete | Tests pass, integration verified |
| Deployment Review | ORR | Testing complete | Ready for production use |

### 5.2 Agent Documentation Structure

Apply INCOSE requirements engineering to agent documentation:

**Agent Specification Document:**
```markdown
# Agent: {Name}

## 1. Purpose and Stakeholders
- Mission/purpose statement
- Stakeholder needs analysis

## 2. Capabilities (Requirements)
- CAP-001: {Capability with verification method}
- CAP-002: ...

## 3. Constraints
- Technical constraints
- Resource constraints

## 4. Interfaces
- Input interfaces
- Output interfaces
- Dependencies

## 5. Verification Matrix
| Capability | Method | Status |
|------------|--------|--------|

## 6. Traceability
- Links to higher-level requirements
- Links to implementation
- Links to test cases
```

### 5.3 Agent Quality Assurance Process

Implement RFA/RID-style feedback capture:

**Agent Review Item Format:**
```yaml
rid_id: ARI-{agent}-{sequence}
reviewer: {agent_id or human}
severity: critical | major | minor
category: capability | interface | documentation | behavior
description: |
  Clear description of the issue
recommendation: |
  Suggested resolution
disposition: pending | accepted | rejected | deferred
resolution: |
  How the issue was addressed
```

### 5.4 Jerry-Specific Applications

**Work Item Tracking Enhancement:**
- Add SE-style review milestones to work items
- Track RIDs/RFAs as linked artifacts
- Implement entry/exit criteria for state transitions

**Agent Constitution Alignment:**
- P-001 (Truth and Accuracy) → Verification requirements
- P-002 (File Persistence) → Configuration management
- P-010 (Task Tracking Integrity) → Technical assessment
- P-022 (No Deception) → Validation with stakeholders

**Orchestration Skill Enhancement:**
- Apply Standing Review Board pattern to multi-agent workflows
- Implement gate-based checkpoints for complex workflows
- Use RFA/RID for inter-agent feedback

---

## 6. Sources

### NASA Documents
- [NASA Systems Engineering Handbook (SP-6105)](https://www.nasa.gov/reference/systems-engineering-handbook/)
- [NPR 7123.1C - NASA Systems Engineering Processes and Requirements](https://nodis3.gsfc.nasa.gov/displayAll.cfm?Internal_ID=N_PR_7123_001C_&page_name=all)
- [NPR 7123.1D - Appendix G Technical Review Criteria](https://nodis3.gsfc.nasa.gov/displayDir.cfm?Internal_ID=N_PR_7123_001D_&page_name=AppendixG)
- [NASA Standing Review Board Handbook](https://ntrs.nasa.gov/citations/20230001306)
- [NASA SE Lifecycle Phases](https://www.nasa.gov/reference/3-0-nasa-program-project-life-cycle/)
- [NASA SE Engine Overview](https://www.nasa.gov/reference/2-2-an-overview-of-the-se-engine-by-project-phase/)
- [NASA RID Processing Procedure](http://mae-nas.eng.usu.edu/MAE_5900_Web/5900/USLI_2010/PDF_files/NASA_RID_procedure.pdf)
- [NASA Decision Gate Process](https://ntrs.nasa.gov/api/citations/20120013467/downloads/20120013467.pdf)

### INCOSE Documents
- [INCOSE Systems Engineering Handbook 5th Edition](https://www.incose.org/publications/products/se-handbook-v4)
- [INCOSE SE Handbook - SEBoK Reference](https://sebokwiki.org/wiki/INCOSE_Systems_Engineering_Handbook)
- [INCOSE MBSE Initiative](https://www.incose.org/communities/working-groups-initiatives/mbse-initiative)
- [INCOSE Guide to MBSE](https://visuresolutions.com/alm-guide/incose-guide-to-mbse/)
- [INCOSE Requirements Working Group](https://www.incose.org/communities/working-groups-initiatives/requirements)
- [INCOSE Guide to Writing Requirements](https://visuresolutions.com/alm-guide/incose-guide-to-writing-requirements/)
- [INCOSE V&V Guidance](https://www.incose.org/docs/default-source/los-angeles/2024-06_vnv_across_lifecycle.pdf)
- [INCOSE Traceability Presentation](https://www.incose.org/docs/default-source/working-groups/requirements-wg/monthlymeetings2024/traceability_110524.pdf)

### Standards
- [ISO/IEC/IEEE 15288:2023 - System Life Cycle Processes](https://www.iso.org/standard/81702.html)
- [ISO/IEC/IEEE 15288 - SEBoK Reference](https://sebokwiki.org/wiki/ISO/IEC/IEEE_15288)

### Industry Analysis
- [Jama Software - NASA SE Handbook Analysis](https://www.jamasoftware.com/blog/unveiling-the-nasa-systems-engineering-handbook-rev2-a-comprehensive-guide-for-space-exploration/)
- [Space Project Milestones Decoded](https://anywaves.com/resources/blog/space-project-milestones-a-practical-guide/)
- [Wikipedia - Design Review (US Government)](https://en.wikipedia.org/wiki/Design_review_(U.S._government))
- [Wikipedia - MBSE](https://en.wikipedia.org/wiki/Model-based_systems_engineering)

---

## Appendix A: NASA Technical Review Quick Reference

### Review Sequence
```
Pre-Phase A: MCR
Phase A:     SRR → MDR
Phase B:     PDR
Phase C:     CDR → PRR
Phase D:     TRR → ORR → FRR
Phase E:     Periodic Reviews
Phase F:     Disposal Readiness Review
```

### Entry/Exit Criteria Template

**Review Entry Criteria:**
- [ ] Previous review actions closed
- [ ] Required documentation complete and distributed
- [ ] Risk register current
- [ ] Resource availability confirmed

**Review Success Criteria:**
- [ ] All RIDs/RFAs dispositioned
- [ ] Review board report complete
- [ ] Action plan agreed
- [ ] Decision memorandum signed

---

## Appendix B: INCOSE Requirements Checklist

### Individual Requirement Quality
- [ ] Necessary - traces to stakeholder need
- [ ] Unambiguous - single interpretation
- [ ] Complete - no missing information
- [ ] Singular - addresses one thing
- [ ] Feasible - achievable within constraints
- [ ] Verifiable - can be tested/demonstrated
- [ ] Correct - accurately represents need
- [ ] Conforming - follows standard format

### Requirements Set Quality
- [ ] Complete - covers all capabilities
- [ ] Consistent - no conflicts between requirements
- [ ] Feasible - achievable as a set
- [ ] Comprehensible - can be understood by all stakeholders
- [ ] Able to be validated - can confirm right system built

---

*Document generated by WI-SAO-047 research task*
*Part of SAO-INIT-008: Agent/Skill Enhancement Initiative*
