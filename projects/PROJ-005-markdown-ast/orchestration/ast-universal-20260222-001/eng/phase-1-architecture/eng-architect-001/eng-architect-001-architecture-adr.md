# ADR: Universal Markdown Parser Architecture

<!-- PS-ID: ADR-PROJ005-003 | ENTRY: 2026-02-22 | AGENT: eng-architect | CRITICALITY: C4 -->
<!-- REVISION: 5 | PREVIOUS-SCORE: 0.946 (REVISE) | DATE: 2026-02-23 -->

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary (L0)](#executive-summary-l0) | Stakeholder-level architecture decision overview |
| [Status](#status) | ADR lifecycle state |
| [Context](#context) | Problem statement and driving forces |
| [Decision](#decision) | Chosen architecture with rationale |
| [Architecture Overview](#architecture-overview) | Component diagram and relationships |
| [Design Decision 1: Polymorphic Parser Pattern](#design-decision-1-polymorphic-parser-pattern) | Multi-format frontmatter parsing strategy |
| [Design Decision 2: Document Type Detection](#design-decision-2-document-type-detection) | Auto-detection strategy |
| [Design Decision 3: UniversalDocument Facade](#design-decision-3-universaldocument-facade) | Unified API surface |
| [Design Decision 4: Schema Extension Architecture](#design-decision-4-schema-extension-architecture) | How new schemas are registered |
| [Design Decision 5: CLI Extension Strategy](#design-decision-5-cli-extension-strategy) | Subcommands vs enhanced flags |
| [Design Decision 6: XmlSectionParser Implementation](#design-decision-6-xmlsectionparser-implementation) | Regex-only, no XML parser |
| [Design Decision 7: HtmlCommentMetadata Implementation](#design-decision-7-htmlcommentmetadata-implementation) | HTML comment parsing approach |
| [Design Decision 8: Input Bounds Enforcement](#design-decision-8-input-bounds-enforcement) | Resource limit architecture |
| [Design Decision 9: Error Handling Strategy](#design-decision-9-error-handling-strategy) | Unified error handling for all parsers |
| [Design Decision 10: YAML Type Normalization](#design-decision-10-yaml-type-normalization) | Type coercion handling |
| [Hexagonal Architecture Compliance](#hexagonal-architecture-compliance) | H-07 verification |
| [One-Class-Per-File Compliance](#one-class-per-file-compliance) | H-10 verification |
| [H-33 Compliance Strategy](#h-33-compliance-strategy) | AST-based parsing boundary |
| [Performance Requirements](#performance-requirements) | Performance baseline expectations |
| [Migration Safety](#migration-safety) | Backward compatibility and rollout strategy |
| [Consequences](#consequences) | Positive, negative, and neutral outcomes |
| [Alternatives Considered](#alternatives-considered) | Rejected approaches with rationale |
| [Strategic Implications (L2)](#strategic-implications-l2) | Long-term architecture evolution |
| [References](#references) | Source document traceability |
| [Disclaimer](#disclaimer) | Limitations and assumptions |
| [Revision History](#revision-history) | Change log for this document |

---

## Executive Summary (L0)

This ADR defines the architecture for extending the Jerry AST skill from a single-format blockquote frontmatter parser to a universal markdown parser supporting 10 distinct file types. The architecture uses a **polymorphic parser pattern** where a `UniversalDocument` facade delegates to type-specific parsers (YamlFrontmatter, XmlSectionParser, HtmlCommentMetadata) selected by a `DocumentTypeDetector`. All new components are domain-layer classes following the existing hexagonal architecture (H-07), one-class-per-file rule (H-10), and frozen-dataclass immutability pattern. All container fields in result objects use `tuple[..., ...]` (not `list`) to ensure deep immutability. The schema validation engine is extended via a registry pattern that permits adding new file-type schemas without modifying existing code, with a `freeze()` mechanism to prevent runtime poisoning. The CLI is enhanced with a `--type` flag and new subcommands rather than modifying existing command semantics.

**Pre-existing defect note:** The existing `FrontmatterField` at `frontmatter.py:54` uses `@dataclass` without `frozen=True`. This contradicts constraint C-05. Migration to `frozen=True` is a P0 prerequisite for this ADR (see [Migration Safety](#migration-safety)).

---

## Status

**PROPOSED** -- Pending implementation review and C4 quality gate.

---

## Context

### Problem Statement

The Jerry AST skill currently supports only one frontmatter format (blockquote `> **Key:** Value`) and six worktracker entity schemas. The Jerry Framework uses 10 distinct markdown file types with three different metadata embedding patterns:

1. **YAML frontmatter** (`---` delimited) -- Agent definitions, SKILL.md files
2. **Blockquote frontmatter** (`> **Key:** Value`) -- Worktracker entities, strategy templates, pattern docs
3. **HTML comment metadata** (`<!-- key: value -->`) -- ADRs, templates

Additionally, agent definition files use XML-like section tags (`<identity>`, `<methodology>`, etc.) for structured body content, and rule files use L2-REINJECT HTML comments (already supported).

Without a universal parser, each file type requires ad-hoc parsing logic, duplicating validation patterns and preventing unified tooling.

### Driving Forces

1. **H-33 compliance:** AST-based parsing is required for worktracker entity operations. Extending this to all file types enables consistent, reliable parsing across the framework.
2. **H-34 compliance:** Agent definition YAML frontmatter must validate against JSON Schema (`docs/schemas/agent-definition-v1.schema.json`). This requires YAML parsing capability.
3. **Tool consolidation:** A single `jerry ast` CLI namespace should handle all markdown parsing needs, reducing cognitive load and tool proliferation.
4. **Quality gate enablement:** Universal parsing enables automated structural validation of all 10 file types in CI/CD (L5 enforcement).

### Constraints

| ID | Constraint | Source |
|----|-----------|--------|
| C-01 | Domain layer MUST NOT import from interface/application/infrastructure | H-07 |
| C-02 | One class per file | H-10 |
| C-03 | AST-based parsing required for entity operations | H-33 |
| C-04 | YAML: `yaml.safe_load()` ONLY. Banned API lint rule (M-01), AST integration test (M-04a), and CI grep check (M-04b) enforce this. | Threat Model M-01, M-04a, M-04b |
| C-05 | All domain objects MUST be immutable (frozen dataclasses with `tuple` containers). **Existing defect:** `FrontmatterField` at `frontmatter.py:54` uses `@dataclass` without `frozen=True` -- migration to `frozen=True` is a P0 prerequisite. | Existing pattern; P0 migration |
| C-06 | Input bounds validation on all parsers, including post-parse result size verification for YAML (M-20) | Threat Model M-05 through M-07, M-16, M-17, M-20 |
| C-07 | No full XML parser library (XXE prevention) | Threat Model M-11 |

---

## Decision

Adopt a **polymorphic parser pattern** with the following architecture:

1. **DocumentTypeDetector** determines file type from path patterns (first-match-wins semantics, ordered list) with structural-cue fallback (priority: YAML > blockquote > XML > HTML).
2. **UniversalDocument** facade creates a type-specific parse result by delegating to the appropriate parser(s).
3. Each parser (YamlFrontmatter, XmlSectionParser, HtmlCommentMetadata) is a standalone domain class producing frozen dataclass results with `tuple` containers.
4. The schema validation engine is extended with a `SchemaRegistry` class supporting dynamic registration with collision detection and a `freeze()` method for post-initialization immutability.
5. The CLI gains a `--type` flag for explicit type specification and new subcommands for type-specific operations.
6. All parsers return result objects with typed error fields (no exceptions for parse failures); `UniversalParseResult` aggregates parse errors.

---

## Architecture Overview

### Component Diagram

```
src/domain/markdown_ast/
  |
  |-- jerry_document.py          [EXISTING] JerryDocument facade (markdown-it-py)
  |-- frontmatter.py             [EXISTING, MODIFIED] BlockquoteFrontmatter
  |                              (FrontmatterField migrated to frozen=True)
  |-- reinject.py                [EXISTING, MODIFIED] L2-REINJECT directive extraction
  |                              (add file-origin trust checking, M-22)
  |-- nav_table.py               [EXISTING] Navigation table helpers
  |-- schema.py                  [EXISTING, EXTENDED] Schema validation engine
  |                              (SchemaRegistry with freeze(), MappingProxyType)
  |
  |-- yaml_frontmatter.py        [NEW] YamlFrontmatter parser
  |-- xml_section.py             [NEW] XmlSectionParser
  |-- html_comment.py            [NEW] HtmlCommentMetadata parser
  |-- document_type.py           [NEW] DocumentTypeDetector + DocumentType enum
  |-- universal_document.py      [NEW] UniversalDocument facade
  |-- input_bounds.py            [NEW] InputBounds configuration and checking
  |
  |-- __init__.py                [EXTENDED] New public exports

src/interface/cli/
  |-- ast_commands.py            [EXTENDED] New subcommands, --type flag,
                                  path containment (M-08), atomic write (M-21)
```

### Dependency Graph (Domain Layer)

```
UniversalDocument
    |
    +-- DocumentTypeDetector (determines which parsers to invoke)
    +-- JerryDocument (base markdown AST, always invoked)
    +-- YamlFrontmatter (conditional: agent defs, SKILL.md)
    +-- BlockquoteFrontmatter (conditional: worktracker, strategies, patterns)
    +-- XmlSectionParser (conditional: agent defs)
    +-- HtmlCommentMetadata (conditional: ADRs, templates)
    +-- InputBounds (cross-cutting: all parsers)
    +-- extract_reinject_directives (conditional: rule files)
    +-- extract_nav_table (always available)
    +-- validate_document (optional: schema validation)
```

All arrows point inward (domain classes depend only on other domain classes). No domain class imports from `src/interface/` or `src/application/`. This satisfies H-07.

---

## Design Decision 1: Polymorphic Parser Pattern

### Decision

Each metadata format (YAML frontmatter, blockquote frontmatter, XML sections, HTML comments) is handled by a dedicated parser class. The `UniversalDocument` facade selects which parsers to invoke based on the detected `DocumentType`.

### Rationale

1. **Single Responsibility Principle:** Each parser handles exactly one format. Testing, debugging, and security review are scoped to one format per class.
2. **Open-Closed Principle:** New formats can be added by creating a new parser class and registering it with `UniversalDocument`. No modification of existing parser code is required.
3. **Security isolation:** A vulnerability in `YamlFrontmatter` does not affect `BlockquoteFrontmatter` or `XmlSectionParser`. The blast radius of each parser is bounded (see T-YF-07 CWE-502, T-XS-07 CWE-611 in threat model — polymorphic isolation prevents cross-parser vulnerability propagation).
4. **Existing precedent:** The current codebase already follows this pattern: `BlockquoteFrontmatter`, `ReinjectDirective`, and `NavEntry` are separate domain classes with dedicated extraction functions.

### Class: YamlFrontmatter

```python
# src/domain/markdown_ast/yaml_frontmatter.py

@dataclass(frozen=True)
class YamlFrontmatterField:
    """Single field from YAML frontmatter."""
    key: str
    value: str | int | float | bool | list | None
    value_type: str  # "str", "int", "float", "bool", "list", "null"

@dataclass(frozen=True)
class YamlFrontmatterResult:
    """Complete YAML frontmatter extraction result."""
    fields: tuple[YamlFrontmatterField, ...]
    raw_yaml: str          # The raw YAML text between --- delimiters
    start_line: int        # 0-based line of opening ---
    end_line: int          # 0-based line of closing ---
    parse_error: str | None  # None if parsing succeeded
    parse_warnings: tuple[str, ...] = ()  # Duplicate key warnings, type coercion notes

class YamlFrontmatter:
    """Extract and validate YAML frontmatter from --- delimited blocks."""

    @staticmethod
    def extract(doc: JerryDocument, bounds: InputBounds | None = None) -> YamlFrontmatterResult:
        """Extract YAML frontmatter using yaml.safe_load() ONLY.

        Extracts only the FIRST --- ... --- pair (first-pair-only rule).
        Subsequent --- blocks are ignored.
        """
        ...
```

**Key constraints:**
- MUST use `yaml.safe_load()`. The module MUST NOT import `yaml.load`, `yaml.unsafe_load`, `yaml.FullLoader`, or `yaml.UnsafeLoader`.
- MUST check YAML block size against `InputBounds.max_yaml_block_bytes` (default 32 KB) before calling `yaml.safe_load()` (M-07).
- MUST verify post-parse result size against `InputBounds.max_yaml_result_bytes` (default 64 KB) after `yaml.safe_load()` returns (M-20). This closes the temporal gap where anchor expansion occurs in memory.
- MUST validate post-parse result against `InputBounds.max_frontmatter_keys` and `InputBounds.max_nesting_depth` (M-06).
- MUST detect duplicate keys in raw YAML and include warnings in `parse_warnings` (M-23).
- MUST extract only the first `---` ... `---` pair (M-24: first-pair-only rule).
- Result is a frozen dataclass (immutable). Container fields use `tuple`.
- Parsing errors produce a result with `parse_error` set, not an exception (DD-9).
- MUST catch `yaml.scanner.ScannerError`, `yaml.parser.ParserError`, and `yaml.constructor.ConstructorError` individually. Error messages MUST NOT include raw file content or full file paths (M-19).

### Class: XmlSectionParser

```python
# src/domain/markdown_ast/xml_section.py

@dataclass(frozen=True)
class XmlSection:
    """Single XML-tagged section from an agent definition body."""
    tag_name: str           # e.g., "identity", "methodology"
    content: str            # Text content between opening and closing tags
    start_line: int         # 0-based line of <tag>
    end_line: int           # 0-based line of </tag>

@dataclass(frozen=True)
class XmlSectionResult:
    """Complete XML section extraction result."""
    sections: tuple[XmlSection, ...]
    parse_error: str | None  # None if parsing succeeded

class XmlSectionParser:
    """Extract XML-tagged sections using regex, NOT an XML parser."""

    ALLOWED_TAGS: frozenset[str] = frozenset({
        "identity", "purpose", "input", "capabilities",
        "methodology", "output", "guardrails",
    })

    @staticmethod
    def extract(doc: JerryDocument, bounds: InputBounds | None = None) -> XmlSectionResult:
        """Extract XML-tagged sections. Rejects tags not in ALLOWED_TAGS."""
        ...
```

**Key constraints:**
- MUST use regex-based extraction, NOT `xml.etree.ElementTree` or any XML parser library (M-11: XXE prevention).
- MUST use non-greedy matching for content between tags (M-15).
- MUST reject nested tags of the same name.
- MUST validate tag names against `ALLOWED_TAGS` whitelist.
- MUST enforce `InputBounds.max_section_count` and `InputBounds.max_value_length`.
- **Tag-in-content limitation:** Content discussing XML-like tags as examples (e.g., prose describing `<identity>`) may be partially consumed by the regex. Authors should use backtick-fenced code blocks for tag examples. This is a known limitation, not a bug.

### Class: HtmlCommentMetadata

```python
# src/domain/markdown_ast/html_comment.py

@dataclass(frozen=True)
class HtmlCommentField:
    """Single key-value pair from an HTML comment metadata block."""
    key: str
    value: str
    line_number: int

@dataclass(frozen=True)
class HtmlCommentBlock:
    """Complete HTML comment metadata extraction result."""
    fields: tuple[HtmlCommentField, ...]
    raw_comment: str
    line_number: int

@dataclass(frozen=True)
class HtmlCommentResult:
    """Complete HTML comment metadata extraction result."""
    blocks: tuple[HtmlCommentBlock, ...]
    parse_error: str | None  # None if parsing succeeded

class HtmlCommentMetadata:
    """Extract structured metadata from HTML comments in ADRs and templates."""

    @staticmethod
    def extract(doc: JerryDocument, bounds: InputBounds | None = None) -> HtmlCommentResult:
        """Extract HTML comment metadata blocks."""
        ...
```

**Key constraints:**
- MUST use the first `-->` as the comment terminator (M-13). Values containing `-->` cause the comment to be truncated, not the parser to fail.
- Regex MUST use non-greedy `.*?` up to `-->`, NOT `[^>]*` character class (FM-007-B1 fix).
- MUST distinguish between L2-REINJECT comments (handled by `reinject.py`) and metadata comments.
- MUST NOT extract comments that look like L2-REINJECT directives (avoid duplication with `extract_reinject_directives`). The negative lookahead MUST be case-insensitive to prevent `l2-reinject:` bypasses.

---

## Design Decision 2: Document Type Detection

### Decision

Use a **path-first, structure-fallback** detection strategy with an explicit `DocumentType` enum. Path patterns use **first-match-wins** semantics against an ordered list. Structural cues use a defined priority order for conflicting signals.

### DocumentType Enum

```python
# src/domain/markdown_ast/document_type.py

from enum import Enum

class DocumentType(Enum):
    """Jerry markdown file type classification."""
    AGENT_DEFINITION = "agent_definition"
    SKILL_DEFINITION = "skill_definition"
    RULE_FILE = "rule_file"
    ADR = "adr"
    STRATEGY_TEMPLATE = "strategy_template"
    WORKTRACKER_ENTITY = "worktracker_entity"
    FRAMEWORK_CONFIG = "framework_config"      # CLAUDE.md, AGENTS.md
    ORCHESTRATION_ARTIFACT = "orchestration_artifact"
    PATTERN_DOCUMENT = "pattern_document"
    KNOWLEDGE_DOCUMENT = "knowledge_document"
    UNKNOWN = "unknown"
```

### Detection Algorithm

```python
class DocumentTypeDetector:
    """Detect Jerry markdown file type from path patterns and structural cues."""

    # Ordered list: first match wins. More specific patterns before broader ones.
    PATH_PATTERNS: list[tuple[str, DocumentType]] = [
        # 1. Most specific patterns first
        ("skills/*/agents/*.md",           DocumentType.AGENT_DEFINITION),
        ("skills/*/SKILL.md",              DocumentType.SKILL_DEFINITION),
        (".context/rules/*.md",            DocumentType.RULE_FILE),
        (".claude/rules/*.md",             DocumentType.RULE_FILE),
        ("docs/design/*.md",              DocumentType.ADR),
        (".context/templates/adversarial/*.md", DocumentType.STRATEGY_TEMPLATE),
        # 2. Worktracker patterns (multiple paths)
        ("projects/*/WORKTRACKER.md",      DocumentType.WORKTRACKER_ENTITY),
        ("projects/**/work/**/*.md",       DocumentType.WORKTRACKER_ENTITY),
        # 3. Framework config (exact filenames)
        ("CLAUDE.md",                      DocumentType.FRAMEWORK_CONFIG),
        ("AGENTS.md",                      DocumentType.FRAMEWORK_CONFIG),
        # 4. Broader patterns last
        ("projects/*/orchestration/**/*.md", DocumentType.ORCHESTRATION_ARTIFACT),
        ("docs/knowledge/**/*.md",         DocumentType.KNOWLEDGE_DOCUMENT),
    ]

    # Structural cue priority order for conflicting signals.
    # When multiple cues match, higher priority wins.
    STRUCTURAL_CUE_PRIORITY: list[tuple[str, DocumentType]] = [
        ("---",              DocumentType.AGENT_DEFINITION),  # YAML delimiters
        ("> **",            DocumentType.WORKTRACKER_ENTITY), # Blockquote frontmatter
        ("<identity>",       DocumentType.AGENT_DEFINITION),  # XML sections
        ("<!-- L2-REINJECT", DocumentType.RULE_FILE),         # Reinject directives
        ("<!--",            DocumentType.ADR),                # HTML comments (last)
    ]

    @classmethod
    def detect(cls, file_path: str, content: str) -> DocumentType:
        """
        Detect document type. Path patterns take priority (first-match-wins);
        structural cues are fallback with defined priority ordering.
        """
        ...
```

**Pattern collision handling:** Multiple patterns can match the same file (e.g., `projects/*/orchestration/**/work/**/*.md` matches both `WORKTRACKER_ENTITY` and `ORCHESTRATION_ARTIFACT`). The first-match-wins rule resolves this deterministically: more specific patterns are listed before broader ones. A collision test suite (see [Migration Safety](#migration-safety)) validates that no ambiguous orderings exist for known file paths.

### Rationale

1. **Path-first is deterministic.** Given the same file path, the same type is always returned regardless of file content. This prevents content-based type spoofing (T-DT-01).
2. **Structure-fallback handles edge cases.** Files not matching any known path pattern can still be classified by structural cues with defined priority ordering.
3. **`UNKNOWN` as a safe default.** Unclassifiable files are typed as `UNKNOWN`, which routes them to the base JerryDocument parser (markdown-only, no metadata extraction). This is the most conservative behavior.
4. **Dual-signal validation (M-14).** When both path and structure signals are available, a mismatch triggers a warning in the parse result, alerting the user that the file's location does not match its content structure.

---

## Design Decision 3: UniversalDocument Facade

### Decision

Create a `UniversalDocument` class that wraps `JerryDocument` and adds type-specific parsed results as optional attributes. All container fields use `tuple` (not `list`) to ensure deep immutability.

```python
# src/domain/markdown_ast/universal_document.py

@dataclass(frozen=True)
class UniversalParseResult:
    """Complete parse result from UniversalDocument."""
    document_type: DocumentType
    jerry_document: JerryDocument              # Always present
    yaml_frontmatter: YamlFrontmatterResult | None
    blockquote_frontmatter: BlockquoteFrontmatter | None
    xml_sections: tuple[XmlSection, ...] | None       # tuple, NOT list
    html_comments: tuple[HtmlCommentBlock, ...] | None  # tuple, NOT list
    reinject_directives: tuple[ReinjectDirective, ...] | None  # tuple, NOT list
    nav_entries: tuple[NavEntry, ...] | None           # tuple, NOT list
    type_detection_warning: str | None         # Set when path/structure mismatch (M-14)
    parse_errors: tuple[str, ...] = ()         # Aggregated errors from all parsers (DD-9)

class UniversalDocument:
    """Unified facade for parsing any Jerry markdown file type."""

    @staticmethod
    def parse(
        content: str,
        file_path: str | None = None,
        document_type: DocumentType | None = None,
        bounds: InputBounds | None = None,
    ) -> UniversalParseResult:
        """
        Parse content into a type-specific UniversalParseResult.

        If document_type is provided, it is used directly (explicit override).
        If file_path is provided without document_type, auto-detection is used.
        If neither is provided, structure-only detection is attempted.

        The bounds parameter defaults to InputBounds.DEFAULT when None.
        """
        if bounds is None:
            bounds = InputBounds.DEFAULT
        ...
```

### Rationale

1. **Backward compatibility.** `JerryDocument` remains the base parsing layer. `UniversalDocument` is an additive facade, not a replacement.
2. **Deep immutability.** `UniversalParseResult` uses `frozen=True` AND `tuple` containers. Python's `frozen=True` prevents attribute reassignment; `tuple` prevents container mutation. This combination provides true immutability -- `result.xml_sections.append(x)` raises `AttributeError` (tuple has no `append`).
3. **Optional attributes with error distinction.** Each parser result is `None` when the parser was not invoked. The `parse_errors` tuple collects errors from parsers that were invoked but failed, enabling callers to distinguish "not invoked" from "invoked and failed" (DD-9).
4. **Explicit override.** The `document_type` parameter allows callers to bypass auto-detection. The `bounds` parameter defaults to `InputBounds.DEFAULT` when `None`, ensuring security-by-default.

### Parser Invocation Matrix

| DocumentType | JerryDocument | YamlFrontmatter | BlockquoteFrontmatter | XmlSectionParser | HtmlCommentMetadata | ReinjectDirectives | NavTable |
|-------------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| AGENT_DEFINITION | Y | Y (YAML frontmatter for metadata) | - | Y (structured body sections) | - | - | Y |
| SKILL_DEFINITION | Y | Y (YAML frontmatter for metadata) | - | - | - | - | Y |
| RULE_FILE | Y | - | - | - | - | Y (L2-REINJECT directives) | Y |
| ADR | Y | - | - | - | Y (PS-ID, ENTRY, AGENT metadata) | - | Y |
| STRATEGY_TEMPLATE | Y | - | Y (blockquote metadata) | - | - | - | - |
| WORKTRACKER_ENTITY | Y | - | Y (blockquote frontmatter) | - | - | - | Y |
| FRAMEWORK_CONFIG | Y | - | - | - | - | Y (L2-REINJECT directives) | Y |
| ORCHESTRATION_ARTIFACT | Y | - | - | - | Y (engagement metadata) | - | Y |
| PATTERN_DOCUMENT | Y | - | Y (blockquote metadata) | - | - | - | Y |
| KNOWLEDGE_DOCUMENT | Y | - | - | - | - | - | Y |
| UNKNOWN | Y | - | - | - | - | - | Y |

**Per-cell rationale notes:**
- **AGENT_DEFINITION + YAML:** Agent definitions use `---`-delimited YAML frontmatter for `name`, `version`, `model`, etc. (H-34).
- **AGENT_DEFINITION + XML:** Agent body uses `<identity>`, `<methodology>`, etc. tags per `agent-development-standards.md`.
- **RULE_FILE + Reinject:** Rule files contain `<!-- L2-REINJECT: ... -->` directives for L2 enforcement.
- **ADR + HTML:** ADRs use `<!-- PS-ID: ... | ENTRY: ... -->` for provenance metadata.
- **STRATEGY_TEMPLATE - NavTable:** Strategy templates are short-form documents; nav table is not required.
- **UNKNOWN + NavTable:** Even unclassified documents get nav table extraction for H-23 compliance checking.

---

## Design Decision 4: Schema Extension Architecture

### Decision

Extend the existing schema registry pattern in `schema.py` with a `SchemaRegistry` class that supports dynamic registration of new file-type schemas, collision detection, and post-initialization immutability via `freeze()`.

```python
# Extended in src/domain/markdown_ast/schema.py

from types import MappingProxyType

class SchemaRegistry:
    """Registry for file-type schemas with dynamic registration and freeze support."""

    def __init__(self) -> None:
        self._schemas: dict[str, EntitySchema] = {}
        self._frozen: bool = False

    def register(self, schema: EntitySchema) -> None:
        """Register a schema. Raises ValueError on key collision (T-SV-04 prevention).
        Raises RuntimeError if registry is frozen.

        Registration protocol:
        1. Call register() for each schema at module load time.
        2. Call freeze() after all registrations are complete.
        3. After freeze(), register() raises RuntimeError.
        """
        if self._frozen:
            raise RuntimeError(
                f"Cannot register schema '{schema.entity_type}': registry is frozen. "
                f"Call register() before freeze()."
            )
        if schema.entity_type in self._schemas:
            raise ValueError(
                f"Schema '{schema.entity_type}' already registered. "
                f"Key collision detected (T-SV-04)."
            )
        self._schemas[schema.entity_type] = schema

    def freeze(self) -> None:
        """Freeze the registry. After this call, register() raises RuntimeError.
        The internal dict is replaced with a MappingProxyType for read-only access."""
        self._frozen = True
        # Note: MappingProxyType is used for the public view; the internal
        # dict reference is kept for get() performance but cannot be modified
        # via register() after freeze.

    @property
    def schemas(self) -> MappingProxyType[str, EntitySchema]:
        """Read-only view of registered schemas."""
        return MappingProxyType(self._schemas)

    def get(self, entity_type: str) -> EntitySchema:
        """Look up a schema by entity type. Raises ValueError if not found."""
        schema = self._schemas.get(entity_type)
        if schema is None:
            valid = ", ".join(sorted(self._schemas.keys()))
            raise ValueError(f"Unknown entity type '{entity_type}'. Valid types: {valid}.")
        return schema

    def list_types(self) -> list[str]:
        """Return all registered entity type names."""
        return sorted(self._schemas.keys())

# Module-level default registry (backward compatible)
_DEFAULT_REGISTRY = SchemaRegistry()
# ... register all schemas ...
_DEFAULT_REGISTRY.freeze()  # Freeze after module-level registration
```

### New Schemas (10 File Types)

| Entity Type | Schema Name | Key FieldRules | Key SectionRules |
|-------------|-------------|----------------|------------------|
| `agent_definition` | `AGENT_DEFINITION_SCHEMA` | name, version, description, model (from JSON Schema) | identity, capabilities, guardrails, output, constitution (YAML) + XML sections |
| `skill_definition` | `SKILL_DEFINITION_SCHEMA` | name, version, description | Agents, When to Use |
| `rule_file` | `RULE_FILE_SCHEMA` | (no frontmatter) | HARD Rules, Document Sections |
| `adr` | `ADR_SCHEMA` | PS-ID, ENTRY, AGENT (from HTML comments) | Status, Context, Decision, Consequences |
| `strategy_template` | `STRATEGY_TEMPLATE_SCHEMA` | Strategy, ID, Family (blockquote) | Prompt Template, Rubric |
| `epic` through `bug` | (existing, unchanged) | (existing) | (existing) |
| `framework_config` | `FRAMEWORK_CONFIG_SCHEMA` | (minimal) | Document Sections |
| `orchestration_artifact` | `ORCHESTRATION_SCHEMA` | (HTML comment metadata) | varies |
| `pattern_document` | `PATTERN_SCHEMA` | (blockquote metadata) | varies |
| `knowledge_document` | `KNOWLEDGE_SCHEMA` | (minimal) | Document Sections |

### Rationale

1. **Registry pattern prevents ad-hoc schema lookups.** The existing `get_entity_schema()` function uses a module-level dict (`_SCHEMA_REGISTRY` at `schema.py:530`). The `SchemaRegistry` class formalizes this with collision detection (T-SV-04) and freeze support (T-SV-05).
2. **`freeze()` prevents runtime poisoning.** After module-level registration, `freeze()` makes the registry immutable. Any attempt to register new schemas at runtime raises `RuntimeError`. The `schemas` property returns a `MappingProxyType` for read-only access.
3. **Dynamic registration enables extension.** Future file types can be added by calling `registry.register()` before `freeze()`.
4. **Backward compatibility.** The existing `get_entity_schema()` function continues to work by delegating to the default registry.

---

## Design Decision 5: CLI Extension Strategy

### Decision

Extend the existing CLI with:
1. A `--type` flag on `ast validate` and `ast frontmatter` for explicit type specification.
2. A `ast sections` subcommand for extracting XML-tagged sections.
3. A `ast metadata` subcommand for extracting HTML comment metadata.
4. A `ast detect` subcommand for showing the auto-detected document type.

### New CLI Commands

| Command | Purpose | Output |
|---------|---------|--------|
| `jerry ast validate FILE --type agent_definition` | Validate against agent definition schema | JSON validation report |
| `jerry ast frontmatter FILE --format yaml` | Extract YAML frontmatter | JSON key-value pairs |
| `jerry ast sections FILE` | Extract XML-tagged sections | JSON section list |
| `jerry ast metadata FILE` | Extract HTML comment metadata | JSON metadata blocks |
| `jerry ast detect FILE` | Show auto-detected document type | JSON with `type` field (deterministic enum value) |

**Note on `ast detect`:** The `detect` command returns a deterministic `DocumentType` enum value, not a confidence score. Path-based detection is binary (matches or doesn't); structural-cue detection uses priority ordering, not probabilistic scoring. The output includes a `method` field indicating whether path or structure was used.

### Rationale

1. **No breaking changes.** Existing commands retain their current behavior when invoked without new flags.
2. **Explicit type override.** The `--type` flag allows users to bypass auto-detection.
3. **New subcommands for new capabilities.** `ast sections` and `ast metadata` are genuinely new operations.
4. **`ast detect` for debugging.** Helps users understand which type the detector assigns.

---

## Design Decision 6: XmlSectionParser Implementation

### Decision

Use regex-based string scanning to extract XML-tagged sections. Do NOT use any XML parser library (`xml.etree.ElementTree`, `lxml`, `xml.sax`, etc.).

### Implementation Approach

```python
_SECTION_PATTERN = re.compile(
    r'^<(?P<tag>[a-z][a-z_-]*)>\s*\n'   # Opening tag on its own line
    r'(?P<content>.*?)'                   # Non-greedy content capture
    r'\n</(?P=tag)>\s*$',                 # Matching closing tag on its own line
    re.MULTILINE | re.DOTALL
)
```

### Rationale

1. **XXE prevention (M-11, T-XS-07 CWE-611).** XML parsers introduce XXE attack surface. Since Jerry's XML-like tags are not real XML, a full XML parser is unnecessary.
2. **Simplicity.** The tag format is constrained: opening tag on its own line, closing tag on its own line, tag names from a known whitelist.
3. **Performance.** Regex scanning is faster than XML parsing for simple patterns.
4. **Precedent.** The existing `reinject.py` and `frontmatter.py` use regex.

### Tag Validation Rules

| Rule | Implementation |
|------|---------------|
| Tag name must be in `ALLOWED_TAGS` | Whitelist check before content extraction |
| Nested tags of the same name are rejected | Post-match check: content does not contain `<tagname>` |
| Unclosed tags produce an error, not a partial match | Regex requires matching closing tag |
| Tags must be on their own line | `^` and `$` anchors with `re.MULTILINE` |
| Content is trimmed of leading/trailing whitespace | `.strip()` on extracted content |
| Max content length per section enforced | `InputBounds.max_value_length` check |
| **Tag-in-content limitation** | Content discussing tags as examples may be consumed; use backtick code blocks for examples |

---

## Design Decision 7: HtmlCommentMetadata Implementation

### Decision

Extract HTML comments matching the ADR metadata pattern (`<!-- key: value | key: value -->`) using regex. Distinguish from L2-REINJECT comments by pattern exclusion.

### Implementation Approach

```python
# ADR metadata pattern: <!-- PS-ID: value | ENTRY: value | AGENT: value -->
_METADATA_COMMENT_PATTERN = re.compile(
    r'<!--\s*(?!(?i)L2-REINJECT:)'  # Case-insensitive negative lookahead
    r'(?P<body>.*?'                  # Non-greedy body (NOT [^>]*)
    r'(?:\w+\s*:\s*[^|]*?)'         # At least one key: value pair
    r'(?:\s*\|\s*\w+\s*:\s*[^|]*?)*'  # Optional additional | key: value pairs
    r')\s*-->',                      # First --> terminates (M-13)
    re.MULTILINE
)
```

### Rationale

1. **L2-REINJECT exclusion (T-HC-04 CWE-94, T-HC-07 CWE-284).** The case-insensitive negative lookahead `(?!(?i)L2-REINJECT:)` ensures that L2-REINJECT directives (handled by `reinject.py`) are not extracted twice, and prevents case-variant bypasses (`l2-reinject:`, `L2-Reinject:`).
2. **First `-->` termination (M-13, T-HC-03 CWE-74).** The non-greedy `.*?` matches up to the first `-->`. Values containing `-->` cause the match to end early (truncation over injection).
3. **No `[^>]` bug (FM-007-B1 fix).** The regex uses `.*?` (non-greedy any-character) instead of `[^>]*` (no-greater-than character class). The `[^>]` pattern incorrectly rejects `>` inside metadata values.
4. **Pipe-separated key-value format.** The ADR metadata format uses `|` as a field separator.

---

## Design Decision 8: Input Bounds Enforcement

### Decision

Create a dedicated `InputBounds` configuration class that all parsers accept as an optional parameter. Default bounds are security-conscious; callers may relax them with documented justification.

```python
# src/domain/markdown_ast/input_bounds.py

@dataclass(frozen=True)
class InputBounds:
    """Configurable resource limits for parser input validation."""

    max_file_bytes: int = 1_048_576         # 1 MB (M-05)
    max_yaml_block_bytes: int = 32_768      # 32 KB pre-parse (M-07)
    max_yaml_result_bytes: int = 65_536     # 64 KB post-parse (M-20, closes temporal gap)
    max_alias_count: int = 10               # Max YAML anchor/alias references (M-20)
    max_frontmatter_keys: int = 100         # (M-16)
    max_nesting_depth: int = 5              # (M-06)
    max_section_count: int = 20             # (M-16)
    max_comment_count: int = 50             # (M-16)
    max_value_length: int = 10_000          # characters (M-17)
    max_reinject_count: int = 50            # (M-16)

    # Default singleton
    DEFAULT: ClassVar[InputBounds]

InputBounds.DEFAULT = InputBounds()
```

### Rationale

1. **Centralized configuration.** All bounds are in one frozen dataclass, making them auditable and testable.
2. **Opt-in relaxation.** Parsers use `InputBounds.DEFAULT` unless the caller provides a custom instance.
3. **Frozen immutability.** Bounds cannot be modified after construction.
4. **Documented defaults.** Each default value references the threat model mitigation that justifies it.
5. **Temporal gap closure (T-YF-06 CWE-776, T-YF-05 CWE-400).** `max_yaml_result_bytes` (M-20) closes the gap between pre-parse input size (M-07) and post-parse depth check (M-06) -- `yaml.safe_load()` expands anchors/aliases IN MEMORY during parsing.
6. **Alias count limit.** `max_alias_count` provides an additional pre-parse defense: count `*` references in the raw YAML block before calling `yaml.safe_load()`.

---

## Design Decision 9: Error Handling Strategy

### Decision

All parsers return **result objects with typed error fields**. Parsers MUST NOT raise exceptions for parse failures. The `UniversalParseResult` aggregates parse errors from all invoked parsers.

### Error Handling Pattern

```python
# Each parser returns a result object with an error field:
#   parse_error: str | None  -- None if parsing succeeded, error message if failed

# UniversalParseResult aggregates errors:
#   parse_errors: tuple[str, ...]  -- Aggregated errors from all invoked parsers

# Parser implementation pattern:
class YamlFrontmatter:
    @staticmethod
    def extract(doc: JerryDocument, bounds: InputBounds | None = None) -> YamlFrontmatterResult:
        try:
            yaml_block = _extract_yaml_block(doc.source)
            # ... pre-parse checks ...
            result = yaml.safe_load(yaml_block)
            # ... post-parse checks ...
            return YamlFrontmatterResult(fields=..., parse_error=None)
        except yaml.scanner.ScannerError as e:
            return YamlFrontmatterResult(fields=(), parse_error=f"YAML scan error at line {e.problem_mark.line}: {e.problem}")
        except yaml.parser.ParserError as e:
            return YamlFrontmatterResult(fields=(), parse_error=f"YAML parse error at line {e.problem_mark.line}: {e.problem}")
        except yaml.constructor.ConstructorError as e:
            return YamlFrontmatterResult(fields=(), parse_error=f"YAML construction error: {e.problem}")
```

### Rationale

1. **Uniform error reporting.** Callers can distinguish "parser not invoked" (`None` result) from "parser invoked successfully" (result with `parse_error=None`) from "parser invoked and failed" (result with `parse_error` set).
2. **No exception propagation.** Parse failures are expected in a tool that processes untrusted markdown. Exceptions should not bubble up to the CLI layer unhandled.
3. **Error aggregation.** `UniversalParseResult.parse_errors` collects all parser errors, making it easy to report all issues in a single CLI output.
4. **Sanitized messages (T-YF-04 CWE-209).** Error messages include error type and line number but exclude raw file content and full file paths (M-19).

---

## Design Decision 10: YAML Type Normalization

### Decision

`yaml.safe_load()` produces typed Python values (bool, int, float, None), but the existing schema validation engine (`schema.py`) expects string values for `FieldRule.allowed_values` matching. The YamlFrontmatter parser normalizes all values to their string representation for schema compatibility.

### Type Normalization Rules

| YAML Input | `yaml.safe_load()` Result | Normalized Value | Type String |
|------------|--------------------------|------------------|-------------|
| `name: opus` | `str("opus")` | `"opus"` | `"str"` |
| `version: 1.0.0` | `str("1.0.0")` | `"1.0.0"` | `"str"` |
| `required: true` | `bool(True)` | `"true"` | `"bool"` |
| `required: false` | `bool(False)` | `"false"` | `"bool"` |
| `count: 42` | `int(42)` | `"42"` | `"int"` |
| `score: 3.14` | `float(3.14)` | `"3.14"` | `"float"` |
| `value: null` | `None` | `"null"` | `"null"` |
| `items: [a, b]` | `list(["a", "b"])` | `"a, b"` | `"list"` |

### Rationale

1. **Schema compatibility (T-YF-07 CWE-502 mitigation dependency).** The existing `FieldRule.allowed_values` and `value_pattern` operate on strings. Converting typed values to their canonical string representation enables reuse of the existing validation engine. Type normalization operates on `yaml.safe_load()` output, which is restricted to basic Python types (str, int, float, bool, list, dict, None) — the `safe_load()` constraint is the T-YF-07 mitigation.
2. **Original type preserved.** `YamlFrontmatterField.value` stores the original typed value; `YamlFrontmatterField.value_type` stores the type string. Schema validation operates on the normalized string; downstream consumers can use the original typed value.
3. **Predictable coercion.** The normalization rules are explicit and documented. `True` always becomes `"true"` (lowercase), not `"True"` or `"yes"`.

---

## Hexagonal Architecture Compliance

### H-07 Verification

| Layer | Components | Import Rules | Compliance |
|-------|-----------|-------------|------------|
| **Domain** | `jerry_document.py`, `frontmatter.py`, `schema.py`, `nav_table.py`, `reinject.py`, `yaml_frontmatter.py`, `xml_section.py`, `html_comment.py`, `document_type.py`, `universal_document.py`, `input_bounds.py` | MUST NOT import from `src/interface/`, `src/application/`, `src/infrastructure/` | PASS: All domain classes import only from `src/domain/markdown_ast/` and standard library / PyYAML |
| **Interface** | `ast_commands.py` | MAY import from domain | PASS: Imports from `src/domain/markdown_ast` |
| **Application** | (none for AST skill) | -- | N/A |
| **Infrastructure** | (none for AST skill) | -- | N/A |

### Dependency Direction Verification

```
Interface Layer (ast_commands.py)
    |
    | imports
    v
Domain Layer (universal_document.py, etc.)
    |
    | imports
    v
Standard Library + PyYAML (safe_load only) + markdown-it-py + mdformat
```

All dependency arrows point inward (toward domain) or downward (toward libraries). No outward arrows from domain to interface/application/infrastructure. **H-07 compliance: PASS.**

---

## One-Class-Per-File Compliance

### H-10 Verification

| File | Primary Class | Supporting Types | H-10 Compliance |
|------|---------------|------------------|-----------------|
| `jerry_document.py` | `JerryDocument` | (none) | PASS |
| `frontmatter.py` | `BlockquoteFrontmatter` | `FrontmatterField` (data class, migrated to frozen=True) | PASS (data class is supporting type) |
| `yaml_frontmatter.py` | `YamlFrontmatter` | `YamlFrontmatterField`, `YamlFrontmatterResult` (data classes) | PASS |
| `xml_section.py` | `XmlSectionParser` | `XmlSection`, `XmlSectionResult` (data classes) | PASS |
| `html_comment.py` | `HtmlCommentMetadata` | `HtmlCommentField`, `HtmlCommentBlock`, `HtmlCommentResult` (data classes) | PASS |
| `document_type.py` | `DocumentTypeDetector` | `DocumentType` (enum) | PASS |
| `universal_document.py` | `UniversalDocument` | `UniversalParseResult` (data class) | PASS |
| `input_bounds.py` | `InputBounds` | (none) | PASS |
| `schema.py` | `SchemaRegistry` (new) + existing validation | `EntitySchema`, `FieldRule`, `SectionRule`, `ValidationViolation`, `ValidationReport` (data classes) | PASS |
| `nav_table.py` | (functions, no primary class) | `NavEntry`, `NavValidationResult` (data classes) | PASS (utility module pattern) |
| `reinject.py` | (functions, no primary class) | `ReinjectDirective` (data class) | PASS (utility module pattern) |

**Note on H-10 interpretation:** Frozen data classes that serve as the return type or parameter type of the primary class in the same file are considered supporting types, not separate behavioral classes.

---

## H-33 Compliance Strategy

### Boundary Definition

H-33 requires AST-based parsing for worktracker entity operations. This ADR extends AST-based parsing to ALL 10 file types. The boundary between H-33-mandatory and H-33-optional operations is:

| Operation | H-33 Mandatory? | Rationale |
|-----------|:---:|-----------|
| Worktracker entity frontmatter extraction | YES | Core H-33 requirement |
| Worktracker entity validation | YES | Core H-33 requirement |
| Agent definition YAML parsing | YES (via H-34) | H-34 requires JSON Schema validation of agent YAML |
| XML section extraction | NO (optional) | Enhancement; not required by any HARD rule |
| HTML comment metadata | NO (optional) | Enhancement; not required by any HARD rule |
| Document type detection | NO (optional) | Routing utility; not a structural requirement |
| Universal document parsing | NO (wrapper) | Convenience facade; delegates to H-33-mandatory parsers |

### CLI Integration

The `jerry ast frontmatter` and `jerry ast validate` commands remain the H-33 enforcement points. The new `jerry ast sections`, `jerry ast metadata`, and `jerry ast detect` commands are extensions that do not affect H-33 compliance.

---

## Performance Requirements

### Baseline Expectations

| Operation | Target Latency | Target Memory | Justification |
|-----------|---------------|---------------|---------------|
| Document type detection | < 1ms | < 1 MB | Path pattern matching is O(n) on pattern count; structural cue matching is O(n) on content length |
| YAML frontmatter extraction | < 50ms for 32KB block | < 64 MB (bounded by M-20) | `yaml.safe_load()` is CPU-bound; M-20 caps memory |
| XML section extraction | < 10ms for typical agent def | < 10 MB | Regex scan is O(n) on content length |
| HTML comment extraction | < 10ms for typical ADR | < 10 MB | Regex scan is O(n) on content length |
| Blockquote frontmatter (existing) | < 5ms (measured baseline) | < 5 MB | Existing performance, unchanged |
| Schema validation | < 10ms per schema | < 1 MB | Field/section rule matching is O(n * m) |
| Full universal parse | < 100ms for typical file | < 64 MB | Sum of component latencies |

### Performance Constraints

1. **No O(2^n) operations.** All regex patterns MUST avoid nested quantifiers that cause exponential backtracking (M-12). Pattern review is required during Phase 3 testing.
2. **Memory bounded by InputBounds.** Maximum memory consumption is bounded by `max_file_bytes` (1 MB input) + `max_yaml_result_bytes` (64 KB post-parse). The theoretical maximum is approximately 65 MB for a pathological file that maximizes all parser allocations.
3. **No lazy evaluation.** All parser results are fully materialized before returning. No generator-based streaming (simplifies error handling and immutability).

For context, Python markdown-it-py parses a 100KB markdown file in approximately 50ms on modern hardware, consistent with our universal parse target of <100ms for typical files.

**Measurement status:** Target latencies above are estimates based on algorithmic complexity analysis, not measured benchmarks. Phase 3 testing will validate these targets; deviations exceeding 2x will trigger performance investigation.

---

## Migration Safety

### Pre-existing Defect: FrontmatterField Mutability

The existing `FrontmatterField` at `frontmatter.py:54` uses `@dataclass` without `frozen=True`. This is a **P0 prerequisite migration** that must be completed before the universal parser can claim immutability as a defense-in-depth property.

**Migration task:**
1. Change `@dataclass` to `@dataclass(frozen=True)` on `FrontmatterField`.
2. Verify no code in the codebase mutates `FrontmatterField` attributes (search for `field.key =`, `field.value =`, etc.).
3. Run existing test suite to confirm no regressions.

### Golden-File Test Suite

A golden-file test suite validates that the universal parser produces identical output to the existing parsers for all known file patterns:

| Test Category | Source Files | Assertion |
|--------------|-------------|-----------|
| Worktracker entities | All `projects/**/work/**/*.md` files | `UniversalDocument.parse()` frontmatter == `BlockquoteFrontmatter.extract()` frontmatter |
| Rule files | All `.context/rules/*.md` files | `UniversalDocument.parse()` reinject directives == `extract_reinject_directives()` output |
| Existing schemas | All 6 worktracker entity types | `validate_document(doc, schema)` unchanged |

### Canary Mode

A `--legacy` flag on `ast validate` and `ast frontmatter` forces the use of existing parsers (bypassing `UniversalDocument`). This enables side-by-side comparison during rollout:

```bash
# Compare outputs:
jerry ast frontmatter FILE              # New universal parser
jerry ast frontmatter FILE --legacy     # Existing BlockquoteFrontmatter only
diff <(jerry ast frontmatter FILE) <(jerry ast frontmatter FILE --legacy)
```

### Pattern Collision Test Suite

A dedicated test validates that no file path in the repository matches multiple `PATH_PATTERNS` entries. The test:
1. Enumerates all `.md` files in the repository.
2. For each file, runs `DocumentTypeDetector.detect()` and records which patterns matched.
3. Fails if any file matches 2+ patterns (indicating an ordering ambiguity).

---

## Consequences

### Positive

1. **Unified parsing API.** All 10 file types are parseable through a single `UniversalDocument.parse()` call.
2. **Automated validation.** New schemas enable CI/CD structural validation of agent definitions, SKILL.md files, ADRs, and other framework documents.
3. **H-34 enablement.** YAML frontmatter parsing enables JSON Schema validation of agent definitions.
4. **Security-by-design.** Input bounds (including post-parse result size verification M-20), `yaml.safe_load()` enforcement with triple defense-in-depth, no-XML-parser constraints, `SchemaRegistry.freeze()`, and `tuple` containers for deep immutability are architectural decisions.
5. **Backward compatibility.** Existing `JerryDocument` users are unaffected. The `BlockquoteFrontmatter` API is unchanged (except `FrontmatterField` gains `frozen=True`).

### Negative

1. **Increased codebase size.** Five new domain files (~800-1200 lines total estimated) and CLI extensions increase maintenance surface.
2. **PyYAML dependency.** While already present in the project, the AST skill now has a direct dependency on PyYAML, coupling it to PyYAML's security posture.
3. **Schema maintenance burden.** Ten file-type schemas require ongoing maintenance as file formats evolve.
4. **Detection ambiguity.** Files that don't match known path patterns rely on structural detection, which is inherently less reliable than path-based detection.
5. **FrontmatterField migration.** The `frozen=True` migration is a breaking change if any code mutates `FrontmatterField` attributes (unlikely but must be verified).

### Neutral

1. **Performance impact bounded.** `UniversalDocument` only invokes parsers relevant to the detected type. Performance targets are documented in [Performance Requirements](#performance-requirements). Actual benchmarks will be collected during Phase 3 testing.
2. **No API changes to existing CLI commands.** New functionality is additive.

---

## Alternatives Considered

### Alternative 1: Single Parser with Format Auto-Detection

**Rejected.** A single parser class that internally handles all formats would violate the Single Responsibility Principle, create a monolithic class difficult to test and review, and mix the security profiles of different format parsers.

### Alternative 2: Full XML Parser for Section Extraction

**Rejected.** Using `xml.etree.ElementTree` or `lxml` would introduce XXE (XML External Entity) attack surface (T-XS-07, DREAD 33). The tag format is simple enough for regex. `defusedxml` mitigates XXE but adds a dependency for no functional benefit over regex. The ADR mandates regex-only parsing (DD-6).

### Alternative 3: Extending JerryDocument Instead of Creating UniversalDocument

**Rejected.** Adding YAML, XML, and HTML comment parsing to `JerryDocument` would bloat the class, violate Single Responsibility, and break H-10. The facade pattern preserves clean separation.

### Alternative 4: Using `ruamel.yaml` Instead of PyYAML

**Considered but deferred.** `ruamel.yaml` preserves YAML comments and formatting, which would improve write-back fidelity. However, PyYAML is already a project dependency, `ruamel.yaml` is a larger library with more attack surface, and write-back for YAML frontmatter is not in the initial scope.

### Alternative 5: Plugin-Based Parser Architecture

**Rejected.** A plugin system (entry points, dynamic loading) adds complexity disproportionate to the current scale (10 file types, 4 parsers). The registry pattern provides extensibility without dynamic loading overhead or security risks.

---

## Strategic Implications (L2)

### Architecture Evolution Path

1. **Phase 1 (this ADR):** Read-only universal parsing. All new parsers extract data; no write-back for new formats. `FrontmatterField` migrated to `frozen=True`.
2. **Phase 2 (future):** Write-back for YAML frontmatter. Requires `ruamel.yaml` evaluation or custom YAML serialization.
3. **Phase 3 (future):** CI/CD integration. `jerry ast validate --type agent_definition --schema agent-definition-v1` as a pre-commit hook and GitHub Actions step.
4. **Phase 4 (future):** Cross-file validation. Validate that entity references (Parent, children) resolve to existing files.

### Security Posture

The architecture decisions in this ADR establish a security-first foundation:
- **No arbitrary deserialization:** `yaml.safe_load()` is an architectural constraint with triple enforcement (lint rule, AST test, CI grep).
- **No XML parser:** XXE is eliminated by architecture, not by configuration.
- **Deep immutability:** `frozen=True` dataclasses with `tuple` containers prevent both attribute reassignment and container mutation.
- **Input bounds by default:** Resource exhaustion requires explicit opt-in relaxation. Post-parse result size verification (M-20) closes the temporal gap in YAML expansion.
- **Registry freeze:** `SchemaRegistry.freeze()` prevents runtime schema poisoning.
- **Governance trust boundary:** L2-REINJECT extraction requires file-origin trust checking (M-22).

These constraints should be preserved as the parser evolves. Any proposal to relax them requires a new threat model and C4-level ADR.

---

## References

| Source | Content | Location |
|--------|---------|----------|
| Threat Model | STRIDE, DREAD, Attack Trees, PASTA for universal parser | `projects/PROJ-005-markdown-ast/orchestration/ast-universal-20260222-001/eng/phase-1-architecture/eng-architect-001/eng-architect-001-threat-model.md` |
| Trust Boundaries | ASCII trust boundary diagram | `projects/PROJ-005-markdown-ast/orchestration/ast-universal-20260222-001/eng/phase-1-architecture/eng-architect-001/eng-architect-001-trust-boundaries.md` |
| Agent Definition Schema | JSON Schema for YAML frontmatter validation | `docs/schemas/agent-definition-v1.schema.json` |
| Existing AST Implementation | JerryDocument, BlockquoteFrontmatter, schema.py | `src/domain/markdown_ast/` |
| Agent Development Standards | H-34, agent definition format | `.context/rules/agent-development-standards.md` |
| Quality Enforcement | H-07, H-10, H-33 | `.context/rules/quality-enforcement.md` |
| PyYAML safe_load | Safe YAML deserialization documentation | PyYAML docs: `yaml.safe_load()` |
| OWASP XXE Prevention | XML External Entity attack prevention | OWASP XXE Prevention Cheat Sheet |

---

## Disclaimer

This ADR is based on the proposed architecture as of 2026-02-22. Implementation details may evolve during development. All security constraints (C-04 through C-07) are non-negotiable; any deviation requires a new C4-level ADR with updated threat model.

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-22 | Initial ADR |
| 2.3.0 | 2026-02-23 | **Iteration 5 final revisions.** Added threat model forward-references (threat IDs + CWE numbers) to design decision rationales: DD-1 (T-YF-07, T-XS-07), DD-6 (T-XS-07), DD-7 (T-HC-04, T-HC-07, T-HC-03), DD-8 (T-YF-06, T-YF-05), DD-9 (T-YF-04), DD-10 (T-YF-07). Establishes bidirectional traceability between architecture decisions and threat model. |
| 2.2.0 | 2026-02-23 | **Iteration 4 targeted revisions for 0.95 threshold.** Added comparative performance context (markdown-it-py 50ms benchmark) to Performance Requirements section. |
| 2.1.0 | 2026-02-22 | **Iteration 3 targeted revisions:** Added measurement status caveat to Performance Requirements section noting target latencies are estimates pending Phase 3 validation. |
| 2.0.0 | 2026-02-22 | **Iteration 2 revisions:** (P0) T-01: Added C-05 revision note acknowledging FrontmatterField mutability defect, documented P0 migration task in Migration Safety section; (P0) T-02: Added `max_yaml_result_bytes` (64KB) and `max_alias_count` (10) to InputBounds (DD-8), documented temporal gap closure in DD-8 rationale; (P0) T-04: Added case-insensitive negative lookahead in DD-7, referenced M-22 trusted path whitelist; (P0) T-03: Changed all `list[...]` containers in UniversalParseResult to `tuple[..., ...]`, updated DD-3 rationale for deep immutability; (P1) T-05: Added `freeze()` method and `MappingProxyType` to SchemaRegistry (DD-4), documented registration protocol; (P1) T-06: Added DD-9 (Error Handling Strategy) with per-parser result objects and error aggregation; (P1) T-07: Documented first-match-wins semantics and structural cue priority in DD-2, added collision test requirement; (P1) FM-002-B1: Specified yaml exception types in DD-1 and DD-9; (P1) FM-003-B1: Added duplicate key detection in DD-1 YamlFrontmatter constraints; (P1) FM-004-B1: Added first-pair-only extraction rule in DD-1; (P1) FM-005-B1: Documented tag-in-content limitation in DD-6; (P1) FM-007-B1: Fixed HtmlComment regex from `[^>]` to non-greedy `.*?` in DD-7; (P1) PM-001-B1: Added Migration Safety section with golden-file test suite, canary mode, --legacy flag; (P1) PM-008-B1: Added DD-10 (YAML Type Normalization); (P1) IN-001-B1: Updated C-04 constraint to include M-04a AST test and M-04b CI grep; (P2) SM-002-B1: Added per-cell rationale to parser invocation matrix; (P2) PM-007-B1: Added Performance Requirements section; (P2) CC-006-B1: Added H-33 Compliance Strategy section; (P2) SR-009-B1: Added registration protocol in DD-4; (P2) FM-018-B1: Removed possessive quantifier guidance from implicit references. |

---

<!-- VERSION: 2.3.0 | DATE: 2026-02-23 | AGENT: eng-architect | ENGAGEMENT: ENG-0001 -->
