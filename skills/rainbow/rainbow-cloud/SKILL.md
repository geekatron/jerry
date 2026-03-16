---
name: rainbow-cloud
description: >-
  Cloud security sub-skill of /rainbow. Provides cloud security posture
  assessment, IaC auditing, Kubernetes policy validation, cloud compliance
  scanning, and infrastructure relationship mapping. Uses Checkov (IaC),
  Prowler (AWS/Azure/GCP), Kubescape (K8s), Kyverno CLI (policy), and
  Cartography (infrastructure graphing). Zone 1 (analysis) for local IaC
  and manifest scanning. Zone 2 (active) for live cloud and cluster
  operations. Kyverno is dual-zone: validate=Z1, mutate=Z2, generate=Z3.
  Invoke for: cloud compliance, IaC audit, Kubernetes security, cloud
  posture, Prowler, Kubescape, Kyverno, Checkov, cloud asset mapping,
  Cartography, infrastructure graph.
version: "1.0.0"
agents:
  - rainbow-cloud-auditor
  - rainbow-cloud-mapper
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
activation-keywords:
  - "cloud compliance"
  - "cloud posture"
  - "cloud security"
  - "IaC audit"
  - "IaC scan"
  - "Kubernetes security"
  - "K8s security"
  - "Kyverno"
  - "Kubescape"
  - "Prowler"
  - "Checkov"
  - "Cartography"
  - "cloud asset mapping"
  - "infrastructure graph"
  - "CIS benchmark cloud"
  - "cloud compliance scan"
  - "cloud infrastructure mapping"
---

