# EN-001 Jerry Prompt Effectiveness Research: Orchestration Plan

> **Document ID:** PROJ-006-ORCH-PLAN
> **Project:** PROJ-006-jerry-prompt
> **Spike:** EN-001 - Research Effective Jerry Prompt Patterns
> **Workflow ID:** `prompt-research-20260218-001`
> **Status:** PLANNED
> **Version:** 1.0
> **Created:** 2026-02-18
> **Last Updated:** 2026-02-18

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Workflow Overview](#l0-workflow-overview) | High-level summary for stakeholders |
| [L1: Technical Plan](#l1-technical-plan) | Workflow diagram, phases, agents, barriers |
| [L2: Implementation Details](#l2-implementation-details) | State schema, path configuration, recovery strategies |
| [Execution Constraints](#execution-constraints) | Constitutional and soft constraints |
| [Success Criteria](#success-criteria) | Phase exit and workflow completion criteria |
| [Risk Mitigations](#risk-mitigations) | Risk analysis and mitigations |
| [Resumption Context](#resumption-context) | Current state and next actions |
| [Disclaimer](#disclaimer) | Agent-generated output notice |

---

## 1. Executive Summary

This orchestration plan coordinates a structured research workflow for EN-001 (Research Effective Jerry Prompt Patterns). The workflow deploys all 9 problem-solving agents across 3 sequential phases, each gated by an adversarial critic checkpoint requiring a quality score >= 0.92. The research question is: **"What prompts are most effective when working with Jerry?"**

**Current State:** Workflow not started. All phases in BACKLOG.

**Orchestration Pattern:** Sequential Pipeline with Critic Checkpoints (Pattern 2) — three phases with full adversarial critique gates between each transition.

### 1.1 Workflow Identification

| Field | Value | Source |
|-------|-------|--------|
| Workflow ID | `prompt-research-20260218-001` | auto-generated |
| ID Format | `{purpose}-{YYYYMMDD}-{NNN}` | semantic-date-seq |
| Base Path | `projects/PROJ-006-jerry-prompt/orchestration/prompt-research-20260218-001/` | Dynamic |

**Artifact Output Locations:**

| Layer | Path |
|-------|------|
| Orchestration base | `projects/PROJ-006-jerry-prompt/orchestration/prompt-research-20260218-001/` |
| Phase 1 pipeline artifacts | `projects/PROJ-006-jerry-prompt/orchestration/prompt-research-20260218-001/ps/phase-1-discovery/` |
| Phase 2 pipeline artifacts | `projects/PROJ-006-jerry-prompt/orchestration/prompt-research-20260218-001/ps/phase-2-analysis/` |
| Phase 3 pipeline artifacts | `projects/PROJ-006-jerry-prompt/orchestration/prompt-research-20260218-001/ps/phase-3-synthesis/` |
| Gates | `projects/PROJ-006-jerry-prompt/orchestration/prompt-research-20260218-001/gates/` |
| Phase 1 project outputs | `projects/PROJ-006-jerry-prompt/research/` |
| Phase 2 project outputs | `projects/PROJ-006-jerry-prompt/analysis/` |
| Phase 3 project outputs | `projects/PROJ-006-jerry-prompt/synthesis/` |

---

## L0: Workflow Overview

This workflow uses Jerry's own problem-solving skill to research what makes a Jerry prompt effective. The research question — "What prompts are most effective when working with Jerry?" — is investigated through three sequential phases: Discovery (gather evidence), Analysis (find patterns), and Synthesis (produce guidance).

Each phase uses specialist agents suited to the work: researchers and investigators gather evidence, analysts and architects decode patterns, synthesizers and reporters produce final deliverables. At every phase boundary, an adversarial critic challenges the work and a reviewer validates quality. No phase advances until quality score reaches 0.92 or above on a 0–1 scale.

The output of this workflow is a best-practices guide with at least three prompt templates, a quality rubric, and a catalog of effective and anti-patterns — ready for inclusion in Jerry's documentation.

**Delivery:** `projects/PROJ-006-jerry-prompt/synthesis/` — best-practices guide, template library, quality rubric.

---

## L1: Technical Plan

### 2.1 Pipeline Diagram

```
PIPELINE: ps (problem-solving)
══════════════════════════════════════════════════════════════════════════════════

PHASE 1: Discovery — Survey, investigate, gather primary corpus
────────────────────────────────────────────────────────────────────────────────

 ┌────────────────────────────────┐
 │ ps-researcher                  │  STEP 1a: EXTERNAL SURVEY
 │ Survey Anthropic prompt docs,  │  Gather prompt engineering literature,
 │ academic sources, industry     │  industry guides, LLM best practices
 │ best practices                 │
 └───────────────┬────────────────┘
                 │ (concurrent)
 ┌───────────────▼────────────────┐
 │ ps-investigator                │  STEP 1b: INTERNAL INVESTIGATION
 │ Analyze Jerry CLAUDE.md,       │  Deep analysis of Jerry's own skill
 │ skill files, agent specs,      │  architecture, user prompt example,
 │ orchestration examples,        │  how skills/agents are invoked
 │ user example prompt            │
 └───────────────┬────────────────┘
                 │
                 ▼
╔═══════════════════════════════════════════════════════════════════════════════╗
║                         CRITIC GATE 1 (quality >= 0.92)                      ║
║  ┌─────────────────────────────────────────────────────────────────────────┐ ║
║  │ ps-critic:   Adversarial review — probe for coverage gaps, weak         │ ║
║  │              evidence, selection bias, missing domains                  │ ║
║  │ ps-reviewer: Quality review — evidence quality, source credibility,     │ ║
║  │              completeness of corpus                                     │ ║
║  │ Condition:   quality_score >= 0.92 OR iterate with feedback             │ ║
║  │ Artifact:    gates/gate-1/gate-1-result.md                              │ ║
║  └─────────────────────────────────────────────────────────────────────────┘ ║
║  STATUS: PENDING                                                              ║
╚═══════════════════════════════════════════════════════════════════════════════╝
                 │ Gate PASS
                 ▼

PHASE 2: Analysis — Pattern recognition, rubric design, taxonomy
────────────────────────────────────────────────────────────────────────────────

 ┌────────────────────────────────┐
 │ ps-analyst                     │  STEP 2a: PATTERN ANALYSIS
 │ Categorize prompt structures,  │  Identify effectiveness correlations,
 │ identify what traits produce   │  analyze skill invocation patterns,
 │ high-quality outcomes          │  quantify anti-pattern frequency
 └───────────────┬────────────────┘
                 │ (concurrent)
 ┌───────────────▼────────────────┐
 │ ps-architect                   │  STEP 2b: RUBRIC + TAXONOMY DESIGN
 │ Design prompt quality rubric   │  Define measurable evaluation criteria,
 │ and pattern taxonomy           │  create classification system for
 │                                │  prompt types and effectiveness tiers
 └───────────────┬────────────────┘
                 │
                 ▼
╔═══════════════════════════════════════════════════════════════════════════════╗
║                         CRITIC GATE 2 (quality >= 0.92)                      ║
║  ┌─────────────────────────────────────────────────────────────────────────┐ ║
║  │ ps-critic:    Adversarial challenge — attack analysis rigor, probe for  │ ║
║  │               confounds, challenge rubric subjectivity, find edge cases │ ║
║  │ ps-validator: Validate analysis completeness, verify rubric measurabil- │ ║
║  │               ity, confirm taxonomy covers observed prompt diversity     │ ║
║  │ Condition:    quality_score >= 0.92 OR iterate with feedback             │ ║
║  │ Artifact:     gates/gate-2/gate-2-result.md                             │ ║
║  └─────────────────────────────────────────────────────────────────────────┘ ║
║  STATUS: BLOCKED                                                              ║
╚═══════════════════════════════════════════════════════════════════════════════╝
                 │ Gate PASS
                 ▼

PHASE 3: Synthesis — Best-practices guide, templates, executive summary
────────────────────────────────────────────────────────────────────────────────

 ┌────────────────────────────────┐
 │ ps-synthesizer                 │  STEP 3a: SYNTHESIS
 │ Compile findings into          │  Integrate Phase 1 evidence with
 │ comprehensive best-practices   │  Phase 2 patterns and rubric into
 │ guide with anti-patterns       │  coherent, actionable guidance doc
 └───────────────┬────────────────┘
                 │
 ┌───────────────▼────────────────┐
 │ ps-reporter                    │  STEP 3b: DELIVERABLES
 │ Create prompt template library │  Produce >= 3 templates, executive
 │ and executive summary          │  summary, quality rubric card
 └───────────────┬────────────────┘
                 │
                 ▼
╔═══════════════════════════════════════════════════════════════════════════════╗
║                         CRITIC GATE 3 (quality >= 0.92)                      ║
║  ┌─────────────────────────────────────────────────────────────────────────┐ ║
║  │ ps-critic:    Final adversarial review — challenge all outputs, verify  │ ║
║  │               templates are actionable, probe for internal consistency  │ ║
║  │ ps-validator: Validate templates are complete and acceptance criteria   │ ║
║  │               for EN-001 are met                                        │ ║
║  │ Condition:    quality_score >= 0.92 OR iterate with feedback             │ ║
║  │ Artifact:     gates/gate-3/gate-3-result.md                             │ ║
║  └─────────────────────────────────────────────────────────────────────────┘ ║
║  STATUS: BLOCKED                                                              ║
╚═══════════════════════════════════════════════════════════════════════════════╝
                 │ Gate PASS
                 ▼
       ┌─────────────────────────┐
       │    WORKFLOW COMPLETE     │
       │  EN-001 SPIKE RESOLVED  │
       └─────────────────────────┘
```

### 2.2 Orchestration Pattern Classification

| Pattern | Applied | Description |
|---------|---------|-------------|
| Sequential Pipeline | Yes | Phases 1 → 2 → 3 must execute in order |
| Critic Checkpoints | Yes | Each phase boundary has adversarial gate (>= 0.92) |
| Concurrent Sub-tasks | Yes | Phase 1: researcher + investigator run concurrently; Phase 2: analyst + architect run concurrently |
| Iteration Loops | Yes | Gate failure triggers feedback loop back to phase agents |
| Hierarchical | Yes | Orchestrator delegates to worker agents (P-003 compliant) |

---

## 3. Phase Definitions

### 3.1 Pipeline: ps (problem-solving)

| Phase | Name | Purpose | Agents | Status |
|-------|------|---------|--------|--------|
| 1 | Discovery | Gather prompt examples, analyze Jerry internals, survey external prompt engineering research | ps-researcher, ps-investigator | PENDING |
| GATE 1 | Discovery Critic Gate | Adversarial challenge of Phase 1 completeness and evidence quality | ps-critic, ps-reviewer | PENDING |
| 2 | Analysis | Deconstruct prompt anatomy, identify patterns, correlate prompt traits with quality outcomes | ps-analyst, ps-architect | BLOCKED |
| GATE 2 | Analysis Critic Gate | Adversarial challenge of analysis rigor and rubric validity | ps-critic, ps-validator | BLOCKED |
| 3 | Synthesis | Produce best-practices guide, prompt templates, quality rubric | ps-synthesizer, ps-reporter | BLOCKED |
| GATE 3 | Synthesis Critic Gate | Final adversarial review of all deliverables | ps-critic, ps-validator | BLOCKED |

---

## 4. Adversarial Critic Gate Protocol

### 4.1 Gate Criteria

All gates use the same adversarial critique framework with a **quality threshold of 0.92**. Gate failure triggers an iteration loop: agents are sent back to their phase with specific feedback, then re-submitted for gate review.

```
GATE EXECUTION SEQUENCE
════════════════════════

1. ps-critic performs ADVERSARIAL CHALLENGE using all 4 modes:
   └─ Devil's Advocate: "What if this research assumption is wrong?"
   └─ Steelman:         "What is the strongest objection to these findings?"
   └─ Red Team:         "How could this analysis be gamed or manipulated?"
   └─ Blue Team:        "Defend what is working well and why"

2. ps-reviewer / ps-validator performs QUALITY REVIEW:
   └─ Evidence quality and source credibility
   └─ Coverage completeness (no major gaps)
   └─ Internal consistency
   └─ Actionability of outputs

3. Scoring:
   └─ Combined quality_score computed (see evaluation criteria below)
   └─ If quality_score >= 0.92: GATE PASSES → advance to next phase
   └─ If quality_score < 0.92: GATE FAILS → feedback issued, phase agents iterate

4. Gate result artifact persisted to:
   └─ gates/gate-{N}/gate-{N}-result.md
```

### 4.2 Quality Evaluation Criteria

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Completeness | 0.30 | All required topics covered; no major gaps in evidence or output |
| Accuracy | 0.25 | Claims are evidence-based; sources credible; reasoning sound |
| Rigor | 0.20 | Methodology is systematic; patterns are distinguishable from noise |
| Actionability | 0.15 | Outputs are usable by Jerry users without further interpretation |
| Consistency | 0.10 | Internal consistency; no contradictions between sections |

### 4.3 Gate Definitions

| Gate | After Phase | Critics | Reviewers | Threshold | Status |
|------|-------------|---------|-----------|-----------|--------|
| gate-1 | Phase 1 (Discovery) | ps-critic | ps-reviewer | >= 0.92 | PENDING |
| gate-2 | Phase 2 (Analysis) | ps-critic | ps-validator | >= 0.92 | BLOCKED |
| gate-3 | Phase 3 (Synthesis) | ps-critic | ps-validator | >= 0.92 | BLOCKED |

### 4.4 Iteration Rules

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Max iterations per gate | 2 | Prevents infinite loops; 3rd failure escalates to user |
| Iteration delay | None | Agents revise immediately on feedback |
| Escalation trigger | >= 3 failed attempts at same gate | Research complexity may require scope reduction or user input |

---

## 5. Agent Registry

### 5.1 Phase 1 Agents (Discovery)

| Agent ID | Role | Responsibility | Output Artifact | Status |
|----------|------|---------------|----------------|--------|
| ps-researcher | External Surveyor | Survey Anthropic prompt engineering docs, academic sources, prompt engineering guides, LLM behavior research | `ps/phase-1-discovery/ps-researcher/ps-researcher-survey.md` | PENDING |
| ps-investigator | Internal Investigator | Analyze Jerry's CLAUDE.md, skill files (all 5 skills), agent specs, orchestration examples, decode the user's example prompt | `ps/phase-1-discovery/ps-investigator/ps-investigator-investigation.md` | PENDING |

**Phase 1 project-level outputs:** `projects/PROJ-006-jerry-prompt/research/`

### 5.2 Gate 1 Agents (Discovery Critic Gate)

| Agent ID | Role | Responsibility | Output Artifact | Status |
|----------|------|---------------|----------------|--------|
| ps-critic | Adversarial Critic | Challenge discovery completeness, probe for coverage gaps, weak evidence, selection bias | `gates/gate-1/gate-1-ps-critic-challenge.md` | PENDING |
| ps-reviewer | Quality Reviewer | Assess evidence quality, source credibility, corpus completeness | `gates/gate-1/gate-1-ps-reviewer-review.md` | PENDING |

**Gate result:** `gates/gate-1/gate-1-result.md`

### 5.3 Phase 2 Agents (Analysis)

| Agent ID | Role | Responsibility | Output Artifact | Status |
|----------|------|---------------|----------------|--------|
| ps-analyst | Pattern Analyst | Categorize prompt structures, identify effectiveness correlations, map skill invocation patterns, quantify anti-pattern frequency | `ps/phase-2-analysis/ps-analyst/ps-analyst-analysis.md` | BLOCKED |
| ps-architect | Rubric + Taxonomy Designer | Design prompt quality rubric with measurable criteria; create classification taxonomy for prompt types and effectiveness tiers | `ps/phase-2-analysis/ps-architect/ps-architect-rubric-taxonomy.md` | BLOCKED |

**Phase 2 project-level outputs:** `projects/PROJ-006-jerry-prompt/analysis/`

### 5.4 Gate 2 Agents (Analysis Critic Gate)

| Agent ID | Role | Responsibility | Output Artifact | Status |
|----------|------|---------------|----------------|--------|
| ps-critic | Adversarial Critic | Attack analysis rigor, probe for confounds, challenge rubric subjectivity, find edge cases | `gates/gate-2/gate-2-ps-critic-challenge.md` | BLOCKED |
| ps-validator | Completeness Validator | Validate analysis completeness, verify rubric measurability, confirm taxonomy covers observed diversity | `gates/gate-2/gate-2-ps-validator-validation.md` | BLOCKED |

**Gate result:** `gates/gate-2/gate-2-result.md`

### 5.5 Phase 3 Agents (Synthesis)

| Agent ID | Role | Responsibility | Output Artifact | Status |
|----------|------|---------------|----------------|--------|
| ps-synthesizer | Synthesis Author | Compile Phase 1 evidence and Phase 2 patterns into a comprehensive best-practices guide including anti-patterns | `ps/phase-3-synthesis/ps-synthesizer/ps-synthesizer-guide.md` | BLOCKED |
| ps-reporter | Report Author | Create prompt template library (>= 3 templates), executive summary for stakeholders, quality rubric card | `ps/phase-3-synthesis/ps-reporter/ps-reporter-deliverables.md` | BLOCKED |

**Phase 3 project-level outputs:** `projects/PROJ-006-jerry-prompt/synthesis/`

### 5.6 Gate 3 Agents (Synthesis Critic Gate — Final)

| Agent ID | Role | Responsibility | Output Artifact | Status |
|----------|------|---------------|----------------|--------|
| ps-critic | Adversarial Critic | Final adversarial review — challenge all outputs, verify templates are actionable, probe for internal consistency | `gates/gate-3/gate-3-ps-critic-challenge.md` | BLOCKED |
| ps-validator | Completeness Validator | Validate templates meet EN-001 acceptance criteria, confirm deliverables are complete and usable | `gates/gate-3/gate-3-ps-validator-validation.md` | BLOCKED |

**Gate result:** `gates/gate-3/gate-3-result.md`

---

## L2: Implementation Details

### 6.1 State Schema (ORCHESTRATION.yaml)

See companion file: `projects/PROJ-006-jerry-prompt/ORCHESTRATION.yaml`

The YAML state file is the single source of truth (SSOT) for machine-readable workflow state. It tracks:
- Workflow metadata and status
- Pipeline and phase progression
- Agent execution status and artifact paths
- Gate conditions and results
- Execution queue ordering
- Checkpoints for recovery

### 6.2 Dynamic Path Configuration

All artifact paths use dynamic identifiers. No hardcoded pipeline names in paths.

```
projects/PROJ-006-jerry-prompt/
├── orchestration/
│   └── prompt-research-20260218-001/         # Workflow ID (dynamic)
│       ├── ps/                                # Pipeline alias
│       │   ├── phase-1-discovery/             # Phase 1
│       │   │   ├── ps-researcher/
│       │   │   │   └── ps-researcher-survey.md
│       │   │   └── ps-investigator/
│       │   │       └── ps-investigator-investigation.md
│       │   ├── phase-2-analysis/              # Phase 2
│       │   │   ├── ps-analyst/
│       │   │   │   └── ps-analyst-analysis.md
│       │   │   └── ps-architect/
│       │   │       └── ps-architect-rubric-taxonomy.md
│       │   └── phase-3-synthesis/             # Phase 3
│       │       ├── ps-synthesizer/
│       │       │   └── ps-synthesizer-guide.md
│       │       └── ps-reporter/
│       │           └── ps-reporter-deliverables.md
│       ├── gates/                             # Critic gate artifacts
│       │   ├── gate-1/
│       │   │   ├── gate-1-ps-critic-challenge.md
│       │   │   ├── gate-1-ps-reviewer-review.md
│       │   │   └── gate-1-result.md           # PASS/FAIL + score
│       │   ├── gate-2/
│       │   │   ├── gate-2-ps-critic-challenge.md
│       │   │   ├── gate-2-ps-validator-validation.md
│       │   │   └── gate-2-result.md
│       │   └── gate-3/
│       │       ├── gate-3-ps-critic-challenge.md
│       │       ├── gate-3-ps-validator-validation.md
│       │       └── gate-3-result.md
│       ├── ORCHESTRATION_PLAN.md              # This file
│       └── ORCHESTRATION.yaml                 # Machine-readable state
├── research/                                  # Phase 1 project-level outputs
├── analysis/                                  # Phase 2 project-level outputs
└── synthesis/                                 # Phase 3 project-level outputs
```

**Path Construction Rules:**
- Workflow base: `projects/PROJ-006-jerry-prompt/orchestration/{workflow_id}/`
- Pipeline alias: `ps` (derived from skill source: `problem-solving`)
- Phase ID: `phase-{N}-{kebab-slug}`
- Agent isolation: `{agent-id}/` subdirectory per agent
- Artifact filename: `{agent-id}-{artifact-type}.md`
- Gate artifacts: `gates/gate-{N}/{agent-id}-{role}.md`

### 6.3 Recovery Strategies

| Failure Mode | Detection | Recovery |
|--------------|-----------|----------|
| Agent execution failure | Agent status = FAILED in YAML | Re-run agent from last checkpoint with same inputs |
| Gate score < 0.92 | Gate result = FAIL in gate artifact | Feed specific critique back to phase agents; re-run; re-submit for gate |
| Gate iteration limit exceeded | Iteration count >= 3 | Escalate to user with gate feedback summary |
| Missing source artifact | Agent reports input not found | Identify which agent should produce it; re-run that agent first |
| Self-referential bias detected | ps-critic flags bias in Gate 2/3 | Introduce additional external reference sources in Phase 2/3 input |

### 6.4 Checkpoint Strategy

| Trigger | When | Purpose |
|---------|------|---------|
| PHASE_1_COMPLETE | After Gate 1 passes | Preserve Discovery corpus before Analysis begins |
| PHASE_2_COMPLETE | After Gate 2 passes | Preserve rubric/taxonomy before Synthesis begins |
| WORKFLOW_COMPLETE | After Gate 3 passes | Final state snapshot; EN-001 resolved |

---

## Execution Constraints

### Hard Constraints (Jerry Constitution)

| Constraint | ID | Enforcement |
|------------|----|----|
| Single agent nesting | P-003 | Orchestrator -> Worker only. No agent spawns sub-agents. |
| File persistence | P-002 | All state and artifacts to filesystem |
| No deception | P-022 | Transparent reasoning. Critique issues not hidden. |
| User authority | P-020 | User approves escalations. User can override any gate. |

### Soft Constraints

| Constraint | Value | Rationale |
|------------|-------|-----------|
| Max concurrent agents | 2 | Researcher + Investigator in Phase 1; Analyst + Architect in Phase 2 |
| Max gate iterations | 2 | 3rd failure escalates to user |
| Checkpoint frequency | PHASE | Recovery at phase gate boundaries |
| Quality threshold | 0.92 | Higher than standard 0.85 for research quality |
| Evidence sources | >= 4 | At least 4 distinct sources to reduce single-source bias |

---

## Success Criteria

### Phase 1 Exit Criteria (requires Gate 1 PASS)

| Criterion | Evidence |
|-----------|----------|
| External prompt engineering survey complete | ps-researcher artifact present with >= 4 cited sources |
| Jerry internals fully analyzed | ps-investigator artifact covers CLAUDE.md, all 5 skill files, agent specs |
| User example prompt deconstructed | ps-investigator artifact includes anatomy of example prompt |
| Gate 1 quality score >= 0.92 | gate-1-result.md shows PASS with score |

### Phase 2 Exit Criteria (requires Gate 2 PASS)

| Criterion | Evidence |
|-----------|----------|
| Prompt structure categories documented | ps-analyst artifact with taxonomy table |
| Effectiveness correlations identified | ps-analyst artifact with correlation mapping |
| Quality rubric designed | ps-architect artifact with measurable criteria |
| Pattern taxonomy created | ps-architect artifact with classification system |
| Gate 2 quality score >= 0.92 | gate-2-result.md shows PASS with score |

### Phase 3 Exit Criteria (requires Gate 3 PASS)

| Criterion | Evidence |
|-----------|----------|
| Best-practices guide complete | ps-synthesizer artifact in synthesis/ directory |
| Anti-patterns documented | Best-practices guide includes anti-patterns section |
| >= 3 prompt templates created | ps-reporter artifact with template library |
| Executive summary produced | ps-reporter artifact includes stakeholder summary |
| Gate 3 quality score >= 0.92 | gate-3-result.md shows PASS with score |

### Workflow Completion Criteria (EN-001 Resolution)

| Criterion | Verification |
|-----------|-------------|
| All phases COMPLETE | All phase status = COMPLETE in ORCHESTRATION.yaml |
| All gates PASS | gate-1, gate-2, gate-3 all show PASS in result artifacts |
| EN-001 acceptance criteria met | All 7 items in EN-001 Definition of Done checked |
| Deliverables persisted | research/, analysis/, synthesis/ directories populated |

---

## Risk Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| "Effectiveness" too subjective to measure | High | Medium | ps-architect designs rubric with objective, measurable criteria in Phase 2 before synthesis begins |
| Limited prompt corpus (few real examples) | Medium | Medium | ps-investigator mines Jerry's own orchestration history + skill invocation patterns as proxy corpus |
| Self-referential bias (Jerry researching Jerry) | Medium | Low | ps-researcher explicitly targets external sources; ps-critic is tasked with bias detection at every gate |
| Gate iteration deadlock | Low | Medium | Max 2 iterations before user escalation; user can approve partial pass |
| Phase 2 rubric too complex to be actionable | Medium | High | ps-critic specifically attacks rubric complexity at Gate 2; actionability weighted 0.15 in scoring |
| Phase 3 templates too generic | Medium | Medium | ps-reporter receives rubric as explicit input; ps-validator checks template specificity |

---

## Resumption Context

### Current Execution State

```
WORKFLOW STATUS AS OF 2026-02-18
=================================

Workflow ID: prompt-research-20260218-001
Pipeline: ps

  Phase 1 (Discovery):    PENDING
  Gate 1 (Discovery):     PENDING
  Phase 2 (Analysis):     BLOCKED (by Gate 1)
  Gate 2 (Analysis):      BLOCKED (by Phase 2)
  Phase 3 (Synthesis):    BLOCKED (by Gate 2)
  Gate 3 (Final):         BLOCKED (by Phase 3)

Overall Progress: 0%
```

### Next Actions

1. Execute ps-researcher: Survey external prompt engineering documentation and research
2. Execute ps-investigator (concurrent): Analyze Jerry internals — CLAUDE.md, skill files, agent specs, orchestration examples, example prompt
3. Execute ps-critic: Adversarial review of Phase 1 discovery completeness
4. Execute ps-reviewer: Quality review of evidence and source coverage
5. Evaluate Gate 1: If score >= 0.92, advance; else iterate with feedback
6. Execute ps-analyst: Pattern analysis of Phase 1 findings
7. Execute ps-architect (concurrent): Design rubric and taxonomy
8. Execute ps-critic: Adversarial challenge of analysis rigor
9. Execute ps-validator: Validate analysis completeness
10. Evaluate Gate 2: If score >= 0.92, advance; else iterate with feedback
11. Execute ps-synthesizer: Compile best-practices guide
12. Execute ps-reporter: Produce template library and executive summary
13. Execute ps-critic: Final adversarial review of all deliverables
14. Execute ps-validator: Validate EN-001 acceptance criteria met
15. Evaluate Gate 3: If score >= 0.92, mark workflow COMPLETE

---

## Disclaimer

This orchestration plan was generated by the orch-planner agent (v2.1.0) in the Jerry framework. It documents a workflow design for EN-001 (Research Effective Jerry Prompt Patterns) using all 9 problem-solving skill agents across 3 phases with adversarial critic gates (quality >= 0.92) at each phase boundary. Human review is recommended before execution. All paths are repository-relative and cross-session portable.

---

*Document ID: PROJ-006-ORCH-PLAN*
*Workflow ID: prompt-research-20260218-001*
*Version: 1.0*
*Cross-Session Portable: All paths are repository-relative*
