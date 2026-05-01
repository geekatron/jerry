# TASK-008 Delivery Evidence: SKILL.md ADR Cross-Reference CI Check

> **Agent:** eng-devsecops
> **Date:** 2026-04-30
> **Task:** TASK-008 — Add CI check: every SKILL.md ADR cross-reference resolves
> **Status:** COMPLETE

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Script Summary](#script-summary) | Detection logic overview |
| [Pre-commit Hook Addition](#pre-commit-hook-addition) | YAML diff |
| [CI Workflow Addition](#ci-workflow-addition) | GitHub Actions change |
| [Test Results](#test-results) | pytest output |
| [Live-Tree Verification](#live-tree-verification) | Exit code and output |
| [AC Checklist](#ac-checklist) | Acceptance criteria sign-off |

---

## Script Summary

**Path:** `scripts/check_skill_adr_references.py`

The script implements the detection algorithm specified in `ci-check-spec.md` using only the Python standard library (`os`, `re`, `subprocess`, `sys`, `pathlib`).

Detection logic:

1. **Repository root** — obtained via `git rev-parse --show-toplevel`; falls back to `cwd()` for isolated test runs.
2. **SKILL.md discovery** — single-level glob `skills/*/SKILL.md` under the repository root (not recursive, per spec). Accepts explicit file path arguments to support pre-commit's selective invocation mode.
3. **ADR reference extraction** — each SKILL.md is scanned line-by-line with the regex `\]\(([^)]*docs/adrs/ADR-\d+[^)]*\.md)[^)]*\)`. Anchor fragments (`#section`) are stripped before path resolution.
4. **Path resolution** — paths starting with `./` or `../` are resolved relative to the SKILL.md's directory and then made repo-root-relative via `Path.resolve()` + `relative_to(repo_root)`. Paths not starting with those prefixes are treated as already repo-root-relative.
5. **Existence check** — `Path.is_file()` (follows symlinks per spec §Implementation Notes).
6. **Violation reporting** — each broken reference is printed as `BROKEN ADR REF: {skill_file}:{line}: '{raw_path}' -> resolved '{resolved}' does not exist`. A summary line follows. Exit code 0 on PASS, 1 on any violation.

Performance: O(N) where N = total ADR references; each reference is resolved and stat-checked exactly once.

---

## Pre-commit Hook Addition

Added to `.pre-commit-config.yaml` between the `skill-output-path-enforcement` hook and the `validate-templates` hook:

```yaml
  # =============================================================================
  # SKILL.md ADR Cross-Reference Integrity (TASK-008, STORY-001)
  # Asserts every docs/adrs/ADR-NNN*.md reference in skills/*/SKILL.md resolves
  # to a real file in the repository. Catches future packaging gaps.
  # =============================================================================
  - repo: local
    hooks:
      - id: skill-adr-refs
        name: SKILL.md ADR cross-reference integrity
        entry: uv run --frozen python scripts/check_skill_adr_references.py
        language: system
        files: ^(skills/[^/]+/SKILL\.md|docs/adrs/ADR-[0-9]+.*\.md)$
        pass_filenames: false
        always_run: false
        stages: [pre-commit]
```

The `files` pattern fires the hook when either a `skills/*/SKILL.md` or a `docs/adrs/ADR-NNN*.md` file is staged — covering both authoring a new SKILL.md reference and adding/removing an ADR file.

`pass_filenames: false` — the script discovers SKILL.md files itself via glob; no filenames are passed by pre-commit.

---

## CI Workflow Addition

Added as a step at the end of the `validation` job in `.github/workflows/ci.yml`, after the existing frontmatter validation step:

```yaml
      # TASK-008: SKILL.md ADR cross-reference integrity (STORY-001)
      - name: Check SKILL.md ADR cross-references (TASK-008)
        run: uv run python scripts/check_skill_adr_references.py
```

The `validation` job already has `uv sync --frozen` installed and Python available; no new setup steps were needed. The step runs after frontmatter validation so errors are grouped with related structural checks. Failure of this step causes the `validation` job to fail, which in turn causes the `ci-success` gate job to fail — blocking merge.

---

## Test Results

**Test file:** `tests/unit/scripts/test_check_skill_adr_references.py`

**Run command:** `uv run pytest tests/unit/scripts/test_check_skill_adr_references.py -v`

```
============================= test session starts ==============================
platform darwin -- Python 3.12.12, pytest-9.0.3, pluggy-1.6.0
rootdir: .
configfile: pytest.ini
collecting ... collected 13 items

tests/unit/scripts/test_check_skill_adr_references.py::test_valid_adr_reference_exits_zero PASSED [  7%]
tests/unit/scripts/test_check_skill_adr_references.py::test_broken_adr_reference_exits_one PASSED [ 15%]
tests/unit/scripts/test_check_skill_adr_references.py::test_multiple_references_reports_all_broken PASSED [ 23%]
tests/unit/scripts/test_check_skill_adr_references.py::test_extract_strips_anchor_fragment PASSED [ 30%]
tests/unit/scripts/test_check_skill_adr_references.py::test_extract_multiple_refs_on_one_line PASSED [ 38%]
tests/unit/scripts/test_check_skill_adr_references.py::test_extract_ignores_non_adr_links PASSED [ 46%]
tests/unit/scripts/test_check_skill_adr_references.py::test_extract_returns_empty_for_unreadable_file PASSED [ 53%]
tests/unit/scripts/test_check_skill_adr_references.py::test_resolve_relative_path PASSED [ 61%]
tests/unit/scripts/test_check_skill_adr_references.py::test_resolve_already_repo_relative_path PASSED [ 69%]
tests/unit/scripts/test_check_skill_adr_references.py::test_format_violation_line_matches_spec PASSED [ 76%]
tests/unit/scripts/test_check_skill_adr_references.py::test_format_summary_line PASSED [ 84%]
tests/unit/scripts/test_check_skill_adr_references.py::test_main_no_skill_files_found PASSED [ 92%]
tests/unit/scripts/test_check_skill_adr_references.py::test_spec_fixture_exact_output PASSED [100%]

============================== 13 passed in 0.10s ==============================
```

**Test count:** 13 passed, 0 failed.

Tests cover:
- Passing case (exit 0, valid reference)
- Failing case (exit 1, broken reference named in output)
- Edge case (multiple references: all broken ones reported, valid one not flagged)
- `extract_adr_references`: anchor stripping, multi-match per line, non-ADR links ignored, unreadable file
- `resolve_adr_path`: relative and repo-root-relative paths
- `format_violation_line`: exact format per ci-check-spec.md
- `format_summary_line`: exact format per ci-check-spec.md
- `main`: no SKILL.md files found
- Integration: ci-check-spec.md test fixture scenario

---

## Live-Tree Verification

**Run command:** `uv run python scripts/check_skill_adr_references.py`

**Output:**
```
ADR cross-reference check: all references resolve (30 SKILL.md file(s) checked). OK.
```

**Exit code:** 0

30 SKILL.md files were scanned. Zero broken ADR cross-references found. The previous eng-lead step (TASK-004/005/006) updated all stale references in `skills/transcript/` from the old jerry-core project path to `docs/adrs/`, and TASK-001 vendored `ADR-007-output-template-specification.md` into `docs/adrs/`. The live tree is consistent.

---

## AC Checklist

| AC | Status | Evidence |
|----|--------|----------|
| Script exists at `scripts/check_skill_adr_references.py` | PASS | File created; live-tree run confirms execution |
| Pre-commit hook wired | PASS | `skill-adr-refs` hook added to `.pre-commit-config.yaml` |
| Live-tree passes (exit 0) | PASS | Exit code 0; 30 SKILL.md files checked, 0 broken |
| Tests pass | PASS | 13/13 passed |
| Delivery evidence persisted | PASS | This file |
| Zero broken references in live tree | PASS | Script output: "all references resolve (30 SKILL.md file(s) checked)" |
| CI workflow step added | PASS | Step added to `validation` job in `.github/workflows/ci.yml` |
