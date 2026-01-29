# EN-014:DISC-008: Comprehensive TDD Implementation Gap

<!--
TEMPLATE: Discovery
VERSION: 1.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9, worktracker.md (Discovery File)
CREATED: 2026-01-29 (User Review - Post TASK-168)
PURPOSE: Document comprehensive gaps in TDD identified by user review
TRIGGER: User feedback on TDD-EN014-domain-schema-v2.md after TASK-168 Final Adversarial Review
EXTENDS: DISC-007 (surface-level gaps from automated reviews)
-->

> **Type:** discovery
> **Status:** RESOLVED
> **Priority:** CRITICAL
> **Impact:** CRITICAL
> **Created:** 2026-01-29T14:30:00Z
> **Resolved:** 2026-01-29T16:30:00Z
> **Parent:** EN-014
> **Owner:** Claude
> **Source:** User Review (Post TASK-168)
> **Resolution:** TDD v3.0.0 with Sections 6-11 (ps-critic 0.96)

---

## Frontmatter

```yaml
id: "EN-014:DISC-008"
work_type: DISCOVERY
title: "Comprehensive TDD Implementation Gap"

classification: TECHNICAL

status: RESOLVED
resolution: "TDD v3.0.0 revision with Sections 6-11 addressing all 9 gaps (ps-critic 0.96)"

priority: CRITICAL
impact: CRITICAL

assignee: "Claude"
created_by: "Claude"

created_at: "2026-01-29T14:30:00Z"
updated_at: "2026-01-29T14:30:00Z"
completed_at: "2026-01-29T14:30:00Z"

parent_id: "EN-014"

tags:
  - "tdd-gap"
  - "implementation-architecture"
  - "runtime-environment"
  - "testing-strategy"
  - "ci-cd"
  - "jerry-cli"
  - "critical"

finding_type: GAP
confidence_level: HIGH
source: "User Review (Post TASK-168)"
research_method: "User feedback analysis"

validated: true
validation_date: "2026-01-29T14:30:00Z"
validated_by: "User"
```

---

## State Machine

**Current State:** `DOCUMENTED`

```
PENDING → IN_PROGRESS → DOCUMENTED
                            ↑
                       (completed)
```

---

## Summary

**Core Finding:** The TDD-EN014-domain-schema-v2.md passed automated adversarial review (TASK-168: 10/10 reviews, all ≥0.90) but **fails the implementability test**. User review identified that Sections 5.2.1 and 5.2.2 are "afterthought" patches rather than integrated architecture. The TDD lacks sufficient detail for Claude (or another implementer) to execute without blocking ambiguity.

**Key Findings:**
1. **Section 5.2.1/5.2.2 are disconnected** - Python code provided without runtime context, integration points, or lifecycle
2. **No testing strategy** - RED/GREEN/REFACTOR TDD approach completely absent
3. **No CI/CD pipeline specification** - GitHub Actions configuration and quality gates missing
4. **No runtime environment** - Python interpreter, dependencies, and user machine setup undefined
5. **Jerry CLI integration not considered** - Custom script vs. existing CLI architecture not evaluated

**Validation:** Confirmed by User review after TASK-168 approval

---

## Context

### Background

After TASK-168 Final Adversarial Review passed with all scores ≥0.90, the user conducted a manual review of the TDD and identified critical gaps that the automated review missed. The user's key question:

> "If you gave this to yourself is there enough detail for you to execute smoothly or would you be blocked by the ambiguity?"

**Answer: The TDD would cause blocking ambiguity during implementation.**

### Research Question

**What comprehensive implementation details are missing from the TDD that would enable unambiguous implementation of the domain validation system?**

### Relationship to DISC-007

DISC-007 captured surface-level gaps from ps-critic and nse-qa reviews:
- IMPL-001: Technology selection (ajv vs jsonschema)
- IMPL-002: Validator location
- IMPL-003: Execution context
- IMPL-004: SV-006 algorithm

**DISC-008 extends DISC-007** with deeper architectural gaps:
- Runtime environment specification
- Testing strategy (RED/GREEN/REFACTOR)
- CI/CD pipeline configuration
- Jerry CLI integration analysis
- Integration lifecycle (when, how, who calls validators)

