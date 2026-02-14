# TASK-004: SessionStart Hook Architecture Design

<!--
DOCUMENT-ID: FEAT-005:EN-403:TASK-004
TEMPLATE: Architecture Design
VERSION: 1.0.0
AGENT: ps-architect (Claude Opus 4.6)
DATE: 2026-02-13
PARENT: EN-403 (Hook-Based Enforcement Implementation)
FEATURE: FEAT-005 (Quality Framework Enforcement Mechanisms)
EPIC: EPIC-002 (Quality Framework Enforcement)
PROJECT: PROJ-001-oss-release
QUALITY-TARGET: >= 0.92
CONSUMERS: TASK-007 (implementation), TASK-008 (code review), TASK-009 (adversarial review)
REQUIREMENTS-COVERED: REQ-403-050 through REQ-403-055, REQ-403-060, REQ-403-070/071, REQ-403-075-078, REQ-403-080-082, REQ-403-094/095/096
-->

> **Version:** 1.0.0
> **Agent:** ps-architect (Claude Opus 4.6)
> **Status:** COMPLETE
> **Created:** 2026-02-13
> **Layer:** L1 (Static Context -- Enhancement)
> **Primary Vector:** V-003 (SessionStart Injection)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Mission](#mission) | What these enhancements do and why they matter |
| [Current Implementation Analysis](#current-implementation-analysis) | What the existing SessionStart hook already does |
| [Architecture Overview](#architecture-overview) | High-level design with hexagonal layers |
| [Quality Context Design](#quality-context-design) | What quality framework content to inject |
| [Integration with Existing Hook](#integration-with-existing-hook) | How enhancements fit into the current SessionStart flow |
| [L2 Coordination](#l2-coordination) | How SessionStart and UserPromptSubmit work together |
| [Adversarial Strategy Integration](#adversarial-strategy-integration) | S-014, S-007 touchpoint design |
| [Decision Criticality Defaults](#decision-criticality-defaults) | Initial C1-C4 assessment |
| [Token Budget Contribution](#token-budget-contribution) | Impact on the 12,476 token L1 target |
| [Error Handling](#error-handling) | Fail-open behavior |
| [Platform Adaptation](#platform-adaptation) | Non-Claude-Code platform considerations |
| [File Layout](#file-layout) | Where new and modified code lives |
| [Interface Contracts](#interface-contracts) | Output schema changes |
| [Testing Strategy](#testing-strategy) | How to verify the design |
| [Requirements Coverage](#requirements-coverage) | Which requirements this design satisfies |
| [References](#references) | Source documents |

---

## Mission

The SessionStart hook enhancement adds **quality framework context injection** to the existing session initialization flow. This provides the L1 behavioral foundation that L2 (UserPromptSubmit) subsequently reinforces throughout the session.

**Role in the defense-in-depth architecture:**

```
Session starts
    │
    ├── L1: SessionStart injects quality context (THIS ENHANCEMENT)
    │   └── Quality gate (0.92), constitutional principles, creator-critic-revision
    │
    ├── L1: .claude/rules/ loaded by Claude Code (existing)
    │   └── Architecture standards, coding standards, testing standards
    │
    └── L2: UserPromptSubmit reinforces critical rules (TASK-002)
        └── Re-injects on every prompt to counteract L1 degradation
```

**The relationship between SessionStart (L1) and UserPromptSubmit (L2):**
- **SessionStart** provides the **comprehensive** quality context at session start when the context window is clean and attention is maximal
- **UserPromptSubmit** provides **ultra-compact** reinforcement (~600 tokens) on every prompt to sustain critical rules as the context degrades

SessionStart can afford to be more detailed and explanatory because it fires once when comprehension is highest. UserPromptSubmit must be ultra-compact because it fires on every prompt and is constrained to 600 tokens.

---

## Current Implementation Analysis

The existing SessionStart hook (`scripts/session_start_hook.py`) performs:

1. **Environment setup:** Find `uv`, sync dependencies
2. **CLI invocation:** Run `jerry --json projects context`
3. **Output formatting:** Transform CLI JSON to hook JSON with `systemMessage` and `additionalContext`
4. **Project context:** Three cases -- valid project, invalid project, no project set
5. **Pre-commit check:** Warn if pre-commit hooks are not installed

**Current output structure:**

```
systemMessage: "Jerry Framework: Project PROJ-001-oss-release active"
additionalContext:
    "Jerry Framework initialized. See CLAUDE.md for context.
    <project-context>
    ProjectActive: PROJ-001-oss-release
    ProjectPath: /path/to/project
    ValidationMessage: Project is properly configured
    </project-context>
    <dev-environment-warning>  (optional)
    Pre-commit hooks are NOT installed...
    </dev-environment-warning>"
```

**What is missing (the gap this design fills):**
1. No quality framework context (0.92 threshold, scoring rubric)
2. No constitutional principles summary
3. No adversarial review cycle requirements
4. No decision criticality defaults
5. No strategy availability awareness

**Design constraint:** The enhancement must **complement** the existing project context resolution without breaking any existing functionality (REQ-403-053). Quality context is additive content appended to the `additionalContext` field.

---

## Architecture Overview

### Enhancement Strategy: Additive Content Injection

Rather than modifying the existing hook's core logic, the enhancement adds a **quality context generation module** that produces additional content to append to the hook's `additionalContext` output.

```
┌──────────────────────────────────────────────────────────────┐
│            EXISTING SESSION START FLOW                        │
│                                                              │
│  scripts/session_start_hook.py                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ 1. Find uv, sync deps                              │    │
│  │ 2. Run jerry --json projects context                │    │
│  │ 3. Parse CLI JSON                                   │    │
│  │ 4. format_hook_output() -> (systemMsg, addlContext) │    │
│  │ 5. Check pre-commit hooks                           │    │
│  │ 6. output_json(systemMsg, addlContext)               │    │
│  └──────────────────┬──────────────────────────────────┘    │
│                     │                                        │
│                     ▼                                        │
│            QUALITY CONTEXT ENHANCEMENT (NEW)                 │
│                                                              │
│  src/infrastructure/internal/enforcement/                     │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ session_quality_context.py                          │    │
│  │                                                     │    │
│  │   class SessionQualityContextGenerator:             │    │
│  │     def generate() -> str                           │    │
│  │                                                     │    │
│  │   Produces XML-tagged quality context:              │    │
│  │   - <quality-framework>                             │    │
│  │   -   Quality gate threshold                        │    │
│  │   -   Constitutional principles                     │    │
│  │   -   Creator-critic-revision cycle                 │    │
│  │   -   Decision criticality defaults                 │    │
│  │   -   Adversarial strategy availability             │    │
│  │   - </quality-framework>                            │    │
│  └─────────────────────────────────────────────────────┘    │
│                     │                                        │
│                     ▼                                        │
│  Modified session_start_hook.py:                             │
│  additionalContext = project_context + quality_context        │
└──────────────────────────────────────────────────────────────┘
```

### Why Additive, Not Replacement

1. **Risk minimization:** The existing SessionStart hook is battle-tested and handles complex cases (project validation, error formatting). Rewriting it risks regression.
2. **Clear separation of concerns:** Project context (existing) and quality context (new) are independent concerns. They can be developed, tested, and maintained separately.
3. **Incremental deployment:** The quality context module can be deployed without modifying the existing hook's core logic. If the module fails, the existing hook continues to work.

---

## Quality Context Design

### Content Specification

The quality context block is injected as a structured XML section within `additionalContext`:

```xml
<quality-framework version="1.0">
  <quality-gate>
    Target: >= 0.92 for all deliverables.
    Scoring: Use S-014 (LLM-as-Judge) with dimension-level rubrics.
    Known bias: S-014 has leniency bias. Score critically -- 0.92 means genuinely excellent.
    Cycle: Creator -> Critic -> Revision (minimum 3 iterations). Do not bypass.
  </quality-gate>

  <constitutional-principles>
    HARD constraints (cannot be overridden):
    - P-003: No recursive subagents. Max ONE level: orchestrator -> worker.
    - P-020: User authority. User decides. Never override. Ask before destructive ops.
    - P-022: No deception. Never deceive about actions, capabilities, or confidence.
    Python: UV only. Never use python/pip directly. Use 'uv run'.
  </constitutional-principles>

  <adversarial-strategies>
    Available strategies for quality enforcement:
    - S-014 (LLM-as-Judge): Rubric-based scoring. Use for all deliverables.
    - S-007 (Constitutional AI): Principle-by-principle review. Check .claude/rules/.
    - S-010 (Self-Refine): Self-review before presenting outputs. Apply always.
    - S-003 (Steelman): Charitable reconstruction before critique.
    - S-002 (Devil's Advocate): Strongest counterargument to prevailing conclusion.
    - S-013 (Inversion): Ask "how could this fail?" before proposing.
    - S-004 (Pre-Mortem): "Imagine it failed -- why?" for planning tasks.
    - S-012 (FMEA): Systematic failure mode enumeration for architecture.
    - S-011 (CoVe): Factual verification for claims and documentation.
    - S-001 (Red Team): Adversary simulation for security-sensitive work.
  </adversarial-strategies>

  <decision-criticality>
    Assess every task's criticality:
    - C1 (Routine): Reversible, < 3 files, no external deps -> Self-Check only
    - C2 (Standard): Reversible within 1 day, 3-10 files -> Standard Critic
    - C3 (Significant): > 1 day to reverse, > 10 files, API changes -> Deep Review
    - C4 (Critical): Irreversible, architecture/governance changes -> Tournament Review
    AUTO-ESCALATE: Any change to docs/governance/ or .claude/rules/ is C3 or higher.
  </decision-criticality>
</quality-framework>
```

### Content Design Principles

1. **Detailed at session start:** Unlike V-024 (600 token budget), SessionStart context can be more comprehensive because it fires once when the context window is clean and attention is maximal.
2. **Reference-oriented:** Points Claude to `.claude/rules/` for full details rather than duplicating rule content. The quality context provides the framework; the rules provide the specifics.
3. **Structured with XML tags:** Each section is independently parseable by Claude (REQ-403-094).
4. **Actionable:** Content is phrased as instructions ("Score all deliverables", "Assess every task's criticality") not descriptions.

### Token Estimate

| Section | Estimated Tokens |
|---------|-----------------|
| `<quality-gate>` | ~80 |
| `<constitutional-principles>` | ~65 |
| `<adversarial-strategies>` | ~120 |
| `<decision-criticality>` | ~85 |
| XML wrapper and version | ~10 |
| **Total** | **~360 tokens** |

This contributes ~360 tokens to the L1 Static Context budget. Per REQ-403-055, this must fit within the 12,476 token L1 target from ADR-EPIC002-002.

---

## Integration with Existing Hook

### Modification Points

The existing `session_start_hook.py` requires **two changes**:

#### Change 1: Import Quality Context Generator

```python
# Add near the top of session_start_hook.py, after existing imports
try:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src.infrastructure.internal.enforcement.session_quality_context import (
        SessionQualityContextGenerator,
    )
    QUALITY_CONTEXT_AVAILABLE = True
except ImportError:
    QUALITY_CONTEXT_AVAILABLE = False
```

#### Change 2: Append Quality Context in `main()`

```python
# In main(), after format_hook_output() and before output_json()

        # Generate quality framework context (NEW)
        quality_context = ""
        if QUALITY_CONTEXT_AVAILABLE:
            try:
                generator = SessionQualityContextGenerator()
                quality_context = generator.generate()
            except Exception as e:
                log_error(log_file, f"WARNING: Quality context generation failed: {e}")
                quality_context = ""  # Fail-open

        # Append quality context to additional context
        if quality_context:
            additional_context = additional_context + "\n\n" + quality_context

        # Transform to hook format (existing)
        output_json(system_message, additional_context)
```

### Integration Flow

```
session_start_hook.py main()
       │
       ├── Find uv, sync deps (existing)
       ├── Run jerry --json projects context (existing)
       ├── Parse CLI JSON (existing)
       ├── format_hook_output() -> (systemMsg, additionalContext) (existing)
       ├── Check pre-commit hooks (existing)
       │
       ├── Generate quality context (NEW)
       │   ├── Try import SessionQualityContextGenerator
       │   ├── If available: generator.generate()
       │   └── If error: log + empty string (fail-open)
       │
       ├── Append quality context to additionalContext (NEW)
       │
       └── output_json(systemMsg, additionalContext) (existing)
```

### What Does NOT Change

- Project context resolution (valid/invalid/no project)
- Pre-commit hook warning
- Error handling for uv/CLI failures
- `systemMessage` content (user-visible)
- Hook JSON output structure

---

## L2 Coordination

### SessionStart (L1) Provides, UserPromptSubmit (L2) Reinforces

The two hooks form a coordinated pair:

| Aspect | SessionStart (L1) | UserPromptSubmit (L2) |
|--------|-------------------|----------------------|
| **Fires** | Once per session | Every prompt |
| **Token budget** | ~360 tokens (one-time) | ~600 tokens (amortized) |
| **Content depth** | Comprehensive (full strategy list, detailed criteria) | Ultra-compact (key reminders only) |
| **Content focus** | Framework and reference material | Critical rules and thresholds |
| **Context rot** | VULNERABLE (degrades over session) | IMMUNE (re-injected every prompt) |
| **Purpose** | Establish baseline understanding | Sustain critical rules |

### Content Overlap

Some content appears in both hooks:
- **0.92 quality threshold:** SessionStart provides context; UserPromptSubmit reinforces the number
- **Constitutional principles:** SessionStart lists key principles; UserPromptSubmit reminds of them
- **Self-review (S-010):** SessionStart lists it as available; UserPromptSubmit reminds to apply it

This overlap is **intentional** and part of the defense-in-depth design. The SessionStart context may degrade, but the UserPromptSubmit reinforcement ensures the most critical elements survive.

### Content Non-Overlap

Some content is only in SessionStart:
- Full adversarial strategy list (S-001 through S-014) -- too large for V-024 budget
- Decision criticality framework (C1-C4 with detailed criteria) -- reference material
- Scoring methodology details -- one-time establishment

Some content is only in UserPromptSubmit:
- Leniency bias calibration for S-014 -- relevant when scoring is active
- Steelman reminder -- relevant when review is expected
- Deep-review escalation -- relevant at C3+

---

## Adversarial Strategy Integration

### S-014 (LLM-as-Judge) -- Session Initialization

**Integration:** The `<quality-gate>` section injects the scoring framework including:
- The 0.92 threshold (the central quality target)
- S-014 as the scoring mechanism (rubric-based evaluation)
- Leniency bias awareness (R-014-FN calibration)
- Creator-critic-revision cycle (minimum 3 iterations)

**Rationale:** S-014 functions as the scoring backbone for quality gates. Establishing the scoring framework at session start ensures Claude has the full context before any scoring is needed. The UserPromptSubmit hook then reinforces the threshold value on every prompt.

### S-007 (Constitutional AI) -- Session Initialization

**Integration:** The `<constitutional-principles>` section injects the three HARD constitutional constraints (P-003, P-020, P-022) plus the Python/UV environment rule.

**Rationale:** The constitution is the foundation for all enforcement. Loading it at session start establishes the behavioral baseline. Only the most critical principles are listed (keeping the section compact); Claude is directed to `.claude/rules/` for the complete rule set.

**Selection criteria for included principles:** Only principles with "HARD" enforcement level and "Violations will be blocked" status are included. These are the principles most critical to reinforce.

---

## Decision Criticality Defaults

### Initial Assessment Context

The `<decision-criticality>` section provides Claude with the C1-C4 framework and assessment criteria. This enables Claude to self-assess criticality for each task.

### Auto-Escalation Rules

The SessionStart context establishes the auto-escalation rule:

> **AUTO-ESCALATE:** Any change to `docs/governance/` or `.claude/rules/` is C3 or higher.

This rule is enforced at two layers:
1. **L1 (SessionStart):** Claude is aware of the rule from session start
2. **L3 (PreToolUse):** The PreToolUse hook deterministically enforces the escalation (REQ-403-061)

The dual enforcement provides defense-in-depth: if Claude forgets the rule under context rot (L1 failure), the PreToolUse hook (L3) catches the violation.

---

## Token Budget Contribution

### Analysis

| Component | Tokens |
|-----------|--------|
| Quality context (this enhancement) | ~360 |
| Existing project context | ~150 |
| Pre-commit warning (when present) | ~80 |
| **Total SessionStart contribution to L1** | **~510-590** |

Per ADR-EPIC002-002, the L1 target is ~12,476 tokens. The SessionStart hook contributes ~590 tokens, which is **4.7%** of the L1 budget. The remaining ~11,886 tokens are consumed by `.claude/rules/` files loaded by Claude Code at session start.

This contribution is well within budget and leaves ample room for the rules files.

### Budget Sensitivity

If the rules optimization effort (25,700 down to 12,476 tokens) requires tighter budgets, the SessionStart quality context can be trimmed by:
1. Removing the full strategy list (saves ~120 tokens)
2. Condensing decision criticality to a single line (saves ~65 tokens)
3. Minimum viable: quality gate + constitutional principles = ~145 tokens

---

## Error Handling

### Fail-Open Design (REQ-403-070)

The quality context generation is wrapped in a try/except with fail-open behavior:

```python
try:
    generator = SessionQualityContextGenerator()
    quality_context = generator.generate()
except Exception as e:
    log_error(log_file, f"WARNING: Quality context generation failed: {e}")
    quality_context = ""  # Fail-open: no quality context, but session proceeds
```

**What happens on failure:**
1. The error is logged to the hook error log (REQ-403-071)
2. No quality context is appended
3. The existing project context continues to function normally
4. The session starts without quality framework context
5. The UserPromptSubmit hook (L2) still fires and provides basic reinforcement

**Failure does NOT cascade:** Even if SessionStart quality context fails, the UserPromptSubmit hook operates independently. L2 enforcement is not dependent on L1 having successfully loaded quality context.

### ImportError Handling

The `QUALITY_CONTEXT_AVAILABLE` flag ensures that if the quality context module is not yet deployed, the existing hook behavior is completely unchanged. This enables:
- Incremental deployment (module can be added independently)
- Safe rollback (removing the module restores original behavior)
- Development environment compatibility (module may not be available in all environments)

---

## Platform Adaptation

### Claude Code (Primary Platform)

On Claude Code, the SessionStart hook fires automatically at session initialization. The `additionalContext` field injects quality framework context into Claude's context window alongside the project context.

### Non-Claude-Code Platforms

Per REQ-403-077, the quality context generator is importable as a standalone library:

```python
# Example: Non-Claude-Code session initialization
from src.infrastructure.internal.enforcement.session_quality_context import (
    SessionQualityContextGenerator,
)

generator = SessionQualityContextGenerator()
quality_context = generator.generate()

# Platform-specific injection
inject_into_system_prompt(quality_context)
```

**Alternative integration paths:**
1. **Cursor/Windsurf:** Add quality context to custom instructions or project rules
2. **Generic LLM API:** Prepend quality context to the system message
3. **MCP-based platforms:** Use MCP tool context injection when available
4. **Manual:** Copy the quality context block and paste it into the first message of a session

The quality context is pure text with XML tags. It has no platform dependencies.

---

## File Layout

### New Files

| File | Layer | Purpose |
|------|-------|---------|
| `src/infrastructure/internal/enforcement/session_quality_context.py` | Infrastructure | Quality context generator |
| `tests/unit/enforcement/test_session_quality_context.py` | Test | Unit tests for generator |

### Modified Files

| File | Change |
|------|--------|
| `scripts/session_start_hook.py` | Add quality context import and append logic |

### Detailed Component: `session_quality_context.py`

```python
"""Session quality context generator for SessionStart hook.

Generates quality framework context to inject at session
initialization. This content establishes the L1 behavioral
foundation that L2 (UserPromptSubmit) subsequently reinforces.
"""
from __future__ import annotations


class SessionQualityContextGenerator:
    """Generates quality framework context for session start.

    The generated content includes:
    - Quality gate threshold and scoring requirements
    - Constitutional principles summary
    - Available adversarial strategies
    - Decision criticality framework

    The generator is stateless and produces identical output
    on every invocation (content is static by design).
    """

    VERSION: str = "1.0"

    def generate(self) -> str:
        """Generate the quality framework context block.

        Returns:
            XML-tagged quality context string.
        """
        sections = [
            self._quality_gate_section(),
            self._constitutional_section(),
            self._strategies_section(),
            self._criticality_section(),
        ]

        return (
            f'<quality-framework version="{self.VERSION}">\n'
            + "\n\n".join(sections)
            + "\n</quality-framework>"
        )

    def _quality_gate_section(self) -> str:
        """Generate quality gate section."""
        return (
            "  <quality-gate>\n"
            "    Target: >= 0.92 for all deliverables.\n"
            "    Scoring: Use S-014 (LLM-as-Judge) with "
            "dimension-level rubrics.\n"
            "    Known bias: S-014 has leniency bias. "
            "Score critically -- 0.92 means genuinely excellent.\n"
            "    Cycle: Creator -> Critic -> Revision "
            "(minimum 3 iterations). Do not bypass.\n"
            "  </quality-gate>"
        )

    def _constitutional_section(self) -> str:
        """Generate constitutional principles section."""
        return (
            "  <constitutional-principles>\n"
            "    HARD constraints (cannot be overridden):\n"
            "    - P-003: No recursive subagents. "
            "Max ONE level: orchestrator -> worker.\n"
            "    - P-020: User authority. User decides. "
            "Never override. Ask before destructive ops.\n"
            "    - P-022: No deception. Never deceive about "
            "actions, capabilities, or confidence.\n"
            "    Python: UV only. Never use python/pip directly. "
            "Use 'uv run'.\n"
            "  </constitutional-principles>"
        )

    def _strategies_section(self) -> str:
        """Generate adversarial strategies section."""
        return (
            "  <adversarial-strategies>\n"
            "    Available strategies for quality enforcement:\n"
            "    - S-014 (LLM-as-Judge): "
            "Rubric-based scoring. Use for all deliverables.\n"
            "    - S-007 (Constitutional AI): "
            "Principle-by-principle review. Check .claude/rules/.\n"
            "    - S-010 (Self-Refine): "
            "Self-review before presenting outputs. Apply always.\n"
            "    - S-003 (Steelman): "
            "Charitable reconstruction before critique.\n"
            "    - S-002 (Devil's Advocate): "
            "Strongest counterargument to prevailing conclusion.\n"
            "    - S-013 (Inversion): "
            "Ask 'how could this fail?' before proposing.\n"
            "    - S-004 (Pre-Mortem): "
            "'Imagine it failed -- why?' for planning tasks.\n"
            "    - S-012 (FMEA): "
            "Systematic failure mode enumeration for architecture.\n"
            "    - S-011 (CoVe): "
            "Factual verification for claims and documentation.\n"
            "    - S-001 (Red Team): "
            "Adversary simulation for security-sensitive work.\n"
            "  </adversarial-strategies>"
        )

    def _criticality_section(self) -> str:
        """Generate decision criticality section."""
        return (
            "  <decision-criticality>\n"
            "    Assess every task's criticality:\n"
            "    - C1 (Routine): Reversible, < 3 files, "
            "no external deps -> Self-Check only\n"
            "    - C2 (Standard): Reversible within 1 day, "
            "3-10 files -> Standard Critic\n"
            "    - C3 (Significant): > 1 day to reverse, "
            "> 10 files, API changes -> Deep Review\n"
            "    - C4 (Critical): Irreversible, architecture/"
            "governance changes -> Tournament Review\n"
            "    AUTO-ESCALATE: Any change to docs/governance/ "
            "or .claude/rules/ is C3 or higher.\n"
            "  </decision-criticality>"
        )
```

---

## Interface Contracts

### Output Schema (Enhanced)

The hook output structure remains unchanged. The quality context is appended to the existing `additionalContext` string:

```json
{
    "systemMessage": "Jerry Framework: Project PROJ-001-oss-release active",
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": "Jerry Framework initialized. See CLAUDE.md for context.\n<project-context>\nProjectActive: PROJ-001-oss-release\n...\n</project-context>\n\n<quality-framework version=\"1.0\">\n  <quality-gate>\n    Target: >= 0.92 for all deliverables.\n    ...\n  </quality-gate>\n  ...\n</quality-framework>"
    }
}
```

The `systemMessage` is NOT modified. The quality context is invisible to the user terminal output -- it only appears in Claude's context window via `additionalContext`.

### Internal Interface

```python
class SessionQualityContextGenerator:
    VERSION: str = "1.0"
    def generate(self) -> str:
        """Returns XML-tagged quality framework context string."""
```

The interface is deliberately simple: no parameters needed because the content is static. If future requirements add dynamic content (e.g., project-specific quality thresholds), the interface can be extended with optional parameters without breaking existing callers.

---

## Testing Strategy

### Unit Tests

| Test | File | Validates |
|------|------|-----------|
| `test_generate_returns_xml_tagged_content` | `test_session_quality_context.py` | REQ-403-094 |
| `test_quality_gate_includes_092_threshold` | `test_session_quality_context.py` | REQ-403-050 |
| `test_quality_gate_includes_scoring_requirement` | `test_session_quality_context.py` | REQ-403-050 (S-014) |
| `test_quality_gate_includes_leniency_bias` | `test_session_quality_context.py` | REQ-403-050 |
| `test_quality_gate_includes_creator_critic_revision` | `test_session_quality_context.py` | REQ-403-052 |
| `test_constitutional_includes_p003_p020_p022` | `test_session_quality_context.py` | REQ-403-051 |
| `test_strategies_lists_all_10_selected` | `test_session_quality_context.py` | REQ-403-051 |
| `test_criticality_includes_c1_through_c4` | `test_session_quality_context.py` | REQ-403-054 |
| `test_criticality_includes_auto_escalation` | `test_session_quality_context.py` | REQ-403-054, REQ-403-060 |
| `test_token_estimate_within_budget` | `test_session_quality_context.py` | REQ-403-055 |
| `test_generator_is_stateless` | `test_session_quality_context.py` | REQ-403-081 |
| `test_generator_uses_no_external_imports` | `test_session_quality_context.py` | REQ-403-075 |

### Integration Tests

| Test | Validates |
|------|-----------|
| Modified `session_start_hook.py` includes quality context in output | REQ-403-050, REQ-403-051 |
| Modified hook preserves existing project context output | REQ-403-053 |
| Modified hook fails-open when generator module unavailable | REQ-403-070 |
| Modified hook fails-open when generator raises exception | REQ-403-070, REQ-403-071 |

### Contract Tests

| Test | Validates |
|------|-----------|
| Hook output JSON is valid and parseable | Interface contract |
| `additionalContext` contains both `<project-context>` and `<quality-framework>` tags | REQ-403-094 |
| `systemMessage` is unchanged from existing behavior | REQ-403-053 |

---

## Requirements Coverage

| Requirement | Covered By |
|-------------|-----------|
| REQ-403-050 | `_quality_gate_section()` includes 0.92 threshold |
| REQ-403-051 | `_constitutional_section()` includes P-003, P-020, P-022; `_strategies_section()` includes S-007 |
| REQ-403-052 | `_quality_gate_section()` includes "Creator -> Critic -> Revision" |
| REQ-403-053 | Additive design; existing format_hook_output() unchanged |
| REQ-403-054 | `_criticality_section()` includes C1-C4 defaults |
| REQ-403-055 | ~360 tokens within L1 budget (4.7% of 12,476) |
| REQ-403-060 | `_criticality_section()` includes C1-C4 framework |
| REQ-403-070 | try/except with empty string fallback |
| REQ-403-071 | log_error() on failure |
| REQ-403-075 | No imports beyond stdlib (no imports at all in generator) |
| REQ-403-076 | N/A (no file path operations in generator) |
| REQ-403-077 | Generator importable as standalone library |
| REQ-403-078 | N/A (no file reads in generator) |
| REQ-403-080 | Generator in infrastructure/internal/enforcement/ |
| REQ-403-081 | Stateless generator with typed returns |
| REQ-403-082 | session_start_hook.py is thin adapter |
| REQ-403-094 | XML `<quality-framework>` tags |
| REQ-403-095 | Quality threshold present in SessionStart (L1) and UserPromptSubmit (L2) |
| REQ-403-096 | Creator-critic-revision cycle in quality-gate section |

---

## References

| # | Citation | Used For |
|---|----------|----------|
| 1 | ADR-EPIC002-002 v1.2.0 (ACCEPTED) | L1 layer definition, V-003 properties, token budget (12,476), defense-in-depth |
| 2 | Barrier-1 ADV-to-ENF Handoff | SessionStart strategy touchpoints (S-014, S-007), quality gate integration, decision criticality |
| 3 | EN-403 Enabler Definition v2.0.0 | FR-005/006, NFR-001/002/005 |
| 4 | TASK-001 Hook Requirements (this enabler) | REQ-403-050 through REQ-403-096 |
| 5 | TASK-002 UserPromptSubmit Design (this enabler) | L2 coordination, content overlap/non-overlap |
| 6 | `scripts/session_start_hook.py` | Existing implementation to enhance |
| 7 | `hooks/hooks.json` | Current hook registration (SessionStart) |
| 8 | EN-302 TASK-005 ADR-EPIC002-001 | Selected 10 adversarial strategies |

---

*Agent: ps-architect (Claude Opus 4.6)*
*Date: 2026-02-13*
*Parent: EN-403 Hook-Based Enforcement Implementation*
*Quality Target: >= 0.92*
*Target ACs: 4, 5, 10, 11*
