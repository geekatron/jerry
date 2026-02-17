# TASK-007: Orchestration SKILL.md Update Content

<!--
DOCUMENT-ID: FEAT-004:EN-307:TASK-007
VERSION: 1.0.0
AGENT: ps-architect-307
DATE: 2026-02-13
STATUS: Complete
PARENT: EN-307 (Orchestration Skill Enhancement - Adversarial Loops)
FEATURE: FEAT-004 (Adversarial Strategy Research & Skill Enhancement)
EPIC: EPIC-002 (Quality Framework Enforcement)
PROJECT: PROJ-001-oss-release
ACTIVITY: DOCUMENTATION
-->

> **Version:** 1.0.0
> **Agent:** ps-architect-307
> **Quality Target:** >= 0.92
> **Purpose:** Define the content to add to the orchestration SKILL.md (v3.0.0) documenting adversarial loop patterns, quality gate configuration, and enhanced capabilities

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this update delivers |
| [Version Bump](#version-bump) | SKILL.md version change |
| [Updated Frontmatter](#updated-frontmatter) | New activation keywords and metadata |
| [New Key Capabilities](#new-key-capabilities) | Additions to Key Capabilities list |
| [New Workflow Pattern Section](#new-workflow-pattern-section) | Pattern 4: Adversarial Feedback Loop |
| [Updated State Schema Section](#updated-state-schema-section) | New ORCHESTRATION.yaml fields |
| [New Adversarial Configuration Section](#new-adversarial-configuration-section) | Quality gate and strategy configuration |
| [Updated Agent Table](#updated-agent-table) | Agent version updates |
| [Updated Constitutional Compliance](#updated-constitutional-compliance) | New compliance entries |
| [Integration Points](#integration-points) | Where new content inserts into existing SKILL.md |
| [Traceability](#traceability) | Mapping to requirements |
| [References](#references) | Source citations |

---

## Summary

This document defines the content additions and modifications needed for the orchestration SKILL.md to document adversarial feedback loop patterns. The updates transform SKILL.md from v2.1.0 to v3.0.0. This document does NOT directly modify the existing SKILL.md file; it specifies the exact content to add, where to add it, and what to modify.

Key additions:
1. **New workflow pattern** (Pattern 4: Adversarial Feedback Loop) alongside existing patterns
2. **Adversarial configuration section** documenting quality gate setup
3. **Updated state schema** with new ORCHESTRATION.yaml fields
4. **Updated agent table** reflecting v3.0.0 capabilities
5. **Updated activation keywords** for adversarial-related triggers

---

## Version Bump

| Field | Old | New |
|-------|-----|-----|
| Version | 2.1.0 | 3.0.0 |
| Description | Multi-agent workflow orchestration with state tracking... | Multi-agent workflow orchestration with state tracking, checkpointing, cross-pollinated pipelines, and adversarial feedback loops... |

---

## Updated Frontmatter

### New Activation Keywords

Add the following to the `activation-keywords` list:

```yaml
activation-keywords:
  # existing:
  - "orchestration"
  - "multi-agent workflow"
  - "pipeline"
  - "cross-pollinated"
  - "sync barrier"
  - "checkpoint"
  - "workflow state"
  - "parallel agents"
  - "agent coordination"
  - "execution tracking"
  # NEW v3.0.0:
  - "adversarial review"
  - "quality gate"
  - "creator-critic-revision"
  - "adversarial feedback loop"
  - "quality score"
  - "adversarial iteration"
```

---

## New Key Capabilities

### Insert After Existing Key Capabilities

Add to the Key Capabilities list in the Purpose section:

```markdown
### Key Capabilities

- **Cross-Pollinated Pipelines** - Bidirectional agent pipelines with barrier synchronization
- **State Management** - YAML-based machine-readable state (SSOT)
- **Checkpoint Recovery** - Resume workflows from any checkpoint
- **Execution Queues** - Priority-ordered agent execution with dependencies
- **Metrics Tracking** - Progress percentages, success rates, timing
- **Adversarial Feedback Loops** - Automatic creator-critic-revision cycles with quality gates [NEW]
- **Quality Gate Enforcement** - Score-based pass/fail at sync barriers with escalation [NEW]
- **Strategy-Based Review** - 10 adversarial strategies assigned by criticality level [NEW]
```

### Updated "When to Use" Section

Add to the "Activate when" list:

```markdown
Activate when:

- Coordinating **3+ agents** in a structured workflow
- Running **parallel pipelines** that need synchronization
- Workflow spans **multiple sessions** and needs state persistence
- Need **checkpointing** for long-running processes
- Require **visibility** into complex workflow progress
- Workflow artifacts need **adversarial quality review** [NEW]
- Quality gates needed at **sync barriers** before cross-pollination [NEW]
```

---

## New Workflow Pattern Section

### Pattern 4: Adversarial Feedback Loop

Insert as a new pattern after the existing Pattern 3 (Fan-Out/Fan-In):

```markdown
### Pattern 4: Adversarial Feedback Loop

Creator-critic-revision cycles with quality gate enforcement. Automatically embedded when adversarial validation is enabled.

```
┌──────────┐
│ Creator  │ ← Produces initial artifacts
└────┬─────┘
     │
     ▼
┌──────────┐     ┌──────────┐
│ Critic   │────►│ Revision │ ← Iteration 1
│ (S-002,  │     │ (address │
│  S-014)  │     │ findings)│
└──────────┘     └────┬─────┘
                      │
                      ▼
                ┌──────────┐     ┌──────────┐
                │ Critic   │────►│ Revision │ ← Iteration 2
                │ (S-007,  │     │ (address │
                │  S-014)  │     │ findings)│
                └──────────┘     └────┬─────┘
                                      │
                                      ▼
                                ┌──────────┐
                                │  Critic  │ ← Iteration 3 (scoring)
                                │  (S-001, │   May be SKIPPED if
                                │   S-014) │   score >= 0.92
                                └────┬─────┘
                                     │
                                     ▼
                               ┌───────────┐
                               │ Validator  │ ← Final quality verdict
                               └───────────┘
```

**Key features:**
- **Automatic injection:** Orch-planner auto-generates this pattern for qualifying phases
- **Quality gate:** >= 0.92 threshold (from quality-enforcement.md SSOT)
- **Minimum 3 iterations:** H-14 enforcement, with early exit at iteration 2 if threshold met
- **Strategy assignment:** Based on C1-C4 criticality level
- **S-014 LLM-as-Judge:** Required at every iteration for scoring (H-15)
- **P-003 compliant:** All agents (creator, critic, validator) are workers of the orchestrator

**Configuration:**
```yaml
workflow:
  constraints:
    adversarial_validation: true
    quality_gate_threshold: 0.92
    adversarial_iteration_min: 3
  patterns:
    - ADVERSARIAL_FEEDBACK
```
```

---

## Updated State Schema Section

### New Fields in ORCHESTRATION.yaml Structure

Add the following to the State Schema section:

```markdown
### ORCHESTRATION.yaml Structure (v3.0.0)

```yaml
workflow:
  id: string
  name: string
  project_id: string
  status: ACTIVE|PAUSED|COMPLETE|FAILED
  constraints:                              # [NEW v3.0.0]
    quality_gate_threshold: 0.92            # Quality gate score
    adversarial_iteration_min: 3            # Minimum iterations
    adversarial_validation: true            # Enable adversarial loops
    criticality_default: "C2"              # Default criticality level
  patterns:                                 # [NEW v3.0.0]
    - ADVERSARIAL_FEEDBACK                  # Pattern flag

pipelines:
  {pipeline_id}:
    current_phase: number
    phases:
      - id: number
        name: string
        status: PENDING|IN_PROGRESS|COMPLETE|BLOCKED
        criticality: "C1"|"C2"|"C3"|"C4"   # [NEW] Decision criticality
        quality_scores: [float]              # [NEW] Score per iteration
        final_quality_score: float           # [NEW] Final achieved score
        validation_verdict: string           # [NEW] PASS|CONDITIONAL PASS|FAIL
        agents:
          - id: string
            status: PENDING|IN_PROGRESS|COMPLETE|FAILED|SKIPPED
            artifact: string
            role: "creator"|"critic"|"validator"  # [NEW] Agent role
            adversarial_strategies: [string]       # [NEW] Assigned strategies

execution_queue:
  current_group: number
  groups:
    - id: number
      execution_mode: PARALLEL|SEQUENTIAL
      agents: [agent_ids]
      adversarial_context:                  # [NEW v3.0.0]
        cycle_phase: string                 # creator|critic|revision|validation
        iteration: number                   # Current iteration
        max_iterations: number              # Maximum iterations
        quality_threshold: float            # Gate threshold
        strategies: [string]                # Strategies for this group
      iterations:                           # [NEW v3.0.0]
        - iteration: number
          status: PENDING|COMPLETE|SKIPPED
          scores: {enabler: score}
          delta: {enabler: delta}
          findings_resolved: {enabler: summary}

metrics:
  phases_complete: number
  phases_total: number
  agents_executed: number
  agents_total: number
  quality:                                  # [NEW v3.0.0]
    adversarial_iterations_completed: number
    adversarial_iterations_total: number
    quality_scores:
      - enabler: string
        iteration_1: float
        iteration_2: float
        validation: string

resumption:
  adversarial_feedback_status:              # [NEW v3.0.0]
    total_enablers: number
    enablers_complete: number
    enablers_validated: number
    current_enabler: string
    current_iteration: string
```
```

---

## New Adversarial Configuration Section

### Insert After "Workflow Configuration" Section

```markdown
## Adversarial Configuration

### Enabling Adversarial Feedback Loops

Adversarial feedback loops are enabled by default for new workflows (NFR-307-003). To configure:

```yaml
workflow:
  constraints:
    adversarial_validation: true       # Enable (default for new workflows)
    quality_gate_threshold: 0.92       # Score required to pass
    adversarial_iteration_min: 3       # Minimum review iterations
    criticality_default: "C2"          # Default criticality if not per-phase
```

### Opting Out

Per P-020 (User Authority), adversarial loops can be disabled:

**Workflow-level opt-out:**
```yaml
workflow:
  constraints:
    adversarial_validation: false      # Disables all adversarial loops
```

**Phase-level opt-out:**
```yaml
phases:
  - id: 1
    adversarial_review: false          # This phase only
```

### Criticality Levels

Criticality determines adversarial review intensity:

| Level | Description | Strategies | Token Budget |
|-------|-------------|-----------|--------------|
| C1 | Routine | S-010 only | Ultra-Low (1,600-2,100) |
| C2 | Significant | 2-3 per iteration | Low-Medium (8,000-20,000) |
| C3 | Major | 3-5 per iteration | Medium (15,000-40,000) |
| C4 | Critical | All 10 (phased) | High (40,000-80,000) |

### Strategy Pool

The 10 adversarial strategies available for assignment (from ADR-EPIC002-001):

| Code | Strategy | Primary Use |
|------|----------|------------|
| S-014 | LLM-as-Judge | Scoring (required every iteration) |
| S-002 | Devil's Advocate | Challenge assumptions |
| S-003 | Steelman | Strengthen arguments |
| S-004 | Pre-Mortem | Failure scenario analysis |
| S-007 | Constitutional AI | Rule compliance checking |
| S-010 | Self-Refine | Self-improvement (C1) |
| S-001 | Red Team | Adversarial attack simulation |
| S-011 | CoVe | Verification chain |
| S-012 | FMEA | Failure mode analysis |
| S-013 | Inversion | Reverse assumption testing |

### Quality Gate Decision Matrix

| Score | At Max Iterations? | Result | Action |
|-------|-------------------|--------|--------|
| >= 0.92 | Any | PASS | Proceed to next phase |
| < 0.92 | No | CONTINUE | Next iteration |
| 0.85-0.91 | Yes | CONDITIONAL PASS | User ratification required |
| < 0.85 | Yes | FAIL | Blocker created, phase blocked |
```

---

## Updated Agent Table

```markdown
## Available Agents

| Agent | Version | Role | Output |
|-------|---------|------|--------|
| `orch-planner` | **3.0.0** | Creates orchestration plan with **adversarial cycles** | `ORCHESTRATION_PLAN.md` |
| `orch-tracker` | **3.0.0** | Updates execution state and **quality scores** | `ORCHESTRATION.yaml`, `ORCHESTRATION_WORKTRACKER.md` |
| `orch-synthesizer` | **3.0.0** | Creates final workflow synthesis **with adversarial analysis** | `synthesis/workflow-synthesis.md` |
```

---

## Updated Constitutional Compliance

Add to the Constitutional Compliance table:

```markdown
## Constitutional Compliance

| Principle | Requirement | Implementation |
|-----------|-------------|----------------|
| P-002 | File Persistence | All state persisted to ORCHESTRATION.yaml |
| P-003 | No Recursive Subagents | Main context invokes workers only (creator, critic, validator are all workers) |
| P-010 | Task Tracking | ORCHESTRATION_WORKTRACKER.md updated |
| P-020 | User Authority | Adversarial opt-out supported; CONDITIONAL PASS requires user ratification |
| P-022 | No Deception | Honest status, quality scores, and progress reporting |
| H-13 | Quality Gate Threshold | >= 0.92 enforced from quality-enforcement.md SSOT |
| H-14 | Minimum Iterations | 3 creator-critic-revision iterations minimum |
| H-15 | S-014 Required | LLM-as-Judge scoring at every adversarial iteration |
| H-16 | Anti-Leniency | Calibration required for all critic agents |
```

---

## Integration Points

### Where Content Inserts into Existing SKILL.md

| New Content | Insert Location | Type |
|-------------|----------------|------|
| Activation keywords | `activation-keywords` in frontmatter | Append |
| Adversarial capabilities | After existing Key Capabilities list | Append |
| "When to use" additions | After existing activation list | Append |
| Pattern 4 diagram | After Pattern 3 (Fan-Out/Fan-In) | Insert new section |
| Adversarial Configuration | After "Workflow Configuration" section | Insert new section |
| Updated state schema fields | Within existing State Schema section | Extend |
| Updated agent table | Replace existing agent table | Replace |
| Constitutional compliance additions | Append to existing table | Append |
| v3.0.0 version footer | Replace version in footer | Replace |

### Sections NOT Modified

The following existing sections remain unchanged:
- Purpose (core description)
- Core Artifacts table
- P-003 Compliance section
- Pattern 1 (Cross-Pollinated Pipeline)
- Pattern 2 (Sequential with Checkpoints)
- Pattern 3 (Fan-Out/Fan-In)
- Quick Start (steps 1-3)
- Tool Invocation Examples
- Templates table
- References

---

## Traceability

| Requirement | Content Section | Status |
|-------------|----------------|--------|
| NFR-307-007 | All sections (documentation completeness) | Covered |
| NFR-307-008 | New Workflow Pattern Section (live example) | Covered |
| NFR-307-001 | Adversarial Configuration (opt-out, backward compat) | Covered |
| NFR-307-002 | Adversarial Configuration (opt-out mechanism) | Covered |
| NFR-307-003 | Adversarial Configuration (default-on) | Covered |
| NFR-307-005 | Updated Constitutional Compliance (P-003) | Covered |
| NFR-307-006 | Adversarial Configuration (platform portability) | Covered |

---

## References

| # | Citation | Sections Referenced |
|---|----------|-------------------|
| 1 | FEAT-004:EN-307:TASK-001 (Requirements) | NFR-307-001 through NFR-307-008 |
| 2 | FEAT-004:EN-307:TASK-002 (Planner Design) | Pattern injection, strategy selection |
| 3 | FEAT-004:EN-307:TASK-003 (Tracker Design) | Quality gate logic, score aggregation |
| 4 | Orchestration SKILL.md v2.1.0 | Baseline for integration points |
| 5 | ADR-EPIC002-001 | Strategy pool, C1-C4 criticality |
| 6 | Barrier-2 ENF-to-ADV Handoff | H-13 through H-16 |

---

*Document ID: FEAT-004:EN-307:TASK-007*
*Agent: ps-architect-307*
*Created: 2026-02-13*
*Status: Complete*
