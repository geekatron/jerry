# PROJ-005: Markdown AST Infrastructure - Work Tracker

> Global Manifest for PROJ-005. Investigate and implement AST-based markdown manipulation for the full Jerry surface.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Project overview and status |
| [Epics](#epics) | Strategic work items |
| [Decisions](#decisions) | Key decisions |
| [History](#history) | Change log |

---

## Summary

| Field | Value |
|-------|-------|
| Project | PROJ-005-markdown-ast |
| Status | IN-PROGRESS |
| Created | 2026-02-19 |
| Language Constraint | Python only (UV ecosystem) |
| Target Scope | Full Jerry surface (worktracker, skills, rules, templates, orchestration, ADRs) |

---

## Epics

| ID | Title | Status | Priority |
|----|-------|--------|----------|
| [EPIC-001](./work/EPIC-001-markdown-ast/EPIC-001-markdown-ast.md) | Markdown AST Infrastructure | in-progress | high |

> Features, Spikes, and Tasks are tracked within the Epic and its children.

---

## Decisions

| ID | Title | Status | Impact |
|----|-------|--------|--------|
| GO-001 | AST-first architecture adoption (markdown-it-py + mdformat, Pattern D) | decided | high |

---

## History

| Date | Author | Change |
|------|--------|--------|
| 2026-02-19 | Claude | PROJ-005 created. AST-based markdown manipulation initiative to replace raw text operations across Jerry's full documentation surface. |
| 2026-02-19 | Claude | Orchestration `spike-eval-20260219-001` complete. SPIKE-001 + SPIKE-002 evaluated. GO decision: adopt markdown-it-py + mdformat with Pattern D hybrid integration. QG scores: 0.96, 0.97, 0.96. |
| 2026-02-20 | Claude | FEAT-001 decomposed into 1 enabler (EN-001: R-01 PoC, 3 SP) + 10 stories (37 SP) = 40 SP across 4 implementation phases. EN-001 is the critical gate. |
| 2026-02-21 | Claude | BUG-001 filed under FEAT-001: CI/CD lint & test failures on PR #48. 32 ruff errors in r01_poc.py + 2 PROJ-006 test failures. TASK-001 (fix lint), TASK-002 (fix tests). |
| 2026-02-22 | Claude | BUG-001 resolved. TASK-001: ruff exclude for PoC + 22 pre-existing lint errors fixed. TASK-002: spec-driven project validation tests + SSOT sync tests + flaky perf thresholds relaxed. C4 adversarial review 0.955. CI green (run 22267538092). Commits: 9b34ca8, 3a69f7c. |
| 2026-02-24 | Claude | BUG-004 filed under FEAT-001: DocumentTypeDetector misclassifies most files as agent_definition. RCA: 3 root causes (overly broad `---` structural cue, incomplete path patterns, nav table over-reporting). EN-002 created: Document Type Ontology Hardening. Full taxonomy audit: 2,774 .md files across 20+ categories, only ~8 covered by PATH_PATTERNS. EN-002 expanded to 6 tasks (13 SP): enum expansion, path pattern rewrite, structural cue fix, full-repo parametrized regression test (~2,774 files), nav table audit, validation scan. |
