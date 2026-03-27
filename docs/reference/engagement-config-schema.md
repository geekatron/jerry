# Engagement Config Schema Reference

> Field-level specification for the Jerry engagement configuration YAML, schema version 1.0.0.

<!-- Quality criteria: skills/diataxis/rules/diataxis-standards.md Section 1 (R-01 through R-07) -->
<!-- Anti-patterns to avoid: RAP-01 (marketing claims), RAP-02 (instructions/recipes), RAP-03 (narrative explanation) -->
<!-- Voice: Neutral, precise, austere. No opinions, no superlatives. See Section 5. -->

## Document Sections

| Section | Purpose |
|---------|---------|
| [Overview](#overview) | Schema version, file-level constraints |
| [Section 1: engagement](#section-1-engagement) | Engagement metadata fields |
| [Section 2: scope](#section-2-scope) | Target and technique scope fields |
| [Section 3: infrastructure](#section-3-infrastructure) | Proxy and sensor infrastructure fields |
| [Section 4: teams](#section-4-teams) | Red and blue team operator fields |
| [Section 5: credentials](#section-5-credentials) | Credential reference fields |
| [Section 6: rules_of_engagement](#section-6-rules_of_engagement) | Authorization and data handling fields |
| [Section 7: purple_team](#section-7-purple_team) | Purple team exercise configuration fields |
| [Section 8: output](#section-8-output) | Report and archive output fields |
| [Mode-Specific Requirements](#mode-specific-requirements) | Required sections per engagement mode |
| [Credential Reference Format](#credential-reference-format) | Keychain and environment variable resolution |
| [Related](#related) | Companion documents |

---

## Overview

The engagement configuration YAML is the single input artifact consumed by `jerry cyber-ops engage`. It defines all parameters for one engagement session: identity, scope, infrastructure, teams, credentials, rules of engagement, purple-team behavior, and output.

| Property | Value |
|----------|-------|
| Schema version | 1.0.0 |
| File format | YAML |
| Authority | ADR-PROJ023-010 Decision 2 |
| Source feature | FEAT-023-006 (Engagement Config Integration) |
| Template path | `skills/cyber-ops/templates/engagement-config-template.yaml` |

**Constraint:** The credential value MUST NOT appear in this file. Only references (keychain key name or environment variable name) are permitted. See [Credential Reference Format](#credential-reference-format).

---

## Section 1: engagement

The `engagement` top-level key contains required identity metadata for the engagement.

| Field | Type | Required | Default | Constraints |
|-------|------|----------|---------|-------------|
| `id` | string | Yes | — | Format: `ENG-{N}` where N is a numeric sequence |
| `name` | string | Yes | — | Human-readable label; no format constraint |
| `type` | enum | Yes | — | See valid values below |
| `mode` | enum | Yes | — | `purple` \| `split` \| `single` |
| `start_date` | string | Yes | — | ISO 8601 date: `YYYY-MM-DD` |
| `end_date` | string | No | — | ISO 8601 date: `YYYY-MM-DD` |
| `classification` | enum | No | `confidential` | `public` \| `internal` \| `confidential` \| `restricted` |

**Valid values — `type`:**

| Value | Description |
|-------|-------------|
| `penetration_test` | Structured test of specific targets and techniques |
| `red_team` | Adversarial simulation with broader scope |
| `purple_team` | Collaborative red/blue exercise with correlation |
| `blue_team` | Defensive-only detection and response exercise |
| `threat_hunt` | Hypothesis-driven hunt for indicators of compromise |

**Valid values — `mode`:**

| Value | Description |
|-------|-------------|
| `purple` | Single operator performing both red and blue roles; requires `purple_team` section |
| `split` | Separate red and blue operators; requires both `teams.red` and `teams.blue` |
| `single` | Red operator only; `teams.blue` is not evaluated |

**Example:**

```yaml
engagement:
  id: "ENG-0042"
  name: "External perimeter assessment Q2-2026"
  type: "penetration_test"
  mode: "single"
  start_date: "2026-04-01"
  end_date: "2026-04-14"
  classification: "confidential"
```

---

## Section 2: scope

The `scope` top-level key defines authorized targets, techniques, and execution time constraints.

### `scope.targets`

| Field | Type | Required | Default | Constraints |
|-------|------|----------|---------|-------------|
| `targets` | sequence | Yes | — | Minimum one entry |
| `targets[].host` | string | Yes | — | IP address, CIDR notation, or hostname |
| `targets[].type` | enum | Yes | — | `ip` \| `cidr` \| `hostname` \| `url` |
| `targets[].description` | string | No | — | Free text label for the target |

**Valid values — `targets[].type`:**

| Value | Accepted host format |
|-------|---------------------|
| `ip` | Single IPv4 or IPv6 address |
| `cidr` | CIDR range, e.g. `10.0.0.0/24` |
| `hostname` | DNS name, e.g. `api.example.com` |
| `url` | Full URL including scheme, e.g. `https://example.com/app` |

### `scope.authorized_techniques`

| Field | Type | Required | Default | Constraints |
|-------|------|----------|---------|-------------|
| `authorized_techniques` | sequence of strings | No | `[]` | ATT&CK technique IDs, e.g. `T1595` |

### `scope.excluded_techniques`

| Field | Type | Required | Default | Constraints |
|-------|------|----------|---------|-------------|
| `excluded_techniques` | sequence of strings | No | `[]` | ATT&CK technique IDs explicitly forbidden |

### `scope.exclusions`

| Field | Type | Required | Default | Constraints |
|-------|------|----------|---------|-------------|
| `exclusions` | sequence | No | `[]` | Out-of-scope hosts |
| `exclusions[].host` | string | No | — | IP, CIDR, or hostname to exclude |
| `exclusions[].reason` | string | No | — | Free text justification |

### `scope.time_window`

| Field | Type | Required | Default | Constraints |
|-------|------|----------|---------|-------------|
| `time_window` | mapping | No | — | Omit to allow execution at any time |
| `time_window.timezone` | string | No | `UTC` | IANA timezone identifier |
| `time_window.start_hour` | integer | No | `0` | 0–23 (inclusive) |
| `time_window.end_hour` | integer | No | `24` | 1–24 (inclusive); `24` means end of day |
| `time_window.days` | sequence of strings | No | All days | Abbreviated day names: `mon` `tue` `wed` `thu` `fri` `sat` `sun` |

**Example:**

```yaml
scope:
  targets:
    - host: "203.0.113.0/28"
      type: "cidr"
      description: "DMZ subnet"
    - host: "api.example.com"
      type: "hostname"
      description: "Public API endpoint"
  authorized_techniques:
    - "T1595"
    - "T1590"
  excluded_techniques:
    - "T1498"
  exclusions:
    - host: "203.0.113.14"
      reason: "Production payment processor — out of scope"
  time_window:
    timezone: "America/New_York"
    start_hour: 20
    end_hour: 6
    days: ["mon", "tue", "wed", "thu", "fri"]
```

---

## Section 3: infrastructure

The `infrastructure` top-level key configures proxy node pools and detection sensors. Omitting this section is equivalent to `proxy.enabled: false` and `sensors.enabled: false`.

### `infrastructure.proxy`

| Field | Type | Required | Default | Constraints |
|-------|------|----------|---------|-------------|
| `proxy.enabled` | boolean | No | `false` | Set `true` to provision nodes |
| `proxy.provider` | enum | No | `digitalocean` | `digitalocean` \| `vultr` \| `hetzner` |
| `proxy.region` | string | No | `nyc1` | Provider-specific region identifier |
| `proxy.count` | integer | No | `1` | 1–10 (inclusive) |
| `proxy.proxy_type` | enum | No | `direct_socks5` | `direct_socks5` \| `ssh_tunnel` |
| `proxy.socks_port` | integer | No | `1080` | 1–65535; the port the SOCKS5 listener binds on each node |
| `proxy.operator_ip` | string | No | — | Allowlisted operator source IP; omit to skip IP allowlisting |
| `proxy.image` | string | No | `ubuntu-24-04-x64` | Provider OS image slug |
| `proxy.size` | string | No | `s-1vcpu-1gb` | Provider instance size slug |

**Valid values — `proxy.proxy_type`:**

| Value | Description |
|-------|-------------|
| `direct_socks5` | SOCKS5 daemon bound directly on the node |
| `ssh_tunnel` | SOCKS5 proxied over an SSH tunnel to the node |

**Example:**

```yaml
infrastructure:
  proxy:
    enabled: true
    provider: "digitalocean"
    region: "nyc1"
    count: 3
    proxy_type: "direct_socks5"
    socks_port: 1080
    operator_ip: "198.51.100.42"
    image: "ubuntu-24-04-x64"
    size: "s-1vcpu-1gb"
```

### `infrastructure.sensors`

| Field | Type | Required | Default | Constraints |
|-------|------|----------|---------|-------------|
| `sensors.enabled` | boolean | No | `false` | Set `true` to deploy detection sensors |
| `sensors.type` | enum | No | `wazuh` | `wazuh` \| `elastic` \| `splunk` |

**Valid values — `sensors.type`:**

| Value | Description |
|-------|-------------|
| `wazuh` | Wazuh SIEM agent deployment |
| `elastic` | Elastic Security agent deployment |
| `splunk` | Splunk Universal Forwarder deployment |

**Example:**

```yaml
  sensors:
    enabled: true
    type: "wazuh"
```

---

## Section 4: teams

The `teams` top-level key declares operator assignments. Required for `split` mode. Evaluated but not enforced in `single` and `purple` modes.

### `teams.red`

| Field | Type | Required | Default | Constraints |
|-------|------|----------|---------|-------------|
| `red.operator` | string | No | — | Operator name or ID |
| `red.role` | enum | No | `attacker` | `attacker` \| `validator` |

**Valid values — `teams.red.role`:**

| Value | Description |
|-------|-------------|
| `attacker` | Executes offensive techniques against targets |
| `validator` | Validates findings produced by another operator |

### `teams.blue`

| Field | Type | Required | Default | Constraints |
|-------|------|----------|---------|-------------|
| `blue.operator` | string | No | — | Operator name or ID; required for `split` mode |
| `blue.role` | enum | No | `defender` | `defender` \| `hunter` |

**Valid values — `teams.blue.role`:**

| Value | Description |
|-------|-------------|
| `defender` | Monitors, detects, and responds to red activity |
| `hunter` | Performs proactive threat hunting independent of red activity |

**Example:**

```yaml
teams:
  red:
    operator: "alice"
    role: "attacker"
  blue:
    operator: "bob"
    role: "defender"
```

---

## Section 5: credentials

The `credentials` top-level key holds references to secrets. The secret value MUST NOT appear here. Only the keychain key name or environment variable name is stored.

### `credentials.proxy_api_key`

| Field | Type | Required | Default | Constraints |
|-------|------|----------|---------|-------------|
| `proxy_api_key.source` | enum | Yes | — | `keychain` \| `environment` |
| `proxy_api_key.key_name` | string | No | — | Keychain key name; resolved as `jerry/{key_name}`. Required when `source` is `keychain`. |
| `proxy_api_key.env_var` | string | No | — | Environment variable name containing the secret value. Required when `source` is `environment`; also used as a fallback when `source` is `keychain` and the keychain lookup fails. |

**Valid values — `proxy_api_key.source`:**

| Value | Resolution behavior |
|-------|---------------------|
| `keychain` | Secret read from OS keychain under the key `jerry/{key_name}` |
| `environment` | Secret read from the named environment variable |

**Example:**

```yaml
credentials:
  proxy_api_key:
    source: "keychain"
    key_name: "proxy.digitalocean.api-key"
    env_var: "JERRY_PROXY_DIGITALOCEAN_API_KEY"
```

---

## Section 6: rules_of_engagement

The `rules_of_engagement` top-level key documents authorization, escalation, and data handling constraints. Recommended for all engagements.

| Field | Type | Required | Default | Constraints |
|-------|------|----------|---------|-------------|
| `authorization` | string | No | — | Path or URI to the signed authorization document |
| `escalation_contact` | string | No | — | Name, email, or phone number to contact on incident |
| `emergency_stop` | boolean | No | `true` | When `true`, the emergency stop capability is active |
| `notification_required` | boolean | No | `false` | When `true`, the target must be notified before testing begins |
| `data_handling` | enum | No | `no_exfil` | `no_exfil` \| `evidence_vault_only` \| `client_approved` |

**Valid values — `data_handling`:**

| Value | Description |
|-------|-------------|
| `no_exfil` | No data leaves the target environment |
| `evidence_vault_only` | Evidence written only to the local evidence vault |
| `client_approved` | Data handling per client-approved evidence agreement |

**Example:**

```yaml
rules_of_engagement:
  authorization: "docs/authorizations/ENG-0042-signed.pdf"
  escalation_contact: "security-lead@example.com"
  emergency_stop: true
  notification_required: false
  data_handling: "evidence_vault_only"
```

---

## Section 7: purple_team

The `purple_team` top-level key configures purple team exercise behavior. Required when `engagement.mode` is `purple`.

| Field | Type | Required | Default | Constraints |
|-------|------|----------|---------|-------------|
| `technique_approval` | enum | Yes (purple mode) | `per_technique` | `per_technique` \| `batch` \| `pre_approved` |
| `pivot_mode` | enum | Yes (purple mode) | `sequential` | `sequential` \| `interleaved` |
| `correlation_mode` | enum | Yes (purple mode) | `real_time` | `real_time` \| `post_execution` |

**Valid values — `technique_approval`:**

| Value | Description |
|-------|-------------|
| `per_technique` | Blue team approval required before each individual technique executes |
| `batch` | Blue team approves a batch of techniques; each in the batch runs without further approval |
| `pre_approved` | All techniques in `scope.authorized_techniques` are pre-approved; no runtime approval required |

**Valid values — `pivot_mode`:**

| Value | Description |
|-------|-------------|
| `sequential` | Red executes one technique completely; blue reviews; then the next technique begins |
| `interleaved` | Red and blue activities alternate within each technique execution window |

**Valid values — `correlation_mode`:**

| Value | Description |
|-------|-------------|
| `real_time` | Detection correlation evaluated as each technique executes |
| `post_execution` | Correlation evaluated after all techniques in a batch have executed |

**Example:**

```yaml
purple_team:
  technique_approval: "per_technique"
  pivot_mode: "sequential"
  correlation_mode: "real_time"
```

---

## Section 8: output

The `output` top-level key controls report generation and artifact retention.

| Field | Type | Required | Default | Constraints |
|-------|------|----------|---------|-------------|
| `report_format` | enum | No | `markdown` | `markdown` \| `pdf` \| `html` |
| `report_template` | enum | No | `default` | `default` \| `executive` \| `technical` |
| `archive_location` | string | No | — | Absolute or repo-relative path; overrides the default engagement archive directory |
| `retention_days` | integer | No | `90` | Minimum `1`; number of days engagement artifacts are retained before expiry |

**Valid values — `report_format`:**

| Value | Description |
|-------|-------------|
| `markdown` | Markdown file (`.md`) |
| `pdf` | PDF rendered from the Markdown source |
| `html` | HTML rendered from the Markdown source |

**Valid values — `report_template`:**

| Value | Description |
|-------|-------------|
| `default` | Standard engagement report template |
| `executive` | Condensed summary; findings without technical detail |
| `technical` | Full technical detail including tool output and evidence references |

**Example:**

```yaml
output:
  report_format: "markdown"
  report_template: "technical"
  archive_location: "work/engagements/ENG-0042"
  retention_days: 90
```

---

## Mode-Specific Requirements

This table states which sections are required, recommended, or optional per engagement mode value.

| Section | `purple` mode | `split` mode | `single` mode |
|---------|--------------|-------------|--------------|
| `engagement` | Required | Required | Required |
| `scope` | Required | Required | Required |
| `infrastructure` | Optional | Optional | Optional |
| `teams.red` | Required | Required | Optional |
| `teams.blue` | Required (same operator as red) | Required (distinct operator) | Not evaluated |
| `credentials` | Required when `infrastructure.proxy.enabled: true` | Required when `infrastructure.proxy.enabled: true` | Required when `infrastructure.proxy.enabled: true` |
| `rules_of_engagement` | Recommended | Recommended | Recommended |
| `purple_team` | Required | Not evaluated | Not evaluated |
| `output` | Optional | Optional | Optional |

---

## Credential Reference Format

All fields under `credentials` store references, not values. The resolution chain is:

| `source` value | Primary resolution | Fallback |
|---------------|--------------------|---------|
| `keychain` | OS keychain lookup under key `jerry/{key_name}` | `env_var` value, if present |
| `environment` | Environment variable named by `env_var` | None |

**Keychain key naming convention:** `{service}.{provider}.{secret-type}`

| Example key_name | Resolved keychain path | Secret purpose |
|-----------------|----------------------|----------------|
| `proxy.digitalocean.api-key` | `jerry/proxy.digitalocean.api-key` | DigitalOcean API key for proxy provisioning |
| `proxy.vultr.api-key` | `jerry/proxy.vultr.api-key` | Vultr API key for proxy provisioning |
| `proxy.hetzner.api-key` | `jerry/proxy.hetzner.api-key` | Hetzner API key for proxy provisioning |

**Constraint:** The `key_name` field holds the key name only. The actual credential value MUST be stored in the OS keychain or environment and MUST NOT appear in the engagement config file or be committed to version control.

---

## Related

- **How-To Guide:** [How to run an engagement](../how-to/run-engagement.md) — Task-oriented engagement execution steps
- **How-To Guide:** [How to configure proxy infrastructure](../how-to/configure-proxy.md) — Proxy pool provisioning steps
- **Explanation:** [About the engagement lifecycle](../explanation/engagement-lifecycle.md) — Design rationale and mode semantics
- **Template:** [`skills/cyber-ops/templates/engagement-config-template.yaml`](../../skills/cyber-ops/templates/engagement-config-template.yaml) — Annotated blank template
- **Template:** [`skills/cyber-ops/templates/pentest-template.yaml`](../../skills/cyber-ops/templates/pentest-template.yaml) — Pre-filled penetration test config
- **Template:** [`skills/cyber-ops/templates/purple-team-template.yaml`](../../skills/cyber-ops/templates/purple-team-template.yaml) — Pre-filled purple team config
