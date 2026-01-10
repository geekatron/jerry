# NASA SE Process Mapping to Jerry Framework

> **Document ID:** NASA-SE-MAPPING
> **Version:** 1.0.0
> **Date:** 2026-01-09
> **Standard:** NPR 7123.1D (17 Common Technical Processes)

---

## Overview

This document maps NASA's 17 Common Technical Processes (NPR 7123.1D) to the Jerry Framework's NASA SE skill agents, tools, and artifacts.

---

## Process-to-Agent Mapping Matrix

| # | NASA Process | NPR Section | NSE Agent | Jerry Integration |
|---|--------------|-------------|-----------|-------------------|
| 1 | Stakeholder Expectations Definition | 3.2.1 | `nse-requirements` | Work Tracker items |
| 2 | Technical Requirements Definition | 3.2.2 | `nse-requirements` | `requirements/` artifacts |
| 3 | Logical Decomposition | 3.2.3 | `nse-architecture` | `architecture/` artifacts |
| 4 | Design Solution Definition | 3.2.4 | `nse-architecture` | ADR format |
| 5 | Product Implementation | 3.3.1 | (External) | Code artifacts |
| 6 | Product Integration | 3.3.2 | `nse-integration` | `integration/` artifacts |
| 7 | Product Verification | 3.3.3 | `nse-verification` | `verification/` artifacts |
| 8 | Product Validation | 3.3.4 | `nse-verification` | `verification/` artifacts |
| 9 | Product Transition | 3.3.5 | `nse-reporter` | Status reports |
| 10 | Technical Planning | 3.4.1 | `nse-reporter` | PLAN.md integration |
| 11 | Requirements Management | 3.4.2 | `nse-requirements` | Traceability matrices |
| 12 | Interface Management | 3.4.3 | `nse-integration` | ICD artifacts |
| 13 | Technical Risk Management | 3.4.4 | `nse-risk` | `risks/` artifacts |
| 14 | Configuration Management | 3.4.5 | `nse-configuration` | `configuration/` artifacts |
| 15 | Technical Data Management | 3.4.6 | `nse-configuration` | Knowledge artifacts |
| 16 | Technical Assessment | 3.4.7 | `nse-reporter` | `reports/` artifacts |
| 17 | Decision Analysis | 3.4.8 | `nse-architecture` | Trade study artifacts |

---

## Detailed Process Mappings

### System Design Processes (1-4)

#### Process 1: Stakeholder Expectations Definition

| Attribute | NASA Definition | Jerry Implementation |
|-----------|-----------------|---------------------|
| **Purpose** | Identify stakeholders, elicit expectations, transform into requirements | `nse-requirements` agent |
| **Inputs** | Mission objectives, constraints, interfaces | Work Tracker items, project PLAN.md |
| **Outputs** | Stakeholder needs baseline | `requirements/{proj}-{entry}-stakeholder-needs.md` |
| **Activities** | Identify stakeholders, elicit needs, prioritize | Agent prompts for stakeholder analysis |
| **Work Products** | Stakeholder register, needs statements | Markdown artifacts with traceability |

**Jerry Mapping:**
```
User: "Identify stakeholder needs for the authentication module"
Agent: nse-requirements
Output: projects/PROJ-002/requirements/proj-002-e-XXX-stakeholder-needs.md
Format: Stakeholder → Need → Priority → Trace-to-Requirement
```

---

#### Process 2: Technical Requirements Definition

| Attribute | NASA Definition | Jerry Implementation |
|-----------|-----------------|---------------------|
| **Purpose** | Transform stakeholder expectations into technical requirements | `nse-requirements` agent |
| **Inputs** | Stakeholder needs, constraints, standards | Previous stakeholder analysis |
| **Outputs** | Technical requirements baseline | `requirements/{proj}-{entry}-requirements-spec.md` |
| **Activities** | Define requirements, allocate, verify quality | Agent requirements engineering |
| **Work Products** | Requirements specification, rationale | Formal "shall" statements |

**Requirement Format (NASA-HDBK-1009A):**
```markdown
| ID | Requirement | Rationale | Parent | Verification | Status |
|----|-------------|-----------|--------|--------------|--------|
| REQ-001 | The system shall authenticate users within 2 seconds | Performance constraint | STK-003 | Test | Draft |
```

