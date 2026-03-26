# Credential Naming Convention

> Reference documentation for Jerry credential identifiers, type registry, resolution order, port API, and security properties.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Service Name](#service-name) | Keyring service identifier constant |
| [Username Format](#username-format) | Dot-delimited username structure |
| [Type Registry](#type-registry) | All defined credential types with status |
| [Resolution Order](#resolution-order) | Tiered lookup sequence |
| [CredentialStorePort API](#credentialstoreport-api) | Port interface methods and contracts |
| [Environment Variable Naming](#environment-variable-naming) | Env-var pattern and defined variables |
| [Security Properties](#security-properties) | Per-tier security characteristics |

---

## Service Name

| Attribute | Value |
|-----------|-------|
| Service name | `jerry` |
| Scope | All Jerry credentials across all namespaces |
| Storage location | OS keychain (macOS Keychain, Linux Secret Service, Windows Credential Manager) |

The service name is a constant. All credentials registered under Jerry share this single service name, differentiated by their structured username.

**Example keychain entry:**

```
service:  jerry
username: proxy.digitalocean.api-key
password: dop_v1_...
```

---

## Username Format

```
{namespace}.{scope}.{type}
```

| Component | Position | Description | Constraints |
|-----------|----------|-------------|-------------|
| `namespace` | 1 | Logical domain grouping | Lowercase ASCII; defined in [Type Registry](#type-registry) |
| `scope` | 2 | Instance discriminator within the namespace | Lowercase ASCII; provider name, engagement ID, or tool name |
| `type` | 3 | Credential material type | Lowercase ASCII with hyphens; defined in [Type Registry](#type-registry) |

Delimiter: `.` (ASCII full stop). Three components required. No whitespace permitted.

**Constructed examples:**

| Input | Username |
|-------|----------|
| namespace=`proxy`, scope=`digitalocean`, type=`api-key` | `proxy.digitalocean.api-key` |
| namespace=`engagement`, scope=`ENG-001`, type=`ssh-private-key` | `engagement.ENG-001.ssh-private-key` |

---

## Type Registry

All defined credential types. The `Username` column shows a concrete example using a representative scope value.

| Namespace | Scope | Type | Username (example) | Description | Status |
|-----------|-------|------|-------------------|-------------|--------|
| `proxy` | `{provider}` | `api-key` | `proxy.digitalocean.api-key` | Cloud provider API token for node provisioning | Implemented |
| `proxy` | `{provider}` | `api-key` | `proxy.vultr.api-key` | Vultr API token for node provisioning | Planned (FEAT-023-008) |
| `proxy` | `{provider}` | `api-key` | `proxy.hetzner.api-key` | Hetzner API token for node provisioning | Planned (FEAT-023-008) |
| `engagement` | `{eng-id}` | `ssh-private-key` | `engagement.ENG-001.ssh-private-key` | Per-engagement SSH private key | Planned |
| `engagement` | `{eng-id}.{node-id}` | `socks5` | `engagement.ENG-001.do-12345.socks5` | Per-node SOCKS5 proxy credentials | Planned |
| `tool` | `{tool-name}` | `api-key` | `tool.shodan.api-key` | External tool API key | Future |
| `cloud` | `{provider}` | `ssh-passphrase` | `cloud.digitalocean.ssh-passphrase` | SSH key passphrase for cloud provider key | Future |

**Scope placeholder conventions:**

| Placeholder | Format | Example |
|-------------|--------|---------|
| `{provider}` | Lowercase provider name | `digitalocean`, `vultr`, `hetzner` |
| `{eng-id}` | Engagement identifier | `ENG-001` |
| `{node-id}` | Node identifier | `do-12345` |
| `{tool-name}` | Lowercase tool name | `shodan` |

**Status definitions:**

| Status | Meaning |
|--------|---------|
| `Implemented` | Type is used in production code. Adapters exist. |
| `Planned` | Type is specified. Implementation tracked by the referenced feature or story. |
| `Future` | Type is reserved. No active implementation work. |

---

## Resolution Order

`CredentialStorePort` implementations are composed in the following priority sequence. The first tier to return a value terminates the lookup. If no tier contains the credential, `CredentialNotFoundError` is raised.

| Priority | Tier | Implementation Class | Lookup Mechanism |
|----------|------|---------------------|-----------------|
| 1 (highest) | OS keychain | `KeyringCredentialStore` | `keyring.get_password("jerry", username)` |
| 2 | Environment variable | `EnvCredentialStore` | `os.environ.get("JERRY_PROXY_{PROVIDER}_API_KEY")` |
| 3 (terminal) | Not found | — | Raises `CredentialNotFoundError` |

The `CredentialNotFoundError` message includes both the keychain store command and the environment variable name, listing both resolution paths.

---

## CredentialStorePort API

Module: `src.proxy_infra.domain.ports.credential_store_port`

```python
class CredentialStorePort(ABC):
```

Abstract port. Implementations: `KeyringCredentialStore`, `EnvCredentialStore`.

### Methods

#### `get_credential`

```python
def get_credential(self, provider_name: str) -> str
```

| Attribute | Value |
|-----------|-------|
| Parameter | `provider_name: str` — provider identifier, case-insensitive (e.g., `"digitalocean"`) |
| Returns | `str` — API key value; never `None` (FM-011) |
| Raises | `CredentialNotFoundError` — when no credential is configured for `provider_name` |

#### `store_credential`

```python
def store_credential(self, provider_name: str, api_key: str) -> None
```

| Attribute | Value |
|-----------|-------|
| Parameter `provider_name` | `str` — provider identifier |
| Parameter `api_key` | `str` — credential value to store |
| Returns | `None` |
| Raises | Nothing (implementation-defined; keyring errors propagate as-is) |

**Durability note:** `EnvCredentialStore.store_credential` writes to the current process environment only. The value does not persist across process restarts. `KeyringCredentialStore.store_credential` writes to the OS keychain and persists across restarts.

#### `delete_credential`

```python
def delete_credential(self, provider_name: str) -> bool
```

| Attribute | Value |
|-----------|-------|
| Parameter | `provider_name: str` — provider identifier |
| Returns | `True` if the credential was found and deleted; `False` if not found |
| Raises | Nothing (implementation-defined) |

### Exception

```python
class CredentialNotFoundError(Exception)
```

Module: `src.proxy_infra.domain.exceptions.credential_not_found_error`

Raised by `get_credential` when no credential is found at any tier. The message includes the provider name and actionable remediation text identifying both storage paths.

---

## Environment Variable Naming

Pattern: `JERRY_PROXY_{PROVIDER}_API_KEY`

`{PROVIDER}` is the provider name uppercased. The prefix `JERRY_PROXY_` and suffix `_API_KEY` are constants defined in `EnvCredentialStore`.

| Environment Variable | Provider | Status |
|---------------------|----------|--------|
| `JERRY_PROXY_DIGITALOCEAN_API_KEY` | `digitalocean` | Implemented |
| `JERRY_PROXY_VULTR_API_KEY` | `vultr` | Planned (FEAT-023-008) |
| `JERRY_PROXY_HETZNER_API_KEY` | `hetzner` | Planned (FEAT-023-008) |

**Example:**

```
JERRY_PROXY_DIGITALOCEAN_API_KEY=dop_v1_abc123...
```

`EnvCredentialStore` accepts the `provider_name` argument in any case and uppercases it internally when constructing the variable name.

---

## Security Properties

| Property | `KeyringCredentialStore` (Keychain tier) | `EnvCredentialStore` (Env var tier) |
|----------|------------------------------------------|--------------------------------------|
| Encrypted at rest | Yes — OS Secure Enclave (macOS) or equivalent | No |
| Authentication required to read | Yes — Touch ID or user password (macOS) | No |
| Visible in process environment | No | Yes — readable via `/proc/{pid}/environ` or equivalent |
| Visible in tool output | No — credential value never passed to logging calls (APIKEY-002) | If echoed by shell or logging code |
| Persists across process restart | Yes | Only if set in shell profile or launch configuration |
| Available in headless CI | Depends on keyring backend; may be unavailable without desktop session | Yes — primary tier for CI |

**Constraint APIKEY-002:** Credential values are never passed to any logging call in either implementation. Only the provider name is logged.

**Constraint FM-011:** `get_credential` raises `CredentialNotFoundError` on miss; it never returns `None`.
