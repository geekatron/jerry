# WI-SAO-046: Context7 + Anthropic Research

**Document ID**: WI-SAO-046-RESEARCH-001
**Date**: 2026-01-12
**Author**: Claude Agent (WI-SAO-046)
**Status**: Complete

---

## Executive Summary

This research synthesizes the latest best practices from Anthropic and Context7 sources for AI agent design, prompt engineering, and context engineering. Three key findings emerge: (1) Context engineering has superseded prompt engineering as the primary discipline for building effective agents, with the "Write/Select/Compress/Isolate" taxonomy providing a comprehensive framework; (2) The orchestrator-worker pattern with detailed task delegation is the predominant architecture for multi-agent systems; (3) Treating context as a finite resource with diminishing marginal returns is fundamental to reliable agent behavior.

---

## 1. Agent Design Patterns

### 1.1 Role-Goal-Backstory Pattern

The Role-Goal-Backstory pattern establishes agent identity through three components:

**Standard Template Structure** (from Claude Code Agent Development Skill):

```markdown
You are [role] specializing in [domain].

**Your Core Responsibilities:**
1. [Primary responsibility]
2. [Secondary responsibility]
3. [Additional responsibilities...]

**Analysis Process:**
1. [Step one]
2. [Step two]
3. [Step three]

**Quality Standards:**
- [Standard 1]
- [Standard 2]

**Output Format:**
Provide results in this format:
- [What to include]
- [How to structure]

**Edge Cases:**
Handle these situations:
- [Edge case 1]: [How to handle]
- [Edge case 2]: [How to handle]
```

**Key Principles:**
- Write in second person ("You are...", "You will...")
- Be specific rather than generic - avoid vague instructions
- Include concrete examples when they would clarify behavior
- Balance comprehensiveness with clarity - every instruction should add value
- Build in quality assurance and self-correction mechanisms

### 1.2 Capability Description Best Practices

**System Prompt Contract Format** (recommended structure):

| Component | Purpose | Example |
|-----------|---------|---------|
| **Role** | One-line identity | "You are an expert code quality reviewer" |
| **Goal** | What success looks like | "Identify bugs, security issues, and style violations" |
| **Constraints** | Behavioral boundaries | "Never modify code directly; only suggest changes" |
| **If Unsure** | Uncertainty handling | "Ask clarifying questions rather than guessing" |
| **Output Format** | Structure specification | "Return findings as JSON with severity, location, description" |

**From Anthropic's Guidance:**
> "A good Claude system prompt reads like a short contract - explicit, bounded, and verifiable."

**Specificity Guidelines:**
- Use "simple, direct language that presents ideas at the right altitude for the agent"
- Organize into distinct sections using XML tags or Markdown headers
- Start with a minimal prompt, then iteratively add instructions based on failure modes
- Minimal doesn't mean short - provide sufficient upfront information

### 1.3 Persona Activation

