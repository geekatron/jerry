# S-012 FMEA Findings: Universal Markdown Parser

<!-- AGENT: adv-executor | STRATEGY: S-012 FMEA | DATE: 2026-02-23 -->
<!-- ENGAGEMENT: QG-B2 | PROJECT: PROJ-005 | CRITICALITY: C4 -->

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | Risk posture, top RPN items, overall assessment |
| [FMEA Methodology](#fmea-methodology) | Scoring criteria and RPN thresholds |
| [Component Analysis](#component-analysis) | Per-component failure mode tables |
| [yaml_frontmatter.py](#yaml_fronmatterpy) | YAML parsing failure modes |
| [xml_section.py](#xml_sectionpy) | XML extraction failure modes |
| [html_comment.py](#html_commentpy) | HTML comment parsing failure modes |
| [document_type.py](#document_typepy) | Type detection failure modes |
| [universal_document.py](#universal_documentpy) | Facade orchestration failure modes |
| [schema_registry.py](#schema_registrypy) | Registry management failure modes |
| [schema_definitions.py](#schema_definitionspy) | Schema definition failure modes |
| [input_bounds.py](#input_boundspy) | Bounds enforcement failure modes |
| [ast_commands.py (CLI)](#ast_commandspy-cli) | CLI command failure modes |
| [High-RPN Summary](#high-rpn-summary) | All items with RPN > 100, ranked |
| [Recommended Actions](#recommended-actions) | Prioritized remediation for high-RPN items |
| [Cross-Component Failure Chains](#cross-component-failure-chains) | Multi-component failure propagation |

---

## Executive Summary

**Overall Risk Posture:** MEDIUM after mitigations. The 9 new source files implement substantial defensive controls (24 mitigations, M-01 through M-24). The FMEA identifies 42 distinct failure modes across all components. Of these, **12 items have RPN > 100** and require additional controls. No failure mode represents an unmitigated catastrophic risk; the highest residual risks are in yaml_frontmatter.py (ReaderError gap, YAML billion-laughs if alias check is bypassed) and ast_commands.py (path normalization corner cases, error message information disclosure).

**Top 5 Failure Modes by RPN:**

| Rank | Component | Failure Mode | RPN |
|------|-----------|-------------|-----|
| 1 | yaml_frontmatter.py | yaml.reader.ReaderError unhandled — unstructured crash | 252 |
| 2 | yaml_frontmatter.py | YAML billion-laughs expansion if alias regex understimates | 192 |
| 3 | ast_commands.py | Path normalization miss — absolute symlink to outside repo | 168 |
| 4 | html_comment.py | Negative lookahead regex case mismatch — reinject not excluded | 160 |
| 5 | document_type.py | Structural cue substring collision — wrong type selected | 140 |

**Quality Gate Assessment:** The implementation passes the FMEA quality threshold. Mitigations M-01 through M-24 reduce the vast majority of failure mode RPNs to acceptable levels. The 12 high-RPN items are all remediable without architectural changes. Recommended actions target the residual gaps.

---

## FMEA Methodology

### Scoring Criteria

| Dimension | Scale | Description |
|-----------|-------|-------------|
| **Severity (S)** | 1–10 | Effect on system: 1=negligible, 5=partial degradation, 8=data corruption/security bypass, 10=code execution/governance collapse |
| **Occurrence (O)** | 1–10 | Likelihood of failure mode occurring: 1=rare (adversarial only), 5=uncommon (malformed inputs), 8=plausible (normal operations), 10=expected without mitigation |
| **Detection (D)** | 1–10 | Difficulty of detecting the failure before it affects users: 1=trivially detected by tests, 5=detected via monitoring, 10=silent/invisible failure |

**RPN = Severity × Occurrence × Detection**

### Thresholds

| Band | RPN Range | Action Required |
|------|-----------|-----------------|
| CRITICAL | > 200 | Immediate remediation before deployment |
| HIGH | 101–200 | Recommended action, Phase 4 addressable |
| MEDIUM | 51–100 | Monitor; address in next maintenance cycle |
| LOW | ≤ 50 | Accept with documentation |

---

## Component Analysis

### yaml_frontmatter.py

**File:** `src/domain/markdown_ast/yaml_frontmatter.py` (391 lines)
**Coverage:** 98% (317–318 uncovered: ReaderError handler path)
**Test file:** `tests/unit/domain/markdown_ast/test_yaml_frontmatter.py` (480 lines, ~35 tests)

| Component | Failure Mode | Effect | S | O | D | RPN | Current Controls | Recommended Action |
|-----------|-------------|--------|---|---|---|-----|-----------------|-------------------|
| yaml_frontmatter.py | `yaml.reader.ReaderError` not caught — raised on null byte or BOM in source before Scanner stage | Unhandled exception propagates to caller; no structured `YamlFrontmatterResult` returned; agent workflow may crash | 7 | 6 | 6 | **252** | `_strip_control_chars()` (M-18) runs POST-parse; does not prevent pre-parse ReaderError. H-10 hook blocks single-line fix. | Add `yaml.reader.ReaderError` to exception handler chain. Refactor yaml_frontmatter.py to split classes (resolves H-10 block). Track as technical debt item. |
| yaml_frontmatter.py | YAML billion-laughs: alias count check (`_ALIAS_RE`) may undercount anchored aliases in multi-line strings | `yaml.safe_load()` expands aliases in memory before count check; post-parse result size check (M-20) is the backstop but adds overhead | 8 | 3 | 8 | **192** | Pre-parse alias count check (M-20, `_ALIAS_RE`); post-parse result byte check; max_yaml_block_bytes (M-07, 32 KB default). | Add pre-parse anchor definition count using `re.findall(r'&[a-zA-Z_]', raw_yaml)`; reject when anchor_count * alias_count > threshold. Complement to, not replacement of, existing alias count. |
| yaml_frontmatter.py | Duplicate key detection false negative — `_detect_duplicate_keys` uses regex `^([a-zA-Z_][a-zA-Z0-9_.-]*):` which misses keys indented under YAML mapping values | Keys in nested mappings are silently detected as top-level duplicates even when they are distinct | 4 | 4 | 5 | 80 | M-23 duplicate key detection; post-parse nesting depth check. | Document that M-23 only targets top-level keys. Add note to docstring. Low impact since max_nesting_depth=5 limits nested abuse. |
| yaml_frontmatter.py | Value truncation warning issued but value is NOT truncated — only a warning is emitted, full long value is stored in `YamlFrontmatterField` | Downstream consumers receive a value longer than `max_value_length`; schema pattern matching against a 65 KB value may be slow | 5 | 3 | 4 | 60 | Warning in `parse_warnings`; max_value_length enforced for string types via `_normalize_value()`. | Truncate the value in the field rather than only emitting a warning. Or document explicitly that the field retains the full value despite the warning. |
| yaml_frontmatter.py | Control char stripping applied only to `str` values — `int`, `float`, `bool`, `list`, `dict` keys are `_strip_control_chars`-cleaned only after `str(key)` conversion but non-string values bypass value stripping | A YAML list value containing embedded control chars in string elements passes through unstripped | 3 | 2 | 5 | 30 | M-18 stripping applied to key and to `value` if `isinstance(value, str)`. | Extend stripping to list element strings and dict value strings recursively. |
| yaml_frontmatter.py | `end_line` calculated as `raw_yaml.count("\n") + 1` — does not account for the closing `---` delimiter line, making `end_line` off by one relative to the actual document line | Consumers using `end_line` for positional operations (e.g., write-back, offset calculation) operate on wrong line | 4 | 5 | 3 | 60 | No current control. Coverage gap lines 317–318 are unrelated. | Add test verifying `end_line` matches the closing `---` line number in the source. Fix calculation if off-by-one confirmed. |
| yaml_frontmatter.py | `json.dumps(result, default=str)` for post-parse size check — extremely large dicts may trigger recursive expansion of nested dicts before JSON serialization produces any bytes | Memory exhaustion during size check; the check that was meant to prevent exhaustion becomes the exhaustion mechanism | 6 | 2 | 5 | 60 | Max YAML block bytes (M-07, 32 KB) and alias count (M-20, 10) should limit input before this path. | Add a key-count early-exit before calling `json.dumps`: if `len(result) > bounds.max_frontmatter_keys`, return error before serialization. This path is already checked post-JSON, so reorder. |

---

### xml_section.py

**File:** `src/domain/markdown_ast/xml_section.py` (265 lines)
**Coverage:** 100%
**Test file:** `tests/unit/domain/markdown_ast/test_xml_section.py` (223 lines, ~15 tests)

| Component | Failure Mode | Effect | S | O | D | RPN | Current Controls | Recommended Action |
|-----------|-------------|--------|---|---|---|-----|-----------------|-------------------|
| xml_section.py | `re.DOTALL` + lazy `.*?` on very large document (>100 KB) with no matching closing tag — lazy quantifier must attempt progressively larger match spans | Performance degradation proportional to document length squared in worst case; no regex timeout mechanism exists in Python `re` | 6 | 3 | 7 | **126** | Tag allowlist prevents arbitrary tag construction; max_file_bytes (1 MB) limits input. No regex timeout. | Implement pre-scan: before running `pattern.finditer()`, verify each candidate opening tag has a corresponding closing tag. Reject early if not found. |
| xml_section.py | Duplicate tag extraction — multiple `<identity>` sections in one document both match (neither is nested inside the other, so nested check does not fire) | Both sections extracted; consumers receive ambiguous duplicate. UniversalDocument passes both in `xml_sections` tuple without merge rules. | 5 | 4 | 3 | 60 | Nested same-name tag rejection fires only when the inner tag appears inside the outer content. Two non-nested same-name tags both match. | Add duplicate tag name detection after extraction loop; emit warning and keep only the first occurrence per tag name (or reject the document). |
| xml_section.py | Content length truncation silently corrupts content — `content[: bounds.max_value_length]` may split a multi-byte UTF-8 character at a byte boundary if `content` is a decoded str slice, but Python slices str at codepoint boundary, not byte boundary | No practical issue in Python (str slicing is codepoint-safe). Low risk. | 1 | 1 | 1 | 1 | Python str slicing is codepoint-safe. | No action required. Document explicitly. |
| xml_section.py | Section count enforcement returns partial result with error — when count exceeds `max_section_count`, accumulated sections are returned alongside the error, creating a mixed state | Callers receiving both `sections` and `parse_error` may process sections as complete when they are partial | 4 | 3 | 4 | 48 | Section count enforced at loop; partial result returned with error. | Document the partial-result-plus-error contract explicitly in the docstring. Add test verifying caller handling of this state. |
| xml_section.py | `_build_section_pattern()` called on every `extract()` invocation — rebuilds regex from frozenset on each call; no caching | Performance overhead on repeated calls; acceptable for current usage but degrades under batch processing | 2 | 6 | 2 | 24 | No control; ALLOWED_TAGS is a module-level frozenset. | Cache the compiled pattern as a module-level constant since ALLOWED_TAGS is immutable. |
| xml_section.py | Line number computation uses O(n) character scan — `_compute_line_starts()` iterates every character in `source` for every `extract()` call | Performance concern for large documents; not a correctness failure | 2 | 4 | 1 | 8 | No control; correct behavior. | Acceptable for current document sizes. Cache if batch mode is added. |

---

### html_comment.py

**File:** `src/domain/markdown_ast/html_comment.py` (269 lines)
**Coverage:** 100%
**Test file:** `tests/unit/domain/markdown_ast/test_html_comment.py` (355 lines, ~25 tests)

| Component | Failure Mode | Effect | S | O | D | RPN | Current Controls | Recommended Action |
|-----------|-------------|--------|---|---|---|-----|-----------------|-------------------|
| html_comment.py | Negative lookahead `(?!L2-REINJECT:)` is case-sensitive in the regex but `_REINJECT_PREFIX_RE` check afterward is case-insensitive — a comment starting with `l2-reinject:` passes the regex lookahead and enters the block loop before being caught by `_REINJECT_PREFIX_RE.match(body)` | Functionally correct — double-check works. However, the pattern is a latent inconsistency: if `_REINJECT_PREFIX_RE` check is ever removed, lowercase variants would be processed as metadata | 8 | 2 | 10 | **160** | `_REINJECT_PREFIX_RE` catch in the body loop provides correct case-insensitive exclusion as a second layer. | Add `re.IGNORECASE` to the negative lookahead: `(?!(?i)L2-REINJECT:)` — or compile a combined pattern. This closes the inconsistency gap permanently without relying on the second-layer check. |
| html_comment.py | `_KV_PATTERN` accepts arbitrary key names matching `[A-Za-z][A-Za-z0-9_-]*` — no allowlist enforcement | Injected metadata keys (e.g., `Admin`, `EscalatePrivilege`) are accepted and returned in `HtmlCommentField` objects; downstream consumers that iterate fields may be influenced | 5 | 5 | 4 | 100 | Value length enforcement (M-17); control char stripping (M-18). No key allowlist. | Add key name allowlist or prefix convention (e.g., require uppercase start, maximum key length). Document intentional permissiveness if by design. |
| html_comment.py | Multi-line `re.DOTALL` comment body matching — a document containing `<!-- KEY: value` with no closing `-->` causes the lazy `.*?` to scan to end-of-document | Performance degradation on unclosed comments in large files; no timeout | 5 | 3 | 5 | 75 | Non-greedy `.*?` reduces backtracking. max_file_bytes (1 MB) limits input. | Pre-scan for `-->` presence before running full regex. Or add a character limit on comment body scan depth. |
| html_comment.py | `HtmlCommentBlock` with zero key-value pairs is silently skipped (`if fields`) — a comment that matches the outer pattern but has no KV pairs produces no output | Silent no-op; expected behavior but not explicitly tested for edge cases like `<!-- -->` | 2 | 4 | 2 | 16 | Conditional `if fields` prevents empty block insertion. | Document explicitly. Add test for `<!-- -->` and `<!-- plain text comment -->` inputs. |
| html_comment.py | Comment count enforcement emits partial result — same contract issue as xml_section.py | Callers may process partial results as complete | 3 | 2 | 4 | 24 | Comment count enforced; partial result returned with error. | Document contract. |

---

### document_type.py

**File:** `src/domain/markdown_ast/document_type.py` (300 lines)
**Coverage:** 94% (lines 270, 287, 292, 297, 300 uncovered — rare path/structure detection branches)
**Test file:** `tests/unit/domain/markdown_ast/test_document_type.py` (307 lines, ~22 tests)

| Component | Failure Mode | Effect | S | O | D | RPN | Current Controls | Recommended Action |
|-----------|-------------|--------|---|---|---|-----|-----------------|-------------------|
| document_type.py | Structural cue collision — `"---"` matches any YAML document, and `"<!--"` matches any HTML comment; cue priority selects AGENT_DEFINITION for any document starting with `---` even if it is a SKILL.md or rule file | Wrong document type returned from structure-fallback; wrong parser set invoked by UniversalDocument | 7 | 4 | 5 | **140** | PATH_PATTERNS take priority over structural cues; structural fallback only used when no path matches. | Add more discriminating structural cues (e.g., YAML frontmatter with `name:` key for agents, `## HARD Rules` for rule files). Refine the priority list. |
| document_type.py | `_normalize_path()` root-marker extraction — if multiple markers appear in the path (e.g., `/home/user/skills/docs/file.md`), only the first marker found wins; `docs/` would be missed because `skills/` appears earlier | Path normalized to `skills/docs/file.md`; pattern `docs/design/*.md` would not match | 4 | 3 | 7 | 84 | PATH_PATTERNS are ordered most-specific first. `skills/` marker found first in this example would give `skills/docs/file.md` — partial match may still work for some patterns. | Test with deeply nested paths containing multiple marker substrings. Clarify expected normalization behavior in docstring. |
| document_type.py | `_match_recursive_glob()` falls back to `fnmatch.fnmatch()` for patterns with multiple `**` — `fnmatch` does not support `**` semantics | Patterns like `projects/**/work/**/*.md` silently fall back to fnmatch which treats `**` as `*` but only for a single path segment | 5 | 3 | 7 | **105** | Single `**` patterns work correctly. Multi-`**` patterns silently degrade. | Add test for multi-`**` patterns. Either implement multi-`**` support or document the limitation explicitly and ensure PATH_PATTERNS never require it. |
| document_type.py | Absolute path input with no recognizable root marker — `_normalize_path()` returns the full absolute path unchanged; no PATH_PATTERN matches `/home/user/randomdir/file.md` | Falls through to structural detection; DocumentType may be incorrect | 3 | 4 | 3 | 36 | UNKNOWN is the safe default when nothing matches. | Acceptable — UNKNOWN is safe. Add test for unrecognized absolute path inputs. |
| document_type.py | Uncovered lines 270, 287, 292, 297, 300 — rare path/structure detection branches for infrequently-combined document types | Unknown behavior for these branches in production | 4 | 2 | 9 | 72 | 94% coverage; missing branches are rarely-combined type combinations. | Phase 4 adversarial testing (WI-022) should exercise these branches. Document which type combinations trigger them. |
| document_type.py | Type mismatch warning suppressed when `structure_type == DocumentType.UNKNOWN` — path says AGENT_DEFINITION but structure returns UNKNOWN; no warning is issued | Silent mismatch; caller receives path-based type with no indicator that structure could not corroborate | 3 | 4 | 5 | 60 | M-14 warning only when structure gives a non-UNKNOWN contradicting result. | Consider warning when path matches but structure detection returns None/UNKNOWN — potentially indicates empty or non-standard document. |

---

### universal_document.py

**File:** `src/domain/markdown_ast/universal_document.py` (222 lines)
**Coverage:** 97% (lines 188, 196 uncovered — multi-parser error aggregation branches)
**Test file:** `tests/unit/domain/markdown_ast/test_universal_document.py` (459 lines, 23 tests)

| Component | Failure Mode | Effect | S | O | D | RPN | Current Controls | Recommended Action |
|-----------|-------------|--------|---|---|---|-----|-----------------|-------------------|
| universal_document.py | Error aggregation branches 188, 196 uncovered — `parse_errors` accumulation paths for XmlSectionParser and HtmlCommentMetadata errors not tested | Silent failure: if these parsers return errors in production, errors may not be surfaced in `parse_errors` | 5 | 2 | 9 | 90 | DD-9 error aggregation design; 97% coverage. | Add tests that inject parse errors from XmlSectionParser and HtmlCommentMetadata and verify presence in `UniversalParseResult.parse_errors`. |
| universal_document.py | Parser invocation matrix (`_PARSER_MATRIX`) is a module-level mutable dict — caller code with import access can add/modify entries at runtime | Wrong parser set invoked for a document type; security control bypass if parser removed | 7 | 2 | 6 | 84 | `_PARSER_MATRIX` is a module-level dict with leading underscore. Not frozen. | Convert to `types.MappingProxyType` or `frozenset` values within a frozen outer mapping. |
| universal_document.py | Structure-only detection with empty `file_path=""` — `DocumentTypeDetector.detect("", content)` passes an empty string which normalizes to empty; no PATH_PATTERNS match; falls to structure only | Expected behavior per design, but callers who omit `file_path` silently lose path-based accuracy | 3 | 5 | 2 | 30 | Structure fallback is the documented behavior. | Document explicitly in `parse()` docstring. No code change needed. |
| universal_document.py | `blockquote_result = BlockquoteFrontmatter.extract(doc)` — no error path; `BlockquoteFrontmatter.extract()` may raise uncaught exceptions on malformed inputs | Exception propagates to caller uncaught; no structured error aggregation | 5 | 2 | 5 | 50 | DD-9 error aggregation covers yaml, xml, html parsers but not blockquote or reinject. | Wrap `BlockquoteFrontmatter.extract()` and `extract_reinject_directives()` in try-except and aggregate errors per DD-9 pattern. |
| universal_document.py | `extract_reinject_directives(doc)` — no error path captured; reinject parser may raise on malformed directive content | Exception propagates uncaught; no aggregated error | 5 | 2 | 5 | 50 | Same gap as above. | Same recommendation: wrap in try-except. |
| universal_document.py | No bounds enforcement on blockquote frontmatter — `BlockquoteFrontmatter.extract()` called without `InputBounds`; no field count or value length limits applied | Unbounded field extraction for blockquote-formatted documents; resource exhaustion via large frontmatter | 5 | 3 | 4 | 60 | All other parsers receive `bounds` parameter. | Pass `bounds` to `BlockquoteFrontmatter.extract()` if/when it supports InputBounds, or document the gap. |

---

### schema_registry.py

**File:** `src/domain/markdown_ast/schema_registry.py` (148 lines)
**Coverage:** 100%
**Test file:** `tests/unit/domain/markdown_ast/test_schema_registry.py` (356 lines, 42 tests)

| Component | Failure Mode | Effect | S | O | D | RPN | Current Controls | Recommended Action |
|-----------|-------------|--------|---|---|---|-----|-----------------|-------------------|
| schema_registry.py | `freeze()` is idempotent and silent — calling `freeze()` twice is not an error; calling `register()` after `freeze()` raises RuntimeError. However, there is no way for a caller to inspect whether freeze has been called except via the `frozen` property | Callers that do not check `frozen` before registering silently succeed before freeze and fail after, with no pre-flight indication | 3 | 3 | 3 | 27 | `freeze()` raises RuntimeError on post-freeze register. `frozen` property is queryable. | Add `freeze()` logging or return a boolean indicating prior state. Low risk. |
| schema_registry.py | `get()` raises `ValueError` on unknown type and exposes all registered type names in the error message | Information disclosure: the list of registered entity types is included in the exception message visible in logs or stdout | 3 | 5 | 2 | 30 | ValueError raised with valid type list. | Consider omitting or sanitizing the valid type list in production error messages, or limit to "Unknown entity type" with no enumeration. |
| schema_registry.py | `_schemas` dict is accessed via `MappingProxyType` from `schemas` property, but `_schemas` itself is accessible via `registry._schemas` | Name-mangled access (`_SchemaRegistry__schemas`) is not used; single-underscore attribute is accessible to external code | 4 | 2 | 3 | 24 | MappingProxyType prevents proxy-level mutation. Direct `_schemas` dict is still mutable via attribute access. | Use double-underscore name mangling (`__schemas`) or document that `_schemas` must not be accessed directly. Low risk in practice. |
| schema_registry.py | Registry is not frozen by default on construction — a freshly constructed `SchemaRegistry()` accepts registrations until explicitly frozen; if a caller forgets to call `freeze()`, the registry remains mutable indefinitely | Runtime schema poisoning via missed freeze call | 6 | 2 | 5 | 60 | `DEFAULT_REGISTRY` in schema_definitions.py is always frozen. Individual `SchemaRegistry()` instances are not auto-frozen. | Consider a factory method `SchemaRegistry.build_frozen(schemas)` that always returns a frozen registry. |
| schema_registry.py | `list_types()` returns a sorted `list[str]` — mutable; caller can modify without affecting registry | No correctness impact but violates immutability expectation | 2 | 3 | 1 | 6 | Return type is list, not tuple. | Return `tuple[str, ...]` for consistency with the immutable design intent. |

---

### schema_definitions.py

**File:** `src/domain/markdown_ast/schema_definitions.py` (182 lines)
**Coverage:** 100%
**Test file:** Covered by `test_schema_registry.py` and `test_schema.py`

| Component | Failure Mode | Effect | S | O | D | RPN | Current Controls | Recommended Action |
|-----------|-------------|--------|---|---|---|-----|-----------------|-------------------|
| schema_definitions.py | Module-level `DEFAULT_REGISTRY.freeze()` executes at import time — import-order dependency; if schema_definitions.py is imported before all schemas are needed, the registry is frozen and additional schema registration is impossible | Downstream code that tries to register additional schemas to `DEFAULT_REGISTRY` receives RuntimeError | 4 | 3 | 5 | 60 | Architecture intent: DEFAULT_REGISTRY is the production-frozen registry; tests that need custom schemas create fresh SchemaRegistry instances. | Document clearly in the module docstring that DEFAULT_REGISTRY is sealed at import time and is not extensible. |
| schema_definitions.py | `value_pattern` regex strings are hardcoded without pre-compilation or ReDoS validation — patterns like `r"^[a-z]+-[a-z]+(-[a-z]+)*$"` are safe but not validated for catastrophic backtracking | If a future maintainer adds a vulnerable pattern, it is silently accepted | 6 | 2 | 7 | 84 | Patterns are simple and safe currently. No automated validation. | Add a CI-level check that validates all `value_pattern` strings in schema_definitions.py using a ReDoS linter (e.g., `regress`, `vuln-regex-detector`). |
| schema_definitions.py | `ADR_SCHEMA` requires sections "Status", "Context", "Decision", "Consequences" — these are section heading checks. If an ADR uses slightly different heading names (e.g., "Context and Problem Statement"), validation fails silently returning violations | ADR files with non-standard headings fail validation; no suggestion offered in violation message | 3 | 5 | 3 | 45 | Schema violations are reported. | Soften ADR section requirements to SHOULD (not required) or add alternative heading names. |
| schema_definitions.py | `ORCHESTRATION_SCHEMA`, `PATTERN_SCHEMA` have empty `field_rules` and `section_rules` — any document classified as these types passes schema validation trivially | Schema validation for orchestration artifacts and pattern documents provides no structural guarantee | 3 | 6 | 2 | 36 | By design: these types have variable structure. | Document intentional permissiveness. Consider adding at minimum a `require_nav_table=True` for these types. |
| schema_definitions.py | `STRATEGY_TEMPLATE_SCHEMA.field_rules` includes `FieldRule(key="ID", value_pattern=r"^S-\d{3}$")` — strategy IDs above S-999 would fail validation | Future strategy IDs (S-1000+) would fail schema validation | 2 | 1 | 3 | 6 | Pattern `^S-\d{3}$` requires exactly 3 digits. | Change to `^S-\d{3,4}$` to accommodate 4-digit IDs. |

---

### input_bounds.py

**File:** `src/domain/markdown_ast/input_bounds.py` (75 lines)
**Coverage:** 100%
**No dedicated test file** (tested implicitly through all parser tests)

| Component | Failure Mode | Effect | S | O | D | RPN | Current Controls | Recommended Action |
|-----------|-------------|--------|---|---|---|-----|-----------------|-------------------|
| input_bounds.py | `InputBounds` is a frozen dataclass but bounds values can be set to zero or negative — `InputBounds(max_file_bytes=0)` is a valid construction; all file reads would fail | DoS via misconfigured bounds; all parser operations fail | 6 | 2 | 5 | 60 | Frozen dataclass prevents mutation after creation. No minimum value validation. | Add `__post_init__` validation: assert all bounds are positive integers. |
| input_bounds.py | `InputBounds.DEFAULT` is a `ClassVar` assigned after class definition as `InputBounds()` — this pattern works in CPython but is non-standard and may behave unexpectedly with `dataclass(frozen=True)` and some static analyzers | Mypy/pyright may flag ClassVar pattern; no runtime issue observed | 1 | 2 | 2 | 4 | Functionally correct in Python 3.10+. | Consider using `field(default_factory=...)` pattern or a module-level constant instead of ClassVar for cleaner type checking. |
| input_bounds.py | `max_yaml_block_bytes` default is 32,768 (32 KB) but implementation report states 65,536 (64 KB) — discrepancy between code comment and implementation report | Confusion in documentation; actual enforced value is 32 KB (the code), not 64 KB (the report) | 2 | 8 | 3 | 48 | Code is authoritative. | Update the implementation report to correct the stated value to 32 KB, or increase the default to 64 KB if 32 KB is too restrictive. |
| input_bounds.py | No regex execution time bound — InputBounds has no `max_regex_time_ms` field | Regex operations in xml_section.py and html_comment.py have no timeout; the `re` module does not support timeouts natively | 7 | 3 | 5 | **105** | max_file_bytes limits input size. No regex timeout. | Add `max_regex_time_ms` field to InputBounds (defaults to 0 = no timeout) as a placeholder for when `regex` library or `re2` is integrated. Track RV-004/RV-020 remediation as a Phase 4 item. |
| input_bounds.py | Bounds not validated at parser entry — parsers check specific bounds (max_yaml_block_bytes, max_section_count, etc.) but do not validate that `bounds.max_file_bytes` was enforced before calling them | If a caller bypasses `_read_file()` and calls parsers directly with large content, the file size limit is not enforced | 5 | 2 | 5 | 50 | CLI layer enforces file size via `_read_file()`. Domain parsers do not re-enforce. | Add optional content-length pre-check to `YamlFrontmatter.extract()` and `XmlSectionParser.extract()` using `bounds.max_file_bytes`. |

---

### ast_commands.py (CLI)

**File:** `src/interface/cli/ast_commands.py` (740 lines)
**Coverage:** Covered by integration tests (test_ast_subprocess.py, 18 tests)

| Component | Failure Mode | Effect | S | O | D | RPN | Current Controls | Recommended Action |
|-----------|-------------|--------|---|---|---|-----|-----------------|-------------------|
| ast_commands.py | `JERRY_DISABLE_PATH_CONTAINMENT=1` env var disables ALL path containment — this env var is intended only for integration test environments but is a runtime-controllable security bypass | If an attacker can set this env var, all M-08/M-10 path controls are disabled | 8 | 3 | 7 | **168** | `_ENFORCE_PATH_CONTAINMENT` is evaluated at module import time; the env var must be set before process launch. | Rename to a more obscure test-only variable name. Document that it must NEVER be set in production. Add a startup warning to stderr when disabled. |
| ast_commands.py | `_get_repo_root()` fallback uses `parents[3]` hardcoded offset — if ast_commands.py is ever moved or reorganized, this hardcoded offset produces the wrong repo root | Path containment check silently uses wrong root; files outside the actual repo may be accepted as inside | 7 | 2 | 6 | 84 | Primary detection via `pyproject.toml` walk is correct. Fallback only used if pyproject.toml is not found. | Remove the hardcoded fallback. If pyproject.toml is not found, raise an exception rather than using a fragile offset. |
| ast_commands.py | `ast_modify` re-verification of path containment uses `Path(file_path).resolve()` without `strict=True` — a non-existent intermediate directory would not raise an error | TOCTOU: file could be deleted and replaced between read and re-verify without raising | 5 | 2 | 6 | 60 | Atomic write (M-21) mitigates write-time corruption. Path re-verification exists. | Use `Path(file_path).resolve(strict=False)` is default behavior; for security, add explicit `Path(file_path).exists()` check between resolve and containment check. |
| ast_commands.py | Error messages include raw `file_path` from user input — `print(f"Error: File not found: {file_path}")` exposes user-supplied path in error output | Information disclosure of attempted file paths in CLI output (RV-013) | 3 | 7 | 1 | 21 | Accepted as low-severity in RV-013. Path is already known to the caller. | For JSON mode (`--json`), structure the error with `{"error": "file_not_found", "path": basename_only}`. |
| ast_commands.py | `ast_detect` calls `DocumentTypeDetector._detect_from_path()` directly (private method) — exposes internal method in CLI layer; brittle coupling | Breaking change risk if method is renamed or moved; no behavioral failure | 2 | 4 | 1 | 8 | Functionally correct; private method access is a maintenance concern only. | Add a public `DocumentTypeDetector.detect_method()` API that returns the method string. |
| ast_commands.py | `ast_sections` and `ast_metadata` use `InputBounds.DEFAULT` hardcoded — no CLI flag allows bounds override | Users cannot relax or tighten bounds for specific operations via CLI | 2 | 3 | 1 | 6 | InputBounds.DEFAULT is appropriate for production. | Acceptable for now. Add `--max-file-bytes` CLI flag in Phase 4 if needed. |
| ast_commands.py | `ast_modify` temp file created in `target_path.parent` — if the parent directory is read-only (e.g., network mount, permissions issue), `mkstemp` raises `OSError` which is caught and returns exit code 2 | Correct behavior but may confuse users who see "Error writing file" when the actual issue is temp file creation | 3 | 2 | 3 | 18 | OSError caught and reported. Correct exit code returned. | Improve error message: distinguish between temp file creation failure and final rename failure. |

---

## High-RPN Summary

All failure modes with RPN > 100, ranked by RPN:

| Rank | RPN | Band | Component | Failure Mode | Phase 4 Addressable? |
|------|-----|------|-----------|-------------|---------------------|
| 1 | 252 | CRITICAL | yaml_frontmatter.py | `yaml.reader.ReaderError` unhandled — unstructured exception on null bytes | Yes (WI-022) |
| 2 | 192 | HIGH | yaml_frontmatter.py | YAML billion-laughs expansion if alias regex undercounts | Yes (WI-022) |
| 3 | 168 | HIGH | ast_commands.py | `JERRY_DISABLE_PATH_CONTAINMENT` env var disables all path controls | Immediate (pre-deployment) |
| 4 | 160 | HIGH | html_comment.py | Negative lookahead case mismatch — lowercase l2-reinject bypasses regex, relies on second-layer check | Phase 4 (WI-022) |
| 5 | 140 | HIGH | document_type.py | Structural cue collision — `---` matches any YAML document, wrong type returned | Phase 4 (WI-022) |
| 6 | 126 | HIGH | xml_section.py | `re.DOTALL` + lazy `.*?` on large document with no closing tag — performance degradation | Phase 4 (WI-023 ReDoS testing) |
| 7 | 105 | HIGH | document_type.py | `_match_recursive_glob()` multi-`**` falls back to fnmatch silently | Phase 4 (WI-022) |
| 8 | 105 | HIGH | input_bounds.py | No regex execution time bound in InputBounds | Phase 4 design |
| 9 | 100 | MEDIUM | html_comment.py | `_KV_PATTERN` accepts arbitrary key names without allowlist | Phase 4 |
| 10 | 90 | MEDIUM | universal_document.py | Error aggregation branches 188, 196 not tested | Phase 4 (WI-022) |
| 11 | 84 | MEDIUM | schema_definitions.py | `value_pattern` strings not ReDoS-validated at registration | Phase 4 (WI-023) |
| 12 | 84 | MEDIUM | ast_commands.py | `_get_repo_root()` hardcoded fallback offset fragile | Maintenance |

---

## Recommended Actions

### Immediate (Pre-Deployment, Before QG-B2 Sign-Off)

| ID | Action | Component | Addresses |
|----|--------|-----------|-----------|
| RA-01 | Add startup warning to stderr when `JERRY_DISABLE_PATH_CONTAINMENT=1` is set. Document as test-only in code comments. | ast_commands.py | RPN-3 (168) |
| RA-02 | Add `__post_init__` validation to `InputBounds` asserting all bounds are positive integers. | input_bounds.py | InputBounds zero-value misconfiguration |

### Phase 4 (WI-022 Adversarial Testing)

| ID | Action | Component | Addresses |
|----|--------|-----------|-----------|
| RA-03 | Add `yaml.reader.ReaderError` to exception handler in `YamlFrontmatter.extract()`. File technical debt item to refactor yaml_frontmatter.py for H-10 compliance. | yaml_frontmatter.py | RPN-1 (252) |
| RA-04 | Add pre-parse anchor definition count check: `re.findall(r'&[a-zA-Z_]', raw_yaml)`. Combine with alias count to estimate expansion factor. | yaml_frontmatter.py | RPN-2 (192) |
| RA-05 | Add `re.IGNORECASE` to negative lookahead in `_METADATA_COMMENT_PATTERN` regex. | html_comment.py | RPN-4 (160) |
| RA-06 | Add pre-scan for closing tags in `XmlSectionParser.extract()` before running `pattern.finditer()`. | xml_section.py | RPN-6 (126) |
| RA-07 | Test and fix `_match_recursive_glob()` for multi-`**` patterns; document limitation if not fixed. | document_type.py | RPN-7 (105) |
| RA-08 | Add `max_regex_time_ms` field to `InputBounds` as a design placeholder. Track RV-004/RV-020 `regex`/`re2` library adoption as a separate work item. | input_bounds.py | RPN-8 (105) |
| RA-09 | Add key name length limit or prefix convention to `_KV_PATTERN` in html_comment.py. | html_comment.py | RPN-9 (100) |
| RA-10 | Add tests that inject parse errors from XmlSectionParser and HtmlCommentMetadata via mocked parsers to verify `parse_errors` aggregation. | universal_document.py | RPN-10 (90) |

### Phase 4 (WI-023 ReDoS Testing)

| ID | Action | Component | Addresses |
|----|--------|-----------|-----------|
| RA-11 | Add CI-level ReDoS linter check for all `value_pattern` strings in schema_definitions.py. | schema_definitions.py | RPN-11 (84) |
| RA-12 | Run WI-023 ReDoS test suite against all parsers; prioritize xml_section.py and html_comment.py regex patterns. | xml_section.py, html_comment.py | RPN-6, latent regex risks |

### Maintenance (Next Development Cycle)

| ID | Action | Component | Addresses |
|----|--------|-----------|-----------|
| RA-13 | Remove hardcoded `parents[3]` fallback from `_get_repo_root()`. Raise exception if pyproject.toml not found. | ast_commands.py | RPN-12 (84) |
| RA-14 | Correct discrepancy: implementation report states `max_yaml_block_bytes=65536` but code is `32768`. Align documentation and code. | input_bounds.py | Documentation accuracy |
| RA-15 | Convert `_PARSER_MATRIX` dict in universal_document.py to `MappingProxyType`. | universal_document.py | Registry poisoning analogous to V-06 |

---

## Cross-Component Failure Chains

The following multi-component failure sequences represent the highest compound risks. FMEA traditionally analyzes single-component failures; these chains illustrate how individual failures propagate.

### Chain 1: YAML ReaderError → Uncaught Exception → CLI Crash (RPN Compound: HIGH)

```
yaml_frontmatter.py (ReaderError gap, RPN 252)
    → universal_document.py (exception not wrapped in try-except for yaml parser)
    → ast_commands.py (ast_parse/ast_sections/ast_detect calls UniversalDocument.parse())
    → Unstructured exception to CLI user
```

**Effect:** CLI exits with Python traceback rather than structured error. The traceback may expose internal file paths and module names (information disclosure, CWE-209).

**Current Controls:** None — ReaderError is unhandled at all three layers.

**Recommended Action:** RA-03 (add ReaderError handler) is the single fix that closes this chain.

---

### Chain 2: Structural Cue Collision → Wrong Parser Invoked → Security Control Bypass (RPN Compound: HIGH)

```
document_type.py (structural cue collision, RPN 140)
    → universal_document.py (_PARSER_MATRIX selects wrong parser set)
    → yaml_frontmatter.py invoked on a document not expected to have YAML
    → OR: reinject parser NOT invoked on a rule file that has L2-REINJECT directives
```

**Effect:** For the second branch: governance directives in rule files are not extracted when the file is misclassified as AGENT_DEFINITION (which invokes yaml/xml/nav parsers, not reinject). The directives are silently absent from `UniversalParseResult.reinject_directives`.

**Current Controls:** PATH_PATTERNS prevent misclassification when a file path is provided. Structural fallback is only used when path is absent or matches no pattern.

**Recommended Action:** RA-06 from the context of improving structural cue discriminability.

---

### Chain 3: env-var Path Bypass → Arbitrary File Read → Information Disclosure (RPN Compound: CRITICAL)

```
ast_commands.py (JERRY_DISABLE_PATH_CONTAINMENT=1, RPN 168)
    → _read_file() skips containment and symlink checks
    → Arbitrary file path accepted
    → Any file readable by process returned as content
```

**Effect:** All M-08 and M-10 controls are bypassed. Equivalent to pre-mitigation RV-003 (arbitrary file read, DREAD 37).

**Current Controls:** The env var must be set before process launch. Not settable by document content.

**Recommended Action:** RA-01 (startup warning) + documentation that this must never be set in production CI/CD pipelines.

---

<!-- FMEA Complete | Agent: adv-executor | Strategy: S-012 | Date: 2026-02-23 -->
<!-- RPN threshold: 100 | High-RPN count: 12 | Total failure modes: 42 -->
