# Agent Synthesis Patterns: Fan-In Aggregation Research

**Document ID:** PS-ORCH-002-RESEARCH
**Date:** 2026-01-11
**Author:** ps-researcher v2.1.0
**PS Entry:** e-001

---

## L0: Executive Summary

Multi-agent synthesis requires structured aggregation patterns to combine diverse agent outputs into coherent results. The dominant patterns are **hierarchical aggregation** (tree-structured reduction), **consensus-based merging** (voting/agreement mechanisms), and **quality-weighted synthesis** (confidence-scored combination). Effective fan-in requires explicit conflict resolution strategies and traceability from source to synthesis.

---

## L1: Key Findings

### 1. Fan-In Aggregation Patterns

| Pattern | Use Case | Trade-offs |
|---------|----------|------------|
| **Hierarchical Reduction** | Large agent counts, tree-structured tasks | Scalable but loses minority perspectives |
| **Consensus Voting** | Discrete decisions, classification tasks | Simple but requires agreement threshold tuning |
| **Weighted Ensemble** | Continuous outputs, confidence-scored agents | Flexible but requires calibrated confidence |
| **Debate/Critique Loop** | High-stakes synthesis, adversarial validation | High quality but computationally expensive |

### 2. Industry Best Practices

1. **Explicit Provenance**: Every synthesized claim should trace to source agents (Microsoft AutoGen pattern [1])
2. **Conflict Detection Before Resolution**: Surface disagreements explicitly rather than averaging them away (OpenAI swarm pattern [2])
3. **Quality Gates**: Establish minimum confidence thresholds before including agent outputs (Anthropic MCP pattern [3])
4. **Structured Output Schemas**: Enforce consistent output formats across agents to enable mechanical aggregation (LangChain LCEL pattern [4])

### 3. Quality Control in Synthesis Workflows

- **Pre-synthesis validation**: Schema conformance, completeness checks
- **During synthesis**: Conflict detection, outlier identification
- **Post-synthesis verification**: Self-consistency, coverage analysis
- **Meta-evaluation**: Human-in-the-loop spot checks, automated regression testing

---

## L2: Detailed Analysis

### 2.1 Hierarchical Aggregation (MapReduce Pattern)

The MapReduce pattern from distributed computing translates directly to multi-agent synthesis:

```
Agent_1 ─┐
Agent_2 ─┼─► Reducer_A ─┐
Agent_3 ─┘              │
                        ├─► Final Synthesizer ─► Output
Agent_4 ─┐              │
Agent_5 ─┼─► Reducer_B ─┘
Agent_6 ─┘
```

**Advantages:**
- Scales logarithmically with agent count
- Natural parallelization at each level
- Clear responsibility boundaries

**Challenges:**
- Information loss at each reduction level
- Reducer design significantly impacts quality
- Difficult to surface minority but valid perspectives

**Citation:** Dean, J., & Ghemawat, S. (2004). MapReduce: Simplified Data Processing on Large Clusters. OSDI'04 [5]

### 2.2 Consensus Mechanisms

Drawing from distributed systems and blockchain consensus:

1. **Majority Voting**: Simple plurality wins (2/3 agreement threshold common)
2. **Weighted Voting**: Agent reliability scores influence vote weight
3. **Byzantine Fault Tolerance**: Tolerate up to f faulty agents in 3f+1 total
4. **Probabilistic Consensus**: Accept outputs above confidence threshold

**Quality Control Integration:**
- Track agent reliability over time
- Penalize consistent outliers
- Reward agents whose outputs survive synthesis

**Citation:** Castro, M., & Liskov, B. (1999). Practical Byzantine Fault Tolerance. OSDI'99 [6]

### 2.3 Debate and Critique Patterns

Adversarial synthesis improves quality through structured disagreement:

1. **Generator-Critic**: One agent proposes, another critiques (Anthropic Constitutional AI pattern [7])
2. **Multi-Agent Debate**: Agents argue positions, synthesizer adjudicates (MIT/Google debate research [8])
3. **Red Team/Blue Team**: Adversarial validation before synthesis acceptance

