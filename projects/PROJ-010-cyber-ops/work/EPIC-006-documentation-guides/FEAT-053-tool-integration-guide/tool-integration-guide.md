# Tool Integration Guide

> Hands-on guide for integrating external security tools with the Jerry Cyber Ops /eng-team and /red-team skills using the adapter architecture.

<!--
DOCUMENT-ID: FEAT-053:tool-integration-guide
AUTHOR: PROJ-010 Phase 6
DATE: 2026-02-22
STATUS: DRAFT
PARENT: FEAT-053 (Tool Integration Guide)
EPIC: EPIC-006 (Documentation & Guides)
PROJECT: PROJ-010-cyber-ops
TYPE: User Guide
SSOT: ADR-PROJ010-005 (Tool Integration Adapter Architecture)
-->

## Document Sections

| Section | Purpose |
|---------|---------|
| [Audience Guide](#audience-guide) | L0/L1/L2 reading paths |
| [Adapter Architecture Overview](#adapter-architecture-overview) | Protocol hierarchy, common interface, and design principles |
| [Supported Tools Reference](#supported-tools-reference) | Per-tool integration details for offensive and defensive tools |
| [Custom Adapter Creation Guide](#custom-adapter-creation-guide) | Step-by-step guide for building CLI, API, MCP, and Library adapters |
| [Tool Integration Testing Guide](#tool-integration-testing-guide) | Testing strategies for adapter reliability and security |
| [Examples](#examples) | Metasploit, Burp Suite, and Semgrep integration scenarios |
| [Security Controls](#security-controls) | Sandboxing, credential management, and output validation |
| [Troubleshooting](#troubleshooting) | Common integration issues and resolution |
| [References](#references) | SSOT and source document traceability |

---

## Audience Guide

| Level | Audience | Sections to Focus On |
|-------|----------|---------------------|
| **L0 (Stakeholder)** | Project managers, engagement leads | [Adapter Architecture Overview](#adapter-architecture-overview), [Supported Tools Reference](#supported-tools-reference) |
| **L1 (Practitioner)** | Security engineers integrating tools | [Supported Tools Reference](#supported-tools-reference), [Custom Adapter Creation Guide](#custom-adapter-creation-guide), [Examples](#examples) |
| **L2 (Architect)** | Framework designers, adapter developers | All sections, especially [Custom Adapter Creation Guide](#custom-adapter-creation-guide), [Security Controls](#security-controls), [Tool Integration Testing Guide](#tool-integration-testing-guide) |

---

## Adapter Architecture Overview

The tool integration adapter architecture follows an MCP-primary design with CLI, API, and Library fallbacks. All adapter types implement a common interface that abstracts protocol-specific details from agent logic. Tools augment agent capability -- they do not enable it. Every agent functions fully at standalone level (Level 2) without any tools.

**SSOT:** ADR-PROJ010-005 (Tool Integration Adapter Architecture -- MCP-Primary with Common Interface).

### Protocol Hierarchy

| Priority | Protocol | When to Use | Trade-offs |
|----------|----------|-------------|------------|
| Primary | **MCP Server** | Tool has an MCP server; frequent cross-session use; multiple agents need access | Native Claude Code integration; structured tool calling; requires MCP server |
| Fallback 1 | **CLI Adapter** | CLI-based tool with structured output; no MCP server; lightweight use | Simple implementation; no daemon needed; subprocess overhead |
| Fallback 2 | **API Adapter** | REST/GraphQL/RPC API; persistent state or session management needed | Rich interaction; session management; requires running service |
| Fallback 3 | **Library Adapter** | Python library for direct integration (e.g., Impacket, pymetasploit3) | Zero parsing overhead; tighter coupling to internals |

### Architecture Diagram

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

### Common Adapter Interface

All adapter types implement this interface:

```python
from cyberops.adapters import ToolParams, StructuredResult

class CyberOpsAdapter:
    """Base interface for all tool adapters."""

    def execute(self, params: ToolParams) -> StructuredResult:
        """Execute tool operation and return structured result."""
        ...

    def is_available(self) -> bool:
        """Check whether tool is installed, reachable, and licensed."""
        ...

    def get_capabilities(self) -> list[str]:
        """Return supported operations for agent discovery."""
        ...

    def validate_params(self, params: ToolParams) -> ValidationResult:
        """Validate parameters before execution (pre-flight check)."""
        ...
```

### Design Principles

1. **Agent code calls adapters, never tools directly.** Agent logic operates on normalized findings, never on raw tool output.
2. **Adapter availability is checked at execution time, not design time.** Tool substitution requires zero agent code changes.
3. **Each adapter handles authentication, timeout, error recovery, and output parsing internally.**
4. **All tool outputs are normalized to the common Finding schema before agent consumption.**
5. **Standalone capability is mandatory.** Every agent works without tools (Level 2). Tools enrich evidence quality but do not enable reasoning.

### Three-Level Degradation Model

| Level | Name | Tool Access | Evidence Quality | Agent Behavior |
|-------|------|-------------|-----------------|----------------|
| 0 | Full Access | All tools available | Tool-validated | Agent orchestrates tools, cross-correlates findings. Findings carry `evidence_level: tool-validated`. |
| 1 | Partial Access | Some tools available | Mixed | Agent uses available tools, notes gaps. Gap areas carry `evidence_level: partial-coverage`. |
| 2 | Standalone | No tools available | LLM-only | Agent performs analysis from methodology knowledge. All findings carry `evidence_level: unvalidated`. |

### SARIF-Based Finding Normalization

All tool outputs are normalized to a 12-field common Finding schema before agent consumption. SARIF v2.1.0 (OASIS standard) is the primary normalization format.

| Field | Type | Description |
|-------|------|-------------|
| `id` | `str` | Unique finding identifier (tool-scoped) |
| `source_tool` | `str` | Tool that produced the finding |
| `severity` | `enum` | CRITICAL, HIGH, MEDIUM, LOW, INFO |
| `category` | `enum` | VULNERABILITY, MISCONFIGURATION, SECRET, COMPLIANCE, etc. |
| `title` | `str` | Human-readable finding title |
| `description` | `str` | Detailed finding description |
| `location` | `Location | None` | File path, URL, host:port, or code location |
| `evidence` | `str | None` | Raw evidence from tool (sanitized) |
| `remediation` | `str | None` | Suggested fix or mitigation |
| `references` | `list[str]` | CVE IDs, CWE IDs, tool-specific rule IDs |
| `confidence` | `float` | 0.0-1.0 confidence score |
| `raw_data` | `dict` | Original tool output preserved for audit |

**Normalization paths by output format:**

| Source Format | Normalization | Complexity | Example Tools |
|---------------|--------------|------------|---------------|
| SARIF v2.1.0 | Direct parse | Low | CodeQL, Semgrep, Nuclei, Trivy, Checkmarx |
| JSON (custom) | Tool-specific mapper | Medium | Nmap (libnmap), ZAP, SonarQube, Snyk, BloodHound |
| XML | ElementTree/lxml parse | Medium | Nmap (native), Burp Suite Professional |
| CycloneDX/SPDX | SBOM-to-Finding mapper | Medium | Trivy (SBOM mode), Snyk SBOM |
| Structured text | Custom parser | High | NetExec, Hashcat |

---

## Supported Tools Reference

### Offensive Tools

| Tool | Adapter Type | Output Format | SARIF | Priority | Primary Agents |
|------|-------------|---------------|-------|----------|----------------|
| **Nmap** | CLI Adapter | XML (via `-oX`) | No (custom normalizer) | P1 | red-recon |
| **Nuclei** | CLI Adapter | JSON, SARIF (native) | Yes | P1 | red-vuln, red-exploit |
| **Metasploit** | Library (pymetasploit3) + API (JSON-RPC) | JSON-RPC responses | No (custom normalizer) | P2 | red-exploit |
| **BloodHound CE** | API Adapter (REST + Neo4j) | JSON | No (custom normalizer) | P2 | red-recon, red-lateral |
| **Burp Suite** | API Adapter (REST/GraphQL) | JSON, SARIF (Enterprise) | Partial | P2 | red-exploit, red-vuln |
| **Impacket** | Library Adapter | Python objects | No (custom normalizer) | P3 | red-exploit, red-privesc, red-lateral |
| **NetExec** | CLI Adapter | Structured text + SQLite | No (custom normalizer) | P3 | red-lateral, red-privesc |

**Deferred tools (not recommended for initial integration):**
- **Cobalt Strike** -- Proprietary, operational safety concerns
- **Responder** -- Passive tool, unstructured log output
- **Hashcat/JtR** -- Long-running batch processing

### Defensive Tools

| Tool | Adapter Type | Output Format | SARIF | Priority | Primary Agents |
|------|-------------|---------------|-------|----------|----------------|
| **Semgrep** | CLI + MCP Server (official) | JSON, SARIF (native) | Yes | P1 | eng-devsecops, eng-security |
| **Trivy** | CLI Adapter | JSON, SARIF, CycloneDX | Yes | P1 | eng-devsecops, eng-infra |
| **Checkov** | CLI Adapter | JSON, SARIF | Yes | P1 | eng-devsecops, eng-infra |
| **Nuclei** | CLI Adapter | JSON, SARIF (native) | Yes | P1 | eng-devsecops |
| **CodeQL** | CLI Adapter | SARIF (native) | Yes (gold standard) | P2 | eng-devsecops, eng-security |
| **OWASP ZAP** | API Adapter (REST) + CLI | JSON, XML, Markdown | Partial (via plugins) | P2 | eng-devsecops |
| **SonarQube** | API Adapter (REST + webhooks) | JSON | No (custom normalizer) | P2 | eng-devsecops |
| **Snyk** | CLI + API Adapter | JSON, SARIF, CycloneDX | Yes (via CLI) | P2 | eng-devsecops |
| **Checkmarx One** | API Adapter (REST, OAuth) | JSON, SARIF | Yes | P3 | eng-security |
| **Nikto** | CLI Adapter | JSON, XML | No (custom normalizer) | P3 | eng-devsecops |

### Tool Orchestration Patterns

Three orchestration patterns are supported at the adapter layer:

**Pattern 1: Sequential Chaining** -- One tool's output feeds the next.

```
Nmap (recon) -> Finding[] -> Nuclei (vuln scan on discovered services) -> Finding[] -> Agent
```

Use case: red-recon runs Nmap; findings inform red-vuln's Nuclei scan targets.

**Pattern 2: Parallel Execution** -- Multiple tools run simultaneously on independent inputs.

```
                    -> Semgrep (SAST)     -> Finding[] ->
Agent (planning) -> -> Trivy (containers)  -> Finding[] -> Agent (synthesis + dedup)
                    -> Checkov (IaC)       -> Finding[] ->
```

Use case: eng-devsecops orchestrates parallel scans across code, containers, and IaC.

**Pattern 3: Conditional Branching** -- Agent selects tools based on target characteristics.

```
Agent -> Initial Analysis ->
    if web_application: ZAP active scan + Semgrep
    if active_directory: BloodHound + NetExec + Impacket
    if source_code: Semgrep + CodeQL
    if containers: Trivy + Checkov
    if network_target: Nmap + Nuclei
```

---

## Custom Adapter Creation Guide

### Creating a CLI Adapter

CLI adapters wrap command-line tools that produce structured output (JSON, XML, SARIF). This is the most common adapter type for security tools.

**Step 1: Create the adapter class.**

```python
# cyberops/adapters/cli/nmap_adapter.py
import shutil
import subprocess
from cyberops.adapters.base import CyberOpsAdapter, ToolParams, StructuredResult
from cyberops.adapters.normalizers import NmapNormalizer

class NmapAdapter(CyberOpsAdapter):
    """CLI adapter for Nmap network scanner."""

    tool_name = "nmap"
    adapter_type = "cli"
    default_timeout = 300  # 5 minutes

    # Command allowlist -- ONLY these flags are permitted
    ALLOWED_FLAGS = {
        "-sS", "-sT", "-sU", "-sV", "-sC", "-O",
        "-p", "-Pn", "--open", "-oX", "-oN",
        "--top-ports", "--min-rate", "--max-rate",
        "-T0", "-T1", "-T2", "-T3", "-T4",
        "-A", "--script", "-n", "-v",
    }

    def is_available(self) -> bool:
        """Check if nmap binary is in PATH."""
        return shutil.which("nmap") is not None

    def get_capabilities(self) -> list[str]:
        """Return supported operations."""
        return [
            "port_scan",
            "service_detection",
            "os_fingerprint",
            "script_scan",
            "vulnerability_scan",
        ]

    def validate_params(self, params: ToolParams) -> ValidationResult:
        """Validate scan parameters before execution."""
        # Verify all flags are in the allowlist
        for flag in params.flags:
            base_flag = flag.split("=")[0] if "=" in flag else flag
            if base_flag not in self.ALLOWED_FLAGS:
                return ValidationResult(
                    valid=False,
                    error=f"Flag '{base_flag}' not in command allowlist"
                )
        # Verify target is in scope (for /red-team)
        if params.scope_validation_required:
            if not self.scope_oracle.validate_target(params.target):
                return ValidationResult(
                    valid=False,
                    error=f"Target '{params.target}' is outside authorized scope"
                )
        return ValidationResult(valid=True)

    def execute(self, params: ToolParams) -> StructuredResult:
        """Execute nmap scan and return normalized findings."""
        if not self.is_available():
            return StructuredResult(
                status="unavailable",
                evidence_level="none",
                message="nmap not found in PATH",
                findings=[],
                verification_guidance=[
                    "Install nmap: https://nmap.org/download.html",
                    "Verify installation: nmap --version",
                ]
            )

        validation = self.validate_params(params)
        if not validation.valid:
            return StructuredResult(
                status="validation_error",
                evidence_level="none",
                message=validation.error,
                findings=[],
            )

        # Build command with XML output
        cmd = self._build_command(params)

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                timeout=params.timeout or self.default_timeout,
                text=True,
                shell=False,  # NEVER use shell=True
            )

            if result.returncode != 0:
                return StructuredResult(
                    status="tool_error",
                    evidence_level="none",
                    message=f"nmap exited with code {result.returncode}: {result.stderr[:500]}",
                    findings=[],
                )

            # Normalize XML output to Finding schema
            findings = NmapNormalizer.normalize(result.stdout)

            return StructuredResult(
                status="success",
                evidence_level="tool-validated",
                message=f"Scan complete: {len(findings)} findings",
                findings=findings,
                raw_output=result.stdout,
            )

        except subprocess.TimeoutExpired:
            return StructuredResult(
                status="timeout",
                evidence_level="none",
                message=f"nmap timed out after {params.timeout or self.default_timeout}s",
                findings=[],
            )

    def _build_command(self, params: ToolParams) -> list[str]:
        """Build nmap command with validated flags."""
        cmd = ["nmap"]
        cmd.extend(params.flags)
        cmd.extend(["-oX", "-"])  # XML output to stdout
        cmd.append(params.target)
        return cmd
```

**Step 2: Create the normalizer.**

```python
# cyberops/adapters/normalizers/nmap_normalizer.py
from libnmap.parser import NmapParser
from cyberops.adapters.schema import Finding, Location, Severity

class NmapNormalizer:
    """Normalize Nmap XML output to the common Finding schema."""

    @staticmethod
    def normalize(xml_output: str) -> list[Finding]:
        """Parse Nmap XML and produce normalized Findings."""
        report = NmapParser.parse_fromstring(xml_output)
        findings = []

        for host in report.hosts:
            for service in host.services:
                if service.state == "open":
                    finding = Finding(
                        id=f"nmap-{host.address}-{service.port}-{service.protocol}",
                        source_tool="nmap",
                        severity=Severity.INFO,
                        category="DISCOVERY",
                        title=f"Open port: {service.port}/{service.protocol} ({service.service})",
                        description=(
                            f"Service {service.service} version {service.banner} "
                            f"detected on {host.address}:{service.port}/{service.protocol}"
                        ),
                        location=Location(
                            host=host.address,
                            port=service.port,
                            protocol=service.protocol,
                        ),
                        evidence=service.banner,
                        remediation=None,
                        references=[],
                        confidence=0.9,
                        raw_data={
                            "host": host.address,
                            "port": service.port,
                            "protocol": service.protocol,
                            "service": service.service,
                            "banner": service.banner,
                            "state": service.state,
                        },
                    )
                    findings.append(finding)

        return findings
```

**Step 3: Register the adapter.**

```yaml
# cyberops/adapters/registry.yaml
adapters:
  nmap:
    class: cyberops.adapters.cli.nmap_adapter.NmapAdapter
    type: cli
    skills: [red-team, eng-team]
    agents: [red-recon, eng-devsecops]
    priority: P1
```

### Creating an API Adapter

API adapters connect to tools with REST, GraphQL, or RPC interfaces that require authentication and session management.

```python
# cyberops/adapters/api/sonarqube_adapter.py
import httpx
from cyberops.adapters.base import CyberOpsAdapter, ToolParams, StructuredResult
from cyberops.adapters.credentials import CredentialBroker

class SonarQubeAdapter(CyberOpsAdapter):
    """API adapter for SonarQube code quality platform."""

    tool_name = "sonarqube"
    adapter_type = "api"

    def __init__(self, config: dict):
        self.base_url = config["base_url"]
        self.credential_broker = CredentialBroker("sonarqube")

    def is_available(self) -> bool:
        """Check if SonarQube server is reachable."""
        try:
            token = self.credential_broker.get_token()
            response = httpx.get(
                f"{self.base_url}/api/system/status",
                headers={"Authorization": f"Bearer {token}"},
                timeout=10,
            )
            return response.status_code == 200
        except (httpx.ConnectError, httpx.TimeoutException):
            return False

    def get_capabilities(self) -> list[str]:
        return [
            "code_quality_analysis",
            "issue_querying",
            "quality_gate_status",
            "quality_profile_management",
        ]

    def execute(self, params: ToolParams) -> StructuredResult:
        """Query SonarQube issues for a project."""
        if not self.is_available():
            return StructuredResult(
                status="unavailable",
                evidence_level="none",
                message="SonarQube server not reachable",
                findings=[],
                verification_guidance=[
                    f"Verify SonarQube is running at {self.base_url}",
                    "Check API token in credential store",
                ]
            )

        token = self.credential_broker.get_token()

        # Query issues with pagination
        findings = []
        page = 1
        while True:
            response = httpx.get(
                f"{self.base_url}/api/issues/search",
                headers={"Authorization": f"Bearer {token}"},
                params={
                    "projectKeys": params.project_key,
                    "severities": "CRITICAL,MAJOR,MINOR",
                    "statuses": "OPEN,CONFIRMED",
                    "ps": 100,
                    "p": page,
                },
                timeout=30,
            )

            if response.status_code != 200:
                return StructuredResult(
                    status="tool_error",
                    evidence_level="none",
                    message=f"SonarQube API error: {response.status_code}",
                    findings=[],
                )

            data = response.json()
            for issue in data.get("issues", []):
                findings.append(self._normalize_issue(issue))

            if page * 100 >= data.get("total", 0):
                break
            page += 1

        return StructuredResult(
            status="success",
            evidence_level="tool-validated",
            message=f"Retrieved {len(findings)} issues from SonarQube",
            findings=findings,
        )

    def _normalize_issue(self, issue: dict) -> Finding:
        """Normalize a SonarQube issue to the Finding schema."""
        severity_map = {
            "BLOCKER": Severity.CRITICAL,
            "CRITICAL": Severity.HIGH,
            "MAJOR": Severity.MEDIUM,
            "MINOR": Severity.LOW,
            "INFO": Severity.INFO,
        }
        return Finding(
            id=f"sonarqube-{issue['key']}",
            source_tool="sonarqube",
            severity=severity_map.get(issue.get("severity", "INFO"), Severity.INFO),
            category="VULNERABILITY" if issue.get("type") == "VULNERABILITY" else "CODE_SMELL",
            title=issue.get("message", ""),
            description=issue.get("message", ""),
            location=Location(
                file_path=issue.get("component", "").split(":")[-1],
                line=issue.get("line"),
            ),
            evidence=None,
            remediation=None,
            references=[issue.get("rule", "")],
            confidence=0.85,
            raw_data=issue,
        )
```

### Creating an MCP Server Adapter

MCP servers provide native Claude Code integration. Use FastMCP 3.0 for building custom servers.

```python
# cyberops/mcp_servers/semgrep_server.py
from fastmcp import FastMCP
import subprocess
import json

mcp = FastMCP("semgrep-security")

@mcp.tool()
def scan_code(
    target_path: str,
    config: str = "auto",
    severity: str = "ERROR,WARNING",
    output_format: str = "sarif",
) -> dict:
    """Run Semgrep scan on target code path.

    Args:
        target_path: Path to scan (file or directory)
        config: Semgrep config (auto, p/security-audit, or custom YAML path)
        severity: Comma-separated severity filter
        output_format: Output format (sarif or json)
    """
    cmd = [
        "semgrep", "scan",
        "--config", config,
        f"--{output_format}",
        "--severity", severity,
        target_path,
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=120,
        shell=False,
    )

    if output_format == "sarif":
        return json.loads(result.stdout)
    return json.loads(result.stdout)

@mcp.tool()
def generate_rule(
    pattern: str,
    language: str,
    message: str,
    severity: str = "WARNING",
) -> str:
    """Generate a Semgrep YAML rule from parameters.

    Args:
        pattern: Semgrep pattern to match
        language: Target language (python, javascript, etc.)
        message: Alert message when pattern matches
        severity: Rule severity (ERROR, WARNING, INFO)
    """
    rule = {
        "rules": [{
            "id": f"custom-rule-{hash(pattern) % 10000}",
            "pattern": pattern,
            "message": message,
            "languages": [language],
            "severity": severity,
        }]
    }
    import yaml
    return yaml.dump(rule, default_flow_style=False)

if __name__ == "__main__":
    mcp.run()
```

Register the MCP server in Claude Code's configuration:

```json
// .claude/settings.local.json (gitignored -- contains credentials)
{
  "mcpServers": {
    "semgrep-security": {
      "command": "uv",
      "args": ["run", "python", "cyberops/mcp_servers/semgrep_server.py"],
      "env": {}
    }
  }
}
```

### Creating a Library Adapter

Library adapters integrate Python packages directly, avoiding subprocess overhead.

```python
# cyberops/adapters/library/impacket_adapter.py
from cyberops.adapters.base import CyberOpsAdapter, ToolParams, StructuredResult
from cyberops.adapters.credentials import CredentialBroker

class ImpacketAdapter(CyberOpsAdapter):
    """Library adapter for Impacket protocol library."""

    tool_name = "impacket"
    adapter_type = "library"

    def is_available(self) -> bool:
        """Check if impacket is importable."""
        try:
            import impacket
            return True
        except ImportError:
            return False

    def get_capabilities(self) -> list[str]:
        return [
            "smb_enumeration",
            "ldap_query",
            "kerberos_operations",
            "credential_testing",
            "remote_execution",
        ]

    def execute(self, params: ToolParams) -> StructuredResult:
        """Execute Impacket operation."""
        if not self.is_available():
            return StructuredResult(
                status="unavailable",
                evidence_level="none",
                message="impacket not installed. Install with: uv add impacket",
                findings=[],
            )

        # Scope validation for /red-team
        if params.scope_validation_required:
            if not self.scope_oracle.validate_target(params.target):
                return StructuredResult(
                    status="scope_violation",
                    evidence_level="none",
                    message=f"Target '{params.target}' outside authorized scope",
                    findings=[],
                )

        # Retrieve scoped credentials (agent never sees raw creds)
        creds = CredentialBroker("impacket").get_credentials(params.target)

        if params.operation == "smb_enumeration":
            return self._smb_enumerate(params, creds)
        elif params.operation == "ldap_query":
            return self._ldap_query(params, creds)
        else:
            return StructuredResult(
                status="unsupported",
                evidence_level="none",
                message=f"Operation '{params.operation}' not supported",
                findings=[],
            )

    def _smb_enumerate(self, params, creds) -> StructuredResult:
        """Enumerate SMB shares on target."""
        from impacket.smbconnection import SMBConnection

        try:
            conn = SMBConnection(params.target, params.target, timeout=30)
            conn.login(creds.username, creds.password, creds.domain)
            shares = conn.listShares()
            conn.logoff()

            findings = []
            for share in shares:
                share_name = share["shi1_netname"][:-1]  # Remove null terminator
                findings.append(Finding(
                    id=f"impacket-smb-{params.target}-{share_name}",
                    source_tool="impacket",
                    severity=Severity.INFO,
                    category="DISCOVERY",
                    title=f"SMB Share: {share_name}",
                    description=f"SMB share '{share_name}' accessible on {params.target}",
                    location=Location(host=params.target, port=445, protocol="tcp"),
                    confidence=0.95,
                    raw_data={"share_name": share_name, "remark": share["shi1_remark"]},
                ))

            return StructuredResult(
                status="success",
                evidence_level="tool-validated",
                message=f"Enumerated {len(findings)} SMB shares",
                findings=findings,
            )
        except Exception as e:
            return StructuredResult(
                status="tool_error",
                evidence_level="none",
                message=f"SMB enumeration failed: {str(e)[:200]}",
                findings=[],
            )
```

---

## Tool Integration Testing Guide

### Test Categories

| Test Category | Purpose | Required For |
|---------------|---------|--------------|
| **Availability tests** | Verify `is_available()` returns correct result | All adapters |
| **Happy path tests** | Verify successful execution with valid input | All adapters |
| **Error handling tests** | Verify graceful handling of tool failures | All adapters |
| **Timeout tests** | Verify timeout enforcement | CLI and API adapters |
| **Normalization tests** | Verify Finding schema output is correct | All adapters |
| **Security tests** | Verify allowlist enforcement, no shell injection | CLI adapters |
| **Scope validation tests** | Verify scope proxy integration | /red-team adapters |
| **Credential isolation tests** | Verify credentials never leak to agent context | All adapters with auth |

### Writing Adapter Tests

```python
# tests/adapters/test_nmap_adapter.py
import pytest
from cyberops.adapters.cli.nmap_adapter import NmapAdapter

class TestNmapAdapter:
    """Tests for the Nmap CLI adapter."""

    def test_is_available_when_installed(self, mock_shutil_which):
        """Verify is_available returns True when nmap is in PATH."""
        mock_shutil_which.return_value = "/usr/bin/nmap"
        adapter = NmapAdapter()
        assert adapter.is_available() is True

    def test_is_available_when_not_installed(self, mock_shutil_which):
        """Verify is_available returns False when nmap is not in PATH."""
        mock_shutil_which.return_value = None
        adapter = NmapAdapter()
        assert adapter.is_available() is False

    def test_execute_returns_unavailable_when_not_installed(self, mock_shutil_which):
        """Verify execute returns StructuredResult with unavailable status."""
        mock_shutil_which.return_value = None
        adapter = NmapAdapter()
        result = adapter.execute(ToolParams(target="10.0.0.1", flags=["-sV"]))
        assert result.status == "unavailable"
        assert result.evidence_level == "none"
        assert len(result.verification_guidance) > 0

    def test_execute_successful_scan(self, mock_subprocess, sample_nmap_xml):
        """Verify successful scan produces normalized findings."""
        mock_subprocess.return_value.stdout = sample_nmap_xml
        mock_subprocess.return_value.returncode = 0
        adapter = NmapAdapter()
        result = adapter.execute(ToolParams(target="10.0.0.1", flags=["-sV"]))
        assert result.status == "success"
        assert result.evidence_level == "tool-validated"
        assert len(result.findings) > 0
        # Verify Finding schema compliance
        for finding in result.findings:
            assert finding.source_tool == "nmap"
            assert finding.id is not None
            assert finding.severity is not None

    def test_command_allowlist_rejects_dangerous_flags(self):
        """Verify flags not in allowlist are rejected."""
        adapter = NmapAdapter()
        result = adapter.validate_params(
            ToolParams(target="10.0.0.1", flags=["--script", "exploit"])
        )
        # --script is allowed, "exploit" as a separate arg would be treated as target
        # Actual dangerous flags:
        result = adapter.validate_params(
            ToolParams(target="10.0.0.1", flags=["--interactive"])
        )
        assert result.valid is False

    def test_shell_false_enforced(self, mock_subprocess):
        """Verify subprocess.run is called with shell=False."""
        adapter = NmapAdapter()
        adapter.execute(ToolParams(target="10.0.0.1", flags=["-sV"]))
        call_kwargs = mock_subprocess.call_args
        assert call_kwargs.kwargs.get("shell") is False

    def test_timeout_enforcement(self, mock_subprocess_timeout):
        """Verify timeout produces correct result."""
        adapter = NmapAdapter()
        result = adapter.execute(
            ToolParams(target="10.0.0.1", flags=["-sV"], timeout=5)
        )
        assert result.status == "timeout"

    def test_scope_validation_for_red_team(self, mock_scope_oracle):
        """Verify out-of-scope targets are rejected."""
        mock_scope_oracle.validate_target.return_value = False
        adapter = NmapAdapter()
        result = adapter.execute(
            ToolParams(
                target="192.168.1.1",  # Not in scope
                flags=["-sV"],
                scope_validation_required=True,
            )
        )
        assert result.status == "validation_error"
```

### Running Tests

```bash
# Run all adapter tests
uv run pytest tests/adapters/ -v

# Run tests for a specific adapter
uv run pytest tests/adapters/test_nmap_adapter.py -v

# Run with coverage
uv run pytest tests/adapters/ --cov=cyberops.adapters --cov-report=term-missing

# Run security-specific tests
uv run pytest tests/adapters/ -m security -v
```

---

## Examples

### Example 1: Metasploit Integration (Library + API Adapter)

**Scenario:** red-exploit needs to search for exploit modules, configure them, and retrieve results through Metasploit's JSON-RPC interface.

**Prerequisites:**
- Metasploit Framework installed
- `msfrpcd` daemon running (or `msfconsole` with msgrpc plugin)
- pymetasploit3 library installed: `uv add pymetasploit3`

**Adapter configuration:**

```yaml
# cyberops/adapters/registry.yaml
adapters:
  metasploit:
    class: cyberops.adapters.library.metasploit_adapter.MetasploitAdapter
    type: library
    skills: [red-team]
    agents: [red-exploit, red-privesc]
    priority: P2
    config:
      rpc_host: "127.0.0.1"
      rpc_port: 55553
      credential_key: "metasploit"  # References credential broker
```

**Usage in agent workflow:**

```python
# Agent logic (red-exploit)
adapter = adapter_registry.get("metasploit")

# Search for exploit modules matching a CVE
result = adapter.execute(ToolParams(
    operation="module_search",
    query="cve:2026-1234",
    module_type="exploit",
))

if result.status == "success":
    # Agent reasons about available exploits
    for finding in result.findings:
        # finding.title = "exploit/windows/smb/cve_2026_1234"
        # finding.description = "Remote code execution via SMB..."
        # finding.references = ["CVE-2026-1234", "CWE-787"]
        ...
elif result.status == "unavailable":
    # Level 2 fallback: methodology guidance without tool
    # Agent provides PTES exploitation methodology using CVE database knowledge
    ...
```

**Degradation behavior:**

| Level | Metasploit Available | Agent Behavior |
|-------|---------------------|----------------|
| 0 | msfrpcd running, authenticated | Agent searches modules, configures exploits, retrieves session data |
| 1 | msfrpcd unreachable | Agent notes Metasploit unavailable, provides manual `msfconsole` commands |
| 2 | Not installed | Agent provides PTES exploitation methodology guidance without tool specifics |

### Example 2: Burp Suite Integration (API Adapter)

**Scenario:** eng-devsecops wants to run a Burp Suite DAST scan against a web application and consume the results as normalized findings.

**Prerequisites:**
- Burp Suite Professional or Enterprise running
- API key configured
- Target URL authorized in engagement scope

**Adapter usage:**

```python
# Agent logic (eng-devsecops)
adapter = adapter_registry.get("burp_suite")

# Check availability first
if not adapter.is_available():
    # Level 1/2 fallback: use OWASP ZAP instead or provide DAST methodology
    zap_adapter = adapter_registry.get("owasp_zap")
    if zap_adapter.is_available():
        result = zap_adapter.execute(ToolParams(
            operation="active_scan",
            target_url="https://app.example.com",
        ))
    else:
        # Level 2: pure methodology guidance
        analysis.evidence_level = "unvalidated"
        analysis.add_gap("burp_suite", ["Install Burp Suite or OWASP ZAP for DAST"])
        return analysis

# Burp Suite is available -- run scan
result = adapter.execute(ToolParams(
    operation="active_scan",
    target_url="https://app.example.com",
    scan_config="default",
))

if result.status == "success":
    # Findings are normalized to the common schema
    for finding in result.findings:
        # finding.source_tool = "burp_suite"
        # finding.severity = Severity.HIGH
        # finding.category = "VULNERABILITY"
        # finding.title = "SQL Injection in /api/users"
        # finding.location = Location(url="https://app.example.com/api/users")
        # finding.remediation = "Use parameterized queries..."
        ...
```

**API adapter handles internally:**
- Authentication with API key via credential broker
- Scan initiation and progress polling
- SARIF output parsing (Enterprise) or JSON normalization (Professional)
- Rate limiting and timeout management
- TLS certificate verification

### Example 3: Semgrep Integration (CLI + MCP Adapter)

**Scenario:** eng-devsecops configures Semgrep for SAST scanning. Semgrep has both a CLI adapter and an official MCP server, demonstrating the protocol hierarchy in practice.

**MCP server path (preferred when configured):**

```json
// .claude/settings.local.json
{
  "mcpServers": {
    "semgrep": {
      "command": "uvx",
      "args": ["semgrep", "--mcp"],
      "env": {}
    }
  }
}
```

When the MCP server is configured, the agent can invoke Semgrep directly through Claude Code's native tool calling, with structured parameters and typed responses.

**CLI adapter fallback (when MCP server is not configured):**

```python
# Agent logic (eng-devsecops)
adapter = adapter_registry.get("semgrep")

# Run SAST scan with security audit rules
result = adapter.execute(ToolParams(
    operation="scan",
    target_path="./src",
    config="p/security-audit",
    output_format="sarif",
    severity="ERROR,WARNING",
))

if result.status == "success":
    # SARIF output is parsed directly (native SARIF support)
    critical_findings = [
        f for f in result.findings if f.severity == Severity.CRITICAL
    ]

    # Bidirectional: agent can also GENERATE custom rules
    custom_rule = adapter.execute(ToolParams(
        operation="generate_rule",
        pattern="$X == $X",
        language="python",
        message="Comparison of expression with itself is always true",
        severity="WARNING",
    ))

    # Write the custom rule for future scans
    # This is unique to YAML-first tools like Semgrep
```

**Bidirectional integration detail:**

Semgrep, Checkov, and Nuclei all use YAML-based rule definitions that are LLM-friendly. This means agents can both:
1. **Consume findings** from tool scans (standard adapter flow)
2. **Generate custom rules** for the tool to execute (reverse flow)

This bidirectional capability is a key advantage of YAML-first tools and is only available for tools with LLM-writable rule formats.

---

## Security Controls

Security controls are enforced at the adapter layer, not the agent layer. Agents never interact directly with tools or credentials.

**SSOT:** ADR-PROJ010-005, Section 4 (Security Controls at the Adapter Layer).

### Control Matrix

| Control | Implementation | Rationale |
|---------|---------------|-----------|
| **Command allowlists** | CLI adapters maintain explicit allowlists of permitted flags. No argument passes to subprocess without allowlist validation. | Prevents command injection |
| **shell=False mandatory** | `shell=True` is forbidden in all subprocess calls | Prevents shell injection |
| **Subprocess sandboxing** | Fresh sandbox per invocation. Explicit timeout, output size limits, resource constraints. | Prevents cross-invocation contamination |
| **Credential broker** | Agents never see raw credentials. Adapters retrieve credentials at execution time from secure store. | Eliminates credential exposure in agent context |
| **Output schema validation** | All JSON, SARIF, and XML outputs are schema-validated before agent consumption. | Prevents prompt injection via tool output |
| **Output size limits** | Adapter enforces maximum output size (configurable per tool). | Prevents context window exhaustion |
| **Scope-validating proxy** | /red-team tool invocations pass through Tool Proxy before execution. Default-deny. | Makes out-of-scope actions structurally impossible |
| **TLS-only for remote** | API adapters enforce TLS. Certificate validation mandatory. | Prevents credential interception |
| **Rate limiting** | API adapters implement rate limiting with exponential backoff. | Prevents API abuse |

### Credential Broker Pattern

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

Credential configuration lives in `.claude/settings.local.json` (gitignored):

```json
{
  "credentials": {
    "sonarqube": {
      "type": "api_token",
      "token_env": "SONARQUBE_TOKEN"
    },
    "burp_suite": {
      "type": "api_key",
      "key_env": "BURP_API_KEY"
    },
    "metasploit": {
      "type": "rpc_token",
      "token_env": "MSF_RPC_TOKEN"
    }
  }
}
```

### Scope-Validating Proxy (/red-team only)

For /red-team operations, every tool invocation passes through the Tool Proxy:

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

/eng-team operations do not require the scope proxy because they operate on source code and configurations, not live targets.

---

## Troubleshooting

### Common Issues

| Issue | Cause | Resolution |
|-------|-------|------------|
| Adapter returns "unavailable" | Tool not installed or not in PATH | Verify installation: `which <tool>` or check `is_available()` |
| "Scope violation" error | Target outside authorized engagement scope | Verify scope document targets; run `scope_oracle.validate_target()` manually |
| Timeout on CLI adapter | Tool execution exceeds timeout limit | Increase `timeout` parameter; check if tool is blocked by firewall |
| Empty findings from SARIF parser | Tool ran successfully but produced no findings | Verify target has analyzable content; check tool configuration and rules |
| Authentication failure on API adapter | Expired or invalid credentials | Rotate credentials in `.claude/settings.local.json`; check token expiry |
| Output size limit exceeded | Tool output exceeds maximum | Increase limit in adapter config; check if scan scope is too broad |
| Normalization produces incorrect severity | Tool-to-Finding severity mapping mismatch | Review normalizer severity mapping; adjust for tool-specific severity scales |
| MCP server not connecting | MCP server process failed to start | Check `uv run` command in settings; verify dependencies installed |
| "shell=True" audit failure | Code review found shell=True usage | Replace with explicit command list (never use shell=True) |
| Findings not deduplicating | Different tools report same vulnerability differently | Check Finding `id` generation; ensure cross-tool correlation uses CVE/CWE references |

### Diagnostic Commands

```bash
# Check if a tool is available
uv run python -c "from cyberops.adapters.cli.nmap_adapter import NmapAdapter; print(NmapAdapter().is_available())"

# List all registered adapters and their availability
uv run python -m cyberops.adapters.status

# Test a specific adapter with dry-run
uv run python -m cyberops.adapters.test --adapter nmap --dry-run

# Validate adapter registry configuration
uv run python -m cyberops.adapters.validate

# Show the normalization output for a sample tool output
uv run python -m cyberops.adapters.normalize --tool nmap --input sample_nmap_output.xml

# Check credential broker configuration (without exposing credentials)
uv run python -m cyberops.adapters.credentials --check
```

### Existing Security MCP Servers

Before building a custom MCP server, evaluate these existing implementations:

| MCP Server | Tools Wrapped | Assessment Criteria |
|------------|--------------|---------------------|
| Semgrep MCP (official) | Semgrep | Highest trust -- official from Semgrep team |
| mcp-for-security (cyproxio) | Nmap, SQLMap, FFUF, Masscan | Code review required for command injection risks |
| pentest-mcp (DMontgomery40) | Nmap, GoBuster, Nikto, JtR, Hashcat | Evaluate code quality and security controls |
| hexstrike-ai (0x4m4) | 150+ tools | Largest server; evaluate for reference patterns |
| sast-mcp (Sengtocxoen) | Multiple SAST tools | Claude Code integration focus |

**Evaluation checklist before adopting an existing MCP server:**

1. Code review for command injection vulnerabilities
2. Output format validation (schema adherence, sanitization)
3. Maintenance status and community activity
4. License compatibility
5. Alignment with the common adapter interface contract
6. Credential handling practices

---

## References

| Source | Content |
|--------|---------|
| [ADR-PROJ010-005](../../decisions/ADR-PROJ010-005-tool-integration-adapters.md) | SSOT: Tool Integration Adapter Architecture -- MCP-Primary with Common Interface |
| [ADR-PROJ010-004](../../decisions/ADR-PROJ010-004-configurable-rule-sets.md) | Configurable Rule Set Architecture (tool selection per engagement profile) |
| [C-001](../research/stream-c-tool-integration/C-001-offensive-tools.md) | Offensive Tool Ecosystem Survey (12 tools analyzed) |
| [C-002](../research/stream-c-tool-integration/C-002-defensive-tools.md) | Defensive Tool Ecosystem Survey (12 tools analyzed) |
| [C-003](../research/stream-c-tool-integration/C-003-agentic-integration-patterns.md) | Agentic Tool Integration Patterns (MCP, adapters, standalone design) |
| [PLAN.md R-012](../../PLAN.md) | Tool Integration Architecture requirement |
| [PLAN.md R-020](../../PLAN.md) | Authorization verification requirement |
| `/eng-team SKILL.md` | Engineering team skill definition |
| `/red-team SKILL.md` | Red team skill definition |

### External Standards and Specifications

| Standard | URL |
|----------|-----|
| SARIF v2.1.0 (OASIS) | https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html |
| MCP Specification 2025-11-25 | https://modelcontextprotocol.io/specification/2025-11-25 |
| FastMCP 3.0 | https://www.firecrawl.dev/blog/fastmcp-tutorial-building-mcp-servers-python |
| Nmap Output Documentation | https://nmap.org/book/man-output.html |
| Semgrep Rule Syntax | https://semgrep.dev/docs/writing-rules/rule-syntax |
| Nuclei Template Docs | https://docs.projectdiscovery.io/templates/introduction |
| ZAP API Reference | https://www.zaproxy.org/docs/api/ |
| SonarQube Webhooks | https://docs.sonarsource.com/sonarqube-server/2025.2/project-administration/webhooks/ |
| pymetasploit3 | https://github.com/DanMcInerney/pymetasploit3 |
| BloodHound CE | https://github.com/SpecterOps/BloodHound |

---

*PROJ-010: Cyber Ops -- Tool Integration Guide*
*SSOT: ADR-PROJ010-005*
*Created: 2026-02-22*
