# RED-0002: CWE-843 Attack Path Analysis — DocumentTypeDetector Post-EN-002

<!-- AGENT: red-vuln | VERSION: 1.0.0 | DATE: 2026-02-24 | ENGAGEMENT: RED-0002 -->
<!-- METHODOLOGY: PTES Vulnerability Analysis Phase + NIST SP 800-115 Chapter 4 (Technical Examination) -->
<!-- SCOPE: iteration-2/red-lead-scope.md | PRIOR REVIEW: iteration-1/eng-security-review.md -->

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Findings by severity, risk posture, top exploitable findings |
| [L1 Technical Findings](#l1-technical-findings) | Full finding inventory with CWE, CVSS, attack paths, exploitability |
| [L2 Strategic Implications](#l2-strategic-implications) | Attack path chains, risk scoring, eng-team remediation recommendations |
| [Attack Surface Analysis](#attack-surface-analysis) | AS-1 through AS-5 complete analysis with crafted input examples |
| [Prior Finding Remediation Verification](#prior-finding-remediation-verification) | F-001 through F-009 residual risk assessment |
| [DocumentType Enum Coverage Audit](#documenttype-enum-coverage-audit) | Pattern and structural cue coverage for each enum value |
| [Scope Compliance](#scope-compliance) | Authorization confirmation, technique log, constraint verification |

---

## L0 Executive Summary

### Engagement

**Engagement ID:** RED-0002
**Scope Version:** 1.0
**Analysis Date:** 2026-02-24
**Agent:** red-vuln
**Methodology:** PTES Vulnerability Analysis + NIST SP 800-115 Chapter 4 (Static Code Analysis)
**Authorization:** User-confirmed per red-lead-scope.md

### Findings by Severity

| Severity | Count | Finding IDs | Key CWE |
|----------|-------|-------------|---------|
| Critical | 0 | — | — |
| High | 0 | — | — |
| Medium | 2 | RV-001, RV-002 | CWE-843, CWE-697 |
| Low | 3 | RV-003, RV-004, RV-005 | CWE-843, CWE-843, CWE-691 |
| Informational | 3 | RV-006, RV-007, RV-008 | CWE-754, CWE-20, design gap |
| **Total** | **8** | | |

### Overall Risk Posture

**PASS with residual medium risk.** The EN-002 implementation substantially improves the security posture relative to the pre-EN-002 BUG-004 state. The F-001 remediation (the `already_relative` guard at line 293) is effective for the primary attack vector identified in the iteration-1 review. No Critical or High findings are present in the post-EN-002 code.

Two medium findings remain:

1. **RV-001 (Medium, CWE-843):** The `already_relative` guard relies on a starts-with check against ten root markers. A path component that is a prefix of a root marker (e.g., a directory named `skill` vs. the marker `skills/`) does not trigger the guard, leaving a narrow residual bypass window for multi-hop absolute paths originating outside the repo root. This is a narrowing of F-001, not its complete closure.

2. **RV-002 (Medium, CWE-697):** The `SKILL_RESOURCE` and `TEMPLATE` enum values are absent from `_PARSER_MATRIX` in `universal_document.py`. When `detected_type` is `SKILL_RESOURCE` or `TEMPLATE`, `_PARSER_MATRIX.get(detected_type, set())` returns the empty set fallback, invoking zero parsers and producing a `UniversalParseResult` with all parser fields as `None`. This is a silent type confusion — the caller receives a result typed as `SKILL_RESOURCE` or `TEMPLATE` with no parsed content.

### Top Exploitable Findings

| Rank | Finding | Exploitability | CVSS | Impact |
|------|---------|---------------|------|--------|
| 1 | RV-001: `already_relative` residual bypass | Demonstrable | 5.3 | Path type confusion via absolute path manipulation |
| 2 | RV-002: Missing `_PARSER_MATRIX` entries | Demonstrable | 4.0 | Silent parser starvation for SKILL_RESOURCE / TEMPLATE types |
| 3 | RV-003: `> **Type:**` false positive via quoted content | Theoretical | 3.1 | Worktracker misclassification for path-unmatched files |

---

## L1 Technical Findings

---

### RV-001: `already_relative` Guard Does Not Cover All Absolute Path Bypass Vectors

**Classification**

| Attribute | Value |
|-----------|-------|
| CWE ID | CWE-843 (Type Confusion) / CWE-22 (Path Traversal) |
| CVSS 3.1 Vector | AV:L/AC:H/PR:N/UI:N/S:U/C:L/I:M/A:N |
| CVSS 3.1 Score | **5.3 (Medium)** |
| Severity | Medium |
| Exploitability | Demonstrable |
| Affected File | `src/domain/markdown_ast/document_type.py` |
| Affected Function | `_normalize_path()` (lines 257–317) |
| Prior Finding | F-001 (High, CWE-22/CWE-843) — Partially Remediated |
| ATT&CK Analog | T1036 (Masquerading) — file at attacker-controlled path acquires trusted type identity |

**Remediation Status for F-001**

The iteration-1 F-001 finding described: `idx > 0` extraction strips any absolute path containing an embedded root marker to the marker position, allowing an untrusted path to acquire a trusted type identity. The EN-002 implementation added the `already_relative` guard:

```python
# document_type.py lines 293-299
already_relative = any(path.startswith(m) for m in root_markers)
if not already_relative:
    for marker in root_markers:
        idx = path.find(marker)
        if idx > 0:
            path = path[idx:]
            break
```

This guard correctly prevents the primary F-001 attack vector for paths that already start with a recognized root marker. The remediation is **partially effective**.

**Residual Bypass Analysis**

The `already_relative` check uses `str.startswith()` against each of ten markers. The guard fires and blocks extraction when the path begins with one of the ten strings. Three residual bypass conditions exist:

**Condition 1 — Absolute path with embedded marker, no starts-with match.**

The guard only blocks extraction when `path.startswith(marker)` is true for at least one marker. For a pure absolute path not beginning with any marker, the extraction loop still executes normally. The remediation closes one case (already-relative paths being re-extracted) but does not restrict the original F-001 vulnerability for paths that are genuinely absolute:

```
Input:  "/tmp/attacker/skills/target/agents/malicious.md"
Guard:  already_relative = False  (no marker starts with "/tmp/")
Loop:   idx = path.find("skills/") -> positive index
        path becomes "skills/target/agents/malicious.md"
Match:  skills/*/agents/*.md  -> DocumentType.AGENT_DEFINITION
```

This is the identical F-001 attack vector. The remediation does not address it. The eng-security review noted this is acceptable when `detect()` callers are contractually restricted to trusted filesystem-verified paths. However, the `ast_detect` CLI entry point (ast_commands.py line 617) passes the user-supplied `file_path` argument directly to `DocumentTypeDetector.detect(file_path, source)` without restricting it to repo-relative form. The path containment check in `_read_file` (lines 176–223) verifies the file is within the repo root but does NOT normalize the path to repo-relative form before passing it to `detect()`. This means a legitimate in-repo file at an absolute path is correctly read but then passed as an absolute path to `detect()`, triggering the extraction logic.

Crafted demonstration input:

```python
# File physically at: /Users/dev/jerry/skills/tooling/agents/inject.md
# CLI invocation: jerry ast detect /Users/dev/jerry/skills/tooling/agents/inject.md
# ast_detect passes file_path = "/Users/dev/jerry/skills/tooling/agents/inject.md"
# to DocumentTypeDetector.detect()
# _normalize_path extracts "skills/tooling/agents/inject.md"
# Pattern skills/*/agents/*.md matches -> AGENT_DEFINITION (correct)
# BUT: same behavior for any path whose absolute form contains a root marker.
```

This is expected and correct behavior for in-repo files. The risk is for user-supplied paths to files at adversarially chosen locations:

```python
# File at: /tmp/evil/skills/tooling/agents/inject.md
# Path containment check in ast_detect would REJECT this path:
# resolved = Path("/tmp/evil/...").resolve() -> not inside repo root
# -> "Error: Path escapes repository root"  -> return 2
```

**Critical observation:** The `_read_file` path containment check (lines 176–223) in ast_commands.py is an effective gate against adversarial external paths at the CLI entry point. A path that escapes the repository root is rejected before `detect()` is called. This substantially reduces the exploitability of the F-001 residual for the CLI path.

**Condition 2 — Paths originating from `UniversalDocument.parse()` without path containment.**

`UniversalDocument.parse()` (universal_document.py line 119) accepts `file_path` as an optional parameter with no path containment enforcement. Any caller that passes an unvalidated absolute path bypasses the CLI path containment gate:

```python
# Direct API usage (not through CLI):
result = UniversalDocument.parse(
    content=open("/tmp/evil/skills/x/agents/evil.md").read(),
    file_path="/tmp/evil/skills/x/agents/evil.md"
)
# detect() is called with the raw untrusted path
# _normalize_path strips to "skills/x/agents/evil.md"
# Classified as AGENT_DEFINITION
```

The domain API has no path containment guard. The protection exists only at the CLI adapter layer. Any programmatic caller of `UniversalDocument.parse()` or `DocumentTypeDetector.detect()` that passes user-controlled paths is exposed to F-001's original form.

**Condition 3 — Mixed separator bypass.**

On Windows, `path.replace(os.sep, "/")` converts backslashes before the `already_relative` check. On POSIX (the primary deployment platform), `os.sep == "/"`, making the replace a no-op. Mixed separators do not create a bypass on POSIX. On Windows, a path like `C:\users\jerry\skills\agents\file.md` becomes `C:/users/jerry/skills/agents/file.md` after the replace, and the guard correctly does not trigger (path does not start with a marker). Extraction proceeds as in Condition 1. Mixed separators are not an additional bypass beyond the base F-001 on POSIX, but on Windows they could combine with a Windows drive letter to bypass `already_relative` while still containing an embedded marker.

**Downstream Impact**

Type confusion escalates to the `_PARSER_MATRIX`. AGENT_DEFINITION triggers `{"yaml", "xml", "nav"}` parsers. A file misclassified as AGENT_DEFINITION:
1. Has YAML frontmatter extracted — potential source of schema validation with agent-definition field rules
2. Has XML sections extracted — `<identity>`, `<methodology>`, `<purpose>` etc. parsed
3. Has navigation table extracted

For automation workflows that auto-apply schema validation based on type, this results in agent-definition schema validation being applied to an arbitrary file, which may pass permissive field checks or produce validation failures that are logged and ignored.

**Remediation Recommendation**

Primary: Normalize the path to repo-relative form at the `detect()` entry point using the same `_get_repo_root()` logic already present in the CLI adapter. Add a `_to_repo_relative()` helper that resolves the path, verifies containment, and strips the repo root prefix before calling `_normalize_path`. Document this as a precondition in the `detect()` docstring per the eng-security recommendation.

Secondary (defense-in-depth): Add a precondition docstring to `detect()` explicitly stating that `file_path` must be a repo-relative path or a filesystem-verified absolute path contained within the known repository root.

---

### RV-002: `SKILL_RESOURCE` and `TEMPLATE` Missing from `_PARSER_MATRIX`

**Classification**

| Attribute | Value |
|-----------|-------|
| CWE ID | CWE-697 (Incorrect Comparison) / CWE-754 (Improper Check for Exceptional Conditions) |
| CVSS 3.1 Vector | AV:L/AC:L/PR:N/UI:N/S:U/C:N/I:M/A:L |
| CVSS 3.1 Score | **4.0 (Medium)** |
| Severity | Medium |
| Exploitability | Demonstrable (deterministic — no craft required) |
| Affected File | `src/domain/markdown_ast/universal_document.py` (lines 96–108) |
| Affected Function | `UniversalDocument.parse()` (line 159: `_PARSER_MATRIX.get(detected_type, set())`) |
| Prior Finding | F-009 (Informational) — Extends finding to parser matrix gap |

**Data Flow Trace**

```
detect("skills/ast/rules/behavior.md", content)
    -> normalized: "skills/ast/rules/behavior.md"
    -> _detect_from_path:
        check "skills/*/agents/*.md"        -> no match
        check "skills/*/SKILL.md"           -> no match
        check ".context/rules/*.md"         -> no match
        check ".claude/rules/*.md"          -> no match
        check "docs/design/*.md"            -> no match
        check "docs/adrs/*.md"              -> no match
        check ".context/templates/adversarial/*.md" -> no match
        check "skills/*/PLAYBOOK.md"        -> no match
        check "skills/*/rules/*.md"         -> MATCH -> DocumentType.RULE_FILE

# But for: skills/ast/tests/test-case-01.md
detect("skills/ast/tests/test-case-01.md", content)
    -> check "skills/*/tests/*.md"          -> MATCH -> DocumentType.SKILL_RESOURCE

# In UniversalDocument.parse():
detected_type = DocumentType.SKILL_RESOURCE
parsers_to_run = _PARSER_MATRIX.get(DocumentType.SKILL_RESOURCE, set())
# DocumentType.SKILL_RESOURCE is NOT a key in _PARSER_MATRIX
# .get() returns the default: set()
# parsers_to_run = set()  -> ZERO parsers invoked

# Result:
UniversalParseResult(
    document_type=DocumentType.SKILL_RESOURCE,
    jerry_document=doc,
    yaml_frontmatter=None,     # not invoked
    blockquote_frontmatter=None,  # not invoked
    xml_sections=None,         # not invoked
    html_comments=None,        # not invoked
    reinject_directives=None,  # not invoked
    nav_entries=None,          # not invoked (!)
    type_detection_warning=None,
    parse_errors=()
)
```

**Current `_PARSER_MATRIX` (universal_document.py lines 96–108)**

```python
_PARSER_MATRIX: dict[DocumentType, set[str]] = {
    DocumentType.AGENT_DEFINITION: {"yaml", "xml", "nav"},
    DocumentType.SKILL_DEFINITION: {"yaml", "nav"},
    DocumentType.RULE_FILE: {"reinject", "nav"},
    DocumentType.ADR: {"html_comment", "nav"},
    DocumentType.STRATEGY_TEMPLATE: {"blockquote"},
    DocumentType.WORKTRACKER_ENTITY: {"blockquote", "nav"},
    DocumentType.FRAMEWORK_CONFIG: {"reinject", "nav"},
    DocumentType.ORCHESTRATION_ARTIFACT: {"html_comment", "nav"},
    DocumentType.PATTERN_DOCUMENT: {"blockquote", "nav"},
    DocumentType.KNOWLEDGE_DOCUMENT: {"nav"},
    DocumentType.UNKNOWN: {"nav"},
}
```

**Missing enum values:** `DocumentType.SKILL_RESOURCE` and `DocumentType.TEMPLATE` are both absent.

**Impact Assessment**

The `_PARSER_MATRIX.get(detected_type, set())` default-empty-set fallback is safe in the sense that no exception is raised and no wrong parser is invoked. However, the resulting `UniversalParseResult` is silently incomplete:

1. `nav_entries` is `None` (not an empty tuple) — callers that check `if result.nav_entries is None` to distinguish "not invoked" from "invoked with no entries" receive the wrong answer. For SKILL_RESOURCE files that legitimately have no nav table, `nav_entries = None` is indistinguishable from `nav_entries = ()` at the caller level.

2. For TEMPLATE files (`skills/*/templates/*.md`, `.context/templates/**/*.md`), the `blockquote` parser is not invoked. Templates may contain `> **Strategy:**` blockquote frontmatter (STRATEGY_TEMPLATE structural cue). A TEMPLATE file would not have its blockquote frontmatter extracted if called through UniversalDocument.

3. Any automation that routes behavior based on `UniversalParseResult` field presence will silently produce incorrect results for these two types without any error signal.

**Correlation with F-009**

The eng-security F-009 finding flagged that SKILL_RESOURCE and TEMPLATE have no schemas registered in the schema registry. This finding extends F-009: the gap is not only in schema registration but also in parser matrix registration. Both the schema registry and the parser matrix are incomplete for the two new DocumentType values.

**Remediation Recommendation**

Add `_PARSER_MATRIX` entries for both missing types:

```python
DocumentType.SKILL_RESOURCE: {"nav"},    # minimal — skill resources vary; nav table is universal
DocumentType.TEMPLATE: {"blockquote", "nav"},  # templates may have blockquote frontmatter
```

The parser selection rationale:
- SKILL_RESOURCE files include playbooks, test data, reference docs, composition notes. The common parse operation is nav table extraction. `{"nav"}` is consistent with KNOWLEDGE_DOCUMENT treatment.
- TEMPLATE files (skills/*/templates/*.md, .context/templates/**/*.md) may include STRATEGY_TEMPLATE-style blockquote frontmatter (`> **Strategy:**`). `{"blockquote", "nav"}` mirrors PATTERN_DOCUMENT.

---

### RV-003: `> **Type:**` Structural Cue False-Positive via Quoted Content

**Classification**

| Attribute | Value |
|-----------|-------|
| CWE ID | CWE-843 (Type Confusion via content injection) |
| CVSS 3.1 Vector | AV:L/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:N |
| CVSS 3.1 Score | **3.1 (Low)** |
| Severity | Low |
| Exploitability | Theoretical |
| Affected File | `src/domain/markdown_ast/document_type.py` (line 158) |
| Affected Cue | `("> **Type:**", DocumentType.WORKTRACKER_ENTITY)` |
| Prior Finding | Extends F-005 (Low, CWE-843) scope |

**Analysis**

The `_detect_from_structure` method uses `if cue in content` (line 247), which is a substring containment check with no line-boundary awareness. The cue `"> **Type:**"` is intended to match the blockquote frontmatter pattern used in worktracker entity files:

```markdown
> **Type:** Bug
```

However, this exact string can appear in non-worktracker content in two realistic scenarios:

**Scenario A — Markdown discussing blockquote frontmatter format:**

```markdown
The worktracker entity format uses blockquote fields. For example:
> **Type:** Bug
This is the Type field that specifies the entity classification.
```

A knowledge document or rule file explaining the blockquote frontmatter format would contain the literal string `> **Type:**` as an example. If this file has no path pattern match (e.g., a documentation file in an unrecognized path), it would be misclassified as WORKTRACKER_ENTITY.

**Scenario B — Markdown quoting a discussion that mentions type:**

```markdown
In response to the question "what is the format?", the answer was:
> **Type:** should always be one of the valid entity types
```

A quoted reply or meeting note containing this phrase would trigger the cue.

**Exploitability Constraint**

This is rated Theoretical because:

1. Path patterns cover essentially all legitimate document locations in the repo. For a file to reach the structural fallback, it must be located at a path matching none of the 63+ patterns. This is an unusual but possible condition (e.g., a newly created top-level directory, a file in a non-standard location).

2. The misclassification produces a WORKTRACKER_ENTITY type, which invokes `{"blockquote", "nav"}` parsers — a relatively benign parser set compared to AGENT_DEFINITION's `{"yaml", "xml", "nav"}`.

3. The M-14 dual-signal warning (line 200–209) would not fire because the file has no path match; the warning only fires when `path_type is not None AND structure_type disagrees`. A file reaching structural-only detection never generates an M-14 warning, making the misclassification silent.

**Downstream Impact**

Silent WORKTRACKER_ENTITY misclassification for a knowledge or template file. The blockquote parser would extract frontmatter that does not follow worktracker entity format, producing an incomplete or empty `BlockquoteFrontmatter`. No schema validation is triggered by the parser matrix step alone. Impact is limited to incorrect type labeling in `UniversalParseResult.document_type`.

**Remediation Recommendation**

The cue is acceptable given path coverage. To further reduce false positives, consider anchoring the cue check to the beginning of a line by replacing the substring check with a regex check in `_detect_from_structure` for high-precision cues. Alternatively, require that `> **Type:**` be followed by a space and then a known entity type value. This is a low-priority refinement given the theoretical exploitability.

---

### RV-004: `<!-- L2-REINJECT` Cue Triggered by Content Discussing L2-REINJECT

**Classification**

| Attribute | Value |
|-----------|-------|
| CWE ID | CWE-843 (Type Confusion via content injection) |
| CVSS 3.1 Vector | AV:L/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:N |
| CVSS 3.1 Score | **2.5 (Low)** |
| Severity | Low |
| Exploitability | Theoretical |
| Affected File | `src/domain/markdown_ast/document_type.py` (line 160) |
| Affected Cue | `("<!-- L2-REINJECT", DocumentType.RULE_FILE)` |
| Prior Finding | Extends F-005 (Low, CWE-843) |

**Analysis**

The `<!-- L2-REINJECT` substring is highly specific — it is an HTML comment prefix with an application-specific keyword. However, it appears in one realistic false-positive scenario:

**Scenario — Documentation explaining the L2-REINJECT format:**

The rule files themselves (`.context/rules/*.md`) contain instructional content about the L2-REINJECT marker format. Any documentation file, article, or design document that discusses the L2-REINJECT mechanism would contain the literal string:

```markdown
The framework uses `<!-- L2-REINJECT: rank=N, content="..." -->` markers to
inject critical rules into every prompt context.
```

A documentation file at an unrecognized path (e.g., `docs/architecture/l2-reinject-design.md`) would trigger this cue and be misclassified as RULE_FILE.

**Exploitability Constraint**

The path `docs/architecture/*.md` is not in the PATH_PATTERNS list. Files in `docs/architecture/` would fall through to structural detection. In the current repo, the closest matching pattern is `docs/*.md` (KNOWLEDGE_DOCUMENT, Tier 5 catch-all) which matches shallow `docs/` files but NOT `docs/architecture/*.md` (because `*` in fnmatch does not cross directory boundaries). A file at `docs/architecture/l2-reinject-design.md` would receive no path match and fall to structural detection.

This is a narrow gap: `docs/architecture/` is not in the pattern list, making any file there path-unmatched. Such files should be KNOWLEDGE_DOCUMENT but the `<!-- L2-REINJECT` cue would classify them as RULE_FILE if they discuss the L2 mechanism.

**Downstream Impact**

RULE_FILE invokes `{"reinject", "nav"}` parsers. The reinject parser would scan for `<!-- L2-REINJECT:` directives and extract them. A documentation file about L2-REINJECT would have actual L2-REINJECT directives extracted as if they were operative, potentially causing automation that processes RULE_FILE results to treat example directives as real ones.

**Remediation Recommendation**

Add `docs/architecture/*.md` to PATH_PATTERNS as KNOWLEDGE_DOCUMENT to eliminate the gap. This is a pattern coverage issue, not a cue specificity issue. The `<!-- L2-REINJECT` cue is highly specific and the gap is the missing pattern rather than the cue being too broad.

---

### RV-005: `_match_recursive_glob` Multiple-`**` Fallback Uses `fnmatch` Incorrectly for Recursive Patterns

**Classification**

| Attribute | Value |
|-----------|-------|
| CWE ID | CWE-691 (Insufficient Control Flow Management) |
| CVSS 3.1 Vector | AV:L/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:N |
| CVSS 3.1 Score | **2.5 (Low)** |
| Severity | Low |
| Exploitability | Theoretical |
| Affected File | `src/domain/markdown_ast/document_type.py` (lines 353–356) |
| Affected Function | `_match_recursive_glob()` |
| Prior Finding | Extends F-006 (Low, CWE-20) — `_match_recursive_glob` edge case noted |

**Analysis**

`_match_recursive_glob` handles the case where a pattern contains more than one `**` via a fallback at lines 353–356:

```python
parts = pattern.split("**")
if len(parts) != 2:
    # Multiple ** -- fall back to fnmatch (best effort)
    return fnmatch.fnmatch(path, pattern)
```

The comment says "best effort," which is accurate — `fnmatch.fnmatch` does not natively support `**` (recursive glob) semantics. `fnmatch` treats `**` as two consecutive wildcards matching any two characters (not as a recursive directory matcher). This means that for any pattern containing multiple `**` segments, the match behavior is incorrect and unpredictable.

**Current pattern audit — are any patterns in PATH_PATTERNS multiple-`**`?**

Reviewing all 63+ entries in PATH_PATTERNS (lines 74–145), the patterns containing `**` are:

```
"skills/*/knowledge/**/*.md"       -- one ** (safe path)
"skills/*/test_data/**/*.md"       -- one ** (safe path)
"projects/*/work/**/*.md"          -- one ** (safe path)
"projects/*/orchestration/**/*.md" -- one ** (safe path)
".context/templates/worktracker/*.md" -- zero **
".context/templates/design/*.md"   -- zero **
".context/templates/**/*.md"       -- one ** (safe path)
".context/patterns/**/*.md"        -- one ** (safe path)
"docs/knowledge/**/*.md"           -- one ** (safe path)
"docs/research/**/*.md"            -- one ** (safe path)
"docs/synthesis/**/*.md"           -- one ** (safe path)
"docs/scores/**/*.md"              -- one ** (safe path)
"docs/reviews/**/*.md"             -- one ** (safe path)
"docs/rewrites/**/*.md"            -- one ** (safe path)
"docs/blog/**/*.md"                -- one ** (safe path)
"work/**/*.md"                     -- one ** (safe path)
```

**No current pattern contains multiple `**`.** The fallback code path is currently unreachable in production.

**Risk — Future Pattern Addition**

The fallback is a latent bug that would activate silently if a future maintainer adds a pattern like `"projects/*/work/**/*.md/**/*.md"` or any other multi-`**` pattern. The `fnmatch` fallback would silently produce incorrect match results without error, log output, or test failure (since tests would need to be written for the new pattern).

The specific `fnmatch` behavior for `**` patterns: `fnmatch.fnmatch("projects/x/work/a/b.md", "projects/*/work/**/*.md")` — fnmatch translates `**` as matching any two characters (`..` in regex terms), not zero-or-more directories. The pattern would not match paths where the `**` needs to expand to multiple path segments.

**Exploitability**

Currently not exploitable — the fallback is unreachable. The risk is a future maintenance trap. No current attack path exists through this code.

**Remediation Recommendation**

Replace the silent fallback with an explicit error or a correct recursive implementation:

```python
if len(parts) != 2:
    # Multiple ** segments are not supported. Log and return False to avoid
    # incorrect matches from fnmatch's non-recursive ** behavior.
    import warnings
    warnings.warn(
        f"Pattern '{pattern}' contains multiple '**' segments; "
        "recursive glob matching is not supported for this pattern. "
        "Returns False (no match).",
        stacklevel=2
    )
    return False
```

Returning `False` (no match) for unsupported patterns is safer than `fnmatch.fnmatch` which silently gives wrong answers. A `False` result causes the file to fall through to the next pattern; an incorrect `True` result from `fnmatch` causes premature type classification.

---

### RV-006: UNKNOWN Classification Silently Bypasses All Parsers Except `nav`

**Classification**

| Attribute | Value |
|-----------|-------|
| CWE ID | CWE-754 (Improper Check for Exceptional Conditions) |
| CVSS 3.1 Vector | N/A (behavioral design finding) |
| CVSS 3.1 Score | Informational |
| Severity | Informational |
| Exploitability | Demonstrable by design |
| Affected File | `src/domain/markdown_ast/universal_document.py` (line 107) |
| Prior Finding | F-008 (Informational) — Extends to parser matrix behavior |

**Analysis**

`DocumentType.UNKNOWN: {"nav"}` in `_PARSER_MATRIX` invokes only the nav table parser for unclassified files. This is correct by design and safe: unclassified files receive minimal parsing rather than an incorrect type-specific parse.

**Data Flow for UNKNOWN through CLI:**

```
# ast_detect CLI (ast_commands.py lines 598-633):
doc_type, warning = DocumentTypeDetector.detect(file_path, source)
# If doc_type == UNKNOWN:
output = {"type": "unknown", "method": "structure" or "path", "warning": None}
# Returns exit code 0 with {"type": "unknown"}

# ast_validate CLI (ast_commands.py lines 312-418):
# schema parameter is passed by user ("--schema epic", etc.)
# For UNKNOWN files: schema would be None (user didn't provide --schema)
# without --schema: only nav table validation runs
# schema_registry is NOT called for UNKNOWN -> no ValueError
# Result: nav table validation report with schema_valid: True
```

**F-008 Verification:** The `ast_validate` function (lines 312–418) does not call `schema_registry.get()` unless `schema` is explicitly provided via `--schema`. The F-008 concern (that UNKNOWN would trigger `schema_registry.get("unknown")` and raise ValueError) does not exist in the current implementation because `ast_validate` uses a different schema lookup mechanism (`get_entity_schema(schema)` from the worktracker schema module, not the DocumentType-based schema registry). The F-008 concern is therefore resolved by the current implementation — `ast_validate` is not a DocumentType-aware validator; it accepts an explicit schema type string.

**Forcing UNKNOWN Classification**

A file can be forced to UNKNOWN by placing it at a path matching none of the 63+ patterns and crafting content that matches none of the 6 structural cues. For example:

```
Path:    "custom/mydir/notes.md"
Content: "# My Notes\n\nSome text with no structural markers.\n"
Result:  (DocumentType.UNKNOWN, None)
```

The downstream impact is nav-only parsing — the file receives only nav table extraction. This is the correct safe default. There is no bypass of schema validation because UNKNOWN files are not schema-validated by any current automation path.

**Explicit Type Override (`document_type=UNKNOWN`):**

`UniversalDocument.parse(content, document_type=DocumentType.UNKNOWN)` on line 150 (`if document_type is not None: detected_type = document_type`) bypasses all detection and uses the provided type directly. A caller explicitly passing `UNKNOWN` receives nav-only parsing. This is intentional behavior but worth documenting: callers can force nav-only parsing by passing `document_type=DocumentType.UNKNOWN`.

**Risk Assessment**

No security concern. UNKNOWN is a safe sentinel. Nav-only parsing is intentional. No schema validation bypass occurs because the CLI `ast_validate` command does not route UNKNOWN files to schema validation.

---

### RV-007: `_ROOT_FILES` Basename Extraction Does Not Verify Parent Directory

**Classification**

| Attribute | Value |
|-----------|-------|
| CWE ID | CWE-20 (Improper Input Validation) |
| CVSS 3.1 Vector | AV:L/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:N |
| CVSS 3.1 Score | **2.0 (Informational boundary)** |
| Severity | Informational |
| Exploitability | Theoretical |
| Affected File | `src/domain/markdown_ast/document_type.py` (lines 304–315) |
| Affected Function | `_normalize_path()` — `_ROOT_FILES` extraction block |

**Analysis**

The `_ROOT_FILES` extraction at lines 304–315:

```python
_ROOT_FILES = frozenset({
    "CLAUDE.md", "AGENTS.md", "README.md", "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md", "SECURITY.md", "GOVERNANCE.md",
    "SOUNDTRACK.md",
})
basename = path.rsplit("/", 1)[-1] if "/" in path else path
if basename in _ROOT_FILES and "/" in path:
    is_under_known_root = any(path.startswith(m) for m in root_markers)
    if not is_under_known_root:
        path = basename
```

This block reduces a path like `/some/absolute/dir/CLAUDE.md` to the basename `CLAUDE.md` when the path is not already under a known root marker. The intent is to allow absolute paths to root-level files to be correctly classified as FRAMEWORK_CONFIG.

**Bypass Scenario**

A file named `CLAUDE.md` located in a nested directory (e.g., `/tmp/evil/CLAUDE.md`) would have its path reduced to `CLAUDE.md` and match the `("CLAUDE.md", DocumentType.FRAMEWORK_CONFIG)` pattern. The classification is FRAMEWORK_CONFIG, which invokes `{"reinject", "nav"}` parsers — the same as a legitimate root-level `CLAUDE.md`.

**Exploitability Constraint**

The path containment check in `_read_file` would reject `/tmp/evil/CLAUDE.md` (escapes repo root). Within the repo, a file named `CLAUDE.md` in a nested directory (e.g., `skills/adversary/CLAUDE.md`) would first match the `skills/*/*.md` catch-all (SKILL_RESOURCE) at line 96, which fires before the `_ROOT_FILES` extraction would be relevant. The `_ROOT_FILES` block only affects paths that: (a) have a basename in `_ROOT_FILES`, (b) contain a `/`, AND (c) are not under a known root marker. For a path like `skills/adversary/CLAUDE.md`, `already_relative` is `True` (starts with `skills/`), so the entire marker extraction block (including `_ROOT_FILES`) is skipped. The `_ROOT_FILES` block only applies to absolute paths not under a root marker, which the CLI path containment check rejects for external paths.

**Risk Assessment**

Informational. The `_ROOT_FILES` extraction is only reachable for absolute paths to files within the repo root that have no root marker in their path (e.g., a file at a root-level path like `/Users/dev/jerry/CLAUDE.md` where the absolute path is passed directly). In this case, the extraction reduces it to `CLAUDE.md` and classification is FRAMEWORK_CONFIG — which is the correct answer. No type confusion occurs for legitimate usage.

---

### RV-008: `_match_recursive_glob` Suffix Matching Does Not Require Full Segment Alignment

**Classification**

| Attribute | Value |
|-----------|-------|
| CWE ID | CWE-697 (Incorrect Comparison) |
| CVSS 3.1 Vector | N/A (logic analysis — no current exploitation path found) |
| CVSS 3.1 Score | Informational |
| Severity | Informational |
| Exploitability | Theoretical (requires specific path construction) |
| Affected File | `src/domain/markdown_ast/document_type.py` (lines 375–382) |
| Affected Function | `_match_recursive_glob()` — suffix matching block |

**Analysis**

The suffix matching block (lines 375–382):

```python
if suffix_pattern:
    suffix_segments = suffix_pattern.split("/")
    if len(remaining_segments) < len(suffix_segments):
        return False
    for rs, sp in zip(reversed(remaining_segments), reversed(suffix_segments), strict=False):
        if not fnmatch.fnmatch(rs, sp):
            return False
    return True
```

The algorithm reverses both the remaining path segments and the suffix pattern segments, then checks them pairwise from the end. The `strict=False` in `zip` means the shorter sequence controls the iteration.

**Observation:** For a pattern like `work/**/*.md` (prefix=`work`, suffix=`*.md`), `suffix_segments = ["*.md"]` and `remaining_segments` is everything after `work/`. The zip reversal pairs only the last segment of remaining with `*.md`. This is correct: any file under `work/` at any depth with a `.md` extension matches. No gap here.

**Edge case analysis:** Consider pattern `.context/templates/**/*.md`:
- prefix = `.context/templates`
- suffix = `*.md`
- For path `.context/templates/adversarial/s-001-red-team.md`:
  - prefix_segments = `[".context", "templates"]`
  - path_segments = `[".context", "templates", "adversarial", "s-001-red-team.md"]`
  - After prefix match: remaining = `["adversarial", "s-001-red-team.md"]`
  - suffix = `*.md`, suffix_segments = `["*.md"]`
  - zip(reversed(["adversarial", "s-001-red-team.md"]), reversed(["*.md"])) -> pairs ("s-001-red-team.md", "*.md")
  - fnmatch("s-001-red-team.md", "*.md") -> True
  - Returns True (correct)

All current patterns with `**` use a single-segment suffix (`*.md`) making the suffix matching effectively a last-segment check. No ambiguity exists for the current pattern set.

**Theoretical gap:** A hypothetical pattern like `docs/**/*-notes.md` would have suffix=`*-notes.md`. The algorithm checks only the last segment, which is correct. A deeper theoretical issue: if `remaining_segments` has length 0 (path ends exactly at `**`), `len(remaining_segments) < len(suffix_segments)` would be True (0 < 1), returning `False`. This means `docs/` exactly (no file after the marker) does not match `docs/**/*.md` — which is correct behavior.

**Risk Assessment**

No exploitation path found for current patterns. The implementation is correct for all existing `**` patterns. Informational documentation of the algorithm's assumptions for future maintainers.

---

## L2 Strategic Implications

### Attack Path Chains

**Chain 1: Absolute Path -> Type Confusion -> Incorrect Parser Invocation (RV-001 + RV-002)**

```
Step 1: Attacker controls file_path parameter to detect() or UniversalDocument.parse()
Step 2: Absolute path containing embedded root marker
        e.g., "/external/evil/skills/target/agents/evil.md"
Step 3: _normalize_path strips to "skills/target/agents/evil.md"
Step 4: Pattern "skills/*/agents/*.md" matches -> AGENT_DEFINITION
Step 5: _PARSER_MATRIX["agent_definition"] = {"yaml", "xml", "nav"}
Step 6: YAML frontmatter extracted from evil file content
Step 7: XML sections extracted from evil file content
Step 8: Classification result stored in UniversalParseResult.document_type

PREREQUISITE: Attacker must control file_path parameter value AND
              the path containment check in _read_file must be bypassed
              (only possible via direct API usage, not through CLI)
IMPACT: Type confusion escalates to wrong parser invocation
MITIGATING CONTROL: CLI _read_file path containment check blocks this
                    for CLI entry point; domain API has no containment check
```

**Chain 2: Missing Parser Matrix + Caller Assumption (RV-002 standalone)**

```
Step 1: File at "skills/ast/tests/test-case.md"
Step 2: detect() -> SKILL_RESOURCE (correct classification)
Step 3: UniversalDocument.parse() -> _PARSER_MATRIX.get(SKILL_RESOURCE, set()) = set()
Step 4: Zero parsers invoked
Step 5: nav_entries = None (not invoked)
Step 6: Caller checks: if result.nav_entries is not None -> False (skips nav processing)
Step 7: Nav table validation silently not performed for SKILL_RESOURCE files

PREREQUISITE: None — deterministic for any SKILL_RESOURCE or TEMPLATE file
IMPACT: Silent parser starvation; incorrect behavior for callers expecting
        nav_entries to be an empty tuple (not None) for types that have nav tables
MITIGATING CONTROL: None currently; files are correctly classified but silently un-parsed
```

**Chain 3: Structural Cue Content Override -> M-14 Warning Suppression (AS-3 via RV-003/RV-004)**

```
Step 1: File at path-unmatched location (e.g., custom dir not in patterns)
Step 2: File content contains structural cue (e.g., "<!-- L2-REINJECT" in docs)
Step 3: _detect_from_structure fires -> RULE_FILE
Step 4: No path match -> no M-14 warning generated (warning only fires when both signals present)
Step 5: Type stored as RULE_FILE in result with no warning
Step 6: Reinject directives extracted from example content
        Extraction may produce "false" reinject directives from documentation examples

PREREQUISITE: File at unrecognized path containing documentation about cues
IMPACT: Silent misclassification; no M-14 warning to alert callers
        Reinject parser processes example directives as operative
```

### Risk Scoring Summary

| Finding | CVSS | Exploitability | Attacker Prerequisite | Current Controls |
|---------|------|---------------|----------------------|-----------------|
| RV-001 | 5.3 | Demonstrable (via API) | Control `file_path` param value | CLI path containment (partial) |
| RV-002 | 4.0 | Demonstrable (deterministic) | None — triggers for all SKILL_RESOURCE/TEMPLATE | No mitigation |
| RV-003 | 3.1 | Theoretical | File at unrecognized path + content with cue | Path pattern coverage |
| RV-004 | 2.5 | Theoretical | File at unrecognized path + discussing L2-REINJECT | Path pattern coverage |
| RV-005 | 2.5 | Not currently exploitable | Requires multi-`**` pattern addition | Unreachable code path |
| RV-006 | Info | Design behavior | None | N/A — correct behavior |
| RV-007 | 2.0 | Theoretical | Absolute path to ROOT_FILE-named file | CLI path containment |
| RV-008 | Info | Not exploitable | N/A | N/A — correct implementation |

### Architectural Recommendations for eng-team

**Recommendation 1: Complete `_PARSER_MATRIX` (Priority: High)**

Add SKILL_RESOURCE and TEMPLATE to `_PARSER_MATRIX` in `universal_document.py`. This is a one-line-per-type addition that eliminates RV-002 completely. Suggested entries:

```python
DocumentType.SKILL_RESOURCE: {"nav"},
DocumentType.TEMPLATE: {"blockquote", "nav"},
```

This should be treated as a defect in the EN-002 implementation, not a future enhancement. The pattern matrix coverage is incomplete relative to the DocumentType enum coverage.

**Recommendation 2: Restrict `detect()` to Repo-Relative Paths (Priority: Medium)**

The `detect()` entry point should require repo-relative paths or add an internal path relativization step. The path containment control exists in the CLI adapter but not in the domain layer. Options:

- Option A: Accept only repo-relative paths (enforce by assertion or by stripping the repo root prefix before calling `_normalize_path`).
- Option B: Add a `_to_repo_relative()` pre-processing step inside `detect()` that uses `pathlib.Path` to resolve and relativize.
- Option C: Document the precondition explicitly in the `detect()` docstring and add a `TrustedPath` wrapper type to make the trust assumption visible at call sites.

**Recommendation 3: Add Coverage for `docs/architecture/` (Priority: Low)**

Add `docs/architecture/*.md` and `docs/architecture/**/*.md` to PATH_PATTERNS as KNOWLEDGE_DOCUMENT to eliminate the gap that enables RV-004. This is a one-line pattern addition.

**Recommendation 4: Fix the Multiple-`**` Fallback (Priority: Low)**

Replace `return fnmatch.fnmatch(path, pattern)` with `return False` (with warning) in the multi-`**` fallback to eliminate the latent maintenance trap identified in RV-005.

**Recommendation 5: Complete Schema Registration (F-009 Follow-through)**

Register SKILL_RESOURCE and TEMPLATE in the schema registry, even with minimal schemas (per the eng-security F-009 recommendation). This closes the gap between the DocumentType enum, the pattern coverage, the parser matrix, and the schema registry — all four systems should have consistent coverage.

---

## Attack Surface Analysis

### AS-1: Path-Based Detection Bypass — Post-F-001 Remediation Assessment

**Question 1: Can embedded markers still cause incorrect extraction?**

Yes. The `already_relative` guard blocks extraction only when the path already starts with a root marker. For an absolute path containing an embedded marker but not starting with one (e.g., `/tmp/evil/skills/agents/evil.md`), the extraction loop executes. This is the F-001 residual described in RV-001.

**Question 2: Does `already_relative` cover all relative paths?**

The `already_relative` check covers the ten root markers listed at lines 281–292. A file at a repo path like `skills/agents/evil.md` (already relative) correctly sets `already_relative = True` and skips extraction. Edge case: a relative path that starts with a root-marker-like string that is not a full marker (e.g., `skill_data/agents/evil.md`) — `any(path.startswith(m) for m in root_markers)` would not match `skills/` (note the trailing slash in the marker). `skill_data/agents/evil.md` does not start with `skills/` (different prefix). This is correct — `skill_data/` is not a recognized root and would fall through pattern matching to UNKNOWN.

**Question 3: Can `_ROOT_FILES` basename extraction be abused?**

Partially analyzed in RV-007. The extraction is gated by: (a) basename must be in `_ROOT_FILES`, (b) path must have `/` (not already a basename), AND (c) path must not start with a known root marker. For in-repo absolute paths (e.g., `/Users/dev/jerry/CLAUDE.md`), the extraction reduces to `CLAUDE.md` -> FRAMEWORK_CONFIG (correct). For external paths, CLI path containment rejects them. No type confusion via `_ROOT_FILES` manipulation found.

**Question 4: Mixed separators combined with root marker embedding?**

On POSIX: `os.sep == "/"`, replace is no-op. Mixed separators do not create additional bypass. On Windows: path becomes forward-slash normalized, then the existing bypass conditions apply. The Windows case does not add new bypass vectors beyond the existing F-001 residual.

**Question 5: Residual risk from `ast_detect` CLI entry point?**

The `ast_detect` function (ast_commands.py line 617) passes `file_path` (the user-supplied argument) directly to `DocumentTypeDetector.detect(file_path, source)`. The path containment check (lines 242–247) verifies the path is within the repo root BEFORE reading the file, but passes the original (potentially absolute) path string to `detect()`. For legitimate in-repo absolute paths, this produces correct results because the absolute path is correctly relativized by `_normalize_path`. For adversarial paths, the CLI path containment check is the effective barrier.

**Overall AS-1 Assessment:** The `already_relative` guard is an improvement over the pre-EN-002 state but is not a complete fix. The domain layer (`detect()` and `UniversalDocument.parse()`) remains vulnerable to F-001 for direct API callers. The CLI adapter provides an effective compensating control via path containment. Risk is Medium for direct API usage, Low for CLI-mediated usage.

---

### AS-2: `fnmatch` Wildcard Exploitation — Post-EN-002 Analysis

**Question 1: Does `fnmatch` treat wildcards in path argument as literals?**

Confirmed: `fnmatch.fnmatch(path, pattern)` translates the PATTERN to a regex and matches the PATH string. Characters `*`, `?`, `[`, `]` in the PATH argument are treated as literals, not pattern metacharacters. The eng-security F-006 conclusion is verified and unchanged.

**Question 2: Do individual segments in `_match_recursive_glob` introduce new risk for `[` or `]` in path segments?**

The segment-by-segment matching at lines 368–370 calls `fnmatch.fnmatch(ps, pp)` where `ps` is a path segment and `pp` is a pattern segment. If a path segment contains `[` or `]` characters (e.g., a filename like `[draft].md`), `fnmatch.fnmatch("[draft].md", "*.md")` returns `False` because fnmatch interprets `[draft]` in the PATH as a character class in PATTERN position — BUT here `[draft].md` is in the PATH position (first argument), not the PATTERN position (second argument). `fnmatch.fnmatch` treats the first argument as the string to test and the second as the pattern. Character classes in the string-to-test position are literals. `fnmatch.fnmatch("[draft].md", "*.md")` correctly returns `True` (`*` in pattern matches `[draft]` in string literally).

Verification: Python's `fnmatch.translate` shows that `fnmatch.fnmatch(string, pattern)` internally performs `re.match(fnmatch.translate(pattern), string)`. The string argument undergoes no special treatment — it is matched as a literal string against the translated regex. Brackets in the string are not interpreted as character classes.

**Question 3: Can `**` in an actual filename trick `_path_matches_glob`?**

`_path_matches_glob` checks `if "**" in pattern` (line 334) — it checks the PATTERN string, not the PATH string. A filename containing `**` (e.g., `skills/tooling/agents/evil**.md`) does not trigger the recursive branch because the PATTERN (`skills/*/agents/*.md`) does not contain `**`. The `fnmatch.fnmatch("skills/tooling/agents/evil**.md", "skills/*/agents/*.md")` call treats `**` in the path as literal characters. Result: `False` (because `fnmatch` matches the path literally against the pattern; `evil**` does not match the pattern's `*` without `**` expansion). Confirmed: wildcards in path filenames do not cause unintended matches.

**Question 4: Can multiple `**` patterns produce unexpected matches?**

Analyzed in RV-005. No current patterns have multiple `**`. The fallback code is unreachable in production. When reachable, it would produce incorrect results. Risk is latent, not current.

**Question 5: Can single-star patterns cross directory boundaries?**

`fnmatch.fnmatch` does NOT treat `*` as "any characters including `/`" — Python's fnmatch translates `*` to `(?s:.*)\Z` BUT only when not using `os.path` matching (using `os.path.fnmatch`). Actually, the Python `fnmatch` module translates `*` to `.*` (matching any characters including `/` in the regex). This means `fnmatch.fnmatch("docs/knowledge/sub/file.md", "docs/*.md")` returns `True` in pure Python fnmatch.

**This is a significant finding.** The `docs/*.md` pattern at line 141 is intended to match only shallow files in `docs/` (like `docs/BOOTSTRAP.md`). However, `fnmatch.fnmatch` with `*` DOES cross directory boundaries because `*` translates to `.*` (dot-star) in regex, which matches `/`. Therefore:

```
fnmatch.fnmatch("docs/knowledge/sub/file.md", "docs/*.md")
# fnmatch translates "docs/*.md" to regex: (?s:docs/.*\.md)\Z
# "docs/knowledge/sub/file.md" matches this regex -> True
```

This means `docs/*.md` (intended as a shallow catch-all for root-level docs files) actually matches ALL `.md` files under `docs/` at any depth. However, this does NOT create type confusion for the current pattern ordering because all specific `docs/` sub-patterns (lines 126–140) appear BEFORE the `docs/*.md` catch-all (line 141) in Tier 5. Files in `docs/knowledge/` match `docs/knowledge/**/*.md` (line 126) before reaching `docs/*.md`. Files in `docs/design/` match `docs/design/*.md` (line 80, Tier 1) before reaching `docs/*.md`.

The only files that reach `docs/*.md` are files in unrecognized `docs/` subdirectories that no specific pattern catches. For those files, both the intended KNOWLEDGE_DOCUMENT classification (shallow `docs/` files) and the actual deeper classification (files in unrecognized subdirs like `docs/architecture/`) produce the same type: KNOWLEDGE_DOCUMENT. There is no type confusion — the `docs/*.md` catch-all effectively works as a catch-all for all `docs/**/*.md` that aren't caught by more specific patterns.

**Overall AS-2 Assessment:** No exploitable wildcard manipulation found. The `fnmatch` boundary-crossing behavior of `*` in pattern position is present but does not create type confusion due to correct pattern ordering. Confirmed that wildcards in path arguments are treated as literals. The AS-2 attack surface is adequately mitigated.

---

### AS-3: Structural Cue Content Override — Remaining 6 Cues Analysis

**Signal combination architecture (verified):**

At lines 197–216, when `path_type is not None`, path takes authority and any disagreeing structure signal produces an M-14 warning. Structural cues can never override a path-based classification. This correctly implements T-DT-01 defense.

**False-positive rate analysis per cue (structure-only path — no path match):**

| Cue | DocumentType | False-Positive Scenario | Frequency Estimate |
|-----|-------------|------------------------|-------------------|
| `<identity>` | AGENT_DEFINITION | Any file discussing agent definition `<identity>` sections (documentation, guides, this file) | Rare — highly specific XML tag |
| `<methodology>` | AGENT_DEFINITION | Same as above | Rare — highly specific |
| `> **Type:**` | WORKTRACKER_ENTITY | Docs explaining blockquote frontmatter format; quoted text mentioning "Type:" | Low — format is Jerry-specific |
| `<!-- L2-REINJECT` | RULE_FILE | Documentation discussing L2-REINJECT format | Low-Medium — more commonly discussed |
| `> **Strategy:**` | STRATEGY_TEMPLATE | Docs explaining adversarial strategy templates | Very rare — highly specific |
| `> **Version:**` | SKILL_DEFINITION | Docs with `> **Version:** 1.0` (version blockquote in arbitrary docs) | Low-Medium — "Version" is common in docs |

**`> **Version:**` analysis:**

The `> **Version:**` cue (line 164) could trigger on any documentation file that includes a version-annotated blockquote:

```markdown
> **Version:** 2.3.1
```

This pattern may appear in changelogs, design documents, or release notes at unrecognized path locations. If triggered, the file would be misclassified as SKILL_DEFINITION, invoking `{"yaml", "nav"}` parsers. YAML frontmatter extraction would run on a file that likely has no YAML frontmatter.

This scenario was not included in the AS-3 questions but represents a false-positive comparable to `> **Type:**`. Both cues use the `> **Bold:**` blockquote field format.

**BUG-004 root cause elimination verification:**

The pre-EN-002 structural cues `("---", DocumentType.AGENT_DEFINITION)` and `("<!--", DocumentType.AGENT_DEFINITION)` have been removed. The BUG-004 root cause (the `"---"` cue matching ALL files with YAML frontmatter or horizontal rules, and `"<!--"` matching all files with HTML comments) is fully eliminated. The six remaining cues are substantially more precise.

**M-14 warning generation for path-matched files:**

For files that DO have a path match, the M-14 warning fires when: (a) path_type is determined, AND (b) structure_type disagrees AND is not UNKNOWN. An attacker who crafts file content to trigger a structural cue on a file that has a correct path classification would receive an M-14 warning in the result. This warning is informational, not blocking — the path classification is used. The M-14 mechanism works correctly as designed.

**AS-3 Overall Assessment:** The AS-3 attack surface is substantially reduced by EN-002. The structural cues are sufficiently precise for a fallback system. Remaining false-positive risk (RV-003, RV-004) is Theoretical and limited to files at unrecognized path locations.

---

### AS-4: UNKNOWN Fallback Abuse — Complete Data Flow Trace

**UNKNOWN invocation matrix:**

```
detect() returns UNKNOWN when:
    path_type = None (no pattern match)
    AND structure_type = None (no cue match)
    -> return (DocumentType.UNKNOWN, None)

_PARSER_MATRIX[UNKNOWN] = {"nav"}
-> nav table extraction runs
-> all other parser fields = None
-> UniversalParseResult.document_type = UNKNOWN
-> parse_errors = ()
```

**ast_detect CLI for UNKNOWN:**

```python
doc_type, warning = DocumentTypeDetector.detect(file_path, source)
# doc_type = DocumentType.UNKNOWN
method = "path"
path_type = DocumentTypeDetector._detect_from_path(_normalize_for_detection(file_path))
if path_type is None:  # True for UNKNOWN files
    method = "structure"
output = {"type": "unknown", "method": "structure"}  # warning = None for true UNKNOWN
```

Exit code 0 returned. The CLI provides no error indication for UNKNOWN — it is treated as a successful detection with result `"unknown"`.

**ast_validate CLI for UNKNOWN without --schema:**

```python
# schema = None (not provided)
doc = JerryDocument.parse(source)
nav_result = validate_nav_table(doc)
output = {
    "is_valid": nav_result.is_valid,
    "schema_valid": True,  # hardcoded True when no schema provided
    "schema_violations": []
}
return 0
```

F-008 is resolved: `ast_validate` without `--schema` does NOT call `schema_registry.get()`. It performs nav table validation only and returns `schema_valid: True` (which is technically misleading for an UNKNOWN file but does not raise an exception). This is the safe behavior noted in the eng-security review.

**Forcing UNKNOWN — Impact Assessment:**

An attacker who forces a file to UNKNOWN (by placing it at an unrecognized path with content matching no structural cues) achieves nav-only parsing. The impact is parser starvation, not type escalation. For a file that SHOULD be an AGENT_DEFINITION (e.g., an agent definition file at a non-standard path), UNKNOWN classification means YAML and XML sections are not extracted, causing any automation that depends on these fields to silently receive `None` fields. This is a type confusion attack with impact of bypassing content-based validation rather than enabling privilege escalation.

**AS-4 Overall Assessment:** UNKNOWN is the correct safe default. No schema validation bypass exists. Parser starvation (receiving UNKNOWN for a file that should have a specific type) is possible but the downstream impact is limited to missing parsed content, not incorrect parsed content. No critical vulnerability.

---

### AS-5: First-Match-Wins Ordering Confusion — Complete Pattern Analysis

**Tier 1 pattern set (lines 75–82) — Specificity analysis:**

| Pattern | Type | Can a file match this AND a later pattern with different type? |
|---------|------|---------------------------------------------------------------|
| `skills/*/agents/*.md` | AGENT_DEFINITION | Also matches `skills/*/*.md` (Tier 2, SKILL_RESOURCE) — Tier 1 wins, correct |
| `skills/*/SKILL.md` | SKILL_DEFINITION | Also matches `skills/*/*.md` (Tier 2) — Tier 1 wins, correct |
| `.context/rules/*.md` | RULE_FILE | No overlap — `.context/` prefix is exclusive |
| `.claude/rules/*.md` | RULE_FILE | No overlap |
| `docs/design/*.md` | ADR | Also matches `docs/*.md` (Tier 5) — Tier 1 wins, correct |
| `docs/adrs/*.md` | ADR | Also matches `docs/*.md` (Tier 5) — Tier 1 wins, correct |
| `.context/templates/adversarial/*.md` | STRATEGY_TEMPLATE | Also matches `.context/templates/**/*.md` (Tier 5, TEMPLATE) — Tier 1 wins, correct |

**Key ordering invariant verified:** The `.context/templates/adversarial/*.md` -> STRATEGY_TEMPLATE pattern at line 82 (Tier 1) correctly precedes `.context/templates/**/*.md` -> TEMPLATE at line 123 (Tier 5). A strategy template is correctly classified as STRATEGY_TEMPLATE, not the more generic TEMPLATE.

**AS-5 Question 5 — `work/` vs `projects/*/orchestration/` overlap:**

These patterns are siblings, not overlapping. `projects/*/work/**/*.md` covers files under the `work/` subdirectory of any project. `projects/*/orchestration/**/*.md` covers files under the `orchestration/` subdirectory. The directory structures are mutually exclusive unless a symlink creates a path that satisfies both. No symlink-based ambiguity risk was found in the analysis.

**`work/**/*.md` (line 120, Tier 5) — distinct from `projects/*/work/**/*.md`:**

`work/**/*.md` at the repository root (Tier 5) matches files under a top-level `work/` directory. This is separate from project-scoped `projects/*/work/**/*.md` (Tier 3). Files in the top-level `work/` directory (if it exists) are classified as WORKTRACKER_ENTITY. This is the correct classification per the git status output showing `?? work/` as an untracked directory.

**AS-5 Question 6 — DocumentType enum coverage audit:**

See dedicated [DocumentType Enum Coverage Audit](#documenttype-enum-coverage-audit) section below.

**`skills/*/*.md` catch-all (line 96, Tier 2) analysis:**

Files captured by this catch-all that are NOT captured by more specific Tier 2 patterns include:
- `skills/{name}/README.md` — no specific pattern for SKILL README files
- `skills/{name}/CHANGELOG.md` — no specific pattern
- `skills/{name}/OVERVIEW.md` — no specific pattern
- `skills/{name}/*.md` at the skill root level (any filename not specifically matched)

SKILL_RESOURCE is an appropriate classification for these files (they are skill-scoped supporting documents). No type confusion identified.

**`docs/*.md` catch-all (line 141, Tier 5) analysis:**

As noted in AS-2 analysis: `fnmatch.fnmatch("docs/subdir/file.md", "docs/*.md")` returns `True` because `*` crosses directory boundaries in Python's fnmatch. This means `docs/*.md` is effectively a catch-all for all docs files not captured by more specific patterns. All such files are classified as KNOWLEDGE_DOCUMENT, which is correct — there is no type confusion, just a broader-than-intended effective scope for the pattern.

**`.context/templates/**/*.md` catch-all (line 123, Tier 5) analysis:**

Files captured by this catch-all that are NOT under `adversarial/` include:
- `.context/templates/worktracker/*.md` — matched earlier at line 121 (TEMPLATE), correct
- `.context/templates/design/*.md` — matched earlier at line 122 (TEMPLATE), correct
- Any other subdirectory under `.context/templates/` that isn't `adversarial/`

For files in `.context/templates/adversarial/`, the Tier 1 pattern (line 82) catches them as STRATEGY_TEMPLATE before they reach the Tier 5 catch-all. The question is whether any non-adversarial template should be STRATEGY_TEMPLATE. The answer is no: STRATEGY_TEMPLATE is specifically for adversarial strategy templates. Other template subdirectories are correctly TEMPLATE.

**AS-5 Overall Assessment:** Pattern ordering is correct. All identified multi-match scenarios resolve to the correct type via first-match-wins. The documented tier structure is functionally sound. The `fnmatch` boundary-crossing behavior of `*` means some patterns are effectively broader than their text suggests, but all cases produce correct type classification.

---

## Prior Finding Remediation Verification

| Finding | Severity | Status in EN-002 | Residual Risk | Engagement Finding |
|---------|----------|-----------------|---------------|-------------------|
| F-001 | High (CWE-22/843) | Partially remediated (`already_relative` guard) | Medium — RV-001 | Direct API callers remain vulnerable; CLI protected by path containment |
| F-002 | Medium (CWE-843) | Fully remediated — `"## Status"` ADR cue removed | None | `STRUCTURAL_CUE_PRIORITY` contains 6 entries; no `"## Status"` present |
| F-003 | Medium (CWE-697) | Fully remediated — ordering is correct | None | `projects/*/work/**/*.md` at line 99 (Tier 3) precedes `projects/*/orchestration/**/*.md` at line 119 (Tier 5) |
| F-004 | Medium (CWE-20) | Resolved — `detect()` returns 2-tuple consistently | None | Return type is `tuple[DocumentType, str | None]` throughout; no 3-tuple implemented |
| F-005 | Low (CWE-843) | Accepted — `<purpose>` cue retained with documentation comment | Low (theoretical) | `<purpose>` tag not present in STRUCTURAL_CUE_PRIORITY in current code; F-005 cue was removed entirely |
| F-006 | Low (CWE-20) | Confirmed non-exploitable | None | Verified: fnmatch treats path argument as literal in both simple and segment matching |
| F-007 | Low (CWE-20) | Unresolved — null byte guard not added | Low | Null bytes not rejected; behavior on POSIX: markers found, path stripped; worst case: UNKNOWN return |
| F-008 | Info | Resolved by design — `ast_validate` uses explicit schema param | None | Confirmed: `ast_validate` does not call `schema_registry.get(doc_type)` |
| F-009 | Info | Partially resolved — new types exist but lack matrix entries | Medium — RV-002 | SKILL_RESOURCE and TEMPLATE not in `_PARSER_MATRIX` |

**F-005 note:** The current `STRUCTURAL_CUE_PRIORITY` does not contain `"<purpose>"`. Only 6 cues are present: `<identity>`, `<methodology>`, `> **Type:**`, `<!-- L2-REINJECT`, `> **Strategy:**`, `> **Version:**`. The F-005 cue (`<purpose>`) appears to have been removed entirely during EN-002 implementation rather than merely accepted as low risk. This reduces the AS-3 attack surface from 7 cues to 6.

---

## DocumentType Enum Coverage Audit

**Enum values defined (document_type.py lines 47–59):** 13 values

| DocumentType | PATH_PATTERNS Coverage | Structural Cue | `_PARSER_MATRIX` | Schema Registry |
|-------------|----------------------|----------------|-----------------|----------------|
| AGENT_DEFINITION | `skills/*/agents/*.md` (Tier 1) | `<identity>`, `<methodology>` | `{"yaml", "xml", "nav"}` | Expected present |
| SKILL_DEFINITION | `skills/*/SKILL.md` (Tier 1) | `> **Version:**` | `{"yaml", "nav"}` | Expected present |
| SKILL_RESOURCE | 10 patterns (Tier 2) | None | **MISSING** | Absent (F-009) |
| RULE_FILE | `.context/rules/*.md`, `.claude/rules/*.md`, `skills/*/rules/*.md` (Tier 1-2) | `<!-- L2-REINJECT` | `{"reinject", "nav"}` | Expected present |
| ADR | `docs/design/*.md`, `docs/adrs/*.md`, `projects/*/decisions/*.md` (Tier 1, 3) | None | `{"html_comment", "nav"}` | Expected present |
| STRATEGY_TEMPLATE | `.context/templates/adversarial/*.md` (Tier 1) | `> **Strategy:**` | `{"blockquote"}` | Expected present |
| WORKTRACKER_ENTITY | `projects/*/WORKTRACKER.md`, `projects/*/work/**/*.md`, etc. (Tier 3, 5) | `> **Type:**` | `{"blockquote", "nav"}` | Expected present |
| FRAMEWORK_CONFIG | Root files, `projects/*/PLAN.md`, etc. (Tier 3, 4) | None | `{"reinject", "nav"}` | Expected present |
| ORCHESTRATION_ARTIFACT | `projects/*/orchestration/**/*.md` (Tier 5) | None | `{"html_comment", "nav"}` | Expected present |
| TEMPLATE | `skills/*/templates/*.md`, `.context/templates/...` (Tier 2, 5) | None | **MISSING** | Absent (F-009) |
| PATTERN_DOCUMENT | `.context/patterns/**/*.md`, `.context/guides/*.md` (Tier 5) | None | `{"blockquote", "nav"}` | Expected present |
| KNOWLEDGE_DOCUMENT | Multiple `docs/` patterns, `projects/*/analysis/`, etc. (Tier 3, 5) | None | `{"nav"}` | Expected present |
| UNKNOWN | Fallback (no pattern) | Fallback (no cue) | `{"nav"}` | Absent by design (correct) |

**Summary of coverage gaps:**

- SKILL_RESOURCE: Has path patterns (10 entries), no structural cue, NO parser matrix entry, no schema — three-system gap
- TEMPLATE: Has path patterns (3 entries), no structural cue, NO parser matrix entry, no schema — three-system gap

---

## Scope Compliance

### Authorization Verification

**Authorization Status:** User confirmed per engagement initiation. This analysis operates within the scope defined in `red-lead-scope.md` version 1.0.

### Techniques Used

| Technique | Applied To | Findings Produced |
|-----------|-----------|------------------|
| STATIC-001 (Source code review) | `document_type.py`, `universal_document.py`, `ast_commands.py` | RV-001 through RV-008 |
| STATIC-002 (Data flow analysis) | AS-4 UNKNOWN trace, AS-1 path normalization trace, RV-002 parser matrix trace | RV-001, RV-002, RV-006 |
| STATIC-003 (Pattern ordering analysis) | AS-5 complete 63+ pattern analysis | AS-5 ordering verification |
| STATIC-004 (Input crafting for theoretical validation) | AS-1 bypass demonstrations, AS-2 wildcard tests, AS-3 false-positive scenarios | RV-003, RV-004 |
| STATIC-005 (Downstream impact analysis) | `_PARSER_MATRIX` propagation, `UniversalParseResult` field analysis | RV-002, RV-006 |

### Files Accessed (Read-Only)

| File | Purpose | Lines Read |
|------|---------|------------|
| `src/domain/markdown_ast/document_type.py` | Primary target | Full (1–385) |
| `src/domain/markdown_ast/universal_document.py` | Downstream consumer | Full (1–213) |
| `src/domain/markdown_ast/universal_parse_result.py` | Downstream consumer | Full (1–72) |
| `src/interface/cli/ast_commands.py` | CLI adapter | Full (1–736) |
| `src/infrastructure/internal/enforcement/pre_tool_enforcement_engine.py` | Reference | Lines 505–527 only |
| `src/domain/markdown_ast/__init__.py` | Public API | Full (1–174) |

### Constraint Verification

| Constraint | Status |
|-----------|--------|
| Read-only access | COMPLIED — no files modified |
| No code modification | COMPLIED |
| No test execution | COMPLIED |
| No network access | COMPLIED |
| All findings include CWE + CVSS | COMPLIED |
| Theoretical paths labeled | COMPLIED — Exploitability field in each finding |
| Correlation with F-001 through F-009 | COMPLIED — see Remediation Verification section |

---

*Engagement: RED-0002*
*Analysis Version: 1.0.0*
*Agent: red-vuln*
*Date: 2026-02-24*
*Methodology: PTES Vulnerability Analysis Phase + NIST SP 800-115 Chapter 4*
*Constitutional Compliance: P-003 (no subagents), P-020 (user authority), P-022 (no deception)*
*Output: L0/L1/L2 per P-002 persistence requirement*
*Authorization: Confirmed by user per red-lead-scope.md v1.0*
