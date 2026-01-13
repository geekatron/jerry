# Traceability Enhancement: TDD Approach

> **Document ID:** TEST-NSE-TRACE-001
> **Version:** 1.0
> **Date:** 2026-01-09
> **Status:** TDD RED PHASE - Tests First
> **Purpose:** Evidence-based TDD approach to enhance traceability in NASA SE Skill

---

## L0: Executive Summary (ELI5)

**What's the problem?**
Like a detective solving a case, NASA Systems Engineering needs to track every clue (requirement) to every risk and design decision. Right now, our risk agent says "there's a risk" but doesn't point to which specific requirements are affected. This is like a doctor saying "something's wrong" but not saying which body part.

**What's the fix?**
We're adding explicit links from:
1. Risks → Requirements (which requirements are at risk?)
2. Architecture decisions → Requirements (which requirements drove this design?)
3. Integration artifacts → Upstream documents (where did this come from?)

**How do we do it safely?**
We write tests FIRST (TDD), then make changes. If any existing test breaks, we fix it before moving forward.

---

## L1: Technical Approach (Engineer Level)

### 1.1 Research Foundation

| Source | Citation | Key Finding |
|--------|----------|-------------|
| [NPR 7123.1D](https://nodis3.gsfc.nasa.gov/displayDir.cfm?t=NPR&c=7123&s=1B) | NASA | "Requirements must be individually verifiable and traceable to a higher level requirement" |
| [INCOSE Traceability WG](https://www.incose.org/docs/default-source/working-groups/requirements-wg/monthlymeetings2024/traceability_110524.pdf) | Lou Wheatcraft | "Traceability: The Threads That Link SE Artifacts" - bidirectional tracing required |
| [Perforce RTM Guide](https://www.perforce.com/resources/alm/requirements-traceability-matrix) | Industry | "Bidirectional traceability enables navigation both forward and backward" |
| [Visure Solutions](https://visuresolutions.com/requirements-management-traceability-guide/best-practices-requirements-traceabilty/) | Industry | "Automated bidirectional traceability minimizes risk and ensures quality" |
| [Security Compass](https://www.securitycompass.com/blog/four-types-of-requirements-traceability/) | Industry | "A risk matrix should link potential risks to requirements for mitigation measures" |
| [ComplianceQuest](https://www.compliancequest.com/requirements-traceability/what-is-rtm-matrix-and-example/) | Industry | "Traceability matrices demonstrate all risks are mitigated by requirements" |

### 1.2 TDD Methodology

Following industry best practices from:
- [Microsoft Engineering Playbook](https://microsoft.github.io/code-with-engineering-playbook/automated-testing/unit-testing/tdd-example) - Red-Green-Refactor
- [DAGWorks TDD for LLMs](https://blog.dagworks.io/p/test-driven-development-tdd-of-llm) - pytest for LLM testing
- [DeepEval G-Eval](https://deepeval.com/docs/metrics-llm-evals) - LLM-as-a-Judge evaluation
- [Latent Space AI Agents TDD](https://www.latent.space/p/anita-tdd) - Behavioral testing for agents

**TDD Cycle:**
```
RED     → Write failing test for expected behavior
GREEN   → Implement minimum code to pass test
REFACTOR → Improve code while keeping tests green
```

### 1.3 Issues to Fix

| Issue ID | Problem | P-040 Violation | Enhancement |
|----------|---------|-----------------|-------------|
| ORCH-ISS-001 | Risk register lacks requirement refs | Yes | Add `affected_requirements` field |
| ORCH-ISS-002 | Change impact incomplete for risk | Yes | Requires ISS-001 fix |
| ORCH-ISS-003 | Architecture has limited req trace | Partial | Add `driving_requirements` section |
| ORCH-ISS-004 | Integration lacks artifact refs | Partial | Add `source_artifacts` field |

---

## L2: TDD Test Suite (Architect Level)

### 2.1 Test Strategy

**Test Categories:**
1. **Schema Tests** - Verify template fields exist
2. **Compliance Tests** - Verify P-040 traceability principle
3. **Output Tests** - Verify agent produces traceable output
4. **Regression Tests** - Verify existing behavior unchanged

**Evaluation Method:**
- G-Eval LLM-as-Judge with threshold 0.8 (per DeepEval best practices)
- Golden dataset comparison (per Datadog methodology)

### 2.2 RED Phase Tests (Write Before Implementation)

---

#### BHV-TRACE-001: Risk-to-Requirement Traceability

```yaml
id: BHV-TRACE-001
category: Compliance
principle: P-040 (Requirements Traceability)
agent: nse-risk
status: RED (Test written, implementation pending)
threshold: 0.8
industry_reference: "INCOSE Requirements WG - Bidirectional Traceability"

scenario: |
  nse-risk agent creates a risk register that traces each risk
  to affected requirements (per NPR 7123.1D Process 13 and NPR 8000.4C)

prompt: |
  ## NSE CONTEXT (REQUIRED)
  - **Project ID:** PROJ-TEST-001
  - **Entry ID:** e-001
  - **Topic:** Authentication Risks

  Identify and assess risks for the following requirements:
  - REQ-AUTH-001: The system shall authenticate users via OAuth 2.0
  - REQ-AUTH-002: The system shall enforce MFA for admin users
  - REQ-AUTH-003: Sessions shall expire after 30 minutes of inactivity

expected_behavior: |
  Agent should:
  1. Create risk register at projects/PROJ-TEST-001/risks/
  2. Each risk MUST include "Affected Requirements" field
  3. Affected Requirements MUST reference specific REQ-* IDs
  4. Bidirectional: Requirements should be traceable TO risks

pass_criteria:
  - risk_file_created: true
  - has_affected_requirements_field: true
  - affected_requirements_contains_req_ids: true
  - req_ids_match_format: "^REQ-[A-Z]+-\\d{3}$"
  - disclaimer_present: true

evaluation_rubric:
  5: "All risks have affected_requirements with valid REQ-* IDs"
  4: "Most risks (>80%) have affected_requirements"
  3: "Some risks (~50%) have affected_requirements"
  2: "Few risks (<30%) have affected_requirements"
  1: "No affected_requirements field present"

current_behavior: |
  Agent creates risk register WITHOUT affected_requirements field.
  grep -c "REQ-" RISK-NSE-SKILL-001.md → 0 specific requirement refs
  P-040 VIOLATION: Risks are not traceable to requirements.
```

---

#### BHV-TRACE-002: Architecture Driving Requirements

```yaml
id: BHV-TRACE-002
category: Compliance
principle: P-040 (Requirements Traceability)
agent: nse-architecture
status: RED (Test written, implementation pending)
threshold: 0.8
industry_reference: "NPR 7123.1D Process 3/4 - Trace design to requirements"

scenario: |
  nse-architecture agent creates trade study that traces each alternative
  and the selected design to driving requirements.

prompt: |
  ## NSE CONTEXT (REQUIRED)
  - **Project ID:** PROJ-TEST-001
  - **Entry ID:** e-002
  - **Topic:** Data Storage Architecture

  Perform a trade study for data storage approach considering:
  - REQ-DATA-001: System shall store 10TB of data
  - REQ-DATA-002: Data shall be encrypted at rest
  - REQ-DATA-003: System shall support 99.9% availability

expected_behavior: |
  Agent should:
  1. Create trade study at projects/PROJ-TEST-001/architecture/
  2. Trade study MUST include "Driving Requirements" section
  3. Each alternative MUST show which requirements it addresses
  4. Selected design MUST trace to all addressed requirements
  5. Any requirements NOT addressed MUST be flagged

pass_criteria:
  - trade_study_created: true
  - has_driving_requirements_section: true
  - alternatives_reference_requirements: true
  - selected_design_traces_to_requirements: true
  - unaddressed_requirements_flagged: true

evaluation_rubric:
  5: "Full requirements trace matrix for all alternatives"
  4: "Driving requirements section with most req refs (>80%)"
  3: "Driving requirements section with some refs (~50%)"
  2: "Generic requirements mention without specific IDs"
  1: "No requirements traceability in trade study"

current_behavior: |
  TSR-NSE-SKILL-001.md has only 2 REQ-NSE refs (driving only).
  No requirements trace matrix for alternatives.
  Limited P-040 compliance.
```

---

#### BHV-TRACE-003: Integration Source Artifact Refs

```yaml
id: BHV-TRACE-003
category: Compliance
principle: P-040 (Requirements Traceability)
agent: nse-integration
status: RED (Test written, implementation pending)
threshold: 0.8
industry_reference: "NPR 7123.1D Process 6/12 - Interface traceability"

scenario: |
  nse-integration agent creates ICD that traces each interface to
  source architecture and requirements artifacts.

prompt: |
  ## NSE CONTEXT (REQUIRED)
  - **Project ID:** PROJ-TEST-001
  - **Entry ID:** e-003
  - **Topic:** API Integration

  Create interface control document for:
  - Interface IF-001: REST API between Frontend and Backend
  - Source Architecture: TSR-PROJ-TEST-001.md
  - Source Requirements: REQ-API-001, REQ-API-002

expected_behavior: |
  Agent should:
  1. Create ICD at projects/PROJ-TEST-001/interfaces/
  2. Each interface MUST include "Source Artifacts" field
  3. Source Artifacts MUST reference TSR-* and/or REQ-* documents
  4. Bidirectional: Architecture should be traceable to interfaces

pass_criteria:
  - icd_created: true
  - has_source_artifacts_field: true
  - references_architecture_docs: true
  - references_requirements_docs: true
  - uses_document_id_format: true

evaluation_rubric:
  5: "All interfaces have source_artifacts with TSR and REQ refs"
  4: "Most interfaces (>80%) have source_artifacts"
  3: "Some interfaces (~50%) have source_artifacts"
  2: "Interfaces reference agents but not specific documents"
  1: "No source artifact traceability"

current_behavior: |
  ICD-NSE-SKILL-001.md references agent names not artifact IDs.
  No explicit TSR-* or REQ-* document references per interface.
  ORCH-ISS-004: Limited artifact-level traceability.
```

---

#### BHV-TRACE-004: Risk Change Impact Analysis

```yaml
id: BHV-TRACE-004
category: Workflow
principle: P-040 (Requirements Traceability)
agent: nse-risk
status: RED (Test written, implementation pending)
threshold: 0.8
industry_reference: "FMEA/FMECA hazard-to-requirement linkage"

scenario: |
  When a requirement changes, nse-risk can identify all affected risks
  via the affected_requirements field (reverse lookup).

prompt: |
  ## NSE CONTEXT (REQUIRED)
  - **Project ID:** PROJ-TEST-001
  - **Entry ID:** e-004
  - **Topic:** Change Impact - REQ-AUTH-001

  Assess risk impact if REQ-AUTH-001 is changed from OAuth 2.0 to SAML.

  Existing Risk Register:
  - R-001: If OAuth token is compromised... | Affected: REQ-AUTH-001, REQ-AUTH-002
  - R-002: If MFA is bypassed... | Affected: REQ-AUTH-002
  - R-003: If session timeout fails... | Affected: REQ-AUTH-003

expected_behavior: |
  Agent should:
  1. Identify R-001 as affected (references REQ-AUTH-001)
  2. Not flag R-002 or R-003 as directly affected
  3. Provide impact analysis for affected risks
  4. Recommend risk register update

pass_criteria:
  - identifies_affected_risks: ["R-001"]
  - correctly_excludes: ["R-002", "R-003"]
  - provides_impact_analysis: true
  - recommends_update: true

evaluation_rubric:
  5: "Precisely identifies affected risks via req trace"
  4: "Identifies most affected risks correctly"
  3: "Identifies some risks but with false positives"
  2: "Cannot determine affected risks from req ID"
  1: "Reports 'cannot determine impact' (current state)"

current_behavior: |
  ORCH-ISS-002: Risk impact assessment cannot identify affected
  requirements because risks don't trace to requirements.
  Change Impact workflow incomplete for risk domain.
```

---

### 2.3 Regression Tests

These tests verify existing behavior is preserved:

```yaml
regression_tests:
  - id: REG-001
    name: "Risk register still produces L0/L1/L2 output"
    agent: nse-risk
    expected: All three output levels present

  - id: REG-002
    name: "Risk register still uses If-Then format"
    agent: nse-risk
    expected: All risks use "If [condition], then [consequence]"

  - id: REG-003
    name: "Risk register still includes 5x5 matrix"
    agent: nse-risk
    expected: L×C scoring with proper thresholds

  - id: REG-004
    name: "Risk register still escalates RED risks"
    agent: nse-risk
    expected: RED risks highlighted in L0 summary

  - id: REG-005
    name: "Trade study still uses Kepner-Tregoe matrix"
    agent: nse-architecture
    expected: Weighted criteria evaluation present

  - id: REG-006
    name: "ICD still uses N² diagram format"
    agent: nse-integration
    expected: Interface matrix structure preserved

  - id: REG-007
    name: "All outputs still include P-043 disclaimer"
    agent: all
    expected: Mandatory disclaimer present
```

---

## 3. Implementation Plan

### Phase 1: Schema Enhancement (GREEN Phase)

| Change | Agent | Field to Add | Location |
|--------|-------|--------------|----------|
| Risk-Req Trace | nse-risk | `affected_requirements` | Risk Details table |
| Arch-Req Trace | nse-architecture | `requirements_trace` | Trade Study section |
| Integ-Artifact Trace | nse-integration | `source_artifacts` | Interface table |

### Phase 2: Template Updates

**Risk Register Template Enhancement:**
```markdown
#### R-001: {Risk Title}

| Attribute | Value |
|-----------|-------|
| **Risk Statement** | If [condition], then [consequence] |
| **Affected Requirements** | REQ-XXX-001, REQ-XXX-002 | ← NEW FIELD
| **Category** | Technical / Cost / Schedule / Safety |
| ... existing fields ...
```

**Trade Study Template Enhancement:**
```markdown
## 2. Requirements Trace Matrix ← NEW SECTION

| Requirement | Alternative A | Alternative B | Alternative C |
|-------------|:-------------:|:-------------:|:-------------:|
| REQ-XXX-001 | ✅ Full | ⚠️ Partial | ❌ Gap |
| REQ-XXX-002 | ✅ Full | ✅ Full | ✅ Full |
```

**ICD Template Enhancement:**
```markdown
| Interface | Participants | Source Artifacts | REQ Trace |
|-----------|-------------|------------------|-----------|
| IF-001 | A ↔ B | TSR-XXX-001, REQ-XXX-001 | REQ-IF-001 | ← NEW COLUMNS
```

### Phase 3: Validation

1. Run BHV-TRACE-001 through BHV-TRACE-004 → Expect PASS
2. Run REG-001 through REG-007 → Expect PASS (no regression)
3. Re-run orchestration tests → Expect improved results

---

## 4. Success Criteria

| Metric | Before | After | Target |
|--------|--------|-------|--------|
| ORCH-ISS-001 | OPEN | CLOSED | Risk traces to requirements |
| ORCH-ISS-002 | OPEN | CLOSED | Change impact works |
| ORCH-ISS-003 | DEFERRED | CLOSED | Full req trace matrix |
| ORCH-ISS-004 | DEFERRED | CLOSED | Artifact refs present |
| Orchestration Pass Rate | 63% | 95%+ | All patterns pass |

---

## 5. References

1. [NPR 7123.1D - NASA SE Processes](https://nodis3.gsfc.nasa.gov/displayDir.cfm?t=NPR&c=7123&s=1B) - Traceability requirements
2. [INCOSE Traceability Working Group](https://www.incose.org/docs/default-source/working-groups/requirements-wg/monthlymeetings2024/traceability_110524.pdf) - Best practices
3. [Perforce RTM Guide](https://www.perforce.com/resources/alm/requirements-traceability-matrix) - Bidirectional traceability
4. [Microsoft Engineering Playbook TDD](https://microsoft.github.io/code-with-engineering-playbook/automated-testing/unit-testing/tdd-example) - Red-Green-Refactor
5. [DAGWorks TDD for LLMs](https://blog.dagworks.io/p/test-driven-development-tdd-of-llm) - pytest for LLM testing
6. [DeepEval G-Eval](https://deepeval.com/docs/metrics-llm-evals) - LLM-as-a-Judge evaluation
7. [Confident AI Agent Metrics](https://deepeval.com/guides/guides-ai-agent-evaluation-metrics) - Agent evaluation
8. [Security Compass Traceability](https://www.securitycompass.com/blog/four-types-of-requirements-traceability/) - Risk-requirement linking
9. [NASA FMEA Handbook](https://standards.nasa.gov/standard/GSFC/GSFC-HDBK-8004) - Hazard-requirement traceability
10. [ComplianceQuest RTM](https://www.compliancequest.com/requirements-traceability/what-is-rtm-matrix-and-example/) - Risk mitigation traceability

---

*DISCLAIMER: This test plan is AI-generated based on industry best practices for TDD and NASA SE standards. Implementation requires human review and validation.*
