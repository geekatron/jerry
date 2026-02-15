# S-001: Red Team Analysis -- Adversarial Strategy Execution Template

<!--
TEMPLATE: S-001 Red Team Analysis Adversarial Strategy Execution Template
VERSION: 1.0.0 | DATE: 2026-02-15
SOURCE: quality-enforcement.md SSOT, ADR-EPIC002-001, TEMPLATE-FORMAT.md v1.1.0
ENABLER: EN-809 (S-001 Template)
STATUS: ACTIVE
CONFORMANCE: TEMPLATE-FORMAT.md v1.1.0

Academic Foundation:
- U.S. military red teaming origins (1960s-1970s): Cold War wargaming and competitive hypothesis testing
- Zenko (2015): "Red Team: How to Succeed By Thinking Like the Enemy" (Basic Books)
- MITRE ATT&CK framework: Adversary TTP taxonomy for systematic threat vector enumeration
- NIST SP 800-53: Security and Privacy Controls -- red team assessment methodology
- TIBER-EU (2018): ECB threat intelligence-based ethical red teaming framework
- Wood & Duggan (2000): "Red Teaming of Advanced Information Assurance Concepts" (DARPA)

Origin: U.S. military, 1960s-1970s Cold War wargaming.
Domain: Adversarial Simulation, Security Assessment, Risk Management.
Key insight: Emulation of a SPECIFIC threat actor perspective -- not just "what could go wrong"
but "what would adversary X do?" -- tests the entire defense chain under realistic attack conditions.
-->

