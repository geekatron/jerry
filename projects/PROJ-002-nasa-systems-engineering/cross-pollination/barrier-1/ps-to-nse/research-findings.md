# Barrier 1: ps-* Research Findings for nse-* Pipeline

> **Document ID:** BARRIER-1-PS-TO-NSE
> **Date:** 2026-01-09
> **Source Pipeline:** ps-* (Problem-Solving Research)
> **Target Pipeline:** nse-* (NASA SE Formalization)
> **Phase Transition:** Research → Scope

---

## Executive Summary

The ps-* pipeline completed Phase 1 research with 3 agents analyzing skills optimization, agent design, and industry best practices. This document extracts key findings for the nse-* pipeline to formalize into requirements, risks, and architecture decisions.

---

## 1. Options Identified

| Option ID | Description | Source | Priority | Impact |
|-----------|-------------|--------|----------|--------|
| OPT-001 | Add explicit `model: opus/sonnet/haiku` to agent frontmatter | skills-optimization.md | High | Enables consistent agent behavior |
| OPT-002 | Implement Generator-Critic loops for quality assurance | agent-design.md | High | 15-25% quality improvement per research |
| OPT-003 | Add checkpointing mechanism from LangGraph | industry-practices.md | P1 | Enables debugging, replay, time-travel |
| OPT-004 | Add parallel execution primitives from Google ADK | industry-practices.md | P1 | Sequential-only is bottleneck |
| OPT-005 | Add guardrail validation hooks from OpenAI SDK | industry-practices.md | P1 | Constitutional principles need runtime enforcement |
| OPT-006 | Create ps-orchestrator and nse-orchestrator agents | agent-design.md | High | 10% efficiency improvement |
| OPT-007 | Add nse-explorer agent for divergent research | agent-design.md | Critical | All current nse-* agents are convergent |
| OPT-008 | Implement two-phase (divergent→convergent) prompting | agent-design.md | High | Supports exploration→refinement pattern |

---

## 2. Industry Best Practices Discovered

| Practice ID | Framework | Pattern | Applicability |
|-------------|-----------|---------|---------------|
| PRC-001 | Anthropic Claude | Initializer Agent Pattern | High - Better cross-session continuity |
| PRC-002 | Anthropic Claude | claude-progress.txt | High - Already partial via WORKTRACKER.md |
| PRC-003 | LangGraph | State checkpointing with time-travel | High - Currently missing |
| PRC-004 | Google ADK | SequentialAgent/ParallelAgent/LoopAgent | High - Code-first workflow |
| PRC-005 | CrewAI | Memory layers (short/long/entity) | Medium - Currently JSON files only |
| PRC-006 | OpenAI SDK | Agent-as-Tool pattern | Medium - More control than handoffs |
| PRC-007 | All Frameworks | Generator-Critic iteration | High - Quality assurance |
| PRC-008 | Anthropic | WRITE/SELECT/COMPRESS/ISOLATE taxonomy | High - Context engineering |

### Framework Comparison Summary

| Dimension | Jerry | Strength/Gap |
|-----------|-------|--------------|
| Constitutional Governance | Unique | **Strength** - P-001 to P-043 |
| L0/L1/L2 Output Levels | Unique | **Strength** - Progressive disclosure |
| Domain Specialization | nse-* NASA SE | **Strength** - NPR 7123.1D mapping |
| Parallel Execution | None | **Gap** - LangGraph/ADK have native |
| State Checkpointing | None | **Gap** - LangGraph specialty |
| Guardrail Hooks | Soft | **Gap** - OpenAI SDK has built-in |
| Generator-Critic | None | **Gap** - ADK LoopAgent |

---

## 3. Optimization Opportunities

| Area | Current State | Proposed Change | Impact |
|------|---------------|-----------------|--------|
| Activation Keywords | 18 (ps-*), 27 (nse-*) | Add 10+ missing keywords | Improved routing accuracy |
| Cognitive Mode | All nse-* convergent | Add divergent phases to nse-requirements, nse-architecture, nse-risk | Better creative exploration |
| State Management | Implicit file-based | Explicit schema with output_keys | Reliable agent chaining |
| Orchestration | Implicit pipelines | Explicit orchestrator agents | 10% efficiency gain |
| Cross-Skill Handoff | Not formalized | Define interface contracts | Enable ps-* → nse-* flows |
| Quality Loop | None | Generator-Critic pairing | 15-25% quality improvement |
| Parallel Execution | Sequential only | Fan-out/fan-in patterns | Faster multi-topic research |

---

## 4. Gaps for nse-* to Formalize

These gaps from ps-* research should become formal requirements:

