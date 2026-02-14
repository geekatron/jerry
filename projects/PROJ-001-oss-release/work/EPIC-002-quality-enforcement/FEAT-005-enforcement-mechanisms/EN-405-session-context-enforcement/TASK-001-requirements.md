# TASK-001: Requirements for Session Context Enforcement Injection

<!--
DOCUMENT-ID: FEAT-005:EN-405:TASK-001
TEMPLATE: Requirements Specification
VERSION: 1.0.0
AGENT: ps-architect-405 (Claude Opus 4.6)
DATE: 2026-02-14
PARENT: EN-405 (Session Context Enforcement Injection)
FEATURE: FEAT-005 (Quality Framework Enforcement Mechanisms)
EPIC: EPIC-002 (Quality Framework Enforcement)
PROJECT: PROJ-001-oss-release
QUALITY-TARGET: >= 0.92
METHODOLOGY: NASA NPR 7123.1D (Requirements Engineering)
CONSUMERS: TASK-002 (preamble design), TASK-003 (hook enhancement), TASK-004 (integration), TASK-005 (implementation), TASK-006 (preamble content)
-->

> **Version:** 1.0.0
> **Agent:** ps-architect-405 (Claude Opus 4.6)
> **Status:** COMPLETE
> **Created:** 2026-02-14
> **Methodology:** NASA NPR 7123.1D Section 6.1 (Technical Requirements Definition)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Purpose and Scope](#purpose-and-scope) | Why this requirements document exists and what it covers |
| [Source Traceability](#source-traceability) | Mapping of authoritative inputs to requirements |
| [Functional Requirements](#functional-requirements) | What the session context injection must accomplish |
| [Integration Requirements](#integration-requirements) | How injection integrates with existing session_start_hook.py |
| [Performance Requirements](#performance-requirements) | Timing, token budget, and overhead constraints |
| [Adversarial Strategy Requirements](#adversarial-strategy-requirements) | Strategy activation sets from barrier-2 handoff |
| [Error Handling Requirements](#error-handling-requirements) | Fail-open behavior and logging |
| [Requirements Traceability Matrix](#requirements-traceability-matrix) | Full traceability from requirement to source and verification |
| [Verification Methods](#verification-methods) | How each requirement will be verified |
| [References](#references) | All source documents |

---

## Purpose and Scope

This document formalizes the requirements for EN-405 (Session Context Enforcement Injection). EN-405 enhances the SessionStart hook to inject quality framework enforcement context at session initialization, establishing the L1 behavioral foundation that L2 (UserPromptSubmit) subsequently reinforces.

Requirements are derived from four authoritative sources:

1. **EN-403 TASK-001** (Hook Requirements) -- Formal requirements REQ-403-050 through REQ-403-055, REQ-403-070/071, REQ-403-075 through REQ-403-082, REQ-403-094 through REQ-403-096
2. **EN-403 TASK-004** (SessionStart Design) -- Architecture design specification including SessionQualityContextGenerator, XML output format, token budget, error handling
3. **Barrier-2 ADV-to-ENF Handoff** -- Per-criticality strategy activation sets, 8-dimension context taxonomy, decision tree, token budget constraints
4. **EN-404 TASK-003/TASK-004** -- Tiered enforcement strategy (HARD/MEDIUM/SOFT), HARD rule inventory (H-13 through H-19), quality-enforcement.md SSOT designation, language patterns

### Scope Boundaries

**In scope:**
- Quality framework context injection at session start (V-003)
- SessionQualityContextGenerator module creation
- Integration with existing session_start_hook.py
- XML-tagged quality context output
- Per-criticality strategy awareness content

**Out of scope:**
- UserPromptSubmit hook (L2) -- covered by EN-403 TASK-002
- PreToolUse hook (L3) -- covered by EN-403 TASK-003
- PostToolUse hook (L4) -- deferred to Phase 5
- Rule file rewriting (quality-enforcement.md creation) -- covered by EN-404 TASK-005/006/007
- Dynamic strategy selection at runtime -- EN-405 provides awareness, not runtime gating

---

## Source Traceability

### Authoritative Source Documents

| Source ID | Document | Location | Content Used |
|-----------|----------|----------|-------------|
| SRC-001 | EN-403 TASK-001 (Hook Requirements) | `EN-403-hook-based-enforcement/TASK-001-hook-requirements.md` | REQ-403-050 through REQ-403-055, cross-cutting requirements |
| SRC-002 | EN-403 TASK-004 (SessionStart Design) | `EN-403-hook-based-enforcement/TASK-004-sessionstart-design.md` | Architecture, XML format, token budget, integration flow |
| SRC-003 | Barrier-2 ADV-to-ENF Handoff | `orchestration/.../barrier-2/adv-to-enf/barrier-2-adv-to-enf-handoff.md` | Per-criticality strategy sets, decision tree, token budgets, ENF-MIN |
| SRC-004 | EN-404 TASK-003 (Tiered Enforcement) | `EN-404-rule-based-enforcement/TASK-003-tiered-enforcement.md` | HARD rules H-13 through H-19, SSOT designation, quality-enforcement.md |
| SRC-005 | EN-404 TASK-004 (HARD Language Patterns) | `EN-404-rule-based-enforcement/TASK-004-hard-language-patterns.md` | L2-REINJECT content, enforcement language patterns |
| SRC-006 | Current session_start_hook.py | `scripts/session_start_hook.py` | Existing implementation to enhance |

---

## Functional Requirements

### Content Requirements

| Req ID | Requirement | Priority | Source | Rationale |
|--------|-------------|----------|--------|-----------|
| FR-405-001 | The session context injection SHALL inject quality gate threshold information (>= 0.92) into the session context via a `<quality-gate>` XML section. | HARD | SRC-001 (REQ-403-050); SRC-002 (quality-gate section) | S-014 (LLM-as-Judge) scoring backbone requires threshold awareness from session start. |
| FR-405-002 | The session context injection SHALL inject HARD constitutional principles (P-003, P-020, P-022) and the UV-only environment rule into a `<constitutional-principles>` XML section. | HARD | SRC-001 (REQ-403-051); SRC-002 (constitutional section); SRC-004 (H-01 through H-06) | Constitutional principles are the behavioral foundation; must be primed at session start. |
| FR-405-003 | The session context injection SHALL inject a listing of all 10 selected adversarial strategies with concise descriptions into an `<adversarial-strategies>` XML section. | HARD | SRC-002 (strategies section); SRC-003 (Per-Criticality Strategy Sets) | Claude must know the full strategy catalog to select appropriate strategies per criticality. |
| FR-405-004 | The session context injection SHALL inject the C1-C4 decision criticality framework with assessment criteria and auto-escalation rules into a `<decision-criticality>` XML section. | HARD | SRC-001 (REQ-403-054, REQ-403-060); SRC-002 (criticality section); SRC-004 (Decision Criticality Integration) | Criticality assessment drives strategy selection and quality gate enforcement. |
| FR-405-005 | The session context injection SHALL inject the creator-critic-revision cycle requirement (minimum 3 iterations for C2+ tasks). | HARD | SRC-001 (REQ-403-052, REQ-403-096); SRC-004 (H-14) | The cycle is a HARD rule (H-14) per EN-404 TASK-003. Must be established at session start. |
| FR-405-006 | The session context injection SHALL inject the S-014 leniency bias awareness note (R-014-FN calibration). | MEDIUM | SRC-002 (quality-gate section); SRC-003 (S-014 Known limitation) | Without calibration awareness, quality scores systematically exceed actual quality. |
| FR-405-007 | The session context injection SHALL inject the mandatory governance escalation rule: artifacts touching `docs/governance/`, `.context/rules/`, or `.claude/rules/` are automatically C3+. | HARD | SRC-001 (REQ-403-061); SRC-004 (H-19, Mandatory Escalation Rules) | Governance auto-escalation is a HARD rule. Session start must prime this awareness. |

### Format Requirements

| Req ID | Requirement | Priority | Source | Rationale |
|--------|-------------|----------|--------|-----------|
| FR-405-010 | The quality context SHALL be wrapped in a top-level `<quality-framework version="1.0">` XML tag. | HARD | SRC-001 (REQ-403-094); SRC-002 (XML output design) | XML tags enable Claude to distinguish enforcement content from user content. |
| FR-405-011 | The quality context SHALL contain exactly 4 XML subsections: `<quality-gate>`, `<constitutional-principles>`, `<adversarial-strategies>`, `<decision-criticality>`. | HARD | SRC-002 (Content Specification) | The 4-section structure provides complete enforcement coverage while maintaining token efficiency. |
| FR-405-012 | Each XML section SHALL be independently parseable -- Claude must be able to reference individual sections without reading the full block. | MEDIUM | SRC-001 (REQ-403-094); SRC-002 (Content Design Principles) | Independent parseability improves Claude's ability to selectively reference enforcement context. |
| FR-405-013 | The quality context content SHALL be phrased as actionable instructions ("Score all deliverables", "Assess every task's criticality"), not descriptions. | MEDIUM | SRC-002 (Content Design Principles, point 4) | Imperative voice has ~90% compliance rate vs ~40% for advisory passive voice (SRC-005, Enforcement Language Hierarchy). |

### Criticality-Aware Content Requirements

| Req ID | Requirement | Priority | Source | Rationale |
|--------|-------------|----------|--------|-----------|
| FR-405-020 | The `<adversarial-strategies>` section SHALL list all 10 selected strategies: S-001 (Red Team), S-002 (Devil's Advocate), S-003 (Steelman), S-004 (Pre-Mortem), S-007 (Constitutional AI), S-010 (Self-Refine), S-011 (CoVe), S-012 (FMEA), S-013 (Inversion), S-014 (LLM-as-Judge). | HARD | SRC-003 (Per-Criticality Strategy Sets); SRC-002 (strategies section) | Claude must know the complete catalog; per-criticality selection is a runtime decision. |
| FR-405-021 | The `<decision-criticality>` section SHALL include per-criticality strategy activation guidance: C1 (S-010 required), C2 (S-007 + S-002 + S-014 required), C3 (6+ strategies required), C4 (all 10 required). | MEDIUM | SRC-003 (Per-Criticality Strategy Sets) | Per-criticality strategy sets are the primary output of the ADV pipeline's EN-303 decision tree. |
| FR-405-022 | The `<decision-criticality>` section SHALL include the auto-escalation rules: AE-001 (JERRY_CONSTITUTION.md -> C3 min), AE-002 (.claude/rules/ -> C3 min), AE-003 (new ADR -> C3 min), AE-004 (modified baselined ADR -> C4), AE-005 (security code -> C3 min). | MEDIUM | SRC-003 (Auto-Escalation Rules) | Auto-escalation rules fire before strategy selection; Claude must know them from session start. |

---

## Integration Requirements

| Req ID | Requirement | Priority | Source | Rationale |
|--------|-------------|----------|--------|-----------|
| IR-405-001 | The session context injection SHALL complement the existing project context resolution in session_start_hook.py without breaking current functionality. | HARD | SRC-001 (REQ-403-053); SRC-006 (existing hook) | Existing hook handles project context, validation, and pre-commit warnings. Integration must be additive. |
| IR-405-002 | The quality context SHALL be appended to the `additionalContext` field of the hook JSON output, after the existing project context. | HARD | SRC-002 (Integration with Existing Hook, Change 2) | The `additionalContext` field is the Claude Code mechanism for context injection. Quality context is additive content. |
| IR-405-003 | The `systemMessage` field SHALL NOT be modified by the quality context injection. | HARD | SRC-002 (What Does NOT Change) | The systemMessage is user-visible terminal output. Quality context is for Claude's context window only. |
| IR-405-004 | The SessionQualityContextGenerator SHALL be implemented as a separate module in `src/infrastructure/internal/enforcement/session_quality_context.py`. | HARD | SRC-002 (File Layout); SRC-001 (REQ-403-080) | Hexagonal architecture requires enforcement logic separated from hook infrastructure. |
| IR-405-005 | The session_start_hook.py SHALL import SessionQualityContextGenerator via a try/except block with a `QUALITY_CONTEXT_AVAILABLE` flag, enabling incremental deployment. | HARD | SRC-002 (Change 1, ImportError Handling) | If the module is not deployed, the existing hook must function unchanged. Fail-open by design. |
| IR-405-006 | The quality context generation SHALL occur AFTER format_hook_output() and BEFORE output_json() in the main() function flow. | HARD | SRC-002 (Integration Flow) | This position ensures project context is established before quality context is appended. |
| IR-405-007 | The following existing hook behaviors SHALL NOT be modified: (a) project context resolution, (b) pre-commit hook warning, (c) error handling for uv/CLI failures, (d) hook JSON output structure. | HARD | SRC-002 (What Does NOT Change); SRC-001 (REQ-403-053) | Backward compatibility is mandatory. Regression in existing functionality is unacceptable. |

---

## Performance Requirements

| Req ID | Requirement | Priority | Source | Rationale |
|--------|-------------|----------|--------|-----------|
| PR-405-001 | The quality context generation SHALL add less than 500ms overhead to the session start process. | HARD | EN-405 AC-9 | Session start must not noticeably slow down. The generator is stateless string concatenation; overhead should be negligible (<1ms). |
| PR-405-002 | The quality context SHALL contribute approximately 360 tokens to the L1 Static Context budget. | MEDIUM | SRC-002 (Token Estimate); SRC-001 (REQ-403-055) | ~360 tokens is 4.7% of the 12,476 L1 budget, leaving ample room for .claude/rules/ files. |
| PR-405-003 | The quality context token count SHALL be verified against the 12,476 token L1 target from ADR-EPIC002-002. Combined SessionStart contribution (project context + quality context) SHALL NOT exceed ~590 tokens. | MEDIUM | SRC-002 (Token Budget Contribution) | Total SessionStart contribution (~590 tokens) must fit within the L1 budget alongside ~11,886 tokens for rules files. |
| PR-405-004 | If the token budget requires trimming, the quality context SHALL support degradation in this priority: (1) remove full strategy list (saves ~120 tokens), (2) condense criticality to single line (saves ~65 tokens), (3) minimum viable: quality gate + constitutional principles = ~145 tokens. | LOW | SRC-002 (Budget Sensitivity) | Budget sensitivity plan ensures graceful degradation if rules optimization requires tighter budgets. |

---

## Adversarial Strategy Requirements

These requirements integrate the ADV pipeline findings from the Barrier-2 handoff.

| Req ID | Requirement | Priority | Source | Rationale |
|--------|-------------|----------|--------|-----------|
| SR-405-001 | The session context SHALL communicate strategy availability awareness, not runtime strategy selection or enforcement. | HARD | SRC-003 (Integration Guidance for EN-405) | Session start provides the catalog; runtime selection is a separate concern driven by the decision tree. |
| SR-405-002 | The strategy listing SHALL order strategies by their role in the quality framework: scoring backbone (S-014) first, constitutional compliance (S-007) second, universal self-review (S-010) third, then remaining strategies in descending composite score order. | MEDIUM | SRC-003 (Per-Criticality Strategy Sets); SRC-002 (strategies section) | Ordering by role prominence ensures most critical strategies are salient even under early context rot. |
| SR-405-003 | The session context SHALL NOT include full token budget costs per strategy. Token budget information is reference-level detail beyond the scope of session priming. | LOW | SRC-003 (Token Budget Constraints) | Token budget detail would consume ~80 additional tokens for minimal enforcement value at session start. |
| SR-405-004 | The session context SHALL NOT include ENF-MIN degraded environment handling. ENF-MIN is a runtime detection concern, not a session priming concern. | LOW | SRC-003 (ENF-MIN Handling) | Including ENF-MIN adds ~60 tokens of rarely applicable content. ENF-MIN handling belongs in runtime enforcement logic. |
| SR-405-005 | The session context SHALL include the SYN #1 pairing guidance (S-003 Steelman before S-002 Devil's Advocate) as part of the quality gate section or adversarial strategies section. | MEDIUM | SRC-003 (Strategy Pairings, SYN pair #1) | This is the "canonical Jerry review protocol" per Barrier-2. It costs ~15 tokens and is high enforcement value. |

---

## Error Handling Requirements

| Req ID | Requirement | Priority | Source | Rationale |
|--------|-------------|----------|--------|-----------|
| EH-405-001 | The quality context generation SHALL implement fail-open error handling: any exception SHALL result in empty quality context, not hook failure. | HARD | SRC-001 (REQ-403-070); SRC-002 (Error Handling) | User authority (P-020) requires enforcement never blocks session start due to quality context errors. |
| EH-405-002 | All quality context generation errors SHALL be logged to the hook error log with sufficient detail for diagnosis. | HARD | SRC-001 (REQ-403-071); SRC-002 (Error Handling) | Fail-open must not mean fail-silent. Errors must be observable. |
| EH-405-003 | When quality context generation fails, the UserPromptSubmit hook (L2) SHALL still provide basic enforcement independently. | HARD | SRC-002 (Error Handling, "Failure does NOT cascade") | L2 operates independently of L1. If SessionStart quality context fails, L2 still fires. |
| EH-405-004 | ImportError for the SessionQualityContextGenerator module SHALL be handled gracefully, resulting in the existing hook behavior with no quality context. | HARD | SRC-002 (ImportError Handling) | Enables incremental deployment and safe rollback. |

---

## Requirements Traceability Matrix

| EN-405 Req ID | EN-403 Source Req | Barrier-2 Section | EN-404 Source | Verification |
|---------------|-------------------|-------------------|---------------|-------------|
| FR-405-001 | REQ-403-050 | Quality Gate and Scoring | H-13, H-17 | Test (T) |
| FR-405-002 | REQ-403-051 | -- | H-01, H-02, H-03, H-05 | Test (T) |
| FR-405-003 | REQ-403-051 | Per-Criticality Strategy Sets | -- | Test (T) |
| FR-405-004 | REQ-403-054, REQ-403-060 | Decision Tree | Decision Criticality Integration | Test (T) |
| FR-405-005 | REQ-403-052, REQ-403-096 | Creator-Critic-Revision | H-14 | Test (T) |
| FR-405-006 | -- | Quality Gate and Scoring | -- | Inspection (I) |
| FR-405-007 | REQ-403-061 | Auto-Escalation Rules | H-19 | Test (T) |
| FR-405-010 | REQ-403-094 | -- | -- | Test (T) |
| FR-405-011 | REQ-403-094 | -- | -- | Test (T) |
| FR-405-012 | REQ-403-094 | -- | -- | Inspection (I) |
| FR-405-013 | -- | -- | HARD Language Patterns | Inspection (I) |
| FR-405-020 | -- | Per-Criticality Strategy Sets | -- | Test (T) |
| FR-405-021 | -- | Per-Criticality Strategy Sets | -- | Test (T) |
| FR-405-022 | -- | Auto-Escalation Rules | Mandatory Escalation Rules | Test (T) |
| IR-405-001 | REQ-403-053 | -- | -- | Test (T) |
| IR-405-002 | REQ-403-053 | -- | -- | Test (T) |
| IR-405-003 | -- | -- | -- | Inspection (I) |
| IR-405-004 | REQ-403-080 | -- | -- | Inspection (I) |
| IR-405-005 | REQ-403-070 | -- | -- | Test (T) |
| IR-405-006 | -- | -- | -- | Inspection (I) |
| IR-405-007 | REQ-403-053 | -- | -- | Test (T) |
| PR-405-001 | -- | -- | -- | Test (T) |
| PR-405-002 | REQ-403-055 | -- | -- | Analysis (A) |
| PR-405-003 | REQ-403-055 | -- | -- | Analysis (A) |
| PR-405-004 | -- | Token Budget Constraints | -- | Inspection (I) |
| SR-405-001 | -- | Integration Guidance | -- | Inspection (I) |
| SR-405-002 | -- | Per-Criticality Strategy Sets | -- | Inspection (I) |
| SR-405-003 | -- | Token Budget Constraints | -- | Inspection (I) |
| SR-405-004 | -- | ENF-MIN Handling | -- | Inspection (I) |
| SR-405-005 | -- | Strategy Pairings | -- | Test (T) |
| EH-405-001 | REQ-403-070 | -- | -- | Test (T) |
| EH-405-002 | REQ-403-071 | -- | -- | Test (T) |
| EH-405-003 | REQ-403-085 | -- | -- | Analysis (A) |
| EH-405-004 | REQ-403-070 | -- | -- | Test (T) |

**Coverage Summary:**
- Total requirements: 34
- Traced to EN-403 requirements: 22 (65%)
- Traced to Barrier-2 handoff: 15 (44%)
- Traced to EN-404 deliverables: 10 (29%)
- With defined verification method: 34 (100%)
- HARD priority: 21 (62%)
- MEDIUM priority: 9 (26%)
- LOW priority: 4 (12%)

---

## Verification Methods

| Method | Symbol | Count | Applicable When |
|--------|--------|-------|-----------------|
| Test (T) | T | 21 | Requirement specifies functional behavior with observable output |
| Inspection (I) | I | 10 | Requirement specifies structural property (format, architecture) |
| Analysis (A) | A | 3 | Requirement specifies a constraint requiring analytical techniques (token budget) |

### Key Verification Activities

| Activity | Requirements Verified | Method | Timing |
|----------|----------------------|--------|--------|
| Unit tests for SessionQualityContextGenerator | FR-405-001 through FR-405-022 | T | TASK-005 implementation |
| Integration tests for session_start_hook.py | IR-405-001 through IR-405-007 | T | TASK-010 integration testing |
| Token budget analysis | PR-405-002, PR-405-003 | A | TASK-006 preamble content |
| Performance measurement | PR-405-001 | T | TASK-010 integration testing |
| Error injection tests | EH-405-001 through EH-405-004 | T | TASK-005 implementation |
| Code review for architecture compliance | IR-405-004, IR-405-005 | I | TASK-007 code review |
| Content review for language patterns | FR-405-013 | I | TASK-008 adversarial review |

---

## References

| # | Document | Location | Content Used |
|---|----------|----------|--------------|
| 1 | EN-403 TASK-001 (Hook Requirements) | `FEAT-005/EN-403-hook-based-enforcement/TASK-001-hook-requirements.md` | REQ-403-050 through REQ-403-096 |
| 2 | EN-403 TASK-004 (SessionStart Design) | `FEAT-005/EN-403-hook-based-enforcement/TASK-004-sessionstart-design.md` | Architecture, XML format, integration flow, token budget |
| 3 | Barrier-2 ADV-to-ENF Handoff | `orchestration/.../barrier-2/adv-to-enf/barrier-2-adv-to-enf-handoff.md` | Per-criticality strategy sets, decision tree, auto-escalation, ENF-MIN |
| 4 | EN-404 TASK-003 (Tiered Enforcement) | `FEAT-005/EN-404-rule-based-enforcement/TASK-003-tiered-enforcement.md` | HARD rules H-13 through H-19, SSOT, quality-enforcement.md |
| 5 | EN-404 TASK-004 (HARD Language Patterns) | `FEAT-005/EN-404-rule-based-enforcement/TASK-004-hard-language-patterns.md` | Enforcement language hierarchy, L2-REINJECT format |
| 6 | Current session_start_hook.py | `scripts/session_start_hook.py` | Existing implementation patterns |
| 7 | EN-405 Enabler Definition | `FEAT-005/EN-405-session-context-enforcement/EN-405-session-context-enforcement.md` | Acceptance criteria, task decomposition |

---

*Agent: ps-architect-405 (Claude Opus 4.6)*
*Date: 2026-02-14*
*Parent: EN-405 Session Context Enforcement Injection*
*Quality Target: >= 0.92*
*Total Requirements: 34 (21 HARD, 9 MEDIUM, 4 LOW)*
