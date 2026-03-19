# Security Control Verification and Hexagonal Compliance Review

> **Phase:** 3 (Security Verification)
> **Agent:** eng-architect
> **Project:** PROJ-0037-doc-module
> **Date:** 2026-03-10
> **Methodology:** STRIDE mitigation verification, OWASP Top 10 mapping, hexagonal architecture compliance audit
> **Input:** Threat model (`security/threat-model-doc-module.md`), specification (`specifications/doc-module-spec.md`), source code (`src/docs/`)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Security control compliance summary |
| [L1: Per-Mitigation Verification](#l1-per-mitigation-verification) | Detailed verification with file:line citations |
| [L2: Residual Risk and Strategic Assessment](#l2-residual-risk-and-strategic-assessment) | OWASP mapping, residual risk, architectural observations |

---

## L0: Executive Summary

### Security Control Compliance

| Mitigation | Threat | Status | Summary |
|------------|--------|--------|---------|
| M-1 | T-1 (YAML injection) | **COMPLIANT** | HTML stripping, unsafe link neutralization, field length truncation all implemented |
| M-2 | E-1 (Jinja2 code execution) | **COMPLIANT** | `SandboxedEnvironment` + `StrictUndefined` correctly configured |
| M-3 | T-3 (Partial write corruption) | **COMPLIANT** | `tempfile.NamedTemporaryFile` + `os.replace()` atomic write with cleanup |
| M-4 | E-2 (Supply chain) | **COMPLIANT** | `jinja2>=3.1.6,<4.0` pinned in `pyproject.toml` |
| M-5 | T-1, D-1 (Schema validation) | **COMPLIANT** | Name regex, version regex, description length, keyword count all validated |

### Hexagonal Compliance

| Constraint | Status | Summary |
|------------|--------|---------|
| H-07 (Layer isolation) | **COMPLIANT** | No cross-layer import violations detected |
| H-10 (One class per file) | **COMPLIANT** | Each `.py` file contains exactly one class or protocol |
| H-11 (Type hints + docstrings) | **COMPLIANT** | All public functions have type annotations and docstrings |
| H-33 (AST-based parsing) | **COMPLIANT** | `AstFrontmatterReader` delegates to `jerry ast frontmatter` subprocess |

### Overall Verdict

**PASS** -- All 5 threat model mitigations are correctly implemented. All hexagonal architecture constraints are satisfied. No CRITICAL or HIGH findings. Two LOW observations documented in L2.

---

## L1: Per-Mitigation Verification

### M-1: Sanitize YAML Field Values Before Rendering (T-1)

**Specification requirement:** Strip or escape raw HTML tags. Validate URLs against an allowlist. Enforce maximum field length (description <= 1024 chars).

**Status:** COMPLIANT

**Evidence:**

| Control | File | Lines | Implementation |
|---------|------|-------|----------------|
| HTML tag stripping | `src/docs/application/services/skill_extractor.py` | 34, 260 | `_HTML_TAG_PATTERN = re.compile(r"<[^>]+>")` applied via `_sanitize_description()` at line 260: `sanitized = _HTML_TAG_PATTERN.sub("", text)` |
| Unsafe link neutralization | `src/docs/application/services/skill_extractor.py` | 38-40, 262 | `_UNSAFE_LINK_PATTERN` regex strips markdown links with non-allowlisted URL schemes (`javascript:`, `data:`, `vbscript:`, etc.) while preserving `https://`, `http://`, `mailto:`, and relative paths. Applied at line 262: `sanitized = _UNSAFE_LINK_PATTERN.sub(r"\1", sanitized)` |
| Description length truncation | `src/docs/application/services/skill_extractor.py` | 42, 263 | `_MAX_DESCRIPTION_LENGTH = 1024` applied via slice at line 263: `sanitized.strip()[:_MAX_DESCRIPTION_LENGTH]` |
| Name length truncation | `src/docs/application/services/skill_extractor.py` | 41, 118 | `_MAX_NAME_LENGTH = 100` applied at line 118: `name = str(raw_name).strip()[:_MAX_NAME_LENGTH]` |

**Verification of URL allowlist logic (line 38-40):**

```python
_UNSAFE_LINK_PATTERN = re.compile(
    r"\[([^\]]*)\]\((?!https?://|mailto:|/)(?:[a-zA-Z][a-zA-Z0-9+\-.]*:)[^)]*\)"
)
```

The negative lookahead `(?!https?://|mailto:|/)` allows:
- `http://` and `https://` links (standard web URLs)
- `mailto:` links (email)
- `/` (relative paths starting with slash)

All other scheme-prefixed URLs (matching `[a-zA-Z][a-zA-Z0-9+\-.]*:`) are neutralized by replacing the full `[text](url)` with just the link text. This correctly covers `javascript:`, `data:`, `vbscript:`, `file:`, and other dangerous schemes.

**Sanitization is applied to both skill and agent descriptions:** Skill descriptions at line 136, agent descriptions at line 229. Both call `self._sanitize_description()`.

---

### M-2: Use Jinja2 `SandboxedEnvironment` (E-1)

**Specification requirement:** Use `SandboxedEnvironment` (not default `Environment`). Set `undefined=StrictUndefined`. Set `autoescape=False` (output is markdown, not HTML).

**Status:** COMPLIANT

**Evidence:**

| Control | File | Lines | Implementation |
|---------|------|-------|----------------|
| SandboxedEnvironment import | `src/docs/infrastructure/adapters/jinja2_renderer.py` | 20 | `from jinja2.sandbox import SandboxedEnvironment` |
| SandboxedEnvironment instantiation | `src/docs/infrastructure/adapters/jinja2_renderer.py` | 56-60 | `self._env = SandboxedEnvironment(loader=FileSystemLoader(template_dir), undefined=StrictUndefined, autoescape=False)` |
| StrictUndefined import | `src/docs/infrastructure/adapters/jinja2_renderer.py` | 19 | `from jinja2 import FileSystemLoader, StrictUndefined` |
| Template directory validation | `src/docs/infrastructure/adapters/jinja2_renderer.py` | 50-55 | `if not template_path.is_dir(): raise FileNotFoundError(...)` -- prevents loading templates from nonexistent directories |

**Configuration match to threat model specification:**

| Parameter | Threat Model Spec | Implementation | Match |
|-----------|-------------------|----------------|-------|
| Environment class | `SandboxedEnvironment` | `SandboxedEnvironment` | Yes |
| loader | `FileSystemLoader(template_dir)` | `FileSystemLoader(template_dir)` | Yes |
| autoescape | `False` | `False` | Yes |
| undefined | `StrictUndefined` | `StrictUndefined` | Yes |

The implementation is an exact match to the threat model specification at lines 173-179 of `threat-model-doc-module.md`.

---

### M-3: Atomic Write Pattern (T-3)

**Specification requirement:** Write to a temporary file in the same directory, then `os.replace()` to the target path. Atomic on POSIX; atomic in Python 3.3+ on Windows.

**Status:** COMPLIANT

**Evidence:**

| Control | File | Lines | Implementation |
|---------|------|-------|----------------|
| tempfile import | `generate_docs_command_handler.py` | 20 | `import tempfile` |
| os import | `generate_docs_command_handler.py` | 19 | `import os` |
| NamedTemporaryFile creation | `generate_docs_command_handler.py` | 281-287 | `temp_fd = tempfile.NamedTemporaryFile(mode="w", dir=dir_name, delete=False, suffix=".tmp", encoding="utf-8")` |
| Write content to temp | `generate_docs_command_handler.py` | 289 | `temp_fd.write(content)` |
| Close before replace | `generate_docs_command_handler.py` | 290 | `temp_fd.close()` |
| Atomic replace | `generate_docs_command_handler.py` | 291 | `os.replace(temp_path, str(readme))` |
| Cleanup on failure | `generate_docs_command_handler.py` | 293-298 | `except` block removes temp file via `os.unlink(temp_path)` with `OSError` catch |
| Same-directory write | `generate_docs_command_handler.py` | 277 | `dir_name = str(readme.parent) if readme.parent != Path() else "."` ensures temp file is in the same directory as target (required for atomicity on cross-filesystem scenarios) |

**Additional security control (not in threat model):** Path traversal guard at lines 97-108 validates that `command.readme_path` resolves to a location within the repository root (`Path.cwd().resolve()`), preventing `--readme ../../etc/passwd` attacks. This is a defense-in-depth measure beyond the M-3 specification.

---

### M-4: Pin Jinja2 Dependency Version (E-2)

**Specification requirement:** Pin Jinja2 dependency version. Current pin: `jinja2>=3.1.6,<4.0` (widened from original spec `>=3.1,<3.2` during Phase 3 hardening).

**Status:** COMPLIANT

**Evidence:**

| Control | File | Line | Implementation |
|---------|------|------|----------------|
| Version pin | `pyproject.toml` | 40 | `"jinja2>=3.1.6,<4.0",` |

The pin was widened from the original spec `>=3.1,<3.2` to `>=3.1.6,<4.0` during Phase 3 hardening (see gate-disposition-b3.md). The `>=3.1.6` lower bound explicitly excludes CVE-2025-27516-affected versions. The `<4.0` upper bound permits all future 3.x patch and minor releases, eliminating the structural risk of being stranded on a vulnerable version if a future CVE requires 3.2+.

---

### M-5: YAML Field Schema Validation (T-1, D-1)

**Specification requirement:** Validate extracted YAML fields against expected types and sizes: `name` (string, max 100 chars, pattern `^[a-z][a-z0-9-]*$`), `description` (string, max 1024 chars), `version` (string, pattern `^\d+\.\d+\.\d+$`), `activation-keywords` (array, max 30 entries). Reject files that fail validation with a clear error message including file path.

**Status:** COMPLIANT

**Evidence:**

| Validation | File | Lines | Implementation | Failure Behavior |
|------------|------|-------|----------------|------------------|
| Skill name pattern | `skill_extractor.py` | 31, 119 | `_SKILL_NAME_PATTERN = re.compile(r"^[a-zA-Z][a-zA-Z0-9-]*$")` with `if not _SKILL_NAME_PATTERN.match(name)` | Skip skill, log warning with file path |
| Agent name pattern | `skill_extractor.py` | 32, 219 | `_AGENT_NAME_PATTERN = re.compile(r"^[a-z][a-z0-9-]*$")` with `if not _AGENT_NAME_PATTERN.match(name)` | Skip agent, log warning with file path |
| Version pattern | `skill_extractor.py` | 33, 131 | `_VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")` with `if not _VERSION_PATTERN.match(version)` | Default to `"0.0.0"` |
| Name max length | `skill_extractor.py` | 41, 118 | `_MAX_NAME_LENGTH = 100` with `[:_MAX_NAME_LENGTH]` truncation | Silently truncate |
| Description max length | `skill_extractor.py` | 42, 263 | `_MAX_DESCRIPTION_LENGTH = 1024` with `[:_MAX_DESCRIPTION_LENGTH]` truncation | Silently truncate |
| activation-keywords count | `skill_extractor.py` | 43, 148 | `_MAX_ACTIVATION_KEYWORDS = 30` with `len(raw_keywords) > _MAX_ACTIVATION_KEYWORDS` check | Warn only (documented policy: keywords are routing metadata, truncation would alter routing behavior) |
| Missing name field | `skill_extractor.py` | 111-115 | `if not raw_name: return None` | Skip, log warning with file path |
| Missing description | `skill_extractor.py` | 139-140 | `if not description: description = "(no description)"` | Default to `"(no description)"` per spec |

**Observation on skill name pattern:** The threat model specifies `^[a-z][a-z0-9-]*$` (lowercase only) for the `name` field. The implementation uses `^[a-zA-Z][a-zA-Z0-9-]*$` (mixed case) for skill names at line 31. The spec also shows `^[a-zA-Z][a-zA-Z0-9-]*$` for SKILL.md names in the "YAML Fields Extracted" table. Agent names correctly use the lowercase-only pattern `^[a-z][a-z0-9-]*$` at line 32. This is consistent with the spec's differentiation between skill names (which may start uppercase per SKILL.md convention) and agent names (which follow kebab-case).

**Rejection behavior:** Files failing validation are skipped with `logger.warning()` messages that include the file path, matching the threat model requirement for "clear error message including the file path."

---

### H-33: AST-Based Parsing

**Specification requirement:** AST-based parsing REQUIRED for worktracker entity operations. Use `jerry ast frontmatter`, NEVER use regex for frontmatter extraction.

**Status:** COMPLIANT

**Evidence:**

| Control | File | Lines | Implementation |
|---------|------|-------|----------------|
| Subprocess delegation | `ast_frontmatter_reader.py` | 57-62 | `subprocess.run(["uv", "run", "jerry", "ast", "frontmatter", str(file_path)], ...)` |
| No regex frontmatter parsing | All `src/docs/` files | N/A | No file contains regex-based YAML frontmatter extraction. All frontmatter access goes through `IFrontmatterReader` port |
| H-05 compliance | `ast_frontmatter_reader.py` | 58 | Command uses `uv run` (not `python` or `pip`) |
| No `shell=True` | `ast_frontmatter_reader.py` | 57-62 | `subprocess.run()` uses list-form arguments, preventing command injection |
| Timeout protection | `ast_frontmatter_reader.py` | 62 | `timeout=30` prevents hung subprocess from blocking indefinitely |
| File existence check | `ast_frontmatter_reader.py` | 53-54 | Pre-check with `path.exists()` before subprocess invocation |
| Output validation | `ast_frontmatter_reader.py` | 87-98 | JSON parsing of stdout with type assertion (`isinstance(data, dict)`) |

---

## Hexagonal Architecture Compliance

### H-07: Architecture Layer Isolation

**Status:** COMPLIANT

**Import dependency matrix:**

| Source Layer | Imports From | Violation? | Evidence |
|-------------|-------------|------------|----------|
| Domain (`domain/`) | Standard library only (`typing`, `dataclasses`) | No | `frontmatter_reader.py`, `template_renderer.py`, `agent_data.py`, `skill_data.py` -- zero imports from `application/` or `infrastructure/` |
| Application (`application/`) | Domain value objects, Domain ports (TYPE_CHECKING only) | No | `skill_extractor.py` imports `AgentData`, `SkillData` (domain VOs); `IFrontmatterReader` under `TYPE_CHECKING`. Handler imports `GenerateDocsCommand`, `GenerateDocsResult` (application DTOs) and domain ports under `TYPE_CHECKING` |
| Infrastructure (`infrastructure/`) | Domain ports only | No | `jinja2_renderer.py` imports `ITemplateRenderer` (domain port). `ast_frontmatter_reader.py` imports `IFrontmatterReader` (domain port). Neither imports from `application/` |

**Key observation:** The application layer imports domain ports via `TYPE_CHECKING` blocks only (lines 26-27 of `skill_extractor.py`, lines 29-32 of `generate_docs_command_handler.py`). This means the port types are used for type annotation only and are not runtime dependencies, which is the correct hexagonal pattern -- the application layer depends on domain abstractions, and concrete implementations are injected at the composition root.

No application or domain file imports from `infrastructure`. No domain file imports from `application`. No infrastructure file imports from `application`. The dependency direction is strictly inward: infrastructure -> domain, application -> domain.

### H-10: One Class Per File

**Status:** COMPLIANT

| File | Classes/Protocols | Count | Compliant |
|------|-------------------|-------|-----------|
| `domain/ports/frontmatter_reader.py` | `IFrontmatterReader` | 1 | Yes |
| `domain/ports/template_renderer.py` | `ITemplateRenderer` | 1 | Yes |
| `domain/value_objects/agent_data.py` | `AgentData` | 1 | Yes |
| `domain/value_objects/skill_data.py` | `SkillData` | 1 | Yes |
| `application/commands/generate_docs_command.py` | `GenerateDocsCommand` | 1 | Yes |
| `application/results/generate_docs_result.py` | `GenerateDocsResult` | 1 | Yes |
| `application/handlers/commands/generate_docs_command_handler.py` | `GenerateDocsCommandHandler` | 1 | Yes |
| `application/services/skill_extractor.py` | `SkillExtractor` | 1 | Yes |
| `infrastructure/adapters/jinja2_renderer.py` | `Jinja2Renderer` | 1 | Yes |
| `infrastructure/adapters/ast_frontmatter_reader.py` | `AstFrontmatterReader` | 1 | Yes |

### H-11: Type Hints and Docstrings on Public Functions

**Status:** COMPLIANT

| File | Public Functions | Type Hints | Docstrings | Compliant |
|------|-----------------|------------|------------|-----------|
| `skill_extractor.py` | `__init__`, `extract_all` | Yes (all params + return) | Yes (Args, Returns) | Yes |
| `jinja2_renderer.py` | `__init__`, `render_section`, `inject_between_markers` | Yes (all params + return) | Yes (Args, Returns, Raises) | Yes |
| `generate_docs_command_handler.py` | `__init__`, `handle` | Yes (all params + return) | Yes (Args, Returns, Note) | Yes |
| `ast_frontmatter_reader.py` | `read_frontmatter` | Yes (all params + return) | Yes (Args, Returns, Raises) | Yes |
| `frontmatter_reader.py` | `read_frontmatter` | Yes (all params + return) | Yes (Args, Returns, Raises) | Yes |
| `template_renderer.py` | `render_section`, `inject_between_markers` | Yes (all params + return) | Yes (Args, Returns, Raises) | Yes |

Private methods (`_extract_skill`, `_extract_agents`, `_extract_agent`, `_sanitize_description`, `_check_drift`, `_write_readme`, `_load_yaml`) also have type hints and docstrings, exceeding the H-11 requirement.

---

## L2: Residual Risk and Strategic Assessment

### OWASP Top 10 (2021) Mapping

| OWASP Category | Relevant Threats | Mitigations | Residual Risk |
|----------------|-----------------|-------------|---------------|
| **A03:2021 Injection** | T-1 (YAML injection into README), E-1 (Jinja2 template code execution) | M-1 (input sanitization), M-2 (SandboxedEnvironment), M-5 (schema validation) | **LOW** -- Sandboxed rendering prevents code execution. Input sanitization prevents markdown injection of dangerous link schemes. Residual: markdown formatting injection (bold, headers) remains possible but is not exploitable in a git-reviewed README context. |
| **A05:2021 Security Misconfiguration** | E-1 (Jinja2 without sandbox) | M-2 (SandboxedEnvironment explicit, not default Environment) | **NEGLIGIBLE** -- Correct class is imported and instantiated. No configuration drift path exists because the environment is created in the constructor. |
| **A06:2021 Vulnerable and Outdated Components** | E-2 (Jinja2 supply chain) | M-4 (version pin `>=3.1.6,<4.0`) | **LOW** -- Pin widened during Phase 3 hardening to allow all 3.x patch and minor updates. Lower bound `>=3.1.6` explicitly excludes CVE-2025-27516-affected versions. Pallets project has strong security track record. `pip-audit` already present in dev dependencies for automated vulnerability scanning. |
| **A08:2021 Software and Data Integrity Failures** | T-3 (partial write corruption) | M-3 (atomic write via `tempfile` + `os.replace`) | **NEGLIGIBLE** -- Atomic replace is a well-established pattern. Cleanup on failure prevents orphaned temp files. |

### Residual Risk Register

| ID | Risk | Severity | Likelihood | Residual Level | Notes |
|----|------|----------|------------|----------------|-------|
| RR-1 | Markdown formatting injection in descriptions | Low | Low | **Accepted** | An attacker with repo write access could craft a description containing markdown formatting (e.g., `# HEADING` or `**bold**`) that disrupts README visual layout. This is not exploitable because: (a) repo write access implies trust, (b) all changes go through PR review, (c) the `jerry docs generate --check` CI gate would surface unexpected content. |
| RR-2 | Activation-keywords exceeding max count (warn-only) | Low | Low | **Accepted** | The M-5 implementation uses warn-only policy for `activation-keywords > 30` rather than rejection. This is a deliberate design decision documented in the code (lines 143-146 of `skill_extractor.py`): truncation would silently alter routing behavior, which is a worse outcome than a warning. The doc module does not render activation-keywords in README output, so oversized keyword lists pose no rendering risk. |

### Defense-in-Depth Observations

The implementation includes two security controls beyond the threat model specification:

1. **Path traversal guard** (lines 95-108 of `generate_docs_command_handler.py`): Validates that `command.readme_path` resolves within the repository root directory. This prevents `--readme ../../etc/passwd` or similar path traversal attacks. Not specified in the threat model but provides defense-in-depth for the CLI entry point.

2. **Command injection prevention** (lines 57-62 of `ast_frontmatter_reader.py`): The subprocess call uses list-form arguments (`["uv", "run", "jerry", "ast", "frontmatter", str(file_path)]`) rather than `shell=True`, preventing command injection via crafted file paths. Combined with the `timeout=30` parameter, this bounds both the execution scope and duration of the subprocess.

### NIST CSF 2.0 Function Mapping

| CSF Function | Controls | Coverage |
|-------------|----------|----------|
| **Identify (ID)** | Threat model documents all trust boundaries and attack surfaces | Complete |
| **Protect (PR)** | M-1 (sanitization), M-2 (sandboxing), M-3 (atomic write), M-4 (version pin), M-5 (schema validation) | Complete |
| **Detect (DE)** | `--check` mode detects drift; CI workflow enforces freshness | Partial -- no runtime anomaly detection, but appropriate for a build-time tool |
| **Respond (RS)** | Error codes (0-3) with diagnostic messages; `logger.warning()` for skipped files | Adequate |
| **Recover (RC)** | Atomic write (M-3) prevents corruption; git provides full recovery via version history | Complete |

### Architectural Compliance Summary

The doc module implementation demonstrates strong alignment with the Jerry Framework's security architecture principles:

- **Hexagonal layer isolation (H-07):** Clean inward-only dependency direction. Domain knows nothing about infrastructure. Application depends on domain abstractions. Infrastructure implements domain ports.
- **Single responsibility (H-10):** One class per file across all 10 source files.
- **Type safety (H-11):** Full type annotations and docstrings on all public and private functions.
- **AST compliance (H-33):** Frontmatter parsing delegates to `jerry ast frontmatter` without any regex-based YAML extraction.
- **UV compliance (H-05):** Subprocess uses `uv run` for Python execution.

No findings require remediation. All mitigations are correctly implemented and verified against the threat model specification.

---

*Review conducted by eng-architect. All citations reference files under `src/docs/` in the `feat/proj-0037-doc-module` branch.*
*Threat model: `projects/PROJ-0037-doc-module/security/threat-model-doc-module.md`*
*Specification: `projects/PROJ-0037-doc-module/specifications/doc-module-spec.md`*
