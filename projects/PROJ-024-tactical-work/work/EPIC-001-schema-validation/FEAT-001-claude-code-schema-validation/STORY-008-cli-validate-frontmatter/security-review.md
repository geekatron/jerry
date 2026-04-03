# Security Review -- `jerry agents validate-frontmatter`

> eng-security | STORY-008 | 2026-03-26
> Reviewer: eng-security (forensic cognitive mode)
> Scope: Three-file manual review -- command handler, CLI main, CLI parser

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Severity counts, overall posture, top risks, immediate actions |
| [L1 Technical Findings](#l1-technical-findings) | Individual findings with CWE, CVSS, location, evidence, remediation |
| [L1 ASVS Verification](#l1-asvs-verification) | Chapter-by-chapter compliance status |
| [L1 H-07 Layer Compliance](#l1-h-07-layer-compliance) | Architecture layer isolation check |
| [L1 H-11 Type Annotation Compliance](#l1-h-11-type-annotation-compliance) | Public function type annotation check |
| [L2 Strategic Implications](#l2-strategic-implications) | Posture assessment, patterns, architectural recommendations |

---

## L0 Executive Summary

### Finding Count by Severity

| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 2 |
| Low | 2 |
| Info | 3 |
| **Total** | **7** |

### Overall Security Assessment

**PASS with findings.** The implementation is structurally sound. YAML is parsed exclusively with `yaml.safe_load` (no code execution risk). File discovery is confined to a fixed subtree. Input from the CLI is accepted only through argparse with no shell interpolation. The two Medium findings are both information-disclosure issues in error output; neither enables remote code execution or privilege escalation. The two Low findings are minor robustness and standards-compliance gaps.

### Top 3 Risk Areas

1. **Information disclosure in error output (Medium, F-001 and F-002):** File system paths, YAML parse error detail, and raw `repr()` of frontmatter field values are emitted to stdout. In a CI/CD context where stdout is captured in build logs, this can expose internal repository structure and configuration content.
2. **Broad bare `except Exception` in schema error handler (Low, F-003):** A single `except Exception` clause silently swallows errors during `repr()` of the erroneous value. While the risk surface is confined to cosmetic output, the pattern violates the project's coding standard (coding-standards.md) and masks unexpected failures.
3. **No sandbox boundary on `repo_root` override (Low, F-004):** `ValidateFrontmatterCommand.repo_root` accepts an arbitrary `Path` value at the data-layer boundary. If a caller passes a crafted path, file discovery silently escapes the intended `skills/` subtree. The current CLI caller is safe, but the handler has no enforcement of the intended constraint.

### Recommended Immediate Actions

1. Truncate the parse-error message before emitting it to stdout (strip internal YAML stack detail, emit only "YAML syntax error at line N"). Addresses F-001.
2. Replace `except Exception` with `except (TypeError, ValueError)` in `_schema_errors` and document the rationale. Addresses F-003.
3. Add `verify_within_repo_root` validation in `ValidateFrontmatterCommandHandler.handle()` when `command.repo_root` overrides the default. Addresses F-004.

---

## L1 Technical Findings

### F-001 -- Information Disclosure: YAML Parse Error Detail in stdout

| Attribute | Value |
|-----------|-------|
| CWE | CWE-209 -- Generation of Error Message Containing Sensitive Information |
| CVSS 3.1 Base Score | 4.3 (AV:L/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N) |
| Severity | Medium |
| File | `src/agents/application/commands/validate_frontmatter_command.py` |
| Lines | 378-379 |
| ASVS | V7.4.1 -- Error messages must not contain sensitive information |

**Evidence.**

The `_extract_frontmatter` method formats YAML parse exceptions directly into the error string returned to the caller:

```python
except yaml.YAMLError as exc:
    return raw_text, None, f"YAML parse error: {exc}"
```

`yaml.YAMLError` exceptions include full problem marks with line numbers, column numbers, and, in some scanner variants, the offending raw bytes. This string is then stored verbatim in `FrontmatterFileResult.errors` and printed to stdout in both the human-readable path (`_print_frontmatter_table`, main.py line 830-833) and the JSON path (`_handle_agents_validate_frontmatter`, main.py lines 746-748):

```python
# JSON path -- raw error value emitted in "value" field
{"field": e[0], "constraint": e[1], "value": e[2]}

# Human path -- value truncated to 60 chars but still the full YAML scanner message
val_display = val if len(val) <= 60 else val[:57] + "..."
```

In CI logs and build artifacts, this reveals internal repository file paths embedded in PyYAML's problem mark string (e.g., `in "<unicode string>", line 3, column 5`). When combined with the relative file path also present in the output, an observer gains a complete view of the internal YAML structure at the failure point.

**Data flow trace.** User invokes CLI -> argparse provides no path traversal opportunity here -> `_extract_frontmatter` reads file -> PyYAML scanner raises `YAMLError` -> exception `str()` captured without sanitisation -> propagated through `FrontmatterFileResult.errors[0][2]` -> printed verbatim to stdout in both output modes.

**Remediation.**

Replace the exception capture with a sanitised message that retains actionability without raw exception detail:

```python
except yaml.YAMLError as exc:
    # Extract line/column only; do not emit raw scanner marks which may
    # include internal path references or raw byte sequences.
    line = getattr(getattr(exc, "problem_mark", None), "line", None)
    location = f" at line {line + 1}" if line is not None else ""
    return raw_text, None, f"YAML syntax error{location}"
```

---

### F-002 -- Information Disclosure: `repr()` of Frontmatter Field Values in stdout

| Attribute | Value |
|-----------|-------|
| CWE | CWE-209 -- Generation of Error Message Containing Sensitive Information |
| CVSS 3.1 Base Score | 3.3 (AV:L/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N) |
| Severity | Medium |
| File | `src/agents/application/commands/validate_frontmatter_command.py` |
| Lines | 415-418 |
| ASVS | V7.4.1 |

**Evidence.**

`_schema_errors` calls `repr()` on the erroneous frontmatter value and emits it in the validation output:

```python
try:
    current_val = repr(error.instance)
    if len(current_val) > 120:
        current_val = current_val[:117] + "..."
except Exception:
    current_val = "(unable to represent)"
```

`error.instance` is the YAML-parsed Python object at the failing JSON Schema path. For a string field that fails validation, this is the raw string content of that frontmatter field -- potentially a description, a hook path, or a tool pattern containing internal path or configuration details. These values are emitted verbatim (up to 120 characters) in both the JSON output `"value"` field (main.py line 748) and the human table (main.py line 833, truncated at 60 characters).

The risk is limited because: (a) the caller already has read access to the file being validated; (b) this is a local CLI tool, not a network service. The concern is CI log capture and any future remote execution context.

**Remediation.**

For string field values, truncate to a safe preview length before `repr()` to limit the content exposed. Apply different handling for scalars vs. collections:

```python
try:
    instance = error.instance
    if isinstance(instance, str) and len(instance) > 40:
        instance = instance[:37] + "..."
    current_val = repr(instance)
    if len(current_val) > 120:
        current_val = current_val[:117] + "..."
except (TypeError, ValueError):
    current_val = "(unable to represent)"
```

---

### F-003 -- Bare `except Exception` Swallows Unexpected Failures

| Attribute | Value |
|-----------|-------|
| CWE | CWE-390 -- Detection of Error Condition Without Action |
| CVSS 3.1 Base Score | 2.0 (AV:L/AC:H/PR:L/UI:N/S:U/C:N/I:N/A:L) |
| Severity | Low |
| File | `src/agents/application/commands/validate_frontmatter_command.py` |
| Lines | 419-420 |
| H-rule | Coding Standards: "NEVER catch `Exception` broadly and silently swallow errors" |

**Evidence.**

```python
except Exception:
    current_val = "(unable to represent)"
```

`repr()` raises `TypeError` when `__repr__` raises, or `RecursionError` for deeply nested structures. Catching the bare `Exception` base class swallows `RecursionError` (a `BaseException` subclass -- actually this specific one would not be caught, but `MemoryError` on a pathological YAML document would be). More concretely, it violates the project's `coding-standards.md` which explicitly prohibits broad exception catches: "NEVER catch `Exception` broadly and silently swallow errors."

**Remediation.**

Replace with specific exception types:

```python
except (TypeError, ValueError):
    current_val = "(unable to represent)"
```

---

### F-004 -- No Repo-Root Boundary Enforcement on Override Path

| Attribute | Value |
|-----------|-------|
| CWE | CWE-22 -- Improper Limitation of a Pathname to a Restricted Directory |
| CVSS 3.1 Base Score | 2.5 (AV:L/AC:H/PR:L/UI:R/S:U/C:L/I:N/A:N) |
| Severity | Low |
| File | `src/agents/application/commands/validate_frontmatter_command.py` |
| Lines | 256, 261, 265, 267, 300, 326 |
| ASVS | V5.2.2 -- File path validation |

**Evidence.**

`ValidateFrontmatterCommand.repo_root` is an optional override that the handler uses verbatim:

```python
repo_root = command.repo_root if command.repo_root is not None else self._repo_root
```

The discovery methods then construct `repo_root / "skills"` and call `rglob()` on it. The guard in the current CLI caller (main.py line 707) resolves from `__file__` and is safe. However, the handler itself imposes no constraint. Any caller that constructs a `ValidateFrontmatterCommand(repo_root=Path("/"))` would cause file discovery to scan from the filesystem root's `skills/` subdirectory.

The `.graveyard` exclusion check (`if ".graveyard" in fp.parts`) is correctly implemented as a name-based check against `Path.parts`, which is not susceptible to `..` escape because `Path.parts` is normalised. This is correct and provides partial mitigation.

**Data flow trace.** `ValidateFrontmatterCommand.repo_root` -> `handle()` line 256 -> `_discover_agent_files(repo_root, ...)` -> `(repo_root / "skills").rglob("agents/*.md")` -> unrestricted glob if `repo_root` is attacker-controlled.

**Remediation.**

Add boundary enforcement in `handle()` before using the override:

```python
repo_root = command.repo_root if command.repo_root is not None else self._repo_root
# Enforce that any override is still inside (or equal to) the handler's
# known repo root to prevent escaping the intended scan boundary.
if command.repo_root is not None:
    try:
        repo_root.resolve().relative_to(self._repo_root.resolve())
    except ValueError as exc:
        raise ValueError(
            f"repo_root override '{repo_root}' is outside the handler's "
            f"repo root '{self._repo_root}'"
        ) from exc
```

---

### F-005 -- YAML Safe Load Confirmed (Informational)

| Attribute | Value |
|-----------|-------|
| CWE | CWE-502 -- Deserialization of Untrusted Data (not applicable -- mitigated) |
| Severity | Info |
| File | `src/agents/application/commands/validate_frontmatter_command.py` |
| Lines | 377 |

**Evidence.** `yaml.safe_load(raw_text)` is used exclusively. `yaml.load()` with an arbitrary `Loader` is absent from all three files. The YAML content originates from the local repository filesystem, not from network input. **No finding; confirmed correct.**

---

### F-006 -- No Shell Execution in Any Reviewed Code Path (Informational)

| Attribute | Value |
|-----------|-------|
| CWE | CWE-78 -- OS Command Injection (not applicable -- mitigated) |
| Severity | Info |
| File | All three files |

**Evidence.** No `subprocess`, `os.system`, `os.popen`, `eval`, or `exec` calls appear in any of the three reviewed files. The parser uses only `argparse` with defined argument types. **No finding; confirmed correct.**

---

### F-007 -- No Hardcoded Credentials or Secrets (Informational)

| Attribute | Value |
|-----------|-------|
| CWE | CWE-798 -- Use of Hard-coded Credentials (not applicable) |
| Severity | Info |
| File | All three files |

**Evidence.** No API keys, tokens, passwords, or secret patterns are present. Schema file paths are constructed from `__file__` resolution, not from user-supplied input. **No finding; confirmed correct.**

---

## L1 ASVS Verification

Relevant chapters for a local CLI validation tool operating on repository files.

### V5 -- Validation, Sanitization and Encoding

| Requirement | ID | Status | Notes |
|-------------|-----|--------|-------|
| All user-supplied inputs validated before use | V5.1.1 | PASS | argparse defines allowed argument types; filters are optional strings only |
| File paths validated against allowed locations | V5.2.2 | PARTIAL | Discovery is confined to `skills/` subtree via hardcoded join; repo_root override has no boundary check (F-004) |
| YAML parsed safely | V5.3.7 | PASS | `yaml.safe_load` exclusively; no `yaml.load` present |
| Input values not reflected unsanitised into output | V5.3.1 | PARTIAL | `repr()` of field values and raw YAML exception text emitted to stdout (F-001, F-002) |

### V7 -- Error Handling and Logging

| Requirement | ID | Status | Notes |
|-------------|-----|--------|-------|
| Error messages do not reveal stack traces or system paths | V7.4.1 | PARTIAL | YAML parser exception string contains problem-mark detail (F-001) |
| All exceptions are handled specifically, not broadly | V7.1.2 | PARTIAL | Bare `except Exception` in `_schema_errors` (F-003) |
| Logging does not contain sensitive information | V7.1.1 | PASS | No logging calls in reviewed code; all output via `print()` with reviewed content |

### V4 -- Access Control

| Requirement | ID | Status | Notes |
|-------------|-----|--------|-------|
| Operations restricted to authorised resources | V4.2.1 | PASS | All file access confined to local filesystem; no network access; argparse arguments do not accept file paths (only filter names) |

### V1 -- Architecture

| Requirement | ID | Status | Notes |
|-------------|-----|--------|-------|
| Least privilege principle applied | V1.1.2 | PASS | Command handler reads files only; no write operations anywhere in reviewed scope |
| Sensitive data not stored unnecessarily | V1.8.1 | PASS | No persistence of file content; results are transient in-memory objects |

---

## L1 H-07 Layer Compliance

### Verified Import Paths

The command handler (`src/agents/application/commands/validate_frontmatter_command.py`) imports:

| Import | Layer | Permitted? |
|--------|-------|-----------|
| `from __future__ import annotations` | stdlib | PASS |
| `import json` | stdlib | PASS |
| `import re` | stdlib | PASS |
| `from dataclasses import dataclass, field` | stdlib | PASS |
| `from pathlib import Path` | stdlib | PASS |
| `from typing import Any` | stdlib | PASS |
| `import yaml` (deferred inside method) | third-party | PASS |
| `from jsonschema import Draft202012Validator` (deferred inside method) | third-party | PASS |

**Result: H-07 PASS.** The application layer command handler imports only stdlib and third-party libraries. There are no imports from `infrastructure/`, `interface/`, or `domain/`. The deferred `import yaml` and `from jsonschema import Draft202012Validator` inside methods is an unusual pattern -- it avoids import-time failure if optional dependencies are absent, which is acceptable, but it makes dependency declaration less visible. This is not a security issue but is noted as a style observation.

The CLI main.py (`src/interface/cli/main.py`) correctly imports from `src.agents.application.commands.validate_frontmatter_command` (interface importing from application), which is permitted by H-07.

---

## L1 H-11 Type Annotation Compliance

### Command Handler (`validate_frontmatter_command.py`)

| Method | Annotations | Status |
|--------|------------|--------|
| `ValidateFrontmatterCommandHandler.__init__` | All params annotated; return `None` implicit | PASS |
| `ValidateFrontmatterCommandHandler.handle` | `command: ValidateFrontmatterCommand`, return `ValidateFrontmatterResult` | PASS |
| `_discover_agent_files` | `repo_root: Path`, `agent_filter: str \| None`, return `list[Path]` | PASS |
| `_discover_skill_files` | `repo_root: Path`, `skill_filter: str \| None`, return `list[Path]` | PASS |
| `_extract_frontmatter` | `file_path: Path`, return `tuple[str \| None, dict[str, Any] \| None, str \| None]` | PASS |
| `_schema_errors` | `frontmatter: dict[str, Any]`, `schema: dict[str, Any]`, return `list[tuple[str, str, str]]` | PASS |
| `_validate_agent_file` | `fp: Path`, `repo_root: Path`, return `FrontmatterFileResult` | PASS |
| `_validate_skill_file` | `fp: Path`, `repo_root: Path`, return `FrontmatterFileResult` | PASS |

### CLI Main (`main.py`) -- functions related to the reviewed feature

| Function | Annotations | Status |
|----------|------------|--------|
| `_handle_agents` | `args: Any`, `json_output: bool`, return `int` | PASS |
| `_handle_agents_validate_frontmatter` | `args: Any`, `json_output: bool`, return `int` | PASS |
| `_print_frontmatter_table` | `result: Any`, return `None` | PARTIAL -- `result: Any` lacks specificity; should be `result: ValidateFrontmatterResult`. Not a security issue, but a type fidelity gap. |

**Result: H-11 overall PASS.** All public methods have annotations. One annotation uses `Any` where a more specific type is available (`_print_frontmatter_table`), which is a code quality gap but not a security gap.

---

## L2 Strategic Implications

### Security Posture Assessment

The `validate-frontmatter` command is a read-only, local-filesystem tool with a tightly scoped attack surface. The implementation reflects security-conscious design: exclusive use of `yaml.safe_load`, no shell execution, no network calls, argparse with no user-controlled file paths. The findings are confined to output hygiene (information disclosure) and standards conformance gaps, not exploitable vulnerabilities.

**CVSS aggregate risk for this command in its current deployment context (local developer tool):** Low. The two Medium findings are contextually downgraded by the local execution environment; they would escalate to High if this command were exposed via a CI webhook or API endpoint where stdout is consumed by external parties.

### Systemic Patterns

Two systemic patterns appear across the implementation:

1. **Exception-as-string pattern.** Three locations in the handler capture exception objects and include their string representation in user-facing output (`f"PyYAML not installed: {exc}"`, `f"Could not read file: {exc}"`, `f"YAML parse error: {exc}"`). This pattern recurs consistently and suggests a broader codebase habit of treating exception messages as safe to emit. A targeted code review of other command handlers should check for the same pattern, particularly any handler that reads external files or invokes third-party parsers.

2. **Deferred third-party imports.** Both `import yaml` and `from jsonschema import Draft202012Validator` are deferred inside method bodies rather than declared at module top. While this avoids import-time failures for optional dependencies, it obscures the dependency graph and makes it harder for static analysis tools to verify that correct versions are installed. This is a maintainability concern; the deferred import for `yaml` inside `_extract_frontmatter` also means the `ImportError` path (line 358) returns `(None, None, error_string)` rather than raising, silently converting a missing dependency into a "no frontmatter found" outcome for the caller (which treats `raw_text is None` as no frontmatter, not as a dependency error). This is a latent logic bug unrelated to security but worth noting.

### Threat Model Comparison

The threat model for a local CLI validation tool predicts: (a) no remote attack surface; (b) primary risk is local information disclosure in logs; (c) secondary risk is path traversal on developer workstations if filter inputs are user-controlled. Findings F-001 through F-004 map precisely to these predicted categories. No unexpected attack surface was identified.

### Recommendations for Security Architecture Evolution

1. Introduce a `sanitise_for_output(exc: Exception) -> str` utility function in `shared_kernel/` to standardise exception-to-string conversion across all command handlers. This centralises the disclosure control and eliminates the recurring pattern.
2. Define a `RepoRootBoundary` value object in the agents bounded context that encapsulates path validation and subtree confinement, making the boundary check reusable across any future command that accepts a `repo_root` override.
3. When this command is integrated into CI (its stated purpose per the docstring: "CI integration"), revisit the Medium findings at that point and promote them to High severity, triggering the project's C3 review threshold.

---

*Review completed: 2026-03-26*
*Reviewer: eng-security*
*Files reviewed: 3 (1,686 lines total)*
*Methodology: Manual data-flow tracing, CWE Top 25 2025 checklist, ASVS 5.0 Chapter V5/V7, H-07/H-11 compliance check*
*Confidence: 0.88 -- high confidence on all three files; confidence is not 1.0 because deferred imports reduce static analysis visibility into third-party library behaviour at schema validation time*
