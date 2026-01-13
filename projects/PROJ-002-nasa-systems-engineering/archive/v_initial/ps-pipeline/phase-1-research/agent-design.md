# Agent Design and Best Practices Research

> **Document ID:** ps-r-002
> **Phase:** 1 - Research (ps-* Pipeline)
> **Project:** PROJ-002-nasa-systems-engineering
> **Date:** 2026-01-09
> **Agent:** ps-researcher

---

## L0: Executive Summary

Current Jerry Framework agent designs exhibit strong role differentiation and domain-specific personas, but lack cognitive mode diversity (all nse-* agents are convergent), missing the divergent-convergent phase transitions recommended by persona theory research. Orchestration patterns are implicit rather than explicit, and Belbin team role coverage is incomplete with no dedicated Plant (creative/divergent) role among nse-* agents.

---

## L1: Technical Analysis

### 1. ps-* Agent Design Analysis

The problem-solving pipeline includes 8 agents with distinct responsibilities:

| Agent | Primary Role | Cognitive Mode | Belbin Analog |
|-------|--------------|----------------|---------------|
| ps-researcher | Deep research, web search, document analysis | Divergent | Resource Investigator |
| ps-analyst | Gap analysis, synthesis, pattern recognition | Convergent | Monitor Evaluator |
| ps-architect | System design, component relationships | Mixed | Plant/Specialist |
| ps-investigator | Root cause analysis, evidence gathering | Convergent | Specialist |
| ps-reporter | Status synthesis, executive communication | Convergent | Completer Finisher |
| ps-reviewer | Quality validation, checklist verification | Convergent | Monitor Evaluator |
| ps-synthesizer | Multi-source integration, coherent narratives | Convergent | Teamworker |
| ps-validator | Correctness verification, testing | Convergent | Completer Finisher |

**Strengths:**
- Clear role differentiation between research, analysis, and synthesis phases
- Pipeline structure supports handoff between agents
- L0/L1/L2 output levels standardized across agents

**Gaps Identified:**
- No explicit cognitive_mode metadata field in agent definitions
- Orchestration patterns not formalized
- State schema for agent chaining not consistently defined

### 2. nse-* Agent Design Analysis

The NASA Systems Engineering pipeline includes 8 agents mapped to NPR 7123.1D processes:

| Agent | NASA Processes | Cognitive Mode | Output Key |
|-------|----------------|----------------|------------|
| nse-requirements | Process 1 (Stakeholder Expectations), Process 2 (Technical Requirements) | Convergent | `requirements_output` |
| nse-risk | Process 16 (Risk Management) | Convergent | `risk_output` |
| nse-architecture | Process 3 (Logical Decomposition), Process 4 (Design Solution) | Convergent | `architecture_output` |
| nse-reviewer | Process 17 (Technical Assessment) | Convergent | `reviewer_output` |
| nse-verification | Process 8 (Verification), Process 9 (Validation) | Convergent | `verification_output` |
| nse-integration | Process 6 (Product Integration), Process 12 (Interface Management) | Convergent | `integration_output` |
| nse-configuration | Process 14 (Configuration Management), Process 15 (Technical Data Management) | Convergent | `configuration_output` |
| nse-reporter | Aggregator (all processes) | Convergent | `status_report` |

**Strengths:**
- Explicit cognitive_mode metadata in all agent definitions
- State management with clear input/output keys for chaining
- NASA process traceability embedded in persona descriptions
- Mandatory disclaimers for regulatory compliance
- Comprehensive templates for deliverables (ICD, N² diagrams, risk registers)

**Critical Gap - Cognitive Mode Homogeneity:**
All 8 nse-* agents are marked as `cognitive_mode: "convergent"`. Per persona theory research (agent-research-003), this is a significant design flaw:

> "NASA SE is not monolithically convergent. Early lifecycle activities (concept exploration, alternative analysis) benefit from divergent thinking, while later activities (verification, configuration control) require convergent discipline."

**Recommended Cognitive Mode Distribution:**

| Agent | Current | Recommended | Rationale |
|-------|---------|-------------|-----------|
| nse-requirements | Convergent | **Divergent → Convergent** | Stakeholder elicitation requires exploration |
| nse-architecture | Convergent | **Divergent → Convergent** | Trade studies require alternative generation |
| nse-risk | Convergent | **Divergent** (identification) **→ Convergent** (mitigation) | Risk identification is exploratory |
| nse-reviewer | Convergent | Convergent | Correct - assessment is evaluative |
| nse-verification | Convergent | Convergent | Correct - test execution is procedural |
| nse-integration | Convergent | Convergent | Correct - integration follows defined interfaces |
| nse-configuration | Convergent | Convergent | Correct - CM is control-oriented |
| nse-reporter | Convergent | Convergent | Correct - synthesis from defined inputs |

