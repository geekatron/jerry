# Trust Boundary Diagram: Universal Markdown Parser

<!-- ENG-ARCHITECT-001 | ENGAGEMENT: ENG-0001 | PROJECT: PROJ-005 | CRITICALITY: C4 -->
<!-- DATE: 2026-02-22 | AUTHOR: eng-architect -->
<!-- REVISION: 4 | PREVIOUS-SCORE: 0.944 (REVISE) | DATE: 2026-02-23 -->

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary (L0)](#executive-summary-l0) | Stakeholder-level trust boundary overview |
| [Primary Trust Boundary Diagram](#primary-trust-boundary-diagram) | Main ASCII diagram showing all six trust zones |
| [Detailed Boundary Crossings](#detailed-boundary-crossings) | Per-crossing data transformation and validation |
| [Parser-Specific Data Flow Diagrams](#parser-specific-data-flow-diagrams) | Per-parser input-to-output flows |
| [Schema Validation Checkpoint Diagram](#schema-validation-checkpoint-diagram) | Where validation occurs in the pipeline |
| [Write-Back Path Diagram](#write-back-path-diagram) | Output path trust analysis |
| [Threat Overlay](#threat-overlay) | Where threats map to boundaries |
| [Strategic Implications (L2)](#strategic-implications-l2) | Security architecture considerations |
| [Disclaimer](#disclaimer) | Limitations and assumptions |
| [Revision History](#revision-history) | Change log for this document |

---

## Executive Summary (L0)

The universal markdown parser operates across **six trust zones** with five boundary crossings. The primary trust boundary is **BC-02: File Content to Parser** -- where untrusted file content is transformed into typed structures by format-specific parsers. All new parsers produce frozen (immutable) domain objects with `tuple` containers, creating a one-way trust amplification: once content crosses BC-03 into the domain object zone, it cannot be modified. The diagrams below show the complete flow from CLI input through parsing, validation, and output, with validation checkpoints marked at each boundary crossing.

**Pre-existing defect note:** The existing `FrontmatterField` at `frontmatter.py:54` uses `@dataclass` without `frozen=True`. This is a P0 prerequisite migration -- until corrected, Zone 4's immutability assertion does not hold for blockquote frontmatter fields. All NEW domain objects use `frozen=True` with `tuple` containers from the start.

---

## Primary Trust Boundary Diagram

```
+===========================================================================+
||                                                                         ||
||  ZONE 1: CLI INPUT (UNTRUSTED)                                          ||
||  +-----------------------------------------------------------------+    ||
||  |  User-supplied arguments:                                       |    ||
||  |    - file_path: string (may contain ../traversal)               |    ||
||  |    - --type: optional document type override                    |    ||
||  |    - --schema: optional schema type                             |    ||
||  |    - key/value: for ast modify                                  |    ||
||  +-----------------------------------------------------------------+    ||
||                                                                         ||
+=============================== BC-01 ====================================+
   |                    BOUNDARY CROSSING 01                        |
   |  Validation: path existence, path containment (M-08),         |
   |              file size limit (M-05), UTF-8 encoding check,    |
   |              symlink resolution (M-10)                        |
   v                                                               v
+===========================================================================+
||                                                                         ||
||  ZONE 2: FILE CONTENT (UNTRUSTED)                                       ||
||  +-----------------------------------------------------------------+    ||
||  |  Raw file bytes read from disk via Path.read_text():            |    ||
||  |    - Markdown source text (may contain any content)             |    ||
||  |    - Embedded YAML blocks (--- delimited)                       |    ||
||  |    - Embedded XML-like tags (<identity>, etc.)                  |    ||
||  |    - Embedded HTML comments (<!-- key: value -->)               |    ||
||  |    - Embedded L2-REINJECT directives                            |    ||
||  |    - Blockquote frontmatter (> **Key:** Value)                  |    ||
||  +-----------------------------------------------------------------+    ||
||                                                                         ||
||  +-----------------------------------------------------------------+    ||
||  |  DocumentTypeDetector.detect(path, content)                     |    ||
||  |    IN:  file_path (Z1) + content (Z2)                          |    ||
||  |    OUT: DocumentType enum                                       |    ||
||  |    Path patterns: first-match-wins (ordered list)              |    ||
||  |    Structural cues: priority order (YAML>blockquote>XML>HTML)   |    ||
||  +-----------------------------------------------------------------+    ||
||                                                                         ||
+=============================== BC-02 ====================================+
   |                    BOUNDARY CROSSING 02                        |
   |  Validation: InputBounds enforcement (M-05, M-06, M-07,      |
   |              M-16, M-17, M-20), format-specific checks,       |
   |              L2-REINJECT trusted path check (M-22)            |
   v                                                               v
+===========================================================================+
||                                                                         ||
||  ZONE 3: PARSER LAYER (SEMI-TRUSTED)                                    ||
||  +-----------------------------------------------------------------+    ||
||  |                                                                 |    ||
||  |  +-------------------+  +-------------------+                   |    ||
||  |  | JerryDocument     |  | YamlFrontmatter   |                   |    ||
||  |  | .parse()          |  | .extract()        |                   |    ||
||  |  | markdown-it-py    |  | yaml.safe_load()  |   <-- CRITICAL   |    ||
||  |  | commonmark mode   |  | ONLY. NEVER       |       CONTROL    |    ||
||  |  |                   |  | yaml.load() or    |       POINT      |    ||
||  |  |                   |  | yaml.unsafe_load()|                   |    ||
||  |  |                   |  | Post-parse M-20:  |                   |    ||
||  |  |                   |  | result size check  |                   |    ||
||  |  +-------------------+  +-------------------+                   |    ||
||  |                                                                 |    ||
||  |  +-------------------+  +-------------------+                   |    ||
||  |  | BlockquoteFront-  |  | XmlSectionParser  |                   |    ||
||  |  | matter.extract()  |  | .extract()        |                   |    ||
||  |  | regex: > **K:** V |  | regex ONLY        |   <-- NO XML     |    ||
||  |  | (existing impl)   |  | NO xml.etree      |       PARSER     |    ||
||  |  |                   |  | NO lxml           |       ALLOWED    |    ||
||  |  +-------------------+  +-------------------+                   |    ||
||  |                                                                 |    ||
||  |  +-------------------+  +-------------------+                   |    ||
||  |  | HtmlCommentMeta-  |  | extract_reinject_ |                   |    ||
||  |  | data.extract()    |  | directives()      |                   |    ||
||  |  | regex: <!-- k:v-->|  | regex: L2-REINJECT|                   |    ||
||  |  | excludes REINJECT |  | (existing impl)   |                   |    ||
||  |  | (case-insensitive)|  | TRUSTED PATHS     |   <-- M-22      |    ||
||  |  +-------------------+  | REQUIRED          |       GOVERNANCE |    ||
||  |                         +-------------------+       BOUNDARY   |    ||
||  |                                                                 |    ||
||  |  +-------------------+                                          |    ||
||  |  | extract_nav_      |                                          |    ||
||  |  | table()           |                                          |    ||
||  |  | regex: nav rows   |                                          |    ||
||  |  | (existing impl)   |                                          |    ||
||  |  +-------------------+                                          |    ||
||  |                                                                 |    ||
||  +-----------------------------------------------------------------+    ||
||                                                                         ||
+=============================== BC-03 ====================================+
   |                    BOUNDARY CROSSING 03                        |
   |  Validation: type checking, value sanitization (M-18),        |
   |              immutability enforcement (frozen dataclass +     |
   |              tuple containers), control character stripping   |
   v                                                               v
+===========================================================================+
||                                                                         ||
||  ZONE 4: DOMAIN OBJECTS (TRUSTED)                                       ||
||  +-----------------------------------------------------------------+    ||
||  |  All NEW objects are frozen dataclasses with tuple containers   |    ||
||  |  (IMMUTABLE after creation -- both attribute and container):   |    ||
||  |                                                                 |    ||
||  |  UniversalParseResult (frozen)                                  |    ||
||  |    .document_type: DocumentType (enum)                          |    ||
||  |    .jerry_document: JerryDocument (source, tokens, tree)        |    ||
||  |    .yaml_frontmatter: YamlFrontmatterResult | None              |    ||
||  |      .fields: tuple[YamlFrontmatterField, ...] (frozen)        |    ||
||  |    .blockquote_frontmatter: BlockquoteFrontmatter | None        |    ||
||  |      ._fields: list[FrontmatterField]                           |    ||
||  |        ^^^ EXISTING DEFECT: FrontmatterField is NOT frozen.    |    ||
||  |        P0 migration to frozen=True required (see ADR C-05).    |    ||
||  |    .xml_sections: tuple[XmlSection, ...] | None (frozen items) |    ||
||  |    .html_comments: tuple[HtmlCommentBlock, ...] | None (frozen)|    ||
||  |    .reinject_directives: tuple[ReinjectDirective, ...] (frozen)|    ||
||  |    .nav_entries: tuple[NavEntry, ...] | None (frozen items)    |    ||
||  |    .type_detection_warning: str | None                          |    ||
||  |    .parse_errors: tuple[str, ...] (aggregated parser errors)   |    ||
||  |                                                                 |    ||
||  |  IMMUTABILITY NOTE:                                             |    ||
||  |  - frozen=True prevents attribute reassignment                  |    ||
||  |  - tuple containers prevent append/extend/mutation              |    ||
||  |  - Combined: result.xml_sections.append(x) -> AttributeError  |    ||
||  |  - EXCEPTION: FrontmatterField (pre-existing, not yet frozen)  |    ||
||  |  - NOTE: `BlockquoteFrontmatter` stores fields in a mutable   |    ||
||  |    `list[FrontmatterField]` (see `frontmatter.py:131`). The   |    ||
||  |    P0 migration to `frozen=True` on `FrontmatterField`        |    ||
||  |    addresses attribute mutability but does not address the     |    ||
||  |    mutable `_fields` list container. A separate migration to  |    ||
||  |    `tuple` for the internal `_fields` storage is recommended  |    ||
||  |    as a Phase 2 implementation task.                           |    ||
||  |  - **Demonstration:** `fm = BlockquoteFrontmatter.extract(doc);|    ||
||  |    fm._fields.append(spoofed_field)` succeeds on the current   |    ||
||  |    implementation, adding an unauthorized field to the parsed   |    ||
||  |    result. After `tuple` migration:                            |    ||
||  |    `fm._fields.append(spoofed_field)` raises `AttributeError`. |    ||
||  |  - Python dataclass frozen=True does NOT enforce type           |    ||
||  |    annotations at runtime; types are enforced by construction   |    ||
||  |    discipline in the parser layer (Zone 3)                      |    ||
||  |                                                                 |    ||
||  +-----------------------------------------------------------------+    ||
||                                                                         ||
+=============================== BC-04 ====================================+
   |                    BOUNDARY CROSSING 04                        |
   |  Validation: schema rule application, field/section checks,   |
   |              nav table validation (H-23)                       |
   v                                                               v
+===========================================================================+
||                                                                         ||
||  ZONE 5: SCHEMA VALIDATION (TRUSTED)                                    ||
||  +-----------------------------------------------------------------+    ||
||  |  validate_document(doc, schema) -> ValidationReport             |    ||
||  |                                                                 |    ||
||  |  SchemaRegistry (frozen after module-level registration)        |    ||
||  |    .get(entity_type) -> EntitySchema                            |    ||
||  |    .freeze() called at module load -> prevents runtime poison   |    ||
||  |    .schemas -> MappingProxyType (read-only view)                |    ||
||  |                                                                 |    ||
||  |  EntitySchema (frozen)                                          |    ||
||  |    .field_rules: tuple[FieldRule, ...]                          |    ||
||  |      - required field checks                                   |    ||
||  |      - allowed_values enum checks                              |    ||
||  |      - value_pattern regex checks (ReDoS-safe per M-12)        |    ||
||  |    .section_rules: tuple[SectionRule, ...]                      |    ||
||  |      - required heading checks                                 |    ||
||  |    .require_nav_table: bool                                     |    ||
||  |                                                                 |    ||
||  |  ValidationReport (frozen)                                      |    ||
||  |    .is_valid: bool                                              |    ||
||  |    .violations: tuple[ValidationViolation, ...]                 |    ||
||  |                                                                 |    ||
||  +-----------------------------------------------------------------+    ||
||                                                                         ||
+===========================================================================+
   |
   |  BC-05a: JSON output to stdout (read path, safe)
   |  BC-05b: Write-back to file (modify path, requires TOCTOU mitigation)
   v
+===========================================================================+
||                                                                         ||
||  ZONE 6: FILE SYSTEM OUTPUT (SEMI-TRUSTED)                              ||
||  +-----------------------------------------------------------------+    ||
||  |  Read Path (ast parse, ast validate, ast frontmatter, etc.):    |    ||
||  |    - JSON serialization of domain objects to stdout              |    ||
||  |    - Error message sanitization (M-19)                          |    ||
||  |    - No file system writes                                      |    ||
||  |                                                                 |    ||
||  |  Write Path (ast modify):                                       |    ||
||  |    - Path containment re-verified (M-08)                        |    ||
||  |    - Atomic write via temp file + os.rename (M-21, TOCTOU)     |    ||
||  |    - Modified content written atomically                        |    ||
||  |    - Restricted to frontmatter value changes only               |    ||
||  +-----------------------------------------------------------------+    ||
||                                                                         ||
+===========================================================================+
```

---

## Detailed Boundary Crossings

### BC-01: CLI Input to File Content

```
CLI Arguments (Z1)                          File Content (Z2)
+------------------+                        +------------------+
| file_path: str   |----[VALIDATION]------->| content: str     |
| --type: str?     |                        | (UTF-8 decoded)  |
| --schema: str?   |                        +------------------+
+------------------+

VALIDATION CHECKS:
  [V1] Path(file_path).exists()             -> Error: "File not found" (exit code 2)
  [V2] Path(file_path).resolve().is_relative_to(repo_root)
                                            -> Error: "Path outside repository" (exit code 2) (M-08)
  [V3] Path(file_path).stat().st_size <= 1_048_576
                                            -> Error: "File exceeds 1MB limit" (exit code 2) (M-05)
  [V4] Path(file_path).read_text(encoding="utf-8")
                                            -> Error: "UTF-8 decode failed" (exit code 2)
  [V5] os.path.realpath() == resolved path  -> Warning: "Symlink detected" (M-10)
```

### BC-02: File Content to Parser

```
Raw Content (Z2)                            Parser Input (Z3)
+------------------+                        +------------------+
| markdown source  |----[VALIDATION]------->| format-specific  |
| with embedded    |                        | structures       |
| metadata         |                        +------------------+
+------------------+

VALIDATION CHECKS (per parser):

YamlFrontmatter:
  [V6]  YAML block size <= 32KB (M-07)     -> Error: "YAML block exceeds 32KB" in parse_error
  [V7]  yaml.safe_load() ONLY (M-01, M-04) -> Enforced by architecture (lint, AST test, CI grep)
  [V8]  Result key count <= 100 (M-16)     -> Error: "Exceeds max key count" in parse_error
  [V9]  Result nesting depth <= 5 (M-06)   -> Error: "Exceeds max nesting depth" in parse_error
  [V10] Result size <= 64KB (M-20)         -> Error: "YAML expansion exceeds 64KB" in parse_error
  [V11] Alias count <= 10 (M-20)           -> Error: "Exceeds max alias count" in parse_error
  [V12] First --- pair only (M-24)         -> Subsequent blocks silently ignored
  [V13] Duplicate key detection (M-23)     -> Warning in parse_warnings

XmlSectionParser:
  [V14] Tag name in ALLOWED_TAGS whitelist  -> Non-whitelisted tags silently skipped
  [V15] Section count <= 20 (M-16)         -> Error: "Exceeds max section count" in parse_error
  [V16] Content length per section <= 10,000 chars (M-17)
                                            -> Error: "Section content exceeds limit" in parse_error
  [V17] No nested same-name tags (M-15)    -> Error: "Nested same-name tag detected" in parse_error

HtmlCommentMetadata:
  [V18] Comment count <= 50 (M-16)         -> Error: "Exceeds max comment count" in parse_error
  [V19] Value length <= 10,000 chars (M-17)-> Error: "Value exceeds length limit" in parse_error
  [V20] Not an L2-REINJECT comment (case-insensitive exclusion)
                                            -> L2-REINJECT comments silently excluded

BlockquoteFrontmatter (existing):
  [V21] (No current limits -- RECOMMEND adding M-16 field count limit)
                                            -> On failure: N/A (no limit currently enforced)

ReinjectDirectives (existing + enhanced):
  [V22] File-origin trust check (M-22)     -> Error: "File not in TRUSTED_REINJECT_PATHS" (directives ignored)
  [V23] (RECOMMEND adding M-16 directive count limit)
                                            -> On failure: N/A (no limit currently enforced)
```

### BC-03: Parser to Domain Objects

```
Parsed Structures (Z3)                      Domain Objects (Z4)
+------------------+                        +------------------+
| dicts, strings,  |----[VALIDATION]------->| frozen dataclass |
| regex matches    |                        | instances with   |
|                  |                        | tuple containers |
+------------------+                        +------------------+

VALIDATION CHECKS:
  [V24] All values have control characters stripped (M-18)
                                            -> On failure: Characters silently removed
  [V25] All string values within max_value_length (M-17)
                                            -> On failure: parse_error set, empty result returned
  [V26] Frozen dataclass construction (immutability enforced by Python runtime)
                                            -> On failure: FrozenInstanceError on assignment attempt
  [V27] Tuple container construction (deep immutability)
                                            -> On failure: AttributeError on mutation attempt (no .append)
  [V28] Type annotations satisfied (enforced by construction discipline, NOT runtime)
                                            -> On failure: TypeError in downstream processing
```

### BC-04: Domain Objects to Schema Validation

```
Domain Objects (Z4)                         Validation Engine (Z5)
+------------------+                        +------------------+
| typed, immutable |----[VALIDATION]------->| schema rules     |
| domain objects   |                        | applied          |
+------------------+                        +------------------+

VALIDATION CHECKS:
  [V29] Required fields present             -> On failure: ValidationViolation(severity="error")
  [V30] Field values in allowed_values enum -> On failure: ValidationViolation(severity="error")
  [V31] Field values match value_pattern regex (ReDoS-safe per M-12)
                                            -> On failure: ValidationViolation(severity="error")
  [V32] Required sections present           -> On failure: ValidationViolation(severity="error")
  [V33] Nav table valid (H-23)              -> On failure: ValidationViolation(severity="error")
```

### BC-05: Domain Objects to Output

```
Domain Objects (Z4)                         Output (Z6)
+------------------+                        +------------------+
| validated,       |----[VALIDATION]------->| JSON stdout      |
| immutable        |                        | or file write    |
| domain objects   |                        +------------------+
+------------------+

VALIDATION CHECKS:
  [V34] JSON serialization (json.dumps)     -> On failure: TypeError (caught and reported)
  [V35] Error messages sanitized (M-19)     -> On failure: Raw paths/content in error output
  [V36] Write-back: atomic write via temp+rename (M-21)
                                            -> On failure: Partial write corruption prevented
  [V37] Write-back: path re-verified against repo root (M-08)
                                            -> On failure: Error "Path outside repository" (exit code 2)
```

---

## Parser-Specific Data Flow Diagrams

### YAML Frontmatter Data Flow

```
File Content (Z2)
    |
    |  [1] Scan for first --- delimiter pair (first-pair-only, M-24)
    |      Pattern: first line is "---", scan for second "---"
    |      Subsequent --- blocks are ignored
    v
+-------------------------------------------+
| Raw YAML Block                             |
| (text between first and second --- lines)  |
+-------------------------------------------+
    |
    |  [2] PRE-PARSE CHECKS:
    |      - SIZE: len(yaml_block) <= 32KB? (M-07)
    |        YES -> continue
    |        NO  -> return error result
    |      - ALIAS COUNT: count(*ref) <= max_alias_count? (M-20)
    |        YES -> continue
    |        NO  -> return error result
    |      - DUPLICATE KEYS: scan for repeated key names (M-23)
    |        Found -> add to parse_warnings
    v
+-------------------------------------------+
| yaml.safe_load(yaml_block)                 |
| CRITICAL: safe_load ONLY                   |
| Rejects: !!python/*, !!map, custom tags    |
| Allows: str, int, float, bool, list, dict  |
| NOTE: Expands anchors/aliases IN MEMORY    |
+-------------------------------------------+
    |
    |  [3] POST-PARSE CHECKS:
    |      - Result size <= 64KB? (M-20, closes temporal gap)
    |        YES -> continue
    |        NO  -> return error result ("expansion exceeded limit")
    |      - Key count <= 100? (M-16)
    |      - Nesting depth <= 5? (M-06)
    |
    |  [4] TYPE NORMALIZATION (DD-10):
    |      - bool -> "true"/"false"
    |      - int/float -> str()
    |      - None -> "null"
    |      - list -> "a, b, c"
    v
+-------------------------------------------+
| YamlFrontmatterResult (frozen dataclass)   |
|   .fields: tuple[YamlFrontmatterField, ...]|
|   .raw_yaml: str                           |
|   .start_line: int                         |
|   .end_line: int                           |
|   .parse_error: str | None                 |
|   .parse_warnings: tuple[str, ...]         |
+-------------------------------------------+
```

### XML Section Data Flow

```
File Content (Z2)
    |
    |  [1] Regex scan: <tag>...</tag> patterns
    |      Non-greedy (.*?) content matching (M-15)
    |      Tags on their own lines (^ $ anchors)
    v
+-------------------------------------------+
| Candidate matches                          |
+-------------------------------------------+
    |
    |  [2] WHITELIST CHECK: tag_name in ALLOWED_TAGS?
    |      YES -> continue
    |      NO  -> skip (silently ignored)
    |
    |  [3] NESTING CHECK: content contains <tag_name>?
    |      YES -> reject match, set parse_error
    |      NO  -> continue
    |
    |  [4] BOUNDS CHECK:
    |      - Section count <= 20? (M-16)
    |      - Content length <= 10,000 chars? (M-17)
    v
+-------------------------------------------+
| XmlSectionResult (frozen dataclass)        |
|   .sections: tuple[XmlSection, ...]        |
|     .tag_name: str                         |
|     .content: str                          |
|     .start_line: int                       |
|     .end_line: int                         |
|   .parse_error: str | None                 |
+-------------------------------------------+
```

### HTML Comment Metadata Data Flow

```
File Content (Z2)
    |
    |  [1] Regex scan: <!-- ... --> patterns
    |      Case-insensitive negative lookahead: NOT L2-REINJECT
    |      Non-greedy .*? up to first --> (M-13, NOT [^>]*)
    v
+-------------------------------------------+
| Candidate comment strings                  |
+-------------------------------------------+
    |
    |  [2] Parse key: value pairs (pipe-separated)
    |      Pattern: word : value (| word : value)*
    |
    |  [3] BOUNDS CHECK:
    |      - Comment count <= 50? (M-16)
    |      - Value length <= 10,000 chars? (M-17)
    |
    |  [4] SANITIZE:
    |      - Strip control characters (M-18)
    v
+-------------------------------------------+
| HtmlCommentResult (frozen dataclass)       |
|   .blocks: tuple[HtmlCommentBlock, ...]    |
|     .fields: tuple[HtmlCommentField, ...]  |
|     .raw_comment: str                      |
|     .line_number: int                      |
|   .parse_error: str | None                 |
+-------------------------------------------+
```

---

## Schema Validation Checkpoint Diagram

```
                    PARSE PHASE                    VALIDATE PHASE
                    ==========                     ==============

File Content --> BC-02 --> Parsers --> BC-03 --> Domain Objects --> BC-04 --> Schema
                  |                      |                            |
              [CHECKPOINT 1]         [CHECKPOINT 2]             [CHECKPOINT 3]
              Input bounds           Type safety                Schema rules
              Pre-parse:             + deep immutability        (FieldRule,
                M-05 (file size)     (frozen dataclass +         SectionRule,
                M-07 (YAML block)     tuple containers)          NavTable H-23)
                M-20 alias count     (M-18 sanitization)
              Post-parse:
                M-20 (result size)
                M-06 (depth)
                M-16 (count limits)
                M-17 (value length)

CHECKPOINT 1 (BC-02): Prevents oversized/malformed input from reaching parsers
  AND prevents expanded YAML output from exceeding memory bounds.
  - File size limit (1 MB)
  - YAML block size limit (32 KB) -- pre-parse
  - YAML result size limit (64 KB) -- post-parse (closes temporal gap)
  - YAML alias count limit (10) -- pre-parse
  - Field/section/comment count limits
  - Value length limits

CHECKPOINT 2 (BC-03): Ensures parsed data is well-typed and deeply immutable.
  - Frozen dataclass construction (prevents attribute reassignment)
  - Tuple containers (prevents container mutation: no append/extend)
  - Control character stripping
  - Type construction discipline (NOT runtime type enforcement)
  - EXCEPTION: FrontmatterField is NOT yet frozen (P0 migration required)

CHECKPOINT 3 (BC-04): Validates parsed data against structural schemas.
  - Required fields present
  - Field values in allowed set
  - Required sections present
  - Navigation table compliant (H-23)
```

---

## Write-Back Path Diagram

```
                        READ PATH (Safe)
                        ================

File (Z2) --> Parsers (Z3) --> Domain Objects (Z4) --> JSON stdout (Z6)
                                                        (no file write)


                        WRITE PATH (Requires Extra Validation)
                        ======================================

File (Z2) --> Parsers (Z3) --> Domain Objects (Z4)
                                     |
                                     | fm.set(key, value)
                                     v
                              Modified JerryDocument
                                     |
                                     | doc.render()
                                     v
                              Normalized markdown string
                                     |
                                     | [W1] PATH RE-VERIFY: resolved.is_relative_to(repo_root)?
                                     |      On failure: Error "Path outside repository" (exit code 2)
                                     | [W2] CONTENT CHECK: modified content is valid markdown?
                                     |      On failure: mdformat rendering error (exit code 2)
                                     | [W3] ATOMIC WRITE (M-21, TOCTOU mitigation):
                                     |      a. Write to temp file: path.with_suffix('.tmp')
                                     |      b. os.rename(temp_path, target_path)
                                     |      On failure: Partial write prevented; temp file cleaned up
                                     v
                              File (Z6) -- atomically replaced

WRITE PATH CONTROLS:
  [W1] Path containment re-verified before write (M-08)
       Mitigates TOCTOU by checking the resolved path immediately before rename.
  [W2] Content rendered through mdformat ensures valid markdown output.
  [W3] Atomic write via temp file + os.rename prevents partial writes and
       mitigates symlink substitution between read and write (T-WB-01).
  [W4] Only frontmatter VALUE changes are written; no structural modifications.
  [W5] Write-back currently only supports blockquote frontmatter (ast modify).
       YAML frontmatter write-back is NOT in scope for Phase 1.
```

---

## Threat Overlay

This section maps the highest-risk threats from the threat model to the boundary crossings where they are relevant.

```
+===========================================================================+
||  ZONE 1: CLI INPUT                                                      ||
||                                                                         ||
||  T-DT-04: Path traversal    -----------> BC-01 [M-08 blocks]           ||
||  T-DT-05: Symlink following -----------> BC-01 [M-10 blocks]           ||
||                                                                         ||
+=============================== BC-01 ====================================+
                                    |
+===========================================================================+
||  ZONE 2: FILE CONTENT                                                   ||
||                                                                         ||
||  T-DT-01: Type spoofing     -----------> DocumentTypeDetector [M-14]   ||
||  T-DT-02: Ambiguous detection ---------> DocumentTypeDetector [M-14]   ||
||                                                                         ||
+=============================== BC-02 ====================================+
                                    |
+===========================================================================+
||  ZONE 3: PARSER LAYER                                                   ||
||                                                                         ||
||  T-YF-07: yaml.load() code exec ------> YamlFrontmatter                ||
||                                          [M-01, M-04a, M-04b]          ||
||  T-YF-06: Billion laughs DoS ---------> YamlFrontmatter                ||
||                                          [M-07 pre + M-20 post]        ||
||  T-YF-05: Deep nesting DoS  ----------> YamlFrontmatter [M-06]        ||
||  T-YF-02: Anchor/alias injection -----> YamlFrontmatter [M-06, M-20]  ||
||  T-YF-09: Duplicate key injection ----> YamlFrontmatter [M-23 warn]   ||
||  T-XS-07: XXE via XML parser ---------> XmlSectionParser [M-11]        ||
||             (architecturally eliminated by regex-only DD-6)             ||
||  T-XS-02: Nested tag confusion -------> XmlSectionParser [M-15]        ||
||  T-XS-08: Tag-in-content consumption -> XmlSectionParser [DD-6 known]  ||
||  T-HC-03: --> in value ---------------> HtmlCommentMetadata [M-13]     ||
||  T-HC-04: L2-REINJECT injection ------> extract_reinject [M-22]        ||
||  T-HC-07: L2-REINJECT spoofing -------> extract_reinject [M-22]        ||
||  T-SV-03: ReDoS in value_pattern -----> Schema validation [M-12]       ||
||  T-SV-05: Registry poisoning ---------> SchemaRegistry [freeze()]      ||
||                                                                         ||
+=============================== BC-03 ====================================+
                                    |
+===========================================================================+
||  ZONE 4: DOMAIN OBJECTS                                                 ||
||                                                                         ||
||  Threat surface:                                                        ||
||    - NEW objects: frozen dataclass + tuple = deeply immutable            ||
||    - EXISTING FrontmatterField: NOT YET frozen (P0 migration)           ||
||    - Python frozen=True does NOT enforce type annotations at runtime    ||
||                                                                         ||
+=============================== BC-04 ====================================+
                                    |
+===========================================================================+
||  ZONE 5: SCHEMA VALIDATION (Trusted -- frozen registry, schema rules)   ||
+=============================== BC-05 ====================================+
                                    |
+===========================================================================+
||  ZONE 6: OUTPUT                                                         ||
||                                                                         ||
||  T-YF-04: Error message leak ----------> JSON output [M-19]            ||
||  T-DT-04: Write-back traversal -------> ast modify [M-08 re-verify]   ||
||  T-WB-01: TOCTOU race condition ------> ast modify [M-21 atomic write] ||
||                                                                         ||
+===========================================================================+
```

---

## Strategic Implications (L2)

### Defense-in-Depth Architecture

The trust boundary diagram reveals a **three-checkpoint defense-in-depth** architecture:

1. **Checkpoint 1 (BC-02):** Input bounds prevent resource exhaustion before and after parsing. Pre-parse checks (M-05, M-07, alias count) reject oversized or suspicious input before `yaml.safe_load()` is called. Post-parse checks (M-20 result size, M-06 depth) catch expansion attacks that pass pre-parse limits. This two-phase approach closes the temporal gap where `yaml.safe_load()` expands anchors in memory.

2. **Checkpoint 2 (BC-03):** Frozen dataclass construction with `tuple` containers enforces deep immutability at the language level. Once data crosses this boundary, neither attributes nor container contents can be modified. The Python runtime prevents both `result.field = x` (FrozenInstanceError) and `result.xml_sections.append(x)` (AttributeError -- tuples have no append). **Exception:** The existing `FrontmatterField` is not yet frozen; this P0 migration must complete before this checkpoint provides complete coverage.

3. **Checkpoint 3 (BC-04):** Schema validation provides semantic checking beyond structural parsing. A YAML block might parse correctly (Checkpoint 1) and produce valid types (Checkpoint 2) but contain semantically invalid values. Checkpoint 3 catches these. The `SchemaRegistry` is frozen after module-level registration, preventing runtime poisoning.

### Key Observation: Zone 3 is the Attack Surface

All identified threats with DREAD scores >= 28 target Zone 3 (Parser Layer). This is expected: parsers are the components that transform untrusted input into trusted objects. The security posture of the universal parser depends primarily on the quality of Zone 3 implementations and the effectiveness of Checkpoint 1 (BC-02) input bounds -- both pre-parse and post-parse.

### Governance Boundary

The L2-REINJECT extraction function operates within Zone 3 but has governance-level impact: injected directives control per-prompt rule enforcement across the entire Jerry Framework. The M-22 trusted path whitelist creates a governance boundary within Zone 3, distinguishing files that may contribute governance directives from files that may not. This is a trust-level distinction within a single zone, reflecting the elevated criticality of governance directive extraction.

### Recommendation: Prioritize Parser Testing

Given that Zone 3 concentrates the attack surface, Phase 3 (Testing) should prioritize:
1. Adversarial input fuzzing for each parser (including YAML billion-laughs with anchor expansion)
2. Integration tests for each mitigation (M-01 through M-24)
3. Property-based testing for parser correctness under malformed input
4. Performance testing under resource-limit boundary conditions
5. Golden-file regression testing for migration safety

---

## Disclaimer

This trust boundary analysis is based on the proposed architecture as described in `eng-architect-001-architecture-adr.md` and the existing codebase as of 2026-02-22. Trust zone assignments assume the parsers are implemented according to the constraints documented in the ADR. If implementation deviates from these constraints (e.g., using `xml.etree` instead of regex for XML section parsing), the trust boundaries and threat overlay must be reassessed.

**Zone 4 qualification:** The "Trusted" designation for Zone 4 is contingent on: (a) all new domain objects using `frozen=True` with `tuple` containers, and (b) the P0 migration of `FrontmatterField` to `frozen=True`. Until migration (b) completes, Zone 4 has a known gap for blockquote frontmatter fields.

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-22 | Initial trust boundary diagram |
| 2.2.0 | 2026-02-23 | **Iteration 4 targeted revisions for 0.95 threshold.** Added concrete mutability demonstration (`fm._fields.append(spoofed_field)` exploit and post-migration `AttributeError`) to Zone 4 IMMUTABILITY NOTE. |
| 2.1.0 | 2026-02-22 | **Iteration 3 targeted revisions:** Added precise characterization of `BlockquoteFrontmatter._fields` mutable list container in Zone 4 IMMUTABILITY NOTE; recommended `tuple` migration for `_fields` storage as Phase 2 task. |
| 2.0.0 | 2026-02-22 | **Iteration 2 revisions:** (P0) T-01: Updated Zone 4 to distinguish "existing (not yet frozen)" FrontmatterField from "new (frozen by design)" objects; added P0 migration note and IMMUTABILITY NOTE block; (P0) T-03: Changed all `list[...]` containers to `tuple[..., ...]` in Zone 4 diagram and all data flow diagrams; updated Checkpoint 2 to describe deep immutability via frozen+tuple; (P0) T-04: Added L2-REINJECT governance boundary in Zone 3 (M-22 trusted paths, case-insensitive exclusion); added T-HC-04 and T-HC-07 to threat overlay; added governance boundary discussion in L2 implications; (P0) T-02: Updated YAML data flow to show M-20 post-parse result size verification, alias count pre-check; updated Checkpoint 1 description to include post-parse phase; (P1) T-08: Updated write-back path with M-21 atomic write (temp file + os.rename); added T-WB-01 to threat overlay; added "On Failure" actions to all W1-W5 controls; (P1) T-05: Updated Zone 5 SchemaRegistry to show freeze() and MappingProxyType; added T-SV-05 to threat overlay; (P2) SM-003-B1: Added "On Failure" column/description to all V1-V37 validation checks; (P2) FM-007-B1: Updated HTML comment data flow to specify non-greedy .*? instead of [^>]*; (P2) Zone count: Corrected to "six trust zones" throughout (was textually inconsistent); Added parse_errors aggregation to Zone 4; Updated YAML data flow with duplicate key detection, first-pair-only rule, type normalization; Added XmlSectionResult and HtmlCommentResult wrapper types to data flows; Added Runtime type annotation note to Zone 4. |

---

<!-- VERSION: 2.2.0 | DATE: 2026-02-23 | AGENT: eng-architect | ENGAGEMENT: ENG-0001 -->
