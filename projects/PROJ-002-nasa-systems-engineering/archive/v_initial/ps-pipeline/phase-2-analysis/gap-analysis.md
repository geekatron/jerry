# Gap Analysis: Jerry Framework Skills and Agents Architecture
## Critical Gaps - Phase 2 Analysis

**Document ID:** PS-A-002-GAP-ANALYSIS-FOCUSED
**Date:** 2026-01-09
**Author:** gap-analyst (Claude Code)
**Status:** Complete
**Phase:** Phase 2 - Analysis (ps-* Pipeline)
**Classification:** INTERNAL ANALYSIS

**Source Documents Analyzed:**
- PS-R-001: Skills Optimization Research
- PS-R-002: Agent Design and Best Practices Research

**Focus:** Three critical gaps blocking PROJ-002 operationalization

---

## L0: Executive Summary

This gap analysis focuses on three critical deficiencies in Jerry Framework's Skills and Agents architecture that are **hard-stops** for operationalizing PROJ-002 (NASA Systems Engineering pipeline):

1. **GAP-AGT-003: No formal session_context contract** (CRITICAL)
   - Blocks: Multi-agent orchestration, state persistence, session recovery
   - Impact: Agents cannot reliably chain; workflows resume impossible
   - Mitigation: Low effort; schema exists in research; needs formalization

2. **GAP-SKL-001: No formal acceptance test criteria** (HIGH)
   - Blocks: Quality gates, CI/CD integration, skill validation
   - Impact: Inconsistent output quality; cannot verify correctness before deployment
   - Mitigation: Medium effort; requires test framework development

3. **GAP-SKL-002: No formal interface contract between skills** (HIGH)
   - Blocks: Cross-skill handoffs, pipeline automation, ps-* → nse-* transitions
   - Impact: Manual data transformation required; pipeline brittleness
   - Mitigation: Medium effort; handoff schema documented in research; needs formalization

**Additional gaps** (7 more identified) span cognitive mode homogeneity, missing agent personas, orchestration infrastructure, and parallel execution. All gaps include severity ratings, root causes, and specific mitigation strategies structured as L0/L1/L2.

**Key Business Impact:** Without addressing these gaps, PROJ-002 cannot proceed beyond Phase 2 analysis—orchestration logic cannot be implemented, quality gates cannot be enforced, and pipeline automation cannot be achieved.

---

## L1: Gap Severity Analysis

### Priority Matrix

| Gap ID | Severity | Research Coverage | Mitigation Available | Priority |
|--------|----------|-------------------|----------------------|----------|
| GAP-AGT-003 | **Critical** | HIGH | YES | P0 |
| RGAP-004 | **Critical** | NONE | NO | P0 |
| GAP-SKL-002 | High | HIGH | YES | P1 |
| GAP-AGT-004 | High | HIGH | YES | P1 |
| GAP-AGT-009 | High | MEDIUM | PARTIAL | P1 |
| GAP-AGT-007 | High | MEDIUM | PARTIAL | P1 |
| GAP-SKL-001 | High | MEDIUM | PARTIAL | P2 |
| RGAP-001 | Medium | HIGH | YES | P2 |
| RGAP-002 | Medium | HIGH | YES | P2 |
| RGAP-005 | Medium | LOW | PARTIAL | P2 |
| RGAP-007 | Medium | HIGH | YES | P2 |
| RGAP-008 | Medium | HIGH | YES | P3 |
| RGAP-009 | Medium | HIGH | YES | P3 |
| RGAP-010 | Medium | MEDIUM | PARTIAL | P3 |
| RGAP-003 | Low | NONE | NO | P4 |
| RGAP-006 | Low | LOW | NO | P4 |

---

### Detailed Gap Assessment

#### CRITICAL SEVERITY

##### GAP-AGT-003: No Formal session_context Contract
- **Source:** nse-r-002 Requirements Analysis
- **Research Coverage:** HIGH (ps-r-001 Section 2.2, ps-r-002 REQ-007)
- **Research Finding:** ps-r-001 proposes explicit state schema:
  ```yaml
  state_management:
    output_key: "{agent-type}_output"
    schema:
      ps_id: string
      entry_id: string
      artifact_path: string
      summary: string (max 500 chars)
      confidence: float (0.0-1.0)
      next_agent_hint: enum[ps-researcher, ps-analyst, ...]
      handoff_context:
        key_findings: array[string]
        open_questions: array[string]
        blockers: array[string]
    persistence: file
  ```