### 3. Orchestrator/Specialist Analysis

The `.claude/agents/` directory contains hierarchical agents:

**orchestrator.md:**
- Persona: "Distinguished Systems Architect" - detailed, domain-specific (good practice)
- Decision Framework with Scope/Expertise/Risk/Clarity evaluation
- Explicit delegation criteria to specialists
- Synthesis responsibility after specialist work completes

**qa-engineer.md:**
- Persona: "Meticulous QA Engineer" - specific behavioral traits
- Clear test category focus (Unit, Integration, E2E)
- Handoff triggers defined

**security-auditor.md:**
- Persona: "Paranoid by design" - memorable, distinct characterization
- OWASP Top 10 checklist embedded
- Severity rating scheme standardized

**Alignment with Persona Theory:**
These agents follow best practices from research:
1. Detailed, domain-specific personas (not generic "helpful assistant")
2. Clear role boundaries prevent overlap
3. Hierarchical structure with defined delegation
4. Generator-Critic pattern implicit (Orchestrator generates tasks, Specialists critique/validate)

### 4. Persona Theory Alignment Assessment

Based on agent-research-003-persona-theory.md findings:

| Principle | Current Alignment | Evidence |
|-----------|-------------------|----------|
| Detailed personas > generic labels | **HIGH** | All agents have specific domain expertise, behavioral traits |
| Cognitive mode scaffolding | **LOW** | nse-* all convergent; ps-* modes implicit |
| Two-phase prompting | **PARTIAL** | Pipeline structure supports phases but not explicit mode transitions |
| Multi-agent specialist roles | **HIGH** | Clear specialization across all agent families |
| Persona consistency | **HIGH** | Personas maintained throughout agent definitions |

**Key Research Finding (Anthropic):**
> "Adding personas in system prompts does not improve model performance across a range of questions compared to the control setting."

**Implication:** Personas are most effective for:
- Open-ended, creative tasks (divergent phases)
- Role-play and perspective-taking
- Style/tone consistency

Less effective for:
- Factual accuracy tasks
- Structured output generation
- Verification/validation tasks

This suggests our convergent agents (verification, configuration, reviewer) may not benefit significantly from elaborate personas, while divergent agents (research, architecture exploration, risk identification) benefit most.

### 5. Role Differentiation Assessment

**ps-* Family:**
- Low overlap risk - pipeline structure enforces sequential handoff
- Clear boundaries: research → analysis → architecture → synthesis → validation
- No circular dependencies detected

**nse-* Family:**
- Low overlap risk - NASA process mapping creates clear lanes
- Potential overlap: nse-reviewer vs nse-verification (both assess quality)
  - Differentiation: nse-reviewer = technical assessment (Process 17)
  - nse-verification = test execution (Processes 8, 9)
- nse-reporter aggregates without overlap (type: aggregator)

**Cross-Family:**
- ps-reviewer and nse-reviewer have similar functions but different domains
- No explicit handoff protocol between ps-* and nse-* pipelines
- Gap: Need cross-pollination interface definition

### 6. Orchestration Pattern Analysis

Based on agent-research-004-persona-compatibility.md:

**Current State:**
- Implicit orchestration through pipeline conventions
- No explicit orchestrator agent for ps-* or nse-* families
- `.claude/agents/orchestrator.md` exists but scope is general (delegates to QA, Security)

**Recommended Patterns:**

1. **Hierarchical Orchestration** (Currently Partial)
   - Orchestrator → Specialist delegation exists for QA/Security
   - Missing: ps-orchestrator, nse-orchestrator

2. **Generator-Critic Loop** (Not Implemented)
   - Could pair: ps-architect (generate) ↔ ps-reviewer (critique)
   - Could pair: nse-architecture (generate) ↔ nse-reviewer (critique)

3. **Researcher-Analyst-Writer Pipeline** (Implemented)
   - ps-researcher → ps-analyst → ps-reporter follows this pattern
   - nse-* agents follow similar flow to nse-reporter

**Research Finding:**
> "Hierarchical structures improve efficiency (10% faster with orchestrator)"

**Recommendation:** Add explicit orchestrator agents for each pipeline family.

### 7. Belbin Team Role Coverage

Mapping current agents to Belbin roles (from agent-research-004):

