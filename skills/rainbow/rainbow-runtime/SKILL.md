---
name: rainbow-runtime
description: >-
  Runtime instrumentation sub-skill of /rainbow. Provides dual-zone network
  traffic interception (mitmproxy) and dynamic process instrumentation (Frida)
  within authorized engagement scope. Zone 2 (passive capture): transparent
  proxy capture, function tracing with read-only hooks. Zone 3 (active
  modification): response modification scripts, write hooks, memory patching --
  requires per-operation human approval (P-020). Invoke for: traffic
  interception, mitmproxy, Frida, runtime instrumentation, function tracing,
  process hooking, API hooking, protocol analysis, SSL interception, mobile
  app instrumentation, runtime security testing.
version: "1.0.0"
agents:
  - rainbow-runtime-instrument
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
activation-keywords:
  - "traffic interception"
  - "mitmproxy"
  - "mitmdump"
  - "mitmweb"
  - "Frida"
  - "frida-trace"
  - "runtime instrumentation"
  - "function tracing"
  - "function hooking"
  - "process hooking"
  - "process injection"
  - "API hooking"
  - "protocol analysis"
  - "SSL interception"
  - "TLS interception"
  - "mobile app instrumentation"
  - "proxy capture"
  - "runtime security"
  - "dynamic instrumentation"
  - "memory patching"
  - "Interceptor"
---

