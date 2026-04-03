# Red-Team Engagement Scope: PROJ-021 Use Case Skills

> **Engagement ID:** RED-0001
> **Version:** 1.0
> **Classification:** Internal Security Assessment
> **Criticality:** C4 (irreversible -- framework integration gate)
> **Methodology:** PTES Pre-Engagement Interactions + NIST SP 800-115 Chapter 3
> **Date:** 2026-03-09
> **Created by:** red-lead
> **Status:** PENDING USER AUTHORIZATION

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Engagement overview, scope boundaries, timeline, risk summary |
| [L1: Technical Scope](#l1-technical-scope) | Target inventory, attack surface enumeration, methodology selection |
| [L2: Strategic Context](#l2-strategic-context) | Threat model, risk appetite, success criteria, coverage analysis |
| [Rules of Engagement](#rules-of-engagement) | Authorized and prohibited actions, escalation procedures |
| [Target Inventory](#target-inventory) | Complete file manifest for all assets under assessment |
| [Attack Surface Matrix](#attack-surface-matrix) | Surface-by-skill mapping with feasibility and priority |
| [Assessment Methodology](#assessment-methodology) | PTES phases, ATT&CK technique mapping, assessment procedures |
| [Success Criteria](#success-criteria) | What constitutes a finding vs. accepted risk |
| [Out of Scope](#out-of-scope) | Explicit exclusions |
| [Scope Document (YAML)](#scope-document-yaml) | Formal machine-readable scope for agent authorization |
| [S-010 Self-Review Checklist](#s-010-self-review-checklist) | Pre-delivery quality verification |

---

## L0: Executive Summary

### Engagement Overview

This red-team engagement authorizes an offensive security assessment of three new Jerry Framework skills -- `/use-case`, `/test-spec`, and `/contract-design` -- before they are integrated into the production framework. The engagement is scoped as an assessment-only review: document attack vectors, assess feasibility, and rate risk. No live exploitation, no payload generation, no persistent changes to target assets.

The three skills form a pipeline: `/use-case` produces structured use case artifacts, `/test-spec` transforms those artifacts into BDD test specifications, and `/contract-design` transforms them into OpenAPI 3.1 contracts. This pipeline topology means that a compromise in an upstream skill can propagate to all downstream skills -- making cross-skill trust boundary analysis a primary focus of this engagement.

### Scope Boundaries

- **IN SCOPE:** All files within `skills/use-case/`, `skills/test-spec/`, and `skills/contract-design/` directories. Agent definitions, governance YAML, composition files, templates, rules, schemas, sample files, contracts, and behavior tests. Cross-skill data flow trust boundaries.
- **OUT OF SCOPE:** Jerry Framework core, other skills (e.g., `/problem-solving`, `/adversary`, `/eng-team`), CI/CD infrastructure, runtime Claude Code platform, MCP servers, worktracker core logic. See [Out of Scope](#out-of-scope) for the full exclusion list.

### Timeline

| Phase | Duration | Activity |
|-------|----------|----------|
| Scope Definition (this document) | step-11b-scope | Define targets, attack surfaces, RoE, methodology |
| Vulnerability Analysis | step-11b-vuln | Execute assessment against authorized surfaces |
| Findings Report | step-11b-report | Compile findings, rate risk, recommend remediation |
| GATE-5b Evaluation | Post-report | Adversary loop + gate evaluation (threshold: 0.95) |

### Risk Summary

The engagement targets a documentation-generation pipeline operating within a trusted LLM framework. The skills do not execute arbitrary code against external systems, do not make network calls, and do not process untrusted external input in their intended operation. However, the LLM-mediated nature of the pipeline creates attack surfaces not present in traditional software: prompt injection via crafted artifacts, guardrail bypass through context manipulation, and trust boundary violations at skill handoff points. Three prior eng-security reviews (step-9, step-10, step-11) identified 23 total findings (0 Critical, 2 High, 6 Medium, 12 Low, 3 Informational). This red-team assessment focuses on attack vectors that static security review cannot detect -- specifically, adversarial input crafting, cross-skill pipeline poisoning, and behavioral guardrail bypass under pressure.

---

## L1: Technical Scope

### Skills Under Assessment

| Skill | Agents | Tool Tier | Model | Prior Gate Score | Prior Security Findings |
|-------|--------|-----------|-------|-----------------|------------------------|
| `/use-case` | uc-author (T2, integrative, Sonnet), uc-slicer (T2, systematic, Sonnet) | T2 | Sonnet | GATE-3: 0.956 | 7 (0C, 0H, 1M, 4L, 2I) |
| `/test-spec` | tspec-generator (T2, systematic, Sonnet), tspec-analyst (T2, convergent, Sonnet) | T2 | Sonnet | GATE-4: 0.957 | 9 (0C, 0H, 2M, 4L, 3I) |
| `/contract-design` | cd-generator (T2, convergent, Opus), cd-validator (T2, systematic, Sonnet) | T2 | Opus/Sonnet | GATE-5: 0.956 | 7 (0C, 2H, 3M, 2L, 0I) |

### Attack Surface Summary

Nine attack surfaces are identified across three categories:

**Category 1: Agent Behavioral Surfaces (LLM-specific)**
1. P-003 bypass vectors -- recursive subagent spawning
2. Content-abuse vectors -- harmful content generation via /use-case
3. Guardrail bypass -- forbidden action circumvention via prompt injection

**Category 2: Data Flow Surfaces (pipeline-specific)**
4. YAML frontmatter injection -- malicious frontmatter propagation
5. Template injection -- UC artifact field manipulation of OpenAPI output
6. Cross-skill pipeline poisoning -- upstream output corrupting downstream input

**Category 3: Control Mechanism Surfaces (framework-specific)**
7. Trigger map routing manipulation -- adversarial misrouting
8. Tool tier escalation -- T2 agents performing T3+ operations
9. PROTOTYPE label bypass -- x-prototype:true circumvention

### Methodology Selection Rationale

**Primary: PTES (Penetration Testing Execution Standard)**
- Pre-engagement interactions: this scope document (PTES Section I)
- Intelligence gathering: prior eng-security reviews serve as reconnaissance input
- Threat modeling: STRIDE-based threat model from step-11 architecture document
- Vulnerability analysis: assessment-only evaluation against all 9 attack surfaces
- Reporting: structured findings with CVSS scoring, CWE mapping, remediation

**Secondary: NIST SP 800-115 (Technical Guide to Information Security Testing)**
- Planning phase: scope definition, RoE establishment (Chapter 3)
- Assessment methodology: documentation review + security architecture review (Chapter 4)

**ATT&CK Mapping:** This engagement maps to the following ATT&CK for LLMs concepts (adapted from MITRE ATLAS):
- AML.T0043 (Craft Adversarial Data) -- crafted UC artifacts as adversarial input
- AML.T0040 (ML Supply Chain Compromise) -- pipeline poisoning via trusted artifact chain
- AML.T0051 (LLM Prompt Injection) -- guardrail bypass through embedded instructions
- AML.T0054 (LLM Meta Prompt Extraction) -- system prompt exfiltration via UC content fields

---

## L2: Strategic Context

### Threat Model

**Threat Actor Profile:** An internal user or collaborator with legitimate access to the Jerry Framework who crafts adversarial use case artifacts to exploit the UC-to-test-spec-to-contract pipeline. The attacker has full knowledge of the skill definitions, templates, and transformation rules (white-box assessment). The attacker's goal is one or more of:

1. **Guardrail circumvention:** Cause agents to violate constitutional constraints (P-003, P-020, P-022)
2. **Output corruption:** Produce malicious or misleading test specifications or API contracts
3. **Scope escape:** Cause agents to read/write files outside their authorized directories
4. **Pipeline poisoning:** Inject content in upstream artifacts that activates downstream vulnerabilities
5. **Label bypass:** Remove or circumvent the PROTOTYPE safety label on generated contracts

**Trust Boundaries:**

```
[User Input] --> [uc-author] --> [UC Artifact] --> [uc-slicer] --> [UC Artifact + slices/interactions]
                                                       |
                                    +------------------+------------------+
                                    |                                     |
                              [tspec-generator]                     [cd-generator]
                                    |                                     |
                              [Feature File]                      [OpenAPI Contract]
                                    |                                     |
                              [tspec-analyst]                       [cd-validator]
                                    |                                     |
                           [Coverage Report]                    [Validation Report]
```

Each arrow represents a trust boundary. The critical insight is that `/test-spec` and `/contract-design` both trust the UC artifact produced by `/use-case` without independent structural verification beyond JSON Schema validation. Schema validation catches structural defects but not semantic poisoning.

### Risk Appetite

| Risk Level | Appetite | Rationale |
|------------|----------|-----------|
| Critical findings | Zero tolerance | Must be resolved before GATE-5b |
| High findings | Low tolerance | Must be dispositioned (fix or accept-with-mitigation) before GATE-5b |
| Medium findings | Moderate tolerance | Must be documented; remediation plan required |
| Low findings | Acceptance permitted | Document and track for future hardening |

### Coverage Analysis Against Engagement Objectives

| Objective | Attack Surfaces Covering It | Prior eng-security Coverage | Red-Team Delta |
|-----------|---------------------------|---------------------------|----------------|
| Constitutional compliance (P-003/P-020/P-022) | AS-1, AS-3, AS-9 | Cross-file compliance matrices in all 3 reviews | Adversarial bypass attempts (not covered by static review) |
| Cross-skill data integrity | AS-4, AS-5, AS-6 | Trust boundary analysis in step-10 and step-11 | Active pipeline poisoning scenarios |
| Output path safety | AS-8, AS-5 | SEC-005 (step-9), SEC-002/SEC-004 (step-10), SEC-CD-005 (step-11) | Adversarial slug/path crafting beyond static pattern analysis |
| PROTOTYPE label integrity | AS-9 | SEC-CD-007 (step-11) | Bypass scenario enumeration |
| Routing integrity | AS-7 | Not covered by eng-security | Full coverage by red-team |
| Tool tier boundary | AS-8 | T2 tier verification in all 3 reviews | Adversarial escalation attempts |

---

## Rules of Engagement

### Authorized Actions

| Action | Authorization Level | Conditions |
|--------|-------------------|------------|
| Static analysis of all files in target inventory | Full | Read-only access to all listed files |
| Adversarial input crafting (document attack scenarios) | Full | Document the crafted input; do not execute against live agents |
| Cross-skill data flow analysis | Full | Trace data paths from /use-case through /test-spec and /contract-design |
| Guardrail effectiveness assessment | Full | Evaluate whether documented guardrails can be bypassed; document the vector |
| Schema validation boundary testing | Full | Assess what schema validation catches vs. what passes through |
| Template injection analysis | Full | Analyze template placeholders for injection vectors |
| Trigger map collision analysis | Full | Assess routing manipulation vectors between the three skills |
| PROTOTYPE label bypass enumeration | Full | Document all paths that could remove or bypass x-prototype:true |
| Prior finding validation | Full | Verify that eng-security findings are accurately scoped and prioritized |

### Prohibited Actions

| Action | Reason |
|--------|--------|
| Live exploitation against running agents | Assessment-only engagement; no active exploitation authorized |
| Modification of any target files | Red-team is read-only; remediation is a separate phase |
| Generation of exploit code or payloads | Assessment documents attack vectors; does not produce weaponized artifacts |
| Testing against framework core or other skills | Out of scope -- see [Out of Scope](#out-of-scope) |
| Network-based testing | Skills have no network surface; not applicable |
| Social engineering of human operators | Not applicable to this engagement type |
| Persistence mechanisms | Not applicable to this engagement type |
| Data exfiltration testing | Not applicable; skills process framework-internal artifacts only |

### Escalation Procedures

| Condition | Action |
|-----------|--------|
| Critical finding discovered | Immediate documentation; flag in findings report with CRITICAL severity; mandatory escalation to user before GATE-5b |
| Finding affects framework core (not just target skills) | Document finding; flag as OUT_OF_SCOPE_ESCALATION; recommend separate engagement for framework-level assessment |
| Scope ambiguity (target file unclear) | Apply H-31: ask user for clarification before including in assessment |
| Assessment blocked by missing information | Document blocker; proceed with available information; note confidence reduction |

### Emergency Stop Conditions

| Condition | Response |
|-----------|----------|
| Assessment discovers active exploitation in progress | Halt assessment; escalate to user immediately |
| Target files are modified by another process during assessment | Halt assessment on affected files; re-read files; resume after confirming stable state |

### Communication Channel

All findings communicated via the structured findings report at `security/red-team-report.md`. Intermediate status via orchestration worktracker updates.

---

## Target Inventory

### /use-case Skill (15 files)

| # | File | Type | Security Relevance |
|---|------|------|-------------------|
| 1 | `skills/use-case/agents/uc-author.md` | Agent definition | System prompt, guardrails, forbidden actions, tool declarations |
| 2 | `skills/use-case/agents/uc-author.governance.yaml` | Governance metadata | Tool tier, constitutional compliance, forbidden actions (NPT-009) |
| 3 | `skills/use-case/agents/uc-slicer.md` | Agent definition | System prompt, guardrails, input validation gates, lifecycle management |
| 4 | `skills/use-case/agents/uc-slicer.governance.yaml` | Governance metadata | Tool tier, constitutional compliance, forbidden actions (NPT-009) |
| 5 | `skills/use-case/composition/uc-author.agent.yaml` | Composition config | Runtime agent configuration, tool list |
| 6 | `skills/use-case/composition/uc-author.prompt.md` | Composition prompt | System prompt copy (drift risk -- SEC-007 from step-9) |
| 7 | `skills/use-case/composition/uc-slicer.agent.yaml` | Composition config | Runtime agent configuration, tool list |
| 8 | `skills/use-case/composition/uc-slicer.prompt.md` | Composition prompt | System prompt copy (drift risk) |
| 9 | `skills/use-case/templates/use-case-brief.template.md` | Template | BRIEFLY_DESCRIBED level template |
| 10 | `skills/use-case/templates/use-case-casual.template.md` | Template | BULLETED_OUTLINE level template |
| 11 | `skills/use-case/templates/use-case-realization.template.md` | Template | ESSENTIAL_OUTLINE / FULLY_DESCRIBED template |
| 12 | `skills/use-case/templates/use-case-slice.template.md` | Template | Slice document template |
| 13 | `skills/use-case/rules/use-case-writing-rules.md` | Rules | Cockburn 12-step process, UC 2.0 lifecycle, INVEST criteria |
| 14 | `skills/use-case/tests/BEHAVIOR_TESTS.md` | Tests | BDD behavior test specification |
| 15 | `skills/use-case/samples/sample-use-case.md` | Sample | Example output artifact |

### /test-spec Skill (14 files)

| # | File | Type | Security Relevance |
|---|------|------|-------------------|
| 16 | `skills/test-spec/SKILL.md` | Skill definition | Routing keywords, description, agent inventory |
| 17 | `skills/test-spec/agents/tspec-generator.md` | Agent definition | System prompt, Clark algorithm, guardrails, input validation |
| 18 | `skills/test-spec/agents/tspec-generator.governance.yaml` | Governance metadata | Tool tier, constitutional compliance, forbidden actions |
| 19 | `skills/test-spec/agents/tspec-analyst.md` | Agent definition | System prompt, 7 Cs framework, coverage computation |
| 20 | `skills/test-spec/agents/tspec-analyst.governance.yaml` | Governance metadata | Tool tier, constitutional compliance, forbidden actions |
| 21 | `skills/test-spec/composition/tspec-generator.agent.yaml` | Composition config | Runtime agent configuration |
| 22 | `skills/test-spec/composition/tspec-analyst.agent.yaml` | Composition config | Runtime agent configuration |
| 23 | `skills/test-spec/composition/tspec-generator.prompt.md` | Composition prompt | System prompt copy |
| 24 | `skills/test-spec/composition/tspec-analyst.prompt.md` | Composition prompt | System prompt copy |
| 25 | `skills/test-spec/templates/bdd-scenario.template.md` | Template | Gherkin BDD Feature file template |
| 26 | `skills/test-spec/templates/test-plan.template.md` | Template | Coverage report template |
| 27 | `skills/test-spec/rules/clark-transformation-rules.md` | Rules | Clark (2018) UC2.0-to-Gherkin mapping algorithm (22 rules) |
| 28 | `skills/test-spec/tests/BEHAVIOR_TESTS.md` | Tests | BDD behavior test specification |
| 29 | `skills/test-spec/samples/sample-test-specification.md` | Sample | Example output artifact |

### /contract-design Skill (17 files)

| # | File | Type | Security Relevance |
|---|------|------|-------------------|
| 30 | `skills/contract-design/SKILL.md` | Skill definition | Routing keywords, description, agent inventory |
| 31 | `skills/contract-design/agents/cd-generator.md` | Agent definition | System prompt, UC-to-contract algorithm, guardrails |
| 32 | `skills/contract-design/agents/cd-generator.governance.yaml` | Governance metadata | Tool tier, constitutional compliance, forbidden actions |
| 33 | `skills/contract-design/agents/cd-validator.md` | Agent definition | System prompt, 9-step validation protocol, guardrails |
| 34 | `skills/contract-design/agents/cd-validator.governance.yaml` | Governance metadata | Tool tier, constitutional compliance, forbidden actions |
| 35 | `skills/contract-design/composition/cd-generator.agent.yaml` | Composition config | Runtime agent configuration |
| 36 | `skills/contract-design/composition/cd-validator.agent.yaml` | Composition config | Runtime agent configuration |
| 37 | `skills/contract-design/composition/cd-generator.prompt.md` | Composition prompt | System prompt copy |
| 38 | `skills/contract-design/composition/cd-validator.prompt.md` | Composition prompt | System prompt copy |
| 39 | `skills/contract-design/templates/openapi-template.yaml` | Template | OpenAPI 3.1 scaffold with placeholders |
| 40 | `skills/contract-design/templates/asyncapi-template.yaml` | Template | Deferred AsyncAPI template (SEC-CD-004 risk) |
| 41 | `skills/contract-design/templates/cloudevents-template.yaml` | Template | Deferred CloudEvents template (SEC-CD-004 risk) |
| 42 | `skills/contract-design/templates/json-schema-template.json` | Template | JSON Schema template |
| 43 | `skills/contract-design/rules/uc-to-contract-rules.md` | Rules | UC-to-OpenAPI transformation algorithm (22 rules) |
| 44 | `skills/contract-design/contracts/CD_SKILL_CONTRACT.yaml` | Contract | Skill contract definition |
| 45 | `skills/contract-design/tests/BEHAVIOR_TESTS.md` | Tests | BDD behavior test specification |
| 46 | `skills/contract-design/samples/sample-contract.openapi.yaml` | Sample | Example output artifact |

### Cross-Skill Reference Artifacts (assessed for trust boundary analysis)

| # | File | Type | Security Relevance |
|---|------|------|-------------------|
| 47 | Prior security review: step-9-eng-security-review.md | Reference | /use-case findings baseline |
| 48 | Prior security review: step-10-eng-security-review.md | Reference | /test-spec findings baseline |
| 49 | Prior security review: step-11-eng-security-review.md | Reference | /contract-design findings baseline |

**Total target files: 46 primary + 3 reference = 49**

---

## Attack Surface Matrix

### Surface-by-Skill Mapping

| # | Attack Surface | /use-case | /test-spec | /contract-design | Priority | Feasibility |
|---|---------------|-----------|------------|-----------------|----------|-------------|
| AS-1 | P-003 bypass (recursive subagent spawning) | uc-author, uc-slicer | tspec-generator, tspec-analyst | cd-generator, cd-validator | P1 | Low -- all agents are T2 without Task tool; structural enforcement prevents delegation |
| AS-2 | Content-abuse (harmful content generation) | uc-author (primary) | tspec-generator (derived) | cd-generator (derived) | P2 | Medium -- uc-author accepts freeform user descriptions; content flows downstream |
| AS-3 | Guardrail bypass via prompt injection | All agents | All agents | All agents | P0 | Medium -- crafted UC artifact content could embed instructions that override agent guardrails |
| AS-4 | YAML frontmatter injection | uc-author (producer) | tspec-generator (consumer) | cd-generator (consumer) | P0 | Medium -- UC artifacts with crafted frontmatter fields could inject unexpected metadata |
| AS-5 | Template injection | -- | tspec-generator (template consumer) | cd-generator (template consumer) | P1 | Medium -- UC field values populate template placeholders; injection possible at substitution points |
| AS-6 | Cross-skill pipeline poisoning | uc-slicer (exit point) | tspec-generator (entry point) | cd-generator (entry point) | P0 | Medium -- trusted artifact chain means downstream skills inherit upstream compromises |
| AS-7 | Trigger map routing manipulation | All (routing target) | All (routing target) | All (routing target) | P2 | Low -- trigger map uses keyword matching with negative keywords; manipulation requires specific keyword collision |
| AS-8 | Tool tier escalation (T2 to T3+) | uc-author, uc-slicer | tspec-generator, tspec-analyst | cd-generator, cd-validator | P1 | Low -- tool list is declarative in YAML frontmatter; Claude Code enforces tool restrictions |
| AS-9 | PROTOTYPE label bypass | -- | -- | cd-generator, cd-validator | P1 | Medium -- multiple paths to circumvent x-prototype:true (SEC-CD-007 baseline) |

### Priority Definitions

| Priority | Definition | Assessment Depth |
|----------|-----------|-----------------|
| P0 | Critical path -- finding could compromise pipeline integrity | Full scenario development, multi-step attack chain analysis |
| P1 | Significant -- finding could compromise individual skill integrity | Scenario development, feasibility assessment |
| P2 | Notable -- finding could cause misuse or degraded operation | Vector documentation, feasibility estimate |

---

## Assessment Methodology

### PTES Phases Applicable

| PTES Phase | Applicability | Activities |
|------------|--------------|------------|
| I. Pre-Engagement | **This document** | Scope definition, RoE, target inventory, methodology selection |
| II. Intelligence Gathering | Completed (prior reviews) | eng-security reviews serve as passive reconnaissance; all 23 findings are input to vulnerability analysis |
| III. Threat Modeling | Completed (architecture) | STRIDE analysis from step-11 architecture document; threat actor profile defined in L2 above |
| IV. Vulnerability Analysis | **step-11b-vuln** | Assessment against all 9 attack surfaces per the assessment procedures below |
| V. Exploitation | **NOT AUTHORIZED** | Assessment-only engagement -- no live exploitation |
| VI. Post-Exploitation | **NOT APPLICABLE** | No exploitation means no post-exploitation |
| VII. Reporting | **step-11b-report** | Structured findings report with CVSS, CWE, remediation recommendations |

### Assessment Procedures by Attack Surface

**AS-1: P-003 Bypass Vectors**
- Procedure: Review all 6 agent definitions for Task tool presence in YAML frontmatter `tools` list. Review composition YAML for Task tool. Review governance YAML forbidden_actions for P-003 entries. Assess whether freeform user input could instruct agents to invoke Task indirectly (e.g., via Bash).
- Evidence: Tool list audit, forbidden action audit, Bash command pattern analysis.

**AS-2: Content-Abuse Vectors**
- Procedure: Assess uc-author's input validation gates. Determine whether harmful content (violence, illegal activity descriptions, PII) could be embedded in use case titles, actor descriptions, flow steps, or extension conditions. Trace whether such content propagates unchanged through tspec-generator and cd-generator.
- Evidence: Input validation rule analysis, content propagation trace through pipeline.

**AS-3: Guardrail Bypass via Prompt Injection**
- Procedure: Analyze each freeform text field in the UC artifact schema (title, actor descriptions, flow step actions, extension conditions, interaction descriptions). Assess whether crafted content in these fields could embed instructions that override agent guardrails when the agent reads the artifact. Focus on fields that are processed by downstream agents.
- Evidence: Schema field enumeration, agent processing logic analysis, injection vector categorization.

**AS-4: YAML Frontmatter Injection**
- Procedure: Assess whether a UC artifact with crafted YAML frontmatter fields (including fields not defined in the schema but permitted by `additionalProperties: true`) could influence downstream agent behavior. Assess schema validation coverage for each field type.
- Evidence: Schema additionalProperties analysis, downstream field consumption analysis.

**AS-5: Template Injection**
- Procedure: Analyze OpenAPI template (`openapi-template.yaml`) and BDD template (`bdd-scenario.template.md`) placeholder patterns. Determine whether UC artifact field values could inject YAML structure, Gherkin keywords, or Markdown formatting that alters the semantic meaning of generated output.
- Evidence: Template placeholder audit, substitution point analysis, injection scenario construction.

**AS-6: Cross-Skill Pipeline Poisoning**
- Procedure: Trace data flow from uc-author output through uc-slicer to tspec-generator and cd-generator. Identify which fields are trusted without independent validation. Assess whether poisoned field values survive schema validation at each skill boundary.
- Evidence: End-to-end data flow trace, schema validation coverage at each boundary, field trust analysis.

**AS-7: Trigger Map Routing Manipulation**
- Procedure: Analyze trigger map entries for /use-case, /test-spec, and /contract-design. Identify keyword collisions with other skills. Test whether adversarial phrasing could route requests to the wrong skill or suppress intended routing.
- Evidence: Trigger map collision analysis, negative keyword effectiveness assessment.

**AS-8: Tool Tier Escalation**
- Procedure: Verify that all 6 agents are correctly constrained to T2 tools. Assess whether Bash tool access (present in all agents) could be leveraged to perform T3+ operations (web requests, MCP calls). Assess whether crafted input could cause agents to attempt operations beyond their tier.
- Evidence: Tool list audit per agent, Bash execution surface analysis, escalation scenario assessment.

**AS-9: PROTOTYPE Label Bypass**
- Procedure: Enumerate all paths by which x-prototype:true could be removed from a generated contract. Assess cd-generator's output constraints, cd-validator's Step 7 enforcement, and template-level enforcement. Assess whether a crafted UC artifact could cause cd-generator to omit the label.
- Evidence: PROTOTYPE enforcement audit across cd-generator, cd-validator, and template; bypass scenario enumeration.

---

## Success Criteria

### What Constitutes a Finding

A finding is a documented attack vector that meets ALL of the following:

| Criterion | Definition |
|-----------|-----------|
| Identified vector | A specific, reproducible method of exploitation or abuse |
| Affected asset | One or more files in the target inventory |
| Impact assessment | Documented consequence (confidentiality, integrity, availability, or governance impact) |
| Feasibility rating | Low / Medium / High based on attacker effort and preconditions |
| CVSS score | Scored using CVSS 3.1 base metrics |
| CWE mapping | Mapped to the most specific applicable CWE identifier |

### What Constitutes Accepted Risk

An accepted risk is a documented attack vector where ALL of the following apply:

| Criterion | Definition |
|-----------|-----------|
| Impact is Low or Informational severity | CVSS base score < 4.0 |
| Compensating controls exist | At least one mitigating factor documented |
| Residual risk is documented | Risk after compensating controls is explicitly stated |
| Acceptance is traceable | Documented in findings report with rationale |

### Deduplication with Prior Findings

This engagement MUST NOT duplicate findings already documented in the three prior eng-security reviews. For each attack surface, the assessment will:

1. Reference the prior finding ID (e.g., SEC-001 from step-9) if the eng-security review already covers the vector
2. Assess whether the prior finding's severity rating and remediation recommendation are accurate from a red-team perspective
3. Identify any additional attack vectors NOT covered by the prior review
4. Document the delta between eng-security static analysis and red-team adversarial assessment

Prior findings that are confirmed as accurately scoped and rated will be referenced, not re-documented. New findings that extend or contradict prior assessments will be documented as new findings with cross-references.

### Gate Criteria (GATE-5b)

| Criterion | Threshold |
|-----------|-----------|
| No unresolved CRITICAL findings | Zero tolerance |
| All HIGH findings dispositioned | Fix or accept-with-documented-mitigation |
| All MEDIUM findings documented with remediation plan | Remediation plan required; immediate fix not required for gate |
| Findings report passes C4 adversary loop | Score >= 0.95 |

---

## Out of Scope

### Explicit Exclusions

| Exclusion | Rationale |
|-----------|-----------|
| Jerry Framework core (`src/`, `docs/governance/`, `.context/rules/`) | Separate engagement required; framework-level assessment has different risk profile |
| Other skills (`/problem-solving`, `/adversary`, `/eng-team`, `/nasa-se`, etc.) | Not part of PROJ-021; assessment scoped to the three new skills only |
| CI/CD infrastructure (GitHub Actions, pre-commit hooks) | Infrastructure testing requires separate authorization |
| Claude Code runtime platform | Platform security is Anthropic's responsibility; not assessable from within the framework |
| MCP servers (Context7, Memory-Keeper) | These skills do not use MCP tools; MCP assessment is out of scope |
| Worktracker core logic | Skills interact with worktracker via CLI only; worktracker internals are out of scope |
| JSON Schema files (`docs/schemas/*.json`) | Schemas are consumed by agents but are framework-level assets; schema-level findings should reference the prior eng-security finding (SEC-002 step-9, SEC-003 step-10) |
| Live agent execution testing | Assessment-only; no live exploitation or agent invocation for testing purposes |
| Social engineering | Not applicable to this engagement type |
| Physical security | Not applicable |
| Network infrastructure | Skills have no network surface |

### Boundary Cases

| Case | Decision | Rationale |
|------|----------|-----------|
| Schema files referenced by target skills | Read for context; findings against schema files reference prior eng-security IDs | Schemas are shared framework assets; skill-specific schema consumption patterns are in scope |
| ORCHESTRATION.yaml workflow definition | Read for context; not an assessment target | Orchestration is the coordination layer, not an attack surface for these skills |
| Trigger map entries in mandatory-skill-usage.md | In scope for AS-7 (routing manipulation) | Trigger map entries for these three skills are directly relevant to routing attack surface |

---

## Scope Document (YAML)

```yaml
scope:
  engagement_id: "RED-0001"
  version: "1.0"
  authorized_targets:
    - type: "directory"
      value: "skills/use-case/"
    - type: "directory"
      value: "skills/test-spec/"
    - type: "directory"
      value: "skills/contract-design/"
    - type: "file"
      value: ".context/rules/mandatory-skill-usage.md"
      note: "Trigger map entries for routing analysis (AS-7) only"
    - type: "reference"
      value: "projects/PROJ-021-use-case/orchestration/use-case-skills-20260308-001/implementation/step-9-eng-security-review.md"
      note: "Prior findings baseline -- read-only reference"
    - type: "reference"
      value: "projects/PROJ-021-use-case/orchestration/use-case-skills-20260308-001/implementation/step-10-eng-security-review.md"
      note: "Prior findings baseline -- read-only reference"
    - type: "reference"
      value: "projects/PROJ-021-use-case/orchestration/use-case-skills-20260308-001/implementation/step-11-eng-security-review.md"
      note: "Prior findings baseline -- read-only reference"
  technique_allowlist:
    - "T1592"   # Gather Victim Host Information (adapted: gather target file inventory)
    - "T1190"   # Exploit Public-Facing Application (adapted: assess input validation surfaces)
    - "T1059"   # Command and Scripting Interpreter (adapted: assess Bash tool abuse vectors)
    - "T1548"   # Abuse Elevation Control Mechanism (adapted: assess tool tier escalation)
    - "T1565"   # Data Manipulation (adapted: assess pipeline poisoning)
    - "T1036"   # Masquerading (adapted: assess PROTOTYPE label bypass)
  time_window:
    start: "2026-03-09"
    end: "2026-03-10"
    note: "Assessment-only; no live exploitation window required"
  exclusion_list:
    - "src/**"
    - "docs/governance/**"
    - ".context/rules/** (except mandatory-skill-usage.md trigger map)"
    - "skills/problem-solving/**"
    - "skills/adversary/**"
    - "skills/eng-team/**"
    - "skills/nasa-se/**"
    - "skills/orchestration/**"
    - "skills/worktracker/**"
    - "skills/transcript/**"
    - "skills/saucer-boy/**"
    - "skills/saucer-boy-framework-voice/**"
    - "skills/ast/**"
    - "skills/red-team/**"
    - "skills/pm-pmm/**"
    - "skills/prompt-engineering/**"
    - "skills/diataxis/**"
    - "skills/user-experience/**"
  rules_of_engagement:
    escalation_contact: "User (PROJ-021 owner)"
    emergency_stop: "Critical finding or active exploitation detected"
    communication_channel: "Orchestration worktracker + findings report"
    social_engineering_authorized: false
    persistence_authorized: false
    exfiltration_authorized: false
    data_types_permitted:
      - "agent definitions (markdown, YAML)"
      - "template files (markdown, YAML, JSON)"
      - "rule files (markdown)"
      - "sample files (markdown, YAML)"
      - "test specifications (markdown)"
      - "prior security review reports (markdown)"
  agent_authorizations:
    - agent: "red-lead"
      role: "Engagement lead -- scope definition and oversight"
      techniques: ["scope-definition", "methodology-selection"]
    - agent: "red-vuln"
      role: "Vulnerability analyst -- attack surface assessment"
      techniques: ["T1592", "T1190", "T1059", "T1548", "T1565", "T1036"]
    - agent: "red-reporter"
      role: "Findings reporter -- compile and rate findings"
      techniques: ["report-compilation"]
  evidence_handling:
    storage: "projects/PROJ-021-use-case/orchestration/use-case-skills-20260308-001/security/"
    retention_days: 90
    destruction_method: "git branch deletion after merge to main"
  signature:
    authorized_by: "PENDING -- requires user confirmation"
    date: "2026-03-09"
    confirmation: "User must confirm this scope document before red-vuln may begin assessment"
```

---

## S-010 Self-Review Checklist

| # | Check | Status | Evidence |
|---|-------|--------|----------|
| 1 | Scope boundaries are explicit and non-ambiguous | PASS | Target inventory lists all 46+3 files; exclusion list covers all other skills and framework components |
| 2 | Rules of engagement distinguish authorized from prohibited actions | PASS | Authorized actions table (9 entries) and prohibited actions table (8 entries) are comprehensive |
| 3 | All 9 attack surfaces from the engagement request are covered | PASS | AS-1 through AS-9 mapped in attack surface matrix with per-surface assessment procedures |
| 4 | Prior eng-security findings are referenced without duplication | PASS | Deduplication criteria defined; prior findings referenced by ID (SEC-xxx from step-9/10/11) |
| 5 | YAML scope document includes all required fields | PASS | engagement_id, authorized_targets, technique_allowlist, time_window, exclusion_list, rules_of_engagement, agent_authorizations, evidence_handling, signature -- all present |
| 6 | Assessment methodology maps to specific procedures per attack surface | PASS | 9 assessment procedures defined (AS-1 through AS-9) with evidence requirements |
| 7 | Success criteria distinguish findings from accepted risks | PASS | Finding criteria (6 conditions) and accepted risk criteria (4 conditions) defined |
| 8 | Gate criteria (GATE-5b) are traceable to ORCHESTRATION.yaml | PASS | GATE-5b threshold 0.95, trigger condition, and finding disposition requirements aligned with orchestration |
| 9 | Navigation table present with anchor links (H-23) | PASS | 11-entry navigation table with functional anchor links |
| 10 | Constitutional compliance: P-003 (no subagent spawning), P-020 (user authority respected), P-022 (no deception about scope or capabilities) | PASS | Scope document explicitly awaits user authorization (P-020); all limitations disclosed (P-022); no delegation to sub-agents (P-003) |
| 11 | L0/L1/L2 output levels present | PASS | L0 (executive summary), L1 (technical scope), L2 (strategic context) all present |
| 12 | Scope document does not authorize live exploitation | PASS | Prohibited actions table explicitly prohibits live exploitation; PTES Phase V marked NOT AUTHORIZED |

---

*Engagement Scope Version: 1.0*
*Agent: red-lead*
*Constitutional Compliance: P-003 (no recursive subagents), P-020 (user authorization required), P-022 (all limitations disclosed)*
*SSOT: ORCHESTRATION.yaml step-11b-scope*
*Created: 2026-03-09*
