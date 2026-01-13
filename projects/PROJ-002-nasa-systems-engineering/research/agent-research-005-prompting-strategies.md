# Agent Research 005: Prompting Strategies for Multi-Agent AI Systems

**Document ID:** AGENT-RESEARCH-005
**Date:** 2026-01-09
**Author:** ps-researcher (Claude Opus 4.5)
**Status:** Complete
**Classification:** Research Document

---

## Executive Summary

This research document synthesizes the latest best practices and techniques for prompting strategies in multi-agent AI systems. The field has evolved significantly from simple "prompt engineering" to a more comprehensive discipline now called **"context engineering"** - the systematic management of all information that influences model behavior at runtime.

Key findings indicate that effective multi-agent systems require:
1. **Structured context management** using the write/select/compress/isolate taxonomy
2. **Clear persona activation** through role, goal, and backstory specifications
3. **Explicit state handoff protocols** with carefully managed message passing
4. **Cognitive mode selection** through task classification and appropriate technique matching
5. **Hierarchical prompt structures** using XML or Markdown sections

The research draws from Anthropic's official guidance, LangChain/CrewAI frameworks, academic research on Chain-of-Thought prompting, and industry best practices from 2025-2026.

---

## 1. Context Engineering: The Evolution of Prompt Engineering

### 1.1 Definition and Scope

Context engineering represents a paradigm shift from crafting individual prompts to designing complete information systems for AI agents:

