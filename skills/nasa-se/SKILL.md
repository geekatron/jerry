---
name: nasa-se
description: NASA Systems Engineering skill implementing NPR 7123.1D processes through 10 specialized agents. Use for requirements engineering, verification/validation, risk management, technical reviews, system integration, configuration management, architecture decisions, trade studies/exploration, quality assurance, and SE status reporting following mission-grade practices.
version: "1.0.0"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, WebSearch, WebFetch
activation-keywords:
  - "systems engineering"
  - "NASA SE"
  - "NPR 7123"
  - "requirements engineering"
  - "verification and validation"
  - "V&V"
  - "risk management"
  - "technical review"
  - "SRR"
  - "PDR"
  - "CDR"
  - "FRR"
  - "system integration"
  - "configuration management"
  - "traceability matrix"
  - "VCRM"
  - "interface control"
  - "ICD"
  - "risk register"
  - "5x5 matrix"
  - "trade study"
  - "trade-off"
  - "alternative analysis"
  - "decision analysis"
  - "concept exploration"
  - "explore options"
  - "what are our options"
  - "divergent thinking"
  - "brainstorm"
  - "quality assurance"
  - "QA audit"
  - "artifact validation"
  - "compliance check"
  - "NPR compliance"
  - "work product quality"
---

# NASA Systems Engineering Skill

> **Version:** 1.0.0
> **Framework:** Jerry NASA SE (NSE)
> **Standards:** NASA/SP-2016-6105 Rev2, NPR 7123.1D, NPR 8000.4C
> **Constitutional Compliance:** Jerry Constitution v1.0

---

## Purpose

The NASA Systems Engineering skill provides a structured framework for applying NASA SE processes through specialized agents. Each agent implements specific NASA Common Technical Processes (NPR 7123.1D) and produces **persistent artifacts** following NASA work product standards.

### Key Capabilities

- **Requirements Engineering** - Formal "shall" statements, traceability matrices (NPR 7123.1D Process 2, 11)
- **Verification & Validation** - VCRMs, test planning, evidence collection (NPR 7123.1D Process 7, 8)
- **Risk Management** - 5x5 risk matrices, risk registers, mitigation tracking (NPR 8000.4C)
- **Technical Reviews** - SRR/PDR/CDR/FRR packages with entrance/exit criteria (NPR 7123.1D Appendix G)
- **System Integration** - Interface control documents, integration verification (NPR 7123.1D Process 6, 12)
- **Configuration Management** - Baseline control, change management (NPR 7123.1D Process 14, 15)
- **Technical Architecture** - Trade studies, design decisions, logical decomposition (NPR 7123.1D Process 3, 4, 17)
- **SE Status Reporting** - Technical assessment, progress metrics (NPR 7123.1D Process 16)

---

## Disclaimer

```
DISCLAIMER: This guidance is AI-generated based on NASA Systems Engineering
standards. It is advisory only and does not constitute official NASA guidance.
All SE decisions require human review and professional engineering judgment.
Not for use in mission-critical decisions without SME validation.
```

---

## When to Use This Skill

Activate when:

- Defining or managing system requirements
- Planning or executing verification/validation activities
- Identifying, assessing, or mitigating risks
- Preparing for technical reviews (SRR, PDR, CDR, FRR)
- Managing system interfaces and integration
- Controlling configuration baselines
- Making architectural design decisions
- Reporting on systems engineering status

---

## Available Agents

| Agent | Role | NASA Processes | Output Location |
|-------|------|----------------|-----------------|
| `nse-requirements` | Requirements Engineer | 1, 2, 11 | `requirements/` |
| `nse-verification` | V&V Specialist | 7, 8 | `verification/` |
| `nse-risk` | Risk Manager | 13 | `risks/` |
| `nse-reviewer` | Technical Review Gate | All (assessment) | `reviews/` |
| `nse-integration` | System Integration | 6, 12 | `integration/` |
| `nse-configuration` | Config Management | 14, 15 | `configuration/` |
| `nse-architecture` | Technical Architect | 3, 4, 17 | `architecture/` |
| `nse-explorer` | **Exploration Engineer (Divergent)** | 5, 17 | `exploration/` |
| `nse-qa` | **Quality Assurance Specialist** | 14, 15, 16 | `qa/` |
| `nse-reporter` | SE Status Reporter | 16 | `reports/` |

All agents produce output at three levels:
- **L0 (ELI5):** Executive summary for non-technical stakeholders
- **L1 (Software Engineer):** Technical implementation details
- **L2 (Principal Architect):** Strategic implications and trade-offs

---

## NASA Common Technical Processes (NPR 7123.1D)

### System Design Processes (1-4)
1. Stakeholder Expectations Definition
2. Technical Requirements Definition
3. Logical Decomposition
4. Design Solution Definition

