# ADR-PROJ010-002: Skill Routing & Invocation Architecture

> **ADR ID:** ADR-PROJ010-002
> **Version:** 1.0.0
> **Date:** 2026-02-22
> **Author:** ps-architect
> **Status:** PROPOSED
> **Deciders:** User (P-020 authority), ps-architect (recommendation)
> **Quality Target:** >= 0.95
> **Parent Feature:** FEAT-011 (Skill Routing & Invocation Architecture)
> **Parent Epic:** EPIC-002 (Architecture & Design)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Status](#status) | Current decision lifecycle stage and downstream dependency gating |
| [Context](#context) | Why this decision is needed, constraints, and research foundation |
| [Decision](#decision) | Full routing architecture: SKILL.md structure, trigger maps, routing table, workflow patterns, safety alignment, Jerry integration, circuit breakers, red-lead mandate |
| [Options Considered](#options-considered) | Three routing architecture approaches evaluated |
| [Consequences](#consequences) | Positive, negative, and neutral outcomes |
| [Evidence Base](#evidence-base) | Summary of findings from Phase 1 research artifacts |
| [Compliance](#compliance) | Jerry framework compliance assessment |
| [Related Decisions](#related-decisions) | Upstream and downstream decision linkages |
| [Open Questions](#open-questions) | Genuine ambiguities requiring Phase 2 resolution |
| [References](#references) | Source citations with artifact traceability |

---

## Status

**PROPOSED** -- This ADR awaits adversarial review and user ratification.

**Downstream Dependency Gating:** FEAT-020 (/eng-team skill implementation) and FEAT-030 (/red-team skill implementation) are BLOCKED until this ADR is ACCEPTED. Both build-phase features depend on the routing architecture defined here for SKILL.md structure, keyword triggers, agent selection logic, and workflow orchestration patterns.

**Required Review Process:**
1. C4 /adversary review with all 10 selected strategies (quality target >= 0.95)
2. User ratification per P-020 (User Authority)

---

## Context

### Why This Decision Is Needed

PROJ-010 introduces two new Jerry skills -- /eng-team (10 agents) and /red-team (11 agents) -- that are architecturally distinct from all existing Jerry skills. Existing skills (/problem-solving, /adversary, /orchestration) use 3-7 agents with relatively straightforward routing. The cybersecurity skills introduce three novel routing challenges that no existing Jerry skill addresses:

1. **Scale:** 21 agents across 2 skills with overlapping security terminology require disambiguation logic that goes beyond simple keyword matching. A request mentioning "vulnerability" could route to eng-security (manual review), eng-devsecops (automated scanning), red-vuln (offensive vulnerability analysis), or red-exploit (exploitation), depending on context.

2. **Non-linear workflow:** /red-team explicitly requires non-linear agent invocation (A-004 R-ROSTER-014), where any agent is invocable after red-lead establishes scope, and agents cycle back to earlier phases as engagements progress. This contrasts with /eng-team's sequential 8-step phase-gate model and with Jerry's existing linear workflow patterns.

3. **Cross-skill integration:** Purple team scenarios require coordinated routing across both skills simultaneously -- red-recon feeding eng-architect, red-exploit testing eng-backend's code -- creating a routing pattern that no single Jerry skill currently handles.

Without a formalized routing architecture, FEAT-020 and FEAT-030 would independently design incompatible routing mechanisms, purple team integration would be ad hoc, and the 21-agent roster's value would be undermined by routing failures that send requests to the wrong agent.

### Research Foundation

Phase 1 research across 6 streams and 20 artifacts provides the definitive specification input for this ADR. The key inputs are:

| Input | Source | Description |
|-------|--------|-------------|
| /eng-team 8-step workflow sequence | F-001 | Sequential phase-gate: eng-architect through eng-incident |
| /red-team non-linear kill chain | A-004 R-ROSTER-014 | Agents invocable in any order after red-lead establishes scope |
| Keyword trigger maps (21 agents) | S-002 Skill Routing Specification Input | Full trigger-to-agent mapping for both skills |
| Routing decision table (12 scenarios) | S-002 Skill Routing Specification Input | Context-dependent routing including purple team and safety alignment |
| 5 multi-agent workflow patterns | S-002 Skill Routing Specification Input | Sequential, non-linear, parallel, purple team, conditional |
| 4 cross-skill integration points | A-004 R-ROSTER-013 | Threat-Informed Architecture, Attack Surface Validation, Secure Code vs. Exploitation, Incident Response Validation |
| Circuit breaker mandate | F-002 R-AUTH-006 | Scope revalidation at every phase transition |
| Safety alignment compatibility | D-002 Finding 5, Ethical Boundaries section | Methodology-first framing avoids safety filter conflicts |
| Agent capability boundaries | S-002 Agent Architecture Specification Input | Non-overlapping capability domains for all 21 agents |

### Constraints

| Constraint | Source | Impact on Routing |
|------------|--------|-------------------|
| H-25, H-26 | skill-standards | SKILL.md structure, naming, registration requirements |
| H-22 | mandatory-skill-usage | Proactive skill invocation; /eng-team and /red-team must register trigger keywords |
| AD-001 | Methodology-First Design | All routing produces methodology guidance, not execution automation |
| AD-002 | 21-Agent Roster | Routing must address 10 /eng-team + 11 /red-team agents |
| AD-004 | Three-Layer Authorization | /red-team routing must integrate with scope enforcement infrastructure |
| P-003 | No Recursive Subagents | Skill invokes agents as workers; no agent-spawns-agent chains |
| R-ROSTER-014 | Non-Linear Kill Chain | /red-team workflow must support any-order invocation after red-lead |

---

## Decision

### 1. SKILL.md Structure

Both /eng-team and /red-team follow Jerry's skill standard (H-25, H-26). Each SKILL.md file provides the routing entry point for its skill.

#### /eng-team SKILL.md Location and Structure

**Location:** `skills/eng-team/SKILL.md` (H-25: exactly `SKILL.md`, case-sensitive)
**Folder:** `skills/eng-team/` (H-26: kebab-case, matches `name` field)

```yaml
name: eng-team
description: >
  Secure engineering team skill providing methodology guidance for building
  security-hardened software. Invoked when users request system design,
  implementation, code review, testing, CI/CD security, or incident response
  with security considerations. Routes to 10 specialized agents covering
  architecture through post-deployment. Integrates NIST SSDF governance,
  Microsoft SDL phases, OWASP ASVS verification, SLSA supply chain integrity,
  and DevSecOps automation patterns.
version: 1.0.0
agents:
  - eng-architect
  - eng-lead
  - eng-backend
  - eng-frontend
  - eng-infra
  - eng-qa
  - eng-security
  - eng-reviewer
  - eng-devsecops
  - eng-incident
```

**Description compliance (H-26):** WHAT: secure engineering methodology guidance across 10 agents. WHEN: system design, implementation, code review, testing, CI/CD, incident response with security context. Triggers listed. Under 1024 characters. No XML.

**Agent definitions location (H-26):** `skills/eng-team/agents/{agent-name}.md` using full repo-relative paths.

#### /red-team SKILL.md Location and Structure

**Location:** `skills/red-team/SKILL.md`
**Folder:** `skills/red-team/`

```yaml
name: red-team
description: >
  Offensive security team skill providing methodology guidance for penetration
  testing and red team engagements. Invoked when users request penetration
  testing, reconnaissance, vulnerability analysis, exploitation methodology,
  social engineering, C2 infrastructure, or engagement reporting. Routes to
  11 specialized agents covering the full MITRE ATT&CK kill chain.
  All engagements require red-lead scope authorization before any other agent.
  Follows PTES, OSSTMM, and ATT&CK methodology frameworks.
version: 1.0.0
agents:
  - red-lead
  - red-recon
  - red-vuln
  - red-exploit
  - red-privesc
  - red-lateral
  - red-persist
  - red-exfil
  - red-reporter
  - red-infra
  - red-social
```

#### Registration Requirements (H-26)

Both skills MUST be registered in:
- `CLAUDE.md` Quick Reference skills table
- `AGENTS.md` agent registry
- `mandatory-skill-usage.md` trigger map (since both skills require proactive invocation per H-22)

### 2. Keyword Trigger Maps

Keyword triggers determine which skill and agent handles a user request. Triggers are registered in `mandatory-skill-usage.md` per H-22 and resolved by the routing logic defined in Section 3.

#### /eng-team Keyword Triggers (10 agents)

| Trigger Keywords | Agent | Routing Context |
|------------------|-------|-----------------|
| design, architecture, ADR, threat model, system design, STRIDE, DREAD, PASTA, NIST CSF | eng-architect | Architecture and threat modeling tasks |
| implementation plan, code standards, PR review, dependencies, tech lead, maturity assessment, SAMM | eng-lead | Planning and standards enforcement |
| backend, server-side, API, authentication, authorization, database, input validation | eng-backend | Server-side implementation |
| frontend, client-side, XSS, CSP, CORS, output encoding, DOM | eng-frontend | Client-side implementation |
| infrastructure, IaC, container, Kubernetes, Docker, network, secrets, SBOM, supply chain, SLSA | eng-infra | Infrastructure and supply chain security |
| test, QA, fuzzing, coverage, boundary testing, regression, security testing | eng-qa | Testing and quality assurance |
| code review, secure review, CWE, vulnerability assessment, security requirements | eng-security | Manual secure code review |
| final review, review gate, standards compliance, deliverable review | eng-reviewer | Final gate review |
| CI/CD, pipeline, SAST, DAST, scanning, automated security, container scan, dependency scan | eng-devsecops | Automated security tooling |
| incident, response, post-deployment, vulnerability lifecycle, monitoring, breach, runbook | eng-incident | Incident response and post-deployment |

**Source:** S-002 Skill Routing Specification Input, /eng-team Keyword Triggers table. Keywords derive from agent capability boundaries established in A-004 and standard mappings in B-003 and F-001.

#### /red-team Keyword Triggers (11 agents)

| Trigger Keywords | Agent | Routing Context |
|------------------|-------|-----------------|
| scope, rules of engagement, authorization, methodology, engagement, coordination, RoE | red-lead | Engagement management (MANDATORY FIRST) |
| reconnaissance, OSINT, enumeration, discovery, fingerprint, attack surface, DNS | red-recon | Reconnaissance phase |
| vulnerability, CVE, scan, exploit availability, attack path, risk score | red-vuln | Vulnerability analysis |
| exploit, payload, proof of concept, vulnerability chain, initial access, execution | red-exploit | Exploitation |
| privilege escalation, privesc, credential, token, misconfig, local admin, domain admin | red-privesc | Privilege escalation |
| lateral movement, pivot, tunnel, living off the land, internal network | red-lateral | Lateral movement |
| persistence, backdoor, scheduled task, rootkit, detection evasion | red-persist | Persistence |
| exfiltration, data theft, covert channel, DLP bypass, collection | red-exfil | Data exfiltration |
| report, finding, remediation, executive summary, documentation, engagement report | red-reporter | Reporting |
| C2, command and control, payload build, redirector, infrastructure, tool development | red-infra | Infrastructure and tooling |
| social engineering, phishing, pretext, human vector, spear phishing, vishing | red-social | Social engineering |

**Source:** S-002 Skill Routing Specification Input, /red-team Keyword Triggers table. Keywords derive from MITRE ATT&CK tactic-to-agent mapping validated in A-004.

#### Keyword Collision Resolution

Security terminology frequently overlaps between skills. The routing logic applies the following disambiguation rules:

| Ambiguous Keyword | /eng-team Resolution | /red-team Resolution | Disambiguation Signal |
|--------------------|---------------------|----------------------|----------------------|
| vulnerability | eng-security or eng-devsecops | red-vuln | Defensive context (review, scan, fix) vs. offensive context (exploit, attack path) |
| scanning | eng-devsecops | red-recon or red-vuln | Build pipeline context vs. target enumeration context |
| authentication | eng-backend | red-privesc | Implementation context vs. bypass/exploitation context |
| infrastructure | eng-infra | red-infra | Build/deploy context vs. C2/engagement context |
| report | eng-reviewer | red-reporter | Standards compliance context vs. engagement findings context |

**Resolution principle:** When keywords are ambiguous, routing examines the surrounding context for offensive vs. defensive intent signals. If intent remains ambiguous after context analysis, the router defaults to the defensive (/eng-team) interpretation and confirms with the user per H-31 (clarify when ambiguous).

### 3. Routing Decision Table

The routing decision table defines 12 canonical scenarios covering single-skill, cross-skill, and edge-case routing. This is the authoritative reference for agent selection logic.

| # | Input Characteristics | Skill | Agent Selection | Routing Logic | Evidence |
|---|----------------------|-------|-----------------|---------------|----------|
| 1 | System design request with security consideration | /eng-team | eng-architect | Architecture + security trigger keywords; defensive context | S-002 row 1 |
| 2 | Request to implement secure backend feature | /eng-team | eng-lead then eng-backend | eng-lead plans, eng-backend implements; Pattern 1 sequential | S-002 row 2 |
| 3 | Request to scan code for vulnerabilities (automated) | /eng-team | eng-devsecops | Automated scanning triggers; pipeline/CI/CD context | S-002 row 3 |
| 4 | Request to review code for security flaws (manual) | /eng-team | eng-security | Manual review triggers; code review context | S-002 row 4 |
| 5 | Request to review deliverable for standards compliance | /eng-team | eng-reviewer | Final gate triggers; standards compliance context | S-002 row 5 |
| 6 | Request for penetration test of target | /red-team | red-lead (MANDATORY FIRST) | All engagements start with scope definition; red-lead always first | S-002 row 6; Section 8 of this ADR |
| 7 | Request for target reconnaissance | /red-team | red-recon (after red-lead scope) | Recon triggers; requires active scope from red-lead | S-002 row 7 |
| 8 | Request to exploit specific vulnerability | /red-team | red-exploit (after red-lead scope) | Exploit triggers; requires active scope and authorization verification | S-002 row 8 |
| 9 | Request for engagement report | /red-team | red-reporter | Reporting triggers; no scope prerequisite for report generation from existing findings | S-002 row 9 |
| 10 | Request for C2 setup or payload building | /red-team | red-infra (after red-lead scope) | Infrastructure triggers; requires active scope | S-002 row 10 |
| 11 | Request involving both building and attacking (purple team) | Both | Cross-skill purple team routing; Pattern 4 | Both skill triggers present; activates cross-skill integration points | S-002 row 11; Section 4.4 |
| 12 | Request about threat modeling informed by adversary TTPs | Both | red-recon then eng-architect | Cross-skill integration point 1: Threat-Informed Architecture | S-002 row 12; A-004 R-ROSTER-013 |
| 13 | Safety alignment conflict (direct exploit code request) | /red-team | Reframe through methodology | Frame as PTES/OWASP methodology guidance per D-002; Section 5 of this ADR | S-002 row 13; D-002 |

**Routing precedence rules:**
1. If /red-team triggers are present and no active scope exists, route to red-lead first (Section 8).
2. If both /eng-team and /red-team triggers are present, evaluate for purple team routing (Scenario 11/12).
3. If only one skill's triggers match, route to that skill's most specific agent.
4. If keyword collision exists, apply disambiguation rules from Section 2.
5. If intent remains ambiguous after all rules, default to /eng-team and confirm with user per H-31.

### 4. Multi-Agent Workflow Patterns

Five workflow patterns govern how agents execute within and across skills. These patterns are compositions -- a single engagement may use multiple patterns at different stages.

#### Pattern 1: Sequential Phase-Gate (/eng-team Default)

The /eng-team follows an 8-step sequential workflow derived from the Microsoft SDL phase-gate model (F-001) and NIST SSDF practice groups.

```
Trigger: "Build a secure API"
  Step 1: eng-architect   (design + threat model)         [MS SDL Requirements/Design]
  Step 2: eng-lead        (implementation plan)            [MS SDL Requirements]
  Step 3: eng-backend     (implement)                      [MS SDL Implementation]
         eng-frontend    (implement, if applicable)       [MS SDL Implementation]
         eng-infra       (infrastructure, if applicable)  [MS SDL Implementation]
  Step 4: eng-devsecops   (automated scans)                [DevSecOps Pipeline]
  Step 5: eng-qa          (tests)                          [MS SDL Verification]
  Step 6: eng-security    (manual review)                  [MS SDL Verification]
  Step 7: eng-reviewer    (final gate + /adversary for C2+)[MS SDL Release]
  Step 8: eng-incident    (IR plan + runbooks)             [MS SDL Release + SSDF RV]
```

**Handoff mechanism:** Each phase produces a defined artifact (design document, implementation plan, code, scan results, test results, review report). Phase transition requires prior phase artifact completion. eng-reviewer is the mandatory final gate with /adversary integration for C2+ deliverables per R-013.

**Partial invocation:** Not all 8 steps are required for every request. If a user requests only "review this code for security flaws," routing skips directly to eng-security (Scenario 4). The sequential model applies when a full SDLC engagement is requested.

**eng-incident activation:** eng-incident operates post-deployment and is not gated by eng-reviewer. It activates when incident response, vulnerability lifecycle, or monitoring triggers are detected, independent of the build workflow.

**Source:** F-001 Workflow Sequence with SDLC Model Integration; S-002 Pattern 1.

#### Pattern 2: Non-Linear with Phase Cycling (/red-team)

The /red-team workflow is explicitly non-linear per A-004 R-ROSTER-014. Real penetration testing engagements are iterative -- exploitation discovers new reconnaissance targets, privilege escalation reveals new vulnerabilities, and lateral movement opens new attack surfaces. The kill chain organizes capability domains, not workflow sequence.

```
Trigger: "Penetration test against target X"
  Step 1: red-lead     (scope + authorization)  [MANDATORY FIRST -- Section 8]
  Then, any order:
    red-recon    (attack surface mapping)
    red-vuln     (vulnerability identification)
    red-exploit  (exploitation)
       -> discovers new attack surface -> cycles back to red-recon
    red-privesc  (escalation)
       -> discovers new vulnerabilities -> cycles back to red-vuln
    red-lateral  (network movement)
    red-persist  (persistence, if authorized in RoE)
    red-exfil    (data exfiltration, if authorized in RoE)
    red-infra    (C2 infrastructure, tool development)
    red-social   (social engineering, if authorized in RoE)
  Final: red-reporter  (documentation + remediation)  [MANDATORY for engagement close]
```

**Phase cycling:** Agents may cycle back to earlier phases. When red-exploit discovers a new attack surface, routing returns to red-recon for further enumeration. When red-privesc discovers new vulnerabilities on a compromised host, routing returns to red-vuln for analysis. This cycling is structurally supported, not an exception.

**Circuit breaker at every transition:** Before routing transitions between agents, the circuit breaker performs scope compliance verification (Section 7). This check occurs whether the transition moves forward through the kill chain, cycles back to an earlier phase, or moves laterally to a parallel capability.

**RoE-gated agents:** red-persist, red-exfil, and red-social are only invocable if explicitly authorized in the Rules of Engagement defined by red-lead. Routing checks the active scope document before allowing invocation of these agents.

**Source:** A-004 R-ROSTER-014; S-002 Pattern 2; F-002 R-AUTH-006.

#### Pattern 3: Parallel Execution (Within a Phase)

When multiple agents can operate independently on the same inputs, they execute in parallel to reduce engagement time.

```
Trigger: "Implement feature X" (after eng-architect and eng-lead phases complete)
  Parallel:
    eng-backend   (server-side implementation)
    eng-frontend  (client-side implementation)
    eng-infra     (infrastructure provisioning)
  Sequential after parallel:
    eng-devsecops (automated scans on all outputs)
    eng-qa        (tests across all components)
```

**Parallel eligibility criteria:** Agents execute in parallel when (a) their inputs are available from a completed prior phase, (b) their work does not depend on each other's output, and (c) they operate on distinct capability domains. In the /eng-team context, eng-backend, eng-frontend, and eng-infra satisfy all three criteria during the implementation phase.

**Parallel in /red-team:** Parallel execution also applies within /red-team when independent agents operate on distinct targets or attack vectors within the authorized scope. For example, red-recon performing network enumeration while red-social performs social reconnaissance, or red-exploit targeting one vulnerability while red-privesc escalates on a previously compromised host.

**Source:** S-002 Pattern 3.

#### Pattern 4: Purple Team Cross-Skill (Integration Testing)

Purple team scenarios activate the four cross-skill integration points defined in A-004 R-ROSTER-013. Both skills' agents operate on shared artifacts in an adversarial-collaborative dynamic.

```
Trigger: "Validate security of component Y"
  Phase A (parallel):
    eng-architect  (design review, threat model)
    red-recon      (attack surface mapping of eng-architect's design)
  Phase B:
    red-vuln       (vulnerability analysis of architecture decisions)
    red-exploit    (attempt exploitation of eng-backend's implementation)
  Phase C (parallel):
    eng-security   (review red team findings against code)
    eng-incident   (response exercise against red team post-exploitation)
  Phase D:
    red-reporter + eng-reviewer  (joint assessment, combined report)
```

**Four integration points:**

| # | Integration Point | Source Agent(s) | Target Agent(s) | Data Exchanged |
|---|-------------------|-----------------|-----------------|----------------|
| 1 | Threat-Informed Architecture | red-recon | eng-architect | Adversary TTPs, threat landscape, attack surface intelligence |
| 2 | Attack Surface Validation | red-recon, red-vuln | eng-infra, eng-devsecops | Validation results against hardened infrastructure |
| 3 | Secure Code vs. Exploitation | red-exploit, red-privesc | eng-security, eng-backend, eng-frontend | Exploitation results against reviewed and built code |
| 4 | Incident Response Validation | red-persist, red-lateral, red-exfil | eng-incident | Exercise results against response runbooks |

**Purple team routing activation:** Cross-skill routing activates when (a) the user explicitly requests purple team or combined assessment, (b) both offensive and defensive trigger keywords appear in the request, or (c) the engagement plan (established by red-lead or eng-architect) specifies cross-skill integration points. Activation of integration point 3 or 4 requires an active red-lead scope.

**Source:** A-004 R-ROSTER-013; S-002 Pattern 4; S-001 Cross-Skill Integration Points.

#### Pattern 5: Conditional Branching (Context-Dependent)

Routing adapts based on target characteristics, available information, and engagement scope. The same high-level request produces different agent selections depending on context.

```
Trigger: "Security assessment of application Z"
  Agent selection based on target characteristics:
    if web_application:       eng-frontend + eng-backend focus
    if infrastructure_target: eng-infra focus
    if API_service:           eng-backend + red-exploit (API testing)
    if source_code_available: eng-security + eng-devsecops
    if network_target:        red-recon + red-vuln + red-exploit
    if social_vector_authorized: red-social + red-recon
```

**Branching signals:** The router examines the request for context signals that determine branching: technology stack mentions (web, API, cloud, mobile), asset type (source code, running application, network infrastructure), available access level (source code access, network access, credential access), and engagement type (assessment, penetration test, red team exercise).

**Compound branching:** Multiple branches may activate simultaneously. A request for "security assessment of a web application with available source code" activates both the web_application branch (eng-frontend + eng-backend) and the source_code_available branch (eng-security + eng-devsecops), combining into a comprehensive assessment workflow.

**Source:** S-002 Pattern 5.

### 5. Safety Alignment Compatibility

Commercial LLM compliance with cyber attack assistance decreased from 52% to 28% (D-002 Finding 5, CyberSecEval 3 data). This improved safety alignment means that /red-team routing must account for the possibility that direct requests for offensive techniques will trigger safety filter refusals.

**Resolution through methodology-first design (AD-001):**

PROJ-010's methodology-first architecture (AD-001) inherently avoids most safety alignment conflicts because the skills produce what LLMs reliably allow -- methodology guidance, planning, analysis, and reporting -- rather than what they refuse -- direct exploit code generation, malware creation, and attack automation. This is not a workaround; it is the core design principle validated independently by three research streams (Convergence 1 in S-001: streams D, C, and A).

**Routing-level safety alignment handling:**

| Request Type | Routing Action | Rationale |
|-------------|----------------|-----------|
| Methodology guidance (e.g., "How do I test for SQL injection per OWASP?") | Route normally to appropriate agent | Within LLM allowed zone; professional security methodology |
| Direct exploit request (e.g., "Write me a SQL injection exploit for target X") | Reframe as methodology guidance | Route to red-exploit with PTES/OWASP framing: "Guide exploitation methodology for authorized SQL injection testing against in-scope target per PTES Technical Guidelines" |
| Explicit malware request | Decline with explanation | Beyond PROJ-010 scope; methodology-first design does not generate malware |
| Attack automation request | Route to red-infra for methodology | Guide C2 framework selection and configuration methodology, not direct payload generation |

**Implementation in agent prompts:** All /red-team agent definitions frame guidance within established professional methodology (PTES, OSSTMM, NIST SP 800-115, OWASP Testing Guide) using professional security terminology. Agent prompts include professional context framing (e.g., "You are a professional penetration testing methodology advisor operating under an authorized engagement scope") that signals legitimate security work to the underlying model's safety classifiers.

**What this does NOT do:** This approach does not attempt to bypass or circumvent safety alignment. /red-team agents never generate exploit code directly; they guide practitioners to use established exploitation frameworks (Metasploit, Burp Suite, Nuclei) with methodology-driven approaches. The approach works because PROJ-010's design aligns with what models allow (methodology guidance) rather than what they refuse (direct exploitation).

**Source:** D-002 Finding 5 (Safety Alignment Paradox), D-002 Ethical Boundaries section, D-002 Design Implication 3, S-001 Conflict 5 resolution, S-002 Safety Alignment Compatibility section.

### 6. Integration with Jerry Routing Standards

/eng-team and /red-team integrate with Jerry's existing skill routing infrastructure through the mandatory-skill-usage.md trigger map pattern (H-22) and the skill invocation mechanism defined in CLAUDE.md.

#### Trigger Map Registration

The following entries are added to `mandatory-skill-usage.md` Trigger Map:

| Detected Keywords | Skill |
|-------------------|-------|
| secure design, threat model, secure architecture, STRIDE, DREAD, secure implementation, code review for security, SAST, DAST, supply chain security, incident response, DevSecOps, OWASP, ASVS, CWE, CIS benchmark, SSDF, SLSA, build a secure, security requirements | `/eng-team` |
| penetration test, pentest, red team, offensive security, reconnaissance, exploit, privilege escalation, lateral movement, persistence, exfiltration, C2, command and control, social engineering, phishing, attack surface, kill chain, PTES, OSSTMM, ATT&CK, rules of engagement, engagement report | `/red-team` |

**Proactive invocation (H-22):** Both skills MUST be invoked proactively when trigger keywords are detected. The router does not wait for explicit `/eng-team` or `/red-team` invocation from the user.

#### CLAUDE.md Quick Reference Registration

| Skill | Purpose |
|-------|---------|
| `/eng-team` | Secure engineering: design, implementation, review, testing, CI/CD security, incident response |
| `/red-team` | Offensive security: penetration testing, red team engagements, vulnerability analysis, exploitation methodology |

#### Interaction with Existing Skills

| Existing Skill | Integration Pattern | When Both Apply |
|----------------|--------------------|-----------------|
| `/adversary` | eng-reviewer invokes /adversary for C2+ deliverables; red-reporter quality reviewed by /adversary | /adversary is the quality gate; /eng-team and /red-team are the domain skills |
| `/orchestration` | Multi-phase workflows (Pattern 1, Pattern 4) use /orchestration for phase tracking | /orchestration manages workflow state; skill routing manages agent selection |
| `/problem-solving` | Research tasks within an engagement (e.g., investigating a novel vulnerability) use /problem-solving agents | /problem-solving provides research methodology; /eng-team or /red-team provides domain context |
| `/worktracker` | All engagement progress tracked through /worktracker entities | /worktracker manages state persistence; skill routing manages execution flow |

**No routing conflicts with existing skills:** /eng-team and /red-team trigger keywords are domain-specific (cybersecurity terminology) and do not overlap with existing skill triggers (research/analysis for /problem-solving, requirements/specification for /nasa-se, pipeline/workflow for /orchestration). The keyword "red team" appears in both /adversary and /red-team trigger maps; disambiguation: "red team" in the context of adversarial quality review routes to /adversary; "red team" in the context of penetration testing or offensive security routes to /red-team.

### 7. Circuit Breaker Integration

The /red-team workflow integrates circuit breaker checks at every phase transition per F-002 R-AUTH-006. Circuit breakers prevent cascading failures (OWASP ASI08) where errors or scope violations propagate through the agent chain.

**Circuit breaker check sequence (executed at every /red-team agent transition):**

```
Before invoking next_agent:
  1. Verify scope compliance of current_agent's outputs
     - All actions within authorized target list
     - All techniques within authorized ATT&CK technique IDs
     - Time window still active
     - No exclusion list violations
  2. Confirm authorization for next_agent's capability domain
     - next_agent's required authorization level met in scope document
     - RoE permits the next phase (e.g., persistence authorized?)
  3. Evaluate engagement health
     - Check for cascading failure indicators
     - Assess cumulative scope boundary proximity
  4. Decision
     - PROCEED: transition to next_agent
     - ALERT: transition proceeds but red-lead notified of boundary proximity
     - PAUSE: transition blocked; red-lead must review and authorize
     - HALT: engagement suspended; user escalation required
```

**Circuit breaker applies to all transition types:**
- Forward transitions (red-recon to red-vuln to red-exploit)
- Backward cycles (red-exploit back to red-recon)
- Lateral transitions (red-recon to red-social)
- Phase skips (red-recon directly to red-exploit, skipping red-vuln)

**Circuit breaker threshold configuration:** Specific thresholds for ALERT vs. PAUSE vs. HALT are designated as Open Question OQ-006 in S-002. This ADR mandates the circuit breaker mechanism and check sequence; threshold configuration is deferred to FEAT-015 (Authorization & Scope Control Architecture) where the scope enforcement infrastructure is fully specified.

**Source:** F-002 R-AUTH-006; S-002 /red-team Non-Linear Kill Chain requirements; S-002 OQ-006.

### 8. Red-Lead as Mandatory First Agent

All /red-team engagements MUST start with red-lead for scope definition and authorization verification. No other /red-team agent can be invoked before red-lead establishes an active scope.

**Enforcement mechanism:**

```
On /red-team skill invocation:
  if no active_scope exists:
    Route to red-lead regardless of trigger keywords
    red-lead establishes:
      - Target authorization (IP ranges, domains, applications)
      - Technique authorization (ATT&CK technique IDs permitted)
      - Time window (engagement start/end)
      - Exclusion list (systems/data/techniques that must not be touched)
      - Rules of Engagement (RoE-gated agent access: persist, exfil, social)
      - Methodology selection (PTES, OSSTMM, or custom)
    Store scope document in engagement workspace
    Set active_scope = true
  if active_scope exists:
    Route to agent per keyword triggers and routing decision table
    Apply circuit breaker check (Section 7) before agent invocation
```

**Rationale:** The red-lead-first mandate is a structural authorization control, not a procedural guideline. It ensures that no reconnaissance, exploitation, or any other offensive activity occurs without explicit scope boundaries. This directly implements the principle from S-001 Convergence 3 that "authorization scope bounds risk more effectively than human oversight" -- the scope document created by red-lead becomes the structural constraint that all subsequent agent invocations are validated against.

**Exception: red-reporter without active scope.** red-reporter can be invoked without an active scope when the user requests report generation from previously collected findings (Routing Decision Table scenario 9). Report generation is a documentation activity, not an offensive activity, and does not require scope authorization.

**Source:** S-002 Routing Decision Table row 6; A-004 R-ROSTER-010 (expanded red-lead scope); F-002 R-AUTH-003 (scope oracle), R-AUTH-006 (circuit breaker); AD-004 (three-layer authorization).

---

## Options Considered

### Option A: Flat Keyword Routing (Rejected)

**Description:** Simple keyword-to-agent mapping without context awareness, workflow patterns, or cross-skill integration. Each incoming request is matched against a flat keyword table and routed to the single best-matching agent.

**Evaluation:**

| Dimension | Assessment |
|-----------|------------|
| Simplicity | HIGH -- minimal routing logic; easy to implement and debug |
| Disambiguation | LOW -- cannot resolve keyword collisions (e.g., "vulnerability" maps to eng-security OR red-vuln with no disambiguation) |
| Workflow support | NONE -- no sequential, parallel, or non-linear workflow orchestration |
| Cross-skill | NONE -- no purple team integration mechanism |
| Safety alignment | NONE -- no reframing of safety-filtered requests |
| Scalability | LOW -- 21 agents with overlapping security terminology would produce frequent misrouting |

**Rejection rationale:** Insufficient for the complexity of 21 agents across 2 skills with overlapping terminology. Flat routing cannot support /red-team's non-linear kill chain (R-ROSTER-014) or purple team integration (R-ROSTER-013). Misrouting risk is unacceptably high given that routing a defensive request to an offensive agent (or vice versa) would produce incorrect and potentially harmful guidance.

### Option B: Context-Aware Routing with Workflow Patterns (Selected)

**Description:** Multi-layer routing combining keyword triggers, context disambiguation, 5 workflow patterns, cross-skill integration points, circuit breaker enforcement, and safety alignment compatibility. This is the architecture documented in the Decision section.

**Evaluation:**

| Dimension | Assessment |
|-----------|------------|
| Simplicity | MEDIUM -- more complex routing logic; requires context analysis and workflow state tracking |
| Disambiguation | HIGH -- context-aware resolution of keyword collisions using offensive/defensive intent signals |
| Workflow support | HIGH -- 5 patterns covering sequential, non-linear, parallel, cross-skill, and conditional scenarios |
| Cross-skill | HIGH -- 4 defined integration points with activation criteria |
| Safety alignment | HIGH -- methodology-first reframing at routing layer; professional context in agent prompts |
| Scalability | HIGH -- pattern-based architecture accommodates roster changes (deferred agents) without routing redesign |

**Selection rationale:** Balances routing accuracy with implementation complexity. The 5 workflow patterns are compositions of simpler primitives (sequential handoff, parallel fork, conditional branch, cycle-back) that can be implemented incrementally. The context-disambiguation layer adds moderate complexity but eliminates the primary failure mode of flat routing (keyword collision misrouting). Circuit breaker integration makes /red-team routing structurally safe rather than procedurally safe.

### Option C: Intent Classification Model (Deferred)

**Description:** Train or fine-tune a classification model to predict the correct skill and agent from natural language requests, replacing keyword matching entirely.

**Evaluation:**

| Dimension | Assessment |
|-----------|------------|
| Simplicity | LOW -- requires training data, model training/fine-tuning, inference infrastructure |
| Disambiguation | POTENTIALLY HIGH -- a well-trained model could resolve ambiguity better than keyword rules |
| Workflow support | MEDIUM -- classification identifies the starting agent but still needs workflow orchestration |
| Cross-skill | MEDIUM -- can classify purple team intent but needs the same integration architecture |
| Safety alignment | SAME -- safety alignment is a model-level concern, not a routing-level one |
| Scalability | HIGH -- adapts to new agents through retraining rather than rule updates |

**Deferral rationale:** Option C requires training data that does not yet exist (PROJ-010 has no usage data). The classification model would still need the workflow patterns, circuit breakers, and integration points from Option B -- it replaces only the keyword-to-agent mapping layer. The additional infrastructure complexity (model hosting, training pipeline, evaluation) is not justified until PROJ-010 has operational usage data that demonstrates keyword routing limitations. Reconsideration trigger: if keyword routing accuracy falls below 85% in Phase 5 purple team exercises.

---

## Consequences

### Positive

| Consequence | Impact | Confidence |
|-------------|--------|------------|
| Unambiguous agent selection for 21 agents across 2 skills | Eliminates misrouting between offensive and defensive agents | HIGH -- keyword disambiguation rules cover all identified collision cases |
| /red-team structural safety through mandatory red-lead first + circuit breakers | Scope violations are structurally prevented, not procedurally prevented | HIGH -- follows Convergence 3 principle validated by 3 independent research streams |
| Purple team integration through defined cross-skill integration points | Enables the adversarial-collaborative dynamic that drives security improvement | HIGH -- 4 integration points derived from A-004 with elite organization validation |
| /eng-team workflow traces to established SDLC models (MS SDL, SSDF, SAMM, SLSA) | Every agent activity has standards traceability for audit and compliance | HIGH -- F-001 mapping provides practice-level traceability |
| Safety alignment compatibility without circumvention | Legitimate security work proceeds without triggering safety filters | HIGH -- methodology-first design validated by D-002 and Convergence 1 |
| Jerry routing standards compliance (H-22, H-25, H-26) | Both skills integrate seamlessly with existing Jerry infrastructure | HIGH -- architectural requirements are well-defined |

### Negative

| Consequence | Impact | Mitigation |
|-------------|--------|------------|
| Routing complexity increases skill invocation latency | Context disambiguation and circuit breaker checks add processing time to every /red-team transition | Circuit breaker checks are lightweight scope document lookups; context disambiguation operates on keyword matching, not model inference |
| Keyword trigger maintenance burden | 21 agents with evolving terminology require ongoing trigger map updates | Trigger maps are YAML configuration, not code; updates are additive (new keywords) not structural |
| Non-linear /red-team workflow complicates state tracking | Phase cycling creates complex engagement state that must be persisted across sessions | Jerry's filesystem-as-memory architecture (CLAUDE.md core solution) handles state persistence; /orchestration provides workflow tracking |
| Purple team routing introduces cross-skill coupling | Changes to one skill's routing may affect the other skill's integration points | Integration points are defined at the agent boundary level, not the routing logic level; agent capability changes require explicit integration point review |

### Neutral

| Consequence | Impact |
|-------------|--------|
| Option C (intent classification) is deferred, not rejected | If keyword routing proves insufficient, the classification layer can be added on top of Option B's workflow infrastructure without redesign |
| Circuit breaker threshold configuration is deferred to FEAT-015 | The mechanism is defined; thresholds require authorization architecture context that FEAT-015 provides |
| Routing architecture is roster-dependent | If deferred agents (eng-threatintel, eng-compliance, red-opsec, red-cloud) are activated, trigger maps must be extended but workflow patterns remain unchanged |

---

## Evidence Base

### Primary Evidence Sources

| Artifact | Contribution to This ADR | Confidence |
|----------|--------------------------|------------|
| S-002: Architecture Implications Synthesis | Definitive specification input: keyword triggers, routing decision table, 5 workflow patterns, safety alignment compatibility, cross-cutting concerns | HIGH -- synthesized from 6 streams and 20 artifacts |
| S-001: Cross-Stream Findings Consolidation | Agent team design, workflow patterns, 6 convergence findings, 5 conflict resolutions | HIGH -- cross-stream validation |
| A-004: Final Roster Recommendation | Non-linear kill chain (R-ROSTER-014), 4 cross-skill integration points (R-ROSTER-013), agent capability boundaries, ATT&CK coverage proof | HIGH -- validated against 7 elite organizations |
| F-001: Secure SDLC Lifecycle Patterns | /eng-team 8-step workflow sequence, agent-to-SDLC-phase mapping, layered SDLC model architecture | HIGH -- 5 SDLC models analyzed |
| F-002: Security Architecture Patterns | Circuit breaker mandate (R-AUTH-006), three-layer authorization, per-agent authorization model | HIGH -- OWASP Agentic AI Top 10 coverage |
| D-002: LLM Capability Boundaries | Safety alignment paradox, methodology-first validation, capability matrix, hallucination mitigation | HIGH -- academic benchmarks + industry evidence |

### Cross-Stream Convergence Validation

Three convergence findings from S-001 directly validate this ADR's design decisions:

| Convergence | Streams | ADR Decision It Validates |
|-------------|---------|---------------------------|
| Convergence 1: Methodology-First Design | D + C + A | Safety alignment compatibility (Section 5) -- routing produces methodology guidance, not execution |
| Convergence 3: Authorization Scope Over Human Oversight | F + C + D | Red-lead mandate (Section 8) + circuit breakers (Section 7) -- structural authorization over procedural |
| Convergence 6: Security Decomposition Requires Multiple Specialized Roles | A + B + F | Keyword trigger granularity (Section 2) -- 21 agents with distinct, non-overlapping capability domains |

### Conflict Resolutions Incorporated

| Conflict | Streams | Resolution Applied |
|----------|---------|-------------------|
| Conflict 5: Safety Alignment vs. Red Team Utility | D vs. PLAN.md | Section 5 -- methodology-first framing resolves the paradox |
| Conflict 3: Threat Intelligence Dedicated vs. Cross-Skill | A-001 vs. PLAN.md | Routing Decision Table scenario 12 -- red-recon to eng-architect cross-skill integration |

---

## Compliance

### Jerry Framework Compliance

| Rule | Compliance | Evidence |
|------|-----------|----------|
| H-22 (Proactive skill invocation) | COMPLIANT | Trigger maps in Section 2 and 6 registered for mandatory-skill-usage.md |
| H-25 (SKILL.md exactly, case-sensitive) | COMPLIANT | Section 1 specifies `SKILL.md` for both skills |
| H-26 (Kebab-case folder, matches name) | COMPLIANT | `skills/eng-team/` matches `name: eng-team`; `skills/red-team/` matches `name: red-team` |
| H-25 (No README.md in skill folder) | COMPLIANT | Neither skill folder contains README.md |
| H-26 (Description: WHAT+WHEN+triggers, <1024 chars, no XML) | COMPLIANT | Both descriptions specify what, when, and triggers; under 1024 characters; no XML |
| H-26 (Full repo-relative paths) | COMPLIANT | Agent definitions at `skills/{skill}/agents/{agent}.md` |
| H-26 (Register in CLAUDE.md + AGENTS.md + mandatory-skill-usage.md) | COMPLIANT | Section 6 specifies all three registration points |
| H-31 (Clarify when ambiguous) | COMPLIANT | Disambiguation rules default to /eng-team and confirm with user when ambiguous |
| P-003 (No recursive subagents) | COMPLIANT | Skills invoke agents as workers; no agent-spawns-agent chains |
| P-020 (User authority) | COMPLIANT | ADR status is PROPOSED; requires user ratification |

### PROJ-010 Requirements Compliance

| Requirement | Compliance | Evidence |
|-------------|-----------|----------|
| R-013 (C4 /adversary on every phase) | COMPLIANT | eng-reviewer invokes /adversary for C2+; quality target >= 0.95 |
| R-014 (Full /orchestration planning) | COMPLIANT | Multi-phase workflows use /orchestration for state tracking |
| R-018 (Real offensive techniques mapped to ATT&CK) | COMPLIANT | /red-team keyword triggers map to ATT&CK tactics via A-004 coverage proof |
| R-020 (Authorization verification) | COMPLIANT | Red-lead mandate (Section 8) + circuit breakers (Section 7) |

---

## Related Decisions

### Upstream Dependencies (This ADR Depends On)

| Decision | Relationship | Status |
|----------|-------------|--------|
| AD-001 (Methodology-First Design) | Foundational principle that constrains all routing to produce methodology guidance | Proposed in S-002; HIGH confidence |
| AD-002 (21-Agent Roster) | Defines the agents that routing must address | Proposed in S-002; HIGH confidence |
| AD-004 (Three-Layer Authorization) | Authorization model that /red-team routing integrates with | Proposed in S-002; HIGH confidence |

### Downstream Dependents (Depend On This ADR)

| Decision/Feature | Relationship | Impact if Changed |
|------------------|-------------|-------------------|
| FEAT-020 (/eng-team skill implementation) | Implements /eng-team SKILL.md, keyword triggers, and Pattern 1 workflow | Keyword triggers and workflow sequence must be updated |
| FEAT-030 (/red-team skill implementation) | Implements /red-team SKILL.md, keyword triggers, Pattern 2 workflow, and red-lead mandate | Non-linear workflow and circuit breaker integration must be updated |
| FEAT-015 (Authorization & Scope Control) | Provides the circuit breaker thresholds and scope oracle that this ADR's routing depends on | Circuit breaker check sequence (Section 7) depends on FEAT-015 threshold configuration |
| ADR-PROJ010-001 (Agent Team Architecture, if exists) | Agent capability boundaries used for keyword disambiguation | Capability boundary changes require trigger map updates |

### Parallel Decisions (Inform Each Other)

| Decision | Relationship |
|----------|-------------|
| FEAT-010 (Agent Team Architecture) | Agent definitions provide the capability boundaries that routing uses for disambiguation |
| FEAT-012 (LLM Portability Architecture) | Portable agent definitions must include routing metadata (triggers, workflow position) |
| FEAT-013 (Configurable Rule Set Architecture) | Rule set configuration affects routing context (standards-based agent selection) |
| FEAT-014 (Tool Integration Adapter Architecture) | Tool availability affects Pattern 5 conditional branching (tool-augmented vs. standalone routing) |

---

## Open Questions

### OQ-001: Purple Team Orchestration Ownership

**Context:** Pattern 4 (Purple Team Cross-Skill) requires coordinating agents from both /eng-team and /red-team. Neither skill individually owns the orchestration.

**Question:** Does purple team orchestration belong to a new cross-skill orchestrator, to /orchestration as a general-purpose workflow tool, or to one skill that acts as the lead for that specific integration point?

**Recommendation:** Use /orchestration as the cross-skill coordinator, with the "source" skill from each integration point leading its side. For Integration Point 1 (Threat-Informed Architecture), red-recon leads the offensive side and eng-architect leads the defensive side, with /orchestration managing the handoff.

### OQ-002: Trigger Map Versioning and Evolution

**Context:** As PROJ-010 gains operational usage, keyword triggers will need refinement. New security terminology emerges, user request patterns are discovered, and deferred agents may be activated.

**Question:** How are trigger map changes governed? Do they require ADR revision (this ADR is C4), or can trigger maps evolve independently with lighter governance?

**Recommendation:** Trigger maps are configuration, not architecture. Trigger keyword additions and adjustments should follow C2 governance (HARD + MEDIUM rules, S-014 scoring). Structural routing changes (new workflow patterns, new integration points, changes to disambiguation rules) require C3+ governance and this ADR's revision.

### OQ-003: Circuit Breaker Threshold Configuration

**Context:** Section 7 defines the circuit breaker mechanism and check sequence but defers threshold configuration to FEAT-015.

**Question:** What specific conditions trigger ALERT vs. PAUSE vs. HALT? Should thresholds be configurable per engagement profile?

**Recommendation:** Thresholds should be configurable per engagement profile, aligned with AD-007 (configurable rule sets). Default thresholds should be conservative (lower thresholds for ALERT and PAUSE). FEAT-015 must specify defaults and override mechanisms. This is OQ-006 from S-002.

---

## References

### Primary Research Artifacts

| Artifact | Location | Content |
|----------|----------|---------|
| S-002: Architecture Implications Synthesis | `projects/PROJ-010-cyber-ops/work/research/synthesis/S-002-architecture-implications.md` | Skill Routing Specification Input (keyword triggers, routing decision table, 5 workflow patterns); 12 architecture decisions |
| S-001: Cross-Stream Findings Consolidation | `projects/PROJ-010-cyber-ops/work/research/synthesis/S-001-cross-stream-findings.md` | 6 convergence findings, 5 conflict resolutions, agent team design, workflow patterns |
| A-004: Final Roster Recommendation | `projects/PROJ-010-cyber-ops/work/research/stream-a-role-completeness/A-004-roster-recommendation.md` | R-ROSTER-013 (cross-skill integration), R-ROSTER-014 (non-linear kill chain), 21-agent roster, ATT&CK 14/14 coverage |
| F-001: Secure SDLC Lifecycle Patterns | `projects/PROJ-010-cyber-ops/work/research/stream-f-secure-sdlc/F-001-secure-sdlc-patterns.md` | /eng-team 8-step workflow sequence, 5-model layered SDLC architecture, agent-to-phase mapping |
| F-002: Security Architecture Patterns | `projects/PROJ-010-cyber-ops/work/research/stream-f-secure-sdlc/F-002-security-architecture-patterns.md` | R-AUTH-006 (circuit breakers), three-layer authorization, per-agent authorization model |
| D-002: LLM Capability Boundaries | `projects/PROJ-010-cyber-ops/work/research/stream-d-prior-art/D-002-llm-capability-boundaries.md` | Safety alignment paradox, methodology-first validation, capability matrix |

### Jerry Framework References

| Document | Location | Content |
|----------|----------|---------|
| CLAUDE.md | `CLAUDE.md` | Identity, HARD constraints, skill quick reference |
| mandatory-skill-usage.md | `.context/rules/mandatory-skill-usage.md` | H-22 trigger map pattern, proactive invocation rules |
| quality-enforcement.md | `.context/rules/quality-enforcement.md` | Quality gate (>= 0.92), criticality levels, strategy catalog |
| skill-standards (H-25, H-26) | `.context/rules/` | SKILL.md naming, folder structure, description, registration |

### External Standards Referenced

| Standard | Usage in This ADR |
|----------|-------------------|
| MITRE ATT&CK Enterprise v14 | /red-team keyword triggers mapped to 14 tactics; agent-to-tactic assignment |
| PTES (Penetration Testing Execution Standard) | /red-team methodology framing for safety alignment; engagement phases |
| OSSTMM (Open Source Security Testing Methodology Manual) | Alternative methodology selection by red-lead |
| NIST SP 800-218 SSDF | /eng-team governance backbone; agent-to-practice mapping |
| Microsoft SDL | /eng-team workflow structure; 5-phase model maps to 8-step agent sequence |
| OWASP ASVS 5.0 | /eng-team verification standards; routing context for standards-aware agent selection |
| OWASP SAMM v2 | Maturity assessment integration; eng-lead routing context |
| Google SLSA v1.0 | Supply chain integrity; eng-infra and eng-devsecops routing context |
| OWASP Agentic AI Top 10 | Circuit breaker justification (ASI08); scope enforcement architecture |
| CyberSecEval 3 (Meta) | Safety alignment compliance data (52% to 28%); methodology-first validation |
