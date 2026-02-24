# B-004: Threat Modeling Methodology Comparison

> Stream B: Methodology Standards | PROJ-010 Cyber Ops | Phase 1 Research

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | High-level comparison and recommendation |
| [L1: Key Findings](#l1-key-findings) | Structured findings on methodology suitability |
| [L2: Detailed Analysis](#l2-detailed-analysis) | Deep analysis of STRIDE, DREAD, PASTA, LINDDUN, and Attack Trees |
| [Agent Mapping](#agent-mapping) | How threat modeling maps to eng-architect and other /eng-team agents |
| [Evidence and Citations](#evidence-and-citations) | Categorized, dated sources |
| [Recommendations](#recommendations) | Default threat modeling methodology for eng-architect |

---

## L0: Executive Summary

Five threat modeling methodologies were analyzed for the /eng-team eng-architect agent: STRIDE (threat identification), DREAD (risk scoring), PASTA (attack simulation), LINDDUN (privacy threats), and Attack Trees (hierarchical attack decomposition). STRIDE provides the most natural fit as the primary threat identification methodology -- its 6 threat categories (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege) are well-understood, map directly to security properties, and are straightforward to apply systematically to system components. DREAD provides the complementary risk scoring dimension that STRIDE lacks, enabling prioritization of identified threats. The recommended default configuration for eng-architect is STRIDE for threat identification paired with DREAD for risk scoring, supplemented by Attack Trees for complex attack path visualization. PASTA should be available for risk-centric engagements requiring business impact analysis, and LINDDUN should be available for privacy-regulated applications (GDPR, HIPAA, CCPA).

---

## L1: Key Findings

### Finding 1: STRIDE Is the Industry Standard for Systematic Threat Identification

Developed at Microsoft, STRIDE is the most widely adopted threat modeling methodology. Its 6 categories map directly to violated security properties (Authentication, Integrity, Non-repudiation, Confidentiality, Availability, Authorization). This property-based mapping makes it systematic: for every system component, apply each STRIDE category to identify threats. This systematic nature makes it well-suited for agentic automation -- eng-architect can methodically apply STRIDE categories to each component in the architecture.

### Finding 2: DREAD Provides Quantitative Risk Scoring That STRIDE Lacks

STRIDE identifies threats but does not score them. DREAD fills this gap with a 5-dimension scoring model (Damage, Reproducibility, Exploitability, Affected Users, Discoverability), each rated 1-10. The composite DREAD score enables threat prioritization. While DREAD has been criticized for subjectivity (different analysts may assign different scores), this is acceptable for an agentic context where consistent scoring rubrics can be defined and applied uniformly.

### Finding 3: PASTA Is the Most Comprehensive but Most Complex

PASTA's 7-stage process connects technical threats to business impact through attack simulation. It is the most thorough methodology but also the most resource-intensive. For eng-architect, PASTA is appropriate for high-criticality engagements (C3/C4) where business impact analysis is critical, but it is excessive for routine (C1/C2) threat modeling.

### Finding 4: LINDDUN Addresses a Distinct Privacy-Specific Gap

LINDDUN's 7 privacy threat categories (Linking, Identifying, Non-repudiation, Detecting, Disclosure of information, Unawareness, Non-compliance) address threats that STRIDE does not cover. STRIDE's "Information Disclosure" is a single category that LINDDUN expands into 7 nuanced privacy dimensions. For applications subject to GDPR, HIPAA, or CCPA, LINDDUN provides essential coverage that STRIDE alone cannot deliver. LINDDUN is included in ISO 27550 (Privacy Engineering) and endorsed by the European Data Protection Supervisor.

### Finding 5: Attack Trees Provide Unmatched Visualization of Complex Attack Scenarios

Bruce Schneier's Attack Trees provide a hierarchical decomposition of attack goals into sub-goals, enabling visualization of complex, multi-step attack paths. Attack Trees are not a standalone methodology but a powerful analytical technique that complements any threat modeling approach. They are particularly valuable for eng-architect when analyzing complex attack scenarios involving vulnerability chaining or multi-stage exploitation.

---

## L2: Detailed Analysis

### STRIDE (Microsoft, 1999)

#### Overview

STRIDE was developed by Loren Kohnfelder and Praerit Garg at Microsoft in 1999. It categorizes threats by the security property they violate, providing a systematic checklist approach to threat identification.

#### The 6 STRIDE Categories

| Category | Violated Property | Description | Examples |
|----------|-------------------|-------------|----------|
| **Spoofing** | Authentication | Pretending to be something or someone other than yourself | Forged authentication tokens, IP spoofing, DNS spoofing, credential theft, session hijacking |
| **Tampering** | Integrity | Modifying data or code without authorization | SQL injection, cross-site scripting, man-in-the-middle attacks, binary patching, log tampering |
| **Repudiation** | Non-repudiation | Claiming to have not performed an action | Deleting audit logs, denying transactions, forging timestamps, unsigned actions |
| **Information Disclosure** | Confidentiality | Exposing information to unauthorized parties | Data leakage, error messages revealing internals, directory traversal, unencrypted transmission, side-channel attacks |
| **Denial of Service** | Availability | Denying access to a resource or service | Resource exhaustion, algorithmic complexity attacks, amplification attacks, deadlocks, race conditions |
| **Elevation of Privilege** | Authorization | Gaining capabilities beyond what is authorized | Buffer overflows, privilege escalation, insecure direct object references, missing function-level access control |

#### STRIDE Application Process

1. **Decompose the system:** Create data flow diagrams (DFDs) identifying processes, data stores, data flows, external entities, and trust boundaries.
2. **Apply STRIDE per element:** For each DFD element, systematically consider each STRIDE category.
3. **Document threats:** Record each identified threat with its category, affected component, and description.
4. **Prioritize:** Use DREAD or another scoring method to prioritize threats.
5. **Mitigate:** Define countermeasures for prioritized threats.

#### STRIDE per Element (Refined Approach)

| DFD Element | Applicable STRIDE Categories |
|-------------|------------------------------|
| External Entity | S, R |
| Process | S, T, R, I, D, E (all 6) |
| Data Store | T, R, I, D |
| Data Flow | T, I, D |
| Trust Boundary | (Threats occur at boundary crossings) |

#### Strengths and Weaknesses

| Strengths | Weaknesses |
|-----------|------------|
| Systematic -- covers all 6 security properties | Does not include risk scoring (needs DREAD or CVSS) |
| Well-understood -- extensive industry adoption | Can generate large numbers of threats without prioritization |
| Easy to learn -- minimal training required | Does not address privacy threats (need LINDDUN) |
| Maps to security controls -- each category implies countermeasures | DFD creation can be time-consuming for large systems |
| Suitable for automation -- checklist approach works well for agents | Does not model attack paths (needs Attack Trees) |

### DREAD (Microsoft, ~2002)

#### Overview

DREAD is a risk scoring methodology developed at Microsoft to complement STRIDE. It provides a quantitative score for each identified threat, enabling prioritization.

#### The 5 DREAD Dimensions

| Dimension | Question | Score Range | Scoring Guide |
|-----------|----------|-------------|---------------|
| **Damage** | How much damage would the attack cause? | 1-10 | 1 = minimal impact; 5 = individual user compromise; 10 = complete system destruction |
| **Reproducibility** | How easy is it to reproduce the attack? | 1-10 | 1 = very difficult, requires specific conditions; 5 = requires specific tools; 10 = trivially reproducible |
| **Exploitability** | How easy is it to launch the attack? | 1-10 | 1 = requires advanced custom tooling; 5 = requires existing tools with configuration; 10 = script kiddie level |
| **Affected Users** | How many users are impacted? | 1-10 | 1 = single user under rare conditions; 5 = subset of users; 10 = all users |
| **Discoverability** | How easy is it to discover the vulnerability? | 1-10 | 1 = requires source code access; 5 = discoverable by network monitoring; 10 = visible in browser address bar |

#### DREAD Score Calculation

**Formula:** DREAD Score = (D + R + E + A + D) / 5

| Score Range | Risk Level | Action |
|-------------|------------|--------|
| 0-3 | Low | Monitor, address in normal development cycle |
| 4-6 | Medium | Address in upcoming sprint/release |
| 7-10 | High/Critical | Address immediately, consider emergency patch |

#### Strengths and Weaknesses

| Strengths | Weaknesses |
|-----------|------------|
| Quantitative -- produces a comparable numeric score | Subjective -- different analysts may score differently |
| Simple -- 5 clear dimensions, easy to understand | Discoverability dimension is controversial (assumes security through obscurity has value) |
| Prioritization -- enables risk-based ordering | No formal calibration method for scoring consistency |
| Complementary -- pairs naturally with STRIDE | Microsoft itself has moved toward CVSS for some uses |
| Agent-friendly -- consistent rubrics enable automated scoring | Scores can be gamed by adjusting individual dimensions |

#### DREAD for Agentic Context

The subjectivity criticism of DREAD is mitigated in an agentic context because:
1. eng-architect can apply consistent scoring rubrics (unlike human teams with varying expertise)
2. Scoring criteria can be codified as rules in the agent definition
3. Multiple scoring rounds (via /adversary integration) can validate consistency
4. DREAD scores can be cross-referenced with CVSS where applicable

### PASTA (Process for Attack Simulation and Threat Analysis)

#### Overview

PASTA is a 7-stage, risk-centric threat modeling methodology that connects technical threats to business impact through attack simulation. Developed by Tony UcedaVelez and Marco Morana, PASTA provides the most comprehensive end-to-end threat modeling process.

#### The 7 PASTA Stages

| Stage | Name | Purpose | Key Activities | Outputs |
|-------|------|---------|----------------|---------|
| 1 | **Define Objectives** | Align threat modeling with business goals | Identify business objectives, security requirements, compliance requirements, risk tolerance | Business context document, compliance mapping, risk appetite statement |
| 2 | **Define Technical Scope** | Map the technical landscape | Application architecture mapping, technology stack identification, infrastructure dependencies, data flow analysis | Technical scope document, architecture diagrams, dependency maps |
| 3 | **Application Decomposition** | Understand application internals | User roles and permissions, asset identification, data classification, entry points and trust levels, DFD creation | Application decomposition, DFDs, asset inventory, trust boundary analysis |
| 4 | **Threat Analysis** | Identify potential threats | Threat intelligence gathering, threat library consultation (OWASP Top 10, CWE), attack pattern analysis, threat agent profiling | Threat catalogue, threat agent profiles, relevant attack patterns |
| 5 | **Vulnerability Analysis** | Identify exploitable weaknesses | Vulnerability scanning, code analysis, configuration review, vulnerability-to-threat correlation, attack tree construction | Validated vulnerability list, vulnerability-threat correlation, attack trees |
| 6 | **Attack Modeling** | Simulate attacks | Attack tree refinement, attack simulation, exploit path mapping, business impact assessment per attack path | Attack models, simulated attack paths, business impact scores |
| 7 | **Risk and Impact Analysis** | Quantify risk and define countermeasures | Risk scoring (combining likelihood and impact), countermeasure identification, residual risk assessment, remediation prioritization | Risk register, prioritized countermeasures, residual risk assessment, remediation roadmap |

#### PASTA vs. STRIDE Comparison

| Dimension | STRIDE | PASTA |
|-----------|--------|-------|
| Approach | Threat-centric (what can go wrong?) | Risk-centric (what is the business impact?) |
| Complexity | Low-Medium | High |
| Time investment | Hours | Days to weeks |
| Business alignment | Implicit | Explicit (stages 1, 6, 7) |
| Attack simulation | No | Yes (stage 6) |
| Vulnerability analysis | No (separate activity) | Integrated (stage 5) |
| Quantitative output | No (needs DREAD) | Yes (risk scores) |
| Best for | Standard application threat modeling | High-criticality systems, regulatory compliance |

#### Strengths and Weaknesses

| Strengths | Weaknesses |
|-----------|------------|
| End-to-end -- covers business context through remediation | Resource-intensive -- 7 stages require significant effort |
| Risk-centric -- connects threats to business impact | Complexity -- requires experienced practitioners |
| Attack simulation -- validates theoretical threats | Time-consuming -- days to weeks for full process |
| Evidence-based -- grounds findings in real threat intelligence | Overhead -- excessive for routine/low-criticality systems |
| Comprehensive -- integrates vulnerability analysis into threat modeling | Requires business stakeholder involvement (stages 1, 7) |

### LINDDUN (KU Leuven, 2011)

#### Overview

LINDDUN is a privacy-specific threat modeling framework developed by researchers at KU Leuven. It systematically identifies privacy threats, analogous to how STRIDE identifies security threats. LINDDUN has been recognized in ISO 27550 (Privacy Engineering for System Life Cycle Processes) and endorsed by the European Data Protection Supervisor.

#### The 7 LINDDUN Categories

| Category | Description | Privacy Property Violated | Examples |
|----------|-------------|---------------------------|----------|
| **Linking** | Ability to correlate data items to the same data subject without knowing identity | Unlinkability | Correlating browsing history across sites, linking anonymized datasets, behavioral profiling |
| **Identifying** | Revealing the identity behind pseudonymous or anonymous data | Anonymity / Pseudonymity | De-anonymization attacks, identity correlation, metadata analysis |
| **Non-repudiation** | Inability of users to deny their actions or data | Plausible deniability | Irrefutable audit trails, digital signatures binding identity to actions, blockchain immutability |
| **Detecting** | Discovering the existence of data or actions without accessing content | Undetectability | Traffic analysis revealing communication patterns, metadata exposure, timing attacks |
| **Disclosure of Information** | Unauthorized access to personal data content | Confidentiality | Data breaches, unauthorized API access, insider access to PII, unencrypted storage |
| **Unawareness** | Users not informed about data collection and processing | Transparency / Intervenability | Hidden data collection, unclear privacy policies, no consent management, no data portability |
| **Non-compliance** | Violation of privacy regulations and policies | Compliance | GDPR violations, HIPAA violations, CCPA non-compliance, data retention violations |

#### LINDDUN Application Process

1. **Define DFD:** Create data flow diagram (same as STRIDE)
2. **Map LINDDUN categories to DFD elements:** Systematic application per element
3. **Identify threat trees:** Use LINDDUN threat tree catalogue
4. **Prioritize threats:** Using risk assessment or misuse cases
5. **Define mitigations:** Select privacy-enhancing technologies (PETs) and controls

#### LINDDUN per Element Mapping

| DFD Element | Applicable Categories |
|-------------|----------------------|
| Entity | L, I, Nr, D, U, Nc |
| Process | L, I, Nr, D, Di, U, Nc (all 7) |
| Data Store | L, I, D, Di, U, Nc |
| Data Flow | L, I, D, Di |

#### When to Use LINDDUN

| Condition | Use LINDDUN? |
|-----------|--------------|
| Application processes PII under GDPR | YES -- mandatory privacy threat analysis |
| Application handles PHI under HIPAA | YES -- privacy is a regulatory requirement |
| Application subject to CCPA/CPRA | YES -- consumer privacy rights |
| Internal-only application, no PII | NO -- STRIDE sufficient |
| Infrastructure-only (no application data) | NO -- STRIDE sufficient |
| System with anonymization/pseudonymization | YES -- test effectiveness of privacy controls |

#### Strengths and Weaknesses

| Strengths | Weaknesses |
|-----------|------------|
| Privacy-specific -- covers threats STRIDE misses | Narrow scope -- only privacy, not general security |
| Regulatory alignment -- GDPR, HIPAA, CCPA | Less industry adoption than STRIDE |
| Academically rigorous -- developed at KU Leuven, ISO 27550 | Requires privacy expertise to apply effectively |
| Complementary to STRIDE -- fills confidentiality gap | DFD creation overhead (shared with STRIDE) |
| Threat tree catalogue -- structured threat identification | Limited tooling compared to STRIDE |

### Attack Trees (Bruce Schneier, 1999)

#### Overview

Attack Trees are hierarchical models of attacks against a system, with the attacker's goal as the root node and different ways of achieving that goal as child nodes. Formalized by Bruce Schneier in 1999 (building on earlier work by the defense industry), Attack Trees provide a visual, structured method for analyzing complex, multi-step attacks.

#### Structure

```
Root: Attacker Goal (e.g., "Compromise Admin Account")
├── OR: Exploit Authentication Weakness
│   ├── AND: Credential Stuffing
│   │   ├── Obtain Leaked Credential Database
│   │   └── Automate Login Attempts
│   ├── OR: Brute Force
│   │   ├── Dictionary Attack
│   │   └── Exhaustive Search
│   └── OR: Phishing
│       ├── Spear Phishing Email
│       └── Credential Harvesting Site
├── OR: Exploit Authorization Weakness
│   ├── IDOR (Insecure Direct Object Reference)
│   └── Privilege Escalation via Misconfigured RBAC
└── OR: Exploit Session Management
    ├── Session Fixation
    └── Session Hijacking via XSS
```

#### Key Concepts

| Concept | Description |
|---------|-------------|
| **Root Node** | The attacker's ultimate goal |
| **Leaf Nodes** | Atomic attack steps (cannot be further decomposed) |
| **AND Nodes** | All child nodes must succeed for this node to succeed |
| **OR Nodes** | Any one child node succeeding is sufficient |
| **Annotations** | Cost, difficulty, likelihood, tools required per node |
| **Pruning** | Removing infeasible branches based on attacker capability assumptions |

#### Attack Tree Analysis Types

| Analysis Type | Purpose |
|---------------|---------|
| **Boolean (Possible/Impossible)** | Mark each leaf as possible or impossible given attacker profile; propagate up |
| **Cost Analysis** | Assign cost to each leaf; calculate minimum cost attack path |
| **Probability Analysis** | Assign probability to each leaf; calculate overall attack probability |
| **Skill Level Analysis** | Assign required skill level; identify low-skill attack paths |
| **Detection Analysis** | Assign detection probability; identify stealthy attack paths |

#### Strengths and Weaknesses

| Strengths | Weaknesses |
|-----------|------------|
| Visual -- complex attacks become understandable | Not a complete methodology -- needs STRIDE/PASTA for threat identification |
| Analytical -- supports quantitative analysis (cost, probability) | Manual construction is time-consuming for large systems |
| Hierarchical -- naturally decomposes complex attacks | Can become unwieldy for systems with many attack vectors |
| Reusable -- subtrees can be reused across analyses | Requires attacker perspective expertise |
| Agent-friendly -- structured format is well-suited for LLM generation | No standard notation (multiple formats exist) |

### Comparative Summary

| Criterion | STRIDE | DREAD | PASTA | LINDDUN | Attack Trees |
|-----------|--------|-------|-------|---------|-------------|
| **Type** | Threat identification | Risk scoring | Full lifecycle | Privacy threats | Attack visualization |
| **Approach** | Security property-based | Quantitative scoring | Risk and business-centric | Privacy property-based | Goal-based decomposition |
| **Complexity** | Low | Low | High | Medium | Medium |
| **Time Investment** | Hours | Minutes per threat | Days-weeks | Hours-days | Hours per tree |
| **Output** | Threat list | Scored threat list | Risk register + countermeasures | Privacy threat list | Attack tree diagrams |
| **Automation Suitability** | High | High | Medium | Medium | High |
| **Standalone?** | Yes (with limitations) | No (needs threats from STRIDE/PASTA) | Yes (comprehensive) | Yes (privacy-specific) | No (needs threat source) |
| **Origin** | Microsoft (1999) | Microsoft (~2002) | UcedaVelez/Morana | KU Leuven (2011) | Schneier (1999) |
| **Best For** | Standard threat identification | Threat prioritization | High-criticality risk analysis | Privacy-regulated applications | Complex attack path analysis |

---

## Agent Mapping

### eng-architect Threat Modeling Workflow

eng-architect is the primary threat modeling agent. The recommended workflow integrates multiple methodologies:

| Step | Activity | Methodology | Criticality Trigger |
|------|----------|-------------|---------------------|
| 1 | Create Data Flow Diagram | (Shared prerequisite) | All levels |
| 2 | Systematic threat identification | **STRIDE** per element | All levels (C1-C4) |
| 3 | Privacy threat identification | **LINDDUN** | When PII/privacy regulations apply |
| 4 | Risk scoring | **DREAD** | C2+ |
| 5 | Complex attack path analysis | **Attack Trees** | C3+ (complex systems) |
| 6 | Business impact and attack simulation | **PASTA** (stages 4-7) | C4 (mission-critical) |
| 7 | Remediation prioritization | DREAD scores + business impact | All levels |

### Threat Modeling Integration with Other /eng-team Agents

| Agent | Threat Modeling Role | Interaction with eng-architect |
|-------|---------------------|-------------------------------|
| **eng-architect** | Primary: Creates threat models, identifies threats, scores risks | Owns the threat model as a deliverable |
| **eng-lead** | Reviews threat model, ensures coverage, validates priorities | Reviews and approves eng-architect's threat model |
| **eng-backend** | Implements mitigations for backend threats (injection, auth, crypto) | Receives threat mitigations from eng-architect as implementation requirements |
| **eng-frontend** | Implements mitigations for frontend threats (XSS, CSRF, CSP) | Receives threat mitigations from eng-architect as implementation requirements |
| **eng-infra** | Implements mitigations for infrastructure threats (misconfig, supply chain) | Receives threat mitigations from eng-architect as infrastructure requirements |
| **eng-security** | Validates that identified threats are mitigated, performs SAST/DAST against threat model | Uses eng-architect's threat model as a testing guide |
| **eng-qa** | Tests threat mitigations, creates security test cases from threat model | Creates test cases for each identified threat and its mitigation |
| **eng-reviewer** | Verifies threat model completeness and mitigation implementation | Uses eng-architect's threat model as a review checklist |

### Threat Modeling and /red-team Integration (Purple Team)

| Integration Point | Methodology Connection |
|-------------------|----------------------|
| eng-architect STRIDE output feeds red-vuln analysis | Red-vuln validates whether identified threats are actually exploitable |
| eng-architect Attack Trees feed red-exploit path planning | Red-exploit tests the attack paths eng-architect theorized |
| DREAD scores compared against red-team exploitation results | Validates scoring accuracy -- did high-DREAD threats actually prove exploitable? |
| LINDDUN threats tested by red-exfil | Red-exfil tests data disclosure, linking, and identification threats |

---

## Evidence and Citations

### Industry Leaders

| Source | Date | Content |
|--------|------|---------|
| [Microsoft -- Threat Modeling (STRIDE)](https://www.microsoft.com/en-us/securityengineering/sdl/threatmodeling) | 1999-present | Original STRIDE methodology from Microsoft SDL |
| [NIST -- LINDDUN Privacy Threat Modeling Framework](https://www.nist.gov/privacy-framework/linddun-privacy-threat-modeling-framework) | 2020 | NIST recognition of LINDDUN for privacy engineering |
| [OWASP -- PASTA Threat Modeling](https://owasp.org/www-pdf-archive/AppSecEU2012_PASTA.pdf) | 2012 | OWASP presentation of PASTA methodology |

### Industry Experts

| Source | Date | Content |
|--------|------|---------|
| [Security Compass -- STRIDE vs LINDDUN vs PASTA](https://www.securitycompass.com/blog/comparing-stride-linddun-pasta-threat-modeling/) | 2025 | Comprehensive methodology comparison |
| [Software Secured -- Comparison of STRIDE, DREAD, PASTA](https://www.softwaresecured.com/post/comparison-of-stride-dread-pasta) | 2025 | Side-by-side methodology comparison |
| [VerSprite -- PASTA Threat Modeling 7 Steps](https://versprite.com/blog/what-is-pasta-threat-modeling/) | 2025 | Detailed PASTA stage breakdown (VerSprite developed PASTA) |
| [Aptori -- STRIDE vs PASTA](https://www.aptori.com/blog/stride-vs-pasta-a-comparison-of-threat-modeling-methodologies) | 2025 | Methodology comparison with selection guidance |
| [Blue Goat Cyber -- DREAD vs STRIDE vs PASTA for Medical Devices](https://bluegoatcyber.com/blog/comparing-dread-stride-and-pasta-threat-models-which-is-most-effective/) | 2025 | Domain-specific comparison |

### Industry Innovators

| Source | Date | Content |
|--------|------|---------|
| [ThreatModeler -- PASTA Methodology](https://threatmodeler.com/glossary/pasta-threat-methodology/) | 2025 | PASTA tooling and automation |
| [IriusRisk -- PASTA Threat Modeling](https://www.iriusrisk.com/resources-blog/pasta-threat-modeling-methodologies) | 2025 | PASTA automation tooling perspective |
| [Drata -- PASTA Tutorial and Best Practices](https://drata.com/grc-central/risk/pasta-threat-modeling) | 2025 | PASTA practical implementation guide |

### Community Experts

| Source | Date | Content |
|--------|------|---------|
| [LINDDUN.org](https://linddun.org/) | 2025 | Official LINDDUN framework documentation |
| [LINDDUN Privacy Threat Categories](https://linddun.org/linddun-go-categories/) | 2025 | Detailed category descriptions |
| [TechRxiv -- Comparative Analysis of Threat Modelling Methods](https://www.techrxiv.org/users/845749/articles/1234181-a-comparative-analysis-of-threat-modelling-methods-stride-dread-vast-pasta-octave-and-linddun) | 2024 | Academic comparative analysis (Dr. Nitin Naik) |
| [Cloud Audit Controls -- Integrating STRIDE, DREAD, LINDDUN, and PASTA](https://www.cloudauditcontrols.com/2025/12/protect-integrating-stride-dread.html) | 2025-12 | Multi-methodology integration approach |

### Community Innovators

| Source | Date | Content |
|--------|------|---------|
| [EC-Council -- Attack Trees in Cybersecurity](https://www.eccouncil.org/cybersecurity-exchange/threat-intelligence/attack-trees-cybersecurity/) | 2024 | Attack Tree practical guide |
| [Amenaza Technologies -- Attack Tree Origins](https://www.amenaza.com/attack-tree-origins.php) | 2024 | Historical context for Attack Trees |
| [CBTW -- Threat Modeling Method Selection](https://cbtw.tech/insights/threat-modeling-which-method-should-you-choose-for-your-company-stride-dread-qtmm-linddun-pasta) | 2025 | Practitioner selection guide |

### Community Leaders

| Source | Date | Content |
|--------|------|---------|
| [Bruce Schneier -- Attack Trees (Dr. Dobb's Journal)](https://www.sciepub.com/reference/5472) | 1999 | Original Attack Trees paper |
| [FireCompass -- Bruce Schneier on AI, Attack Trees, and Pen Testing](https://firecompass.com/ai-in-cybersecurity-bruce-schneier/) | 2025 | Schneier's perspectives on AI and attack tree evolution |
| [O'Reilly -- Threat Modeling Chapter 4: Attack Trees](https://www.oreilly.com/library/view/threat-modeling/9781118810057/c04.xhtml) | 2014 | Adam Shostack's authoritative threat modeling book |

---

## Recommendations

### R1: STRIDE + DREAD as Default Threat Modeling Methodology

eng-architect SHOULD use STRIDE for threat identification and DREAD for risk scoring as the default threat modeling methodology. This combination provides:
- Systematic threat identification (STRIDE's 6 categories cover all security properties)
- Quantitative risk prioritization (DREAD's 5-dimension scoring)
- Low overhead (suitable for C1-C4 criticality levels)
- High automation suitability (checklist-based approach works well for agents)

### R2: Criticality-Based Methodology Escalation

eng-architect SHOULD select additional methodologies based on engagement criticality:

| Criticality | Methodologies | Rationale |
|-------------|---------------|-----------|
| C1 (Routine) | STRIDE only | Quick threat identification sufficient |
| C2 (Standard) | STRIDE + DREAD | Risk scoring enables prioritization |
| C3 (Significant) | STRIDE + DREAD + Attack Trees | Complex systems need attack path visualization |
| C4 (Critical) | STRIDE + DREAD + Attack Trees + PASTA (stages 4-7) | Mission-critical systems need full business impact analysis |

### R3: LINDDUN for Privacy-Regulated Applications

eng-architect SHOULD invoke LINDDUN when the system processes PII subject to privacy regulations (GDPR, HIPAA, CCPA, CPRA). LINDDUN should be applied in addition to STRIDE, not as a replacement. The determination of whether LINDDUN applies should be part of the initial scoping phase.

### R4: Attack Trees as Standard Visualization for Complex Attacks

eng-architect SHOULD produce Attack Trees for any threat that involves multi-step exploitation, vulnerability chaining, or complex attack paths. Attack Trees should be:
- Generated as part of the threat model deliverable
- Annotated with cost, skill level, and detection probability
- Used as input for eng-qa test case generation
- Fed to /red-team agents for purple team validation

### R5: DREAD Scoring Rubric Standardization

To address DREAD's subjectivity weakness, eng-architect SHOULD use a standardized scoring rubric with explicit criteria for each dimension and score level. This rubric should be:
- Defined in the /eng-team rule set
- Configurable per R-011 (organizations may have their own risk scoring frameworks)
- Validated through /adversary integration for C2+ deliverables

### R6: Configurable Methodology Selection (R-011 Compliance)

Per R-011 (Configurable Rule Sets), users MUST be able to override the default STRIDE+DREAD methodology with organization-specific threat modeling frameworks. eng-architect should support:
- STRIDE replacement (e.g., organization uses OCTAVE instead)
- DREAD replacement (e.g., organization uses CVSS-based scoring)
- Additional methodology plugins (e.g., organization requires VAST for agile environments)
- Custom threat categories beyond the standard STRIDE/LINDDUN sets

### R7: Threat Model as a Living Document

eng-architect SHOULD treat the threat model as a living document that is updated throughout the development lifecycle:
- Initial threat model during architecture phase
- Updated during implementation as new threats are identified
- Validated during security testing (eng-security)
- Retested during purple team validation (/red-team)
- Updated post-engagement with lessons learned