# Rainbow Cloud Sub-Skill

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
| [Tool Inventory](#tool-inventory) | Tools with CLI patterns and zone mapping |
| [Security Zone Enforcement](#security-zone-enforcement) | Zone 1/2 with dual-zone Kyverno |
| [Credential Filter](#credential-filter) | Mandatory output sanitization |
| [Internal Routing](#internal-routing) | How rainbow-orchestrator routes to this sub-skill |
| [Cross-Sub-Skill Data Contracts](#cross-sub-skill-data-contracts) | Pipeline integration with other sub-skills |
| [Known Limitations and Compensating Controls](#known-limitations-and-compensating-controls) | P-022 honest disclosure |
| [Constitutional Compliance](#constitutional-compliance) | Governance alignment |

---

## Purpose

The `/rainbow-cloud` sub-skill provides **tool-assisted cloud security posture assessment and infrastructure mapping**. It covers cloud compliance auditing, IaC security scanning, Kubernetes policy validation, and infrastructure relationship discovery.

This sub-skill is part of the /rainbow composable architecture (ADR-PROJ023-001, Wave 2). It delivers independent value without requiring other /rainbow sub-skills to be operational.

### Key Capabilities

- **IaC Security Scanning** -- Scan Terraform, CloudFormation, Kubernetes, Helm, Dockerfile, Bicep, and ARM templates for misconfigurations (Checkov)
- **Cloud Compliance Auditing** -- Audit AWS, Azure, and GCP accounts against CIS, PCI-DSS, HIPAA, SOC 2, and GDPR frameworks (Prowler)
- **Kubernetes Security Posture** -- Assess K8s clusters and manifests against NSA-CISA, CIS, MITRE ATT&CK, and SOC 2 frameworks (Kubescape)
- **Kubernetes Policy Validation** -- Validate resources against policies with dual-zone enforcement: validate at Zone 1, mutate at Zone 2, generate at Zone 3 (Kyverno CLI)
- **Infrastructure Relationship Mapping** -- Discover cloud asset relationships, attack surface exposure, and IAM trust chains via graph analysis (Cartography + Neo4j)

### What This Sub-Skill Is NOT

- Does NOT provide network reconnaissance or active target probing (use `/rainbow-recon`)
- Does NOT provide exploit execution or penetration testing (use `/rainbow-exploit`)
- Does NOT sign or attest artifacts (Zone 3 -- managed by `rainbow-orchestrator`)
- Does NOT provide secure development guidance or threat modeling (use `/eng-team`)
- Does NOT perform malware analysis or author detection rules (use `/blue-team`)

---

## When to Use

Activate when the request involves:

- Scanning IaC templates for security misconfigurations
- Auditing cloud account security posture against compliance frameworks
- Assessing Kubernetes cluster or manifest security
- Validating Kubernetes resources against Kyverno policies
- Mapping cloud infrastructure assets and discovering relationships
- Identifying attack surface exposure and IAM trust chains

Do NOT invoke when:

- Task requires network reconnaissance or active target probing -- use `/rainbow-recon`
- Task requires exploit execution -- use `/rainbow-exploit`
- Task is malware analysis or threat detection -- use `/blue-team`
- Task is penetration testing methodology without tool execution -- use `/red-team`
- Task is building secure software or threat modeling -- use `/eng-team`
- Task is supply chain scanning (SBOM, CVE, signature verification) -- use `/rainbow-supply-chain`

---

## Agent Registry

| Agent | Role | Zone | Tools | Cognitive Mode |
|-------|------|------|-------|---------------|
| `rainbow-cloud-auditor` | Cloud security posture auditor | Zone 1/2 | Checkov, Prowler, Kubescape, Kyverno | systematic |
| `rainbow-cloud-mapper` | Cloud infrastructure relationship mapper | Zone 2 | Cartography (+ Neo4j) | divergent |

**Tool tier:** Both agents are T2 (Read-Write). Neither agent has Task tool access per H-34/P-003.

---

## Tool Inventory

| Tool | Version | Agent | Zone 1 Operations | Zone 2 Operations | Zone 3 Operations |
|------|---------|-------|-------------------|-------------------|-------------------|
| **Checkov** | >= 3.0 | auditor | `-d`, `-f`, `--framework` (scan) | `--fix` (remediation) | -- |
| **Prowler** | >= 4.0 | auditor | -- | `aws`, `azure`, `gcp` (live cloud audit) | -- |
| **Kubescape** | >= 3.0 | auditor | `scan <local-manifest>` | `scan` (live cluster) | -- |
| **Kyverno** | >= 1.11 | auditor | `apply --resource`, `test`, `json` | `apply` (mutate, no `--resource`) | `generate` (NOT available) |
| **Cartography** | >= 0.90 | mapper | -- | Cloud asset sync to Neo4j | -- |

### CLI Quick Reference

| Tool | Primary Command | Output Flag |
|------|----------------|-------------|
| Checkov | `checkov -d <dir> --output json --framework <fw>` | `--output json` |
| Prowler | `prowler <provider> --output-formats json-ocsf` | `--output-formats json-ocsf` |
| Kubescape | `kubescape scan <target> --format json --output <file>` | `--format json` |
| Kyverno | `kyverno apply <policy> --resource <resource>` | `--policy-report` |
| Cartography | `cartography --neo4j-uri bolt://<host>:7687` | Neo4j graph database |

---

## Security Zone Enforcement

**Default zone:** Zone 1 (Analysis) for local IaC and manifest operations. Zone 2 for live cloud/cluster operations.

### Zone Classification

| Zone | Operations | Authorization |
|------|-----------|---------------|
| **Zone 1** | Checkov scan mode; Kubescape local manifest scan; Kyverno apply with `--resource`, test, json | Project scope only (H-04) |
| **Zone 2** | Prowler cloud auditing; Kubescape live cluster scan; Kyverno mutate (apply without `--resource`); Cartography cloud sync | Engagement scope required |
| **Zone 3** | Kyverno generate mode | NOT available to sub-skill agents. Per-operation approval via rainbow-orchestrator. |

### Dual-Zone Tool: Kyverno

Kyverno is the only tool in this sub-skill that spans all three zones. Classification is deterministic based on policy content and CLI flags:

| Kyverno Mode | Zone | Boundary Marker | Rule |
|-------------|------|-----------------|------|
| Validate (apply with `--resource`) | Zone 1 | `--resource` flag present | Local-only evaluation |
| Test | Zone 1 | `test` subcommand | Local test case execution |
| JSON validation | Zone 1 | `json` subcommand | Local payload validation |
| Mutate (apply without `--resource`) | Zone 2 | No `--resource` flag, cluster context | Live cluster enforcement |
| Generate | Zone 3 | Policy contains `generate` rules | NEVER execute |

See `skills/rainbow/rainbow-cloud/rules/kyverno-escalation-protocol.md` for the full escalation protocol.
See `skills/rainbow/rainbow-cloud/rules/kyverno-dryrun-enforcement.yaml` for dry-run enforcement configuration.

### Enforcement Layers

1. **Agent-level guardrails:** Each agent validates CLI subcommands against its zone allowlist before execution.
2. **Sub-skill rules:** This SKILL.md declares zone classification with explicit escalation conditions.
3. **Kyverno escalation protocol:** Dedicated rule file classifies every Kyverno operation by zone.
4. **Parent orchestrator:** `rainbow-orchestrator` validates engagement scope before routing Zone 2 requests.

### Escalation Triggers

| Trigger | From | To | Action |
|---------|------|----|--------|
| Prowler cloud scan requested | N/A | Zone 2 | Agent validates engagement scope. If absent, halts and escalates. |
| Kubescape live cluster scan requested | Zone 1 | Zone 2 | Agent validates engagement scope. If absent, halts and escalates. |
| Kyverno mutate mode requested | Zone 1 | Zone 2 | Agent classifies policy, validates scope. If absent, halts and escalates. |
| Kyverno generate mode detected | Any | Zone 3 | Agent NEVER executes. Informs user. Returns to orchestrator. |
| Checkov `--fix` requested | Zone 1 | Zone 2 | Agent halts. Returns to orchestrator for scope validation. |
| Cartography cloud sync requested | N/A | Zone 2 | Agent validates engagement scope with authorized cloud accounts. |

See `skills/rainbow/rules/zone-1-analysis.md` and `skills/rainbow/rules/zone-2-active.md` for full guardrail profiles.

---

## Credential Filter

The credential filter pipeline is MANDATORY for all tool output. No tool output enters the context window without passing through the 3-layer filter.

| Layer | Mechanism | Relevance to Cloud Security |
|-------|-----------|--------------------------|
| L1 | Regex pattern matching | Cloud audit output may contain AWS access keys, Azure client secrets, GCP service account keys |
| L2 | Entropy detection | Base64-encoded credentials in cloud configuration metadata and policy definitions |
| L3 | Structural analysis | JSON/YAML cloud audit output (Prowler, Checkov, Kubescape) may contain sensitive key-value pairs |

**Full specification:** `skills/rainbow/rules/rainbow-credential-filter.md`

**Fail-closed behavior:** Filter crash or timeout rejects the entire tool output block. Flagged content quarantined to `work/.credential-quarantine/`.

**Cloud-specific heightened sensitivity:** Cloud audit tools (Prowler, Cartography) process cloud provider credentials for API access. The agent MUST NEVER log, expose, or include cloud provider credentials in any output or context window entry.

---

## Known Limitations and Compensating Controls

> Honest disclosure per P-022. These are accepted architectural limitations documented in ADR-PROJ023-001.

### Zone Enforcement Is Behavioral-Only

Zone enforcement relies on LLM behavioral compliance with subcommand allowlists. No L3 runtime gate validates Bash commands before execution.

**Compensating controls:**
1. **Bash subcommand allowlists** -- Both agents declare zone-specific allowlists in `.governance.yaml`
2. **NPT-009-complete forbidden actions** -- Zone violation entries use structured negation with consequences
3. **BDD zone enforcement scenarios** -- Both agents have BDD scenarios testing zone escalation and boundary refusal
4. **Kyverno escalation protocol** -- Dedicated rule file provides deterministic zone classification for Kyverno operations

### Credential Filter Is W0 Specification-Only

The credential filter pipeline is a W0 specification. Both agents declare `credential_filter_applied_to_all_tool_output` as a behavioral constraint. Runtime enforcement deferred to W1.

**Compensating controls:**
1. **Three-layer specification** -- L1 regex, L2 entropy, L3 structural analysis fully specified
2. **Behavioral declaration** -- Both agents include credential filter in `output_filtering`
3. **Fail-closed specification** -- Filter crash or timeout rejects entire tool output block
4. **BDD credential filter scenarios** -- Both agents have credential filter application and quarantine scenarios

### Cartography Requires Neo4j Sidecar

Cartography requires a running Neo4j database. Container orchestration for the Neo4j sidecar is deferred to T0.8 (Docker Compose infrastructure phase).

**Compensating controls:**
1. **Level 1/2 degradation** -- rainbow-cloud-mapper functions at reduced capability without Neo4j
2. **Methodology guidance** -- Agent provides Cypher query patterns and expected graph structures without execution
3. **Docker placeholder** -- `skills/rainbow/rainbow-cloud/tests/docker/README.md` documents the Neo4j dependency

### Prowler Scan Duration

Prowler cloud account scans may take 15-60 minutes for comprehensive assessment. This is an inherent cloud API query latency issue.

**Compensating controls:**
1. **Targeted scanning** -- Use `--checks <check-id>` or `--compliance <framework>` to scope specific assessments
2. **Severity filtering** -- Use `--severity <level>` to prioritize high-severity findings
3. **Duration reporting** -- Agent reports estimated and actual scan duration in audit logs

---

## Internal Routing

The `rainbow-orchestrator` routes to this sub-skill based on request keywords.

### Activation Keywords (from rainbow-orchestrator)

Cloud security keywords that trigger routing to this sub-skill:
- Cloud compliance, cloud posture, IaC audit, Kubernetes security, K8s security
- Tool names: Checkov, Prowler, Kubescape, Kyverno, Cartography
- Cloud asset mapping, infrastructure graph, CIS benchmark (cloud context)

### Agent Selection Within Sub-Skill

| Request Type | Agent | Rationale |
|-------------|-------|-----------|
| IaC scanning, cloud compliance audit, K8s posture, policy validation | `rainbow-cloud-auditor` | Auditor handles all compliance and policy tools |
| Infrastructure mapping, asset discovery, relationship analysis | `rainbow-cloud-mapper` | Mapper handles Cartography and graph analysis |
| Mixed (audit + map) | Both, sequenced by orchestrator | Auditor first (compliance baseline), then mapper (relationship discovery) |

---

## Cross-Sub-Skill Data Contracts

### Cloud Audit to Recon Pipeline (Cross-Sub-Skill)

Prowler and Kubescape findings may identify targets that warrant deeper reconnaissance. This cross-sub-skill handoff is managed by `rainbow-orchestrator`.

| Stage | Source Agent | Target Agent | Data | Orchestrator Action |
|-------|-------------|-------------|------|-------------------|
| 1 | `rainbow-cloud-auditor` (Prowler) | `rainbow-recon-pipeline` (Nuclei) | Publicly exposed endpoints from cloud audit | Construct handoff with artifact path |

### Cloud Mapper to Exploit Pipeline (Cross-Sub-Skill)

Cartography attack surface maps may identify targets for exploitation assessment. This is a Zone 2 -> Zone 3 escalation managed by `rainbow-orchestrator` with per-operation approval.

| Stage | Source Agent | Target Agent | Data | Orchestrator Action |
|-------|-------------|-------------|------|-------------------|
| 1 | `rainbow-cloud-mapper` (Cartography) | `rainbow-exploit-*` | Attack paths from graph analysis | Per-operation approval required (Zone 3) |

### Supply Chain to Cloud Pipeline (Cross-Sub-Skill)

Checkov findings from `/rainbow-supply-chain` may feed into cloud-specific Checkov assessments.

| Stage | Source Agent | Target Agent | Data | Orchestrator Action |
|-------|-------------|-------------|------|-------------------|
| 1 | `rainbow-sc-scanner` (Checkov) | `rainbow-cloud-auditor` (Checkov) | IaC findings for cloud-specific follow-up | Construct handoff with artifact path |

---

## Constitutional Compliance

| Principle | Application |
|-----------|-------------|
| **P-003 / H-01** | Both agents are T2 workers. No Task tool access. No delegation. |
| **P-020 / H-02** | Audit and mapping scope approved by user. Zone 2 operations require engagement scope. Zone 3 never attempted by agents. |
| **P-022 / H-03** | Audit coverage limitations disclosed. Tool database freshness reported. Kyverno zone classification transparent. |
| **P-001** | All findings evidence-based with benchmark references and tool output citations. |
| **P-002** | All audit reports, policy reports, mapping results, and audit logs persisted. |
| **H-34** | Both agents use dual-file architecture (.md + .governance.yaml). Constitutional compliance triplet in every agent. |

---

## References

| Source | Content |
|--------|---------|
| ADR-PROJ023-001 | Architecture decision: composable sub-skill structure, agent registry, zone classification |
| `skills/rainbow/SKILL.md` | Parent skill: routing, engagement lifecycle, security zone overview |
| `skills/rainbow/rules/rainbow-credential-filter.md` | Credential filter 3-layer specification |
| `skills/rainbow/rules/zone-1-analysis.md` | Zone 1 guardrail profile |
| `skills/rainbow/rules/zone-2-active.md` | Zone 2 guardrail profile |
| `skills/rainbow/rainbow-cloud/rules/kyverno-escalation-protocol.md` | Kyverno dual-zone escalation protocol |
| `skills/rainbow/rainbow-cloud/rules/kyverno-dryrun-enforcement.yaml` | Kyverno dry-run enforcement configuration |
| Tool documentation cache | `projects/PROJ-023-exploit-framework/work/research/tool-docs-cache.md` |

---

*Sub-Skill Version: 1.0.0*
*Constitutional Compliance: Jerry Constitution v1.0*
*SSOT: ADR-PROJ023-001*
*Created: 2026-03-16*
