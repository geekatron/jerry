---
name: nasa-se
description: NASA Systems Engineering skill implementing NPR 7123.1D processes through 10 specialized agents. Use for requirements engineering, verification/validation, risk management, technical reviews, system integration, configuration management, architecture decisions, trade studies/exploration, quality assurance, and SE status reporting following mission-grade practices.
version: "1.2.0"
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

> **Version:** 1.2.0
> **Framework:** Jerry NASA SE (NSE)
> **Standards:** NASA/SP-2016-6105 Rev2, NPR 7123.1D, NPR 8000.4C
> **Constitutional Compliance:** Jerry Constitution v1.0

---

## Document Audience (Triple-Lens)

This SKILL.md serves multiple audiences:

| Level | Audience | Sections to Focus On |
|-------|----------|---------------------|
| **L0 (ELI5)** | Project stakeholders, new users | [Purpose](#purpose), [When to Use](#when-to-use-this-skill), [Quick Reference](#quick-reference) |
| **L1 (Engineer)** | Engineers invoking agents | [Invoking an Agent](#invoking-an-agent), [Adversarial Quality Mode](#adversarial-quality-mode), [Agent Details](#agent-details) |
| **L2 (Architect)** | SE workflow designers | [Orchestration Flow](#orchestration-flow), [State Passing](#state-passing-between-agents), [NPR Processes](#nasa-common-technical-processes-npr-71231d) |

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

## Tool Invocation Examples

Each agent uses the allowed tools differently. Here are concrete examples:

### Requirements Engineering (nse-requirements)

```
1. Find stakeholder documentation:
   Glob(pattern="projects/${JERRY_PROJECT}/stakeholders/**/*.md")
   → Returns list of stakeholder needs for requirements derivation

2. Search for existing requirements:
   Grep(pattern="REQ-NSE-|shall", path="projects/${JERRY_PROJECT}/requirements/", output_mode="content", -C=2)
   → Find existing requirements for traceability matrix

3. Read NASA standards for compliance:
   WebFetch(url="https://nodis3.gsfc.nasa.gov/displayDir.cfm?Internal_ID=N_PR_7123_001D_",
            prompt="Extract requirements management guidance from NPR 7123.1D")
   → Reference authoritative NASA source

4. Create requirements output (MANDATORY per P-002, P-043):
   Write(
       file_path="projects/${JERRY_PROJECT}/requirements/proj-002-e-101-auth-requirements.md",
       content="---\nDISCLAIMER: This guidance is AI-generated...\n---\n\n# Requirements: Authentication\n\n## L0: Executive Summary\n..."
   )
   → Persist with mandatory disclaimer - transient output VIOLATES P-002 and P-043
```

### Risk Assessment (nse-risk)

```
1. Find existing risk artifacts:
   Glob(pattern="projects/${JERRY_PROJECT}/risks/**/*.md")
   → Discover existing risk register and assessments

2. Search for risk keywords in project:
   Grep(pattern="risk|threat|vulnerability|5x5", path="projects/${JERRY_PROJECT}/", output_mode="content", -C=2)
   → Find risk-related discussions across project

3. Read project context for risk identification:
   Read(file_path="projects/${JERRY_PROJECT}/requirements/requirements-spec.md")
   → Load requirements to identify verification risks

4. Create risk register (MANDATORY per P-002, P-043):
   Write(
       file_path="projects/${JERRY_PROJECT}/risks/proj-002-e-201-risk-register.md",
       content="---\nDISCLAIMER: This guidance is AI-generated...\n---\n\n# Risk Register: Deployment Phase\n\n## L0: Executive Summary\n..."
   )
   → Persist risk findings with mandatory disclaimer
```

### Technical Review (nse-reviewer)

```
1. Find review artifacts to evaluate:
   Glob(pattern="projects/${JERRY_PROJECT}/requirements/**/*.md")
   → Discover requirements for review gate assessment

2. Search for review readiness indicators:
   Grep(pattern="Status: (Approved|Baselined)|TBD|TBR", path="projects/${JERRY_PROJECT}/", output_mode="content", -C=2)
   → Find approval status and unresolved items

3. Read verification status:
   Read(file_path="projects/${JERRY_PROJECT}/verification/VCRM.md")
   → Load VCRM for review entrance criteria check

4. Create review package (MANDATORY per P-002, P-043):
   Write(
       file_path="projects/${JERRY_PROJECT}/reviews/proj-002-e-301-PDR-entrance.md",
       content="---\nDISCLAIMER: This guidance is AI-generated...\n---\n\n# PDR Entrance Checklist\n\n## L0: Executive Summary\n..."
   )
   → Persist review findings with mandatory disclaimer
```

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

## Adversarial Quality Mode

> **Source:** EPIC-002 EN-305 (NASA-SE Skill Enhancement), EN-303 (Situational Applicability Mapping)
> **SSOT:** `.context/rules/quality-enforcement.md` (canonical constants)

The NASA SE skill integrates adversarial quality controls into systems engineering processes. All SE review gates, V&V activities, and risk assessments incorporate structured adversarial challenge through creator-critic-revision cycles.

### V&V Enhancement with Adversarial Review

Verification and validation activities are enhanced with adversarial challenge at each stage:

| V&V Activity | Adversarial Enhancement | Strategies Applied |
|--------------|------------------------|-------------------|
| Requirements Review | Challenge completeness, ambiguity, testability | S-002 (Devil's Advocate), S-013 (Inversion) |
| Design Verification | Challenge design assumptions and failure modes | S-004 (Pre-Mortem), S-012 (FMEA) |
| Test Planning | Challenge test coverage and boundary conditions | S-013 (Inversion), S-011 (CoVe) |
| Validation | Challenge fitness for purpose against stakeholder needs | S-003 (Steelman), S-007 (Constitutional AI) |

### Quality Scoring Integration

All NSE deliverables at C2+ criticality require quality scoring per the SSOT:

- **Threshold:** >= 0.92 weighted composite score (ref: `.context/rules/quality-enforcement.md` H-13)
- **Scoring mechanism:** S-014 (LLM-as-Judge) with dimension-level rubrics
- **Minimum cycle count:** 3 iterations (creator -> critic -> revision) (ref: H-14)
- **Self-review:** Required before presenting any deliverable (ref: H-15, S-010)

| Dimension | Weight | NSE Focus |
|-----------|--------|-----------|
| Completeness | 0.20 | All NPR 7123.1D processes addressed |
| Internal Consistency | 0.20 | Requirements/design/V&V alignment |
| Methodological Rigor | 0.20 | NASA standards compliance |
| Evidence Quality | 0.15 | Traceability, evidence links |
| Actionability | 0.15 | Clear next steps, RFAs |
| Traceability | 0.10 | Bidirectional trace integrity |

### Criticality-Based Review Intensity

Review intensity scales with decision criticality (ref: `.context/rules/quality-enforcement.md` Criticality Levels):

| Criticality | Review Intensity | Required Strategies | NSE Context Examples |
|-------------|-----------------|---------------------|---------------------|
| C1 (Routine) | Self-check only | S-010 (Self-Refine) | Minor requirement wording updates |
| C2 (Standard) | Standard critic cycle | S-007, S-002, S-014 | New requirements, routine V&V |
| C3 (Significant) | Deep review | C2 + S-004, S-012, S-013 | API changes, new interfaces, risk mitigations |
| C4 (Critical) | Tournament review | All 10 selected strategies | Architecture decisions, safety-critical requirements |

### Review Gate Integration

NPR 7123.1D review gates map to adversarial review levels:

| Review Gate | NPR 7123.1D | Minimum Criticality | Primary Strategies | Focus |
|-------------|-------------|---------------------|-------------------|-------|
| SRR | Appendix G.1 | C2 | S-002, S-003, S-013, S-014 | Requirements completeness, ambiguity |
| PDR | Appendix G.2 | C2 | S-004, S-012, S-014 | Design approach soundness, failure modes |
| CDR | Appendix G.3 | C3 | S-002, S-004, S-007, S-012, S-013, S-014 | Design completeness, V&V readiness |
| TRR | Appendix G.4 | C2 | S-011, S-013, S-014 | Test coverage, verification gaps |
| FRR | Appendix G.5 | C3 | S-001, S-004, S-012, S-014 | Readiness, residual risk |

**Auto-Escalation:** Artifacts touching `docs/governance/JERRY_CONSTITUTION.md` auto-escalate to C4. Artifacts touching `.context/rules/` auto-escalate to C3 minimum (ref: AE-001, AE-002).

### Strategy Catalog Reference for NSE Contexts

| NSE Context | Recommended Strategies | Rationale |
|-------------|----------------------|-----------|
| Requirements engineering | S-002, S-003, S-013, S-014 | Challenge completeness (Devil's Advocate), strengthen arguments (Steelman), invert assumptions (Inversion), score quality (LLM-as-Judge) |
| Verification planning | S-002, S-011, S-013, S-014 | Challenge V&V coverage (Devil's Advocate), verify claims (CoVe), identify gaps via inversion (Inversion), score V&V completeness (LLM-as-Judge) |
| Validation activities | S-003, S-007, S-014 | Strengthen stakeholder alignment (Steelman), check constitutional compliance (Constitutional AI), score fitness (LLM-as-Judge) |
| Risk assessment | S-001, S-004, S-012, S-014 | Red-team assumptions (Red Team), pre-mortem on mitigations (Pre-Mortem), structured failure analysis (FMEA), score assessment quality (LLM-as-Judge) |
| Design review (PDR/CDR) | S-002, S-004, S-012, S-013 | Challenge design decisions (Devil's Advocate), imagine failures (Pre-Mortem), structured failure modes (FMEA), invert constraints (Inversion) |
| Technical review (SRR/FRR) | S-001, S-002, S-003, S-014 | Red-team readiness (Red Team), challenge assumptions (Devil's Advocate), strengthen case (Steelman), score readiness (LLM-as-Judge) |

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

*Skill Version: 1.2.0*
*Constitutional Compliance: Jerry Constitution v1.0 + P-040, P-041, P-042, P-043*
*Enhancement: EN-708 adversarial quality mode integration (EPIC-002 design)*
*Last Updated: 2026-02-14*
