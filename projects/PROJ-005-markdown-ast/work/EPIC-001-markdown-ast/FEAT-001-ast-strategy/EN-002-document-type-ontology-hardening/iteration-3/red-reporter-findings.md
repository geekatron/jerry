# RED-0002: Consolidated Security Finding Report
# EN-002 Document Type Ontology Hardening

<!-- AGENT: red-reporter | VERSION: 1.0.0 | DATE: 2026-02-24 | ENGAGEMENT: RED-0002 -->
<!-- METHODOLOGY: PTES Reporting Phase, OSSTMM Reporting Standards, NIST SP 800-115 Chapter 8 -->
<!-- SOURCES: iteration-1/eng-security-review.md, iteration-2/red-lead-scope.md, iteration-2/red-vuln-cwe843-analysis.md, src/domain/markdown_ast/document_type.py -->

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Business-focused overview for non-technical stakeholders |
| [L1 Finding Inventory](#l1-finding-inventory) | Complete finding table with CWE, CVSS, ATT&CK, and remediation status |
| [L2 Strategic Implications](#l2-strategic-implications) | Security program assessment and long-term recommendations |
| [Engagement Summary](#engagement-summary) | Scope, authorization, targets, methodology |
| [Remediation Status by Finding](#remediation-status-by-finding) | Per-finding status after EN-002 implementation |
| [Residual Risk Assessment](#residual-risk-assessment) | Overall post-EN-002 security posture |
| [Recommendations](#recommendations) | Prioritized remaining actions |
| [Scope Compliance Attestation](#scope-compliance-attestation) | Formal attestation that operations stayed within authorized scope |
| [Evidence Chain](#evidence-chain) | Artifact index and evidence provenance |

---

## L0 Executive Summary

### What Was Tested

The `DocumentTypeDetector` component in the Jerry framework (`src/domain/markdown_ast/document_type.py`) underwent two rounds of security review during the EN-002 Document Type Ontology Hardening enabler. This component classifies every markdown file in the repository into one of 13 document types, which determines how the file is parsed and validated by downstream automation.

The engagement tested five attack surfaces: path-based detection bypass, wildcard exploitation in pattern matching, structural cue content override, misuse of the UNKNOWN fallback type, and type confusion via pattern ordering. The review included a pre-implementation security code review (eng-security, iteration-1) followed by a post-implementation static vulnerability analysis (red-vuln, iteration-2) verifying whether the implementation resolved the identified issues.

### What Was Found

**Before EN-002:** The component had an active critical defect (BUG-004): the `"---"` structural cue caused approximately 59% of repository files (approximately 1,634 of 2,774 files) to be misclassified as AGENT_DEFINITION. One High finding (F-001, CWE-22/CWE-843), three Medium findings, three Low findings, and two Informational findings were identified.

**After EN-002:** No Critical or High findings remain. The implementation resolved the majority of identified issues. Two Medium findings persist as residual risk: a partial remediation of the path normalization vulnerability (RV-001) and missing parser matrix entries for two new document types (RV-002). Three Low and three Informational findings carry over or were newly identified; all are assessed as acceptable residual risk given current deployment constraints.

### Findings Count by Severity (Post-EN-002)

| Severity | Pre-EN-002 | Post-EN-002 | Delta |
|----------|-----------|-------------|-------|
| Critical | 0 | 0 | -- |
| High | 1 (F-001) | 0 | -1 (resolved) |
| Medium | 3 (F-002, F-003, F-004) | 2 (RV-001, RV-002) | -1 |
| Low | 3 (F-005, F-006, F-007) | 3 (RV-003, RV-004, RV-005) | 0 |
| Informational | 2 (F-008, F-009) | 3 (RV-006, RV-007, RV-008) | +1 |
| **Total** | **9** | **8** | **-1** |

### Overall Security Posture Assessment

**CONDITIONAL PASS.** EN-002 substantially improved the security posture of the `DocumentTypeDetector`. The root cause of BUG-004 (type confusion affecting 59% of files) has been eliminated. The implementation correctly enforces path-first detection, structured pattern tiers, and specific structural cues. The residual risk is bounded and manageable.

Two items require near-term attention before this component can be considered fully hardened: the parser matrix must be completed for the two new document types (two-line code change), and the path normalization vulnerability requires either a precondition docstring or a code-level fix for direct API callers.

### Top Risks to Business Operations

1. **Silent parser starvation for new document types (RV-002):** Files classified as SKILL_RESOURCE or TEMPLATE receive zero parsers in the current implementation. Any automation that processes these files via `UniversalDocument.parse()` receives a result with all content fields as `None`. This is a deterministic defect for a known set of files — not a theoretical attack. Priority: fix immediately as part of EN-002 completion.

2. **Path normalization bypass for direct API callers (RV-001):** The `detect()` domain API does not enforce path containment. A caller passing an absolute path to a file outside the repository root can cause the component to classify the file as an arbitrary trusted type. In the current deployment this is mitigated by the CLI adapter's path containment check, but the domain layer has no independent defense. Priority: document precondition; consider code fix if programmatic API usage expands.

3. **Structural cue false-positive for files at unrecognized paths (RV-003, RV-004):** Files at paths not covered by the 63+ pattern list fall through to structural cue detection, which can produce silent misclassification if the file content contains Jerry-specific strings in an explanatory context. Priority: accepted risk with two targeted pattern additions recommended.

---

## L1 Finding Inventory

### Complete Finding Table

| ID | Source | Severity | CWE | CVSS 3.1 | ATT&CK Analog | Status | Residual Risk |
|----|--------|----------|-----|----------|---------------|--------|---------------|
| F-001 | eng-security | High | CWE-22 / CWE-843 | 6.5 | T1036 (Masquerading) | Partially remediated | RV-001 (Medium) |
| F-002 | eng-security | Medium | CWE-843 | 4.3 | -- | Fully remediated | None |
| F-003 | eng-security | Medium | CWE-697 | 3.3 | -- | Fully remediated | None |
| F-004 | eng-security | Medium | CWE-20 | 4.4 | -- | Not applicable | None |
| F-005 | eng-security | Low | CWE-843 | 2.5 | -- | Fully remediated | None |
| F-006 | eng-security | Low | CWE-20 | 2.0 | -- | Confirmed non-finding | None |
| F-007 | eng-security | Low | CWE-20 | 2.0 | -- | Accepted risk | Low |
| F-008 | eng-security | Info | CWE-20 | N/A | -- | Resolved by design | None |
| F-009 | eng-security | Info | CWE-20 | N/A | -- | Partially resolved | RV-002 (Medium) |
| RV-001 | red-vuln | Medium | CWE-843 / CWE-22 | 5.3 | T1036 | New finding (F-001 residual) | Medium |
| RV-002 | red-vuln | Medium | CWE-697 / CWE-754 | 4.0 | -- | New finding (F-009 extension) | Medium |
| RV-003 | red-vuln | Low | CWE-843 | 3.1 | -- | Accepted risk | Low (Theoretical) |
| RV-004 | red-vuln | Low | CWE-843 | 2.5 | -- | Accepted risk | Low (Theoretical) |
| RV-005 | red-vuln | Low | CWE-691 | 2.5 | -- | Accepted risk (latent) | Low (Not exploitable) |
| RV-006 | red-vuln | Info | CWE-754 | N/A | -- | Design behavior confirmed | None |
| RV-007 | red-vuln | Info | CWE-20 | 2.0 | -- | Accepted risk | Informational |
| RV-008 | red-vuln | Info | CWE-697 | N/A | -- | Implementation correct | None |

### Individual Finding Reports

---

#### F-001: Root Marker Extraction Allows Embedded-Marker Path Confusion

| Attribute | Value |
|-----------|-------|
| Source | eng-security (iteration-1) |
| Severity | High |
| CWE | CWE-22 (Path Traversal) / CWE-843 (Type Confusion) |
| CVSS 3.1 | AV:L/AC:H/PR:N/UI:N/S:U/C:L/I:H/A:N -- Score: 6.5 |
| ATT&CK | T1036 (Masquerading) |
| Affected Component | `_normalize_path()` -- root marker extraction loop |
| ASVS Reference | V5.1.2 (Input Validation), V5.1.3 (Untrusted Path Handling) |
| Exploitability | Demonstrable (domain API), Low (CLI via path containment) |
| Post-EN-002 Status | Partially remediated |

**Description:** The `_normalize_path` function extracted the repo-relative portion of an absolute path by finding the first occurrence of a known root marker string (e.g., `skills/`, `docs/`) anywhere in the path using `str.find()`. A path like `/tmp/attacker/skills/target/agents/malicious.md` would have `skills/` found at a non-zero index, causing the path to be truncated to `skills/target/agents/malicious.md`, which then matches the `skills/*/agents/*.md` pattern and produces type AGENT_DEFINITION for an untrusted external file.

**EN-002 Remediation Applied:** The `already_relative` guard was added at lines 293-299 of `document_type.py`. When the path already starts with a recognized root marker (i.e., it is already in repo-relative form), the extraction loop is skipped entirely.

**Residual Risk (see RV-001):** The guard protects already-relative paths but does not address genuine absolute paths to files outside the repository. The domain API (`detect()` and `UniversalDocument.parse()`) has no path containment enforcement. The CLI adapter compensates via a path containment check in `_read_file`. Direct API callers remain exposed to the original F-001 vector.

**Remediation Guidance:** Add a precondition to the `detect()` docstring explicitly stating that `file_path` must be a repo-relative path or a filesystem-verified absolute path contained within the known repository root. As a code-level fix, implement a `_to_repo_relative()` helper that resolves the path against the repo root and strips the prefix before calling `_normalize_path`. This eliminates the substring-search ambiguity entirely.

---

#### F-002: "## Status" Structural Cue Creates ADR Type Confusion

| Attribute | Value |
|-----------|-------|
| Source | eng-security (iteration-1) |
| Severity | Medium |
| CWE | CWE-843 (Type Confusion) |
| CVSS 3.1 | AV:L/AC:M/PR:N/UI:N/S:U/C:N/I:M/A:N -- Score: 4.3 |
| Post-EN-002 Status | Fully remediated |

**Description:** The proposed `("## Status", DocumentType.ADR)` structural cue would have fired on any path-unmatched file containing the `## Status` heading, a section common in worktracker entities, skill playbooks, and knowledge documents. This would have produced silent ADR misclassification.

**EN-002 Remediation Applied:** The `"## Status"` cue was removed entirely from `STRUCTURAL_CUE_PRIORITY`. The final implementation contains 6 structural cues, none of which include `"## Status"`. Verified in `document_type.py` lines 153-165. No residual risk.

---

#### F-003: First-Match-Wins Ordering: `projects/*/work/**` Pattern Ordering

| Attribute | Value |
|-----------|-------|
| Source | eng-security (iteration-1) |
| Severity | Medium |
| CWE | CWE-697 (Incorrect Comparison) |
| CVSS 3.1 | AV:L/AC:M/PR:N/UI:N/S:U/C:N/I:L/A:N -- Score: 3.3 |
| Post-EN-002 Status | Fully remediated |

**Description:** The proposed pattern ordering for `projects/*/work/**/*.md` (WORKTRACKER_ENTITY) and `projects/*/orchestration/**/*.md` (ORCHESTRATION_ARTIFACT) had a potential maintenance risk if the ordering intent was not documented. The concern was that a future maintainer could insert a pattern between them and disrupt the intended precedence.

**EN-002 Remediation Applied:** The implementation places `projects/*/work/**/*.md` at line 99 (Tier 3) and `projects/*/orchestration/**/*.md` at line 119 (Tier 5). The 5-tier comment structure (lines 75, 83, 97, 110, 118) documents the ordering intent directly in the code. The red-vuln analysis confirmed that `work/` and `orchestration/` are sibling directories with non-overlapping patterns; no symlink-based ambiguity was found. No residual risk.

---

#### F-004: UNKNOWN Fallback API Change Is a Breaking Change

| Attribute | Value |
|-----------|-------|
| Source | eng-security (iteration-1) |
| Severity | Medium |
| CWE | CWE-20 (Improper Input Validation -- API contract violation) |
| CVSS 3.1 | AV:L/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:L -- Score: 4.4 |
| Post-EN-002 Status | Not applicable |

**Description:** The EN-002 design proposed changing `detect()` to return a 3-tuple when UNKNOWN is returned, which would have broken all callers using 2-element destructuring (`doc_type, warning = detect(...)`).

**EN-002 Remediation Applied:** The 3-tuple return was not implemented. The final `detect()` method (lines 167-216) returns `tuple[DocumentType, str | None]` consistently for all code paths including UNKNOWN. The implementation uses `return (DocumentType.UNKNOWN, None)` at line 216. This finding is not applicable to the current implementation. No residual risk.

---

#### F-005: `"<purpose>"` Structural Cue False Positive Risk

| Attribute | Value |
|-----------|-------|
| Source | eng-security (iteration-1) |
| Severity | Low |
| CWE | CWE-843 (Type Confusion) |
| CVSS 3.1 | AV:L/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:N -- Score: 2.5 |
| Post-EN-002 Status | Fully remediated |

**Description:** The proposed `("<purpose>", DocumentType.AGENT_DEFINITION)` structural cue could have triggered on documentation files discussing the agent definition `<purpose>` section format.

**EN-002 Remediation Applied:** The `<purpose>` cue was removed entirely from the final `STRUCTURAL_CUE_PRIORITY`. Only `<identity>` and `<methodology>` are used as AGENT_DEFINITION structural cues (lines 154-156). The removal further reduces the AS-3 attack surface beyond what eng-security recommended. No residual risk.

---

#### F-006: `fnmatch` Wildcard Exploitation Analysis

| Attribute | Value |
|-----------|-------|
| Source | eng-security (iteration-1) |
| Severity | Low |
| CWE | CWE-20 (Improper Input Validation) |
| CVSS 3.1 | AV:L/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:N -- Score: 2.0 |
| Post-EN-002 Status | Confirmed non-finding |

**Description:** Concern that filenames containing glob-special characters (`*`, `?`, `[`, `]`) could cause unintended pattern matches.

**Red-vuln Verification:** Confirmed that `fnmatch.fnmatch(path, pattern)` treats the path argument as a literal string. Wildcards in the path argument are not interpreted as metacharacters. The segment-by-segment matching in `_match_recursive_glob` was also verified: brackets in path segments are treated literally when in the string (first argument) position. The `**`-in-filename case was also tested: `_path_matches_glob` checks `if "**" in pattern`, not `if "**" in path`, so filenames containing `**` do not trigger the recursive branch. No exploitation path found. Non-finding confirmed.

---

#### F-007: `_normalize_path` Does Not Reject Null Bytes

| Attribute | Value |
|-----------|-------|
| Source | eng-security (iteration-1) |
| Severity | Low |
| CWE | CWE-20 (Improper Input Validation) |
| CVSS 3.1 | AV:L/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:N -- Score: 2.0 |
| Post-EN-002 Status | Accepted risk |

**Description:** A path argument containing null bytes is not rejected by `_normalize_path`. A null-byte-injected path could trigger marker extraction at an unexpected position.

**Risk Acceptance Rationale:** The typical call sites (CLI `ast_detect` reading from `pathlib.Path.rglob`, internal tests with trusted paths) do not produce paths containing null bytes. Even if a null-byte path reaches `fnmatch`, the worst outcome is UNKNOWN return (the safe default). The risk is accepted at current deployment scope. Adding a null byte guard is a one-line defensive hardening measure that should be included in a future hardening sweep.

**Recommended Guard (not yet implemented):**
```python
def _normalize_path(file_path: str) -> str:
    if "\x00" in file_path:
        return ""  # Safe: empty path matches no pattern, returns UNKNOWN
    ...
```

---

#### F-008: UNKNOWN Schema Gap -- Registry Has No UNKNOWN Schema

| Attribute | Value |
|-----------|-------|
| Source | eng-security (iteration-1) |
| Severity | Informational |
| CWE | CWE-20 (Missing validation for sentinel type) |
| CVSS 3.1 | N/A (behavioral, not exploitable) |
| Post-EN-002 Status | Resolved by design |

**Description:** Concern that `schema_registry.get("unknown")` would raise `ValueError` if `ast_validate` was called for an UNKNOWN file without an explicit `--schema` flag.

**Red-vuln Verification:** Confirmed resolved. The `ast_validate` CLI command does not call `schema_registry.get(doc_type)` as a DocumentType-based lookup. It accepts an explicit `--schema` parameter and only calls `get_entity_schema(schema)` when that parameter is provided. For UNKNOWN files without `--schema`, the command performs nav table validation only and returns `schema_valid: True`. No ValueError is raised. No residual risk.

---

#### F-009: New `SKILL_RESOURCE` and `TEMPLATE` Enum Values Have No Schemas

| Attribute | Value |
|-----------|-------|
| Source | eng-security (iteration-1) |
| Severity | Informational |
| CWE | CWE-20 (Missing validation for new entity types) |
| CVSS 3.1 | N/A (behavioral) |
| Post-EN-002 Status | Partially resolved -- extended by RV-002 |

**Description:** The new `SKILL_RESOURCE` and `TEMPLATE` enum values were not registered in the schema registry, meaning `schema_registry.get("skill_resource")` would raise ValueError.

**EN-002 Partial Remediation:** The red-vuln analysis confirmed that schema registration is still absent for both types. Additionally, red-vuln extended this finding: both types are also absent from `_PARSER_MATRIX` in `universal_document.py`, creating a three-system gap (path patterns registered, schema absent, parser matrix absent). This extension is captured as RV-002.

---

#### RV-001: `already_relative` Guard Does Not Cover All Absolute Path Bypass Vectors

| Attribute | Value |
|-----------|-------|
| Source | red-vuln (iteration-2) |
| Severity | Medium |
| CWE | CWE-843 (Type Confusion) / CWE-22 (Path Traversal) |
| CVSS 3.1 | AV:L/AC:H/PR:N/UI:N/S:U/C:L/I:M/A:N -- Score: 5.3 |
| ATT&CK | T1036 (Masquerading) |
| Exploitability | Demonstrable (via direct API), Low (via CLI) |
| Prior Finding | F-001 (High) -- partially remediated |
| Post-EN-002 Status | Residual medium risk |

**Description:** The `already_relative` guard (lines 293-299 of `document_type.py`) prevents re-extraction of already-relative paths but does not prevent the original F-001 attack vector for genuine absolute paths to files outside the repo. Three bypass conditions exist:

1. **Absolute path not starting with a root marker:** A path like `/tmp/evil/skills/target/agents/evil.md` does not start with any root marker, so `already_relative = False`. The extraction loop executes, finds `skills/` at a positive index, and strips to `skills/target/agents/evil.md` -- an AGENT_DEFINITION match.

2. **Domain API with no path containment:** `UniversalDocument.parse()` and `DocumentTypeDetector.detect()` accept any `file_path` argument with no containment enforcement. Direct API callers are fully exposed to the F-001 vector. The CLI path containment check in `_read_file` (ast_commands.py lines 176-223) is the only compensating control and only applies to the CLI entry point.

3. **Mixed separators (POSIX: no additional bypass; Windows: additional bypass condition):** On POSIX deployments (primary deployment platform), mixed separators do not add bypass vectors. On Windows, a drive letter combined with an embedded marker creates a condition identical to Condition 1.

**Mitigating Controls:** CLI `_read_file` path containment check blocks external paths for the CLI entry point. Direct API usage (not through CLI) has no compensating control.

**Remediation Guidance:**

Primary: Add a `_to_repo_relative()` pre-processing step inside `detect()` using `pathlib.Path` resolution and prefix stripping. This eliminates the vulnerability at the domain layer.

Secondary (minimum): Add an explicit precondition to the `detect()` docstring: "file_path must be a repo-relative path or a filesystem-verified absolute path within the repository root."

---

#### RV-002: `SKILL_RESOURCE` and `TEMPLATE` Missing from `_PARSER_MATRIX`

| Attribute | Value |
|-----------|-------|
| Source | red-vuln (iteration-2) |
| Severity | Medium |
| CWE | CWE-697 (Incorrect Comparison) / CWE-754 (Improper Check for Exceptional Conditions) |
| CVSS 3.1 | AV:L/AC:L/PR:N/UI:N/S:U/C:N/I:M/A:L -- Score: 4.0 |
| Exploitability | Demonstrable (deterministic -- no craft required) |
| Prior Finding | F-009 (Informational) -- extended |
| Post-EN-002 Status | Defect in EN-002 implementation |

**Description:** `DocumentType.SKILL_RESOURCE` and `DocumentType.TEMPLATE` are present in the `DocumentType` enum and have 10 and 3 path patterns respectively, but are absent from `_PARSER_MATRIX` in `universal_document.py` (lines 96-108). When `detect()` returns either type, `UniversalDocument.parse()` calls `_PARSER_MATRIX.get(detected_type, set())` which returns the default empty set. Zero parsers are invoked, producing a `UniversalParseResult` with all content fields as `None`.

**Impact:** Deterministic for every SKILL_RESOURCE and TEMPLATE file in the repository. Callers cannot distinguish "parser not invoked" from "parser returned no results" because both produce `None` fields. Navigation table validation silently does not run for these file types. Any automation routing on field presence receives incorrect results without error or warning.

**Affected Files:** All files at paths matching:
- `skills/*/PLAYBOOK.md`, `skills/*/tests/*.md`, `skills/*/composition/*.md`, `skills/*/reference/*.md`, `skills/*/references/*.md`, `skills/*/docs/*.md`, `skills/*/validation/*.md`, `skills/shared/*.md`, `skills/*/test_data/**/*.md`, `skills/*/*.md` (SKILL_RESOURCE)
- `skills/*/templates/*.md`, `.context/templates/worktracker/*.md`, `.context/templates/design/*.md`, `.context/templates/**/*.md`, `docs/templates/*.md` (TEMPLATE)

**Remediation Guidance:** Add two entries to `_PARSER_MATRIX` in `universal_document.py`:

```python
DocumentType.SKILL_RESOURCE: {"nav"},
DocumentType.TEMPLATE: {"blockquote", "nav"},
```

This is a two-line code change. SKILL_RESOURCE should receive nav table extraction (consistent with KNOWLEDGE_DOCUMENT treatment). TEMPLATE should receive blockquote and nav extraction because template files may contain `> **Strategy:**` or similar blockquote frontmatter.

Additionally, register `SKILL_RESOURCE_SCHEMA` and `TEMPLATE_SCHEMA` in the schema registry (per F-009 recommendation), even with empty rule sets, to prevent `ValueError` if schema lookup is ever attempted for these types.

---

#### RV-003: `> **Type:**` Structural Cue False-Positive via Quoted Content

| Attribute | Value |
|-----------|-------|
| Source | red-vuln (iteration-2) |
| Severity | Low |
| CWE | CWE-843 (Type Confusion via content injection) |
| CVSS 3.1 | AV:L/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:N -- Score: 3.1 |
| Exploitability | Theoretical |
| Prior Finding | Extends F-005 scope |
| Post-EN-002 Status | Accepted risk |

**Description:** The `_detect_from_structure` method uses `if cue in content` (line 247), a substring containment check with no line-boundary awareness. The cue `"> **Type:**"` can appear in non-worktracker content: documentation files explaining the blockquote frontmatter format, or any file containing a quoted passage that mentions the Type field. Files at path-unmatched locations containing this string are silently misclassified as WORKTRACKER_ENTITY.

**Exploitability Constraint:** Requires a file at a path matching none of the 63+ path patterns. The M-14 warning does not fire for structural-only detections (it requires both path and structural signals), so the misclassification is silent. The `{"blockquote", "nav"}` parser set invoked for WORKTRACKER_ENTITY is relatively benign.

**Risk Acceptance Rationale:** The 63+ path patterns cover essentially all legitimate document locations. Files reaching structural-only detection are unusual edge cases. Accepted as residual low risk.

---

#### RV-004: `<!-- L2-REINJECT` Cue Triggered by Documentation About L2-REINJECT

| Attribute | Value |
|-----------|-------|
| Source | red-vuln (iteration-2) |
| Severity | Low |
| CWE | CWE-843 (Type Confusion via content injection) |
| CVSS 3.1 | AV:L/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:N -- Score: 2.5 |
| Exploitability | Theoretical |
| Prior Finding | Extends F-005 scope |
| Post-EN-002 Status | Accepted risk with pattern gap identified |

**Description:** A documentation file at `docs/architecture/*.md` (a path not covered by any current pattern) that discusses the L2-REINJECT mechanism would contain the literal string `<!-- L2-REINJECT` and be misclassified as RULE_FILE. The reinject parser would then extract example directives as operative directives.

**Pattern Gap:** `docs/architecture/` is not in PATH_PATTERNS. The `docs/*.md` catch-all covers only shallow `docs/` root files in intended interpretation, though due to `fnmatch`'s boundary-crossing `*` behavior it also catches files in unrecognized subdirectories (producing KNOWLEDGE_DOCUMENT, the correct type for those files). However, this only applies when `docs/architecture/*.md` reaches structural detection -- which requires that no earlier pattern matches. The `docs/*.md` pattern at line 141 DOES match `docs/architecture/file.md` via fnmatch's `*` boundary-crossing, so the gap is narrower than it appears: `docs/architecture/*.md` files would actually match `docs/*.md` and be classified as KNOWLEDGE_DOCUMENT before reaching structural detection.

**Risk Assessment:** Theoretical. The path gap identified by red-vuln is partially self-healed by the broader-than-intended `fnmatch` behavior of `docs/*.md`. Accepted as residual low risk with a low-priority recommendation to explicitly add `docs/architecture/*.md` to PATH_PATTERNS.

---

#### RV-005: `_match_recursive_glob` Multiple-`**` Fallback Is Incorrect

| Attribute | Value |
|-----------|-------|
| Source | red-vuln (iteration-2) |
| Severity | Low |
| CWE | CWE-691 (Insufficient Control Flow Management) |
| CVSS 3.1 | AV:L/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:N -- Score: 2.5 |
| Exploitability | Not currently exploitable (fallback is unreachable) |
| Prior Finding | Extends F-006 scope |
| Post-EN-002 Status | Accepted risk (latent maintenance trap) |

**Description:** `_match_recursive_glob` handles patterns containing more than one `**` by falling back to `fnmatch.fnmatch(path, pattern)` with a "best effort" comment (lines 353-356). However, `fnmatch` does not support recursive `**` semantics -- it treats `**` as two consecutive single-character wildcards. For any multi-`**` pattern, this fallback silently produces incorrect match results.

**Current State:** No patterns in `PATH_PATTERNS` contain multiple `**`. The fallback code path is currently unreachable in production. The risk is a latent maintenance trap: a future maintainer adding a pattern with multiple `**` segments would receive silently incorrect match behavior.

**Recommended Fix (low priority):**
```python
if len(parts) != 2:
    import warnings
    warnings.warn(
        f"Pattern '{pattern}' contains multiple '**' segments; "
        "returning False (no match) to avoid incorrect fnmatch behavior.",
        stacklevel=2
    )
    return False
```

---

#### RV-006: UNKNOWN Classification Silently Bypasses All Parsers Except nav

| Attribute | Value |
|-----------|-------|
| Source | red-vuln (iteration-2) |
| Severity | Informational |
| CWE | CWE-754 (Improper Check for Exceptional Conditions) |
| CVSS 3.1 | N/A (behavioral design finding) |
| Post-EN-002 Status | Design behavior confirmed -- no action required |

**Description:** `DocumentType.UNKNOWN: {"nav"}` in `_PARSER_MATRIX` means UNKNOWN files receive nav-only parsing. The F-008 concern (that `ast_validate` would raise ValueError for UNKNOWN files) was verified as not applicable: `ast_validate` does not use DocumentType-based schema lookup. UNKNOWN is the correct safe sentinel with minimal, benign parsing. No security concern.

---

#### RV-007: `_ROOT_FILES` Basename Extraction Does Not Verify Parent Directory

| Attribute | Value |
|-----------|-------|
| Source | red-vuln (iteration-2) |
| Severity | Informational |
| CWE | CWE-20 (Improper Input Validation) |
| CVSS 3.1 | AV:L/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:N -- Score: 2.0 |
| Exploitability | Theoretical |
| Post-EN-002 Status | Accepted risk |

**Description:** The `_ROOT_FILES` extraction block (lines 304-315) reduces any absolute path ending in a root-level filename (e.g., `CLAUDE.md`) to its basename when the path is not under a known root marker. A file named `CLAUDE.md` at an external path would be classified as FRAMEWORK_CONFIG. In practice, the CLI path containment check rejects external paths, and in-repo nested files named `CLAUDE.md` are caught by more specific patterns before the `_ROOT_FILES` block applies. Risk is informational.

---

#### RV-008: `_match_recursive_glob` Suffix Matching Algorithm Is Correct

| Attribute | Value |
|-----------|-------|
| Source | red-vuln (iteration-2) |
| Severity | Informational |
| CWE | CWE-697 (Incorrect Comparison) |
| CVSS 3.1 | N/A (logic analysis -- no exploitation path) |
| Post-EN-002 Status | Implementation confirmed correct |

**Description:** The suffix matching algorithm in `_match_recursive_glob` (lines 375-382) reverses both the remaining path segments and suffix pattern segments and checks them pairwise. Red-vuln verified this is correct for all current patterns (all use single-segment suffixes `*.md`). No exploitation path found. Informational documentation of algorithm behavior for future maintainers.

---

## L2 Strategic Implications

### Systemic Security Patterns Identified

**Pattern 1: Trust Level Mismatch Between Path Origin and Path Processing**

The most significant systemic finding across both reviews is that path trust level and path processing are conflated in `_normalize_path`. The function is designed for usability (handling both absolute and relative paths transparently) but this usability-first design creates a security tension: stripping an absolute path prefix is a trust reduction operation (moving from an untrusted absolute path to a trusted relative form) but it is implemented without verifying that the trust reduction is warranted. The CLI adapter compensates via containment checks, but the domain layer has no independent defense. This is an architectural concern that will require attention if the programmatic API surface expands.

**Pattern 2: Three-System Registration Gap for New DocumentType Values**

When new `DocumentType` enum values were added in EN-002 (`SKILL_RESOURCE`, `TEMPLATE`), three registration systems required updating: the PATH_PATTERNS list, the schema registry, and `_PARSER_MATRIX`. The path patterns were added. The schema registry and parser matrix were not. This three-system gap is a process failure, not a code failure -- the acceptance criteria for EN-002 (TC-6) specified schema registration but did not explicitly include parser matrix registration. Future enum additions must include a checklist verifying all three systems.

**Pattern 3: Structural Cue Precision Degrades as Documentation Grows**

The structural cues are precision-dependent: they work correctly when the specific strings they look for are rare in repo content. As documentation about the framework grows (guides, architecture docs, published articles about Jerry), structural cues become more likely to appear in documentation content rather than in the document types they are designed to detect. The path-first architecture mitigates this for files at recognized paths, but the fallback structural detection layer has no mechanism to distinguish "this cue appears as an operative marker" from "this cue appears as a discussed example." This is an inherent limitation of substring-based structural detection.

### Defense Gap Analysis

| Defense Layer | Pre-EN-002 | Post-EN-002 | Gap Status |
|---------------|-----------|-------------|------------|
| Path-first classification | Implemented but undermined by broad `"---"` cue | Correctly implemented and enforced | Closed |
| Structural cue specificity | Very low (`"---"`, `"<!--"` match ~59% of files) | High (6 specific cues) | Substantially closed |
| Pattern ordering documentation | Absent | 5-tier comment structure present | Closed |
| Parser matrix completeness | 11 of 11 known types registered | 11 of 13 types registered | Gap: SKILL_RESOURCE, TEMPLATE |
| Schema registry completeness | Matches enum | Matches enum minus 2 new types | Gap: SKILL_RESOURCE, TEMPLATE |
| Domain API path containment | Absent | Absent (CLI adapter compensates) | Partial -- domain layer gap |
| Null byte rejection | Absent | Absent | Gap: low severity, accepted |

### Comparison with Industry Benchmarks

The post-EN-002 `DocumentTypeDetector` implements the correct security architecture for a classification component:

- **Allowlist-based classification (OWASP ASVS V5.1.2):** PATH_PATTERNS is an explicit allowlist; unmatched files receive the safe UNKNOWN type rather than a default permissive classification.
- **Authority hierarchy (OWASP ASVS V1.5.2):** Path takes priority over content, preventing content-based spoofing of the classification signal.
- **Safe default (NIST SP 800-53 SI-10):** UNKNOWN is the safe fallback; the component fails closed (no parsers) rather than open (all parsers).
- **Explicit trust boundaries:** The M-14 dual-signal warning mechanism surfaces disagreements between path and structural signals, preventing silent misclassification for path-matched files.

The residual gaps (domain API path containment, parser matrix completeness) are known and bounded. The overall architecture conforms to industry patterns for input validation components.

### Long-Term Remediation Roadmap

| Priority | Item | Effort | Target |
|----------|------|--------|--------|
| P1 | Complete `_PARSER_MATRIX` for SKILL_RESOURCE and TEMPLATE | Minimal (2 lines) | EN-002 completion |
| P1 | Register SKILL_RESOURCE_SCHEMA and TEMPLATE_SCHEMA | Minimal (schema stubs) | EN-002 completion |
| P2 | Add `detect()` docstring precondition for path trust | Minimal (documentation) | Next sprint |
| P2 | Add null byte guard to `_normalize_path` | Minimal (1 line) | Next hardening sweep |
| P3 | Add `docs/architecture/*.md` to PATH_PATTERNS | Minimal (1 line) | Pattern coverage audit |
| P3 | Replace multi-`**` fallback with explicit `return False` + warning | Minimal (4 lines) | Next hardening sweep |
| P4 | Implement `_to_repo_relative()` domain-layer path containment | Low-Medium | Future API hardening |

---

## Engagement Summary

### Authorization and Scope

| Attribute | Value |
|-----------|-------|
| Engagement ID | RED-0002 |
| Authorization | User-confirmed per red-lead-scope.md v1.0 |
| Engagement Type | Static vulnerability analysis (analysis-only, read-only) |
| Time Window | 2026-02-24 (single-session engagement) |
| Methodology | PTES Pre-Engagement Interactions + NIST SP 800-115 Chapter 4 |
| Agent Authorization | red-vuln (AUTHORIZED), red-lead (scope only), red-reporter (conditional) |
| No-go agents | red-exploit, red-privesc, red-lateral, red-persist, red-exfil, red-social, red-infra |

### Authorized Target Files

| File | Role |
|------|------|
| `src/domain/markdown_ast/document_type.py` | Primary target -- all attack surfaces |
| `src/domain/markdown_ast/universal_document.py` | Downstream consumer -- `_PARSER_MATRIX` |
| `src/domain/markdown_ast/universal_parse_result.py` | Downstream consumer -- result type |
| `src/interface/cli/ast_commands.py` | CLI adapter -- entry point analysis |
| `src/infrastructure/internal/enforcement/pre_tool_enforcement_engine.py` | Read-only reference |
| `src/domain/markdown_ast/__init__.py` | Public API surface verification |

### Techniques Applied

| Technique | Description | Findings |
|-----------|-------------|---------|
| STATIC-001 | Source code review for type confusion patterns | RV-001 through RV-008 |
| STATIC-002 | Data flow analysis through classification pipeline | RV-001, RV-002, RV-006 |
| STATIC-003 | Pattern ordering analysis for first-match-wins semantics | AS-5 verification |
| STATIC-004 | Crafted input construction for theoretical attack path validation | RV-003, RV-004 |
| STATIC-005 | Downstream impact analysis via `_PARSER_MATRIX` | RV-002, RV-006 |

### What Was Not Authorized

- Modification of any source file
- Execution of exploit code against live systems
- Network access or external reconnaissance
- Automated fuzzing or test execution
- Modification of test files

---

## Remediation Status by Finding

| Finding | Pre-Status | EN-002 Action | Post-Status | Verification Method |
|---------|-----------|---------------|-------------|---------------------|
| F-001 (High, CWE-22/843) | Open | `already_relative` guard added at lines 293-299 | Partially remediated | red-vuln static analysis -- RV-001 documents residual bypass via domain API |
| F-002 (Medium, CWE-843) | Open | `"## Status"` cue removed entirely | Fully remediated | red-vuln verified: STRUCTURAL_CUE_PRIORITY has 6 entries, no `"## Status"` present |
| F-003 (Medium, CWE-697) | Open | 5-tier comment structure; correct ordering implemented | Fully remediated | red-vuln verified: `projects/*/work/**/*.md` at Tier 3 (line 99) precedes `projects/*/orchestration/**/*.md` at Tier 5 (line 119) |
| F-004 (Medium, CWE-20) | Open | 3-tuple return not implemented | Not applicable | red-vuln verified: `detect()` returns `tuple[DocumentType, str \| None]` consistently |
| F-005 (Low, CWE-843) | Open | `<purpose>` cue removed (beyond recommendation -- full removal) | Fully remediated | red-vuln verified: `<purpose>` absent from STRUCTURAL_CUE_PRIORITY |
| F-006 (Low, CWE-20) | Open | fnmatch behavior confirmed; no code change required | Confirmed non-finding | red-vuln verified: path argument treated as literal; segment matching also verified |
| F-007 (Low, CWE-20) | Open | No null byte guard added | Accepted risk | red-vuln confirmed: null bytes reach `_normalize_path`; worst case UNKNOWN (safe) |
| F-008 (Info, CWE-20) | Open | `ast_validate` uses explicit schema param; no DocumentType-based registry call | Resolved by design | red-vuln traced `ast_validate` code path; confirmed no `schema_registry.get(doc_type)` call |
| F-009 (Info, CWE-20) | Open | SKILL_RESOURCE and TEMPLATE added to enum and patterns | Partially resolved | red-vuln confirmed: both types absent from `_PARSER_MATRIX` and schema registry (RV-002) |
| RV-001 (Medium, CWE-843) | New | -- | Open | New finding from red-vuln analysis |
| RV-002 (Medium, CWE-697) | New | -- | Open | New finding from red-vuln analysis |
| RV-003 (Low, CWE-843) | New | -- | Accepted risk | Theoretical exploitability; path coverage mitigates |
| RV-004 (Low, CWE-843) | New | -- | Accepted risk | Partially self-healed by fnmatch boundary crossing; theoretical |
| RV-005 (Low, CWE-691) | New | -- | Accepted risk | Fallback currently unreachable; latent maintenance trap |
| RV-006 (Info, CWE-754) | New | -- | Design confirmed | Correct behavior; informational |
| RV-007 (Info, CWE-20) | New | -- | Accepted risk | Informational; CLI containment compensates |
| RV-008 (Info, CWE-697) | New | -- | Implementation confirmed correct | Algorithm verified for all current patterns |

---

## Residual Risk Assessment

### Post-EN-002 Security Posture: CONDITIONAL PASS

The EN-002 implementation has closed the BUG-004 root cause (the `"---"` structural cue causing 59% of files to be misclassified as AGENT_DEFINITION). The classification pipeline is substantially more accurate and secure than the pre-EN-002 state.

### Residual Risk Summary

**Medium residual risk (2 findings -- action required):**

- **RV-001:** The domain API (`detect()`, `UniversalDocument.parse()`) accepts unvalidated absolute paths. The CLI adapter compensates with a path containment check, but direct API callers have no independent protection. Risk is bounded by the current deployment context where the programmatic API is used only internally with trusted paths.

- **RV-002:** SKILL_RESOURCE and TEMPLATE are classified correctly but parsed with zero parsers. This is a deterministic defect affecting a known set of files. All automation that processes these types via `UniversalDocument.parse()` receives silently incomplete results.

**Low residual risk (3 findings -- accepted):**

- **RV-003, RV-004:** Structural cue false-positives for files at unrecognized paths. Theoretical exploitability; limited impact (benign parser sets invoked). Path coverage mitigates substantially.
- **RV-005:** Latent bug in multi-`**` fallback. Currently unreachable. No current exploit path.

**Informational (3 findings -- no action required):**

- **RV-006, RV-007, RV-008:** Design behaviors confirmed correct; implementation verified correct; informational for future maintainers.

### Risk Rating by Dimension

| Dimension | Pre-EN-002 | Post-EN-002 |
|-----------|-----------|-------------|
| Classification accuracy | Critical (59% misclassification) | High (2 types missing parsers only) |
| Path-based spoofing resistance | High (F-001 active) | Medium (domain API gap) |
| Structural cue precision | Critical (`"---"` matches all YAML) | High (6 specific cues) |
| UNKNOWN fallback safety | High | High |
| Pattern ordering correctness | Medium (undocumented) | High (5-tier documented) |
| Parser matrix completeness | High | Medium (2 of 13 types missing) |
| Schema registry completeness | High | Medium (2 of 13 types missing) |

---

## Recommendations

### Immediate (EN-002 Completion Criteria)

1. **Complete `_PARSER_MATRIX` for SKILL_RESOURCE and TEMPLATE (RV-002):** Add two entries to `_PARSER_MATRIX` in `universal_document.py`. This is a two-line code change that eliminates the silent parser starvation defect for all SKILL_RESOURCE and TEMPLATE files. Recommend treating this as a defect in the EN-002 implementation, not a future enhancement.

   ```python
   # In universal_document.py, _PARSER_MATRIX:
   DocumentType.SKILL_RESOURCE: {"nav"},
   DocumentType.TEMPLATE: {"blockquote", "nav"},
   ```

2. **Register SKILL_RESOURCE_SCHEMA and TEMPLATE_SCHEMA (F-009 follow-through):** Add minimal schema stubs in the schema registry for both types to prevent ValueError if schema lookup is ever attempted. Empty schemas are acceptable.

### Near-Term (Next Sprint)

3. **Add `detect()` docstring precondition for path trust (RV-001 documentation):** Document that `file_path` must be a repo-relative path or a filesystem-verified path within the repo root. This formally establishes the trust precondition that the CLI adapter enforces but the domain layer does not.

4. **Add null byte guard to `_normalize_path` (F-007):** Add a one-line guard at the start of `_normalize_path` to reject null bytes and return an empty string (which produces UNKNOWN, the safe default). This is defensive hardening against an unlikely but possible input vector.

### Low Priority (Next Hardening Sweep)

5. **Add `docs/architecture/*.md` to PATH_PATTERNS as KNOWLEDGE_DOCUMENT (RV-004):** Explicit pattern eliminates the dependency on fnmatch's boundary-crossing behavior to cover this path, making the intent unambiguous.

6. **Replace multi-`**` fallback with `return False` and a warning (RV-005):** Eliminates the latent maintenance trap where a future multi-`**` pattern would silently produce incorrect match results.

### Future (API Hardening)

7. **Implement `_to_repo_relative()` domain-layer path containment (RV-001 code fix):** When the programmatic API surface expands beyond internal trusted callers, implement path resolution and containment at the domain layer so the defense does not depend solely on the CLI adapter.

---

## Scope Compliance Attestation

I, red-reporter, attest that based on my review of the evidence chain documented below:

**Engagement RED-0002 operated within the authorized scope defined in `iteration-2/red-lead-scope.md` version 1.0.**

Specifically:

1. **Target compliance:** All analysis was performed on the six authorized target files. No files outside the authorized target list were modified. No files outside the authorized target list were used as attack targets.

2. **Technique compliance:** Only STATIC-001 through STATIC-005 (static analysis techniques) were applied. No active exploitation, no code modification, no test execution, no network access, and no automated fuzzing occurred.

3. **Agent authorization compliance:** red-vuln (AUTHORIZED) performed the analysis. red-lead (AUTHORIZED) defined the scope. red-reporter (CONDITIONALLY AUTHORIZED) produced this report. No non-authorized agents (red-exploit, red-privesc, red-lateral, red-persist, red-exfil, red-social, red-infra, red-recon) participated in the engagement.

4. **Rules of engagement compliance:** The engagement was analysis-only. All findings are framed as methodology guidance with exploitability assessments clearly labeled (Theoretical / Demonstrable / Confirmed). No finding constitutes an executable exploit. Crafted input examples in the red-vuln analysis are for analysis demonstration only.

5. **Constitutional compliance:** P-003 (no recursive subagents), P-020 (user authority respected -- engagement confirmed by user), P-022 (no deception -- risk scores are honest assessments not inflated or minimized).

6. **Scope boundary compliance:** No findings were produced from files outside the authorized target list. The scope exclusions (tests/**, schema files, .context/rules/**, docs/governance/**) were respected. One observation about schema registration (F-009, RV-002) referenced schema files only by name from source code analysis of the primary target files, not by direct read.

**Attestation: All operations in engagement RED-0002 remained within the authorized scope boundaries.**

---

## Evidence Chain

### Artifact Index

| Artifact | Location | Agent | Date | Role |
|----------|----------|-------|------|------|
| Scope document | `iteration-2/red-lead-scope.md` | red-lead | 2026-02-24 | Authorization boundary definition |
| eng-security review | `iteration-1/eng-security-review.md` | eng-security | 2026-02-24 | 9 pre-implementation findings (F-001 through F-009) |
| red-vuln analysis | `iteration-2/red-vuln-cwe843-analysis.md` | red-vuln | 2026-02-24 | 8 post-implementation findings (RV-001 through RV-008); F-001 through F-009 remediation verification |
| Source code (primary target) | `src/domain/markdown_ast/document_type.py` | -- | Current | Implementation evidence for all findings |
| This report | `iteration-3/red-reporter-findings.md` | red-reporter | 2026-02-24 | Consolidated report |

### Evidence Chain Validation

| Finding | Evidence Source | Evidence Type | Confidence |
|---------|----------------|---------------|------------|
| F-001 remediation (partial) | `document_type.py` lines 293-299 | Code inspection | High |
| F-002 remediation (full) | `document_type.py` lines 153-165 | Code inspection -- `"## Status"` absent | High |
| F-003 remediation (full) | `document_type.py` lines 99, 119 | Code inspection -- correct tier placement | High |
| F-004 not applicable | `document_type.py` lines 167-216 | Code inspection -- 2-tuple return throughout | High |
| F-005 remediation (full) | `document_type.py` lines 153-165 | Code inspection -- `<purpose>` absent | High |
| F-006 non-finding confirmed | red-vuln-cwe843-analysis.md AS-2 | Static analysis with Python fnmatch verification | High |
| F-007 accepted | `document_type.py` lines 257-317 | Code inspection -- no null byte guard | High |
| F-008 resolved by design | red-vuln-cwe843-analysis.md RV-006 | Data flow trace through ast_commands.py | High |
| F-009 partial | red-vuln-cwe843-analysis.md RV-002 | Code inspection -- `_PARSER_MATRIX` lines 96-108 | High |
| RV-001 new finding | red-vuln-cwe843-analysis.md RV-001 | Static analysis -- three residual bypass conditions | High |
| RV-002 new finding | red-vuln-cwe843-analysis.md RV-002 | Code inspection -- SKILL_RESOURCE, TEMPLATE absent from matrix | High |
| RV-003 through RV-008 | red-vuln-cwe843-analysis.md | Static analysis with crafted input examples | Medium-High |

### Confidence Statement

**High confidence** for all findings with direct code evidence (code line references, function names, confirmed absence or presence of specific constructs).

**Medium confidence** for findings dependent on behavioral analysis of the CLI adapter (F-008, RV-006) where full CLI code was read by red-vuln but not independently verified by red-reporter. The red-vuln analysis provides function-level data flow traces that are internally consistent with the scope document and source code.

**Manual evidence verification recommended** for F-009 schema registry state (schema registration was inferred from F-009 description and red-vuln's enumeration of missing entries; direct schema_definitions.py inspection was not part of this report generation).

---

*Engagement: RED-0002*
*Report Version: 1.0.0*
*Agent: red-reporter*
*Date: 2026-02-24*
*Methodology: PTES Reporting Phase, OSSTMM Reporting Standards, NIST SP 800-115 Chapter 8*
*Constitutional Compliance: P-003 (no subagents), P-020 (user authority), P-022 (no deception)*
*Output: L0/L1/L2 per P-002 persistence requirement*
*Scope Compliance: Attested -- all operations within RED-0002 authorized boundaries*