**Jerry Mapping:**
```
User: "Create requirements for user authentication"
Agent: nse-requirements
Output: projects/PROJ-002/requirements/proj-002-e-XXX-auth-requirements.md
Format: ID, Shall-statement, Rationale, Parent-trace, V-method
```

---

#### Process 3: Logical Decomposition

| Attribute | NASA Definition | Jerry Implementation |
|-----------|-----------------|---------------------|
| **Purpose** | Decompose system into logical components | `nse-architecture` agent |
| **Inputs** | Technical requirements, constraints | Requirements baseline |
| **Outputs** | Logical architecture, function allocation | `architecture/{proj}-{entry}-decomposition.md` |
| **Activities** | Identify functions, allocate to components | Functional analysis |
| **Work Products** | Functional hierarchy, N² diagram | Architecture artifacts |

**Jerry Mapping:**
```
User: "Decompose the API service into logical components"
Agent: nse-architecture
Output: projects/PROJ-002/architecture/proj-002-e-XXX-logical-decomposition.md
Format: Function hierarchy, component allocation, interface identification
```

---

#### Process 4: Design Solution Definition

| Attribute | NASA Definition | Jerry Implementation |
|-----------|-----------------|---------------------|
| **Purpose** | Define physical design solution | `nse-architecture` agent |
| **Inputs** | Logical architecture, design constraints | Decomposition artifacts |
| **Outputs** | Design specification, drawings | `architecture/{proj}-{entry}-design-spec.md` |
| **Activities** | Trade studies, design synthesis, design verification | Trade study process |
| **Work Products** | Design documents, trade studies | ADR format artifacts |

**Trade Study Format:**
```markdown
## Trade Study: {Decision}

### Alternatives
| Option | Description | Pros | Cons |
|--------|-------------|------|------|

### Evaluation Criteria
| Criterion | Weight | Option A | Option B | Option C |
|-----------|--------|----------|----------|----------|

### Recommendation
{Selected option with rationale}
```

**Jerry Mapping:**
```
User: "Trade study: SQL vs NoSQL for audit logs"
Agent: nse-architecture
Output: projects/PROJ-002/architecture/proj-002-e-XXX-trade-sql-nosql.md
Format: ADR with trade study matrix
```

---

### Product Realization Processes (5-9)

#### Process 5: Product Implementation

| Attribute | NASA Definition | Jerry Implementation |
|-----------|-----------------|---------------------|
| **Purpose** | Build or code the product | External (code artifacts) |
| **Inputs** | Design specifications | Architecture artifacts |
| **Outputs** | Implemented product | Source code |
| **Note** | This process is external to NSE agents | Developer responsibility |

**Jerry Integration:**
- NSE agents provide requirements and design inputs
- Code implementation is external to NASA SE skill
- `nse-verification` validates implementation against requirements

---

#### Process 6: Product Integration

| Attribute | NASA Definition | Jerry Implementation |
|-----------|-----------------|---------------------|
| **Purpose** | Integrate components into assemblies | `nse-integration` agent |
| **Inputs** | Implemented products, ICDs | Code + interface docs |
| **Outputs** | Integrated system, integration evidence | `integration/{proj}-{entry}-integration.md` |
| **Activities** | Plan integration, execute, verify interfaces | Integration verification |
| **Work Products** | Integration plan, ICD, integration reports | Markdown artifacts |

**ICD Format:**
```markdown
## Interface Control Document: {Interface Name}

### Interface Identification
| Attribute | Value |
|-----------|-------|
| Interface ID | IF-001 |
| Provider | {Component A} |
| Consumer | {Component B} |

### Interface Specification
| Parameter | Type | Direction | Format | Constraints |
|-----------|------|-----------|--------|-------------|
```

**Jerry Mapping:**
```
User: "Create ICD for frontend-backend API interface"
Agent: nse-integration
Output: projects/PROJ-002/integration/proj-002-e-XXX-icd-api.md
Format: Interface ID, endpoints, data formats, constraints
```

---

#### Process 7: Product Verification

