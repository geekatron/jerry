---
name: ast
description: Markdown AST operations for Jerry documents. Provides structured parse, query, modify, validate, and render operations on Jerry markdown files via the jerry ast CLI.
version: "1.1.0"
allowed-tools: Read, Write, Edit, Bash
activation-keywords:
  - "/ast"
  - "/jerry:ast"
  - "parse markdown"
  - "query frontmatter"
  - "modify frontmatter"
  - "validate markdown"
  - "render markdown"
  - "extract reinject"
  - "validate nav table"

---

# AST Skill

> **Version:** 1.1.0
> **Framework:** Jerry Framework v0.9.0
> **Layer:** CLI adapter (single entry point to domain layer)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Overview](#overview) | What this skill does and why |
| [When to Use This Skill](#when-to-use-this-skill) | Triggers and use cases |
| [Operations Reference](#operations-reference) | All available CLI commands |
| [Quick Reference](#quick-reference) | Copy-paste examples for common tasks |
| [Architecture Notes](#architecture-notes) | Layer compliance and design |

---

## Overview

The AST skill provides structured markdown operations for Claude agents working
within the Jerry Framework. All operations are exposed via the `jerry ast` CLI
namespace, which is the single adapter between agents and the
`src.domain.markdown_ast` domain layer.

### Core Capabilities

- **Parse:** Tokenize a markdown file and return AST structure as JSON.
- **Frontmatter:** Extract `> **Key:** Value` fields as a JSON object.
- **Modify:** Change a frontmatter field value and write back to disk.
- **Validate:** Check nav table compliance (H-23/H-24) and entity schema validation.
- **Render:** Normalize markdown via mdformat.
- **Reinject:** Extract all L2-REINJECT directives as a JSON list.
- **Query:** Query AST nodes by type.

---

## When to Use This Skill

Invoke `/ast` when you need to:

- Read frontmatter fields from a Jerry entity file (story, task, enabler, bug).
- Modify a single frontmatter field without disturbing the rest of the file.
- Validate that a markdown file complies with H-23 (nav table required) and H-24 (anchor links).
- Extract L2-REINJECT directives to inspect or audit the re-injection payload.
- Normalize markdown formatting before writing or diffing files.

Do NOT use `/ast` for:
- Reading raw file content (use Read tool directly).
- Writing arbitrary content to files (use Write/Edit tools directly).

---

## Operations Reference

All operations are invoked via `jerry ast <command>`. In agent context, use the
`--directory` prefix:

```bash
uv run --directory ${CLAUDE_PLUGIN_ROOT} jerry ast <command> [args]
```

### jerry ast parse

```bash
jerry ast parse <file>
```

Parse a markdown file and output the full AST as JSON (tokens + tree).

**Exit codes:** 0 success, 2 file error.

---

### jerry ast frontmatter

```bash
jerry ast frontmatter <file>
```

Extract all blockquote frontmatter fields as a JSON object.

**Output:** `{"Type": "story", "Status": "pending", ...}` or `{}` if no frontmatter.

**Exit codes:** 0 success, 2 file error.

---

### jerry ast modify

```bash
jerry ast modify <file> --key <KEY> --value <VALUE>
```

Modify one frontmatter field and write the updated content back to disk.

**Output:** `{"file": "...", "key": "...", "value": "...", "status": "modified"}`

**Exit codes:** 0 success, 1 key not found, 2 file error.

---

### jerry ast validate

```bash
jerry ast validate <file> [--schema <type>] [--nav]
```

Validate file structure against H-23/H-24 nav table rules and optionally
against an entity schema.

**Without `--schema`:** Returns JSON with nav table validation results.

**With `--schema <type>`:** Validates against entity schema (epic, feature,
story, enabler, task, bug). Returns JSON with both nav table and schema results.

**With `--nav`:** Includes detailed nav table entries in the output
(section_name, anchor, description, line_number).

**Output JSON keys:**

| Key | Type | Description |
|-----|------|-------------|
| `is_valid` | bool | True only when nav and schema are both valid |
| `nav_table_valid` | bool | True if nav table exists and covers all ## headings |
| `missing_nav_entries` | list | Heading texts absent from nav table |
| `orphaned_nav_entries` | list | Nav entries with no matching heading |
| `schema_valid` | bool | True when schema passes or no schema provided |
| `schema_violations` | list | Violation dicts (with --schema only) |
| `nav_entries` | list | Detailed entries (with --nav only) |

**Exit codes:** 0 success, 1 validation failure, 2 file/schema error.

---

### jerry ast render

```bash
jerry ast render <file>
```

Parse a file and output normalized (mdformat) markdown to stdout.

**Exit codes:** 0 success, 2 file error.

---

### jerry ast reinject

```bash
jerry ast reinject <file>
```

Extract all L2-REINJECT directives from a markdown file as a JSON list.

**Output:** List of dicts with rank, tokens, content, line_number.

**Exit codes:** 0 success, 2 file error.

---

### jerry ast query

```bash
jerry ast query <file> <selector>
```

Query AST nodes by type (e.g., heading, blockquote, paragraph).

**Output:** `{"selector": "...", "count": N, "nodes": [...]}`

**Exit codes:** 0 success, 2 file error.

---

## Quick Reference

### Read frontmatter from a story file

```bash
uv run jerry ast frontmatter projects/PROJ-005-markdown-ast/work/EPIC-001-markdown-ast/FEAT-001-ast-strategy/ST-005-ast-skill/ST-005-ast-skill.md
```

### Update story status

```bash
uv run jerry ast modify projects/PROJ-005-markdown-ast/work/EPIC-001-markdown-ast/FEAT-001-ast-strategy/ST-005-ast-skill/ST-005-ast-skill.md --key Status --value in-progress
```

### Validate a rule file for H-23/H-24 compliance

```bash
uv run jerry ast validate --nav .context/rules/quality-enforcement.md
```

### Extract L2-REINJECT directives from a rule file

```bash
uv run jerry ast reinject .context/rules/quality-enforcement.md
```

### Parse a file and inspect its structure

```bash
uv run jerry ast parse .context/rules/quality-enforcement.md
```

### Validate an entity file against a schema

```bash
uv run jerry ast validate --schema story projects/PROJ-005-markdown-ast/work/EPIC-001-markdown-ast/FEAT-001-ast-strategy/ST-005-ast-skill/ST-005-ast-skill.md
```

---

## Architecture Notes

### Single CLI Adapter

The `jerry ast` CLI namespace (`src/interface/cli/ast_commands.py`) is the
single adapter between agents and the domain layer. There is no separate
skill script — the CLI is the adapter:

```
jerry ast <command>                 <- CLI (interface layer)
    -> src.domain.markdown_ast     <- domain layer
```

The domain layer (`src/domain/markdown_ast/`) does NOT import back into the
interface layer (H-07 enforced by architecture boundary tests).

### References

| Topic | Location |
|-------|----------|
| Domain layer exports | `src/domain/markdown_ast/__init__.py` |
| CLI commands | `src/interface/cli/ast_commands.py` |
| CLI parser | `src/interface/cli/parser.py` |
| Unit tests | `tests/unit/interface/cli/test_ast_commands.py` |
| Integration tests | `tests/integration/cli/test_ast_subprocess.py` |
| H-23/H-24 rules | `.context/rules/markdown-navigation-standards.md` |
| Quality enforcement | `.context/rules/quality-enforcement.md` |
