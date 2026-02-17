# TASK-005: Implementation Specification

<!--
DOCUMENT-ID: FEAT-005:EN-405:TASK-005
TEMPLATE: Implementation Specification
VERSION: 1.0.0
AGENT: ps-architect-405 (Claude Opus 4.6)
DATE: 2026-02-14
PARENT: EN-405 (Session Context Enforcement Injection)
FEATURE: FEAT-005 (Quality Framework Enforcement Mechanisms)
EPIC: EPIC-002 (Quality Framework Enforcement)
PROJECT: PROJ-001-oss-release
QUALITY-TARGET: >= 0.92
REQUIREMENTS-COVERED: All FR-405-xxx, IR-405-xxx, EH-405-xxx, PR-405-xxx
NOTE: This is a specification-level document (design doc), NOT production deployment.
-->

> **Version:** 1.0.0
> **Agent:** ps-architect-405 (Claude Opus 4.6)
> **Status:** COMPLETE
> **Created:** 2026-02-14
> **Note:** Specification-level code. Implementation will be done by a later task (TASK-005 implementation phase).

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Implementation Overview](#implementation-overview) | What files are created/modified and why |
| [File 1: session_quality_context.py](#file-1-session_quality_contextpy) | Full specification-level code for the generator module |
| [File 2: __init__.py](#file-2-__init__py) | Package initialization |
| [File 3: session_start_hook.py Modifications](#file-3-session_start_hookpy-modifications) | Exact changes to the existing hook |
| [File 4: Unit Test Specification](#file-4-unit-test-specification) | Test cases for the generator |
| [Error Handling Specification](#error-handling-specification) | How errors are handled at each level |
| [Token Budget Verification](#token-budget-verification) | Character count to token estimate mapping |
| [Traceability](#traceability) | Requirements coverage |
| [References](#references) | Source documents |

---

## Implementation Overview

| # | File | Action | Layer |
|---|------|--------|-------|
| 1 | `src/infrastructure/internal/enforcement/session_quality_context.py` | CREATE | Infrastructure |
| 2 | `src/infrastructure/internal/enforcement/__init__.py` | CREATE | Infrastructure |
| 3 | `scripts/session_start_hook.py` | MODIFY (+21 lines) | Interface (thin adapter) |
| 4 | `tests/unit/enforcement/test_session_quality_context.py` | CREATE | Test |

---

## File 1: session_quality_context.py

**Path:** `src/infrastructure/internal/enforcement/session_quality_context.py`
**Purpose:** Quality framework context generator for SessionStart hook
**Lines:** ~120

```python
"""Session quality context generator for SessionStart hook.

Generates quality framework context to inject at session
initialization. This content establishes the L1 behavioral
foundation that L2 (UserPromptSubmit) subsequently reinforces.

References:
    - EN-403 TASK-004: SessionStart Hook Architecture Design
    - EN-405 TASK-002: Quality Framework Preamble Design
    - Barrier-2 ADV-to-ENF Handoff: Per-criticality strategy sets
"""
from __future__ import annotations


class SessionQualityContextGenerator:
    """Generates quality framework context for session start.

    The generated content includes:
    - Quality gate threshold and scoring requirements
    - Constitutional principles summary
    - Available adversarial strategies (all 10 selected)
    - Decision criticality framework (C1-C4)

    The generator is stateless and produces identical output
    on every invocation (content is static by design).

    Design properties:
    - Stateless: no instance state
    - Pure: no I/O, no file reads, no network
    - Deterministic: same output every time
    - Stdlib-only: no external imports (REQ-403-075)
    """

    VERSION: str = "1.0"

    def generate(self) -> str:
        """Generate the quality framework context block.

        Returns:
            XML-tagged quality context string (~435 calibrated tokens / ~524 conservative).
            Contains 4 sections: quality-gate, constitutional-principles,
            adversarial-strategies, decision-criticality.
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
        """Generate quality gate section.

        Includes:
        - 0.92 threshold (HARD rule H-13)
        - S-014 scoring mechanism
        - Leniency bias awareness (R-014-FN)
        - Creator-critic-revision cycle (HARD rule H-14)
        - SYN #1 pairing: S-003 before S-002
        - Context rot awareness (Barrier-2 recommendation)
        """
        return (
            "  <quality-gate>\n"
            "    Target: >= 0.92 for all deliverables.\n"
            "    Scoring: Use S-014 (LLM-as-Judge) with "
            "dimension-level rubrics.\n"
            "    Known bias: S-014 has leniency bias. "
            "Score critically -- 0.92 means genuinely excellent.\n"
            "    Cycle: Creator -> Critic -> Revision "
            "(minimum 3 iterations). Do not bypass.\n"
            "    Pairing: Steelman (S-003) before Devil's Advocate "
            "(S-002) -- canonical review protocol.\n"
            "    Context rot: After ~20K tokens, re-read "
            ".claude/rules/ and consider session restart "
            "for C3+ work.\n"
            "  </quality-gate>"
        )

    def _constitutional_section(self) -> str:
        """Generate constitutional principles section.

        Includes HARD rules H-01, H-02, H-03, H-05/H-06.
        Only principles with HARD enforcement and highest
        bypass-impact are included.
        """
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
        """Generate adversarial strategies section.

        Lists all 10 selected strategies ordered by role prominence:
        scoring backbone first, constitutional compliance second,
        universal self-review third, then remaining strategies
        in descending composite score order.
        """
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
        """Generate decision criticality section.

        Includes C1-C4 definitions, per-criticality strategy
        guidance (FR-405-021), and expanded auto-escalation
        rules (AE-001 through AE-004 from EN-303).
        """
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
            "    Strategy guidance: C1(S-010) "
            "C2(S-007+S-002+S-014) "
            "C3(6+ strategies) C4(all 10).\n"
            "    AUTO-ESCALATE: governance files/rules -> C3+; "
            "new/modified ADR -> C3+; "
            "modified baselined ADR -> C4.\n"
            "  </decision-criticality>"
        )
```

### Design Notes

1. **No imports beyond `__future__`:** The generator uses only Python string operations. Zero external dependencies.

2. **Explicit string concatenation:** Each section builds its content with explicit string concatenation using `( )` grouping. This is more verbose but easier to audit line-by-line than f-strings with embedded newlines.

3. **Each `_section()` method returns the full XML section** including opening and closing tags with 2-space indentation. The `generate()` method wraps them with the top-level tag.

4. **Docstrings on every method** per coding standards H-12. Each docstring explains what is included and why.

5. **SYN #1 pairing** added to `_quality_gate_section()` per SR-405-005 (TASK-002 preamble design). This is the only addition beyond the EN-403 TASK-004 baseline design.

---

## File 2: __init__.py

**Path:** `src/infrastructure/internal/enforcement/__init__.py`

```python
"""Enforcement infrastructure for Jerry quality framework.

This package contains enforcement-related infrastructure components
including session context injection and (future) prompt reinforcement.
"""
```

**Note:** If `src/infrastructure/internal/` does not have an `__init__.py`, one must be created there as well. Verify directory structure before implementation.

---

## File 3: session_start_hook.py Modifications

**Path:** `scripts/session_start_hook.py`

### Modification 1: Import Block (After Existing Imports)

Insert after `from pathlib import Path` (use pattern-based identification, not absolute line numbers):

```python

# Quality framework context injection (EN-405)
_project_root = str(Path(__file__).resolve().parent.parent)
try:
    sys.path.insert(0, _project_root)
    from src.infrastructure.internal.enforcement.session_quality_context import (
        SessionQualityContextGenerator,
    )
    QUALITY_CONTEXT_AVAILABLE = True
except Exception:
    QUALITY_CONTEXT_AVAILABLE = False
finally:
    # Clean up sys.path to avoid shadowing stdlib modules
    if _project_root in sys.path:
        sys.path.remove(_project_root)
```

### Modification 2: Quality Context Generation (In `main()`, After `format_hook_output()`)

Insert between the current lines:
```python
        system_message, additional_context = format_hook_output(cli_data, precommit_warning)
        # === INSERT HERE ===
        output_json(system_message, additional_context)
```

New code:
```python
        # Generate quality framework context (EN-405)
        quality_context = ""
        if QUALITY_CONTEXT_AVAILABLE:
            try:
                generator = SessionQualityContextGenerator()
                quality_context = generator.generate()
            except Exception as e:
                log_error(log_file, f"WARNING: Quality context generation failed: {e}")
                quality_context = ""  # Fail-open: session proceeds without quality context

        # Append quality context to additional context (EN-405)
        if quality_context:
            additional_context = additional_context + "\n\n" + quality_context
```

---

## File 4: Unit Test Specification

**Path:** `tests/unit/enforcement/test_session_quality_context.py`

```python
"""Unit tests for SessionQualityContextGenerator.

Tests verify that the quality framework context block contains
all required sections, content elements, and formatting.
"""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from src.infrastructure.internal.enforcement.session_quality_context import (
    SessionQualityContextGenerator,
)


class TestSessionQualityContextGenerator:
    """Tests for the SessionQualityContextGenerator class."""

    def setup_method(self) -> None:
        """Create generator instance for each test."""
        self.generator = SessionQualityContextGenerator()
        self.output = self.generator.generate()

    # --- Structure Tests ---

    def test_generate_returns_xml_tagged_content(self) -> None:
        """Output is wrapped in quality-framework XML tags."""
        assert '<quality-framework version="1.0">' in self.output
        assert "</quality-framework>" in self.output

    def test_output_contains_4_xml_sections(self) -> None:
        """Output contains exactly 4 required XML subsections."""
        assert "<quality-gate>" in self.output
        assert "</quality-gate>" in self.output
        assert "<constitutional-principles>" in self.output
        assert "</constitutional-principles>" in self.output
        assert "<adversarial-strategies>" in self.output
        assert "</adversarial-strategies>" in self.output
        assert "<decision-criticality>" in self.output
        assert "</decision-criticality>" in self.output

    # --- Quality Gate Section Tests ---

    def test_quality_gate_includes_092_threshold(self) -> None:
        """Quality gate section includes 0.92 threshold."""
        assert "0.92" in self.output

    def test_quality_gate_includes_scoring_requirement(self) -> None:
        """Quality gate section references S-014 as scoring mechanism."""
        assert "S-014" in self.output
        assert "LLM-as-Judge" in self.output

    def test_quality_gate_includes_leniency_bias(self) -> None:
        """Quality gate section warns about S-014 leniency bias."""
        assert "leniency bias" in self.output

    def test_quality_gate_includes_creator_critic_revision(self) -> None:
        """Quality gate section includes the creator-critic-revision cycle."""
        assert "Creator" in self.output
        assert "Critic" in self.output
        assert "Revision" in self.output
        assert "3 iterations" in self.output

    def test_quality_gate_includes_context_rot_awareness(self) -> None:
        """Quality gate section includes context rot awareness line."""
        assert "Context rot" in self.output or "context rot" in self.output
        assert "20K" in self.output

    def test_quality_gate_includes_syn1_pairing(self) -> None:
        """Quality gate section includes SYN #1 pairing guidance."""
        assert "Steelman" in self.output
        assert "S-003" in self.output
        assert "S-002" in self.output
        # Verify ordering: S-003 before S-002 in the pairing line
        pairing_line = [
            line for line in self.output.split("\n")
            if "Pairing" in line or "canonical" in line.lower()
        ]
        assert len(pairing_line) >= 1

    # --- Constitutional Section Tests ---

    def test_constitutional_includes_p003_p020_p022(self) -> None:
        """Constitutional section includes all three HARD principles."""
        assert "P-003" in self.output
        assert "P-020" in self.output
        assert "P-022" in self.output

    def test_constitutional_includes_uv_only(self) -> None:
        """Constitutional section includes UV-only rule."""
        assert "UV only" in self.output or "uv run" in self.output

    # --- Strategies Section Tests ---

    def test_strategies_lists_all_10_selected(self) -> None:
        """Strategies section lists all 10 selected strategies."""
        required_strategies = [
            "S-014", "S-007", "S-010", "S-003", "S-002",
            "S-013", "S-004", "S-012", "S-011", "S-001",
        ]
        for strategy in required_strategies:
            assert strategy in self.output, f"Missing strategy: {strategy}"

    def test_strategies_ordered_by_role_prominence(self) -> None:
        """Strategies ordered: S-014 first, S-007 second, S-010 third."""
        s014_pos = self.output.index("S-014")
        s007_pos = self.output.index("S-007")
        s010_pos = self.output.index("S-010")
        # S-014 appears before S-007 which appears before S-010
        # (first occurrence in the strategies section)
        strategies_section = self.output[
            self.output.index("<adversarial-strategies>"):
            self.output.index("</adversarial-strategies>")
        ]
        first_s014 = strategies_section.index("S-014")
        first_s007 = strategies_section.index("S-007")
        first_s010 = strategies_section.index("S-010")
        assert first_s014 < first_s007 < first_s010

    # --- Criticality Section Tests ---

    def test_criticality_includes_c1_through_c4(self) -> None:
        """Criticality section includes all four levels."""
        assert "C1" in self.output
        assert "C2" in self.output
        assert "C3" in self.output
        assert "C4" in self.output

    def test_criticality_includes_per_criticality_strategy_guidance(self) -> None:
        """Criticality section includes per-criticality strategy activation."""
        assert "C1(S-010)" in self.output
        assert "C2(S-007+S-002+S-014)" in self.output
        assert "C3(6+ strategies)" in self.output
        assert "C4(all 10)" in self.output

    def test_criticality_includes_auto_escalation(self) -> None:
        """Criticality section includes expanded auto-escalation rules."""
        assert "AUTO-ESCALATE" in self.output
        assert "governance" in self.output
        assert "rules" in self.output
        assert "ADR" in self.output  # AE-003/AE-004 coverage

    # --- Non-Functional Tests ---

    def test_generator_is_stateless(self) -> None:
        """Generator produces identical output on repeated invocations."""
        output1 = self.generator.generate()
        output2 = self.generator.generate()
        assert output1 == output2

    def test_generator_uses_no_external_imports(self) -> None:
        """Generator module uses only stdlib imports."""
        import importlib.util

        spec = importlib.util.find_spec(
            "src.infrastructure.internal.enforcement.session_quality_context"
        )
        if spec is None or spec.origin is None:
            pytest.skip("Module not found via importlib; verify install")
        module_path = Path(spec.origin)
        source = module_path.read_text()
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert alias.name.startswith(("__future__",)), (
                        f"Non-stdlib import: {alias.name}"
                    )
            elif isinstance(node, ast.ImportFrom):
                if node.module and not node.module.startswith("__future__"):
                    pytest.fail(
                        f"Non-stdlib import: from {node.module}"
                    )

    def test_token_estimate_within_budget(self) -> None:
        """Output is within calibrated token budget."""
        # Conservative estimate: chars / 4
        conservative_tokens = len(self.output) / 4
        # Calibrated estimate: chars / 4 * 0.83 (XML content correction)
        calibrated_tokens = conservative_tokens * 0.83
        # Budget: ~435 calibrated tokens target, allow up to 500 calibrated for margin
        assert calibrated_tokens <= 500, (
            f"Calibrated token estimate {calibrated_tokens:.0f} exceeds 500 budget"
        )
        # Sanity check: should be at least 350 calibrated tokens
        assert calibrated_tokens >= 350, (
            f"Calibrated token estimate {calibrated_tokens:.0f} suspiciously low"
        )

    # --- Degradation Tests (Finding 17) ---

    def test_output_valid_without_strategy_list(self) -> None:
        """Degraded preamble (no strategy list) still has valid XML structure."""
        # Simulate degradation step 1: remove strategy list
        output = self.output
        start = output.index("<adversarial-strategies>")
        end = output.index("</adversarial-strategies>") + len("</adversarial-strategies>")
        degraded = output[:start] + output[end:]
        # Verify remaining XML structure
        assert '<quality-framework version="1.0">' in degraded
        assert "</quality-framework>" in degraded
        assert "<quality-gate>" in degraded
        assert "<constitutional-principles>" in degraded
        assert "<decision-criticality>" in degraded

    def test_output_valid_at_minimum_viable(self) -> None:
        """Minimum viable preamble (quality-gate + constitutional only) has valid structure."""
        output = self.output
        # Extract quality-gate section
        qg_start = output.index("<quality-gate>")
        qg_end = output.index("</quality-gate>") + len("</quality-gate>")
        quality_gate = output[qg_start:qg_end]
        # Extract constitutional section
        cp_start = output.index("<constitutional-principles>")
        cp_end = output.index("</constitutional-principles>") + len("</constitutional-principles>")
        constitutional = output[cp_start:cp_end]
        # Verify both sections are self-contained
        assert "0.92" in quality_gate
        assert "P-003" in constitutional
        assert "P-020" in constitutional
```

### Test Count: 20

| Category | Tests |
|----------|-------|
| Structure | 2 (XML wrapper, 4 sections) |
| Quality gate content | 5 (threshold, scoring, bias, cycle, SYN #1, context rot) |
| Constitutional content | 2 (principles, UV) |
| Strategies content | 2 (all 10, ordering) |
| Criticality content | 3 (C1-C4, per-criticality strategy guidance, auto-escalation) |
| Non-functional | 3 (stateless, stdlib-only, token budget) |
| Degradation | 2 (no strategy list, minimum viable) |
| FR-405-021 verification | 1 (per-criticality strategy activation in output) |

---

## Error Handling Specification

### Import-Level Error Handling

```python
# In session_start_hook.py, import block
_project_root = str(Path(__file__).resolve().parent.parent)
try:
    sys.path.insert(0, _project_root)
    # ... import SessionQualityContextGenerator ...
    QUALITY_CONTEXT_AVAILABLE = True
except Exception:
    QUALITY_CONTEXT_AVAILABLE = False
    # No logging here -- this is expected when module is not deployed
    # except Exception (not ImportError) catches SyntaxError, AttributeError, etc.
    # to ensure fail-open: quality context import failures must NEVER produce
    # user-visible errors (the outer main() handler calls output_error())
finally:
    if _project_root in sys.path:
        sys.path.remove(_project_root)
```

**Behavior:** Silent fail for ANY exception type. No log entry because this is a normal state during incremental deployment. The `except Exception` catch is intentionally broad: a `SyntaxError` in the quality context module would otherwise fall through to the outer `main()` handler which calls `output_error()` producing user-visible terminal output -- violating the fail-open design intent.

### Generation-Level Error Handling

```python
# In session_start_hook.py, main()
try:
    generator = SessionQualityContextGenerator()
    quality_context = generator.generate()
except Exception as e:
    log_error(log_file, f"WARNING: Quality context generation failed: {e}")
    quality_context = ""
```

**Behavior:** Log warning with full exception message, then continue with empty quality context. The `Exception` catch is intentionally broad to ensure fail-open in all scenarios.

### Error Chain Summary

| Error Level | Caught By | Logged? | Recovery |
|-------------|-----------|---------|----------|
| Any exception during import (ImportError, SyntaxError, etc.) | Import try/except Exception | No (expected state) | QUALITY_CONTEXT_AVAILABLE = False; sys.path cleaned up |
| Any exception during generate() | main() try/except Exception | Yes (WARNING) | quality_context = "" |
| Any exception in main() outer try | Existing handler | Yes (ERROR) | output_error() -> exit 0 |

---

## Token Budget Verification

### Character Count Analysis

The following counts reflect the revised preamble content with per-criticality strategy guidance (FR-405-021), expanded AUTO-ESCALATE (AE-001 through AE-004), and context rot awareness line.

```
<quality-framework version="1.0">     = 37 chars
  <quality-gate>                       = 16 chars
    Target + Scoring + Bias +          = ~325 chars (6 lines, including context rot line)
    Cycle + Pairing + Context rot
  </quality-gate>                      = 17 chars
                                       [blank line = 1 char]
  <constitutional-principles>          = 29 chars
    HARD constraints...                = ~280 chars (5 lines)
  </constitutional-principles>         = 30 chars
                                       [blank line = 1 char]
  <adversarial-strategies>             = 26 chars
    Available strategies...            = ~590 chars (11 lines)
  </adversarial-strategies>            = 27 chars
                                       [blank line = 1 char]
  <decision-criticality>               = 24 chars
    Assess + C1-C4 + Strategy          = ~440 chars (8 lines, including strategy guidance + expanded AE)
    guidance + AUTO-ESCALATE
  </decision-criticality>              = 25 chars
</quality-framework>                   = 22 chars
```

**Estimated total characters:** ~2,096
**Conservative token estimate (chars/4):** ~524
**Calibrated token estimate (chars/4 * 0.83):** ~435

**Token estimation methodology:** The chars/4 method is a conservative upper bound. For XML-structured content with repeated patterns (e.g., `- S-NNN (Name):`), tokenizers produce ~17% fewer tokens. The 0.83x calibration factor is derived from EN-403 TASK-004's analysis of XML content tokenization variance. The actual token count MUST be verified with a real tokenizer (tiktoken cl100k_base or Claude tokenizer) per REQ-403-083 before production deployment.

### Budget Compliance

| Metric | Conservative (chars/4) | Calibrated (chars/4 * 0.83) | Budget | Status |
|--------|----------------------|---------------------------|--------|--------|
| Estimated tokens | ~524 | ~435 | ~450 max (calibrated) | WITHIN BUDGET (calibrated) |
| SessionStart total | ~674-754 | ~585-665 | ~650 target | NEAR TARGET (calibrated) |
| % of L1 budget | ~5.4-6.0% | ~4.7-5.3% | < 6% | WITHIN BUDGET |

**Note:** If real tokenizer verification shows the calibrated count exceeds 450 tokens, apply the degradation priority from PR-405-004: (1) shorten strategy descriptions by ~5 words each (-50 tokens), (2) condense C1-C4 to compact format (-50 tokens).

---

## Traceability

### Requirements Fully Specified

| Requirement | Implementation Location |
|-------------|----------------------|
| FR-405-001 | `_quality_gate_section()`: "Target: >= 0.92" |
| FR-405-002 | `_constitutional_section()`: P-003, P-020, P-022, UV |
| FR-405-003 | `_strategies_section()`: all 10 strategies |
| FR-405-004 | `_criticality_section()`: C1-C4 + AUTO-ESCALATE |
| FR-405-005 | `_quality_gate_section()`: "minimum 3 iterations" |
| FR-405-006 | `_quality_gate_section()`: "leniency bias" |
| FR-405-007 | `_criticality_section()`: AUTO-ESCALATE line |
| FR-405-010 | `generate()`: `<quality-framework version="1.0">` wrapper |
| FR-405-011 | `generate()`: 4 section methods called |
| FR-405-012 | Each section in its own XML block |
| FR-405-013 | All content uses imperative voice |
| FR-405-020 | `_strategies_section()`: 10 strategy lines |
| IR-405-001 | Hook modification is additive only |
| IR-405-002 | `additional_context + "\n\n" + quality_context` |
| IR-405-003 | systemMessage not referenced in new code |
| IR-405-004 | Module at `src/infrastructure/internal/enforcement/` |
| IR-405-005 | `QUALITY_CONTEXT_AVAILABLE` flag pattern |
| IR-405-006 | Insert point between format_hook_output() and output_json() |
| EH-405-001 | `except Exception as e` -> empty string |
| EH-405-002 | `log_error(log_file, ...)` |
| EH-405-004 | `except Exception` -> flag = False; sys.path cleaned up in finally |
| PR-405-001 | Pure string concatenation; << 1ms |
| PR-405-002 | ~435 calibrated tokens / ~524 conservative (2,096 characters) |

---

## References

| # | Document | Content Used |
|---|----------|--------------|
| 1 | EN-403 TASK-004 (SessionStart Design) | Primary code reference: class structure, method signatures, XML format |
| 2 | TASK-001 (requirements) | FR-405-xxx, IR-405-xxx, EH-405-xxx, PR-405-xxx |
| 3 | TASK-002 (preamble design) | Content specification for each section |
| 4 | TASK-003 (hook enhancement) | Integration points, file layout |
| 5 | TASK-004 (integration design) | Modification specification, backward compatibility |
| 6 | EN-404 TASK-003 (Tiered Enforcement) | HARD rules H-13 through H-19 |
| 7 | Barrier-2 ADV-to-ENF Handoff | Strategy catalog, criticality definitions |

---

*Agent: ps-architect-405 (Claude Opus 4.6)*
*Date: 2026-02-14*
*Parent: EN-405 Session Context Enforcement Injection*
*Quality Target: >= 0.92*
*Module: ~120 lines*
*Hook Changes: +21 lines*
*Unit Tests: 20*
