# RED-0002: CWE-843 Verification -- DocumentTypeDetector Engagement Scope

<!-- AGENT: red-lead | VERSION: 1.0.0 | DATE: 2026-02-24 | ENGAGEMENT: RED-0002 -->
<!-- METHODOLOGY: PTES Pre-Engagement Interactions + NIST SP 800-115 Chapter 3 -->

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Engagement overview, authorized activities, risk summary |
| [L1 Scope Document](#l1-scope-document) | Complete YAML scope, technique allowlists, target specifications |
| [L2 Methodology Rationale](#l2-methodology-rationale) | Methodology selection, coverage analysis, risk assessment |
| [Engagement Context](#engagement-context) | Prior work, threat model correlation, engagement objectives |
| [Attack Surface Definitions](#attack-surface-definitions) | Five authorized attack surfaces with precise boundaries |
| [Agent Authorization Matrix](#agent-authorization-matrix) | Authorized agents, techniques, and constraints |
| [Evidence Handling](#evidence-handling) | Storage, retention, destruction procedures |
| [Rules of Engagement](#rules-of-engagement) | Escalation, emergency stop, communication |
| [Authorization](#authorization) | User signature block |

---

## L0 Executive Summary

### Engagement Overview

This engagement authorizes **red-vuln** to perform static vulnerability analysis of the `DocumentTypeDetector` component in `src/domain/markdown_ast/document_type.py` and its downstream consumers. The analysis targets five specific attack surfaces identified during EN-002 (Document Type Ontology Hardening) implementation to verify whether CWE-843 (Type Confusion) vulnerabilities remain exploitable after the ontology hardening changes.

### Context

EN-002 expanded the `DocumentTypeDetector` from 12 to 63+ path patterns, replaced overly broad structural cues (`"---"`, `"<!--"`) with precise XML-tag and frontmatter cues, and fixed the `_normalize_path` embedded-marker confusion (F-001 CWE-22). A prior eng-security review (iteration-1) identified 9 findings (1 High, 3 Medium, 3 Low, 2 Informational). This engagement verifies the post-implementation residual risk.

### Authorized Activities

- Static analysis of source code and pattern lists
- Crafted input construction (path strings, file content strings) for analysis
- Pattern matching verification against `fnmatch` and `_match_recursive_glob`
- Data flow tracing through `detect()` to `_PARSER_MATRIX` to downstream parsers
- CWE classification and exploitability scoring of findings

### Activities NOT Authorized

- Modification of any source file
- Execution of exploit code against live systems
- Network access or external reconnaissance
- Fuzzing or automated testing execution (analysis-only engagement)
- Modification of test files or test execution

### Risk Summary

| Risk | Mitigation |
|------|------------|
| Analysis scope creep beyond target files | Explicit file allowlist in scope document |
| Findings interpreted as actionable exploits | Analysis-only framing; all findings are methodology guidance |
| False positives from theoretical-only attack paths | Exploitability scoring with realistic likelihood assessment required |

---

## L1 Scope Document

```yaml
scope:
  engagement_id: "RED-0002"
  version: "1.0"
  title: "CWE-843 Verification -- DocumentTypeDetector Post-EN-002"
  methodology: "PTES Pre-Engagement + NIST SP 800-115 (Static Analysis)"

  authorized_targets:
    - type: "source_file"
      value: "src/domain/markdown_ast/document_type.py"
      description: "Primary target -- DocumentTypeDetector, PATH_PATTERNS, STRUCTURAL_CUE_PRIORITY, _normalize_path, _path_matches_glob, _match_recursive_glob"
    - type: "source_file"
      value: "src/domain/markdown_ast/universal_document.py"
      description: "Downstream consumer -- _PARSER_MATRIX type-to-parser routing"
    - type: "source_file"
      value: "src/domain/markdown_ast/universal_parse_result.py"
      description: "Downstream consumer -- UniversalParseResult document_type field"
    - type: "source_file"
      value: "src/interface/cli/ast_commands.py"
      description: "CLI adapter -- ast_detect, _normalize_for_detection entry points"
    - type: "source_file"
      value: "src/infrastructure/internal/enforcement/pre_tool_enforcement_engine.py"
      description: "Read-only reference -- verify DocumentType usage in enforcement context"
    - type: "source_file"
      value: "src/domain/markdown_ast/__init__.py"
      description: "Read-only reference -- public API surface verification"

  technique_allowlist:
    # Static analysis techniques only -- no active exploitation
    - "T1592.004"  # Gather Victim Host Information: Client Configurations (static code analysis analog)
    - "STATIC-001"  # Source code review for type confusion patterns
    - "STATIC-002"  # Data flow analysis through classification pipeline
    - "STATIC-003"  # Pattern ordering analysis for first-match-wins semantics
    - "STATIC-004"  # Input crafting for theoretical attack path validation
    - "STATIC-005"  # Downstream impact analysis (type confusion propagation)

  time_window:
    start: "2026-02-24T00:00:00Z"
    end: "2026-02-24T23:59:59Z"
    note: "Single-session engagement"

  exclusion_list:
    - "tests/**"                           # No test file modification or execution
    - "src/domain/markdown_ast/schema_*"   # Schema files are out of scope (covered by eng-security F-008/F-009)
    - ".context/rules/**"                  # Framework rules are not targets
    - "docs/governance/**"                 # Governance documents are not targets
    - "*.py" # outside authorized_targets  # Any Python file not explicitly listed above

  rules_of_engagement:
    escalation_contact: "user (session owner)"
    emergency_stop: "Terminate agent session"
    communication_channel: "Claude Code session"
    social_engineering_authorized: false
    persistence_authorized: false
    exfiltration_authorized: false
    data_types_permitted:
      - "source code analysis results"
      - "CWE classifications"
      - "exploitability assessments"
    analysis_only: true
    no_code_modification: true
    no_test_execution: true
    finding_format: "CWE classification + CVSS 3.1 score + exploitability assessment"

  agent_authorizations:
    - agent: "red-vuln"
      authorization_level: "full"
      techniques_permitted:
        - "STATIC-001"
        - "STATIC-002"
        - "STATIC-003"
        - "STATIC-004"
        - "STATIC-005"
      constraints:
        - "Read-only access to authorized target files"
        - "No modification of any file except the output report"
        - "All findings must include CWE ID and exploitability score"
        - "Theoretical attack paths must be clearly labeled as theoretical"
        - "Must correlate findings with prior eng-security review (iteration-1)"

  evidence_handling:
    storage: "projects/PROJ-005-markdown-ast/work/EPIC-001-markdown-ast/FEAT-001-ast-strategy/EN-002-document-type-ontology-hardening/iteration-2/"
    output_file: "red-vuln-cwe843-analysis.md"
    retention_days: 90
    destruction_method: "git history retention (no separate destruction required)"

  signature:
    authorized_by: "PENDING -- requires user confirmation"
    date: "2026-02-24"
    confirmation: "PENDING"
```

---

## L2 Methodology Rationale

### Methodology Selection

**Selected: PTES Pre-Engagement Interactions + NIST SP 800-115 Chapter 4 (Technical Examination)**

| Methodology | Applicability | Selection Rationale |
|-------------|---------------|---------------------|
| PTES | Pre-engagement scoping, target definition, rules of engagement | Standard professional engagement scoping framework; provides the authorization structure |
| NIST SP 800-115 Ch. 4 | Technical examination (code review, static analysis) | Appropriate for source code vulnerability analysis without active exploitation |
| OSSTMM | Not selected for this engagement | OSSTMM operational security testing methodology is better suited for network/service testing; this engagement is purely static code analysis |

### Why Static Analysis Only

The target component (`DocumentTypeDetector`) is a pure function with no side effects, no network access, no file system writes, and no authentication. The attack surface is entirely in the logic of path normalization, pattern matching, and signal combination. Static analysis with crafted input construction provides complete coverage of the attack surface without requiring active exploitation.

### Coverage Analysis Against Engagement Objectives

| Objective | Attack Surface | Techniques | Coverage |
|-----------|---------------|------------|----------|
| AS-1: Path-based detection bypass | `_normalize_path()` lines 257-317 | STATIC-001, STATIC-002, STATIC-004 | Full -- all code paths in `_normalize_path` are analyzable statically |
| AS-2: `fnmatch` wildcard exploitation | `_path_matches_glob()` lines 320-336, `_match_recursive_glob()` lines 339-384 | STATIC-001, STATIC-004 | Full -- fnmatch behavior is deterministic and documented |
| AS-3: Structural cue content override | `_detect_from_structure()` lines 233-249, `detect()` signal combination lines 197-216 | STATIC-001, STATIC-002 | Full -- linear scan with string containment is fully analyzable |
| AS-4: UNKNOWN fallback abuse | `detect()` return path lines 212-216, `_PARSER_MATRIX` UNKNOWN entry | STATIC-002, STATIC-005 | Full -- data flow from UNKNOWN through parser matrix is traceable |
| AS-5: First-match-wins ordering confusion | `PATH_PATTERNS` list lines 74-145 (63+ entries), `_detect_from_path()` lines 218-231 | STATIC-003, STATIC-004 | Full -- pattern ordering is a static property of the list |

### Prior Work Correlation

This engagement builds on the eng-security review (iteration-1) which identified 9 findings. The engagement objectives map to prior findings as follows:

| Attack Surface | Prior Finding | Prior Status | This Engagement's Focus |
|---------------|---------------|--------------|------------------------|
| AS-1 | F-001 (High, CWE-22/CWE-843) | Remediated in EN-002 (idx > 0 check + already_relative guard) | Verify remediation completeness; identify residual bypass vectors |
| AS-2 | F-006 (Low, CWE-20) | Confirmed non-exploitable by eng-security | Verify against the expanded 63+ pattern set; analyze `_match_recursive_glob` edge cases |
| AS-3 | F-002 (Medium, CWE-843), F-005 (Low, CWE-843) | F-002 remediated (## Status cue removed); F-005 accepted (purpose cue retained) | Verify remaining cues cannot override path classification; test new cues against full corpus |
| AS-4 | F-008 (Info), F-009 (Info) | Design-only findings; no code changes | Trace UNKNOWN through _PARSER_MATRIX to verify safe downstream behavior |
| AS-5 | F-003 (Medium, CWE-697) | Ordering documented as correct | Analyze the full 63+ pattern list for type confusion cases between tiers |

---

## Engagement Context

### Target Component Architecture

```
                    detect(file_path, content)
                              |
                    +---------+---------+
                    |                   |
           _normalize_path()    _detect_from_structure()
                    |                   |
           _detect_from_path()         (fallback only)
                    |                   |
           _path_matches_glob()         |
                    |                   |
                    +-------+-----------+
                            |
                    Signal Combination
                    (path authoritative)
                            |
                    DocumentType enum
                            |
                    _PARSER_MATRIX
                    (universal_document.py)
                            |
                    Type-specific parsers
                    (schema selection)
```

### Files in Scope with Line Ranges

| File | Lines | Component | Role in Analysis |
|------|-------|-----------|-----------------|
| `document_type.py` | 1-385 | DocumentType, DocumentTypeDetector, _normalize_path, _path_matches_glob, _match_recursive_glob | Primary target -- all 5 attack surfaces |
| `universal_document.py` | 92-108 | _PARSER_MATRIX | AS-4, AS-5 downstream impact -- type determines which parsers run |
| `universal_parse_result.py` | 45-71 | UniversalParseResult | AS-4 downstream impact -- type stored in frozen result |
| `ast_commands.py` | 598-735 | ast_detect, _normalize_for_detection | AS-1 entry point -- CLI passes file_path to detect() |
| `pre_tool_enforcement_engine.py` | 510-514 | Reference only | Verify no additional DocumentType consumption |
| `__init__.py` | -- | Public exports | Verify API surface |

---

## Attack Surface Definitions

### AS-1: Path-Based Detection Bypass

**Objective:** Determine whether crafted paths can trick `_normalize_path` into extracting incorrect repo-relative portions after the F-001 remediation.

**Scope Boundary:**
- `_normalize_path()` function (lines 257-317)
- Root markers list (lines 281-292)
- The `already_relative` check (line 293)
- The `_ROOT_FILES` basename extraction (lines 304-315)

**Specific Questions for red-vuln:**
1. Can a path that starts with a root marker but contains another embedded root marker cause incorrect extraction? (e.g., `skills/evil/projects/victim/work/entity.md`)
2. Does the `already_relative` guard at line 293 cover all cases where the path starts with a marker?
3. Can the `_ROOT_FILES` basename extraction at lines 304-315 be abused to classify an arbitrary file as a root-level framework config?
4. What happens with mixed separators (forward + backslash) combined with root marker embedding?
5. What is the residual risk after F-001 remediation for paths originating from `ast_detect` CLI entry point?

**CWE Focus:** CWE-22 (Path Traversal), CWE-843 (Type Confusion via path manipulation)

---

### AS-2: `fnmatch` Wildcard Exploitation

**Objective:** Determine whether filenames containing glob-special characters (`*`, `?`, `[`, `]`) can cause unintended pattern matches in the expanded 63+ pattern set.

**Scope Boundary:**
- `_path_matches_glob()` function (lines 320-336)
- `_match_recursive_glob()` function (lines 339-384)
- `fnmatch.fnmatch()` stdlib behavior with special characters in path argument
- All 63+ entries in `PATH_PATTERNS` (lines 74-145)

**Specific Questions for red-vuln:**
1. Confirm that `fnmatch.fnmatch(path, pattern)` treats special characters in the path argument as literals (eng-security F-006 conclusion).
2. Analyze the `_match_recursive_glob` segment-by-segment matching (lines 362-382): does `fnmatch.fnmatch(ps, pp)` on individual segments introduce any new risk when path segments contain `[` or `]`?
3. Can a path with `**` in its actual filename trick `_path_matches_glob` into taking the recursive branch incorrectly?
4. Test the `len(parts) != 2` fallback at line 354-356: can a pattern or path with multiple `**` segments produce unexpected matches?
5. With 63+ patterns now, are there any patterns where `*` (single-star, non-recursive) could accidentally cross a directory boundary in `fnmatch`?

**CWE Focus:** CWE-20 (Improper Input Validation), CWE-843 (Type Confusion via wildcard manipulation)

---

### AS-3: Structural Cue Content Override

**Objective:** Determine whether file content can cause structural cues to override the correct path-based classification, or cause misclassification in the fallback path.

**Scope Boundary:**
- `STRUCTURAL_CUE_PRIORITY` list (lines 153-165, 6 entries)
- `_detect_from_structure()` method (lines 233-249)
- Signal combination logic in `detect()` (lines 197-216)
- M-14 dual-signal warning generation (lines 200-209)

**Specific Questions for red-vuln:**
1. Can an attacker craft file content that triggers a high-priority structural cue (`<identity>`, `<methodology>`) to produce a false M-14 warning on a correctly path-classified file? What is the impact of such a warning?
2. For files that fall through path matching to structure-only detection: which of the 6 remaining cues have the highest false-positive rate across realistic Jerry repository content?
3. Can the `> **Type:**` cue (line 158) be triggered by content that is NOT worktracker blockquote frontmatter? (e.g., markdown quoting a discussion about types)
4. Can the `<!-- L2-REINJECT` cue (line 160) be triggered by content that discusses L2-REINJECT markers rather than containing actual markers?
5. Does the removal of `"---"` and `"<!--"` cues (EN-002 remediation) fully eliminate the BUG-004 root cause? Are there any residual broad-match cues?

**CWE Focus:** CWE-843 (Type Confusion via content injection), CWE-345 (Insufficient Verification of Data Authenticity)

---

### AS-4: UNKNOWN Fallback Abuse

**Objective:** Determine whether the UNKNOWN classification can be weaponized to bypass schema validation or cause incorrect downstream behavior.

**Scope Boundary:**
- `detect()` return path for UNKNOWN (lines 212-216)
- `_PARSER_MATRIX` UNKNOWN entry in `universal_document.py` (line 107: `DocumentType.UNKNOWN: {"nav"}`)
- `UniversalDocument.parse()` behavior when `document_type == UNKNOWN` (lines 158-159)
- `ast_detect` CLI output for UNKNOWN files

**Specific Questions for red-vuln:**
1. When UNKNOWN is returned, `_PARSER_MATRIX` invokes only the `nav` parser. Is there any scenario where UNKNOWN + nav-only parsing produces a security-relevant misinterpretation?
2. Can an attacker force a file that SHOULD be classified (e.g., an agent definition) to fall through to UNKNOWN by crafting a path that avoids all 63+ patterns AND avoids all structural cues? What would the impact be?
3. Does the `UniversalDocument.parse()` explicit type override path (line 150: `if document_type is not None`) bypass all detection logic? If a caller passes `document_type=UNKNOWN` explicitly, what parsers run?
4. If `detect()` returns UNKNOWN and the file is passed to `jerry ast validate` without a `--schema` flag, what happens? Is schema validation skipped (safe) or does it produce an error?

**CWE Focus:** CWE-843 (Type Confusion via forced misclassification), CWE-754 (Improper Check for Exceptional Conditions)

---

### AS-5: First-Match-Wins Ordering Confusion

**Objective:** Determine whether the ordering of the 63+ `PATH_PATTERNS` entries creates type confusion opportunities where a file could match an incorrect pattern before reaching its correct pattern.

**Scope Boundary:**
- Complete `PATH_PATTERNS` list (lines 74-145, 63+ entries, 5 tiers)
- `_detect_from_path()` iteration (lines 218-231)
- Tier boundaries: Tier 1 (lines 75-82), Tier 2 (lines 83-96), Tier 3 (lines 97-109), Tier 4 (lines 110-117), Tier 5 (lines 118-144)

**Specific Questions for red-vuln:**
1. Identify all cases where a file path could match a Tier N pattern AND a Tier M pattern (M > N), resulting in a different classification than intended. For each case, assess whether the Tier N classification is correct or incorrect.
2. Specifically analyze the `skills/*/*.md` catch-all (line 96, Tier 2): which files does this capture that are NOT captured by more specific Tier 2 patterns? Is SKILL_RESOURCE the correct classification for all of them?
3. Analyze the `docs/*.md` catch-all (line 141, Tier 5): can this capture files that should be classified as something other than KNOWLEDGE_DOCUMENT?
4. Analyze the `.context/templates/**/*.md` catch-all (line 123, Tier 5): can this capture files that should be classified as STRATEGY_TEMPLATE but are not under the `adversarial/` subdirectory?
5. Is there any path that matches BOTH `projects/*/work/**/*.md` (WORKTRACKER_ENTITY) AND `projects/*/orchestration/**/*.md` (ORCHESTRATION_ARTIFACT)? The directory structure `projects/*/work/` and `projects/*/orchestration/` are siblings, but could a symlink or unusual nesting create ambiguity?
6. For each of the 13 DocumentType values, verify that at least one PATH_PATTERN maps to it. Identify any enum values that are reachable ONLY via structural cues (no path pattern).

**CWE Focus:** CWE-843 (Type Confusion via ordering), CWE-697 (Incorrect Comparison -- pattern precedence)

---

## Agent Authorization Matrix

| Agent | Authorization | Techniques | Constraints |
|-------|--------------|------------|-------------|
| red-vuln | AUTHORIZED | STATIC-001 through STATIC-005 | Read-only analysis; no code modification; findings require CWE + CVSS |
| red-lead | AUTHORIZED (this document) | Scope definition only | Oversight role; does not analyze code |
| red-recon | NOT AUTHORIZED | -- | No reconnaissance phase needed for static code analysis |
| red-exploit | NOT AUTHORIZED | -- | No exploitation; analysis-only engagement |
| red-privesc | NOT AUTHORIZED | -- | No privilege escalation applicable |
| red-lateral | NOT AUTHORIZED | -- | No lateral movement applicable |
| red-persist | NOT AUTHORIZED | -- | RoE-gated; not applicable |
| red-exfil | NOT AUTHORIZED | -- | RoE-gated; not applicable |
| red-social | NOT AUTHORIZED | -- | RoE-gated; not applicable |
| red-infra | NOT AUTHORIZED | -- | No infrastructure needed |
| red-reporter | CONDITIONALLY AUTHORIZED | Report generation | May be invoked after red-vuln completes for formal report if requested |

---

## Evidence Handling

| Attribute | Value |
|-----------|-------|
| Storage location | `projects/PROJ-005-markdown-ast/work/EPIC-001-markdown-ast/FEAT-001-ast-strategy/EN-002-document-type-ontology-hardening/iteration-2/` |
| Primary output file | `red-vuln-cwe843-analysis.md` |
| Evidence format | Markdown with CWE classifications, CVSS scores, data flow traces, and crafted input examples |
| Retention | 90 days (standard project retention) |
| Destruction method | Git history retention; no separate destruction required |
| Classification | Internal -- engagement findings for development team consumption |

---

## Rules of Engagement

### Engagement Rules

| Rule | Specification |
|------|---------------|
| Analysis only | No active exploitation, no code modification, no test execution |
| File access | Read-only access to 6 authorized target files listed in scope |
| Output | Single analysis report written to `iteration-2/red-vuln-cwe843-analysis.md` |
| Finding format | Each finding must include: CWE ID, CVSS 3.1 vector and score, exploitability assessment (Theoretical / Demonstrable / Confirmed), affected function and line range, crafted input example, downstream impact via _PARSER_MATRIX |
| Correlation | All findings must be correlated with prior eng-security findings (F-001 through F-009) |
| Residual risk | For each prior finding that was remediated, red-vuln must assess whether the remediation is complete |

### Escalation Procedures

| Condition | Action |
|-----------|--------|
| Finding exceeds CVSS 7.0 (High) | Flag in report with URGENT marker; recommend immediate remediation before EN-002 completion |
| Finding contradicts eng-security assessment | Document discrepancy with evidence; both assessments remain valid pending resolution |
| Scope boundary reached | Document as "out of scope, requires separate engagement" in findings |
| Ambiguity in attack surface definition | Reference this scope document; if still ambiguous, proceed with the more restrictive interpretation |

### Emergency Stop Conditions

| Condition | Action |
|-----------|--------|
| Agent attempts to modify source files | Halt immediately; this violates analysis-only constraint |
| Agent attempts network access | Halt immediately; no network access authorized |
| Agent scope exceeds authorized target files | Halt and re-read scope document |

---

## Authorization

### Signature Block

```yaml
authorization:
  engagement_id: "RED-0002"
  authorized_by: "PENDING -- user must confirm"
  date: "2026-02-24"
  confirmation: |
    I authorize red-vuln to perform static vulnerability analysis of the
    DocumentTypeDetector component within the scope defined in this document.
    Analysis is read-only with no code modification, no test execution, and
    no active exploitation. Findings will be documented in
    iteration-2/red-vuln-cwe843-analysis.md with CWE classifications and
    exploitability scores.
  scope_version: "1.0"
  methodology: "PTES + NIST SP 800-115 (Static Analysis)"
```

**ACTION REQUIRED:** This scope document requires your explicit authorization before red-vuln can proceed. Please confirm by stating that you authorize this engagement within the defined scope.

---

*Engagement: RED-0002*
*Scope Version: 1.0*
*Agent: red-lead*
*Date: 2026-02-24*
*Methodology: PTES Pre-Engagement Interactions, NIST SP 800-115 Chapter 3-4*
*Constitutional Compliance: P-003 (no subagents), P-020 (user authority), P-022 (no deception)*
*Output: L0/L1/L2 per P-002 persistence requirement*
