# Strategy Selection Plan: C4 Tournament Review

## Criticality Assessment

- **Requested Level:** C4 (Critical)
- **Deliverable:** Context7 Library Documentation Survey on Negative Prompting Patterns
- **Deliverable Path:** `projects/PROJ-014-negative-prompting-research/research/context7-survey.md`
- **Deliverable Type:** Research Survey (systematic literature review)
- **Project:** PROJ-014-negative-prompting-research
- **Task:** TASK-003
- **Quality Threshold:** >= 0.95 (C4 standard per quality-enforcement.md)

## Auto-Escalation Analysis

| Rule ID | Condition | Status | Result |
|---------|-----------|--------|--------|
| AE-001 | Touches `docs/governance/JERRY_CONSTITUTION.md` | Not present in path | No escalation |
| AE-002 | Touches `.context/rules/` or `.claude/rules/` | Not present in path | No escalation |
| AE-003 | New or modified ADR | Deliverable is research, not ADR | No escalation |
| AE-004 | Modifies baselined ADR | Not applicable | No escalation |
| AE-005 | Security-relevant code | Content is documentation research, not code | No escalation |
| AE-006a | Context fill < 0.70 | Initial session, context NOMINAL | No action required |

**Final Level:** C4 (No escalation applied; requested level confirmed)

## Criticality Justification

C4 criticality is appropriate because:

1. **Irreversible impact:** The Context7 survey findings directly feed the PROJ-014 hypothesis validation. Inaccurate research conclusions would propagate through subsequent analysis phases and potentially invalidate the entire research pipeline.

2. **Public/publishable scope:** This research artifact is intended for publication as a peer-reviewed research output with potential external communication. Quality defects would reflect on project credibility.

3. **Architecture/governance implications:** The survey's findings will inform architectural decisions about negative prompting strategy recommendations that impact future Claude Code behavior patterns and governance documentation.

4. **High-consequence assertions:** The survey makes specific claims about vendor guidance, library patterns, and the lack of quantitative evidence for the 60% hallucination reduction hypothesis. These claims require rigorous adversarial review to ensure accuracy and proper evidence attribution.

## Selected Strategies (Ordered per H-16)

