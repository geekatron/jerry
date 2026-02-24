# C-001: Offensive Tool Ecosystem Survey

> Stream C: Tool Integration | PROJ-010 Cyber Ops | Phase 1 Research

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | High-level findings and strategic implications |
| [L1: Key Findings](#l1-key-findings) | Structured findings by tool category |
| [L2: Detailed Analysis](#l2-detailed-analysis) | Per-tool deep dive with API details |
| [Evidence and Citations](#evidence-and-citations) | Dated sources, categorized |
| [Recommendations](#recommendations) | Priority tools and adapter architecture |

---

## L0: Executive Summary

The offensive security tool ecosystem provides substantial automation surfaces for agentic integration. Tools range from fully API-driven platforms (Metasploit RPC, Burp Suite REST/GraphQL, BloodHound CE REST API) to CLI-centric utilities (Nmap, Hashcat, NetExec) that require output parsing adapters. The most promising integration targets are Metasploit (via pymetasploit3 or JSON-RPC), Nuclei (YAML template engine with structured JSON output), and BloodHound CE (REST API with Neo4j query backend). Cobalt Strike's Aggressor scripting and Impacket's Python library offer direct programmatic access but require careful scoping due to their operational sensitivity. The "standalone capable" design principle (R-012) is achievable: agents can perform reasoning, planning, and reporting without tool access, while tools augment with real-time data collection, exploitation, and validation capabilities.

---

## L1: Key Findings

### Finding 1: Three Integration Tiers Emerge

Offensive tools fall into three natural tiers based on agentic integration feasibility:

- **Tier 1 -- API-Native** (Metasploit RPC, Burp Suite REST/GraphQL, BloodHound CE REST): These expose structured APIs with authentication, session management, and JSON/XML responses. They are the highest-value integration targets.
- **Tier 2 -- Structured CLI** (Nuclei, Nmap, Hashcat, NetExec): These are CLI-driven but produce structured output (JSON, XML, YAML). They require CLI adapter wrappers but the output is machine-parseable.
- **Tier 3 -- Programmatic Library** (Impacket, pymetasploit3): Python libraries offering direct protocol-level access. Integration is via Python import rather than API/CLI wrapping.

### Finding 2: Existing MCP Security Servers Validate the Pattern

Multiple MCP server implementations for security tools already exist on GitHub (as of 2025-2026):
- **mcp-for-security** (cyproxio): Wraps SQLMap, FFUF, Nmap, Masscan
- **pentest-mcp** (DMontgomery40): Wraps Nmap, GoBuster, Nikto, JtR, Hashcat
- **hexstrike-ai**: 150+ cybersecurity tools wrapped as MCP servers
- **sast-mcp**: Integrates multiple SAST tools with Claude Code
- **pentestMCP**: 20+ security assessment utilities via MCP

This validates that CLI-to-MCP wrapping is a proven pattern for security tools.

### Finding 3: Output Format Standardization Is Mixed

- Nmap: XML (well-structured, mature parsers exist)
- Nuclei: JSON (native, well-structured)
- Metasploit: JSON-RPC responses (structured)
- Burp Suite: JSON/HTML reports, GraphQL responses
- BloodHound: JSON (REST API), Cypher query results
- Hashcat/JtR: Plain text (requires custom parsing)
- NetExec: Structured text (semi-parseable)
- Responder: Log files (unstructured)

### Finding 4: Authentication Complexity Varies Significantly

- Metasploit: Token-based (msfrpcd generates temporary tokens)
- Burp Suite: API key (configured per-instance)
- BloodHound CE: Session-based (JWT tokens)
- Cobalt Strike: Team server authentication + Aggressor scripting context
- Most CLI tools: No authentication (local execution)

---

## L2: Detailed Analysis

### Tool Inventory

| Tool | API Type | Automation Level | Input Format | Output Format | Auth | Agentic Feasibility |
|------|----------|-----------------|--------------|---------------|------|---------------------|
| Metasploit | JSON-RPC / MessagePack RPC | High | JSON-RPC calls | JSON responses | Token (msfrpcd) | HIGH -- full programmatic control via pymetasploit3 or direct RPC |
| Burp Suite Pro | REST API | Medium | HTTP requests | JSON, HTML reports | API Key | MEDIUM -- requires licensed instance, API key management |
| Burp Suite DAST (Enterprise) | REST + GraphQL API | High | HTTP/GraphQL | JSON, SARIF | API Key + OAuth | HIGH -- scheduled scans, CI/CD integration, GraphQL preferred for new integrations |
| Nmap | CLI | High (via wrappers) | CLI flags | XML, grepable, normal text | None (local) | HIGH -- excellent XML output, mature Python parsers (libnmap, python-nmap) |
| BloodHound CE | REST API + Neo4j Cypher | High | HTTP requests, Cypher queries | JSON | JWT session token | HIGH -- REST API for data queries, Neo4j for graph traversal |
| Nuclei | CLI + Template Engine | High | YAML templates, CLI flags | JSON, SARIF, Markdown | None (local), API key (Cloud) | HIGH -- structured YAML templates, JSON output, AI template generation |
| Cobalt Strike | Aggressor Script + BOFs | Medium | Sleep scripting language, C (BOFs) | Script-dependent | Team server auth | LOW -- proprietary, requires active C2 infrastructure, licensing constraints |
| Impacket | Python library | High | Python API calls | Python objects, stdout | N/A (library) | HIGH -- direct Python integration, comprehensive protocol support |
| NetExec | CLI | Medium | CLI flags | Structured text, DB storage | None (local) | MEDIUM -- text output requires parsing, but protocol coverage is excellent |
| Responder | CLI | Low | CLI flags | Log files | None (local) | LOW -- passive listener, unstructured output, requires network position |
| Hashcat | CLI | Medium | CLI flags, rule files | Text (cracked passwords) | None (local) | MEDIUM -- GPU-dependent, long-running, text output needs parsing |
| John the Ripper | CLI | Medium | CLI flags, rule files | Text (cracked passwords) | None (local) | MEDIUM -- similar to Hashcat, rule engine compatible |

### Per-Tool Deep Dive

#### Metasploit Framework

**API Surface:**
- **JSON-RPC endpoint**: `/api/` path exposes all MSF RPC v1.0 methods via JSON-RPC over HTTP/HTTPS
- **MessagePack RPC**: Original binary protocol on port 55553 (msfrpcd default)
- **pymetasploit3**: Python automation library providing MsfRpcClient with segmented management modules (auth, consoles, core, db, jobs, modules, plugins, sessions)

**Key Automation Capabilities:**
- Module search, configuration, and execution (exploits, auxiliaries, post-exploitation)
- Session management (list, interact, read/write to shells/meterpreter)
- Database integration (hosts, services, vulnerabilities, credentials)
- Console creation and command execution
- Job management (background tasks)
- Plugin loading and management

**Integration Pattern:**
```
Agent -> pymetasploit3 -> msfrpcd (JSON-RPC) -> Metasploit Framework
                                              -> PostgreSQL (data store)
```

**Agentic Feasibility: HIGH**
- Full programmatic control over the entire framework
- Structured JSON responses for all operations
- Session interaction supports command execution with timeout handling
- PowerShell script import and execution supported
- Database queries return structured host/service/vulnerability data

**Key Limitation:** Requires running msfrpcd daemon or msfconsole with msgrpc plugin loaded. Infrastructure setup is a prerequisite.

#### Burp Suite (Professional + DAST/Enterprise)

**API Surface:**
- **Professional REST API**: Enabled via Settings > Suite > REST API, requires API key, default endpoint configurable
- **DAST (Enterprise) REST API**: Full scan management, scheduling, reporting
- **DAST GraphQL API**: Recommended for new integrations, broadest functionality
- **Montoya Extension API**: Java-based extension framework, now includes built-in AI/LLM support (2025.2+)

**Key Automation Capabilities:**
- Scan initiation, monitoring, and results retrieval
- Portfolio-level scheduled scanning (daily/weekly/monthly)
- CI/CD pipeline integration (Jenkins, TeamCity)
- SARIF output for integration with code scanning platforms
- Extension development with LLM integration via Montoya API

**Integration Pattern:**
```
Agent -> REST/GraphQL API -> Burp Suite Instance -> Target Application
                          -> Scan Results (JSON/SARIF)
```

**Agentic Feasibility: MEDIUM-HIGH**
- Enterprise/DAST edition offers the richest API surface
- Professional edition REST API is more limited but functional
- API key authentication is straightforward
- GraphQL API provides flexible querying of results
- AI integration in Montoya API (2025+) opens extension-based patterns

**Key Limitation:** Commercial licensing required. Professional edition has limited API compared to Enterprise/DAST.

#### Nmap

**API Surface:**
- **CLI with structured output**: `-oX` (XML), `-oG` (grepable), `-oN` (normal)
- **libnmap (Python)**: NmapProcess (execution) + NmapParser (XML parsing) + NmapDiff (comparison)
- **python-nmap**: Alternative Python wrapper for nmap execution and result parsing
- **NSE (Nmap Scripting Engine)**: Lua-based scripts for extended scanning capabilities

**Key Automation Capabilities:**
- Port scanning with service/version detection
- OS fingerprinting
- NSE script execution (vuln detection, brute force, discovery)
- XML output with complete host, port, service, script result data
- Scan diffing for change detection

**Integration Pattern:**
```
Agent -> libnmap.NmapProcess -> nmap binary -> XML output
      -> libnmap.NmapParser -> NmapReport/NmapHost/NmapService objects
```

**Agentic Feasibility: HIGH**
- XML output is comprehensive and well-structured
- libnmap provides both execution and parsing in a single library
- NmapParser can parse partial XML fragments (individual hosts/ports)
- NSE scripts extend scanning beyond basic port/service discovery
- Mature ecosystem with multiple Python parsing libraries

**Key Limitation:** Scan duration can be long for large networks. Requires appropriate network access and permissions.

#### BloodHound Community Edition

**API Surface:**
- **REST API**: HTTP endpoints for data queries, user management, upload
- **Neo4j Cypher**: Direct graph database queries for attack path analysis
- **SharpHound/AzureHound**: Data collectors (C#/.NET) that feed BloodHound
- **bloodhound-cli (Python)**: CLI tool supporting both Legacy and CE backends
- **Blade (Go)**: CLI tool using bloodhound-go-sdk and neo4j-go-driver

**Key Automation Capabilities:**
- Attack path querying and shortest-path analysis
- Domain enumeration data upload and management
- Custom Cypher queries for bespoke analysis
- Data export and reporting
- Integration with pentesting workflows via REST API

**Integration Pattern:**
```
SharpHound/AzureHound -> Data Collection -> BloodHound CE
Agent -> REST API / Neo4j Cypher -> Attack Path Analysis
      -> bloodhound-cli (Python) -> Structured Output
```

**Agentic Feasibility: HIGH**
- REST API provides structured JSON responses
- Cypher queries enable sophisticated graph analysis
- Python CLI tools available for programmatic interaction
- Attack path data is inherently structured (nodes + edges)
- Active development community with automation-focused tooling

**Key Limitation:** Requires SharpHound data collection (which requires domain access) before analysis is meaningful.

#### Nuclei (ProjectDiscovery)

**API Surface:**
- **CLI**: Feature-rich with JSON/SARIF/Markdown output options
- **YAML Template Engine**: Declarative vulnerability definitions
- **Template Registry**: Community-curated templates (9000+ as of late 2025)
- **AI Template Generation**: `-ai` flag for natural language to template conversion
- **ProjectDiscovery Cloud Platform**: API for template management and scan orchestration

**Key Automation Capabilities:**
- Template-based vulnerability scanning across HTTP, DNS, network, file protocols
- Custom template authoring in YAML DSL
- AI-powered template generation from CVE descriptions
- JSON output with structured vulnerability findings
- Template auto-update from community registry
- Severity-based filtering and reporting

**Integration Pattern:**
```
Agent -> nuclei CLI -> YAML Templates -> Target Scanning
      -> JSON Output -> Structured Findings
      -> AI Flag -> Natural Language -> Template Generation
```

**Agentic Feasibility: HIGH**
- YAML templates are agent-writable (an agent can generate scanning templates)
- JSON output is structured and parseable
- AI template generation aligns naturally with LLM-based agents
- Template registry provides extensive coverage without custom development
- Severity and tag filtering enable focused scanning

**Key Limitation:** Template quality varies in community contributions. Cloud features require ProjectDiscovery account.

#### Cobalt Strike

**API Surface:**
- **Aggressor Script**: Sleep-based scripting language for automation and customization
- **Beacon Object Files (BOFs)**: Compiled C programs executing within Beacon process
- **External C2**: Custom communication channels
- **Malleable C2 Profiles**: Traffic shaping configuration
- **Python Bridge**: Third-party bridge enabling Python-based automation

**Key Automation Capabilities:**
- Automated beacon task execution via Aggressor scripts
- Custom post-exploitation via BOFs
- Lateral movement automation
- Data extraction and operation decision-making
- Workflow customization and extension

**Integration Pattern:**
```
Agent -> Python Bridge / Aggressor Script -> Cobalt Strike Team Server
      -> Beacon -> Target Systems
```

**Agentic Feasibility: LOW**
- Proprietary commercial tool with strict licensing
- Requires active C2 infrastructure (team server)
- Aggressor scripting is a niche language (Sleep)
- Python bridge exists but is community-maintained
- Operational security concerns with automated C2 operations
- NOT recommended for automated agent integration due to safety implications

**Key Limitation:** Licensing cost, operational complexity, and the significant safety/legal implications of automated C2 operations make this unsuitable for general agentic integration.

#### Impacket

**API Surface:**
- **Python library**: Direct import and use of protocol implementations
- **Example scripts**: Standalone tools (secretsdump.py, smbexec.py, psexec.py, etc.)
- **Protocol classes**: SMB1-3, MSRPC, LDAP, Kerberos, MSSQL, etc.

**Key Automation Capabilities:**
- Low-level protocol access (SMB, MSRPC, LDAP, Kerberos, MSSQL)
- Authentication with passwords, hashes, tickets, and keys
- Remote command execution (PsExec, WMIExec, SMBExec, etc.)
- Credential extraction (secretsdump, DCSync)
- Active Directory interaction (LDAP queries, Kerberos operations)

**Integration Pattern:**
```
Agent -> Python import impacket -> Protocol Classes -> Target Systems
      -> Example Scripts (CLI) -> Text Output -> Parsing
```

**Agentic Feasibility: HIGH (as Python library)**
- Direct Python integration eliminates CLI parsing overhead
- Comprehensive protocol coverage for AD environments
- Well-maintained (Fortra/Core Security), active development
- 2025 updates include Windows Server 2025 LDAPS/LAPS support
- Can be imported directly into agent code

**Key Limitation:** Requires understanding of underlying protocols. Example scripts produce text output requiring parsing if used via CLI.

#### NetExec (formerly CrackMapExec)

**API Surface:**
- **CLI**: Rich command-line interface with protocol-specific subcommands
- **Module system**: Extensible via Python modules
- **Database**: SQLite backend for storing results
- **Protocol support**: SMB, LDAP, WinRM, RDP, MSSQL, SSH, FTP, VNC

**Key Automation Capabilities:**
- Multi-protocol credential validation (spray, brute force)
- Command execution across multiple hosts
- Enumeration (shares, users, groups, sessions)
- BloodHound integration (data collection)
- Module-based extensibility for custom operations

**Integration Pattern:**
```
Agent -> nxc CLI -> Protocol Operations -> Target Network
      -> SQLite DB -> Result Queries
      -> Text Output -> Parsing
```

**Agentic Feasibility: MEDIUM**
- Excellent protocol coverage and enumeration capabilities
- Module system enables extensibility
- SQLite database provides structured result storage
- Text output is semi-structured but requires parsing
- Active development and community support

**Key Limitation:** Primary output is text-based, requiring custom parsers. No formal API beyond CLI.

#### Responder

**API Surface:**
- **CLI only**: Command-line execution with interface binding
- **Log files**: Captured credentials written to log directory
- **Analyze mode**: `-A` flag for passive monitoring without poisoning

**Agentic Feasibility: LOW**
- Passive network listener requiring specific network position
- Unstructured log file output
- Limited automation surface beyond start/stop
- Real-time nature conflicts with request/response agent patterns
- Better suited as infrastructure component than agent-controlled tool

#### Hashcat / John the Ripper

**API Surface:**
- **Hashcat CLI**: GPU-accelerated password cracking with rule engine
- **John the Ripper CLI**: CPU-focused with extensive format support
- **Rule engines**: Compatible rule syntax between tools
- **Hashtopolis**: Distributed management platform with web API
- **Status output**: Hashcat supports `--status-json` for machine-readable progress

**Agentic Feasibility: MEDIUM**
- Long-running operations (minutes to days) conflict with synchronous agent patterns
- Hashcat `--status-json` provides structured progress monitoring
- Rule engine is text-based and agent-writable
- Hashtopolis API enables distributed job management
- Results are simple text (hash:password pairs)

**Key Limitation:** GPU dependency for Hashcat, long execution times, and the fundamentally batch-processing nature of password cracking.

---

## Evidence and Citations

### Primary Sources (accessed 2026-02-22)

**Metasploit:**
- [Rapid7 RPC API Documentation](https://docs.rapid7.com/metasploit/rpc-api/) -- Official RPC API reference
- [Metasploit JSON-RPC Documentation](https://docs.metasploit.com/docs/using-metasploit/advanced/RPC/how-to-use-metasploit-json-rpc.html) -- JSON-RPC endpoint details
- [pymetasploit3 (GitHub)](https://github.com/DanMcInerney/pymetasploit3) -- Python automation library
- [Coalfire pymetasploit3](https://coalfire.com/the-coalfire-blog/pymetasploit3-metasploit-automation-library) -- Usage documentation

**Burp Suite:**
- [PortSwigger REST API Documentation](https://portswigger.net/burp/documentation/enterprise/api-documentation/rest) -- Enterprise REST API
- [PortSwigger REST API Settings](https://portswigger.net/burp/documentation/desktop/settings/suite/rest-api) -- Professional REST API config
- [PortSwigger API Overview](https://portswigger.net/burp/documentation/enterprise/user-guide/api-documentation/api-overview) -- GraphQL API recommendation
- [Burp Suite 2025.2 AI Integration](https://gbhackers.com/burp-suite-professional-community-2025-2/) -- Montoya API AI features

**Nmap:**
- [Nmap Output Documentation](https://nmap.org/book/man-output.html) -- Official output format reference
- [libnmap Documentation](https://libnmap.readthedocs.io/en/latest/parser.html) -- Python parser library
- [python-nmap (PyPI)](https://pypi.org/project/python-nmap/) -- Alternative Python wrapper

**BloodHound CE:**
- [BloodHound GitHub (SpecterOps)](https://github.com/SpecterOps/BloodHound) -- Official repository
- [BloodHound CE Ultimate Guide](https://m4lwhere.medium.com/the-ultimate-guide-for-bloodhound-community-edition-bhce-80b574595acf) -- REST API usage
- [bloodhound-cli (PyPI)](https://pypi.org/project/bloodhound-cli/) -- Python CLI tool
- [Blade CLI Tool](https://cybercx.com.au/blog/introducing-blade-streamlined-command-line-tool-for-bloodhound-and-neo4j/) -- Go CLI for BloodHound CE + Neo4j

**Nuclei:**
- [Nuclei GitHub (ProjectDiscovery)](https://github.com/projectdiscovery/nuclei) -- Official repository
- [Nuclei Template Documentation](https://docs.projectdiscovery.io/templates/introduction) -- Template authoring guide
- [AI Template Generation Blog](https://projectdiscovery.io/blog/future-of-automating-nuclei-templates-with-ai) -- AI-powered template creation
- [Nuclei Templates November 2025](https://projectdiscovery.io/blog/nuclei-templates-november-2025) -- Recent template releases

**Cobalt Strike:**
- [Aggressor Script Documentation](https://hstechdocs.helpsystems.com/manuals/cobaltstrike/current/userguide/content/topics/welcome_cs-scripting.htm) -- Official scripting reference
- [BOF Documentation](https://hstechdocs.helpsystems.com/manuals/cobaltstrike/current/userguide/content/topics/beacon-object-files_with-aggressor-script.htm) -- Beacon Object Files guide

**Impacket:**
- [Impacket GitHub (Fortra)](https://github.com/fortra/impacket) -- Official repository
- [Impacket PyPI](https://pypi.org/project/impacket/) -- Package with protocol details
- [Impacket Core Security Page](https://www.coresecurity.com/core-labs/impacket) -- Protocol implementation list

**NetExec:**
- [NetExec Cheat Sheet (StationX)](https://www.stationx.net/netexec-cheat-sheet/) -- 2026 command reference
- [NetExec Introduction (BHIS)](https://www.blackhillsinfosec.com/getting-started-with-netexec/) -- Getting started guide
- [NetExec Automation Gist](https://gist.github.com/VasanthVanan/a55048e34938ebcdbfb6ff9a6a13bfcb) -- Automation patterns

**Responder:**
- [Responder GitHub (SpiderLabs)](https://github.com/SpiderLabs/Responder) -- Official repository
- [Kali Linux Responder](https://www.kali.org/tools/responder/) -- Tool documentation

**Hashcat / John the Ripper:**
- [Hashcat Rule-Based Attack](https://hashcat.net/wiki/doku.php?id=rule_based_attack) -- Rule engine documentation
- [Hashcat Rules Engine (GitHub)](https://github.com/llamasoft/HashcatRulesEngine) -- Standalone rule engine
- [John the Ripper 2025 Advanced Usage](https://www.onlinehashcrack.com/guides/security-tools/john-the-ripper-2025-advanced-usage.php) -- Current capabilities

**MCP Security Servers:**
- [mcp-for-security (GitHub)](https://github.com/cyproxio/mcp-for-security) -- Nmap, SQLMap, FFUF, Masscan MCP servers
- [pentest-mcp (GitHub)](https://github.com/DMontgomery40/pentest-mcp) -- Professional pentesting MCP server
- [hexstrike-ai (GitHub)](https://github.com/0x4m4/hexstrike-ai) -- 150+ cybersecurity tools via MCP
- [pentestMCP (GitHub)](https://github.com/ramkansal/pentestMCP) -- 20+ security tools via MCP

---

## Recommendations

### Priority Integration Targets (Tier 1 -- Implement First)

1. **Nmap** -- Highest ROI. Structured XML output, mature Python parsers (libnmap), universal applicability in reconnaissance. CLI adapter pattern with XML parsing.

2. **Nuclei** -- Template-based scanning with JSON output. Agent can both consume results AND generate templates (YAML DSL is LLM-friendly). CLI adapter with JSON parsing.

3. **BloodHound CE** -- REST API provides structured attack path data. Critical for Active Directory assessments. REST API adapter pattern.

### Secondary Integration Targets (Tier 2 -- Implement When Needed)

4. **Metasploit** -- Full framework access via pymetasploit3. High capability but higher complexity. Python library integration pattern.

5. **Impacket** -- Direct Python library for AD protocol operations. Complements BloodHound and NetExec. Python library integration pattern.

6. **NetExec** -- Broad protocol coverage for credential validation and enumeration. CLI adapter with text parsing + SQLite query.

### Deferred (Tier 3 -- Not Recommended for Initial Integration)

7. **Burp Suite** -- Requires commercial licensing; ZAP provides open-source alternative with comparable API
8. **Cobalt Strike** -- Proprietary, operational safety concerns, not suitable for automated agent control
9. **Responder** -- Passive tool, unstructured output, limited automation surface
10. **Hashcat/JtR** -- Long-running batch operations; better as infrastructure than agent-controlled tools

### Recommended Adapter Architecture

```
+------------------+     +-------------------+     +------------------+
|                  |     |                   |     |                  |
|   Jerry Agent    |---->|  Tool Adapter     |---->|  Security Tool   |
|   (Standalone    |     |  Layer            |     |  (Optional)      |
|    Capable)      |<----|                   |<----|                  |
|                  |     |  - CLI Adapter    |     |  - Nmap          |
+------------------+     |  - API Adapter    |     |  - Nuclei        |
                         |  - Library Adapter|     |  - BloodHound    |
                         |  - MCP Server     |     |  - Metasploit    |
                         +-------------------+     +------------------+
                                |
                         +-------------------+
                         |  Output Parser    |
                         |  - XML (Nmap)     |
                         |  - JSON (Nuclei)  |
                         |  - SARIF          |
                         |  - Text (fallback)|
                         +-------------------+
```

**Design Principles:**
- Each adapter implements a common interface: `execute(params) -> StructuredResult`
- Adapters handle authentication, timeout, error recovery
- Output parsers normalize tool-specific formats to a common finding schema
- Agent logic operates on normalized findings, NOT raw tool output
- Agent MUST be fully functional without any tools (R-012 standalone capable)
- Tools augment agent reasoning with real-time data, not replace it