**Six-Step Agent Creation Process** (from Anthropic's agent-creation-system-prompt):

1. **Extract Core Intent**: Identify fundamental purpose, key responsibilities, and success criteria
2. **Design Expert Persona**: Create compelling identity embodying deep domain knowledge
3. **Architect Comprehensive Instructions**: Develop system prompt with behavioral boundaries
4. **Optimize for Performance**: Include decision-making frameworks and quality control mechanisms
5. **Create Identifier**: Design concise, descriptive identifier (lowercase, hyphens, 3-50 chars)
6. **Define Triggering Conditions**: Specify when the agent should be activated with examples

**Identifier Naming Rules:**
- Use lowercase letters, numbers, and hyphens only
- Typically 2-4 words joined by hyphens
- Clearly indicate primary function
- Avoid generic terms like "helper" or "assistant"

---

## 2. Prompt Engineering

### 2.1 Write/Select/Compress/Isolate Taxonomy

Anthropic's context engineering taxonomy combines four complementary techniques:

| Technique | Description | Implementation |
|-----------|-------------|----------------|
| **Write** | Persist critical information externally | Structured notes, memory tools, progress files |
| **Select** | Choose optimal tokens for context | Just-in-time retrieval, tool search, filtering |
| **Compress** | Summarize to preserve key information | Compaction, summarization, clearing tool outputs |
| **Isolate** | Separate concerns across agents | Sub-agents with clean contexts, orchestrator pattern |

**Write - Structured Note-Taking (Agentic Memory):**
- Agents regularly write external notes that persist outside the context window
- Enables multi-hour tasks without losing critical context
- Tracks progress across dozens of tool calls
- Maintains strategic knowledge without consuming working memory

**Select - Just-in-Time Retrieval:**
- Maintain lightweight identifiers (file paths, queries, URLs)
- Dynamically load information at runtime using tools
- Mirrors human cognition - use indexing systems rather than memorizing
- Enables progressive disclosure through exploration

**Compress - Compaction Strategy:**
- Preserve architectural decisions, unresolved issues, implementation details
- Discard redundant tool outputs
- Start by maximizing recall, then iterate to improve precision
- Safe lightweight approach: clear tool result outputs after processing

**Isolate - Sub-Agent Architecture:**
- Delegate focused tasks to specialized sub-agents with clean context windows
- Main agent coordinates strategy
- Sub-agents explore extensively (tens of thousands of tokens)
- Return only condensed summaries (1,000-2,000 tokens)

**Results:** Anthropic reported up to 54% improvement in agent tasks through these approaches.

### 2.2 Chain-of-Thought Patterns

**Thinking Process Implementation:**

```xml
<thinking>
  [Model's internal reasoning process here]
</thinking>
<final_answer>
  [Model's final response here]
</final_answer>
```

**Extended Thinking Activation:**
- Use keywords: "think", "think hard", "ultrathink"
- Especially helpful for tasks involving reflection after tool use
- Critical for complex multi-step reasoning
- Guide initial or interleaved thinking for better results

**Explore, Plan, Code, Commit Pattern:**
1. Ask Claude to read relevant files without writing code initially
2. Request a plan using extended thinking
3. Have Claude implement the solution
4. Request commit and PR creation

This prevents premature coding and improves solutions for complex problems.

### 2.3 System Prompt Structure

**Recommended Organization:**

```markdown
# System Prompt Structure

## Background Information
<background_information>
[Context about the domain, project, or task]
</background_information>

## Instructions
<instructions>
[Core behavioral directives]
</instructions>

## Tool Guidance
<tool_guidance>
[When and how to use available tools]
</tool_guidance>

## Output Format
<output_format>
[Specification for response structure]
</output_format>

## Edge Cases
<edge_cases>
[Special situation handling]
</edge_cases>
```

**Core Principles for Claude 4.x:**
1. **Be Explicit**: Claude 4.x responds to precise instructions
2. **Add Context**: Explain WHY, not just WHAT
3. **Use Examples**: Show, don't just tell
4. **Encourage Reasoning**: Chain of thought dramatically improves quality
5. **Define Output Format**: Be specific about structure and style

**Few-Shot Example Guidelines:**
- Start with one example (one-shot)
- Only add more if output still doesn't match needs
- Curate diverse, canonical examples that portray expected behavior
- Avoid listing exhaustive edge cases - examples function as visual demonstrations

---

## 3. Tool Use Patterns

### 3.1 Function Schema Design

**Tool Definition Best Practices:**

```json
{
  "name": "get_stock_price",
  "description": "Get the current stock price for a given ticker symbol.",
  "input_schema": {
    "type": "object",
    "properties": {
      "ticker": {
        "type": "string",
        "description": "The stock ticker symbol, e.g. AAPL for Apple Inc."
      }
    },
    "required": ["ticker"]
  }
}
```

**Critical Guidelines:**
- Tools should be "self-contained, robust to error, and extremely clear"
- Maintain minimal overlap in functionality
- Make input parameters "descriptive, unambiguous"
- Curate a minimal viable toolset
- Single-purpose tools work better
- At most one level of nested parameters

**Strict Schema Validation:**
- Add `strict: true` to ensure tool calls always match schema exactly
- Prevents type mismatches or missing fields
- Essential for production agents where invalid parameters cause failures

### 3.2 Error Handling

**Tool Result Processing:**

```json
{
  "type": "tool_result",
  "tool_use_id": "toolu_01D7FLrfh4GYq7yT1ULFeyMV",
  "content": "259.75 USD"
}
```

**Error Handling Patterns:**
- Document return formats clearly (data types, field names, possible values)
- Handle error states gracefully in tool responses
- Use `is_error: true` flag for failed tool calls
- Provide actionable error messages that guide retry behavior

**Retry Strategy:**
- Implement exponential backoff for transient failures
- Cap maximum retry attempts
- Preserve tool call context across retries
- Consider fallback tools for critical operations

### 3.3 Advanced Tool Use Features

**Three New Beta Features (November 2025):**

#### Tool Search Tool
- Allows Claude to discover tools on-demand rather than loading all definitions
- Reduces token consumption by 85% in testing
- Mark tools with `defer_loading: true` for discovery
- Best for >10K tokens in tool definitions

#### Programmatic Tool Calling
- Claude orchestrates tools through code rather than sequential API calls
- 37% token reduction on complex research tasks
- Eliminates 19+ inference passes in 20+ tool call workflows
- Intermediate results stay in code execution environment

#### Tool Use Examples
- Provides concrete usage patterns beyond JSON schemas
- Accuracy improvement from 72% to 90% on complex parameter handling
- Include 1-5 realistic examples per tool
- Show minimal, partial, and full specification patterns

**Layered Approach:**
| Bottleneck | Solution |
|------------|----------|
| Context bloat | Tool Search Tool |
| Intermediate data pollution | Programmatic Tool Calling |
| Parameter errors | Tool Use Examples |

---

## 4. State Management

### 4.1 Context Handoff

**Orchestrator-Worker Pattern:**

The orchestrator-worker design features a central controller that:
1. Analyzes user queries
2. Develops strategies
3. Spawns subagents to explore aspects simultaneously
4. Synthesizes results from workers

**Subagent Delegation Requirements:**

Each subagent needs:
- Clear objective
- Output format specification
- Guidance on tools and sources available
- Clear task boundaries

**Scaling Rules:**
| Task Complexity | Agents | Tool Calls |
|-----------------|--------|------------|
| Simple fact-finding | 1 | 3-10 |
| Comparisons | 2-4 | Variable |
| Complex research | 10+ | Divided responsibilities |

**Context Window Transitions:**

Each new session follows standardized onboarding:
1. Verify working directory with `pwd`
2. Read progress logs and git history
3. Execute basic end-to-end tests before new work
4. Select single highest-priority incomplete feature

### 4.2 Session State Schema

**Critical Artifacts for Continuity:**

| Artifact | Purpose | Format |
|----------|---------|--------|
| `claude-progress.txt` | Chronological log of agent actions | Plain text |
| Feature list file | Requirements with pass/fail status | JSON |
| Git repository | Enables reverting and recovery | Git |
| `init.sh` script | Standardizes startup | Shell script |

**Two-Phase Harness Design:**
1. **Initializer Agent** (first session only): Sets up environment with context for future agents
2. **Coding Agent** (subsequent sessions): Continues work with structured artifact access

**Session Bookends:**
- Git commits and progress updates mark session boundaries
- Ensures code appropriate for merging to main branch
- Enables resumption from failure points

### 4.3 Multi-Agent Coordination

**Current State:** Synchronous execution where lead agent waits for subagent completion.

**Coordination Mechanisms:**
- Parallel tool calling: Subagents execute 3+ tools simultaneously
- State persistence: External memory stores completed work phases
- Error resilience: Systems resume from failure points
- Rainbow deployments: Gradual traffic shifts prevent disrupting running agents

**Context Preservation Across Windows:**

```python
class ConversationHistory:
    def __init__(self):
        self.turns = []

    def add_turn_assistant(self, content):
        self.turns.append({
            "role": "assistant",
            "content": [{"type": "text", "text": content}]
        })

    def add_turn_user(self, content):
        self.turns.append({
            "role": "user",
            "content": [{"type": "text", "text": content}]
        })

    def get_turns(self):
        # Apply ephemeral cache control to last user turn
        result = []
        for turn in reversed(self.turns):
            if turn["role"] == "user":
                result.append({
                    "role": "user",
                    "content": [{
                        "type": "text",
                        "text": turn["content"][0]["text"],
                        "cache_control": {"type": "ephemeral"}
                    }]
                })
                break
            result.append(turn)
        return list(reversed(result))
```

---

## 5. Anti-patterns

### 5.1 Tool Use Anti-patterns

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| **Context pollution from tool results** | 10MB log files enter context even when only summary needed | Use Programmatic Tool Calling to filter before Claude sees data |
| **Relying only on JSON schema** | Can't express usage patterns or conventions | Include 1-5 concrete examples per tool |
| **Inference overhead from multiple calls** | Each tool call requires full model inference pass | Use parallel tool calling and code-based orchestration |
| **Over-permissive tool permissions** | Security risk and decision paralysis | Only include tools the skill actually needs |
| **Complex custom commands** | Defeats purpose of natural language interface | Better instructions over magic commands |
| **Bloated tool sets** | Ambiguous decision points | Curate minimal viable toolset |

### 5.2 Prompt Anti-patterns

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| **Exhaustive edge case lists** | Clutters prompt, reduces focus | Curate diverse canonical examples instead |
| **Generic instructions** | "Add tests" yields worse results | Be specific: "Write test covering edge case where user is logged out" |
| **Vague uncertainty handling** | Leads to hallucination | Explicit permission to express uncertainty |
| **Overly rigid instructions** | Brittle behavior | Balance specificity with flexibility |
| **Poor CLAUDE.md maintenance** | Wasted context on ineffective instructions | Iterate and refine like any critical prompt |

### 5.3 Context Management Anti-patterns

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| **Pre-loading all data** | Context rot, diminishing returns | Just-in-time retrieval with lightweight identifiers |
| **Never clearing context** | Performance degradation | Use `/clear` between major tasks |
| **Single-agent for complex tasks** | Context exhaustion | Sub-agent architecture with result summarization |
| **No state persistence** | Lost progress across sessions | Structured note-taking and memory tools |
| **Attempting one-shot implementations** | Context exhausted mid-work | One feature per session, incremental progress |

### 5.4 Architecture Anti-patterns

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| **Vague subagent delegation** | Duplicated work, gaps, missed information | Detailed task descriptions with objectives and boundaries |
| **No testing enforcement** | Bugs not visible from code alone | Browser automation for verification |
| **Markdown feature lists** | Prone to inappropriate modification | JSON-formatted lists resist modification |
| **No failure recovery** | Full restarts on failure | Git-based recovery and checkpoint systems |

---

## 6. Sources

### Anthropic Official Sources

- [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) - Anthropic Engineering Blog (September 2025)
- [Claude Code: Best Practices for Agentic Coding](https://www.anthropic.com/engineering/claude-code-best-practices) - Anthropic Engineering Blog
- [How We Built Our Multi-Agent Research System](https://www.anthropic.com/engineering/multi-agent-research-system) - Anthropic Engineering Blog
- [Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) - Anthropic Engineering Blog
- [Introducing Advanced Tool Use on Claude Developer Platform](https://www.anthropic.com/engineering/advanced-tool-use) - Anthropic Engineering Blog (November 2025)
- [Claude 4 System Card](https://www.anthropic.com/claude-4-system-card) - Anthropic
- [Claude API Documentation](https://platform.claude.com/docs/en/api/messages) - Claude Platform
- [Prompting Best Practices](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices) - Claude Docs

### Context7 Sources

- [Claude Code Documentation](https://github.com/anthropics/claude-code) - Context7 Library ID: /anthropics/claude-code
- [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook) - Context7 Library ID: /anthropics/anthropic-cookbook
- [Anthropic Courses](https://github.com/anthropics/courses) - Context7 Library ID: /anthropics/courses
- [Awesome Claude Skills](https://github.com/composiohq/awesome-claude-skills) - Context7 Library ID: /composiohq/awesome-claude-skills

### Third-Party Analysis

- [Context Engineering 101: What We Can Learn from Anthropic](https://omnigeorgio.beehiiv.com/p/context-engineering-101-what-we-can-learn-from-anthropic)
- [Agentic Workflows with Claude: Architecture Patterns](https://medium.com/@aminsiddique95/agentic-workflows-with-claude-architecture-patterns-design-principles-production-patterns-72bbe4f7e85a) - Medium
- [Claude Agent SDK Best Practices for AI Agent Development (2025)](https://skywork.ai/blog/claude-agent-sdk-best-practices-ai-agents-2025/)
- [Mastering Claude Agent Patterns: A Deep Dive for 2025](https://sparkco.ai/blog/mastering-claude-agent-patterns-a-deep-dive-for-2025)
- [Claude Prompt Engineering Best Practices (2026)](https://promptbuilder.cc/blog/claude-prompt-engineering-best-practices-2026)

---

## Appendix A: Quick Reference Card

### System Prompt Template

```markdown
You are [ROLE] specializing in [DOMAIN].

## Core Responsibilities
1. [Primary responsibility]
2. [Secondary responsibility]

## Analysis Process
1. [Step one]
2. [Step two]

## Quality Standards
- [Standard 1]
- [Standard 2]

## Output Format
[Specification]

## If Unsure
Ask clarifying questions rather than guessing.

## Edge Cases
- [Case 1]: [Handling]
```

### Tool Definition Template

```json
{
  "name": "tool_name",
  "description": "Clear description of purpose and return value",
  "input_schema": {
    "type": "object",
    "properties": {
      "param": {
        "type": "string",
        "description": "What this parameter does and format"
      }
    },
    "required": ["param"]
  },
  "strict": true
}
```

### Context Engineering Checklist

- [ ] Minimal viable toolset defined
- [ ] Just-in-time retrieval implemented
- [ ] Compaction strategy in place
- [ ] Sub-agent delegation planned
- [ ] Progress persistence configured
- [ ] Error recovery mechanisms ready
- [ ] Session transition artifacts defined

---

*End of Document*
