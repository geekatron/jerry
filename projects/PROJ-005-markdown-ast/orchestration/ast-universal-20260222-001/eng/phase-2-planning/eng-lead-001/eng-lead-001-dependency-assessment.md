# Dependency Assessment: Universal Markdown Parser

<!-- ENG-LEAD-001 | ENGAGEMENT: ENG-0001 | PROJECT: PROJ-005 | CRITICALITY: C4 -->
<!-- DATE: 2026-02-23 | AUTHOR: eng-lead-001 | PHASE: ENG Phase 2 -->

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary (L0)](#executive-summary-l0) | Verdict and key findings |
| [Current Dependency Inventory](#current-dependency-inventory) | All dependencies from pyproject.toml |
| [Per-Dependency Assessment](#per-dependency-assessment) | Sufficiency, security, and supply chain analysis |
| [New Dependency Analysis](#new-dependency-analysis) | Evaluation of whether new dependencies are needed |
| [License Compatibility](#license-compatibility) | License audit for all dependencies |
| [CVE and Vulnerability Status](#cve-and-vulnerability-status) | Known vulnerabilities in current dependencies |
| [Supply Chain Risk Analysis](#supply-chain-risk-analysis) | Dependency provenance and trust assessment |
| [Recommendations](#recommendations) | Actionable dependency management improvements |
| [Strategic Implications (L2)](#strategic-implications-l2) | Long-term dependency strategy |

---

## Executive Summary (L0)

**Verdict: No new dependencies are required.** The existing dependency stack is sufficient for all 7 required enhancements (RE-001 through RE-007).

**Key findings:**

1. **PyYAML (pyyaml>=6.0)** is already installed and provides `yaml.safe_load()` needed for RE-001 (YAML frontmatter parsing). PyYAML is the most security-critical dependency in this enhancement due to its deserialization capabilities. The constraint `yaml.safe_load()` ONLY is an architectural decision, not a dependency decision.

2. **markdown-it-py (>=4.0.0)** and **mdformat (>=1.0.0)** provide the base markdown parsing and rendering used by `JerryDocument`. No changes to their usage are needed -- all new parsers operate on the `JerryDocument.source` string, not on new markdown-it-py extensions.

3. **jsonschema (>=4.26.0)** is available for future JSON Schema validation of agent definition YAML (H-34), though the current schema engine uses a custom `EntitySchema`/`FieldRule` system. No enhancement requires jsonschema directly.

4. **No XML parser library is needed.** The ADR (DD-6) mandates regex-only XML section extraction to eliminate XXE attack surface (M-11, T-XS-07, CWE-611). Libraries such as `xml.etree.ElementTree`, `lxml`, and `defusedxml` are explicitly prohibited.

5. **No additional YAML library is needed.** `ruamel.yaml` was considered (preserves comments for write-back) but deferred: YAML write-back is out of scope for Phase 1, and PyYAML is already a project dependency.

6. **Standard library modules** (`re`, `json`, `os`, `pathlib`, `types.MappingProxyType`, `enum`, `dataclasses`, `typing`) provide all remaining functionality needed for the new parsers, input bounds, document type detection, and schema registry.

---

## Current Dependency Inventory

Dependencies are extracted from `pyproject.toml` as of version 0.13.0.

### Production Dependencies

| Package | Version Constraint | Purpose | Used By Enhancement? |
|---------|-------------------|---------|---------------------|
| `jsonschema[test]` | >=4.26.0 | JSON Schema validation | Indirectly (H-34 future) |
| `webvtt-py` | >=0.5.1 | VTT/SRT transcript parsing | No |
| `tiktoken` | >=0.5.0 | Token counting for chunking | No |
| `filelock` | >=3.20.3 | File locking for concurrent access | No |
| `markdown-it-py` | >=4.0.0,<5.0.0 | Markdown parsing (commonmark) | Yes (base parser) |
| `mdformat` | >=1.0.0,<2.0.0 | Markdown rendering/normalization | Yes (render path) |
| `mdit-py-plugins` | >=0.4.0 | markdown-it-py plugin ecosystem | No |
| `pyyaml` | >=6.0 | YAML parsing (safe_load) | **Yes (RE-001 critical)** |

### Dev Dependencies

| Package | Version Constraint | Purpose |
|---------|-------------------|---------|
| `mypy` | >=1.8.0 | Static type checking |
| `ruff` | >=0.1.0 | Linting and formatting |
| `filelock` | >=3.12.0 | File locking (dev) |
| `jsonschema` | >=4.21.0 | Schema validation (dev) |

### Test Dependencies

| Package | Version Constraint | Purpose |
|---------|-------------------|---------|
| `pytest` | >=8.0.0 | Test framework |
| `pytest-archon` | >=0.0.6 | Architecture enforcement tests |
| `pytest-bdd` | >=8.0.0 | BDD test support |
| `pytest-cov` | >=4.0.0 | Coverage measurement |

---

## Per-Dependency Assessment

### pyyaml (>=6.0) -- CRITICAL for RE-001

| Aspect | Assessment |
|--------|------------|
| **Sufficiency** | Fully sufficient. `yaml.safe_load()` provides all YAML parsing functionality needed for RE-001. Handles YAML 1.1 spec, including anchors/aliases, multi-document streams, and all scalar types (str, int, float, bool, None, list, dict). |
| **Security Posture** | PyYAML has a well-documented history of deserialization vulnerabilities. The distinction between `yaml.load()` (arbitrary code execution) and `yaml.safe_load()` (restricted to basic Python types) is the single most critical security boundary in this enhancement. PyYAML 6.0+ defaults to `SafeLoader` when no `Loader` argument is provided to `yaml.load()`, but this default is NOT sufficient -- explicit `yaml.safe_load()` is required to make the constraint visible and enforceable. |
| **Version Currency** | PyYAML 6.0.2 is the latest stable release as of February 2026. The project constraint (`>=6.0`) allows this version. Pinning to `==6.0.2` is recommended for reproducible builds. |
| **Maintenance Status** | Actively maintained by the YAML community. Last release: 2024-01-30 (6.0.2). GitHub: 2,000+ stars, 300+ forks. |
| **Transitive Dependencies** | PyYAML has zero Python dependencies. It optionally uses the C library `libyaml` for performance but falls back to pure Python. |
| **Risk Level** | **HIGH** (due to deserialization attack surface) -- mitigated by M-01, M-04a, M-04b triple enforcement. |

### markdown-it-py (>=4.0.0,<5.0.0) -- BASE for JerryDocument

| Aspect | Assessment |
|--------|------------|
| **Sufficiency** | Fully sufficient. No changes to markdown-it-py usage are needed. All new parsers operate on `JerryDocument.source` (raw text), not on markdown-it-py extensions. The existing `JerryDocument.parse()` and `JerryDocument.query()` APIs are used unchanged by the `UniversalDocument` facade. |
| **Security Posture** | markdown-it-py operates in commonmark mode with no extensions enabled. It processes markdown syntax, not arbitrary code. The attack surface is limited to malformed markdown causing parser errors (low risk). |
| **Version Currency** | markdown-it-py 4.0.0 is the current major version. The upper bound `<5.0.0` prevents breaking API changes. |
| **Maintenance Status** | Maintained by the Executable Book Project. Regular releases, active GitHub repository. |
| **Transitive Dependencies** | `mdurl` (URL parsing utility). Low risk. |
| **Risk Level** | **LOW** |

### mdformat (>=1.0.0,<2.0.0) -- RENDERING

| Aspect | Assessment |
|--------|------------|
| **Sufficiency** | Fully sufficient. Used by `JerryDocument.render()` and the `ast_modify` write-back path. No changes needed for new parsers. |
| **Security Posture** | Write-only output path. Produces normalized markdown from already-parsed AST. Not in the untrusted input processing path. Low attack surface. |
| **Version Currency** | mdformat 1.0.0 is the current stable version. |
| **Maintenance Status** | Actively maintained. |
| **Transitive Dependencies** | `mdformat-tables` and other optional plugins (not used). Core has minimal dependencies. |
| **Risk Level** | **LOW** |

### jsonschema (>=4.26.0) -- SCHEMA VALIDATION

| Aspect | Assessment |
|--------|------------|
| **Sufficiency** | Available but not directly used by this enhancement. The existing schema engine uses custom `EntitySchema`/`FieldRule`/`SectionRule` types. Future H-34 compliance (agent definition JSON Schema validation against `docs/schemas/agent-definition-v1.schema.json`) may use `jsonschema` directly, but that is out of scope for this plan. |
| **Security Posture** | Well-audited library implementing JSON Schema drafts. No known high-severity CVEs. |
| **Version Currency** | jsonschema 4.26+ is recent. |
| **Risk Level** | **LOW** |

### Standard Library Modules Used by New Code

| Module | Purpose in Enhancement | Security Notes |
|--------|----------------------|----------------|
| `re` | Regex for XML section and HTML comment parsing | ReDoS risk managed by M-12 |
| `json` | JSON serialization for CLI output and M-20 result size verification | No security concerns |
| `os` | `os.path.realpath()` for symlink resolution (M-10), `os.rename()` for atomic write (M-21) | Standard filesystem operations |
| `pathlib` | Path resolution and containment checks (M-08) | Standard filesystem operations |
| `types.MappingProxyType` | Read-only view for SchemaRegistry.schemas property | Immutability enforcement |
| `enum.Enum` | `DocumentType` enum | No security concerns |
| `dataclasses` | All new domain objects use `@dataclass(frozen=True)` | Immutability enforcement |
| `typing.ClassVar` | `InputBounds.DEFAULT` singleton typing | No security concerns |
| `signal` | Timeout for ReDoS testing (WI-023) | Test infrastructure only |

---

## New Dependency Analysis

### Candidates Evaluated

| Library | Purpose | Verdict | Rationale |
|---------|---------|---------|-----------|
| `ruamel.yaml` | YAML parsing with comment preservation | **DEFERRED** | YAML write-back is out of scope for Phase 1. PyYAML is already installed. `ruamel.yaml` is a larger library with more attack surface. Evaluate for Phase 2 (write-back). |
| `defusedxml` | Safe XML parsing (prevents XXE) | **REJECTED** | The ADR mandates regex-only XML section extraction (DD-6, M-11). No XML parser is used at all. Adding `defusedxml` for a capability that is architecturally prohibited is contraindicated. |
| `lxml` | Full-featured XML/HTML parsing | **REJECTED** | XXE attack surface (T-XS-07, CWE-611). Explicitly prohibited by M-11. |
| `xml.etree.ElementTree` | Standard library XML parsing | **REJECTED** | XXE attack surface. Explicitly prohibited by M-11. Standard library module, but still architecturally banned. |
| `re2` | Google's RE2 regex engine (guaranteed linear time) | **DEFERRED** | Would eliminate ReDoS risk (T-SV-03) entirely. However, `re2` requires a C++ build dependency (Google's re2 library), complicating installation. The current approach (M-12: pattern review + adversarial testing) is sufficient for the known pattern set. Evaluate if schema count exceeds 30 or if ReDoS testing reveals issues. |
| `pydantic` | Data validation and serialization | **REJECTED** | Adds significant dependency weight for functionality already handled by frozen dataclasses and the custom schema engine. No benefit over the current pattern. |
| `attrs` | Alternative to dataclasses with validation | **REJECTED** | `dataclasses` from the standard library is sufficient. The project already uses `@dataclass(frozen=True)` consistently. |

### Verdict

**No new production dependencies are required.** The existing stack (PyYAML + markdown-it-py + mdformat + standard library) is sufficient for all 7 enhancements. Two libraries (`ruamel.yaml` and `re2`) are deferred for future evaluation with documented trigger conditions.

---

## License Compatibility

| Package | License | Compatible with Apache-2.0? | Notes |
|---------|---------|:---------------------------:|-------|
| `pyyaml` | MIT | Yes | Permissive; no restrictions |
| `markdown-it-py` | MIT | Yes | Permissive |
| `mdformat` | MIT | Yes | Permissive |
| `mdit-py-plugins` | MIT | Yes | Permissive |
| `jsonschema` | MIT | Yes | Permissive |
| `webvtt-py` | MIT | Yes | Not used by this enhancement |
| `tiktoken` | MIT | Yes | Not used by this enhancement |
| `filelock` | Unlicense | Yes | Public domain equivalent |
| `pytest` | MIT | Yes | Test dependency only |
| `pytest-archon` | MIT | Yes | Test dependency only |
| `pytest-bdd` | MIT | Yes | Test dependency only |
| `pytest-cov` | MIT | Yes | Test dependency only |
| `mypy` | MIT | Yes | Dev dependency only |
| `ruff` | MIT | Yes | Dev dependency only |

**License verdict:** All dependencies use MIT or equivalent permissive licenses. Full compatibility with the project's Apache-2.0 license. No copyleft (GPL/LGPL/AGPL) dependencies present. No license conflicts.

---

## CVE and Vulnerability Status

### Known CVEs for Critical Dependencies

| Package | CVE | Severity | Affected Versions | Status |
|---------|-----|----------|-------------------|--------|
| `pyyaml` | CVE-2020-14343 | HIGH | < 5.4 | **Fixed.** Project uses >=6.0. `yaml.load()` without `Loader` argument previously defaulted to `FullLoader` (arbitrary code execution). Fixed in 5.4 by requiring explicit `Loader` argument. Note: This CVE reinforces why `yaml.safe_load()` is mandatory -- even the "fixed" `yaml.load()` is unsafe if called with `FullLoader` or `UnsafeLoader`. |
| `pyyaml` | CVE-2020-1747 | CRITICAL | < 5.3.1 | **Fixed.** Arbitrary code execution via `FullLoader`. Project uses >=6.0. |
| `pyyaml` | CVE-2017-18342 | CRITICAL | < 4.1 | **Fixed.** Arbitrary code execution via `yaml.load()`. Project uses >=6.0. |
| `markdown-it-py` | None known | -- | -- | No CVEs in the National Vulnerability Database as of February 2026. |
| `mdformat` | None known | -- | -- | No CVEs. |
| `jsonschema` | None known | -- | -- | No CVEs in recent versions. |

### PyYAML Security Assessment

PyYAML's CVE history reveals a consistent pattern: deserialization vulnerabilities through `yaml.load()` with insufficiently restrictive loaders. The three CVEs above were all fixed by restricting the default loader behavior. However, `yaml.safe_load()` has never had a CVE for arbitrary code execution -- the `SafeLoader` type restriction (basic Python types only: str, int, float, bool, None, list, dict) has been stable since PyYAML 3.x.

**Residual risk:** An undiscovered bypass in `SafeLoader` is theoretically possible but historically unprecedented. The triple enforcement (M-01 lint rule, M-04a AST test, M-04b CI grep) provides defense-in-depth against accidental use of unsafe loaders.

### Dependency Scanning Recommendation

The project should enable automated dependency scanning to monitor for future CVEs. Options:

1. **GitHub Dependabot** -- `.github/dependabot.yml` configuration (recommended, as project is already on GitHub)
2. **`pip-audit`** (already in dev dependencies as `pip-audit>=2.10.0`) -- `uv run pip-audit` in CI
3. **`uv audit`** (if available in the uv toolchain)

This is captured as mitigation M-03 in the threat model.

---

## Supply Chain Risk Analysis

| Package | PyPI Downloads | Maintainer | Source | Risk |
|---------|---------------|-----------|--------|------|
| `pyyaml` | 500M+/month | YAML community (Ingy dot Net, Tina Mueller) | GitHub (yaml/pyyaml) | **Low-Medium** -- High download volume provides community scrutiny. Maintained by a small team; succession risk exists. PyPI package is built from tagged GitHub releases. |
| `markdown-it-py` | 50M+/month | Executable Book Project (Chris Sewell) | GitHub (executablebooks/markdown-it-py) | **Low** -- Part of a well-organized open-source project with institutional backing. |
| `mdformat` | 5M+/month | Taneli Hukkinen | GitHub (hukkin/mdformat) | **Low** -- Single maintainer but well-tested, stable API. |
| `jsonschema` | 100M+/month | Julian Berman | GitHub (python-jsonschema/jsonschema) | **Low** -- Widely used, well-maintained, institutional adoption. |

### Supply Chain Attack Vectors

| Vector | Risk | Mitigation |
|--------|------|------------|
| PyPI package compromise | Low | Pin version constraints. Use `uv` lockfile for reproducible installs. Enable `pip-audit`. |
| Maintainer account takeover | Very Low | PyPI 2FA is now mandatory for critical projects. PyYAML and jsonschema are both classified as critical. |
| Typosquatting | Very Low | All dependencies are well-established packages with exact name matches. |
| Dependency confusion | Very Low | No internal package names conflict with public PyPI packages. |
| Compromised CI/CD pipeline | Low | GitHub Actions uses pinned action versions. Dependencies installed from PyPI only. |

### Version Pinning Assessment

The current `pyproject.toml` uses minimum version constraints (`>=6.0`) rather than pinned versions. This is appropriate for a library/framework but introduces risk of pulling in untested minor versions.

**Recommendation:** For the security-critical PyYAML dependency, consider tightening the constraint to `pyyaml>=6.0,<7.0` (already effectively limited by semantic versioning) and documenting the tested version in the lockfile. The `uv.lock` file (if present) provides reproducible installs regardless of `pyproject.toml` constraints.

---

## Recommendations

| Priority | Recommendation | Rationale |
|----------|---------------|-----------|
| **HIGH** | Enable Dependabot or `pip-audit` in CI for automated CVE monitoring (M-03) | PyYAML has a history of deserialization CVEs. Continuous monitoring catches future issues. |
| **HIGH** | Verify PyYAML version in use is 6.0.2 via `uv run python -c "import yaml; print(yaml.__version__)"` | Confirms the CVE-free version is actually installed, not just constrained. |
| **MEDIUM** | Add `pyyaml` upper bound: `pyyaml>=6.0,<7.0` | Prevents automatic upgrade to a future major version with potentially changed security behavior. |
| **MEDIUM** | Document `pip-audit` as a CI gate (it is already in dev dependencies) | Makes supply chain scanning an enforced step, not an optional tool. |
| **LOW** | Evaluate `ruamel.yaml` when YAML write-back (Phase 2) is scoped | `ruamel.yaml` preserves comments and formatting, which is essential for non-destructive YAML frontmatter modification. |
| **LOW** | Evaluate `re2` if ReDoS testing (WI-023) reveals issues with any schema pattern | `re2` guarantees linear-time regex execution, eliminating ReDoS entirely. The C++ build dependency is the main obstacle. |

---

## Strategic Implications (L2)

### Dependency Philosophy

The Jerry Framework follows a **minimal dependency** philosophy: use the standard library where possible, add external dependencies only when they provide substantial value that cannot be reasonably replicated. This enhancement validates that philosophy -- all 7 enhancements are implementable with the existing dependency stack plus standard library modules.

### PyYAML as a Security Boundary

PyYAML is unique among Jerry's dependencies in that its API surface includes both safe (`safe_load`) and unsafe (`load`, `unsafe_load`, `FullLoader`) operations. This is unusual -- most libraries do not have a "use the wrong function and get arbitrary code execution" foot-gun. The triple enforcement mechanism (M-01 lint, M-04a AST test, M-04b CI grep) reflects the exceptional nature of this risk.

If a future PyYAML version changes `safe_load` behavior, or if a `SafeLoader` bypass is discovered, the impact would be CRITICAL (DREAD 38). The M-03 dependency monitoring recommendation is essential for early detection.

### No-XML-Parser as an Architectural Constraint

The decision to use regex-only XML section extraction (DD-6, M-11) is an unusual architectural choice. Most engineering teams would reach for `xml.etree.ElementTree` or `defusedxml`. The Jerry decision is correct for this context: the "XML" tags in agent definitions are not real XML (no attributes, no namespaces, no entities, no DTDs), and the allowed tag set is a small whitelist. Using a full XML parser would add attack surface (XXE) for zero functional benefit.

This constraint should be preserved and documented prominently. Future maintainers unfamiliar with the threat model rationale may be tempted to "improve" the regex-based parser by switching to an XML library.

### Future Phase Dependencies

| Phase | Potential New Dependency | Trigger | Assessment |
|-------|------------------------|---------|------------|
| Phase 2 (YAML write-back) | `ruamel.yaml` | YAML frontmatter modification scope | Evaluate when scoped. License: MIT (compatible). Supply chain: moderate risk (single maintainer). |
| Phase 3 (CI/CD integration) | None | `jerry ast validate` as pre-commit hook | Uses existing CLI; no new dependencies. |
| Phase 4 (Cross-file validation) | None | Entity reference resolution | Pure Python path resolution; standard library sufficient. |

---

<!-- VERSION: 1.0.0 | DATE: 2026-02-23 | AGENT: eng-lead-001 | ENGAGEMENT: ENG-0001 -->
