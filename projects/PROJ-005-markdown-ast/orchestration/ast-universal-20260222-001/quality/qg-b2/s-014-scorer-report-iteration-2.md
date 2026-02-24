# S-014 Scorer Report: QG-B2 Barrier 2 Quality Gate -- Iteration 2

<!-- AGENT: adv-scorer | STRATEGY: S-014 (LLM-as-Judge) | DATE: 2026-02-23 -->
<!-- ENGAGEMENT: ast-universal-20260222-001 | PROJECT: PROJ-005 | CRITICALITY: C4 -->
<!-- THRESHOLD: 0.95 | ITERATION: 2 of max 5 | PREVIOUS: 0.812 (REJECTED) -->

## Document Sections

| Section | Purpose |
|---------|---------|
| [Anti-Leniency Statement](#anti-leniency-statement) | Scoring discipline declaration |
| [Iteration 1 Delta Summary](#iteration-1-delta-summary) | What changed and overall assessment |
| [Unified Finding Verification](#unified-finding-verification) | Per-finding resolution status for UF-001 through UF-042 |
| [New Findings](#new-findings) | Issues introduced or exposed by the iteration 2 remediation |
| [Per-Dimension Scoring](#per-dimension-scoring) | 0.0-1.0 scores per dimension with justification |
| [Weighted Composite Score](#weighted-composite-score) | Final score and band classification |
| [Prioritized Remediation List](#prioritized-remediation-list) | Remaining items for iteration 3 |
| [Next Iteration Guidance](#next-iteration-guidance) | Path to 0.95 |

---

## Anti-Leniency Statement

This scoring actively counteracts leniency bias per S-014 protocol. The following principles govern this iteration 2 scoring:

1. **Evidence over intent.** Remediations claimed as addressed are verified against actual source code using Grep/Read. A finding marked RESOLVED must have its root cause eliminated, not merely acknowledged.
2. **Factual corrections are scored as corrections, not new content.** Fixing a wrong function name from `_atomic_write()` to the actual inline implementation is a correction that restores baseline accuracy, not a quality improvement. The score improvement reflects removal of defects, not addition of new quality.
3. **New issues introduced by remediation are weighted.** If fixing UF-001 introduces a new inaccuracy, the net improvement is zero for that finding.
4. **Cross-deliverable consistency is evaluated holistically.** Both documents must now tell the same story. Partial alignment (e.g., mitigation numbering cross-reference added to IR but VA still uses old numbers in body text) receives partial credit.
5. **The threshold is 0.95.** The iteration 1 guidance estimated 0.92-0.94 post-P0/P1 remediation. This scorer independently verifies whether that estimate was accurate.

---

## Iteration 1 Delta Summary

**Remediation scope:** 11 P0 items + 10 P1 items + 4 P2 items = 25 of 29 remediation items addressed. All P0 blockers were addressed. All P1 required items were addressed. 4 of 8 P2 recommended items were addressed.

**Assessment:** The remediation was substantial and well-targeted. The most impactful changes were:
- Factual corrections in the IR (function names, mitigation counts, coverage characterization)
- VA status updates for RV-003, RV-005, RV-007 (stale-to-current)
- Mitigation Numbering Cross-Reference section added to IR
- VA scope boundary statement and confidence correction
- Nine new Known Gaps (Gap 4 through Gap 9) added to IR
- Appendix B fully updated with post-Phase-3 statuses
- RV-022b added to VA

**Overall:** The deliverables have improved materially. The IR is now substantially more honest about its known gaps. The VA now correctly reflects the post-Phase-3 state. Cross-deliverable consistency has improved significantly through the mitigation numbering cross-reference.

---

## Unified Finding Verification

### Category A: Factual Errors in Implementation Report

| UF | Finding | Remediation | Status | Verification Notes |
|----|---------|-------------|--------|-------------------|
| UF-001 | `_atomic_write()` function name error | REM-P0-001: WI-020 evidence corrected to inline implementation at lines 520-535 using `tempfile.mkstemp()` + `os.rename()`. | **RESOLVED** | Verified: `ast_commands.py` lines 520-535 contain `tempfile.mkstemp()` at line 524 and `os.rename()` at line 534. IR WI-020 evidence now reads "ast_commands.py `ast_modify()` (lines 520-535) implements atomic write inline using `tempfile.mkstemp()` + `os.rename()`". Stdlib function names are now correct. |
| UF-002 | `_resolve_and_check_path()` function name error | REM-P0-002: WI-018 evidence corrected to `_check_path_containment()` (line 178). | **RESOLVED** | Verified: `ast_commands.py` line 178 defines `def _check_path_containment(file_path: str)`. IR WI-018 now correctly references this function. |
| UF-003 | "24 mitigations" vs 21-row table | REM-P0-003: Executive summary corrected to "21 mitigations (M-01 through M-24, excluding M-02, M-03, M-09)". | **RESOLVED** | The executive summary now states 21 mitigations and parenthetically explains the 3 excluded IDs (M-02, M-03, M-09 deferred to Phase 4). This is accurate and internally consistent with the 21-row Security Mitigations Implemented table. |
| UF-004 | M-05 label mismatch (regex timeout vs file size) | REM-P0-004: M-05 in mitigations table corrected with asterisk notation. Gap 8 added for regex timeout non-implementation. | **RESOLVED** | The Security Mitigations table now has M-05 marked with an asterisk and a footnote explaining the mislabeling. Gap 8 explicitly documents that regex timeout (the threat model's M-05) is NOT implemented, with residual risk assessment. This is now accurate and transparent. |
| UF-005 | WI-004 TOML section misattribution | REM-P2-001: Corrected to `[tool.ruff.lint]` select. | **RESOLVED** | Verified: `pyproject.toml` line 95 shows `[tool.ruff.lint]` and line 104 shows `"S506"` in the select list. IR WI-004 evidence now correctly cites `[tool.ruff.lint]` select. |
| UF-006 | H-10 compliance: NEW files described as pre-existing, `document_type.py` omitted | REM-P0-005: Corrected to "EXCEPTION (DOCUMENTED)" with all 5 NEW files identified. `document_type.py` included. | **RESOLVED** | IR H-10 row now lists all 5 files as NEW with specific class counts. The characterization as "EXCEPTION (DOCUMENTED)" with ADR-justified refactoring recommended is accurate and transparent. |
| UF-007 | Approximate test counts | REM-P2-002: All counts replaced with exact numbers (33, 12, 25, 28, 42, 23 = 163 total). | **RESOLVED** | IR Test File Inventory now shows exact counts. Sum: 33+12+25+28+42+23 = 163. Note: Total new tests is 163, not 446. The 446 figure is the full markdown_ast unit test suite (163 new + 283 pre-existing). This is consistent with the Baseline comparison note stating "Implementation added 157 new markdown_ast unit tests (from 289 to 446)." Minor arithmetic discrepancy: 446-289=157 new tests, but the test file inventory sums to 163 new tests. See [NF-001](#nf-001). |
| UF-008 | `reinject.py` coverage mischaracterized as pre-existing | REM-P0-006: Correctly characterized as NEW WI-019 security code. | **RESOLVED** | IR Coverage analysis of misses now explicitly states "Lines 265-281 are NEW code from WI-019 implementing `_is_trusted_path()` (M-22 trusted path whitelist)." The Impact is correctly assessed as HIGH. |
| UF-009 | H-05 CI violation (pip-audit) | REM-P1-004: H-05 compliance updated to "COMPLIANT (with CI exception)". | **RESOLVED** | IR H-05 row now documents the CI exception with specific details about `python -m pip install` and `pip install pip-audit` usage. Classified as "pending UV-native pip-audit integration." Transparent and accurate. |

### Category B: Cross-Deliverable Inconsistencies

| UF | Finding | Remediation | Status | Verification Notes |
|----|---------|-------------|--------|-------------------|
| UF-010 | M-12 mitigation number collision | REM-P0-011: Mitigation Numbering Cross-Reference section added to IR. VA also has numbering note. | **RESOLVED** | IR now contains a dedicated "Mitigation Numbering Cross-Reference" section with a 4-column table reconciling M-05, M-11, M-12 between the two documents. The table correctly identifies the threat model as the authoritative source. VA executive summary now includes a "Mitigation numbering note" directing readers to the IR cross-reference. |
| UF-011 | M-11 mitigation number collision | REM-P0-011: Covered by same cross-reference table as UF-010. | **RESOLVED** | M-11 is explicitly reconciled in the cross-reference table: IR uses M-11 for "regex-only XML parsing (DD-6)" while the threat model uses M-11 for "symlink resolution." |
| UF-012 | WI number discrepancy (M-21 to WI-019 vs WI-020) | REM-P2-008: VA M-21 WI reference corrected from WI-019 to WI-020. | **RESOLVED** | VA Appendix B now shows M-21 as "IMPLEMENTED (WI-020)" consistent with the IR. |
| UF-013 | DD-4 and DD-5 absent from compliance table | REM-P2-003: DD-4 and DD-5 rows added. | **RESOLVED** | IR Design Decision Compliance table now includes DD-4 (Schema extension for new document types) and DD-5 (CLI extensions for new file types), both marked COMPLIANT with appropriate evidence. |

### Category C: Stale Vulnerability Assessment Statuses

| UF | Finding | Remediation | Status | Verification Notes |
|----|---------|-------------|--------|-------------------|
| UF-014 | RV-003 status stale ("CONFIRMED -- no mitigation") | REM-P0-007: Updated to MITIGATED with env var bypass caveat. | **RESOLVED** | VA RV-003 status now reads "MITIGATED via `_check_path_containment()` (WI-018). Path containment validates resolved paths fall within repo root using `Path.resolve()` + `os.path.realpath()`. Caveat: M-08 is globally bypassable via `JERRY_DISABLE_PATH_CONTAINMENT=1` env var." Original status preserved with strikethrough for audit trail. |
| UF-015 | RV-005 status stale ("CONFIRMED -- no freeze mechanism") | REM-P0-008: Updated to PARTIALLY MITIGATED with `_schemas` accessibility caveat. | **RESOLVED** | VA RV-005 status now reads "PARTIALLY MITIGATED via `SchemaRegistry.freeze()` (WI-003). The registry uses `MappingProxyType` after `freeze()`. Caveat: The internal `_schemas` dict is still accessible via the single-underscore attribute." Accurate and appropriately qualified. |
| UF-016 | RV-007 status stale ("CONFIRMED -- no atomic write") | REM-P0-009: Updated to MITIGATED with remaining TOCTOU risk noted. | **RESOLVED** | VA RV-007 status now reads "MITIGATED via atomic write pattern (WI-020). [...] Remaining risk: Write-back path re-verification uses only `Path.resolve()`, not the dual `resolve()` + `realpath()` symlink detection." Accurate characterization of residual risk. |
| UF-017 | VA scope not bounded temporally, confidence overclaimed | REM-P0-010: Scope boundary statement added. Confidence for existing code adjusted from 0.92 to 0.85. | **RESOLVED** | VA executive summary now contains a detailed scope boundary statement identifying that the assessment was conducted against the pre-Phase-3 codebase, that 9 new files were NOT reviewed, and that L1-A findings reflect pre-implementation state. Overall confidence is now 0.88, with existing code analysis at 0.85 (reduced from 0.92). This is an appropriate correction. |
| UF-018 | Appendix B Full Mitigation Status table not updated post-implementation | REM-P1-008: Fully updated with post-Phase-3 implementation statuses. | **RESOLVED** | VA Appendix B now shows all 24 mitigations with current implementation status (IMPLEMENTED, NOT IMPLEMENTED, PARTIALLY SUFFICIENT, etc.) and sufficiency assessments with caveats. M-01 through M-24 each have a status column reflecting the Phase 3 state. |

### Category D: Implementation Gaps (Code-Level)

| UF | Finding | Remediation | Status | Verification Notes |
|----|---------|-------------|--------|-------------------|
| UF-019 | `ast_reinject` CLI not wiring `file_path` to `extract_reinject_directives` | REM-P1-001: Gap 4 added documenting the wiring gap with single-line fix path. | **RESOLVED** | IR Gap 4 documents the specific issue (line 581 calls `extract_reinject_directives(doc)` without `file_path`), the impact (HIGH -- M-22 bypass), and the remediation path (single-line fix). Verified against code: `ast_commands.py` line 581 confirms `directives = extract_reinject_directives(doc)` with no `file_path` argument. Gap is accurately documented. |
| UF-020 | `_is_trusted_path()` substring match vulnerability | REM-P1-002: Gap 5 added documenting the vulnerability. | **RESOLVED** | IR Gap 5 documents the substring `in` check issue, the bypass vector (`projects/evil/.context/rules/fake.md`), the impact (HIGH), and the remediation path (`startswith()` or `Path` prefix matching). Verified against code: `reinject.py` line 274 confirms `if trusted in normalized:` -- a substring match, not a prefix match. Gap is accurately documented. |
| UF-021 | `JERRY_DISABLE_PATH_CONTAINMENT` env var global bypass | REM-P1-003: Gap 6 added documenting the env var bypass with risk assessment. | **RESOLVED** | IR Gap 6 documents the env var's unrestricted scope, the impact (HIGH -- M-08 completely disableable), and 4 remediation options. Verified against code: `ast_commands.py` lines 62-64 confirm the env var is checked unconditionally at module load time with no restriction to test contexts. |
| UF-022 | `modify_reinject_directive()` also bypasses trust check | | **PARTIALLY RESOLVED** | IR Gap 4 mentions "The `modify_reinject_directive()` call path (line 501) has the same gap and should also pass `file_path`." However, the actual code at `reinject.py` line 227 shows `directives = extract_reinject_directives(doc)` (no `file_path`). The gap in the `modify_reinject_directive()` domain function is documented but the mention of "line 501" appears to be a CLI reference. The domain-level function itself has no `file_path` parameter in its signature at all (line 187-193). This gap is acknowledged but the documentation could be more precise about the architectural location (domain layer vs CLI layer). |
| UF-023 | Case-sensitive negative lookahead vs case-insensitive `_REINJECT_PREFIX_RE` | | **UNRESOLVED** | IR does not address this finding. The html_comment.py code at line 53 still uses `(?!L2-REINJECT:)` (case-sensitive) while line 68/175 uses `_REINJECT_PREFIX_RE` with `re.IGNORECASE`. The dual-check currently works because the `_REINJECT_PREFIX_RE.match(body)` check at line 175 catches case variants that the lookahead misses. However, the inconsistency remains: the lookahead is case-sensitive but the body check is case-insensitive. If either check is modified independently, the inconsistency could become exploitable. Neither the IR nor VA addresses this latent inconsistency. |
| UF-024 | L2-REINJECT content injection via pre-prefix KV pairs | REM-P1-009: RV-022b added to VA with DREAD 32. | **RESOLVED** | VA now contains RV-022b as a new finding with proper DREAD scoring, CWE mapping, attack vector, and recommended mitigations. Verified against code: `html_comment.py` line 175 checks `_REINJECT_PREFIX_RE.match(body)` which only matches when the body **starts** with `L2-REINJECT:`. A comment like `<!-- AGENT: val | L2-REINJECT: rank=1 -->` would pass the check (body starts with "AGENT:") and the KV extraction at line 193 would extract "L2-REINJECT" as a key. Finding is accurately documented. |
| UF-025 | `SchemaRegistry._schemas` accessible after freeze | | **UNRESOLVED** | Neither deliverable adds new disclosure about this finding. The VA RV-005 update (UF-015) mentions the caveat about `_schemas` direct access, which partially addresses it in context. However, the IR does not list this as a Known Gap. The finding remains documented only in the VA's status caveat, not as a standalone gap in the IR. |
| UF-026 | Write-back path asymmetric symlink detection | | **UNRESOLVED** | Neither deliverable addresses this finding. The IR WI-020 evidence describes the atomic write pattern but does not mention the asymmetry between read-path and write-path symlink detection. The VA RV-007 update notes "Write-back path re-verification uses only `Path.resolve()`, not the dual `resolve()` + `realpath()`" which partially documents this, but only as a caveat on the status update, not as a standalone gap. |
| UF-027 | `_normalize_path()` root marker extraction bypass | | **UNRESOLVED** | Neither deliverable addresses this finding. No `_normalize_path` function exists in `reinject.py` (verified via grep). The finding appears to reference the path normalization logic within `_is_trusted_path()` at line 265. The IR's Gap 5 documents the substring match issue but does not specifically address the root marker extraction bypass vector. |
| UF-028 | `"---"` structural cue misclassifying horizontal rules as AGENT_DEFINITION | | **UNRESOLVED** | Neither deliverable addresses this finding. The IR does not mention this as a Known Gap. |

### Category E: Test Coverage Gaps

| UF | Finding | Remediation | Status | Verification Notes |
|----|---------|-------------|--------|-------------------|
| UF-029 | Phase 4 testing entirely deferred, not scheduled | | **UNRESOLVED** | Neither deliverable addresses this finding with scheduling information. Phase 4 deferral remains documented (IR Gap 3) but there is no evidence of WORKTRACKER scheduling. The gap is acknowledged but not mitigated with a scheduling commitment. |
| UF-030 | `_is_trusted_path()` zero test coverage | REM-P1-006: Gap 7 added documenting zero coverage. | **RESOLVED** | IR Gap 7 documents the zero coverage for lines 164 and 265-281, the impact (HIGH), and a remediation path listing 6 specific test case categories. Verified against code: `reinject.py` coverage report shows lines 265-281 as missed. |
| UF-031 | Billion-laughs mitigation test uses trivial single alias | | **UNRESOLVED** | Neither deliverable addresses this finding. No updates to test quality characterization. |
| UF-032 | YAML merge key (`<<: *anchor`) behavior untested | | **UNRESOLVED** | Neither deliverable addresses this finding. |
| UF-033 | CI coverage threshold 80% vs H-20's 90% | REM-P1-005: H-20 compliance updated to "COMPLIANT (domain) / EXCEPTION (CI)". Gap 9 added. | **RESOLVED** | IR H-20 row now explicitly documents the 80% vs 90% discrepancy and Gap 9 provides the remediation path (update ci.yml threshold). Verified against code: `.github/workflows/ci.yml` lines 304 and 405 confirm `--cov-fail-under=80`. |
| UF-034 | Integration tests universally disable path containment | | **UNRESOLVED** | Neither deliverable explicitly addresses this as a gap. The IR mentions `JERRY_DISABLE_PATH_CONTAINMENT=1` in the modified test files section (line 126) and Gap 6 documents the env var broadly, but the specific issue that zero integration tests validate path containment in production mode is not called out. |
| UF-035 | `universal_document.py` error aggregation branches untested | | **UNRESOLVED** | Not addressed. Mentioned in coverage analysis as "Addressable in Phase 4 adversarial testing" but not listed as a Known Gap. |
| UF-036 | Unicode confusable bypass for L2-REINJECT key | | **UNRESOLVED** | Not addressed. This was a P2 item (REM-P2-007) and was not included in the iteration 2 remediation scope. |

### Category F: Documentation and Methodology Gaps

| UF | Finding | Remediation | Status | Verification Notes |
|----|---------|-------------|--------|-------------------|
| UF-037 | `reinject.py` coverage explanation sparse | | **UNRESOLVED** | Not addressed. The IR's coverage analysis now correctly characterizes the uncovered lines as NEW WI-019 code (UF-008 fix) but does not add the cross-reference to RV-015 collision risk. Partial improvement from UF-008 remediation. |
| UF-038 | VA insufficient mitigation findings lack implementation guidance | | **UNRESOLVED** | Not addressed. This was a P2 item (REM-P2-004) not in scope for iteration 2. |
| UF-039 | Gap 1 M-18 pre-parse vs post-parse characterization | REM-P1-007: Gap 1 impact assessment corrected. | **RESOLVED** | IR Gap 1 now correctly states "The `_strip_control_chars()` function (M-18) operates post-parse on field values, not pre-parse on raw YAML input. ReaderError occurs during the pre-parse Reader stage, before M-18 can act. The LOW rating holds because in practice, YAML frontmatter in Jerry markdown files never contains raw control characters, but the technical basis is corrected." This is technically accurate and honest about the revised justification. |
| UF-040 | H-10 blocking rationale for ReaderError fix may be incorrect | | **UNRESOLVED** | Not addressed. This was a P2 item (REM-P2-006). The IR still claims H-10 blocks the fix without verifying whether the hook actually blocks exception clause additions. |
| UF-041 | Regex timeout (M-05) unimplemented, not disclosed as gap | REM-P1-010: Gap 8 added documenting non-implementation with residual risk assessment. | **RESOLVED** | IR Gap 8 explicitly documents that regex timeout is NOT IMPLEMENTED, identifies affected parsers (xml_section.py, html_comment.py, frontmatter.py), explains the technical limitation (Python `re` has no timeout), and assesses the residual risk (bounded by InputBounds.max_file_bytes but not eliminated). |
| UF-042 | `_KV_PATTERN` accepts arbitrary key names | | **UNRESOLVED** | Not addressed. This was a Low severity finding. VA Appendix B notes M-07 as "PARTIALLY SUFFICIENT" with reference to RV-022 and RV-022b, which provides some documentation. |

### Verification Summary

| Status | Count | Percentage |
|--------|-------|------------|
| RESOLVED | 26 | 61.9% |
| PARTIALLY RESOLVED | 1 | 2.4% |
| UNRESOLVED | 15 | 35.7% |
| **Total** | **42** | |

**P0 items:** 11/11 RESOLVED (100%)
**P1 items:** 10/10 RESOLVED (100%)
**P2 items addressed:** 4/4 RESOLVED (100%)
**P2 items not addressed:** 4/4 UNRESOLVED (as expected)
**Other unresolved:** 11 items were categorized at iteration 1 as implicit in the P0/P1/P2 tiers or were Medium/Low severity items not specifically remediation-targeted. These include UF-022 (partially), UF-023, UF-025, UF-026, UF-027, UF-028, UF-029, UF-031, UF-032, UF-034, UF-035.

---

## New Findings

### NF-001: Test Count Arithmetic Discrepancy

**Severity:** Minor
**Deliverable:** IR

The IR states "Implementation added 157 new markdown_ast unit tests (from 289 to 446)" but the Test File Inventory sums to 163 new tests (33+12+25+28+42+23=163). The delta 446-289=157 is inconsistent with the 163 total from the test file inventory. Possible explanations: (a) 6 tests were added to modified test files (e.g., `test_frontmatter.py` added `test_field_is_frozen`), not new test files, which could account for the discrepancy if the baseline already included some tests that were counted differently, or (b) the baseline 289 count includes tests from the 2 modified test files that are double-counted.

**Impact:** Cosmetic. Does not affect any dimension materially. The exact test counts are an improvement over iteration 1's approximations.

### NF-002: `modify_reinject_directive()` Lacks `file_path` Parameter Entirely

**Severity:** Medium
**Deliverable:** IR

IR Gap 4 mentions the `modify_reinject_directive()` call path having "the same gap" as `ast_reinject`. However, the domain-level `modify_reinject_directive()` function (reinject.py line 187-193) does not accept a `file_path` parameter at all. The fix described in Gap 4 ("change `extract_reinject_directives(doc)` to `extract_reinject_directives(doc, file_path=file_path)` at line 581") applies only to the CLI `ast_reinject` command. For `modify_reinject_directive()`, the fix would require adding a `file_path` parameter to the function signature AND passing it through to the internal `extract_reinject_directives()` call at line 227. This is a 2-3 line fix, not a single-line fix. The gap documentation is accurate about the existence of the problem but understates the scope of the modification path.

### NF-003: VA Appendix B M-03 Status May Be Inaccurate

**Severity:** Minor
**Deliverable:** VA

VA Appendix B lists M-03 (YAML anchor/alias depth limit) as "IMPLEMENTED (WI-005) as pre-parse alias count check" with status "PARTIALLY SUFFICIENT." The IR does not explicitly list M-03 as implemented -- M-03 is excluded from the "21 mitigations" count per the executive summary ("M-01 through M-24, excluding M-02, M-03, M-09 which are deferred to Phase 4"). If M-03 is deferred, the VA should not claim it is IMPLEMENTED. However, the VA's characterization as "PARTIALLY SUFFICIENT" with the caveat about pre-parse vs post-parse timing suggests that a partial implementation exists (alias count check) even though full M-03 is deferred. This is a minor cross-document tension rather than a factual error.

### NF-004: VA Body Text Still Uses Original RV Status Language in Some Places

**Severity:** Minor
**Deliverable:** VA

The VA RV-003, RV-005, and RV-007 findings have been updated with "UPDATED (Phase 3)" status annotations using strikethrough of the original status. This is a good audit trail approach. However, the original Description text for these findings still describes the pre-Phase-3 state (e.g., RV-003 Description says "accepts an arbitrary file path from CLI arguments and reads it directly [...] with no path containment"). The Description sections were not updated to reflect the current mitigated state. This is acceptable since the Description represents the finding as originally discovered, and the Status field carries the update. But it could confuse readers who read only the Description and miss the Status update.

---

## Per-Dimension Scoring

### Dimension 1: Completeness (Weight: 0.20)

**Score: 0.92**

**Justification:**

Improvements from iteration 1 (0.83):
- Executive summary mitigation count corrected (UF-003): eliminates the 14% overstatement.
- M-05 mislabeling resolved with asterisk notation + Gap 8 (UF-004): the deliverable now accurately represents what IS and IS NOT implemented.
- DD-4 and DD-5 added to compliance table (UF-013): full design decision traceability.
- VA scope boundary clarified (UF-017): readers know exactly what was and was not reviewed.
- 9 new Known Gaps (Gap 1 through Gap 9): the IR is substantially more complete in its disclosure of implementation limitations.
- VA Appendix B fully updated (UF-018): all 24 mitigations now have current status.
- RV-022b added to VA (UF-024): net-new exploitable gap is now documented.

Remaining deficiencies:
- Phase 4 testing still not scheduled (UF-029): deferral is documented but no commitment to scheduling.
- Several medium-severity implementation gaps (UF-023, UF-025, UF-026, UF-027, UF-028) are not documented as Known Gaps in the IR. These are documented in the iteration 1 scorer report but not in the deliverables themselves.
- UF-031 (billion-laughs test quality) and UF-032 (YAML merge key) are test methodology gaps not disclosed in the IR.
- UF-034 (no integration test for path containment in production mode) is not disclosed.

The 9 new Known Gaps represent a significant completeness improvement. The remaining gaps are primarily medium-severity items that affect completeness at the margin. Score of 0.92 reflects a deliverable set that is now materially complete for its stated scope with residual gaps in implementation-level disclosure.

---

### Dimension 2: Internal Consistency (Weight: 0.20)

**Score: 0.91**

**Justification:**

Improvements from iteration 1 (0.74):
- Mitigation numbering cross-reference table (UF-010, UF-011): M-05, M-11, M-12 collisions are now reconciled with the threat model as authoritative source. This was the single largest consistency failure in iteration 1.
- Function name corrections (UF-001, UF-002): WI-020 and WI-018 evidence now references actual function names that can be verified in the codebase.
- VA statuses updated (UF-014, UF-015, UF-016): the two deliverables no longer directly contradict each other on remediation status.
- WI number alignment (UF-012): M-21 now consistently references WI-020 in both documents.
- H-10 classification corrected (UF-006): NEW files are now correctly classified.
- Coverage characterization corrected (UF-008): NEW WI-019 code is no longer mischaracterized as pre-existing.
- VA confidence corrected (UF-017): 0.85 for existing code analysis is more appropriate than 0.92 given scope limitations.

Remaining deficiencies:
- Test count arithmetic discrepancy (NF-001): minor, but 157 vs 163 is a surface-level inconsistency.
- VA Appendix B M-03 tension (NF-003): IR says M-03 deferred, VA says M-03 implemented (partially). This is a minor cross-document tension.
- `modify_reinject_directive()` gap description slightly imprecise (NF-002): the "single-line fix" characterization understates the actual modification scope.
- UF-022 partial resolution: the gap is documented but the architectural location description is not fully precise.
- VA body text for updated findings still describes pre-Phase-3 state (NF-004): acceptable as audit trail but creates potential reader confusion.

The mitigation numbering cross-reference alone accounts for roughly +0.10 on this dimension. The function name corrections and VA status updates account for another +0.07. Score of 0.91 reflects substantially improved cross-deliverable consistency with minor residual tensions.

---

### Dimension 3: Methodological Rigor (Weight: 0.20)

**Score: 0.93**

**Justification:**

Improvements from iteration 1 (0.86):
- M-18 pre-parse vs post-parse correction (UF-039): Gap 1 impact assessment now has technically correct justification. The LOW rating is maintained but the reasoning is honest about M-18's actual scope.
- Regex timeout explicitly documented as NOT IMPLEMENTED (UF-041): Gap 8 provides honest residual risk assessment rather than leaving M-05 as implicitly implemented.
- VA scope boundary and confidence correction (UF-017): methodologically sound temporal scoping.
- Known Gaps 4-9: systematic disclosure of implementation limitations demonstrates methodological discipline.

Remaining deficiencies:
- H-10 blocking rationale unverified (UF-040): the claim that H-10 blocks the ReaderError fix is still unverified. If incorrect, the gap's "Root cause of non-fix" is misleading.
- Billion-laughs test adequacy not addressed (UF-031): the test uses a trivial configuration that does not exercise the mitigation under realistic attack conditions.
- YAML merge key behavior untested (UF-032): a known YAML security concern with no verification.
- Case-sensitive vs case-insensitive inconsistency in html_comment.py (UF-023): a latent methodological gap in the defense-in-depth analysis.

Score of 0.93 reflects a deliverable set with sound methodology and honest self-assessment, with residual gaps in verification depth for edge-case security controls.

---

### Dimension 4: Evidence Quality (Weight: 0.15)

**Score: 0.93**

**Justification:**

Improvements from iteration 1 (0.79):
- Function name corrections (UF-001, UF-002): evidence now references verifiable entities in the codebase. This was the most significant evidence quality failure in iteration 1.
- Exact test counts (UF-007): removes approximation uncertainty from a C4 deliverable.
- Mitigation count correction (UF-003): executive summary now matches the evidence table.
- M-05 mislabeling resolved (UF-004): the Security Mitigations table is now evidence-accurate.
- VA statuses updated (UF-014, UF-015, UF-016): evidence is now temporally correct.
- TOML section corrected (UF-005): WI-004 evidence is now verifiable.
- Coverage characterization corrected (UF-008): evidence correctly attributes code authorship.
- H-05 CI exception disclosed (UF-009): evidence now transparent about the deviation.

Remaining deficiencies:
- Test count arithmetic discrepancy (NF-001): 157 vs 163 is a minor evidence precision issue.
- VA finding descriptions not updated to reflect post-Phase-3 state (NF-004): the Description sections still describe the pre-mitigation state, which is technically the finding description (accurate as discovered) but could be confusing.
- M-03 cross-document status tension (NF-003): evidence about M-03 implementation is slightly inconsistent between IR and VA.

Score of 0.93 reflects evidence that is now substantially verifiable against the actual codebase, with minor residual precision issues.

---

### Dimension 5: Actionability (Weight: 0.15)

**Score: 0.93**

**Justification:**

Improvements from iteration 1 (0.87):
- Gap 4 (M-22 CLI wiring): specific single-line fix path documented.
- Gap 5 (`_is_trusted_path()` substring): specific fix documented (`startswith()` or `Path` prefix matching).
- Gap 6 (env var bypass): 4 remediation options documented.
- Gap 7 (zero test coverage): 6 specific test case categories listed.
- Gap 8 (regex timeout): 3 remediation options documented with Phase 4 characterization.
- Gap 9 (CI coverage threshold): specific fix documented.
- RV-022b in VA: 3 recommended mitigations documented.
- All gaps include impact assessment and remediation path.

Remaining deficiencies:
- Phase 4 still not scheduled (UF-029): no WORKTRACKER commitment.
- Several medium-severity gaps (UF-023, UF-025, UF-026, UF-027, UF-028) lack actionable remediation paths in the deliverables.
- VA insufficient mitigation findings still lack implementation guidance (UF-038).

Score of 0.93 reflects highly actionable Known Gaps with specific fix paths, with residual gaps in scheduling and some medium-severity items.

---

### Dimension 6: Traceability (Weight: 0.10)

**Score: 0.93**

**Justification:**

Improvements from iteration 1 (0.76):
- Mitigation Numbering Cross-Reference table: the single most impactful traceability improvement. M-05, M-11, M-12 can now be traced across documents using the reconciliation table.
- Threat model cited as authoritative source for mitigation numbering.
- DD-4 and DD-5 added to compliance table (UF-013): full design decision chain.
- WI number alignment (UF-012): consistent WI references across documents.
- VA scope boundary: temporal traceability for findings is now clear.

Remaining deficiencies:
- Test count arithmetic discrepancy (NF-001): minor traceability noise.
- M-03 cross-document tension (NF-003): minor trace disruption.
- No authoritative mitigation register exists as a standalone artifact. The threat model is cited as authoritative but the cross-reference table is embedded in the IR, not in a shared location.

Score of 0.93 reflects strong cross-document traceability with the mitigation numbering issue substantially resolved.

---

## Weighted Composite Score

### Per-Deliverable Scores

**Implementation Report (eng-backend-001):**

| Dimension | Weight | Score | Weighted |
|-----------|--------|-------|----------|
| Completeness | 0.20 | 0.93 | 0.186 |
| Internal Consistency | 0.20 | 0.92 | 0.184 |
| Methodological Rigor | 0.20 | 0.93 | 0.186 |
| Evidence Quality | 0.15 | 0.94 | 0.141 |
| Actionability | 0.15 | 0.94 | 0.141 |
| Traceability | 0.10 | 0.93 | 0.093 |
| **Subtotal** | | | **0.931** |

**Vulnerability Assessment (red-vuln-001):**

| Dimension | Weight | Score | Weighted |
|-----------|--------|-------|----------|
| Completeness | 0.20 | 0.91 | 0.182 |
| Internal Consistency | 0.20 | 0.90 | 0.180 |
| Methodological Rigor | 0.20 | 0.93 | 0.186 |
| Evidence Quality | 0.15 | 0.92 | 0.138 |
| Actionability | 0.15 | 0.92 | 0.138 |
| Traceability | 0.10 | 0.93 | 0.093 |
| **Subtotal** | | | **0.917** |

### Combined Barrier 2 Score

| Component | Weight | Score | Weighted |
|-----------|--------|-------|----------|
| Implementation Report | 0.50 | 0.931 | 0.466 |
| Vulnerability Assessment | 0.50 | 0.917 | 0.459 |
| **Combined Composite** | | | **0.924** |

### Band Classification

| Band | Range | Result |
|------|-------|--------|
| PASS | >= 0.95 | -- |
| **REVISE** | **0.85 - 0.94** | **0.924** |
| REJECTED | < 0.85 | -- |

**Outcome: REVISE**

The combined composite of 0.924 falls in the REVISE band. The gap to threshold is 0.026 (0.95 - 0.924). This is a near-threshold case. The iteration 1 estimate of 0.92-0.94 post-P0/P1 remediation was accurate.

### Score Delta from Iteration 1

| Dimension | Iter 1 | Iter 2 | Delta |
|-----------|--------|--------|-------|
| Completeness | 0.83 | 0.92 | +0.09 |
| Internal Consistency | 0.74 | 0.91 | +0.17 |
| Methodological Rigor | 0.86 | 0.93 | +0.07 |
| Evidence Quality | 0.79 | 0.93 | +0.14 |
| Actionability | 0.87 | 0.93 | +0.06 |
| Traceability | 0.76 | 0.93 | +0.17 |
| **Composite** | **0.812** | **0.924** | **+0.112** |

The largest improvements were in Internal Consistency (+0.17) and Traceability (+0.17), which were the dimensions most affected by the mitigation numbering collisions. Evidence Quality (+0.14) benefited from the function name and status corrections. These align with the iteration 1 estimates.

---

## Prioritized Remediation List

### P0: Required for Pass (Must Fix for >= 0.95)

| ID | Deliverable | Finding | Required Action | Expected Impact |
|----|-------------|---------|-----------------|-----------------|
| REM-I2-P0-001 | IR | UF-023 | Document the case-sensitive negative lookahead vs case-insensitive `_REINJECT_PREFIX_RE` inconsistency in html_comment.py. Add to Known Gaps or integrate into Gap 4 discussion. The current dual-check architecture works but the inconsistency is a latent risk if either check is modified independently. | Consistency +0.01, Methodological Rigor +0.01 |
| REM-I2-P0-002 | IR | UF-025 | Add `SchemaRegistry._schemas` post-freeze accessibility as a Known Gap (or integrate into the mitigation cross-reference noting the RV-005 caveat). The IR should be self-contained in disclosing known security limitations, not reliant on the VA for this disclosure. | Completeness +0.01, Consistency +0.005 |
| REM-I2-P0-003 | IR | UF-026 | Document the write-back path asymmetric symlink detection as a Known Gap. The read path uses `resolve()` + `realpath()` but the write path uses only `resolve()`. This creates a TOCTOU window. | Completeness +0.01, Rigor +0.005 |
| REM-I2-P0-004 | IR | UF-028 | Document the `"---"` structural cue horizontal rule misclassification as a Known Gap in document type detection. This affects the accuracy of the DocumentTypeDetector for files containing horizontal rules. | Completeness +0.005, Rigor +0.005 |
| REM-I2-P0-005 | IR | NF-001 | Reconcile the test count discrepancy: 446-289=157 new tests vs 163 new tests in the test file inventory table. Clarify whether the baseline 289 includes tests from modified files. | Consistency +0.005, Evidence +0.005 |
| REM-I2-P0-006 | IR | UF-040 | Verify the H-10 hook behavior: does it actually block exception clause additions to existing try/except blocks? If it does not, apply the ReaderError fix and update Gap 1. If it does, document the specific hook behavior. This is a methodological rigor item: the gap's root cause attribution must be verified. | Rigor +0.01, Evidence +0.005 |
| REM-I2-P0-007 | IR | UF-034 | Add a note to Gap 6 or a separate gap disclosing that integration tests universally set `JERRY_DISABLE_PATH_CONTAINMENT=1`, meaning no integration test validates path containment in production mode. | Completeness +0.005, Rigor +0.005 |

### P1: Recommended (Strengthens Quality)

| ID | Deliverable | Finding | Recommended Action | Expected Impact |
|----|-------------|---------|-------------------|-----------------|
| REM-I2-P1-001 | IR | UF-029 | Add Phase 4 scheduling commitment or reference a WORKTRACKER entity for WI-022 through WI-025. Even a "planned for next orchestration cycle" statement adds accountability. | Actionability +0.005 |
| REM-I2-P1-002 | IR | UF-031 | Add a note to Gap 3 (Phase 4 deferral) that billion-laughs mitigation testing should include multi-level anchor expansion, not just trivial single-alias tests. | Rigor +0.005 |
| REM-I2-P1-003 | IR | NF-002 | Clarify in Gap 4 that `modify_reinject_directive()` requires a signature change (adding `file_path` parameter), not just a single-line call-site change. The fix is 2-3 lines, not 1. | Evidence +0.005 |
| REM-I2-P1-004 | VA | NF-003 | Reconcile M-03 status: either align with IR (deferred to Phase 4) or clarify that a partial implementation exists (pre-parse alias count) while full M-03 is deferred. | Consistency +0.005 |
| REM-I2-P1-005 | IR | UF-027 | Add the `_is_trusted_path()` root marker extraction bypass to Gap 5 as a secondary attack vector beyond the substring match. | Completeness +0.005 |
| REM-I2-P1-006 | VA | UF-038 | Add implementation guidance for M-05 (regex timeout): recommend the `regex` library with `timeout` parameter or `google-re2` binding. | Actionability +0.005 |

### Score Improvement Estimate

If all P0 items are addressed:

| Dimension | Current | Estimated Post-P0 | Delta |
|-----------|---------|-------------------|-------|
| Completeness | 0.92 | 0.95-0.96 | +0.03-0.04 |
| Internal Consistency | 0.91 | 0.94-0.95 | +0.03-0.04 |
| Methodological Rigor | 0.93 | 0.96-0.97 | +0.03-0.04 |
| Evidence Quality | 0.93 | 0.95-0.96 | +0.02-0.03 |
| Actionability | 0.93 | 0.95-0.96 | +0.02-0.03 |
| Traceability | 0.93 | 0.95-0.96 | +0.02-0.03 |
| **Estimated Composite** | **0.924** | **0.95-0.96** | **+0.026-0.036** |

---

## Next Iteration Guidance

### What Must Change

1. **Address all 7 P0 items.** These are disclosure additions to Known Gaps (REM-I2-P0-001 through P0-004, P0-007), a test count reconciliation (P0-005), and an H-10 hook verification (P0-006). None require code changes.

2. **The gap to 0.95 is 0.026.** The 7 P0 items collectively provide an estimated +0.026-0.036 improvement across all dimensions. Addressing all 7 should bring the composite to the 0.95-0.96 range.

3. **P1 items provide insurance.** If the P0 improvements are at the lower end of estimates (~+0.026), the P1 items provide an additional ~+0.03 buffer to ensure a clear pass.

### Iteration Strategy

- **Iteration 3:** Apply all P0 items. Apply P1 items if time permits. Expected outcome: PASS (0.95-0.96).
- **Iteration 4 (unlikely needed):** If iteration 3 lands at exactly 0.95 or introduces new findings from the added content, a final polish pass.

### What Must NOT Change

The core deliverable quality has improved substantially. The implementation report's 9 Known Gaps demonstrate honest self-assessment. The VA's updated statuses and scope boundary statement demonstrate intellectual rigor. The mitigation numbering cross-reference resolves the primary traceability failure. These improvements should be preserved.

### Risk Assessment

The primary risk for iteration 3 is introducing new inconsistencies through the added content. Each new Known Gap must be internally consistent with the existing gap numbering, the mitigation cross-reference, and the VA findings. Careful cross-checking during the P0 additions will mitigate this risk.

---

<!-- AGENT: adv-scorer | STRATEGY: S-014 (LLM-as-Judge) | DATE: 2026-02-23 -->
<!-- THRESHOLD: 0.95 | RESULT: REVISE | COMPOSITE: 0.924 -->
<!-- IMPLEMENTATION REPORT: 0.931 | VULNERABILITY ASSESSMENT: 0.917 -->
<!-- BAND: REVISE (0.85 - 0.94) | ITERATION: 2 of max 5 -->
<!-- PREVIOUS: 0.812 (REJECTED, Iteration 1) | DELTA: +0.112 -->
<!-- UNIFIED FINDINGS: 42 | RESOLVED: 26 | PARTIALLY: 1 | UNRESOLVED: 15 | NEW: 4 -->
<!-- P0 REMEDIATION: 7 | P1 RECOMMENDED: 6 -->
*S-014 Scorer Report v2.0.0*
*Quality Gate: QG-B2 | Barrier 2 | Iteration 2*
*Combined Composite: 0.924 (REVISE -- below 0.95 threshold, above 0.85)*
*Gap to Pass: 0.026 | Estimated iterations to pass: 1 (iteration 3)*
