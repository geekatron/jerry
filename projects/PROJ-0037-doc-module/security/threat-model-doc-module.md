# Threat Model: Auto-Documentation Module

> **Phase:** B3 (Workstream B)
> **Agent:** eng-architect
> **Project:** PROJ-0037-doc-module
> **Date:** 2026-03-08
> **Methodology:** STRIDE

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [System Description](#system-description) | What the doc module does and its trust boundaries |
| [STRIDE Analysis](#stride-analysis) | Per-threat-category analysis |
| [Trust Boundaries](#trust-boundaries) | Where trust transitions occur |
| [Attack Surface](#attack-surface) | Entry points for adversarial input |
| [Risk Summary](#risk-summary) | Prioritized risk table |
| [Mitigations](#mitigations) | Recommended controls |

---

## System Description

The auto-documentation module (`jerry docs generate`) reads YAML frontmatter from `skills/*/SKILL.md` and `skills/*/agents/*.md` files, renders README sections via Jinja2 templates, and writes (or compares) the output to `README.md`.

```
┌─────────────────────────────────────────────────────┐
│                   TRUST BOUNDARY 1                   │
│                  (Repository Files)                  │
│                                                      │
│  skills/*/SKILL.md ─────┐                            │
│  skills/*/agents/*.md ──┤                            │
│                         ▼                            │
│              ┌──────────────────┐                    │
│              │ jerry ast        │ ◄── H-33 parser    │
│              │ frontmatter      │                    │
│              └────────┬─────────┘                    │
│                       │ structured data              │
│                       ▼                              │
│  ┌─────────────────────────────────────────┐         │
│  │           TRUST BOUNDARY 2              │         │
│  │         (Template Rendering)            │         │
│  │                                         │         │
│  │  .context/templates/docs/*.jinja2 ──┐   │         │
│  │                                     ▼   │         │
│  │              ┌──────────────────┐       │         │
│  │              │ Jinja2 Renderer  │       │         │
│  │              │ (autoescape=ON)  │       │         │
│  │              └────────┬─────────┘       │         │
│  └───────────────────────┼─────────────────┘         │
│                          │ rendered markdown          │
│                          ▼                            │
│              ┌──────────────────┐                    │
│              │ README.md        │ ◄── output         │
│              └──────────────────┘                    │
└─────────────────────────────────────────────────────┘
```

---

## STRIDE Analysis

### S — Spoofing

| Threat | Severity | Likelihood | Description |
|--------|----------|------------|-------------|
| S-1: Spoofed SKILL.md | Low | Low | An attacker with write access to the repo creates a malicious SKILL.md with a spoofed `name` field to impersonate another skill. |

**Analysis:** This requires repository write access, which already implies trust. The doc module reads from the local filesystem within the repository — no network access, no authentication. Spoofing is bounded by git access controls.

**Risk:** Low. Mitigated by existing git access controls and PR review.

### T — Tampering

| Threat | Severity | Likelihood | Description |
|--------|----------|------------|-------------|
| T-1: Malformed YAML injection | Medium | Medium | A SKILL.md file contains YAML that, when rendered into README, produces misleading or malicious content (e.g., markdown links to phishing sites). |
| T-2: Template tampering | Medium | Low | An attacker modifies Jinja2 templates in `.context/templates/docs/` to inject content into generated README. |
| T-3: Partial write corruption | Medium | Low | The generator crashes mid-write to README.md, leaving a partially written file. |

**Analysis:**
- **T-1** is the primary concern. YAML `description` fields are free-text and could contain markdown links, HTML, or other injection payloads that render in GitHub's markdown viewer. The Jinja2 renderer MUST sanitize or escape field values.
- **T-2** requires repo write access to `.context/templates/`. Same trust boundary as T-1.
- **T-3** is a real concern. Writing directly to README.md without atomicity could corrupt the file if the process is interrupted (e.g., Ctrl+C during pre-commit hook).

### R — Repudiation

| Threat | Severity | Likelihood | Description |
|--------|----------|------------|-------------|
| R-1: Untracked README changes | Low | Low | Generated README changes bypass git history if the generator overwrites without commit context. |

**Analysis:** Low concern. The generator produces content that must be staged and committed through normal git workflow. Git history provides full auditability.

### I — Information Disclosure

| Threat | Severity | Likelihood | Description |
|--------|----------|------------|-------------|
| I-1: Internal metadata leakage | Low | Medium | YAML frontmatter fields intended for internal use (e.g., `allowed-tools`, `activation-keywords`) are rendered into the public README. |

**Analysis:** The template controls which fields are rendered. The template SHOULD only render `name`, `description`, and agent count — not internal fields like `allowed-tools` or `activation-keywords`. This is a template design decision, not a runtime vulnerability.

### D — Denial of Service

| Threat | Severity | Likelihood | Description |
|--------|----------|------------|-------------|
| D-1: Pathological YAML | Low | Low | A SKILL.md with extremely large YAML frontmatter (megabytes) causes the parser to consume excessive memory or time. |
| D-2: Template rendering loop | Low | Low | A Jinja2 template with recursive includes or unbounded loops causes the renderer to hang. |

**Analysis:** Both are theoretical. Jerry's `jerry ast frontmatter` processes files that are typically < 10KB. Jinja2 has configurable sandbox and rendering limits. The pre-commit hook has a natural timeout.

### E — Elevation of Privilege

| Threat | Severity | Likelihood | Description |
|--------|----------|------------|-------------|
| E-1: Jinja2 template code execution | High | Low | If Jinja2 templates are rendered without sandboxing, template expressions could execute arbitrary Python code. |
| E-2: Supply chain attack via Jinja2 dependency | Medium | Low | A compromised Jinja2 package could execute arbitrary code during template rendering. |

**Analysis:**
- **E-1:** Jinja2's `SandboxedEnvironment` prevents access to dangerous Python builtins. The generator MUST use `SandboxedEnvironment`, not the default `Environment`.
- **E-2:** Jinja2 is maintained by the Pallets project (same maintainers as Flask). It has 65K+ GitHub stars, regular security releases, and broad industry adoption. Risk is low but not zero. Pin the dependency version in `pyproject.toml`.

---

## Trust Boundaries

| Boundary | From | To | Trust Level |
|----------|------|----|-------------|
| TB-1 | Repository files (`skills/*/`) | `jerry ast` parser | High — files are version-controlled and PR-reviewed |
| TB-2 | Parsed YAML data | Jinja2 renderer | Medium — data content is trusted but should be sanitized for output context (markdown) |
| TB-3 | Jinja2 templates (`.context/templates/docs/`) | Jinja2 renderer | High — templates are version-controlled |
| TB-4 | Rendered output | README.md | High — output is text, written to a file already under version control |

---

## Attack Surface

| Entry Point | Input Type | Validation Required |
|-------------|-----------|---------------------|
| `skills/*/SKILL.md` YAML frontmatter | YAML text (name, description, version, keywords) | Schema validation: field types, max lengths |
| `skills/*/agents/*.md` YAML frontmatter | YAML text (name, description, model, tools) | Schema validation: field types, max lengths |
| `.context/templates/docs/*.jinja2` | Jinja2 template files | Version-controlled; review at PR time |
| CLI arguments (`--write`, `--check`) | Command-line flags | Standard CLI argument parsing (click/argparse) |

---

## Risk Summary

| ID | Threat | Severity | Likelihood | Risk | Mitigation Priority |
|----|--------|----------|------------|------|---------------------|
| T-1 | YAML injection into README | Medium | Medium | **Medium** | High — implement in v1.0 |
| E-1 | Jinja2 code execution | High | Low | **Medium** | High — use SandboxedEnvironment |
| T-3 | Partial write corruption | Medium | Low | **Low** | Medium — atomic write pattern |
| E-2 | Jinja2 supply chain | Medium | Low | **Low** | Medium — pin dependency version |
| I-1 | Internal metadata in README | Low | Medium | **Low** | Low — template design controls this |
| D-1 | Pathological YAML | Low | Low | **Negligible** | Low — file size check |

---

## Mitigations

### M-1: Sanitize YAML field values before rendering (T-1)

Escape markdown-significant characters in extracted `description` fields before passing to Jinja2. Specifically:
- Strip or escape raw HTML tags
- Validate URLs in description fields against an allowlist (e.g., must be relative paths or `https://` to known domains)
- Enforce maximum field length (e.g., `description` <= 1024 chars, per H-28)

### M-2: Use Jinja2 `SandboxedEnvironment` (E-1)

```python
from jinja2.sandbox import SandboxedEnvironment

env = SandboxedEnvironment(
    loader=FileSystemLoader(template_dir),
    autoescape=False,  # Output is markdown, not HTML
    undefined=StrictUndefined,  # Fail on missing variables
)
```

### M-3: Atomic write pattern (T-3)

Write to a temporary file in the same directory, then `os.replace()` to the target path. This is atomic on POSIX systems. On Windows, use `os.replace()` which is atomic in Python 3.3+.

```python
import tempfile
import os

def atomic_write(target_path: str, content: str) -> None:
    dir_name = os.path.dirname(target_path)
    with tempfile.NamedTemporaryFile(mode='w', dir=dir_name, delete=False, suffix='.tmp') as f:
        f.write(content)
        temp_path = f.name
    os.replace(temp_path, target_path)
```

### M-4: Pin Jinja2 dependency version (E-2)

In `pyproject.toml`, pin to a specific minor version:
```toml
[project]
dependencies = [
    "jinja2>=3.1,<3.2",
]
```

### M-5: YAML field schema validation (T-1, D-1)

Before rendering, validate extracted YAML fields against expected types and sizes:
- `name`: string, max 100 chars, matches `^[a-z][a-z0-9-]*$`
- `description`: string, max 1024 chars
- `version`: string, matches `^\d+\.\d+\.\d+$`
- `activation-keywords`: array of strings, max 30 entries

Reject files that fail validation with a clear error message including the file path.
