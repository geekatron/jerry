# EN-703 Adversarial Critique -- Iteration 1

> Agent: en703-critic (ps-critic)
> Date: 2026-02-14
> Strategies: FMEA, Red Team
> Verdict: REVISE

## Document Sections

| Section | Purpose |
|---------|---------|
| [Scoring](#scoring) | Weighted composite score across 6 dimensions |
| [Verdict](#verdict-revise) | Overall PASS/REVISE determination |
| [Steelman (H-16)](#steelman-h-16) | Acknowledging strengths before criticizing |
| [FMEA Analysis](#fmea-analysis) | Failure mode identification with RPN scores |
| [Red Team Findings](#red-team-findings) | Bypass attempts and evasion analysis |
| [Findings](#findings) | Classified findings (Critical, Major, Minor) |
| [Recommendations](#recommendations) | Specific, actionable improvements |

---

## Scoring

| Dimension | Weight | Score | Justification |
|-----------|--------|-------|---------------|
| Completeness | 0.20 | 0.82 | V-039 and V-040 deferred (ACs #3, #4 unmet). Creator instructions did not request them, but the EN-703 spec explicitly lists them as acceptance criteria. Deferral is documented but ACs remain unchecked. Additionally, missing tests for `importlib.import_module` boundary validation (only `__import__` is tested), no test for `typing.TYPE_CHECKING` attribute form, no determinism/idempotency test, no performance/large-file test. |
| Internal Consistency | 0.20 | 0.93 | Engine implementation matches rules file definitions well. Hook integration correctly delegates to engine. One inconsistency: the TASK-003 design specifies dynamic imports as warnings-only (REQ-403-035), but the engine blocks them. Another: design references `pretool_enforcement.py` but implementation uses `pre_tool_enforcement_engine.py`. Minor -- the design is a guide, not a spec. |
| Methodological Rigor | 0.20 | 0.88 | Strong AST-based approach with correct `ast.walk` usage. TYPE_CHECKING detection is well-implemented using identity comparison (`child is node`). However, several evasion vectors are unaddressed (see Red Team). The `_check_import_boundary` method uses naive string part-matching that produces false positives (e.g., a variable named `infrastructure` in a module path). The `replace(old_string, new_string, 1)` in `evaluate_edit` only replaces the first occurrence -- this matches the Edit tool semantics correctly. |
| Evidence Quality | 0.15 | 0.95 | All 38 new tests pass. 23 existing tests pass. Ruff clean. Tests cover happy path, negative, edge, and combined scenarios. Creator report is accurate -- test counts match. Integration tests run the actual hook subprocess. |
| Actionability | 0.15 | 0.92 | Code can be deployed as-is for V-038 and V-041 enforcement. Hook integration works. Fail-open behavior is sound. The `sys.path` manipulation in the hook is pragmatic if inelegant. One concern: the `sys.path.insert(0, _project_root)` could theoretically shadow other modules. |
| Traceability | 0.10 | 0.90 | Good traceability from engine code to design document (TASK-003). Requirements citations (REQ-403-xxx) in design. Docstrings reference EN-703, V-038, V-041. Missing: no explicit traceability from test cases to specific requirement IDs (tests reference V-038/V-041 by section, not individual REQs). |
| **Weighted Composite** | **1.00** | **0.8960** | Below 0.92 threshold -- REVISE required |

**Calculation:**
- (0.82 x 0.20) + (0.93 x 0.20) + (0.88 x 0.20) + (0.95 x 0.15) + (0.92 x 0.15) + (0.90 x 0.10)
- = 0.164 + 0.186 + 0.176 + 0.1425 + 0.138 + 0.090
- = **0.8965**

---

## Verdict: REVISE

The weighted composite score of **0.8965** falls below the **0.92** threshold required for C2+ deliverables (H-13). Two critical findings and three major findings require creator action before this can pass the quality gate.

---

## Steelman (H-16)

Before critiquing, the following strengths deserve explicit acknowledgment:

1. **Solid Architecture.** The enforcement engine is correctly placed in `src/infrastructure/internal/enforcement/` with stdlib-only imports. It follows the hexagonal architecture it enforces. The `EnforcementDecision` frozen dataclass is well-designed with sensible defaults.

2. **Fail-Open is Sound.** The fail-open error handling is implemented consistently across all code paths -- `evaluate_write`, `evaluate_edit`, `_validate_content`, and the hook integration. Every external-facing method wraps in `try/except` with approve-on-error. This is the right design choice for a development tool.

3. **TYPE_CHECKING Detection is Correct.** The AST-based TYPE_CHECKING detection using identity comparison (`child is node`) is the right approach. It correctly handles both `if TYPE_CHECKING:` and `if typing.TYPE_CHECKING:` attribute forms. It does not rely on fragile string matching.

4. **Edit Operation Coverage.** The `evaluate_edit` method correctly reads the existing file, applies the edit in-memory, and validates the resulting content. This closes the B-002 gap identified in the design document and ensures Edit operations get the same enforcement as Write operations.

5. **Backward Compatibility.** The Phase 3 integration in `pre_tool_use.py` is cleanly additive. All 23 existing hook tests pass. The lazy import with `ImportError` fallback ensures the existing security guardrails function even if the enforcement module is unavailable.

6. **Test Quality.** The 32 unit tests and 6 integration tests are well-structured with BDD naming, clear Arrange/Act/Assert patterns, and good use of `pytest` fixtures with `tmp_path`. The combined-violations test is a nice touch.

7. **Clean Separation of Concerns.** Rules are in `enforcement_rules.py`, engine logic in `pre_tool_enforcement_engine.py`, and hook integration in `pre_tool_use.py`. This follows the "enforcement logic separated from hook adapter" principle (REQ-403-080).

---

## FMEA Analysis

| # | Component | Failure Mode | Effect | Sev | Occ | Det | RPN | Mitigation |
|---|-----------|-------------|--------|-----|-----|-----|-----|------------|
| FM-1 | `_check_import_boundary` | False positive on module names containing layer keywords (e.g., `domain_utils.infrastructure_helpers`) | Legitimate code blocked erroneously | 7 | 3 | 5 | 105 | Change to check only the immediate path segment after `src.` rather than any part containing the keyword |
| FM-2 | `_is_type_checking_import` | User defines own `TYPE_CHECKING = True` variable to exempt runtime imports from boundary checking | Architecture violation bypasses enforcement | 8 | 2 | 7 | 112 | Accept risk -- AST cannot distinguish user-defined from `typing.TYPE_CHECKING`; L5 pre-commit catches this |
| FM-3 | `evaluate_edit` | File read race condition: file changes between read and edit application | Stale content validation; violation may pass or fail incorrectly | 4 | 2 | 8 | 64 | Accept risk -- Claude Code serializes tool calls; concurrent file modification is extremely unlikely |
| FM-4 | `_check_imports` (dynamic) | `exec("from src.infrastructure import X")` bypasses detection | Architecture violation enters codebase | 7 | 2 | 9 | 126 | Add `exec` call detection for strings containing import keywords; or accept as L5 responsibility |
| FM-5 | `_check_imports` (dynamic) | `importlib.import_module(variable)` not checked | Architecture violation via variable-based dynamic import | 6 | 3 | 8 | 144 | Accept risk for V1 -- documented in design (m-001). Dynamic imports with variable args cannot be statically validated. |
| FM-6 | `_determine_layer` | Bounded context paths (e.g., `src/session_management/domain/`) -- layer detection matches "domain" inside nested BC path | False layer assignment for BC-nested files | 5 | 4 | 5 | 100 | Need test coverage for bounded context paths; current behavior is actually correct but untested |
| FM-7 | `_check_one_class_per_file` | `@dataclass` and frozen dataclass co-located with engine class (e.g., `EnforcementDecision` + `PreToolEnforcementEngine`) | Engine's own file would be flagged if moved to domain | 3 | 2 | 3 | 18 | Accept -- `EnforcementDecision` is a data class co-located with its engine; acceptable per coding standards exception |
| FM-8 | Hook Phase 3 | `sys.path.insert(0, _project_root)` shadows other modules | Unexpected module resolution in subsequent imports | 5 | 1 | 7 | 35 | Low risk; only affects the hook process lifetime |
| FM-9 | `_is_validatable_python` | Relative path with no `src` prefix passed for a file actually under src/ | File incorrectly classified as non-validatable | 6 | 2 | 5 | 60 | The hook always passes absolute paths from `tool_input`; low real-world risk |
| FM-10 | `_check_governance_escalation` | Path traversal: `../../../.context/rules/` within an absolute path could match governance pattern | False governance escalation for unrelated files | 3 | 1 | 4 | 12 | Low risk -- paths are normalized; prefix matching after `relative_to` handles this |

### Top 3 RPN Risks:

1. **FM-5 (RPN 144):** Dynamic import with variable argument -- cannot be statically resolved. Accepted risk, documented.
2. **FM-4 (RPN 126):** `exec`-based import evasion -- not detected. Should be flagged as known limitation.
3. **FM-2 (RPN 112):** Self-defined `TYPE_CHECKING` variable exploits exemption. Architectural risk accepted for V1.

---

## Red Team Findings

### RT-1: Bare Layer Import Without `src.` Prefix (BYPASSES)

**Attack:** A domain file writes `from infrastructure.adapters import Adapter` (without the `src.` prefix).

**Analysis:** The `_check_import_boundary` method splits the import module by `.` and checks if any part is in `forbidden_layers`. The part `infrastructure` would be found in `RECOGNIZED_LAYERS` and `forbidden_layers` for a domain file. **This is actually detected correctly** because the method iterates through all module parts.

**Verdict:** NOT a bypass. The engine handles this case.

### RT-2: Aliased Import (`import src.infrastructure as infra`) (BYPASSES)

**Attack:** A domain file writes `import src.infrastructure.adapters as adapters`.

**Analysis:** This is an `ast.Import` node. The engine processes `alias.name` which is `src.infrastructure.adapters`. The part `infrastructure` would match. **This is correctly detected.**

**Verdict:** NOT a bypass.

### RT-3: `exec`-Based Import Evasion (BYPASSES)

**Attack:** `exec("from src.infrastructure.adapters import FileAdapter")` inside a domain module.

**Analysis:** The engine does not detect `exec` calls. The `_is_dynamic_import` method only checks for `__import__` and `importlib.import_module`. An `exec` call with an import statement would bypass enforcement entirely.

**Verdict:** BYPASS CONFIRMED. Severity: MAJOR. The design document (TASK-003 m-001) explicitly acknowledges this as an accepted limitation. However, no test documents this gap, and no warning is emitted.

### RT-4: `importlib.import_module(variable)` (BYPASSES)

**Attack:** `importlib.import_module(module_name)` where `module_name` is a variable, not a string constant.

**Analysis:** The engine's dynamic import handling in `_check_imports` checks `node.args[0]` for `ast.Constant`. If the argument is a variable (`ast.Name`), no boundary check occurs. The engine currently **blocks** `__import__("src.infrastructure.adapters")` correctly but silently approves `importlib.import_module(some_var)` where `some_var` could resolve to a boundary-violating module.

**Verdict:** BYPASS CONFIRMED but ACCEPTED RISK. The design explicitly documents this (m-001). Static analysis cannot resolve variable values. L5 pre-commit catches runtime violations.

### RT-5: Nested Public Classes (DOES NOT BYPASS)

**Attack:** Place two public classes as nested classes inside one outer class.

**Analysis:** The `_check_one_class_per_file` uses `ast.iter_child_nodes(tree)` which only iterates top-level nodes. Nested classes are not counted. The design intent is "one public **top-level** class per file." Nested classes inside an outer class are a legitimate pattern.

**Verdict:** NOT a bypass. Design intent correctly implemented.

### RT-6: Self-Defined `TYPE_CHECKING` Variable (BYPASSES)

**Attack:** Define `TYPE_CHECKING = True` locally (not from `typing`) and use `if TYPE_CHECKING:` to guard forbidden imports that are actually executed at runtime.

**Analysis:** The `_is_type_checking_import` method checks for `ast.Name` with `id == "TYPE_CHECKING"` or `ast.Attribute` with `attr == "TYPE_CHECKING"`. It does NOT verify that `TYPE_CHECKING` was imported from `typing`. A developer could write:
```python
TYPE_CHECKING = True
if TYPE_CHECKING:
    from src.infrastructure.adapters import Adapter  # Actually runs at runtime!
```
The engine would exempt this import. Combined with `from __future__ import annotations`, the runtime import would succeed and the boundary violation would pass enforcement.

**Verdict:** BYPASS CONFIRMED. Severity: MAJOR. However, this is a deliberate evasion requiring intentional abuse. Natural code patterns always import `TYPE_CHECKING` from `typing`. The risk is low-probability but the engine should ideally verify the import source. This can be deferred as L5 responsibility.

### RT-7: `__import__` Dynamic Import -- Boundary Check Logic (DEVIATION FROM DESIGN)

**Attack:** Verify that `__import__("src.infrastructure.adapters")` in a domain file is handled correctly.

**Analysis:** The implementation wraps the boundary violation message with `f"Dynamic import violation: {violation}"`. The test `test_evaluate_write_when_dynamic_import_then_blocks` verifies this works. However, the design document (TASK-003) says dynamic imports should be **flagged as warnings** (per REQ-403-035), but the implementation **blocks** them. This is a deviation from the design -- though arguably a more conservative choice.

**Verdict:** DEVIATION, not a bypass. The implementation is MORE strict than the design specifies. This should be documented as an intentional deviation or aligned with the design.

### RT-8: Denial-of-Service via Large File (POTENTIAL ISSUE)

**Attack:** Write a Python file with 100K+ lines to cause `ast.parse()` to take excessive time.

**Analysis:** The design document specifies a 500ms latency target. For typical files (<1000 lines), `ast.parse()` is fast. For very large files (>5000 lines), it may approach the budget. There is no file-size guard or timeout in the engine. However, the hook is invoked by Claude Code with its own timeout configuration, providing an external safety net.

**Verdict:** LOW RISK. Claude Code's hook timeout provides external protection. No action required for V1.

### RT-9: `NotebookEdit` Tool Not Handled (GAP)

**Attack:** Use the `NotebookEdit` tool to inject Python code with architecture violations into a `.ipynb` file that is later converted to `.py`.

**Analysis:** The hook only checks `Write` and `Edit` tools in Phase 3. `NotebookEdit` is not intercepted. However, notebooks are typically not in `src/` and are not subject to architecture enforcement. This is acceptable.

**Verdict:** NOT a meaningful gap for current architecture.

---

## Findings

### Critical

**C-1: AC #3 (V-039) and AC #4 (V-040) Not Implemented -- 2 of 10 ACs Unmet**

The EN-703 enabler spec (acceptance criteria table) explicitly lists:
- AC #3: "V-039: AST type hint enforcement implemented for public functions/methods"
- AC #4: "V-040: AST docstring enforcement implemented for public classes/functions/methods"

These are not implemented. The creator report marks them as "DEFERRED" with justification that "the creator instructions explicitly focused on V-038 and V-041." However, the acceptance criteria are the definition of done for the enabler, not the creator instructions. The deliverable cannot pass the quality gate with 2 of 10 ACs unmet (80% AC coverage).

**Remediation:** Either (a) implement V-039 and V-040, or (b) formally amend the EN-703 enabler spec to remove ACs #3 and #4 and add them to a follow-up enabler. Option (b) is acceptable if V-039/V-040 complexity justifies separate enablers.

**C-2: `_check_import_boundary` False Positive Risk on Module Part Matching**

The boundary check iterates through ALL parts of an import module name:
```python
for part in module_parts:
    if part in RECOGNIZED_LAYERS and part in forbidden_layers:
        return violation
```

This means an import like `from some_library.domain_tools import helper` would trigger a false positive because `domain` is not actually a part here -- wait, actually `domain_tools` would NOT match `domain` since they're separate parts after `split(".")`. Let me reconsider.

Actually, the split is on `.`, so `some_library.domain_tools` splits to `["some_library", "domain_tools"]`. The part `domain_tools` does NOT equal `domain`, so no false positive. However, consider: `from my_package.domain.util import X` -- the part `domain` DOES match. If a third-party library happens to have a `domain` subpackage, this would cause a false positive.

**Downgrade to MAJOR.** Third-party imports with a `domain` or `infrastructure` path segment would be falsely flagged. This is unlikely in practice for domain-layer files (which should have no third-party imports per the architecture rules) but could affect `infrastructure` layer files importing third-party packages with an `interface` subpackage.

### Major

**M-1: Missing Test for `importlib.import_module()` Boundary Check**

The test `test_evaluate_write_when_dynamic_import_then_blocks` only tests `__import__("src.infrastructure.adapters")`. There is no test for `importlib.import_module("src.infrastructure.adapters")`. While the code handles both patterns, the test gap means regressions in `importlib` detection would go unnoticed.

**Remediation:** Add a test case for `importlib.import_module` with a constant string argument violating boundaries.

**M-2: Missing Test for Bounded Context Paths**

The engine's `_determine_layer` method searches for layer names in path parts. For bounded context paths like `src/session_management/domain/entities/work_item.py`, the method would find `domain` and correctly identify the layer. However, there is no test for this important real-world path pattern. The project's architecture (per `architecture-standards.md`) explicitly uses bounded contexts with nested layer directories.

**Remediation:** Add test cases for bounded context paths (e.g., `src/session_management/domain/`, `src/work_tracking/application/`).

**M-3: Dynamic Import Blocks vs. Design Spec Warns**

The design document (TASK-003, REQ-403-035) specifies: "Dynamic import detection is flagged as warnings (not blocking)." The implementation blocks dynamic imports that resolve to a boundary violation. This is inconsistent with the design specification.

Either:
- (a) The implementation should warn (not block) for dynamic imports, matching the design.
- (b) The deviation should be explicitly documented in the creator report as an intentional upgrade.

The creator report does not mention this behavioral difference.

**Remediation:** Document the deviation in the creator report and add a design decision entry justifying the stricter behavior, OR change the behavior to warn instead of block.

### Minor

**m-1: `EnforcementDecision` Co-Located with Engine Violates One-Class-Per-File**

The `pre_tool_enforcement_engine.py` file contains two public constructs: `EnforcementDecision` (a frozen dataclass) and `PreToolEnforcementEngine` (the engine class). The creator report acknowledges this as "data class co-location is an accepted exception." This is consistent with the coding standards exception for "Related small value objects" but should be explicitly noted.

**m-2: No `__init__.py` in `tests/unit/enforcement/`**

The creator report mentions creating `tests/unit/enforcement/__init__.py` but I could not verify its existence during this review (it was not in the files to review). If missing, pytest may have issues with module collection in some configurations.

**m-3: Creator Report Test Count Discrepancy**

The creator report states "32 passed" for unit tests. The actual test file contains 7 test classes with tests totaling: 11 (V038) + 5 (V041) + 5 (Governance) + 4 (ErrorHandling) + 4 (EditOps) + 2 (Decision) + 1 (Combined) = **32 tests**. Running the tests shows **32 passed** in unit tests and **6 passed** in integration. Total = **38 new tests**. The creator report says "38 new tests" in one place and "32 unit tests" in another -- these are consistent (32 unit + 6 integration = 38).

**However**, the creator report says the grand total is 61 (38 + 23 existing). Running all three test files: 32 + 6 + 23 = **61 passed**. This is accurate.

No issue -- just verified consistency.

**m-4: Hook `sys.path` Manipulation Could Be Cleaner**

The hook adds `_project_root` to `sys.path` with:
```python
_project_root = str(Path(__file__).resolve().parent.parent)
```

This relies on `pre_tool_use.py` being at `scripts/pre_tool_use.py` (two levels from root). If the file is moved, the path calculation breaks silently (fail-open due to `ImportError`). A more robust approach would search for `CLAUDE.md` upward, matching the engine's own `_find_root()`.

**m-5: Missing Test for `typing.TYPE_CHECKING` Attribute Access Form**

The `_is_type_checking_import` method handles both `if TYPE_CHECKING:` and `if <something>.TYPE_CHECKING:`. However, the test only covers the `if TYPE_CHECKING:` form (Name node). There is no test for `if typing.TYPE_CHECKING:` (Attribute node). While the code handles both, the test gap could allow regression.

---

## Recommendations

### Must-Fix (for REVISE iteration):

1. **Address AC #3/#4 Deferral Formally.** Either implement V-039/V-040 or amend the EN-703 spec to split them into a separate enabler (e.g., EN-703a). The current state of "DEFERRED" in the creator report without amending the enabler spec leaves ACs unchecked, which blocks quality gate passage on Completeness.

2. **Add Missing Test Cases.** The following tests should be added:
   - `importlib.import_module("src.infrastructure.adapters")` in domain file (dynamic import variant)
   - Bounded context path: `src/session_management/domain/entity.py` with infrastructure import
   - `if typing.TYPE_CHECKING:` attribute access form
   - Idempotency test: same input produces same output across multiple calls

3. **Document Dynamic Import Block vs. Warn Deviation.** Add a design decision entry in the creator report explaining why dynamic imports are blocked rather than warned, or change behavior to match REQ-403-035.

### Should-Fix:

4. **Add `exec`-Based Import Detection as Known Limitation.** While not required for V1, add a code comment and test documenting that `exec("from src.infrastructure import X")` is a known evasion vector that L5 handles.

5. **Add False-Positive Mitigation for Third-Party Imports.** Consider restricting import boundary checking to imports that start with `src.` or contain a recognized project prefix. This avoids false positives from third-party libraries with `domain`, `infrastructure`, or `interface` in their package structure.

### May-Fix:

6. **Extract `EnforcementDecision` to its own file** (`enforcement_decision.py`) for strict one-class-per-file compliance.

7. **Make hook `sys.path` resolution more robust** by using the same `_find_root()` pattern as the engine.

---

*Agent: en703-critic (ps-critic)*
*Date: 2026-02-14*
*Strategies: FMEA (10 failure modes analyzed), Red Team (9 bypass attempts)*
*Quality Gate: 0.8965 < 0.92 -- REVISE*
