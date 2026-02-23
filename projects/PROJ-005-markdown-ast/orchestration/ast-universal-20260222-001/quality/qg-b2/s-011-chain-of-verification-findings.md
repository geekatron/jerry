# S-011 Chain-of-Verification Findings

<!-- QG-B2 | STRATEGY: S-011 | AGENT: adv-executor | CRITICALITY: C4 -->
<!-- DATE: 2026-02-23 | ENGAGEMENT: PROJ-005 Universal Markdown Parser -->

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | Verification outcome, overall confidence, critical findings |
| [Implementation Report Claims](#implementation-report-claims) | Claims 1-8 verified against source and test evidence |
| [Vulnerability Assessment Claims](#vulnerability-assessment-claims) | Claims 9-12 verified against report content |
| [Cross-Report Discrepancies](#cross-report-discrepancies) | Inconsistencies found between the two deliverables |
| [Verification Methodology](#verification-methodology) | How each claim was verified |

---

## Executive Summary

**Strategy:** S-011 (Chain-of-Verification)
**Deliverables evaluated:**
1. `eng/phase-3-implementation/eng-backend-001/eng-backend-001-implementation-report.md`
2. `red/phase-2-vulnerability/red-vuln-001/red-vuln-001-vulnerability-assessment.md`

**Verification outcome summary:**

| Claim | Status | Severity of Discrepancy |
|-------|--------|------------------------|
| 1. 21 of 21 work items completed | VERIFIED | -- |
| 2. 446 unit tests passing | VERIFIED | -- |
| 3. 98% domain coverage | VERIFIED | -- |
| 4. yaml.safe_load() exclusively | VERIFIED | -- |
| 5. No xml.etree imports | VERIFIED | -- |
| 6. S506 ruff rule | PARTIALLY_VERIFIED | Minor: location description inaccurate |
| 7. Frozen dataclasses | VERIFIED | -- |
| 8. 24 mitigations implemented | PARTIALLY_VERIFIED | Significant: table has 21 rows, not 24 |
| 9. 27 findings | VERIFIED | -- |
| 10. DREAD scores | VERIFIED | -- |
| 11. CWE mappings | VERIFIED | -- |
| 12. Pre-existing vulnerabilities | VERIFIED | -- |

**Overall confidence in deliverables:** HIGH (0.91)

**Critical finding:** Claim 8 ("24 mitigations implemented") is PARTIALLY_VERIFIED. The Security Mitigations section of the implementation report lists 21 entries, not 24. The claim in the executive summary overstates the table content by 3. This discrepancy requires resolution before QG-B2 acceptance.

---

## Implementation Report Claims

### Claim 1: "21 of 21 work items completed"

**Claimed in:** Executive Summary, line "Work items completed | 21 of 21 (WI-001 through WI-021)"

**Verification method:** Read the Work Item Completion Matrix section; count rows; check for any non-DONE status values.

**Evidence:**
- Matrix contains exactly 21 rows (WI-001 through WI-021).
- `grep "^| WI-" ... | wc -l` returns 21.
- `grep "^| WI-" ... | grep -v "DONE"` returns zero matches -- all 21 rows carry status DONE.
- Each WI entry includes specific file names, line numbers, or test function names as evidence.

**Status: VERIFIED**

---

### Claim 2: "446 unit tests passing"

**Claimed in:** Executive Summary table, line "Unit tests (markdown_ast) | 446 passed" and Coverage Report header "Coverage for `src/domain/markdown_ast/` from 446 unit tests"

**Verification method:** Run `uv run pytest tests/unit/domain/markdown_ast/ -v --tb=short` and read the final summary line.

**Evidence:**
```
============================= 446 passed in 0.70s ==============================
```
All 446 tests pass. Zero failures. Zero errors.

**Status: VERIFIED**

---

### Claim 3: "98% domain coverage"

**Claimed in:** Executive Summary "Domain module coverage | 98% (879 stmts, 20 missed)" and Coverage Report table "TOTAL | 879 | 20 | 98%"

**Verification method:** Run `uv run pytest tests/unit/domain/markdown_ast/ --cov=src/domain/markdown_ast --cov-report=term-missing` and read the coverage output.

**Evidence:**
```
Name                                                Stmts   Miss  Cover   Missing
---------------------------------------------------------------------------------
src/domain/markdown_ast/__init__.py                    13      0   100%
src/domain/markdown_ast/document_type.py               89      5    94%   270, 287, 292, 297, 300
src/domain/markdown_ast/frontmatter.py                 90      0   100%
src/domain/markdown_ast/html_comment.py                68      0   100%
src/domain/markdown_ast/input_bounds.py                17      0   100%
src/domain/markdown_ast/jerry_document.py              65      0   100%
src/domain/markdown_ast/nav_table.py                   69      0   100%
src/domain/markdown_ast/reinject.py                    51     11    78%   164, 265-281
src/domain/markdown_ast/schema.py                      92      0   100%
src/domain/markdown_ast/schema_definitions.py          29      0   100%
src/domain/markdown_ast/schema_registry.py             29      0   100%
src/domain/markdown_ast/universal_document.py          69      2    97%   188, 196
src/domain/markdown_ast/universal_parse_result.py      22      0   100%
src/domain/markdown_ast/xml_section.py                 63      0   100%
src/domain/markdown_ast/yaml_frontmatter.py           113      2    98%   317-318
---------------------------------------------------------------------------------
TOTAL                                                 879     20    98%
```
Per-file figures, statement counts, miss counts, and missing line numbers match the report's Coverage Report table exactly.

**Status: VERIFIED**

---

### Claim 4: "yaml.safe_load() exclusively"

**Claimed in:** Executive Summary (no new dependencies, secure YAML parsing), Design Decision Compliance table (DD-10 YAML type normalization), Security Mitigations table (M-01).

**Verification method:** Grep `src/` for `yaml.load` (without `safe_`) to detect any unsafe YAML load calls.

**Evidence:**
- `grep -rn "yaml\.load\b" src/` returns no matches. Zero instances of bare `yaml.load` in source.
- In `src/domain/markdown_ast/yaml_frontmatter.py:270`: `result = yaml.safe_load(raw_yaml)` is the only YAML deserialization call.
- The module-level docstring at line 8 states: "Uses ``yaml.safe_load()`` exclusively. (M-01, T-YF-07 CWE-502)"
- CI step at `.github/workflows/ci.yml` lines 97-112 ("Check for banned YAML APIs") greps `src/` for `yaml.load(` and `yaml.unsafe_load(` and fails on any match.

**Status: VERIFIED**

---

### Claim 5: "No xml.etree imports"

**Claimed in:** WI-007 evidence ("Regex-only parsing (DD-6, M-11)"), Design Decision Compliance (DD-6: "No xml.etree import anywhere in domain layer").

**Verification method:** Grep `src/` for `xml.etree` import statements.

**Evidence:**
- `grep -rn "^import xml\.etree|^from xml\.etree" src/` returns no matches.
- The only occurrence of the string `xml.etree` in `src/` is in a docstring comment in `xml_section.py:9`: "Does NOT use any XML parser library (``xml.etree``, ``lxml``, ``xml.sax``)" -- this is documentation, not an import.
- `grep "^import\|^from" src/domain/markdown_ast/xml_section.py` confirms imports are: `__future__`, `re`, `dataclasses`, `src.domain.markdown_ast.input_bounds`, `src.domain.markdown_ast.jerry_document`.

**Status: VERIFIED**

---

### Claim 6: "S506 ruff rule"

**Claimed in:** WI-004 evidence "pyproject.toml ruff `[tool.ruff.lint.per-file-ignores]` enables S506"

**Verification method:** Read `pyproject.toml` to locate the S506 configuration.

**Evidence:**
- S506 IS present and active in `pyproject.toml` at line 104:
  ```toml
  [tool.ruff.lint]
  select = [
      ...
      "S506",  # WI-004: Ban unsafe YAML APIs (yaml.load, yaml.unsafe_load) (T-YF-07, M-01)
  ]
  ```
- S506 is in the `select` list under `[tool.ruff.lint]`, meaning it is globally enabled for the project.

**Discrepancy:** The implementation report's WI-004 evidence string says `[tool.ruff.lint.per-file-ignores]`. The actual location is `[tool.ruff.lint]` `select`. These are different TOML sections with different semantics. `per-file-ignores` suppresses rules per file; `select` enables rules globally. The report's citation of the wrong TOML section is a minor documentation inaccuracy. The underlying fact (S506 is active) is correct.

**Status: PARTIALLY_VERIFIED** -- S506 is active; the report's location description (`per-file-ignores`) is incorrect. The actual location is `[tool.ruff.lint]` `select`.

---

### Claim 7: "Frozen dataclasses"

**Claimed in:** WI-001 evidence ("FrontmatterField frozen=True"), WI-002 evidence ("Frozen dataclass"), multiple WI entries for new domain classes, Design Decision Compliance (DD-8).

**Verification method:** Grep `src/domain/markdown_ast/` for `@dataclass(frozen=True)`.

**Evidence:**
All new domain classes use `frozen=True`:
```
src/domain/markdown_ast/schema.py:67:@dataclass(frozen=True)          -- FieldRule
src/domain/markdown_ast/schema.py:94:@dataclass(frozen=True)          -- EntitySchema
src/domain/markdown_ast/schema.py:113:@dataclass(frozen=True)         -- SchemaMatch
src/domain/markdown_ast/schema.py:144:@dataclass(frozen=True)         -- ValidationResult
src/domain/markdown_ast/schema.py:176:@dataclass(frozen=True)         -- FieldValidationResult
src/domain/markdown_ast/input_bounds.py:30:@dataclass(frozen=True)    -- InputBounds (WI-002)
src/domain/markdown_ast/reinject.py:84:@dataclass(frozen=True)        -- ReinjectDirective
src/domain/markdown_ast/universal_document.py:52:@dataclass(frozen=True) -- (WI-013)
src/domain/markdown_ast/nav_table.py:55:@dataclass(frozen=True)       -- NavEntry
src/domain/markdown_ast/xml_section.py:76:@dataclass(frozen=True)     -- XmlSection (WI-007)
src/domain/markdown_ast/xml_section.py:93:@dataclass(frozen=True)     -- XmlSectionResult (WI-007)
src/domain/markdown_ast/frontmatter.py:54:@dataclass(frozen=True)     -- FrontmatterField (WI-001)
src/domain/markdown_ast/yaml_frontmatter.py:72:@dataclass(frozen=True) -- YamlFrontmatterField (WI-005)
src/domain/markdown_ast/yaml_frontmatter.py:89:@dataclass(frozen=True) -- YamlFrontmatterResult (WI-005)
src/domain/markdown_ast/universal_parse_result.py:45:@dataclass(frozen=True) -- UniversalParseResult (WI-013)
src/domain/markdown_ast/html_comment.py:71:@dataclass(frozen=True)    -- HtmlCommentField (WI-009)
src/domain/markdown_ast/html_comment.py:86:@dataclass(frozen=True)    -- HtmlCommentResult (WI-009)
src/domain/markdown_ast/html_comment.py:101:@dataclass(frozen=True)   -- (WI-009)
```
All new domain dataclasses created in this implementation use `frozen=True`. The pre-existing `BlockquoteFrontmatter` and `JerryDocument` classes are not frozen (noted as technical debt by both the implementation report and the red team assessment).

**Status: VERIFIED**

---

### Claim 8: "24 mitigations implemented"

**Claimed in:** Executive Summary "The implementation enforces 24 threat model mitigations and remediates 2 pre-existing vulnerabilities (V-05, V-06)." Section heading "Security Mitigations Implemented" also implies 24.

**Verification method:** Count the rows in the Security Mitigations Implemented table.

**Evidence:**
The table contains exactly 21 rows (verified by `grep "^| M-" ... | wc -l` returning 21):

| Mitigations Listed | IDs |
|-------------------|-----|
| 21 table rows | M-01, M-04b, M-05, M-06, M-07, M-08, M-10, M-11, M-12, M-13, M-14, M-15, M-16, M-17, M-18, M-19, M-20, M-21, M-22, M-23, M-24 |

**Missing from table (gaps relative to 24):**
- M-02 is absent from the implementation table (present in the threat model and red team's Appendix B as "Banned API lint (CI grep)" -- this is what WI-021 implements, which appears as M-04b in the implementation report).
- M-03 is absent (YAML anchor/alias depth limit -- the red team flags this as "INSUFFICIENT" in Appendix B because PyYAML has no native support).
- M-04 is absent as a standalone entry (M-04b appears but not M-04 itself: "SchemaRegistry freeze" is implemented as SchemaRegistry with `freeze()` method per WI-003, but is not in the mitigations table).
- M-09 is absent (path traversal prevention -- the implementation report's M-10 covers this functionality, but M-09 is missing as a distinct entry).

**Analysis:** The executive summary claims "24 mitigations" but the evidentiary table has 21 rows. The discrepancy of 3 could be explained by: (a) the report's mitigation numbering does not match the threat model's M-01 through M-24 numbering sequentially (gaps at M-02, M-03, M-04, M-09), (b) some mitigations that are combined under a single WI may not be individually listed.

This is a material discrepancy between the executive summary metric and the supporting evidence table.

**Status: PARTIALLY_VERIFIED** -- The table supports 21 implemented mitigations, not 24. The three-item gap between the claimed count (24) and the table evidence (21) is not explained in the report.

---

## Vulnerability Assessment Claims

### Claim 9: "27 findings"

**Claimed in:** L0 Executive Summary "Total | 27" and section heading "L1: Detailed Findings"

**Verification method:** Count `#### RV-` section headings in the document.

**Evidence:**
- `grep -c "^#### RV-" red-vuln-001-vulnerability-assessment.md` returns 27.
- Finding IDs are RV-001 through RV-027, all consecutive with no gaps.
- Severity breakdown in the table: Critical (2) + High (8) + Medium (11) + Low (6) = 27. ✓

**Status: VERIFIED**

---

### Claim 10: "DREAD scores"

**Claimed in:** Top 5 findings table and individual finding tables.

**Verification method:** Extract D+R+E+A+D dimension values from each of the top 5 findings and verify they sum to the stated total.

**Evidence:**

| Finding | Dimensions (D,R,E,A,D) | Sum | Claimed | Match |
|---------|------------------------|-----|---------|-------|
| RV-001 | 10, 9, 8, 8, 7 | 42 | 42 | YES |
| RV-002 | 10, 7, 7, 9, 8 | 41 | 41 | YES |
| RV-003 | 8, 9, 8, 6, 6 | 37 | 37 | YES |
| RV-004 | 7, 8, 7, 7, 6 | 35 | 35 | YES |
| RV-005 | 8, 6, 6, 8, 6 | 34 | 34 | YES |

All five DREAD totals are arithmetically correct. The dimension values are internally consistent (each component 1-10, five components, total is sum of five values).

**Status: VERIFIED**

---

### Claim 11: "CWE mappings"

**Claimed in:** Individual finding tables and Top 5 summary table.

**Verification method:** Verify each CWE ID for the top 5 findings is real and appropriately matched to the described vulnerability class (verified against established CWE knowledge base).

**Evidence:**

| Finding | CWE | Description | Appropriate? |
|---------|-----|-------------|-------------|
| RV-001 | CWE-502 | Deserialization of Untrusted Data | YES -- YAML `yaml.load()` enabling code execution is the canonical CWE-502 scenario |
| RV-002 | CWE-94 | Improper Control of Generation of Code | YES -- injecting governance directives that modify control flow is code/logic injection |
| RV-003 | CWE-22 | Improper Limitation of a Pathname to a Restricted Directory | YES -- path traversal to read files outside the workspace is the exact CWE-22 scenario |
| RV-004 | CWE-1333 | Inefficient Regular Expression Complexity | YES -- ReDoS via catastrophic backtracking is the canonical CWE-1333 scenario |
| RV-005 | CWE-913 | Improper Control of Dynamically-Managed Code Resources | YES -- runtime mutation of a module-level schema registry falls within CWE-913 |

Additional CWEs verified spot-check:
- RV-008: CWE-471 (Modification of Assumed-Immutable Data) -- correct for mutable domain objects claiming immutability.
- RV-007: CWE-367 (Time-of-check Time-of-use Race Condition) -- correct for TOCTOU write-back.
- RV-019: CWE-776 (Improper Restriction of Recursive Entity References in DTDs) -- this CWE is technically for XML DTD entity expansion (the "Billion Laughs" origin). YAML anchor expansion is analogous but not identical. The CWE is close but not the most precise mapping; CWE-400 (Uncontrolled Resource Consumption) would be equally appropriate. This is a judgment call, not an error.

All CWE IDs are real (not fabricated) and are contextually appropriate to their associated vulnerability descriptions.

**Status: VERIFIED** -- with minor note on RV-019 CWE-776 mapping precision.

---

### Claim 12: "Pre-existing vulnerabilities" (7 cited existing vulns match code review)

**Claimed in:** L0 Executive Summary "The existing AST subsystem has 7 pre-existing vulnerabilities (V-01 through V-07 per threat model)"

**Verification method:** Read the threat model file to confirm V-01 through V-07 exist as defined; verify the vulnerability descriptions in the red team report match the threat model definitions; spot-check V-05 and V-06 remediation against source code.

**Evidence:**

From `eng-architect-001-threat-model.md` lines 614-620:
```
V-01: ast_commands.py:144-163 (_read_file) -- No path containment
V-02: ast_commands.py:380-419 (ast_modify) -- Write-back unconstrained
V-03: frontmatter.py:46 (_FRONTMATTER_PATTERN) -- No max match count
V-04: schema.py:279 (re.fullmatch) -- No ReDoS protection
V-05: frontmatter.py:54 (FrontmatterField) -- mutable dataclass
V-06: schema.py:530 (_SCHEMA_REGISTRY) -- mutable dict, runtime poisoning
V-07: reinject.py:94 (extract_reinject_directives) -- no file-origin trust
```

The red team report's references to each V-number match the threat model definitions:
- RV-003 references V-01 (path traversal in `_read_file`) -- matches.
- RV-007 references V-02 (TOCTOU in `ast_modify`) -- matches.
- RV-005 references V-06 (SchemaRegistry poisoning) -- matches.
- RV-006 references V-07 (reinject no origin check) -- matches.
- RV-008 references V-05 (FrontmatterField mutability) -- matches (partial remediation noted).

**V-05 remediation verification (source code):**
`src/domain/markdown_ast/frontmatter.py:54`: `@dataclass(frozen=True)` is confirmed present on `FrontmatterField`. The red team correctly notes partial remediation -- the containing `_fields: list` is still mutable (RV-008).

**V-06 remediation verification (source code):**
`src/domain/markdown_ast/schema_registry.py` implements `SchemaRegistry` class with `freeze()` method. The `schemas` property returns `MappingProxyType(self._schemas)` (read-only view). The old `_SCHEMA_REGISTRY` module-level dict has been replaced by a `SchemaRegistry` instance.

**Status: VERIFIED**

---

## Cross-Report Discrepancies

Two discrepancies exist between the implementation report and the red team vulnerability assessment that are not acknowledged by either document.

### Discrepancy 1: M-11 Numbering Conflict

**Implementation Report (M-11):** "Regex-only XML parsing | WI-007 | XmlSectionParser uses regex, no xml.etree (DD-6)"

**Red Team Assessment (M-11):** "Symlink resolution -- `Path.resolve(strict=True)` before all file operations" (Appendix B and throughout recommendations).

These are two different mitigations assigned the same M-number. The implementation report's numbering does not align with the threat model's mitigation numbering that the red team uses. This creates confusion in cross-referencing between the two deliverables.

**Impact:** Readers comparing the two reports cannot reliably map mitigation numbers across documents. This undermines the traceability chain between architecture, implementation, and security validation.

### Discrepancy 2: M-04 / M-04b / M-02 Numbering

**Implementation Report:** Lists "M-04b | CI grep check for banned YAML APIs | WI-021". The "b" suffix is non-standard. The implementation report does not include M-02 or M-04 as standalone rows.

**Red Team Assessment (Appendix B):** Lists M-02 as "Banned API lint (CI grep for yaml.load)" with status "Planned (WI-024)". The red team's WI-024 differs from the implementation report's WI-021 for the same logical mitigation.

**Impact:** The red team's mitigation validation table (Appendix B) cannot be reliably reconciled with the implementation report's mitigation table due to numbering misalignment.

---

## Verification Methodology

| Claim | Method | Tool Used |
|-------|--------|-----------|
| WI completion | Direct read of Work Item Completion Matrix; grep for non-DONE rows | Read, Grep |
| Test count | Execute test suite via uv run pytest | Bash |
| Coverage | Execute pytest with --cov flag | Bash |
| yaml.safe_load | Negative grep for `yaml.load\b` in src/ | Grep |
| xml.etree | Negative grep for `^import xml.etree` and `^from xml.etree` in src/ | Grep |
| S506 | Read pyproject.toml and locate S506 configuration | Read |
| Frozen dataclasses | Grep for `@dataclass(frozen=True)` in domain directory | Grep |
| Mitigation count | Grep and count `^| M-` rows in implementation report table | Bash |
| Finding count | Count `^#### RV-` headings in vulnerability assessment | Bash |
| DREAD arithmetic | Extract D+R+E+A+D values from finding tables, compute sums | Manual calculation |
| CWE validation | Cross-reference CWE IDs against established weakness taxonomy | Knowledge base |
| Pre-existing vulns | Read threat model source file; compare to report references; inspect source | Read, Grep |

---

## Overall Assessment

**Verified claims:** 10 of 12 (fully VERIFIED)
**Partially verified claims:** 2 of 12 (PARTIALLY_VERIFIED)
**Unverified claims:** 0 of 12

**Quality threshold (>= 0.95):** The two partially-verified findings represent material inaccuracies that reduce confidence below the 0.95 threshold.

**Confidence in each deliverable:**

| Deliverable | Confidence | Primary Issue |
|-------------|------------|---------------|
| Implementation Report | 0.88 | "24 mitigations" claim overstates the table by 3; S506 section citation is wrong |
| Vulnerability Assessment | 0.93 | Finding count, DREAD arithmetic, and CWE IDs are accurate; strong methodology |

**Required corrections before QG-B2 acceptance:**

1. **Implementation Report (BLOCKING):** Reconcile the "24 mitigations implemented" executive summary claim with the 21-row Security Mitigations table. Either: (a) add the missing 3 mitigation rows, or (b) correct the executive summary to state "21 mitigations". Also update M-11 numbering to align with the threat model's mitigation numbering.

2. **Implementation Report (MINOR):** Correct WI-004 evidence string. Replace "`[tool.ruff.lint.per-file-ignores]`" with "`[tool.ruff.lint]` select" to accurately describe where S506 is configured.

3. **Cross-Report (MEDIUM):** The M-number namespace conflict between the implementation report and red team assessment should be resolved in a follow-up document or errata note, so that future reviewers can reliably cross-reference mitigations across the two deliverables.

---

<!-- Agent: adv-executor | Strategy: S-011 | QG: QG-B2 | Date: 2026-02-23 -->
*S-011 Chain-of-Verification v1.0.0*
*Deliverables evaluated: Implementation Report + Vulnerability Assessment*
*Status: PARTIALLY_VERIFIED (2 claims require correction before QG-B2 acceptance)*
