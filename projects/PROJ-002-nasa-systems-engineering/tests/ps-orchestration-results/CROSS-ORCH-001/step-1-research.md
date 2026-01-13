# Verification and Validation Best Practices for AI-Integrated Space Mission Systems

**Document ID:** CROSS-ORCH-001-STEP-1
**Author:** ps-researcher (Jerry Framework)
**Date:** 2026-01-11
**Status:** Complete
**Pattern:** Sequential Cross-Family (ps-researcher -> nse-requirements)

---

## L0: Executive Summary

This literature review examines the current state of Verification and Validation (V&V) practices for autonomous systems and AI integration in space missions. The research identifies a significant gap between traditional V&V methodologies designed for deterministic systems and the emerging requirements for AI/ML-based autonomous spacecraft systems.

### Key Findings Summary

1. **Standard Evolution:** NASA and ESA standards (NASA-STD-7009B, NASA-STD-8739.8B, ECSS-E-ST-40C Rev.1) are actively being updated but lag behind AI/ML adoption curves
2. **Non-Determinism Challenge:** Traditional V&V assumes input A produces output B; AI systems require probabilistic acceptance criteria
3. **Readiness Framework Gap:** Space Trusted Autonomy Readiness Levels (STAR Levels) provide a maturity model but lack binding verification requirements
4. **Continuous V&V Paradigm:** ESA proposes shifting from pre-launch complete verification to continuous post-deployment validation
5. **Tool Ecosystem:** NASA FRET v3.0 introduces probabilistic requirements formalization but integration with AI systems remains nascent

### Critical Gap Analysis

| Domain | Traditional V&V | AI-Specific Need | Gap Severity |
|--------|----------------|------------------|--------------|
| Requirements | Deterministic specifications | Probabilistic constraints | HIGH |
| Testing Coverage | 100% path coverage | Statistical confidence bounds | HIGH |
| Runtime Verification | Not required | Continuous monitoring | MEDIUM |
| Explainability | N/A | Mandatory for anomaly diagnosis | HIGH |
| Safety Standards | Mature (DO-178C) | No equivalent for AI (EASA Level 1-2 only) | CRITICAL |

---

## L1: Technical Details

### 1. Current NASA Standards for AI/ML System Verification

#### NASA-STD-7009B: Standard for Models and Simulations (March 2024)

The latest revision (NASA-STD-7009B) establishes uniform practices for modeling and simulation credibility assessment using the Credibility Assessment Scale (CAS). Key provisions:

- **Verification:** Process of determining extent to which M&S complies with requirements and specifications
- **Validation:** Process of determining degree to which M&S accurately represents real-world from perspective of intended uses
- **Uncertainty Characterization:** Mandatory characterization of uncertainty in M&S results throughout lifecycle

