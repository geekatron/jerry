# eBPF Transparent Proxy Reference

> Authoritative specification for the 3-program BPF architecture, shared map schemas, BPF lifecycle manager, Envoy transparent TCP configuration, and container capability requirements used by the rainbow exploit sub-skill.

<!-- Quality criteria: skills/diataxis/rules/diataxis-standards.md Section 1 (R-01 through R-07) -->
<!-- Anti-patterns to avoid: RAP-01 (marketing claims), RAP-02 (instructions/recipes), RAP-03 (narrative explanation) -->
<!-- Voice: Neutral, precise, austere. No opinions, no superlatives. See Section 5. -->

## Document Sections

| Section | Purpose |
|---------|---------|
| [Architecture Overview](#architecture-overview) | Data flow diagram: connect4, sockops, getsockopt, Envoy |
| [BPF Programs](#bpf-programs) | Per-program hook type, function signature, behavior, skip conditions |
| [Shared Maps](#shared-maps) | maps.h — type, key, value, max_entries, writer, reader |
| [BPF Manager](#bpf-manager) | BpfManager class, methods, lifecycle sequence, rollback, constants |
| [Lifecycle Port](#lifecycle-port) | IBpfLifecyclePort protocol interface |
| [Envoy Configuration](#envoy-configuration) | Listeners, clusters, scope translator |
| [Container Requirements](#container-requirements) | Capabilities, volumes, sysctls |
| [Constraints](#constraints) | Cross-reference table of named constraints |
| [Source Files](#source-files) | Repository-relative file paths |

---

## Architecture Overview

Three BPF programs cooperate across two map chains to redirect outbound TCP connections from tool containers through Envoy's transparent TCP listener and restore the original destination for scope enforcement.

```
Tool Container (outbound connect())
        |
        | cgroup/connect4 fires
        v
[ connect4_redirect ]
  - Reads SO_MARK; skips if == 100
  - Skips loopback (127.0.0.0/8)
  - Stores cookie -> orig_dst in dst_lookup map
  - Rewrites destination to 127.0.0.1:15001
        |
        | TCP handshake completes (ACTIVE_ESTABLISHED)
        v
[ sockops_port_cookie ]
  - Writes src_port -> socket_cookie in port_cookie map
        |
        | Envoy calls getsockopt(SOL_IP, SO_ORIGINAL_DST)
        v
[ getsockopt_orig_dst ]
  - Reads port_cookie[peer_port] -> cookie
  - Reads dst_lookup[cookie] -> struct orig_dst
  - Writes sockaddr_in_bpf to optval buffer
        |
        v
Envoy transparent_tcp listener (port 15001)
  - envoy.filters.listener.original_dst recovers original destination
  - RBAC network filter (destination_ip scope enforcement) -> tcp_proxy -> original_dst_cluster
  - RBAC denial: connection closed for out-of-scope destinations
        |
        | original_dst_cluster upstream socket
        v
[ upstream bind: SO_MARK = 100 ]
  - Prevents connect4 from re-intercepting Envoy's own connections
```

---

## BPF Programs

All three programs are compiled to separate BPF object files. The load order in `_PROGRAMS` is connect4 first, sockops second, getsockopt third.

---

### `connect4`

| Attribute | Value |
|-----------|-------|
| Section | `SEC("cgroup/connect4")` |
| Function | `connect4_redirect(struct bpf_sock_addr *ctx)` |
| Hook type | cgroup/connect4 |
| Attach cgroup | Tool container cgroup |
| Object file | `connect4.bpf.o` |
| Pin name | `rainbow_connect4` |
| bpftool attach type | `connect4` |
| Source | `src/proxy_infra/ebpf_poc/connect4.bpf.c` |

**Skip conditions** — program returns 1 (allow, no redirect) when:

| Condition | Check |
|-----------|-------|
| SO_MARK equals `ENVOY_MARK` (100) | `bpf_getsockopt(SOL_SOCKET, SO_MARK)` returns 0 and mark == 100 |
| Destination is loopback | `(dst_ip_hbo & 0xff000000u) == 0x7f000000u` |

When `bpf_getsockopt` fails (non-zero return), mark is treated as 0. The program proceeds to intercept.

**On intercept:**

1. Reads socket cookie via `bpf_get_socket_cookie(ctx)`.
2. Stores `struct orig_dst { dst_ip = ctx->user_ip4, dst_port = ctx->user_port }` in `dst_lookup[cookie]` with `BPF_ANY`.
3. Overwrites `ctx->user_ip4` with `bpf_htonl(0x7f000001u)` (127.0.0.1).
4. Overwrites `ctx->user_port` with `bpf_htons(ENVOY_PORT)` (15001).

**Constants defined in this file:**

| Constant | Value | Type |
|----------|-------|------|
| `LOOPBACK_PREFIX` | `0x7f000000u` | `__u32` |
| `LOOPBACK_MASK` | `0xff000000u` | `__u32` |
| `SOL_SOCKET` | `1` | `int` (guarded by `#ifndef`) |
| `SO_MARK` | `36` | `int` (guarded by `#ifndef`) |

**Example — map entry written on intercept:**

```c
/* cookie = bpf_get_socket_cookie(ctx) */
struct orig_dst orig = {
    .dst_ip   = ctx->user_ip4,    /* network byte order */
    .dst_port = ctx->user_port,   /* network byte order, lower 16 bits */
};
bpf_map_update_elem(&dst_lookup, &cookie, &orig, BPF_ANY);
```

---

### `sockops`

| Attribute | Value |
|-----------|-------|
| Section | `SEC("sockops")` |
| Function | `sockops_port_cookie(struct bpf_sock_ops *skops)` |
| Hook type | cgroup/sock_ops |
| Attach cgroup | Tool container cgroup |
| Object file | `sockops.bpf.o` |
| Pin name | `rainbow_sockops` |
| bpftool attach type | `sock_ops` |
| Source | `src/proxy_infra/ebpf_poc/sockops.bpf.c` |

**Trigger condition:**

| Condition | Check |
|-----------|-------|
| Outbound TCP handshake complete | `skops->op == BPF_SOCK_OPS_ACTIVE_ESTABLISHED_CB` |

The program returns 1 immediately for all other `op` values.

**On trigger:**

1. Reads `skops->local_port` (`__u32`, host byte order) as the ephemeral source port.
2. Reads socket cookie via `bpf_get_socket_cookie(skops)`.
3. Stores `port_cookie[src_port] = cookie` with `BPF_ANY`.

**Example — map entry written on established connection:**

```c
__u32 src_port = skops->local_port;  /* host byte order */
__u64 cookie   = bpf_get_socket_cookie(skops);
bpf_map_update_elem(&port_cookie, &src_port, &cookie, BPF_ANY);
```

---

### `getsockopt`

| Attribute | Value |
|-----------|-------|
| Section | `SEC("cgroup/getsockopt")` |
| Function | `getsockopt_orig_dst(struct bpf_sockopt *ctx)` |
| Hook type | cgroup/getsockopt |
| Attach cgroup | Envoy container cgroup |
| Object file | `getsockopt.bpf.o` |
| Pin name | `rainbow_getsockopt` |
| bpftool attach type | `getsockopt` |
| Source | `src/proxy_infra/ebpf_poc/getsockopt.bpf.c` |

**Passthrough condition (constraint C6):**

The program returns 1 (passthrough) for every getsockopt call where `ctx->level != SOL_IP (0)` or `ctx->optname != SO_ORIGINAL_DST (80)`. All other getsockopt calls are unmodified.

**Constants defined in this file:**

| Constant | Value | Type |
|----------|-------|------|
| `SO_ORIGINAL_DST` | `80` | `int` |
| `SOL_IP` | `0` | `int` (guarded by `#ifndef`) |
| `AF_INET` | `2` | `int` (guarded by `#ifndef`) |

**On intercept (`SOL_IP:SO_ORIGINAL_DST`):**

1. Reads `ctx->sk->dst_port` (network byte order, lower 16 bits) and converts to host byte order: `bpf_ntohs((__u16)ctx->sk->dst_port)`. This is the tool container's ephemeral source port as seen from Envoy.
2. Looks up `port_cookie[peer_port]` — returns 1 on NULL (see diagnostic note below).
3. Looks up `dst_lookup[*cookie]` — returns 1 on NULL.
4. Bounds-checks `ctx->optval` against `ctx->optval_end` — returns 1 if buffer too small.
5. Writes `struct sockaddr_in_bpf` to `ctx->optval`.
6. Sets `ctx->retval = 0` (overrides kernel `-ENOPROTOOPT`).
7. Sets `ctx->optlen = sizeof(struct sockaddr_in_bpf)`.

**NULL lookup diagnostic:** A NULL result from either map lookup indicates one of: sockops has not fired yet for this connection (TCP handshake not yet `ESTABLISHED`), LRU eviction under concurrency exceeding 4096, or the connection was not intercepted by connect4 (loopback or SO_MARK bypass). Diagnostic: `bpftool map dump pinned /sys/fs/bpf/maps/port_cookie` and inspect for the peer port entry.

**Output struct `sockaddr_in_bpf`:**

| Field | Type | Value written |
|-------|------|---------------|
| `sin_family` | `__u16` | `AF_INET` (2) |
| `sin_port` | `__u16` | `(__u16)orig->dst_port` — network byte order; lower 16 bits of `ctx->user_port` stored by connect4 |
| `sin_addr` | `__u32` | `orig->dst_ip` — network byte order |
| `sin_zero[8]` | `__u8[8]` | zero-filled via `__builtin_memset` |

**Compiler barrier note:** An `asm volatile("" ::: "memory")` barrier separates the writes to `ctx->retval` and `ctx->optlen`. Without the barrier, clang -O2 may merge these two adjacent 32-bit writes into a single 64-bit store; the BPF verifier rejects 64-bit context field access.

**Example — output struct population:**

```c
struct sockaddr_in_bpf *sa = ctx->optval;
sa->sin_family = AF_INET;
sa->sin_port   = (__u16)orig->dst_port;
sa->sin_addr   = orig->dst_ip;
__builtin_memset(sa->sin_zero, 0, sizeof(sa->sin_zero));
ctx->retval = 0;
asm volatile("" ::: "memory");
ctx->optlen = (__s32)sizeof(struct sockaddr_in_bpf);
```

---

## Shared Maps

Maps are defined in `src/proxy_infra/ebpf_poc/maps.h` and included by all three BPF programs. Constraint C7 requires map schemas to be defined in this shared header only.

---

### `dst_lookup`

| Attribute | Value |
|-----------|-------|
| Map type | `BPF_MAP_TYPE_LRU_HASH` |
| Key type | `__u64` — socket cookie |
| Value type | `struct orig_dst` |
| `max_entries` | `4096` |
| Written by | `connect4` |
| Read by | `getsockopt` |
| Pin path | `_DEFAULT_MAP_DIR` (`/sys/fs/bpf/rainbow_maps`) via `bpftool prog load ... pinmaps` |

**`struct orig_dst` fields:**

| Field | Type | Byte order | Description |
|-------|------|------------|-------------|
| `dst_ip` | `__u32` | Network | Original destination IPv4 address |
| `dst_port` | `__u32` | Network | Original destination port; lower 16 bits significant |

**LRU eviction behavior:** When concurrent connections exceed 4096, the oldest entries are evicted. A `getsockopt` lookup for an evicted cookie returns NULL; the program returns 1 (passthrough) and Envoy receives the kernel default `-ENOPROTOOPT`. Active connections within map capacity are unaffected.

**Example — map definition in maps.h:**

```c
struct {
    __uint(type, BPF_MAP_TYPE_LRU_HASH);
    __uint(max_entries, 4096);
    __type(key,   __u64);           /* socket cookie */
    __type(value, struct orig_dst);
} dst_lookup SEC(".maps");
```

---

### `port_cookie`

| Attribute | Value |
|-----------|-------|
| Map type | `BPF_MAP_TYPE_LRU_HASH` |
| Key type | `__u32` — source port, host byte order |
| Value type | `__u64` — socket cookie |
| `max_entries` | `4096` |
| Written by | `sockops` |
| Read by | `getsockopt` |
| Pin path | `_DEFAULT_MAP_DIR` (`/sys/fs/bpf/rainbow_maps`) via `bpftool prog load ... pinmaps` |

Key is `__u32` to match `bpf_sock_ops->local_port` type. Host byte order matches `sockops`'s write format. LRU eviction automatically overwrites stale entries from TIME_WAIT port reuse.

**Example — map definition in maps.h:**

```c
struct {
    __uint(type, BPF_MAP_TYPE_LRU_HASH);
    __uint(max_entries, 4096);
    __type(key,   __u32);   /* source port, host byte order */
    __type(value, __u64);   /* socket cookie */
} port_cookie SEC(".maps");
```

---

### Shared Constants (maps.h)

| Constant | Value | Constraint |
|----------|-------|------------|
| `ENVOY_PORT` | `15001` | C8: reserved for Envoy transparent TCP listener only |
| `ENVOY_MARK` | `100` | C2: must be exactly 100; must match Envoy `upstream_bind_config.socket_options` |

---

## BPF Manager

### `BpfManager`

| Attribute | Value |
|-----------|-------|
| Class | `BpfManager` |
| Module | `src/proxy_infra/infrastructure/bpf/bpf_manager.py` |
| Implements | `IBpfLifecyclePort` protocol |
| Architecture layer | Infrastructure (H-07 compliant; subprocess and pathlib permitted) |
| Constraints | H-10 (one class per file), H-11 (type annotations), C5, B3, F-8 |

#### Module-Level Constants

| Constant | Value | Type |
|----------|-------|------|
| `_BPFFS_ROOT` | `/sys/fs/bpf` | `Path` |
| `_DEFAULT_MAP_DIR` | `/sys/fs/bpf/rainbow_maps` | `Path` |
| `_CGROUP_DOCKER_ROOT` | `/sys/fs/cgroup/docker` | `Path` |
| `_INTERCEPT_CGROUP_NAME` | `jerry-intercept` | `str` |

#### `_PROGRAMS` Tuple

The `_PROGRAMS` module-level tuple defines the three programs in load order. Load order is significant: connect4 must be loaded first.

| Index | `name` | `object_suffix` | `pin_name` | `attach_type` |
|-------|--------|-----------------|------------|---------------|
| 0 | `connect4` | `connect4.bpf.o` | `rainbow_connect4` | `connect4` |
| 1 | `sockops` | `sockops.bpf.o` | `rainbow_sockops` | `sock_ops` |
| 2 | `getsockopt` | `getsockopt.bpf.o` | `rainbow_getsockopt` | `getsockopt` |

#### Constructor

```python
BpfManager(
    bpf_object_path: str,
    bridge_port: int = 15001,
    pin_path: str | None = None,
    map_dir: str | None = None,
) -> None
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `bpf_object_path` | `str` | — | Path to compiled BPF object file or directory. If a file path, parent directory is used. |
| `bridge_port` | `int` | `15001` | Envoy listening port checked by `is_ready()`. |
| `pin_path` | `str \| None` | `None` | Deprecated; ignored. Pin paths are derived from `_PROGRAMS`. |
| `map_dir` | `str \| None` | `None` | Override for bpffs map directory. Defaults to `_DEFAULT_MAP_DIR`. |

#### Public Methods

---

##### `load_and_attach`

```python
def load_and_attach(self, container_id: str) -> None
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `container_id` | `str` | Docker container ID (short or full). |

**Raises:** `RuntimeError` if any BPF load, pin, or attachment fails.

**Lifecycle sequence:**

| Step | Action | Constraint |
|------|--------|------------|
| 1 | Load and pin all 3 programs atomically; rollback on partial failure | C5 |
| 2 | Detach any stale BPF from root cgroup (`/sys/fs/cgroup`) | F-2 |
| 3 | Locate container cgroup under `_CGROUP_DOCKER_ROOT` | — |
| 4 | Create `jerry-intercept` as child cgroup of container cgroup | F-8 |
| 5 | Attach pinned `connect4` program to container cgroup | — |

**Rollback behavior:** If any program in step 1 fails to load, all previously loaded programs in `_loaded_programs` are unpinned in reverse order via `_rollback_loaded()`.

---

##### `detach_and_cleanup`

```python
def detach_and_cleanup(self) -> None
```

Detaches all 3 programs from the recorded attached cgroup and unpins all 3 pin paths from bpffs. Safe to call when `load_and_attach` was never completed. Constraint B3 applies: no programs remain pinned after this method returns.

Non-fatal on individual detach/unpin errors; warnings are logged.

---

##### `get_container_cgroup`

```python
def get_container_cgroup(self, container_id: str) -> str
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `container_id` | `str` | Short or full Docker container ID. |

**Returns:** Absolute path string to the container's cgroup directory under `_CGROUP_DOCKER_ROOT`.

**Raises:** `RuntimeError` if no matching cgroup directory is found.

---

##### `create_intercept_cgroup`

```python
def create_intercept_cgroup(self, container_cgroup: str) -> str
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `container_cgroup` | `str` | Absolute path to the container's cgroup directory. |

**Returns:** Absolute path string to the `jerry-intercept` child cgroup (`{container_cgroup}/jerry-intercept`).

**Raises:** `RuntimeError` if the child cgroup cannot be created.

Constraint F-8: `jerry-intercept` must be a child of the container cgroup, not of the root cgroup.

---

##### `is_ready`

```python
def is_ready(self) -> bool
```

**Returns:** `True` when all 3 programs are pinned on bpffs and Envoy is in LISTEN state on `bridge_port`.

Verifies via `bpftool prog show pinned {pin_path}` for each of the 3 programs, and via `ss -tlnp` for the port check.

---

## Lifecycle Port

### `IBpfLifecyclePort`

| Attribute | Value |
|-----------|-------|
| Protocol class | `IBpfLifecyclePort` |
| Module | `src/proxy_infra/domain/ports/bpf_lifecycle_port.py` |
| Metaclass | `typing.Protocol` with `runtime_checkable` |
| Architecture layer | Domain (H-07 compliant; no infrastructure or application imports) |
| Constraints | H-07, H-10, H-11 |

**Methods:**

| Method | Signature | Returns | Raises |
|--------|-----------|---------|--------|
| `load_and_attach` | `(self, container_id: str) -> None` | `None` | `RuntimeError` on BPF load, pin, or attachment failure |
| `is_ready` | `(self) -> bool` | `True` if BPF programs are pinned and Envoy is listening on port 15001 | — |
| `detach_and_cleanup` | `(self) -> None` | `None` | — (safe to call without prior `load_and_attach`) |

**Example — protocol declaration:**

```python
@runtime_checkable
class IBpfLifecyclePort(Protocol):
    def load_and_attach(self, container_id: str) -> None: ...
    def is_ready(self) -> bool: ...
    def detach_and_cleanup(self) -> None: ...
```

---

## Envoy Configuration

### `transparent_tcp` Listener

| Attribute | Value |
|-----------|-------|
| Listener name | `transparent_tcp` |
| Bind address | `0.0.0.0:15001` |
| Constraint | C8: port 15001 reserved for Envoy transparent TCP |

**Listener filter:**

| Filter name | Type | Purpose |
|-------------|------|---------|
| `envoy.filters.listener.original_dst` | `envoy.extensions.filters.listener.original_dst.v3.OriginalDst` | Recovers the BPF-redirected original destination via `SO_ORIGINAL_DST` |

**Filter chains:**

| Chain | `filter_chain_match` | Filter | Cluster |
|-------|---------------------|--------|---------|
| `scope_chain` | Single filter chain with RBAC + tcp_proxy | `envoy.filters.network.rbac` (scope enforcement) + `envoy.filters.network.tcp_proxy` (forwarding) | `original_dst_cluster` |

Scope enforcement uses the Envoy RBAC network filter with `destination_ip` permissions. The RBAC filter checks the restored destination IP from the `original_dst` listener filter. Connections to IPs not in the engagement scope are denied by RBAC before reaching the tcp_proxy filter.

Scope domains are DNS-resolved to /32 CIDRs at config generation time by `_resolve_scope_to_cidrs()`. Wildcard domains (e.g., `*.example.com`) cannot be resolved and log a warning — plain TCP connections to wildcard domains will be denied.

**Example — listener YAML:**

```yaml
name: transparent_tcp
address:
  socket_address:
    address: 0.0.0.0
    port_value: 15001
listener_filters:
- name: envoy.filters.listener.original_dst
  typed_config:
    '@type': type.googleapis.com/envoy.extensions.filters.listener.original_dst.v3.OriginalDst
filter_chains:
- filters:
  - name: envoy.filters.network.rbac
    typed_config:
      '@type': type.googleapis.com/envoy.extensions.filters.network.rbac.v3.RBAC
      stat_prefix: transparent_tcp_scope
      rules:
        action: ALLOW
        policies:
          engagement_scope:
            permissions:
            - destination_ip:
                address_prefix: 93.184.216.34
                prefix_len: 32
            principals:
            - any: true
  - name: envoy.filters.network.tcp_proxy
    typed_config:
      '@type': type.googleapis.com/envoy.extensions.filters.network.tcp_proxy.v3.TcpProxy
      stat_prefix: transparent_tcp
      cluster: original_dst_cluster
```

---

### `original_dst_cluster`

| Attribute | Value |
|-----------|-------|
| Cluster name | `original_dst_cluster` |
| `type` | `ORIGINAL_DST` |
| `lb_policy` | `CLUSTER_PROVIDED` (mandatory for `ORIGINAL_DST` type) |
| `connect_timeout` | `10s` |

**Upstream bind config socket options:**

| Field | Value | Description |
|-------|-------|-------------|
| `description` | `SO_MARK for BPF loop prevention (C2: must be 100)` | — |
| `level` | `1` | `SOL_SOCKET` |
| `name` | `36` | `SO_MARK` |
| `int_value` | `100` | `ENVOY_MARK`; must match `maps.h` `#define ENVOY_MARK 100` (C2) |
| `state` | `STATE_PREBIND` | Socket option applied before bind |

**Example — cluster YAML:**

```yaml
name: original_dst_cluster
type: ORIGINAL_DST
connect_timeout: 10s
lb_policy: CLUSTER_PROVIDED
upstream_bind_config:
  socket_options:
  - description: 'SO_MARK for BPF loop prevention (C2: must be 100)'
    level: 1
    name: 36
    int_value: 100
    state: STATE_PREBIND
```

---

### `deny_all_tcp` Cluster

| Attribute | Value |
|-----------|-------|
| Cluster name | `deny_all_tcp` |
| `type` | `STATIC` |
| `lb_policy` | `ROUND_ROBIN` |
| `connect_timeout` | `1s` |
| `endpoints` | `[]` (empty) |

Empty endpoints list causes Envoy to immediately close connections routed to this cluster.

**Example — cluster YAML:**

```yaml
name: deny_all_tcp
type: STATIC
connect_timeout: 1s
lb_policy: ROUND_ROBIN
load_assignment:
  cluster_name: deny_all_tcp
  endpoints: []
```

---

### Scope Translator

| Attribute | Value |
|-----------|-------|
| Module | `src/tool_exec/infrastructure/envoy/scope_translator.py` |
| Exception class | `ScopeTranslationError(Exception)` |

#### `translate_scope_to_envoy`

```python
def translate_scope_to_envoy(
    scope_path: Path,
    zone: int,
    *,
    include_c2: bool = False,
) -> list[dict[str, Any]]
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `scope_path` | `Path` | — | Path to the engagement scope YAML file. |
| `zone` | `int` | — | Target zone. Accepts `2` or `3` only. |
| `include_c2` | `bool` | `False` | When `True` and `zone == 3`, appends `c2_infrastructure` targets to the domain list. |

**Returns:** `list[dict[str, Any]]` — list of Envoy `virtual_host` dicts for injection into `route_config.virtual_hosts`.

**Raises:** `ScopeTranslationError` for invalid scope files, unsupported zones, or unsupported target types. `FileNotFoundError` if `scope_path` does not exist.

**Supported target types:**

| Target type | Extracted value | Notes |
|-------------|----------------|-------|
| `domain` | Bare domain and `domain:443` | Wildcard subdomains require explicit `*.domain` entry in scope; no auto-expansion |
| `ip` | IP and `ip:443` | IPv4 only |
| `url` | Host extracted from URL and `host:443` | Protocol and path stripped |
| `cloud_account` | Provider API domains from `_CLOUD_PROVIDER_DOMAINS` map | Format: `provider:account_id` |
| `ip_range` | Not supported | Raises `ScopeTranslationError` |

**Cloud provider domain mappings:**

| Provider key | Domains added |
|-------------|---------------|
| `aws` | `*.amazonaws.com`, `*.aws.amazon.com`, `sts.amazonaws.com` |
| `azure` | `*.azure.com`, `*.microsoftonline.com`, `management.azure.com`, `login.microsoftonline.com` |
| `gcp` | `*.googleapis.com`, `accounts.google.com`, `oauth2.googleapis.com`, `cloudresourcemanager.googleapis.com` |

---

#### `generate_envoy_config`

```python
def generate_envoy_config(
    base_config_path: Path,
    scope_path: Path,
    output_path: Path,
    zone: int,
    *,
    include_c2: bool = False,
) -> Path
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `base_config_path` | `Path` | — | Path to the base Envoy config template YAML. |
| `scope_path` | `Path` | — | Path to the engagement scope YAML. |
| `output_path` | `Path` | — | Path to write the generated Envoy config. |
| `zone` | `int` | — | Target zone (`2` or `3`). |
| `include_c2` | `bool` | `False` | Include `c2_infrastructure` targets (Zone 3 only). |

**Returns:** `Path` to the generated config file.

**Raises:** `ScopeTranslationError` on translation or config generation failure. `FileNotFoundError` if base config or scope file does not exist.

**Actions performed on the base config:**

| Action | Function called |
|--------|----------------|
| Inject scope `virtual_host` entries before `deny_all` catch-all | `_add_transparent_tcp_listener` |
| Append `transparent_tcp` listener on port 15001 | `_add_transparent_tcp_listener` |
| Append `original_dst_cluster` with `SO_MARK=100` | `_add_original_dst_cluster` |
| Append `deny_all_tcp` cluster with no endpoints | `_add_deny_all_tcp_cluster` |

The output file is prefixed with a `# GENERATED` comment block. The base config must contain a `deny_all` virtual_host (domains `["*"]`); `generate_envoy_config` raises `ScopeTranslationError` if absent.

---

## Container Requirements

### `bpf-init` Sidecar

| Requirement | Value |
|-------------|-------|
| Linux capabilities | `CAP_BPF`, `CAP_NET_ADMIN`, `CAP_SYS_ADMIN` |
| `no-new-privileges` | Set |
| Purpose | Loads and pins BPF programs; holds kernel capabilities so tool containers require none |

### Tool Containers

| Requirement | Value | Constraint |
|-------------|-------|------------|
| Linux capabilities | None (zero) | DC-2: init container pattern; capabilities isolated to sidecar |
| bpffs mount | Read-only bind mount at `/sys/fs/bpf` | Allows `bpftool` reads without write access |
| BPF objects volume | Read-only bind mount (compiled `.bpf.o` files) | — |
| IPv6 | Disabled via `net.ipv6.conf.all.disable_ipv6=1` sysctl | DC-4: connect4 intercepts IPv4 only; IPv6 connections bypass BPF undetected |

---

## Constraints

Named constraints referenced in source code comments, docstrings, and architecture notes.

| ID | Statement |
|----|-----------|
| C2 | `ENVOY_MARK` must be exactly `100`. Must match between `maps.h` and Envoy `upstream_bind_config.socket_options.int_value`. **Security boundary:** SO_MARK is settable by any process with `CAP_NET_ADMIN`. The loop prevention mechanism depends on tool containers having **zero** capabilities (DC-2: init container pattern). If DC-2 is violated (tool container gains `CAP_NET_ADMIN`), a process could set SO_MARK=100 to bypass BPF interception entirely. |
| C5 | During an active engagement, all 3 BPF programs must remain loaded. Partial loading (fewer than 3 programs) is prohibited. **Failure mode:** connect4-only (no sockops/getsockopt) is **fail-open** — connections redirect to Envoy port 15001 but Envoy cannot recover the original destination, so connections fail or bypass scope enforcement. sockops-only or getsockopt-only have no interception effect. `BpfManager.load_and_attach()` rolls back all programs atomically if any program fails to load. |
| C6 | `getsockopt` intercepts only `SOL_IP:SO_ORIGINAL_DST` (level `0`, optname `80`). All other getsockopt calls pass through unmodified. |
| C7 | Map schemas must be defined in the shared header `maps.h` only. Individual program files must not redefine map structures. |
| C8 | `ENVOY_PORT` must be exactly `15001`. Port 15001 is reserved for the Envoy transparent TCP listener. |
| B3 | BPF programs must not remain attached or pinned after teardown. `detach_and_cleanup()` must complete successfully before engagement termination. |
| F-2 | On `load_and_attach`, any stale BPF attached to the root cgroup (`/sys/fs/cgroup`) must be detached before per-container attachment. |
| F-8 | The `jerry-intercept` cgroup must be a child of the container cgroup. It must not be created directly under the root cgroup. |
| DC-1 | The `dst_lookup` map is keyed by socket cookie (per-socket unique identifier) to ensure concurrent connection safety. |
| DC-2 | BPF capabilities are held by the `bpf-init` init container only. Tool containers carry zero Linux capabilities. |
| DC-4 | IPv6 is disabled on tool containers via sysctl. The `connect4` BPF program intercepts IPv4 only. |

---

## Source Files

| File | Description |
|------|-------------|
| `src/proxy_infra/ebpf_poc/maps.h` | Shared BPF map schemas: `struct orig_dst`, `dst_lookup`, `port_cookie`, `ENVOY_PORT`, `ENVOY_MARK` |
| `src/proxy_infra/ebpf_poc/connect4.bpf.c` | BPF cgroup/connect4 program: outbound connect() interception and redirection |
| `src/proxy_infra/ebpf_poc/sockops.bpf.c` | BPF cgroup/sock_ops program: source port to socket cookie mapping |
| `src/proxy_infra/ebpf_poc/getsockopt.bpf.c` | BPF cgroup/getsockopt program: SO_ORIGINAL_DST interception and original destination restoration |
| `src/proxy_infra/infrastructure/bpf/bpf_manager.py` | `BpfManager` class: 3-program lifecycle management |
| `src/proxy_infra/domain/ports/bpf_lifecycle_port.py` | `IBpfLifecyclePort` protocol: domain layer port definition |
| `src/tool_exec/infrastructure/envoy/scope_translator.py` | `ScopeTranslator`: engagement scope to Envoy config translation |
| `skills/rainbow/config/envoy/envoy-zone2-active.yaml` | Generated Zone 2 Envoy config example (includes transparent_tcp listener) |

---

## Verification Status

The unified 3-program BPF architecture is implemented (EN-023-009, EN-023-010), unit-tested, and E2E-verified. All 5 E2E integration tests pass (`tests/e2e/proxy_infra/test_unified_envoy_bpf.py`) against real Docker containers with real BPF programs. Tests verify: raw TCP through Envoy, concurrent connection correctness, RBAC scope enforcement denial, SO_MARK loop prevention, and 3-program cgroup attachment.

---

## Related

- **Explanation:** [About the eBPF Architecture Decision](../research/ebpf-architecture-decision.md) — Design rationale and architectural context
- **How-To Guide:** [Add BPF to a Tool Container](../playbooks/ebpf-tool-container.md) — Operational task instructions
- **Tutorial:** [eBPF Engagement Walkthrough](../tutorials/ebpf-engagement-walkthrough.md) — Hands-on engagement with BPF verification
