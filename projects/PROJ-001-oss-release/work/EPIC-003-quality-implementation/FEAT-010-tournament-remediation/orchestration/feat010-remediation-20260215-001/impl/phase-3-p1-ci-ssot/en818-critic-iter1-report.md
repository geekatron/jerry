# EN-818 Critic Report -- Iteration 1

> **Critic:** ps-critic (opus) | **Protocol:** S-014 C4 LLM-as-Judge
> **Enabler:** EN-818 Template Validation CI Gate
> **Date:** 2026-02-15
> **Iteration:** 1

---

## Findings

### F-001: Operator Precedence Bug in `check_scoring_rubric_tables`

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **File** | `scripts/validate_templates.py` lines 384-389 |

**Evidence:**

```python
has_dimension_weights = (
    "Dimension Weights" in rubric_content
    or "dimension weights" in rubric_content
    or "Dimension" in rubric_content
    and "Weight" in rubric_content
)
```

**Analysis:** Due to Python operator precedence, `and` binds more tightly than `or`. This expression evaluates as:

```python
("Dimension Weights" in rubric_content) or
("dimension weights" in rubric_content) or
(("Dimension" in rubric_content) and ("Weight" in rubric_content))
```

While the third clause happens to produce the intended behavior in this specific case (checking both "Dimension" AND "Weight"), the second `or` means that if "Dimension Weights" is present as a literal string, the check passes without verifying that an actual table with "Weight" exists. More critically, any Scoring Rubric section containing just the word "Dimension" (e.g., in prose text like "each dimension is...") combined with "Weight" anywhere would pass even if no actual Dimension Weights table exists. The intended logic appears to be a fallback chain where the final case requires both words present, which accidentally works, but the expression is fragile and misleading. A correct parenthesized version should be:

```python
has_dimension_weights = (
    "Dimension Weights" in rubric_content
    or "dimension weights" in rubric_content
    or ("Dimension" in rubric_content and "Weight" in rubric_content)
)
```

**Recommendation:** Add explicit parentheses around the `and` clause to make intent clear and prevent regression if the expression is modified in the future.

---

### F-002: Double Validation in Summary -- O(2N) Performance Waste

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **File** | `scripts/validate_templates.py` lines 563-565 |

**Evidence:**

```python
# Print summary
passed_count = sum(1 for f in template_files if validate_template(f).passed)
failed_count = len(template_files) - passed_count
```

**Analysis:** The `main()` function already validates each template in the loop on lines 544-561 and tracks `all_passed`. However, the summary computation on line 564 calls `validate_template(f)` a second time for every template file, re-reading and re-parsing all 10 files. This doubles the total work. With 10 templates, this produces 20 file reads and 160 regex operations instead of 10 and 80 respectively. The `all_passed` boolean is already tracked but `passed_count` is not, despite being trivially derivable from the loop's existing `validation` results.

**Recommendation:** Collect validation results in a list during the first loop pass and compute `passed_count` from the cached results:

```python
validations = [validate_template(f) for f in template_files]
# ... use validations in the loop ...
passed_count = sum(1 for v in validations if v.passed)
```

---

### F-003: Missing Validation -- Section Ordering Not Checked

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **File** | `scripts/validate_templates.py` lines 158-184 |

**Evidence:** The TEMPLATE-FORMAT.md Validation Checklist (line 305) states:

> "All 8 canonical sections present **in order** (Identity, Purpose, Prerequisites, Execution Protocol, Output Format, Scoring Rubric, Examples, Integration)"

The script's `check_all_sections_present()` function checks only for presence using `any()` across all headings. It does not verify that the sections appear in the canonical order.

**Analysis:** A template with sections in the wrong order (e.g., Examples before Execution Protocol) would pass validation. This is a gap between the validation checklist specification and the script implementation.

**Recommendation:** After confirming all sections are present, extract the position index of each section in the headings list and verify they are monotonically increasing.

---

### F-004: Missing Validation -- Metadata Blockquote Header Not Checked

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **File** | `scripts/validate_templates.py` (missing check) |

**Evidence:** The TEMPLATE-FORMAT.md Validation Checklist (line 308) states:

> "Metadata blockquote header present"

Every strategy template begins with a blockquote metadata header (e.g., `> **Type:** adversarial-strategy-template`). The validation script has no check for this.

**Analysis:** The script's 8 checks do not include verification of the metadata blockquote header, which is listed as a required structural element in the validation checklist. This is a completeness gap.

**Recommendation:** Add a 9th check function `check_metadata_blockquote()` that verifies the template contains a blockquote section with required metadata fields (Type, Status, Version, Date, Source).

---

### F-005: Missing Validation -- File Length Under 500 Lines Not Checked

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **File** | `scripts/validate_templates.py` (missing check) |

**Evidence:** The TEMPLATE-FORMAT.md Validation Checklist (line 309) states:

> "File length under 500 lines"

The TEMPLATE-FORMAT.md Overview (line 54) further elaborates:

> "Templates SHOULD target 200-400 lines. Templates exceeding 500 lines are acceptable when the excess is justified..."

The validation script has no file length check.