**Implementation Considerations:**
- Debate rounds should be bounded (typically 2-3 iterations)
- Clear termination criteria prevent infinite loops
- Synthesizer must have authority to break deadlocks

**Citation:** Irving, G., Christiano, P., & Amodei, D. (2018). AI Safety via Debate. arXiv:1805.00899 [8]

### 2.4 Structured Output Requirements

For mechanical aggregation, agent outputs must conform to shared schemas:

```yaml
agent_output:
  confidence: 0.85
  claims:
    - statement: "..."
      evidence: ["..."]
      sources: ["..."]
  uncertainties:
    - "..."
  conflicts_with: []  # IDs of conflicting claims
```

**Schema Enforcement Strategies:**
- JSON Schema validation at output boundaries
- Pydantic/Zod models for type safety
- Retry with feedback on schema violations

**Citation:** LangChain Documentation - Structured Output [4]

---

## L3: Implementation Recommendations for Jerry Framework

### 3.1 Recommended Pattern for PS Orchestration

Given Jerry's hexagonal architecture and emphasis on traceability:

1. **Use Quality-Weighted Hierarchical Aggregation**
   - Agents output confidence scores (P-001 Truth and Accuracy)
   - Reducer agents weight by confidence and historical reliability
   - Final synthesizer preserves dissenting views as footnotes

2. **Implement session_context for Provenance**
   - Every agent output carries session_context YAML
   - Synthesizer aggregates source_agent references
   - Full audit trail from claim to originating agent

3. **Apply Generator-Critic Loops for High-Stakes Outputs**
   - ps-critic agent validates ps-generator outputs
   - Bounded to 2 iterations per P-003 (no recursive spawning)
   - Explicit conflict resolution documentation

### 3.2 Integration Points

- **Work Tracker**: Track synthesis tasks as work items with parent-child relationships
- **Constitution Compliance**: P-004 requires documenting synthesis rationale
- **File Persistence**: P-002 mandates all intermediate outputs persisted

---

## References

[1] Microsoft AutoGen. (2023). Multi-Agent Conversation Framework. https://microsoft.github.io/autogen/

[2] OpenAI. (2024). Swarm: Educational Framework for Multi-Agent Systems. https://github.com/openai/swarm

[3] Anthropic. (2024). Model Context Protocol Specification. https://modelcontextprotocol.io/

[4] LangChain. (2024). LCEL: LangChain Expression Language. https://python.langchain.com/docs/concepts/lcel/

[5] Dean, J., & Ghemawat, S. (2004). MapReduce: Simplified Data Processing on Large Clusters. OSDI'04.

[6] Castro, M., & Liskov, B. (1999). Practical Byzantine Fault Tolerance. OSDI'99.

[7] Bai, Y., et al. (2022). Constitutional AI: Harmlessness from AI Feedback. arXiv:2212.08073.

[8] Irving, G., Christiano, P., & Amodei, D. (2018). AI Safety via Debate. arXiv:1805.00899.

---

```yaml
session_context:
  schema_version: "1.0.0"
  session_id: "ps-orch-002-test"
  source_agent:
    id: "ps-researcher"
    family: "ps"
    version: "2.1.0"
  target_agent:
    id: "ps-synthesizer"
  payload:
    key_findings:
      - "Hierarchical aggregation (MapReduce) scales logarithmically but risks minority perspective loss"
      - "Consensus mechanisms require explicit agreement thresholds and Byzantine fault tolerance considerations"
      - "Generator-Critic loops improve synthesis quality but must be bounded to prevent infinite recursion"
      - "Structured output schemas with confidence scores enable mechanical aggregation and quality weighting"
      - "Full provenance tracking (source agent to final claim) is essential for auditability"
    artifacts:
      - path: "projects/PROJ-002-nasa-systems-engineering/tests/ps-orchestration-results/PS-ORCH-002/fanout-research.md"
        type: "research"
    confidence: 0.88
    research_coverage:
      - "Multi-agent aggregation patterns"
      - "Consensus mechanisms from distributed systems"
      - "Debate and adversarial validation"
      - "Structured output requirements"
```
