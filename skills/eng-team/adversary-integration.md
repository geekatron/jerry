# /eng-team Adversary Integration

> **Version:** 1.0.0
> **Skill:** /eng-team
> **Feature:** FEAT-025 (/adversary Integration)
> **SSOT:** `.context/rules/quality-enforcement.md`, ADR-PROJ010-001

## Document Sections

| Section | Purpose |
|---------|---------|
| [Overview](#overview) | Integration scope and rationale |
| [Integration Point Mapping](#integration-point-mapping) | Which agent outputs go through /adversary |
| [Scoring Trigger Definitions](#scoring-trigger-definitions) | Decision table: output type x criticality |
| [Escalation Paths](#escalation-paths) | What happens when deliverables score below threshold |
| [eng-reviewer Orchestration](#eng-reviewer-orchestration) | How eng-reviewer invokes /adversary |
| [End-to-End Quality Workflow](#end-to-end-quality-workflow) | From agent output to accepted deliverable |

---

## Overview

The /eng-team skill integrates with the /adversary skill to enforce quality gates on security-critical deliverables. This integration ensures that architecture decisions, implementation artifacts, and review findings receive appropriate adversarial scrutiny based on their criticality level.

**Governing Rules:**
- H-13: Quality threshold >= 0.92 for C2+ deliverables
- H-14: Creator-critic-revision cycle (minimum 3 iterations)
- H-15: Self-review (S-010) before presenting any deliverable
- H-16: Steelman (S-003) before critique (S-002)
- H-17: Quality scoring via S-014 LLM-as-Judge REQUIRED

**Integration Agent:** eng-reviewer is the primary integration point. It orchestrates /adversary invocation for C2+ deliverables at the Step 7 final quality gate.

---

## Integration Point Mapping

| Agent | Output Type | /adversary Integration | Criticality Trigger |
|-------|------------|----------------------|-------------------|
| eng-architect | Architecture decisions, threat models | Yes -- via eng-reviewer at Step 7 | C2+ (always for architecture decisions) |
| eng-lead | Implementation plans, standards mappings | Yes -- via eng-reviewer at Step 7 | C2+ |
| eng-backend | Secure implementation artifacts | Yes -- via eng-reviewer at Step 7 | C2+ |
| eng-frontend | Secure implementation artifacts | Yes -- via eng-reviewer at Step 7 | C2+ |
| eng-infra | IaC configurations, container hardening | Yes -- via eng-reviewer at Step 7 | C3+ (infrastructure changes are auto-C3 per AE-005) |
| eng-devsecops | Pipeline configurations, scan results | Indirect -- results feed into eng-reviewer assessment | C2+ |
| eng-qa | Test results, coverage reports | Indirect -- results feed into eng-reviewer assessment | C2+ |
| eng-security | Code review findings | Yes -- via eng-reviewer at Step 7 | C2+ |
| eng-reviewer | Final gate decision | Self -- eng-reviewer IS the /adversary integration point | C2+ |
| eng-incident | IR plans, runbooks | Yes -- via eng-reviewer if part of engagement | C2+ |

### Direct vs. Indirect Integration

- **Direct:** Agent output is explicitly submitted to /adversary for scoring via eng-reviewer
- **Indirect:** Agent output contributes evidence to eng-reviewer's assessment but is not independently scored

---

## Scoring Trigger Definitions

### Decision Table: Output Type x Criticality -> Strategy Set

| Output Type | C1 (Routine) | C2 (Standard) | C3 (Significant) | C4 (Critical) |
|-------------|-------------|---------------|-------------------|---------------|
| Architecture decisions | S-010 | S-007, S-002, S-014 | C2 + S-004, S-012, S-013 | All 10 strategies |
| Threat models | S-010 | S-007, S-002, S-014 | C2 + S-004, S-012, S-013 | All 10 strategies (tournament) |
| Implementation plans | S-010 | S-007, S-002, S-014 | C2 + S-004, S-012, S-013 | All 10 strategies |
| Code artifacts | S-010 | S-007, S-014 | C2 + S-004, S-013 | All 10 strategies |
| IaC/Infrastructure | S-010 | S-007, S-002, S-014 | C2 + S-004, S-012, S-013 | All 10 strategies |
| Test results | S-010 | S-014 | S-014, S-013 | C2 + S-004, S-012 |
| Code review findings | S-010 | S-007, S-014 | C2 + S-004, S-013 | All 10 strategies |
| IR plans/runbooks | S-010 | S-007, S-002, S-014 | C2 + S-004, S-012, S-013 | All 10 strategies |
| Engagement-level report | S-010 | S-007, S-002, S-014 | C2 + S-004, S-012, S-013 | All 10 strategies (tournament) |

### Auto-Escalation Rules (AE)

| Condition | Escalation | Source |
|-----------|------------|--------|
| Architecture changes (new service, API redesign) | Auto-C3 minimum | AE-003 |
| Security-relevant code (auth, crypto, input validation) | Auto-C3 minimum | AE-005 |
| Infrastructure changes (IaC, container, network) | Auto-C3 minimum | AE-005 |
| Authentication/authorization system changes | Auto-C4 | Security criticality |

---

## Escalation Paths

### Below-Threshold Scoring

| Score Band | Range | Action | Responsible |
|------------|-------|--------|-------------|
| PASS | >= 0.95 | Deliverable accepted | eng-reviewer approves |
| REVISE | 0.85 - 0.94 | Targeted revision, re-score | Original agent revises, eng-reviewer re-scores |
| REJECTED | < 0.85 | Significant rework required | Original agent reworks, escalate to eng-architect if systemic |

### Escalation Protocol

1. **First failure (REVISE band):** eng-reviewer returns specific findings to the originating agent with revision guidance. Agent revises and resubmits.
2. **Second failure (any band):** eng-reviewer escalates to eng-lead for implementation plan review. May indicate systemic design issue.
3. **Third failure or REJECTED band:** Escalation to eng-architect for architecture review. Possible design-level root cause.
4. **Persistent failure:** User notification per P-020. Human judgment required.

### Quality Score Dimensions (S-014)

| Dimension | Weight | eng-team Focus |
|-----------|--------|---------------|
| Completeness | 0.20 | All threat categories addressed, all requirements mapped |
| Internal Consistency | 0.20 | Findings consistent across agents, no contradictions |
| Methodological Rigor | 0.20 | Standards correctly applied (STRIDE, OWASP, SSDF) |
| Evidence Quality | 0.15 | Findings backed by tool output, code references, CVE citations |
| Actionability | 0.15 | Remediation guidance specific and implementable |
| Traceability | 0.10 | Requirements -> implementation -> test -> review chain intact |

---

## eng-reviewer Orchestration

### Step 7 Quality Gate Procedure

```
1. eng-reviewer receives all prior agent outputs (Steps 1-6)
2. eng-reviewer performs self-review (S-010, H-15)
3. eng-reviewer determines deliverable criticality (C1-C4)
4. For C2+:
   a. eng-reviewer invokes /adversary (adv-selector)
   b. adv-selector maps criticality to strategy set
   c. adv-executor runs selected strategies against deliverables
   d. adv-scorer produces dimension-level quality scores
   e. eng-reviewer evaluates results against threshold (>= 0.95)
5. If PASS: eng-reviewer issues approval
6. If FAIL: eng-reviewer returns findings to originating agent(s)
7. Revision cycle repeats (H-14: minimum 3 iterations)
```

### eng-reviewer /adversary Invocation Pattern

eng-reviewer submits to /adversary:
- **Deliverable:** The consolidated output from all prior steps
- **Criticality level:** Determined by eng-reviewer based on scope
- **Context:** Threat model, compliance requirements, test results
- **Threshold:** >= 0.95 quality score

/adversary returns:
- **Strategy execution reports:** Per-strategy findings
- **Quality score:** Weighted composite across 6 dimensions
- **Specific findings:** Actionable issues for revision

---

## End-to-End Quality Workflow

```
Agent Output (Steps 1-6)
    |
    v
eng-reviewer Self-Review (S-010, H-15)
    |
    v
Criticality Assessment (C1/C2/C3/C4)
    |
    +-- C1: Self-review sufficient, approve
    |
    +-- C2+: Submit to /adversary
            |
            v
        adv-selector: Choose strategy set
            |
            v
        adv-executor: Run strategies
            |
            v
        adv-scorer: Score (6 dimensions)
            |
            v
        Score >= 0.95? --YES--> APPROVED
            |
            NO
            |
            v
        Return findings to agent
            |
            v
        Agent revises deliverable
            |
            v
        Re-submit to eng-reviewer (loop, H-14 min 3 iterations)
```

### Engagement-Level vs. Artifact-Level Scoring

| Scope | When | What Gets Scored |
|-------|------|-----------------|
| Artifact-level | Each step completion | Individual agent output |
| Engagement-level | Step 7 final gate | Consolidated deliverable across all steps |

eng-reviewer performs engagement-level scoring at Step 7. Individual artifact-level scoring MAY occur during earlier steps if the engagement criticality is C3+.

---

*Version: 1.0.0 | /eng-team Skill | FEAT-025 | PROJ-010 Cyber Ops*
