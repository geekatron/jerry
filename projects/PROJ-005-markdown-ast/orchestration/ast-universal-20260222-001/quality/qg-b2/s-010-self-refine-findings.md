# S-010 Self-Refine Findings: Barrier 2 Quality Gate

<!-- STRATEGY: S-010 (Self-Refine) | QG: QG-B2 | AGENT: adv-executor | CRITICALITY: C4 -->
<!-- DATE: 2026-02-23 | ENGAGEMENT: AST-UNIVERSAL-20260222-001 -->

## Document Sections

| Section | Purpose |
|---------|---------|
| [Strategy Application](#strategy-application) | How S-010 was applied to Barrier 2 deliverables |
| [Deliverable A: Implementation Report Findings](#deliverable-a-implementation-report-findings) | Self-refine analysis of eng-backend-001 report |
| [Deliverable B: Vulnerability Assessment Findings](#deliverable-b-vulnerability-assessment-findings) | Self-refine analysis of red-vuln-001 report |
| [Source Code Cross-Verification Findings](#source-code-cross-verification-findings) | Discrepancies found between reports and actual code |
| [Per-Dimension Preliminary Scores](#per-dimension-preliminary-scores) | 0.0-1.0 scores per scoring dimension per deliverable |
| [Composite Preliminary Score](#composite-preliminary-score) | Weighted composite and threshold comparison |
| [Improvement Recommendations](#improvement-recommendations) | Specific actionable revisions required |

---

## Strategy Application

**S-010 Self-Refine** asks: *"If I were the creator reviewing my own work, what would I fix?"* For each deliverable, this strategy examines:

1. Incomplete sections or missing evidence
2. Claims without supporting test evidence
3. Inconsistencies between the report and actual code
4. Areas where the work could be stronger with minor revision

**Artifacts reviewed:**

| Artifact | Path |
|----------|------|
| Implementation Report | `projects/PROJ-005-markdown-ast/orchestration/ast-universal-20260222-001/eng/phase-3-implementation/eng-backend-001/eng-backend-001-implementation-report.md` |
| Vulnerability Assessment | `projects/PROJ-005-markdown-ast/orchestration/ast-universal-20260222-001/red/phase-2-vulnerability/red-vuln-001/red-vuln-001-vulnerability-assessment.md` |
| Source: yaml_frontmatter.py | `src/domain/markdown_ast/yaml_frontmatter.py` |
| Source: xml_section.py | `src/domain/markdown_ast/xml_section.py` |
| Source: html_comment.py | `src/domain/markdown_ast/html_comment.py` |
| Source: document_type.py | `src/domain/markdown_ast/document_type.py` |
| Source: universal_document.py | `src/domain/markdown_ast/universal_document.py` |
| Source: schema_registry.py | `src/domain/markdown_ast/schema_registry.py` |
| Source: ast_commands.py | `src/interface/cli/ast_commands.py` |

---

## Deliverable A: Implementation Report Findings

### Finding IR-001: Function Name Inaccuracy in WI-020 Evidence (CRITICAL)

| Field | Detail |
|-------|--------|
| **Severity** | Critical -- factual error in evidence claim |
| **Location** | Implementation Report, Work Item Completion Matrix, WI-020 row (line 70) |
| **Section** | Also repeated in Security Mitigations Implemented, M-21 row (line 193) |

**What the report claims:**
```
WI-020 | 3 | Write-back TOCTOU mitigation (M-21) | DONE |
`ast_commands.py` `_atomic_write()` uses `tempfile.NamedTemporaryFile` + `os.replace()` for atomic writes.
```

**What the code actually contains:**

The function `_atomic_write()` does not exist in `src/interface/cli/ast_commands.py`. The TOCTOU mitigation is implemented inline within `ast_modify()` (lines 510-535 of the actual file). The implementation uses `tempfile.mkstemp()` (not `NamedTemporaryFile`) and `os.rename()` (not `os.replace()`).

The distinction between `os.replace()` and `os.rename()` is security-relevant: `os.replace()` is guaranteed atomic on POSIX systems and also works across filesystems on some systems, whereas `os.rename()` is platform-dependent in behavior for cross-filesystem renames, though both are atomic within the same filesystem.

**Self-refine question:** If I were the creator, would I have caught that I described a helper function `_atomic_write()` that does not actually exist, and named the wrong stdlib function (`NamedTemporaryFile` vs `mkstemp`, `os.replace` vs `os.rename`)?

**Impact:** Downstream reviewers and quality gate assessors who search for `_atomic_write` will not find it, calling evidence validity into question.

---

### Finding IR-002: WI-018 Function Name Inaccuracy

| Field | Detail |
|-------|--------|
| **Severity** | Moderate -- factual error in evidence |
| **Location** | Implementation Report, Work Item Completion Matrix, WI-018 row (line 68) |

**What the report claims:**
```
`ast_commands.py` `_resolve_and_check_path()` validates all file paths against repo root.
```

**What the code actually contains:**

The function `_resolve_and_check_path()` does not exist in `src/interface/cli/ast_commands.py`. The actual function is `_check_path_containment()` (line 178 of the actual file), which returns a `(Path | None, str | None)` tuple.

**Self-refine question:** If I were the creator, would I have caught that I referenced a function by the wrong name in the evidence?

**Impact:** Evidentiary integrity is weakened. Any reader trying to verify the claim will not find the named function.

---

### Finding IR-003: M-12 Mitigation Number Collision

| Field | Detail |
|-------|--------|
| **Severity** | Moderate -- terminology inconsistency across deliverables |
| **Location** | Implementation Report, Security Mitigations Implemented table (line 184) |
| **Cross-reference** | Vulnerability Assessment uses M-12 for a different mitigation |

**What the implementation report claims:**
```
| M-12 | Schema value_pattern validation | WI-014/015 | Schema definitions use pre-tested patterns |
```

**What the vulnerability assessment uses M-12 for:**
```
M-12 file-origin trust (CRITICAL): MUST restrict reinject parsing to files in `.context/rules/`
and `.claude/rules/` directories only.
```

The two deliverables assign conflicting semantics to the M-12 mitigation identifier. The implementation report uses M-12 for "Schema value_pattern validation." The vulnerability assessment uses M-12 for "file-origin trust for reinject parsing" (referenced at lines 233, 629, 953, 984, 995, 1052, 1053, 1086 of the VA). This creates a traceability break: downstream consumers of either document cannot cross-reference mitigations without confusion.

**Root cause:** The implementation report's mitigation table likely reflects an earlier version of the threat model mitigation numbering that diverged from the vulnerability assessment's numbering. Neither document cites a single authoritative mitigation register.

---

### Finding IR-004: DD-4 and DD-5 Absent from Design Decision Compliance Table

| Field | Detail |
|-------|--------|
| **Severity** | Minor -- completeness gap |
| **Location** | Implementation Report, Design Decision Compliance table (lines 200-212) |

The Design Decision Compliance table covers DD-1, DD-2, DD-3, DD-6, DD-7, DD-8, DD-9, DD-10. DD-4 and DD-5 are not present. The implementation report does not explain why DD-4 and DD-5 are skipped.

If DD-4 and DD-5 do not apply to Phase 3 implementation, the table should include a row noting "N/A -- not in Phase 3 scope." Without this, a reader cannot determine whether DD-4 and DD-5 are intentionally excluded or accidentally omitted.

**Self-refine question:** If I were the creator, would I have noticed the non-sequential numbering DD-1, 2, 3, 6, 7, 8, 9, 10 and added a note explaining the gap?

---

### Finding IR-005: Test Count Approximations Undermine Traceability

| Field | Detail |
|-------|--------|
| **Severity** | Minor -- evidence quality |
| **Location** | Implementation Report, Test File Inventory table (lines 109-117) |

The test count column for four of six new test files uses approximation notation (`~35`, `~15`, `~25`, `~22`). Only `test_schema_registry.py` (42 tests) and `test_universal_document.py` (23 tests) have exact counts. The executive summary states "446 passed" (exact), which means exact counts are available from test runner output -- the approximations represent a documentation choice to not run the count per-file.

**Self-refine question:** If I were the creator and I had the full test suite output with 446 passing tests in the markdown_ast module, would I have used `pytest --collect-only` to obtain exact per-file counts? Approximations weaken the evidentiary quality of the test inventory.

---

### Finding IR-006: reinject.py Coverage Explanation is Sparse

| Field | Detail |
|-------|--------|
| **Severity** | Minor -- completeness |
| **Location** | Implementation Report, Coverage Report (lines 153-154) and Known Gaps Gap 2 (lines 245-253) |

The coverage report notes `reinject.py` at 78% with missing lines 164, 265-281 and attributes this to "pre-existing code paths not in scope." The Known Gaps section repeats this characterization. However, no specific explanation is given for *why* lines 265-281 are uncovered -- what code paths do they represent?

A self-reviewing creator would strengthen the rationale: lines 265-281 in reinject.py could be edge-case branches in the `modify_reinject_directive()` function (RV-015 in the vulnerability assessment identifies this function as having a collision risk bug). If these uncovered lines include the collision-risk code path, the gap becomes more significant than "pre-existing technical debt."

---

### Finding IR-007: H-10 Compliance Note Contains an Inaccuracy

| Field | Detail |
|-------|--------|
| **Severity** | Minor -- accuracy |
| **Location** | Implementation Report, HARD Rule Compliance, H-10 row (line 221) |

The report states:
```
Pre-existing multi-class files (yaml_frontmatter.py, html_comment.py) preserved as-is
per H-10 hook enforcement.
```

The parenthetical identifies two files as pre-existing multi-class: `yaml_frontmatter.py` and `html_comment.py`. However, the Strategic Implications section (line 277) lists three files: `yaml_frontmatter.py`, `html_comment.py`, AND `document_type.py`. The HARD Rule Compliance entry omits `document_type.py` from the list, creating an internal inconsistency.

Both `document_type.py` (which contains `DocumentType` enum + `DocumentTypeDetector` class) and the other two are new files introduced by this implementation, not truly "pre-existing." The framing as "pre-existing multi-class" is misleading for new files.

---

## Deliverable B: Vulnerability Assessment Findings

### Finding VA-001: RV-003 Status Stale -- Vulnerability is Now Remediated

| Field | Detail |
|-------|--------|
| **Severity** | Critical -- stale status claim |
| **Location** | Vulnerability Assessment, RV-003 finding (line 83) |

**What the VA states:**
```
| **Status** | CONFIRMED -- no mitigation exists in current code |
```

**What the implementation shows:**

WI-018 (Phase 3) implemented path containment via `_check_path_containment()` in `ast_commands.py`. The `_read_file()` function (lines 228-261) now calls `_check_path_containment()` when `_ENFORCE_PATH_CONTAINMENT` is `True`. M-08 and M-10 are listed as DONE in the implementation report.

The vulnerability assessment's RV-003 was written during Phase 2 (before Phase 3 implementation). The status "CONFIRMED -- no mitigation exists" is now stale given Phase 3 completion. A self-reviewing vulnerability assessor would have either: (a) reviewed the Phase 3 implementation code before finalizing the report, or (b) explicitly scoped the assessment as "pre-Phase 3 implementation" to justify the stale status.

**Self-refine question:** If I were the red-vuln-001 creator and I knew Phase 3 implementation was concurrent or just completed, would I have reviewed the actual implementation code to update the RV-003 status from "no mitigation" to "MITIGATED (WI-018)"?

---

### Finding VA-002: RV-005 Status Also Stale -- SchemaRegistry Freeze Implemented

| Field | Detail |
|-------|--------|
| **Severity** | Critical -- stale status claim |
| **Location** | Vulnerability Assessment, RV-005 finding (line 162) |

**What the VA states:**
```
| **Status** | CONFIRMED -- no freeze mechanism in current code |
```

**What the implementation shows:**

WI-003 (Phase 0) implemented `SchemaRegistry` with `freeze()` method in `src/domain/markdown_ast/schema_registry.py`. The registry is confirmed frozen at module load time. The implementation report lists this as DONE with test coverage in `test_schema_registry.py` (42 tests).

The vulnerability assessment's source code reviewed section (lines 1148-1158) lists `src/domain/markdown_ast/schema.py` but not `src/domain/markdown_ast/schema_registry.py`, confirming the VA reviewed the pre-implementation codebase and did not incorporate the Phase 0-2 implementation.

This is the same root cause as VA-001: the VA's scope description says it reviewed "planned code" (L1-B section), but RV-005 is categorized under L1-A (existing code findings) with a "current code" status -- which is now outdated.

---

### Finding VA-003: RV-007 Status Stale -- TOCTOU Mitigation Implemented

| Field | Detail |
|-------|--------|
| **Severity** | High -- stale status claim |
| **Location** | Vulnerability Assessment, RV-007 finding (line 246) |

**What the VA states:**
```
| **Status** | CONFIRMED -- no atomic write or re-verification in current code |
```

**What the implementation shows:**

WI-020 (Phase 3) implemented the atomic write pattern in `ast_modify()` using `tempfile.mkstemp()` and `os.rename()`. Path re-verification occurs at lines 511-518 before the write. This is consistent with M-21 being marked DONE in the implementation report.

The recommended mitigations section of RV-007 (line 271) references "M-21 atomic write (planned in WI-019)" -- but the implementation report cross-references M-21 to WI-020, not WI-019. This WI number discrepancy compounds the stale status problem.

---

### Finding VA-004: M-12 Mitigation is Described as Planned but Partially Implemented

| Field | Detail |
|-------|--------|
| **Severity** | High -- accuracy |
| **Location** | Vulnerability Assessment, Appendix B, M-12 row (line 1052) |

The VA assesses M-12 as "Planned (WI-020)" for "file-origin trust for reinject." However, per the implementation report, WI-020 covers "Write-back TOCTOU mitigation (M-21)" -- not M-12. The VA's assignment of WI-020 to M-12 is internally inconsistent with both the VA's own M-12 description and the implementation report's WI-020 description.

More importantly: the actual `html_comment.py` code contains a case-insensitive `_REINJECT_PREFIX_RE` check that excludes L2-REINJECT comments from HTML comment processing (lines 68 and 175 of html_comment.py). This is a partial implementation of content-level exclusion, not full file-origin trust. The VA's M-12 status of "Planned" is therefore partially incorrect -- the content exclusion is done, but the file-origin directory restriction is not.

---

### Finding VA-005: L2-B Section Claims the Assessment Covers Planned Code, but Statuses for Existing Vulnerabilities Are Not Updated Post-Implementation

| Field | Detail |
|-------|--------|
| **Severity** | High -- methodological consistency |
| **Location** | Vulnerability Assessment, L0 Risk Posture Assessment (lines 51-55) and References (lines 1148-1158) |

The VA's references section (Source Code Reviewed) lists only pre-Phase-3 files:
- `jerry_document.py`, `frontmatter.py`, `schema.py`, `nav_table.py`, `reinject.py`, `ast_commands.py`, `parser.py`

None of the new Phase 1-3 source files are listed as reviewed:
- `yaml_frontmatter.py`, `xml_section.py`, `html_comment.py`, `document_type.py`, `schema_registry.py`, `schema_definitions.py`, `universal_document.py`, `universal_parse_result.py`, `input_bounds.py`

The L1-B section correctly labels findings as "Planned Code Findings" for these new components. However, the L1-A section's existing code findings (RV-003, RV-005, RV-007, RV-008 through RV-018) were assessed against the pre-implementation codebase. Given that Phase 3 implementation was described as complete in the concurrent eng-backend-001 report, the VA should have either:

1. Reviewed the new implementation files and updated statuses
2. Explicitly bounded its scope as "pre-Phase-3" in the title and risk posture section

The current state -- presenting "CONFIRMED -- no mitigation exists" for vulnerabilities that have been remediated -- overstates residual risk and may misdirect Phase 4 remediation efforts.

---

### Finding VA-006: Confidence Score Not Calibrated Against Stale Status

| Field | Detail |
|-------|--------|
| **Severity** | Moderate -- confidence calibration |
| **Location** | Vulnerability Assessment, L0 Confidence section (lines 58-64) |

The VA reports:
```
Existing code analysis: 0.92 (direct code review, all source files inspected)
```

However, as documented in VA-005, the "existing code analysis" only covered 8 pre-Phase-3 source files. The 9 new domain source files were not reviewed (they are listed in L1-B as "planned code"). Given that at least 3 existing-code findings (RV-003, RV-005, RV-007) have stale statuses due to Phase 3 implementation, the confidence of 0.92 for existing code analysis is overclaimed.

A self-reviewing creator would ask: "Did I actually review *all* existing source files, including those just implemented?" The confidence score should reflect that the scope of "existing code" was bounded to the pre-implementation codebase.

---

### Finding VA-007: Appendix B Mitigation Table Has Conflicting Column Semantics

| Field | Detail |
|-------|--------|
| **Severity** | Moderate -- clarity |
| **Location** | Vulnerability Assessment, Appendix B, two separate tables (lines 1027-1064) |

Appendix B contains two tables: "Barrier 1 Priority Mitigations" and "Full Mitigation Status." The second table assigns "Planned (WI-XXX)" or "NOT IMPLEMENTED" to all 24 mitigations. However, several of these are now implemented per the implementation report (M-01, M-04, M-05, M-06, M-07, M-08, etc.).

A self-reviewing creator would have either:
1. Used the present tense conditional ("will be implemented") if writing before Phase 3 completion
2. Updated the table with actual implementation status after reviewing Phase 3 output
3. Added a header note: "Status reflects pre-Phase-3 assessment; update required after WI-001 through WI-021 completion"

---

### Finding VA-008: WI Number Discrepancy Between VA and Implementation Report (RV-007)

| Field | Detail |
|-------|--------|
| **Severity** | Moderate -- traceability |
| **Location** | Vulnerability Assessment, RV-007, Recommended Mitigations (line 271) |

The VA states: `M-21 atomic write (planned in WI-019)`. The implementation report assigns M-21 to WI-020, not WI-019. This one-off error in WI numbering between the two documents breaks cross-document traceability. The VA's reference "WI-019" for atomic write is incorrect; WI-019 covers L2-REINJECT trusted path whitelist.

---

### Finding VA-009: Three Mitigations Assessed as Insufficient Lack Implementation Guidance Detail

| Field | Detail |
|-------|--------|
| **Severity** | Moderate -- actionability |
| **Location** | Vulnerability Assessment, L2 Strategic Analysis (lines 950-953) |

The VA identifies three mitigations as insufficient:
- M-03 (YAML anchor depth limit): "Implementation guidance is missing"
- M-05 (regex timeout): "No specific mechanism identified. Python's `re` module does not support timeouts. Requires `regex` library or `re2`."
- M-12 (file-origin trust): "No allowed-directory list is defined"

While these are valid findings, the VA stops at identifying the gap. A stronger self-refining pass would add specific remediation recommendations for each:

For M-03: "Recommend implementing a pre-parse anchor count scanner: `raw_yaml.count('&') <= bounds.max_alias_count` before `yaml.safe_load()` invocation." (Note: the implementation at `yaml_frontmatter.py` lines 250-262 already does alias *reference* counting via `_ALIAS_RE`, but not anchor definition counting.)

For M-05: Recommend a specific library choice (`regex` with timeout, or signal-based timeout) rather than leaving it open.

For M-12: Provide the specific directory allowlist: `.context/rules/`, `.claude/rules/`.

---

## Source Code Cross-Verification Findings

These findings arise from comparing the reports' claims against the actual source code.

### Finding SV-001: html_comment.py Negative Lookahead is Case-Sensitive Despite Claim of Case-Insensitivity

| Field | Detail |
|-------|--------|
| **Severity** | High -- security accuracy |
| **Location** | `src/domain/markdown_ast/html_comment.py`, line 53 |
| **Report Claim** | Implementation Report WI-009 claims "Case-insensitive L2-REINJECT exclusion" |

The implementation at `html_comment.py` lines 51-57:
```python
_METADATA_COMMENT_PATTERN = re.compile(
    r"<!--\s*"
    r"(?!L2-REINJECT:)"  # <-- This lookahead is case-SENSITIVE
    r"(?P<body>.*?)"
    r"\s*-->",
    re.DOTALL,
)
```

The comment in the source code states `# Negative lookahead (case-insensitive via _is_reinject)` but no `_is_reinject` function exists. The lookahead `(?!L2-REINJECT:)` is case-sensitive. The downstream `_REINJECT_PREFIX_RE` at line 68 is case-insensitive (`re.IGNORECASE`), and is applied at line 175 via `_REINJECT_PREFIX_RE.match(body)`.

The actual exclusion works as follows:
1. The regex negative lookahead catches exact-case `L2-REINJECT:` (case-sensitive)
2. The `_REINJECT_PREFIX_RE.match(body)` catches all other case variants (case-insensitive)

This means the regex lookahead is redundant for the case-insensitive protection (since `_REINJECT_PREFIX_RE` handles all cases), and the comment in the source code references a non-existent function (`_is_reinject`). The vulnerability assessment (RV-014) correctly identifies the case-sensitivity gap in `reinject.py`'s pattern, but does not note the misleading comment in `html_comment.py`.

Both the implementation report and the source code comment contain accuracy gaps about the mechanism.

---

### Finding SV-002: `_normalize_value()` Does Not Preserve Original YAML Value for Non-String Types in `YamlFrontmatterField.value`

| Field | Detail |
|-------|--------|
| **Severity** | Moderate -- design accuracy |
| **Location** | `src/domain/markdown_ast/yaml_frontmatter.py`, lines 358-382 |

The `YamlFrontmatterField` dataclass is documented as:
```
value: The original typed value from ``yaml.safe_load()``.
```

However, the implementation at lines 358-382 stores the `value` field as the *original* unmodified Python object (bool, int, float, list, dict, None) -- NOT the normalized string. The `_normalize_value()` function produces `(normalized_str, value_type)` but only the `value_type` string is stored from the normalization; `normalized` is only used for length checking (line 365) and is then discarded. The actual stored value is the raw YAML-parsed `value` object.

This means:
- `YamlFrontmatterField.value` contains `True` (bool), not `"true"` (str) for boolean YAML values
- The docstring for `value` says "original typed value" -- this is accurate
- But the module-level docstring (line 18) says "DD-10 type normalization" -- which is only partially true; normalization is used for bounds checking but not for value storage

The implementation report's WI-005 description states "DD-10 type normalization" without noting that the normalization is applied to the display/storage of `value_type` rather than `value` itself. Whether this is the intended design is unclear, but the documentation is ambiguous.

---

### Finding SV-003: `_detect_from_structure()` Uses Substring Match for `---` -- Will False-Positive on Any File Containing Three Dashes

| Field | Detail |
|-------|--------|
| **Severity** | Moderate -- correctness |
| **Location** | `src/domain/markdown_ast/document_type.py`, lines 90-96 |

The `STRUCTURAL_CUE_PRIORITY` list at lines 90-96:
```python
("---", DocumentType.AGENT_DEFINITION),
```

This performs a simple `"---" in content` check. Any markdown file containing a horizontal rule (`---`) or any triple-dash sequence (common in markdown documents, table separators, etc.) will match this cue and be classified as `AGENT_DEFINITION` during structure-only detection.

The implementation report (WI-011 description) does not note this limitation. The vulnerability assessment discusses type detection evasion (RV-021) but focuses on type confusion attacks rather than false positives from the `---` structural cue.

The path-first detection makes this low-risk for files with known paths, but for the structure-only fallback case (when no file path is provided to `UniversalDocument.parse()`), the classification is unreliable. This is the coverage gap behind `document_type.py` lines 270, 287, 292, 297, 300 being uncovered in the test suite.

---

### Finding SV-004: UniversalDocument.parse() Passes Empty String to DocumentTypeDetector When No file_path

| Field | Detail |
|-------|--------|
| **Severity** | Low -- correctness note |
| **Location** | `src/domain/markdown_ast/universal_document.py`, lines 157-160 |

When `file_path` is `None`, the code calls:
```python
detected_type, detection_warning = DocumentTypeDetector.detect("", content)
```

`_normalize_path("")` returns `""`. The path-based detection loop returns `None` for an empty string (no pattern matches). This silently falls through to structure-only detection. The behavior is correct but should be documented -- a caller who omits `file_path` and provides content that begins with `---` will receive `DocumentType.AGENT_DEFINITION` even if the content is not an agent definition.

The implementation report does not document this behavior in any "Known Gaps" or "Design Notes" section.

---

## Per-Dimension Preliminary Scores

### Deliverable A: Implementation Report (eng-backend-001)

| Dimension | Weight | Raw Score (0.0-1.0) | Weighted |
|-----------|--------|---------------------|---------|
| Completeness | 0.20 | 0.82 | 0.164 |
| Internal Consistency | 0.20 | 0.78 | 0.156 |
| Methodological Rigor | 0.20 | 0.88 | 0.176 |
| Evidence Quality | 0.15 | 0.75 | 0.113 |
| Actionability | 0.15 | 0.90 | 0.135 |
| Traceability | 0.10 | 0.78 | 0.078 |
| **Deliverable A Composite** | | | **0.822** |

**Dimension rationale:**

- **Completeness (0.82):** All 21 WIs are accounted for. All required sections present. Deducted for DD-4/DD-5 absence in compliance table (IR-004) and absence of coverage analysis depth for reinject.py lines (IR-006).
- **Internal Consistency (0.78):** Two function names are incorrect (IR-001, IR-002). M-12 number collision with VA (IR-003). H-10 compliance note inconsistency between body and strategic implications (IR-007).
- **Methodological Rigor (0.88):** Implementation approach is sound. Security controls are mapped to WIs. Coverage report is provided. Deducted for not verifying function names match actual code.
- **Evidence Quality (0.75):** Four of six test file entries use approximation counts (IR-005). Two WI evidence entries reference non-existent function names (IR-001, IR-002). These are the primary evidence quality failures.
- **Actionability (0.90):** Strategic implications and known gaps are well-structured and actionable. Phase 4 deferral is clearly explained.
- **Traceability (0.78):** Mitigation-to-WI mapping is present. M-12 number collision breaks cross-document traceability (IR-003). DD numbering gap (IR-004) weakens design decision traceability.

---

### Deliverable B: Vulnerability Assessment (red-vuln-001)

| Dimension | Weight | Raw Score (0.0-1.0) | Weighted |
|-----------|--------|---------------------|---------|
| Completeness | 0.20 | 0.84 | 0.168 |
| Internal Consistency | 0.20 | 0.72 | 0.144 |
| Methodological Rigor | 0.20 | 0.85 | 0.170 |
| Evidence Quality | 0.15 | 0.83 | 0.125 |
| Actionability | 0.15 | 0.82 | 0.123 |
| Traceability | 0.10 | 0.75 | 0.075 |
| **Deliverable B Composite** | | | **0.805** |

**Dimension rationale:**

- **Completeness (0.84):** 27 findings is comprehensive. 8 new threats identified beyond the original threat model. Appendices A, B, C add significant depth. Deducted for missing Phase 3 implementation review (VA-005).
- **Internal Consistency (0.72):** Three stale statuses for remediatedfound ings (VA-001, VA-002, VA-003). M-12 mitigation semantic collision (VA-004). WI number discrepancy (VA-008). Confidence score not calibrated against scope (VA-006). This is the lowest dimension due to multiple consistency failures.
- **Methodological Rigor (0.85):** PTES/OSSTMM/DREAD methodology is well-applied. DREAD challenge log is rigorous. Defense-in-depth analysis by zone is sound. Deducted for not scoping the assessment temporally against Phase 3 implementation.
- **Evidence Quality (0.83):** Direct code review evidence is strong for the 8 files listed. Attack vectors are concrete and specific. Deducted for stale statuses that would lead a Phase 4 team to re-investigate already-mitigated vulnerabilities.
- **Actionability (0.82):** Priority ordering (P0/P1/P2/P3) is clear. Attack catalog is actionable for Phase 4 testing. Insufficient mitigations are identified (VA-009). Deducted for lack of specific implementation guidance for the three insufficient mitigations.
- **Traceability (0.75):** CWE/DREAD/threat model references are consistently applied. M-12 collision (Finding IR-003/VA-004) breaks cross-document traceability. WI number discrepancy (VA-008) breaks WI-to-finding traceability.

---

## Composite Preliminary Score

| Deliverable | Weighted Score | Threshold | Pass/Fail |
|-------------|---------------|-----------|-----------|
| Implementation Report (A) | 0.822 | 0.95 | FAIL |
| Vulnerability Assessment (B) | 0.805 | 0.95 | FAIL |
| **Combined (equal weight)** | **0.814** | **0.95** | **FAIL** |

**Threshold context:** C4 criticality with user-specified threshold of 0.95 (above standard 0.92). Neither deliverable passes at the 0.95 threshold or the standard 0.92 threshold.

**Primary drivers of score reduction:**

For Deliverable A:
- IR-001/IR-002: Function name inaccuracies in evidence (high impact on Evidence Quality and Internal Consistency)
- IR-003: M-12 number collision (cross-document traceability break)

For Deliverable B:
- VA-001/VA-002/VA-003: Three stale "CONFIRMED -- no mitigation" statuses for mitigations now implemented in Phase 3 (high impact on Internal Consistency)
- VA-005/VA-006: Scope not bounded temporally; confidence score overclaimed

---

## Improvement Recommendations

### Priority 1 (Required for Threshold -- Factual Corrections)

| ID | Deliverable | Finding | Required Action |
|----|-------------|---------|-----------------|
| REC-001 | A | IR-001 | Correct WI-020 evidence: remove reference to non-existent `_atomic_write()`. State the actual implementation: "inline in `ast_modify()` (lines 510-535) using `tempfile.mkstemp()` + `os.rename()`." |
| REC-002 | A | IR-002 | Correct WI-018 evidence: change `_resolve_and_check_path()` to `_check_path_containment()` (actual function at `ast_commands.py` line 178). |
| REC-003 | A | IR-003 | Add note to Security Mitigations table: cite the authoritative mitigation numbering source (threat model document reference). Disambiguate M-12 conflict with VA's M-12. |
| REC-004 | B | VA-001 | Update RV-003 status from "CONFIRMED -- no mitigation exists" to "MITIGATED (WI-018, Phase 3). M-08/M-10 implemented via `_check_path_containment()` in `ast_commands.py`." |
| REC-005 | B | VA-002 | Update RV-005 status from "CONFIRMED -- no freeze mechanism" to "MITIGATED (WI-003, Phase 0). `SchemaRegistry.freeze()` implemented; frozen at module load time in `schema.py`." |
| REC-006 | B | VA-003 | Update RV-007 status from "CONFIRMED -- no atomic write" to "MITIGATED (WI-020, Phase 3). Atomic write via `tempfile.mkstemp()` + `os.rename()` in `ast_modify()`." Also correct WI reference from WI-019 to WI-020. |
| REC-007 | B | VA-005 | Add scope boundary statement to the Executive Summary: "This assessment was conducted against the pre-Phase-3 codebase. L1-A findings reflect pre-implementation state. Phase 3 implementation status for L1-A mitigations requires re-verification." |
| REC-008 | B | VA-006 | Revise confidence score for "Existing code analysis" from 0.92 to reflect that 9 Phase 1-3 new source files were not reviewed. Suggested: 0.80 with notation "bounded to 8 pre-Phase-3 files." |

### Priority 2 (Strengthening -- Evidence and Consistency)

| ID | Deliverable | Finding | Recommended Action |
|----|-------------|---------|-------------------|
| REC-009 | A | IR-004 | Add DD-4 and DD-5 rows to Design Decision Compliance table with either compliance status or "N/A -- [reason]." |
| REC-010 | A | IR-005 | Replace approximation counts (~35, ~15, ~25, ~22) with exact counts from `pytest --collect-only`. Exact counts are available given the total of 446 tests is reported precisely. |
| REC-011 | A | IR-006 | Add analysis of what code paths lines 265-281 in reinject.py represent. Clarify whether they include the collision-risk path identified in RV-015. |
| REC-012 | A | IR-007 | Add `document_type.py` to the H-10 compliance note list of multi-class files. Revise framing from "pre-existing" to "new files co-located per ADR exception." |
| REC-013 | B | VA-009 | Add specific implementation guidance for three insufficient mitigations (M-03: pre-parse anchor count; M-05: `regex` library with timeout or signal; M-12: directory allowlist). |

### Priority 3 (Source Code Corrections -- Minor)

| ID | Source | Finding | Recommended Action |
|----|--------|---------|-------------------|
| REC-014 | `html_comment.py` line 53 | SV-001 | Correct the inline comment: remove reference to non-existent `_is_reinject` function. State actual mechanism: "case-insensitive exclusion handled by `_REINJECT_PREFIX_RE.match()` at line 175." |
| REC-015 | `yaml_frontmatter.py` | SV-002 | Clarify `YamlFrontmatterField.value` docstring: distinguish "original typed value (bool/int/float/etc.)" from the normalized string representation in `value_type`. |
| REC-016 | `document_type.py` | SV-003 | Document limitation of `"---"` structural cue in the class docstring or in a comment: "Note: `---` matches any file containing a horizontal rule; reliable only for files where path detection fails." |

---

<!-- AGENT: adv-executor | STRATEGY: S-010 (Self-Refine) | QG: QG-B2 | DATE: 2026-02-23 -->
<!-- THRESHOLD: 0.95 (C4) | RESULT: FAIL | COMPOSITE: 0.814 -->
<!-- DELIVERABLE A: 0.822 | DELIVERABLE B: 0.805 -->