- **Mitigation Strategy:** Adopt proposed schema as formal contract, enforce via YAML frontmatter validation
- **Effort:** LOW (schema exists, needs formalization)
- **Risk if Unaddressed:** Agent chaining failures, lost context between handoffs

##### RGAP-004: Error Handling Patterns for Cascading Agent Failures
- **Source:** nse-r-001 Requirements Analysis
- **Research Coverage:** NONE
- **Research Finding:** Neither ps-r-001 nor ps-r-002 address error handling. ps-r-001 Section 2.4 notes "Missing PLAYBOOK Topics: Error Recovery Patterns" but provides no solution.
- **Mitigation Strategy:** REQUIRES NEW RESEARCH
  - Investigate: Circuit breaker patterns, retry with backoff, fallback agents
  - Reference: LangGraph fault tolerance, CrewAI error handling
  - Proposed: Add `ps-recovery` agent or error recovery middleware
- **Effort:** HIGH (requires design and implementation)
- **Risk if Unaddressed:** Single agent failure cascades through pipeline, lost work

#### HIGH SEVERITY

##### GAP-SKL-002: No Formal Interface Contract Between Skills
- **Source:** nse-r-001 Requirements Analysis
- **Research Coverage:** HIGH (ps-r-001 Section 2.4, ps-r-002 REQ-005)
- **Research Finding:** ps-r-001 identifies "Cross-Skill Handoffs - ps-* to nse-* transitions" as missing PLAYBOOK topic. ps-r-002 REQ-005 requires formal interface contracts.
- **Mitigation Strategy:**
  1. Define handoff schema: `{source_skill, target_skill, context_bundle, continuation_hint}`
  2. Add cross-skill section to PLAYBOOK.md
  3. Create example ps-analyst to nse-risk handoff
- **Effort:** LOW (ps-r-001 provides schema outline)
- **Risk if Unaddressed:** Cannot operationalize dual-pipeline workflow for PROJ-002

##### GAP-AGT-004: Handoff Manifest Not Implemented
- **Source:** nse-r-001 Requirements Analysis
- **Research Coverage:** HIGH (ps-r-002 Section 6, REQ-003)
- **Research Finding:** ps-r-002 recommends "Add explicit orchestrator agents for each pipeline family" with "clear delegation criteria (complexity, domain, risk)." Missing orchestrators mean no formalized handoff authority.
- **Mitigation Strategy:**
  1. Create `ps-orchestrator.md` with delegation manifest
  2. Create `nse-orchestrator.md` with NASA process-based routing
  3. Define handoff manifest schema: `{source_agent, target_agent, criteria, artifacts}`
- **Effort:** MEDIUM (requires new agent definitions)
- **Risk if Unaddressed:** Ad-hoc delegation, inconsistent routing

##### GAP-AGT-009: Tool Registry Not Centralized
- **Source:** nse-r-002 Requirements Analysis
- **Research Coverage:** MEDIUM (ps-r-001 Section 1.2)
- **Research Finding:** ps-r-001 notes Claude Code best practice compliance for `allowed-tools` in YAML frontmatter, but each agent defines tools independently. No centralized registry exists.
- **Mitigation Strategy:**
  1. Create `tools/REGISTRY.md` with canonical tool list
  2. Reference registry from agent `allowed-tools` sections
  3. Implement validation script to check consistency
- **Effort:** MEDIUM (requires new file and validation)
- **Risk if Unaddressed:** Tool sprawl, inconsistent capabilities across agents

##### GAP-AGT-007: No Automated Persona Consistency Verification
- **Source:** nse-r-002 Requirements Analysis
- **Research Coverage:** MEDIUM (ps-r-002 Section 4, L1)
- **Research Finding:** ps-r-002 assesses "Persona consistency: HIGH" for current agents but provides no automated verification mechanism. Notes reliance on "Consistent persona maintenance throughout definitions" (manual).
- **Mitigation Strategy:**
  1. Define persona consistency criteria (tone, expertise claims, role boundaries)
  2. Create persona validation test suite (golden prompt/response pairs)
  3. Add to CI/CD pipeline