# Rainbow Runtime Sub-Skill

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
| [Security Zone Enforcement](#security-zone-enforcement) | Zone 2 passive capture, Zone 3 active modification |
| [Credential Filter](#credential-filter) | Mandatory output sanitization |
| [Internal Routing](#internal-routing) | How rainbow-orchestrator routes to this sub-skill |
| [Cross-Sub-Skill Data Contracts](#cross-sub-skill-data-contracts) | Pipeline integration with other sub-skills |
| [Known Limitations](#known-limitations) | Honest limitations disclosure per P-022 |
| [Constitutional Compliance](#constitutional-compliance) | Governance alignment |
| [Acceptance Criteria Coverage Matrix](#acceptance-criteria-coverage-matrix) | AC-to-file traceability |

---

## Purpose

The `/rainbow-runtime` sub-skill provides **tool-assisted runtime instrumentation** within authorized engagement boundaries. It covers two complementary domains: network traffic interception via mitmproxy and dynamic process instrumentation via Frida.

This sub-skill is part of the /rainbow composable architecture (ADR-PROJ023-001, Wave 3b). It operates as a **dual-zone agent**: Zone 2 for passive capture and read-only instrumentation, Zone 3 for active traffic/process modification requiring per-operation human approval.

### Key Capabilities

- **Network Traffic Interception** -- Capture and analyze HTTP/HTTPS traffic through seven proxy modes: regular, transparent, reverse, local, socks5, wireguard, upstream (mitmproxy, mitmdump, mitmweb)
- **Traffic Replay and Analysis** -- Replay captured flows for offline security analysis, filter by URL pattern, extract request/response pairs
- **Function Call Tracing** -- Trace function calls in target processes with read-only observation of arguments and return values (Frida Interceptor.attach, frida-trace)
- **Process and Device Enumeration** -- List processes on local, USB-connected, and remote devices (frida-ps, frida-ls-devices)
- **Function Discovery** -- Discover exported functions and internal methods in target processes (frida-discover)
- **Traffic Modification** -- Modify intercepted HTTP requests and responses via Python scripts (Zone 3, mitmproxy -s)
- **Function Hooking** -- Replace function behavior, modify arguments and return values (Zone 3, Frida Interceptor.replace)
- **Memory Patching** -- Write to process memory for runtime behavior modification (Zone 3, Frida Memory.write*)

### What This Sub-Skill Is NOT

- Does NOT exploit vulnerabilities (use `/rainbow-exploit`)
- Does NOT perform reconnaissance scanning (use `/rainbow-recon`)
- Does NOT generate SBOMs or scan supply chains (use `/rainbow-supply-chain`)
- Does NOT audit cloud configurations (use `/rainbow-cloud`)
- Does NOT provide penetration testing methodology without tool execution (use `/red-team`)
- Does NOT provide secure development guidance (use `/eng-team`)
- Does NOT perform malware analysis or threat detection (use `/blue-team`)

---

## When to Use

Activate when the request involves:

- Intercepting network traffic from an authorized target
- Setting up a proxy for HTTP/HTTPS traffic capture
- Analyzing captured traffic flows for security findings
- Tracing function calls in a target process
- Hooking API calls in a mobile application (Android/iOS)
- Discovering exported functions in a target binary
- Modifying intercepted traffic (Zone 3)
- Patching process memory or replacing function behavior (Zone 3)
- SSL/TLS interception and certificate pinning analysis
- Protocol analysis through intercepted traffic

Do NOT invoke when:

- Task requires vulnerability exploitation beyond traffic/process modification -- use `/rainbow-exploit`
- Task requires network reconnaissance scanning -- use `/rainbow-recon`
- Task requires supply chain scanning -- use `/rainbow-supply-chain`
- Task requires cloud security posture assessment -- use `/rainbow-cloud`
- Task is malware analysis or threat detection -- use `/blue-team`
- Task is penetration testing methodology without tool execution -- use `/red-team`
- No engagement scope document exists -- create one first via `engagement-scope-template.yaml`

---

## Agent Registry

| Agent | Role | Zone | Tools | Cognitive Mode | Tier |
|-------|------|------|-------|---------------|------|
| `rainbow-runtime-instrument` | Dual-zone runtime instrumentation specialist | Zone 2/3 | mitmproxy, mitmdump, mitmweb, Frida (frida, frida-trace, frida-ps, frida-ls-devices, frida-discover, frida-kill) | convergent | Tier B |

**Tool tier:** T2 (Read-Write). Agent does NOT have Task tool access per H-34/P-003.

**Tier classification rationale:** Both mitmproxy and Frida are classified as Tier B because they require external target interaction (network proxy setup, process attachment). Tier A tools (like Subfinder, Nuclei in /rainbow-recon) have direct CLI execution patterns; Tier B tools require environment configuration (proxy routing, device attachment, root/administrator access for transparent mode).

### Agent Selection Guide

| Request Type | Agent | Zone |
|-------------|-------|------|
| Traffic capture (any proxy mode) | `rainbow-runtime-instrument` | Zone 2 |
| Traffic replay and analysis | `rainbow-runtime-instrument` | Zone 2 |
| Function tracing (read-only) | `rainbow-runtime-instrument` | Zone 2 |
| Process/device enumeration | `rainbow-runtime-instrument` | Zone 2 |
| Traffic modification via script | `rainbow-runtime-instrument` | Zone 3 |
| Function replacement / write hooks | `rainbow-runtime-instrument` | Zone 3 |
| Memory patching | `rainbow-runtime-instrument` | Zone 3 |

---

## Tool Inventory

### Tier B Tools (Agent: rainbow-runtime-instrument)

**mitmproxy Suite:**

| Tool | Version | CLI Pattern | Output | Zone 2 Operations | Zone 3 Operations |
|------|---------|-------------|--------|-------------------|-------------------|
| **mitmproxy** | >= 10.0 | `mitmproxy --mode <mode>` | Interactive console | Traffic capture (all modes) | With `-s` modification scripts |
| **mitmdump** | >= 10.0 | `mitmdump -w <file>` | Flow files, stdout | Non-interactive capture, replay | With `-s` modification scripts |
| **mitmweb** | >= 10.0 | `mitmweb --listen-port <port>` | Web UI | Traffic capture via browser | With `-s` modification scripts |

**Frida Suite:**

| Tool | Version | CLI Pattern | Output | Zone 2 Operations | Zone 3 Operations |
|------|---------|-------------|--------|-------------------|-------------------|
| **frida** | >= 16.0 | `frida -n <proc> -l <script>` | REPL / script output | Read-only scripts (send/log) | Write hooks, function replacement |
| **frida-trace** | >= 16.0 | `frida-trace -n <proc> -i <fn>` | Trace output | Function call tracing | -- |
| **frida-ps** | >= 16.0 | `frida-ps [-U\|-R]` | Process list | Process enumeration | -- |
| **frida-ls-devices** | >= 16.0 | `frida-ls-devices` | Device list | Device enumeration | -- |
| **frida-discover** | >= 16.0 | `frida-discover -n <proc>` | Function list | Function discovery | -- |
| **frida-kill** | >= 16.0 | `frida-kill -n <proc>` | -- | -- | Process termination |

### Tier C Tools (Methodology Reference Only)

No Tier C tools for /rainbow-runtime. All tools are Tier B with direct CLI execution.

### Tool Relationship Diagram

```
mitmproxy (traffic interception)         Frida (process instrumentation)
    |                                         |
    +-- Zone 2: capture flows                 +-- Zone 2: trace functions
    |   mitmdump -w capture.flow              |   frida-trace -n proc -i fn
    |   mitmdump -n -r capture.flow           |   frida -n proc -l read.js
    |                                         |
    +-- Zone 3: modify flows                  +-- Zone 3: modify behavior
        mitmproxy -s modify.py                    frida -n proc -l write.js
        (per-operation approval)                  (per-operation approval)
```

---

## Security Zone Enforcement

**Dual-zone agent:** Zone 2 (default for passive capture) and Zone 3 (for active modification).

### Zone Classification

| Zone | Operations | Authorization |
|------|-----------|---------------|
| **Zone 2** | mitmproxy/mitmdump capture (all modes), flow replay, Frida read-only hooks, frida-trace, frida-ps, frida-ls-devices, frida-discover | Engagement scope required (operator-approved) |
| **Zone 3** | mitmproxy/mitmdump with modification scripts (-s), Frida write hooks, Frida Interceptor.replace, Frida memory patching, frida-kill | Per-operation human approval required |

### Dual-Zone Classification Authority

The authoritative zone classification for mitmproxy and Frida operations is defined in `skills/rainbow/rainbow-runtime/rules/runtime-interception-protocol.md`. This protocol provides:

1. **Exhaustive operation-to-zone mapping** for both mitmproxy and Frida operations.
2. **Script content analysis procedure** for classifying `-s` and `-l` scripts.
3. **Fail-closed default** for unrecognized operations.
4. **Escalation procedure** from Zone 2 to Zone 3.

### mitmproxy Dual-Zone Rules

| mitmproxy Operation | Zone | Classification Rule |
|---------------------|------|-------------------|
| All proxy modes (capture only) | Zone 2 | No `-s` flag, or `-s` script only logs/inspects |
| `-s` script that modifies request/response | Zone 3 | Script contains assignment to flow attributes |
| Flow replay/read (`-n -r`) | Zone 2 | Read-only analysis of captured flows |

### Frida Dual-Zone Rules

| Frida Operation | Zone | Classification Rule |
|-----------------|------|-------------------|
| Interceptor.attach with send()/console.log() only | Zone 2 | Callbacks observe but do not modify |
| frida-trace (all modes) | Zone 2 | Read-only function call tracing |
| frida-ps, frida-ls-devices, frida-discover | Zone 2 | Read-only enumeration |
| Interceptor.replace | Zone 3 | Function replacement modifies target behavior |
| args[N] = ..., retval.replace() | Zone 3 | Argument/return value modification |
| Memory.write* | Zone 3 | Direct memory modification |
| frida-kill | Zone 3 | Process termination modifies system state |

### Enforcement Layers

1. **Agent-level guardrails:** The agent validates targets against engagement scope and classifies operations before every tool invocation.
2. **Script content analysis:** The agent reads script content and scans for Zone 3 indicators before execution.
3. **Sub-skill rules:** This SKILL.md declares dual-zone with explicit Zone 3 escalation triggers.
4. **Runtime interception protocol:** `runtime-interception-protocol.md` provides the exhaustive classification matrix.
5. **Parent orchestrator:** `rainbow-orchestrator` validates engagement scope before routing Zone 2/3 requests.

### Zone 3 scope_gate_halt

When ANY Zone 3 operation is identified, the agent MUST:

1. HALT execution immediately.
2. Present the per-operation approval request to the operator (per zone-3-exploit.md).
3. Wait for explicit operator approval.
4. Only proceed on affirmative approval. Reject on silence, ambiguity, or timeout.
5. Log the approval decision in the Zone 3 audit log before execution.

---

## Credential Filter

The credential filter pipeline is MANDATORY for all tool output. No tool output enters the context window without passing through the 3-layer filter.

| Layer | Mechanism | Relevance to Runtime Instrumentation |
|-------|-----------|-------------------------------------|
| L1 | Regex pattern matching | Intercepted traffic frequently contains API keys, bearer tokens, session cookies, authorization headers |
| L2 | Entropy detection | Frida output may surface encoded credentials from process memory |
| L3 | Structural analysis | JSON API responses captured by mitmproxy may contain sensitive key-value pairs (password, token, secret fields) |

**Full specification:** `skills/rainbow/rules/rainbow-credential-filter.md`

**Fail-closed behavior:** Filter crash or timeout rejects the entire tool output block. Flagged content quarantined to `work/.credential-quarantine/`.

**Runtime instrumentation heightened sensitivity:** Traffic interception and process hooking have the HIGHEST probability of capturing credential material among all /rainbow operations. The credential filter MUST operate at maximum sensitivity for this sub-skill. The agent MUST assume all intercepted traffic contains credentials until the filter confirms otherwise.

**Zone-specific credential handling:**
- **Zone 2:** Quarantine events logged and user notified per P-020. Agent does NOT re-run tools to obtain quarantined output.
- **Zone 3:** All quarantined material tracked as evidence per zone-3-exploit.md evidence handling protocol. Quarantined credentials stored in vault via reference-only access.

---

## Internal Routing

The `rainbow-orchestrator` routes to this sub-skill based on request keywords.

### Activation Keywords (from rainbow-orchestrator)

Runtime instrumentation keywords that trigger routing to this sub-skill:
- Traffic interception, mitmproxy, mitmdump, proxy capture
- Frida, function tracing, function hooking, process hooking, process injection
- API hooking, protocol analysis, SSL interception, TLS interception
- Runtime instrumentation, dynamic instrumentation, mobile app instrumentation
- Memory patching, Interceptor, runtime security

### Disambiguation from Other Sub-Skills

| Request Contains | Routes To | Rationale |
|-----------------|-----------|-----------|
| "intercept traffic" / "mitmproxy" / "Frida" | `/rainbow-runtime` | Runtime instrumentation tools |
| "scan vulnerabilities" / "Nuclei" / "subdomain" | `/rainbow-recon` | Reconnaissance tools |
| "exploit" / "pwntools" / "Metasploit" | `/rainbow-exploit` | Exploitation tools |
| "SBOM" / "Trivy" / "supply chain" | `/rainbow-supply-chain` | Supply chain tools |
| "cloud posture" / "Prowler" / "Checkov" | `/rainbow-cloud` | Cloud audit tools |

---

## Cross-Sub-Skill Data Contracts

### Recon to Runtime Pipeline (Cross-Sub-Skill)

Reconnaissance findings from /rainbow-recon feed into runtime instrumentation for deeper analysis of discovered services.

| Stage | Source Agent | Target Agent | Data | Orchestrator Action |
|-------|-------------|-------------|------|-------------------|
| 1 | `rainbow-recon-pipeline` (httpx) | `rainbow-runtime-instrument` | Live HTTP services list | Construct handoff with artifact path |

**Minimum Entry Schema (JSONL):**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `url` | string | Yes | Live HTTP/HTTPS URL of target service |
| `status_code` | integer | Yes | HTTP response status code |
| `title` | string | No | Page title from httpx probe |
| `tech` | array | No | Detected technologies from httpx |
| `host` | string | Yes | Target hostname or IP |

**Empty-Result Handling:** If httpx discovers zero live services, the orchestrator MUST NOT route to `/rainbow-runtime`. The agent MUST: (1) acknowledge the empty input, (2) suggest alternative reconnaissance approaches.

**Handoff Quality:** Handoff follows `handoff-v2.schema.json`. Required: `confidence` >= 0.7 before routing to runtime pipeline. `key_findings` MUST include live service count, technology summary, and any scan limitations.

### Runtime to Exploit Pipeline (Cross-Sub-Skill)

Runtime analysis findings from /rainbow-runtime feed into /rainbow-exploit for exploitation of discovered weaknesses.

| Stage | Source Agent | Target Agent | Data | Orchestrator Action |
|-------|-------------|-------------|------|-------------------|
| 1 | `rainbow-runtime-instrument` | `/rainbow-exploit` agents | Runtime finding report | Construct handoff with artifact path; Zone 3 approval required |

**Minimum Entry Schema (Markdown/JSON):**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `finding_id` | string | Yes | Unique finding identifier |
| `target` | string | Yes | Target host/process/application |
| `finding_type` | enum | Yes | `auth_bypass`, `data_exposure`, `insecure_config`, `injection`, `api_weakness` |
| `evidence_path` | string | Yes | Path to captured traffic or trace artifact |
| `severity` | enum | Yes | `info`, `low`, `medium`, `high`, `critical` |

**Empty-Result Handling:** If runtime analysis discovers zero findings, the source agent MUST: (1) persist the clean analysis report, (2) include `finding_count: 0` in handoff `key_findings`, (3) set `confidence` to 0.8 (capture completed successfully with no findings). The orchestrator MUST NOT route to `/rainbow-exploit` when findings are empty.

**Handoff Quality:** Handoff follows `handoff-v2.schema.json`. Required: `confidence` >= 0.7. `key_findings` MUST include finding count by severity, target coverage, and capture duration.

---

## Known Limitations

> Honest disclosure per P-022. These are accepted architectural limitations documented in ADR-PROJ023-001.

### Zone Enforcement Is Behavioral-Only

Zone enforcement relies on LLM behavioral compliance with the zone classification procedure and script content analysis. No L3 runtime gate validates Bash commands or script content before execution.

**Compensating controls:**
1. **Script content analysis procedure** -- Agent reads and classifies script content before execution per `runtime-interception-protocol.md`
2. **NPT-009-complete forbidden actions** -- Zone violation entries use structured negation with consequences
3. **BDD zone enforcement scenarios** -- Comprehensive BDD scenarios testing Zone 2/3 classification, escalation, and boundary refusal
4. **Engagement scope validation** -- Every tool invocation gated by engagement scope checks
5. **Fail-closed default** -- Unrecognized operations classified as Zone 3

### Credential Filter Is W0 Specification-Only

The credential filter pipeline is a W0 specification. The agent declares `credential_filter_applied_to_all_tool_output` as a behavioral constraint. Runtime enforcement deferred to W1.

**Compensating controls:**
1. **Three-layer specification** -- L1 regex, L2 entropy, L3 structural fully specified in `rainbow-credential-filter.md`
2. **Behavioral declaration** -- Agent includes credential filter in `output_filtering`
3. **Fail-closed specification** -- Filter crash or timeout rejects entire tool output block
4. **BDD credential filter scenarios** -- Comprehensive credential filter application and quarantine scenarios
5. **Heightened sensitivity** -- Agent assumes all intercepted traffic contains credentials

### Script Classification Is LLM-Parsed

mitmproxy script content and Frida script content classification relies on the agent reading and analyzing script source code. This is an LLM-driven classification, not a deterministic runtime gate.

**Compensating controls:**
1. **Explicit indicator lists** -- Zone 2 and Zone 3 indicators documented in `runtime-interception-protocol.md`
2. **Fail-closed default** -- Ambiguous or unparseable scripts classified as Zone 3
3. **BDD scenarios** -- Script classification scenarios in test suite
4. **Human approval for Zone 3** -- All Zone 3 operations require per-operation human approval (P-020)

### Engagement Scope Validation Is Agent-Enforced

Engagement scope validation is performed by the agent before each operation. No middleware intercepts and validates scope before tool execution.

**Compensating controls:**
1. **scope_gate_halt guardrail** -- Agent declares HALT behavior when scope is missing
2. **Pre-execution gate** -- Agent documents the 5-check validation procedure
3. **BDD scenarios** -- Scope validation scenarios in test suite
4. **Audit logging** -- Every operation logs `target_authorized` and `technique_authorized` fields

### Agent Operates 2 CLI Toolkits (AP-07 Compliant)

The `rainbow-runtime-instrument` agent operates 2 CLI toolkits: mitmproxy suite (mitmproxy, mitmdump, mitmweb) and Frida suite (frida, frida-trace, frida-ps, frida-ls-devices, frida-discover, frida-kill). This represents 2 distinct tool ecosystems but approximately 9 individual CLI binaries.

**Justification:** mitmproxy and Frida are complementary runtime instrumentation toolkits. mitmproxy handles network traffic; Frida handles process internals. They address different layers of the same runtime analysis task. The agent never selects between them based on ambiguous context -- network traffic requests use mitmproxy, process instrumentation requests use Frida.

**Compensating controls:**
1. **Clear domain separation** -- mitmproxy for network layer, Frida for process layer; no ambiguous tool selection
2. **Unified purpose** -- Both toolkits serve the single purpose of runtime instrumentation
3. **AP-07 monitoring** -- Combined tool count monitored; if additional tools are needed, they should route to a new agent or sub-skill
4. **Suite binaries share patterns** -- mitmproxy suite shares proxy patterns; Frida suite shares `-n`/`-U`/`-R` targeting patterns

### Tool Availability Is Environment-Dependent

Both mitmproxy and Frida must be installed in the execution environment. Frida additionally requires appropriate privileges (root/administrator for some operations, USB debugging for Android).

**Compensating controls:**
1. **AD-010 degradation levels** -- Level 0 (full tools), Level 1 (partial), Level 2 (standalone guidance)
2. **P-022 disclosure** -- Agent discloses when tools are unavailable and operates in degraded mode
3. **Container infrastructure** -- Planned via T0.8 for consistent tool availability (deferred)

---

## Constitutional Compliance

| Principle | Application |
|-----------|-------------|
| **P-003 / H-01** | Agent is T2 worker. No Task tool access. No delegation. |
| **P-020 / H-02** | Instrumentation scope approved by user. Engagement scope required. Zone 3 modification requires per-operation human approval. scope_gate_halt enforced. |
| **P-022 / H-03** | Capture coverage limitations disclosed. Tool availability reported. Zone classification decisions transparent. Known limitations documented above. |
| **P-001** | All findings evidence-based with captured traffic and trace log citations. |
| **P-002** | All capture artifacts, trace logs, and audit logs persisted. |
| **H-34** | Agent uses dual-file architecture (.md + .governance.yaml). Constitutional compliance triplet present. |

---

## Acceptance Criteria Coverage Matrix

| AC | Description | Satisfied By |
|----|-------------|-------------|
| AC-F-02 | Agent definition follows dual-file architecture (H-34) | `agents/rainbow-runtime-instrument.md` + `.governance.yaml` |
| AC-F-03 | Constitutional compliance triplet (H-35) | `.governance.yaml`: `constitution.principles_applied` includes P-003, P-020, P-022; `capabilities.forbidden_actions` >= 3 entries (7 entries present) |
| AC-F-04 | Zone enforcement rules and escalation protocols | `rules/runtime-interception-protocol.md` (dual-zone classification); SKILL.md [Security Zone Enforcement](#security-zone-enforcement) |
| AC-F-16 | BDD scenarios per agent (H-20) | `tests/bdd/test_runtime_instrument.feature` (39 scenarios) |
| AC-F-17 | Credential filter integration | SKILL.md [Credential Filter](#credential-filter); agent `.md` Credential Filter Application section; BDD credential filter scenarios |
| H-20 | BDD test-first, 90% line coverage | 39 BDD scenarios covering: engagement scope (6), mitmproxy Zone 2 (7), Frida Zone 2 (5), Zone 3 classification/escalation (9), credential filter (3), output (2), constitutional (3), adversarial (2), degradation (2) |

---

## References

| Source | Content |
|--------|---------|
| ADR-PROJ023-001 | Architecture decision: composable sub-skill structure, agent registry, zone classification |
| `skills/rainbow/SKILL.md` | Parent skill: routing, engagement lifecycle, security zone overview |
| `skills/rainbow/rules/rainbow-credential-filter.md` | Credential filter 3-layer specification |
| `skills/rainbow/rules/zone-2-active.md` | Zone 2 guardrail profile |
| `skills/rainbow/rules/zone-3-exploit.md` | Zone 3 guardrail profile |
| `skills/rainbow/rules/engagement-lifecycle.md` | Engagement lifecycle model |
| `skills/rainbow/rules/engagement-scope-template.yaml` | Engagement scope template |
| `skills/rainbow/rules/rules-of-engagement-template.md` | Rules of engagement template |
| `skills/rainbow/rainbow-runtime/rules/runtime-interception-protocol.md` | Dual-zone classification authority |
| mitmproxy documentation | `https://docs.mitmproxy.org/stable/` |
| Frida documentation | `https://frida.re/docs/home/` |

---

*Sub-Skill Version: 1.0.0*
*Constitutional Compliance: Jerry Constitution v1.0*
*SSOT: ADR-PROJ023-001*
*Created: 2026-03-16*
