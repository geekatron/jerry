# Implementation Specification: Auto-Documentation Module

> **Phase:** B4 (Workstream B)
> **Agent:** ps-analyst
> **Project:** PROJ-0037-doc-module
> **Date:** 2026-03-08
> **Input:** ADR-PROJ0037-001 (Option A selected), Threat Model

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Overview](#overview) | Module purpose and scope |
| [Input Parsing](#input-parsing) | YAML frontmatter extraction specification |
| [Output Rendering](#output-rendering) | Jinja2 template structure and README sections |
| [Drift Detection](#drift-detection) | Comparison algorithm and exit codes |
| [Error Handling](#error-handling) | Malformed input, missing fields, empty directories |
| [Integration Points](#integration-points) | CLI, pre-commit hook, CI workflow |
| [File Structure](#file-structure) | Module layout and class responsibilities |
| [Test Plan](#test-plan) | Unit, integration, and golden-file tests |
| [Security Controls](#security-controls) | Mitigations from threat model |

---

## Overview

The auto-documentation module extends the Jerry CLI with a `docs generate` subcommand that:
1. Extracts YAML frontmatter from all `skills/*/SKILL.md` and `skills/*/agents/*.md` files
2. Renders README sections (skills table, features section) via Jinja2 templates
3. Compares generated output against current README.md to detect drift
4. Optionally writes the generated output to README.md

**Scope boundary:** The module generates the **skills table** and **features bullet list** sections of README.md. All other sections (intro, installation, platform support, known limitations, documentation table, contributor guide, references, license) remain manually authored.

---

## Input Parsing

### Extraction Pipeline

```
1. Glob: skills/*/SKILL.md → list of skill paths
2. For each skill path:
   a. jerry ast frontmatter → {name, description, version, activation-keywords, agents?}
   b. Glob: skills/{name}/agents/*.md (exclude *TEMPLATE*, *EXTENSION*)
   c. For each agent path:
      jerry ast frontmatter → {name, description, model, tools}
   d. Assemble SkillData(name, description, version, agent_count, agents[])
3. Sort skills alphabetically by name
4. Return list[SkillData]
```

### Data Models

```python
@dataclass
class AgentData:
    """Extracted agent metadata from YAML frontmatter."""
    name: str
    description: str
    model: str
    file_path: str

@dataclass
class SkillData:
    """Extracted skill metadata with agent inventory."""
    name: str
    description: str
    version: str
    agent_count: int
    agents: list[AgentData]
    file_path: str
```

### YAML Fields Extracted

**From SKILL.md:**

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `name` | str | Yes | `^[a-zA-Z][a-zA-Z0-9-]*$`, max 100 chars |
| `description` | str | Yes | Max 1024 chars, no raw HTML |
| `version` | str | Yes | `^\d+\.\d+\.\d+$` |
| `activation-keywords` | list[str] | No | Max 30 entries (not rendered in README) |

**From agent .md files:**

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `name` | str | Yes | `^[a-z][a-z0-9-]*$`, max 100 chars |
| `description` | str | Yes | Max 1024 chars |
| `model` | str | No | One of: `sonnet`, `opus`, `haiku` |

### Exclusion Rules

Files matching these patterns are excluded from agent counting:
- `*TEMPLATE*` (e.g., `PS_AGENT_TEMPLATE.md`, `NSE_AGENT_TEMPLATE.md`)
- `*EXTENSION*` (e.g., `PS_EXTENSION.md`, `NSE_EXTENSION.md`)

This matches the exclusion logic documented in AGENTS.md (4 files excluded, 58 invokable agents).

---

## Output Rendering

### Template Structure

```
.context/templates/docs/
├── skills-table.md.jinja2      # Skills table section
├── features-section.md.jinja2  # Features bullet list
└── _macros.jinja2              # Shared Jinja2 macros
```

### Skills Table Template (`skills-table.md.jinja2`)

```jinja
| Skill | Purpose | Example |
|-------|---------|---------|
{% for skill in skills %}
| `/{{ skill.name }}` | {{ skill.description | truncate(60) }} | {{ skill.example }} |
{% endfor %}
```

**Example mapping:** Each skill needs a one-line example. These are stored in a static mapping file (`.context/templates/docs/skill-examples.yaml`) to avoid extracting examples from SKILL.md (which would require parsing beyond frontmatter):

```yaml
problem-solving: '"Research OAuth2 patterns"'
worktracker: '"Create a task for login feature"'
nasa-se: '"Define requirements for API"'
# ... etc
```

### Features Section Template (`features-section.md.jinja2`)

```jinja
- **{{ total_agents }} Specialized Agents** across {{ total_skills }} skills — from research and analysis to security testing and infrastructure hardening. See [AGENTS.md](AGENTS.md) for the full registry.
{% for feature in features %}
- **{{ feature.title }}**: {{ feature.description }}
{% endfor %}
```

Features are a curated list (not auto-generated from skills) stored in `.context/templates/docs/features.yaml`:

```yaml
- title: "Structured Problem-Solving"
  description: "9 agents (researcher, analyst, architect, validator, synthesizer, reviewer, critic, investigator, reporter) with adversarial quality gates"
# ... etc
```

### README Integration

The generated sections are injected into README.md between marker comments:

```markdown
<!-- BEGIN:GENERATED:SKILLS_TABLE -->
| Skill | Purpose | Example |
...
<!-- END:GENERATED:SKILLS_TABLE -->

<!-- BEGIN:GENERATED:FEATURES -->
- **58 Specialized Agents** across 13 skills...
...
<!-- END:GENERATED:FEATURES -->
```

Non-generated sections remain untouched. The generator:
1. Reads current README.md
2. Finds marker comment pairs
3. Replaces content between markers with generated content
4. Preserves everything outside markers

---

## Drift Detection

### Algorithm

```python
def check_drift(readme_path: str, generated_sections: dict[str, str]) -> bool:
    """Return True if drift is detected (content differs from generated), False if content matches."""
    current = read_file(readme_path)
    for section_name, generated_content in generated_sections.items():
        begin_marker = f"<!-- BEGIN:GENERATED:{section_name} -->"
        end_marker = f"<!-- END:GENERATED:{section_name} -->"
        current_section = extract_between(current, begin_marker, end_marker)
        if current_section.strip() != generated_content.strip():
            return True
    return False
```

### Exit Codes

| Code | Meaning | When |
|------|---------|------|
| 0 | No drift | `--check` mode: README matches generated output |
| 0 | Write success | `--write` mode: README updated successfully |
| 1 | Drift detected | `--check` mode: README differs from generated output |
| 2 | Parse error | YAML frontmatter is malformed or missing required fields |
| 3 | Template error | Jinja2 template has syntax errors |

---

## Error Handling

| Error Condition | Behavior | Exit Code |
|-----------------|----------|-----------|
| SKILL.md missing `name` field | Log warning with file path; skip this skill | 2 |
| SKILL.md missing `description` field | Log warning with file path; use `"(no description)"` | 0 (warning) |
| Agent .md missing `name` field | Log warning with file path; skip this agent | 2 |
| `description` exceeds 1024 chars | Truncate to 1024 chars; log warning | 0 (warning) |
| `description` contains raw HTML tags | Strip HTML tags; log warning | 0 (warning) |
| No SKILL.md files found in `skills/` | Error: "No skills found in skills/ directory" | 2 |
| Jinja2 template not found | Error: "Template not found: {template_path}" | 3 |
| README.md missing marker comments | Error: "Marker not found: {marker_name}. Add <!-- BEGIN:GENERATED:{name} --> and <!-- END:GENERATED:{name} --> markers to README.md" | 2 |
| README.md does not exist (with `--write`) | Create new README.md with markers and generated content | 0 |

---

## Integration Points

### CLI Command

```bash
# Check for drift (pre-commit hook mode)
uv run jerry docs generate --check

# Write generated sections to README.md
uv run jerry docs generate --write

# Print generated sections to stdout (development/debug)
uv run jerry docs generate

# Specify custom README path
uv run jerry docs generate --readme path/to/README.md --check
```

### Pre-Commit Hook

Add to `.pre-commit-config.yaml` or Jerry's hook registration:

```python
# scripts/check_docs.py
"""Pre-commit hook: verify README documentation sections are current."""
import subprocess
import sys

result = subprocess.run(
    ["uv", "run", "jerry", "docs", "generate", "--check"],
    capture_output=True,
    text=True,
)

if result.returncode == 1:
    print("README.md documentation sections are out of date.")
    print("Run: uv run jerry docs generate --write")
    print(result.stdout)
    sys.exit(1)
elif result.returncode > 1:
    print(f"Documentation generation error: {result.stderr}")
    sys.exit(1)
```

### CI Workflow

```yaml
# .github/workflows/docs-check.yml
name: Documentation Check
on: [push, pull_request]
jobs:
  docs-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
      - run: uv sync
      - run: uv run jerry docs generate --check
```

---

## File Structure

> **Note:** Layout follows hexagonal architecture per H-07. Departed from the original flat layout to align with the established Jerry architecture pattern.

```
src/docs/
├── __init__.py
├── domain/
│   ├── ports/
│   │   ├── frontmatter_reader.py   # IFrontmatterReader Protocol
│   │   └── template_renderer.py     # ITemplateRenderer Protocol
│   └── value_objects/
│       ├── skill_data.py            # SkillData frozen dataclass
│       └── agent_data.py            # AgentData frozen dataclass
├── application/
│   ├── commands/
│   │   └── generate_docs_command.py # Command DTO
│   ├── results/
│   │   └── generate_docs_result.py  # Result DTO
│   ├── handlers/
│   │   └── commands/
│   │       └── generate_docs_command_handler.py  # Orchestration handler
│   └── services/
│       └── skill_extractor.py       # Metadata extraction service
└── infrastructure/
    └── adapters/
        ├── jinja2_renderer.py       # ITemplateRenderer implementation
        └── ast_frontmatter_reader.py # IFrontmatterReader implementation

.context/templates/docs/
├── skills-table.md.jinja2        # Skills table template
├── features-section.md.jinja2    # Features section template
├── skill-examples.yaml           # Static skill example mapping
├── features.yaml                 # Curated features list
└── _macros.jinja2                # Shared Jinja2 macros

scripts/
└── check_docs.py                 # Pre-commit hook script
```

### Class Responsibilities

| Class | File | Responsibility |
|-------|------|---------------|
| `GenerateDocsCommandHandler` | `application/handlers/commands/generate_docs_command_handler.py` | Orchestrates extraction → rendering → drift check → write. Entry point for CLI command. |
| `SkillExtractor` | `application/services/skill_extractor.py` | Globs for SKILL.md and agent files, calls `jerry ast frontmatter`, returns `list[SkillData]`. Handles exclusion rules and validation. |
| `Jinja2Renderer` | `infrastructure/adapters/jinja2_renderer.py` | Loads Jinja2 templates, renders sections, injects between markers. Uses `SandboxedEnvironment`. |
| `AstFrontmatterReader` | `infrastructure/adapters/ast_frontmatter_reader.py` | Reads YAML frontmatter via `jerry ast frontmatter` subprocess (H-33). |
| `SkillData` | `domain/value_objects/skill_data.py` | Frozen dataclass for skill metadata. |
| `AgentData` | `domain/value_objects/agent_data.py` | Frozen dataclass for agent metadata. |
| `IFrontmatterReader` | `domain/ports/frontmatter_reader.py` | Protocol defining the frontmatter reader port. |
| `ITemplateRenderer` | `domain/ports/template_renderer.py` | Protocol defining the template renderer port. |

---

## Test Plan

### Unit Tests

| Test | File | What It Verifies |
|------|------|-----------------|
| `test_extract_skill_frontmatter` | `tests/unit/docs/test_extractor.py` | SkillExtractor correctly parses SKILL.md YAML frontmatter |
| `test_extract_agent_frontmatter` | `tests/unit/docs/test_extractor.py` | SkillExtractor correctly parses agent .md YAML frontmatter |
| `test_exclude_template_files` | `tests/unit/docs/test_extractor.py` | Files matching `*TEMPLATE*` and `*EXTENSION*` are excluded from agent count |
| `test_validation_rejects_missing_name` | `tests/unit/docs/test_extractor.py` | SkillExtractor raises/logs error when `name` is missing |
| `test_validation_strips_html` | `tests/unit/docs/test_extractor.py` | HTML tags in `description` are stripped |
| `test_render_skills_table` | `tests/unit/docs/test_renderer.py` | ReadmeRenderer produces correct markdown table from SkillData list |
| `test_render_features_section` | `tests/unit/docs/test_renderer.py` | ReadmeRenderer produces correct features bullets |
| `test_inject_between_markers` | `tests/unit/docs/test_renderer.py` | Content between markers is replaced; content outside markers is preserved |
| `test_missing_markers_error` | `tests/unit/docs/test_renderer.py` | Error raised when markers are not found in README |
| `test_atomic_write` | `tests/unit/docs/test_generator.py` | Atomic write pattern works (write to temp, replace) |

### Integration Tests

| Test | File | What It Verifies |
|------|------|-----------------|
| `test_end_to_end_generate` | `tests/integration/docs/test_docs_generate.py` | Full pipeline: glob → extract → render → compare against expected output |
| `test_check_mode_detects_drift` | `tests/integration/docs/test_docs_generate.py` | `--check` returns exit code 1 when README differs |
| `test_check_mode_passes_when_current` | `tests/integration/docs/test_docs_generate.py` | `--check` returns exit code 0 when README matches |
| `test_write_mode_updates_readme` | `tests/integration/docs/test_docs_generate.py` | `--write` updates README.md and subsequent `--check` passes |

### Golden File Tests

| Test | File | What It Verifies |
|------|------|-----------------|
| `test_golden_skills_table` | `tests/golden/docs/test_golden.py` | Generated skills table matches `tests/golden/docs/expected-skills-table.md` |
| `test_golden_features_section` | `tests/golden/docs/test_golden.py` | Generated features section matches `tests/golden/docs/expected-features.md` |

**Golden file update process:** When skills or agents are added, run `uv run pytest tests/golden/docs/ --update-golden` to regenerate expected files. Review the diff before committing.

---

## Security Controls

Per threat model (Phase B3):

| ID | Mitigation | Implementation |
|----|-----------|----------------|
| M-1 | Sanitize YAML fields | `SkillExtractor` validates field types, lengths, strips HTML |
| M-2 | Sandboxed Jinja2 | `ReadmeRenderer` uses `SandboxedEnvironment` with `StrictUndefined` |
| M-3 | Atomic writes | `DocsGenerator` uses `tempfile` + `os.replace()` pattern |
| M-4 | Pinned Jinja2 version | `pyproject.toml`: `jinja2>=3.1,<3.2` |
| M-5 | Schema validation | `SkillExtractor` validates against field constraints before rendering |
