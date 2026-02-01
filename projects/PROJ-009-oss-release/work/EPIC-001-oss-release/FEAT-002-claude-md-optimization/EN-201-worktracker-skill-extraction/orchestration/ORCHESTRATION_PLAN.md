# ORCHESTRATION_PLAN.md - EN-201 Worktracker Skill Extraction

> **Document ID:** EN-201-ORCH-PLAN
> **Project:** PROJ-009-oss-release
> **Workflow ID:** `en201-extraction-20260201-001`
> **Status:** ACTIVE
> **Version:** 2.0
> **Created:** 2026-02-01
> **Last Updated:** 2026-02-01
> **Protocol:** DISC-002 Adversarial Review
> **Prior Art:** FEAT-001 Research Phase Quality Gates (qg-0 through qg-4)

---

## 1. Executive Summary

This orchestration plan coordinates the parallel extraction of worktracker content from CLAUDE.md into modular rule files, using the **DISC-002 Adversarial Review Protocol** established in the FEAT-001 research phase.

**Problem:** CLAUDE.md contains 371 lines of worktracker content loaded at every session start, contributing to context rot.

**Solution:** Extract content to 4 modular rule files in `skills/worktracker/rules/`, loaded on-demand via `/worktracker` skill invocation.

**Current State:** TASK-001 complete (SKILL.md fixed). Ready to execute parallel extraction with quality gates.

**Orchestration Pattern:** Fan-Out/Fan-In with **DISC-002 Adversarial Review Loops**

### 1.1 Workflow Identification

| Field | Value | Source |
|-------|-------|--------|
| Workflow ID | `en201-extraction-20260201-001` | auto |
| ID Format | `{enabler}-{purpose}-{YYYYMMDD}-{NNN}` | semantic-date-seq |
| Base Path | `EN-201-worktracker-skill-extraction/orchestration/` | Enabler-scoped |
| Protocol | **DISC-002** | Adversarial Review Protocol |
| Prior Art | FEAT-001/orchestration/oss-release-20260131-001/quality-gates/ | Research Phase |

**Artifact Output Locations:**
- Extraction artifacts: `skills/worktracker/rules/`
- Quality gate artifacts: `orchestration/quality-gates/`
- Escalation artifacts: `orchestration/escalations/`

---

## 2. Workflow Architecture

### 2.1 DISC-002 Adversarial Review Protocol

This workflow implements the **DISC-002 Adversarial Review Protocol** established in the FEAT-001 research phase. Key characteristics:

| Protocol Element | Implementation |
|------------------|----------------|
| **Review Agents** | ps-critic (Quality Evaluator) + nse-qa (NASA SE Compliance) |
| **Quality Threshold** | ≥ 0.92 (per DEC-OSS-001) |
| **Max Iterations** | 3 per artifact (then human escalation per DEC-OSS-004) |
| **Mandatory Findings** | Minimum 3 adversarial findings per review |
| **Versioned Files** | `*-review.md` → `*-review-v2.md` → `*-review-v3.md` |
| **Red Team Framing** | Actively seek weaknesses, blind spots, contradictions |

**Prior Art:** See `FEAT-001-research-and-preparation/orchestration/oss-release-20260131-001/quality-gates/qg-0/` for implementation examples.

### 2.2 Pipeline Diagram

