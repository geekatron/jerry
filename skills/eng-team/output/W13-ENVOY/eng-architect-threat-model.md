# STRIDE Threat Model: Envoy Forward Proxy Network Isolation Architecture

> **Engagement:** W13-ENVOY
> **Date:** 2026-03-18
> **Agent:** eng-architect
> **Criticality:** C3 (AE-005 security architecture)
> **Methodology:** STRIDE + DREAD scoring + Attack Trees (top 3) + LINDDUN (PII assessment)
> **Architecture Under Analysis:** ADR-PROJ023-003 v2 -- Option D (Envoy Forward Proxy with Deny-by-Default Egress)
> **NIST CSF 2.0 Mapping:** Identify (ID.AM, ID.RA), Protect (PR.AC, PR.DS, PR.IP), Detect (DE.CM, DE.AE)
> **SSDF Mapping:** PO.1 (security requirements), PO.2 (roles), PO.5 (secure environments)

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Key threats, risk posture, business impact |
| [L1: Trust Boundary Inventory](#l1-trust-boundary-inventory) | Six trust boundaries with data flow descriptions |
| [L1: STRIDE Analysis by Trust Boundary](#l1-stride-analysis-by-trust-boundary) | Per-boundary STRIDE with DREAD scoring |
| [L1: Consolidated Threat Register](#l1-consolidated-threat-register) | All threats ranked by DREAD composite score |
| [L1: Attack Trees (Top 3 Threats)](#l1-attack-trees-top-3-threats) | Chained attack path analysis |
| [L1: LINDDUN Privacy Assessment](#l1-linddun-privacy-assessment) | PII flow through engagement scope |
| [L1: Mitigation Recommendations](#l1-mitigation-recommendations) | Mapped to FEAT-W13 tasks T13-001 through T13-023 |
| [L2: Strategic Implications](#l2-strategic-implications) | Long-term security posture, three-zone evolution |
| [Traceability](#traceability) | Source references |

---

## L0: Executive Summary

### Architecture Overview

The Envoy forward proxy architecture introduces a three-layer defense-in-depth model for the Rainbow Series tool execution framework. Tool containers operate on Docker networks declared `internal: true`, which structurally prevents direct internet access. An Envoy proxy container bridges each internal network to the external internet, enforcing per-zone egress allowlists. The CLI layer provides engagement scope validation, approval gates, and credential filtering as the application-level business logic layer.

### Top 5 Threats by Risk

| Rank | Threat ID | Title | DREAD Score | Trust Boundary |
|------|-----------|-------|-------------|----------------|
| 1 | T-TB2-04 | DNS tunneling bypasses Envoy HTTP proxy | 32 | TB-2 (Tool to Envoy) |
| 2 | T-TB4-01 | Malicious engagement scope generates permissive Envoy config | 30 | TB-4 (Scope to Config Generator) |
| 3 | T-TB2-03 | Raw TCP exfiltration bypasses HTTP_PROXY | 28 | TB-2 (Tool to Envoy) |
| 4 | T-TB6-01 | docker-compose.yml tampered to remove Envoy or change networks | 27 | TB-6 (Compose to Envoy) |
| 5 | T-TB3-02 | Envoy config hot-reload injects unauthorized routes | 25 | TB-3 (Envoy to External) |

### Security Posture Assessment

The Envoy forward proxy architecture achieves a **strong security posture** for HTTP/HTTPS traffic. The `internal: true` network topology provides structural isolation that cannot be bypassed by application-level attacks. The primary residual risks concentrate around two areas:

1. **Non-HTTP protocol bypass** (DNS tunneling, raw TCP). Tools like Impacket and pwntools make raw TCP connections that do not traverse the HTTP proxy. The ADR acknowledges this and proposes iptables REDIRECT within the compose network for transparent proxying. This mitigation is essential and must be implemented as a hard dependency, not a deferred enhancement.

2. **Scope-to-config translation integrity**. The engagement scope YAML is the single policy document that determines what Envoy allows. A flawed or malicious scope document becomes an overly permissive Envoy configuration. The translation pipeline is a critical trust boundary.

### Business Risk Impact

If the identified threats are not mitigated, the framework risks:
- **Unauthorized network access from tool containers** -- a compromised or misbehaving tool reaching targets outside the authorized engagement scope, creating legal liability.
- **Evidence chain contamination** -- unlogged network connections bypassing the Envoy access log, undermining forensic integrity.
- **Scope violation** -- tools accessing resources not authorized by the engagement operator, violating the rules of engagement.

---

## L1: Trust Boundary Inventory

Six trust boundaries identified in the Envoy forward proxy architecture. Each boundary represents a transition between components operating at different privilege levels or with different trust assumptions.

### TB-1: Tool Container to Internal Docker Network

| Attribute | Value |
|-----------|-------|
| **Components** | Tool container (e.g., recon-pipeline, exploit-ops) and Docker internal network |
| **Data Flow** | Tool container generates network traffic (TCP, UDP, DNS, HTTP/HTTPS) |
| **Trust Transition** | Container process (untrusted -- may be compromised binary) to network namespace (infrastructure-controlled) |
| **Zone Applicability** | All zones with networking (Zone 1 update, Zone 2, Zone 3) |
| **Key Question** | Can a tool container escape the internal network and reach the internet directly? |

### TB-2: Tool Container to Envoy Proxy

| Attribute | Value |
|-----------|-------|
| **Components** | Tool container egress traffic and Envoy proxy listener |
| **Data Flow** | HTTP/HTTPS via HTTP_PROXY env var; CONNECT method for TLS tunneling |
| **Trust Transition** | Untrusted tool traffic to policy enforcement point (Envoy) |
| **Zone Applicability** | Zone 1 update, Zone 2, Zone 3 |
| **Key Question** | Can a tool bypass the proxy via DNS tunneling, raw TCP, CONNECT method abuse, or protocol-level tricks? |

### TB-3: Envoy Proxy to External Network

| Attribute | Value |
|-----------|-------|
| **Components** | Envoy proxy egress interface and the public internet |
| **Data Flow** | Proxied HTTP/HTTPS connections to allowlisted destinations |
| **Trust Transition** | Policy enforcement point (Envoy -- trusted) to external network (untrusted) |
| **Zone Applicability** | Zone 1 update, Zone 2, Zone 3 |
| **Key Question** | Can Envoy be manipulated to forward traffic to unauthorized destinations? |

### TB-4: Engagement Scope YAML to Envoy Config Generator

| Attribute | Value |
|-----------|-------|
| **Components** | Engagement scope document (`SCOPE.yaml`) and `scope_translator.py` |
| **Data Flow** | YAML fields (authorized_targets, excluded_targets) parsed and translated to Envoy virtual_host routes |
| **Trust Transition** | Operator-authored document (semi-trusted) to machine-generated proxy configuration (trusted as policy) |
| **Zone Applicability** | Zone 2, Zone 3 |
| **Key Question** | Can a malicious or malformed scope document produce an overly permissive Envoy config? |

### TB-5: CLI to Envoy Config Lifecycle

| Attribute | Value |
|-----------|-------|
| **Components** | CLI handler (`tool_exec_commands.py`) and Envoy configuration files |
| **Data Flow** | CLI invokes `--init-engagement` which triggers scope translation; CLI invokes `docker compose exec` which uses the running Envoy config |
| **Trust Transition** | Application logic (CLI) trusting that the Envoy config matches the current engagement scope |
| **Zone Applicability** | Zone 2, Zone 3 |
| **Key Question** | What if the Envoy config is stale (from a prior engagement) when the CLI invokes a tool? |

### TB-6: Docker Compose to Envoy

| Attribute | Value |
|-----------|-------|
| **Components** | `docker-compose.yml` files and the Envoy service definition |
| **Data Flow** | Compose file declares network topology, Envoy service, and environment variables |
| **Trust Transition** | Configuration-as-code (file on disk, editable by any developer) to running infrastructure |
| **Zone Applicability** | All zones |
| **Key Question** | What if docker-compose.yml is modified to remove Envoy, change `internal: true` to `internal: false`, or remove HTTP_PROXY vars? |

---

## L1: STRIDE Analysis by Trust Boundary

### TB-1: Tool Container to Internal Docker Network

#### S -- Spoofing

| ID | Threat | DREAD | Score |
|----|--------|-------|-------|
| T-TB1-S01 | A tool container spoofs its network identity (MAC/IP) to appear as the Envoy proxy container, intercepting traffic from other containers on the same internal network. | D:4 R:6 E:3 A:4 D:5 | 22 |

**Analysis:** Docker's internal bridge networking assigns IPs via DHCP from the bridge subnet. Container MAC and IP can be overridden with `--mac-address` and `--ip` in compose, but not at runtime by the container process without `NET_ADMIN` capability. With `no-new-privileges:true` and no `NET_ADMIN` cap, ARP spoofing from within the container is blocked at the kernel level.

**DREAD Breakdown:** Damage=4 (could intercept other containers' traffic, not full compromise). Reproducibility=6 (requires NET_ADMIN absence to be enforced; reliable if so). Exploitability=3 (requires kernel-level capability the container does not have). Affected Users=4 (other containers on same internal network). Discoverability=5 (well-known Docker networking behavior).

#### T -- Tampering

| ID | Threat | DREAD | Score |
|----|--------|-------|-------|
| T-TB1-T01 | A compromised tool container modifies the shared `/work` volume to inject malicious content that influences other containers or the host. | D:6 R:8 E:7 A:5 D:4 | 30 |

**Analysis:** All tool containers mount `../../../../work:/work`. A compromised binary can write arbitrary data to this shared volume. Other containers reading from the same volume (e.g., one tool's output used as another tool's input) trust this data. The host filesystem is also directly affected since the volume is a bind mount.

**DREAD Breakdown:** Damage=6 (cross-container poisoning via shared filesystem; evidence integrity compromised). Reproducibility=8 (trivial -- write to /work from any container). Exploitability=7 (any write operation to the bind mount). Affected Users=5 (all containers sharing the volume + host). Discoverability=4 (requires knowledge of the bind mount path).

**Note:** This is a pre-existing threat not introduced by the Envoy architecture but worth cataloging because the Envoy network isolation does not protect against filesystem-based lateral movement.

#### R -- Repudiation

| ID | Threat | DREAD | Score |
|----|--------|-------|-------|
| T-TB1-R01 | A tool container makes network connections that are not logged because they occur within the internal Docker network (container-to-container), bypassing Envoy's access log. | D:4 R:7 E:6 A:3 D:4 | 24 |

**Analysis:** Envoy only logs traffic that transits through it. Container-to-container communication on the same internal Docker network (e.g., exploit-msf connecting to postgres) is direct and not proxied. This traffic has no audit trail in Envoy's access log.

**DREAD Breakdown:** Damage=4 (audit gap for lateral movement within cluster). Reproducibility=7 (any container-to-container communication on the same internal network). Exploitability=6 (standard network communication). Affected Users=3 (containers within same compose cluster). Discoverability=4 (requires knowledge of internal network topology).

#### I -- Information Disclosure

| ID | Threat | DREAD | Score |
|----|--------|-------|-------|
| T-TB1-I01 | A tool container enumerates the internal Docker network to discover other containers, the Envoy proxy IP, and the network gateway, revealing infrastructure topology. | D:3 R:8 E:8 A:3 D:6 | 28 |

**Analysis:** Basic network reconnaissance (`ip addr`, `arp -a`, DNS queries for container names) reveals the internal topology. Docker's embedded DNS resolves service names to container IPs. This is informational but aids more sophisticated attacks.

**DREAD Breakdown:** Damage=3 (information only; enables follow-on attacks). Reproducibility=8 (trivial from any container with basic tools). Exploitability=8 (standard network utilities). Affected Users=3 (infrastructure knowledge gained). Discoverability=6 (well-known Docker behavior).

#### D -- Denial of Service

| ID | Threat | DREAD | Score |
|----|--------|-------|-------|
| T-TB1-D01 | A tool container floods the internal Docker network or the Envoy proxy with traffic, causing denial of service for other containers in the same compose cluster. | D:4 R:7 E:7 A:4 D:5 | 27 |

**Analysis:** No rate limiting exists at the Docker network level between containers. A single misbehaving container can saturate the internal bridge bandwidth or exhaust Envoy's connection pool, starving other containers of proxy capacity.

**DREAD Breakdown:** Damage=4 (cluster-level DoS; does not affect host or other clusters). Reproducibility=7 (high-volume traffic generation is trivial). Exploitability=7 (no special capabilities required). Affected Users=4 (all containers in same cluster). Discoverability=5 (obvious behavior pattern).

#### E -- Elevation of Privilege

| ID | Threat | DREAD | Score |
|----|--------|-------|-------|
| T-TB1-E01 | A tool container exploits a Docker engine vulnerability to escape the container namespace and gain host access, bypassing all network isolation. | D:10 R:2 E:2 A:10 D:3 | 27 |

**Analysis:** Container escape is the nuclear option. If achieved, all three layers (Docker network, Envoy proxy, CLI logic) are bypassed because the attacker operates at the host level. `no-new-privileges:true` and `seccomp` profiles reduce the attack surface. The `frida` container currently has `cap_add: SYS_PTRACE` and `seccomp:unconfined`, which significantly increases this risk for that specific container.

**DREAD Breakdown:** Damage=10 (full host compromise). Reproducibility=2 (requires 0-day or known unpatched CVE). Exploitability=2 (requires deep kernel/container runtime knowledge). Affected Users=10 (entire host and all clusters). Discoverability=3 (publicly disclosed CVEs are discoverable; 0-days are not).

---

### TB-2: Tool Container to Envoy Proxy

#### S -- Spoofing

| ID | Threat | DREAD | Score |
|----|--------|-------|-------|
| T-TB2-S01 | A tool container spoofs HTTP headers (e.g., `Host`, `:authority`) to trick Envoy into routing traffic to an unauthorized destination that matches the allowlist pattern. | D:6 R:6 E:5 A:5 D:5 | 27 |

**Analysis:** Envoy's allowlist matching uses the `:authority` header (or `Host` header) to determine whether a destination is permitted. If the regex is imprecise (e.g., matching `github.com` but also `evil-github.com` due to missing anchor), a tool can craft requests to unauthorized destinations. The ADR's Zone 1 config uses anchored regex (`^(github\\.com|...)$`), which mitigates this for static allowlists. Zone 2/3 dynamic configs generated from scope YAML need the same rigor.

**DREAD Breakdown:** Damage=6 (unauthorized egress to attacker-controlled host). Reproducibility=6 (requires regex weakness in generated config). Exploitability=5 (header crafting is straightforward). Affected Users=5 (engagement scope violated). Discoverability=5 (regex testing reveals weaknesses).

#### T -- Tampering

| ID | Threat | DREAD | Score |
|----|--------|-------|-------|
| T-TB2-T01 | A tool container tampers with the HTTP_PROXY environment variable to point at a different proxy or directly at an external host, bypassing Envoy. | D:3 R:3 E:4 A:3 D:4 | 17 |

**Analysis:** The `internal: true` network topology prevents this from succeeding. Even if the tool modifies its own `HTTP_PROXY` env var to point at an external IP, the internal Docker network has no route to the external network. The traffic will fail to connect. This is the core value of the `internal: true` design. The only reachable hosts are those on the same internal network -- and the only host with an external route is Envoy.

**DREAD Breakdown:** Damage=3 (attempt fails due to network topology). Reproducibility=3 (env var modification is trivial but effect is null). Exploitability=4 (trivial to attempt). Affected Users=3 (only the attacking container is affected). Discoverability=4 (well-known technique).

**Residual risk:** If `internal: true` is ever removed from the Docker network declaration, this threat becomes critical. This is why TB-6 (Compose file tampering) is a high-priority trust boundary.

#### T -- Tampering (Protocol)

| ID | Threat | DREAD | Score |
|----|--------|-------|-------|
| T-TB2-T02 | A tool container sends a malformed HTTP CONNECT request that exploits an Envoy parsing vulnerability, causing Envoy to forward traffic to an unintended destination. | D:7 R:3 E:3 A:5 D:4 | 22 |

**Analysis:** Envoy's HTTP CONNECT implementation is mature and extensively fuzzed. However, forward proxy CONNECT handling (where Envoy tunnels arbitrary TCP via CONNECT method) is a complex code path. A vulnerability in CONNECT parsing could allow destination manipulation.

**DREAD Breakdown:** Damage=7 (arbitrary egress via compromised proxy). Reproducibility=3 (requires specific Envoy version vulnerability). Exploitability=3 (requires protocol-level exploitation expertise). Affected Users=5 (all traffic through that Envoy instance). Discoverability=4 (Envoy CVEs are publicly tracked).

#### R -- Repudiation

| ID | Threat | DREAD | Score |
|----|--------|-------|-------|
| T-TB2-R01 | A tool container uses the CONNECT method to tunnel opaque TCP traffic through Envoy, making the proxied content invisible to Envoy's access log beyond the destination host:port. | D:4 R:8 E:7 A:4 D:5 | 28 |

**Analysis:** When Envoy handles CONNECT requests, it sees the destination host:port but not the payload (which is opaque TCP after the CONNECT handshake). For HTTPS traffic this is expected (TLS encrypted). For Zone 3 with MITM capability, Envoy can terminate TLS and inspect content. Without MITM, the access log records the connection metadata but not the data transferred.

**DREAD Breakdown:** Damage=4 (reduced audit granularity, not full bypass). Reproducibility=8 (standard CONNECT behavior). Exploitability=7 (standard HTTPS). Affected Users=4 (forensic evidence quality degraded). Discoverability=5 (well-understood proxy behavior).

#### I -- Information Disclosure

| ID | Threat | DREAD | Score |
|----|--------|-------|-------|
| T-TB2-I01 | Envoy access logs capture sensitive data in URL paths, query parameters, or HTTP headers that transits through the proxy. | D:5 R:7 E:8 A:4 D:4 | 28 |

**Analysis:** Envoy's JSON access log format in the ADR logs `%REQ(:METHOD)%`, `%REQ(X-ENVOY-ORIGINAL-PATH?:PATH)%`, and `%UPSTREAM_HOST%`. URL paths and query strings may contain API keys, tokens, or sensitive target information. This is a design tension: logging is needed for forensic evidence, but the logs themselves become sensitive artifacts.

**DREAD Breakdown:** Damage=5 (credential/sensitive data exposure in log files). Reproducibility=7 (any HTTP request with sensitive URL parameters). Exploitability=8 (no special effort; normal tool operation). Affected Users=4 (engagement evidence integrity). Discoverability=4 (requires access to Envoy log volume).

#### I -- Information Disclosure (DNS)

| ID | Threat | DREAD | Score |
|----|--------|-------|-------|
| T-TB2-04 | **DNS tunneling bypasses Envoy HTTP proxy.** A compromised tool encodes exfiltration data in DNS queries. Docker's embedded DNS resolver forwards these queries to the host's DNS resolver, which resolves them on the public internet. DNS traffic does not traverse the HTTP proxy. | D:8 R:7 E:5 A:6 D:6 | **32** |

**Analysis:** This is the **highest-risk threat** in the model. The `internal: true` Docker network blocks direct TCP/UDP egress to external IPs, but Docker's embedded DNS resolver (at 127.0.0.11) provides DNS resolution for all containers. A tool can make DNS queries to attacker-controlled domains (e.g., `data.evil.com`) that encode exfiltrated data in the subdomain labels. These DNS queries are resolved by Docker's DNS, which forwards to the host's upstream resolver, which resolves on the public internet. The Envoy proxy never sees this traffic.

**DREAD Breakdown:** Damage=8 (data exfiltration channel that bypasses all proxy controls). Reproducibility=7 (DNS resolution works from any container on internal network). Exploitability=5 (requires DNS tunneling tooling like `dnscat2` or custom scripts). Affected Users=6 (any container with DNS access). Discoverability=6 (DNS tunneling is a well-documented technique in offensive security literature).

**Mitigation priority:** CRITICAL. Without DNS egress control, the `internal: true` + Envoy architecture has a structural bypass for any tool capable of DNS-based exfiltration.

#### D -- Denial of Service

| ID | Threat | DREAD | Score |
|----|--------|-------|-------|
| T-TB2-D01 | A tool container exhausts Envoy's connection pool or memory by opening thousands of concurrent connections, causing proxy-level denial of service for all containers in the cluster. | D:4 R:7 E:7 A:4 D:5 | 27 |

**Analysis:** Envoy has configurable circuit breakers and connection limits, but the default configuration in the ADR does not specify these limits. A single tool opening unbounded connections can exhaust Envoy's resources.

**DREAD Breakdown:** Damage=4 (cluster-level proxy DoS). Reproducibility=7 (trivial to generate many connections). Exploitability=7 (no special capability required). Affected Users=4 (all containers sharing the proxy). Discoverability=5 (standard DoS technique).

#### E -- Elevation of Privilege

| ID | Threat | DREAD | Score |
|----|--------|-------|-------|
| T-TB2-03 | **Raw TCP exfiltration bypasses HTTP_PROXY.** Tools like Impacket and pwntools make raw TCP connections that ignore the HTTP_PROXY environment variable. If transparent proxy (iptables REDIRECT) is not implemented, these tools can make direct TCP connections to the Envoy proxy's external-facing interface or exploit the network namespace. | D:7 R:7 E:5 A:5 D:4 | **28** |

**Analysis:** The ADR identifies this gap and proposes iptables REDIRECT within the compose network namespace. However, this is described as a mitigation, not as an implementation requirement. If transparent proxy is not deployed, Zone 3 tools (Impacket, pwntools, Metasploit) operating over raw TCP/SMB/RPC protocols bypass Envoy entirely. The `internal: true` network blocks direct external routing, so the raw TCP connections will fail to reach external hosts directly -- but if the Envoy container has a port exposed or the transparent proxy NAT is misconfigured, the tool could potentially reach external hosts through the Envoy container's network namespace.

**DREAD Breakdown:** Damage=7 (unauthorized egress for Zone 3 exploitation tools). Reproducibility=7 (Impacket always uses raw TCP). Exploitability=5 (transparent proxy misconfiguration or absence). Affected Users=5 (Zone 3 engagement scope violated). Discoverability=4 (requires understanding of proxy architecture).

---

### TB-3: Envoy Proxy to External Network

#### S -- Spoofing

| ID | Threat | DREAD | Score |
|----|--------|-------|-------|
| T-TB3-S01 | An external attacker spoofs DNS responses to redirect Envoy's upstream connections to a malicious host, causing tools to interact with attacker-controlled infrastructure instead of legitimate targets. | D:6 R:5 E:4 A:5 D:4 | 24 |

**Analysis:** Envoy uses `LOGICAL_DNS` cluster type, which resolves hostnames at connection time. If the DNS resolver used by Envoy is susceptible to cache poisoning or if upstream DNS is not secured with DNSSEC/DoH, an attacker could redirect connections.

**DREAD Breakdown:** Damage=6 (tool interacts with attacker infrastructure; potential credential theft). Reproducibility=5 (requires DNS poisoning capability). Exploitability=4 (DNS attacks are well-understood but require positioning). Affected Users=5 (all connections through poisoned resolution). Discoverability=4 (DNS poisoning detection is non-trivial).

#### T -- Tampering

| ID | Threat | DREAD | Score |
|----|--------|-------|-------|
| T-TB3-T01 | Envoy's TLS configuration is weakened (outdated cipher suites, disabled certificate verification), allowing man-in-the-middle attacks between Envoy and upstream destinations. | D:6 R:4 E:4 A:5 D:5 | 24 |

**Analysis:** Envoy's default TLS settings are secure, but the generated Envoy config from scope_translator.py must not weaken them. Zone 3 MITM capability intentionally terminates TLS for credential scrubbing -- this creates a configuration where Envoy holds generated TLS certificates, increasing the certificate management attack surface.

**DREAD Breakdown:** Damage=6 (MITM on proxied connections). Reproducibility=4 (requires config weakness). Exploitability=4 (MITM positioning is non-trivial externally). Affected Users=5 (all TLS connections through that Envoy). Discoverability=5 (TLS configuration is auditable).

#### T -- Tampering (Config Reload)

| ID | Threat | DREAD | Score |
|----|--------|-------|-------|
| T-TB3-02 | **Envoy config hot-reload injects unauthorized routes.** If Envoy is configured for dynamic config (xDS, or file-based hot reload via inotify), a compromised tool that has write access to the Envoy config volume can modify the allowlist at runtime, adding attacker-controlled destinations. | D:8 R:5 E:5 A:5 D:2 | **25** |

**Analysis:** The ADR mounts Envoy config as `:ro` (read-only), which prevents tool containers from modifying the config file. However, Envoy supports file-based config reload via inotify on the config file. If the `:ro` mount flag is accidentally omitted, or if Envoy is configured with xDS (dynamic configuration), a tool with `/work` volume access could potentially write to the Envoy config path if the mount paths overlap.

**DREAD Breakdown:** Damage=8 (arbitrary egress via allowlist manipulation). Reproducibility=5 (requires writable config volume or xDS access). Exploitability=5 (config file format is documented). Affected Users=5 (all containers using the proxy). Discoverability=2 (hot reload behavior is not obvious to attackers without infrastructure knowledge).

#### R -- Repudiation

| ID | Threat | DREAD | Score |
|----|--------|-------|-------|
| T-TB3-R01 | Envoy access logs on the `envoy-z*-logs` volume are tampered with by a container that has write access to the volume, destroying forensic evidence. | D:6 R:4 E:4 A:5 D:3 | 22 |

**Analysis:** The Envoy log volume is declared as a named Docker volume, not a bind mount. Tool containers do not mount this volume. However, if a container escape occurs (T-TB1-E01), the attacker could access the volume from the host. The log volume should be treated as a forensic artifact with integrity protection.

**DREAD Breakdown:** Damage=6 (evidence destruction undermines engagement reporting). Reproducibility=4 (requires volume access). Exploitability=4 (requires container escape or volume misconfiguration). Affected Users=5 (engagement forensic integrity). Discoverability=3 (requires infrastructure knowledge).

#### I -- Information Disclosure

| ID | Threat | DREAD | Score |
|----|--------|-------|-------|
| T-TB3-I01 | Envoy's error responses to denied requests leak internal network topology information (container names, internal IPs, Envoy version) to tool containers. | D:3 R:7 E:8 A:3 D:5 | 26 |

**Analysis:** The ADR's deny response returns `"DENIED: destination not in zone1-update allowlist"`. This is informational but could be more verbose in Envoy's default error pages, potentially revealing server version, listener configuration, or internal addressing.

**DREAD Breakdown:** Damage=3 (information disclosure only). Reproducibility=7 (trigger by requesting any non-allowlisted host). Exploitability=8 (trivial curl request). Affected Users=3 (attacker gains infrastructure knowledge). Discoverability=5 (Envoy error format is well-documented).

#### D -- Denial of Service

| ID | Threat | DREAD | Score |
|----|--------|-------|-------|
| T-TB3-D01 | External targets rate-limit or block the Envoy proxy's source IP, causing all Zone 2 reconnaissance tools to fail. | D:3 R:6 E:3 A:4 D:6 | 22 |

**Analysis:** All tool containers in a cluster share the Envoy proxy's external IP. If one tool triggers rate limiting on the target, all tools in that cluster are affected. This is a known consequence of the proxy architecture.

**DREAD Breakdown:** Damage=3 (operational inconvenience, not security breach). Reproducibility=6 (common for aggressive scanning). Exploitability=3 (not attacker-controlled). Affected Users=4 (all Zone 2 tools in the cluster). Discoverability=6 (obvious when tools fail).

#### E -- Elevation of Privilege

| ID | Threat | DREAD | Score |
|----|--------|-------|-------|
| T-TB3-E01 | An attacker exploits an Envoy CVE to achieve remote code execution on the Envoy container, gaining control of the proxy and its external network interface. | D:9 R:2 E:2 A:6 D:4 | 23 |

**Analysis:** Envoy is a high-value target because it is the sole container with external network access. An RCE on Envoy gives the attacker: (a) full external network access (bypass all allowlists), (b) ability to intercept all proxied traffic (MITM), (c) access to Envoy logs (evidence tampering). Envoy has a strong security track record but is not immune to CVEs.

**DREAD Breakdown:** Damage=9 (full proxy compromise; gateway to external network). Reproducibility=2 (requires specific CVE). Exploitability=2 (requires RCE chain). Affected Users=6 (all containers and all network traffic). Discoverability=4 (Envoy CVEs are publicly tracked).

---

### TB-4: Engagement Scope YAML to Envoy Config Generator

#### S -- Spoofing

| ID | Threat | DREAD | Score |
|----|--------|-------|-------|
| T-TB4-S01 | A malicious actor creates a fraudulent engagement scope document that bypasses the `rainbow-orchestrator` validation (e.g., by placing the scope file directly on disk without going through the orchestrator). | D:6 R:5 E:5 A:5 D:4 | 25 |

**Analysis:** The engagement scope validation is performed by `rainbow-orchestrator` at runtime. However, the scope-to-Envoy-config translation happens at `--init-engagement` time. If a scope file is placed on disk before the orchestrator validates it, or if the translator reads the file without re-validating, an unauthorized scope document becomes an Envoy config.

**DREAD Breakdown:** Damage=6 (unauthorized targets added to Envoy allowlist). Reproducibility=5 (requires file system access to scope directory). Exploitability=5 (file creation is trivial). Affected Users=5 (engagement scope boundary violated). Discoverability=4 (scope file presence is discoverable).

#### T -- Tampering

| ID | Threat | DREAD | Score |
|----|--------|-------|-------|
| T-TB4-01 | **Malicious engagement scope generates permissive Envoy config.** The scope YAML contains wildcard targets (e.g., `*.com`), CIDR ranges encompassing the entire internet (e.g., `0.0.0.0/0`), or targets that resolve to attacker-controlled infrastructure. The scope-to-Envoy translator generates a permissive allowlist that defeats the deny-by-default posture. | D:8 R:7 E:6 A:6 D:3 | **30** |

**Analysis:** This is the **second-highest-risk threat**. The engagement scope template says "No wildcards without explicit operator justification" but enforcement of this constraint in `scope_translator.py` is not yet implemented. The translator must reject:
- Wildcard domain patterns broader than necessary (e.g., `*.com`, `*.*`)
- CIDR ranges broader than /16 without explicit justification
- localhost/loopback targets that could be used for SSRF
- Cloud metadata service IPs (169.254.169.254, fd00:ec2::254)

**DREAD Breakdown:** Damage=8 (effectively removes network isolation for the engagement). Reproducibility=7 (scope file creation is straightforward). Exploitability=6 (requires understanding of Envoy config generation). Affected Users=6 (all containers in the engagement). Discoverability=3 (overly permissive config may not be immediately obvious).

#### R -- Repudiation

| ID | Threat | DREAD | Score |
|----|--------|-------|-------|
| T-TB4-R01 | The scope-to-Envoy translation does not log the translation mapping, making it impossible to audit which scope entries produced which Envoy routes. | D:4 R:6 E:8 A:4 D:3 | 25 |

**Analysis:** If the translation process is opaque, an auditor cannot verify that the running Envoy config accurately reflects the approved scope document. The translation should produce a deterministic, logged mapping.

**DREAD Breakdown:** Damage=4 (audit trail gap). Reproducibility=6 (every translation has this gap if logging is absent). Exploitability=8 (not an exploit; an architectural omission). Affected Users=4 (engagement auditors). Discoverability=3 (requires audit process awareness).

#### I -- Information Disclosure

| ID | Threat | DREAD | Score |
|----|--------|-------|-------|
| T-TB4-I01 | The generated Envoy config contains authorized target information from the scope document, exposing engagement targets to anyone with access to the Envoy config file or the Envoy admin interface. | D:4 R:8 E:8 A:3 D:4 | 27 |

**Analysis:** The Envoy config file contains the domain/IP allowlist derived from the engagement scope. This is sensitive information -- it reveals which targets are being tested. The config is mounted as a bind mount in the compose file, readable by anyone with host filesystem access. Envoy's admin interface (if enabled) also exposes the route configuration.

**DREAD Breakdown:** Damage=4 (engagement target exposure). Reproducibility=8 (config file is always present). Exploitability=8 (file read is trivial). Affected Users=3 (engagement confidentiality). Discoverability=4 (known file location).

#### D -- Denial of Service

| ID | Threat | DREAD | Score |
|----|--------|-------|-------|
| T-TB4-D01 | A scope document with thousands of targets produces an Envoy config that exceeds Envoy's route table capacity, causing Envoy to fail to start or to degrade in performance. | D:3 R:4 E:6 A:4 D:3 | 20 |

**Analysis:** Envoy can handle large route tables, but an adversarial scope document with thousands of entries could cause memory pressure or slow route matching. The translator should impose a reasonable limit.

**DREAD Breakdown:** Damage=3 (proxy startup failure; operational issue). Reproducibility=4 (requires very large scope document). Exploitability=6 (trivial to create large YAML). Affected Users=4 (entire cluster cannot start). Discoverability=3 (failure is obvious at startup).

#### E -- Elevation of Privilege

| ID | Threat | DREAD | Score |
|----|--------|-------|-------|
| T-TB4-E01 | YAML deserialization vulnerability in `scope_translator.py` allows code execution when parsing a crafted scope document. | D:8 R:3 E:4 A:6 D:3 | 24 |

**Analysis:** Python's `yaml.safe_load()` prevents arbitrary object instantiation. If `yaml.load()` (unsafe) is used instead, a crafted YAML document can execute arbitrary Python code. This must be enforced in the translator implementation.

**DREAD Breakdown:** Damage=8 (code execution in the CLI process). Reproducibility=3 (requires unsafe YAML loader). Exploitability=4 (well-documented YAML deserialization attacks). Affected Users=6 (CLI process compromise). Discoverability=3 (code review reveals loader choice).

---

### TB-5: CLI to Envoy Config Lifecycle

#### S -- Spoofing

| ID | Threat | DREAD | Score |
|----|--------|-------|-------|
| T-TB5-S01 | The CLI trusts that the Envoy config on disk matches the current engagement scope without re-verifying. A stale Envoy config from a prior engagement is used for the current engagement, allowing access to the prior engagement's targets. | D:6 R:6 E:7 A:5 D:3 | 27 |

**Analysis:** If the operator runs `--init-engagement` for engagement A, then starts engagement B without re-running init, the Envoy config still permits engagement A's targets. The CLI must verify config freshness at tool invocation time.

**DREAD Breakdown:** Damage=6 (cross-engagement target access). Reproducibility=6 (common operator workflow error). Exploitability=7 (no special effort; just forget to re-init). Affected Users=5 (engagement B's scope violated). Discoverability=3 (config staleness is not visible to the operator).

#### T -- Tampering

| ID | Threat | DREAD | Score |
|----|--------|-------|-------|
| T-TB5-T01 | An operator or automated process modifies the Envoy config file on disk after `--init-engagement` but before tool execution, adding unauthorized targets. | D:6 R:5 E:6 A:5 D:3 | 25 |

**Analysis:** The Envoy config is a file on the host filesystem. Between translation and Envoy loading, the file can be modified. The `:ro` mount prevents modification from within the Envoy container, but the host-side file is writable.

**DREAD Breakdown:** Damage=6 (unauthorized target access). Reproducibility=5 (requires host filesystem access). Exploitability=6 (file editing is trivial). Affected Users=5 (engagement scope violated). Discoverability=3 (file modification may not be detected).

#### R -- Repudiation

| ID | Threat | DREAD | Score |
|----|--------|-------|-------|
| T-TB5-R01 | No audit trail links the CLI's `--init-engagement` invocation to the specific Envoy config file that was generated, making it impossible to prove which config was active during a specific tool execution. | D:5 R:7 E:8 A:4 D:3 | 27 |

**Analysis:** The CLI should log: (a) the scope document hash at init time, (b) the generated Envoy config hash, (c) the Envoy config hash at tool execution time. If these hashes differ, the config was modified between init and execution.

**DREAD Breakdown:** Damage=5 (forensic integrity gap). Reproducibility=7 (every engagement has this gap if hashing is absent). Exploitability=8 (not an exploit; an omission). Affected Users=4 (engagement auditors). Discoverability=3 (requires audit awareness).

#### D -- Denial of Service

| ID | Threat | DREAD | Score |
|----|--------|-------|-------|
| T-TB5-D01 | The CLI's `--init-engagement` fails silently, leaving no Envoy config in place. Envoy starts with an empty config or fails to start, blocking all tool execution. | D:3 R:4 E:5 A:4 D:5 | 21 |

**Analysis:** The CLI must verify that the translation succeeded and that Envoy can load the config. A health check endpoint on Envoy should be verified after config deployment.

**DREAD Breakdown:** Damage=3 (operational failure, not security breach). Reproducibility=4 (error conditions are specific). Exploitability=5 (depends on error handling quality). Affected Users=4 (entire engagement blocked). Discoverability=5 (failure is obvious).

---

### TB-6: Docker Compose to Envoy

#### S -- Spoofing

| ID | Threat | DREAD | Score |
|----|--------|-------|-------|
| T-TB6-S01 | A developer creates a parallel docker-compose.override.yml that overrides the network configuration, replacing `internal: true` with a standard bridge network or removing the Envoy service. | D:7 R:5 E:7 A:5 D:3 | 27 |

**Analysis:** Docker Compose automatically merges `docker-compose.override.yml` with `docker-compose.yml`. A developer who finds the proxy inconvenient could create an override file that disables the security controls. This override file might not be committed to version control.

**DREAD Breakdown:** Damage=7 (complete bypass of network isolation). Reproducibility=5 (requires developer action). Exploitability=7 (override files are standard Docker Compose). Affected Users=5 (local development environment exposed). Discoverability=3 (override file may not be visible in git).

#### T -- Tampering

| ID | Threat | DREAD | Score |
|----|--------|-------|-------|
| T-TB6-01 | **docker-compose.yml tampered to remove Envoy or change networks.** A pull request modifies a compose file to: (a) remove the Envoy service, (b) change `internal: true` to `internal: false`, (c) remove HTTP_PROXY environment variables, or (d) add `network_mode: host` to a tool container. | D:8 R:6 E:7 A:6 D:3 | **27** |

**Analysis:** Compose files are configuration-as-code. Any developer with write access to the repository can modify them. A subtle change (removing one line: `internal: true`) completely defeats the network isolation. Code review is the primary defense, but the change may be buried in a large PR.

**DREAD Breakdown:** Damage=8 (complete bypass of network isolation for affected cluster). Reproducibility=6 (requires write access to repo). Exploitability=7 (single-line change). Affected Users=6 (all containers in the affected cluster). Discoverability=3 (subtle change in a YAML file).

#### R -- Repudiation

| ID | Threat | DREAD | Score |
|----|--------|-------|-------|
| T-TB6-R01 | Changes to docker-compose.yml files are not tracked separately from other code changes, making it difficult to identify when network isolation was modified. | D:3 R:6 E:8 A:3 D:3 | 23 |

**Analysis:** Git tracks all file changes, but there is no specific CI check that validates the network isolation properties of compose files. A change that removes `internal: true` would be visible in the PR diff but not automatically flagged.

**DREAD Breakdown:** Damage=3 (audit difficulty, not direct compromise). Reproducibility=6 (every PR could potentially modify compose files). Exploitability=8 (no special effort). Affected Users=3 (code reviewers). Discoverability=3 (requires awareness of which lines are security-critical).

#### E -- Elevation of Privilege

| ID | Threat | DREAD | Score |
|----|--------|-------|-------|
| T-TB6-E01 | A tool container's compose definition is modified to add `privileged: true`, `network_mode: host`, or `cap_add: NET_ADMIN`, granting the container host-level network access that bypasses all Docker network isolation. | D:9 R:4 E:7 A:6 D:3 | 29 |

**Analysis:** `privileged: true` or `network_mode: host` gives a container full host network access. `cap_add: NET_ADMIN` allows the container to modify its own network configuration. The frida container currently has `cap_add: SYS_PTRACE` and `seccomp:unconfined`, which is already elevated. Adding `NET_ADMIN` would be a single-line change.

**DREAD Breakdown:** Damage=9 (full host network bypass). Reproducibility=4 (requires compose file modification). Exploitability=7 (well-known Docker capabilities). Affected Users=6 (entire host network). Discoverability=3 (subtle compose file change).

---

## L1: Consolidated Threat Register

All threats ranked by DREAD composite score (Damage + Reproducibility + Exploitability + Affected Users + Discoverability).

| Rank | ID | Threat Title | DREAD | Boundary | NIST CSF |
|------|-----|-------------|-------|----------|----------|
| 1 | T-TB2-04 | DNS tunneling bypasses Envoy HTTP proxy | 32 | TB-2 | PR.DS, DE.CM |
| 2 | T-TB1-T01 | Shared /work volume cross-container poisoning | 30 | TB-1 | PR.DS, PR.IP |
| 3 | T-TB4-01 | Malicious scope generates permissive Envoy config | 30 | TB-4 | PR.AC, PR.IP |
| 4 | T-TB6-E01 | Compose modified to add privileged/host networking | 29 | TB-6 | PR.AC, PR.IP |
| 5 | T-TB2-03 | Raw TCP exfiltration bypasses HTTP_PROXY | 28 | TB-2 | PR.DS, DE.CM |
| 6 | T-TB2-R01 | CONNECT method opaque tunnel reduces audit | 28 | TB-2 | DE.AE |
| 7 | T-TB2-I01 | Envoy access logs capture sensitive URL data | 28 | TB-2 | PR.DS |
| 8 | T-TB1-I01 | Internal network topology enumeration | 28 | TB-1 | PR.DS |
| 9 | T-TB2-S01 | Host header spoofing bypasses allowlist regex | 27 | TB-2 | PR.AC |
| 10 | T-TB1-D01 | Internal network/proxy flooding DoS | 27 | TB-1 | PR.IP |
| 11 | T-TB1-E01 | Container escape via Docker engine CVE | 27 | TB-1 | PR.AC |
| 12 | T-TB6-01 | Compose file tampered to remove Envoy/change networks | 27 | TB-6 | PR.IP |
| 13 | T-TB6-S01 | docker-compose.override.yml disables isolation | 27 | TB-6 | PR.IP |
| 14 | T-TB4-I01 | Generated Envoy config exposes engagement targets | 27 | TB-4 | PR.DS |
| 15 | T-TB5-S01 | Stale Envoy config from prior engagement | 27 | TB-5 | PR.IP |
| 16 | T-TB5-R01 | No config-to-execution hash audit trail | 27 | TB-5 | DE.AE |
| 17 | T-TB3-I01 | Envoy error responses leak topology info | 26 | TB-3 | PR.DS |
| 18 | T-TB3-02 | Envoy config hot-reload injects unauthorized routes | 25 | TB-3 | PR.AC |
| 19 | T-TB4-S01 | Fraudulent scope bypasses orchestrator validation | 25 | TB-4 | PR.AC |
| 20 | T-TB4-R01 | No scope-to-config translation audit log | 25 | TB-4 | DE.AE |
| 21 | T-TB5-T01 | Host-side Envoy config modification after init | 25 | TB-5 | PR.IP |
| 22 | T-TB3-S01 | DNS poisoning redirects Envoy upstream connections | 24 | TB-3 | PR.DS |
| 23 | T-TB3-T01 | TLS config weakness enables upstream MITM | 24 | TB-3 | PR.DS |
| 24 | T-TB1-R01 | Internal container-to-container traffic unlogged | 24 | TB-1 | DE.CM |
| 25 | T-TB4-E01 | YAML deserialization code execution | 24 | TB-4 | PR.IP |
| 26 | T-TB6-R01 | Compose security changes not flagged in CI | 23 | TB-6 | DE.AE |
| 27 | T-TB3-E01 | Envoy RCE via CVE | 23 | TB-3 | PR.AC |
| 28 | T-TB2-T02 | CONNECT request parsing exploit | 22 | TB-2 | PR.AC |
| 29 | T-TB1-S01 | ARP spoofing on internal network | 22 | TB-1 | PR.AC |
| 30 | T-TB3-R01 | Envoy log volume tampering | 22 | TB-3 | DE.AE |
| 31 | T-TB3-D01 | Target rate-limits shared proxy IP | 22 | TB-3 | PR.IP |
| 32 | T-TB5-D01 | Silent init failure blocks engagement | 21 | TB-5 | PR.IP |
| 33 | T-TB4-D01 | Oversized scope exhausts Envoy route table | 20 | TB-4 | PR.IP |
| 34 | T-TB2-T01 | HTTP_PROXY env var modification (blocked by internal:true) | 17 | TB-2 | PR.AC |

---

## L1: Attack Trees (Top 3 Threats)

### Attack Tree 1: DNS Tunneling Exfiltration (T-TB2-04, DREAD 32)

```
GOAL: Exfiltrate data from tool container bypassing Envoy proxy
|
+-- [AND] Establish DNS tunnel
|   |
|   +-- [1] Gain code execution in tool container
|   |   |
|   |   +-- [1a] Compromised tool binary (supply chain attack on tool image)
|   |   +-- [1b] Malicious Nuclei template with embedded commands
|   |   +-- [1c] Tool-specific RCE (e.g., Metasploit plugin vulnerability)
|   |
|   +-- [2] Encode data in DNS queries
|   |   |
|   |   +-- [2a] Use dnscat2 (pre-installed in exploit containers)
|   |   +-- [2b] Custom DNS exfiltration script (Python one-liner)
|   |   +-- [2c] Abuse legitimate tool DNS resolution (Subfinder resolves attacker domain)
|   |
|   +-- [3] DNS queries reach external resolver
|       |
|       +-- [3a] Docker embedded DNS (127.0.0.11) forwards to host resolver [CURRENT STATE]
|       +-- [3b] Container's /etc/resolv.conf points to host DNS [CURRENT STATE]
|       +-- [3c] Tool directly queries public DNS (8.8.8.8) -- BLOCKED by internal:true
|
+-- [OR] Receive exfiltrated data
    |
    +-- [4a] Attacker-controlled authoritative DNS server decodes queries
    +-- [4b] DNS logging on attacker infrastructure captures subdomain labels
```

**Critical path:** 1a/1b -> 2b -> 3a -> 4a. A compromised tool or malicious template encodes data in DNS queries. Docker's embedded DNS resolver forwards to the host, which resolves on the internet. The attacker's authoritative DNS server receives the encoded data.

**Mitigation chain:**
- Block path 3a: Configure Docker daemon DNS to use an internal DNS resolver that blocks queries to non-allowlisted domains (**T13-005** scope).
- Block path 2: Network policy on the Envoy container to restrict UDP port 53 egress to only the allowlisted DNS resolver (**new task recommendation**).
- Detect path 1: Container image integrity verification at startup (**T13-001** scope).

---

### Attack Tree 2: Malicious Scope-to-Config Translation (T-TB4-01, DREAD 30)

```
GOAL: Generate overly permissive Envoy config from engagement scope
|
+-- [OR] Inject permissive scope document
|   |
|   +-- [1] Operator creates scope with wildcards
|   |   |
|   |   +-- [1a] *.com wildcard in authorized_targets
|   |   +-- [1b] 0.0.0.0/0 CIDR in authorized_targets
|   |   +-- [1c] Cloud metadata IP (169.254.169.254) in authorized_targets
|   |
|   +-- [2] Bypass orchestrator validation
|   |   |
|   |   +-- [2a] Place scope file directly on disk (skip rainbow-orchestrator)
|   |   +-- [2b] Modify scope file after orchestrator validation but before translation
|   |   +-- [2c] YAML injection via target value field (e.g., value: "*.com\n  - type: domain\n    value: attacker.com")
|   |
|   +-- [3] Exploit translator defects
|       |
|       +-- [3a] Regex generation from domain targets omits anchoring
|       +-- [3b] IP-to-CIDR expansion creates broader range than intended
|       +-- [3c] Cloud account mapping generates *.amazonaws.com (all AWS)
|
+-- [AND] Config loaded by Envoy
    |
    +-- [4] Envoy loads generated config at startup or hot-reload
    +-- [5] Tool container traffic to unauthorized destination is allowed
```

**Critical path:** 1a -> 3a -> 4 -> 5. An operator creates a scope with a domain wildcard. The translator fails to anchor the regex. Envoy allows traffic to any domain matching the unanchored pattern.

**Mitigation chain:**
- Block path 1: Input validation in scope_translator.py rejects wildcards broader than `*.specific-domain.tld` (**T13-012** scope).
- Block path 3a: Generated Envoy regex uses `^` and `$` anchors and `\\.` escaped dots (**T13-012** scope).
- Block path 2a: scope_translator.py re-validates the scope document independently of the orchestrator (**T13-014** scope).
- Detect path 5: Envoy access log analysis alerts on connections to destinations not in the scope (**T13-019** scope).

---

### Attack Tree 3: Raw TCP Proxy Bypass (T-TB2-03, DREAD 28)

```
GOAL: Make raw TCP connections from Zone 3 container bypassing Envoy allowlist
|
+-- [AND] Tool uses raw TCP (not HTTP_PROXY)
|   |
|   +-- [1] Tool is a raw TCP tool
|   |   |
|   |   +-- [1a] Impacket (SMB, RPC, LDAP, Kerberos over raw TCP)
|   |   +-- [1b] pwntools (raw socket connections)
|   |   +-- [1c] Metasploit (exploit payloads over raw TCP)
|   |   +-- [1d] Nmap/naabu (port scanning over raw TCP/SYN)
|   |
|   +-- [2] Transparent proxy not deployed
|   |   |
|   |   +-- [2a] iptables REDIRECT not configured in container namespace
|   |   +-- [2b] Transparent proxy feature deferred as "future enhancement"
|   |   +-- [2c] Transparent proxy configured but does not cover all ports
|   |
|   +-- [3] Traffic reaches destination
|       |
|       +-- [3a] internal:true blocks direct external routing [MITIGATED]
|       +-- [3b] Container-level iptables REDIRECT to Envoy transparent port [TARGET STATE]
|       +-- [3c] Tool connects to another container which has external access [PIVOT]
|
+-- [OR] Exfiltrate data over raw TCP
    |
    +-- [4a] Impacket writes extracted credentials to attacker SMB share
    +-- [4b] Reverse shell to attacker-controlled host
    +-- [4c] Custom TCP exfiltration channel
```

**Critical path:** 1a -> 2b -> 3c -> 4a. Impacket uses raw TCP for SMB. If transparent proxy is not deployed, the connection attempts fail on the internal network (3a mitigates direct external access). However, if the attacker can pivot through another container with external access (3c -- e.g., the Envoy container itself via an exploit), the raw TCP traffic reaches the external network.

**Mitigation chain:**
- Block path 2: Implement iptables REDIRECT in container network namespace as a mandatory requirement, not optional (**T13-004** scope -- must be elevated to hard requirement).
- Block path 3c: Envoy container must not expose any ports to the internal network other than the proxy port. Envoy should drop capabilities (`--cap-drop ALL`) (**T13-001** scope).
- Detect: Envoy transparent proxy mode logs all TCP connections including non-HTTP (**T13-019** scope).

---

## L1: LINDDUN Privacy Assessment

### PII Data Flows Through the Proxy Architecture

| PII Category | Data Location | Flow Path | Risk |
|--------------|--------------|-----------|------|
| **Target names/domains** | Engagement scope YAML `authorized_targets` | Scope YAML -> scope_translator.py -> Envoy config file -> Envoy route matching -> Envoy access logs | Medium: Target identity is sensitive business information. Exposure reveals which organizations are being tested. |
| **Target IP addresses** | Engagement scope YAML `authorized_targets` | Same as above | Medium: IP addresses reveal network infrastructure of assessed organizations. |
| **Operator identity** | Engagement scope YAML `operator_approval.approved_by`, `escalation_authority` | Scope YAML -> generated config comments (if included) | Low: Operator names are internal personnel identifiers. |
| **Credential material** | Tool output transiting Envoy (Zone 3 with MITM) | Tool -> Envoy (MITM terminates TLS) -> credential filter -> quarantine | High: Zone 3 MITM enables Envoy to see decrypted traffic that may contain extracted credentials. |
| **DNS query content** | DNS queries from tool containers | Tool -> Docker DNS -> host resolver -> external DNS | Medium: DNS queries reveal target names and reconnaissance activity. |
| **URL paths with parameters** | HTTP requests through Envoy | Tool -> Envoy -> access log -> log volume | Medium: URL paths may contain API keys, tokens, or query parameters with PII. |

### LINDDUN Categories

| Category | Applicable | Assessment |
|----------|-----------|------------|
| **L** -- Linkability | Yes | Envoy access logs link individual tool operations to specific engagement targets and timestamps. An attacker with log access can reconstruct the full engagement timeline. |
| **I** -- Identifiability | Yes | Operator identity in scope documents and log correlation to specific engagement IDs enables identification of who authorized which operations. |
| **N** -- Non-repudiation | Positive (by design) | The architecture intentionally provides non-repudiation via access logs and evidence chain of custody. This is a feature, not a threat, for the engagement use case. |
| **D** -- Detectability | Yes | The presence of Envoy proxy containers, specific Docker network names (zone2-active, zone3-exploit), and access log volumes makes the framework's existence and purpose detectable on the host. |
| **D** -- Disclosure (unintended) | Yes | Envoy access logs, generated Envoy configs, and engagement scope documents all contain target information that could be disclosed if the host is compromised. |
| **U** -- Unawareness | Low | Operators explicitly create and approve scope documents. Target organizations may not be aware they are being assessed (normal for authorized penetration testing). |
| **N** -- Non-compliance | Varies | Engagement scope documents must comply with rules of engagement. Evidence retention (`evidence_retention_days: 90`) and destruction (`secure-delete`) must be enforced for GDPR/regulatory compliance if target data includes EU citizens. |

### LINDDUN Mitigations

| Category | Mitigation | Task Mapping |
|----------|-----------|-------------|
| Linkability | Envoy access logs should be encrypted at rest on the log volume. | T13-001 (Envoy Dockerfile -- add log encryption) |
| Identifiability | Operator names in scope documents should not propagate to Envoy config files. Envoy configs should contain only technical allowlist data. | T13-012 (scope_translator.py) |
| Detectability | Docker network and container names should not use zone-revealing nomenclature in production deployments. | T13-006 through T13-011 (compose integration -- consider configurable naming) |
| Disclosure | Generated Envoy configs and log volumes should have restrictive file permissions (0600). | T13-001 (Envoy Dockerfile) |
| Non-compliance | Evidence retention and destruction timelines must be implemented in the CLI engagement lifecycle. | T13-023 (documentation) |

---

## L1: Mitigation Recommendations

Each recommendation maps to a specific FEAT-W13 task and addresses one or more threats from the register.

### Critical Mitigations (Must-implement before FEAT-W13 is considered complete)

| # | Mitigation | Threats Addressed | Task | Implementation Guidance |
|---|-----------|-------------------|------|------------------------|
| M-01 | **DNS egress control.** Configure Docker daemon or compose DNS settings to use an internal DNS resolver. In the compose network, add a DNS proxy container (e.g., CoreDNS or unbound) that restricts queries to: (a) Zone 1 update: only DB host domains, (b) Zone 2: engagement scope domains + DNS resolution for subdomain enumeration, (c) Zone 3: engagement scope + C2. Block all other DNS queries. | T-TB2-04 (DNS tunneling, DREAD 32) | T13-002, T13-003, T13-004 (per-zone Envoy configs should include DNS proxy config) | Add a `dns-proxy` service to each compose cluster. Set container `dns:` to point at the internal DNS proxy. The DNS proxy allowlist mirrors the Envoy HTTP allowlist. |
| M-02 | **Scope input validation in translator.** `scope_translator.py` MUST reject: wildcard domains broader than `*.specific.tld`, CIDR ranges broader than /16 without operator override, localhost/loopback targets, cloud metadata IPs (169.254.169.254), duplicate targets, and targets with embedded newlines or YAML injection characters. Use `yaml.safe_load()` exclusively. | T-TB4-01 (malicious scope, DREAD 30), T-TB4-E01 (YAML deser) | T13-012 | Implement a `ScopeValidator` class with deterministic rejection rules. Unit test with adversarial scope fixtures. |
| M-03 | **Transparent proxy for raw TCP.** Implement iptables REDIRECT within the compose network namespace for Zone 3 containers. This redirects all outbound TCP to Envoy's transparent proxy listener. This is a mandatory implementation requirement, not a deferred enhancement. | T-TB2-03 (raw TCP bypass, DREAD 28) | T13-004 | Add an init container or entrypoint script that configures iptables REDIRECT. Envoy must be configured with a transparent proxy listener in addition to the HTTP proxy listener. |
| M-04 | **Compose file CI validation.** Add a CI check (L5 enforcement layer) that validates all compose files for: `internal: true` on all non-egress networks, presence of Envoy service, HTTP_PROXY/HTTPS_PROXY env vars on all tool containers, absence of `privileged: true`, `network_mode: host`, and `cap_add: NET_ADMIN`. | T-TB6-01 (compose tampering, DREAD 27), T-TB6-E01 (privileged escalation, DREAD 29) | T13-005 (extend to CI validation) | Implement as a YAML linter in the CI pipeline. Use `yq` or Python `yaml.safe_load()` to parse and assert structural invariants. |

### High Mitigations (Strongly recommended; implement within FEAT-W13 timeline)

| # | Mitigation | Threats Addressed | Task | Implementation Guidance |
|---|-----------|-------------------|------|------------------------|
| M-05 | **Envoy config integrity hashing.** At `--init-engagement`, compute SHA-256 of the generated Envoy config. Store the hash in the engagement evidence directory. At tool execution time, re-compute the hash and compare. Reject execution if hashes differ. | T-TB5-S01 (stale config, DREAD 27), T-TB5-T01 (config modification, DREAD 25), T-TB5-R01 (no audit trail, DREAD 27) | T13-014 (CLI integration) | Store hash at `work/engagements/{id}/envoy-config-hash.sha256`. Compare at tool invocation time in the CLI handler. |
| M-06 | **Envoy deny-all default with explicit allowlist anchoring.** All generated Envoy route configs MUST: use `^...$` anchored regex for domain matching, escape dots (`\\.`), include a terminal deny-all route returning HTTP 403, and log denied requests. | T-TB2-S01 (header spoofing, DREAD 27), T-TB4-01 (permissive config, DREAD 30) | T13-002, T13-003, T13-004 | The ADR's Zone 1 config already demonstrates this pattern. Ensure the scope_translator.py generates the same pattern for Zone 2/3 dynamic configs. |
| M-07 | **Envoy connection limits and circuit breakers.** Configure per-cluster Envoy with: `max_connections`, `max_pending_requests`, `max_requests`, and `max_retries` circuit breaker thresholds. Rate-limit per-source-container if Envoy supports source-based routing. | T-TB2-D01 (proxy DoS, DREAD 27), T-TB1-D01 (network flooding, DREAD 27) | T13-002, T13-003, T13-004 | Add `circuit_breakers` configuration to each Envoy cluster definition. Recommended starting values: `max_connections: 100`, `max_pending_requests: 50`. |
| M-08 | **Scope-to-config translation audit logging.** `scope_translator.py` MUST log: input scope document path and SHA-256, each authorized_target and its generated Envoy route entry, each excluded_target and its generated deny entry, output Envoy config path and SHA-256. | T-TB4-R01 (no translation audit, DREAD 25) | T13-012 | Structured JSON log to `work/engagements/{id}/audit/scope-translation.log`. |
| M-09 | **Disable Envoy admin interface.** Do not enable Envoy's admin interface in any zone config. If admin is needed for debugging, bind to localhost only with authentication. | T-TB4-I01 (config exposure, DREAD 27), T-TB3-I01 (topology leak, DREAD 26) | T13-001 (Envoy Dockerfile) | Omit `admin:` section from Envoy config. If needed: `address: 127.0.0.1`, not `0.0.0.0`. |
| M-10 | **Read-only Envoy config mount enforcement.** All compose files MUST mount Envoy config with `:ro` flag. CI validation (M-04) should verify this. | T-TB3-02 (hot-reload injection, DREAD 25) | T13-006 through T13-011 | Already in the ADR design. CI check ensures it is not accidentally removed. |

### Medium Mitigations (Recommended; implement in follow-on sprint)

| # | Mitigation | Threats Addressed | Task | Implementation Guidance |
|---|-----------|-------------------|------|------------------------|
| M-11 | **Envoy access log sensitivity filtering.** Configure Envoy access log format to redact or hash query parameters and specific headers (Authorization, Cookie, X-Api-Key) before writing to the log file. | T-TB2-I01 (sensitive URL data, DREAD 28) | T13-002, T13-003, T13-004 | Use Envoy's `%REQ(header)%` with selective inclusion rather than logging all headers. Consider a log post-processor. |
| M-12 | **docker-compose.override.yml prevention.** Add a `.gitignore` entry for `docker-compose.override.yml` in each skill's Docker directory. Add a pre-commit hook that rejects compose override files. | T-TB6-S01 (override bypass, DREAD 27) | T13-005 (extend scope) | `.gitignore` prevents accidental commit. Pre-commit hook prevents intentional bypass. |
| M-13 | **Envoy log volume integrity.** Mount Envoy log volumes as append-only (if the filesystem supports it) or implement log shipping to an external location that tool containers cannot reach. | T-TB3-R01 (log tampering, DREAD 22) | T13-019 (E2E proxy tests) | Consider `chattr +a` on the log directory in the Envoy entrypoint. |
| M-14 | **Container image verification at startup.** Before starting tool containers, verify image digests against a known-good manifest. This prevents supply chain attacks that could inject DNS tunneling or proxy bypass capabilities. | T-TB2-04 (DNS tunneling path 1a), T-TB1-E01 (container escape) | T13-001 (Envoy Dockerfile scope extension) | Use Docker Content Trust or Cosign verification in the compose startup lifecycle. |
| M-15 | **Reduce frida container privileges.** Evaluate whether `SYS_PTRACE` can be scoped more narrowly. Remove `seccomp:unconfined` and use a custom seccomp profile that allows only ptrace-related syscalls. | T-TB1-E01 (container escape, DREAD 27) | T13-010 (rainbow-runtime compose) | Custom seccomp profile in `skills/rainbow-runtime/tests/docker/frida/seccomp.json`. |

---

## L2: Strategic Implications

### Three-Zone Security Model Evolution

The Envoy forward proxy architecture represents a **qualitative upgrade** in the three-zone security model's enforcement posture. The evolution path is:

| Phase | Enforcement Model | Trust Assumptions |
|-------|-------------------|-------------------|
| Pre-W13 (current) | Mixed: Zone 1 uses `network_mode: none` (structural). Zone 2/3 use bridge networking with behavioral CLI enforcement only. | CLI is trusted to invoke tools correctly. Once invoked, tools have unrestricted network access. |
| W13 (Envoy proxy) | Three-layer: `internal: true` (structural) + Envoy allowlist (network policy) + CLI behavioral gates (application). | Envoy is trusted as the network policy enforcement point. CLI is trusted for business logic. Tools are untrusted for network access. |
| Post-W13 (mature) | Three-layer + DNS control + transparent proxy + container image verification. | Envoy + DNS proxy form a complete network control plane. Tools are untrusted for all network operations including DNS. |

### Architectural Debt Items

| Item | Source Threat | Priority | Description |
|------|--------------|----------|-------------|
| DNS control plane | T-TB2-04 | Critical | The DNS tunneling gap is the largest residual risk in the architecture. Without DNS egress control, the `internal: true` + Envoy design has a structural bypass. This should be addressed in FEAT-W13, not deferred. |
| Transparent proxy for raw TCP | T-TB2-03 | Critical | Zone 3 tools (Impacket, pwntools, Metasploit) use raw TCP. Without transparent proxy, these tools either cannot reach their targets (functionality broken) or the proxy is bypassed (security broken). This must be part of the initial Envoy deployment. |
| Shared /work volume isolation | T-TB1-T01 | High | The shared bind mount is a pre-existing cross-container attack surface. Consider per-container subdirectories with restrictive permissions, or per-engagement Docker volumes instead of bind mounts. |
| frida elevated privileges | T-TB1-E01 | Medium | The frida container's `SYS_PTRACE` + `seccomp:unconfined` is the weakest isolation point in the entire architecture. This is operationally necessary for frida's function but should be offset with additional monitoring. |

### Risk Acceptance Decisions

The following residual risks require explicit operator acceptance:

| Residual Risk | Acceptance Rationale | Compensating Control |
|---------------|---------------------|---------------------|
| Envoy is a single point of failure for external access | Envoy compromise is high-impact but low-probability (mature codebase, active security team, CVE response process). Benefit of centralized policy enforcement outweighs risk. | Pin Envoy version in Dockerfile (T13-001). Monitor Envoy CVE feed. Automated rebuild on security patch release. |
| Zone 3 MITM enables Envoy to see decrypted traffic | Necessary for credential scrubbing (defense-in-depth with CLI credential filter). Envoy container must be treated as a high-trust component. | Envoy container runs non-root (T13-001). Envoy config is read-only mount. No admin interface. |
| Container-to-container traffic within a cluster is unlogged by Envoy | Envoy only sees egress traffic. Lateral movement within a cluster (e.g., exploit-msf to postgres) is not proxied. | This is acceptable for Zone 3 where containers are expected to communicate (exploit-msf depends on postgres). For Zone 1/2, containers should not communicate with each other -- enforce with separate Docker networks per service where feasible. |

### NIST CSF 2.0 Function Mapping

| CSF Function | Relevant Controls | Threat Model Coverage |
|-------------|-------------------|----------------------|
| **Identify (ID)** | ID.AM-2 (software inventory), ID.RA-1 (risk assessment) | Trust boundary inventory, threat register, DREAD scoring |
| **Protect (PR)** | PR.AC-3 (network access control), PR.DS-2 (data in transit), PR.IP-1 (security config) | Envoy allowlists (PR.AC), internal:true networks (PR.AC), config integrity hashing (PR.IP) |
| **Detect (DE)** | DE.CM-1 (network monitoring), DE.AE-3 (event correlation) | Envoy access logs (DE.CM), DNS query monitoring (DE.CM), config hash verification (DE.AE) |
| **Respond (RS)** | RS.AN-1 (investigation), RS.MI-1 (incident containment) | Emergency stop mechanism (Zone 3), circuit breaker on proxy DoS |
| **Recover (RC)** | RC.RP-1 (recovery planning) | Envoy stateless restart, config regeneration from scope document |

---

## Traceability

| Reference | Location |
|-----------|----------|
| ADR-PROJ023-003 v2 | `projects/PROJ-023-exploit-framework/work/design/network-isolation-analysis.md` |
| FEAT-W13 | `projects/PROJ-023-exploit-framework/work/FEAT-W13-envoy-network-isolation/FEAT-W13.md` |
| Zone 2 Guardrail Profile | `skills/rainbow/rules/zone-2-active.md` |
| Zone 3 Guardrail Profile | `skills/rainbow/rules/zone-3-exploit.md` |
| Engagement Scope Template | `skills/rainbow/rules/engagement-scope-template.yaml` |
| Tool Resolution Table | `skills/rainbow/config/tool-exec.yaml` |
| Compose: rainbow-supply-chain | `skills/rainbow-supply-chain/tests/docker/docker-compose.yml` |
| Compose: blue-team | `skills/blue-team/tests/docker/docker-compose.yml` |
| Compose: rainbow-recon | `skills/rainbow-recon/tests/docker/docker-compose.yml` |
| Compose: rainbow-cloud | `skills/rainbow-cloud/tests/docker/docker-compose.yml` |
| Compose: rainbow-runtime | `skills/rainbow-runtime/tests/docker/docker-compose.yml` |
| Compose: rainbow-exploit | `skills/rainbow-exploit/tests/docker/docker-compose.yml` |
| NIST CSF 2.0 | Framework functions: Identify, Protect, Detect, Respond, Recover |
| STRIDE | Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege |
| DREAD | Damage, Reproducibility, Exploitability, Affected Users, Discoverability (scale 1-10 per factor, composite sum) |
| LINDDUN | Linkability, Identifiability, Non-repudiation, Detectability, Disclosure, Unawareness, Non-compliance |

---

*Threat model produced by eng-architect. C3 criticality per AE-005 (security-relevant architecture). 34 threats identified across 6 trust boundaries. 15 mitigations recommended (4 critical, 6 high, 5 medium). Top risk: DNS tunneling bypass (DREAD 32) -- requires DNS egress control as a mandatory FEAT-W13 deliverable.*
