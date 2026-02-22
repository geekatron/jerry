# Threat Framework Analysis: MITRE + OWASP + NIST

> Agent: ps-researcher-002
> Phase: 1 (Deep Research)
> Pipeline: PS (Problem-Solving)
> Status: COMPLETE
> Date: 2026-02-22

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary-l0) | 5-bullet overview of total landscape |
| [MITRE ATT&CK Enterprise Analysis](#mitre-attck-enterprise-analysis-l1) | 14 tactics mapped to agentic relevance |
| [MITRE ATLAS Analysis](#mitre-atlas-analysis-l1) | 15 AI-specific tactics, 14 new agent techniques |
| [MITRE ATT&CK Mobile Analysis](#mitre-attck-mobile-analysis-l1) | Mobile agent deployment risks |
| [OWASP LLM Top 10 (2025) Analysis](#owasp-llm-top-10-2025-analysis-l1) | LLM01-LLM10 per-item analysis |
| [OWASP Agentic Top 10 (2026) Analysis](#owasp-agentic-top-10-2026-analysis-l1----critical-section) | ASI01-ASI10 deep analysis with Jerry mapping |
| [OWASP API Security Top 10 Analysis](#owasp-api-security-top-10-analysis-l1) | API1-API10 MCP surface mapping |
| [OWASP Web Top 10 Analysis](#owasp-web-top-10-analysis-l1) | A01-A10 agent web interaction relevance |
| [NIST AI RMF (600-1) Analysis](#nist-ai-rmf-600-1-analysis-l1) | 4 functions, 12 GenAI risk categories |
| [NIST CSF 2.0 Analysis](#nist-csf-20-analysis-l1) | 6 functions, IR 8596 AI profile overlay |
| [NIST SP 800-53 Analysis](#nist-sp-800-53-analysis-l1) | 20 control families mapped to agentic needs |
| [Cross-Framework Mapping](#cross-framework-mapping-l2) | Unified taxonomy, overlaps, gaps |
| [Agentic Threat Priority Matrix](#agentic-threat-priority-matrix) | Consolidated priority ranking |
| [Citations](#citations) | All sources with authority classification |

---

## Executive Summary (L0)

- **Total scope consumed:** 10 security framework scopes across 3 standards bodies (MITRE, OWASP, NIST), yielding 14 ATT&CK Enterprise tactics, 15 ATLAS AI-specific tactics with 66 techniques (including 14 new agent-specific techniques from Oct 2025), 12 ATT&CK Mobile tactics, 40 OWASP risk items across 4 Top 10 lists, 20 NIST 800-53 control families with 1,007 controls, 6 CSF 2.0 functions with 22 categories, and 12 GenAI risk categories from AI 600-1.
- **Most critical framework:** OWASP Agentic Top 10 (2026) is the single most directly applicable framework for Jerry, mapping ASI01-ASI10 to specific Jerry attack surfaces including prompt injection via tool results (ASI01), MCP tool misuse (ASI02), orchestrator-worker privilege inheritance (ASI03), delegated trust boundary violations in multi-agent handoffs (ASI04), and context/memory poisoning of L2 re-injection markers (ASI06).
- **Key threat categories for agentic systems:** (1) Prompt injection (direct and indirect), (2) Tool/MCP supply chain compromise, (3) Privilege escalation through delegation chains, (4) Memory and context manipulation, (5) Cascading failures in multi-agent workflows, (6) Identity and access mismanagement, (7) Rogue agent persistence.
- **Critical gap identified:** No existing framework fully addresses the specific threat of constitutional governance bypass through context rot -- Jerry's L1-L5 enforcement architecture addresses a threat surface that falls between ATLAS's "AI Agent Context Poisoning" (AML.T0080) and OWASP's "Memory and Context Poisoning" (ASI06), but neither framework explicitly models the degradation of behavioral constraints as context fills.
- **Industry consensus validated:** Defense-in-depth is the only viable strategy; 12 published defenses were bypassed with >90% success rate using adaptive attacks (joint OpenAI/Anthropic/Google DeepMind study). Jerry's 5-layer enforcement architecture (L1-L5) aligns with Google DeepMind's 5-layer defense and Microsoft Agent 365's control plane architecture.

---

## MITRE ATT&CK Enterprise Analysis (L1)

### Tactics Overview (14)

The ATT&CK Enterprise Matrix defines 14 tactics representing adversary objectives during an attack lifecycle. While designed for traditional enterprise IT, many tactics have direct analogs in agentic AI systems.

| # | Tactic ID | Tactic Name | Description | Agentic Relevance |
|---|-----------|-------------|-------------|-------------------|
| 1 | TA0043 | Reconnaissance | Information gathering about targets prior to attack | HIGH -- Agent configurations, SKILL.md files, CLAUDE.md rules, MCP server definitions are discoverable |
| 2 | TA0042 | Resource Development | Establishing infrastructure and capabilities | MEDIUM -- Adversaries develop malicious MCP servers, poisoned prompt templates, or adversarial inputs |
| 3 | TA0001 | Initial Access | Gaining entry into target systems | CRITICAL -- Prompt injection (direct/indirect) is the primary initial access vector for agents |
| 4 | TA0002 | Execution | Running malicious code or commands | CRITICAL -- Agent tool invocation executes commands; Bash, Write, Edit tools enable arbitrary execution |
| 5 | TA0003 | Persistence | Maintaining access after initial compromise | HIGH -- Poisoned memory, modified agent configs, corrupted context persist across sessions |
| 6 | TA0004 | Privilege Escalation | Obtaining higher-level permissions | CRITICAL -- Agents inherit user credentials; orchestrator-worker delegation enables privilege inheritance |
| 7 | TA0005 | Defense Evasion | Avoiding security protections | HIGH -- Context rot degrades L1 behavioral rules; adversaries craft inputs to bypass L2 re-injection |
| 8 | TA0006 | Credential Access | Obtaining authentication credentials | HIGH -- API keys, MCP server tokens, SSH keys in agent context; RAG credential harvesting |
| 9 | TA0007 | Discovery | Gathering information about environment | HIGH -- Agents can discover system architecture, file structures, tool capabilities via Read/Glob/Grep |
| 10 | TA0008 | Lateral Movement | Accessing additional systems | MEDIUM -- Multi-agent handoffs enable movement between agent contexts; MCP servers bridge systems |
| 11 | TA0009 | Collection | Gathering data of interest | HIGH -- Agents have broad file read access; tool results contain sensitive data |
| 12 | TA0011 | Command and Control | Communicating with compromised systems | LOW -- Less directly applicable; agent-to-API communication is the nearest analog |
| 13 | TA0010 | Exfiltration | Removing data from target environment | HIGH -- Agents can exfiltrate via WebFetch, Bash (curl), or tool invocations that write to external services |
| 14 | TA0040 | Impact | Disrupting or modifying systems | CRITICAL -- Agents with Write/Edit/Bash can modify files, delete data, corrupt configurations |

### Techniques Most Relevant to Agentic Systems

| ATT&CK Technique | ID | Agentic Analog | Relevance |
|-------------------|----|----------------|-----------|
| Phishing (Spearphishing Attachment) | T1566.001 | Indirect prompt injection via document content | CRITICAL |
| Command and Scripting Interpreter | T1059 | Agent Bash tool execution of injected commands | CRITICAL |
| Exploitation of Remote Services | T1210 | MCP server exploitation, tool API abuse | HIGH |
| Valid Accounts | T1078 | Agent inheriting user credentials/tokens | HIGH |
| Data from Local System | T1005 | Agent Read tool accessing sensitive files | HIGH |
| Modify System Process | T1543 | Modifying agent configuration files | HIGH |
| Obtain Capabilities: AI | T1588.007 | Adversary acquiring AI tools/models for attacks | MEDIUM |
| Supply Chain Compromise | T1195 | Compromised MCP servers, poisoned dependencies | HIGH |
| Exfiltration Over Web Service | T1567 | Agent using WebFetch to send data externally | HIGH |
| Account Manipulation | T1098 | Agent modifying permissions or access controls | HIGH |

### Agentic Attack Surface Mapping

| ATT&CK Category | Jerry Component | Attack Vector | Existing Mitigation |
|------------------|-----------------|---------------|---------------------|
| Initial Access | Agent input processing | Prompt injection via user input, tool results, file content | L2 re-injection, input validation guardrails |
| Execution | Bash, Write, Edit tools | Injected commands executed via tool calls | Tool tier restrictions (T1-T5), H-35 forbidden actions |
| Persistence | .context/rules/, agent definitions | Poisoned rule files persist malicious instructions | L5 CI verification, H-19 governance escalation |
| Privilege Escalation | Orchestrator-worker delegation | Worker agent inheriting orchestrator's full permissions | H-01/P-003 single-level nesting, tool tier enforcement |
| Defense Evasion | Context window | L1 rules degrade with context fill; crafted inputs bypass L2 | AE-006 context fill monitoring, L3 deterministic gating |
| Discovery | Glob, Grep, Read tools | Agent reveals system structure, configurations, secrets | Output filtering guardrails, T1 read-only restrictions |
| Exfiltration | WebFetch, Bash (network) | Data sent to external endpoints via agent tools | Network isolation, domain allowlists (sandboxing) |

---

## MITRE ATLAS Analysis (L1)

### Tactics Overview (15)

MITRE ATLAS (Adversarial Threat Landscape for AI Systems) extends ATT&CK with AI/ML-specific tactics. It inherits 13 ATT&CK tactics adapted for AI contexts and adds 2 unique AI-specific tactics: ML Model Access and ML Attack Staging.

| # | Tactic ID | Tactic Name | Description | Agentic Relevance |
|---|-----------|-------------|-------------|-------------------|
| 1 | AML.TA0001 | Reconnaissance | Discover ML artifacts, model ontology, active scanning | HIGH -- Agent configs, tool definitions, prompt templates are discoverable |
| 2 | AML.TA0002 | Resource Development | Acquire tools and capabilities for adversarial ML attacks | MEDIUM -- Develop malicious prompts, proxy models, adversarial inputs |
| 3 | AML.TA0003 | Initial Access | Supply chain compromise and prompt injection | CRITICAL -- Primary attack vector for agent systems |
| 4 | AML.TA0004 | ML Model Access | Gain access to target ML models via APIs or artifacts | HIGH -- API access to LLM enables prompt injection, model probing |
| 5 | AML.TA0005 | Execution | User execution and LLM plugin compromise | CRITICAL -- Agent tool execution is the primary action mechanism |
| 6 | AML.TA0006 | Persistence | Modify AI agent configurations for persistent access | HIGH -- Agent config files, memory stores, context persist changes |
| 7 | AML.TA0007 | Privilege Escalation | Exploit ML systems for elevated access | HIGH -- Delegation chains, credential inheritance |
| 8 | AML.TA0008 | Defense Evasion | Adversarial perturbation and prompt extraction | HIGH -- Crafted inputs bypass safety filters and constitutional rules |
| 9 | AML.TA0009 | Credential Access | Extract credentials from AI agent configurations | CRITICAL -- MCP server tokens, API keys in agent context |
| 10 | AML.TA0010 | Discovery | Enumerate AI agent configurations and capabilities | HIGH -- Tool definitions, activation triggers, embedded knowledge |
| 11 | AML.TA0011 | Collection | Data extraction from AI services and RAG databases | HIGH -- Agent-accessible data stores, file systems |
| 12 | AML.TA0012 | ML Attack Staging | Data poisoning and backdoor insertion into models | MEDIUM -- Less directly applicable to prompt-based agents |
| 13 | AML.TA0013 | Exfiltration | Data theft via inference APIs and agent tools | HIGH -- Tool invocation-based exfiltration |
| 14 | AML.TA0014 | Impact | Denial of service and model evasion attacks | HIGH -- Token exhaustion, agent loops, destructive actions |
| 15 | AML.TA0015 | Command and Control | Remote control of compromised AI systems | LOW -- Less applicable to single-context agent execution |

### Agent-Specific Techniques (14 new, Oct 2025)

In October 2025, MITRE ATLAS collaborated with Zenity Labs to add 14 new techniques and sub-techniques specifically for AI agents and GenAI systems. These represent the most current and directly applicable threat taxonomy for agentic systems.

| Technique ID | Name | Description | Jerry Relevance |
|--------------|------|-------------|-----------------|
| AML.T0080 | AI Agent Context Poisoning | Manipulate context used by agent's LLM to influence responses or actions | CRITICAL -- Directly targets L1/L2 context; poisoned tool results could override constitutional rules |
| AML.T0080.000 | Context Poisoning: Memory | Alter long-term memory to persist malicious changes across sessions | HIGH -- Memory-Keeper stored contexts could be poisoned |
| AML.T0080.001 | Context Poisoning: Thread | Inject malicious instructions into chat thread for session-duration changes | CRITICAL -- Single-session context injection via tool results |
| AML.T0081 | Modify AI Agent Configuration | Change agent configuration files for persistent malicious behavior | CRITICAL -- Modifying .context/rules/, agent definitions, SKILL.md files |
| AML.T0082 | RAG Credential Harvesting | Use LLM to search for credentials in RAG databases | HIGH -- Credentials in project files, configs, or Memory-Keeper |
| AML.T0083 | Credentials from AI Agent Config | Extract credentials from agent configuration files | HIGH -- MCP server configs contain tokens, API keys |
| AML.T0084 | Discover AI Agent Configuration | Discover agent configuration, tools, services | HIGH -- Agent definitions, AGENTS.md, tool registries are readable |
| AML.T0084.000 | Discover: Embedded Knowledge | Discover data sources agents can access | HIGH -- File system, Memory-Keeper, Context7 sources |
| AML.T0084.001 | Discover: Tool Definitions | Identify available tools and capabilities | HIGH -- Tool lists in agent YAML, SKILL.md descriptions |
| AML.T0084.002 | Discover: Activation Triggers | Discover keywords/workflows triggering agent execution | HIGH -- mandatory-skill-usage.md trigger map is discoverable |
| AML.T0085 | Data from AI Services | Collect sensitive information from AI-enabled services | HIGH -- Agent-accessible services, databases, APIs |
| AML.T0085.000 | Data from AI Services: RAG | Prompt retrieval from RAG databases containing internal documents | MEDIUM -- Jerry doesn't use RAG but principle applies to Memory-Keeper |
| AML.T0085.001 | Data from AI Services: Agent Tools | Invoke agent tools to retrieve data from organizational APIs | HIGH -- Agent tools provide broad data access |
| AML.T0086 | Exfiltration via Agent Tool Invocation | Use prompts to invoke write-capable tools for data exfiltration | CRITICAL -- Bash, WebFetch, Write tools could exfiltrate data |

### Prompt Injection Taxonomy

ATLAS classifies prompt injection under Initial Access (AML.TA0003) with growing sub-technique granularity:

| Type | Description | Agentic Attack Surface |
|------|-------------|----------------------|
| Direct Prompt Injection | Adversary crafts input directly to manipulate LLM behavior | User messages, slash command arguments |
| Indirect Prompt Injection | Malicious instructions embedded in data the agent processes | File contents read via Read tool, WebFetch results, MCP server responses, tool output |
| Context Window Injection | Poisoning context through accumulated tool results | Long-running sessions where tool results push out constitutional rules |
| Configuration-Based Injection | Modifying agent config files to inject persistent instructions | .context/rules/ files, agent definition YAML, SKILL.md |

### AI Supply Chain Threats

| Threat Vector | ATLAS Mapping | Jerry-Specific Risk |
|---------------|---------------|---------------------|
| Malicious MCP Servers | AML.T0081 + Supply Chain | Poisoned MCP servers impersonate trusted tools, inject instructions |
| Compromised Dependencies | Supply Chain Compromise | Python packages (uv add), npm packages, model files |
| Poisoned Prompt Templates | AML.T0081 | Adversarial templates in .context/templates/ |
| Model Integrity | ML Attack Staging | Less relevant for API-based LLM consumption |

---

## MITRE ATT&CK Mobile Analysis (L1)

### Mobile Agent Deployment Risks

The ATT&CK Mobile Matrix covers 12 tactics across Android and iOS platforms. While designed for traditional mobile threats, several tactics become relevant when agents operate on or interact with mobile devices.

| # | Tactic ID | Tactic Name | Techniques | Agentic Mobile Relevance |
|---|-----------|-------------|------------|--------------------------|
| 1 | TA0027 | Initial Access | 8 | MEDIUM -- Mobile agent apps, deep links, app store supply chain |
| 2 | TA0041 | Execution | 4 | MEDIUM -- Mobile agent code execution, inter-process communication |
| 3 | TA0028 | Persistence | 8 | MEDIUM -- Persistent agent background processes, scheduled tasks |
| 4 | TA0029 | Privilege Escalation | 3 | HIGH -- Mobile agent escalating OS-level permissions |
| 5 | TA0030 | Defense Evasion | 17 | MEDIUM -- Agents masquerading as legitimate apps, code obfuscation |
| 6 | TA0031 | Credential Access | 6 | HIGH -- Keylogging, credential store access by agent apps |
| 7 | TA0032 | Discovery | 8 | MEDIUM -- Agent enumerating device capabilities, contacts, files |
| 8 | TA0033 | Lateral Movement | 2 | LOW -- Limited mobile lateral movement surface |
| 9 | TA0035 | Collection | 15 | HIGH -- Camera, microphone, location, contacts, files accessible to agents |
| 10 | TA0037 | Command and Control | 9 | MEDIUM -- Agent communication channels, C2 via standard protocols |
| 11 | TA0036 | Exfiltration | 2 | HIGH -- Data exfiltration via agent network access |
| 12 | TA0034 | Impact | 10 | MEDIUM -- Device wipe, data encryption, denial of service |

**Key mobile-agent threat scenarios:**

1. **Mobile agent supply chain:** Compromised agent SDKs or plugins distributed via app stores (maps to TA0027 Initial Access via Supply Chain).
2. **Sensor access abuse:** Mobile agents with camera, microphone, or location permissions can collect data beyond intended scope (maps to TA0035 Collection).
3. **BYOD agent isolation:** Employee devices running enterprise agents may lack proper sandboxing, enabling data leakage between personal and corporate contexts.
4. **Mobile MCP transport:** Agent-to-server communication over mobile networks may be more vulnerable to interception and manipulation.

**Overall Mobile Relevance to Jerry:** LOW-MEDIUM. Jerry currently operates as a CLI tool (Claude Code), not a mobile application. Mobile risks become relevant if Jerry agents are deployed in mobile contexts or interact with mobile APIs. The most transferable insights are around sandboxing (applicable to container isolation) and supply chain (applicable to MCP servers).

---

## OWASP LLM Top 10 (2025) Analysis (L1)

### Per-Item Analysis (LLM01-LLM10)

| ID | Name | Description | Agentic Relevance | Priority |
|----|------|-------------|-------------------|----------|
| LLM01 | Prompt Injection | Adversary crafts inputs to manipulate LLM behavior; includes direct injection (user input) and indirect injection (via external data sources, tool results, retrieved documents) | CRITICAL -- Primary attack vector. Agents process untrusted data from files, MCP servers, web content. Indirect injection is the dominant threat because agents consume diverse, untrusted data sources. | P1 |
| LLM02 | Sensitive Information Disclosure | LLM reveals system prompts, training data, PII, credentials, or internal state in responses | HIGH -- Agent context contains CLAUDE.md rules, constitutional constraints, MCP server tokens, project secrets. System prompt leakage exposes the entire governance architecture. | P2 |
| LLM03 | Supply Chain | Vulnerabilities in third-party components, pre-trained models, training data, plugin ecosystems | HIGH -- MCP servers are the primary supply chain attack surface for agents. Malicious MCP servers can inject instructions, exfiltrate data, or alter tool behavior. Python dependencies (via uv) are secondary. | P2 |
| LLM04 | Data and Model Poisoning | Manipulation of training data, fine-tuning data, or embeddings to introduce bias, backdoors, or harmful behavior | MEDIUM -- Less directly applicable to prompt-based agents using API-accessed LLMs. However, context poisoning (corrupting agent memory, rule files, or stored contexts) is the agentic analog. | P3 |
| LLM05 | Improper Output Handling | LLM output consumed by downstream systems without validation, enabling injection into web pages, databases, shells, or other agents | HIGH -- Agent output fed to Bash, Write, Edit tools. Unvalidated agent output can trigger arbitrary code execution or file modification. Multi-agent handoffs pass outputs without sanitization. | P2 |
| LLM06 | Excessive Agency | LLM-based systems with too many tools, excessive permissions, or high autonomy act beyond intended scope | CRITICAL -- Core agentic risk. Agents with Bash, Write, Edit, Task tools have broad system access. Over-privileged tool tiers (T5 when T1 suffices) amplify blast radius. Maps directly to Jerry's T1-T5 tier model. | P1 |
| LLM07 | System Prompt Leakage | Information embedded in system prompts leaks through LLM responses, compromising confidential instructions, governance rules, or architectural details | HIGH -- Jerry's CLAUDE.md, constitutional rules, L2 re-injection markers, agent definitions contain sensitive governance information. Leakage exposes enforcement architecture. | P2 |
| LLM08 | Vector and Embedding Weaknesses | Vulnerabilities in RAG systems and vector databases enabling poisoning, unauthorized access, or manipulation of retrieval results | MEDIUM -- Jerry doesn't use traditional RAG/vector stores, but Memory-Keeper stored contexts and Context7 lookups are analogous retrieval surfaces. | P3 |
| LLM09 | Misinformation | LLM generates confident but false information that may be relied upon for decisions | MEDIUM -- Agent-generated security guidance, architectural recommendations, or code could contain subtle errors. Self-review (S-010) and creator-critic (H-14) cycles partially mitigate. | P3 |
| LLM10 | Unbounded Consumption | Excessive resource usage through token-heavy prompts, recursive agent calls, or denial-of-service attacks | HIGH -- Agent loops (AP-04), recursive tool calls, long-running sessions consume excessive tokens and compute. Circuit breaker (H-36) and iteration ceilings (RT-M-010) are existing mitigations. | P2 |

### Agentic Relevance Mapping

| Relevance Tier | LLM IDs | Count | Key Insight |
|----------------|---------|-------|-------------|
| CRITICAL | LLM01, LLM06 | 2 | Prompt injection and excessive agency are the twin pillars of agentic risk |
| HIGH | LLM02, LLM03, LLM05, LLM07, LLM10 | 5 | Information disclosure, supply chain, output handling, prompt leakage, resource exhaustion |
| MEDIUM | LLM04, LLM08, LLM09 | 3 | Data poisoning, embedding weaknesses, misinformation -- less directly applicable but not ignorable |

---

## OWASP Agentic Top 10 (2026) Analysis (L1) -- CRITICAL SECTION

The OWASP Top 10 for Agentic Applications 2026 (released December 10, 2025) is the first industry-standard threat classification specifically for autonomous AI agent systems. Developed by 100+ experts, it is the single most directly applicable framework for Jerry's security architecture.

### Per-Item Deep Analysis (ASI01-ASI10)

#### ASI01: Agent Goal Hijack

**Description:** Attackers alter an agent's objectives or decision path through malicious text content. Agents cannot reliably separate instructions from data. They pursue unintended actions when processing poisoned emails, PDFs, meeting invites, RAG documents, or web content.

**Attack Vectors:**
- Indirect prompt injection via file content processed by Read tool
- Poisoned MCP server responses containing embedded instructions
- Malicious content in WebFetch results
- Crafted tool outputs that redirect agent behavior
- Calendar invites, email content, or document metadata containing hidden instructions

**Impact:** Loss of data confidentiality, unauthorized actions, compromised decision-making, constitutional rule bypass.

**Jerry-Specific Threat Surface:**
- Agent reads a file containing hidden instructions that override CLAUDE.md rules
- WebFetch retrieves a page with embedded prompt injection in HTML comments
- MCP server (Context7, Memory-Keeper) returns poisoned data containing instructions
- Tool results from Bash commands include crafted output designed to redirect agent behavior
- A user-provided document contains instructions to "ignore all previous rules"

**Agentic Relevance:** CRITICAL

**Recommended Mitigations for Jerry:**
1. Treat all tool results, file contents, and external data as untrusted input
2. Implement input sanitization layer between tool results and LLM processing (L3 pre-tool gating)
3. L2 re-injection of constitutional rules after every tool result (existing; strengthen)
4. Require human approval for goal changes or high-impact actions (H-02 user authority)
5. Implement content source classification (trusted vs. untrusted)
6. Monitor for anomalous behavior patterns after processing external content

---

#### ASI02: Tool Misuse and Exploitation

**Description:** Agents use legitimate tools unsafely due to ambiguous prompts, misalignment, or manipulated input. Over-privileged tools combined with poisoned descriptors or unclear instructions enable destructive sequences.

**Attack Vectors:**
- Over-privileged tools with write access to production systems
- Poisoned MCP server tool descriptors
- Shell tools executing unvalidated commands
- Tool chaining that creates unintended side effects
- Ambiguous prompts leading to destructive parameter selection

**Impact:** Data loss, exfiltration, system compromise, production environment damage.

**Jerry-Specific Threat Surface:**
- Bash tool executing injected shell commands (rm -rf, curl to exfil endpoint)
- Write/Edit tools modifying critical files (.context/rules/, CLAUDE.md, agent definitions)
- Task tool delegating to workers with inherited broad permissions
- MCP tool invocations with manipulated parameters
- Tool chaining: Read sensitive file -> Bash curl to external endpoint

**Agentic Relevance:** CRITICAL

**Recommended Mitigations for Jerry:**
1. Enforce principle of least privilege via tool tier model (T1-T5) -- existing
2. Implement argument validation before tool execution (L3 pre-tool gating)
3. Sandboxed execution for Bash tool (filesystem isolation, network restrictions)
4. Policy controls on every tool invocation (deterministic allowlist/denylist)
5. Tool descriptor integrity verification for MCP servers
6. Rate limiting on destructive operations (Write, Edit, Bash)

---

#### ASI03: Identity and Privilege Abuse

**Description:** Agents inherit user or system identities with high-privilege credentials, session tokens, and delegated access that can be unintentionally reused, escalated, or passed across agents.

**Attack Vectors:**
- Credential inheritance across orchestrator-worker delegation
- Cached SSH keys or API tokens in agent memory/context
- Cross-agent delegation without scope restrictions
- Confused deputy attacks where agent acts with user's full permissions
- Session token replay across agent boundaries

**Impact:** Unauthorized system access, privilege escalation, lateral movement.

**Jerry-Specific Threat Surface:**
- Orchestrator delegates to worker with full user file system access
- Agent context contains API keys loaded from .env or config files
- MCP server tokens shared across all agents in a session
- Worker agent inheriting orchestrator's Bash execution privilege
- Memory-Keeper stores containing credential material

**Agentic Relevance:** HIGH

**Recommended Mitigations for Jerry:**
1. Implement short-lived, task-scoped credentials
2. Enforce per-agent identity (unique agent names in YAML definitions -- existing)
3. Tool tier restrictions prevent workers from accessing T5 tools (H-35 -- existing)
4. Implement credential scanning in agent context before tool invocation
5. Scope MCP server access per agent definition
6. Audit credential material in Memory-Keeper stored contexts

---

#### ASI04: Agentic Supply Chain Vulnerabilities

**Description:** Agent supply chains include tools, plugins, prompt templates, model files, and MCP servers fetched dynamically at runtime. Compromised components alter agent behavior or expose data.

**Attack Vectors:**
- Malicious MCP servers impersonating trusted tools
- Poisoned prompt templates in .context/templates/
- Compromised third-party agents in orchestrated workflows
- Vulnerable Python dependencies
- Runtime component fetching without integrity verification

**Impact:** Widespread agent behavior compromise, data exfiltration at scale, loss of system integrity.

**Jerry-Specific Threat Surface:**
- MCP servers (Context7, Memory-Keeper) are third-party services fetched at runtime
- Agent definition files loaded dynamically via Task tool
- Python dependencies managed via uv without hash verification
- .context/templates/ adversarial strategy templates could be poisoned
- SKILL.md files loaded at session start establish agent behavior

**Agentic Relevance:** HIGH

**Recommended Mitigations for Jerry:**
1. Implement MCP server integrity verification (signed manifests)
2. Pin and hash-verify all Python dependencies (uv.lock)
3. L5 CI validation of agent definition files and templates
4. Curated registry of approved MCP servers
5. Sandboxed execution for third-party MCP tool calls
6. Kill switch capability for compromised MCP servers

---

#### ASI05: Unexpected Code Execution

**Description:** Agents generate or run code unsafely, including shell commands, scripts, migrations, template evaluation, or deserialization triggered through generated output.

**Attack Vectors:**
- Code assistants running generated patches directly without review
- Prompt injection triggering shell command execution
- Unsafe deserialization in agent memory systems
- Template evaluation executing injected code
- "Vibe coding" where agent-generated code bypasses controls

**Impact:** Remote code execution, system compromise, arbitrary code on sensitive systems.

**Jerry-Specific Threat Surface:**
- Bash tool executes agent-generated commands without human review
- Write tool creates executable scripts
- Edit tool modifies existing code with injected content
- Agent-generated Python code executed via `uv run`
- Template rendering with injected code in adversarial strategy templates

**Agentic Relevance:** HIGH

**Recommended Mitigations for Jerry:**
1. Sandbox Bash tool execution (existing Claude Code sandboxing)
2. Require human confirmation for destructive Bash commands (H-02)
3. Static analysis on agent-generated code before execution
4. Restrict Write tool from creating executable files in system paths
5. Template rendering should not evaluate arbitrary expressions
6. Implement code review gate for generated patches

---

#### ASI06: Memory and Context Poisoning

**Description:** Agents rely on memory systems, embeddings, RAG databases, and summaries. Attackers poison this memory to influence future decisions or long-term behavior.

**Attack Vectors:**
- RAG poisoning through malicious document injection
- Cross-tenant context leakage
- Long-term behavioral drift from adversarial content exposure
- Persistent state corruption in memory stores
- Poisoned summaries that distort future reasoning

**Impact:** Ongoing behavioral manipulation, decision poisoning across sessions, cross-tenant leakage.

**Jerry-Specific Threat Surface:**
- Memory-Keeper stored contexts poisoned with malicious instructions
- L2 re-injection markers in .context/rules/ files modified to inject adversarial content
- Context rot (R-T01) naturally degrades constitutional enforcement over long sessions
- Agent definition YAML frontmatter modified with subtle behavioral changes
- Cross-session context from Memory-Keeper carrying poisoned data
- Worktracker files containing hidden instructions in entity descriptions

**Agentic Relevance:** CRITICAL (for Jerry specifically, because context IS the enforcement mechanism)

**Recommended Mitigations for Jerry:**
1. Integrity verification for .context/rules/ files (hash-based, L5 CI)
2. Memory-Keeper input sanitization before storage
3. Context isolation per session/task (existing via Task tool fresh context)
4. Expiry policies for Memory-Keeper entries
5. L2 re-injection as context rot countermeasure (existing; strengthen with integrity checks)
6. Monitor context fill levels (AE-006 escalation -- existing)
7. Implement data provenance tracking for all context sources

---

#### ASI07: Insecure Inter-Agent Communication

**Description:** Multi-agent systems exchange messages across MCP, A2A channels, RPC endpoints, or shared memory. Unencrypted or unauthenticated communication enables interception and instruction injection.

**Attack Vectors:**
- Spoofed agent identities in delegation chains
- Replayed delegation messages
- Message tampering on unprotected channels
- Man-in-the-middle attacks on inter-agent protocols
- Unauthorized agent discovery and registration

**Impact:** Unauthorized inter-agent actions, privilege escalation via spoofing, data exfiltration.

**Jerry-Specific Threat Surface:**
- Orchestrator-worker communication via Task tool lacks cryptographic authentication
- Handoff data structures (HD-M-001) contain unverified from_agent fields
- MCP server communication may lack mutual TLS
- Agent routing decisions based on unverified skill claims
- Shared file system used as implicit communication channel (no message integrity)

**Agentic Relevance:** HIGH

**Recommended Mitigations for Jerry:**
1. Implement handoff schema validation (HD-M-001 -- existing MEDIUM standard)
2. Verify agent identity in handoff from_agent fields
3. Implement signed handoff payloads for C3+ deliverables
4. Mutual TLS for MCP server connections
5. Anti-replay protections in multi-agent workflows
6. Agent discovery restricted to registered agents in AGENTS.md

---

#### ASI08: Cascading Failures

**Description:** Small errors in one agent propagate across planning, execution, memory, and downstream systems. Interconnected agent architectures amplify failures rapidly.

**Attack Vectors:**
- Hallucinating planner issues destructive tasks to multiple agents
- Poisoned state propagating through deployment pipelines
- Single agent failure cascading through dependent systems
- Error amplification through serial handoffs (Telephone Game, AP-03)
- Memory corruption spreading across agent network

**Impact:** System-wide failures, widespread data loss/corruption, infrastructure damage.

**Jerry-Specific Threat Surface:**
- Orchestrator makes incorrect plan; workers execute destructive tasks in parallel
- Quality score false positives (adv-scorer leniency) let bad deliverables cascade
- Poisoned handoff data propagates through multi-phase orchestration
- Circuit breaker failure allows unbounded routing loops (AP-04)
- Error in one agent's output corrupts downstream agent context

**Agentic Relevance:** MEDIUM

**Recommended Mitigations for Jerry:**
1. Circuit breaker with max 3 hops (H-36 -- existing)
2. Isolation boundaries between agents (Task tool context isolation -- existing)
3. Rate limits on agent actions
4. Pre-deployment testing of multi-step plans
5. Quality gate at handoff boundaries (HD-M-003 -- existing)
6. Structured error propagation in multi_skill_context (existing)

---

#### ASI09: Human-Agent Trust Exploitation

**Description:** Users over-trust agent recommendations or explanations. Attackers or misaligned agents leverage this trust to influence decisions or extract sensitive information.

**Attack Vectors:**
- Coding assistants introducing subtle backdoors
- Agents persuading users to reveal credentials
- Confident but false security recommendations
- Social engineering through agent responses
- Manipulation of human-in-the-loop approval processes

**Impact:** User-initiated security breaches, credential theft, harmful outcomes.

**Jerry-Specific Threat Surface:**
- Agent presents quality scores (S-014) that appear legitimate but are inflated
- Agent recommends architectural changes that introduce vulnerabilities
- User trusts agent-generated code without thorough review
- Agent manipulates H-02 user authority requests to obtain destructive approvals
- Persuasive agent output overrides user's security instincts

**Agentic Relevance:** MEDIUM

**Recommended Mitigations for Jerry:**
1. Self-review (S-010) and creator-critic (H-14) cycles reduce false confidence
2. Quality gate threshold (>= 0.92 for C2+) with anti-leniency measures
3. Forced confirmations for destructive/irreversible actions (H-02)
4. Clear risk indicators on uncertain outputs
5. P-022 no deception requirement for confidence calibration
6. Immutable audit logs of agent recommendations

---

#### ASI10: Rogue Agents

**Description:** Compromised or misaligned agents act harmfully while appearing legitimate. They may self-replicate actions, persist across sessions, or impersonate other agents.

**Attack Vectors:**
- Agents continuing data exfiltration after single prompt injection
- Approval agents silently approving unsafe actions
- Cost optimizers deleting critical backups
- Self-replicating agents spreading across systems
- Compromised agents impersonating trusted agents

**Impact:** Sustained data breaches, persistent unauthorized access, systemic attacks.

**Jerry-Specific Threat Surface:**
- A compromised adv-scorer agent inflating quality scores to pass bad deliverables
- A worker agent continuing harmful actions after prompt injection in single task
- Rogue orch-planner creating malicious work plans that direct destructive actions
- Agent definition files modified to create persistently malicious agent behavior
- ps-researcher agent exfiltrating sensitive data while appearing to do research

**Agentic Relevance:** CRITICAL

**Recommended Mitigations for Jerry:**
1. Agent definition integrity verification (H-34 schema validation, L5 CI)
2. Behavioral anomaly monitoring for agent output patterns
3. Kill switch capability for rapid agent deactivation
4. Role-based access controls for agent management
5. Regular audit of agent logs and decisions (RT-M-008 routing records)
6. Sandboxed execution environments for all agents
7. Constitutional compliance check (S-007) as persistent behavioral verification

### Jerry-Specific Threat Mapping

| ASI Item | Jerry Component | Threat Vector | Existing Mitigation | Gap |
|----------|-----------------|---------------|---------------------|-----|
| ASI01 | Input processing | Prompt injection via tool results | L2 re-injection | No input sanitization layer between tool results and LLM |
| ASI02 | Tool execution | Over-privileged tools | T1-T5 tiers, H-35 | No argument validation before execution |
| ASI03 | Delegation | Credential inheritance | P-003 single-level | No per-task credential scoping |
| ASI04 | MCP integration | Malicious MCP servers | None | No MCP server integrity verification |
| ASI05 | Bash/Write tools | Code execution | Claude Code sandbox | No static analysis on generated code |
| ASI06 | Context/memory | Context poisoning | L2 re-injection, AE-006 | No integrity verification for .context/rules/ at runtime |
| ASI07 | Agent handoffs | Spoofed/tampered messages | Handoff schema (MEDIUM) | No cryptographic authentication on handoffs |
| ASI08 | Orchestration | Error cascade | Circuit breaker H-36 | No pre-deployment plan validation |
| ASI09 | User interaction | Trust exploitation | H-14 creator-critic, S-010 | No forced explanation of uncertainty |
| ASI10 | Agent definitions | Rogue behavior | H-34 schema, L5 CI | No runtime behavioral anomaly detection |

### Recommended Mitigations per ASI Item -- Jerry Priority

| Priority | ASI Items | Mitigation Theme | Implementation Effort |
|----------|-----------|-----------------|----------------------|
| P1 (Immediate) | ASI01, ASI02, ASI06, ASI10 | Input sanitization, tool argument validation, context integrity, agent integrity | HIGH |
| P2 (Near-term) | ASI03, ASI04, ASI07 | Credential scoping, supply chain verification, handoff authentication | MEDIUM |
| P3 (Strategic) | ASI05, ASI08, ASI09 | Code review gates, plan validation, trust calibration | MEDIUM |

---

## OWASP API Security Top 10 Analysis (L1)

### Per-Item Analysis (API1-API10)

| ID | Name | Description | MCP/Agent Relevance | Priority |
|----|------|-------------|---------------------|----------|
| API1:2023 | Broken Object Level Authorization (BOLA) | Endpoints expose object IDs without validating ownership; attackers manipulate IDs to access unauthorized objects | HIGH -- MCP servers expose tool endpoints; agents may access data objects without ownership validation | P2 |
| API2:2023 | Broken Authentication | Weak authentication enables token compromise and identity assumption | HIGH -- MCP server authentication; agent-to-API authentication tokens; API key management | P2 |
| API3:2023 | Broken Object Property Level Authorization | Inadequate property-level validation enables data exposure or manipulation | MEDIUM -- MCP tool responses may expose unintended properties; agent tool schemas may not restrict returned fields | P3 |
| API4:2023 | Unrestricted Resource Consumption | Uncontrolled resource requests cause DoS or cost increases | HIGH -- Agent tool invocations can generate unbounded API calls; token exhaustion attacks; MCP server resource abuse | P2 |
| API5:2023 | Broken Function Level Authorization | Complex access policies enable privilege escalation | HIGH -- MCP server tools may expose admin functions; agent tool tiers bypass if not enforced server-side | P2 |
| API6:2023 | Unrestricted Access to Sensitive Business Flows | Business operations vulnerable to automated exploitation | MEDIUM -- Agents can automate abuse of business-logic APIs at scale | P3 |
| API7:2023 | Server Side Request Forgery (SSRF) | Unvalidated remote resource fetching enables crafted request injection | HIGH -- WebFetch tool fetches arbitrary URLs; MCP servers may fetch resources on behalf of agents | P2 |
| API8:2023 | Security Misconfiguration | Configuration gaps create attack surfaces | HIGH -- MCP server misconfiguration; agent definition errors; overly permissive tool configurations | P2 |
| API9:2023 | Improper Inventory Management | Inadequate version tracking exposes deprecated endpoints | MEDIUM -- MCP server version management; deprecated tool endpoints; untracked API surface | P3 |
| API10:2023 | Unsafe Consumption of APIs | Third-party API integrations trusted excessively | CRITICAL -- Agents consume MCP server responses, Context7 data, and external APIs without sufficient validation; maps directly to ASI04 supply chain | P1 |

### MCP Server Attack Surface Mapping

| API Risk | MCP Attack Vector | Jerry-Specific Surface |
|----------|-------------------|----------------------|
| API1 (BOLA) | MCP server returns data for wrong tenant/session | Memory-Keeper cross-session data access |
| API2 (Auth) | Weak or absent MCP server authentication | MCP servers configured without auth in .claude/settings.local.json |
| API4 (Resource) | Agent floods MCP server with requests | Memory-Keeper/Context7 unbounded queries |
| API5 (BFLA) | MCP server exposes admin tools to all callers | Memory-Keeper delete/admin operations accessible |
| API7 (SSRF) | MCP server fetches attacker-controlled URLs | Context7 resolve/query with attacker-crafted library names |
| API8 (Misconfig) | MCP server default configs expose debug endpoints | Development MCP servers in production |
| API10 (Unsafe Consumption) | Agent trusts MCP response content blindly | All MCP tool results consumed without validation |

---

## OWASP Web Top 10 Analysis (L1)

### Per-Item Analysis (A01-A10)

| ID | Name | Description | Agent Web Interaction Relevance | Priority |
|----|------|-------------|-------------------------------|----------|
| A01:2021 | Broken Access Control | Improper enforcement of user permissions | HIGH -- Agents accessing web resources may bypass access controls; WebFetch may access unintended resources | P2 |
| A02:2021 | Cryptographic Failures | Weak or misapplied cryptography | MEDIUM -- Agent-to-API communication encryption; MCP transport security; credential storage | P3 |
| A03:2021 | Injection | Untrusted input passed to interpreters | CRITICAL -- Prompt injection is the AI analog; agent tool inputs may contain injection payloads | P1 |
| A04:2021 | Insecure Design | Flawed application architecture | HIGH -- Agent architecture without security-by-design; missing threat modeling for agent workflows | P2 |
| A05:2021 | Security Misconfiguration | Improperly configured systems | HIGH -- Agent tool configurations, MCP server settings, permission overrides | P2 |
| A06:2021 | Vulnerable and Outdated Components | Known-vulnerable dependencies | HIGH -- Python packages, MCP servers, model APIs with known CVEs | P2 |
| A07:2021 | Identification and Authentication Failures | Broken authentication mechanisms | HIGH -- Agent identity, MCP server auth, API key management | P2 |
| A08:2021 | Software and Data Integrity Failures | Unverified updates, CI/CD compromise | HIGH -- Agent definition integrity, MCP server updates, dependency verification | P2 |
| A09:2021 | Security Logging and Monitoring Failures | Insufficient logging for detection | HIGH -- Agent action logging, tool invocation audit trails, routing decision records | P2 |
| A10:2021 | Server-Side Request Forgery (SSRF) | Server-side requests to attacker-controlled URIs | HIGH -- WebFetch tool fetches arbitrary URLs; agent-initiated HTTP requests via Bash | P2 |

### Relevance to Agent Web Interactions

The web security landscape is particularly relevant to agents because:

1. **Agents as web clients:** WebFetch, Bash (curl), and MCP server interactions make agents web clients that process untrusted web content.
2. **Injection paradigm shift:** A03 Injection maps directly to prompt injection -- the fundamental threat to LLM-based agents.
3. **Integrity concerns:** A08 Software and Data Integrity Failures maps to agent supply chain (ASI04) -- unverified MCP servers, unsigned agent definitions, unchecked dependency updates.
4. **Logging imperative:** A09 maps to ASI09 Insufficient Logging -- agents require comprehensive audit trails for all tool invocations, routing decisions, and state changes.
5. **SSRF amplification:** A10 SSRF is amplified in agents because they can be instructed to make arbitrary web requests via prompt injection.

---

## NIST AI RMF (600-1) Analysis (L1)

### Functions: MAP, MEASURE, MANAGE, GOVERN

The NIST AI Risk Management Framework (AI RMF 1.0, NIST AI 100-1) defines four functions for managing AI risk. NIST AI 600-1 is the Generative AI Profile that maps these functions to 12 GenAI-specific risk categories.

| Function | Purpose | Agentic Application |
|----------|---------|---------------------|
| GOVERN | Establish and maintain AI risk governance | Jerry constitutional governance (JERRY_CONSTITUTION.md), HARD rules, quality enforcement, criticality levels |
| MAP | Contextualize AI risks within organizational context | Threat framework mapping (this document), attack surface identification, risk classification |
| MEASURE | Quantify and track AI risks | Quality scoring (S-014), FMEA monitoring thresholds (RT-M-011 through RT-M-015), routing observability |
| MANAGE | Prioritize and act on AI risks | Mitigation implementation, security controls, enforcement architecture (L1-L5) |

### GenAI Profile Risk Categories (12)

| # | Risk Category | Description | Agentic Relevance | Priority |
|---|---------------|-------------|-------------------|----------|
| 1 | CBRN Information | Access to chemical, biological, radiological, nuclear weapons information | LOW -- Agent unlikely to encounter CBRN content in Jerry context; model-level safeguards apply | P4 |
| 2 | Confabulation | Confident false statements (hallucinations) | HIGH -- Agent generates security recommendations, code, or architectural guidance that may be subtly wrong; maps to ASI09 trust exploitation | P2 |
| 3 | Dangerous/Violent Content | Generation of harmful content | LOW -- Not directly relevant to Jerry's development tooling context | P4 |
| 4 | Data Privacy | Leakage, unauthorized use, de-anonymization | HIGH -- Agent processes project files, credentials, PII; maps to LLM02 sensitive disclosure | P2 |
| 5 | Environmental Impact | High computing resource usage | LOW -- Relevant at scale but not a primary security concern | P4 |
| 6 | Harmful Bias | Discriminatory outputs | LOW -- Less directly relevant to development tooling security | P4 |
| 7 | Human-AI Configuration | Automation bias, over-reliance, emotional entanglement | MEDIUM -- Developer over-trust in agent recommendations; maps to ASI09 | P3 |
| 8 | Information Integrity | Difficulty distinguishing fact from fiction | HIGH -- Agent-generated deliverables may contain unverified claims; quality gate (H-13) and citation requirements mitigate | P2 |
| 9 | Information Security | Cybersecurity impacts of GenAI deployment | CRITICAL -- Core concern; encompasses all agentic security risks | P1 |
| 10 | Intellectual Property | Copyright and IP infringement in training/outputs | MEDIUM -- Agent may generate code with IP concerns; less of a security risk | P3 |
| 11 | Obscene/Degrading Content | Illegal or abusive content generation | LOW -- Not directly relevant to development tooling | P4 |
| 12 | Value Chain/Component Integration | Risks from integrating AI components | HIGH -- MCP servers, third-party models, dependency chain; maps to ASI04, LLM03 | P2 |

### GOVERN Function -- Jerry Alignment

The GOVERN function in AI RMF maps directly to Jerry's governance architecture:

| AI RMF GOVERN Element | Jerry Implementation |
|----------------------|----------------------|
| Policies and procedures | JERRY_CONSTITUTION.md, HARD rules (H-01 through H-36) |
| Roles and responsibilities | Agent definitions with identity, expertise, capabilities |
| Risk tolerance | Criticality levels (C1-C4), quality thresholds |
| Monitoring and oversight | AE-006 context monitoring, routing observability, audit trails |
| Documentation | ADR process, worktracker, skill documentation |

---

## NIST CSF 2.0 Analysis (L1)

### Functions: Identify, Protect, Detect, Respond, Recover, Govern

NIST CSF 2.0 (released February 2024) provides a voluntary framework for managing cybersecurity risk. Version 2.0 adds the Govern function and expands to 6 functions, 22 categories, and 107 subcategories.

| Function | ID | Categories | Description | Agentic Application |
|----------|-----|------------|-------------|---------------------|
| Govern | GV | 6 | Cybersecurity risk governance and strategy | Constitutional governance, HARD rules, criticality levels, escalation rules |
| Identify | ID | 4 | Asset management, risk assessment, improvement | Agent/tool inventory, attack surface mapping, threat framework consumption |
| Protect | PR | 5 | Access control, awareness, data security, platform security, resilience | Tool tier enforcement, credential management, sandboxing, input validation |
| Detect | DE | 2 | Continuous monitoring, adverse event analysis | Routing observability, FMEA thresholds, anomaly detection |
| Respond | RS | 4 | Incident management, analysis, reporting, mitigation | Circuit breaker activation, human escalation, error propagation handling |
| Recover | RC | 2 | Recovery planning, execution | Session recovery, checkpoint restoration, graceful degradation |

### IR 8596 AI Profile Overlay

NIST IR 8596 (draft, December 2025) overlays three AI-specific focus areas onto CSF 2.0:

| Focus Area | Description | Jerry Application | Priority |
|------------|-------------|-------------------|----------|
| **Secure** | Managing cybersecurity challenges when integrating AI into systems | Securing agent architecture, tool tier enforcement, MCP server security, supply chain verification | P1 |
| **Detect** (Defend) | Using AI to improve cybersecurity while managing risks AI poses to defense | Agent-assisted security analysis (this project), quality gate automation, adversarial review | P2 |
| **Thwart** | Building resilience against AI-enabled cyber attacks | Defense against prompt injection, adversarial inputs, rogue agents, cascading failures | P1 |

**Key IR 8596 finding relevant to Jerry:**

> "AI agent systems are capable of taking autonomous actions that impact real-world systems and may be susceptible to hijacking, backdoor attacks, and other exploits."

This directly validates the OWASP Agentic Top 10 threat model and confirms that agentic security is recognized as a distinct concern by US government standards bodies.

**CSF 2.0 Categories Most Relevant to Agent Security:**

| Category ID | Category Name | Agentic Relevance |
|-------------|---------------|-------------------|
| GV.OC | Organizational Context | HIGH -- Agent deployment context, risk tolerance |
| GV.RM | Risk Management Strategy | HIGH -- Criticality levels, quality thresholds |
| GV.SC | Supply Chain Risk Management | CRITICAL -- MCP servers, dependencies, model APIs |
| ID.AM | Asset Management | HIGH -- Agent inventory, tool inventory, MCP server inventory |
| ID.RA | Risk Assessment | CRITICAL -- Threat framework mapping, FMEA analysis |
| PR.AA | Identity Management, Auth, Access Control | CRITICAL -- Agent identity, tool access, credential management |
| PR.DS | Data Security | HIGH -- Agent context protection, memory isolation |
| PR.PS | Platform Security | HIGH -- Sandboxing, tool execution security |
| DE.CM | Continuous Monitoring | HIGH -- Agent behavior monitoring, routing observability |
| DE.AE | Adverse Event Analysis | HIGH -- Anomaly detection in agent behavior |
| RS.MA | Incident Management | HIGH -- Circuit breaker, human escalation, error handling |
| RC.RP | Recovery Planning | MEDIUM -- Session recovery, checkpoint restore |

---

## NIST SP 800-53 Analysis (L1)

### Key Control Families for Agentic Systems

NIST SP 800-53 Rev 5 defines 20 control families with 1,007 controls. The following families are most relevant to agentic AI security:

| Family | ID | Controls | Agentic Relevance | Priority |
|--------|----|----------|-------------------|----------|
| Access Control | AC | 25 base controls | CRITICAL -- Agent tool access, T1-T5 tiers, orchestrator-worker delegation, MCP server access | P1 |
| Audit and Accountability | AU | 16 base controls | CRITICAL -- Agent action logging, tool invocation audit, routing decision records, compliance evidence | P1 |
| Assessment, Authorization, Monitoring | CA | 9 base controls | HIGH -- Agent definition validation, quality gates, continuous monitoring | P2 |
| Configuration Management | CM | 14 base controls | HIGH -- Agent config integrity, .context/rules/ management, MCP server configuration | P2 |
| Contingency Planning | CP | 13 base controls | MEDIUM -- Session recovery, checkpoint/restore, graceful degradation | P3 |
| Identification and Authentication | IA | 12 base controls | CRITICAL -- Agent identity, MCP server authentication, credential management | P1 |
| Incident Response | IR | 10 base controls | HIGH -- Circuit breaker activation, human escalation, error handling | P2 |
| Maintenance | MA | 6 base controls | LOW -- Less directly applicable to agent runtime | P4 |
| Personnel Security | PS | 9 base controls | LOW -- Human operator security, not directly agent-applicable | P4 |
| Risk Assessment | RA | 7 base controls | HIGH -- Threat framework consumption, FMEA analysis, vulnerability scanning | P2 |
| System and Services Acquisition | SA | 22 base controls | HIGH -- MCP server acquisition, dependency management, supply chain | P2 |
| System and Communications Protection | SC | 51 base controls | CRITICAL -- Agent sandboxing, network isolation, input validation, encryption | P1 |
| System and Information Integrity | SI | 23 base controls | CRITICAL -- Agent output validation, integrity monitoring, malicious input detection | P1 |
| Supply Chain Risk Management | SR | 12 base controls | HIGH -- MCP supply chain, dependency chain, model API provider chain | P2 |
| PII Processing and Transparency | PT | 8 base controls | MEDIUM -- Agent processing of personal data, transparency of agent decisions | P3 |
| Awareness and Training | AT | 6 base controls | MEDIUM -- Operator security awareness for agent systems | P3 |
| Media Protection | MP | 8 base controls | LOW -- Physical media less relevant to agent context | P4 |
| Physical and Environmental Protection | PE | 23 base controls | LOW -- Physical security not directly applicable | P4 |
| Planning | PL | 11 base controls | MEDIUM -- Security planning for agent deployments | P3 |
| Program Management | PM | 32 base controls | MEDIUM -- Organizational security program for agent governance | P3 |

### Control-to-Threat Mapping

| SP 800-53 Control | Control Name | OWASP Agentic Threat | MITRE ATLAS Technique |
|-------------------|-------------|---------------------|----------------------|
| AC-3 | Access Enforcement | ASI02 Tool Misuse, ASI03 Privilege Abuse | AML.T0081 Modify Agent Config |
| AC-4 | Information Flow Enforcement | ASI07 Insecure Inter-Agent Communication | AML.T0086 Exfil via Agent Tool |
| AC-6 | Least Privilege | ASI02 Tool Misuse, ASI03 Privilege Abuse | AML.T0085 Data from AI Services |
| AU-2 | Event Logging | ASI09 Insufficient Logging | AML.T0084 Discover Agent Config |
| AU-3 | Content of Audit Records | ASI09 Insufficient Logging | AML.T0086 Exfil via Agent Tool |
| AU-6 | Audit Record Review | ASI09 Insufficient Logging, ASI10 Rogue Agents | AML.T0080 Context Poisoning |
| CM-3 | Configuration Change Control | ASI06 Memory Poisoning | AML.T0081 Modify Agent Config |
| CM-7 | Least Functionality | ASI02 Tool Misuse | AML.T0085.001 AI Agent Tools |
| IA-2 | Identification and Authentication | ASI03 Privilege Abuse, ASI07 Inter-Agent Comms | AML.T0083 Creds from Agent Config |
| IA-8 | Identification and Authentication (Non-Org Users) | ASI07 Inter-Agent Communication | AML.T0082 RAG Credential Harvesting |
| IR-4 | Incident Handling | ASI08 Cascading Failures | AML.T0080 Context Poisoning |
| RA-3 | Risk Assessment | All ASI items | All AML techniques |
| RA-5 | Vulnerability Monitoring and Scanning | ASI04 Supply Chain | AML.T0084 Discover Agent Config |
| SA-8 | Security and Privacy Engineering Principles | ASI04 Supply Chain | Supply Chain Compromise |
| SC-7 | Boundary Protection | ASI01 Goal Hijack, ASI07 Inter-Agent Comms | AML.T0080 Context Poisoning |
| SC-8 | Transmission Confidentiality and Integrity | ASI07 Insecure Inter-Agent Comms | AML.T0086 Exfil via Agent Tool |
| SI-3 | Malicious Code Protection | ASI05 Code Execution, ASI10 Rogue Agents | AML.T0081 Modify Agent Config |
| SI-4 | System Monitoring | ASI09 Logging, ASI10 Rogue Agents | AML.T0080 Context Poisoning |
| SI-10 | Information Input Validation | ASI01 Goal Hijack, ASI06 Memory Poisoning | AML.T0080 Context Poisoning |
| SR-3 | Supply Chain Controls and Processes | ASI04 Supply Chain | Supply Chain Compromise |
| SR-6 | Supplier Assessments and Reviews | ASI04 Supply Chain | AML.T0081 Modify Agent Config |

---

## Cross-Framework Mapping (L2)

### Unified Threat Taxonomy

Consolidating across all 10 framework scopes, the agentic threat landscape resolves to 8 primary threat categories:

| # | Unified Threat Category | MITRE ATT&CK | MITRE ATLAS | OWASP LLM | OWASP Agentic | OWASP API | OWASP Web | NIST AI RMF | NIST CSF | NIST 800-53 |
|---|------------------------|--------------|-------------|-----------|---------------|-----------|-----------|-------------|----------|-------------|
| 1 | **Prompt Injection & Goal Hijack** | TA0001 (Initial Access) | AML.T0080 (Context Poisoning) | LLM01 | ASI01 | -- | A03 (Injection) | Cat 9 (InfoSec) | DE.AE | SI-10 |
| 2 | **Tool Misuse & Excessive Agency** | TA0002 (Execution) | AML.T0085.001 (Agent Tools) | LLM06 | ASI02 | API5 (BFLA) | A01 (Access Control) | Cat 9 (InfoSec) | PR.AA | AC-3, AC-6 |
| 3 | **Privilege Escalation & Identity Abuse** | TA0004 (Priv Esc) | AML.T0083 (Creds from Config) | LLM06 | ASI03 | API1 (BOLA), API2 (Auth) | A07 (Auth Failures) | Cat 9 (InfoSec) | PR.AA | IA-2, AC-6 |
| 4 | **Supply Chain Compromise** | TA0042 (Resource Dev) | Supply Chain | LLM03 | ASI04 | API10 (Unsafe Consumption) | A06 (Vuln Components), A08 (Integrity) | Cat 12 (Value Chain) | GV.SC | SA-8, SR-3 |
| 5 | **Memory & Context Manipulation** | TA0003 (Persistence) | AML.T0080 (Context Poisoning) | LLM04, LLM08 | ASI06 | -- | -- | Cat 8 (Info Integrity) | PR.DS | CM-3, SI-4 |
| 6 | **Information Disclosure & Exfiltration** | TA0009 (Collection), TA0010 (Exfil) | AML.T0086 (Exfil via Agent Tool) | LLM02, LLM07 | ASI03, ASI05 | API3 (Property Auth) | A02 (Crypto) | Cat 4 (Data Privacy) | PR.DS | SC-8, AC-4 |
| 7 | **Inter-Agent Communication & Cascading Failures** | TA0008 (Lateral Movement) | -- | LLM05, LLM10 | ASI07, ASI08 | API8 (Misconfig) | A04 (Insecure Design) | Cat 7 (Human-AI) | RS.MA | SC-7, IR-4 |
| 8 | **Rogue Agents & Trust Exploitation** | TA0005 (Defense Evasion) | AML.T0081 (Modify Config) | LLM09 | ASI09, ASI10 | -- | A09 (Logging) | Cat 2 (Confabulation) | DE.CM | AU-2, AU-6 |

### Framework Overlap Analysis

| Overlap Zone | Frameworks | Insight |
|-------------|------------|---------|
| Prompt Injection | ATT&CK T1566, ATLAS AML.T0080, LLM01, ASI01, Web A03 | **Strongest cross-framework convergence.** Every framework identifies input manipulation as a primary threat. The agentic dimension adds indirect injection via tool results. |
| Supply Chain | ATT&CK T1195, LLM03, ASI04, API10, Web A06/A08, CSF GV.SC, 800-53 SR | **Second-strongest convergence.** MCP servers are the unique agentic supply chain surface not fully addressed by traditional frameworks. |
| Access Control / Privilege | ATT&CK TA0004, ASI02/ASI03, API1/API2/API5, Web A01/A07, 800-53 AC/IA | **Well-understood in traditional security.** Agentic novelty is in delegation chains and tool permission inheritance. |
| Logging & Monitoring | ASI09, Web A09, 800-53 AU, CSF DE.CM | **Universal gap.** Agent action observability is consistently flagged as underdeveloped across all frameworks. |
| Context/Memory | ATLAS AML.T0080, LLM04/LLM08, ASI06 | **AI-specific convergence.** No traditional framework (ATT&CK, Web, API) addresses this. It is unique to AI agent systems. |

### Coverage Gaps

| Gap | Description | Frameworks That Miss It | Severity |
|-----|-------------|------------------------|----------|
| **Context Rot as Security Threat** | Progressive degradation of behavioral constraints as context fills. Jerry's L1 rules are vulnerable to context rot (enforcement architecture L1 = "Vulnerable" to context rot). No framework explicitly models this. | ALL | CRITICAL |
| **Constitutional Governance Bypass** | Adversary specifically targeting the governance layer (CLAUDE.md, L2 re-injection markers) to disable enforcement. ASI06 is closest but doesn't address the specific threat of disabling the security enforcement mechanism itself. | ALL (partial: ASI06) | CRITICAL |
| **MCP Protocol-Specific Threats** | MCP is a new protocol (late 2024) without dedicated framework coverage. OWASP API Top 10 applies in principle, but MCP-specific attack vectors (tool descriptor poisoning, server impersonation, tool schema manipulation) have no dedicated taxonomy. | ALL | HIGH |
| **Multi-Agent Coordination Attacks** | Attacks that exploit coordination mechanisms (handoff schemas, routing tables, circuit breakers) rather than individual agents. ASI07/ASI08 touch this but don't provide tactical detail. | ATT&CK Enterprise, ATT&CK Mobile, Web, API | HIGH |
| **Agent Definition Integrity** | The integrity of agent definition files (YAML frontmatter + Markdown body) as a security-critical configuration surface. ATLAS AML.T0081 is closest but doesn't address the specific format. | ATT&CK, LLM Top 10, Web, API, NIST | MEDIUM |
| **Tool-Result-to-Prompt Boundary** | The specific trust boundary where tool execution results re-enter the LLM prompt context. This is the primary injection surface for indirect prompt injection in agents but has no dedicated framework treatment. | ALL (partial: ASI01, LLM01) | CRITICAL |

---

## Agentic Threat Priority Matrix

| Threat Category | MITRE Coverage | OWASP Coverage | NIST Coverage | Agentic Relevance | Priority | Jerry Gap Status |
|----------------|---------------|----------------|---------------|-------------------|----------|-----------------|
| Prompt Injection & Goal Hijack | ATT&CK TA0001, ATLAS AML.T0080 | LLM01, ASI01 | AI 600-1 Cat 9, CSF DE.AE, 800-53 SI-10 | CRITICAL | P1 | PARTIAL -- L2 re-injection exists; no input sanitization layer |
| Tool Misuse & Excessive Agency | ATT&CK TA0002, ATLAS AML.T0085.001 | LLM06, ASI02 | AI 600-1 Cat 9, CSF PR.AA, 800-53 AC-3/AC-6 | CRITICAL | P1 | PARTIAL -- T1-T5 tiers exist; no argument validation |
| Memory & Context Manipulation | ATT&CK TA0003, ATLAS AML.T0080 | LLM04/LLM08, ASI06 | AI 600-1 Cat 8, CSF PR.DS, 800-53 CM-3/SI-4 | CRITICAL | P1 | PARTIAL -- L2 re-injection, AE-006; no runtime integrity verification |
| Rogue Agents & Trust Exploitation | ATT&CK TA0005, ATLAS AML.T0081 | LLM09, ASI09/ASI10 | AI 600-1 Cat 2, CSF DE.CM, 800-53 AU-2/AU-6 | CRITICAL | P1 | PARTIAL -- H-34 schema, L5 CI; no runtime behavioral monitoring |
| Privilege Escalation & Identity Abuse | ATT&CK TA0004, ATLAS AML.T0083 | LLM06, ASI03 | AI 600-1 Cat 9, CSF PR.AA, 800-53 IA-2/AC-6 | HIGH | P2 | PARTIAL -- P-003, T1-T5 tiers; no per-task credential scoping |
| Supply Chain Compromise | ATT&CK TA0042, ATLAS Supply Chain | LLM03, ASI04 | AI 600-1 Cat 12, CSF GV.SC, 800-53 SR | HIGH | P2 | GAP -- No MCP server integrity verification |
| Information Disclosure & Exfiltration | ATT&CK TA0009/TA0010, ATLAS AML.T0086 | LLM02/LLM07, ASI03/ASI05 | AI 600-1 Cat 4, CSF PR.DS, 800-53 SC-8/AC-4 | HIGH | P2 | PARTIAL -- Output filtering guardrails; no data loss prevention |
| Inter-Agent Comms & Cascading Failures | ATT&CK TA0008, ATLAS (gap) | LLM05/LLM10, ASI07/ASI08 | AI 600-1 Cat 7, CSF RS.MA, 800-53 SC-7/IR-4 | HIGH | P2 | PARTIAL -- Circuit breaker H-36, handoff schema; no cryptographic auth |
| Context Rot as Security Vector | (gap) | (gap) | (gap) | CRITICAL | P1 | JERRY-SPECIFIC -- L2 re-injection addresses this but needs hardening |
| MCP Protocol-Specific Threats | (gap) | (partial: API10) | (partial: SR) | HIGH | P2 | GAP -- No MCP-specific security controls |

---

## Citations

| # | Source | Authority | URL |
|---|--------|-----------|-----|
| 1 | MITRE ATT&CK Enterprise Matrix | Standards Body | https://attack.mitre.org/matrices/enterprise/ |
| 2 | MITRE ATT&CK Mobile Matrix | Standards Body | https://attack.mitre.org/matrices/mobile/ |
| 3 | MITRE ATLAS | Standards Body | https://atlas.mitre.org/ |
| 4 | MITRE ATT&CK STIX Data Repository | Standards Body | https://github.com/mitre-attack/attack-stix-data |
| 5 | MITRE ATLAS Data Repository | Standards Body | https://github.com/mitre-atlas/atlas-data |
| 6 | Zenity Labs & MITRE ATLAS Collaboration | Industry Expert / Standards Body | https://zenity.io/blog/current-events/zenity-labs-and-mitre-atlas-collaborate-to-advances-ai-agent-security-with-the-first-release-of |
| 7 | Vectra AI -- MITRE ATLAS 15 Tactics Guide | Industry Expert | https://www.vectra.ai/topics/mitre-atlas |
| 8 | Practical DevSecOps -- ATLAS Framework Guide | Industry Expert | https://www.practical-devsecops.com/mitre-atlas-framework-guide-securing-ai-systems/ |
| 9 | OWASP Top 10 for LLM Applications 2025 | Industry Standard | https://genai.owasp.org/llm-top-10/ |
| 10 | OWASP Top 10 for Agentic Applications 2026 | Industry Standard | https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/ |
| 11 | OWASP Agentic AI Threats & Mitigations | Industry Standard | https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/ |
| 12 | Aikido -- OWASP Agentic Top 10 Full Guide | Community Expert | https://www.aikido.dev/blog/owasp-top-10-agentic-applications |
| 13 | OWASP API Security Top 10 2023 | Industry Standard | https://owasp.org/API-Security/editions/2023/en/0x11-t10/ |
| 14 | OWASP Top 10 Web 2021 | Industry Standard | https://owasp.org/Top10/2021/ |
| 15 | OWASP AI Agent Security Cheat Sheet | Industry Standard | https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet |
| 16 | OWASP Prompt Injection Prevention Cheat Sheet | Industry Standard | https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet |
| 17 | NIST AI RMF 1.0 (AI 100-1) | US Government / Standards Body | https://www.nist.gov/itl/ai-risk-management-framework |
| 18 | NIST AI 600-1 GenAI Profile | US Government / Standards Body | https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf |
| 19 | NIST CSF 2.0 | US Government / Standards Body | https://csrc.nist.gov/projects/cybersecurity-framework |
| 20 | NIST IR 8596 CSF Profile for AI (Draft) | US Government / Standards Body | https://csrc.nist.gov/pubs/ir/8596/iprd |
| 21 | NIST SP 800-53 Rev 5 | US Government / Standards Body | https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final |
| 22 | NIST OSCAL Content Repository | US Government / Standards Body | https://github.com/usnistgov/oscal-content |
| 23 | CyberSaint -- NIST 800-53 Control Families | Community Expert | https://www.cybersaint.io/blog/nist-800-53-control-families |
| 24 | Anthropic -- Claude Code Sandboxing | Industry Leader | https://www.anthropic.com/engineering/claude-code-sandboxing |
| 25 | Anthropic -- GTG-1002 Incident | Industry Leader | https://www.anthropic.com/news/disrupting-AI-espionage |
| 26 | Securiti AI -- Anthropic Exploit Analysis | Industry Expert | https://securiti.ai/blog/anthropic-exploit-era-of-ai-agent-attacks/ |
| 27 | Google DeepMind -- Gemini Security Safeguards | Industry Leader | https://deepmind.google/blog/advancing-geminis-security-safeguards/ |
| 28 | Google DeepMind -- Intelligent AI Delegation | Industry Leader / Academic | https://arxiv.org/abs/2602.11865 |
| 29 | Microsoft -- Agent 365 Security | Industry Leader | https://www.microsoft.com/en-us/security/blog/2025/11/18/ambient-and-autonomous-security-for-the-agentic-era/ |
| 30 | Microsoft -- Agent Factory (6-Part Series) | Industry Leader | https://azure.microsoft.com/en-us/blog/agent-factory-creating-a-blueprint-for-safe-and-secure-ai-agents/ |
| 31 | Meta -- Practical AI Agent Security (Rule of Two) | Industry Leader | https://ai.meta.com/blog/practical-ai-agent-security/ |
| 32 | Cisco -- State of AI Security 2026 | Industry Expert | https://blogs.cisco.com/ai/cisco-state-of-ai-security-2026-report |
| 33 | Joint Study -- The Attacker Moves Second | Industry Leader / Academic | https://simonwillison.net/2025/Nov/2/new-prompt-injection-papers/ |
| 34 | MITRE D3FEND Ontology | Standards Body | https://d3fend.mitre.org/ |
| 35 | Center for Threat-Informed Defense -- Mappings Explorer | Industry Expert | https://github.com/center-for-threat-informed-defense/mappings-explorer |
| 36 | Federal Register -- AI Agents Security RFI | US Government | https://www.federalregister.gov/documents/2026/01/08/2026-00206/request-for-information-regarding-security-considerations-for-artificial-intelligence-agents |
| 37 | NIST Draft Guidelines -- Cybersecurity for AI Era | US Government | https://www.nist.gov/news-events/news/2025/12/draft-nist-guidelines-rethink-cybersecurity-ai-era |
| 38 | SecurityScorecard -- NIST CSF 2.0 Guide | Community Expert | https://securityscorecard.com/blog/examining-nist-csf-2-0-everything-you-need-to-know/ |
| 39 | Palo Alto Networks -- OWASP Agentic Top 10 | Industry Expert | https://www.paloaltonetworks.com/blog/cloud-security/owasp-agentic-ai-security/ |
| 40 | Qualys -- OWASP LLM Top 10 2025 Updates | Industry Expert | https://blog.qualys.com/vulnerabilities-threat-research/2024/11/25/ai-under-the-microscope-whats-changed-in-the-owasp-top-10-for-llms-2025 |
| 41 | OWASP GenAI Security Project | Industry Standard | https://genai.owasp.org/ |
