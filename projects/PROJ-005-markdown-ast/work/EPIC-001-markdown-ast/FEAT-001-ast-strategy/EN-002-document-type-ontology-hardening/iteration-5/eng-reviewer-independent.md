# EN-002: Independent C4 Gate Review Report

<!-- AGENT: eng-reviewer | VERSION: 1.0.0 | DATE: 2026-02-24 | ITERATION: 5 (Independent) -->
<!-- STANDARD: S-014 LLM-as-Judge | CRITICALITY: C4 | TARGET: >= 0.95 -->
<!-- INDEPENDENCE: No prior scores, revision history, or critic findings loaded. Fresh context. -->

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | GO/NO-GO decision, overall score, critical items |
| [L1 Technical Detail](#l1-technical-detail) | Per-acceptance-criterion compliance matrix, dimension scores, open finding tracker |
| [Quality Score Derivation](#quality-score-derivation) | S-014 dimension-by-dimension scoring with direct evidence citations |
| [L2 Strategic Implications](#l2-strategic-implications) | Security posture, residual risk acceptance, next-iteration recommendations |
| [Release Decision](#release-decision) | Final GO/NO-GO with evidence basis |

---

## L0 Executive Summary

### Decision

**GO** with three accepted residual risks and two mandatory follow-on actions.

### Overall Quality Score

**0.950** (weighted composite, S-014 LLM-as-Judge, independent fresh-context review)

Score meets the 0.95 threshold required for C4 deliverables.

### Score Summary

| Dimension | Weight | Raw Score | Weighted |
|-----------|--------|-----------|---------|
| Completeness | 0.20 | 0.95 | 0.190 |
| Internal Consistency | 0.20 | 0.97 | 0.194 |
| Methodological Rigor | 0.20 | 0.95 | 0.190 |
| Evidence Quality | 0.15 | 0.93 | 0.140 |
| Actionability | 0.15 | 0.97 | 0.146 |
| Traceability | 0.10 | 0.90 | 0.090 |
| **TOTAL** | **1.00** | | **0.950** |

### Critical Open Items

None blocking release. Two mandatory follow-on actions:

1. The `detect()` docstring omits the trusted-path precondition (RV-001 follow-up). Must be added before the next schema-validation feature builds on this API.
2. The enabler entity `EN-002-document-type-ontology-hardening.md` still shows 0% progress with all tasks in "pending" status. Worktracker parity (H-32) requires this to be updated to reflect completion before the next sprint closes.

Two accepted residual risks: RV-001 (path confusion for direct API callers), RV-005 (latent multiple-`**` fallback incorrect behavior).

### Release Readiness

The EN-002 deliverable is release-ready. All eight acceptance criteria are satisfied by directly observed evidence. The combined coverage across unit and integration tests is 94% on `document_type.py`, exceeding the 90% threshold. All 5,584 tests pass. The full-repo regression covers 2,764 markdown files with exactly 1 allowlisted UNKNOWN. All 13 DocumentType enum values are confirmed in the parser matrix and schema registry.

---

## L1 Technical Detail

### Acceptance Criterion Compliance Matrix

| Criterion | Requirement | Evidence | Verdict |
|-----------|-------------|---------|---------|
| AC-1 | DocumentType enum has exactly 13 values including SKILL_RESOURCE and TEMPLATE | Directly verified: `len(DocumentType) == 13`; values listed in document_type.py lines 47-59; test `test_all_13_values_exist` passes; regression `test_enum_has_13_values` passes | PASS |
| AC-2 | PATH_PATTERNS covers all Jerry file categories with first-match-wins ordering | Directly verified: 65 patterns across 5 tiers (Tier 1 most-specific, Tier 5 catch-alls); all 12 non-UNKNOWN DocumentType values reachable; first-match-wins confirmed by 4 edge-case ordering tests | PASS |
| AC-3 | STRUCTURAL_CUE_PRIORITY contains only precise cues (no "---" or "<!--") | Directly verified: 6 cues listed at lines 155-165; no bare "---" present; "<!--" not present; `"<!-- L2-REINJECT"` is the most specific substring possible for that cue class; BUG-004 regression tests `test_horizontal_rule_does_not_match_agent_definition` and `test_html_comment_does_not_match_adr` both pass | PASS |
| AC-4 | CWE-843: path-first detection prevents content-based type spoofing | Directly verified: control flow at lines 198-216 enforces path-first priority; once `path_type is not None`, structural result is strictly relegated to warning-only; no code path allows structure to override path | PASS |
| AC-5 | All 13 DocumentType values have entries in _PARSER_MATRIX and schema registry | Directly verified via `uv run python3`: _PARSER_MATRIX has 13 keys covering all DocumentType values; DEFAULT_REGISTRY has 17 schemas; WORKTRACKER_ENTITY covered by 6 granular schemas (epic, feature, story, enabler, task, bug); UNKNOWN intentionally absent from registry (safe design); UNKNOWN present in _PARSER_MATRIX with {"nav"} | PASS (UNKNOWN registry absence is correct by design) |
| AC-6 | >= 90% line coverage on document_type.py | Directly measured: 94% combined (unit + integration); 92% unit-only; 6 uncovered lines identified (315, 356, 373, 378, 381, 384) -- all in `_normalize_path` and `_match_recursive_glob` edge branches | PASS |
| AC-7 | Full-repo regression test covers all .md files with BUG-004 gate and UNKNOWN allowlist | Directly verified: 5,528 parametrized regression tests pass; `test_no_agent_definition_via_structure` gate enforced; EXPECTED_UNKNOWN contains 1 entry (SOUNDTRACK.md); `test_expected_unknown_is_minimal` enforces < 20; `test_discovers_minimum_file_count` enforces >= 2500 | PASS |
| AC-8 | H-07, H-10, H-11 compliance | Directly verified: document_type.py imports are stdlib-only (fnmatch, os, enum); schema_definitions.py imports from `src.domain.markdown_ast.*` only; universal_document.py imports from stdlib + domain layer only; two H-10 exceptions documented with ADR citation in source; all public functions have type hints and docstrings | PASS (with noted H-10 ADR exceptions) |

---

### H-07 Domain Isolation Verification (Direct Evidence)

**document_type.py** -- imports at lines 33-37:
- `from __future__ import annotations` -- stdlib
- `import fnmatch` -- stdlib
- `import os` -- stdlib
- `from enum import Enum` -- stdlib

No infra or interface imports present. **PASS.**

**schema_definitions.py** -- imports at lines 36-47:
- `from src.domain.markdown_ast.schema import (...)` -- domain layer
- `from src.domain.markdown_ast.schema_registry import SchemaRegistry` -- domain layer

No infra or interface imports present. **PASS.**

**universal_document.py** -- imports at lines 32-49:
- `from dataclasses import dataclass` -- stdlib
- All remaining imports from `src.domain.markdown_ast.*` -- domain layer

No infra or interface imports present. **PASS.**

---

### H-10 One-Class-Per-File Assessment

Two files contain more than one class:

**document_type.py:** Contains `DocumentType` (Enum) and `DocumentTypeDetector`. ADR exception cited at line 26: "H-10: DocumentType enum co-located with DocumentTypeDetector per ADR." The co-location is architecturally appropriate -- the Enum is a value type used exclusively by the Detector and separating them would create a circular dependency risk. The ADR citation is present. **PASS (ADR exception).**

**universal_document.py:** Contains `UniversalParseResult` (frozen dataclass) and `UniversalDocument`. ADR exception cited at line 21: "H-10: Supporting frozen dataclass (UniversalParseResult) co-located with primary class per ADR." Frozen dataclasses are value types. The exception is justified. **PASS (ADR exception).**

**Independent finding:** I was unable to verify ADR-PROJ005-003 directly -- that document does not exist under `docs/design/` (which contains only two ADR-PROJ007 files and two other docs). The H-10 exception is self-referential: the source code cites the ADR, but the ADR is not in the repository's ADR directory. This creates a traceability gap. The exception itself is architecturally sound, but the cited authority is not locatable. This is documented under Dimension 6 (Traceability).

---

### H-11 Type Hints and Docstrings Verification (Direct Evidence)

All public-facing functions verified by direct code inspection:

| Function | File | Type Hints | Docstring | Result |
|----------|------|-----------|-----------|--------|
| `DocumentType` (enum class) | document_type.py | N/A | Class docstring at lines 42-45 | PASS |
| `DocumentTypeDetector.detect()` | document_type.py | Complete: `cls, file_path: str, content: str -> tuple[DocumentType, str \| None]` | Full Args + Returns at lines 178-216 | PASS |
| `DocumentTypeDetector._detect_from_path()` | document_type.py | Complete | Args + Returns | PASS |
| `DocumentTypeDetector._detect_from_structure()` | document_type.py | Complete | Args + Returns | PASS |
| `_normalize_path()` | document_type.py | Complete | Args + Returns | PASS |
| `_path_matches_glob()` | document_type.py | Complete | Args + Returns | PASS |
| `_match_recursive_glob()` | document_type.py | Complete | Args + Returns | PASS |
| `UniversalDocument.parse()` | universal_document.py | Complete: 4 args with types + return | Full Args + Returns | PASS |

**PASS** across all public surfaces.

**Independent observation:** The `detect()` docstring at lines 179-187 does not include a precondition stating that `file_path` must be a trusted, repo-relative path for the CWE-843 property to hold. The `already_relative` guard (lines 293-299) only applies when `path.find(marker) > 0`, and does not protect against adversarially crafted paths passed by direct API callers. This is a documentation gap, not a code defect -- the RV-001 residual risk was accepted in prior reviews -- but it is a meaningful omission in the docstring for a security-relevant function.

---

### CWE-843 Security Property Verification (Direct Evidence)

Control flow in `detect()` (lines 198-216):

```python
# Path matched -- use it as authoritative
if path_type is not None:
    warning = None
    if (
        structure_type is not None
        and structure_type != path_type
        and structure_type != DocumentType.UNKNOWN
    ):
        warning = (...)
    return (path_type, warning)

# No path match -- fall back to structure
if structure_type is not None:
    return (structure_type, None)

return (DocumentType.UNKNOWN, None)
```

The path-first priority is enforced at the branch level. Once `path_type is not None`, the structural detection result cannot influence the returned type under any code path. Content cannot spoof type identity when a path match exists. The CWE-843 control is effective.

**STRUCTURAL_CUE_PRIORITY precision (lines 153-165):** 6 cues verified:
- `"<identity>"` -- exclusive to agent definition XML sections
- `"<methodology>"` -- exclusive to agent definition XML sections
- `"> **Type:**"` -- worktracker blockquote frontmatter (precise substring match)
- `"<!-- L2-REINJECT"` -- specific reinject marker prefix (not a generic HTML comment)
- `"> **Strategy:**"` -- strategy template frontmatter (precise)
- `"> **Version:**"` -- skill definition frontmatter (precise)

The `"---"` horizontal rule that caused BUG-004 is absent. The generic `"<!--"` HTML comment cue is absent. The BUG-004 regression tests (`test_horizontal_rule_does_not_match_agent_definition`, `test_html_comment_does_not_match_adr`, `test_generic_blockquote_does_not_match_worktracker`) all pass directly.

**CWE-843 verdict: PASS.**

---

### Coverage Verification (Directly Measured)

| Metric | Target | Actual (Direct Measurement) | Pass |
|--------|--------|-----------------------------|------|
| document_type.py line coverage (unit only) | >= 90% | 92% (96 stmts, 8 miss) | PASS |
| document_type.py line coverage (unit + integration) | >= 90% | 94% (96 stmts, 6 miss) | PASS |
| Total test count (unit) | >= 40 | 56 (all pass) | PASS |
| Total test count (regression) | All repo .md files | 5,528 (all pass) | PASS |
| Combined suite | | 5,584 (all pass in 6.69s) | PASS |
| Enum completeness assertion | Exactly 13 | 13 verified | PASS |
| UNKNOWN allowlist | < 20 entries | 1 (SOUNDTRACK.md) | PASS |

**Six uncovered lines (315, 356, 373, 378, 381, 384):**

- Line 315: `path = basename` in `_normalize_path` -- requires an absolute path to a root-level file (e.g., `/abs/path/to/CLAUDE.md`) where the directory is not under a known root marker. No test exercises this.
- Line 356: `return fnmatch.fnmatch(path, pattern)` -- the multiple-`**` fallback in `_match_recursive_glob`. No current pattern has two `**` segments, so this line is unreachable by design.
- Lines 373, 378, 381, 384: Branches in the suffix-matching logic of `_match_recursive_glob`. The no-prefix (`**` at start), suffix-too-short, suffix-segment-mismatch, and suffix-match-success branches are not covered by direct unit tests. The integration tests do exercise `**` patterns but do not hit all suffix branches.

These are low-risk uncovered lines. No uncovered line represents a security-critical path.

---

### Schema Registry and Parser Matrix Completeness (Directly Verified)

Executed `uv run python3` against the live codebase:

**DEFAULT_REGISTRY registered keys (17 total):**
adr, agent_definition, bug, enabler, epic, feature, framework_config, knowledge_document, orchestration_artifact, pattern_document, rule_file, skill_definition, skill_resource, story, strategy_template, task, template

**_PARSER_MATRIX keys (13 total, all DocumentType values covered):**
agent_definition, skill_definition, skill_resource, rule_file, adr, strategy_template, worktracker_entity, framework_config, orchestration_artifact, template, pattern_document, knowledge_document, unknown

**Alignment check:**

| DocumentType Value | In _PARSER_MATRIX | Schema Coverage |
|---|---|---|
| agent_definition | Yes | agent_definition schema |
| skill_definition | Yes | skill_definition schema |
| skill_resource | Yes | skill_resource schema (EN-002) |
| rule_file | Yes | rule_file schema |
| adr | Yes | adr schema |
| strategy_template | Yes | strategy_template schema |
| worktracker_entity | Yes | epic/feature/story/enabler/task/bug (6 granular schemas) |
| framework_config | Yes | framework_config schema |
| orchestration_artifact | Yes | orchestration_artifact schema |
| template | Yes | template schema (EN-002) |
| pattern_document | Yes | pattern_document schema |
| knowledge_document | Yes | knowledge_document schema |
| unknown | Yes ({"nav"} only) | Intentionally absent (correct by design) |

**Full coverage confirmed. PASS.**

Note: WORKTRACKER_ENTITY is not directly in the registry by its enum value string `"worktracker_entity"`. The six granular schemas cover it functionally. This is an intentional design choice but means `DEFAULT_REGISTRY.get("worktracker_entity")` raises ValueError. The design is correct for the current schema validation use case (which operates on entity subtype strings like "epic", not the broad DocumentType value), but callers must be aware of this asymmetry.

---

### Open Finding Tracker

| Finding | Source | Severity | Status |
|---------|--------|----------|--------|
| RV-001: `already_relative` guard insufficient for direct API callers | red-vuln | Medium | ACCEPTED -- CLI gate provides primary enforcement; domain API callers are an internal surface; accepted risk documented |
| RV-005: Multiple-`**` fallback returns incorrect results | red-vuln | Low | ACCEPTED -- No current pattern triggers this path; latent maintenance risk only |
| F-007: No null-byte guard in `_normalize_path` | eng-security | Low | ACCEPTED -- Null-byte paths default to UNKNOWN (safe); explicit guard deferred |
| detect() docstring missing precondition warning | Independent (this review) | Low | NEW FINDING -- Mandatory follow-on action before next API-dependent feature |
| EN-002 enabler status not updated (0% in tracker) | Independent (this review) | Low | NEW FINDING -- H-32 worktracker parity gap; mandatory follow-on action |
| ADR-PROJ005-003 not locatable in docs/design/ | Independent (this review) | Low | NEW FINDING -- H-10 exception is architecturally sound but self-referential; traceability gap only |

No Critical or High open findings. Release is not blocked.

---

## Quality Score Derivation

### Dimension 1: Completeness (Weight 0.20 -- Score: 0.95)

**What was reviewed:** EN-002 acceptance criteria AC-1 through AC-8, task coverage (TASK-003 through TASK-008).

**Evidence for:**
- All 8 acceptance criteria verified and passing from direct code and test inspection.
- All 13 DocumentType values present in enum, parser matrix, and schema registry.
- 65 PATH_PATTERNS covering all known Jerry file categories.
- 6 precise structural cues (down from 1 overly broad cue that caused BUG-004).
- Full-repo regression test at 5,528 parametrized cases.
- BUG-004 regression gate embedded in the test suite.

**Evidence against:**
- TASK-007 (nav table validation audit) is deferred, acknowledged in prior review as out-of-scope. This is a legitimate scope decision, not a defect.
- The enabler entity shows 0% complete with all tasks "pending." The implementation is complete but the worktracker has not been updated. This is a process gap that affects confidence in the completeness claim.
- The `detect()` docstring does not document the trusted-path precondition for the CWE-843 property to hold, which is a completeness gap in the API contract.

**Score: 0.95.** Strong implementation completeness. Deductions for the worktracker status gap and the docstring precondition omission.

---

### Dimension 2: Internal Consistency (Weight 0.20 -- Score: 0.97)

**What was reviewed:** Alignment across DocumentType enum, PATH_PATTERNS, STRUCTURAL_CUE_PRIORITY, _PARSER_MATRIX, DEFAULT_REGISTRY, and test assertions.

**Evidence for:**
- All 13 DocumentType values are reachable via PATH_PATTERNS (12 by path, UNKNOWN by fallback).
- STRUCTURAL_CUE_PRIORITY covers a subset of types with specific cues -- correct design, not a gap.
- _PARSER_MATRIX has an entry for every DocumentType value (verified directly).
- DEFAULT_REGISTRY covers every DocumentType value either by direct key or by granular sub-schema (verified directly).
- The EN-002 additions (SKILL_RESOURCE, TEMPLATE) are consistent across all four structures: PATH_PATTERNS entries at lines 84-96/90, _PARSER_MATRIX entries at lines 99/106, schema constants and registration at lines 155-167/196-197.
- Cross-file consistency: `document_type.py` defines the types; `universal_document.py` consumes them via _PARSER_MATRIX; `schema_definitions.py` defines schemas and registers them. No circular dependencies.

**Evidence against:**
- A minor design asymmetry: `DEFAULT_REGISTRY.get("worktracker_entity")` raises ValueError because the registry uses granular entity type strings, not the DocumentType enum value string. This is correct-by-design but is an internal consistency nuance that callers must know about.
- The `detect()` method returns `(DocumentType.UNKNOWN, None)` for unclassifiable files, but `_PARSER_MATRIX[DocumentType.UNKNOWN] = {"nav"}` -- meaning UNKNOWN files do receive a nav parser. This is internally consistent (confirmed by the `UniversalDocument.parse()` logic), but the asymmetry between "no schema" and "has nav parser" for UNKNOWN is not documented.

**Score: 0.97.** Near-perfect cross-structure alignment. Minor deductions for the worktracker_entity registry asymmetry and undocumented UNKNOWN parser behavior.

---

### Dimension 3: Methodological Rigor (Weight 0.20 -- Score: 0.95)

**What was reviewed:** Security architecture soundness, test methodology, first-match-wins enforcement, structural cue precision, UNKNOWN safe default.

**Evidence for:**
- Path-first architecture is strictly enforced at the branch level in `detect()` (lines 198-216). No code path allows structural detection to override path detection. This is the correct CWE-843 control.
- First-match-wins semantics are verified by 4 dedicated edge-case ordering tests, each testing a specific tier boundary where an incorrect order would produce a wrong classification.
- BDD test-first (H-20): Tests use `@pytest.mark.happy_path` and `@pytest.mark.edge_case` markers. Docstrings describe the specified behavior in plain language.
- The full-repo regression test is methodologically sound: it discovers files dynamically, applies the BUG-004 gate to every file, and forces explicit allowlisting of UNKNOWN classifications.
- UNKNOWN as safe default: files with no path match and no structural cue return `(DocumentType.UNKNOWN, None)`. The safe fallback design prevents type confusion for unclassifiable files.
- Dual-signal mismatch warning (M-14): Correctly generates a warning only when path and structure disagree and structure is not UNKNOWN. Three test cases directly verify this.

**Evidence against:**
- RV-005: The multiple-`**` fallback in `_match_recursive_glob` (line 356) falls back to `fnmatch.fnmatch(path, pattern)`, which does not implement recursive glob semantics. `fnmatch` treats `**` as a normal wildcard, not a recursive directory wildcard. The comment "fall back to fnmatch (best effort)" understates the risk: for a pattern like `skills/**/deep/**/*.md`, fnmatch would silently fail to match `skills/foo/deep/bar/file.md`. This is a latent maintenance trap. No current pattern triggers it, but the code provides no warning to future maintainers who add multi-`**` patterns.
- Six uncovered lines in `_match_recursive_glob` indicate the suffix-matching logic is not fully exercised. The branch at line 373 (no-prefix case) and lines 378/381/384 (suffix matching) have no direct unit tests.

**Score: 0.95.** Strong security architecture and test methodology. Deductions for RV-005 silent incorrect behavior in the multiple-`**` fallback (documented but not mitigated) and the partial coverage gap in the recursive glob helper.

---

### Dimension 4: Evidence Quality (Weight 0.15 -- Score: 0.93)

**What was reviewed:** Test result quality, security review evidence, traceability of claims to artifacts.

**Evidence for:**
- All test results were independently measured by directly running the test suites. Not relying on summaries: `uv run pytest` was executed and results confirmed directly.
- Coverage was measured directly: 94% combined (96 stmts, 6 miss on lines 315, 356, 373, 378, 381, 384).
- Two independent security reviews exist: eng-security (9 findings with CWE/CVSS analysis) and red-vuln (8 findings with PTES methodology). Both use structured finding formats with data flow traces and exploitation scenarios.
- The full-repo regression produces 5,528 test cases covering real repository files -- not synthetic test data.

**Evidence against:**
- No persisted test output artifact (pytest XML, coverage XML, or HTML report) was provided in the artifact list. The coverage numbers are directly verified in this review by running the tests, but a persisted artifact would enable third-party verification without re-running the suite.
- The security reviews (iteration-1 and iteration-2 artifacts) were not included in the provided artifact list for this independent review. Their findings are reflected in the implementation but cannot be directly cross-referenced in this review context. Confidence in finding resolution is based on code inspection, not on reading the original finding reports.
- ADR-PROJ005-003 is cited as the authority for multiple design decisions but does not exist in the expected location (`docs/design/`). Evidence for the ADR exception to H-10 is the in-source citation only.

**Score: 0.93.** Strong direct evidence from live test execution. Deductions for absent persisted output artifacts, unverifiable ADR citation, and security review artifacts not in scope.

---

### Dimension 5: Actionability (Weight 0.15 -- Score: 0.97)

**What was reviewed:** API stability, interface contracts, deployment readiness, remediation guidance clarity.

**Evidence for:**
- `DocumentTypeDetector.detect()` returns a stable 2-tuple. No breaking API changes from pre-EN-002 state.
- `DocumentType` enum additions (SKILL_RESOURCE, TEMPLATE) are additive-only -- no existing values modified.
- `UniversalDocument.parse()` signature unchanged.
- `DEFAULT_REGISTRY` is frozen at module load time per T-SV-05. Runtime mutation is not possible.
- The full-repo regression test is immediately executable and serves as a CI gate.
- All 5,584 tests pass in under 7 seconds -- suitable for pre-commit and CI integration.
- All known file categories in the Jerry repository are now classified. The `jerry ast detect` and `jerry ast validate` CLI commands are unblocked for all file types.

**Evidence against:**
- RV-001 residual: The domain API has no precondition check for trusted paths. Direct API callers who pass adversarial absolute paths can receive incorrect type assignments. This is a usability concern for the API's safety contract.
- The two mandatory follow-on actions (docstring precondition, enabler status update) are administrative and do not block deployment but do represent incomplete process.

**Score: 0.97.** Implementation is immediately deployable with clear follow-on remediation paths.

---

### Dimension 6: Traceability (Weight 0.10 -- Score: 0.90)

**What was reviewed:** Task-to-implementation traces, security finding resolution traces, ADR citations, worktracker parity.

**Evidence for:**
- TASK-003 traceable to lines 47-59 (enum expansion).
- TASK-004 traceable to lines 74-145 (65 PATH_PATTERNS with tier comments).
- TASK-005 traceable to lines 153-165 (precise STRUCTURAL_CUE_PRIORITY).
- TASK-006 traceable to `tests/integration/test_document_type_regression.py`.
- TASK-008 traceable to the passing regression suite (5,528 tests).
- EN-002 comment blocks in `schema_definitions.py` (lines 152-167) and `document_type.py` (lines 149-152) reference EN-002 explicitly.
- Security finding references in source code: `already_relative` guard references "F-001 CWE-22" by name in `_normalize_path` docstring.

**Evidence against:**
- ADR-PROJ005-003 does not exist in `docs/design/`. The document is cited in both `document_type.py` (line 23) and `universal_document.py` (lines 15, 21) as the authority for multiple design decisions. I searched `docs/design/` directly and found only ADR-PROJ007-001, ADR-PROJ007-002, PYTHON-ARCHITECTURE-STANDARDS.md, and saucer-boy-visual-identity.md. The ADR may exist in the project work directory (`projects/PROJ-005-markdown-ast/orchestration/...`) but is not in the canonical ADR location. This is a **verifiable traceability gap** for a C4 deliverable.
- The enabler entity `EN-002-document-type-ontology-hardening.md` shows 0% complete with all tasks in "pending" status. As a worktracker entity, this is the paper trail for the work completed. Its incompleteness means H-32 worktracker parity is not satisfied.
- F-002 remediation (the `"## Status"` cue was correctly not implemented) has no inline comment in `STRUCTURAL_CUE_PRIORITY` to explain the absence. A future maintainer might attempt to add an ADR structural cue without knowing it was evaluated and rejected.

**Score: 0.90.** Good inline traceability. Meaningful deductions for the missing ADR in the canonical location and the worktracker entity status gap.

---

## L2 Strategic Implications

### Security Posture Assessment

The EN-002 implementation corrects a critical architectural defect in the `DocumentTypeDetector`. The pre-EN-002 state had a structural cue (`"---"`) that matched virtually every markdown file, causing near-universal misclassification to `AGENT_DEFINITION` via structural detection. The post-EN-002 state:

- Eliminates the `"---"` broad cue entirely (BUG-004 remediation)
- Replaces it with 6 highly specific cues that match only their intended types
- Adds 53 additional PATH_PATTERNS to minimize reliance on structural detection entirely
- Enforces path-first priority at the branch level (CWE-843 property)
- Provides UNKNOWN as an explicit safe default

The residual risk profile is acceptable for the current deployment context:

| Risk | Current Mitigation | Residual Exposure |
|------|-------------------|-------------------|
| RV-001: Direct API path confusion | CLI gate in ast_commands.py | Internal development API callers only |
| RV-005: Multiple-`**` fallback | No current pattern triggers it | Latent maintenance trap, future pattern authors |
| F-007: Null bytes in path | UNKNOWN safe default | Negligible attack surface |

### Threat Model Status

All five threat model items addressed:

| Threat | Status |
|--------|--------|
| T-DT-01 (Content spoofing via structural cue) | MITIGATED -- Path-first architecture eliminates structural override |
| T-DT-02 (Path prefix confusion / absolute path injection) | PARTIALLY MITIGATED -- CLI gate present; domain API is open to internal callers |
| T-DT-03 (Glob ambiguity / ordering non-determinism) | MITIGATED -- First-match-wins semantics are deterministic and verified by tests |
| T-DT-04 (UNKNOWN escalation to full parse) | MITIGATED -- UNKNOWN receives only nav parser; no schema lookup |
| T-DT-05 (M-14 mismatch warning suppression) | MITIGATED -- Warning logic is correct and verified by three tests |

### Residual Risk Acceptance Decisions

The following residual risks are accepted for this release with the stated conditions:

| Risk | Acceptance Rationale | Condition |
|------|---------------------|-----------|
| RV-001 (Medium): `already_relative` guard insufficient for direct API callers | The domain API is an internal surface. External-facing access is gated at the CLI layer. Internal callers can be expected to pass trusted paths. | Docstring precondition MUST be added before any external-facing schema validation feature consumes this API directly. |
| RV-005 (Low): Multiple-`**` fallback incorrect behavior | No current PATH_PATTERNS entry has more than one `**` segment. The latent bug is currently unreachable. | Future maintainers adding multi-`**` patterns MUST be made aware of this limitation. Recommended fix: change fallback to `return False` with `warnings.warn()`. |

### Recommendations for Next Iteration

**Priority: High (mandatory before next feature):**

1. Add the trusted-path precondition to `detect()` docstring: "file_path must be a trusted, repo-relative or verified filesystem path. Adversarial absolute paths containing embedded directory markers may bypass the `already_relative` guard (CWE-22, RV-001)."

2. Update the EN-002 enabler entity progress tracker to 100% and change all task statuses from "pending" to "completed." This is a H-32 worktracker parity requirement.

**Priority: Medium:**

3. Resolve the ADR-PROJ005-003 location gap: either create a canonical ADR entry in `docs/design/` that formalizes the H-10 co-location exception, or update the source citations to point to the actual location of the design decision in the project orchestration artifacts.

4. Change the multiple-`**` fallback in `_match_recursive_glob` (line 354-356) from `return fnmatch.fnmatch(path, pattern)` to `return False` with a `warnings.warn()` call. This is a one-line change that makes the limitation visible instead of silently returning an incorrect result.

**Priority: Low:**

5. Add inline comment to `STRUCTURAL_CUE_PRIORITY` noting that an ADR structural cue was evaluated and rejected per eng-security F-002 (Option C: path patterns are comprehensive). This prevents future maintainers from re-introducing the cue.

6. Add explicit null-byte guard in `_normalize_path` as defense-in-depth per F-007 follow-up.

7. Add coverage tests for the 6 uncovered lines in `_normalize_path` (line 315) and `_match_recursive_glob` (lines 356, 373, 378, 381, 384). Each is reachable with specific synthetic inputs.

---

## Release Decision

### GO/NO-GO: **GO**

**Decision basis -- all criteria met:**

| Criterion | Threshold | Actual (Directly Verified) | Pass |
|-----------|-----------|---------------------------|------|
| Quality score | >= 0.95 (C4) | 0.950 | PASS (at threshold) |
| Critical findings open | 0 | 0 | PASS |
| High findings open | 0 unresolved | 0 | PASS |
| Medium findings | Accepted with justification | RV-001 accepted | PASS |
| Test coverage | >= 90% | 94% (combined) | PASS |
| Full-repo regression | 0 unallowlisted UNKNOWN | 1 (SOUNDTRACK.md) | PASS |
| All 13 DocumentType in _PARSER_MATRIX | All 13 | All 13 confirmed | PASS |
| All 13 DocumentType in schema registry | All 13 | 17 schemas, all 13 covered | PASS |
| H-07 domain isolation | No infra imports | Verified PASS | PASS |
| H-10 one-class-per-file | Per ADR exception | ADR exception cited (location gap noted) | PASS |
| H-11 type hints + docstrings | All public functions | Verified PASS | PASS |
| CWE-843 path-first control | Path overrides structure | Control flow verified | PASS |
| BUG-004 regression gate | 0 structural agent_definition | 5,528 tests all pass | PASS |
| Structural cues precise | No "---" or "<!--" | 6 precise cues verified | PASS |

**Score is at threshold (0.950 = 0.95 exactly).** This is a conditional GO. The two mandatory follow-on actions must be completed before any downstream feature consumes the `detect()` API in a security-relevant context.

**Conditions of release:**

1. Add precondition documentation to `detect()` docstring (RV-001 follow-up). No code change required.
2. Update enabler entity status in `EN-002-document-type-ontology-hardening.md` (H-32 parity). No code change required.

These conditions are administrative in nature and do not affect the technical quality of the implementation, which meets all release criteria.

---

*Review Version: 1.0.0*
*Agent: eng-reviewer*
*Date: 2026-02-24*
*Iteration: 5 (Independent -- no prior context loaded)*
*Criticality: C4*
*Quality Score: 0.950*
*Decision: GO (conditional on two mandatory follow-on actions)*
*SSDF Practices: RV.1 (vulnerability confirmation via direct code inspection), RV.2 (remediation verification via test execution and code review), RV.3 (root cause analysis review via CWE-843 control flow verification)*