| Belbin Role | AI Analog | ps-* Agent | nse-* Agent | Gap? |
|-------------|-----------|------------|-------------|------|
| Plant | Creative/Divergent | ps-architect (partial) | **NONE** | **YES** |
| Resource Investigator | Researcher | ps-researcher | **NONE** | **YES** |
| Coordinator | Orchestrator | **NONE** | **NONE** | **YES** |
| Shaper | Driver/Challenger | **NONE** | **NONE** | **YES** |
| Monitor Evaluator | Critic/Validator | ps-analyst, ps-reviewer | nse-reviewer | No |
| Teamworker | Synthesizer | ps-synthesizer | nse-reporter | No |
| Implementer | Builder | **NONE** | nse-integration, nse-configuration | Partial |
| Completer Finisher | QA/Validator | ps-validator, ps-reporter | nse-verification | No |
| Specialist | Domain Expert | ps-investigator | All nse-* (domain-specific) | No |

**Critical Gaps:**
1. **No Plant (Creative/Divergent)** in nse-* family - all convergent
2. **No Resource Investigator** in nse-* family - no exploratory research agent
3. **No Coordinator (Orchestrator)** in either family
4. **No Shaper (Driver/Challenger)** - agents that push for progress/challenge status quo

---

## L2: Strategic Implications

### Improvements Needed

#### Priority 1: Cognitive Mode Diversity (Critical)
- Add `cognitive_mode` field to all ps-* agent definitions
- Implement divergent phases for nse-requirements, nse-architecture, nse-risk
- Consider two-phase agents with mode transitions:
  ```yaml
  cognitive_phases:
    - phase: exploration
      mode: divergent
      activities: [brainstorm, alternatives, edge_cases]
    - phase: refinement
      mode: convergent
      activities: [evaluate, select, document]
  ```

#### Priority 2: Orchestration Infrastructure (High)
- Create `ps-orchestrator.md` for problem-solving pipeline
- Create `nse-orchestrator.md` for NASA SE pipeline
- Implement explicit delegation protocols
- Add state tracking for multi-agent sessions

#### Priority 3: Missing Personas (Medium)
- Add `nse-explorer.md` - divergent research/trade study agent (Plant + Resource Investigator)
- Add `ps-coordinator.md` - pipeline orchestration (Coordinator role)
- Consider `nse-challenger.md` - devil's advocate for design reviews (Shaper role)

#### Priority 4: Cross-Pollination Formalization (Medium)
- Define handoff protocol between ps-* and nse-* pipelines
- Standardize state schema across families
- Create explicit interface contracts

### Missing Personas Recommended

| Proposed Agent | Family | Belbin Role | Cognitive Mode | Rationale |
|----------------|--------|-------------|----------------|-----------|
| nse-explorer | nse-* | Plant + Resource Investigator | Divergent | Trade studies, concept exploration |
| nse-orchestrator | nse-* | Coordinator | Mixed | Pipeline coordination, delegation |
| ps-orchestrator | ps-* | Coordinator | Mixed | Problem-solving coordination |
| nse-challenger | nse-* | Shaper | Divergent | Design critique, assumption challenges |

### Orchestration Recommendations

1. **Adopt Hierarchical Orchestration**
   - One orchestrator per pipeline family
   - Clear delegation criteria (complexity, domain, risk)
   - Synthesis responsibility at orchestrator level

2. **Implement Generator-Critic Loops**
   - nse-architecture ↔ nse-reviewer (iterative design refinement)
   - nse-requirements ↔ nse-verification (requirements validation cycle)
   - ps-architect ↔ ps-reviewer (design critique loop)

3. **Formalize State Management**
   - Standardize state schema across all agents
   - Implement checkpointing for long-running sessions
   - Define rollback/recovery protocols

4. **Add Pipeline Coordination Points**
   - Define explicit phase gates (research → analysis → design → verification)
   - Create handoff checklists between agents
   - Implement quality gates before cross-family transitions

---

## Research Questions - Answers

### Q1: Are our agent personas well-defined according to persona theory research?

**Answer: MOSTLY YES, with caveats.**

Strengths:
- Detailed, domain-specific personas (not generic)
- Clear behavioral traits and expertise areas
- Consistent persona maintenance throughout definitions

Weaknesses:
- Cognitive mode scaffolding incomplete
- Two-phase (divergent→convergent) prompting not implemented
- Some personas may be over-elaborate for convergent tasks where they add minimal value

### Q2: What cognitive modes (divergent/convergent) should each agent have?

**Answer: See detailed table in L1 Section 2.**

Key recommendations:
- nse-requirements, nse-architecture, nse-risk should support divergent phases
- nse-verification, nse-configuration, nse-integration are correctly convergent
- ps-researcher, ps-architect should be explicitly divergent
- ps-validator, ps-reviewer should be explicitly convergent

### Q3: Are agent roles overlapping or are they properly differentiated?

