# Jerry Framework - Expanded Discoveries Catalog

> **Purpose:** Comprehensive discovery documentation following PS-EXPORT-SPECIFICATION v2.1
> **Format:** L0 (ELI5) / L1 (Software Engineer) / L2 (Principal Architect)
> **Created:** 2026-01-08
> **Session:** claude/create-code-plugin-skill-MG1nh

---

## Phase 0: Research & Analysis Discoveries

### DISC-001: Context Rot Threshold

**ID:** DISC-001
**Slug:** context-rot-threshold
**Name:** Context Rot Threshold at ~256k Tokens
**Short Description:** LLM performance degrades as context fills, even within technical limits; ~256k tokens is practical ceiling.

**Long Description:**
Chroma Research identified "context rot" as a phenomenon where LLM accuracy degrades significantly as the context window fills, even when total token count is well within the advertised technical limit. Their research shows that at approximately 256k tokens, performance degradation becomes severe enough to impact practical applications. This has direct implications for Jerry's design - the framework must offload state to the filesystem rather than rely on in-context memory.

**Evidence:**
- [Chroma Research: Context Rot](https://research.trychroma.com/context-rot)
- Observed in Claude, GPT-4, and other models

**Level Impact:**
- **L0:** AI gets confused when you give it too much to remember at once, even if it says it can handle more
- **L1:** Design systems that persist state to files; use Work Tracker for task continuity across sessions
- **L2:** Implement filesystem-as-memory architecture; context is expensive, storage is cheap

---

### DISC-002: MCP Python SDK Available

**ID:** DISC-002
**Slug:** mcp-python-sdk
**Name:** Model Context Protocol Has Official Python SDK
**Short Description:** Anthropic provides official Python SDK for MCP, enabling native Python server development.

**Long Description:**
The Model Context Protocol (MCP) provides a standardized way to build context servers for LLMs. Anthropic released an official Python SDK (`mcp`) alongside the TypeScript reference implementation. This validates the decision to use Python for Jerry's core - MCP servers can be implemented in Python without requiring TypeScript/Node.js dependencies.

**Evidence:**
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP Specification](https://spec.modelcontextprotocol.io/)

**Level Impact:**
- **L0:** We can build the special helper tools in Python, not JavaScript
- **L1:** Implement MCP servers in Python using `mcp` package; no polyglot required
- **L2:** MCP enables standardized tool interfaces; consider MCP for Work Tracker queries

---

### DISC-003: Hexagonal Enables Polyglot

**ID:** DISC-003
**Slug:** hexagonal-polyglot-adapters
**Name:** Hexagonal Architecture Enables Polyglot Adapters
**Short Description:** Port-and-adapter pattern allows language-specific adapters without domain contamination.

**Long Description:**
Hexagonal Architecture (Ports & Adapters) naturally supports polyglot implementations. The domain layer remains pure Python with no external dependencies, while adapters in the infrastructure layer can be implemented in any language that can communicate with the domain (via ports). This means TypeScript could be used for network-facing adapters (e.g., MCP servers, API gateways) while keeping business logic in Python.

**Evidence:**
- [Alistair Cockburn: Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/)
- Standard DDD practice

**Level Impact:**
- **L0:** The inside of the app speaks Python, but the outside can speak any language
- **L1:** Define ports as Python protocols; implement adapters in Python first, TypeScript if needed later
- **L2:** Enables future flexibility without rewriting core; defer polyglot decision until proven necessary

---

## Phase 2.5: Deep Analysis Discoveries

### DISC-004: Small Aggregates Principle

**ID:** DISC-004
**Slug:** small-aggregates-principle
**Name:** 70% of Aggregate Roots Are Single Entity + Value Objects
**Short Description:** Vernon's research shows most ARs should be small; large ARs cause performance issues.

**Long Description:**
Vaughn Vernon's "Implementing Domain-Driven Design" presents research showing that approximately 70% of aggregate roots in well-designed systems consist of a single entity plus value objects. Large aggregates that attempt to encapsulate entire object graphs cause: (1) contention/locking issues, (2) poor performance on updates, (3) difficulty in testing. This directly informed Jerry's decision to use Task as the primary small AR rather than Plan (large) or Phase (medium).

**Evidence:**
- Vernon, V. (2013). *Implementing Domain-Driven Design*. Addison-Wesley.
- Evans, E. (2003). *Domain-Driven Design*. Addison-Wesley.

**Level Impact:**
- **L0:** Smaller boxes of related stuff work better than giant boxes with everything
- **L1:** Design Task AR with ~5 entities max; use references (IDs) to related aggregates
- **L2:** Apply invariant-boundary heuristic: AR boundary should match consistency boundary, not convenience

---

### DISC-005: Task as Primary AR

**ID:** DISC-005
**Slug:** task-primary-aggregate-root
**Name:** Task Should Be Primary Aggregate Root
**Short Description:** Based on Vernon's ProjectOvation case study, Task (not Plan/Phase) should be the primary AR.

**Long Description:**
Vernon's ProjectOvation example in "Implementing DDD" demonstrates a project management domain where BacklogItem (analogous to Task) is the primary aggregate root, not Project or Sprint. The reasoning: BacklogItem is the unit of work, has its own lifecycle, and is the primary target of commands. Project and Sprint reference collections of BacklogItem IDs. This pattern directly applies to Jerry's Work Tracker.

**Evidence:**
- Vernon, V. (2013). *Implementing Domain-Driven Design*, Chapter 10.
- ProjectOvation case study

**Level Impact:**
- **L0:** The individual task is the star of the show, not the big project plan
- **L1:** Implement Task.create(), Task.complete(), Task.add_subtask() as primary operations
- **L2:** Phase and Plan become reference-holders with eventual consistency; task events drive state changes

---

### DISC-006: ECW Plan AR Performance

**ID:** DISC-006
**Slug:** ecw-plan-ar-slow
**Name:** ECW Plan AR Caused Performance Issues
**Short Description:** User confirmed that ECW's Plan-as-primary-AR design caused noticeable slowness.

**Long Description:**
During analysis of ECW artifacts, the user explicitly confirmed that the Plan-centric aggregate root design caused performance problems in practice. The Plan AR in ECW contained deep object graphs (Plan → Phases → Tasks → Subtasks), requiring loading the entire graph for any operation. This validates the decision to restructure with Task as primary AR and use eventual consistency for Plan/Phase state.

**Evidence:**
- User feedback in session
- ECW v3 lesson: "Plan AR too large"

**Level Impact:**
- **L0:** Loading the whole project plan every time was too slow
- **L1:** Never load Plan with all children; use lazy loading or ID references
- **L2:** Plan AR contains phase_ids: List[PhaseId], not phases: List[Phase]; projections derive state

---

### DISC-007: ECW Phase AR Also Slow

**ID:** DISC-007
**Slug:** ecw-phase-ar-slow
**Name:** ECW Phase AR Also Caused Performance Issues
**Short Description:** User confirmed Phase-as-AR still had performance issues, though less severe than Plan.

**Long Description:**
Following the Plan AR discussion, user confirmed that even Phase-as-primary-AR showed performance issues in ECW, though less severe. Phases containing Task object graphs still required substantial data loading. This reinforces the decision to make Task the primary AR, with Phase and Plan as secondary ARs holding only references (task_ids, phase_ids) and deriving state through projections.

**Evidence:**
- User feedback in session
- ECW iteration history

**Level Impact:**
- **L0:** Even medium-sized groupings were too slow; individual tasks work best
- **L1:** Phase AR contains task_ids: List[TaskId], derives progress from projections
- **L2:** Eventual consistency between Task→Phase→Plan via domain events; no immediate consistency needed

---

### DISC-008: CloudEvents Required

**ID:** DISC-008
**Slug:** cloudevents-required
**Name:** CloudEvents 1.0 Is Hard Requirement
**Short Description:** User mandated CloudEvents 1.0 spec for all domain events in Jerry.

**Long Description:**
The user explicitly stated CloudEvents as a hard requirement for Jerry. CloudEvents 1.0 is a CNCF specification for describing events in a common way. It provides: (1) standard envelope with required attributes (id, source, type, time), (2) extension mechanism for custom attributes, (3) multiple protocol bindings (HTTP, AMQP, Kafka), (4) JSON schema for validation. All Jerry domain events must conform to CloudEvents 1.0.

**Evidence:**
- [CloudEvents Specification 1.0](https://cloudevents.io/)
- CNCF Incubating Project
- User requirement

**Level Impact:**
- **L0:** All messages between parts of the system must follow a specific "envelope" format
- **L1:** Implement CloudEvent base class with id, source, specversion, type, time; extend for domain events
- **L2:** CloudEvents enables interoperability; events can be consumed by external systems unchanged

---

### DISC-009: Strongly Typed IDs Required

**ID:** DISC-009
**Slug:** strongly-typed-ids
**Name:** Strongly Typed Identity Objects Are Hard Requirement
**Short Description:** User mandated strongly typed IDs (TaskId, PhaseId) rather than raw UUID/GUID.

**Long Description:**
The user explicitly required strongly typed identity objects instead of raw UUID/string identifiers. This is a DDD best practice that prevents accidental ID mixing (passing PhaseId where TaskId expected). Strongly typed IDs also enable: (1) validation at construction, (2) type-safe repository methods, (3) IDE autocomplete, (4) self-documenting code. In Jerry, all IDs extend VertexId for graph compatibility.

**Evidence:**
- Evans, E. (2003). *Domain-Driven Design*. Chapter on Value Objects.
- Vernon, V. (2013). *Implementing DDD*. Identity chapter.
- User requirement

**Level Impact:**
- **L0:** Each type of ID has its own label so you can't mix them up
- **L1:** Create TaskId, PhaseId, PlanId classes extending VertexId; use in method signatures
- **L2:** Compile-time safety for identity handling; impossible to pass wrong ID type

---

### DISC-010: ECW 108+ Use Cases

**ID:** DISC-010
**Slug:** ecw-use-cases-documented
**Name:** ECW v3 Had 108+ Documented Use Cases
**Short Description:** ECW's glimmering-brewing-lake artifact contains 108+ use cases as reference material.

**Long Description:**
Analysis of ECW's knowledge artifacts revealed extensive use case documentation in the glimmering-brewing-lake series. These 108+ use cases cover: work management, knowledge capture, identity & access, and reporting bounded contexts. While Jerry is a fresh implementation, these use cases serve as reference material for feature discovery and edge case identification.

**Evidence:**
- `docs/knowledge/dragonsbelurkin/glimmering-brewing-lake.md`
- ECW v3 documentation archive

**Level Impact:**
- **L0:** The previous project documented over 100 different things the system should do
- **L1:** Reference ECW use cases during feature design; don't reinvent without checking prior work
- **L2:** ECW use cases inform bounded context boundaries and aggregate responsibilities

---

### DISC-011: Blackboard Pattern for LLM Agents

**ID:** DISC-011
**Slug:** blackboard-pattern-llm
**Name:** Blackboard Pattern Shows 13-57% Improvement Over Master-Slave
**Short Description:** Research shows blackboard architecture outperforms master-slave for LLM agent orchestration.

**Long Description:**
ECW lessons learned and academic research indicate that the Blackboard Pattern (shared workspace with opportunistic problem-solving) outperforms master-slave architectures for LLM agent coordination. In master-slave, a central controller becomes a bottleneck and single point of failure. Blackboard allows agents to contribute asynchronously, with improvement ranges of 13-57% depending on task complexity and parallelism potential.

**Evidence:**
- ECW_COMPREHENSIVE_LESSONS_LEARNED.md
- Academic research on multi-agent systems

**Level Impact:**
- **L0:** Instead of one boss telling everyone what to do, agents share a common "whiteboard" and help when they can
- **L1:** Design agent orchestration with shared state (filesystem/database) rather than direct agent-to-agent calls
- **L2:** Blackboard enables horizontal scaling and resilience; agents can fail without blocking others

---

### DISC-012: Hook Subprocess Isolation (LES-030)

**ID:** DISC-012
**Slug:** hook-subprocess-isolation
**Name:** Hooks Cannot Access MCP Context
**Short Description:** Claude Code hooks run as subprocesses without access to MCP tools or parent context.

**Long Description:**
LES-030 from ECW documents a critical constraint: Claude Code hooks (pre/post tool use, subagent stop) execute as isolated subprocesses. They cannot access MCP servers, cannot use Claude Code's tools, and cannot see the conversation context. Hooks receive only stdin input and produce stdout output. This limits enforcement to what can be done with pure filesystem/shell operations.

**Evidence:**
- ECW LES-030
- Claude Code hook documentation
- Hard-rules.md constraint c-012

**Level Impact:**
- **L0:** The safety checkpoints can't use the AI's special tools - they're in their own little box
- **L1:** Hooks must use Python/shell for enforcement; cannot call MCP tools or read conversation
- **L2:** Design enforcement tiers with hook limitations in mind; Advisory/Soft via prompts, Medium/Hard via filesystem

---

### DISC-013: No Recursive Subagents (c-015)

**ID:** DISC-013
**Slug:** no-recursive-subagents
**Name:** Task Tool Filtered at Adapter Level
**Short Description:** Constraint c-015 prevents subagents from spawning further subagents via Task tool.

**Long Description:**
ECW constraint c-015 prohibits recursive subagent spawning - a subagent cannot use the Task tool to spawn another subagent. This prevents: (1) runaway agent multiplication, (2) context explosion, (3) unpredictable behavior. The constraint is enforced at the adapter level by filtering allowed-tools for subagents. This has implications for multi-agent design in Jerry.

**Evidence:**
- ECW constraint c-015
- Hard-rules.md

**Level Impact:**
- **L0:** Helper agents can't create more helper agents - only the main agent can do that
- **L1:** Subagent tool lists must exclude Task; design for single-level delegation
- **L2:** Orchestration must be flat (coordinator → specialist) not nested (coordinator → sub-coordinator → specialist)

---

### DISC-014: Mandatory Persistence (c-009)

**ID:** DISC-014
**Slug:** mandatory-persistence
**Name:** All Agent Outputs Must Be Files
**Short Description:** Constraint c-009 requires all agent work products to be persisted as files, not transient output.

**Long Description:**
ECW constraint c-009 mandates that all agent outputs must be persisted to the filesystem using the Write tool. Transient output (returned text) is insufficient because: (1) it's lost on context compaction, (2) it can't be referenced by other agents, (3) it's not auditable. This constraint is enforced through the 4-tier enforcement system, with PostToolUse hooks verifying file creation.

**Evidence:**
- ECW constraint c-009
- Hard-rules.md
- All ps-*.md agents

**Level Impact:**
- **L0:** All work must be saved to files, not just displayed - otherwise it gets lost
- **L1:** Always use Write tool at end of agent work; call link-artifact after
- **L2:** Filesystem is source of truth; enables agent continuity across sessions and context compactions

---

## Graph Data Model Discoveries (Phase 2.5)

### DISC-026: Property Graph Model

**ID:** DISC-026
**Slug:** property-graph-model
**Name:** Property Graph Model for Gremlin Compatibility
**Short Description:** Vertex/Edge/Property abstractions prepare for eventual Gremlin/graph database migration.

**Long Description:**
Jerry's domain model uses property graph abstractions (Vertex, Edge, Property) that align with Apache TinkerPop's Gremlin query language. This enables future migration from file-based storage to a graph database (JanusGraph, Neptune, CosmosDB) without domain model changes. The abstractions include: Vertex (node with id, label, properties), Edge (connection with id, label, properties, in/out vertices), and Property (key-value with optional meta-properties).

**Evidence:**
- [Apache TinkerPop](https://tinkerpop.apache.org/)
- GRAPH_DATA_MODEL_ANALYSIS.md

**Level Impact:**
- **L0:** We're organizing data like a web of connected points, so we can ask questions about connections later
- **L1:** Implement Vertex, Edge, Property base classes; all entities extend Vertex
- **L2:** Graph model enables relationship queries (all tasks blocked by X, dependency chains) impossible with relational

---

### DISC-027: VertexId Base Class

**ID:** DISC-027
**Slug:** vertex-id-base-class
**Name:** All Strongly Typed IDs Extend VertexId
**Short Description:** TaskId, PhaseId, PlanId all extend VertexId for graph-native identity.

**Long Description:**
The strongly typed ID hierarchy has VertexId as the base class. All domain entity IDs (TaskId, PhaseId, PlanId, SubtaskId) extend VertexId, which itself extends a graph-native identity concept. This enables: (1) polymorphic handling of any entity ID, (2) graph operations that work on any vertex type, (3) unified serialization for graph storage. VertexId contains the raw identifier and label information.

**Evidence:**
- GRAPH_DATA_MODEL_ANALYSIS.md
- TinkerPop Element interface

**Level Impact:**
- **L0:** All IDs are the same kind of thing at their core, just with different labels
- **L1:** Implement VertexId(value: str, label: str); TaskId extends with label="task"
- **L2:** Enables generic graph algorithms; can traverse from any vertex type without type-specific code

---

### DISC-038: VertexProperty vs EdgeProperty

**ID:** DISC-038
**Slug:** vertex-property-edge-property
**Name:** TinkerPop Distinguishes VertexProperty from EdgeProperty
**Short Description:** VertexProperty has meta-properties and cardinality; EdgeProperty is simple key-value.

**Long Description:**
Apache TinkerPop distinguishes between VertexProperty and EdgeProperty. VertexProperty is a full Element with its own id, can have meta-properties (properties on the property), and supports cardinality (SINGLE, LIST, SET for multi-valued properties). EdgeProperty is a simple key-value pair without meta-properties. This distinction enables audit trails (who/when changed a property) via meta-properties on VertexProperty.

**Evidence:**
- [TinkerPop VertexProperty](https://tinkerpop.apache.org/docs/current/reference/#vertex-properties)
- GRAPH_DATA_MODEL_ANALYSIS.md Section 2.4

**Level Impact:**
- **L0:** Properties on points (vertices) can have their own properties; properties on lines (edges) can't
- **L1:** Implement separate VertexProperty and EdgeProperty classes; use VP for audit-requiring fields
- **L2:** Meta-properties enable temporal queries ("what was the value on date X?") without separate audit tables

---

## Agent Enforcement Discoveries (Phase 3.5)

### DISC-031: 4-Tier Progressive Enforcement

**ID:** DISC-031
**Slug:** four-tier-progressive-enforcement
**Name:** Advisory → Soft → Medium → Hard Enforcement Tiers
**Short Description:** Industry standard is progressive enforcement from advisory reminders to hard blocks.

**Long Description:**
Research across Anthropic, OpenAI, Google DeepMind, and academic sources reveals consensus on progressive enforcement for AI agents. The 4-tier model: (1) Advisory (60%) - session start reminders, documentation, (2) Soft (30%) - warnings, self-monitoring, retry suggestions, (3) Medium (8%) - tool restrictions, required confirmations, (4) Hard (2%) - blocking, termination. Hard enforcement is reserved for safety-critical constraints; most enforcement should be soft.

**Evidence:**
- AGENT_BEHAVIOR_ENFORCEMENT_ANALYSIS.md
- Anthropic Constitutional AI
- OpenAI Model Spec
- Google DeepMind CCLs

**Level Impact:**
- **L0:** Start with gentle reminders, then warnings, then restrictions, only block for serious stuff
- **L1:** Implement SessionStart hooks (advisory), PreToolUse prompts (soft), tool filtering (medium)
- **L2:** Match enforcement tier to constraint severity; over-enforcement degrades agent utility

---

### DISC-032: Constitutional AI Foundation

**ID:** DISC-032
**Slug:** constitutional-ai-foundation
**Name:** Constitutional AI Enables Self-Supervised Alignment
**Short Description:** Anthropic's Constitutional AI uses principles rather than human labeling for alignment.

**Long Description:**
Anthropic's Constitutional AI (CAI) approach trains models to self-supervise alignment using a constitution of principles rather than extensive human labeling. The model critiques its own outputs against the constitution and revises. This approach is foundational for Jerry's enforcement design - agents can be given a "constitution" (Jerry Constitution) and trained/prompted to self-monitor compliance, reducing need for external enforcement.

**Evidence:**
- [Anthropic Constitutional AI](https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback)
- Bai et al. (2022)

**Level Impact:**
- **L0:** Instead of someone checking everything, the AI learns rules and checks itself
- **L1:** Create Jerry Constitution with principles; inject into agent prompts for self-monitoring
- **L2:** CAI-inspired approach reduces enforcement overhead; constitution is compressed governance

---

### DISC-033: 75% Soft Enforcement Consensus

**ID:** DISC-033
**Slug:** soft-enforcement-consensus
**Name:** Industry Consensus Favors 75% Soft Enforcement
**Short Description:** Research shows 75% of enforcement should be soft (warnings, suggestions) not hard (blocks).

**Long Description:**
Analysis of industry practices reveals that approximately 75% of agent enforcement is soft (advisory + soft tiers) while only 25% is hard (medium + hard tiers). Hard enforcement creates friction, degrades user experience, and can cause agents to find workarounds. Soft enforcement guides behavior through prompts, warnings, and suggestions, maintaining agent utility while achieving compliance. Jerry should follow this ratio.

**Evidence:**
- AGENT_BEHAVIOR_ENFORCEMENT_ANALYSIS.md
- OpenAI, Anthropic, Google practices

**Level Impact:**
- **L0:** Most rules should be reminders and suggestions, not brick walls
- **L1:** Design constraints with enforcement tier; default to Advisory unless safety-critical
- **L2:** Hard enforcement for c-009 (persistence), c-015 (no recursion); soft for everything else

---

## Summary Statistics

| Phase | Discoveries | Categories |
|-------|-------------|------------|
| Phase 0 | DISC-001 to DISC-003 | Research, Architecture |
| Phase 2.5 | DISC-004 to DISC-030 | DDD, Performance, CloudEvents, Graph |
| Phase 3.5 | DISC-031 to DISC-053 | Enforcement, Security, Agent Design, Serialization |
| **Total** | **53** | Multiple |

---

## References

Full citations are provided in each discovery's Evidence section. Key sources:

1. Vernon, V. (2013). *Implementing Domain-Driven Design*. Addison-Wesley.
2. Evans, E. (2003). *Domain-Driven Design*. Addison-Wesley.
3. Cockburn, A. (2005). "Hexagonal Architecture"
4. Apache TinkerPop Documentation
5. CloudEvents Specification 1.0
6. Chroma Research: Context Rot
7. Anthropic Constitutional AI Paper
8. OpenAI Model Spec (2024)
9. Google DeepMind CCLs
10. TOON Specification v3.0
