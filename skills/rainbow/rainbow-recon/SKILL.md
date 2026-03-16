---
name: rainbow-recon
description: >-
  Reconnaissance sub-skill of /rainbow. Provides systematic active
  reconnaissance pipelines and OSINT collection within authorized engagement
  scope. Uses Subfinder, httpx, dnsx, Naabu, Katana, Nuclei (detection
  templates), OWASP Amass, and Maigret. Zone 2 (active reconnaissance) --
  requires validated engagement scope document. Invoke for: subdomain
  enumeration, port scanning, HTTP probing, DNS resolution, web crawling,
  vulnerability detection, OSINT, attack surface mapping, username enumeration,
  reconnaissance pipeline.
version: "1.0.0"
agents:
  - rainbow-recon-pipeline
  - rainbow-recon-osint
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
activation-keywords:
  - "subdomain enumeration"
  - "port scanning"
  - "HTTP probing"
  - "DNS resolution"
  - "web crawling"
  - "vulnerability scanning"
  - "reconnaissance"
  - "recon pipeline"
  - "attack surface"
  - "OSINT"
  - "Subfinder"
  - "httpx"
  - "dnsx"
  - "Naabu"
  - "Katana"
  - "Nuclei"
  - "Amass"
  - "Maigret"
  - "username enumeration"
  - "certificate transparency"
---

# Rainbow Recon Sub-Skill

