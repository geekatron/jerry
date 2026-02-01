# FEAT-001:DEC-002: Orchestration Execution Decisions

<!--
TEMPLATE: Decision
VERSION: 1.0.0
SOURCE: .context/templates/worktracker/DECISION.md
CREATED: 2026-01-31
PURPOSE: Capture decisions made during orchestration planning and execution
-->

> **Type:** decision
> **Status:** ACCEPTED
> **Priority:** HIGH
> **Created:** 2026-01-31T16:00:00Z
> **Parent:** FEAT-001
> **Owner:** User + Claude
> **Related:** FEAT-001:DEC-001

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overview of 4 orchestration decisions |
| [Decision Context](#decision-context) | Background, constraints, stakeholders |
| [Decisions](#decisions) | D-001 through D-004 detailed decisions |
| [Decision Summary](#decision-summary) | Quick reference table |
| [Related Artifacts](#related-artifacts) | Parent, related documents |
| [Document History](#document-history) | Change log |

---

## Frontmatter

```yaml
id: "FEAT-001:DEC-002"
work_type: DECISION
title: "Orchestration Execution Decisions"
status: ACCEPTED
priority: HIGH
created_by: "Claude"
participants:
  - "User"
  - "Claude"
created_at: "2026-01-31T16:00:00Z"
updated_at: "2026-01-31T18:00:00Z"
decided_at: "2026-01-31T16:30:00Z"
parent_id: "FEAT-001"
tags: ["orchestration", "quality-gates", "execution-strategy", "tiered-execution"]
decision_count: 4
superseded_by: null
supersedes: null
```

---

## Summary

This document captures the decisions made during orchestration planning and execution. These decisions refine the high-level orchestration approach from DEC-001 into specific execution strategies.

**Decisions Captured:** 4

**Key Outcomes:**
- 19 agents organized into 5 phases with dual quality gates
- Tiered execution within phases for dependency management
- Quality gate threshold set to ≥0.92 with adversarial prompting
- User checkpoints after each quality gate
- Auto-retry mechanism (2x) before user escalation

---

## Decision Context

### Background

After accepting the orchestration approach in DEC-001:D-002, detailed execution decisions were needed to define how the 19 agents would be coordinated, what quality thresholds to use, and how to handle failures.

### Constraints

- Must maximize parallel execution for efficiency
- Must respect agent dependencies
- Must ensure high quality (≥0.90 baseline, pushed to ≥0.92)
- Must provide user visibility and control
- Must handle failures gracefully

### Stakeholders

| Stakeholder | Role | Interest |
|-------------|------|----------|
| User | Project Owner | Quality, visibility, control |
| Claude | Orchestrator | Execution efficiency, state management |

---

## Decisions

### D-001: Tiered Execution Strategy (DEC-OSS-001)

**Date:** 2026-01-31
**Participants:** User, Claude

#### Question/Context

How should agents be executed within each phase, given that some agents depend on outputs from others?

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | Tiered Execution | Within-phase tiers (parallel within tier, sequential between) | Optimal parallelism, respects dependencies |
| **B** | Full Sequential | All agents one-by-one | Safe but slow |
| **C** | Full Parallel | All agents at once | Fast but ignores dependencies |

#### Decision

**We decided:** Use tiered execution within phases:
- **Tier 1:** Independent agents run in parallel (e.g., ps-researcher, ps-analyst, nse-explorer, nse-requirements)
- **Tier 2:** Dependent agents run after Tier 1 completes (e.g., nse-risk requires Tier 1 outputs)
- **Tier 3:** Quality gate agents run in parallel (ps-critic, nse-qa)
- **Tier 4:** Reports/synthesis run after gates pass

#### Rationale

This balances execution speed with correctness. Parallel execution within tiers maximizes throughput while sequential tiers ensure dependencies are met.

#### Implications

- **Positive:** Optimal efficiency, correct dependency handling
- **Negative:** More complex orchestration logic
- **Follow-up required:** Document tier dependencies in ORCHESTRATION.yaml

---

### D-002: Quality Gate Threshold ≥0.92 (DEC-OSS-002)

**Date:** 2026-01-31
**Participants:** User, Claude

#### Question/Context

What quality threshold should be required for quality gates to pass?

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | ≥0.92 | Higher bar, better quality | May require more iterations |
| **B** | ≥0.90 | Standard threshold | Acceptable but not excellent |
| **C** | ≥0.85 | Lower bar | Faster but lower quality |

#### Decision

**We decided:** Set quality gate threshold to ≥0.92 for all gates.

Both quality gate agents (ps-critic and nse-qa) must achieve ≥0.92 for a gate to pass. This is higher than the typical 0.90 threshold to ensure excellence for the OSS release.

#### Rationale

The OSS release represents Jerry's public face. Higher quality thresholds ensure the release artifacts meet a standard appropriate for open-source community adoption. The 0.92 threshold provides margin above the 0.90 baseline.

#### Implications

- **Positive:** Higher quality deliverables
- **Negative:** May require remediation iterations
- **Follow-up required:** Implement auto-retry mechanism for failures

---

### D-003: User Checkpoints After Each Gate (DEC-OSS-003)

**Date:** 2026-01-31
**Participants:** User, Claude

#### Question/Context

When should the user be consulted during orchestration execution?

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | After Each Quality Gate | 5 checkpoints total | Maximum control, visibility |
| **B** | Only at Start/End | 2 checkpoints | Faster but less control |
| **C** | On Failure Only | Variable | Efficient but less visibility |

#### Decision

**We decided:** Pause for user checkpoint after each quality gate completes (5 total).

Checkpoints occur after: QG-0, QG-1, QG-2, QG-3, QG-4

#### Rationale

Given the OSS release's importance, user visibility and control at each phase boundary ensures alignment and allows course correction before proceeding.

#### Implications

- **Positive:** Maximum user control, visibility into progress
- **Negative:** Requires user availability, may slow overall progress
- **Follow-up required:** Document checkpoint expectations in ORCHESTRATION_PLAN.md

---

### D-004: Auto-Retry Before Escalation (DEC-OSS-004)

**Date:** 2026-01-31
**Participants:** User, Claude

#### Question/Context

How should quality gate failures be handled?

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | Auto-Retry 2x | Automatic remediation attempts before user | Efficient, handles transient issues |
| **B** | Immediate Escalation | User involved immediately | Maximum control but interruptive |
| **C** | No Retry | Fail and stop | Simple but harsh |

#### Decision

**We decided:** Implement 2x auto-retry for quality gate failures before escalating to user.

Process:
1. Gate fails (score < 0.92)
2. Automatically analyze issues and attempt remediation
3. Re-run gate evaluation
4. If still fails, retry once more
5. After 2 failures, escalate to user with diagnostic report

#### Rationale

Minor issues can often be resolved automatically. The 2x retry limit prevents infinite loops while giving reasonable opportunity for self-correction before bothering the user.

#### Implications

- **Positive:** Reduces user interruptions, handles minor issues automatically
- **Negative:** May delay user awareness of persistent issues
- **Follow-up required:** Document retry logic and escalation triggers

---

## Decision Summary

| ID | Decision | Date | Status |
|----|----------|------|--------|
| D-001 | Tiered execution within phases | 2026-01-31 | ACCEPTED |
| D-002 | Quality gate threshold ≥0.92 | 2026-01-31 | ACCEPTED |
| D-003 | User checkpoints after each gate | 2026-01-31 | ACCEPTED |
| D-004 | Auto-retry 2x before user escalation | 2026-01-31 | ACCEPTED |

---

## Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Parent | [FEAT-001](./FEAT-001-research-and-preparation.md) | Parent feature |
| Related | [DEC-001](./FEAT-001--DEC-001-transcript-decisions.md) | Transcript planning decisions |
| Related | [ORCHESTRATION_PLAN.md](./orchestration/ORCHESTRATION_PLAN.md) | Orchestration plan document |
| Related | [ORCHESTRATION.yaml](./orchestration/ORCHESTRATION.yaml) | Machine-readable orchestration state |
| Convention | [.context/templates/worktracker/DECISION.md](../../../../.context/templates/worktracker/DECISION.md) | Decision template |

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-31T18:00:00Z | Claude | Created decision document from execution planning |

---

## Metadata

```yaml
id: "FEAT-001:DEC-002"
parent_id: "FEAT-001"
work_type: DECISION
title: "Orchestration Execution Decisions"
status: ACCEPTED
priority: HIGH
created_by: "Claude"
created_at: "2026-01-31T16:00:00Z"
updated_at: "2026-01-31T18:00:00Z"
decided_at: "2026-01-31T16:30:00Z"
participants: ["User", "Claude"]
tags: ["orchestration", "quality-gates", "execution-strategy", "tiered-execution"]
decision_count: 4
superseded_by: null
supersedes: null
```

---