| Gap ID | Description | Suggested Requirement | Priority |
|--------|-------------|----------------------|----------|
| GAP-001 | No explicit model specification | REQ: Add `model` field to frontmatter | High |
| GAP-002 | No parallel execution | REQ: Design parallel agent primitive | High |
| GAP-003 | No formal ps-analyst → nse-risk handoff | REQ: Define risk handoff protocol | High |
| GAP-004 | No quality loop for refinement | REQ: Implement generator-critic loops | Medium |
| GAP-005 | NASA SE keywords incomplete | REQ: Expand activation keywords | Medium |
| GAP-006 | All nse-* agents convergent | REQ: Add divergent nse-explorer agent | Critical |
| GAP-007 | No pipeline orchestrators | REQ: Create ps-orchestrator, nse-orchestrator | High |
| GAP-008 | No checkpointing | REQ: Implement state checkpointing | High |
| GAP-009 | No guardrail hooks | REQ: Add pre/post validation | High |
| GAP-010 | No context compaction strategy | DOC: Formalize compaction guidance | Medium |

---

## 5. Proposed Requirements for nse-* Pipeline

### From ps-r-002 (Agent Design):

| REQ ID | Requirement Statement | Priority | Rationale |
|--------|----------------------|----------|-----------|
| REQ-PS-001 | All agent definitions MUST include explicit `cognitive_mode` field | High | Enables phase transitions |
| REQ-PS-002 | Agents requiring divergent+convergent MUST implement `cognitive_phases` | High | Supports exploration→refinement |
| REQ-PS-003 | Each pipeline family MUST have dedicated orchestrator agent | High | 10% efficiency per research |
| REQ-PS-004 | nse-* pipeline MUST include divergent-mode agent | Critical | Missing Plant/Resource Investigator |
| REQ-PS-005 | Formal interface contracts MUST be defined for ps-* ↔ nse-* | Medium | No protocol exists |
| REQ-PS-006 | Design agents MUST be paired with critic agents | Medium | Generator-Critic quality |
| REQ-PS-007 | All agents MUST use consistent state schema | Medium | Reliable chaining |

### From ps-r-003 (Industry Practices):

| REQ ID | Requirement Statement | Priority | Industry Reference |
|--------|----------------------|----------|-------------------|
| REQ-IND-001 | Framework MUST implement checkpointing mechanism | P1 | LangGraph |
| REQ-IND-002 | Framework MUST support parallel execution primitive | P1 | ADK ParallelAgent |
| REQ-IND-003 | Framework MUST add guardrail validation hooks | P1 | OpenAI SDK |
| REQ-IND-004 | Framework SHOULD implement initializer agent pattern | P2 | Anthropic |
| REQ-IND-005 | Framework SHOULD document context compaction strategy | P2 | Anthropic |
| REQ-IND-006 | Framework SHOULD implement generator-critic loops | P2 | ADK LoopAgent |

---

## 6. Belbin Team Role Analysis

**Current Coverage:**

| Belbin Role | ps-* Agent | nse-* Agent | Status |
|-------------|------------|-------------|--------|
| Plant (Creative) | ps-architect (partial) | **NONE** | **Critical Gap** |
| Resource Investigator | ps-researcher | **NONE** | **Critical Gap** |
| Coordinator | **NONE** | **NONE** | **Critical Gap** |
| Shaper (Driver) | **NONE** | **NONE** | Gap |
| Monitor Evaluator | ps-analyst, ps-reviewer | nse-reviewer | Covered |
| Teamworker | ps-synthesizer | nse-reporter | Covered |
| Implementer | **NONE** | nse-integration | Partial |
| Completer Finisher | ps-validator | nse-verification | Covered |
| Specialist | ps-investigator | All nse-* | Covered |

**Recommended New Agents:**

| Proposed Agent | Family | Belbin Role | Cognitive Mode |
|----------------|--------|-------------|----------------|
| nse-explorer | nse-* | Plant + Resource Investigator | Divergent |
| nse-orchestrator | nse-* | Coordinator | Mixed |
| ps-orchestrator | ps-* | Coordinator | Mixed |
| nse-challenger | nse-* | Shaper | Divergent |

---

## Cross-Pollination Validation

This artifact is ready for nse-* pipeline consumption when:
- [ ] nse-risk reviews risks associated with proposed changes
- [ ] nse-architecture designs implementation approach
- [ ] nse-requirements formalizes into REQ statements

---

## Source Artifacts

| Artifact | Path | Agent |
|----------|------|-------|
| Skills Optimization | `ps-pipeline/phase-1-research/skills-optimization.md` | ps-r-001 |
| Agent Design | `ps-pipeline/phase-1-research/agent-design.md` | ps-r-002 |
| Industry Practices | `ps-pipeline/phase-1-research/industry-practices.md` | ps-r-003 |

---

*Cross-pollination artifact generated at Sync Barrier 1*
*Date: 2026-01-09*
