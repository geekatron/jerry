# ADR-PROJ010-005: Tool Integration Adapter Architecture -- MCP-Primary with Common Interface

<!--
DOCUMENT-ID: ADR-PROJ010-005
AUTHOR: ps-architect agent
DATE: 2026-02-22
STATUS: PROPOSED
PARENT: FEAT-014 (Tool Integration Adapter Architecture)
EPIC: EPIC-002 (Architecture & Design)
PROJECT: PROJ-010-cyber-ops
ADR-ID: ADR-PROJ010-005
TYPE: Architecture Decision Record
-->

> **ADR ID:** ADR-PROJ010-005
> **Version:** 1.0.0
> **Date:** 2026-02-22
> **Author:** ps-architect
> **Status:** PROPOSED
> **Deciders:** User (P-020 authority), ps-architect (recommendation)
> **Quality Target:** >= 0.95
> **Parent Feature:** FEAT-014 (Tool Integration Adapter Architecture)
> **Parent Epic:** EPIC-002 (Architecture & Design)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Status](#status) | Current decision lifecycle stage and ratification state |
| [Context](#context) | Why this decision is needed, requirements, and constraints |
| [Decision](#decision) | Protocol hierarchy, common interface, SARIF normalization, standalone design, security controls, and implementation priority |
| [Options Considered](#options-considered) | Four integration approaches evaluated per AD-005 |
| [Consequences](#consequences) | Positive, negative, and neutral outcomes |
| [Evidence Base](#evidence-base) | Summary of Phase 1 research findings from Stream C and synthesis |
| [Compliance](#compliance) | R-012, R-020, P-003, P-020 compliance assessment |
| [Related Decisions](#related-decisions) | Upstream and downstream decision linkages |
| [Limitations and Epistemic Status](#limitations-and-epistemic-status) | Epistemic boundaries and validation requirements |
| [References](#references) | Source citations |

---

## Status

**PROPOSED** -- This ADR requires adversarial review and user ratification before transitioning to ACCEPTED.

**Scope:** This ADR formalizes three architecture decisions from Phase 1 research synthesis (S-002):

| Decision ID | Title | Confidence |
|-------------|-------|------------|
| AD-005 | MCP-Primary Tool Integration with CLI/API Fallback | HIGH |
| AD-006 | SARIF-Based Finding Normalization | HIGH |
| AD-010 | Standalone Capable Design with Three-Level Degradation | HIGH |

All three decisions achieved HIGH confidence through cross-stream convergence in Phase 1 research. AD-005 and AD-006 map directly to FEAT-014 (Tool Integration Adapter Architecture). AD-010 maps to both FEAT-014 and FEAT-010 (Agent Team Architecture) and is included here because standalone capability is an architectural property of the adapter layer.

---

## Context

### Why This Decision Is Needed

R-012 (Tool Integration Architecture) requires that both /eng-team and /red-team skills define integration points with external tooling frameworks and that these integrations be architected as pluggable adapters. R-012 further mandates that skills be fully capable without external tools -- tools augment capability, they do not enable it. Without a formalized adapter architecture, each tool integration would be ad hoc, creating inconsistent interfaces, duplicated parsing logic, and tight coupling between agent logic and tool-specific details. This ADR establishes the architectural foundation that all tool integrations across both skills must follow.

### Background

Phase 1 research produced three research artifacts in Stream C (Tool Integration):

- **C-001** (Offensive Tool Ecosystem Survey): Analyzed 12 offensive tools across API type, automation level, output format, and agentic feasibility. Identified three integration tiers: API-native (Metasploit, Burp Suite, BloodHound CE), structured CLI (Nuclei, Nmap, Hashcat, NetExec), and programmatic library (Impacket, pymetasploit3). Confirmed that 6 existing security MCP servers validate the MCP wrapping pattern for security tools.

- **C-002** (Defensive Tool Ecosystem Survey): Analyzed 12 defensive tools with the same framework. Identified SARIF v2.1.0 as the de facto finding normalization standard with native support from CodeQL, Semgrep, Nuclei, Trivy, and Checkmarx. Identified two distinct integration patterns: pipeline integration (stateless CLI with structured output) and platform API (stateful REST/GraphQL with authentication).

- **C-003** (Agentic Tool Integration Patterns): Analyzed MCP protocol adoption (97M+ monthly SDK downloads, 13,000+ servers as of late 2025), three adapter patterns (MCP server, CLI adapter, API adapter), the "standalone capable" design pattern, security sandboxing approaches, and existing security MCP server implementations. Designed the common adapter interface and finding normalization schema.

The synthesis artifact S-002 (Architecture Implications) consolidated these findings into three architecture decisions (AD-005, AD-006, AD-010) and identified cross-cutting concerns for tool integration adapter design, including scope-validating proxy integration, security controls at the adapter layer, and data interchange format convergence.

### Requirements

| Requirement | Source | Impact on Architecture |
|-------------|--------|------------------------|
| R-012 | PLAN.md | Pluggable adapter architecture; standalone capable design; tools augment, not enable |
| R-020 | PLAN.md | Authorization verification before active testing; scope enforcement at tool invocation layer |
| R-013 | PLAN.md | Quality gate >= 0.95; /adversary integration for deliverable quality |
| R-011 | PLAN.md | Configurable rule sets; tool selection adaptable per engagement profile |
| AD-001 | S-002 | Methodology-first design paradigm; agents defined by knowledge domains, not tool operation |
| AD-004 | S-002 | Three-layer authorization; Tool Proxy validates scope before tool execution |

### Constraints

| Constraint | Source | Impact on Design |
|------------|--------|------------------|
| **AD-001: Methodology-first** | S-002 (highest-confidence finding) | Every agent capability must work without tools. Tool integration is enhancement, not dependency. |
| **AD-004: Three-layer authorization** | S-002 | All /red-team tool invocations must pass through scope-validating Tool Proxy before execution. |
| **P-003: No recursive subagents** | Jerry Constitution (HARD) | Tool adapters operate within the orchestrator -> worker pattern; no nested agent spawning for tool orchestration. |
| **Security tool safety** | Domain constraint | Security tools can cause damage (active scanning, exploitation). Sandboxing, credential isolation, and scope enforcement are non-negotiable. |
| **Tool availability variance** | Operational constraint | Tools may be unavailable due to licensing (Burp Suite, Cobalt Strike), infrastructure (SonarQube requires server), or network constraints. Architecture must handle all availability states. |
| **Output format heterogeneity** | C-001, C-002 | Tools produce SARIF, JSON, XML, CycloneDX/SPDX, structured text, and unstructured text. A normalization layer is required. |
| **MCP attack vectors** | C-003 | Prompt injection via tool output is a documented MCP attack vector (Red Hat, Pillar Security, Practical DevSecOps). Output validation before agent consumption is mandatory. |

---

## Decision

This ADR establishes the tool integration adapter architecture for PROJ-010's /eng-team and /red-team skills. The architecture comprises five integrated design decisions: a protocol hierarchy with common adapter interface (AD-005), SARIF-based finding normalization (AD-006), standalone capable design with graceful degradation (AD-010), security controls at the adapter layer, and a phased implementation priority.

### 1. Protocol Hierarchy with Common Adapter Interface (AD-005)

**Decision:** Adopt MCP as the primary integration protocol, CLI adapters as the first fallback, API adapters as the second fallback, and library adapters as the third fallback -- all behind a common adapter interface.

**Protocol Hierarchy:**

| Priority | Protocol | When to Use | Trade-offs |
|----------|----------|-------------|------------|
| Primary | **MCP Server** | Tool has or can get an MCP server; used frequently across sessions; multiple agents need access | Native Claude Code integration; structured tool calling; requires MCP server implementation |
| Fallback 1 | **CLI Adapter** | Tool is CLI-based with structured output; no MCP server available; lightweight/infrequent use | Simple implementation; no daemon needed; subprocess overhead; output parsing required |
| Fallback 2 | **API Adapter** | Tool exposes REST/GraphQL/RPC API; persistent state or session management needed | Rich interaction; session management; requires running service; authentication complexity |
| Fallback 3 | **Library Adapter** | Tool provides Python library for direct integration (e.g., Impacket, pymetasploit3) | Zero parsing overhead; direct protocol access; tighter coupling to tool internals |

**Rationale:** Claude Code natively supports MCP, making it the natural primary protocol. The 97M+ monthly SDK downloads and 13,000+ MCP servers (as of late 2025) validate MCP as the industry standard for AI-tool integration, backed by Anthropic, OpenAI, Google, and Microsoft. Six existing security MCP servers (mcp-for-security, pentest-mcp, pentestMCP, hexstrike-ai, sast-mcp, Semgrep MCP) prove that the pattern works for security tools specifically. FastMCP 3.0 (released January 2026) provides a mature framework for building custom MCP servers in Python. However, most current security tools lack MCP servers, making CLI adapters the practical first fallback for initial implementation. API adapters handle tools with REST/GraphQL interfaces (SonarQube, Burp Suite, ZAP, BloodHound CE). Library adapters handle tools that expose Python libraries for direct protocol-level access (Impacket, pymetasploit3).

**Common Adapter Interface:**

All adapter types implement a common interface that abstracts protocol-specific details from agent logic:

```
execute(tool_name: str, params: ToolParams) -> StructuredResult | ToolUnavailableError
```

| Method | Purpose |
|--------|---------|
| `execute(params)` | Execute tool operation and return structured result or unavailability error |
| `is_available()` | Check whether tool is installed, reachable, and licensed |
| `get_capabilities()` | Return tool's supported operations for agent discovery |
| `validate_params(params)` | Validate parameters before execution (pre-flight check) |

**Design rules:**
- Agent code calls adapters, never tools directly.
- Agent logic operates on normalized findings (see Section 2), never on raw tool output.
- Adapter availability is checked at execution time, not design time.
- Tool substitution (replacing one adapter with another) requires zero agent code changes.
- Each adapter handles authentication, timeout, error recovery, and output parsing internally.

**Architecture:**

```
+----------------------------------------------------------------------+
|                        Jerry Cyber Ops Skills                         |
|                                                                       |
|  +------------------+    +-------------------+    +-----------------+ |
|  | /red-team Skill  |    | /eng-team Skill   |    | Shared Layer    | |
|  |                  |    |                   |    |                 | |
|  | - red-recon      |    | - eng-devsecops   |    | - Finding       | |
|  | - red-vuln       |    | - eng-security    |    |   Schema        | |
|  | - red-exploit    |    | - eng-infra       |    | - SARIF Parser  | |
|  | - red-privesc    |    | - eng-qa          |    | - Adapter Base  | |
|  | - (all 11)       |    | - (all 10)        |    | - Credential    | |
|  +--------+---------+    +--------+----------+    |   Broker        | |
|           |                       |               +---------+-------+ |
|           v                       v                         |         |
|  +--------------------------------------------------------------+    |
|  |                    Tool Adapter Layer                          |    |
|  |                                                                |    |
|  |  +----------+  +----------+  +----------+  +----------+      |    |
|  |  | MCP      |  | CLI      |  | API      |  | Library  |      |    |
|  |  | Adapters |  | Adapters |  | Adapters |  | Adapters |      |    |
|  |  +----------+  +----------+  +----------+  +----------+      |    |
|  +--------------------------------------------------------------+    |
+----------------------------------------------------------------------+
           |                |               |              |
     MCP Protocol      subprocess       HTTP/RPC      Python import
           |                |               |              |
     +----------+    +----------+    +----------+    +----------+
     | Nmap MCP |    | nmap     |    | SonarQube|    | impacket |
     | Semgrep  |    | nuclei   |    | ZAP API  |    | pymsf3   |
     | MCP      |    | trivy    |    | Snyk API |    |          |
     +----------+    | checkov  |    | Burp API |    |          |
                     +----------+    +----------+    +----------+
```

### 2. SARIF-Based Finding Normalization (AD-006)

**Decision:** Adopt SARIF v2.1.0 as the primary finding normalization format with a 12-field common Finding schema. All tool outputs are normalized to this schema before agent consumption.

**Rationale:** SARIF v2.1.0 is an OASIS standard with native support from the highest-priority security tools: CodeQL, Semgrep, Nuclei, Trivy, Checkmarx, and Burp Suite DAST. SARIF includes severity, source location, rule metadata, and fix suggestions in a structured, machine-readable format. Using SARIF as the normalization target means that SARIF-producing tools require minimal parsing, while non-SARIF tools are normalized through custom normalizers. This is consistent with Convergence 5 from the Phase 1 synthesis: JSON Schema for tool definitions, SARIF for findings, YAML for configuration -- three structured formats forming the universal data interchange layer.

**Common Finding Schema:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | `str` | Unique finding identifier (tool-scoped) |
| `source_tool` | `str` | Tool that produced the finding |
| `severity` | `enum` | CRITICAL, HIGH, MEDIUM, LOW, INFO |
| `category` | `enum` | VULNERABILITY, MISCONFIGURATION, SECRET, COMPLIANCE, LICENSE, WEAK_CRYPTO, INJECTION, etc. |
| `title` | `str` | Human-readable finding title |
| `description` | `str` | Detailed finding description |
| `location` | `Location \| None` | File path, URL, host:port, or code location if applicable |
| `evidence` | `str \| None` | Raw evidence from tool (sanitized) |
| `remediation` | `str \| None` | Suggested fix or mitigation |
| `references` | `list[str]` | CVE IDs, CWE IDs, tool-specific rule IDs, URLs |
| `confidence` | `float` | 0.0-1.0 confidence score from tool or normalizer |
| `raw_data` | `dict` | Original tool output preserved for audit and deep inspection |

**Normalization enables:**
- Cross-tool finding correlation: the same vulnerability found by Semgrep and CodeQL is linked.
- Severity-based prioritization regardless of source tool.
- Uniform reporting across all integrated tools.
- Agent reasoning over findings without tool-specific knowledge.
- Deduplication of findings when multiple tools report the same issue.

**Normalizer architecture by tool output format:**

| Source Format | Normalization Path | Complexity | Coverage |
|---------------|-------------------|------------|----------|
| SARIF v2.1.0 | Direct parse via sarif-python library | Low | CodeQL, Semgrep, Nuclei, Trivy, Checkmarx, Burp DAST |
| JSON (custom) | Tool-specific JSON-to-Finding mapper | Medium | Nmap (via libnmap), ZAP, SonarQube, Snyk, BloodHound |
| XML | ElementTree/lxml parse + mapper | Medium | Nmap (native), Burp Suite Professional, Nikto |
| CycloneDX/SPDX | SBOM-to-Finding mapper (dependency vulnerabilities) | Medium | Trivy (SBOM mode), Snyk SBOM |
| Structured text | Custom parser per tool | High | NetExec, Hashcat (`--status-json` reduces to JSON) |
| Unstructured text | Avoided where possible; regex fallback | Very High | Responder logs (deferred; not recommended for integration) |

### 3. Standalone Capable Design with Three-Level Degradation (AD-010)

**Decision:** All 21 agents function without any external tools. Three-level graceful degradation ensures every capability works at all levels with reduced evidence quality at lower levels.

**Rationale:** This decision follows directly from AD-001 (methodology-first design paradigm), the highest-confidence finding in Phase 1 research. Agents are defined by knowledge domains, not tool operation. D-002 (LLM capability boundaries) confirms that LLMs reliably perform methodology guidance, code pattern detection, threat modeling, and report generation without tools. R-012 mandates this explicitly: "Skills MUST be fully capable without external tools -- tools augment, not enable."

**Degradation Levels:**

| Level | Name | Tool Access | Evidence Quality | Agent Behavior |
|-------|------|-------------|-----------------|----------------|
| 0 | Full Access | All configured tools available | Tool-validated | Agent orchestrates tools, cross-correlates findings, provides evidence-backed analysis. Findings carry `evidence_level: tool-validated`. |
| 1 | Partial Access | Some tools available, gaps present | Mixed | Agent uses available tools, notes coverage gaps with explicit uncertainty markers. Findings from available tools carry `evidence_level: tool-validated`; gap areas carry `evidence_level: partial-coverage` with list of unavailable tools. |
| 2 | Standalone | No tools available | LLM-only | Agent performs analysis using LLM knowledge base. All findings carry `evidence_level: unvalidated` and include manual verification guidance. Reports include "Unvalidated Assessment" header and recommended manual verification steps. |

**Per-capability degradation mapping:**

| Agent Capability | Level 0 (Full Tools) | Level 1 (Partial) | Level 2 (Standalone) |
|-----------------|----------------------|-------------------|---------------------|
| Threat modeling | LLM reasoning + Nmap/BloodHound recon data | LLM reasoning + available scan data + gap notes | LLM reasoning over scope description with "unvalidated" markers |
| Vulnerability assessment | Semgrep/CodeQL/Nuclei scan results + LLM analysis | Available tool results + LLM pattern analysis for gaps | Pattern-based analysis from LLM training data with "unvalidated" markers |
| Risk prioritization | Real-time CVSS data + exploit availability + tool correlation | Available data + LLM estimation for gaps | CVSS-based reasoning from LLM knowledge with uncertainty bands |
| Remediation advice | Tool-specific fix suggestions (Semgrep autofix) + LLM guidance | Available tool fixes + LLM guidance for gaps | Best-practice recommendations from LLM knowledge |
| Report generation | Report enriched with concrete tool evidence | Report with partial evidence + documented gaps | Structured report from LLM analysis with verification checklist |
| Attack path analysis | BloodHound graph data + Nmap topology + validation | Available graph/scan data + theoretical modeling for gaps | Theoretical path modeling from scope description |

**Implementation pattern:**

```python
class CyberOpsAdapter:
    """Adapter that reports availability and returns structured results."""

    def execute(self, params: ToolParams) -> StructuredResult:
        if not self.is_available():
            return StructuredResult(
                status="unavailable",
                evidence_level="none",
                message=f"{self.tool_name} not found or not reachable",
                findings=[],
                verification_guidance=self.manual_verification_steps(params)
            )
        # ... execute tool and return normalized findings
```

```python
class AgentAnalysis:
    """Agent that operates standalone and enriches with tools when available."""

    def analyze(self, scope: Scope) -> Analysis:
        # Step 1: LLM-based analysis (always available)
        analysis = self.reason_about_scope(scope)
        analysis.evidence_level = "unvalidated"

        # Step 2: Tool augmentation (when available)
        for adapter in self.configured_adapters():
            result = adapter.execute(self.build_params(scope))
            if result.status == "success":
                analysis.enrich(result.findings)
                analysis.evidence_level = "tool-validated"
            elif result.status == "unavailable":
                analysis.add_gap(adapter.tool_name, result.verification_guidance)
                if analysis.evidence_level != "tool-validated":
                    analysis.evidence_level = "partial-coverage"

        return analysis
```

### 4. Security Controls at the Adapter Layer

**Decision:** Enforce security controls at the adapter layer, not the agent layer. Agents never interact directly with tools or credentials.

**Rationale:** Security tools can cause real damage -- active scanning can disrupt services, exploitation can compromise systems, and credential exposure can cascade. The documented MCP attack vectors (prompt injection via tool output, tool poisoning, credential theft) require that security controls be enforced architecturally at a layer agents cannot bypass. C-003 research identified these controls as non-negotiable. AD-004 (three-layer authorization) mandates that the Tool Proxy validates scope before every tool execution for /red-team operations.

**Control Matrix:**

| Control | Implementation | Rationale |
|---------|---------------|-----------|
| **Command allowlists** | CLI adapters maintain explicit allowlists of permitted command arguments. No argument passes to subprocess without allowlist validation. `shell=True` is forbidden in all subprocess calls. | Prevents command injection via manipulated parameters. |
| **Subprocess sandboxing** | Fresh sandbox per tool invocation. Each subprocess runs with explicit timeout, output size limits, and resource constraints. No persistent state between invocations. | Prevents tool output from contaminating agent state across invocations. |
| **Credential broker pattern** | Agents never see raw credentials. Adapters retrieve credentials from a secure store at execution time. Credentials are scoped to minimum required permissions and are time-limited where supported. Credential configuration lives in `.claude/settings.local.json` (gitignored). | Eliminates credential exposure in agent context window. Limits blast radius of credential compromise. |
| **Output schema validation** | All JSON, SARIF, and XML outputs are schema-validated before agent consumption. Validated outputs are normalized to the Finding schema. Validation failures logged and output rejected. | Prevents prompt injection via tool output, which is a documented MCP attack vector (Red Hat 2026, Pillar Security 2025, Practical DevSecOps 2026). |
| **Output size limits** | Adapter enforces maximum output size (configurable per tool). Outputs exceeding the limit are truncated with a truncation marker and the full output preserved to audit log. | Prevents context window exhaustion from verbose tool output. |
| **Scope-validating proxy** | For /red-team: all tool invocations pass through the Tool Proxy before execution. The proxy validates target parameters and ATT&CK technique IDs against the signed engagement scope document. Unauthorized targets or techniques are rejected at the proxy layer with default-deny. The adapter interface supports scope validation as transparent middleware. | Implements AD-004 Layer 2 (dynamic authorization). Makes out-of-scope actions structurally impossible, not procedurally prevented. |
| **TLS-only for remote tools** | API adapters enforce TLS for all remote connections. Certificate validation is mandatory. No plaintext HTTP connections. | Prevents credential interception and man-in-the-middle attacks on tool API communication. |
| **Rate limiting** | API adapters implement rate limiting with exponential backoff. Respects tool API rate limits. | Prevents API abuse and service disruption. |

**Credential broker architecture:**

```
+------------------+     +-------------------+     +------------------+
|                  |     |                   |     |                  |
|   Jerry Agent    |     | Credential Broker |     |  Security Tool   |
|                  |     |                   |     |                  |
|  NO credentials  |---->| Scoped tokens     |---->| Authenticated    |
|  in context      |     | Per-tool secrets  |     | operations       |
|                  |     | Time-limited      |     |                  |
+------------------+     +-------------------+     +------------------+
```

### 5. Adapter Specifications by Tool Category

**Decision:** Define adapter specifications for each tool category with integration tier, output format, and SARIF compatibility.

#### Offensive Tool Adapters

| Tool | Integration Tier | Adapter Type | Output Format | SARIF Compatible | Priority |
|------|-----------------|--------------|---------------|-----------------|----------|
| Nmap | Tier 2 (Structured CLI) | CLI Adapter | XML (via `-oX`), parsed by libnmap | No (custom normalizer: XML -> Finding) | P1 |
| Nuclei | Tier 2 (Structured CLI) | CLI Adapter | JSON, SARIF (native) | Yes (native SARIF output) | P1 |
| Metasploit | Tier 1 (API-Native) | Library Adapter (pymetasploit3) + API Adapter (JSON-RPC) | JSON-RPC responses | No (custom normalizer: JSON-RPC -> Finding) | P2 |
| BloodHound CE | Tier 1 (API-Native) | API Adapter (REST + Neo4j Cypher) | JSON | No (custom normalizer: graph -> Finding) | P2 |
| Impacket | Tier 3 (Library) | Library Adapter (Python import) | Python objects | No (custom normalizer: objects -> Finding) | P3 |
| NetExec | Tier 2 (Structured CLI) | CLI Adapter | Structured text + SQLite | No (custom normalizer: text/DB -> Finding) | P3 |
| Burp Suite | Tier 1 (API-Native) | API Adapter (REST/GraphQL) | JSON, SARIF (Enterprise) | Partial (Enterprise SARIF; Professional JSON) | P2 |
| Cobalt Strike | Deferred | Not recommended | Aggressor Script | No | Deferred (operational safety) |
| Responder | Deferred | Not recommended | Log files (unstructured) | No | Deferred (low automation surface) |
| Hashcat/JtR | Deferred | Not recommended for direct agent control | Text | No | Deferred (batch processing; use Hashtopolis API if needed) |

#### Defensive Tool Adapters

| Tool | Integration Tier | Adapter Type | Output Format | SARIF Compatible | Priority |
|------|-----------------|--------------|---------------|-----------------|----------|
| Semgrep | Tier 2 + MCP | CLI Adapter + MCP Server (official) | JSON, SARIF (native) | Yes (native SARIF output) | P1 |
| Trivy | Tier 2 (Structured CLI) | CLI Adapter | JSON, SARIF, CycloneDX | Yes (native SARIF output) | P1 |
| Checkov | Tier 2 (Structured CLI) | CLI Adapter | JSON, SARIF | Yes (native SARIF output) | P1 |
| CodeQL | Tier 2 (Structured CLI) | CLI Adapter | SARIF (native) | Yes (gold standard SARIF) | P2 |
| OWASP ZAP | Tier 1 (API-Native) | API Adapter (REST) + CLI Adapter (automation framework) | JSON, XML, Markdown | Partial (via plugins) | P2 |
| SonarQube | Tier 1 (API-Native) | API Adapter (REST + webhooks) | JSON | No (custom normalizer: API -> Finding) | P2 |
| Snyk | Tier 1 + CLI | CLI Adapter + API Adapter | JSON, SARIF, CycloneDX/SPDX | Yes (SARIF via CLI) | P2 |
| Checkmarx One | Tier 1 (API-Native) | API Adapter (REST, OAuth) | JSON, SARIF | Yes (native SARIF) | P3 |
| Nikto | Tier 2 (Structured CLI) | CLI Adapter | JSON, XML | No (custom normalizer) | P3 |
| Dependabot/Renovate | Configuration-driven | Config generation (not runtime adapter) | PR-based | N/A | P3 |

### 6. Tool Orchestration Patterns

**Decision:** Support three tool orchestration patterns at the adapter layer, managed by agent logic through the common interface.

**Pattern 1: Sequential Chaining**

One tool's normalized output feeds into the next tool's parameters.

```
Nmap (recon) -> Finding[] -> Nuclei (vuln scan on discovered services) -> Finding[] -> Agent (analysis)
```

Use case: /red-team reconnaissance-to-exploitation pipeline. red-recon runs Nmap, findings inform red-vuln's Nuclei scan configuration.

**Pattern 2: Parallel Execution**

Multiple tools run simultaneously on independent inputs. Results are merged and deduplicated.

```
                    -> Semgrep (SAST)     -> Finding[] ->
Agent (planning) -> -> Trivy (containers)  -> Finding[] -> Agent (synthesis + dedup)
                    -> Checkov (IaC)       -> Finding[] ->
```

Use case: /eng-team multi-tool defensive scan. eng-devsecops orchestrates parallel scans across code, containers, and infrastructure-as-code.

**Pattern 3: Conditional Branching**

Agent selects tools based on target characteristics discovered during analysis.

```
Agent -> Initial Analysis ->
    if web_application: ZAP active scan + Semgrep
    if active_directory: BloodHound + NetExec + Impacket
    if source_code: Semgrep + CodeQL
    if containers: Trivy + Checkov
    if network_target: Nmap + Nuclei
```

Use case: Both skills. Agent dynamically selects appropriate tools based on scope and target profile.

### 7. Scope-Validating Proxy Integration

**Decision:** For /red-team operations, all tool invocations pass through the Tool Proxy as transparent middleware in the adapter layer.

**Rationale:** AD-004 (three-layer authorization) mandates that no tool can be invoked outside the engagement scope. The Tool Proxy is a separate trust domain that agents cannot modify or bypass. Integrating scope validation at the adapter layer makes this enforcement transparent to agent logic while being architecturally inescapable.

**Proxy validation flow:**

```
red-exploit Agent
    |
    | execute(nmap_adapter, {target: "10.0.0.1", ports: "1-1000"})
    v
Common Adapter Interface
    |
    | Scope Validation Middleware (transparent)
    v
Tool Proxy (separate trust domain)
    |
    | Check: Is 10.0.0.1 in target allowlist?
    | Check: Is port scanning in technique allowlist?
    | Check: Is current time within engagement window?
    | Check: Is 10.0.0.1 NOT in exclusion list?
    v
    [ALL PASS] -> CLI Adapter -> nmap binary -> results
    [ANY FAIL] -> ScopeViolationError (logged to audit trail)
```

**Key properties:**
- Scope validation is transparent to agent code. Agents call adapters normally; the proxy intercepts.
- /eng-team operations do not require scope proxy (they operate on source code and configurations, not live targets).
- Proxy operates in a separate trust domain with its own process and permissions.
- Default-deny: if the proxy is unavailable, tools are inaccessible and agents degrade to standalone (Level 2).
- Every proxy decision is logged to the tamper-evident audit trail per AD-004 Layer 3.

### 8. Existing Security MCP Servers

**Decision:** Evaluate and leverage existing security MCP servers where they meet quality and security standards, rather than building all adapters from scratch.

| MCP Server | Tools Wrapped | Transport | Assessment |
|------------|--------------|-----------|------------|
| mcp-for-security (cyproxio) | SQLMap, FFUF, Nmap, Masscan | STDIO | Evaluate for Nmap integration at P2 (MCP evaluation phase) |
| pentest-mcp (DMontgomery40) | Nmap, GoBuster, Nikto, JtR, Hashcat | STDIO/HTTP/SSE | Evaluate for multi-tool wrapping pattern |
| pentestMCP (ramkansal) | 20+ tools (Nmap, Nuclei, ZAP, SQLMap, etc.) | STDIO | Broadest tool coverage; evaluate code quality and security |
| hexstrike-ai (0x4m4) | 150+ cybersecurity tools | STDIO | Largest server; evaluate for reference patterns |
| sast-mcp (Sengtocxoen) | Multiple SAST tools | STDIO | Claude Code integration focus; evaluate for /eng-team |
| Semgrep MCP (official) | Semgrep | STDIO | Official from Semgrep team; highest trust for Semgrep integration |

**Evaluation criteria before adoption:**
- Code review for security vulnerabilities (command injection, credential exposure).
- Output format validation (schema adherence, sanitization).
- Maintenance status and community activity.
- License compatibility.
- Alignment with PROJ-010 common adapter interface contract.

### 9. Implementation Priority

| Priority | Component | Effort | Value | Rationale |
|----------|-----------|--------|-------|-----------|
| **P0** | Common Adapter Interface + Finding Schema | Medium | Foundation | All other integration work depends on the interface contract and normalization schema. No tool can be integrated without these. |
| **P0** | Standalone agent logic (no tools) | High | Core functionality | R-012 mandate. Every agent capability must work at Level 2 before any tool integration begins. Tools augment; they do not enable. |
| **P1** | SARIF parser + normalization layer | Medium | Cross-tool correlation | Enables consumption of findings from any SARIF-producing tool through a single parser. Foundation for deduplication and correlation. |
| **P1** | CLI adapters: Nmap, Semgrep, Trivy, Nuclei, Checkov | Medium | Highest-ROI tool coverage | These 5 tools cover reconnaissance (Nmap), SAST (Semgrep), SCA/container/IaC scanning (Trivy), vulnerability scanning (Nuclei), and IaC policy enforcement (Checkov). All are CLI-based with structured output. |
| **P2** | MCP server evaluation (existing servers) | Low | Leverage community work | Evaluate existing security MCP servers against quality criteria. Adopt where suitable; build custom where not. |
| **P2** | API adapters: ZAP, SonarQube, Burp Suite, BloodHound CE | Medium | Platform integration | REST/GraphQL integrations for tools with persistent state and rich API surfaces. |
| **P2** | CLI adapters: CodeQL, Snyk | Medium | Deep analysis coverage | CodeQL provides deep semantic analysis with gold-standard SARIF. Snyk adds SCA and SBOM generation. |
| **P3** | Custom MCP servers for priority tools | High | Native Claude Code integration | Build MCP servers for tools where CLI/API adapters prove insufficient or where MCP provides significant UX advantage. |
| **P3** | Library adapters: Impacket, pymetasploit3 | Medium | Deep protocol access | Python library integration for AD protocol operations and Metasploit framework access. |
| **P3** | Remaining adapters: NetExec, Nikto, Checkmarx | Low-Medium | Extended coverage | Lower-priority tools integrated based on engagement demand. |

---

## Options Considered

### Option 1: MCP-Only Integration

**Description:** Integrate all tools exclusively through the MCP protocol. Build custom MCP servers for tools that lack them.

**Pros:**
- Single integration protocol across all tools.
- Native Claude Code support with structured tool calling.
- Consistent authentication and error handling model.

**Cons:**
- Most current security tools lack MCP servers; building 20+ custom servers is a multi-month effort.
- Blocks all tool integration until MCP servers are built.
- Overkill for tools used infrequently or with simple CLI invocation patterns.

**Why rejected:** The effort to build custom MCP servers for all 24 analyzed tools would delay tool integration by months. CLI adapters provide 80% of the value at 20% of the effort for the initial implementation. MCP servers can be built incrementally as the adapter layer matures.

### Option 2: CLI-Only via Subprocess

**Description:** Integrate all tools via subprocess invocation with output parsing. No MCP, no API clients.

**Pros:**
- Simplest implementation for most tools.
- No external dependencies (MCP runtime, HTTP clients).
- Works with any tool that has a CLI.

**Cons:**
- Cannot leverage native Claude Code MCP integration.
- Missing session management, persistent state, and rich interaction patterns needed for platform tools (SonarQube, Burp Suite, ZAP).
- Output parsing fragility for tools with unstable CLI output formats.
- No structured tool calling; parameter validation is adapter-side only.

**Why rejected:** CLI-only cannot handle platform tools (SonarQube, Burp Suite, BloodHound CE) that require session management, authentication flows, and stateful interaction. It also forgoes the native MCP integration that Claude Code provides.

### Option 3: API-Only via HTTP Clients

**Description:** Integrate all tools via their REST/GraphQL/RPC APIs. Wrap CLI tools in local API servers.

**Pros:**
- Rich interaction patterns with session management.
- Structured JSON responses from all tools.
- Supports authentication and rate limiting natively.

**Cons:**
- Many security tools (Nmap, Nuclei, Checkov, Hashcat) have no API -- wrapping them in local API servers adds complexity for no benefit over direct subprocess.
- Requires running API servers for CLI tools, adding infrastructure overhead.
- Does not leverage MCP's structured tool calling.

**Why rejected:** Wrapping CLI tools in local API servers adds unnecessary complexity. The protocol should match the tool's native interface, not force all tools through a single protocol.

### Option 4: Protocol Hierarchy -- MCP Primary, CLI/API/Library Fallback (CHOSEN)

**Description:** Adopt a protocol hierarchy where MCP is the primary integration protocol, CLI adapters handle tools without MCP servers, API adapters handle platform tools, and library adapters handle tools with Python SDKs. All behind a common adapter interface that abstracts protocol details from agents.

**Pros:**
- Matches each tool to its natural integration protocol, minimizing impedance mismatch.
- Common adapter interface provides agent-level uniformity regardless of underlying protocol.
- MCP-first strategy leverages Claude Code's native capabilities and the growing MCP ecosystem.
- CLI adapters provide fast, low-effort integration for the majority of current security tools.
- API adapters provide rich interaction for platform tools that need session management.
- Library adapters provide direct protocol access for tools with Python SDKs.
- Tool substitution requires zero agent code changes.
- Incremental MCP migration: tools can start as CLI adapters and be upgraded to MCP as servers become available.

**Cons:**
- Four adapter types to maintain increases the adapter layer's surface area.
- Developers must understand which protocol tier to use for new tools.
- Testing matrix is larger (each adapter type needs its own test patterns).

**Why chosen:** This option provides the best balance of pragmatism and architecture. It enables immediate tool integration via CLI adapters (P1) while establishing the path to MCP-native integration (P2/P3). The common adapter interface ensures that the choice of protocol is an adapter-layer concern that agents never need to know about. The protocol hierarchy matches the empirical reality of the security tool ecosystem: most tools are CLI-based today, some expose APIs, and MCP servers are emerging rapidly but are not yet universal.

---

## Consequences

### Positive

1. **R-012 compliance.** The architecture directly satisfies R-012's requirements: pluggable adapters (common interface), standalone capability (three-level degradation), and tool augmentation without dependency. Every agent capability works at Level 2 (standalone) before any tool integration is implemented.

2. **Cross-tool finding correlation.** The SARIF-based normalization layer (AD-006) enables findings from different tools to be correlated, deduplicated, and prioritized using a single schema. A vulnerability found by both Semgrep and CodeQL is linked rather than reported twice. Severity-based prioritization works regardless of source tool.

3. **Tool substitution without agent changes.** The common adapter interface means that replacing Semgrep with a different SAST tool requires only a new adapter implementation, not changes to any agent that consumes SAST findings. This protects against tool vendor lock-in and accommodates organizational tool preferences per R-011.

4. **Architectural scope enforcement.** The scope-validating proxy integration (Section 7) makes out-of-scope tool invocation structurally impossible for /red-team operations. This implements AD-004 Layer 2 (dynamic authorization) at the adapter layer, where it cannot be bypassed by agent logic.

5. **Fast initial tool coverage.** The P1 priority (Nmap, Semgrep, Trivy, Nuclei, Checkov) provides coverage across reconnaissance, SAST, SCA, container scanning, vulnerability scanning, and IaC policy enforcement using CLI adapters that are straightforward to implement. These five tools cover the highest-ROI integration targets identified in C-001 and C-002.

6. **Security-by-architecture.** Security controls (command allowlists, subprocess sandboxing, credential broker, output validation, size limits) are enforced at the adapter layer, not the agent layer. Agents cannot bypass these controls because they never interact with tools directly.

7. **Incremental MCP migration.** Tools start as CLI adapters and can be upgraded to MCP servers without agent changes. This avoids blocking integration on MCP server availability while establishing the path toward native Claude Code integration.

8. **Bidirectional tool integration.** For tools with LLM-writable rule formats (Semgrep YAML rules, Checkov YAML policies, Nuclei YAML templates), agents can both consume findings and generate custom rules. This is a unique advantage of the YAML-first tools identified in C-002.

### Negative

1. **Four adapter types increase maintenance surface.** The protocol hierarchy requires maintaining four adapter base classes (MCP, CLI, API, Library) with distinct implementation patterns, error handling, and test strategies. Each new tool requires selecting the appropriate tier and implementing the tier-specific adapter logic.
   - **Mitigation:** The common adapter interface and Finding schema are shared across all tiers, limiting the divergence to protocol-specific concerns (subprocess management, HTTP client, MCP protocol, Python import). The adapter base classes encapsulate these concerns, and new tool adapters are relatively thin.
   - **Impact estimate:** LOW. The four adapter types are well-defined by the tool ecosystem's natural integration patterns. The alternative (forcing all tools through one protocol) would create more maintenance burden through impedance mismatch.

2. **SARIF normalization adds a processing layer.** Every tool output passes through normalization before agent consumption. This adds latency and creates a potential information loss point where tool-specific details that do not map to the 12-field Finding schema are relegated to `raw_data`.
   - **Mitigation:** The `raw_data` field preserves the complete original output for deep inspection. Normalization latency is negligible compared to tool execution time (seconds for SARIF parsing vs. minutes for Nmap/Nuclei scans).
   - **Impact estimate:** LOW. SARIF parsing is a well-understood problem with mature libraries (sarif-python, sarif-tools). The normalization step is computationally trivial.

3. **Existing MCP servers may not meet security standards.** Community-built MCP servers for security tools may contain command injection vulnerabilities, credential exposure, or inadequate output sanitization. Adopting them without review creates supply chain risk.
   - **Mitigation:** Evaluation criteria defined in Section 8 require code review, output validation, and license compatibility assessment before adoption. Build custom where community servers fail review.
   - **Impact estimate:** MEDIUM. This is a genuine risk that requires active evaluation effort at P2. The mitigation (code review before adoption) is labor-intensive but necessary.

4. **Standalone mode produces lower-quality output.** Level 2 (standalone) analysis relies on LLM training data, which may be outdated, incomplete, or hallucinated. The "unvalidated" markers communicate this limitation but do not eliminate it.
   - **Mitigation:** This is inherent to AD-001 (methodology-first) and R-012 (standalone capable). The markers ensure that consumers of Level 2 output understand its limitations. The architecture provides the upgrade path: as tools become available, evidence quality improves transparently.
   - **Impact estimate:** LOW. This is a design trade-off, not a defect. The alternative (failing entirely when tools are unavailable) is worse.

5. **Scope proxy adds latency to /red-team tool invocations.** Every /red-team tool call passes through the Tool Proxy for scope validation before execution, adding a validation step to the critical path.
   - **Mitigation:** Scope validation is a fast operation (scope document comparison, not network call). The alternative (no scope enforcement) is not acceptable per AD-004 and R-020.
   - **Impact estimate:** LOW. Scope validation latency is sub-millisecond; tool execution latency is seconds to minutes.

### Neutral (Requires Monitoring)

1. **MCP ecosystem maturity for security tools.** The MCP ecosystem is growing rapidly (13,000+ servers as of late 2025) but security-specific MCP servers are still early-stage. The rate at which high-quality security MCP servers appear will determine the migration pace from CLI to MCP adapters. This should be reassessed at each implementation phase.

2. **SARIF v2.1.0 version stability.** SARIF v2.1.0 is the current OASIS standard. If a v3.0 is released with breaking changes, the normalization layer will need migration. This is a low-probability risk given SARIF's stability, but should be monitored.

3. **Tool output format stability.** CLI adapters depend on stable output formats (`--json`, `--sarif`, `-oX`). Tool version upgrades may change output schemas. Adapter tests should pin to specific tool versions and validate output schema compatibility on upgrade.

4. **Credential broker implementation complexity.** The credential broker pattern is architecturally clean but requires careful implementation to avoid credential leakage through logging, error messages, or subprocess environment variables. Implementation must undergo security review.

---

## Evidence Base

### Stream C Research Findings

Phase 1 research in Stream C (Tool Integration) produced three artifacts with findings that directly inform this ADR:

#### C-001: Offensive Tool Ecosystem (12 tools analyzed)

| Finding | Impact on Architecture |
|---------|------------------------|
| Three integration tiers emerge naturally: API-native, structured CLI, programmatic library | Protocol hierarchy (Section 1) maps directly to these tiers |
| Existing MCP servers validate security tool wrapping pattern | MCP-primary strategy (Section 1) is de-risked by 6 proven implementations |
| Output format standardization is mixed: XML (Nmap), JSON (Nuclei, Metasploit), text (Hashcat, NetExec) | Normalization layer (Section 2) is essential; SARIF alone is insufficient |
| Nmap (CLI + XML) and Nuclei (CLI + JSON/SARIF) are highest-ROI offensive integration targets | P1 priority includes both |
| Cobalt Strike, Responder, and Hashcat are not suitable for direct agent integration | Deferred in adapter specifications (Section 5) |

#### C-002: Defensive Tool Ecosystem (12 tools analyzed)

| Finding | Impact on Architecture |
|---------|------------------------|
| SARIF v2.1.0 has broad native support: CodeQL, Semgrep, Nuclei, Trivy, Checkmarx | SARIF as primary normalization format (Section 2) |
| Two integration patterns: pipeline (CLI) and platform (API) | Protocol hierarchy covers both patterns |
| YAML rule authoring (Semgrep, Checkov, Nuclei) is LLM-friendly | Bidirectional integration noted in Consequences |
| Semgrep MCP server (official) exists | Semgrep is P1 with both CLI and MCP adapter paths |
| Webhook patterns (SonarQube, Snyk) enable event-driven integration | API adapter design supports webhook listeners |

#### C-003: Agentic Tool Integration Patterns

| Finding | Impact on Architecture |
|---------|------------------------|
| MCP: 97M+ monthly SDK downloads, 13,000+ servers, backed by Anthropic/OpenAI/Google/Microsoft | MCP as primary protocol (Section 1) |
| Common adapter interface: `execute(params) -> StructuredResult \| ToolUnavailableError` | Common interface design (Section 1) |
| Standalone capable design is an established pattern (Toolformer, CoT + Tools, fallback strategies) | Three-level degradation (Section 3) |
| Sandboxing is mandatory: command allowlists, no shell=True, credential scoping, output validation | Security controls (Section 4) |
| MCP attack vectors: prompt injection via tool output, tool poisoning | Output schema validation requirement (Section 4) |
| FastMCP 3.0 (January 2026) recommended for custom MCP server building | Custom MCP servers at P3 |

### Synthesis Findings (S-002)

| Finding | Impact on Architecture |
|---------|------------------------|
| Convergence 5: JSON Schema + SARIF + YAML as universal data interchange layer | Three-format architecture adopted (JSON Schema for tool definitions, SARIF for findings, YAML for configuration) |
| AD-005 HIGH confidence: three independent streams converge on protocol hierarchy | Decision confidence validated |
| AD-006 HIGH confidence: SARIF normalization converges across streams C, E, and F | Decision confidence validated |
| AD-010 HIGH confidence: follows from AD-001 (methodology-first) and D-002 capability analysis | Decision confidence validated |
| Cross-cutting: scope-validating proxy for /red-team tool access | Scope proxy integration (Section 7) |
| Cross-cutting: adapter interface supports scope validation as transparent middleware | Proxy is middleware, not agent responsibility |

---

## Compliance

### R-012: Tool Integration Architecture

| R-012 Clause | Compliance | Evidence |
|-------------|------------|----------|
| "Both skills MUST define integration points with external tooling frameworks" | COMPLIANT | Adapter specifications (Section 5) define integration for 24 tools across /eng-team and /red-team |
| "Integration MUST be architected as pluggable adapters" | COMPLIANT | Common adapter interface (Section 1) with four adapter types; tool substitution requires zero agent changes |
| "Skills MUST be fully capable without external tools" | COMPLIANT | Standalone capable design (Section 3) with three-level degradation; Level 2 (no tools) provides full capability with "unvalidated" markers |
| "Tools augment, not enable" | COMPLIANT | AD-001 methodology-first paradigm; agents defined by knowledge domains, not tool operation; tools enrich evidence quality but do not enable reasoning |

### R-020: Authorization Verification

| R-020 Clause | Compliance | Evidence |
|-------------|------------|----------|
| "MUST enforce authorization verification before any active testing operation" | COMPLIANT | Scope-validating proxy (Section 7) checks every /red-team tool invocation against engagement scope before execution |
| "Scope MUST be defined and confirmed" | COMPLIANT | Tool Proxy requires valid signed scope document; engagement cannot start without it |
| "Out-of-scope actions MUST be refused" | COMPLIANT | Default-deny at proxy layer; unauthorized targets and techniques are rejected and logged |

### P-003: No Recursive Subagents

All adapter types operate within the orchestrator -> worker pattern. Tool adapters are function calls within agent execution, not nested agent invocations. Tool orchestration patterns (sequential, parallel, conditional) are managed by agent logic through the common interface, not by spawning sub-agents.

### P-020: User Authority

This ADR is a recommendation, not a final decision. Per P-020, the user retains authority to:
- Override any adapter specification or priority ordering.
- Direct inclusion of deferred tools or exclusion of prioritized tools.
- Modify the protocol hierarchy or security control requirements.
- Accept, reject, or request revision of this ADR.

---

## Related Decisions

### Upstream (Inputs to This ADR)

| Decision / Artifact | Relationship | Status |
|---------------------|-------------|--------|
| **AD-001** (Methodology-First Design) | Foundational constraint: agents defined by knowledge domains, not tool operation. AD-010 (standalone capable) follows directly. | HIGH confidence (S-002) |
| **AD-004** (Three-Layer Authorization) | Mandates scope-validating Tool Proxy for /red-team operations. Section 7 implements AD-004 Layer 2 at the adapter layer. | HIGH confidence (S-002) |
| **C-001** (Offensive Tool Ecosystem Survey) | Per-tool API details, integration tiers, and output formats for 12 offensive tools. | Complete |
| **C-002** (Defensive Tool Ecosystem Survey) | Per-tool API details, SARIF adoption analysis, and YAML rule authoring patterns for 12 defensive tools. | Complete |
| **C-003** (Agentic Integration Patterns) | MCP adoption data, three adapter patterns, standalone capable design, security controls, existing MCP servers. | Complete |
| **S-002** (Architecture Implications Synthesis) | AD-005, AD-006, AD-010 decision details; cross-cutting concerns; data interchange formats. | Complete |
| **R-012** (PLAN.md) | Requirement: pluggable adapters, standalone capable, tools augment not enable. | Baselined |
| **R-020** (PLAN.md) | Requirement: authorization verification before active testing. | Baselined |

### Downstream (Decisions Informed by This ADR)

| Decision / Feature | Relationship | Status |
|--------------------|-------------|--------|
| **FEAT-010** (Agent Team Architecture) | Agent-to-tool mapping uses adapter specifications from Section 5. Each agent's `capabilities.allowed_tools` references adapters defined here. Standalone capability (Section 3) constrains all agent definitions. | Planned |
| **FEAT-011** (Skill Routing & Invocation) | Tool orchestration patterns (Section 6) inform routing logic for multi-tool workflows. | Planned |
| **FEAT-013** (Configurable Rule Set Architecture) | Rule sets govern tool selection per engagement profile per R-011. Adapter specifications define which tools are configurable. | Planned |
| **FEAT-015** (Authorization & Scope Control) | Scope-validating proxy integration (Section 7) is the tool-layer implementation of AD-004. FEAT-015 defines the scope document format and oracle behavior that the proxy consumes. | Planned |
| **EPIC-003** (Engineering Team Build) | /eng-team agents use defensive tool adapters (Semgrep, Trivy, CodeQL, etc.) through the common interface. | Planned |
| **EPIC-004** (Red Team Build) | /red-team agents use offensive tool adapters (Nmap, Nuclei, Metasploit, etc.) through the common interface with scope proxy. | Planned |

---

## Limitations and Epistemic Status

**This ADR is an AI-generated architecture decision recommendation.** All evidence, analysis, and architectural evaluation cited in this document were produced by AI agents during Phase 1 research (ps-researcher, ps-analyst, ps-architect) without human subject matter expert validation. The following epistemic boundaries apply:

### What This ADR Can Claim

1. **Research grounding.** The architecture decisions are grounded in Phase 1 research across 6 streams and 20 artifacts. The MCP adoption data (97M+ SDK downloads, 13,000+ servers) is sourced from dated industry reports. The tool ecosystem surveys (C-001, C-002) are based on official documentation and dated source citations. The security MCP server implementations are verifiable on GitHub.

2. **Cross-stream convergence.** All three decisions (AD-005, AD-006, AD-010) achieved HIGH confidence through independent convergence across multiple research streams. AD-005 was validated by streams C and E. AD-006 was validated by streams C, E, and F. AD-010 was validated by streams C and D and follows logically from AD-001.

3. **Pattern validity.** The adapter patterns (MCP server, CLI adapter, API adapter, library adapter) are established software architecture patterns. The SARIF standard is an OASIS specification with documented tool support. The common interface pattern is standard in all analyzed agentic frameworks (LangChain, CrewAI, AutoGen).

### What This ADR Cannot Claim

1. **Implementation feasibility validation.** No prototype adapter has been built. The effort estimates (Medium, High) are architectural assessments, not implementation measurements. Actual effort will be determined during Phase 3 implementation.

2. **Tool output stability guarantees.** CLI adapter designs assume stable output formats (`--json`, `--sarif`, `-oX`). Tool version upgrades may break output parsers. This risk is mitigated by version pinning and schema validation in adapter tests but cannot be eliminated.

3. **Security control sufficiency.** The security controls (command allowlists, sandboxing, credential broker, output validation) are architecturally sound but have not been penetration tested. The adequacy of these controls against real attack vectors will only be validated during Phase 5 purple team exercises.

4. **MCP ecosystem projection accuracy.** The MCP ecosystem is growing rapidly. The projection that MCP servers will become available for more security tools is reasonable but not guaranteed. The architecture's CLI-first fallback strategy mitigates this uncertainty.

5. **Performance characteristics.** The three-level degradation model, SARIF normalization overhead, and scope proxy latency have not been benchmarked. Performance validation is a Phase 3 implementation concern.

### Structural Limitation: AI Assessment of AI Tool Integration

This ADR describes an architecture for AI agents to use security tools. The architecture was designed by AI agents (ps-architect) analyzing research produced by AI agents (ps-researcher, ps-analyst). The resulting system will be used by AI agents in production. This creates a self-referential assessment structure where the designer, the evaluator, and the consumer share the same model's capabilities and blind spots. User review and ratification (P-020) is the primary mitigation for this structural limitation.

---

## References

### Phase 1 Research Artifacts

| # | Citation | Role in This ADR |
|---|----------|-----------------|
| 1 | C-001: Offensive Tool Ecosystem Survey | Per-tool integration tiers, API surfaces, output formats, agentic feasibility for 12 offensive tools |
| 2 | C-002: Defensive Tool Ecosystem Survey | Per-tool integration details, SARIF adoption analysis, YAML rule authoring patterns for 12 defensive tools |
| 3 | C-003: Agentic Tool Integration Patterns | MCP adoption data, adapter pattern designs, standalone capable pattern, security controls, existing MCP servers |
| 4 | S-002: Architecture Implications Synthesis | AD-005, AD-006, AD-010 decision formalization; cross-cutting concerns; data interchange formats |

### External Standards and Specifications

| # | Citation | Relevance |
|---|----------|-----------|
| 5 | [SARIF v2.1.0 (OASIS)](https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html) | Primary finding normalization format; AD-006 foundation |
| 6 | [MCP Specification 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25) | Primary integration protocol specification |
| 7 | [MCP Enterprise Adoption Guide](https://guptadeepak.com/the-complete-guide-to-model-context-protocol-mcp-enterprise-adoption-market-trends-and-implementation-strategies/) | 97M+ SDK downloads, 13K+ servers adoption data |
| 8 | [SARIF Guide (Sonar)](https://www.sonarsource.com/resources/library/sarif/) | SARIF adoption and tooling landscape |

### Security and Sandboxing

| # | Citation | Relevance |
|---|----------|-----------|
| 9 | [MCP Security Risks (Red Hat)](https://www.redhat.com/en/blog/model-context-protocol-mcp-understanding-security-risks-and-controls) | MCP risk analysis informing security controls |
| 10 | [MCP Security Vulnerabilities 2026 (Practical DevSecOps)](https://www.practical-devsecops.com/mcp-security-vulnerabilities/) | Prompt injection and tool poisoning attack vectors |
| 11 | [MCP Security Risks (Pillar Security)](https://www.pillar.security/blog/the-security-risks-of-model-context-protocol-mcp) | Comprehensive MCP risk assessment |
| 12 | [NVIDIA Sandboxing Guidance](https://developer.nvidia.com/blog/practical-security-guidance-for-sandboxing-agentic-workflows-and-managing-execution-risk) | Practical agent sandboxing patterns |
| 13 | [Claude Code Sandboxing (Anthropic)](https://www.anthropic.com/engineering/claude-code-sandboxing) | Credential isolation patterns |
| 14 | [How to Sandbox AI Agents 2026 (Northflank)](https://northflank.com/blog/how-to-sandbox-ai-agents) | MicroVM and gVisor sandboxing strategies |

### MCP Server Building and Tools

| # | Citation | Relevance |
|---|----------|-----------|
| 15 | [FastMCP Tutorial (Firecrawl)](https://www.firecrawl.dev/blog/fastmcp-tutorial-building-mcp-servers-python) | FastMCP 3.0 for custom MCP server building |
| 16 | [mcp-for-security (GitHub)](https://github.com/cyproxio/mcp-for-security) | Existing security MCP server: Nmap, SQLMap, FFUF, Masscan |
| 17 | [pentest-mcp (GitHub)](https://github.com/DMontgomery40/pentest-mcp) | Existing security MCP server: pentesting tools |
| 18 | [hexstrike-ai (GitHub)](https://github.com/0x4m4/hexstrike-ai) | Existing security MCP server: 150+ cybersecurity tools |
| 19 | [sast-mcp (GitHub)](https://github.com/Sengtocxoen/sast-mcp) | Existing security MCP server: SAST tools for Claude Code |
| 20 | [MCP-Scan (Invariant Labs)](https://github.com/invariantlabs-ai/mcp-scan) | Security scanning tool for MCP servers |

### Agentic Architecture Patterns

| # | Citation | Relevance |
|---|----------|-----------|
| 21 | [Agentic AI Design Patterns 2025 (Azilen)](https://www.azilen.com/blog/agentic-ai-design-patterns/) | Tool use + fallback patterns informing standalone design |
| 22 | [CLI Patterns for AI Agents (InfoQ)](https://www.infoq.com/articles/ai-agent-cli/) | `--json` flag as API contract pattern |
| 23 | [Agent Design Patterns (Databricks)](https://docs.databricks.com/aws/en/generative-ai/guide/agent-system-design-patterns) | Tool use + fallback design patterns |

### Tool Documentation

| # | Citation | Relevance |
|---|----------|-----------|
| 24 | [Nmap Output Documentation](https://nmap.org/book/man-output.html) | XML output format specification |
| 25 | [libnmap Documentation](https://libnmap.readthedocs.io/en/latest/parser.html) | Python parser for Nmap XML |
| 26 | [Semgrep Rule Syntax](https://semgrep.dev/docs/writing-rules/rule-syntax) | YAML rule structure for LLM generation |
| 27 | [Nuclei Template Documentation](https://docs.projectdiscovery.io/templates/introduction) | YAML template authoring for LLM generation |
| 28 | [Trivy CLI Reference](https://trivy.dev/docs/latest/references/configuration/cli/trivy_kubernetes/) | Multi-target scanning capabilities |
| 29 | [ZAP API Reference](https://www.zaproxy.org/docs/api/) | REST API for DAST integration |
| 30 | [SonarQube Webhooks Documentation](https://docs.sonarsource.com/sonarqube-server/2025.2/project-administration/webhooks/) | Webhook-driven integration pattern |
| 31 | [Checkov YAML Custom Policies](https://www.checkov.io/3.Custom%20Policies/YAML%20Custom%20Policies.html) | LLM-writable policy format |
| 32 | [CodeQL CLI SARIF Output](https://docs.github.com/en/code-security/codeql-cli/using-the-advanced-functionality-of-the-codeql-cli/sarif-output) | Gold-standard SARIF generation |
| 33 | [pymetasploit3 (GitHub)](https://github.com/DanMcInerney/pymetasploit3) | Python automation library for Metasploit |
| 34 | [BloodHound CE (GitHub)](https://github.com/SpecterOps/BloodHound) | REST API and graph database for attack path analysis |

### Jerry Framework Sources

| # | Citation | Relevance |
|---|----------|-----------|
| 35 | PLAN.md R-012 | Tool Integration Architecture requirement |
| 36 | PLAN.md R-020 | Authorization verification requirement |
| 37 | PLAN.md R-011 | Configurable rule sets requirement |
| 38 | S-002 AD-001 | Methodology-first design paradigm |
| 39 | S-002 AD-004 | Three-layer authorization architecture |
| 40 | S-002 Convergence 5 | JSON Schema + SARIF + YAML data interchange convergence |
