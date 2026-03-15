---
name: blue-team
description: >-
  Defensive cybersecurity operations skill. Provides threat detection rule
  authoring (YARA-X, Sigma, Suricata), malware analysis (Ghidra, JADX),
  incident response (NIST 800-61r2, Plaso), compliance scanning (Checkov,
  Trivy, Prowler, Kubescape, OpenSCAP), threat intelligence (MISP, STIX/TAXII),
  and D3FEND countermeasure mapping. All agents operate in Security Zone 1
  (Analysis) -- read-only analysis and local artifact production only.
  Invoke for: threat detection, malware analysis, YARA rules, incident response,
  compliance audit, CIS benchmark, NIST assessment, threat intelligence,
  D3FEND mapping, IOC management, security monitoring, forensic analysis.
version: "1.0.0"
agents:
  - blue-lead
  - blue-detect
  - blue-monitor
  - blue-siem
  - blue-malware-analyst
  - blue-incident-resp
  - blue-comply
  - blue-posture-k8s
  - blue-posture-sys
  - blue-intel
  - blue-d3fend
  - blue-ioc
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch, mcp__context7__resolve-library-id, mcp__context7__query-docs
activation-keywords:
  - "threat detection"
  - "malware analysis"
  - "YARA"
  - "IOC"
  - "indicator of compromise"
  - "reverse engineering"
  - "binary analysis"
  - "blue team defense"
  - "defensive operations"
  - "compliance audit"
  - "CIS benchmark"
  - "NIST assessment"
  - "incident response"
  - "IR playbook"
  - "forensic analysis"
  - "threat intelligence"
  - "D3FEND"
  - "SIEM"
  - "Sigma rules"
  - "detection rules"
  - "threat hunting"
  - "security monitoring"
  - "security posture"
  - "Kubernetes security"
---

# Blue Team Skill

> **Version:** 1.0.0
> **Framework:** Jerry Blue-Team
> **Constitutional Compliance:** Jerry Constitution v1.0
> **SSOT Reference:** ADR-PROJ023-001 (Accepted, Hybrid B+C architecture)

## Document Audience (Triple-Lens)

