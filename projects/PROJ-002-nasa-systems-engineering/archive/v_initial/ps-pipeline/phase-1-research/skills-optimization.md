# ps-r-001: Skills Optimization Research

**Document ID:** PS-R-001-SKILLS-OPT
**Date:** 2026-01-09
**Author:** ps-researcher (Claude Opus 4.5)
**Status:** Complete
**PS Context:**
- **Project ID:** PROJ-002
- **Entry ID:** ps-r-001
- **Topic:** Skills Architecture Optimization

---

## L0: Executive Summary

The Jerry Framework's Skills architecture (ps-* and nse-*) demonstrates **industry-leading maturity** with comprehensive XML-structured agent templates, L0/L1/L2 tiered output, and explicit constitutional compliance. Key optimization opportunities include: (1) adding missing activation keywords for edge cases, (2) implementing explicit state management schemas per Google ADK patterns, (3) adding generator-critic feedback loops, and (4) formalizing cross-skill handoff protocols. The architecture surpasses CrewAI/LangGraph defaults but could benefit from their state persistence and parallel execution patterns.

---

## L1: Technical Analysis

### 1. Current State Analysis

#### 1.1 Skills Architecture Assessment

| Component | ps-* Skill (v2.0.0) | nse-* Skill (v1.0.0) | Assessment |
|-----------|---------------------|----------------------|------------|
| YAML Frontmatter | Complete | Complete | Excellent |
| Activation Keywords | 18 keywords | 27 keywords | Good, gaps exist |
| Agent Template | XML-structured v2.0 | XML-structured v1.0 | Industry-aligned |
| Output Levels | L0/L1/L2 | L0/L1/L2 | Best practice |
| Constitutional Compliance | P-001 through P-022 | P-001 through P-042 | Comprehensive |
| State Management | Implicit (file-based) | Implicit (file-based) | Improvement needed |
| Guardrails | Input/Output validation | Input/Output + disclaimer | Strong |
| Playbook | Comprehensive | Comprehensive | Production-ready |

#### 1.2 SKILL.md Claude Code Best Practices Alignment

Based on research from `agent-research-001-claude-code-mechanics.md`:

| Best Practice | Current Implementation | Compliance |
|---------------|------------------------|------------|
| YAML frontmatter with `allowed-tools` | YES | COMPLIANT |
| `activation-keywords` array | YES | COMPLIANT |
| XML-structured agent body | YES (per PS_AGENT_TEMPLATE) | INDUSTRY-LEADING |
| Clear tool restrictions | YES (explicit forbidden actions) | COMPLIANT |
| Model specification | MISSING | GAP |
| `permissionMode` configuration | MISSING | GAP |
| Explicit persona definition | YES | COMPLIANT |
| State output_key specification | PARTIAL (documented but not enforced) | IMPROVEMENT NEEDED |

#### 1.3 Agent Template Quality Assessment

**PS_AGENT_TEMPLATE v2.0 Strengths:**
1. **Identity Section**: Role, expertise, cognitive_mode clearly defined
2. **Persona Section**: Tone, communication_style, audience_level
3. **Capabilities Section**: Allowed tools, forbidden actions
4. **Guardrails Section**: Input validation patterns, output filtering
5. **Constitutional Compliance Section**: Explicit principle mapping
6. **Output Levels Section**: L0/L1/L2 with audience guidance
7. **State Management Section**: Output keys and schema (Google ADK pattern)

**NSE_AGENT_TEMPLATE v1.0 Additions:**
1. **Mandatory Disclaimer Section**: Addresses AI hallucination risk
2. **NASA SE Methodology Section**: NPR 7123.1D process alignment
3. **Extended Constitution**: P-040 (Traceability), P-041 (V&V), P-042 (Risk)

### 2. Optimization Opportunities

#### 2.1 Missing Activation Keywords

