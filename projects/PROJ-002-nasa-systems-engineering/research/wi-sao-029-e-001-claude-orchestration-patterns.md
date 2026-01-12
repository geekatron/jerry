# Research: Claude Code Orchestration Patterns for Multi-Agent Testing

**PS ID:** wi-sao-029
**Entry ID:** e-001
**Topic:** Claude Code Task Tool and Orchestration Patterns for Multi-Agent Testing
**Date:** 2026-01-11
**Researcher:** ps-researcher (Claude Opus 4.5)
**Status:** Complete

---

## L0: Executive Summary

Claude Code provides multi-agent orchestration through the **Task tool**, which spawns isolated subagents with their own context windows. Key findings for multi-agent testing workflows:

1. **Single Nesting Constraint (P-003):** Subagents cannot spawn other subagents. Maximum depth is 1 level (orchestrator → workers).

2. **Parallel Execution:** Up to 10 concurrent subagents, with queue management for larger workloads. Tasks can be launched in parallel by including multiple Task tool invocations in a single message.

3. **Context Isolation:** Each subagent has its own 200K token context window. Context passing is lossy - orchestrator summarizes relevant information in the task prompt.

4. **State Management:** File-based persistence is the primary pattern. Agents communicate via artifacts, not shared memory.

5. **Background Execution:** The `run_in_background` parameter enables async execution where agents create output files retrievable via TaskOutput tool.

6. **Model Selection:** Subagent types include Explore (Haiku), Plan, and General-Purpose. Custom agents can specify model via `model: sonnet | opus | haiku`.

**For multi-agent testing:** Use fan-out pattern to spawn parallel test agents, fan-in pattern to aggregate results, and sequential chains for dependent verification steps. All state must be persisted to files per P-002.

---

## L1: Technical Findings

### 1. Task Tool Specification

The Task tool is Claude Code's core mechanism for spawning subagents. Based on system prompt analysis and SDK documentation:

**Tool Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `subagent_type` | string | Yes | Selects which agent type to use |
| `prompt` | string | Yes | Detailed task description with context |
| `description` | string | Recommended | 3-5 word summary for logging/display |
| `resume` | string | No | Agent ID to continue previous invocation |
| `run_in_background` | boolean | No | Execute asynchronously while continuing work |

