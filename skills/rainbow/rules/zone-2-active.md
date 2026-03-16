# Zone 2: Active Reconnaissance/Interaction -- Guardrail Profile

> Active network interaction zone. Applies to agents performing reconnaissance, active queries against live targets, and controlled system interaction. REQUIRES engagement scope document. Dual-zone tools escalate to Zone 3 when operation mode crosses the exploitation boundary.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Zone Definition](#zone-definition) | What Zone 2 covers and who it applies to |
| [Engagement Scope Requirement](#engagement-scope-requirement) | Scope document structure and validation |
| [Permitted Operations](#permitted-operations) | Exhaustive list of allowed operation types |
| [Prohibited Operations](#prohibited-operations) | Operations that require Zone 3 escalation |
| [Tool Allowlist](#tool-allowlist) | Tools permitted at Zone 2 with allowed subcommands |
| [Dual-Zone Tool Escalation](#dual-zone-tool-escalation) | Nuclei, Kyverno, and Cosign Zone 2/3 boundary rules |
| [Engagement Lifecycle](#engagement-lifecycle) | Scope, execute, report, debrief phases |
| [Credential Filter](#credential-filter) | How credential filtering applies at Zone 2 |
| [Audit Logging](#audit-logging) | What must be logged for every Zone 2 operation |
| [Escalation Triggers](#escalation-triggers) | Conditions that force escalation to Zone 3 |
| [Traceability](#traceability) | ADR and design source references |

---

## Zone Definition

**Zone 2 (Active Reconnaissance/Interaction)** is the middle security zone. Agents operating in Zone 2 interact with live systems -- querying DNS, scanning ports, crawling web applications, intercepting traffic, and modifying cloud resources within authorized scope. Zone 2 operations can affect target system logs and may be detected by defensive monitoring.

### Applicable Sub-Skills and Agents

| Sub-Skill | Agent | Condition |
|-----------|-------|-----------|
| `/rainbow-recon` | `rainbow-recon-pipeline` | All operations |
| `/rainbow-recon` | `rainbow-recon-osint` | All operations |
| `/rainbow-cloud` | `rainbow-cloud-auditor` | Kyverno `mutate` mode (without `--resource`) |
| `/rainbow-cloud` | `rainbow-cloud-mapper` | All operations (Cartography queries live cloud APIs) |
| `/rainbow-runtime` | `rainbow-runtime-instrument` | `intercept` mode (mitmproxy traffic capture, Frida read-only hooks) |
| `/rainbow-supply-chain` | `rainbow-sc-verifier` | Cosign `download signature`, `download sbom` (remote registry access) |

---

## Engagement Scope Requirement

Zone 2 operations MUST NOT begin until an engagement scope document exists and has been validated by `rainbow-orchestrator` or `red-lead`.

### Scope Document Structure

The engagement scope document is a markdown file persisted at `skills/rainbow/output/{engagement-id}/SCOPE.md` within the active project workspace. It MUST contain the following fields.

| Field | Description | Validation Rule |
|-------|-------------|-----------------|
| `engagement_id` | Unique identifier for this engagement | Pattern: `RBW-NNNN` (e.g., `RBW-0001`) |
| `created_by` | Agent or operator who created the scope | Must be `rainbow-orchestrator`, `red-lead`, or operator name |
| `created_at` | ISO 8601 timestamp | Must be a valid timestamp |
| `authorized_targets` | Exhaustive list of targets (IPs, domains, URLs, cloud accounts, registries) | At least 1 target; no wildcards without explicit operator approval |
| `excluded_targets` | Targets explicitly excluded from scope | May be empty; if present, takes precedence over authorized targets |
| `time_window` | Start and end timestamps for authorized activity | `start` must be in the future or present; `end` must be after `start` |
| `technique_allowlist` | Specific techniques/tool modes authorized | At least 1 technique; must map to Zone 2 permitted operations |
| `escalation_authority` | Who can approve Zone 3 escalation | Must name a human operator |
| `rules_of_engagement` | Constraints on behavior (rate limits, stealth requirements, data handling) | At least 1 rule |
| `operator_approval` | Operator name and approval timestamp | REQUIRED before any Zone 2 operation executes |

### Scope Validation

Before routing any task to a Zone 2 agent, `rainbow-orchestrator` MUST verify:

1. The scope document exists at the expected path.
2. The `time_window` includes the current time.
3. The requested target is in `authorized_targets` and NOT in `excluded_targets`.
4. The requested technique is in `technique_allowlist`.
5. `operator_approval` is present and non-empty.

If any validation check fails, the orchestrator MUST reject the task and inform the user with the specific failing check per P-022.

---

## Permitted Operations

Zone 2 agents are authorized to perform the following operation types, subject to engagement scope constraints.

| Operation Type | Description | Example |
|---------------|-------------|---------|
| Subdomain enumeration | Discover subdomains of authorized target domains | `subfinder -d target.com` |
| Port scanning | Scan authorized target IPs/ranges for open ports | `naabu -host target.com -top-ports 1000` |
| HTTP probing | Probe discovered hosts for live HTTP services | `httpx -l hosts.txt -status-code -title` |
| DNS resolution | Resolve DNS records for authorized domains | `dnsx -l domains.txt -a -aaaa -mx` |
| Web crawling | Crawl authorized web applications for endpoint discovery | `katana -u https://target.com -d 3` |
| Vulnerability detection scanning | Run Nuclei detection templates against authorized targets | `nuclei -t cves/ -u https://target.com` |
| OSINT gathering | Collect publicly available intelligence on authorized targets | `amass enum -d target.com` |
| Cloud asset mapping | Map cloud infrastructure for authorized accounts | Cartography against authorized cloud accounts |
| Kubernetes resource mutation | Apply Kyverno mutations to authorized clusters | `kyverno apply policy.yaml` (without `--resource`, targets live cluster) |
| Traffic interception | Capture and inspect traffic from authorized targets | `mitmproxy` in transparent or regular mode |
| Remote signature/SBOM download | Download signatures or SBOMs from authorized registries | `cosign download signature image:tag` |
| Username enumeration (OSINT) | Discover usernames/profiles on public platforms | `maigret username` |

---

## Prohibited Operations

The following operations are NOT permitted at Zone 2. Attempting any of these MUST trigger escalation to Zone 3.

| Prohibited Operation | Required Zone | Escalation Path |
|---------------------|---------------|-----------------|
| Exploitation of any vulnerability | Zone 3 | Per-operation human approval required |
| Payload delivery or execution | Zone 3 | Per-operation human approval required |
| Credential extraction or dumping | Zone 3 | Per-operation human approval required |
| System modification (beyond authorized Kyverno mutations) | Zone 3 | Per-operation human approval required |
| Artifact signing or attestation | Zone 3 | Vault authorization required |
| Nuclei exploit templates | Zone 3 | Template classification check triggers escalation |
| Kyverno resource generation | Zone 3 | Per-operation human approval required |
| Post-exploitation activity | Zone 3 | Per-operation human approval required |
| Process modification via Frida | Zone 3 | Frida read-only hooks stay Zone 2; write hooks escalate |

---

## Tool Allowlist

Only the following tools and subcommands are permitted at Zone 2. Engagement scope validation MUST pass before any tool invocation.

| Tool | Allowed Subcommands/Modes | Forbidden at Zone 2 |
|------|--------------------------|---------------------|
| **Subfinder** | `-d`, `-dL` (domain enumeration) | -- |
| **httpx** | Probing with standard flags | -- |
| **dnsx** | DNS resolution modes | -- |
| **Naabu** | Port scanning with rate limits from RoE | Scanning targets outside scope |
| **Katana** | Web crawling with depth limits from RoE | -- |
| **Nuclei** | Detection templates ONLY (see dual-zone rules below) | Exploit templates, custom templates without review |
| **OWASP Amass** | `enum` subcommand | -- |
| **Maigret** | Username search | -- |
| **Cartography** | Cloud asset mapping for authorized accounts | Accounts outside scope |
| **Kyverno** | `apply` without `--resource` (mutate mode); `validate` | `generate` mode |
| **Cosign** | `download signature`, `download sbom` | `sign`, `attest`, `attach` |
| **mitmproxy** | Transparent/regular proxy capture | Traffic modification (use `mitmdump` scripts that modify responses) |
| **Frida** | Read-only hooks, function tracing | Write hooks, memory patching |

### Target Validation

Before every tool invocation, the agent MUST:

1. Extract the target (domain, IP, URL, cloud account) from the command arguments.
2. Check the target against `authorized_targets` in the engagement scope.
3. Check the target against `excluded_targets` in the engagement scope.
4. If the target is not authorized or is excluded, REJECT the command and log the rejection.

---

## Dual-Zone Tool Escalation

Three tools span the Zone 2/Zone 3 boundary. The classification is based on the specific CLI subcommand or template category -- not on agent judgment. For unrecognized subcommands not listed below, the default classification is the HIGHER zone (fail-closed).

### Nuclei (Home: `/rainbow-recon`)

| Operation | Zone | Classification Rule |
|-----------|------|-------------------|
| Detection templates: severity `info`, `low`, `medium`, `high`, `critical` WITHOUT any `deny_tags` per `nuclei-template-allowlist.yaml` (11 tags as of v1.0) | Zone 2 | Template is on the allowlist maintained in `/rainbow-recon/rules/nuclei-template-allowlist.yaml` |
| Exploit templates: matching any `deny_tags` entry per `nuclei-template-allowlist.yaml`, OR templates with `extractors` targeting `deny_extractor_fields` (12 fields as of v1.0) | Zone 3 | Template matches deny-tag list; agent presents template metadata to user for per-operation approval per P-020 |
| Custom/community templates not on allowlist | Zone 3 (default) | Fail-closed: all custom templates default to Zone 3 until reviewed and added to allowlist |

**Enforcement procedure:**

1. Agent parses the Nuclei template YAML to extract `info.severity` and `info.tags`.
2. Agent checks tags against the `deny_tags` list in `nuclei-template-allowlist.yaml` (11 tags as of v1.0).
3. Agent checks for `extractors` targeting fields matching the `deny_extractor_fields` list in `nuclei-template-allowlist.yaml` (12 fields as of v1.0).
4. If any deny-tag matches OR extractor targets sensitive fields: HALT and escalate to Zone 3.
5. If the template is not on the allowlist: HALT and escalate to Zone 3.
6. Otherwise: proceed at Zone 2.

### Kyverno (Home: `/rainbow-cloud`)

| Operation | Zone | Classification Rule |
|-----------|------|-------------------|
| `validate` mode | Zone 1 | `--resource` enforced (see `zone-1-analysis.md`) |
| `mutate` mode (`apply` without `--resource`) | Zone 2 | Requires engagement scope + cluster authorization |
| `generate` mode | Zone 3 | Resource generation requires per-operation human approval |

**Enforcement:** The `rainbow-cloud-auditor` agent MUST parse the Kyverno policy YAML to determine the operation type (`validate`, `mutate`, `generate`). Policies containing `generate` rules trigger Zone 3 escalation regardless of other content.

### Cosign (Home: `/rainbow-supply-chain`)

| Operation | Zone | Classification Rule |
|-----------|------|-------------------|
| `verify`, `tree` | Zone 1 | Read-only verification (see `zone-1-analysis.md`) |
| `download signature`, `download sbom` | Zone 2 | Read-only remote access; requires engagement scope for target registry |
| `sign`, `attest`, `attach` | Zone 3 | Artifact modification; requires per-operation approval + vault authorization |

---

## Engagement Lifecycle

Zone 2 operations follow a structured engagement lifecycle. Each phase has a gate that must be passed before proceeding.

### Phase 1: Scope

| Action | Owner | Gate |
|--------|-------|------|
| Create engagement scope document | `rainbow-orchestrator` or `red-lead` | -- |
| Define authorized targets, time window, technique allowlist | Operator | -- |
| Operator reviews and approves scope | Operator (human) | `operator_approval` field populated |
| `rainbow-orchestrator` validates scope document | `rainbow-orchestrator` | All validation checks pass |

### Phase 2: Execute

| Action | Owner | Gate |
|--------|-------|------|
| Route tasks to Zone 2 agents with scope reference | `rainbow-orchestrator` | Scope validated |
| Agent validates each target against scope before execution | Zone 2 agent | Target in `authorized_targets`, not in `excluded_targets` |
| Agent validates technique against `technique_allowlist` | Zone 2 agent | Technique on allowlist |
| Execute tool within rate limits specified in `rules_of_engagement` | Zone 2 agent | RoE constraints respected |
| Log all operations per audit logging requirements | Zone 2 agent | Audit log entry created |

### Phase 3: Report

| Action | Owner | Gate |
|--------|-------|------|
| Aggregate findings from all Zone 2 operations | `rainbow-reporter` (future agent (post-W3)) | All Zone 2 tasks complete or time window expired |
| Produce reconnaissance/assessment report | `rainbow-reporter` (future agent (post-W3)) | Report persisted to `skills/rainbow/output/{id}/reports/` |
| Identify findings requiring Zone 3 escalation | `rainbow-reporter` (future agent (post-W3)) | Zone 3 candidates flagged in report |

> **Note:** `rainbow-reporter` is a planned future agent (post-W3 wave). Until implemented, Phase 3 reporting is performed by `rainbow-orchestrator` or the operator directly.

### Phase 4: Debrief

| Action | Owner | Gate |
|--------|-------|------|
| Review scope coverage (targets assessed vs. authorized) | Operator + `rainbow-orchestrator` | -- |
| Review any scope violations or escalation events | Operator | -- |
| Archive engagement artifacts | `rainbow-orchestrator` | All artifacts in `skills/rainbow/output/{id}/` |
| Close engagement if Zone 3 is not needed | Operator | Explicit operator decision |

---

## Credential Filter

The credential filter pipeline applies to ALL tool output at Zone 2. Zone 2 tools are more likely to produce credential material than Zone 1 tools (reconnaissance output may contain leaked credentials, cloud audit results may expose secrets).

| Filter Layer | Applies at Zone 2 | Rationale |
|-------------|-------------------|-----------|
| L1: Regex pattern matching | Yes | Reconnaissance output frequently contains API keys, tokens in headers |
| L2: Entropy-based detection | Yes | OSINT and cloud mapping may surface encoded credentials |
| L3: Structural analysis | Yes | Cloud audit JSON output may contain sensitive configuration values |

**Fail-closed behavior applies.** If the credential filter crashes or times out, the tool output is rejected and quarantined. See `skills/rainbow/rules/rainbow-credential-filter.md` for the full credential filter specification.

**Zone 2 heightened sensitivity:** Zone 2 agents MUST treat any credential filter quarantine event as a potential credential exposure. The agent MUST:

1. Log the quarantine event with tool name, target, and timestamp.
2. Notify the user per P-020.
3. NOT attempt to re-run the tool to obtain the quarantined output.
4. Continue with remaining tasks using non-quarantined output.

---

## Audit Logging

Every Zone 2 operation MUST produce a detailed audit log entry. Zone 2 logging is more comprehensive than Zone 1 due to the live system interaction.

### Required Log Fields

| Field | Description | Example |
|-------|-------------|---------|
| `timestamp` | ISO 8601 operation timestamp | `2026-03-14T10:30:00Z` |
| `zone` | Always `2` | `2` |
| `engagement_id` | Reference to engagement scope document | `RBW-0001` |
| `agent` | Agent name that executed the operation | `rainbow-recon-pipeline` |
| `tool` | Tool name | `nuclei` |
| `subcommand` | Specific subcommand/mode invoked | `detection scan` |
| `target` | Target addressed (IP, domain, URL) | `target.com` |
| `target_authorized` | Whether target passed scope validation | `true` |
| `technique` | Technique category | `vulnerability-detection-scanning` |
| `technique_authorized` | Whether technique passed allowlist check | `true` |
| `result_summary` | One-line summary of findings | `12 findings (2 high, 4 medium, 6 info)` |
| `credential_filter_status` | Whether credential filter passed, quarantined, or rejected | `passed` |
| `duration_seconds` | How long the operation took | `47` |
| `escalation_triggered` | Whether this operation triggered zone escalation | `false` |

### Log Location

Audit logs are persisted to `skills/rainbow/output/{engagement-id}/audit/zone-2/{date}-{agent}-{tool}.log` within the active project workspace.

---

## Escalation Triggers

The following conditions MUST trigger escalation from Zone 2 to Zone 3. The agent halts the current operation and returns control to `rainbow-orchestrator` with the escalation reason.

| Trigger | Escalation Target | Action |
|---------|-------------------|--------|
| Nuclei template matches deny-tag list | Zone 3 | Halt; present template metadata to user for approval |
| Nuclei template not on allowlist | Zone 3 | Halt; request human review of template |
| Kyverno policy contains `generate` rules | Zone 3 | Halt; present policy and target namespace for approval |
| Cosign `sign`, `attest`, or `attach` requested | Zone 3 | Halt; request vault authorization and per-operation approval |
| Frida write hook or memory patch requested | Zone 3 | Halt; request per-operation approval |
| mitmproxy response modification script requested | Zone 3 | Halt; request per-operation approval |
| Target not in `authorized_targets` | REJECT (not escalation) | Do not execute; log rejection; inform user |
| Target in `excluded_targets` | REJECT (not escalation) | Do not execute; log rejection; inform user |
| Time window expired | REJECT (not escalation) | Do not execute; inform user scope has expired |
| Technique not in `technique_allowlist` | REJECT (not escalation) | Do not execute; inform user technique not authorized |
| Discovery of exploitable vulnerability | Informational (no automatic escalation) | Log finding in report; Zone 3 escalation requires operator decision |

---

## Traceability

| Reference | Location |
|-----------|----------|
| ADR-PROJ023-001 (Architecture Decision) | `projects/PROJ-023-exploit-framework/work/design/skill-architecture.md` |
| Security Zone Enforcement Mechanism | ADR-PROJ023-001, Section "Security Zone Enforcement Mechanism" |
| Dual-Zone Tool Escalation Protocol | ADR-PROJ023-001, Section "Dual-Zone Tool Escalation Protocol" |
| Credential Filter Architecture | ADR-PROJ023-001, Section "Credential Filter Architecture" |
| Credential Filter Rules | `skills/rainbow/rules/rainbow-credential-filter.md` |
| Zone 1 Guardrail Profile | `skills/rainbow/rules/zone-1-analysis.md` |
| Zone 3 Guardrail Profile | `skills/rainbow/rules/zone-3-exploit.md` |
