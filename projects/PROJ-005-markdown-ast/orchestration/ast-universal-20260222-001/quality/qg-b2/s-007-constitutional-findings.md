# S-007 Constitutional AI Critique: QG-B2 Findings

<!-- AGENT: adv-executor | STRATEGY: S-007 | ENGAGEMENT: QG-B2 | DATE: 2026-02-23 -->
<!-- CRITICALITY: C4 | DELIVERABLES: eng-backend-001-implementation-report, red-vuln-001-vulnerability-assessment -->

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | Overall compliance verdict and score |
| [Compliance Matrix](#compliance-matrix) | Per-rule PASS/FAIL with evidence |
| [H-07: Architecture Layer Isolation](#h-07-architecture-layer-isolation) | Domain import boundary analysis |
| [H-10: One Class Per File](#h-10-one-class-per-file) | Multi-class file violations and ADR justification |
| [H-11: Type Hints and Docstrings](#h-11-type-hints-and-docstrings) | Public function signature compliance |
| [H-05: UV-Only Python](#h-05-uv-only-python) | Execution environment compliance |
| [H-20: BDD Test-First, 90% Coverage](#h-20-bdd-test-first-90-coverage) | Coverage enforcement finding |
| [H-33: AST-Based Parsing](#h-33-ast-based-parsing) | Worktracker operation compliance |
| [P-003, P-020, P-022: Constitutional Triplet](#p-003-p-020-p-022-constitutional-triplet) | Constitutional principle compliance |
| [Input Validation Guardrails](#input-validation-guardrails) | Parser input validation assessment |
| [Deliverable Quality Assessment](#deliverable-quality-assessment) | Implementation report and vulnerability assessment quality |
| [Remediation Recommendations](#remediation-recommendations) | Prioritized corrective actions |

---

## Executive Summary

**Overall Constitutional Compliance Verdict: CONDITIONAL PASS with mandatory remediation.**

Strategy S-007 (Constitutional AI Critique) was applied to the two Barrier 2 deliverables and their associated source code. The evaluation covered 7 HARD rules and the constitutional triplet (P-003, P-020, P-022).

**Summary verdict by rule:**

| Rule | Status | Severity |
|------|--------|----------|
| H-07 (Architecture layer isolation) | PASS | -- |
| H-10 (One class per file) | FAIL | High |
| H-11 (Type hints + docstrings) | PASS with minor gaps | Low |
| H-05 (UV-only Python) | PASS | -- |
| H-20 (BDD test-first, 90% coverage) | FAIL (CI enforcement gap) | High |
| H-33 (AST-based parsing) | PASS | -- |
| P-003 (No recursive subagents) | PASS | -- |
| P-020 (User authority) | PASS | -- |
| P-022 (No deception) | PASS | -- |
| Input validation guardrails | PASS with known gaps | Medium |

**Two HARD rule violations identified:**

1. **H-10 FAIL:** Five new source files each contain multiple public classes. The implementation report acknowledges this as an ADR-justified exception (ADR-PROJ005-003), but no such ADR decision explicitly documents the H-10 deviation for these specific files. The justification is present in docstrings but not in a formal waiver.

2. **H-20 FAIL (CI enforcement gap):** The CI pipeline enforces `--cov-fail-under=80`, not 90% as required by H-20/H-21. While actual domain module coverage is 98%, the enforcement gate does not protect against future regressions. The `reinject.py` file at 78% coverage is below the H-20 threshold and would not be caught by the CI gate.

**Quality threshold assessment:** The deliverables meet the >= 0.95 quality threshold specified for this engagement on all dimensions except the two identified HARD rule findings. Both findings are addressable without architectural rework.

---

## Compliance Matrix

| Rule ID | Rule | Status | Evidence Location |
|---------|------|--------|-------------------|
| H-07 | Architecture layer isolation: domain MUST NOT import application/infrastructure/interface | **PASS** | See [H-07 section](#h-07-architecture-layer-isolation) |
| H-10 | One class per file | **FAIL** | 5 files with multiple public classes; see [H-10 section](#h-10-one-class-per-file) |
| H-11 | Type hints + docstrings on all public functions | **PASS** (minor gaps noted) | See [H-11 section](#h-11-type-hints-and-docstrings) |
| H-05 | UV-only Python execution | **PASS** | `pyproject.toml`, `ci.yml`, implementation report line 219 |
| H-20 | BDD test-first, 90% line coverage | **FAIL** (CI enforcement gap) | `ci.yml:304` enforces 80%, not 90%; `reinject.py` at 78% |
| H-33 | AST-based parsing for worktracker entity operations | **PASS** | CLI commands use `JerryDocument`/`UniversalDocument`; no regex frontmatter extraction in worktracker path |
| P-003 | No recursive subagents | **PASS** | Deliverables are implementation artifacts, not agent definitions |
| P-020 | User authority -- never override | **PASS** | No user-authority override patterns found |
| P-022 | No deception about actions/capabilities | **PASS** | Both reports accurately disclose gaps and limitations |

---

## H-07: Architecture Layer Isolation

**Verdict: PASS**

**Methodology:** Searched all seven new domain files for imports from `src.application`, `src.infrastructure`, or `src.interface` namespaces.

**Evidence:**

All seven new source files in `src/domain/markdown_ast/` import exclusively from:
- Python stdlib (`re`, `json`, `os`, `fnmatch`, `enum`, `dataclasses`, `collections`, `types`, `bisect`, `typing`)
- Other domain modules (`src.domain.markdown_ast.*`)

```
src/domain/markdown_ast/yaml_frontmatter.py  -- imports: __future__, json, re, collections, dataclasses, yaml, src.domain.markdown_ast.input_bounds, src.domain.markdown_ast.jerry_document
src/domain/markdown_ast/xml_section.py       -- imports: __future__, re, dataclasses, src.domain.markdown_ast.input_bounds, src.domain.markdown_ast.jerry_document
src/domain/markdown_ast/html_comment.py      -- imports: __future__, re, dataclasses, src.domain.markdown_ast.input_bounds, src.domain.markdown_ast.jerry_document
src/domain/markdown_ast/document_type.py     -- imports: __future__, fnmatch, os, enum
src/domain/markdown_ast/schema_registry.py   -- imports: __future__, types, typing (TYPE_CHECKING only: src.domain.markdown_ast.schema)
src/domain/markdown_ast/universal_document.py -- imports: __future__, dataclasses, src.domain.markdown_ast.* (domain only)
src/domain/markdown_ast/__init__.py          -- imports: src.domain.markdown_ast.* (domain only)
```

**Special case -- `schema_registry.py` TYPE_CHECKING import:** Line 37 imports `EntitySchema` from `src.domain.markdown_ast.schema` inside a `TYPE_CHECKING` guard. This import is elided at runtime and does not violate H-07 (intra-domain import is permitted). Compliant per coding-standards.md SOFT guidance.

**Special case -- `bisect` inline import:** `xml_section.py:262`, `html_comment.py:266`, `frontmatter.py:489` import `bisect` inline inside the `_offset_to_line()` function body. This is stdlib and does not violate H-07. The inline placement is unusual but not a rule violation.

**Conclusion:** No H-07 violations detected in any of the seven new source files.

---

## H-10: One Class Per File

**Verdict: FAIL**

**Rule:** `H-10: Each Python file SHALL contain exactly ONE public class or protocol.`

**Violations found:**

| File | Public Classes | Count | Violation |
|------|---------------|-------|-----------|
| `src/domain/markdown_ast/yaml_frontmatter.py` | `YamlFrontmatterField`, `YamlFrontmatterResult`, `YamlFrontmatter` | 3 | YES |
| `src/domain/markdown_ast/xml_section.py` | `XmlSection`, `XmlSectionResult`, `XmlSectionParser` | 3 | YES |
| `src/domain/markdown_ast/html_comment.py` | `HtmlCommentField`, `HtmlCommentBlock`, `HtmlCommentResult`, `HtmlCommentMetadata` | 4 | YES |
| `src/domain/markdown_ast/document_type.py` | `DocumentType`, `DocumentTypeDetector` | 2 | YES |
| `src/domain/markdown_ast/universal_document.py` | `UniversalParseResult`, `UniversalDocument` | 2 | YES |
| `src/domain/markdown_ast/schema_registry.py` | `SchemaRegistry` | 1 | NO -- compliant |

**Compliant files:**
- `schema_registry.py`: 1 class -- PASS
- `universal_parse_result.py` (separate file): 1 class -- PASS (correctly extracted)

**Assessment of implementation report justification:**

The implementation report (line 221) claims:
> "Pre-existing multi-class files (yaml_frontmatter.py, html_comment.py) preserved as-is per H-10 hook enforcement."

This claim is **inaccurate** on two counts:

1. `yaml_frontmatter.py`, `xml_section.py`, `html_comment.py`, `document_type.py`, and `universal_document.py` are **new files** created by this implementation, not pre-existing files. The "grandfathered" exception applies only to files that existed before H-10 was enforced. New files must comply.

2. The docstrings in these files reference "ADR" as the justification:
   - `yaml_frontmatter.py:28`: "H-10: Supporting frozen dataclasses (YamlFrontmatterField, YamlFrontmatterResult) are co-located with primary class per ADR."
   - `xml_section.py:25`: "H-10: Supporting frozen dataclasses (XmlSection, XmlSectionResult) are co-located with primary class per ADR."
   - `html_comment.py:27`: "H-10: Supporting frozen dataclasses (HtmlCommentField, HtmlCommentBlock, HtmlCommentResult) are co-located with primary class per ADR."

   The referenced ADR (ADR-PROJ005-003) must explicitly waive H-10 for these classes. If it does not contain a documented H-10 exception, these files lack the required justification per the architecture-standards.md MEDIUM override requirement ("Override requires documented justification").

**Impact of the violation:**

- These files cannot be edited via Claude Code tooling without encountering the H-10 pre-tool-use hook, as acknowledged in the implementation report (Gap 1: `yaml.reader.ReaderError` not caught -- single-line fix blocked by H-10 enforcement).
- The technical debt created by this violation is already causing downstream gaps: the `yaml.reader.ReaderError` handler cannot be added without first resolving the H-10 conflict.

**Remediation path:** Either (a) refactor each file to one class per file -- creating `yaml_frontmatter_field.py`, `yaml_frontmatter_result.py`, `xml_section_data.py`, `xml_section_result.py`, etc. -- or (b) file a formal ADR exception per quality-enforcement.md MEDIUM override requirements, documented with justification for co-location (data locality, cohesion, API ergonomics).

---

## H-11: Type Hints and Docstrings

**Verdict: PASS (with minor observations)**

**Rule:** `H-11: All public functions and methods MUST have type annotations. H-12 (consolidated into H-11): All public functions, classes, and modules MUST have docstrings.`

**Assessment methodology:** Reviewed all public functions and methods across the seven new files.

**Type annotation coverage:**

All public `def` signatures in the new files include full type annotations:

| File | Public Method | Return Type | Params Typed |
|------|--------------|-------------|--------------|
| `yaml_frontmatter.py` | `YamlFrontmatter.extract()` | `YamlFrontmatterResult` | YES |
| `xml_section.py` | `XmlSectionParser.extract()` | `XmlSectionResult` | YES |
| `html_comment.py` | `HtmlCommentMetadata.extract()` | `HtmlCommentResult` | YES |
| `document_type.py` | `DocumentTypeDetector.detect()` | `tuple[DocumentType, str \| None]` | YES |
| `document_type.py` | `DocumentTypeDetector._detect_from_path()` | `DocumentType \| None` | YES |
| `document_type.py` | `DocumentTypeDetector._detect_from_structure()` | `DocumentType \| None` | YES |
| `universal_document.py` | `UniversalDocument.parse()` | `UniversalParseResult` | YES |
| `schema_registry.py` | All 6 public methods | Typed | YES |

**Docstring coverage:**

All public classes, methods, and modules have docstrings. Module-level docstrings are present in all seven files. Dataclass field docstrings are present in Attributes sections of class docstrings.

**Minor observation -- private helper functions:** Several private functions (`_normalize_value`, `_check_nesting_depth`, `_detect_duplicate_keys`, `_strip_control_chars`, `_compute_line_starts`, `_offset_to_line`, `_build_section_pattern`, `_normalize_path`, `_path_matches_glob`, `_match_recursive_glob`) have type annotations and docstrings, which exceeds the H-11 requirement (only public functions are required). This is positive evidence of quality discipline.

**Observation -- docstring duplication:** `_strip_control_chars()` and `_compute_line_starts()` and `_offset_to_line()` are duplicated verbatim across `xml_section.py`, `html_comment.py`, and `frontmatter.py`. This is a code quality concern (DRY principle) but not a HARD rule violation. Recommend extracting to a shared `_parsing_utils.py` module.

---

## H-05: UV-Only Python

**Verdict: PASS**

**Evidence:**

1. **Implementation report (line 219):** Explicitly asserts "All execution via `uv run`, all deps via `uv add`. No `python`/`pip` direct usage."
2. **pyproject.toml:** No `pip install` or direct `python` invocations found in the configuration.
3. **CI workflow:** Test execution uses `uv run pytest` throughout.
4. **New dependencies introduced:** Zero (per implementation report Executive Summary). No new packages required no `uv add` calls.
5. **PyYAML usage:** Already a declared dependency (`pyyaml>=6.0`). No new installation needed.

No H-05 violations detected.

---

## H-20: BDD Test-First, 90% Coverage

**Verdict: FAIL (CI enforcement gap)**

**Rule:** `H-20: (a) BDD Red phase -- NEVER write implementation before test fails; (b) 90% line coverage REQUIRED.`

**Findings:**

### Finding 1: CI threshold is 80%, not 90%

**Location:** `.github/workflows/ci.yml:304`
```yaml
--cov-fail-under=80 \
```

The CI gate enforces 80% minimum coverage. H-20(b) requires 90%. This means a commit that drops overall coverage from 98% to, for example, 83% would pass CI but violate H-20. The H-20 requirement is not enforced at the gate level.

**Severity:** High. This is a governance gap -- the rule exists but its enforcement is misconfigured. The gap will not prevent future regressions below the 90% threshold.

**Note:** The current actual coverage (98% for `src/domain/markdown_ast/`) satisfies H-20(b) at this point in time, but the enforcement mechanism is insufficient.

### Finding 2: reinject.py at 78% coverage is below H-20 threshold

**Location:** `src/domain/markdown_ast/reinject.py`

Per the implementation report Coverage Report table (line 141):
```
reinject.py | 51 | 11 | 78% | 164, 265-281
```

78% is below the 90% threshold required by H-20(b). The implementation report acknowledges this as "pre-existing technical debt" (Gap 2, lines 246-253), but the rule applies to the full module -- not only new code. The file is within `src/domain/markdown_ast/`, which is the scope of the 98% coverage claim. The 98% figure is for the aggregate; `reinject.py` individually violates H-20.

**Severity:** High. This specific file is below threshold. The pre-existing nature of the uncovered lines does not exempt it from H-20 compliance.

### Finding 3: BDD Red phase (H-20a) -- evidence is present but not verifiable post-hoc

The implementation report describes test files being created for each work item (WI-006, WI-008, WI-010, WI-012, WI-016, WI-014 via registry tests). The report structure implies test-first was followed, but H-20(a) (Red phase) cannot be verified from the implementation report alone because it requires inspection of commit history. This is noted as a limitation of the S-007 constitutional audit rather than a confirmed violation.

**Remediation:**

1. Correct `.github/workflows/ci.yml:304` to `--cov-fail-under=90`.
2. Add tests for `reinject.py` lines 164 and 265-281 to bring it above 90%. This should be captured in WI-022 (adversarial test suite, Phase 4).
3. Consider adding per-file coverage minimums in pytest configuration to prevent regression in individual files.

---

## H-33: AST-Based Parsing

**Verdict: PASS**

**Rule:** `H-33: AST-based parsing REQUIRED for worktracker entity operations. NEVER use regex for frontmatter extraction.`

**Assessment:**

H-33 applies to worktracker entity operations -- specifically `jerry ast frontmatter` and `jerry ast validate` CLI commands. The assessment evaluates whether these commands use AST-based parsing (via `JerryDocument`/`UniversalDocument`) rather than regex-based frontmatter extraction.

**Evidence:**

1. All CLI commands (`ast_commands.py`) invoke `JerryDocument.parse()` or `UniversalDocument.parse()` as the entry point (per implementation report WI-017, line 67).
2. The `UniversalDocument` facade delegates to `BlockquoteFrontmatter.extract()` for worktracker entities (per `_PARSER_MATRIX`, `universal_document.py:106`).
3. `BlockquoteFrontmatter.extract()` uses `markdown-it-py` token-based parsing (confirmed pre-existing architecture).
4. No regex-based frontmatter extraction is introduced in the new CLI commands per the implementation report.
5. The vulnerability assessment (RV-006) identifies that `reinject.py` uses pattern matching for L2-REINJECT directives, but this is the reinject parser -- not worktracker frontmatter operations. H-33 specifically targets frontmatter extraction.

**No H-33 violations detected.**

---

## P-003, P-020, P-022: Constitutional Triplet

**Verdict: PASS for both deliverables**

### P-003: No Recursive Subagents

**Assessment:** Both deliverables are implementation and assessment artifacts, not agent definitions. They do not create, invoke, or configure agents. No recursive subagent patterns are introduced by the new parser code.

The new CLI commands (`ast_detect`, `ast_sections`, `ast_metadata`) are synchronous functions that parse markdown -- they do not invoke agents.

**PASS.**

### P-020: User Authority -- Never Override

**Assessment:** The implementation does not introduce any mechanism to override user decisions. Parser result objects are immutable (`frozen=True` dataclasses with tuple containers). The CLI returns results to the user without making autonomous decisions on their behalf.

The vulnerability assessment correctly identifies several security risks (RV-006 governance directive injection, RV-007 TOCTOU) but does not itself override user authority -- it discloses risks for user decision.

**PASS.**

### P-022: No Deception About Actions, Capabilities, or Confidence

**Assessment of the implementation report:**

The implementation report accurately discloses:
- Known Gap 1: `yaml.reader.ReaderError` not caught (lines 231-243)
- Known Gap 2: `reinject.py` coverage at 78% (lines 246-253)
- Known Gap 3: Phase 4 work items deferred (lines 255-259)
- H-10 technical debt (lines 277-279)

The report's H-10 compliance claim (line 221) is **inaccurate** (claims pre-existing grandfathering for new files), which could be considered a P-022 concern. However, the inaccuracy appears to be an error in classification rather than intentional deception -- the files are acknowledged as technically debt-laden in the Strategic Implications section (line 277). This is assessed as an **error requiring correction**, not a constitutional deception violation.

**Assessment of the vulnerability assessment:**

The red-vuln-001 report explicitly states confidence levels (overall 0.88, with breakdown by analysis type). It clearly distinguishes confirmed findings from planned-code findings. It documents 6 DREAD score disagreements with eng-architect-001 and provides reasoning. Limitations are disclosed.

**PASS for both deliverables.** The implementation report inaccuracy on H-10 classification must be corrected.

---

## Input Validation Guardrails

**Verdict: PASS with known gaps (pre-existing and documented)**

**Assessment per agent-development-standards.md guardrails template:**

The new parsers implement comprehensive input validation consistent with the guardrail requirements:

| Guardrail | Implementation | Status |
|-----------|---------------|--------|
| File size limit | `InputBounds.max_file_bytes` enforced at CLI layer (M-05) | PASS |
| YAML block size | `InputBounds.max_yaml_block_bytes` pre-parse (M-07) | PASS |
| Alias/anchor count | `InputBounds.max_alias_count` pre-parse (M-20) | PASS |
| Key count | `InputBounds.max_frontmatter_keys` post-parse (M-16) | PASS |
| Nesting depth | `_check_nesting_depth()` post-parse (M-06) | PASS |
| Value length | `InputBounds.max_value_length` per-field (M-17) | PASS |
| Control char stripping | `_strip_control_chars()` in all parsers (M-18) | PASS |
| Section count | `InputBounds.max_section_count` in XmlSectionParser (M-16) | PASS |
| Comment count | `InputBounds.max_comment_count` in HtmlCommentMetadata (M-16) | PASS |
| Safe YAML loading | `yaml.safe_load()` exclusively (M-01) | PASS |
| Banned API CI check | `ci.yml` security job (M-04b, WI-021) | PASS |
| Tag name allowlist | `XmlSectionParser.ALLOWED_TAGS` frozenset | PASS |
| L2-REINJECT exclusion | Case-insensitive `_REINJECT_PREFIX_RE` in HtmlCommentMetadata | PASS |
| Atomic write | `_atomic_write()` via tempfile + os.replace() (M-21) | PASS |
| Path containment | `_resolve_and_check_path()` in CLI (M-08, M-10) | PASS |

**Known gaps (documented, pre-existing or deferred):**

1. **`yaml.reader.ReaderError` not caught** (`yaml_frontmatter.py`): Documented as Gap 1 in implementation report. Low impact given M-18 pre-sanitization. Blocked by H-10 enforcement on multi-class file. Remediation path is clear (refactor or H-10 exception ADR).

2. **regex timeout for ReDoS** (red-vuln-001 RV-004, RV-020): Python's `re` module does not natively support timeouts. The vulnerability assessment correctly identifies M-05 as "INSUFFICIENT" because no implementation mechanism is specified. This is a **deferred gap** requiring Phase 4 resolution (WI-023 ReDoS test suite). No mitigation is in place for complex regex patterns in `schema.py:279` (`re.fullmatch(rule.value_pattern, value)`).

3. **reinject.py origin checking** (red-vuln-001 RV-006): M-12 (file-origin trust) is assessed as deferred -- the reinject parser does not restrict file origins. This is documented in the vulnerability assessment but no Phase 3 mitigation addresses it.

**Assessment:** The input validation guardrails are substantially complete for the new parsers. The three documented gaps are correctly disclosed and have defined remediation paths. None of the gaps introduces an immediate critical risk in the primary use case (processing trusted Jerry framework files).

---

## Deliverable Quality Assessment

### Implementation Report (eng-backend-001)

**Strengths:**
- Complete work item traceability (21/21 WI status with specific evidence references)
- Accurate coverage reporting including per-file miss analysis
- Transparent disclosure of three known gaps with root cause analysis
- Security mitigation matrix maps M-01 through M-24 to work items
- Design decision compliance table is specific and verifiable

**Weaknesses identified by S-007:**
- H-10 compliance claim is inaccurate (lines 220-221): claims pre-existing grandfathering for new files
- Does not disclose the CI coverage threshold gap (--cov-fail-under=80 vs H-20's 90%)
- `reinject.py` 78% coverage is listed in the coverage table but not flagged as an H-20 violation

**Verdict:** High-quality document with two disclosure gaps that require correction.

### Vulnerability Assessment (red-vuln-001)

**Strengths:**
- 27 findings with complete DREAD scoring and CWE mapping
- 6 DREAD challenge disagreements are documented with independent reasoning (Appendix A)
- Mitigation sufficiency assessments are differentiated (SUFFICIENT vs INSUFFICIENT)
- Three mitigations correctly flagged as insufficient (M-03, M-05, M-12)
- Attack catalog provides concrete, executable attack vectors
- Confidence levels are calibrated and disclosed per handoff protocol (0.88 overall)

**Weaknesses identified by S-007:**
- Does not assess the CI coverage threshold gap (out of scope for red team, but relevant to constitutional analysis)
- RV-018 (`reinject.py` tokens= field) identifies a governance coverage gap but does not note the H-20 coverage violation for that file

**Verdict:** High-quality security assessment. The assessment scope (security) does not require coverage or architectural compliance findings -- these are correctly left to S-007.

---

## Remediation Recommendations

Prioritized by severity and blocking impact:

### Priority 1: Mandatory (HARD rule violations)

**REM-001: Resolve H-10 violations in five new source files**

- **Files:** `yaml_frontmatter.py`, `xml_section.py`, `html_comment.py`, `document_type.py`, `universal_document.py`
- **Action (preferred):** File a formal MEDIUM-override justification ADR for co-locating data classes with their primary parser class. The justification exists informally in docstrings but is not codified as a governance decision. The ADR should document the trade-off: cohesion and API ergonomics (co-location) vs. H-10 one-class-per-file constraint.
- **Action (alternative):** Refactor each file to one class per file. This enables future edits (including the `yaml.reader.ReaderError` fix) without hook interference.
- **Criticality:** Auto-C3 (touching architecture) per AE-003.

**REM-002: Fix CI coverage threshold to enforce H-20**

- **File:** `.github/workflows/ci.yml:304`
- **Change:** `--cov-fail-under=80` -> `--cov-fail-under=90`
- **Additionally:** Add tests for `reinject.py:164,265-281` (currently 78% coverage) as part of WI-022 (Phase 4 adversarial testing).
- **Criticality:** C2 (affects CI configuration, reversible in one day).

### Priority 2: Recommended (documentation corrections)

**REM-003: Correct H-10 compliance claim in implementation report**

- **File:** `eng-backend-001-implementation-report.md:221`
- **Current text:** "Pre-existing multi-class files (yaml_frontmatter.py, html_comment.py) preserved as-is per H-10 hook enforcement."
- **Issue:** These are new files, not pre-existing. The text mischaracterizes the violation.
- **Correction:** Rewrite to accurately state that new files contain multiple classes per ADR-PROJ005-003 design decision (cohesion trade-off), and document as a pending MEDIUM override justification.

**REM-004: Address `yaml.reader.ReaderError` gap**

- **File:** `src/domain/markdown_ast/yaml_frontmatter.py:270-300`
- **Action:** After resolving REM-001 (H-10), add `yaml.reader.ReaderError` to the exception handler chain. Single-line addition.
- **Criticality:** Low (M-18 provides pre-parse control char sanitization that mitigates most paths to this error).

### Priority 3: Deferred (Phase 4 scope)

**REM-005: Implement regex timeout for ReDoS mitigation**

- **Components:** `schema.py:279`, future XmlSectionParser patterns
- **Action:** Evaluate `regex` library or `re2` wrapper. If Python `re` is retained, add pre-compile pattern complexity validation (reject nested quantifiers) at schema registration time.
- **Criticality:** Captured in WI-023 (ReDoS test suite).

**REM-006: Implement reinject file-origin trust (M-12)**

- **Component:** `src/domain/markdown_ast/reinject.py`
- **Action:** Define allowed directory list (`.context/rules/`, `.claude/rules/`). Add origin check in `extract_reinject_directives()` or at CLI layer before invoking the reinject parser.
- **Criticality:** High security impact (RV-006 DREAD 33) but architectural change; assign to Phase 4.

---

<!-- AGENT: adv-executor | STRATEGY: S-007 Constitutional AI Critique | DATE: 2026-02-23 -->
<!-- VERDICT: CONDITIONAL PASS | HARD RULE VIOLATIONS: 2 (H-10, H-20) | MANDATORY REMEDIATION REQUIRED -->
*S-007 Constitutional Findings v1.0.0*
*Deliverables evaluated: eng-backend-001-implementation-report.md, red-vuln-001-vulnerability-assessment.md*
*Source files evaluated: yaml_frontmatter.py, xml_section.py, html_comment.py, document_type.py, universal_document.py, schema_registry.py, __init__.py*
*Quality threshold: >= 0.95 | Achieved: 0.94 (below threshold due to 2 HARD rule violations requiring mandatory remediation)*
