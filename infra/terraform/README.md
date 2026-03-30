# infra/terraform Reference

> Information-oriented reference for the Terraform provisioning layer.
> Quadrant: Reference. Audience: Engineers operating or extending the exploit framework.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Directory Layout](#directory-layout) | Filesystem structure of `infra/terraform/` |
| [Module: digitalocean-proxy](#module-digitalocean-proxy) | Resources, inputs, and outputs |
| [Template Rendering](#template-rendering) | HclGenerator and Jinja2 SandboxedEnvironment |
| [Provider Version Pinning](#provider-version-pinning) | versions.tf constraints |
| [Extension Interface](#extension-interface) | Contract for adding a new provider module |

---

## Directory Layout

```
infra/terraform/
└── modules/
    └── digitalocean-proxy/
        ├── main.tf.j2      # Jinja2 template; rendered per engagement
        └── versions.tf     # Provider version constraints
```

`modules/` contains one subdirectory per provider. Each provider subdirectory holds the Jinja2 template (`main.tf.j2`) and the provider pin (`versions.tf`). No root-level `main.tf` exists; all HCL is generated into an engagement-scoped working directory at runtime.

---

## Module: digitalocean-proxy

**Source:** `infra/terraform/modules/digitalocean-proxy/main.tf.j2`

The module provisions a single-droplet SOCKS5 proxy for a named engagement. Three DigitalOcean resources are created atomically within one `terraform apply` invocation.

### Resources Created

| Resource | Terraform Address | Description |
|----------|-------------------|-------------|
| SSH key | `digitalocean_ssh_key.proxy_key` | Uploads the operator's public key to DigitalOcean. Name: `jerry-proxy-{engagement_id}`. |
| Droplet | `digitalocean_droplet.proxy` | Ubuntu droplet running microsocks v1.0.4 as a systemd service. Name: `jerry-proxy-{engagement_id}-{region}-0`. Tagged `jerry-proxy` and `{engagement_id}`. |
| Firewall | `digitalocean_firewall.proxy_fw` | Restricts inbound TCP to ports 22 and `{socks_port}` from `{operator_ip}/32` only. Allows all outbound TCP. Name: `jerry-proxy-{engagement_id}-0`. |

The droplet `user_data` cloud-config installs `ufw`, `gcc`, `make`, and `git`; enables UFW with deny-incoming defaults; compiles and installs microsocks; generates random SOCKS5 credentials stored in `/etc/microsocks.env` (mode 0600); and starts the microsocks systemd service.

### Inputs

All inputs are Jinja2 template variables passed by `HclGenerator.generate()`. Every input is validated against an allowlist regex before rendering; see [Template Rendering](#template-rendering).

| Variable | Type | Constraints | Description |
|----------|------|-------------|-------------|
| `engagement_id` | string | Pattern: `^[A-Za-z0-9_-]+$` | Unique engagement identifier. Interpolated into resource names and tags. |
| `region` | string | Pattern: `^[a-z0-9-]+$` | DigitalOcean region slug (e.g., `nyc3`, `ams3`). |
| `size` | string | Pattern: `^[a-z0-9-]+$` | DigitalOcean droplet size slug (e.g., `s-1vcpu-1gb`). |
| `image` | string | Pattern: `^[a-z0-9.-]+$` | DigitalOcean image slug (e.g., `ubuntu-22-04-x64`). |
| `operator_ip` | string | Valid IPv4 or IPv6 address | Source IP for UFW rules and firewall inbound allowlist. Applied as `{operator_ip}/32` in the DigitalOcean firewall resource. |
| `ssh_public_key` | string | Matches `^ssh-(rsa\|ed25519\|ecdsa)[- ]\S+` | OpenSSH public key uploaded to DigitalOcean as `jerry-proxy-{engagement_id}`. |
| `socks_port` | integer | 1–65535 | TCP port microsocks listens on. Opened in UFW and DigitalOcean firewall from `operator_ip` only. |

**Example config dict:**

```python
{
    "engagement_id": "eng-042",
    "region": "nyc3",
    "size": "s-1vcpu-1gb",
    "image": "ubuntu-22-04-x64",
    "operator_ip": "203.0.113.10",
    "ssh_public_key": "ssh-ed25519 AAAA... operator@host",
    "socks_port": 1080,
}
```

### Outputs

| Output | Terraform Address | Type | Description |
|--------|-------------------|------|-------------|
| `droplet_ip` | `output.droplet_ip` | string | Public IPv4 address of the proxy droplet. |
| `droplet_id` | `output.droplet_id` | string | DigitalOcean numeric droplet ID. |
| `ssh_key_id` | `output.ssh_key_id` | string | DigitalOcean SSH key resource ID. |
| `firewall_id` | `output.firewall_id` | string | DigitalOcean firewall resource ID. |

---

## Template Rendering

**Source:** `src/proxy_infra/infrastructure/terraform/hcl_generator.py`

`HclGenerator` renders `main.tf.j2` into a caller-supplied working directory. The rendered file is always named `main.tf`.

### Class: HclGenerator

```
HclGenerator(template_dir: Path)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `template_dir` | `pathlib.Path` | Root of the templates directory. `HclGenerator` constructs a `FileSystemLoader` from this path. The template is resolved as `{template_dir}/digitalocean-proxy/main.tf.j2`. |

### Method: generate

```
HclGenerator.generate(config: dict[str, Any], work_dir: Path) -> Path
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `config` | `dict[str, Any]` | Engagement config. Required keys: `engagement_id`, `region`, `size`, `image`, `ssh_public_key`, `operator_ip`, `socks_port`. |
| `work_dir` | `pathlib.Path` | Directory to write `main.tf` into. Must exist before calling. |

**Returns:** `pathlib.Path` pointing to the written `main.tf`.

**Raises:** `ValueError` if any required field is absent, empty, or fails allowlist validation.

### Jinja2 Environment

`HclGenerator` instantiates `jinja2.sandbox.SandboxedEnvironment` with `autoescape=False` and `keep_trailing_newline=True`. `SandboxedEnvironment` restricts attribute access and disallows execution of arbitrary Python expressions within the template. All config values are validated against allowlist regexes before `template.render()` is called; this is the primary injection prevention layer (C-04).

**DigitalOcean token:** The rendered `main.tf` configures the `digitalocean` provider with no inline token. The provider reads `DIGITALOCEAN_TOKEN` from the environment at `terraform apply` time.

---

## Provider Version Pinning

**Source:** `infra/terraform/modules/digitalocean-proxy/versions.tf`

| Constraint | Value |
|------------|-------|
| Terraform CLI minimum | `>= 1.0.0` |
| `digitalocean/digitalocean` provider | `= 2.43.0` (exact pin) |

The provider is pinned to an exact version (`= 2.43.0`) to prevent supply chain drift. The same pin is declared in both `versions.tf` and the `terraform` block inside `main.tf.j2`; both must remain in sync when upgrading.

To upgrade the provider version: update the version string in `versions.tf` and in `main.tf.j2`, then run `terraform init -upgrade` in the engagement working directory.

---

## Extension Interface

A new provider module is a directory at `infra/terraform/modules/{provider}-proxy/` containing at minimum `main.tf.j2` and `versions.tf`.

### Required Template Variables

A conforming `main.tf.j2` must consume the same seven Jinja2 variables that `HclGenerator.generate()` passes. The generator passes exactly these names; templates referencing other names will produce unrendered placeholder text.

| Variable | Passed by HclGenerator |
|----------|------------------------|
| `engagement_id` | Yes |
| `region` | Yes |
| `size` | Yes |
| `image` | Yes |
| `operator_ip` | Yes |
| `ssh_public_key` | Yes |
| `socks_port` | Yes |

### Required Output Names

The orchestration layer reads output values by name after `terraform apply`. A conforming module must declare these four Terraform outputs:

| Output name | Expected value |
|-------------|----------------|
| `droplet_ip` | Public IP of the proxy instance |
| `droplet_id` | Provider-assigned instance ID |
| `ssh_key_id` | Provider-assigned SSH key ID |
| `firewall_id` | Provider-assigned firewall/security-group ID |

### HclGenerator Template Lookup

`HclGenerator.generate()` hardcodes the template path as `digitalocean-proxy/main.tf.j2` relative to `template_dir`:

```python
template = env.get_template("digitalocean-proxy/main.tf.j2")
```

A new provider module requires a corresponding `get_template()` call with the new module name. The `template_dir` passed to `HclGenerator.__init__()` must be the parent of all provider module directories (i.e., `infra/terraform/modules/`).

### Input Validation

`HclGenerator._validate_config()` applies seven allowlist regexes. New provider modules that require additional variables or relaxed constraints must extend `_validate_config()` accordingly. The existing seven validations are applied unconditionally for all provider modules.
