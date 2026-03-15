---
name: rainbow
description: "Composable cybersecurity tool-execution skill with 5 sub-skills spanning supply chain security, reconnaissance, cloud security posture, exploitation frameworks, and runtime instrumentation. Invoked when users request tool-assisted security operations: SBOM generation, vulnerability scanning, subdomain enumeration, cloud posture auditing, exploit framework usage, or C2 infrastructure. Routes to 14 specialized agents across 3 security zones. Requires engagement scope for Zone 2/3 operations. Follows MITRE ATT&CK, PTES, and NIST CSF methodology frameworks."
version: "1.0.0"
agents:
  - rainbow-orchestrator
  - rainbow-reporter
  - rainbow-sc-scanner
  - rainbow-sc-verifier
  - rainbow-recon-pipeline
  - rainbow-recon-osint
  - rainbow-cloud-auditor
  - rainbow-cloud-mapper
  - rainbow-exploit-ops
  - rainbow-exploit-c2
  - rainbow-exploit-ad
  - rainbow-exploit-msf
  - rainbow-runtime-instrument
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch, mcp__context7__resolve-library-id, mcp__context7__query-docs
activation-keywords:
  - "SBOM"
  - "vulnerability scan"
  - "supply chain security"
  - "container scan"
  - "IaC scan"
  - "reconnaissance pipeline"
  - "subdomain enumeration"
  - "port scan"
  - "cloud security posture"
  - "exploit framework"
  - "exploit methodology"
  - "Nuclei"
  - "Trivy"
  - "Checkov"
  - "Syft"
  - "Grype"
  - "rainbow"
  - "tool-assisted pentest"
  - "OSINT tools"
  - "C2 framework"
  - "Prowler"
  - "Kubescape"
  - "Subfinder"
  - "httpx"
  - "pwntools"
  - "Impacket"
  - "Metasploit"
  - "mitmproxy"
  - "Frida"
  - "mobile security scan"
---

# Rainbow Skill

> **Version:** 1.0.0
> **Framework:** Jerry Rainbow Series
> **Constitutional Compliance:** Jerry Constitution v1.0
> **SSOT Reference:** ADR-PROJ023-001 (Rainbow Series Cybersecurity Skill Architecture)

## Document Audience (Triple-Lens)

