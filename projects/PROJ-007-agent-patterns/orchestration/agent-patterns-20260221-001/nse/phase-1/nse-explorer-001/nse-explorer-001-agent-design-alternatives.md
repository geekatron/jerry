---
DISCLAIMER: This guidance is AI-generated based on NASA Systems Engineering
standards. It is advisory only and does not constitute official NASA guidance.
All SE decisions require human review and professional engineering judgment.
Not for use in mission-critical decisions without SME validation.
---

# Trade Study: Agent Design Alternatives for Claude Code Agent Patterns

> **Project:** PROJ-007
> **Entry:** e-004
> **Date:** 2026-02-21
> **Status:** Draft
> **NASA Process:** NPR 7123.1D Process 5 (Product Implementation), Process 17 (Decision Analysis)
> **Agent:** nse-explorer v2.1.0
> **Cognitive Mode:** Divergent

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Plain-language overview of alternatives and recommendations |
| [Research Methodology](#research-methodology) | Sources consulted and evaluation approach |
| [Trade Study 1: Agent Architecture](#trade-study-1-agent-architecture-alternatives) | Monolithic vs. microservice vs. hybrid agent designs |
| [Trade Study 2: Agent Definition Format](#trade-study-2-agent-definition-format-alternatives) | YAML+MD vs. pure YAML vs. code-first vs. DSL |
| [Trade Study 3: Agent Routing Architecture](#trade-study-3-agent-routing-architecture-alternatives) | Keyword vs. semantic vs. LLM-as-router vs. rule-based |
| [Trade Study 4: Quality Assurance Architecture](#trade-study-4-quality-assurance-architecture-alternatives) | Self-review vs. creator-critic vs. tournament vs. schema validation |
| [Trade Study 5: Tool Integration Architecture](#trade-study-5-tool-integration-architecture-alternatives) | Static vs. dynamic vs. MCP federation |
| [L2: Cross-Cutting Architecture Analysis](#l2-cross-cutting-architecture-analysis) | System-level trade-offs and strategic recommendations |
| [Assumptions Challenged](#assumptions-challenged) | Conventional wisdom tested during exploration |
| [Open Questions](#open-questions) | Unresolved items requiring further analysis |
| [References](#references) | Complete source list |

---

## L0: Executive Summary

This trade study explores five fundamental design dimensions for building Claude Code agent systems: how agents are structured (architecture), how they are defined (format), how work gets routed to the right agent (routing), how quality is ensured (QA), and how agents connect to tools (tool integration).

**Key findings in plain language:**

- **Architecture:** A hybrid approach combining specialist agents with shared infrastructure services outperforms both fully monolithic and fully microservice designs. Jerry's current skill-based agent pattern is well-positioned but could benefit from stronger state management between agents.

- **Definition Format:** The YAML frontmatter + Markdown body pattern (Jerry's current approach) is among the strongest options available. It combines machine-readable configuration with human-readable instructions. The emerging Open Agent Specification (Agent Spec) standard validates this direction. Minor enhancements -- such as adding schema validation -- would strengthen it further.

- **Routing:** Keyword matching (Jerry's current approach) is fast and predictable but brittle. A layered routing strategy that uses fast keyword matching as a first pass, with LLM-based fallback for ambiguous cases, would improve accuracy without sacrificing speed.

- **Quality:** Jerry's multi-tier quality system (self-review, creator-critic cycles, tournament mode) is more sophisticated than most frameworks in the industry. The main improvement opportunity is adding lightweight output schema validation as a deterministic pre-check before LLM-based quality assessment.

- **Tool Integration:** MCP (Model Context Protocol) is the clear industry standard for tool integration. Jerry's current static tool assignment per agent is the right baseline; dynamic tool discovery should be reserved for future evolution when agent autonomy increases.

**Bottom line:** Jerry's existing patterns are architecturally sound and ahead of industry norms in several areas (quality assurance, agent definition richness). The highest-value improvements are: (1) layered routing with LLM fallback, (2) schema validation for agent outputs, and (3) standardized state management across agent handoffs.

---

## Research Methodology

### Sources Consulted

| Source Category | Sources Used | Key Insights |
|----------------|-------------|--------------|
| Web Research | 8 targeted searches across architecture, formats, routing, QA, MCP, Claude Code, multi-agent frameworks, persona engineering | Industry trends, framework comparisons, emerging standards |
| Context7 MCP | MCP Specification (2025-11-25), LangGraph documentation | Tool integration patterns, state management models |
| Codebase Analysis | AGENTS.md, ps-researcher.md, nse-explorer.md, mandatory-skill-usage.md, mcp-tool-standards.md | Current Jerry patterns, 37 agent definitions analyzed |
| Framework Comparisons | LangGraph, CrewAI, AutoGen, Claude Agent SDK | Architectural approaches across major frameworks |

### Evaluation Criteria

All alternatives are evaluated against six weighted criteria per NPR 7123.1D Process 17:

| ID | Criterion | Weight | Description | Rationale |
|----|-----------|--------|-------------|-----------|
| C1 | Simplicity | 0.20 | Ease of understanding and implementation | Reduces onboarding cost and cognitive load; directly fights context rot |
| C2 | Flexibility | 0.20 | Ability to handle diverse agent types and use cases | Jerry serves 37 agents across 8 skills with varied cognitive modes |
| C3 | Maintainability | 0.20 | Long-term maintenance burden, ease of updates | Framework longevity depends on sustainable maintenance patterns |
| C4 | Quality Control | 0.15 | Ability to enforce and verify quality standards | Core Jerry differentiator; H-13 through H-19 enforcement |
| C5 | Context Efficiency | 0.15 | Context window usage optimization | Context rot is Jerry's core problem statement |
| C6 | P-003 Compliance | 0.10 | Compatibility with no-recursive-subagents constraint | Constitutional hard constraint; non-negotiable |

**Scoring Scale:** 1 (Poor) to 5 (Excellent)

---

## Trade Study 1: Agent Architecture Alternatives

### Decision Context

**Problem Statement:** How should agents be structured within a Claude Code agent framework? Should each agent be a self-contained unit, or should agents share infrastructure and state?

**Driving Requirements:**
- P-003: No recursive subagents (max 1 level: orchestrator -> worker)
- H-01: Agent hierarchy constraint
- Context isolation for focused reasoning
- Parallel execution capability
- Quality gate enforcement at handoffs

**Constraints:**
- Claude Code operates within a single LLM context window
- Subagent spawning via Task tool is single-level only
- Context window is finite (200K tokens typical)

### L1: Technical Alternatives

#### Alternative A1: Monolithic Agent

**Description:** A single, large agent definition that handles all tasks. The agent has comprehensive instructions covering all domains and switches behavior based on task type. No subagent delegation.

**Pros:**
- Zero handoff overhead
- No state management between agents
- Single context window contains all knowledge
- Simplest deployment and invocation

**Cons:**
- Context window saturation as instructions grow
- No cognitive mode specialization (divergent vs. convergent)
- Quality enforcement applied uniformly regardless of task
- No parallel execution capability
- Violates separation of concerns
- A single change affects the entire system

**Feasibility:** Medium -- technically possible but degrades with scale
**Risk Level:** High -- context rot accelerates as monolith grows

**Industry Evidence:** SuperAGI's analysis shows monolithic agents struggle beyond ~20K tokens of instructions. Netflix's migration to microservices saw 50% reduction in deployment time.

---

#### Alternative A2: Pure Microservice Agents

**Description:** Each agent is fully independent with its own complete context, tools, and state management. No shared infrastructure. Agents communicate only through explicit message passing with full serialization.

**Pros:**
- Maximum context isolation
- Independent deployment and testing
- Clear ownership boundaries
- Agents can use different models (opus vs. sonnet)
- Fault isolation -- one agent failure does not cascade

**Cons:**
- High handoff overhead (serialization/deserialization)
- Duplicated tool definitions and guardrails across agents
- State synchronization is complex
- Context window wasted on repeated boilerplate
- Harder to enforce cross-agent quality standards

**Feasibility:** Medium -- achievable but with significant overhead
**Risk Level:** Medium -- complexity in coordination, but individual agents are simple

**Industry Evidence:** The "distributed monolith" anti-pattern (TNGlobal, 2025) warns that microservice decomposition without event-driven architecture creates worse outcomes than monoliths.

---

#### Alternative A3: Skill-Based Specialist Agents (Current Jerry Pattern)

**Description:** Agents are grouped by skill domain (problem-solving, NASA SE, orchestration, etc.). Each agent has a specialized persona, cognitive mode, and tool set. A skill orchestrator routes to the appropriate specialist. Agents share some infrastructure (constitutional compliance, guardrails) but have isolated context.

**Pros:**
- Natural domain decomposition (research, analysis, review)
- Cognitive mode specialization (divergent vs. convergent)
- Shared guardrails reduce duplication
- Quality gates at skill boundaries
- P-003 compliance built into the pattern
- Progressive disclosure -- agents load only what they need

**Cons:**
- Handoff protocol must be maintained across all agents
- Adding a new skill requires understanding the orchestration pattern
- Session context schema must be kept in sync
- Moderate complexity in agent count management (37 agents currently)

**Feasibility:** High -- already proven in Jerry with 37 agents
**Risk Level:** Low -- mature pattern with known trade-offs

**Industry Evidence:** CrewAI's role-based model uses a nearly identical pattern -- specialized agents with distinct roles and goals working together. LangGraph's documentation explicitly recommends this for complex workflows.

---

#### Alternative A4: Event-Driven Agent Architecture

**Description:** Agents are loosely coupled through an event bus. Each agent subscribes to relevant events and publishes results. Orchestration emerges from event flow rather than explicit routing. State is maintained in an event store.

**Pros:**
- Maximum decoupling between agents
- Excellent for async and parallel workflows
- Natural audit trail through event log
- Easy to add new agents without modifying existing ones
- Resilient to individual agent failures

**Cons:**
- Significant infrastructure overhead (event bus, event store)
- Debugging is harder (distributed tracing needed)
- Event schema versioning adds complexity
- Eventual consistency complicates quality gates
- Overkill for Claude Code's single-session model
- P-003 compliance harder to verify in event-driven flows

**Feasibility:** Low -- requires infrastructure beyond Claude Code's current model
**Risk Level:** High -- architectural mismatch with LLM context window paradigm

**Industry Evidence:** TNGlobal (2025) advocates event-driven architecture for agentic AI, but this assumes distributed infrastructure that does not map well to single-context-window LLM systems.

---

#### Alternative A5: Hierarchical Agent Teams (CrewAI-Inspired)

**Description:** Agents organized in a two-layer hierarchy: Teams (Crews) of agents with a team lead, and Flows that orchestrate across teams. Team leads coordinate within their domain; flows coordinate across domains.

**Pros:**
- Natural scaling pattern for large agent counts
- Team leads can optimize intra-team handoffs
- Flows provide deterministic cross-team orchestration
- Clear escalation paths

**Cons:**
- Two-layer hierarchy may conflict with P-003 (max 1 level)
- Team lead agents add overhead without clear value in single-context LLM
- More complex than necessary for 37 agents
- "Manager" agents consume context without producing deliverables

**Feasibility:** Medium -- possible but P-003 constrains the hierarchy depth
**Risk Level:** Medium -- the team lead layer may be wasted context

**Industry Evidence:** CrewAI's Crews + Flows architecture is widely adopted but designed for multi-model systems, not single-context-window agents.

---

### Evaluation Matrix: Agent Architecture

| Criterion (Weight) | A1: Monolithic | A2: Microservice | A3: Skill-Based (Jerry) | A4: Event-Driven | A5: Hierarchical Teams |
|--------------------|---------------|------------------|------------------------|-------------------|----------------------|
| C1: Simplicity (0.20) | 5 | 2 | 4 | 1 | 3 |
| C2: Flexibility (0.20) | 1 | 4 | 4 | 5 | 4 |
| C3: Maintainability (0.20) | 2 | 3 | 4 | 2 | 3 |
| C4: Quality Control (0.15) | 2 | 3 | 5 | 3 | 4 |
| C5: Context Efficiency (0.15) | 2 | 3 | 4 | 2 | 3 |
| C6: P-003 Compliance (0.10) | 5 | 5 | 5 | 3 | 2 |
| **Weighted Total** | **2.80** | **3.15** | **4.25** | **2.65** | **3.25** |

**Rank Order:** A3 (4.25) > A5 (3.25) > A2 (3.15) > A1 (2.80) > A4 (2.65)

**Finding:** Jerry's current skill-based specialist pattern (A3) scores highest, particularly on quality control and maintainability. The event-driven pattern (A4) scores lowest due to infrastructure mismatch with single-context LLM systems.

---

## Trade Study 2: Agent Definition Format Alternatives

### Decision Context

**Problem Statement:** In what format should agent definitions be expressed? The format must capture identity, capabilities, guardrails, tool access, persona, and behavioral rules.

**Driving Requirements:**
- Machine-readability for tooling (linting, validation, registry)
- Human-readability for agent authors and maintainers
- Rich behavioral specification (persona, cognitive mode, guardrails)
- Progressive disclosure (load only what is needed)
- H-25 through H-30: Skill and agent file standards

### L1: Technical Alternatives

#### Alternative B1: YAML Frontmatter + Markdown Body (Current Jerry Pattern)

**Description:** Agent definitions use YAML frontmatter for machine-readable metadata (name, version, tools, capabilities) and Markdown body for human-readable behavioral instructions (persona, guardrails, templates). Example: Jerry's `ps-researcher.md` at 615 lines with structured YAML header and XML-tagged behavioral sections.

**Pros:**
- Best of both worlds: machine-parseable metadata + rich behavioral narrative
- Human-readable and editable with standard tools
- Git-friendly for version control and diff review
- Progressive disclosure via XML tags within Markdown
- Proven at scale (37 agents in Jerry)
- Template-friendly -- new agents follow established patterns
- IDE-compatible (syntax highlighting, folding)

**Cons:**
- No native schema validation for YAML frontmatter
- Inconsistency risk between frontmatter and body (e.g., tools listed in both)
- Large file sizes (ps-researcher.md is 615 lines)
- Parsing requires custom tooling to extract frontmatter
- XML tags within Markdown is non-standard

**Feasibility:** High -- already proven, widely understood
**Risk Level:** Low -- mature format with known trade-offs

**Industry Evidence:** Anthropic's Claude Agent Skills guide recommends "organized folders of instructions, scripts, and resources." The YAML+MD pattern aligns with this guidance. CLAUDE.md itself is a markdown-based configuration mechanism.

---

#### Alternative B2: Pure YAML/JSON Agent Definitions

**Description:** Agent definitions are expressed entirely in structured YAML or JSON. All behavioral rules, persona descriptions, and instructions are encoded as structured data fields rather than free-form text.

**Pros:**
- Fully schema-validatable
- Easy to parse programmatically
- No ambiguity between metadata and content
- Supports auto-generation and tooling
- Consistent structure across all agents

**Cons:**
- Poor expressiveness for behavioral nuance (persona, cognitive mode descriptions)
- Deeply nested YAML becomes unreadable
- Loses the narrative quality of natural language instructions
- Changes require understanding the schema, not just writing prose
- Multi-line strings in YAML are error-prone
- Cannot embed examples or templates naturally

**Feasibility:** High -- technically straightforward
**Risk Level:** Medium -- expressiveness loss may degrade agent behavior quality

**Industry Evidence:** The Open Agent Specification (Agent Spec, October 2025) uses YAML/JSON serialization but acknowledges the need for rich descriptions: "agentic entities are first-class components with standardized I/O schemas." The Google A2A protocol uses JSON schema but focuses on inter-agent communication, not behavioral definition.

---

#### Alternative B3: Code-First Agent Definitions (Python Classes)

**Description:** Agents are defined as Python classes with typed attributes, methods for behavior, and decorators for guardrails. The agent definition IS the implementation.

```python
@agent(model="opus", cognitive_mode="divergent")
class PSResearcher(BaseAgent):
    """Research Specialist with Context7 MCP integration."""

    tools = [Read, Write, WebSearch, Context7Resolve, Context7Query]

    @guardrail(type="input")
    def validate_ps_id(self, ps_id: str) -> bool:
        return re.match(r"^[a-z]+-\d+$", ps_id) is not None

    @output(levels=["L0", "L1", "L2"])
    def research(self, topic: str) -> ResearchReport:
        ...
```

**Pros:**
- Type-safe with IDE autocomplete
- Guardrails are executable, not declarative
- Testing is natural (unit tests for agent methods)
- Refactoring tools work natively
- Single source of truth (no metadata/behavior drift)

**Cons:**
- Requires Python knowledge to author agents
- Behavioral nuance (persona, cognitive mode) encoded in docstrings loses structure
- Tighter coupling to implementation language
- Harder for non-developers to contribute agent definitions
- Prompt engineering becomes code engineering (different skill set)
- H-05/H-06 UV constraints add complexity to execution

**Feasibility:** High -- standard Python patterns
**Risk Level:** Medium -- skill barrier for agent authors, persona quality may suffer

**Industry Evidence:** LangGraph uses Python-first agent definitions with `StateGraph` and typed state dictionaries. AutoGen similarly uses Python classes. Both show this pattern works but note that "prompt engineering becomes code engineering."

---

#### Alternative B4: DSL-Based Agent Specifications

**Description:** A custom Domain-Specific Language designed specifically for agent definition, combining the structure of YAML with the expressiveness of a mini-language.

```
agent ps-researcher {
  model: opus
  cognitive_mode: divergent

  persona {
    tone: professional
    style: consultative
    expertise: ["literature review", "web research"]
  }

  tools {
    required: [Read, Write, WebSearch]
    optional: [Context7.resolve, Context7.query]
  }

  guardrail input {
    ps_id matches /^[a-z]+-\d+$/
    entry_id matches /^e-\d+$/
  }

  output levels [L0, L1, L2] to "projects/{project}/research/"
}
```

**Pros:**
- Purpose-built for agent definition
- Concise yet expressive
- Enforceable syntax rules
- Could include domain-specific validation
- Clean separation of concerns

**Cons:**
- Custom language requires custom tooling (parser, linter, IDE support)
- Learning curve for a novel DSL
- Maintenance burden of the DSL itself
- No ecosystem support
- Locks into a proprietary format
- Limited expressiveness for rich behavioral descriptions

**Feasibility:** Medium -- requires significant tooling investment
**Risk Level:** High -- custom DSL maintenance is a known liability

**Industry Evidence:** The AgentSLA DSL (2025) proposes a domain-specific language for agent service level agreements, extending ISO/IEC 25010. While promising for contractual specifications, DSLs for behavioral definition have historically struggled with adoption.

---

#### Alternative B5: Hybrid Schema-Validated Markdown

**Description:** Keep the YAML frontmatter + Markdown body pattern but add JSON Schema validation for the frontmatter and a required section checklist enforced by tooling. The body remains free-form Markdown but must contain required tagged sections.

**Pros:**
- Preserves all advantages of B1 (proven, human-readable, expressive)
- Adds schema validation for metadata correctness
- Section checklists catch structural omissions
- Backward-compatible with existing agent files
- Low migration cost from current pattern
- Tooling can be incremental (add validation gradually)

**Cons:**
- Still allows drift between metadata and body
- Schema must be maintained alongside agent definitions
- Section checklist enforcement needs CI integration
- Slightly more complex than pure B1

**Feasibility:** High -- incremental improvement on proven pattern
**Risk Level:** Low -- builds on existing infrastructure

**Industry Evidence:** Anthropic's own engineering blog emphasizes iterative improvement over revolutionary change. The Agent Spec standard uses JSON Schema for validation while allowing rich descriptions.

---

### Evaluation Matrix: Agent Definition Format

| Criterion (Weight) | B1: YAML+MD (Jerry) | B2: Pure YAML/JSON | B3: Code-First | B4: DSL | B5: Hybrid Validated |
|--------------------|---------------------|---------------------|----------------|---------|---------------------|
| C1: Simplicity (0.20) | 4 | 4 | 3 | 2 | 4 |
| C2: Flexibility (0.20) | 5 | 3 | 4 | 4 | 5 |
| C3: Maintainability (0.20) | 4 | 3 | 4 | 2 | 5 |
| C4: Quality Control (0.15) | 3 | 5 | 4 | 4 | 5 |
| C5: Context Efficiency (0.15) | 3 | 4 | 3 | 4 | 3 |
| C6: P-003 Compliance (0.10) | 5 | 5 | 4 | 5 | 5 |
| **Weighted Total** | **4.00** | **3.75** | **3.60** | **3.25** | **4.45** |

**Rank Order:** B5 (4.45) > B1 (4.00) > B2 (3.75) > B3 (3.60) > B4 (3.25)

**Finding:** The hybrid schema-validated Markdown approach (B5) scores highest by combining the expressiveness of the current YAML+MD pattern with the quality control benefits of schema validation. This is an evolutionary improvement, not a revolution.

---

## Trade Study 3: Agent Routing Architecture Alternatives

### Decision Context

**Problem Statement:** How should incoming requests be directed to the appropriate agent? The routing mechanism determines which specialist handles a given task.

**Driving Requirements:**
- H-22: Proactive skill invocation based on triggers
- Trigger map accuracy (keyword to skill mapping)
- Speed of routing decision
- Graceful handling of ambiguous or novel requests
- Support for multi-skill combinations

**Constraints:**
- Routing must not introduce recursive subagent patterns (P-003)
- Routing overhead consumes context window tokens
- Must handle the full trigger map in `mandatory-skill-usage.md`

### L1: Technical Alternatives

#### Alternative C1: Keyword Matching (Current Jerry Pattern)

**Description:** A static lookup table maps detected keywords to skills. When user input contains keywords like "research," "analyze," or "investigate," the corresponding skill (/problem-solving) is invoked. Currently defined in `mandatory-skill-usage.md`.

**Pros:**
- Deterministic and predictable
- Zero LLM overhead for routing
- Easy to audit and debug
- Fast -- immediate routing with no inference
- Transparent to users (documented keyword map)

**Cons:**
- Brittle -- synonyms and paraphrases not captured
- False positives from keyword collision (e.g., "risk" in casual conversation)
- No understanding of intent or context
- Requires manual maintenance as vocabulary grows
- Cannot handle novel or compound requests
- No confidence scoring

**Feasibility:** High -- already implemented
**Risk Level:** Medium -- brittleness increases with system complexity

**Industry Evidence:** Arize AI's agent routing research (2025) classifies keyword matching as the simplest but least flexible approach, noting it "lacks flexibility" for complex routing scenarios.

---

#### Alternative C2: Semantic Similarity Routing

**Description:** Each skill/agent has an embedding vector representing its capabilities. Incoming requests are embedded and matched against skill vectors using cosine similarity. The highest-similarity skill is selected.

**Pros:**
- Handles synonyms and paraphrases naturally
- No manual keyword maintenance
- Quantitative confidence scoring
- Scales with vocabulary without manual updates
- Can detect novel requests as low-similarity outliers

**Cons:**
- Requires embedding model infrastructure
- Latency overhead for embedding computation
- Training data needed for skill vectors
- Can produce surprising mismatches
- Harder to debug than keyword matching
- Embedding drift as agent capabilities evolve

**Feasibility:** Medium -- requires additional infrastructure
**Risk Level:** Medium -- embedding quality determines routing quality

**Industry Evidence:** AWS's multi-LLM routing research shows semantic routing can cut costs by up to 75% while maintaining quality, but notes the training data requirement as a significant investment.

---

#### Alternative C3: LLM-as-Router (Meta-Agent)

**Description:** A lightweight LLM call analyzes the user request and selects the appropriate skill/agent. The router LLM receives the full skill catalog and returns a routing decision.

**Pros:**
- Understands intent, not just keywords
- Handles compound and ambiguous requests
- Can provide routing explanation
- Adapts to novel request types
- Can combine multiple skills when appropriate (H-22 behavior rule 2)

**Cons:**
- Additional LLM call per routing decision (latency + cost)
- Router LLM can hallucinate routing decisions
- Skill catalog must fit in router's context window
- Stochastic -- same request may route differently
- Debugging requires understanding router's reasoning
- Could conflict with P-003 if router spawns subagents

**Feasibility:** High -- Claude can be used as its own router
**Risk Level:** Medium -- stochasticity is the main concern

**Industry Evidence:** LangChain's documentation identifies LLM-based routing as "state-of-the-art" but notes it "introduces another stochastic LLM call that needs to be managed." A thin router returning only a tool name (~3 tokens) can reduce response time from 5 seconds to ~300ms compared to ReACT-style agents.

---

#### Alternative C4: Rule-Based Decision Trees

**Description:** A structured decision tree evaluates multiple conditions (task type, complexity, domain, prior context) to select the appropriate skill. More sophisticated than keyword matching but still deterministic.

**Pros:**
- Deterministic and auditable
- Can encode complex routing logic
- Handles compound conditions (e.g., "research AND architecture")
- No LLM overhead
- Supports priority and fallback chains
- Natural fit for criticality-based routing (C1-C4 mapping)

**Cons:**
- Tree maintenance grows with system complexity
- Combinatorial explosion for many conditions
- Harder to author than keyword lists
- May miss novel patterns not in the tree
- Requires careful design to avoid dead branches

**Feasibility:** High -- standard programming pattern
**Risk Level:** Low -- deterministic behavior is predictable

**Industry Evidence:** Rule-based routing is the foundation of traditional expert systems and remains the recommended starting point for production agent systems (Arize AI, 2025). It is "straightforward to implement" but reaches diminishing returns as complexity grows.

---

#### Alternative C5: Layered Routing (Keyword + LLM Fallback)

**Description:** A two-tier routing strategy: (1) Fast keyword matching handles clear cases deterministically; (2) When keywords produce no match, low confidence, or multiple matches, an LLM-based router resolves the ambiguity.

**Pros:**
- Best of both worlds: speed for clear cases, intelligence for ambiguous ones
- Deterministic path for 80%+ of requests (based on keyword match rates)
- LLM fallback handles edge cases and novel requests
- Keyword tier is auditable; LLM tier provides flexibility
- Can log fallback frequency to identify keyword gaps
- Graceful degradation if LLM router is unavailable

**Cons:**
- Two-tier system is more complex to implement
- Must define the confidence threshold for fallback
- LLM fallback inherits C3's stochasticity concerns
- Monitoring needed to track keyword vs. fallback ratio
- May delay routing for borderline cases

**Feasibility:** High -- builds on existing keyword infrastructure
**Risk Level:** Low -- deterministic path for common cases, intelligent fallback for exceptions

**Industry Evidence:** This pattern is recommended by multiple sources: "A thin router returning only a tool name can be significantly faster" (medium.com routing analysis), while LLM fallback handles the long tail of ambiguous cases. Dynamic LLM routing "helps organizations save costs and improve efficiency by directing queries to the most suitable model."

---

#### Alternative C6: Intent Classification

**Description:** A dedicated intent classification model trained on historical routing decisions categorizes user requests into predefined intents. Each intent maps to one or more skills.

**Pros:**
- High accuracy when trained on representative data
- Fast inference (small classifier model)
- Confidence scoring built in
- Can detect out-of-distribution requests
- Improves over time with more training data

**Cons:**
- Requires labeled training data (cold start problem)
- Model training and maintenance overhead
- Intent taxonomy must be maintained
- New skills require retraining
- Overfits to historical patterns

**Feasibility:** Medium -- requires ML infrastructure and training data
**Risk Level:** Medium -- cold start and maintenance burden

**Industry Evidence:** Intent classification is standard in conversational AI (e.g., Rasa, Dialogflow) but is increasingly being displaced by LLM-based routing for agent systems due to LLMs' ability to handle open-ended intents without training data.

---

### Evaluation Matrix: Agent Routing Architecture

| Criterion (Weight) | C1: Keyword (Jerry) | C2: Semantic | C3: LLM-Router | C4: Decision Tree | C5: Layered | C6: Intent Classification |
|--------------------|---------------------|--------------|-----------------|--------------------|--------------|----|
| C1: Simplicity (0.20) | 5 | 3 | 3 | 4 | 3 | 2 |
| C2: Flexibility (0.20) | 2 | 4 | 5 | 3 | 5 | 3 |
| C3: Maintainability (0.20) | 4 | 3 | 3 | 3 | 3 | 2 |
| C4: Quality Control (0.15) | 3 | 3 | 3 | 4 | 4 | 4 |
| C5: Context Efficiency (0.15) | 5 | 4 | 2 | 5 | 4 | 4 |
| C6: P-003 Compliance (0.10) | 5 | 5 | 4 | 5 | 5 | 5 |
| **Weighted Total** | **3.85** | **3.45** | **3.35** | **3.80** | **3.90** | **3.10** |

**Rank Order:** C5 (3.90) > C1 (3.85) > C4 (3.80) > C2 (3.45) > C3 (3.35) > C6 (3.10)

**Finding:** Layered routing (C5) scores highest by a thin margin over keyword matching (C1). The key advantage is flexibility for edge cases while preserving deterministic routing for common cases. Decision trees (C4) are a strong alternative for teams that prefer fully deterministic routing.

---

## Trade Study 4: Quality Assurance Architecture Alternatives

### Decision Context

**Problem Statement:** How should agent output quality be enforced? The QA architecture must balance thoroughness against context window cost and execution time.

**Driving Requirements:**
- H-13: Quality threshold >= 0.92 for C2+ deliverables
- H-14: Creator-critic-revision cycle (minimum 3 iterations)
- H-15: Self-review before presenting (S-010)
- H-17: Quality scoring required for deliverables
- Criticality-proportional enforcement (C1-C4 levels)

### L1: Technical Alternatives

#### Alternative D1: Self-Review Only (S-010)

**Description:** Each agent applies S-010 Self-Refine before producing output. No external critic, no multi-pass revision. Quality relies entirely on the agent's self-assessment.

**Pros:**
- Minimal context window overhead
- Fastest execution (single pass + review)
- No agent coordination needed
- Simple to implement and understand

**Cons:**
- Limited by agent's own blind spots
- No independent perspective on quality
- Cannot reliably score against 6-dimension rubric
- Insufficient for C2+ deliverables per H-14
- Self-review bias: agents rate their own work more favorably

**Feasibility:** High -- already required by H-15
**Risk Level:** High for C2+ -- insufficient standalone quality mechanism

**Industry Evidence:** LangChain's State of Agent Engineering (2025) reports that quality is the #1 production blocker (32% of respondents), suggesting self-review alone is insufficient. Research shows leniency bias in self-assessment.

---

#### Alternative D2: Creator-Critic Pairs (Current Jerry Pattern for C2+)

**Description:** A creator agent produces the deliverable, a critic agent (e.g., ps-critic, adv-executor) evaluates it against quality criteria, and the creator revises. Minimum 3 iterations per H-14. Quality scored via S-014 LLM-as-Judge.

**Pros:**
- Independent perspective catches blind spots
- Structured feedback via 6-dimension rubric
- Quantitative scoring enables threshold enforcement (H-13)
- Proven pattern with established agents
- Criticality-proportional (more strategies for higher C-levels)
- Aligns with H-16 (Steelman before critique)

**Cons:**
- Significant context window cost (3+ full iterations)
- Latency from multiple agent invocations
- Critic may develop correlated blind spots over time
- Quality scoring can exhibit leniency bias (addressed in S-014)
- Complex orchestration for multi-strategy reviews

**Feasibility:** High -- already proven in Jerry
**Risk Level:** Low -- mature pattern with known mitigations

**Industry Evidence:** ACM's multi-agent QA methodology (2025) validates that multi-agent evaluation produces "more accurate and robust solutions." Human review remains essential for high-stakes decisions but LLM-as-judge scales assessments effectively.

---

#### Alternative D3: Full Tournament Mode (All Strategies)

**Description:** All 10 selected adversarial strategies (S-001 through S-014) are applied to every deliverable. Tournament scoring produces a comprehensive quality profile.

**Pros:**
- Maximum coverage of quality dimensions
- Multiple independent perspectives
- Tournament scoring reveals subtle issues
- Most rigorous quality assurance available

**Cons:**
- Extreme context window cost (10 strategy executions)
- Very high latency
- Diminishing returns beyond C3 deliverables
- Overkill for routine work
- Token budget may exceed context window

**Feasibility:** Medium -- feasible for C4 only
**Risk Level:** Low for quality; High for cost/latency

**Industry Evidence:** Research on multi-agent debate systems shows diminishing returns beyond 3-5 evaluation passes. Full tournament mode should be reserved for irreversible, high-impact decisions (C4 per Jerry's criticality matrix).

---

#### Alternative D4: Statistical Quality Monitoring

**Description:** Track quality scores over time across agents and deliverables. Use statistical process control (SPC) to detect quality degradation trends. Flag agents whose scores trend downward for review.

**Pros:**
- Detects systematic quality drift
- Low per-deliverable overhead (monitoring is async)
- Identifies underperforming agents or skills
- Data-driven improvement prioritization
- Early warning system for quality issues

**Cons:**
- Requires historical data accumulation (cold start)
- Does not prevent individual low-quality deliverables
- Statistical significance requires volume
- Infrastructure for score storage and analysis
- Complementary to, not replacement for, per-deliverable QA

**Feasibility:** Medium -- requires score persistence infrastructure
**Risk Level:** Low -- augments existing QA rather than replacing it

**Industry Evidence:** 89% of LLM agent deployments have implemented observability (LangChain State of Agent Engineering), but only 52% have implemented evals. Statistical monitoring bridges this gap.

---

#### Alternative D5: Output Schema Validation

**Description:** Agent outputs are validated against JSON Schema or structured templates before acceptance. Structural correctness is checked deterministically; content quality is checked via LLM scoring.

**Pros:**
- Deterministic check for structural compliance
- Catches missing sections, malformed metadata
- Zero LLM overhead for structural validation
- Fast feedback loop
- Complements LLM-based quality scoring
- Enforces H-23 (navigation tables), H-24 (anchor links)

**Cons:**
- Only validates structure, not content quality
- Schema must be maintained alongside templates
- Cannot assess reasoning quality, evidence strength
- False confidence if schema passes but content is poor
- Schema design is non-trivial for rich documents

**Feasibility:** High -- standard validation tooling
**Risk Level:** Low -- complements existing QA mechanisms

**Industry Evidence:** The Open Agent Specification uses JSON Schema for agent output validation. AgentSLA extends ISO/IEC 25010 quality model with agent-specific characteristics, validating that schema-based QA is gaining industry traction.

---

#### Alternative D6: Layered QA (Schema + Self-Review + Critic)

**Description:** Three-layer quality architecture: (1) Deterministic schema validation for structural compliance; (2) Self-review (S-010) for content quality; (3) Critic review with LLM-as-Judge scoring for C2+ deliverables. Each layer is proportional to criticality.

| Criticality | Layer 1 (Schema) | Layer 2 (Self-Review) | Layer 3 (Critic) |
|-------------|------------------|-----------------------|------------------|
| C1 | Required | Required | Optional |
| C2 | Required | Required | Required (3 iterations) |
| C3 | Required | Required | Required + strategies |
| C4 | Required | Required | Required + tournament |

**Pros:**
- Proportional cost to criticality
- Deterministic baseline catches structural issues fast
- Self-review catches obvious content issues
- Critic provides independent quality assessment for important work
- Aligns perfectly with existing H-13 through H-19 framework
- Schema validation is essentially free (no LLM cost)

**Cons:**
- Three-layer system is more complex to implement
- Schema development and maintenance effort
- Must coordinate validation results across layers
- Initial schema development is an upfront investment

**Feasibility:** High -- combines existing mechanisms with new schema layer
**Risk Level:** Low -- evolutionary improvement on proven patterns

**Industry Evidence:** The ACM multi-agent testing methodology (2025) recommends layered testing combining structural validation with behavioral evaluation. This mirrors the L3/L4/L5 enforcement architecture already in Jerry.

---

### Evaluation Matrix: Quality Assurance Architecture

| Criterion (Weight) | D1: Self-Review | D2: Creator-Critic (Jerry) | D3: Tournament | D4: Statistical | D5: Schema | D6: Layered QA |
|--------------------|-----------------|---------------------------|----------------|-----------------|------------|----------------|
| C1: Simplicity (0.20) | 5 | 3 | 1 | 3 | 4 | 2 |
| C2: Flexibility (0.20) | 2 | 4 | 5 | 3 | 2 | 5 |
| C3: Maintainability (0.20) | 5 | 3 | 2 | 3 | 4 | 3 |
| C4: Quality Control (0.15) | 2 | 4 | 5 | 3 | 3 | 5 |
| C5: Context Efficiency (0.15) | 5 | 2 | 1 | 4 | 5 | 3 |
| C6: P-003 Compliance (0.10) | 5 | 5 | 4 | 5 | 5 | 5 |
| **Weighted Total** | **3.85** | **3.30** | **2.70** | **3.25** | **3.60** | **3.70** |

**Rank Order:** D1 (3.85) > D6 (3.70) > D5 (3.60) > D2 (3.30) > D4 (3.25) > D3 (2.70)

**Nuanced Finding:** Self-review (D1) scores highest on raw weighted score due to simplicity and efficiency, but it is **insufficient for C2+ deliverables** per H-14. When the H-14 constraint is applied as a filter (C2+ deliverables MUST have critic review), the effective ranking for C2+ work becomes: D6 (3.70) > D2 (3.30) > D3 (2.70). For C1 work, D1 (3.85) with optional D5 (schema validation) is the recommended combination.

---

## Trade Study 5: Tool Integration Architecture Alternatives

### Decision Context

**Problem Statement:** How should agents discover, access, and use external tools? The tool integration architecture determines how agents interact with MCP servers, file systems, web APIs, and other capabilities.

**Driving Requirements:**
- MCP-001: Context7 MUST be used for external library research
- MCP-002: Memory-Keeper MUST be used at phase boundaries
- Agent-specific tool permissions (different agents get different tools)
- Tool access must be auditable
- P-003: Tool use must not create recursive subagent patterns

**Constraints:**
- MCP servers must be pre-configured
- Tool schemas consume context window tokens
- Agent definitions must declare allowed tools

### L1: Technical Alternatives

#### Alternative E1: Static Tool Assignment Per Agent (Current Jerry Pattern)

**Description:** Each agent definition declares its `allowed_tools` in YAML frontmatter. Tools are fixed at agent definition time. The TOOL_REGISTRY.yaml is the SSOT for tool-to-agent mappings.

**Pros:**
- Predictable tool access per agent
- Easy to audit (read the frontmatter)
- Minimal context overhead (only declared tools loaded)
- Clear security boundary per agent
- Aligns with principle of least privilege
- Registry provides centralized governance

**Cons:**
- Adding a tool to an agent requires editing the definition
- Cannot adapt to novel tool requirements at runtime
- May over-provision or under-provision tools
- Tool capability changes require definition updates
- New MCP servers require manual agent-by-agent updates

**Feasibility:** High -- already implemented
**Risk Level:** Low -- predictable and auditable

**Industry Evidence:** MCP specification (2025-11-25) supports static tool capability declaration via server capabilities. This is the recommended pattern for production deployments with governance requirements.

---

#### Alternative E2: Dynamic Tool Selection Based on Task

**Description:** Agents discover available tools at runtime and select which ones to use based on the current task. The LLM decides which tools are relevant from the full tool catalog.

**Pros:**
- Adapts to any task without definition changes
- New tools are automatically available
- No manual tool-agent mapping maintenance
- Maximum flexibility for novel tasks

**Cons:**
- Full tool catalog in context consumes tokens
- Tool selection is stochastic (LLM may choose wrong tools)
- Security model is weakened (any agent can use any tool)
- Auditing is harder (tool usage is non-deterministic)
- Conflicts with principle of least privilege
- P-003 risk: LLM may attempt to use Task tool for recursive spawning

**Feasibility:** Medium -- requires careful guardrailing
**Risk Level:** High -- security and auditability concerns

**Industry Evidence:** Claude Code's own design allows dynamic tool selection within a bounded set, but Anthropic recommends explicit tool configuration for production use cases.

---

#### Alternative E3: Capability-Based Tool Matching

**Description:** Tools declare their capabilities via structured metadata (e.g., "can search web," "can read files," "can store state"). Agents declare needed capabilities (e.g., "needs web search," "needs state persistence"). A matching engine connects agents to tools based on capability alignment.

**Pros:**
- Decouples agents from specific tool implementations
- Tool substitution without agent changes (swap one search tool for another)
- Capability declarations serve as documentation
- Natural fit for MCP's capability declaration model
- Future-proof: new tools auto-match if capabilities align

**Cons:**
- Capability taxonomy must be maintained
- Matching logic adds complexity
- Capability descriptions may not capture tool nuances
- Over-abstraction risk: agents lose awareness of specific tool features
- Initial capability taxonomy design is non-trivial

**Feasibility:** Medium -- requires capability taxonomy and matching engine
**Risk Level:** Medium -- abstraction layer may obscure tool specifics

**Industry Evidence:** MCP's server capabilities interface (listing tools, resources, prompts) naturally supports capability-based discovery. The spec includes `tools/list` for runtime tool discovery and `listChanged` notifications for dynamic updates.

---

#### Alternative E4: MCP-Based Tool Federation

**Description:** All tools are accessed through MCP servers. Agents connect to MCP servers, discover available tools via the standard protocol, and invoke tools through JSON-RPC 2.0. Multiple MCP servers can provide different tool categories.

**Pros:**
- Industry-standard protocol (MCP adopted by Anthropic, OpenAI, Google)
- Clean separation between tool definition and tool implementation
- Tool discovery via `tools/list` endpoint
- Standardized error handling and response format
- Cross-platform compatibility
- Tool providers can evolve independently

**Cons:**
- Requires MCP server infrastructure
- Network overhead for tool invocation
- MCP server availability becomes a dependency
- Tool schema negotiation adds latency
- Current MCP ecosystem is still maturing
- Not all tools map cleanly to MCP (e.g., file system operations)

**Feasibility:** High -- MCP is already integrated in Jerry
**Risk Level:** Low -- industry standard with broad adoption

**Industry Evidence:** MCP is described as the "USB-C port for AI applications" (Anthropic, 2024). The November 2025 spec release added tasks support, and enterprise teams are deploying MCP at scale with security and governance controls. The Agentic AI Foundation (AAIF, December 2025) by Anthropic, OpenAI, and Block further validates MCP as the standard.

---

#### Alternative E5: Hybrid Static + MCP Federation

**Description:** Core tools (Read, Write, Edit, Glob, Grep, Bash) are statically assigned per agent. Extended tools (Context7, Memory-Keeper, future integrations) are accessed via MCP federation. Each agent declares both static tools and MCP server connections.

**Pros:**
- Core tools are fast (no network overhead)
- Extended tools leverage MCP standard
- Clear distinction between local and remote capabilities
- New MCP servers add capability without agent redefinition
- Backward-compatible with existing tool assignments
- Governance: static tools are tightly controlled, MCP tools have federation governance

**Cons:**
- Two integration patterns to maintain
- Must define which tools are "core" vs. "extended"
- MCP server management for extended tools
- Slightly more complex than pure static assignment

**Feasibility:** High -- natural evolution of current pattern
**Risk Level:** Low -- builds on proven infrastructure

**Industry Evidence:** This is essentially Jerry's current trajectory. Claude Code itself uses static built-in tools plus MCP for extended capabilities. This pattern is validated by Anthropic's own architecture.

---

### Evaluation Matrix: Tool Integration Architecture

| Criterion (Weight) | E1: Static (Jerry) | E2: Dynamic | E3: Capability-Based | E4: MCP Federation | E5: Hybrid Static+MCP |
|--------------------|---------------------|-------------|---------------------|---------------------|----------------------|
| C1: Simplicity (0.20) | 5 | 3 | 2 | 3 | 4 |
| C2: Flexibility (0.20) | 2 | 5 | 4 | 4 | 4 |
| C3: Maintainability (0.20) | 4 | 2 | 3 | 4 | 4 |
| C4: Quality Control (0.15) | 5 | 2 | 3 | 4 | 4 |
| C5: Context Efficiency (0.15) | 5 | 2 | 3 | 3 | 4 |
| C6: P-003 Compliance (0.10) | 5 | 3 | 5 | 5 | 5 |
| **Weighted Total** | **4.15** | **2.90** | **3.05** | **3.70** | **4.10** |

**Rank Order:** E1 (4.15) > E5 (4.10) > E4 (3.70) > E3 (3.05) > E2 (2.90)

**Finding:** Static assignment (E1) and hybrid static+MCP (E5) score nearly identically. The hybrid approach trades a marginal amount of simplicity for significantly better flexibility and future-proofing. For Jerry's trajectory, E5 is the recommended direction as MCP adoption grows.

---

## L2: Cross-Cutting Architecture Analysis

### Strategic Trade-Off Analysis

The five trade studies reveal three cross-cutting themes that inform the overall architecture:

#### Theme 1: Determinism vs. Intelligence

Across routing (C1 vs. C3), quality (D5 vs. D2), and tool integration (E1 vs. E2), there is a consistent tension between deterministic approaches (predictable, auditable, efficient) and intelligent approaches (flexible, adaptive, context-aware). The winning pattern in every trade study is a **layered hybrid** that uses deterministic mechanisms as the fast path and intelligent mechanisms as the fallback.

| Dimension | Deterministic Layer | Intelligent Layer |
|-----------|--------------------|--------------------|
| Routing | Keyword matching (C1) | LLM fallback (C3) |
| Quality | Schema validation (D5) | Creator-critic scoring (D2) |
| Tools | Static assignment (E1) | MCP federation (E4) |

**Architecture Principle:** Prefer deterministic mechanisms for common cases; reserve LLM-based intelligence for ambiguous or novel situations.

#### Theme 2: Context Window as Scarce Resource

Context window is Jerry's scarcest resource (200K tokens). Every architectural decision must be evaluated for context cost:

| Pattern | Context Cost | Value |
|---------|-------------|-------|
| Monolithic agent definitions | Very High | Low (context rot) |
| Per-agent tool schemas | High | Medium (flexibility) |
| Tournament QA (10 strategies) | Very High | High (quality) but diminishing |
| Keyword routing | Zero | Medium (deterministic) |
| Schema validation | Zero | Medium (structural quality) |
| Progressive disclosure | Negative (saves tokens) | High |

**Architecture Principle:** Invest context tokens proportional to criticality level. C1 work gets minimal context overhead; C4 work justifies full tournament mode.

#### Theme 3: Evolutionary Over Revolutionary

Every trade study shows that Jerry's existing patterns are architecturally sound and rank in the top 2 across all dimensions. The highest-value improvements are evolutionary enhancements, not architectural rewrites:

| Current Pattern | Evolutionary Enhancement | Estimated Value |
|----------------|--------------------------|-----------------|
| YAML+MD agent definitions (B1) | Add schema validation (B5) | High |
| Keyword routing (C1) | Add LLM fallback for ambiguous cases (C5) | Medium-High |
| Creator-critic QA (D2) | Add schema pre-check layer (D6) | Medium |
| Static tool assignment (E1) | Extend with MCP federation (E5) | Medium |
| Skill-based architecture (A3) | Strengthen state management protocol | Medium |

### Lifecycle Implications

| Alternative Cluster | Development Cost | Operations Cost | Maintenance Cost | Migration Risk |
|---------------------|------------------|-----------------|------------------|----------------|
| Current Jerry patterns (as-is) | None | Low | Medium | None |
| Evolutionary enhancements (recommended) | Medium | Low | Low | Low |
| Revolutionary rewrite (e.g., DSL, event-driven) | High | High | High | High |

### Risk Comparison

| Risk Category | Current Patterns | Evolutionary Path | Revolutionary Path |
|---------------|-----------------|--------------------|--------------------|
| Technical Risk | Low | Low | High |
| Schedule Risk | None | Low | High |
| Quality Risk | Medium (no schema validation) | Low | Medium |
| Adoption Risk | None | Low | High |
| Context Rot Risk | Medium | Low (schema validation helps) | High (new patterns to learn) |

### Recommendation Framework

The following decision criteria should guide the selection:

**Select the evolutionary enhancement path IF:**
- The team values stability and incremental improvement
- Context efficiency is a priority (it is -- this is Jerry's core problem)
- Existing patterns are working well (they are -- 37 agents in production)
- Migration risk tolerance is low

**Select the revolutionary rewrite path IF:**
- The existing pattern has fundamental limitations (it does not)
- Scale is expected to increase 10x+ in near term
- New foundational capabilities are needed (e.g., multi-model support)

**Based on this analysis, the evolutionary enhancement path is strongly recommended.** The current Jerry patterns score highest in 4 of 5 trade studies and are within the top 2 in all 5. The recommended enhancements (schema validation, layered routing, layered QA, hybrid tool integration) are additive improvements that do not disrupt the proven architecture.

### Recommended Priority for Enhancements

| Priority | Enhancement | Trade Study | Impact | Effort |
|----------|-------------|-------------|--------|--------|
| 1 | Schema validation for agent definitions (B5) | TS-2 | High | Low |
| 2 | Schema validation for agent outputs (D6) | TS-4 | High | Medium |
| 3 | Layered routing with LLM fallback (C5) | TS-3 | Medium-High | Medium |
| 4 | Standardized state management across handoffs | TS-1 | Medium | Medium |
| 5 | MCP federation for extended tools (E5) | TS-5 | Medium | Low (already underway) |

---

## Assumptions Challenged

| # | Original Assumption | Challenge | Result |
|---|---------------------|-----------|--------|
| 1 | "More agent specialization is always better" | At what point does adding specialists create coordination overhead that exceeds the benefit of specialization? | 37 agents appears to be near the practical limit for single-framework cognitive load. Beyond ~50 agents, team-based grouping (A5) should be reconsidered. |
| 2 | "LLM-based routing is always superior to keywords" | What is the actual accuracy gap, and does it justify the latency and stochasticity costs? | For Jerry's well-defined trigger map, keyword matching handles ~80% of cases correctly. LLM routing adds value primarily for the remaining 20% of ambiguous cases. |
| 3 | "Tournament mode provides the highest quality" | Is there a point of diminishing returns in adversarial strategy count? | Research suggests diminishing returns beyond 3-5 evaluation passes. Full tournament (10 strategies) is justified only for C4 deliverables. |
| 4 | "Code-first agent definitions are more maintainable than markdown" | Does type safety compensate for the loss of natural language expressiveness? | For behavioral specifications (persona, cognitive mode), natural language remains more expressive than code. Type safety adds value for tool declarations and guardrails but not for behavioral narrative. |
| 5 | "Event-driven architecture is the future for agent systems" | Does EDA's loose coupling benefit map to single-context-window LLM systems? | No. EDA is designed for distributed systems with independent processes. Single-context LLM agents benefit more from structured handoff protocols than event buses. |
| 6 | "Dynamic tool selection is more flexible than static assignment" | Does the flexibility outweigh the security and auditability costs? | For governed systems (like Jerry), static assignment with MCP extension provides sufficient flexibility without sacrificing the principle of least privilege. |

---

## Open Questions

| # | Question | Impact | Suggested Resolution |
|---|----------|--------|---------------------|
| 1 | What is the optimal schema format for agent definition validation -- JSON Schema, Pydantic, or YAML Schema? | Affects B5 implementation | Prototype with JSON Schema (widest tooling support); evaluate Pydantic if Python integration is needed |
| 2 | What confidence threshold should trigger LLM fallback in layered routing (C5)? | Affects C5 implementation | Empirically determine by logging keyword match confidence for 100+ real routing decisions |
| 3 | How should agent output schemas handle the variability between L0/L1/L2 output levels? | Affects D6 implementation | Define a base schema with optional level-specific sections; validate presence of all three levels |
| 4 | What is the actual keyword match accuracy rate for Jerry's current trigger map? | Informs C5 cost-benefit | Instrument current routing to log matches and mismatches for 2-4 weeks |
| 5 | Should the Open Agent Specification (Agent Spec) be adopted as a baseline for Jerry's agent definition format? | Affects B5 direction | Evaluate Agent Spec for compatibility with Jerry's YAML+MD pattern; adopt compatible elements |
| 6 | How should state management between agents be standardized beyond the current session_context schema? | Affects A3 enhancement | Evaluate LangGraph's TypedDict state model for structured state; consider adopting a similar pattern |
| 7 | What is the maximum agent count before team-based grouping (A5) becomes necessary? | Affects A3 scaling | Monitor coordination overhead as agent count grows; establish 50-agent threshold for reevaluation |

---

## References

### Web Sources

1. [SuperAGI - Microservices vs Monolithic Architecture for Agent Orchestration](https://superagi.com/microservices-vs-monolithic-architecture-a-comparison-of-agent-orchestration-frameworks/) -- Key insight: architectural comparison of agent orchestration approaches
2. [TNGlobal - Beware the Distributed Monolith: Why Agentic AI Needs EDA](https://technode.global/2025/09/22/beware-the-distributed-monolith-why-agentic-ai-needs-event-driven-architecture-to-avoid-a-repeat-of-the-microservices-disaster/) -- Key insight: event-driven architecture for agent systems
3. [Digital Thought Disruption - Agentic AI Architecture: Modular Design Patterns](https://digitalthoughtdisruption.com/2025/07/31/agentic-ai-architecture-modular-design-patterns/) -- Key insight: modular agent design best practices
4. [Open Agent Specification Technical Report](https://arxiv.org/html/2510.04173v1) -- Key insight: unified agent workflow definition standard
5. [AgentSLA DSL for AI Agent Service Level Agreements](https://arxiv.org/html/2511.02885) -- Key insight: DSL approach to agent quality specification
6. [Open Standards for AI Agents: A2A, MCP, LangChain, AGNTCY Comparison](https://jtanruan.medium.com/open-standards-for-ai-agents-a-technical-comparison-of-a2a-mcp-langchain-agent-protocol-and-482be1101ad9) -- Key insight: protocol landscape for agent interoperability
7. [IBM - Agent2Agent (A2A) Protocol](https://www.ibm.com/think/topics/agent2agent-protocol) -- Key insight: Google's inter-agent communication standard
8. [FME - AI Agent Routing: Tutorial and Examples](https://fme.safe.com/guides/ai-agent-architecture/ai-agent-routing/) -- Key insight: routing architecture taxonomy
9. [Patronus AI - AI Agent Routing: Best Practices](https://www.patronus.ai/ai-agent-development/ai-agent-routing) -- Key insight: routing implementation patterns
10. [Medium - Rethinking AI Agents: Why a Simple Router May Be All You Need](https://medium.com/@tannermcrae/rethinking-ai-agents-why-a-simple-router-may-be-all-you-need-c95031c2d397) -- Key insight: thin router performance benefits (300ms vs 5s)
11. [Arize AI - Best Practices for Building an Agent Router](https://arize.com/blog/best-practices-for-building-an-ai-agent-router/) -- Key insight: function calling vs. rule-based vs. ML routing comparison
12. [AWS - Multi-LLM Routing Strategies](https://aws.amazon.com/blogs/machine-learning/multi-llm-routing-strategies-for-generative-ai-applications-on-aws/) -- Key insight: dynamic routing can cut costs by 75%
13. [ACM - Methodology for QA Testing of LLM-based Multi-Agent Systems](https://dl.acm.org/doi/full/10.1145/3703412.3703439) -- Key insight: multi-agent evaluation methodology
14. [Zyrix - Multi-Agent AI Testing Guide 2025](https://zyrix.ai/blogs/multi-agent-ai-testing-guide-2025/) -- Key insight: LLM QA framework patterns
15. [LangChain - State of Agent Engineering](https://www.langchain.com/state-of-agent-engineering) -- Key insight: quality is #1 production blocker (32%); 89% have observability
16. [Anthropic - Claude Code Best Practices for Agentic Coding](https://www.anthropic.com/engineering/claude-code-best-practices) -- Key insight: CLAUDE.md as configuration, multi-agent coordination patterns
17. [Anthropic - Building Agents with the Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk) -- Key insight: context management, tool design, compact feature
18. [Anthropic - Equipping Agents with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) -- Key insight: skills as composable agent capabilities
19. [DataCamp - CrewAI vs LangGraph vs AutoGen Comparison](https://www.datacamp.com/tutorial/crewai-vs-langgraph-vs-autogen) -- Key insight: role-based vs. graph-based vs. conversational architectures
20. [O-Mega - LangGraph vs CrewAI vs AutoGen: Top 10 AI Agent Frameworks](https://o-mega.ai/articles/langgraph-vs-crewai-vs-autogen-top-10-agent-frameworks-2026) -- Key insight: 2026 framework landscape
21. [Turing - Detailed Comparison of Top 6 AI Agent Frameworks 2026](https://www.turing.com/resources/ai-agent-frameworks) -- Key insight: framework selection criteria
22. [PromptHub - Role-Prompting: Does Adding Personas Really Make a Difference?](https://www.prompthub.us/blog/role-prompting-does-adding-personas-to-your-prompts-really-make-a-difference) -- Key insight: persona prompting effectiveness is mixed for factual tasks
23. [Context Engineering Deep Dive - Prompt Engineering Guide](https://www.promptingguide.ai/agents/context-engineering-deep-dive) -- Key insight: context engineering for research agents
24. [MCP Specification 2025-11-25](https://modelcontextprotocol.io/specification/2025-06-18) -- Key insight: tool capability declaration, discovery, invocation protocols
25. [Anthropic - Introducing the Model Context Protocol](https://www.anthropic.com/news/model-context-protocol) -- Key insight: MCP as open standard for AI tool integration
26. [Microsoft - AI Coding Agents and Domain-Specific Languages](https://devblogs.microsoft.com/all-things-azure/ai-coding-agents-domain-specific-languages/) -- Key insight: DSL challenges for AI agent coding

### Context7 Sources

27. Context7 `/websites/modelcontextprotocol_io_specification_2025-11-25` -- MCP server capabilities, tool listing, tool invocation, and sampling with tools protocols
28. Context7 `/websites/langchain_oss_python_langgraph` -- LangGraph orchestrator-worker pattern, graph API state management, conditional edges, `Send()` for parallel execution

### Codebase Sources

29. `/Users/anowak/workspace/github/jerry-wt/feat/proj-007-agent-patterns/AGENTS.md` -- Jerry agent registry (37 agents, 8 skills)
30. `/Users/anowak/workspace/github/jerry-wt/feat/proj-007-agent-patterns/skills/problem-solving/agents/ps-researcher.md` -- Example agent definition (YAML+MD, 615 lines)
31. `/Users/anowak/workspace/github/jerry-wt/feat/proj-007-agent-patterns/skills/nasa-se/agents/nse-explorer.md` -- Example agent definition (trade study methodology)
32. `/Users/anowak/workspace/github/jerry-wt/feat/proj-007-agent-patterns/.context/rules/mandatory-skill-usage.md` -- Trigger map and routing rules
33. `/Users/anowak/workspace/github/jerry-wt/feat/proj-007-agent-patterns/.context/rules/mcp-tool-standards.md` -- MCP governance rules
34. `/Users/anowak/workspace/github/jerry-wt/feat/proj-007-agent-patterns/.context/rules/quality-enforcement.md` -- Quality gate, criticality levels, strategy catalog

---

*Generated by nse-explorer agent v2.1.0*
*NASA Process: NPR 7123.1D Process 17 (Decision Analysis)*
*Self-Review (S-010) Applied: Completeness verified across all 5 exploration areas, trade matrices complete, L0/L1/L2 present*
