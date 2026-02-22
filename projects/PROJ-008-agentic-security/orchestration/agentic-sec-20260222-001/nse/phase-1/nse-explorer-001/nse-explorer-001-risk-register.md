# Agentic Security Risk Register (FMEA)

> Agent: nse-explorer-001
> Phase: 1 (Requirements Discovery)
> Pipeline: NSE (NASA-SE)
> Status: COMPLETE
> Date: 2026-02-22

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary-l0) | Total risks, top 5 by RPN, critical categories |
| [FMEA Methodology](#fmea-methodology-l2) | Scoring criteria, scale definitions, RPN calculation |
| [Severity Scale](#severity-scale) | 1-10 severity scoring definitions |
| [Occurrence Scale](#occurrence-scale) | 1-10 occurrence scoring definitions |
| [Detection Scale](#detection-scale) | 1-10 detection scoring definitions |
| [Risk Register](#risk-register-l1) | All 60 failure modes across 10 categories |
| [Category 1: Prompt Injection Attacks](#category-1-prompt-injection-attacks) | Direct, indirect, extraction, goal hijacking |
| [Category 2: Privilege Escalation](#category-2-privilege-escalation) | Tool tier bypass, nesting violation, permission escape |
| [Category 3: Supply Chain Threats](#category-3-supply-chain-threats) | MCP poisoning, dependency attacks, skill tampering |
| [Category 4: Data Exfiltration](#category-4-data-exfiltration) | Credential leakage, prompt exposure, cross-agent leak |
| [Category 5: Agent Manipulation](#category-5-agent-manipulation) | Goal hijacking, tool misuse, memory manipulation |
| [Category 6: Inter-Agent Communication](#category-6-inter-agent-communication) | Trust boundary, handoff poisoning, contamination |
| [Category 7: Infrastructure Threats](#category-7-infrastructure-threats) | MCP compromise, filesystem, network, denial of service |
| [Category 8: Governance Bypass](#category-8-governance-bypass) | Constitutional circumvention, quality gate manipulation |
| [Category 9: Cascading Failures](#category-9-cascading-failures) | Error propagation, quality degradation, context rot |
| [Category 10: Identity and Access](#category-10-identity-and-access) | Agent spoofing, session hijacking, authority bypass |
| [Top 20 Risks by RPN Score](#top-20-risks-by-rpn-score) | Prioritized risk ranking |
| [Risk Heat Map](#risk-heat-map-l2) | Visual severity vs. occurrence distribution |
| [Jerry-Specific Vulnerabilities](#jerry-specific-vulnerabilities) | Architecture-specific threat analysis |
| [Recommended Risk Mitigation Priorities](#recommended-risk-mitigation-priorities) | Top 10 actions for Phase 2 |
| [Citations](#citations) | All sources with authority classification |

---

## Executive Summary (L0)

- **Total failure modes analyzed:** 60 across 10 threat categories, scored using FMEA methodology (Severity x Occurrence x Detection = RPN).
- **Top 5 risks by RPN:** (1) Indirect prompt injection via MCP tool results (RPN 504), (2) Malicious MCP server packages (RPN 480), (3) Constitutional constraint circumvention via context rot (RPN 432), (4) Indirect prompt injection via file contents (RPN 392), (5) Agent goal hijacking through poisoned context (RPN 378).
- **Most critical category:** Category 1 (Prompt Injection Attacks) dominates the top 20 with 5 entries, followed closely by Category 3 (Supply Chain Threats) with 4 entries and Category 8 (Governance Bypass) with 3 entries.
- **Industry validation:** Meta-analysis of 78 recent studies (2021-2026) shows attack success rates against state-of-the-art defenses exceed 85% when adaptive attack strategies are employed. The joint OpenAI/Anthropic/Google DeepMind study ("The Attacker Moves Second") demonstrated 12 published defenses bypassed with >90% success using adaptive attacks.
- **Jerry's existing defense posture:** The 5-layer enforcement architecture (L1-L5), constitutional HARD rules, and tool tier system (T1-T5) provide defense-in-depth that exceeds most agentic frameworks. However, critical gaps exist in: indirect prompt injection detection on tool outputs (L4 gap), MCP supply chain verification (no L3/L5 gate), and cross-agent data flow validation (handoff integrity not cryptographically verified).

---

## FMEA Methodology (L2)

This risk register uses Failure Mode and Effects Analysis (FMEA) per SAE J1739 / IEC 60812 methodology adapted for agentic AI systems. Each failure mode is scored on three independent dimensions:

- **Severity (S):** Impact magnitude if the failure occurs (1-10 scale).
- **Occurrence (O):** Likelihood that the failure mode will manifest (1-10 scale).
- **Detection (D):** Ability of current controls to detect the failure before impact (1-10 scale, where 1 = almost certain detection, 10 = almost impossible to detect).

**Risk Priority Number (RPN) = S x O x D** (range: 1-1000)

**RPN Action Thresholds:**

| RPN Range | Priority | Action Required |
|-----------|----------|-----------------|
| 400-1000 | Critical | Immediate mitigation; Phase 2 architecture MUST address |
| 200-399 | High | Phase 2 architecture SHOULD address; implement by Phase 3 |
| 100-199 | Medium | Address during Phase 3 implementation |
| 1-99 | Low | Monitor; address if resources permit |

**Scoring calibration:** Scores are calibrated against industry incident data from the Anthropic GTG-1002 disclosure, Cisco State of AI Security 2026 report, OWASP Agentic Top 10, and the Agent Security Bench (ASB) published at ICLR 2025. Jerry-specific mitigations are factored into Detection scores where applicable.

---

## Severity Scale

| Score | Level | Description |
|-------|-------|-------------|
| 1 | Negligible | No observable impact on system or users. Cosmetic issue only. |
| 2 | Very Minor | Minor inconvenience. Agent output slightly degraded but still usable. |
| 3 | Minor | Single agent task fails; easily retried. No data exposure. |
| 4 | Low | Multiple agent tasks fail. Minor data exposure (non-sensitive). Recoverable within session. |
| 5 | Moderate | Significant workflow disruption. Partial sensitive data exposure. Requires manual intervention. |
| 6 | Significant | Complete workflow failure. Sensitive data exposed to unauthorized context. Requires session restart. |
| 7 | High | Governance constraint bypassed. Significant sensitive data exposure. Agent performs unauthorized actions. |
| 8 | Very High | Constitutional rule violation achieved. Credential exposure. Agent executes actions against user intent. |
| 9 | Critical | Full agent compromise. System-wide credential exposure. Persistent unauthorized access established. |
| 10 | Catastrophic | Complete system compromise. Irreversible data exfiltration. External system damage. Arbitrary code execution on host. |

---

## Occurrence Scale

| Score | Level | Description |
|-------|-------|-------------|
| 1 | Extremely Unlikely | < 1 in 100,000 sessions. Requires nation-state resources and novel zero-day. |
| 2 | Very Unlikely | 1 in 10,000 sessions. Requires sophisticated attacker with Jerry-specific knowledge. |
| 3 | Unlikely | 1 in 1,000 sessions. Requires moderate attacker skill and framework familiarity. |
| 4 | Low | 1 in 500 sessions. Known attack vector but requires specific conditions. |
| 5 | Moderate | 1 in 100 sessions. Documented attack technique applicable to Jerry's architecture. |
| 6 | Moderately High | 1 in 50 sessions. Common attack pattern with available tooling. |
| 7 | High | 1 in 20 sessions. Well-documented attack with high applicability. Meta-analysis: >50% success rate. |
| 8 | Very High | 1 in 10 sessions. Trivially exploitable with standard tools. Industry incident precedent. |
| 9 | Almost Certain | 1 in 5 sessions. Inherent architectural vulnerability. Active exploitation in the wild. |
| 10 | Inevitable | Every session. Fundamental design limitation. Cannot be prevented, only mitigated. |

---

## Detection Scale

| Score | Level | Description |
|-------|-------|-------------|
| 1 | Almost Certain | L3/L5 deterministic gate catches 100% of occurrences before execution. |
| 2 | Very High | L3 pre-tool check catches >95% before execution. Minimal bypass opportunity. |
| 3 | High | L2 per-prompt re-injection + L4 post-tool inspection catches >90%. |
| 4 | Moderately High | L4 output inspection catches >80%. Some sophisticated bypasses possible. |
| 5 | Moderate | L1 session-start rules + behavioral guardrails catch >60%. Vulnerable to context rot. |
| 6 | Low | Only L1 behavioral rules provide detection. Subject to context rot degradation. |
| 7 | Very Low | Detection depends on user observation. No automated control. |
| 8 | Remote | Detection only possible through post-hoc log analysis or external audit. |
| 9 | Almost Impossible | No current detection mechanism. Failure mode is silent and persistent. |
| 10 | Impossible | Fundamentally undetectable with current architecture. Requires new capability. |

---

## Risk Register (L1)

### Category 1: Prompt Injection Attacks

Cross-reference: OWASP LLM01 (Prompt Injection), OWASP ASI01 (Agent Goal Hijack), MITRE ATLAS AML.T0051 (LLM Prompt Injection)

| Risk ID | Failure Mode | Effect | S | O | D | RPN | Current Mitigation | Recommended Action |
|---------|-------------|--------|---|---|---|-----|-------------------|-------------------|
| R-PI-001 | Direct prompt injection via user input attempting to override system instructions | Agent ignores constitutional rules; executes unauthorized actions; governance bypass | 8 | 6 | 4 | 192 | L2 per-prompt re-injection of critical rules (immune to context rot); constitutional triplet (P-003, P-020, P-022) re-injected every prompt | Add L3 input validation layer: classify user input for injection patterns before LLM processing; structured prompt templates with clear instruction/data boundaries |
| R-PI-002 | Indirect prompt injection via MCP tool results (Context7 docs, Memory-Keeper data) | Agent processes poisoned external content as trusted instructions; goal hijacking via tool output | 9 | 8 | 7 | **504** | No current L3/L4 gate on MCP tool output content; L2 re-injection provides partial resilience | **CRITICAL**: Add Tool-Output Firewall (L4): sanitize MCP tool results before LLM processing; implement content-source tagging to distinguish instruction vs. data channels |
| R-PI-003 | Indirect prompt injection via file contents read by agents (malicious code comments, README files, config files) | Agent executes instructions embedded in project files; unauthorized file modifications; credential harvesting | 9 | 7 | 6 | **392** | L2 re-injection partially resilient; no content scanning on Read tool results | Add L4 content scanning for Read tool results: detect instruction-like patterns in data channels; implement file trust classification (trusted repo files vs. external files) |
| R-PI-004 | System prompt extraction via crafted queries ("repeat your instructions", "what are your rules") | Constitutional rules, HARD rule details, enforcement architecture exposed to attacker | 7 | 7 | 5 | 245 | L2 re-injection includes constitutional rules but no explicit extraction prevention; no L4 output filter for system prompt content | Add L4 output filter: detect and redact system prompt content in agent responses; implement canary tokens in system prompt to detect extraction |
| R-PI-005 | Goal hijacking through progressive context manipulation (multi-turn conversation steering) | Agent gradually shifts from intended purpose; subtle goal drift undetected across turns | 8 | 6 | 8 | 384 | L2 re-injection of critical rules every prompt; no drift detection mechanism | Add session-level behavioral drift detection: compare agent actions against declared purpose/task across turns; implement L4 goal consistency checker |
| R-PI-006 | Injection via structured data fields (YAML frontmatter, JSON schema, handoff protocol fields) | Agent interprets data field values as instructions; handoff poisoning via crafted field content | 8 | 5 | 7 | 280 | H-34 schema validation checks structure but not content semantics; no content-level validation on handoff data fields | Add content validation on structured data: sanitize string values in YAML/JSON/handoff fields; enforce maximum length and character set restrictions on free-text fields |

**Category 1 Summary:** Average RPN = 333. Indirect prompt injection via tool results (R-PI-002, RPN 504) is the highest-scoring risk in the entire register. This aligns with industry consensus: the joint OpenAI/Anthropic/Google study found >90% bypass rates against published defenses. Jerry's L2 re-injection provides significant resilience against direct injection but offers limited protection against indirect injection through data channels (MCP results, file contents).

---

### Category 2: Privilege Escalation

Cross-reference: OWASP ASI03 (Privilege Escalation), OWASP LLM06 (Excessive Agency), MITRE ATT&CK TA0004 (Privilege Escalation)

| Risk ID | Failure Mode | Effect | S | O | D | RPN | Current Mitigation | Recommended Action |
|---------|-------------|--------|---|---|---|-----|-------------------|-------------------|
| R-PE-001 | Tool tier bypass: T1 (Read-Only) agent accessing Write/Edit/Bash tools through prompt manipulation | Validation agent writes to files; read-only agent modifies codebase; integrity violation | 9 | 4 | 3 | 108 | H-34 schema validates `capabilities.allowed_tools` in agent definitions; L3 pre-tool check should verify tool access; H-35 forbids Task in worker agents | Implement runtime L3 tool access enforcement: verify calling agent identity against allowed_tools whitelist before every tool invocation; log all tool access attempts |
| R-PE-002 | P-003 nesting violation: worker agent spawns sub-workers via Task tool | Recursive delegation chain; uncontrolled agent proliferation; token exhaustion; accountability loss | 9 | 3 | 2 | 54 | H-01/P-003 HARD rule; H-35 requires workers exclude Task from allowed_tools; L2 re-injection of P-003 every prompt | Current controls are strong. Add L5 CI validation: grep all worker agent definitions for Task tool presence; automated rejection |
| R-PE-003 | Permission boundary escape via Bash tool: agent executes system commands beyond intended scope | Arbitrary command execution on host; file system modification; network access; credential theft | 10 | 5 | 5 | 250 | Tool tier system restricts Bash to T2+; no command-level restriction within Bash tool | Add command allowlist/blocklist for Bash tool (L3): restrict to safe commands per agent role; block `curl`, `wget`, `ssh`, `nc` by default; require explicit approval for network commands |
| R-PE-004 | Privilege accumulation through multi-hop handoffs: each agent adds capabilities across chain | Downstream agent inherits combined privileges of all upstream agents; violates least privilege | 8 | 5 | 7 | 280 | HD-M-004 requires criticality not decrease; no explicit privilege tracking in handoff protocol | Add privilege tracking to handoff schema: each handoff declares maximum tool tier; downstream agent MUST NOT exceed upstream privilege level; L3 enforcement |
| R-PE-005 | MCP server grants elevated filesystem access beyond agent's declared tool tier | Agent reads/writes files outside its declared scope via MCP server capabilities | 8 | 6 | 6 | 288 | No current MCP-to-tool-tier mapping; MCP servers operate outside tool tier enforcement | Add MCP capability mapping to tool tier system: each MCP server declares maximum privilege level; L3 gate validates MCP operations against agent's tier |
| R-PE-006 | Environment variable exposure: agent accesses API keys, tokens, secrets via Bash env inspection | Credential theft; API key compromise; external service unauthorized access | 9 | 6 | 5 | 270 | No current environment variable filtering; Bash tool has full env access | Add environment variable sandboxing: filter sensitive env vars before Bash execution; implement secret detection in L4 output filtering |

**Category 2 Summary:** Average RPN = 208. MCP-based privilege escalation (R-PE-005, RPN 288) and privilege accumulation through handoffs (R-PE-004, RPN 280) highlight gaps in the current architecture where tool tier enforcement does not extend to MCP operations or multi-agent chains. The P-003 nesting violation (R-PE-002, RPN 54) is well-mitigated by existing controls.

---

### Category 3: Supply Chain Threats

Cross-reference: OWASP ASI04 (Agentic Supply Chain Vulnerabilities), OWASP LLM03 (Supply Chain), MITRE ATLAS AML.T0018 (ML Supply Chain Compromise)

| Risk ID | Failure Mode | Effect | S | O | D | RPN | Current Mitigation | Recommended Action |
|---------|-------------|--------|---|---|---|-----|-------------------|-------------------|
| R-SC-001 | Malicious MCP server package: compromised or trojanized MCP server in tool chain | Full agent compromise; data exfiltration via BCC-style shadowing; credential harvesting; backdoor persistence | 10 | 8 | 6 | **480** | No MCP server verification mechanism; `.claude/settings.local.json` configures MCP servers manually; no integrity checking | **CRITICAL**: Implement MCP server verification: cryptographic hash pinning, allowlisted server registry, runtime integrity monitoring; add L5 CI gate to verify MCP server configurations |
| R-SC-002 | Dependency poisoning via compromised pip/npm packages consumed by MCP servers or skills | Code execution in build/runtime environment; persistent backdoor; data theft | 9 | 6 | 7 | 378 | H-05 UV-only enforcement for Python; no dependency integrity verification beyond UV lock file | Add dependency verification: lockfile integrity checking at L5; SCA scanning for known vulnerabilities; pin all transitive dependencies; monitor for typosquatting |
| R-SC-003 | Skill/agent definition tampering: malicious modification of agent YAML/Markdown definitions | Agent behavior altered; guardrails removed; tool access expanded; constitutional compliance bypassed | 10 | 4 | 4 | 160 | H-34 schema validation; H-35 constitutional triplet requirement; L5 CI gate on agent definitions; git version control | Add integrity verification: cryptographic signing of agent definitions; L3 runtime hash comparison against committed versions; audit log for all definition changes |
| R-SC-004 | Context7 library data poisoning: compromised documentation returns malicious content | Agents incorporate malicious patterns from poisoned docs; indirect injection via research results | 8 | 5 | 8 | 320 | MCP-001 mandates Context7 for external docs; no verification of Context7 content integrity | Add source verification layer: cross-reference Context7 results against known-good sources; flag content that contains instruction-like patterns; implement content trust scoring |
| R-SC-005 | Model supply chain: fine-tuning attack or compromised model weights serving unexpected behavior | Behavioral changes bypass all prompt-level controls; subtle bias introduction; backdoor activation | 10 | 2 | 9 | 180 | Jerry uses Anthropic API (model integrity managed by Anthropic); no local model hosting | Monitor Anthropic model behavior: baseline expected model responses; detect behavioral drift across model updates; maintain model version pinning capability |
| R-SC-006 | L2-REINJECT marker tampering: removal or modification of per-prompt re-injection HTML comments | Critical HARD rules no longer re-injected; context rot immunity destroyed; governance bypass enabled | 10 | 3 | 3 | 90 | L2 markers in committed files; L5 CI can verify marker presence; git version control | Add L5 CI gate: verify all required L2-REINJECT markers are present and unmodified in every commit; automated marker integrity checking |

**Category 3 Summary:** Average RPN = 268. Malicious MCP servers (R-SC-001, RPN 480) represent the second-highest risk, validated by Cisco's finding that MCP creates a "vast unmonitored attack surface" and the Anthropic GTG-1002 incident demonstrating MCP supply chain exploitation. Context7 data poisoning (R-SC-004, RPN 320) is a Jerry-specific risk due to MCP-001 mandating Context7 as the primary documentation source.

---

### Category 4: Data Exfiltration

Cross-reference: OWASP LLM02 (Sensitive Information Disclosure), OWASP LLM07 (System Prompt Leakage), MITRE ATT&CK TA0010 (Exfiltration)

| Risk ID | Failure Mode | Effect | S | O | D | RPN | Current Mitigation | Recommended Action |
|---------|-------------|--------|---|---|---|-----|-------------------|-------------------|
| R-DE-001 | Credential leakage through agent output: API keys, tokens, passwords in generated text | External service compromise; unauthorized access to third-party systems; financial exposure | 9 | 6 | 5 | 270 | Guardrails template requires `no_secrets_in_output` in output_filtering; behavioral enforcement only (L1) | Add L4 deterministic secret detection: regex-based scanning of all agent output for credential patterns (API keys, tokens, passwords); block output containing detected secrets |
| R-DE-002 | System prompt / constitutional rule exposure in agent responses | Attacker learns governance structure, HARD rules, enforcement gaps; enables targeted bypass attempts | 7 | 7 | 6 | 294 | L2 re-injection does not include extraction prevention; no L4 output filtering for system prompt content | Add L4 system prompt canary detection: embed unique canary tokens; detect their presence in output; implement response scanning for rule content verbatim matches |
| R-DE-003 | Sensitive file content in agent responses: private keys, .env files, credentials.json read and output | Full credential exposure; infrastructure compromise; third-party service breach | 10 | 5 | 5 | 250 | Agent guardrails include `no_secrets_in_output`; no file-level access control; Read tool can access any file | Add file access control layer (L3): maintain sensitive file patterns (.env, *.key, credentials.*, id_rsa); block Read operations on sensitive files; require explicit user approval |
| R-DE-004 | Cross-agent data leakage via handoff protocol: sensitive data passed between agents without need-to-know | Information from one task context bleeds into another; violates data minimization principle | 7 | 6 | 7 | 294 | CB-03 recommends file-path references over inline content; no data classification in handoff protocol | Add data classification to handoff schema: tag artifacts with sensitivity level; L3 validates receiving agent's clearance level matches data classification |
| R-DE-005 | Memory-Keeper data exposure: stored context items accessible across sessions without access control | Prior session sensitive data exposed to new sessions; cross-project data leakage | 7 | 5 | 7 | 245 | Memory-Keeper key pattern `jerry/{project}/` provides namespace isolation; no access control enforcement | Add session-level access control to Memory-Keeper: enforce project-scoped access; require authentication for cross-project reads; audit all cross-session access |
| R-DE-006 | Exfiltration via Bash tool: agent uses curl/wget to send data to external endpoints | Data exfiltration to attacker-controlled servers; silent and persistent | 10 | 4 | 6 | 240 | No network access control on Bash tool; no command filtering | Add network egress filtering (L3): block outbound network commands by default; allowlist specific domains; log all network operations; require user approval for external communication |

**Category 4 Summary:** Average RPN = 265. System prompt exposure (R-DE-002, RPN 294) and cross-agent data leakage (R-DE-004, RPN 294) are the top category risks. Jerry's guardrails template provides behavioral guidance (`no_secrets_in_output`) but lacks deterministic L3/L4 enforcement for data exfiltration prevention.

---

### Category 5: Agent Manipulation

Cross-reference: OWASP ASI01 (Agent Goal Hijack), OWASP ASI02 (Tool Misuse), OWASP ASI05 (Memory/Context Manipulation), OWASP ASI10 (Rogue Agents)

| Risk ID | Failure Mode | Effect | S | O | D | RPN | Current Mitigation | Recommended Action |
|---------|-------------|--------|---|---|---|-----|-------------------|-------------------|
| R-AM-001 | Agent goal hijacking through poisoned context: attacker injects goal-altering instructions into agent's working context | Agent pursues attacker's objectives while appearing to work on user's task; subtle misdirection | 9 | 7 | 6 | **378** | L2 re-injection of constitutional rules; H-02/P-020 user authority principle; no runtime goal consistency verification | Add goal consistency monitoring (L4): compare agent actions against declared task/purpose each turn; detect behavioral deviation from initial task assignment; alert on goal drift |
| R-AM-002 | Tool misuse: agent uses tools beyond intended scope (e.g., Read agent using Write, research agent modifying code) | Unauthorized modifications; data corruption; integrity violations | 8 | 5 | 3 | 120 | H-34/H-35 tool restrictions in agent definitions; tool tier system T1-T5; schema-validated allowed_tools list | Implement runtime tool access matrix enforcement (L3): verify every tool call against agent's declared allowed_tools; reject unauthorized tool invocations deterministically |
| R-AM-003 | Memory/context manipulation: poisoning of Memory-Keeper stores or cached file data | Persistent incorrect context influences future agent decisions; corrupted research findings propagated | 8 | 5 | 8 | 320 | MCP-002 requires Memory-Keeper at phase boundaries; no integrity verification on stored/retrieved data | Add integrity verification to Memory-Keeper operations: cryptographic hashing of stored content; verify hash on retrieval; detect tampering between store and retrieve |
| R-AM-004 | Rogue agent behavior: agent deviates from defined methodology due to adversarial input or model instability | Agent produces harmful output; bypasses guardrails; violates constitutional constraints while appearing compliant | 9 | 4 | 7 | 252 | Constitutional triplet (P-003, P-020, P-022) in every agent; guardrails template; L2 re-injection | Add behavioral attestation: agent must declare actions before execution; L4 validates declared actions match actual tool calls; implement action logging with post-hoc audit |
| R-AM-005 | Cognitive mode exploitation: attacker crafts input that exploits specific cognitive mode weaknesses (e.g., divergent mode's broad exploration used to explore attacker-controlled sources) | Agent follows attacker-planted research trails; introduces malicious references into findings | 7 | 4 | 8 | 224 | Cognitive mode taxonomy defines expected behavior; no runtime mode enforcement | Add mode-specific guardrails: divergent mode limits source exploration to allowlisted domains; convergent mode requires evidence threshold before conclusions; forensic mode logs all causal chain steps |
| R-AM-006 | Output template manipulation: agent generates output in unexpected format that bypasses downstream validation | Malformed output evades quality gate; schema validation tricked by edge cases; downstream agents misparse | 6 | 5 | 5 | 150 | H-34 schema validation; output.required and output.location in agent definitions; quality gate scoring | Add strict output schema enforcement (L3): validate agent output structure before delivery; reject non-conforming output; implement output checksums in handoff |

**Category 5 Summary:** Average RPN = 241. Agent goal hijacking (R-AM-001, RPN 378) and memory manipulation (R-AM-003, RPN 320) are the critical risks. The gap between Jerry's schema-level validation (H-34) and runtime behavioral enforcement is the primary vulnerability. Anthropic's GTG-1002 incident demonstrated that model-level guardrails are "architectural suggestions, not enforcement mechanisms" -- validating the need for deterministic L3 enforcement beyond behavioral rules.

---

### Category 6: Inter-Agent Communication

Cross-reference: OWASP ASI04 (Delegated Trust Boundary Violations), OWASP ASI07 (Insecure Inter-Agent Communication), OWASP ASI08 (Cascading Failures)

| Risk ID | Failure Mode | Effect | S | O | D | RPN | Current Mitigation | Recommended Action |
|---------|-------------|--------|---|---|---|-----|-------------------|-------------------|
| R-IC-001 | Delegated trust boundary violation: orchestrator passes elevated trust to worker via handoff without validation | Worker operates with trust level exceeding its defined scope; trust transitivity violation | 8 | 6 | 6 | 288 | HD-M-004 criticality non-decrease rule; handoff schema requires criticality field; no trust-level tracking | Add explicit trust boundary enforcement in handoff protocol: each agent declares maximum trust level; orchestrator validates worker trust level before delegation; L3 enforcement |
| R-IC-002 | Handoff data poisoning: malicious content injected into handoff artifacts or key_findings fields | Downstream agent processes poisoned findings as trusted upstream output; error amplification | 8 | 5 | 7 | 280 | Handoff schema validates required fields (HD-M-001); content validation limited to structural checks | Add content integrity verification to handoff: hash handoff artifacts at send; verify at receive; implement content scanning on key_findings for injection patterns |
| R-IC-003 | Insecure inter-agent communication: Task tool passes full context without data minimization | Worker receives more context than necessary; expanded attack surface; violates least privilege | 7 | 7 | 6 | 294 | CB-03 recommends file-path references over inline content; CB-04 limits key_findings to 3-5 bullets; these are MEDIUM standards, not enforced | Enforce data minimization in Task invocations (L3): validate Task prompt size against maximum threshold; flag prompts exceeding threshold for user review; enforce CB-03/CB-04 at L3 |
| R-IC-004 | Cross-pipeline contamination at barriers: poisoned PS pipeline output influences NSE pipeline decisions | Incorrect research findings corrupt requirements; cascading quality degradation across pipelines | 8 | 4 | 6 | 192 | Cross-pollination barriers exist in orchestration; quality gates at barriers; adversarial review at barriers | Add cross-pipeline integrity gates: independent validation of cross-pipeline artifacts; require adversarial review (S-001) on barrier-crossing deliverables; implement artifact provenance tracking |
| R-IC-005 | Message replay attack: captured handoff data replayed to redirect agent actions | Agent processes stale or recycled instructions; performs outdated or repeated actions | 6 | 3 | 8 | 144 | No replay prevention mechanism; handoffs lack timestamps or nonces | Add temporal validation to handoffs: include timestamps and request_id nonces; reject handoffs with expired timestamps; implement handoff sequence numbering |
| R-IC-006 | Orchestrator compromise leading to coordinated worker manipulation | All workers receive poisoned instructions from compromised orchestrator; systemic failure | 10 | 3 | 7 | 210 | Orchestrator is T5 (Full) tier; single point of coordination per P-003; no orchestrator integrity monitoring | Add orchestrator behavioral monitoring: validate orchestrator instructions against ORCHESTRATION.yaml plan; detect deviations from declared workflow; alert on unexpected agent invocations |

**Category 6 Summary:** Average RPN = 235. Insecure inter-agent communication (R-IC-003, RPN 294) scores highest due to the gap between MEDIUM-tier data minimization standards (CB-03, CB-04) and enforced L3 controls. Delegated trust boundary violations (R-IC-001, RPN 288) and handoff data poisoning (R-IC-002, RPN 280) reflect the absence of cryptographic integrity in the handoff protocol.

---

### Category 7: Infrastructure Threats

Cross-reference: OWASP LLM10 (Unbounded Consumption), MITRE ATT&CK TA0011 (Command and Control), MITRE ATT&CK TA0040 (Impact)

| Risk ID | Failure Mode | Effect | S | O | D | RPN | Current Mitigation | Recommended Action |
|---------|-------------|--------|---|---|---|-----|-------------------|-------------------|
| R-IT-001 | MCP server compromise: attacker gains control of running MCP server process | Full interception of tool results; injection of poisoned data; credential harvesting; persistent backdoor | 10 | 4 | 7 | 280 | MCP servers run as local processes; no runtime integrity monitoring; no process isolation | Add MCP server sandboxing: run MCP servers in isolated processes with minimal permissions; implement health monitoring; detect unexpected process behavior |
| R-IT-002 | File system manipulation: attacker modifies files read by agents between Write and Read operations (TOCTOU) | Agent reads tampered file content; integrity violation; potential code injection | 8 | 3 | 7 | 168 | Git version control provides audit trail; no runtime file integrity monitoring | Add file integrity monitoring for critical files: hash verification on Read operations for `.context/rules/`, agent definitions, and configuration files |
| R-IT-003 | SSRF via Bash/WebFetch tools: agent makes requests to internal network endpoints | Internal service discovery; credential harvesting from metadata endpoints; network lateral movement | 9 | 5 | 5 | 225 | No URL validation on WebFetch tool; no network egress filtering on Bash tool | Add URL allowlist for WebFetch (L3): block internal IP ranges (169.254.x.x, 10.x.x.x, 192.168.x.x); validate URLs against allowlist; log all external requests |
| R-IT-004 | Token exhaustion / denial of service via agent loops or unbounded tool calls | Session becomes unusable; cost escalation; context window exhausted | 7 | 6 | 4 | 168 | H-36 circuit breaker (3 hops max); RT-M-010 iteration ceilings (C1=3, C2=5, C3=7, C4=10); AE-006 context fill monitoring | Enhance circuit breaker: add token consumption tracking per agent per session; implement hard token budget limits; alert before budget exhaustion |
| R-IT-005 | Configuration file manipulation: attacker modifies `.claude/settings.local.json` to add malicious MCP servers | New attack-controlled MCP server injected into tool chain; persistent backdoor | 10 | 3 | 5 | 150 | File is tracked by git (changes visible in diffs); no runtime configuration validation | Add configuration integrity verification (L3): hash-verify settings files at session start; detect unauthorized modifications; alert on MCP server configuration changes |
| R-IT-006 | Bash command injection: agent constructs shell commands from untrusted input allowing injection | Arbitrary command execution on host; full system compromise | 10 | 5 | 6 | 300 | No input sanitization on Bash tool parameters; agents construct commands from context data | **HIGH**: Add Bash command sanitization (L3): validate command structure before execution; block shell metacharacters in dynamically constructed commands; implement command allowlisting per agent tier |

**Category 7 Summary:** Average RPN = 215. Bash command injection (R-IT-006, RPN 300) is the top infrastructure risk, followed by MCP server compromise (R-IT-001, RPN 280). Jerry's local-first architecture reduces cloud-specific attack surfaces but introduces host-level risks through the Bash tool's unrestricted execution capability.

---

### Category 8: Governance Bypass

Cross-reference: OWASP ASI01 (Agent Goal Hijack -- governance aspect), NIST CSF GV (Govern function), Jerry constitutional architecture

| Risk ID | Failure Mode | Effect | S | O | D | RPN | Current Mitigation | Recommended Action |
|---------|-------------|--------|---|---|---|-----|-------------------|-------------------|
| R-GB-001 | Constitutional constraint circumvention via context rot: HARD rules degrade as context fills | Rules loaded at L1 become unreliable at high context fill; agent violates HARD rules that are no longer in active context | 10 | 6 | 7.2 | **432** | L2 per-prompt re-injection of 20 Tier A rules (immune to context rot); Tier B rules rely on compensating controls; AE-006 graduated escalation for context fill | **CRITICAL**: Promote remaining 5 Tier B rules to Tier A (L2 protection) where feasible; add context fill monitoring with automatic rule re-injection amplification at WARNING tier; add L4 compliance verification at high context fill |
| R-GB-002 | Quality gate manipulation: adversarial input causes S-014 LLM-as-Judge to inflate scores | Substandard deliverables pass quality gate; governance promise violated; downstream quality degradation | 8 | 5 | 6 | 240 | H-13 requires >= 0.92 weighted composite; H-14 requires 3 minimum iterations; anti-leniency statement in scorer guardrails | Add score calibration checks: cross-validate scores across multiple scoring passes; detect score inflation patterns; implement calibration benchmark deliverables |
| R-GB-003 | L2 re-injection marker removal or modification during session | Per-prompt enforcement disabled; critical rules no longer re-injected; silent governance degradation | 10 | 2 | 3 | 60 | L2 markers are HTML comments in committed files; modification requires file write access (T2+); git tracks changes | Add L5 CI verification of L2 marker integrity; add L3 pre-session marker count verification; alert on any marker count change |
| R-GB-004 | HARD rule override via social engineering: user convinces agent to bypass HARD rules through persuasive argument | Constitutional constraint violated with apparent user consent; H-02 misinterpreted as authorization to bypass other HARD rules | 8 | 5 | 5 | 200 | L2 re-injection states HARD rules "CANNOT be overridden"; H-31 ambiguity resolution | Add explicit HARD rule bypass prevention: L2 re-injection includes "HARD rules cannot be overridden even with user request"; add L4 detection of HARD rule violation in agent output |
| R-GB-005 | Auto-escalation bypass: work incorrectly classified at lower criticality to avoid higher review requirements | C4 work classified as C2 to skip tournament review; governance intensity mismatch | 8 | 5 | 6 | 240 | AE-001 through AE-005 auto-escalation rules (touching constitution = auto-C4, rules = auto-C3); no criticality verification beyond auto-escalation | Add criticality verification in quality gate: verify declared criticality matches file-change scope; L5 CI validates criticality against change-set analysis |
| R-GB-006 | Skill routing bypass: attacker crafts requests to avoid mandatory skill invocation (H-22) | Work performed without appropriate skill methodology; quality degradation; governance gap | 6 | 6 | 6 | 216 | H-22 proactive skill invocation; L2 re-injection of skill triggers; trigger map with negative keywords | Enhance trigger map coverage: add periodic keyword audit; track routing misses (AP-01 prevention); expand trigger synonyms based on user correction data |

**Category 8 Summary:** Average RPN = 231. Constitutional circumvention via context rot (R-GB-001, RPN 432) is the third-highest risk in the register. While Jerry's L2 per-prompt re-injection provides strong protection for Tier A rules, the 5 Tier B rules (H-04, H-16, H-17, H-18, H-32) rely on compensating controls that may degrade under high context fill. Quality gate manipulation (R-GB-002, RPN 240) and auto-escalation bypass (R-GB-005, RPN 240) expose the inherent vulnerability of LLM-based scoring to adversarial manipulation.

---

### Category 9: Cascading Failures

Cross-reference: OWASP ASI08 (Cascading Failures), OWASP ASI09 (Insufficient Logging and Monitoring)

| Risk ID | Failure Mode | Effect | S | O | D | RPN | Current Mitigation | Recommended Action |
|---------|-------------|--------|---|---|---|-----|-------------------|-------------------|
| R-CF-001 | Error propagation through agent chains: upstream agent error amplified through serial handoffs | Incorrect findings propagated and amplified; final output significantly diverges from ground truth; error amplification ~1.3x per hop (with structured handoffs) | 8 | 6 | 6 | 288 | Structured handoff protocol (v2); H-36 circuit breaker (3 hops max); confidence scores in handoffs | Add error attenuation: require each agent to independently verify upstream key_findings; add "verification_status" field to handoff; implement cross-reference checks at each hop |
| R-CF-002 | Quality degradation through serial handoffs: information loss at each boundary | Key context lost at each handoff; downstream agents operate with incomplete picture; final output missing critical details | 7 | 7 | 6 | 294 | CB-02 through CB-05 context budget standards; handoff key_findings (3-5 bullets); artifact file-path references | Enforce handoff completeness verification: receiving agent must acknowledge all artifacts and key_findings; implement handoff receipt confirmation; track information coverage metrics |
| R-CF-003 | Context rot leading to security bypass: enforcement layers degrade as context fills during long sessions | Security controls become unreliable; agent ignores security-relevant rules; protection weakens silently | 9 | 7 | 5 | 315 | AE-006 graduated escalation (WARNING at 70%, CRITICAL at 80%, EMERGENCY at 88%); L2 re-injection immune to context rot | Implement automatic session partitioning for security-critical work: enforce session restart at CRITICAL context fill; preserve security state across sessions via Memory-Keeper; add L4 security rule compliance checking at every context tier |
| R-CF-004 | False positive in security controls: legitimate actions blocked by overly aggressive security gates | Workflow halted on valid operations; user frustration; security control bypass encouraged | 5 | 6 | 4 | 120 | Current security controls are behavioral (permissive); quality gate has defined thresholds | Design security controls with tunable sensitivity: implement confidence-based alerting vs. blocking; provide user override with audit trail; calibrate detection thresholds empirically |
| R-CF-005 | False negative in security controls: attack passes through all detection layers undetected | Full attack success despite defense-in-depth; false sense of security | 9 | 5 | 9 | 405 | 5-layer enforcement architecture (L1-L5); defense-in-depth design; multiple independent controls | Add adversarial testing program: red team exercises against Jerry's security controls; track detection rates per layer; implement canary attacks for continuous validation |
| R-CF-006 | Checkpoint data corruption: Memory-Keeper or file-based checkpoints corrupted during save | Session state lost or corrupted; unable to resume from last known good state; rework required | 6 | 3 | 5 | 90 | MCP-002 requires Memory-Keeper at phase boundaries; git provides file-level version control | Add checkpoint integrity verification: hash-verify checkpoint data on save and restore; implement redundant checkpointing (Memory-Keeper + file system); validate checkpoint completeness |

**Category 9 Summary:** Average RPN = 252. False negatives in security controls (R-CF-005, RPN 405) scores critically high because defense-in-depth, while the best available strategy, still has inherent gaps. The joint industry study ("The Attacker Moves Second") confirmed >90% bypass rates against published defenses. Quality degradation through serial handoffs (R-CF-002, RPN 294) is an inherent challenge of multi-agent architectures that Jerry's handoff protocol partially addresses but does not fully solve.

---

### Category 10: Identity and Access

Cross-reference: OWASP ASI06 (Identity and Access Mismanagement), OWASP ASI03 (Privilege Escalation -- identity aspect), NIST SP 800-53 IA (Identification and Authentication)

| Risk ID | Failure Mode | Effect | S | O | D | RPN | Current Mitigation | Recommended Action |
|---------|-------------|--------|---|---|---|-----|-------------------|-------------------|
| R-IA-001 | Agent identity spoofing: attacker crafts input that makes agent claim to be a different agent | Confused trust relationships; wrong methodology applied; security controls bypassed based on false identity | 8 | 4 | 7 | 224 | Agent names in YAML frontmatter; `from_agent` field in handoff; no cryptographic identity verification | Add cryptographic agent identity: each agent definition has a unique identity token; handoffs include signed agent identity; L3 validates agent identity before trust decisions |
| R-IA-002 | Insufficient authentication between agents: Task tool invokes workers without verifying orchestrator identity | Rogue orchestrator deploys workers; unauthorized delegation chains; accountability loss | 8 | 4 | 7 | 224 | P-003 enforces single-level nesting; Task tool is restricted to T5; no inter-agent authentication | Add orchestrator authentication: Task tool validates calling context against declared orchestrator; implement delegation tokens per handoff chain; log delegation lineage |
| R-IA-003 | Session hijacking: attacker gains access to running session context (memory, files, env vars) | Full session state exposed; ability to inject instructions; credential access; impersonation | 9 | 3 | 6 | 162 | Local-first architecture (no cloud sessions); file system permissions; OS-level access control | Leverage OS-level sandboxing: implement seatbelt/bubblewrap isolation per Anthropic model; restrict file access to project directory; sandbox network access |
| R-IA-004 | User authority bypass (P-020 violation): agent performs destructive action without user consent | Data loss; irreversible changes; trust violation; constitutional breach | 9 | 4 | 3 | 108 | H-02/P-020 HARD rule; L2 re-injection every prompt; H-31 ambiguity resolution (ask before destructive ops) | Add action classification (L3): classify tool calls as safe/destructive; require explicit user confirmation for destructive operations; implement undo capability where possible |
| R-IA-005 | Cross-project access: agent reads or modifies files from a different project's directory | Data exposure across project boundaries; integrity violation of unrelated project | 7 | 5 | 6 | 210 | H-04 requires active project; Memory-Keeper key pattern includes project ID; no file-level project boundary enforcement | Add project-scoped file access (L3): restrict Read/Write/Edit operations to active project directory and shared resources; block cross-project file access without explicit user approval |
| R-IA-006 | Stale session credentials: API tokens or MCP server credentials persist beyond intended session lifetime | Expired or revoked credentials used for unauthorized access; silent authentication failures; credential reuse attacks | 7 | 5 | 7 | 245 | No session-level credential management; MCP server credentials persist in configuration files | Add session-scoped credential management: implement credential rotation at session boundaries; validate credential freshness before use; revoke session-specific tokens on session end |

**Category 10 Summary:** Average RPN = 196. Stale session credentials (R-IA-006, RPN 245) and agent identity spoofing (R-IA-001, RPN 224) are the top risks. Jerry currently lacks cryptographic agent identity verification -- agents are identified by string names in YAML frontmatter and handoff `from_agent` fields, but no cryptographic mechanism prevents spoofing. This aligns with Microsoft's Agent 365 finding that unique agent identity is a prerequisite for enterprise-grade agent security.

---

## Top 20 Risks by RPN Score

| Rank | Risk ID | Failure Mode | RPN | Category | OWASP Ref | Recommended Priority |
|------|---------|-------------|-----|----------|-----------|---------------------|
| 1 | R-PI-002 | Indirect prompt injection via MCP tool results | **504** | 1: Prompt Injection | ASI01, LLM01 | CRITICAL -- Phase 2 architecture MUST address |
| 2 | R-SC-001 | Malicious MCP server packages | **480** | 3: Supply Chain | ASI04, LLM03 | CRITICAL -- Phase 2 architecture MUST address |
| 3 | R-GB-001 | Constitutional constraint circumvention via context rot | **432** | 8: Governance Bypass | ASI01 | CRITICAL -- Phase 2 architecture MUST address |
| 4 | R-CF-005 | False negative in security controls (attack passes undetected) | 405 | 9: Cascading Failures | ASI09 | CRITICAL -- Phase 2 architecture MUST address |
| 5 | R-PI-003 | Indirect prompt injection via file contents | **392** | 1: Prompt Injection | ASI01, LLM01 | CRITICAL -- Phase 2 architecture MUST address |
| 6 | R-PI-005 | Goal hijacking through progressive context manipulation | 384 | 1: Prompt Injection | ASI01 | HIGH -- Phase 2 architecture SHOULD address |
| 7 | R-AM-001 | Agent goal hijacking through poisoned context | **378** | 5: Agent Manipulation | ASI01 | HIGH -- Phase 2 architecture SHOULD address |
| 8 | R-SC-002 | Dependency poisoning via compromised pip/npm packages | 378 | 3: Supply Chain | ASI04, LLM03 | HIGH -- Phase 2 architecture SHOULD address |
| 9 | R-SC-004 | Context7 library data poisoning | 320 | 3: Supply Chain | ASI04 | HIGH -- Phase 2 architecture SHOULD address |
| 10 | R-AM-003 | Memory/context manipulation via Memory-Keeper | 320 | 5: Agent Manipulation | ASI05 | HIGH -- Phase 2 architecture SHOULD address |
| 11 | R-CF-003 | Context rot leading to security bypass | 315 | 9: Cascading Failures | ASI08 | HIGH -- Phase 2 architecture SHOULD address |
| 12 | R-IT-006 | Bash command injection | 300 | 7: Infrastructure | ASI02, ASI05 | HIGH -- Phase 2 architecture SHOULD address |
| 13 | R-DE-002 | System prompt / constitutional rule exposure | 294 | 4: Data Exfiltration | LLM07 | HIGH -- Phase 2 architecture SHOULD address |
| 14 | R-DE-004 | Cross-agent data leakage via handoff protocol | 294 | 4: Data Exfiltration | ASI07 | HIGH -- Phase 2 architecture SHOULD address |
| 15 | R-IC-003 | Insecure inter-agent communication (data minimization gap) | 294 | 6: Inter-Agent Communication | ASI07 | HIGH -- Phase 2 architecture SHOULD address |
| 16 | R-CF-002 | Quality degradation through serial handoffs | 294 | 9: Cascading Failures | ASI08 | HIGH -- Phase 2 architecture SHOULD address |
| 17 | R-IC-001 | Delegated trust boundary violation | 288 | 6: Inter-Agent Communication | ASI04 | HIGH -- Phase 2 architecture SHOULD address |
| 18 | R-CF-001 | Error propagation through agent chains | 288 | 9: Cascading Failures | ASI08 | HIGH -- Phase 2 architecture SHOULD address |
| 19 | R-PE-005 | MCP server grants elevated filesystem access | 288 | 2: Privilege Escalation | ASI03 | HIGH -- Phase 2 architecture SHOULD address |
| 20 | R-PI-006 | Injection via structured data fields (YAML/JSON/handoff) | 280 | 1: Prompt Injection | ASI01 | HIGH -- Phase 2 architecture SHOULD address |

---

## Risk Heat Map (L2)

```
                    Low Occurrence (1-3)        Medium Occurrence (4-6)        High Occurrence (7-10)
                  +---------------------------+---------------------------+---------------------------+
                  |                           |                           |                           |
  High Severity  |  R-PE-002 (54)            |  R-PE-003 (250)           |  R-PI-002 (504) *CRIT*    |
  (8-10)         |  R-SC-006 (90)            |  R-PE-004 (280)           |  R-PI-003 (392) *CRIT*    |
                  |  R-SC-005 (180)           |  R-PE-005 (288)           |  R-PI-005 (384)           |
                  |  R-IT-002 (168)           |  R-PE-006 (270)           |  R-AM-001 (378)           |
                  |  R-IA-003 (162)           |  R-SC-001 (480) *CRIT*    |  R-GB-001 (432) *CRIT*    |
                  |  R-IC-006 (210)           |  R-SC-002 (378)           |  R-CF-003 (315)           |
                  |  R-GB-003 (60)            |  R-SC-004 (320)           |  R-CF-002 (294)           |
                  |  R-SC-003 (160)           |  R-DE-001 (270)           |  R-CF-005 (405) *CRIT*    |
                  |  R-IT-005 (150)           |  R-DE-003 (250)           |                           |
                  |                           |  R-AM-003 (320)           |                           |
                  |                           |  R-AM-004 (252)           |                           |
                  |                           |  R-IT-001 (280)           |                           |
                  |                           |  R-IT-003 (225)           |                           |
                  |                           |  R-IT-006 (300)           |                           |
                  |                           |  R-GB-002 (240)           |                           |
                  |                           |  R-GB-004 (200)           |                           |
                  |                           |  R-GB-005 (240)           |                           |
                  |                           |  R-IC-002 (280)           |                           |
                  |                           |  R-IA-004 (108)           |                           |
                  +---------------------------+---------------------------+---------------------------+
                  |                           |                           |                           |
  Medium          |  R-CF-006 (90)            |  R-DE-005 (245)           |  R-IC-003 (294)           |
  Severity        |  R-IC-005 (144)           |  R-CF-004 (120)           |  R-DE-002 (294)           |
  (5-7)          |                           |  R-IA-001 (224)           |  R-PI-004 (245)           |
                  |                           |  R-IA-002 (224)           |  R-DE-004 (294)           |
                  |                           |  R-AM-005 (224)           |  R-CF-001 (288)           |
                  |                           |  R-AM-006 (150)           |                           |
                  |                           |  R-IA-005 (210)           |                           |
                  |                           |  R-IA-006 (245)           |                           |
                  |                           |  R-GB-006 (216)           |                           |
                  +---------------------------+---------------------------+---------------------------+
                  |                           |                           |                           |
  Low Severity   |                           |                           |                           |
  (1-4)          |                           |  R-PI-001 (192)           |                           |
                  |                           |  R-PE-001 (108)           |                           |
                  |                           |  R-IT-004 (168)           |                           |
                  |                           |  R-AM-002 (120)           |                           |
                  +---------------------------+---------------------------+---------------------------+
```

**Key:** `*CRIT*` = RPN >= 400 (Critical priority, immediate action required)

**Heat map interpretation:** The upper-right quadrant (High Severity + High Occurrence) contains the 5 most dangerous risks. The concentration of risks in the Medium Occurrence column reflects that most agentic attack techniques are well-documented but require specific conditions to exploit against Jerry's defense-in-depth architecture.

---

## Jerry-Specific Vulnerabilities

These vulnerabilities are specific to Jerry's architecture and do not apply to generic agentic frameworks.

### V-001: L2 Re-Injection Gap (Tier B Rules)

**Description:** Jerry's 5-layer enforcement architecture classifies 20 HARD rules as Tier A (L2-protected, immune to context rot) and 5 HARD rules as Tier B (relying on compensating controls). The Tier B rules (H-04, H-16, H-17, H-18, H-32) are vulnerable to context rot degradation.

**Impact:** At high context fill (>80%), Tier B rules may be silently ignored. H-16 (steelman before critique) and H-17 (quality scoring) degradation could result in lower-quality adversarial reviews that miss security issues. H-18 (constitutional compliance check) degradation is particularly dangerous as it removes a key governance verification step.

**Current mitigation:** Compensating controls (SessionStart hook for H-04, skill enforcement for H-16/H-17/H-18, CI workflow for H-32).

**Recommended:** Promote H-18 (constitutional compliance) to Tier A. The remaining Tier B rules have adequate compensating controls. Monitor context fill via AE-006 and trigger mandatory checkpoint at CRITICAL tier.

### V-002: MCP Tool Output Channel (Instruction/Data Confusion)

**Description:** Jerry mandates Context7 (MCP-001) and Memory-Keeper (MCP-002) usage through HARD rules. MCP tool outputs are returned directly into the LLM context without content-source tagging or sanitization. The LLM cannot distinguish between trusted instructions and untrusted data returned from MCP tools.

**Impact:** An attacker who controls or poisons MCP tool data (Context7 documentation, Memory-Keeper stored context, or third-party MCP servers) can inject instructions that the LLM processes as trusted guidance. This is the architectural root cause of R-PI-002 (RPN 504).

**Current mitigation:** L2 re-injection of critical rules provides partial resilience, but does not prevent the LLM from acting on injected instructions in tool results.

**Recommended:** Implement Tool-Output Firewall at L4: classify and sanitize MCP tool results before LLM processing. Tag content with source provenance. Implement input/output firewalls per Google DeepMind's defense architecture.

### V-003: Bash Tool Unrestricted Execution

**Description:** The Bash tool in Jerry's tool tier system (T2+) provides unrestricted shell command execution. There is no command allowlisting, blocklisting, or argument sanitization. Any agent with T2+ access can execute arbitrary system commands including network operations, file system modifications outside project scope, and environment variable inspection.

**Impact:** This creates multiple attack paths: credential harvesting (R-PE-006), data exfiltration (R-DE-006), SSRF (R-IT-003), command injection (R-IT-006), and privilege escalation (R-PE-003). The Bash tool is the single most powerful attack surface in Jerry's architecture.

**Current mitigation:** Tool tier system restricts Bash to T2+ agents. No per-command restrictions.

**Recommended:** Implement Bash command classification and restriction (L3): maintain per-tier command allowlists; block network commands (curl, wget, ssh, nc) by default; require user approval for destructive commands; sanitize dynamically constructed command arguments.

### V-004: Handoff Protocol Lacks Cryptographic Integrity

**Description:** Jerry's handoff protocol (v2) uses schema-validated structured data with required fields (`from_agent`, `to_agent`, `task`, `success_criteria`, `artifacts`, `key_findings`, `blockers`, `confidence`, `criticality`). However, handoff data is passed as plain text/YAML with no cryptographic integrity verification.

**Impact:** An attacker who can inject into the orchestrator's context can craft forged handoffs that downstream agents accept as legitimate. The `from_agent` field can be spoofed. Artifact paths can be redirected. Key findings can be fabricated. This enables R-IC-001 (trust boundary violations), R-IC-002 (handoff poisoning), and R-IA-001 (agent identity spoofing).

**Current mitigation:** Schema validation (HD-M-001) verifies structure but not authenticity. Handoff content is not signed or hashed.

**Recommended:** Add handoff integrity: hash artifacts at send, verify at receive. Sign handoffs with agent identity. Implement handoff chain provenance tracking. This aligns with Google DeepMind's Delegation Capability Tokens concept using cryptographic caveats.

### V-005: Quality Gate LLM-as-Judge Adversarial Vulnerability

**Description:** Jerry's quality gate uses S-014 (LLM-as-Judge) with a 6-dimension rubric and >= 0.92 weighted composite threshold. The scorer (adv-scorer) is itself an LLM agent whose scoring can be influenced by crafted deliverable content.

**Impact:** An adversarially crafted deliverable can manipulate the scorer into inflating scores. This bypasses H-13 (quality threshold), allowing substandard deliverables to pass through the governance system. Particularly dangerous for security deliverables where false quality assurance could mask vulnerabilities.

**Current mitigation:** Anti-leniency statement in scorer guardrails. Multiple iterations (H-14, minimum 3). Fresh context review for C3+ (FC-M-001).

**Recommended:** Add score calibration benchmarks: known-quality deliverables scored periodically to detect drift. Implement multi-scorer consensus: require 2+ independent scoring passes that must converge. Add deterministic quality checks (H-34 schema validation) before LLM scoring.

### V-006: File System as Infinite Memory (Persistence Threat)

**Description:** Jerry's core design principle -- "Filesystem as infinite memory. Persist state to files; load selectively" -- means the file system contains the complete accumulated knowledge, decisions, and state of all sessions. This creates a high-value target.

**Impact:** Compromise of the file system exposes: all constitutional rules and enforcement details, all agent definitions with guardrails, all project work including research findings and architecture decisions, all HARD rules and their enforcement gaps (from this risk register), and all quality gate thresholds. An attacker with file system access has complete knowledge of Jerry's defense architecture.

**Current mitigation:** OS-level file permissions. Git version control (audit trail). Local-first architecture (no network exposure by default).

**Recommended:** Implement sensitive file classification: mark files containing security-critical information; encrypt at rest where feasible; restrict Read tool access to classified files; implement audit logging for all file access operations.

---

## Recommended Risk Mitigation Priorities

The following 10 actions are recommended for Phase 2 architecture design, ordered by aggregate RPN impact.

| Priority | Action | Addresses Risk IDs | Aggregate RPN | Implementation Layer |
|----------|--------|-------------------|---------------|---------------------|
| 1 | **Tool-Output Firewall (L4):** Sanitize and classify all MCP tool results and file Read outputs before LLM processing. Implement content-source tagging to distinguish instruction channels from data channels. | R-PI-002, R-PI-003, R-SC-004, R-AM-003 | 1,636 | L4 (post-tool inspection) |
| 2 | **MCP Supply Chain Verification:** Implement cryptographic hash pinning for MCP server packages. Maintain allowlisted server registry. Add runtime integrity monitoring. L5 CI gate for MCP configuration validation. | R-SC-001, R-PE-005, R-IT-001, R-IT-005 | 1,198 | L3 (pre-tool), L5 (CI) |
| 3 | **Bash Tool Hardening (L3):** Implement command classification, allowlisting, and argument sanitization per agent tier. Block network commands by default. Require user approval for destructive operations. | R-PE-003, R-PE-006, R-DE-006, R-IT-003, R-IT-006 | 1,285 | L3 (pre-tool) |
| 4 | **Handoff Integrity Protocol:** Add cryptographic hashing of handoff artifacts, agent identity signing, data classification, and handoff chain provenance. Enforce data minimization at L3. | R-IC-001, R-IC-002, R-IC-003, R-DE-004, R-IA-001 | 1,380 | L3 (pre-tool), L4 (post-tool) |
| 5 | **Context Rot Security Hardening:** Promote H-18 to Tier A. Implement automatic session partitioning at CRITICAL context fill for security-critical work. Add L4 security rule compliance verification at WARNING+ tiers. | R-GB-001, R-CF-003, R-PI-005 | 1,131 | L2 (per-prompt), L4 (post-tool) |
| 6 | **Runtime Tool Access Matrix (L3):** Enforce agent-to-tool-tier mapping at runtime. Verify every tool call against agent's declared `allowed_tools`. Block unauthorized tool invocations deterministically. | R-PE-001, R-PE-004, R-AM-002 | 508 | L3 (pre-tool) |
| 7 | **Secret Detection and Data Loss Prevention (L4):** Implement regex-based credential scanning on all agent output. Add file access control for sensitive file patterns. Block output containing detected secrets. | R-DE-001, R-DE-003, R-DE-005, R-PE-006 | 1,025 | L4 (post-tool) |
| 8 | **Goal Consistency and Behavioral Monitoring (L4):** Track agent actions against declared task/purpose. Detect behavioral deviation and goal drift. Implement action classification (safe/destructive). | R-AM-001, R-AM-004, R-AM-005, R-GB-004 | 1,054 | L4 (post-tool) |
| 9 | **Adversarial Testing Program:** Implement red team exercises against Jerry's security controls. Track detection rates per layer. Run canary attacks for continuous validation. Calibrate quality gate scoring. | R-CF-005, R-GB-002, R-CF-004 | 765 | L5 (post-hoc verification) |
| 10 | **Agent Identity and Authentication:** Implement cryptographic agent identity tokens. Add delegation tokens for handoff chains. Validate agent identity at trust boundaries. Add session-scoped credential management. | R-IA-001, R-IA-002, R-IA-006 | 693 | L3 (pre-tool), L4 (post-tool) |

**Estimated coverage:** These 10 actions address 50 of the 60 identified failure modes (83% coverage). The remaining 10 risks have RPN < 200 and are addressed by existing controls or lower-priority enhancements.

---

## Citations

| # | Source | Authority | Relevance |
|---|--------|-----------|-----------|
| 1 | [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) | Industry Standard | ASI01-ASI10 threat classification; primary framework for agentic threat taxonomy |
| 2 | [OWASP Top 10 for LLM Applications 2025](https://genai.owasp.org/llm-top-10/) | Industry Standard | LLM01-LLM10 threat classification; prompt injection, supply chain, excessive agency |
| 3 | [Anthropic GTG-1002 Incident Disclosure](https://www.anthropic.com/news/disrupting-AI-espionage) | Industry Leader | Real-world AI-orchestrated espionage; validates model guardrails insufficiency |
| 4 | [Securiti AI -- Anthropic Exploit Analysis](https://securiti.ai/blog/anthropic-exploit-era-of-ai-agent-attacks/) | Industry Expert | Analysis of GTG-1002; "model-level guardrails function as architectural suggestions" |
| 5 | [Cisco State of AI Security 2026](https://blogs.cisco.com/ai/cisco-state-of-ai-security-2026-report) | Industry Expert | MCP attack surface analysis; 83% agentic deployment, 29% readiness; malicious MCP BCC attack |
| 6 | [Meta -- Practical AI Agent Security (Rule of Two)](https://ai.meta.com/blog/practical-ai-agent-security/) | Industry Leader | Design constraint: max 2 of (untrusted input, sensitive data, external state change) |
| 7 | [Google DeepMind -- Defending Gemini Against IPI](https://arxiv.org/html/2505.14534v1) | Industry Leader / Academic | 5-layer defense architecture; "static defenses offer false sense of security" |
| 8 | [Google DeepMind -- Intelligent AI Delegation](https://arxiv.org/abs/2602.11865) | Industry Leader / Academic | Delegation Capability Tokens; cryptographic caveats for agent chains |
| 9 | [The Attacker Moves Second (Joint Study)](https://simonwillison.net/2025/Nov/2/new-prompt-injection-papers/) | Industry Leader / Academic | 12 defenses bypassed >90% success; defense-in-depth only viable strategy |
| 10 | [Microsoft Agent 365 Security](https://www.microsoft.com/en-us/security/blog/2025/11/18/ambient-and-autonomous-security-for-the-agentic-era/) | Industry Leader | Agent ID, control/data plane separation, registry-based governance |
| 11 | [Microsoft Agent Factory](https://azure.microsoft.com/en-us/blog/agent-factory-creating-a-blueprint-for-safe-and-secure-ai-agents/) | Industry Leader | 5 qualities: unique identity, data protection, built-in controls, threat evaluation, oversight |
| 12 | [Microsoft SDL for AI](https://www.microsoft.com/en-us/security/blog/2026/02/03/microsoft-sdl-evolving-security-practices-for-an-ai-powered-world/) | Industry Leader | AI threat modeling, observability, memory protections, identity/RBAC |
| 13 | [Anthropic Claude Code Sandboxing](https://www.anthropic.com/engineering/claude-code-sandboxing) | Industry Leader | bubblewrap/seatbelt isolation, network filtering, permission model |
| 14 | [OWASP AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet) | Industry Standard | SecureAgentMemory, SecureLLMPipeline, PromptInjectionFilter patterns |
| 15 | [OWASP Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet) | Industry Standard | Input validation layers, HITL, sanitization, structured prompts |
| 16 | [MITRE ATLAS](https://atlas.mitre.org/) | Standards Body | 15 tactics, 66 techniques; 14 new agent-specific techniques (2025) |
| 17 | [ICLR 2025 -- Agent Security Bench](https://proceedings.iclr.cc/paper_files/paper/2025/file/5750f91d8fb9d5c02bd8ad2c3b44456b-Paper-Conference.pdf) | Academic | Benchmark for agentic AI security evaluation |
| 18 | [Prompt Injection on Agentic Coding Assistants (arXiv)](https://arxiv.org/html/2601.17548v1) | Academic | Systematic analysis of prompt injection in skills, tools, protocol ecosystems |
| 19 | [MCP Security Vulnerabilities (Practical DevSecOps)](https://www.practical-devsecops.com/mcp-security-vulnerabilities/) | Industry Expert | MCP-specific prompt injection, tool poisoning, CVE analysis |
| 20 | [Docker -- MCP Security Issues](https://www.docker.com/blog/mcp-security-issues-threatening-ai-infrastructure/) | Industry Expert | MCP infrastructure security; supply chain risks |
| 21 | [Astrix -- State of MCP Server Security 2025](https://astrix.security/learn/blog/state-of-mcp-server-security-2025/) | Industry Expert | 53% insecure static secrets; 43% command injection; 8.5% OAuth adoption |
| 22 | [OWASP MCP Top 10](https://owasp.org/www-project-mcp-top-10/) | Industry Standard | MCP-specific vulnerability classification |
| 23 | [Cisco Integrated AI Security Framework](https://arxiv.org/abs/2512.12921) | Industry Expert / Academic | Lifecycle-aware taxonomy; runtime manipulation; orchestration abuse |
| 24 | [AWS Agentic AI Security Scoping Matrix](https://aws.amazon.com/blogs/security/the-agentic-ai-security-scoping-matrix-a-framework-for-securing-autonomous-ai-systems/) | Industry Leader | Framework for scoping agentic AI security controls |
| 25 | [Palo Alto Networks -- OWASP Agentic Collaboration](https://www.paloaltonetworks.com/blog/cloud-security/owasp-agentic-ai-security/) | Industry Leader | Enterprise agentic security assessment methodology |
| 26 | [NIST IR 8596 -- CSF Profile for AI (Draft)](https://csrc.nist.gov/pubs/ir/8596/iprd) | US Government | AI focus areas overlaid on CSF 2.0; agent hijacking, backdoor attacks |
| 27 | [Your AI, My Shell -- Agentic Coding Editor Attacks](https://arxiv.org/html/2509.22040v1) | Academic | Zero-click attacks; 93.3% Initial Access success rate; IDE agent exploitation |
| 28 | [Anthropic Content Source Management](https://www.technologyreview.com/2026/02/04/1131014/from-guardrails-to-governance-a-ceos-guide-for-securing-agentic-systems) | Industry Leader | Agents as non-human principals; validator between agent and real world |
| 29 | [Microsoft Cloud Adoption Framework for AI Agents](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ai-agents/governance-security-across-organization) | Industry Leader | Data governance, agent observability, agent security layers |
| 30 | [MITRE D3FEND](https://d3fend.mitre.org/) | Standards Body | 267 defensive techniques mapped to ATT&CK; countermeasure reference |

---

*Self-review (S-010) completed. Verified: 60 failure modes across 10 categories. All failure modes scored with S/O/D justification. Top 20 ranked by RPN. Jerry-specific mitigations mapped. OWASP ASI01-ASI10 cross-referenced. 30 citations provided. Heat map and mitigation priorities included.*

*Risk register version: 1.0.0 | Agent: nse-explorer-001 | Pipeline: NSE | Phase: 1*
