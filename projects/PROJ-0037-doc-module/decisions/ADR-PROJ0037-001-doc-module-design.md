# ADR-PROJ0037-001: Auto-Documentation Module Design

> **Phase:** B2 (Workstream B)
> **Agent:** ps-architect
> **Project:** PROJ-0037-doc-module
> **Date:** 2026-03-08
> **Status:** Proposed

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Context](#context) | Problem statement and constraints |
| [Decision](#decision) | Selected option with rationale |
| [Options Considered](#options-considered) | Three design options evaluated |
| [Evaluation](#evaluation) | Dimension-by-dimension comparison |
| [Consequences](#consequences) | Positive, negative, and neutral impacts |
| [Compliance](#compliance) | HARD rule satisfaction |

---

## Context

Jerry's README.md lists 6 of 13 skills and claims "8 specialized agents" when the actual count is 58. This documentation drift occurred because README updates are manual and not enforced. The framework needs an automated mechanism to keep README sections synchronized with the actual skills and agents in the repository.

**Constraints:**
- H-05: All Python execution via `uv run`, dependencies via `uv add`
- H-33: YAML frontmatter extraction MUST use AST-based parsing (`jerry ast`)
- H-10: One class per file
- H-11: Public functions require type hints and docstrings
- README.md is a public-facing file rendered by GitHub — must be committed, not generated at build time

**Inputs available:**
- 13 `skills/*/SKILL.md` files with YAML frontmatter (`name`, `description`, `version`, `activation-keywords`)
- 58 `skills/*/agents/*.md` files with YAML frontmatter (`name`, `description`, `model`, `tools`)
- Existing `jerry ast frontmatter` CLI command for structured extraction

---

## Decision

**Option A: Python CLI command (`jerry docs generate`)** using the existing `jerry ast` module for extraction and Jinja2 for rendering.

### Rationale

1. **Reuses existing infrastructure.** The `jerry ast` module already parses YAML frontmatter from markdown files (H-33 compliant). Adding a `docs` subcommand extends the CLI naturally.
2. **H-05 compliant by construction.** The Jerry CLI is already a uv-managed Python package. `uv add jinja2` adds the rendering dependency. `uv run jerry docs generate` runs it.
3. **H-33 compliant by construction.** Extraction uses `jerry ast frontmatter`, not regex.
4. **Testable at every layer.** Unit tests for extraction (YAML parsing), unit tests for rendering (Jinja2 template output), integration tests for end-to-end (golden file comparison).
5. **Three integration points.** CLI for development (`uv run jerry docs generate`), pre-commit hook for enforcement, CI step for backstop.

---

## Options Considered

### Option A: Python CLI Command (`jerry docs generate`)

Extend the existing Jerry CLI with a `docs generate` subcommand. Uses `jerry ast` for YAML frontmatter extraction from SKILL.md and agent .md files. Renders README sections via Jinja2 templates stored in `.context/templates/docs/`. Outputs to stdout or writes directly to README.md with `--write` flag. Drift detection via `--check` flag (exit code 1 if README differs from generated output).

**Architecture:**
```
skills/*/SKILL.md ──┐
                    ├──► jerry ast frontmatter ──► structured data ──► Jinja2 render ──► README sections
skills/*/agents/*.md┘
```

### Option B: Shell Script (`scripts/generate-docs.sh`)

Lightweight shell script using grep/awk/sed to extract YAML frontmatter fields. Generates markdown via heredoc templates. Runs as pre-commit hook or manual invocation.

### Option C: CI-Only Generation (GitHub Action)

GitHub Action triggered on push to main. Parses SKILL.md files, generates README sections, opens PR if drift detected. No local tooling required.

---

## Evaluation

| Dimension | Option A (Python CLI) | Option B (Shell Script) | Option C (CI-Only) |
|-----------|----------------------|------------------------|-------------------|
| **Maintainability** | High — Jinja2 templates are readable, modifiable, and testable. Adding a new README section means adding a template block. | Low — Heredoc templates with embedded awk are fragile. Complex escaping. Hard to modify without breaking. | Medium — GitHub Action YAML is maintainable but separated from the codebase. |
| **Accuracy** | High — `jerry ast frontmatter` returns structured YAML. Type-safe parsing. Handles multiline descriptions, arrays, nested fields. | Low — grep/awk parsing of YAML is error-prone. Multiline `description:` fields break grep patterns. Arrays require custom parsing. | Medium — Depends on parsing method used in the Action. |
| **H-05 compliance** | **PASS** — `uv run jerry docs generate`. Native uv integration. | **FAIL** — Shell scripts bypass uv. Would need `uv run` wrapper which defeats the purpose of "lightweight." | **N/A** — Runs in CI, not local Python. Not subject to H-05 for local execution, but H-05 applies to any Python in the Action. |
| **H-33 compliance** | **PASS** — Uses `jerry ast frontmatter` by design. | **FAIL** — grep/sed/awk is regex-based parsing, explicitly prohibited by H-33. | **Conditional** — Only if the Action uses `jerry ast` internally. |
| **Developer experience** | High — `uv run jerry docs generate --check` before committing. Immediate feedback. Integrates with existing CLI workflow. | Medium — `./scripts/generate-docs.sh` is simple to run but lacks `--check` mode natively. | Low — Developer commits, pushes, waits for CI, gets PR. Feedback loop is minutes to hours. |
| **Failure mode** | Malformed YAML → `jerry ast` returns parse error with file path and line number. Jinja2 template error → `TemplateSyntaxError` with template name and line. | Malformed YAML → silent incorrect output or awk error with no context. | Same as parsing method used, but error surfaces in CI logs, not developer terminal. |

**Scoring summary:**

| Dimension | Weight | A | B | C |
|-----------|--------|---|---|---|
| Maintainability | 0.25 | 3 | 1 | 2 |
| Accuracy | 0.25 | 3 | 1 | 2 |
| H-05/H-33 compliance | 0.20 | 3 | 0 | 1 |
| Developer experience | 0.15 | 3 | 2 | 1 |
| Failure mode clarity | 0.15 | 3 | 1 | 2 |
| **Weighted total** | | **2.85** | **0.95** | **1.65** |

---

## Consequences

### Positive

- README accuracy is enforced automatically — no more manual skill/agent counting
- Pre-commit hook prevents drift from reaching the repository
- Jinja2 templates serve as living documentation of README structure
- `--check` mode enables CI verification as a backstop
- Extension path is clear: same module can generate AGENTS.md sections, CLAUDE.md skill tables

### Negative

- Adds Jinja2 as a runtime dependency (~1MB, well-maintained Pallets project)
- Templates require maintenance when README structure changes
- Pre-commit hook adds ~1-2 seconds to commit time

### Neutral

- Does not change the README authoring workflow for non-skill/agent sections (intro, installation, platform support remain manually authored)
- Does not generate the entire README — only the skills table and features section are auto-generated; other sections remain static

---

## Compliance

| Rule | Status | Evidence |
|------|--------|----------|
| H-05 (uv-only) | PASS | `uv run jerry docs generate`, `uv add jinja2` |
| H-33 (AST-based parsing) | PASS | Uses `jerry ast frontmatter` for extraction |
| H-10 (one class per file) | PASS | Implementation will follow: `DocsGenerator`, `SkillExtractor`, `ReadmeRenderer` in separate files |
| H-11 (type hints + docstrings) | PASS | All public functions will have type hints and docstrings |
| AE-003 (new ADR = auto-C3) | Acknowledged | This ADR is subject to C3 minimum review |
