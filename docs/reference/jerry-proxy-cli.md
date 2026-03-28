# jerry proxy -- Proxy Infrastructure CLI Reference

> **Diataxis quadrant:** Reference
> **Audience:** Red team operators managing proxy infrastructure via the Jerry CLI

## Document Sections

| Section | Purpose |
|---------|---------|
| [Synopsis](#synopsis) | Command structure overview |
| [Credential Management](#credential-management) | `jerry proxy credentials set/check/delete` |
| [Engagement Pipeline](#engagement-pipeline) | `jerry proxy engage` |
| [Status](#status) | `jerry proxy status` |
| [Destroy](#destroy) | `jerry proxy destroy` |
| [Garbage Collection](#garbage-collection) | `jerry proxy gc` |
| [Exit Codes](#exit-codes) | Return code reference |
| [Environment Variables](#environment-variables) | Env var fallbacks |
| [Security Zones](#security-zones) | Operation zone classification |

---

## Synopsis

```
jerry proxy <command> [options]
jerry proxy credentials <action> <provider>
jerry proxy engage <config.yaml> [--full-pipeline]
jerry proxy status --engagement <id>
jerry proxy destroy --engagement <id> [--node-ids <id>...]
jerry proxy gc --engagement <id> [--dry-run | --confirm]
```

The `proxy` namespace manages proxy infrastructure for red team engagements. All commands that modify cloud resources are Zone 3 operations requiring operator approval (P-020).

---

## Credential Management

### jerry proxy credentials set

Store a cloud provider API key in macOS Keychain.

```
jerry proxy credentials set <provider>
```

| Argument | Required | Description |
|----------|----------|-------------|
| `provider` | Yes | Cloud provider name (e.g., `digitalocean`) |

Prompts for the API key via `getpass` (no echo). The key is stored in macOS Keychain as `jerry/proxy.<provider>.api-key`.

**Example:**

```
$ jerry proxy credentials set digitalocean
Enter digitalocean API key:
Stored in macOS Keychain as jerry/proxy.digitalocean.api-key
```

### jerry proxy credentials check

Check whether a credential exists without revealing the value.

```
jerry proxy credentials check <provider>
```

| Argument | Required | Description |
|----------|----------|-------------|
| `provider` | Yes | Cloud provider name |

Checks Keychain first, then environment variable `JERRY_PROXY_<PROVIDER>_API_KEY`.

**Exit codes:** 0 if found, 1 if not found.

**JSON output** (`--json`):

```json
{"found": true, "provider": "digitalocean", "source": "keychain"}
```

### jerry proxy credentials delete

Remove a stored credential from macOS Keychain.

```
jerry proxy credentials delete <provider>
```

| Argument | Required | Description |
|----------|----------|-------------|
| `provider` | Yes | Cloud provider name |

**Exit codes:** 0 if deleted, 1 if not found.

---

## Engagement Pipeline

### jerry proxy engage

Run the hands-free proxy pipeline from an engagement config file.

```
jerry proxy engage <config> [--full-pipeline]
```

| Argument / Flag | Required | Description |
|-----------------|----------|-------------|
| `config` | Yes | Path to engagement YAML config file |
| `--full-pipeline` | No | Run the full engage-to-route pipeline (provision + inject + verify + compose). Default: provision only. |

**Stages** (when `--full-pipeline` is set):

1. Parse engagement YAML config
2. Create credential directory (`<config_dir>/credentials/`)
3. Generate Ed25519 SSH keypair
4. Build `ProvisionConfig` from config + generated key
5. Provision nodes via cloud provider API
6. Inject SSH credentials, verify SOCKS connectivity, generate compose manifests

**Zone 3 operation** -- requires operator approval.

**Example:**

```
$ jerry proxy engage engagements/RED-0003/config.yaml --full-pipeline
Engaged 2 proxy node(s):
  node-abc123  203.0.113.10  nyc3
  node-def456  203.0.113.11  sfo3
```

---

## Status

### jerry proxy status

List proxy nodes for an engagement.

```
jerry proxy status --engagement <id>
```

| Flag | Required | Description |
|------|----------|-------------|
| `--engagement` | Yes | Engagement ID to query (e.g., `RED-0001`) |

**Zone 1 operation** -- read-only, no pre-flight check required.

**JSON output** (`--json`):

```json
{
  "engagement": "RED-0001",
  "nodes": [
    {"id": "node-abc", "ip": "203.0.113.10", "region": "nyc3", "status": "active"}
  ]
}
```

---

## Destroy

### jerry proxy destroy

Tear down all or specified proxy nodes for an engagement.

```
jerry proxy destroy --engagement <id> [--node-ids <id>...]
```

| Flag | Required | Description |
|------|----------|-------------|
| `--engagement` | Yes | Engagement ID |
| `--node-ids` | No | Specific node IDs to destroy. Default: all nodes for engagement. |

**Zone 3 operation** -- requires operator approval.

**Exit codes:** 0 if all nodes destroyed successfully, 1 if any node failed.

---

## Garbage Collection

### jerry proxy gc

Detect and optionally destroy orphaned proxy nodes.

```
jerry proxy gc --engagement <id> [--dry-run | --confirm]
```

| Flag | Required | Description |
|------|----------|-------------|
| `--engagement` | Yes | Engagement ID to search for orphaned resources |
| `--dry-run` | No | List orphans without destroying (default) |
| `--confirm` | No | Destroy all discovered orphans. **Zone 3 operation.** |

Uses the engagement-tag-scoped query (ISOLATION-002) -- never performs a global sweep.

**JSON output** (`--json`):

```json
{
  "engagement": "RED-0001",
  "dry_run": true,
  "orphan_ids": ["node-orphan-1", "node-orphan-2"],
  "count": 2
}
```

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error (credential not found, partial destroy failure, config not found) |
| 2 | Invalid usage (bad arguments, unrecognized subcommand) |

---

## Environment Variables

| Variable | Purpose | Fallback For |
|----------|---------|-------------|
| `JERRY_PROXY_<PROVIDER>_API_KEY` | Cloud provider API key | `jerry proxy credentials check` checks this after Keychain |
| `DIGITALOCEAN_ACCESS_TOKEN` | DigitalOcean API token (used by adapter) | `DigitalOceanProvisionerAdapter.from_env()` |

---

## Security Zones

| Zone | Commands | Description |
|------|----------|-------------|
| Zone 1 (Read-only) | `status`, `credentials check`, `gc --dry-run` | No cloud resources modified |
| Zone 3 (Mutating) | `engage`, `destroy`, `gc --confirm`, `credentials set/delete` | Cloud resources created or destroyed; requires P-020 approval |

---

*References: STORY-023-022, ADR-PROJ023-008, TASK-023-079*