```
                     EN-201 ORCHESTRATION WORKFLOW (DISC-002)
                     =========================================
                          Quality Gate: 0.92 | Max Iterations: 3
                          Protocol: DISC-002 Adversarial Review

┌─────────────────────────────────────────────────────────────────────────────┐
│                        PHASE 1: CONTENT EXTRACTION (Fan-Out)                │
│                              Execution Mode: PARALLEL                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│  │    TASK-002      │  │    TASK-003      │  │    TASK-004      │  │    TASK-005      │
│  │ Entity Hierarchy │  │ System Mappings  │  │  Behavior Rules  │  │ Directory Struct │
│  │     (~80 LOC)    │  │    (~120 LOC)    │  │     (~60 LOC)    │  │    (~111 LOC)    │
│  └────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘
│           │                     │                     │                     │
│           └─────────────────────┴─────────────────────┴─────────────────────┘
│                                         │
│                                         ▼
│  ┌─────────────────────────────────────────────────────────────────────────┐
│  │                    DISC-002 ADVERSARIAL REVIEW LOOP                      │
│  │                    (per task until ≥0.92 or escalation)                  │
│  │  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  │                                                                   │  │
│  │  │   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐        │  │
│  │  │   │  GENERATE   │────►│  ps-critic  │────►│ Score ≥0.92?│        │  │
│  │  │   │  Content    │     │  REVIEW     │     └──────┬──────┘        │  │
│  │  │   └─────────────┘     │             │            │               │  │
│  │  │         ▲             │ Criteria:   │     YES    │   NO          │  │
│  │  │         │             │ C/A/CL/AC/T │            │               │  │
│  │  │         │             │ Min 3       │            ▼               │  │
│  │  │         │             │ findings    │     ┌─────────────┐        │  │
│  │  │         │             └─────────────┘     │ Iteration   │        │  │
│  │  │         │                                 │   < 3?      │        │  │
│  │  │         │                                 └──────┬──────┘        │  │
│  │  │         │                                  YES   │   NO          │  │
│  │  │         │                                        │               │  │
│  │  │         │             ┌───────────────────┐      │               │  │
│  │  │         └─────────────│ REVISE with       │◄─────┘               │  │
│  │  │                       │ Feedback (REM-*)  │                      │  │
│  │  │                       │ Create *-v{N}.md  │                      │  │
│  │  │                       └───────────────────┘                      │  │
│  │  │                                 │ NO (iter ≥ 3)                  │  │
│  │  │                                 ▼                                │  │
│  │  │                       ┌───────────────────┐        ┌──────────┐  │  │
│  │  │                       │ ESCALATE TO HUMAN │        │  ACCEPT  │  │  │
│  │  │                       │ Review Required   │        │(≥0.92)   │  │  │
│  │  │                       └───────────────────┘        └──────────┘  │  │
│  │  │                                                                   │  │
│  │  └───────────────────────────────────────────────────────────────────┘  │
│  └─────────────────────────────────────────────────────────────────────────┘
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
    ╔═════════════════════════════════════════════════════════════════════════╗
    ║                    QUALITY GATE 1 (QG-1): EXTRACTION                     ║
    ║     DISC-002 Adversarial Review - Both ps-critic AND nse-qa             ║
    ║  ┌───────────────────────────────────────────────────────────────────┐  ║
    ║  │                                                                   │  ║
    ║  │  ┌─────────────────────┐     ┌─────────────────────┐             │  ║
    ║  │  │     ps-critic       │     │      nse-qa         │             │  ║
    ║  │  │  Quality Evaluator  │     │  NASA SE Compliance │             │  ║
    ║  │  │  ──────────────────│     │  ─────────────────── │             │  ║
    ║  │  │  Criteria:          │     │  Criteria:          │             │  ║
    ║  │  │  • Completeness     │     │  • Technical Rigor  │             │  ║
    ║  │  │  • Accuracy         │     │  • Req Traceability │             │  ║
    ║  │  │  • Clarity          │     │  • Verification Evid│             │  ║
    ║  │  │  • Actionability    │     │  • Risk Ident       │             │  ║
    ║  │  │  • Traceability     │     │  • Doc Quality      │             │  ║
    ║  │  │  ──────────────────│     │  ─────────────────── │             │  ║
    ║  │  │  Output:            │     │  Output:            │             │  ║
    ║  │  │  ps-critic-review.md│     │  nse-qa-audit.md    │             │  ║
    ║  │  └─────────────────────┘     └─────────────────────┘             │  ║
    ║  │                                                                   │  ║
    ║  │  Pass Condition: Both reviews ≥0.92 OR human-approved            │  ║
    ║  │  Location: quality-gates/qg-1/                                   │  ║
    ║  └───────────────────────────────────────────────────────────────────┘  ║
    ║  STATUS: PENDING                                                         ║
    ╚═════════════════════════════════════════════════════════════════════════╝
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                     PHASE 2: INTEGRATION REVIEW                              │
│                         Execution Mode: SEQUENTIAL                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │            nse-qa: Integration Quality Audit (Batch Review)           │  │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │  │
│  │  │ Validates all 4 rule files together:                             │  │  │
│  │  │ • INT-001: Complete Migration (all 371 lines accounted for)      │  │  │
│  │  │ • INT-002: No Information Loss (diff shows no missing content)   │  │  │
│  │  │ • INT-003: Consistent Formatting (same style across all files)   │  │  │
│  │  │ • INT-004: Cross-References Valid (all internal links work)      │  │  │
│  │  │ • INT-005: Template Compliance (each file follows rules template)│  │  │
│  │  │ • INT-006: No Duplication (content not duplicated across files)  │  │  │
│  │  └─────────────────────────────────────────────────────────────────┘  │  │
│  │                                                                       │  │
│  │  Output: quality-gates/qg-2/integration-qa-report.md                  │  │
│  │  Quality Threshold: 92% compliance | Max Iterations: 3                │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
    ╔═════════════════════════════════════════════════════════════════════════╗
    ║                   QUALITY GATE 2 (QG-2): INTEGRATION                     ║
    ║     Batch validation of all extraction artifacts                        ║
    ║  ┌───────────────────────────────────────────────────────────────────┐  ║
    ║  │ Pass Condition: Integration review ≥92% OR human-approved         │  ║
    ║  │ No critical findings | High findings ≤3                           │  ║
    ║  │ Location: quality-gates/qg-2/                                     │  ║
    ║  └───────────────────────────────────────────────────────────────────┘  ║
    ║  STATUS: PENDING                                                         ║
    ╚═════════════════════════════════════════════════════════════════════════╝
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PHASE 3: NAVIGATION & VALIDATION                          │
│                         Execution Mode: SEQUENTIAL                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────────────────┐       ┌──────────────────────────┐           │
│  │       TASK-006           │──────►│       TASK-007           │           │
│  │ Update SKILL.md          │       │ Validate Skill Loading   │           │
│  │ Navigation Pointers      │       │ End-to-End Test          │           │
│  └──────────────────────────┘       └──────────────────────────┘           │
│                                                                             │
│  DISC-002 review loop for each task (ps-critic + verification)              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
                         ┌────────────────────────┐
                         │     EN-201 COMPLETE    │
                         │  All 7 Tasks Done      │
                         │  All QGs Passed        │
                         │  Enable EN-202, EN-203 │
                         └────────────────────────┘
```