| Attribute | NASA Definition | Jerry Implementation |
|-----------|-----------------|---------------------|
| **Purpose** | Verify product meets requirements | `nse-verification` agent |
| **Inputs** | Requirements, product, test plans | Requirements baseline + code |
| **Outputs** | Verification evidence, VCRM | `verification/{proj}-{entry}-vcrm.md` |
| **Activities** | Plan V&V, execute tests, collect evidence | VCRM management |
| **Work Products** | Test procedures, VCRM, test reports | Verification artifacts |

**VCRM Format (Verification Cross-Reference Matrix):**
```markdown
| Req ID | Requirement | V-Method | V-Level | Procedure | Status | Evidence |
|--------|-------------|----------|---------|-----------|--------|----------|
| REQ-001 | The system shall... | Test | System | TP-001 | Pass | TR-001 |
```

**Verification Methods:**
- **Analysis (A):** Mathematical or analytical techniques
- **Demonstration (D):** Observation of operation
- **Inspection (I):** Visual examination
- **Test (T):** Execution against criteria

**Jerry Mapping:**
```
User: "Generate VCRM for authentication requirements"
Agent: nse-verification
Output: projects/PROJ-002/verification/proj-002-e-XXX-vcrm-auth.md
Format: Req-to-test trace, verification method, status, evidence
```

---

#### Process 8: Product Validation

| Attribute | NASA Definition | Jerry Implementation |
|-----------|-----------------|---------------------|
| **Purpose** | Validate product meets intended use | `nse-verification` agent |
| **Inputs** | Stakeholder needs, integrated product | Needs baseline + system |
| **Outputs** | Validation evidence | `verification/{proj}-{entry}-validation.md` |
| **Activities** | Plan validation, execute, collect evidence | Validation activities |
| **Work Products** | Validation plan, validation reports | Validation artifacts |

**Jerry Mapping:**
```
User: "Create validation plan for user acceptance"
Agent: nse-verification
Output: projects/PROJ-002/verification/proj-002-e-XXX-validation-plan.md
Format: Need-to-validation trace, acceptance criteria, evidence
```

---

#### Process 9: Product Transition

| Attribute | NASA Definition | Jerry Implementation |
|-----------|-----------------|---------------------|
| **Purpose** | Transition product to operations | `nse-reporter` agent |
| **Inputs** | Validated product, transition plan | V&V evidence + plan |
| **Outputs** | Transitioned product, ORR evidence | `reports/{proj}-{entry}-transition.md` |
| **Activities** | Prepare operations, train users, deploy | Transition planning |
| **Work Products** | Transition plan, training materials | Transition artifacts |

**Jerry Mapping:**
```
User: "Prepare transition report for production deployment"
Agent: nse-reporter
Output: projects/PROJ-002/reports/proj-002-e-XXX-transition-report.md
Format: Readiness assessment, transition checklist, issues
```

---

### Technical Management Processes (10-17)

#### Process 10: Technical Planning

| Attribute | NASA Definition | Jerry Implementation |
|-----------|-----------------|---------------------|
| **Purpose** | Establish and maintain SE plan | `nse-reporter` agent |
| **Inputs** | Project requirements, constraints | Project PLAN.md |
| **Outputs** | Systems Engineering Management Plan | `reports/{proj}-{entry}-semp.md` |
| **Activities** | Define SE approach, resources, schedule | Planning activities |
| **Work Products** | SEMP, WBS, resource plans | Planning artifacts |

**Jerry Mapping:**
```
User: "Generate SE management plan for Phase 2"
Agent: nse-reporter
Output: projects/PROJ-002/reports/proj-002-e-XXX-semp.md
Format: SE approach, processes, resources, schedule
```

---

#### Process 11: Requirements Management

| Attribute | NASA Definition | Jerry Implementation |
|-----------|-----------------|---------------------|
| **Purpose** | Manage requirements throughout lifecycle | `nse-requirements` agent |
| **Inputs** | Requirements baseline, changes | Existing requirements |
| **Outputs** | Updated baseline, traceability | `requirements/{proj}-{entry}-trace-matrix.md` |
| **Activities** | Track requirements, manage changes, trace | Traceability management |
| **Work Products** | Requirements database, traceability matrix | Traceability artifacts |

**Traceability Matrix Format:**
```markdown
| Parent ID | Requirement ID | Child ID | V&V Method | Status |
|-----------|----------------|----------|------------|--------|
| STK-001 | REQ-001 | DES-001 | Test | Verified |
```