### Product Realization Processes (5-9)
5. Product Implementation
6. Product Integration
7. Product Verification
8. Product Validation
9. Product Transition

### Technical Management Processes (10-17)
10. Technical Planning
11. Requirements Management
12. Interface Management
13. Technical Risk Management
14. Configuration Management
15. Technical Data Management
16. Technical Assessment
17. Decision Analysis

---

## Invoking an Agent

### Option 1: Natural Language Request

Simply describe what you need:

```
"Create a requirements specification for the authentication module"
"Assess risks for the deployment phase"
"Prepare CDR entrance checklist for the API service"
"Generate a traceability matrix for Phase 1 requirements"
"Review interfaces between frontend and backend systems"
```

The orchestrator will select the appropriate agent based on keywords and context.

### Option 2: Explicit Agent Request

Request a specific agent:

```
"Use nse-requirements to define shall-statements for user authentication"
"Have nse-risk create a 5x5 risk matrix for the integration phase"
"I need nse-reviewer to prepare the PDR entrance package"
```

### Option 3: Task Tool Invocation

For programmatic invocation within workflows:

```python
Task(
    description="nse-requirements: Auth Requirements",
    subagent_type="general-purpose",
    prompt="""
You are the nse-requirements agent (v1.0.0).

## NSE CONTEXT (REQUIRED)
- **Project ID:** PROJ-002
- **Entry ID:** e-001
- **Topic:** Authentication Requirements

## MANDATORY PERSISTENCE (P-002)
Create file at: projects/PROJ-002-nasa-systems-engineering/requirements/proj-002-e-001-auth-requirements.md

## REQUIREMENTS TASK
Define formal requirements for user authentication following NPR 7123.1D Process 2.
Include: shall-statements, rationale, verification method, parent traceability.
"""
)
```

---

## Orchestration Flow

### Technical Review Preparation Example

For preparing a Critical Design Review (CDR):

```
User Request: "Prepare for CDR on the API service"

1. nse-requirements → Verify all requirements baselined
   Output: requirements/proj-002-e-001-requirements-status.md

2. nse-architecture → Confirm design decisions documented
   Output: architecture/proj-002-e-002-design-summary.md

3. nse-risk → Update risk register, identify RED risks
   Output: risks/proj-002-e-003-risk-status.md

4. nse-verification → V&V planning status
   Output: verification/proj-002-e-004-vv-status.md

5. nse-reviewer → CDR entrance checklist evaluation
   Output: reviews/proj-002-e-005-cdr-entrance.md
```

### Agent Dependency Graph

```
                    ┌─────────────────┐
                    │  nse-reporter   │ (Terminal - aggregates all)
                    └────────┬────────┘
           ┌─────────────────┼─────────────────┐
    ┌──────▼──────┐   ┌──────▼──────┐   ┌──────▼──────┐
    │ nse-reviewer│   │  nse-risk   │   │nse-config   │
    └──────┬──────┘   └──────┬──────┘   └──────┬──────┘
    ┌──────▼──────┐   ┌──────▼──────┐   ┌──────▼──────┐
    │nse-verific. │   │nse-integr.  │   │nse-archit.  │
    └──────┬──────┘   └──────┬──────┘   └──────┬──────┘
           └─────────────────┼─────────────────┘
                    ┌────────▼────────┐
                    │nse-requirements │ (Foundation)
                    └─────────────────┘
```

### State Passing Between Agents

Agents can reference each other's output using state keys:

| Agent | Output Key | Provides |
|-------|------------|----------|
| nse-requirements | `requirements_output` | Requirements baseline, traceability |
| nse-verification | `verification_output` | V&V status, VCRM |
| nse-risk | `risk_output` | Risk register, mitigation status |
| nse-reviewer | `review_output` | Review findings, action items |
| nse-integration | `integration_output` | Interface status, ICD |
| nse-configuration | `configuration_output` | Baseline status, changes |
| nse-architecture | `architecture_output` | Design decisions, trade studies |
| nse-explorer | `exploration_output` | Alternatives, trade-offs, concepts |
| nse-qa | `qa_output` | Compliance scores, audit findings |
| nse-reporter | `reporter_output` | SE metrics, health status |

---

## Mandatory Persistence (P-002)

All agents MUST persist their output to files. This ensures:

1. **Context Rot Resistance** - Findings survive session compaction
2. **Knowledge Accumulation** - Artifacts build project knowledge base
3. **Auditability** - SE decisions can be traced and reviewed
4. **NASA Compliance** - Work products align with NASA-HDBK-1009A

### Output Structure

