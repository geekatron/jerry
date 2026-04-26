---
title: "Deep Research: ISTQB Foundation + CTAL-TAE"
slug: std-3-istqb
candidate: "Candidate 3 (ISTQB)"
project: PROJ-017-e2e-testing-skill
orchestration: e2e-skill-build-20260420-001
phase: 1b-deep-research
agent: ps-researcher-std-3
access_date: 2026-04-21
landscape_card: ../landscape/standards-candidates.md#candidate-3
---

# Deep Research: ISTQB Foundation + CTAL-TAE (Test Automation Engineer)

> Phase 1b deep-dive on the International Software Testing Qualifications Board (ISTQB) body of knowledge -- Certified Tester Foundation Level (CTFL) v4.0, CTAL-TAE v2.0, and adjacent AI syllabi -- as a candidate for informing the Jerry E2E testing skill. Honest P-022 assessment: ISTQB is a *certification scheme with syllabi*, not an international standard in the ISO/IEEE sense; that distinction is material and addressed in Section 2.

## Navigation

| Section | Purpose |
|---------|---------|
| [Methodology Note](#methodology-note) | Queries, fetches, evidence trail |
| [1. What It Specifies](#1-what-it-specifies) | CTFL v4.0, CTAL-TAE v2.0, CT-TAS, CT-AI, CT-GenAI, glossary |
| [2. Scope and Boundary](#2-scope-and-boundary) | Certification vs standard distinction |
| [3. Applicability to Jerry E2E Skill](#3-applicability-to-jerry-e2e-skill) | Operationalizable concepts for E2E |
| [4. Strengths / Unique Contributions](#4-strengths--unique-contributions) | Vocabulary, adoption, extensions |
| [5. Weaknesses / Gaps / Criticisms](#5-weaknesses--gaps--criticisms) | Cert-focus, not a spec, process bias |
| [6. Current State (2024-2026)](#6-current-state-2024-2026) | Version matrix and release timeline |
| [7. Key Implementation Patterns](#7-key-implementation-patterns) | Testable principles for a skill |
| [Sources Retrieved](#sources-retrieved) | All live URLs with access date |

---

## Methodology Note

**Access date:** 2026-04-21 (all URLs retrieved this session). **Tool policy:** live WebSearch + WebFetch only; no training-data-only findings; P-022 honesty applied throughout.

### Queries executed (8 total)

| # | Query | Purpose |
|---|-------|---------|
| Q1 | `ISTQB Foundation Level syllabus 2024 2025 v4` | Locate current CTFL syllabus version |
| Q2 | `ISTQB CTAL-TAE test automation engineer syllabus 2024` | Find latest CTAL-TAE release |
| Q3 | `ISTQB AI testing syllabus 2025 CT-AI` | Coverage of AI-testing extension |
| Q4 | `ISTQB glossary current version 2024` | Glossary versioning & scope |
| Q5 | `ISTQB vs ISO 29119 relationship comparison` | Disambiguate cert vs standard |
| Q6 | `ISTQB test automation architecture layers generic TAA` | gTAA technical content |
| Q7 | `ISTQB Agile testing extension CTFL-AT syllabus 2024` | Agile extension scope |
| Q8 | `ISTQB CTFL v4 learning objectives chapters test design techniques` | CTFL chapter breakdown |
| Q9 | `ISTQB CT-GenAI Testing with Generative AI 2025 release` | Newest specialist syllabus |
| Q10 | `ISTQB criticisms weaknesses certification vs practice` | Balanced assessment (Section 5) |

### Primary-source WebFetch reads (4 total)

| # | URL | Pull |
|---|-----|------|
| F1 | `https://istqb.org/certifications/certified-tester-foundation-level-ctfl-v4-0/` | CTFL v4.0 chapter structure, business outcomes, exam format |
| F2 | `https://istqb.org/certifications/certified-tester-advanced-level-test-automation-engineering-ctal-tae-v2-0/` | CTAL-TAE v2.0 eight-chapter structure and exam details |
| F3 | `https://istqb.org/certifications/certified-tester-ai-testing-ct-ai/` | CT-AI v2.0 topic coverage for ML, LLM, generative AI testing |
| F4 | `https://istqb.org/istqb-has-released-two-new-syllabi-for-test-automation/` | Official CT-TAE / CT-TAS split announcement (Jun 12 2024), sunset schedule |
| F5 | `https://istqb-glossary.page/generic-test-automation-architecture/` | gTAA glossary definition (supplementary) |

### Evidence hygiene

- Every Section 1-7 claim is anchored to a specific search result or fetch listed in [Sources Retrieved](#sources-retrieved).
- Where a primary source did not fully cover a detail (e.g., gTAA layer functions), the gap is disclosed explicitly and the lower-tier source (Sogeti Labs, Adesso, glossary page) is named.
- Section 5 (weaknesses) uses community/practitioner sources with the critical lens preserved; no attempt to hide dissent.

---

## 1. What It Specifies

### 1.1 ISTQB as a scheme (not a single document)

ISTQB is a *certification scheme* operated by the International Software Testing Qualifications Board. It publishes a family of **syllabi** (training and exam specifications) plus a **glossary**, all freely downloadable. The "ISTQB standard" in practice means the combined body of knowledge expressed across the Foundation Level, Advanced Level (CTAL), Specialist, and Expert streams [S1, S2].

### 1.2 Certified Tester Foundation Level (CTFL) v4.0 / v4.0.1

- **Release:** English syllabus, exams, and accredited training published 9 May 2024; v4.0.1 errata 15 Sep 2024. Non-English languages followed 9 Nov 2024 [S1].
- **Accredited training hours:** minimum 1135 minutes (~18h 55m) [S1, S2].
- **64 Learning Objectives** across **14 Business Outcomes** [S2].
- **Six chapters** (per ISTQB's own overview page [F1, S1]):
  1. Fundamentals of Testing -- objectives, principles, activities, testware, roles, skills
  2. Testing Throughout the SDLC -- test levels, test types, maintenance testing; explicitly inclusive of Waterfall, Agile, DevOps, Continuous Delivery [S1]
  3. Static Testing -- reviews, static analysis, feedback loops
  4. Test Analysis & Design -- black-box (equivalence partitioning, boundary value analysis, decision tables, state transition), white-box, experience-based, and collaboration-based techniques (e.g., ATDD) [S2]
  5. Managing the Test Activities -- planning, risk management, monitoring/control, completion, configuration, defect management
  6. Test Tools -- tool support, benefits, automation risks
- **Exam:** 40 MCQs, 60 min (75 min non-native), pass mark 26/40 (65%) [F1].
- **Chapters 4 + 5 combined ~50% of exam weight**, signalling their centrality [S2].

### 1.3 CTAL-TAE v2.0 (Test Automation Engineering)

- **Release:** approved by ISTQB General Assembly in Budapest 3 May 2024; publicly released 12 June 2024 [F4, S2].
- **Structural split in 2024:** the 2016 single syllabus was split into two independent certifications -- **CT-TAE v2.0 (engineering / architecture / implementation)** and **CT-TAS v1.0 (strategy / managerial)**. Neither is a prerequisite for the other; both require CTFL [F4]. Old CT-TAE-2016 sunsets 12 Jun 2025 (English) / 12 Dec 2025 (other languages) [F4].
- **Eight chapters of CTAL-TAE v2.0** [F2]:
  1. Introduction and Objectives for Test Automation
  2. Preparing for Test Automation
  3. Test Automation Architecture (gTAA)
  4. Implementing Test Automation
  5. Implementing and Deployment Strategies (CI/CD integration)
  6. Test Automation Reporting and Metrics
  7. Verifying the Test Automation Solution
  8. Continuous Improvement
- **Exam:** 40 questions, 90 minutes, 43/66 to pass [F2]. Prerequisite: CTFL [S2].
- **Generic Test Automation Architecture (gTAA)** is the technical centrepiece (see Section 7). Four horizontal layers: **Test Generation, Test Definition, Test Execution, Test Adaptation**; three cross-cutting management layers: **Test Management, Project Management, Configuration Management** [S6, F5].

### 1.4 Adjacent syllabi relevant to E2E

| Syllabus | Version | Key date | What it adds for E2E context |
|----------|---------|----------|-----------------------------|
| CTFL-AT (Agile Tester extension) | v1.x (sample exam v1.3 Nov 2024) | Ongoing | Agile team role, sprint-aligned testing, ATDD [S7] |
| CT-AI (AI Testing) | v2.0 | Updated 2024-2025 | Testing ML/LLM systems, non-determinism, data-centric testing, neural networks [F3] |
| CT-GenAI (Testing *with* Generative AI) | v1.0 | Released 29 Jul 2025 (GA approval 25 Jul 2025) | Using LLMs *in the testing process*: prompt engineering, hallucination risk, LLMOps, RAG, LLM agents in testing [S9] |

### 1.5 ISTQB Glossary

- **Current app version v4.5** (announced Nov 2024); prior v4.3 introduced quiz/gamification [S4].
- 500+ definitions, multilingual, online at `glossary.istqb.org`; also available as mobile app [S4].
- Acts as the canonical vocabulary binding all syllabi together -- a key structural feature for any framework reuse (see Section 7).

---

## 2. Scope and Boundary

### 2.1 Certification vs standard -- the material distinction

ISTQB is **not an ISO/IEEE international standard**. It is a body-of-knowledge-plus-certification programme. The relevant international standard for *testing process and documentation* is **ISO/IEC/IEEE 29119** (parts 1-5, first three parts released 2013, part 4 in 2015) [S5]. Per a Springer-published academic mapping study [S5]:

> "The scope of ISTQB is fundamentally limited to Test Management and Dynamic Test. The test process of ISTQB CTFL is largely covered by ISO/IEC/IEEE 29119-2. However, the clauses of the Organizational Test Process of ISO/IEC 29119-2 are hardly dealt with within ISTQB CTFL."

This means: ISTQB covers **how an individual tester / team performs testing**; ISO 29119 additionally covers **how an organisation institutes testing policy and the organisational test process**. For Jerry, ISTQB is an *educational/vocabulary* input; ISO 29119 is a *structural/process* input. They are complementary, not redundant [S5].

### 2.2 What ISTQB covers

- Test fundamentals and principles
- SDLC integration and test levels (component, integration, system, acceptance)
- Test analysis and design techniques (black-box, white-box, experience-based)
- Test management (planning, risk-based testing, estimation, monitoring)
- Static testing (reviews, static analysis)
- Test tools and automation (gTAA via CTAL-TAE)
- Agile, AI-under-test, and AI-in-testing extensions

### 2.3 What ISTQB does **not** cover (explicit gaps)

- **Organisational test policy / governance** (ISO 29119-1 territory) [S5]
- **Prescriptive document templates** (ISO 29119-3 territory)
- **Tool-specific implementation** (Playwright, Selenium, Cypress, etc. are referenced generically; no binding API specs)
- **Contract/API testing tooling details** (topic mentioned but not tool-prescriptive)
- **Ethical/regulatory compliance for safety-critical testing** (deferred to domain standards such as DO-178C, ISO 26262)

### 2.4 Methodology vs certification parts

| Component | Nature | Reusable as methodology? |
|-----------|--------|-------------------------|
| Syllabi LOs (learning objectives) | Knowledge inventory | **Yes** -- vocabulary + structure |
| Glossary | Controlled terminology | **Yes** -- high value for Jerry |
| gTAA model | Architecture reference | **Yes** -- directly operationalizable |
| Test design technique catalogue | Method library | **Yes** -- partial |
| Exam / business outcomes | Certification artefact | **No** -- not applicable to a skill |
| Accreditation guidelines | Training-provider rules | **No** -- not applicable |

---

## 3. Applicability to Jerry E2E Skill

### 3.1 Directly operationalizable concepts

| ISTQB concept | Source | Operationalizable in Jerry E2E skill? |
|---------------|--------|--------------------------------------|
| Seven testing principles (e.g., "testing shows presence of defects") | CTFL Ch. 1 [S1] | **Yes** -- can appear as skill invariants or rule preamble |
| Test levels: component → integration → system → acceptance | CTFL Ch. 2 [F1] | **Yes** -- E2E maps to *system* and *acceptance* levels; this framing is the canonical answer to "where does E2E sit" |
| Test types: functional, non-functional, white-box, change-related | CTFL Ch. 2 [F1] | **Yes** -- taxonomy to structure skill templates |
| Test design techniques (EP, BVA, decision tables, state transition) | CTFL Ch. 4 [S2] | **Yes** -- can back a "generate test cases from requirements" agent step |
| Risk-based testing | CTFL Ch. 5 [F1] | **Yes** -- strong match to Jerry's criticality (C1-C4) model |
| Defect lifecycle and reporting | CTFL Ch. 5 [F1] | **Yes** -- feeds worktracker integration |
| Generic Test Automation Architecture (gTAA): 4 horizontal + 3 management layers | CTAL-TAE Ch. 3 [S6, F2] | **Yes** -- the strongest single deliverable: a reference model for the skill's architecture prompts |
| Test automation in CI/CD | CTAL-TAE Ch. 5 [F2] | **Yes** -- direct alignment with modern E2E execution patterns |
| Test automation verification (meta-testing the framework itself) | CTAL-TAE Ch. 7 [F2] | **Yes** -- novel contribution; many E2E frameworks lack this |
| ATDD / collaboration-based techniques | CTFL Ch. 4 [S2] | **Yes** -- aligns with BDD/Gherkin patterns |

### 3.2 Partially applicable concepts

- **Static testing (reviews)** -- relevant to skill artefact review (e.g., reviewing test plans); less relevant to E2E execution loop.
- **Test management processes** -- relevant at orchestration layer, not inside the E2E skill itself.
- **AI-testing topics (CT-AI)** -- relevant if Jerry E2E skill is asked to test AI features of a SUT [F3]; otherwise optional.
- **Using GenAI in testing (CT-GenAI)** -- directly relevant to Jerry's own design: prompt engineering, hallucination risk, LLM-as-judge patterns [S9]. Meta-aligned with how Jerry uses LLMs.

### 3.3 Not applicable

- Certification exam formats, accreditation rules, training-hour minima.
- Country-specific Member Board processes.

### 3.4 Summary

ISTQB contributes **four reusable artefacts** to a Jerry E2E skill: (a) the glossary as vocabulary SSOT, (b) test-level taxonomy for positioning E2E, (c) gTAA as architecture reference for any automation the skill produces, and (d) risk-based testing as the bridge to Jerry's criticality model.

---

## 4. Strengths / Unique Contributions

| Strength | Evidence | Why it matters for Jerry |
|----------|----------|-------------------------|
| **Widest practitioner vocabulary in industry** | 500+ glossary terms, multilingual, 60+ Member Boards [S4] | Common vocabulary reduces ambiguity in skill prompts and rule files |
| **Free, downloadable, stable PDFs** | All syllabi + glossary freely on istqb.org [S1, S2, F1-F4] | Easy to cite; no licensing blocker for skill authors |
| **Lifecycle-agnostic framing in v4.0** | CTFL v4.0 explicitly aligned to Agile/DevOps/CD [S1] | Matches modern E2E contexts (Jerry's target) |
| **gTAA is a concrete reference architecture** | 4 horizontal + 3 management layers, glossary-anchored [S6, F5] | Unique among candidates -- ISO 29119 has no equivalent architecture model |
| **Active 2024-2025 refresh cycle** | CTFL v4.0.1 (Sep 2024), CTAL-TAE v2.0 (Jun 2024), CT-GenAI v1.0 (Jul 2025) [F4, S9] | Current thinking on AI, CI/CD, and modern SDLC is baked in |
| **Extensions for AI testing and testing with AI** | CT-AI v2.0; CT-GenAI v1.0 [F3, S9] | Directly relevant to Jerry's LLM-first architecture |
| **Explicit split between engineering and strategy** | CT-TAE v2.0 + CT-TAS v1.0 [F4] | Mirrors Jerry's agent-role separation (workers vs orchestrators) |
| **ATDD and collaboration techniques named** | CTFL Ch. 4 [S2] | Clear bridge to BDD/Gherkin in the E2E skill |
| **Test automation verification (meta-testing)** | CTAL-TAE Ch. 7 [F2] | A rare explicit call-out; supports Jerry's self-test culture |

---

## 5. Weaknesses / Gaps / Criticisms

P-022 honesty: ISTQB attracts sustained, substantive criticism. The following is a steelmanned (S-003) summary of dissenting views from practitioner sources [S10].

| Weakness | Evidence | Impact on Jerry use |
|----------|----------|--------------------|
| **Certification-focused, not a technical spec** | ISTQB publishes syllabi and exams; no machine-readable schemas, no normative "MUST" language | Must be *adapted*, not *adopted*; Jerry can take vocabulary and gTAA without taking the exam apparatus |
| **Memorisation vs applied skill** | Critics: "bar is primarily memorization and recall, not applied skill...confidence often falls apart when asked to write a systematic test design from scratch" [S10] | Reminds Jerry to turn concepts into *executable* skill steps, not rote definitions |
| **Weak correlation with job performance** | Practitioner LinkedIn/blog consensus: "never had a client make a hiring decision based on ISTQB certs" [S10] | Don't use ISTQB as a proxy for quality; use it as a vocabulary source |
| **Process bias (waterfall heritage)** | Academic critique notes CTFL is still strong on document-centric test management; less prescriptive on CI/CD beyond naming it [S5] | Jerry's CI/CD-heavy target context needs supplementation from CTAL-TAE + external patterns |
| **No organisational process coverage** | Explicit gap vs ISO 29119-1/2 Organizational Test Process [S5] | If Jerry needs to describe how an organisation *adopts* E2E testing, ISTQB alone is insufficient |
| **Tool-agnostic to a fault** | gTAA is abstract; no bindings to Playwright/Selenium/Cypress etc. [F2, F5] | Skill must supply its own concrete tooling layer |
| **Volume of prose per signal** | CTFL ~18h training for 64 LOs; not all LOs equally useful for an automated-E2E context [S1, S2] | Curate ruthlessly; don't import the full syllabus |
| **Glossary page minimally documented online** | The primary glossary URL returned only a title in WebFetch [F gap for `glossary.istqb.org/en_US/home`] | Use the app and PDF release notes as the authoritative source rather than the root page [S4] |
| **gTAA glossary entry is sparse** | The glossary page gives the definition but not layer details [F5] | Must cite CTAL-TAE syllabus itself (or third-party derivatives like Sogeti Labs, Adesso [S6]) for full layer semantics |
| **Pay-walled local training ecosystems** | Accreditation and exams are monetised via Member Boards | Not a Jerry blocker (syllabi are free), but contributes to ISTQB's "feels heavy" reputation |

---

## 6. Current State (2024-2026)

### Version matrix as of access date 2026-04-21

| Artefact | Version | Release date | Source |
|----------|---------|--------------|--------|
| CTFL (Foundation Level) | v4.0 / v4.0.1 errata | 9 May 2024 (v4.0) / 15 Sep 2024 (v4.0.1) | [S1, S2] |
| CTAL-TAE (Test Automation Engineering) | v2.0 | 12 Jun 2024 (GA approval 3 May 2024) | [F4, S2] |
| CT-TAS (Test Automation Strategy) | v1.0 | 12 Jun 2024 | [F4] |
| CT-AI (AI Testing) | v2.0 (updated) | 2024-2025 | [F3] |
| CT-GenAI (Testing with Generative AI) | v1.0 | 29 Jul 2025 (GA approval 25 Jul 2025) | [S9] |
| CTFL-AT (Agile Tester extension) | v1.3 sample exam | Nov 2024 update | [S7] |
| Glossary (app) | v4.5 | Nov 2024 | [S4] |
| CT-TAE 2016 (legacy) | Sunset | 12 Jun 2025 English / 12 Dec 2025 other langs | [F4] |

### 6.1 Release momentum

ISTQB is in its most active release cycle in a decade. The Foundation Level was restructured (v4.0 is a "total and deep redesign" [S1]); the Test Automation certification was split into engineering + strategy; and two AI-adjacent certifications shipped within 12 months. For Jerry's purposes this means **cite the 2024-2025 documents, not the 2016 CTAL-TAE** when sourcing gTAA content.

### 6.2 Posture toward AI

ISTQB has staked out a clear dual position: **testing AI** (CT-AI v2.0 -- ML, neural networks, LLMs, generative AI systems [F3]) and **testing with AI** (CT-GenAI v1.0 -- prompt engineering, hallucinations, LLMOps, RAG, LLM agents [S9]). Both are directly relevant to Jerry. The CT-GenAI positioning explicitly includes LLM agents in the testing process -- aligned with Jerry's agent-based orchestration.

---

## 7. Key Implementation Patterns / Testable Principles

### 7.1 Generic Test Automation Architecture (gTAA) -- the single most reusable artefact

Per ISTQB CTAL-TAE Ch. 3 and glossary [S6, F5]:

```
+--------------------------+  +------------------+
| Test Management          |  | Project Mgmt     |
+--------------------------+  +------------------+
| Configuration Management                         |
+--------------------------------------------------+
| Test Generation Layer                            |  <- design/capture/derive tests
+--------------------------------------------------+
| Test Definition Layer                            |  <- core framework structures
+--------------------------------------------------+
| Test Execution Layer                             |  <- runs tests, controls TAS
+--------------------------------------------------+
| Test Adaptation Layer                            |  <- interfaces with SUT, harness, env
+--------------------------------------------------+
```

Per the Sogeti Labs summary citing the syllabus [S6]:

- **Test Generation** -- tool support for manually designing test cases, capturing/deriving data, model-based generation.
- **Test Definition** -- part of the core test automation framework.
- **Test Execution** -- "core of a TAS"; actual execution; controls TAS interactions.
- **Test Adaptation** -- test harness control, SUT interaction, monitoring, environment emulation.
- **Layers can be present or absent in any given TAS**; execution + adaptation are the minimum pair for automated execution [S6].

**Actionable for Jerry:** a skill can emit a template mapping each layer to a concrete tool (e.g., Adaptation = Playwright driver; Execution = pytest runner; Definition = pytest-bdd; Generation = LLM-driven spec generator; Management = Jerry worktracker).

### 7.2 Testable principles (CTFL v4.0 seven principles) [S1, F1]

1. Testing shows the presence of defects, not their absence
2. Exhaustive testing is impossible
3. Early testing saves time and money
4. Defects cluster together
5. Tests wear out (the pesticide paradox)
6. Testing is context-dependent
7. Absence-of-defects is a fallacy

Each can back a **skill invariant / prompt guardrail** (e.g., "Never assert the skill's tests prove absence of defects").

### 7.3 Test levels and E2E positioning [F1, S2]

Component → Integration → System → Acceptance. **End-to-end testing maps to *system* and *acceptance* levels**, usually with business-flow scenarios. This is the clean answer to "what is E2E" that avoids the tool-centric trap.

### 7.4 Test design techniques as generator patterns [S2]

- **Equivalence Partitioning** -- reduce input space by classes
- **Boundary Value Analysis** -- focus on edges of partitions
- **Decision Tables** -- combinatorial rule coverage
- **State Transition Testing** -- cover state machine edges
- **Use Case Testing / Scenario Testing** -- business-flow coverage (E2E-aligned)
- **ATDD** -- collaboration-based, BDD-adjacent

A Jerry skill can expose these as *test-generation strategies* when asked to produce cases from requirements.

### 7.5 Risk-based testing → Jerry criticality mapping [F1]

ISTQB risk-based testing prioritises by **likelihood × impact**. This is isomorphic to Jerry's C1-C4 criticality levels in `.context/rules/quality-enforcement.md`. A skill can surface risk-classification as a first-order step before test design.

### 7.6 CI/CD integration [F2, S2]

CTAL-TAE v2.0 Ch. 5 "Implementing and Deployment Strategies" addresses pipeline integration explicitly. E2E patterns include: gate at system-level before release; fast feedback via adaptation-layer mocks; environment-parity via configuration management layer.

### 7.7 Verifying the test automation solution [F2]

CTAL-TAE v2.0 Ch. 7 is notable: the test framework itself must be tested. For Jerry this translates to: the E2E skill must include self-test patterns (smoke tests on scaffold outputs, linting, dry-run validation).

### 7.8 Glossary as SSOT [S4]

The ISTQB glossary's structure (term + definition + source syllabus + synonyms) is a reusable pattern for any Jerry domain vocabulary file.

---

## Sources Retrieved

All URLs retrieved live on 2026-04-21. Five+ live citations required; nine primary/secondary sources listed plus four WebFetch reads.

### Primary ISTQB sources (official)

- **[S1]** ISTQB. *ISTQB Releases Certified Tester Foundation Level v4.0 (CTFL)*. https://istqb.org/istqb-releases-certified-tester-foundation-level-v4-0-ctfl/ (retrieved 2026-04-21)
- **[S2]** ISTQB. *Certified Tester Foundation Level (CTFL) v4.0 Overview*. https://istqb.org/certifications/certified-tester-foundation-level-ctfl-v4-0/ (retrieved 2026-04-21) -- **[F1]**
- **[S3]** ISTQB. *Certified Tester Advanced Level Test Automation Engineering (CTAL-TAE) v2.0*. https://istqb.org/certifications/certified-tester-advanced-level-test-automation-engineering-ctal-tae-v2-0/ (retrieved 2026-04-21) -- **[F2]**
- **[F3]** ISTQB. *Certified Tester AI Testing (CT-AI)*. https://istqb.org/certifications/certified-tester-ai-testing-ct-ai/ (retrieved 2026-04-21)
- **[F4]** ISTQB. *ISTQB has released two new syllabi for test automation* (CT-TAE / CT-TAS split, 12 Jun 2024). https://istqb.org/istqb-has-released-two-new-syllabi-for-test-automation/ (retrieved 2026-04-21)
- **[S4]** ISTQB. *Updated version of the ISTQB Glossary application now available*. https://istqb.org/updated-version-of-the-istqb-glossary-application-now-available/ (retrieved 2026-04-21)
- **[S9]** ISTQB. *ISTQB Certified Tester Specialist Level Testing with Generative AI (CT-GenAI) Press Release*. https://istqb.org/istqb-certified-tester-specialist-level-testing-with-generative-ai-ct-genai-press-release/ (retrieved 2026-04-21)
- **[S7]** ISTQB. *CTFL-AT Overview v1.0*. https://istqb.org/wp-content/uploads/2024/11/ISTQB-CTFL-AT_Overview_v1.0_80JMrDA.pdf (retrieved 2026-04-21)
- **[F5]** ISTQB Glossary. *Generic Test Automation Architecture*. https://istqb-glossary.page/generic-test-automation-architecture/ (retrieved 2026-04-21)

### Secondary (academic and practitioner)

- **[S5]** Colomo-Palacios, R. et al. *From Certifications to International Standards in Software Testing: Mapping from ISTQB to ISO/IEC/IEEE 29119-2*. Springer Nature. https://link.springer.com/chapter/10.1007/978-3-319-97925-0_4 (retrieved 2026-04-21) -- supplementary PDF at https://www.rcolomo.com/papers/326.pdf
- **[S6]** Sogeti Labs. *Benefits of a Generic Test Automation Architecture*. https://labs.sogeti.com/benefits-of-generic-test-automation-architecture/ (retrieved 2026-04-21); and Adesso Blog. *Test automation architecture (TAA) based on a generic test automation architecture (gTAA) according to ISTQB in practice*. https://www.adesso.de/en/news/blog/test-automation-architecture-taa-based-on-a-generic-test-automation-architecture-gtaa-according-to-istqb-in-practice.jsp (retrieved 2026-04-21)
- **[S10]** Ministry of Testing Community (multiple threads) and practitioner blog posts on ISTQB critique. Example: https://club.ministryoftesting.com/t/istqb-that-s-it-no-more-certification-exams-as-they-prove-nothing/23892 and Satisfice blog https://www.satisfice.com/blog/archives/5167 (retrieved 2026-04-21)

### Supporting

- **[S8]** CTAL-TAE v2.0 syllabus PDF (German Testing Board mirror). https://www.gtb.de/wp-content/uploads/2024/11/ISTQB-CTAL-TAE-Syllabus-v2.0-DE.pdf (retrieved 2026-04-21)
- CTFL v4.0.1 syllabus PDF: https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf (retrieved 2026-04-21)

### Cross-reference

- Landscape card: `/Users/victor.lau/workspace/jerry/projects/PROJ-017-e2e-testing-skill/orchestration/e2e-skill-build-20260420-001/research/landscape/standards-candidates.md#candidate-3`
- Sibling deep-research: `std-1` and `std-2` files in the same `deep-standards/` folder.

---

*Phase 1b research artefact -- to be consumed by Phase 1c synthesiser alongside std-1 and std-2.*
