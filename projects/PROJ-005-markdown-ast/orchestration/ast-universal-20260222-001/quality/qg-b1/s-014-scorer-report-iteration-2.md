# S-014 LLM-as-Judge Re-Score Report -- QG-B1 Iteration 2

> **Strategy:** S-014 (LLM-as-Judge)
> **Gate:** QG-B1 (Barrier 1)
> **Iteration:** 2 of 5
> **Prior Score:** 0.835 (REJECTED)
> **Criticality:** C4
> **Threshold:** 0.95
> **Date:** 2026-02-22
> **Scorer:** adv-scorer (S-014)
> **Anti-Leniency Statement:** This report actively counteracts scoring leniency. Do NOT give credit for "intending to fix" something -- only for actually fixing it in the deliverable text. When a revision acknowledges a problem but does not fully resolve it, score it the same as if unaddressed. Surface-level fixes that do not address root cause are scored accordingly. Claims about code changes are verified against the actual source code. Scores reflect defects as found in the v2.0.0 deliverables.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Revision Verification](#revision-verification) | Status of each triangulated finding from Iteration 1 |
| [New Issues Introduced by Revision](#new-issues-introduced-by-revision) | Problems created by v2.0.0 revisions |
| [Per-Deliverable Scoring](#per-deliverable-scoring) | D1-D4 dimension-level scores with justification |
| [Overall QG-B1 Composite Score](#overall-qg-b1-composite-score) | Weighted composite and gate decision |
| [Gate Decision](#gate-decision) | PASS / REVISE / REJECTED determination |
| [Remaining Revision Items](#remaining-revision-items) | Items still needed before re-scoring |

---

## Revision Verification

For each of the 10 triangulated findings from Iteration 1, the revised deliverables (v2.0.0) are verified against the actual source code and cross-checked for completeness.

| # | Triangulated Finding | Status | Verification Notes |
|---|---------------------|--------|-------------------|
| T-01 | FrontmatterField mutability | **FIXED (acknowledgment-based)** | All four deliverables now correctly acknowledge that `FrontmatterField` at `frontmatter.py:54` uses `@dataclass` without `frozen=True`. Verified against source code: line 54 still reads `@dataclass` (no `frozen=True`). The deliverables no longer claim immutability holds for this class -- they document it as a P0 prerequisite migration. D2 (ADR) C-05 now explicitly notes the defect. D3 (Trust Boundaries) Zone 4 now distinguishes "existing (not yet frozen)" from "new (frozen by design)". D1 (Threat Model) adds V-05 vulnerability entry. This is a correct resolution: the deliverables cannot change the source code, so acknowledging the defect and prescribing migration is the appropriate architectural response. |
| T-02 | YAML billion-laughs temporal gap | **FIXED** | D1 adds M-20 (post-parse result size verification, `max_yaml_result_bytes` 64KB) and `max_alias_count` (10). DFD-01 updated with step [4] showing post-parse verification. Attack Tree 2 updated to show M-20 closing the temporal gap. D2 adds `max_yaml_result_bytes` and `max_alias_count` to InputBounds (DD-8) with explicit rationale explaining the temporal gap. D3 updates Checkpoint 1 to include post-parse phase. The mitigation chain is now: M-07 (pre-parse input size) + M-20 alias count pre-check + yaml.safe_load() + M-20 (post-parse result size) + M-06 (post-parse depth). This is a comprehensive fix. |
| T-03 | Mutable list in UniversalParseResult | **FIXED** | D2 (ADR) DD-3 `UniversalParseResult` now declares `xml_sections: tuple[XmlSection, ...] | None`, `html_comments: tuple[HtmlCommentBlock, ...] | None`, `reinject_directives: tuple[ReinjectDirective, ...] | None`, `nav_entries: tuple[NavEntry, ...] | None`. All `list` containers changed to `tuple`. D3 (Trust Boundaries) Zone 4 diagram shows `tuple` throughout. DD-3 rationale explicitly explains deep immutability: `result.xml_sections.append(x)` raises `AttributeError`. `parse_errors` is also `tuple[str, ...]`. Verified internally consistent. |
| T-04 | L2-REINJECT trust boundary gap | **FIXED** | D1 adds T-HC-04 and T-HC-07 threat entries, M-22 (`TRUSTED_REINJECT_PATHS` whitelist), and "Governance attacker" to PASTA threat agents. D2 DD-7 adds case-insensitive negative lookahead `(?!(?i)L2-REINJECT:)`. D3 adds governance boundary in Zone 3 with M-22 annotation. D4 adds GOV-001 through GOV-004 governance injection vectors with dedicated L2-REINJECT testing section. Comprehensive cross-deliverable fix. Source code verified: `reinject.py` currently has NO `TRUSTED_REINJECT_PATHS` -- the deliverables correctly prescribe this as a new mitigation to implement (M-22). |
| T-05 | SchemaRegistry mutability | **FIXED** | D2 DD-4 adds `SchemaRegistry` class with `freeze()` method, `RuntimeError` on post-freeze registration, `MappingProxyType` for read-only `schemas` property, and documented registration protocol. D3 Zone 5 shows frozen registry. D1 T-SV-05 threat entry documents the risk. Source code verified: `schema.py:530` still uses a plain `_SCHEMA_REGISTRY` dict -- the deliverables correctly prescribe the `SchemaRegistry` class as the architectural replacement. |
| T-06 | Missing error handling strategy | **FIXED** | D2 adds DD-9 (Error Handling Strategy) with the pattern: all parsers return result objects with `parse_error: str | None`. `UniversalParseResult` aggregates via `parse_errors: tuple[str, ...]`. Callers can distinguish "not invoked" (None result) from "invoked successfully" (result with `parse_error=None`) from "invoked and failed" (result with `parse_error` set). `XmlSectionResult` and `HtmlCommentResult` both include `parse_error` fields. YAML exception types specified (ScannerError, ParserError, ConstructorError). Complete fix. |
| T-07 | Path pattern ordering ambiguity | **FIXED** | D2 DD-2 now explicitly documents: (1) first-match-wins semantics with ordered list, (2) structural cue priority ordering (YAML > blockquote > XML > HTML), (3) collision test suite in Migration Safety section, (4) `STRUCTURAL_CUE_PRIORITY` list with explicit ordering. D1 DFD-04 step [1] states "First-match-wins semantics (ordered list, see DD-2 in ADR)". Comprehensive fix. |
| T-08 | TOCTOU race condition | **FIXED** | D1 adds T-WB-01 threat entry (DREAD 25, MEDIUM) with M-21 mitigation (atomic write via temp file + os.rename). D3 Write-Back Path Diagram updated with [W1] path re-verification, [W3] atomic write, and "On Failure" actions for all controls. D2 Component Diagram shows `ast_commands.py` with "atomic write (M-21)". Source code verified: `ast_commands.py:410` still uses `Path.write_text()` without atomic write -- deliverables correctly prescribe M-21 as a mitigation to implement. |
| T-09 | DREAD sort order and reproducibility | **PARTIAL** | A new "DREAD Scoring Methodology" section adds calibration guidance with anchored 1-10 scales per dimension and a reproducibility statement. This addresses the reproducibility concern. However, the DREAD table sort order has a NEW error: T-WB-01 (Total: 25) appears in row 5 between T-XS-07 (33) and T-HC-07 (30), when it should be positioned with the other 25-score entries around rows 16-17. The table is NOT strictly sorted by descending Total. See [New Issues Introduced by Revision](#new-issues-introduced-by-revision). |
| T-10 | Cross-deliverable XML parser inconsistency | **FIXED** | D4 (Red Team Scope) completely overhauled XmlSectionParser references: (1) description changed from "Tag injection, nested tag bombs, entity expansion" to "Regex-based extraction" with DD-6 reference, (2) removed CWE-91 and CWE-776, (3) reclassified XXE tests as "Architecture Validation Tests" confirming no xml.etree import, (4) added regex-specific vulnerability test table, (5) added explicit note: "No XML parser library is used." D2 and D4 are now consistent on DD-6 regex-only decision. (6) A-03 coverage correctly reclassified from exploitation to architecture validation. Complete cross-deliverable fix. |

### P1/P2 Standalone Item Verification Summary

| # | Item | Status | Notes |
|---|------|--------|-------|
| 11 | PM-001-B1: Migration safety net | **FIXED** | D2 adds Migration Safety section with golden-file test suite, canary mode (`--legacy` flag), and pattern collision test suite. |
| 12 | PM-008-B1: YAML type coercion | **FIXED** | D2 adds DD-10 (YAML Type Normalization) with explicit coercion rules (bool->"true"/"false", int->str, None->"null", list->"a, b"). |
| 13 | CC-003-B1: GitHub Issue parity | **FIXED** | D4 adds GitHub Issue reference in frontmatter and H-32 compliance note in Disclaimer. (Note: D1-D3 are eng artifacts, not worktracker entities, so GitHub Issue parity is primarily a D4 concern.) |
| 14 | FM-002-B1: yaml.safe_load exceptions | **FIXED** | D1 T-YF-04 and M-19 specify exception types (ScannerError, ParserError, ConstructorError). D2 DD-9 shows per-exception handling. |
| 15 | FM-003-B1: YAML duplicate keys | **FIXED** | D1 adds T-YF-09 threat entry and M-23 mitigation. D2 DD-1 adds duplicate key detection constraint. |
| 16 | FM-004-B1: YAML multi-document | **FIXED** | D1 adds T-YF-10 threat entry and M-24 mitigation. D2 DD-1 adds first-pair-only extraction rule. |
| 17 | FM-005-B1: Tag-in-content | **FIXED** | D1 DFD-02 and D2 DD-6 document the limitation with guidance to use backtick code blocks. |
| 18 | FM-007-B1: HTML comment regex | **FIXED** | D1 DFD-03, D2 DD-7, and D3 HTML Comment data flow all specify non-greedy `.*?` instead of `[^>]*`. |
| 19 | SR-005-B1: ATT&CK/CWE taxonomy mixing | **FIXED** | D4 splits `technique_allowlist` into `attack_techniques` (ATT&CK), `weakness_classes` (CWE), and `governance_injection_vectors` (Jerry-Framework), each with `taxonomy` field. |
| 20 | IN-001-B1: Lint rule gaps | **FIXED** | D1 M-04a (AST integration test) and M-04b (CI grep check) added as defense-in-depth alongside M-01 (lint rule). D2 C-04 updated to include all three mechanisms. |
| 21 | SM-001-B1: Mitigation phase assignment | **FIXED** | D1 mitigation table now includes Phase column (all assigned Phase 2 or Phase 3). |
| 22 | SM-002-B1: Parser matrix rationale | **FIXED** | D2 parser invocation matrix now includes "Per-cell rationale notes" section explaining each Y/-/entry. |
| 23 | SM-003-B1: Validation failure behavior | **FIXED** | D3 validation checks V1-V37 now include "On failure" actions (e.g., `-> Error: "File not found" (exit code 2)`). |
| 24 | CC-001-B1/SR-003-B1: H-05 misattribution | **FIXED** | Searched D1 and D2 -- no incorrect H-05 references to yaml.safe_load found. D2 C-04 correctly cites "Threat Model M-01, M-04a, M-04b" instead of H-05. |
| 25 | FM-018-B1: Python regex features | **FIXED** | D1 M-12 now states: "Python's `re` module does not support possessive quantifiers or atomic groups. Use pattern restructuring instead." |
| 26 | PM-007-B1: No performance baseline | **FIXED** | D2 adds "Performance Requirements" section with target latency and memory per operation, plus performance constraints (no O(2^n), memory bounded by InputBounds). |
| 27 | CC-006-B1: H-33 compliance boundary | **FIXED** | D2 adds "H-33 Compliance Strategy" section with boundary definition table showing H-33-mandatory vs H-33-optional operations. |
| 28 | SR-009-B1: Schema registration mechanism | **FIXED** | D2 DD-4 specifies registration protocol: (1) register() at module load, (2) freeze() after all registrations, (3) register() after freeze() raises RuntimeError. |

**Summary:** 27 of 28 items FIXED. 1 item PARTIAL (T-09: reproducibility fixed, but sort order has a new error). Additionally, 1 new issue introduced by revision.

---

## New Issues Introduced by Revision

### N-01: DREAD Table New Sort Order Error (D1)

**Severity:** Minor
**Location:** D1 Threat Model, DREAD Scoring table, row 5

The v2.0.0 DREAD table introduces a NEW sort order error. T-WB-01 (Total: 25, MEDIUM) is positioned in row 5 between T-XS-07 (Total: 33) and T-HC-07 (Total: 30). The intended strict descending sort order should place T-WB-01 at approximately row 16, adjacent to T-XS-08 (25) and T-YF-09 (25).

The original T-09 finding required re-sorting the table strictly by descending Total. The table was re-sorted, but T-WB-01 (a new entry added for the T-08 fix) was inserted in the wrong position -- likely because it was appended to the HIGH band section without verifying its Total score placement.

**Scoring Impact:** Minor. Depresses Internal Consistency by ~0.01 (cosmetic sort error, easily fixable, does not affect the substance of the DREAD analysis).

### N-02: L2-REINJECT Regex Pattern Mismatch (Pre-Existing, Newly Relevant)

**Severity:** Informational (not scored)
**Location:** D1 and D2 references to `_REINJECT_PATTERN` behavior

The deliverables reference `extract_reinject_directives()` and propose enhancements (M-22 trusted path whitelist). However, the actual `_REINJECT_PATTERN` in `reinject.py:46` requires a `tokens=` field: `rank=(\d+),\s*tokens=(\d+),\s*content="..."`. Most L2-REINJECT comments in the actual codebase (e.g., quality-enforcement.md) omit `tokens=` and use only `rank=` and `content=`. This means the regex does NOT match most real directives. This is a pre-existing issue not introduced by the revision, but the deliverables' threat analysis of L2-REINJECT governance bypass should note that the current regex is already incomplete in its matching coverage. This is informational and not scored as a revision defect.

---

## Per-Deliverable Scoring

### D1: eng-architect-001-threat-model.md (v2.0.0)

| Dimension | Weight | Iter 1 Score | Iter 2 Score | Delta | Justification |
|-----------|--------|-------------|-------------|-------|---------------|
| Completeness | 0.20 | 0.82 | 0.93 | +0.11 | All major gaps closed: T-02 temporal gap addressed with M-20 and alias counting; T-04 L2-REINJECT threats added (T-HC-04, T-HC-07, M-22); T-08 TOCTOU added (T-WB-01, M-21); Threats Not Modeled section added (SM-007-B1); DREAD Scoring Methodology section added; YAML duplicate key (T-YF-09, M-23), multi-document (T-YF-10, M-24), tag-in-content (DFD-02), HTML regex fix (DFD-03) all addressed; defense-in-depth for yaml.safe_load now includes lint rule + AST test + CI grep (3 independent mechanisms); Phase column added to mitigation table. Remaining gap: migration impact for 500+ existing files is mentioned in Threats Not Modeled but not modeled as an operational risk. |
| Internal Consistency | 0.20 | 0.83 | 0.92 | +0.09 | T-01 FrontmatterField correctly acknowledged as pre-existing defect throughout (V-05, System Context, Key Findings #4). H-05 misattribution removed. T-XS-07 residual risk now correctly stated as "Negligible" for regex architecture. ReDoS mitigation M-12 now uses Python-specific guidance. DREAD table has one new sort order error (N-01: T-WB-01 at position 5 should be at position ~16). This prevents a higher score. Threat-to-mitigation cross-references are internally consistent. New mitigations (M-20 through M-24) are correctly referenced in STRIDE, DREAD, Attack Trees, and PASTA sections. |
| Methodological Rigor | 0.20 | 0.85 | 0.94 | +0.09 | Four methodologies applied systematically. T-02 mitigation chain now has three independent controls (M-07 + M-20 alias + M-20 result size). T-04 modeled with STRIDE entries, DREAD scores, and PASTA threat agents. DREAD scoring methodology section provides reproducibility (calibration anchors per dimension, context-specific scale). Attack Tree 2 updated with M-20. Defense-in-depth for yaml.safe_load is exemplary (3 independent mechanisms: lint, AST test, CI grep). M-12 ReDoS guidance now Python-appropriate. |
| Evidence Quality | 0.15 | 0.82 | 0.92 | +0.10 | DREAD calibration anchors provide reproducible scoring methodology. YAML expansion ratio now implicitly bounded: 32KB input -> max 64KB output (M-20). Exception types specified for yaml error handling (ScannerError, ParserError, ConstructorError). NIST CSF mapping expanded to cover M-20 through M-24. Code line references maintained (V-01 through V-12). "No performance impact" claim removed (now deferred to ADR Performance Requirements section). |
| Actionability | 0.15 | 0.88 | 0.95 | +0.07 | 24 mitigations (M-01 through M-24, up from 19) with priorities, Phase assignments, and implementation guidance. M-20 has concrete implementation: `if len(json.dumps(result)) > bounds.max_yaml_result_bytes: return error`. M-21 has concrete implementation: temp file + os.rename. M-22 specifies trusted path list and case-insensitive matching. M-23 specifies pre-parse scan for duplicate keys. M-24 specifies first-pair-only extraction. Each mitigation now has a Phase column enabling sequencing. |
| Traceability | 0.10 | 0.82 | 0.93 | +0.11 | All new threats trace to mitigations (T-HC-04->M-22, T-WB-01->M-21, T-YF-09->M-23, T-YF-10->M-24). New mitigations trace to NIST CSF subcategories. V-05 through V-12 vulnerability entries trace to specific threats. Attack catalog A-01 through A-11 (expanded from A-10) trace to mitigations. Cross-reference to red team scope attack catalog now possible via A-XX IDs. Revision history documents all changes with P0/P1/P2 priority labels and finding IDs. |

**D1 Weighted Score:**
```
(0.93 * 0.20) + (0.92 * 0.20) + (0.94 * 0.20) + (0.92 * 0.15) + (0.95 * 0.15) + (0.93 * 0.10)
= 0.186 + 0.184 + 0.188 + 0.138 + 0.1425 + 0.093
= 0.932
```

**D1 Score: 0.932 -- REVISE** (below 0.95 user threshold, above 0.92 standard threshold)

---

### D2: eng-architect-001-architecture-adr.md (v2.0.0)

| Dimension | Weight | Iter 1 Score | Iter 2 Score | Delta | Justification |
|-----------|--------|-------------|-------------|-------|---------------|
| Completeness | 0.20 | 0.78 | 0.94 | +0.16 | Major gaps closed: DD-9 (Error Handling Strategy), DD-10 (YAML Type Normalization), Performance Requirements section, Migration Safety section (golden-file tests, canary mode, --legacy flag), H-33 Compliance Strategy section. InputBounds extended with `max_yaml_result_bytes` and `max_alias_count` (M-20). SchemaRegistry with freeze() method (DD-4). Registration protocol documented. FrontmatterField defect acknowledged with P0 migration task. All `list` containers changed to `tuple` in UniversalParseResult. 10 design decisions now cover the complete architecture. Parser invocation matrix has per-cell rationale. |
| Internal Consistency | 0.20 | 0.76 | 0.94 | +0.18 | T-01: C-05 now explicitly documents the FrontmatterField defect and prescribes migration -- no longer claims immutability that does not exist. T-03: All container fields in UniversalParseResult use `tuple`, consistent with YamlFrontmatterResult's `fields: tuple[...]` pattern. T-05: SchemaRegistry has freeze() + MappingProxyType, consistent with immutability pattern. T-10: DD-6 consistently referenced as regex-only throughout ADR and red team scope. DD-9 error handling pattern consistently applied across all three parser classes. InputBounds.DEFAULT consistently referenced as the default value. Internal cross-references (DD-1 through DD-10, C-01 through C-07, M-XX references) are all consistent. No internal contradictions found. |
| Methodological Rigor | 0.20 | 0.84 | 0.94 | +0.10 | Systematic alternatives-considered for all 10 design decisions. Defense-in-depth for yaml.safe_load elevated to triple enforcement (M-01 lint + M-04a AST test + M-04b CI grep). M-20 temporal gap analysis demonstrates principled reasoning about when controls execute relative to parser operations. SchemaRegistry freeze() addresses the registry poisoning threat with a concrete mechanism (not just "should be immutable"). Pattern collision test suite demonstrates testing methodology awareness. Performance Requirements section establishes verifiable baselines. Migration Safety section demonstrates backward-compatibility discipline. |
| Evidence Quality | 0.15 | 0.85 | 0.93 | +0.08 | Code examples for all 10 design decisions (class definitions, regex patterns, configuration). InputBounds defaults reference specific threat model mitigation IDs (M-XX). Performance targets include specific latency and memory values with justification. Type normalization rules provide explicit input-to-output mappings. H-07 and H-10 compliance tables with per-file verification. "No performance impact" claim replaced with bounded performance requirements. `max_yaml_result_bytes` (64KB) and `max_alias_count` (10) provide quantitative bounds. Remaining gap: no actual benchmark data (targets are estimates, not measurements -- appropriate for a proposed architecture). |
| Actionability | 0.15 | 0.80 | 0.94 | +0.14 | DD-9 error handling strategy provides implementable pattern (try/except per exception type, result objects with error fields, aggregation). DD-10 type normalization provides explicit coercion rules. Migration Safety provides concrete test strategy (golden-file suite, canary mode with --legacy flag, collision test). SchemaRegistry registration protocol is step-by-step (1. register, 2. freeze, 3. post-freeze raises). Performance Requirements provide verifiable targets. H-33 compliance boundary is clear (which operations are mandatory vs optional). All parser classes have complete constraint lists with M-XX references. |
| Traceability | 0.10 | 0.85 | 0.93 | +0.08 | References table expanded. Constraint table C-01 through C-07 traces to HARD rules and threat model mitigations. DD-1 through DD-10 each reference the motivating requirements. Revision history documents all changes with P0/P1/P2 priority and finding IDs (T-XX, FM-XXX, PM-XXX, etc.). Parser invocation matrix includes rationale notes. H-33 boundary table links to HARD rule references. Performance requirements link to InputBounds and mitigation IDs. Cross-references to threat model and trust boundaries maintained. |

**D2 Weighted Score:**
```
(0.94 * 0.20) + (0.94 * 0.20) + (0.94 * 0.20) + (0.93 * 0.15) + (0.94 * 0.15) + (0.93 * 0.10)
= 0.188 + 0.188 + 0.188 + 0.1395 + 0.141 + 0.093
= 0.938
```

**D2 Score: 0.938 -- REVISE** (below 0.95 user threshold, above 0.92 standard threshold)

---

### D3: eng-architect-001-trust-boundaries.md (v2.0.0)

| Dimension | Weight | Iter 1 Score | Iter 2 Score | Delta | Justification |
|-----------|--------|-------------|-------------|-------|---------------|
| Completeness | 0.20 | 0.83 | 0.95 | +0.12 | All major gaps closed: T-08 TOCTOU mitigation fully specified in Write-Back Path Diagram (M-21 atomic write with temp file + os.rename); L2-REINJECT governance boundary added to Zone 3 (M-22 trusted paths, case-insensitive exclusion); YAML data flow updated with M-20 post-parse verification, alias count check, duplicate key detection, first-pair-only rule, type normalization; V1 through V37 validation checks now include "On Failure" actions; Zone 4 extended with parse_errors aggregation and runtime type annotation note; XmlSectionResult and HtmlCommentResult wrapper types added to data flows. |
| Internal Consistency | 0.20 | 0.80 | 0.94 | +0.14 | T-01: Zone 4 now correctly distinguishes "existing (not yet frozen)" FrontmatterField from "new (frozen by design)" objects with explicit EXCEPTION callout. P0 migration note and IMMUTABILITY NOTE block prevent false claims. T-03: All containers in Zone 4 diagram show `tuple`. Zone count corrected to "six" throughout (was inconsistent). V26 checkpoint correctly states "Frozen dataclass construction" with caveat about FrontmatterField. V28 correctly states "Type annotations satisfied (enforced by construction discipline, NOT runtime)." Checkpoint 2 no longer overclaims language-level type enforcement. Threat overlay consistent with threat model (T-HC-04, T-HC-07, T-WB-01, T-SV-05 all present). |
| Methodological Rigor | 0.20 | 0.88 | 0.95 | +0.07 | Three-checkpoint defense-in-depth architecture clearly articulated with Checkpoint 1 now including post-parse phase (closing temporal gap). Checkpoint 2 distinguishes attribute immutability (frozen=True) from container immutability (tuple) and notes the known exception. Write-back path analysis includes 5 controls (W1-W5) with on-failure actions. Governance boundary analysis in L2 Strategic Implications demonstrates security architecture reasoning about trust-level distinctions within zones. Recommendation section prioritizes parser testing (Zone 3 concentration of attack surface). Per-parser data flow diagrams are systematic and complete. |
| Evidence Quality | 0.15 | 0.85 | 0.93 | +0.08 | ASCII diagrams are clear, well-labeled, and internally consistent. All validation checks (V1-V37) reference specific mitigation IDs. Per-parser data flows show concrete control points with specific bounds values (32KB, 64KB, 100 keys, depth 5, etc.). Zone 4 diagram shows actual field types and container types. Threat overlay maps threats to specific mitigations and boundary crossings. "On Failure" actions are concrete (exit codes, error messages, specific behaviors like "silently ignored" vs "parse_error set"). Runtime type annotation note is factually correct (Python dataclasses do not enforce types at runtime). |
| Actionability | 0.15 | 0.85 | 0.94 | +0.09 | V1-V37 are implementable with "On Failure" column providing concrete responses (exit codes, error messages, specific behaviors). Write-back controls W1-W5 have specific implementation: W3 specifies `path.with_suffix('.tmp')` + `os.rename()`. Per-parser data flows provide step-by-step implementation guidance. Checkpoint descriptions tell implementers exactly what to verify at each boundary. Governance boundary implementation is actionable: file-origin trust check with specific trusted paths. Zone 4 qualification note tells implementers the P0 prerequisite for full Zone 4 trust designation. |
| Traceability | 0.10 | 0.82 | 0.93 | +0.11 | V1-V37 reference mitigations (M-XX). Threat overlay maps threat IDs to zones and mitigations. Boundary crossings BC-01 through BC-05 are enumerated and cross-referenced. Zone 4 references ADR C-05 and scorer T-01. Write-back path references M-08 and M-21. Governance boundary references M-22. Revision history documents all changes with finding IDs (T-01 through T-08, SM-003-B1, FM-007-B1). Checkpoint descriptions reference specific mitigation IDs. |

**D3 Weighted Score:**
```
(0.95 * 0.20) + (0.94 * 0.20) + (0.95 * 0.20) + (0.93 * 0.15) + (0.94 * 0.15) + (0.93 * 0.10)
= 0.190 + 0.188 + 0.190 + 0.1395 + 0.141 + 0.093
= 0.942
```

**D3 Score: 0.942 -- REVISE** (below 0.95 user threshold, above 0.92 standard threshold)

---

### D4: red-lead-001-scope.md (v2.0.0)

| Dimension | Weight | Iter 1 Score | Iter 2 Score | Delta | Justification |
|-----------|--------|-------------|-------------|-------|---------------|
| Completeness | 0.20 | 0.88 | 0.96 | +0.08 | L2-REINJECT governance testing section added with 6 test cases (directive injection, case-variant bypass, whitespace bypass, file-origin trust, rank manipulation, content payload injection). GOV-001 through GOV-004 vectors added to technique_allowlist. Zone 4 authorized target (L2ReinjectEnforcement) added. Architecture validation tests for DD-6 compliance (5 test cases: no xml.etree import, no lxml, no defusedxml, no entity expansion, no DTD recursion). Regex-specific vulnerability tests (9 test cases). Threat Model Cross-Reference section maps all A-01 through A-10. DD-6 architecture validation, governance vector coverage, and ATT&CK technique coverage added to success criteria. GitHub Issue parity addressed. |
| Internal Consistency | 0.20 | 0.80 | 0.95 | +0.15 | T-10 fully resolved: all XmlSectionParser references now describe regex-based extraction per DD-6. CWE-91 and CWE-776 removed. XXE tests reclassified as architecture validation. No cross-deliverable contradictions with ADR DD-6. ATT&CK and CWE taxonomies cleanly separated with `taxonomy` field on each entry. Jerry-Framework governance vectors in their own section. CWE-79 (XSS) removed (CLI has no browser context) -- correct. HtmlCommentMetadata "Embedded scripts" severity correctly reduced to "Low (Content Integrity)". All test tables include Threat Model Ref column linking to threat IDs and attack catalog entries. Component descriptions match ADR design decisions. |
| Methodological Rigor | 0.20 | 0.88 | 0.95 | +0.07 | PTES + OSSTMM methodology with explicit stage mapping. Agent team composition follows principle of least privilege with justified exclusions. Testing approach systematically covers each component with CWE-focused test tables. Threat Model Cross-Reference provides structured mapping from attack catalog to test coverage, demonstrating no coverage gaps. Architecture validation tests (DD-6 compliance) demonstrate architectural verification methodology. Governance injection testing demonstrates awareness of framework-specific threat landscape. Success criteria include quantitative thresholds and are aligned with quality gate handoff requirements. |
| Evidence Quality | 0.15 | 0.85 | 0.94 | +0.09 | Code line references maintained for known risk areas. Test cases have specific expected behaviors and severity ratings. Threat Model Ref column provides traceability evidence. Architecture validation tests specify concrete static analysis commands (`grep -r "import xml" src/`). CVSS v3.1 referenced for scoring. All test cases have expected behavior and severity assessment. CWE classifications are correct and appropriate for the CLI context. Governance injection test cases reference specific threat model IDs (T-04, GOV-001 through GOV-004). |
| Actionability | 0.15 | 0.90 | 0.96 | +0.06 | Per-component test tables with specific test cases, expected behavior, severity, and threat model references. Architecture validation tests are executable (static analysis grep commands). L2-REINJECT governance tests are specific and implementable. Agent team composition with clear phase sequencing and RoE constraints. Evidence handling with naming convention and retention policy. Success criteria with quantitative thresholds. Bash tool scope constraint provides clear boundaries for red-vuln and red-exploit agents. GitHub Issue creation requirement is specific and actionable (title, body content specified). |
| Traceability | 0.10 | 0.80 | 0.95 | +0.15 | Threat Model Cross-Reference section provides complete mapping of A-01 through A-10 to test categories. All test tables include Threat Model Ref column. Technique allowlist entries have taxonomy labels. GOV-001 through GOV-004 reference T-04 triangulated finding. Success criteria reference DD-6, governance vectors, ATT&CK coverage, and CWE coverage separately. Quality gate handoff requirements include DREAD score alignment and threat model cross-reference. Revision history documents all changes with finding IDs and priority labels. GitHub Issue reference in frontmatter provides external traceability. |

**D4 Weighted Score:**
```
(0.96 * 0.20) + (0.95 * 0.20) + (0.95 * 0.20) + (0.94 * 0.15) + (0.96 * 0.15) + (0.95 * 0.10)
= 0.192 + 0.190 + 0.190 + 0.141 + 0.144 + 0.095
= 0.952
```

**D4 Score: 0.952 -- PASS** (above 0.95 user threshold)

---

## Overall QG-B1 Composite Score

### Per-Deliverable Summary

| Deliverable | Iter 1 | Iter 2 | Delta | Band |
|-------------|--------|--------|-------|------|
| D1: Threat Model | 0.837 | 0.932 | +0.095 | REVISE |
| D2: Architecture ADR | 0.808 | 0.938 | +0.130 | REVISE |
| D3: Trust Boundaries | 0.839 | 0.942 | +0.103 | REVISE |
| D4: Red Team Scope | 0.855 | 0.952 | +0.097 | **PASS** |
| **Average** | **0.835** | **0.941** | **+0.106** | **REVISE** |

### Per-Dimension Aggregate (Average across D1-D4)

| Dimension | Weight | D1 | D2 | D3 | D4 | Avg | Iter 1 Avg | Delta |
|-----------|--------|------|------|------|------|------|------------|-------|
| Completeness | 0.20 | 0.93 | 0.94 | 0.95 | 0.96 | 0.945 | 0.828 | +0.117 |
| Internal Consistency | 0.20 | 0.92 | 0.94 | 0.94 | 0.95 | 0.938 | 0.798 | +0.140 |
| Methodological Rigor | 0.20 | 0.94 | 0.94 | 0.95 | 0.95 | 0.945 | 0.863 | +0.082 |
| Evidence Quality | 0.15 | 0.92 | 0.93 | 0.93 | 0.94 | 0.930 | 0.843 | +0.087 |
| Actionability | 0.15 | 0.95 | 0.94 | 0.94 | 0.96 | 0.948 | 0.858 | +0.090 |
| Traceability | 0.10 | 0.93 | 0.93 | 0.93 | 0.95 | 0.935 | 0.823 | +0.112 |

### QG-B1 Composite Score

```
Composite = (0.945 * 0.20) + (0.938 * 0.20) + (0.945 * 0.20) + (0.930 * 0.15) + (0.948 * 0.15) + (0.935 * 0.10)
          = 0.1890 + 0.1876 + 0.1890 + 0.1395 + 0.1422 + 0.0935
          = 0.941
```

**QG-B1 Composite Score: 0.941**

---

## Gate Decision

| Criterion | Value | Assessment |
|-----------|-------|------------|
| Composite Score | 0.941 | Above 0.92 standard threshold (H-13 PASS) |
| Threshold (user-specified) | 0.95 | Gap: -0.009 |
| Standard threshold (H-13) | 0.92 | Exceeded by +0.021 |
| Per-deliverable results | 1 PASS (D4), 3 REVISE (D1-D3) | D4 passes user threshold |
| Score delta from Iter 1 | +0.106 | Substantial improvement |
| Items addressed | 27 of 28 FIXED, 1 PARTIAL | Near-complete revision |
| New issues introduced | 1 (N-01: minor sort error) | Minimal regression |

### Decision: **REVISE**

**Rationale:** The QG-B1 composite score of 0.941 exceeds the standard H-13 threshold of 0.92 (PASS by standard), but falls 0.009 below the user-specified 0.95 threshold. Since the user specified 0.95, the gate decision is REVISE per H-13 (below user threshold).

The revisions demonstrate substantial quality improvement across all six dimensions:
- **Internal Consistency** improved the most (+0.140), driven by resolution of the FrontmatterField mutability contradiction (T-01), mutable list correction (T-03), and XML parser cross-deliverable inconsistency (T-10).
- **Completeness** improved +0.117, driven by new sections (DD-9, DD-10, Migration Safety, Performance Requirements, H-33 Compliance, L2-REINJECT governance testing).
- **All dimensions now score above 0.92** across all deliverables.

D4 (Red Team Scope) passes the 0.95 threshold at 0.952. D1-D3 are in the 0.932-0.942 range, each within reach of 0.95 with targeted fixes.

**Estimated gap to PASS (0.95):** Closing the remaining items below would add approximately +0.01-0.02 to the composite, sufficient to cross 0.95.

---

## Remaining Revision Items

Only items that are NOT yet fixed. Do NOT repeat already-fixed items.

### P1: Required for 0.95

| # | Finding | Deliverable | Required Action | Expected Impact |
|---|---------|-------------|-----------------|-----------------|
| 1 | N-01: DREAD table sort error | D1 | Move T-WB-01 (Total: 25) from row 5 to its correct position near row 16 (between T-XS-08 and T-YF-09, both Total: 25). Verify the entire table is strictly sorted by descending Total with no exceptions. | D1 Internal Consistency +0.01 |
| 2 | D1 Evidence Quality gap | D1 | Add a brief note in the DREAD Scoring Methodology section stating that the calibration anchors were established for initial threat model authoring and should be refined with team calibration exercises when additional threat assessors participate. This addresses the single-assessor reproducibility limitation. | D1 Evidence Quality +0.005 |
| 3 | D2 Evidence Quality gap | D2 | In Performance Requirements, note that target latencies are estimates based on algorithmic complexity analysis, not measured benchmarks. Add: "Phase 3 testing will validate these targets; deviations exceeding 2x will trigger performance investigation." | D2 Evidence Quality +0.005 |
| 4 | D3 Completeness gap | D3 | Add a brief note to the Zone 4 IMMUTABILITY NOTE block: "`BlockquoteFrontmatter` stores fields in a mutable `list[FrontmatterField]` (see `frontmatter.py:131`). The P0 migration to `frozen=True` on `FrontmatterField` addresses attribute mutability but does not address the mutable `_fields` list container. A separate migration to `tuple` for the internal `_fields` storage is recommended." This is a more precise characterization of the pre-existing defect. | D3 Internal Consistency +0.005, Completeness +0.005 |

### P2: Helpful but not strictly required

| # | Finding | Deliverable | Required Action | Expected Impact |
|---|---------|-------------|-----------------|-----------------|
| 5 | Cross-reference gap | D1, D4 | D1 attack catalog now goes to A-11 (including A-11 for symlink TOCTOU). D4 Threat Model Cross-Reference covers A-01 through A-10. Add A-11 to D4's cross-reference table for completeness. | D4 Traceability +0.005 |
| 6 | L2-REINJECT regex coverage note | D1 | In the L2-REINJECT section or M-22, add an informational note that the current `_REINJECT_PATTERN` regex in `reinject.py` requires a `tokens=` field, but many production L2-REINJECT directives omit it. The M-22 enhancement should consider updating the regex to make `tokens=` optional. | D1 Evidence Quality +0.005 |

**Estimated post-revision score:** If all P1 items are addressed: ~0.948-0.953. If P1 + P2 items are addressed: ~0.950-0.955. The deliverables are within reach of the 0.95 threshold with a focused Iteration 3.

---

### Scoring Methodology Notes

1. **Anti-leniency applied consistently.** T-01 (FrontmatterField mutability) was scored as FIXED because the deliverables correctly acknowledge the defect and prescribe migration -- they cannot and should not change source code. The resolution is architecturally appropriate: document the known defect, prescribe the fix, qualify all immutability claims with the exception. This is scored the same as if the code had been changed, because the deliverables' job is to define architecture, not implement it.

2. **New issue N-01 scored proportionally.** The DREAD table sort error is a cosmetic issue that does not affect the substance of the risk analysis. It depresses Internal Consistency by ~0.01 (one row misplaced out of 37). This is less severe than the original T-09 finding because the scoring methodology section has been added (the original finding combined sort order AND reproducibility; reproducibility is now fixed).

3. **D2 (ADR) showed the largest improvement** (+0.130), consistent with it having the most revision items (it was the architectural specification with the most cascading defects in Iteration 1). The addition of DD-9, DD-10, Migration Safety, Performance Requirements, and H-33 Compliance Strategy represents substantial new content that was missing in v1.0.0.

4. **D4 (Red Team Scope) is the only deliverable to PASS the 0.95 threshold.** Its improvement was driven primarily by resolving T-10 (XML parser inconsistency) and adding L2-REINJECT governance testing. The comprehensive Threat Model Cross-Reference section and taxonomy separation in technique_allowlist pushed Traceability from 0.80 to 0.95 (+0.15).

5. **The 0.941 composite represents genuine quality improvement**, not score inflation. 27 of 28 items are verified as FIXED against source code and cross-deliverable consistency checks. The improvement is earned.

---

<!-- VERSION: 2.0.0 | DATE: 2026-02-22 | STRATEGY: S-014 | GATE: QG-B1 | ITERATION: 2 | AGENT: adv-scorer | CRITICALITY: C4 | THRESHOLD: 0.95 -->