**Jerry Mapping:**
```
User: "Create bidirectional traceability matrix for Phase 1"
Agent: nse-requirements
Output: projects/PROJ-002/requirements/proj-002-e-XXX-trace-matrix.md
Format: Parent→Requirement→Design→Test traceability
```

---

#### Process 12: Interface Management

| Attribute | NASA Definition | Jerry Implementation |
|-----------|-----------------|---------------------|
| **Purpose** | Manage system interfaces | `nse-integration` agent |
| **Inputs** | Interface requirements, ICDs | Interface definitions |
| **Outputs** | Interface baseline, N² diagram | `integration/{proj}-{entry}-interface-mgmt.md` |
| **Activities** | Identify interfaces, document, control | Interface control |
| **Work Products** | Interface list, N² diagram, ICDs | Interface artifacts |

**N² Diagram Format:**
```markdown
|           | Comp A | Comp B | Comp C |
|-----------|--------|--------|--------|
| Comp A    | -      | IF-001 | IF-002 |
| Comp B    | IF-003 | -      | IF-004 |
| Comp C    | -      | IF-005 | -      |
```

**Jerry Mapping:**
```
User: "Create N² interface diagram for system components"
Agent: nse-integration
Output: projects/PROJ-002/integration/proj-002-e-XXX-n2-diagram.md
Format: N² matrix with interface IDs
```

---

#### Process 13: Technical Risk Management

| Attribute | NASA Definition | Jerry Implementation |
|-----------|-----------------|---------------------|
| **Purpose** | Identify, assess, mitigate technical risks | `nse-risk` agent |
| **Inputs** | Technical plans, assessments | Project artifacts |
| **Outputs** | Risk register, mitigation plans | `risks/{proj}-{entry}-risk-register.md` |
| **Activities** | Identify risks, analyze, plan mitigation | Risk management |
| **Work Products** | Risk list, 5x5 matrix, mitigation plans | Risk artifacts |

**Risk Register Format (NPR 8000.4C):**
```markdown
| ID | Risk Statement | L | C | Score | Status | Mitigation | Owner |
|----|----------------|---|---|-------|--------|------------|-------|
| R-001 | If [condition], then [consequence] | 4 | 5 | 20 | Active | [Plan] | [Name] |
```

**5x5 Risk Matrix:**
```
        Consequence
        1    2    3    4    5
    5 | 5  | 10 | 15 | 20 | 25 |
L   4 | 4  | 8  | 12 | 16 | 20 |
    3 | 3  | 6  | 9  | 12 | 15 |
    2 | 2  | 4  | 6  | 8  | 10 |
    1 | 1  | 2  | 3  | 4  | 5  |

GREEN: 1-7 | YELLOW: 8-15 | RED: 16-25
```

**Jerry Mapping:**
```
User: "Create risk register for deployment phase"
Agent: nse-risk
Output: projects/PROJ-002/risks/proj-002-e-XXX-risk-register.md
Format: If-then risks, 5x5 scoring, mitigations
```

---

#### Process 14: Configuration Management

| Attribute | NASA Definition | Jerry Implementation |
|-----------|-----------------|---------------------|
| **Purpose** | Establish and maintain configuration baselines | `nse-configuration` agent |
| **Inputs** | Configuration items, baselines | Project artifacts |
| **Outputs** | Configuration baseline, change records | `configuration/{proj}-{entry}-baseline.md` |
| **Activities** | Identify CIs, establish baselines, control changes | Config control |
| **Work Products** | CI list, baselines, change log | Configuration artifacts |

**Jerry Mapping:**
```
User: "Document baseline for release 1.0"
Agent: nse-configuration
Output: projects/PROJ-002/configuration/proj-002-e-XXX-baseline-1.0.md
Format: CI list, baseline contents, change log
```

---

#### Process 15: Technical Data Management

| Attribute | NASA Definition | Jerry Implementation |
|-----------|-----------------|---------------------|
| **Purpose** | Manage technical data throughout lifecycle | `nse-configuration` agent |
| **Inputs** | Technical data, data requirements | Project artifacts |
| **Outputs** | Technical data packages | Knowledge artifacts |
| **Activities** | Identify data, store, distribute | Data management |
| **Work Products** | Data dictionary, data packages | Data artifacts |

