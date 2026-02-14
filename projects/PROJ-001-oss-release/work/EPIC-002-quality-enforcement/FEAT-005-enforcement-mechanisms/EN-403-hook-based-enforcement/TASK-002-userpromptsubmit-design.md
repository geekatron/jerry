# TASK-002: UserPromptSubmit Hook Architecture Design

<!--
DOCUMENT-ID: FEAT-005:EN-403:TASK-002
TEMPLATE: Architecture Design
VERSION: 1.0.0
AGENT: ps-architect (Claude Opus 4.6)
DATE: 2026-02-13
PARENT: EN-403 (Hook-Based Enforcement Implementation)
FEATURE: FEAT-005 (Quality Framework Enforcement Mechanisms)
EPIC: EPIC-002 (Quality Framework Enforcement)
PROJECT: PROJ-001-oss-release
QUALITY-TARGET: >= 0.92
CONSUMERS: TASK-005 (implementation), TASK-008 (code review), TASK-009 (adversarial review)
REQUIREMENTS-COVERED: REQ-403-010 through REQ-403-019, REQ-403-070/071, REQ-403-075-078, REQ-403-080-082, REQ-403-085, REQ-403-090/091, REQ-403-094/095/096
-->

> **Version:** 1.0.0
> **Agent:** ps-architect (Claude Opus 4.6)
> **Status:** COMPLETE
> **Created:** 2026-02-13
> **Layer:** L2 (Per-Prompt Reinforcement)
> **Primary Vectors:** V-005 (UserPromptSubmit Hook), V-024 (Context Reinforcement via Repetition)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Mission](#mission) | What this hook does and why it matters |
| [Architecture Overview](#architecture-overview) | High-level design with hexagonal layers |
| [Detailed Design](#detailed-design) | Component specifications and interfaces |
| [V-024 Content Design](#v-024-content-design) | What to inject, token budget, format |
| [Injection Strategy](#injection-strategy) | When and how to inject reinforcement content |
| [Adversarial Strategy Integration](#adversarial-strategy-integration) | S-007, S-014, S-003, S-010 touchpoint design |
| [Decision Criticality Awareness](#decision-criticality-awareness) | C1-C4 escalation logic |
| [Error Handling](#error-handling) | Fail-open behavior and logging |
| [Platform Adaptation](#platform-adaptation) | Non-Claude-Code platform fallbacks |
| [File Layout](#file-layout) | Where new code lives |
| [Interface Contracts](#interface-contracts) | Input/output schemas |
| [Testing Strategy](#testing-strategy) | How to verify the design |
| [Requirements Coverage](#requirements-coverage) | Which requirements this design satisfies |
| [References](#references) | Source documents |

---

## Mission

The UserPromptSubmit hook is the **primary L2 enforcement mechanism** in Jerry's 5-layer hybrid enforcement architecture. Its single mission is to counteract context rot in L1 (Static Context) by re-injecting critical quality framework content into the LLM context on every user prompt.

**Why this matters:** Without L2, the entire L1 rules layer (~12,476 tokens) degrades to 40-60% effectiveness beyond ~20K context tokens (Liu et al., 2023, "Lost in the Middle"). L2 is the IMMUNE-by-design compensation layer that keeps critical rules alive throughout the session regardless of context window fill level.

**Defense-in-depth role:**

```
L1 (Static Context) ──degrades at 20K+ tokens──> L2 (This Hook) re-injects critical rules
L2 (This Hook) ──LLM ignores re-injected rules──> L3 (PreToolUse) blocks deterministically
```

**Key constraint:** The entire V-024 reinforcement content budget is ~600 tokens per session. Content must be ultra-compact and focused on the highest-value reinforcement items.

---

## Architecture Overview

### Hexagonal Layer Mapping

The UserPromptSubmit hook follows Jerry's hexagonal architecture with clear separation between enforcement logic (portable, testable) and hook infrastructure (Claude Code-specific).

```
┌──────────────────────────────────────────────────────────────┐
│                    INTERFACE LAYER                            │
│                                                              │
│  hooks/user-prompt-submit.py                                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ Thin adapter:                                       │    │
│  │   1. Read JSON from stdin                           │    │
│  │   2. Invoke enforcement logic                       │    │
│  │   3. Format output as hook JSON                     │    │
│  │   4. Handle errors (fail-open)                      │    │
│  └─────────────────────────────────────────────────────┘    │
│                            │                                 │
│                            ▼                                 │
│                    APPLICATION LAYER                          │
│                                                              │
│  src/infrastructure/internal/enforcement/                     │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ prompt_reinforcement_engine.py                      │    │
│  │                                                     │    │
│  │   class PromptReinforcementEngine:                  │    │
│  │     def generate_reinforcement(                     │    │
│  │       context: PromptContext                        │    │
│  │     ) -> ReinforcementContent                       │    │
│  │                                                     │    │
│  │   - Selects reinforcement content based on context  │    │
│  │   - Applies token budget constraints                │    │
│  │   - Applies decision criticality escalation         │    │
│  │   - Composes strategy-specific reminders            │    │
│  └─────────────────────────────────────────────────────┘    │
│                            │                                 │
│                            ▼                                 │
│                    DOMAIN LAYER (Data)                        │
│                                                              │
│  src/infrastructure/internal/enforcement/                     │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ reinforcement_content.py                            │    │
│  │                                                     │    │
│  │   REINFORCEMENT_BLOCKS: dict[str, str]              │    │
│  │   - Constitutional principles block                 │    │
│  │   - Quality gate threshold block                    │    │
│  │   - Self-review reminder block                      │    │
│  │   - Leniency bias calibration block                 │    │
│  │   - Steelman reminder block                         │    │
│  │   - Pre-mortem reminder block (C3+)                 │    │
│  │                                                     │    │
│  │   TOKEN_BUDGET = 600                                │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│                    INFRASTRUCTURE LAYER                       │
│                                                              │
│  src/infrastructure/internal/enforcement/                     │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ context_provider.py                                 │    │
│  │                                                     │    │
│  │   class ContextProvider:                            │    │
│  │     def get_active_rules() -> list[str]             │    │
│  │     def get_project_context() -> ProjectInfo | None │    │
│  │     def detect_deliverable_context() -> bool        │    │
│  │     def detect_review_context() -> bool             │    │
│  └─────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────┘
```

### Design Rationale

**Why enforcement logic lives in `src/infrastructure/internal/enforcement/`:** Per the V-038 design decision in EN-402 TASK-006 (Section 1.2), enforcement utilities are internal infrastructure concerns that serve a cross-cutting role. They are placed alongside `IFileStore` and `ISerializer` implementations in the `infrastructure/internal/` directory. This decision was made to comply with the 4-layer hexagonal structure where all code resides within one of the canonical layers or `shared_kernel/`.

**Why the hook entry point lives in `hooks/`:** The hook JSON registration (`hooks/hooks.json`) points to scripts that are invoked by Claude Code. The thin adapter in `hooks/user-prompt-submit.py` handles the Claude Code-specific protocol (stdin JSON, stdout JSON) while delegating to the portable enforcement engine.

---

## Detailed Design

### Component 1: Hook Entry Point (`hooks/user-prompt-submit.py`)

**Responsibility:** Thin adapter between Claude Code hook protocol and enforcement engine.

```python
#!/usr/bin/env python3
"""UserPromptSubmit Hook -- L2 Per-Prompt Reinforcement.

Delivers V-024 context reinforcement content on every user prompt
to counteract L1 context rot.

Exit Codes:
    0 - Success (reinforcement content injected via additionalContext)
    0 - Error (fail-open: no content injected, error logged)
"""

import json
import sys
from pathlib import Path

# Add project root to path for enforcement imports
_script_dir = Path(__file__).resolve().parent
_project_root = _script_dir.parent
sys.path.insert(0, str(_project_root))

from src.infrastructure.internal.enforcement.prompt_reinforcement_engine import (
    PromptReinforcementEngine,
    PromptContext,
)


def main() -> int:
    """Main hook entry point. Always returns 0 (fail-open)."""
    try:
        # Read hook input from stdin
        input_data = json.loads(sys.stdin.read())

        # Extract prompt context
        prompt_context = PromptContext(
            user_prompt=input_data.get("user_prompt", ""),
            session_id=input_data.get("session_id", ""),
            project_dir=input_data.get("project_dir", ""),
        )

        # Generate reinforcement content
        engine = PromptReinforcementEngine()
        content = engine.generate_reinforcement(prompt_context)

        # Output hook JSON with additionalContext
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": content.rendered_text,
            }
        }))
        return 0

    except Exception as e:
        # Fail-open: log error, output empty context
        print(json.dumps({
            "warning": f"UserPromptSubmit hook error: {e}",
        }), file=sys.stderr)
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": "",
            }
        }))
        return 0


if __name__ == "__main__":
    sys.exit(main())
```

**Key design decisions:**
- **Always returns 0:** Per REQ-403-070, hook errors must never prevent the user's prompt from being submitted.
- **Empty additionalContext on error:** Per REQ-403-071, errors are logged to stderr. An empty context is injected rather than no output (which could cause protocol errors).
- **Path manipulation:** The hook adds the project root to `sys.path` to enable imports from `src/`. This is necessary because hooks execute from the `hooks/` directory.

### Component 2: Reinforcement Engine (`prompt_reinforcement_engine.py`)

**Responsibility:** Core enforcement logic. Selects, composes, and token-budgets the V-024 reinforcement content.

```python
"""Prompt reinforcement engine for V-024 context reinforcement.

Generates ultra-compact reinforcement content within the ~600 token
budget to counteract L1 context rot.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class PromptContext:
    """Input context for reinforcement generation."""
    user_prompt: str = ""
    session_id: str = ""
    project_dir: str = ""


@dataclass(frozen=True)
class ReinforcementContent:
    """Output of the reinforcement engine."""
    rendered_text: str
    token_estimate: int
    blocks_included: list[str] = field(default_factory=list)
    criticality_level: str = "C1"


class PromptReinforcementEngine:
    """Generates V-024 reinforcement content for UserPromptSubmit hook.

    Selects and composes reinforcement blocks within the token budget,
    applying decision criticality escalation when appropriate.

    The engine is stateless and deterministic: given the same
    PromptContext, it produces the same ReinforcementContent.
    """

    TOKEN_BUDGET: int = 600

    def __init__(self) -> None:
        self._content_blocks = _build_content_blocks()

    def generate_reinforcement(
        self,
        context: PromptContext,
    ) -> ReinforcementContent:
        """Generate reinforcement content within token budget.

        Args:
            context: Current prompt context information.

        Returns:
            ReinforcementContent with rendered text and metadata.
        """
        criticality = self._assess_criticality(context)
        selected_blocks = self._select_blocks(context, criticality)
        rendered = self._render(selected_blocks, criticality)
        token_est = self._estimate_tokens(rendered)

        # Trim if over budget
        if token_est > self.TOKEN_BUDGET:
            rendered, token_est, selected_blocks = self._trim_to_budget(
                selected_blocks, criticality
            )

        return ReinforcementContent(
            rendered_text=rendered,
            token_estimate=token_est,
            blocks_included=[b.block_id for b in selected_blocks],
            criticality_level=criticality,
        )

    def _assess_criticality(self, context: PromptContext) -> str:
        """Assess decision criticality from prompt context.

        Returns one of: C1, C2, C3, C4.
        Default is C2 (Standard) for most operations.
        """
        prompt_lower = context.user_prompt.lower()

        # C4: Critical -- architecture changes, governance, public release
        c4_signals = [
            "constitution", "governance", "jerry_constitution",
            "public release", "architecture decision", "adr",
        ]
        if any(signal in prompt_lower for signal in c4_signals):
            return "C4"

        # C3: Significant -- multi-file changes, API changes, rules changes
        c3_signals = [
            ".claude/rules", "rules/", "architecture",
            "breaking change", "api change", "interface change",
        ]
        if any(signal in prompt_lower for signal in c3_signals):
            return "C3"

        # C1: Routine -- simple queries, small edits
        c1_signals = [
            "read", "show", "list", "what is", "how do",
            "explain", "help",
        ]
        if any(signal in prompt_lower for signal in c1_signals):
            return "C1"

        # Default: C2 (Standard)
        return "C2"

    def _select_blocks(
        self,
        context: PromptContext,
        criticality: str,
    ) -> list[ContentBlock]:
        """Select reinforcement blocks based on context and criticality."""
        selected = []

        # Always included (S-007, S-010 are "Always" triggers)
        selected.append(self._content_blocks["quality-gate"])
        selected.append(self._content_blocks["constitutional-principles"])
        selected.append(self._content_blocks["self-review"])

        # Conditionally included
        prompt_lower = context.user_prompt.lower()

        # S-014: When deliverable expected
        deliverable_signals = [
            "implement", "create", "build", "write", "design",
            "produce", "generate", "deliver",
        ]
        if any(s in prompt_lower for s in deliverable_signals):
            selected.append(self._content_blocks["scoring-requirement"])

        # S-003: When review/critique expected
        review_signals = [
            "review", "critique", "evaluate", "assess", "audit",
            "check", "validate",
        ]
        if any(s in prompt_lower for s in review_signals):
            selected.append(self._content_blocks["steelman"])

        # Leniency bias calibration (always for scoring context)
        if self._content_blocks["scoring-requirement"] in selected:
            selected.append(self._content_blocks["leniency-calibration"])

        # C3+: Enhanced reinforcement
        if criticality in ("C3", "C4"):
            selected.append(self._content_blocks["deep-review"])

        return selected

    def _render(
        self,
        blocks: list[ContentBlock],
        criticality: str,
    ) -> str:
        """Render selected blocks into the final reinforcement text."""
        parts = [f"<enforcement-context criticality=\"{criticality}\">"]
        for block in blocks:
            parts.append(block.content)
        parts.append("</enforcement-context>")
        return "\n".join(parts)

    def _estimate_tokens(self, text: str) -> int:
        """Estimate token count. Approximation: ~4 chars per token."""
        return len(text) // 4

    def _trim_to_budget(
        self,
        blocks: list[ContentBlock],
        criticality: str,
    ) -> tuple[str, int, list[ContentBlock]]:
        """Trim blocks to fit within token budget.

        Removes lowest-priority blocks first until budget is met.
        Core blocks (quality-gate, constitutional, self-review) are
        never removed.
        """
        # Sort by priority (lower number = higher priority = kept)
        sorted_blocks = sorted(blocks, key=lambda b: b.priority)
        kept = []
        for block in sorted_blocks:
            candidate = kept + [block]
            rendered = self._render(candidate, criticality)
            if self._estimate_tokens(rendered) <= self.TOKEN_BUDGET:
                kept.append(block)
            elif block.priority <= 2:
                # Core blocks are always kept even if over budget
                kept.append(block)

        rendered = self._render(kept, criticality)
        return rendered, self._estimate_tokens(rendered), kept


@dataclass(frozen=True)
class ContentBlock:
    """A single reinforcement content block."""
    block_id: str
    content: str
    priority: int  # 1=highest, 5=lowest
    token_estimate: int


def _build_content_blocks() -> dict[str, ContentBlock]:
    """Build the static content blocks for V-024 reinforcement."""
    return {
        "quality-gate": ContentBlock(
            block_id="quality-gate",
            content=(
                "QUALITY: Target >= 0.92. Score all deliverables against rubrics. "
                "Creator-critic-revision: minimum 3 iterations."
            ),
            priority=1,
            token_estimate=30,
        ),
        "constitutional-principles": ContentBlock(
            block_id="constitutional-principles",
            content=(
                "CONSTITUTION: P-003 No recursive subagents (max 1 level). "
                "P-020 User authority (never override, ask before destructive). "
                "P-022 No deception (never deceive about actions/capabilities). "
                "P-002 Filesystem as memory (persist to files). "
                "Check .claude/rules/ for full standards."
            ),
            priority=1,
            token_estimate=65,
        ),
        "self-review": ContentBlock(
            block_id="self-review",
            content=(
                "SELF-REVIEW (S-010): Review your output for completeness, "
                "accuracy, and quality before presenting. Apply self-critique."
            ),
            priority=2,
            token_estimate=30,
        ),
        "scoring-requirement": ContentBlock(
            block_id="scoring-requirement",
            content=(
                "SCORING (S-014): Score this deliverable against defined rubrics. "
                "Provide dimension-level breakdown with justifications. "
                "Target: >= 0.92."
            ),
            priority=3,
            token_estimate=35,
        ),
        "steelman": ContentBlock(
            block_id="steelman",
            content=(
                "STEELMAN (S-003): Before critiquing, reconstruct the strongest "
                "version of the argument. Evaluate the steelmanned version."
            ),
            priority=3,
            token_estimate=30,
        ),
        "leniency-calibration": ContentBlock(
            block_id="leniency-calibration",
            content=(
                "CALIBRATION: S-014 has known leniency bias. Score critically. "
                "0.92 means genuinely excellent, not merely adequate."
            ),
            priority=4,
            token_estimate=25,
        ),
        "deep-review": ContentBlock(
            block_id="deep-review",
            content=(
                "DEEP REVIEW (C3+): Apply pre-mortem (S-004): how could this fail? "
                "Apply FMEA (S-012): enumerate failure modes. "
                "Apply inversion (S-013): what anti-patterns exist?"
            ),
            priority=4,
            token_estimate=40,
        ),
    }
```

### Component 3: Reinforcement Content (`reinforcement_content.py`)

**Responsibility:** Static content definitions. Separated from engine to enable independent content updates without modifying logic.

The content blocks are defined inline in `_build_content_blocks()` above for simplicity. If content management becomes complex (e.g., loading from files, versioning), this can be extracted to a separate module.

### Component 4: Context Provider (`context_provider.py`)

**Responsibility:** Read external state (file system, environment) to inform reinforcement decisions.

```python
"""Context provider for prompt reinforcement engine.

Reads external state to inform enforcement decisions.
All I/O is encapsulated here to keep the engine pure.
"""
from __future__ import annotations

from pathlib import Path


class ContextProvider:
    """Provides context information from the file system.

    Encapsulates all file system access to maintain
    testability of the reinforcement engine.
    """

    def __init__(self, project_root: Path | None = None) -> None:
        self._root = project_root or self._find_root()

    def get_constitution_path(self) -> Path:
        """Return path to JERRY_CONSTITUTION.md."""
        return self._root / "docs" / "governance" / "JERRY_CONSTITUTION.md"

    def get_rules_dir(self) -> Path:
        """Return path to .claude/rules/ directory."""
        return self._root / ".claude" / "rules"

    def is_governance_file(self, file_path: str) -> bool:
        """Check if a file path targets governance/constitution files."""
        governance_prefixes = [
            "docs/governance/JERRY_CONSTITUTION.md",
            ".claude/rules/",
            ".context/rules/",
            "docs/governance/",
        ]
        return any(file_path.startswith(p) or file_path.endswith(p)
                    for p in governance_prefixes)

    def _find_root(self) -> Path:
        """Find project root by looking for CLAUDE.md."""
        current = Path.cwd()
        for parent in [current, *current.parents]:
            if (parent / "CLAUDE.md").exists():
                return parent
        return current
```

---

## V-024 Content Design

### Token Budget Allocation

Total budget: **600 tokens** (per ADR-EPIC002-002, Standard Enforcement Budget).

| Block | Token Estimate | Priority | Trigger | Always/Conditional |
|-------|---------------|----------|---------|-------------------|
| quality-gate | ~30 | 1 (Core) | Always | Always |
| constitutional-principles | ~65 | 1 (Core) | Always (S-007) | Always |
| self-review | ~30 | 2 (Core) | Always (S-010) | Always |
| scoring-requirement | ~35 | 3 | Deliverable expected (S-014) | Conditional |
| steelman | ~30 | 3 | Review/critique expected (S-003) | Conditional |
| leniency-calibration | ~25 | 4 | When scoring active | Conditional |
| deep-review | ~40 | 4 | C3+ criticality | Conditional |

**Typical prompt (C2, no deliverable):** quality-gate + constitutional + self-review = ~125 tokens (~500 chars)
**Deliverable prompt (C2):** + scoring + leniency-calibration = ~190 tokens (~760 chars)
**Review prompt (C2):** + steelman = ~155 tokens (~620 chars)
**C3+ prompt:** + deep-review = ~230 tokens (~920 chars)
**Maximum possible (all blocks):** ~255 tokens (~1020 chars) -- within 600 token budget

### Content Format

Reinforcement content uses XML tags per REQ-403-094:

```xml
<enforcement-context criticality="C2">
QUALITY: Target >= 0.92. Score all deliverables against rubrics. Creator-critic-revision: minimum 3 iterations.
CONSTITUTION: P-003 No recursive subagents (max 1 level). P-020 User authority (never override, ask before destructive). P-022 No deception (never deceive about actions/capabilities). P-002 Filesystem as memory (persist to files). Check .claude/rules/ for full standards.
SELF-REVIEW (S-010): Review your output for completeness, accuracy, and quality before presenting. Apply self-critique.
</enforcement-context>
```

### Content Design Principles

1. **Ultra-compact:** Every word must carry enforcement value. No preamble, no explanation, no filler.
2. **Imperative voice:** Direct commands ("Score all deliverables", "Review your output") not descriptions ("The quality gate requires...").
3. **Strategy-tagged:** Each block is tagged with its source strategy (S-007, S-010, etc.) for traceability.
4. **Criticality-aware:** The XML wrapper carries the criticality level so Claude can assess enforcement depth.
5. **Self-contained:** Each block is meaningful without context from other blocks. Any subset of blocks provides value.

---

## Injection Strategy

### When to Inject

**Every user prompt.** This is the defining property of L2 enforcement.

Per REQ-403-010 and the IMMUNE-by-design property from ADR-EPIC002-002: V-024 re-injects on every prompt regardless of context state. If it only injected on some prompts, there would be windows where context rot degrades enforcement uncompensated.

The content *composition* varies per prompt (based on context signals and criticality), but injection itself is unconditional.

### How to Inject

The `additionalContext` field in the hook JSON output adds content to Claude's context window without being visible to the user. This matches the existing SessionStart hook pattern (REQ-403-019).

```json
{
    "hookSpecificOutput": {
        "hookEventName": "UserPromptSubmit",
        "additionalContext": "<enforcement-context criticality=\"C2\">\n...\n</enforcement-context>"
    }
}
```

### Adaptive Content Selection

Content is selected based on two signals:

1. **User prompt keywords:** Detect deliverable-expected, review-expected, or governance-related context from the prompt text.
2. **Decision criticality:** Assess C1-C4 from prompt signals and escalate content intensity accordingly.

This is NOT adaptive frequency (injecting on some prompts but not others). It is adaptive *content* with constant *frequency*.

---

## Adversarial Strategy Integration

### S-007 (Constitutional AI) -- Always

**Integration:** The `constitutional-principles` block reminds Claude of the four critical constitutional principles (P-003, P-020, P-022, P-002) and points to `.claude/rules/` for full standards. This is injected on every prompt.

**Rationale:** S-007 is Jerry's native adversarial pattern -- the rules ARE the constitution. Reinforcement ensures the constitution reference survives context rot.

### S-010 (Self-Refine) -- Always

**Integration:** The `self-review` block reminds Claude to self-review before presenting outputs. This is injected on every prompt.

**Rationale:** Self-Refine is the universal pre-critic baseline (L0 quality). Its effectiveness depends on the LLM remembering to apply it, which degrades under context rot.

### S-014 (LLM-as-Judge) -- When Deliverable Expected

**Integration:** The `scoring-requirement` block injects quality scoring requirements when deliverable signals are detected. The `leniency-calibration` block provides bias correction.

**Trigger detection:** Keywords like "implement", "create", "build", "write", "design", "produce", "generate", "deliver" in the user prompt.

**Rationale:** S-014 is the scoring backbone for the 0.92 quality gate. It has a known leniency bias (R-014-FN) that requires active calibration.

### S-003 (Steelman) -- When Review/Critique Expected

**Integration:** The `steelman` block reminds Claude to reconstruct the strongest version of an argument before critiquing.

**Trigger detection:** Keywords like "review", "critique", "evaluate", "assess", "audit", "check", "validate" in the user prompt.

**Rationale:** Steelman prevents strawman attacks in adversarial review. Its application depends on Claude remembering the technique, which degrades under context rot.

---

## Decision Criticality Awareness

### Criticality Assessment Algorithm

The hook assesses decision criticality from prompt signals:

| Level | Signal Keywords | Content Escalation |
|-------|----------------|-------------------|
| C1 (Routine) | "read", "show", "list", "what is", "explain", "help" | Core blocks only (~125 tokens) |
| C2 (Standard) | Default for most operations | Core + conditional blocks as needed (~125-190 tokens) |
| C3 (Significant) | ".claude/rules", "architecture", "breaking change", "api change" | Core + conditional + deep-review (~230 tokens) |
| C4 (Critical) | "constitution", "governance", "public release", "adr" | Core + conditional + deep-review (~255 tokens) |

### Limitations of Prompt-Based Assessment

The criticality assessment from prompt keywords is a **heuristic approximation**. It cannot reliably detect all C3/C4 situations because:

1. The user may not mention governance files explicitly in their prompt
2. The user may use indirect language that does not contain signal keywords
3. Multi-turn conversations may escalate criticality without a single indicative prompt

**Mitigation:** The PreToolUse hook (L3) provides a deterministic second check for governance file access (REQ-403-032, REQ-403-061). If the UserPromptSubmit hook's heuristic misses a C3+ situation, the PreToolUse hook catches it at the tool-use level.

---

## Error Handling

### Fail-Open Design (REQ-403-070)

```
Exception in hook logic
       │
       ├──► Log error to stderr (REQ-403-071)
       │
       └──► Output empty additionalContext
            │
            └──► Hook returns exit code 0
                 │
                 └──► User prompt proceeds normally
```

### Error Categories and Responses

| Error | Response | Logging |
|-------|----------|---------|
| `json.JSONDecodeError` (invalid stdin) | Empty context, exit 0 | stderr: "Invalid JSON input" |
| `ImportError` (enforcement module not found) | Empty context, exit 0 | stderr: "Enforcement module not available" |
| `FileNotFoundError` (project root not found) | Empty context, exit 0 | stderr: "Project root not found" |
| `Exception` (any other error) | Empty context, exit 0 | stderr: Error message |
| Token budget exceeded | Trim to budget | No error; normal operation |

### What "Fail-Open" Does NOT Mean

- It does NOT mean errors are silently swallowed (REQ-403-071 requires logging)
- It does NOT mean enforcement is permanently disabled (next prompt tries again)
- It does NOT mean the hook exits with non-zero code (which would signal Claude Code to potentially block)

---

## Platform Adaptation

### Claude Code (Primary Platform)

On Claude Code, the hook is registered in `hooks/hooks.json` and invoked automatically on every user prompt. The `additionalContext` field is natively supported.

### Non-Claude-Code Platforms

Per REQ-403-077, the enforcement logic must be importable as a Python library:

```python
# Example: Non-Claude-Code integration
from src.infrastructure.internal.enforcement.prompt_reinforcement_engine import (
    PromptReinforcementEngine,
    PromptContext,
)

engine = PromptReinforcementEngine()
content = engine.generate_reinforcement(PromptContext(
    user_prompt="Implement the login feature",
))

# Platform-specific injection
inject_into_system_prompt(content.rendered_text)
```

**Alternative integration paths:**
1. **Cursor/Windsurf:** Inject V-024 content into the system prompt or custom instructions
2. **Generic LLM API:** Prepend V-024 content to the user message
3. **MCP-based platforms:** Use MCP tool context injection when available

The enforcement engine is pure Python with no Claude Code dependencies. Only the hook entry point (`hooks/user-prompt-submit.py`) is Claude Code-specific.

---

## File Layout

### New Files

| File | Layer | Purpose |
|------|-------|---------|
| `hooks/user-prompt-submit.py` | Interface | Thin adapter: hook entry point |
| `src/infrastructure/internal/enforcement/prompt_reinforcement_engine.py` | Infrastructure | Core enforcement logic |
| `src/infrastructure/internal/enforcement/context_provider.py` | Infrastructure | File system context reading |
| `tests/unit/enforcement/test_prompt_reinforcement_engine.py` | Test | Unit tests for engine |
| `tests/unit/enforcement/test_context_provider.py` | Test | Unit tests for context provider |

### Modified Files

| File | Change |
|------|--------|
| `hooks/hooks.json` | Add UserPromptSubmit hook registration |

### hooks.json Registration

```json
{
    "UserPromptSubmit": [
        {
            "matcher": "*",
            "hooks": [
                {
                    "type": "command",
                    "command": "uv run --directory ${CLAUDE_PLUGIN_ROOT} python ${CLAUDE_PLUGIN_ROOT}/hooks/user-prompt-submit.py",
                    "timeout": 3000
                }
            ]
        }
    ]
}
```

**Timeout:** 3000ms (3 seconds). The hook performs no I/O beyond reading stdin; content generation is in-memory. 3 seconds provides ample margin. Per REQ-403-NFR-005 (NFR-005 in EN-403), latency should be < 500ms; 3s timeout is the safety ceiling.

---

## Interface Contracts

### Input Schema (stdin JSON)

```json
{
    "user_prompt": "string - the user's prompt text",
    "session_id": "string - Claude Code session identifier",
    "project_dir": "string - project directory path"
}
```

Note: The exact input schema for UserPromptSubmit hooks depends on Claude Code's hook protocol. The fields above are the expected inputs based on the SessionStart hook pattern (SRC-006). If the actual schema differs, the thin adapter layer absorbs the difference.

### Output Schema (stdout JSON)

```json
{
    "hookSpecificOutput": {
        "hookEventName": "UserPromptSubmit",
        "additionalContext": "string - V-024 reinforcement content (XML-tagged)"
    }
}
```

### Internal Interfaces

```python
# PromptContext -- input to engine
@dataclass(frozen=True)
class PromptContext:
    user_prompt: str = ""
    session_id: str = ""
    project_dir: str = ""

# ReinforcementContent -- output from engine
@dataclass(frozen=True)
class ReinforcementContent:
    rendered_text: str        # The actual content to inject
    token_estimate: int       # Estimated token count
    blocks_included: list[str]  # Block IDs included
    criticality_level: str    # C1/C2/C3/C4
```

---

## Testing Strategy

### Unit Tests

| Test | File | Validates |
|------|------|-----------|
| `test_generate_reinforcement_includes_core_blocks` | `test_prompt_reinforcement_engine.py` | REQ-403-012, 013, 014 |
| `test_generate_reinforcement_within_token_budget` | `test_prompt_reinforcement_engine.py` | REQ-403-015 |
| `test_deliverable_context_triggers_scoring_block` | `test_prompt_reinforcement_engine.py` | REQ-403-016 |
| `test_review_context_triggers_steelman_block` | `test_prompt_reinforcement_engine.py` | REQ-403-018 |
| `test_scoring_block_includes_leniency_calibration` | `test_prompt_reinforcement_engine.py` | REQ-403-017 |
| `test_c3_criticality_includes_deep_review` | `test_prompt_reinforcement_engine.py` | REQ-403-062 |
| `test_c4_criticality_includes_deep_review` | `test_prompt_reinforcement_engine.py` | REQ-403-062 |
| `test_output_uses_xml_tags` | `test_prompt_reinforcement_engine.py` | REQ-403-094 |
| `test_trim_to_budget_preserves_core_blocks` | `test_prompt_reinforcement_engine.py` | REQ-403-015 |
| `test_engine_is_stateless` | `test_prompt_reinforcement_engine.py` | REQ-403-081 |
| `test_engine_uses_no_external_imports` | `test_prompt_reinforcement_engine.py` | REQ-403-075 |

### Integration Tests

| Test | Validates |
|------|-----------|
| Hook entry point reads stdin JSON and produces valid output JSON | REQ-403-019 |
| Hook returns exit 0 on all error conditions | REQ-403-070 |
| Hook logs errors to stderr | REQ-403-071 |

### Adversarial Tests (for TASK-009)

| Test | Attack Vector |
|------|--------------|
| Verify hook cannot be disabled by user prompt content | Prompt injection |
| Verify hook fires even after 100K+ tokens of conversation | Context rot survival |
| Verify enforcement content survives in Claude's responses | L2 effectiveness |

---

## Requirements Coverage

| Requirement | Covered By |
|-------------|-----------|
| REQ-403-010 | `main()` calls engine on every invocation |
| REQ-403-011 | Output uses `additionalContext` field |
| REQ-403-012 | `quality-gate` content block |
| REQ-403-013 | `constitutional-principles` content block |
| REQ-403-014 | `self-review` content block |
| REQ-403-015 | `TOKEN_BUDGET = 600` and `_trim_to_budget()` |
| REQ-403-016 | Conditional `scoring-requirement` block selection |
| REQ-403-017 | Conditional `leniency-calibration` block selection |
| REQ-403-018 | Conditional `steelman` block selection |
| REQ-403-019 | Output JSON schema in `main()` |
| REQ-403-070 | `main()` try/except returns 0 always |
| REQ-403-071 | stderr logging in except block |
| REQ-403-075 | Only stdlib imports in engine |
| REQ-403-076 | `pathlib.Path` in context_provider |
| REQ-403-077 | Engine importable as library |
| REQ-403-078 | `encoding='utf-8'` in file reads |
| REQ-403-080 | Hexagonal layering (hook -> engine -> content) |
| REQ-403-081 | Engine has typed parameters and returns |
| REQ-403-082 | Hook entry point is thin adapter |
| REQ-403-085 | L2 re-injects on every prompt |
| REQ-403-090 | `constitutional-principles` block (S-007) |
| REQ-403-091 | `self-review` block (S-010) |
| REQ-403-094 | XML `<enforcement-context>` tags |
| REQ-403-095 | Quality threshold in both SessionStart and UserPromptSubmit |
| REQ-403-096 | Creator-critic-revision in quality-gate block |

---

## References

| # | Citation | Used For |
|---|----------|----------|
| 1 | ADR-EPIC002-002 v1.2.0 (ACCEPTED) | L2 layer definition, V-024 token budget, defense-in-depth chain |
| 2 | Barrier-1 ADV-to-ENF Handoff | Strategy touchpoints (S-007, S-010, S-014, S-003), quality gate integration |
| 3 | EN-403 Enabler Definition v2.0.0 | FR-001 through FR-003, FR-007-009, NFR-001/002/005/008 |
| 4 | TASK-001 Hook Requirements (this enabler) | REQ-403-010 through REQ-403-096 |
| 5 | `scripts/session_start_hook.py` | Output format pattern (additionalContext, systemMessage) |
| 6 | `hooks/hooks.json` | Hook registration pattern |
| 7 | EN-402 TASK-006 Execution Plans | Enforcement utility placement in `src/infrastructure/internal/enforcement/` |
| 8 | `.context/rules/architecture-standards.md` | Hexagonal architecture patterns |

---

*Agent: ps-architect (Claude Opus 4.6)*
*Date: 2026-02-13*
*Parent: EN-403 Hook-Based Enforcement Implementation*
*Quality Target: >= 0.92*
*Target ACs: 2, 5, 10, 11*