**Source:** [Claude Code Docs](https://code.claude.com/docs/en/sub-agents), [Claude Agent SDK](https://platform.claude.com/docs/en/agent-sdk/subagents)

**Token Cost:** Approximately 1,210 tokens for Task tool description alone (based on system prompt analysis).

### 2. Subagent Types

Claude Code provides built-in subagent types with specific capabilities:

| Type | Model | Purpose | Tools | Context Access |
|------|-------|---------|-------|----------------|
| **Explore** | Haiku | Codebase search | Read, Grep, Glob, limited Bash | Fresh (independent) |
| **Plan** | Varies | Dedicated planning | Full research capabilities | Full (inherits parent) |
| **General-Purpose** | Inherits | Complex multi-step tasks | All available tools | Full (inherits parent) |

**Custom Agents:** Defined via markdown files in `.claude/agents/` with YAML frontmatter:

```yaml
---
name: test-runner
description: Executes test suites and validates outputs
tools: Read, Bash, Grep, Glob
model: sonnet
---

You are a test execution specialist...
```

**Sources:** [Claude Code Subagents](https://code.claude.com/docs/en/sub-agents), [Claude Agent SDK](https://platform.claude.com/docs/en/agent-sdk/subagents)

### 3. Context Passing Mechanics

**Critical Constraint:** Subagents start with **minimal context**. The orchestrator must explicitly include relevant information in the task prompt.

```
┌─────────────────────────────────────────┐
│         ORCHESTRATOR CONTEXT            │
│  [Full conversation history]            │
│  [All tool results]                     │
│  [User messages]                        │
│                                         │
│         │ Task Tool                     │
│  ┌──────────────────┐                   │
│  │ Summarized prompt │                  │
│  │ (Lossy transfer) │                   │
│  └────────┬─────────┘                   │
└───────────┼─────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────┐
│         SUBAGENT CONTEXT                │
│  [Fresh context window - 200K tokens]   │
│  [Summarized prompt only]               │
│  [No access to parent tool results]     │
└─────────────────────────────────────────┘
```

**Context Access Types:**
- **Full context access:** General-purpose, Plan subagents (can see conversation before tool call)
- **Fresh context:** Explore subagent (search tasks are independent)

**Known Limitations:**
1. Parent agent does not know contents of files created by subagents
2. Information flow bottleneck through lead agent
3. Multi-hop transfers degrade quality ("game of telephone" effect)

**Sources:** [GitHub Issue #1770](https://github.com/anthropics/claude-code/issues/1770), [GitHub Issue #16153](https://github.com/anthropics/claude-code/issues/16153)

### 4. Parallel Execution

**Concurrency Limits:**
- Maximum 10 parallel subagents
- Additional tasks are queued automatically
- Tasks pulled from queue as slots become available

**Batch Execution Pattern:**

```
Parallelism Level: 4
Total Tasks: 10

Batch 1: Tasks 1-4 (parallel) → Complete
Batch 2: Tasks 5-8 (parallel) → Complete
Batch 3: Tasks 9-10 (parallel) → Complete
```

**Best Practice:** "Launch multiple agents concurrently whenever possible. To do that, use a single message with multiple tool uses."

**Example Parallel Invocation (Conceptual):**

```python
# Single message with multiple Task tool calls
[
    Task(description="Test auth module", prompt="..."),
    Task(description="Test data layer", prompt="..."),
    Task(description="Test API endpoints", prompt="...")
]
# All three execute in parallel
```

**Sources:** [Anthropic Engineering Blog](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk), [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)

### 5. Background Execution

The `run_in_background` parameter enables asynchronous execution:

**Behavior:**
1. Task starts execution
2. Control returns immediately to orchestrator
3. Orchestrator can continue other work
4. Agent creates output files during execution
5. Results retrievable via TaskOutput tool

**Use Cases:**
- Long-running research tasks
- Parallel independent analyses
- Non-blocking test execution

**TaskOutput Tool:** Used to retrieve results from background tasks by agent ID.

**Sources:** [Claude Code Subagents](https://code.claude.com/docs/en/sub-agents)

### 6. Resumption Capability

The `resume` parameter allows continuing a previous agent invocation:

```python
Task(
    subagent_type="test-runner",
    resume="agent-12345-abcde",  # Agent ID from previous run
    prompt="Continue from where you left off"
)
```

**Use Cases:**
- Recovery from interruption
- Iterative refinement workflows
- Long-running multi-session tasks

**Sources:** [Claude Code Subagents](https://code.claude.com/docs/en/sub-agents)

### 7. Result Communication

When a subagent completes:

1. Returns a single message back to orchestrator
2. Includes an agent ID for potential resumption
3. Output is initially **invisible to users**
4. Orchestrator must summarize findings in a visible message
5. Background agents create output files retrievable via file-reading tools

**Sources:** [Claude Code Subagents](https://code.claude.com/docs/en/sub-agents)

### 8. State Management Patterns

**File-Based State (P-002 Compliant):**

```
project/
├── tests/
│   ├── test-state.yaml       # Machine-readable state
│   ├── test-results/         # Agent outputs
│   │   ├── agent-001.md
│   │   ├── agent-002.md
│   │   └── agent-003.md
│   └── synthesis/            # Aggregated results
│       └── test-summary.md
└── ORCHESTRATION.yaml        # Workflow state (SSOT)
```

**State Handoff Between Agents:**

Agents communicate via artifacts, not shared memory:

```yaml
# Agent A output
agent_a_output:
  artifact_path: "tests/test-results/agent-001.md"
  summary: "Test suite passed with 95% coverage"
  next_agent_hint: "agent-b for synthesis"

# Agent B reads Agent A's artifact
# Agent B creates its own output
```

**Sources:** [skills/orchestration/docs/STATE_SCHEMA.md], [skills/problem-solving/docs/ORCHESTRATION.md]

---

## L2: Orchestration Patterns for Multi-Agent Testing

### Pattern 1: Sequential Chain

**Use When:** Tests have dependencies (e.g., setup → test → teardown).

```
┌─────────┐     ┌─────────┐     ┌─────────┐
│ Setup   │────►│  Test   │────►│Teardown │
│ Agent   │     │ Agent   │     │ Agent   │
└─────────┘     └─────────┘     └─────────┘
     │               │               │
     ▼               ▼               ▼
  CP-001          CP-002          CP-003
  (checkpoint)    (checkpoint)    (checkpoint)
```

**Implementation:**

```python
# Step 1: Setup
setup_result = Task(
    description="Setup test environment",
    prompt="Create test fixtures and initialize database..."
)

# Step 2: Test (references setup output)
test_result = Task(
    description="Execute test suite",
    prompt=f"""
    ## UPSTREAM ARTIFACTS
    - Setup: {setup_result.artifact_path}

    Execute all test cases...
    """
)

# Step 3: Teardown (references test output)
teardown_result = Task(
    description="Cleanup test environment",
    prompt=f"""
    ## UPSTREAM ARTIFACTS
    - Test Results: {test_result.artifact_path}

    Cleanup test fixtures...
    """
)
```

**Source:** [skills/orchestration/docs/PATTERNS.md]

### Pattern 2: Fan-Out (Parallel Tests)

**Use When:** Independent test suites can run concurrently.

```
                  ┌─────────┐
                  │  Start  │
                  └────┬────┘
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
   ┌────────┐    ┌────────┐    ┌────────┐
   │Test A  │    │Test B  │    │Test C  │
   │(auth)  │    │(data)  │    │(api)   │
   └────┬───┘    └────┬───┘    └────┬───┘
        │              │              │
        └──────────────┴──────────────┘
                       │
                       ▼
                [All Complete]
```

**Implementation:**

Launch multiple Task calls in a single message:

```python
# All three execute in parallel
Task(description="Test auth module", prompt="..."),
Task(description="Test data layer", prompt="..."),
Task(description="Test API endpoints", prompt="...")
```

**Validated in Jerry Framework:**
- TEST-ORCH-002 demonstrated 3 parallel agents with no interference
- All agents reference same input requirements
- Total output: 32,950 bytes from 3 concurrent agents

**Source:** [projects/PROJ-002.../tests/ORCHESTRATION-TEST-STRATEGY.md] (TEST-ORCH-002)

### Pattern 3: Fan-In (Result Aggregation)

**Use When:** Aggregating results from multiple parallel test agents.

```
   ┌────────┐    ┌────────┐    ┌────────┐
   │Test A  │    │Test B  │    │Test C  │
   └────┬───┘    └────┬───┘    └────┬───┘
        │              │              │
        └──────────────┼──────────────┘
                       ▼
                ┌────────────┐
                │ Synthesize │
                │  (report)  │
                └────────────┘
```

**Implementation:**

```python
# After all parallel tests complete
Task(
    description="Synthesize test results",
    prompt=f"""
    ## INPUT ARTIFACTS
    - Auth Tests: tests/results/auth-test.md
    - Data Tests: tests/results/data-test.md
    - API Tests: tests/results/api-test.md

    Aggregate all test results into a consolidated report:
    - Total pass/fail counts
    - Coverage metrics
    - Critical issues
    """
)
```

**Validated in Jerry Framework:**
- TEST-ORCH-003 demonstrated aggregation from 6 source artifacts
- Single output: 14,473 bytes with 20+ explicit source references
- L0/L1/L2 structure properly organized

**Source:** [projects/PROJ-002.../tests/ORCHESTRATION-TEST-STRATEGY.md] (TEST-ORCH-003)

### Pattern 4: Generator-Critic (Test Quality)

**Use When:** Iterative test refinement with quality gates.

```
┌────────────┐         ┌────────────┐
│  Test      │────────►│  Reviewer  │
│  Generator │         │  (Critic)  │
└────────────┘         └─────┬──────┘
      ▲                      │
      │                      │ Feedback
      │                      ▼
      │                ┌──────────┐
      └────────────────┤ Threshold│
                       │  Met?    │
                       └──────────┘
                            │
                            ▼ Yes
                       ┌──────────┐
                       │  Accept  │
                       └──────────┘
```

**Circuit Breaker Settings:**
- max_iterations: 3
- improvement_threshold: 10%
- Stop if no improvement after 2 consecutive iterations

**Implementation:**

```python
# Generator creates test
test_result = Task(
    description="Generate tests",
    prompt="Create comprehensive test suite for module X..."
)

# Critic evaluates
review_result = Task(
    description="Review test quality",
    prompt=f"""
    ## ARTIFACT TO REVIEW
    - Tests: {test_result.artifact_path}

    Evaluate:
    - Coverage completeness
    - Edge case handling
    - Assertion quality

    Return PASS or provide specific feedback for improvement.
    """
)

# Loop if needed (max 3 iterations)
```

**Source:** [skills/orchestration/docs/PATTERNS.md]

### Pattern 5: Review Gate (Quality Validation)

**Use When:** Formal review checkpoints are required.

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Artifacts  │────►│  Reviewer   │────►│ READY/NOT   │
│  (all tests)│     │  (Gate)     │     │   READY     │
└─────────────┘     └─────────────┘     └─────────────┘
```

**Validated in Jerry Framework:**
- TEST-ORCH-004 demonstrated CDR readiness assessment
- 10 entrance criteria evaluated
- Verdict: READY (95% compliance)
- Evidence cited for each criterion

**Source:** [projects/PROJ-002.../tests/ORCHESTRATION-TEST-STRATEGY.md] (TEST-ORCH-004)

### Constitutional Constraints (P-003 Compliance)

All orchestration patterns MUST comply with:

| Principle | Constraint | Enforcement |
|-----------|------------|-------------|
| P-003 | No Recursive Subagents | Agents CANNOT spawn other agents |
| P-002 | File Persistence | All state persisted to files |
| P-020 | User Authority | User can override any decision |
| P-022 | No Deception | Honest status reporting |

**P-003 Architecture:**

```
MAIN CONTEXT (Claude) ← Orchestrator
    │
    ├──► test-agent-001    (worker, cannot spawn)
    ├──► test-agent-002    (worker, cannot spawn)
    ├──► test-agent-003    (worker, cannot spawn)
    └──► synthesis-agent   (worker, cannot spawn)

Maximum nesting depth: 1 level
```

**Sources:** [docs/governance/JERRY_CONSTITUTION.md], [skills/orchestration/SKILL.md]

---

## Industry References

### Anthropic Official Documentation

1. [Create custom subagents - Claude Code Docs](https://code.claude.com/docs/en/sub-agents) - Official subagent format and Task tool
2. [Building agents with the Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk) - SDK architecture
3. [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) - Orchestrator-worker pattern
4. [Claude Code: Best practices for agentic coding](https://www.anthropic.com/engineering/claude-code-best-practices) - Parallel execution
5. [Agent SDK overview - Claude Docs](https://platform.claude.com/docs/en/agent-sdk/overview) - SDK overview
6. [Subagents in the SDK - Claude Docs](https://platform.claude.com/docs/en/agent-sdk/subagents) - Subagent specification
7. [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) - Context management

### Industry Patterns

8. [Microsoft AI Agent Orchestration Patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns) - Enterprise patterns
9. [LangGraph Documentation](https://langchain-ai.github.io/langgraph/) - State management
10. [CrewAI Flows](https://docs.crewai.com/concepts/flows) - Multi-agent workflows

### Internal Research

11. [agent-research-001-claude-code-mechanics.md] - Task tool deep dive
12. [agent-research-002-multi-agent-patterns.md] - Framework comparison
13. [wi-sao-009-e-001-claude-engineer-patterns.md] - Boris Cherny patterns
14. [ORCHESTRATION-TEST-STRATEGY.md] - Validated test patterns

---

## Recommendations for Multi-Agent Testing

### 1. Test Architecture

```
tests/
├── ORCHESTRATION.yaml           # Workflow state (SSOT)
├── test-config.yaml             # Test configuration
├── parallel-tests/              # Fan-out test agents
│   ├── test-suite-001/
│   ├── test-suite-002/
│   └── test-suite-003/
├── synthesis/                   # Fan-in aggregation
│   └── test-summary.md
└── checkpoints/                 # Recovery points
    ├── CP-001.yaml
    └── CP-002.yaml
```

### 2. Agent Invocation Template

```python
Task(
    description="test-{suite-name}: {short-description}",
    subagent_type="general-purpose",  # or custom "test-runner"
    prompt="""
You are a test execution agent.

## TEST CONTEXT
- **Test Suite:** {suite_name}
- **Test ID:** {test_id}
- **Scope:** {scope_description}

## UPSTREAM ARTIFACTS (if applicable)
- {artifact_type}: {path}

## MANDATORY PERSISTENCE (P-002)
After completing tests, you MUST:
1. Create file at: `tests/{suite}/results-{test_id}.md`
2. Include pass/fail counts, coverage, and critical issues

## YOUR TASK
{Detailed test description}
"""
)
```

### 3. Error Handling

| Error Type | Handling |
|------------|----------|
| Agent timeout | Preserve partial output, allow resume via agent ID |
| Test failure | Record failure in artifact, continue other parallel tests |
| Missing dependency | Graceful failure with clear error message |
| State inconsistency | Rebuild from file artifacts (source of truth) |

### 4. Parallel Test Execution

- Use fan-out pattern for independent test suites
- Maximum 10 concurrent agents (queue handles overflow)
- Each agent writes to isolated output path
- No shared mutable state between parallel agents
- Aggregate results with fan-in synthesis agent

---

*Research completed: 2026-01-11*
*Compliance: P-001 (sourced), P-002 (persisted), P-004 (documented)*
*Next action: Apply patterns to multi-agent QA testing framework*