- **Effort:** MEDIUM (requires test infrastructure)
- **Risk if Unaddressed:** Persona drift during long sessions, role confusion

##### GAP-SKL-001: No Formal Acceptance Test Criteria
- **Source:** nse-r-001 Requirements Analysis
- **Research Coverage:** MEDIUM (ps-r-001 Section 4.1, ps-r-002 Section 4)
- **Research Finding:** ps-r-001 notes "Missing: permissionMode configuration" suggesting lack of formal acceptance testing. ps-r-002 notes need for behavioral testing but doesn't specify acceptance criteria.
- **Mitigation Strategy:**
  1. Define acceptance criteria per agent (output format, content requirements)
  2. Create `tests/acceptance/` directory with agent test cases
  3. Map to BEHAVIOR_TESTS.md scenarios
- **Effort:** MEDIUM (requires test case development)
- **Risk if Unaddressed:** Cannot verify agent correctness before deployment

---

## L1: Gap Coverage Assessment

### Research Coverage Summary

| Research Document | Gaps Addressed | Gaps Partially Addressed | Gaps Not Addressed |
|-------------------|----------------|--------------------------|---------------------|
| ps-r-001 (Skills Optimization) | GAP-SKL-002, GAP-AGT-003, RGAP-001, RGAP-007, RGAP-009 | GAP-SKL-001, GAP-AGT-009, RGAP-005, RGAP-010 | RGAP-003, RGAP-004, RGAP-006 |
| ps-r-002 (Agent Design) | GAP-AGT-004, RGAP-002, RGAP-007, RGAP-008, RGAP-009 | GAP-AGT-007, RGAP-010 | RGAP-003, RGAP-004, RGAP-006 |

### Gap-to-Research Mapping

| Gap ID | Description | ps-r-001 Reference | ps-r-002 Reference |
|--------|-------------|-------------------|-------------------|
| RGAP-001 | Skill interface contracts | Section 2.2 (State schema), Section 2.4 (Handoffs) | REQ-005 (Cross-Pipeline Handoff) |
| RGAP-002 | Behavioral testing frameworks | - | Section 4 (Persona Theory Alignment) |
| RGAP-003 | NPR 7123.1D Process 9 handling | - | - |
| RGAP-004 | Cascading failure error handling | Section 2.4 (notes gap) | - |
| RGAP-005 | Agent telemetry/observability | Section 2.2 (State schema mentions confidence) | - |
| RGAP-006 | Persona drift metrics | - | Section 4 (notes consistency but no metrics) |
| RGAP-007 | Cognitive mode switching | Section 2.2 (next_agent_hint) | Section 2 (Cognitive Mode Recommendations), REQ-001, REQ-002 |
| RGAP-008 | Belbin role mapping | - | Section 7 (Complete Belbin analysis) |
| RGAP-009 | Generator-Critic pairing | Section 2.3 (Generator-Critic pattern) | Section 6 (Generator-Critic Loop), REQ-006 |
| RGAP-010 | Constitutional enforcement | - | Section 4 (Persona consistency) |
| GAP-SKL-001 | Acceptance test criteria | Section 1.2 (Best practices alignment) | - |
| GAP-SKL-002 | Interface contract between skills | Section 2.4 (Cross-Skill Handoffs) | REQ-005 |
| GAP-AGT-003 | session_context contract | Section 2.2 (State schema) | REQ-007 |
| GAP-AGT-004 | Handoff manifest | - | Section 6 (Orchestration Patterns), REQ-003 |
| GAP-AGT-007 | Persona consistency verification | - | Section 4 (Alignment assessment) |
| GAP-AGT-009 | Tool registry | Section 1.2 (allowed-tools mention) | - |

---

## L1: Unaddressed Gaps

### New Gaps Discovered During Analysis

