# ORCHESTRATION_PLAN.md

> **Document ID:** PROJ-001-ORCH-PLAN
> **Project:** PROJ-001-oss-release
> **Workflow ID:** `epic001-docs-20260218-001`
> **Status:** ACTIVE
> **Version:** 2.0
> **Created:** 2026-02-18
> **Last Updated:** 2026-02-18

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#1-executive-summary) | Workflow purpose and outcome |
| [Workflow Architecture](#2-workflow-architecture) | Pipeline diagram and pattern classification |
| [Phase Definitions](#3-phase-definitions) | Per-phase agent and artifact specification |
| [Quality Gate Protocol](#4-quality-gate-protocol) | C2 adversarial review definitions |
| [Agent Registry](#5-agent-registry) | All agents across all phases |
| [State Management](#6-state-management) | Artifact paths and checkpoint strategy |
| [Execution Constraints](#7-execution-constraints) | Hard and soft constraints |
| [Success Criteria](#8-success-criteria) | Exit criteria per phase and for completion |
| [Risk Mitigations](#9-risk-mitigations) | Known risks and mitigations |
| [Resumption Context](#10-resumption-context) | Current state and next actions |

---

## 1. Executive Summary

This workflow orchestrates the completion of FEAT-017 (Installation Instructions Modernization) and FEAT-018 (User Documentation — Runbooks & Playbooks) for the Jerry Framework OSS release. These two features together produce the user-facing documentation layer required before public release: accurate installation paths and operational runbooks/playbooks for skill usage.

The workflow addresses:
- **FEAT-017:** Removing private archive-based installation instructions, adding collaborator-based paths (SSH + marketplace), and documenting the future public repository path.
- **FEAT-018:** Defining runbook/playbook structure and creating the getting-started runbook plus three skill playbooks (problem-solving, orchestration, transcript).

FEAT-017 is a hard dependency for FEAT-018 because the getting-started runbook must reference accurate installation instructions.

**Current State:** Not started. INSTALLATION.md exists at `docs/INSTALLATION.md` (470 lines) with marketplace-based instructions that require review and update.

**Orchestration Pattern:** Sequential pipeline with inter-feature dependency barrier. Fan-out in Phase 4 for parallel playbook creation. C2 adversarial quality gates at Phases 2 and 4.

### 1.1 Workflow Identification

| Field | Value | Source |
|-------|-------|--------|
| Workflow ID | `epic001-docs-20260218-001` | auto |
| ID Format | `{purpose}-{YYYYMMDD}-{NNN}` | semantic-date-seq |
| Base Path | `orchestration/epic001-docs-20260218-001/` | Dynamic |

**Artifact Output Locations:**
- Phase documents: `orchestration/epic001-docs-20260218-001/docs/phase-{N}/{agent_id}/`
- Quality gate outputs: `orchestration/epic001-docs-20260218-001/docs/quality-gates/qg-{N}/`
- Final synthesis: `orchestration/epic001-docs-20260218-001/docs/phase-5/`

---

## 2. Workflow Architecture

### 2.1 Pipeline Diagram

```
SEQUENTIAL PIPELINE: epic001-docs-20260218-001
================================================

┌───────────────────────────────────────────────────────────────┐
│  PHASE 1: Requirements & Gap Analysis                         │
│  ──────────────────────────────────                           │
│  • ps-researcher  → gap analysis of INSTALLATION.md          │
│  • nse-requirements → requirements for FEAT-017 + FEAT-018   │
│  STATUS: PENDING                                              │
└──────────────────────────────┬────────────────────────────────┘
                               │
                               ▼
┌───────────────────────────────────────────────────────────────┐
│  PHASE 2: FEAT-017 Execution (Installation Instructions)      │
│  ──────────────────────────────────────────────────────────   │
│  • ps-architect   → create/revise INSTALLATION.md content    │
│  • ps-critic      → creator-critic loop (min 3 iterations)   │
│  STATUS: PENDING                                              │
└──────────────────────────────┬────────────────────────────────┘
                               │
                               ▼
    ╔══════════════════════════════════════════════════════════╗
    ║              QUALITY GATE 1 (QG-1)                       ║
    ║  Strategies: S-007 (Constitutional), S-002 (Devil's      ║
    ║              Advocate), S-014 (LLM-as-Judge)             ║
    ║  Threshold:  >= 0.92 weighted composite                  ║
    ║  Agents:     adv-executor → adv-scorer                   ║
    ║  Output:     qg-1/adv-executor/qg1-review.md            ║
    ║              qg-1/adv-scorer/qg1-score.md               ║
    ║  STATUS: PENDING                                         ║
    ╚══════════════════════════════════════════════════════════╝
                               │
                               ▼ [FEAT-017 COMPLETE — dependency satisfied]
┌───────────────────────────────────────────────────────────────┐
│  PHASE 3: FEAT-018 Scope & Structure (EN-942)                 │
│  ──────────────────────────────────────────────              │
│  • nse-explorer   → evaluate runbook vs playbook approaches  │
│  • ps-architect   → design scope document + structure        │
│  STATUS: PENDING                                              │
└──────────────────────────────┬────────────────────────────────┘
                               │
                               ▼
┌───────────────────────────────────────────────────────────────┐
│  PHASE 4: FEAT-018 Content Creation (EN-943 + EN-944)         │
│  ──────────────────────────────────────────────────────────   │
│                                                               │
│  [Sequential] ps-synthesizer → getting-started runbook       │
│                                                               │
│  [Fan-out — Parallel]                                         │
│  • ps-synthesizer-ps  → problem-solving playbook             │
│  • ps-synthesizer-orch → orchestration playbook              │
│  • ps-synthesizer-tx  → transcript playbook                  │
│                                                               │
│  [Fan-in] ps-critic  → review all 4 deliverables            │
│  STATUS: PENDING                                              │
└──────────────────────────────┬────────────────────────────────┘
                               │
                               ▼
    ╔══════════════════════════════════════════════════════════╗
    ║              QUALITY GATE 2 (QG-2)                       ║
    ║  Strategies: S-007 (Constitutional), S-002 (Devil's      ║
    ║              Advocate), S-014 (LLM-as-Judge)             ║
    ║  Threshold:  >= 0.92 weighted composite                  ║
    ║  Agents:     adv-executor → adv-scorer                   ║
    ║  Output:     qg-2/adv-executor/qg2-review.md            ║
    ║              qg-2/adv-scorer/qg2-score.md               ║
    ║  STATUS: PENDING                                         ║
    ╚══════════════════════════════════════════════════════════╝
                               │
                               ▼
┌───────────────────────────────────────────────────────────────┐
│  PHASE 5: Final Verification & Synthesis                      │
│  ──────────────────────────────────────────                   │
│  • nse-verification → verify all FEAT-017 + FEAT-018 AC      │
│  • orch-synthesizer → final workflow synthesis report         │
│  STATUS: PENDING                                              │
└───────────────────────────────────────────────────────────────┘
                               │
                               ▼
    ╔══════════════════════════════════════════════════════════╗
    ║              QUALITY GATE 3 (QG-3)                       ║
    ║  Final cross-deliverable consistency check               ║
    ║  Strategy: S-014 (LLM-as-Judge) — scoring only          ║
    ║  Threshold: >= 0.92 weighted composite                   ║
    ║  Agent:     adv-scorer                                   ║
    ║  Output:    qg-3/adv-scorer/qg3-final-score.md          ║
    ║  STATUS: PENDING                                         ║
    ╚══════════════════════════════════════════════════════════╝
                               │
                               ▼
                      [WORKFLOW COMPLETE]
```

### 2.2 Orchestration Pattern Classification

| Pattern | Applied | Description |
|---------|---------|-------------|
| Sequential | Yes | Primary pipeline — phases execute in strict order |
| Concurrent | Yes | Phase 4 fan-out: 3 playbooks created in parallel |
| Barrier Sync | Yes | Inter-feature dependency: FEAT-017 complete before FEAT-018 starts |
| Hierarchical | Yes | Orchestrator (main Claude) delegates to agents via Task tool |

---

## 3. Phase Definitions

### 3.1 Phase 1: Requirements & Gap Analysis

| Field | Value |
|-------|-------|
| Purpose | Analyze INSTALLATION.md for FEAT-017 gaps; define requirements for FEAT-018 documentation structure |
| Status | PENDING |
| Exit Criteria | Gap analysis document complete; FEAT-018 requirements document complete |

| Agent ID | Role | Input | Output Artifact Path |
|----------|------|-------|---------------------|
| ps-researcher-001 | Read INSTALLATION.md, identify archive-based refs (EN-939), missing collaborator path (EN-940), missing public repo path (EN-941) | `docs/INSTALLATION.md` | `docs/phase-1/ps-researcher-001/ps-researcher-001-gap-analysis.md` |
| nse-requirements-001 | Define documentation requirements for FEAT-018 (EN-942 scope, EN-943 getting-started, EN-944 playbooks) | Gap analysis output | `docs/phase-1/nse-requirements-001/nse-requirements-001-feat018-requirements.md` |

**Phase 1 Exit Criteria:**
- Gap analysis identifies all archive-based installation references requiring removal
- Gap analysis confirms collaborator path (SSH + marketplace) is absent or incomplete
- Gap analysis confirms public repo path is absent
- FEAT-018 requirements document defines runbook/playbook scope, AC mapping, and coverage plan

---

### 3.2 Phase 2: FEAT-017 Execution (Installation Instructions)

| Field | Value |
|-------|-------|
| Purpose | Execute EN-939, EN-940, EN-941: produce updated INSTALLATION.md content satisfying all FEAT-017 ACs |
| Status | PENDING |
| Blocked By | Phase 1 complete |
| Exit Criteria | Updated INSTALLATION.md content passes QG-1 quality gate (>= 0.92) |

| Agent ID | Role | Input | Output Artifact Path |
|----------|------|-------|---------------------|
| ps-architect-001 | Design and draft updated INSTALLATION.md — remove archive refs, add collaborator section (SSH key + GitHub + marketplace), add public repo section | Phase 1 gap analysis | `docs/phase-2/ps-architect-001/ps-architect-001-installation-draft.md` |
| ps-critic-001 | Creator-critic review of INSTALLATION.md draft (minimum 3 iterations per H-14); apply S-010 self-refine before critique | Draft from ps-architect-001 | `docs/phase-2/ps-critic-001/ps-critic-001-installation-review.md` |

**FEAT-017 Acceptance Criteria Mapping:**
| AC | Validated By |
|----|-------------|
| AC-1: No archive distribution references in active instructions | ps-researcher-001 gap analysis + ps-critic-001 review |
| AC-2: Step-by-step collaborator installation (SSH + GitHub + marketplace) | ps-architect-001 draft, ps-critic-001 review, QG-1 |
| AC-3: Public repository installation path documented | ps-architect-001 draft, ps-critic-001 review, QG-1 |
| AC-4: Claude Code marketplace integration instructions included | ps-architect-001 draft, ps-critic-001 review, QG-1 |

**Phase 2 Exit Criteria:**
- Creator-critic loop completed (minimum 3 iterations)
- Revised INSTALLATION.md content artifact exists
- QG-1 score >= 0.92

---

### 3.3 Phase 3: FEAT-018 Scope & Structure (EN-942)

| Field | Value |
|-------|-------|
| Purpose | Execute EN-942: produce scope document defining runbook vs playbook distinction, coverage plan, and directory structure |
| Status | PENDING |
| Blocked By | QG-1 PASS (FEAT-017 dependency) |
| Exit Criteria | Scope document approved; directory structure designed |

| Agent ID | Role | Input | Output Artifact Path |
|----------|------|-------|---------------------|
| nse-explorer-001 | Trade study: evaluate runbook vs playbook definitions, evaluate structure approaches (flat vs nested docs), map to Jerry conventions | FEAT-018 requirements | `docs/phase-3/nse-explorer-001/nse-explorer-001-structure-trade-study.md` |
| ps-architect-002 | Design scope document (runbook vs playbook distinction, coverage matrix, directory layout, navigation standards compliance) | Trade study output | `docs/phase-3/ps-architect-002/ps-architect-002-feat018-scope.md` |

**EN-942 Acceptance Criteria Mapping:**
| AC | Validated By |
|----|-------------|
| AC-1: Scope document defines runbook vs playbook distinction and coverage plan | ps-architect-002 output, Phase 5 nse-verification |

**Phase 3 Exit Criteria:**
- Runbook vs playbook distinction clearly defined with examples
- Coverage plan maps EN-943 and EN-944 to specific deliverable files
- Directory structure designed (e.g., `docs/runbooks/`, `docs/playbooks/`)
- Navigation standards compliance verified (H-23, H-24)

---

### 3.4 Phase 4: FEAT-018 Content Creation (EN-943 + EN-944)

| Field | Value |
|-------|-------|
| Purpose | Execute EN-943 (getting-started runbook) and EN-944 (3 skill playbooks) in fan-out/fan-in pattern |
| Status | PENDING |
| Blocked By | Phase 3 complete |
| Exit Criteria | All 4 deliverables complete and pass QG-2 (>= 0.92) |

**Sequential step — Getting-Started Runbook (EN-943):**

| Agent ID | Role | Input | Output Artifact Path |
|----------|------|-------|---------------------|
| ps-synthesizer-001 | Create getting-started runbook: initial setup through first skill invocation, references updated INSTALLATION.md | Phase 3 scope, INSTALLATION.md content | `docs/phase-4/ps-synthesizer-001/ps-synthesizer-001-getting-started-runbook.md` |

**Fan-out — Parallel Playbook Creation (EN-944):**

| Agent ID | Role | Input | Output Artifact Path |
|----------|------|-------|---------------------|
| ps-synthesizer-002 | Create problem-solving skill playbook: when/how to use /problem-solving, agent selection guide, trigger map, examples | Phase 3 scope | `docs/phase-4/ps-synthesizer-002/ps-synthesizer-002-playbook-problem-solving.md` |
| ps-synthesizer-003 | Create orchestration skill playbook: when/how to use /orchestration, pipeline patterns, phase definitions, examples | Phase 3 scope | `docs/phase-4/ps-synthesizer-003/ps-synthesizer-003-playbook-orchestration.md` |
| ps-synthesizer-004 | Create transcript skill playbook: when/how to use /transcript, chunk reading strategy, extraction guide, examples | Phase 3 scope | `docs/phase-4/ps-synthesizer-004/ps-synthesizer-004-playbook-transcript.md` |

**Fan-in — Critic Review:**

| Agent ID | Role | Input | Output Artifact Path |
|----------|------|-------|---------------------|
| ps-critic-002 | Creator-critic review of all 4 deliverables (minimum 3 iterations per H-14); verify H-23/H-24 compliance across all | All ps-synthesizer outputs | `docs/phase-4/ps-critic-002/ps-critic-002-feat018-review.md` |

**FEAT-018 Acceptance Criteria Mapping:**
| AC | Validated By |
|----|-------------|
| AC-2: Getting-started runbook covers initial setup through first skill invocation | ps-synthesizer-001, ps-critic-002, QG-2 |
| AC-3: At least 3 skill playbooks created (problem-solving, orchestration, transcript) | ps-synthesizer-002/003/004, ps-critic-002, QG-2 |
| AC-4: All documentation follows H-23, H-24 navigation standards | ps-critic-002, nse-verification in Phase 5 |

**Phase 4 Exit Criteria:**
- Getting-started runbook exists and references updated INSTALLATION.md
- 3 skill playbooks exist (problem-solving, orchestration, transcript)
- Creator-critic loop completed (minimum 3 iterations)
- QG-2 score >= 0.92

---

### 3.5 Phase 5: Final Verification & Synthesis

| Field | Value |
|-------|-------|
| Purpose | Verify all FEAT-017 and FEAT-018 acceptance criteria are met; produce final synthesis report; final quality scoring |
| Status | PENDING |
| Blocked By | QG-2 PASS |
| Exit Criteria | All ACs verified; synthesis report created; QG-3 score >= 0.92 |

| Agent ID | Role | Input | Output Artifact Path |
|----------|------|-------|---------------------|
| nse-verification-001 | Systematic verification against all FEAT-017 + FEAT-018 ACs (8 total); produce traceability matrix | All phase outputs, INSTALLATION.md content, all runbook/playbook content | `docs/phase-5/nse-verification-001/nse-verification-001-ac-verification.md` |
| orch-synthesizer-001 | Create final workflow synthesis: summary of deliverables, decisions made, lessons learned, worktracker update | Verification output, all phase artifacts | `docs/phase-5/orch-synthesizer-001/orch-synthesizer-001-synthesis.md` |

**Phase 5 Exit Criteria:**
- All 8 acceptance criteria verified (FEAT-017: AC-1 through AC-4; FEAT-018: AC-1 through AC-4)
- Traceability matrix maps each AC to its deliverable artifact
- Final synthesis report created
- QG-3 score >= 0.92
- WORKTRACKER.md updated to close FEAT-017 and FEAT-018

---

## 4. Quality Gate Protocol

### 4.1 Quality Gate Definitions (C2)

**Applicable C2 strategies per quality-enforcement.md:**
- **Required:** S-007 (Constitutional AI Critique), S-002 (Devil's Advocate), S-014 (LLM-as-Judge)
- **Optional:** S-003 (Steelman), S-010 (Self-Refine)
- **Threshold:** >= 0.92 weighted composite
- **Minimum iterations:** 3 (creator-critic-revision) per H-14

### 4.2 Quality Gate 1 (QG-1) — After Phase 2

| Field | Value |
|-------|-------|
| Deliverable | Updated INSTALLATION.md content |
| Path | `docs/quality-gates/qg-1/` |
| Strategy Sequence | S-010 (in Phase 2 creator loop) → S-002 (adv-executor) → S-007 (adv-executor) → S-014 (adv-scorer) |
| Threshold | >= 0.92 |
| Pass Action | Proceed to Phase 3 |
| Fail Action | Return to ps-architect-001 for targeted revision; re-score |

| Agent | Task | Output |
|-------|------|--------|
| adv-executor-001 | Apply S-002 (Devil's Advocate) — challenge installation instructions for edge cases, missing scenarios, incorrect sequencing | `docs/quality-gates/qg-1/adv-executor-001/qg1-devils-advocate.md` |
| adv-executor-002 | Apply S-007 (Constitutional AI Critique) — verify AC compliance, H-23/H-24 nav standards, P-022 accuracy | `docs/quality-gates/qg-1/adv-executor-002/qg1-constitutional.md` |
| adv-scorer-001 | Apply S-014 (LLM-as-Judge) — 6-dimension weighted composite score | `docs/quality-gates/qg-1/adv-scorer-001/qg1-score.md` |

**S-014 Scoring Dimensions:**
| Dimension | Weight |
|-----------|--------|
| Completeness | 0.20 |
| Internal Consistency | 0.20 |
| Methodological Rigor | 0.20 |
| Evidence Quality | 0.15 |
| Actionability | 0.15 |
| Traceability | 0.10 |

### 4.3 Quality Gate 2 (QG-2) — After Phase 4

| Field | Value |
|-------|-------|
| Deliverable | Getting-started runbook + 3 skill playbooks (4 documents) |
| Path | `docs/quality-gates/qg-2/` |
| Strategy Sequence | S-010 (in Phase 4 creator loop) → S-002 (adv-executor) → S-007 (adv-executor) → S-014 (adv-scorer) |
| Threshold | >= 0.92 (each individual document AND aggregate) |
| Pass Action | Proceed to Phase 5 |
| Fail Action | Return to relevant ps-synthesizer agent for targeted revision; re-score failing document(s) |

| Agent | Task | Output |
|-------|------|--------|
| adv-executor-003 | Apply S-002 (Devil's Advocate) — challenge each playbook/runbook for gaps, incorrect skill descriptions, missing edge cases | `docs/quality-gates/qg-2/adv-executor-003/qg2-devils-advocate.md` |
| adv-executor-004 | Apply S-007 (Constitutional AI Critique) — verify H-23/H-24 compliance, AC mapping, FEAT-017 dependency satisfied in getting-started | `docs/quality-gates/qg-2/adv-executor-004/qg2-constitutional.md` |
| adv-scorer-002 | Apply S-014 (LLM-as-Judge) — score each document individually, then aggregate | `docs/quality-gates/qg-2/adv-scorer-002/qg2-score.md` |

### 4.4 Quality Gate 3 (QG-3) — After Phase 5

| Field | Value |
|-------|-------|
| Deliverable | All FEAT-017 + FEAT-018 deliverables (cross-deliverable consistency) |
| Path | `docs/quality-gates/qg-3/` |
| Strategy | S-014 (LLM-as-Judge) only — final scoring pass |
| Threshold | >= 0.92 aggregate |
| Pass Action | Workflow COMPLETE |
| Fail Action | Identify failing documents; targeted revision; re-score |

| Agent | Task | Output |
|-------|------|--------|
| adv-scorer-003 | Apply S-014 — final composite score across all deliverables; check cross-document consistency (installation refs match between INSTALLATION.md and getting-started runbook) | `docs/quality-gates/qg-3/adv-scorer-003/qg3-final-score.md` |

### 4.5 Quality Gate Scoring Protocol

Before QG entry, adv-executor agents MUST follow H-16 ordering:
1. Apply S-003 (Steelman) internally — strengthen the deliverable's argument before critiquing
2. Apply S-002 (Devil's Advocate) — then challenge from adversarial perspective
3. Apply S-007 (Constitutional AI Critique) — verify against Jerry Constitution and rules
4. Hand findings to adv-scorer for S-014 scoring

Below-threshold outcomes:
| Band | Score Range | Action |
|------|------------|--------|
| PASS | >= 0.92 | Proceed |
| REVISE | 0.85 - 0.91 | Targeted revision; re-score |
| REJECTED | < 0.85 | Significant rework; full creator loop reset |

---

## 5. Agent Registry

| Agent ID | Phase | Skill | Role | Inputs | Output Path |
|----------|-------|-------|------|--------|-------------|
| ps-researcher-001 | 1 | problem-solving | Gap analysis of INSTALLATION.md | `docs/INSTALLATION.md` | `docs/phase-1/ps-researcher-001/` |
| nse-requirements-001 | 1 | nasa-se | FEAT-018 requirements definition | Phase 1 gap analysis | `docs/phase-1/nse-requirements-001/` |
| ps-architect-001 | 2 | problem-solving | INSTALLATION.md content creation | Phase 1 gap analysis | `docs/phase-2/ps-architect-001/` |
| ps-critic-001 | 2 | problem-solving | Creator-critic review (3+ iterations) | ps-architect-001 draft | `docs/phase-2/ps-critic-001/` |
| adv-executor-001 | QG-1 | adversary | S-002 Devil's Advocate on INSTALLATION.md | ps-critic-001 final | `docs/quality-gates/qg-1/adv-executor-001/` |
| adv-executor-002 | QG-1 | adversary | S-007 Constitutional Critique on INSTALLATION.md | ps-critic-001 final | `docs/quality-gates/qg-1/adv-executor-002/` |
| adv-scorer-001 | QG-1 | adversary | S-014 LLM-as-Judge scoring | adv-executor-001/002 outputs | `docs/quality-gates/qg-1/adv-scorer-001/` |
| nse-explorer-001 | 3 | nasa-se | Runbook/playbook structure trade study | FEAT-018 requirements | `docs/phase-3/nse-explorer-001/` |
| ps-architect-002 | 3 | problem-solving | Scope document + directory structure design | nse-explorer-001 output | `docs/phase-3/ps-architect-002/` |
| ps-synthesizer-001 | 4 | problem-solving | Getting-started runbook creation | Phase 3 scope, INSTALLATION.md | `docs/phase-4/ps-synthesizer-001/` |
| ps-synthesizer-002 | 4 | problem-solving | Problem-solving skill playbook | Phase 3 scope | `docs/phase-4/ps-synthesizer-002/` |
| ps-synthesizer-003 | 4 | problem-solving | Orchestration skill playbook | Phase 3 scope | `docs/phase-4/ps-synthesizer-003/` |
| ps-synthesizer-004 | 4 | problem-solving | Transcript skill playbook | Phase 3 scope | `docs/phase-4/ps-synthesizer-004/` |
| ps-critic-002 | 4 | problem-solving | Creator-critic review of all 4 FEAT-018 docs | All ps-synthesizer outputs | `docs/phase-4/ps-critic-002/` |
| adv-executor-003 | QG-2 | adversary | S-002 Devil's Advocate on FEAT-018 docs | ps-critic-002 final | `docs/quality-gates/qg-2/adv-executor-003/` |
| adv-executor-004 | QG-2 | adversary | S-007 Constitutional Critique on FEAT-018 docs | ps-critic-002 final | `docs/quality-gates/qg-2/adv-executor-004/` |
| adv-scorer-002 | QG-2 | adversary | S-014 LLM-as-Judge scoring (per-doc + aggregate) | adv-executor-003/004 outputs | `docs/quality-gates/qg-2/adv-scorer-002/` |
| nse-verification-001 | 5 | nasa-se | AC verification traceability matrix | All phase outputs | `docs/phase-5/nse-verification-001/` |
| orch-synthesizer-001 | 5 | orchestration | Final workflow synthesis report | Verification + all artifacts | `docs/phase-5/orch-synthesizer-001/` |
| adv-scorer-003 | QG-3 | adversary | S-014 final composite score | All deliverables | `docs/quality-gates/qg-3/adv-scorer-003/` |

---

## 6. State Management

### 6.1 State Files

| File | Purpose |
|------|---------|
| `ORCHESTRATION.yaml` | Machine-readable state (SSOT) — updated by orch-tracker after each phase |
| `ORCHESTRATION_PLAN.md` | This file — strategic context and execution instructions |

### 6.2 Artifact Path Structure

All artifacts stored under the workflow base path using dynamic identifiers:

```
orchestration/epic001-docs-20260218-001/
├── docs/
│   ├── phase-1/
│   │   ├── ps-researcher-001/
│   │   │   └── ps-researcher-001-gap-analysis.md
│   │   └── nse-requirements-001/
│   │       └── nse-requirements-001-feat018-requirements.md
│   ├── phase-2/
│   │   ├── ps-architect-001/
│   │   │   └── ps-architect-001-installation-draft.md
│   │   └── ps-critic-001/
│   │       └── ps-critic-001-installation-review.md
│   ├── phase-3/
│   │   ├── nse-explorer-001/
│   │   │   └── nse-explorer-001-structure-trade-study.md
│   │   └── ps-architect-002/
│   │       └── ps-architect-002-feat018-scope.md
│   ├── phase-4/
│   │   ├── ps-synthesizer-001/
│   │   │   └── ps-synthesizer-001-getting-started-runbook.md
│   │   ├── ps-synthesizer-002/
│   │   │   └── ps-synthesizer-002-playbook-problem-solving.md
│   │   ├── ps-synthesizer-003/
│   │   │   └── ps-synthesizer-003-playbook-orchestration.md
│   │   ├── ps-synthesizer-004/
│   │   │   └── ps-synthesizer-004-playbook-transcript.md
│   │   └── ps-critic-002/
│   │       └── ps-critic-002-feat018-review.md
│   ├── phase-5/
│   │   ├── nse-verification-001/
│   │   │   └── nse-verification-001-ac-verification.md
│   │   └── orch-synthesizer-001/
│   │       └── orch-synthesizer-001-synthesis.md
│   └── quality-gates/
│       ├── qg-1/
│       │   ├── adv-executor-001/
│       │   │   └── qg1-devils-advocate.md
│       │   ├── adv-executor-002/
│       │   │   └── qg1-constitutional.md
│       │   └── adv-scorer-001/
│       │       └── qg1-score.md
│       ├── qg-2/
│       │   ├── adv-executor-003/
│       │   │   └── qg2-devils-advocate.md
│       │   ├── adv-executor-004/
│       │   │   └── qg2-constitutional.md
│       │   └── adv-scorer-002/
│       │       └── qg2-score.md
│       └── qg-3/
│           └── adv-scorer-003/
│               └── qg3-final-score.md
```

### 6.3 Checkpoint Strategy

| Trigger | When | Purpose |
|---------|------|---------|
| PHASE_COMPLETE | After each of the 5 phases | Phase-level rollback point |
| QG_COMPLETE | After each quality gate (QG-1, QG-2, QG-3) | Post-gate state preservation |
| MANUAL | User-triggered | Debug and inspection |

---

## 7. Execution Constraints

### 7.1 Hard Constraints (Jerry Constitution)

| Constraint | ID | Enforcement |
|------------|----|----|
| Single agent nesting | P-003 | Orchestrator (main Claude) invokes agents via Task tool — no recursive subagents |
| File persistence | P-002 | All phase outputs and quality gate artifacts persisted to filesystem before proceeding |
| No deception | P-022 | Quality scores reported as-is; no rounding up to meet threshold |
| User authority | P-020 | Quality gate PASS/FAIL decisions are surfaced to user at each gate |

### 7.1.1 Worktracker Entity Templates

> **WTI-007:** Any worktracker entities created during this workflow (FEATURE, ENABLER updates) MUST use canonical templates from `.context/templates/worktracker/`. Read the appropriate template before creating or updating. Do not create entity files from memory.

### 7.2 Soft Constraints

| Constraint | Value | Rationale |
|------------|-------|-----------|
| Max concurrent agents | 4 | Phase 4 fan-out (3 synthesizers + 1 critic in fan-in) |
| Max QG retries | 2 | Circuit breaker — after 2 failed revisions, escalate to user |
| Checkpoint frequency | PHASE + QG | Recovery at phase and gate boundaries |
| Creator-critic minimum iterations | 3 | H-14 requirement |

---

## 8. Success Criteria

### 8.1 Phase 1 Exit Criteria

| Criterion | Validation |
|-----------|------------|
| Gap analysis covers all EN-939, EN-940, EN-941 scope | ps-researcher-001 artifact covers all 3 enablers |
| FEAT-018 requirements document is actionable | nse-requirements-001 maps each EN to specific deliverable outputs |

### 8.2 Phase 2 Exit Criteria

| Criterion | Validation |
|-----------|------------|
| Archive references removed (AC-1) | ps-architect-001 draft + ps-critic-001 sign-off |
| Collaborator path documented (AC-2) | ps-architect-001 draft includes SSH, GitHub, marketplace steps |
| Public repo path documented (AC-3) | ps-architect-001 draft includes future-state public repo section |
| Marketplace integration included (AC-4) | ps-architect-001 draft includes marketplace integration |
| QG-1 score >= 0.92 | adv-scorer-001 score sheet |

### 8.3 Phase 3 Exit Criteria

| Criterion | Validation |
|-----------|------------|
| Runbook vs playbook distinction defined (EN-942 AC-1) | ps-architect-002 scope document |
| Coverage plan maps EN-943 + EN-944 to files | ps-architect-002 scope document |
| Directory structure defined | ps-architect-002 scope document |

### 8.4 Phase 4 Exit Criteria

| Criterion | Validation |
|-----------|------------|
| Getting-started runbook covers setup through first skill invocation (AC-2) | ps-synthesizer-001 output + ps-critic-002 review |
| 3 skill playbooks exist: problem-solving, orchestration, transcript (AC-3) | ps-synthesizer-002/003/004 outputs |
| All docs comply with H-23, H-24 (AC-4) | ps-critic-002 review |
| QG-2 score >= 0.92 | adv-scorer-002 score sheet |

### 8.5 Phase 5 Exit Criteria

| Criterion | Validation |
|-----------|------------|
| All 8 FEAT-017 + FEAT-018 ACs verified in traceability matrix | nse-verification-001 artifact |
| Final synthesis report created | orch-synthesizer-001 artifact |
| QG-3 score >= 0.92 | adv-scorer-003 score sheet |

### 8.6 Workflow Completion Criteria

| Criterion | Validation |
|-----------|------------|
| All 5 phases COMPLETE | ORCHESTRATION.yaml phase statuses |
| QG-1, QG-2, QG-3 all PASS | Score artifacts in quality-gates/ |
| INSTALLATION.md updated in repository | Committed to docs/INSTALLATION.md |
| Runbooks and playbooks committed | Committed to docs/runbooks/ and docs/playbooks/ |
| WORKTRACKER.md reflects FEAT-017 + FEAT-018 closed | orch-synthesizer-001 update confirmed |

---

## 9. Risk Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| INSTALLATION.md has more archive refs than identified in gap analysis | M | M | ps-researcher-001 performs exhaustive search with grep patterns; ps-critic-001 second-passes for stragglers |
| Collaborator installation steps are not testable (SSH key provisioning is external) | H | M | Document steps as instructions; note external dependencies explicitly; QG-1 S-002 will probe this |
| Public repo path section is speculative (repo not yet public) | H | L | Mark section as "Future State" with clear conditional framing; nse-verification-001 confirms framing is accurate |
| Phase 4 fan-out produces inconsistent style across 3 playbooks | M | M | ps-critic-002 fan-in review enforces consistency; Phase 3 scope document provides style template |
| QG scoring leniency bias (H-13 warning) | M | H | adv-scorer agents must actively counteract leniency per S-014 rubric; scores must be justified per dimension |
| Creator-critic loop stalls below 3 iterations | L | M | Enforced by orch-tracker; minimum 3 iterations logged before QG entry |
| Context rot degrades quality in Phase 4 (large fan-out) | M | M | Each ps-synthesizer agent receives focused input subset; orch-tracker checkpoints after each agent |

---

## 10. Resumption Context

### 10.1 Current Execution State

```
WORKFLOW STATUS AS OF 2026-02-18
=================================

Phase 1 (Requirements & Gap Analysis): PENDING
Phase 2 (FEAT-017 Execution):          PENDING — BLOCKED by Phase 1
Quality Gate 1:                        PENDING — BLOCKED by Phase 2
Phase 3 (FEAT-018 Scope):              PENDING — BLOCKED by QG-1
Phase 4 (FEAT-018 Content):            PENDING — BLOCKED by Phase 3
Quality Gate 2:                        PENDING — BLOCKED by Phase 4
Phase 5 (Verification & Synthesis):    PENDING — BLOCKED by QG-2
Quality Gate 3:                        PENDING — BLOCKED by Phase 5

Overall Progress: 0/5 phases complete
```

### 10.2 Next Actions

1. Invoke orch-tracker to initialize ORCHESTRATION.yaml status tracking
2. Invoke ps-researcher-001 (Phase 1): analyze `docs/INSTALLATION.md` for FEAT-017 gaps
3. Invoke nse-requirements-001 (Phase 1): define FEAT-018 documentation requirements
4. Invoke orch-tracker to checkpoint Phase 1 completion
5. Proceed to Phase 2 per exit criteria

### 10.3 Invocation Pattern

All agents are invoked by the main Claude context via Task tool per P-003:

```
Task: [agent-id]
Context: Read ORCHESTRATION_PLAN.md Phase N definition.
         Read [input artifacts].
         Execute [agent role] and persist output to [output path].
         Confirm output path in response.
```

---

*Document ID: PROJ-001-ORCH-PLAN*
*Workflow ID: epic001-docs-20260218-001*
*Version: 2.0*
*Criticality: C2 (Standard) — documentation changes, reversible within 1 day*
*Cross-Session Portable: All paths are repository-relative*

---

> **DISCLAIMER:** This plan was generated by the orch-planner agent (v2.2.0) acting as a planning artifact producer. It does not execute agents — it defines the execution contract for the main Claude context (orchestrator). All agent invocations are performed by the main context via Task tool. This document is the authoritative strategic context for workflow `epic001-docs-20260218-001`. Do not modify without updating ORCHESTRATION.yaml version field.
