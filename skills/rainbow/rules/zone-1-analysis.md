# Zone 1: Analysis -- Guardrail Profile

> Read-only analysis zone. Applies to all agents operating in passive assessment mode. No engagement scope required. No per-operation approval required. All tool output passes through the credential filter before context window entry.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Zone Definition](#zone-definition) | What Zone 1 covers and who it applies to |
| [Permitted Operations](#permitted-operations) | Exhaustive list of allowed operation types |
| [Prohibited Operations](#prohibited-operations) | Operations that require Zone 2 or Zone 3 escalation |
| [Tool Allowlist](#tool-allowlist) | Tools permitted at Zone 1 with allowed subcommands |
| [Dual-Zone Tool Restrictions](#dual-zone-tool-restrictions) | Cosign and Kyverno Zone 1 constraints |
| [Scope Requirements](#scope-requirements) | What authorization is needed to operate |
| [Credential Filter](#credential-filter) | How credential filtering applies at Zone 1 |
| [Audit Logging](#audit-logging) | What must be logged for every Zone 1 operation |
| [Escalation Triggers](#escalation-triggers) | Conditions that force escalation out of Zone 1 |
| [Traceability](#traceability) | ADR and design source references |

---

## Zone Definition

**Zone 1 (Analysis)** is the lowest-privilege security zone in the /rainbow 3-layer zone model. Agents operating in Zone 1 perform passive, read-only assessment of artifacts, configurations, and supply chain metadata. Zone 1 operations produce local analysis artifacts (reports, SBOMs, vulnerability lists) without interacting with live systems or modifying any target.

### Applicable Sub-Skills and Agents

| Sub-Skill | Agent | Condition |
|-----------|-------|-----------|
| `/rainbow-supply-chain` | `rainbow-sc-scanner` | All operations |
| `/rainbow-supply-chain` | `rainbow-sc-verifier` | Cosign `verify` and `tree` subcommands ONLY |
| `/rainbow-cloud` | `rainbow-cloud-auditor` | Kyverno `validate` mode with `--dry-run` ONLY; Checkov scan mode |
| `/blue-team` | `blue-detect` | All operations |
| `/blue-team` | `blue-malware-analyst` | All operations |
| `/blue-team` | `blue-incident-resp` | All operations (methodology-only) |
| `/blue-team` | `blue-comply` | All operations (methodology-only) |

---

## Permitted Operations

Zone 1 agents are authorized to perform the following operation types. Any operation not listed here is prohibited at Zone 1.

| Operation Type | Description | Example |
|---------------|-------------|---------|
| Local artifact scanning | Analyze files, containers, IaC manifests present in the local workspace | `syft scan ./image.tar` |
| SBOM generation | Produce software bill of materials from local artifacts | `syft packages dir:./src -o spdx-json` |
| Vulnerability matching | Match SBOMs or package lists against vulnerability databases | `grype sbom:./sbom.json` |
| Configuration auditing | Assess IaC and cloud configuration files against policy baselines | `checkov -d ./terraform/` |
| Signature verification | Verify existing signatures on container images or artifacts | `cosign verify --key cosign.pub image:tag` |
| Policy validation | Validate Kubernetes resources against policies without mutation | `kyverno apply policy.yaml --resource pod.yaml --dry-run` |
| Static malware analysis | Analyze binary artifacts without execution | Ghidra headless analysis, JADX decompilation |
| Detection rule evaluation | Apply YARA rules to local samples | `yara-x rules.yar sample.bin` |
| Report generation | Produce analysis reports from tool output | Aggregation and formatting of scan results |

---

## Prohibited Operations

The following operations are NOT permitted at Zone 1. Attempting any of these MUST trigger escalation to the appropriate zone.

| Prohibited Operation | Required Zone | Escalation Path |
|---------------------|---------------|-----------------|
| Network interaction with live targets | Zone 2 | Route through `rainbow-orchestrator` with engagement scope |
| Active reconnaissance (subdomain enumeration, port scanning) | Zone 2 | Route to `/rainbow-recon` agents |
| Artifact signing or attestation | Zone 3 | Cosign `sign`/`attest` requires per-operation approval |
| Kubernetes resource mutation | Zone 2 | Kyverno `mutate` requires engagement scope |
| Kubernetes resource generation | Zone 3 | Kyverno `generate` requires per-operation approval |
| Exploitation of any kind | Zone 3 | Route to `/rainbow-exploit` agents |
| Traffic interception | Zone 2 | Route to `/rainbow-runtime` agents |
| Process instrumentation | Zone 2/3 | Route to `/rainbow-runtime` agents |
| Credential extraction | Zone 3 | Route to `/rainbow-exploit` agents |

---

## Tool Allowlist

Only the following tools and subcommands are permitted at Zone 1. Any tool invocation not matching this allowlist MUST be rejected.

| Tool | Allowed Subcommands/Modes | Forbidden at Zone 1 |
|------|--------------------------|---------------------|
| **Syft** | `scan`, `packages`, `attest` (local only) | Remote registry pulls without local cache |
| **Grype** | `db check`, `db update`, scan against local SBOM/image | -- |
| **Trivy** | `image`, `fs`, `config`, `sbom` (local targets) | `server` mode, remote repository scanning |
| **OSV-Scanner** | `scan` against local lockfiles/SBOMs | -- |
| **Checkov** | `-d`, `-f`, `--framework` (scan mode) | `--fix` (auto-remediation) |
| **Cosign** | `verify`, `tree` | `sign`, `attest`, `attach`, `download` |
| **Kyverno** | `apply --dry-run`, `test` | `apply` without `--dry-run`, `mutate`, `generate` |
| **Snyk CLI** | `test`, `monitor` (read-only analysis) | `fix`, `ignore` (state-changing) |
| **YARA-X** | Rule matching against local samples | -- |
| **Ghidra** | Headless analysis, decompilation | -- |
| **JADX** | APK/DEX decompilation | -- |

### Subcommand Enforcement

Agents MUST validate CLI arguments against the allowlist before execution. The validation check operates as follows:

1. Parse the intended command into tool name and subcommand/flags.
2. Match against the allowlist entry for that tool.
3. If the subcommand or any flag appears in the "Forbidden at Zone 1" column, REJECT the command and log the rejection.
4. If the tool is not in the allowlist at all, REJECT the command.

---

## Dual-Zone Tool Restrictions

Two tools span security zone boundaries. At Zone 1, only the following restricted operation modes are permitted.

### Cosign (Home: `/rainbow-supply-chain`)

| Permitted at Zone 1 | Prohibited at Zone 1 | Escalation Target |
|---------------------|---------------------|-------------------|
| `cosign verify --key <pubkey> <image>` | `cosign sign` | Zone 3 (per-operation approval + vault authorization) |
| `cosign tree <image>` | `cosign attest` | Zone 3 |
| -- | `cosign attach` | Zone 3 |
| -- | `cosign download signature` | Zone 2 (engagement scope for remote registry) |
| -- | `cosign download sbom` | Zone 2 (engagement scope for remote registry) |

**Enforcement:** The `rainbow-sc-verifier` agent MUST check the Cosign subcommand against the Zone 1 allowlist (`verify`, `tree`) before execution. Any other subcommand triggers zone escalation back to `rainbow-orchestrator`.

### Kyverno (Home: `/rainbow-cloud`)

| Permitted at Zone 1 | Prohibited at Zone 1 | Escalation Target |
|---------------------|---------------------|-------------------|
| `kyverno apply --dry-run <policy> --resource <resource>` | `kyverno apply` without `--dry-run` | Zone 2 (engagement scope + cluster authorization) |
| `kyverno test <test-dir>` | `kyverno apply --generate` | Zone 3 (per-operation approval) |

**Enforcement:** The `rainbow-cloud-auditor` agent MUST verify that `--dry-run` is present in all Kyverno `apply` invocations at Zone 1. Absence of `--dry-run` triggers zone escalation.

---

## Scope Requirements

Zone 1 operations require **project scope only** -- no engagement scope document is needed.

| Requirement | Zone 1 | Zone 2 | Zone 3 |
|------------|--------|--------|--------|
| Project scope (JERRY_PROJECT set) | REQUIRED | REQUIRED | REQUIRED |
| Engagement scope document | NOT required | REQUIRED | REQUIRED |
| Per-operation human approval | NOT required | NOT required | REQUIRED |
| Credential vault authorization | NOT required | Conditional | REQUIRED for signing/attestation |

Project scope means `JERRY_PROJECT` is set (H-04) and the work is tracked in the project worktracker. This is the standard Jerry session requirement -- no additional authorization is needed for Zone 1 work.

---

## Credential Filter

The credential filter pipeline applies to ALL tool output at Zone 1, even though Zone 1 tools are unlikely to produce credential material.

| Filter Layer | Applies at Zone 1 | Rationale |
|-------------|-------------------|-----------|
| L1: Regex pattern matching | Yes | Defense-in-depth; scan output may contain credentials in configuration files |
| L2: Entropy-based detection | Yes | Catches novel credential formats in IaC scan results |
| L3: Structural analysis | Yes | JSON/YAML output from Checkov, Trivy may contain sensitive field values |

**Fail-closed behavior applies.** If the credential filter crashes or times out, the tool output is rejected and quarantined. See `skills/rainbow/rules/rainbow-credential-filter.md` for the full credential filter specification.

---

## Audit Logging

Every Zone 1 operation MUST produce an audit log entry. Zone 1 audit logging is lightweight compared to Zone 2/3.

### Required Log Fields

| Field | Description | Example |
|-------|-------------|---------|
| `timestamp` | ISO 8601 operation timestamp | `2026-03-14T10:30:00Z` |
| `zone` | Always `1` | `1` |
| `agent` | Agent name that executed the operation | `rainbow-sc-scanner` |
| `tool` | Tool name | `syft` |
| `subcommand` | Specific subcommand invoked | `scan` |
| `target` | What was scanned (local path, not network target) | `./image.tar` |
| `result_summary` | One-line summary of findings | `47 vulnerabilities (3 critical, 12 high)` |
| `credential_filter_status` | Whether credential filter passed, quarantined, or rejected | `passed` |

### Log Location

Audit logs are persisted to `work/rainbow/audit/zone-1/{date}-{agent}-{tool}.log` within the active project workspace.

---

## Escalation Triggers

The following conditions MUST trigger escalation out of Zone 1. The agent halts the current operation and returns control to `rainbow-orchestrator` with the escalation reason.

| Trigger | Escalation Target | Action |
|---------|-------------------|--------|
| Tool subcommand not on Zone 1 allowlist | Zone 2 or Zone 3 (per dual-zone protocol) | Reject command; return escalation reason to orchestrator |
| Scan target is a remote URL or network endpoint | Zone 2 | Do not execute; request engagement scope |
| Tool output suggests active exploitation opportunity | No action (informational) | Log finding; do not attempt exploitation |
| Credential filter quarantines output | Continue at Zone 1 | Log quarantine event; notify user per P-020 |
| Agent receives task requiring network interaction | Zone 2 | Return task to orchestrator for re-routing |

---

## Traceability

| Reference | Location |
|-----------|----------|
| ADR-PROJ023-001 (Architecture Decision) | `projects/PROJ-023-exploit-framework/work/design/skill-architecture.md` |
| Security Zone Enforcement Mechanism | ADR-PROJ023-001, Section "Security Zone Enforcement Mechanism" |
| Dual-Zone Tool Escalation Protocol | ADR-PROJ023-001, Section "Dual-Zone Tool Escalation Protocol" |
| Credential Filter Architecture | ADR-PROJ023-001, Section "Credential Filter Architecture" |
| Credential Filter Rules | `skills/rainbow/rules/rainbow-credential-filter.md` |
| Zone 2 Guardrail Profile | `skills/rainbow/rules/zone-2-active.md` |
| Zone 3 Guardrail Profile | `skills/rainbow/rules/zone-3-exploit.md` |
