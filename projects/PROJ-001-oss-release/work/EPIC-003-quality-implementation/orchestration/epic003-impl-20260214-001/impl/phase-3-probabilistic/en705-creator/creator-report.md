# EN-705 Creator Report: L2 Per-Prompt Reinforcement Hook

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What was implemented |
| [Files Created](#files-created) | New files with descriptions |
| [Files Modified](#files-modified) | Changed files with descriptions |
| [Design Decisions](#design-decisions) | Architectural choices and rationale |
| [Acceptance Criteria Coverage](#acceptance-criteria-coverage) | AC mapping |
| [Test Results](#test-results) | Test counts and outcomes |
| [Constraints Compliance](#constraints-compliance) | HARD rule compliance verification |

---

## Summary

Implemented the L2 Per-Prompt Reinforcement hook for the Jerry Framework quality enforcement architecture. This hook runs on every user prompt submission via the `UserPromptSubmit` Claude Code hook event, extracting critical quality rules from `quality-enforcement.md` L2-REINJECT markers and injecting them as `additionalContext` to combat context rot.

The implementation follows hexagonal architecture: the enforcement logic resides in `PromptReinforcementEngine` (infrastructure/internal/enforcement), while the hook adapter in `hooks/user-prompt-submit.py` handles the Claude Code protocol translation.

---

## Files Created

| File | Purpose |
|------|---------|
| `src/infrastructure/internal/enforcement/reinforcement_content.py` | Frozen dataclass for structured reinforcement result (preamble, token estimate, item counts) |
| `src/infrastructure/internal/enforcement/prompt_reinforcement_engine.py` | Core engine: parses L2-REINJECT markers, sorts by rank, assembles within 600-token budget |
| `hooks/user-prompt-submit.py` | Claude Code UserPromptSubmit hook adapter; reads stdin JSON, generates reinforcement, writes stdout JSON |
| `tests/unit/enforcement/test_prompt_reinforcement_engine.py` | 33 unit tests across 6 test classes |
| `tests/integration/test_userpromptsubmit_hook_integration.py` | 4 integration tests via subprocess |

## Files Modified

| File | Change |
|------|--------|
| `hooks/hooks.json` | Added `UserPromptSubmit` event entry with matcher `*` and 5000ms timeout |
| `schemas/hooks.schema.json` | Added `UserPromptSubmit` to allowed hook types in the hooks object properties |
| `src/infrastructure/internal/enforcement/__init__.py` | Added exports for `PromptReinforcementEngine` and `ReinforcementContent` |

---

## Design Decisions

### DD-1: One-Class-Per-File Split

The `ReinforcementContent` dataclass was separated into its own file (`reinforcement_content.py`) to comply with H-10 (one class per file). This follows the existing pattern where `EnforcementDecision` is in a separate file from `PreToolEnforcementEngine`.

### DD-2: Fail-Open Architecture

The engine and hook both implement fail-open behavior. Any error (missing file, malformed markers, parse failures, import errors) results in an empty reinforcement -- user work is NEVER blocked. This matches the fail-open pattern established by `PreToolEnforcementEngine`.

### DD-3: Token Estimation Formula

Used `chars/4 * 0.83` with ceiling rounding as specified. The 0.83 calibration factor provides a conservative estimate for English text with technical content. The engine estimates tokens for each marker individually during assembly, and recalculates for the final joined preamble.

### DD-4: Rank-Based Assembly

Markers are sorted by rank ascending (lower rank = higher priority). Items are added in rank order until the token budget is exhausted. This ensures the most critical rules are always included even under tight budgets.

### DD-5: Hook Location in hooks/ Directory

The hook script is placed in `hooks/user-prompt-submit.py` (not `scripts/`) because it uses the Claude Code hook protocol (stdin JSON / stdout JSON) and is invoked directly by the hooks.json configuration. This follows the pattern where hook adapters live in `hooks/` while the session_start_hook uses `scripts/` for historical reasons.

### DD-6: Schema Update

Added `UserPromptSubmit` to `schemas/hooks.schema.json` to prevent contract test failures. The schema validation enforces `additionalProperties: false` on the hooks object, so any new hook type must be explicitly declared.

### DD-7: Stdlib-Only in Engine

The `PromptReinforcementEngine` uses only stdlib imports (`re`, `pathlib`, `dataclasses`). The only non-stdlib import is `ReinforcementContent` from the sibling module in the same enforcement package. This keeps the engine lightweight and avoids dependency issues.

---

## Acceptance Criteria Coverage

| AC | Description | Status | Evidence |
|----|-------------|--------|----------|
| Engine parses L2-REINJECT markers | Extract HTML comment markers from quality-enforcement.md | PASS | `TestParseReinjectMarkers` (8 tests) |
| Engine sorts by rank | Markers sorted ascending by rank value | PASS | `test_parse_markers_when_valid_content_then_sorted_by_rank` |
| Engine enforces 600-token budget | Assembly stops when budget exhausted | PASS | `TestBudgetEnforcement` (5 tests) |
| Token estimation uses chars/4 * 0.83 | Calibrated formula applied | PASS | `TestEstimateTokens` (6 tests) |
| Hook returns valid JSON | Claude Code protocol compliance | PASS | `test_hook_returns_valid_json_with_reinforcement` |
| Hook wraps in XML tags | `<quality-reinforcement>` wrapper | PASS | `test_hook_output_contains_quality_reinforcement_xml_tag` |
| Fail-open on errors | Missing file, malformed markers, etc. | PASS | `TestErrorHandling` (5 tests) + `test_hook_fails_open_on_missing_rules_file` |
| hooks.json updated | UserPromptSubmit event registered | PASS | Manual verification |
| One class per file | H-10 compliance | PASS | Separate files for ReinforcementContent and PromptReinforcementEngine |
| Type hints on all public functions | H-11 compliance | PASS | All public methods have type annotations |
| Docstrings on all public functions | H-12 compliance | PASS | Google-style docstrings on all public methods |
| Frozen dataclass | ReinforcementContent is immutable | PASS | `test_reinforcement_content_when_frozen_then_immutable` |

---

## Test Results

### Unit Tests: 33 passed

```
tests/unit/enforcement/test_prompt_reinforcement_engine.py   33 passed in 0.14s
```

| Test Class | Count | Coverage |
|------------|-------|----------|
| `TestParseReinjectMarkers` | 8 | Parsing, sorting, malformed, empty, single |
| `TestEstimateTokens` | 6 | Empty, short, formula, exact, single char |
| `TestGenerateReinforcement` | 5 | Valid file, ranked items, token estimate, determinism |
| `TestBudgetEnforcement` | 5 | Default, tiny, zero, large, exact budget |
| `TestErrorHandling` | 5 | Missing file, empty, no markers, malformed, directory |
| `TestReinforcementContent` | 4 | Attributes, frozen, equality, empty |

### Integration Tests: 4 passed

```
tests/integration/test_userpromptsubmit_hook_integration.py   4 passed in 0.45s
```

| Test | Description |
|------|-------------|
| `test_hook_returns_valid_json_with_reinforcement` | Full pipeline produces valid JSON output |
| `test_hook_output_contains_quality_reinforcement_xml_tag` | XML tags wrap content correctly |
| `test_hook_fails_open_on_missing_rules_file` | Graceful degradation when rules unavailable |
| `test_hook_always_exits_zero` | Exit code 0 even with invalid input |

### Full Suite Impact

- Before: 2704 passed, 4 failed (2 pre-existing architecture, 2 schema)
- After: 2706 passed, 2 failed (2 pre-existing architecture from EN-706)
- Net: +2 passed (schema failures fixed), +37 new tests, 0 regressions

---

## Constraints Compliance

| Constraint | Status |
|------------|--------|
| H-05: UV only for Python | PASS -- shebang uses `uv run python` |
| H-10: One class per file | PASS -- ReinforcementContent and PromptReinforcementEngine in separate files |
| H-11: Type hints on public functions | PASS -- all public methods annotated |
| H-12: Docstrings on public functions | PASS -- Google-style docstrings on all |
| Fail-open architecture | PASS -- errors never block user work |
| Stdlib-only in engine | PASS -- only re, pathlib, dataclasses + sibling import |
| Python 3.11+ | PASS -- uses `X | None` syntax, `from __future__ import annotations` |