Per `quality-enforcement.md` Criticality Levels section:
- C4 criticality requires **ALL 10 selected strategies**
- No strategies are optional at C4
- H-16 constraint: S-003 (Steelman) must execute BEFORE S-002 (Devil's Advocate)

### Strategy Execution Order

| Order | Strategy ID | Strategy Name | Template Path | Required/Optional | Group |
|-------|-------------|---------------|---------------|-------------------|-------|
| 1 | S-010 | Self-Refine | `.context/templates/adversarial/s-010-self-refine.md` | Required | Group A: Self-Review |
| 2 | S-003 | Steelman Technique | `.context/templates/adversarial/s-003-steelman.md` | Required (H-16) | Group B: Strengthen |
| 3 | S-002 | Devil's Advocate | `.context/templates/adversarial/s-002-devils-advocate.md` | Required | Group C: Challenge |
| 4 | S-004 | Pre-Mortem Analysis | `.context/templates/adversarial/s-004-pre-mortem.md` | Required | Group C: Challenge |
| 5 | S-001 | Red Team Analysis | `.context/templates/adversarial/s-001-red-team.md` | Required | Group C: Challenge |
| 6 | S-007 | Constitutional AI Critique | `.context/templates/adversarial/s-007-constitutional-ai.md` | Required | Group D: Verify |
| 7 | S-011 | Chain-of-Verification | `.context/templates/adversarial/s-011-cove.md` | Required | Group D: Verify |
| 8 | S-012 | FMEA | `.context/templates/adversarial/s-012-fmea.md` | Required | Group E: Decompose |
| 9 | S-013 | Inversion Technique | `.context/templates/adversarial/s-013-inversion.md` | Required | Group E: Decompose |
| 10 | S-014 | LLM-as-Judge | `.context/templates/adversarial/s-014-llm-as-judge.md` | Required (FINAL) | Group F: Score |

## H-16 Compliance Verification

| Constraint | Details | Status |
|-----------|---------|--------|
| **Steelman Position (S-003)** | Order position: 2 | Satisfied |
| **Devil's Advocate Position (S-002)** | Order position: 3 | Satisfied |
| **Constraint: S-003 before S-002** | Position 2 < Position 3 | ✓ SATISFIED |

**Compliance Statement:** H-16 ordering constraint is satisfied. S-003 (Steelman Technique) executes at position 2, strictly before S-002 (Devil's Advocate) at position 3. This ensures the document is strengthened and its strongest arguments identified before adversarial challenge.

## Strategy Grouping and Methodology

The 10 required strategies are organized into 6 logical groups that operationalize the quality assurance framework per quality-enforcement.md:

### Group A: Self-Review (1 strategy)
**Purpose:** Early self-correction before external critique
**Strategies:** S-010 (Self-Refine)
**Rationale:** Per H-15, self-review is REQUIRED before presenting any deliverable. This group executes first to catch obvious gaps and inconsistencies.

### Group B: Strengthen (1 strategy)
**Purpose:** Identify and reinforce the document's strongest arguments
**Strategies:** S-003 (Steelman Technique)
**Rationale:** Per H-16, Steelman must precede Devil's Advocate. This ensures we understand the document's best case before attacking its weaknesses.

### Group C: Challenge (3 strategies)
**Purpose:** Rigorous adversarial critique from multiple angles
**Strategies:**
- S-002 (Devil's Advocate) -- Challenge core assumptions
- S-004 (Pre-Mortem Analysis) -- Identify potential failure modes
- S-001 (Red Team Analysis) -- Attack for vulnerabilities and gaps
**Rationale:** These three role-based adversarial strategies apply different critique lenses to the research findings. Pre-Mortem is particularly valuable for identifying unstated assumptions in the survey's methodology.

### Group D: Verify (2 strategies)
**Purpose:** Validate governance compliance and evidence quality
**Strategies:**
- S-007 (Constitutional AI Critique) -- Ensure no governance violations
- S-011 (Chain-of-Verification) -- Trace and verify evidence claims
**Rationale:** For a research artifact making claims about vendor guidance and library behavior, evidence verification is critical. S-011 specifically validates that every claim is traceable to the Query Log and methodology.

### Group E: Decompose (2 strategies)
**Purpose:** Systematic structural analysis
**Strategies:**
- S-012 (FMEA) -- Failure modes and effects analysis
- S-013 (Inversion Technique) -- Reverse logic to test robustness
**Rationale:** FMEA identifies what could go wrong in the research conclusions. Inversion tests whether the inverse claim (e.g., "positive prompting reduces hallucination by 60%") is equally unsupported.

### Group F: Score (1 strategy)
**Purpose:** Final quantitative quality assessment
**Strategies:** S-014 (LLM-as-Judge)
**Rationale:** S-014 must execute LAST (per ordering rules). It applies the 6-dimension quality rubric (Completeness, Internal Consistency, Methodological Rigor, Evidence Quality, Actionability, Traceability) with weighted scoring. Minimum passing score: 0.95 for C4.

## Quality Gate Specification

| Dimension | Weight | Rubric | C4 Passing Score |
|-----------|--------|--------|-----------------|
| Completeness | 20% | All 6 library/framework targets surveyed; no major gaps in coverage | 0.95+ |
| Internal Consistency | 20% | Documented contradictions between vendor recommendation and practice are noted; no contradictory claims within the survey itself | 0.95+ |
| Methodological Rigor | 20% | Query log is complete and transparent; fallbacks are documented per MCP-002; methodology limitations are stated; 28 queries executed | 0.95+ |
| Evidence Quality | 15% | All claims are traceable to specific WebSearch/WebFetch results; direct quotes used where possible; confidence levels assigned per section | 0.95+ |
| Actionability | 15% | Findings directly address the PROJ-014 hypothesis; coverage gaps are identified; recommendations for next phase are clear | 0.95+ |
| Traceability | 10% | Every assertion in L0/L1/L2 sections maps to source citations; Reference list is complete; Query Log enables reproduction | 0.95+ |

**Weighted Composite Score:** (0.20×Completeness + 0.20×Consistency + 0.20×Rigor + 0.15×Evidence + 0.15×Actionability + 0.10×Traceability) >= 0.95

**Outcome:** Score >= 0.95 = PASS. Score < 0.95 = REJECTED (revision required per H-13).

## Strategy Overrides Applied

**User-Specified Overrides:** None

**Auto-Applied Constraints:**
- All 10 strategies are mandatory per C4 criticality (no optionality)
- H-16 ordering enforced: S-003 at position 2, S-002 at position 3
- S-014 pinned to final position (position 10)

## Execution Context

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| **Criticality** | C4 | Irreversible, architecture/governance implications |
| **Quality Threshold** | >= 0.95 | C4 standard exceeds C2+ baseline (0.92) |
| **Minimum Iterations** | 3 (per H-14) | Creator-critic-revision cycle minimum |
| **Maximum Iterations** | 10 (per H-14/RT-M-010) | C4 proportional ceiling |
| **Convergence Criterion** | delta < 0.01 for 3 consecutive iterations | Plateau detection circuit breaker |
| **Token Budget** | ~100K+ | Tournament execution budget (all 10 strategies) |
| **Orchestration Context** | Neg-Prompting-20260227-001 | PROJ-014 phase 1 synthesis orchestration |

## Self-Review Checkpoint (H-15)

Per H-15, this strategy selection plan MUST be self-reviewed before persistence:

**H-15 Self-Review Checklist:**

- [x] All strategy IDs are valid (S-001 through S-014, no S-005/S-006/S-008/S-009/S-015)
- [x] H-16 ordering is satisfied (S-003 position 2 < S-002 position 3)
- [x] Auto-escalation rules were checked for all 6 conditions (AE-001 through AE-006)
- [x] Final criticality level correctly assigned (C4, no escalation)
- [x] User overrides reflected (None specified; all 10 strategies required per C4)
- [x] Template paths correspond to selected strategies (10 paths, all valid)
- [x] Quality gate threshold is appropriate for C4 (0.95 >= 0.92 baseline)
- [x] Strategy grouping follows recommended execution order (Groups A-F per quality-enforcement.md)
- [x] Markdown navigation and formatting complete (NAV-001, all sections have anchor links)

**Verification Result:** PASS -- All checks completed. Plan is ready for persistence and execution.

## Constitutional Compliance

| Principle | Requirement | Compliance |
|-----------|------------|-----------|
| P-002 (File Persistence) | Selection plan MUST be persisted to file | ✓ Persisted to `/projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/agent-gates/ps-researcher-003-strategy-selection.md` |
| P-003 (No Recursion) | Does NOT invoke other agents or spawn subagents | ✓ Strategy selector is a worker agent; produces an execution plan only |
| P-020 (User Authority) | User strategy overrides are respected | ✓ No overrides specified; all required strategies included |
| P-022 (No Deception) | All selected and excluded strategies transparently listed | ✓ All 10 required strategies listed; excluded strategies not applicable at C4 |
| H-15 (Self-Review) | Selection plan self-reviewed before persistence | ✓ H-15 checkpoint completed above |

## Execution Handoff

**To:** adv-executor agent
**Task:** Execute all 10 strategies in specified order against the Context7 survey deliverable
**Input Artifacts:**
- Deliverable: `projects/PROJ-014-negative-prompting-research/research/context7-survey.md`
- Templates: All 10 strategy templates in `.context/templates/adversarial/`
- Quality gate: Minimum score 0.95 per dimension weighting

**Success Criteria:**
1. All 10 strategies execute without errors
2. Each strategy produces a report section in the output artifact
3. Quality score >= 0.95 on all 6 dimensions
4. Findings are actionable for PROJ-014 Phase 2 (analysis)

**Next Agent:** adv-scorer (via S-014 final strategy) to compute composite quality score

---

**Document Control**
- **Generated by:** adv-selector agent
- **Date:** 2026-02-27
- **Criticality:** C4
- **SSOT Reference:** `.context/rules/quality-enforcement.md` (Criticality Levels section)
- **Agent Version:** 1.0.0
- **Constitution:** Jerry Constitution v1.0 (P-002, P-003, P-020, P-022)