**Source:** [NASA-STD-7009B (March 2024)](https://standards.nasa.gov/sites/default/files/standards/NASA/B/1/NASA-STD-7009B-Final-3-5-2024.pdf)

**Gap:** The standard was designed for physics-based simulations, not data-driven ML models. Uncertainty quantification methods differ fundamentally between deterministic simulations and stochastic neural networks.

#### NASA-STD-8739.8B: Software Assurance and Software Safety Standard (September 2022)

Defines systematic approach to Software Assurance (SA), software safety, and Independent Verification & Validation (IV&V):

- Applies to all software lifecycle phases for NASA-developed or acquired software
- Addresses safety-critical software identification and hazard analysis
- Requires fault tolerance and redundancy for safety-critical functions

**Source:** [NASA-STD-8739.8B (2022)](https://standards.nasa.gov/standard/NASA/NASA-STD-87398)

**Gap:** No explicit provisions for AI/ML systems. The standard assumes explicitly programmed, deterministic software where V&V has "a well-established set of standard tools and techniques that have been used for decades."

#### NPR 7150.2D: NASA Software Engineering Requirements

Current procedural requirements for software engineering, acquisition, development, maintenance, and operations:

- References IEEE 1012 for Software V&V standards
- Integrates with NASA-STD-8739.8 for safety assurance
- Requires software to be "verifiable, validated, and explainable"

**Source:** [NPR 7150.2D](https://nodis3.gsfc.nasa.gov/displayDir.cfm?t=NPR&c=7150&s=2D)

**Gap:** Acknowledges AI/ML challenges but defers to future guidance. States: "For systems which require 100% deterministic confidence, an AI/ML system may not be recommended."

#### NPR 8000.4C: Agency Risk Management Procedural Requirements (April 2022)

Framework for Risk-Informed Decision Making (RIDM) and Continuous Risk Management (CRM):

- Covers safety, mission success, physical security, and cybersecurity risks
- Aligns with NIST Framework for Critical Infrastructure Cybersecurity
- Requires risk acceptance delegation through NASA Technical Authority

**Source:** [NPR 8000.4C (April 2022)](https://explorers.larc.nasa.gov/2023APPROBE/pdf_files/19_NPR%208000.4C%20AgencyRiskMngmt.pdf)

**Gap:** Risk framework assumes quantifiable risk metrics; AI system failure modes are often emergent and difficult to quantify a priori.

### 2. ESA/NASA Joint Approaches to Autonomous System Validation

#### Collaborative GNC V&V Initiative

NASA and ESA, along with DLR and ONERA, have established collaboration on Guidance, Navigation, and Control (GNC) V&V:

- Shared technical language and vision for autonomous GNC
- Driving interests: faster implementation timelines, reduced mission operations support
- Joint recognition: 80% of spacecraft project time spent on V&V activities

**Source:** [NESC Verification and Validation Challenges for Autonomous GNC Technology](https://www.nasa.gov/centers-and-facilities/nesc/verification-and-validation-challenges-for-autonomous-gnc-technology-for-nasas-next-generation-missions/)

#### ESA Verification and Validation Philosophy for Autonomous Systems

ESA proposes paradigm shift for adaptive/evolving systems:

1. **Traditional V&V Insufficiency:** "The traditional process for V&V is not sufficient anymore and needs rethinking"
2. **Risk-Accepted Deployment:** "Basic" examination up to Acceptance Review with acceptable "open" risk
3. **Continuous Examination:** "Periodic" or "continuous" examinations after launch
4. **Digital Twin Integration:** System-level Simulation Facilities for supporting V&V and operations

**Source:** [ESA Nebula - Verification and Validation of Autonomous Systems](https://nebula.esa.int/content/verification-and-validation-autonomous-systems)

**Key Insight:** ESA explicitly acknowledges "it might no longer be possible to run through all possible test scenarios before launch."

#### ECSS Standards Update (April 2025)

European Cooperation for Space Standardization released critical updates:

- **ECSS-E-ST-40C Rev.1:** Space engineering - Software (30 April 2025)
- **ECSS-Q-ST-80C Rev.2:** Software product assurance (30 April 2025)
- **ECSS-E-ST-10-02C Rev.1:** Verification requirements

**Source:** [ECSS Active Standards](https://ecss.nl/standards/active-standards/)

**Challenge Noted:** "Unlike conventional infrastructure components governed by established standards, AI systems lack clear functional requirements and traceability frameworks, especially when developed iteratively."

### 3. Industry Best Practices for Verifying Non-Deterministic Systems

#### DO-178C and DO-333 Formal Methods (Aviation Domain)

DO-178C is the primary certification standard for commercial aerospace software:

- DO-333 supplement provides formal methods guidance
- Mathematical proofs can replace certain testing requirements
- NASA case studies demonstrate theorem proving, model checking, abstract interpretation

**Source:** [NASA DO-333 Formal Methods Case Studies](https://ntrs.nasa.gov/citations/20140004055)

**Gap for AI:** DO-178C designed for traditional (non-ML) software. EASA published initial guidance for Level 1-2 ML applications (2021-2023), but comprehensive AI certification framework pending.

#### Space Trusted Autonomy Readiness Levels (STAR Levels)

Joint framework developed by USSF, NASA, and NRO:

- Two-dimensional scale: readiness and trust
- Addresses multiple trustor communities: developers, operators, consumers
- Acknowledges impossibility of complete terrestrial space condition replication

**Source:** [Space Trusted Autonomy Readiness Levels (IEEE 2023)](https://ntrs.nasa.gov/citations/20220012680)

**Application Example:** NASA Orion Artemis Missions OpNav - first autonomous safety-critical on-board navigation system.

#### NASA FRET: Formal Requirements Elicitation Tool v3.0

NASA-developed tool for formal requirements specification:

- FRETISH language for structured natural language requirements
- **New in v3.0:** Probability field for probabilistic constraints
- Automatic formalization to probabilistic temporal logics
- Integration with PRISM model checker
- Automated test case generation via Kind 2 and NuSMV engines

**Source:** [NASA FRET GitHub](https://github.com/NASA-SW-VnV/fret)

**Significance:** First NASA tool to directly support probabilistic requirements specification, critical for AI system V&V.

#### PropCheck Formal Verification (JPL)

JPL engineers used formal verification-based PropCheck tool for Mars 2020 Perseverance lander software:

- Guaranteed software would not malfunction based on internal bugs/flaws
- Model checking approach for safety-critical flight software
- Demonstrated practical application of formal methods in space domain

**Source:** [Current Robotics Reports - V&V for Space Autonomous Systems](https://link.springer.com/article/10.1007/s43154-021-00058-1)

### 4. Gap Analysis: Traditional V&V vs. AI-Specific Requirements

#### Fundamental Incompatibilities

| Aspect | Traditional V&V | AI/ML Systems | Requirement Gap |
|--------|----------------|---------------|-----------------|
| **Behavior Specification** | Complete pre-operation specification | Emergent from training data | Need runtime behavior bounds |
| **Test Completeness** | Path coverage metrics | Distributional coverage | Statistical acceptance criteria |
| **Repeatability** | Deterministic execution | Stochastic inference | Reproducibility protocols |
| **Failure Modes** | Enumerable | Emergent, novel | Anomaly detection requirements |
| **Certification Evidence** | Code-level analysis | Training data + architecture | Data assurance standards |
| **Runtime Monitoring** | Optional logging | Mandatory confidence tracking | OOD detection requirements |

#### NASA-Identified Challenges

From NASA Software Engineering Handbook Section 7.25 (AI and Software Engineering):

1. "Can't test how the AI would react to every possible situation"
2. "No way to quantify confidence in some techniques (non-deterministic)"
3. "Currently no safety standards for AI on manned-flight missions"
4. "Software needs to be verifiable, validated, AND explainable"

**Source:** [NASA SW Engineering Handbook - AI Section](https://swehb.nasa.gov/display/SWEHBVD/7.25+-+Artificial+Intelligence+And+Software+Engineering)

#### Formal Verification Limitations for AI

Fundamental barriers to formal verification of AI systems:

- Complexity and heterogeneity make general formal verification undecidable
- Non-deterministic modeling produces over-approximate models with spurious bug reports
- AI systems require probabilistic modeling due to distributional environment assumptions
- High-level temporal specifications assume deterministic low-level properties (unrealistic for real sensors)

**Source:** [Towards Verified Artificial Intelligence](https://arxiv.org/pdf/1606.08514)

---

## L2: Strategic Implications and Recommendations

### Emerging Consensus Points

1. **Hybrid V&V Approach:** Combination of formal methods, statistical testing, and runtime monitoring
2. **Continuous Validation:** Shift from pre-launch completeness to lifecycle verification
3. **Explainability Mandate:** AI systems must support post-hoc analysis for anomaly diagnosis
4. **Probabilistic Requirements:** FRET-style tools enabling formal probabilistic constraints
5. **Digital Twin Integration:** ESA-endorsed simulation facilities for ongoing V&V

### Requirements Derivation Guidance (for nse-requirements)

Based on this research, the following requirement categories should be derived:

#### Category A: Requirements Specification Standards
- REQ-A1: AI system requirements SHALL include probabilistic acceptance bounds
- REQ-A2: Requirements SHALL be expressible in formal temporal logics with probability extensions
- REQ-A3: Safety-critical AI functions SHALL have deterministic fallback modes specified

#### Category B: Verification Process Requirements
- REQ-B1: AI systems SHALL undergo credibility assessment per NASA-STD-7009B CAS framework
- REQ-B2: V&V plans SHALL include statistical confidence bounds for test coverage
- REQ-B3: Formal methods SHALL be applied to safety-critical AI decision boundaries

#### Category C: Runtime Monitoring Requirements
- REQ-C1: AI systems SHALL implement out-of-distribution detection mechanisms
- REQ-C2: Inference confidence metrics SHALL be logged for post-flight analysis
- REQ-C3: Continuous validation infrastructure SHALL be provisioned for post-deployment monitoring

#### Category D: Safety Assurance Requirements
- REQ-D1: AI systems SHALL comply with NASA-STD-8739.8B software safety provisions
- REQ-D2: Safety-critical AI SHALL implement graceful degradation to deterministic backup
- REQ-D3: AI training data SHALL be curated per software assurance lifecycle requirements

#### Category E: Explainability Requirements
- REQ-E1: AI decision outputs SHALL include attribution/explanation artifacts
- REQ-E2: Systems SHALL support anomaly reconstruction for failure analysis
- REQ-E3: AI architecture documentation SHALL enable independent audit

### Stakeholder Clarification Needed

The following gaps require stakeholder input before requirements finalization:

1. **Risk Appetite:** What "acceptable open risk" level applies to post-launch continuous V&V?
2. **Determinism Requirements:** Which mission phases mandate deterministic-only operation?
3. **Explainability Depth:** What level of AI decision attribution satisfies flight readiness?
4. **Data Assurance:** What training data provenance documentation is required?
5. **STAR Level Target:** What minimum STAR level is required for autonomous capabilities?

---

## References

### Primary NASA Standards
1. [NASA-STD-7009B: Standard for Models and Simulations (March 2024)](https://standards.nasa.gov/sites/default/files/standards/NASA/B/1/NASA-STD-7009B-Final-3-5-2024.pdf)
2. [NASA-STD-8739.8B: Software Assurance and Software Safety Standard](https://standards.nasa.gov/standard/NASA/NASA-STD-87398)
3. [NPR 7150.2D: NASA Software Engineering Requirements](https://nodis3.gsfc.nasa.gov/displayDir.cfm?t=NPR&c=7150&s=2D)
4. [NPR 8000.4C: Agency Risk Management (April 2022)](https://explorers.larc.nasa.gov/2023APPROBE/pdf_files/19_NPR%208000.4C%20AgencyRiskMngmt.pdf)

### NASA Technical Reports
5. [Autonomy V&V Roadmap and Vision 2045](https://ntrs.nasa.gov/citations/20230003734)
6. [Space Trusted Autonomy Readiness Levels (STAR)](https://ntrs.nasa.gov/citations/20220012680)
7. [DO-333 Formal Methods Case Studies](https://ntrs.nasa.gov/citations/20140004055)
8. [Challenges in V&V of Autonomous Systems for Space Exploration](https://ntrs.nasa.gov/citations/20050238987)

### ESA/European Standards
9. [ESA Nebula: V&V of Autonomous Systems](https://nebula.esa.int/content/verification-and-validation-autonomous-systems)
10. [ECSS-E-ST-40C Rev.1: Software (April 2025)](https://ecss.nl/standard/ecss-e-st-40c-rev-1-software-30-april-2025/)
11. [ESA Artificial Intelligence in Space](https://www.esa.int/Enabling_Support/Preparing_for_the_Future/Discovery_and_Preparation/Artificial_intelligence_in_space)

### Tools and Methods
12. [NASA FRET: Formal Requirements Elicitation Tool](https://github.com/NASA-SW-VnV/fret)
13. [V&V Review for Space Autonomous Systems (Springer)](https://link.springer.com/article/10.1007/s43154-021-00058-1)

### Aviation Standards (Cross-Reference)
14. [DO-178C Wikipedia](https://en.wikipedia.org/wiki/DO-178C)
15. [DO-333 Formal Methods Introduction](https://visuresolutions.com/aerospace-and-defense/do-333/)

---

## session_context

```yaml
schema_version: "1.0.0"
session_id: "cross-orch-001-test"
source_agent: ps-researcher
target_agent: nse-requirements
timestamp: "2026-01-11T00:00:00Z"
handoff_type: sequential_cross_family
pattern: ps-researcher -> nse-requirements

payload:
  document_type: literature_review
  document_id: CROSS-ORCH-001-STEP-1

  key_findings:
    - id: KF-001
      category: standards_gap
      finding: "NASA-STD-7009B credibility assessment designed for physics-based simulations, not ML models"
      source: "NASA-STD-7009B (March 2024)"
      requirement_implication: "REQ: AI systems require ML-specific credibility assessment criteria"
      traceability: "NASA-STD-7009B Section 4"

    - id: KF-002
      category: standards_gap
      finding: "NASA-STD-8739.8B has no explicit AI/ML provisions for safety-critical software"
      source: "NASA-STD-8739.8B (September 2022)"
      requirement_implication: "REQ: Supplementary AI safety assurance requirements needed"
      traceability: "NASA-STD-8739.8B"

    - id: KF-003
      category: paradigm_shift
      finding: "ESA proposes continuous post-deployment V&V with acceptable 'open risk' at launch"
      source: "ESA Nebula - V&V of Autonomous Systems"
      requirement_implication: "REQ: Runtime monitoring and continuous validation infrastructure"
      traceability: "ESA V&V Philosophy"

    - id: KF-004
      category: tool_capability
      finding: "NASA FRET v3.0 introduces probabilistic requirements formalization"
      source: "NASA-SW-VnV/fret GitHub"
      requirement_implication: "REQ: Requirements SHALL support probabilistic temporal logic"
      traceability: "FRET v3.0 Release Notes"

    - id: KF-005
      category: non_determinism
      finding: "100% deterministic confidence not achievable for AI; statistical bounds required"
      source: "NASA SW Engineering Handbook 7.25"
      requirement_implication: "REQ: Statistical acceptance criteria for AI test coverage"
      traceability: "NASA SWEHB 7.25"

    - id: KF-006
      category: safety_critical
      finding: "No safety standards exist for AI on manned-flight missions"
      source: "NASA SW Engineering Handbook 7.25"
      requirement_implication: "REQ: Deterministic fallback modes for safety-critical AI"
      traceability: "NASA SWEHB 7.25"

    - id: KF-007
      category: explainability
      finding: "Software must be verifiable, validated, AND explainable for anomaly diagnosis"
      source: "NASA SW Engineering Handbook 7.25"
      requirement_implication: "REQ: AI decision attribution and explanation artifacts"
      traceability: "NASA SWEHB 7.25"

    - id: KF-008
      category: readiness_framework
      finding: "STAR Levels provide maturity model but lack binding verification requirements"
      source: "NTRS 20220012680"
      requirement_implication: "REQ: Define minimum STAR level thresholds for mission phases"
      traceability: "IEEE Aerospace 2023"

    - id: KF-009
      category: formal_methods
      finding: "Formal verification generally undecidable for AI due to complexity/non-determinism"
      source: "arXiv 1606.08514"
      requirement_implication: "REQ: Hybrid V&V combining formal methods with statistical testing"
      traceability: "Towards Verified AI"

    - id: KF-010
      category: european_standards
      finding: "ECSS-E-ST-40C Rev.1 updated April 2025 but AI traceability frameworks missing"
      source: "ECSS.nl"
      requirement_implication: "REQ: AI-specific traceability framework aligned with ECSS"
      traceability: "ECSS-E-ST-40C Rev.1"

  gaps_requiring_clarification:
    - gap_id: GAP-001
      topic: "Risk Appetite"
      question: "What 'acceptable open risk' level applies to post-launch continuous V&V?"
      stakeholders: ["Safety Engineering", "Mission Assurance"]

    - gap_id: GAP-002
      topic: "Determinism Requirements"
      question: "Which mission phases mandate deterministic-only operation?"
      stakeholders: ["Flight Operations", "Safety Engineering"]

    - gap_id: GAP-003
      topic: "Explainability Depth"
      question: "What level of AI decision attribution satisfies flight readiness?"
      stakeholders: ["Independent V&V", "Flight Directors"]

    - gap_id: GAP-004
      topic: "Data Assurance"
      question: "What training data provenance documentation is required?"
      stakeholders: ["Data Engineering", "Quality Assurance"]

    - gap_id: GAP-005
      topic: "STAR Level Target"
      question: "What minimum STAR level is required for autonomous capabilities?"
      stakeholders: ["Program Management", "Mission Assurance"]

  recommended_requirement_categories:
    - category_id: CAT-A
      name: "Requirements Specification Standards"
      count: 3
      priority: high

    - category_id: CAT-B
      name: "Verification Process Requirements"
      count: 3
      priority: high

    - category_id: CAT-C
      name: "Runtime Monitoring Requirements"
      count: 3
      priority: medium

    - category_id: CAT-D
      name: "Safety Assurance Requirements"
      count: 3
      priority: critical

    - category_id: CAT-E
      name: "Explainability Requirements"
      count: 3
      priority: high

  metadata:
    research_date: "2026-01-11"
    sources_cited: 15
    key_findings_count: 10
    gaps_identified: 5
    requirement_categories: 5
```

---

**END OF DOCUMENT**

*This document was generated by ps-researcher as Step 1 of CROSS-ORCH-001 Cross-Family Interoperability Test. The session_context block above contains structured data for handoff to nse-requirements agent.*
