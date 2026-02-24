# C-003: Agentic Tool Integration Patterns

> Stream C: Tool Integration | PROJ-010 Cyber Ops | Phase 1 Research

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | High-level findings and strategic implications |
| [L1: Key Findings](#l1-key-findings) | Structured findings by pattern category |
| [L2: Detailed Analysis](#l2-detailed-analysis) | Pattern deep dives with architecture details |
| [Evidence and Citations](#evidence-and-citations) | Dated sources, categorized |
| [Recommendations](#recommendations) | Recommended architecture for Jerry cyber ops skills |

---

## L0: Executive Summary

Agentic tool integration has matured significantly in 2025-2026, with the Model Context Protocol (MCP) emerging as the dominant standard for connecting AI agents to external tools. Three primary integration patterns exist: MCP server wrapping (protocol-native), CLI adapter wrapping (subprocess execution with output parsing), and API adapter wrapping (HTTP client with authentication management). The "standalone capable" design principle required by R-012 aligns with modern agentic architecture best practices -- agents should implement graceful degradation where tool absence reduces capability but does not prevent operation. Existing security-focused MCP servers (mcp-for-security, pentest-mcp, hexstrike-ai, sast-mcp) validate that the pattern works for security tools specifically. The critical design decisions for Jerry's cyber ops skills are: (1) adopting a common adapter interface that abstracts tool-specific details, (2) implementing a SARIF-based normalization layer for findings, (3) using the MCP protocol where available and CLI adapters as fallback, and (4) enforcing strict sandboxing with scoped credentials for tool execution.

---

## L1: Key Findings

### Finding 1: MCP Has Become the Industry Standard

The Model Context Protocol (MCP), introduced by Anthropic in November 2024, has achieved rapid and broad adoption:
- **97M+ monthly SDK downloads** as of late 2025
- **13,000+ MCP servers** launched on GitHub in 2025
- **Backed by**: Anthropic, OpenAI, Google, Microsoft
- **Specification version**: 2025-11-25 (latest stable), with June 2025 updates adding OAuth, structured tool outputs, and server-initiated user interactions
- **Transport**: STDIO (local), HTTP/SSE (remote), with Streamable HTTP added in 2025

For Jerry, MCP is the natural integration protocol since Claude Code already uses MCP natively. Security tool MCP servers can be connected directly to Claude Code sessions.

### Finding 2: Three Adapter Patterns Cover All Tool Types

| Pattern | When to Use | Pros | Cons |
|---------|-------------|------|------|
| **MCP Server** | Tool has or can get an MCP server | Native integration with Claude Code; structured tool calling; authentication built in | Requires MCP server implementation or existing one |
| **CLI Adapter** | Tool is CLI-based with structured output | Simple implementation; no daemon needed; works with any CLI tool | Subprocess overhead; output parsing fragility; no persistent state |
| **API Adapter** | Tool exposes REST/GraphQL/RPC API | Rich interaction; persistent state; session management | Requires running service; authentication complexity; network dependency |

All three patterns should implement a common interface:
```
execute(tool_name, params) -> StructuredResult | ToolUnavailableError
```

### Finding 3: "Standalone Capable" Design Is an Established Pattern

Modern agent frameworks recognize graceful degradation as a key design principle:
- **Fallback strategies**: Agents implement complex-to-simple pattern fallback when tools are unavailable
- **CoT + Tools**: Chain-of-thought reasoning works independently; tools enhance with real-time data
- **Memory + Multi-Agent**: Core reasoning persists across tool availability changes
- **Toolformer pattern**: Agents autonomously decide WHEN to call tools, evaluating whether a tool call would improve the result

For Jerry cyber ops skills, this means:
- Offensive skill can analyze scope, plan attack paths, and generate reports using LLM reasoning alone
- Defensive skill can review code patterns, suggest mitigations, and assess risk without tool execution
- Tools ADD: real-time scanning data, exploitation validation, concrete evidence
- Tools DO NOT REPLACE: threat modeling, risk assessment, prioritization, reporting

### Finding 4: Security Considerations Are Critical and Non-Negotiable

Agent tool execution introduces significant security risks:

**Sandboxing is mandatory:**
- MicroVMs (Firecracker, Kata Containers) provide strongest isolation
- gVisor provides syscall interception without full VMs
- Kubernetes agent-sandbox (K8s SIG project, 2025) provides declarative pod-based isolation
- Claude Code uses sandbox isolation to keep credentials outside the execution environment

**Credential management requires scoping:**
- Short-lived tokens with minimum required scope per task
- Secret injection at task start, not inherited from host
- Expired credentials cannot be reused if compromised
- Separate credential stores per tool/task context

**Output sanitization is required:**
- Tool output may contain prompt injection attempts
- SARIF/JSON outputs should be schema-validated before agent consumption
- Unstructured text output requires careful filtering

### Finding 5: Existing Security MCP Servers Provide Reference Implementations

| MCP Server | Tools Wrapped | Transport | Notes |
|------------|--------------|-----------|-------|
| mcp-for-security (cyproxio) | SQLMap, FFUF, Nmap, Masscan | STDIO | Focused on web/network scanning |
| pentest-mcp (DMontgomery40) | Nmap, GoBuster, Nikto, JtR, Hashcat | STDIO/HTTP/SSE | Professional pentesting focus |
| pentestMCP (ramkansal) | 20+ tools (Nmap, Nuclei, ZAP, SQLMap, etc.) | STDIO | Bridge between LLMs and pentest tools |
| hexstrike-ai (0x4m4) | 150+ cybersecurity tools | STDIO | Broadest coverage, autonomous operation |
| sast-mcp (Sengtocxoen) | Multiple SAST tools | STDIO | Claude Code integration focus |
| secops-mcp (securityfortech) | Mixed pentest/defense tools | STDIO | All-in-one security testing |
| Semgrep MCP | Semgrep | STDIO | Official from Semgrep team |
| any-cli-mcp-server (eirikb) | Any CLI tool | STDIO | Generic CLI-to-MCP wrapper using --help |

These demonstrate that the pattern is proven and that we can either use existing MCP servers or build custom ones following established patterns.

---

## L2: Detailed Analysis

### Integration Architecture Patterns

#### Pattern 1: MCP Server Wrapping

**Architecture:**
```
Claude Code / Jerry Agent
    |
    | MCP Protocol (STDIO or HTTP/SSE)
    v
MCP Server (Python/TypeScript/Go)
    |
    | Subprocess / API Call / Library Import
    v
Security Tool (Nmap, Semgrep, ZAP, etc.)
    |
    | Tool-specific output (XML, JSON, text)
    v
Output Parser (in MCP Server)
    |
    | Structured tool result
    v
MCP Response -> Agent
```

**Implementation with FastMCP (Python):**

FastMCP 3.0 (released January 2026) is the recommended framework for building MCP servers in Python. It provides:
- Decorator-based tool definition (`@mcp.tool()`)
- Automatic schema generation from type hints
- STDIO and HTTP transport support
- Built-in error handling and timeout management

**Key Design Decisions:**
- Each security tool gets its own MCP server (separation of concerns)
- Servers are registered in Claude Code's MCP configuration
- Servers handle authentication, timeout, and error recovery internally
- Output is normalized to structured format before returning to agent

**When to Use:**
- Tool will be used frequently across multiple sessions
- Tool integration requires persistent configuration
- Multiple agents need access to the same tool
- Tool output benefits from structured typing

#### Pattern 2: CLI Adapter Wrapping

**Architecture:**
```
Jerry Agent
    |
    | Function call (internal)
    v
CLI Adapter Module (Python)
    |
    | subprocess.run() with timeout
    v
CLI Tool (nmap, nuclei, trivy, etc.)
    |
    | stdout/stderr capture
    v
Output Parser
    |
    | Structured result
    v
Agent receives typed findings
```

**Design Principles for CLI Adapters:**

1. **Consistent global flags**: All CLI tools should support `--output json` or equivalent. The adapter maps to tool-specific flags.

2. **Structured output as contract**: Treat CLI JSON output as a stable API. The `--json` flag provides structured output for programmatic consumption, making CLI part of the pipeline rather than a separate tool.

3. **Timeout management**: All subprocess calls must have explicit timeouts. Security tools can run for minutes (Nmap) or hours (Hashcat).

4. **Error classification**: Distinguish between tool errors (scan failed), permission errors (access denied), and infrastructure errors (tool not installed).

5. **Idempotent execution**: CLI calls should be repeatable without side effects where possible.

**Implementation Pattern:**
```python
class CLIAdapter:
    """Base class for CLI tool adapters."""

    def execute(self, params: ToolParams) -> ToolResult:
        """Execute tool and return structured result."""
        if not self.is_available():
            return ToolResult(
                status="unavailable",
                message=f"{self.tool_name} not found in PATH",
                findings=[]
            )

        cmd = self.build_command(params)
        result = subprocess.run(
            cmd,
            capture_output=True,
            timeout=params.timeout_seconds,
            text=True
        )
        return self.parse_output(result.stdout, result.stderr, result.returncode)

    def is_available(self) -> bool:
        """Check if tool binary is available."""
        return shutil.which(self.tool_name) is not None
```

**When to Use:**
- Tool is CLI-only with no API
- Integration is lightweight/infrequent
- Tool produces structured output (JSON, XML, SARIF)
- No persistent state needed between calls

#### Pattern 3: API Adapter Wrapping

**Architecture:**
```
Jerry Agent
    |
    | Function call (internal)
    v
API Adapter Module (Python)
    |
    | HTTP/RPC client (requests, httpx, etc.)
    v
Tool API Server (SonarQube, Burp Suite, BloodHound, etc.)
    |
    | JSON/GraphQL response
    v
Response Parser
    |
    | Structured result
    v
Agent receives typed findings
```

**Design Principles for API Adapters:**

1. **Authentication abstraction**: Support multiple auth methods (API key, OAuth, JWT, token) via configuration, not code changes.

2. **Session management**: Handle token refresh, session expiry, and reconnection transparently.

3. **Rate limiting**: Respect tool API rate limits with built-in backoff and retry logic.

4. **Pagination**: Handle paginated results automatically, presenting complete result sets to the agent.

5. **Health checking**: Verify API availability before operations to fail fast.

**When to Use:**
- Tool exposes a REST/GraphQL/RPC API
- Persistent state or session management is needed
- Tool requires authentication
- Rich interaction patterns (create project -> run scan -> poll status -> get results)

### Output Parsing Patterns

#### Structured Output Formats

| Format | Tools | Parser | Quality |
|--------|-------|--------|---------|
| SARIF v2.1.0 | CodeQL, Semgrep, Nuclei, Trivy, Checkmarx | sarif-python, sarif-tools | Excellent -- OASIS standard with rich metadata |
| JSON (custom) | Nmap (via libnmap), ZAP, SonarQube, Snyk | json module + schema validation | Good -- tool-specific but structured |
| XML | Nmap (native), Burp Suite, Nikto | ElementTree, lxml | Good -- mature parsing libraries |
| CycloneDX/SPDX | Trivy, Snyk | cyclonedx-python, spdx-tools | Good -- SBOM standards |
| Text (structured) | NetExec, Hashcat, JtR | Custom regex/parsing | Poor -- fragile, version-dependent |
| Text (unstructured) | Responder, some Metasploit output | Custom parsing | Very Poor -- avoid if alternatives exist |

#### Normalization Strategy

All tool outputs should be normalized to a common finding schema:

```python
@dataclass
class Finding:
    """Normalized security finding from any tool."""
    id: str                      # Unique finding identifier
    source_tool: str             # Tool that produced the finding
    severity: Severity           # CRITICAL, HIGH, MEDIUM, LOW, INFO
    category: FindingCategory    # VULNERABILITY, MISCONFIGURATION, SECRET, etc.
    title: str                   # Human-readable finding title
    description: str             # Detailed finding description
    location: Location | None    # File/URL/host/port if applicable
    evidence: str | None         # Raw evidence from tool
    remediation: str | None      # Suggested fix
    references: list[str]        # CVE, CWE, tool-specific rule IDs
    confidence: float            # 0.0-1.0 confidence score
    raw_data: dict               # Original tool output preserved
```

This enables:
- Cross-tool finding correlation (same vulnerability found by Semgrep AND CodeQL)
- Severity-based prioritization regardless of source tool
- Uniform reporting across all integrated tools
- Agent reasoning over findings without tool-specific knowledge

### Tool Orchestration Patterns

#### Sequential Chaining

```
Nmap (recon) -> findings -> Nuclei (vuln scan) -> findings -> Agent (analysis)
```

One tool's output feeds into the next. Nmap discovers services, Nuclei scans them for vulnerabilities, agent analyzes and prioritizes.

#### Parallel Execution

```
                    -> Semgrep (SAST)     -> findings ->
Agent (planning) -> -> Trivy (containers)  -> findings -> Agent (synthesis)
                    -> Checkov (IaC)       -> findings ->
```

Multiple tools run simultaneously when they operate on independent inputs. Results are merged and deduplicated.

#### Conditional Branching

```
Agent -> Initial Scan ->
    if web_app: ZAP active scan
    if AD_env: BloodHound + NetExec
    if source_code: Semgrep + CodeQL
    if containers: Trivy
```

Agent decides which tools to invoke based on target characteristics and initial reconnaissance.

### "Standalone Capable" Design Pattern

**Core Principle:** The agent MUST be fully functional without any external tools. Tools augment capability; they do not enable it.

**Implementation Strategy:**

| Agent Capability | Without Tools | With Tools |
|-----------------|---------------|------------|
| Threat modeling | LLM reasoning over scope description | LLM reasoning + Nmap/BloodHound data |
| Vulnerability assessment | Pattern-based analysis from training data | Semgrep/CodeQL/Nuclei scan results |
| Risk prioritization | CVSS-based reasoning from knowledge | Real-time vulnerability data + exploit availability |
| Remediation advice | Best practice recommendations | Tool-specific fix suggestions (Semgrep autofix) |
| Report generation | Structured report from analysis | Report enriched with tool evidence |
| Attack path analysis | Theoretical path modeling | BloodHound graph data + validation |

**Graceful Degradation Ladder:**

```
Level 0: Full tool access (optimal)
    Agent orchestrates multiple tools, cross-correlates findings,
    provides evidence-backed analysis

Level 1: Partial tool access (degraded)
    Agent uses available tools, notes gaps in coverage,
    provides analysis with explicit uncertainty markers

Level 2: No tool access (standalone)
    Agent performs analysis using LLM knowledge base,
    provides recommendations with "unvalidated" markers,
    suggests manual verification steps
```

**Implementation in Jerry:**

```python
class CyberOpsAgent:
    """Agent that operates standalone and uses tools when available."""

    def analyze(self, scope: Scope) -> Analysis:
        # Step 1: LLM-based analysis (always available)
        analysis = self.reason_about_scope(scope)

        # Step 2: Tool augmentation (when available)
        for tool in self.available_tools():
            try:
                tool_findings = tool.execute(scope)
                analysis.enrich(tool_findings)
                analysis.evidence_level = "tool-validated"
            except ToolUnavailableError:
                analysis.add_gap(f"{tool.name} unavailable")
                analysis.evidence_level = "llm-only"

        return analysis
```

### Framework Comparison: How Others Do It

#### LangChain/LangGraph Tool Integration

- **Tool definition**: `@tool` decorator with name, docstring, and type hints
- **Structured output**: Pydantic BaseModel for output validation
- **Agent pattern**: ReAct (Reason + Act) loop on LangGraph's durable runtime
- **MCP support**: LangGraph supports MCP integration for tool discovery
- **Key insight**: Tools defined with clear schemas; agent decides when to call them

#### CrewAI Tool Integration

- **Role-based agents**: Researchers, analysts, content creators with specialized tools
- **Crews and Flows**: High-level coordination with low-level control
- **Tool assignment**: Tools are assigned to specific agent roles
- **Key insight**: Role specialization determines tool access

#### AutoGen Tool Integration

- **Multi-agent conversation**: Tools exposed as functions in conversation context
- **Code execution**: Built-in sandboxed code execution capability
- **Microsoft ecosystem**: Strong integration with Azure services
- **Key insight**: Tools are conversation participants, not just function calls

#### Jerry Differentiation

Jerry's approach should differ from these frameworks because:
1. **Domain specialization**: Security tools have unique safety requirements
2. **Standalone requirement**: Most frameworks assume tools are always available
3. **MCP native**: Claude Code's MCP integration is more natural than LangChain's tool abstraction
4. **Filesystem persistence**: Jerry persists state to files, not in-memory stores

### Security Considerations for Tool Integration

#### Execution Sandboxing

**Recommended approach for Jerry:**

1. **Local tools (Nmap, Semgrep, Trivy)**: Run via subprocess with:
   - Explicit command allowlists (never pass unsanitized input to shell)
   - Timeout enforcement
   - Output size limits
   - No shell=True in subprocess calls

2. **Remote tools (SonarQube, Burp Suite)**: Connect via API with:
   - TLS-only connections
   - API key/token rotation
   - Request rate limiting
   - Response validation

3. **MCP servers**: Run as separate processes with:
   - STDIO transport for local isolation
   - Process-level resource limits
   - Capability-based tool permissions

#### Credential Management

**Recommended approach for Jerry:**

```
+------------------+     +-------------------+     +------------------+
|                  |     |                   |     |                  |
|   Jerry Agent    |     | Credential Store  |     |  Security Tool   |
|                  |     |                   |     |                  |
|  NO credentials  |---->| Scoped tokens     |---->| Authenticated    |
|  in context      |     | Per-tool secrets  |     | operations       |
|                  |     | Time-limited      |     |                  |
+------------------+     +-------------------+     +------------------+
```

- Agent never sees raw credentials
- Adapters retrieve credentials from secure store at execution time
- Credentials are scoped to minimum required permissions
- All credentials are time-limited where possible
- Credential configuration is in `.claude/settings.local.json` (gitignored)

#### Output Sanitization

- Schema-validate all JSON/SARIF before agent consumption
- Strip potential prompt injection content from unstructured text output
- Limit output size to prevent context window exhaustion
- Log raw output for audit but filter before agent processing

---

## Evidence and Citations

### Primary Sources (accessed 2026-02-22)

**MCP (Model Context Protocol):**
- [MCP Specification 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25) -- Latest stable spec
- [MCP Build Server Tutorial](https://modelcontextprotocol.io/docs/develop/build-server) -- Official build guide
- [MCP Spec Updates June 2025 (Auth0)](https://auth0.com/blog/mcp-specs-update-all-about-auth/) -- OAuth and structured outputs
- [MCP Enterprise Adoption Guide](https://guptadeepak.com/the-complete-guide-to-model-context-protocol-mcp-enterprise-adoption-market-trends-and-implementation-strategies/) -- 97M+ downloads, 13K+ servers
- [MCP Wikipedia](https://en.wikipedia.org/wiki/Model_Context_Protocol) -- Overview and history

**MCP Security:**
- [MCP Security Risks (Red Hat)](https://www.redhat.com/en/blog/model-context-protocol-mcp-understanding-security-risks-and-controls) -- Risk analysis
- [MCP Security Vulnerabilities 2026 (Practical DevSecOps)](https://www.practical-devsecops.com/mcp-security-vulnerabilities/) -- Prompt injection, tool poisoning
- [MCP Security Risks (Pillar Security)](https://www.pillar.security/blog/the-security-risks-of-model-context-protocol-mcp) -- Comprehensive risk assessment
- [MCP Security Resources Feb 2026 (Adversa AI)](https://adversa.ai/blog/top-mcp-security-resources-february-2026/) -- Current resource compilation
- [MCP-Scan (Invariant Labs)](https://github.com/invariantlabs-ai/mcp-scan) -- Security scanning tool for MCP

**MCP Server Building:**
- [FastMCP Tutorial (Firecrawl)](https://www.firecrawl.dev/blog/fastmcp-tutorial-building-mcp-servers-python) -- Python MCP server building
- [How to Build MCP Server (Leanware)](https://www.leanware.co/insights/how-to-build-mcp-server) -- Step-by-step guide
- [any-cli-mcp-server (GitHub)](https://lobehub.com/mcp/eirikb-any-cli-mcp-server) -- Generic CLI-to-MCP wrapper
- [MCP CLI Tool (Phil Schmid)](https://www.philschmid.de/mcp-cli) -- CLI for MCP server interaction

**Security MCP Servers:**
- [mcp-for-security (GitHub)](https://github.com/cyproxio/mcp-for-security) -- Nmap, SQLMap, FFUF, Masscan
- [pentest-mcp (GitHub)](https://github.com/DMontgomery40/pentest-mcp) -- Professional pentesting MCP
- [pentestMCP (GitHub)](https://github.com/ramkansal/pentestMCP) -- 20+ security tools
- [hexstrike-ai (GitHub)](https://github.com/0x4m4/hexstrike-ai) -- 150+ cybersecurity tools
- [sast-mcp (GitHub)](https://github.com/Sengtocxoen/sast-mcp) -- SAST tools for Claude Code

**Agent Sandboxing and Security:**
- [NVIDIA Sandboxing Guidance](https://developer.nvidia.com/blog/practical-security-guidance-for-sandboxing-agentic-workflows-and-managing-execution-risk) -- Practical sandboxing guide
- [Agent Sandbox Kubernetes (K8s SIG)](https://github.com/kubernetes-sigs/agent-sandbox) -- K8s agent isolation
- [Claw EA Secrets Isolation](https://www.clawea.com/controls/secret-boundary) -- Scoped credential patterns
- [Agent Sandbox on K8s (InfoQ)](https://www.infoq.com/news/2025/12/agent-sandbox-kubernetes/) -- gVisor + Kata Containers
- [How to Sandbox AI Agents 2026 (Northflank)](https://northflank.com/blog/how-to-sandbox-ai-agents) -- MicroVMs, gVisor strategies
- [Claude Code Sandboxing (Anthropic)](https://www.anthropic.com/engineering/claude-code-sandboxing) -- Credential isolation
- [INNOQ Dev Sandbox](https://www.innoq.com/en/blog/2025/12/dev-sandbox/) -- Practical agent sandboxing

**Agent Design Patterns:**
- [Agentic AI Design Patterns 2025 (Azilen)](https://www.azilen.com/blog/agentic-ai-design-patterns/) -- Five core patterns
- [Agent Design Patterns (Databricks)](https://docs.databricks.com/aws/en/generative-ai/guide/agent-system-design-patterns) -- Tool use + fallback
- [AI Agent Stack 2026 (Tensorlake)](https://www.tensorlake.ai/blog/the-ai-agent-stack-in-2026-frameworks-runtimes-and-production-tools) -- Framework landscape
- [CLI Patterns for AI Agents (InfoQ)](https://www.infoq.com/articles/ai-agent-cli/) -- --json flag as API contract
- [How Tools Are Called in AI Agents 2025](https://medium.com/@sayalisureshkumbhar/how-tools-are-called-in-ai-agents-complete-2025-guide-with-examples-42dcdfe6ba38) -- Tool calling patterns

**LangChain/LangGraph:**
- [LangChain Agents Documentation](https://docs.langchain.com/oss/python/langchain/agents) -- Agent architecture
- [LangChain Tools Guide 2025 (Latenode)](https://latenode.com/blog/ai-frameworks-technical-infrastructure/langchain-setup-tools-agents-memory/langchain-tools-complete-guide-creating-using-custom-llm-tools-code-examples-2025) -- Custom tool creation
- [LangChain AI Agents Guide 2025 (DigitalApplied)](https://www.digitalapplied.com/blog/langchain-ai-agents-guide-2025) -- Implementation guide
- [Building Custom Tools (Pinecone)](https://www.pinecone.io/learn/series/langchain/langchain-tools/) -- Tool building patterns

**CrewAI / AutoGen:**
- [Best AI Agent Frameworks 2025 (Maxim)](https://www.getmaxim.ai/articles/top-5-ai-agent-frameworks-in-2025-a-practical-guide-for-ai-builders/) -- Framework comparison
- [CrewAI vs AutoGen vs Lindy (Lindy)](https://www.lindy.ai/blog/crewai-vs-autogen) -- Feature comparison
- [Agent Orchestration 2026 (Iterathon)](https://iterathon.tech/blog/ai-agent-orchestration-frameworks-2026) -- LangGraph, CrewAI, AutoGen
- [Top AI Agent Frameworks (Codecademy)](https://www.codecademy.com/article/top-ai-agent-frameworks-in-2025) -- Overview

**Structured Output:**
- [OpenAI Structured Outputs](https://openai.com/index/introducing-structured-outputs-in-the-api/) -- JSON schema adherence
- [Structured Outputs Guide (Agenta)](https://agenta.ai/blog/the-guide-to-structured-outputs-and-function-calling-with-llms) -- Comprehensive guide

**SARIF Standard:**
- [SARIF v2.1.0 (OASIS)](https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html) -- Full specification
- [SARIF Guide (Sonar)](https://www.sonarsource.com/resources/library/sarif/) -- Adoption and tooling

---

## Recommendations

### Recommended Architecture for Jerry Cyber Ops Skills

#### Architecture Overview

```
+----------------------------------------------------------------------+
|                        Jerry Cyber Ops Skills                         |
|                                                                       |
|  +------------------+    +-------------------+    +-----------------+ |
|  | Offensive Skill  |    | Defensive Skill   |    | Shared Layer    | |
|  |                  |    |                   |    |                 | |
|  | - Recon Agent    |    | - SAST Agent      |    | - Finding       | |
|  | - Exploit Agent  |    | - DAST Agent      |    |   Schema        | |
|  | - Post-Exploit   |    | - SCA Agent       |    | - SARIF Parser  | |
|  | - Report Agent   |    | - IaC Agent       |    | - Adapter Base  | |
|  |                  |    | - Report Agent    |    | - Credential    | |
|  +--------+---------+    +--------+----------+    |   Manager       | |
|           |                       |               +---------+-------+ |
|           v                       v                         |         |
|  +--------------------------------------------------------------+    |
|  |                    Tool Adapter Layer                          |    |
|  |                                                                |    |
|  |  +----------+  +----------+  +----------+  +----------+      |    |
|  |  | MCP      |  | CLI      |  | API      |  | Library  |      |    |
|  |  | Adapter  |  | Adapter  |  | Adapter  |  | Adapter  |      |    |
|  |  +----------+  +----------+  +----------+  +----------+      |    |
|  +--------------------------------------------------------------+    |
+----------------------------------------------------------------------+
           |                |               |              |
     MCP Protocol      subprocess       HTTP/RPC      Python import
           |                |               |              |
     +----------+    +----------+    +----------+    +----------+
     | Nmap MCP |    | nuclei   |    | SonarQube|    | impacket |
     | Semgrep  |    | trivy    |    | ZAP      |    |          |
     | MCP      |    | checkov  |    | Snyk     |    |          |
     +----------+    +----------+    +----------+    +----------+
```

#### Design Decisions

**D-001: Adopt MCP as Primary Integration Protocol**
- Rationale: Claude Code natively supports MCP; existing security MCP servers validate the pattern; FastMCP 3.0 simplifies server creation
- Fallback: CLI adapter for tools without MCP servers
- Action: Use existing MCP servers where available; build custom MCP servers for priority tools

**D-002: Implement Common Adapter Interface**
- Rationale: Agent logic should not depend on tool-specific details
- Interface: `execute(params) -> StructuredResult | ToolUnavailableError`
- All adapters (MCP, CLI, API, Library) implement this interface
- Agent code calls adapters, never tools directly

**D-003: Use SARIF as Primary Normalization Format**
- Rationale: SARIF v2.1.0 is OASIS standard, supported by most security tools, and includes severity, location, rule metadata, and fix suggestions
- Implementation: SARIF parser as shared component; custom normalizers for non-SARIF tools
- Finding schema (common internal format) is serializable to/from SARIF

**D-004: Enforce Standalone Capability (R-012)**
- Rationale: Tools may be unavailable due to licensing, infrastructure, or network constraints
- Implementation: Three-level degradation (full tools -> partial tools -> standalone)
- Every agent capability must work at Level 2 (standalone) with reduced evidence quality
- Tool availability checked at execution time, not design time

**D-005: Implement Strict Security Controls**
- Rationale: Security tools can cause damage (active scanning, exploitation)
- Controls: Command allowlists, subprocess sandboxing, credential scoping, output sanitization
- No shell=True, no unsanitized input to commands
- Credentials never in agent context window

#### Implementation Priority

| Priority | Component | Effort | Value |
|----------|-----------|--------|-------|
| P0 | Common Adapter Interface + Finding Schema | Medium | Foundation for all integration |
| P0 | Standalone agent logic (no tools) | High | Core skill functionality |
| P1 | SARIF parser + normalization layer | Medium | Cross-tool finding correlation |
| P1 | CLI adapters: Nmap, Semgrep, Trivy, Nuclei | Medium | Highest-ROI tool coverage |
| P2 | MCP server evaluation (existing servers) | Low | Leverage community work |
| P2 | API adapters: ZAP, SonarQube | Medium | Platform integration |
| P3 | Custom MCP servers for priority tools | High | Native Claude Code integration |
| P3 | Library adapters: Impacket, pymetasploit3 | Medium | Deep protocol access |

#### Key Constraints

1. **R-012 Compliance**: Skills MUST work without any tools. Tool integration is enhancement, not dependency.
2. **Security**: All tool execution must be sandboxed. No credential exposure to agent context.
3. **Idempotency**: Tool operations should be repeatable where possible. Active exploitation requires explicit user authorization.
4. **Timeout Management**: All tool operations have explicit timeouts. Long-running operations (Hashcat, large Nmap scans) must be handled asynchronously.
5. **Output Validation**: All tool output is schema-validated before agent consumption. Prompt injection via tool output is a documented MCP attack vector.