**Analysis:** While the 500-line limit uses SHOULD language (MEDIUM tier), the validation checklist explicitly lists it as a structural check item. Since TEMPLATE-FORMAT.md uses "SHOULD" and notes exceptions are acceptable, this is Minor severity -- but it represents a gap between the checklist specification and the script implementation.

**Recommendation:** Add an optional or warning-level check for file length exceeding 500 lines. Since TEMPLATE-FORMAT.md allows justified exceptions, this could emit a warning rather than a hard failure.

---

### F-006: Missing Validation -- Identity Field Values Not Validated Against SSOT

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **File** | `scripts/validate_templates.py` lines 221-253 |

**Evidence:** The TEMPLATE-FORMAT.md Validation Checklist Section 1 criteria states:

> "7 required fields; Criticality Tier table; **values match SSOT**"

The script's `check_identity_fields()` checks only that the 7 field names are present. It does not validate that values match the SSOT (e.g., that Strategy ID is a valid S-NNN from the catalog, that Composite Score matches ADR-EPIC002-001 values, that Family matches the strategy catalog).

**Analysis:** A template could pass validation with incorrect Identity field values (e.g., `Strategy ID: S-999`, `Composite Score: 9.99`, `Family: Nonexistent Family`). The E2E test file covers some of this (e.g., `test_template_identity_when_read_then_contains_7_required_fields` validates Strategy ID matches), but the validation script itself -- the one used in pre-commit and CI -- does not.

**Recommendation:** Extend `check_identity_fields()` to validate at minimum that Strategy ID matches a known catalog entry. Ideally, also validate Composite Score and Family against known values.

---

### F-007: Missing Validation -- Per-Section Content Checks from Checklist

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **File** | `scripts/validate_templates.py` (missing checks) |

**Evidence:** The TEMPLATE-FORMAT.md Validation Checklist Content per Section table lists numerous validation criteria per section:

| Section | Checklist Criteria | Script Coverage |
|---------|-------------------|-----------------|
| 2. Purpose | 3+ "When to Use"; 2+ "When NOT to Use"; measurable outcome; pairing recs | **None** |
| 3. Prerequisites | Input checklist; context reqs; ordering constraints (H-16) | **None** |
| 4. Execution Protocol | step format followed; decision points; finding prefix; severity defs | **Partial** (only step count) |
| 5. Output Format | 6 output sections; scoring impact table with correct weights; evidence reqs | **None** |
| 6. Scoring Rubric | strategy-specific 4-band rubric | **None** (only threshold bands and dimension weights checked) |
| 7. Examples | Before/After; findings with identifiers; severity applied | **Partial** (only char count) |
| 8. Integration | Pairings; H-16; criticality table matches SSOT; cross-references | **None** |

**Analysis:** Of the 8 content-level validation criteria groups, the script provides only shallow checks for 3 (sections 1, 4, 7) and skips 5 entirely (sections 2, 3, 5, 6 details, 8). The script docstring claims "8 validation checks" covering these areas, but several checks are presence-only (e.g., "Scoring Rubric has threshold bands table and dimension weights table") rather than content-validity checks.

**Recommendation:** Prioritize adding validation for the most impactful missing checks: (1) Purpose section "When to Use" / "When NOT to Use" count, (2) Integration section criticality table matching SSOT values, (3) Examples section Before/After content presence. These are the most automatable of the missing checks.

---

### F-008: CI Job Uses `uv sync` Without `--extra test` -- Correct for Script

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **File** | `.github/workflows/ci.yml` lines 159-160 |

**Evidence:**

```yaml
      - name: Install dependencies
        run: uv sync
```

**Analysis:** The `template-validation` CI job uses `uv sync` without `--extra dev` or `--extra test`. This is actually correct because the validation script (`scripts/validate_templates.py`) uses only stdlib modules (argparse, re, sys, pathlib, typing). No external dependencies are needed. However, there is a potential fragility issue: if the script is later modified to import a third-party library, the CI job would fail silently with an import error rather than providing a clear dependency message. This is Minor because the current state is correct.

**Recommendation:** Add a comment in the CI job explaining why `--extra dev` or `--extra test` is not needed (stdlib-only script), so future maintainers do not accidentally add external imports without updating the CI job.

---

### F-009: Criticality Tier Table Check Is Shallow String Search

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **File** | `scripts/validate_templates.py` lines 256-288 |

**Evidence:**

```python
has_criticality = (
    "Criticality Tier" in identity_content or "criticality tier" in identity_content
)
```

**Analysis:** The `check_criticality_tier_table()` function checks only for the string "Criticality Tier" anywhere in the Identity section. It does not verify that an actual table exists with C1-C4 rows and REQUIRED/OPTIONAL/NOT USED values. A template containing just the text "See Criticality Tier in SSOT" (a prose reference) would pass this check. The TEMPLATE-FORMAT.md specifies this as a "table" requirement, not just a mention.

**Recommendation:** Enhance the check to verify that a markdown table exists within the Criticality Tier subsection, containing at least rows for C1 through C4.

---

