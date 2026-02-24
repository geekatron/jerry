# Inversion Report: Universal Markdown Parser Architecture (Phase 1 Deliverables)

**Strategy:** S-013 Inversion Technique
**Deliverables:** eng-architect-001-threat-model.md, eng-architect-001-architecture-adr.md, eng-architect-001-trust-boundaries.md, red-lead-001-scope.md
**Criticality:** C4
**Date:** 2026-02-22
**Reviewer:** adv-executor (S-013)
**Quality Gate:** QG-B1
**Goals Analyzed:** 7 | **Assumptions Mapped:** 14 | **Vulnerable Assumptions:** 8

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment and recommendation |
| [Step 1: Goal Inventory](#step-1-goal-inventory) | Explicit and implicit goals extracted from deliverables |
| [Step 2: Anti-Goal Analysis](#step-2-anti-goal-analysis) | Inverted goals -- what would guarantee failure |
| [Step 3: Assumption Map](#step-3-assumption-map) | All assumptions with confidence and validation status |
| [Step 4: Stress-Test Results](#step-4-stress-test-results) | Inversion of each assumption with consequences |
| [Step 5: Mitigations](#step-5-mitigations) | Specific actions for Critical and Major findings |
| [Step 6: Scoring Impact](#step-6-scoring-impact) | Dimension-level impact and overall weighted score |
| [Recommendations](#recommendations) | Prioritized mitigation actions |

---

## Summary

The four Phase 1 deliverables form a coherent security-oriented architecture for the universal markdown parser. The inversion analysis identified 14 assumptions across 5 categories (Technical, Process, Environmental, Resource, Temporal). Of these, 8 are vulnerable under stress-testing: 2 Critical, 4 Major, and 2 Minor. The most significant vulnerability cluster is the **single-control-point dependency** pattern -- multiple design decisions rely on a single enforcement mechanism (e.g., `yaml.safe_load()` as the sole deserialization defense, regex-only XML parsing as the sole XXE prevention), with defense-in-depth mechanisms that are documented but whose implementation sequencing is not enforced by the architecture itself. A second vulnerability cluster concerns **detection reliability** -- the path-first type detection strategy assumes the file path always carries reliable type signal, but several real-world scenarios break this assumption.

**Recommendation:** ACCEPT with targeted mitigations. No fundamental architectural flaws were found. The 2 Critical findings require mitigation before implementation proceeds. The 4 Major findings should be addressed during Phase 2 implementation.

---

## Step 1: Goal Inventory

### Explicit Goals

| ID | Goal | Source | Measurable Restatement |
|----|------|--------|------------------------|
| G-01 | Parse 10 distinct file types through a single unified interface | ADR DD-3 (UniversalDocument) | `UniversalDocument.parse()` returns a typed `UniversalParseResult` for all 10 `DocumentType` enum values without error |
| G-02 | Prevent arbitrary code execution from YAML frontmatter parsing | Threat Model T-YF-07, ADR C-04 | `yaml.safe_load()` exclusively used; no import path to `yaml.load()` or `yaml.unsafe_load()` exists in the codebase |
| G-03 | Eliminate XXE attack surface from XML section parsing | Threat Model T-XS-07, ADR C-07, M-11 | No XML parser library imported in `xml_section.py`; only `re` module used |
| G-04 | Enforce input resource bounds across all parsers | Threat Model M-05 through M-07, M-16, M-17, ADR DD-8 | `InputBounds` configuration applied to all parser `.extract()` calls; defaults enforce 1MB file, 32KB YAML, 100 keys, depth 5 |
| G-05 | Maintain immutability of domain objects post-parse | Threat Model Strategic Implication 4, ADR C-05 | All new domain objects use `@dataclass(frozen=True)`; no mutable state crosses BC-03 |

### Implicit Goals

| ID | Goal | Inferred From | Measurable Restatement |
|----|------|---------------|------------------------|
| G-06 | Backward compatibility with existing `JerryDocument` consumers | ADR DD-3 rationale, Consequences (Positive 5) | Existing code calling `JerryDocument.parse()`, `BlockquoteFrontmatter.extract()`, `validate_document()`, and CLI commands `ast parse/validate/frontmatter/modify` produces identical output before and after enhancement |
| G-07 | Accurate document type detection for routing to correct parser(s) | ADR DD-2, Threat Model T-DT-01 | `DocumentTypeDetector.detect()` correctly classifies >= 95% of files in the Jerry repository without misclassification; path-first signal takes precedence over structure-based fallback |

---

## Step 2: Anti-Goal Analysis

### AG-01: Guarantee Code Execution via Parser (Inverts G-02)

**To guarantee arbitrary code execution, we would need:**
1. A code path that calls `yaml.load()` with `FullLoader` or `UnsafeLoader` instead of `yaml.safe_load()`
2. A way to bypass the banned-API lint rule (M-01) -- e.g., obfuscated import, dynamic import, aliased function
3. A way to introduce `yaml.load()` through a dependency chain where a library re-exports PyYAML functions

**Deliverable coverage:** The architecture ADR documents `yaml.safe_load()` as an architectural constraint (C-04). The threat model specifies M-01 (banned-API lint rule) and M-04 (integration test). However, neither document specifies enforcement of the import prohibition at the module level (e.g., `__all__` restriction, import hook, or AST-level check in CI). The lint rule is documented but its implementation mechanism is described as "ruff rule or pre-commit hook" -- neither is specified concretely.

**Finding:** IN-001-B1 (see below)

### AG-02: Guarantee DoS via Resource Exhaustion (Inverts G-04)

**To guarantee denial of service, we would need:**
1. A parser invocation that bypasses `InputBounds` -- e.g., calling the parser directly without the bounds parameter
2. An input that expands exponentially after passing the pre-parse size check (billion laughs)
3. A regex pattern in schema validation that causes catastrophic backtracking (ReDoS)

**Deliverable coverage:** The ADR makes `InputBounds` an optional parameter (`bounds: InputBounds | None = None`) with `InputBounds.DEFAULT` as the fallback. This means callers CAN bypass bounds by passing `None` explicitly. The threat model identifies this risk (M-07, M-06) but the architecture does not enforce bounds at the interface level -- bounds enforcement is delegated to each parser's implementation discipline. The billion-laughs scenario is specifically called out (T-YF-06) with pre-parse size limits, but the post-parse expansion check (M-06, "total serialized size <= 64 KB") occurs AFTER `yaml.safe_load()` has already expanded the content in memory.

**Finding:** IN-002-B1, IN-003-B1 (see below)

### AG-03: Guarantee Parser Misrouting (Inverts G-07)

**To guarantee the wrong parser processes a file, we would need:**
1. A file placed at a path matching one document type but containing content structured for a different type
2. A file not matching any path pattern, forcing structure-based detection, where the structural cues are ambiguous
3. A file with both `---` YAML delimiters and `> **Key:** Value` blockquote frontmatter

**Deliverable coverage:** The ADR documents path-first detection (DD-2) and the threat model identifies type spoofing (T-DT-01, T-DT-02). However, the architecture does not define behavior when a file matches BOTH YAML and blockquote frontmatter structural cues during fallback detection. The Parser Invocation Matrix (ADR DD-3) is defined per DocumentType, not per detected structural features, meaning a misclassified file will have the wrong set of parsers applied.

**Finding:** IN-005-B1 (see below)

### AG-04: Guarantee Governance Bypass via L2-REINJECT (Inverts implicit governance integrity goal)

**To guarantee governance bypass, we would need:**
1. A way to inject unauthorized L2-REINJECT directives through the new HTML comment parser
2. A way to modify existing L2-REINJECT directives through the `ast modify` write-back path
3. A way to suppress legitimate L2-REINJECT directives by crafting content that confuses the reinject parser

**Deliverable coverage:** The red team scope (RED-0001) explicitly calls out "L2-REINJECT spoofing" as a Critical test case. The HtmlCommentMetadata parser is designed with a negative lookahead `(?!L2-REINJECT:)` to exclude reinject directives. However, the deliverables do not address the inverse scenario: what if the negative lookahead has a regex bypass (e.g., unicode normalization, leading whitespace, case variation)? The threat model does not model L2-REINJECT-specific threats despite the red team scope identifying this as governance-critical.

**Finding:** IN-004-B1 (see below)

### AG-05: Guarantee Schema Validation Bypass (Inverts G-01)

**To guarantee schema validation is circumvented, we would need:**
1. Schema registry collision (T-SV-04) -- register a permissive schema under an existing entity type name
2. ReDoS in value_pattern that hangs validation (T-SV-03), causing timeout and skipped validation
3. A document type correctly detected but routed to validation with a schema that does not match its actual structure

**Deliverable coverage:** The ADR addresses collision prevention (`ValueError` on duplicate registration). The threat model identifies ReDoS (T-SV-03, M-12). However, the SchemaRegistry uses a plain `dict` with no locking or immutability after initialization -- if `register()` can be called after initial module load, a malicious agent definition processed during a session could theoretically trigger schema re-registration.

**Finding:** IN-006-B1 (see below)

### AG-06: Guarantee Loss of Backward Compatibility (Inverts G-06)

**To guarantee backward compatibility breaks, we would need:**
1. Changes to `JerryDocument.parse()` return type or behavior
2. Changes to `BlockquoteFrontmatter.extract()` signature or semantics
3. Changes to existing CLI command output format

**Deliverable coverage:** The ADR explicitly states that `UniversalDocument` is additive and `JerryDocument` is unchanged. However, the ADR extends `schema.py` with a `SchemaRegistry` class that replaces the module-level `get_entity_schema()` function. If `get_entity_schema()` delegates to the registry, and the registry initialization order changes, existing callers could get `ValueError` on schemas that were previously available. This is not addressed.

**Finding:** IN-007-B1 (see below)

### AG-07: Guarantee Immutability Violation (Inverts G-05)

**To guarantee domain object mutation post-parse, we would need:**
1. A mutable container inside a frozen dataclass (e.g., `list` field on `UniversalParseResult`)
2. A code path that modifies the `JerryDocument` internal state after it is wrapped by `UniversalParseResult`
3. A post-construction mutation via `object.__setattr__()` on a frozen dataclass

**Deliverable coverage:** The ADR specifies `@dataclass(frozen=True)` for all new types. The `UniversalParseResult` uses `list[XmlSection] | None` for `xml_sections` -- `list` is mutable even inside a frozen dataclass. A consumer could do `result.xml_sections.append(malicious_section)` without triggering a `FrozenInstanceError`. The existing `YamlFrontmatterResult` uses `tuple[YamlFrontmatterField, ...]` (immutable), but `UniversalParseResult` does not.

**Finding:** IN-008-B1 (see below)

---

## Step 3: Assumption Map

| ID | Assumption | Type | Category | Confidence | Validation Status | Consequence of Failure |
|----|-----------|------|----------|------------|-------------------|----------------------|
| A-01 | `yaml.safe_load()` is sufficient defense against all YAML deserialization attacks | Explicit | Technical | High | Logically inferred (PyYAML docs confirm safe_load restricts to basic types) | If safe_load has an undiscovered bypass, arbitrary code execution is possible |
| A-02 | A banned-API lint rule will catch all uses of `yaml.load()` | Explicit | Process | Medium | Not yet validated (lint rule not implemented) | Unsafe YAML load call could enter codebase undetected |
| A-03 | Regex-only XML parsing eliminates all XML-related attack vectors | Explicit | Technical | High | Logically inferred (no XML parser = no XML attack surface) | If regex has edge cases that produce XML-parser-like behavior, some attack vectors persist |
| A-04 | `InputBounds` defaults will be applied by all callers | Implicit | Process | Low | Not validated (optional parameter) | Callers can bypass bounds by not passing the parameter |
| A-05 | Pre-parse YAML size check (32KB) prevents billion-laughs expansion | Explicit | Technical | Medium | Not validated (yaml.safe_load expansion ratios not measured) | A 32KB YAML payload could expand to hundreds of MB via anchor/alias |
| A-06 | Path-first detection is always reliable for files in the Jerry repository | Implicit | Environmental | Medium | Partially validated (current repo structure is consistent) | Files moved, renamed, or placed outside standard paths will be misclassified |
| A-07 | Structural fallback detection can disambiguate when path detection fails | Implicit | Technical | Low | Not validated | Files with ambiguous structural cues (both YAML and blockquote patterns) will be misclassified |
| A-08 | The HtmlCommentMetadata negative lookahead `(?!L2-REINJECT:)` is sufficient to prevent reinject directive spoofing | Implicit | Technical | Medium | Not validated (regex bypass not tested) | Crafted comments could be mistaken for legitimate reinject directives or vice versa |
| A-09 | SchemaRegistry is effectively immutable after module load | Implicit | Technical | Low | Not validated (no immutability enforcement after init) | Runtime schema registration could overwrite validation rules |
| A-10 | Existing `get_entity_schema()` callers will transparently work with the new registry backend | Implicit | Process | Medium | Not validated (delegation not implemented) | Backward compatibility break for existing callers |
| A-11 | Frozen dataclasses with mutable container fields are sufficiently immutable | Implicit | Technical | Low | Not validated (Python semantics allow mutation of list contents inside frozen dataclass) | Post-parse tampering of domain objects via mutable list fields |
| A-12 | The current threat model covers all new attack vectors introduced by universal parsing | Explicit | Process | High | Self-assessed by threat model author | Unidentified attack vectors remain unmitigated |
| A-13 | The red team scope document will be reviewed and confirmed before testing begins | Explicit | Process | High | Enforced by P-020 (user authority) | Unauthorized testing could damage the codebase |
| A-14 | PyYAML version will remain stable and not introduce new unsafe behaviors | Explicit | Environmental | Medium | Not validated (depends on upstream library) | Dependency upgrade introduces new attack surface |

---

## Step 4: Stress-Test Results

| ID | Assumption | Inversion | Plausibility | Severity | Evidence | Affected Dimension |
|----|-----------|-----------|-------------|----------|----------|--------------------|
| IN-001-B1 | A-02: Banned-API lint rule catches all yaml.load() | What if the lint rule has gaps -- dynamic imports (`getattr(yaml, 'load')`), aliased imports (`from yaml import load as safe_load`), or dependency-transitive calls? | Medium -- dynamic import patterns are a known lint-rule bypass technique; aliased imports are syntactically valid Python | Critical | Threat model M-01 specifies "ruff rule or pre-commit hook" but does not specify coverage for dynamic/aliased import patterns. ADR C-04 states the constraint but enforcement is entirely delegated to the unimplemented lint rule. No secondary enforcement (e.g., runtime import hook, integration test that scans AST) is specified. | Methodological Rigor |
| IN-002-B1 | A-05: 32KB pre-parse YAML check prevents billion-laughs | What if yaml.safe_load() can expand a 32KB payload to hundreds of MB via anchor/alias? A 32KB YAML file with nested anchors can produce O(2^n) expansion. | High -- this is a documented characteristic of YAML anchor/alias expansion; a 32KB payload with 40 levels of doubling produces 2^40 elements | Critical | Threat model identifies T-YF-06 and specifies M-07 (pre-parse 32KB limit) + M-06 (post-parse depth validation). But M-06 validates AFTER safe_load completes -- the expansion occurs IN MEMORY during safe_load. Post-parse validation cannot prevent the memory exhaustion that occurs during parsing. | Evidence Quality |
| IN-003-B1 | A-04: InputBounds defaults applied by all callers | What if a developer calls `YamlFrontmatter.extract(doc)` without `bounds` and the default parameter is `None` (not `InputBounds.DEFAULT`)? | High -- the ADR signature shows `bounds: InputBounds | None = None`, meaning `None` is the default, not `InputBounds.DEFAULT`. The parser must internally fall back to defaults, but this is implementation discipline, not architectural enforcement. | Major | ADR DD-8 defines `InputBounds.DEFAULT` as a class-level singleton and states "Parsers use InputBounds.DEFAULT unless the caller provides a custom instance" but the method signature defaults to `None`, not to `InputBounds.DEFAULT`. The gap between intention and API surface creates a contract ambiguity. | Internal Consistency |
| IN-004-B1 | A-08: Negative lookahead prevents L2-REINJECT spoofing | What if the negative lookahead `(?!L2-REINJECT:)` can be bypassed via case variation (`l2-reinject:`), leading whitespace (`  L2-REINJECT:`), unicode confusables, or zero-width characters between "L2" and "-"? | Medium -- HTML comments are case-sensitive in the regex, but L2-REINJECT directives in the codebase are uppercase. A lowercase variant would bypass the negative lookahead AND the reinject parser's own pattern, creating an orphaned directive that neither parser handles. | Major | ADR DD-7 specifies the negative lookahead pattern. The reinject parser in `reinject.py` uses its own pattern `_REINJECT_PATTERN` (not documented in these deliverables). Neither document specifies case-handling coordination between the two parsers. | Completeness |
| IN-005-B1 | A-07: Structural fallback can disambiguate | What if a file has both `---` YAML delimiters and `> **Type:** strategy-template` blockquote frontmatter (e.g., a strategy template that someone adds YAML frontmatter to)? The structural detector would match both YAML and blockquote cues. | High -- the deliverables do not define priority or disambiguation logic for conflicting structural cues. The path-first algorithm handles the common case, but structural fallback is explicitly the fallback for files outside standard paths. | Major | ADR DD-2 defines the detection algorithm with path patterns and "structural-cue fallback" but does not specify the ordering or priority of structural cues. The reference to M-14 (dual-signal validation) produces a warning on mismatch but does not define which signal wins when both are present. | Completeness |
| IN-006-B1 | A-09: SchemaRegistry is immutable after module load | What if `register()` is callable at any time, and a file processed during a session contains code that triggers schema re-registration? | Low -- this requires a code path from file parsing to schema registration, which does not exist in the proposed architecture. However, the registry is a mutable object with no freeze mechanism. | Major | ADR DD-4 shows `SchemaRegistry` with a public `register()` method and collision detection, but no `freeze()` or `locked` state to prevent post-initialization registration. The registry is a module-level singleton, accessible to any code that imports `schema.py`. | Internal Consistency |
| IN-007-B1 | A-10: Existing callers transparently work with registry | What if the `_DEFAULT_REGISTRY` initialization order differs from the current `get_entity_schema()` dict initialization, causing a timing-dependent failure? | Low -- Python module-level initialization is deterministic. However, if the registry auto-registration is moved to a separate initialization function (common pattern for lazy loading), callers that import and use the module early could encounter an empty registry. | Minor | ADR DD-4 states "The six worktracker schemas are auto-registered at module load time" but does not specify whether registration happens at import time (module body) or lazily. | Traceability |
| IN-008-B1 | A-11: Frozen dataclasses are sufficiently immutable | What if `UniversalParseResult.xml_sections` (typed as `list[XmlSection] | None`) is mutated by a consumer calling `.append()` or `.pop()` on the list? | High -- Python frozen dataclasses prevent attribute reassignment (`result.xml_sections = new_list` raises `FrozenInstanceError`) but do NOT prevent mutation of mutable container contents (`result.xml_sections.append(x)` succeeds). This is a well-known Python limitation. | Major | ADR DD-3 specifies `xml_sections: list[XmlSection] | None` and `html_comments: list[HtmlCommentBlock] | None`. The `YamlFrontmatterResult` correctly uses `tuple[...]` for its `fields` attribute, demonstrating awareness of the pattern. But `UniversalParseResult` uses `list` for two fields. | Internal Consistency |

---

## Step 5: Mitigations

### Critical Findings

#### IN-001-B1: Lint Rule Gaps for yaml.load() Detection

**Mitigation:** Implement defense-in-depth beyond the lint rule:
1. Add an integration test (`test_yaml_safe_load_enforcement.py`) that uses Python's `ast` module to scan `yaml_frontmatter.py` for ANY reference to `yaml.load`, `yaml.unsafe_load`, `yaml.FullLoader`, `yaml.UnsafeLoader` -- including aliased imports and `getattr()` patterns.
2. Add a CI check (L5 enforcement) that greps the entire `src/domain/markdown_ast/` directory for `yaml.load` (not just `yaml.safe_load`) and fails on any match.
3. In `yaml_frontmatter.py`, add a module-level assertion: `assert not hasattr(yaml, '_jerry_unsafe_marker')` -- a canary that would be tripped by any monkey-patching attempt.

**Acceptance Criteria:** Three independent mechanisms prevent `yaml.load()` usage: (a) lint rule, (b) AST-based integration test, (c) CI grep check. Any one of the three catching the violation is sufficient.

#### IN-002-B1: Pre-Parse Size Check Insufficient for Billion-Laughs

**Mitigation:** Add a resource-limited parsing wrapper:
1. Use `yaml.safe_load()` with a monitoring wrapper that measures the resulting object's approximate memory size DURING construction, not just after. If the result exceeds 64KB serialized, abort.
2. Alternative: Use a streaming YAML parser or implement a custom anchor/alias counter that rejects YAML with more than N anchor references (e.g., 100) before passing to `yaml.safe_load()`.
3. Most practical: Pre-scan the raw YAML text for anchor (`&`) and alias (`*`) characters. If the ratio of alias references to anchors exceeds a threshold (e.g., 10:1), reject the YAML before parsing.

**Acceptance Criteria:** A 32KB YAML payload with billion-laughs structure is rejected BEFORE `yaml.safe_load()` causes memory exhaustion. Test case: `a: &x [*x,*x,*x,*x,*x,*x,*x,*x,*x,*x]` must be rejected.

### Major Findings

#### IN-003-B1: InputBounds Default Parameter Gap

**Mitigation:** Change the method signature from `bounds: InputBounds | None = None` to `bounds: InputBounds = InputBounds.DEFAULT` across all parser `.extract()` methods. This makes bounds enforcement opt-out (must pass a custom `InputBounds` to relax) rather than opt-in.

**Acceptance Criteria:** Calling `YamlFrontmatter.extract(doc)` without a `bounds` argument applies `InputBounds.DEFAULT` limits. The signature's default value IS `InputBounds.DEFAULT`, not `None`.

#### IN-004-B1: L2-REINJECT Negative Lookahead Bypass

**Mitigation:** Coordinate the two parsers' patterns:
1. The HtmlCommentMetadata parser should use a case-insensitive negative lookahead: `(?!(?i)L2-REINJECT:)`.
2. Both parsers should strip leading whitespace from the comment body before pattern matching.
3. Add an integration test that verifies: (a) legitimate L2-REINJECT directives are ONLY captured by the reinject parser, (b) case-variant L2-REINJECT strings are captured by neither parser (rejected by both).

**Acceptance Criteria:** `<!-- l2-reinject: rank=0, content="..." -->` is rejected by both parsers. `<!-- L2-REINJECT: rank=1, content="..." -->` is captured only by the reinject parser.

#### IN-005-B1: Structural Detection Ambiguity

**Mitigation:** Define an explicit priority ordering for structural cues:
1. `---` YAML delimiters (highest priority in structural fallback)
2. `> **Key:** Value` blockquote frontmatter
3. `<identity>` XML section tags
4. `<!-- key: value -->` HTML comment metadata
5. `<!-- L2-REINJECT: -->` reinject directives

Document this ordering in the `DocumentTypeDetector` class. When multiple structural cues match, use the highest-priority cue. Emit a `type_detection_warning` for multi-cue matches.

**Acceptance Criteria:** A file with both `---` YAML delimiters and `> **Type:**` blockquote patterns, not matching any path pattern, is classified as the YAML-based type (highest structural priority).

#### IN-008-B1: Mutable List Fields in Frozen Dataclass

**Mitigation:** Change `UniversalParseResult` field types from `list` to `tuple`:
- `xml_sections: list[XmlSection] | None` -> `xml_sections: tuple[XmlSection, ...] | None`
- `html_comments: list[HtmlCommentBlock] | None` -> `html_comments: tuple[HtmlCommentBlock, ...] | None`
- `reinject_directives: list[ReinjectDirective] | None` -> `reinject_directives: tuple[ReinjectDirective, ...] | None`
- `nav_entries: list[NavEntry] | None` -> `nav_entries: tuple[NavEntry, ...] | None`

This is consistent with `YamlFrontmatterResult.fields: tuple[YamlFrontmatterField, ...]` in the same ADR.

**Acceptance Criteria:** All container fields on `UniversalParseResult` use `tuple` (immutable), not `list` (mutable). `result.xml_sections.append(x)` raises `AttributeError`.

### Minor Findings

#### IN-006-B1: SchemaRegistry Post-Init Mutability

**Mitigation:** Add a `freeze()` method to `SchemaRegistry` that sets a `_frozen` flag. After module-level initialization calls `_DEFAULT_REGISTRY.freeze()`, subsequent `register()` calls raise `RuntimeError`. This is a defensive measure; the current architecture does not have a code path that triggers runtime registration from file parsing.

**Acceptance Criteria:** `_DEFAULT_REGISTRY.register(new_schema)` after freeze raises `RuntimeError("Registry is frozen")`.

#### IN-007-B1: Registry Initialization Timing

**Mitigation:** Document in the ADR that schema auto-registration occurs at module import time (in the module body, not in a function). Add a module-level comment `# Auto-registration: these execute at import time` above the registration calls.

**Acceptance Criteria:** The ADR specifies "module body" (not lazy/deferred) initialization for the default registry.

---

## Step 6: Scoring Impact

| Dimension | Weight | Score | Impact | Rationale |
|-----------|--------|-------|--------|-----------|
| Completeness | 0.20 | 0.82 | Negative | IN-004-B1: L2-REINJECT spoofing scenario not addressed in threat model despite being governance-critical. IN-005-B1: Structural detection ambiguity behavior undefined for multi-cue matches. The threat model covers the new parser attack vectors thoroughly but has a blind spot at the boundary between the new HtmlCommentMetadata parser and the existing reinject parser. |
| Internal Consistency | 0.20 | 0.80 | Negative | IN-003-B1: API signature (`bounds: None`) contradicts documented intention ("parsers use DEFAULT"). IN-008-B1: `UniversalParseResult` uses mutable `list` while `YamlFrontmatterResult` uses immutable `tuple` for the same pattern -- inconsistent immutability application within the same ADR. IN-006-B1: Registry has public `register()` with no freeze mechanism, contradicting the "immutable after init" implicit assumption. |
| Methodological Rigor | 0.20 | 0.85 | Negative | IN-001-B1: Defense-in-depth for yaml.safe_load enforcement relies on an unimplemented lint rule with unspecified coverage for bypass patterns. The threat model correctly identifies the risk but the ADR's enforcement mechanism is underspecified. The STRIDE/DREAD/PASTA methodology is rigorously applied across all four deliverables. |
| Evidence Quality | 0.15 | 0.80 | Negative | IN-002-B1: The claim that pre-parse size limits prevent billion-laughs is not supported by evidence of expansion ratios. No measurement or reference is provided for how much a 32KB YAML payload can expand. The threat model states the risk but does not quantify the gap between the 32KB limit and the actual expansion potential. |
| Actionability | 0.15 | 0.90 | Neutral | Mitigation recommendations in the threat model (M-01 through M-19) are specific and actionable. The ADR design decisions are implementable. The red team scope is comprehensive with clear test cases. Minor gap: the threat model mitigations do not specify acceptance criteria. |
| Traceability | 0.10 | 0.90 | Neutral | Strong cross-referencing between all four documents. Threat IDs (T-YF-xx, T-XS-xx) map to DREAD scores, attack trees, and mitigations. ADR constraints (C-01 through C-07) trace to threat model mitigations. Red team scope traces to OWASP and CWE. IN-007-B1: Minor gap in traceability between registry initialization specification and backward compatibility claim. |

### Overall Weighted Score

| Dimension | Weight | Score | Weighted |
|-----------|--------|-------|----------|
| Completeness | 0.20 | 0.82 | 0.164 |
| Internal Consistency | 0.20 | 0.80 | 0.160 |
| Methodological Rigor | 0.20 | 0.85 | 0.170 |
| Evidence Quality | 0.15 | 0.80 | 0.120 |
| Actionability | 0.15 | 0.90 | 0.135 |
| Traceability | 0.10 | 0.90 | 0.090 |
| **TOTAL** | **1.00** | | **0.839** |

**Verdict:** REJECTED (below 0.92 threshold). The deliverables are architecturally sound but have specific gaps identified by inversion that require targeted revision. The 2 Critical and 4 Major findings drive the score below threshold. Addressing IN-001-B1, IN-002-B1, IN-003-B1, and IN-008-B1 (the most actionable findings) would likely raise the score into the REVISE band (0.85-0.91). Addressing all 8 findings would likely achieve PASS.

---

## Recommendations

### Priority 1: MUST Mitigate (Critical)

| ID | Finding | Action | Acceptance Criteria |
|----|---------|--------|---------------------|
| IN-001-B1 | Lint rule gaps for yaml.load() | Add AST-based integration test + CI grep check as defense-in-depth | Three independent mechanisms prevent yaml.load() usage |
| IN-002-B1 | Pre-parse size check insufficient for billion-laughs | Add anchor/alias pre-scan before yaml.safe_load() | 32KB billion-laughs YAML rejected before memory exhaustion |

### Priority 2: SHOULD Mitigate (Major)

| ID | Finding | Action | Acceptance Criteria |
|----|---------|--------|---------------------|
| IN-003-B1 | InputBounds default parameter gap | Change signature default from `None` to `InputBounds.DEFAULT` | Bounds enforced without explicit caller opt-in |
| IN-004-B1 | L2-REINJECT negative lookahead bypass | Case-insensitive lookahead + cross-parser coordination test | Case-variant reinject strings rejected by both parsers |
| IN-005-B1 | Structural detection ambiguity | Define explicit structural cue priority ordering | Multi-cue files classified deterministically |
| IN-008-B1 | Mutable list fields in frozen dataclass | Change `list` to `tuple` on `UniversalParseResult` | All container fields immutable |

### Priority 3: MAY Mitigate (Minor)

| ID | Finding | Action | Acceptance Criteria |
|----|---------|--------|---------------------|
| IN-006-B1 | SchemaRegistry post-init mutability | Add `freeze()` method | Post-init registration raises RuntimeError |
| IN-007-B1 | Registry initialization timing | Document module-body initialization in ADR | ADR specifies non-deferred initialization |

---

### Hidden Assumptions Surfaced by Inversion

This analysis surfaced the following assumptions that were not explicitly stated in any deliverable:

1. **Single-control-point sufficiency** -- Multiple design decisions assume a single enforcement mechanism is sufficient (yaml.safe_load, regex-only XML, negative lookahead). The architecture is defense-in-depth in principle but single-point-of-failure in several implementations.

2. **Optional parameter discipline** -- The `InputBounds` design assumes all callers will either pass bounds or that the parser will internally default. The API contract is ambiguous because the default is `None`, not `InputBounds.DEFAULT`.

3. **Container immutability equivalence** -- The deliverables treat frozen dataclasses as fully immutable, but Python's frozen dataclass semantics only prevent attribute reassignment, not mutation of mutable container contents.

4. **Structural detection determinism** -- The path-first detection is deterministic, but the structural fallback is not defined for ambiguous cases. The architecture assumes structural ambiguity is rare enough to handle via warnings, but does not define what the system DOES when both YAML and blockquote patterns are present.

5. **Cross-parser coordination** -- The HtmlCommentMetadata parser and the L2-REINJECT parser operate on the same input (HTML comments) but are designed independently. The negative lookahead is the only coordination mechanism, and it has known regex bypass patterns.

---

<!-- VERSION: 1.0.0 | DATE: 2026-02-22 | STRATEGY: S-013 | QUALITY-GATE: QG-B1 | AGENT: adv-executor -->
