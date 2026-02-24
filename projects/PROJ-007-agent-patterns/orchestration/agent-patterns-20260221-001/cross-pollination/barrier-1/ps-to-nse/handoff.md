# Barrier 1 Cross-Pollination: PS Pipeline -> NSE Pipeline

<!-- HANDOFF: barrier-1 | DIRECTION: ps-to-nse | DATE: 2026-02-21 -->

> Synthesized findings from Problem-Solving Phase 1 Research (3 agents) for consumption by NASA SE Phase 2 Analysis agents (nse-requirements-001, nse-architecture-001, nse-risk-001).

## Document Sections

| Section | Purpose |
|---------|---------|
| [Key Findings Summary](#key-findings-summary) | Critical discoveries across all 3 PS researchers |
| [Agent Architecture Findings](#agent-architecture-findings) | From ps-researcher-001 |
| [Routing & Trigger Findings](#routing--trigger-findings) | From ps-researcher-002 |
| [Industry Best Practice Findings](#industry-best-practice-findings) | From ps-researcher-003 |
| [Consolidated Source Authority](#consolidated-source-authority) | Source quality and coverage |
| [NSE Phase 2 Guidance](#nse-phase-2-guidance) | Specific inputs for each NSE agent |

---

## Key Findings Summary

### Top-Level Consensus (3+ authoritative sources agree)

1. **Start simple, add complexity only when needed.** Anthropic, OpenAI, Google, Microsoft all advocate single-agent-with-tools before multi-agent. (ps-researcher-001, ps-researcher-003)
2. **Orchestrator-Worker is the canonical multi-agent pattern.** Max one level of nesting. Directly validates Jerry's P-003/H-01. (ps-researcher-001, ps-researcher-003)
3. **Context engineering is the defining challenge.** Managing finite context window through compaction, isolation, structured note-taking, and progressive disclosure. (ps-researcher-001, ps-researcher-003)
4. **Structured handoffs are critical.** Free-text handoffs are the #1 source of context loss in production multi-agent systems (Google, 2026). JSON Schema-based handoffs recommended. (ps-researcher-002)
5. **Layered routing outperforms single-mechanism routing.** Keyword -> semantic -> LLM fallback provides best coverage/speed tradeoff. (ps-researcher-002, ps-researcher-003)
6. **Agent Skills (progressive disclosure) prevent context bloat.** Three-tier loading: metadata at startup, core on relevance, supplementary on-demand. (ps-researcher-001)
7. **Quality assurance requires multi-tier approach.** LLM-as-judge, creator-critic loops, behavioral testing, drift detection. (ps-researcher-003)
8. **Guardrails and constitutional constraints are table stakes.** Not optional for production deployments. (ps-researcher-003)
9. **"Bag of Agents" anti-pattern** causes 17x error amplification. Agents need formal topology. (ps-researcher-002)
10. **Context-centric decomposition > problem-centric decomposition.** Divide by context boundaries, not work type. Prevents "telephone game" information degradation. (ps-researcher-002)

### Quantitative Data Points

| Metric | Value | Source |
|--------|-------|--------|
| Multi-agent token overhead vs single-agent | 3-10x | Anthropic, 2026 |
| Rule-based routing latency | ~1ms | ps-researcher-002 |
| Semantic routing latency | ~100ms | ps-researcher-002 |
| LLM-as-router latency | ~500-5000ms | ps-researcher-002 |
| Error amplification without formal topology | 17x | Google DeepMind |
| Claude Code internal tools | 14 (4 command, 6 file, 2 web, 2 control) | ps-researcher-001 |
| Claude Code model tiers | 3 (Haiku/Sonnet/Opus) | ps-researcher-001 |
| Industry frameworks surveyed | 5 (LangGraph/CrewAI/AutoGen/Semantic Kernel/OpenAI Agents SDK) | ps-researcher-003 |

---

## Agent Architecture Findings

**Source:** ps-researcher-001 (14 cited sources)

### Claude Code Agent Architecture

- **Single agent loop** with 14 internal tools, NOT a chatbot
- **Four-stage feedback cycle:** Gather Context -> Take Action -> Verify Work -> Iterate
- **Orchestrator-Worker model:** Lead agent spawns subagents via Task tool; each runs in own context window with custom system prompt and tool access
- **Max one level of nesting** (validates P-003/H-01)
- **Five composable workflow patterns** (Anthropic): Prompt Chaining, Routing, Parallelization, Orchestrator-Workers, Evaluator-Optimizer

### Agent Skills Architecture

- Three-tier progressive disclosure: metadata (startup) -> core (relevance) -> supplementary (on-demand)
- Skills are organized folders with SKILL.md, agents/, templates/
- Prevents context window bloat by selective loading
- Jerry's existing skill architecture validated by Anthropic's published patterns

### Subagent Configuration

- Custom system prompt per subagent
- Tool allowlist/denylist per subagent
- Model selection per subagent (Haiku for fast, Sonnet for balanced, Opus for complex)
- Can run in background with async result retrieval
- Context isolation: subagent does NOT inherit parent's full context

### Key Risk Identified

- **Context rot** at scale: agent performance degrades as context fills
- Mitigation: filesystem-as-memory pattern (Jerry's core solution), structured note-taking, progressive disclosure

---

## Routing & Trigger Findings

**Source:** ps-researcher-002 (23 cited sources)

### Routing Mechanism Spectrum

| Mechanism | Latency | Flexibility | When to Use |
|-----------|---------|-------------|-------------|
| Rule-Based (keyword/regex) | ~1ms | Low | Clear, deterministic patterns |
| ML-Classifier | ~10-50ms | Medium | Large training datasets available |
| Semantic/Embedding | ~100ms | High | Semantic intent matching |
| LLM-as-Router | ~500-5000ms | Highest | Novel/ambiguous inputs |

### Recommended: Layered Trigger Architecture

1. **Fast pass:** Keyword/regex matching (Jerry's current mandatory-skill-usage.md)
2. **Second pass:** Semantic similarity scoring (new capability)
3. **Final arbiter:** LLM intent classification (fallback for ambiguous cases)

### Handoff Protocol Requirements

- **Structured handoff schemas** (JSON Schema) are critical -- free-text handoffs are #1 failure source
- **Context-centric decomposition** recommended -- divide agents by context boundaries, not work type
- **Routing loop prevention** required -- max iterations + circuit breaker pattern
- **Negative keywords + priority ordering** needed to resolve multi-skill keyword overlap

### Anti-Patterns to Codify

1. **Bag of Agents** -- uncoordinated agents without formal topology (17x error amplification)
2. **Over-routing** -- too many routing hops degrade quality
3. **Under-routing** -- single agent trying to do everything
4. **Routing loops** -- agents bouncing between each other without termination
5. **Telephone game** -- information degradation through sequential handoffs

---

## Industry Best Practice Findings

**Source:** ps-researcher-003 (30+ cited sources)

### 8 Agent Pattern Families Identified

1. **Workflow Patterns** (Prompt Chaining, Routing, Parallelization)
2. **Delegation Patterns** (Orchestrator-Workers, Manager, Hierarchical Decomposition)
3. **Quality Patterns** (Evaluator-Optimizer, Generator-Critic, Iterative Refinement)
4. **Context Patterns** (Progressive Disclosure, Skills, Structured Note-Taking)
5. **Safety Patterns** (Constitutional AI, Guardrails, Bounded Autonomy)
6. **Testing Patterns** (LLM-as-Judge, Behavioral Testing, Drift Detection)
7. **Integration Patterns** (MCP, Tool Composition, Capability Discovery)
8. **Governance Patterns** (Human-in-the-Loop, Approval Gates, Audit Trails)

### Framework Comparison (Key Dimensions)

| Dimension | LangGraph | CrewAI | AutoGen | Agent SDK |
|-----------|-----------|--------|---------|-----------|
| Architecture | Graph-based state machine | Role-based crew | Multi-agent conversation | Single-agent + subagents |
| State Management | Explicit (StateGraph) | Implicit (shared memory) | Message-based | Filesystem-based |
| HITL Support | Strong (interrupt_before) | Moderate | Moderate | Strong (hooks, permissions) |
| Best For | Complex workflows | Team collaboration | Research/debate | Tool-augmented tasks |

### Emerging Trends (High PROJ-007 Relevance)

| Trend | Maturity | Relevance |
|-------|----------|-----------|
| Agent Skills / Progressive Disclosure | Production | HIGH |
| MCP (Model Context Protocol) | Production | HIGH |
| Contract-First Delegation (DeepMind) | Research | HIGH |
| Context Engineering as Discipline | Emerging | HIGH |
| Autonomous Purple Teaming | Research | MEDIUM |
| Deep Agents (multi-session) | Early Production | MEDIUM |

---

## Consolidated Source Authority

| Authority Tier | Count | Examples |
|----------------|-------|---------|
| Industry Leader | 12 | Anthropic (5), Google (3), Microsoft (2), OpenAI (2) |
| Official Documentation | 8 | LangGraph, CrewAI, AutoGen, MCP spec |
| Industry Innovator | 10 | Patronus AI, Aurelio Labs, Gartner |
| Community Expert | 15+ | Blog posts, GitHub repos, conference talks |
| Research Paper | 5+ | Google DeepMind delegation, multi-agent surveys |

**Total unique sources across PS Phase 1:** 67+

---

## NSE Phase 2 Guidance

### For nse-requirements-001 (Requirements Engineer)

Use these findings to formulate shall-statements for:
- Agent structure requirements (single-level nesting, context isolation, tool restriction)
- Prompt design requirements (role clarity, progressive disclosure, cognitive mode)
- Routing requirements (layered approach, negative keywords, fallback handling)
- Handoff requirements (structured schemas, context preservation, loop prevention)
- Quality requirements (multi-tier QA, threshold enforcement, iteration limits)
- Anti-pattern avoidance (Bag of Agents, over-routing, telephone game)

### For nse-architecture-001 (Architect)

Use these findings to:
- Map hexagonal architecture concepts to agent patterns (ports = tool interfaces, adapters = prompt strategies, domain = reasoning core)
- Evaluate architecture alternatives against the 5 composable workflow patterns
- Design agent integration patterns based on structured handoff protocols
- Consider context-centric decomposition as the primary design principle

### For nse-risk-001 (Risk Assessor)

Key risks to assess from this research:
- **Context rot** (HIGH likelihood, HIGH impact) -- agent performance degrades with context fill
- **Routing ambiguity** (MEDIUM likelihood, HIGH impact) -- multi-skill keyword overlap
- **Handoff information loss** (HIGH likelihood, MEDIUM impact) -- free-text handoff failures
- **Error amplification** (LOW likelihood, HIGH impact) -- uncoordinated agent topology
- **Token cost escalation** (MEDIUM likelihood, MEDIUM impact) -- multi-agent 3-10x overhead
- **Framework lock-in** (LOW likelihood, MEDIUM impact) -- pattern dependency on Claude Code specifics