> **Type:** adversarial-strategy-template
> **Status:** ACTIVE
> **Version:** 1.0.0
> **Date:** 2026-02-15
> **Source:** quality-enforcement.md, ADR-EPIC002-001, ADR-EPIC002-002
> **Format Conformance:** TEMPLATE-FORMAT.md v1.1.0
> **Enabler:** EN-809

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Identity](#identity) | Strategy classification and metadata |
| [Purpose](#purpose) | When and why to apply Red Team Analysis |
| [Prerequisites](#prerequisites) | Required inputs and ordering constraints (H-16) |
| [Execution Protocol](#execution-protocol) | Step-by-step adversarial emulation procedure |
| [Output Format](#output-format) | Required structure for Red Team report |
| [Scoring Rubric](#scoring-rubric) | Meta-evaluation of strategy execution quality |
| [Examples](#examples) | Concrete C4 demonstration with findings |
| [Integration](#integration) | Cross-strategy pairing, H-16 compliance, criticality mapping |

---

## Identity

| Field | Value |
|-------|-------|
| Strategy ID | S-001 |
| Strategy Name | Red Team Analysis |
| Family | Role-Based Adversarialism |
| Composite Score | 3.35 |
| Finding Prefix | RT-NNN-{execution_id} |
| Version | 1.0.0 |
| Date | 2026-02-15 |

### Criticality Tier Table

| Level | Name | Status | Notes |
|-------|------|--------|-------|
| C1 | Routine | NOT USED | C1 enforces HARD rules only; Red Team not required or optional |
| C2 | Standard | NOT USED | S-001 not in C2 required or optional sets |
| C3 | Significant | OPTIONAL | Part of C3 optional set (S-001, S-003, S-010, S-011) |
| C4 | Critical | REQUIRED | All 10 strategies required; tournament mode |

**Source:** quality-enforcement.md Criticality Levels table (SSOT).

**Foundation:** Red teaming originated in U.S. military Cold War wargaming (1960s-1970s) as a method to test strategic plans by having a dedicated team emulate the adversary. Zenko (2015) demonstrates that organizations consistently underestimate threats until exposed to realistic adversarial simulation. The MITRE ATT&CK framework provides a systematic taxonomy of adversary Tactics, Techniques, and Procedures (TTPs) for structured threat enumeration.

**Jerry Implementation:** Adopts the perspective of a specific threat actor (not generic criticism) to systematically attack the deliverable. For document review: "If I were trying to find the most damaging flaw, what would I attack?" For architecture: "If I were exploiting this system, what would I target?" For governance: "If I wanted to circumvent these rules, how would I do it?" Adapts MITRE ATT&CK thinking to enumerate threat vectors systematically. Implements H-16 ordering (S-003 Steelman MUST run before S-001).

---

## Purpose

### When to Use

1. **C4 Critical Deliverable Review:** ALL Critical deliverables MUST undergo Red Team analysis (required at C4). Apply after Steelman (S-003) has strengthened the deliverable per H-16.

2. **C3 Deliverables with Adversarial Risk:** When a C3 deliverable has security, governance, or exploitation risk surfaces. Red Team is OPTIONAL at C3 but RECOMMENDED when the deliverable defines rules, permissions, or trust boundaries that an adversary might circumvent.

3. **Governance and Constitutional Documents:** When reviewing governance rules, constitutional constraints, or enforcement mechanisms where a motivated actor would seek loopholes, ambiguities, or bypass paths. Red Team reveals weaknesses that collaborative review misses.

4. **Architecture and API Contract Review:** When the deliverable defines system boundaries, authentication flows, access controls, or external interfaces. Red Team emulates an attacker probing for the weakest entry point in the defense chain.

### When NOT to Use

1. **C1/C2 Routine or Standard Decisions:** Red Team is expensive and produces diminishing returns on low-stakes deliverables. For C2 adversarial coverage, redirect to S-002 (Devil's Advocate) which provides sufficient challenge without full adversarial emulation.

2. **Deliverables Without Exploitable Surfaces:** If the deliverable is purely informational (research summaries, analysis reports) with no rules, interfaces, or trust boundaries to attack, Red Team has no adversary to emulate. Redirect to S-004 (Pre-Mortem) for risk-oriented review or S-013 (Inversion) for assumption testing.

### Expected Outcome

A Red Team report containing:
- Explicit threat actor profile defining the adversary's goals, capabilities, and motivations
- Systematic enumeration of attack vectors using structured threat taxonomy (minimum 4 vectors)
- RT-NNN identified findings with severity classification (Critical/Major/Minor)
- Evidence-based exploitability assessment for each attack vector
- Defense gap analysis mapping findings to the 6 S-014 scoring dimensions
- Mitigation recommendations for all Critical and Major findings
- Measurable quality improvement when mitigations are addressed (target: 0.05+ composite score increase)

### Pairing Recommendations

**H-16 Compliance (MANDATORY):** Run S-003 Steelman BEFORE S-001 Red Team. H-16 requires the deliverable to be strengthened before adversarial critique. Red Team must attack the strongest version, not a weak first draft.

| Pairing | Order | Rationale |
|---------|-------|-----------|
| **S-003 + S-001** | S-003 -> S-001 | H-16: Steelman strengthens before Red Team attacks |
| **S-001 + S-014** | S-001 -> S-014 | Findings feed dimension scoring; S-014 validates post-mitigation quality |
| **S-004 + S-001** | S-004 -> S-001 | Pre-Mortem identifies risk areas; Red Team systematically exploits them |
| **S-001 + S-012** | S-001 -> S-012 | Red Team identifies high-level attack vectors; FMEA decomposes into component failure modes |

**Optimal C4 sequence:** S-003 -> S-007 -> S-002 -> S-004 -> S-012 -> S-013 -> S-011 -> S-001 -> S-010 -> S-014

---

## Prerequisites

### Required Inputs

- [ ] Deliverable artifact (architecture, governance document, API contract, design, etc.)
- [ ] Criticality level classification (C3 optional or C4 required)
- [ ] S-003 Steelman output (H-16 compliance: Steelman MUST have been applied first)
- [ ] Quality framework SSOT (`quality-enforcement.md`) for dimension weights and threshold
- [ ] Domain context sufficient to define a realistic threat actor profile

### Context Requirements

The executor must have domain expertise sufficient to emulate a realistic adversary, familiarity with the deliverable's trust boundaries and exploitable surfaces, access to the S-003 Steelman output, and understanding of what an attacker would gain by defeating or circumventing the deliverable.

### Ordering Constraints

**H-16 (MANDATORY):** S-003 Steelman MUST be applied before S-001 Red Team. The deliverable MUST be strengthened before adversarial emulation begins. Executing S-001 without prior S-003 is an H-16 violation.

**Recommended sequence:**
1. S-010 Self-Refine (creator self-review)
2. S-003 Steelman (strengthen the deliverable)
3. S-007 Constitutional AI Critique (HARD rule compliance)
4. S-002 Devil's Advocate (challenge current claims)
5. S-004 Pre-Mortem Analysis (imagine future failures)
6. S-012 FMEA (decompose failure modes)
7. S-013 Inversion (stress-test assumptions)
8. S-011 Chain-of-Verification (verify factual claims)
9. **S-001 Red Team Analysis (this strategy)**
10. S-014 LLM-as-Judge (score the revised deliverable)

**Minimum:** S-003 before S-001. S-014 after S-001 for dimensional scoring.

---

## Execution Protocol

### Step 1: Define the Threat Actor

**Action:** Establish a specific adversary profile with goals, capabilities, and motivations relevant to the deliverable.

**Procedure:**
1. Read the deliverable and S-003 Steelman output in full (H-16 compliance check: if no S-003 output exists, STOP and flag H-16 violation)
2. Identify the deliverable's trust boundaries: what does it protect, enforce, or control?
3. Define the threat actor explicitly:
   - **Goal:** What does the adversary want to achieve? (e.g., bypass governance, exploit API, corrupt data)
   - **Capability:** What resources and knowledge does the adversary have? (e.g., full source access, domain expertise, insider knowledge)
   - **Motivation:** Why would someone attack this? (e.g., avoid compliance overhead, gain unauthorized access, exploit ambiguity)
4. Document the threat actor profile in the output report

**Decision Point:**
- If S-003 Steelman output is missing: STOP. Flag H-16 violation. Do not proceed until S-003 is applied.
- If the deliverable has no exploitable surfaces: STOP. Redirect to S-004 or S-013. Document the redirect rationale.
- If S-003 output exists and exploitable surfaces identified: Proceed to Step 2.

**Output:** Threat actor profile with explicit goal, capability, and motivation.

### Step 2: Enumerate Attack Vectors

**Action:** Systematically identify all avenues the threat actor could use to defeat, exploit, or circumvent the deliverable.

**Procedure:**
Apply the 5 attack vector categories (adapted from MITRE ATT&CK for document/design review):

1. **Ambiguity exploitation:** Vague language, undefined terms, or missing definitions that permit unintended interpretations
2. **Boundary violations:** Gaps between layers, interfaces, or responsibility boundaries that allow unauthorized traversal
3. **Rule circumvention:** Loopholes, exceptions, or edge cases that allow compliance in letter but not spirit
4. **Dependency attacks:** External dependencies, assumptions about environment, or trust chains that can be broken
5. **Degradation paths:** Conditions under which the deliverable's protections erode over time (context rot, configuration drift, knowledge loss)

For each attack vector:
1. Describe the attack in specific terms from the adversary's perspective
2. Assess **exploitability** (High/Medium/Low) -- how easily can the adversary execute this?
3. Assess **severity** using standard definitions (see below)
4. Map to affected scoring dimension
5. Assign RT-NNN-{execution_id} identifier

**Decision Point:**
- If fewer than 4 attack vectors identified: apply deeper analysis per each of the 5 categories. Red Team should find vectors that other strategies miss.
- If Critical findings found: the deliverable has fundamental vulnerabilities requiring mitigation before acceptance.

**Severity Definitions:**
- **Critical:** Attack vector would invalidate the deliverable or allow complete bypass of its protections. Blocks acceptance.
- **Major:** Attack vector would significantly weaken the deliverable or allow partial circumvention. Requires mitigation.
- **Minor:** Attack vector is theoretically possible but low-impact. Improvement opportunity.

**Output:** Attack vector inventory with RT-NNN identifiers, categories, exploitability, severity, and affected dimensions.

### Step 3: Assess Defense Gaps

**Action:** For each attack vector, evaluate what defenses exist (or are missing) in the deliverable.

**Procedure:**
1. For each RT-NNN finding, identify existing defenses in the deliverable (if any)
2. Classify each defense as: **Effective** (blocks the attack), **Partial** (reduces but does not eliminate risk), or **Missing** (no defense exists)
3. For Partial and Missing defenses, specify what the adversary would observe and exploit
4. Prioritize findings:
   - **P0 (Immediate):** Critical severity AND Missing/Partial defense -- MUST mitigate before acceptance
   - **P1 (Important):** Major severity AND Missing defense, OR Critical AND Partial defense -- SHOULD mitigate
   - **P2 (Monitor):** Major AND Partial defense, OR Minor severity -- MAY mitigate

**Output:** Defense gap assessment with prioritization matrix.

### Step 4: Develop Countermeasures

**Action:** For each P0 and P1 finding, specify a concrete countermeasure the deliverable should incorporate.

**Procedure:**
1. For each P0 finding: specify the exact revision needed (close the loophole, add the missing boundary, define the ambiguous term, add the missing defense)
2. For each P1 finding: specify the recommended revision with acceptance criteria
3. For P2 findings: note the risk and recommend monitoring approach
4. Verify each countermeasure directly addresses the attack vector (not generic "improve security")

**Output:** Countermeasure plan with specific actions, acceptance criteria, and priority ordering.

### Step 5: Synthesize and Score Impact

**Action:** Produce a consolidated assessment mapping Red Team findings to quality dimensions.

**Procedure:**
1. Aggregate findings by severity: count Critical, Major, Minor
2. Map findings to the 6 scoring dimensions and assess net impact (Positive/Negative/Neutral) per dimension
3. Estimate composite score impact of countermeasures
4. Determine overall assessment: major remediation required / targeted remediation / proceed with monitoring
5. Apply H-15 self-review before presenting

**Output:** Scoring Impact table, overall assessment, and countermeasure guidance.

---

## Output Format

Every S-001 execution MUST produce a Red Team report with these sections:

### 1. Header

```markdown
# Red Team Report: {{DELIVERABLE_NAME}}

**Strategy:** S-001 Red Team Analysis
**Deliverable:** {{Artifact name, file path, or work item ID}}
**Criticality:** {{C3/C4}}
**Date:** {{ISO 8601 date}}
**Reviewer:** {{Agent ID or human name}}
**H-16 Compliance:** S-003 Steelman applied on {{date}} (confirmed)
**Threat Actor:** {{Brief profile -- goal, capability, motivation}}
```

### 2. Summary

2-3 sentence overall assessment covering: threat actor profile, number and severity of attack vectors identified, overall deliverable security posture, and recommendation (ACCEPT with countermeasures / REVISE / REJECT).

### 3. Findings Table

| ID | Attack Vector | Category | Exploitability | Severity | Priority | Defense | Affected Dimension |
|----|---------------|----------|----------------|----------|----------|---------|-------------------|
| RT-001-{execution_id} | {{Attack vector}} | {{Ambiguity/Boundary/Circumvention/Dependency/Degradation}} | {{H/M/L}} | Critical | P0 | Missing | {{Dimension}} |
| RT-002-{execution_id} | {{Attack vector}} | {{Category}} | {{H/M/L}} | Major | P1 | Partial | {{Dimension}} |

**Finding ID Format:** `RT-{NNN}-{execution_id}` where execution_id is a short timestamp or session identifier (e.g., `RT-001-20260215T1430`) to prevent ID collisions across tournament executions.

### 4. Finding Details

Expanded description for each Critical and Major finding:

```markdown
### RT-001: {{Finding Title}} [CRITICAL]

**Attack Vector:** {{Specific description of how the adversary exploits this}}
**Category:** {{Ambiguity/Boundary/Circumvention/Dependency/Degradation}}
**Exploitability:** {{High/Medium/Low}} -- {{Justification}}
**Severity:** {{Critical/Major}} -- {{Consequence if exploited}}
**Existing Defense:** {{What defense exists, if any}}
**Evidence:** {{Specific references from the deliverable that create this vulnerability}}
**Dimension:** {{Affected scoring dimension}}
**Countermeasure:** {{Specific action to close this attack vector}}
**Acceptance Criteria:** {{What must be demonstrated to resolve this finding}}
```

### 5. Recommendations

Prioritized countermeasure plan grouped by: **P0** (Critical -- MUST mitigate before acceptance), **P1** (Important -- SHOULD mitigate), **P2** (Monitor -- MAY mitigate). Each entry: RT-NNN identifier, specific countermeasure action, and acceptance criteria.

### 6. Scoring Impact

Map Red Team findings to S-014 scoring dimensions (Completeness 0.20, Internal Consistency 0.20, Methodological Rigor 0.20, Evidence Quality 0.15, Actionability 0.15, Traceability 0.10). For each dimension, assess Impact (Positive/Negative/Neutral) with rationale referencing specific RT-NNN findings.

### Evidence Requirements

Each finding MUST include: specific reference to the location in the deliverable that creates the vulnerability, description of the attack scenario with concrete exploitation path, and explanation of why the adversary would target this vector.

---

## Scoring Rubric

This rubric evaluates the **quality of the S-001 Red Team execution itself** (meta-evaluation), not the deliverable being reviewed.

### Threshold Bands

**SSOT threshold (from quality-enforcement.md, MUST NOT be redefined):** >= 0.92 weighted composite score. Below threshold = REJECTED; revision required per H-13.

**Operational bands for S-001 execution quality:**

| Band | Score Range | Outcome |
|------|------------|---------|
| PASS | >= 0.92 | Strategy execution accepted; adversarial analysis is thorough and evidence-based |
| REVISE | 0.85 - 0.91 | Strategy execution requires targeted revision; close to threshold |
| REJECTED | < 0.85 | Strategy execution inadequate; significant rework required (H-13) |

> **Note:** Score bands (PASS/REVISE/REJECTED) are sourced from quality-enforcement.md (Operational Score Bands section). See SSOT for authoritative definitions.

### Dimension Weights

From quality-enforcement.md (MUST NOT be redefined):

| Dimension | Weight | Measures (for S-001 execution quality) |
|-----------|--------|----------------------------------------|
| Completeness | 0.20 | All 5 attack vector categories explored; 4+ vectors; countermeasures for all P0/P1 findings |
| Internal Consistency | 0.20 | Findings do not contradict each other; severity/exploitability consistent with evidence; priorities coherent |
| Methodological Rigor | 0.20 | Threat actor defined; all 5 steps executed; H-16 verified; 5 attack categories used; leniency bias counteracted |
| Evidence Quality | 0.15 | Each attack vector backed by specific deliverable references and realistic exploitation scenarios |
| Actionability | 0.15 | Countermeasures concrete; acceptance criteria specific and verifiable |
| Traceability | 0.10 | Findings linked to deliverable content; dimensions mapped; H-16 compliance documented |

### Strategy-Specific Rubric

| Dimension (Weight) | 0.95+ | 0.90-0.94 | 0.85-0.89 | <0.85 |
|--------------------|-------|-----------|-----------|-------|
| **Completeness (0.20)** | ALL 5 attack categories explored with 6+ vectors; countermeasures for all P0/P1; threat actor vivid and specific | All 5 categories explored; 4-5 vectors; countermeasures for P0; threat actor clear | 3-4 categories explored; 3 vectors; some countermeasures missing; threat actor vague | <3 categories; <3 vectors; no countermeasures; no threat actor |
| **Internal Consistency (0.20)** | Zero contradictions; severity/exploitability/priority aligned with evidence; findings distinct and non-overlapping | No contradictions; severity mostly justified; minor priority gaps | One minor inconsistency; some severity ratings questionable; overlapping vectors | Multiple contradictions; arbitrary severity; redundant vectors |
| **Methodological Rigor (0.20)** | Threat actor explicitly profiled; all 5 steps in order; H-16 verified with evidence; all 5 categories applied; adversary perspective maintained throughout | All steps executed; H-16 verified; most categories applied; adversary perspective present | 4 steps executed; H-16 noted; some categories applied; adversary perspective intermittent | <4 steps; H-16 not checked; ad hoc attack list; no adversary perspective |
| **Evidence Quality (0.15)** | Every vector references specific deliverable content; realistic exploitation paths with concrete consequences; domain-informed attack scenarios | Most vectors have specific evidence; scenarios realistic; minor vagueness | Some vectors have evidence; scenarios plausible but not specific | Vectors speculative; no evidence; generic attacks not tied to deliverable |
| **Actionability (0.15)** | ALL P0/P1 countermeasures specific with verifiable acceptance criteria; creator can act without guessing | Most countermeasures specific; acceptance criteria for P0; minor gaps | Some countermeasures present; criteria vague; creator must interpret | No countermeasures; findings are observations without guidance |
| **Traceability (0.10)** | Every finding traces to deliverable content; all findings mapped to dimensions; H-16 documented with S-003 reference | Most findings traceable; dimension mapping present; H-16 documented | Some findings traceable; partial dimension mapping; H-16 mentioned | Findings not traceable; no dimension mapping; H-16 unknown |

---

## Examples

### Example 1: C4 Governance Document -- Quality Enforcement Rules

**Context:**
- **Deliverable:** Revised quality-enforcement.md defining HARD rules, criticality levels, and enforcement architecture
- **Criticality Level:** C4 (Critical) -- governance document, irreversible, public-facing rules
- **Scenario:** S-003 Steelman applied first (H-16 compliance); S-002, S-004 also completed; now S-001 Red Team

**Before (Key Governance Claims after S-003 Steelman):**

The governance document defines: (1) 24 HARD rules that "CANNOT be overridden," (2) a 5-layer enforcement architecture with L1-L5 defense layers, (3) auto-escalation rules AE-001 through AE-006, (4) a quality threshold of >= 0.92 for C2+ deliverables. The document was strengthened by S-003 and critiqued by S-002 and S-004.

**Strategy Execution (S-001 Red Team):**

**Step 1: Define Threat Actor** -- Profile: "A skilled LLM operator who wants to ship low-quality deliverables quickly. They have full access to the codebase and CLAUDE.md, understand the enforcement architecture, and are motivated to minimize the overhead of quality processes."

**Step 2: Enumerate Attack Vectors**

| ID | Attack Vector | Category | Exploitability | Severity | Priority | Defense | Affected Dimension |
|----|---------------|----------|----------------|----------|----------|---------|-------------------|
| RT-001-20260215T1730 | Context rot degrades L1 rules: after 150K tokens, HARD rules loaded at session start are no longer attended to, effectively disabling enforcement | Degradation | High | Critical | P0 | Partial (L2 re-injection) | Methodological Rigor |
| RT-002-20260215T1730 | C1 classification abuse: operator classifies C3 work as C1 to avoid quality gate, since criticality self-classification has no independent verification | Circumvention | High | Major | P1 | Missing | Internal Consistency |
| RT-003-20260215T1730 | Steelman-before-critique ordering (H-16) has no deterministic enforcement: an agent can claim S-003 was applied without evidence, since no L3 gate checks for S-003 output artifact | Circumvention | Medium | Major | P1 | Missing | Evidence Quality |
| RT-004-20260215T1730 | AE-002 triggers on file path but not content: modifying rule semantics via a new file that imports/overrides `.context/rules/` content would bypass auto-escalation | Boundary | Medium | Major | P1 | Missing | Completeness |
| RT-005-20260215T1730 | Quality score self-assessment leniency: S-014 LLM-as-Judge is executed by the same agent that created the deliverable, enabling unconscious leniency bias | Degradation | Medium | Minor | P2 | Partial (rubric) | Evidence Quality |

**Step 4: Develop Countermeasures**

**P0:** RT-001 -- Increase L2 re-injection token budget for critical HARD rules; add explicit "context health check" step requiring re-read of quality-enforcement.md at 50% context utilization. Acceptance criteria: L2 re-injection strategy documented with specific trigger conditions.

**P1:** RT-002 -- Add "Criticality Justification" requirement: C1 classification must include explicit rationale explaining why criteria (reversible in 1 session, <3 files) are met. RT-003 -- Add S-003 output artifact requirement: H-16 compliance must reference a specific S-003 report with date and findings. RT-004 -- Expand AE-002 to trigger on content that references or modifies rule semantics, not just file paths.

**After (Governance Document Revised Based on RT Findings):**

The creator addressed findings: added context health check procedure (RT-001), criticality justification requirement (RT-002), S-003 artifact evidence requirement (RT-003), and expanded AE-002 trigger scope (RT-004). RT-005 acknowledged with rubric strictness reminder.

**Scoring Impact:**

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | RT-004: AE rule gap leaves governance surface incomplete |
| Internal Consistency | 0.20 | Negative | RT-002: Self-classification without verification contradicts "CANNOT be overridden" claim |
| Methodological Rigor | 0.20 | Negative | RT-001: Context rot undermines the enforcement architecture's reliability claim |
| Evidence Quality | 0.15 | Negative | RT-003: H-16 unenforced means evidence of compliance is unreliable |
| Actionability | 0.15 | Neutral | Countermeasures are concrete and implementable |
| Traceability | 0.10 | Neutral | Document traces to ADRs and constitution |

**Result:** 1 Critical and 3 Major attack vectors identified via adversarial emulation. After countermeasures, the governance document closed 4 of 5 vectors, strengthening enforcement architecture integrity.

---

## Integration

### Canonical Pairings

See [Pairing Recommendations](#pairing-recommendations) for the full pairing table (S-003, S-014, S-004, S-012) with rationale and optimal sequence.

### H-16 Compliance

**H-16 Rule:** Steelman before critique. S-003 MUST execute before S-001. Full ordering constraints and recommended sequences are documented in [Prerequisites: Ordering Constraints](#ordering-constraints) and [Purpose: Pairing Recommendations](#pairing-recommendations).

**Compliant:** S-003 -> S-001 -> S-014; S-003 -> S-004 -> S-001 -> S-014. **Non-Compliant:** S-001 without prior S-003; S-001 -> S-003.

### Criticality-Based Selection Table

From quality-enforcement.md (MUST NOT modify):

| Level | Required Strategies | Optional Strategies | S-001 Status |
|-------|---------------------|---------------------|--------------|
| C1 | S-010 | S-003, S-014 | NOT USED |
| C2 | S-007, S-002, S-014 | S-003, S-010 | NOT USED |
| C3 | C2 + S-004, S-012, S-013 | S-001, S-003, S-010, S-011 | **OPTIONAL** |
| C4 | All 10 selected | None | **REQUIRED** |

**Source:** quality-enforcement.md Criticality Levels table (SSOT). Values MUST match exactly.

### Cross-References

**SSOT:** `.context/rules/quality-enforcement.md` (H-13 threshold, H-16, dimension weights, criticality levels) | `ADR-EPIC002-001` (strategy selection, score 3.35) | `ADR-EPIC002-002` (enforcement architecture) | `.context/templates/adversarial/TEMPLATE-FORMAT.md` v1.1.0

**Strategy Templates:** `s-003-steelman.md` (MUST run before S-001, H-16) | `s-004-pre-mortem.md` (complementary: imagines future failures before adversarial exploitation) | `s-002-devils-advocate.md` (complementary: challenges claims vs. emulates adversary) | `s-012-fmea.md` (decomposes Red Team vectors into component failure modes) | `s-013-inversion.md` (complementary: assumption stress-testing) | `s-014-llm-as-judge.md` (scores post-mitigation revision) | `s-011-cove.md` (complementary: verifies factual claims Red Team may challenge)

**Academic:** Zenko (2015), MITRE ATT&CK, NIST SP 800-53, TIBER-EU (2018), Wood & Duggan (2000). See file header.

**HARD Rules:** H-13 (threshold >= 0.92), H-14 (creator-critic cycle), H-15 (self-review), H-16 (steelman before critique), H-17 (scoring required) -- all from quality-enforcement.md

---

<!-- VALIDATION: 8 sections present | H-23/H-24 nav | RT-NNN prefix | H-16 documented | SSOT weights match | REVISE band noted | C4 example with Critical finding | No absolute paths | 4-band rubric | Under 500 lines -->

---

*Template Version: 1.0.0*
*Format Conformance: TEMPLATE-FORMAT.md v1.1.0*
*SSOT: `.context/rules/quality-enforcement.md`*
*Created: 2026-02-15*
*Enabler: EN-809*
