# Strategy Selection Plan: BUG-006 C4 Migration Implementation

**Generated:** 2026-04-01
**Agent:** adv-selector (v1.0.0)
**SSOT Source:** `.context/rules/quality-enforcement.md`

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Criticality Assessment](#criticality-assessment) | Requested level, auto-escalation check, final level |
| [Auto-Escalation Analysis](#auto-escalation-analysis) | Triggered rules and escalation justification |
| [Selected Strategies (Ordered)](#selected-strategies-ordered) | All 10 required strategies with template paths |
| [H-16 Compliance](#h-16-compliance) | Steelman-before-Devil's Advocate enforcement |
| [Strategy Overrides Applied](#strategy-overrides-applied) | User-requested modifications (if any) |
| [Self-Review Checklist](#self-review-checklist) | Pre-persistence verification per H-15 |

---

## Criticality Assessment

- **Requested Level:** C4 (Critical)
- **Auto-Escalation Applied:** Yes — AE-002, AE-003
- **Escalation Rule IDs:** AE-002 (touches `.context/rules/`), AE-003 (new ADR)
- **Escalation Target:** C3 minimum (both rules)
- **User-Specified Level:** C4 (higher than minimum)
- **Final Level:** C4 (Critical)

**Justification:** The deliverable implements ADR-EPIC002-001 (Unified Output Path Resolution Protocol) across 13 skills, 107 configuration files, and 32 agents. The scope includes:
- Governance rule updates to `.context/rules/agent-development-standards.md` (new MEDIUM standard AD-M-011)
- Infrastructure changes across 3 skill families (eng-team, red-team, user-experience)
- Removal of committed operational state (28 files in `skills/eng-team/output/`)
- Migration of output path patterns affecting all future invocations of 32 agents

This qualifies as irreversible architectural change affecting framework governance. C4 classification is appropriate.

---

## Auto-Escalation Analysis

### Active Escalation Checks (Per SSOT)

| Rule | Condition | Status | Evidence |
|------|-----------|--------|----------|
| AE-001 | Touches `docs/governance/JERRY_CONSTITUTION.md` | No | Deliverable does not modify constitution |
| AE-002 | Touches `.context/rules/` or `.claude/rules/` | **YES — TRIGGERED** | Commit includes `agent-development-standards.md` updates (new MEDIUM standard AD-M-011) |
| AE-003 | New or modified ADR | **YES — TRIGGERED** | Deliverable is ADR-EPIC002-001 (status: proposed, created 2026-03-31) |
| AE-004 | Modifies baselined ADR | No | ADR is new, not modifying prior baselined ADR |
| AE-005 | Security-relevant code | No | No security-specific code changes |
| AE-006 (context fill) | Token exhaustion assessment | No | Context usage nominal; escalation not required |

### Escalation Resolution

- **AE-002 escalation result:** C3 minimum
- **AE-003 escalation result:** C3 minimum
- **Higher escalation applied:** C3 minimum from both rules
- **User specification:** C4 (higher than minimum)
- **Applied level:** C4 (respects user authority per P-020)

**Escalation Summary:** Two independent auto-escalation rules triggered (AE-002, AE-003). Both escalate to C3 minimum. User-specified C4 exceeds the minimum escalation, and is applied without override. Per quality-enforcement.md, C4 requires all 10 selected strategies with no optional strategies.

---

## Selected Strategies (Ordered)

All 10 selected strategies are required for C4 criticality per quality-enforcement.md. The following table shows ordered execution sequence per H-16 and SSOT recommended ordering.

| Order | Strategy ID | Strategy Name | Template Path | Required/Optional | Group |
|-------|-------------|---------------|---------------|-------------------|-------|
| 1 | S-010 | Self-Refine | `.context/templates/adversarial/s-010-self-refine.md` | Required | A: Self-Review |
| 2 | S-003 | Steelman Technique | `.context/templates/adversarial/s-003-steelman.md` | Required | B: Strengthen |
| 3 | S-002 | Devil's Advocate | `.context/templates/adversarial/s-002-devils-advocate.md` | Required | C: Challenge |
| 4 | S-004 | Pre-Mortem Analysis | `.context/templates/adversarial/s-004-pre-mortem.md` | Required | C: Challenge |
| 5 | S-001 | Red Team Analysis | `.context/templates/adversarial/s-001-red-team.md` | Required | C: Challenge |
| 6 | S-007 | Constitutional AI Critique | `.context/templates/adversarial/s-007-constitutional-ai.md` | Required | D: Verify |
| 7 | S-011 | Chain-of-Verification | `.context/templates/adversarial/s-011-cove.md` | Required | D: Verify |
| 8 | S-012 | FMEA | `.context/templates/adversarial/s-012-fmea.md` | Required | E: Decompose |
| 9 | S-013 | Inversion Technique | `.context/templates/adversarial/s-013-inversion.md` | Required | E: Decompose |
| 10 | S-014 | LLM-as-Judge | `.context/templates/adversarial/s-014-llm-as-judge.md` | Required | F: Score |

**Strategy Composite Scores (from ADR-EPIC002-001):**
- S-014 (LLM-as-Judge): 4.40
- S-003 (Steelman): 4.30
- S-013 (Inversion): 4.25
- S-007 (Constitutional AI): 4.15
- S-002 (Devil's Advocate): 4.10
- S-004 (Pre-Mortem): 4.10
- S-010 (Self-Refine): 4.00
- S-012 (FMEA): 3.75
- S-011 (Chain-of-Verification): 3.75
- S-001 (Red Team): 3.35

**Excluded Strategies** (not applicable to C4):
- S-005 (Dialectical Inquiry) — RED risk: requires cross-model LLM
- S-006 (Analysis of Competing Hypotheses) — Redundant with S-013 + S-004
- S-008 (Socratic Method) — Requires interactive multi-turn dialogue
- S-009 (Multi-Agent Debate) — RED risk: requires cross-model LLM
- S-015 (Prompt Adversarial Examples) — RED risk: adversarial prompt injection concern

---

## H-16 Compliance

**H-16 (Steelman before critique):** S-003 (Steelman Technique) MUST be ordered BEFORE S-002 (Devil's Advocate).

| Strategy | Position | Constraint Satisfied |
|----------|----------|---------------------|
| S-003 (Steelman) | 2 | Yes — position 2 < position 3 |
| S-002 (Devil's Advocate) | 3 | Yes — position 3 > position 2 |

**Constraint Status:** SATISFIED. S-003 appears at position 2, S-002 appears at position 3. The ordering enforces strengthening of arguments before adversarial challenge, consistent with H-16 canonical review pairing.

---

## Strategy Overrides Applied

**User-Specified Overrides:** None

**Justification:** The user specified C4 criticality level without requesting any strategy exclusions or additions. Per quality-enforcement.md, C4 criticality requires all 10 selected strategies with no optional strategies. The complete strategy set is applied without modification.

---

## Self-Review Checklist (H-15)

Before persistence, verify per H-15 (Self-Review Before Presenting):

- [x] **All strategy IDs are valid:** All 10 strategies (S-001, S-002, S-003, S-004, S-007, S-010, S-011, S-012, S-013, S-014) are from the selected set per quality-enforcement.md (excluded strategies S-005, S-006, S-008, S-009, S-015 are not included)
- [x] **H-16 ordering satisfied:** S-003 (position 2) before S-002 (position 3) ✓
- [x] **Auto-escalation applied correctly:** AE-002 and AE-003 triggered, escalate to C3 minimum. User specification C4 exceeds minimum and is applied. ✓
- [x] **All template paths valid:** All 10 template paths exist in `.context/templates/adversarial/`:
  - `.context/templates/adversarial/s-001-red-team.md` ✓
  - `.context/templates/adversarial/s-002-devils-advocate.md` ✓
  - `.context/templates/adversarial/s-003-steelman.md` ✓
  - `.context/templates/adversarial/s-004-pre-mortem.md` ✓
  - `.context/templates/adversarial/s-007-constitutional-ai.md` ✓
  - `.context/templates/adversarial/s-010-self-refine.md` ✓
  - `.context/templates/adversarial/s-011-cove.md` ✓
  - `.context/templates/adversarial/s-012-fmea.md` ✓
  - `.context/templates/adversarial/s-013-inversion.md` ✓
  - `.context/templates/adversarial/s-014-llm-as-judge.md` ✓
- [x] **User overrides documented:** No user overrides requested or applied. ✓
- [x] **Required/Optional status correct:** All 10 strategies are marked Required per C4 criticality level. ✓
- [x] **Groups and ordering rationale clear:** Execution order follows SSOT recommended grouping (Self-Review → Strengthen → Challenge → Verify → Decompose → Score). ✓

**Self-Review Result:** PASS. All verification checks complete. Selection plan is ready for persistence and handoff to adv-executor.

---

## Constitutional Compliance

Per the Jerry Constitution governance principles:

| Principle | Requirement | Compliance |
|-----------|------------|-----------|
| P-002 (File Persistence) | Selection plan MUST be persisted to file | Persisted to `projects/PROJ-030-bugs/work/BUG-006-c4-strategy-plan.md` |
| P-003 (No Recursion) | Does NOT invoke other agents or spawn subagents | This agent (adv-selector) is a worker; does not spawn subagents |
| P-020 (User Authority) | User strategy overrides respected; user C4 specification applied | C4 specification applied without override; no user overrides requested |
| P-022 (No Deception) | All selected and excluded strategies transparently listed | 10 selected strategies listed with template paths; 5 excluded strategies listed with exclusion reasons |
| H-15 (Self-Review) | Selection plan self-reviewed before persistence | Self-review checklist completed and PASS |

**Constitutional Status:** COMPLIANT. All principles satisfied.

---

## Next Steps

1. **Handoff to adv-executor:** This selection plan output serves as the orchestration input for the `/adversary` skill's adv-executor agent. Executor will load and apply each strategy in the specified order.

2. **Quality Gate:** Final scoring via S-014 (LLM-as-Judge) will validate the migration deliverable against the 6-dimension S-014 rubric (Completeness, Internal Consistency, Methodological Rigor, Evidence Quality, Actionability, Traceability) with a threshold of >= 0.92 per H-13.

3. **Minimum Iterations:** Per H-14, this C4 deliverable requires minimum 3 creator-critic-revision cycles. All 10 adversarial strategies (tournament mode) are applied in each iteration cycle.

---

## References

| Source | Content | Location |
|--------|---------|----------|
| Quality Enforcement SSOT | Criticality levels, auto-escalation rules, strategy catalog, H-16 ordering | `.context/rules/quality-enforcement.md` |
| Agent Development Standards | Agent role standards, constitutional compliance | `.context/rules/agent-development-standards.md` |
| ADR-EPIC002-001 | Unified Output Path Resolution Protocol (deliverable being reviewed) | `docs/design/ADR-output-path-resolution-001.md` |
| BUG-006 Entity | Bug specification and implementation plan | `projects/PROJ-030-bugs/work/BUG-006-skill-output-path-hardcoded.md` |

---

**Agent Version:** 1.0.0
**Constitutional Compliance:** Jerry Constitution v1.0
**SSOT:** `.context/rules/quality-enforcement.md`
**Created:** 2026-04-01 by adv-selector (Claude Haiku 4.5)
**P-002 Persistence:** File created at `projects/PROJ-030-bugs/work/BUG-006-c4-strategy-plan.md`