---

## Finding

### Gap Analysis Matrix

| Gap ID | Category | DISC-007 | DISC-008 (New) | User Feedback |
|--------|----------|----------|----------------|---------------|
| GAP-IMPL-001 | Technology | ✅ Partial | ❌ | No runtime specification |
| GAP-IMPL-002 | Location | ✅ Partial | ❌ | Jerry CLI option not evaluated |
| GAP-IMPL-003 | Execution | ✅ Partial | ❌ | Integration lifecycle missing |
| GAP-IMPL-004 | Algorithm | ✅ Yes | ❌ | Dangling method without caller |
| GAP-IMPL-005 | Runtime | ❌ | ✅ NEW | Python version, venv, deps |
| GAP-IMPL-006 | Testing | ❌ | ✅ NEW | RED/GREEN/REFACTOR absent |
| GAP-IMPL-007 | CI/CD | ❌ | ✅ NEW | GitHub Actions missing |
| GAP-IMPL-008 | CLI | ❌ | ✅ NEW | Jerry CLI integration |
| GAP-IMPL-009 | Implementability | ❌ | ✅ NEW | Self-assessment: would Claude be blocked? |

### GAP-IMPL-005: Runtime Environment Specification

**Current State:** Section 5.2.2 provides Python code with imports:
```python
from dataclasses import dataclass

def sv006_circular_relationships(domain_data: dict) -> list[ValidationError]:
    ...
```

**What's Missing:**
- Python interpreter specification (python, python3, uv?)
- Virtual environment setup (venv, poetry, pipx?)
- Dependency management (requirements.txt, pyproject.toml?)
- User machine setup instructions
- Pre-requisite checks

**User Quote:**
> "You provided python code but there is no information about how we will execute it (python, python3, uv) - you are pulling in imports, which means dependencies but we have no answers on how we will ensure the user's machine is setup."

### GAP-IMPL-006: Testing Strategy

**Current State:** TDD has NO testing strategy section.

**What's Missing:**
- RED/GREEN/REFACTOR approach specification
- Unit test structure for validators (SV-001 through SV-006)
- Integration test approach
- Test data requirements
- Coverage requirements
- pytest configuration
- Test file location (`tests/unit/`, `tests/integration/`)

**User Quote:**
> "I don't see any information about the testing strategy... Specification with an emphasis on RED/GREEN/REFACTOR TDD strategy."

### GAP-IMPL-007: CI/CD Pipeline Specification

**Current State:** TDD has NO CI/CD section.

**What's Missing:**
- GitHub Actions workflow specification
- Pipeline stages (lint, test, validate)
- Quality gates in CI
- Trigger conditions (PR, push to main)
- Artifact publishing
- Validation on domain YAML file changes

**User Quote:**
> "I don't see any information about the CI/CD pipeline and what we should setup for the github CI/CD runs."

### GAP-IMPL-008: Jerry CLI Integration Analysis

**Current State:** TDD assumes custom validation scripts without considering existing architecture.

**What's Missing:**
- Analysis of Jerry CLI architecture (`jerry session`, `jerry items`, `jerry projects`)
- Decision on custom script vs. CLI integration
- Evaluation of `jerry transcript validate-domain <path>` approach
- Session start hook integration (already uses Jerry CLI)

**User Quote:**
> "We already have a Jerry CLI that solves some of those concerns so it would be important to weigh out writing a custom script vs integrating with the CLI, which is already used by the session start hook."

### GAP-IMPL-009: Integration Lifecycle

**Current State:** Section 5.2.2 provides `sv006_circular_relationships()` function but no context.

**What's Missing:**
- When is validation called? (skill invocation, CLI command, CI pipeline)
- How is validation triggered? (automatic, manual, both)
- Who/what calls the validators? (orchestrator, CLI, hook)
- Error handling flow (block execution? warn and continue?)
- Validation results format and reporting

**User Quote:**
> "5.2.2 doesn't even explain when or how it's called - it's just some dangling method without context - how and when is it going to be called and by who?"

---

## Evidence

### Source Documentation

