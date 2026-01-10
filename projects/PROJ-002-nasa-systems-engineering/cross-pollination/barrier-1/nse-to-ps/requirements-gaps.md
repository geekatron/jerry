# Barrier 1: nse-* Requirements Gaps for ps-* Pipeline

> **Document ID:** BARRIER-1-NSE-TO-PS
> **Date:** 2026-01-09
> **Source Pipeline:** nse-* (NASA SE Formalization)
> **Target Pipeline:** ps-* (Problem-Solving Research)
> **Phase Transition:** Scope → Research

---

## Executive Summary

The nse-* pipeline completed Phase 1 scope analysis with 2 agents analyzing skills requirements and agent requirements. This document extracts research gaps and questions for the ps-* pipeline to explore in Phase 2.

---

## 1. Formal Requirements Defined

### Skills Requirements (47 total)

| Category | Count | Sample Requirements |
|----------|-------|---------------------|
| Problem-Solving Skill | 9 | REQ-SKL-PS-001 through REQ-SKL-PS-009 |
| NASA SE Skill | 15 | REQ-SKL-NSE-001 through REQ-SKL-NSE-015 |
| Work Tracker Skill | 9 | REQ-SKL-WT-001 through REQ-SKL-WT-009 |
| Architecture Skill | 8 | REQ-SKL-ARCH-001 through REQ-SKL-ARCH-008 |
| Non-Functional | 10 | REQ-SKL-NFR-001 through REQ-SKL-NFR-010 |

### Agent Requirements (38 total)

| Category | Count | Sample Requirements |
|----------|-------|---------------------|
| Agent Definition | 18 | REQ-AGT-001 through REQ-AGT-018 |
| Orchestration | 12 | REQ-AGT-ORCH-001 through REQ-AGT-ORCH-012 |
| Persona | 8 | REQ-AGT-PER-001 through REQ-AGT-PER-008 |

---

## 2. Research Gaps Identified

These gaps require exploration by the ps-* research pipeline:

### From nse-r-001 (Skills Requirements):

| Gap ID | Missing Information | Research Question | Suggested Approach |
|--------|---------------------|-------------------|-------------------|
| RGAP-001 | Skill interface contracts | What industry patterns exist for formal skill/capability interface contracts in multi-agent systems? | Survey LangChain, AutoGen, CrewAI APIs |
| RGAP-002 | Behavioral testing frameworks | What behavioral testing frameworks are most effective for LLM agent validation? | Evaluate DeepEval, promptfoo, LangSmith |
| RGAP-003 | Product Transition phase | How do other NASA SE tools handle NPR 7123.1D Process 9 (Product Transition)? | Research NASA MBSE tools, PLM integration |
| RGAP-004 | Error handling patterns | What error handling patterns work best for cascading agent failures? | Study Temporal, Airflow, Step Functions |
| RGAP-005 | Telemetry/observability | What telemetry/observability patterns exist for agent-based systems? | Evaluate LangSmith, Helicone, Anthropic Console |

### From nse-r-002 (Agent Requirements):

| Gap ID | Missing Information | Research Question | Suggested Approach |
|--------|---------------------|-------------------|-------------------|
| RGAP-006 | Persona drift metrics | What metrics effectively measure persona consistency over long sessions? | Literature review, define KPIs |
| RGAP-007 | Cognitive mode switching | Can an agent switch cognitive modes mid-session, and what are the costs? | Empirical testing |
| RGAP-008 | Belbin role mapping | How do the 8 ps-* agents map to Belbin team roles, and are there gaps? | Role mapping analysis |
| RGAP-009 | Generator-Critic pairing | Which ps-* agent pairs show highest synergy in Generator-Critic patterns? | Synergy matrix analysis |
| RGAP-010 | Constitutional enforcement | Can P-001 through P-043 be automatically verified at runtime? | Design runtime checker |

---

## 3. Scope Constraints

These constraints from nse-* analysis impact ps-* research:

| Constraint ID | Constraint | Impact on ps-* Analysis |
|---------------|------------|-------------------------|
| CON-001 | P-003: Single nesting only | Cannot research recursive agent patterns |
| CON-002 | P-022: No deception | Must maintain transparency in all research outputs |
| CON-003 | NPR 7123.1D compliance | NASA SE research must align with 17 processes |
| CON-004 | L0/L1/L2 output levels | All research must produce tiered outputs |
| CON-005 | File persistence (P-002) | All research must be persisted to filesystem |

---

## 4. Standards Compliance Requirements

