# PROJ-008: Data Sources & Repository Registry

> Authoritative data sources for MITRE, OWASP, and NIST framework consumption. All sources verified via Context7, WebSearch, and direct GitHub exploration.

## Document Sections

| Section | Purpose |
|---------|---------|
| [MITRE Repositories](#mitre-repositories) | ATT&CK, ATLAS, CTI GitHub repos |
| [NIST Repositories](#nist-repositories) | OSCAL, SP 800-53, CSF data repos |
| [OWASP Resources](#owasp-resources) | LLM Top 10, API Security, Cheat Sheets |
| [MITRE Defensive Tools](#mitre-defensive-tools) | D3FEND, Mappings Explorer, CALDERA |
| [Industry Guidance](#industry-guidance) | Anthropic, Microsoft, Google, Cisco, Meta, OWASP GenAI |
| [Python Libraries](#python-libraries) | Programmatic consumption tools |
| [Key Research Findings](#key-research-findings) | Critical findings from initial research |
| [Citations](#citations) | All sources with authority classification |

---

## MITRE Repositories

### ATT&CK Enterprise (STIX 2.1 Data)

| Field | Value |
|-------|-------|
| Repository | [mitre-attack/attack-stix-data](https://github.com/mitre-attack/attack-stix-data) |
| Format | STIX 2.1 JSON collections |
| Matrices | Enterprise, Mobile, ICS |
| Reputation | High (Context7 verified, benchmark 87.5) |
| Consumption | Load JSON → `stix2.MemoryStore` → query techniques, tactics, mitigations |
| Key File | `enterprise-attack/enterprise-attack.json` (latest), versioned files available |

**Usage (from Context7):**
```python
from stix2 import MemoryStore
import requests

def get_attack_data(domain):
    stix_json = requests.get(
        f"https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/{domain}/{domain}.json"
    ).json()
    return MemoryStore(stix_data=stix_json["objects"])

enterprise_src = get_attack_data("enterprise-attack")
mobile_src = get_attack_data("mobile-attack")
```

### ATT&CK Python Library

| Field | Value |
|-------|-------|
| Repository | [mitre-attack/mitreattack-python](https://github.com/mitre-attack/mitreattack-python) |
| Package | `mitreattack-python` (pip/uv) |
| Reputation | High (Context7 verified, 95 code snippets) |
| Capabilities | Query STIX data, export to Excel/DataFrames, Navigator layer manipulation |
| Install | `uv add mitreattack-python` |

**Usage (from Context7):**
```python
from mitreattack.stix20 import MitreAttackData

mitre_attack_data = MitreAttackData("enterprise-attack.json")
technique = mitre_attack_data.get_object_by_attack_id('T1134', 'attack-pattern')
tactic = mitre_attack_data.get_object_by_attack_id("TA0001")
mitigations = mitre_attack_data.get_mitigations(remove_revoked_deprecated=True)
```

### MITRE CTI (Cyber Threat Intelligence)

| Field | Value |
|-------|-------|
| Repository | [mitre/cti](https://github.com/mitre/cti) |
| Format | STIX 2.0 |
| Content | ATT&CK and CAPEC datasets |
| Reputation | High (Context7 verified, benchmark 85.8) |

### MITRE ATLAS (AI Threat Landscape)

| Field | Value |
|-------|-------|
| Repository | [mitre-atlas/atlas-data](https://github.com/mitre-atlas/atlas-data) |
| Original Repo | [mitre/advmlthreatmatrix](https://github.com/mitre/advmlthreatmatrix) |
| Organization | [github.com/mitre-atlas](https://github.com/mitre-atlas) |
| Format | STIX 2.1 bundle (ATT&CK data model compatible) |
| Coverage | 15 tactics, 66 techniques, 46 sub-techniques, 26 mitigations, 33 case studies |
| 2025 Update | 14 new techniques for AI agents (prompt injection, memory manipulation) |
| Website | [atlas.mitre.org](https://atlas.mitre.org/) |
| Source | [Vectra AI](https://www.vectra.ai/topics/mitre-atlas), [Practical DevSecOps](https://www.practical-devsecops.com/mitre-atlas-framework-guide-securing-ai-systems/) |

### ATLAS Navigator Data (STIX 2.1 Bridge)

| Field | Value |
|-------|-------|
| Repository | [mitre-atlas/atlas-navigator-data](https://github.com/mitre-atlas/atlas-navigator-data) |
| Format | STIX 2.1 JSON + ATT&CK Navigator layers |
| Stars | 23 |
| Purpose | ATLAS data converted to STIX 2.1; enables unified ATT&CK + ATLAS visualization |

### ATT&CK Navigator

| Field | Value |
|-------|-------|
| Repository | [mitre-attack/attack-navigator](https://github.com/mitre-attack/attack-navigator) |
| Stars | 2,328 |
| License | Apache-2.0 |
| Purpose | Visualization and annotation of ATT&CK matrices; supports custom coverage layers |
| Programmatic | Generate layers via `mitreattack-python` `navlayers` module |

### STIX Python Library

| Field | Value |
|-------|-------|
| Repository | [oasis-open/cti-python-stix2](https://github.com/oasis-open/cti-python-stix2) |
| Package | `stix2` (pip/uv) |
| Reputation | High (Context7 verified, 188 code snippets, benchmark 82.5) |
| Capabilities | Create, parse, and query STIX 2 objects |
| Install | `uv add stix2` |

---

## MITRE Defensive Tools

### D3FEND (Defensive Knowledge Graph)

| Field | Value |
|-------|-------|
| Repository | [d3fend/d3fend-ontology](https://github.com/d3fend/d3fend-ontology) |
| Stars | 98 |
| License | MIT |
| Format | OWL ontology (Turtle) |
| Website | [d3fend.mitre.org](https://d3fend.mitre.org/) |
| Coverage | 267 defensive techniques across 7 tactical categories (Model, Harden, Detect, Isolate, Deceive, Evict, Restore) |
| ATT&CK Mapping | [d3fend.mitre.org/mappings/attack-mitigations](https://d3fend.mitre.org/mappings/attack-mitigations/) |
| Purpose | **Defensive complement to ATT&CK** -- machine-readable mapping from attacker techniques to defender countermeasures |

### Mappings Explorer (ATT&CK to Controls)

| Field | Value |
|-------|-------|
| Repository | [center-for-threat-informed-defense/mappings-explorer](https://github.com/center-for-threat-informed-defense/mappings-explorer) |
| Stars | 90 |
| License | Apache-2.0 |
| Purpose | Maps NIST 800-53, CIS Controls, NIST CSF to ATT&CK techniques |
| Consumption | Structured data files for automated coverage analysis |

### CALDERA (Adversary Emulation Platform)

| Field | Value |
|-------|-------|
| Repository | [mitre/caldera](https://github.com/mitre/caldera) |
| Stars | 6,759 |
| License | Apache-2.0 |
| Purpose | Automated adversary emulation built on ATT&CK; includes `caldera-atlas` plugin for AI adversary emulation |

---

## NIST Repositories

### OSCAL (Open Security Controls Assessment Language)

| Field | Value |
|-------|-------|
| Repository | [usnistgov/OSCAL](https://github.com/usnistgov/OSCAL) |
| Content | OSCAL specification, schemas, tooling |
| Formats | XML, JSON, YAML |
| Purpose | Standardized machine-readable security control representations |

### OSCAL Content (SP 800-53 Controls)

| Field | Value |
|-------|-------|
| Repository | [usnistgov/oscal-content](https://github.com/usnistgov/oscal-content) |
| Key Path | `nist.gov/SP800-53/rev5/` |
| Formats | XML, JSON, YAML |
| Content | SP 800-53 Rev 5 catalog + SP 800-53B baselines |
| YAML Catalog | [NIST_SP-800-53_rev5_catalog.yaml](https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev5/yaml/NIST_SP-800-53_rev5_catalog.yaml) |
| JSON Catalog | Available at same path with `.json` extension |

### NIST CSF 2.0

| Field | Value |
|-------|-------|
| URL | [csrc.nist.gov](https://csrc.nist.gov/projects/cybersecurity-framework) |
| Functions | Identify, Protect, Detect, Respond, Recover, Govern |
| Status | Published February 2024, current as of 2026 |

### NIST AI RMF (600-1) and GenAI Profile (AI 600-1)

| Field | Value |
|-------|-------|
| AI RMF 1.0 | [nist.gov/itl/ai-risk-management-framework](https://www.nist.gov/itl/ai-risk-management-framework) |
| GenAI Profile | [NIST AI 600-1 PDF](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) |
| AI Resource Center | [airc.nist.gov](https://airc.nist.gov) |
| Functions | GOVERN, MAP, MEASURE, MANAGE |
| GenAI Coverage | 12 GAI risk categories (released July 2024) |
| Community Data | [JonathanBowker/NIST-AI-Risk-Management-Framework](https://github.com/JonathanBowker/NIST-AI-Risk-Management-Framework) (XLSX) |

### NIST CSF Profile for AI (IR 8596 -- Draft)

| Field | Value |
|-------|-------|
| URL | [csrc.nist.gov/pubs/ir/8596/iprd](https://csrc.nist.gov/pubs/ir/8596/iprd) |
| Published | December 16, 2025 |
| Purpose | Overlays 3 AI Focus Areas on CSF 2.0: Secure (AI implementations), Detect (AI for cybersecurity), Thwart (adversarial AI) |
| Agent Note | "AI agent systems are capable of taking autonomous actions that impact real-world systems and may be susceptible to hijacking, backdoor attacks, and other exploits" |
| RFI | [Federal Register: Security Considerations for AI Agents](https://www.federalregister.gov/documents/2026/01/08/2026-00206/request-for-information-regarding-security-considerations-for-artificial-intelligence-agents) (Jan 2026) |

### NIST CSF 2.0 MCP Server (Community)

| Field | Value |
|-------|-------|
| Repository | [rocklambros/nist-csf-2-mcp-server](https://github.com/rocklambros/nist-csf-2-mcp-server) |
| Stars | 52 |
| Purpose | MCP server for NIST CSF 2.0 queries -- directly relevant for agentic AI security tooling |

### NVD API

| Field | Value |
|-------|-------|
| API | [nvd.nist.gov/developers/vulnerabilities](https://nvd.nist.gov/developers/vulnerabilities) |
| Python Library | [vehemont/nvdlib](https://github.com/vehemont/nvdlib) (111 stars) |
| MCP Server | [marcoeg/mcp-nvd](https://github.com/marcoeg/mcp-nvd) (MCP protocol access to NVD) |

---

## OWASP Resources

### OWASP Top 10 for LLM Applications 2025

| Field | Value |
|-------|-------|
| URL | [genai.owasp.org/llm-top-10](https://genai.owasp.org/llm-top-10/) |
| PDF | [OWASP-Top-10-for-LLMs-v2025.pdf](https://owasp.org/www-project-top-10-for-large-language-model-applications/assets/PDF/OWASP-Top-10-for-LLMs-v2025.pdf) |
| Context7 ID | `/owasp/top10` (347 snippets, High reputation) |
| Items | LLM01-LLM10 |

**Full List:**

| ID | Name | Agentic Relevance |
|----|------|--------------------|
| LLM01 | Prompt Injection | CRITICAL -- direct and indirect injection via tool results, MCP data |
| LLM02 | Sensitive Information Disclosure | HIGH -- agent may leak system prompts, credentials, internal state |
| LLM03 | Supply Chain | HIGH -- MCP servers, dependencies, model provenance |
| LLM04 | Data and Model Poisoning | MEDIUM -- training data integrity, fine-tuning attacks |
| LLM05 | Improper Output Handling | HIGH -- agent output consumed by downstream systems |
| LLM06 | Excessive Agency | CRITICAL -- agents with too many tools/permissions |
| LLM07 | System Prompt Leakage | HIGH -- governance rules, constitutional constraints exposed |
| LLM08 | Vector and Embedding Weaknesses | MEDIUM -- RAG poisoning, embedding manipulation |
| LLM09 | Misinformation | MEDIUM -- agent generates false security guidance |
| LLM10 | Unbounded Consumption | HIGH -- token exhaustion, denial of service via agent loops |

Source: [OWASP GenAI](https://genai.owasp.org/llmrisk/llm01-prompt-injection/), [Invicti](https://www.invicti.com/blog/web-security/owasp-top-10-risks-llm-security-2025/), [Oligo Security](https://www.oligo.security/academy/owasp-top-10-llm-updated-2025-examples-and-mitigation-strategies)

### OWASP Top 10 for Agentic Applications (2026) -- CRITICAL

| Field | Value |
|-------|-------|
| URL | [genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) |
| Released | December 10, 2025 |
| Threats & Mitigations | [genai.owasp.org/resource/agentic-ai-threats-and-mitigations/](https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/) |
| Community Repo | [precize/Agentic-AI-Top10-Vulnerability](https://github.com/precize/Agentic-AI-Top10-Vulnerability) (171 stars) |
| Dataset | [evolutionstorm/owasp-agentic-security-dataset](https://github.com/evolutionstorm/owasp-agentic-security-dataset) (JSON/YAML) |
| Static Analyzer | [HeadyZhang/agent-audit](https://github.com/HeadyZhang/agent-audit) (40+ rules, MCP config auditing) |
| Cross-Framework Mapping | [emmanuelgjr/owaspllmtop10mapping](https://github.com/emmanuelgjr/owaspllmtop10mapping) (maps to NIST/ISO/MITRE) |

**Full List:**

| ID | Name | Agentic Relevance |
|----|------|--------------------|
| ASI01 | Agent Goal Hijack | CRITICAL -- attackers manipulate agent objectives through poisoned inputs |
| ASI02 | Tool Misuse | CRITICAL -- agents invoke tools exceeding intended scope |
| ASI03 | Privilege Escalation | HIGH -- agents inherit or accumulate excessive permissions |
| ASI04 | Delegated Trust Boundary Violations | HIGH -- trust boundaries breached during inter-agent delegation |
| ASI05 | Memory and Context Manipulation | HIGH -- poisoning of agent memory stores and context |
| ASI06 | Identity and Access Mismanagement | HIGH -- agents without unique identities or proper auth |
| ASI07 | Insecure Inter-Agent Communication | HIGH -- spoofed messages misdirect agent clusters |
| ASI08 | Cascading Failures | MEDIUM -- false signals cascade through automated pipelines |
| ASI09 | Insufficient Logging and Monitoring | MEDIUM -- lack of observability into agent actions |
| ASI10 | Rogue Agents | CRITICAL -- compromised agents acting harmfully while appearing legitimate |

### OWASP AI Agent Security Cheat Sheet

| Field | Value |
|-------|-------|
| URL | [cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet) |
| Context7 ID | `/websites/cheatsheetseries_owasp` (3491 snippets, High reputation, benchmark 65.3) |
| Key Patterns | SecureAgentMemory, SecureLLMPipeline, PromptInjectionFilter |

### OWASP LLM Prompt Injection Prevention Cheat Sheet

| Field | Value |
|-------|-------|
| URL | [cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet) |
| Key Patterns | Input validation layers, HITL for high-risk inputs, sanitization, structured prompts, output validation |

---

## Industry Guidance

### Anthropic -- Claude Agent SDK Security

| Field | Value |
|-------|-------|
| Agent SDK Docs | [platform.claude.com/docs/en/agent-sdk/overview](https://platform.claude.com/docs/en/agent-sdk/overview) |
| Safeguards Blog | [anthropic.com/news/building-safeguards-for-claude](https://www.anthropic.com/news/building-safeguards-for-claude) |
| Authority | Industry Leader |
| Key Findings | Sandboxed containers, tool registration with schemas, permission approval workflows |
| Security Incident | Nov 2025: Chinese state-sponsored attack using Claude Code -- "model-level guardrails function as architectural suggestions, not enforcement mechanisms" |
| Source | [Securiti AI](https://securiti.ai/blog/anthropic-exploit-era-of-ai-agent-attacks/), [The New Stack](https://thenewstack.io/anthropic-agent-sdk-confusion/) |
| Implication | **Validates Jerry's approach**: deterministic L3/L5 enforcement > behavioral guardrails |

### Microsoft -- Agent 365 & AI Agent Security

| Field | Value |
|-------|-------|
| Agent 365 Blog | [microsoft.com/microsoft-365/blog/2025/11/18/microsoft-agent-365-the-control-plane-for-ai-agents](https://www.microsoft.com/en-us/microsoft-365/blog/2025/11/18/microsoft-agent-365-the-control-plane-for-ai-agents/) |
| Security Blog | [microsoft.com/security/blog/2025/11/18/ambient-and-autonomous-security-for-the-agentic-era](https://www.microsoft.com/en-us/security/blog/2025/11/18/ambient-and-autonomous-security-for-the-agentic-era/) |
| Core Primitive | [techcommunity.microsoft.com -- Security as the core primitive](https://techcommunity.microsoft.com/blog/microsoft-security-blog/security-as-the-core-primitive---securing-ai-agents-and-apps/4470197) |
| Fortune 500 Report | [microsoft.com/security/blog/2026/02/10/80-of-fortune-500-use-active-ai-agents](https://www.microsoft.com/en-us/security/blog/2026/02/10/80-of-fortune-500-use-active-ai-agents-observability-governance-and-security-shape-the-new-frontier/) |
| Agent 365 Security | [learn.microsoft.com/security/security-for-ai/agent-365-security](https://learn.microsoft.com/en-us/security/security-for-ai/agent-365-security) |
| Authority | Industry Leader |
| Key Concepts | Agent ID (unique identity per agent), control plane/data plane separation, Entra-based access control, Purview data protection, Defender integration, risk-based adaptive policies |

### Anthropic -- Claude Code Sandboxing Architecture

| Field | Value |
|-------|-------|
| URL | [anthropic.com/engineering/claude-code-sandboxing](https://www.anthropic.com/engineering/claude-code-sandboxing) |
| Authority | Industry Leader |
| Key Findings | Filesystem isolation (bubblewrap/seatbelt), network isolation (Unix socket proxy with domain allowlists), VM isolation on macOS, permission model reduces prompts by 84% |

### Anthropic -- GTG-1002 Incident (First AI-Orchestrated Espionage)

| Field | Value |
|-------|-------|
| Disclosure | [anthropic.com/news/disrupting-AI-espionage](https://www.anthropic.com/news/disrupting-AI-espionage) |
| Analysis | [securiti.ai/blog/anthropic-exploit-era-of-ai-agent-attacks/](https://securiti.ai/blog/anthropic-exploit-era-of-ai-agent-attacks/) |
| Authority | Industry Leader (direct incident disclosure) |
| Impact | Chinese state-sponsored GTG-1002 weaponized Claude Code; 80% autonomous; 30+ orgs compromised |
| Key Lessons | MCP tool supply chain is the attack surface; high-impact actions need HITL; external content must be gated |

### Anthropic -- Content Source Management Guidance

| Field | Value |
|-------|-------|
| URL | [MIT Technology Review / Anthropic](https://www.technologyreview.com/2026/02/04/1131014/from-guardrails-to-governance-a-ceos-guide-for-securing-agentic-systems) |
| Authority | Industry Leader |
| Key Principles | Treat agents as non-human principals; constrain to user's role/geography; validator between agent and real world |

### Google DeepMind -- 5-Layer Defense Architecture

| Field | Value |
|-------|-------|
| URL | [deepmind.google/blog/advancing-geminis-security-safeguards/](https://deepmind.google/blog/advancing-geminis-security-safeguards/) |
| Paper | [arXiv:2505.14534 -- Defending Gemini Against Indirect Prompt Injections](https://arxiv.org/html/2505.14534v1) |
| Authority | Industry Leader |
| Architecture | 5 layers: Prevention → Detection → Verification → Control → Evolution (ART) |
| Key Finding | "Relying on defenses tested only against static attacks offers a false sense of security" |

### Google DeepMind -- Intelligent AI Delegation Framework

| Field | Value |
|-------|-------|
| Paper | [arXiv:2602.11865 -- Intelligent AI Delegation](https://arxiv.org/abs/2602.11865) |
| Authority | Industry Leader / Academic Research |
| Key Concept | Delegation Capability Tokens using cryptographic caveats (Macaroons/Biscuits) for minimum privilege across agent chains |

### Microsoft -- Agent Factory (6-Part Series)

| Field | Value |
|-------|-------|
| URL | [azure.microsoft.com/blog/agent-factory-creating-a-blueprint-for-safe-and-secure-ai-agents/](https://azure.microsoft.com/en-us/blog/agent-factory-creating-a-blueprint-for-safe-and-secure-ai-agents/) |
| Authority | Industry Leader |
| 5 Qualities | Unique identity (Entra Agent ID), data protection (Purview), built-in controls, threat evaluation (PyRIT), continuous oversight (Defender XDR) |

### Microsoft -- Cloud Adoption Framework for AI Agents

| Field | Value |
|-------|-------|
| URL | [learn.microsoft.com/azure/cloud-adoption-framework/ai-agents/governance-security-across-organization](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ai-agents/governance-security-across-organization) |
| Authority | Industry Leader |
| Layers | Data governance, agent observability, agent security (threat protection, HITL, incident response), agent development |

### Microsoft -- SDL for AI

| Field | Value |
|-------|-------|
| URL | [microsoft.com/security/blog/2026/02/03/microsoft-sdl-evolving-security-practices-for-an-ai-powered-world/](https://www.microsoft.com/en-us/security/blog/2026/02/03/microsoft-sdl-evolving-security-practices-for-an-ai-powered-world/) |
| Authority | Industry Leader |
| Coverage | AI threat modeling, observability, memory protections, identity/RBAC enforcement, shutdown mechanisms |

### Cisco -- State of AI Security 2026

| Field | Value |
|-------|-------|
| URL | [blogs.cisco.com/ai/cisco-state-of-ai-security-2026-report](https://blogs.cisco.com/ai/cisco-state-of-ai-security-2026-report) |
| Authority | Industry Expert |
| Key Findings | 83% planned agentic deployment, only 29% felt ready; MCP creates "vast unmonitored attack surface"; malicious MCP package BCC'd all emails |
| Open Source | Cisco released security scanners for MCP, A2A, and agentic skill files |

### Cisco -- Integrated AI Security and Safety Framework

| Field | Value |
|-------|-------|
| Paper | [arXiv:2512.12921](https://arxiv.org/abs/2512.12921) |
| Authority | Industry Expert / Academic Research |
| Scope | Lifecycle-aware taxonomy: content safety, model/data integrity, runtime manipulation (prompt injection, tool/agent misuse), ecosystem risks (orchestration abuse, multi-agent collusion) |

### Meta -- Agents Rule of Two

| Field | Value |
|-------|-------|
| URL | [ai.meta.com/blog/practical-ai-agent-security/](https://ai.meta.com/blog/practical-ai-agent-security/) |
| Authority | Industry Leader |
| Principle | An agent may satisfy no more than 2 of: (A) processing untrusted inputs, (B) accessing sensitive data, (C) changing state externally. Having all 3 without HITL = full exploit chain |

### "The Attacker Moves Second" -- Multi-Organization Study

| Field | Value |
|-------|-------|
| Coverage | [simonwillison.net/2025/Nov/2/new-prompt-injection-papers/](https://simonwillison.net/2025/Nov/2/new-prompt-injection-papers/) |
| Authors | 14 authors from OpenAI, Anthropic, Google DeepMind (joint) |
| Key Finding | 12 published defenses bypassed with >90% success rate using adaptive attacks; defense-in-depth is the only viable strategy |

### OWASP GenAI Security Project

| Field | Value |
|-------|-------|
| URL | [genai.owasp.org](https://genai.owasp.org/) |
| Authority | Community Expert (Industry Standard) |
| Key Output | LLM Top 10, Agentic Top 10, AI Agent Security Cheat Sheet, Prompt Injection Prevention Cheat Sheet |

---

## Python Libraries

| Library | Package | Install | Purpose |
|---------|---------|---------|---------|
| mitreattack-python | `mitreattack-python` | `uv add mitreattack-python` | Query ATT&CK STIX data, export to DataFrames |
| stix2 | `stix2` | `uv add stix2` | Parse/create STIX 2.0/2.1 objects |
| cti-python-stix2 | `stix2` | (same as above) | CTI STIX library |

---

## Key Research Findings

### Finding 1: Model Guardrails Are Not Security Controls (Anthropic Incident)

The November 2025 Anthropic incident proved that behavioral guardrails (training-based) are "architectural suggestions, not enforcement mechanisms." **This validates Jerry's 5-layer enforcement architecture** where L2 (per-prompt re-injection), L3 (deterministic pre-tool gating), and L5 (CI verification) provide context-rot-immune security that doesn't depend on model behavior.

**Source:** [Securiti AI](https://securiti.ai/blog/anthropic-exploit-era-of-ai-agent-attacks/)
**Authority:** Industry Expert

### Finding 2: MITRE ATLAS Added 14 Agent-Specific Techniques (2025)

MITRE ATLAS collaborated with Zenity Labs to add 14 new techniques specifically for AI Agents and GenAI systems in October 2025. These cover prompt injection, memory manipulation, and agent-specific attack vectors that didn't exist in prior versions.

**Source:** [Practical DevSecOps](https://www.practical-devsecops.com/mitre-atlas-framework-guide-securing-ai-systems/)
**Authority:** Industry Expert / Standards Body

### Finding 3: Microsoft Agent 365 -- Control Plane Architecture

Microsoft's Agent 365 establishes that enterprise-grade agent security requires: (a) unique agent identity, (b) control plane/data plane separation, (c) registry-based governance, (d) adaptive risk-based access policies, (e) real-time behavioral monitoring. Jerry's constitutional architecture maps directly to these principles.

**Source:** [Microsoft Security Blog](https://www.microsoft.com/en-us/security/blog/2025/11/18/ambient-and-autonomous-security-for-the-agentic-era/)
**Authority:** Industry Leader

### Finding 4: NIST SP 800-53 Available in Machine-Readable OSCAL Format

NIST provides SP 800-53 Rev 5 controls in YAML, JSON, and XML via the OSCAL content repository. This enables programmatic compliance mapping rather than manual document review.

**Source:** [usnistgov/oscal-content](https://github.com/usnistgov/oscal-content)
**Authority:** Standards Body (US Government)

### Finding 5: OWASP Provides Agent-Specific Security Cheat Sheet

OWASP has a dedicated AI Agent Security Cheat Sheet with concrete implementation patterns (SecureAgentMemory, SecureLLMPipeline, PromptInjectionFilter) that can be adapted for Jerry's agent model.

**Source:** [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet)
**Authority:** Community Expert (Industry Standard)

### Finding 6: OWASP Agentic Top 10 (2026) -- First Agent-Specific Threat Standard

Released December 2025, this is the first industry-standard threat classification specifically for agentic AI systems. The 10 categories (ASI01-ASI10) directly map to Jerry's attack surface: agent goal hijack, tool misuse, privilege escalation, delegated trust boundary violations, memory/context manipulation, identity/access mismanagement, insecure inter-agent communication, cascading failures, insufficient logging, and rogue agents. This is **the most directly applicable framework** for PROJ-008.

**Source:** [OWASP GenAI](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)
**Authority:** Industry Standard

### Finding 7: Meta's Rule of Two -- Design Constraint for Agent Safety

Meta's security team proposes that an agent may satisfy **no more than 2 of**: (A) processing untrusted inputs, (B) accessing sensitive data, (C) making external state changes. Having all three without HITL creates a full exploit chain. This maps directly to Jerry's tool tier system (T1-T5) and helps validate the principle of least privilege enforcement.

**Source:** [Meta AI](https://ai.meta.com/blog/practical-ai-agent-security/)
**Authority:** Industry Leader

### Finding 8: Google DeepMind's 5-Layer Defense -- Defense-in-Depth Validated

Google's Gemini defense architecture uses 5 layers: Prevention, Detection, Verification, Control, Evolution. Key insight: "relying on defenses tested only against static attacks offers a false sense of security." This converges with Jerry's 5-layer enforcement architecture (L1-L5) and validates the defense-in-depth approach.

**Source:** [Google DeepMind](https://deepmind.google/blog/advancing-geminis-security-safeguards/)
**Authority:** Industry Leader

### Finding 9: D3FEND -- Defensive Complement to ATT&CK

MITRE D3FEND provides 267 defensive techniques mapped to ATT&CK attack techniques. Combined with the Mappings Explorer (ATT&CK to NIST 800-53/CIS/CSF mappings), this enables **automated cross-framework coverage analysis**: for every ATT&CK technique we defend against, we can trace to both a defensive technique (D3FEND) and a compliance control (NIST).

**Source:** [D3FEND](https://d3fend.mitre.org/), [Mappings Explorer](https://github.com/center-for-threat-informed-defense/mappings-explorer)
**Authority:** Standards Body

### Finding 10: Industry Consensus on 12 Core Agentic Security Principles

Cross-industry analysis reveals convergence on these principles: (1) defense-in-depth, (2) least privilege, (3) unique agent identity, (4) HITL for high-impact actions, (5) deterministic enforcement over behavioral guardrails, (6) supply chain verification, (7) control plane/data plane separation, (8) structured audit trails, (9) input validation at trust boundaries, (10) output sanitization, (11) cryptographic delegation tokens, (12) graceful degradation. Jerry already implements many of these through its constitutional architecture.

**Source:** Synthesized from Anthropic, Microsoft, Google DeepMind, Cisco, Meta, OWASP guidance
**Authority:** Cross-Industry Consensus

---

## Citations

| # | Source | Authority | URL |
|---|--------|-----------|-----|
| 1 | MITRE ATT&CK STIX Data | Standards Body | https://github.com/mitre-attack/attack-stix-data |
| 2 | MITRE ATT&CK Python Library | Standards Body | https://github.com/mitre-attack/mitreattack-python |
| 3 | MITRE CTI | Standards Body | https://github.com/mitre/cti |
| 4 | MITRE ATLAS Data | Standards Body | https://github.com/mitre-atlas/atlas-data |
| 5 | MITRE ATLAS (advmlthreatmatrix) | Standards Body | https://github.com/mitre/advmlthreatmatrix |
| 6 | OASIS CTI Python STIX2 | Standards Body | https://github.com/oasis-open/cti-python-stix2 |
| 7 | NIST OSCAL | US Government | https://github.com/usnistgov/OSCAL |
| 8 | NIST OSCAL Content (SP 800-53) | US Government | https://github.com/usnistgov/oscal-content |
| 9 | OWASP Top 10 LLM 2025 | Industry Standard | https://genai.owasp.org/llm-top-10/ |
| 10 | OWASP AI Agent Security Cheat Sheet | Industry Standard | https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet |
| 11 | OWASP Prompt Injection Prevention | Industry Standard | https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet |
| 12 | Anthropic Claude Agent SDK | Industry Leader | https://platform.claude.com/docs/en/agent-sdk/overview |
| 13 | Anthropic Safeguards Blog | Industry Leader | https://www.anthropic.com/news/building-safeguards-for-claude |
| 14 | Securiti AI (Anthropic Exploit Analysis) | Industry Expert | https://securiti.ai/blog/anthropic-exploit-era-of-ai-agent-attacks/ |
| 15 | Microsoft Agent 365 Blog | Industry Leader | https://www.microsoft.com/en-us/microsoft-365/blog/2025/11/18/microsoft-agent-365-the-control-plane-for-ai-agents/ |
| 16 | Microsoft Agentic Era Security | Industry Leader | https://www.microsoft.com/en-us/security/blog/2025/11/18/ambient-and-autonomous-security-for-the-agentic-era/ |
| 17 | Microsoft Security Core Primitive | Industry Leader | https://techcommunity.microsoft.com/blog/microsoft-security-blog/security-as-the-core-primitive---securing-ai-agents-and-apps/4470197 |
| 18 | Microsoft Fortune 500 AI Agents Report | Industry Leader | https://www.microsoft.com/en-us/security/blog/2026/02/10/80-of-fortune-500-use-active-ai-agents |
| 19 | Microsoft Agent 365 Security Docs | Industry Leader | https://learn.microsoft.com/en-us/security/security-for-ai/agent-365-security |
| 20 | Codacy Claude Code Guardrails | Community Expert | https://blog.codacy.com/equipping-claude-code-with-deterministic-security-guardrails |
| 21 | Practical DevSecOps ATLAS Guide | Industry Expert | https://www.practical-devsecops.com/mitre-atlas-framework-guide-securing-ai-systems/ |
| 22 | Vectra AI ATLAS Overview | Industry Expert | https://www.vectra.ai/topics/mitre-atlas |
| 23 | NIST ATLAS Presentation | Standards Body | https://csrc.nist.gov/csrc/media/Presentations/2025/mitre-atlas/TuePM2.1-MITRE%20ATLAS%20Overview%20Sept%202025.pdf |
| 24 | Invicti OWASP LLM Guide | Community Expert | https://www.invicti.com/blog/web-security/owasp-top-10-risks-llm-security-2025/ |
| 25 | Context7 (mitreattack-python) | Tool | /mitre-attack/mitreattack-python |
| 26 | Context7 (attack-stix-data) | Tool | /mitre-attack/attack-stix-data |
| 27 | Context7 (OWASP Cheat Sheets) | Tool | /websites/cheatsheetseries_owasp |
| 28 | MITRE ATLAS Navigator Data | Standards Body | https://github.com/mitre-atlas/atlas-navigator-data |
| 29 | MITRE ATT&CK Navigator | Standards Body | https://github.com/mitre-attack/attack-navigator |
| 30 | MITRE D3FEND Ontology | Standards Body | https://github.com/d3fend/d3fend-ontology |
| 31 | D3FEND ATT&CK Mappings | Standards Body | https://d3fend.mitre.org/mappings/attack-mitigations/ |
| 32 | Center for Threat-Informed Defense Mappings Explorer | Industry Expert | https://github.com/center-for-threat-informed-defense/mappings-explorer |
| 33 | MITRE CALDERA (Adversary Emulation) | Standards Body | https://github.com/mitre/caldera |
| 34 | NIST AI 600-1 GenAI Profile | US Government | https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf |
| 35 | NIST IR 8596 CSF Profile for AI (Draft) | US Government | https://csrc.nist.gov/pubs/ir/8596/iprd |
| 36 | Federal Register -- AI Agents Security RFI | US Government | https://www.federalregister.gov/documents/2026/01/08/2026-00206/request-for-information-regarding-security-considerations-for-artificial-intelligence-agents |
| 37 | NIST CSF 2.0 MCP Server (Community) | Community Expert | https://github.com/rocklambros/nist-csf-2-mcp-server |
| 38 | NVD API | US Government | https://nvd.nist.gov/developers/vulnerabilities |
| 39 | nvdlib (NVD Python Library) | Community Expert | https://github.com/vehemont/nvdlib |
| 40 | MCP NVD Server | Community Expert | https://github.com/marcoeg/mcp-nvd |
| 41 | OWASP Top 10 for Agentic Applications 2026 | Industry Standard | https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/ |
| 42 | OWASP Agentic AI Threats & Mitigations | Industry Standard | https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/ |
| 43 | Agentic-AI-Top10-Vulnerability (Community) | Community Expert | https://github.com/precize/Agentic-AI-Top10-Vulnerability |
| 44 | OWASP Agentic Security Dataset | Community Expert | https://github.com/evolutionstorm/owasp-agentic-security-dataset |
| 45 | agent-audit (MCP Static Analyzer) | Community Expert | https://github.com/HeadyZhang/agent-audit |
| 46 | OWASP LLM Top 10 Mapping (Cross-Framework) | Community Expert | https://github.com/emmanuelgjr/owaspllmtop10mapping |
| 47 | JonathanBowker NIST AI RMF Data (XLSX) | Community Expert | https://github.com/JonathanBowker/NIST-AI-Risk-Management-Framework |
| 48 | Anthropic Claude Code Sandboxing | Industry Leader | https://www.anthropic.com/engineering/claude-code-sandboxing |
| 49 | Anthropic GTG-1002 Incident Disclosure | Industry Leader | https://www.anthropic.com/news/disrupting-AI-espionage |
| 50 | MIT Tech Review -- Anthropic Content Source Mgmt | Industry Leader | https://www.technologyreview.com/2026/02/04/1131014/from-guardrails-to-governance-a-ceos-guide-for-securing-agentic-systems |
| 51 | Google DeepMind -- Gemini Security Safeguards | Industry Leader | https://deepmind.google/blog/advancing-geminis-security-safeguards/ |
| 52 | Google DeepMind -- Defending Gemini Against IPI | Industry Leader / Academic | https://arxiv.org/html/2505.14534v1 |
| 53 | Google DeepMind -- Intelligent AI Delegation | Industry Leader / Academic | https://arxiv.org/abs/2602.11865 |
| 54 | Microsoft Agent Factory (6-Part Series) | Industry Leader | https://azure.microsoft.com/en-us/blog/agent-factory-creating-a-blueprint-for-safe-and-secure-ai-agents/ |
| 55 | Microsoft Cloud Adoption Framework for AI Agents | Industry Leader | https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ai-agents/governance-security-across-organization |
| 56 | Microsoft SDL for AI | Industry Leader | https://www.microsoft.com/en-us/security/blog/2026/02/03/microsoft-sdl-evolving-security-practices-for-an-ai-powered-world/ |
| 57 | Cisco State of AI Security 2026 | Industry Expert | https://blogs.cisco.com/ai/cisco-state-of-ai-security-2026-report |
| 58 | Cisco Integrated AI Security Framework | Industry Expert / Academic | https://arxiv.org/abs/2512.12921 |
| 59 | Meta -- Practical AI Agent Security (Rule of Two) | Industry Leader | https://ai.meta.com/blog/practical-ai-agent-security/ |
| 60 | The Attacker Moves Second (Multi-Org Study) | Industry Leader / Academic | https://simonwillison.net/2025/Nov/2/new-prompt-injection-papers/ |
| 61 | OWASP GenAI Security Project | Industry Standard | https://genai.owasp.org/ |
| 62 | Oligo Security -- OWASP LLM Top 10 Guide | Community Expert | https://www.oligo.security/academy/owasp-top-10-llm-updated-2025-examples-and-mitigation-strategies |
| 63 | The New Stack -- Anthropic Agent SDK Analysis | Community Expert | https://thenewstack.io/anthropic-agent-sdk-confusion/ |
| 64 | NIST AI Resource Center | US Government | https://airc.nist.gov |
