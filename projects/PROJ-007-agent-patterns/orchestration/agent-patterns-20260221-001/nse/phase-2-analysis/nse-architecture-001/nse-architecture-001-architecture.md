---
DISCLAIMER: This guidance is AI-generated based on NASA Systems Engineering
standards. It is advisory only and does not constitute official NASA guidance.
All SE decisions require human review and professional engineering judgment.
Not for use in mission-critical decisions without SME validation.
---

# Agent Architecture Reference Model for Claude Code

> **Project:** PROJ-007 | **Agent:** nse-architecture-001 v2.1.0
> **Date:** 2026-02-21 | **Status:** Draft
> **NASA Processes:** NPR 7123.1D Process 3 (Logical Decomposition), Process 4 (Design Solution), Process 17 (Decision Analysis)
> **Cognitive Mode:** Convergent
> **Inputs:** Phase 1 Trade Study (nse-explorer-001), PS-to-NSE Cross-Pollination (barrier-1), Architecture Standards, AGENTS.md, 37 Agent Definitions

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Architecture Summary](#l0-architecture-summary) | Plain-language overview of the reference architecture |
| [1. Agent Architecture Reference Model](#1-agent-architecture-reference-model) | Hexagonal mapping, anatomy, taxonomy |
| [1.1 Hexagonal Architecture Mapping](#11-hexagonal-architecture-mapping) | Ports and adapters applied to agents |
| [1.2 Agent Anatomy Diagram](#12-agent-anatomy-diagram) | Structure, runtime, context flow, lifecycle |
| [1.3 Agent Type Taxonomy](#13-agent-type-taxonomy) | Classification by mode, autonomy, output, tools |
| [2. Integration Architecture](#2-integration-architecture) | Agent-to-agent, agent-to-tool, agent-to-context |
| [2.1 Agent-to-Agent Communication](#21-agent-to-agent-communication) | Invocation, handoff, context passing |
| [2.2 Agent-to-Tool Integration](#22-agent-to-tool-integration) | Tool assignment, restriction, MCP, result handling |
| [2.3 Agent-to-Context Integration](#23-agent-to-context-integration) | Progressive disclosure, budget, isolation, filesystem |
| [3. Design Patterns Catalog](#3-design-patterns-catalog) | Ten architectural patterns with examples |
| [4. Architecture Decision Records](#4-architecture-decision-records) | ADR-001, ADR-002, ADR-003 |
| [5. Self-Review (S-010)](#5-self-review-s-010) | Completeness and quality verification |
| [References](#references) | Source traceability |

---

## L0: Architecture Summary

This document defines a reference architecture for building Claude Code agents -- the specialized AI workers that perform focused tasks within the Jerry framework. The architecture answers three fundamental questions: How should an agent be structured internally? How should agents communicate with each other and with tools? What reusable design patterns should agent authors follow?

**Key architectural decisions:**

- **Hexagonal architecture maps cleanly to agents.** An agent's reasoning core is the domain layer. Tools (Read, Write, Bash, MCP) are ports. Prompt strategies, persona definitions, and output formatters are adapters. The Claude Code runtime is infrastructure. This separation keeps agent definitions focused on *what* to reason about, not *how* the runtime works.

- **Agents are classified along four independent dimensions.** Cognitive mode (divergent vs. convergent), autonomy level (fully autonomous vs. guided vs. interactive), output type (document producer vs. decision maker vs. validator vs. reporter), and tool profile (read-only vs. read-write vs. external-access). These dimensions determine which design patterns apply to a given agent.

- **Ten reusable patterns form the catalog.** From the fundamental Specialist Agent and Orchestrator-Worker patterns, through quality patterns (Creator-Critic-Revision, Quality Gate) and context management patterns (Progressive Disclosure, Context Budget), to governance patterns (Tool Restriction, Structured Handoff). Each pattern is validated by both Jerry's production experience (37 agents) and industry evidence.

- **Three architecture decisions are recommended.** (1) Agent definition format: YAML+Markdown with schema validation (evolutionary enhancement of the current format). (2) Agent routing: keyword-first with LLM fallback for ambiguous cases. (3) Quality assurance: layered architecture with deterministic schema validation, self-review, and critic-scored revision.

**Bottom line:** Jerry's existing skill-based specialist architecture is well-designed and industry-validated. The reference model formalizes the implicit patterns already present in the 37 production agents, making them explicit, teachable, and enforceable.

---

## 1. Agent Architecture Reference Model

### 1.1 Hexagonal Architecture Mapping

The hexagonal architecture (ports and adapters) provides a clean conceptual mapping to Claude Code agent design. In traditional software, hexagonal architecture isolates domain logic from external dependencies through ports (interfaces) and adapters (implementations). The same principle applies to agents: isolate the agent's reasoning core from the runtime environment, tool integrations, and output formatting.

#### Layer Mapping

```
+------------------------------------------------------------------+
|                    INFRASTRUCTURE LAYER                           |
|  Claude Code Runtime | Context Window (200K) | Model (Opus/      |
|  Sonnet/Haiku) | MCP Servers | Filesystem | Session Manager      |
+------------------------------------------------------------------+
|                                                                  |
|  +------------------------------------------------------------+ |
|  |                    ADAPTER LAYER                            | |
|  |                                                            | |
|  |  INBOUND ADAPTERS          OUTBOUND ADAPTERS              | |
|  |  +------------------+     +--------------------+          | |
|  |  | System Prompt    |     | L0/L1/L2 Formatter |          | |
|  |  | (Persona, Mode)  |     | (Output Levels)    |          | |
|  |  +------------------+     +--------------------+          | |
|  |  +------------------+     +--------------------+          | |
|  |  | Session Context  |     | Artifact Writer    |          | |
|  |  | Deserializer     |     | (File Persistence) |          | |
|  |  +------------------+     +--------------------+          | |
|  |  +------------------+     +--------------------+          | |
|  |  | Guardrail        |     | Handoff Schema     |          | |
|  |  | Validator        |     | Serializer         |          | |
|  |  +------------------+     +--------------------+          | |
|  |                                                            | |
|  +------------------------------------------------------------+ |
|                                                                  |
|  +------------------------------------------------------------+ |
|  |                      PORT LAYER                             | |
|  |                                                            | |
|  |  PRIMARY PORTS (Driving)    SECONDARY PORTS (Driven)       | |
|  |  +------------------+     +--------------------+          | |
|  |  | Task Invocation  |     | File System I/O    |          | |
|  |  | (orchestrator    |     | (Read/Write/Edit)  |          | |
|  |  |  calls agent)    |     +--------------------+          | |
|  |  +------------------+     +--------------------+          | |
|  |  +------------------+     | Search & Discovery |          | |
|  |  | Direct User      |     | (Glob/Grep)        |          | |
|  |  | Invocation        |     +--------------------+          | |
|  |  +------------------+     +--------------------+          | |
|  |                           | Web Access          |          | |
|  |                           | (WebSearch/Fetch)   |          | |
|  |                           +--------------------+          | |
|  |                           +--------------------+          | |
|  |                           | MCP Tools           |          | |
|  |                           | (Context7/MemKeep)  |          | |
|  |                           +--------------------+          | |
|  |                           +--------------------+          | |
|  |                           | Execution           |          | |
|  |                           | (Bash/Task)         |          | |
|  |                           +--------------------+          | |
|  |                                                            | |
|  +------------------------------------------------------------+ |
|                                                                  |
|  +------------------------------------------------------------+ |
|  |                     DOMAIN LAYER (Core)                     | |
|  |                                                            | |
|  |  +------------------+  +-------------------+              | |
|  |  | Cognitive Mode   |  | Expertise Domain  |              | |
|  |  | (divergent/      |  | (research, arch,  |              | |
|  |  |  convergent/     |  |  review, risk,    |              | |
|  |  |  integrative)    |  |  orchestration)   |              | |
|  |  +------------------+  +-------------------+              | |
|  |                                                            | |
|  |  +------------------+  +-------------------+              | |
|  |  | Decision Logic   |  | Quality Standards |              | |
|  |  | (constitutional  |  | (H-13 threshold,  |              | |
|  |  |  compliance,     |  |  S-014 rubric,    |              | |
|  |  |  guardrails)     |  |  criticality)     |              | |
|  |  +------------------+  +-------------------+              | |
|  |                                                            | |
|  |  +------------------------------------------+             | |
|  |  | Reasoning Strategy                        |             | |
|  |  | (methodology, process, heuristics)        |             | |
|  |  +------------------------------------------+             | |
|  |                                                            | |
|  +------------------------------------------------------------+ |
+------------------------------------------------------------------+
```

#### Layer Definitions

| Layer | Agent Equivalent | Responsibility | Jerry Implementation |
|-------|-----------------|----------------|---------------------|
| **Domain** | Reasoning Core | Cognitive mode, expertise, decision logic, quality standards, methodology | Markdown body of agent definition file (identity, persona, purpose, methodology sections) |
| **Port** | Tool Interfaces | Abstract contracts for tool access -- what capabilities the agent needs, not how they are provided | `capabilities.allowed_tools` in YAML frontmatter; defines *which* tools, not *how* they work |
| **Adapter** | Prompt Strategies & Formatters | Concrete implementations: system prompt construction, input deserialization, output formatting (L0/L1/L2), artifact persistence, handoff serialization | YAML frontmatter (persona, guardrails, output config); XML-tagged behavioral sections in body |
| **Infrastructure** | Runtime Environment | Claude Code platform, context window, model selection, MCP server connections, filesystem | `.claude/settings.local.json`, MCP server configs, model tier selection in YAML |

#### Dependency Rule (Hexagonal Invariant)

The hexagonal dependency rule applies: **the domain layer MUST NOT depend on any outer layer**. In agent terms:

- The agent's reasoning core (cognitive mode, expertise, methodology) does not reference specific tool names, output formats, or runtime details.
- Tool interfaces are declared as abstract capabilities ("needs web search") rather than concrete implementations ("calls WebSearch tool").
- Output format adapters can change (e.g., switch from markdown to JSON) without modifying the reasoning core.

This maps directly to Jerry's existing architecture standard H-07: "domain MUST NOT import from application, infrastructure, or interface."

#### Mapping to Jerry Codebase Architecture

| Hexagonal Concept | Software (src/) | Agent (skills/*/agents/) |
|-------------------|-----------------|--------------------------|
| Domain Entity | `src/domain/entities/` | Agent identity, cognitive mode, expertise |
| Domain Port | `src/domain/ports/` | `capabilities.allowed_tools` (abstract contract) |
| Application Service | `src/application/handlers/` | Agent methodology and process sections |
| Infrastructure Adapter | `src/infrastructure/adapters/` | MCP tool integrations, file I/O implementations |
| Interface Adapter | `src/interface/cli/` | System prompt construction, output formatting |
| Composition Root | `src/bootstrap.py` | Skill orchestrator (routes to and configures agents) |

---

### 1.2 Agent Anatomy Diagram

#### 1.2.1 Agent Definition File Structure

An agent definition file uses the YAML frontmatter + Markdown body pattern. The YAML frontmatter provides machine-readable metadata; the Markdown body provides human-readable (and LLM-readable) behavioral instructions.

```
+================================================================+
|                    AGENT DEFINITION FILE                        |
|                  (skills/{skill}/agents/{name}.md)              |
+================================================================+
|                                                                |
|  YAML FRONTMATTER (Machine-Readable Metadata)                 |
|  +---------------------------------------------------------+  |
|  | --- (delimiter)                                         |  |
|  |                                                         |  |
|  | name: ps-researcher          # Unique agent identifier  |  |
|  | version: "2.3.0"             # Semver                   |  |
|  | description: "..."           # H-28 compliant           |  |
|  | model: opus                  # Model tier selection      |  |
|  |                                                         |  |
|  | identity:                    # WHO the agent is          |  |
|  |   role: "Research Specialist"                           |  |
|  |   expertise: [...]           # Domain expertise list    |  |
|  |   cognitive_mode: "divergent" # Reasoning approach      |  |
|  |                                                         |  |
|  | persona:                     # HOW the agent communicates|  |
|  |   tone: "professional"                                  |  |
|  |   communication_style: "consultative"                   |  |
|  |   audience_level: "adaptive"                            |  |
|  |                                                         |  |
|  | capabilities:                # WHAT the agent can do     |  |
|  |   allowed_tools: [...]       # Port declarations        |  |
|  |   output_formats: [...]      # Adapter config           |  |
|  |   forbidden_actions: [...]   # Constitutional guardrails|  |
|  |                                                         |  |
|  | guardrails:                  # Safety boundaries         |  |
|  |   input_validation: {...}    # Input format checks      |  |
|  |   output_filtering: [...]    # Output safety checks     |  |
|  |   fallback_behavior: "..."   # Error recovery           |  |
|  |                                                         |  |
|  | output:                      # WHERE results go          |  |
|  |   location: "projects/..."   # Artifact path template   |  |
|  |   levels: [L0, L1, L2]      # Progressive disclosure    |  |
|  |                                                         |  |
|  | validation:                  # POST-COMPLETION checks    |  |
|  |   post_completion_checks: [...]                         |  |
|  |                                                         |  |
|  | constitution:                # Governance alignment      |  |
|  |   principles_applied: [...]                             |  |
|  |                                                         |  |
|  | session_context:             # Handoff schema            |  |
|  |   schema: "..."              # JSON Schema ref           |  |
|  |   on_receive: [...]          # Inbound processing       |  |
|  |   on_send: [...]             # Outbound processing      |  |
|  |                                                         |  |
|  | --- (delimiter)                                         |  |
|  +---------------------------------------------------------+  |
|                                                                |
|  MARKDOWN BODY (LLM-Readable Behavioral Instructions)         |
|  +---------------------------------------------------------+  |
|  | <agent>                      # Root container            |  |
|  |                                                         |  |
|  |   <identity>                 # Rich role description    |  |
|  |     Role, expertise, cognitive mode narrative            |  |
|  |     Key distinctions from similar agents                 |  |
|  |   </identity>                                           |  |
|  |                                                         |  |
|  |   <purpose>                  # Mission statement         |  |
|  |     What this agent does and why                         |  |
|  |   </purpose>                                            |  |
|  |                                                         |  |
|  |   <input>                    # Expected input format     |  |
|  |     Session context, required/optional fields            |  |
|  |   </input>                                              |  |
|  |                                                         |  |
|  |   <capabilities>             # Detailed tool usage       |  |
|  |     Tool-by-tool usage patterns and examples             |  |
|  |   </capabilities>                                       |  |
|  |                                                         |  |
|  |   <methodology>              # HOW to reason             |  |
|  |     Step-by-step process, decision trees                 |  |
|  |     Quality criteria, iteration strategy                 |  |
|  |   </methodology>                                        |  |
|  |                                                         |  |
|  |   <output>                   # Output specification      |  |
|  |     Template, L0/L1/L2 structure, artifact path          |  |
|  |   </output>                                             |  |
|  |                                                         |  |
|  |   <guardrails>               # Safety narrative          |  |
|  |     Constitutional compliance, failure modes              |  |
|  |   </guardrails>                                         |  |
|  |                                                         |  |
|  | </agent>                                                |  |
|  +---------------------------------------------------------+  |
+================================================================+
```

#### 1.2.2 Runtime Behavior Model

```
+-------------------------------------------------------------------+
|                     AGENT RUNTIME BEHAVIOR                        |
+-------------------------------------------------------------------+
|                                                                   |
|  PHASE 1: INITIALIZATION                                         |
|  +---------------------------------------------------------------+
|  |                                                               |
|  |  Orchestrator/User                                            |
|  |       |                                                       |
|  |       v                                                       |
|  |  [Task Tool or Direct Invocation]                             |
|  |       |                                                       |
|  |       v                                                       |
|  |  +-------------------+    +--------------------+              |
|  |  | Load Agent Def    |--->| Construct System   |              |
|  |  | (YAML + Markdown) |    | Prompt (persona +  |              |
|  |  +-------------------+    | guardrails + rules)|              |
|  |                           +--------------------+              |
|  |                                  |                            |
|  |                                  v                            |
|  |                           +--------------------+              |
|  |                           | Apply Tool Config  |              |
|  |                           | (allowlist from    |              |
|  |                           |  capabilities)     |              |
|  |                           +--------------------+              |
|  |                                  |                            |
|  |                                  v                            |
|  |                           +--------------------+              |
|  |                           | Deserialize Input  |              |
|  |                           | (session_context,  |              |
|  |                           |  validate schema)  |              |
|  |                           +--------------------+              |
|  +---------------------------------------------------------------+
|                                                                   |
|  PHASE 2: EXECUTION (Agentic Loop)                               |
|  +---------------------------------------------------------------+
|  |                                                               |
|  |     +----> [Gather Context] ----+                             |
|  |     |      (Read, Glob, Grep,   |                             |
|  |     |       WebSearch, Context7) |                             |
|  |     |                           v                             |
|  |     |      [Reason & Decide]                                  |
|  |     |      (Apply methodology,                                |
|  |     |       cognitive mode,                                   |
|  |     |       domain expertise)                                 |
|  |     |           |                                             |
|  |     |           v                                             |
|  |     |      [Take Action]                                      |
|  |     |      (Write, Edit, Bash,                                |
|  |     |       MCP Store, Task)                                  |
|  |     |           |                                             |
|  |     |           v                                             |
|  |     |      [Verify Work]                                      |
|  |     |      (Read output, check                                |
|  |     |       guardrails, validate                              |
|  |     |       completeness)                                     |
|  |     |           |                                             |
|  |     |           v                                             |
|  |     |      {Complete?} --No---+                               |
|  |     |           |            |                                |
|  |     +-----------+            |                                |
|  |                              |                                |
|  |           Yes                |                                |
|  |            |                 |                                |
|  |            v                 |                                |
|  +---------------------------------------------------------------+
|                                                                   |
|  PHASE 3: OUTPUT                                                  |
|  +---------------------------------------------------------------+
|  |                                                               |
|  |  [Apply Self-Review (S-010 / H-15)]                           |
|  |       |                                                       |
|  |       v                                                       |
|  |  [Format Output (L0/L1/L2)]                                   |
|  |       |                                                       |
|  |       v                                                       |
|  |  [Persist Artifact (Write to file per P-002)]                 |
|  |       |                                                       |
|  |       v                                                       |
|  |  [Run Validation Checks (post_completion_checks)]             |
|  |       |                                                       |
|  |       v                                                       |
|  |  [Serialize Handoff (session_context.on_send)]                |
|  |                                                               |
|  +---------------------------------------------------------------+
|                                                                   |
|  PHASE 4: CLEANUP                                                 |
|  +---------------------------------------------------------------+
|  |                                                               |
|  |  [Return result to orchestrator/user]                         |
|  |  [Context window released (subagent)]                         |
|  |  [MCP state persisted (if applicable)]                        |
|  |                                                               |
|  +---------------------------------------------------------------+
+-------------------------------------------------------------------+
```

#### 1.2.3 Context Flow Diagram

```
+-------------------------------------------------------------------+
|                      CONTEXT FLOW                                 |
+-------------------------------------------------------------------+
|                                                                   |
|  SYSTEM PROMPT ASSEMBLY (at initialization)                       |
|                                                                   |
|  +-------------------+  +-------------------+                     |
|  | Agent Identity    |  | Constitutional    |                     |
|  | (role, expertise, |  | Constraints       |                     |
|  |  cognitive mode,  |  | (H-01..H-31,      |                     |
|  |  persona)         |  |  P-003, P-020,    |                     |
|  +--------+----------+  |  P-022)           |                     |
|           |              +--------+----------+                     |
|           |                       |                               |
|           v                       v                               |
|  +--------------------------------------------+                  |
|  |        SYSTEM PROMPT (combined)             |                  |
|  |  ~2,000-8,000 tokens depending on agent     |                  |
|  +---------------------+----------------------+                  |
|                         |                                         |
|                         v                                         |
|  +--------------------------------------------+                  |
|  |           CONTEXT WINDOW (200K)             |                  |
|  |                                             |                  |
|  |  +-----------+  +------------+  +---------+ |                  |
|  |  | System    |  | User       |  | Tool    | |                  |
|  |  | Prompt    |  | Messages   |  | Results | |                  |
|  |  | (~5%)     |  | (~10-20%)  |  | (~50%)  | |                  |
|  |  +-----------+  +------------+  +---------+ |                  |
|  |                                             |                  |
|  |  +------------------------------------------+ |                |
|  |  | Agent Reasoning & Output (~25-35%)        | |                |
|  |  +------------------------------------------+ |                |
|  |                                             |                  |
|  +--------------------------------------------+                  |
+-------------------------------------------------------------------+
```

---

### 1.3 Agent Type Taxonomy

Agents are classified along four independent dimensions. Each dimension captures a distinct architectural characteristic that influences design patterns, tool assignment, and quality enforcement.

#### Dimension 1: Cognitive Mode

| Mode | Description | Reasoning Pattern | Jerry Examples |
|------|-------------|-------------------|----------------|
| **Divergent** | Explores broadly, generates options, discovers patterns | Wide search, multiple hypotheses, creative association | ps-researcher, nse-explorer, ts-extractor, sb-rewriter |
| **Convergent** | Analyzes narrowly, selects options, produces conclusions | Focused evaluation, criteria-based selection, synthesis | ps-analyst, nse-architecture, adv-scorer, orch-planner |
| **Integrative** | Combines inputs from multiple sources into unified output | Cross-source correlation, pattern merging, gap filling | ps-synthesizer, orch-synthesizer |
| **Systematic** | Applies step-by-step procedures, verifies compliance | Checklist execution, protocol adherence, completeness verification | ps-validator, wt-auditor |
| **Forensic** | Traces causes backward from symptoms to root causes | Causal chain analysis, evidence correlation, hypothesis testing | ps-investigator |

**Design Implications:**
- Divergent agents need broader tool access (WebSearch, Context7) and larger output budgets.
- Convergent agents need structured input schemas and explicit evaluation criteria.
- Integrative agents need access to multiple prior artifacts (file reading) but rarely need web access.
- Systematic agents need checklist-driven methodologies and binary pass/fail output.

#### Dimension 2: Autonomy Level

| Level | Description | Human Interaction | Jerry Examples |
|-------|-------------|-------------------|----------------|
| **Fully Autonomous** | Completes task without human interaction | None during execution; human reviews output | ps-researcher, adv-executor, ts-parser |
| **Guided** | Follows orchestrator directives within defined scope | Orchestrator provides task parameters; agent executes | nse-architecture, ps-analyst, adv-scorer |
| **Interactive** | Requires human input during execution | May ask clarifying questions (H-31) | sb-voice (session mode) |

**Design Implications:**
- Autonomous agents need comprehensive guardrails and self-review (H-15).
- Guided agents need well-defined input schemas and clear scope boundaries.
- Interactive agents need minimal context overhead to preserve budget for conversation.

#### Dimension 3: Output Type

| Type | Description | Quality Enforcement | Jerry Examples |
|------|-------------|---------------------|----------------|
| **Document Producer** | Creates structured documents (research, architecture, requirements) | Full quality gate (H-13, H-14 for C2+) | ps-researcher, nse-architecture, nse-requirements |
| **Decision Maker** | Evaluates alternatives and recommends selections | Weighted criteria matrices, trade study methodology | nse-explorer (trade studies), adv-selector |
| **Validator** | Verifies compliance against criteria; binary pass/fail | Deterministic checks where possible | ps-validator, wt-verifier, wt-auditor |
| **Reporter** | Summarizes existing data into formatted reports | Lower quality gate (C1 sufficient) | ps-reporter, nse-reporter, orch-synthesizer |
| **Transformer** | Converts input from one format/representation to another | Schema validation of output format | ts-formatter, ts-mindmap-ascii, ts-mindmap-mermaid |

**Design Implications:**
- Document producers carry the highest quality burden (3+ creator-critic iterations for C2+).
- Decision makers need explicit methodology sections with criteria, weights, and scoring.
- Validators should maximize deterministic checks (schema validation) before LLM-based assessment.
- Reporters and transformers operate at C1 criticality unless their output feeds C2+ deliverables.

#### Dimension 4: Tool Profile

| Profile | Tools Available | Security Tier | Jerry Examples |
|---------|----------------|---------------|----------------|
| **Read-Only** | Read, Glob, Grep | Lowest privilege | adv-executor, adv-scorer, wt-auditor |
| **Read-Write** | Read, Write, Edit, Glob, Grep, Bash | Standard privilege | ps-analyst, nse-architecture, orch-planner |
| **External-Access** | All above + WebSearch, WebFetch, Context7 | Elevated privilege | ps-researcher, nse-explorer |
| **State-Persistent** | Read-Write + Memory-Keeper (store/retrieve/search) | Elevated privilege | orch-planner, orch-tracker, ps-architect |
| **Full-Access** | External-Access + State-Persistent + Task | Highest privilege | ps-researcher (via Task for delegation) |

**Design Implications:**
- Read-only agents are the safest; prefer this profile when the agent does not need to create files.
- External-access agents carry risk of introducing unvalidated external information; require citation guardrails (P-001, P-004).
- State-persistent agents must follow MCP key patterns (`jerry/{project}/{entity-type}/{entity-id}`).
- Full-access agents must be individually justified; Task tool use requires P-003 compliance verification.

#### Combined Taxonomy Matrix (Representative Agents)

| Agent | Cognitive | Autonomy | Output | Tool Profile |
|-------|-----------|----------|--------|-------------|
| ps-researcher | Divergent | Autonomous | Document Producer | Full-Access |
| ps-analyst | Convergent | Guided | Document Producer | Read-Write |
| ps-critic | Convergent | Guided | Validator | Read-Only + Write |
| ps-synthesizer | Integrative | Guided | Document Producer | External-Access |
| nse-explorer | Divergent | Autonomous | Decision Maker | External-Access |
| nse-architecture | Convergent | Guided | Document Producer | Read-Write |
| nse-requirements | Convergent | Guided | Document Producer | State-Persistent |
| orch-planner | Convergent | Guided | Document Producer | State-Persistent |
| adv-executor | Convergent | Guided | Validator | Read-Only |
| adv-scorer | Convergent | Guided | Validator | Read-Only |
| ts-parser | Convergent | Autonomous | Transformer | State-Persistent |
| sb-voice | Divergent | Interactive | (Conversational) | Read-Only |
| wt-auditor | Systematic | Autonomous | Validator | Read-Only |

---

## 2. Integration Architecture

### 2.1 Agent-to-Agent Communication

#### 2.1.1 Orchestrator-to-Worker Invocation

Claude Code enforces a single-level agent hierarchy per P-003/H-01. The orchestrator (either the lead Claude Code agent or a skill orchestrator like orch-planner) invokes worker agents via the Task tool.

```
+-------------------------------------------------------------------+
|                  INVOCATION ARCHITECTURE                          |
+-------------------------------------------------------------------+
|                                                                   |
|  +-------------------------+                                      |
|  |    ORCHESTRATOR          |                                      |
|  |  (Lead Agent or Skill   |                                      |
|  |   Orchestrator)          |                                      |
|  +--+------+------+--------+                                      |
|     |      |      |                                               |
|     |      |      |  Task Tool (single level, P-003)              |
|     v      v      v                                               |
|  +-----+ +-----+ +-----+                                         |
|  | W-1 | | W-2 | | W-3 |   Worker Agents                        |
|  +-----+ +-----+ +-----+   (ps-researcher, nse-arch, etc.)       |
|     |      |      |                                               |
|     v      v      v                                               |
|  [File] [File] [File]      Artifacts (filesystem-as-memory)      |
|                                                                   |
|  CONSTRAINT: Workers MUST NOT spawn further subagents.            |
|  Workers communicate with each other ONLY through artifacts.      |
+-------------------------------------------------------------------+
```

**Invocation Parameters:**

| Parameter | Purpose | Example |
|-----------|---------|---------|
| System Prompt | Agent definition content (YAML+MD) | Full agent file content |
| User Prompt | Task-specific instructions + session context | "Research X. Session context: {...}" |
| Tool Allowlist | Subset of available tools | `["Read", "Write", "Glob", "Grep", "WebSearch"]` |
| Model | Model tier override | `opus` for complex, `sonnet` for balanced, `haiku` for fast |

#### 2.1.2 Handoff Protocol

Agent-to-agent communication uses a structured handoff schema. This addresses the finding from PS research that free-text handoffs are the #1 source of context loss in production multi-agent systems (Google, 2026).

**Handoff Schema:**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["from_agent", "to_agent", "context", "request"],
  "properties": {
    "from_agent": {
      "type": "string",
      "description": "Sending agent identifier",
      "pattern": "^[a-z]+-[a-z]+(-[a-z]+)?$"
    },
    "to_agent": {
      "type": "string",
      "description": "Receiving agent identifier",
      "pattern": "^[a-z]+-[a-z]+(-[a-z]+)?$"
    },
    "context": {
      "type": "object",
      "required": ["task_id", "artifacts"],
      "properties": {
        "task_id": {
          "type": "string",
          "description": "Work item identifier"
        },
        "artifacts": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Paths to produced artifacts"
        },
        "summary": {
          "type": "string",
          "description": "Brief summary of completed work",
          "maxLength": 500
        },
        "key_findings": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Top 3-5 findings for quick orientation"
        },
        "blockers": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Unresolved issues"
        },
        "confidence": {
          "type": "number",
          "minimum": 0,
          "maximum": 1,
          "description": "Self-assessed confidence in output"
        }
      }
    },
    "request": {
      "type": "string",
      "description": "What the receiving agent should do"
    },
    "priority": {
      "type": "string",
      "enum": ["high", "normal", "low"],
      "default": "normal"
    },
    "criticality": {
      "type": "string",
      "enum": ["C1", "C2", "C3", "C4"],
      "description": "Deliverable criticality level"
    }
  }
}
```

#### 2.1.3 Context Passing Conventions

| Convention | Rule | Rationale |
|------------|------|-----------|
| **Artifacts over summaries** | Pass file paths to produced artifacts rather than inline summaries | Avoids context window inflation; recipient reads what it needs |
| **Key findings as orientation** | Include 3-5 bullet points in `key_findings` for quick context loading | Prevents the "cold start" problem where the recipient must read everything |
| **Confidence signal** | Include self-assessed confidence (0-1) on output quality | Allows downstream agents to allocate more scrutiny to low-confidence inputs |
| **Criticality propagation** | Propagate the criticality level (C1-C4) through the handoff chain | Ensures quality gates are applied consistently throughout the pipeline |
| **Blocker escalation** | List unresolved issues in `blockers` array | Prevents silent information loss at handoff boundaries |

#### 2.1.4 Artifact Format Standards

| Artifact Type | Format | Naming Convention | Location |
|---------------|--------|-------------------|----------|
| Research findings | Markdown (L0/L1/L2) | `{ps-id}-{entry-id}-{topic-slug}.md` | `projects/{proj}/research/` |
| Architecture docs | Markdown (L0/L1/L2) | `{proj-id}-{entry-id}-{topic-slug}.md` | `projects/{proj}/architecture/` |
| Trade studies | Markdown (L0/L1/L2) | `{agent}-{topic-slug}.md` | `projects/{proj}/research/` or `nse/phase-*/` |
| Quality scores | Markdown + YAML data | `{strategy-id}-{deliverable-slug}.md` | `projects/{proj}/critiques/` |
| Orchestration state | YAML | `ORCHESTRATION.yaml` | `projects/{proj}/orchestration/{workflow-id}/` |
| Handoff summaries | Markdown | `handoff.md` | `cross-pollination/barrier-*/` |

---

### 2.2 Agent-to-Tool Integration

#### 2.2.1 Static Tool Assignment (Current Jerry Pattern)

Each agent declares its `allowed_tools` in YAML frontmatter. This is the principle of least privilege applied to agent capabilities. The TOOL_REGISTRY.yaml is the single source of truth for tool-to-agent mappings.

**Tool Categories:**

```
+-------------------------------------------------------------------+
|                      TOOL TAXONOMY                                |
+-------------------------------------------------------------------+
|                                                                   |
|  CORE TOOLS (Claude Code Built-In)                               |
|  +------------------------------------------------------------+  |
|  |                                                            |  |
|  |  FILE I/O          SEARCH          EXECUTION   CONTROL    |  |
|  |  +--------+       +--------+      +--------+ +--------+  |  |
|  |  | Read   |       | Glob   |      | Bash   | | Task   |  |  |
|  |  | Write  |       | Grep   |      +--------+ +--------+  |  |
|  |  | Edit   |       +--------+                             |  |
|  |  +--------+                                              |  |
|  |                                                            |  |
|  +------------------------------------------------------------+  |
|                                                                   |
|  WEB TOOLS (External Access)                                     |
|  +------------------------------------------------------------+  |
|  |  +------------+  +------------+                            |  |
|  |  | WebSearch  |  | WebFetch   |                            |  |
|  |  +------------+  +------------+                            |  |
|  +------------------------------------------------------------+  |
|                                                                   |
|  MCP TOOLS (External Servers)                                    |
|  +------------------------------------------------------------+  |
|  |                                                            |  |
|  |  CONTEXT7 (Docs Lookup)    MEMORY-KEEPER (Persistence)    |  |
|  |  +--------------------+   +-------------------------+     |  |
|  |  | resolve-library-id |   | context_save            |     |  |
|  |  | query-docs         |   | context_get             |     |  |
|  |  +--------------------+   | context_search          |     |  |
|  |                           | context_checkpoint      |     |  |
|  |                           +-------------------------+     |  |
|  |                                                            |  |
|  +------------------------------------------------------------+  |
+-------------------------------------------------------------------+
```

#### 2.2.2 Tool Restriction Profiles

Five security tiers control tool access, aligned with the taxonomy in Section 1.3 Dimension 4:

| Tier | Name | Tools | Use Case | Example Agents |
|------|------|-------|----------|----------------|
| T1 | Read-Only | Read, Glob, Grep | Evaluation, auditing, scoring | adv-executor, adv-scorer, wt-auditor |
| T2 | Read-Write | T1 + Write, Edit, Bash | Analysis, document production | ps-analyst, nse-architecture |
| T3 | External | T2 + WebSearch, WebFetch, Context7 | Research, exploration | ps-researcher, nse-explorer |
| T4 | Persistent | T2 + Memory-Keeper | Cross-session state management | orch-planner, orch-tracker |
| T5 | Full | T3 + T4 + Task | Orchestration, delegation | Lead agent, skill orchestrators |

**Tier Selection Guidelines:**

- Always select the **lowest tier** that satisfies the agent's requirements.
- T5 (Full) must be individually justified; the Task tool enables delegation, which requires P-003 compliance verification.
- T3 (External) agents must include citation guardrails (P-001, P-004) in their output filtering.
- T4 (Persistent) agents must follow the MCP key pattern: `jerry/{project}/{entity-type}/{entity-id}`.

#### 2.2.3 MCP Tool Integration Patterns

MCP tools follow a two-phase protocol: resolve then query (Context7) or store then retrieve (Memory-Keeper).

**Context7 Integration Pattern:**

```
Agent needs library docs
       |
       v
[1. resolve-library-id]
  input: library name + query
  output: library ID
       |
       v
[2. query-docs]
  input: library ID + specific question
  output: relevant documentation snippets
       |
       v
Agent incorporates docs into reasoning
```

**Memory-Keeper Integration Pattern (Phase Boundaries):**

```
Phase N completes
       |
       v
[1. context_save / context_checkpoint]
  key: jerry/{project}/orchestration/{workflow-slug}
  value: phase summary, artifacts, scores
       |
       v
Phase N+1 starts
       |
       v
[2. context_get / context_search]
  key/query: jerry/{project}/orchestration/{workflow-slug}
  output: prior phase context
       |
       v
Agent resumes with prior context loaded
```

#### 2.2.4 Tool Result Handling Patterns

| Pattern | Description | When to Use |
|---------|-------------|-------------|
| **Read-Validate-Act** | Read tool result, validate against expectations, then act on it | File reads, search results -- always verify before using |
| **Search-Narrow-Deep** | Broad search (Glob/Grep) -> narrow candidates -> deep read (Read) | Codebase exploration, finding relevant prior work |
| **Fetch-Cite-Integrate** | Fetch external content (WebFetch/Context7) -> extract citation -> integrate into output | Research agents citing web sources or library docs |
| **Write-Verify-Report** | Write artifact -> Read it back -> Verify completeness -> Report path in handoff | All document-producing agents (P-002 compliance) |
| **Store-Checkpoint-Resume** | Store state to MCP -> Create checkpoint -> Resume from checkpoint in next session | Cross-session workflows via Memory-Keeper |

---

### 2.3 Agent-to-Context Integration

#### 2.3.1 Progressive Disclosure Architecture

Context is the scarcest resource in agent systems (200K token window). Progressive disclosure loads context in stages, ensuring agents receive only what they need when they need it.

```
+-------------------------------------------------------------------+
|              PROGRESSIVE DISCLOSURE (Three Tiers)                 |
+-------------------------------------------------------------------+
|                                                                   |
|  TIER 1: METADATA (Always Loaded -- ~500 tokens)                 |
|  +------------------------------------------------------------+  |
|  |  Loaded at session start via SKILL.md description field.    |  |
|  |  Contains: agent name, role, cognitive mode, trigger words  |  |
|  |  Purpose: Route to correct agent, fast context orientation  |  |
|  +------------------------------------------------------------+  |
|                         |                                         |
|                         | Agent is selected for task               |
|                         v                                         |
|  TIER 2: CORE (Loaded on Relevance -- ~2,000-8,000 tokens)      |
|  +------------------------------------------------------------+  |
|  |  Loaded when agent is invoked via Task tool.                |  |
|  |  Contains: full YAML frontmatter + key behavioral sections  |  |
|  |  Purpose: Agent identity, methodology, guardrails, tools    |  |
|  +------------------------------------------------------------+  |
|                         |                                         |
|                         | Agent encounters specific need           |
|                         v                                         |
|  TIER 3: SUPPLEMENTARY (Loaded on Demand -- variable)            |
|  +------------------------------------------------------------+  |
|  |  Loaded via Read tool during execution.                     |  |
|  |  Contains: templates, examples, reference docs, prior work  |  |
|  |  Purpose: Task-specific knowledge (strategy templates,      |  |
|  |           output format examples, prior research artifacts) |  |
|  +------------------------------------------------------------+  |
+-------------------------------------------------------------------+
```

**Jerry Implementation:**

| Tier | Mechanism | Content | Token Cost |
|------|-----------|---------|------------|
| Tier 1 | SKILL.md `description` field in settings | Agent name, trigger keywords | ~500 per skill |
| Tier 2 | Agent definition file loaded by Task tool | Full YAML+MD behavioral spec | ~2,000-8,000 per agent |
| Tier 3 | Agent uses Read tool during execution | Templates, prior artifacts, rules | Variable (on-demand) |

#### 2.3.2 Context Budget Allocation

The 200K token context window must be budgeted across competing needs:

| Budget Category | Allocation | Tokens (typical) | Contents |
|-----------------|-----------|-------------------|----------|
| System Prompt | ~5% | ~10,000 | Agent definition, constitutional rules, L2 re-injections |
| User Messages | ~10-20% | ~20,000-40,000 | Task instructions, session context, handoff data |
| Tool Results | ~40-50% | ~80,000-100,000 | File reads, search results, web content, MCP responses |
| Agent Reasoning + Output | ~25-35% | ~50,000-70,000 | Chain-of-thought, intermediate decisions, final output |
| Reserved (safety margin) | ~5% | ~10,000 | Prevent context exhaustion at output phase |

**Budget Rules:**

| ID | Rule | Rationale |
|----|------|-----------|
| CB-01 | Reserve at least 5% of context for output generation | Prevents truncated output when context fills during reasoning |
| CB-02 | Tool results should not exceed 50% of total context | Leaves room for reasoning; prefer targeted reads over bulk reads |
| CB-03 | Prefer file-path references over inline content in handoffs | Avoids duplicating large content across handoff + tool result reads |
| CB-04 | Use `key_findings` (3-5 bullets) for quick orientation; defer detail to file reads | 500-token orientation prevents 5,000-token cold read |
| CB-05 | For files >500 lines, use line offset/limit parameters on Read | Prevents single-file context exhaustion |

#### 2.3.3 Context Isolation

Subagents spawned via the Task tool operate in their own context window. They do NOT inherit the parent agent's conversation history, tool results, or reasoning state. This is a feature, not a limitation.

**Context Isolation Benefits:**

| Benefit | Mechanism |
|---------|-----------|
| Fresh reasoning | Subagent starts without the parent's accumulated biases and noise |
| Focused context | Subagent's entire context budget serves a single focused task |
| Security boundary | Subagent cannot access the parent's sensitive intermediate state |
| Parallel execution | Multiple subagents can run concurrently without context interference |

**Context Isolation Costs:**

| Cost | Mitigation |
|------|------------|
| Information loss at handoff boundary | Structured handoff schema (Section 2.1.2) with key_findings |
| Repeated file reads | Accept the cost; isolation value exceeds duplication cost |
| Duplicated guardrail loading | Include guardrails in each agent's system prompt (unavoidable) |

#### 2.3.4 Filesystem-as-Memory Pattern

Jerry's core solution to context rot: use the filesystem as infinite, persistent memory. The context window is working memory (limited, volatile). The filesystem is long-term memory (unlimited, persistent).

```
+-------------------------------------------------------------------+
|             FILESYSTEM-AS-MEMORY ARCHITECTURE                     |
+-------------------------------------------------------------------+
|                                                                   |
|  CONTEXT WINDOW (Working Memory)                                  |
|  +------------------------------------------------------------+  |
|  |  200K tokens, volatile, single-session                      |  |
|  |  Contains: active reasoning, current task state, recent     |  |
|  |  tool results, pending decisions                            |  |
|  +------------------------------------------------------------+  |
|       |            ^                                              |
|       | Write      | Read (selective)                             |
|       v            |                                              |
|  FILESYSTEM (Long-Term Memory)                                    |
|  +------------------------------------------------------------+  |
|  |  Unlimited, persistent, cross-session                       |  |
|  |                                                             |  |
|  |  projects/{proj}/                                           |  |
|  |    PLAN.md              # Strategic intent                  |  |
|  |    WORKTRACKER.md       # Task state                        |  |
|  |    research/            # Research artifacts                |  |
|  |    architecture/        # Architecture docs                 |  |
|  |    decisions/           # ADRs                              |  |
|  |    orchestration/       # Workflow state                    |  |
|  |    critiques/           # Quality assessments               |  |
|  |                                                             |  |
|  |  .context/rules/       # Governance (load selectively)      |  |
|  |  skills/*/agents/      # Agent definitions                  |  |
|  |  .context/templates/   # Output templates                   |  |
|  +------------------------------------------------------------+  |
|       |            ^                                              |
|       | Store      | Retrieve/Search                              |
|       v            |                                              |
|  MCP MEMORY-KEEPER (Cross-Session Memory)                         |
|  +------------------------------------------------------------+  |
|  |  Key-value store, persistent across Claude Code sessions    |  |
|  |  Key pattern: jerry/{project}/{entity-type}/{entity-id}     |  |
|  |  Use case: orchestration phase state, cross-session research|  |
|  +------------------------------------------------------------+  |
+-------------------------------------------------------------------+
```

**Memory Hierarchy:**

| Memory Type | Scope | Persistence | Access Pattern | Token Cost |
|-------------|-------|-------------|----------------|------------|
| Context Window | Single agent execution | Volatile (lost after completion) | Direct (always available) | Part of 200K budget |
| Filesystem | Repository-wide | Persistent (git-backed) | Selective (Read tool on demand) | Per-read (file size) |
| MCP Memory-Keeper | Cross-session | Persistent (MCP server) | Selective (search/retrieve) | Per-read (entry size) |

---

## 3. Design Patterns Catalog

### Pattern 1: Specialist Agent Pattern

**Category:** Structural
**Problem:** A single generalist agent cannot maintain deep expertise across many domains simultaneously. As instructions grow, context rot degrades performance in all areas.
**Solution:** Decompose the generalist into multiple specialist agents, each with focused expertise, a defined cognitive mode, and a restricted tool set. Each specialist operates in its own context window.

```
                     Generalist (anti-pattern)
                     +---------------------+
                     | Research + Analyze + |
                     | Review + Orchestrate |
                     | + Format + Score    |
                     +---------------------+
                              |
                    Decompose by expertise
                              |
            +---------+-------+-------+---------+
            v         v       v       v         v
         +------+ +------+ +------+ +------+ +------+
         | Res. | | Anal.| | Rev. | | Orch.| | Scor.|
         +------+ +------+ +------+ +------+ +------+
         Divergent Converg. Critical Converg. Converg.
```

**When to use:** When the system must handle more than 3 distinct task types requiring different expertise or cognitive modes. When context window is a constraint (it always is).
**When NOT to use:** For simple, single-purpose agents where decomposition adds overhead without benefit. Below the ~3 task-type threshold, a single agent is simpler and sufficient.
**Jerry Implementation:** 37 agents across 8 skills, each with focused expertise (e.g., ps-researcher for research, ps-analyst for analysis, adv-scorer for quality scoring).
**Industry Validation:** CrewAI's role-based model, Anthropic's recommendation to "give subagents focused system prompts," Google DeepMind's contract-first delegation (2025).

---

### Pattern 2: Orchestrator-Worker Pattern

**Category:** Structural
**Problem:** Complex tasks require coordination across multiple specialists. Without orchestration, agents operate as an uncoordinated "bag of agents" (17x error amplification per Google DeepMind).
**Solution:** A single orchestrator agent decomposes complex tasks, delegates to specialist workers via the Task tool, and synthesizes their outputs. The orchestrator handles sequencing, parallelization, and quality gates. Max one level of nesting (P-003/H-01).

```
         +------------------+
         |   ORCHESTRATOR   |
         |  (Lead Agent or  |
         |   orch-planner)  |
         +---+---------+----+
             |         |
        Task Tool  Task Tool
             |         |
         +---v---+ +---v---+
         | W-1   | | W-2   |
         | (opus)| | (son) |
         +---+---+ +---+---+
             |         |
             v         v
          [Artifact] [Artifact]
             |         |
             +----+----+
                  |
                  v
         +------------------+
         |   ORCHESTRATOR   |
         |  (synthesizes)   |
         +------------------+
```

**When to use:** When a task requires 3+ distinct expertise areas (research + analysis + architecture). When outputs must be coordinated and cross-referenced. When parallel execution can reduce total wall-clock time.
**When NOT to use:** For single-domain tasks that one specialist can handle. When the coordination overhead exceeds the benefit (simple tasks).
**Jerry Implementation:** `/orchestration` skill with orch-planner (designs workflow), orch-tracker (manages state), orch-synthesizer (cross-pipeline synthesis). PROJ-007 itself uses this pattern with PS and NSE pipelines running in parallel with sync barriers.
**Industry Validation:** Anthropic's "Orchestrator-Workers" pattern (5 composable workflows), LangGraph's orchestrator-worker with `Send()` for parallel execution, CrewAI's Flows.

---

### Pattern 3: Creator-Critic-Revision Pattern

**Category:** Quality
**Problem:** Self-review alone cannot reliably detect blind spots. Single-pass output quality is insufficient for important (C2+) deliverables. Leniency bias causes agents to rate their own work too favorably.
**Solution:** A creator agent produces the deliverable. An independent critic agent (or adversary) evaluates it against quality criteria using a structured rubric (S-014 LLM-as-Judge). The creator revises based on critique. Minimum 3 iterations (H-14). The Steelman technique (S-003) is applied before Devil's Advocate (S-002) per H-16.

```
    Iteration 1          Iteration 2          Iteration 3
    +--------+           +--------+           +--------+
    | CREATE |           | REVISE |           | REVISE |
    +---+----+           +---+----+           +---+----+
        |                    |                    |
        v                    v                    v
    +--------+           +--------+           +--------+
    | CRITIC |           | CRITIC |           | CRITIC |
    | Score: |           | Score: |           | Score: |
    | 0.78   |           | 0.88   |           | 0.93   |
    +---+----+           +---+----+           +---+----+
        |                    |                    |
    REJECTED             REJECTED             ACCEPTED
    (< 0.92)             (< 0.92)             (>= 0.92, H-13)
```

**When to use:** All C2+ deliverables (H-14 mandates this). Documents that will be baselined or consumed by downstream agents. Architecture decisions, requirements specifications, trade studies.
**When NOT to use:** C1 (routine) work that is reversible within a single session. Status reports, simple file transforms.
**Jerry Implementation:** ps-critic agent evaluates deliverables in creator-critic loops. adv-scorer applies S-014 LLM-as-Judge with 6-dimension rubric (Completeness 0.20, Internal Consistency 0.20, Methodological Rigor 0.20, Evidence Quality 0.15, Actionability 0.15, Traceability 0.10). Quality gate threshold: >= 0.92 weighted composite.
**Industry Validation:** ACM multi-agent QA methodology (2025), Evaluator-Optimizer pattern (Anthropic), LangChain's finding that quality is the #1 production blocker (32% of respondents).

---

### Pattern 4: Progressive Disclosure Pattern

**Category:** Context Management
**Problem:** Loading all agent knowledge at once exhausts the context window before the agent begins its actual work. Large agent definitions (615 lines for ps-researcher) cannot all be resident simultaneously.
**Solution:** Organize agent context into three tiers loaded at different times: metadata (always), core (on invocation), supplementary (on demand). Each tier is progressively more detailed but only loaded when needed.

```
    Session Start          Agent Invoked          During Execution
    +-------------+        +-------------+        +-------------------+
    | TIER 1:     |        | TIER 2:     |        | TIER 3:           |
    | Metadata    |------->| Core        |------->| Supplementary     |
    | (~500 tok)  |        | (~5K tok)   |        | (variable)        |
    | Skill desc, |        | Full YAML+  |        | Templates, prior  |
    | triggers    |        | MD body     |        | work, examples    |
    +-------------+        +-------------+        +-------------------+
    "I know what                "I know how           "I have specific
     agents exist"               to think"              reference data"
```

**When to use:** Always. This is a universal pattern for all agent frameworks operating within finite context windows.
**When NOT to use:** There is no case where loading all context upfront is preferable. Even for small systems, progressive disclosure creates good habits.
**Jerry Implementation:** SKILL.md `description` field (Tier 1), agent definition file (Tier 2), Read tool for templates/prior work (Tier 3). The sb-rewriter agent demonstrates this well: always-loads voice-guide.md + vocabulary-reference.md, reads other references only on demand.
**Industry Validation:** Anthropic's "Agent Skills" engineering blog post (2025), Google's context engineering discipline (2025), Context Rot research by Chroma (2024).

---

### Pattern 5: Tool Restriction Pattern

**Category:** Security/Governance
**Problem:** Giving all agents access to all tools violates the principle of least privilege. A review-only agent with write access could accidentally modify the file it is reviewing. An adversarial scoring agent with web access might look up "correct" answers instead of independently evaluating quality.
**Solution:** Assign each agent the minimum set of tools required for its task. Define security tiers (T1-T5) that group tools by privilege level. Higher-tier access requires explicit justification.

```
    +--------------------------------------------+
    | T1: Read-Only     | Read, Glob, Grep       |
    |   adv-executor, adv-scorer, wt-auditor     |
    +--------------------------------------------+
    | T2: Read-Write    | T1 + Write, Edit, Bash |
    |   ps-analyst, nse-architecture             |
    +--------------------------------------------+
    | T3: External      | T2 + WebSearch, Fetch, |
    |                   |      Context7           |
    |   ps-researcher, nse-explorer              |
    +--------------------------------------------+
    | T4: Persistent    | T2 + Memory-Keeper     |
    |   orch-planner, orch-tracker               |
    +--------------------------------------------+
    | T5: Full          | T3 + T4 + Task         |
    |   Lead agent (rare)                        |
    +--------------------------------------------+
```

**When to use:** Always. Every agent definition must declare its tool profile. Prefer T1 (read-only) as the default; justify upward.
**When NOT to use:** There is no valid reason to skip tool restriction. The "give all tools and hope for the best" approach is the Dynamic Tool Selection anti-pattern (E2 in the trade study, scored lowest at 2.90).
**Jerry Implementation:** `capabilities.allowed_tools` in YAML frontmatter, enforced by Claude Code's Task tool configuration. TOOL_REGISTRY.yaml as SSOT.
**Industry Validation:** MCP specification's server capabilities model, Anthropic's recommendation for "explicit tool configuration for production use cases," principle of least privilege (InfoSec standard).

---

### Pattern 6: Structured Handoff Pattern

**Category:** Integration
**Problem:** Free-text handoffs between agents cause information loss. Key findings are buried in prose. Schema mismatches cause downstream agents to misinterpret upstream output. Google (2026) identifies this as the #1 failure source in production multi-agent systems.
**Solution:** Define a JSON Schema for handoff data. Every agent-to-agent transition includes structured fields: artifacts (file paths), key_findings (3-5 bullets), blockers, confidence score, and criticality level. Handoff schemas are validated on send and receive.

```
    AGENT A (sender)                    AGENT B (receiver)
    +-------------------+               +-------------------+
    | 1. Complete work  |               | 1. Validate schema|
    | 2. Populate       |               | 2. Read artifacts |
    |    session_context|    handoff     | 3. Orient via     |
    |    .on_send       |  ---------->  |    key_findings   |
    | 3. Serialize to   |   (JSON)      | 4. Check blockers |
    |    JSON schema    |               | 5. Begin work     |
    +-------------------+               +-------------------+
```

**When to use:** Every agent-to-agent transition, without exception. Even for "simple" handoffs, the structured schema prevents drift.
**When NOT to use:** Direct user-to-agent interactions (user prompt is the input, not a structured handoff). Single-agent tasks with no downstream consumers.
**Jerry Implementation:** `session_context` section in agent YAML frontmatter with `on_receive` and `on_send` hooks. JSON schema at `docs/schemas/session_context.json`. Current handoff example in AGENTS.md Section "Agent Handoff Protocol."
**Industry Validation:** Google DeepMind's contract-first delegation (2025), LangGraph's typed state dictionaries, OpenAI Agents SDK handoff mechanism.

---

### Pattern 7: Context Budget Pattern

**Category:** Context Management
**Problem:** Context window exhaustion causes mid-task failures. Agents that read too many files early in execution have insufficient context remaining for reasoning and output generation.
**Solution:** Allocate the 200K context window into explicit budget categories: system prompt (~5%), user messages (~15%), tool results (~45%), reasoning + output (~30%), safety margin (~5%). Agents should monitor consumption and prefer targeted reads over bulk reads.

```
    +----------------------------------------------------+
    |              200K CONTEXT WINDOW                   |
    +----------------------------------------------------+
    | System Prompt  |  ~10K  |  Agent def + rules       |
    |----------------+--------+--------------------------|
    | User Messages  |  ~30K  |  Task + handoff data     |
    |----------------+--------+--------------------------|
    | Tool Results   |  ~90K  |  File reads, web, MCP    |
    |----------------+--------+--------------------------|
    | Reasoning      |  ~60K  |  Chain of thought +      |
    |  + Output      |        |  final deliverable       |
    |----------------+--------+--------------------------|
    | Safety Margin  |  ~10K  |  Prevents truncation     |
    +----------------------------------------------------+
```

**When to use:** All agents should be designed with context budget awareness. Particularly critical for research agents (ps-researcher) that read many external sources.
**When NOT to use:** Not applicable -- all agents benefit from budget awareness.
**Jerry Implementation:** Python environment rule for transcript files (H-05 large file handling: never read canonical-transcript.json at ~930KB). Read tool's `offset`/`limit` parameters for long files. Key findings (3-5 bullets) in handoffs instead of full inline content.
**Industry Validation:** Anthropic's "context engineering" discipline, Claude Agent SDK `compact` feature for context management, Chroma's context rot research.

---

### Pattern 8: Quality Gate Pattern

**Category:** Quality/Governance
**Problem:** Quality varies across agent outputs. Without explicit quality enforcement, substandard deliverables propagate through the pipeline and compound errors. 32% of production agent deployments cite quality as the #1 blocker (LangChain, 2025).
**Solution:** Insert quality gates at defined checkpoints -- typically at agent output boundaries, phase boundaries, and handoff points. Each gate applies proportional enforcement based on criticality level (C1-C4). Gates use a layered QA architecture: deterministic schema validation, self-review (S-010), and critic-scored assessment (S-014).

```
    Agent Output
         |
         v
    +-------------------+
    | GATE LAYER 1:     |
    | Schema Validation | -----> REJECT if malformed
    | (deterministic)   |
    +--------+----------+
             |
             v
    +-------------------+
    | GATE LAYER 2:     |
    | Self-Review       | -----> Self-correct if issues found
    | (S-010, H-15)     |
    +--------+----------+
             |
             v (C2+ only)
    +-------------------+
    | GATE LAYER 3:     |
    | Critic Review     | -----> REJECT if score < 0.92 (H-13)
    | (S-014 LLM-as-    |        Route to revision cycle (H-14)
    |  Judge, 6-dim)    |
    +-------------------+
             |
             v
    +-------------------+
    | GATE LAYER 4:     | -----> Full tournament (C4 only)
    | Tournament Mode   |        All 10 strategies
    | (All strategies)  |
    +-------------------+
             |
             v
         ACCEPTED
```

**Criticality-Proportional Application:**

| Criticality | Layer 1 (Schema) | Layer 2 (Self-Review) | Layer 3 (Critic) | Layer 4 (Tournament) |
|-------------|------------------|-----------------------|-------------------|---------------------|
| C1 Routine | Required | Required | Optional | -- |
| C2 Standard | Required | Required | Required (3 iter) | -- |
| C3 Significant | Required | Required | Required + strategies | Optional |
| C4 Critical | Required | Required | Required | Required |

**When to use:** Every agent output. The level of scrutiny is proportional to criticality, but Layer 1 (schema) and Layer 2 (self-review) are universally applied.
**When NOT to use:** Not applicable. Quality gates are always on; the question is how many layers to apply.
**Jerry Implementation:** H-13 (threshold >= 0.92), H-14 (3 min iterations), H-15 (self-review), H-17 (scoring required). Operational score bands: PASS (>= 0.92), REVISE (0.85-0.91), REJECTED (< 0.85). See `quality-enforcement.md` for full SSOT.
**Industry Validation:** ACM multi-agent QA methodology, AgentSLA extending ISO/IEC 25010, LangChain State of Agent Engineering.

---

### Pattern 9: Cognitive Mode Pattern

**Category:** Behavioral
**Problem:** Different tasks require fundamentally different thinking approaches. A research task needs broad, exploratory reasoning (divergent). A review task needs focused, evaluative reasoning (convergent). Using the wrong cognitive mode for a task produces poor results -- a researcher who converges too early misses important sources; a reviewer who diverges explores irrelevant tangents.
**Solution:** Assign each agent an explicit cognitive mode that shapes its reasoning strategy, output structure, and iteration behavior. The mode is declared in YAML frontmatter (`identity.cognitive_mode`) and reinforced in the Markdown behavioral sections.

| Mode | Reasoning Strategy | Output Pattern | Iteration Behavior |
|------|-------------------|----------------|-------------------|
| **Divergent** | Explore broadly, generate multiple hypotheses, defer evaluation | Multiple alternatives, options lists, broad coverage | Expand search space on each iteration |
| **Convergent** | Analyze narrowly, apply criteria, select from options | Ranked recommendations, selected alternatives, focused analysis | Narrow from options to decision on each iteration |
| **Integrative** | Correlate across sources, identify patterns, synthesize themes | Unified narratives, cross-reference tables, gap analysis | Build coherence across inputs on each iteration |
| **Systematic** | Follow procedures, verify compliance, check completeness | Checklists, pass/fail tables, compliance matrices | Process items sequentially without skipping |
| **Forensic** | Trace backward from symptoms, test hypotheses, isolate causes | Root cause chains, evidence correlation, 5 Whys | Narrow hypothesis space on each iteration |

**When to use:** Every agent must have an explicit cognitive mode. Mode selection should be driven by the agent's primary task type, not by the domain.
**When NOT to use:** Not applicable -- cognitive mode is a required attribute of every agent definition.
**Jerry Implementation:** `identity.cognitive_mode` in YAML frontmatter (divergent, convergent, integrative, systematic). Reinforced in `<identity>` XML tag in Markdown body. Examples: ps-researcher (divergent), ps-analyst (convergent), ps-synthesizer (integrative), ps-validator (systematic), ps-investigator (forensic).
**Industry Validation:** Anthropic's recommendation for "distinct personas" in subagents, PromptHub research on role-prompting effectiveness (2025), CrewAI's role-based agent model.

---

### Pattern 10: Layered Routing Pattern

**Category:** Integration
**Problem:** A single routing mechanism cannot handle the full spectrum from clear to ambiguous requests. Keyword matching is fast but brittle. LLM routing is intelligent but slow and stochastic. Neither alone is sufficient.
**Solution:** Implement a layered routing architecture with fast deterministic routing as the primary path and LLM-based routing as a fallback for ambiguous cases.

```
    User Request
         |
         v
    +--------------------+
    | LAYER 1:           |
    | Keyword Matching   |-----> Match found?
    | (mandatory-skill-  |       Yes: Route to skill (fast path)
    |  usage.md trigger  |       ~1ms latency
    |  map)              |
    +--------+-----------+
             |
             | No match or multiple matches
             v
    +--------------------+
    | LAYER 2:           |
    | Rule-Based         |-----> Decision tree resolves?
    | Decision Tree      |       Yes: Route to skill
    | (criticality,      |       ~1ms latency
    |  task type,        |
    |  context clues)    |
    +--------+-----------+
             |
             | Still ambiguous
             v
    +--------------------+
    | LAYER 3:           |
    | LLM-as-Router      |-----> Route to skill
    | (lightweight LLM   |       ~300-500ms latency
    |  call with skill   |       Provides routing explanation
    |  catalog)          |
    +--------------------+
```

**When to use:** Any system with more than 5 routing targets (skills, agents). When the trigger map has keyword overlaps or gaps. When novel request types must be handled gracefully.
**When NOT to use:** Single-skill systems or systems where all requests are deterministically classifiable. When routing latency is the primary constraint.
**Jerry Implementation:** Currently at Layer 1 only (keyword matching via `mandatory-skill-usage.md` trigger map). Layer 2 is partially implemented via skill routing decision tables in `quality-enforcement.md`. Layer 3 is a recommended enhancement (trade study finding C5, scored 3.90).
**Industry Validation:** Arize AI routing best practices (2025), AWS multi-LLM routing research (75% cost reduction), Medium routing analysis (300ms thin router vs. 5s ReACT).

---

## 4. Architecture Decision Records

### ADR-001: Agent Definition Format

**Status:** Recommended (pending human review)

**Context:**
Jerry currently uses YAML frontmatter + Markdown body (pattern B1) for agent definitions. This format is proven across 37 agents but lacks schema validation. The Phase 1 trade study evaluated 5 alternatives and scored B5 (Hybrid Schema-Validated Markdown) highest at 4.45 vs. B1 at 4.00.

**Decision:**
Adopt the Hybrid Schema-Validated Markdown approach (B5): retain the current YAML+MD format and add JSON Schema validation for YAML frontmatter fields. Define a required section checklist enforced by CI tooling.

**Rationale:**
- Backward-compatible with all 37 existing agent definitions
- Catches structural errors (missing required fields, invalid formats) deterministically at CI time
- Preserves the expressiveness of Markdown behavioral sections
- Low migration cost: existing agents pass validation or receive automated fixes
- Aligns with Open Agent Specification direction (YAML/JSON with schema validation)

**Schema Elements (Draft):**

| YAML Field | Required | Type | Validation |
|------------|----------|------|------------|
| `name` | Yes | string | Pattern: `^[a-z]+-[a-z]+(-[a-z]+)?$` |
| `version` | Yes | string | SemVer pattern |
| `description` | Yes | string | Max 1024 chars, no XML (H-28) |
| `model` | Yes | enum | `opus`, `sonnet`, `haiku` |
| `identity.role` | Yes | string | Non-empty |
| `identity.cognitive_mode` | Yes | enum | `divergent`, `convergent`, `integrative`, `systematic`, `forensic` |
| `capabilities.allowed_tools` | Yes | array | Each must be a known tool name |
| `capabilities.forbidden_actions` | Yes | array | Must include P-003, P-020 |
| `guardrails` | Yes | object | Must include `input_validation` and `fallback_behavior` |
| `output.required` | Yes | boolean | -- |
| `constitution.principles_applied` | Yes | array | Must include P-003, P-022 |

**Required Markdown Sections:**

| Section Tag | Required For | Purpose |
|-------------|-------------|---------|
| `<identity>` | All agents | Role and expertise narrative |
| `<purpose>` | All agents | Mission statement |
| `<input>` | All agents | Expected input format |
| `<methodology>` | Document producers, decision makers | Step-by-step process |
| `<output>` | All agents | Output specification |
| `<guardrails>` | All agents | Safety and compliance narrative |

**Consequences:**
- Positive: Deterministic structural validation at CI time; catches errors before agent invocation.
- Positive: Required section checklist prevents incomplete agent definitions.
- Negative: JSON Schema must be maintained alongside agent definitions.
- Negative: Initial effort to create schema and validate all 37 existing agents.

**Alternatives Considered:**
- B2 (Pure YAML/JSON): Loses behavioral expressiveness. Score: 3.75.
- B3 (Code-First): Requires Python knowledge. Score: 3.60.
- B4 (DSL): Custom language maintenance burden. Score: 3.25.

---

### ADR-002: Agent Routing Architecture

**Status:** Recommended (pending human review)

**Context:**
Jerry currently uses keyword matching for routing (pattern C1 via `mandatory-skill-usage.md`). This is fast and deterministic but brittle for ambiguous or novel requests. The Phase 1 trade study scored C5 (Layered Routing) highest at 3.90 vs. C1 at 3.85.

**Decision:**
Adopt Layered Routing (C5): retain keyword matching as the fast path (Layer 1), add a rule-based decision tree for multi-signal resolution (Layer 2), and add LLM-based fallback for ambiguous cases (Layer 3).

**Rationale:**
- Preserves deterministic routing for ~80% of clear-match cases (fast path)
- Handles the ~20% of ambiguous cases that keyword matching misses
- Graceful degradation: if LLM router is unavailable, falls back to Layer 1+2
- Layer 3 can log its routing decisions, identifying keyword gaps for Layer 1 improvement
- Compatible with H-22 (proactive skill invocation) and existing trigger map

**Implementation Sketch:**

```
Layer 1: mandatory-skill-usage.md trigger map (existing)
  - Exact keyword match: route immediately
  - No match: proceed to Layer 2

Layer 2: Rule-based decision tree (new)
  - Evaluate: task type (research/analysis/review/orchestrate)
  - Evaluate: criticality signals (touches governance, API changes)
  - Evaluate: prior context (what skill was last used)
  - Clear resolution: route
  - Ambiguous: proceed to Layer 3

Layer 3: LLM-as-router (new)
  - Lightweight LLM call (~3 token response: skill name)
  - Input: user request + skill catalog summary
  - Output: selected skill name + brief justification
  - Log routing decision for Layer 1 keyword gap analysis
```

**Consequences:**
- Positive: Better handling of ambiguous and compound requests.
- Positive: Feedback loop from Layer 3 logging improves Layer 1 over time.
- Negative: Layers 2 and 3 add implementation complexity.
- Negative: Layer 3 introduces stochasticity for a small percentage of requests.
- Negative: Layer 3 adds ~300-500ms latency for ambiguous cases.

**Alternatives Considered:**
- C2 (Semantic Similarity): Requires embedding infrastructure. Score: 3.45.
- C3 (LLM-Router only): All routes go through LLM. Score: 3.35.
- C4 (Decision Tree only): Deterministic but cannot handle novel patterns. Score: 3.80.
- C6 (Intent Classification): Requires labeled training data. Score: 3.10.

---

### ADR-003: Quality Assurance Architecture

**Status:** Recommended (pending human review)

**Context:**
Jerry currently uses a creator-critic-revision cycle (D2) for C2+ deliverables, with self-review (D1/S-010) for all outputs and tournament mode (D3) for C4. The Phase 1 trade study identified an opportunity to add deterministic schema validation (D5) as a fast pre-check layer, creating a layered QA architecture (D6).

**Decision:**
Adopt Layered QA (D6): add schema validation as Layer 1 before self-review (Layer 2) and critic review (Layer 3). Schema validation catches structural defects deterministically with zero LLM cost.

**Rationale:**
- Schema validation is deterministic, fast, and free (no LLM cost)
- Catches structural issues (missing nav table H-23, missing anchor links H-24, missing L0/L1/L2 levels) before consuming critic context tokens
- Reduces critic workload: critic focuses on content quality, not structural completeness
- Proportional enforcement: C1 gets Layers 1+2; C2+ gets Layers 1+2+3; C4 gets all 4
- Aligns with the existing 5-layer enforcement architecture (L1-L5)

**Layer Definitions:**

| Layer | Mechanism | Cost | Catches |
|-------|-----------|------|---------|
| 1. Schema Validation | JSON Schema / checklist | Zero LLM tokens | Missing sections, malformed metadata, structural defects |
| 2. Self-Review (S-010) | Agent self-assessment | ~2,000 tokens | Obvious content issues, internal inconsistencies |
| 3. Critic Review (S-014) | Independent LLM evaluation | ~5,000-10,000 tokens per iteration | Blind spots, quality scoring, rubric compliance |
| 4. Tournament (All S-*) | All 10 adversarial strategies | ~50,000+ tokens | Maximum coverage for irreversible decisions |

**Consequences:**
- Positive: Structural defects caught before any LLM evaluation (cheaper, faster, deterministic).
- Positive: Critic can focus exclusively on content quality, improving evaluation precision.
- Negative: Output schemas must be designed and maintained for each agent output type.
- Negative: Schema design requires upfront investment (amortized over all future deliverables).

**Alternatives Considered:**
- D1 (Self-Review Only): Insufficient for C2+ per H-14. Score: 3.85 (but filtered by constraint).
- D2 (Creator-Critic Only): Current pattern. Missing deterministic pre-check. Score: 3.30.
- D3 (Full Tournament): Too expensive for routine work. Score: 2.70.
- D4 (Statistical Monitoring): Complementary but does not prevent individual defects. Score: 3.25.

---

## 5. Self-Review (S-010)

Applied S-010 Self-Refine before finalizing this document. The following checklist verifies completeness and quality.

### Completeness Verification

| Required Section | Present | Notes |
|-----------------|---------|-------|
| L0 Architecture Summary | Yes | Plain-language overview with 4 key decisions |
| 1.1 Hexagonal Architecture Mapping | Yes | ASCII diagram + layer definitions + dependency rule |
| 1.2 Agent Anatomy Diagram | Yes | File structure, runtime model, context flow, lifecycle |
| 1.3 Agent Type Taxonomy | Yes | 4 dimensions (cognitive, autonomy, output, tools) + combined matrix |
| 2.1 Agent-to-Agent Communication | Yes | Invocation, handoff schema, context passing, artifact formats |
| 2.2 Agent-to-Tool Integration | Yes | Static assignment, restriction tiers, MCP patterns, result handling |
| 2.3 Agent-to-Context Integration | Yes | Progressive disclosure, budget, isolation, filesystem-as-memory |
| 3. Design Patterns Catalog (10 patterns) | Yes | All 10 patterns with problem/solution/when/Jerry/industry |
| 4. ADR-001 (Definition Format) | Yes | Context, decision, rationale, consequences, alternatives |
| 4. ADR-002 (Routing) | Yes | Context, decision, rationale, consequences, alternatives |
| 4. ADR-003 (QA Architecture) | Yes | Context, decision, rationale, consequences, alternatives |

### Quality Checks

| Check | Result | Notes |
|-------|--------|-------|
| H-23: Navigation table present | PASS | Document Sections table at top |
| H-24: Anchor links in navigation | PASS | All sections use anchor links |
| L0/L1/L2 structure | PASS | L0 summary, L1 technical detail, L2 strategic ADRs |
| ASCII diagrams included | PASS | 10+ diagrams across all major sections |
| Pattern catalog with examples | PASS | 10 patterns, each with Jerry + industry validation |
| Trade study findings incorporated | PASS | All 5 trade study recommendations reflected |
| PS cross-pollination findings incorporated | PASS | All 10 consensus findings addressed |
| Current Jerry architecture accurately represented | PASS | 37 agents, 8 skills, verified against AGENTS.md |
| P-003/H-01 compliance | PASS | Single-level constraint noted throughout |
| Mandatory NASA disclaimer | PASS | Present at document top |

### Identified Gaps (For Future Work)

| Gap | Impact | Suggested Resolution |
|-----|--------|---------------------|
| JSON Schema for handoff data not yet implemented | Medium | Create `docs/schemas/session_context.json` from the schema in Section 2.1.2 |
| Agent definition JSON Schema not yet implemented | Medium | Create `docs/schemas/agent_definition.json` from ADR-001 schema elements |
| Layer 2 and Layer 3 routing not yet implemented | Medium | Implement per ADR-002 specification |
| Output schema templates not yet created | Medium | Create per-output-type schemas per ADR-003 |
| Combined taxonomy matrix covers only 13 of 37 agents | Low | Extend matrix to cover all 37 agents in a future iteration |

---

## References

### Input Sources

| # | Source | Content |
|---|--------|---------|
| 1 | `nse-explorer-001-agent-design-alternatives.md` | Phase 1 trade study with 5 trade study areas, 25 alternatives evaluated |
| 2 | `cross-pollination/barrier-1/ps-to-nse/handoff.md` | PS pipeline findings synthesis: 10 consensus findings, 67+ sources |
| 3 | `.context/rules/architecture-standards.md` | Jerry hexagonal architecture, CQRS, H-07 through H-10 |
| 4 | `AGENTS.md` | Agent registry: 37 agents, 8 skills, handoff protocol |
| 5 | `skills/problem-solving/agents/ps-researcher.md` | Representative agent definition: 615 lines, YAML+MD, Context7 |
| 6 | `skills/nasa-se/agents/nse-architecture.md` | Representative agent definition: convergent, architecture focus |
| 7 | `skills/adversary/agents/adv-executor.md` | Representative agent definition: read-only tools, strategy execution |
| 8 | `skills/orchestration/agents/orch-planner.md` | Representative agent definition: Memory-Keeper, state management |

### External Sources (Via Phase 1 Research)

| # | Source | Key Insight |
|---|--------|-------------|
| 9 | Anthropic - Claude Code Best Practices (2025) | Four-stage feedback cycle, subagent configuration |
| 10 | Anthropic - Building Agents with Claude Agent SDK (2025) | Context management, tool design, compact feature |
| 11 | Anthropic - Agent Skills (2025) | Progressive disclosure, skills as composable capabilities |
| 12 | Google DeepMind - Contract-First Delegation (2025) | Structured handoffs, 17x error amplification without topology |
| 13 | MCP Specification 2025-11-25 | Tool capability declaration, discovery, invocation |
| 14 | LangGraph Documentation | Orchestrator-worker, StateGraph, typed state |
| 15 | CrewAI Architecture | Role-based agents, Crews + Flows |
| 16 | ACM Multi-Agent QA Methodology (2025) | Multi-agent evaluation produces more robust solutions |
| 17 | LangChain State of Agent Engineering (2025) | Quality is #1 blocker (32%), 89% have observability |
| 18 | Arize AI - Agent Routing Best Practices (2025) | Routing mechanism taxonomy and recommendations |
| 19 | Open Agent Specification (2025) | YAML/JSON agent schema with validation |
| 20 | Chroma - Context Rot Research (2024) | LLM performance degradation with context fill |

---

*Generated by nse-architecture-001 agent v2.1.0*
*NASA Processes: NPR 7123.1D Process 3 (Logical Decomposition), Process 4 (Design Solution), Process 17 (Decision Analysis)*
*Self-Review (S-010) Applied: All required sections verified, quality checks passed, gaps documented*