**ps-* Skill Gaps:**
```yaml
# Currently missing keywords that should activate skill:
- "exploratory analysis"    # maps to ps-researcher
- "stakeholder analysis"    # maps to ps-analyst
- "impact assessment"       # maps to ps-analyst
- "constraint analysis"     # maps to ps-validator
- "gap analysis"            # explicit (currently implied in "analyze")
- "postmortem"              # synonym for investigation
- "retrospective"           # synonym for investigation
- "lessons learned"         # maps to ps-synthesizer
- "design review"           # explicit review type
- "threat modeling"         # security-specific analysis
```

**nse-* Skill Gaps:**
```yaml
# Currently missing keywords:
- "mission assurance"       # NASA-specific term
- "independent verification" # IV&V process
- "technical baseline"      # config management term
- "TRL"                     # Technology Readiness Level
- "heritage"                # NASA reuse concept
- "anomaly"                 # maps to nse-risk
- "contingency"             # risk-related
- "delta-CDR"               # incremental review type
- "red team"                # adversarial review
```

#### 2.2 State Management Enhancement

Current state passing is documented but not enforced. Per Google ADK patterns from `agent-research-002`:

```yaml
# PROPOSED: Explicit state schema in YAML frontmatter
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
  persistence: file  # or memory, checkpoint
```

#### 2.3 Missing Orchestration Patterns

From `agent-research-002` analysis, the following patterns are not explicitly documented:

| Pattern | Current Support | Recommendation |
|---------|-----------------|----------------|
| Sequential Pipeline | Implicit (described in PLAYBOOK) | Formalize with examples |
| Hierarchical/Supervisor | Implicit (orchestrator described) | Add explicit coordinator agent |
| Generator-Critic Loop | NOT IMPLEMENTED | Add for quality assurance |
| Parallel Execution | NOT IMPLEMENTED | Add for research fan-out |
| Human-in-the-Loop | NOT IMPLEMENTED | Add breakpoint support |

#### 2.4 Playbook Enhancement Opportunities

**Current PLAYBOOK.md Coverage:**
- Invocation methods (natural language, explicit, chained)
- Orchestration patterns (single, sequential, fan-out, fan-in)
- Practical examples (5 detailed scenarios)
- Tips and best practices
- Troubleshooting

**Missing PLAYBOOK Topics:**
1. **Error Recovery Patterns** - What to do when agents fail
2. **Iterative Refinement** - How to improve agent outputs
3. **Cross-Skill Handoffs** - ps-* to nse-* transitions
4. **Batch Processing** - Handling multiple items
5. **Version Migration** - Updating from v1.x to v2.x

### 3. Industry Comparison

#### 3.1 Framework Feature Matrix

| Feature | Jerry Skills | CrewAI | LangGraph | OpenAI Agents SDK |
|---------|--------------|--------|-----------|-------------------|
| Role-based agents | YES | YES | YES | YES |
| Explicit permissions | YES (forbidden actions) | YES (allow_delegation) | YES (tool restrictions) | YES (guardrails) |
| State persistence | File-based | ChromaDB + SQLite | Checkpointing | Session-based |
| Parallel execution | NOT YET | Flows | Native (Send) | Limited |
| Generator-Critic | NOT YET | @router | Conditional edges | Manual |
| Human-in-the-Loop | NOT YET | human_input=True | interrupt_before/after | Guardrails |
| Tiered output | L0/L1/L2 | NO | NO | NO |
| Constitutional compliance | YES (explicit) | NO | NO | Guidelines only |
| Domain-specific extensions | YES (nse-* with NASA SE) | NO | NO | NO |

#### 3.2 Competitive Advantages

**Jerry Skills Excel At:**
1. **Audience-Aware Output**: L0/L1/L2 tiered explanations unique among frameworks
2. **Constitutional Governance**: Explicit principle enforcement with escalation paths
3. **Domain Extensibility**: nse-* demonstrates clean domain skill extension pattern
4. **Provenance Tracking**: P-004 requires explicit sourcing (missing in competitors)
5. **Context Rot Mitigation**: P-002 mandates file persistence (others rely on memory)