| Level | Audience | Sections to Focus On |
|-------|----------|---------------------|
| **L0 (Stakeholder)** | Engagement managers, leadership | [Purpose](#purpose), [When to Use This Skill](#when-to-use-this-skill), [Routing Disambiguation](#routing-disambiguation), [Quick Reference](#quick-reference) |
| **L1 (Practitioner)** | Security analysts invoking agents | [Available Agents](#available-agents), [Invoking an Agent](#invoking-an-agent), [Orchestration Flow](#orchestration-flow), [Cross-Skill Integration Points](#cross-skill-integration-points) |
| **L2 (Architect)** | Framework designers, governance reviewers | [Zone 1 Enforcement](#zone-1-enforcement), [P-003 Compliance](#p-003-compliance), [Constitutional Compliance](#constitutional-compliance) |

---

## Purpose

The Blue Team skill provides **defensive cybersecurity operations** within the Jerry framework's Hybrid B+C architecture (ADR-PROJ023-001). It routes to 12 specialized agents across 4 domains (detection, forensics, compliance, threat intelligence) that collectively provide threat detection, malware analysis, incident response, compliance scanning, threat intelligence, and D3FEND countermeasure mapping.

### Key Capabilities

- **Threat Detection** -- YARA-X rule validation/execution, Sigma rule authoring, Suricata/Zeek/Falco/Tetragon monitoring methodology, SIEM/XDR correlation
- **Forensics** -- Malware reverse engineering (Ghidra, JADX), incident response playbook execution (NIST 800-61r2), timeline reconstruction (Plaso)
- **Compliance Scanning** -- IaC/cloud (Checkov, Trivy, Prowler), Kubernetes (Kubescape, kube-bench, Kyverno), system-level (OpenSCAP, Cosign)
- **Threat Intelligence** -- MISP/STIX/TAXII intelligence lifecycle, D3FEND countermeasure mapping, IOC lifecycle management and YARA rule authoring
- **Zone 1 Universal Enforcement** -- All operations are read-only analysis or local artifact production; no active response, no infrastructure modification, no live system interaction
- **Three-Level Degradation** -- All agents function standalone (AD-010); tools augment evidence quality but do not enable reasoning

### What This Skill Is NOT

This skill provides **defensive methodology guidance and analysis**, not autonomous security response. It does NOT:

- Execute active response or containment actions on live systems
- Modify production infrastructure or deploy security configurations
- Access live networks or monitored systems directly
- Operate without explicit human authorization for assessment scope
- Replace human judgment for incident severity classification or response decisions

---

## When to Use This Skill

Activate when:

- Authoring or validating threat detection rules (YARA, Sigma, Suricata)
- Performing malware analysis or binary reverse engineering
- Executing incident response playbooks or reconstructing timelines
- Running compliance scans against CIS, NIST, SOC 2, PCI DSS, HIPAA frameworks
- Analyzing threat intelligence feeds or managing IOC lifecycles
- Mapping ATT&CK techniques to D3FEND countermeasures
- Assessing Kubernetes or system-level security posture
- Correlating SIEM/XDR log sources for detection engineering
- Performing forensic timeline reconstruction with Plaso

NEVER invoke this skill when:
- Task is building secure software (defensive architecture/design) -- Consequence: Blue team produces detection and analysis artifacts, not hardened code; STRIDE/DREAD and OWASP ASVS not loaded; use `/eng-team` instead
- Task is offensive security testing or penetration testing -- Consequence: Defensive methodology applied to offensive engagement produces detection rules instead of exploitation methodology; use `/red-team` instead
- Task is adversarial quality review of deliverables -- Consequence: Security analysis methodology applied to quality assessment produces compliance reports instead of quality scores; use `/adversary` instead
- Conducting general security research without a defensive operations context -- Consequence: Blue team agents require assessment scope; unscoped research lacks operational boundaries; use `/problem-solving` instead

See [Routing Disambiguation](#routing-disambiguation) for full exclusion conditions.

---

## Available Agents

| # | Agent | Domain | Role | Model | Tier | Output Location |
|---|-------|--------|------|-------|------|-----------------|
| 1 | `blue-lead` | Governance | Engagement scope and methodology authority | opus | T3 | `work/blue-team/engagements/{engagement-id}/scope.md` |
| 2 | `blue-detect` | Detection | YARA-X rule validation and execution | sonnet | T2 | `work/blue-team/detection/` |
| 3 | `blue-monitor` | Detection | Network/runtime monitoring (Suricata, Zeek, Falco, Tetragon) | sonnet | T2 | `work/blue-team/monitoring/` |
| 4 | `blue-siem` | Detection | SIEM/XDR correlation (Wazuh, Sigma, Hayabusa, Chainsaw) | sonnet | T2 | `work/blue-team/siem/` |
| 5 | `blue-malware-analyst` | Forensics | Malware RE and binary analysis (Ghidra, JADX) | sonnet | T2 | `work/blue-team/analysis/{evidence-id}/` |
| 6 | `blue-incident-resp` | Forensics | IR playbook execution and timeline (Plaso) | sonnet | T2 | `work/blue-team/incidents/{incident-id}/` |
| 7 | `blue-comply` | Compliance | Compliance scan orchestration (Checkov, Trivy, Prowler) | sonnet | T2 | `work/compliance/{assessment-id}/` |
| 8 | `blue-posture-k8s` | Compliance | Kubernetes security posture (Kubescape, kube-bench, Kyverno) | sonnet | T2 | `work/compliance/{assessment-id}/k8s/` |
| 9 | `blue-posture-sys` | Compliance | System-level compliance (OpenSCAP, Cosign) | sonnet | T2 | `work/compliance/{assessment-id}/system/` |
| 10 | `blue-intel` | Threat Intel | Threat intelligence analyst (MISP, STIX/TAXII, OSINT) | opus | T3 | `work/blue-team/intel/{product-slug}.md` |
| 11 | `blue-d3fend` | Threat Intel | D3FEND countermeasure mapper | sonnet | T3 | `work/blue-team/d3fend/{mapping-slug}.md` |
| 12 | `blue-ioc` | Threat Intel | IOC lifecycle manager and YARA rule author | sonnet | T2 | `work/blue-team/ioc/` |

---

## Zone 1 Universal Enforcement

> **ALL 12 agents operate exclusively in Security Zone 1 (Analysis).** No Zone 2 or Zone 3 operations.

Zone 1 means:
- **Read-only analysis** of provided artifacts, logs, and configuration files
- **Local artifact production** (detection rules, reports, compliance findings, STIX bundles)
- **No active response** -- no containment, no quarantine, no blocking
- **No infrastructure modification** -- no firewall rule deployment, no agent installation
- **No live system interaction** -- no network scanning, no service probing

This is the strictest possible security posture for defensive operations. Agents produce artifacts and methodology guidance for human practitioners to deploy.

---

## P-003 Compliance

All blue-team agents are **workers**, NOT orchestrators. The MAIN CONTEXT (Claude session) orchestrates the workflow.

```
P-003 AGENT HIERARCHY:
======================

  +-------------------+
  | MAIN CONTEXT      |  <-- Orchestrator (Claude session)
  | (orchestrator)    |
  +-------------------+
     |  |  |  |  |  |
     v  v  v  v  v  v
  +------+ +------+ +------+ +------+ +------+ +------+
  | blue-| | blue-| | blue-| | blue-| | blue-| | ...  |
  | lead | |detect| |monit.| | siem | |malwr.| |      |
  +------+ +------+ +------+ +------+ +------+ +------+

  Agents CANNOT invoke other agents.
  Agents CANNOT spawn subagents.
  Only MAIN CONTEXT orchestrates the sequence.
```

---

## Invoking an Agent

### Option 1: Natural Language Request

Simply describe what you need:

```
"Start a new defensive assessment for the production Kubernetes cluster"
"Analyze this malware sample with Ghidra"
"Run a CIS benchmark compliance scan on the IaC templates"
"Create YARA rules for the indicators from the latest threat report"
"Map our detection coverage against D3FEND countermeasures"
"Execute the IR playbook for the suspected compromise"
```

The orchestrator will select the appropriate agent(s) based on keywords and context.

### Option 2: Explicit Agent Request

Request a specific agent:

```
"Use blue-lead to define scope for a security assessment"
"Have blue-detect validate and execute these YARA rules"
"I need blue-comply to run Checkov against our Terraform modules"
"Ask blue-intel to analyze the threat intelligence feed"
```

---

## Orchestration Flow

### Assessment Workflow

The /blue-team workflow begins with blue-lead establishing assessment scope. After scope establishment, any agent is invocable based on assessment needs.

```
                    +------------+
                    | blue-lead  |  <-- MANDATORY FIRST (scope establishment)
                    +-----+------+
                          |
                          v
          +---------------+---------------+
          |     SCOPE ESTABLISHED         |
          |  (any agent invocable now)    |
          +---+---+---+---+---+----------+
              |   |   |   |   |
    +---------+   |   |   |   +----------+
    |             |   |   |              |
    v             v   v   v              v
+--------+  +--------+ +--------+  +--------+
|blue-   |  |blue-   | |blue-   |  |blue-   |
|detect  |  |monitor | |siem    |  |intel   |
+---+----+  +--------+ +--------+  +---+----+
    |                                   |
    v                                   v
+--------+     +--------+         +--------+
|blue-   |     |blue-   |         |blue-   |
|malware |     |incident|         |d3fend  |
|analyst |     |resp    |         +--------+
+--------+     +--------+              |
                                       v
+--------+ +--------+ +--------+ +--------+
|blue-   | |blue-   | |blue-   | |blue-   |
|comply  | |posture | |posture | |ioc     |
|        | |k8s     | |sys     | |        |
+--------+ +--------+ +--------+ +--------+
```

### Orchestration Rules

1. **blue-lead MUST establish scope first (MANDATORY).** No other agent operates without an active scope document.

2. **After scope establishment, any agent is invocable in any order based on assessment context.** Domain boundaries organize capability, not workflow sequence.

3. **Cross-domain handoffs are supported:**
   - blue-intel produces intelligence that blue-ioc operationalizes into YARA rules
   - blue-ioc creates YARA rules that blue-detect validates and executes
   - blue-malware-analyst produces IOC lists that feed blue-ioc and blue-detect
   - blue-d3fend identifies coverage gaps that drive detection agent work
   - blue-incident-resp timelines may trigger blue-malware-analyst deep analysis

4. **All handoffs pass through the main context.** No agent directly invokes another (P-003).

---

## Cross-Skill Integration Points

Three integration points connect /blue-team with /red-team and /eng-team for purple team operations.

### Credential Filter Requirement

When processing artifacts received from cross-skill handoffs (particularly IP-5: Red-to-Blue threat-informed defense), /blue-team agents MUST apply the Rainbow credential filter pipeline. Red-team output is classified as `adversary-tainted` and may contain credential material (NTLM hashes, Kerberos tickets, API tokens) embedded in exploitation findings. The credential filter specification is defined in `skills/rainbow/rules/rainbow-credential-filter.md`. All three filter layers (L1 regex, L2 entropy, L3 structural) apply. Fail-closed behavior: if the filter crashes or times out, the artifact is rejected and quarantined before entering the agent's context.

### Integration Point 5: Threat-Informed Defense (IP-5)

| Attribute | Value |
|-----------|-------|
| **Source** | /red-team (red-recon, red-exploit) |
| **Target** | /blue-team (blue-detect, blue-siem, blue-d3fend) |
| **Data Exchanged** | Adversary TTPs, exploitation results, attack patterns |
| **Value** | Detection rules authored against real adversary behavior, not theoretical threats |

### Integration Point 6: Detection Coverage Validation (IP-6)

| Attribute | Value |
|-----------|-------|
| **Source** | /blue-team (blue-siem, blue-d3fend) |
| **Target** | /eng-team (eng-incident, eng-devsecops) |
| **Data Exchanged** | Detection coverage reports, gap analysis, D3FEND mappings |
| **Value** | IR runbooks and DevSecOps pipelines informed by measured detection coverage |

### Integration Point 7: Compliance-to-Architecture Feedback (IP-7)

| Attribute | Value |
|-----------|-------|
| **Source** | /blue-team (blue-comply, blue-posture-k8s, blue-posture-sys) |
| **Target** | /eng-team (eng-architect, eng-infra) |
| **Data Exchanged** | Compliance findings, misconfiguration reports, hardening recommendations |
| **Value** | Architecture and infrastructure decisions informed by measured compliance posture |

---

## Tool Inventory Summary

| Category | Count | Examples |
|----------|-------|---------|
| **Tier A (Execute)** | 11 | YARA-X, Hayabusa, Chainsaw, Checkov, Trivy, Prowler, Kubescape, kube-bench, Cosign, JADX, Plaso |
| **Tier B (Guide-then-execute)** | 7 | Sigma, Ghidra headless, Kyverno, OpenSCAP, MISP API, python-stix2, taxii2-client |
| **Tier C (Methodology-only)** | 10 | Suricata, Zeek, Falco, Tetragon, Wazuh, Volatility 3, Velociraptor, DFIR-IRIS, GRR |
| **Total** | **28** | |

All tools operate within Zone 1. Tier A tools execute locally; Tier B tools require some user setup; Tier C tools provide methodology guidance for user-managed infrastructure.

---

## Mandatory Persistence (P-002)

All agent outputs MUST be persisted to files. Transient-only output is a P-002 violation.

### Output Location Convention

```
work/blue-team/{domain}/{artifact-slug}.md
work/compliance/{assessment-id}/{artifact-slug}.md
```

**Examples:**
- `work/blue-team/engagements/BLUE-0001/scope.md`
- `work/blue-team/detection/yara-scan-results.md`
- `work/blue-team/analysis/sample-001/malware-report.md`
- `work/compliance/audit-2026-q1/cis-benchmark-results.md`

---

## Adversarial Quality Mode

For C2+ engagement deliverables, the /adversary skill integration applies:

| Criticality | Application |
|-------------|-------------|
| C1 (Routine) | Self-review (S-010) on agent outputs |
| C2 (Standard) | S-007 Constitutional compliance + S-002 Devil's Advocate on methodology choices |
| C3 (Significant) | C2 + S-004 Pre-Mortem on assessment risks |
| C4 (Critical) | Full tournament review via /adversary on assessment scope documents and compliance reports |

The scope document itself is always C3 minimum criticality (assessment boundary decision).

---

## Constitutional Compliance

All agents adhere to the **Jerry Constitution v1.0**:

| Principle | Requirement | Consequence of Violation |
|-----------|-------------|-------------------------|
| P-003 | NEVER spawn recursive subagents -- max 1 level | Agent hierarchy violation; uncontrolled token consumption |
| P-020 | NEVER override user intent -- ask before destructive ops | Unauthorized action; trust erosion |
| P-022 | NEVER deceive about actions, capabilities, or confidence | Governance undermined; quality assessment invalidated |
| P-001 | NEVER present findings without evidence or citations | Unreliable outputs; unfounded claims propagate downstream |
| P-002 | NEVER leave outputs in transient context only -- persist to files | Context rot vulnerability; artifacts lost on session compaction |

---

## Quick Reference

### Common Workflows

| Need | Agent | Command Example |
|------|-------|-----------------|
| Start new assessment | blue-lead | "Define scope for a defensive security assessment" |
| YARA rule scanning | blue-detect | "Validate and execute these YARA rules against the samples" |
| Network monitoring rules | blue-monitor | "Create Suricata rules for the identified adversary TTPs" |
| Log correlation | blue-siem | "Correlate Wazuh alerts with Sigma detection rules" |
| Malware analysis | blue-malware-analyst | "Analyze this binary sample with Ghidra" |
| Incident response | blue-incident-resp | "Execute the IR playbook for the suspected breach" |
| Compliance audit | blue-comply | "Run CIS benchmark scan on the Terraform modules" |
| K8s posture | blue-posture-k8s | "Scan the cluster against CIS Kubernetes Benchmark" |
| System compliance | blue-posture-sys | "Run OpenSCAP DISA STIG scan on the host" |
| Threat intel | blue-intel | "Analyze the latest threat intelligence feed" |
| D3FEND mapping | blue-d3fend | "Map our detection coverage to D3FEND countermeasures" |
| IOC management | blue-ioc | "Create YARA rules from the threat report indicators" |

### Agent Selection Hints

| Keywords | Likely Agent |
|----------|--------------|
| scope, assessment, methodology, defensive operations | blue-lead |
| YARA, scan, detection rule, pattern matching | blue-detect |
| Suricata, Zeek, Falco, Tetragon, IDS, network monitoring | blue-monitor |
| Sigma, Wazuh, SIEM, log correlation, EVTX, Hayabusa, Chainsaw | blue-siem |
| malware, binary, reverse engineering, Ghidra, JADX, decompile | blue-malware-analyst |
| incident response, IR playbook, timeline, evidence, forensic, Plaso | blue-incident-resp |
| compliance, CIS, NIST, SOC 2, PCI DSS, HIPAA, Checkov, Trivy, Prowler | blue-comply |
| Kubernetes, kube-bench, Kubescape, Kyverno, K8s security | blue-posture-k8s |
| OpenSCAP, SCAP, Cosign, DISA STIG, system hardening | blue-posture-sys |
| threat intelligence, STIX, TAXII, MISP, OSINT, adversary profile | blue-intel |
| D3FEND, countermeasure, defensive coverage, detection gap | blue-d3fend |
| IOC lifecycle, indicator enrichment, YARA rule creation | blue-ioc |

### Internal Routing Decision Tree

```
User Request
    |
    v
[Contains engagement/methodology/scope question?]
    YES --> blue-lead
    |
    NO
    v
[Contains YARA/file detection/pattern matching?]
    YES --> [YARA rule creation?] --> blue-ioc
           [YARA rule execution/scanning?] --> blue-detect
    |
    NO
    v
[Contains network monitoring/IDS/Suricata/Zeek/Falco/Tetragon?]
    YES --> blue-monitor
    |
    NO
    v
[Contains SIEM/Sigma/Wazuh/log correlation/EVTX?]
    YES --> blue-siem
    |
    NO
    v
[Contains malware/binary/reverse engineering/Ghidra/JADX?]
    YES --> blue-malware-analyst
    |
    NO
    v
[Contains incident response/IR playbook/evidence/timeline?]
    YES --> blue-incident-resp
    |
    NO
    v
[Contains compliance/audit/CIS/NIST/SOC2/PCI/HIPAA?]
    YES --> [Kubernetes-specific?] --> blue-posture-k8s
           [System-level/SCAP/container signing?] --> blue-posture-sys
           [IaC/cloud/multi-framework?] --> blue-comply
    |
    NO
    v
[Contains threat intelligence/adversary/campaign/STIX/MISP?]
    YES --> blue-intel
    |
    NO
    v
[Contains D3FEND/countermeasure/defensive coverage/gap analysis?]
    YES --> blue-d3fend
    |
    NO
    v
[Contains IOC management/indicator lifecycle/IOC aging?]
    YES --> blue-ioc
    |
    NO
    v
blue-lead (default fallback for ambiguous defensive requests)
```

### Agent Trigger Map (5-Column Format)

| Detected Keywords | Negative Keywords | Priority | Compound Triggers | Agent |
|---|---|---|---|---|
| engagement scope, methodology, defensive operations, blue team assessment, security assessment scope | YARA, Sigma, Ghidra, compliance scan, threat intel | 1 | -- | blue-lead |
| YARA, detection rule, malware pattern, IOC matching, threat detection, indicator of compromise, YARA-X, yr scan | YARA rule creation, IOC lifecycle, rule authoring from intel, STIX | 3 | -- | blue-detect |
| Suricata, Zeek, Falco, Tetragon, IDS, IPS, network monitoring, runtime detection, eBPF, container monitoring, PCAP | SIEM, Sigma, Wazuh, log correlation, YARA, compliance | 4 | -- | blue-monitor |
| Wazuh, Sigma, SIEM, XDR, log correlation, detection-as-code, Hayabusa, Chainsaw, EVTX analysis | YARA, network monitoring, Suricata, compliance | 5 | -- | blue-siem |
| malware analysis, reverse engineering, binary analysis, decompile, Ghidra, JADX, APK analysis, static analysis, PE analysis, ELF analysis, shellcode | incident response, detection rule, compliance, threat intel | 6 | "malware analysis" OR "reverse engineering" OR "binary analysis" | blue-malware-analyst |
| incident response, IR playbook, evidence collection, timeline reconstruction, containment, eradication, recovery, post-incident, forensic timeline, NIST 800-61, chain of custody, Plaso | malware analysis, compliance, detection rule, threat intel | 7 | "incident response" OR "IR playbook" OR "evidence collection" | blue-incident-resp |
| compliance audit, CIS benchmark, NIST mapping, SOC 2, PCI DSS, HIPAA, audit evidence, compliance gap, posture assessment, Checkov, Trivy compliance, Prowler | Kubernetes, K8s, SCAP, Cosign, YARA, incident response | 8 | "compliance audit" OR "CIS benchmark" OR "NIST mapping" | blue-comply |
| Kubernetes compliance, CIS K8s, NSA-CISA K8s, kube-bench, Kubescape, Kyverno, K8s RBAC, pod security, K8s security posture | system-level, SCAP, Cosign, Checkov, Prowler | 9 | "Kubernetes security" OR "K8s compliance" OR "kube-bench" | blue-posture-k8s |
| OpenSCAP, SCAP profile, system compliance, Cosign, container signing, DISA STIG, system hardening | Kubernetes, K8s, kube-bench, Checkov, Prowler | 10 | "system compliance" OR "SCAP" OR "container signing" | blue-posture-sys |
| threat intelligence, adversary profile, campaign tracking, STIX, TAXII, MISP, OSINT, threat landscape, intelligence requirement, TLP | IOC lifecycle, YARA rule creation, D3FEND, detection rule | 2 | "threat intelligence" OR "adversary profile" OR "campaign tracking" | blue-intel |
| D3FEND, countermeasure, defensive coverage, ATT&CK mapping, detection gap, countermeasure matrix, defensive architecture | threat intelligence collection, IOC, YARA, compliance | 11 | "D3FEND" OR "countermeasure mapping" OR "defensive coverage" | blue-d3fend |
| IOC lifecycle, IOC management, indicator enrichment, IOC aging, IOC retirement, YARA rule creation, YARA rule authoring, detection signature, STIX indicator | YARA scanning, yr scan, threat intelligence collection, D3FEND | 12 | "IOC lifecycle" OR "YARA rule creation" OR "indicator enrichment" | blue-ioc |

**Priority ordering rationale:** 1=blue-lead (governance, default authority). 2=blue-intel (intelligence drives all other domains). 3-5=Detection domain (most frequently invoked). 6-7=Forensics domain. 8-10=Compliance domain (narrower scope). 11-12=D3FEND/IOC (specialized analytical functions).

---

## Routing Disambiguation

> When this skill is the wrong choice and what happens if misrouted.

| Condition | Use Instead | Consequence of Misrouting |
|-----------|-------------|--------------------------|
| Building secure software or defensive architecture | `/eng-team` | Blue team produces detection and compliance artifacts, not hardened code; STRIDE/DREAD threat modeling and OWASP ASVS not loaded |
| Offensive security testing or penetration testing | `/red-team` | Defensive methodology produces detection rules instead of exploitation methodology; kill chain progression and scope authorization absent |
| Adversarial quality review of deliverables | `/adversary` | Security analysis methodology produces compliance reports instead of quality scores; S-014 rubric not available |
| General security research without defensive context | `/problem-solving` (ps-researcher) | Blue team requires assessment scope; 12 defensive agents loaded when task needs general-purpose research |
| Root cause analysis or debugging | `/problem-solving` (ps-investigator) | Blue team follows detection/response methodology, not causal investigation; 5 Whys not loaded |
| Requirements engineering or V&V | `/nasa-se` | Blue team produces assessment artifacts, not requirements; NPR-compliant traceability absent |

---

## References

| Source | Content |
|--------|---------|
| ADR-PROJ023-001 | Hybrid B+C Skill Architecture (accepted) |
| Phase 4 Detection Design | YARA-X, Suricata, Zeek, Falco, Tetragon, Sigma, Wazuh, Hayabusa, Chainsaw |
| Phase 4 Forensics Design | Ghidra, JADX, Plaso, Volatility, IR playbook, chain of custody |
| Phase 4 Compliance Design | Checkov, Trivy, Prowler, Kubescape, kube-bench, Kyverno, OpenSCAP, Cosign |
| Phase 4 Threat Intel Design | MISP, STIX/TAXII, D3FEND, IOC lifecycle, OSINT |
| `docs/governance/JERRY_CONSTITUTION.md` | Constitutional principles |
| `.context/rules/quality-enforcement.md` | Quality gate thresholds |

---

*Skill Version: 1.0.0*
*Constitutional Compliance: Jerry Constitution v1.0*
*SSOT: ADR-PROJ023-001*
*Created: 2026-03-14*