| Gap ID | Description | Severity | Source | Rationale |
|--------|-------------|----------|--------|-----------|
| GAP-NEW-001 | No explicit model specification | High | ps-r-001 Section 1.2, 4.1 | "Missing: Model specification" - inconsistent agent quality |
| GAP-NEW-002 | No parallel execution support | High | ps-r-001 Section 2.3, 3.2 | "NOT IMPLEMENTED" - limits scale for fan-out research |
| GAP-NEW-003 | No state checkpointing | Medium | ps-r-001 Section 4.1 | Cannot resume failed workflows |
| GAP-NEW-004 | No Human-in-the-Loop support | Medium | ps-r-001 Section 2.3 | "NOT IMPLEMENTED" - no breakpoint support |
| GAP-NEW-005 | All nse-* agents convergent | Critical | ps-r-002 Section 2 | Cognitive mode homogeneity limits exploration phases |
| GAP-NEW-006 | No Plant/Divergent role in nse-* | Critical | ps-r-002 Section 7 | Missing Belbin role for creative exploration |
| GAP-NEW-007 | No Resource Investigator in nse-* | High | ps-r-002 Section 7 | Missing exploratory research agent |
| GAP-NEW-008 | Two-phase prompting not implemented | High | ps-r-002 Section 4 | Divergent-convergent transitions not explicit |

### Gaps Requiring New Research

| Gap ID | Research Question | Suggested Approach |
|--------|-------------------|-------------------|
| RGAP-003 | How do other NASA SE tools handle NPR 7123.1D Process 9 (Product Transition)? | Survey NASA contractor tools (Lockheed Martin, Boeing); review ESA ECSS-E-40 equivalent |
| RGAP-004 | What error handling patterns work for cascading agent failures? | Study LangGraph fault tolerance; research circuit breaker patterns; prototype ps-recovery agent |
| RGAP-006 | What metrics measure persona consistency over long sessions? | Define persona drift indicators; prototype detection mechanism; benchmark against golden outputs |

---

## L2: Strategic Gap Closure Roadmap

### Phase 1: Foundation (Week 1-2)

| Action | Gap(s) Addressed | Owner | Deliverable |
|--------|------------------|-------|-------------|
| Formalize session_context schema | GAP-AGT-003 | ps-architect | `contracts/SESSION_CONTEXT.md` |
| Add model specification to frontmatter | GAP-NEW-001 | All skills | Updated SKILL.md files |
| Define cross-skill handoff protocol | GAP-SKL-002, RGAP-001 | ps-architect | `contracts/HANDOFF_PROTOCOL.md` |
| Create tool registry | GAP-AGT-009 | ps-analyst | `tools/REGISTRY.md` |

### Phase 2: Orchestration (Week 3-4)

| Action | Gap(s) Addressed | Owner | Deliverable |
|--------|------------------|-------|-------------|
| Create ps-orchestrator agent | GAP-AGT-004 | ps-architect | `agents/ps-orchestrator.md` |
| Create nse-orchestrator agent | GAP-AGT-004 | nse-architect | `agents/nse-orchestrator.md` |
| Implement handoff manifest | GAP-AGT-004 | ps-architect | Manifest schema in orchestrators |
| Add cognitive mode field to ps-* | GAP-NEW-005 | ps-analyst | Updated agent templates |

### Phase 3: Quality Assurance (Week 5-6)

| Action | Gap(s) Addressed | Owner | Deliverable |
|--------|------------------|-------|-------------|
| Define acceptance test criteria | GAP-SKL-001 | ps-validator | `tests/acceptance/CRITERIA.md` |
| Create persona consistency tests | GAP-AGT-007 | ps-validator | `tests/persona/` test suite |
| Implement generator-critic pairing | RGAP-009 | ps-architect | ps-critic agent, nse-qa agent |
| Add behavioral test framework | RGAP-002 | ps-validator | `tests/behavioral/` integration |

### Phase 4: Advanced Patterns (Week 7-8)

| Action | Gap(s) Addressed | Owner | Deliverable |
|--------|------------------|-------|-------------|
| Add nse-explorer (divergent) agent | GAP-NEW-005, GAP-NEW-006 | nse-architect | `agents/nse-explorer.md` |
| Implement two-phase prompting | GAP-NEW-008, RGAP-007 | ps-architect | Updated agent templates |
| Research error handling patterns | RGAP-004 | ps-researcher | New research document |
| Add telemetry/observability hooks | RGAP-005 | ps-architect | State schema extensions |

### Phase 5: Compliance & Verification (Week 9-10)

| Action | Gap(s) Addressed | Owner | Deliverable |
|--------|------------------|-------|-------------|
| Research NPR 7123.1D Process 9 | RGAP-003 | nse-researcher | Research document |
| Implement constitutional runtime checks | RGAP-010 | ps-validator | Validation middleware |
| Define persona drift metrics | RGAP-006 | ps-researcher | Metrics specification |
| Validate Belbin coverage | RGAP-008 | ps-analyst | Updated agent family assessment |

