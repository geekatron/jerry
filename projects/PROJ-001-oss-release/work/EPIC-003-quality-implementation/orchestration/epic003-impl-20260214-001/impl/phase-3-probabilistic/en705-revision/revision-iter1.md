# EN-705 Revision Report -- Iteration 1

> Addresses adversarial critic findings from iteration 1 review (score: 0.945 PASS).

## Document Sections

| Section | Purpose |
|---------|---------|
| [Findings Addressed](#findings-addressed) | Summary of all fixes applied |
| [Changes Made](#changes-made) | File-level diff descriptions |
| [Test Results](#test-results) | Regression verification |

---

## Findings Addressed

| Finding | Severity | Status | Description |
|---------|----------|--------|-------------|
| MAJ-01 | Major | FIXED | Missing L2-REINJECT markers for constitutional principles, UV-only, and leniency bias |
| MIN-01 | Minor | FIXED | `tokens` metadata field parsed but never used -- documented limitation |
| MIN-04 | Minor | FIXED | No operational observability for successful hook execution |

---

## Changes Made

### MAJ-01: Missing L2-REINJECT markers in quality-enforcement.md

**File**: `.context/rules/quality-enforcement.md`

Added three new L2-REINJECT markers to the HARD Rule Index section, bringing the total from 4 to 7 markers. The new markers use ranks 1, 3, and 4 to slot in among the existing rank=2, 5, 6, 8 markers:

1. **rank=1** (highest priority): Constitutional principles P-003, P-020, P-022 -- HARD constraints that cannot be overridden.
2. **rank=3**: UV-only Python environment reminder (H-05/H-06).
3. **rank=4**: LLM-as-Judge scoring S-014 leniency bias calibration.

These ensure all five spec content items from the EN-705 specification are now represented as L2-REINJECT markers in the SSOT file.

### MIN-01: `tokens` metadata field documentation

**File**: `src/infrastructure/internal/enforcement/prompt_reinforcement_engine.py`

Added a `Note:` section to the `_parse_reinject_markers` docstring explaining that the `tokens` field is parsed for completeness and potential future use (e.g., pre-computed budgets), but the engine does NOT use it for budget decisions. Instead, it computes its own estimate via `_estimate_tokens()` to ensure consistency regardless of marker metadata accuracy.

### MIN-04: Operational observability for successful execution

**File**: `hooks/user-prompt-submit.py`

Added a debug stderr line emitted when reinforcement is successfully generated and the preamble is non-empty:

```python
print(
    f"L2 reinforce: {result.items_included}/{result.items_total} items, "
    f"~{result.token_estimate} tokens",
    file=sys.stderr,
)
```

This provides operational visibility into successful hook execution without affecting stdout (which carries the JSON response to Claude Code).

---

## Test Results

All 37 EN-705 tests pass with no regressions:

- **Unit tests**: 33/33 PASSED (`tests/unit/enforcement/test_prompt_reinforcement_engine.py`)
- **Integration tests**: 4/4 PASSED (`tests/integration/test_userpromptsubmit_hook_integration.py`)

```
============================== 37 passed in 0.47s ==============================
```

Unit tests are unaffected because they use a self-contained `SAMPLE_QUALITY_ENFORCEMENT` fixture with 4 markers. Integration tests pass because the hook correctly processes the updated quality-enforcement.md with 7 markers, all within the 600-token budget.

---

*Revision completed: 2026-02-14*
*Agent: EN-705 Revision Agent (Iteration 1)*