| Evidence ID | Type | Description | Source | Date |
|-------------|------|-------------|--------|------|
| E-001 | User Feedback | Direct user review of TDD | Session transcript | 2026-01-29 |
| E-002 | TDD | TDD-EN014-domain-schema-v2.md Section 5.2 | docs/design/ | 2026-01-29 |
| E-003 | DISC-007 | Prior gap discovery | EN-014--DISC-007 | 2026-01-29 |
| E-004 | TASK-168 | Final adversarial review (passed but insufficient) | qa/EN-014-e-168-final-review.md | 2026-01-29 |

### User Feedback (Verbatim Excerpts)

**On Section 5.2.1/5.2.2:**
> "Section 5.2.1 and 5.2.2 seem like an afterthought and not really incorporated to solve the problem."

**On Python Code:**
> "You provided python code but there is no information about how we will execute it (python, python3, uv) - you are pulling in imports, which means dependencies but we have no answers on how we will ensure the user's machine is setup."

**On SV-006:**
> "5.2.2 doesn't even explain when or how it's called - it's just some dangling method without context - how and when is it going to be called and by who?"

**On Testing:**
> "I don't see any information about the testing strategy."

**On CI/CD:**
> "I don't see any information about the CI/CD pipeline and what we should setup for the github CI/CD runs."

**On Implementability:**
> "You are going to be consuming this TDD to implement the functionality? If you gave this to yourself is there enough detail for you to execute smoothly or would you be blocked by the ambiguity?"

**On Jerry CLI:**
> "We already have a Jerry CLI that solves some of those concerns so it would be important to weigh out writing a custom script vs integrating with the CLI"

---

## Implications

### Impact on Project

1. **TASK-169 (Human Approval Gate)** - Cannot proceed until TDD gaps are addressed
2. **Implementation Tasks (TASK-126..130, TASK-150..159)** - Blocked by ambiguous TDD
3. **Quality Gate** - Automated reviews passed but TDD fails implementability test

### Decision Made

**DEC-001: CLI Namespace for Domain Validation**
- Decision: Option C - `jerry transcript validate-domain <path>`
- Rationale: Domain validation is scoped to transcript skill; YAGNI for cross-cutting namespace
- See: [EN-014--DEC-001-cli-namespace-domain-validation.md](./EN-014--DEC-001-cli-namespace-domain-validation.md)

### Risks Identified

| Risk | Severity | Mitigation |
|------|----------|------------|
| Implementation blocked by ambiguity | CRITICAL | Address gaps before proceeding |
| Inconsistent validation across integration points | HIGH | Specify all integration points in TDD |
| Testing coverage gaps | MEDIUM | Specify RED/GREEN/REFACTOR strategy |
| CI/CD not enforcing validation | MEDIUM | Specify GitHub Actions workflow |

### Remediation Plan

1. **Create TASK-176:** ps-analyst Deep Gap Analysis (5W2H, Ishikawa)
2. **Create TASK-177:** nse-architect TDD Revision with implementation architecture
3. **Create TASK-178:** ps-critic Validation (0.95 threshold)
4. **Re-execute TASK-168:** Final adversarial review after TDD revision

---

## Relationships

### Extends

- [EN-014:DISC-007](./EN-014--DISC-007-tdd-validation-implementation-gap.md) - Surface-level gaps from automated reviews

### Creates

- [EN-014:DEC-001](./EN-014--DEC-001-cli-namespace-domain-validation.md) - CLI Namespace Decision
- TASK-176 - ps-analyst Deep Gap Analysis (to be created)
- TASK-177 - nse-architect TDD Revision (to be created)
- TASK-178 - ps-critic Validation (to be created)

### Blocks

- [TASK-169](./TASK-169-human-gate.md) - Human Approval Gate (cannot proceed until TDD revised)

### Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Parent | [EN-014-domain-context-files.md](./EN-014-domain-context-files.md) | Parent enabler |
| TDD | [TDD-EN014-domain-schema-v2.md](./docs/design/TDD-EN014-domain-schema-v2.md) | Document with gaps |
| DISC-007 | [EN-014--DISC-007](./EN-014--DISC-007-tdd-validation-implementation-gap.md) | Prior gap discovery |
| Final Review | [EN-014-e-168-final-review.md](./qa/EN-014-e-168-final-review.md) | Review that passed but TDD still insufficient |

