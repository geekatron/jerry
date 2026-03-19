# Auto-Documentation Patterns Research

> **Phase:** B1 (Workstream B)
> **Agent:** ps-researcher
> **Project:** PROJ-0037-doc-module
> **Date:** 2026-03-08

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Top findings and recommendation direction |
| [L1: Pattern Comparison](#l1-pattern-comparison) | Comparative analysis across all patterns |
| [L2: Detailed Analysis](#l2-detailed-analysis) | Full analysis per pattern with Jerry applicability |

---

## L0: Executive Summary

1. **Elixir's `@moduledoc` pattern is the closest conceptual match** to Jerry's SKILL.md/agent .md approach. Both use in-source structured annotations that tooling extracts into browsable documentation. Jerry's YAML frontmatter is the functional equivalent of `@moduledoc`.

2. **Template-based README generation is the practical approach for Jerry.** Unlike Sphinx/mkdocs which build entire doc sites, Jerry needs to inject extracted metadata into specific README sections. Jinja2 templates with YAML data input is the established pattern for this.

3. **Static analysis (no import/execution) is essential.** sphinx-autodoc2 demonstrated that static AST-based parsing (no `import` needed) is the modern standard. Jerry's existing `jerry ast` module already does this for markdown frontmatter — it should be the extraction layer.

4. **Pre-commit hook is the right integration point.** CI-only approaches detect drift too late; CLI-only approaches depend on developer memory. A pre-commit hook runs `jerry docs generate` and fails if the output differs from committed README, ensuring docs stay current without manual intervention.

5. **Jerry already has 80% of the infrastructure.** The `jerry ast` CLI parses YAML frontmatter (H-33). SKILL.md files have structured `name`, `description`, `version`, `activation-keywords` fields. Agent .md files have `name`, `description`, `model`, `tools` frontmatter. The gap is: (a) a Jinja2 rendering step, and (b) a drift detection comparison.

---

## L1: Pattern Comparison

| Dimension | Elixir `@moduledoc` | Sphinx autodoc2 | mkdocs-gen-files | Jinja2 Templates | CI-only |
|-----------|---------------------|-----------------|------------------|-------------------|---------|
| **Extraction method** | Language-native `@doc` attributes compiled into BEAM bytecode; `Code.fetch_docs/1` retrieves at runtime | Static AST analysis of Python source; no import needed | Python scripts run at build time; can read any source | Manual data loading (YAML, JSON, dict) | Same as any above |
| **Rendering method** | ExDoc generates HTML/markdown from extracted docs | RST/MyST generation from docstring AST | Virtual file generation into mkdocs build | Template rendering with inheritance, blocks, filters | Same as any above |
| **Integration point** | `mix docs` CLI command | Sphinx build pipeline | mkdocs build pipeline | Any (CLI, hook, CI) | GitHub Action on push |
| **Failure mode** | Missing `@moduledoc` → module hidden from docs | Malformed Python → parse error with line info | Script exception → build failure with traceback | Template syntax error → Jinja2 `TemplateSyntaxError` | PR opened with diff |
| **Jerry applicability** | **High (conceptual model)** — YAML frontmatter = `@moduledoc`. Jerry CLI = `mix docs`. | **Medium** — Static analysis pattern applicable, but Sphinx is Python-specific. Jerry uses markdown not Python. | **Low** — Requires mkdocs infrastructure Jerry doesn't have. | **High (rendering layer)** — Perfect for injecting extracted YAML into README sections. | **Medium** — Detection works but correction happens too late (after commit). |

---

## L2: Detailed Analysis

### L2.1: Elixir Phoenix `@moduledoc` / ExDoc Pattern

**How it works:**
- Elixir modules declare `@moduledoc` and `@doc` attributes inline with source code
- These are compiled into BEAM bytecode metadata, accessible via `Code.fetch_docs/1`
- `mix docs` invokes ExDoc which reads compiled metadata and generates HTML documentation
- Modules with `@moduledoc false` are explicitly hidden from documentation

**Key insight for Jerry:**
The `@moduledoc` pattern treats **documentation as structured metadata co-located with source**, not as a separate documentation system. This is exactly what Jerry already does with YAML frontmatter in SKILL.md and agent .md files. The gap is that Jerry lacks the equivalent of `mix docs` — a command that reads all frontmatter and renders it into a consumable format.

**Applicability:** Conceptual model only. Jerry doesn't use Elixir. But the metadata-to-docs pipeline pattern is directly transferable: `YAML frontmatter` → `jerry ast extract` → `Jinja2 render` → `README sections`.

### L2.2: Sphinx autodoc2 (Static Analysis)

**How it works:**
- `analyse_module(module_path, module_name)` performs static AST analysis
- Returns structured dictionaries: `{type, full_name, doc, args, return_annotation}`
- No `import` or code execution required — reads Python source as text
- Handles `if TYPE_CHECKING` blocks correctly

**Key insight for Jerry:**
Static analysis is the right approach — Jerry's `jerry ast frontmatter` already does this for markdown YAML frontmatter. The extraction layer exists. What's missing is the rendering layer.

**Applicability:** The static analysis principle applies. The specific Sphinx/RST pipeline does not.

### L2.3: mkdocs-gen-files

**How it works:**
- Python scripts run during mkdocs build via plugin configuration
- Scripts use `mkdocs_gen_files.open()` to create virtual pages
- Pages exist only during build; not committed to repository
- Often paired with mkdocstrings for API doc stubs

**Key insight for Jerry:**
The "virtual file" concept (generated at build time, not committed) is interesting but wrong for Jerry. README.md MUST be committed because GitHub renders it. Jerry needs the opposite: generate → commit → verify no drift.

**Applicability:** Low. Jerry doesn't use mkdocs and needs committed (not virtual) output.

### L2.4: Jinja2 Template Rendering

**How it works:**
- `Environment(loader=FileSystemLoader("templates/"))` loads template files
- Templates use `{% block %}`, `{% extends %}`, `{{ variable }}` syntax
- Filters transform data: `{{ name | title }}`, `{{ items | sort }}`
- Template inheritance allows base README template with overridable sections

**Key insight for Jerry:**
Jinja2 is the ideal rendering layer. A README template with `{% for skill in skills %}` blocks can generate the skills table automatically. The template serves as both the format specification and the rendering engine.

**Example template snippet:**
```jinja
| Skill | Purpose | Agents |
|-------|---------|--------|
{% for skill in skills %}
| `/{{ skill.name }}` | {{ skill.description | truncate(60) }} | {{ skill.agent_count }} |
{% endfor %}
```

**Applicability:** High. Jinja2 is a Python library (H-05 compatible via `uv add jinja2`). Template-based rendering is well-understood and testable.

### L2.5: Pre-commit Hook vs. CI Step vs. CLI Command

| Approach | Pros | Cons | Jerry Fit |
|----------|------|------|-----------|
| **Pre-commit hook** | Catches drift before commit; fast feedback; runs locally | Developers can skip with `--no-verify`; requires hook installation | **Best fit** — Jerry already uses pre-commit hooks in Python |
| **CI step** | Reliable; runs on every push; cannot be bypassed | Drift detected after commit; requires PR to fix; feedback loop is slow | Good as secondary check, not primary |
| **CLI command** | Developer-friendly; explicit invocation; easy to test | Relies on developer memory; no enforcement | Good for development/testing, not enforcement |

**Recommendation:** All three. CLI command (`jerry docs generate`) for development. Pre-commit hook that runs the command and fails on drift. CI step as backstop verification.

### L2.6: Jerry-Specific Considerations

**Existing infrastructure:**
- `jerry ast frontmatter <file>` — Extracts YAML frontmatter from markdown (H-33 compliant)
- `jerry ast validate <file>` — Validates markdown structure
- `scripts/` directory — Existing pre-commit hook scripts (Python)
- `pyproject.toml` — uv-managed dependencies (H-05 compliant)

**Extraction inputs:**
- 13 `skills/*/SKILL.md` files with `name`, `description`, `version`, `activation-keywords`
- 58 `skills/*/agents/*.md` files with `name`, `description`, `model`, `tools`
- `AGENTS.md` — Current verified count and structure

**Governance constraints:**
- H-05: Must use `uv run` for Python execution, `uv add` for dependencies
- H-33: Must use AST-based parsing (jerry ast) for frontmatter extraction, not regex
- H-10: One class per file
- H-11: Type hints and docstrings on public functions

**Dependency considerations:**
- Jinja2 is a well-established, low-risk dependency (Pallets project, widely used)
- Already indirectly present in many Python ecosystems
- SLSA assessment: mature supply chain, regular releases, high GitHub star count

---

## Sources

- [Elixir @moduledoc documentation](https://hexdocs.pm/elixir/1.19.3/writing-documentation)
- [sphinx-autodoc2](https://github.com/sphinx-extensions2/sphinx-autodoc2)
- [mkdocs-gen-files](https://github.com/oprypin/mkdocs-gen-files)
- [Jinja2 Template Documentation](https://jinja.palletsprojects.com/en/stable/templates)
- [yaml-docs](https://github.com/andbron/yaml-docs)
- [andreasbm/readme](https://github.com/andreasbm/readme)
- [mkdocstrings recipes](https://mkdocstrings.github.io/recipes/)