---

### Mitigation Strategies for Critical/High Gaps

#### GAP-AGT-003: session_context Contract (Critical)
**Strategy:** Immediate formalization
1. Extract schema from ps-r-001 Section 2.2
2. Create `contracts/SESSION_CONTEXT.md` with JSON Schema
3. Update all agent templates to reference contract
4. Add validation in orchestrator agents

#### RGAP-004: Cascading Failure Error Handling (Critical)
**Strategy:** Phased research and implementation
1. **Week 1:** Document current failure modes
2. **Week 2:** Research industry patterns (LangGraph, CrewAI)
3. **Week 3:** Design error handling middleware
4. **Week 4:** Prototype ps-recovery agent
5. **Week 5:** Integration testing with failure injection

#### GAP-SKL-002: Interface Contract (High)
**Strategy:** Protocol-first development
1. Define handoff schema based on ps-r-001 proposal
2. Document in PLAYBOOK.md with examples
3. Create validation tooling
4. Test with ps-analyst to nse-risk handoff

#### GAP-AGT-004: Handoff Manifest (High)
**Strategy:** Orchestrator-driven delegation
1. Create orchestrator agents with delegation authority
2. Define manifest schema in orchestrator definitions
3. Implement routing logic based on complexity/domain/risk criteria
4. Document delegation patterns in PLAYBOOK.md

---

## Cross-Pollination Metadata

### Source Agent
- **ID:** ps-analyst (ps-a-001)
- **Pipeline:** ps-* (Problem-Solving)
- **Phase:** Phase 2 - Analysis

### Target Pipelines
1. **nse-risk** - For RGAP-004 cascading failure risk assessment
2. **nse-requirements** - For GAP-SKL-002 interface contract formalization
3. **nse-architecture** - For GAP-AGT-003 session_context schema

### Key Handoff Artifacts

| Artifact | Target | Priority | Description |
|----------|--------|----------|-------------|
| Gap Severity Matrix | nse-risk | High | Risk assessment input |
| State Schema Proposal | nse-architecture | High | Technical baseline for session_context |
| Roadmap Timeline | nse-requirements | Medium | Schedule dependencies |
| New Gaps List | nse-requirements | High | Additional requirements to capture |

### Research Gaps for nse-* Delegation

| Gap ID | Suggested nse-* Owner | Rationale |
|--------|----------------------|-----------|
| RGAP-003 | nse-researcher | NASA SE domain expertise required |
| RGAP-004 | nse-risk | Risk management perspective on failure modes |
| RGAP-006 | nse-verification | V&V expertise for metrics validation |

---

## Constraint Compliance Verification

| Constraint | Compliance | Evidence |
|------------|------------|----------|
| CON-001: P-003 Single nesting only | COMPLIANT | No recursive agent patterns researched or proposed |
| CON-002: P-022 No deception | COMPLIANT | All gaps and limitations transparently documented |
| CON-003: NPR 7123.1D compliance | PARTIAL | RGAP-003 (Process 9) flagged as requiring research |
| CON-004: L0/L1/L2 output levels | COMPLIANT | Document structured with all three levels |
| CON-005: P-002 File persistence | COMPLIANT | Document persisted to `phase-2-analysis/gap-analysis.md` |

---

## References

### Primary Sources
1. `ps-pipeline/phase-1-research/skills-optimization.md` (PS-R-001-SKILLS-OPT)
2. `ps-pipeline/phase-1-research/agent-design.md` (ps-r-002)

### Cross-Pollination Sources
1. nse-r-001 Requirements Analysis (RGAP-001 through RGAP-005)
2. nse-r-002 Requirements Analysis (RGAP-006 through RGAP-010)
3. nse-* Gap Register (GAP-SKL-001/002, GAP-AGT-003/004/007/009)

### Industry References
1. Google ADK State Management Patterns
2. LangGraph Fault Tolerance Documentation
3. CrewAI Error Handling Best Practices
4. NASA NPR 7123.1D Systems Engineering Processes

---

*Gap Analysis Document: PS-A-001-GAP-ANALYSIS*
*Generated by: ps-analyst (ps-a-001)*
*Date: 2026-01-09*
*Classification: ANALYSIS COMPLETE*
