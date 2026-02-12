# EN-004:DEC-002: Pytest Hook File Type Coverage

> **Type:** decision
> **Status:** ACCEPTED
> **Priority:** HIGH
> **Created:** 2026-02-11
> **Parent:** EN-004
> **Owner:** Adam Nowak
> **Related:** BUG-011

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description of decision |
| [Decision Context](#decision-context) | Background and constraints |
| [Evidence](#evidence) | Research findings and data |
| [Decisions](#decisions) | Structured decision entries |
| [Decision Summary](#decision-summary) | Quick reference table |
| [Related Artifacts](#related-artifacts) | Traceability |
| [Document History](#document-history) | Changes |

---

## Summary

Decision on how to extend the pre-commit pytest hook to cover markdown file changes for BUG-011. Research confirmed that 9 test methods in `test_path_conventions.py` scan markdown files, but the pytest hook uses `types: [python]` (line 75), meaning markdown-only commits bypass all architecture tests locally.

**Decisions Captured:** 1

**Key Outcomes:**
- Use `types_or: [python, markdown]` on the pytest hook (Option A)
- Do NOT create a separate markdown-only hook (Option B rejected)
- Pyright hook correctly remains `types: [python]` (no change needed)

---

## Decision Context

### Background

The pytest pre-commit hook in `.pre-commit-config.yaml` (line 75) uses `types: [python]`, which means it only triggers when Python files are staged. Commits that only modify markdown files skip the entire test suite — including architecture tests that validate markdown content.

This gap was identified as the root cause of CI failures during markdown content corrections, where markdown-only commits passed local hooks but failed architecture tests in CI.

### Current State

| Hook | Line | File Type Filter | Affected by BUG-011 |
|------|------|-----------------|---------------------|
| pyright | 60 | `types: [python]` | No (pyright only checks Python) |
| pytest | 75 | `types: [python]` | **Yes** (pytest runs markdown-scanning tests) |
| validate-plugin-manifests | 93 | `files: (plugin\.json\|...)` | No (uses `files:` pattern) |
| trailing-whitespace | 26 | All files (default) | No |
| end-of-file-fixer | 28 | All files (default) | No |

### Constraints

- Must not cause pytest to run twice for mixed Python+markdown commits
- Must not break existing Python-only commit workflows
- Hook execution time should remain reasonable
- Pyright hook must NOT change (it only operates on Python files)

---

## Evidence

### Architecture Tests That Scan Markdown

| # | Test Method | File | Markdown Scanning |
|---|------------|------|-------------------|
| E-1 | `test_no_cross_project_references` | `test_path_conventions.py:60` | `proj_root.rglob("*.md")` |
| E-2 | `test_no_deprecated_pattern` | `test_path_conventions.py:119` | `proj_root.rglob("*.md")` |
| E-3 | `test_no_hardcoded_absolute_paths` | `test_path_conventions.py:144` | `proj_root.rglob("*.md")` |
| E-4 | `test_research_contains_extraction_docs` | `test_path_conventions.py:193` | `research_dir.glob("*.md")` |
| E-5 | `test_synthesis_contains_canon_doc` | `test_path_conventions.py:207` | `synthesis_dir.glob("*.md")` |
| E-6 | `test_decisions_contains_adr_docs` | `test_path_conventions.py:223` | `decisions_dir.glob("*.md")` |
| E-7 | `test_bug001_fix_holds` | `test_path_conventions.py:244` | `category_dir.glob("*.md")` |
| E-8 | `test_new_documents_use_correct_paths` | `test_path_conventions.py:273` | `proj_root.rglob("*.md")` |
| E-9 | `test_all_project_artifacts_in_project_directory` | `test_path_conventions.py:33` | `category_dir.glob("PROJ-*.md")` |

### Pre-commit Configuration

| # | Source | Finding |
|---|--------|---------|
| E-10 | `.pre-commit-config.yaml:75` | `types: [python]` — pytest only triggers on Python files |
| E-11 | `.pre-commit-config.yaml:60` | `types: [python]` — pyright correctly Python-only |
| E-12 | `.pre-commit-config.yaml:93` | `files: (plugin\.json\|...)` — plugin validation uses `files:` pattern |
| E-13 | `.pre-commit-config.yaml` | Zero instances of `types_or` anywhere in config |
| E-14 | `.pre-commit-config.yaml` | Zero hooks explicitly target markdown files |
| E-15 | `.pre-commit-config.yaml:76` | `pass_filenames: false` — pytest ignores staged file list |

### Pre-commit `types_or` Semantics

- `types: [python]` — Trigger only when ALL listed types are staged (AND logic)
- `types_or: [python, markdown]` — Trigger when ANY listed type is staged (OR logic)
- With `pass_filenames: false` (E-15), the hook runs the full test suite regardless of which files triggered it — so no risk of partial execution

### Research Method

/problem-solving agent `ps-researcher` performed systematic analysis of `.pre-commit-config.yaml` and test files to map the coverage gap.

---

## Decisions

### D-001: Use `types_or: [python, markdown]` on the pytest hook

**Date:** 2026-02-11
**Participants:** Adam Nowak, Claude

#### Question/Context

The pytest hook needs to run when markdown files change (in addition to Python files). Two approaches were evaluated.

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A: `types_or` on existing hook (Recommended)** | Change `types: [python]` to `types_or: [python, markdown]` on the pytest hook | Simple 1-line change; runs full suite catching cross-cutting issues; no new hook definition to maintain; `pass_filenames: false` means no partial execution risk | Runs full suite on markdown-only changes (~5-10s for project validation subset) |
| **B: Separate markdown-only hook** | Add new `project-validation` hook: `entry: uv run pytest tests/project_validation/` with `types: [markdown]` | Targeted — only runs architecture tests on markdown | Two hooks to maintain; risks diverging test scope; doesn't catch cross-cutting Python+markdown interactions; adds configuration complexity |

#### Decision

**We decided:** Option A — Change `types: [python]` to `types_or: [python, markdown]` on the existing pytest hook (`.pre-commit-config.yaml` line 75).

#### Rationale

1. **Simplicity** — 1-line change vs adding an entire new hook definition
2. **Completeness** — Full suite catches cross-cutting issues (e.g., a markdown change that violates a path convention checked by a Python test)
3. **No duplication** — Option B creates a second hook that partially overlaps with the first
4. **`pass_filenames: false` makes it safe** (E-15) — The hook runs the full test suite regardless, so there's no risk of selective execution
5. **Minimal performance impact** — Project validation tests add ~5-10s, acceptable for a pre-commit hook
6. **Consistent with existing pattern** — The hook already ignores filenames; changing the trigger filter is the only modification needed

#### Implementation

```yaml
# Before (line 75):
types: [python]

# After:
# Trigger on Python and Markdown changes. Architecture tests (test_path_conventions.py)
# validate markdown content (hardcoded paths, cross-project refs). Without markdown
# in the trigger, markdown-only commits bypass local quality gates. See EN-004:DEC-002.
types_or: [python, markdown]
```

#### Note on Pyright Hook

The pyright hook (line 60) correctly uses `types: [python]` and should NOT be changed. Pyright is a Python type checker — it has no reason to run on markdown files.

#### Implications

- **Positive:** Closes the coverage gap; markdown-only commits now validated locally; minimal change
- **Negative:** Full test suite runs on markdown-only commits (~5-10s overhead, acceptable)
- **Follow-up:** Add explanatory comment in `.pre-commit-config.yaml` per BUG-011/TASK-001 AC

---

## Decision Summary

| ID | Decision | Date | Status |
|----|----------|------|--------|
| D-001 | Use `types_or: [python, markdown]` on pytest hook instead of separate markdown hook | 2026-02-11 | ACCEPTED |

---

## Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Parent | [EN-004](./EN-004-fix-precommit-hook-coverage.md) | Fix Pre-commit Hook Coverage |
| Feature | [FEAT-001](../FEAT-001-fix-ci-build-failures.md) | Fix CI Build Failures |
| Bug | [BUG-011](./BUG-011-precommit-pytest-python-only.md) | Pre-commit pytest hook only triggers on Python file changes |
| Task | [BUG-011/TASK-001](./BUG-011--TASK-001-add-markdown-to-pytest-trigger.md) | Add markdown file types to pytest pre-commit hook trigger |
| File | `.pre-commit-config.yaml` | Pre-commit configuration (line 75) |
| File | `tests/project_validation/architecture/test_path_conventions.py` | 9 test methods scanning markdown files |

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-02-11 | Claude | Created decision document. Option A (types_or) accepted over Option B (separate hook). Based on ps-researcher findings: 9 tests scan markdown, zero hooks trigger on markdown. |

---

## Metadata

```yaml
id: "EN-004:DEC-002"
parent_id: "EN-004"
work_type: DECISION
title: "Pytest Hook File Type Coverage"
status: ACCEPTED
priority: HIGH
created_by: "Claude"
created_at: "2026-02-11"
updated_at: "2026-02-11"
decided_at: "2026-02-11"
participants: ["Adam Nowak", "Claude"]
tags: ["pre-commit", "pytest", "markdown", "types_or", "architecture-tests"]
decision_count: 1
superseded_by: null
supersedes: null
```