### 2.2 Orchestration Pattern Classification

| Pattern | Applied | Description |
|---------|---------|-------------|
| Sequential | Yes | Phases execute in order (1→2→3) |
| Concurrent | Yes | Tasks 002-005 run in parallel within Phase 1 |
| Barrier Sync | Yes | Cross-pollination at barriers |
| Generator-Critic | Yes | Adversarial review loops per task |
| Fan-Out/Fan-In | Yes | Parallel extraction, integration review |

---

## 3. Phase Definitions

### 3.1 Phase 1: Content Extraction (Parallel)

| Task | Name | Source Content | Target File | LOC | Status |
|------|------|----------------|-------------|-----|--------|
| TASK-002 | Entity Hierarchy | CLAUDE.md §1.1-1.2 | `worktracker-entity-hierarchy.md` | ~80 | PENDING |
| TASK-003 | System Mappings | CLAUDE.md §3-4 | `worktracker-system-mappings.md` | ~120 | PENDING |
| TASK-004 | Behavior Rules | CLAUDE.md §Behavior | `worktracker-behavior-rules.md` | ~60 | PENDING |
| TASK-005 | Directory Structure | CLAUDE.md §Dir Struct | `worktracker-directory-structure.md` | ~111 | PENDING |

### 3.2 Phase 2: Integration Review

