# Implementation Plan: Universal Markdown Parser

<!-- ENG-LEAD-001 | ENGAGEMENT: ENG-0001 | PROJECT: PROJ-005 | CRITICALITY: C4 -->
<!-- DATE: 2026-02-23 | AUTHOR: eng-lead-001 | PHASE: ENG Phase 2 -->

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary (L0)](#executive-summary-l0) | Timeline, key decisions, critical path |
| [Implementation Phases](#implementation-phases) | Phase structure and parallelism opportunities |
| [Dependency Graph](#dependency-graph) | Visual dependency relationships between work items |
| [Work Item Catalog](#work-item-catalog) | WI-001 through WI-025 ordered by phase and dependency |
| [Phase 0: P0 Prerequisites](#phase-0-p0-prerequisites) | Blocking defect remediation and security foundations |
| [Phase 1: Core Parsers](#phase-1-core-parsers) | New parser implementations |
| [Phase 2: Integration and Schema](#phase-2-integration-and-schema) | Document type detection, schema extension, universal facade |
| [Phase 3: CLI and Hardening](#phase-3-cli-and-hardening) | CLI extensions, security hardening, existing code fixes |
| [Phase 4: Testing and Validation](#phase-4-testing-and-validation) | Test suites, adversarial testing, golden-file regression |
| [Critical Path Analysis](#critical-path-analysis) | Longest dependency chain and schedule risk |
| [Standards Compliance Matrix](#standards-compliance-matrix) | Per-work-item HARD rule coverage |
| [Risk Register](#risk-register) | Implementation risks and mitigations |
| [Strategic Implications (L2)](#strategic-implications-l2) | Technical debt, maintainability, migration safety |

---

## Executive Summary (L0)

This implementation plan decomposes the 7 required enhancements (RE-001 through RE-007) from ADR-PROJ005-003 into **25 ordered work items** across **5 phases** (Phase 0 through Phase 4). The plan addresses 24 threat model mitigations (M-01 through M-24), 7 pre-existing vulnerabilities (V-01 through V-07), and enforces compliance with 12 HARD rules.

**Key decisions:**

1. **P0 prerequisites block everything.** The `FrontmatterField` mutability defect (V-05), `InputBounds` configuration class, and schema registry `freeze()` must be completed before any new parser work begins. These are not optional -- they establish the immutability and security foundations the entire architecture depends on.

2. **Core parsers can be developed in parallel.** Once Phase 0 completes, `YamlFrontmatter` (RE-001), `XmlSectionParser` (RE-002), and `HtmlCommentMetadata` (RE-003) have no dependencies on each other and can be developed simultaneously.

3. **Integration is sequential.** `DocumentTypeDetector` (RE-004) must complete before `UniversalDocument` (RE-007). Schema extension (RE-005) can proceed in parallel with document type detection. CLI extensions (RE-006) depend on all domain work completing.

4. **No new dependencies required.** The existing dependency stack (PyYAML, markdown-it-py, mdformat, jsonschema) is sufficient for all 7 enhancements. See the companion dependency assessment for full analysis.

**Timeline estimate:** 5 phases, with Phases 1a/1b/1c parallelizable. Critical path runs through Phase 0 -> Phase 1a (YamlFrontmatter, highest complexity) -> Phase 2b (UniversalDocument) -> Phase 3a (CLI) -> Phase 4 (Testing).

**Critical path complexity:** The critical path contains 4 Large (L) work items and 3 Medium (M) work items, with an estimated total of 18-22 files affected (5 new domain files, 3 modified domain files, 1 modified CLI file, 9+ new test files).

---

## Implementation Phases

| Phase | Name | Work Items | Parallelism | Gate |
|-------|------|-----------|-------------|------|
| **Phase 0** | P0 Prerequisites | WI-001 through WI-004 | Sequential (WI-001 first, then WI-002/WI-003/WI-004 parallel) | All existing tests pass; V-05, V-06 remediated |
| **Phase 1** | Core Parsers | WI-005 through WI-010 | WI-005+WI-006 parallel, WI-007+WI-008 parallel, WI-009+WI-010 parallel | Each parser has unit tests passing |
| **Phase 2** | Integration + Schema | WI-011 through WI-016 | WI-011/WI-012 parallel, then WI-013 sequential; WI-014/WI-015/WI-016 parallel with WI-011 | UniversalDocument.parse() returns correct results for all 10 document types |
| **Phase 3** | CLI + Hardening | WI-017 through WI-021 | WI-017 sequential; WI-018/WI-019/WI-020/WI-021 parallel | CLI commands functional; security mitigations verified |
| **Phase 4** | Testing + Validation | WI-022 through WI-025 | WI-022/WI-023 parallel, then WI-024/WI-025 sequential | 90% line coverage; all adversarial tests pass; golden-file regression clean |

---

## Dependency Graph

```
WI-001 (FrontmatterField frozen)
    |
    +---> WI-002 (InputBounds)
    |         |
    |         +---> WI-005 (YamlFrontmatter parser)
    |         |         |
    |         |         +---> WI-006 (YamlFrontmatter tests)
    |         |
    |         +---> WI-007 (XmlSectionParser)
    |         |         |
    |         |         +---> WI-008 (XmlSectionParser tests)
    |         |
    |         +---> WI-009 (HtmlCommentMetadata)
    |         |         |
    |         |         +---> WI-010 (HtmlCommentMetadata tests)
    |         |
    |         +---> WI-011 (DocumentTypeDetector)
    |                   |
    |                   +---> WI-013 (UniversalDocument facade)
    |                             |
    |                             +---> WI-017 (CLI extensions)
    |                                       |
    |                                       +---> WI-024 (Golden-file regression)
    |                                       +---> WI-025 (Integration tests)
    |
    +---> WI-003 (SchemaRegistry freeze)
    |         |
    |         +---> WI-014 (New schemas - agent_definition)
    |         +---> WI-015 (New schemas - remaining types)
    |         +---> WI-016 (New schema tests)
    |
    +---> WI-004 (Banned API lint rule)

WI-012 (Document type detection tests) depends on WI-011
WI-018 (Path containment M-08) depends on Phase 0
WI-019 (L2-REINJECT trust M-22) depends on Phase 0
WI-020 (Write-back TOCTOU M-21) depends on Phase 0
WI-021 (CI grep check M-04b) depends on Phase 0
WI-022 (Adversarial test suite) depends on WI-005, WI-007, WI-009
WI-023 (ReDoS test suite) depends on WI-014, WI-015
```

---

## Work Item Catalog

| WI | Phase | RE | Description | Files | Size | Security | Depends On |
|----|-------|----|-------------|-------|------|----------|------------|
| WI-001 | 0 | -- | FrontmatterField `frozen=True` migration | 2 | S | V-05 | -- |
| WI-002 | 0 | -- | InputBounds configuration class | 1 new | M | M-05/06/07/16/17/20 | WI-001 |
| WI-003 | 0 | -- | SchemaRegistry with `freeze()` | 1 mod | M | T-SV-04/05, M-23 | WI-001 |
| WI-004 | 0 | -- | Banned API lint rule (`yaml.load`) | 1 mod | S | T-YF-07, M-01 | -- |
| WI-005 | 1 | RE-001 | YamlFrontmatter parser | 1 new | L | T-YF-01..10, M-07/19/20/23/24 | WI-002 |
| WI-006 | 1 | RE-001 | YamlFrontmatter unit tests | 1 new | L | M-04a | WI-005 |
| WI-007 | 1 | RE-002 | XmlSectionParser | 1 new | M | T-XS-01..08, M-11/15 | WI-002 |
| WI-008 | 1 | RE-002 | XmlSectionParser unit tests | 1 new | M | -- | WI-007 |
| WI-009 | 1 | RE-003 | HtmlCommentMetadata parser | 1 new | M | T-HC-01..06, M-13 | WI-002 |
| WI-010 | 1 | RE-003 | HtmlCommentMetadata unit tests | 1 new | M | -- | WI-009 |
| WI-011 | 2 | RE-004 | DocumentTypeDetector + DocumentType enum | 1 new | M | T-DT-01..05, M-14 | WI-002 |
| WI-012 | 2 | RE-004 | DocumentTypeDetector tests | 1 new | M | -- | WI-011 |
| WI-013 | 2 | RE-007 | UniversalDocument facade | 1 new | L | DD-3, DD-9 | WI-005, WI-007, WI-009, WI-011 |
| WI-014 | 2 | RE-005 | Schema extension: agent_definition, skill_definition | 1 mod | M | T-SV-01..03, M-12 | WI-003 |
| WI-015 | 2 | RE-005 | Schema extension: remaining 4 new types | 1 mod | M | T-SV-03, M-12 | WI-003 |
| WI-016 | 2 | RE-005 | Schema extension tests | 1 new | M | -- | WI-014, WI-015 |
| WI-017 | 3 | RE-006 | CLI extensions (--type, sections, metadata, detect) | 1 mod | L | -- | WI-013 |
| WI-018 | 3 | -- | Path containment in CLI (M-08, M-10) | 1 mod | S | T-DT-04/05, M-08/10 | Phase 0 |
| WI-019 | 3 | -- | L2-REINJECT trusted path whitelist (M-22) | 1 mod | M | T-HC-04/07, M-22 | Phase 0 |
| WI-020 | 3 | -- | Write-back TOCTOU mitigation (M-21) | 1 mod | S | T-WB-01, M-21 | Phase 0 |
| WI-021 | 3 | -- | CI grep check for banned YAML APIs (M-04b) | 1 new | S | T-YF-07, M-04b | WI-004 |
| WI-022 | 4 | -- | Adversarial test suite (attack catalog A-01..A-11) | 1 new | L | All HIGH+ threats | WI-005, WI-007, WI-009 |
| WI-023 | 4 | -- | ReDoS test suite for schema value_patterns (M-12) | 1 new | M | T-SV-03, M-12 | WI-014, WI-015 |
| WI-024 | 4 | -- | Golden-file regression test suite | 1 new | L | PM-001-B1 | WI-013, WI-017 |
| WI-025 | 4 | -- | Integration tests and coverage verification | 1 new | M | -- | WI-017 |

**Size key:** S = Small (1-2 files, <100 lines changed), M = Medium (1-3 files, 100-300 lines), L = Large (2-4 files, 300-600 lines)

---

## Phase 0: P0 Prerequisites

> These work items BLOCK all subsequent phases. They remediate pre-existing defects and establish security foundations.

### WI-001: FrontmatterField `frozen=True` Migration

| Attribute | Value |
|-----------|-------|
| **Description** | Migrate `FrontmatterField` at `frontmatter.py:54` from `@dataclass` to `@dataclass(frozen=True)`. Verify no code mutates `FrontmatterField` attributes. Run existing test suite to confirm no regressions. |
| **Files Affected** | `src/domain/markdown_ast/frontmatter.py` (modify line 54), `tests/unit/domain/markdown_ast/test_frontmatter.py` (add frozen verification test) |
| **Complexity** | S |
| **Security** | Remediates V-05 (pre-existing mutable domain object). Closes Trust Boundary Zone 4 gap documented in trust boundaries diagram. |
| **Threats Mitigated** | Analogous to T-YF-02 (CWE-20) -- mutable domain objects enable post-parse tampering |
| **HARD Rules** | H-10 (one class per file -- no structural change), H-11 (type hints preserved), H-20 (add regression test) |
| **Depends On** | None |
| **Verification** | `uv run pytest tests/unit/domain/markdown_ast/test_frontmatter.py` passes. Grep for `field.key =`, `field.value =` returns zero hits outside test_frozen assertions. |
| **Acceptance Criteria** | 1. `@dataclass(frozen=True)` on `FrontmatterField`. 2. No existing tests break. 3. New test verifies `FrozenInstanceError` on attribute assignment attempt. |

### WI-002: InputBounds Configuration Class

| Attribute | Value |
|-----------|-------|
| **Description** | Create `src/domain/markdown_ast/input_bounds.py` with the `InputBounds` frozen dataclass per DD-8 in the ADR. Centralized, immutable resource limits used by all parsers. |
| **Files Affected** | `src/domain/markdown_ast/input_bounds.py` (NEW), `src/domain/markdown_ast/__init__.py` (add export), `tests/unit/domain/markdown_ast/test_input_bounds.py` (NEW) |
| **Complexity** | M |
| **Security** | Implements M-05 (max file bytes), M-06 (max nesting depth), M-07 (max YAML block bytes), M-16 (max field/section/comment counts), M-17 (max value length), M-20 (max YAML result bytes, max alias count) |
| **Threats Mitigated** | T-YF-05 (CWE-400), T-YF-06 (CWE-776), T-XS-04 (CWE-400), T-HC-04-DoS (CWE-400) |
| **HARD Rules** | H-07 (domain layer -- no external imports), H-10 (one class per file), H-11 (type hints + docstrings) |
| **Depends On** | WI-001 (establishes frozen dataclass pattern confirmation) |
| **Verification** | Unit tests verify: frozen immutability, DEFAULT singleton, all default values match ADR specification, custom bounds construction. |
| **Acceptance Criteria** | 1. `InputBounds` is `@dataclass(frozen=True)`. 2. `InputBounds.DEFAULT` singleton exists. 3. All 10 configurable bounds present with documented defaults. 4. Tests verify frozen behavior. |

### WI-003: SchemaRegistry with `freeze()` and Collision Detection

| Attribute | Value |
|-----------|-------|
| **Description** | Refactor `schema.py` to replace the mutable `_SCHEMA_REGISTRY` dict (line 530) with a `SchemaRegistry` class supporting `register()`, `freeze()`, `get()`, `list_types()`, and a `schemas` property returning `MappingProxyType`. Existing `get_entity_schema()` delegates to the default registry. Existing schemas registered and frozen at module load. |
| **Files Affected** | `src/domain/markdown_ast/schema.py` (modify), `tests/unit/domain/markdown_ast/test_schema.py` (add registry tests) |
| **Complexity** | M |
| **Security** | Remediates V-06 (mutable module-level dict). Implements collision detection (T-SV-04, CWE-694) and freeze for runtime poisoning prevention (T-SV-05, CWE-915). |
| **Threats Mitigated** | T-SV-04 (CWE-694), T-SV-05 (CWE-915) |
| **HARD Rules** | H-07, H-10 (SchemaRegistry is a new class in existing file alongside EntitySchema -- acceptable as the file's concern is schema infrastructure), H-11 |
| **Depends On** | WI-001 |
| **Verification** | Tests verify: `register()` before freeze succeeds; `register()` after freeze raises `RuntimeError`; duplicate key raises `ValueError`; `schemas` returns `MappingProxyType`; existing `get_entity_schema()` still works for all 6 entity types. |
| **Acceptance Criteria** | 1. `SchemaRegistry` class with `register()`, `freeze()`, `get()`, `list_types()`, `schemas`. 2. Module-level registry frozen after registration. 3. `get_entity_schema()` backward compatible. 4. All existing schema tests pass. |

### WI-004: Banned API Lint Rule for Unsafe YAML

| Attribute | Value |
|-----------|-------|
| **Description** | Add a ruff custom rule or pre-commit hook that flags imports or calls to `yaml.load`, `yaml.unsafe_load`, `yaml.FullLoader`, `yaml.UnsafeLoader` in the codebase. This is the first line of defense for T-YF-07 (DREAD 38, CRITICAL). |
| **Files Affected** | `pyproject.toml` (ruff configuration -- add `S506` security rule or custom ban list), or `.pre-commit-config.yaml` (add grep-based hook) |
| **Complexity** | S |
| **Security** | Implements M-01 (banned API lint rule). First of three defense-in-depth layers for T-YF-07. |
| **Threats Mitigated** | T-YF-07 (CWE-502) |
| **HARD Rules** | H-05 (UV only -- configure via `pyproject.toml`) |
| **Depends On** | None |
| **Verification** | Create a test file containing `yaml.load()` call. Verify ruff or pre-commit flags it. Verify `yaml.safe_load()` is NOT flagged. |
| **Acceptance Criteria** | 1. `yaml.load(`, `yaml.unsafe_load(`, `yaml.FullLoader`, `yaml.UnsafeLoader` are flagged as errors. 2. `yaml.safe_load(` is not flagged. 3. Current codebase passes clean. |

---

## Phase 1: Core Parsers

> These work items implement the three new parser classes. They can be developed in parallel once Phase 0 completes. Each parser has a companion test work item.

### WI-005: YamlFrontmatter Parser (RE-001)

| Attribute | Value |
|-----------|-------|
| **Description** | Create `src/domain/markdown_ast/yaml_frontmatter.py` per DD-1, DD-8, DD-9, DD-10 in the ADR. Includes `YamlFrontmatterField`, `YamlFrontmatterResult`, and `YamlFrontmatter` class with `extract()` static method. |
| **Files Affected** | `src/domain/markdown_ast/yaml_frontmatter.py` (NEW), `src/domain/markdown_ast/__init__.py` (add exports) |
| **Complexity** | L |
| **Security** | M-01 compliance (safe_load only), M-07 (pre-parse size), M-19 (error sanitization), M-20 (post-parse result size + alias count), M-23 (duplicate key detection), M-24 (first-pair-only), M-06 (depth check), M-16 (key count), M-17 (value length), M-18 (control char stripping) |
| **Threats Mitigated** | T-YF-01 through T-YF-10 (all YAML threats) |
| **CWE Coverage** | CWE-502, CWE-776, CWE-400, CWE-20, CWE-209, CWE-290, CWE-138 |
| **HARD Rules** | H-07 (domain only), H-10 (one primary class), H-11 (type hints + docstrings), H-33 (AST-based, no regex for frontmatter extraction -- uses yaml.safe_load) |
| **Depends On** | WI-002 (InputBounds) |
| **Implementation Notes** | 1. Module MUST NOT import `yaml.load`, `yaml.unsafe_load`, `yaml.FullLoader`, `yaml.UnsafeLoader`. 2. All container fields use `tuple` (not `list`). 3. Error handling per DD-9 -- return result with `parse_error` set, never raise. 4. Type normalization per DD-10 (bool -> "true"/"false", int -> str, etc.). 5. Pre-parse alias count check by scanning for `*` references. 6. Post-parse result size via `len(json.dumps(result))`. |
| **Acceptance Criteria** | 1. `YamlFrontmatter.extract()` returns `YamlFrontmatterResult`. 2. All InputBounds limits enforced. 3. Only `yaml.safe_load()` used. 4. Duplicate keys generate warnings. 5. First `---` pair only. 6. Error messages sanitized. |

### WI-006: YamlFrontmatter Unit Tests

| Attribute | Value |
|-----------|-------|
| **Description** | BDD test-first test suite for YamlFrontmatter. Includes happy-path extraction, type normalization, InputBounds enforcement, error handling, and the M-04a AST-based integration test verifying only `yaml.safe_load` is used in the module. |
| **Files Affected** | `tests/unit/domain/markdown_ast/test_yaml_frontmatter.py` (NEW) |
| **Complexity** | L |
| **Security** | M-04a (AST-based test verifying `yaml.safe_load` exclusivity) |
| **HARD Rules** | H-20 (BDD test-first, 90% coverage) |
| **Depends On** | WI-005 |
| **Test Categories** | `@happy-path`: extract valid YAML frontmatter, type normalization. `@negative`: oversized YAML block, exceeds depth, exceeds key count, post-parse size exceeded, duplicate keys. `@edge-case`: empty frontmatter, no closing `---`, multiple `---` blocks (first-pair-only). `@boundary`: exactly 32KB YAML block, exactly 100 keys, depth exactly 5. `@security`: AST verification test (M-04a), `!!python/object` rejection, billion-laughs payload. |
| **Acceptance Criteria** | 1. >= 90% line coverage for `yaml_frontmatter.py`. 2. M-04a AST test passes. 3. All boundary values tested. |

### WI-007: XmlSectionParser (RE-002)

| Attribute | Value |
|-----------|-------|
| **Description** | Create `src/domain/markdown_ast/xml_section.py` per DD-6 in the ADR. Regex-based extraction of XML-tagged sections with allowed-tag whitelist, nesting rejection, non-greedy matching, and InputBounds enforcement. |
| **Files Affected** | `src/domain/markdown_ast/xml_section.py` (NEW), `src/domain/markdown_ast/__init__.py` (add exports) |
| **Complexity** | M |
| **Security** | M-11 (no XML parser library -- regex only), M-15 (non-greedy matching), M-16 (max section count), M-17 (max content length) |
| **Threats Mitigated** | T-XS-01 through T-XS-08 |
| **CWE Coverage** | CWE-611 (eliminated by architecture), CWE-20, CWE-74, CWE-400 |
| **HARD Rules** | H-07, H-10, H-11 |
| **Depends On** | WI-002 (InputBounds) |
| **Implementation Notes** | 1. MUST NOT import `xml.etree`, `lxml`, `xml.sax`, or any XML parser. 2. `ALLOWED_TAGS` is a `frozenset`. 3. Regex uses `re.MULTILINE | re.DOTALL` with non-greedy `.*?`. 4. Post-match check: content does not contain `<tagname>` (nested tag rejection). 5. Content trimmed with `.strip()`. |
| **Acceptance Criteria** | 1. Extracts all 7 allowed tags. 2. Rejects unknown tags. 3. Rejects nested same-name tags. 4. InputBounds enforced. 5. No XML parser library used. |

### WI-008: XmlSectionParser Unit Tests

| Attribute | Value |
|-----------|-------|
| **Description** | BDD test suite for XmlSectionParser. |
| **Files Affected** | `tests/unit/domain/markdown_ast/test_xml_section.py` (NEW) |
| **Complexity** | M |
| **HARD Rules** | H-20 |
| **Depends On** | WI-007 |
| **Test Categories** | `@happy-path`: extract all 7 allowed tags, multi-section document. `@negative`: unknown tag, nested same-name tag, unclosed tag, exceeds section count, exceeds content length. `@edge-case`: tag-in-content limitation (backtick-fenced examples), empty content, whitespace-only content. `@boundary`: exactly 20 sections, content exactly 10,000 chars. |
| **Acceptance Criteria** | >= 90% line coverage for `xml_section.py`. |

### WI-009: HtmlCommentMetadata Parser (RE-003)

| Attribute | Value |
|-----------|-------|
| **Description** | Create `src/domain/markdown_ast/html_comment.py` per DD-7 in the ADR. Regex-based extraction of HTML comment metadata blocks with case-insensitive L2-REINJECT exclusion, first-`-->` termination, non-greedy matching, and InputBounds enforcement. |
| **Files Affected** | `src/domain/markdown_ast/html_comment.py` (NEW), `src/domain/markdown_ast/__init__.py` (add exports) |
| **Complexity** | M |
| **Security** | M-13 (first `-->` termination), M-16 (max comment count), M-17 (max value length), M-18 (control char stripping). Case-insensitive negative lookahead for L2-REINJECT exclusion. |
| **Threats Mitigated** | T-HC-01 through T-HC-06 |
| **CWE Coverage** | CWE-74, CWE-20, CWE-400, CWE-200, CWE-290, CWE-778 |
| **HARD Rules** | H-07, H-10, H-11 |
| **Depends On** | WI-002 (InputBounds) |
| **Implementation Notes** | 1. Regex uses non-greedy `.*?` up to first `-->` (NOT `[^>]*`). 2. Case-insensitive negative lookahead: `(?!(?i)L2-REINJECT:)`. 3. Pipe-separated key-value parsing. 4. Distinguishes from L2-REINJECT comments (handled by `reinject.py`). |
| **Acceptance Criteria** | 1. Extracts pipe-separated metadata from HTML comments. 2. Excludes L2-REINJECT comments (case-insensitive). 3. First `-->` terminates. 4. InputBounds enforced. |

### WI-010: HtmlCommentMetadata Unit Tests

| Attribute | Value |
|-----------|-------|
| **Description** | BDD test suite for HtmlCommentMetadata. |
| **Files Affected** | `tests/unit/domain/markdown_ast/test_html_comment.py` (NEW) |
| **Complexity** | M |
| **HARD Rules** | H-20 |
| **Depends On** | WI-009 |
| **Test Categories** | `@happy-path`: extract ADR metadata, multi-comment document. `@negative`: exceeds comment count, value too long, value contains `-->` (truncation). `@edge-case`: L2-REINJECT exclusion (exact match), L2-REINJECT exclusion (case variants: `l2-reinject:`, `L2-Reinject:`), empty comment, comment with no key-value pairs. `@boundary`: exactly 50 comments, value exactly 10,000 chars. |
| **Acceptance Criteria** | >= 90% line coverage for `html_comment.py`. |

---

## Phase 2: Integration and Schema

> These work items connect the parsers via document type detection and the universal facade, and extend the schema validation engine.

### WI-011: DocumentTypeDetector + DocumentType Enum (RE-004)

| Attribute | Value |
|-----------|-------|
| **Description** | Create `src/domain/markdown_ast/document_type.py` per DD-2 in the ADR. Includes `DocumentType` enum (11 values) and `DocumentTypeDetector` class with path-first, structure-fallback detection using first-match-wins semantics. |
| **Files Affected** | `src/domain/markdown_ast/document_type.py` (NEW), `src/domain/markdown_ast/__init__.py` (add exports) |
| **Complexity** | M |
| **Security** | M-14 (dual-signal type detection with mismatch warning) |
| **Threats Mitigated** | T-DT-01 (CWE-843), T-DT-02 (CWE-20), T-DT-03 (CWE-20) |
| **HARD Rules** | H-07, H-10, H-11 |
| **Depends On** | WI-002 |
| **Implementation Notes** | 1. `PATH_PATTERNS` is an ordered list of `(glob_pattern, DocumentType)` tuples. 2. First-match-wins for path patterns. 3. Structural cue priority: YAML > blockquote > XML > HTML. 4. `UNKNOWN` is the safe default. 5. Dual-signal mismatch produces a warning string, not an error. |
| **Acceptance Criteria** | 1. All 10 document types correctly detected from path patterns. 2. `UNKNOWN` returned for unrecognized paths. 3. Structural fallback works when path does not match. 4. Mismatch warning generated when path and structure disagree. |

### WI-012: DocumentTypeDetector Tests + Pattern Collision Test

| Attribute | Value |
|-----------|-------|
| **Description** | BDD test suite for DocumentTypeDetector. Includes the pattern collision test that enumerates all `.md` files in the repository and verifies no file matches 2+ path patterns. |
| **Files Affected** | `tests/unit/domain/markdown_ast/test_document_type.py` (NEW) |
| **Complexity** | M |
| **HARD Rules** | H-20 |
| **Depends On** | WI-011 |
| **Test Categories** | `@happy-path`: each document type detected from path, structural fallback. `@negative`: binary file, non-UTF-8. `@edge-case`: file matching 0 path patterns (UNKNOWN), mismatch warning. `@integration`: pattern collision test across repository. |
| **Acceptance Criteria** | >= 90% line coverage. Pattern collision test passes for all `.md` files in the repository. |

### WI-013: UniversalDocument Facade (RE-007)

| Attribute | Value |
|-----------|-------|
| **Description** | Create `src/domain/markdown_ast/universal_document.py` per DD-3 and DD-9 in the ADR. `UniversalDocument` class with `parse()` static method that delegates to type-specific parsers based on the parser invocation matrix. `UniversalParseResult` frozen dataclass with `tuple` containers aggregating results from all invoked parsers. |
| **Files Affected** | `src/domain/markdown_ast/universal_document.py` (NEW), `src/domain/markdown_ast/__init__.py` (add exports), `tests/unit/domain/markdown_ast/test_universal_document.py` (NEW) |
| **Complexity** | L |
| **Security** | Aggregates parse errors per DD-9. Default `InputBounds.DEFAULT` when `None`. Deep immutability via `frozen=True` + `tuple` containers. |
| **HARD Rules** | H-07, H-10, H-11 |
| **Depends On** | WI-005 (YamlFrontmatter), WI-007 (XmlSectionParser), WI-009 (HtmlCommentMetadata), WI-011 (DocumentTypeDetector) |
| **Implementation Notes** | 1. Parser invocation matrix from ADR DD-3 table. 2. Each parser invoked conditionally based on `DocumentType`. 3. Parse errors aggregated from all invoked parsers into `parse_errors: tuple[str, ...]`. 4. `type_detection_warning` populated when path/structure mismatch. 5. `document_type` parameter overrides auto-detection when provided. 6. `bounds` parameter defaults to `InputBounds.DEFAULT`. |
| **Acceptance Criteria** | 1. `UniversalDocument.parse()` produces correct `UniversalParseResult` for all 11 `DocumentType` values. 2. Parser invocation matrix matches ADR specification. 3. All result fields are immutable (`frozen=True` + `tuple`). 4. Parse errors aggregated correctly. |

### WI-014: Schema Extension -- Agent Definition and Skill Definition

| Attribute | Value |
|-----------|-------|
| **Description** | Add `AGENT_DEFINITION_SCHEMA` and `SKILL_DEFINITION_SCHEMA` to `schema.py` using the `SchemaRegistry`. These are the highest-priority new schemas because H-34 requires agent definition YAML validation. |
| **Files Affected** | `src/domain/markdown_ast/schema.py` (modify -- add schema definitions and register with new registry) |
| **Complexity** | M |
| **Security** | M-12 (ReDoS-safe `value_pattern` regexes). Schema field rules must avoid nested quantifiers. |
| **Threats Mitigated** | T-SV-01 (CWE-20), T-SV-02 (CWE-20), T-SV-03 (CWE-1333) |
| **HARD Rules** | H-34 (agent definition schema validation enablement) |
| **Depends On** | WI-003 (SchemaRegistry) |
| **Implementation Notes** | 1. Agent definition schema validates YAML frontmatter fields: `name`, `version`, `description`, `model`, `identity.role`, etc. 2. Value patterns for `model` field: `^(opus|sonnet|haiku)$`. 3. Section rules for XML-tagged sections: `<identity>`, `<capabilities>`, `<guardrails>`, `<output>`. 4. All `value_pattern` regexes reviewed for ReDoS safety. |
| **Acceptance Criteria** | 1. `AGENT_DEFINITION_SCHEMA` and `SKILL_DEFINITION_SCHEMA` registered and frozen. 2. Backward compatible with existing 6 schemas. 3. No ReDoS-vulnerable patterns. |

### WI-015: Schema Extension -- Remaining 4 File Types

| Attribute | Value |
|-----------|-------|
| **Description** | Add `RULE_FILE_SCHEMA`, `ADR_SCHEMA`, `STRATEGY_TEMPLATE_SCHEMA`, `FRAMEWORK_CONFIG_SCHEMA`, `ORCHESTRATION_SCHEMA`, `PATTERN_SCHEMA`, and `KNOWLEDGE_SCHEMA` to `schema.py`. |
| **Files Affected** | `src/domain/markdown_ast/schema.py` (modify) |
| **Complexity** | M |
| **Security** | M-12 (ReDoS-safe patterns) |
| **HARD Rules** | H-11 |
| **Depends On** | WI-003 |
| **Implementation Notes** | These schemas are lower-priority than agent/skill definitions. Rule files have no frontmatter (section rules only). ADR schemas validate HTML comment metadata fields (PS-ID, ENTRY, AGENT). Strategy templates validate blockquote metadata (Strategy, ID, Family). |
| **Acceptance Criteria** | 1. All 7 new schemas registered and frozen. 2. Total of 13 schemas in registry (6 existing + 7 new). 3. `get_entity_schema()` works for all types. |

### WI-016: Schema Extension Tests

| Attribute | Value |
|-----------|-------|
| **Description** | Tests for all new schemas. Validates field rules, section rules, and `require_nav_table` settings. Tests ReDoS safety of all new `value_pattern` regexes. |
| **Files Affected** | `tests/unit/domain/markdown_ast/test_schema.py` (modify -- add tests for new schemas) |
| **Complexity** | M |
| **HARD Rules** | H-20 |
| **Depends On** | WI-014, WI-015 |
| **Acceptance Criteria** | 1. All 13 schemas validated in tests. 2. Each schema's required fields and sections verified. |

---

## Phase 3: CLI and Hardening

> These work items extend the CLI and apply security hardening to existing code.

### WI-017: CLI Extensions (RE-006)

| Attribute | Value |
|-----------|-------|
| **Description** | Extend `src/interface/cli/ast_commands.py` with: `--type` flag on `ast validate` and `ast frontmatter`, `ast sections` subcommand, `ast metadata` subcommand, `ast detect` subcommand, `--legacy` flag for canary mode. |
| **Files Affected** | `src/interface/cli/ast_commands.py` (modify), `tests/unit/interface/cli/test_ast_commands.py` (modify -- add tests for new commands) |
| **Complexity** | L |
| **HARD Rules** | H-11 |
| **Depends On** | WI-013 (UniversalDocument) |
| **Implementation Notes** | 1. `ast detect FILE` returns JSON with `type` and `method` fields. 2. `ast sections FILE` returns JSON section list. 3. `ast metadata FILE` returns JSON metadata blocks. 4. `--type agent_definition` overrides auto-detection. 5. `--legacy` forces existing parsers (bypass UniversalDocument). 6. `ast frontmatter FILE --format yaml` extracts YAML frontmatter. |
| **Acceptance Criteria** | 1. All new subcommands functional. 2. `--type` flag works on validate and frontmatter. 3. `--legacy` flag produces backward-compatible output. 4. Existing commands unchanged without new flags. |

### WI-018: Path Containment in CLI (M-08, M-10)

| Attribute | Value |
|-----------|-------|
| **Description** | Enhance `_read_file()` in `ast_commands.py` to: resolve file path with `Path.resolve()`, verify it starts with the repository root (`is_relative_to()`), resolve symlinks with `os.path.realpath()` before containment check, and enforce 1MB file size limit (M-05). |
| **Files Affected** | `src/interface/cli/ast_commands.py` (modify `_read_file()`) |
| **Complexity** | S |
| **Security** | Remediates V-01 (no path containment in `_read_file`). Implements M-08 (repository-root containment) and M-10 (symlink resolution). |
| **Threats Mitigated** | T-DT-04 (CWE-22), T-DT-05 (CWE-59) |
| **HARD Rules** | H-11 |
| **Depends On** | Phase 0 complete |
| **Implementation Notes** | 1. Determine repo root via `Path(__file__).resolve().parents[N]` or git-based detection. 2. `resolved = Path(file_path).resolve()`. 3. `if not resolved.is_relative_to(repo_root): return error`. 4. `if resolved != Path(os.path.realpath(file_path))`: symlink warning. 5. Size check: `resolved.stat().st_size > 1_048_576`. |
| **Acceptance Criteria** | 1. `../../etc/passwd` rejected. 2. Symlinks resolved before containment check. 3. Files > 1MB rejected. 4. Normal repository files accepted. |

### WI-019: L2-REINJECT Trusted Path Whitelist (M-22)

| Attribute | Value |
|-----------|-------|
| **Description** | Enhance `reinject.py` to add file-origin trust checking. Add `TRUSTED_REINJECT_PATHS` constant. `extract_reinject_directives()` gains a `file_path` parameter; directives from untrusted paths are silently excluded. Make `_REINJECT_PATTERN` case-insensitive. Make `tokens=` field optional in the pattern (many production directives omit it). |
| **Files Affected** | `src/domain/markdown_ast/reinject.py` (modify), `tests/unit/domain/markdown_ast/test_reinject.py` (modify -- add trust checking tests) |
| **Complexity** | M |
| **Security** | Remediates V-07 (no file-origin trust checking). Implements M-22 (trusted path whitelist). |
| **Threats Mitigated** | T-HC-04 (CWE-94), T-HC-07 (CWE-284) |
| **HARD Rules** | H-07, H-11 |
| **Depends On** | Phase 0 complete |
| **Implementation Notes** | 1. `TRUSTED_REINJECT_PATHS = (".context/rules/", ".claude/rules/", "CLAUDE.md")`. 2. `file_path` parameter is optional for backward compatibility (default `None` = no trust check). 3. When `file_path` is provided and not in trusted paths, directives are excluded with a warning. 4. `_REINJECT_PATTERN` updated to use `re.IGNORECASE`. 5. `tokens=` field made optional: `(?:tokens=(\d+),\s*)?`. |
| **Acceptance Criteria** | 1. Directives from trusted paths extracted normally. 2. Directives from untrusted paths excluded when `file_path` provided. 3. Backward compatible when `file_path` is `None`. 4. Case-insensitive matching. 5. `tokens=` field optional. |

### WI-020: Write-Back TOCTOU Mitigation (M-21)

| Attribute | Value |
|-----------|-------|
| **Description** | Enhance `ast_modify()` in `ast_commands.py` to use atomic write: write to temp file in same directory, then `os.rename()` to target path. Re-verify path containment immediately before rename. |
| **Files Affected** | `src/interface/cli/ast_commands.py` (modify `ast_modify()`) |
| **Complexity** | S |
| **Security** | Remediates V-02 (write-back path unconstrained, no TOCTOU protection). Implements M-21 (atomic write). |
| **Threats Mitigated** | T-WB-01 (CWE-367) |
| **HARD Rules** | H-11 |
| **Depends On** | Phase 0 complete, WI-018 (path containment) |
| **Implementation Notes** | 1. `temp_path = target_path.with_suffix('.tmp')`. 2. `temp_path.write_text(content, encoding="utf-8")`. 3. Re-verify `target_path.resolve().is_relative_to(repo_root)`. 4. `os.rename(str(temp_path), str(target_path))`. 5. Clean up temp file in `finally` block if rename fails. |
| **Acceptance Criteria** | 1. Write-back uses atomic temp+rename. 2. Path re-verified before rename. 3. Temp file cleaned up on failure. |

### WI-021: CI Grep Check for Banned YAML APIs (M-04b)

| Attribute | Value |
|-----------|-------|
| **Description** | Add a CI step (GitHub Actions) that greps the codebase for `yaml.load(` and `yaml.unsafe_load(` patterns, excluding test files that test rejection behavior. Fail the build if found. |
| **Files Affected** | `.github/workflows/` (new or modified CI workflow step) |
| **Complexity** | S |
| **Security** | Implements M-04b (CI grep check). Third defense-in-depth layer for T-YF-07. |
| **Threats Mitigated** | T-YF-07 (CWE-502) |
| **Depends On** | WI-004 (lint rule) |
| **Implementation Notes** | `grep -rn "yaml\.load\b\|yaml\.unsafe_load" src/ --include="*.py"` with exit code check. Exclude `tests/` directory from the search (test files may intentionally reference these for rejection testing). |
| **Acceptance Criteria** | 1. CI step runs on every PR. 2. Fails if banned pattern found in `src/`. 3. Does not fail on test files. |

---

## Phase 4: Testing and Validation

> These work items ensure comprehensive test coverage, adversarial testing, and migration safety validation.

### WI-022: Adversarial Test Suite

| Attribute | Value |
|-----------|-------|
| **Description** | Create a dedicated adversarial test suite covering all 11 attacks from the PASTA Stage 6 attack catalog (A-01 through A-11). Each attack has a corresponding test that verifies the mitigation works. |
| **Files Affected** | `tests/security/test_adversarial_parsers.py` (NEW) |
| **Complexity** | L |
| **Security** | Validates all CRITICAL and HIGH mitigations from threat model |
| **HARD Rules** | H-20 |
| **Depends On** | WI-005, WI-007, WI-009 |
| **Test Cases** | A-01: `!!python/object` YAML tag (verify safe_load rejects). A-02: L2-REINJECT from untrusted path (verify excluded). A-03: YAML billion-laughs (verify memory bounded by M-20). A-04: `xml.etree` import verification (verify not present). A-05: L2-REINJECT spoofing from non-governance path. A-06: Deeply nested YAML (verify depth limit). A-07: Path traversal via CLI (verify containment). A-08: ReDoS value_pattern (verify no catastrophic backtracking). A-09: YAML anchor injection (verify bounds). A-10: `-->` in HTML comment value (verify truncation). A-11: Symlink substitution in write-back (verify atomic write). |
| **Acceptance Criteria** | All 11 attack tests pass. Each test verifies the specific mitigation identified in the threat model. |

### WI-023: ReDoS Test Suite for Schema value_patterns

| Attribute | Value |
|-----------|-------|
| **Description** | Create test cases that verify all `value_pattern` regexes in FieldRule definitions are safe from catastrophic backtracking. Tests adversarial inputs (e.g., `"a" * 10000`) against each pattern with a timeout. |
| **Files Affected** | `tests/security/test_redos_patterns.py` (NEW) |
| **Complexity** | M |
| **Security** | M-12 (ReDoS-safe regex patterns) |
| **Threats Mitigated** | T-SV-03 (CWE-1333) |
| **HARD Rules** | H-20 |
| **Depends On** | WI-014, WI-015 |
| **Implementation Notes** | 1. Extract all `value_pattern` strings from all registered schemas. 2. For each pattern, test with adversarial inputs: repeated characters, nested groups, alternation chains. 3. Use `signal.alarm()` (Unix) or thread-based timeout to detect backtracking > 1 second. |
| **Acceptance Criteria** | All value_pattern regexes complete in < 1 second on adversarial inputs of 10,000+ characters. |

### WI-024: Golden-File Regression Test Suite

| Attribute | Value |
|-----------|-------|
| **Description** | Validate that `UniversalDocument.parse()` produces identical output to existing parsers for all known file patterns. Implements the golden-file test suite from ADR Migration Safety section. |
| **Files Affected** | `tests/regression/test_golden_files.py` (NEW) |
| **Complexity** | L |
| **HARD Rules** | H-20, H-33 |
| **Depends On** | WI-013, WI-017 |
| **Test Categories** | 1. Worktracker entities: `UniversalDocument.parse()` frontmatter matches `BlockquoteFrontmatter.extract()`. 2. Rule files: reinject directives match `extract_reinject_directives()`. 3. Existing schemas: validation unchanged for all 6 worktracker entity types. 4. Pattern collision: no `.md` file matches 2+ `PATH_PATTERNS`. |
| **Acceptance Criteria** | 1. All worktracker entity files produce identical frontmatter via both paths. 2. All rule files produce identical reinject directives. 3. Pattern collision test passes. |

### WI-025: Integration Tests and Coverage Verification

| Attribute | Value |
|-----------|-------|
| **Description** | End-to-end integration tests for the complete pipeline: CLI -> UniversalDocument -> parsers -> schema validation. Verify 90% line coverage across all new and modified files. |
| **Files Affected** | `tests/integration/cli/test_ast_universal.py` (NEW) |
| **Complexity** | M |
| **HARD Rules** | H-20 (90% line coverage), H-33 |
| **Depends On** | WI-017 |
| **Test Cases** | 1. `jerry ast detect <agent_definition_file>` returns correct type. 2. `jerry ast validate <agent_def> --type agent_definition` validates correctly. 3. `jerry ast sections <agent_def>` returns XML sections. 4. `jerry ast metadata <adr_file>` returns HTML comment metadata. 5. `jerry ast frontmatter <agent_def> --format yaml` returns YAML fields. 6. `--legacy` flag produces backward-compatible output. |
| **Acceptance Criteria** | 1. All integration tests pass. 2. `uv run pytest --cov=src/domain/markdown_ast --cov-report=term-missing` shows >= 90% line coverage. |

---

## Critical Path Analysis

The critical path runs through:

```
WI-001 (FrontmatterField frozen, S)
  -> WI-002 (InputBounds, M)
    -> WI-005 (YamlFrontmatter, L)      <-- longest Phase 1 item
      -> WI-006 (YamlFrontmatter tests, L)
        -> WI-013 (UniversalDocument, L)  <-- Phase 2 bottleneck
          -> WI-017 (CLI extensions, L)    <-- Phase 3 bottleneck
            -> WI-024 (Golden-file regression, L)
              -> WI-025 (Integration tests, M)
```

**Critical path length:** 8 work items (2S + 2M + 4L).

**Schedule risk factors:**

1. **YamlFrontmatter (WI-005)** is the most complex single work item due to the number of security constraints (M-01, M-06, M-07, M-19, M-20, M-23, M-24) and the DD-10 type normalization requirement. Estimated 300-500 lines.

2. **UniversalDocument (WI-013)** depends on all three parsers AND the document type detector completing. It is the single integration point where delays from any Phase 1 work item cascade.

3. **Golden-file regression (WI-024)** requires real repository files and may surface unexpected edge cases in the universal parser that require backtracking to fix parsers.

**Mitigation:** Phase 1 parsers are independent and parallelizable, reducing the calendar time even though WI-005 is on the critical path. WI-007 and WI-009 (with their test items) can complete while WI-005/WI-006 are in progress, so Phase 2 work on WI-011 can begin as soon as WI-002 completes (it does not depend on the parsers).

---

## Standards Compliance Matrix

| Work Item | H-07 | H-10 | H-11 | H-20 | H-33 | H-34 | H-05 | Security Mitigations |
|-----------|:----:|:----:|:----:|:----:|:----:|:----:|:----:|---------------------|
| WI-001 | -- | Y | Y | Y | -- | -- | -- | V-05 |
| WI-002 | Y | Y | Y | Y | -- | -- | -- | M-05/06/07/16/17/20 |
| WI-003 | Y | Y | Y | Y | -- | -- | -- | T-SV-04/05 |
| WI-004 | -- | -- | -- | -- | -- | -- | Y | M-01 |
| WI-005 | Y | Y | Y | -- | Y | Y | -- | M-01/06/07/18/19/20/23/24 |
| WI-006 | -- | -- | -- | Y | -- | -- | Y | M-04a |
| WI-007 | Y | Y | Y | -- | -- | -- | -- | M-11/15/16/17 |
| WI-008 | -- | -- | -- | Y | -- | -- | Y | -- |
| WI-009 | Y | Y | Y | -- | -- | -- | -- | M-13/16/17/18 |
| WI-010 | -- | -- | -- | Y | -- | -- | Y | -- |
| WI-011 | Y | Y | Y | -- | -- | -- | -- | M-14 |
| WI-012 | -- | -- | -- | Y | -- | -- | Y | -- |
| WI-013 | Y | Y | Y | -- | Y | -- | -- | DD-3/9 |
| WI-014 | Y | -- | Y | -- | -- | Y | -- | M-12 |
| WI-015 | Y | -- | Y | -- | -- | -- | -- | M-12 |
| WI-016 | -- | -- | -- | Y | -- | -- | Y | -- |
| WI-017 | -- | -- | Y | -- | -- | -- | -- | -- |
| WI-018 | -- | -- | Y | -- | -- | -- | -- | M-08/10 |
| WI-019 | Y | -- | Y | Y | -- | -- | -- | M-22 |
| WI-020 | -- | -- | Y | -- | -- | -- | -- | M-21 |
| WI-021 | -- | -- | -- | -- | -- | -- | -- | M-04b |
| WI-022 | -- | -- | -- | Y | -- | -- | Y | All HIGH+ |
| WI-023 | -- | -- | -- | Y | -- | -- | Y | M-12 |
| WI-024 | -- | -- | -- | Y | Y | -- | Y | PM-001-B1 |
| WI-025 | -- | -- | -- | Y | Y | -- | Y | -- |

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| `FrontmatterField` `frozen=True` migration breaks downstream code that mutates fields | Low | Medium | WI-001 includes grep verification and full test suite run before proceeding |
| YAML type normalization (DD-10) introduces subtle schema validation regressions | Medium | Medium | WI-006 includes comprehensive type normalization tests; WI-024 golden-file regression catches mismatches |
| `_REINJECT_PATTERN` regex change (tokens= optional, case-insensitive) affects existing directive extraction | Medium | High | WI-019 modifies pattern carefully with full test coverage; backward-compatible `file_path=None` default |
| Golden-file regression (WI-024) reveals edge cases requiring parser fixes | High | Medium | Expected and budgeted. Parser fixes backtrack to Phase 1 work items with localized impact |
| ReDoS in new schema `value_pattern` regexes not caught until Phase 4 | Low | High | WI-023 is a dedicated ReDoS test suite. WI-014/WI-015 include inline ReDoS review during schema creation |
| SchemaRegistry `freeze()` disrupts dynamic test fixtures that modify the registry | Low | Low | Tests use fresh `SchemaRegistry()` instances, not the module-level default |
| `DocumentTypeDetector` path patterns do not cover all repository file layouts | Medium | Low | WI-012 pattern collision test enumerates all `.md` files; gaps discovered at test time |

---

## Strategic Implications (L2)

### Technical Debt

1. **`BlockquoteFrontmatter._fields` remains a mutable list.** WI-001 adds `frozen=True` to `FrontmatterField` (attribute immutability) but the internal `_fields: list[FrontmatterField]` container in `BlockquoteFrontmatter` is still a mutable list. A follow-up migration to `tuple` storage is recommended for Phase 2 but is not a P0 blocker (the trust boundary diagram documents this gap).

2. **`NavValidationResult` is not frozen.** The existing `NavValidationResult` at `nav_table.py:73` uses `@dataclass` without `frozen=True` and has mutable `list` default fields. This is a pre-existing defect analogous to V-05. A migration to `frozen=True` with `tuple` containers is recommended but out of scope for this plan.

3. **`JerryDocument` is not frozen.** The `JerryDocument` class stores `_tokens` and `_tree` as mutable internal state. It documents itself as "immutable after construction" but does not enforce this at the language level. This is a known architectural limitation.

### Maintainability

1. **10 file-type schemas require ongoing maintenance.** As file formats evolve (new frontmatter fields, new section requirements), schemas must be updated. The `SchemaRegistry` pattern makes additions safe (collision detection, freeze) but does not reduce the burden of keeping schemas synchronized with format specifications.

2. **Parser invocation matrix is hardcoded.** The mapping from `DocumentType` to parser invocations in `UniversalDocument` is a lookup table. Adding a new `DocumentType` requires modifying `UniversalDocument.parse()`. A future enhancement could use a registry pattern for parser-to-type bindings.

### Migration Safety

1. **The `--legacy` flag** enables canary rollout by allowing side-by-side comparison of old and new parsers. This should remain available through at least one minor version cycle after the universal parser is GA.

2. **Golden-file regression tests** (WI-024) are the primary safety net for the 500+ existing `.md` files that will be processed by the universal parser. These tests should be run as part of every CI build, not just during initial development.

3. **The pattern collision test** (WI-012) should be a permanent CI fixture, not a one-time validation. New `.md` files added to the repository should be automatically checked for pattern ambiguity.

---

<!-- VERSION: 1.0.0 | DATE: 2026-02-23 | AGENT: eng-lead-001 | ENGAGEMENT: ENG-0001 -->
