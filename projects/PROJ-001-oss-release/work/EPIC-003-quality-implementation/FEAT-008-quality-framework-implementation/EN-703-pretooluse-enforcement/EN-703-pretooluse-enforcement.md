# EN-703: PreToolUse Enforcement Engine

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-14 (Claude)
PURPOSE: Implement L3 Pre-Action Gating enforcement engine with AST-based analysis
-->

> **Type:** enabler
> **Status:** pending
> **Priority:** critical
> **Impact:** critical
> **Enabler Type:** infrastructure
> **Created:** 2026-02-14
> **Due:** —
> **Completed:** —
> **Parent:** FEAT-008
> **Owner:** —
> **Effort:** 13

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this enabler delivers |
| [Problem Statement](#problem-statement) | Why this work is needed |
| [Technical Approach](#technical-approach) | How we'll implement it |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Evidence](#evidence) | Proof of completion |
| [Dependencies](#dependencies) | What this depends on |
| [History](#history) | Change log |

---

## Summary

Implement the L3 Pre-Action Gating enforcement engine. Uses AST-based analysis to deterministically block non-compliant tool calls before execution. Implements vectors V-038 (import boundary), V-039 (type hints), V-040 (docstrings), V-041 (one-class-per-file). Zero token cost, context-rot-immune. The engine runs externally as a Python AST analyzer, making enforcement decisions without depending on LLM context state.

## Problem Statement

Currently no deterministic enforcement prevents architectural violations at write-time. The `pre_tool_use.py` hook exists but lacks AST-based enforcement capabilities designed in EPIC-002. Violations of import boundaries, missing type hints, missing docstrings, and multi-class files can only be caught after the fact by CI or manual review. This creates a gap where non-compliant code enters the codebase and must be retroactively fixed, wasting cycles and degrading quality. The PreToolUse hook (V-001) at L3 in the 5-layer architecture is the only layer that can prevent violations before they occur at the tool call level, operating deterministically regardless of LLM context rot.

## Technical Approach

1. **Create `src/infrastructure/internal/enforcement/pre_tool_enforcement_engine.py`** -- Central engine class (`PreToolEnforcementEngine`) that orchestrates all AST-based checks. Accepts file content and file path, returns pass/fail with structured violation reports.

2. **Implement V-038: AST Import Boundary Validation** -- Parse Python AST to extract all imports. Check imports against layer dependency rules (domain cannot import infrastructure, application cannot import interface, etc.). Block file writes that would introduce boundary violations.

3. **Implement V-039: AST Type Hint Enforcement** -- Parse function/method signatures via AST. Verify all public functions and methods have type annotations on parameters and return types. Flag missing type hints on public API surfaces.

4. **Implement V-040: AST Docstring Enforcement** -- Parse AST to check for docstrings on all public classes, functions, and methods. Verify presence (not content quality) of docstring nodes.

5. **Implement V-041: AST One-Class-Per-File Check** -- Count public class definitions per file via AST. Flag files with more than one public class (classes not prefixed with underscore).

6. **Enhance `scripts/pre_tool_use.py`** -- Integrate the enforcement engine into the existing PreToolUse hook. Route file write operations through the engine. Implement fail-open error handling: engine errors must not block user work (log and allow).

7. **Testing** -- Unit tests for each vector checker in isolation. Integration test for the hook end-to-end with mock tool calls. Verify `uv run pytest` passes.

**Design Source:** EPIC-002 EN-403/TASK-003 (PreToolUse design), EN-402 (priority analysis -- V-038 scored 4.92 WCS, highest priority vector)

## Acceptance Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| 1 | PreToolEnforcementEngine class created in `src/infrastructure/internal/enforcement/pre_tool_enforcement_engine.py` | [x] |
| 2 | V-038: AST import boundary validation implemented and blocks cross-layer violations | [x] |
| 3 | ~~V-039: AST type hint enforcement~~ | DEFERRED |
| 4 | ~~V-040: AST docstring enforcement~~ | DEFERRED |
| 5 | V-041: AST one-class-per-file check implemented | [x] |
| 6 | `scripts/pre_tool_use.py` enhanced with engine integration | [x] |
| 7 | Unit tests for implemented vectors (V-038, V-041) with happy path, negative, and edge cases | [x] |
| 8 | Integration test for hook end-to-end | [x] |
| 9 | Fail-open error handling: engine errors do not block user work | [x] |
| 10 | `uv run pytest` passes | [x] |

### AC #3 and #4 Deferral Note

ACs #3 (V-039: type hint enforcement) and #4 (V-040: docstring enforcement) are **DEFERRED to a follow-up enabler**. The EPIC-002 design phase (EN-403/TASK-003) explicitly classified V-039 and V-040 as "DESIGNED (not implemented)" for the initial implementation phase. The creator instructions for EN-703 focused on the two highest-priority vectors: V-038 (import boundary, WCS 4.92) and V-041 (one-class-per-file). The engine architecture (`_validate_content` method) is designed to be extended with additional check methods for V-039 and V-040 in a subsequent enabler without modifying existing code.

## Evidence

_No evidence yet. Will be populated during implementation._

## Dependencies

| Type | Item | Description |
|------|------|-------------|
| depends_on | EN-402 | Enforcement priority analysis (V-038 scored 4.92 WCS) |
| depends_on | EN-403 | Hook-based enforcement design (TASK-003: PreToolUse design) |
| related_to | EN-704 | Pre-commit gates (L5) catch what L3 misses |
| related_to | EN-705 | UserPromptSubmit hook (L2) compensates for L1 rot; L3 compensates for L2 |
| parent | FEAT-008 | Quality Framework Implementation |

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-14 | Claude | pending | Enabler created. Implements L3 Pre-Action Gating with vectors V-038, V-039, V-040, V-041. Design sourced from EPIC-002 EN-403/TASK-003 and EN-402 priority analysis. |
| 2026-02-14 | Claude | in_progress | Initial implementation (creator iteration 0): V-038 and V-041 implemented with 38 tests. V-039/V-040 deferred per EPIC-002 design phasing. |
| 2026-02-14 | Claude | in_progress | Adversarial critique iteration 1: score 0.8965, REVISE verdict. 2 critical, 3 major, 5 minor findings. |
| 2026-02-14 | Claude | in_progress | Creator revision iteration 1: Addressed all critique findings. ACs #3/#4 formally deferred in spec. EnforcementDecision extracted to own file (one-class-per-file compliance). Added false-positive mitigation for third-party imports. Added 11 new tests (importlib.import_module, bounded context paths, typing.TYPE_CHECKING attribute form, third-party false positives, idempotency). Documented dynamic-import block-vs-warn design deviation (DD-7). Total: 43 unit + 6 integration = 49 enforcement tests. |