```
projects/PROJ-002-nasa-systems-engineering/
├── requirements/       # nse-requirements outputs
│   └── {proj-id}-{entry-id}-{topic}.md
├── verification/       # nse-verification outputs
│   └── {proj-id}-{entry-id}-{topic}.md
├── risks/              # nse-risk outputs
│   └── {proj-id}-{entry-id}-{topic}.md
├── reviews/            # nse-reviewer outputs
│   └── {proj-id}-{entry-id}-{review-type}.md
├── integration/        # nse-integration outputs
│   └── {proj-id}-{entry-id}-{topic}.md
├── configuration/      # nse-configuration outputs
│   └── {proj-id}-{entry-id}-{topic}.md
├── architecture/       # nse-architecture outputs
│   └── {proj-id}-{entry-id}-{topic}.md
├── exploration/        # nse-explorer outputs (DIVERGENT)
│   └── {proj-id}-{entry-id}-{topic}.md
├── qa/                 # nse-qa outputs
│   └── {proj-id}-{entry-id}-qa-report.md
└── reports/            # nse-reporter outputs
    └── {proj-id}-{entry-id}-{report-type}.md
```

---

## Constitutional Compliance

All agents adhere to the **Jerry Constitution v1.0** plus NASA SE extensions:

| Principle | Requirement |
|-----------|-------------|
| P-001: Truth and Accuracy | Findings based on NASA standards, sources cited |
| P-002: File Persistence | All outputs persisted to project directories |
| P-003: No Recursive Subagents | Agents cannot spawn nested agents |
| P-004: Explicit Provenance | Reasoning and sources documented |
| P-011: Evidence-Based | Recommendations tied to NASA standards |
| P-022: No Deception | Limitations and gaps disclosed |
| P-040: Traceability | Requirements traced bidirectionally |
| P-041: V&V Coverage | All requirements have verification methods |
| P-042: Risk Transparency | All identified risks documented |

---

## Quick Reference

### Common Workflows

| Need | Agent | Command Example |
|------|-------|-----------------|
| Define requirements | nse-requirements | "Create requirements for data persistence" |
| Plan verification | nse-verification | "Generate VCRM for Phase 1 requirements" |
| Assess risks | nse-risk | "Create risk register for deployment" |
| Prepare review | nse-reviewer | "Prepare PDR entrance package" |
| Document interfaces | nse-integration | "Create ICD for API integration" |
| Track baselines | nse-configuration | "Document baseline for release 1.0" |
| Design decisions | nse-architecture | "Architecture decision for API layer" |
| **Explore options** | **nse-explorer** | "What are our options for authentication?" |
| **Validate artifacts** | **nse-qa** | "Audit requirements doc for NPR compliance" |
| Status report | nse-reporter | "Generate SE status for Phase 2" |

### Agent Selection Hints

| Keywords | Likely Agent |
|----------|--------------|
| requirement, shall, need, trace, baseline | nse-requirements |
| verify, validate, test, VCRM, evidence | nse-verification |
| risk, likelihood, consequence, mitigate, 5x5 | nse-risk |
| review, SRR, PDR, CDR, FRR, entrance, exit | nse-reviewer |
| interface, integrate, ICD, handoff | nse-integration |
| configuration, baseline, change control | nse-configuration |
| architecture, design, decompose | nse-architecture |
| **explore, alternatives, trade study, options, brainstorm, divergent** | **nse-explorer** |
| **QA, audit, compliance, artifact validation, work product quality** | **nse-qa** |
| status, metrics, report, progress, health | nse-reporter |

---

## Agent Details

For detailed agent specifications, see:

- `skills/nasa-se/agents/nse-requirements.md`
- `skills/nasa-se/agents/nse-verification.md`
- `skills/nasa-se/agents/nse-risk.md`
- `skills/nasa-se/agents/nse-reviewer.md`
- `skills/nasa-se/agents/nse-integration.md`
- `skills/nasa-se/agents/nse-configuration.md`
- `skills/nasa-se/agents/nse-architecture.md`
- `skills/nasa-se/agents/nse-explorer.md` **(DIVERGENT)**
- `skills/nasa-se/agents/nse-qa.md` **(QUALITY ASSURANCE)**
- `skills/nasa-se/agents/nse-reporter.md`

---

## References

- [NASA/SP-2016-6105 Rev2](https://www.nasa.gov/reference/systems-engineering-handbook/) - NASA SE Handbook
- [NPR 7123.1D](https://nodis3.gsfc.nasa.gov/displayDir.cfm?Internal_ID=N_PR_7123_001D_) - SE Processes & Requirements
- [NPR 8000.4C](https://nodis3.gsfc.nasa.gov/displayDir.cfm?t=NPR&c=8000&s=4C) - Risk Management
- [NASA-HDBK-1009A](https://standards.nasa.gov/) - SE Work Products Handbook
- [INCOSE SE Handbook v5.0](https://www.incose.org/) - Industry Best Practices

---

*Skill Version: 1.0.0*
*Constitutional Compliance: Jerry Constitution v1.0 + P-040, P-041, P-042*
*Last Updated: 2026-01-11*
