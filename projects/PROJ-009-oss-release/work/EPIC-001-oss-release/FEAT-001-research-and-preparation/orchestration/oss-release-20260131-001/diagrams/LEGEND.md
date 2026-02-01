# Orchestration Diagram Legend

> **Document ID:** PROJ-009-ORCH-DIAGRAM-LEGEND
> **Version:** 5.4.0
> **Created:** 2026-02-01
> **Diagram File:** `orchestration-detailed.mmd`

---

## Color Scheme (Dark Theme Optimized)

### Phase Status Colors

| Color | Hex | Meaning |
|-------|-----|---------|
| Dark Green | `#22543d` | COMPLETE - Phase/tier finished successfully |
| Purple | `#553c9a` | READY - Phase/tier unblocked, awaiting execution |
| Gray | `#4a5568` | BLOCKED - Phase/tier waiting on dependencies |

### Tier Designation Colors

| Color | Hex | Tier | Meaning |
|-------|-----|------|---------|
| Yellow/Amber | `#744210` | Tier 1 | Foundation/Critical work |
| Blue | `#2c5282` | Tier 2 | Parallel execution |
| Teal | `#285e61` | Tier 3 | Dependent work |
| Red | `#742a2a` | Tier 4 | Synthesis/Final |

### Pipeline Colors

| Color | Hex | Pipeline |
|-------|-----|----------|
| Purple | `#3c366b` | PS (Problem-Solving) Pipeline |
| Teal | `#234e52` | NSE (NASA SE) Pipeline |

### Quality Gate Colors

| Color | Meaning |
|-------|---------|
| Green border | PASSED (>= 0.92 threshold) |
| Red fill | FAILED (< 0.92 threshold) |
| Gray | PENDING |

### Special Elements

| Color | Element |
|-------|---------|
| Orange/Yellow | Checkpoints (CP-001 through CP-005) |
| Orange/Yellow | Discovery nodes (DISC-001) |
| Orange/Yellow | Remediation actions |

---

## Agent Identification

### PS Pipeline Agents (21 total)

| ID | Agent Name | Role | Phase(s) |
|----|------------|------|----------|
| PS-01 | ps-researcher | Research Specialist | 0, 1 |
| PS-01a | ps-researcher-claude-code | Claude Code CLI Research | 0 |
| PS-01b | ps-researcher-claude-md | CLAUDE.md Optimization Research | 0 |
| PS-01c | ps-researcher-plugins | Plugin Architecture Research | 0 |
| PS-01d | ps-researcher-skills | Skills Patterns Research | 0 |
| PS-01e | ps-researcher-decomposition | Decomposition Research | 0 |
| PS-02 | ps-analyst | Analysis Specialist | 0, 1 |
| PS-03-001 | ps-architect-001 | ADR-001 CLAUDE.md Decomposition | 2 |
| PS-03-002 | ps-architect-002 | ADR-002 Repository Sync | 2 |
| PS-03-003 | ps-architect-003 | ADR-003 Worktracker Extraction | 2 |
| PS-03-004 | ps-architect-004 | ADR-004 Multi-Persona Docs | 2 |
| PS-03-005 | ps-architect-005 | ADR-005 Repository Migration | 2 |
| PS-03-006 | ps-architect-006 | ADR-006 Transcript Templates | 2 |
| PS-03-007 | ps-architect-007 | ADR-007 OSS Checklist | 2 |
| PS-04 | ps-critic | ADVERSARIAL Quality Evaluator | QG 0-4 |
| PS-05 | ps-validator | Validation Specialist | 3 |
| PS-06 | ps-synthesizer | Synthesis Specialist | 3 |
| PS-07 | ps-reviewer | Review Specialist | 3 |
| PS-08 | ps-investigator | Investigation Specialist | 1 |
| PS-09 | ps-reporter | Reporting Specialist | 0-4 |

### NSE Pipeline Agents (10 total)

| ID | Agent Name | Role | Phase(s) |
|----|------------|------|----------|
| NSE-01 | nse-requirements | Requirements Engineer | 0, 2 |
| NSE-02 | nse-verification | V&V Specialist | 1, 4 |
| NSE-03 | nse-risk | Risk Manager (CONTINUOUS) | 0-4 |
| NSE-04 | nse-reviewer | Technical Review Gate | 3 |
| NSE-05 | nse-integration | System Integration | 2 |
| NSE-06 | nse-configuration | Config Management | 2, 3 |
| NSE-07 | nse-architecture | Technical Architect | 2 |
| NSE-08 | nse-explorer | Exploration Engineer | 0 |
| NSE-09 | nse-qa | QA Specialist (NASA Audit) | QG 0-4 |
| NSE-10 | nse-reporter | SE Status Reporter | 0-4 |

---

## Quality Gates