| Level | Audience | Sections to Focus On |
|-------|----------|---------------------|
| **L0 (Stakeholder)** | Engagement managers, leadership | [Purpose](#purpose), [When to Use This Skill](#when-to-use-this-skill), [Routing Disambiguation](#routing-disambiguation), [Security Zone Overview](#security-zone-overview) |
| **L1 (Practitioner)** | Security operators invoking agents | [Sub-Skill Registry](#sub-skill-registry), [Internal Routing](#internal-routing), [Engagement Lifecycle](#engagement-lifecycle), [Quick Reference](#quick-reference) |
| **L2 (Architect)** | Framework designers, governance reviewers | [Security Zone Enforcement](#security-zone-enforcement), [Credential Filter Reference](#credential-filter-reference), [P-003 Compliance](#p-003-compliance), [Constitutional Compliance](#constitutional-compliance) |

---

## Purpose

The Rainbow skill provides **composable tool-execution capability** for cybersecurity operations. It routes to 14 specialized agents organized across 5 sub-skills, each aligned to a distinct security domain and tool ecosystem. Unlike /red-team (methodology guidance) and /eng-team (secure development), /rainbow executes security tools (scanners, exploit frameworks, reconnaissance pipelines) within a governed security zone model.

### Key Capabilities

- **Supply Chain Security** -- SBOM generation, vulnerability scanning, container/IaC auditing, signature verification (Syft, Grype, Trivy, OSV-Scanner, Checkov, Cosign, Snyk CLI)
- **Reconnaissance Pipelines** -- Subdomain enumeration, port scanning, HTTP probing, vulnerability detection, OSINT (Subfinder, httpx, dnsx, Naabu, Katana, Nuclei, OWASP Amass, Maigret)
- **Cloud Security Posture** -- Cloud configuration auditing, Kubernetes policy validation, infrastructure mapping (Checkov, Prowler, Kubescape, Kyverno, Cartography)
- **Exploitation Frameworks** -- Binary exploitation, C2 infrastructure, Active Directory attacks, Metasploit integration (pwntools, Impacket, Donut, Empire, Mythic, BloodHound CE, Metasploit)
- **Runtime Instrumentation** -- Traffic interception, dynamic analysis, mobile security (mitmproxy, Frida)
- **Three-Zone Security Model** -- Graduated authorization from audit-only (Zone 1) through reconnaissance (Zone 2) to exploitation (Zone 3)
- **Credential Filter Pipeline** -- Defense-in-depth credential sanitization on all tool output before context window entry

### What This Skill Is NOT

This skill provides **tool-execution orchestration**, not methodology guidance. It does NOT:

- Provide penetration testing methodology (use `/red-team` for PTES/OSSTMM methodology)
- Perform secure development or threat modeling (use `/eng-team` for STRIDE/DREAD/SDLC)
- Perform adversarial quality review of deliverables (use `/adversary`)
- Generate weaponized exploit code from scratch without framework tooling
- Operate Zone 2/3 tools without engagement scope authorization

This design follows the ADR-PROJ023-001 composable architecture: each sub-skill owns a distinct security domain with explicit tool assignments, zone classifications, and guardrail profiles.

---

## When to Use This Skill

Activate when:

- Generating SBOMs or scanning for supply chain vulnerabilities
- Running reconnaissance pipelines against authorized targets
- Auditing cloud infrastructure security posture
- Using exploit frameworks within an authorized engagement
- Performing runtime instrumentation or dynamic analysis
- Verifying container image signatures or artifact provenance
- Scanning IaC templates for misconfigurations

NEVER invoke this skill when:
- Task is penetration testing **methodology** guidance without tool execution -- Consequence: /rainbow loads tool adapters and execution pipelines instead of PTES/OSSTMM methodology; use `/red-team` instead
- Task is building secure software or threat modeling -- Consequence: offensive tool context loaded instead of STRIDE/DREAD/OWASP; use `/eng-team` instead
- Task is adversarial quality review of deliverables -- Consequence: tool-execution agents loaded for quality assessment; use `/adversary` instead
- Task is malware analysis or threat detection -- Consequence: offensive tools loaded instead of YARA-X/Ghidra; use `/blue-team` instead
- No engagement scope exists for Zone 2/3 operations -- Consequence: Zone 2/3 agents will halt at scope validation

See [Routing Disambiguation](#routing-disambiguation) for full exclusion conditions.

---

## Sub-Skill Registry

| Sub-Skill | Zone | Agents | Tools | Description |
|-----------|------|--------|-------|-------------|
| `/rainbow-supply-chain` | 1 (1/3 for signing) | `rainbow-sc-scanner`, `rainbow-sc-verifier` | Syft, Grype, Trivy, OSV-Scanner, Checkov, Cosign, Snyk CLI | SBOM generation, vulnerability scanning, signature verification |
| `/rainbow-recon` | 2 | `rainbow-recon-pipeline`, `rainbow-recon-osint` | Subfinder, httpx, dnsx, Naabu, Katana, Nuclei, OWASP Amass, Maigret | Subdomain enumeration, port scanning, OSINT, vulnerability detection |
| `/rainbow-cloud` | 1/2 | `rainbow-cloud-auditor`, `rainbow-cloud-mapper` | Checkov, Prowler, Kubescape, Kyverno, Cartography | Cloud posture auditing, Kubernetes policy, infrastructure mapping |
| `/rainbow-exploit` | 3 | `rainbow-exploit-ops`, `rainbow-exploit-c2`, `rainbow-exploit-ad`, `rainbow-exploit-msf` | pwntools, Impacket, Donut, Empire, Mythic, BloodHound CE, Metasploit | Binary exploitation, C2, Active Directory attacks, Metasploit |
| `/rainbow-runtime` | 2/3 | `rainbow-runtime-instrument` | mitmproxy, Frida | Traffic interception, dynamic analysis, runtime instrumentation |

**Cross-cutting:** `rainbow-orchestrator` (T5, routing only), `rainbow-reporter` (T1, report generation from outputs)

---

## Internal Routing

The `rainbow-orchestrator` is the sole routing authority within /rainbow. It receives requests from the main context and routes to the appropriate sub-skill agent based on request classification.

### Routing Decision Tree

```
User Request -> rainbow-orchestrator
    |
    +-- Contains supply chain keywords (SBOM, CVE scan, container scan, IaC, signature)?
    |   YES -> Classify zone (verify=Zone 1, sign=Zone 3)
    |   Route to rainbow-sc-scanner or rainbow-sc-verifier
    |
    +-- Contains reconnaissance keywords (subdomain, port scan, OSINT, enumerate)?
    |   YES -> Validate engagement scope (Zone 2 required)
    |   Route to rainbow-recon-pipeline or rainbow-recon-osint
    |
    +-- Contains cloud keywords (cloud posture, Kubernetes, infrastructure map)?
    |   YES -> Classify zone (audit=Zone 1, map=Zone 2)
    |   Route to rainbow-cloud-auditor or rainbow-cloud-mapper
    |
    +-- Contains exploit keywords (pwntools, C2, AD attack, Metasploit)?
    |   YES -> Validate engagement scope + Zone 3 authorization
    |   Route to rainbow-exploit-{ops|c2|ad|msf}
    |
    +-- Contains runtime keywords (mitmproxy, Frida, intercept, instrument)?
    |   YES -> Classify zone (intercept=Zone 2, modify=Zone 3)
    |   Route to rainbow-runtime-instrument
    |
    +-- Contains report keywords (report, summarize findings)?
    |   YES -> Route to rainbow-reporter
    |
    +-- No match -> Escalate to user per H-31
```

### Agent-to-Sub-Skill Mapping

| Agent | Sub-Skill | Security Zone |
|-------|-----------|---------------|
| `rainbow-orchestrator` | `/rainbow` (parent) | Governance |
| `rainbow-reporter` | `/rainbow` (cross-cutting) | -- |
| `rainbow-sc-scanner` | `/rainbow-supply-chain` | Zone 1 |
| `rainbow-sc-verifier` | `/rainbow-supply-chain` | Zone 1/3 |
| `rainbow-recon-pipeline` | `/rainbow-recon` | Zone 2 |
| `rainbow-recon-osint` | `/rainbow-recon` | Zone 2 |
| `rainbow-cloud-auditor` | `/rainbow-cloud` | Zone 1/2 |
| `rainbow-cloud-mapper` | `/rainbow-cloud` | Zone 2 |
| `rainbow-exploit-ops` | `/rainbow-exploit` | Zone 3 |
| `rainbow-exploit-c2` | `/rainbow-exploit` | Zone 3 |
| `rainbow-exploit-ad` | `/rainbow-exploit` | Zone 3 |
| `rainbow-exploit-msf` | `/rainbow-exploit` | Zone 3 |
| `rainbow-runtime-instrument` | `/rainbow-runtime` | Zone 2/3 |

---

## Security Zone Overview

Three security zones govern authorization requirements. Zone classification determines which guardrails, approval gates, and credential handling apply to each operation.

| Zone | Name | Authorization | Scope | Examples |
|------|------|--------------|-------|---------|
| **Zone 1** | Audit/Scan | Project scope (no engagement required) | Read-only analysis of owned assets | SBOM generation, IaC scanning, signature verification, cloud posture audit |
| **Zone 2** | Reconnaissance | Engagement scope required | Active probing of authorized targets | Subdomain enumeration, port scanning, OSINT, cloud infrastructure mapping |
| **Zone 3** | Exploitation | Engagement scope + per-operation human approval | Offensive operations against authorized targets | Exploit execution, C2 infrastructure, AD attacks, artifact signing |

### Zone Escalation Rules

- Zone 1 operations execute within project scope without engagement authorization
- Zone 2 operations require an active engagement scope document before execution
- Zone 3 operations require engagement scope PLUS per-operation human approval per P-020
- Dual-zone tools (Nuclei, Cosign, Kyverno) escalate based on operation mode, not tool identity
- Zone escalation requires scope validation; de-escalation within an active engagement is permitted without additional authorization (e.g., Zone 3 to Zone 2 fallback after exploitation phase completes)

---

## Security Zone Enforcement

Zone enforcement operates at three layers per ADR-PROJ023-001.

### Layer 1: Parent Orchestrator

The `rainbow-orchestrator` validates engagement scope before routing to Zone 2/3 sub-skill agents. Zone 1 sub-skills bypass this gate. The orchestrator maintains engagement lifecycle state (scope document, RoE, phase gates).

### Layer 2: Sub-Skill Rules

Each sub-skill declares its zone's guardrail profile in its SKILL.md rules. Dual-zone sub-skills (`/rainbow-cloud`, `/rainbow-runtime`, `/rainbow-supply-chain`) declare operation-mode-aware zone escalation rules specifying which CLI subcommands or template categories trigger which zone's guardrails.

### Layer 3: Agent-Level Guardrails

Each agent's `.governance.yaml` declares constitutional compliance (P-003, P-020, P-022), forbidden actions, and tool-specific guardrails. Zone 3 agents include credential vault reference-only access and artifact quarantine directives.

### Dual-Zone Tool Escalation

Three tools span security zone boundaries with explicit, technically-enforced classification:

| Tool | Home Sub-Skill | Zone 1 Operations | Zone 2 Operations | Zone 3 Operations |
|------|---------------|-------------------|-------------------|-------------------|
| **Nuclei** | `/rainbow-recon` | -- | Detection templates (severity-based, no exploit tags) | Exploit templates (tagged `exploit`, `rce`, `upload`) |
| **Cosign** | `/rainbow-supply-chain` | `verify`, `tree` | `download signature/sbom` | `sign`, `attest`, `attach` |
| **Kyverno** | `/rainbow-cloud` | `validate` (with mandatory `--dry-run`) | `mutate` (after scope validation) | `generate` (per-operation approval) |

---

## Credential Filter Reference

The credential filter pipeline is a shared infrastructure component that operates as a mandatory pre-processing gate on all tool output before context window entry. No tool output enters the context window without passing through the filter.

**Architecture:** Defense-in-depth with three layers:

| Layer | Mechanism | Coverage |
|-------|-----------|----------|
| L1 | Regex pattern matching | Known credential formats (AWS keys, API tokens, SSH keys, NTLM hashes, Kerberos material, connection strings) |
| L2 | Entropy-based detection | Novel formats, base64-encoded secrets (Shannon entropy > 4.5 for strings > 16 chars) |
| L3 | Structural analysis | JSON/YAML key-name matching against sensitive field patterns |

**Fail-closed behavior:** Filter crash or timeout rejects the entire tool output block. Flagged content is quarantined to `work/.credential-quarantine/` with user notification.

**Full specification:** `skills/rainbow/rules/rainbow-credential-filter.md`

---

## P-003 Compliance

The `rainbow-orchestrator` is the **sole T5 agent** in /rainbow. All other agents are T2 workers that MUST NOT have Task tool access per H-34.

```
P-003 AGENT HIERARCHY:
======================

  +-------------------+
  | MAIN CONTEXT      |  <-- Framework orchestrator (Claude session)
  | (orchestrator)    |
  +-------------------+
          |
          v
  +---------------------+
  | rainbow-orchestrator |  <-- T5 routing agent (sole Task tool user)
  | (sub-orchestrator)   |
  +---------------------+
     |  |  |  |  |  |
     v  v  v  v  v  v
  +------+ +------+ +------+ +------+ +------+ +------+
  | sc-  | | sc-  | | recon| | cloud| |exploi| | ...  |  <-- T2 workers
  |scannr| |verif | | pipe | | audit| | t-ops| |      |
  +------+ +------+ +------+ +------+ +------+ +------+

  Maximum nesting depth: 2 hops (main context -> orchestrator -> worker)
  Within H-36 circuit breaker limit of 3 hops.
  Sub-skill agents CANNOT invoke other agents.
  Sub-skill agents CANNOT spawn subagents.
```

**Purple team mode exception:** During purple team exercises, the main context invokes /rainbow sub-skill agents directly (bypassing `rainbow-orchestrator`) to avoid consuming all 3 circuit breaker hops. See ADR-PROJ023-001 Purple Team Composition Model.

---

## Engagement Lifecycle

### Lifecycle Phases

| Phase | Action | Zone Gate |
|-------|--------|-----------|
| **1. Scope Establishment** | Create engagement scope document (engagement_id, authorized targets, technique allowlist, time window, exclusions, RoE) | Required for Zone 2/3 |
| **2. Tool Execution** | Route requests to sub-skill agents per internal routing decision tree | Zone-specific gates apply |
| **3. Evidence Collection** | All tool outputs persisted to engagement output directory | Credential filter applied |
| **4. Reporting** | `rainbow-reporter` generates unified findings report from all sub-skill outputs | No zone gate |
| **5. Engagement Close** | Scope document archived, evidence retention policy applied | -- |

### Engagement Scope Document

Zone 2/3 operations require an active engagement scope document. The scope document follows the same YAML schema as /red-team scope documents for cross-skill compatibility:

```yaml
scope:
  engagement_id: "RBW-NNNN"
  version: "1.0"
  authorized_targets: [{type, value}]
  technique_allowlist: ["TNNNN", ...]
  time_window: {start, end}
  exclusion_list: [...]
  zone_authorizations:
    zone_2: true
    zone_3: false  # requires explicit per-operation approval even when true
  evidence_handling: {storage, retention_days, destruction_method}
  signature: {authorized_by, date, confirmation}
```

### Output Location Convention

```
skills/rainbow/output/{engagement-id}/{agent-name}-{topic-slug}.md
```

Evidence artifacts are stored in:

```
skills/rainbow/output/{engagement-id}/evidence/
```

---

## Routing Disambiguation

> When this skill is the wrong choice and what happens if misrouted.

| Condition | Use Instead | Consequence of Misrouting |
|-----------|-------------|--------------------------|
| Penetration testing methodology guidance (PTES, OSSTMM) | `/red-team` | Tool-execution agents loaded instead of methodology agents; PTES pre-engagement methodology not available |
| Building secure software, threat modeling, STRIDE/DREAD | `/eng-team` | Offensive tool context loaded instead of defensive engineering; OWASP ASVS compliance not available |
| Adversarial quality review of deliverables | `/adversary` | Tool-execution agents loaded for quality assessment; S-014 rubric not available |
| Malware analysis, threat detection, YARA rules | `/blue-team` | Offensive tools loaded instead of defensive detection; YARA-X and Ghidra analysis not available |
| General security research without tool execution | `/problem-solving` | Tool adapter overhead loaded for research task; ps-researcher methodology not available |
| No engagement scope and Zone 2/3 operations needed | Establish scope first | Zone 2/3 agents will halt at scope validation |

**Disambiguation rules (trigger map):**
- "vulnerability scan" or "Nuclei" -> `/rainbow` (tool-assisted scanning)
- "penetration test methodology" or "PTES" -> `/red-team` (engagement methodology)
- "malware analysis" or "YARA" -> `/blue-team` (defensive detection/analysis)
- "secure development" or "SAST pipeline" -> `/eng-team` (engineering methodology)
- Ambiguous -> H-31 clarification

---

## Cross-Skill Integration Points

Six integration points connect /rainbow with /red-team, /blue-team, and /eng-team.

| # | Source | Target | Data Flow |
|---|--------|--------|-----------|
| IP-1 | red-recon | eng-architect | Threat intelligence for STRIDE/DREAD |
| IP-2 | /rainbow-recon | eng-infra, eng-devsecops | Attack surface validation results (enriched with tool output) |
| IP-3 | /rainbow-exploit | eng-security, eng-backend, eng-frontend | Exploitation results (enriched with tool output) |
| IP-4 | red-persist, red-lateral | eng-incident | IR exercise results |
| IP-5 | /rainbow-recon, /rainbow-exploit | blue-detect | TTPs, IOC patterns for detection tuning |
| IP-6 | blue-detect, blue-analyst | eng-incident, eng-devsecops | Detection coverage reports, analysis findings |

---

## Constitutional Compliance

| Principle | Application |
|-----------|-------------|
| **P-003 / H-01** | Single T5 agent (`rainbow-orchestrator`). All sub-skill agents are T2 workers. Maximum 2 hops for any request. |
| **P-020 / H-02** | Zone 3 operations require per-operation human approval. Zone 2 requires engagement scope. Zone 1 within project scope. |
| **P-022 / H-03** | All routing decisions transparent. Tool execution status reported. Credential filter quarantine actions disclosed. |
| **P-001** | All findings evidence-based with tool output citations. |
| **P-002** | All tool outputs, engagement state, and scope documents persisted to filesystem. |
| **H-34** | All agents use dual-file architecture (.md + .governance.yaml). Constitutional compliance triplet in every agent. |
| **H-36** | Parent-routed registration (single trigger map entry). Maximum 2 hops within circuit breaker limit. |

---

## Quick Reference

### Common Workflows

| Need | Agent | Example |
|------|-------|---------|
| Generate SBOM for a container image | rainbow-sc-scanner | "Generate SBOM for the nginx:latest container image" |
| Scan for vulnerabilities in dependencies | rainbow-sc-scanner | "Scan this project's dependencies for known vulnerabilities" |
| Verify container image signature | rainbow-sc-verifier | "Verify the cosign signature on this container image" |
| Enumerate subdomains for authorized target | rainbow-recon-pipeline | "Run subdomain enumeration against target.example.com" |
| Perform OSINT on target organization | rainbow-recon-osint | "Gather OSINT on the target organization" |
| Audit cloud infrastructure posture | rainbow-cloud-auditor | "Audit AWS account security posture with Prowler" |
| Map cloud infrastructure | rainbow-cloud-mapper | "Map the infrastructure graph with Cartography" |
| Execute exploit against authorized target | rainbow-exploit-ops | "Use pwntools to exploit the buffer overflow in the target binary" |
| Set up C2 infrastructure | rainbow-exploit-c2 | "Configure Empire C2 for the engagement" |
| Analyze AD attack paths | rainbow-exploit-ad | "Map AD attack paths with BloodHound" |
| Run Metasploit module | rainbow-exploit-msf | "Execute the Metasploit module for CVE-2026-XXXX" |
| Intercept traffic | rainbow-runtime-instrument | "Set up mitmproxy to intercept HTTPS traffic from the target app" |
| Generate engagement report | rainbow-reporter | "Generate findings report for engagement RBW-0001" |

### Sub-Skill Creation Criterion

New sub-skills are justified ONLY when tools share a distinct workflow pipeline AND a distinct security zone profile AND tool count exceeds 10 in an existing sub-skill. Document justification per ADR-PROJ023-001 risk R-1.

---

## References

| Source | Content |
|--------|---------|
| ADR-PROJ023-001 | Rainbow Series Cybersecurity Skill Architecture (composable design, agent registry, security zones) |
| `/red-team` SKILL.md | Offensive methodology skill (methodology guidance, not tool execution) |
| `/eng-team` SKILL.md | Secure engineering skill (defensive development) |
| `docs/governance/JERRY_CONSTITUTION.md` | Constitutional principles |
| `.context/rules/quality-enforcement.md` | Quality gate thresholds |
| `.context/rules/agent-development-standards.md` | Agent definition standards (H-34, tool tiers) |
| `.context/rules/agent-routing-standards.md` | Routing standards (H-36, circuit breaker) |

---

*Skill Version: 1.0.0*
*Constitutional Compliance: Jerry Constitution v1.0*
*SSOT: ADR-PROJ023-001*
*Created: 2026-03-14*
