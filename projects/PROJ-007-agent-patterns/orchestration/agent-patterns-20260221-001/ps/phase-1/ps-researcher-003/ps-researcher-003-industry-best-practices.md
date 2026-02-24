# PS-Researcher-003: Industry Best Practices, Community Patterns, and Prior Art for AI Agent Systems

<!-- VERSION: 1.0.0 | DATE: 2026-02-21 | PS-ID: PROJ-007 | ENTRY-ID: e-003 -->

> Comprehensive research on established patterns, frameworks, and best practices for building AI agent systems, sourced from industry leaders, framework documentation, and community practitioners.

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | ELI5 overview of the agent landscape |
| [L1 Detailed Findings](#l1-detailed-findings) | Research question analysis with evidence |
| [L2 Strategic Analysis](#l2-strategic-analysis) | Pattern taxonomy, framework matrix, implications |
| [Agent Pattern Taxonomy](#agent-pattern-taxonomy) | Categorized pattern catalog |
| [Framework Comparison Matrix](#framework-comparison-matrix) | Multi-dimensional framework comparison |
| [Best Practice Consensus](#best-practice-consensus) | Cross-source agreement analysis |
| [Emerging Trends](#emerging-trends) | Novel approaches gaining traction |
| [Source Registry](#source-registry) | All citations with classification |
| [Self-Review Checklist](#self-review-checklist) | S-010 verification |

---

## L0 Executive Summary

The AI agent landscape in 2025-2026 has matured from experimental chatbot wrappers into a well-defined engineering discipline with established design patterns, production frameworks, and governance models. The field converges on a core insight articulated by every major industry player: **start simple, add complexity only when demonstrably needed**. Anthropic, OpenAI, Google, and Microsoft all advocate beginning with optimized single LLM calls before graduating to workflow orchestrations and then to fully autonomous agents. The most effective agent systems use composable building blocks -- prompt chaining, routing, parallelization, orchestrator-workers, and evaluator-optimizer loops -- rather than monolithic, complex architectures.

Multi-agent orchestration has become the dominant paradigm for complex tasks, with frameworks like LangGraph (graph-based state machines), CrewAI (role-based crew collaboration), and Microsoft's Agent Framework (enterprise orchestration patterns) providing production-ready infrastructure. Google's Agent Development Kit (ADK) codifies eight essential patterns ranging from sequential pipelines to human-in-the-loop architectures. A critical consensus has emerged around **context engineering** as the defining challenge: managing the finite context window through compaction, sub-agent isolation, structured note-taking, and progressive disclosure is what separates production agents from demos. Agent Skills -- modular capability packages with progressive disclosure -- represent a maturing pattern for extending agent capabilities without context bloat.

The governance and safety dimension has moved from optional to mandatory. Guardrails, constitutional AI constraints, red teaming, and human-in-the-loop approval gates are now considered table stakes for production deployments. Testing has evolved beyond unit tests to include LLM-as-judge evaluations, end-to-end behavioral testing, and continuous monitoring for drift. Gartner predicts 40% of enterprise applications will embed AI agents by end of 2026, with the market projected to reach $52.62 billion by 2030. The field is decisively moving from experimentation to operational deployment, with bounded autonomy -- agents acting independently where outcomes are predictable while keeping humans involved when risk increases -- emerging as the dominant deployment philosophy.

---

## L1 Detailed Findings

### RQ-1: Established Agent Design Patterns from Authoritative Sources

#### Anthropic: Building Effective Agents

Anthropic's canonical guide ([Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)) establishes the foundational distinction between **workflows** ("systems where LLMs and tools are orchestrated through predefined code paths") and **agents** ("systems where LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks"). This distinction is critical for architectural decisions.

**Five Workflow Patterns:**

1. **Prompt Chaining**: Sequential steps where each LLM call processes prior outputs, with programmatic "gates" for quality checks between stages. Best for tasks decomposable into fixed subtasks where latency-accuracy tradeoffs are acceptable. Example: document outline -> validation -> full document writing.

2. **Routing**: Classifies inputs and directs them to specialized followup tasks. Enables separation of concerns and task-specific optimization. Example: routing simple queries to Claude Haiku, complex ones to Claude Sonnet.

3. **Parallelization**: Simultaneous LLM work with aggregated outputs. Two variations: *sectioning* (independent subtasks in parallel) and *voting* (same task executed multiple times for diversity). Example: guardrails with separate screening/response calls.

4. **Orchestrator-Workers**: Central LLM dynamically breaks tasks, delegates to worker LLMs, synthesizes results. Key distinction from parallelization: subtasks determined by orchestrator at runtime, not predefined. Example: multi-file code modifications.

5. **Evaluator-Optimizer**: One LLM generates, another evaluates in iterative loops. Requires clear evaluation criteria and demonstrable improvement potential. Example: literary translation refinement.

**Three Core Implementation Principles:**
- **Simplicity**: Straightforward agent design avoiding unnecessary complexity
- **Transparency**: Explicitly display agent planning steps
- **Agent-Computer Interface (ACI)**: Tool documentation crafted with same rigor as human-computer interfaces

**Source:** [Anthropic Research -- Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) | Classification: Industry Leader

#### Anthropic: Effective Harnesses for Long-Running Agents

Anthropic's harness guide ([Effective Harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)) addresses multi-session agent persistence:

- **Initializer Agent**: First session establishes infrastructure (init.sh scripts, progress files, initial git commits)
- **Coding Agent**: Subsequent sessions follow structured patterns -- work on single features sequentially, commit changes with descriptive messages, write progress summaries enabling quick context restoration
- **State Recovery Protocol**: Sessions begin by checking working directory, reading git logs and progress files, reviewing feature lists
- **Feature List (JSON)**: Comprehensive enumeration of requirements with pass/fail tracking prevents premature completion declarations

**Source:** [Anthropic Engineering -- Effective Harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) | Classification: Industry Leader

#### OpenAI: A Practical Guide to Building Agents

OpenAI's guide ([Practical Guide](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/)) identifies two main orchestration patterns:

- **Manager Pattern**: Central LLM orchestrates specialized agents through tool calls, synthesizing results into cohesive interactions
- **Decentralized Pattern**: Agents handoff workflow execution to one another via one-way transfers

**Key Best Practices:**
- Start with incremental approach rather than complex architecture
- Architecture over prompts: structured workflows, persistent sessions, clean architecture
- Use structured outputs for machine-parseable agent communication
- Restrict and consolidate tool calls to reduce ambiguity
- Shift to higher-level guidance rather than prescriptive prompting -- GPT-5's reasoning performs better with flexibility

**Source:** [OpenAI -- Practical Guide to Building Agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/) | Classification: Industry Leader

#### Google: Eight Essential Multi-Agent Design Patterns

Google's ADK guide ([Developer's Guide to Multi-Agent Patterns](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/)) codifies eight patterns:

1. **Sequential Pipeline**: Linear workflow, agents pass outputs via shared state
2. **Coordinator/Dispatcher**: Central agent analyzes intent, routes to specialists
3. **Parallel Fan-Out/Gather**: Concurrent execution with result aggregation
4. **Hierarchical Decomposition**: Parent agents break goals into sub-tasks, treat sub-agents as tools
5. **Generator and Critic**: One agent generates, another validates with conditional looping
6. **Iterative Refinement**: Cycle through generation/critique/refinement until quality thresholds met
7. **Human-in-the-Loop**: Agents handle routine work, pause for human authorization on high-stakes decisions
8. **Composite Patterns**: Real applications combine multiple patterns

**Best Practices:**
- Use descriptive `output_key` values in session state
- Sub-agent descriptions function as "API documentation for the LLM"
- Start with sequential chains before adding nested loops

**Source:** [Google Developers Blog -- Multi-Agent Patterns in ADK](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/) | Classification: Industry Leader

#### Google DeepMind: Intelligent AI Delegation Framework

Google DeepMind published a framework for intelligent AI delegation (February 2026) addressing the "agentic web":

- **Contract-First Principles**: A delegator cannot assign a task unless the outcome can be precisely verified
- **Recursive Decomposition**: If a task is too subjective or complex to verify, recursively decompose until sub-tasks match automated verification capabilities
- **Scaling Principles**: Quantitative scaling principles for agent systems, moving from heuristic to principled design

**Source:** [Google DeepMind -- AI Agent Delegation Framework](https://creati.ai/ai-news/2026-02-17/google-deepmind-ai-agent-delegation-framework/) | Classification: Industry Leader

#### Microsoft: AI Agent Orchestration Patterns

Microsoft's Azure Architecture Center ([AI Agent Design Patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns)) defines five orchestration patterns with detailed implementation guidance:

1. **Sequential Orchestration** (pipeline/prompt chaining): Linear pipeline with clear stage dependencies. Anti-patterns: failures propagate, no parallelism.

2. **Concurrent Orchestration** (fan-out/fan-in): Parallel independent processing with aggregation. Supports deterministic or dynamic agent selection. Requires conflict resolution strategy.

3. **Group Chat Orchestration** (roundtable/debate): Shared conversation thread with chat manager controlling flow. Includes **Maker-Checker Loops** (evaluator-optimizer within group chat). Recommendation: limit to 3 or fewer agents.

4. **Handoff Orchestration** (routing/triage): Dynamic delegation where agents assess and transfer tasks. One active agent at a time. Watch for infinite handoff loops.

5. **Magentic Orchestration** (adaptive planning): Dynamic task ledger built collaboratively. Manager agent iterates, backtracks, delegates. Best for open-ended problems with no predetermined solution path.

**Complexity Spectrum:**
| Level | Description |
|-------|-------------|
| Direct model call | Single LLM call, no agent logic |
| Single agent with tools | One agent with reasoning loop and tools |
| Multi-agent orchestration | Multiple specialized agents with coordination |

**Implementation Considerations:**
- Context and state management across agent boundaries
- Reliability patterns (timeouts, retries, circuit breakers, graceful degradation)
- Security (least privilege, content safety guardrails at multiple points)
- Cost optimization (right-size models per agent complexity)
- Observability (instrument all operations and handoffs)

**Source:** [Microsoft Azure Architecture Center -- AI Agent Orchestration Patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns) | Classification: Industry Leader

---

### RQ-2: Community-Driven Patterns for Claude Code / LLM Agent Development

Community patterns from Claude Code practitioners ([Best Practices](https://code.claude.com/docs/en/best-practices), [Agent Teams Guide](https://claudefa.st/blog/guide/agents/agent-teams-best-practices)):

**CLAUDE.md as Procedural Memory:**
- The CLAUDE.md file is the single most important tool for guiding agent behavior
- Functions as project-level system prompt loaded at session start
- Should include coding conventions, architectural decisions, project context, and behavioral rules

**Parallel Session Patterns:**
- Run multiple Claude sessions for speed, isolated experiments, or complex workflows
- **Writer/Reviewer Pattern**: One session writes tests, another writes code to pass them
- **Security Audit Chain**: Security-audit agent -> fix-implementation agent -> test-validation agent

**Agent Teams Best Practices:**
- Use delegate mode (Shift+Tab) with explicit file boundaries per teammate
- Sweet spot: 5-6 self-contained tasks per teammate with clear deliverables
- Eliminate common failures by giving explicit file ownership boundaries

**Prompt Engineering for Claude Code:**
- More precise instructions = fewer corrections needed
- Reference specific files, mention constraints, point to example patterns
- Smaller, focused prompts lead to better reasoning and cleaner implementations
- Test-driven development is especially powerful in agentic programming

**Iterative Development Strategy:**
- Write tests first based on expected input/output pairs (TDD)
- Work on single features sequentially rather than attempting everything at once
- Commit frequently with descriptive messages for session recovery

**Source:** [Claude Code Best Practices](https://code.claude.com/docs/en/best-practices), [Agent Teams Guide](https://claudefa.st/blog/guide/agents/agent-teams-best-practices), [Writing a Good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md) | Classification: Community Expert, Official Documentation

---

### RQ-3: Key Multi-Agent Orchestration Frameworks and Design Philosophies

#### LangGraph (LangChain)

**Philosophy:** Graph-based state machines for agent orchestration. LangChain publicly shifted focus: "Use LangGraph for agents, not LangChain."

**Core Concepts:**
- **StateGraph**: Directed graph where nodes are agent functions and edges define transitions
- **Conditional Edges**: Runtime routing based on state (e.g., `should_continue` functions)
- **Checkpointing**: Durable execution via SQLite or other backends for state persistence
- **Interrupts**: Human-in-the-loop via `interrupt()` mechanism for approval gates
- **Functional API**: `@entrypoint()` and `@task` decorators for simpler orchestration
- **Hybrid APIs**: Combine Graph API for complex coordination with Functional API for data processing

**Pattern Examples (from Context7):**
```python
# Orchestrator-Worker Pattern
@entrypoint()
def orchestrator_worker(topic: str):
    sections = orchestrator(topic).result()
    section_futures = [llm_call(section) for section in sections]
    final_report = synthesizer(
        [section_fut.result() for section_fut in section_futures]
    ).result()
    return final_report

# Parallel Execution Pattern
parallel_builder = StateGraph(State)
parallel_builder.add_edge(START, "call_llm_1")
parallel_builder.add_edge(START, "call_llm_2")
parallel_builder.add_edge(START, "call_llm_3")
parallel_builder.add_edge("call_llm_1", "aggregator")
```

**Strengths:** Precise control over agent flow, built-in persistence, human-in-the-loop, streaming support.

**Source:** [LangGraph Documentation](https://docs.langchain.com/oss/python/langgraph) (Context7 /websites/langchain_oss_python_langgraph), [LangChain Blog](https://blog.langchain.com/choosing-the-right-multi-agent-architecture/) | Classification: Industry Innovator

#### CrewAI

**Philosophy:** Role-based agent collaboration modeled after human team dynamics.

**Core Concepts:**
- **Agents**: Defined with `role`, `goal`, `backstory`, and `allow_delegation` flag
- **Tasks**: Include `description`, `expected_output`, and assigned `agent`
- **Crews**: Collections of agents and tasks with process type (sequential or hierarchical)
- **Delegation**: Agents with `allow_delegation=True` can delegate sub-tasks to teammates

**Pattern Examples (from Context7):**
```python
# Hierarchical Crew with Manager
crew = Crew(
    agents=[manager, researcher, writer],
    tasks=[project_task],
    process=Process.hierarchical,
    manager_llm="gpt-4o",
)

# Collaborative Single Task
collaborative_task = Task(
    description="""Create a marketing strategy.
    Writer: Focus on messaging and content strategy
    Researcher: Provide market analysis and competitor insights
    Work together to create a comprehensive strategy.""",
    agent=writer  # Lead agent, can delegate
)
```

**Strengths:** Intuitive role-based design, built-in guardrails, memory, knowledge, and observability for production systems.

**Source:** [CrewAI Documentation](https://github.com/crewaiinc/crewai) (Context7 /crewaiinc/crewai) | Classification: Industry Innovator

#### Microsoft AutoGen / Agent Framework

**Philosophy:** Conversation-based multi-agent coordination. In October 2025, Microsoft merged AutoGen with Semantic Kernel into the unified **Microsoft Agent Framework** with GA set for Q1 2026.

**Core Concepts:**
- **MagenticOneGroupChat**: Team managed by MagenticOne orchestrator architecture
- **SelectorGroupChat**: Model-based speaker selection for multi-agent teams
- **OrchestratorAgent**: Manages multi-layer worker agent coordination
- **TerminationCondition**: Configurable conditions for conversation ending
- **AssistantAgent**: Specialized agents with tools and descriptions

**Pattern Examples (from Context7):**
```python
# SelectorGroupChat with specialized agents
team = SelectorGroupChat(
    [travel_advisor, hotel_agent, flight_agent],
    model_client=model_client,
    termination_condition=TextMentionTermination("TERMINATE"),
)

# MagenticOneGroupChat
team = MagenticOneGroupChat(
    participants=[agent1, agent2],
    model_client=model_client,
    max_turns=20,
    max_stalls=3,
)
```

**Strengths:** Enterprise-grade, multi-language support (C#, Python, Java), deep Azure integration, production SLAs.

**Source:** [AutoGen Documentation](https://microsoft.github.io/autogen/stable/) (Context7 /websites/microsoft_github_io_autogen_stable), [Microsoft Agent Framework](https://learn.microsoft.com/en-us/agent-framework/) | Classification: Industry Leader

#### Other Notable Frameworks

- **OpenAI Agents SDK**: Replaced experimental Swarm framework (March 2025). Production-ready handoffs, guardrails, and tracing. Provider-agnostic.
- **Semantic Kernel**: Being migrated into Microsoft Agent Framework. Enterprise orchestration for C#/Python/Java.
- **Agency Swarm**: Community-driven framework for swarm-style agent coordination.
- **Mastra**: TypeScript-first agent framework for web developers.
- **Google ADK**: Agent Development Kit with built-in support for eight design patterns.

**Source:** [Framework Comparison -- Turing](https://www.turing.com/resources/ai-agent-frameworks), [Langfuse Comparison](https://langfuse.com/blog/2025-03-19-ai-agent-comparison) | Classification: Industry Innovator, Community Expert

---

### RQ-4: Prompt Engineering Patterns for Agent Personas/Roles

**Role Prompting (Persona Prompting):**
Assigning a specific role, persona, or expert identity before task execution. Research categorizes persona information into:
- **Demographics**: Age, gender, region
- **Attitudinal/Social**: Ideology, trust, moral values, behavioral inclinations
- **Professional/Expertise**: Domain expertise, occupation ("expert persona prompting")

**Advanced Persona Techniques:**

1. **Structured Multi-Paragraph Prompts**: Include biography, social context, beliefs, and lived experiences in explicit sections, directing the LLM to reference the persona in task reasoning.

2. **Town Hall Debate Prompting**: Multiple instantiations of the LLM as distinct "expert" personas engage in structured debate, defend, critique, and vote. Achieves +13% cell accuracy improvements for GPT-4o on logic puzzles.

3. **Persona Switch**: Compares outputs from both zero-shot and role-play prompts step-wise using the logit gap, selecting the most confident path per generation step. Yields up to +5.13% accuracy versus single-strategy baselines.

4. **Progressive Disclosure for Personas (Agent Skills)**: Three-tier hierarchy:
   - Level 1: Name and description loaded at startup
   - Level 2: Full SKILL.md content loaded when relevant
   - Level 3+: Additional linked files loaded when contextually appropriate

**CrewAI Agent Persona Pattern:**
```python
researcher = Agent(
    role="Research Specialist",
    goal="Find accurate, up-to-date information on any topic",
    backstory="""You're a meticulous researcher with expertise in finding
    reliable sources and fact-checking information across various domains.""",
    allow_delegation=True,
)
```

**Best Practices for Agent Personas:**
- Enhancing prompts with structure significantly improves outputs
- Clear constraints help the model stay within scope
- The more precise the instructions, the fewer corrections needed
- Role descriptions should include WHAT the agent does and WHEN it should be invoked
- Avoid overly prescriptive prompting that degrades results

**Source:** [LearnPrompting -- Role Prompting](https://learnprompting.org/docs/advanced/zero_shot/role_prompting), [Towards AI -- Persona Pattern](https://towardsai.net/p/artificial-intelligence/the-persona-pattern-unlocking-modular-intelligence-in-ai-agents), [The New Stack -- AI Agent Persona](https://thenewstack.io/how-to-define-an-ai-agent-persona-by-tweaking-llm-prompts/) | Classification: Community Expert, Research Paper

---

### RQ-5: Established Patterns for Agent Tool Use and Function Calling

#### Anthropic: Writing Tools for Agents

Anthropic's guide ([Writing Tools for Agents](https://www.anthropic.com/engineering/writing-tools-for-agents)) provides the most comprehensive tool design framework:

**Strategic Tool Selection:**
- Build tools for specific high-impact workflows rather than wrapping every API endpoint
- Consolidate multiple operations into single tools (e.g., `schedule_event` replaces `list_users` + `list_events` + `create_event`)
- Each tool needs clear, distinct purpose; overlapping tools confuse agents
- "If humans can't definitively select which tool to use, agents won't either"

**Namespacing:**
- Group related tools under common prefixes (`asana_search`, `asana_projects_search`)
- Test both prefix and suffix-based naming schemes

**Response Optimization:**
- Return high-signal information (semantic names over UUIDs)
- Implement response format control (concise vs. detailed enum)
- Use pagination, filtering, and truncation for token efficiency
- Create actionable error messages guiding the agent

**Agent-Computer Interface (ACI):**
- Design with same rigor applied to human-computer interfaces
- Include example usage, edge cases, input format requirements
- Clear boundary definitions between similar tools
- Poka-yoke design (make mistakes harder to make)
- SWE-bench optimization: requiring absolute filepaths prevented relative path errors

**Tool Description Crafting:**
- Describe tools as you would to a new team member
- Make implicit context explicit: specialized query formats, terminology, resource relationships
- Use unambiguous parameter names (`user_id` not `user`)
- Small refinements yield dramatic improvements

**Evaluation-Driven Development:**
- Run realistic test tasks with verifiable outcomes
- Measure beyond accuracy: runtime, token consumption, error rates
- Analyze agent behavior in raw transcripts
- Use held-out test sets to prevent overfitting

**Source:** [Anthropic Engineering -- Writing Tools for Agents](https://www.anthropic.com/engineering/writing-tools-for-agents) | Classification: Industry Leader

#### Industry Consensus on Tool Use

- **Schema Enforcement**: Use structured outputs to keep every step machine-parseable (OpenAI, Anthropic)
- **Verification-Aware Planning**: Encode pass-fail checks for each subtask so agents proceed or halt on facts
- **Security**: Treat agents like real software users, follow least-privilege access (NIST AC-6), layer defenses using OWASP Top 10 for LLM Applications
- **Model Context Protocol (MCP)**: Open standard allowing agents to access tools, data, and services uniformly with security and audit trails

**Source:** [Prompt Engineering Guide -- Function Calling](https://www.promptingguide.ai/agents/function-calling), [Composio -- Tool Calling Guide](https://composio.dev/blog/ai-agent-tool-calling-guide), [SparkCo -- Tool Calling Best Practices](https://sparkco.ai/blog/mastering-tool-calling-best-practices-for-2025) | Classification: Community Expert, Official Documentation

---

### RQ-6: Quality Assurance Patterns for Agent Output Validation

**Evaluation Frameworks:**

1. **LLM-as-Judge (S-014)**: Use language models to evaluate agent outputs against scoring rubrics. Requires counteracting leniency bias. Used by Anthropic, Google, and Microsoft in their evaluation pipelines.

2. **Creator-Critic-Revision Loops**: Multiple iteration cycles where one agent generates and another evaluates. Google ADK's Generator-Critic pattern implements this with conditional looping. Microsoft's Maker-Checker loop is a formalized version within group chat orchestration.

3. **End-to-End Behavioral Testing**: Browser automation (Puppeteer MCP) for verification as human users would test. Prevents false "completion" declarations based on unit tests alone.

4. **Continuous Monitoring**: As agents gain autonomy, evaluation shifts from occasional testing to continuous oversight. Teams need ways to detect regressions, behavioral drift, and emerging risk patterns over time.

**Key Evaluation Benchmarks:**
- **AlpacaEval**: Tests response relevance, factual consistency, coherence
- **GAIA**: Simulates complex real-world queries; measures reasoning, retrieval, task execution
- **LangBench**: Measures goal completion, context retention, error recovery
- **SWE-bench**: Verifiable coding agent performance against real GitHub issues

**Testing Patterns:**
- Use scoring rubrics or LLM-as-judge evaluations rather than exact-match assertions (Microsoft recommendation)
- Implement integration tests for multi-agent workflows
- Design testable interfaces for individual agents
- Track performance and resource metrics to establish baselines

**Agent Evaluation Platforms (2025-2026):**
- Standardized practice supported by well-defined testing suites
- Specialized monitoring platforms for both technical performance and user-facing quality
- Repeatable, data-backed validation methods

**Source:** [Tricentis -- QA Trends 2026](https://www.tricentis.com/blog/qa-trends-ai-agentic-testing), [Master of Code -- AI Evaluation Metrics](https://masterofcode.com/blog/ai-agent-evaluation), [Maxim -- Agent Eval Platforms](https://www.getmaxim.ai/articles/the-5-leading-platforms-for-ai-agent-evals-in-2025/) | Classification: Community Expert, Industry Innovator

---

### RQ-7: Context Management Strategies for Long-Running Agent Workflows

#### Anthropic: Effective Context Engineering

Anthropic's context engineering guide ([Effective Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)) provides the definitive framework:

**Core Principle:** "Find the smallest set of high-signal tokens that maximize desired outcomes."

**Context Rot:** Model accuracy in recalling information decreases as context window size increases. Context is a finite resource with diminishing marginal returns. Transformer attention requires n-squared pairwise relationships for n tokens.

**Strategies:**

1. **Compaction**: Summarize conversations approaching context limits, preserving architectural decisions and implementation details while discarding redundant tool outputs. Tune: maximize recall first, then improve precision.

2. **Structured Note-Taking**: Agents maintain persistent memory outside the context window (NOTES.md, to-do lists) pulled back later. Enables multi-hour coherence across context resets.

3. **Sub-Agent Architectures**: Specialized sub-agents handle focused tasks with clean context windows, returning condensed summaries (1,000-2,000 tokens) to a coordinating main agent. "Clear separation of concerns."

4. **Just-in-Time Retrieval**: Maintain lightweight identifiers (file paths, links, queries) and dynamically load data using tools rather than pre-processing everything.

5. **Progressive Disclosure**: Allow agents to incrementally discover context through exploration. Metadata (folder hierarchies, naming conventions, timestamps) provides behavioral signals.

6. **Tool Result Clearing**: Lightweight compaction method that removes intermediate tool outputs after they have been processed.

**System Prompt Optimization:**
- "Right Altitude Principle": Balance between specificity and flexibility
- Use distinct sections with XML tagging or Markdown headers
- Start minimal, add instructions based on failure modes

**Source:** [Anthropic Engineering -- Effective Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | Classification: Industry Leader

#### JetBrains Research: Efficient Context Management

JetBrains identified two primary strategies:
- **LLM Summarization**: Compresses long history into compact form (reduces resolution of all turn parts)
- **Observation Masking**: Targets environment observation only while preserving action and reasoning history in full

**Source:** [JetBrains Research -- Efficient Context Management](https://blog.jetbrains.com/research/2025/12/efficient-context-management/) | Classification: Industry Innovator

#### Google: Context-Aware Multi-Agent Framework

Google's approach: Architecting efficient context-aware multi-agent frameworks for production, emphasizing context isolation across sub-agents where each agent has specific tools, instructions, and its own context window.

**Source:** [Google Developers Blog -- Context-Aware Multi-Agent Framework](https://developers.googleblog.com/architecting-efficient-context-aware-multi-agent-framework-for-production/) | Classification: Industry Leader

#### LangChain: Context Engineering for Agents

LangChain identifies four key strategies: **writing** (external memory), **selecting** (relevant retrieval), **compressing** (summarization/trimming), and **isolating** (compartmentalized workflows).

**Source:** [LangChain Blog -- Context Engineering](https://blog.langchain.com/context-engineering-for-agents/) | Classification: Industry Innovator

---

### RQ-8: Agent Testing Patterns and Methodologies

**Testing Strategy Taxonomy:**

1. **Unit Testing Individual Agents**: Test each agent in isolation with controlled inputs and expected outputs. Design testable interfaces per agent (Microsoft recommendation).

2. **Integration Testing Multi-Agent Workflows**: Test full orchestration pipelines. Use scoring rubrics or LLM-as-judge evaluations rather than exact-match assertions due to nondeterministic outputs.

3. **End-to-End Behavioral Testing**: Browser automation and real-world task simulation. Anthropic uses Puppeteer MCP for verification as human users would test. Prevents premature completion declarations.

4. **Evaluation-Driven Development**: Start by identifying capability gaps through testing on representative tasks, then incrementally build skills addressing shortcomings (Anthropic Agent Skills methodology).

5. **Adversarial Testing (Red Teaming)**: Probe for failure modes, prompt injection vulnerabilities, and guardrail bypasses. Purple teaming (combined red + blue) with autonomous agents for continuous feedback loops.

6. **Regression and Drift Detection**: Continuous monitoring for behavioral drift over time. Establish baselines for performance and resource metrics.

7. **Feature List Tracking**: Comprehensive enumeration of requirements with explicit pass/fail tracking (Anthropic harness pattern). Each feature marked "failing" initially provides clear implementation targets.

**Evaluation Metrics:**
- Tool call runtime and frequency
- Total token consumption
- Error rates by parameter type
- Goal completion rate
- Context retention quality
- Error recovery capability
- Factual consistency and coherence

**Testing Anti-Patterns:**
- Relying solely on unit tests (miss integration failures)
- Exact-match assertions on nondeterministic outputs
- Testing without held-out test sets (overfitting)
- Declaring victory based on agent self-assessment without external verification

**Source:** [Microsoft -- Observability and Testing](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns), [Anthropic -- Effective Harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents), [Anthropic -- Writing Tools for Agents](https://www.anthropic.com/engineering/writing-tools-for-agents) | Classification: Industry Leader

---

### RQ-9: Governance/Safety Patterns for Agent Systems

**Guardrail Architectures:**

1. **Multi-Layer Guardrails**: Apply content safety guardrails at multiple points -- user input, tool calls, tool responses, and final output. Intermediate agents can introduce or propagate harmful content (Microsoft recommendation).

2. **Constitutional AI Constraints**: Predefined ethical principles or behavioral rules that agents must follow. Red teaming evaluates whether models consistently follow their "constitution." Violations are detected and corrected.

3. **Least Privilege Principle**: Treat agents as non-human principals with the same discipline applied to employees. Run each agent as the requesting user with permissions constrained to that user's role and geography.

4. **Human-in-the-Loop (HITL)**: Mandatory approval gates for high-stakes decisions. Scope gates to specific tool invocations rather than full agent outputs. Persist state at checkpoints for resumption.

5. **Bounded Autonomy**: Agents act independently where outcomes are predictable while keeping humans involved when risk or uncertainty increases. Progressive trust calibration over time.

6. **Red Teaming / Purple Teaming**: Adversarial testing with autonomous agents for continuous feedback loops. Purple teaming merges red (attack) and blue (defend) into combined exercises. Texas law provides affirmative defenses for parties using adversarial testing.

7. **Audit Trails and Observability**: Instrument all agent operations and handoffs. Maintain complete audit trails for post-incident review. Design audit trails to meet compliance requirements.

8. **Agent Identity and Authentication**: Implement authentication and secure networking between agents. Consider data privacy implications of agent communications.

**Regulatory Landscape (2025-2026):**
- AI guardrails moving from optional to mandatory (StateTech)
- Insurers introducing "AI Security Riders" requiring documented adversarial testing
- NIST AI Risk Management Framework as standard reference
- OWASP Top 10 for LLM Applications for layered defenses

**Source:** [MIT Technology Review -- Guardrails to Governance](https://www.technologyreview.com/2026/02/04/1131014/from-guardrails-to-governance-a-ceos-guide-for-securing-agentic-systems), [Skywork -- Agentic AI Safety](https://skywork.ai/blog/agentic-ai-safety-best-practices-2025-enterprise/), [Palo Alto Networks -- AI Red Teaming](https://www.paloaltonetworks.com/cyberpedia/what-is-ai-red-teaming) | Classification: Industry Leader, Community Expert

---

### RQ-10: Emerging Patterns and Innovations (2025-2026)

**1. Multi-Agent as Microservices:**
A "microservices revolution" where single all-purpose agents are replaced by orchestrated teams of specialized agents. Gartner reported 1,445% surge in multi-agent system inquiries from Q1 2024 to Q2 2025.

**2. Deep Agents:**
Based on models with ~200,000 token context windows, enabling tool use, local execution, file system access, and independent code writing. These agents reason through complex problems autonomously over extended sessions.

**3. Agent Skills as Modular Capabilities:**
Anthropic's Agent Skills pattern -- organized folders of instructions, scripts, and resources that agents discover and load dynamically. Progressive disclosure keeps context window usage efficient. Currently works across Claude.ai, Claude Code, Agent SDK, and Developer Platform.

**4. Model Context Protocol (MCP):**
Open standard allowing agents to access tools, data, and services uniformly with security and audit trails. Enables agents to be deployed reliably across systems and scale quickly.

**5. Agent-Native Architectures:**
Companies designing experiences where autonomous agents are the primary interface rather than supplementary features, bypassing traditional software paradigms.

**6. Contract-First Delegation (Google DeepMind):**
Formal verification contracts for agent task delegation. Tasks decomposed recursively until sub-tasks match automated verification capabilities.

**7. Context Engineering as Core Discipline:**
Shift from "prompt engineering" to "context engineering" -- managing the full lifecycle of information flowing through agent context windows. Recognized as the defining challenge for production agents.

**8. Agentic Coding Trends:**
Anthropic's 2026 Agentic Coding Trends Report documents how coding agents are reshaping software development practices, with TDD and evaluation-driven development as primary methodologies.

**9. Autonomous Purple Teaming:**
Automated red + blue team exercises using AI agents for continuous security validation at scale. Federal agencies adopting this approach for AI security.

**10. Bounded Autonomy Philosophy:**
Industry consensus moving toward agents with defined autonomy boundaries rather than fully autonomous systems. Trust calibration: agents begin with supervised actions and progressively gain autonomy based on demonstrated reliability.

**Market Projections:**
- AI agents market: $5.25B (2024) to $52.62B (2030)
- 40% of enterprise applications expected to embed agents by end of 2026 (Gartner)
- 25% of GenAI-investing businesses deploying agents in 2026, 50% by 2027 (Deloitte)

**Source:** [Machine Learning Mastery -- Agentic AI Trends 2026](https://machinelearningmastery.com/7-agentic-ai-trends-to-watch-in-2026/), [Deloitte -- Agentic AI Strategy](https://www.deloitte.com/us/en/insights/topics/technology-management/tech-trends/2026/agentic-ai-strategy.html), [Anthropic -- 2026 Agentic Coding Trends Report](https://resources.anthropic.com/hubfs/2026%20Agentic%20Coding%20Trends%20Report.pdf) | Classification: Industry Leader, Research Paper

---

## L2 Strategic Analysis

### Agent Pattern Taxonomy

Patterns organized by architectural family, with cross-references to authoritative sources:

#### Family 1: Sequential Patterns

| Pattern | Description | Sources |
|---------|-------------|---------|
| Prompt Chaining | Fixed sequential steps with quality gates | Anthropic, Google ADK, Microsoft |
| Sequential Pipeline | Linear agent pipeline via shared state | Google ADK, Microsoft, LangGraph |
| Progressive Refinement | Draft -> review -> polish workflows | Anthropic, Microsoft (Maker-Checker) |

#### Family 2: Routing Patterns

| Pattern | Description | Sources |
|---------|-------------|---------|
| Input Classification Routing | Classify input, route to specialized handler | Anthropic, Google ADK |
| Handoff/Transfer | Dynamic one-way delegation between agents | OpenAI, Microsoft, LangGraph |
| Coordinator/Dispatcher | Central agent analyzes intent, routes to specialists | Google ADK, Microsoft |

#### Family 3: Parallel Patterns

| Pattern | Description | Sources |
|---------|-------------|---------|
| Sectioning | Independent subtasks in parallel | Anthropic, LangGraph |
| Voting | Same task executed multiple times for diversity | Anthropic, Microsoft |
| Fan-Out/Gather | Concurrent execution with result aggregation | Google ADK, Microsoft, LangGraph |

#### Family 4: Hierarchical Patterns

| Pattern | Description | Sources |
|---------|-------------|---------|
| Orchestrator-Workers | Central LLM delegates to workers dynamically | Anthropic, LangGraph, Microsoft |
| Hierarchical Decomposition | Parent agents treat sub-agents as tools | Google ADK, CrewAI |
| Manager Pattern | Central manager coordinates via tool calls | OpenAI, CrewAI |

#### Family 5: Iterative Patterns

| Pattern | Description | Sources |
|---------|-------------|---------|
| Evaluator-Optimizer | Generate then evaluate in loops | Anthropic, Google ADK |
| Generator-Critic | Generate, validate, conditional loop | Google ADK, Microsoft |
| Maker-Checker Loop | Formal turn-based create/evaluate cycle | Microsoft |
| Creator-Critic-Revision | Multi-iteration quality improvement | Jerry Framework (H-14) |

#### Family 6: Collaborative Patterns

| Pattern | Description | Sources |
|---------|-------------|---------|
| Group Chat | Shared conversation thread with manager | Microsoft, AutoGen |
| Role-Based Crew | Agents with roles, goals, backstories collaborate | CrewAI |
| Multi-Agent Debate | Expert personas debate to reach consensus | Microsoft, Research Papers |

#### Family 7: Adaptive Patterns

| Pattern | Description | Sources |
|---------|-------------|---------|
| Magentic Orchestration | Dynamic task ledger built collaboratively | Microsoft, AutoGen |
| Autonomous Agent Loop | LLM uses tools based on environmental feedback | Anthropic |
| Contract-First Delegation | Recursive decomposition with verification | Google DeepMind |

#### Family 8: Context Management Patterns

| Pattern | Description | Sources |
|---------|-------------|---------|
| Compaction/Summarization | Compress history preserving key decisions | Anthropic, LangChain, JetBrains |
| Structured Note-Taking | Persistent external memory (NOTES.md) | Anthropic |
| Sub-Agent Isolation | Clean context windows per sub-agent | Anthropic, Google, LangChain |
| Progressive Disclosure | Incremental context loading via exploration | Anthropic (Agent Skills) |
| Just-in-Time Retrieval | Dynamic data loading via tools | Anthropic |
| Observation Masking | Preserve reasoning, compress observations | JetBrains |

---

### Framework Comparison Matrix

| Dimension | LangGraph | CrewAI | AutoGen/MS Agent Framework | OpenAI Agents SDK | Google ADK |
|-----------|-----------|--------|---------------------------|-------------------|------------|
| **Architecture** | Graph-based state machines | Role-based crews | Conversation-based teams | Handoff-based | Pattern-based toolkit |
| **Primary Abstraction** | Nodes + Edges | Agents + Tasks + Crews | Agents + GroupChat | Agents + Handoffs | Agents + Patterns |
| **State Management** | StateGraph with checkpointing | Built-in memory + knowledge | Session state + persistence | Managed infrastructure | session.state with output_key |
| **Multi-Agent Pattern** | Conditional edges, sub-graphs | Sequential/Hierarchical process | SelectorGroupChat, MagenticOne | Manager/Decentralized | 8 built-in patterns |
| **Human-in-the-Loop** | interrupt() mechanism | Approval callbacks | Human participant in chat | Built-in guardrails | Pause/resume pattern |
| **Persistence** | SQLite, PostgreSQL checkpointing | Built-in persistence | Checkpoint features | Managed state | State persistence |
| **Language Support** | Python, JavaScript | Python | Python, C#, Java | Python, TypeScript | Python |
| **Enterprise Readiness** | High (LangSmith observability) | Medium (growing) | High (Azure integration) | High (OpenAI infrastructure) | High (Google Cloud) |
| **Learning Curve** | Moderate-High | Low-Moderate | Moderate | Low-Moderate | Moderate |
| **Best For** | Complex stateful workflows | Team-like collaboration | Enterprise multi-agent | Simple agent orchestration | Google Cloud workloads |
| **GitHub Stars** | ~30K+ (LangChain ecosystem) | ~25K+ | ~40K+ | Growing | Growing |
| **Key Differentiator** | Graph precision + streaming | Intuitive role metaphor | Enterprise + multi-language | Provider-agnostic simplicity | Google Cloud integration |

---

### Strategic Implications for PROJ-007

1. **Pattern Language Maturity**: The agent pattern space has converged sufficiently to establish a canonical pattern taxonomy. All four major industry leaders (Anthropic, OpenAI, Google, Microsoft) agree on core patterns with only naming differences.

2. **Context Engineering as Foundation**: Context management is the single most important architectural concern. Jerry Framework's existing Context Rot mitigation (filesystem as infinite memory, selective loading) aligns perfectly with industry best practices. The L2 reinforcement injection pattern maps to Anthropic's "Right Altitude" principle.

3. **Skill Architecture Validation**: Anthropic's Agent Skills pattern validates Jerry's existing skill architecture. Progressive disclosure (L1/L2/L3 loading), SKILL.md as entry point, and modular capability packages mirror Anthropic's recommendations.

4. **Quality Gate Alignment**: The industry consensus on Creator-Critic-Revision loops (Google's Generator-Critic, Microsoft's Maker-Checker, Anthropic's Evaluator-Optimizer) validates Jerry's H-14 requirement for minimum 3-iteration cycles.

5. **Bounded Autonomy**: Industry consensus favors bounded autonomy over full independence. Jerry's H-02 (user authority) and H-31 (clarify when ambiguous) align with this philosophy.

6. **Tool Design is Underinvested**: Most frameworks focus on orchestration patterns but underinvest in tool interface design. Anthropic's ACI concept and tool writing guide represent the most advanced thinking. This is an area where PROJ-007 rules and guides can add significant value.

7. **Governance as Table Stakes**: Guardrails, constitutional constraints, and safety patterns are no longer optional. Jerry's existing governance framework (constitutional compliance, auto-escalation rules, criticality levels) is ahead of most industry implementations.

8. **Testing Gap**: Agent testing methodologies are still maturing. The industry has converged on LLM-as-judge and evaluation-driven development, but comprehensive testing frameworks remain an open problem. Jerry's S-014 LLM-as-Judge strategy is well-positioned.

---

## Best Practice Consensus

Areas where three or more authoritative sources agree:

| Consensus Area | Sources | Key Insight |
|----------------|---------|-------------|
| Start simple, add complexity when needed | Anthropic, OpenAI, Google, Microsoft | "Find the simplest solution possible"; avoid premature complexity |
| Tool design requires as much rigor as prompts | Anthropic, OpenAI, Google | ACI design, clear descriptions, poka-yoke principles |
| Context is a finite, precious resource | Anthropic, Google, LangChain, JetBrains | Context rot is real; manage aggressively via compaction and isolation |
| Multi-agent = microservices for AI | Google, Microsoft, Anthropic | Specialization, scalability, maintainability benefits |
| Human-in-the-loop is mandatory for high-stakes | All five leaders | Bounded autonomy over full independence |
| Iterative evaluation loops improve quality | Anthropic, Google, Microsoft | Generator-critic/evaluator-optimizer as core pattern |
| Structured outputs for agent communication | OpenAI, Anthropic, Microsoft | Schema enforcement keeps communication machine-parseable |
| Test with LLM-as-judge, not exact match | Anthropic, Microsoft, Google | Nondeterministic outputs require rubric-based evaluation |
| Least privilege for agent security | Microsoft, NIST, Anthropic | Treat agents as non-human principals with constrained permissions |
| Progressive trust calibration | OpenAI, Google, Community | Begin supervised, increase autonomy based on demonstrated reliability |

---

## Emerging Trends

| Trend | Maturity | Trajectory | Relevance to PROJ-007 |
|-------|----------|------------|----------------------|
| MCP (Model Context Protocol) | Adopted | Becoming standard | High -- tool integration standard |
| Agent Skills / Modular Capabilities | Adopted | Core pattern | High -- validates Jerry skill architecture |
| Context Engineering (vs. Prompt Engineering) | Growing | Replacing prompt engineering | Critical -- core of Jerry's value proposition |
| Contract-First Delegation | Research | Emerging from DeepMind | Medium -- future verification patterns |
| Autonomous Purple Teaming | Early | Government adoption | Medium -- enhances adversary skill |
| Agent-Native Architectures | Growing | Enterprise adoption | Low -- Jerry is developer tool, not end-user product |
| Deep Agents (200K+ context) | Adopted | Standard capability | High -- informs context management strategy |
| Multi-Agent as Microservices | Adopted | Industry consensus | High -- validates Jerry's agent decomposition |
| Bounded Autonomy | Adopted | Industry consensus | High -- aligns with H-02 user authority |
| Agentic Coding / TDD | Growing | Developer adoption | High -- informs agent testing guidance |

---

## Source Registry

### Industry Leaders

| Source | URL | Classification | Topics |
|--------|-----|---------------|--------|
| Anthropic -- Building Effective Agents | [Link](https://www.anthropic.com/research/building-effective-agents) | Industry Leader | Patterns, workflows, tool design |
| Anthropic -- Effective Context Engineering | [Link](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | Industry Leader | Context management |
| Anthropic -- Writing Tools for Agents | [Link](https://www.anthropic.com/engineering/writing-tools-for-agents) | Industry Leader | Tool design, ACI |
| Anthropic -- Effective Harnesses | [Link](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) | Industry Leader | Long-running agents |
| Anthropic -- Agent Skills | [Link](https://claude.com/blog/equipping-agents-for-the-real-world-with-agent-skills) | Industry Leader | Skill architecture |
| OpenAI -- Practical Guide to Building Agents | [Link](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/) | Industry Leader | Architecture, patterns |
| OpenAI -- Building Agents (Developers) | [Link](https://developers.openai.com/tracks/building-agents/) | Industry Leader | Agent SDK, patterns |
| Google -- Agent Design Patterns (Cloud) | [Link](https://docs.cloud.google.com/architecture/choose-design-pattern-agentic-ai-system) | Industry Leader | Design pattern selection |
| Google -- Multi-Agent Patterns in ADK | [Link](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/) | Industry Leader | 8 essential patterns |
| Google DeepMind -- Delegation Framework | [Link](https://creati.ai/ai-news/2026-02-17/google-deepmind-ai-agent-delegation-framework/) | Industry Leader | Contract-first delegation |
| Google DeepMind -- Scaling Agent Systems | [Link](https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/) | Industry Leader | Scaling principles |
| Microsoft -- AI Agent Orchestration Patterns | [Link](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns) | Industry Leader | 5 orchestration patterns |

### Industry Innovators

| Source | URL | Classification | Topics |
|--------|-----|---------------|--------|
| LangGraph Documentation | [Context7](https://docs.langchain.com/oss/python/langgraph) | Industry Innovator | Graph-based orchestration |
| LangChain -- Context Engineering | [Link](https://blog.langchain.com/context-engineering-for-agents/) | Industry Innovator | Context strategies |
| LangChain -- Multi-Agent Architecture | [Link](https://blog.langchain.com/choosing-the-right-multi-agent-architecture/) | Industry Innovator | Architecture selection |
| CrewAI Documentation | [Context7](https://github.com/crewaiinc/crewai) | Industry Innovator | Role-based agents |
| JetBrains Research -- Context Management | [Link](https://blog.jetbrains.com/research/2025/12/efficient-context-management/) | Industry Innovator | Observation masking |
| Langfuse -- Framework Comparison | [Link](https://langfuse.com/blog/2025-03-19-ai-agent-comparison) | Industry Innovator | Framework analysis |

### Community Expert

| Source | URL | Classification | Topics |
|--------|-----|---------------|--------|
| Claude Code Best Practices | [Link](https://code.claude.com/docs/en/best-practices) | Official Documentation | Claude Code patterns |
| Agent Teams Best Practices | [Link](https://claudefa.st/blog/guide/agents/agent-teams-best-practices) | Community Expert | Agent teams |
| Writing a Good CLAUDE.md | [Link](https://www.humanlayer.dev/blog/writing-a-good-claude-md) | Community Expert | Project context |
| Awesome Claude Code | [Link](https://github.com/hesreallyhim/awesome-claude-code) | Community Expert | Community resources |
| Turing -- Framework Comparison | [Link](https://www.turing.com/resources/ai-agent-frameworks) | Community Expert | Framework comparison |
| O'Reilly -- Multi-Agent Architectures | [Link](https://www.oreilly.com/radar/designing-effective-multi-agent-architectures/) | Community Expert | Architecture design |

### Research / Reports

| Source | URL | Classification | Topics |
|--------|-----|---------------|--------|
| Anthropic -- 2026 Agentic Coding Trends | [Link](https://resources.anthropic.com/hubfs/2026%20Agentic%20Coding%20Trends%20Report.pdf) | Research Paper | Coding agents |
| Google DeepMind -- Scaling Agent Systems | [Link](https://arxiv.org/html/2512.08296v1) | Research Paper | Scaling principles |
| Deloitte -- Agentic AI Strategy | [Link](https://www.deloitte.com/us/en/insights/topics/technology-management/tech-trends/2026/agentic-ai-strategy.html) | Research Paper | Enterprise strategy |
| MIT Technology Review -- Guardrails to Governance | [Link](https://www.technologyreview.com/2026/02/04/1131014/from-guardrails-to-governance-a-ceos-guide-for-securing-agentic-systems) | Research Paper | Governance |

---

## Self-Review Checklist

S-010 Self-Refine verification against all 10 research questions:

| RQ | Question | Covered | Evidence Quality | Notes |
|----|----------|---------|-----------------|-------|
| RQ-1 | Established patterns from Anthropic, OpenAI, Google, Microsoft | Yes | Strong -- primary sources fetched and analyzed | All four leaders documented with specific patterns |
| RQ-2 | Community patterns for Claude Code / LLM agents | Yes | Strong -- official docs + community guides | CLAUDE.md, parallel sessions, agent teams documented |
| RQ-3 | Multi-agent frameworks and philosophies | Yes | Strong -- Context7 docs + web research | LangGraph, CrewAI, AutoGen with code examples |
| RQ-4 | Prompt engineering for personas/roles | Yes | Moderate -- research papers + community guides | Role prompting, persona switch, structured personas |
| RQ-5 | Tool use and function calling | Yes | Strong -- Anthropic primary source | ACI concept, tool design guide, evaluation methodology |
| RQ-6 | Quality assurance for agent output | Yes | Moderate -- industry consensus documented | LLM-as-judge, behavioral testing, evaluation platforms |
| RQ-7 | Context management strategies | Yes | Strong -- multiple primary sources | Compaction, note-taking, sub-agent isolation, progressive disclosure |
| RQ-8 | Agent testing patterns | Yes | Moderate -- synthesized from multiple sources | Testing taxonomy, metrics, anti-patterns documented |
| RQ-9 | Governance/safety patterns | Yes | Strong -- regulatory + technical sources | Multi-layer guardrails, constitutional AI, red/purple teaming |
| RQ-10 | Emerging patterns 2025-2026 | Yes | Strong -- current sources | 10 trends with maturity and trajectory assessments |

**Citation Verification:**
- All major claims traced to specific sources
- Source classification applied (Industry Leader, Industry Innovator, Community Expert, Research Paper)
- URLs provided for all primary sources
- Context7 used for LangGraph, CrewAI, and AutoGen documentation (MCP-001 compliance)
- WebSearch used for industry context across all research questions

**Completeness Assessment:**
- L0 (ELI5) executive summary: Present (3 paragraphs)
- L1 (Engineer) detailed findings: Present (10 research questions with evidence)
- L2 (Architect) strategic analysis: Present (pattern taxonomy, framework matrix, implications)
- Agent Pattern Taxonomy: Present (8 families, 25+ patterns)
- Framework Comparison Matrix: Present (5 frameworks, 12 dimensions)
- Best Practice Consensus: Present (10 consensus areas)
- Emerging Trends: Present (10 trends with maturity assessment)

**Identified Gaps:**
- Agency Swarm and Mastra frameworks have limited primary documentation -- assessed at surface level only
- Semantic Kernel standalone patterns not deeply researched (superseded by Microsoft Agent Framework)
- Academic papers on agent patterns (arXiv) referenced but not deeply analyzed -- additional pass may be warranted
- Anthropic's 2026 Agentic Coding Trends Report referenced but PDF not fully parsed

**Quality Assessment:** This research provides comprehensive, well-cited coverage across all 10 research questions with strong evidence from authoritative sources. The pattern taxonomy and framework comparison matrix provide actionable reference material for PROJ-007 rule and guide development.
