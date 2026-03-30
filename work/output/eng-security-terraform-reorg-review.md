# Security Code Review: Terraform Artifact Reorganization

| Field | Value |
|-------|-------|
| Reviewer | eng-security |
| Date | 2026-03-29 |
| Scope | Terraform module relocation + HclGenerator path change |
| Files Reviewed | 5 source files + root .gitignore |
| Methodology | Manual code review — CWE Top 25 2025, OWASP ASVS 5.0 V5 (Validation) |
| SSDF Practice | PW.7 (Review and/or analyze human-readable code) |

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Finding counts, overall posture, top risks |
| [L1 Technical Findings](#l1-technical-findings) | Individual findings with CWE, CVSS, evidence, remediation |
| [L2 Strategic Implications](#l2-strategic-implications) | Systemic patterns, architectural recommendations |

---

## L0 Executive Summary

| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 1 |
| Medium | 2 |
| Low | 1 |
| Info | 1 |
| **Total** | **5** |

**Overall Security Assessment:** The reorganization is structurally sound. The two pre-existing controls — `SandboxedEnvironment` and the input allowlist validation — survived the move intact. No new injection surface was introduced by the path change. Three issues warrant remediation before this change ships: one high-severity gap in `.gitignore` coverage, one medium-severity IPv6 validation bypass, and one medium-severity `template_dir` trust boundary gap.

**Top 3 Risk Areas:**

1. Generated `main.tf` files written to runtime `work/` paths are not excluded by `.gitignore` — engagement HCL containing operator IP and SSH keys can be committed to the repository.
2. `_IPV6_PATTERN` accepts syntactically invalid strings (e.g., `:::::::::::`) that survive validation, allowing malformed values to flow into the HCL firewall resource.
3. `HclGenerator.__init__` accepts any `Path` object without asserting it resolves within a trusted subtree — a caller passing `Path("/etc")` or a relative path resolving outside the project would silently succeed.

**Recommended Immediate Actions:**

1. Add `work/**/terraform/` and `work/**/main.tf` exclusions to `.gitignore` (FINDING-001).
2. Tighten `_IPV6_PATTERN` to the `ipaddress` stdlib validator (FINDING-002).
3. Add a `template_dir` canonicalization check in `HclGenerator.__init__` (FINDING-003).

---

## L1 Technical Findings

### FINDING-001 — Generated `main.tf` files not excluded by `.gitignore`

| Field | Value |
|-------|-------|
| Severity | HIGH |
| CWE | CWE-312: Cleartext Storage of Sensitive Information |
| CVSS 3.1 | 7.5 (AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N) |
| ASVS | V8.3.4 — Sensitive data not stored unless necessary |
| Affected Files | `.gitignore`, `src/proxy_infra/infrastructure/adapters/terraform_provisioner_adapter.py` line 85-86 |

**Evidence.**

`TerraformProvisionerAdapter.__init__` writes engagement-scoped terraform working directories under `self._engagement_dir / "terraform"` (adapter line 85). The `engagement_dir` is constructed at call sites from paths within `work/engagements/` or similar runtime directories. `HclGenerator.generate` writes `main.tf` into that directory (hcl_generator.py line 94).

The generated `main.tf` contains rendered values for `operator_ip`, `ssh_public_key`, and `engagement_id` (template lines 15–16, 37–38, 76–77).

The `.gitignore` excludes:
- `*.tfstate` / `*.tfstate.*` — state files only
- `**/.terraform/` — provider cache
- `*.tfvars` — variable files

It does NOT exclude `*.tf` files or `work/**/terraform/` paths. The template source files at `infra/terraform/modules/digitalocean-proxy/` are intentionally tracked, which makes a wildcard `*.tf` exclusion inappropriate. The gap is that generated (rendered) `.tf` files in runtime paths are not excluded.

**Reproduction.** Run a provisioning flow against any engagement. Observe that `work/engagements/<id>/terraform/main.tf` is created with plaintext operator IP and SSH public key. Run `git status` — the file appears as untracked and would be staged by `git add .`.

**Remediation.**

Add to `.gitignore`:

```gitignore
# Generated HCL (runtime engagement artifacts — contain operator IP and SSH keys)
work/**/terraform/
work/**/main.tf
```

Alternatively, if the engagement directory structure is always under `work/engagements/`:

```gitignore
work/engagements/*/terraform/
```

This is distinct from the existing `projects/*/work/engagements/RED-*/` exclusion, which targets project-scoped paths rather than the top-level `work/` runtime directory.

---

### FINDING-002 — `_IPV6_PATTERN` accepts syntactically invalid IPv6 strings

| Field | Value |
|-------|-------|
| Severity | MEDIUM |
| CWE | CWE-20: Improper Input Validation |
| CVSS 3.1 | 4.6 (AV:N/AC:H/PR:L/UI:N/S:U/C:N/I:L/A:N) |
| ASVS | V5.1.3 — Input validation against allowlist |
| Affected File | `src/proxy_infra/infrastructure/terraform/hcl_generator.py` lines 30, 155–157 |

**Evidence.**

```python
_IPV6_PATTERN = re.compile(r"^[0-9a-fA-F:]+$")
```

This pattern matches any string composed entirely of hex digits and colons. It does not enforce:
- Maximum colon count (valid IPv6 has at most 7 colons, or 8 groups separated by 7)
- The `::` expansion rules
- The maximum total length (39 characters for full form)

Strings that pass validation but are not valid IPv6 addresses include:

- `:::::::::::::::` (15 colons — invalid)
- `gggg` — fails (non-hex), but `aaaa` passes and is not a valid IP
- `:` — single colon passes

These values would be interpolated directly into the `source_addresses` field of the `digitalocean_firewall` resource (template lines 76, 81), which Terraform would then reject at plan time — but only at plan time, not at Python validation time. The intent of `_validate_config` is to fail fast before subprocess invocation; the IPv6 path undermines that intent for malformed inputs.

There is no practical code injection risk here because the IPv6 characters (`[0-9a-fA-F:]`) cannot escape HCL string context. The risk is late failure (at terraform plan) vs. early failure (at Python validation) and potential firewall misconfiguration if the provider accepts a malformed CIDR.

**Remediation.**

Replace the regex with `ipaddress.ip_address()`:

```python
import ipaddress

def _validate_ip(value: str) -> None:
    try:
        ipaddress.ip_address(value)
    except ValueError as exc:
        raise ValueError(
            f"operator_ip '{value}' is not a valid IPv4 or IPv6 address"
        ) from exc
```

Then in `_validate_config`, replace lines 155–157:

```python
# Before:
if not (_IPV4_PATTERN.match(operator_ip) or _IPV6_PATTERN.match(operator_ip)):
    raise ValueError(...)

# After:
_validate_ip(operator_ip)
```

The `ipaddress` module is stdlib (Python 3.3+); no new dependency. `_IPV4_PATTERN` and `_IPV6_PATTERN` can both be removed.

---

### FINDING-003 — `HclGenerator.__init__` does not assert `template_dir` resolves within project tree

| Field | Value |
|-------|-------|
| Severity | MEDIUM |
| CWE | CWE-22: Improper Limitation of a Pathname to a Restricted Directory (Path Traversal) |
| CVSS 3.1 | 4.4 (AV:L/AC:L/PR:H/UI:N/S:U/C:H/I:N/A:N) |
| ASVS | V5.2.2 — Canonicalize path before use |
| Affected File | `src/proxy_infra/infrastructure/terraform/hcl_generator.py` lines 46–53 |

**Evidence.**

```python
def __init__(self, template_dir: Path) -> None:
    self._template_dir = template_dir   # stored as-is, no canonicalization
```

`FileSystemLoader` (line 105) is initialized directly from `str(self._template_dir)`. Jinja2's `FileSystemLoader` does enforce that templates stay within its root — a template path of `../../etc/passwd` would be blocked by `FileSystemLoader`'s own `get_source` boundary check. However:

1. The `template_dir` root itself is not verified. A caller passing `Path("/etc")` or `Path("../../../../etc")` would make `/etc` the valid loader root, from which `digitalocean-proxy/main.tf.j2` would simply fail to resolve — but there is no controlled error indicating why.

2. The `template_dir` accepts relative paths (the default hardcoding in `TerraformProvisionerAdapter` is `Path("infra/terraform/modules")` — a relative path resolved at CWD). If the adapter is constructed from an unexpected working directory, it silently loads templates from the wrong location.

3. The `get_template` call (line 81) uses a hardcoded string `"digitalocean-proxy/main.tf.j2"`. This is not attacker-controlled and is therefore not a live traversal vector in the current call graph. The risk is defensive depth: if `template_dir` were ever made configurable through an API surface, there is no backstop.

**Severity note.** This is MEDIUM rather than HIGH because the actual template name passed to `get_template` is hardcoded in `generate()` (line 81) and not derived from any external input. Exploitability requires a malicious caller with access to construct `HclGenerator` directly, which implies elevated trust.

**Remediation.**

Add a project-root boundary check in `__init__`:

```python
from pathlib import Path

def __init__(self, template_dir: Path) -> None:
    resolved = Path(template_dir).resolve()
    project_root = Path(__file__).resolve().parents[4]  # src/proxy_infra/infrastructure/terraform/hcl_generator.py -> 4 levels up to repo root
    try:
        resolved.relative_to(project_root)
    except ValueError as exc:
        raise ValueError(
            f"template_dir '{template_dir}' resolves to '{resolved}' "
            f"which is outside the project root '{project_root}'"
        ) from exc
    self._template_dir = resolved
```

Alternatively, resolve relative to a known-good anchor (e.g., the project root constant defined at bootstrap time) rather than `__file__`-relative counting, which is fragile to refactoring.

---

### FINDING-004 — `versions.tf` pins Terraform CLI with `>=` rather than exact version

| Field | Value |
|-------|-------|
| Severity | LOW |
| CWE | CWE-1104: Use of Unmaintained Third-Party Components (supply chain variant) |
| CVSS 3.1 | 2.1 (AV:N/AC:H/PR:N/UI:R/S:U/C:N/I:L/A:N) |
| ASVS | V10.2.1 — Components obtained from trusted sources with version pinning |
| Affected File | `infra/terraform/modules/digitalocean-proxy/versions.tf` line 5 |

**Evidence.**

```hcl
required_version = ">= 1.0.0"
```

The DigitalOcean provider is pinned exactly (`= 2.43.0`), which is the higher-risk component since it makes API calls. The Terraform CLI itself uses a floor constraint. This is a lower risk than unpinned providers, but it means any future Terraform release (including a hypothetical 2.x with breaking HCL semantics) would be accepted silently.

**Remediation.**

Pin to a tested minor range:

```hcl
required_version = "~> 1.9"
```

Or exact pin if reproducibility is required:

```hcl
required_version = "= 1.9.8"
```

The exact pin used in the DO provider (`= 2.43.0`) is the stricter pattern and should be applied consistently.

---

### FINDING-005 — `autoescape=False` on `SandboxedEnvironment` is correct but warrants a comment

| Field | Value |
|-------|-------|
| Severity | INFO |
| CWE | N/A (informational note) |
| Affected File | `src/proxy_infra/infrastructure/terraform/hcl_generator.py` lines 76–79 |

**Evidence.**

```python
env = SandboxedEnvironment(
    loader=self._make_loader(),
    autoescape=False,
    keep_trailing_newline=True,
)
```

`autoescape=False` is correct for HCL output — HTML escaping would corrupt the generated `main.tf` (e.g., `&amp;` in an SSH key). The `SandboxedEnvironment` provides the meaningful safety boundary here: it blocks access to Python builtins, `os`, `subprocess`, and arbitrary attribute traversal from within the template itself.

The concern is that a future developer might enable `autoescape=True` thinking it "adds security" and inadvertently corrupt HCL output, or might switch to `Environment` (unsandboxed) without understanding the injection risk if input validation were ever weakened.

**Recommendation.**

Add an inline comment explaining the intentional configuration:

```python
env = SandboxedEnvironment(
    loader=self._make_loader(),
    # autoescape=False is intentional: HCL output is not HTML.
    # HTML escaping would corrupt values (e.g., & in SSH keys -> &amp;).
    # Injection prevention is handled by:
    #   1. SandboxedEnvironment (blocks Python builtins/os/subprocess in templates)
    #   2. _validate_config() allowlist regexes on all interpolated values (C-04)
    autoescape=False,
    keep_trailing_newline=True,
)
```

---

## L2 Strategic Implications

### Security Posture Assessment

The reorganization does not regress any existing security control. Both pre-existing protections (`SandboxedEnvironment`, input allowlist regexes) are present and unchanged after the move. The template path is now a hardcoded string within `generate()` rather than being derived from external input, which is a marginal improvement over the prior structure.

### Systemic Patterns

**Pattern 1: Validation lives far from the trust boundary.**
`_validate_config` is called inside `HclGenerator.generate()`, which is the right place for template-injection prevention. However, `TerraformProvisionerAdapter.provision()` also accepts a `ProvisionConfig` domain object that it converts to a `dict` (adapter lines 133–144). The domain object's own validation (if any) is bypassed by the `isinstance(config, dict)` branch at line 133 — a raw `dict` passed directly to `provision()` skips any VO-level constraints and relies solely on `_validate_config`. This is not a vulnerability in the current call graph but creates a fragile single-validation-point dependency.

**Pattern 2: Runtime artifact paths not systematically excluded.**
The `.gitignore` was updated for the OPSEC-motivated exclusion of state files and provider cache (`# Terraform state and provider cache (OPSEC R-GITIGNORE)` comment, lines 58–64) but the generated HCL files themselves were not included in that same batch. This suggests the exclusion was written with the provider cache and state in mind, but the rendered template output was not considered a sensitive artifact at that time. Now that the template renders operator IPs and SSH public keys, the generated `.tf` files should be treated as sensitive at the same level as `.tfstate` files.

**Pattern 3: Terraform CLI version drift vs. provider pin mismatch.**
The provider uses exact pinning (`= 2.43.0`). The CLI uses a floor (`>= 1.0.0`). This asymmetry suggests the supply chain concern was applied to the provider but not carried through to the CLI. A consistent pinning posture for both components would close the gap.

### Threat Model Correlation

No threat model artifact was passed for this review. Based on the code, the implicit threat model is:
- Malicious config values injected through the `config` dict to achieve Jinja2 template injection or HCL manipulation — mitigated by allowlist regex validation and `SandboxedEnvironment`.
- Generated state or secrets committed to version control — partially mitigated by `.gitignore` (gap: `main.tf` not excluded, FINDING-001).
- Supply chain manipulation of Terraform provider — mitigated by exact provider pin in `versions.tf`.

The missing `.gitignore` entry (FINDING-001) is the only finding where a concrete sensitive data exposure path exists in the current artifact set.
