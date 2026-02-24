# ORCHESTRATION_PLAN.md

> **Document ID:** PROJ-009-ORCH-PLAN
> **Project:** PROJ-009-llm-deception-research
> **Workflow ID:** `llm-deception-20260221-001`
> **Status:** ACTIVE
> **Version:** 2.0
> **Created:** 2026-02-22
> **Last Updated:** 2026-02-22

## Document Sections

| Section | Purpose |
|---------|---------|
| [1. Executive Summary](#1-executive-summary) | Workflow purpose, pattern, and identification |
| [2. Workflow Architecture](#2-workflow-architecture) | Pipeline diagram and pattern classification |
| [3. Phase Definitions](#3-phase-definitions) | Per-pipeline phase tables with agents and status |
| [4. Sync Barrier Protocol](#4-sync-barrier-protocol) | Barrier transition rules and definitions |
| [5. Agent Registry](#5-agent-registry) | All 21 agents with inputs, outputs, and status |
| [6. State Management](#6-state-management) | State files, artifact paths, checkpoint strategy |
| [7. Execution Constraints](#7-execution-constraints) | Hard and soft constraints from constitution |
| [8. Quality Gate Protocol](#8-quality-gate-protocol) | C4 tournament protocol for all gates |
| [9. A/B Test Isolation Protocol](#9-ab-test-isolation-protocol) | R-002 isolation requirements |
| [10. Requirements Traceability](#10-requirements-traceability) | R-001 through R-008 mapped to phases and agents |
| [11. Risk Mitigations](#11-risk-mitigations) | Risk register with likelihood, impact, mitigation |
| [12. Session Management Strategy](#12-session-management-strategy) | 10-session execution plan |
| [13. Resumption Context](#13-resumption-context) | Current state and next actions |

---

## 1. Executive Summary

This workflow orchestrates a C4 mission-critical research project documenting LLM deception patterns -- systematic behavioral flaws arising from training incentives, not adversarial attacks. Two cross-pollinated pipelines (Problem Solving + NASA Systems Engineering) execute across 5 phases with 4 sync barriers. The project produces multi-platform content in Saucer Boy voice targeting Anthropic/Boris engagement with a constructive, evidence-driven call to action.

**8 non-negotiable requirements** (R-001 through R-008) govern all work. The primary evidence mechanism is a controlled A/B test (R-002): Agent A operates on internal LLM knowledge only, while Agent B operates exclusively on Context7 + WebSearch. Both undergo C4 adversarial review at >= 0.95 quality threshold with up to 5 revision iterations.

**Current State:** Phase 0 (Planning) complete. Phase 1 ready for execution.

**Orchestration Pattern:** Cross-Pollinated Pipeline (Pattern 5) with Sequential phases, Concurrent execution within phases, and Barrier Sync at phase boundaries.

### 1.1 Workflow Identification

| Field | Value | Source |
|-------|-------|--------|
| Workflow ID | `llm-deception-20260221-001` | user-specified |
| ID Format | `{purpose}-{YYYYMMDD}-{NNN}` | semantic-date-seq |
| Base Path | `orchestration/llm-deception-20260221-001/` | Dynamic |

**Artifact Output Locations:**

- Pipeline A (PS): `orchestration/llm-deception-20260221-001/ps/`
- Pipeline B (NSE): `orchestration/llm-deception-20260221-001/nse/`
- Cross-pollination: `orchestration/llm-deception-20260221-001/cross-pollination/`

---

## 2. Workflow Architecture

### 2.1 Pipeline Diagram

```
PS PIPELINE (ps)                              NSE PIPELINE (nse)
==============                               ================

Phase 1: Evidence Collection                 Phase 1: Requirements & Prior Art
+------------------------+                  +------------------------+
| ps-researcher-001      |                  | nse-requirements-001   |
| ps-researcher-002      |                  | nse-explorer-001       |
| ps-investigator-001    |                  |                        |
| STATUS: PENDING        |                  | STATUS: PENDING        |
+------------+-----------+                  +------------+-----------+
             |                                           |
             +-------------------+------ ----------------+
                                 |
                    +============+============+
                    ||   BARRIER 1 (QG-1)    ||
                    ||   C4 Tournament       ||
                    ||   >= 0.95, 5 iter max ||
                    +============+============+
                                 |
             +-------------------+------ ----------------+
             |                                           |
Phase 2: A/B Test Execution                  Phase 2: V&V
+------------------------+                  +------------------------+
| ps-researcher-003 (A)  |                  | nse-verification-001   |
| ps-researcher-004 (B)  |                  |                        |
| ps-critic-001          |                  |                        |
| ps-critic-002          |                  |                        |
| ps-analyst-001         |                  |                        |
| STATUS: BLOCKED        |                  | STATUS: BLOCKED        |
+------------+-----------+                  +------------+-----------+
             |                                           |
             +-------------------+------ ----------------+
                                 |
                    +============+============+
                    ||   BARRIER 2 (QG-2)    ||
                    ||   C4 Tournament       ||
                    ||   >= 0.95, 5 iter max ||
                    +============+============+
                                 |
             +-------------------+------ ----------------+
             |                                           |
Phase 3: Research Synthesis                  Phase 3: Technical Review
+------------------------+                  +------------------------+
| ps-synthesizer-001     |                  | nse-reviewer-001       |
| ps-architect-001       |                  |                        |
| STATUS: BLOCKED        |                  | STATUS: BLOCKED        |
+------------+-----------+                  +------------+-----------+
             |                                           |
             +-------------------+------ ----------------+
                                 |
                    +============+============+
                    ||   BARRIER 3 (QG-3)    ||
                    ||   C4 Tournament       ||
                    ||   >= 0.95, 5 iter max ||
                    +============+============+
                                 |
             +-------------------+------ ----------------+
             |                                           |
Phase 4: Content Production                  Phase 4: Quality Assurance
+------------------------+                  +------------------------+
| sb-voice-001 (LinkedIn)|                  | nse-qa-001             |
| sb-voice-002 (Twitter) |                  |                        |
| sb-voice-003 (Blog)    |                  |                        |
| STATUS: BLOCKED        |                  | STATUS: BLOCKED        |
+------------+-----------+                  +------------+-----------+
             |                                           |
             +-------------------+------ ----------------+
                                 |
                    +============+============+
                    ||   BARRIER 4 (QG-4)    ||
                    ||   C4 Tournament       ||
                    ||   >= 0.95, 5 iter max ||
                    +============+============+
                                 |
             +-------------------+------ ----------------+
             |                                           |
Phase 5: Final Review                        Phase 5: Final V&V
+------------------------+                  +------------------------+
| ps-reviewer-001        |                  | nse-verification-002   |
| ps-reporter-001        |                  |                        |
| STATUS: BLOCKED        |                  | STATUS: BLOCKED        |
+------------------------+                  +------------------------+
                                 |
                    +============+============+
                    ||   FINAL QG (QG-5)     ||
                    ||   C4 Tournament       ||
                    ||   >= 0.95, 5 iter max ||
                    +============+============+
```

### 2.2 Orchestration Pattern Classification

| Pattern | Applied | Description |
|---------|---------|-------------|
| Sequential | Yes | Phases execute in order (1 through 5) |
| Concurrent | Yes | PS and NSE pipelines run in parallel within each phase |
| Barrier Sync | Yes | Cross-pollination at 4 sync barriers + final QG |
| Hierarchical | Yes | Orchestrator delegates to skill-specific agents |

---

## 3. Phase Definitions

### 3.1 Pipeline A (PS) Phases

| Phase | Name | Purpose | Agents | Status |
|-------|------|---------|--------|--------|
| 1 | Evidence Collection | Academic lit, industry reports, conversation mining (R-003, R-004) | ps-researcher-001, ps-researcher-002, ps-investigator-001 | PENDING |
| 2 | A/B Test Execution | Controlled comparison internal vs external (R-001, R-002) | ps-researcher-003, ps-researcher-004, ps-critic-001, ps-critic-002, ps-analyst-001 | BLOCKED |
| 3 | Research Synthesis | Unified thesis, architectural analysis (R-004) | ps-synthesizer-001, ps-architect-001 | BLOCKED |
| 4 | Content Production | Multi-platform Saucer Boy content (R-005, R-008) | sb-voice-001, sb-voice-002, sb-voice-003 | BLOCKED |
| 5 | Final Review | Citation check, publication readiness (R-004) | ps-reviewer-001, ps-reporter-001 | BLOCKED |

### 3.2 Pipeline B (NSE) Phases

| Phase | Name | Purpose | Agents | Status |
|-------|------|---------|--------|--------|
| 1 | Requirements & Prior Art | Formalize A/B test design, prior art survey | nse-requirements-001, nse-explorer-001 | PENDING |
| 2 | Verification & Validation | A/B test methodology V&V (R-002) | nse-verification-001 | BLOCKED |
| 3 | Technical Review | Synthesis rigor review | nse-reviewer-001 | BLOCKED |
| 4 | Quality Assurance | Content audit (R-004, R-008) | nse-qa-001 | BLOCKED |
| 5 | Final V&V | Requirements verification (R-001 through R-008) | nse-verification-002 | BLOCKED |

---

## 4. Sync Barrier Protocol

### 4.1 Barrier Transition Rules

```
1. PRE-BARRIER CHECK
   [ ] All phase agents in both pipelines have completed execution
   [ ] All phase artifacts exist and are valid
   [ ] No blocking errors or unresolved issues
   [ ] All outputs persisted to filesystem (P-002)

2. CROSS-POLLINATION EXECUTION
   [ ] Extract key findings from PS pipeline phase output
   [ ] Extract key findings from NSE pipeline phase output
   [ ] Transform into cross-pollination handoff artifacts
   [ ] Validate artifact schema and content
   [ ] Persist handoff artifacts to cross-pollination/ directory

3. QUALITY GATE EXECUTION
   [ ] C4 tournament protocol applied (all 10 strategies)
   [ ] Quality score >= 0.95 achieved or 5 iterations exhausted
   [ ] All QG artifacts persisted in quality-gates/qg-{id}/

4. POST-BARRIER VERIFICATION
   [ ] Both pipelines acknowledge receipt of cross-pollination artifacts
   [ ] Inputs incorporated into next phase context
   [ ] Barrier status updated to COMPLETE
   [ ] Memory-Keeper checkpoint stored (MCP-002)
```

### 4.2 Barrier Definitions

| Barrier | After Phase | PS to NSE Artifact | NSE to PS Artifact | Quality Gate | Status |
|---------|-------------|--------------------|--------------------|-------------|--------|
| barrier-1 | Phase 1 | Evidence summary, pattern catalog, research gaps | Finalized research questions, isolation specification, methodology constraints | QG-1 | PENDING |
| barrier-2 | Phase 2 | A/B test results, comparison highlights, raw data | V&V results, methodology validation report, isolation audit | QG-2 | PENDING |
| barrier-3 | Phase 3 | Unified synthesis, architectural recommendations | Technical review findings, rigor assessment, RIDs | QG-3 | PENDING |
| barrier-4 | Phase 4 | Final content (LinkedIn, Twitter, Blog), per-platform quality scores | QA audit results, citation verification, tone compliance | QG-4 | PENDING |

---

## 5. Agent Registry

### 5.1 Phase 1 Agents

| Agent ID | Pipeline | Phase | Role | Input Artifacts | Output Path | Status |
|----------|----------|-------|------|-----------------|-------------|--------|
| ps-researcher-001 | PS | 1 | Academic literature on LLM sycophancy, deception, hallucination, RLHF failure modes | PLAN.md requirements | `ps/phase-1-evidence/ps-researcher-001/` | PENDING |
| ps-researcher-002 | PS | 1 | Industry reports on LLM behavioral flaws from authoritative sources | PLAN.md requirements | `ps/phase-1-evidence/ps-researcher-002/` | PENDING |
| ps-investigator-001 | PS | 1 | Mine conversation histories for deception patterns (R-003) | Conversation histories | `ps/phase-1-evidence/ps-investigator-001/` | PENDING |
| nse-requirements-001 | NSE | 1 | Formalize research questions and A/B test comparison criteria | PLAN.md R-001, R-002 | `nse/phase-1-requirements/nse-requirements-001/` | PENDING |
| nse-explorer-001 | NSE | 1 | Prior art survey on LLM comparison methodologies | Academic databases | `nse/phase-1-requirements/nse-explorer-001/` | PENDING |

### 5.2 Phase 2 Agents

| Agent ID | Pipeline | Phase | Role | Input Artifacts | Output Path | Status |
|----------|----------|-------|------|-----------------|-------------|--------|
| ps-researcher-003 | PS | 2 | Agent A (Control): Answer research questions using ONLY internal LLM knowledge | Finalized questions from barrier-1 | `ps/phase-2-ab-test/ps-researcher-003/` | BLOCKED |
| ps-researcher-004 | PS | 2 | Agent B (Treatment): Answer research questions using ONLY Context7 + WebSearch | Finalized questions from barrier-1 | `ps/phase-2-ab-test/ps-researcher-004/` | BLOCKED |
| ps-critic-001 | PS | 2 | C4 adversarial review of Agent A output (>= 0.95, up to 5 iterations) | ps-researcher-003 output | `ps/phase-2-ab-test/ps-critic-001/` | BLOCKED |
| ps-critic-002 | PS | 2 | C4 adversarial review of Agent B output (>= 0.95, up to 5 iterations) | ps-researcher-004 output | `ps/phase-2-ab-test/ps-critic-002/` | BLOCKED |
| ps-analyst-001 | PS | 2 | Comparative analysis across all dimensions (accuracy, currency, completeness, sources, calibration) | ps-critic-001 + ps-critic-002 final outputs | `ps/phase-2-ab-test/ps-analyst-001/` | BLOCKED |
| nse-verification-001 | NSE | 2 | V&V of A/B test methodology -- isolation, question identity, comparison fairness | ps-researcher-003 + ps-researcher-004 configs | `nse/phase-2-vv/nse-verification-001/` | BLOCKED |

### 5.3 Phase 3 Agents

| Agent ID | Pipeline | Phase | Role | Input Artifacts | Output Path | Status |
|----------|----------|-------|------|-----------------|-------------|--------|
| ps-synthesizer-001 | PS | 3 | Synthesize Phase 1 evidence + Phase 2 A/B results into unified thesis | Phase 1 evidence + Phase 2 analysis | `ps/phase-3-synthesis/ps-synthesizer-001/` | BLOCKED |
| ps-architect-001 | PS | 3 | Map deception patterns to training incentive structures; propose architectural solutions | ps-synthesizer-001 output | `ps/phase-3-synthesis/ps-architect-001/` | BLOCKED |
| nse-reviewer-001 | NSE | 3 | Technical review of synthesis for rigor and completeness | ps-synthesizer-001 + ps-architect-001 outputs | `nse/phase-3-review/nse-reviewer-001/` | BLOCKED |

### 5.4 Phase 4 Agents

| Agent ID | Pipeline | Phase | Role | Input Artifacts | Output Path | Status |
|----------|----------|-------|------|-----------------|-------------|--------|
| sb-voice-001 | PS | 4 | Produce LinkedIn post (1500-2000 chars) in Saucer Boy voice | Phase 3 synthesis | `ps/phase-4-content/sb-voice-001/` | BLOCKED |
| sb-voice-002 | PS | 4 | Produce X/Twitter thread (5-8 tweets) in Saucer Boy voice | Phase 3 synthesis | `ps/phase-4-content/sb-voice-002/` | BLOCKED |
| sb-voice-003 | PS | 4 | Produce blog article (1500-2500 words) in Saucer Boy voice | Phase 3 synthesis | `ps/phase-4-content/sb-voice-003/` | BLOCKED |
| nse-qa-001 | NSE | 4 | Quality audit of final content against R-004 (citations) and R-008 (tone) | sb-voice-001/002/003 outputs | `nse/phase-4-qa/nse-qa-001/` | BLOCKED |

### 5.5 Phase 5 Agents

| Agent ID | Pipeline | Phase | Role | Input Artifacts | Output Path | Status |
|----------|----------|-------|------|-----------------|-------------|--------|
| ps-reviewer-001 | PS | 5 | Final cross-check of all citations, sources, and claims | All content outputs | `ps/phase-5-final/ps-reviewer-001/` | BLOCKED |
| ps-reporter-001 | PS | 5 | Publication readiness report | All project artifacts | `ps/phase-5-final/ps-reporter-001/` | BLOCKED |
| nse-verification-002 | NSE | 5 | Final V&V -- all requirements (R-001 through R-008) verified against deliverables | All deliverables | `nse/phase-5-final-vv/nse-verification-002/` | BLOCKED |

---

## 6. State Management

### 6.1 State Files

| File | Purpose |
|------|---------|
| `ORCHESTRATION.yaml` | Machine-readable state (SSOT) -- phases, agents, barriers, quality gates |
| `ORCHESTRATION_WORKTRACKER.md` | Tactical execution documentation -- session logs, decisions |
| `ORCHESTRATION_PLAN.md` | This file -- strategic context and architecture |

### 6.2 Artifact Path Structure

All artifacts are stored under the workflow's base path using dynamic identifiers. All paths below are relative to `projects/PROJ-009-llm-deception-research/`:

```
orchestration/llm-deception-20260221-001/
+-- ORCHESTRATION.yaml
+-- ORCHESTRATION_PLAN.md
+-- ORCHESTRATION_WORKTRACKER.md
+-- ps/
|   +-- phase-1-evidence/
|   |   +-- ps-researcher-001/
|   |   |   +-- academic-literature.md
|   |   |   +-- sources.md
|   |   +-- ps-researcher-002/
|   |   |   +-- industry-reports.md
|   |   |   +-- sources.md
|   |   +-- ps-investigator-001/
|   |       +-- conversation-mining.md
|   |       +-- pattern-catalog.md
|   +-- phase-2-ab-test/
|   |   +-- ps-researcher-003/
|   |   |   +-- agent-a-responses.md
|   |   |   +-- agent-a-revision-{N}.md
|   |   +-- ps-researcher-004/
|   |   |   +-- agent-b-responses.md
|   |   |   +-- agent-b-revision-{N}.md
|   |   +-- ps-critic-001/
|   |   |   +-- agent-a-review-{N}.md
|   |   +-- ps-critic-002/
|   |   |   +-- agent-b-review-{N}.md
|   |   +-- ps-analyst-001/
|   |       +-- comparative-analysis.md
|   +-- phase-3-synthesis/
|   |   +-- ps-synthesizer-001/
|   |   |   +-- unified-synthesis.md
|   |   +-- ps-architect-001/
|   |       +-- architectural-analysis.md
|   |       +-- solution-recommendations.md
|   +-- phase-4-content/
|   |   +-- sb-voice-001/
|   |   |   +-- linkedin-post.md
|   |   |   +-- linkedin-revision-{N}.md
|   |   +-- sb-voice-002/
|   |   |   +-- twitter-thread.md
|   |   |   +-- twitter-revision-{N}.md
|   |   +-- sb-voice-003/
|   |       +-- blog-article.md
|   |       +-- blog-revision-{N}.md
|   +-- phase-5-final/
|       +-- ps-reviewer-001/
|       |   +-- citation-check.md
|       +-- ps-reporter-001/
|           +-- publication-readiness-report.md
+-- nse/
|   +-- phase-1-requirements/
|   |   +-- nse-requirements-001/
|   |   |   +-- research-questions.md
|   |   |   +-- ab-test-specification.md
|   |   +-- nse-explorer-001/
|   |       +-- prior-art-survey.md
|   +-- phase-2-vv/
|   |   +-- nse-verification-001/
|   |       +-- methodology-validation.md
|   |       +-- isolation-audit.md
|   +-- phase-3-review/
|   |   +-- nse-reviewer-001/
|   |       +-- technical-review.md
|   |       +-- rids.md
|   +-- phase-4-qa/
|   |   +-- nse-qa-001/
|   |       +-- content-audit.md
|   |       +-- citation-verification.md
|   |       +-- tone-compliance.md
|   +-- phase-5-final-vv/
|       +-- nse-verification-002/
|           +-- requirements-verification-matrix.md
+-- cross-pollination/
|   +-- barrier-1/
|   |   +-- ps-to-nse/
|   |   |   +-- handoff.md
|   |   +-- nse-to-ps/
|   |       +-- handoff.md
|   +-- barrier-2/
|   |   +-- ps-to-nse/
|   |   |   +-- handoff.md
|   |   +-- nse-to-ps/
|   |       +-- handoff.md
|   +-- barrier-3/
|   |   +-- ps-to-nse/
|   |   |   +-- handoff.md
|   |   +-- nse-to-ps/
|   |       +-- handoff.md
|   +-- barrier-4/
|       +-- ps-to-nse/
|       |   +-- handoff.md
|       +-- nse-to-ps/
|           +-- handoff.md
+-- quality-gates/
    +-- qg-1/
    |   +-- tournament-results.md
    |   +-- scores.md
    +-- qg-2/
    |   +-- tournament-results.md
    |   +-- scores.md
    |   +-- qg-2a-agent-a/
    |   |   +-- tournament-results.md
    |   +-- qg-2b-agent-b/
    |       +-- tournament-results.md
    +-- qg-3/
    |   +-- tournament-results.md
    |   +-- scores.md
    +-- qg-4/
    |   +-- tournament-results.md
    |   +-- scores.md
    |   +-- qg-4l-linkedin/
    |   |   +-- tournament-results.md
    |   +-- qg-4t-twitter/
    |   |   +-- tournament-results.md
    |   +-- qg-4b-blog/
    |       +-- tournament-results.md
    +-- qg-5/
        +-- tournament-results.md
        +-- scores.md
```

### 6.3 Checkpoint Strategy

| Trigger | When | Purpose |
|---------|------|---------|
| PHASE_COMPLETE | After each phase completes in both pipelines | Phase-level rollback point |
| BARRIER_COMPLETE | After each sync barrier + quality gate | Cross-pollination recovery point |
| MANUAL | User-triggered | Debug and inspection |
| COMPACTION | Context fill >= 0.80 (AE-006c) | Emergency state preservation |

---

## 7. Execution Constraints

### 7.1 Hard Constraints (Jerry Constitution)

| Constraint | ID | Enforcement |
|------------|----|----|
| Single agent nesting | P-003 | Orchestrator to Worker only -- no worker-spawns-worker |
| File persistence | P-002 | All state and artifacts to filesystem |
| No deception | P-022 | Transparent reasoning and limitations |
| User authority | P-020 | User approves quality gates and publication |

### 7.1.1 Worktracker Entity Templates

> **WTI-007:** Entity files (EPIC, FEATURE, ENABLER, TASK, etc.) created during orchestration MUST use canonical templates from `.context/templates/worktracker/`. Read the appropriate template first, then populate. Do not create entity files from memory or by copying other instance files.

### 7.2 Soft Constraints

| Constraint | Value | Rationale |
|------------|-------|-----------|
| Max concurrent agents | 5 | Resource management -- prevent context overflow |
| Max quality gate iterations | 5 | Circuit breaker -- escalate to human if not met |
| Checkpoint frequency | PHASE | Recovery granularity at phase boundaries |
| Context fill monitoring | AE-006 graduated | NOMINAL < 0.70, WARNING >= 0.70, CRITICAL >= 0.80, EMERGENCY >= 0.88 |

---

## 8. Quality Gate Protocol

### 8.1 C4 Tournament Protocol

All quality gates apply the full C4 tournament protocol (all 10 selected adversarial strategies). This is mandated by the project criticality level (C4: irreversible once published, public-facing, mission-critical).

**Execution sequence (H-16 ordering enforced):**

1. **adv-selector** confirms all 10 strategies required for C4 criticality
2. **adv-executor** applies strategies in H-16 canonical order:
   - S-010 Self-Refine (self-review before presenting)
   - S-003 Steelman (strengthen before critiquing -- H-16 mandates before S-002)
   - S-002 Devil's Advocate (identify weaknesses)
   - S-004 Pre-Mortem (anticipate failure modes)
   - S-001 Red Team (adversarial attack simulation)
   - S-007 Constitutional AI Critique (governance compliance)
   - S-011 Chain-of-Verification (claim verification)
   - S-012 FMEA (failure mode and effects analysis)
   - S-013 Inversion (reverse assumption testing)
3. **adv-scorer** applies S-014 LLM-as-Judge with 6-dimension rubric:

| Dimension | Weight |
|-----------|--------|
| Completeness | 0.20 |
| Internal Consistency | 0.20 |
| Methodological Rigor | 0.20 |
| Evidence Quality | 0.15 |
| Actionability | 0.15 |
| Traceability | 0.10 |

4. **Revision loop:** Up to 5 iterations with feedback returned to creator agent
5. **Threshold:** >= 0.95 weighted composite (project-specific per R-002/R-005)
6. **Artifacts:** All tournament results persisted in `quality-gates/qg-{id}/`

### 8.2 Quality Gate Inventory

| Gate ID | After | Scope | Deliverables Under Review | Status |
|---------|-------|-------|---------------------------|--------|
| QG-1 | Phase 1 | Barrier 1 | Evidence summary, pattern catalog, research questions, methodology | PENDING |
| QG-2 | Phase 2 | Barrier 2 | A/B test results, comparative analysis, V&V report | PENDING |
| QG-2A | Phase 2 | Agent A review | Agent A (internal knowledge) responses -- all revisions | PENDING |
| QG-2B | Phase 2 | Agent B review | Agent B (Context7 + WebSearch) responses -- all revisions | PENDING |
| QG-3 | Phase 3 | Barrier 3 | Unified synthesis, architectural recommendations, technical review | PENDING |
| QG-4 | Phase 4 | Barrier 4 | All content outputs, QA audit results | PENDING |
| QG-4L | Phase 4 | LinkedIn review | LinkedIn post -- Saucer Boy voice + accuracy | PENDING |
| QG-4T | Phase 4 | Twitter review | Twitter thread -- Saucer Boy voice + accuracy | PENDING |
| QG-4B | Phase 4 | Blog review | Blog article -- Saucer Boy voice + accuracy | PENDING |
| QG-5 | Phase 5 | Final gate | All deliverables, requirements verification matrix | PENDING |

**Total quality gates: 10**

---

## 9. A/B Test Isolation Protocol

Per R-002, the A/B test requires strict isolation between Agent A (Control) and Agent B (Treatment). This section documents the enforcement mechanisms.

### 9.1 Isolation Matrix

| Dimension | Agent A (Control) | Agent B (Treatment) |
|-----------|-------------------|---------------------|
| Data source | Internal LLM knowledge ONLY | Context7 + WebSearch ONLY |
| Tool access | NO web tools, NO Context7 | Context7 resolve + query, WebSearch, WebFetch |
| Research questions | Identical set (finalized at barrier-1) | Identical set (finalized at barrier-1) |
| Output directory | `.../ps-researcher-003/` | `.../ps-researcher-004/` |
| Isolation enforcement | Cannot see Agent B outputs at any point | Cannot see Agent A outputs at any point |
| Quality review | C4 adversarial (>= 0.95, up to 5 iterations) via ps-critic-001 | C4 adversarial (>= 0.95, up to 5 iterations) via ps-critic-002 |
| Revision tracking | Every revision preserved (agent-a-revision-{N}.md) | Every revision preserved (agent-b-revision-{N}.md) |

### 9.2 Isolation Enforcement

1. **Separate invocations:** Agent A and Agent B are invoked in separate agent calls with no shared context
2. **Separate output directories:** Outputs written to distinct paths that the other agent never reads
3. **Separate critics:** ps-critic-001 reviews only Agent A; ps-critic-002 reviews only Agent B
4. **Post-hoc comparison only:** ps-analyst-001 performs comparative analysis AFTER both agents complete and pass their respective quality gates
5. **V&V audit:** nse-verification-001 independently validates that isolation was maintained throughout

### 9.3 Comparison Dimensions

| Dimension | Measurement | Expected Outcome |
|-----------|-------------|------------------|
| Factual Accuracy | Verifiable claims vs. hallucinations | Agent B significantly higher |
| Currency | Information freshness (months since last update) | Agent B uses current data |
| Completeness | Coverage of known facts | Agent B more comprehensive |
| Source Quality | Number and authority of citations | Agent B has verifiable sources |
| Confidence Calibration | Claimed confidence vs. actual accuracy | Agent A over-confident on stale data |

---

## 10. Requirements Traceability

| Requirement | Description | Verified By Phase(s) | Verified By Agent(s) | Final V&V |
|-------------|-------------|----------------------|----------------------|-----------|
| R-001 | Stale Data Problem: demonstrate LLM internal data is stale vs. fresh searches | Phase 2 (A/B test) | ps-researcher-003, ps-researcher-004, ps-analyst-001 | nse-verification-002 |
| R-002 | A/B Test Design: controlled comparison with isolation, C4 review, revision preservation | Phase 2 | ps-researcher-003, ps-researcher-004, ps-critic-001, ps-critic-002, nse-verification-001 | nse-verification-002 |
| R-003 | Conversation History Mining: scan histories for deception patterns with timestamps | Phase 1 | ps-investigator-001 | nse-verification-002 |
| R-004 | Evidence-Driven Decisions: data-driven, citations, URLs, persisted in repo | Phase 1, 2, 3, 5 | ps-researcher-001, ps-researcher-002, ps-synthesizer-001, ps-reviewer-001 | nse-verification-002 |
| R-005 | Publication Quality Gate: /saucer-boy + C4 /adversary >= 0.95, up to 5 iterations, revisions preserved | Phase 4 | sb-voice-001, sb-voice-002, sb-voice-003, nse-qa-001 | nse-verification-002 |
| R-006 | Full Orchestration: /orchestration + /problem-solving + /nasa-se, no shortcuts | All | All agents | nse-verification-002 |
| R-007 | No Token Budget: mission-critical, quality over efficiency | All | All agents | nse-verification-002 |
| R-008 | Constructive Tone: highlight problems without mocking, offer opportunity to do better | Phase 4, 5 | sb-voice-001, sb-voice-002, sb-voice-003, nse-qa-001, ps-reviewer-001 | nse-verification-002 |

---

## 11. Risk Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Context window overflow | High | High | 10-session strategy with AE-006 graduated monitoring; checkpoint at every phase boundary; Memory-Keeper persistence at barriers |
| Quality gate loops (>5 iterations) | Medium | Medium | Hard cap at 5 iterations; escalate to human review if threshold not met after 5; focus revision feedback on lowest-scoring dimensions |
| A/B test isolation breach | Low | Critical | Separate agent invocations with no shared context; separate output directories; nse-verification-001 audit; V&V confirmation at barrier-2 |
| Citation URL rot | Medium | Medium | WebFetch verification of all URLs in Phase 5 by ps-reviewer-001; flag broken links for replacement |
| Saucer Boy voice inconsistency | Medium | Medium | Explicit /saucer-boy skill invocation with full context per platform; C4 adversarial review includes voice fidelity dimension |
| Compaction event during critical phase | Medium | High | AE-006 graduated escalation; mandatory checkpoint before compaction; session restart with Memory-Keeper retrieval |
| Research question bias | Low | Medium | nse-requirements-001 formalizes questions; nse-explorer-001 validates against prior art; questions finalized before A/B test begins |
| Stale data in Agent B responses | Low | Low | Agent B exclusively uses Context7 + WebSearch; freshness is the treatment variable; timestamps on all sources |

---

## 12. Session Management Strategy

| Session | Phase | Work | Key Outputs |
|---------|-------|------|-------------|
| 1 | 0 | Orchestration planning, scaffolding, work decomposition | ORCHESTRATION_PLAN.md, ORCHESTRATION.yaml, entity files |
| 2 | 1 | PS: ps-researcher-001 (academic literature) | Academic literature review with citations |
| 3 | 1 | PS: ps-researcher-002 (industry reports), ps-investigator-001 (conversation mining) | Industry reports, pattern catalog |
| 4 | 1 | NSE: nse-requirements-001, nse-explorer-001 + Barrier 1 + QG-1 | Research questions, prior art, barrier-1 cross-pollination |
| 5 | 2 | PS: ps-researcher-003 (Agent A), ps-critic-001 (A review) | Agent A responses + revisions |
| 6 | 2 | PS: ps-researcher-004 (Agent B), ps-critic-002 (B review) | Agent B responses + revisions |
| 7 | 2 | PS: ps-analyst-001 + NSE: nse-verification-001 + Barrier 2 + QG-2 | Comparative analysis, V&V, barrier-2 cross-pollination |
| 8 | 3 | PS: ps-synthesizer-001, ps-architect-001 + NSE: nse-reviewer-001 + Barrier 3 + QG-3 | Unified synthesis, architecture, technical review |
| 9 | 4 | PS: sb-voice-001/002/003 + NSE: nse-qa-001 + Barrier 4 + QG-4/4L/4T/4B | LinkedIn, Twitter, Blog content + QA audit |
| 10 | 5 | PS: ps-reviewer-001, ps-reporter-001 + NSE: nse-verification-002 + QG-5 | Citation check, publication readiness, final V&V |

---

## 13. Resumption Context

### 13.1 Current Execution State

```
WORKFLOW STATUS AS OF 2026-02-22
================================

Pipeline A (PS):
  Phase 1 (Evidence Collection):     PENDING
  Phase 2 (A/B Test Execution):      BLOCKED (by Phase 1)
  Phase 3 (Research Synthesis):      BLOCKED (by Phase 2)
  Phase 4 (Content Production):      BLOCKED (by Phase 3)
  Phase 5 (Final Review):           BLOCKED (by Phase 4)

Pipeline B (NSE):
  Phase 1 (Requirements & Prior Art): PENDING
  Phase 2 (Verification & Validation): BLOCKED (by Phase 1)
  Phase 3 (Technical Review):        BLOCKED (by Phase 2)
  Phase 4 (Quality Assurance):       BLOCKED (by Phase 3)
  Phase 5 (Final V&V):              BLOCKED (by Phase 4)

Barriers:
  Barrier 1 (QG-1): PENDING (after Phase 1)
  Barrier 2 (QG-2): PENDING (after Phase 2)
  Barrier 3 (QG-3): PENDING (after Phase 3)
  Barrier 4 (QG-4): PENDING (after Phase 4)
  Final QG (QG-5):  PENDING (after Phase 5)

Quality Gates:
  QG-1:  PENDING
  QG-2:  PENDING
  QG-2A: PENDING
  QG-2B: PENDING
  QG-3:  PENDING
  QG-4:  PENDING
  QG-4L: PENDING
  QG-4T: PENDING
  QG-4B: PENDING
  QG-5:  PENDING
```

### 13.2 Next Actions

1. **Execute Phase 1 PS pipeline agents** -- ps-researcher-001 (academic lit), ps-researcher-002 (industry reports), ps-investigator-001 (conversation mining) can run concurrently
2. **Execute Phase 1 NSE pipeline agents** -- nse-requirements-001 (formalize questions), nse-explorer-001 (prior art) can run concurrently with PS Phase 1
3. **Prepare for Barrier 1** -- once all Phase 1 agents complete, execute cross-pollination and QG-1 tournament

---

*Document ID: PROJ-009-ORCH-PLAN*
*Workflow ID: llm-deception-20260221-001*
*Version: 2.0*
*Cross-Session Portable: All paths are repository-relative*
*Generated by: orch-planner agent*
*This document is the strategic context reference for the LLM Deception Research orchestration. For machine-readable state, see ORCHESTRATION.yaml. For tactical execution logs, see ORCHESTRATION_WORKTRACKER.md.*