**Jerry Skills Lag Behind:**
1. **Parallel Execution**: No native fan-out support (LangGraph, CrewAI have this)
2. **State Checkpointing**: No time-travel debugging (LangGraph specialty)
3. **Interactive Refinement**: No generator-critic loops (Google ADK, CrewAI Flows)
4. **Programmatic Orchestration**: Skills designed for natural language, not SDK-first

### 4. Missing Capabilities

#### 4.1 Critical Gaps

| Gap | Impact | Priority | Effort |
|-----|--------|----------|--------|
| No explicit model specification | Inconsistent agent quality | HIGH | LOW |
| No parallel execution | Slow multi-topic research | HIGH | MEDIUM |
| No generator-critic pattern | Quality inconsistency | MEDIUM | MEDIUM |
| No state checkpointing | Cannot resume failed workflows | MEDIUM | HIGH |
| No cross-skill handoff protocol | Manual ps-* to nse-* | MEDIUM | LOW |

#### 4.2 Recommended New Agents

Based on industry patterns and identified gaps:

| Proposed Agent | Pattern | Purpose |
|----------------|---------|---------|
| `ps-coordinator` | Supervisor | Central orchestration for complex multi-agent workflows |
| `ps-critic` | Generator-Critic | Quality evaluation and feedback generation |
| `ps-parallel` | Map-Reduce | Coordinate parallel research/analysis |
| `nse-coordinator` | Supervisor | NASA SE workflow orchestration |
| `nse-qa` | Generator-Critic | SE artifact quality assurance |

---

## L2: Strategic Implications

### 1. Recommendations

#### 1.1 Immediate Actions (Week 1-2)

| Action | Rationale | Owner |
|--------|-----------|-------|
| Add missing activation keywords | Improves auto-routing accuracy | ps-* maintainer |
| Add `model: opus/sonnet/haiku` to frontmatter | Enables consistent agent behavior | Both skills |
| Document cross-skill handoff protocol | Enables ps-* to nse-* pipeline | Documentation |
| Add error recovery section to PLAYBOOKs | Improves user experience | Documentation |

#### 1.2 Short-Term Improvements (Week 3-6)

| Action | Rationale | Dependencies |
|--------|-----------|--------------|
| Implement `ps-critic` agent | Quality assurance pattern | PS_AGENT_TEMPLATE |
| Add state schema enforcement | Google ADK alignment | Template update |
| Create cross-skill handoff examples | Enable pipeline workflows | Handoff protocol |
| Add batch processing guidance | Enterprise use cases | PLAYBOOK update |

#### 1.3 Medium-Term Enhancements (Week 7-12)

| Action | Rationale | Dependencies |
|--------|-----------|--------------|
| Implement parallel execution support | Performance for fan-out research | Architecture decision |
| Add state checkpointing | Resume failed workflows | Infrastructure change |
| Create `ps-coordinator` agent | Complex workflow orchestration | Parallel support |
| SDK integration layer | Programmatic orchestration | Design decision |

### 2. Risks of Not Addressing

| Risk | Consequence | Likelihood | Impact |
|------|-------------|------------|--------|
| Missing keywords cause routing failures | User frustration, manual intervention | HIGH | MEDIUM |
| No parallel execution limits scale | Cannot compete with CrewAI/LangGraph for complex tasks | MEDIUM | HIGH |
| No quality loop causes inconsistent output | Trust erosion, rework | MEDIUM | MEDIUM |
| No cross-skill handoff blocks pipelines | Cannot operationalize PROJ-002 dual-pipeline | HIGH | HIGH |

### 3. Implementation Priority

**Priority Matrix:**

```
HIGH IMPACT
    ^
    |  [1] Keywords     [2] Cross-skill handoff
    |  [3] ps-critic    [4] Parallel execution
    |
    |  [5] State schema [6] Checkpointing
    |
    |  [7] Coordinator  [8] SDK layer
    +---------------------------------------->
                                    HIGH EFFORT
```

