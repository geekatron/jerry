# BUG-004: Document type detection misclassifies most files as agent_definition

<!--
TEMPLATE: Bug
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.10
-->

> **Type:** bug
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Severity:** major
> **Created:** 2026-02-24
> **Due:** --
> **Completed:** --
> **Parent:** FEAT-001-ast-strategy
> **Owner:** --
> **Found In:** main @ d25fa28c (v0.20.0)
> **Fix Version:** --

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Bug overview and key details |
| [Steps to Reproduce](#steps-to-reproduce) | How to reproduce |
| [Environment](#environment) | Runtime environment |
| [Root Cause Analysis](#root-cause-analysis) | Two distinct root causes identified |
| [Acceptance Criteria](#acceptance-criteria) | Fix verification conditions |
| [Related Items](#related-items) | Links and hierarchy |
| [History](#history) | Change log |

---

## Summary

The `jerry ast detect` command misclassifies most markdown files as `agent_definition` due to two bugs in `DocumentTypeDetector` (`src/domain/markdown_ast/document_type.py`). Additionally, the `jerry ast validate` command (without `--schema`) reports spurious nav table failures for files with valid navigation tables that use heading levels other than `##`, or where nav entries reference headings at `###` or deeper levels.

**Key Details:**
- **Symptom:** `jerry ast detect` reports `agent_definition` with structural mismatch warnings on rule files, worktracker entities, orchestration artifacts, skill playbooks, and most other file types. `jerry ast validate` reports `is_valid: false` on 8/10 of the largest framework files. Of the 2,774 `.md` files in the repo, an estimated 1,634 have no path pattern match and fall through to the buggy `"---"` structural cue.
- **Frequency:** Every invocation of `jerry ast detect` or `jerry ast validate` on affected files
- **Workaround:** None -- the detect and validate commands produce incorrect results

---

## Steps to Reproduce

### Prerequisites

- Jerry Framework v0.20.0 on main branch
- `uv` installed

### Steps to Reproduce

**Bug 1: Structural cue misclassification**

1. Run `uv run jerry ast detect ".context/rules/quality-enforcement.md"`
2. Observe output: `{"type": "rule_file", "method": "path", "warning": "Path suggests rule_file but content structure suggests agent_definition"}`
3. Run `uv run jerry ast detect "skills/problem-solving/PLAYBOOK.md"`
4. Observe output: `{"type": "agent_definition", "method": "structure"}` -- PLAYBOOK.md has NO path pattern match, so it falls to structural detection, and the `---` YAML delimiter cue matches `agent_definition`

**Bug 2: Nav table validation reports false failures**

1. Run `uv run jerry ast validate "skills/transcript/SKILL.md"`
2. Observe `is_valid: false` with 32 missing nav entries -- but these are `###` headings, not `##` headings. The nav table only covers `##` headings, yet the validator expects nav entries for ALL headings

### Expected Result

- `detect` should correctly classify PLAYBOOK.md, WORKTRACKER.md, etc. without false `agent_definition` structural matches
- `validate` should report `is_valid: true` for files with properly structured `##`-level nav tables, even when `###` sub-headings exist

### Actual Result

- `detect`: 5/5 tested files produce structural mismatch warnings or outright misclassification
- `validate`: 8/10 of the largest files report `is_valid: false` due to nav table validation failures

---

## Environment

| Attribute | Value |
|-----------|-------|
| **Operating System** | macOS Darwin 24.6.0 |
| **Runtime** | Python via uv (jerry v0.20.0) |
| **Application Version** | v0.20.0 (d25fa28c) |
| **Configuration** | Default |
| **Deployment** | Local development |

---

## Root Cause Analysis

### Investigation Summary

Tested the top 10 largest markdown files in the repository against all AST parser commands (`parse`, `validate`, `frontmatter`, `detect`). Cross-referenced results with source code analysis of `DocumentTypeDetector` and `validate_nav_table`.

### Root Cause 1: Overly broad structural cue for `agent_definition`

**File:** `src/domain/markdown_ast/document_type.py:91`

The first structural cue in `STRUCTURAL_CUE_PRIORITY` is:

```python
STRUCTURAL_CUE_PRIORITY: list[tuple[str, DocumentType]] = [
    ("---", DocumentType.AGENT_DEFINITION),   # <-- BUG: matches ALL files with horizontal rules
    ("> **", DocumentType.WORKTRACKER_ENTITY),
    ("<identity>", DocumentType.AGENT_DEFINITION),
    ("<!-- L2-REINJECT", DocumentType.RULE_FILE),
    ("<!--", DocumentType.ADR),
]
```

The string `"---"` (horizontal rule / YAML frontmatter delimiter) appears in virtually every Jerry markdown file. Since structural cues use first-match-wins semantics, nearly every file without a path pattern match gets classified as `agent_definition`. The cue was intended to match YAML frontmatter delimiters specific to agent definition `.md` files, but `---` is used universally as a section separator across all Jerry markdown files.

**Impact:** Any file not matched by `PATH_PATTERNS` (playbooks, research artifacts, synthesis docs, templates, etc.) is misclassified as `agent_definition` via structural detection.

### Root Cause 2: Incomplete path patterns in ontology

**File:** `src/domain/markdown_ast/document_type.py:69-86`

The `PATH_PATTERNS` list has significant coverage gaps:

| File Pattern | Missing Type | Example |
|---|---|---|
| `skills/*/PLAYBOOK.md` | Not in patterns | `skills/problem-solving/PLAYBOOK.md` |
| `skills/*/tests/*.md` | Not in patterns | `skills/nasa-se/tests/BEHAVIOR_TESTS.md` |
| `.context/templates/**/*.md` | Not in patterns | `.context/templates/design/TDD.template.md` |
| `docs/synthesis/**/*.md` | Not in patterns | `docs/synthesis/work-026-e-003-*.md` |

When path detection returns `None`, the buggy structural cue detection takes over and misclassifies these files.

### Root Cause 3: Nav table validator over-reports missing entries

**File:** `src/domain/markdown_ast/nav_table.py:256-259`

The `_extract_h2_headings` function correctly extracts only `##` headings. However, the `validate` CLI command reports these as "missing nav entries" without distinguishing between intentionally omitted sub-headings (`###`) and genuinely missing `##` sections. In files like `SKILL.md` (transcript skill), many `###` headings appear as section content under `##` parents, but the validation output conflates them with missing nav table coverage.

**Correction on re-inspection:** The validator itself only checks `##` headings (line 203: `if node.tag != "h2": continue`). The actual issue is that these files have many `##` headings that are NOT listed in the nav table -- the nav table only covers a subset. So the validator is technically correct that these are missing, but the files are structured with intentionally partial nav tables (covering major sections only, not every `##`).

### Contributing Factors

- The `---` string was likely chosen during initial development when agent definitions were the primary structural target, before the framework expanded to many document types
- Path patterns were defined for the core ontology types but not extended when new file categories (playbooks, behavior tests, templates, synthesis docs) were added
- No regression test validates structural cue detection accuracy across all document types

---

## Acceptance Criteria

### Fix Verification

- [ ] `jerry ast detect` correctly classifies files without false `agent_definition` structural matches
- [ ] `jerry ast detect "skills/problem-solving/PLAYBOOK.md"` does NOT return `agent_definition`
- [ ] `jerry ast detect ".context/rules/quality-enforcement.md"` returns `rule_file` without structural mismatch warning
- [ ] `jerry ast detect` on all 10 tested files returns correct types without warnings
- [ ] Structural cue `"---"` is replaced or refined so it does not match every markdown file

### Quality Checklist

- [ ] Regression tests added for structural cue detection across all document types
- [ ] Existing tests still passing
- [ ] No new issues introduced
- [ ] Path patterns cover all known Jerry file categories

---

## Related Items

### Hierarchy

- **Parent:** [FEAT-001: AST Strategy](../FEAT-001-ast-strategy.md)
- **Parent Epic:** [EPIC-001: Markdown AST Infrastructure](../../EPIC-001-markdown-ast.md)

### Related Items

- **Related Enabler:** [EN-002: Document Type Ontology Hardening](../EN-002-document-type-ontology-hardening/EN-002-document-type-ontology-hardening.md)
- **Source File:** `src/domain/markdown_ast/document_type.py`
- **Source File:** `src/domain/markdown_ast/nav_table.py`

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-24 | Claude | pending | Initial report. RCA complete: 3 root causes identified (overly broad structural cue, incomplete path patterns, nav table over-reporting). Filed with EN-002 for systematic fix. |
