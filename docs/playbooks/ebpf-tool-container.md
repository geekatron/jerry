# Add BPF Transparent Proxy to a Tool Container

> Get all outbound TCP from your new tool container silently routed through Envoy for engagement scope enforcement.

<!-- Quality criteria: skills/diataxis/rules/diataxis-standards.md Section 1 (H-01 through H-07) -->
<!-- Anti-patterns to avoid: HAP-01 (no teaching), HAP-04 (no edge-case completeness) -->
<!-- Voice: Direct, action-oriented, efficient. No "why" digressions. See Section 5. -->

## Document Sections

| Section | Purpose |
|---------|---------|
| [Before You Begin](#before-you-begin) | What must already exist |
| [Step 1: Confirm bpf-init Is in Your Compose File](#step-1-confirm-bpf-init-is-in-your-compose-file) | Add the sidecar if missing |
| [Step 2: Add BPF Volumes and PATH to Your Tool Container](#step-2-add-bpf-volumes-and-path-to-your-tool-container) | Read-only mounts |
| [Step 3: Add depends_on Ordering](#step-3-add-depends_on-ordering) | Enforce startup sequence |
| [Step 4: Disable IPv6](#step-4-disable-ipv6) | Sysctls entry |
| [Step 5: Add Security Options](#step-5-add-security-options) | no-new-privileges |
| [Complete Example](#complete-example) | Full service definition |
| [Verification](#verification) | Confirm 3 BPF programs are attached |
| [Troubleshooting](#troubleshooting) | Common failure modes |
| [Related](#related) | Reference and explanation documents |

---

## Before You Begin

You need:

- A Docker Compose file for Zone 2 or Zone 3 that already has an Envoy service (`envoy-z2` or `envoy-z3`)
- The `bpf-builder:latest` image built and available locally (`docker images bpf-builder`)
- `bpf-objects` named volume declared in the `volumes:` section of the Compose file

---

## Step 1: Confirm bpf-init Is in Your Compose File

Check whether your Compose file already defines `bpf-init`. If it does, skip to [Step 2](#step-2-add-bpf-volumes-and-path-to-your-tool-container).

If it does not, add the YAML anchor and service definition:

```yaml
# At the top of the file, before services:
x-bpf-init-capabilities: &bpf-init-capabilities
  cap_add:
    - CAP_BPF
    - CAP_NET_ADMIN
    - CAP_SYS_ADMIN
  security_opt:
    - no-new-privileges:true
  volumes:
    - /sys/fs/bpf:/sys/fs/bpf
    - /sys/fs/cgroup:/sys/fs/cgroup:rw
    - bpf-objects:/opt/ebpf

services:

  bpf-init:
    image: bpf-builder:latest
    <<: *bpf-init-capabilities
    command: >
      sh -c "cp /build/connect4.bpf.o /opt/ebpf/connect4.bpf.o &&
             cp /build/sockops.bpf.o /opt/ebpf/sockops.bpf.o &&
             cp /build/getsockopt.bpf.o /opt/ebpf/getsockopt.bpf.o &&
             cp /usr/local/bin/bpftool /opt/ebpf/bpftool &&
             chmod +x /opt/ebpf/bpftool &&
             echo 'BPF artifacts ready' && sleep infinity"
    networks:
      - <your-zone-network>
    healthcheck:
      test: ["CMD-SHELL", "test -f /opt/ebpf/connect4.bpf.o && test -f /opt/ebpf/sockops.bpf.o && test -f /opt/ebpf/getsockopt.bpf.o"]
      interval: 2s
      timeout: 2s
      retries: 5
      start_period: 2s
```

Replace `<your-zone-network>` with your zone's internal network name (e.g., `zone2-active` or `zone3-exploit`).

Also add `bpf-objects` to the top-level `volumes:` section if it is not already there:

```yaml
volumes:
  bpf-objects:
```

---

## Step 2: Add BPF Volumes and PATH to Your Tool Container

Add these entries under your tool service:

```yaml
your-tool:
  volumes:
    - bpf-objects:/opt/ebpf:ro        # BPF programs + bpftool (read-only)
    - /sys/fs/bpf:/sys/fs/bpf:ro      # bpffs (read-only)
  environment:
    PATH: "/opt/ebpf:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
```

The `:ro` suffix on both mounts is required -- tool containers must not modify BPF programs or maps.

---

## Step 3: Add depends_on Ordering

Add `depends_on` to your tool service so it waits for `bpf-init` to become healthy before starting:

```yaml
your-tool:
  depends_on:
    bpf-init:
      condition: service_healthy
    envoy-z2:
      condition: service_started
```

If your service is in Zone 3, use `envoy-z3` instead:

```yaml
your-tool:
  depends_on:
    bpf-init:
      condition: service_healthy
    envoy-z3:
      condition: service_started
```

---

## Step 4: Disable IPv6

Add the sysctl entry to your tool service:

```yaml
your-tool:
  sysctls:
    net.ipv6.conf.all.disable_ipv6: 1
```

---

## Step 5: Add Security Options

Add `no-new-privileges` to your tool service:

```yaml
your-tool:
  security_opt:
    - no-new-privileges:true
```

---

## Complete Example

A full service definition for a Zone 2 tool container with all required entries:

```yaml
x-bpf-init-capabilities: &bpf-init-capabilities
  cap_add:
    - CAP_BPF
    - CAP_NET_ADMIN
    - CAP_SYS_ADMIN
  security_opt:
    - no-new-privileges:true
  volumes:
    - /sys/fs/bpf:/sys/fs/bpf
    - /sys/fs/cgroup:/sys/fs/cgroup:rw
    - bpf-objects:/opt/ebpf

services:

  bpf-init:
    image: bpf-builder:latest
    <<: *bpf-init-capabilities
    command: >
      sh -c "cp /build/connect4.bpf.o /opt/ebpf/connect4.bpf.o &&
             cp /build/sockops.bpf.o /opt/ebpf/sockops.bpf.o &&
             cp /build/getsockopt.bpf.o /opt/ebpf/getsockopt.bpf.o &&
             cp /usr/local/bin/bpftool /opt/ebpf/bpftool &&
             chmod +x /opt/ebpf/bpftool &&
             echo 'BPF artifacts ready' && sleep infinity"
    networks:
      - zone2-active
    healthcheck:
      test: ["CMD-SHELL", "test -f /opt/ebpf/connect4.bpf.o && test -f /opt/ebpf/sockops.bpf.o && test -f /opt/ebpf/getsockopt.bpf.o"]
      interval: 2s
      timeout: 2s
      retries: 5
      start_period: 2s

  your-tool:
    build:
      context: ./your-tool
      dockerfile: Dockerfile
    image: rainbow-your-tool:latest
    volumes:
      - bpf-objects:/opt/ebpf:ro
      - /sys/fs/bpf:/sys/fs/bpf:ro
    networks:
      - zone2-active
    environment:
      # NOTE: No HTTP_PROXY/HTTPS_PROXY needed. The unified BPF architecture
      # intercepts ALL outbound TCP (including HTTP) via connect4 and routes
      # through Envoy's transparent_tcp listener on port 15001.
      PATH: "/opt/ebpf:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
    sysctls:
      net.ipv6.conf.all.disable_ipv6: 1
    security_opt:
      - no-new-privileges:true
    depends_on:
      bpf-init:
        condition: service_healthy
      envoy-z2:
        condition: service_started

  envoy-z2:
    image: envoyproxy/envoy:v1.31-latest
    volumes:
      - ../../../../skills/rainbow/config/envoy/envoy-zone2-active.yaml:/etc/envoy/envoy.yaml:ro
    networks:
      - zone2-active
      - zone2-egress
    security_opt:
      - no-new-privileges:true
    healthcheck:
      test: ["CMD-SHELL", "bash -c '</dev/tcp/localhost/3128' || exit 1"]
      interval: 5s
      timeout: 3s
      retries: 5

networks:
  zone2-active:
    driver: bridge
    internal: true
  zone2-egress:
    driver: bridge

volumes:
  bpf-objects:
```

---

## Verification

After `docker compose up -d`, verify all three BPF programs are attached to your tool container's cgroup. Find the container's cgroup path, then check its `jerry-intercept` child:

```bash
# Find the container cgroup (hostname prefix matches container ID)
CGROUP=$(docker compose exec your-tool sh -c \
  'find /sys/fs/cgroup/docker -maxdepth 1 -name "$(hostname)*" -type d | head -1')
docker compose exec your-tool bpftool cgroup show "${CGROUP}/jerry-intercept"
```

Expected output lists all three programs:

```
ID       AttachType      AttachFlags     Name
...      connect4                        connect4_redirect
...      sock_ops                        sockops_port_cookie
...      getsockopt                      getsockopt_orig_dst
```

Verify the destination lookup map is accessible:

```bash
docker compose exec your-tool bpftool map dump pinned /sys/fs/bpf/rainbow_maps/dst_lookup
```

Expected: exits 0 (map exists and is readable, even if empty before any connections are made).

---

## Troubleshooting

**Problem:** `bpftool cgroup show` returns no programs or an empty list.

**Solution:** `bpf-init` finished before BpfManager attached the programs to the container's cgroup. Restart the tool container after confirming `bpf-init` is healthy: `docker compose restart your-tool`.

---

**Problem:** `bpftool map dump` returns `Permission denied`.

**Solution:** The `/sys/fs/bpf` volume mount is missing or was added without `:ro`. Verify the mount entry in your service definition matches Step 2 exactly.

---

**Problem:** Connections from the tool container time out instead of reaching Envoy.

**Solution:** Envoy is not running or the `transparent_tcp` listener on port 15001 is not configured. Check `docker compose ps` to confirm `envoy-z2` (or `envoy-z3`) is up, then verify the Envoy config includes a `transparent_tcp` listener. See [eBPF Transparent Proxy Reference](../reference/ebpf-transparent-proxy.md) for listener configuration requirements.

---

**Problem:** `bpf-init` stays in `starting` state and never becomes healthy.

**Solution:** The `bpf-builder:latest` image is not present. Run `docker images bpf-builder` to confirm. Build it from `src/proxy_infra/infrastructure/bpf/Dockerfile.bpf-builder` if missing.

---

## Related

- **Reference:** [eBPF Transparent Proxy Reference](../reference/ebpf-transparent-proxy.md) -- map schemas, program specifications, capability requirements
- **Explanation:** [About eBPF Transparent Proxy Architecture](../research/ebpf-architecture-decision.md) -- design decisions and architectural context
