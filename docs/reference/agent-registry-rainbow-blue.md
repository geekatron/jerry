# Agent Registry: /rainbow and /blue-team

> Reference documentation for all agents in the `/rainbow` skill suite and the `/blue-team` skill. Describes agent identity, capabilities, security zone, and file location for each of the 26 agents across both skills.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Registry Format](#registry-format) | Column definitions and entry structure |
| [/rainbow Agents](#rainbow-agents) | 14 agents across 6 sub-skills |
| -- [rainbow-orchestrator](#rainbow-orchestrator) | Top-level /rainbow coordinator |
| -- [rainbow-reporter](#rainbow-reporter) | Engagement report synthesis |
| -- [/rainbow-supply-chain Agents](#rainbow-supply-chain-agents) | Supply chain scanning sub-skill |
| -- [/rainbow-recon Agents](#rainbow-recon-agents) | Reconnaissance sub-skill |
| -- [/rainbow-cloud Agents](#rainbow-cloud-agents) | Cloud security posture sub-skill |
| -- [/rainbow-exploit Agents](#rainbow-exploit-agents) | Exploitation framework sub-skill |
| -- [/rainbow-runtime Agents](#rainbow-runtime-agents) | Runtime instrumentation sub-skill |
| [/blue-team Agents](#blue-team-agents) | 12 agents, Zone 1 only |
| [Key Capabilities by Agent](#key-capabilities-by-agent) | Abbreviated capability reference |
| [Security Zone Summary](#security-zone-summary) | Agent-to-zone mapping |

---

## Registry Format

Each entry in this registry describes one agent using the following fields.

| Field | Description |
|-------|-------------|
| **Name** | Agent identifier. Matches the `name` field in the agent's `.md` frontmatter. |
| **File path** | Repository-relative path to the agent's `.md` definition file. |
| **Role** | Single-sentence role description. |
| **Cognitive mode** | Reasoning mode: `divergent`, `convergent`, `integrative`, `systematic`, or `forensic`. |
| **Tool tier** | Security tier: T1 (Read-Only), T2 (Read-Write), T3 (External), T4 (Persistent), T5 (Full). |
| **Security zone** | Zone 1 (Analysis), Zone 2 (Active Reconnaissance), Zone 3 (Exploitation). Agents may span zones when tool capabilities differ by zone. |
| **Model** | LLM model: `opus` or `sonnet`. |

---

## /rainbow Agents

### Parent Skill Agents

#### rainbow-orchestrator

| Field | Value |
|-------|-------|
| **Name** | `rainbow-orchestrator` |
| **File path** | `skills/rainbow/agents/rainbow-orchestrator.md` |
| **Role** | Coordinates /rainbow sub-skill invocation, manages engagement scope, produces final engagement summary. |
| **Cognitive mode** | convergent |
| **Tool tier** | T5 (Full — Task tool for sub-skill delegation) |
| **Security zone** | Zone 1 / Zone 2 / Zone 3 (scope-governed) |
| **Model** | opus |

#### rainbow-reporter

| Field | Value |
|-------|-------|
| **Name** | `rainbow-reporter` |
| **File path** | `skills/rainbow/agents/rainbow-reporter.md` |
| **Role** | Synthesizes findings from all sub-skills into a consolidated engagement report. |
| **Cognitive mode** | integrative |
| **Tool tier** | T2 (Read-Write) |
| **Security zone** | Zone 1 |
| **Model** | sonnet |

---

### /rainbow-supply-chain Agents

| Name | File path | Role | Cognitive mode | Tool tier | Security zone | Model |
|------|-----------|------|----------------|-----------|---------------|-------|
| `rainbow-sc-scanner` | `skills/rainbow/rainbow-supply-chain/agents/rainbow-sc-scanner.md` | Executes SBOM generation and vulnerability scanning against supply chain artifacts. | systematic | T2 | Zone 1 | sonnet |
| `rainbow-sc-verifier` | `skills/rainbow/rainbow-supply-chain/agents/rainbow-sc-verifier.md` | Verifies signatures and provenance chains for container images and packages. | systematic | T2 | Zone 1 / Zone 2 | sonnet |

**Installed tools:** Syft (>=1.0), Grype (>=0.74), Trivy (>=0.50), OSV-Scanner (>=2.0), Checkov (>=3.0), Cosign (>=2.2), Snyk CLI (Latest).

---

### /rainbow-recon Agents

| Name | File path | Role | Cognitive mode | Tool tier | Security zone | Model |
|------|-----------|------|----------------|-----------|---------------|-------|
| `rainbow-recon-pipeline` | `skills/rainbow/rainbow-recon/agents/rainbow-recon-pipeline.md` | Executes automated reconnaissance pipeline using Tier A tools. | systematic | T2 | Zone 2 | sonnet |
| `rainbow-recon-osint` | `skills/rainbow/rainbow-recon/agents/rainbow-recon-osint.md` | Performs OSINT collection and passive reconnaissance using Tier B tools. | divergent | T2 | Zone 2 | sonnet |

**Installed tools — Tier A:** Subfinder (>=2.6), httpx (>=1.6), dnsx (>=1.2), Naabu (>=2.4), Katana (>=1.0), Nuclei (>=3.0 — detection templates Zone 2, exploit templates Zone 3).

**Installed tools — Tier B:** OWASP Amass (>=4.2), Maigret (>=0.4).

---

### /rainbow-cloud Agents

| Name | File path | Role | Cognitive mode | Tool tier | Security zone | Model |
|------|-----------|------|----------------|-----------|---------------|-------|
| `rainbow-cloud-auditor` | `skills/rainbow/rainbow-cloud/agents/rainbow-cloud-auditor.md` | Audits IaC files and live cloud/Kubernetes configurations for security misconfigurations. | systematic | T2 | Zone 1 (IaC) / Zone 2 (live) | sonnet |
| `rainbow-cloud-mapper` | `skills/rainbow/rainbow-cloud/agents/rainbow-cloud-mapper.md` | Maps cloud resource relationships and attack paths using graph-based analysis. | divergent | T2 | Zone 2 | sonnet |

**Installed tools:** Checkov (>=3.0), Prowler (>=4.0), Kubescape (>=3.0), Kyverno (>=1.11 — validate=Zone 1, mutate=Zone 2, generate=Zone 3), Cartography (>=0.90).

---

### /rainbow-exploit Agents

| Name | File path | Role | Cognitive mode | Tool tier | Security zone | Model |
|------|-----------|------|----------------|-----------|---------------|-------|
| `rainbow-exploit-ops` | `skills/rainbow/rainbow-exploit/agents/rainbow-exploit-ops.md` | Executes general exploitation operations using pwntools and Impacket. | convergent | T2 | Zone 3 | opus |
| `rainbow-exploit-c2` | `skills/rainbow/rainbow-exploit/agents/rainbow-exploit-c2.md` | Manages command and control infrastructure using Empire and Mythic. | convergent | T2 | Zone 3 | opus |
| `rainbow-exploit-ad` | `skills/rainbow/rainbow-exploit/agents/rainbow-exploit-ad.md` | Analyzes Active Directory attack paths and performs AD-specific exploitation. | forensic | T2 | Zone 2 / Zone 3 | opus |
| `rainbow-exploit-msf` | `skills/rainbow/rainbow-exploit/agents/rainbow-exploit-msf.md` | Executes Metasploit-based exploitation with module selection and post-exploitation. | convergent | T2 | Zone 3 | opus |

**Installed tools:** pwntools (>=4.12), Impacket (>=0.12), Donut (>=1.0), Empire (>=5.0), Mythic (>=3.3), BloodHound CE (>=5.0 — Zone 2), Metasploit (>=6.4).

**Zone requirement:** All /rainbow-exploit agents require per-operation human approval before Zone 3 execution.

---

### /rainbow-runtime Agents

| Name | File path | Role | Cognitive mode | Tool tier | Security zone | Model |
|------|-----------|------|----------------|-----------|---------------|-------|
| `rainbow-runtime-instrument` | `skills/rainbow/rainbow-runtime/agents/rainbow-runtime-instrument.md` | Instruments running processes and network traffic for dynamic analysis and interception. | convergent | T2 | Zone 2 (capture) / Zone 3 (active interception) | opus |

**Installed tools — mitmproxy suite:** mitmproxy, mitmdump, mitmweb (>=10.0). Passive capture is Zone 2; `-s` script injection is Zone 3.

**Installed tools — Frida suite:** frida, frida-trace, frida-ps, frida-ls-devices, frida-discover, frida-kill (>=16.0).

---

## /blue-team Agents

All /blue-team agents are confined to Zone 1 (Analysis). No live system interaction, no network reconnaissance, no exploitation capability.

| Name | File path | Role | Cognitive mode | Tool tier | Security zone | Model |
|------|-----------|------|----------------|-----------|---------------|-------|
| `blue-lead` | `skills/blue-team/agents/blue-lead.md` | Coordinates /blue-team agents, scopes defensive exercises, produces consolidated reports. | convergent | T3 | Zone 1 | opus |
| `blue-detect` | `skills/blue-team/agents/blue-detect.md` | Writes and validates detection rules (YARA-X, Sigma). | systematic | T2 | Zone 1 | sonnet |
| `blue-monitor` | `skills/blue-team/agents/blue-monitor.md` | Produces monitoring configurations and Suricata/Falco rule templates. | systematic | T2 | Zone 1 | sonnet |
| `blue-siem` | `skills/blue-team/agents/blue-siem.md` | Creates and validates Sigma rules for SIEM integration. | systematic | T2 | Zone 1 | sonnet |
| `blue-malware-analyst` | `skills/blue-team/agents/blue-malware-analyst.md` | Performs static malware analysis using YARA-X, JADX, Ghidra headless, and Plaso. | systematic | T2 | Zone 1 | sonnet |
| `blue-incident-resp` | `skills/blue-team/agents/blue-incident-resp.md` | Performs incident response triage and timeline reconstruction from forensic artifacts. | systematic | T2 | Zone 1 | sonnet |
| `blue-comply` | `skills/blue-team/agents/blue-comply.md` | Executes compliance audits against CIS benchmarks, NIST CSF, and cloud security frameworks. | systematic | T2 | Zone 1 | sonnet |
| `blue-posture-k8s` | `skills/blue-team/agents/blue-posture-k8s.md` | Assesses Kubernetes security posture using Kubescape, kube-bench, and Kyverno. | systematic | T2 | Zone 1 | sonnet |
| `blue-posture-sys` | `skills/blue-team/agents/blue-posture-sys.md` | Assesses system-level security posture using OpenSCAP and Checkov. | systematic | T2 | Zone 1 | sonnet |
| `blue-intel` | `skills/blue-team/agents/blue-intel.md` | Performs threat intelligence analysis using MISP, python-stix2, and taxii2-client. | divergent | T3 | Zone 1 | opus |
| `blue-d3fend` | `skills/blue-team/agents/blue-d3fend.md` | Maps ATT&CK techniques to D3FEND countermeasures and produces D3FEND Gap Envelopes (DGE). | convergent | T3 | Zone 1 | sonnet |
| `blue-ioc` | `skills/blue-team/agents/blue-ioc.md` | Transforms red-team findings from RBEE envelopes into typed detection rules (YARA, Sigma). | systematic | T2 | Zone 1 | sonnet |

**Tool tiers:** /blue-team uses 28 tools across three tiers. Tier A (11 tools, execution-validated): YARA-X, Hayabusa, Chainsaw, Checkov, Trivy, Prowler, Kubescape, kube-bench, Cosign, JADX, Plaso. Tier B (7 tools, execution-validated with limitations): Sigma, Ghidra headless, Kyverno, OpenSCAP, MISP API, python-stix2, taxii2-client. Tier C (10 tools, methodology-only, no Jerry execution): Suricata, Zeek, Falco, Tetragon, Wazuh, Volatility 3, Velociraptor, DFIR-IRIS, GRR, TheHive.

---

## Key Capabilities by Agent

| Agent | Primary capability | Secondary capability | Key tools |
|-------|--------------------|---------------------|-----------|
| `rainbow-orchestrator` | Sub-skill coordination | Scope enforcement | Task (T5) |
| `rainbow-reporter` | Report synthesis | Cross-sub-skill findings merge | Read, Write |
| `rainbow-sc-scanner` | SBOM generation | Vulnerability scanning | Syft, Grype, Trivy |
| `rainbow-sc-verifier` | Signature verification | Provenance chain validation | Cosign, Trivy |
| `rainbow-recon-pipeline` | Subdomain enumeration | Port scanning, web crawling | Subfinder, httpx, Naabu, Katana, Nuclei |
| `rainbow-recon-osint` | OSINT collection | Passive DNS, social enumeration | Amass, Maigret |
| `rainbow-cloud-auditor` | IaC misconfiguration detection | Live cloud posture assessment | Checkov, Prowler, Kubescape |
| `rainbow-cloud-mapper` | Attack path mapping | Resource relationship graph | Cartography |
| `rainbow-exploit-ops` | Binary exploitation | Protocol-level attacks | pwntools, Impacket |
| `rainbow-exploit-c2` | C2 infrastructure setup | Agent deployment | Empire, Mythic |
| `rainbow-exploit-ad` | AD attack path analysis | Kerberoasting, BloodHound query | BloodHound CE, Impacket |
| `rainbow-exploit-msf` | Metasploit module execution | Post-exploitation | Metasploit |
| `rainbow-runtime-instrument` | Network traffic interception | Dynamic binary instrumentation | mitmproxy suite, Frida suite |
| `blue-lead` | Defensive exercise coordination | Purple team management | Task (T3 delegation) |
| `blue-detect` | YARA-X rule authoring | Rule syntax validation | YARA-X (yr check, yr scan) |
| `blue-monitor` | Monitoring configuration | Suricata/Falco rule templates | Methodology (Tier C) |
| `blue-siem` | Sigma rule authoring | Log source correlation | Sigma, Hayabusa, Chainsaw |
| `blue-malware-analyst` | Static analysis | Log correlation | YARA-X, JADX, Ghidra, Plaso |
| `blue-incident-resp` | IR triage | Timeline reconstruction | Hayabusa, Chainsaw, Plaso |
| `blue-comply` | CIS benchmark audit | Cloud compliance | Checkov, Trivy, Prowler, kube-bench |
| `blue-posture-k8s` | Kubernetes posture | Policy validation | Kubescape, kube-bench, Kyverno |
| `blue-posture-sys` | System posture | IaC compliance | OpenSCAP, Checkov |
| `blue-intel` | Threat intelligence analysis | STIX/TAXII data handling | MISP API, python-stix2, taxii2-client |
| `blue-d3fend` | ATT&CK-to-D3FEND mapping | DGE production | D3FEND KB (methodology) |
| `blue-ioc` | IOC rule generation from RBEE | STIX transformation | YARA-X, Sigma |

---

## Security Zone Summary

| Zone | Definition | Agents |
|------|------------|--------|
| **Zone 1** (Analysis) | Read-only analysis of artifacts, local files, and static data. No live system contact. No engagement scope required. | All /blue-team agents (12). rainbow-orchestrator (when scoping), rainbow-reporter, rainbow-sc-scanner, rainbow-sc-verifier (local artifacts), rainbow-cloud-auditor (IaC files only). |
| **Zone 2** (Active Reconnaissance) | Network contact with in-scope targets. Engagement scope document required before execution. | rainbow-recon-pipeline, rainbow-recon-osint, rainbow-cloud-auditor (live cloud/cluster), rainbow-cloud-mapper, rainbow-exploit-ad (BloodHound collection), rainbow-runtime-instrument (passive capture). |
| **Zone 3** (Exploitation) | Active exploitation, C2 operation, code injection, traffic manipulation. Per-operation human approval required. Engagement RoE must explicitly permit. | rainbow-exploit-ops, rainbow-exploit-c2, rainbow-exploit-msf, rainbow-exploit-ad (exploitation phase), rainbow-runtime-instrument (active script injection). |

**Zone boundary enforcement:** Zone promotion requires explicit scope document authorization. Zone 3 operations additionally require per-operation human approval at runtime. Agents that span zones apply the higher-zone constraints whenever Zone 3 capabilities are invoked.

---

*Source: `AGENTS.md` (agent registry), sub-skill `SKILL.md` files.*
*Schema: `docs/schemas/agent-governance-v1.schema.json` (governance metadata), Claude Code official frontmatter (runtime config).*
