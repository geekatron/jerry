# Tool CLI Patterns and Exchange Schemas

> Reference documentation for all tools used by the `/rainbow` and `/blue-team` skills, including CLI patterns, version constraints, and security zone assignments. Also documents the four cross-skill exchange envelope schemas (RBEE, CFE, DGE, Emulation Manifest) with required field specifications.

## Document Sections

| Section | Purpose |
|---------|---------|
| [CLI Pattern Format](#cli-pattern-format) | Column definitions for CLI pattern entries |
| [/rainbow-supply-chain Tools](#rainbow-supply-chain-tools) | Syft, Grype, Trivy, OSV-Scanner, Checkov, Cosign, Snyk CLI |
| [/rainbow-recon Tools](#rainbow-recon-tools) | Subfinder, httpx, dnsx, Naabu, Katana, Nuclei (Tier A); Amass, Maigret (Tier B) |
| [/rainbow-cloud Tools](#rainbow-cloud-tools) | Checkov, Prowler, Kubescape, Kyverno, Cartography |
| [/rainbow-exploit Tools](#rainbow-exploit-tools) | pwntools, Impacket, Donut, Empire, Mythic, BloodHound CE, Metasploit |
| [/rainbow-runtime Tools](#rainbow-runtime-tools) | mitmproxy suite, Frida suite |
| [/blue-team Tools](#blue-team-tools) | Tier A (11), Tier B (7), Tier C (10 — methodology only) |
| [Exchange Schemas](#exchange-schemas) | RBEE, CFE, DGE, Emulation Manifest |
| -- [RBEE v1](#rbee-v1-red-blue-exchange-envelope) | Red-to-Blue findings transfer |
| -- [CFE v1](#cfe-v1-coverage-feedback-envelope) | Blue-to-Red coverage feedback |
| -- [DGE v1](#dge-v1-d3fend-gap-envelope) | Blue-to-Red D3FEND gap analysis |
| -- [Emulation Manifest v1](#emulation-manifest-v1) | Purple team exercise control |

---

## CLI Pattern Format

Each tool entry specifies the following fields.

| Field | Description |
|-------|-------------|
| **Tool** | Tool name and minimum version. |
| **Agent** | Agent(s) that invoke this tool. |
| **Security zone** | Minimum zone required to invoke this tool. |
| **Primary CLI pattern** | Representative CLI invocation showing required arguments. |
| **Output format** | Default output format produced by the tool. |
| **Notes** | Version constraints, zone promotion conditions, or behavioral exceptions. |

---

## /rainbow-supply-chain Tools

### Syft

| Field | Value |
|-------|-------|
| **Tool** | Syft >= 1.0 |
| **Agent** | `rainbow-sc-scanner` |
| **Security zone** | Zone 1 |
| **Primary CLI pattern** | `syft <image-or-dir> -o syft-json=sbom.json` |
| **Output format** | JSON (syft-json schema), CycloneDX JSON, SPDX JSON |
| **Notes** | Operates on local files and images only. No network contact required for SBOM generation. |

### Grype

| Field | Value |
|-------|-------|
| **Tool** | Grype >= 0.74 |
| **Agent** | `rainbow-sc-scanner` |
| **Security zone** | Zone 1 |
| **Primary CLI pattern** | `grype sbom:sbom.json -o json --file grype-results.json` |
| **Output format** | JSON with vulnerability match records |
| **Notes** | Grype fetches the vulnerability database on first run (network required for DB update, not for scan execution). Pass `--db-only` to update only the local DB. |

### Trivy (supply chain)

| Field | Value |
|-------|-------|
| **Tool** | Trivy >= 0.50 |
| **Agent** | `rainbow-sc-scanner`, `rainbow-sc-verifier` |
| **Security zone** | Zone 1 |
| **Primary CLI pattern** | `trivy image --format json --output trivy-results.json <image>` |
| **Output format** | JSON |
| **Notes** | Also used by /blue-team (blue-comply). Supply chain usage is Zone 1. Live registry scans are Zone 2. |

### OSV-Scanner

| Field | Value |
|-------|-------|
| **Tool** | OSV-Scanner >= 2.0 |
| **Agent** | `rainbow-sc-scanner` |
| **Security zone** | Zone 1 |
| **Primary CLI pattern** | `osv-scanner scan --format json --output osv-results.json <dir-or-lockfile>` |
| **Output format** | JSON |
| **Notes** | Queries the OSV database (network required). Operates on dependency manifests and lock files. |

### Checkov (supply chain)

| Field | Value |
|-------|-------|
| **Tool** | Checkov >= 3.0 |
| **Agent** | `rainbow-sc-scanner` |
| **Security zone** | Zone 1 |
| **Primary CLI pattern** | `checkov -d <dir> --framework dockerfile,terraform --output json` |
| **Output format** | JSON |
| **Notes** | Also used by /rainbow-cloud and /blue-team. Supply chain usage targets Dockerfile and IaC files. |

### Cosign

| Field | Value |
|-------|-------|
| **Tool** | Cosign >= 2.2 |
| **Agent** | `rainbow-sc-verifier` |
| **Security zone** | Zone 1 / Zone 2 |
| **Primary CLI pattern** | `cosign verify --certificate-identity=<id> --certificate-oidc-issuer=<issuer> <image>` |
| **Output format** | JSON (signed payload and certificate chain) |
| **Notes** | Zone 1 for local artifact verification. Zone 2 when contacting a remote registry. |

### Snyk CLI

| Field | Value |
|-------|-------|
| **Tool** | Snyk CLI (Latest) |
| **Agent** | `rainbow-sc-scanner` |
| **Security zone** | Zone 1 |
| **Primary CLI pattern** | `snyk test --json --file=<manifest> > snyk-results.json` |
| **Output format** | JSON |
| **Notes** | Requires `SNYK_TOKEN` environment variable. Contacts Snyk API for vulnerability data (network required). |

---

## /rainbow-recon Tools

### Tier A Tools

#### Subfinder

| Field | Value |
|-------|-------|
| **Tool** | Subfinder >= 2.6 |
| **Agent** | `rainbow-recon-pipeline` |
| **Security zone** | Zone 2 |
| **Primary CLI pattern** | `subfinder -d <domain> -o subdomains.txt -oJ` |
| **Output format** | Text (one subdomain per line) or JSON with `-oJ` |
| **Notes** | Active DNS enumeration. Engagement scope required before invocation. |

#### httpx

| Field | Value |
|-------|-------|
| **Tool** | httpx >= 1.6 |
| **Agent** | `rainbow-recon-pipeline` |
| **Security zone** | Zone 2 |
| **Primary CLI pattern** | `httpx -l subdomains.txt -o live-hosts.txt -status-code -title -json` |
| **Output format** | JSON (one record per line) |
| **Notes** | HTTP probing sends requests to in-scope hosts. |

#### dnsx

| Field | Value |
|-------|-------|
| **Tool** | dnsx >= 1.2 |
| **Agent** | `rainbow-recon-pipeline` |
| **Security zone** | Zone 2 |
| **Primary CLI pattern** | `dnsx -l subdomains.txt -a -cname -resp -json -o dns-records.json` |
| **Output format** | JSON |
| **Notes** | DNS resolution sends queries to authoritative servers for in-scope domains. |

#### Naabu

| Field | Value |
|-------|-------|
| **Tool** | Naabu >= 2.4 |
| **Agent** | `rainbow-recon-pipeline` |
| **Security zone** | Zone 2 |
| **Primary CLI pattern** | `naabu -l live-hosts.txt -p 80,443,8080,8443 -o open-ports.txt -json` |
| **Output format** | JSON |
| **Notes** | Port scanning contacts in-scope hosts. Zone 2 minimum. |

#### Katana

| Field | Value |
|-------|-------|
| **Tool** | Katana >= 1.0 |
| **Agent** | `rainbow-recon-pipeline` |
| **Security zone** | Zone 2 |
| **Primary CLI pattern** | `katana -u <url> -d 3 -o crawl-output.txt -jc` |
| **Output format** | Text (one URL per line) or JSON with `-jc` |
| **Notes** | Web crawling makes HTTP requests to in-scope web applications. |

#### Nuclei

| Field | Value |
|-------|-------|
| **Tool** | Nuclei >= 3.0 |
| **Agent** | `rainbow-recon-pipeline` |
| **Security zone** | Zone 2 (detection templates) / Zone 3 (exploit templates) |
| **Primary CLI pattern** | `nuclei -l live-hosts.txt -t <template-path> -o nuclei-results.txt -json` |
| **Output format** | JSON |
| **Notes** | Detection-category templates are Zone 2. Templates in the `exploits/` category require Zone 3 authorization. Template category is visible in the template's `tags` field. |

---

### Tier B Tools

#### OWASP Amass

| Field | Value |
|-------|-------|
| **Tool** | OWASP Amass >= 4.2 |
| **Agent** | `rainbow-recon-osint` |
| **Security zone** | Zone 2 |
| **Primary CLI pattern** | `amass enum -d <domain> -o amass-output.txt -json amass-results.json` |
| **Output format** | JSON |
| **Notes** | Passive enumeration uses third-party data sources; active mode sends DNS queries. Both require Zone 2. |

#### Maigret

| Field | Value |
|-------|-------|
| **Tool** | Maigret >= 0.4 |
| **Agent** | `rainbow-recon-osint` |
| **Security zone** | Zone 2 |
| **Primary CLI pattern** | `maigret <username> --json --output maigret-results.json` |
| **Output format** | JSON |
| **Notes** | Queries social platforms for username presence. Zone 2 due to external HTTP requests. Engagement scope must include OSINT authorization. |

---

## /rainbow-cloud Tools

### Checkov (cloud/IaC)

| Field | Value |
|-------|-------|
| **Tool** | Checkov >= 3.0 |
| **Agent** | `rainbow-cloud-auditor` |
| **Security zone** | Zone 1 (IaC files) / Zone 2 (live cloud scan) |
| **Primary CLI pattern** | `checkov -d <iac-dir> --framework terraform,cloudformation,kubernetes --output json` |
| **Output format** | JSON |
| **Notes** | Static IaC analysis is Zone 1. `--runner-filter-tags` limits scope. Live cloud scanning with `--bc-api-key` is Zone 2. |

### Prowler

| Field | Value |
|-------|-------|
| **Tool** | Prowler >= 4.0 |
| **Agent** | `rainbow-cloud-auditor` |
| **Security zone** | Zone 2 |
| **Primary CLI pattern** | `prowler <provider> --output-formats json --output-directory prowler-results/` |
| **Output format** | JSON |
| **Notes** | Live cloud API calls to AWS, GCP, or Azure. `<provider>` is one of: `aws`, `gcp`, `azure`. Requires cloud credentials. |

### Kubescape

| Field | Value |
|-------|-------|
| **Tool** | Kubescape >= 3.0 |
| **Agent** | `rainbow-cloud-auditor` |
| **Security zone** | Zone 1 (manifest files) / Zone 2 (live cluster) |
| **Primary CLI pattern** | `kubescape scan --format json --output kubescape-results.json <framework>` |
| **Output format** | JSON |
| **Notes** | `<framework>` is one of: `nsa`, `mitre`, `cis-v1.23-t1.0.1`. Scanning local YAML manifests is Zone 1. Connecting to a live cluster via kubeconfig is Zone 2. |

### Kyverno

| Field | Value |
|-------|-------|
| **Tool** | Kyverno >= 1.11 |
| **Agent** | `rainbow-cloud-auditor` |
| **Security zone** | Zone 1 (validate) / Zone 2 (mutate) / Zone 3 (generate) |
| **Primary CLI pattern** | `kyverno apply <policy-file> --resource <manifest-file>` |
| **Output format** | Human-readable or JSON with `--output json` |
| **Notes** | Three operation modes map to three zones: `apply` (policy validation against manifests) is Zone 1; live cluster mutation is Zone 2; resource generation requires Zone 3. |

### Cartography

| Field | Value |
|-------|-------|
| **Tool** | Cartography >= 0.90 |
| **Agent** | `rainbow-cloud-mapper` |
| **Security zone** | Zone 2 |
| **Primary CLI pattern** | `cartography --neo4j-uri bolt://localhost:7687 --selected-modules <modules>` |
| **Output format** | Neo4j graph (attack path queries via Cypher) |
| **Notes** | Requires cloud credentials and a running Neo4j instance. Ingests cloud APIs to build an attack graph. Zone 2 due to live cloud API calls. |

---

## /rainbow-exploit Tools

### pwntools

| Field | Value |
|-------|-------|
| **Tool** | pwntools >= 4.12 |
| **Agent** | `rainbow-exploit-ops` |
| **Security zone** | Zone 3 |
| **Primary CLI pattern** | `python -c "from pwn import *; ..."` (library-based, no standalone CLI) |
| **Output format** | Depends on exploit script |
| **Notes** | Python library. Exploit scripts are written in Python using the pwntools API. Per-operation human approval required before Zone 3 execution. |

### Impacket

| Field | Value |
|-------|-------|
| **Tool** | Impacket >= 0.12 |
| **Agent** | `rainbow-exploit-ops`, `rainbow-exploit-ad` |
| **Security zone** | Zone 3 |
| **Primary CLI patterns** | `impacket-secretsdump <domain>/<user>:<pass>@<host>` / `impacket-smbexec <domain>/<user>:<pass>@<host>` |
| **Output format** | Human-readable |
| **Notes** | Suite of protocol-level attack scripts. Per-operation human approval required. |

### Donut

| Field | Value |
|-------|-------|
| **Tool** | Donut >= 1.0 |
| **Agent** | `rainbow-exploit-ops` |
| **Security zone** | Zone 3 |
| **Primary CLI pattern** | `donut -f <input-file> -o shellcode.bin` |
| **Output format** | Binary shellcode |
| **Notes** | Converts PE/DLL/NET assemblies to position-independent shellcode. Per-operation human approval required. |

### Empire

| Field | Value |
|-------|-------|
| **Tool** | Empire >= 5.0 |
| **Agent** | `rainbow-exploit-c2` |
| **Security zone** | Zone 3 |
| **Primary CLI pattern** | `empire server --config empire-config.yaml` |
| **Output format** | REST API on `http://localhost:1337` |
| **Notes** | C2 framework. Server must be running. Stager generation and listener management via REST API or `empire client`. Per-operation human approval required. |

### Mythic

| Field | Value |
|-------|-------|
| **Tool** | Mythic >= 3.3 |
| **Agent** | `rainbow-exploit-c2` |
| **Security zone** | Zone 3 |
| **Primary CLI pattern** | `./install_docker_mythic.sh` then `./mythic-cli start` |
| **Output format** | REST API and web UI |
| **Notes** | Container-based C2 framework. Agent (payload) generation via `mythic-cli` or REST API. Per-operation human approval required. |

### BloodHound CE

| Field | Value |
|-------|-------|
| **Tool** | BloodHound CE >= 5.0 |
| **Agent** | `rainbow-exploit-ad` |
| **Security zone** | Zone 2 |
| **Primary CLI pattern** | `bloodhound-ce --neo4j-uri bolt://localhost:7687` (UI-based query tool) |
| **Output format** | Graph queries via web UI or REST API |
| **Notes** | BloodHound data collection (SharpHound/AzureHound) is Zone 2. Query analysis of collected data is also Zone 2. Active exploitation of attack paths is Zone 3. |

### Metasploit

| Field | Value |
|-------|-------|
| **Tool** | Metasploit >= 6.4 |
| **Agent** | `rainbow-exploit-msf` |
| **Security zone** | Zone 3 |
| **Primary CLI pattern** | `msfconsole -q -x "use <module>; set RHOSTS <target>; set LHOST <local>; run"` |
| **Output format** | Interactive console output; JSON via `db_export` |
| **Notes** | Per-operation human approval required before any exploit module execution. Auxiliary/scanner modules are Zone 2; exploit and post modules are Zone 3. |

---

## /rainbow-runtime Tools

### mitmproxy Suite

| Tool | Version | Agent | Zone | Primary CLI pattern | Notes |
|------|---------|-------|------|---------------------|-------|
| `mitmproxy` | >= 10.0 | `rainbow-runtime-instrument` | Zone 2 (capture) / Zone 3 (scripts) | `mitmproxy --mode transparent -p 8080` | Interactive TUI proxy. |
| `mitmdump` | >= 10.0 | `rainbow-runtime-instrument` | Zone 2 (capture) / Zone 3 (scripts) | `mitmdump -p 8080 -w capture.mitm` | Non-interactive capture to file. `-s <script.py>` activates Zone 3. |
| `mitmweb` | >= 10.0 | `rainbow-runtime-instrument` | Zone 2 (capture) / Zone 3 (scripts) | `mitmweb -p 8080` | Web UI proxy. `-s <script.py>` activates Zone 3. |

**Zone note:** Passive traffic capture is Zone 2. Loading an addon script (`-s`) that modifies or injects content is Zone 3 and requires per-operation human approval.

### Frida Suite

| Tool | Version | Agent | Zone | Primary CLI pattern | Notes |
|------|---------|-------|------|---------------------|-------|
| `frida` | >= 16.0 | `rainbow-runtime-instrument` | Zone 2 / Zone 3 | `frida -U -f <bundle-id> -l <script.js>` | Instruments a process via USB-connected device. |
| `frida-trace` | >= 16.0 | `rainbow-runtime-instrument` | Zone 2 | `frida-trace -U -n <process> -i "<function-pattern>"` | Traces function calls in running process. |
| `frida-ps` | >= 16.0 | `rainbow-runtime-instrument` | Zone 1 / Zone 2 | `frida-ps -U` | Lists processes on a connected device. |
| `frida-ls-devices` | >= 16.0 | `rainbow-runtime-instrument` | Zone 1 | `frida-ls-devices` | Lists Frida-visible devices. |
| `frida-discover` | >= 16.0 | `rainbow-runtime-instrument` | Zone 2 | `frida-discover -U -n <process>` | Discovers exported functions in a process. |
| `frida-kill` | >= 16.0 | `rainbow-runtime-instrument` | Zone 2 / Zone 3 | `frida-kill -U <pid>` | Terminates a process on a connected device. |

**Zone note:** Passive observation (frida-ps, frida-ls-devices, frida-discover) is Zone 1 or Zone 2. Code injection and function hooking via `-l <script.js>` is Zone 3 and requires per-operation human approval.

---

## /blue-team Tools

### Tier A Tools (Execution-Validated)

| Tool | Version | Agent(s) | Zone | Primary CLI pattern | Output format |
|------|---------|----------|------|---------------------|---------------|
| YARA-X (`yr`) | >= 1.0 | `blue-detect`, `blue-malware-analyst`, `blue-ioc` | Zone 1 | `yr scan <rule-file> <target-dir>` | Text / JSON with `--output-format=json` |
| Hayabusa | >= 2.16 | `blue-siem`, `blue-incident-resp` | Zone 1 | `hayabusa csv-timeline -d <evtx-dir> -o timeline.csv` | CSV or JSON |
| Chainsaw | >= 2.9 | `blue-siem`, `blue-incident-resp` | Zone 1 | `chainsaw hunt <evtx-dir> --rules <rules-dir> --json` | JSON |
| Checkov | >= 3.0 | `blue-comply`, `blue-posture-k8s`, `blue-posture-sys` | Zone 1 | `checkov -d <dir> --output json` | JSON |
| Trivy | >= 0.50 | `blue-comply` | Zone 1 | `trivy image --format json <image>` | JSON |
| Prowler | >= 4.0 | `blue-comply` | Zone 1 | `prowler aws --output-formats json` | JSON |
| Kubescape | >= 3.0 | `blue-posture-k8s` | Zone 1 | `kubescape scan --format json <framework>` | JSON |
| kube-bench | >= 0.8 | `blue-posture-k8s` | Zone 1 | `kube-bench --json` | JSON |
| Cosign | >= 2.2 | `blue-comply` | Zone 1 | `cosign verify --certificate-identity=<id> --certificate-oidc-issuer=<issuer> <image>` | JSON |
| JADX | >= 1.5 | `blue-malware-analyst` | Zone 1 | `jadx -d <output-dir> <apk-or-dex>` | Java source files |
| Plaso | >= 20240308 | `blue-malware-analyst`, `blue-incident-resp` | Zone 1 | `log2timeline.py <storage.plaso> <source>` then `psort.py -o dynamic -w timeline.csv <storage.plaso>` | CSV / JSON |

### Tier B Tools (Execution-Validated with Limitations)

| Tool | Version | Agent(s) | Zone | Primary CLI pattern | Output format |
|------|---------|----------|------|---------------------|---------------|
| Sigma (sigma-cli) | >= 0.10 | `blue-siem`, `blue-ioc` | Zone 1 | `sigma convert -t <backend> <rule.yml>` | Backend-specific query format |
| Ghidra headless | >= 11.0 | `blue-malware-analyst` | Zone 1 | `analyzeHeadless <project-dir> <project-name> -import <binary> -postScript <script.java>` | Depends on analysis script |
| Kyverno | >= 1.11 | `blue-posture-k8s` | Zone 1 | `kyverno apply <policy> --resource <manifest>` | Human-readable |
| OpenSCAP (`oscap`) | >= 1.3 | `blue-posture-sys` | Zone 1 | `oscap xccdf eval --profile <profile> --results results.xml <datastream>` | XML |
| MISP API | >= 2.4 | `blue-intel` | Zone 1 | Python client: `misp.search(type_attribute='domain', value='<domain>')` | JSON |
| python-stix2 | >= 3.0 | `blue-intel`, `blue-ioc` | Zone 1 | Python library (no standalone CLI) | STIX 2.1 JSON bundles |
| taxii2-client | >= 2.3 | `blue-intel` | Zone 1 | Python library: `server = Server('<taxii-url>'); collection.get_objects()` | STIX 2.1 JSON bundles |

### Tier C Tools (Methodology Only — No Jerry Execution)

Tier C tools are deployed in user infrastructure. Jerry agents produce configuration templates and rule files for these tools; they do not execute them.

| Tool | Category | Agent that produces templates | Notes |
|------|----------|------------------------------|-------|
| Suricata | Network IDS/IPS | `blue-monitor` | Rule templates produced; execution requires user-deployed Suricata instance. |
| Zeek | Network analysis | `blue-monitor` | Script templates produced; execution requires user-deployed Zeek instance. |
| Falco | Runtime security | `blue-monitor` | Policy templates produced; execution requires user-deployed Falco. |
| Tetragon | eBPF security | `blue-monitor` | TracingPolicy YAML templates; execution requires Tetragon in cluster. |
| Wazuh | SIEM/EDR | `blue-monitor` | Ruleset templates; execution requires user-deployed Wazuh. |
| Volatility 3 | Memory forensics | `blue-malware-analyst` | Methodology guidance only; execution requires memory image and local install. |
| Velociraptor | DFIR | `blue-incident-resp` | VQL query templates; execution requires Velociraptor deployment. |
| DFIR-IRIS | IR case management | `blue-incident-resp` | Case export templates; execution requires DFIR-IRIS instance. |
| GRR | Remote live forensics | `blue-incident-resp` | Hunt configuration templates; execution requires GRR server. |
| TheHive | Case management | `blue-incident-resp` | Alert/case JSON templates; execution requires TheHive instance. |

---

## Exchange Schemas

Four schemas govern data transfer in purple team exercises. All schemas are located at `docs/schemas/` and validated against JSON Schema Draft 2020-12.

### RBEE v1 (Red-Blue Exchange Envelope)

**Schema file:** `docs/schemas/rbee-v1.schema.json`

**Schema ID:** `https://jerry.dev/schemas/rbee-v1.schema.json`

**Direction:** Red-team (`/red-team`) to Blue-team (`/blue-team`). Taint level: `adversary-produced`, `adversary-controlled`, or `engagement-generated`.

**Purpose:** Transfers a single red-team finding (one ATT&CK technique instance) from `red-reporter` to `blue-ioc` for detection rule generation.

**Required fields:**

| Field | Type | Pattern / Enum | Description |
|-------|------|----------------|-------------|
| `finding_id` | string | `^F-[0-9]{3,}$` | Unique finding identifier within the engagement. |
| `engagement_id` | string | `^[a-z0-9-]+$` | Engagement this finding belongs to. |
| `attack_technique.id` | string | `^T\d{4}(\.\d{3})?$` | ATT&CK technique or sub-technique ID. |
| `attack_technique.tactic` | string | `^TA\d{4}$` | Parent ATT&CK tactic ID. |
| `attack_technique.name` | string | — | Human-readable technique name. |
| `severity.qualitative` | string | `critical \| high \| medium \| low \| informational` | Finding severity classification. |
| `taint_level` | string | `adversary-produced \| adversary-controlled \| engagement-generated` | Trust classification of the finding's content. |
| `indicator_summary` | string | max 2000 chars | Brief description of indicators present. |
| `artifacts` | array | — | Array of artifact references (paths within `work/`, not inline content). |

**Notable optional fields:** `file_indicators` (YARA-targetable hashes and filenames), `network_indicators` (domains, IPs, URLs), `behavioral_indicators` (process, registry, command patterns), `d3fend_countermeasures` (D3FEND IDs in format `^D3-[A-Z]{2,5}$`), `requested_rule_types` (YARA, Sigma, Suricata), `trust_classification`, `data_classification`.

**Exchange directory:** `work/purple-team/exchange/{engagement-id}/rbee/`

**Example finding_id:** `F-001`, `F-012`

---

### CFE v1 (Coverage Feedback Envelope)

**Schema file:** `docs/schemas/cfe-v1.schema.json`

**Schema ID:** `https://jerry.dev/schemas/cfe-v1.schema.json`

**Direction:** Blue-team (`/blue-team`) to Red-team (`/red-team`). Taint level: `analysis-derived`.

**Purpose:** Reports detection coverage status for all ATT&CK techniques in the exercise to `red-vuln` for vulnerability priority adjustment.

**Required fields:**

| Field | Type | Pattern / Enum | Description |
|-------|------|----------------|-------------|
| `engagement_id` | string | `^[a-z0-9-]+$` | Engagement this feedback relates to. |
| `from_skill` | string | const: `/blue-team` | Always `/blue-team` for CFE envelopes. |
| `to_skill` | string | const: `/red-team` | Always `/red-team` for CFE envelopes. |
| `coverage_matrix` | array | minItems: 1 | Per-technique coverage entries. See sub-fields below. |
| `coverage_matrix[].technique_id` | string | `^T\d{4}(\.\d{3})?$` | ATT&CK technique ID. |
| `coverage_matrix[].coverage_status` | string | `detected \| partial \| undetected` | Overall detection status for this technique. |
| `confidence_tier` | string | `verified \| partial \| unverified` | Overall confidence for the coverage feedback. |
| `d3fend_kb_version` | string | — | D3FEND KB version used for mapping. |

**Coverage status definitions:**

| Value | Meaning |
|-------|---------|
| `detected` | Full detection across all relevant domains. |
| `partial` | Detection in some domains but not all, or confidence < 0.70. |
| `undetected` | No detection rule exists for this technique. |

**Confidence tier definitions:**

| Value | Meaning |
|-------|---------|
| `verified` | All detection results backed by Tier A tool execution. |
| `partial` | Mix of Tier A/B validated and Tier C methodology-only results. |
| `unverified` | Rule authorship only; no execution validation performed. |

**Exchange directory:** `work/purple-team/exchange/{engagement-id}/cfe/`

**Consumer:** `red-vuln`. When a CFE is available, `red-vuln` incorporates `coverage_status` as an additional factor in vulnerability priority scoring.

---

### DGE v1 (D3FEND Gap Envelope)

**Schema file:** `docs/schemas/dge-v1.schema.json`

**Schema ID:** `https://jerry.dev/schemas/dge-v1.schema.json`

**Direction:** Blue-team (`/blue-team`) to Red-team (`/red-team`). Taint level: `analysis-derived`.

**Purpose:** Reports D3FEND countermeasure coverage gaps from `blue-d3fend` to `red-lead` for future engagement scoping.

**Required fields:**

| Field | Type | Pattern / Enum | Description |
|-------|------|----------------|-------------|
| `engagement_id` | string | `^[a-z0-9-]+$` | Engagement this gap analysis relates to. |
| `from_skill` | string | const: `/blue-team` | Always `/blue-team` for DGE envelopes. |
| `to_skill` | string | const: `/red-team` | Always `/red-team` for DGE envelopes. |
| `coverage_gaps` | array | minItems: 0 | Per-technique gap entries. Empty array indicates full D3FEND coverage. |
| `coverage_gaps[].technique_id` | string | `^T\d{4}(\.\d{3})?$` | ATT&CK technique with a coverage gap. |
| `coverage_gaps[].gap_type` | string | `no_rule \| partial_rule \| untested` | Gap classification. |
| `coverage_gaps[].priority` | string | `high \| medium \| informational` | Priority for `red-lead` scoping decisions. |
| `d3fend_kb_version` | string | — | D3FEND KB version. Required for staleness tracking (security control T-04). |
| `analysis_date` | string | ISO 8601 date | Date when gap analysis was performed. |

**Gap type definitions:**

| Value | Meaning |
|-------|---------|
| `no_rule` | No detection rule exists for this technique. |
| `partial_rule` | Rule exists but coverage is incomplete. |
| `untested` | Rule exists but validation requires Tier C infrastructure not yet available. |

**Priority definitions:**

| Value | `red-lead` recommended action |
|-------|-------------------------------|
| `high` | Include in next engagement RoE technique allowlist. |
| `medium` | Include in capability development roadmap. |
| `informational` | Track for maturity roadmap. |

**Exchange directory:** `work/purple-team/exchange/{engagement-id}/dge/`

**Consumer:** `red-lead`. When a DGE is available from a prior exercise, `red-lead` incorporates gap priorities into technique selection for future engagement scoping. `red-lead` MUST verify `d3fend_kb_version` currency before incorporating gaps.

---

### Emulation Manifest v1

**Schema file:** `docs/schemas/emulation-manifest-v1.schema.json`

**Schema ID:** `https://jerry.dev/schemas/emulation-manifest-v1.schema.json`

**Direction:** Internal control document. Produced by `red-lead`; consumed by all red-team agents during purple team exercise execution.

**Purpose:** Defines the full set of ATT&CK techniques to emulate in a purple team exercise, assigns techniques to agents, and tracks execution status per technique.

**Required fields:**

| Field | Type | Pattern / Enum | Description |
|-------|------|----------------|-------------|
| `manifest_id` | string | `^manifest-[a-z0-9-]+-s[0-9]+$` | Unique identifier. Pattern encodes engagement ID and session number. |
| `engagement_id` | string | `^[a-z0-9-]+$` | Parent engagement identifier. |
| `techniques` | array | — | Array of technique execution entries. See sub-fields below. |
| `techniques[].technique_id` | string | `^T\d{4}(\.\d{3})?$` | ATT&CK technique or sub-technique ID. |
| `techniques[].name` | string | — | Human-readable technique name. |
| `techniques[].tactic` | string | — | Parent ATT&CK tactic. |
| `techniques[].assigned_agent` | string | `^red-[a-z]+(-[a-z]+)*$` | Red-team agent responsible for emulation. |
| `techniques[].zone` | string | `Zone 1 \| Zone 2 \| Zone 3` | Security zone required for emulation. |
| `techniques[].emulation_status` | string | See below | Current execution status. |
| `phases` | array | minItems: 1 | Purple team exercise phases with technique assignments. |

**Emulation status values:**

| Value | Meaning |
|-------|---------|
| `PLANNED` | Technique approved for emulation; not yet executed. |
| `IN_PROGRESS` | Emulation currently underway. |
| `COMPLETE` | Emulation finished; findings produced. |
| `EMULATION_SKIPPED` | Technique skipped per RoE or operational decision. |
| `EMULATION_FAILED` | Emulation attempted but did not complete. |
| `NOT_IN_SCOPE` | Technique excluded from this engagement's RoE. |

**Manifest ID example:** `manifest-purple-2026-001-s1` (engagement `purple-2026-001`, session 1).

**Storage location:** `work/purple-team/exchange/{engagement-id}/manifest.yaml`

**Validation rules (EM-01 through EM-08):** Documented in the schema `$comment` field. Key rules: all `technique_id` values must be unique within `techniques`; `assigned_agent` must match a registered red-team agent name pattern; Zone 3 assignments require explicit RoE authorization field.

---

*Source: `docs/schemas/rbee-v1.schema.json`, `docs/schemas/cfe-v1.schema.json`, `docs/schemas/dge-v1.schema.json`, `docs/schemas/emulation-manifest-v1.schema.json`, sub-skill `SKILL.md` files.*
