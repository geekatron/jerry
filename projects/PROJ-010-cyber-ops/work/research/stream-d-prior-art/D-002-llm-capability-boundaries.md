# D-002: LLM Capability Boundaries for Security Tasks

> Stream D: Prior Art & Industry | PROJ-010 Cyber Ops | Phase 1 Research

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | High-level capability assessment |
| [L1: Key Findings](#l1-key-findings) | Structured findings on capabilities and limits |
| [L2: Detailed Analysis](#l2-detailed-analysis) | Deep analysis by capability domain |
| [Capability Matrix](#capability-matrix) | What works, what struggles, what fails |
| [Academic Benchmarks](#academic-benchmarks) | CyberSecEval, HarmBench, AI Cyber Model Arena |
| [Known Failure Modes](#known-failure-modes) | Documented LLM security failures |
| [Ethical Boundaries](#ethical-boundaries) | Safety alignment impact on security capabilities |
| [Capability vs Augmentation Boundary](#capability-vs-augmentation-boundary) | Where LLM operates vs where it needs tools |
| [Evidence and Citations](#evidence-and-citations) | All sources dated and categorized |
| [Implications for PROJ-010](#implications-for-proj-010) | Design implications from capability analysis |

---

## L0: Executive Summary

LLMs demonstrate strong and improving capabilities in several cybersecurity domains -- code vulnerability pattern detection, threat intelligence synthesis, security report generation, and methodology guidance -- but face fundamental limitations in novel exploit generation, binary exploitation, real-time network interaction, and runtime analysis. Academic benchmarks (CyberSecEval 3, HarmBench, Wiz AI Cyber Model Arena) provide increasingly rigorous measurements. The most critical failure mode for PROJ-010 is hallucination: LLMs fabricate CVEs, generate plausible-but-incorrect vulnerability reports, and produce exploit code with subtle errors. The evidence strongly supports PROJ-010's design as a methodology-guidance framework rather than an autonomous execution engine -- LLMs excel at structured reasoning, knowledge synthesis, and procedural guidance while requiring human verification and tool integration for execution-level security tasks.

---

## L1: Key Findings

### Finding 1: LLMs Excel at Pattern-Based Vulnerability Detection When Augmented

LLMs integrated with static analysis tools show substantial improvements: IRIS with GPT-4 detected 55 vulnerabilities versus 27 by CodeQL alone (2x improvement). Chain-of-Thought prompting improves precision and recall in vulnerability detection. Fine-tuned models achieve up to 99% accuracy in narrow domains (e.g., Solidity smart contract vulnerabilities). However, without tool augmentation, 12-65% of LLM-generated code snippets trigger CWE-classified vulnerabilities, depending on task, language, model, and prompting configuration.

### Finding 2: Exploit Generation Remains Unreliable

CyberSecEval 3 found that even top-performing models (Llama 3 405B) lack breakthrough exploitation capabilities, though they outperform models without coding capabilities. Research from May 2025 found that no LLM successfully generated exploits for custom labs with refactored code. CVE-Genie, a multi-agent framework, successfully reproduces approximately 51% of 2024-2025 CVEs -- impressive but far from reliable. Most commercial LLMs refuse exploit generation requests, requiring multi-round interactions or jailbreaking.

### Finding 3: AI Agents Match Humans in Directed Web Hacking Tasks

Wiz's research showed AI models successfully solved 9/10 directed web hacking challenges. Hack the Box's 2026 competition saw AI agent teams achieve 95% solve rate (19/20 challenges). Stanford's ARTEMIS placed second overall in a bug bounty competition with an 82% valid submission rate at $18/hour (vs $60/hour for human pentesters). However, performance degrades significantly when moving from directed to broad-scope scenarios -- cost increases 2-2.5x while effectiveness decreases.

### Finding 4: Hallucination Is the Dominant Failure Mode

LLMs generate vulnerability reports regardless of whether vulnerabilities exist. The NVD backlog crisis was worsened by AI-generated false CVE submissions -- only ~20% of recent CVEs may be valid. Over 40% of AI-generated code solutions contain security flaws. Open-source maintainers report receiving ~2 AI-generated false security reports per week, consuming all available contribution time. This is the most significant practical limitation for any LLM-based security tool.

### Finding 5: Safety Alignment Creates a Security Capability Paradox

There is an inherent tension between LLM safety alignment and offensive security utility. CyberSecEval reports that average LLM compliance rate with cyber attack assistance requests decreased from 52% to 28% (improved safety), but this also reduces legitimate red-team utility. Claude Sonnet 3.5 achieved the highest safety robustness (4.39% ASR across all attack methods) precisely because it refused more often -- but this means it also refuses legitimate security research queries. Local/uncensored models comply with up to 95% of requests but lack safety guardrails entirely.

### Finding 6: Multi-Agent Architectures Show Promise

Multi-agent approaches outperform single-agent systems. XBOW's coordinator/solver architecture, multi-LLM collaboration for buffer overflow exploitation, and PentAGI's specialized agent roles all demonstrate that decomposing security tasks across specialized agents produces better results. The Wiz AI Cyber Model Arena confirmed that performance is jointly determined by model AND agent scaffold -- the same model performs dramatically differently depending on orchestration.

---

## L2: Detailed Analysis

### What LLMs Can Reliably Do

#### Code Vulnerability Pattern Detection

LLMs are effective at identifying known vulnerability patterns in source code, particularly when augmented with static analysis tools. The combination of LLM reasoning with tool-based evidence produces results that exceed either approach alone.

**Evidence:**
- IRIS + GPT-4: 55 vulnerabilities detected vs 27 by CodeQL alone (ACM Computing Surveys, 2025)
- External feedback from static analyzers like Bandit improves vulnerability refinement by up to 30% with GPT-4
- Fine-tuned GPT-4 achieved 99% accuracy in Solidity vulnerability detection (domain-specific)
- Snyk DeepCode AI's hybrid Symbolic + Generative approach achieves near-zero false positives for known patterns

**Caveats:**
- Performance is highly language- and framework-dependent
- Novel vulnerability classes not in training data are missed
- Business logic vulnerabilities remain largely undetectable
- False positive rates vary significantly by configuration (12-65% of generated code is non-compliant)

#### Threat Intelligence Synthesis

LLMs excel at synthesizing threat intelligence from multiple sources, summarizing threat actor profiles, and contextualizing indicators of compromise within organizational contexts.

**Evidence:**
- Google Sec-Gemini v1 achieves approximately 7x reduction in analyst time for threat intelligence queries
- Mandiant Threat Intelligence AI leverages Sec-PaLM to summarize and act on threat data relevant to specific organizations
- CrowdStrike Charlotte AI fuses analyst expertise with autonomous reasoning for investigation acceleration

#### Security Report Generation

LLMs are strong at generating structured security reports, vulnerability descriptions, remediation guidance, and executive summaries from technical findings.

**Evidence:**
- HackerOne's "bionic hackers" use AI for report writing, proof-of-concept generation, and refining exploit code
- Snyk DeepCode AI explains vulnerabilities in plain language
- Microsoft Security Copilot generates investigation summaries and playbooks

#### Methodology Guidance and Knowledge Retrieval

LLMs are highly effective at guiding practitioners through established security methodologies (OWASP Testing Guide, PTES, NIST frameworks) and retrieving relevant knowledge for specific scenarios.

**Evidence:**
- This is the least-studied but most practically valuable capability for PROJ-010's use case
- Security training platforms (SANS SEC598) increasingly incorporate AI-guided methodology application
- HackerGPT's primary value is answering complex cybersecurity questions with detailed, prompt responses

#### Configuration Analysis

LLMs can analyze security configurations (cloud IAM policies, firewall rules, application settings) against best practices and identify misconfigurations.

**Evidence:**
- Wiz AI connects context across infrastructure, identity, data, and AI for risk assessment
- Google SecOps generates detection rules from natural language descriptions
- GitHub Copilot's secret scanning achieves 94% false positive reduction through contextual analysis

### What LLMs Struggle With

#### Novel Exploit Development

LLMs cannot reliably generate working exploits for previously unknown vulnerabilities. They can sometimes produce exploits for well-documented vulnerability classes, but novel attack chains require human creativity and deep system understanding.

**Evidence:**
- CyberSecEval 3: "Further work is needed for LLMs to become proficient at exploit generation"
- May 2025 research: No LLM successfully generated exploits for custom labs with refactored code
- GPT-4o (strongest performer) typically made one or two errors per attempt on exploit generation
- CVE-Genie reproduces only 51% of known CVEs -- and these are KNOWN vulnerabilities with existing descriptions

#### Runtime Analysis and Dynamic Testing

LLMs cannot interact with running systems in real-time, observe program behavior, or perform dynamic analysis. They can reason about code statically but cannot replace debuggers, dynamic analysis tools, or runtime monitoring.

**Evidence:**
- CyberSecEval 3: "Real-world vulnerability identification typically involves multi-step reasoning processes that require feedback from dynamic and static analysis tools"
- No single static analyzer (including LLM-based ones) reliably detects all vulnerability classes
- Dynamic analysis, fuzzing, and runtime monitoring remain essential complements

#### Binary Exploitation

Binary-level vulnerability exploitation (buffer overflows, heap exploitation, ROP chains) remains largely beyond LLM capabilities without significant human guidance and tool support.

**Evidence:**
- PwnGPT benchmark (July 2025) using Binary Exploitation CTF challenges shows models need significant scaffolding
- Multi-LLM collaboration can exploit buffer overflows but "assumes access to necessary data for vulnerability identification, which is not always feasible in real-world scenarios"
- Binary analysis requires understanding of specific architectures, memory layouts, and protection mechanisms that LLMs reason about poorly

#### Multi-Step Attack Chains

Real-world attacks involve chaining multiple vulnerabilities and techniques across different systems. LLMs struggle with the sequential reasoning, state tracking, and adaptive decision-making this requires.

**Evidence:**
- Wiz research: Moving from directed to broad-scope scenarios decreases AI agent effectiveness and increases cost by 2-2.5x
- AI excels at directed tasks but "moving to a more realistic, less directed approach makes the agents less effective"
- Zero-days, creative chains of exploitation, and deep logic flaws "remain overwhelmingly human discoveries"

#### Real-Time Network Interaction

LLMs cannot directly interact with network protocols, perform real-time packet analysis, or adapt to dynamic network conditions.

**Evidence:**
- All agentic security tools require tool integration (Nmap, Metasploit, etc.) for network interaction
- The LLM provides reasoning and decision-making; tools provide execution
- This is a fundamental architectural constraint, not a solvable limitation

### What LLMs Cannot Do (Fundamental Limitations)

- **True zero-day discovery in the wild:** While Google's Big Sleep found 20 vulnerabilities in open-source software and even predicted exploitation of CVE-2025-6965, this required extensive threat intelligence integration and specialized infrastructure beyond LLM capability alone
- **Adaptive adversary simulation:** Real adversaries adapt in real-time to defensive responses; LLMs cannot maintain persistent state across an engagement without external state management
- **Physical security assessment:** Social engineering execution, physical access testing, and hardware-level attacks are inherently beyond LLM scope
- **Legal and compliance judgment:** LLMs cannot make binding legal determinations about what constitutes authorized testing

---

## Capability Matrix

| Security Task | LLM Capability Level | Tool Augmentation Needed | Reliability | PROJ-010 Relevance |
|---------------|---------------------|--------------------------|-------------|-------------------|
| **Code vulnerability pattern detection** | HIGH | Static analysis tools (CodeQL, Bandit, Semgrep) | High with augmentation, medium without | /eng-team: code review guidance |
| **Threat intelligence synthesis** | HIGH | Threat feeds, CTI platforms | High | /red-team: threat context for engagements |
| **Security report generation** | HIGH | Template systems | High | Both skills: report structure |
| **Methodology guidance** | HIGH | Knowledge bases, framework docs | High | Core capability for both skills |
| **Configuration analysis** | HIGH | Cloud APIs, config parsers | Medium-High | /eng-team: infrastructure security review |
| **Vulnerability prioritization** | MEDIUM-HIGH | CVSS data, exploit DB, context | Medium-High | Both skills: risk assessment |
| **Threat modeling** | MEDIUM-HIGH | Architecture diagrams, data flow | Medium | /eng-team: STRIDE/DREAD guidance |
| **Known exploit reproduction** | MEDIUM | Exploitation frameworks (Metasploit) | ~51% success rate | /red-team: methodology guidance only |
| **Phishing content generation** | MEDIUM-HIGH | Email infrastructure | High for content, medium for targeting | /red-team: social engineering planning |
| **Attack path analysis** | MEDIUM | Graph databases (BloodHound) | Medium with tools | /red-team: engagement planning |
| **Novel exploit development** | LOW | Extensive tooling and human guidance | Low (~0% for refactored code) | Out of scope for PROJ-010 |
| **Binary exploitation** | LOW | Debuggers, disassemblers, custom tools | Low without extensive scaffolding | Out of scope for PROJ-010 |
| **Real-time network interaction** | NONE (requires tools) | Nmap, Wireshark, custom scripts | N/A (tool capability) | /red-team: tool orchestration guidance |
| **Runtime dynamic analysis** | NONE (requires tools) | Debuggers, fuzzers, DAST tools | N/A (tool capability) | /eng-team: testing methodology guidance |
| **Adaptive adversary simulation** | LOW | State management, C2 frameworks | Low | /red-team: exercise planning only |

---

## Academic Benchmarks

### CyberSecEval (Meta, Versions 1-3)

**Purpose:** Suite of security benchmarks measuring LLM cybersecurity risks and capabilities.

**Key Findings (CyberSecEval 3, August 2024 -- latest published):**
- All tested models showed 26-41% successful prompt injection rates
- Models with coding capabilities outperform those without for exploit generation
- Llama 3 405B outperforms comparison models but lacks "breakthrough exploitation capabilities"
- Multi-step reasoning for real-world vulnerability identification remains beyond LLM capabilities
- Safety-utility tradeoff: Conditioning for safety causes false rejection of benign prompts
- Average LLM compliance with cyber attack requests decreased from 52% to 28% (improved safety)

**Relevance to PROJ-010:** Confirms that LLMs should guide methodology rather than execute exploitation. The safety-utility tradeoff directly impacts /red-team skill design -- need to structure prompts as legitimate security methodology guidance rather than direct attack requests.

### HarmBench (UC Berkeley, Google DeepMind, Center for AI Safety)

**Purpose:** Standardized evaluation framework for automated red teaming and robust refusal.

**Key Findings:**
- 400+ adversarial attacks evaluated across 6 risk categories (chemical/biological safety, misinformation, cybercrime, illegal activities, copyright)
- Claude 3.5 Sonnet v2 achieved highest safety robustness: only 4.39% ASR across all attack methods
- Supports quantitative evaluation of diverse red-team strategies including token-level optimization and LLM-in-the-loop prompting
- Has become the standard for cross-method safety evaluation in academic research and industry

**Relevance to PROJ-010:** HarmBench results inform which models are most resistant to misuse (important for /red-team skill's ethical boundary enforcement) and which attack categories trigger refusals (important for designing prompts that legitimate security work can proceed without false refusals).

### Wiz AI Cyber Model Arena (Wiz, February 2026)

**Purpose:** Real-world benchmark testing AI agents across 257 offensive security challenges in 5 domains.

**Key Findings:**
- Tested 25 agent-model combinations (4 agents x 8 models)
- Claude Code on Claude Opus 4.6 ranked #1 overall
- Performance jointly determined by model AND agent scaffold -- same model swings dramatically by agent
- Performance is highly domain-specific -- no model/agent dominates all categories
- Zero-day discovery, CVE detection, API security, web security, and cloud security tested independently

**Relevance to PROJ-010:** Confirms that agent architecture (scaffold/orchestration) matters as much as model capability. Directly supports Jerry's multi-skill architecture approach. Also confirms domain specificity -- /eng-team and /red-team should specialize rather than trying to be universal.

### Hack the Box AI vs Human Competition (2026)

**Purpose:** Head-to-head competition between AI agent teams and 403 human teams across 20 challenges.

**Key Findings:**
- 5 of 8 AI-agent teams achieved 95% solve rate (19/20 challenges)
- AI agents made thousands of requests per second -- impossible for humans to match
- AI still struggled with novel attack chains and creative exploitation

**Relevance to PROJ-010:** Demonstrates that well-orchestrated AI agents can rival experts in structured challenges, supporting the viability of AI-guided security methodology. But also confirms that human creativity remains essential for novel scenarios.

### Stanford ARTEMIS Study (2025)

**Purpose:** AI agent for autonomous bug bounty competition.

**Key Findings:**
- Placed second overall, discovering 9 valid vulnerabilities with 82% valid submission rate
- Outperformed 9 of 10 human participants
- Cost: $18/hour vs $60/hour for professional penetration testers
- Demonstrates significant cost efficiency for directed vulnerability discovery

**Relevance to PROJ-010:** Shows that AI-guided security work is economically viable and can outperform many human practitioners for structured tasks. Supports the business case for PROJ-010's skills.

---

## Known Failure Modes

### Hallucinated CVEs and Vulnerability Reports

**Problem:** LLMs generate vulnerability reports regardless of whether vulnerabilities actually exist. They produce answers that sound correct but are completely unfounded.

**Scale of Impact:**
- NVD analyzed fewer than 300 CVEs by March 2025, with 30,000+ backlogged -- crisis worsened by AI-generated false submissions
- Former insiders estimate only ~20% of recent CVEs are valid (rest are duplicates, invalid, or inflated)
- Open-source maintainers receive ~2 AI-generated false security reports per week

**PROJ-010 Mitigation:** Design skills to provide methodology guidance and structured analysis frameworks rather than generating vulnerability findings directly. Require human verification at all decision points. Include explicit warnings about hallucination risk in /red-team outputs.

### Incorrect Exploit Code

**Problem:** LLM-generated exploit code frequently contains subtle errors that prevent successful exploitation or, worse, create unintended consequences.

**Evidence:**
- Over 40% of AI-generated code solutions contain security flaws
- GPT-4o typically makes 1-2 errors per exploit generation attempt
- 50% of LLM-generated code contains exploitable threats

**PROJ-010 Mitigation:** /red-team should never generate exploit code directly. Instead, guide practitioners to use established exploitation frameworks (Metasploit, custom tooling) with methodology-driven approach.

### False Positive Vulnerabilities

**Problem:** LLMs over-report vulnerabilities, identifying benign code patterns as security issues.

**Evidence:**
- XBOW requires deterministic validation to filter AI hallucinations
- Without augmentation, LLM vulnerability detection has high false positive rates
- AI agents "tend to produce false positives, exaggerate severity of findings"

**PROJ-010 Mitigation:** /eng-team should include triage guidance that helps engineering teams distinguish real vulnerabilities from false positives. Integrate with tool-based validation workflows.

### Safety Refusal of Legitimate Security Work

**Problem:** Safety-aligned LLMs refuse legitimate security research and penetration testing queries, treating them as malicious.

**Evidence:**
- Claude Sonnet 4.5 and Grok 4 refuse prompts with obfuscated text (returning "Safety Fail")
- Claude 3.5 Sonnet v2 has highest safety robustness (4.39% ASR) -- also highest refusal rate for security queries
- CyberSecEval: Safety-utility tradeoff causes false rejection of benign prompts

**PROJ-010 Mitigation:** Frame all security guidance within established professional methodology (PTES, OWASP, NIST). Use professional security terminology and context. Avoid patterns that trigger safety filters while maintaining ethical boundaries.

### Context Window Limitations

**Problem:** Complex security assessments require analyzing large codebases, network architectures, and multi-system interactions that exceed LLM context windows.

**Evidence:**
- Real-world vulnerability identification requires multi-step reasoning with tool feedback
- Moving from directed to broad-scope scenarios decreases effectiveness and increases cost 2-2.5x
- Enterprise environments are orders of magnitude more complex than CTF challenges

**PROJ-010 Mitigation:** Leverage Jerry's filesystem-as-memory architecture to manage security assessment state across sessions. Decompose large assessments into focused analysis tasks. Use structured templates to keep each interaction focused and context-efficient.

---

## Ethical Boundaries

### Safety Alignment Impact on Red Team Capabilities

The tension between LLM safety alignment and offensive security utility is the defining challenge for any AI-assisted red team tool.

**Current State:**
- Commercial models (Claude, GPT, Gemini) implement robust safety filters that refuse many offensive security requests
- Average compliance with cyber attack assistance decreased from 52% to 28% (CyberSecEval)
- Open-source/local models comply with up to 95% of requests but lack any safety guardrails
- Multi-round interaction or jailbreaking techniques can bypass safety filters but are ethically problematic

**What Models Refuse:**
- Direct exploit code generation for specific targets
- Malware creation or modification
- Attack automation against specific systems
- Social engineering content targeting real individuals
- Prompts with obfuscated text or encoded payloads

**What Models Allow (generally):**
- Security methodology guidance and planning
- Vulnerability analysis of code provided by the user
- Defensive security architecture recommendations
- Threat modeling and risk assessment
- Report generation and documentation
- General security education and training

**PROJ-010 Implications:**
- /red-team must operate within the "allowed" zone -- methodology guidance, planning, analysis, reporting
- Avoid designing features that require the LLM to generate exploit code or attack payloads
- Frame all capabilities as professional security methodology application
- Document ethical boundaries explicitly in skill design
- The methodology-first approach inherently avoids most safety alignment conflicts

### Responsible Disclosure Considerations

LLM-generated vulnerability findings must follow responsible disclosure practices. PROJ-010 should include guidance on disclosure timelines, coordination with vendors, and handling of sensitive findings.

### Dual-Use Risk Management

PROJ-010 must address the dual-use nature of security knowledge:
- /eng-team guidance on "common vulnerability patterns" could be misused to create vulnerabilities
- /red-team methodology guidance could be used for unauthorized testing
- Mitigation: governance through Jerry framework constraints, explicit ethical guidelines, audit trails

---

## Capability vs Augmentation Boundary

### Where the LLM Operates Autonomously (High Confidence)

| Task | LLM Role | Confidence | Notes |
|------|----------|------------|-------|
| Methodology selection | Recommend appropriate security framework/methodology for context | High | Core PROJ-010 value |
| Report structuring | Generate report templates and organize findings | High | /eng-team and /red-team |
| Knowledge retrieval | Surface relevant security guidance, standards, best practices | High | Both skills |
| Threat modeling facilitation | Guide STRIDE/DREAD/PASTA analysis through structured questioning | High | /eng-team |
| Risk prioritization | Rank and contextualize security findings | Medium-High | Both skills |
| Security architecture review | Analyze design patterns against security principles | Medium-High | /eng-team |

### Where the LLM Requires Tool Integration (Augmented)

| Task | LLM Role | Tool Role | Notes |
|------|----------|-----------|-------|
| Code vulnerability detection | Reason about findings, reduce false positives, explain | Static analysis tools detect | /eng-team guides tool selection and interpretation |
| Threat intelligence | Synthesize and contextualize | Threat feeds provide data | /red-team contextualizes for specific engagements |
| Configuration assessment | Analyze against best practices | Config parsers extract data | /eng-team guides assessment methodology |
| Attack path analysis | Reason about paths, prioritize | Graph databases (BloodHound) map | /red-team guides analysis approach |

### Where the LLM Should Not Operate (Human Required)

| Task | Why Human Required | PROJ-010 Approach |
|------|-------------------|-------------------|
| Exploit execution | Legal liability, real system impact, safety alignment blocks | Methodology guidance only |
| Authorization decisions | Legal and contractual obligations | Provide checklists, human decides |
| Novel vulnerability discovery | Creative reasoning beyond LLM capability | Guide methodology, human discovers |
| Physical security testing | Requires physical presence and judgment | Provide planning frameworks only |
| Disclosure decisions | Legal, ethical, and relationship considerations | Provide disclosure framework, human decides |

---

## Evidence and Citations

### Academic Research

- Meta CyberSecEval 3: [Paper](https://arxiv.org/abs/2408.01605) | [CyberSecEval 2](https://arxiv.org/abs/2404.13161) (accessed Feb 2026)
- HarmBench: [Paper](https://arxiv.org/abs/2402.04249) | [Website](https://www.harmbench.org/) | [GitHub](https://github.com/centerforaisafety/HarmBench) (accessed Feb 2026)
- PwnGPT exploit generation: [ACL 2025 paper](https://aclanthology.org/2025.acl-long.562.pdf) (accessed Feb 2026)
- LLM exploit generation evaluation: [Paper](https://arxiv.org/html/2505.01065v1) (accessed Feb 2026)
- CVE-Genie multi-agent CVE reproduction: [Paper](https://arxiv.org/html/2509.01835v1) (accessed Feb 2026)
- LLMs in Software Security survey: [ACM Computing Surveys](https://dl.acm.org/doi/10.1145/3769082) | [ArXiv](https://arxiv.org/abs/2502.07049) (accessed Feb 2026)
- LLM-as-Judge for code verification: [Frontiers](https://www.frontiersin.org/journals/computer-science/articles/10.3389/fcomp.2025.1655469/full) (accessed Feb 2026)
- AI agents vs cybersecurity professionals: [Paper](https://arxiv.org/html/2512.09882v1) (accessed Feb 2026)
- LLM red teaming survey: [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0306457325001803) (accessed Feb 2026)
- SORRY-BENCH refusal evaluation: [ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/file/9622163c87b67fd5a4a0ec3247cf356e-Paper-Conference.pdf) (accessed Feb 2026)

### Industry Benchmarks and Reports

- Wiz AI Cyber Model Arena: [Benchmark](https://www.wiz.io/blog/introducing-ai-cyber-model-arena-a-real-world-benchmark-for-ai-agents-in-cybersec) | [AI agents vs humans](https://www.wiz.io/blog/ai-agents-vs-humans-who-wins-at-web-hacking-in-2026) (accessed Feb 2026)
- Hack the Box AI vs Human CTF: [Results](https://www.hackthebox.com/blog/ai-vs-human-ctf-hack-the-box-results) (accessed Feb 2026)
- Stanford ARTEMIS: [Euronews coverage](https://www.euronews.com/next/2025/12/15/for-15-an-hour-an-ai-agent-outperforms-human-hackers-study-shows) (accessed Feb 2026)
- HackerOne 2025 report: [AI security trends](https://www.hackerone.com/blog/ai-security-trends-2025) | [210% spike](https://www.hackerone.com/press-release/hackerone-report-finds-210-spike-ai-vulnerability-reports-amid-rise-ai-autonomy) (accessed Feb 2026)
- Google Big Sleep: [Project Zero blog](https://projectzero.google/2024/10/from-naptime-to-big-sleep.html) | [20 vulnerabilities](https://techcrunch.com/2025/08/04/google-says-its-ai-based-bug-hunter-found-20-security-vulnerabilities/) (accessed Feb 2026)
- Snyk AI code security benchmark: [Comparison](https://sanj.dev/post/ai-code-security-tools-comparison) (accessed Feb 2026)

### Hallucination and Failure Mode Evidence

- NVD backlog crisis: [OWASP LLM09:2025 Misinformation](https://genai.owasp.org/llmrisk/llm092025-misinformation/) (accessed Feb 2026)
- AI-generated false vulnerability reports: [AI slop vs OSS security](https://devansh.bearblog.dev/ai-slop/) (accessed Feb 2026)
- AI-generated code vulnerabilities: [Endor Labs analysis](https://www.endorlabs.com/learn/the-most-common-security-vulnerabilities-in-ai-generated-code) (accessed Feb 2026)
- LLM-assisted CTI vulnerabilities: [Paper](https://arxiv.org/html/2509.23573v3) (accessed Feb 2026)

### Safety Alignment and Ethical Boundaries

- Local LLM security paradox: [Quesma blog](https://quesma.com/blog/local-llms-security-paradox/) (accessed Feb 2026)
- System-level safety red teaming: [Paper](https://arxiv.org/abs/2506.05376) (accessed Feb 2026)
- General Analysis LLM safety benchmarks: [Leaderboard](https://www.generalanalysis.com/benchmarks) (accessed Feb 2026)
- GitHub Copilot replicating vulnerabilities: [TechTarget](https://www.techtarget.com/searchsecurity/news/366571117/GitHub-Copilot-replicating-vulnerabilities-insecure-code) (accessed Feb 2026)

---

## Implications for PROJ-010

### Design Implication 1: Methodology-First Architecture Is Validated

The evidence overwhelmingly supports PROJ-010's design as methodology guidance rather than execution automation. LLMs excel at exactly the capabilities /eng-team and /red-team need: structured reasoning, knowledge synthesis, methodology application, and report generation. The capabilities where LLMs fail (exploit execution, runtime analysis, novel discovery) are explicitly out of scope.

### Design Implication 2: Hallucination Mitigation Must Be Central

Every output from /eng-team and /red-team must include appropriate confidence indicators and verification guidance. The skills should never present AI-generated findings as ground truth. Structured templates with explicit "verify by" instructions are essential.

### Design Implication 3: Safety Alignment Compatibility Required

Both skills must be designed to work within commercial LLM safety boundaries. This means:
- Frame all guidance as professional security methodology application
- Avoid patterns that trigger safety filters (direct exploit requests, attack code generation)
- Use established security terminology and professional context
- Test against safety alignment to ensure legitimate use cases are not blocked

### Design Implication 4: Tool Integration Design Matters

The Wiz AI Cyber Model Arena demonstrated that agent scaffold matters as much as model capability. PROJ-010's integration with Jerry framework (quality enforcement, knowledge management, workflow structure) is a significant advantage. The skill architecture should be designed to orchestrate tool integration rather than replacing tools.

### Design Implication 5: Domain Specialization Over Generalization

Benchmarks consistently show that AI security capabilities are highly domain-specific. /eng-team and /red-team should specialize deeply in their respective domains rather than attempting to cover all security tasks. This specialization aligns with Jerry's skill architecture.

### Design Implication 6: Human-in-the-Loop Is Not Optional

No benchmark or study supports fully autonomous security operations without human oversight. PROJ-010 should design for "bionic" security practitioners -- human experts augmented by AI methodology guidance -- rather than autonomous security agents. This is both the most effective and most ethically sound approach.