**Answer: PROPERLY DIFFERENTIATED with minor concerns.**

- NASA process mapping creates clear boundaries for nse-* agents
- Pipeline structure prevents overlap in ps-* agents
- Minor concern: nse-reviewer vs nse-verification distinction could be clearer
- No circular validation anti-pattern detected

### Q4: What orchestration patterns should we adopt?

**Answer: Hierarchical Orchestration + Generator-Critic Loops.**

1. Add orchestrator agents for each pipeline family
2. Implement iterative refinement loops (architect ↔ reviewer)
3. Define explicit delegation criteria
4. Formalize state management for multi-agent sessions

### Q5: Are our agents following the Belbin team role model?

**Answer: PARTIALLY - significant gaps exist.**

Covered: Monitor Evaluator, Teamworker, Completer Finisher, Specialist
Missing: Plant (critical), Coordinator (critical), Resource Investigator, Shaper

---

## Cross-Pollination Metadata

### Target Pipeline: nse-* (NASA Systems Engineering)

### Handoff Artifacts for nse-requirements

| Artifact | Description | Priority |
|----------|-------------|----------|
| Cognitive mode requirements | Need divergent phase for stakeholder elicitation | High |
| State schema standardization | Input/output key conventions | Medium |
| Two-phase prompting template | Exploration → refinement pattern | High |

### Handoff Artifacts for nse-risk

| Artifact | Description | Priority |
|----------|-------------|----------|
| Divergent risk identification | Brainstorming phase for risk discovery | High |
| Belbin Plant integration | Creative exploration of edge cases | Medium |
| Generator-Critic loop design | Risk identification ↔ mitigation critique | Medium |

### Suggested Cross-Pollination Routes

1. **ps-researcher → nse-explorer (proposed)**
   - Research methodologies transfer
   - Web search and document analysis patterns
   - Divergent exploration techniques

2. **ps-orchestrator (proposed) → nse-orchestrator (proposed)**
   - Delegation framework sharing
   - State management patterns
   - Quality gate definitions

3. **ps-reviewer → nse-reviewer**
   - Critique patterns standardization
   - Checklist harmonization
   - Feedback loop optimization

---

## Gaps for Formalization

The following gaps should become formal requirements in the nse-* pipeline:

### REQ-001: Cognitive Mode Metadata
**Description:** All agent definitions MUST include explicit `cognitive_mode` field with value from {divergent, convergent, mixed}.
**Rationale:** Enables proper phase transitions and persona optimization.
**Priority:** High

### REQ-002: Two-Phase Agent Template
**Description:** Agents requiring both divergent and convergent thinking MUST implement `cognitive_phases` structure with explicit mode transitions.
**Rationale:** Supports exploration→refinement pattern per persona theory.
**Priority:** High

### REQ-003: Pipeline Orchestrator Agents
**Description:** Each agent pipeline family MUST have a dedicated orchestrator agent with delegation authority.
**Rationale:** Hierarchical orchestration improves efficiency by 10% per research.
**Priority:** High

### REQ-004: Divergent Explorer Agent
**Description:** nse-* pipeline MUST include at least one divergent-mode agent for trade studies and concept exploration.
**Rationale:** All current nse-* agents are convergent, missing Plant/Resource Investigator roles.
**Priority:** Critical

### REQ-005: Cross-Pipeline Handoff Protocol
**Description:** Formal interface contracts MUST be defined for handoffs between ps-* and nse-* pipelines.
**Rationale:** Currently no explicit protocol exists.
**Priority:** Medium

### REQ-006: Generator-Critic Loop Implementation
**Description:** Design agents (architecture) MUST be paired with critique agents (reviewer) in iterative refinement loops.
**Rationale:** Generator-Critic pattern produces higher quality outputs per research.
**Priority:** Medium

### REQ-007: State Schema Standardization
**Description:** All agents MUST use consistent state schema with defined input/output keys.
**Rationale:** Enables reliable agent chaining and session recovery.
**Priority:** Medium

---

## References

1. agent-research-003-persona-theory.md - Persona Theory and Cognitive Mode Research
2. agent-research-004-persona-compatibility.md - Multi-Agent Compatibility Patterns
3. Anthropic Research: Persona Vectors and Constitutional AI
4. Belbin Team Roles Model (adapted for AI agents)
5. NASA NPR 7123.1D - Systems Engineering Processes and Requirements

---

## Document Metadata

- **Created:** 2026-01-09
- **Author:** ps-researcher (Agent ID: ps-r-002)
- **Version:** 1.0
- **Status:** Complete
- **Next Action:** Handoff to nse-requirements for REQ-001 through REQ-007 implementation
