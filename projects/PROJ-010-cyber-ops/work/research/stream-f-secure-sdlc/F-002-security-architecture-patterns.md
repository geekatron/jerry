# F-002: Security Architecture Patterns for Agent Teams

> Stream F: Secure SDLC | PROJ-010 Cyber Ops | Phase 1 Research

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | High-level synthesis of agent security architecture patterns |
| [L1: Key Findings](#l1-key-findings) | Numbered findings with evidence on authorization, isolation, and guardrails |
| [L2: Detailed Analysis](#l2-detailed-analysis) | Deep analysis of patterns, OWASP Agentic AI Top 10, existing tools |
| [Authorization Architecture for /red-team](#authorization-architecture-for-red-team) | Specific patterns for FEAT-015 and FEAT-035 |
| [Evidence and Citations](#evidence-and-citations) | Categorized sources per R-006 |
| [Recommendations](#recommendations) | Numbered recommendations for authorization and guardrail architecture |

---

## L0: Executive Summary

Security architecture for LLM agent teams performing security operations presents unique challenges distinct from both traditional software security and conventional AI safety. This research analyzes authorization patterns, scope control, audit trail design, agent isolation, and guardrail enforcement across the emerging agentic security landscape. The OWASP Top 10 for Agentic Applications (December 2025) identifies 10 risks specific to autonomous AI agents, with Agent Goal Hijack (ASI01), Tool Misuse (ASI02), and Identity and Privilege Abuse (ASI03) being the most directly relevant to /red-team operations. AWS's Agentic AI Security Scoping Matrix provides a 4-level framework categorizing agent architectures by connectivity and autonomy, with corresponding security controls for each level. Production agentic security tools (XBOW, PentAGI, Escape) demonstrate real-world authorization patterns including isolated Docker execution environments, scope-constrained tool access, and automated evidence collection. The critical architectural insight is that authorization scope bounds risk more effectively than human oversight -- agents with properly constrained authorization scopes pose bounded risk regardless of their autonomy level. For /red-team, this means R-020 (scope verification before execution) should be implemented as a layered authorization architecture combining pre-engagement scope definition (red-lead), runtime scope enforcement (per-agent tool access control), and post-execution audit verification (red-reporter), rather than relying solely on human-in-the-loop approval for each action.

---

## L1: Key Findings

### Finding 1: The OWASP Top 10 for Agentic Applications Defines the Canonical Risk Taxonomy for Agent Security

The OWASP GenAI Security Project released the OWASP Top 10 for Agentic Applications in December 2025, developed through collaboration with over 100 security researchers, industry practitioners, and technology providers (OWASP GenAI, December 2025). Unlike the LLM Top 10 which focuses on content generation risks, the Agentic Top 10 addresses risks from autonomous action -- what happens when models can plan, persist, and delegate across tools and systems. The 10 risks are: ASI01 Agent Goal Hijack, ASI02 Tool Misuse, ASI03 Identity and Privilege Abuse, ASI04 Supply Chain Vulnerabilities, ASI05 Unexpected Code Execution, ASI06 Memory and Context Poisoning, ASI07 Insecure Inter-Agent Communication, ASI08 Cascading Failures, ASI09 Human-Agent Trust Exploitation, and ASI10 Rogue Agents. For /red-team specifically, ASI01 (goal hijack redirecting offensive operations), ASI02 (red team tools used beyond authorized scope), ASI03 (privilege abuse accessing out-of-scope systems), and ASI08 (cascading failures in multi-agent exploitation chains) represent the highest-priority risks that the authorization architecture must address.

### Finding 2: Authorization Scope Bounds Risk More Effectively Than Human Oversight

A critical finding from the NIST AI Agent RFI (2025-0035) analysis and production deployment evidence is that authorization scope -- constraining what agents can do -- provides more reliable risk bounding than human oversight -- watching what agents are doing (NIST AI Agent RFI Analysis, 2025). An agent with properly constrained authorization scopes poses bounded risk regardless of autonomy level: an agent that can only read from a specific database, write to a designated output location, and call a limited set of APIs has a defined blast radius. This is directly relevant to R-020 (scope verification before execution): rather than requiring a human to approve every red-lead action, the architecture should define scope constraints that make out-of-scope actions structurally impossible. This aligns with the principle that security is an architectural property, not an operational procedure.

### Finding 3: AWS's Agentic AI Security Scoping Matrix Provides a Graduated Security Control Framework

AWS developed the Agentic AI Security Scoping Matrix that categorizes four distinct agentic architectures based on connectivity and autonomy, mapping security controls across each scope level (AWS Security Blog, 2025). The scopes range from prescribed agency (securing approval workflows) through monitored agency, supervised agency, to full agency (continuous behavioral validation and agency boundary enforcement). For /red-team, this maps to engagement phases: pre-engagement planning operates at prescribed agency (red-lead defines exact scope), active reconnaissance operates at monitored agency (red-recon within defined targets), exploitation operates at supervised agency (red-exploit with scope-checked tool access), and post-exploitation operates at full agency only for pre-approved lateral movement within defined network boundaries. Each escalation in agency requires corresponding escalation in authorization controls, isolation, and audit granularity.

### Finding 4: Production Agentic Security Tools Demonstrate Isolated Execution as the Primary Safety Pattern

XBOW, the autonomous offensive security platform, coordinates hundreds of autonomous AI agents each focused on a specific attack vector. These agents collaborate to discover vulnerabilities, attempt exploit paths, and validate them with proof-of-concept payloads (XBOW, 2025). PentAGI, the open-source alternative, runs fully autonomous penetration testing in isolated Docker environments with a built-in suite of 20+ professional security tools including nmap, metasploit, and sqlmap (GitHub/vxcontrol, 2025). The common architectural pattern across production tools is containerized isolation: each agent or agent group operates within a sandboxed environment with constrained network access, limited filesystem visibility, and scoped tool access. XBOW provides "Pentest On-Demand" where AI agents execute targeted attacks autonomously but within defined application scope boundaries. This validates that autonomous offensive security agents are production-viable when combined with proper isolation and scope enforcement.

### Finding 5: Layered Guardrail Enforcement Is the Emerging Industry Standard

Forrester introduced AEGIS (Agentic AI Guardrails for Information Security) in 2025, a six-domain framework for managing agentic AI safely (BigID, 2025). NVIDIA published practical security guidance for sandboxing agentic workflows that defines credential scoping, network controls, and filesystem restrictions for agent execution environments (NVIDIA Developer Blog, 2025). Enkrypt AI documented a layered guardrail framework with risk taxonomy specific to agent systems (Enkrypt AI, 2025). The convergence across these independent sources establishes layered guardrails as the standard pattern: network layer (allowlists, proxy controls), application layer (tool access policies), agent layer (scope verification, behavioral bounds), and data layer (credential scoping, filesystem restrictions). For /red-team, this translates to: network scope enforcement (only authorized targets reachable), tool scope enforcement (only authorized techniques permitted), agent scope enforcement (red-lead validates all actions against rules of engagement), and data scope enforcement (evidence collection and exfiltration only to authorized repositories).

### Finding 6: Agent Identity and Credential Management Requires Ephemeral, Scoped Credentials

Just-in-time provisioning gives agents scoped, ephemeral identities that match their role (Strata Identity, 2025). Agents do not "log in" the way humans do -- they act continuously, adapt mid-execution, and transition between contexts, so access must be dynamic, context-aware, and enforced at runtime. Organizations should map agent capabilities to specific data domains and business functions to prevent capability creep. For /red-team, this means each agent should have engagement-specific credentials that expire at engagement end, scope-specific network tokens that limit reachability to authorized targets, technique-specific tool access that is granted per rules-of-engagement and revoked when the technique phase completes, and temporal constraints that enforce engagement time windows. The credential broker pattern (NVIDIA, 2025) -- where a trusted intermediary provides short-lived tokens not directly accessible to the agent -- prevents credential leakage even if an agent is compromised.

### Finding 7: Audit Trail and Evidence Collection Must Be Tamper-Evident and Comprehensive

All production agentic security tools implement comprehensive logging as a fundamental architectural requirement. XBOW documents every agent action with timestamps for audit trail reconstruction. PentAGI logs all tool invocations, outputs, and agent decisions within the isolated Docker environment. The OWASP Agentic AI recommendations emphasize that evidence preservation is critical for both regulatory compliance and operational accountability. For /red-team, R-020's evidence preservation requirement should be implemented as a separate audit subsystem that: records all agent actions with timestamps, captures tool inputs and outputs, maintains chain-of-custody for evidence, produces tamper-evident logs (e.g., hash-chained or signed), and generates engagement reports that trace findings back to specific agent actions. red-reporter should consume this audit trail as the authoritative source for engagement documentation.

---

## L2: Detailed Analysis

### OWASP Top 10 for Agentic Applications: Risk Analysis for /red-team

| Risk ID | Risk Name | Description | /red-team Impact | Mitigation Pattern |
|---------|-----------|-------------|------------------|-------------------|
| **ASI01** | Agent Goal Hijack | Adversary manipulates agent goals through hidden prompts or injected instructions | Red team agent goals redirected to unauthorized targets; exploitation tools used against out-of-scope systems | Immutable scope definitions loaded from signed engagement file; goal validation against scope at every decision point |
| **ASI02** | Tool Misuse | Legitimate tools bent into destructive or unauthorized outputs | Red team tools (nmap, metasploit, sqlmap) used against targets not in scope | Tool invocation proxy that validates target parameters against scope before execution; default-deny tool access policy |
| **ASI03** | Identity and Privilege Abuse | Leaked credentials enable operations beyond intended scope | Red team credentials used to access production systems not in engagement scope | Ephemeral, engagement-scoped credentials; credential broker pattern; network-level scope enforcement |
| **ASI04** | Supply Chain Vulnerabilities | Runtime components poisoned or compromised | Red team agent dependencies (tool integrations, libraries) tampered with | Signed agent definitions; verified tool binaries; SLSA provenance for agent runtime |
| **ASI05** | Unexpected Code Execution | Natural-language execution paths enable remote code execution | Agent-generated exploitation scripts execute beyond intended scope | Sandboxed execution environments; code review before execution for C3+ engagements |
| **ASI06** | Memory and Context Poisoning | Agent memory/context manipulated to reshape behavior | Red team agent tactics influenced by poisoned intelligence from compromised sources | Validated intelligence sources; context integrity verification; immutable engagement parameters |
| **ASI07** | Insecure Inter-Agent Communication | Spoofed messages between agents misdirect operations | Fake messages between red-recon and red-exploit cause exploitation of wrong targets | Authenticated inter-agent messaging; signed task delegation; chain-of-authority verification |
| **ASI08** | Cascading Failures | False signals cascade through automated pipelines | Failed exploitation triggers automated escalation beyond scope | Circuit breakers between agent phases; mandatory scope revalidation at phase transitions; blast radius limits |
| **ASI09** | Human-Agent Trust Exploitation | Agent presents misleading confidence to human operators | Red team agent reports false positives as confirmed vulnerabilities, leading to wrong remediation | Mandatory evidence verification; confidence scoring on all findings; /adversary review of reports |
| **ASI10** | Rogue Agents | Agent exhibits misalignment, concealment, or self-directed action | Red team agent conducts unauthorized testing, conceals out-of-scope activity | Comprehensive audit logging; behavioral monitoring; scope verification at every tool invocation |

### Authorization and Scope Control Patterns

#### Pattern 1: Pre-Engagement Scope Definition (Structural Authorization)

The scope definition creates an immutable authorization boundary before any active operations begin. This pattern treats scope as a data artifact, not a prompt instruction.

| Component | Description | Owner | Enforcement |
|-----------|-------------|-------|-------------|
| **Scope Document** | Signed YAML/JSON defining authorized targets, techniques, time windows, exclusions | red-lead | Loaded at engagement start; cannot be modified without re-authorization |
| **Target Allowlist** | Explicit list of IP ranges, domains, applications authorized for testing | red-lead | Network-level enforcement; all agent network access filtered through scope proxy |
| **Technique Allowlist** | MITRE ATT&CK technique IDs authorized for this engagement | red-lead | Tool access gated by technique mapping; unauthorized techniques structurally unavailable |
| **Time Window** | Start/end timestamps for engagement authorization | red-lead | Credential expiration tied to time window; agent access automatically revoked at window close |
| **Exclusion List** | Explicit systems, networks, data types that must not be touched | red-lead | Deny rules checked before every tool invocation; supersede all allow rules |

#### Pattern 2: Runtime Scope Enforcement (Dynamic Authorization)

| Layer | Control | Implementation | Bypass Protection |
|-------|---------|----------------|-------------------|
| **Network** | Target reachability filtering | Proxy/firewall rules derived from scope document; only authorized IPs/ports reachable | Agent cannot bypass network controls without host-level access |
| **Tool** | Tool invocation interception | Every tool call passes through scope-checking middleware that validates target and technique against scope | Tools accessed through API wrapper, not directly; raw tool binaries not on agent PATH |
| **Agent** | Decision-point scope check | Before each operation, agent queries scope oracle with proposed action; oracle returns allow/deny | Scope oracle is a separate process with its own trust domain; agent cannot modify oracle |
| **Data** | Evidence and output controls | Agent can only write to designated evidence repository; no arbitrary file or network output | Output channels whitelisted; all other egress blocked |

#### Pattern 3: Post-Execution Audit Verification (Retrospective Authorization)

| Activity | Description | Owner | Automation |
|----------|-------------|-------|-----------|
| **Action log review** | Every agent action compared against scope document | red-reporter | Automated scope compliance check on action logs |
| **Evidence verification** | All findings traced to authorized actions within scope | red-reporter | Chain-of-custody verification from finding to agent action to scope authorization |
| **Scope deviation detection** | Identify any actions that approached or touched scope boundaries | red-lead | Automated boundary proximity analysis |
| **Compliance report** | Formal attestation that engagement stayed within authorized scope | red-lead, red-reporter | Generated from audit trail; requires red-lead sign-off |

### Agent Isolation and Sandboxing Patterns

#### Isolation Architecture Comparison

| Pattern | Isolation Level | Network Control | Filesystem Control | Credential Model | Used By |
|---------|----------------|-----------------|--------------------|--------------------|---------|
| **Container-per-agent** | Process isolation; shared kernel | Per-container network policy | Read-only rootfs; designated volumes for output | Injected via secrets manager; not in agent context | PentAGI (Docker) |
| **VM-per-engagement** | Full hardware isolation | VM-level firewall rules | Complete filesystem isolation | VM-scoped credential vault | XBOW (implied) |
| **Sandbox-per-execution** | Execution isolation; shared agent process | Execution-scoped network rules | Temp directory per execution; cleaned after | Per-execution token from credential broker | NVIDIA guidance |
| **Namespace-per-team** | Kubernetes namespace isolation | NetworkPolicy per namespace | PVC with access controls | ServiceAccount per agent role | Enterprise DevSecOps |

#### Recommended Isolation Architecture for /red-team

| Component | Pattern | Rationale |
|-----------|---------|-----------|
| **Engagement boundary** | VM-per-engagement or namespace-per-engagement | Complete isolation between engagements; prevents data leakage between engagements |
| **Agent execution** | Container-per-agent-group | Agents in the same kill-chain phase share context but are isolated from other phases |
| **Tool execution** | Sandbox-per-execution | Each tool invocation runs in a fresh sandbox; prevents tool output from contaminating agent state |
| **Evidence storage** | Dedicated volume with append-only writes | Tamper-evident evidence collection; agents can write but not modify or delete |

### Guardrail Enforcement Patterns

#### Guardrail Layer Architecture

| Layer | Guardrail Type | Enforcement Mechanism | /red-team Application |
|-------|---------------|----------------------|-----------------------|
| **L1: Constitutional** | Hard constraints that cannot be violated | Pre-loaded immutable rules; checked before every action | R-020 scope verification; no out-of-scope actions under any circumstances |
| **L2: Policy** | Engagement-specific rules from scope document | Loaded at engagement start; checked at decision points | Authorized targets, techniques, time windows from red-lead scope definition |
| **L3: Behavioral** | Runtime behavioral bounds | Monitored during execution; alerts on anomalous patterns | Circuit breakers if agent behavior deviates from expected patterns (e.g., scanning non-target IPs) |
| **L4: Output** | Output validation and sanitization | Applied to all agent outputs before delivery | Evidence integrity checks; report accuracy verification; confidence scoring |

#### Guardrail Enforcement Decision Table

| Scenario | L1 Action | L2 Action | L3 Action | L4 Action |
|----------|-----------|-----------|-----------|-----------|
| Agent targets out-of-scope system | BLOCK (hard deny) | -- | -- | -- |
| Agent uses unauthorized technique | BLOCK (hard deny) | -- | -- | -- |
| Agent operates outside time window | BLOCK (credential expired) | -- | -- | -- |
| Agent approaches scope boundary | ALLOW | WARN (log proximity) | ALERT (notify red-lead) | -- |
| Agent finds vulnerability in-scope | ALLOW | ALLOW | MONITOR | VERIFY (evidence chain) |
| Agent attempts unknown tool | BLOCK (default deny) | -- | -- | -- |
| Agent produces report with low confidence | ALLOW | ALLOW | ALLOW | HOLD (require verification) |
| Agent exhibits anomalous behavior pattern | ALLOW | ALLOW | ESCALATE (to red-lead) | -- |

### Existing Agentic Security Tool Analysis

#### XBOW: Autonomous Offensive Security Platform

| Aspect | Implementation | Relevance to /red-team |
|--------|---------------|------------------------|
| **Architecture** | Coordinates hundreds of autonomous AI agents, each focused on a specific attack vector | Validates multi-agent offensive security as production-viable |
| **Scope control** | Agents operate within defined application scope boundaries | Demonstrates scope-bounded autonomous exploitation |
| **Agent coordination** | Agents collaborate to discover vulnerabilities, attempt exploit paths, and validate with PoC payloads | Maps to /red-team kill-chain agent coordination |
| **Evidence** | All actions logged with timestamps for audit trail | Validates comprehensive audit trail as architectural requirement |
| **Business model** | "Pentest On-Demand" -- fully automated penetration testing service | Demonstrates commercial viability of autonomous red teaming |
| **Scale** | Machine-speed testing; deeper attack paths than manual testing | Validates agent advantage: breadth and speed beyond human capacity |

#### PentAGI: Open-Source Autonomous Penetration Testing

| Aspect | Implementation | Relevance to /red-team |
|--------|---------------|------------------------|
| **Architecture** | Fully autonomous AI agent that determines and executes penetration testing steps | Validates single-agent autonomous offensive operations |
| **Isolation** | Isolated Docker environments for all security testing operations | Validates container isolation as standard pattern |
| **Tool integration** | Built-in suite of 20+ professional security tools (nmap, metasploit, sqlmap, etc.) | Demonstrates pluggable tool adapter pattern (R-012) |
| **Autonomy** | AI-powered agent automatically determines next penetration testing steps | Validates autonomous decision-making in offensive security |
| **Openness** | Open-source (GitHub: vxcontrol/pentagi) | Provides reference architecture for agent-based pentesting |

#### Escape: API Security Platform

| Aspect | Implementation | Relevance to /red-team |
|--------|---------------|------------------------|
| **Architecture** | Agentic pentesting focused on API security | Demonstrates domain-specific agent specialization |
| **Scope** | API-scoped testing with schema-driven boundaries | Validates schema-based scope enforcement |
| **Evidence** | Detailed vulnerability documentation with remediation guidance | Aligns with R-021 (actionable remediation) |

### Agentic AI Governance Frameworks

| Framework | Source | Date | Key Contributions |
|-----------|--------|------|-------------------|
| **OWASP Top 10 Agentic Applications** | OWASP GenAI Security Project | December 2025 | 10-risk taxonomy; threat-model-based reference; Practical Guide to Securing Agentic Applications |
| **OWASP Agentic AI Threats and Mitigations** | OWASP | 2025 | Detailed threat models with mitigation strategies per risk |
| **AEGIS** | Forrester | 2025 | Six-domain framework: Identity, Data, Access, Monitoring, Governance, Resilience |
| **Agentic AI Security Scoping Matrix** | AWS | 2025 | 4-level autonomy classification with mapped security controls |
| **Singapore Model AI Governance Framework for Agentic AI** | IMDA Singapore | 2025 | Government governance framework for agentic AI systems |
| **NIST AI RMF** | NIST | 2025 | Risk Management Framework for AI systems including agents |
| **ISO 42001** | ISO | 2023 | AI management system standard with risk assessment and transparency requirements |
| **OWASP LLMSVS** | OWASP | 2025 | LLM Security Verification Standard for pentesting LLM-integrated apps |

---

## Authorization Architecture for /red-team

### FEAT-015 and FEAT-035 Authorization Requirements Mapping

Based on PLAN.md requirements R-020 (authorization verification), R-021 (actionable remediation), and the authorization control table in the PLAN, the following architecture integrates research findings into concrete design patterns for /red-team.

#### Authorization Flow

```
1. SCOPE DEFINITION (Pre-Engagement)
   red-lead defines:
   - Target allowlist (IPs, domains, applications)
   - Technique allowlist (ATT&CK technique IDs)
   - Time window (start/end timestamps)
   - Exclusion list (explicit deny)
   - Rules of engagement (engagement-specific constraints)
   - Evidence handling requirements

2. SCOPE COMPILATION (Engagement Start)
   Scope document is:
   - Validated for completeness and consistency
   - Signed by red-lead (and optionally by user/client)
   - Compiled into machine-enforceable rules
   - Distributed to scope enforcement infrastructure

3. RUNTIME ENFORCEMENT (Active Engagement)
   Every agent action is:
   - Intercepted by scope enforcement middleware
   - Validated against compiled scope rules
   - Logged to tamper-evident audit trail
   - Allowed (in-scope) or blocked (out-of-scope)

4. PHASE TRANSITION VERIFICATION
   At each kill-chain phase transition:
   - Current phase scope compliance verified
   - Next phase authorization confirmed
   - Scope revalidation if engagement conditions changed
   - Circuit breaker check for cascading failure patterns

5. EVIDENCE COLLECTION (Continuous)
   Throughout engagement:
   - All actions recorded with timestamps
   - Tool inputs/outputs captured
   - Findings linked to specific authorized actions
   - Chain-of-custody maintained for all evidence

6. POST-ENGAGEMENT AUDIT
   red-reporter generates:
   - Scope compliance attestation
   - Finding-to-authorization trace
   - Scope boundary proximity report
   - Engagement timeline with action-scope mapping
```

#### Per-Agent Authorization Model

| Agent | Authorization Level | Tool Access | Network Scope | Data Access |
|-------|---------------------|-------------|--------------|-------------|
| **red-lead** | Full engagement scope; can define/modify scope | All coordination tools | All authorized targets (for verification) | Full audit trail; scope documents |
| **red-recon** | Reconnaissance scope only | Passive/active recon tools only (nmap, Shodan, DNS tools) | Authorized target IPs/domains only | Target enumeration data; no exploit output |
| **red-vuln** | Analysis scope; read-only against targets | Vulnerability scanners, CVE databases | Authorized targets (scan only, no exploitation) | Scan results; CVE data; no credentials |
| **red-exploit** | Exploitation scope; target + technique allowlist | Exploitation frameworks (Metasploit, custom), within technique allowlist | Authorized targets only; port-level restrictions | Exploitation artifacts; PoC outputs |
| **red-privesc** | Post-exploitation scope; compromised host only | Privilege escalation tools on compromised hosts | Compromised host only (until lateral movement authorized) | Local host data; credential material |
| **red-lateral** | Lateral movement scope; authorized network range | Pivoting tools, C2 usage | Authorized network range; red-infra C2 infrastructure | Internal network data within scope |
| **red-persist** | Persistence scope; if authorized in RoE | Persistence mechanism tools | Compromised hosts within scope | Host-level configuration |
| **red-exfil** | Exfiltration scope; data types specified in RoE | Data identification and transfer tools | Evidence repository only (no external exfil) | Classified data within engagement scope |
| **red-infra** | Infrastructure scope; engagement infra only | C2 frameworks, payload builders, redirectors | Engagement infrastructure network | C2 infrastructure; payload artifacts |
| **red-social** | Social engineering scope; if authorized in RoE | Phishing tools, pretexting frameworks | Email/communication channels as authorized | Contact lists; social data within scope |
| **red-reporter** | Report scope; read-only on all engagement data | Report generation tools | Evidence repository (read); report delivery (write) | Full engagement data (read-only) |

#### Scope Enforcement Architecture

| Component | Function | Trust Level | Failure Mode |
|-----------|----------|-------------|--------------|
| **Scope Document Store** | Immutable storage for signed scope definitions | Highest -- cannot be modified by agents | Engagement cannot start without valid scope |
| **Scope Oracle** | Evaluates proposed actions against scope rules | High -- separate process, own trust domain | Default deny; agents cannot operate if oracle unavailable |
| **Tool Proxy** | Intercepts all tool invocations; validates against scope | High -- agents access tools only through proxy | Tools inaccessible without proxy; no direct tool access |
| **Network Enforcer** | Firewall/proxy rules derived from scope | High -- infrastructure-level enforcement | No network access outside scope; fail-closed |
| **Audit Logger** | Records all actions to tamper-evident log | High -- append-only; separate from agent access | Engagement pauses if audit system fails |
| **Evidence Vault** | Stores all engagement artifacts with chain-of-custody | High -- append-only for agents; read by red-reporter | Evidence preserved even if agent systems fail |
| **Circuit Breaker** | Monitors for cascading failures and scope boundary proximity | Medium -- advisory and escalation | Alerts red-lead; does not independently halt engagement |

---

## Evidence and Citations

### Industry Leaders

| Source | Date | Content |
|--------|------|---------|
| [OWASP Top 10 for Agentic Applications](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) | December 2025 | ASI01-ASI10 risk taxonomy for autonomous AI agents |
| [OWASP GenAI Security Project -- Agentic Applications Announcement](https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/) | December 2025 | Benchmark for agentic security; 100+ researcher collaboration |
| [OWASP -- Agentic AI Threats and Mitigations](https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/) | 2025 | Threat-model-based reference for emerging agentic threats |
| [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) | 2025 | LLM-specific risk taxonomy (distinct from Agentic Top 10) |
| [AWS -- Agentic AI Security Scoping Matrix](https://aws.amazon.com/blogs/security/the-agentic-ai-security-scoping-matrix-a-framework-for-securing-autonomous-ai-systems/) | 2025 | 4-level autonomy classification with mapped security controls |
| [AWS -- Securing Agentic AI (Detailed)](https://aws.amazon.com/ai/security/agentic-ai-scoping-matrix/) | 2025 | Comprehensive agentic AI security framework |
| [IBM -- Agentic AI Security Guide](https://www.ibm.com/think/insights/agentic-ai-security) | 2025 | Enterprise agentic AI security guidance |
| [NVIDIA -- Practical Security Guidance for Sandboxing Agentic Workflows](https://developer.nvidia.com/blog/practical-security-guidance-for-sandboxing-agentic-workflows-and-managing-execution-risk) | 2025 | Credential scoping, network controls, filesystem restrictions for agent sandboxing |
| [Singapore IMDA -- Model AI Governance Framework for Agentic AI](https://www.imda.gov.sg/-/media/imda/files/about/emerging-tech-and-research/artificial-intelligence/mgf-for-agentic-ai.pdf) | 2025 | Government governance framework for agentic AI |

### Industry Experts

| Source | Date | Content |
|--------|------|---------|
| [BleepingComputer -- Real-World Attacks Behind OWASP Agentic AI Top 10](https://www.bleepingcomputer.com/news/security/the-real-world-attacks-behind-owasp-agentic-ai-top-10/) | 2025 | Real-world attack examples mapped to ASI01-ASI10 |
| [Human Security -- OWASP Top 10 Agentic AI Risks Explained](https://www.humansecurity.com/learn/blog/owasp-top-10-agentic-applications/) | 2025 | Detailed explanations of each agentic AI risk |
| [Practical DevSecOps -- OWASP Top 10 Agentic Applications](https://www.practical-devsecops.com/owasp-top-10-agentic-applications/) | 2025 | Practical DevSecOps perspective on agentic risks |
| [Palo Alto Networks -- OWASP Agentic AI Security](https://www.paloaltonetworks.com/blog/cloud-security/owasp-agentic-ai-security/) | 2025 | Cloud security implications of agentic AI risks |
| [NIST AI Agent RFI (2025-0035) Analysis](https://www.rockcybermusings.com/p/nist-ai-agent-rfi-2025-0035-human-oversight-wrong-fix) | 2025 | Authorization scope vs. human oversight; NIST AI governance |
| [Strata Identity -- 8 Strategies for AI Agent Security](https://www.strata.io/blog/agentic-identity/8-strategies-for-ai-agent-security-in-2025/) | 2025 | JIT provisioning, ephemeral identities, dynamic access for agents |
| [Obsidian Security -- 2025 AI Agent Security Landscape](https://www.obsidiansecurity.com/blog/ai-agent-market-landscape) | 2025 | Market landscape analysis of AI agent security players and trends |
| [Koi AI -- OWASP Agentic AI Top 10 Practical Guide](https://www.koi.ai/blog/owasp-agentic-ai-top-10-a-practical-security-guide) | 2025 | Practical security guide for OWASP agentic risks |
| [Asteros -- Penetration Testing LLM-Integrated Apps Using OWASP LLMSVS](https://asteros.com/2025/04/penetration-testing-llm-integrated-apps-using-the-owasp-llmsvs/) | April 2025 | OWASP LLM Security Verification Standard for pentesting |

### Industry Innovators

| Source | Date | Content |
|--------|------|---------|
| [XBOW -- Autonomous Offensive Security Platform](https://xbow.com) | 2025 | Hundreds of autonomous AI agents for vulnerability discovery and exploitation |
| [XBOW -- Pentest On-Demand Announcement](https://www.businesswire.com/news/home/20251112470912/en/Announcing-XBOW-Pentest-On-Demand-for-Security-at-Machine-Speed) | November 2025 | Fully automated penetration testing at machine speed |
| [XBOW -- Web Application Penetration Testing](https://xbow.com/pentest) | 2025 | AI-powered web application security testing |
| [PentAGI (GitHub: vxcontrol/pentagi)](https://github.com/vxcontrol/pentagi) | 2025 | Open-source autonomous AI penetration testing with Docker isolation |
| [Escape -- Agentic Pentesting Tools Comparison](https://escape.tech/blog/best-agentic-pentesting-tools/) | 2025 | In-depth comparison of agentic pentesting platforms |
| [Vanta + XBOW Partnership](https://www.businesswire.com/news/home/20250805805375/en/Vanta-Partners-with-XBOW-to-Deliver-Autonomous-Penetration-Testing-to-Startups) | August 2025 | Enterprise adoption of autonomous pentesting |
| [Enkrypt AI -- Securing AI Agents with Layered Guardrails](https://www.enkryptai.com/blog/securing-ai-agents-a-comprehensive-framework-for-agent-guardrails) | 2025 | Comprehensive agent guardrail framework with risk taxonomy |
| [BigID -- AEGIS Explained: Guardrails for Autonomous AI Systems](https://bigid.com/blog/what-is-aegis/) | 2025 | Forrester AEGIS framework analysis |

### Community Leaders

| Source | Date | Content |
|--------|------|---------|
| [OWASP Agentic Security Initiative (ASI)](https://owasp.org/www-project-top-10-for-large-language-model-applications/initiatives/agent_security_initiative/) | 2025 | Official OWASP ASI project page |
| [Rippling -- Agentic AI Security Guide](https://www.rippling.com/blog/agentic-ai-security) | 2025 | Enterprise agentic AI security best practices |
| [Skywork AI -- Agentic AI Safety Best Practices 2025](https://skywork.ai/blog/agentic-ai-safety-best-practices-2025-enterprise/) | 2025 | Enterprise guardrails and safety patterns for agentic AI |

### Community Experts

| Source | Date | Content |
|--------|------|---------|
| [CybersecurityNews -- PentAGI Analysis](https://cybersecuritynews.com/pentagi-penetration-testing-tool/) | 2025 | PentAGI tool analysis and 20+ tool integration details |
| [VPNCentral -- PentAGI Tool Integration](https://vpncentral.com/pentagi-ai-powered-penetration-testing-tool-integrates-20-security-tools-for-automated-assessments/) | 2025 | Detailed PentAGI security tool integration analysis |
| [Lares Labs -- OWASP Agentic Top 10: Threats in the Wild](https://labs.lares.com/owasp-agentic-top-10/) | 2025 | Real-world threat examples for each agentic risk |
| [Lasso Security -- OWASP Top 10 for Agentic Applications](https://www.lasso.security/blog/owasp-top-10-for-agentic-applications) | 2025 | Detailed agentic risk analysis with mitigation strategies |
| [Toloka AI -- Essential AI Agent Guardrails](https://toloka.ai/blog/essential-ai-agent-guardrails-for-safe-and-ethical-implementation/) | 2025 | Practical guardrail implementation guidance |

### Community Innovators

| Source | Date | Content |
|--------|------|---------|
| [Medium (Aaron Brown) -- Building Leading Open-Source Pentesting Agent](https://medium.com/data-science-collective/building-the-leading-open-source-pentesting-agent-architecture-lessons-from-xbow-benchmark-f6874f932ca4) | 2025 | Architecture lessons from XBOW benchmark for agent-based pentesting |
| [Security Boulevard -- Best Agentic Pentesting Tools 2026](https://securityboulevard.com/2025/12/best-agentic-pentesting-tools-in-2026/) | December 2025 | Comprehensive agentic pentesting tool comparison |
| [Idan Habler (Medium) -- Demystifying OWASP Top 10 for Agentic Applications](https://idanhabler.medium.com/demystifying-the-owasp-top-10-for-agentic-applications-4eedba941b2c) | December 2025 | Practitioner analysis of agentic AI risks |
| [ArXiv -- AI Agent Code of Conduct: Automated Guardrail Policy-as-Prompt Synthesis](https://arxiv.org/html/2509.23994v1) | 2025 | Academic research on automated guardrail generation |

---

## Recommendations

### R-AUTH-001: Implement Layered Authorization Architecture for /red-team

/red-team MUST implement a layered authorization architecture combining structural authorization (pre-engagement scope definition by red-lead), runtime enforcement (scope oracle and tool proxy for every agent action), and retrospective verification (post-engagement audit by red-reporter). This three-layer approach addresses OWASP ASI01 (goal hijack), ASI02 (tool misuse), and ASI03 (identity abuse) simultaneously. Priority: HIGH.

### R-AUTH-002: Adopt Default-Deny Tool Access Policy

Every /red-team agent MUST operate under a default-deny tool access policy where tools are explicitly granted per engagement scope, not implicitly available. Tools should be accessed through a scope-validating proxy that checks target and technique parameters against the engagement scope document before permitting execution. This directly implements R-020 (scope verification before execution) at the architectural level. Priority: HIGH.

### R-AUTH-003: Implement Scope Oracle as Separate Trust Domain

The scope enforcement mechanism MUST operate in a separate trust domain from the agents it governs. Agents must not be able to modify, bypass, or disable scope enforcement. The scope oracle should be an independent service that evaluates proposed actions against the signed scope document and returns allow/deny decisions. This addresses the core OWASP ASI10 (rogue agents) risk. Priority: HIGH.

### R-AUTH-004: Use Ephemeral, Engagement-Scoped Credentials

All /red-team agent credentials MUST be ephemeral (time-bounded to engagement window), scope-bounded (limited to authorized targets and techniques), and broker-mediated (provided by a credential broker not directly accessible to agents). This follows the NVIDIA credential broker pattern and Strata Identity JIT provisioning guidance to limit blast radius in case of agent compromise. Priority: HIGH.

### R-AUTH-005: Implement Tamper-Evident Audit Trail

All /red-team agent actions MUST be logged to a tamper-evident audit system (hash-chained or signed log entries) that is append-only for agents and read-only for red-reporter. The audit trail must capture: action timestamp, agent identity, tool invocation details, target parameters, scope oracle decision, and action result. This satisfies R-020's evidence preservation requirement. Priority: HIGH.

### R-AUTH-006: Implement Circuit Breakers at Phase Transitions

The /red-team workflow MUST include circuit breaker checks at every kill-chain phase transition. Before an agent passes findings to the next phase agent (e.g., red-recon to red-vuln, red-exploit to red-privesc), the circuit breaker verifies scope compliance of the current phase and confirms authorization for the next phase. This addresses OWASP ASI08 (cascading failures) where errors propagate through the agent chain. Priority: MEDIUM.

### R-AUTH-007: Address All 10 OWASP Agentic AI Risks in Architecture

The /red-team and /eng-team architectures MUST include explicit mitigations for all 10 OWASP Agentic AI risks (ASI01 through ASI10). The risk-to-mitigation mapping in the L2 analysis table should be formalized into architectural requirements during Phase 2 Architecture. Priority: HIGH.

### R-AUTH-008: Design Agent Isolation Following Production Tool Patterns

/red-team agent execution SHOULD follow the isolation patterns demonstrated by XBOW and PentAGI: containerized execution environments, scoped network access, limited filesystem visibility, and separate evidence storage. The specific isolation granularity (container-per-agent vs. container-per-phase) should be determined during Phase 2 Architecture based on performance and coordination requirements. Priority: MEDIUM.

### R-AUTH-009: Implement Progressive Autonomy Deployment

When deploying /red-team, organizations SHOULD follow the AWS Agentic AI Security Scoping Matrix's progressive autonomy pattern: start with prescribed agency (human approves every action), advance to monitored agency (human reviews logs in near-real-time), then supervised agency (human reviews at phase boundaries), and finally full agency (human reviews engagement summary) as organizational confidence grows. This reduces deployment risk while building operational experience. Priority: MEDIUM.

### R-AUTH-010: Validate Authorization Architecture Through Purple Team Exercise

During Phase 5 (Purple Team Validation), /red-team's authorization architecture MUST be specifically tested: attempt out-of-scope actions, verify they are blocked; verify audit trail captures all blocked attempts; verify circuit breakers trigger on cascading failure patterns; verify credential expiration enforces time windows. Authorization architecture is a security control and must be validated like any other security control. Priority: HIGH.