### F-010: E2E Test `test_validation_script_verbose_when_run_then_shows_details` Has Weak Assertion

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **File** | `tests/e2e/test_adversary_templates_e2e.py` lines 715-727 |

**Evidence:**

```python
def test_validation_script_verbose_when_run_then_shows_details(self):
    """Running with --verbose should produce detailed output."""
    ...
    assert result.returncode == 0
    # Verbose output should mention each template
    assert "s-001-red-team.md" in result.stdout or "S-001" in result.stdout
```

**Analysis:** The test asserts that verbose output mentions at least one template (S-001) but does not verify the distinguishing behavior of `--verbose` mode. In the script, non-verbose mode also prints template filenames (line 549: `print(f"[{status}] {template_path.name}")`). The test should verify that verbose mode produces check-level detail (e.g., the individual check results like "All 8 canonical sections") that would NOT appear in non-verbose mode for passing templates.

**Recommendation:** Assert that verbose output contains check-level detail strings like "All 8 canonical sections" or the check mark symbol, which only appear in verbose mode for passing templates.

---

### F-011: Pre-commit Hook Pattern Does Not Match TEMPLATE-FORMAT.md Itself

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **File** | `.pre-commit-config.yaml` line 138 |

**Evidence:**

```yaml
files: \.context/templates/adversarial/.*\.md$
```

**Analysis:** The pre-commit hook triggers on ALL `.md` files in the adversarial templates directory, including `TEMPLATE-FORMAT.md` itself. The validation script explicitly excludes `TEMPLATE-FORMAT.md` from validation (line 508: `if f.name != "TEMPLATE-FORMAT.md"`), so this is functionally harmless -- modifying TEMPLATE-FORMAT.md will trigger the hook, which will validate only the 10 strategy templates. However, this could be confusing: a developer editing only TEMPLATE-FORMAT.md would see the hook run but might wonder why their file is not being validated.

**Recommendation:** This is acceptable behavior (modifying the format document should trigger re-validation of strategy templates). Optionally, add a comment in the pre-commit config explaining this intentional behavior.

---

## Dimension Scores

| Dimension | Score | Weight | Weighted | Evidence |
|-----------|-------|--------|----------|----------|
| Completeness | 0.82 | 0.20 | 0.164 | Script implements 8 of 8 claimed checks, but only covers ~40% of the TEMPLATE-FORMAT.md validation checklist criteria (F-003, F-004, F-005, F-006, F-007). Pre-commit hook, CI job, and E2E tests are all present and structurally complete. |
| Internal Consistency | 0.90 | 0.20 | 0.180 | Script docstring claims 8 checks and delivers 8. Operator precedence bug (F-001) introduces a latent inconsistency in the scoring rubric check. Summary double-validation (F-002) is internally inconsistent with the loop that already tracks `all_passed`. |
| Methodological Rigor | 0.88 | 0.20 | 0.176 | BDD test naming convention followed. Script uses clean separation of concerns (data structures, helpers, checks, main). Validation checks use regex-based parsing that handles both heading formats. However, multiple checks are shallow string searches rather than structural validation (F-009). |
| Evidence Quality | 0.92 | 0.15 | 0.138 | Script produces clear PASS/FAIL output per template with check-level detail in verbose mode. E2E tests provide subprocess-based evidence that the script runs correctly. CI job produces visible output. |
| Actionability | 0.93 | 0.15 | 0.140 | The deliverables are immediately usable: pre-commit hook will trigger, CI job will run, script exits 0/1 correctly. Output messages are clear and include specific failure details with template names. All recommendations in findings are concrete and implementable. |
| Traceability | 0.90 | 0.10 | 0.090 | Script references EN-818 and TEMPLATE-FORMAT.md in its docstring. CI job has EN-818 comment. Pre-commit config has EN-818 comment. E2E test references EN-812 (not EN-818) in its module docstring but the TestTemplateValidationScript class is clearly attributable. |

**Weighted Composite: 0.888**

## Gate Decision

**REVISE** (0.888 < 0.920 threshold)

## Summary

The EN-818 deliverables provide a functional template validation pipeline with all four required components (script, pre-commit hook, CI job, E2E tests) present and operational. The script runs successfully against all 10 templates, the pre-commit hook triggers on the correct file pattern, the CI job is properly integrated into the `ci-success` dependency chain, and the E2E tests verify end-to-end behavior via subprocess execution.

However, the deliverables fall short of the C4 quality threshold due to two categories of issues. First, the validation script covers only a subset of the TEMPLATE-FORMAT.md validation checklist criteria (F-003 through F-007), with 5 of the 8 content-level section checks receiving no validation coverage, and structural checks for section ordering, metadata blockquote, and file length missing entirely. Second, there is a latent operator precedence bug in the scoring rubric check (F-001, Critical) and a performance issue from double-validating all templates in the summary computation (F-002, Major). The most impactful remediation actions are: (1) fix the operator precedence bug, (2) eliminate the double validation, (3) add section ordering verification, and (4) add at least 2-3 of the highest-value missing content checks (Purpose section criteria count, Integration criticality table SSOT match, Examples Before/After presence).