| Standard | Requirement | Research Needed |
|----------|-------------|-----------------|
| NPR 7123.1D | 17 process coverage | Processes 5, 9, 10 need mapping |
| JERRY_CONSTITUTION | P-001 through P-043 compliance | Runtime enforcement patterns |
| Agent Templates | PS_AGENT_TEMPLATE v2.0, NSE_AGENT_TEMPLATE v1.0 | Schema unification |
| INCOSE SE Handbook v5.0 | Cross-reference validation | Industry alignment check |

---

## 5. Critical Gaps Summary

### High-Severity Gaps (Must Address):

| GAP ID | Description | Severity | Upstream Source |
|--------|-------------|----------|-----------------|
| GAP-SKL-001 | No formal acceptance test criteria | High | skills-requirements.md |
| GAP-SKL-002 | No formal interface contract between skills | High | skills-requirements.md |
| GAP-AGT-003 | No formal session_context contract | Critical | agent-requirements.md |
| GAP-AGT-004 | Handoff manifest not implemented | High | agent-requirements.md |
| GAP-AGT-009 | Tool registry not centralized | High | agent-requirements.md |

### Medium-Severity Gaps (Should Address):

| GAP ID | Description | Severity | Upstream Source |
|--------|-------------|----------|-----------------|
| GAP-SKL-003 | No agent specification file format | Medium | skills-requirements.md |
| GAP-AGT-005 | Constitutional principle mapping incomplete | Medium | agent-requirements.md |
| GAP-AGT-007 | No automated persona consistency verification | High | agent-requirements.md |
| GAP-AGT-008 | Cognitive mode task routing implicit | Medium | agent-requirements.md |

---

## 6. Risk Assessment

| Risk ID | Risk Statement | Likelihood | Consequence | Score |
|---------|----------------|------------|-------------|-------|
| R-REQ-001 | IF skill interface contracts not formalized THEN cross-skill integration may fail | 4 | 4 | 16 (RED) |
| R-REQ-002 | IF behavioral tests not defined THEN skill regressions undetected | 4 | 3 | 12 (YELLOW) |
| R-REQ-003 | IF agent specs lack schema THEN inconsistent definitions | 3 | 3 | 9 (YELLOW) |
| R-REQ-004 | IF NSE processes 9,10 remain unaddressed THEN incomplete NASA coverage | 2 | 3 | 6 (GREEN) |
| R-REQ-005 | IF context isolation issues persist THEN subagent quality degrades | 3 | 4 | 12 (YELLOW) |

---

## 7. Cross-Family Integration Opportunities

The ps-* and nse-* agent families share structural overlap that can be unified:

| Component | ps-* Implementation | nse-* Implementation | Integration Action |
|-----------|---------------------|---------------------|-------------------|
| Frontmatter | YAML with 6 fields | YAML with 8 fields | Unify to superset schema |
| Identity | role, expertise, cognitive_mode | Same + NASA process ref | Add optional process refs |
| Persona | tone, style | tone, style, formality | Add formality to ps-* |
| Capabilities | allowed_tools, forbidden | Same | Create shared tool registry |
| Output Levels | L0/L1/L2 | L0/L1/L2 | Already aligned |

---

## 8. Recommended Research Tasks for ps-*

### Priority 1 (Phase 2):

| Task | Research Focus | Expected Output |
|------|----------------|-----------------|
| Research interface contracts | Survey agent framework APIs | Interface specification pattern |
| Research behavioral testing | Evaluate testing frameworks | Testing framework recommendation |
| Research error handling | Study orchestration patterns | Error recovery protocol |
| Research telemetry | Evaluate observability tools | Telemetry framework recommendation |

### Priority 2 (Phase 2-3):

| Task | Research Focus | Expected Output |
|------|----------------|-----------------|
| Research persona drift | Define measurement metrics | Persona consistency KPIs |
| Research cognitive switching | Test mode transitions | Mode switching guidelines |
| Research Belbin mapping | Analyze role coverage | Gap analysis with recommendations |
| Research constitutional automation | Design runtime checker | P-001 to P-043 verification approach |

---

## Cross-Pollination Validation

This artifact is ready for ps-* pipeline consumption when:
- [ ] ps-researcher acknowledges research gaps
- [ ] ps-analyst prioritizes gap exploration
- [ ] ps-architect considers constraints in designs

---

## Source Artifacts

| Artifact | Path | Agent |
|----------|------|-------|
| Skills Requirements | `nse-pipeline/phase-1-scope/skills-requirements.md` | nse-r-001 |
| Agent Requirements | `nse-pipeline/phase-1-scope/agent-requirements.md` | nse-r-002 |

---

*Cross-pollination artifact generated at Sync Barrier 1*
*Date: 2026-01-09*
