# S-003 Steelman Technique: QG-B2 Findings

<!-- ADV-EXECUTOR-001 | STRATEGY: S-003 Steelman | DATE: 2026-02-23 | QG: QG-B2 -->
<!-- ENGAGEMENT: ast-universal-20260222-001 | CRITICALITY: C4 -->

## Document Sections

| Section | Purpose |
|---------|---------|
| [Overview](#overview) | Strategy context, scope, scoring approach |
| [Steelman: Implementation Report](#steelman-implementation-report) | Strongest arguments for eng-backend-001 deliverable decisions |
| [Steelman: Vulnerability Assessment](#steelman-vulnerability-assessment) | Strongest arguments for red-vuln-001 deliverable decisions |
| [Steelman: Source Code Decisions](#steelman-source-code-decisions) | Strongest arguments for key implementation choices in source files |
| [Per-Dimension Preliminary Scores](#per-dimension-preliminary-scores) | Dimension-level preliminary scoring with rationale |
| [Areas Needing Reinforcement](#areas-needing-reinforcement) | Where claims are well-supported vs. where they need strengthening |
| [Composite Score](#composite-score) | Weighted preliminary composite |

---

## Overview

**Strategy:** S-003 Steelman Technique -- strengthen arguments and approaches taken before critique, identifying the strongest possible interpretation of each decision.

**Scope:**
1. Implementation Report (`eng-backend-001-implementation-report.md`)
2. Vulnerability Assessment (`red-vuln-001-vulnerability-assessment.md`)
3. Key source files: `yaml_frontmatter.py`, `xml_section.py`, `html_comment.py`, `document_type.py`, `universal_document.py`, `schema_registry.py`

**Steelman posture:** For each major decision, the strongest defensible rationale is articulated in full before any critique is raised. Areas where evidence is thin or missing are flagged under [Areas Needing Reinforcement](#areas-needing-reinforcement).

---

## Steelman: Implementation Report

### Decision 1: Zero New Dependencies

**Claim:** The implementation added zero new third-party dependencies.

**Steelman argument:** This is architecturally the strongest possible outcome for a parser expansion of this scope. Introducing new dependencies creates transitive supply chain risk, version pin fragility, and import latency. By reusing PyYAML (which was already present and validated), the implementation avoids the most common source of supply chain vulnerabilities. PyYAML's `safe_load()` is a known quantity: battle-tested in millions of deployments, well-documented security posture, and audited specifically for safe deserialization. A fresh YAML library (e.g., `strictyaml`, `ruamel.yaml`) would introduce an unaudited surface. The existing stack was sufficient for all seven required enhancements -- this is not a constraint-imposed omission but a positive engineering choice that reduces attack surface.

**Evidence quality:** Directly verifiable from `pyproject.toml` (no changes to deps section) and the implementation report's explicit statement. High confidence.

---

### Decision 2: Polymorphic Parser Pattern with Parser Invocation Matrix

**Claim:** Each format has its own parser class; the `UniversalDocument` facade selects parsers via `_PARSER_MATRIX`.

**Steelman argument:** The polymorphic approach is superior to a monolithic parser for exactly the security-relevant reasons that matter in this system. A monolithic parser would process all input through a single code path, meaning a failure mode in YAML parsing could influence XML section parsing state. By isolating parsers, the blast radius of any single parser's failure is bounded: a malformed YAML block produces a `YamlFrontmatterResult` with `parse_error` set, but `XmlSectionParser` and `HtmlCommentMetadata` continue to operate independently on the same document. The `_PARSER_MATRIX` approach makes parser selection a configuration concern, not a logic concern -- it is directly readable and auditable as a data structure rather than a conditional tree. Adding a new document type requires exactly three touchpoints (new parser file, matrix entry, result field) with no changes to existing parsers. This open-closed property is the hallmark of a well-designed extension point.

**Evidence quality:** Confirmed directly in source code (`universal_document.py` lines 96-108). The matrix is visible, auditable, and tested (23 unit tests in `test_universal_document.py`). High confidence.

---

### Decision 3: 98% Domain Coverage with 21/21 Work Items Complete

**Claim:** All 21 work items are complete; domain module coverage is 98% (879 statements, 20 missed).

**Steelman argument:** 98% coverage on a new security-sensitive parser module is a rigorous result that exceeds industry standard practice. The 20 missed statements are fully enumerated and categorized in the report -- they are not unknown gaps but documented, analyzed misses with explicit remediation paths. The three categories of misses (rare type-detection branches, pre-existing reinject.py paths, multi-parser error aggregation combinations) are exactly the types of paths that require adversarial or integration testing to exercise -- they are not reachable via normal unit test parametrization. The report correctly defers these to Phase 4 adversarial testing (WI-022 through WI-025) rather than attempting to manufacture artificial test inputs at the unit level, which would test the test harness rather than real behavior. The pre-implementation baseline of 289 passing tests growing to 4,870 in the full suite (adding 157 new markdown_ast unit tests and 18 integration tests) demonstrates thorough test-first development discipline per H-20.

**Evidence quality:** Coverage numbers are verifiable by running `uv run pytest`. Work item evidence is specific to file and line number. High confidence.

---

### Decision 4: Gap Transparency (yaml.reader.ReaderError and H-10 Constraint)

**Claim:** The report documents a known gap (yaml.reader.ReaderError not caught) and its root cause (H-10 multi-class enforcement).

**Steelman argument:** This is the report's most intellectually honest element. Rather than silently accepting the gap or misrepresenting it as a design decision, the report names the constraint (H-10 one-class-per-file enforcement blocking edits to `yaml_frontmatter.py`), assesses the impact as LOW with explicit reasoning (the `_strip_control_chars()` M-18 mitigation prevents the most common triggering inputs), provides both remediation paths (file split or exception handler addition), and notes that the `_strip_control_chars()` function is tested independently. A report that presents a perfect implementation is more suspicious than one that enumerates its known edges with honest impact assessment. This gap disclosure strengthens rather than weakens the report's credibility.

**Evidence quality:** Directly verified in source: `yaml_frontmatter.py` exception handlers cover `ScannerError`, `ParserError`, `ConstructorError` but not `yaml.reader.ReaderError`. The H-10 constraint is verified by the pre-tool-use hook behavior described. High confidence.

---

### Decision 5: HARD Rule Compliance Documentation

**Claim:** All seven applicable HARD rules are explicitly verified with specific evidence.

**Steelman argument:** The compliance matrix is not a checkbox exercise. Each entry cites a specific mechanism: H-07 compliance cites "no domain-to-interface imports"; H-10 compliance acknowledges the grandfathered multi-class files but explains the pre-tool enforcement behavior that prevents inadvertent violations; H-20 compliance cites 98% coverage. This specificity means the compliance claims are falsifiable -- each one can be independently verified by inspecting the named file or running the named test. A compliance matrix that says "compliant" without evidence is worthless; this one provides auditable evidence for each rule. The CI workflow addition (WI-021 -- grep check for banned YAML APIs) moves compliance verification from a runtime assertion to a structural gate, which is the strongest possible enforcement form.

**Evidence quality:** Each compliance row is independently verifiable. CI workflow grep check is visible in the named `.github/workflows/ci.yml` lines. High confidence.

---

## Steelman: Vulnerability Assessment

### Decision 6: 27 Findings with DREAD Calibration and Self-Disagreement

**Claim:** The assessment produced 27 findings and explicitly challenges 6 of the architect's DREAD scores, including adjusting one score downward (RV-020, -2 from T-XS-07).

**Steelman argument:** A vulnerability assessment that only escalates scores relative to the architect's baseline is subject to systematic inflation bias -- every finding becomes "worse than thought." The red-vuln-001 assessor's willingness to downgrade T-XS-07 by 2 points (reasoning that the lazy quantifier `.*?` is materially less prone to catastrophic backtracking than nested quantifiers) demonstrates genuine technical calibration rather than adversarial posturing. The 6 upward challenges are individually justified with specific technical reasoning: the YAML deserialization Damage score being raised to 10 (from 9) is correct because arbitrary code execution is definitionally maximum damage on the DREAD scale. The L2-REINJECT governance injection being raised from 27 to 33 is well-justified because the original score of 5 for Damage does not account for the meta-security nature of the target -- it is not "information tampering" (STRIDE-T) but tampering with the enforcement mechanism for all 25 HARD rules, a qualitatively different impact class.

**Evidence quality:** All DREAD challenges are documented in Appendix A with specific per-dimension reasoning. The downgrade for RV-020 demonstrates calibration integrity. High confidence.

---

### Decision 7: Separating Existing Code Findings from Planned Code Findings

**Claim:** The assessment distinguishes L1-A (existing code) from L1-B (planned code) findings.

**Steelman argument:** This structural separation is the architecturally correct approach for a pre-implementation red team assessment. Treating planned-code findings with the same weight as existing-code findings without distinguishing them would either inflate the apparent current risk (by presenting planned risks as present) or deflate planned risks (by burying them in the existing-code section). By separating them, the assessment enables the engineering team to: (a) act immediately on existing code findings (RV-003 through RV-018 require no implementation to address), (b) use the planned code findings as implementation requirements for WI-005 through WI-011, and (c) track mitigation status accurately by phase. The confidence calibration (0.92 for existing code vs. 0.85 for planned code) is appropriately differentiated -- planned code analysis is inherently more speculative and the assessment correctly represents this uncertainty.

**Evidence quality:** The distinction is maintained consistently throughout the report. Confidence scores are differentiated. The implementation priority table maps findings to phases. High confidence.

---

### Decision 8: Three Insufficiently-Specified Mitigations Called Out Explicitly

**Claim:** Three mitigations (M-03, M-05, M-12) are assessed as "insufficient as specified" even though they are the architect's own mitigations.

**Steelman argument:** Calling out the architect's own mitigations as insufficient is the adversarial posture this assessment is designed to perform. The three insufficiency findings are technically specific and actionable:
- M-03 (YAML anchor depth limit): PyYAML's `safe_load()` genuinely does not natively support depth limiting. The assessment is correct that implementation guidance is missing and that a custom SafeLoader subclass or pre-parse scan would be required.
- M-05 (regex timeout): Python's `re` module genuinely has no timeout parameter. The assessment is correct that the mitigation requires a library choice (`regex` or `re2`) that is not specified.
- M-12 (file-origin trust): "Path-based trust boundary" without an explicit allowed-directory list is an incomplete specification. The assessment is correct that the mitigation is architectural intention without operational definition.

These three are exactly the gap category that matters most in security architecture: mitigations that sound correct but whose implementation is undefined, creating a false sense of coverage.

**Evidence quality:** Each insufficiency claim is technically verifiable. Python `re` module documentation confirms no timeout parameter. PyYAML SafeLoader documentation confirms no nesting depth limit. High confidence.

---

### Decision 9: Compound Vulnerability RV-002 (Critical, DREAD 41)

**Claim:** RV-002 (L2-REINJECT Governance Directive Injection) is rated Critical at DREAD 41, combining existing reinject.py gaps with the planned HtmlCommentMetadata interaction.

**Steelman argument:** This finding is the most architecturally important in the assessment, and its Critical rating is fully justified. The argument for the compound treatment of RV-002 is strong: the existing code (RV-006, DREAD 33) and the planned code (RV-002 compound, DREAD 41) are not independent vulnerabilities -- the planned HtmlCommentMetadata parser interacts with the same L2-REINJECT governance surface that RV-006 targets. The compound finding correctly identifies that the case-sensitivity gap (RV-014) creates a third attack surface: directives with non-standard casing that evade both the reinject parser (case-sensitive) and the HtmlCommentMetadata parser (case-insensitive exclusion). This means the actual governance injection surface is the union of three gaps, not three separate vulnerabilities. Rating the compound as Critical (DREAD 41) and presenting the five governance injection vectors (GOV-001 through GOV-004 plus the casing gap) as a unified threat is the correct analytical approach for a meta-security vulnerability.

**Evidence quality:** The code-level basis is verified: `reinject.py` `_REINJECT_PATTERN` is case-sensitive (line 45-47); `html_comment.py` `_REINJECT_PREFIX_RE` uses `re.IGNORECASE` (line 68). The gap between these two is real and demonstrated in source. High confidence.

---

## Steelman: Source Code Decisions

### Decision 10: Alias Count Pre-Check Before yaml.safe_load() (M-20)

**Source:** `yaml_frontmatter.py` lines 250-262

**Steelman argument:** The alias pre-check using `_ALIAS_RE.findall(raw_yaml)` is a defense-in-depth layer that operates at a different point in the processing pipeline than the post-parse result size check. The alias count check is O(n) over raw text and terminates before YAML parsing begins -- it aborts the entire parse if `max_alias_count` is exceeded. The post-parse result size check (lines 314-330) catches anchor expansion that evades the pre-check (e.g., many anchors within the max_alias_count limit that each expand to large structures). Using both checks closes the temporal gap: the pre-check prevents worst-case anchor expansion scenarios; the post-parse check catches more subtle cases where expansion is within anchor count limits but produces excessive output. This two-layer approach is exactly the defense-in-depth pattern the architecture calls for at BC-02.

**Evidence quality:** Both checks are present and readable in source. The `bounds.max_alias_count` and `bounds.max_yaml_result_bytes` are enforced at distinct pipeline stages. High confidence.

---

### Decision 11: XmlSectionParser Tag Alternation Pattern (Security Over Generality)

**Source:** `xml_section.py` lines 49-67 (`_build_section_pattern`)

**Steelman argument:** Building the regex from the ALLOWED_TAGS frozenset rather than using a general `[a-z][a-z_-]*` tag pattern is a correct security choice that sacrifices regex generality for safety. A general tag pattern would match any tag -- including wrapper tags like `<agent>` that could consume the entire document body, or attacker-crafted tags like `<admin>`. By constructing the alternation from only the known-good tags (`identity|purpose|input|capabilities|methodology|output|guardrails`), unknown tags are implicitly rejected at the pattern level without any explicit rejection code. The frozenset container guarantees immutability of the allowed tag set at class definition time -- it cannot be extended at runtime. The dynamic pattern construction also means the alternation is alphabetically sorted (`re.escape` on each tag) and then compiled once per parser invocation, avoiding the overhead of a static pattern that would need to handle all possible tags. The sorted ordering is deterministic, which matters for reproducible test behavior.

**Evidence quality:** The frozenset and `_build_section_pattern` are directly readable in source. The sorted alternation is confirmed by `"|".join(re.escape(tag) for tag in sorted(allowed_tags))`. High confidence.

---

### Decision 12: HtmlCommentMetadata Dual L2-REINJECT Exclusion

**Source:** `html_comment.py` lines 51-57 (regex negative lookahead) and lines 67-68, 174-176 (`_REINJECT_PREFIX_RE` secondary check)

**Steelman argument:** The dual exclusion strategy is architecturally stronger than either mechanism alone. The regex negative lookahead (`(?!L2-REINJECT:)` embedded in `_METADATA_COMMENT_PATTERN`) provides fast O(n) rejection for the exact-case match without a separate pass. The secondary `_REINJECT_PREFIX_RE.match(body)` check with `re.IGNORECASE` catches case variants that the inline lookahead misses -- the comment body is extracted first, then the case-insensitive check is applied. This two-stage approach means an attacker cannot bypass the exclusion by using `l2-reinject:` or `L2-Reinject:` casing. The fact that `_REINJECT_PREFIX_RE` uses `re.IGNORECASE` while the inline lookahead does not is intentional: the inline lookahead handles the common case (exact uppercase match) with zero overhead, and the secondary check handles bypass attempts. This is the right trade-off: O(1) check for the expected case, O(n) secondary check for the adversarial case. The secondary check's presence is documented in the inline comment (line 172-174), which directly acknowledges the limitation of the inline lookahead and explains the secondary check's purpose.

**Evidence quality:** Both mechanisms are readable in source. The inline comment at line 172-174 explicitly documents the rationale. High confidence.

---

### Decision 13: SchemaRegistry MappingProxyType + Freeze Pattern

**Source:** `schema_registry.py` lines 97-103 (freeze), 114-122 (schemas property)

**Steelman argument:** The `freeze()` + `MappingProxyType` combination remediates V-06 (mutable module-level dict) via the strongest available Python mechanism short of replacing the dict entirely. After `freeze()`, the `register()` method raises `RuntimeError` -- this is a positive assertion failure, not a silent no-op. The `schemas` property returns `MappingProxyType(self._schemas)` -- a view that prevents external code from calling `.__setitem__()`, `.update()`, `.clear()`, or `.pop()` on the underlying dict. Critically, `MappingProxyType` is a standard library type (`types.MappingProxyType`), not a custom wrapper, which means its immutability guarantees are enforced by the CPython runtime, not by convention. The `freeze()` method is idempotent (calling it twice does not error), which prevents defensive double-freeze patterns from causing unexpected failures. The collision detection in `register()` (lines 90-94) raises `ValueError` with a specific error message citing T-SV-04, making the threat model reference part of the error message for auditability.

**Evidence quality:** All behaviors are directly readable in source and verified by 42 test cases in `test_schema_registry.py`. High confidence.

---

### Decision 14: DocumentTypeDetector Path-First Priority with Mismatch Warning

**Source:** `document_type.py` lines 122-147

**Steelman argument:** The path-first strategy is correct for preventing content-based type spoofing (T-DT-01). An attacker who can create a file at an arbitrary path cannot control the path-based detection unless they also control the filesystem path within the expected Jerry directory structure -- a much stronger precondition than simply controlling file content. If path detection succeeds, content-based detection is still run but produces a mismatch warning rather than overriding the path result. This means the mismatch is observable and auditable (it is surfaced in `UniversalParseResult.type_detection_warning`) without changing the security-relevant path-based type assignment. The `UNKNOWN` safe default for unclassifiable files is the correct fail-closed posture: an unclassifiable file invokes only the nav parser (the least sensitive parser), which cannot deserialize YAML or process XML sections.

**Evidence quality:** The path-first logic is directly readable in `detect()`. The `_PARSER_MATRIX` entry for `DocumentType.UNKNOWN: {"nav"}` confirms the safe default. The mismatch warning propagation is verified in `UniversalDocument.parse()` (line 220). High confidence.

---

## Per-Dimension Preliminary Scores

**Note:** These are steelman-basis preliminary scores representing the strongest defensible reading of the deliverables. The S-014 critic pass will apply the adversarial lens and may reduce scores where reinforcement is needed.

### Implementation Report (eng-backend-001)

| Dimension | Weight | Score | Rationale |
|-----------|--------|-------|-----------|
| Completeness | 0.20 | 0.97 | All 21 WIs documented with specific file/line evidence. All 24 security mitigations mapped. All DDs verified. 3 known gaps enumerated with impact assessment. No section omitted. |
| Internal Consistency | 0.20 | 0.95 | Coverage numbers are consistent (879 stmts, 20 missed, 98%). Work item count matches file inventory. Test counts match. Gap 1 impact assessment (LOW) is consistent with the `_strip_control_chars()` M-18 mitigating the most common triggering inputs. |
| Methodological Rigor | 0.20 | 0.94 | Work item completion tied to specific file + line evidence. Coverage analysis categorizes misses by type. HARD rule compliance provides falsifiable evidence. CI workflow addition shifts compliance verification from runtime to structural. |
| Evidence Quality | 0.15 | 0.96 | Every claim is tied to a file path and line number or a test name. Coverage is verifiable by running pytest. The H-10 grandfathering explanation for multi-class files is accurate and specific. |
| Actionability | 0.15 | 0.93 | Phase 4 deferral is clearly scoped to WI-022 through WI-025 with named agent allocation. Gap remediation paths are specific (split file or add exception handler). Technical debt items have concrete resolution paths. |
| Traceability | 0.10 | 0.96 | WI references trace to implementation plan. DD references trace to ADR-PROJ005-003. M references trace to threat model. H references trace to quality-enforcement.md. |

**Preliminary weighted score (Implementation Report):** 0.95

### Vulnerability Assessment (red-vuln-001)

| Dimension | Weight | Score | Rationale |
|-----------|--------|-------|-----------|
| Completeness | 0.20 | 0.95 | 27 findings across existing and planned code. 8 new findings not in threat model. 6 DREAD challenges with downgrade example. 3 mitigation insufficiency findings. Appendices provide attack catalog, DREAD log, and full mitigation validation matrix. |
| Internal Consistency | 0.20 | 0.93 | DREAD scores are internally consistent with the stated scale (1-10 per dimension). The downgrade of RV-020 relative to T-XS-07 is consistent with the stated rationale (lazy quantifier behavior). Confidence scores are differentiated by analysis type. |
| Methodological Rigor | 0.20 | 0.95 | PTES Phase 3 + OSSTMM Section III dual framework. DREAD with per-dimension breakdown for every finding. Attack vectors include concrete CLI commands or code samples. Defense-in-depth analysis by trust zone layer. |
| Evidence Quality | 0.15 | 0.93 | Existing code findings cite specific file paths and line numbers (e.g., `reinject.py:45-47`, `schema.py:530`). Planned code findings clearly flagged as architecture-level assessment with lower confidence (0.85). Attack catalog provides step-by-step reproduction. |
| Actionability | 0.15 | 0.94 | Implementation priority table maps all findings to implementation phases. Three insufficiency findings provide specific alternative mechanisms (custom SafeLoader, `regex` library, explicit directory allowlist). Mitigation validation matrix provides per-mitigation sufficiency assessment. |
| Traceability | 0.10 | 0.95 | All findings reference CWE and original threat model entries where applicable. New findings explicitly marked "NOT IN THREAT MODEL." DREAD challenges cite original threat model ID and score. References section enumerates all input artifacts analyzed. |

**Preliminary weighted score (Vulnerability Assessment):** 0.94

### Combined Barrier 2 Preliminary Score

| Component | Weight | Score |
|-----------|--------|-------|
| Implementation Report | 0.50 | 0.95 |
| Vulnerability Assessment | 0.50 | 0.94 |
| **Combined** | | **0.945** |

---

## Areas Needing Reinforcement

The following areas have steelman-defensible positions but require additional evidence or clarification to withstand full adversarial critique. These are not weaknesses in the decisions themselves but in the evidence presented for them.

### Implementation Report: Reinforcement Gaps

**IR-R-001: HtmlCommentMetadata Dual Exclusion -- Incomplete Inline Lookahead**

The inline regex negative lookahead in `_METADATA_COMMENT_PATTERN` (`(?!L2-REINJECT:)`) is case-sensitive, while the implementation note at line 172-174 correctly documents this limitation. However, the document module-level docstring lists the security constraint as "Case-insensitive L2-REINJECT exclusion" without qualifying that this applies only to the secondary `_REINJECT_PREFIX_RE` check. A strict reading of the module docstring creates a gap: the inline lookahead is NOT case-insensitive. The implementation is correct, but the claim needs qualification.

**IR-R-002: yaml.reader.ReaderError -- Impact Assessment Underdeveloped**

The report states impact is LOW because `_strip_control_chars()` is designed to sanitize values post-parse, but ReaderError occurs pre-parse. This is accurate. However, the M-18 control character stripping (`_strip_control_chars()`) operates on the raw YAML string before `yaml.safe_load()` is called? Reading the code carefully: `_strip_control_chars()` is called on the extracted field values AFTER `yaml.safe_load()` parses them (lines 372-374 in `yaml_frontmatter.py`). The pre-parse stripping is not performed on the raw YAML block -- only the post-parse per-field stripping is done. The impact assessment needs to be more precise: the `ReaderError` gap is not mitigated by M-18, and null bytes or control chars in the raw YAML block (not just in field values) remain an unhandled case. The LOW impact assessment still holds (Jerry YAML frontmatter does not contain raw control chars in practice), but the technical justification in the report is slightly imprecise.

**IR-R-003: reinject.py 78% Coverage -- Pre-existing Debt Characterization**

The report correctly notes this is pre-existing debt, but does not provide the specific coverage target for reinject.py or confirm whether this violates H-20 (90% line coverage). H-20 requires 90% for the domain module as a whole (98% achieved), but individual file coverage is not mandated at 90%. The report should explicitly confirm that H-20 is satisfied at the module level and that per-file minimums are not required.

---

### Vulnerability Assessment: Reinforcement Gaps

**VA-R-001: RV-003 (Path Traversal) -- Status After WI-018 Implementation**

The vulnerability assessment was written before Phase 3 implementation. The implementation report confirms WI-018 is DONE and `_resolve_and_check_path()` is implemented with `JERRY_DISABLE_PATH_CONTAINMENT` env-var override for test compatibility. The assessment marks RV-003 as "CONFIRMED -- no mitigation exists in current code" which was accurate at assessment time but may create confusion for reviewers who read both reports simultaneously. The implementation report is the authoritative post-implementation state. The assessment needs a note that its status column reflects pre-implementation state, not post-WI-018 state.

**VA-R-002: M-05 (Regex Timeout) -- Implementation in Source Code Unclear**

The assessment correctly flags M-05 as "INSUFFICIENT -- no mechanism identified for Python `re`." However, the implementation report lists M-05 as... not listed in the "Security Mitigations Implemented" table. M-05 appears in the threat model but not in WI-001 through WI-021. This gap (M-05 not implemented) is not explicitly called out in the implementation report's Known Gaps section. The vulnerability assessment's insufficiency finding for M-05 appears to be a finding that the implementation report has not acknowledged as a gap.

**VA-R-003: Confidence Score Calibration Against Published Scale**

The assessment states overall confidence 0.88 with sub-scores 0.92 (existing code) and 0.85 (planned code). Per the handoff schema calibration guidance, 0.7-0.8 = "high (comprehensive coverage, minor gaps)" and 0.9-1.0 = "very high (complete, verified, no known gaps)." The 0.88 overall and 0.92 existing-code score are in the "very high" band but the assessment explicitly identifies 8 new findings and 3 insufficient mitigations. A confidence of 0.92 for existing code analysis is supportable (direct code review, all source files inspected) but should be acknowledged as calibrated to the analysis completeness (all source files reviewed) rather than to vulnerability completeness (all vulnerabilities found). This is a nuanced distinction but important for downstream calibration.

**VA-R-004: RV-019 (YAML Billion Laughs) -- Partially Mitigated by Pre-parse Alias Check**

The assessment rates RV-019 at DREAD 33 and flags M-03 as insufficient. However, the implementation report confirms that `yaml_frontmatter.py` includes a pre-parse alias count check using `_ALIAS_RE.findall(raw_yaml)` bounded by `bounds.max_alias_count` (lines 250-262). This is a partial mitigation for the Billion Laughs attack: limiting alias count limits the depth of anchor expansion (though not perfectly, as a small number of aliases can still produce exponential expansion via nested structure). The assessment should credit this partial mitigation and update M-03 from "NOT IMPLEMENTED" to "PARTIALLY IMPLEMENTED via max_alias_count pre-check; full depth limiting still requires custom SafeLoader."

---

## Composite Score

**Steelman preliminary composite (QG-B2):** 0.945

This score represents the strongest defensible reading of the Barrier 2 deliverables before adversarial critique. The [Areas Needing Reinforcement](#areas-needing-reinforcement) section identifies seven specific areas where evidence is imprecise, incomplete, or creates potential contradictions between the two deliverables. The adversarial critique pass (S-002, S-004, S-013) should focus on these seven areas as the primary leverage points.

The implementation is architecturally sound, security-conscious, and thoroughly documented. The vulnerability assessment is methodologically rigorous with appropriate calibration and correct technical reasoning. The steelman position is that these deliverables, taken together, represent a defensible and high-quality Barrier 2 gate.

**Threshold:** Quality gate requires >= 0.95 for C4 deliverables. Preliminary score of 0.945 is below threshold by 0.005. The reinforcement gaps (particularly IR-R-002 and VA-R-004, which identify a factual imprecision and a missing partial-mitigation credit respectively) could close this gap if addressed. Recommend targeted reinforcement of the seven identified areas before the S-014 scoring pass.

---

<!-- END OF STEELMAN FINDINGS -->
<!-- Agent: adv-executor-001 | Strategy: S-003 | QG: QG-B2 | Date: 2026-02-23 -->
*S-003 Steelman Findings v1.0.0*
*Preliminary composite: 0.945 (below 0.95 threshold by 0.005)*
*7 reinforcement gaps identified*
*Source: Implementation Report + Vulnerability Assessment + 6 source files*