---

## Recommendations

### Immediate Actions

1. **Create DEC-001** - Document CLI namespace decision (Option C: `jerry transcript validate-domain`)
2. **Create TASK-176** - ps-analyst deep gap analysis with user feedback as input
3. **Create TASK-177** - nse-architect TDD revision with implementation architecture
4. **Create TASK-178** - ps-critic validation at 0.95 threshold

### Hybrid Approach (User Approved)

```
GAP ANALYSIS → TDD REVISION WORKFLOW
=====================================

Step 1: ps-analyst Deep Gap Analysis
      - Input: This DISC-008 + User feedback
      - Frameworks: 5W2H, Ishikawa
      - Output: Comprehensive gap analysis with remediation requirements

Step 2: nse-architect TDD Revision
      - Input: Gap analysis from Step 1
      - Focus: Implementation architecture, not implementation code
      - Scope:
        * Runtime environment specification
        * Testing strategy (RED/GREEN/REFACTOR)
        * CI/CD pipeline specification
        * Jerry CLI integration (Option C)
        * Integration lifecycle (when/how/who)

Step 3: ps-critic Validation
      - Threshold: 0.95
      - Focus: Implementability - would Claude be blocked?

Step 4: Re-execute TASK-168
      - Fresh final adversarial review
```

### TDD Revision Scope

The revised TDD should answer these questions unambiguously:

| Question | Required Answer |
|----------|----------------|
| How do I run the validators? | `jerry transcript validate-domain <path>` |
| What Python version is required? | Python 3.11+ |
| How are dependencies managed? | pyproject.toml in skills/transcript/ |
| Where do validators live? | src/interface/cli/ + src/domain/validation/ |
| When is validation called? | Skill invocation, CLI command, CI pipeline |
| How do I test validators? | RED/GREEN/REFACTOR with pytest |
| What's the CI/CD setup? | .github/workflows/validate-domain.yml |

---

## Open Questions

### Questions Resolved

1. **Q:** Should validators be runnable code or LLM specifications?
   - **Resolution:** Option A - Runnable Python code (all validators)
   - **Rationale:** Deterministic validation required for all integration points (skill, CLI, CI)

2. **Q:** What CLI namespace should domain validation use?
   - **Resolution:** Option C - `jerry transcript validate-domain <path>`
   - **Rationale:** YAGNI - scoped to transcript skill, can extract later if needed

3. **Q:** What level of detail for CI/CD and testing?
   - **Resolution:** Specification level with RED/GREEN/REFACTOR emphasis
   - **Rationale:** Implementation phase handles actual files; TDD specifies approach

### Questions for Gap Analysis

1. **Q:** What existing Jerry CLI architecture patterns should validation follow?
   - **Investigation Method:** ps-analyst analysis of `src/interface/cli/`
   - **Priority:** HIGH

2. **Q:** What test infrastructure exists that validation can leverage?
   - **Investigation Method:** ps-analyst analysis of `tests/` structure
   - **Priority:** HIGH

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-29 | Claude | Created discovery document from user review feedback |

---

## Metadata

```yaml
id: "EN-014:DISC-008"
parent_id: "EN-014"
work_type: DISCOVERY
title: "Comprehensive TDD Implementation Gap"
status: DOCUMENTED
priority: CRITICAL
impact: CRITICAL
created_by: "Claude"
created_at: "2026-01-29T14:30:00Z"
updated_at: "2026-01-29T14:30:00Z"
completed_at: "2026-01-29T14:30:00Z"
tags: ["tdd-gap", "implementation-architecture", "runtime-environment", "testing-strategy", "ci-cd", "jerry-cli", "critical"]
source: "User Review (Post TASK-168)"
finding_type: GAP
confidence_level: HIGH
validated: true
extends: "EN-014:DISC-007"
creates:
  - "EN-014:DEC-001"
  - "TASK-176"
  - "TASK-177"
  - "TASK-178"
blocks:
  - "TASK-169"
```