**Recommended Sequence:**
1. Keywords (low effort, immediate routing improvement)
2. Cross-skill handoff protocol (enables PROJ-002 pipeline)
3. ps-critic agent (quality assurance)
4. State schema enforcement (Google ADK alignment)
5. Parallel execution (performance)
6. ps-coordinator agent (complex orchestration)

---

## Cross-Pollination Metadata

- **Source Agent:** ps-r-001 (ps-researcher)
- **Target Audience:** nse-requirements, nse-architecture, project leadership
- **Pipeline Phase:** Phase 1 - Research
- **Artifact Type:** Research Document

### Key Handoff Items for nse-* Pipeline

1. **REQ-001: Activation Keyword Coverage**
   - Add missing NASA SE keywords to nse-* SKILL.md
   - Keywords: mission assurance, independent verification, TRL, heritage, anomaly

2. **REQ-002: Cross-Skill Handoff Protocol**
   - Define formal ps-* to nse-* handoff schema
   - Include: source agent, target agent, context bundle, continuation_hint

3. **REQ-003: State Management Schema**
   - Formalize output_key and state schema in nse-* agents
   - Align with Google ADK state management patterns

4. **REQ-004: Quality Assurance Agent**
   - Create nse-qa agent for SE artifact quality evaluation
   - Implement generator-critic pattern

### Gaps for nse-* Pipeline to Address

| Gap ID | Description | Recommended Action |
|--------|-------------|-------------------|
| GAP-001 | No explicit model specification in agent definitions | Add `model: opus/sonnet` to frontmatter |
| GAP-002 | No parallel execution for V&V activities | Design nse-parallel agent |
| GAP-003 | No formal handoff from ps-analyst to nse-risk | Define risk assessment handoff protocol |
| GAP-004 | No quality loop for requirements refinement | Implement nse-qa with generator-critic |
| GAP-005 | NASA SE keywords incomplete | Expand activation keywords list |

### Research Artifacts for Reference

| Artifact | Location | Relevance |
|----------|----------|-----------|
| Claude Code Mechanics | `research/agent-research-001-claude-code-mechanics.md` | Task tool patterns |
| Multi-Agent Patterns | `research/agent-research-002-multi-agent-patterns.md` | Industry comparison |
| PS Agent Template | `skills/problem-solving/agents/PS_AGENT_TEMPLATE.md` | Template standard |
| NSE Agent Template | `skills/nasa-se/agents/NSE_AGENT_TEMPLATE.md` | NASA SE extension |

---

## References

### Primary Sources Analyzed

1. `skills/problem-solving/SKILL.md` (v2.0.0)
2. `skills/problem-solving/PLAYBOOK.md` (v2.0.0)
3. `skills/problem-solving/agents/PS_AGENT_TEMPLATE.md` (v2.0.0)
4. `skills/nasa-se/SKILL.md` (v1.0.0)
5. `skills/nasa-se/PLAYBOOK.md` (v1.0.0)
6. `skills/nasa-se/agents/NSE_AGENT_TEMPLATE.md` (v1.0.0)
7. `projects/PROJ-002-nasa-systems-engineering/research/agent-research-001-claude-code-mechanics.md`
8. `projects/PROJ-002-nasa-systems-engineering/research/agent-research-002-multi-agent-patterns.md`

### Industry References

- [Anthropic Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Google ADK Multi-Agent Patterns](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/)
- [LangGraph Multi-Agent Workflows](https://blog.langchain.com/langgraph-multi-agent-workflows/)
- [CrewAI Documentation](https://docs.crewai.com/)
- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)

---

*Research Document: PS-R-001-SKILLS-OPT*
*Generated by: ps-researcher (ps-r-001)*
*Date: 2026-01-09*
*Classification: RESEARCH ONLY*
