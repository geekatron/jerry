# EN-818 Critic Report -- Iteration 2

> **Critic:** ps-critic (opus) | **Protocol:** S-014 C4 LLM-as-Judge
> **Enabler:** EN-818 Template Validation CI Gate
> **Date:** 2026-02-15
> **Iteration:** 2
> **Prior Score:** 0.888 (REVISE)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Prior Finding Verification](#prior-finding-verification) | Evidence-based verification of iteration 1 remediation |
| [New Findings](#new-findings) | Issues introduced or surfaced by the revision |
| [Dimension Scores](#dimension-scores) | 6-dimension weighted rubric scoring |
| [Gate Decision](#gate-decision) | PASS/REVISE with threshold comparison |
| [Score Progression](#score-progression) | Iteration-over-iteration tracking |

---

## Prior Finding Verification

### F-001 (Critical): Operator Precedence Bug -- RESOLVED

**Original:** `and` binds tighter than `or` in `check_scoring_rubric_tables`, making the third clause fragile.

**Evidence of fix (lines 432-436 of `scripts/validate_templates.py`):**

```python
has_dimension_weights = (
    "Dimension Weights" in rubric_content
    or "dimension weights" in rubric_content
    or ("Dimension" in rubric_content and "Weight" in rubric_content)
)
```

**Verification:** Explicit parentheses now wrap the `and` clause on line 435. The logical semantics are correct: the fallback check requires BOTH "Dimension" AND "Weight" to be present. The three-clause `or` chain is now unambiguous regardless of operator precedence. **RESOLVED.**

---

### F-002 (Major): Double Validation in Summary -- RESOLVED

**Original:** `validate_template()` called twice per template -- once in the loop, once in the summary `sum()` generator.

**Evidence of fix (lines 726-749 of `scripts/validate_templates.py`):**

```python
validations = []
for template_path in template_files:
    validation = validate_template(template_path)
    validations.append(validation)
    ...

# Print summary
passed_count = sum(1 for v in validations if v.passed)
failed_count = len(template_files) - passed_count
```

**Verification:** Validation results are now collected into a `validations` list during the first (and only) loop pass. The summary `passed_count` is computed from the cached `validations` list without re-invoking `validate_template()`. File reads go from 20 to 10 and regex operations from 160 to 80. **RESOLVED.**

---

### F-003 (Major): Missing Section Ordering Check -- RESOLVED

**Original:** `check_all_sections_present()` checked only presence, not canonical order.

**Evidence of fix (lines 186-222 of `scripts/validate_templates.py`):**

```python
section_positions = {}
for section in CANONICAL_SECTIONS:
    position = None
    for idx, heading in enumerate(headings):
        if section in heading or heading.endswith(f": {section}"):
            position = idx
            break
    if position is None:
        missing_sections.append(section)
    else:
        section_positions[section] = position

# Check section ordering (positions should be monotonically increasing)
positions = [section_positions[section] for section in CANONICAL_SECTIONS]
if positions != sorted(positions):
    return ValidationResult(
        check_name="All 8 canonical sections",
        passed=False,
        message="Sections are not in canonical order",
    )
```

**Verification:** The function now tracks the heading index of each canonical section in `section_positions`, then verifies the position sequence is monotonically increasing by comparing `positions` to `sorted(positions)`. A template with sections out of order (e.g., Examples before Execution Protocol) would now fail validation. The success message has been updated to "All sections present and in order". **RESOLVED.**

---

### F-004 (Major): Missing Metadata Blockquote Check -- RESOLVED

**Original:** No validation that templates contain the required metadata blockquote header.

**Evidence of fix (lines 491-508 of `scripts/validate_templates.py`):**

```python
def check_metadata_blockquote(content: str) -> ValidationResult:
    """Check that template contains a metadata blockquote with required fields."""
    has_type_metadata = re.search(r"^>\s+\*\*Type:\*\*", content, re.MULTILINE)
    has_status_metadata = re.search(r"^>\s+\*\*Status:\*\*", content, re.MULTILINE)

    if not (has_type_metadata or has_status_metadata):
        return ValidationResult(
            check_name="Metadata blockquote",
            passed=False,
            message="No metadata blockquote found with Type or Status fields",
        )
```

**Verification:** New `check_metadata_blockquote()` function checks for blockquote lines (`> **Type:**` or `> **Status:**`) using regex with `re.MULTILINE` to match at line start. Cross-referenced against the sample template `s-001-red-team.md` which contains `> **Type:** adversarial-strategy-template` and `> **Status:** ACTIVE` -- these patterns will match. The check is included in the `validate_template()` check list at line 661. **RESOLVED.**

---

### F-006 (Major): Identity Field Values Not Validated Against SSOT -- RESOLVED

**Original:** Strategy ID field value not validated against the known catalog.

**Evidence of fix (lines 69-81, 288-295 of `scripts/validate_templates.py`):**

```python
VALID_STRATEGY_IDS = {
    "S-001", "S-002", "S-003", "S-004", "S-007",
    "S-010", "S-011", "S-012", "S-013", "S-014",
}

# ... inside check_identity_fields():
strategy_id = fields.get("Strategy ID", "")
if strategy_id not in VALID_STRATEGY_IDS:
    return ValidationResult(
        check_name="Identity section fields",
        passed=False,
        message=f"Strategy ID '{strategy_id}' not in SSOT (expected one of {sorted(VALID_STRATEGY_IDS)})",
    )
```

**Verification:** The `VALID_STRATEGY_IDS` set contains exactly the 10 selected strategy IDs from `quality-enforcement.md` SSOT. Cross-verified: SSOT Strategy Catalog lists S-001, S-002, S-003, S-004, S-007, S-010, S-011, S-012, S-013, S-014 -- exact match. The validation now rejects any template with a Strategy ID not in this set (e.g., `S-999` would fail). The error message includes the full valid set for developer guidance. **RESOLVED.**

---

### F-007 (Major): Missing Per-Section Content Checks -- RESOLVED

**Original:** 5 of 8 section groups had no validation coverage.

**Evidence of fix (lines 511-619 of `scripts/validate_templates.py`):**

Three new check functions added:

1. **`check_purpose_section_content()`** (lines 511-548): Extracts Purpose section, verifies `### When to Use` and `### When NOT to Use` subheadings exist via `re.MULTILINE` regex.

2. **`check_integration_section_content()`** (lines 551-584): Extracts Integration section, verifies C1, C2, C3, C4 all appear in the content.

3. **`check_examples_section_structure()`** (lines 587-619): Extracts Examples section, checks for "Before", "After", or "Example" keywords.

All three are included in the `validate_template()` check list (lines 662-664). The script docstring (lines 14, 19-20) documents these new checks.

**Verification:** The total check count is now 12, up from 8 in iteration 1. The three highest-value missing checks recommended in F-007 have all been implemented. The remaining gaps (Prerequisites section input checklist, Output Format 6-section structure, Scoring Rubric strategy-specific bands) are lower priority and were not required for threshold attainment. **RESOLVED.**

---

### F-005 (Minor): File Length Check Missing -- ACKNOWLEDGED (No Change)

**Status:** Correctly scoped out. TEMPLATE-FORMAT.md uses SHOULD language (MEDIUM tier). The script focuses on HARD-tier structural requirements. Absence of this check does not impact the quality gate for HARD compliance. **ACCEPTED.**

---

### F-008 (Minor): CI Job `uv sync` Without `--extra test` -- ACKNOWLEDGED (No Change)

**Status:** Correctly identified as a non-issue. The validation script uses only stdlib imports. The CI job is correct as-is. **ACCEPTED.**

---

### F-009 (Minor): Criticality Tier Table Check Shallow -- ACKNOWLEDGED (No Change)

**Status:** The check at lines 304-336 still uses string search for "Criticality Tier". While shallow, it provides a gate that catches completely missing criticality content. The new `check_integration_section_content()` function (F-007 fix) adds C1-C4 verification in the Integration section, which provides complementary structural coverage. **ACCEPTED.**

---

### F-010 (Minor): Verbose Mode Test Weak Assertion -- ACKNOWLEDGED (No Change)

**Status:** The test at lines 715-727 of the E2E file still asserts `"s-001-red-team.md" in result.stdout or "S-001" in result.stdout`. While this does not distinguish verbose from non-verbose output, both modes do produce template names. The test's primary purpose is to verify the `--verbose` flag does not cause a crash and produces output -- it serves this purpose. **ACCEPTED.**

---

### F-011 (Minor): Pre-commit Hook Pattern Matches TEMPLATE-FORMAT.md -- ACKNOWLEDGED (No Change)

**Status:** Intentional behavior. Editing the format document should trigger re-validation of strategy templates to catch format drift. **ACCEPTED.**

---

## New Findings

### F-012: `check_examples_section_structure` Uses Overly Permissive OR Logic

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **File** | `scripts/validate_templates.py` lines 603-608 |

**Evidence:**

```python
has_before = "Before" in examples_content or "before" in examples_content
has_after = "After" in examples_content or "after" in examples_content
has_example = "Example" in examples_content or "example" in examples_content

if not (has_before or has_after or has_example):
```

**Analysis:** The check requires only ONE of Before, After, or Example to be present (any single word suffices). A template containing only the word "example" in a sentence like "For example, consider..." would pass. The TEMPLATE-FORMAT.md specifies a Before/After transformation pattern as the expected structure. The validation should ideally require at least TWO of these keywords (e.g., Before AND After) to verify the transformation pattern.

However, this is Minor because: (1) all 10 current templates contain rich Examples sections with all three keywords; (2) the `check_examples_content()` function separately enforces a 200-character minimum, preventing trivially thin content; and (3) the E2E tests in `TestTemplateContentQuality` provide a secondary check.

**Recommendation:** Consider tightening to require `(has_before and has_after) or has_example` to match the Before/After transformation pattern intent. Low priority.

---

### F-013: `check_integration_section_content` C1-C4 Check Is Not Table-Aware

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **File** | `scripts/validate_templates.py` lines 567-573 |

**Evidence:**

```python
has_c1 = "C1" in integration_content
has_c2 = "C2" in integration_content
has_c3 = "C3" in integration_content
has_c4 = "C4" in integration_content
```

**Analysis:** The check looks for the literal strings "C1" through "C4" anywhere in the Integration section. This would match a prose mention like "As discussed in C1 Routine contexts..." without verifying that an actual criticality table exists with C1-C4 rows. However, this is Minor because: (1) all 10 current templates have proper criticality tables in the Integration section, (2) the string search does verify that all four levels are at least referenced, and (3) the E2E test `test_skill_md_when_read_then_contains_correct_criticality_mapping` provides deeper structural verification.

**Recommendation:** Consider enhancing to detect table row patterns like `| C1 |` or `| C2 |`. Low priority.

---

### F-014: `VALID_STRATEGY_IDS` Set Is Hardcoded, Not Derived from SSOT at Runtime

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **File** | `scripts/validate_templates.py` lines 69-81 |

**Evidence:**

```python
VALID_STRATEGY_IDS = {
    "S-001", "S-002", "S-003", "S-004", "S-007",
    "S-010", "S-011", "S-012", "S-013", "S-014",
}
```

**Analysis:** The valid strategy IDs are hardcoded in the script rather than being read from `quality-enforcement.md` at runtime. If the SSOT is updated (e.g., a strategy is added or removed), the script would need a manual code update. This is a minor maintainability concern. However, for a CI validation script, hardcoded constants are actually a defensible design choice: they provide deterministic behavior, avoid runtime file parsing complexity, and make the validation self-contained. The E2E test suite provides the dynamic SSOT cross-check.

**Recommendation:** Acceptable as-is. Document the SSOT provenance in a comment (already partially done at line 69: "Valid Strategy IDs from quality-enforcement.md SSOT"). If the strategy catalog changes, the script comment and set will need updating. No change required.

---

## Dimension Scores

| Dimension | Score | Weight | Weighted | Evidence |
|-----------|-------|--------|----------|----------|
| Completeness | 0.92 | 0.20 | 0.184 | Script now implements 12 validation checks (up from 8), covering sections 1-8 with at least one content check per section group. F-003 (ordering), F-004 (metadata blockquote), F-006 (SSOT validation), F-007 (3 new content checks) all resolved. Remaining gaps are limited to deeper structural checks within sections (e.g., step format within Execution Protocol, 6-section Output Format verification) which are MEDIUM-tier concerns. Pre-commit hook, CI job, and E2E tests all present. Script docstring accurately reflects the 12 checks. |
| Internal Consistency | 0.95 | 0.20 | 0.190 | F-001 operator precedence bug fixed -- expression is now unambiguous. F-002 double validation eliminated -- summary computed from cached results. Script docstring (lines 2-33) accurately documents all 12 checks and matches the actual implementation. `VALID_STRATEGY_IDS` set matches the SSOT Strategy Catalog exactly (cross-verified). `CANONICAL_SECTIONS` list matches TEMPLATE-FORMAT.md. The `TemplateValidation` NamedTuple and `ValidationResult` NamedTuple provide a consistent data model. Check names in output match check function names. |
| Methodological Rigor | 0.93 | 0.20 | 0.186 | BDD test naming convention consistently followed in E2E tests. Script uses clean separation of concerns: constants, data structures, helpers, check functions, orchestration, main. Section ordering verification uses a sound algorithm (monotonic position check). Identity field validation uses set membership against SSOT constants. New content checks use `re.MULTILINE` regex for heading detection, which is the correct approach for markdown structure. The 12-check architecture covers structural, content, and SSOT-consistency dimensions of template validation. Minor: some new checks (F-012, F-013) use shallow string search rather than structural table parsing, but this is a pragmatic tradeoff documented in the acknowledged findings. |
| Evidence Quality | 0.94 | 0.15 | 0.141 | Script produces clear PASS/FAIL output per template with check-level detail in verbose mode. 12 checks provide granular failure diagnostics with specific messages (e.g., "Missing sections: X, Y", "Strategy ID 'S-999' not in SSOT", "Sections are not in canonical order"). E2E `TestTemplateValidationScript` class provides 5 subprocess-based tests verifying script existence, exit code 0, verbose output, pre-commit hook presence, and CI job presence. All 186 tests pass, 1 skipped. Template validation: 10/10 PASS. |
| Actionability | 0.95 | 0.15 | 0.143 | All four deliverables (script, pre-commit hook, CI job, E2E tests) are immediately operational. Pre-commit hook triggers correctly on `.context/templates/adversarial/*.md` pattern. CI job is integrated into the `ci-success` dependency chain (line 410). Script exit code 0/1 semantics are correct for CI gate behavior. Error messages include specific file names, check names, and remediation hints (e.g., listing valid strategy IDs on SSOT mismatch). The `--verbose` flag provides developer-friendly detailed output. |
| Traceability | 0.93 | 0.10 | 0.093 | Script docstring references EN-818, TEMPLATE-FORMAT.md, and quality-enforcement.md (lines 27-29). CI job section header contains EN-818 reference (line 143). Pre-commit section header contains EN-818 reference (line 130). E2E test class `TestTemplateValidationScript` is clearly attributable to EN-818. `VALID_STRATEGY_IDS` comment (line 69) traces to quality-enforcement.md SSOT. `CANONICAL_SECTIONS` matches TEMPLATE-FORMAT.md specification. Minor: the E2E test module docstring still references EN-812 rather than EN-818, but the class-level test coverage for EN-818 is clearly delineated. |

**Weighted Composite: 0.937**

Calculation: (0.184) + (0.190) + (0.186) + (0.141) + (0.143) + (0.093) = **0.937**

---

## Gate Decision

**PASS** (0.937 >= 0.920 threshold)

---

## Score Progression

| Iteration | Score | Decision | Key Changes |
|-----------|-------|----------|-------------|
| 1 | 0.888 | REVISE | 8 checks, operator precedence bug, double validation, missing ordering/metadata/SSOT checks |
| 2 | 0.937 | PASS | 12 checks, all 6 critical/major findings resolved, 3 new minor findings (accepted) |

**Delta: +0.049** (+5.5% improvement)

**Dimension-level progression:**

| Dimension | Iter 1 | Iter 2 | Delta |
|-----------|--------|--------|-------|
| Completeness | 0.82 | 0.92 | +0.10 |
| Internal Consistency | 0.90 | 0.95 | +0.05 |
| Methodological Rigor | 0.88 | 0.93 | +0.05 |
| Evidence Quality | 0.92 | 0.94 | +0.02 |
| Actionability | 0.93 | 0.95 | +0.02 |
| Traceability | 0.90 | 0.93 | +0.03 |

The largest improvement is in **Completeness** (+0.10), driven by the addition of 4 new validation checks addressing F-003, F-004, F-006, and F-007. **Internal Consistency** gained +0.05 from the F-001 operator precedence fix and F-002 double-validation elimination. **Methodological Rigor** improved +0.05 from the addition of algorithmic ordering verification and SSOT set-membership validation.

---

## Summary

The EN-818 revision successfully resolves all 6 critical and major findings from iteration 1. The validation script now provides 12 checks (up from 8) covering structural integrity, content presence, SSOT consistency, and section ordering. The operator precedence bug (F-001) is fixed with explicit parentheses, the double-validation performance issue (F-002) is eliminated with cached results, and the validation coverage has been extended to include metadata blockquote checks, section ordering verification, SSOT Strategy ID validation, Purpose section content checks, Integration section C1-C4 verification, and Examples section structure checks.

Three new minor findings (F-012 through F-014) were identified, all relating to the depth of string-based validation in the new checks. These are pragmatic tradeoffs that do not impact the deliverable's fitness for purpose. The script, pre-commit hook, CI job, and E2E tests form a complete, operational CI gate for template format compliance.

The weighted composite score of **0.937** exceeds the 0.920 C4 quality threshold. **Gate decision: PASS.**