**Jerry Mapping:**
```
User: "Create technical data package for CDR"
Agent: nse-configuration
Output: projects/PROJ-002/configuration/proj-002-e-XXX-tdp-cdr.md
Format: Data inventory, locations, access
```

---

#### Process 16: Technical Assessment

| Attribute | NASA Definition | Jerry Implementation |
|-----------|-----------------|---------------------|
| **Purpose** | Assess technical progress and health | `nse-reporter` agent |
| **Inputs** | Plans, metrics, status data | Project state |
| **Outputs** | Technical assessment reports | `reports/{proj}-{entry}-assessment.md` |
| **Activities** | Collect metrics, assess progress, report | Status reporting |
| **Work Products** | TPM reports, health assessments | Report artifacts |

**Jerry Mapping:**
```
User: "Generate technical assessment for Phase 2"
Agent: nse-reporter
Output: projects/PROJ-002/reports/proj-002-e-XXX-assessment.md
Format: Metrics, health indicators, issues, recommendations
```

---

#### Process 17: Decision Analysis

| Attribute | NASA Definition | Jerry Implementation |
|-----------|-----------------|---------------------|
| **Purpose** | Apply systematic decision-making | `nse-architecture` agent |
| **Inputs** | Decision problem, alternatives, criteria | Decision context |
| **Outputs** | Decision record, rationale | `architecture/{proj}-{entry}-adr-{topic}.md` |
| **Activities** | Define problem, evaluate alternatives, select | Trade studies |
| **Work Products** | Decision analysis reports, ADRs | Decision artifacts |

**ADR Format (Nygard + NASA):**
```markdown
# ADR-XXX: {Decision Title}

## Status
{Proposed | Accepted | Deprecated | Superseded}

## Context
{What is the issue or need driving this decision?}

## Decision
{What is the change that we're proposing and/or doing?}

## Alternatives Considered
| Option | Description | Pros | Cons |
|--------|-------------|------|------|

## Consequences
{What becomes easier or harder because of this change?}

## NASA SE Compliance
{NPR 7123.1D Process 17 alignment, risk implications}
```

**Jerry Mapping:**
```
User: "Document decision: Redis vs Memcached for caching"
Agent: nse-architecture
Output: projects/PROJ-002/architecture/proj-002-e-XXX-adr-caching.md
Format: ADR with trade study matrix
```

---

## Technical Review Integration

### Review Gates to Agent Mapping

| Review | Phase | Primary Agents | Artifacts Required |
|--------|-------|----------------|-------------------|
| MCR | Formulation | nse-requirements | Stakeholder needs, ConOps |
| SRR | Formulation | nse-requirements, nse-architecture | Requirements, architecture |
| MDR/SDR | Formulation | nse-architecture, nse-risk | Design, risks |
| PDR | Implementation | All except nse-reporter | PDR package |
| CDR | Implementation | All | CDR package |
| SIR | Implementation | nse-integration, nse-verification | Integration evidence |
| TRR | Implementation | nse-verification | Test readiness |
| SAR | Implementation | nse-verification, nse-reviewer | Acceptance evidence |
| ORR | Operations | nse-reporter | Operations readiness |
| FRR | Operations | All | Flight/mission readiness |

### Review Package Content

```
{review}-package/
├── entrance-checklist.md      # nse-reviewer
├── requirements-status.md     # nse-requirements
├── design-status.md           # nse-architecture
├── risk-status.md             # nse-risk
├── vv-status.md               # nse-verification
├── integration-status.md      # nse-integration
├── configuration-status.md    # nse-configuration
└── executive-summary.md       # nse-reporter
```

---

## References

- NASA/SP-2016-6105 Rev2 - NASA Systems Engineering Handbook
- NPR 7123.1D - NASA Systems Engineering Processes and Requirements
- NPR 8000.4C - Agency Risk Management Procedural Requirements
- NASA-HDBK-1009A - NASA Systems Engineering Work Products Handbook
- INCOSE SE Handbook v5.0 - Systems Engineering Handbook

---

*Document Version: 1.0.0*
*Last Updated: 2026-01-09*
