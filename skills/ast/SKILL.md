---
name: ast
description: Markdown AST operations for Jerry documents. Provides structured parse, query, modify, validate, and render operations on Jerry markdown files via the domain layer.
version: "1.0.0"
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

> **Version:** 1.0.0
> **Framework:** Jerry Framework v0.5.0
> **Layer:** Interface (skill script wrapping domain layer)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Overview](#overview) | What this skill does and why |
| [When to Use This Skill](#when-to-use-this-skill) | Triggers and use cases |
| [Operations Reference](#operations-reference) | All available operations with signatures |
| [Quick Reference](#quick-reference) | Copy-paste examples for common tasks |
| [Architecture Notes](#architecture-notes) | Layer compliance and import rules |

---

## Overview

The AST skill provides structured markdown operations for Claude agents working
within the Jerry Framework. It wraps the `src.domain.markdown_ast` domain layer
in thin file-level functions that Claude can invoke during interactive sessions.

All operations read from and write to the filesystem. The domain layer handles
all AST parsing, transformation, and rendering -- the skill scripts are pure
wrappers with no parsing logic of their own.

### Core Capabilities

- **Parse:** Tokenize a markdown file and return AST structure information.
- **Query Frontmatter:** Extract `> **Key:** Value` fields as a plain dict.
- **Modify Frontmatter:** Change a frontmatter field value and write back to disk.
- **Validate:** Check H-23/H-24 nav table compliance and stub schema validation.
- **Render:** Normalize markdown via mdformat and return the result.
- **Extract Reinject:** Extract all L2-REINJECT directives from a rule file.
- **Validate Nav Table:** Full H-23/H-24 audit with per-entry serializable output.

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

All operations live in `skills/ast/scripts/ast_ops.py`. Invoke via `uv run python`:

```
uv run python -c "from skills.ast.scripts.ast_ops import <function>; ..."
```

### parse_file

```python
parse_file(file_path: str) -> dict
```

Parse a markdown file and return structured AST information.

**Returns dict with:**

| Key | Type | Description |
|-----|------|-------------|
| `file_path` | str | The path as provided |
| `source_length` | int | Total character count |
| `node_types` | list[str] | Unique AST node types present |
| `heading_count` | int | Total number of heading nodes |
| `has_frontmatter` | bool | True if any `> **Key:** Value` fields found |

**Raises:** `FileNotFoundError` if file does not exist.

---

### query_frontmatter

```python
query_frontmatter(file_path: str) -> dict[str, str]
```

Extract all blockquote frontmatter fields as a plain dict.

**Returns:** `{"Type": "story", "Status": "pending", ...}` or `{}` if no frontmatter.

**Raises:** `FileNotFoundError` if file does not exist.

---

### modify_frontmatter

```python
modify_frontmatter(file_path: str, key: str, value: str) -> str
```

Modify one frontmatter field and write the updated content back to disk.

**Returns:** The new file content as a string.

**Raises:**
- `FileNotFoundError` if file does not exist.
- `KeyError` if the key does not exist in the frontmatter.

---

### validate_file

```python
validate_file(file_path: str, schema: str | None = None) -> dict
```

Validate file structure against H-23/H-24 and an optional entity schema.

When a schema name is provided (e.g., "epic", "story", "enabler", "task",
"bug", "feature"), the document is validated against the corresponding
built-in entity schema from ST-006. When no schema is provided, schema
validation is skipped (schema_valid defaults to True).

**Returns dict with:**

| Key | Type | Description |
|-----|------|-------------|
| `is_valid` | bool | True only when nav and schema are both valid |
| `nav_table_valid` | bool | True if nav table exists and covers all ## headings |
| `missing_nav_entries` | list[str] | Heading texts absent from nav table |
| `orphaned_nav_entries` | list[str] | Nav entries with no matching heading |
| `schema_valid` | bool | True when schema passes or no schema provided |
| `schema` | str or None | The schema name provided |
| `schema_violations` | list[dict] | Violation dicts with field_path, expected, actual, severity, message |

**Raises:** `FileNotFoundError` if file does not exist. `ValueError` if schema name is unknown.

---

### render_file

```python
render_file(file_path: str) -> str
```

Parse a file and return it as normalized (mdformat) markdown.

**Returns:** Normalized markdown string. Empty string for empty files.

**Raises:** `FileNotFoundError` if file does not exist.

---

### extract_reinject

```python
extract_reinject(file_path: str) -> list[dict]
```

Extract all L2-REINJECT directives from a markdown file.

**Returns list of dicts, each with:**

| Key | Type | Description |
|-----|------|-------------|
| `rank` | int | Priority rank (lower = injected first) |
| `tokens` | int | Estimated token count |
| `content` | str | The reinject payload string |
| `line_number` | int | Zero-based line index |

**Raises:** `FileNotFoundError` if file does not exist.

---

### validate_nav_table_file

```python
validate_nav_table_file(file_path: str) -> dict
```

Validate H-23/H-24 navigation table compliance with serializable entry output.

**Returns dict with:**

| Key | Type | Description |
|-----|------|-------------|
| `is_valid` | bool | True if nav table exists and all headings are covered |
| `missing_entries` | list[str] | ## heading texts absent from nav table |
| `orphaned_entries` | list[str] | Section names in nav table with no matching heading |
| `entries` | list[dict] | All nav table entries (section_name, anchor, description, line_number) |

**Raises:** `FileNotFoundError` if file does not exist.

---

## Quick Reference

### Read frontmatter from a story file

```python
uv run python -c "
from skills.ast.scripts.ast_ops import query_frontmatter
fm = query_frontmatter('projects/PROJ-005-markdown-ast/work/ST-005.md')
print(fm)
"
```

### Update story status

```python
uv run python -c "
from skills.ast.scripts.ast_ops import modify_frontmatter
new_content = modify_frontmatter(
    'projects/PROJ-005-markdown-ast/work/ST-005.md',
    'Status',
    'in-progress'
)
print('Updated!')
"
```

### Validate a rule file for H-23/H-24 compliance

```python
uv run python -c "
from skills.ast.scripts.ast_ops import validate_nav_table_file
result = validate_nav_table_file('.context/rules/quality-enforcement.md')
print('Valid:', result['is_valid'])
if result['missing_entries']:
    print('Missing:', result['missing_entries'])
"
```

### Extract L2-REINJECT directives from a rule file

```python
uv run python -c "
from skills.ast.scripts.ast_ops import extract_reinject
directives = extract_reinject('.context/rules/quality-enforcement.md')
for d in directives:
    print(f'rank={d[\"rank\"]} tokens={d[\"tokens\"]}: {d[\"content\"][:60]}...')
"
```

### Parse a file and inspect its structure

```python
uv run python -c "
from skills.ast.scripts.ast_ops import parse_file
info = parse_file('.context/rules/quality-enforcement.md')
print('Length:', info['source_length'])
print('Headings:', info['heading_count'])
print('Has frontmatter:', info['has_frontmatter'])
print('Node types:', info['node_types'])
"
```

---

## Architecture Notes

### Layer Compliance

The skill scripts are in the **interface layer** (`skills/`) and are permitted to
import from the domain layer per H-07. The import chain is:

```
skills/ast/scripts/ast_ops.py   <- interface layer (skill)
    -> src.domain.markdown_ast  <- domain layer
```

The domain layer (`src/domain/markdown_ast/`) does NOT import back into the
interface layer (H-07 enforced by architecture boundary tests).

### Python Path

The `skills/` directory is on `sys.path` via `pytest.ini` (`pythonpath = .`).
For invocation outside pytest, ensure the project root is on `sys.path` or
invoke via `uv run` from the project root.

### ST-006 Schema Integration

The `validate_file()` function accepts a `schema` argument and validates the
document against the corresponding built-in entity schema from ST-006. Valid
schema names: "epic", "feature", "story", "enabler", "task", "bug". When no
schema is provided, schema validation is skipped. Schema violations are returned
as structured dicts in the `schema_violations` key.

### References

| Topic | Location |
|-------|----------|
| Domain layer exports | `src/domain/markdown_ast/__init__.py` |
| Skill scripts | `skills/ast/scripts/ast_ops.py` |
| Unit tests | `tests/unit/skills/ast/test_ast_ops.py` |
| H-23/H-24 rules | `.context/rules/markdown-navigation-standards.md` |
| Quality enforcement | `.context/rules/quality-enforcement.md` |
| ST-005 story | `projects/PROJ-005-markdown-ast/work/ST-005.md` |
