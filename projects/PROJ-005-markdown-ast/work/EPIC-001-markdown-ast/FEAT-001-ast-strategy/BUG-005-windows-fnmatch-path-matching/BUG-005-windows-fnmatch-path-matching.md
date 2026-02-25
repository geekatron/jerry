# BUG-005: Windows fnmatch.fnmatch applies normcase, breaking path pattern matching

<!--
TEMPLATE: Bug
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.10
-->

> **Type:** bug
> **Status:** in_progress
> **Priority:** high
> **Impact:** medium
> **Severity:** major
> **Created:** 2026-02-24
> **Due:** --
> **Completed:** --
> **Parent:** FEAT-001-ast-strategy
> **Owner:** Claude
> **Found In:** main @ 011b9391 (proj-005/en-002-ontology-hardening branch)
> **Fix Version:** --

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Bug overview and key details |
| [Steps to Reproduce](#steps-to-reproduce) | How to reproduce |
| [Environment](#environment) | Runtime environment |
| [Root Cause Analysis](#root-cause-analysis) | Why fnmatch breaks on Windows |
| [Fix Description](#fix-description) | Solution approach |
| [Acceptance Criteria](#acceptance-criteria) | Fix verification conditions |
| [Related Items](#related-items) | Links and hierarchy |
| [History](#history) | Change log |

---

## Summary

The `DocumentTypeDetector` CI test `test_orchestration_artifact_path` fails on Windows (Python 3.14) because `fnmatch.fnmatch` calls `os.path.normcase` which lowercases paths AND converts `/` to `\` on Windows. This causes `projects/*/PLAN.md` (Tier 3) to case-insensitively match `projects/PROJ-001/orchestration/phase-1/plan.md` before the correct pattern `projects/*/orchestration/**/*.md` (Tier 5) is reached.

**Key Details:**
- **Symptom:** `test_orchestration_artifact_path` returns `FRAMEWORK_CONFIG` instead of `ORCHESTRATION_ARTIFACT` on Windows
- **Frequency:** Every CI run on `windows-latest` with Python 3.14
- **Workaround:** None -- test fails on Windows CI

---

## Steps to Reproduce

### Prerequisites

- Python 3.14 on Windows (or any Windows Python)

### Steps to Reproduce

1. Run `uv run pytest tests/unit/domain/markdown_ast/test_document_type.py::TestPathDetection::test_orchestration_artifact_path` on Windows
2. Observe assertion failure: `assert DocumentType.FRAMEWORK_CONFIG == DocumentType.ORCHESTRATION_ARTIFACT`

### Expected Result

- `DocumentTypeDetector.detect("projects/PROJ-001/orchestration/phase-1/plan.md", "")` returns `ORCHESTRATION_ARTIFACT`

### Actual Result

- Returns `FRAMEWORK_CONFIG` because `fnmatch.fnmatch` lowercases `PLAN.md` to `plan.md` via `os.path.normcase`, allowing `projects/*/PLAN.md` to match the orchestration path

---

## Environment

| Attribute | Value |
|-----------|-------|
| **Operating System** | Windows (GitHub Actions `windows-latest`) |
| **Runtime** | Python 3.14 via pip install |
| **Application Version** | proj-005/en-002-ontology-hardening branch |
| **Configuration** | Default |
| **Deployment** | CI/CD (GitHub Actions) |

---

## Root Cause Analysis

### Investigation Summary

Traced the CI failure to `fnmatch.fnmatch` behavior differences between Unix and Windows.

### Root Cause

`fnmatch.fnmatch(name, pattern)` calls `os.path.normcase()` on both arguments before matching. On Windows, `os.path.normcase`:
1. Converts all characters to lowercase
2. Converts forward slashes `/` to backslashes `\`

This causes two problems:
1. **Case folding:** Pattern `PLAN.md` matches path `plan.md` after both are lowercased
2. **Slash conversion:** `*` in the regex can match `\` characters, allowing it to cross path segment boundaries

Combined effect: `fnmatch.fnmatch("projects/PROJ-001/orchestration/phase-1/plan.md", "projects/*/PLAN.md")` returns `True` on Windows because after normcase:
- Pattern: `projects\*\plan.md`
- Path: `projects\proj-001\orchestration\phase-1\plan.md`
- `*` matches `proj-001\orchestration\phase-1` (crossing directory boundaries)
- `plan.md` matches `plan.md` (case-folded)

Since `projects/*/PLAN.md` is at Tier 3 (line 100) and `projects/*/orchestration/**/*.md` is at Tier 5 (line 119), the wrong pattern matches first.

### Contributing Factors

- `_normalize_path` correctly converts to forward-slash POSIX form, but `fnmatch.fnmatch` un-does this by calling `normcase`
- `fnmatch`'s `*` matches any character including path separators (unlike shell glob where `*` excludes `/`)
- On Unix, the case mismatch (`PLAN` vs `plan`) prevents the false match, masking the underlying issue

---

## Fix Description

### Solution Approach

Replace all `fnmatch.fnmatch` calls with `fnmatch.fnmatchcase` in `document_type.py`. `fnmatchcase` does NOT call `os.path.normcase`, so it performs case-sensitive matching without path separator conversion. Since `_normalize_path` already converts paths to forward-slash POSIX form, no platform-specific normalization is needed.

### Changes Made

- `_path_matches_glob` line 358: `fnmatch.fnmatch` -> `fnmatch.fnmatchcase`
- `_match_recursive_glob` line 378: `fnmatch.fnmatch` -> `fnmatch.fnmatchcase`
- `_match_recursive_glob` line 391: `fnmatch.fnmatch` -> `fnmatch.fnmatchcase` (segment matching)
- `_match_recursive_glob` line 402: `fnmatch.fnmatch` -> `fnmatch.fnmatchcase` (suffix segment matching)

### Code References

| File | Change Description |
|------|-------------------|
| `src/domain/markdown_ast/document_type.py:358` | `fnmatch.fnmatch` -> `fnmatch.fnmatchcase` in `_path_matches_glob` |
| `src/domain/markdown_ast/document_type.py:378,391,402` | `fnmatch.fnmatch` -> `fnmatch.fnmatchcase` in `_match_recursive_glob` |
| `tests/unit/domain/markdown_ast/test_document_type.py` | Add Windows normcase regression test |

---

## Acceptance Criteria

### Fix Verification

- [ ] `fnmatch.fnmatchcase` used in all path matching (zero `fnmatch.fnmatch` calls in document_type.py)
- [ ] `test_orchestration_artifact_path` passes on all platforms (Linux, macOS, Windows)
- [ ] Regression test added: simulating Windows normcase behavior does not cause misclassification
- [ ] All existing 56 unit tests still pass

### Quality Checklist

- [ ] Existing tests still passing
- [ ] No new issues introduced
- [ ] CI green on all matrix entries

---

## Related Items

### Hierarchy

- **Parent:** [FEAT-001: AST Strategy](../FEAT-001-ast-strategy.md)
- **Parent Epic:** [EPIC-001: Markdown AST Infrastructure](../../EPIC-001-markdown-ast.md)

### Related Items

- **Related Enabler:** [EN-002: Document Type Ontology Hardening](../EN-002-document-type-ontology-hardening/EN-002-document-type-ontology-hardening.md) -- EN-002 introduced the path patterns that exposed this issue
- **Source File:** `src/domain/markdown_ast/document_type.py`
- **CI Run:** PR #91, check `Test pip (Python 3.14, windows-latest)`

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-24 | Claude | in_progress | Filed from CI failure on PR #91. RCA: fnmatch.fnmatch applies os.path.normcase on Windows. Fix: replace with fnmatch.fnmatchcase. |
