# Research: LLM Guardrail Frameworks - Industry Survey

<!--
DOCUMENT-ID: FEAT-005:EN-401-TASK-002-RESEARCH
AUTHOR: ps-researcher agent (v2.2.0)
DATE: 2026-02-12
STATUS: Complete (pending adversarial quality review)
PARENT: EN-401 (Deep Research: Enforcement Vectors & Best Practices)
FEATURE: FEAT-005 (Quality Framework Enforcement Mechanisms)
EPIC: EPIC-002 (Quality Framework Enforcement)
PROJECT: PROJ-001-oss-release
PS-ID: EN-401
ENTRY-ID: TASK-002
-->

> **Version:** 1.0.0
> **Agent:** ps-researcher (v2.2.0)
> **Confidence:** HIGH for Guardrails AI, NeMo Guardrails, LangChain (well-documented OSS projects); MEDIUM-HIGH for Constitutional AI (published research); MEDIUM for emerging frameworks (Llama Guard, Rebuff, Semantic Kernel -- less documentation available through training data)
> **Research Limitation:** WebSearch, WebFetch, and Context7 tools were unavailable during this research session. All content is sourced from the agent's training knowledge (literature through May 2025) and from citations within the Jerry codebase. A follow-up web-validation pass is recommended to verify URLs and check for post-May-2025 updates.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | L0 overview of the guardrail framework landscape and Jerry relevance |
| [Methodology](#methodology) | Research approach, source evaluation, confidence disclosure |
| [Framework 1: Guardrails AI](#framework-1-guardrails-ai) | Deep dive into architecture, validators, guard composition, enforcement modes |
| [Framework 2: NVIDIA NeMo Guardrails](#framework-2-nvidia-nemo-guardrails) | Colang language, rail types, programmable flows, LLM integration |
| [Framework 3: LangChain/LangGraph](#framework-3-langchainlanggraph-guardrails) | Output parsers, state machine enforcement, tool validation |
| [Framework 4: Anthropic Constitutional AI](#framework-4-anthropic-constitutional-ai) | Principle-based self-critique, enforcement mechanism |
| [Framework 5: Microsoft Semantic Kernel](#framework-5-microsoft-semantic-kernel) | Filters, planners, guardrails patterns |
| [Framework 6: CrewAI](#framework-6-crewai) | Task guardrails, agent constraints, structured output |
| [Framework 7: Meta Llama Guard](#framework-7-meta-llama-guard) | Classification-based safety, taxonomy-driven enforcement |
| [Framework 8: Rebuff](#framework-8-rebuff) | Prompt injection detection, multi-layer defense |
| [Framework 9: Other Notable Frameworks](#framework-9-other-notable-frameworks) | Guidance, Outlines, Instructor, LMQL |
| [Comparative Analysis](#comparative-analysis) | L2 comparison matrix across all frameworks |
| [Architectural Patterns for Jerry](#architectural-patterns-for-jerry) | Recommended patterns, integration considerations |
| [Sources and References](#sources-and-references) | Full bibliography |
| [Disclaimer](#disclaimer) | Research limitations and caveats |

---

## Executive Summary

### The LLM Guardrail Landscape (L0)

The LLM guardrail ecosystem has rapidly matured since 2023, producing a diverse set of frameworks that enforce constraints on LLM inputs, outputs, and workflows. This research surveys **9 major frameworks** and identifies **6 architectural patterns** directly applicable to Jerry's enforcement mechanisms.

**Key Finding:** The industry has converged on a **layered enforcement model** with three primary enforcement levels:

1. **Input-level enforcement** -- Validating/modifying prompts before they reach the LLM (NeMo input rails, Rebuff prompt injection detection, Guardrails AI input validation)
2. **Output-level enforcement** -- Validating/correcting LLM responses after generation (Guardrails AI validators, LangChain output parsers, Llama Guard classification)
3. **Workflow-level enforcement** -- Enforcing state machines, checkpoints, and process compliance across multi-step interactions (LangGraph state machines, CrewAI task guardrails, NeMo dialog rails)

**Jerry occupies a unique position** in this landscape because it enforces **process compliance** (quality gates, adversarial review cycles, skill invocation) rather than **content safety** (toxicity, hallucination, PII). Most existing frameworks focus on content safety. However, the architectural patterns they use -- validators, rails, state machines, layered defense -- are directly transferable to process compliance enforcement.

### Top 6 Patterns for Jerry Adoption

| # | Pattern | Source Framework(s) | Jerry Application |
|---|---------|--------------------|--------------------|
| 1 | **Validator Composition** | Guardrails AI | Chain multiple quality validators (artifact presence, quality score, citation check) |
| 2 | **Programmable Rails** | NeMo Guardrails | Define enforcement flows in a declarative language (rules files + hooks) |
| 3 | **State Machine Enforcement** | LangGraph | Enforce workflow compliance via checkpoint-gated state transitions |
| 4 | **Self-Critique Loop** | Constitutional AI | Embed quality self-evaluation as mandatory post-generation step |
| 5 | **Multi-Layer Defense** | Rebuff, NeMo, Guardrails AI | Combine input rails + output validation + workflow gates |
| 6 | **Structured Output Enforcement** | LangChain, Instructor, Outlines | Enforce schema compliance on deliverable structure |

---

## Methodology

### Research Approach

This research was conducted using a systematic framework analysis method:

1. **Framework Identification**: Identified candidate frameworks from published literature, GitHub repositories, conference proceedings, and industry reports through training data (cutoff: May 2025).

2. **Architecture Analysis**: For each framework, analyzed: (a) core architecture and design philosophy, (b) enforcement mechanisms and their implementation, (c) extensibility and composition patterns, (d) enforcement modes (block, warn, correct, log).

3. **Pattern Extraction**: Extracted reusable architectural patterns that can be applied to Jerry regardless of the source framework's specific implementation.

4. **Comparative Analysis**: Built a multi-dimensional comparison matrix across all frameworks.

5. **Jerry Applicability Assessment**: Evaluated each framework's patterns against Jerry's specific requirements (process compliance, quality gates, adversarial review cycles).

### Source Evaluation

| Source Type | Confidence Level | Justification |
|-------------|-----------------|---------------|
| Published OSS documentation (GitHub READMEs, official docs) | **High** | Verified, maintained by framework authors |
| Published research papers (arXiv, NeurIPS, ICML) | **High** | Peer-reviewed or well-cited preprints |
| Blog posts and tutorials | **Medium** | Practical but may be outdated or opinionated |
| Training data knowledge | **Medium** | May be outdated for rapidly evolving projects |

### Confidence Disclosure

**IMPORTANT**: WebSearch, WebFetch, and Context7 query-docs tools were unavailable during this research session. All information is sourced from training data (cutoff: May 2025). The guardrail framework landscape evolves rapidly -- specific API details, version numbers, and feature sets should be verified against current documentation before implementation decisions are made.

---

## Framework 1: Guardrails AI

### Overview

**Guardrails AI** (https://www.guardrailsai.com/) is an open-source Python framework that provides a structured approach to validating LLM outputs. It wraps LLM calls with a `Guard` object that applies a chain of `Validator` instances to the LLM's response.

- **GitHub**: https://github.com/guardrails-ai/guardrails
- **License**: Apache 2.0
- **Language**: Python
- **Maturity**: Production-ready (v0.4.x+ as of early 2025)
- **Primary Focus**: Output validation and correction

### Architecture

Guardrails AI follows a **middleware/pipeline architecture** where the LLM call is wrapped by a Guard that orchestrates validation:

```
User Prompt
    |
    v
[Guard Object]
    |
    +-- Pre-processing (prompt template, input validation)
    |
    +-- LLM Call (OpenAI, Anthropic, local models)
    |
    +-- Post-processing Pipeline
    |   |
    |   +-- Validator 1 (e.g., no_profanity)
    |   +-- Validator 2 (e.g., valid_json)
    |   +-- Validator 3 (e.g., entity_extraction)
    |   |
    |   +-- On Failure:
    |       +-- REASK: Re-prompt the LLM with validation feedback
    |       +-- FIX: Programmatically correct the output
    |       +-- FILTER: Remove invalid portions
    |       +-- REFRAIN: Return None/empty
    |       +-- NOOP: Log and pass through
    |       +-- EXCEPTION: Raise error
    |
    v
Validated Output
```

**Key Architectural Insight**: The Guard acts as an **interceptor** that sits between the caller and the LLM. This is architecturally equivalent to Jerry's hook system -- both intercept at lifecycle boundaries.

### Validators

Guardrails AI provides both built-in validators and a community-contributed **Guardrails Hub** (https://hub.guardrailsai.com/):

**Built-in Validator Types:**

| Category | Validators | Description |
|----------|-----------|-------------|
| **Structural** | `valid_json`, `valid_python`, `valid_sql` | Output follows syntactic rules |
| **Semantic** | `is_relevant`, `on_topic`, `no_hallucination` | Output is semantically appropriate |
| **Content Safety** | `no_profanity`, `no_pii`, `no_toxic_language` | Output meets safety standards |
| **Custom** | User-defined validators | Any programmatic check |

**Validator Interface:**

```python
from guardrails.validators import Validator, register_validator, PassResult, FailResult

@register_validator(name="quality-score-check", data_type="string")
class QualityScoreValidator(Validator):
    """Validates that output contains a quality score >= threshold."""

    def __init__(self, threshold: float = 0.92, **kwargs):
        super().__init__(threshold=threshold, **kwargs)
        self._threshold = threshold

    def validate(self, value: str, metadata: dict) -> PassResult | FailResult:
        # Extract quality score from output
        score = self._extract_score(value)
        if score is None:
            return FailResult(
                error_message="Output does not contain a quality score. "
                              "Include a quality score calculation.",
                fix_value=None,
            )
        if score < self._threshold:
            return FailResult(
                error_message=f"Quality score {score} is below threshold {self._threshold}.",
                fix_value=None,
            )
        return PassResult()
```

**Citation**: Guardrails AI documentation, "Writing Custom Validators" (https://docs.guardrailsai.com/hub/how_to_guides/custom_validator/).

### Guard Composition

Multiple validators are composed within a `Guard` object using a **RAIL specification** (Reliable AI Markup Language) or Python API:

**RAIL XML Specification:**

```xml
<rail version="0.1">
  <output>
    <string name="analysis"
            validators="is_relevant;no_hallucination;quality-score-check"
            on-fail-is_relevant="reask"
            on-fail-no_hallucination="reask"
            on-fail-quality-score-check="reask" />
  </output>
</rail>
```

**Python API:**

```python
from guardrails import Guard
from guardrails.hub import IsRelevant, NoHallucination

guard = Guard().use_many(
    IsRelevant(on_fail="reask"),
    NoHallucination(on_fail="reask"),
    QualityScoreValidator(threshold=0.92, on_fail="reask"),
)

result = guard(
    llm_api=openai.chat.completions.create,
    prompt="Analyze the enforcement vectors...",
    model="gpt-4",
    max_tokens=2000,
    num_reasks=3,  # Maximum retry attempts
)
```

**Composition Patterns:**
- **Sequential**: Validators run in order; first failure triggers the on-fail action
- **Parallel**: Validators can be grouped to run concurrently for performance
- **Conditional**: Validators can be conditionally applied based on metadata
- **Nested**: Guard can validate nested structures (e.g., JSON fields independently)

**Citation**: Guardrails AI documentation, "Guard Composition" (https://docs.guardrailsai.com/concepts/guard/).

### Enforcement Modes

| Mode | Guardrails AI Name | Behavior | Jerry Equivalent |
|------|-------------------|----------|-----------------|
| **Correct** | `FIX` | Programmatically fix the output | PostToolUse hook with correction injection |
| **Retry** | `REASK` | Re-prompt the LLM with validation feedback | Creator-Critic-Revision loop |
| **Filter** | `FILTER` | Remove invalid portions, return rest | Partial output with quality warnings |
| **Block** | `REFRAIN` | Return None/empty | PreToolUse hook `block` decision |
| **Error** | `EXCEPTION` | Raise Python exception | Hard enforcement failure |
| **Log** | `NOOP` | Log violation, pass through | Advisory enforcement |

**Key Insight for Jerry**: The `REASK` pattern is architecturally identical to Jerry's creator-critic-revision cycle. Guardrails AI's `num_reasks` parameter (maximum retry attempts) maps directly to Jerry's "max 3 iterations" rule. The key difference is that Guardrails AI automates the retry loop, while Jerry requires explicit agent orchestration.

### Relevance to Jerry

**Directly Applicable Patterns:**

1. **Validator abstraction**: Define quality checks as composable, reusable validators. Jerry could define validators for: artifact presence, quality score threshold, citation presence, template compliance, test file existence.

2. **On-fail actions**: The graduated response model (fix > reask > filter > refrain > exception) maps to Jerry's enforcement tiers (advisory > soft > medium > hard).

3. **REASK as self-correction**: The automatic re-prompting with validation feedback is the programmatic equivalent of Jerry's adversarial review cycle. Jerry's hooks could inject validation failure feedback into the next prompt.

4. **Schema-driven validation**: RAIL specifications provide a declarative way to define expected output structure. Jerry could define RAIL-like specifications for deliverable templates.

**Gaps vs Jerry's Needs:**

- Guardrails AI focuses on **single LLM call** validation, not **multi-step workflow** enforcement
- No built-in support for **process compliance** (skill invocation, planning prerequisites)
- No **stateful enforcement** across a conversation session

---

## Framework 2: NVIDIA NeMo Guardrails

### Overview

**NVIDIA NeMo Guardrails** (https://github.com/NVIDIA/NeMo-Guardrails) is an open-source toolkit for adding programmable guardrails to LLM-based conversational systems. Its distinguishing feature is **Colang**, a purpose-built modeling language for defining conversational guardrails.

- **GitHub**: https://github.com/NVIDIA/NeMo-Guardrails
- **License**: Apache 2.0
- **Language**: Python, Colang (DSL)
- **Maturity**: Production-ready (v0.9.x as of early 2025)
- **Primary Focus**: Conversational AI safety and compliance

### Architecture

NeMo Guardrails follows a **runtime interception architecture** with three categories of rails:

```
User Input
    |
    v
[INPUT RAILS] <-- Pre-processing guardrails
    |  - Jailbreak detection
    |  - Topic restriction
    |  - Input sanitization
    |  - Content moderation
    |
    v
[DIALOG RAILS] <-- Conversation flow control
    |  - Canonical form matching
    |  - Flow enforcement
    |  - Topic steering
    |  - Action sequencing
    |
    v
[LLM GENERATION]
    |
    v
[OUTPUT RAILS] <-- Post-generation guardrails
    |  - Hallucination detection
    |  - Fact checking
    |  - Output moderation
    |  - Format validation
    |
    v
Final Response
```

**Key Architectural Insight**: The three-rail architecture (input, dialog, output) provides enforcement at three distinct lifecycle phases. This maps directly to Jerry's hook architecture:
- **Input rails** = UserPromptSubmit hook
- **Dialog rails** = Session-level state machine enforcement (no direct Jerry equivalent yet)
- **Output rails** = PostToolUse hook

### Colang Programming Language

Colang is a domain-specific language (DSL) for defining conversational guardrails. It uses a natural-language-like syntax for defining message patterns, flows, and actions:

**Colang v2.x Syntax:**

```colang
# Define canonical forms for user messages
define user ask about implementation
  "Can you implement this feature?"
  "Write the code for..."
  "Build the..."
  "Let's implement..."

# Define a guardrail flow
define flow check_quality_prerequisites
  """Enforce quality prerequisites before implementation."""
  user ask about implementation

  # Check if plan exists
  $plan_exists = execute check_plan_exists()

  if not $plan_exists
    bot inform "A quality plan is required before implementation. "
        "Please create a PLAN.md first using /orchestration."
    stop

  # Check if tests exist
  $tests_exist = execute check_tests_exist()

  if not $tests_exist
    bot inform "Tests should be written first (Red phase of BDD). "
        "Please create test files before implementing."

# Define an action
define action check_plan_exists
  """Check if PLAN.md exists in the project directory."""
  # Python action registered in config
```

**Colang Key Concepts:**

| Concept | Description | Jerry Equivalent |
|---------|-------------|-----------------|
| **Canonical forms** | Normalized representations of user intents | Task classification in UserPromptSubmit hook |
| **Flows** | Sequences of interactions with conditions and actions | Workflow enforcement in orchestration |
| **Actions** | Python functions callable from Colang | Hook script logic |
| **Bot messages** | Responses injected by the guardrail system | Context injection via hooks |
| **Variables** | Session-scoped state | Stateful enforcement via filesystem |

**Citation**: NVIDIA NeMo Guardrails documentation, "Colang Language Reference" (https://docs.nvidia.com/nemo/guardrails/colang-2/overview.html).

### Rail Types in Detail

#### Input Rails

Input rails process the user's message before it reaches the LLM:

```colang
define flow input_check_quality_requirements
  """Block implementation requests that lack prerequisites."""
  user ask about implementation

  $has_plan = execute check_artifact("PLAN.md")
  $has_tests = execute check_artifact("tests/")

  if not $has_plan
    bot "QUALITY GATE: Cannot proceed with implementation. "
        "No PLAN.md found. Please create one first."
    stop
```

**Enforcement modes for input rails:**
- **Block**: Prevent the message from reaching the LLM
- **Modify**: Alter the message before it reaches the LLM (e.g., prepend quality context)
- **Allow**: Pass through with optional logging

#### Dialog Rails

Dialog rails enforce conversation-level patterns across multiple turns:

```colang
define flow enforce_creator_critic_cycle
  """Ensure creator-critic-revision cycle is followed."""

  # Track state
  $phase = "creator"

  # Creator phase
  user request implementation
  bot produce implementation artifact
  $phase = "critic"

  # Critic phase (must happen before completion)
  bot invoke adversarial review
  $review_score = execute get_review_score()

  if $review_score < 0.92
    $phase = "revision"
    bot request revision based on critique
    # Loop back to critic
  else
    $phase = "complete"
    bot confirm quality gate passed
```

**Key Insight for Jerry**: Dialog rails are the most unique and powerful feature of NeMo Guardrails, and they address a gap in Jerry's current enforcement. Jerry's hooks operate at individual lifecycle points, but **dialog rails enforce patterns across the entire conversation**. This is the enforcement equivalent of a state machine that tracks whether the agent is following the prescribed workflow.

#### Output Rails

Output rails validate and potentially modify LLM responses:

```colang
define flow output_check_citations
  """Ensure all claims have citations."""
  bot $response

  $has_citations = execute check_citations($response)

  if not $has_citations
    bot "NOTE: The previous response contained claims without citations. "
        "Per quality requirements, all claims must have authoritative citations."
```

### LLM Integration

NeMo Guardrails wraps the LLM call and manages the full interaction lifecycle:

```python
from nemoguardrails import LLMRails, RailsConfig

config = RailsConfig.from_path("./config")
rails = LLMRails(config)

# The rails object wraps the LLM and enforces all defined guardrails
response = rails.generate(messages=[
    {"role": "user", "content": "Implement the work item tracking feature"}
])
```

**Configuration structure:**

```yaml
# config.yml
models:
  - type: main
    engine: openai
    model: gpt-4

rails:
  input:
    flows:
      - input_check_quality_requirements
  dialog:
    flows:
      - enforce_creator_critic_cycle
  output:
    flows:
      - output_check_citations
```

**Citation**: NVIDIA NeMo Guardrails documentation, "Getting Started" (https://docs.nvidia.com/nemo/guardrails/getting-started.html).

### Relevance to Jerry

**Directly Applicable Patterns:**

1. **Three-rail architecture**: Input, dialog, and output rails provide enforcement at three distinct lifecycle phases. Jerry's hook system maps well to input rails (UserPromptSubmit) and output rails (PostToolUse), but lacks dialog-level enforcement.

2. **Colang-inspired declarative enforcement**: While Jerry cannot use Colang directly (it wraps a different LLM runtime), the concept of declaring enforcement flows in a readable DSL is valuable. Jerry's `.claude/rules/` files serve a similar purpose but lack programmability.

3. **Canonical form matching**: NeMo's intent classification for routing enforcement is analogous to Jerry's proposed task classification in the UserPromptSubmit hook.

4. **Session-scoped state**: NeMo maintains state across the conversation, enabling dialog-level enforcement. Jerry's proposed `.jerry/enforcement/session-state.json` addresses the same need.

**Gaps vs Jerry's Needs:**

- NeMo Guardrails is designed to **wrap** the LLM call. Jerry's enforcement must work **alongside** Claude Code's existing architecture (hooks), not replace it.
- Colang requires a separate runtime engine. Jerry would need to implement equivalent logic in Python hook scripts.
- NeMo focuses on safety guardrails rather than process compliance guardrails.

---

## Framework 3: LangChain/LangGraph Guardrails

### Overview

**LangChain** (https://github.com/langchain-ai/langchain) and **LangGraph** (https://github.com/langchain-ai/langgraph) provide complementary approaches to LLM guardrails: LangChain focuses on **output parsing and validation** while LangGraph provides **state machine enforcement** for multi-step workflows.

- **GitHub**: https://github.com/langchain-ai/langchain, https://github.com/langchain-ai/langgraph
- **License**: MIT
- **Language**: Python, JavaScript/TypeScript
- **Maturity**: Production-ready (LangChain v0.2.x+, LangGraph v0.1.x+ as of early 2025)
- **Primary Focus**: LLM application development and orchestration

### LangChain Output Parsers

LangChain provides structured output parsing that enforces schema compliance:

**Pydantic Output Parser:**

```python
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field, field_validator

class QualityDeliverable(BaseModel):
    """Schema for a quality-compliant deliverable."""

    content: str = Field(description="The main deliverable content")
    quality_score: float = Field(
        description="Quality score (0.0 - 1.0)",
        ge=0.0, le=1.0
    )
    citations: list[str] = Field(
        description="List of authoritative citations",
        min_length=1
    )
    review_iterations: int = Field(
        description="Number of creator-critic-revision iterations completed",
        ge=1
    )
    skill_invocations: list[str] = Field(
        description="Skills invoked during this work",
        min_length=1
    )

    @field_validator("quality_score")
    @classmethod
    def score_meets_threshold(cls, v: float) -> float:
        if v < 0.92:
            raise ValueError(
                f"Quality score {v} is below the 0.92 threshold. "
                "Revise deliverable until quality target is met."
            )
        return v

parser = PydanticOutputParser(pydantic_object=QualityDeliverable)

# Get format instructions to include in the prompt
format_instructions = parser.get_format_instructions()
# Returns: "The output should be formatted as a JSON instance that conforms to..."
```

**Output Fixing Parser (auto-correction):**

```python
from langchain.output_parsers import OutputFixingParser

fixing_parser = OutputFixingParser.from_llm(
    parser=parser,
    llm=ChatOpenAI(model="gpt-4"),
    max_retries=3,
)

# If parsing fails, the LLM is asked to fix the output
result = fixing_parser.parse(malformed_output)
```

**Key Insight for Jerry**: The `OutputFixingParser` with `max_retries` is another instance of the automated retry pattern (like Guardrails AI's `REASK`). The retry count maps to Jerry's maximum adversarial iteration count.

**Citation**: LangChain documentation, "Output Parsers" (https://python.langchain.com/docs/concepts/output_parsers/).

### LangGraph State Machine Enforcement

LangGraph enables **stateful, graph-based** workflow enforcement where each node is a processing step and edges define valid transitions:

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

class QualityWorkflowState(TypedDict):
    """State schema for quality-enforced workflow."""
    task_type: str
    plan_exists: bool
    implementation_complete: bool
    tests_written: bool
    review_score: float
    review_iterations: int
    artifacts_persisted: list[str]

def should_continue(state: QualityWorkflowState) -> str:
    """Quality gate: determine next step based on state."""
    if not state["plan_exists"]:
        return "create_plan"
    if not state["tests_written"]:
        return "write_tests"
    if not state["implementation_complete"]:
        return "implement"
    if state["review_score"] < 0.92 and state["review_iterations"] < 3:
        return "review"
    if state["review_score"] >= 0.92:
        return END
    return "escalate"

# Build the graph
workflow = StateGraph(QualityWorkflowState)

# Add nodes
workflow.add_node("create_plan", create_plan_node)
workflow.add_node("write_tests", write_tests_node)
workflow.add_node("implement", implement_node)
workflow.add_node("review", review_node)
workflow.add_node("escalate", escalate_node)

# Add conditional edges (quality gates)
workflow.add_conditional_edges(
    "implement",
    should_continue,
    {
        "review": "review",
        "create_plan": "create_plan",
        "write_tests": "write_tests",
    }
)

workflow.add_conditional_edges(
    "review",
    should_continue,
    {
        "review": "review",  # Loop for revision
        END: END,
        "escalate": "escalate",
    }
)

# Compile with checkpointing
from langgraph.checkpoint.sqlite import SqliteSaver
memory = SqliteSaver.from_conn_string("quality_checkpoints.db")
app = workflow.compile(checkpointer=memory)
```

**Key LangGraph Enforcement Concepts:**

| Concept | Description | Jerry Equivalent |
|---------|-------------|-----------------|
| **State schema** | TypedDict defining workflow state | `.jerry/enforcement/session-state.json` |
| **Conditional edges** | State-dependent routing | Quality gate decisions in hooks |
| **Checkpointing** | Automatic state persistence | Orchestration checkpoints |
| **Interrupts** | Human-in-the-loop breakpoints | PreToolUse `ask` decision / P-020 escalation |
| **Subgraphs** | Nested graph workflows | Subagent orchestration |

**Citation**: LangGraph documentation, "State and Checkpoints" (https://langchain-ai.github.io/langgraph/concepts/).

### Tool Use Validation

LangChain/LangGraph validate tool calls before execution:

```python
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

class WriteFileInput(BaseModel):
    """Schema for file write operations with quality gates."""
    file_path: str = Field(description="Path to write the file")
    content: str = Field(description="File content")
    quality_evidence: str | None = Field(
        default=None,
        description="Reference to quality review artifact"
    )

def write_file_with_quality_gate(
    file_path: str,
    content: str,
    quality_evidence: str | None = None
) -> str:
    """Write a file, enforcing quality evidence for implementation files."""
    if file_path.startswith("src/") and quality_evidence is None:
        return (
            "QUALITY GATE FAILURE: Writing implementation files requires "
            "quality_evidence referencing a review artifact. "
            "Complete adversarial review first."
        )
    # Proceed with write...
    return f"File written: {file_path}"

tool = StructuredTool.from_function(
    func=write_file_with_quality_gate,
    name="write_file",
    args_schema=WriteFileInput,
)
```

### Relevance to Jerry

**Directly Applicable Patterns:**

1. **State machine enforcement (LangGraph)**: The most relevant pattern for Jerry. LangGraph's state-based workflow enforcement directly models Jerry's quality workflow: plan -> test -> implement -> review -> commit. Jerry could implement equivalent state tracking in its hook system.

2. **Checkpointing**: LangGraph's automatic state persistence maps to Jerry's orchestration checkpoints and the proposed `.jerry/enforcement/session-state.json`.

3. **Conditional routing**: LangGraph's quality-gate-based routing is the programmatic equivalent of Jerry's hook decisions (approve/block/ask).

4. **Schema-enforced outputs**: Pydantic-based output validation ensures deliverables contain required fields (quality score, citations, review evidence).

5. **Auto-correction parsers**: The `OutputFixingParser` pattern of re-prompting with validation feedback aligns with Jerry's REASK-equivalent in the creator-critic-revision cycle.

**Gaps vs Jerry's Needs:**

- LangGraph requires building the application with LangGraph's graph primitives. Jerry must work within Claude Code's existing hook architecture.
- LangChain's output parsers assume control over the LLM call. Jerry's hooks operate as side-effects on Claude Code's existing processing.
- No direct support for multi-agent adversarial review cycles.

---

## Framework 4: Anthropic Constitutional AI

### Overview

**Constitutional AI (CAI)** is Anthropic's approach to training AI systems that are helpful, harmless, and honest by using a set of explicit principles (a "constitution") for self-evaluation and revision. Unlike the other frameworks surveyed here, CAI operates at the **training level** rather than the **runtime level**, but its principles and self-critique mechanism are directly applicable to runtime enforcement.

- **Paper**: Bai et al., "Constitutional AI: Harmlessness from AI Feedback" (2022, arXiv:2212.08073)
- **Organization**: Anthropic
- **Primary Focus**: Training-time alignment, self-critique
- **License**: Research paper (methodology is publicly documented)

### Architecture

CAI operates through a two-phase training process:

**Phase 1: Supervised Learning from Self-Critique (SL-CAI)**

```
1. Generate initial response to prompt
2. For each constitutional principle:
   a. Ask the model to critique its own response against the principle
   b. Ask the model to revise its response based on the critique
3. Use the final revised response as training data
```

**Phase 2: Reinforcement Learning from AI Feedback (RLHF-CAI)**

```
1. Generate multiple responses to prompt
2. Use a separate model (trained on constitutional principles)
   to rank responses by constitutional compliance
3. Use rankings as reward signal for RL training
```

**Key Architectural Insight**: The self-critique loop in Phase 1 is structurally identical to Jerry's creator-critic-revision cycle. The difference is that CAI performs this at training time, while Jerry performs it at runtime.

### Constitutional Principles

Anthropic defines constitutional principles as natural-language rules that the model evaluates against. Example principles from the original paper:

```
Principle: "Please choose the assistant response that is as harmless
and helpful as possible, without being deceitful."

Principle: "Choose the response that answers the human's question
in a more friendly and amiable manner."

Principle: "Which of these assistant responses is less harmful?
Choose the response that is less racially biased."
```

**Jerry's Constitutional Principles (from JERRY_CONSTITUTION.md):**

Jerry already implements a constitutional approach with principles like:
- P-001: Truth and Accuracy
- P-002: File Persistence
- P-003: No Recursive Subagents
- P-004: Explicit Provenance
- P-020: User Authority
- P-022: No Deception

**Key Insight for Jerry**: Jerry's constitution is more specific and actionable than Anthropic's general principles. This is a strength -- research shows that specific, actionable principles produce higher compliance than abstract ones.

### Enforcement Mechanism: Self-Critique Protocol

The self-critique protocol can be implemented at runtime:

```
Before completing any deliverable, the agent MUST:

1. GENERATE the initial output (Creator phase)

2. CRITIQUE against each quality principle:
   - QE-001: "Does this output follow the creator-critic-revision cycle?"
   - QE-002: "Does this output include a quality score >= 0.92?"
   - QE-003: "Were the appropriate skills invoked?"
   - QE-004: "Are all outputs persisted to the filesystem?"
   - QE-005: "Do all claims have authoritative citations?"

3. REVISE if any principle is violated

4. REPEAT until all principles pass or max iterations reached
```

**Self-Critique Implementation for Jerry:**

```python
# Conceptual implementation for a PostToolUse hook
QUALITY_PRINCIPLES = [
    {
        "id": "QE-001",
        "principle": "Creator-Critic-Revision Cycle",
        "check": "Has this deliverable been through adversarial review?",
        "enforcement": "hard",
    },
    {
        "id": "QE-002",
        "principle": "Quality Score Threshold",
        "check": "Is the quality score documented and >= 0.92?",
        "enforcement": "hard",
    },
    {
        "id": "QE-003",
        "principle": "Skill Invocation",
        "check": "Were /problem-solving, /nasa-se, /orchestration invoked as needed?",
        "enforcement": "medium",
    },
    {
        "id": "QE-004",
        "principle": "Artifact Persistence",
        "check": "Are all outputs persisted to the filesystem?",
        "enforcement": "hard",
    },
    {
        "id": "QE-005",
        "principle": "Citation Provenance",
        "check": "Do all claims have authoritative citations?",
        "enforcement": "medium",
    },
]

def generate_self_critique_prompt(principles: list[dict]) -> str:
    """Generate a self-critique injection for the agent."""
    critique = "<quality-self-critique>\n"
    critique += "Before completing this response, evaluate against:\n\n"
    for p in principles:
        level = "MANDATORY" if p["enforcement"] == "hard" else "RECOMMENDED"
        critique += f"[{p['id']}] [{level}] {p['check']}\n"
    critique += "\nIf any MANDATORY check fails, REVISE before responding.\n"
    critique += "</quality-self-critique>\n"
    return critique
```

**Citation**: Bai et al., "Constitutional AI: Harmlessness from AI Feedback" (2022, Anthropic, arXiv:2212.08073).
**Citation**: Anthropic, "Claude's Character" (https://www.anthropic.com/research/claudes-character) documents how principles shape model behavior.

### Relevance to Jerry

**Directly Applicable Patterns:**

1. **Principle-based self-critique**: Jerry can inject self-critique checklists into the agent's context via UserPromptSubmit hooks, forcing evaluation against quality principles before responding.

2. **Constitutional hierarchy**: The tiered principle system (HARD, MEDIUM, SOFT) maps to Jerry's enforcement tiers (Article V).

3. **Revision loop**: The generate-critique-revise cycle at the core of CAI is structurally identical to Jerry's creator-critic-revision workflow.

4. **Explicit principles over implicit training**: CAI research shows that explicit, written principles produce more reliable behavior than implicit expectations. This validates Jerry's approach of codifying quality rules in `.claude/rules/`.

**Gaps vs Jerry's Needs:**

- CAI operates at training time. Jerry needs runtime enforcement.
- CAI self-critique relies on the model honestly evaluating itself. The model can still "choose" to ignore self-critique, hence the need for programmatic enforcement (hooks).
- CAI does not address multi-step workflow compliance.

---

## Framework 5: Microsoft Semantic Kernel

### Overview

**Microsoft Semantic Kernel** (https://github.com/microsoft/semantic-kernel) is an SDK for integrating LLMs into applications. It provides a **filters and planners** architecture that enables guardrails at multiple levels.

- **GitHub**: https://github.com/microsoft/semantic-kernel
- **License**: MIT
- **Language**: C#, Python, Java
- **Maturity**: Production-ready (v1.x as of 2024-2025)
- **Primary Focus**: Enterprise LLM application development

### Filters (Guardrails Pattern)

Semantic Kernel implements guardrails through **filters** that intercept function calls:

```python
from semantic_kernel.filters import (
    FunctionInvocationContext,
    PromptRenderContext,
)

class QualityEnforcementFilter:
    """Filter that enforces quality prerequisites."""

    async def on_function_invocation(
        self,
        context: FunctionInvocationContext,
        next: Callable,
    ):
        """Intercept function calls for quality gate enforcement."""
        function_name = context.function.name

        # Check quality prerequisites for implementation functions
        if function_name.startswith("implement_"):
            if not self._plan_exists():
                context.result = FunctionResult(
                    value="QUALITY GATE: Plan required before implementation.",
                    function=context.function,
                )
                return  # Block the function call

        # Proceed with the function call
        await next(context)

        # Post-execution: inject quality reminder
        if context.result:
            context.result.metadata["quality_reminder"] = (
                "Remember: Schedule adversarial review before marking complete."
            )

    async def on_prompt_render(
        self,
        context: PromptRenderContext,
        next: Callable,
    ):
        """Inject quality context into prompts."""
        # Prepend quality enforcement context
        quality_context = self._get_quality_enforcement_context()
        context.rendered_prompt = quality_context + context.rendered_prompt
        await next(context)
```

**Filter Types:**

| Filter Type | When | Purpose | Jerry Equivalent |
|-------------|------|---------|-----------------|
| **Prompt Render Filter** | Before prompt sent to LLM | Modify/enhance prompt | UserPromptSubmit hook |
| **Function Invocation Filter** | Before/after function execution | Gate tool usage | PreToolUse/PostToolUse hooks |
| **Auto Function Invocation Filter** | Before/after auto-invoked functions | Control autonomous actions | PreToolUse hook with matcher |

**Citation**: Microsoft Semantic Kernel documentation, "Filters" (https://learn.microsoft.com/en-us/semantic-kernel/concepts/enterprise-readiness/filters).

### Planners and Quality Gates

Semantic Kernel's **planner** system generates execution plans that can include quality gates:

```python
from semantic_kernel.planners import SequentialPlanner

planner = SequentialPlanner(kernel)
plan = await planner.create_plan(
    goal="Implement the work item tracking feature"
)

# The plan includes steps that can be gated
for step in plan.steps:
    # Check quality prerequisites before each step
    if step.requires_quality_gate():
        gate_result = await quality_gate_check(step)
        if not gate_result.passed:
            logger.warning(f"Quality gate failed for step: {step.name}")
            break

    result = await step.invoke(kernel)
```

### Relevance to Jerry

**Directly Applicable Patterns:**

1. **Filter pipeline**: Semantic Kernel's filter architecture (pre-invocation, post-invocation, prompt render) maps precisely to Jerry's hook architecture. The implementation pattern is nearly identical.

2. **Enterprise-grade design**: Semantic Kernel is designed for enterprise applications with strong typing, dependency injection, and testability -- aligned with Jerry's hexagonal architecture.

3. **Planner-as-quality-gate**: Using the planner to decompose tasks and gate each step provides workflow-level enforcement.

**Gaps vs Jerry's Needs:**

- Semantic Kernel is an SDK for building applications, not a standalone guardrail framework. Jerry would need to adapt patterns rather than use the framework directly.
- C# primary language (Python SDK is less mature).

---

## Framework 6: CrewAI

### Overview

**CrewAI** (https://github.com/crewAIInc/crewAI) is a multi-agent orchestration framework that includes built-in guardrails for task execution, agent constraints, and structured output validation.

- **GitHub**: https://github.com/crewAIInc/crewAI
- **License**: MIT
- **Language**: Python
- **Maturity**: Growing adoption (v0.x as of early 2025)
- **Primary Focus**: Multi-agent orchestration with task management

### Task Guardrails

CrewAI provides guardrails at the task level:

```python
from crewai import Task, Agent, Crew
from crewai.guardrails import OutputGuardrail

# Define output validation
def validate_quality_output(output: str) -> tuple[bool, str]:
    """Validate that output meets quality requirements."""
    issues = []

    if "quality_score" not in output.lower():
        issues.append("Missing quality score")
    if "citations" not in output.lower():
        issues.append("Missing citations")
    if "review" not in output.lower():
        issues.append("No evidence of review")

    if issues:
        return False, f"Quality issues: {', '.join(issues)}"
    return True, ""

research_task = Task(
    description="Research enforcement vectors with citations",
    agent=researcher_agent,
    expected_output="Research report with quality score >= 0.92",
    guardrail=OutputGuardrail(
        validation_function=validate_quality_output,
        max_retries=3,
        on_fail="retry",  # or "error", "warn"
    ),
)
```

### Agent Constraints

CrewAI allows defining constraints on agent behavior:

```python
researcher = Agent(
    role="Quality Researcher",
    goal="Produce high-quality research with authoritative citations",
    backstory="You are a meticulous researcher who never makes unsourced claims.",
    allow_delegation=False,  # Cannot delegate to other agents
    max_iter=15,  # Maximum reasoning iterations
    max_rpm=10,  # Rate limiting
    verbose=True,  # Logging for audit trail
)
```

### Structured Output Validation

CrewAI uses Pydantic models for structured output enforcement:

```python
from pydantic import BaseModel, Field

class ResearchOutput(BaseModel):
    """Enforced output schema for research tasks."""
    summary: str = Field(min_length=100)
    findings: list[str] = Field(min_length=3)
    citations: list[str] = Field(min_length=5)
    quality_score: float = Field(ge=0.0, le=1.0)
    methodology: str = Field(min_length=50)

task = Task(
    description="Research LLM guardrail frameworks",
    output_pydantic=ResearchOutput,  # Enforce schema
    agent=researcher,
)
```

**Citation**: CrewAI documentation, "Guardrails" (https://docs.crewai.com/concepts/guardrails).

### Relevance to Jerry

**Directly Applicable Patterns:**

1. **Task-level guardrails with retry**: CrewAI's task guardrail pattern (validate -> retry on failure -> max retries -> error) maps directly to Jerry's creator-critic-revision cycle.

2. **Agent constraints**: Defining what agents can and cannot do aligns with Jerry's role-based agent system (ps-researcher, ps-critic, etc.).

3. **Structured output schemas**: Pydantic-based output validation ensures deliverables contain required quality metadata.

4. **Multi-agent orchestration with guardrails**: CrewAI is the closest framework to Jerry's multi-agent architecture, making its guardrail patterns directly relevant.

**Gaps vs Jerry's Needs:**

- CrewAI manages its own LLM calls. Jerry operates through Claude Code's hook system.
- CrewAI's guardrails are task-scoped, not session-scoped.
- No support for adversarial review patterns (Red Team, Devil's Advocate, etc.).

---

## Framework 7: Meta Llama Guard

### Overview

**Llama Guard** is Meta's safety classification model that evaluates LLM inputs and outputs against a configurable taxonomy of unsafe content categories. Unlike the other frameworks which are libraries/SDKs, Llama Guard is a **fine-tuned language model** purpose-built for content classification.

- **Paper**: Inan et al., "Llama Guard: LLM-based Input-Output Safeguard for Human-AI Conversations" (2023, Meta)
- **Models**: Llama Guard 1, Llama Guard 2, Llama Guard 3 (progressively improved)
- **License**: Llama 2/3 Community License
- **Primary Focus**: Safety classification

### Architecture

Llama Guard operates as a **classifier model** that evaluates text against a taxonomy:

```
Input/Output Text
    |
    v
[Llama Guard Model]
    |
    +-- Classification: "safe" or "unsafe"
    |
    +-- If unsafe: Category identification
    |   (e.g., "S1: Violence", "S2: Sexual Content")
    |
    v
Decision: Allow / Block
```

**Taxonomy-Based Classification:**

```
TASK: Evaluate the following text against the safety taxonomy.

TAXONOMY:
S1: Violence and Threats
S2: Sexual Content
S3: Criminal Planning
S4: Hate Speech
S5: Self-Harm
S6: Custom Category (user-defined)

TEXT: [input or output text]

CLASSIFICATION: safe / unsafe
CATEGORY: [if unsafe, list violated categories]
```

**Key Insight**: Llama Guard's taxonomy-driven approach can be adapted for **quality compliance classification** rather than safety classification:

```
JERRY QUALITY TAXONOMY:
Q1: Missing Quality Score (deliverable lacks documented quality score)
Q2: Missing Citations (claims without authoritative sources)
Q3: Missing Review Evidence (no adversarial review artifacts)
Q4: Missing Tests (implementation without corresponding tests)
Q5: Workflow Violation (skipped planning or review phases)
Q6: Skill Non-Invocation (required skill not invoked)
```

**Citation**: Inan et al., "Llama Guard: LLM-based Input-Output Safeguard for Human-AI Conversations" (2023, arXiv:2312.06674).

### Relevance to Jerry

**Directly Applicable Patterns:**

1. **Taxonomy-driven classification**: Define quality violation categories and classify agent outputs against them. This could be implemented as a PostToolUse check that classifies written content.

2. **Model-based evaluation**: Using an LLM as a quality evaluator (the judge pattern) aligns with Jerry's ps-critic agent role. The difference is that Llama Guard uses a specialized fine-tuned model, while Jerry uses the same model with different prompting.

3. **Configurable categories**: The ability to define custom categories means the taxonomy can evolve with Jerry's quality requirements.

**Gaps vs Jerry's Needs:**

- Llama Guard requires running a separate model for classification. This adds latency and infrastructure complexity.
- Designed for content safety, not process compliance.
- Binary (safe/unsafe) classification lacks the nuance of quality scoring (0.0-1.0).

---

## Framework 8: Rebuff

### Overview

**Rebuff** (https://github.com/protectai/rebuff) is a framework specifically designed for detecting and preventing **prompt injection attacks**. While narrower in scope than the other frameworks, its multi-layer defense architecture provides important patterns for Jerry.

- **GitHub**: https://github.com/protectai/rebuff
- **License**: Apache 2.0
- **Language**: Python
- **Maturity**: Early stage (v0.x)
- **Primary Focus**: Prompt injection detection and prevention

### Multi-Layer Defense Architecture

Rebuff implements a **defense-in-depth** approach with four detection layers:

```
User Input
    |
    v
[Layer 1: Heuristic Analysis]
    |  - Pattern matching for known injection patterns
    |  - Regular expressions, keyword detection
    |  - Fast, deterministic, low latency
    |
    v
[Layer 2: LLM-Based Detection]
    |  - Ask an LLM: "Is this input a prompt injection attempt?"
    |  - Semantic understanding of intent
    |  - Higher accuracy, higher latency
    |
    v
[Layer 3: Vector Database Similarity]
    |  - Compare input embedding against known injection database
    |  - Catches novel variations of known attacks
    |  - Requires embedding model + vector store
    |
    v
[Layer 4: Canary Token Detection]
    |  - Insert unique tokens in system prompt
    |  - Check if output contains the canary token
    |  - Detects output-side injection leakage
    |
    v
Combined Score -> Allow / Block Decision
```

**Key Architectural Insight**: The multi-layer approach where each layer compensates for the weaknesses of the others is directly applicable to Jerry's defense-in-depth enforcement strategy. Each enforcement vector (hooks, rules, pre-commit, CI) is a "layer" that catches what the previous layer missed.

**Citation**: Rebuff documentation (https://github.com/protectai/rebuff/blob/main/README.md).

### Relevance to Jerry

**Directly Applicable Patterns:**

1. **Multi-layer defense-in-depth**: The principle that no single defense is sufficient is validated by Rebuff's architecture. Jerry's enforcement should combine: rule-based enforcement (heuristic) + hook-based enforcement (programmatic) + pre-commit enforcement (deterministic) + CI enforcement (comprehensive).

2. **Heuristic + LLM-based detection**: Combining fast heuristic checks (e.g., keyword detection for task classification) with deeper LLM-based analysis (e.g., self-critique against principles) provides both speed and accuracy.

3. **Canary token pattern**: Jerry could inject "canary" instructions in enforcement context and check whether the agent acknowledges them, detecting when enforcement context is being ignored.

---

## Framework 9: Other Notable Frameworks

### Microsoft Guidance

**Guidance** (https://github.com/guidance-ai/guidance) provides a templating language for constraining LLM generation:

```python
import guidance

@guidance
def quality_deliverable(lm):
    lm += "Research findings:\n"
    lm += guidance.gen("findings", max_tokens=2000)
    lm += "\n\nQuality score: "
    lm += guidance.gen("score", regex=r"0\.\d{2}")  # Force decimal format
    lm += "\n\nCitations:\n"
    lm += guidance.gen("citations", stop="\n\n")
    return lm
```

**Relevance**: Token-level generation constraints ensure structural compliance. Not directly applicable to Jerry (cannot control Claude Code's generation) but the concept of schema-constrained generation is relevant.

### Outlines (dottxt)

**Outlines** (https://github.com/dottxt-ai/outlines) provides structured generation using finite state machines and regular expressions to constrain LLM output:

```python
import outlines

model = outlines.models.transformers("mistralai/Mistral-7B-v0.1")
generator = outlines.generate.json(model, QualityDeliverable)
result = generator("Research enforcement vectors...")
```

**Relevance**: Schema-enforced generation at the token level. Relevant concept for ensuring deliverable structure compliance.

### Instructor

**Instructor** (https://github.com/jxnl/instructor) patches LLM clients to return structured Pydantic objects with automatic retry:

```python
import instructor
from openai import OpenAI

client = instructor.from_openai(OpenAI())

deliverable = client.chat.completions.create(
    model="gpt-4",
    response_model=QualityDeliverable,
    max_retries=3,
    messages=[
        {"role": "user", "content": "Research enforcement vectors"}
    ],
)
# deliverable is a validated QualityDeliverable Pydantic object
```

**Relevance**: The `max_retries` + `response_model` pattern is another implementation of the validate-retry loop. Instructor's approach of patching the client library is architecturally similar to Jerry's hook system (intercept at the boundary).

### LMQL

**LMQL** (https://lmql.ai/) is a query language for LLMs that supports inline constraints:

```python
@lmql.query
def research_query():
    '''lmql
    "Research enforcement vectors."
    "[FINDINGS]" where len(FINDINGS) > 500
    "Quality score: [SCORE]" where SCORE in ["0.92", "0.93", "0.94", "0.95", "0.96", "0.97", "0.98", "0.99", "1.00"]
    "Citations: [CITATIONS]" where len(CITATIONS) > 100
    '''
```

**Relevance**: Inline constraints on generated content. The concept of embedding quality constraints directly into the generation request is relevant to Jerry's prompt engineering patterns.

---

## Comparative Analysis

### L2: Multi-Dimensional Comparison Matrix

| Framework | Enforcement Approach | Enforcement Level | Enforcement Mode | Open Source | License | Maturity | Jerry Applicability |
|-----------|---------------------|-------------------|-----------------|------------|---------|----------|-------------------|
| **Guardrails AI** | Rules-based (validators) | Output | Block, Retry, Fix, Filter, Log | Yes | Apache 2.0 | Production | **HIGH** -- Validator composition pattern |
| **NeMo Guardrails** | Hybrid (Colang DSL + LLM) | Input, Dialog, Output | Block, Modify, Allow | Yes | Apache 2.0 | Production | **HIGH** -- Three-rail architecture, dialog enforcement |
| **LangChain/LangGraph** | Rules-based + State machine | Output, Workflow | Block, Retry, Route | Yes | MIT | Production | **CRITICAL** -- State machine enforcement |
| **Constitutional AI** | LLM-based (self-critique) | Output (training & runtime) | Revise, Score | Research | N/A | Research | **HIGH** -- Self-critique protocol |
| **Semantic Kernel** | Rules-based (filters) | Input, Output, Function | Block, Modify, Log | Yes | MIT | Production | **MEDIUM** -- Filter pipeline pattern |
| **CrewAI** | Rules-based (task guardrails) | Task output | Retry, Error, Warn | Yes | MIT | Growing | **HIGH** -- Task-level guardrails, multi-agent |
| **Llama Guard** | ML-based (classifier) | Input, Output | Block, Allow | Yes | Llama License | Production | **LOW** -- Safety focus, not process compliance |
| **Rebuff** | Hybrid (heuristic + ML) | Input | Block, Allow | Yes | Apache 2.0 | Early | **MEDIUM** -- Multi-layer defense pattern |
| **Guidance/Outlines** | Rules-based (generation constraints) | Generation | Constrain | Yes | MIT/Apache | Production | **LOW** -- Cannot control Claude Code generation |
| **Instructor** | Rules-based (schema validation) | Output | Retry, Error | Yes | MIT | Production | **MEDIUM** -- Schema validation + retry pattern |

### Enforcement Level Coverage

| Level | Frameworks | Jerry Implementation |
|-------|-----------|---------------------|
| **Input** | NeMo (input rails), Rebuff, Semantic Kernel (prompt filter) | UserPromptSubmit hook |
| **Output** | Guardrails AI, NeMo (output rails), LangChain (parsers), Llama Guard, Instructor | PostToolUse hook |
| **Dialog/Workflow** | NeMo (dialog rails), LangGraph (state machine), CrewAI (task guardrails) | Orchestration + stateful hooks |
| **Generation** | Guidance, Outlines, LMQL | Not directly applicable (cannot control Claude generation) |
| **Training** | Constitutional AI | Not applicable (Jerry does not train models) |

### Enforcement Mode Coverage

| Mode | Description | Frameworks | Jerry Implementation |
|------|-------------|-----------|---------------------|
| **Block** | Prevent action entirely | All except Constitutional AI | PreToolUse `block` decision |
| **Retry/Reask** | Re-prompt with feedback | Guardrails AI, LangChain, CrewAI, Instructor | Creator-Critic-Revision loop |
| **Fix/Correct** | Programmatically fix output | Guardrails AI | PostToolUse correction injection |
| **Modify** | Alter input/output | NeMo, Semantic Kernel | UserPromptSubmit context injection |
| **Warn/Log** | Record violation, allow through | All | PostToolUse audit logging |
| **Route** | Redirect to different workflow | LangGraph | Hook-based state machine routing |
| **Score** | Evaluate without blocking | Constitutional AI, Llama Guard | Quality score calculation |

---

## Architectural Patterns for Jerry

### Pattern 1: Validator Composition (from Guardrails AI)

**Description**: Define discrete, reusable quality validators that can be composed into validation chains.

**Jerry Implementation Concept:**

```python
# src/quality/validators/base.py
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

class ValidationResult(Enum):
    PASS = "pass"
    FAIL = "fail"
    WARN = "warn"

@dataclass(frozen=True)
class ValidatorOutput:
    result: ValidationResult
    message: str
    validator_id: str

class QualityValidator(ABC):
    """Base class for composable quality validators."""

    @abstractmethod
    def validate(self, context: dict) -> ValidatorOutput: ...

# src/quality/validators/artifact_presence.py
class ArtifactPresenceValidator(QualityValidator):
    """Check that required artifacts exist."""

    def __init__(self, required_artifacts: list[str]):
        self._required = required_artifacts

    def validate(self, context: dict) -> ValidatorOutput:
        missing = [a for a in self._required if not Path(a).exists()]
        if missing:
            return ValidatorOutput(
                result=ValidationResult.FAIL,
                message=f"Missing artifacts: {missing}",
                validator_id="artifact_presence",
            )
        return ValidatorOutput(
            result=ValidationResult.PASS,
            message="All required artifacts present",
            validator_id="artifact_presence",
        )

# src/quality/validators/chain.py
class ValidatorChain:
    """Compose multiple validators into a chain."""

    def __init__(self, validators: list[QualityValidator]):
        self._validators = validators

    def validate_all(self, context: dict) -> list[ValidatorOutput]:
        return [v.validate(context) for v in self._validators]

    def any_failures(self, context: dict) -> bool:
        return any(
            r.result == ValidationResult.FAIL
            for r in self.validate_all(context)
        )
```

### Pattern 2: Programmable Rails (from NeMo Guardrails)

**Description**: Define enforcement flows in a declarative format that is readable and maintainable.

**Jerry Implementation Concept**: Extend `.claude/rules/` with structured enforcement declarations:

```yaml
# .jerry/enforcement/quality-rails.yaml
rails:
  input:
    - name: classify_task
      description: "Classify user prompt into task type"
      action: classify
      categories:
        - implementation
        - research
        - design
        - review
        - testing

    - name: check_prerequisites
      description: "Verify prerequisites for task type"
      conditions:
        implementation:
          required_artifacts: ["PLAN.md", "tests/"]
          required_skills: ["/orchestration"]
        research:
          required_skills: ["/problem-solving"]
          required_sections: ["methodology", "citations"]

  output:
    - name: check_quality_score
      description: "Verify quality score in deliverable"
      threshold: 0.92
      enforcement: hard

    - name: check_citations
      description: "Verify citations present"
      min_citations: 3
      enforcement: medium

  dialog:
    - name: enforce_creator_critic_cycle
      description: "Track and enforce creator-critic-revision"
      min_iterations: 3
      max_iterations: 5
      enforcement: hard
```

### Pattern 3: State Machine Enforcement (from LangGraph)

**Description**: Define valid workflow states and transitions, enforce them via hooks.

**Jerry Implementation Concept:**

```python
# .jerry/enforcement/workflow_state.py
from enum import Enum

class WorkflowPhase(Enum):
    PLANNING = "planning"
    TESTING = "testing"
    IMPLEMENTATION = "implementation"
    REVIEW = "review"
    REVISION = "revision"
    COMPLETE = "complete"

VALID_TRANSITIONS = {
    WorkflowPhase.PLANNING: {WorkflowPhase.TESTING},
    WorkflowPhase.TESTING: {WorkflowPhase.IMPLEMENTATION},
    WorkflowPhase.IMPLEMENTATION: {WorkflowPhase.REVIEW},
    WorkflowPhase.REVIEW: {WorkflowPhase.REVISION, WorkflowPhase.COMPLETE},
    WorkflowPhase.REVISION: {WorkflowPhase.REVIEW},
    WorkflowPhase.COMPLETE: set(),
}

def enforce_transition(current: WorkflowPhase, target: WorkflowPhase) -> bool:
    """Check if workflow transition is valid."""
    return target in VALID_TRANSITIONS.get(current, set())
```

### Pattern 4: Self-Critique Injection (from Constitutional AI)

**Description**: Inject self-evaluation checklists into agent context, forcing reflection before action.

**Jerry Implementation**: Via UserPromptSubmit hook (already proposed in TASK-001 research). The self-critique checklist is injected as `additionalContext` on every prompt.

### Pattern 5: Multi-Layer Defense (from Rebuff + NeMo + Guardrails AI)

**Description**: Combine multiple enforcement mechanisms so each layer catches what the previous layer missed.

**Jerry's Defense Layers:**

```
Layer 1: Rules (.claude/rules/)
    Mechanism: Declarative instructions in context
    Catches: Unintentional deviations
    Weakness: Can be "forgotten" in long contexts

Layer 2: Session Context (UserPromptSubmit hook)
    Mechanism: Injected enforcement on every prompt
    Catches: Context-rot-induced compliance drift
    Weakness: Agent may deprioritize injected context

Layer 3: Tool Gating (PreToolUse hook)
    Mechanism: Block non-compliant tool usage
    Catches: Premature implementation without prerequisites
    Weakness: Cannot enforce thought process

Layer 4: Output Validation (PostToolUse hook)
    Mechanism: Validate outputs and inject reminders
    Catches: Quality violations in produced artifacts
    Weakness: Reactive (action already taken)

Layer 5: Commit Gating (pre-commit hooks)
    Mechanism: Block non-compliant commits
    Catches: Anything that slipped through layers 1-4
    Weakness: Late in the process (effort already spent)

Layer 6: CI/CD Gating (GitHub Actions)
    Mechanism: Block non-compliant merges
    Catches: Cross-session quality violations
    Weakness: Latest possible enforcement point
```

### Pattern 6: Schema-Enforced Deliverables (from LangChain + Instructor + CrewAI)

**Description**: Define Pydantic schemas for deliverable metadata that enforce quality fields.

**Jerry Implementation Concept:**

```python
from pydantic import BaseModel, Field, field_validator

class DeliverableMetadata(BaseModel):
    """Required metadata for any Jerry deliverable."""

    document_id: str = Field(description="Unique document identifier")
    author: str = Field(description="Agent or human author")
    quality_score: float = Field(ge=0.0, le=1.0)
    review_iterations: int = Field(ge=0)
    citations: list[str] = Field(min_length=0)
    skills_invoked: list[str] = Field(default_factory=list)
    artifacts_produced: list[str] = Field(min_length=1)

    @field_validator("quality_score")
    @classmethod
    def meets_threshold(cls, v: float) -> float:
        if v < 0.92:
            raise ValueError(f"Quality score {v} below 0.92 threshold")
        return v
```

### Integration Architecture for Jerry

Based on the patterns analyzed, the recommended integration architecture is:

```
                    ┌─────────────────────────┐
                    │   Quality Rails Config    │
                    │ (.jerry/enforcement/*.yaml)│
                    └────────────┬──────────────┘
                                 │
                                 │ Loaded by
                                 ▼
┌──────────────────────────────────────────────────────────────┐
│                    ENFORCEMENT ENGINE                         │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Validator    │  │  State       │  │  Self-Critique│      │
│  │  Chain        │  │  Machine     │  │  Injector    │      │
│  │  (Pattern 1)  │  │  (Pattern 3) │  │  (Pattern 4) │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                  │                  │               │
│         └──────────────────┼──────────────────┘               │
│                            │                                  │
│                            ▼                                  │
│                  ┌──────────────────┐                         │
│                  │  Enforcement      │                         │
│                  │  Decision Engine  │                         │
│                  │  (approve/block/  │                         │
│                  │   ask/warn/log)   │                         │
│                  └──────────────────┘                         │
└──────────────────────────┬───────────────────────────────────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │SessionStrt│ │UserPrompt│ │PreToolUse│
        │  Hook     │ │Submit Hk │ │  Hook    │
        └──────────┘ └──────────┘ └──────────┘
              │            │            │
              ▼            ▼            ▼
        ┌──────────────────────────────────────┐
        │         Claude Code Runtime           │
        └──────────────────────────────────────┘
              │
              ▼
        ┌──────────┐ ┌──────────┐
        │PostToolUs│ │  Stop    │
        │  Hook    │ │  Hook    │
        └──────────┘ └──────────┘
```

---

## Sources and References

### Framework Documentation (Primary Sources)

| # | Source | URL | Used For |
|---|--------|-----|----------|
| 1 | Guardrails AI Documentation | https://docs.guardrailsai.com/ | Validator architecture, Guard composition, RAIL specs |
| 2 | Guardrails AI GitHub | https://github.com/guardrails-ai/guardrails | Implementation patterns, validator interface |
| 3 | Guardrails Hub | https://hub.guardrailsai.com/ | Community validators, validator taxonomy |
| 4 | NVIDIA NeMo Guardrails Documentation | https://docs.nvidia.com/nemo/guardrails/ | Colang language, rail types, architecture |
| 5 | NeMo Guardrails GitHub | https://github.com/NVIDIA/NeMo-Guardrails | Implementation, configuration, examples |
| 6 | LangChain Documentation | https://python.langchain.com/docs/ | Output parsers, tool validation |
| 7 | LangGraph Documentation | https://langchain-ai.github.io/langgraph/ | State machines, checkpoints, conditional routing |
| 8 | Microsoft Semantic Kernel Documentation | https://learn.microsoft.com/en-us/semantic-kernel/ | Filters, planners, enterprise patterns |
| 9 | Semantic Kernel GitHub | https://github.com/microsoft/semantic-kernel | Implementation patterns |
| 10 | CrewAI Documentation | https://docs.crewai.com/ | Task guardrails, agent constraints |
| 11 | CrewAI GitHub | https://github.com/crewAIInc/crewAI | Multi-agent orchestration patterns |
| 12 | Rebuff GitHub | https://github.com/protectai/rebuff | Multi-layer defense architecture |
| 13 | Guidance GitHub | https://github.com/guidance-ai/guidance | Constrained generation patterns |
| 14 | Outlines GitHub | https://github.com/dottxt-ai/outlines | Structured generation via FSM |
| 15 | Instructor GitHub | https://github.com/jxnl/instructor | Schema validation + retry patterns |
| 16 | LMQL Website | https://lmql.ai/ | Query language constraints |

### Research Papers

| # | Citation | Key Finding |
|---|----------|-------------|
| 17 | Bai et al., "Constitutional AI: Harmlessness from AI Feedback" (2022, Anthropic, arXiv:2212.08073) | Self-critique against explicit principles is more reliable than implicit procedure-following |
| 18 | Inan et al., "Llama Guard: LLM-based Input-Output Safeguard for Human-AI Conversations" (2023, Meta, arXiv:2312.06674) | Taxonomy-driven classification for LLM safety; configurable categories |
| 19 | Wu et al., "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation" (2023, Microsoft Research) | Multi-agent governance patterns, termination conditions |
| 20 | Rebedea et al., "NeMo Guardrails: A Toolkit for Controllable and Safe LLM Applications with Programmable Rails" (2023, NVIDIA, arXiv:2310.10501) | Programmable rails architecture, Colang design, three-rail system |
| 21 | Liu et al., "Lost in the Middle: How Language Models Use Long Contexts" (2023, arXiv:2307.03172) | LLMs perform worse on information in the middle of long contexts |
| 22 | Wei et al., "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models" (2022, NeurIPS) | Explicit reasoning steps improve task accuracy |

### Industry Standards (Cross-Referenced)

| # | Standard | Relevance |
|---|----------|-----------|
| 23 | IETF RFC 2119 "Key words for Requirement Levels" | MUST/SHOULD/MAY hierarchy used in enforcement tiers |
| 24 | OWASP Top 10 for LLM Applications (2023) | LLM-specific security concerns informing guardrail design |

### Jerry Internal References

| # | Source | Path | Used For |
|---|--------|------|----------|
| 25 | Enforcement Vectors Research (TASK-001) | `FEAT-005/research-enforcement-vectors.md` | Cross-reference with Claude Code hooks research |
| 26 | 15 Adversarial Strategies (FEAT-004) | `FEAT-004/research-15-adversarial-strategies.md` | Adversarial review patterns used in enforcement |
| 27 | Jerry Constitution | `docs/governance/JERRY_CONSTITUTION.md` | Constitutional principles, enforcement tiers |
| 28 | Orchestration Plan (FEAT-005) | `FEAT-005/ORCHESTRATION_PLAN.md` | Workflow context for this research |
| 29 | EN-401 Enabler | `EN-401-deep-research-enforcement-vectors.md` | Task definition and scope |
| 30 | FEAT-005 Feature | `FEAT-005-enforcement-mechanisms.md` | Parent feature acceptance criteria |

---

## Disclaimer

This research was generated by the ps-researcher agent (v2.2.0) operating within the Jerry Framework. The following limitations apply:

1. **Web access was unavailable**: WebSearch, WebFetch, and Context7 query-docs tools were denied during this research session. All information is sourced from training data (cutoff: May 2025). Framework APIs, version numbers, and specific features should be verified against current documentation.

2. **Rapidly evolving landscape**: The LLM guardrail ecosystem changes rapidly. New frameworks may have emerged, and existing frameworks may have significantly updated their APIs since May 2025. Guardrails AI, NeMo Guardrails, and LangGraph in particular were undergoing active development at the training cutoff.

3. **Code examples are conceptual**: Code snippets are illustrative examples based on documented APIs. They are not production-ready and should be validated against current framework documentation before use.

4. **Confidence levels vary**: Framework documentation based on well-maintained OSS projects (Guardrails AI, LangChain) carries higher confidence. Less mature or specialized frameworks (Rebuff, LMQL) carry lower confidence.

5. **Jerry applicability assessments are recommendations**: The applicability ratings are based on architectural analysis and pattern matching. Actual implementation feasibility depends on Claude Code's current hook API, performance constraints, and user experience considerations.

6. **Quality review required**: This research has NOT been through the creator-critic-revision cycle. Per EPIC-002's requirements, this document should undergo adversarial review (TASK-008 in EN-401) before acting on its findings.

---

*Document Version: 1.0.0*
*Classification: Research*
*PS-ID: EN-401*
*Entry-ID: TASK-002*
*Author: ps-researcher (Claude, Opus 4.6)*
*Created: 2026-02-12*
*Constitutional Compliance: P-001 (Truth), P-002 (Persistence), P-004 (Provenance), P-022 (No Deception)*
