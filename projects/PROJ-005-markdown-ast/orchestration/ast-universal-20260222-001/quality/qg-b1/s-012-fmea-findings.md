# FMEA Report: Universal Markdown Parser Phase 1 Architecture Deliverables

**Strategy:** S-012 FMEA (Failure Mode and Effects Analysis)
**Deliverables:** eng-architect-001-threat-model.md, eng-architect-001-architecture-adr.md, eng-architect-001-trust-boundaries.md, red-lead-001-scope.md
**Criticality:** C4
**Date:** 2026-02-22
**Reviewer:** adv-executor (S-012)
**H-16 Compliance:** S-012 executed as part of QG-B1 tournament sequence
**Elements Analyzed:** 12 | **Failure Modes Identified:** 36 | **Total RPN:** 5,720

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall FMEA assessment |
| [Element Inventory](#element-inventory) | Decomposition of deliverables into analyzable elements |
| [Findings Table](#findings-table) | All failure modes with RPN scores |
| [Finding Details](#finding-details) | Expanded descriptions for Critical and Major findings |
| [Recommendations](#recommendations) | Prioritized corrective actions |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 quality dimensions |

---

## Summary

Twelve elements were analyzed across the four Phase 1 architecture deliverables covering the universal markdown parser design. Thirty-six failure modes were identified using the five-lens methodology (Missing, Incorrect, Ambiguous, Inconsistent, Insufficient). The highest-RPN finding is FM-001-B1 (RPN 336): the architecture ADR lacks a concrete YAML anchor/alias expansion limit, relying on post-parse depth validation (M-06) which does not address exponential expansion at a given depth. Seven findings are classified Critical (RPN >= 200), fourteen are Major (RPN 80-199), and fifteen are Minor (RPN < 80). The overall assessment is **ACCEPT with targeted corrections** -- the architecture is fundamentally sound, with well-reasoned security constraints (yaml.safe_load enforcement, no XML parser, frozen dataclasses, input bounds), but has specific gaps in DoS mitigation specification, cross-deliverable consistency, edge case handling documentation, and governance-critical component protection that require corrective action before implementation begins.

---

## Element Inventory

| ID | Element | Source Deliverable | Description |
|----|---------|--------------------|-------------|
| E-01 | YamlFrontmatter Parser Design | ADR (DD1), Threat Model (STRIDE YF) | YAML frontmatter extraction using yaml.safe_load with InputBounds |
| E-02 | XmlSectionParser Design | ADR (DD6), Threat Model (STRIDE XS) | Regex-based XML section extraction with tag whitelist |
| E-03 | HtmlCommentMetadata Design | ADR (DD7), Threat Model (STRIDE HC) | HTML comment metadata extraction with L2-REINJECT exclusion |
| E-04 | DocumentTypeDetector Design | ADR (DD2), Threat Model (STRIDE DT) | Path-first, structure-fallback document type detection |
| E-05 | UniversalDocument Facade | ADR (DD3), Trust Boundaries | Unified parsing facade with type-specific delegation |
| E-06 | SchemaRegistry / Extended Schemas | ADR (DD4), Threat Model (STRIDE SV) | Dynamic schema registration with collision detection |
| E-07 | InputBounds Configuration | ADR (DD8), Trust Boundaries (Checkpoints) | Centralized resource limit configuration |
| E-08 | Trust Boundary Architecture | Trust Boundaries (Primary Diagram) | Six-zone trust model with five boundary crossings |
| E-09 | DREAD Scoring and Risk Prioritization | Threat Model (DREAD, PASTA) | Risk quantification and prioritized mitigation |
| E-10 | CLI Extension Strategy | ADR (DD5), Red Team Scope (CLI Testing) | New subcommands and --type flag |
| E-11 | Red Team Scope and RoE | Red Team Scope (Full Document) | Engagement authorization, targets, constraints |
| E-12 | Cross-Deliverable Consistency | All Four Deliverables | Alignment between threat model, ADR, trust boundaries, and red team scope |

---

## Findings Table

| ID | Element | Failure Mode | S | O | D | RPN | Severity | Corrective Action | Affected Dimension |
|----|---------|-------------|---|---|---|-----|----------|-------------------|--------------------|
| FM-001-B1 | E-01 | YAML anchor/alias expansion limit not concretely specified -- M-06 validates depth but not expansion factor; billion laughs at depth 2 bypasses depth limit | 8 | 7 | 6 | 336 | Critical | Specify maximum post-parse result size (e.g., 64KB serialized) AND maximum alias expansion count independently of nesting depth | Completeness |
| FM-002-B1 | E-01 | No specification of yaml.safe_load exception handling -- ConstructorError, ScannerError, ParserError may leak internal state if not caught and sanitized | 7 | 7 | 6 | 294 | Critical | Specify complete exception type list and sanitized error message format in ADR DD1 and threat model | Methodological Rigor |
| FM-003-B1 | E-01 | YAML duplicate key behavior unspecified -- PyYAML silently uses last value for duplicate keys; no mention of detection or warning in ADR | 6 | 6 | 7 | 252 | Critical | Specify duplicate key detection and behavior (reject or warn with last-wins) in YamlFrontmatter design | Completeness |
| FM-004-B1 | E-01 | YAML multi-document handling unspecified -- files with multiple --- delimited blocks may cause yaml.safe_load to process only first block or raise errors; ADR silent on this | 6 | 6 | 7 | 252 | Critical | Specify that only the first --- pair is extracted as frontmatter; additional --- delimiters are treated as content | Completeness |
| FM-005-B1 | E-02 | XmlSectionParser regex DOTALL with non-greedy may fail on legitimate content containing tag-like strings -- a methodology section discussing `<identity>` as an example would be partially consumed | 7 | 5 | 6 | 210 | Critical | Specify escaping convention for literal tag references in content, or document limitation that content must not contain opening tags matching ALLOWED_TAGS | Internal Consistency |
| FM-006-B1 | E-12 | Red team scope references "XML parser (TBD)" for XmlSectionParser despite ADR DD6 mandating regex-only -- inconsistency between deliverables | 7 | 6 | 5 | 210 | Critical | Update red team scope to reflect ADR decision: XmlSectionParser uses regex, not XML parser; remove XXE test cases as they become N/A or reframe as architecture validation tests | Internal Consistency |
| FM-007-B1 | E-03 | HtmlCommentMetadata regex pattern in ADR DD7 uses `[^>]*?` which does not match the stated "first --> terminates" behavior -- the negated character class `[^>]` prevents matching of `>` inside values even where `-->` is not present | 6 | 6 | 6 | 216 | Critical | Revise regex to use a non-greedy match up to `-->` rather than character-class exclusion of `>`; verify regex handles values containing isolated `>` characters | Methodological Rigor |
| FM-008-B1 | E-04 | DocumentTypeDetector PATH_PATTERNS uses glob-style patterns but no glob matching library is specified -- fnmatch, pathlib.match, or custom matching could produce different results | 6 | 5 | 6 | 180 | Major | Specify which glob matching implementation is used and document its semantic (fnmatch, PurePath.match, or regex conversion) | Actionability |
| FM-009-B1 | E-04 | Structure-fallback detection priority/ordering unspecified -- file with both --- delimiters AND `<identity>` tags matches multiple structural cues with no documented precedence | 6 | 6 | 5 | 180 | Major | Specify structural cue evaluation order and define which cue wins when multiple match; document as part of DD2 detection algorithm | Methodological Rigor |
| FM-010-B1 | E-05 | UniversalParseResult uses `list[XmlSection]` and `list[HtmlCommentBlock]` (mutable) inside a frozen dataclass -- list contents can be mutated despite frozen container, violating immutability guarantee | 7 | 5 | 5 | 175 | Major | Use `tuple[XmlSection, ...]` and `tuple[HtmlCommentBlock, ...]` for all collection attributes in UniversalParseResult, matching the tuple pattern used in YamlFrontmatterResult | Internal Consistency |
| FM-011-B1 | E-06 | SchemaRegistry uses `dict[str, EntitySchema]` as internal storage -- mutable dict in a class that should provide immutable-after-registration semantics; no freeze mechanism after initialization | 6 | 5 | 6 | 180 | Major | Add a `freeze()` method or use module-level registry construction pattern that prevents post-initialization registration; alternatively document that register() is only called during module load | Methodological Rigor |
| FM-012-B1 | E-07 | InputBounds.DEFAULT uses ClassVar assignment after class definition (`InputBounds.DEFAULT = InputBounds()`) which is a mutable class attribute -- can be reassigned at runtime | 5 | 4 | 7 | 140 | Major | Use `ClassVar` with a property or module-level constant pattern; alternatively, make DEFAULT a module-level constant outside the class | Internal Consistency |
| FM-013-B1 | E-08 | Trust boundary diagram marks Zone 4 as "no threats at this boundary" but XmlSection and HtmlCommentBlock lists are mutable (FM-010-B1) -- threat assertion is premature | 6 | 5 | 5 | 150 | Major | Update trust boundary document to acknowledge mutable collection risk at BC-03 boundary until FM-010-B1 is resolved; or resolve FM-010-B1 first and then the assertion holds | Internal Consistency |
| FM-014-B1 | E-09 | DREAD scores for T-YF-06 (billion laughs) give Exploitability 7, but yaml.safe_load faithfully processes anchors/aliases with no built-in limit -- Exploitability should arguably be higher (8-9) since crafting the payload is trivial | 5 | 5 | 6 | 150 | Major | Re-evaluate T-YF-06 DREAD Exploitability rating; consider that a billion-laughs YAML can be generated in a single line and requires zero specialized knowledge | Evidence Quality |
| FM-015-B1 | E-08 | Write-back path diagram shows TOCTOU concern (W1) but provides no mitigation beyond path re-verification -- an attacker could replace the file with a symlink between read and write | 6 | 4 | 6 | 144 | Major | Specify atomic write pattern (write to tempfile then rename) or file descriptor-based locking to mitigate TOCTOU; add as mitigation M-20 in threat model | Completeness |
| FM-016-B1 | E-11 | Red team scope lists CWE-79 (XSS) for HtmlCommentMetadata but the parser output is JSON to stdout -- XSS is not applicable to a CLI tool; misclassified CWE | 5 | 5 | 5 | 125 | Major | Replace CWE-79 with CWE-94 (Code Injection) or CWE-20 (Improper Input Validation) for HtmlCommentMetadata; XSS requires a browser rendering context | Evidence Quality |
| FM-017-B1 | E-10 | CLI `ast detect` subcommand returns "JSON with type and confidence" but DocumentTypeDetector returns a deterministic DocumentType enum with no confidence score -- output format mismatch | 5 | 5 | 5 | 125 | Major | Either add a confidence field to DocumentTypeDetector (path match = 1.0, structure match = 0.8, fallback = 0.5) or update CLI spec to return type only without confidence | Internal Consistency |
| FM-018-B1 | E-12 | Threat model mitigation M-12 recommends "possessive quantifiers or atomic groups" for ReDoS-safe regex but Python re module does not support possessive quantifiers or atomic groups | 6 | 4 | 5 | 120 | Major | Replace M-12 guidance with Python-specific alternatives: use `re2` via `google-re2` package, or manually restructure regex to avoid catastrophic backtracking; alternatively use anchored patterns with character classes | Actionability |
| FM-019-B1 | E-02 | XmlSectionParser ALLOWED_TAGS is a frozen set constant -- adding new section types (future agent definition evolution) requires code modification, violating Open-Closed Principle | 4 | 5 | 6 | 120 | Major | Allow ALLOWED_TAGS to be extended via constructor parameter with a frozen default; document extension mechanism in ADR DD6 | Actionability |
| FM-020-B1 | E-03 | HtmlCommentMetadata negative lookahead `(?!L2-REINJECT:)` depends on exact prefix -- a whitespace-variant `<!--  L2-REINJECT:` (extra space) would not be excluded by the negative lookahead but also would not be matched by reinject.py's pattern | 5 | 4 | 6 | 120 | Major | Specify whitespace normalization before L2-REINJECT pattern matching or use a more robust exclusion strategy (e.g., check content for "L2-REINJECT" substring after extraction) | Completeness |
| FM-021-B1 | E-09 | Attack tree 1 assessment states yaml.safe_load "rejects !!python tags" but does not mention !!yaml tags or custom tag handling -- yaml.safe_load restricts to SafeLoader but documentation should be explicit about what IS allowed | 5 | 4 | 6 | 120 | Major | Add explicit enumeration of what yaml.safe_load accepts (str, int, float, bool, list, dict, None, date, timestamp) and what it rejects (all !!python, !!yaml, custom tags) | Evidence Quality |
| FM-022-B1 | E-11 | Red team scope authorizes red-vuln to use "Write" and "Edit" tools but scope says "MUST NOT modify production source code" -- ambiguity about what constitutes "production source code" vs test/evidence files | 5 | 5 | 5 | 125 | Major | Define explicit boundary: production source = `src/`, `.context/`, `skills/`; evidence directory = `projects/PROJ-005-markdown-ast/.../red/evidence/`; all writes must be within evidence directory | Actionability |
| FM-023-B1 | E-05 | Parser invocation matrix marks STRATEGY_TEMPLATE as BlockquoteFrontmatter but strategy templates use mixed formats (blockquote metadata header + XML-like structure) -- templates may not be fully parsed | 4 | 5 | 5 | 100 | Major | Audit strategy template format to determine if XML sections or HTML comments are also present; update parser invocation matrix if additional parsers are needed | Completeness |
| FM-024-B1 | E-07 | InputBounds max_nesting_depth = 5 may be insufficient for legitimate deeply-nested YAML structures in agent definitions (e.g., `capabilities.allowed_tools` nested under `capabilities` nested under root) | 4 | 5 | 5 | 100 | Major | Validate max_nesting_depth = 5 against actual agent definition YAML depth requirements; document the deepest legitimate structure and set limit to max(legitimate_depth + 1, 5) | Evidence Quality |
| FM-025-B1 | E-06 | EntitySchema validation uses `re.fullmatch()` for value_pattern but ADR does not specify whether patterns are compiled once (at schema registration) or per-validation -- per-validation compilation is a performance concern | 4 | 5 | 4 | 80 | Major | Specify that value_pattern regex patterns are pre-compiled at schema registration time using `re.compile()`; stored as compiled patterns rather than raw strings | Actionability |
| FM-026-B1 | E-08 | Trust boundary document labels Zone 3 as "semi-trusted" but lists seven parser components in that zone -- the "semi-trusted" label may give false confidence; parsers are the primary attack surface | 4 | 4 | 5 | 80 | Minor |  Relabel Zone 3 as "transformation boundary" or "untrusted-to-trusted transition" to better convey that this is where the security-critical transformation occurs | Evidence Quality |
| FM-027-B1 | E-10 | CLI `--format yaml` flag on `ast frontmatter` implies format detection override but DocumentTypeDetector handles type detection -- two different mechanisms (--format for frontmatter format vs --type for document type) could confuse users | 4 | 4 | 5 | 80 | Minor | Consolidate to single `--type` flag that implies frontmatter format, or document the distinction clearly in CLI help text | Actionability |
| FM-028-B1 | E-01 | YamlFrontmatterField uses `value_type: str` field with string values "str", "int", etc. -- stringly-typed enum; should use Python enum for type safety | 3 | 4 | 5 | 60 | Minor | Replace `value_type: str` with `value_type: YamlValueType` enum containing STR, INT, FLOAT, BOOL, LIST, NULL members | Methodological Rigor |
| FM-029-B1 | E-04 | DocumentTypeDetector returns UNKNOWN for files outside known path patterns with no structural cues -- silent fallback to minimal parsing may hide misplaced files | 3 | 5 | 4 | 60 | Minor | Add an info-level log or warning when UNKNOWN is returned; include file path and which structural cues were checked | Traceability |
| FM-030-B1 | E-09 | Threat model NIST CSF mapping assigns M-01 (banned API lint rule) to PR.DS-01 (data-at-rest integrity) -- a lint rule protects code quality not data integrity; better mapped to PR.DS-06 or PR.IP-03 | 3 | 3 | 6 | 54 | Minor | Remap M-01 to NIST CSF PR.IP-03 (Configuration management) or PR.DS-06 (Integrity checking mechanisms) | Traceability |
| FM-031-B1 | E-11 | Red team scope time window of 30 days (2026-02-22 to 2026-03-22) may be insufficient for Phase 2-4 execution given the engagement depends on new component implementation | 3 | 4 | 4 | 48 | Minor | Add note that time window begins when implementation is available for testing; scope v1.1 should update dates post-implementation | Actionability |
| FM-032-B1 | E-12 | Threat model references "line 144-163" and "line 279" in existing source code -- line references are brittle and will break after any edit to referenced files | 3 | 6 | 3 | 54 | Minor | Replace line references with function/method names (e.g., `_read_file()` in `ast_commands.py`, `re.fullmatch()` in `EntitySchema.validate()`) or use stable anchors | Traceability |
| FM-033-B1 | E-05 | UniversalDocument.parse() signature accepts `file_path: str | None` but Path objects are used throughout the codebase -- inconsistent type (str vs Path) | 3 | 4 | 4 | 48 | Minor | Use `file_path: str | Path | None` or `file_path: Path | None` to match codebase conventions | Internal Consistency |
| FM-034-B1 | E-07 | InputBounds max_reinject_count = 50 is specified but no threat model mitigation ID is assigned to L2-REINJECT count limiting -- gap in mitigation traceability | 3 | 3 | 5 | 45 | Minor | Assign a mitigation ID (e.g., M-16e) specifically for L2-REINJECT count limiting and add to threat model mitigation table | Traceability |
| FM-035-B1 | E-06 | Schema definitions for new file types (10 schemas) are listed in ADR DD4 but field rules are only sketched at high level -- implementation will require significant interpretation | 3 | 5 | 3 | 45 | Minor | Expand schema definitions to include concrete FieldRule and SectionRule specifications for at least the three highest-priority types (agent_definition, skill_definition, adr) | Completeness |
| FM-036-B1 | E-08 | Trust boundary checkpoint 2 (BC-03) lists "Type annotation enforcement" by dataclass as a validation check -- Python dataclasses do not enforce type annotations at runtime without a validation library | 4 | 3 | 4 | 48 | Minor | Clarify that type enforcement is structural (frozen dataclass prevents mutation) not runtime type-checking; or specify use of a runtime type checker (e.g., beartype, pydantic) | Evidence Quality |

---

## Finding Details

### FM-001-B1: YAML Anchor/Alias Expansion Limit Gap (Critical, RPN 336)

**Element:** E-01 (YamlFrontmatter Parser Design)

**Failure Mode:** The architecture specifies post-parse depth validation (M-06: max nesting depth <= 5) and pre-parse size validation (M-07: max YAML block <= 32KB) as defenses against YAML billion-laughs attacks. However, a billion-laughs payload at nesting depth 2 can expand to gigabytes of memory from a 32KB input. The YAML `a: &x [*x, *x, *x, *x, *x, *x, *x, *x, *x, *x]` pattern produces 10^N elements at depth N, so depth 2 with 10 aliases per level produces 100 elements -- manageable. But `a: &x [*x, *x, *x, *x, *x, *x, *x, *x, *x, *x, *x, *x, *x, *x, *x, *x, *x, *x, *x, *x]` (20 aliases) at depth 2 produces 400 elements, each potentially containing nested structures. The gap is that M-06 checks depth but not total expansion factor. M-07 limits the input bytes but not the output memory.

**Effect:** yaml.safe_load faithfully expands all anchors and aliases. A carefully crafted 32KB YAML input could expand to hundreds of megabytes in memory, causing the CLI process to consume excessive memory and potentially crash the developer's machine.

**S/O/D Rationale:** Severity 8 (DoS of developer machine is significant). Occurrence 7 (billion-laughs payloads are well-known and trivial to craft; the gap in M-06 is real). Detection 6 (the gap is subtle -- depth validation gives false confidence that expansion is bounded).

**Corrective Action:** Add a post-parse result size validation step: after yaml.safe_load returns, serialize the result with `json.dumps()` and check that the serialized size is <= InputBounds.max_yaml_result_bytes (suggest 64KB default). This catches expansion attacks regardless of nesting depth. Add `max_yaml_result_bytes: int = 65_536` to InputBounds class.

**Acceptance Criteria:** ADR DD1 specifies post-parse result size limit. InputBounds class includes max_yaml_result_bytes field. Threat model M-06 is updated to distinguish depth limit from expansion limit.

**Post-Correction RPN Estimate:** S=8, O=3, D=3 = 72 (Major, from 336)

---

### FM-002-B1: yaml.safe_load Exception Handling Unspecified (Critical, RPN 294)

**Element:** E-01 (YamlFrontmatter Parser Design)

**Failure Mode:** The ADR specifies that parsing errors produce a result with `parse_error` set rather than raising exceptions. However, neither the ADR nor the threat model enumerate the specific exception types that yaml.safe_load can raise (yaml.YAMLError, yaml.scanner.ScannerError, yaml.parser.ParserError, yaml.constructor.ConstructorError) or specify how the error message should be sanitized. PyYAML error messages include the problematic line content and context markers, which could leak partial file content through CLI JSON output.

**Effect:** Unsanitized YAML parsing errors could leak internal file content fragments through the CLI JSON error output. Without specified exception handling, implementers may catch only `yaml.YAMLError` and miss `TypeError` from unexpected input types, or may not sanitize the error message per M-19.

**S/O/D Rationale:** Severity 7 (information disclosure through error messages). Occurrence 7 (YAML parse errors are common with malformed input). Detection 6 (implementers may not think to enumerate all exception types).

**Corrective Action:** Add an exception handling specification to ADR DD1: catch `yaml.YAMLError` (base class for all PyYAML errors) and `TypeError`; extract error type name and line number only; do not include the problematic content in the error message; set `parse_error` to `f"{type(e).__name__} at line {getattr(e, 'problem_mark', {}).line}"`.

**Acceptance Criteria:** ADR DD1 includes exception handling specification with sanitized error message format.

**Post-Correction RPN Estimate:** S=7, O=3, D=3 = 63 (Minor, from 294)

---

### FM-003-B1: YAML Duplicate Key Behavior Unspecified (Critical, RPN 252)

**Element:** E-01 (YamlFrontmatter Parser Design)

**Failure Mode:** PyYAML's yaml.safe_load silently uses the last value when duplicate keys are present in YAML. The ADR does not specify whether the YamlFrontmatter parser should detect duplicate keys, warn about them, or reject the input. The red team scope identifies this as a test case but the architecture does not define the expected behavior.

**Effect:** An agent definition with duplicate keys (e.g., two `model:` fields) would silently use the last value. This could be exploited to inject unexpected values: a reviewer reads the first `model: sonnet` and approves, while the parser uses the second `model: opus` appended at the bottom.

**S/O/D Rationale:** Severity 6 (silent value override is a data integrity concern). Occurrence 6 (duplicate keys in YAML are easy to introduce accidentally or maliciously). Detection 7 (the behavior is silent -- no warning or error is produced).

**Corrective Action:** Specify in ADR DD1 that YamlFrontmatter MUST detect duplicate keys by comparing the raw YAML key list against the parsed dict key count (if `len(raw_keys) != len(parsed_dict.keys())`, duplicates exist). When duplicates are detected, include a warning in the parse result (new field `duplicate_key_warnings: tuple[str, ...]`).

**Acceptance Criteria:** ADR DD1 specifies duplicate key detection mechanism and warning behavior.

**Post-Correction RPN Estimate:** S=6, O=6, D=3 = 108 (Major, from 252)

---

### FM-004-B1: YAML Multi-Document Handling Unspecified (Critical, RPN 252)

**Element:** E-01 (YamlFrontmatter Parser Design)

**Failure Mode:** YAML files may contain multiple document separators (`---`). The frontmatter convention uses `---` as opening and closing delimiters for the YAML block. A file with three `---` markers creates ambiguity about which block constitutes the frontmatter. PyYAML's `yaml.safe_load()` processes only the first document in a stream; `yaml.safe_load_all()` processes all documents. The ADR does not specify how extra `---` delimiters should be handled.

**Effect:** Files with `---` in body content (e.g., horizontal rules in markdown, which are rendered from `---`) could be misinterpreted as frontmatter delimiters, causing incorrect content extraction.

**S/O/D Rationale:** Severity 6 (incorrect frontmatter extraction produces wrong validation results). Occurrence 6 (markdown horizontal rules using `---` are common). Detection 7 (the interaction between markdown `---` rules and YAML delimiters is a subtle edge case).

**Corrective Action:** Specify in ADR DD1: (1) only the FIRST `---` pair in the file (lines 0-N where line 0 is `---` and line N is the next `---`) constitutes frontmatter; (2) `---` lines after the closing delimiter are treated as markdown content; (3) the extraction regex must anchor the opening `---` to line 0 or line 1 of the file.

**Acceptance Criteria:** ADR DD1 specifies multi-document handling rules with examples.

**Post-Correction RPN Estimate:** S=6, O=3, D=3 = 54 (Minor, from 252)

---

### FM-005-B1: XmlSectionParser Content Containing Tag-Like Strings (Critical, RPN 210)

**Element:** E-02 (XmlSectionParser Design)

**Failure Mode:** The XmlSectionParser uses regex with non-greedy matching to extract content between `<tag>` and `</tag>`. However, if the content of a section discusses XML tags as examples (e.g., a methodology section that explains the `<identity>` tag format), the regex could match the example tag instead of the actual closing tag, causing content truncation or section misattribution.

**Effect:** Agent definition files that document their own structure (meta-documentation) would be incorrectly parsed. The parser would extract truncated content or assign content to the wrong section.

**S/O/D Rationale:** Severity 7 (section misattribution corrupts the parsed document structure). Occurrence 5 (agent definitions discussing their own format is plausible but not the common case). Detection 6 (the failure would produce silently wrong results -- no error, just wrong content).

**Corrective Action:** Specify in ADR DD6 that content between section tags must not contain standalone opening tags matching ALLOWED_TAGS on their own line. If literal tag references are needed in content, they should be escaped (e.g., `\<identity\>` or wrapped in code blocks). Alternatively, specify that the regex requires the tag to be the ONLY content on its line (no leading whitespace indentation that would indicate it is within a code block).

**Acceptance Criteria:** ADR DD6 documents the limitation and specifies either an escaping convention or a robust heuristic for distinguishing section tags from content tags.

**Post-Correction RPN Estimate:** S=7, O=3, D=4 = 84 (Major, from 210)

---

### FM-006-B1: Cross-Deliverable Inconsistency -- XML Parser Decision (Critical, RPN 210)

**Element:** E-12 (Cross-Deliverable Consistency)

**Failure Mode:** The ADR (DD6) explicitly mandates regex-only parsing for XmlSectionParser and rejects full XML parsers to prevent XXE. The threat model documents T-XS-07 (XXE via XML parser) and mitigates it with M-11 (no full XML parser). However, the red team scope document's XmlSectionParser section (page 577-587) includes test cases for "Entity expansion (XXE)" with DOCTYPE declarations and "Billion laughs" with entity expansion -- attacks that are only possible if a full XML parser is used. The scope document also labels XmlSectionParser with "XML parser (TBD)" in the input vectors table, contradicting the ADR's decided architecture.

**Effect:** The red team will allocate testing effort to attack vectors that are architecturally impossible (XXE, entity expansion) while potentially under-testing the actual attack surface (regex-based parsing vulnerabilities like ReDoS on the section pattern, greedy vs non-greedy mismatches, malformed tag handling).

**S/O/D Rationale:** Severity 7 (misdirected security testing wastes effort and may miss real vulnerabilities). Occurrence 6 (the inconsistency is present in the current deliverables). Detection 5 (requires reading multiple deliverables to notice the contradiction).

**Corrective Action:** Update red team scope to: (1) replace "XML parser (TBD)" with "Regex-based extraction (per ADR DD6)"; (2) reclassify XXE and entity expansion test cases as architecture validation tests (verify regex is used, not XML parser) rather than exploitation tests; (3) add regex-specific test cases (ReDoS on section pattern, non-greedy matching edge cases, Unicode tag names).

**Acceptance Criteria:** Red team scope XmlSectionParser test cases align with ADR DD6 regex-only architecture decision.

**Post-Correction RPN Estimate:** S=7, O=2, D=3 = 42 (Minor, from 210)

---

### FM-007-B1: HtmlCommentMetadata Regex Incorrectly Excludes `>` in Values (Critical, RPN 216)

**Element:** E-03 (HtmlCommentMetadata Design)

**Failure Mode:** The ADR DD7 regex pattern includes `[^>]*?` which is a non-greedy match of characters that are NOT `>`. This means any HTML comment value containing a `>` character would cause the regex to fail to match or match incorrectly. For example, `<!-- PS-ID: ADR-PROJ005-003 | ENTRY: 2026-02-22 | NOTE: score > 0.92 -->` would fail because `> 0.92` contains a `>` character. The stated behavior ("first `-->` terminates") is correct, but the regex implementation does not achieve this behavior because `[^>]` excludes all `>` characters, not just `-->` sequences.

**Effect:** Legitimate HTML comment metadata containing `>` characters in values (mathematical expressions, markdown fragments, comparison operators) would not be extracted, causing silent data loss.

**S/O/D Rationale:** Severity 6 (silent data loss in metadata extraction). Occurrence 6 (the `>` character is common in technical metadata values). Detection 6 (the regex looks plausible at first glance but the `[^>]` exclusion is incorrect for the stated behavior).

**Corrective Action:** Replace `[^>]*?` with a pattern that matches up to `-->` specifically: use `(?:(?!-->).)*` (negative lookahead for `-->` at each position) or use a two-step approach (find `<!--`, then scan forward for first `-->`, extract body between them).

**Acceptance Criteria:** ADR DD7 regex correctly handles values containing isolated `>` characters while still terminating at `-->`.

**Post-Correction RPN Estimate:** S=6, O=2, D=3 = 36 (Minor, from 216)

---

## Recommendations

### Critical Findings (RPN >= 200) -- Mandatory Corrective Actions

| Priority | ID | Corrective Action | Est. RPN Reduction |
|----------|----|--------------------|-------------------|
| 1 | FM-001-B1 | Add post-parse YAML result size limit (max_yaml_result_bytes) to InputBounds; distinct from depth limit | 336 -> 72 |
| 2 | FM-007-B1 | Fix HtmlCommentMetadata regex to use `(?:(?!-->).)*` instead of `[^>]*?` | 216 -> 36 |
| 3 | FM-002-B1 | Specify yaml.safe_load exception handling with sanitized error messages | 294 -> 63 |
| 4 | FM-003-B1 | Specify YAML duplicate key detection with warning mechanism | 252 -> 108 |
| 5 | FM-004-B1 | Specify multi-document YAML handling (first --- pair only) | 252 -> 54 |
| 6 | FM-005-B1 | Specify escaping convention or limitation for tag-like strings in XML section content | 210 -> 84 |
| 7 | FM-006-B1 | Align red team scope with ADR DD6 regex-only decision for XmlSectionParser | 210 -> 42 |

### Major Findings (RPN 80-199) -- Recommended Corrective Actions

| Priority | ID | Corrective Action | Est. RPN Reduction |
|----------|----|--------------------|-------------------|
| 8 | FM-008-B1 | Specify glob matching implementation for DocumentTypeDetector | 180 -> 60 |
| 9 | FM-009-B1 | Specify structural cue evaluation order for multi-cue files | 180 -> 60 |
| 10 | FM-010-B1 | Replace mutable `list` with immutable `tuple` in UniversalParseResult | 175 -> 35 |
| 11 | FM-011-B1 | Add SchemaRegistry freeze mechanism or document initialization-only registration | 180 -> 60 |
| 12 | FM-013-B1 | Update trust boundary Zone 4 assertion to acknowledge mutable collections | 150 -> 50 |
| 13 | FM-014-B1 | Re-evaluate T-YF-06 DREAD Exploitability rating | 150 -> 120 |
| 14 | FM-015-B1 | Specify TOCTOU mitigation for write-back path (atomic write or fd locking) | 144 -> 48 |
| 15 | FM-018-B1 | Replace M-12 possessive quantifier guidance with Python-compatible alternatives | 120 -> 40 |
| 16 | FM-012-B1 | Fix InputBounds.DEFAULT mutability concern | 140 -> 45 |
| 17 | FM-016-B1 | Reclassify CWE-79 to CWE-94 or CWE-20 for HtmlCommentMetadata | 125 -> 40 |
| 18 | FM-017-B1 | Resolve ast detect confidence score inconsistency | 125 -> 40 |
| 19 | FM-019-B1 | Allow XmlSectionParser ALLOWED_TAGS extension via constructor parameter | 120 -> 40 |
| 20 | FM-020-B1 | Improve L2-REINJECT exclusion robustness for whitespace variants | 120 -> 40 |
| 21 | FM-021-B1 | Add explicit enumeration of yaml.safe_load accepted/rejected types | 120 -> 40 |
| 22 | FM-022-B1 | Define explicit production vs evidence directory boundary in red team scope | 125 -> 40 |
| 23 | FM-023-B1 | Audit strategy template format and update parser invocation matrix | 100 -> 35 |
| 24 | FM-024-B1 | Validate max_nesting_depth against actual agent definition YAML depth | 100 -> 35 |
| 25 | FM-025-B1 | Specify pre-compiled regex patterns for value_pattern in schema | 80 -> 25 |

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative (-0.06) | FM-001-B1 (expansion limit gap), FM-003-B1 (duplicate keys), FM-004-B1 (multi-document), FM-015-B1 (TOCTOU), FM-020-B1 (L2-REINJECT exclusion), FM-023-B1 (strategy template parsing), FM-035-B1 (schema details). Seven findings identify missing specifications that would leave implementation ambiguous. The architecture covers the major components thoroughly but has gaps in edge case handling and secondary defense mechanisms. |
| Internal Consistency | 0.20 | Negative (-0.07) | FM-005-B1 (tag-in-content), FM-006-B1 (cross-deliverable XML parser conflict), FM-010-B1 (mutable lists in frozen dataclass), FM-012-B1 (mutable DEFAULT), FM-013-B1 (Zone 4 assertion premature), FM-017-B1 (confidence score mismatch), FM-033-B1 (str vs Path). Seven findings identify inconsistencies between deliverables or within a single deliverable's claims vs specifications. The cross-deliverable XML parser disagreement (FM-006-B1) is the most impactful. |
| Methodological Rigor | 0.20 | Positive (+0.02) | The STRIDE/DREAD/Attack Trees/PASTA methodology is thoroughly applied. The trust boundary model is well-structured. The red team scope uses appropriate PTES + OSSTMM methodology. Minor methodological gaps exist (FM-002-B1 exception handling, FM-009-B1 detection ordering, FM-028-B1 stringly-typed enum) but the overall rigor is high. |
| Evidence Quality | 0.15 | Neutral (0.00) | FM-014-B1 (DREAD calibration), FM-016-B1 (CWE misclassification), FM-021-B1 (incomplete safe_load enumeration), FM-024-B1 (nesting depth not validated against data), FM-036-B1 (type enforcement claim). Five findings identify evidence quality concerns, but they are balanced by strong evidence in other areas (attack trees with clear likelihood assessments, PASTA stages with concrete scenarios, DREAD scoring with dimension-level rationale). |
| Actionability | 0.15 | Negative (-0.03) | FM-008-B1 (glob implementation unspecified), FM-018-B1 (Python-incompatible regex guidance), FM-019-B1 (ALLOWED_TAGS extensibility), FM-025-B1 (regex compilation timing), FM-027-B1 (CLI flag confusion), FM-031-B1 (time window). Six findings identify areas where the specifications are not directly implementable without further interpretation or do not account for Python-specific limitations. |
| Traceability | 0.10 | Neutral (+0.01) | FM-030-B1 (NIST CSF mapping), FM-032-B1 (line number brittleness), FM-034-B1 (missing mitigation ID for reinject count). Three minor traceability findings. Overall traceability is strong: mitigations map to threats, threats map to components, DREAD scores map to priorities, NIST CSF coverage is documented. |

### Estimated Dimension Scores (Pre-Correction)

| Dimension | Weight | Estimated Score | Weighted |
|-----------|--------|----------------|----------|
| Completeness | 0.20 | 0.84 | 0.168 |
| Internal Consistency | 0.20 | 0.82 | 0.164 |
| Methodological Rigor | 0.20 | 0.93 | 0.186 |
| Evidence Quality | 0.15 | 0.88 | 0.132 |
| Actionability | 0.15 | 0.85 | 0.128 |
| Traceability | 0.10 | 0.90 | 0.090 |
| **Weighted Composite** | **1.00** | | **0.868** |

### Estimated Dimension Scores (Post-Correction of Critical + Major Findings)

| Dimension | Weight | Estimated Score | Weighted |
|-----------|--------|----------------|----------|
| Completeness | 0.20 | 0.94 | 0.188 |
| Internal Consistency | 0.20 | 0.95 | 0.190 |
| Methodological Rigor | 0.20 | 0.95 | 0.190 |
| Evidence Quality | 0.15 | 0.93 | 0.140 |
| Actionability | 0.15 | 0.93 | 0.140 |
| Traceability | 0.10 | 0.93 | 0.093 |
| **Weighted Composite** | **1.00** | | **0.941** |

**Assessment:** Pre-correction composite of 0.868 falls in the REVISE band. Addressing all seven Critical findings and the top Major findings would raise the composite to an estimated 0.941, above the 0.92 PASS threshold.

---

*FMEA Report Version: 1.0.0*
*Strategy: S-012 (Failure Mode and Effects Analysis)*
*Template: `.context/templates/adversarial/s-012-fmea.md` v1.0.0*
*SSOT: `.context/rules/quality-enforcement.md`*
*Date: 2026-02-22*
*Reviewer: adv-executor*
*Quality Gate: QG-B1*
*Workflow: ast-universal-20260222-001*
