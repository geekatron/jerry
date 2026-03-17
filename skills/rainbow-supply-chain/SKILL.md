---
name: rainbow-supply-chain
description: >-
  Supply chain security sub-skill of /rainbow. Provides SBOM generation,
  vulnerability scanning, IaC security auditing, container image signature
  verification, and license compliance analysis. Uses Syft, Grype, Trivy,
  OSV-Scanner, Checkov, Cosign, and Snyk CLI. Zone 1 (analysis) by default.
  Cosign download = Zone 2. Cosign sign/attest = Zone 3 (not available to
  sub-skill agents). Invoke for: SBOM, vulnerability scan, container scan,
  IaC scan, signature verification, license compliance, supply chain audit.
version: "1.0.0"
agents:
  - rainbow-sc-scanner
  - rainbow-sc-verifier
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
activation-keywords:
  - "SBOM"
  - "supply chain"
  - "vulnerability scan"
  - "container scan"
  - "IaC scan"
  - "signature verification"
  - "Cosign verify"
  - "Syft"
  - "Grype"
  - "Trivy"
  - "OSV-Scanner"
  - "Checkov"
  - "Snyk"
  - "license compliance"
  - "artifact provenance"
  - "CycloneDX"
  - "SPDX"
---

# Rainbow Supply Chain Sub-Skill

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
| [Security Zone Enforcement](#security-zone-enforcement) | Zone 1 default with Zone 2/3 escalation |
| [Credential Filter](#credential-filter) | Mandatory output sanitization |
| [Internal Routing](#internal-routing) | How rainbow-orchestrator routes to this sub-skill |
| [Cross-Sub-Skill Data Contracts](#cross-sub-skill-data-contracts) | Pipeline integration with other sub-skills |
| [Constitutional Compliance](#constitutional-compliance) | Governance alignment |

---

## Purpose

The `/rainbow-supply-chain` sub-skill provides **tool-assisted supply chain security assessment**. It covers the full supply chain verification lifecycle: SBOM generation, vulnerability scanning, IaC auditing, signature verification, license compliance, and provenance validation.

This sub-skill is part of the /rainbow composable architecture (ADR-PROJ023-001, Wave 1). It delivers independent value without requiring other /rainbow sub-skills to be operational.

### Key Capabilities

- **SBOM Generation** -- Produce CycloneDX/SPDX bills of materials from container images, filesystems, and archives (Syft)
- **Vulnerability Scanning** -- Match dependencies against vulnerability databases (Grype, OSV-Scanner, Snyk CLI)
- **Multi-Target Scanning** -- Scan containers, filesystems, and IaC for vulnerabilities and misconfigurations (Trivy)
- **IaC Security Auditing** -- Validate Terraform, CloudFormation, Kubernetes, Helm, Dockerfile against security policies (Checkov)
- **Signature Verification** -- Validate container image signatures and attestation trees (Cosign)
- **License Compliance** -- Check dependency licenses against organizational policies (Snyk CLI)
- **Provenance Validation** -- Assess supply chain trust against SLSA levels

### What This Sub-Skill Is NOT

- Does NOT provide reconnaissance or active probing (use `/rainbow-recon`)
- Does NOT sign or attest artifacts (Zone 3 -- managed by `rainbow-orchestrator`)
- Does NOT provide penetration testing methodology (use `/red-team`)
- Does NOT provide secure development guidance (use `/eng-team`)
- Does NOT perform malware analysis (use `/blue-team`)

---

## When to Use

Activate when the request involves:

- Generating SBOMs from container images or source code
- Scanning dependencies for known vulnerabilities (CVEs)
- Auditing IaC templates for security misconfigurations
- Verifying container image signatures or attestation chains
- Checking license compliance of dependencies
- Assessing supply chain trust and provenance

Do NOT invoke when:

- Task requires network reconnaissance or active target probing -- use `/rainbow-recon`
- Task requires exploit execution -- use `/rainbow-exploit`
- Task is malware analysis or threat detection -- use `/blue-team`
- Task is penetration testing methodology without tool execution -- use `/red-team`
- Task is building secure software or threat modeling -- use `/eng-team`

---

## Agent Registry

| Agent | Role | Zone | Tools | Cognitive Mode |
|-------|------|------|-------|---------------|
| `rainbow-sc-scanner` | SBOM generation and vulnerability scanning | Zone 1 | Syft, Grype, Trivy, OSV-Scanner, Checkov | systematic |
| `rainbow-sc-verifier` | Artifact verification and provenance | Zone 1/2 | Cosign (verify/tree = Z1, download = Z2), Snyk CLI | systematic |

**Tool tier:** Both agents are T2 (Read-Write). Neither agent has Task tool access per H-34/P-003.

---

## Tool Inventory

| Tool | Version | Agent | Zone 1 Operations | Zone 2 Operations | Zone 3 Operations |
|------|---------|-------|-------------------|-------------------|-------------------|
| **Syft** | >= 1.0 | scanner | `scan`, `packages` | -- | -- |
| **Grype** | >= 0.74 | scanner | `sbom:` scan, `db check/update` | -- | -- |
| **Trivy** | >= 0.50 | scanner | `image`, `fs`, `config`, `sbom` | -- | -- |
| **OSV-Scanner** | >= 2.0 | scanner | `scan` (local lockfiles/SBOMs) | -- | -- |
| **Checkov** | >= 3.0 | scanner | `-d`, `-f`, `--framework` (scan) | `--fix` (remediation) | -- |
| **Cosign** | >= 2.2 | verifier | `verify`, `tree` | `download signature/sbom` | `sign`, `attest`, `attach` (NOT available) |
| **Snyk CLI** | Latest | verifier | `test`, `monitor`, `container test` | -- | -- |

### CLI Quick Reference

| Tool | Primary Command | Output Flag |
|------|----------------|-------------|
| Syft | `syft scan <target> -o cyclonedx-json=<file>` | `-o cyclonedx-json` |
| Grype | `grype sbom:<sbom.json> --output json` | `--output json` |
| Trivy | `trivy <type> <target> -f json -o <file>` | `-f json` |
| OSV-Scanner | `osv-scanner scan -L <lockfile> --format json` | `--format json` |
| Checkov | `checkov -d <dir> --output json` | `--output json` |
| Cosign | `cosign verify --key <key> <image>` | JSON stdout |
| Snyk | `snyk test --json-file-output=<file>` | `--json-file-output` |

---

## Security Zone Enforcement

**Default zone:** Zone 1 (Analysis). All standard scanning and verification operations are Zone 1.

### Zone Classification

| Zone | Operations | Authorization |
|------|-----------|---------------|
| **Zone 1** | All Syft, Grype, Trivy, OSV-Scanner scans; Checkov scan mode; Cosign verify/tree; Snyk test/monitor | Project scope only (H-04) |
| **Zone 2** | Checkov `--fix`; Cosign `download`; Snyk `fix`/`ignore` | Engagement scope required |
| **Zone 3** | Cosign `sign`/`attest`/`attach` | NOT available to sub-skill agents. Per-operation approval + vault authorization via rainbow-orchestrator. |

### Enforcement Layers

1. **Agent-level guardrails:** Each agent validates CLI subcommands against its Zone 1 allowlist before execution.
2. **Sub-skill rules:** This SKILL.md declares Zone 1 as default with explicit escalation conditions.
3. **Parent orchestrator:** `rainbow-orchestrator` validates engagement scope before routing Zone 2 requests.

### Escalation Triggers

| Trigger | From | To | Action |
|---------|------|----|--------|
| Checkov `--fix` requested | Zone 1 | Zone 2 | Agent halts. Returns to orchestrator for scope validation. |
| Cosign `download` requested | Zone 1 | Zone 2 | Agent validates engagement scope. If absent, halts and escalates. |
| Cosign `sign`/`attest`/`attach` requested | Any | Zone 3 | Agent NEVER executes. Informs user. Returns to orchestrator. |
| Remote target scan requested | Zone 1 | Zone 2 | Agent halts. Returns to orchestrator for scope validation. |

See `skills/rainbow/rules/zone-1-analysis.md` and `skills/rainbow/rules/zone-2-active.md` for full guardrail profiles.

---

## Credential Filter

The credential filter pipeline is MANDATORY for all tool output. No tool output enters the context window without passing through the 3-layer filter.

| Layer | Mechanism | Relevance to Supply Chain |
|-------|-----------|--------------------------|
| L1 | Regex pattern matching | IaC scans may surface embedded credentials in configuration files |
| L2 | Entropy detection | Base64-encoded secrets in container layers or dependency metadata |
| L3 | Structural analysis | JSON/YAML scan output may contain sensitive key-value pairs |

**Full specification:** `skills/rainbow/rules/rainbow-credential-filter.md`

**Fail-closed behavior:** Filter crash or timeout rejects the entire tool output block. Flagged content quarantined to `work/.credential-quarantine/`.

---

## Known Limitations and Compensating Controls

> Honest disclosure per P-022. These are accepted architectural limitations documented in ADR-PROJ023-001.

### Zone Enforcement Is Behavioral-Only

Zone enforcement relies on LLM behavioral compliance with subcommand allowlists. No L3 runtime gate validates Bash commands before execution.

**Compensating controls:**
1. **Bash subcommand allowlists** -- Both agents declare `bash_subcommand_allowlist_zone_1` (and zone_2 for verifier) in `.governance.yaml`
2. **NPT-009-complete forbidden actions** -- Zone violation entries use structured negation with consequences
3. **BDD zone enforcement scenarios** -- Both agents have BDD scenarios testing zone escalation and boundary refusal
4. **Dual-zone Cosign classification** -- verify/tree = Zone 1, download = Zone 2, sign/attest/attach = Zone 3 (never executed)

### Credential Filter Is W0 Specification-Only

The credential filter pipeline is a W0 specification. Both agents declare `credential_filter_applied_to_all_tool_output` as a behavioral constraint. Runtime enforcement deferred to W1.

**Compensating controls:**
1. **Three-layer specification** -- L1 regex, L2 entropy, L3 structural analysis fully specified in `skills/rainbow/rules/rainbow-credential-filter.md`
2. **Behavioral declaration** -- Both agents include credential filter in `output_filtering`
3. **Fail-closed specification** -- Filter crash or timeout rejects entire tool output block
4. **BDD credential filter scenarios** -- Both agents have credential filter application and quarantine scenarios

---

## Internal Routing

The `rainbow-orchestrator` routes to this sub-skill based on request keywords.

### Activation Keywords (from rainbow-orchestrator)

Supply chain keywords that trigger routing to this sub-skill:
- SBOM, CVE scan, container scan, IaC scan/audit, signature verification
- Tool names: Syft, Grype, Trivy, OSV-Scanner, Checkov, Cosign, Snyk
- Supply chain, dependency audit, license compliance, artifact provenance

### Agent Selection Within Sub-Skill

| Request Type | Agent | Rationale |
|-------------|-------|-----------|
| SBOM generation, vulnerability scanning, IaC scanning | `rainbow-sc-scanner` | Scanner handles all scanning tools |
| Signature verification, attestation inspection, license compliance | `rainbow-sc-verifier` | Verifier handles trust and compliance tools |
| Mixed (scan + verify) | Both, sequenced by orchestrator | Scanner first (produces SBOM), then verifier (validates provenance) |

---

## Cross-Sub-Skill Data Contracts

### Syft-to-Grype Pipeline (Intra-Sub-Skill)

| Stage | Tool | Input | Output | Format |
|-------|------|-------|--------|--------|
| 1 | Syft | Container image / filesystem | SBOM | CycloneDX JSON |
| 2 | Grype | SBOM (via `sbom:` prefix) | Vulnerability report | Grype JSON |

### Supply Chain to Recon Pipeline (Cross-Sub-Skill)

Grype vulnerability report feeds into Nuclei detection scanning for web-facing targets. This cross-sub-skill handoff is managed by `rainbow-orchestrator` per handoff-v2.schema.json.

| Stage | Source Agent | Target Agent | Data | Orchestrator Action |
|-------|-------------|-------------|------|-------------------|
| 1 | `rainbow-sc-scanner` (Grype) | `rainbow-recon-pipeline` (Nuclei) | Vulnerability report JSON | Construct handoff with artifact path |

---

## Constitutional Compliance

| Principle | Application |
|-----------|-------------|
| **P-003 / H-01** | Both agents are T2 workers. No Task tool access. No delegation. |
| **P-020 / H-02** | Scan scope approved by user. Zone 2 operations require engagement scope. Zone 3 never attempted. |
| **P-022 / H-03** | Scan coverage limitations disclosed. Tool database freshness reported. Verification results accurate. |
| **P-001** | All findings evidence-based with CVE references and tool output citations. |
| **P-002** | All scan reports, SBOMs, verification results, and audit logs persisted. |
| **H-34** | Both agents use dual-file architecture (.md + .governance.yaml). Constitutional compliance triplet in every agent. |

---

## References

| Source | Content |
|--------|---------|
| ADR-PROJ023-001 | Architecture decision: composable sub-skill structure, agent registry, zone classification |
| `skills/rainbow/SKILL.md` | Parent skill: routing, engagement lifecycle, security zone overview |
| `skills/rainbow/rules/rainbow-credential-filter.md` | Credential filter 3-layer specification |
| `skills/rainbow/rules/zone-1-analysis.md` | Zone 1 guardrail profile (default for this sub-skill) |
| `skills/rainbow/rules/zone-2-active.md` | Zone 2 guardrail profile (Cosign download, Checkov fix) |
| Tool documentation cache | `projects/PROJ-023-exploit-framework/work/research/tool-docs-cache.md` |

---

*Sub-Skill Version: 1.0.0*
*Constitutional Compliance: Jerry Constitution v1.0*
*SSOT: ADR-PROJ023-001*
*Created: 2026-03-14*