| Agent | Purpose | Input | Output | Status |
|-------|---------|-------|--------|--------|
| nse-qa | Integration audit | 4 rule files | QA report | PENDING |

### 3.3 Phase 3: Navigation & Validation

| Task | Name | Depends On | Status |
|------|------|------------|--------|
| TASK-006 | Update SKILL.md navigation | Phase 2 complete | BLOCKED |
| TASK-007 | Validate skill loading | TASK-006 complete | BLOCKED |

---

## 4. Agent Selection Rationale

### 4.1 Generator-Critic Pattern (Task-Level Review)

| Role | Agent | Rationale |
|------|-------|-----------|
| Generator | Main Context (Claude) | Content extraction is straightforward; no specialized agent needed |
| Critic | **ps-critic** | Purpose-built for iterative quality evaluation with scores |

**Why ps-critic over nse-qa for task-level review:**
- ps-critic: Designed for iterative generator-critic loops with quality scores
- nse-qa: Designed for artifact compliance validation (NASA standards)
- Task-level extraction benefits from iterative refinement (ps-critic's specialty)

### 4.2 Integration Review (Batch Review)

| Role | Agent | Rationale |
|------|-------|-----------|
| Integration Auditor | **nse-qa** | Validates all 4 files together for completeness, consistency, compliance |

**Why nse-qa for integration review:**
- Checklist-based validation against defined criteria
- Compliance scoring (pass/fail with percentages)
- Designed for artifact validation (work product quality)
- Can verify traceability (all source content accounted for)

### 4.3 Agent Capability Matrix

| Agent | Quality Score | Iterative Loop | Compliance Check | Traceability | Best For |
|-------|--------------|----------------|------------------|--------------|----------|
| ps-critic | 0.0-1.0 | ✅ Native | ❌ | ❌ | Per-task refinement |
| nse-qa | % score | ❌ | ✅ Native | ✅ | Batch validation |
| ps-reviewer | Severity | ❌ | ❌ | ❌ | Code/design review |
| nse-reviewer | Gate | ❌ | ✅ | ✅ | Technical reviews (SRR/PDR) |

---

## 5. DISC-002 Quality Criteria

> **Protocol:** DISC-002 Adversarial Review
> **Prior Art:** FEAT-001 Quality Gates (qg-0 through qg-4)

### 5.1 ps-critic: Quality Evaluator Criteria

Based on research phase implementation (see `qg-0/ps-critic-review.md`):

| Criterion | Code | Weight | Description | 0.92+ Threshold |
|-----------|------|--------|-------------|-----------------|
| Completeness | C | 0.30 | All source content extracted without omissions | 100% of source content present |
| Accuracy | A | 0.25 | Content matches source exactly without drift | Zero content modifications |
| Clarity | CL | 0.20 | Clear and understandable content | Crystal clear, well-organized |
| Actionability | AC | 0.15 | Recommendations are implementable | Specific, measurable actions |
| Traceability | T | 0.10 | Cross-references to source material | Direct links to CLAUDE.md sections |

**Quality Score Formula:** `Score = (C × 0.30) + (A × 0.25) + (CL × 0.20) + (AC × 0.15) + (T × 0.10)`

**Scoring Rubric (per criterion):**

| Score | Level | Description |
|-------|-------|-------------|
| 0.95+ | Excellent | Exceeds expectations, no improvements needed |
| 0.90-0.94 | Good | Meets expectations, minor improvements possible |
| 0.85-0.89 | Acceptable | Meets minimum bar, some improvements needed |
| 0.80-0.84 | Needs Work | Below acceptable, specific improvements required |
| < 0.80 | Poor | Significant rework required |

### 5.2 nse-qa: NASA SE Compliance Criteria

Based on research phase implementation (see `qg-0/nse-qa-audit.md`):

| Criterion | Code | Weight | Description | Pass Condition |
|-----------|------|--------|-------------|----------------|
| Technical Rigor | TR | 0.20 | Systematic methodology, structured approach | Follows established extraction patterns |
| Requirements Traceability | RT | 0.20 | Explicit linkages to source requirements | Every section traces to CLAUDE.md section |
| Verification Evidence | VE | 0.20 | Evidence sufficient to support conclusions | Line counts, diffs, file comparisons |
| Risk Identification | RI | 0.20 | Risks identified and assessed | Content loss, formatting issues documented |
| Documentation Quality | DQ | 0.20 | Format supports technical review | NPR 7123.1D compliant structure |

**Compliance Score Formula:** `Score = (TR + RT + VE + RI + DQ) / 5`

### 5.3 Integration Checklist (INT-*)

| Check ID | Criterion | Pass Condition | Verification Method |
|----------|-----------|----------------|---------------------|
| INT-001 | Complete Migration | All 371 lines accounted for | Line count comparison |
| INT-002 | No Information Loss | Diff shows no missing content | Source/target diff |
| INT-003 | Consistent Formatting | Same style across all 4 files | Style guide compliance |
| INT-004 | Cross-References Valid | All internal links work | Link validation |
| INT-005 | Template Compliance | Each file follows rules template | Template comparison |
| INT-006 | No Duplication | Content not duplicated across files | Duplicate detection |

### 5.4 DISC-002 Adversarial Findings Requirements

Per DISC-002 protocol, each review MUST identify minimum findings:

| Finding Type | Description | Minimum Required |
|--------------|-------------|------------------|
| **Blind Spots** | Areas not covered by artifact | 1+ |
| **Weak Assumptions** | Unstated assumptions that could fail | 1+ |
| **Missing Evidence** | Claims without supporting evidence | 0+ |
| **Contradictions** | Internal or cross-artifact conflicts | 0+ |

**Total Mandatory Findings:** Minimum 3 per review

**Finding Severity Classification:**

| Severity | Impact | Action Required |
|----------|--------|-----------------|
| CRITICAL | Score impact > 0.05 | Must fix before gate pass |
| HIGH | Score impact 0.02-0.05 | Should fix, may pass with plan |
| MEDIUM | Score impact 0.01-0.02 | Should fix, may defer |
| LOW | Score impact < 0.01 | Optional improvement |

### 5.5 Remediation Items (REM-*)

When a review fails to meet threshold, remediation items are generated:

| ID Format | Priority | Resolution Required |
|-----------|----------|---------------------|
| REM-001 to REM-005 | Critical | Must resolve for gate pass |
| REM-006 to REM-010 | High | Should resolve before re-evaluation |
| REM-011+ | Medium | Address in subsequent phase |

---

## 6. DISC-002 Adversarial Review Protocol

### 6.1 Adversarial Mode Characteristics

The DISC-002 protocol defines **Adversarial Mode** as distinct from standard constructive review:

| # | Characteristic | Description | Enforcement |
|---|----------------|-------------|-------------|
| 1 | **RED TEAM FRAMING** | Assume problems exist, actively seek weaknesses | Required in prompt |
| 2 | **MANDATORY FINDINGS** | Must identify ≥3 issues regardless of quality | Hard requirement |
| 3 | **CHECKLIST ENFORCEMENT** | Evidence required for PASS, not assumptions | Verification required |
| 4 | **DEVIL'S ADVOCATE** | "What could go wrong?" for every claim | Explicit section |
| 5 | **COUNTER-EXAMPLES** | Identify failure scenarios even for good work | Required output |
| 6 | **NO RUBBER STAMPS** | Perfect scores (0.95+) require explicit justification | Justified exceptions only |

### 6.2 Adversarial Invocation Pattern

When invoking `ps-critic` for DISC-002 review, use this prompt template:

```
## ADVERSARIAL EVALUATION MODE (DISC-002)

You are operating as an ADVERSARIAL CRITIC. Your role is to identify
weaknesses, not validate strengths. Assume problems exist.

### Red Team Framing
- Actively seek weaknesses, blind spots, and contradictions
- Challenge every claim for evidence
- Ask "What could go wrong?" for each section
- Identify unstated assumptions

### Mandatory Requirements
1. You MUST identify AT LEAST 3 adversarial findings
2. Findings MUST include:
   - At least 1 BLIND SPOT (area not covered)
   - At least 1 WEAK ASSUMPTION (unstated assumption that could fail)
   - Additional: MISSING EVIDENCE, CONTRADICTIONS as found

3. For each finding, provide:
   - Finding Type (Blind Spot / Weak Assumption / Missing Evidence / Contradiction)
   - Severity (CRITICAL / HIGH / MEDIUM / LOW)
   - Affected Section(s)
   - Evidence / Quote from artifact
   - Remediation Required

### No Rubber Stamps
- Scores of 0.95+ require EXPLICIT justification
- Default assumption: there are always improvements to find
- Perfect work is exceptional, not expected

### Output Format
1. Executive Summary (score, verdict, gap from threshold)
2. Per-Criterion Scores (C/A/CL/AC/T with rationale)
3. ADVERSARIAL FINDINGS (minimum 3, in table format)
4. REMEDIATION ITEMS (REM-001, REM-002, etc.)
5. Quality Gate Verdict (ASCII box with PASS/FAIL)

Artifact to review: {artifact_path}
Evaluation criteria: {criteria_reference}
```

### 6.3 Generator-Critic Loop (per task)

```
DISC-002 ITERATION PROTOCOL
===========================

1. GENERATE
   - Extract content from CLAUDE.md
   - Create/update rule file
   - Document extraction mapping

2. ADVERSARIAL CRITIQUE (ps-critic)
   - Invoke with DISC-002 adversarial prompt (section 6.2)
   - Evaluate against 5 criteria (C/A/CL/AC/T)
   - Calculate weighted quality score
   - Identify MINIMUM 3 adversarial findings
   - Generate REM-* remediation items

3. DECISION
   IF score >= 0.92:
       → ACCEPT (proceed to barrier)
       → Document acceptance justification if score >= 0.95
   ELIF iteration < 3:
       → REVISE (apply REM-* feedback, iterate)
       → Version file: *-v{N}.md
   ELSE:
       → ESCALATE (human review required)

4. FEEDBACK UPSTREAM
   - Specific REM-* items to address
   - Evidence from source/target comparison
   - Concrete revision instructions
   - Expected score improvement estimate
   - Version tracking: v1 → v2 → v3
```

### 6.4 Escalation Protocol

```
HUMAN ESCALATION (after 3 iterations)
=====================================

Trigger: Quality score < 0.92 after 3 adversarial review iterations

Artifact: orchestration/escalations/TASK-{N}-escalation.md

Content:
1. Iteration History
   - v1 score, key findings
   - v2 score, remediation applied, remaining gaps
   - v3 score, blocking issues identified

2. Adversarial Findings Summary
   - All CRITICAL and HIGH findings across iterations
   - Which were resolved, which remain

3. Human Decision Options
   a) Accept with documented caveats (record in ORCHESTRATION.yaml)
   b) Provide specific guidance for v4 (exception to 3-iteration limit)
   c) Take over manual editing (human-generated artifact)

4. Decision Recording
   - User decision captured in escalation artifact
   - ORCHESTRATION.yaml updated with human_override: true
   - Traceability maintained for audit
```

---

## 7. Sync Barrier Protocol

### 7.1 Barrier 1: Phase 1 → Phase 2 Transition

```
BARRIER 1 CHECKLIST
===================

PRE-BARRIER (all must be true):
□ TASK-002 quality ≥ 0.92 OR human-approved
□ TASK-003 quality ≥ 0.92 OR human-approved
□ TASK-004 quality ≥ 0.92 OR human-approved
□ TASK-005 quality ≥ 0.92 OR human-approved
□ All 4 rule files exist in skills/worktracker/rules/
□ No blocking issues open

TRANSITION:
□ Create Phase 1 completion checkpoint
□ Aggregate quality scores for Phase 2 input
□ Update ORCHESTRATION.yaml status

POST-BARRIER:
□ Phase 2 (nse-qa) unblocked
□ Integration review can begin
```

### 7.2 Barrier 2: Phase 2 → Phase 3 Transition

```
BARRIER 2 CHECKLIST
===================

PRE-BARRIER:
□ nse-qa compliance ≥ 92% OR human-approved
□ No critical findings in QA report
□ All major findings addressed or accepted

TRANSITION:
□ Create Phase 2 completion checkpoint
□ Document QA findings summary
□ Update ORCHESTRATION.yaml status

POST-BARRIER:
□ TASK-006 unblocked
□ Navigation update can begin
```

---

## 8. State Files

| File | Purpose | Location |
|------|---------|----------|
| `ORCHESTRATION_PLAN.md` | Strategic context (this file) | `orchestration/` |
| `ORCHESTRATION.yaml` | Machine-readable state (SSOT) | `orchestration/` |
| `ORCHESTRATION_WORKTRACKER.md` | Tactical execution tracking | `orchestration/` |

### 8.1 Artifact Locations (DISC-002 Structure)

Following the FEAT-001 research phase pattern:

```
EN-201-worktracker-skill-extraction/
├── orchestration/
│   ├── ORCHESTRATION_PLAN.md          # This file (strategic context)
│   ├── ORCHESTRATION.yaml             # Machine state (SSOT)
│   ├── ORCHESTRATION_WORKTRACKER.md   # Execution tracking (tactical)
│   │
│   ├── quality-gates/                 # DISC-002 Review Artifacts
│   │   │
│   │   ├── qg-1/                      # Quality Gate 1: Extraction Review
│   │   │   ├── ps-critic-review.md           # v1 critic review
│   │   │   ├── ps-critic-review-v2.md        # v2 (if iteration needed)
│   │   │   ├── ps-critic-review-v3.md        # v3 (max before escalation)
│   │   │   ├── nse-qa-audit.md               # v1 NASA SE audit
│   │   │   ├── nse-qa-audit-v2.md            # v2 (if iteration needed)
│   │   │   └── remediation-log.md            # REM-* tracking
│   │   │
│   │   └── qg-2/                      # Quality Gate 2: Integration Review
│   │       ├── integration-qa-report.md      # Batch integration review
│   │       └── integration-qa-report-v2.md   # v2 (if iteration needed)
│   │
│   └── escalations/                   # Human escalation docs (if needed)
│       └── TASK-{N}-escalation.md
│
└── (task files: TASK-001-*.md through TASK-007-*.md)
```

### 8.2 File Naming Conventions (DISC-002)

| Artifact Type | Naming Pattern | Version Pattern |
|---------------|----------------|-----------------|
| ps-critic review | `ps-critic-review.md` | `ps-critic-review-v{N}.md` |
| nse-qa audit | `nse-qa-audit.md` | `nse-qa-audit-v{N}.md` |
| Integration report | `integration-qa-report.md` | `integration-qa-report-v{N}.md` |
| Escalation | `TASK-{N}-escalation.md` | N/A (single instance) |
| Remediation log | `remediation-log.md` | Append-only |

### 8.3 Quality Gate Folder Structure

Each quality gate folder (`qg-{N}/`) contains:

1. **ps-critic-review.md** - Quality evaluator output with:
   - Executive Summary (score, threshold, verdict)
   - Per-artifact scores (C/A/CL/AC/T)
   - Adversarial findings (minimum 3)
   - Remediation requirements (REM-*)
   - Quality Gate Verdict (ASCII box)

2. **nse-qa-audit.md** - NASA SE compliance output with:
   - Overall determination (TR/RT/VE/RI/DQ)
   - NPR 7123.1D compliance matrix
   - Non-conformances (NCR-*)
   - Certification statement

3. **Versioned files** - When iteration needed:
   - Previous score documented
   - Improvement tracked
   - Remediation status updated

---

## 9. Execution Constraints

### 9.1 Hard Constraints (Jerry Constitution)

| Constraint | ID | Enforcement |
|------------|----|----|
| Single agent nesting | P-003 | Orchestrator → Worker only |
| File persistence | P-002 | All state to filesystem |
| No deception | P-022 | Transparent quality scores |
| User authority | P-020 | User approves escalations |

### 9.2 Workflow Constraints

| Constraint | Value | Rationale |
|------------|-------|-----------|
| Quality threshold | 0.92 | High bar for content extraction accuracy |
| Max iterations | 3 | Circuit breaker to prevent infinite loops |
| Max concurrent tasks | 4 | All Phase 1 tasks can run in parallel |
| Checkpoint frequency | PHASE | Recovery at phase boundaries |

---

## 10. Risk Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Content loss during extraction | Low | High | ps-critic validates completeness; nse-qa cross-checks |
| Quality threshold too strict | Medium | Medium | Human escalation path; threshold can be adjusted |
| Iteration loop stuck | Low | Medium | 3-iteration circuit breaker; human escalation |
| Agent hallucination | Low | Medium | Evidence-based critique; source comparison |
| Inconsistent formatting | Medium | Low | nse-qa integration check; template compliance |

---

## 11. Success Criteria

### 11.1 Phase Completion Criteria

| Phase | Criterion | Validation |
|-------|-----------|------------|
| Phase 1 | All 4 extractions ≥ 0.92 | ps-critic quality scores |
| Phase 2 | Integration review ≥ 92% | nse-qa compliance score |
| Phase 3 | Navigation works, skill loads | Manual verification |

### 11.2 Workflow Completion Criteria

| Criterion | Validation |
|-----------|------------|
| All 7 tasks complete | Task status = DONE |
| All barriers passed | Barrier status = COMPLETE |
| 371 lines migrated | Line count comparison |
| Skill loads correctly | `/worktracker` invocation test |
| EN-202, EN-203 unblocked | Dependency resolution |

---

## 12. Resumption Context

### 12.1 Current Execution State

```
WORKFLOW STATUS AS OF 2026-02-01
================================

Phase 1 (Content Extraction):
  TASK-002: PENDING
  TASK-003: PENDING
  TASK-004: PENDING
  TASK-005: PENDING

Phase 2 (Integration Review):
  nse-qa: BLOCKED (waiting Phase 1)

Phase 3 (Navigation & Validation):
  TASK-006: BLOCKED (waiting Phase 2)
  TASK-007: BLOCKED (waiting TASK-006)

Barriers:
  Barrier 1: PENDING
  Barrier 2: PENDING
```

### 12.2 Next Actions

1. Execute TASK-002 through TASK-005 in parallel
2. For each task: generate → ps-critic → iterate until ≥0.92
3. Upon all Phase 1 complete: pass Barrier 1
4. Execute nse-qa integration review
5. Continue to Phase 3

---

*Document ID: EN-201-ORCH-PLAN*
*Workflow ID: en201-extraction-20260201-001*
*Version: 1.0*
*Cross-Session Portable: All paths are repository-relative*
