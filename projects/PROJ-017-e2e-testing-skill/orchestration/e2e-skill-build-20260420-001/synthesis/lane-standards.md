---
agent: ps-synthesizer-standards
phase: 1c
workflow: e2e-skill-build-20260420-001
inputs_count: 5
date: 2026-04-21
project: PROJ-017-e2e-testing-skill
gate_upstream: phase1b-score.md (0.947 PASS)
---

# Phase 1c Standards Lane Synthesis

> Synthesizes 5 deep-dive standards research files into a unified view for the /e2e-testing skill.
> This document is the "standards half" input to the Phase 2 master synthesis.

## Document Sections

| Section | Purpose |
|---------|---------|
| [1. Cross-File Comparison Matrix](#1-cross-file-comparison-matrix) | Standards at a glance across key dimensions |
| [2. Distilled Common Themes](#2-distilled-common-themes) | 5 themes emerging across 2+ standards |
| [3. Contradictions and Tensions](#3-contradictions-and-tensions) | Where the standards pull in different directions |
| [4. Coverage Gaps for Web-Service E2E](#4-coverage-gaps-for-web-service-e2e) | What the 5 standards collectively leave unspecified |
| [5. Recommended Standards Posture](#5-recommended-standards-posture) | Which to align with, which to deviate from, and why |
| [6. Proposed Top-5 Distilled Principles](#6-proposed-top-5-distilled-principles) | The "standards half" of the final 10 skill principles |
| [7. Open Questions for Master Synthesis](#7-open-questions-for-master-synthesis) | What the innovators lane and eng-team baseline must resolve |
| [Source Files](#source-files) | Input files with one-line coverage notes |

---

**Synthesis Method:** All five input files (std-1 through std-5) were read in full before any theme, principle, or matrix entry was written. Themes required evidence from at least two distinct source files to be included; single-source observations are noted as gaps or tensions rather than confirmed themes. Applicability ratings in the matrix are assessed from the perspective of a Jerry E2E skill that orchestrates automated testing of web services using LLM-based agents, as stated in the matrix reading note below.

---

## 1. Cross-File Comparison Matrix

| Standard | Scope | Nature | Primary Authority | Current Version (2026) | Applicability to E2E of Web Services | Applicability to Agentic Flows | Cost to Adopt |
|----------|-------|--------|-------------------|------------------------|--------------------------------------|-------------------------------|---------------|
| **W3C WebDriver (Level 2)** | Browser remote-control wire protocol: HTTP/JSON endpoint families covering sessions, navigation, elements, actions, cookies, prompts, screenshots | Technical specification (protocol standard) | W3C Browser Testing and Tools Working Group; editors Simon Stewart (Apple), David Burns (BrowserStack) | Level 2 Working Draft dated 2026-04-01; Level 1 is REC; BiDi WD dated 2026-03-19 | **HIGH** — foundational cross-browser automation protocol; all E2E tooling (Selenium, Playwright, WebdriverIO, Cypress) builds on or conforms to it | **MEDIUM** — the synchronous HTTP model does not map to event-driven agent state machines; BiDi WebSockets are closer but still page-centric | Free; open spec; all major browser vendors ship conforming drivers |
| **ISO/IEC/IEEE 29119** | Software testing vocabulary, processes, documentation templates, test design techniques, keyword-driven testing, agile/AI/biometric testing guidelines | Multi-part process standard (8 parts) | ISO/IEC JTC 1/SC 7/WG 26 jointly with IEEE C/S2ESC | Parts 1-4: 2021-2022 editions; Part 5: 2024; Parts 6/11/13: 2020-2021 TRs | **HIGH** (process/documentation backbone) — Parts 2, 3, 4 provide the lifecycle model and artifact catalog; no web-specific or API-specific content | **LOW** — standard predates agentic paradigms; no oracle-problem or non-determinism guidance for agentic loops (Part 11 covers AI-under-test but not AI-as-tester) | Parts 1 and 11 are free; Parts 2-5, 6, 13 are paywalled at low-to-mid hundreds USD/CHF per part |
| **ISTQB CTFL + CTAL-TAE** | Testing fundamentals, SDLC integration, test design techniques, test automation architecture (gTAA), CI/CD integration, AI testing, testing with GenAI | Certification scheme with syllabi and glossary; not an ISO/IEEE standard | International Software Testing Qualifications Board; 60+ national Member Boards | CTFL v4.0.1 (Sep 2024); CTAL-TAE v2.0 (Jun 2024); CT-GenAI v1.0 (Jul 2025) | **HIGH** (vocabulary and architecture reference) — gTAA layers map directly to E2E toolchain; risk-based testing bridges to modern CI/CD gates | **MEDIUM** — CT-GenAI v1.0 (Jul 2025) explicitly addresses LLM agents in testing; CT-AI v2.0 covers AI-under-test; but gTAA layers were not designed for agentic orchestrators | Free to download (syllabi and glossary); exam/accreditation costs apply to human certification only |
| **OWASP WSTG** | Security-focused web application and web service testing: 12 categories, ~109 test cases covering auth, session, input validation, business logic, API, client-side | Security testing guide (open documentation standard) | OWASP Foundation (Flagship Project); community-maintained by Elie Saad and Rick Mitchell | Stable: v4.2 (released 2020-12-03); v5.0 in development (open milestone, no release date) | **HIGH** (security axis) — 12 categories with versioned test IDs cover the security surface of web services; BUSL and APIT chapters are uniquely well-suited to E2E | **HIGH** — Business Logic (BUSL) tests are inherently agentic: they require reasoning about workflow abuse, circumvention, and multi-step misuse that automated scanners cannot perform | Free; CC BY-SA 4.0 |
| **Cucumber / Gherkin** | Plain-text DSL for BDD scenarios: Given-When-Then grammar, Feature/Rule/Scenario structure, tags, Scenario Outline, data tables, localisation | De facto specification DSL (open source grammar, not ISO/IEEE standard) | Cucumber Open Source Project; community-governed since 2024 | Grammar: copyright 2014-2026 (living); Gherkin 6 (Rule keyword) is current; no numbered grammar version | **HIGH** (specification format) — Gherkin is the dominant format for executable E2E acceptance criteria across web service and UI testing stacks | **HIGH** — LLM-generated Gherkin scores 92-95% relevance in 2024-2025 peer-reviewed studies; ACM 2024 demonstrates multi-agent Gherkin execution without pre-authored step definitions | Free; open source; all implementations freely available |

**Reading note:** "Applicability" is rated from the perspective of a Jerry E2E skill that orchestrates automated testing of web services (UI + API layers) using LLM-based agents. A rating of HIGH means the standard contributes directly operative content; MEDIUM means it contributes relevant concepts requiring adaptation; LOW means minimal direct usefulness without significant bridging.

---

## 2. Distilled Common Themes

The following themes each appear in two or more of the five standards with substantive evidence. Themes are presented in descending order of cross-file coverage.

---

### Theme 1: Risk-Based Test Prioritisation as a First-Class Design Input

All three process-oriented standards (ISO 29119, ISTQB, OWASP WSTG) independently mandate risk-based reasoning as the primary driver of test selection and ordering. This is not optional guidance; in each case it is embedded in the core model.

- **ISO 29119-2** (std-2 §3 "High relevance"): "Design-Test-Strategy activity mandates explicit risk-based prioritisation as a first-class input to test-level and technique selection." The Part 2 process model requires test strategy to document product-risk (severity × likelihood) before any design step.
- **ISTQB CTFL v4.0** (std-3 §7.5): Risk-based testing is a named chapter (CTFL Ch. 5) and maps directly to "likelihood × impact" prioritisation. The mapping study cited in std-3 (Colomo-Palacios et al. [S5]) confirms CTFL's risk-based model is "largely covered by ISO 29119-2."
- **OWASP WSTG** (std-4 §1 and §2): WSTG is structured around threat-driven reasoning — the 12 categories represent a taxonomy of risk areas; the Testing Framework chapter positions threat modeling as the design step before test execution.
- **W3C WebDriver** (std-1 §5): Does not directly mandate risk-based ordering, but its standardised error taxonomy (P-WD-5) enables risk-aware triage by mapping failures to classes (e.g., `stale element reference` = flakiness risk; `element click intercepted` = concurrency risk).
- **Gherkin** (std-5 §7.1 and §7.3): Example Mapping's Rule-card structure implicitly encodes risk — examples illustrate rules in priority order, and open questions (red cards) surface risk to the backlog before scenarios are formalised.

**Synthesis verdict:** Risk-based prioritisation is the most consistent imperative across the standards lane. Any Jerry E2E skill that does not surface risk classification as an explicit early step — before test design — would be out of alignment with four of the five standards.

---

### Theme 2: Layered Test Automation Architecture with Separation of Concerns

Three standards independently converge on a layered model that separates test specification, test execution, and system-under-test interface. They use different vocabulary but describe structurally equivalent separations.

- **ISTQB CTAL-TAE v2.0** (std-3 §7.1): The Generic Test Automation Architecture (gTAA) explicitly specifies four horizontal layers: Test Generation, Test Definition, Test Execution, Test Adaptation. Execution and Adaptation are the minimum pair; upper layers are optional.
- **W3C WebDriver** (std-1 §7, P-WD-1): "Protocol layer isolation" mandates that skill operations be specified in WebDriver command vocabulary as an implementation-agnostic binding — the specification layer is separate from the driver binding.
- **Gherkin** (std-5 §7.4): Hexagonal BDD explicitly positions Gherkin scenarios at the driver-port level, with step definitions as primary adapters — mirroring the gTAA's Definition/Adaptation split. The principle is testable: step-definition files should import only from application/domain layers plus driver-port adapters, not directly from Selenium/Playwright APIs.
- **ISO 29119-2** (std-2 §3): The three-layer process model (Organisational / Test Management / Dynamic) is a meta-level instantiation of the same separation of concerns: policy governs strategy, strategy governs execution.
- **OWASP WSTG** (std-4 §7.3): The passive/active two-phase testing pattern is a lightweight separation between discovery (specification) and probing (execution) — a domain-specific instance of the same layering principle.

**Synthesis verdict:** Separation of specification from execution from interface is an independently derived consensus across four of the five standards. The Jerry E2E skill's architecture should encode this separation as a HARD constraint.

---

### Theme 3: Traceability — Every Test Artifact Links to a Test Basis

Four of the five standards require or strongly recommend that each test case be traceable to the artifact that justified it (requirement, user story, risk item, threat model, business rule). The vocabulary differs but the structural requirement is identical.

- **ISO 29119-3** (std-2 §7, P7): "Each Test Case Spec references (a) the Test Basis (requirement/user story), (b) the Test Condition, (c) the applied Test Design Technique." Annex T in Part 3 provides the mapping template.
- **ISTQB CTFL v4.0** (std-3 §3.1): CTFL's test analysis step explicitly requires tracing test conditions to the test basis; defect reports must reference the test case; test cases must reference their technique.
- **Gherkin / BDD** (std-5 §7.1): Example Mapping's principle — "scenarios MUST be derived from a Business-Development-Testing conversation over concrete examples" — is itself a traceability requirement. The Discovery artifact is the test basis for each Gherkin scenario.
- **OWASP WSTG** (std-4 §7.2): Each WSTG test uses a structured template (Summary, Test Objectives, Procedure, Remediation, References) that explicitly links the test to CWE IDs and RFCs — its own form of test-basis traceability.
- **W3C WebDriver** (std-1 §7, P-WD-5 and P-WD-10): WPT as conformance evidence is a vendor-level traceability mechanism; the skill's CI consulting wpt.fyi for the tested command/browser pair creates traceability from test failures to spec conformance.

**Synthesis verdict:** Traceability is universally expected across all five standards, though they express it differently. The Jerry skill should require every generated test artifact to declare its basis (story/risk/WSTG ID/Gherkin feature link) as a non-optional metadata field.

---

### Theme 4: Specification by Example as the Preferred Test Design Mode

The three standards closest to test specification (Gherkin, ISTQB, ISO 29119-4) independently endorse scenario-based and example-driven test design as the preferred technique for system/acceptance-level testing — which is precisely where E2E sits.

- **Gherkin** (std-5 §7.3): Specification by Example (Gojko Adzic lineage) is the explicit design philosophy: each Rule is illustrated by a minimum set of concrete examples covering positive and each boundary variation. `Scenario Outline` compresses data-varying examples.
- **ISO 29119-4** (std-2 §7, P9, P11): "For system/acceptance-level E2E, specification-based + experience-based techniques dominate." The technique catalog names "scenario testing, use-case testing" as the preferred specification-based techniques at E2E level; structure-based (white-box) techniques are inappropriate at E2E.
- **ISTQB CTFL v4.0** (std-3 §7.4): Use Case Testing and Scenario Testing are named E2E-aligned techniques; ATDD/collaboration-based techniques bridge to BDD. The principle "Testing is context-dependent" (CTFL Principle 6) argues that technique selection must match the system level.
- **OWASP WSTG** (std-4 §3 BUSL): Business Logic tests are "where agentic/E2E shines" precisely because they require scenario-level reasoning about workflow circumvention and multi-step misuse — they cannot be reduced to input/output probes.

**Synthesis verdict:** The convergence on scenario/example-based design at the E2E level is strong across four standards. This argues for Gherkin scenarios (or a Gherkin-compatible format) as the native specification format for the Jerry E2E skill's generated artifacts.

---

### Theme 5: Living Documentation — Tests as Durable, Executable Specifications

Three standards frame test artifacts not merely as pass/fail scripts but as durable, maintainable specifications that communicate intent and remain accurate over time.

- **Gherkin / BDD** (std-5 §3.3 and §4.2): "Declarative Gherkin scenarios describe what the system does, so the feature file itself is accurate product documentation that cannot rot silently — a failing scenario fails the build." This is the core "living documentation" claim of BDD.
- **ISO 29119-3** (std-2 §7, P6, P7, P8): The integrated artifact set (Parts 2+3) is designed so that every process step has a documented output; artifact naming aligns to the standard's vocabulary; Annex T maps to legacy IEEE 829 names. The intent is documentation that persists across project lifecycles.
- **ISTQB CTAL-TAE v2.0** (std-3 §7.7): "Verifying the test automation solution" (Chapter 7) requires the test framework itself to be tested — the framework is a durable artifact, not a disposable script pile. This meta-testing principle treats the automation as a long-lived asset.
- **OWASP WSTG** (std-4 §7.2 and §7.5): The per-test structured template and the checklist/reporting artifacts are designed for re-use across assessments; the versioned ID format (`WSTG-v42-AUTH-09`) enables stable cross-referencing as the guide evolves.

**Synthesis verdict:** Three of five standards treat test artifacts as long-lived, readable specifications rather than ephemeral scripts. This aligns with Jerry's "filesystem as infinite memory" identity. The skill should enforce scenario-file persistence with declarative style as a HARD rule.

---

## 3. Contradictions and Tensions

The following tensions are real disagreements between the standards. They are disclosed per P-022 rather than papered over.

---

### Tension 1: Process Formality vs Lightweight Collaboration

**The contradiction:** ISO 29119 (std-2) mandates a heavyweight documentation trail — Test Plan, Test Design Specification, Test Case Specification, Test Procedure Specification, Test Environment Requirements, Test Status Report, Test Completion Report, Test Incident Report (std-2 §7, P6). Each document template is prescribed in Part 3. In contrast, Gherkin/BDD (std-5) explicitly rejects document-centric approaches in favor of "conversations first" (Hellesøy, cited in std-5 §5.3). The Stop 29119 criticism (std-2 §5) — backed by the Association for Software Testing and the International Society for Software Testing — characterises ISO 29119 as producing "ponderous, wasteful bureaucracy and paperwork" at the expense of tester judgment.

**Where they agree:** Both standards endorse risk-based prioritisation. ISO 29119-6 TR (agile guidance) attempts to provide lightweight variants of the Part 3 templates; ISTQB's agile extension (CTFL-AT) bridges the gap from the ISTQB side.

**Resolution for Jerry:** Jerry should treat ISO 29119-3 templates as an a-la-carte menu, not a mandatory checklist. For any given E2E run, only the artifacts with genuine downstream value (Test Plan for complex projects; Test Incident Report for CI/CD failure records) should be generated. The Gherkin feature file is itself the test case specification when the declarative style is followed — it satisfies the Part 3 intent without a separate document.

---

### Tension 2: Certification Syllabus vs Technical Specification

**The contradiction:** ISTQB (std-3) is explicitly a certification scheme, not a technical specification. It carries no normative "MUST" language about implementation. The gTAA, while a valuable reference architecture, is described at an abstraction level that requires teams to supply concrete tooling. W3C WebDriver (std-1), by contrast, is a normative technical specification with algorithmic conformance requirements and a concrete endpoint vocabulary. ISO 29119 occupies a middle ground — normative process requirements ("the test strategy SHALL be risk-based") with no implementation prescriptions.

**Consequence for Jerry:** ISTQB concepts (gTAA, risk-based testing, seven principles) are directly reusable as vocabulary and architecture reference but cannot be cited as compliance anchors. W3C WebDriver can be cited as a conformance target. ISO 29119 can be cited as a process-compliance target in enterprise/regulated contexts.

**Resolution for Jerry:** Layer the three authorities differently — WebDriver for protocol conformance (HARD rules with spec section citations), ISO 29119 for process/documentation structure (MEDIUM rules with part/clause references), ISTQB for vocabulary and gTAA architecture reference (SOFT guidance and templates).

---

### Tension 3: Security-Only Scope (WSTG) vs Functional E2E

**The contradiction:** OWASP WSTG (std-4 §2) explicitly excludes "functional/acceptance/UI-behavioural correctness" from its scope. It tests whether features can be abused, not whether they work. The other four standards do not cover the security axis with comparable depth. A skill that treats WSTG as its primary test catalog will miss all functional correctness; a skill that ignores WSTG will miss the entire security surface.

**There is no genuine disagreement here** — the standards are addressing different testing concerns — but the tension for a unified E2E skill is real: how to orchestrate security and functional tests in a single workflow without conflating them.

**Resolution for Jerry:** Model security scenarios and functional scenarios as distinct but coexisting test types within the same Gherkin feature hierarchy. WSTG test IDs become `@wstg:WSTG-v42-<CAT>-<NN>` tags on security scenarios; ISTQB technique names tag functional scenarios. A single pipeline gate can run both suites and report their results in coordinated but separate sections.

---

### Tension 4: Stable Standards vs Rapidly Evolving Technology

**The contradiction:** ISO 29119 Parts 1-4 (2021-2022 editions, no announced revision) and OWASP WSTG v4.2 (stable since 2020-12-03) were written before the dominance of modern API-first, SPA, WebSocket, and agentic architectures. WebDriver BiDi (std-1 §6) is still a Working Draft; Gherkin does not have a version number at all. ISTQB is the most current (2024-2025 refresh cycle) but its gTAA was designed for traditional automation tools.

**Specific examples of gap:** WSTG has 3 APIT tests in stable v4.2 vs 20 INPV tests — severely under-weighted for API-first web services (std-4 §5). ISO 29119-2 treats the system-under-test as a largely monolithic unit with no distributed/event-driven guidance (std-2 §5). WebDriver Classic has no server-push events, requiring BiDi — which Safari does not yet support (std-1 §6).

**Resolution for Jerry:** Treat the standards as a base layer that must be extended. Do not wait for standards to catch up to agentic architectures — name the extensions explicitly in the skill as "Jerry supplements" and document what standard they extend and why.

---

### Tension 5: ISO 29119's Institutional Authority vs Its Community Rejection

**This is a genuine unresolved tension.** ISO 29119 is the only joint ISO/IEC/IEEE international standard for software testing (std-2 §4), giving it legal and procurement recognition in most jurisdictions. Simultaneously, the Stop 29119 campaign (2014, led by James Bach, Cem Kaner, and others) resulted in over 3,000 signatures and the formation of the International Society for Software Testing as a direct counter-movement (std-2 §5). The philosophical split between context-driven testing and standards-driven testing "remains unresolved as of 2026" (std-2 §5).

**Consequence for Jerry:** Adopting ISO 29119 uncritically risks framing the skill as document-bureaucracy-first and alienating context-driven practitioners. Ignoring it risks non-compliance in regulated/enterprise procurement contexts. There is no synthesis position that satisfies both camps.

**Resolution for Jerry (recommended posture):** Declare ISO 29119 as an *optional compliance layer* rather than a mandatory framework. The skill's default operation follows BDD/Gherkin + risk-based prioritisation (which both camps accept) and generates ISO 29119-compatible artifacts on demand. This resolves the procurement concern without mandating the documentation burden.

---

## 4. Coverage Gaps for Web-Service E2E Specifically

The following are what the five standards collectively leave unspecified. The Jerry skill will need to invent or borrow from outside the standards lane (likely from the innovators lane or from first principles).

---

### Gap 1: Agentic Loop Semantics

None of the five standards define how to test a system where the actor is an LLM-based agent rather than a human or deterministic script. ISO 29119-11 TR covers testing AI-under-test (the SUT contains AI) but not AI-as-tester (the agent is the test executor). Gherkin's agentic execution experiments (std-5 §3.4 and §6.5) are emergent research findings, not normative guidance. ISTQB's CT-GenAI v1.0 (std-3 §1.4) addresses LLM agents in testing but provides syllabus-level guidance, not executable specifications.

**What the skill needs to invent:** Semantics for "When an agentic actor..." — how to specify the expected trajectory of a multi-step agentic flow, not just the final state. How to assert over intermediate states that the agent visited. How to handle non-deterministic agent paths that still produce a correct end state.

---

### Gap 2: Self-Healing Selectors

W3C WebDriver (std-1 §5, P-WD-3) addresses flakiness through explicit/fluent waits but not through selector resilience. The standard error taxonomy names `stale element reference` but provides no remediation model. Flakiness-budget concepts — acceptable rates of non-deterministic failure in a CI pipeline — do not appear in any of the five standards.

**What the skill needs to invent:** A self-healing selector strategy (attribute-priority fallbacks, ARIA role anchors, semantic locators) and a quantified flakiness budget expressed as a CI gate threshold (e.g., test pass rate must be >= 98% across last 20 runs before a selector is classified as flaky).

---

### Gap 3: LLM-Driven Test Generation Quality Gates

The quality of LLM-generated test scenarios is addressed empirically in std-5 (95% relevance, 100% clarity, 94.2% completeness from arXiv 2508.20744) but none of the standards define normative thresholds for generated test quality. ISO 29119-4 defines coverage measures for human-authored tests; there is no equivalent for generated tests. OWASP WSTG provides a template structure but assumes human-authored procedure text.

**What the skill needs to invent:** A quality gate for LLM-generated scenarios that scores generated tests against dimensions analogous to the Jerry quality gate (completeness, internal consistency, traceability) before they are committed to the test suite.

---

### Gap 4: Distributed and Event-Driven E2E

ISO 29119-2 (std-2 §5) explicitly lacks guidance for microservices, event-driven, and distributed E2E. W3C WebDriver is page-centric; even BiDi's Network module covers browser-level network events, not inter-service event flows. OWASP WSTG is service-boundary-aware (API testing chapter) but does not address event choreography, saga patterns, or asynchronous eventual consistency as E2E test concerns.

**What the skill needs to invent:** Patterns for asserting over event flows (e.g., "Given a purchase event is published, then the inventory service eventually reflects the decrement within 5 seconds"). This is outside all five standards.

---

### Gap 5: Contract Testing and Consumer-Driven Test Boundary

The five standards treat E2E as a testing mode that exercises the full stack from the outside. None of them address contract testing (Pact, Spring Cloud Contract) as a complementary boundary that reduces E2E surface area. OWASP WSTG's APIT chapter covers security probing of APIs but not correctness contracts between producers and consumers.

**What the skill needs to invent:** A decision rule for when to write a WSTG-tagged E2E security scenario vs a consumer-driven contract test vs a unit test — the risk-based demarcation of the E2E boundary.

---

### Gap 6: Observability and Telemetry as Test Evidence

None of the five standards address how to use application telemetry (traces, metrics, logs) as assertions in E2E tests. ISO 29119-3's Test Incident Report assumes observable failure at the test-execution layer. OWASP WSTG's reporting chapter assumes human-readable findings. The Gherkin `Then` assertion is implicitly a black-box assertion on visible state.

**What the skill needs to invent:** Patterns for `Then` steps that assert on telemetry signals (e.g., "Then the P99 latency of the checkout endpoint is below 200ms") and a standard way to surface distributed trace IDs in test reports for correlation with test failures.

---

## 5. Recommended Standards Posture

The recommendation below distinguishes three categories: explicit alignment (the skill's rules cite these and are constrained by them), selective alignment (the skill borrows components but deviates where specified), and deliberate non-alignment (the skill explicitly chooses not to follow).

---

### Explicit Alignment

**W3C WebDriver Level 2 (std-1 §7) — align with P-WD-1 through P-WD-10.**

Rationale: WebDriver is the only normative technical specification with vendor conformance across all four major browser engines. It provides the durable protocol abstraction that insulates the skill from tooling churn. The skill's protocol-aware layer should cite WebDriver command vocabulary for every browser interaction primitive (std-1 §3). Specifically:

- P-WD-3 (waits not sleeps) should be a HARD rule in the skill.
- P-WD-5 (deterministic error taxonomy) should drive the skill's diagnostic output format.
- P-WD-9 (forward-compatible to BiDi) should be a MEDIUM rule with explicit capability-gate logic.

**OWASP WSTG v4.2 stable (std-4 §7.1-7.6) — align with the WSTG-v42-`<CAT>`-`<NN>` identifier scheme.**

Rationale: WSTG provides the only named, numbered, freely licensed taxonomy of ~109 security-relevant E2E tests. The skill should adopt the version-pinned ID format for all security scenarios (`WSTG-v42-<CAT>-<NN>`) and implement the passive-then-active test sequencing model (std-4 §7.3). The BUSL chapter (10 tests) maps directly to agentic scenario generation and should be a first-tier deliverable of the skill.

---

### Selective Alignment

**ISO/IEC/IEEE 29119 (std-2) — selectively align; borrow processes and vocabulary, not documentation burden.**

Align with:
- 29119-1 vocabulary (std-2 §3): Use the canonical terms (test basis, test condition, test coverage item, entry/exit criteria) in all skill-generated artifacts — this is free and enables cross-team legibility.
- 29119-2 dynamic test workflow (std-2 §7, P1-P5): Plan → Design → Implement → Execute → Report as the E2E run lifecycle structure. This is the process backbone.
- 29119-4 technique naming (std-2 §7, P9, P11): Each generated test case declares its technique from the Part 4 catalog — scenario testing, use-case testing, exploratory testing at E2E level.

Deviate from:
- 29119-3 full document set (std-2 §7, P6): The skill should NOT generate all eight prescribed document types by default. Treat as opt-in for regulated/enterprise contexts. The Gherkin feature file serves as the test case specification; a brief test plan markdown file serves as the project test plan. This deviation is justified by Tension 1 above.
- 29119-5 keyword-driven architecture (std-2 §7, P12-P13): The skill should NOT mandate a keyword-driven layer — Gherkin is already the human-readable specification format and the gTAA's Generation/Definition layers handle the same concern with more ecosystem support.

**ISTQB CTFL + CTAL-TAE (std-3) — selectively align; adopt gTAA, principles, and vocabulary; reject exam-apparatus framing.**

Align with:
- gTAA four-layer model (std-3 §7.1): Use as the reference architecture template for any E2E automation framework the skill provisions. The layer-to-tool mapping (Adaptation = Playwright; Execution = pytest; Definition = pytest-bdd; Generation = Jerry LLM agent; Management = Jerry worktracker) is directly actionable.
- CTFL seven testing principles (std-3 §7.2): Encode as skill invariants/prompt guardrails (e.g., "Never assert the skill's tests prove absence of defects" — Principle 1).
- Risk-based testing (std-3 §7.5): First-order step before test design; map to Jerry's C1-C4 criticality model.

Deviate from:
- CTFL Chapter 5 test-management documentation weight: ISTQB expects documentation of planning, estimation, and monitoring in a form that is certification-exam-relevant. Jerry's worktracker already handles this; the skill should not duplicate it.
- CTAL-TAE v2.0 as the canonical test automation guide: gTAA is useful; the exam chapters on frameworks and tools are too abstract for a skill that must make concrete technology choices.

**Gherkin / BDD (std-5) — selectively align; adopt declarative style and Discovery discipline; do not enforce Three Amigos as a blocking gate in automated contexts.**

Align with:
- Declarative scenario style (std-5 §7.2): HARD rule — `When` steps MUST describe behaviour, not UI mechanics. A linting rule flagging UI-verb tokens ("click", "type", "enter") in scenario steps is directly encodable.
- Gherkin 6 `Rule` keyword (std-5 §7.6): Use Feature → Rule → Scenario hierarchy to mirror the Example Mapping structure; enforce via linting.
- Background discipline (std-5 §7.5): Background MUST contain only `Given` steps applicable to every scenario in the Feature/Rule; warn if > 4 steps.
- Test-first alignment (std-5 §7.8): Scenarios MUST be written before implementation is present (H-20 alignment).

Deviate from:
- Three Amigos as a blocking prerequisite: the full Discovery workshop is valuable for human teams but is not always applicable when Jerry is auto-generating scenarios from requirements. The skill should treat Discovery as a SHOULD (include a reference to the generating artifact in the Feature description) rather than a HARD gate.
- Gherkin as the only permitted format: the skill may need to express API-level tests in a way that Gherkin does not serve well (e.g., OpenAPI-based contract assertions). Gherkin should be the preferred format for user-journey tests; non-Gherkin formats are permitted for infrastructure-layer tests.

---

## 6. Proposed Top-5 Distilled Principles

These are the five principles the new /e2e-testing skill should operationalize, each traceable to one or more of the five input files. These form the "standards half" of the final 10 skill principles; the innovators lane synthesizer produces the other 5.

---

### SP-1: Risk-First Test Ordering

**Principle:** Before any test design step, the skill MUST classify the scenario's risk (likelihood × impact) using a documented scale and use that classification to drive test ordering and CI gate placement.

**Rationale:** This is the highest-confidence theme across the standards lane — independently mandated by ISO 29119-2 (std-2 §7 P3), ISTQB CTFL Ch. 5 (std-3 §7.5), and structurally encoded in OWASP WSTG's threat-driven 12-category taxonomy (std-4 §2). It also aligns with Jerry's own C1-C4 criticality model in `quality-enforcement.md`.

**Traceability:** std-2 §7 P3 ("Design-Test-Strategy is risk-based"); std-3 §7.5 ("Risk-based testing → Jerry criticality mapping"); std-4 §1 (threat-driven taxonomy as the structural expression of risk ordering).

**Testable assertion:** Every test case artifact generated by the skill MUST include a `risk_level` field (HIGH/MEDIUM/LOW) and a `criticality` field (C1-C4) populated before test-step authoring begins.

---

### SP-2: Declarative Scenario Specification with Traceable Basis

**Principle:** All E2E test scenarios MUST be expressed in declarative Gherkin (or equivalent declarative format) and MUST include a `@basis:` tag or equivalent metadata linking the scenario to its test basis (user story ID, WSTG test ID, risk item, or requirement reference).

**Rationale:** Declarative style (std-5 §7.2) prevents UI-coupling rot; traceable basis (std-2 §7 P7; std-4 §7.2 per-test template; std-3 §3.1) is independently required by three standards and is the mechanism that keeps the test suite honest as the system evolves.

**Traceability:** std-5 §7.2 (declarative over imperative); std-2 §7 P7 (traceability to test basis); std-4 §7.2 (per-test structured template with Summary/Objectives/References); std-3 §3.1 (CTFL test analysis traces conditions to basis).

**Testable assertion:** A linting rule rejects any `Scenario` whose `When` steps contain UI-verb tokens ("click", "type", "enter", "navigate to", "fill in") and any Scenario lacking a `@basis:` tag with a non-empty reference value.

---

### SP-3: gTAA-Conformant Automation Layer

**Principle:** Any automation framework provisioned or referenced by the skill MUST map its components to the four gTAA layers (Generation, Definition, Execution, Adaptation) with at least Execution and Adaptation present. The Adaptation layer MUST be the exclusive integration point with the browser/API driver; all other layers MUST NOT import directly from driver APIs.

**Rationale:** The gTAA (std-3 §7.1) and WebDriver protocol-layer isolation (std-1 §7 P-WD-1) converge on the same architectural constraint — separation of the specification/execution layers from the driver interface. Hexagonal BDD (std-5 §7.4) provides the BDD-specific expression of the same principle.

**Traceability:** std-3 §7.1 (gTAA four-layer model and layer-to-tool mapping); std-1 §7 P-WD-1 (protocol layer isolation); std-5 §7.4 (hexagonal BDD — step definitions import only from domain/port layers).

**Testable assertion:** The skill's framework template generates separate source modules for each gTAA layer; an import graph check (analogous to Jerry's H-07/H-08 architecture rules) rejects direct driver-API imports from Definition or Generation layer files.

---

### SP-4: Security Scenario Coverage via WSTG Taxonomy

**Principle:** For any web service E2E test suite, the skill MUST generate or recommend at minimum one security scenario from each of the WSTG categories ATHN, ATHZ, SESS, INPV, BUSL, and APIT, using version-pinned WSTG test IDs (`WSTG-v42-<CAT>-<NN>`) as the canonical identifier in scenario tags and test reports.

**Rationale:** WSTG is the only standard among the five that provides a complete, named, freely licensed security-testing taxonomy specific to web applications and services (std-4 §4). Without an explicit coverage requirement, security testing is the area most likely to be omitted from E2E suites that focus only on functional correctness. The BUSL category (std-4 §3) is uniquely suited to agentic execution and must be first-tier, not optional.

**Traceability:** std-4 §1 (12-category taxonomy with test counts); std-4 §3 (BUSL and ATHN as highest-applicability categories); std-4 §7.1 (version-pinned ID format `WSTG-v42-<CAT>-<NN>`).

**Testable assertion:** The skill's completeness check verifies that the generated test suite contains at least one scenario tagged with each of the six mandatory WSTG category codes; a CI gate reports per-category WSTG coverage as a distinct metric.

---

### SP-5: Forward-Compatible Protocol with Explicit Error Taxonomy

**Principle:** The skill MUST specify browser interaction operations in W3C WebDriver command vocabulary (std-1 §3 endpoint families) and MUST map all test failures to the WebDriver error taxonomy (`no such element`, `stale element reference`, `element click intercepted`, `timeout`, `invalid session id`) in its diagnostic output. Where a feature requires server-push events (network interception, console log monitoring, exception capture), the skill MUST gate that feature on BiDi capability negotiation (`webSocketUrl`) rather than requiring a Chrome-only CDP fallback.

**Rationale:** W3C WebDriver (std-1) provides the only cross-browser-conformant protocol vocabulary. The error taxonomy (P-WD-5) enables structured, remediable diagnostics rather than opaque failure messages. The BiDi forward-compatibility rule (P-WD-9) is the mechanism that keeps the skill viable as browser vendors accelerate BiDi adoption and deprecate CDP (Firefox CDP deprecation started v129 per std-1 §6).

**Traceability:** std-1 §7 P-WD-1 (protocol layer isolation); std-1 §7 P-WD-5 (deterministic error taxonomy); std-1 §7 P-WD-9 (forward-compatible to BiDi); std-1 §6 (vendor conformance and BiDi adoption trajectory).

**Testable assertion:** The skill's diagnostic output for any failed test MUST include a `webdriver_error_class` field populated from the canonical error code list; any implementation that uses `goog:chromeOptions`-exclusive features (CDP endpoints, Chrome DevTools Protocol URLs) without a non-Chromium fallback is flagged as a portability violation.

---

## 7. Open Questions for Master Synthesis

The following questions were surfaced during this synthesis and require input from the innovators lane synthesis and/or the eng-team baseline to resolve. They are not answerable from the standards alone.

1. **Agentic loop semantics:** The standards provide no normative model for multi-step agentic test execution. The innovators lane (Browser-Use, Skyvern, GenIA-E2ETest) is the expected source of patterns for asserting over intermediate agent states, handling non-deterministic paths, and qualifying "success" for an agentic actor. Master synthesis should reconcile these with Gherkin's `When/Then` model from the standards lane.

2. **Self-healing selectors:** W3C WebDriver's error taxonomy names `stale element reference` but provides no remediation model. The innovators lane may provide selector-resilience patterns (e.g., ARIA-based locators, Playwright's semantic locators, AI-driven element recovery). Master synthesis should determine whether this becomes SP-5's forward-compatibility clause or a separate principle.

3. **Flakiness budget:** None of the five standards define an acceptable non-determinism rate for E2E tests. The eng-team baseline presumably surfaces this as a current operational gap. Master synthesis should define a concrete threshold (e.g., a test with >= 2% failure rate on green code is classified as flaky and must be quarantined) and source it from practitioner evidence in the innovators lane.

4. **LLM-generated test quality gate:** The standards provide no mechanism for scoring the quality of generated test scenarios. The GenIA-E2ETest metrics (execution recall, manual modification rate) from the innovators lane are the closest existing answer. Master synthesis should determine whether these metrics become a skill-level quality gate or an advisory threshold.

5. **Contract testing boundary:** No standard among the five addresses the demarcation between E2E and contract testing. The innovators lane may have patterns for when to prefer a Pact-style consumer-driven contract over a full-stack E2E scenario. Master synthesis should produce a decision rule that the skill can apply at test-design time.

6. **Distributed and event-driven E2E:** ISO 29119 and OWASP WSTG do not address testing across asynchronous service boundaries. The innovators lane or eng-team baseline may surface patterns (e.g., test containers for event brokers, Testcontainers-based service mesh simulation). Master synthesis should determine whether this is in scope for the initial skill or deferred.

7. **ISO 29119 compliance opt-in depth:** The recommended posture above treats ISO 29119-3 documentation templates as opt-in. The master synthesis should determine whether any enterprise context in Jerry's current project portfolio (PROJ-007, PROJ-014) requires a specific 29119 compliance level that would make this opt-in mandatory in practice.

8. **Gherkin vs YAML vs OpenAPI for API-level tests:** The standards lane endorses Gherkin for user-journey scenarios but leaves unspecified what format API-level E2E assertions should use (WSTG APIT tests are narrative prose; ISO 29119 is format-agnostic). The innovators lane likely produces a concrete tooling answer. Master synthesis should resolve the format question for API-only E2E test cases.

---

## Source Files

| File | Type | Key Contribution | Principles Contributed |
|------|------|------------------|------------------------|
| `research/deep-standards/std-1-w3c-webdriver.md` | Technical specification deep-dive | W3C WebDriver Level 2 protocol vocabulary, BiDi evolution, cross-browser conformance model, 10 P-WD-N testable principles, error taxonomy | SP-3 (protocol isolation), SP-5 (error taxonomy + BiDi forward-compat) |
| `research/deep-standards/std-2-iso-29119.md` | Process standard deep-dive | ISO/IEC/IEEE 29119 eight-part series scope, three-layer process model, artifact catalog, test technique categorisation, 16 P1-P16 testable principles, Stop-29119 controversy | SP-1 (risk-first ordering), SP-2 (traceability to test basis), Tension 1 (process formality) |
| `research/deep-standards/std-3-istqb.md` | Certification scheme deep-dive | CTFL v4.0 seven principles, gTAA four-layer reference architecture, risk-based testing, CI/CD integration, CT-GenAI v1.0 (LLM-in-testing), test automation verification | SP-1 (risk mapping to C1-C4), SP-3 (gTAA architecture), SP-2 (partial — vocabulary traceability) |
| `research/deep-standards/std-4-owasp-wstg.md` | Security testing guide deep-dive | WSTG v4.2 12-category taxonomy (~109 tests), versioned test ID format, passive/active test sequencing, BUSL as agentic-test category, APIT chapter for API-first services | SP-4 (security coverage via WSTG taxonomy) |
| `research/deep-standards/std-5-cucumber-gherkin.md` | BDD DSL deep-dive | Gherkin grammar (Feature/Rule/Scenario/Given-When-Then), declarative style mandate, Example Mapping/Three Amigos Discovery, hexagonal BDD, agentic Gherkin execution research (92-95% LLM quality), 8 testable principles | SP-2 (declarative scenario format), SP-3 (hexagonal BDD / gTAA alignment) |