> **Version:** 1.0.0
> **Parent Skill:** /rainbow
> **Constitutional Compliance:** Jerry Constitution v1.0
> **SSOT Reference:** ADR-PROJ023-001 (Rainbow Series Cybersecurity Skill Architecture)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Purpose](#purpose) | Sub-skill identity and scope |
| [When to Use](#when-to-use) | Activation conditions and exclusions |
| [Agent Registry](#agent-registry) | Agent table with roles and zones |
| [Tool Inventory](#tool-inventory) | Tools with CLI patterns, tiers, and zone mapping |
| [Security Zone Enforcement](#security-zone-enforcement) | Zone 2 default with Zone 3 Nuclei escalation |
| [Credential Filter](#credential-filter) | Mandatory output sanitization |
| [Internal Routing](#internal-routing) | How rainbow-orchestrator routes to this sub-skill |
| [Cross-Sub-Skill Data Contracts](#cross-sub-skill-data-contracts) | Pipeline integration with other sub-skills |
| [Known Limitations](#known-limitations) | Honest limitations disclosure per P-022 |
| [Constitutional Compliance](#constitutional-compliance) | Governance alignment |
| [Acceptance Criteria Coverage Matrix](#acceptance-criteria-coverage-matrix) | AC-to-file traceability |

---

## Purpose

The `/rainbow-recon` sub-skill provides **tool-assisted active reconnaissance and OSINT collection** within authorized engagement boundaries. It covers the reconnaissance lifecycle: subdomain enumeration, DNS resolution, HTTP probing, port scanning, web crawling, vulnerability detection scanning, and open-source intelligence gathering.

This sub-skill is part of the /rainbow composable architecture (ADR-PROJ023-001, Wave 2a). It operates exclusively in **Zone 2 (Active Reconnaissance)** and requires a validated engagement scope document before any operation.

### Key Capabilities

- **Subdomain Enumeration** -- Discover subdomains for authorized target domains (Subfinder)
- **HTTP Probing** -- Probe discovered hosts for live HTTP services and technology detection (httpx)
- **DNS Resolution** -- Resolve DNS records for comprehensive domain intelligence (dnsx)
- **Port Scanning** -- Discover open ports on authorized target hosts (Naabu)
- **Web Crawling** -- Crawl authorized web applications for endpoint and parameter discovery (Katana)
- **Vulnerability Detection** -- Template-based vulnerability detection scanning (Nuclei -- detection templates only at Zone 2)
- **Attack Surface Mapping** -- Deep OSINT-based attack surface mapping with certificate transparency, ASN, and WHOIS data (OWASP Amass)
- **Username OSINT** -- Enumerate usernames across 3,000+ platforms (Maigret)

### What This Sub-Skill Is NOT

- Does NOT exploit vulnerabilities (use `/rainbow-exploit`)
- Does NOT generate SBOMs or scan supply chains (use `/rainbow-supply-chain`)
- Does NOT audit cloud configurations (use `/rainbow-cloud`)
- Does NOT intercept traffic or instrument processes (use `/rainbow-runtime`)
- Does NOT provide penetration testing methodology without tool execution (use `/red-team`)
- Does NOT provide secure development guidance (use `/eng-team`)
- Does NOT perform malware analysis or threat detection (use `/blue-team`)

---

## When to Use

Activate when the request involves:

- Enumerating subdomains for a target domain
- Scanning for open ports on authorized targets
- Probing HTTP services and detecting technologies
- Resolving DNS records for domain intelligence
- Crawling web applications for endpoints
- Running Nuclei detection templates against authorized targets
- Gathering OSINT on authorized targets or usernames
- Mapping attack surfaces with Amass
- Building reconnaissance pipelines

Do NOT invoke when:

- Task requires vulnerability exploitation -- use `/rainbow-exploit`
- Task requires supply chain scanning -- use `/rainbow-supply-chain`
- Task requires cloud security posture assessment -- use `/rainbow-cloud`
- Task is malware analysis or threat detection -- use `/blue-team`
- Task is penetration testing methodology without tool execution -- use `/red-team`
- No engagement scope document exists -- create one first via `engagement-scope-template.yaml`

---

## Agent Registry

| Agent | Role | Zone | Tools | Cognitive Mode | Tier |
|-------|------|------|-------|---------------|------|
| `rainbow-recon-pipeline` | Systematic reconnaissance pipeline orchestrator | Zone 2 | Subfinder, httpx, dnsx, Naabu, Katana, Nuclei (detection) | systematic | Tier A |
| `rainbow-recon-osint` | OSINT and passive reconnaissance specialist | Zone 2 | OWASP Amass, Maigret | divergent | Tier B |

**Tool tier:** Both agents are T2 (Read-Write). Neither agent has Task tool access per H-34/P-003.

### Agent Selection Guide

| Request Type | Agent | Rationale |
|-------------|-------|-----------|
| Subdomain discovery, port scanning, HTTP probing, vulnerability scanning | `rainbow-recon-pipeline` | Pipeline handles active reconnaissance tools |
| OSINT, attack surface mapping, username enumeration, certificate transparency | `rainbow-recon-osint` | OSINT specialist handles passive intelligence gathering |
| Full reconnaissance (active + OSINT) | Both, sequenced by orchestrator | Pipeline first (active recon), then OSINT (complementary intelligence) |

---

## Tool Inventory

### Tier A Tools (Agent: rainbow-recon-pipeline)

| Tool | Version | CLI Pattern | Output | Zone 2 Operations |
|------|---------|-------------|--------|-------------------|
| **Subfinder** | >= 2.6 | `subfinder -d <domain> -oJ -o output.json` | JSONL | Subdomain enumeration |
| **httpx** | >= 1.6 | `httpx -l targets.txt -json -o results.json` | JSONL | HTTP probing, technology detection |
| **dnsx** | >= 1.2 | `dnsx -l subdomains.txt -json -o results.json` | JSONL | DNS resolution, record enumeration |
| **Naabu** | >= 2.4 | `naabu -l targets.txt -json -o results.json` | JSONL | Port scanning with rate limits |
| **Katana** | >= 1.0 | `katana -u <url> -jsonl -o results.json` | JSONL | Web crawling with depth limits |
| **Nuclei** | >= 3.0 | `nuclei -l targets.txt -jsonl -o results.json` | JSONL | Detection templates (Zone 2); exploit templates (Zone 3) |

### Tier B Tools (Agent: rainbow-recon-osint)

| Tool | Version | CLI Pattern | Output | Zone 2 Operations |
|------|---------|-------------|--------|-------------------|
| **OWASP Amass** | >= 4.2 | `amass enum -d <domain> -json output.json` | JSON | Attack surface mapping (passive/active) |
| **Maigret** | >= 0.4 | `maigret <username> --json output.json` | JSON | Username OSINT across 3,000+ sites |

### Tier C Tools (Methodology Reference Only)

No Tier C tools for /rainbow-recon. All tools are Tier A or B with direct CLI execution.

### Tool Pipeline Flow

```
Subfinder (subdomains)
    |
    v
dnsx (DNS resolution)
    |
    v
httpx (HTTP probing)    Naabu (port scanning)
    |                       |
    v                       v
Katana (web crawling)   [merge live targets]
    |                       |
    +----------+------------+
               |
               v
        Nuclei (detection scan)
```

OSINT runs in parallel:
```
Amass (attack surface mapping) --> correlate with pipeline findings
Maigret (username OSINT)       --> correlate with pipeline findings
```

---

## Security Zone Enforcement

**Default zone:** Zone 2 (Active Reconnaissance). ALL operations require engagement scope validation.

### Zone Classification

| Zone | Operations | Authorization |
|------|-----------|---------------|
| **Zone 2** | All Subfinder, httpx, dnsx, Naabu, Katana operations; Nuclei detection templates; Amass enum; Maigret search | Engagement scope required (operator-approved) |
| **Zone 3** | Nuclei exploit templates (matching deny_tags per `nuclei-template-allowlist.yaml`, 11 tags as of v1.0); custom/community templates not on allowlist | Per-operation human approval required |

### Dual-Zone Nuclei Classification

Nuclei is the only dual-zone tool in /rainbow-recon. Classification is based on template content, not agent judgment.

| Nuclei Operation | Zone | Rule |
|-----------------|------|------|
| Detection templates on allowlist | Zone 2 | Template in `nuclei-template-allowlist.yaml`; no deny_tags; no deny_extractor_fields |
| Exploit templates | Zone 3 | Template matches deny_tags list |
| Credential-extracting templates | Zone 3 | Template extractors target credential fields |
| Custom/community templates | Zone 3 | Fail-closed: default to Zone 3 until reviewed |

See `skills/rainbow/rainbow-recon/rules/nuclei-template-allowlist.yaml` for the allowlist.
See `skills/rainbow/rainbow-recon/rules/nuclei-escalation-protocol.md` for the escalation procedure.

### Enforcement Layers

1. **Agent-level guardrails:** Each agent validates targets against engagement scope before every tool invocation.
2. **Sub-skill rules:** This SKILL.md declares Zone 2 with explicit Zone 3 escalation for Nuclei.
3. **Parent orchestrator:** `rainbow-orchestrator` validates engagement scope before routing Zone 2 requests.
4. **Nuclei template gate:** `rainbow-recon-pipeline` classifies every Nuclei template before execution.

---

## Credential Filter

The credential filter pipeline is MANDATORY for all tool output. No tool output enters the context window without passing through the 3-layer filter.

| Layer | Mechanism | Relevance to Reconnaissance |
|-------|-----------|---------------------------|
| L1 | Regex pattern matching | Reconnaissance output may surface API keys, tokens in HTTP headers |
| L2 | Entropy detection | OSINT and Amass output may contain encoded credentials from breaches |
| L3 | Structural analysis | JSON scan output may contain sensitive key-value pairs |

**Full specification:** `skills/rainbow/rules/rainbow-credential-filter.md`

**Fail-closed behavior:** Filter crash or timeout rejects the entire tool output block. Flagged content quarantined to `work/.credential-quarantine/`.

**Zone 2 heightened sensitivity:** Zone 2 agents MUST treat any credential filter quarantine event as a potential credential exposure. The agent MUST: (1) log the quarantine event, (2) notify the user per P-020, (3) NOT re-run the tool to obtain quarantined output, (4) continue with remaining tasks using non-quarantined output.

---

## Internal Routing

The `rainbow-orchestrator` routes to this sub-skill based on request keywords.

### Activation Keywords (from rainbow-orchestrator)

Reconnaissance keywords that trigger routing to this sub-skill:
- Subdomain enumeration, port scanning, HTTP probing, DNS resolution, web crawling
- Vulnerability scanning (detection), reconnaissance pipeline, attack surface mapping
- OSINT, username enumeration, certificate transparency
- Tool names: Subfinder, httpx, dnsx, Naabu, Katana, Nuclei, Amass, Maigret

### Agent Selection Within Sub-Skill

| Request Type | Agent | Rationale |
|-------------|-------|-----------|
| Active reconnaissance (scanning, probing, crawling) | `rainbow-recon-pipeline` | Pipeline handles systematic active recon |
| OSINT and passive intelligence gathering | `rainbow-recon-osint` | OSINT specialist for divergent intelligence |
| Full reconnaissance engagement | Both, sequenced | Pipeline first, then OSINT for correlation |

---

## Cross-Sub-Skill Data Contracts

### Reconnaissance to Exploit Pipeline (Cross-Sub-Skill)

Nuclei vulnerability findings feed into /rainbow-exploit for exploitation assessment. This cross-sub-skill handoff is managed by `rainbow-orchestrator` per handoff-v2.schema.json.

| Stage | Source Agent | Target Agent | Data | Orchestrator Action |
|-------|-------------|-------------|------|-------------------|
| 1 | `rainbow-recon-pipeline` (Nuclei) | `/rainbow-exploit` agents | Vulnerability findings JSONL | Construct handoff with artifact path; Zone 3 approval required |

**Minimum Entry Schema (JSONL):**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `template-id` | string | Yes | Nuclei template identifier |
| `matched-at` | string | Yes | Target URL or endpoint where finding was detected |
| `severity` | enum | Yes | `info`, `low`, `medium`, `high`, `critical` |
| `host` | string | Yes | Target host |
| `timestamp` | string | Yes | ISO 8601 detection timestamp |
| `info.name` | string | Yes | Template name (human-readable finding title) |

**Empty-Result Handling:** If Nuclei produces zero findings (no vulnerabilities detected), the source agent MUST: (1) persist an empty JSONL artifact with a header comment noting zero findings, (2) include `result_count: 0` in the handoff `key_findings`, (3) set handoff `confidence` to 0.9 (high -- scan completed successfully with no findings). The orchestrator MUST NOT route to `/rainbow-exploit` when findings are empty.

**Handoff Quality:** Handoff follows `handoff-v2.schema.json`. Required: `confidence` >= 0.7 before routing to exploit pipeline. `key_findings` MUST include finding count by severity, target coverage percentage, and any scan limitations.

### Supply Chain to Recon Pipeline (Cross-Sub-Skill)

Grype vulnerability reports from /rainbow-supply-chain feed into Nuclei for web-facing validation.

| Stage | Source Agent | Target Agent | Data | Orchestrator Action |
|-------|-------------|-------------|------|-------------------|
| 1 | `rainbow-sc-scanner` (Grype) | `rainbow-recon-pipeline` (Nuclei) | Vulnerability report JSON | Construct handoff with artifact path |

**Minimum Entry Schema (JSON):**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `vulnerability.id` | string | Yes | CVE or advisory identifier |
| `vulnerability.severity` | enum | Yes | Severity rating |
| `artifact.name` | string | Yes | Affected package name |
| `artifact.version` | string | Yes | Affected package version |

**Empty-Result Handling:** If Grype reports zero vulnerabilities, the source agent MUST: (1) persist the clean scan report, (2) include `vulnerability_count: 0` in handoff `key_findings`, (3) set `confidence` to 0.9. The orchestrator SHOULD still route to recon pipeline if the operator has authorized web-facing validation regardless of supply chain findings.

**Handoff Quality:** Handoff follows `handoff-v2.schema.json`. Required: `confidence` >= 0.6 (supply chain findings are preliminary and may not have web-facing exposure).

### Recon to Cloud Pipeline (Cross-Sub-Skill)

Cloud infrastructure discovered via Amass or Subfinder feeds into /rainbow-cloud for posture assessment.

| Stage | Source Agent | Target Agent | Data | Orchestrator Action |
|-------|-------------|-------------|------|-------------------|
| 1 | `rainbow-recon-osint` (Amass) | `/rainbow-cloud` agents | Cloud asset discovery JSON | Construct handoff with artifact path |

**Minimum Entry Schema (JSON):**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Asset identifier (domain, IP, cloud resource) |
| `type` | enum | Yes | Asset type (e.g., `domain`, `ip`, `cloud_service`) |
| `source` | string | Yes | Discovery source (e.g., `amass`, `subfinder`) |

**Empty-Result Handling:** If Amass discovers zero cloud assets, the source agent MUST: (1) persist the empty discovery report, (2) include `cloud_asset_count: 0` in handoff `key_findings`, (3) set `confidence` to 0.7 (absence of cloud assets may indicate incomplete OSINT rather than true absence). The orchestrator MUST NOT route to `/rainbow-cloud` when no cloud assets are discovered.

**Handoff Quality:** Handoff follows `handoff-v2.schema.json`. Required: `confidence` >= 0.6 (OSINT discovery completeness is inherently uncertain).

---

## Known Limitations

> Honest disclosure per P-022. These are accepted architectural limitations documented in ADR-PROJ023-001.

### Zone Enforcement Is Behavioral-Only

Zone enforcement relies on LLM behavioral compliance with subcommand allowlists. No L3 runtime gate validates Bash commands before execution.

**Compensating controls:**
1. **Bash subcommand allowlists** -- Both agents declare `bash_subcommand_allowlist_zone_2` in `.governance.yaml`
2. **NPT-009-complete forbidden actions** -- Zone violation entries use structured negation with consequences
3. **BDD zone enforcement scenarios** -- Both agents have BDD scenarios testing zone escalation and boundary refusal
4. **Engagement scope validation** -- Every tool invocation gated by engagement scope checks
5. **Nuclei template gate** -- Template classification procedure is deterministic and documented

### Credential Filter Is W0 Specification-Only

The credential filter pipeline is a W0 specification. Both agents declare `credential_filter_applied_to_all_tool_output` as a behavioral constraint. Runtime enforcement deferred to W1.

**Compensating controls:**
1. **Three-layer specification** -- L1 regex, L2 entropy, L3 structural fully specified in `rainbow-credential-filter.md`
2. **Behavioral declaration** -- Both agents include credential filter in `output_filtering`
3. **Fail-closed specification** -- Filter crash or timeout rejects entire tool output block
4. **BDD credential filter scenarios** -- Both agents have credential filter application and quarantine scenarios

### Nuclei Template Classification Is LLM-Parsed

Nuclei template classification relies on the agent parsing template YAML and checking against the allowlist. This is an LLM-driven classification, not a deterministic runtime gate.

**Compensating controls:**
1. **Allowlist + deny-tag approach** -- Explicit allowlist with fail-closed default to Zone 3
2. **Deterministic classification procedure** -- Step-by-step procedure documented in `nuclei-escalation-protocol.md`
3. **BDD scenarios** -- Template classification scenarios in test suite
4. **Human approval for Zone 3** -- All Zone 3 templates require per-operation human approval (P-020)

### Engagement Scope Validation Is Agent-Enforced

Engagement scope validation is performed by the agent before each operation. No middleware intercepts and validates scope before tool execution.

**Compensating controls:**
1. **scope_gate_halt guardrail** -- Both agents declare HALT behavior when scope is missing
2. **Pre-execution gate** -- Both agents document the 5-check validation procedure
3. **BDD scenarios** -- Scope validation scenarios in test suite
4. **Audit logging** -- Every operation logs `target_authorized` and `technique_authorized` fields

### Pipeline Agent Operates 6 CLI Tools (AC-F-17 Exception)

The `rainbow-recon-pipeline` agent operates 6 CLI tools (Subfinder, httpx, dnsx, Naabu, Katana, Nuclei) against the AC-F-17 design target of maximum 5 CLI tools per agent. This is a documented exception per AP-07 (Tool Overload Creep) analysis.

**Justification:** All 6 tools are from the ProjectDiscovery ecosystem and share unified CLI patterns (JSONL output, `-l` list input, consistent flag conventions). They form a single sequential reconnaissance pipeline where each tool's output feeds the next stage. The agent never selects between tools based on context -- it executes the full pipeline in fixed order. This is functionally a single pipeline with 6 stages, not 6 independent tool selections.

**Compensating controls:**
1. **Sequential pipeline execution** -- Only one tool is active at any time; no parallel tool selection decision
2. **Unified CLI patterns** -- All 6 tools share ProjectDiscovery conventions (JSONL output, `-l`/`-u` input, `-o` output), reducing tool selection complexity
3. **Fixed pipeline order** -- Subfinder -> dnsx -> httpx -> Naabu -> Katana -> Nuclei; agent does not dynamically select which tools to run
4. **AP-07 monitoring** -- Tool count monitored; if additional tools are needed, they route to `rainbow-recon-osint` instead

### Tool Availability Is Environment-Dependent

All reconnaissance tools must be installed in the execution environment. Tool availability is not guaranteed.

**Compensating controls:**
1. **AD-010 degradation levels** -- Level 0 (full tools), Level 1 (partial), Level 2 (standalone guidance)
2. **P-022 disclosure** -- Agent discloses when tools are unavailable and operates in degraded mode
3. **Container infrastructure** -- Planned via T0.8 for consistent tool availability (deferred)

---

## Constitutional Compliance

| Principle | Application |
|-----------|-------------|
| **P-003 / H-01** | Both agents are T2 workers. No Task tool access. No delegation. |
| **P-020 / H-02** | Reconnaissance scope approved by user. Engagement scope required. Zone 3 escalation requires per-operation human approval. |
| **P-022 / H-03** | Scan coverage limitations disclosed. Tool availability reported. Nuclei template classification transparent. Known limitations documented above. |
| **P-001** | All findings evidence-based with tool output citations and template/CVE references. |
| **P-002** | All scan reports, JSONL artifacts, and audit logs persisted. |
| **H-34** | Both agents use dual-file architecture (.md + .governance.yaml). Constitutional compliance triplet in every agent. |

---

## Acceptance Criteria Coverage Matrix

| AC | Description | Satisfied By |
|----|-------------|-------------|
| AC-F-02 | Agent definition follows dual-file architecture (H-34) | `agents/rainbow-recon-pipeline.md` + `.governance.yaml`; `agents/rainbow-recon-osint.md` + `.governance.yaml` |
| AC-F-03 | Constitutional compliance triplet (H-35) | All `.governance.yaml` files: `constitution.principles_applied` includes P-003, P-020, P-022; `capabilities.forbidden_actions` >= 3 entries |
| AC-F-04 | Zone enforcement rules and escalation protocols | `rules/nuclei-template-allowlist.yaml` (dual-zone classification); `rules/nuclei-escalation-protocol.md` (Zone 2->3 procedure); SKILL.md [Security Zone Enforcement](#security-zone-enforcement) |
| AC-F-16 | BDD scenarios per agent (H-20) | `tests/bdd/test_recon_pipeline.feature` (34 scenarios); `tests/bdd/test_recon_osint.feature` (29 scenarios) |
| AC-F-17 | Credential filter integration | SKILL.md [Credential Filter](#credential-filter); both agent `.md` files Credential Filter Application section; BDD credential filter scenarios in both feature files |
| H-20 | BDD test-first, 90% line coverage | 63 total BDD scenarios across 2 agents covering: engagement scope, tool workflows, credential filter, constitutional, adversarial, degradation |

---

## References

| Source | Content |
|--------|---------|
| ADR-PROJ023-001 | Architecture decision: composable sub-skill structure, agent registry, zone classification |
| `skills/rainbow/SKILL.md` | Parent skill: routing, engagement lifecycle, security zone overview |
| `skills/rainbow/rules/rainbow-credential-filter.md` | Credential filter 3-layer specification |
| `skills/rainbow/rules/zone-2-active.md` | Zone 2 guardrail profile |
| `skills/rainbow/rules/engagement-lifecycle.md` | Engagement lifecycle model |
| `skills/rainbow/rules/engagement-scope-template.yaml` | Engagement scope template |
| `skills/rainbow/rules/rules-of-engagement-template.md` | Rules of engagement template |
| `skills/rainbow/rainbow-recon/rules/nuclei-template-allowlist.yaml` | Nuclei template Zone 2/3 classification |
| `skills/rainbow/rainbow-recon/rules/nuclei-escalation-protocol.md` | Nuclei dual-zone escalation procedure |
| Tool documentation cache | `projects/PROJ-023-exploit-framework/work/research/tool-docs-cache.md` |

---

*Sub-Skill Version: 1.0.0*
*Constitutional Compliance: Jerry Constitution v1.0*
*SSOT: ADR-PROJ023-001*
*Created: 2026-03-16*
