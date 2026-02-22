# Purple Team Integration Framework

<!--
DOCUMENT-ID: FEAT-040-PTIF
AUTHOR: Claude (ps-architect context)
DATE: 2026-02-22
STATUS: PROPOSED
PARENT-FEATURE: FEAT-040 (Purple Team Integration Framework)
PARENT-EPIC: EPIC-005 (Purple Team Validation)
PROJECT: PROJ-010-cyber-ops
TYPE: Integration Framework Specification
CRITICALITY: C4 (Critical -- cross-skill orchestration protocol governing adversarial-collaborative dynamics)
-->

> **Document ID:** FEAT-040-PTIF
> **Version:** 1.0.0
> **Date:** 2026-02-22
> **Status:** PROPOSED
> **Quality Target:** >= 0.95
> **Criticality:** C4
> **Parent Feature:** FEAT-040 (Purple Team Integration Framework)
> **Parent Epic:** EPIC-005 (Purple Team Validation)
> **SSOT References:** ADR-PROJ010-001 (Agent Team Architecture), ADR-PROJ010-006 (Authorization & Scope Control)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Stakeholder-level overview of purple team value proposition |
| [Purple Team Engagement Protocol](#purple-team-engagement-protocol) | Step-by-step workflow for initiating, executing, and concluding exercises |
| [Handoff Mechanisms](#handoff-mechanisms) | Detailed specifications for all 4 integration points |
| [Finding Flow](#finding-flow) | How red-team findings propagate to eng-team for remediation |
| [Remediation Tracking and Verification Loop](#remediation-tracking-and-verification-loop) | Fix, re-test, close cycle design |
| [Adversary Integration](#adversary-integration) | How /adversary scores purple team exercises |
| [Output Level Specifications](#output-level-specifications) | L0, L1, L2 output format requirements |
| [L2: Strategic Implications](#l2-strategic-implications) | Long-term value, maturity model, measurement framework |
| [Compliance](#compliance) | Constitutional and requirement compliance |
| [References](#references) | Source citations with traceability |

---

## L0: Executive Summary

### What Purple Team Integration Achieves

The Purple Team Integration Framework defines how PROJ-010's two complementary skills -- /eng-team (10 agents for secure software engineering) and /red-team (11 agents for offensive security) -- engage adversarially to produce security outcomes superior to either skill operating in isolation. The framework operationalizes the design principle stated in ADR-PROJ010-001: "the two skills work as adversaries: /eng-team builds, /red-team breaks. The gap between them is where the hardening happens."

This is not a testing methodology. It is an orchestration protocol that governs how defensive engineering artifacts become offensive attack targets, how offensive findings become defensive remediation work items, and how the cycle repeats until measurable hardening objectives are achieved.

### Key Stakeholder Value

| Stakeholder | Value Delivered |
|-------------|-----------------|
| **Engineering leadership** | Quantifiable security posture improvement through adversarial validation; measurable reduction in exploitable attack surface across design, implementation, and operations |
| **Security teams** | Structured purple team exercises with defined engagement protocols, reproducible finding formats (SARIF v2.1.0 per AD-006), and evidence-based remediation tracking |
| **Project managers** | Clear workflow phases with defined entry/exit criteria, progress metrics tied to finding resolution rates, and maturity-level progression tracking |
| **Compliance officers** | Audit trail from vulnerability discovery through remediation verification, traceability from findings to ATT&CK techniques to SSDF practices, and formal closure attestation |

### Framework Design Principles

Four principles govern all purple team operations:

1. **Architectural scope enforcement.** All offensive operations conform to ADR-PROJ010-006's three-layer authorization architecture. Purple team exercises inherit the scope enforcement infrastructure -- the Scope Oracle, Tool Proxy, Network Enforcer, and Credential Broker validate every action. Security is structural, not procedural (S-001 Convergence 3, 2026-02-22).

2. **Methodology-first engagement.** Consistent with AD-001 (Methodology-First Design Paradigm), purple team exercises produce methodology guidance, structured analysis, and verification instructions. Agents guide practitioners; they do not autonomously exploit targets (D-002, 2026-02-22).

3. **Evidence-based finding flow.** Every finding includes ATT&CK technique IDs, CVSS/DREAD severity scores, SARIF-formatted evidence, and explicit remediation guidance. No finding is communicated without supporting evidence (P-001 Truth and Accuracy, P-004 Explicit Provenance).

4. **Closed-loop remediation.** Every finding enters a tracked remediation lifecycle: discovery, triage, assignment, fix, re-test, verification, closure. No finding is closed without re-test confirmation by the originating offensive agent.

**Evidence basis:** ADR-PROJ010-001 Section 5 (Cross-Skill Integration Points, 2026-02-22); ADR-PROJ010-006 (Authorization Architecture, 2026-02-22); S-002 Pattern 4 (Purple Team Cross-Skill routing, 2026-02-22); A-002 Finding 7 (Netflix Attack Emulation Team validates adversarial-collaborative dynamic, 2026-02-22).

---

## Purple Team Engagement Protocol

### Protocol Overview

A purple team engagement is a structured adversarial exercise where /eng-team and /red-team operate on shared artifacts within a defined scope. The protocol comprises six phases with defined entry criteria, activities, exit criteria, and quality gates.

```
Phase 1: Engagement Planning
    |
Phase 2: Defensive Baseline
    |
Phase 3: Offensive Assessment
    |
Phase 4: Finding Synthesis & Remediation
    |
Phase 5: Verification & Re-Test
    |
Phase 6: Closure & Reporting
```

### Phase 1: Engagement Planning

| Attribute | Value |
|-----------|-------|
| **Duration** | Session start; prerequisite for all subsequent phases |
| **Entry Criteria** | Active PROJ-010 project context; identified target system, component, or design artifact |
| **Primary Agents** | red-lead (scope), eng-architect (target nomination), eng-lead (engineering context) |
| **Quality Gate** | Scope document signed and loaded; eng-team target artifacts identified |

#### Activities

1. **Target nomination.** eng-architect or eng-lead identifies the engineering artifact to be assessed. This may be a threat model, architecture design, implementation, infrastructure configuration, or incident response plan.

2. **Scope definition.** red-lead creates the engagement scope document per ADR-PROJ010-006 Section 9. For purple team exercises, the scope document includes:
   - `engagement_id` in `PT-NNNN` format (purple team namespace)
   - `authorized_targets` derived from eng-team artifact boundaries
   - `technique_allowlist` aligned with the integration point being exercised
   - `time_window` for the exercise duration
   - `rules_of_engagement` including purple team-specific constraints (e.g., cooperative finding disclosure, real-time communication channel)
   - `agent_authorizations` scoped to the integration points under test

3. **Integration point selection.** The engagement plan specifies which of the 4 integration points (defined in ADR-PROJ010-001 Section 5) are in scope for this exercise. Each integration point activates a defined set of agent pairings.

4. **Communication channel establishment.** Purple team exercises require a real-time communication channel between offensive and defensive agents. This channel enables cooperative disclosure of findings during the exercise (unlike a pure red team assessment where findings are withheld until reporting). The channel is defined in the scope document's `rules_of_engagement.communication_channel` field.

5. **Baseline artifact exchange.** eng-team provides the target artifacts to be assessed. These are loaded into the engagement evidence vault as the defensive baseline. red-team reviews the baseline to plan the offensive approach.

#### Phase 1 Output

| Artifact | Owner | Location |
|----------|-------|----------|
| Purple team scope document | red-lead | `skills/red-team/output/{engagement-id}/red-lead-scope.md` |
| Target artifact inventory | eng-architect / eng-lead | `skills/eng-team/output/{engagement-id}/eng-architect-target-inventory.md` |
| Integration point selection | Both | Encoded in scope document `agent_authorizations` |

**Evidence basis:** ADR-PROJ010-006 Section 9 (Scope Document Specification, 2026-02-22); red-team SKILL.md Mandatory Authorization section (2026-02-22).

### Phase 2: Defensive Baseline

| Attribute | Value |
|-----------|-------|
| **Duration** | Follows Phase 1; eng-team produces or identifies existing artifacts |
| **Entry Criteria** | Signed scope document; target artifacts nominated |
| **Primary Agents** | eng-architect, eng-lead, eng-backend, eng-frontend, eng-infra, eng-devsecops, eng-qa, eng-security |
| **Quality Gate** | Baseline artifacts pass eng-reviewer quality gate at >= 0.95 per R-013 |

#### Activities

1. **Baseline artifact production or identification.** If target artifacts already exist (e.g., an existing threat model or implementation), they are ingested as the baseline. If the exercise is assessing a new design, eng-team produces the baseline through its 8-step sequential workflow.

2. **Baseline artifact types by integration point.** Each integration point defines what eng-team artifacts constitute the "defensive baseline" that red-team will attack:

   | Integration Point | Eng-Team Baseline Artifacts | Producing Agents |
   |-------------------|----------------------------|------------------|
   | IP-1: Threat-Informed Architecture | Threat model (STRIDE/DREAD), architecture design, trust boundary diagrams, ADRs | eng-architect |
   | IP-2: Attack Surface Validation | Infrastructure configuration, container hardening specs, SBOM, DevSecOps pipeline configs, scan results | eng-infra, eng-devsecops |
   | IP-3: Secure Code vs. Exploitation | Implementation code, code review findings, ASVS verification results, SAST/DAST scan outputs | eng-backend, eng-frontend, eng-security, eng-devsecops |
   | IP-4: Incident Response Validation | IR runbooks, monitoring configuration, detection rules, vulnerability lifecycle procedures | eng-incident |

3. **Baseline quality gate.** eng-reviewer validates baseline artifacts against quality standards. For C2+ exercises, /adversary integration applies per the eng-team SKILL.md Adversarial Quality Mode section. Baseline artifacts must achieve >= 0.95 quality score before the exercise proceeds to Phase 3.

#### Phase 2 Output

| Artifact | Owner | Location |
|----------|-------|----------|
| Baseline artifacts (per integration point) | eng-team agents | `skills/eng-team/output/{engagement-id}/` |
| Baseline quality gate report | eng-reviewer | `skills/eng-team/output/{engagement-id}/eng-reviewer-baseline-gate.md` |

**Evidence basis:** eng-team SKILL.md Orchestration Flow (8-step workflow, 2026-02-22); ADR-PROJ010-001 Section 8 (Layered SDLC Governance, 2026-02-22).

### Phase 3: Offensive Assessment

| Attribute | Value |
|-----------|-------|
| **Duration** | Core exercise phase; duration per scope document time window |
| **Entry Criteria** | Baseline artifacts at >= 0.95 quality; scope document active; circuit breaker checks passing |
| **Primary Agents** | red-recon, red-vuln, red-exploit, red-privesc, red-lateral, red-persist, red-exfil, red-infra, red-social (per scope authorization) |
| **Quality Gate** | All findings documented in SARIF v2.1.0; evidence chain complete; scope compliance confirmed |

#### Activities

1. **Offensive execution per integration point.** Red-team agents assess eng-team baseline artifacts using their non-linear kill chain workflow (ADR-PROJ010-001 Section 5). The kill chain organizes capability, not workflow sequence -- agents cycle between phases as findings dictate.

   | Integration Point | Red-Team Assessment Activities | Active Agents |
   |-------------------|-------------------------------|---------------|
   | IP-1: Threat-Informed Architecture | Review threat model completeness against known adversary TTPs; identify missing threat scenarios; assess trust boundary adequacy; validate DREAD scoring against real exploit availability | red-recon, red-vuln |
   | IP-2: Attack Surface Validation | Test infrastructure hardening effectiveness; validate container security; probe for exposed services; test DevSecOps pipeline bypass paths | red-recon, red-vuln, red-infra |
   | IP-3: Secure Code vs. Exploitation | Attempt exploitation of implemented code; test auth/authz bypass; probe input validation; demonstrate privilege escalation paths; test detection evasion against SAST/DAST | red-exploit, red-privesc, red-vuln |
   | IP-4: Incident Response Validation | Execute post-exploitation techniques against IR runbooks; test detection rule coverage; probe persistence mechanisms; test exfiltration channels against monitoring | red-persist, red-lateral, red-exfil |

2. **Circuit breaker enforcement.** Per ADR-PROJ010-006 Section 2, the circuit breaker check occurs at every agent transition during the offensive assessment. Scope revalidation, time window check, technique check, agent authorization check, and RoE gate checks execute at every transition. Any check failure halts the offensive assessment and routes to red-lead for scope review.

3. **Real-time finding communication.** In purple team exercises (unlike pure red team assessments), findings are communicated through the established communication channel as they are discovered. This enables:
   - eng-team to observe the attack methodology in real-time
   - Immediate cooperative discussion of defensive gaps
   - Real-time adjustment of defensive posture (if the scope document permits)
   - Shared understanding of finding severity and exploitability

4. **Evidence collection.** All findings are documented with:
   - SARIF v2.1.0 formatted finding record (per AD-006)
   - MITRE ATT&CK technique ID mapping
   - Severity classification (Critical/High/Medium/Low/Informational)
   - Evidence artifacts stored in the engagement evidence vault
   - Chain-of-custody from discovery through agent action to scope authorization

#### Phase 3 Output

| Artifact | Owner | Location |
|----------|-------|----------|
| Finding records (SARIF v2.1.0) | red-team agents | `skills/red-team/output/{engagement-id}/findings/` |
| Evidence artifacts | red-team agents | `skills/red-team/output/{engagement-id}/evidence/` |
| Interim finding notifications | red-reporter | Real-time via communication channel |
| Scope compliance log | Audit Logger | `skills/red-team/output/{engagement-id}/audit/` |

**Evidence basis:** red-team SKILL.md Orchestration Flow (non-linear kill chain, 2026-02-22); ADR-PROJ010-006 Section 2 (Dynamic Authorization, 2026-02-22); ADR-PROJ010-001 Section 5 (Cross-Skill Integration Points, 2026-02-22).

### Phase 4: Finding Synthesis and Remediation Assignment

| Attribute | Value |
|-----------|-------|
| **Duration** | Follows Phase 3 offensive assessment completion |
| **Entry Criteria** | Offensive assessment complete; all findings documented in SARIF v2.1.0; scope compliance confirmed |
| **Primary Agents** | red-reporter (synthesis), eng-security (triage), eng-devsecops (automated remediation), eng-architect (architectural findings) |
| **Quality Gate** | Finding synthesis report passes /adversary quality gate at >= 0.95; all findings triaged and assigned |

#### Activities

1. **Finding consolidation.** red-reporter collects all findings from Phase 3 and produces the consolidated finding synthesis report. This includes:
   - Cross-finding correlation (multiple findings exploiting the same root cause)
   - Severity-weighted risk scoring
   - ATT&CK technique coverage analysis (which tactics/techniques succeeded, which were blocked)
   - Remediation recommendations with priority ordering
   - Impact assessment following the shared ownership model (red-exploit for technical impact demonstration, red-reporter for impact documentation per ADR-PROJ010-001 S-001 Conflict 2 resolution)

2. **Triage and assignment.** eng-security reviews the consolidated findings and assigns remediation ownership:

   | Finding Category | Assigned To | Rationale |
   |-----------------|-------------|-----------|
   | Architecture/design flaws | eng-architect | Threat model gaps, trust boundary issues, architectural vulnerabilities |
   | Implementation vulnerabilities | eng-backend / eng-frontend | Code-level security flaws, input validation bypasses, auth/authz issues |
   | Infrastructure misconfigurations | eng-infra | Container hardening gaps, IaC security issues, network segmentation failures |
   | Pipeline/tooling gaps | eng-devsecops | SAST/DAST coverage gaps, scanning rule misses, pipeline bypass paths |
   | Detection/response gaps | eng-incident | IR runbook deficiencies, monitoring blind spots, detection rule failures |
   | Test coverage gaps | eng-qa | Missing security test cases, fuzzing coverage holes |

3. **Remediation plan creation.** Each assigned eng-team agent produces a remediation plan for their assigned findings. The plan includes:
   - Root cause analysis
   - Proposed fix with implementation guidance
   - Estimated effort and timeline
   - Re-test criteria (what red-team must verify to close the finding)
   - SSDF practice reference (traceability to governance framework per ADR-PROJ010-001 Section 8)

#### Phase 4 Output

| Artifact | Owner | Location |
|----------|-------|----------|
| Consolidated finding synthesis report | red-reporter | `skills/red-team/output/{engagement-id}/red-reporter-finding-synthesis.md` |
| Triage and assignment matrix | eng-security | `skills/eng-team/output/{engagement-id}/eng-security-triage-matrix.md` |
| Remediation plans (per assigned agent) | Assigned eng-team agents | `skills/eng-team/output/{engagement-id}/{agent}-remediation-{finding-id}.md` |

**Evidence basis:** AD-006 (SARIF-Based Finding Normalization, S-002, 2026-02-22); ADR-PROJ010-001 Section 5 (Impact shared ownership, S-001 Conflict 2 resolution, 2026-02-22).

### Phase 5: Verification and Re-Test

| Attribute | Value |
|-----------|-------|
| **Duration** | Iterative; repeats until all Critical and High findings are verified closed |
| **Entry Criteria** | Remediation plans complete; fixes implemented; re-test scope authorized in scope document |
| **Primary Agents** | Originating red-team agents (re-test), eng-reviewer (verification gate) |
| **Quality Gate** | All Critical findings verified closed; all High findings verified closed or risk-accepted; verification report passes /adversary quality gate |

#### Activities

1. **Fix implementation.** Assigned eng-team agents implement the remediation per their remediation plans. Fix artifacts are persisted to the engagement output directory.

2. **Re-test execution.** The originating red-team agent (the agent that discovered the finding) re-tests the remediated artifact using the same technique that produced the original finding. Re-test results are documented as a SARIF finding update with one of three outcomes:

   | Re-Test Outcome | Definition | Next Action |
   |-----------------|-----------|-------------|
   | **VERIFIED_CLOSED** | The original exploitation technique no longer succeeds against the remediated artifact. The vulnerability is confirmed fixed. | Finding status updated to `closed`. No further action. |
   | **PARTIALLY_REMEDIATED** | The original technique is blocked, but a variant or bypass still succeeds. The root cause is not fully addressed. | Finding returns to Phase 4 for revised remediation. Re-test cycle repeats. |
   | **NOT_REMEDIATED** | The original exploitation technique still succeeds. The fix is ineffective. | Finding returns to Phase 4 with escalated priority. Root cause re-analyzed. |

3. **Verification cycle iteration.** Findings that are not fully remediated cycle back through Phase 4 (revised remediation plan) and Phase 5 (re-test). This cycle repeats until the finding achieves VERIFIED_CLOSED status or is formally risk-accepted by the engagement stakeholder.

4. **Risk acceptance process.** Findings that cannot be remediated within the engagement time window may be formally risk-accepted. Risk acceptance requires:
   - Documented justification for acceptance
   - Compensating controls identified (if any)
   - Residual risk level assessed
   - Stakeholder sign-off (per P-020 User Authority)
   - Risk acceptance recorded in the finding synthesis report

#### Phase 5 Output

| Artifact | Owner | Location |
|----------|-------|----------|
| Re-test results (SARIF updates) | Originating red-team agents | `skills/red-team/output/{engagement-id}/findings/{finding-id}-retest.sarif.md` |
| Verification status matrix | eng-reviewer | `skills/eng-team/output/{engagement-id}/eng-reviewer-verification-matrix.md` |
| Risk acceptance records (if any) | eng-security | `skills/eng-team/output/{engagement-id}/eng-security-risk-acceptance.md` |

**Evidence basis:** ADR-PROJ010-006 Section 7 (Audit Trail Requirements, 2026-02-22); F-002 Pattern 3 (Post-Execution Audit Verification, 2026-02-22).

### Phase 6: Closure and Reporting

| Attribute | Value |
|-----------|-------|
| **Duration** | Final phase; produces engagement deliverables |
| **Entry Criteria** | All findings triaged to terminal state (VERIFIED_CLOSED or risk-accepted) |
| **Primary Agents** | red-reporter (engagement report), eng-reviewer (final quality gate), red-lead (scope compliance) |
| **Quality Gate** | Final report passes /adversary C4 quality gate at >= 0.95; scope compliance attestation signed |

#### Activities

1. **Final engagement report generation.** red-reporter produces the comprehensive engagement report including:
   - L0 Executive Summary for leadership
   - L1 Technical Detail for engineering teams
   - L2 Strategic Implications for architecture and governance
   - Full finding inventory with resolution status
   - ATT&CK coverage map (techniques tested vs. techniques that succeeded)
   - Remediation effectiveness metrics
   - Residual risk assessment
   - Recommendations for security posture improvement

2. **Scope compliance attestation.** red-lead reviews the audit trail and produces the scope compliance report per ADR-PROJ010-006 Layer 3. This attests that the entire engagement operated within authorized scope boundaries.

3. **Quality gate review.** eng-reviewer applies the final quality gate per R-013. For C4 exercises (and all purple team exercises are C4 per the criticality of cross-skill orchestration), the full /adversary tournament review applies with all 10 selected strategies.

4. **Engagement closure.** The engagement is formally closed. The scope document is marked as concluded. Evidence vault is sealed for retention per the evidence handling policy.

#### Phase 6 Output

| Artifact | Owner | Location |
|----------|-------|----------|
| Final engagement report (L0/L1/L2) | red-reporter | `skills/red-team/output/{engagement-id}/red-reporter-final-report.md` |
| Scope compliance attestation | red-lead | `skills/red-team/output/{engagement-id}/red-lead-compliance.md` |
| Quality gate report | eng-reviewer | `skills/eng-team/output/{engagement-id}/eng-reviewer-final-gate.md` |
| /adversary quality scores | /adversary | `skills/eng-team/output/{engagement-id}/adversary-quality-scores.md` |

**Evidence basis:** red-team SKILL.md (red-reporter mandatory last for reporting, 2026-02-22); eng-team SKILL.md (eng-reviewer final gate with /adversary, 2026-02-22); quality-enforcement.md (C4 criticality requires all 10 strategies, 2026-02-22).

---

## Handoff Mechanisms

### Integration Point Architecture

Four integration points define the purple team seams between /eng-team and /red-team. Each integration point specifies the source agents, target agents, data format, trigger conditions, and handoff protocol. These integration points were established in ADR-PROJ010-001 Section 5 and validated against the Netflix Attack Emulation Team model (A-002 Finding 7, 2026-02-22).

### Integration Point 1: Threat-Informed Architecture

| Attribute | Value |
|-----------|-------|
| **Direction** | Bidirectional: eng-architect <-> red-recon |
| **Primary Flow** | eng-architect threat models -> red-recon attack planning -> eng-architect model refinement |
| **Trigger** | eng-architect produces a threat model (STRIDE/DREAD/Attack Trees); red-recon produces threat intelligence |
| **Data Format** | Threat model artifact (markdown with STRIDE matrices, DREAD scores, trust boundary diagrams) |

#### Handoff Protocol

**eng-architect to red-recon (defensive to offensive):**

1. eng-architect produces a threat model using the criticality-based methodology escalation defined in ADR-PROJ010-001 Section 9 (STRIDE for C1, STRIDE+DREAD for C2, adding Attack Trees at C3, adding PASTA stages 4-7 at C4).
2. The threat model is persisted to `skills/eng-team/output/{engagement-id}/eng-architect-threat-model.md`.
3. red-recon consumes the threat model to identify gaps: threats that eng-architect did not anticipate, attack surfaces not covered by trust boundaries, DREAD scores that underestimate real exploit availability.
4. red-recon produces a threat intelligence supplement mapping real adversary TTPs (MITRE ATT&CK technique IDs) to the threat model's identified threats.

**red-recon to eng-architect (offensive to defensive):**

1. red-recon produces attack surface intelligence during reconnaissance operations.
2. Intelligence includes: adversary TTPs observed in the wild, attack surface elements not present in the original threat model, technology-specific vulnerability patterns.
3. eng-architect consumes this intelligence to refine the threat model: add missing threat scenarios, update DREAD scores with real-world exploit availability data, extend trust boundaries to cover newly identified attack surfaces.

#### Data Exchange Specification

| Field | Type | Description |
|-------|------|-------------|
| `threat_model_id` | string | Identifier linking to the eng-architect threat model |
| `attack_surface_elements` | list[object] | Newly identified attack surface components with ATT&CK technique mapping |
| `ttp_mapping` | list[object] | Real adversary TTPs mapped to threat model threats (technique ID, group attribution, prevalence) |
| `dread_adjustments` | list[object] | Recommended DREAD score adjustments with evidence (finding ID, exploit availability data) |
| `coverage_gaps` | list[string] | Threat scenarios present in the real threat landscape but absent from the threat model |
| `trust_boundary_gaps` | list[object] | Attack surfaces that cross trust boundaries not identified in the original model |

**Evidence basis:** ADR-PROJ010-001 Section 5 Integration Point 1 (2026-02-22); ADR-PROJ010-001 Section 9 (Threat Modeling Methodology AD-009, 2026-02-22); S-002 Cross-Skill Integration Points table (2026-02-22).

### Integration Point 2: Attack Surface Validation

| Attribute | Value |
|-----------|-------|
| **Direction** | Unidirectional: eng-infra/eng-devsecops -> red-recon/red-vuln (target provisioning); red-recon/red-vuln -> eng-infra/eng-devsecops (validation results) |
| **Primary Flow** | eng-team hardened targets -> red-team validates hardening effectiveness -> eng-team remediates gaps |
| **Trigger** | eng-infra produces infrastructure configuration or eng-devsecops updates pipeline security |
| **Data Format** | Infrastructure specifications (IaC, container configs, SBOM); validation results (SARIF v2.1.0 findings) |

#### Handoff Protocol

**eng-infra/eng-devsecops to red-recon/red-vuln (defensive to offensive):**

1. eng-infra produces infrastructure hardening artifacts: IaC templates, container security configurations, network segmentation rules, SBOM with dependency provenance.
2. eng-devsecops produces pipeline security artifacts: SAST/DAST configuration, secrets scanning rules, container scanning policies, dependency analysis configuration.
3. These artifacts define the "hardened target" that red-team will validate.

**red-recon/red-vuln to eng-infra/eng-devsecops (offensive to defensive):**

1. red-recon performs attack surface mapping against the hardened infrastructure. Identifies exposed services, open ports, misconfigured network segments, container escape paths.
2. red-vuln performs vulnerability analysis against the hardened targets. Identifies CVEs in container base images, IaC misconfigurations, pipeline bypass paths.
3. Validation results are produced as SARIF v2.1.0 findings with severity classification and remediation guidance.

#### Data Exchange Specification

| Field | Type | Description |
|-------|------|-------------|
| `target_inventory` | list[object] | Infrastructure components under test (container images, IaC templates, network segments) |
| `hardening_specifications` | list[object] | CIS Benchmark references, SLSA build levels, container security policies applied |
| `validation_findings` | list[SARIF_Result] | SARIF v2.1.0 formatted findings from validation testing |
| `attack_surface_delta` | object | Comparison of intended attack surface (per eng-infra design) vs. actual attack surface (per red-recon mapping) |
| `pipeline_bypass_paths` | list[object] | DevSecOps pipeline configurations that can be circumvented, with technique descriptions |

**Evidence basis:** ADR-PROJ010-001 Section 5 Integration Point 2 (2026-02-22); S-002 Agent Architecture Specification Input (eng-infra, eng-devsecops tool categories, 2026-02-22).

### Integration Point 3: Secure Code vs. Exploitation

| Attribute | Value |
|-----------|-------|
| **Direction** | Bidirectional: eng-security/eng-backend/eng-frontend <-> red-exploit/red-privesc |
| **Primary Flow** | eng-team reviewed code -> red-team exploitation attempts -> eng-team targeted remediation |
| **Trigger** | eng-security completes code review; eng-backend/eng-frontend produce implementation artifacts |
| **Data Format** | Code review findings (ASVS verification); exploitation results (SARIF v2.1.0 with PoC references) |

#### Handoff Protocol

**eng-team to red-team (defensive to offensive):**

1. eng-security produces code review findings against CWE Top 25 and OWASP ASVS. The review report identifies vulnerabilities found and, critically, areas assessed as secure.
2. eng-backend/eng-frontend produce implementation artifacts with security controls (input validation, auth/authz, output encoding, CSP/CORS configuration).
3. eng-devsecops produces automated scan results (SAST/DAST findings) that represent the automated security baseline.

**red-team to eng-team (offensive to defensive):**

1. red-exploit attempts exploitation of the implemented code, focusing on:
   - Vulnerabilities identified by eng-security (confirming exploitability and severity)
   - Areas assessed as secure (testing whether secure coding practices withstand real exploitation)
   - Automated scan gaps (testing for vulnerabilities that SAST/DAST missed)
2. red-privesc tests privilege boundaries in the implementation: authentication bypass, authorization escalation, token manipulation, credential harvesting.
3. Exploitation results include PoC demonstrations (methodology guidance, not weaponized exploit code per AD-001), SARIF-formatted findings, and remediation guidance targeting the specific implementation patterns.

#### Data Exchange Specification

| Field | Type | Description |
|-------|------|-------------|
| `code_review_report` | object | eng-security review with CWE mappings, ASVS references, and secure/vulnerable assessments |
| `sast_dast_results` | list[SARIF_Result] | Automated scan findings from eng-devsecops |
| `exploitation_results` | list[SARIF_Result] | red-exploit/red-privesc findings with ATT&CK technique IDs |
| `bypass_demonstrations` | list[object] | Methodology guidance for bypassing identified security controls (PoC approach, not weaponized code) |
| `detection_evasion_results` | list[object] | Techniques that evaded SAST/DAST detection, with evasion method and recommendation for rule improvement |
| `privilege_boundary_results` | list[object] | Privilege escalation path analysis with affected auth/authz controls |

**Evidence basis:** ADR-PROJ010-001 Section 5 Integration Point 3 (2026-02-22); eng-team SKILL.md (eng-security CWE Top 25 + OWASP ASVS review, 2026-02-22); red-team SKILL.md (red-exploit TA0001/TA0002, red-privesc TA0004/TA0006, 2026-02-22).

### Integration Point 4: Incident Response Validation

| Attribute | Value |
|-----------|-------|
| **Direction** | Bidirectional: eng-incident <-> red-persist/red-lateral/red-exfil |
| **Primary Flow** | eng-incident response plans -> red-team post-exploitation testing -> eng-incident plan revision |
| **Trigger** | eng-incident produces IR runbooks and monitoring configuration; red-team reaches post-exploitation phase |
| **Data Format** | IR runbooks (markdown); exercise results (SARIF v2.1.0 with detection gap analysis) |

#### Handoff Protocol

**eng-incident to red-team (defensive to offensive):**

1. eng-incident produces incident response artifacts: IR runbooks for specific scenarios, monitoring configuration (detection rules, alerting thresholds), containment procedures, and vulnerability lifecycle management procedures.
2. These artifacts define the "response baseline" -- what eng-incident expects to detect, contain, and remediate.

**red-team to eng-incident (offensive to defensive):**

1. red-persist tests detection rule coverage by establishing persistence mechanisms (TA0003) and observing whether eng-incident's monitoring detects the activity. Persistence-phase defense evasion techniques (indicator removal, timestomping) test the resilience of detection rules.
2. red-lateral tests containment procedure effectiveness by executing lateral movement (TA0008) and discovery (TA0007) within authorized scope. Tests whether network segmentation and monitoring detect internal movement.
3. red-exfil tests data loss prevention by executing exfiltration techniques (TA0009/TA0010) within authorized data types. Tests whether DLP controls and monitoring detect data exfiltration attempts.
4. Exercise results include: detection gap analysis (what was detected vs. what evaded detection), containment effectiveness assessment (whether containment procedures limited blast radius), and evasion success documentation (which techniques evaded which controls).

#### Data Exchange Specification

| Field | Type | Description |
|-------|------|-------------|
| `ir_runbooks` | list[object] | eng-incident response plans with detection rules, containment procedures, escalation paths |
| `monitoring_config` | object | Detection rule specifications, alerting thresholds, log collection scope |
| `detection_gap_analysis` | list[object] | Post-exploitation activities that evaded detection, with technique ID and evasion method |
| `containment_effectiveness` | list[object] | Containment procedures tested with success/failure per containment boundary |
| `exfiltration_test_results` | list[object] | DLP control effectiveness per exfiltration technique; channels tested and detection status |
| `evasion_catalog` | list[object] | Defense evasion techniques that succeeded, with recommended detection improvements |

**Evidence basis:** ADR-PROJ010-001 Section 5 Integration Point 4 (2026-02-22); ADR-PROJ010-001 Section 6 (Defense Evasion Ownership Model, 2026-02-22); red-team SKILL.md (RoE-gated agents red-persist, red-exfil, 2026-02-22).

---

## Finding Flow

### Finding Lifecycle

Every finding discovered during a purple team exercise follows a defined lifecycle from discovery through closure. The lifecycle ensures that no finding is lost, every finding is tracked to resolution, and all finding transitions are auditable.

```
DISCOVERED --> TRIAGED --> ASSIGNED --> IN_REMEDIATION --> RE_TESTED --> CLOSED
                  |                                           |
                  +--> RISK_ACCEPTED                         +--> PARTIALLY_REMEDIATED --> (back to ASSIGNED)
                                                             +--> NOT_REMEDIATED --> (back to ASSIGNED, escalated)
```

### Finding Record Format (SARIF v2.1.0)

All findings are recorded in SARIF v2.1.0 format per AD-006 (SARIF-Based Finding Normalization, S-002, 2026-02-22). The SARIF format provides cross-tool interoperability, industry-standard severity classification, and machine-readable finding records.

Each finding record contains the following fields from the AD-006 common Finding schema:

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `id` | string | Unique finding identifier within the engagement (`PT-NNNN-FFF` format) | Yes |
| `source_tool` | string | Agent and tool that produced the finding (e.g., `red-exploit/metasploit`) | Yes |
| `severity` | enum | `critical`, `high`, `medium`, `low`, `informational` | Yes |
| `category` | string | Finding category (e.g., `injection`, `broken-auth`, `misconfig`, `detection-gap`) | Yes |
| `title` | string | Concise finding title | Yes |
| `description` | string | Detailed finding description with exploitation methodology | Yes |
| `location` | object | Affected component, file, endpoint, or infrastructure element | Yes |
| `evidence` | list[object] | Supporting evidence (tool output, screenshots, log entries) stored in evidence vault | Yes |
| `remediation` | object | Recommended fix with implementation guidance and SSDF practice reference | Yes |
| `references` | list[object] | ATT&CK technique IDs, CVE references, CWE mappings, ASVS requirements | Yes |
| `confidence` | enum | `confirmed`, `probable`, `possible` | Yes |
| `raw_data` | object | Original tool output for verification | No |

### Severity Classification

Finding severity follows a five-level scale aligned with CVSS v3.1 qualitative ratings and the criticality levels from quality-enforcement.md:

| Severity | CVSS Range | Definition | SLA |
|----------|-----------|------------|-----|
| **Critical** | 9.0 - 10.0 | Exploitation leads to full system compromise, data breach, or complete security control bypass. Actively exploitable with publicly available techniques. | Must be remediated and re-tested within the engagement. No risk acceptance permitted for Critical findings. |
| **High** | 7.0 - 8.9 | Exploitation leads to significant unauthorized access, privilege escalation, or sensitive data exposure. Exploitation methodology well-understood. | Must be remediated and re-tested within the engagement or formally risk-accepted with compensating controls. |
| **Medium** | 4.0 - 6.9 | Exploitation requires specific conditions or user interaction. Impact is limited or contained by existing controls. | Should be remediated within the engagement. Risk acceptance with documented justification permitted. |
| **Low** | 0.1 - 3.9 | Minor security weakness with limited exploitation potential. Defense-in-depth improvement. | Documented for future remediation. Risk acceptance standard. |
| **Informational** | N/A | Security observation, best practice recommendation, or defense improvement suggestion. Not an exploitable vulnerability. | Documented for awareness. No remediation required. |

### Finding Communication Protocol

Findings move through the system via three communication mechanisms:

1. **Real-time channel (during Phase 3).** Offensive agents communicate findings to defensive agents through the established communication channel as they are discovered. This enables cooperative discussion and immediate understanding of the finding's impact.

2. **SARIF-formatted finding records (Phase 3 output).** All findings are persisted as SARIF v2.1.0 records in `skills/red-team/output/{engagement-id}/findings/`. This is the authoritative finding record.

3. **Consolidated finding synthesis report (Phase 4).** red-reporter aggregates all findings into a synthesis report that correlates related findings, prioritizes remediation, and provides the L0/L1/L2 view for different audiences.

### Agent-to-Agent Finding Routing

| Finding Source | Finding Target | Routing Logic |
|---------------|----------------|---------------|
| red-recon | eng-architect | Threat model gaps, missing attack surface coverage |
| red-recon | eng-infra | Exposed infrastructure, misconfigured services |
| red-vuln | eng-devsecops | Scanning tool misses, vulnerability detection gaps |
| red-vuln | eng-backend / eng-frontend | Specific CVEs in implementation dependencies |
| red-exploit | eng-security | Exploitation of code patterns, auth/authz bypass |
| red-exploit | eng-backend / eng-frontend | Implementation-level vulnerabilities |
| red-privesc | eng-backend | Privilege escalation through application logic |
| red-privesc | eng-infra | Privilege escalation through infrastructure misconfiguration |
| red-lateral | eng-infra | Network segmentation failures, containment bypass |
| red-lateral | eng-incident | Internal movement detection gaps |
| red-persist | eng-incident | Persistence detection failures, indicator removal success |
| red-exfil | eng-incident | DLP bypass, exfiltration channel detection failures |
| red-social | eng-architect | Human attack vector gaps in threat model |
| red-infra | eng-devsecops | C2 detection gaps in pipeline security monitoring |

**Evidence basis:** AD-006 (SARIF v2.1.0 normalization, S-002, 2026-02-22); C-003 (common Finding schema with 12 fields, 2026-02-22); S-002 Data Interchange Formats (SARIF for findings, 2026-02-22).

---

## Remediation Tracking and Verification Loop

### Remediation Lifecycle

The remediation tracking system ensures every finding follows a deterministic path from discovery to closure. The system operates as a closed loop: no finding is closed without verification by the originating offensive agent.

```
+------------------+     +------------------+     +------------------+
|   FINDING        |     |   REMEDIATION    |     |   VERIFICATION   |
|   DISCOVERY      | --> |   IMPLEMENTATION | --> |   RE-TEST        |
|   (red-team)     |     |   (eng-team)     |     |   (red-team)     |
+------------------+     +------------------+     +------------------+
                                                         |
                                     +-------------------+-------------------+
                                     |                   |                   |
                              VERIFIED_CLOSED    PARTIALLY_REMEDIATED   NOT_REMEDIATED
                                     |                   |                   |
                              Finding closed    Returns to remediation  Escalated priority
                                                with revised plan      Returns to remediation
```

### Tracking Data Model

Each finding is tracked with the following remediation metadata:

| Field | Type | Description |
|-------|------|-------------|
| `finding_id` | string | Unique finding identifier (`PT-NNNN-FFF`) |
| `status` | enum | `discovered`, `triaged`, `assigned`, `in_remediation`, `re_tested`, `verified_closed`, `partially_remediated`, `not_remediated`, `risk_accepted` |
| `severity` | enum | `critical`, `high`, `medium`, `low`, `informational` |
| `discovered_by` | string | Red-team agent that discovered the finding |
| `assigned_to` | string | Eng-team agent responsible for remediation |
| `discovery_date` | datetime | When the finding was discovered |
| `assignment_date` | datetime | When the finding was assigned for remediation |
| `remediation_date` | datetime | When the fix was implemented |
| `retest_date` | datetime | When the re-test was performed |
| `closure_date` | datetime | When the finding reached terminal state |
| `remediation_cycles` | integer | Number of remediation-retest iterations |
| `attack_technique` | string | MITRE ATT&CK technique ID used in discovery |
| `retest_technique` | string | MITRE ATT&CK technique ID used in re-test (same as discovery) |
| `ssdf_practice` | string | NIST SSDF practice reference for the remediation activity |
| `evidence_refs` | list[string] | References to evidence artifacts in the evidence vault |

### Verification Rules

The following rules govern the verification loop:

| Rule ID | Rule | Rationale |
|---------|------|-----------|
| VR-001 | The originating red-team agent MUST perform the re-test. No other agent may verify closure. | The discovering agent has the deepest understanding of the exploitation technique and can most accurately assess whether the fix addresses the root cause vs. merely addressing the specific exploit path. |
| VR-002 | Re-tests MUST use the same ATT&CK technique as the original finding, plus at least one variant technique from the same tactic. | Prevents narrow fixes that address only the specific exploit path while leaving the underlying vulnerability exploitable through variant techniques. |
| VR-003 | Critical findings MUST be verified closed before the engagement can proceed to Phase 6. No risk acceptance is permitted for Critical findings. | Critical findings represent full system compromise. Risk acceptance at this severity is not a valid remediation path. |
| VR-004 | High findings MUST be verified closed or formally risk-accepted with compensating controls before the engagement can proceed to Phase 6. | High findings represent significant security impact. Formal risk acceptance with documented compensating controls is an acceptable alternative to full remediation. |
| VR-005 | A finding that returns NOT_REMEDIATED after the second re-test cycle MUST be escalated to eng-architect for root cause analysis. | Repeated remediation failure indicates a design-level issue rather than an implementation-level issue. Architectural review may be required. |
| VR-006 | All re-test results MUST be documented as SARIF finding updates in the evidence vault. | Ensures complete audit trail of the remediation verification process. |

### Remediation Metrics

The following metrics are tracked across the engagement and reported in the Phase 6 closure report:

| Metric | Definition | Target |
|--------|-----------|--------|
| **Finding Resolution Rate** | Percentage of findings that reached VERIFIED_CLOSED status | >= 90% for Critical + High |
| **Mean Time to Remediate (MTTR)** | Average time from finding discovery to VERIFIED_CLOSED | Tracked per severity level; no fixed target (engagement-dependent) |
| **Remediation Cycle Count** | Average number of remediation-retest iterations per finding | <= 2 (lower indicates higher remediation quality) |
| **Risk Acceptance Rate** | Percentage of findings resolved through risk acceptance | <= 10% for High severity; 0% for Critical |
| **Root Cause Distribution** | Distribution of findings by root cause category (design, implementation, configuration, detection) | Tracked for trend analysis across engagements |
| **ATT&CK Coverage** | Percentage of authorized ATT&CK techniques that were tested | >= 80% of authorized techniques |

**Evidence basis:** ADR-PROJ010-006 Section 7 (Audit Trail Requirements, 2026-02-22); F-002 Pattern 3 (Post-Execution Audit Verification, 2026-02-22); eng-team SKILL.md (eng-reviewer final gate, 2026-02-22).

---

## Adversary Integration

### /adversary Skill Role in Purple Team Exercises

The /adversary skill provides independent quality validation of purple team exercise deliverables. Its role is to ensure that findings, remediation plans, and engagement reports meet the quality standards defined in quality-enforcement.md.

All purple team exercises are classified as C4 criticality because they involve cross-skill orchestration of both offensive and defensive agents with irreversible security implications. C4 criticality requires all 10 selected strategies from the strategy catalog.

### Quality Gate Application Points

/adversary quality gates apply at four points during a purple team exercise:

| Gate Point | Phase | What Is Scored | Quality Target | Required Strategies |
|-----------|-------|----------------|----------------|---------------------|
| **Baseline Quality Gate** | Phase 2 (Defensive Baseline) | eng-team baseline artifacts (threat models, implementations, configs) | >= 0.95 | All 10 (C4) |
| **Finding Synthesis Gate** | Phase 4 (Finding Synthesis) | red-reporter consolidated finding synthesis report | >= 0.95 | All 10 (C4) |
| **Verification Gate** | Phase 5 (Verification) | Remediation effectiveness and re-test completeness | >= 0.95 | All 10 (C4) |
| **Final Report Gate** | Phase 6 (Closure) | Final engagement report (L0/L1/L2) | >= 0.95 | All 10 (C4) |

### Scoring Dimensions

The S-014 LLM-as-Judge scoring rubric from quality-enforcement.md applies with the standard 6-dimension weighting. For purple team exercises, the dimensions have specific interpretations:

| Dimension | Weight | Purple Team Interpretation |
|-----------|--------|---------------------------|
| **Completeness** | 0.20 | All integration points tested; all authorized ATT&CK techniques exercised; all findings documented; all remediation plans address root causes |
| **Internal Consistency** | 0.20 | Findings, remediation plans, re-test results, and closure report tell a coherent narrative; no contradictions between offensive findings and defensive assessments |
| **Methodological Rigor** | 0.20 | Offensive techniques follow PTES/OSSTMM methodology; defensive remediation follows SSDF practices; threat modeling uses appropriate criticality-based methodology per AD-009 |
| **Evidence Quality** | 0.15 | All findings supported by tool output, ATT&CK technique references, and SARIF-formatted evidence; no unsubstantiated claims; confidence levels accurately reflect evidence strength |
| **Actionability** | 0.15 | Remediation guidance is specific, implementable, and verifiable; re-test criteria are defined for every finding; risk acceptance decisions include compensating controls |
| **Traceability** | 0.10 | Findings trace to ATT&CK techniques; remediation traces to SSDF practices; engagement report traces to scope document; audit trail is complete and tamper-evident |

### Strategy Application

For C4 purple team exercises, all 10 selected strategies apply. The following table maps each strategy to its specific application within the purple team context:

| Strategy | ID | Application in Purple Team |
|----------|----|---------------------------|
| LLM-as-Judge | S-014 | Quantitative scoring of all gate deliverables using the 6-dimension rubric |
| Steelman Technique | S-003 | Strengthen eng-team's defensive approach before red-team critiques it (H-16: steelman before critique) |
| Inversion Technique | S-013 | Identify what would make the engagement fail; design exercises to prevent those failure modes |
| Constitutional AI Critique | S-007 | Verify that all engagement activities comply with Jerry Constitution, scope constraints, and PROJ-010 requirements |
| Devil's Advocate | S-002 | Challenge assumptions in both offensive findings and defensive remediation plans; applied after steelman per H-16 |
| Pre-Mortem Analysis | S-004 | Before Phase 3, identify likely engagement failure modes (scope boundary issues, finding communication gaps, remediation cycle bottlenecks) |
| Self-Refine | S-010 | Every agent self-reviews output before handoff per H-15 |
| FMEA | S-012 | Failure mode analysis on the purple team protocol itself: what can go wrong at each phase transition, and what are the mitigations |
| Chain-of-Verification | S-011 | Verify that finding evidence chains are unbroken from discovery through remediation to closure |
| Red Team Analysis | S-001 | Apply adversarial thinking to the purple team protocol itself: how could the protocol be gamed or circumvented |

### eng-reviewer as /adversary Orchestrator

Within purple team exercises, eng-reviewer serves as the orchestration point for /adversary integration. eng-reviewer invokes /adversary scoring at each quality gate point and determines whether the gate is passed or the deliverable is rejected per H-13 (quality threshold >= 0.92 for C2+; >= 0.95 for PROJ-010 per R-013).

eng-reviewer maintains the quality score history across gate points, enabling trend analysis:

| Metric | Definition |
|--------|-----------|
| **Gate Pass Rate** | Percentage of deliverables that pass the quality gate on first submission |
| **Revision Depth** | Average number of creator-critic-revision cycles per deliverable (H-14 minimum 3) |
| **Score Trajectory** | Quality score progression across revision iterations |
| **Dimension Gap Analysis** | Identification of consistently low-scoring dimensions for process improvement |

**Evidence basis:** quality-enforcement.md (C4 criticality requires all 10 strategies, quality threshold >= 0.92, 2026-02-22); eng-team SKILL.md (eng-reviewer /adversary integration at >= 0.95, 2026-02-22); quality-enforcement.md Strategy Catalog (S-001 through S-014, 2026-02-22).

---

## Output Level Specifications

### L0: Executive Summary

**Audience:** Engagement managers, leadership, compliance officers, non-technical stakeholders.

**Purpose:** Answers "What does this mean for the organization's security posture?"

**Content Requirements:**

| Element | Description |
|---------|-------------|
| Engagement overview | Scope, duration, integration points tested |
| Key finding summary | Number of findings by severity; top 3 most impactful findings in plain language |
| Remediation status | Finding resolution rate; number of Critical/High findings closed vs. risk-accepted |
| Security posture assessment | Qualitative assessment of defensive capability against tested attack techniques |
| Risk summary | Residual risk after remediation; risk-accepted findings with compensating controls |
| Recommendation summary | Top 3 prioritized actions for security improvement |

**Format:** Narrative markdown with summary tables. Maximum 2 pages equivalent. No technical jargon. All findings described in terms of business impact, not technical mechanism.

### L1: Technical Detail

**Audience:** Security engineers, developers, DevSecOps practitioners, incident responders.

**Purpose:** Provides implementation-specific technical content with code examples, configuration guidance, and specific remediation steps.

**Content Requirements:**

| Element | Description |
|---------|-------------|
| Full finding inventory | Complete SARIF-formatted finding records with ATT&CK technique IDs, CVE references, CWE mappings |
| Exploitation methodology | Step-by-step methodology for each finding (PTES/OSSTMM framework, not weaponized exploit code) |
| Remediation guidance | Specific code changes, configuration updates, or architectural modifications with implementation examples |
| Re-test results | Complete re-test records with SARIF updates, verification status, and variant technique results |
| ATT&CK coverage map | Technique-level coverage analysis: tested vs. blocked vs. succeeded |
| Tool output | Referenced tool outputs stored in evidence vault |
| Detection recommendations | Specific detection rule additions, monitoring configuration changes, and alerting threshold adjustments |

**Format:** Structured markdown with code blocks, SARIF excerpts, and cross-references to evidence vault artifacts. Length as needed for complete technical coverage.

### L2: Strategic Implications

**Audience:** Architecture and governance reviewers, security strategy planners, framework designers.

**Purpose:** Trade-off analysis, long-term security posture evolution, and architectural implications of findings.

**Content Requirements:**

| Element | Description |
|---------|-------------|
| Architectural pattern analysis | Findings grouped by architectural root cause; systemic patterns identified across multiple findings |
| Defense-in-depth assessment | Evaluation of which defense layers held, which failed, and where defense-in-depth gaps exist |
| Maturity assessment | OWASP SAMM maturity scoring for relevant security practices, with improvement recommendations |
| Threat landscape alignment | Assessment of defensive posture against the current threat landscape (informed by red-recon intelligence) |
| Long-term recommendations | Architectural changes, process improvements, and capability investments for sustainable security improvement |
| Purple team protocol assessment | Lessons learned about the purple team process itself; protocol improvements for future exercises |
| Measurement framework | Metrics for tracking security posture improvement across multiple engagement cycles |

**Format:** Analytical markdown with trend analysis, comparison tables, and strategic recommendation frameworks. Cross-references to ADR decisions affected by findings.

---

## L2: Strategic Implications

### Long-Term Value of Purple Team Integration

The purple team integration framework delivers compounding value across successive engagement cycles. Each cycle produces:

1. **Hardening velocity.** Measured improvement in finding resolution rate and reduction in Critical/High findings per cycle. As eng-team internalizes remediation patterns, fewer vulnerabilities reach the offensive assessment phase.

2. **Detection maturity.** Each IR validation exercise (Integration Point 4) identifies detection gaps. Successive exercises show measurable improvement in detection coverage as eng-incident refines monitoring and response capabilities.

3. **Threat model accuracy.** Each threat-informed architecture exercise (Integration Point 1) calibrates eng-architect's threat models against real adversary TTPs. Over time, threat models become predictive rather than reactive.

4. **Cross-skill efficiency.** As the handoff mechanisms mature, the time from finding discovery to remediation verification decreases. The communication channel and SARIF standardization reduce friction in the finding flow.

### Purple Team Maturity Model

Organizations progress through four maturity levels in their purple team practice. Each level builds on the previous:

| Level | Name | Characteristics | Entry Criteria |
|-------|------|-----------------|----------------|
| **Level 1: Initial** | Ad-hoc purple team exercises with basic finding documentation | Single integration point tested; manual finding tracking; basic SARIF compliance; L1 output only | Purple team scope document created; at least one integration point exercised |
| **Level 2: Defined** | Structured exercises with standardized finding flow and remediation tracking | All 4 integration points testable; full SARIF compliance; remediation tracking with re-test verification; L0 + L1 output | >= 3 engagements completed; finding resolution rate >= 80% for Critical + High |
| **Level 3: Measured** | Quantitative tracking across engagement cycles with trend analysis | Cross-engagement metrics; SAMM maturity scoring; ATT&CK coverage tracking; defense-in-depth assessment; L0 + L1 + L2 output | >= 5 engagements completed; finding resolution rate >= 90%; MTTR trending downward |
| **Level 4: Optimized** | Continuous improvement with predictive security posture management | Hardening velocity tracked; detection maturity measured; threat model accuracy validated; purple team protocol self-assessed and refined; /adversary scoring at all gate points | >= 10 engagements completed; zero Critical findings persisting across cycles; SAMM Level 2+ on all relevant practices |

### Measurement Framework

The following metrics framework enables tracking of purple team effectiveness across engagement cycles:

#### Leading Indicators (Predictive)

| Metric | Definition | Measurement Method |
|--------|-----------|-------------------|
| Threat Model Coverage | Percentage of real adversary TTPs covered by eng-architect threat models | red-recon TTP mapping vs. eng-architect STRIDE/DREAD coverage |
| Defensive Baseline Quality | Average /adversary quality score for baseline artifacts | S-014 scoring at Phase 2 gate |
| ATT&CK Technique Authorization | Breadth of authorized techniques per engagement | Scope document technique_allowlist count vs. total ATT&CK enterprise techniques |

#### Lagging Indicators (Outcome)

| Metric | Definition | Measurement Method |
|--------|-----------|-------------------|
| Finding Resolution Rate | Percentage of Critical + High findings reaching VERIFIED_CLOSED | Remediation tracking system terminal state analysis |
| Mean Time to Remediate | Average elapsed time from discovery to VERIFIED_CLOSED | Remediation tracking timestamps |
| Repeat Finding Rate | Percentage of findings in current engagement that match patterns from prior engagements | Cross-engagement finding correlation by CWE, ATT&CK technique, and root cause category |
| Detection Gap Reduction | Change in detection gap count between successive IR validation exercises | Integration Point 4 detection_gap_analysis comparison across engagements |

#### Process Health Indicators

| Metric | Definition | Measurement Method |
|--------|-----------|-------------------|
| Gate Pass Rate | Percentage of deliverables passing /adversary quality gate on first submission | eng-reviewer quality gate tracking |
| Remediation Cycle Depth | Average number of remediation-retest iterations per finding | Remediation tracking cycle count |
| Scope Compliance Rate | Percentage of engagements with zero scope deviations | ADR-PROJ010-006 Layer 3 compliance report |
| Purple Team Protocol Adherence | Percentage of protocol phases executed per specification | Phase entry/exit criteria compliance audit |

### Architectural Evolution Implications

Purple team findings drive architectural evolution through three feedback mechanisms:

1. **ADR revision triggers.** Findings that reveal systemic architectural weaknesses trigger ADR revision proposals. For example, if Integration Point 3 consistently reveals auth/authz bypass patterns, this may trigger a revision to AD-009 (threat modeling methodology) to mandate LINDDUN analysis for authentication systems regardless of PII involvement.

2. **Agent capability refinement.** Findings that consistently appear at specific integration points indicate potential agent capability gaps. For example, if Integration Point 2 consistently reveals container escape paths that eng-infra's baseline does not address, this may indicate a need to expand eng-infra's container security capability domain.

3. **Deferred agent reconsideration.** Purple team exercise outcomes contribute to the reconsideration triggers for the 4 deferred agents (eng-threatintel, eng-compliance, red-opsec, red-cloud) defined in ADR-PROJ010-001 Section 4. For example, if /eng-team operates independently of /red-team in purple team exercises (OQ-003), this validates the eng-threatintel promotion trigger.

**Evidence basis:** A-002 Finding 7 (Netflix Attack Emulation Team measures "control confidence" through adversarial validation, 2026-02-22); ADR-PROJ010-001 Section 4 (Deferred Agents with Reconsideration Triggers, 2026-02-22); ADR-PROJ010-001 Consequences (purple team integration as positive consequence, 2026-02-22); OWASP SAMM v2.0 maturity progression model (owaspsamm.org).

---

## Compliance

### Jerry Framework Compliance

| Constraint | Status | Implementation |
|------------|--------|----------------|
| P-001: Truth and Accuracy | COMPLIANT | All findings evidence-based with ATT&CK citations, SARIF-formatted evidence, and confidence levels. No unsubstantiated claims. |
| P-002: File Persistence | COMPLIANT | All purple team artifacts persisted to engagement output directories. Finding records, remediation plans, re-test results, and engagement reports are file-persisted. |
| P-003: No Recursive Subagents (H-01) | COMPLIANT | Purple team protocol is orchestrated by the main context. Agents are workers; no agent invokes another agent. Cross-skill handoffs route through the orchestrator. |
| P-004: Explicit Provenance | COMPLIANT | All findings cite ATT&CK technique IDs, CVE references, and methodology standards. Remediation cites SSDF practices. Evidence chain is documented. |
| P-020: User Authority (H-02) | COMPLIANT | User authorizes scope document. Risk acceptance requires user sign-off. User can override any protocol decision. |
| P-022: No Deception (H-03) | COMPLIANT | Confidence levels honestly reported. Limitations disclosed. Standalone analysis marked as "unvalidated" per AD-010. |

### PROJ-010 Requirement Compliance

| Requirement | Status | Implementation |
|-------------|--------|----------------|
| R-001: Secure by Design | COMPLIANT | Purple team protocol inherits ADR-PROJ010-006 three-layer authorization. Scope enforcement is structural, not procedural. |
| R-013: C4 /adversary on Every Phase | COMPLIANT | /adversary quality gates at all four protocol gate points (baseline, finding synthesis, verification, final report). All 10 strategies required. |
| R-018: Real Offensive Techniques | COMPLIANT | Red-team agents use ATT&CK technique IDs. PTES/OSSTMM methodology. Finding records include technique-level attribution. |
| R-020: Authorization Verification | COMPLIANT | All offensive operations within signed scope document. Circuit breaker at every agent transition. Scope Oracle validates every action. |

### ADR Compliance

| ADR | Compliance | Implementation |
|-----|------------|----------------|
| ADR-PROJ010-001 | COMPLIANT | All 4 cross-skill integration points operationalized with defined handoff protocols, data exchange specifications, and agent routing. |
| ADR-PROJ010-006 | COMPLIANT | Three-layer authorization inherited. Purple team scope documents use `PT-NNNN` namespace. Circuit breaker enforcement at all agent transitions. Layer 3 scope compliance attestation at engagement closure. |

---

## References

### Architecture Decision Records

| ADR | Title | Relevance to This Document |
|-----|-------|---------------------------|
| [ADR-PROJ010-001](../../../decisions/ADR-PROJ010-001-agent-team-architecture.md) | Agent Team Architecture | 21-agent roster (AD-002); 4 cross-skill integration points (Section 5); 8-step eng-team workflow; non-linear red-team workflow; defense evasion model (Section 6); threat modeling methodology (AD-009); standalone design (AD-010); deferred agent triggers (Section 4) |
| [ADR-PROJ010-006](../../../decisions/ADR-PROJ010-006-authorization-scope-control.md) | Authorization & Scope Control | Three-layer authorization architecture (AD-004); 7 scope enforcement components; per-agent authorization model; audit trail requirements; OWASP Agentic AI Top 10 coverage; progressive autonomy model (AD-012); scope document specification |

### Architecture Decisions Referenced

| AD | Title | Usage in This Document |
|----|-------|----------------------|
| AD-001 | Methodology-First Design | Purple team exercises produce methodology guidance; agents guide practitioners, not autonomous exploitation |
| AD-004 | Three-Layer Authorization | Purple team scope enforcement inherits structural + dynamic + retrospective authorization layers |
| AD-006 | SARIF-Based Finding Normalization | All findings formatted in SARIF v2.1.0; common Finding schema with 12 fields |
| AD-008 | Layered SDLC Governance | Remediation plans reference SSDF practice IDs; baseline quality measured against SDLC governance layers |
| AD-009 | STRIDE+DREAD Threat Modeling | Integration Point 1 uses criticality-based methodology escalation for threat model assessment |
| AD-010 | Standalone Capable Design | All agents function without tools; findings from standalone analysis marked "unvalidated" |
| AD-011 | Agent Isolation Architecture | Purple team engagement isolation boundaries (VM-per-engagement, container-per-agent-group) |
| AD-012 | Progressive Autonomy Deployment | Purple team exercises operate at autonomy level appropriate to organizational maturity |

### Phase 1 Research Artifacts

| Artifact | Content | Citations in This Document |
|----------|---------|---------------------------|
| S-001 | Cross-Stream Findings Consolidation | Convergence 3 (scope over oversight); Conflict 2 resolution (Impact shared ownership) |
| S-002 | Architecture Implications Synthesis | Pattern 4 (Purple Team Cross-Skill routing); cross-skill integration point definitions; data interchange formats |
| A-002 | Red Team Organization Research | Finding 7 (Netflix Attack Emulation Team model); adversarial-collaborative dynamic validation |
| C-003 | Tool Integration Architecture | Common Finding schema (12 fields); SARIF normalization; common adapter interface |
| D-002 | LLM Capability Boundaries | Methodology-first design validation; LLMs excel at structured reasoning, not autonomous exploitation |
| F-002 | Security Architecture Patterns | Three-layer auth patterns; scope enforcement components; audit trail design; OWASP Agentic AI Top 10 |

### Skill References

| Skill | Version | Content |
|-------|---------|---------|
| [/eng-team SKILL.md](../../../../skills/eng-team/SKILL.md) | 1.0.0 | 10-agent roster; 8-step sequential workflow; state passing; layered SDLC governance; adversarial quality mode |
| [/red-team SKILL.md](../../../../skills/red-team/SKILL.md) | 1.0.0 | 11-agent roster; non-linear kill chain; mandatory authorization; circuit breaker integration; 4 cross-skill integration points |

### Standards References

| Standard | Version | Usage in This Document |
|----------|---------|----------------------|
| MITRE ATT&CK Enterprise | 2025 | Technique-level finding attribution; coverage analysis; tactic mapping per integration point |
| SARIF | v2.1.0 (OASIS) | Finding record format per AD-006; cross-tool interoperability |
| NIST SP 800-218 SSDF | v1.1 (2022) | Remediation traceability to governance framework practices |
| OWASP SAMM | v2.0 | Maturity model for purple team practice progression |
| PTES | Current | Offensive methodology framework for red-team exercises |
| OSSTMM | Current | Security testing methodology framework |
| CVSS | v3.1 | Severity classification alignment for finding severity scale |
| OWASP Agentic AI Top 10 | December 2025 | Risk taxonomy; scope enforcement validation against ASI01-ASI10 |

### Feature Traceability

| Feature | Title | Relationship |
|---------|-------|-------------|
| FEAT-040 | Purple Team Integration Framework | This document is the primary deliverable |
| FEAT-041 | /eng-team vs /red-team Gap Analysis | Consumes purple team findings for coverage gap identification |
| FEAT-042 | Hardening Cycle & Remediation | Implements the remediation tracking loop defined here |
| FEAT-043 | Portability Validation | Validates that purple team protocol works across LLM providers |
| FEAT-044 | Cross-Skill Integration Testing | Tests the 4 integration points defined here |

---

*Document Version: 1.0.0*
*Constitutional Compliance: Jerry Constitution v1.0*
*SSOT: ADR-PROJ010-001, ADR-PROJ010-006*
*Created: 2026-02-22*