> "Building with language models is becoming less about finding the right words and phrases for your prompts, and more about answering the broader question of 'what configuration of context is most likely to generate our model's desired behavior?'"
> - [Anthropic Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

Context engineering encompasses:
- **System prompts** - Core instructions and behavioral guidelines
- **Tool definitions** - Available capabilities and their usage patterns
- **Message history** - Conversation state and prior interactions
- **Retrieved documents** - External knowledge via RAG
- **Memory systems** - Persistent state across sessions
- **Model Context Protocol (MCP)** - Standardized context interfaces

### 1.2 The Four Strategic Categories

According to [LangChain's context engineering documentation](https://docs.langchain.com/oss/python/langchain/context-engineering), effective context management follows four strategic categories:

| Strategy | Purpose | Techniques |
|----------|---------|------------|
| **Write** | Persist information for later use | Memory stores, note-taking, checkpoint files |
| **Select** | Filter to most relevant information | Semantic search, relevance scoring, recency weighting |
| **Compress** | Reduce tokens while preserving meaning | Summarization, fact extraction, conversation compaction |
| **Isolate** | Separate concerns between agents | Sub-agent architectures, clean context windows |

### 1.3 The P.A.R.T. Framework

The [Prompt Engineering Guide](https://www.promptingguide.ai/guides/context-engineering-guide) documents the P.A.R.T. framework for organizing agent context:

- **P**rompt - Core instructions and task definitions
- **A**rchive - Historical context and prior interactions
- **R**esources - Domain knowledge and reference materials
- **T**ools - External capabilities and API integrations

### 1.4 Context Window Optimization

Key insights for managing context windows:

1. **The "Needle in a Haystack" Problem** - Information buried deep in large contexts is often ignored or retrieved unreliably

2. **KV-Cache Hit Rate** - The single most important metric for production-stage AI agents, directly affecting latency and cost

3. **Compaction Strategies**:
   - Summarize conversations approaching context limits
   - Preserve architectural decisions and critical details
   - Discard redundant tool outputs

4. **Structured Note-Taking** - Agents maintain persistent memory files (e.g., NOTES.md, TODO lists) outside the context window

---

## 2. Prompting Strategy Catalog

### 2.1 Chain-of-Thought (CoT) Prompting

**Source:** [Prompting Guide - CoT](https://www.promptingguide.ai/techniques/cot)

Chain-of-Thought prompting enables complex reasoning through intermediate steps. First introduced by DeepMind in 2022, it gained renewed attention with OpenAI's o1 model.

#### Variants

| Variant | Description | Example Trigger |
|---------|-------------|-----------------|
| **Zero-Shot CoT** | Add reasoning trigger without examples | "Let's think step by step" |
| **Few-Shot CoT** | Provide reasoning examples before task | Include worked examples with steps |
| **Auto-CoT** | Automated generation of reasoning chains | Clustering + sampling algorithms |
| **Multimodal CoT** | Extend to text + images | Image analysis with step reasoning |

#### 2025-2026 Developments

- **Layered CoT** - Multiple reasoning passes with review opportunities (healthcare, finance)
- **Trace-of-Thought** - Optimized for smaller models (~7B parameters)
- **LongRePS** - Designed for long-context tasks with supervised reasoning paths

#### When to Use CoT

| Model Type | CoT Benefit | Recommendation |
|------------|-------------|----------------|
| Non-reasoning models | Modest improvement, increased variability | Use for complex reasoning tasks |
| Reasoning models (o1, o3) | Marginal benefit, significant time cost | Often unnecessary - models reason natively |
| Claude 4.x | Strong native reasoning | Use for complex multi-step problems |

### 2.2 Tree of Thoughts (ToT) Prompting

**Source:** [Prompting Guide - ToT](https://www.promptingguide.ai/techniques/tot)

ToT generalizes CoT by maintaining a tree of thoughts with search algorithms (BFS, DFS) for systematic exploration:

```
Problem
   |
   +-- Thought A
   |      |
   |      +-- Thought A1 [Evaluated: Good]
   |      +-- Thought A2 [Evaluated: Bad] (backtrack)
   |
   +-- Thought B
          |
          +-- Thought B1 [Evaluated: Good]
```

**Key Differences from CoT:**
- Enables backtracking and alternative exploration
- Uses self-evaluation at each step
- Suitable for reinforcement learning scenarios
- Better for tasks requiring multiple solution paths

### 2.3 Structured Prompting (XML/JSON)

**Source:** [Claude Docs - XML Tags](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/use-xml-tags)

#### XML Prompting for Claude

XML tags provide clear structure and separation:

```xml
<background_information>
Context about the domain and task requirements.
</background_information>

<instructions>
1. First, analyze the input data
2. Then, identify key patterns
3. Finally, generate recommendations
</instructions>

<examples>
<example>
<input>Sample input here</input>
<output>Expected output format</output>
</example>
</examples>

<formatting>
Return results as a numbered list.
</formatting>
```

**Benefits:**
- Clarity: Separates instructions from examples from context
- Accuracy: Reduces misinterpretation
- Flexibility: Easy to modify sections independently
- Parseability: Enables structured output extraction

#### JSON Prompting for Multi-Agent Systems

**Source:** [AI Competence - JSON Prompting](https://aicompetence.org/json-prompting-supercharges-multi-agent-ai-systems/)

JSON is particularly effective for inter-agent communication:

```json
{
  "task": "analyze_data",
  "context": {
    "domain": "financial_analysis",
    "priority": "high"
  },
  "constraints": {
    "max_tokens": 2000,
    "format": "structured_report"
  },
  "input_data": {
    "source": "quarterly_report_q3_2025",
    "metrics": ["revenue", "churn", "expansion"]
  }
}
```

**Advantages for Multi-Agent:**
- Shared schema ensures predictable outputs
- Machine-readable for downstream agents
- Reduces cascading failures
- Enables workflow branching and validation

### 2.4 Multishot (Few-Shot) Prompting

Examples are "pictures worth a thousand words" for guiding model behavior.

**When to Use:**
- Tasks requiring specific output formats
- Domain-specific terminology or style
- Complex reasoning patterns
- Edge case handling

**Best Practices:**
1. Provide 2-5 representative examples
2. Use consistent formatting across examples
3. Include diverse cases covering edge scenarios
4. Clearly separate examples from the actual task

```xml
<examples>
<example>
<user_input>Calculate the ROI for a $10,000 investment returning $12,500</user_input>
<agent_response>
ROI = (Final Value - Initial Investment) / Initial Investment * 100
ROI = ($12,500 - $10,000) / $10,000 * 100
ROI = $2,500 / $10,000 * 100
ROI = 25%

The investment yielded a 25% return.
</agent_response>
</example>
</examples>
```

---

## 3. Persona Activation Patterns

### 3.1 Role-Playing Language Agents (RPLAs)

**Source:** [ArXiv - Survey on Role-Playing Language Agents](https://arxiv.org/html/2404.18231v1)

Role-Playing Language Agents leverage multiple LLM abilities:
- In-context learning
- Instruction following
- Social intelligence

**Key Requirements for Effective Role-Playing:**
1. **Active Engagement** - Produce responses in dialogue format with deep immersion
2. **Avoid Out-of-Character** - Never say "As an AI model..."
3. **Consistent Personality** - Stable across turns, sessions, and languages
4. **Role Fidelity** - Balance character authenticity with task effectiveness

### 3.2 The Role-Goal-Backstory Pattern

**Source:** [CrewAI Documentation](https://github.com/crewaiinc/crewai/blob/main/docs/en/guides/agents/crafting-effective-agents.mdx)

The most effective persona activation uses three components:

```yaml
agent:
  role: "SaaS Metrics Specialist focusing on growth-stage startups"
  goal: "Identify actionable insights from business data that can directly
         impact customer retention and revenue growth"
  backstory: "With 10+ years analyzing SaaS business models, you've developed
              a keen eye for the metrics that truly matter for sustainable
              growth. You've helped numerous companies identify the leverage
              points that turned around their business trajectory. You believe
              in connecting data to specific, actionable recommendations rather
              than general observations."
```

### 3.3 Persona Prompt Formats

**Source:** [Emergent Mind - Persona Prompting](https://www.emergentmind.com/topics/persona-prompting)

Two key dimensions for persona formulation:

| Dimension | Options | Best Practice |
|-----------|---------|---------------|
| **Role Adoption Format** | "You are...", third-person cues, interview Q&A | Interview format yields more stable, less stereotyped outputs |
| **Demographic/Identity Priming** | Explicit attributes, implicit context | System 2 persona prompts reduce stereotypical responses by up to 13% |

### 3.4 Expert Prompting vs. Basic Persona

**Source:** [PromptHub - Role Prompting](https://www.prompthub.us/blog/role-prompting-does-adding-personas-to-your-prompts-really-make-a-difference)

Research shows that basic persona prompting ("You are a helpful assistant") barely outperforms vanilla prompting. However, **expert prompting** with specific domain knowledge significantly improves performance.

**Ineffective:**
```
You are a helpful data analyst.
```

**Effective:**
```
You are a senior data analyst with 15 years of experience in SaaS metrics.
You specialize in cohort analysis, churn prediction, and revenue attribution.
You always validate assumptions with data before making recommendations and
explicitly state confidence levels in your conclusions.
```

---

## 4. State Handoff Prompting for Multi-Agent Systems

### 4.1 The Handoff Architecture

**Source:** [LangChain - Multi-Agent Handoffs](https://docs.langchain.com/oss/python/langchain/multi-agent/handoffs)

Handoffs enable dynamic behavior changes based on state:

```python
@tool
def transfer_to_sales(runtime: ToolRuntime) -> Command:
    # Get the AI message that triggered this handoff
    last_ai_message = runtime.state["messages"][-1]

    # Create an artificial tool response to complete the pair
    transfer_message = ToolMessage(
        content="Transferred to sales agent",
        tool_call_id=runtime.tool_call_id,
    )

    return Command(
        goto="sales_agent",
        update={
            "active_agent": "sales_agent",
            # Pass only these two messages, not the full subagent history
            "messages": [last_ai_message, transfer_message],
        },
        graph=Command.PARENT,
    )
```

### 4.2 Context Engineering for Handoffs

**Critical Insight:** "Reliability lives and dies in the handoffs. Most 'agent failures' are actually orchestration and context-transfer issues."

**Key Principles:**

1. **Explicit Message Selection** - You must explicitly decide what messages pass between agents
2. **Avoid Context Bloat** - Don't pass full conversation history; select relevant context only
3. **Complete Message Pairs** - Always include AI message + corresponding tool response
4. **State Variable Tracking** - Use persistent state variables (e.g., `active_agent`) to track flow

### 4.3 Memory Architecture for Multi-Agent Systems

**Source:** [Vellum - Multi-Agent Systems](https://www.vellum.ai/blog/multi-agent-systems-building-with-context-engineering)

| Memory Type | Purpose | Scope |
|-------------|---------|-------|
| **Short-term (Rolling)** | Current plan/state | Last N turns |
| **Long-term (Persistent)** | Reusable knowledge | Cross-session |
| **Shared Project** | Team coordination | All agents (with ACLs) |
| **Private Agent** | Agent-specific state | Single agent |

### 4.4 Orchestration Patterns

**Source:** [Azure Architecture - AI Agent Patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns)

| Pattern | Description | Use Case |
|---------|-------------|----------|
| **Sequential** | Agents run in fixed order | Linear workflows |
| **Concurrent** | Agents run in parallel | Independent subtasks |
| **Supervisor-Worker** | Manager coordinates workers | Complex branching tasks |
| **Group Chat** | Agents discuss collaboratively | Consensus-building |
| **Handoff** | Dynamic routing based on state | Customer service, triage |

---

## 5. Cognitive Mode Prompting

### 5.1 System 1 vs. System 2 Thinking

**Source:** [Latitude Blog - LLM Reasoning](https://latitude-blog.ghost.io/blog/complete-guide-to-prompt-engineering-for-llm-reasoning/)

| Mode | Characteristics | Prompting Approach |
|------|-----------------|-------------------|
| **System 1** | Fast, intuitive, pattern-matching | Default LLM behavior |
| **System 2** | Slow, deliberate, analytical | Chain-of-Thought, explicit reasoning |

### 5.2 Task Classification for Mode Selection

**Source:** [Vendasta - AI Prompting Guide](https://www.vendasta.com/blog/ai-prompting/)

Classify tasks along dimensions to select appropriate prompting mode:

| Dimension | Options | Recommended Technique |
|-----------|---------|----------------------|
| **Complexity** | Simple vs. multi-step | Direct instructions vs. CoT |
| **Output Type** | Creative vs. analytical vs. structured | Role-setting vs. CoT vs. format specs |
| **Error Tolerance** | High-stakes vs. experimental | Layered CoT with review vs. flexible prompts |
| **Frequency** | One-time vs. repeated | Ad-hoc vs. optimized templates |

### 5.3 Analytical Mode Prompting

For reasoning, logic, and problem-solving:

```xml
<mode>analytical</mode>

<instructions>
You are solving a complex problem that requires careful reasoning.

1. First, clearly state your understanding of the problem
2. Identify all relevant constraints and variables
3. Consider multiple approaches before selecting one
4. Show your work step-by-step
5. Verify your answer by checking against the original constraints
6. State your confidence level and any assumptions made
</instructions>

<thinking_protocol>
Before providing your final answer:
- List what you know for certain
- List what you're uncertain about
- Consider alternative interpretations
- Check for logical errors
</thinking_protocol>
```

### 5.4 Creative Mode Prompting

For ideation, writing, and generative tasks:

```xml
<mode>creative</mode>

<instructions>
You are generating creative content with flexible boundaries.

1. Explore multiple directions before committing
2. Prioritize originality and unexpectedness
3. Balance novelty with coherence
4. Feel free to take creative risks
5. Use vivid, specific language
</instructions>

<creative_parameters>
- Tone: [playful/serious/contemplative]
- Style: [minimalist/elaborate/experimental]
- Constraints: [optional specific requirements]
</creative_parameters>
```

---

## 6. System Prompt Structure and Best Practices

### 6.1 Recommended Sections

**Source:** [GitHub - Awesome AI System Prompts](https://github.com/dontriskit/awesome-ai-system-prompts)

Modern system prompts typically include these sections:

```markdown
# Role and Identity
[Who the agent is and their expertise]

# Goals and Objectives
[What the agent should accomplish]

# Capabilities and Tools
[Available tools and how to use them]

# Instructions
[Step-by-step behavioral guidance]

# Guardrails and Constraints
[Non-negotiable rules and boundaries]

# Output Format
[Expected response structure]

# Examples
[Concrete demonstrations of desired behavior]
```

### 6.2 The "Right Altitude" Principle

**Source:** [Anthropic Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

System prompts should operate at the "Goldilocks zone":

| Extreme | Problem | Example |
|---------|---------|---------|
| **Too Specific** | Brittle, high maintenance | "If the user says X, respond with exactly Y" |
| **Too Vague** | No actionable guidance | "Be helpful and answer questions" |
| **Right Altitude** | Flexible heuristics | "When facing ambiguous requests, ask clarifying questions. Prioritize accuracy over speed." |

### 6.3 Emphasis and Reinforcement

**Source:** [Datablist - Prompt Writing Rules](https://www.datablist.com/how-to/rules-writing-prompts-ai-agents)

For critical instructions:
1. Add "This step is important" after key instructions
2. Repeat most important 1-2 instructions
3. Place critical rules in dedicated `# Guardrails` section
4. Use formatting (bold, caps) sparingly for emphasis

### 6.4 Tool Design Principles

**Source:** [Anthropic Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

1. **Self-contained** - Each tool should be independently usable
2. **Robust to error** - Handle edge cases gracefully
3. **Clear intent** - Obvious when to use each tool
4. **Minimal overlap** - Avoid ambiguity between tools
5. **Token-efficient returns** - Return concise, relevant information

---

## 7. Example Prompts with Explanations

### 7.1 Multi-Agent Orchestrator System Prompt

```xml
<identity>
You are the Orchestrator Agent, responsible for coordinating a team of
specialized agents to complete complex tasks.
</identity>

<capabilities>
You have access to the following specialist agents:
- ResearchAgent: Deep research and information gathering
- AnalysisAgent: Data analysis and pattern recognition
- WriterAgent: Content creation and documentation
- ReviewerAgent: Quality assurance and verification
</capabilities>

<orchestration_protocol>
1. Receive task from user
2. Decompose into subtasks appropriate for each specialist
3. Assign subtasks with clear context and success criteria
4. Collect and synthesize results
5. Verify completeness before presenting to user
</orchestration_protocol>

<handoff_format>
When delegating to a specialist, use this structure:
<delegation>
<target_agent>[Agent Name]</target_agent>
<task>[Clear task description]</task>
<context>[Relevant background information]</context>
<success_criteria>[How to know the task is complete]</success_criteria>
<return_format>[Expected output structure]</return_format>
</delegation>
</handoff_format>

<guardrails>
- Never execute tasks directly; always delegate to appropriate specialist
- Ensure each specialist receives only the context they need
- Verify outputs before synthesizing final response
- Acknowledge uncertainty when specialists provide conflicting information
</guardrails>
```

**Explanation:** This prompt establishes clear identity, enumerates capabilities, provides a protocol for orchestration, standardizes the handoff format, and sets non-negotiable guardrails.

### 7.2 Domain Expert Persona Activation

```yaml
agent:
  role: "NASA Systems Engineering Process Expert"

  goal: >
    Guide teams through NASA NPR 7123.1-compliant systems engineering
    processes, ensuring proper documentation and review gate readiness.

  backstory: >
    You have 20+ years of experience as a NASA systems engineer, having
    worked on missions from early concept development through operations.
    You've served as Chief Systems Engineer on two flagship missions and
    have trained over 100 engineers in SE best practices. You're known for
    your ability to translate complex process requirements into actionable
    guidance while maintaining rigor and traceability.

  expertise_areas:
    - Technical Review Gates (SRR, PDR, CDR, etc.)
    - Requirements Management and Verification
    - Risk Management and Mitigation
    - Interface Control Documents
    - V&V Planning and Execution

  communication_style:
    - Direct and precise
    - Uses NASA terminology correctly
    - Provides references to NPR/NPD documents
    - Balances theory with practical experience
    - Asks clarifying questions before providing guidance
```

**Explanation:** This YAML-based persona combines role/goal/backstory with explicit expertise areas and communication style, creating a highly specific and consistent agent personality.

### 7.3 Analytical Reasoning Task

```xml
<task_type>analytical_reasoning</task_type>

<problem>
Analyze the following system architecture for potential single points of
failure and propose redundancy strategies.
</problem>

<reasoning_protocol>
Apply structured analysis using this framework:

<step_1>Component Identification</step_1>
List all components and their dependencies.

<step_2>Failure Mode Analysis</step_2>
For each component, identify:
- What happens if it fails?
- What depends on it?
- Is there a workaround?

<step_3>Risk Prioritization</step_3>
Rank failures by: Likelihood x Impact x Detectability

<step_4>Mitigation Strategies</step_4>
For high-priority risks, propose:
- Redundancy options
- Graceful degradation paths
- Monitoring and alerting

<step_5>Trade-off Analysis</step_5>
Evaluate each mitigation for:
- Implementation cost
- Operational complexity
- Effectiveness
</reasoning_protocol>

<output_format>
Present findings in a structured table with columns:
Component | Failure Mode | Risk Score | Mitigation | Trade-offs
</output_format>
```

**Explanation:** This prompt activates analytical mode by providing a step-by-step reasoning protocol, ensuring thorough analysis before conclusions.

### 7.4 Creative Ideation Task

```xml
<task_type>creative_ideation</task_type>

<challenge>
Generate innovative approaches to reducing context window consumption
in long-running agent systems.
</challenge>

<creative_parameters>
<exploration_mode>divergent</exploration_mode>
<constraint_level>low</constraint_level>
<inspiration_domains>
- Cognitive science and human memory
- Database indexing and caching
- Compression algorithms
- Collaborative filtering
</inspiration_domains>
</creative_parameters>

<ideation_protocol>
1. Generate 10+ initial ideas without self-censoring
2. Cluster ideas by underlying principle
3. Select 3 most promising for deeper exploration
4. For each, articulate:
   - Core mechanism
   - Novel insight
   - Potential challenges
   - Implementation sketch
</ideation_protocol>

<output_format>
Present as creative brief with:
- Idea name (memorable, descriptive)
- One-line pitch
- How it works
- Why it might succeed
- Open questions
</output_format>
```

**Explanation:** This prompt activates creative mode with exploration parameters, draws inspiration from diverse domains, and provides structure without constraining ideation.

---

## 8. Sources and References

### Primary Sources

- [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) - Anthropic Engineering
- [Prompting Best Practices - Claude Docs](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices) - Anthropic
- [Prompt Engineering Guide](https://www.promptingguide.ai/) - DAIR.AI
- [Context Engineering Guide](https://www.promptingguide.ai/guides/context-engineering-guide) - DAIR.AI

### Framework Documentation

- [LangChain Multi-Agent Handoffs](https://docs.langchain.com/oss/python/langchain/multi-agent/handoffs) - LangChain
- [LangChain Context Engineering](https://docs.langchain.com/oss/python/langchain/context-engineering) - LangChain
- [CrewAI Crafting Effective Agents](https://github.com/crewaiinc/crewai/blob/main/docs/en/guides/agents/crafting-effective-agents.mdx) - CrewAI
- [CrewAI Customizing Prompts](https://github.com/crewaiinc/crewai/blob/main/docs/en/guides/advanced/customizing-prompts.mdx) - CrewAI

### Research Papers and Articles

- [Chain-of-Thought Prompting](https://www.promptingguide.ai/techniques/cot) - Prompting Guide
- [Tree of Thoughts](https://www.promptingguide.ai/techniques/tot) - Prompting Guide
- [Survey on Role-Playing Language Agents](https://arxiv.org/html/2404.18231v1) - ArXiv
- [The Decreasing Value of Chain of Thought](https://gail.wharton.upenn.edu/research-and-insights/tech-report-chain-of-thought/) - Wharton AI Labs

### Industry Best Practices

- [Multi-Agent AI Systems: Orchestrating AI Workflows](https://www.v7labs.com/blog/multi-agent-ai) - V7 Labs
- [AI Agent Orchestration Best Practices](https://skywork.ai/blog/ai-agent-orchestration-best-practices-handoffs/) - Skywork AI
- [Azure AI Agent Design Patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns) - Microsoft Azure
- [Multi-Agent Systems Building with Context Engineering](https://www.vellum.ai/blog/multi-agent-systems-building-with-context-engineering) - Vellum
- [Awesome AI System Prompts](https://github.com/dontriskit/awesome-ai-system-prompts) - GitHub

### Memory and State Management

- [OpenAI Agents SDK - Session Memory](https://cookbook.openai.com/examples/agents_sdk/session_memory) - OpenAI Cookbook
- [Context Personalization with Long-Term Memory](https://cookbook.openai.com/examples/agents_sdk/context_personalization) - OpenAI Cookbook
- [Memory and State in LLM Applications](https://arize.com/blog/memory-and-state-in-llm-applications/) - Arize AI

### Prompt Format Resources

- [Use XML Tags to Structure Prompts](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/use-xml-tags) - Claude Docs
- [Structured Prompting Techniques: XML & JSON](https://codeconductor.ai/blog/structured-prompting-techniques-xml-json/) - CodeConductor
- [JSON Prompting for Multi-Agent AI Systems](https://aicompetence.org/json-prompting-supercharges-multi-agent-ai-systems/) - AI Competence

---

## 9. Key Takeaways

### For System Prompt Design

1. **Structure matters** - Use XML tags or Markdown headers to organize sections
2. **Find the right altitude** - Specific enough to guide, flexible enough to adapt
3. **Centralize guardrails** - Dedicate a section for non-negotiable rules
4. **Include examples** - Concrete demonstrations improve instruction following

### For Multi-Agent Orchestration

1. **Design handoffs carefully** - Most agent failures are context-transfer issues
2. **Select, don't include everything** - Pass only relevant context between agents
3. **Isolate agent concerns** - Each agent should have a clean, focused context window
4. **Use typed state** - Track agent state with explicit variables

### For Persona Activation

1. **Use Role-Goal-Backstory** - The most effective activation pattern
2. **Be specific, not generic** - Expert prompting significantly outperforms basic persona
3. **Interview format works best** - Gradually elicit identity attributes
4. **Maintain consistency** - Same personality across turns and sessions

### For Reasoning Tasks

1. **Match mode to task** - Analytical vs. creative require different approaches
2. **Use CoT selectively** - Not always beneficial, especially for reasoning-native models
3. **Provide reasoning protocols** - Step-by-step frameworks improve analytical outputs
4. **Allow exploration** - Creative tasks need divergent, low-constraint prompts

---

*Document generated by ps-researcher agent conducting deep research on prompting strategies for multi-agent AI systems.*
