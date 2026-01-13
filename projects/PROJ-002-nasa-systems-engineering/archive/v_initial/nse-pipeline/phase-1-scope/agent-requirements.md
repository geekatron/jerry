# Agent Formal Requirements Analysis

> **Document ID:** NSE-REQ-AGT-001
> **Agent ID:** nse-r-002 (nse-requirements)
> **Project:** PROJ-002-nasa-systems-engineering
> **Phase:** 1 - Scope (nse-* Pipeline)
> **Date:** 2026-01-09
> **NPR 7123.1D Process:** 4.2 Stakeholder Expectations Definition, 4.3 Technical Requirements Definition

---

## L0: Executive Summary

This document presents formal "shall" requirements for the Jerry Framework Agent System based on analysis of 20 agent definitions across three agent families (ps-*, nse-*, .claude/agents/*), two template specifications, and two research documents on persona theory and multi-agent compatibility.

### Key Findings

1. **Template Divergence**: The ps-* and nse-* agent families share ~70% structural similarity but lack formal inheritance or verification mechanisms
2. **Persona Inconsistency Risk**: Research indicates personas work best for "open-ended tasks requiring creativity or domain-specific knowledge" but consistency enforcement is absent
3. **Orchestration Gap**: No formal contract defines how agents chain state, handoff artifacts, or validate predecessor outputs
4. **Constitutional Compliance**: 43 principles (P-001 through P-043) are referenced but no automated verification exists
5. **Cognitive Mode Specification**: Two modes (convergent/divergent) are defined but selection criteria are implicit

### Requirements Summary

| Category | Total Requirements | Critical | High | Medium |
|----------|-------------------|----------|------|--------|
| Agent Definition | 18 | 5 | 8 | 5 |
| Orchestration | 12 | 4 | 5 | 3 |
| Persona | 8 | 2 | 4 | 2 |
| **Total** | **38** | **11** | **17** | **10** |

---

## L1: Technical Requirements

### 1. Agent Definition Requirements

These requirements govern the structural and behavioral specification of individual agents.

#### 1.1 Frontmatter Structure Requirements

| REQ ID | Requirement Statement | Priority | Rationale | Verification Method |
|--------|----------------------|----------|-----------|-------------------|
| REQ-AGT-001 | Each agent definition file SHALL include a YAML frontmatter section delimited by `---` markers | Critical | Enables machine parsing and validation of agent metadata | Automated schema validation |
| REQ-AGT-002 | The frontmatter SHALL include fields: `agent_id`, `version`, `status`, `family`, `cognitive_mode` | Critical | Minimum viable identification for orchestration | Schema validation |
| REQ-AGT-003 | The `agent_id` field SHALL follow pattern `{family}-{role}` (e.g., `ps-analyst`, `nse-requirements`) | High | Enables deterministic agent resolution and routing | Regex validation |
| REQ-AGT-004 | The `version` field SHALL follow semantic versioning (MAJOR.MINOR.PATCH) | Medium | Enables compatibility tracking across agent updates | Semver parsing |
| REQ-AGT-005 | The `status` field SHALL be one of: `draft`, `active`, `deprecated`, `archived` | High | Prevents invocation of non-production agents | Enum validation |

#### 1.2 Identity Section Requirements

| REQ ID | Requirement Statement | Priority | Rationale | Verification Method |
|--------|----------------------|----------|-----------|-------------------|
| REQ-AGT-006 | Each agent SHALL define an Identity section with `role`, `expertise`, and `primary_function` | Critical | Establishes agent purpose and capability boundaries | Section presence check |
| REQ-AGT-007 | The `role` field SHALL be a noun phrase describing the agent's professional role (e.g., "Requirements Analyst") | High | Enables persona consistency per research findings | NLP role extraction |
| REQ-AGT-008 | The `expertise` field SHALL list 3-7 domain competencies as a YAML array | High | Bounds agent's advisory scope | Array length validation |
| REQ-AGT-009 | The `primary_function` field SHALL begin with an action verb | Medium | Ensures clear actionable purpose | Verb detection |

#### 1.3 Capability and Tool Requirements

| REQ ID | Requirement Statement | Priority | Rationale | Verification Method |
|--------|----------------------|----------|-----------|-------------------|
| REQ-AGT-010 | Each agent SHALL explicitly enumerate `allowed_tools` as a YAML array | Critical | Prevents capability creep and unauthorized operations | Tool registry validation |
| REQ-AGT-011 | Each agent SHALL explicitly enumerate `forbidden_actions` as a YAML array | Critical | Enforces negative guardrails | Static analysis |
| REQ-AGT-012 | Tools listed in `allowed_tools` SHALL exist in the Jerry tool registry | High | Prevents runtime resolution failures | Registry lookup |
| REQ-AGT-013 | The `forbidden_actions` list SHALL include at minimum: actions violating constitutional principles | High | Links guardrails to constitution | Principle mapping |

#### 1.4 Output Specification Requirements

| REQ ID | Requirement Statement | Priority | Rationale | Verification Method |
|--------|----------------------|----------|-----------|-------------------|
| REQ-AGT-014 | Each agent SHALL specify supported output levels (L0, L1, L2) | High | Enables audience-appropriate communication | Level presence check |
| REQ-AGT-015 | L0 output level SHALL target "executive/non-technical" audience with ELI5 language | Medium | Per research: "audience adaptation improves perceived quality" | Readability scoring |
| REQ-AGT-016 | L1 output level SHALL target "software engineer" audience with technical precision | Medium | Primary operator audience | Technical term density |
| REQ-AGT-017 | L2 output level SHALL target "principal architect/strategist" with systems thinking | Medium | Strategic decision support | Abstraction level analysis |
| REQ-AGT-018 | Each agent SHALL define a `default_output_format` for file persistence | High | Enables consistent artifact generation | Format validation |

---

### 2. Orchestration Requirements

These requirements govern multi-agent coordination, state management, and workflow execution.

#### 2.1 State Management Requirements

| REQ ID | Requirement Statement | Priority | Rationale | Verification Method |
|--------|----------------------|----------|-----------|-------------------|
| REQ-AGT-ORCH-001 | Each agent invocation SHALL receive a `session_context` object from the orchestrator | Critical | Enables stateful multi-agent workflows | Context presence assertion |
| REQ-AGT-ORCH-002 | The `session_context` SHALL include: `session_id`, `predecessor_agent`, `handoff_artifacts`, `accumulated_state` | Critical | Per research: "state loss across agent boundaries causes coherence degradation" | Schema validation |
| REQ-AGT-ORCH-003 | Agents SHALL persist significant outputs to the filesystem before returning control | High | Per P-002: "Significant outputs SHALL be persisted to filesystem" | File creation verification |
| REQ-AGT-ORCH-004 | Each agent SHALL return a `handoff_manifest` listing artifacts produced for successor agents | High | Enables traceable information flow | Manifest structure check |

#### 2.2 Agent Chaining Requirements

| REQ ID | Requirement Statement | Priority | Rationale | Verification Method |
|--------|----------------------|----------|-----------|-------------------|
| REQ-AGT-ORCH-005 | The orchestrator SHALL enforce maximum ONE level of agent nesting (orchestrator -> worker) | Critical | Per P-003 (Hard principle): "Maximum ONE level of agent nesting" | Call depth tracking |
| REQ-AGT-ORCH-006 | Worker agents SHALL NOT spawn sub-agents or invoke the Task tool | Critical | Prevents recursive agent loops | Static analysis of agent files |
| REQ-AGT-ORCH-007 | Agent chains SHALL be defined declaratively in workflow specifications | High | Enables auditability and optimization | Workflow schema validation |
| REQ-AGT-ORCH-008 | Each workflow step SHALL specify `preconditions` and `postconditions` | High | Enables formal verification of workflow correctness | Condition specification check |

#### 2.3 Coordination Pattern Requirements

| REQ ID | Requirement Statement | Priority | Rationale | Verification Method |
|--------|----------------------|----------|-----------|-------------------|
| REQ-AGT-ORCH-009 | Multi-agent workflows SHALL implement either Sequential, Generator-Critic, or Hierarchical patterns | High | Per research: "these patterns show 15-40% quality improvement" | Pattern classification |
| REQ-AGT-ORCH-010 | Generator-Critic patterns SHALL pair cognitively diverse agents (divergent + convergent) | High | Per research: "Generator-Critic patterns improve quality by 15-25%" | Cognitive mode analysis |
| REQ-AGT-ORCH-011 | Parallel agent invocations SHALL be independent with no shared mutable state | Medium | Prevents race conditions and non-determinism | Dependency analysis |
| REQ-AGT-ORCH-012 | Orchestration failures SHALL trigger graceful degradation, not cascading failures | Medium | Per research: "anti-patterns cause cascading failures" | Error handling review |

---

### 3. Persona Requirements

These requirements govern agent persona consistency, cognitive mode specification, and team composition.

#### 3.1 Persona Consistency Requirements

| REQ ID | Requirement Statement | Priority | Rationale | Verification Method |
|--------|----------------------|----------|-----------|-------------------|
| REQ-AGT-PER-001 | Each agent SHALL define a Persona section with `tone`, `communication_style`, and `audience_adaptation` | Critical | Per research: "detailed domain-specific personas outperform generic roles" | Section presence check |
| REQ-AGT-PER-002 | Persona attributes SHALL remain stable throughout a single agent invocation | Critical | Per research: "persona consistency is a significant challenge" | Output consistency scoring |
| REQ-AGT-PER-003 | The `tone` field SHALL be one of: `formal`, `professional`, `conversational`, `technical` | High | Enables predictable communication style | Enum validation |
| REQ-AGT-PER-004 | The `communication_style` field SHALL specify verbosity and structure preferences | High | Enables output format predictability | Style attribute validation |

#### 3.2 Cognitive Mode Requirements

| REQ ID | Requirement Statement | Priority | Rationale | Verification Method |
|--------|----------------------|----------|-----------|-------------------|
| REQ-AGT-PER-005 | Each agent SHALL specify a `cognitive_mode` of either `convergent` or `divergent` | High | Per research: "cognitive modes can be scaffolded through prompting" | Mode presence check |
| REQ-AGT-PER-006 | Convergent agents SHALL prioritize analysis, synthesis, and decision support | Medium | Enables appropriate task routing | Task-mode alignment |
| REQ-AGT-PER-007 | Divergent agents SHALL prioritize exploration, ideation, and alternative generation | Medium | Enables creative task support | Task-mode alignment |

#### 3.3 Team Composition Requirements

| REQ ID | Requirement Statement | Priority | Rationale | Verification Method |
|--------|----------------------|----------|-----------|-------------------|
| REQ-AGT-PER-008 | Multi-agent teams SHALL include complementary Belbin-style roles, not overlapping roles | High | Per research: "complementary roles outperform overlapping" | Role diversity analysis |

---

## Gap Analysis

The following gaps were identified between current agent implementations and formal requirements:

| GAP ID | Gap Description | Affected Agents | Severity | Recommended Action |
|--------|-----------------|-----------------|----------|-------------------|
| GAP-AGT-001 | No schema validation exists for agent YAML frontmatter | All 20 agents | High | Implement JSON Schema for agent files |
| GAP-AGT-002 | Agent status field missing from most ps-* agents | ps-analyst, ps-architect, ps-investigator, ps-reporter, ps-researcher, ps-reviewer, ps-synthesizer, ps-validator | Medium | Add `status: active` to all production agents |
| GAP-AGT-003 | No formal session_context contract defined | All agents | Critical | Define TypeScript/Python interface for session_context |
| GAP-AGT-004 | Handoff_manifest not implemented in current agent outputs | All agents | High | Add handoff_manifest generation to agent templates |
| GAP-AGT-005 | Constitutional principle mapping incomplete | nse-* agents reference P-001 to P-043, ps-* agents reference subset | Medium | Audit all agents for complete principle coverage |
| GAP-AGT-006 | Output level (L0/L1/L2) selection criteria not formalized | All agents | Medium | Define selector algorithm based on user role/context |
| GAP-AGT-007 | No automated persona consistency verification | All agents | High | Implement persona drift detection in orchestrator |
| GAP-AGT-008 | Cognitive mode task routing implicit | Orchestrator | Medium | Formalize task-to-mode mapping rules |
| GAP-AGT-009 | Tool registry not centralized | All agents | High | Create `tools/REGISTRY.md` with canonical tool list |
| GAP-AGT-010 | Version field absent from all agent files | All 20 agents | Medium | Add `version: 1.0.0` to all agents |
| GAP-AGT-011 | No workflow specification format defined | Orchestration layer | High | Define YAML workflow DSL |
| GAP-AGT-012 | Anti-pattern detection not implemented | Orchestrator | Medium | Add runtime checks for groupthink, authority bias, skill mismatch |

---

## L2: Strategic Implications

### Architectural Recommendations

1. **Agent Schema Registry**: Implement a centralized schema registry for agent definitions, enabling:
   - Compile-time validation of agent files
   - Version compatibility checking
   - Deprecation warnings

2. **Session Context Contract**: Define a formal TypeScript/Python interface for `session_context`:
   ```typescript
   interface SessionContext {
     session_id: string;
     predecessor_agent: string | null;
     handoff_artifacts: Artifact[];
     accumulated_state: Map<string, unknown>;
     constitutional_compliance: PrincipleCheckResult[];
   }
   ```

3. **Persona Verification Layer**: Implement runtime persona consistency checking:
   - Monitor output style across invocation
   - Flag persona drift for orchestrator review
   - Enable persona "lock" for critical workflows

4. **Workflow Definition Language**: Create a declarative workflow DSL:
   ```yaml
   workflow: requirements-to-implementation
   steps:
     - agent: nse-requirements
       postconditions: [requirements_doc_exists]
     - agent: nse-architecture
       preconditions: [requirements_doc_exists]
       pattern: generator-critic
       critic: nse-reviewer
   ```

### Research Gaps for ps-* Pipeline

The following research gaps should be explored by the ps-* pipeline:

1. **Persona Drift Quantification**: What metrics effectively measure persona consistency over long sessions?
2. **Cognitive Mode Switching**: Can an agent switch cognitive modes mid-session, and what are the costs?
3. **Belbin Role Mapping**: How do the 8 ps-* agents map to Belbin team roles, and are there gaps?
4. **Generator-Critic Optimal Pairing**: Which ps-* agent pairs show highest synergy in Generator-Critic patterns?
5. **Constitutional Enforcement Automation**: Can P-001 through P-043 be automatically verified at runtime?

### Cross-Family Integration

The ps-* and nse-* agent families share significant structural overlap:

| Component | ps-* Implementation | nse-* Implementation | Integration Opportunity |
|-----------|---------------------|---------------------|------------------------|
| Frontmatter | YAML with 6 fields | YAML with 8 fields | Unify to superset |
| Identity | role, expertise, cognitive_mode | Same + NASA process ref | Add NASA refs to ps-* |
| Persona | tone, style | tone, style, formality | Add formality to ps-* |
| Capabilities | allowed_tools, forbidden | Same | Shared tool registry |
| Output Levels | L0/L1/L2 | L0/L1/L2 | Already aligned |

---

## Cross-Pollination Metadata

| Field | Value |
|-------|-------|
| **Source Agent** | nse-requirements (nse-r-002) |
| **Target Audience** | ps-* pipeline, orchestrator development, agent governance |
| **Key Handoff Items** | 38 formal requirements (REQ-AGT-*), 12 gaps (GAP-AGT-*), session_context interface proposal |
| **Research Gaps for ps-*** | Persona drift metrics, cognitive mode switching costs, Belbin role mapping, Generator-Critic optimal pairs, constitutional enforcement automation |
| **Downstream Consumers** | nse-architecture (architecture trade study), nse-verification (test case generation), ps-researcher (gap exploration) |

---

## Traceability Matrix

| Requirement | Source Document | Constitutional Principle | Verification Status |
|-------------|-----------------|-------------------------|-------------------|
| REQ-AGT-001 | PS_AGENT_TEMPLATE.md, NSE_AGENT_TEMPLATE.md | P-002 | Not Verified |
| REQ-AGT-006 | agent-research-003-persona-theory.md | P-001 | Not Verified |
| REQ-AGT-010 | .claude/agents/TEMPLATE.md | P-003 | Not Verified |
| REQ-AGT-ORCH-005 | JERRY_CONSTITUTION.md (P-003) | P-003 (Hard) | Not Verified |
| REQ-AGT-PER-001 | agent-research-003-persona-theory.md | P-001, P-022 | Not Verified |
| REQ-AGT-PER-008 | agent-research-004-persona-compatibility.md | P-001 | Not Verified |

---

## Appendix A: Agent Inventory

| Agent ID | Family | Cognitive Mode | Status | Version |
|----------|--------|---------------|--------|---------|
| ps-analyst | problem-solving | convergent | active | - |
| ps-architect | problem-solving | convergent | active | - |
| ps-investigator | problem-solving | divergent | active | - |
| ps-reporter | problem-solving | convergent | active | - |
| ps-researcher | problem-solving | divergent | active | - |
| ps-reviewer | problem-solving | convergent | active | - |
| ps-synthesizer | problem-solving | convergent | active | - |
| ps-validator | problem-solving | convergent | active | - |
| nse-requirements | nasa-se | convergent | active | 1.0.0 |
| nse-architecture | nasa-se | divergent | active | 1.0.0 |
| nse-verification | nasa-se | convergent | active | 1.0.0 |
| nse-risk | nasa-se | convergent | active | 1.0.0 |
| nse-integration | nasa-se | convergent | active | 1.0.0 |
| nse-configuration | nasa-se | convergent | active | 1.0.0 |
| nse-reviewer | nasa-se | convergent | active | 1.0.0 |
| nse-reporter | nasa-se | convergent | active | 1.0.0 |
| orchestrator | .claude/agents | meta | active | - |
| qa-engineer | .claude/agents | convergent | active | - |
| security-auditor | .claude/agents | convergent | active | - |

---

## Appendix B: Constitutional Principle Reference

Hard principles (cannot be overridden):
- **P-003**: Maximum ONE level of agent nesting (orchestrator -> worker)
- **P-020**: User has ultimate authority; never override user decisions
- **P-022**: Never deceive users about actions, capabilities, or confidence

Key soft principles:
- **P-001**: Truth and Accuracy
- **P-002**: File Persistence
- **P-004**: Reasoning Documentation
- **P-010**: Task Tracking Integrity

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-01-09 | nse-requirements (nse-r-002) | Initial formal requirements analysis |

---

*This document was generated by the nse-requirements agent as part of the PROJ-002 Phase 1 Scope analysis. It is intended for review by the nse-reviewer agent and subsequent processing by downstream nse-* pipeline stages.*