### Gate Summary

| Gate | Phase | Tier | Threshold | Score | Status |
|------|-------|------|-----------|-------|--------|
| QG-0 v1 | 0 | - | 0.92 | 0.876 | FAILED |
| QG-0 v2 | 0 | - | 0.92 | 0.936 | PASSED |
| QG-1 | 1 | - | 0.92 | 0.942 | PASSED |
| QG-2.1 | 2 | 1 | 0.92 | 0.94 | PASSED |
| QG-2.2 | 2 | 2 | 0.92 | 0.9345 | PASSED |
| QG-2.3 | 2 | 3 | 0.92 | 0.955 | PASSED |
| QG-2.4 | 2 | 4 | 0.92 | 0.96 | PASSED |
| QG-3 v1 | 3 | - | 0.92 | 0.915 | FAILED |
| QG-3 v2 | 3 | - | 0.92 | 0.93 | PASSED |
| QG-4 | 4 | - | 0.92 | - | PENDING |

### Dual Evaluators

Each quality gate uses TWO evaluators:
1. **ps-critic** (ADVERSARIAL) - Uses DISC-002 protocol
2. **nse-qa** (NASA Audit) - Uses NPR-7123.1D protocol

---

## Checkpoints

| ID | Location | Trigger | Timestamp |
|----|----------|---------|-----------|
| CP-001 | After Barrier 1 | BARRIER_COMPLETE | 2026-01-31T21:45:00Z |
| CP-002 | After Barrier 2 | BARRIER_COMPLETE | 2026-01-31T22:45:00Z |
| CP-003 | After Barrier 3 | BARRIER_COMPLETE | 2026-02-01 |
| CP-004 | After Barrier 4 | BARRIER_COMPLETE | 2026-02-01 |
| CP-005 | Workflow Complete | WORKFLOW_COMPLETE | PENDING |

---

## Barriers

| ID | After Phase | Status | Cross-Pollination |
|----|-------------|--------|-------------------|
| Barrier 1 | Phase 0 | COMPLETE | PS-to-NSE: 9 artifacts, NSE-to-PS: 5 artifacts |
| Barrier 2 | Phase 1 | COMPLETE | PS-to-NSE: 7 artifacts, NSE-to-PS: 4 artifacts |
| Barrier 3 | Phase 2 | COMPLETE | PS-to-NSE: 7 ADRs (~30k words), NSE-to-PS: 4 artifacts |
| Barrier 4 | Phase 3 | COMPLETE | PS-to-NSE: 3 artifacts, NSE-to-PS: 3 artifacts |

---

## Adversarial Feedback Loops

The diagram shows dotted lines representing adversarial feedback loops:

1. **QG-0 v1 FAIL -> DISC-001 -> QG-0 v2 PASS**
   - ps-critic identified 5 missed research topics
   - Remediation: 5 expanded research agents (PS-01a through PS-01e)
   - Result: +6.3% improvement (0.876 -> 0.931)

2. **QG-3 v1 FAIL -> Remediation -> QG-3 v2 PASS**
   - ps-critic identified CRIT-001 (VR chaos), CRIT-002 (RPN error), HIGH-001 (self-review)
   - Remediation: vr-reconciliation.md (SSOT), self-review-rationale.md (6 controls), RPN corrected (717)
   - Result: CONDITIONAL PASS (0.88) with minor gaps accepted

---

## ADR Dependency Graph (Phase 2)

```
TIER 1: ADR-001 (CRITICAL - Foundation)
         |
    +----+----+----+----+
    |    |    |    |    |
    v    v    v    v    v
TIER 2: ADR-002  ADR-003  ADR-004  ADR-006  nse-architecture
         |
         +--------+
         |        |
         v        v
TIER 3: ADR-005   nse-integration
         |
         v
TIER 4: ADR-007 (Synthesis - depends on ALL)
```

---

## Rendering the Diagram

```bash
# Using Mermaid CLI (mmdc)
mmdc -i orchestration-detailed.mmd -o orchestration-detailed.svg -b transparent

# With specific width
mmdc -i orchestration-detailed.mmd -o orchestration-detailed.png -w 3000 -b '#1a202c'
```

---

## Current State Summary

| Metric | Value |
|--------|-------|
| Phases Complete | 4/5 (Phase 0, 1, 2, 3) |
| Phases Ready | 1/5 (Phase 4) |
| Quality Gates Passed | 7/8 (QG-0, QG-1, QG-2.1-2.4, QG-3) |
| Barriers Complete | 4/4 |
| Checkpoints Created | 4/5 (CP-001 through CP-004) |
| Agents Executed | 26/30 |
| Total Agents | 30 (21 PS + 10 NSE - 1 shared ps-critic) |
| Remediation Cycles | 2 (QG-0, QG-3) |
