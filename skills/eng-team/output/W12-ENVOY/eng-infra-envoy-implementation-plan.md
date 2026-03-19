# Envoy Forward Proxy Implementation Plan
# Rainbow Three-Zone Model -- Network Isolation Infrastructure

> **Engagement ID:** W12-ENVOY
> **Agent:** eng-infra
> **Date:** 2026-03-18
> **Criticality:** C3 (security-critical infrastructure, >10 files affected, AE-003 + AE-005)
> **ADR Source:** ADR-PROJ023-003 v2.0.0 (network-isolation-analysis.md) -- Option D: Forward Proxy with Deny-by-Default Egress
> **Constitutional Compliance:** P-001 (evidence-based), P-002 (persisted), P-003 (single-level nesting), P-020 (user authority), P-022 (no deception)

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Security posture, SLSA level, CIS compliance status |
| [L1: Per-Compose-File Changes](#l1-per-compose-file-changes) | Exact diff-ready changes for all 6 compose files |
| [L1: Envoy Configuration Files](#l1-envoy-configuration-files) | Complete YAML for all 4 zone configs |
| [L1: Engagement-Scope-to-Envoy Translation](#l1-engagement-scope-to-envoy-translation) | Three options evaluated; recommendation with rationale |
| [L1: E2E Validation Tests](#l1-e2e-validation-tests) | Test matrix proving the proxy works |
| [L1: Effort Estimates](#l1-effort-estimates) | Worktracker-ready tasks with hour estimates |
| [L1: Raw TCP Tool Handling](#l1-raw-tcp-tool-handling) | Impacket / pwntools bypass; recommendation |
| [L2: Strategic Implications](#l2-strategic-implications) | Supply chain risk, SLSA roadmap, vendor assessment |

---

## L0: Executive Summary

### Infrastructure Security Posture

This plan implements ADR-PROJ023-003 v2.0.0's selected Option D: a deny-by-default Envoy forward proxy per Docker compose cluster. The architecture creates three independent security layers at different trust boundaries:

1. **Docker `internal: true` network topology** -- tool containers have no external route by construction. A compromised tool binary cannot reach the internet regardless of what code it executes.
2. **Envoy proxy egress policy** -- the only container with an external route enforces a zone-specific allowlist. Every connection is logged to structured JSON for forensic chain of custody.
3. **CLI behavioral gates** -- engagement scope validation, per-operation approval, and credential filtering at the application layer (unchanged from current implementation).

This is genuine defense in depth: compromising one layer does not compromise the others. The CLI cannot bypass Envoy (separate container). Envoy cannot be bypassed by tool containers (Docker topology has no direct external route).

### SLSA Build Level

The Envoy proxy containers themselves target **SLSA Level 2**:
- Envoy is a well-known open-source project from the CNCF with a documented build process.
- `envoyproxy/envoy:v1.31-latest` is pulled from Docker Hub. For production engagement use, pin to a digest-addressed image (e.g., `envoyproxy/envoy@sha256:<digest>`) to achieve provenance integrity.
- Zone config files are version-controlled in this repository with SHA-256 audit trail.
- Achieving SLSA Level 3 requires a hardened build platform for the Envoy base image -- use `envoyproxy/envoy:v1.31-latest` from the official CNCF-maintained registry, not third-party mirrors.

### CIS Benchmark Status

| Category | Status | Notes |
|----------|--------|-------|
| Container Runtime (CIS Docker 1.6) | PARTIAL | `no-new-privileges:true` on all services. Non-root user in Envoy base image. Read-only config mount. |
| Network (CIS Docker 5.x) | PASS after changes | `internal: true` enforces network segmentation per CIS 5.29. Named networks per CIS 5.24. |
| Secrets / Credentials | PASS | No credentials in compose environment variables. Proxy auth not required for internal network routing. |
| Logging | PASS after changes | Envoy access logs in structured JSON to volume-mounted evidence path. |

### Key Supply Chain Risks

| Risk | Severity | Mitigation |
|------|----------|-----------|
| `envoyproxy/envoy:v1.31-latest` tag is mutable | HIGH | Pin to digest in production; rotate on CVE advisories. |
| Envoy config generation (scope-to-policy) is security-critical new code | HIGH | Test coverage >= 90% required per H-20; mutation testing for allowlist generation logic. |
| Zone 2/3 allowlists generated at engagement init -- stale if scope changes mid-engagement | MEDIUM | Envoy hot-restart on scope update; CLI pre-flight validates config is current. |
| Impacket/pwntools bypass HTTP_PROXY (raw TCP) | MEDIUM | `internal: true` provides network-level containment; transparent proxy deferred to Phase 2. |

---

## L1: Per-Compose-File Changes

### Structural Pattern (All 6 Files)

Every compose file adopts the same topology:

```
Tool containers
  |__ zone{N}-active network  (internal: true -- no external route)
  |   HTTP_PROXY=http://envoy-z{N}:3128

Envoy proxy
  |__ zone{N}-active network  (receives tool traffic)
  |__ zone{N}-egress network  (external route to internet, allowlist-filtered)
  |   Volume: per-zone envoy config (read-only)
  |   Volume: /var/log/envoy -> evidence volume

DB-only internal services (postgres)
  |__ {service}-internal network  (internal: true -- isolated from tool and egress networks)
```

---

### 1. `skills/rainbow-supply-chain/tests/docker/docker-compose.yml`

**Zone mapping:**
- `scanner` (syft): Zone 1 Offline -- SBOM from local artifacts, no network needed.
- `scanner-net` (grype, osv-scanner): Zone 1 DB-Update -- vulnerability DB downloads via proxy.
- `verifier` (cosign, snyk): Zone 1 DB-Update -- signature verification and advisory lookup via proxy.

**Changes required:**
- Remove `network_mode: none` from all services (it blocks naming any network; incompatible with named networks).
- Add named networks: `zone1-offline` (`internal: true`), `zone1-update` (`internal: true`), `zone1-egress` (bridge, external).
- Split `scanner` into `scanner` (offline) and `scanner-net` (proxy-enabled). The tool-exec.yaml service split is addressed in Section 7 below.
- Add `envoy-z1-update` service.
- Add `depends_on: envoy-z1-update: condition: service_started` to `scanner-net` and `verifier`.

```yaml
---
# Zone 1: Supply chain scanning
# Zone 1 Offline: syft (SBOM generation, no network)
# Zone 1 DB-Update: grype, osv-scanner, cosign, snyk (vulnerability DBs + registries via proxy)

services:

  scanner:
    # syft: local SBOM generation from images and directories.
    # No network required. Reads from /work volume only.
    build:
      context: ./scanner
    volumes:
      - ../../../../work:/work
    working_dir: /work
    networks:
      - zone1-offline
    security_opt:
      - no-new-privileges:true

  scanner-net:
    # grype, osv-scanner: vulnerability DB download from osv.dev, nvd.nist.gov.
    # Routes all egress through envoy-z1-update (allowlisted DB hosts only).
    build:
      context: ./scanner
    volumes:
      - ../../../../work:/work
    working_dir: /work
    networks:
      - zone1-update
    environment:
      HTTP_PROXY: "http://envoy-z1-update:3128"
      HTTPS_PROXY: "http://envoy-z1-update:3128"
      NO_PROXY: "localhost,127.0.0.1"
    security_opt:
      - no-new-privileges:true
    depends_on:
      envoy-z1-update:
        condition: service_started

  verifier:
    # cosign verify, snyk: signature + advisory lookup.
    # Routes egress through envoy-z1-update (allowlisted hosts only).
    build:
      context: ./verifier
    volumes:
      - ../../../../work:/work
    working_dir: /work
    networks:
      - zone1-update
    environment:
      HTTP_PROXY: "http://envoy-z1-update:3128"
      HTTPS_PROXY: "http://envoy-z1-update:3128"
      NO_PROXY: "localhost,127.0.0.1"
    security_opt:
      - no-new-privileges:true
    depends_on:
      envoy-z1-update:
        condition: service_started

  envoy-z1-update:
    # Deny-by-default egress proxy for Zone 1 DB-Update.
    # Allowlist: github.com, objects.githubusercontent.com, osv.dev, api.osv.dev,
    #            nvd.nist.gov, services.nvd.nist.gov, pypi.org, files.pythonhosted.org,
    #            toolbox-data.anchore.io (grype DB), sigstore.dev (cosign TUF).
    image: envoyproxy/envoy:v1.31-latest
    volumes:
      - ../../../../skills/rainbow/config/envoy/envoy-zone1-update.yaml:/etc/envoy/envoy.yaml:ro
      - envoy-z1-logs:/var/log/envoy
    networks:
      - zone1-update
      - zone1-egress
    security_opt:
      - no-new-privileges:true
    healthcheck:
      test: ["CMD-SHELL", "curl -sf http://localhost:9901/ready || exit 1"]
      interval: 5s
      timeout: 3s
      retries: 5

networks:
  zone1-offline:
    driver: bridge
    internal: true
    # Zone 1 Offline: zero external connectivity. No proxy. syft only.
  zone1-update:
    driver: bridge
    internal: true
    # Zone 1 DB-Update: internal only. External access via envoy-z1-update proxy.
  zone1-egress:
    driver: bridge
    # External route. Only envoy-z1-update is attached to this network.

volumes:
  envoy-z1-logs:
```

**tool-exec.yaml service mapping updates required:**

| Tool Prefix | Old Service | New Service | Reason |
|-------------|-------------|-------------|--------|
| `syft` | `scanner` | `scanner` | Unchanged -- stays offline |
| `grype` | `scanner` | `scanner-net` | Needs DB network access |
| `osv-scanner` | `scanner` | `scanner-net` | Needs OSV API access |
| `cosign` | `verifier` | `verifier` | Service name unchanged; network changed |
| `snyk` | `verifier` | `verifier` | Service name unchanged; network changed |

---

### 2. `skills/blue-team/tests/docker/docker-compose.yml`

**Zone mapping:**
- `detection` (YARA-X, Sigma, Hayabusa, Chainsaw): Zone 1 Offline -- local file analysis.
- `compliance` (Checkov -- IaC scan mode): Zone 1 Offline -- local file scan.
- `compliance-net` (Trivy -- DB download): Zone 1 DB-Update -- vulnerability DB via proxy.
- `forensics` (Ghidra, volatility): Zone 1 Offline -- local artifact analysis.
- `intel` (MISP client, STIX): Zone 1 Offline for test fixtures; may need Zone 1 DB-Update for live MISP lookup.

**Changes required:**
- Remove `network_mode: none` from all services.
- Add `zone1-offline`, `zone1-update`, `zone1-egress` networks.
- Add new `compliance-net` service (same Dockerfile as `compliance`, different network + proxy env).
- Add `envoy-z1-update` service.

```yaml
---
# Zone 1: Blue team defensive analysis
# Zone 1 Offline: YARA, Sigma, Hayabusa, Chainsaw, Checkov (IaC), forensics, intel
# Zone 1 DB-Update: Trivy (vulnerability DB download)

services:

  detection:
    # YARA-X, Sigma CLI, Hayabusa, Chainsaw: local artifact analysis.
    # No network required.
    build:
      context: ./detection
      dockerfile: Dockerfile
    image: blue-detection:latest
    container_name: blue-detection
    working_dir: /app
    volumes:
      - detection-output:/output
      - detection-fixtures:/fixtures
      - ../../../../work:/work
    security_opt:
      - no-new-privileges:true
    networks:
      - zone1-offline
    entrypoint: ["/bin/bash"]
    stdin_open: true
    tty: true

  compliance:
    # Checkov: IaC scanning against local files.
    # No network required for IaC-only mode.
    build:
      context: ./compliance
      dockerfile: Dockerfile
    image: blue-compliance:latest
    container_name: blue-compliance
    working_dir: /app
    volumes:
      - compliance-output:/output
      - compliance-fixtures:/fixtures
      - ../../../../work:/work
    security_opt:
      - no-new-privileges:true
    networks:
      - zone1-offline
    entrypoint: ["/bin/bash"]
    stdin_open: true
    tty: true

  compliance-net:
    # Trivy: vulnerability DB download from GitHub releases and NVD.
    # Requires proxy-gated network access.
    # Note: separate service from compliance to preserve Zone 1 Offline isolation
    # for Checkov while enabling Trivy DB updates.
    build:
      context: ./compliance
      dockerfile: Dockerfile
    image: blue-compliance:latest
    container_name: blue-compliance-net
    working_dir: /app
    volumes:
      - compliance-output:/output
      - compliance-fixtures:/fixtures
      - ../../../../work:/work
    security_opt:
      - no-new-privileges:true
    networks:
      - zone1-update
    environment:
      HTTP_PROXY: "http://envoy-z1-update:3128"
      HTTPS_PROXY: "http://envoy-z1-update:3128"
      NO_PROXY: "localhost,127.0.0.1"
    entrypoint: ["/bin/bash"]
    stdin_open: true
    tty: true
    depends_on:
      envoy-z1-update:
        condition: service_started

  forensics:
    # Ghidra, Volatility3, plaso: local binary/memory analysis.
    # No network required.
    build:
      context: ./forensics
      dockerfile: Dockerfile
    image: blue-forensics:latest
    container_name: blue-forensics
    working_dir: /app
    volumes:
      - forensics-output:/output
      - forensics-fixtures:/fixtures
      - ../../../../work:/work
    security_opt:
      - no-new-privileges:true
    networks:
      - zone1-offline
    entrypoint: ["/bin/bash"]
    stdin_open: true
    tty: true

  intel:
    # MISP client, STIX tools: test fixtures only (offline).
    # If live MISP feed lookup required in future, move to zone1-update
    # and add MISP API endpoint to the Zone 1 allowlist.
    build:
      context: ./intel
      dockerfile: Dockerfile
    image: blue-intel:latest
    container_name: blue-intel
    working_dir: /app
    volumes:
      - intel-output:/output
      - intel-fixtures:/fixtures
      - ../../../../work:/work
    security_opt:
      - no-new-privileges:true
    networks:
      - zone1-offline
    entrypoint: ["/bin/bash"]
    stdin_open: true
    tty: true

  envoy-z1-update:
    image: envoyproxy/envoy:v1.31-latest
    volumes:
      - ../../../../skills/rainbow/config/envoy/envoy-zone1-update.yaml:/etc/envoy/envoy.yaml:ro
      - envoy-z1-logs:/var/log/envoy
    networks:
      - zone1-update
      - zone1-egress
    security_opt:
      - no-new-privileges:true
    healthcheck:
      test: ["CMD-SHELL", "curl -sf http://localhost:9901/ready || exit 1"]
      interval: 5s
      timeout: 3s
      retries: 5

networks:
  zone1-offline:
    driver: bridge
    internal: true
  zone1-update:
    driver: bridge
    internal: true
  zone1-egress:
    driver: bridge

volumes:
  detection-output:
  detection-fixtures:
  compliance-output:
  compliance-fixtures:
  forensics-output:
  forensics-fixtures:
  intel-output:
  intel-fixtures:
  envoy-z1-logs:
```

**tool-exec.yaml service mapping updates required:**

| Tool Prefix | Old Service | New Service |
|-------------|-------------|-------------|
| `trivy` | `compliance` | `compliance-net` |
| All other blue-team tools | unchanged | unchanged |

---

### 3. `skills/rainbow-recon/tests/docker/docker-compose.yml`

**Zone mapping:**
- `recon-pipeline` (Subfinder, httpx, dnsx, naabu, katana, Nuclei): Zone 2 Active -- all egress through Envoy with engagement-scope-derived allowlist.

**Changes required:**
- Replace existing `cloud-net` bridge network with `zone2-active` (`internal: true`) + `zone2-egress` (bridge).
- Add `HTTP_PROXY`/`HTTPS_PROXY` environment variables to `recon-pipeline`.
- Add `envoy-z2` service.
- Add evidence volume mount to `envoy-z2` for log collection.

```yaml
---
# Zone 2: Active reconnaissance
# Tools: Subfinder, httpx, dnsx, naabu, katana, Nuclei
# Engagement scope required before execution (validated by CLI).
# Envoy enforces scope-derived allowlist at network level.

services:

  recon-pipeline:
    build:
      context: ./recon-pipeline
      dockerfile: Dockerfile
    image: rainbow-recon-pipeline:latest
    container_name: recon-pipeline
    working_dir: /work
    volumes:
      - ../../../../work:/work
    networks:
      - zone2-active
    environment:
      HTTP_PROXY: "http://envoy-z2:3128"
      HTTPS_PROXY: "http://envoy-z2:3128"
      # Exclude internal DNS resolution from proxy to avoid breaking dnsx
      # which uses raw DNS sockets (not HTTP). dnsx is NOT proxy-aware.
      # dnsx reaches targets via direct UDP/TCP DNS -- see Raw TCP section.
      NO_PROXY: "localhost,127.0.0.1"
    security_opt:
      - no-new-privileges:true
    read_only: false
    entrypoint: ["/bin/sh"]
    stdin_open: true
    tty: true
    depends_on:
      envoy-z2:
        condition: service_started

  envoy-z2:
    # Zone 2 deny-by-default proxy.
    # Config is generated from engagement scope YAML by:
    #   jerry tool exec --init-engagement <scope.yaml>
    # Config location: skills/rainbow/config/envoy/envoy-zone2-active.yaml
    # Access log: /var/log/envoy/access.log -> mounted to evidence volume.
    image: envoyproxy/envoy:v1.31-latest
    volumes:
      - ../../../../skills/rainbow/config/envoy/envoy-zone2-active.yaml:/etc/envoy/envoy.yaml:ro
      - envoy-z2-logs:/var/log/envoy
      - ../../../../work:/work:ro
    networks:
      - zone2-active
      - zone2-egress
    security_opt:
      - no-new-privileges:true
    healthcheck:
      test: ["CMD-SHELL", "curl -sf http://localhost:9901/ready || exit 1"]
      interval: 5s
      timeout: 3s
      retries: 5

networks:
  zone2-active:
    driver: bridge
    internal: true
    # Internal network: recon-pipeline cannot reach internet directly.
    # All HTTP/HTTPS egress routes through envoy-z2.
  zone2-egress:
    driver: bridge
    # External route. Only envoy-z2 is attached to this network.

volumes:
  envoy-z2-logs:
```

**DNS bypass note (load-bearing):** `dnsx` uses raw UDP/TCP DNS sockets. It does NOT use HTTP_PROXY. The `internal: true` network allows DNS queries to pass through the Docker-embedded resolver to the host's DNS, which then reaches the internet. This is an intentional bypass because DNS is required for subdomain enumeration. See Raw TCP Tool Handling section for full analysis. Document this as a known gap in Zone 2 coverage.

---

### 4. `skills/rainbow-cloud/tests/docker/docker-compose.yml`

**Zone mapping:**
- `cloud-auditor` (Checkov, Prowler, Kubescape): Split by tool operation:
  - Checkov IaC scan: Zone 1 Offline (local files).
  - Prowler / Kubescape: Zone 2 (cloud API calls to AWS/Azure/GCP; engagement scope required).
  - Current compose has a single `cloud-auditor` service. Keep single service but route through Zone 2 proxy because Prowler and Kubescape API calls are the primary use case. Checkov in IaC mode does not make outbound calls so the proxy allowlist does not restrict it.

**Changes required:**
- Replace `cloud-net` bridge network with `zone2-active` (`internal: true`) + `zone2-egress` (bridge).
- Add `HTTP_PROXY`/`HTTPS_PROXY` to `cloud-auditor`.
- Add `envoy-z2` service.
- Add cloud API endpoints to Zone 2 allowlist (AWS STS, GCP APIs, Azure ARM) -- these are added during `--init-engagement` as the cloud account is the engagement target.

```yaml
---
# Zone 2: Cloud security posture assessment
# Tools: Checkov (IaC), Prowler (AWS/Azure/GCP), Kubescape (Kubernetes)
# Engagement scope required for Prowler/Kubescape (cloud account is the target).
# Checkov in IaC mode is offline; proxy does not restrict it.

services:

  cloud-auditor:
    build:
      context: ./cloud-auditor
      dockerfile: Dockerfile
    image: rainbow-cloud-auditor:latest
    container_name: cloud-auditor
    working_dir: /work
    volumes:
      - cloud-output:/work/output
      - ../../../../work:/work
    networks:
      - zone2-active
    environment:
      HTTP_PROXY: "http://envoy-z2:3128"
      HTTPS_PROXY: "http://envoy-z2:3128"
      NO_PROXY: "localhost,127.0.0.1"
    security_opt:
      - no-new-privileges:true
    entrypoint: ["/bin/sh"]
    stdin_open: true
    tty: true
    depends_on:
      envoy-z2:
        condition: service_started

  envoy-z2:
    # Zone 2 deny-by-default proxy for cloud API access.
    # Engagement scope must include cloud_account targets.
    # Cloud API endpoints (AWS STS, GCP IAM, Azure ARM) are added
    # to the generated Zone 2 Envoy config at --init-engagement time.
    image: envoyproxy/envoy:v1.31-latest
    volumes:
      - ../../../../skills/rainbow/config/envoy/envoy-zone2-active.yaml:/etc/envoy/envoy.yaml:ro
      - envoy-z2-logs:/var/log/envoy
      - ../../../../work:/work:ro
    networks:
      - zone2-active
      - zone2-egress
    security_opt:
      - no-new-privileges:true
    healthcheck:
      test: ["CMD-SHELL", "curl -sf http://localhost:9901/ready || exit 1"]
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
  cloud-output:
  envoy-z2-logs:
```

---

### 5. `skills/rainbow-exploit/tests/docker/docker-compose.yml`

**Zone mapping:**
- `exploit-ops` (Impacket, pwntools, donut): Zone 3 -- raw TCP tools, engagement targets.
- `exploit-c2` (Empire, Starkiller): Zone 3 -- C2 infrastructure communication.
- `exploit-msf` (Metasploit): Zone 3 -- active exploitation, DB access.
- `postgres`: DB service -- `msf-internal` network only (`internal: true`); no internet access.

**Changes required:**
- Add `zone3-exploit` (`internal: true`), `zone3-egress` (bridge), `msf-internal` (`internal: true`) networks.
- Add `HTTP_PROXY`/`HTTPS_PROXY` to all exploit services.
- Set `NO_PROXY=localhost,127.0.0.1,postgres` on `exploit-msf` (postgres is on a separate internal network but we include it in NO_PROXY defensively).
- Move `postgres` from default Docker network to `msf-internal` only.
- Add `envoy-z3` service.
- Preserve `postgres` healthcheck and `exploit-msf` depends_on.

```yaml
---
# Zone 3: Exploitation
# Tools: Impacket, pwntools/donut, Metasploit, Empire/Starkiller
# Engagement scope + per-operation human approval required before each invocation.
# All HTTP/HTTPS egress routes through envoy-z3 (scope-derived allowlist + C2 IPs).
# Raw TCP tools (Impacket, pwntools): see Raw TCP Tool Handling section.
# postgres is on msf-internal only -- no external route.

services:

  exploit-ops:
    # Impacket (impacket-*), pwntools, donut.
    # Note: Impacket uses raw SMB/LDAP/Kerberos (TCP 445, 389, 88).
    # HTTP_PROXY does NOT affect these connections.
    # Network-level containment via internal: true prevents direct internet egress.
    # See Raw TCP Tool Handling section for transparent proxy option.
    build:
      context: ./exploit-ops
      dockerfile: Dockerfile
    image: rainbow-exploit-ops:latest
    container_name: rainbow-exploit-ops
    volumes:
      - ../../../../work:/work
    networks:
      - zone3-exploit
    environment:
      HTTP_PROXY: "http://envoy-z3:3128"
      HTTPS_PROXY: "http://envoy-z3:3128"
      NO_PROXY: "localhost,127.0.0.1"
    security_opt:
      - no-new-privileges:true
    stdin_open: true
    tty: true
    depends_on:
      envoy-z3:
        condition: service_started

  exploit-c2:
    # Empire (C2 framework), Starkiller (Empire UI).
    # C2 listener port exposed for inbound agent callbacks.
    # Outbound C2 traffic (staging, updates) routes through envoy-z3.
    # C2 infrastructure IPs must be in engagement scope and added to Zone 3 allowlist.
    build:
      context: ./exploit-c2
      dockerfile: Dockerfile
    image: rainbow-exploit-c2:latest
    container_name: rainbow-exploit-c2
    ports:
      - "1337:1337"
    volumes:
      - ../../../../work:/work
    networks:
      - zone3-exploit
    environment:
      HTTP_PROXY: "http://envoy-z3:3128"
      HTTPS_PROXY: "http://envoy-z3:3128"
      NO_PROXY: "localhost,127.0.0.1"
    security_opt:
      - no-new-privileges:true
    stdin_open: true
    tty: true
    depends_on:
      envoy-z3:
        condition: service_started

  exploit-msf:
    # Metasploit Framework: msfconsole, msfvenom.
    # DB connection to postgres is on msf-internal (separate network, no proxy).
    # External module downloads and target connections through envoy-z3.
    build:
      context: ./exploit-msf
      dockerfile: Dockerfile
    image: rainbow-exploit-msf:latest
    container_name: rainbow-exploit-msf
    depends_on:
      postgres:
        condition: service_healthy
      envoy-z3:
        condition: service_started
    environment:
      DATABASE_URL: "postgresql://msf:msf@postgres:5432/msf"
      HTTP_PROXY: "http://envoy-z3:3128"
      HTTPS_PROXY: "http://envoy-z3:3128"
      # postgres is on msf-internal, not zone3-exploit.
      # NO_PROXY prevents proxy lookup for postgres hostname.
      NO_PROXY: "localhost,127.0.0.1,postgres"
    volumes:
      - ../../../../work:/work
    networks:
      - zone3-exploit
      - msf-internal
    security_opt:
      - no-new-privileges:true
    stdin_open: true
    tty: true

  postgres:
    # Metasploit database. Isolated on msf-internal only.
    # No external network access: postgres has no business reaching the internet.
    image: postgres:16-alpine
    container_name: rainbow-msf-postgres
    environment:
      POSTGRES_USER: msf
      POSTGRES_PASSWORD: msf
      POSTGRES_DB: msf
    volumes:
      - msf-pgdata:/var/lib/postgresql/data
    networks:
      - msf-internal
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U msf"]
      interval: 10s
      timeout: 5s
      retries: 5

  envoy-z3:
    # Zone 3 deny-by-default proxy for exploitation traffic.
    # Config generated from engagement scope + C2 infrastructure IPs.
    # Full connection logging: timestamp, method, URL, response code, bytes.
    # Zone 3 enables TLS interception for credential scrubbing (optional --
    # requires trust anchor injection into tool containers; see config).
    image: envoyproxy/envoy:v1.31-latest
    volumes:
      - ../../../../skills/rainbow/config/envoy/envoy-zone3-exploit.yaml:/etc/envoy/envoy.yaml:ro
      - envoy-z3-logs:/var/log/envoy
      - ../../../../work:/work:ro
    networks:
      - zone3-exploit
      - zone3-egress
    security_opt:
      - no-new-privileges:true
    healthcheck:
      test: ["CMD-SHELL", "curl -sf http://localhost:9901/ready || exit 1"]
      interval: 5s
      timeout: 3s
      retries: 5

networks:
  zone3-exploit:
    driver: bridge
    internal: true
    # Tool containers on this network have no direct external route.
    # All HTTP/HTTPS egress must pass through envoy-z3.
  zone3-egress:
    driver: bridge
    # External route. Only envoy-z3 is attached to this network.
  msf-internal:
    driver: bridge
    internal: true
    # postgres isolation: no external route, no proxy.

volumes:
  msf-pgdata:
  envoy-z3-logs:
```

---

### 6. `skills/rainbow-runtime/tests/docker/docker-compose.yml`

**Zone mapping:**
- `mitmproxy` (mitmproxy, mitmdump, mitmweb): Zone 2 -- network interception boundary.
- `frida` (frida, frida-trace, frida-ps): Zone 3 -- process instrumentation.
- This compose file spans two zones and therefore needs **two Envoy instances**.

**Changes required:**
- Add `zone2-active`, `zone2-egress`, `zone3-exploit`, `zone3-egress` networks.
- Assign `mitmproxy` to `zone2-active`; assign `frida` to `zone3-exploit`.
- Add `HTTP_PROXY` to both services.
- Add `envoy-z2` and `envoy-z3` services.

```yaml
---
# Zone 2/3 boundary: runtime analysis and process instrumentation.
# mitmproxy: Zone 2 (network interception boundary -- captures traffic to/from targets).
# frida: Zone 3 (process attachment -- requires elevated capabilities).
# These services MUST NOT share a network namespace (zone isolation preserved).

services:

  mitmproxy:
    # mitmproxy, mitmdump, mitmweb: TLS-intercepting proxy for traffic analysis.
    # Zone 2: engagement scope required. Targets must be in allowlist.
    # Note: mitmproxy acts as a MITM proxy for tool traffic -- its OWN outbound
    # traffic (to targets it is proxying for) routes through envoy-z2.
    build:
      context: ./mitmproxy
      dockerfile: Dockerfile
    image: rainbow-runtime-mitmproxy:latest
    container_name: rainbow-runtime-mitmproxy
    ports:
      - "8080:8080"
    volumes:
      - ../../../../work:/work
    networks:
      - zone2-active
    environment:
      HTTP_PROXY: "http://envoy-z2:3128"
      HTTPS_PROXY: "http://envoy-z2:3128"
      NO_PROXY: "localhost,127.0.0.1"
    stdin_open: true
    tty: true
    depends_on:
      envoy-z2:
        condition: service_started

  frida:
    # frida, frida-trace, frida-ps: dynamic instrumentation.
    # Zone 3: per-operation approval required.
    # SYS_PTRACE capability required for process attachment.
    # HTTP_PROXY: any Frida network calls (e.g., device connect) route through envoy-z3.
    build:
      context: ./frida
      dockerfile: Dockerfile
    image: rainbow-runtime-frida:latest
    container_name: rainbow-runtime-frida
    cap_add:
      - SYS_PTRACE
    security_opt:
      - seccomp:unconfined
    volumes:
      - ../../../../work:/work
    networks:
      - zone3-exploit
    environment:
      HTTP_PROXY: "http://envoy-z3:3128"
      HTTPS_PROXY: "http://envoy-z3:3128"
      NO_PROXY: "localhost,127.0.0.1"
    stdin_open: true
    tty: true
    depends_on:
      envoy-z3:
        condition: service_started

  envoy-z2:
    image: envoyproxy/envoy:v1.31-latest
    volumes:
      - ../../../../skills/rainbow/config/envoy/envoy-zone2-active.yaml:/etc/envoy/envoy.yaml:ro
      - envoy-z2-logs:/var/log/envoy
      - ../../../../work:/work:ro
    networks:
      - zone2-active
      - zone2-egress
    security_opt:
      - no-new-privileges:true
    healthcheck:
      test: ["CMD-SHELL", "curl -sf http://localhost:9901/ready || exit 1"]
      interval: 5s
      timeout: 3s
      retries: 5

  envoy-z3:
    image: envoyproxy/envoy:v1.31-latest
    volumes:
      - ../../../../skills/rainbow/config/envoy/envoy-zone3-exploit.yaml:/etc/envoy/envoy.yaml:ro
      - envoy-z3-logs:/var/log/envoy
      - ../../../../work:/work:ro
    networks:
      - zone3-exploit
      - zone3-egress
    security_opt:
      - no-new-privileges:true
    healthcheck:
      test: ["CMD-SHELL", "curl -sf http://localhost:9901/ready || exit 1"]
      interval: 5s
      timeout: 3s
      retries: 5

networks:
  zone2-active:
    driver: bridge
    internal: true
  zone2-egress:
    driver: bridge
  zone3-exploit:
    driver: bridge
    internal: true
  zone3-egress:
    driver: bridge

volumes:
  envoy-z2-logs:
  envoy-z3-logs:
```

---

## L1: Envoy Configuration Files

All configs live under: `skills/rainbow/config/envoy/`

**Important implementation note:** Envoy's standard HTTP proxy forward mode requires the `envoy.filters.http.dynamic_forward_proxy` filter for CONNECT tunnel support (HTTPS). The configs below use the HTTP Connection Manager with a route-based allowlist for simplicity and correctness. The `dynamic_forward_proxy` cluster handles DNS resolution for the upstream targets. This config pattern is Envoy v1.31 compatible.

---

### Zone 1 Offline: No Envoy Required

Services on `zone1-offline` (`internal: true`) have zero egress. The Docker network provides the isolation. No proxy container is needed. Document the services on this network:

```
zone1-offline services (no network egress, ever):
  - scanner (syft)               -- supply-chain compose
  - detection                    -- blue-team compose
  - compliance (Checkov IaC mode) -- blue-team compose
  - forensics                    -- blue-team compose
  - intel                        -- blue-team compose
```

---

### `skills/rainbow/config/envoy/envoy-zone1-update.yaml`

Static allowlist for vulnerability DB hosts. No engagement scope needed -- these are fixed infrastructure hosts for tool database updates.

```yaml
# envoy-zone1-update.yaml
# Zone 1 DB-Update: deny-by-default egress proxy.
# Allowlist: fixed set of vulnerability DB and package registry hosts.
# Used by: scanner-net (grype, osv-scanner), verifier (cosign, snyk),
#           compliance-net (trivy), cloud-auditor (checkov registry mode).
# No dynamic config: allowlist is static and version-controlled.

admin:
  address:
    socket_address:
      address: 0.0.0.0
      port_value: 9901

static_resources:
  listeners:
    - name: egress_proxy
      address:
        socket_address:
          address: 0.0.0.0
          port_value: 3128
      filter_chains:
        - filters:
            - name: envoy.filters.network.http_connection_manager
              typed_config:
                "@type": type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager
                stat_prefix: zone1_update_egress
                upgrade_configs:
                  - upgrade_type: CONNECT
                access_log:
                  - name: envoy.access_loggers.file
                    typed_config:
                      "@type": type.googleapis.com/envoy.extensions.access_loggers.file.v3.FileAccessLog
                      path: /var/log/envoy/access.log
                      log_format:
                        json_format:
                          ts: "%START_TIME%"
                          method: "%REQ(:METHOD)%"
                          authority: "%REQ(:AUTHORITY)%"
                          path: "%REQ(X-ENVOY-ORIGINAL-PATH?:PATH)%"
                          upstream: "%UPSTREAM_HOST%"
                          response_code: "%RESPONSE_CODE%"
                          bytes_rx: "%BYTES_RECEIVED%"
                          bytes_tx: "%BYTES_SENT%"
                          duration_ms: "%DURATION%"
                          zone: "zone1-update"
                          verdict: "%RESPONSE_CODE_DETAILS%"
                http_filters:
                  - name: envoy.filters.http.dynamic_forward_proxy
                    typed_config:
                      "@type": type.googleapis.com/envoy.extensions.filters.http.dynamic_forward_proxy.v3.FilterConfig
                      dns_cache_config:
                        name: dynamic_forward_proxy_cache
                        dns_lookup_family: V4_PREFERRED
                  - name: envoy.filters.http.router
                    typed_config:
                      "@type": type.googleapis.com/envoy.extensions.filters.http.router.v3.Router
                route_config:
                  name: zone1_update_routes
                  virtual_hosts:
                    - name: allowed_db_hosts
                      # Allowlisted vulnerability DB and package registry hosts.
                      # Add new hosts here via PR; change requires review (CIS SoCo).
                      domains:
                        - "github.com"
                        - "objects.githubusercontent.com"
                        - "codeload.github.com"
                        - "api.github.com"
                        - "osv.dev"
                        - "api.osv.dev"
                        - "nvd.nist.gov"
                        - "services.nvd.nist.gov"
                        - "pypi.org"
                        - "files.pythonhosted.org"
                        # Grype vulnerability DB (Anchore)
                        - "toolbox-data.anchore.io"
                        # Trivy DB (GitHub releases via Aquasecurity CDN)
                        - "ghcr.io"
                        - "pkg.dev"
                        # cosign TUF root (Sigstore)
                        - "tuf-repo-cdn.sigstore.dev"
                        - "rekor.sigstore.dev"
                        - "fulcio.sigstore.dev"
                      routes:
                        - match:
                            prefix: "/"
                          route:
                            cluster: dynamic_forward_proxy_cluster
                            timeout: 60s
                    - name: deny_all
                      domains:
                        - "*"
                      routes:
                        - match:
                            prefix: "/"
                          direct_response:
                            status: 403
                            body:
                              inline_string: |
                                ZONE1-UPDATE DENIED: destination not in allowlist.
                                Permitted hosts: github.com, osv.dev, nvd.nist.gov,
                                pypi.org, toolbox-data.anchore.io, ghcr.io, sigstore.dev.
                                To add a host, submit a PR to envoy-zone1-update.yaml.

  clusters:
    - name: dynamic_forward_proxy_cluster
      lb_policy: CLUSTER_PROVIDED
      cluster_type:
        name: envoy.clusters.dynamic_forward_proxy
        typed_config:
          "@type": type.googleapis.com/envoy.extensions.clusters.dynamic_forward_proxy.v3.ClusterConfig
          dns_cache_config:
            name: dynamic_forward_proxy_cache
            dns_lookup_family: V4_PREFERRED
```

---

### `skills/rainbow/config/envoy/envoy-zone2-active.yaml`

This file is a **template**. The `[[GENERATED_VIRTUAL_HOSTS]]` placeholder is replaced by the scope-to-Envoy translator at `--init-engagement` time. The deny-all catch-all is always present and always last.

The file checked into the repository must be a valid Envoy config with a restrictive default that blocks all traffic (empty allowlist) until `--init-engagement` runs. This prevents accidental unrestricted egress if the file is used without engagement initialization.

```yaml
# envoy-zone2-active.yaml
# Zone 2 Active Reconnaissance: deny-by-default egress proxy.
# This file is GENERATED by: jerry tool exec --init-engagement <scope.yaml>
# DO NOT EDIT MANUALLY during an engagement.
# The engagement scope YAML is the source of truth.
#
# Default state (pre-engagement-init): all traffic denied.
# After --init-engagement: target hosts from scope.authorized_targets are added.
#
# Connection logging: ALL connections logged (allowed and denied).
# Log destination: /var/log/envoy/access.log -> mounted to evidence volume.

admin:
  address:
    socket_address:
      address: 0.0.0.0
      port_value: 9901

static_resources:
  listeners:
    - name: egress_proxy
      address:
        socket_address:
          address: 0.0.0.0
          port_value: 3128
      filter_chains:
        - filters:
            - name: envoy.filters.network.http_connection_manager
              typed_config:
                "@type": type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager
                stat_prefix: zone2_active_egress
                upgrade_configs:
                  - upgrade_type: CONNECT
                access_log:
                  - name: envoy.access_loggers.file
                    typed_config:
                      "@type": type.googleapis.com/envoy.extensions.access_loggers.file.v3.FileAccessLog
                      # Evidence path: synced with engagement evidence directory
                      # by CLI at --init-engagement time (symlink or volume bind).
                      path: /var/log/envoy/access.log
                      log_format:
                        json_format:
                          ts: "%START_TIME%"
                          method: "%REQ(:METHOD)%"
                          authority: "%REQ(:AUTHORITY)%"
                          path: "%REQ(X-ENVOY-ORIGINAL-PATH?:PATH)%"
                          upstream: "%UPSTREAM_HOST%"
                          upstream_cluster: "%UPSTREAM_CLUSTER%"
                          response_code: "%RESPONSE_CODE%"
                          bytes_rx: "%BYTES_RECEIVED%"
                          bytes_tx: "%BYTES_SENT%"
                          duration_ms: "%DURATION%"
                          zone: "zone2-active"
                          verdict: "%RESPONSE_CODE_DETAILS%"
                          # Forensic fields for chain of custody
                          request_id: "%REQ(X-REQUEST-ID)%"
                          downstream_remote: "%DOWNSTREAM_REMOTE_ADDRESS%"
                http_filters:
                  - name: envoy.filters.http.dynamic_forward_proxy
                    typed_config:
                      "@type": type.googleapis.com/envoy.extensions.filters.http.dynamic_forward_proxy.v3.FilterConfig
                      dns_cache_config:
                        name: dynamic_forward_proxy_cache
                        dns_lookup_family: V4_PREFERRED
                  - name: envoy.filters.http.router
                    typed_config:
                      "@type": type.googleapis.com/envoy.extensions.filters.http.router.v3.Router
                route_config:
                  name: zone2_active_routes
                  virtual_hosts:
                    # --- ENGAGEMENT SCOPE TARGETS (generated by --init-engagement) ---
                    # Placeholder: replaced by scope-to-Envoy translator.
                    # Format: one virtual_host entry per authorized target domain.
                    # DEFAULT (pre-init): empty -- no targets authorized.
                    # [[GENERATED_VIRTUAL_HOSTS]]
                    # --- END GENERATED TARGETS ---
                    - name: deny_all
                      domains:
                        - "*"
                      routes:
                        - match:
                            prefix: "/"
                          direct_response:
                            status: 403
                            body:
                              inline_string: |
                                ZONE2-ACTIVE DENIED: destination not in engagement scope.
                                Run: jerry tool exec --init-engagement <scope.yaml>
                                to generate allowlist from engagement scope document.
                                Engagement scope is the source of truth for authorized targets.

  clusters:
    - name: dynamic_forward_proxy_cluster
      lb_policy: CLUSTER_PROVIDED
      cluster_type:
        name: envoy.clusters.dynamic_forward_proxy
        typed_config:
          "@type": type.googleapis.com/envoy.extensions.clusters.dynamic_forward_proxy.v3.ClusterConfig
          dns_cache_config:
            name: dynamic_forward_proxy_cache
            dns_lookup_family: V4_PREFERRED
```

---

### `skills/rainbow/config/envoy/envoy-zone3-exploit.yaml`

Zone 3 extends Zone 2 with:
1. C2 infrastructure IPs (added from engagement scope `c2_infrastructure` field).
2. Full request/response header logging for credential scrubbing detection.
3. Optional TLS MITM capability (documented below; not enabled by default).

```yaml
# envoy-zone3-exploit.yaml
# Zone 3 Exploitation: deny-by-default egress proxy.
# This file is GENERATED by: jerry tool exec --init-engagement <scope.yaml>
# C2 infrastructure IPs are added from scope.c2_infrastructure (if present).
#
# Connection logging: ALL connections logged with full request headers.
# Log destination: /var/log/envoy/access.log -> evidence volume.
#
# TLS interception (MITM): NOT enabled by default.
# To enable: set ENVOY_Z3_MITM=true at --init-engagement time.
# Requires: CA cert injected into tool containers (trust anchor installation).
# Purpose: credential scrubbing in Zone 3 network traffic (defense in depth
#          with CLI credential filter which catches tool output credentials).

admin:
  address:
    socket_address:
      address: 0.0.0.0
      port_value: 9901

static_resources:
  listeners:
    - name: egress_proxy
      address:
        socket_address:
          address: 0.0.0.0
          port_value: 3128
      filter_chains:
        - filters:
            - name: envoy.filters.network.http_connection_manager
              typed_config:
                "@type": type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager
                stat_prefix: zone3_exploit_egress
                upgrade_configs:
                  - upgrade_type: CONNECT
                access_log:
                  - name: envoy.access_loggers.file
                    typed_config:
                      "@type": type.googleapis.com/envoy.extensions.access_loggers.file.v3.FileAccessLog
                      path: /var/log/envoy/access.log
                      log_format:
                        json_format:
                          ts: "%START_TIME%"
                          method: "%REQ(:METHOD)%"
                          authority: "%REQ(:AUTHORITY)%"
                          path: "%REQ(X-ENVOY-ORIGINAL-PATH?:PATH)%"
                          upstream: "%UPSTREAM_HOST%"
                          upstream_cluster: "%UPSTREAM_CLUSTER%"
                          response_code: "%RESPONSE_CODE%"
                          bytes_rx: "%BYTES_RECEIVED%"
                          bytes_tx: "%BYTES_SENT%"
                          duration_ms: "%DURATION%"
                          zone: "zone3-exploit"
                          verdict: "%RESPONSE_CODE_DETAILS%"
                          request_id: "%REQ(X-REQUEST-ID)%"
                          downstream_remote: "%DOWNSTREAM_REMOTE_ADDRESS%"
                          # Zone 3: log User-Agent and Authorization headers
                          # for credential detection (defense in depth with CLI filter).
                          user_agent: "%REQ(USER-AGENT)%"
                          # Note: Authorization header value is REDACTED in the
                          # credential-scrubbing pipeline; logged as presence indicator only.
                          auth_present: "%REQ(AUTHORIZATION)%"
                http_filters:
                  - name: envoy.filters.http.dynamic_forward_proxy
                    typed_config:
                      "@type": type.googleapis.com/envoy.extensions.filters.http.dynamic_forward_proxy.v3.FilterConfig
                      dns_cache_config:
                        name: dynamic_forward_proxy_cache
                        dns_lookup_family: V4_PREFERRED
                  - name: envoy.filters.http.router
                    typed_config:
                      "@type": type.googleapis.com/envoy.extensions.filters.http.router.v3.Router
                route_config:
                  name: zone3_exploit_routes
                  virtual_hosts:
                    # --- ENGAGEMENT SCOPE TARGETS (generated by --init-engagement) ---
                    # Includes: scope.authorized_targets (same as Zone 2)
                    # Plus:     scope.c2_infrastructure hosts (Zone 3 only)
                    # [[GENERATED_VIRTUAL_HOSTS]]
                    # --- END GENERATED TARGETS ---
                    - name: deny_all
                      domains:
                        - "*"
                      routes:
                        - match:
                            prefix: "/"
                          direct_response:
                            status: 403
                            body:
                              inline_string: |
                                ZONE3-EXPLOIT DENIED: destination not in engagement scope.
                                Authorized targets: scope.authorized_targets + scope.c2_infrastructure.
                                Run: jerry tool exec --init-engagement <scope.yaml>

  clusters:
    - name: dynamic_forward_proxy_cluster
      lb_policy: CLUSTER_PROVIDED
      cluster_type:
        name: envoy.clusters.dynamic_forward_proxy
        typed_config:
          "@type": type.googleapis.com/envoy.extensions.clusters.dynamic_forward_proxy.v3.ClusterConfig
          dns_cache_config:
            name: dynamic_forward_proxy_cache
            dns_lookup_family: V4_PREFERRED
```

---

## L1: Engagement-Scope-to-Envoy Translation

### Three Options Evaluated

#### Option 1: Static (Recommended for Phase 1)

`jerry tool exec --init-engagement <scope.yaml>` generates a complete per-engagement Envoy config from the scope YAML, writes it to `skills/rainbow/config/envoy/envoy-zone{2,3}-active.yaml`, and Envoy loads it on startup (or after hot restart).

**Translation logic (per engagement `authorized_targets` entry):**

```
authorized_targets entry -> Envoy virtual_host entry

type: domain, value: "example.com"
  -> domains: ["example.com", "*.example.com"]  (wildcard subdomains)

type: ip, value: "203.0.113.42"
  -> domains: ["203.0.113.42"]

type: ip_range, value: "203.0.113.0/24"
  -> CANNOT express as Envoy virtual_host domain match.
  -> Use a cluster with ORIGINAL_DST and an IP-based RBAC filter.
  -> See implementation note below.

type: url, value: "https://app.example.com/api"
  -> domains: ["app.example.com"]  (host extracted from URL)

type: cloud_account, value: "aws:123456789012"
  -> domains: ["*.amazonaws.com", "*.aws.amazon.com"] (cloud provider endpoint wildcards)
  -> This is a fixed mapping per cloud provider, not dynamic.

c2_infrastructure (Zone 3 only):
  -> Same domain/IP translation as authorized_targets.
```

**IP range handling (important):** Envoy virtual host domain matching does not support CIDR notation. For IP range targets, the translator must either:
- (a) Enumerate all IPs in the range and create individual entries (impractical for /16 ranges).
- (b) Use Envoy's RBAC filter at the network level for IP-based allow rules.
- **Recommendation:** Require `type: ip` (single IPs) or `type: domain` in scope for Zone 2/3 targets. Flag `type: ip_range` as requiring manual Envoy config and block `--init-engagement` for ip_range targets until the RBAC filter implementation is complete.

**Pros:** Simple. No running sidecar. Config is version-controlled per engagement. Envoy hot-restart on config change is deterministic.

**Cons:** Requires Envoy hot restart when scope changes mid-engagement. New code path (translator) is security-critical and needs test coverage.

**Implementation location:** `src/tool_exec/infrastructure/envoy/scope_translator.py`

---

#### Option 2: Dynamic (xDS API sidecar)

A small Python or Go sidecar serves the Envoy xDS API. Envoy polls the sidecar for config updates. The sidecar reads the scope YAML and generates xDS clusters/routes dynamically.

**Pros:** Config updates take effect without Envoy restart. Elegant for mid-engagement scope changes.

**Cons:** Adds a running sidecar process (new attack surface). xDS API is complex to implement correctly. Overkill for the current engagement model where scope changes require human re-approval anyway. The sidecar itself is a new security-critical component.

**Verdict:** Rejected for Phase 1. Consider for Phase 3 when engagement scope hot-update (without full restart) becomes a requirement.

---

#### Option 3: Hybrid (Static + Reload Script)

Static config generation (Option 1) + a `reload.sh` script that sends `kill -HUP` to the Envoy process (or calls `envoy --mode validate && kill -USR2` for hot restart) after scope updates.

**Pros:** No sidecar. Handles mid-engagement scope changes without full `docker compose restart`.

**Cons:** `kill -HUP` behavior in Docker containers can be fragile (PID 1 vs. child process). Hot restart (`-USR2`) requires Envoy to be the init process or managed by a process supervisor.

**Verdict:** Use as Phase 1.5 enhancement after Option 1 is stable. The hot-restart mechanism is documented in Envoy's admin API (`POST /quitquitquit` + restart, or `POST /drain_listeners`).

---

### Recommendation: Option 1 (Static Generation)

**Implementation spec for `src/tool_exec/infrastructure/envoy/scope_translator.py`:**

```python
# Public interface (H-11 compliant: type hints + docstring required)

from pathlib import Path
from src.tool_exec.domain.entities.engagement_scope import EngagementScope

def translate_scope_to_envoy_config(
    scope: EngagementScope,
    zone: int,
    template_path: Path,
    output_path: Path,
) -> None:
    """
    Generate an Envoy virtual host allowlist from an engagement scope document.

    Reads the zone-specific Envoy config template, replaces the
    [[GENERATED_VIRTUAL_HOSTS]] placeholder with virtual_host entries
    derived from scope.authorized_targets (and scope.c2_infrastructure
    for zone 3), and writes the result to output_path.

    Validates the generated config with `envoy --mode validate` before writing.

    Args:
        scope: Parsed and validated engagement scope.
        zone: Target zone (2 or 3). Zone 3 includes c2_infrastructure hosts.
        template_path: Path to the zone-specific Envoy config template.
        output_path: Destination path for the generated config.

    Raises:
        EnvoyConfigGenerationError: If the generated config fails Envoy validation.
        ScopeTranslationError: If a scope target type cannot be translated.
        UnsupportedTargetTypeError: If scope contains ip_range targets
            (not yet supported; requires RBAC filter implementation).
    """
```

**Test requirements (H-20 compliance):**
- Unit tests: `tests/unit/tool_exec/test_scope_translator.py`
  - Domain target translation (wildcard subdomain generation)
  - IP target translation
  - URL target translation (hostname extraction)
  - Cloud account target translation (AWS, GCP, Azure endpoint wildcards)
  - ip_range target raises `UnsupportedTargetTypeError`
  - Zone 3 includes c2_infrastructure; Zone 2 excludes it
  - Template placeholder replacement produces valid YAML
  - Envoy config validation subprocess call
- Integration tests: `tests/integration/test_scope_translator_integration.py`
  - Generated config loads in a real Envoy container
  - Allowlisted host returns 200; non-allowlisted host returns 403

---

## L1: E2E Validation Tests

All tests live in: `skills/rainbow/tests/docker/test-envoy-proxy.sh`

The test script uses the same `docker compose` invocation pattern as the existing `test-tool-exec.sh`.

### Test Matrix

#### Group 1: Zone 1 Offline Isolation

```bash
# TC-E2E-001: Zone 1 offline container cannot reach the internet
# Service: scanner (syft), network: zone1-offline (internal: true)
# Expected: connection refused or network unreachable (not 200)
test_zone1_offline_no_internet() {
  result=$(docker compose -f skills/rainbow-supply-chain/tests/docker/docker-compose.yml \
    exec -T scanner \
    curl --connect-timeout 5 --max-time 10 -sf http://httpbin.org/get 2>&1)
  # Should fail: no route to host
  assert_not_contains "$result" '"url"'
  assert_contains "$result" "Could not resolve host\|Network unreachable\|Connection refused\|curl: (6)\|curl: (7)"
}

# TC-E2E-002: Zone 1 offline -- DNS resolution also blocked
test_zone1_offline_dns_blocked() {
  result=$(docker compose -f skills/rainbow-supply-chain/tests/docker/docker-compose.yml \
    exec -T scanner \
    nslookup httpbin.org 2>&1 || true)
  # DNS may resolve via Docker's embedded resolver even on internal: true
  # But TCP connection to resolved IP must fail.
  tcp_result=$(docker compose -f skills/rainbow-supply-chain/tests/docker/docker-compose.yml \
    exec -T scanner \
    curl --connect-timeout 5 -sf http://93.184.216.34/ 2>&1 || true)
  assert_not_contains "$tcp_result" "200"
}
```

#### Group 2: Zone 1 DB-Update Allowlist Enforcement

```bash
# TC-E2E-003: Zone 1 DB-update CAN reach github.com
test_zone1_update_allows_github() {
  result=$(docker compose -f skills/rainbow-supply-chain/tests/docker/docker-compose.yml \
    exec -T scanner-net \
    curl --connect-timeout 10 --max-time 30 -sf \
    --proxy http://envoy-z1-update:3128 \
    https://api.github.com/zen 2>&1)
  assert_contains "$result" "."  # Any response body means github.com is reachable
}

# TC-E2E-004: Zone 1 DB-update CANNOT reach arbitrary internet hosts
test_zone1_update_denies_arbitrary() {
  result=$(docker compose -f skills/rainbow-supply-chain/tests/docker/docker-compose.yml \
    exec -T scanner-net \
    curl --connect-timeout 10 --max-time 15 -sf -o /dev/null -w "%{http_code}" \
    --proxy http://envoy-z1-update:3128 \
    http://httpbin.org/get 2>&1)
  assert_equals "$result" "403"
}

# TC-E2E-005: Zone 1 DB-update allows osv.dev
test_zone1_update_allows_osv() {
  result=$(docker compose -f skills/rainbow-supply-chain/tests/docker/docker-compose.yml \
    exec -T scanner-net \
    curl --connect-timeout 10 --max-time 30 -sf \
    --proxy http://envoy-z1-update:3128 \
    https://api.osv.dev/v1/vulns/OSV-2020-1 2>&1)
  assert_contains "$result" "id"
}

# TC-E2E-006: Zone 1 DB-update allows nvd.nist.gov
test_zone1_update_allows_nvd() {
  result=$(docker compose -f skills/rainbow-supply-chain/tests/docker/docker-compose.yml \
    exec -T scanner-net \
    curl --connect-timeout 10 --max-time 30 -sf -o /dev/null -w "%{http_code}" \
    --proxy http://envoy-z1-update:3128 \
    https://nvd.nist.gov/vuln/detail/CVE-2021-44228 2>&1)
  # NVD returns 200 for known CVEs
  assert_equals "$result" "200"
}
```

#### Group 3: Zone 2 Scope Enforcement

```bash
# TC-E2E-007: Zone 2 can reach engagement-scope targets
# Prerequisite: --init-engagement run with scope containing testphp.vulnweb.com
test_zone2_allows_scope_target() {
  # Use a known test/training target safe for inclusion in test scope
  result=$(docker compose -f skills/rainbow-recon/tests/docker/docker-compose.yml \
    exec -T recon-pipeline \
    curl --connect-timeout 10 --max-time 30 -sf -o /dev/null -w "%{http_code}" \
    http://testphp.vulnweb.com/ 2>&1)
  # If scope contains testphp.vulnweb.com, returns 200; otherwise 403
  assert_equals "$result" "200"
}

# TC-E2E-008: Zone 2 CANNOT reach non-scope hosts
test_zone2_denies_non_scope() {
  result=$(docker compose -f skills/rainbow-recon/tests/docker/docker-compose.yml \
    exec -T recon-pipeline \
    curl --connect-timeout 10 --max-time 15 -sf -o /dev/null -w "%{http_code}" \
    http://example.com/ 2>&1)
  # example.com is not in test engagement scope
  assert_equals "$result" "403"
}

# TC-E2E-009: Zone 2 direct internet bypass is blocked (no proxy env var path)
test_zone2_no_direct_bypass() {
  # Clear proxy env vars and try direct connection; should fail due to internal: true
  result=$(docker compose -f skills/rainbow-recon/tests/docker/docker-compose.yml \
    exec -T -e HTTP_PROXY="" -e HTTPS_PROXY="" recon-pipeline \
    curl --connect-timeout 5 --max-time 10 -sf http://httpbin.org/get 2>&1)
  # Should fail: no route to host (internal: true has no external route)
  assert_not_contains "$result" '"url"'
}
```

#### Group 4: Zone 3 Logging

```bash
# TC-E2E-010: Zone 3 Envoy logs the connection
test_zone3_envoy_logs_connection() {
  # Make a request through Zone 3 proxy to a scope-allowlisted target
  docker compose -f skills/rainbow-exploit/tests/docker/docker-compose.yml \
    exec -T exploit-ops \
    curl --connect-timeout 10 --max-time 15 -sf -o /dev/null \
    http://testphp.vulnweb.com/ 2>&1 || true

  # Check Envoy access log for the request
  log_entry=$(docker compose -f skills/rainbow-exploit/tests/docker/docker-compose.yml \
    exec -T envoy-z3 \
    cat /var/log/envoy/access.log | tail -5)
  assert_contains "$log_entry" "testphp.vulnweb.com"
  assert_contains "$log_entry" '"zone":"zone3-exploit"'
}
```

#### Group 5: Proxy Bypass Regression (Tool Without Proxy Env Vars)

```bash
# TC-E2E-011: Tool without proxy env vars falls back to direct (blocked by internal: true)
# This validates that the network-level enforcement is not solely dependent on
# tools respecting HTTP_PROXY.
test_direct_access_blocked_without_proxy() {
  # Run a temporary container on zone2-active without proxy env vars
  result=$(docker run --rm \
    --network "$(docker compose -f skills/rainbow-recon/tests/docker/docker-compose.yml \
      ps -q recon-pipeline | head -1 | xargs docker inspect --format '{{range .NetworkSettings.Networks}}{{.NetworkID}}{{end}}')" \
    alpine:latest \
    curl --connect-timeout 5 --max-time 10 -sf http://httpbin.org/get 2>&1 || true)
  # Must fail: zone2-active is internal: true
  assert_not_contains "$result" '"url"'
}
```

### Test Runner

```bash
# skills/rainbow/tests/docker/test-envoy-proxy.sh
# Run: bash skills/rainbow/tests/docker/test-envoy-proxy.sh

set -euo pipefail
PASS=0; FAIL=0

assert_contains() { [[ "$1" == *"$2"* ]] && ((PASS++)) || { echo "FAIL: expected '$2' in '$1'"; ((FAIL++)); }; }
assert_not_contains() { [[ "$1" != *"$2"* ]] && ((PASS++)) || { echo "FAIL: unexpected '$2' in '$1'"; ((FAIL++)); }; }
assert_equals() { [[ "$1" == "$2" ]] && ((PASS++)) || { echo "FAIL: expected '$2' got '$1'"; ((FAIL++)); }; }

# Source test functions defined above...
# Run all test groups...
# Report results

echo "Results: ${PASS} passed, ${FAIL} failed"
[[ $FAIL -eq 0 ]]
```

---

## L1: Effort Estimates

Total estimate: **68-88 hours** (conservative range accounting for Envoy config debugging and test environment setup).

### Task Breakdown

| Task ID | Task | Hours | Notes |
|---------|------|-------|-------|
| TASK-ENV-001 | Envoy base image and Dockerfile | 4h | Use `envoyproxy/envoy:v1.31-latest`; create thin wrapper image pinned to digest; non-root user; read-only filesystem. |
| TASK-ENV-002 | `envoy-zone1-update.yaml` -- static allowlist config | 6h | Config + local validation with `envoy --mode validate`. Include: test against real DB endpoints (grype pull, trivy pull, osv-scanner). |
| TASK-ENV-003 | `envoy-zone2-active.yaml` -- template config | 4h | Template with placeholder. Default-deny stub. Validate with `envoy --mode validate`. |
| TASK-ENV-004 | `envoy-zone3-exploit.yaml` -- template config + logging | 6h | Zone 3 header logging. Optional MITM capability (document but don't enable). Validate. |
| TASK-ENV-005 | Compose changes: `rainbow-supply-chain` | 4h | Network split, service split (scanner/scanner-net), Envoy service, healthcheck, depends_on. |
| TASK-ENV-006 | Compose changes: `blue-team` | 4h | Same pattern as supply-chain. compliance/compliance-net split. |
| TASK-ENV-007 | Compose changes: `rainbow-recon` | 3h | Replace existing cloud-net with zone2-active + zone2-egress. Envoy service. |
| TASK-ENV-008 | Compose changes: `rainbow-cloud` | 3h | Same as recon. Cloud API endpoints in allowlist generation. |
| TASK-ENV-009 | Compose changes: `rainbow-exploit` | 5h | Three-network topology (zone3-exploit, zone3-egress, msf-internal). postgres isolation. |
| TASK-ENV-010 | Compose changes: `rainbow-runtime` | 4h | Two Envoy instances (zone2 + zone3). Service network assignment. |
| TASK-ENV-011 | `scope_translator.py` -- scope-to-Envoy config generator | 10h | Port: `ScopeTranslationPort`. Adapter: static YAML generation. Domain: target type mapping. Envoy validation subprocess call. Error types. |
| TASK-ENV-012 | Unit tests for `scope_translator.py` | 8h | H-20 compliance (90% line coverage). Test all target types. Test zone 2 vs zone 3 output. Test error conditions. |
| TASK-ENV-013 | `--init-engagement` CLI command | 5h | Reads scope YAML, calls translator, writes configs, validates Envoy config, reports outcome. |
| TASK-ENV-014 | `tool-exec.yaml` service mapping updates | 2h | grype->scanner-net, osv-scanner->scanner-net, trivy->compliance-net. Validate tool resolution. |
| TASK-ENV-015 | E2E proxy validation test script | 8h | All 11 TCs in Section 4. CI fixture scope (testphp.vulnweb.com for Zone 2 tests). |
| TASK-ENV-016 | CI pipeline updates | 4h | `.github/workflows/proj023-ci.yml`: add Envoy test job. Pre-generate Zone 2/3 configs from CI fixture scope before running E2E tests. |
| TASK-ENV-017 | Envoy log collection in evidence pipeline | 4h | Volume mount to `work/engagements/<id>/evidence/envoy/`. SHA-256 hash on log rotation. |
| TASK-ENV-018 | Developer documentation | 3h | `skills/rainbow/docs/envoy-proxy-guide.md`: how to debug 403s, how to update Zone 1 allowlist, how to run --init-engagement. |

**Critical path:** TASK-ENV-001 -> ENV-002 -> ENV-005 -> ENV-014 -> ENV-015 (unblocked by scope translator).
**Secondary path:** ENV-003 -> ENV-011 -> ENV-012 -> ENV-013 -> ENV-015.

---

## L1: Raw TCP Tool Handling

### The Problem

`HTTP_PROXY` and `HTTPS_PROXY` are environment variables that only affect tools which implement the proxy protocol in their HTTP/HTTPS client library. Tools that bypass the HTTP stack and make raw TCP/UDP connections do not respect these variables.

**Affected tools in the Rainbow framework:**

| Tool | Protocol | Zone | Bypass Type |
|------|----------|------|-------------|
| `impacket-*` | SMB (TCP 445), LDAP (TCP 389/636), Kerberos (TCP 88), DCE-RPC | Zone 3 | Raw TCP socket |
| `pwntools`/`pwn` | Raw TCP/UDP (arbitrary) | Zone 3 | Raw socket |
| `donut` | Shellcode injection (local) | Zone 3 | Local; no network egress |
| `naabu` | TCP SYN port scanning | Zone 2 | Raw socket (libpcap) |
| `dnsx` | DNS UDP/TCP (port 53) | Zone 2 | Raw DNS socket |

### Network-Level Containment (Already in Place)

The `internal: true` network topology is the primary mitigation for raw TCP tools. Because no container on `zone2-active` or `zone3-exploit` has an external route (only `envoy-z2` / `envoy-z3` are connected to egress networks), raw TCP connections to non-container destinations CANNOT complete. The connection attempt will fail at the Docker network layer -- not at the proxy layer, but at the IP routing layer. This is structural enforcement, not behavioral.

**What raw TCP tools CAN do on `internal: true` networks:**
- Connect to other containers on the same network (e.g., `exploit-ops` to `exploit-c2` for tool chaining).
- Connect to the Envoy proxy container itself (Envoy is on the same network).

**What raw TCP tools CANNOT do:**
- Connect to any IP outside the Docker bridge subnet. The `internal: true` flag removes the default route from the bridge, so packets destined for external IPs have no route and are dropped.

**Exception -- DNS resolution:** Docker's embedded DNS resolver (`127.0.0.11`) is reachable from all containers regardless of `internal: true` setting. This means `dnsx` can resolve hostnames, but cannot TCP-connect to the resolved IPs (no external route). For subdomain enumeration, DNS resolution is the goal -- the inability to TCP-connect to findings is acceptable.

### Option A: Transparent Proxy via Container-Level iptables REDIRECT

**How it works:**
The `exploit-ops` container's init script adds iptables rules to redirect raw TCP connections to Envoy's TCP proxy port. This operates inside the container's network namespace (not the host's), so it works on macOS Docker Desktop without elevated host privileges.

```bash
# entrypoint snippet for exploit-ops (APPROACH A -- PHASE 2)
# Requires: NET_ADMIN capability on exploit-ops container.
# Add to exploit-ops service in compose:
#   cap_add:
#     - NET_ADMIN

# Redirect all TCP traffic not bound for internal containers to Envoy TCP proxy
iptables -t nat -A OUTPUT -p tcp \
  ! -d 172.16.0.0/12 \   # Exclude Docker bridge subnets
  -j REDIRECT --to-port 10001   # Envoy TCP proxy listener on port 10001

# Envoy Zone 3 TCP proxy listener (to add to envoy-zone3-exploit.yaml):
# listeners:
#   - name: tcp_transparent_proxy
#     address:
#       socket_address:
#         address: 0.0.0.0
#         port_value: 10001
#     filter_chains:
#       - filters:
#           - name: envoy.filters.network.tcp_proxy
#             typed_config:
#               "@type": type.googleapis.com/envoy.extensions.filters.network.tcp_proxy.v3.TcpProxy
#               stat_prefix: zone3_tcp_transparent
#               cluster: dynamic_forward_proxy_cluster
#               access_log: [...]
```

**Pros:** Raw TCP tools are proxied and logged.
**Cons:** Requires `NET_ADMIN` capability on `exploit-ops` (capability escalation); less safe. Transparent proxy for non-HTTP protocols (SMB, Kerberos) requires Envoy to support the protocol or act as a TCP pass-through (CONNECT tunnel). Connection metadata is logged, but payload is not inspected for these protocols.

### Option B: Accept Bypass, Document as Known Gap (Recommended for Phase 1)

Accept that Impacket, pwntools, and naabu bypass `HTTP_PROXY`. Document the boundary explicitly:

**Mitigation already in place:** `internal: true` network prevents these tools from reaching any IP outside the Docker bridge subnet. A compromised Impacket binary cannot reach an attacker-controlled exfiltration endpoint because the Docker network has no external route. The gap is that Impacket connections to **engagement targets** are not proxied (and therefore not logged in Envoy access logs).

**Evidence gap:** Zone 3 forensic evidence for raw TCP connections (Impacket SMB, Kerberos) will be missing from Envoy logs. Tool output (captured via volume mount + credential filter pipeline) remains the evidence source for these protocols.

**Future mitigation:** Tool-output-level logging (already implemented via evidence persistence pipeline) captures Impacket stdout/stderr. This is less complete than network-level logging but sufficient for Phase 1.

### Recommendation

**Phase 1:** Option B. Accept the bypass. Document the known gap in Zone 3 evidence quality for raw TCP tools. The `internal: true` network provides structural containment (cannot reach unauthorized destinations). The CLI's credential filter and evidence persistence pipeline provide tool-output-level logging.

**Phase 2:** Implement Option A for Zone 3 `exploit-ops` only. Scope to that specific service (Impacket is the primary concern). Add `NET_ADMIN` capability to `exploit-ops`. Add TCP transparent proxy listener to `envoy-zone3-exploit.yaml`. Track as TASK-ENV-019.

**Design note:** Do not add `NET_ADMIN` to Zone 2 containers (recon-pipeline). The port scanner `naabu` uses raw sockets for SYN scanning of engagement targets -- that is its legitimate function. Logging every SYN packet would produce noise with limited forensic value. The engagement scope (which must include target IPs before `naabu` runs) provides the authorization record. DNS bypass in `dnsx` is also acceptable for Zone 2 subdomain enumeration.

---

## L2: Strategic Implications

### Supply Chain Risk Landscape

| Component | Risk | Severity | Mitigation |
|-----------|------|----------|-----------|
| `envoyproxy/envoy:v1.31-latest` | Mutable tag; upstream compromise | HIGH | Pin to digest for production: `envoyproxy/envoy@sha256:<digest>`. Rotate on CVE advisories via Trivy. SBOM generation via Syft before each engagement. |
| Scope-to-Envoy translator | Security-critical new code; misconfigurations allow unauthorized egress | HIGH | 90% test coverage (H-20). Mutation testing for allowlist generation. Code review as C3 deliverable (AE-005). |
| Zone 2/3 Envoy configs (generated) | Generated file in repo; could be overwritten with permissive config | MEDIUM | CI gate validates generated configs before PR merge. `.gitignore` for engagement-specific configs; only templates committed. |
| Grype/Trivy DB from GitHub releases | DB integrity: could be tampered if GitHub releases are compromised | MEDIUM | Grype verifies DB with cosign signatures. Trivy uses GHCR OCI artifacts with cosign attestations. Zone 1 allowlist includes sigstore.dev for verification. |
| mitmproxy as Zone 2 MITM tool | mitmproxy intercepts TLS; CA cert is a trust anchor | HIGH (operational) | CA cert scoped to engagement containers only. Cert stored in evidence dir, not system trust store. Destroyed at engagement close per `engagement_lifecycle.md`. |

### SLSA Maturity Roadmap

**Current state (post-implementation):** SLSA Level 1.5 (informal)
- Build process documented (Dockerfiles, compose files, this plan).
- No signed provenance for Envoy config files.
- No hermetic build for tool container images.

**Target state (6 months):** SLSA Level 2
- Signed provenance for all Docker images built in CI (`cosign attest`).
- Envoy config changes trigger CI validation (Envoy --mode validate gate).
- SBOM generated for all tool images via Syft (already tooled in rainbow-supply-chain).
- Pinned image digests for all compose services (Envoy, postgres, tool images).

**Target state (12 months):** SLSA Level 3
- Hardened CI build platform (GitHub Actions with SLSA provenance generator action).
- Non-falsifiable provenance for all compose service images.
- Two-party review for changes to Zone 1 allowlist and Envoy configs (AE-005 C3 enforcement already in place).

### Infrastructure Security Evolution Path

```
Phase 1 (this plan):
  Option D Forward Proxy -- HTTP/HTTPS tools proxied.
  Raw TCP tools contained by internal: true but not proxied.
  Static scope-to-Envoy translation at engagement init.

Phase 2 (3-6 months):
  Transparent TCP proxy for Zone 3 exploit-ops (NET_ADMIN).
  Envoy hot-restart for mid-engagement scope updates.
  Envoy admin API metrics -> engagement evidence (bytes, connections by destination).

Phase 3 (6-12 months):
  xDS sidecar for dynamic scope updates.
  Per-operation Envoy config toggle via CLI (without container restart).
  Envoy WASM filter for credential scrubbing in network traffic (replaces auth_present logging).
```

### Vendor Dependency Risk Assessment

| Vendor | Product | Risk Category | Assessment |
|--------|---------|---------------|-----------|
| Envoy Proxy (CNCF) | envoy | Critical infrastructure | Low vendor risk. CNCF graduated project. Google, Lyft, AWS as primary contributors. Active CVE response track record. Primary risk is configuration complexity. |
| Docker Inc. / Moby | Docker Engine | Critical infrastructure | Medium risk (Docker Desktop licensing changes). Mitigated by Compose spec compatibility with Podman Compose, Finch (AWS), and OrbStack as alternatives. All compose files use standard Compose spec features. |
| Aqua Security | Trivy | Tool dependency | Low risk. Trivy is MIT licensed. DB hosted on GitHub and GHCR. Alternative: Grype for overlapping vulnerability coverage. |
| Anchore | Grype, Syft | Tool dependency | Low risk. Apache 2.0 licensed. DB hosted on toolbox-data.anchore.io (CDN-backed). Syft is used for SBOM generation in supply-chain workflow. |

---

*Confidence: HIGH for per-compose-file changes and Envoy Zone 1 config (well-understood Envoy forward proxy pattern). MEDIUM for Zone 2/3 dynamic config generation (scope translator is new code; Envoy dynamic forward proxy filter behavior under edge cases requires integration testing). LOW for Zone 3 MITM capability (TLS interception adds significant operational complexity; deferred to Phase 2 with explicit opt-in).*

*Validation required: All Envoy configs MUST pass `envoy --mode validate` before use. All compose changes MUST be tested with `docker compose config` (syntax validation) and the E2E test suite (behavioral validation). Checkov scan of compose files REQUIRED before merging (CIS Docker benchmark checks).*
