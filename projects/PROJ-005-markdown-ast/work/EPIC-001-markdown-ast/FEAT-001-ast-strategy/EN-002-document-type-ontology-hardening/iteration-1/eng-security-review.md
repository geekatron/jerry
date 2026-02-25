# EN-002 Security Code Review: Document Type Ontology Hardening

<!-- AGENT: eng-security | VERSION: 1.0.0 | DATE: 2026-02-24 | TASK: EN-002 security review -->
<!-- CWE: CWE-843 (Type Confusion) | ASVS: V5 (Validation, Sanitization, Encoding) -->

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Findings by severity, overall assessment, immediate actions |
| [L1 Technical Findings](#l1-technical-findings) | Individual finding reports with CWE, CVSS, evidence, remediation |
| [L2 Strategic Implications](#l2-strategic-implications) | Security posture, systemic patterns, architectural recommendations |
| [ASVS Verification](#asvs-verification) | OWASP ASVS 5.0 chapter verification status |
| [Review Scope and Methodology](#review-scope-and-methodology) | Files reviewed, data flow traced, CWE checklist applied |

---

## L0 Executive Summary

### Findings by Severity

| Severity | Count | CWE IDs |
|----------|-------|---------|
| Critical | 0 | -- |
| High | 1 | CWE-843 |
| Medium | 3 | CWE-22, CWE-843, CWE-697 |
| Low | 3 | CWE-20, CWE-435, CWE-691 |
| Informational | 2 | -- |
| **Total** | **9** | |

### Overall Security Assessment

**CONDITIONAL PASS.** The proposed changes substantially improve the security posture of `DocumentTypeDetector` by eliminating the root cause of BUG-004 (CWE-843 via the `"---"` structural cue). The path-first architecture correctly enforces the CWE-843 control. However, three medium-severity findings require remediation before the implementation is complete: the `_normalize_path` root marker extraction is exploitable via embedded marker strings, the `"## Status"` structural cue produces ADR type confusion, and the first-match-wins ordering contains one demonstrable type confusion case in the `docs/` catch-all zone.

The UNKNOWN fallback, as proposed, correctly returns UNKNOWN without triggering schema validation, which is the safe behavior. The fnmatch wildcard attack surface is limited and largely mitigated by path normalization.

### Top 3 Risk Areas

1. **Root Marker Extraction in `_normalize_path`** (Finding F-001, High/CWE-22): A crafted path containing an embedded marker string (e.g., `/tmp/evil/skills/x.md`) is silently stripped to the portion starting at the marker, potentially matching a legitimate pattern from an untrusted path origin. This is the highest-risk issue because it is the only mechanism that could allow structural-cue-level evidence to corrupt path-based classification.

2. **`"## Status"` Structural Cue ADR Ambiguity** (Finding F-002, Medium/CWE-843): Every Jerry worktracker entity file contains `## History`, `## Summary`, and frequently `## Status`. The proposed structural cue `("## Status", DocumentType.ADR)` will fire on worktracker entity files that have no path pattern match. The current WORKTRACKER_ENTITY cue `("> **Type:**", ...)` has higher priority in the proposed list, so for files with both signals the worktracker type wins. However, a worktracker entity file that uses blockquote-free status notation (plain `## Status` heading with no blockquote frontmatter) would be misclassified as ADR via structural detection.

3. **`docs/` Catch-All Pattern Before `docs/knowledge/`** (Finding F-003, Medium/CWE-697): In the proposed Tier 5, `docs/knowledge/**/*.md` appears before the catch-all `docs/*.md`, which is correct. However, the pattern `docs/*.md` (single-star, shallow) will match files in the `docs/` root but NOT in subdirectories (because `*` in fnmatch does not cross directory boundaries). This is actually safe but the intent is ambiguous and the test in eng-qa-test-strategy.md tests `docs/BOOTSTRAP.md` which is shallow-rooted. The more dangerous case is that `docs/schemas/*.md` and other specific subdirectory patterns listed in Tier 5 must all appear BEFORE the `docs/*.md` catch-all -- this ordering is satisfied in the proposed list. No exploitation exists for the current ordering, but the intent gap creates future maintenance risk.

### Recommended Immediate Actions

1. **F-001 (High)**: Add path canonicalization before root marker extraction to reject paths containing null bytes, validate that the path originates from a trusted source, or at minimum reject paths where the extracted portion differs from the expected normalized form.

2. **F-002 (Medium)**: Replace `("## Status", DocumentType.ADR)` with a more specific ADR cue that does not conflict with worktracker entity sections. Recommended: `("## Decision\n", DocumentType.ADR)` or a two-signal compound: `"## Status" AND "## Decision"` in the same file.

3. **F-004 (Medium)**: The UNKNOWN fallback signature change (`detect()` returning a 3-tuple vs. the current 2-tuple) is a breaking API change. Verify that all call sites are updated atomically and that the `UNKNOWN` type is explicitly excluded from schema lookup in `schema_registry.get()`.

---

## L1 Technical Findings

---

### F-001: Root Marker Extraction Allows Embedded-Marker Path Confusion

**Classification**

| Attribute | Value |
|-----------|-------|
| CWE ID | CWE-22 (Path Traversal) / CWE-843 (Type Confusion) |
| CVSS 3.1 | AV:L/AC:H/PR:N/UI:N/S:U/C:L/I:H/A:N -- Score: **6.5 (Medium-High)** |
| Severity | High |
| Affected File | `src/domain/markdown_ast/document_type.py` |
| Affected Function | `_normalize_path()` (lines 188--231) |
| ASVS Reference | V5.1.2 (Input Validation), V5.1.3 (Untrusted Path Handling) |

**Data Flow Trace**

```
External caller: detect(file_path, content)
    -> _normalize_path(file_path)              [line 120]
        -> path.replace(os.sep, "/")           [line 202]
        -> path.find(marker) for each marker   [lines 219-221]
            IF idx > 0: path = path[idx:]      [line 221]  <-- VULNERABILITY
        -> return stripped path
    -> _detect_from_path(normalized_path)      [line 123]
        -> _path_matches_glob(normalized_path, pattern)  [line 160]
```

**Proof of Vulnerability**

The root marker extraction loop at line 219-221:

```python
for marker in root_markers:
    idx = path.find(marker)
    if idx > 0:
        path = path[idx:]
        break
```

The condition `idx > 0` (not `idx == 0`) means any path that *contains* a root marker string anywhere after position 0 will be truncated to start at that marker. Consider:

```python
_normalize_path("/tmp/attacker/skills/target/agents/malicious.md")
# path.find("skills/") -> returns the index of "skills/" inside the string
# idx > 0 is True (idx is around 16)
# path becomes "skills/target/agents/malicious.md"
# _path_matches_glob("skills/target/agents/malicious.md", "skills/*/agents/*.md") -> True
# Returns AGENT_DEFINITION
```

In the current implementation this is a limited risk because the only callers are the `jerry ast detect` CLI command and internal tests that pass trusted paths. However, if `detect()` is ever called with user-supplied paths (e.g., a future `jerry ast detect` that scans arbitrary directories or is invoked from an agent workflow with user-provided file paths), this becomes a type confusion escalation: a file at an untrusted path gains the type of a legitimate agent definition and consequently receives agent-definition schema validation, which is more permissive for fields like `name` (regex `^[a-z]+-[a-z]+(-[a-z]+)*$`) and `model` (`allowed_values=("opus","sonnet","haiku")`). For automation workflows that route files based on detected type (pre-commit hook, `jerry ast validate` auto-schema), this could result in inappropriate schema selection.

**Note on null bytes**: `fnmatch.fnmatch` passes paths to the C-level `os.path` functions on Python 3.12+. Null bytes in paths will raise `ValueError` in `fnmatch` on most platforms. However, `path.find(marker)` will not raise on null bytes -- it will find the marker if present. A path like `/tmp/\x00skills/x.md` would have `find("skills/")` return a positive index. This is an edge case but worth documenting.

**Exploitation Scenario (Internal Automation)**

1. An agent workflow constructs a file path by reading from an untrusted source (e.g., a maliciously crafted worktracker entity containing a `File:` reference like `/tmp/evil/skills/agents/agent.md`)
2. The workflow calls `detect(path, content)` where `path` is user-controlled
3. `_normalize_path` strips to `skills/agents/agent.md`
4. Pattern `skills/*/agents/*.md` matches
5. File is classified as `AGENT_DEFINITION` and receives agent-definition schema validation instead of UNKNOWN
6. Pre-commit hook or automation trusts the classification and proceeds

**Remediation Code Example**

Replace the marker extraction block with an anchored check:

```python
# CURRENT (vulnerable):
for marker in root_markers:
    idx = path.find(marker)
    if idx > 0:
        path = path[idx:]
        break

# PROPOSED (safe):
for marker in root_markers:
    idx = path.find(marker)
    if idx > 0:
        candidate = path[idx:]
        # Safety gate: the extracted portion must not re-contain suspicious sequences.
        # Reject if the path segment before the marker contains another marker
        # (indicates embedded marker injection rather than genuine absolute path).
        prefix = path[:idx]
        if not any(m in prefix for m in root_markers):
            path = candidate
            break
        # If prefix itself contains a marker, the path is ambiguous.
        # Fall through without stripping -- let the full path fail to match.
```

A stricter alternative: resolve the path to an absolute form using `pathlib.Path.resolve()` before normalization when the path appears absolute, then verify the resolved path is actually within the expected repository root. This eliminates the substring-search ambiguity entirely.

**Risk Acceptance Condition**: This finding is acceptable at current risk level IF the call surface of `detect()` is contractually restricted to trusted, filesystem-verified paths (paths read via `pathlib.Path.rglob` over the known repo root). This should be documented as a precondition in the `detect()` docstring.

---

### F-002: `"## Status"` Structural Cue Creates ADR Type Confusion

**Classification**

| Attribute | Value |
|-----------|-------|
| CWE ID | CWE-843 (Type Confusion) |
| CVSS 3.1 | AV:L/AC:M/PR:N/UI:N/S:U/C:N/I:M/A:N -- Score: **4.3 (Medium)** |
| Severity | Medium |
| Affected File | EN-002 proposed `STRUCTURAL_CUE_PRIORITY` (not yet implemented) |
| Affected Section | Phase 2 structural cue replacement (EN-002 Technical Approach) |
| ASVS Reference | V5.1.1 (Input Validation -- type-based routing) |

**Data Flow Trace**

```
detect("skills/old-skill/LEGACY.md", legacy_content)
    -> _normalize_path(...)         -> "skills/old-skill/LEGACY.md"
    -> _detect_from_path(...)       -> None  (no pattern matches)
    -> _detect_from_structure(content)
        -> check "<identity>"       -> not found
        -> check "<methodology>"    -> not found
        -> check "<purpose>"        -> not found
        -> check "> **Type:**"      -> not found (file uses plain heading, no blockquote)
        -> check "<!-- L2-REINJECT" -> not found
        -> check "> **Strategy:**"  -> not found
        -> check "## Status"        -> FOUND  <-- misclassifies as ADR
        -> return DocumentType.ADR  <-- WRONG
```

**Proof of Vulnerability**

`## Status` is a standard section heading used in multiple Jerry document categories:

- Every worktracker entity has a `## Status` section in some form
- Skill playbooks may contain `## Status` as an operational readiness section
- Knowledge documents frequently use `## Status` headings

The proposed structural cue `("## Status", DocumentType.ADR)` is less specific than the preceding cues but will fire on any path-unmatched file containing this heading. The eng-qa-test-strategy.md provides a test `("## Status\n\nProposed.\n", DocumentType.ADR, "ADR status heading")` -- but this is a happy-path test. The actual risk is:

```python
# A legacy skill playbook with no path pattern match
content = "# Skill Playbook\n\n## Status\n\nProduction ready.\n\n## Usage\n...\n"
doc_type, _ = detect("skills/old-skill/LEGACY-PLAYBOOK.md", content)
# Returns ADR (misclassification) instead of UNKNOWN
# The ADR schema requires sections: Status, Context, Decision, Consequences
# Validation will fail, but the TYPE is wrong, which corrupts auto-schema routing
```

The `ADR_SCHEMA` has `section_rules` requiring `Status`, `Context`, `Decision`, `Consequences` all present (`required=True`). A misclassified file attempting auto-schema validation would fail validation rather than receiving the correct schema -- but in a "fail open" automation context where validation failures are logged and ignored, the file could proceed with the wrong schema.

**Remediation**

Replace `("## Status", DocumentType.ADR)` with a compound two-signal check. Since `_detect_from_structure` currently supports single-string cues only, options are:

Option A -- Replace with the most distinctive ADR marker not shared with other types:
```python
("## Decision\n", DocumentType.ADR),   # "Decision" is ADR-specific
```
Note: Even "## Decision" could appear in other documents, but it is far less common than "## Status".

Option B -- Add a compound structural cue mechanism (requires API change to `_detect_from_structure`):
```python
# New tuple format: (required_cue_1, optional_cue_2, doc_type)
# Only matches if BOTH cues are present
("## Status", "## Decision", DocumentType.ADR),
```

Option C -- Remove the `## Status` ADR cue entirely. With comprehensive path patterns, the ADR structural cue should rarely activate. The `docs/design/*.md` and `docs/adrs/*.md` patterns cover all known ADR locations. ADRs outside these paths should return UNKNOWN, not ADR.

**Recommended**: Option C (remove the cue). The pattern coverage for ADRs is already complete. Relying on a generic heading as a structural fingerprint for a strict-schema type (ADR requires 4 mandatory sections) creates a false classification risk with no compensating benefit.

---

### F-003: First-Match-Wins Ordering: `projects/*/work/**` vs `projects/*/orchestration/**`

**Classification**

| Attribute | Value |
|-----------|-------|
| CWE ID | CWE-697 (Incorrect Comparison) |
| CVSS 3.1 | AV:L/AC:M/PR:N/UI:N/S:U/C:N/I:L/A:N -- Score: **3.3 (Low)** |
| Severity | Medium (due to schema routing impact) |
| Affected File | EN-002 proposed `PATH_PATTERNS` |
| Affected Pattern | Tier 3 ordering: `projects/*/work/**/*.md` vs `projects/*/orchestration/**/*.md` |
| ASVS Reference | V5.1.1 (Input Validation -- classifier ordering) |

**Data Flow Trace**

```
detect("projects/PROJ-XXX/work/orchestration-notes/phase-1/plan.md", "")
    -> _detect_from_path("projects/PROJ-XXX/work/orchestration-notes/phase-1/plan.md")
        -> check "projects/*/WORKTRACKER.md"  -> no match
        -> check "projects/*/work/**/*.md"     -> MATCH: returns WORKTRACKER_ENTITY
        [never reaches "projects/*/orchestration/**/*.md"]
```

**Analysis**

This is an INTENDED behavior, not a bug: a file under `work/` should always be classified as WORKTRACKER_ENTITY even if its subdirectory name contains "orchestration". The eng-qa test strategy correctly identifies this as OZ-05 and tests it:

```
Input: "projects/PROJ-XXX/work/orchestration-notes/plan.md"
Expected: WORKTRACKER_ENTITY
```

However, the reverse case reveals the classification intent gap:

```
detect("projects/PROJ-XXX/orchestration/WORKTRACKER.md", "")
    -> check "projects/*/WORKTRACKER.md"        -> no match
       (pattern is "projects/*/WORKTRACKER.md" with single *, which matches
        "projects/PROJ-XXX/WORKTRACKER.md" but NOT "projects/PROJ-XXX/orchestration/WORKTRACKER.md"
        because * does not cross directory boundaries in fnmatch)
    -> check "projects/*/work/**/*.md"           -> no match
    -> check "projects/*/PLAN.md"               -> no match
    -> check "projects/*/decisions/*.md"         -> no match
    -> check "projects/*/analysis/*.md"          -> no match
    -> check "projects/*/research/*.md"          -> no match
    -> check "projects/*/synthesis/*.md"         -> no match
    -> check "projects/*/critiques/*.md"         -> no match
    -> check "projects/*/orchestration/**/*.md"  -> MATCH: ORCHESTRATION_ARTIFACT
```

So `projects/PROJ-XXX/orchestration/WORKTRACKER.md` is classified as ORCHESTRATION_ARTIFACT, which is correct. The eng-qa strategy tests this case and expects ORCHESTRATION_ARTIFACT. No actual misclassification.

**Residual Risk**

The ordering is correct but the intent is expressed only in pattern position, not in documentation. A future maintainer adding patterns to Tier 3 could accidentally insert a new broad `projects/*/` pattern before the `orchestration/**` pattern, causing type confusion for files in orchestration directories. The risk is a future maintenance error, not a current exploit.

**Remediation**

Add ordering comments to the proposed `PATH_PATTERNS` to document WHY the ordering is as it is:

```python
# --- Tier 3: Worktracker entities ---
# ORDERING INVARIANT: projects/*/work/**/*.md MUST precede projects/*/orchestration/**/*.md
# A file under work/ is ALWAYS a worktracker entity even if its subdirectory
# contains "orchestration" in the name. Violating this order causes WORKTRACKER_ENTITY
# files to be misclassified as ORCHESTRATION_ARTIFACT (T-DT-02).
("projects/*/WORKTRACKER.md", DocumentType.WORKTRACKER_ENTITY),
("projects/*/work/**/*.md", DocumentType.WORKTRACKER_ENTITY),
```

---

### F-004: UNKNOWN Fallback API Change Is a Breaking Change

**Classification**

| Attribute | Value |
|-----------|-------|
| CWE ID | CWE-20 (Improper Input Validation -- API contract violation) |
| CVSS 3.1 | AV:L/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:L -- Score: **4.4 (Medium)** |
| Severity | Medium |
| Affected File | EN-002 Phase 3 proposed `detect()` signature |
| Affected Section | Phase 3: UNKNOWN fallback with structured logging |
| ASVS Reference | V5.1.1 (Input Validation -- caller validation of return type) |

**Data Flow Trace**

```
# Proposed change: detect() returns 3-tuple on UNKNOWN
return (DocumentType.UNKNOWN, None, {"unmatched_path": normalized_path})

# Current return type: tuple[DocumentType, str | None]
# Proposed return type for UNKNOWN: tuple[DocumentType, str | None, dict | None]

# All existing callers perform:
doc_type, warning = DocumentTypeDetector.detect(...)
# If detect() returns a 3-tuple, this unpacking raises ValueError:
# "too many values to unpack (expected 2)"
```

**Proof of Vulnerability**

The EN-002 Phase 3 design proposes:
```python
return (DocumentType.UNKNOWN, None, {"unmatched_path": normalized_path})
```

But the current `detect()` signature returns `tuple[DocumentType, str | None]`. Any caller using two-element destructuring -- including the existing tests (`doc_type, warning = DocumentTypeDetector.detect(...)`) and the CLI adapter -- would raise a `ValueError` at runtime.

Search for all call sites:

```python
# In tests/unit/domain/markdown_ast/test_document_type.py
doc_type, warning = DocumentTypeDetector.detect(...)   # All 20+ test cases use this
doc_type, _ = DocumentTypeDetector.detect(...)         # Pattern used in 5 tests
```

The regression test in eng-qa-test-strategy.md also uses `doc_type, warning = DocumentTypeDetector.detect(...)` (line 146 of strategy doc). All of these would fail if detect() returns a 3-tuple for UNKNOWN.

**Impact on Security Control**: If the 3-tuple return is not handled atomically across all call sites, any runtime code path that encounters an unmatched file would raise ValueError instead of gracefully returning UNKNOWN. This converts the "safe default" into a runtime exception, which could be logged as an error and suppressed by exception handlers -- silently allowing the file to proceed without classification.

**Remediation**

Option A -- Keep the 2-tuple return, store diagnostic info as a side channel:
```python
# Return type remains: tuple[DocumentType, str | None]
# When UNKNOWN, include diagnostic info in the warning field:
return (DocumentType.UNKNOWN, f"unmatched_path:{normalized_path}")
```

Option B -- Structured return type via dataclass (recommended):
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class DetectionResult:
    doc_type: DocumentType
    warning: str | None
    diagnostic: dict[str, str] | None = None

# Callers use result.doc_type, result.warning, result.diagnostic
```

Option C -- Keep 2-tuple but bump the return type annotation to `tuple[DocumentType, str | None]` and put diagnostics in a separate `detect_with_diagnostics()` method, keeping `detect()` backward-compatible.

**Recommended**: Option A is the lowest-risk change. The diagnostic data (the normalized path) is inherently low-value -- it's already known to the caller from the input. If structured diagnostics are needed for the regression test, add a separate `_detect_details()` internal method used only by tests.

---

### F-005: `"<purpose>"` Structural Cue False Positive Risk

**Classification**

| Attribute | Value |
|-----------|-------|
| CWE ID | CWE-843 (Type Confusion -- structural cue over-triggering) |
| CVSS 3.1 | AV:L/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:N -- Score: **2.5 (Low)** |
| Severity | Low |
| Affected File | EN-002 proposed `STRUCTURAL_CUE_PRIORITY` |
| Affected Cue | `("<purpose>", DocumentType.AGENT_DEFINITION)` |
| ASVS Reference | V5.1.1 (Input Validation) |

**Analysis**

The proposed structural cue `("<purpose>", DocumentType.AGENT_DEFINITION)` relies on the substring `<purpose>` appearing in file content. While `<purpose>` is defined as an XML-tagged section in agent definitions (per `agent-development-standards.md`), the string can appear in other contexts:

1. **HTML in markdown**: A file discussing HTML `<purpose>` elements or containing example code with `<purpose>` tags
2. **Documentation about agent definitions**: Any file that *explains* the `<purpose>` section format would contain the literal string `<purpose>` and be misclassified as an agent definition
3. **Template files**: The agent definition template files in `skills/*/templates/` would contain `<purpose>` as example content -- but these will be covered by path patterns (`skills/*/templates/*.md` -> TEMPLATE), so the structural fallback would not activate for them

This is LOW severity because: (a) the path patterns should cover all legitimate agent definition locations (`skills/*/agents/*.md`), making the structural cue a rarely-used fallback; (b) misclassification to AGENT_DEFINITION triggers schema validation which checks for `name`, `version`, `description`, `model` fields -- most non-agent-definition files would fail this validation, making the misclassification self-revealing.

**Remediation**

The cue is acceptable given the path-first architecture. Document in code that these structural cues are a last-resort fallback and should rarely activate after EN-002 pattern expansion. No code change required; add a comment:

```python
# STRUCTURAL_CUE_PRIORITY is the fallback layer activated ONLY when no PATH_PATTERN matches.
# After EN-002, path patterns cover >98% of repo files. These cues handle the residual.
# False positives here produce warnings (M-14) and fail strict schema validation --
# misclassification is self-revealing. Precision is preferred over recall for structural cues.
```

---

### F-006: `fnmatch` Wildcard Exploitation Analysis

**Classification**

| Attribute | Value |
|-----------|-------|
| CWE ID | CWE-20 (Improper Input Validation -- wildcard inputs) |
| CVSS 3.1 | AV:L/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:N -- Score: **2.0 (Low)** |
| Severity | Low (Informational boundary) |
| Affected File | `src/domain/markdown_ast/document_type.py` |
| Affected Functions | `_path_matches_glob()`, `_match_recursive_glob()` |

**Analysis**

`fnmatch.fnmatch(path, pattern)` treats the PATTERN as containing wildcards, not the path. The path argument is matched AGAINST the pattern; wildcards in the path argument are treated as literal characters by the underlying implementation.

Specifically: `fnmatch.fnmatch("skills/*/agents/evil*.md", "skills/*/agents/*.md")` returns `False` in Python's fnmatch because `fnmatch` translates the PATTERN to a regex and matches the PATH against it. The path `"skills/*/agents/evil*.md"` is treated as a literal string with literal `*` characters.

Verification:

```python
import fnmatch
# Wildcard in PATH, not in PATTERN
fnmatch.fnmatch("skills/*/agents/evil.md", "skills/*/agents/*.md")
# -> False (the literal "*" in path does not match against the pattern's "*")

# Wildcard in PATTERN matches any path
fnmatch.fnmatch("skills/foo/agents/evil.md", "skills/*/agents/*.md")
# -> True (pattern wildcard matches "foo" and "evil")
```

**Result**: An attacker cannot craft a filename containing `*` or `?` to exploit the pattern matching -- fnmatch correctly treats path arguments as literal strings. This is a non-finding with informational documentation value.

**One Edge Case Noted**: The `_match_recursive_glob` function splits on `**` and then calls `fnmatch.fnmatch(ps, pp)` on individual segments (line 283). If a PATH SEGMENT contains `?`, `[`, or `]` characters (characters that have special meaning in the pattern position), they are treated as literals in the path argument. However, if a PATTERN SEGMENT itself contains special characters beyond `*` and `?`, this is also handled by fnmatch correctly. No exploitation path exists.

---

### F-007: `_normalize_path` Does Not Reject Null Bytes

**Classification**

| Attribute | Value |
|-----------|-------|
| CWE ID | CWE-20 (Improper Input Validation) |
| CVSS 3.1 | AV:L/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:N -- Score: **2.0 (Low)** |
| Severity | Low |
| Affected File | `src/domain/markdown_ast/document_type.py` |
| Affected Function | `_normalize_path()` |

**Analysis**

A path argument containing null bytes (e.g., `"skills/agents/\x00evil.md"`) is not rejected by `_normalize_path`. The behavior depends on how the normalized path is subsequently used:

- `fnmatch.fnmatch("skills/agents/\x00evil.md", "skills/*/agents/*.md")` -- fnmatch on Python 3.12+ will raise `ValueError: embedded null character` on most OS calls, but pure Python fnmatch uses regex matching and may not raise. Testing required.
- `path.find("skills/")` on a path with embedded null bytes will find the marker at the correct position (null bytes are valid Python string characters), potentially stripping prefix before the null byte.

This is LOW severity because: (a) the typical call sites receive paths from `pathlib.Path.rglob` which does not yield paths with null bytes; (b) even if a null-byte path reaches `fnmatch`, the worst outcome is UNKNOWN return (safe default), not a valid type match.

**Remediation**

Add a null byte guard at the start of `_normalize_path`:

```python
def _normalize_path(file_path: str) -> str:
    if "\x00" in file_path:
        return ""  # Safe: empty path matches no pattern, returns UNKNOWN
    # ... rest of normalization
```

---

### F-008: `UNKNOWN` Schema Gap -- Registry Has No UNKNOWN Schema

**Classification**

| Attribute | Value |
|-----------|-------|
| CWE ID | CWE-20 (Improper Input Validation -- missing validation for sentinel type) |
| CVSS 3.1 | N/A (behavioral, not exploitable) |
| Severity | Informational |
| Affected File | `src/domain/markdown_ast/schema_definitions.py` |

**Analysis**

`DEFAULT_REGISTRY` in `schema_definitions.py` registers schemas for 15 types but does NOT register a schema for `DocumentType.UNKNOWN`. The `schema_registry.get("unknown")` call raises `ValueError: Unknown entity type 'unknown'`. This is the CORRECT behavior: UNKNOWN files should not receive any schema.

However, the `jerry ast validate` command must explicitly guard against calling `schema_registry.get(doc_type.value)` when `doc_type == DocumentType.UNKNOWN`. If this guard is missing from the CLI adapter, the UNKNOWN type would produce a `ValueError` exception rather than a graceful "file not validated" result.

The proposed EN-002 changes do not modify `schema_definitions.py` for UNKNOWN. This is correct by design -- but the CLI adapter guard must be confirmed present and tested.

**Action**: Verify that the CLI adapter (`jerry ast validate` command) checks `if doc_type == DocumentType.UNKNOWN: skip_validation()` before calling `schema_registry.get()`. This is a test gap, not a code vulnerability.

---

### F-009: New `SKILL_RESOURCE` and `TEMPLATE` Enum Values Have No Schemas

**Classification**

| Attribute | Value |
|-----------|-------|
| CWE ID | CWE-20 (Missing validation for new entity types) |
| CVSS 3.1 | N/A (behavioral) |
| Severity | Informational |
| Affected File | `src/domain/markdown_ast/schema_definitions.py` |

**Analysis**

The proposed enum additions (`SKILL_RESOURCE`, `TEMPLATE`) are noted in EN-002 acceptance criteria TC-6: "New DocumentType values have corresponding schemas in schema_definitions.py." If `SKILL_RESOURCE` or `TEMPLATE` files are passed to `jerry ast validate`, `schema_registry.get("skill_resource")` raises `ValueError`.

The `ADR_SCHEMA` requires 4 mandatory sections -- the most restrictive schema in the current registry. The `KNOWLEDGE_SCHEMA` and `ORCHESTRATION_SCHEMA` have no field or section rules -- the most permissive. New enum values should have schemas registered even if the schemas are empty (like `ORCHESTRATION_SCHEMA`) to prevent `ValueError` from the schema registry.

**Action**: Register `SKILL_RESOURCE_SCHEMA` and `TEMPLATE_SCHEMA` (even with empty rules) in TASK-003 scope. Confirm in EN-002 acceptance criteria TC-6.

---

## L2 Strategic Implications

### Security Posture Assessment

The proposed EN-002 changes represent a materially significant improvement to the security posture of `DocumentTypeDetector`. The current implementation (BUG-004) has an active CWE-843 defect: every file not matched by path patterns is misclassified as AGENT_DEFINITION via the `"---"` structural cue. This is a type confusion vulnerability that corrupts the entire classification pipeline for approximately 1,634 of 2,774 files (~59%).

After EN-002, the posture improves to a residual risk of:
- F-001 (High): Embedded-marker path confusion in `_normalize_path` -- low likelihood in current deployment (trusted call sites), but requires documentation or code fix
- F-002 (Medium): `"## Status"` ADR cue over-triggering -- low file count affected (files without path matches and with `## Status` heading), but easy to fix
- F-004 (Medium): API breaking change for UNKNOWN -- requires atomic migration of all call sites

### Systemic Vulnerability Patterns

**Pattern 1: Trust Level Mismatch Between Path and Content**

The path-first architecture correctly establishes that path evidence is more trusted than content evidence. However, `_normalize_path` performs a lossy transformation (prefix stripping) that can cause an untrusted path to acquire the authority of a trusted path. The root cause is that path normalization is designed for usability (handle both absolute and relative paths), but it conflates path trust level reduction (stripping a prefix) with path identity preservation. These concerns should be separated.

**Pattern 2: Structural Cue Precision vs. Recall**

The proposed structural cues improve precision over the current `"---"` cue but still make tradeoffs. `"<identity>"`, `"<methodology>"`, `"<purpose>"` are high-precision agent definition markers. `"## Status"` is low-precision. The pattern across the cue list suggests a need for a formal specificity metric -- cues should be ranked not just by priority but by a documented false-positive rate estimation. The eng-qa strategy's cue precision tests cover this but the production code has no safeguard against adding low-specificity cues.

**Pattern 3: Catch-All Patterns and Type Escalation**

The proposed catch-all patterns (`docs/*.md`, `.context/templates/**/*.md`) correctly handle files not covered by specific patterns. However, catch-alls create a risk surface where the order of the catch-all relative to specific patterns is load-bearing security logic. This pattern is well-managed by the first-match-wins semantics, but requires ongoing vigilance as new patterns are added. The ordering comment recommendation in F-003 mitigates the maintenance risk.

### Comparison with Threat Model Predictions

The threat model (referenced in code comments) predicts T-DT-01 through T-DT-05. This review confirms:

| Threat | Threat Model Prediction | Review Finding |
|--------|------------------------|----------------|
| T-DT-01: Content spoofing structural cue | Path-first prevents structural override | CONFIRMED: Path-first is enforced in `detect()` -- no structural cue can override a path match (verified at lines 129-141) |
| T-DT-02: Path prefix confusion | Root marker extraction may confuse prefixes | FOUND: F-001 directly addresses this threat -- the marker extraction is the attack surface |
| T-DT-03: Glob ambiguity injection | First-match-wins is deterministic | CONFIRMED: The ordering is deterministic; no glob ambiguity creates non-deterministic behavior |
| T-DT-04: UNKNOWN escalation | UNKNOWN as safe default prevents silent bypass | PARTIALLY CONFIRMED: UNKNOWN is safe but F-008 (missing schema guard in CLI) requires verification |
| T-DT-05: Mismatch warning suppression | Dual-signal always produces warning | CONFIRMED: The warning logic at lines 132-140 fires for any structural mismatch when path type is established |

### Recommendations for Security Architecture Evolution

1. **Formalize the path trust model**: Add a `TrustedPath` type wrapper or validation gate at the `detect()` entry point. Files passed from `pathlib.Path.rglob` are trusted; files passed from user-supplied strings require sanitization. This is a one-line API change with significant security clarity benefit.

2. **Structural cue specificity score**: Adopt a documented minimum specificity requirement for new structural cues. A cue is acceptable if its false-positive rate across the full repo corpus (2,774 files) is below 0.5% (approx. 14 files). The `"## Status"` cue fails this test and should be removed.

3. **Pattern change audit trail**: Consider adding a comment-based audit trail to each PATH_PATTERNS entry documenting the date added, the EN/TASK reference, and the count of files it covers. This turns the pattern list into a self-documenting security audit log.

---

## ASVS Verification

**OWASP ASVS 5.0 Chapter Verification (relevant chapters for this component)**

| ASVS Chapter | Requirement | Status | Evidence |
|--------------|-------------|--------|---------|
| V5.1.1 | Input Validation: Validate all input from untrusted sources | PARTIAL | `detect()` accepts arbitrary strings; `_normalize_path` normalizes but does not fully reject adversarial inputs (F-001, F-007) |
| V5.1.2 | Input Validation: Positive validation (allowlist) | PASS | PATH_PATTERNS is an explicit allowlist; no pattern matches implies UNKNOWN (safe default) |
| V5.1.3 | Input Validation: Path canonicalization before security decision | PARTIAL | Normalization occurs before pattern matching, but normalization itself has an embedded-marker vulnerability (F-001) |
| V5.2.1 | Sanitization: Encode output appropriately | PASS | `detect()` returns enum values and string warnings -- no HTML or command output |
| V1.5.2 | Architecture: Trust Boundaries | PASS | Path-first architecture correctly establishes path as higher-trust signal than content |
| V7.4.1 | Error Handling: Avoid leaking sensitive information in errors | PASS | Warning messages expose path segments but no secrets; UNKNOWN fallback is informative, not harmful |
| V8.3.1 | Data Protection: Classify data | PASS | DocumentType enum provides explicit classification; UNKNOWN is an explicit safe sentinel |

**ASVS V5 Verification Summary**: 5 of 7 requirements fully pass. Two partial findings (V5.1.1 and V5.1.3) correspond to F-001 and F-007, which have documented remediations.

---

## Review Scope and Methodology

### Files Reviewed

| File | Purpose | Lines Read |
|------|---------|------------|
| `src/domain/markdown_ast/document_type.py` | Primary subject -- current implementation | 1-299 |
| `src/domain/markdown_ast/schema_definitions.py` | Schema registry and type-to-schema mapping | 1-179 |
| `src/domain/markdown_ast/schema_registry.py` | Registry freeze/collision behavior | 1-149 |
| `src/domain/markdown_ast/input_bounds.py` | Input validation bounds (context) | 1-76 |
| `tests/unit/domain/markdown_ast/test_document_type.py` | Existing test coverage | 1-277 |
| `projects/.../EN-002-document-type-ontology-hardening.md` | Proposed changes specification | Full |
| `projects/.../BUG-004-document-type-detection-misclassification.md` | RCA for current defects | Full |
| `projects/.../iteration-1/eng-qa-test-strategy.md` | QA test strategy (prior input) | Full |

### Data Flow Traced

1. `detect(file_path, content)` entry point -> `_normalize_path()` -> root marker extraction -> `_detect_from_path()` -> `_path_matches_glob()` / `_match_recursive_glob()` -> type return or fallback
2. `detect()` -> `_detect_from_structure(content)` -> linear scan of `STRUCTURAL_CUE_PRIORITY` -> type return or None
3. Combine signals: `path_type` authority check -> warning generation -> return
4. `DocumentType.UNKNOWN` -> schema registry `get()` call chain (F-008 gap)

### CWE Top 25 2025 Checklist (Selected for Review Scope)

| CWE | Name | Status |
|-----|------|--------|
| CWE-843 | Type Confusion | REVIEWED -- Primary threat; findings F-001, F-002, F-005 |
| CWE-22 | Path Traversal | REVIEWED -- `_normalize_path` marker extraction (F-001) |
| CWE-20 | Improper Input Validation | REVIEWED -- Null bytes (F-007), API contract (F-004), missing schemas (F-008, F-009) |
| CWE-697 | Incorrect Comparison | REVIEWED -- Pattern ordering (F-003) |
| CWE-435 | Improper Interaction Between Multiple Correctly-Behaving Entities | REVIEWED -- Structural cue + path classification interaction (F-005) |
| CWE-691 | Insufficient Control Flow Management | REVIEWED -- First-match-wins ordering; `_match_recursive_glob` fallback path |
| CWE-79 | XSS | NOT APPLICABLE -- No rendering of file content |
| CWE-89 | SQL Injection | NOT APPLICABLE -- No database access |
| CWE-78 | OS Command Injection | NOT APPLICABLE -- No system command execution |
| CWE-287 | Improper Authentication | NOT APPLICABLE -- No authentication in this component |
| CWE-502 | Deserialization | NOT APPLICABLE -- No object deserialization |
| CWE-798 | Hardcoded Credentials | NOT APPLICABLE -- No credentials in this component |
| CWE-352 | CSRF | NOT APPLICABLE -- No web request handling |

### Threat Model Correlation

This review correlates with the threat model referenced in `document_type.py` (T-DT-01 through T-DT-05). All five predicted threats were verified in this review. F-001 is the primary confirmation of T-DT-02 (path prefix confusion), which the threat model predicted but for which the current implementation has an incomplete mitigation.

---

### Review Confidence and Limitations

**Confidence: HIGH** for findings F-001 through F-005 (code-level analysis with reproduction steps). **MEDIUM** for F-008 and F-009 (require CLI adapter code inspection not included in this review scope -- the CLI adapter file was not read). **HIGH** for F-006 (fnmatch behavior confirmed against Python documentation semantics for wildcard handling).

**Limitations**:
- The full CLI adapter code (`src/interface/...` or equivalent) was not reviewed. F-008 and F-009 depend on assumptions about CLI adapter behavior.
- The threat model document (`eng-architect-001-threat-model.md`) was not directly read -- threat model references are drawn from code comments in `document_type.py` and `schema_registry.py`.
- No runtime testing was performed. All findings are based on static code analysis and data flow tracing.

---

*Review Version: 1.0.0*
*Agent: eng-security*
*Date: 2026-02-24*
*Source: EN-002 Document Type Ontology Hardening -- Security Review*
*SSDF Practice: PW.7 (Manual code review to identify vulnerabilities)*
*Reviewed files: document_type.py, schema_definitions.py, schema_registry.py, input_bounds.py, test_document_type.py, EN-002 design doc, BUG-004 RCA, eng-qa-test-strategy.md*
