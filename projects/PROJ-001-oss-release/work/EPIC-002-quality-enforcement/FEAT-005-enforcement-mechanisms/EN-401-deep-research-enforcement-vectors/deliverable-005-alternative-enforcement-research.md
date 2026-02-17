# Research: Alternative & Emerging Enforcement Approaches for LLM Agent Systems

<!--
DOCUMENT-ID: FEAT-005:EN-401-TASK-005-RESEARCH
AUTHOR: nse-explorer agent (v2.2.0)
DATE: 2026-02-13
STATUS: Complete (pending adversarial quality review)
PARENT: EN-401 (Deep Research: Enforcement Vectors & Best Practices)
FEATURE: FEAT-005 (Quality Framework Enforcement Mechanisms)
EPIC: EPIC-002 (Quality Framework Enforcement)
PROJECT: PROJ-001-oss-release
PS-ID: EN-401
ENTRY-ID: TASK-005
NASA-SE-PERSPECTIVE: NPR 7123.1D - IV&V, Mission Assurance, Configuration Management
-->

> **Version:** 1.0.0
> **Agent:** nse-explorer (v2.2.0)
> **Confidence:** MEDIUM-HIGH for MCP-based enforcement and AST-based analysis (well-documented OSS projects in training data); MEDIUM for cross-platform enforcement (rapidly evolving landscape); MEDIUM for novel research approaches (emerging field, limited peer review); HIGH for NASA/safety-critical analogies (established standards)
> **Research Limitation:** WebSearch, WebFetch, and Context7 query-docs tools were unavailable during this research session. All content is sourced from the agent's training knowledge (cutoff May 2025), MCP Python SDK library resolution (Context7), and direct analysis of the Jerry codebase. Post-May-2025 developments should be verified before implementation decisions.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Landscape overview of alternative enforcement approaches |
| [L1: Detailed Catalog](#l1-detailed-catalog-of-alternative-enforcement-approaches) | Each approach with mechanism, novelty, and applicability |
| [L2: Architectural Recommendations](#l2-architectural-recommendations-for-jerry) | Which alternatives Jerry should pursue |
| [Methodology](#methodology) | Research approach, sources, confidence |
| [Approach 1: MCP-Based Enforcement](#approach-1-mcp-based-enforcement) | MCP servers as enforcement middleware |
| [Approach 2: AST-Based Code Analysis Guardrails](#approach-2-ast-based-code-analysis-guardrails) | Static analysis of LLM-generated code |
| [Approach 3: Runtime Verification](#approach-3-runtime-verification-approaches) | Real-time agent behavior monitoring |
| [Approach 4: Formal Methods for LLM Outputs](#approach-4-formal-methods-for-llm-outputs) | Formal specification and verification |
| [Approach 5: Cross-Platform Enforcement Patterns](#approach-5-cross-platform-enforcement-patterns) | OpenAI, Google, Amazon patterns |
| [Approach 6: Novel Enforcement Research (2024-2026)](#approach-6-novel-enforcement-research-2024-2026) | Multi-agent governance, embedding-based compliance |
| [Approach 7: Physical Systems Analogies (NASA SE)](#approach-7-physical-systems-analogies-nasa-se) | IV&V, mission assurance, NASA-STD-8739.8 |
| [Comparative Analysis](#comparative-analysis) | Cross-approach comparison matrix |
| [Sources and References](#sources-and-references) | Full bibliography |
| [Disclaimer](#disclaimer) | Research limitations |

---

## L0: Executive Summary

### The Alternative Enforcement Landscape

Beyond the standard Claude Code enforcement vectors already researched (hooks, rules, prompt engineering, session context, pre-commit gates), there exists a rich landscape of **emerging and alternative enforcement approaches** drawn from multiple domains: protocol-level middleware (MCP), static analysis (AST), runtime verification, formal methods, cross-platform patterns, novel AI governance research, and safety-critical engineering standards.

This research identifies **7 distinct alternative enforcement families** containing **18 specific mechanisms** applicable to Jerry's quality framework enforcement goals.

### Critical Finding

**The most impactful alternative enforcement approach for Jerry is MCP-based enforcement middleware.** The Model Context Protocol provides a standards-based mechanism for tool wrapping, compliance checking, audit logging, and dynamic rule injection that complements (and in some cases surpasses) Claude Code's native hook system. Jerry can implement MCP enforcement servers that intercept and validate tool usage, provide compliance-aware resources, and inject enforcement context through MCP prompts -- all through a standardized, portable protocol.

### Top 5 Alternative Approaches (Ranked by Jerry Applicability)

| Rank | Approach | Novelty | Feasibility for Claude Code | Expected Impact |
|------|----------|---------|---------------------------|-----------------|
| 1 | **MCP-Based Enforcement Middleware** | HIGH | HIGH (Claude Code natively supports MCP) | CRITICAL -- portable, standards-based enforcement |
| 2 | **AST-Based Code Analysis in PreToolUse** | MEDIUM | HIGH (Jerry already uses AST in arch tests) | HIGH -- structural code validation before write |
| 3 | **Cross-Platform Portable Patterns** | MEDIUM | HIGH (design patterns, not platform-specific) | HIGH -- framework portability |
| 4 | **NASA IV&V Patterns for Agent Systems** | HIGH | MEDIUM (requires cultural adaptation) | HIGH -- proven rigor from safety-critical systems |
| 5 | **Runtime State Machine Enforcement** | MEDIUM | MEDIUM (requires state tracking infrastructure) | MEDIUM-HIGH -- workflow compliance guarantee |

### Key Insight from NASA SE Perspective

The most robust enforcement systems in safety-critical engineering share three properties that LLM agent enforcement currently lacks:

1. **Independence**: The verification entity is organizationally and technically independent from the development entity. In Jerry, the agent that creates output currently also reviews it -- there is no truly independent verification.

2. **Completeness**: Every requirement has a mapped verification method, and every verification method traces back to a requirement. Jerry has acceptance criteria but no formal Verification Cross-Reference Matrix (VCRM).

3. **Audit Trail**: Every action, decision, and artifact is timestamped, attributed, and immutable. Jerry persists artifacts (P-002) but does not maintain a comprehensive audit trail.

These gaps represent the highest-leverage improvement opportunities for Jerry's enforcement architecture.

---

## L1: Detailed Catalog of Alternative Enforcement Approaches

### Catalog Summary

| # | Approach | Origin | Mechanism | Novelty (1-5) | Claude Code Applicability |
|---|----------|--------|-----------|---------------|--------------------------|
| 1 | MCP Enforcement Server | Model Context Protocol | Tool wrapping, resource injection | 5 | DIRECT -- Claude Code supports MCP natively |
| 2 | MCP Audit Logger | Model Context Protocol | Transparent logging via MCP server | 4 | DIRECT -- MCP server captures all tool calls |
| 3 | MCP Dynamic Rule Provider | Model Context Protocol | MCP resources serve rules contextually | 4 | DIRECT -- MCP resources inject into context |
| 4 | AST Validation in PreToolUse | Static analysis | Parse code AST before writing to disk | 3 | HIGH -- Jerry already has AST infrastructure |
| 5 | Tree-sitter Multi-Language Guards | Static analysis | Universal parser for code validation | 3 | MEDIUM -- requires tree-sitter dependency |
| 6 | Import Graph Enforcement | Static analysis | Validate architectural boundaries | 3 | HIGH -- Jerry already does this in tests |
| 7 | Runtime State Machine | Formal methods | Finite automaton enforcing workflow | 3 | MEDIUM -- requires state tracking |
| 8 | Temporal Logic Specifications | Formal methods | LTL/CTL for workflow compliance | 2 | LOW -- high complexity, academic maturity |
| 9 | Contract-Based Agent Design | Formal methods | Pre/postconditions on agent actions | 3 | MEDIUM -- fits with hooks architecture |
| 10 | Property-Based Testing of LLM Outputs | Formal methods | Hypothesis-style testing | 3 | HIGH -- integrates with pytest |
| 11 | OpenAI Assistants Enforcement | Cross-platform | Function calling constraints, code interpreter sandbox | 2 | LOW -- platform-specific |
| 12 | Amazon Bedrock Guardrails | Cross-platform | Content filtering, denied topics, word filters | 3 | LOW -- platform-specific, content-focused |
| 13 | Google Gemini Safety Settings | Cross-platform | Harm category thresholds | 2 | LOW -- platform-specific, safety-focused |
| 14 | Multi-Agent Governance | Novel research | Agents monitoring/correcting each other | 4 | MEDIUM -- Jerry has multi-agent architecture |
| 15 | Embedding-Based Compliance | Novel research | Semantic similarity for rule matching | 4 | LOW -- requires embedding infrastructure |
| 16 | Tool-Use Monitoring & Intervention | Novel research | Statistical anomaly detection on tool patterns | 3 | MEDIUM -- requires baseline data |
| 17 | NASA IV&V for AI Agents | Safety-critical | Independent verification entity | 5 | HIGH -- directly applicable pattern |
| 18 | Configuration Management Enforcement | Safety-critical | Baseline management, change control | 3 | HIGH -- maps to git-based workflows |

---

## Methodology

### Research Approach

This research employed a **multi-domain exploration methodology** aligned with NASA NPR 7123.1D Section 6.3 (Technical Assessment):

1. **Domain Survey**: Systematically surveyed enforcement approaches across six domains: protocol middleware (MCP), static analysis (AST/tree-sitter), formal methods, cross-platform AI, novel AI research, and safety-critical engineering.

2. **Codebase Grounding**: Each approach was evaluated against Jerry's existing codebase capabilities -- particularly the AST-based architecture tests, the pattern library validation system, and the hook infrastructure.

3. **Applicability Assessment**: Each approach was scored on (a) novelty over existing vectors, (b) technical feasibility within Claude Code, (c) implementation effort, (d) expected enforcement effectiveness, and (e) portability across platforms.

4. **NASA SE Lens**: Applied NPR 7123.1D IV&V principles, NASA-STD-8739.8 software quality assurance, and configuration management concepts to assess enforcement rigor.

### Source Evaluation

| Source Type | Confidence Level | Justification |
|-------------|-----------------|---------------|
| MCP SDK documentation (Context7 library resolution) | **HIGH** | Official SDK, high reputation score (85.5), 417 code snippets |
| Jerry codebase (direct analysis) | **HIGH** | First-hand examination of AST tests, hooks, patterns |
| Cross-platform API documentation (training data) | **MEDIUM** | Based on pre-May 2025 documentation; APIs evolve rapidly |
| NASA/safety-critical standards | **HIGH** | Established, audited, decades of operational validation |
| Novel AI research (training data) | **MEDIUM** | Emerging field, limited peer review, rapidly evolving |
| Formal methods literature | **HIGH** | Established computer science foundations |

### Confidence Disclosure

**IMPORTANT**: WebSearch, WebFetch, and Context7 query-docs tools were unavailable. The MCP Python SDK library was resolved via Context7 (library ID: `/modelcontextprotocol/python-sdk`, benchmark score: 85.5) but documentation content could not be retrieved. All MCP implementation details are based on training data knowledge of the MCP specification and SDK architecture. Cross-platform enforcement details (OpenAI, Google, Amazon) reflect pre-May 2025 API states and should be verified against current documentation.

---

## Approach 1: MCP-Based Enforcement

### 1.1 Overview

The **Model Context Protocol (MCP)** is an open standard (published by Anthropic) that defines a protocol for LLM applications to communicate with external tools, resources, and prompts through a standardized JSON-RPC interface. Claude Code natively supports MCP servers, making MCP-based enforcement directly applicable to Jerry.

**Key Insight**: MCP provides a **protocol-level** enforcement vector that operates at a different abstraction layer than hooks. While hooks intercept Claude Code's internal tool lifecycle, MCP servers provide **external tool definitions** that Claude interacts with through the MCP protocol. This creates an opportunity for enforcement middleware that wraps, validates, and audits tool usage through the protocol layer.

### 1.2 MCP Enforcement Server Architecture

An MCP enforcement server can implement three enforcement primitives:

#### 1.2.1 Tool Wrapping for Compliance Checking

The MCP server exposes "wrapped" versions of standard tools that include compliance validation:

```python
# Conceptual MCP enforcement server
from mcp.server import Server
from mcp.types import Tool, TextContent

server = Server("jerry-enforcement")

@server.tool()
async def write_file_with_quality_gate(
    file_path: str,
    content: str,
    quality_evidence: str | None = None,
) -> list[TextContent]:
    """Write a file with mandatory quality evidence.

    This tool wraps the standard Write tool but requires
    quality evidence (review reference, quality score) before
    allowing the write to proceed.

    Args:
        file_path: Path to write to.
        content: File content.
        quality_evidence: Reference to quality review artifact.
            Required for src/ files.
    """
    # Enforcement gate
    if file_path.startswith("src/") and not quality_evidence:
        return [TextContent(
            type="text",
            text="BLOCKED: Writing to src/ requires quality_evidence. "
                 "Provide a reference to a quality review artifact."
        )]

    # If validation passes, perform the actual write
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    Path(file_path).write_text(content)

    # Audit log
    log_enforcement_event("write_approved", file_path, quality_evidence)

    return [TextContent(type="text", text=f"File written: {file_path}")]
```

**Enforcement Power**: HIGH -- The MCP tool definition itself includes the quality constraint as a parameter. Claude cannot use the tool without providing the required parameter, creating a **structural enforcement** that is harder to bypass than prompt-based enforcement.

**Limitation**: Claude can still use the native Write tool instead of the MCP-wrapped version. This requires combining MCP enforcement with PreToolUse hooks that block native Write when the MCP alternative is available.

#### 1.2.2 MCP Resource Providers for Dynamic Rule Injection

MCP resources allow servers to provide contextual information that Claude can read. An enforcement server can expose quality framework rules as MCP resources:

```python
@server.resource("jerry://enforcement/rules")
async def get_enforcement_rules() -> str:
    """Provide current enforcement rules based on project context."""
    project = os.environ.get("JERRY_PROJECT", "")
    rules = load_project_enforcement_rules(project)
    return format_rules_as_context(rules)

@server.resource("jerry://enforcement/compliance-status")
async def get_compliance_status() -> str:
    """Provide current compliance status for the session."""
    status = load_compliance_state()
    return f"""
    Quality Compliance Dashboard:
    - Quality reviews completed: {status.reviews_completed}
    - Quality score documented: {status.score_documented}
    - Skills invoked: {', '.join(status.skills_invoked)}
    - Artifacts persisted: {status.artifacts_persisted}
    - Overall compliance: {status.compliance_percentage}%
    """
```

**Enforcement Power**: MEDIUM -- Resources provide context that Claude can read, but Claude is not forced to read them. However, MCP resources can be auto-loaded or referenced in prompts.

#### 1.2.3 MCP Prompts for Enforcement Templates

MCP prompts define reusable prompt templates that enforce specific interaction patterns:

```python
@server.prompt()
async def quality_review_prompt(
    artifact_path: str,
    review_type: str = "adversarial",
) -> list[PromptMessage]:
    """Structured quality review prompt template.

    Enforces the creator-critic-revision cycle by providing
    a structured review template.
    """
    return [
        PromptMessage(
            role="user",
            content=TextContent(
                type="text",
                text=f"""
                Perform a {review_type} review of: {artifact_path}

                MANDATORY REVIEW STRUCTURE:
                1. Score each dimension (0.0-1.0):
                   - Completeness: __
                   - Accuracy: __
                   - Depth: __
                   - Citations: __
                   - Actionability: __
                2. Calculate composite score (weighted average)
                3. List specific findings (strengths and weaknesses)
                4. Provide actionable revision recommendations
                5. Verdict: APPROVE (>=0.92) / REVISE (<0.92)
                """
            ),
        )
    ]
```

**Enforcement Power**: MEDIUM -- Prompts provide structure but rely on user/agent choosing to invoke them.

### 1.3 MCP Audit Logging Server

A dedicated MCP server for audit logging captures all tool interactions and creates an immutable compliance record:

```python
@server.tool()
async def log_quality_event(
    event_type: str,
    artifact_path: str,
    quality_score: float | None = None,
    review_reference: str | None = None,
    metadata: dict | None = None,
) -> list[TextContent]:
    """Log a quality framework event for audit purposes."""
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": event_type,
        "artifact_path": artifact_path,
        "quality_score": quality_score,
        "review_reference": review_reference,
        "session_id": os.environ.get("SESSION_ID"),
        "metadata": metadata or {},
    }

    # Append to immutable audit log
    audit_path = Path(".jerry/enforcement/audit.jsonl")
    audit_path.parent.mkdir(parents=True, exist_ok=True)
    with open(audit_path, "a") as f:
        f.write(json.dumps(event) + "\n")

    return [TextContent(type="text", text=f"Logged: {event_type}")]
```

**NASA SE Parallel**: This mirrors NASA's requirement for audit trails in configuration management (NASA-STD-8739.8, Section 4.3). Every modification to a controlled artifact must be recorded with who, what, when, and why.

### 1.4 Applicability Assessment

| Dimension | Assessment | Notes |
|-----------|------------|-------|
| **Claude Code Compatibility** | DIRECT | Claude Code natively supports MCP servers |
| **Implementation Effort** | MEDIUM (2-3 weeks) | Requires MCP server development and integration |
| **Enforcement Strength** | HIGH | Structural enforcement via tool parameters |
| **Bypass Resistance** | MEDIUM | Agent can use native tools unless blocked by hooks |
| **Portability** | HIGH | MCP is an open standard, works with any MCP-compatible client |
| **Maintenance** | MEDIUM | MCP server is a separate component to maintain |

### 1.5 Jerry-Specific Recommendation

**PURSUE**: MCP-based enforcement is the highest-priority alternative approach for Jerry. Implement:

1. **Phase 1**: MCP audit logging server (captures tool usage for compliance reporting)
2. **Phase 2**: MCP enforcement tool wrappers (quality-gated Write/Edit operations)
3. **Phase 3**: MCP resource providers (dynamic rule injection based on project state)

**Synergy with Existing Hooks**: Combine MCP enforcement with PreToolUse hooks that redirect native tool calls to MCP-wrapped versions. This creates a defense-in-depth where the hook blocks unvalidated native operations and the MCP server provides the validated alternative.

---

## Approach 2: AST-Based Code Analysis Guardrails

### 2.1 Overview

AST (Abstract Syntax Tree) based code analysis provides **structural validation** of LLM-generated code before it is written to disk. Rather than using regex patterns (which Jerry's current PatternLibrary uses), AST analysis understands code structure -- imports, class definitions, function signatures, type annotations -- enabling enforcement of architectural rules, coding standards, and quality requirements.

**Key Insight**: Jerry already uses AST analysis in its architecture tests (`tests/architecture/test_composition_root.py`, `tests/architecture/test_session_hook_architecture.py`). The same AST analysis infrastructure can be moved **upstream** into the PreToolUse hook to enforce architectural boundaries at write-time rather than test-time.

### 2.2 PreToolUse AST Validation

When Claude attempts to Write or Edit a Python file, the PreToolUse hook can parse the proposed content as an AST and validate it against Jerry's coding standards:

```python
import ast
from pathlib import Path


def validate_python_content(file_path: str, content: str) -> tuple[bool, str]:
    """Validate Python content against Jerry's coding standards via AST.

    Checks:
    1. Architecture boundaries (no forbidden imports)
    2. Type hints on public functions
    3. Docstrings on public classes/functions
    4. One-class-per-file rule
    5. Frozen dataclass for value objects
    """
    try:
        tree = ast.parse(content)
    except SyntaxError as e:
        return False, f"Syntax error in proposed code: {e}"

    violations = []

    # Check 1: Architecture boundary enforcement
    if "src/domain/" in file_path:
        forbidden_imports = check_domain_imports(tree)
        if forbidden_imports:
            violations.append(
                f"Domain layer cannot import from: {forbidden_imports}"
            )

    if "src/application/" in file_path:
        forbidden_imports = check_application_imports(tree)
        if forbidden_imports:
            violations.append(
                f"Application layer cannot import from: {forbidden_imports}"
            )

    # Check 2: Type hints on public functions
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if not node.name.startswith("_"):
                if node.returns is None:
                    violations.append(
                        f"Public function '{node.name}' missing return type hint"
                    )

    # Check 3: Docstrings on public classes
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            if not node.name.startswith("_"):
                if not (
                    node.body
                    and isinstance(node.body[0], ast.Expr)
                    and isinstance(node.body[0].value, ast.Constant)
                    and isinstance(node.body[0].value.value, str)
                ):
                    violations.append(
                        f"Public class '{node.name}' missing docstring"
                    )

    # Check 4: One-class-per-file
    public_classes = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.ClassDef)
        and not node.name.startswith("_")
    ]
    if len(public_classes) > 1:
        class_names = [c.name for c in public_classes]
        violations.append(
            f"One-class-per-file violation: found {class_names}"
        )

    if violations:
        return False, "; ".join(violations)
    return True, ""


def check_domain_imports(tree: ast.AST) -> list[str]:
    """Check that domain layer has no forbidden imports."""
    forbidden_prefixes = [
        "src.application",
        "src.infrastructure",
        "src.interface",
    ]
    violations = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            for prefix in forbidden_prefixes:
                if node.module.startswith(prefix):
                    violations.append(node.module)
    return violations
```

### 2.3 Tree-sitter for Multi-Language Analysis

Tree-sitter is a parser generator tool and incremental parsing library that can parse code in multiple languages into concrete syntax trees. For Jerry, tree-sitter could extend AST validation beyond Python:

- **Markdown validation**: Validate that research artifacts contain required sections (navigation tables, methodology, sources)
- **YAML/JSON schema validation**: Validate configuration files against schemas
- **Mixed-language analysis**: Validate code blocks within markdown documents

**Citation**: Tree-sitter project (https://tree-sitter.github.io/tree-sitter/). Developed by Max Brunsfeld, used by GitHub, Neovim, and many other tools.

**Feasibility**: MEDIUM -- Requires adding tree-sitter-python and tree-sitter-languages dependencies. The incremental parsing capability is valuable for real-time validation but may be over-engineered for hook-based batch validation.

### 2.4 Import Graph Enforcement at Write-Time

Jerry's architecture tests already validate import boundaries at test-time. Moving this to write-time provides immediate feedback:

```python
def check_import_graph_at_write(file_path: str, content: str) -> tuple[bool, str]:
    """Enforce architecture boundaries at write-time.

    This reuses the same logic from tests/architecture/test_composition_root.py
    but executes in the PreToolUse hook.
    """
    # Determine which layer this file belongs to
    layer = determine_layer(file_path)
    if layer is None:
        return True, ""  # Not in a managed layer

    try:
        tree = ast.parse(content)
    except SyntaxError:
        return True, ""  # Let syntax errors be caught elsewhere

    imports = extract_imports(tree)

    # Apply layer-specific import rules
    forbidden = get_forbidden_imports_for_layer(layer)
    violations = [imp for imp in imports if any(imp.startswith(f) for f in forbidden)]

    if violations:
        return False, (
            f"Architecture violation: {layer} layer cannot import from "
            f"{violations}. Fix imports before writing."
        )
    return True, ""
```

### 2.5 Applicability Assessment

| Dimension | Assessment | Notes |
|-----------|------------|-------|
| **Claude Code Compatibility** | HIGH | Fits directly into PreToolUse hook |
| **Implementation Effort** | LOW (Jerry already has AST infrastructure) | Reuse existing `get_imports_from_file()` |
| **Enforcement Strength** | HIGH | Blocks non-compliant code before write |
| **Bypass Resistance** | HIGH | Cannot write code that fails AST validation |
| **Portability** | HIGH | Python AST is stdlib, no external dependencies |
| **Maintenance** | LOW | Rules mirror existing architecture tests |

### 2.6 Jerry-Specific Recommendation

**PURSUE (HIGH PRIORITY)**: This is the lowest-effort, highest-impact alternative approach because Jerry already has the AST infrastructure in its architecture tests. The implementation is essentially: move `get_imports_from_file()` and related functions from `tests/architecture/` into `scripts/pre_tool_use.py` and add content-level validation to the Write/Edit hook path.

---

## Approach 3: Runtime Verification Approaches

### 3.1 Overview

Runtime verification monitors agent behavior during execution and checks it against a formal specification. Unlike hooks (which intercept specific lifecycle events), runtime verification operates on the **behavioral trace** of the agent -- the sequence of actions, tool calls, and state transitions over time.

### 3.2 State Machine Enforcement for Workflow Compliance

The core idea is to model Jerry's quality workflow as a finite state machine and enforce that the agent follows valid state transitions:

```
STATES:
  PLANNING       -- Agent is creating or reviewing a plan
  RESEARCHING    -- Agent is conducting research
  IMPLEMENTING   -- Agent is writing code
  TESTING        -- Agent is writing/running tests
  REVIEWING      -- Agent is conducting quality review
  REVISING       -- Agent is revising based on review
  COMPLETING     -- Agent is documenting completion

TRANSITIONS:
  PLANNING -> RESEARCHING       (plan approved)
  PLANNING -> IMPLEMENTING      (BLOCKED: must research first)
  RESEARCHING -> IMPLEMENTING   (research complete)
  IMPLEMENTING -> TESTING       (code written)
  IMPLEMENTING -> COMPLETING    (BLOCKED: must test first)
  TESTING -> REVIEWING          (tests pass)
  REVIEWING -> REVISING         (review complete, score < 0.92)
  REVIEWING -> COMPLETING       (review complete, score >= 0.92)
  REVISING -> REVIEWING         (revision complete)

ENFORCEMENT:
  If agent attempts IMPLEMENTING before RESEARCHING -> block
  If agent attempts COMPLETING before REVIEWING -> block
  If agent attempts COMPLETING with score < 0.92 -> block
```

**Implementation via Hooks**: The state machine can be implemented using the filesystem (`.jerry/enforcement/workflow-state.json`) and enforced through the combined action of UserPromptSubmit (detect task type and update state), PreToolUse (gate tool usage based on state), and PostToolUse (transition state after successful tool use).

```python
# .jerry/enforcement/workflow-state.json
{
    "current_state": "IMPLEMENTING",
    "transitions": [
        {"from": "PLANNING", "to": "RESEARCHING", "timestamp": "..."},
        {"from": "RESEARCHING", "to": "IMPLEMENTING", "timestamp": "..."}
    ],
    "blocked_transitions": [],
    "quality_score": null,
    "reviews_completed": 0
}
```

**NASA SE Parallel**: This directly mirrors NASA's Life Cycle Review Gates (SRR, PDR, CDR, TRR, ORR). Each review gate has entry criteria, exit criteria, and mandatory artifacts. You cannot proceed to the next phase without passing the current gate. NPR 7123.1D Section 6.6 defines these gates explicitly.

### 3.3 Temporal Logic Specifications

Temporal logic (LTL - Linear Temporal Logic, CTL - Computation Tree Logic) provides a formal language for specifying properties that must hold over time:

```
# LTL-style specifications for Jerry's quality workflow

# Property 1: Every implementation must eventually be tested
G(implement_file -> F(run_tests))

# Property 2: Every test run must be preceded by test writing
G(run_tests -> O(write_test))

# Property 3: Completion must be preceded by review
G(mark_complete -> O(quality_review AND score >= 0.92))

# Property 4: No implementation before planning
G(!plan_exists -> !implement_file)

# Property 5: Reviews must cycle (creator -> critic -> revision)
G(review_complete AND score < 0.92 -> F(revision AND F(review_complete)))
```

Where:
- `G` = Globally (always true)
- `F` = Eventually (true at some point in the future)
- `O` = Once (was true at some point in the past)
- `->` = Implies

**Feasibility**: LOW for direct implementation. Temporal logic model checkers (SPIN, NuSMV) are designed for concurrent system verification and would require significant adaptation for LLM agent monitoring. However, the **specifications themselves** are valuable as a formal statement of what Jerry's enforcement must achieve, even if enforcement uses simpler mechanisms (state machines, hooks).

**Citation**: Pnueli, A. "The temporal logic of programs" (1977, FOCS). The foundational paper on temporal logic for program verification.

**Citation**: Clarke, E.M., Grumberg, O., Peled, D.A. "Model Checking" (MIT Press, 1999). The standard reference for model checking theory and practice.

### 3.4 Constraint Satisfaction During Execution

Rather than model checking, a simpler runtime verification approach uses **constraint satisfaction**:

```python
class RuntimeConstraintChecker:
    """Check constraints on agent behavior during execution."""

    def __init__(self, state_path: Path):
        self.state = self._load_state(state_path)
        self.constraints = [
            # (constraint_name, check_function, enforcement_level)
            ("plan_before_implement", self._check_plan_exists, "HARD"),
            ("test_before_complete", self._check_tests_exist, "HARD"),
            ("review_before_complete", self._check_review_exists, "HARD"),
            ("score_threshold", self._check_score_threshold, "HARD"),
            ("skill_invocation", self._check_skills_invoked, "MEDIUM"),
        ]

    def check_all(self, proposed_action: str) -> list[ConstraintViolation]:
        """Check all constraints for a proposed action."""
        violations = []
        for name, check_fn, level in self.constraints:
            result = check_fn(proposed_action)
            if not result.satisfied:
                violations.append(ConstraintViolation(
                    constraint=name,
                    level=level,
                    message=result.message,
                    proposed_action=proposed_action,
                ))
        return violations
```

### 3.5 Applicability Assessment

| Dimension | Assessment | Notes |
|-----------|------------|-------|
| **Claude Code Compatibility** | MEDIUM | Requires state tracking infrastructure |
| **Implementation Effort** | MEDIUM (state machine), HIGH (temporal logic) | State machine is practical; full model checking is not |
| **Enforcement Strength** | HIGH | Prevents out-of-order workflow steps |
| **Bypass Resistance** | HIGH (state machine), MEDIUM (temporal logic) | State machine blocks invalid transitions |
| **Portability** | HIGH | State machine pattern is universal |
| **Maintenance** | MEDIUM | State definitions need updating with workflow changes |

### 3.6 Jerry-Specific Recommendation

**PURSUE (MEDIUM PRIORITY)**: Implement a filesystem-backed state machine for workflow enforcement. The temporal logic specifications serve as requirements documentation but should not be implemented as a model checker. Use the simpler constraint satisfaction approach.

---

## Approach 4: Formal Methods for LLM Outputs

### 4.1 Overview

Formal methods apply mathematical techniques to specify, develop, and verify software systems. For LLM agent enforcement, formal methods provide rigorous ways to specify what "correct" agent behavior looks like and verify that actual behavior conforms.

### 4.2 Contract-Based Design for Agent Interactions

Design-by-Contract (DbC) specifies preconditions, postconditions, and invariants for each operation:

```python
from dataclasses import dataclass
from typing import Callable


@dataclass
class AgentContract:
    """Contract for an agent action."""

    action_name: str
    preconditions: list[Callable[[], bool]]
    postconditions: list[Callable[[], bool]]
    invariants: list[Callable[[], bool]]


# Contract: Create implementation file
create_implementation_contract = AgentContract(
    action_name="create_implementation",
    preconditions=[
        lambda: plan_exists(),                    # Plan must exist
        lambda: requirements_defined(),           # Requirements must be defined
        lambda: not is_workflow_state("BLOCKED"), # Not in blocked state
    ],
    postconditions=[
        lambda: test_file_exists(),               # Test file must exist
        lambda: docstrings_present(),             # All public functions documented
        lambda: type_hints_present(),             # All public functions typed
    ],
    invariants=[
        lambda: architecture_boundaries_respected(),  # No layer violations
        lambda: one_class_per_file(),                 # File organization rule
    ],
)
```

**Citation**: Meyer, B. "Object-Oriented Software Construction" (Prentice Hall, 1997). The foundational work on Design by Contract.

**Applicability**: MEDIUM -- Contracts can be enforced through the hook system. Preconditions map to PreToolUse checks; postconditions map to PostToolUse checks; invariants map to both. The challenge is implementing the check functions (e.g., `test_file_exists()` requires knowing which test file corresponds to the implementation file).

### 4.3 Property-Based Testing of LLM Outputs

Property-based testing (PBT) generates random inputs and checks that outputs satisfy specified properties. For LLM agents, PBT can validate that generated code satisfies structural properties:

```python
from hypothesis import given, strategies as st


@given(st.text(min_size=1, max_size=100))
def test_work_item_title_always_produces_valid_id(title: str):
    """Property: Any non-empty title produces a valid work item ID."""
    work_item = WorkItem.create(title=title)
    assert work_item.id is not None
    assert len(work_item.id.value) > 0


@given(st.sampled_from(["pending", "in_progress", "done", "cancelled"]))
def test_state_transitions_are_deterministic(initial_state: str):
    """Property: State transitions from any state are deterministic."""
    item = create_work_item_in_state(initial_state)
    valid_transitions = item.status.get_valid_transitions()

    for target in valid_transitions:
        # Transition should always succeed
        transitioned = transition_to(item, target)
        assert transitioned.status == target
```

**Citation**: Claessen, K. and Hughes, J. "QuickCheck: A Lightweight Tool for Random Testing of Haskell Programs" (2000, ICFP). The foundational paper on property-based testing.

**Citation**: MacIver, D. et al. "Hypothesis: A new approach to property-based testing" (2019, Journal of Open Source Software). The Python implementation.

**Applicability**: HIGH -- Jerry already uses pytest; Hypothesis integrates directly. Property-based testing is particularly valuable for validating domain logic (value objects, state machines, event sourcing) where the space of valid inputs is large but the invariants are well-defined.

### 4.4 Formal Specification of Output Requirements

Formal specifications can define exactly what a "quality-compliant" output looks like:

```
SPECIFICATION: ResearchArtifact
  REQUIRED SECTIONS:
    - executive_summary: NonEmpty(String)
    - methodology: Contains("source evaluation" OR "confidence")
    - sources: MinCount(3, Citation)
    - disclaimer: Contains("limitation" OR "caveat")

  STRUCTURAL CONSTRAINTS:
    - navigation_table: Present AND Contains(AnchorLinks)
    - word_count: >= 1000
    - heading_hierarchy: Monotonic(h1 > h2 > h3)

  QUALITY CONSTRAINTS:
    - citation_density: >= 1 per 500 words
    - claim_support: ForAll(Claim, HasCitation(Claim))
```

This specification can be implemented as a validation function that checks markdown artifacts:

```python
def validate_research_artifact(content: str) -> list[str]:
    """Validate a research artifact against formal specification."""
    violations = []

    # Check required sections
    required_sections = [
        ("executive_summary", r"##\s+(Executive\s+)?Summary"),
        ("methodology", r"##\s+Methodology"),
        ("sources", r"##\s+(Sources|References)"),
        ("disclaimer", r"##\s+Disclaimer"),
    ]
    for name, pattern in required_sections:
        if not re.search(pattern, content, re.IGNORECASE):
            violations.append(f"Missing required section: {name}")

    # Check navigation table
    if "| Section | Purpose |" not in content:
        violations.append("Missing navigation table")

    # Check minimum word count
    word_count = len(content.split())
    if word_count < 1000:
        violations.append(f"Word count {word_count} < 1000 minimum")

    return violations
```

### 4.5 Applicability Assessment

| Dimension | Assessment | Notes |
|-----------|------------|-------|
| **Claude Code Compatibility** | HIGH (PBT, specification validation), LOW (model checking) | Practical subsets integrate well |
| **Implementation Effort** | LOW (PBT, spec validation), HIGH (full formal methods) | Start with practical subsets |
| **Enforcement Strength** | HIGH (for what they cover) | Mathematically rigorous where applicable |
| **Bypass Resistance** | HIGH | Formal validation is deterministic |
| **Portability** | HIGH | Based on standard tools (Hypothesis, regex, AST) |
| **Maintenance** | MEDIUM | Specifications must evolve with requirements |

### 4.6 Jerry-Specific Recommendation

**PURSUE (SELECTIVE)**:
- **YES**: Property-based testing for domain logic (integrate Hypothesis into test suite)
- **YES**: Formal output specification validation for research artifacts (implement as PostToolUse check)
- **NO**: Full temporal logic model checking (too complex, insufficient ROI)
- **MAYBE**: Contract-based design (valuable conceptually, implement as hook precondition/postcondition checks)

---

## Approach 5: Cross-Platform Enforcement Patterns

### 5.1 Overview

Multiple LLM platforms provide enforcement mechanisms. While many are platform-specific, the **patterns** they implement are often portable. This section catalogs enforcement patterns from OpenAI, Google, and Amazon, and identifies which patterns can be transferred to Claude Code/Jerry.

### 5.2 OpenAI Assistants API Enforcement Mechanisms

The OpenAI Assistants API (v2, 2024) provides:

**Function Calling Constraints**:
- `tools` parameter defines exactly which tools an assistant can use
- `tool_choice` can force use of a specific tool or set to `"none"` to prevent tool use entirely
- Structured output via `response_format` with JSON Schema

**Code Interpreter Sandbox**:
- Code execution runs in an isolated sandbox environment
- File access is restricted to uploaded files
- No network access from the sandbox
- Execution timeout enforcement

**File Search with Knowledge Cutoff**:
- Vector store for RAG with configurable retrieval
- Annotations in responses link back to source documents

**Run-Level Configuration**:
- `max_completion_tokens` caps output length
- `truncation_strategy` controls context management
- `temperature` and `top_p` control output determinism

**Portable Pattern**: **Tool restriction and structured output enforcement**. Jerry can implement this through:
1. PreToolUse hooks that whitelist allowed tools per task type
2. PostToolUse hooks that validate output structure against JSON schemas
3. MCP tool definitions that enforce structured parameters

**Citation**: OpenAI Assistants API documentation (https://platform.openai.com/docs/assistants/overview). Accessed via training data, pre-May 2025.

### 5.3 Amazon Bedrock Guardrails

Amazon Bedrock Guardrails (GA December 2023, enhanced 2024) provides:

**Content Filtering**:
- Configurable thresholds for hate, insults, sexual content, violence, misconduct
- Each category has strength levels: NONE, LOW, MEDIUM, HIGH

**Denied Topics**:
- Custom topic definitions with example prompts
- Topic detection uses NLI (natural language inference) models
- Can block both input and output containing denied topics

**Word/Phrase Filters**:
- Exact match and regex-based blocking
- Applied to both input and output

**PII Detection and Redaction**:
- Automatic PII detection (names, SSNs, emails, etc.)
- Configurable action per PII type: BLOCK or ANONYMIZE
- Custom regex patterns for domain-specific PII

**Contextual Grounding Check** (2024):
- Validates that model responses are grounded in provided context
- Configurable grounding threshold
- Detects hallucination by comparing output to reference sources

**Portable Patterns for Jerry**:

| Bedrock Pattern | Jerry Applicability | Implementation Vector |
|----------------|--------------------|-----------------------|
| Content filtering with thresholds | Adapt for quality content checks (e.g., citation density thresholds) | PostToolUse hook or MCP tool |
| Denied topics | Block certain code patterns (e.g., `eval()`, `exec()`, direct infra imports in domain) | PreToolUse hook (already partially implemented) |
| PII redaction | Already implemented in Jerry's PostToolUse output filtering | Existing infrastructure |
| Contextual grounding | **Highly applicable**: Validate that research claims are grounded in cited sources | Novel implementation needed |
| Configurable thresholds | Quality score thresholds with configurable strictness per project | Configuration file + hook enforcement |

**Citation**: Amazon Bedrock Guardrails documentation (https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html). AWS re:Invent 2023 launch, enhanced at re:Invent 2024.

### 5.4 Google Gemini Safety Settings

Google Gemini API provides:

**Safety Settings**:
- Per-category harm thresholds (harassment, hate speech, sexually explicit, dangerous content)
- Threshold levels: BLOCK_NONE, BLOCK_ONLY_HIGH, BLOCK_MEDIUM_AND_ABOVE, BLOCK_LOW_AND_ABOVE

**System Instructions**:
- Persistent instructions prepended to all prompts
- Cannot be overridden by user prompts
- Similar to Claude's system prompts but with explicit override protection

**Structured Output**:
- `response_mime_type` for JSON output
- Schema enforcement via `response_schema` parameter
- Enum constraints on output fields

**Portable Pattern**: **System instruction override protection**. Google's explicit protection against user prompt injection overriding system instructions is a pattern Jerry should adopt. Currently, Claude's context window management means that early instructions can be pushed into the "middle" where they receive less attention (the "Lost in the Middle" effect). The portable pattern is:

1. Place critical enforcement instructions at both the beginning AND end of the context
2. Use hooks to reinject enforcement instructions on every prompt (UserPromptSubmit)
3. Mark enforcement instructions as non-overridable through explicit language and structural protection

**Citation**: Google Gemini API documentation (https://ai.google.dev/docs). Based on training data, pre-May 2025.

### 5.5 Portable Enforcement Pattern Catalog

Synthesizing across platforms, the following patterns are **platform-independent** and applicable to Jerry:

| Pattern | Description | OpenAI | Bedrock | Gemini | Claude Code | Jerry Implementation |
|---------|-------------|--------|---------|--------|-------------|---------------------|
| **Tool Restriction** | Whitelist allowed tools per context | YES | N/A | N/A | Via PreToolUse hooks | Implement tool whitelisting |
| **Structured Output** | Enforce output schema compliance | YES | YES | YES | Via PostToolUse hooks | Implement schema validation |
| **Content Threshold** | Configurable quality thresholds | N/A | YES | YES | Via hooks + config | Implement threshold config |
| **Grounding Check** | Validate claims against sources | N/A | YES | N/A | Via PostToolUse | Implement citation validation |
| **Instruction Protection** | Prevent override of enforcement instructions | N/A | N/A | YES | Via UserPromptSubmit + rules positioning | Implement reinsertion pattern |
| **Execution Sandbox** | Isolated code execution | YES | N/A | N/A | Via Bash hook restrictions | Extend Bash restrictions |
| **Audit Trail** | Log all actions immutably | Partial | YES | Partial | Via PostToolUse + MCP | Implement comprehensive logging |

### 5.6 Applicability Assessment

| Dimension | Assessment | Notes |
|-----------|------------|-------|
| **Claude Code Compatibility** | HIGH (patterns are portable) | Implementation uses Claude Code mechanisms |
| **Implementation Effort** | LOW-MEDIUM per pattern | Most patterns map to existing hook infrastructure |
| **Enforcement Strength** | VARIES by pattern | Structural enforcement is strongest |
| **Bypass Resistance** | VARIES by pattern | Platform-enforced > prompt-based |
| **Portability** | HIGH (that's the point) | Patterns work across platforms |
| **Maintenance** | LOW | Patterns are stable architectural concepts |

### 5.7 Jerry-Specific Recommendation

**PURSUE (HIGH PRIORITY for portable patterns)**: Adopt the portable enforcement patterns as a cross-platform abstraction layer. This ensures Jerry's enforcement approach is not locked to Claude Code's specific hook API, making the framework more resilient to API changes and more valuable to users on other platforms.

---

## Approach 6: Novel Enforcement Research (2024-2026)

### 6.1 Overview

The field of LLM agent governance is rapidly evolving. This section catalogs emerging research approaches that may become practical enforcement mechanisms in the near future.

### 6.2 Multi-Agent Governance Frameworks

**Concept**: Instead of a single enforcement mechanism, use specialized governance agents that monitor and correct other agents' behavior.

**Architecture**:
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Creator     │────>│  Governor   │────>│  Auditor    │
│  Agent       │     │  Agent      │     │  Agent      │
│ (does work)  │     │ (enforces)  │     │ (verifies)  │
└─────────────┘     └─────────────┘     └─────────────┘
        │                  │                    │
        v                  v                    v
   Artifacts          Enforcement          Audit Trail
                       Decisions
```

**Key Research**:
- **Constitutional AI** (Bai et al., 2022): Self-critique against principles
- **Debate** (Irving et al., 2018): Two agents argue, judge decides
- **Recursive Reward Modeling** (Leike et al., 2018): Agents evaluate agents
- **RLHF-Inspired Runtime Patterns**: Use reward models at runtime to score agent behavior

**Citation**: Irving, G., Christiano, P., Amodei, D. "AI safety via debate" (2018, arXiv:1805.00899). Proposes adversarial debate as a scalable alignment mechanism.

**Citation**: Leike, J. et al. "Scalable agent alignment via reward modeling" (2018, arXiv:1811.07871). Recursive reward modeling for agent evaluation.

**Applicability to Jerry**: MEDIUM-HIGH. Jerry already has the multi-agent architecture (ps-researcher, ps-critic, ps-reviewer, nse-explorer, etc.) and the creator-critic-revision cycle. The novel aspect would be making the governance agent **always active** rather than invoked on demand. This maps to the proposed UserPromptSubmit hook acting as a persistent "governance agent" that evaluates every action.

**Limitation**: Jerry's constraint P-003 (No Recursive Subagents) limits nesting to one level (orchestrator -> worker). A dedicated governance agent would need to operate at the same level as the orchestrator, not as a sub-sub-agent.

### 6.3 Decentralized Enforcement (Agents Monitoring Each Other)

**Concept**: Rather than a central enforcement mechanism, agents monitor each other's outputs and flag violations. This is inspired by blockchain consensus mechanisms and Byzantine fault tolerance.

**Research Direction**: Multi-agent frameworks (AutoGen, CrewAI) are exploring "peer review" patterns where each agent's output is validated by at least one other agent before being accepted.

**Citation**: Wu et al., "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation" (2023, Microsoft Research). Section on "Nested Conversations" describes multi-agent validation patterns.

**Applicability to Jerry**: LOW-MEDIUM. Jerry's single-level subagent constraint (P-003) limits the depth of peer review. However, the pattern could be implemented as **sequential validation** where the orchestrator sends output to a reviewer agent before accepting it. This is essentially what the creator-critic-revision cycle already does.

### 6.4 Embedding-Based Compliance Checking

**Concept**: Use embedding models to check semantic similarity between agent outputs and compliance exemplars. Instead of regex-based pattern matching, use learned representations to detect compliance.

**Architecture**:
```
Agent Output ──> Embedding Model ──> Similarity Score ──> Compliance Decision
                       ^
                       |
               Compliance Exemplar Embeddings
               (known-good outputs, templates)
```

**Use Cases**:
1. **Template compliance**: Check if a research artifact is "similar enough" to a known-good template
2. **Style consistency**: Check if code follows Jerry's naming conventions by comparing to exemplar code
3. **Quality estimation**: Estimate quality score based on semantic similarity to high-quality exemplars

**Feasibility**: LOW for Jerry currently. Requires:
- An embedding model (could use Anthropic's API or local model)
- A vector store for exemplar embeddings
- Latency budget for embedding computation in hooks

**Future Potential**: HIGH. As embedding infrastructure becomes cheaper and faster, this approach could provide more nuanced compliance checking than regex or AST-based methods.

### 6.5 Tool-Use Monitoring and Intervention

**Concept**: Build statistical models of "normal" agent tool usage patterns and detect anomalies that may indicate enforcement bypass.

**Research**: This is analogous to **intrusion detection systems (IDS)** in network security, which monitor traffic patterns and flag anomalies.

**Example Patterns to Monitor**:
- Agent writes implementation files without first reading test files -> possible test-first violation
- Agent writes to `src/` without any prior reads from `.claude/rules/` -> possible rule bypass
- Agent tool call frequency changes dramatically -> possible context degradation
- Agent stops invoking skills after initial session -> possible skill invocation decay

**Implementation**: Lightweight logging in PostToolUse hook + periodic analysis script:

```python
def detect_anomalies(tool_log: list[ToolEvent]) -> list[Anomaly]:
    """Detect behavioral anomalies in tool usage patterns."""
    anomalies = []

    # Check: Implementation without preceding test
    write_events = [e for e in tool_log if e.tool == "Write" and "src/" in e.path]
    for write in write_events:
        preceding = [e for e in tool_log if e.timestamp < write.timestamp]
        test_reads = [e for e in preceding if "test" in e.path.lower()]
        if not test_reads:
            anomalies.append(Anomaly(
                type="implementation_without_test_context",
                event=write,
                severity="MEDIUM",
            ))

    return anomalies
```

### 6.6 Applicability Assessment

| Dimension | Assessment | Notes |
|-----------|------------|-------|
| **Claude Code Compatibility** | VARIES | Multi-agent: MEDIUM; Embedding: LOW; Monitoring: HIGH |
| **Implementation Effort** | MEDIUM-HIGH | All approaches require new infrastructure |
| **Enforcement Strength** | MEDIUM | Probabilistic rather than deterministic |
| **Bypass Resistance** | MEDIUM | Statistical approaches can have false negatives |
| **Portability** | HIGH (patterns), LOW (implementations) | Concepts are universal |
| **Maintenance** | HIGH | Models need retraining, baselines need updating |

### 6.7 Jerry-Specific Recommendation

**PURSUE (LOW PRIORITY -- Future Investment)**:
- **YES**: Tool-use monitoring (lightweight, integrates with PostToolUse logging)
- **MAYBE**: Multi-agent governance (explore after P-003 constraint is revisited)
- **DEFER**: Embedding-based compliance (wait for cheaper, faster embedding infrastructure)
- **DEFER**: Decentralized enforcement (current architecture doesn't support it well)

---

## Approach 7: Physical Systems Analogies (NASA SE)

### 7.1 Overview

Safety-critical systems engineering has decades of experience enforcing process compliance in environments where failure has catastrophic consequences. This section applies NASA SE perspective to LLM agent enforcement, identifying patterns that can elevate Jerry's enforcement rigor.

### 7.2 Independent Verification & Validation (IV&V)

**NASA Definition**: "The process of evaluating work products, activities, and processes to ensure compliance with stated requirements and standards, where the evaluation is performed by personnel or organizations that are not responsible for the development" (NPR 7123.1D, Section 6.8).

**Key Properties of IV&V**:
1. **Technical Independence**: The verifier uses different tools, techniques, and approaches than the developer
2. **Managerial Independence**: The verifier reports to a different management chain
3. **Financial Independence**: The verifier has separate funding (cannot be pressured by developer)

**Application to Jerry**:

| IV&V Property | Jerry Current State | Gap | Recommended Enhancement |
|---------------|--------------------|----|------------------------|
| Technical Independence | ps-critic uses same model as creator | No diversity | Use different prompt strategies, or different model providers for review |
| Managerial Independence | Same orchestrator controls both creator and critic | No separation | Implement governance hooks that are outside orchestrator control |
| Financial Independence | Not applicable (no budgets) | N/A | N/A |
| Separate Tools | Same tool set for creation and review | Partial overlap | Implement dedicated review tools with different analysis capabilities |
| Formal Verification Plans | No formal V&V plan | Major gap | Create verification plan per deliverable type |

**Proposed IV&V Implementation for Jerry**:

```markdown
## Verification Plan for Research Artifacts

### Verification Methods

| Requirement | Method | Tool | Independence Level |
|------------|--------|------|-------------------|
| Contains executive summary | Inspection | AST/regex validator | AUTOMATED (fully independent) |
| Citations are authoritative | Analysis | ps-reviewer agent | AGENT (independent agent) |
| Quality score >= 0.92 | Test | Quality scoring tool | AUTOMATED |
| Methodology documented | Inspection | Template validator | AUTOMATED |
| Claims are supported | Analysis | ps-critic with adversarial lens | AGENT |
| Navigation table present | Inspection | Markdown validator | AUTOMATED |

### Verification Cross-Reference Matrix (VCRM)

| Requirement ID | Requirement Text | Verification Method | Verification Artifact | Status |
|---------------|-----------------|---------------------|----------------------|--------|
| REQ-001 | Research artifact contains executive summary | Automated inspection | validation-report.json | PENDING |
| REQ-002 | All claims have citations | Agent analysis | review-artifact.md | PENDING |
| REQ-003 | Quality score >= 0.92 | Automated test | quality-score.json | PENDING |
```

**Citation**: NASA NPR 7123.1D "NASA Systems Engineering Processes and Requirements" (2020), Section 6.8 "Verification and Validation".

**Citation**: NASA NPR 7150.2D "NASA Software Engineering Requirements" (2021), Section 5.3.5 "Independent Verification and Validation".

### 7.3 Mission Assurance Framework

**NASA Definition**: "The disciplined application of engineering, quality, and management principles toward the goal of achieving mission success" (NASA NPR 8705.6).

**Mission Assurance Practices Applicable to LLM Agents**:

1. **Problem/Failure Reporting (PFR)**: Every failure must be formally reported, root-cause analyzed, and corrective action tracked to closure.

   **Jerry Application**: When an agent bypasses quality enforcement (detected via audit log or post-hoc review), create a formal incident record:

   ```markdown
   ## Enforcement Failure Report

   **ID:** EFR-001
   **Date:** 2026-02-13
   **Classification:** Quality Bypass
   **Severity:** Medium

   **Description:** Agent wrote implementation file without invoking
   /problem-solving skill for research phase.

   **Root Cause:** UserPromptSubmit hook not implemented; no enforcement
   of skill invocation requirement.

   **Corrective Action:** Implement UserPromptSubmit hook with skill
   invocation tracking.

   **Verification:** Hook test confirms skill invocation enforcement.

   **Status:** OPEN
   ```

2. **Configuration Management (CM)**: All artifacts under configuration control. Changes require formal change requests, impact analysis, and approval.

   **Jerry Application**: Jerry already uses git for configuration management. The gap is that enforcement rule changes are not formally tracked. Proposed enhancement: require an ADR (Architecture Decision Record) for any change to enforcement rules, hook configurations, or quality thresholds.

3. **Risk Management**: Proactive identification, assessment, and mitigation of risks.

   **Jerry Application**: Apply FMEA (Failure Mode and Effects Analysis) to each enforcement vector:

   | Enforcement Vector | Failure Mode | Effect | Severity | Probability | Detection | RPN | Mitigation |
   |-------------------|-------------|--------|----------|-------------|-----------|-----|------------|
   | PreToolUse hook | Hook timeout | Tool call proceeds unchecked | Medium | Low | Low | 6 | Optimize hook performance; set appropriate timeouts |
   | Rules (.claude/) | Context rot pushes rules to middle | Agent ignores rules | High | High | Low | 18 | Reinforce via UserPromptSubmit; recency injection |
   | Quality scoring | Score not calculated | Non-compliant output accepted | High | Medium | Medium | 12 | Automated scoring in PostToolUse; block completion without score |
   | Adversarial review | Review skipped | Low-quality output shipped | High | High | Low | 18 | Enforce via Stop hook; require review artifact |

   (RPN = Severity x Probability x Detection, each on 1-5 scale)

**Citation**: NASA NPR 8705.6 "Safety and Mission Assurance (SMA) Policy" (2021).

**Citation**: SAE J1739 "Potential Failure Mode and Effects Analysis in Design (Design FMEA), Potential Failure Mode and Effects Analysis in Manufacturing and Assembly Processes (Process FMEA)" (2009).

### 7.4 NASA-STD-8739.8 Software Quality Assurance

**NASA-STD-8739.8** establishes requirements for software assurance across all NASA programs. Key enforcement patterns:

1. **Software Classification**: Software is classified by criticality level (A through D), with higher levels requiring more rigorous assurance practices.

   | NASA Level | Description | Jerry Equivalent |
   |-----------|-------------|-----------------|
   | Class A | Human safety, mission success | Core framework code (src/domain/, src/application/) |
   | Class B | Mission significant | Infrastructure adapters, hooks |
   | Class C | Support | Scripts, utilities, documentation |
   | Class D | Internal | Test helpers, development tools |

   **Enforcement Implication**: Different enforcement rigor based on file classification. Files in `src/domain/` get HARD enforcement (AST validation, mandatory type hints, docstrings). Files in `scripts/` get MEDIUM enforcement (basic quality checks only).

2. **Peer Review Requirements**: All Class A/B software must have formal peer review with documented findings and resolution.

   **Jerry Application**: Make adversarial review MANDATORY for domain and application layer changes, OPTIONAL for infrastructure and interface changes.

3. **Test Coverage Requirements**: Minimum coverage thresholds based on software class.

   | NASA Class | Statement Coverage | Branch Coverage | MC/DC |
   |-----------|-------------------|-----------------|-------|
   | Class A | 100% | 100% | Required |
   | Class B | 90% | 80% | Optional |
   | Class C | 80% | N/A | N/A |

   **Jerry Current State**: 90% line coverage threshold (matches Class B). Consider increasing domain layer coverage to 100% (Class A).

**Citation**: NASA-STD-8739.8B "NASA Software Assurance and Software Safety Standard" (2022).

### 7.5 Safety-Critical Systems: How They Enforce Compliance

Across NASA, DO-178C, ISO 26262, and IEC 61508, safety-critical systems share enforcement principles:

| Principle | NASA | DO-178C | ISO 26262 | IEC 61508 | Jerry Application |
|-----------|------|---------|-----------|-----------|-------------------|
| **Classification** | Software Classes A-D | Design Assurance Levels A-E | ASIL A-D | SIL 1-4 | Classify files by enforcement rigor |
| **Independence** | IV&V organization | Independent QA | Confirmation measures | Independent assessment | Separate creator and reviewer agents |
| **Traceability** | Requirements -> V&V -> Artifacts | Objectives -> Data -> Evidence | Requirements -> Work Products | Safety Requirements -> Tests | VCRM implementation |
| **Gate Reviews** | SRR, PDR, CDR, TRR, ORR | Planning, Development, Verification, CM | Concept, System, Safety Validation | Safety Concept, Design, Integration | Workflow state machine gates |
| **Audit Trail** | All actions logged | Data item tracking | Work product documentation | Safety lifecycle documentation | PostToolUse + MCP audit logging |
| **Escape Clause** | Formal waiver process | Alternative means of compliance | Rationale for deviation | Justification for non-compliance | Jerry does not have a waiver process |

**Missing from Jerry**: A **formal waiver process**. In safety-critical systems, you can deviate from a requirement, but you must formally document the deviation, provide justification, assess the impact, and get explicit approval. Jerry's current enforcement has no waiver mechanism -- constraints are either enforced or not, with no middle ground for justified exceptions.

**Proposed Waiver Process**:
```markdown
## Quality Waiver Request

**ID:** QW-001
**Date:** 2026-02-13
**Requester:** [Agent/User]
**Constraint:** QE-002 (Quality Score >= 0.92)
**Requested Deviation:** Accept score of 0.87 for this artifact
**Justification:** Exploratory research with inherently uncertain
findings; higher score not achievable without fabricating confidence.
**Impact Assessment:** LOW -- exploratory artifact, not implementation guide.
**Approval:** [User must approve]
**Expiry:** This waiver, this artifact only.
```

### 7.6 Applicability Assessment

| Dimension | Assessment | Notes |
|-----------|------------|-------|
| **Claude Code Compatibility** | HIGH (patterns), MEDIUM (implementation) | Patterns are universal; implementation needs adaptation |
| **Implementation Effort** | MEDIUM | VCRM and classification are significant but one-time efforts |
| **Enforcement Strength** | VERY HIGH | Proven in systems where lives depend on compliance |
| **Bypass Resistance** | VERY HIGH | Multi-layered with independent verification |
| **Portability** | VERY HIGH | Industry standards, not platform-specific |
| **Maintenance** | MEDIUM-HIGH | Classification and VCRM must be maintained |

### 7.7 Jerry-Specific Recommendation

**PURSUE (HIGH PRIORITY)**:
1. **File classification system**: Classify Jerry's codebase by enforcement rigor level (Class A-D)
2. **VCRM for quality requirements**: Map every quality requirement to a verification method and artifact
3. **Formal waiver process**: Implement a documented exception mechanism
4. **FMEA for enforcement vectors**: Systematically analyze failure modes of each enforcement mechanism
5. **Enforcement failure reporting**: Create incident records for enforcement bypasses

---

## Comparative Analysis

### Cross-Approach Comparison Matrix

| Approach | Novelty (1-5) | Feasibility (1-5) | Impact (1-5) | Effort (1-5) | Bypass Resistance (1-5) | Total (Max 25) |
|----------|-------------|-------------------|-------------|-------------|------------------------|----------------|
| MCP Enforcement Server | 5 | 4 | 5 | 3 | 4 | **21** |
| AST Code Analysis in PreToolUse | 3 | 5 | 4 | 5 | 5 | **22** |
| Runtime State Machine | 3 | 4 | 4 | 3 | 4 | **18** |
| Property-Based Testing | 3 | 5 | 3 | 4 | 5 | **20** |
| Cross-Platform Portable Patterns | 3 | 5 | 4 | 4 | 3 | **19** |
| NASA IV&V Patterns | 5 | 3 | 5 | 2 | 5 | **20** |
| Contract-Based Design | 3 | 3 | 3 | 3 | 4 | **16** |
| Tool-Use Monitoring | 3 | 4 | 3 | 3 | 3 | **16** |
| Formal Output Specification | 3 | 4 | 3 | 4 | 4 | **18** |
| Multi-Agent Governance | 4 | 3 | 4 | 2 | 3 | **16** |
| Embedding-Based Compliance | 4 | 2 | 3 | 1 | 3 | **13** |
| Temporal Logic | 2 | 2 | 3 | 1 | 4 | **12** |

**Scoring Key**:
- Novelty: How different is this from existing enforcement vectors? (5 = completely novel)
- Feasibility: How practical to implement in Claude Code/Jerry? (5 = drop-in)
- Impact: How much will this improve enforcement? (5 = transformative)
- Effort: How easy to implement? (5 = trivial, 1 = months of work)
- Bypass Resistance: How hard to circumvent? (5 = impossible to bypass)

### Implementation Priority Recommendation

Based on the comparative analysis:

**Tier 1: Immediate (Next Sprint)**
1. **AST Code Analysis in PreToolUse** (Score: 22) -- Jerry already has the infrastructure; this is a repackaging exercise
2. **MCP Enforcement Server** (Score: 21) -- Highest novelty and impact; Claude Code supports MCP natively

**Tier 2: Near-Term (Next 2 Sprints)**
3. **Property-Based Testing** (Score: 20) -- Integrates with existing pytest infrastructure
4. **NASA IV&V Patterns** (Score: 20) -- High impact but requires cultural/process changes
5. **Cross-Platform Portable Patterns** (Score: 19) -- Improves portability and resilience

**Tier 3: Medium-Term (Next Quarter)**
6. **Runtime State Machine** (Score: 18) -- Requires state tracking infrastructure
7. **Formal Output Specification** (Score: 18) -- Valuable for artifact validation

**Tier 4: Future Investigation**
8. **Contract-Based Design** (Score: 16)
9. **Tool-Use Monitoring** (Score: 16)
10. **Multi-Agent Governance** (Score: 16)
11. **Embedding-Based Compliance** (Score: 13)
12. **Temporal Logic** (Score: 12)

---

## L2: Architectural Recommendations for Jerry

### Architecture Decision: Which Alternatives Are Worth Pursuing?

Based on the comprehensive analysis across all 7 approach families and 18 specific mechanisms, the following architectural recommendations are made for Jerry:

### Recommendation 1: Implement MCP Enforcement Server (CRITICAL)

**Rationale**: MCP provides the only **protocol-level** enforcement vector in the catalog. Unlike hooks (which are Claude Code-specific), MCP is an open standard that works across MCP-compatible clients. The MCP enforcement server can provide:
- Tool wrapping with structural parameter enforcement
- Compliance-aware resources
- Standardized audit logging
- Enforcement that is harder to bypass than prompt-based approaches

**Architecture**:
```
Claude Code
    |
    +-- Native Tools (Write, Edit, Bash)
    |       |
    |       +-- PreToolUse Hook (blocks native Write when MCP available)
    |
    +-- MCP Enforcement Server
            |
            +-- jerry://tools/write_with_quality_gate
            +-- jerry://tools/complete_with_review
            +-- jerry://resources/enforcement-rules
            +-- jerry://resources/compliance-status
            +-- jerry://prompts/quality-review
            +-- jerry://audit/log
```

**Effort**: 2-3 weeks
**Risk**: MCP server maintenance overhead; potential latency
**Mitigation**: Start with audit logging (lowest risk, highest diagnostic value)

### Recommendation 2: Move AST Validation to PreToolUse (HIGH PRIORITY)

**Rationale**: Jerry already has all the infrastructure needed (`tests/architecture/test_composition_root.py` contains `get_imports_from_file()`, `has_infrastructure_import()`, and layer boundary checking). Moving this to the PreToolUse hook provides immediate structural enforcement of architecture boundaries at write-time rather than test-time.

**Architecture**:
```
PreToolUse Hook (enhanced)
    |
    +-- Phase 1: Security checks (existing)
    +-- Phase 2: Pattern library validation (existing)
    +-- Phase 3: AST structural validation (NEW)
            |
            +-- Import boundary enforcement
            +-- Type hint verification
            +-- Docstring presence check
            +-- One-class-per-file rule
            +-- Frozen dataclass for value objects
```

**Effort**: 3-5 days (reuse existing code)
**Risk**: False positives blocking legitimate writes
**Mitigation**: Start with WARN mode; escalate to BLOCK after tuning

### Recommendation 3: Implement File Classification System (HIGH PRIORITY)

**Rationale**: NASA-STD-8739.8 demonstrates that different code requires different levels of assurance. Applying uniform enforcement to all files creates unnecessary friction for low-criticality code and potentially insufficient rigor for high-criticality code.

**Proposed Classification**:
```
Class A (HARD enforcement):
  - src/domain/**
  - src/shared_kernel/**
  - src/application/handlers/**

Class B (MEDIUM enforcement):
  - src/application/ports/**
  - src/application/commands/**
  - src/application/queries/**
  - src/infrastructure/**

Class C (SOFT enforcement):
  - src/interface/**
  - scripts/**

Class D (ADVISORY only):
  - tests/**
  - docs/**
  - projects/**
```

**Effort**: 1-2 days
**Risk**: Classification may need revision as codebase evolves
**Mitigation**: Store classification in a configuration file; review quarterly

### Recommendation 4: Implement VCRM for Quality Requirements (MEDIUM PRIORITY)

**Rationale**: Jerry has acceptance criteria scattered across FEAT-005, EN-401 through EN-406, and various task files. A Verification Cross-Reference Matrix (VCRM) provides a single source of truth that maps every requirement to its verification method, verification artifact, and current verification status.

**Effort**: 1-2 days (template + initial population)
**Risk**: VCRM maintenance overhead
**Mitigation**: Automate VCRM updates via PostToolUse hooks

### Recommendation 5: Add Property-Based Testing to Domain Layer (MEDIUM PRIORITY)

**Rationale**: Jerry's domain layer (value objects, state machines, aggregates) has well-defined invariants that are ideal candidates for property-based testing. Adding Hypothesis to the test suite provides mathematically rigorous testing of domain logic.

**Effort**: 2-3 days
**Risk**: Hypothesis test execution time
**Mitigation**: Run property-based tests only in CI, not in pre-commit

### Recommendation 6: Implement Formal Waiver Process (LOW PRIORITY)

**Rationale**: Safety-critical systems recognize that rigid enforcement without exception mechanisms leads to workarounds. A formal waiver process provides a documented, auditable way to grant exceptions when justified.

**Effort**: 1 day
**Risk**: Waivers could become too easy to obtain
**Mitigation**: Require user approval for all waivers; expire waivers after single use

### Architecture Integration Map

```
┌──────────────────────────────────────────────────────────────────────┐
│                     Jerry Enforcement Architecture                    │
│                     (Enhanced with Alternative Approaches)            │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Layer 0: File Classification (NASA-STD-8739.8)                     │
│  ┌──────────┬──────────┬──────────┬──────────┐                      │
│  │ Class A  │ Class B  │ Class C  │ Class D  │                      │
│  │ HARD     │ MEDIUM   │ SOFT     │ ADVISORY │                      │
│  └──────────┴──────────┴──────────┴──────────┘                      │
│                                                                      │
│  Layer 1: Rules (.claude/rules/) -- Always present in context        │
│                                                                      │
│  Layer 2: MCP Enforcement Server -- Protocol-level enforcement       │
│  ┌──────────┬──────────┬──────────┬──────────┐                      │
│  │ Tools    │Resources │ Prompts  │  Audit   │                      │
│  └──────────┴──────────┴──────────┴──────────┘                      │
│                                                                      │
│  Layer 3: Hooks -- Lifecycle interception                            │
│  ┌──────────┬──────────┬──────────┬──────────┐                      │
│  │UserPrompt│PreToolUse│PostTool  │  Stop    │                      │
│  │ Submit   │+ AST     │Use       │          │                      │
│  └──────────┴──────────┴──────────┴──────────┘                      │
│                                                                      │
│  Layer 4: Runtime State Machine -- Workflow enforcement              │
│  ┌──────────────────────────────────────────┐                       │
│  │ PLAN -> RESEARCH -> IMPLEMENT -> TEST    │                       │
│  │   -> REVIEW -> REVISE -> COMPLETE        │                       │
│  └──────────────────────────────────────────┘                       │
│                                                                      │
│  Layer 5: Pre-Commit / CI Gates -- Last line of defense              │
│  ┌──────────┬──────────┬──────────┐                                 │
│  │ Quality  │Coverage  │ VCRM     │                                 │
│  │ Artifacts│ Check    │ Verify   │                                 │
│  └──────────┴──────────┴──────────┘                                 │
│                                                                      │
│  Layer 6: IV&V -- Independent verification                           │
│  ┌──────────┬──────────┬──────────┐                                 │
│  │ Property │ Formal   │ FMEA     │                                 │
│  │ Testing  │ Spec     │ Analysis │                                 │
│  └──────────┴──────────┴──────────┘                                 │
│                                                                      │
│  Cross-Cutting: Audit Trail + Enforcement Failure Reporting          │
│  ┌──────────────────────────────────────────┐                       │
│  │ MCP Audit Log + PostToolUse Logging      │                       │
│  │ + Enforcement Failure Reports (EFR)      │                       │
│  │ + Formal Waiver Process                  │                       │
│  └──────────────────────────────────────────┘                       │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Sources and References

### MCP / Protocol

| # | Source | Key Finding |
|---|--------|-------------|
| 1 | Model Context Protocol Python SDK (Context7 library: `/modelcontextprotocol/python-sdk`, reputation: HIGH, score: 85.5, 417 snippets) | MCP server architecture with tools, resources, and prompts |
| 2 | Anthropic MCP Specification (https://spec.modelcontextprotocol.io) | JSON-RPC protocol for tool wrapping and resource provision |
| 3 | MCP for Beginners (Context7 library: `/microsoft/mcp-for-beginners`, reputation: HIGH, score: 64.7, 8684 snippets) | MCP educational curriculum covering enforcement patterns |

### AST / Static Analysis

| # | Source | Key Finding |
|---|--------|-------------|
| 4 | Python `ast` module documentation (https://docs.python.org/3/library/ast.html) | Standard library AST parsing and analysis |
| 5 | Tree-sitter project (https://tree-sitter.github.io/tree-sitter/) | Universal incremental parser for multi-language analysis |
| 6 | Jerry codebase: `tests/architecture/test_composition_root.py` | Existing AST-based import boundary validation |
| 7 | Jerry codebase: `tests/architecture/test_session_hook_architecture.py` | Existing architecture test infrastructure |

### Formal Methods

| # | Source | Key Finding |
|---|--------|-------------|
| 8 | Pnueli, A. "The temporal logic of programs" (1977, FOCS) | Foundational temporal logic for program verification |
| 9 | Clarke, E.M., Grumberg, O., Peled, D.A. "Model Checking" (MIT Press, 1999) | Model checking theory and practice |
| 10 | Meyer, B. "Object-Oriented Software Construction" (Prentice Hall, 1997) | Design by Contract |
| 11 | Claessen, K. and Hughes, J. "QuickCheck: A Lightweight Tool for Random Testing" (2000, ICFP) | Property-based testing |
| 12 | MacIver, D. et al. "Hypothesis" (2019, JOSS) | Python property-based testing |

### Cross-Platform

| # | Source | Key Finding |
|---|--------|-------------|
| 13 | OpenAI Assistants API documentation (https://platform.openai.com/docs/assistants) | Function calling constraints, code interpreter sandbox |
| 14 | Amazon Bedrock Guardrails documentation (https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html) | Content filtering, contextual grounding, denied topics |
| 15 | Google Gemini API documentation (https://ai.google.dev/docs) | Safety settings, system instruction protection |

### Novel Research

| # | Source | Key Finding |
|---|--------|-------------|
| 16 | Bai et al., "Constitutional AI" (2022, Anthropic, arXiv:2212.08073) | Self-critique against explicit principles |
| 17 | Irving, G., Christiano, P., Amodei, D. "AI safety via debate" (2018, arXiv:1805.00899) | Adversarial debate as alignment mechanism |
| 18 | Leike, J. et al. "Scalable agent alignment via reward modeling" (2018, arXiv:1811.07871) | Recursive reward modeling |
| 19 | Wu et al., "AutoGen" (2023, Microsoft Research) | Multi-agent governance patterns |

### NASA / Safety-Critical Standards

| # | Source | Key Finding |
|---|--------|-------------|
| 20 | NASA NPR 7123.1D "Systems Engineering Processes and Requirements" (2020) | IV&V, gate reviews, VCRM, configuration management |
| 21 | NASA NPR 7150.2D "Software Engineering Requirements" (2021) | IV&V requirements, peer review, traceability |
| 22 | NASA-STD-8739.8B "Software Assurance and Software Safety Standard" (2022) | Software classification (A-D), assurance levels, coverage requirements |
| 23 | NASA NPR 8705.6 "Safety and Mission Assurance Policy" (2021) | Problem/failure reporting, configuration management, risk management |
| 24 | NASA-HDBK-1009A "Systems Engineering Handbook" | Implementation guidance for NPR 7123.1D |
| 25 | RTCA DO-178C "Software Considerations in Airborne Systems" (2011) | Objective-based verification, independent QA |
| 26 | ISO 26262:2018 "Road vehicles -- Functional safety" | ASIL classification, work product verification |
| 27 | IEC 61508:2010 "Functional safety of electrical/electronic/programmable electronic safety-related systems" | SIL classification, safety lifecycle |
| 28 | SAE J1739 "FMEA in Design and Manufacturing" (2009) | FMEA methodology |

### Jerry Internal References

| # | Source | Path | Used For |
|---|--------|------|----------|
| 29 | Jerry Constitution | `docs/governance/JERRY_CONSTITUTION.md` | Enforcement tiers, principles |
| 30 | Architecture tests | `tests/architecture/test_composition_root.py` | Existing AST infrastructure |
| 31 | Session hook tests | `tests/architecture/test_session_hook_architecture.py` | Hook boundary enforcement |
| 32 | PreToolUse hook | `scripts/pre_tool_use.py` | Current security enforcement |
| 33 | Pattern library | `scripts/patterns/loader.py` | Regex-based pattern validation |
| 34 | Hooks configuration | `hooks/hooks.json` | Current hook architecture |
| 35 | TASK-001 research | `EN-401.../deliverable-001-claude-code-hooks-research.md` | Hooks API capabilities |
| 36 | TASK-002 research | `EN-401.../deliverable-002-guardrail-frameworks-research.md` | Industry guardrail frameworks |

---

## Disclaimer

This research was generated by the nse-explorer agent operating within the Jerry Framework with a NASA Systems Engineering perspective. The following limitations apply:

1. **Web access was unavailable**: WebSearch, WebFetch, and Context7 query-docs tools were denied during this research session. All external references are sourced from training data (cutoff: May 2025) and from the Jerry codebase. The MCP Python SDK library was resolved via Context7 (confirming its existence and reputation) but documentation content could not be retrieved.

2. **Cross-platform API details may be outdated**: OpenAI Assistants API, Amazon Bedrock Guardrails, and Google Gemini Safety Settings evolve rapidly. The details provided reflect pre-May 2025 documentation. Specific API parameters, configuration options, and feature availability should be verified against current documentation before implementation.

3. **MCP enforcement server is conceptual**: The MCP server code examples are architectural proposals, not production-ready implementations. They require proper error handling, testing, security review, and integration with Jerry's existing infrastructure.

4. **NASA standard references are from established versions**: NASA NPR 7123.1D (2020), NASA-STD-8739.8B (2022), and other standards referenced are the versions known through training data. These standards are periodically updated; verify current versions before formal compliance claims.

5. **Confidence levels vary by section**: MCP enforcement and AST analysis (medium-high confidence -- based on well-documented open-source projects). Cross-platform enforcement (medium confidence -- APIs evolve rapidly). Novel research (medium confidence -- emerging field). NASA SE analogies (high confidence -- established standards with decades of validation).

6. **Quality review required**: This research has NOT been through the adversarial creator-critic-revision cycle. Per EPIC-002's requirements, this document should undergo adversarial review (TASK-008 through TASK-011) before acting on its findings.

---

*Document Version: 1.0.0*
*Classification: Research*
*Author: nse-explorer (v2.2.0, Claude Opus 4.6)*
*NASA SE Framework: NPR 7123.1D, NASA-STD-8739.8B, NPR 7150.2D*
*Constitutional Compliance: P-001 (Truth), P-002 (Persistence), P-004 (Provenance), P-022 (No Deception)*
*Word Count: ~8,500*
*Distinct Alternative Approaches Identified: 18 (across 7 families)*
*Cross-Platform Analysis: 3 platforms (OpenAI, Amazon, Google)*
*NASA SE Standards Referenced: 7 (NPR 7123.1D, NPR 7150.2D, NASA-STD-8739.8B, NPR 8705.6, DO-178C, ISO 26262, IEC 61508)*
*Citations: 36*
