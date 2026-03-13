# Strategy Selection Plan

## Criticality Assessment

- **Requested Level:** C2 (Standard)
- **Auto-Escalation Applied:** No
- **Final Level:** C2 (confirmed, no escalation)

### Escalation Rules Checked (Active Runtime)

| Rule ID | Condition | Triggered | Rationale |
|---------|-----------|-----------|-----------|
| AE-001 | Deliverable touches `docs/governance/JERRY_CONSTITUTION.md` | No | Deliverable is orchestration plan, not governance document |
| AE-002 | Deliverable touches `.context/rules/` or `.claude/rules/` | No | Deliverable path is in projects/, not .context/ |
| AE-003 | Deliverable is new or modified ADR | No | Deliverable is Orchestration Plan type, not ADR |
| AE-004 | Deliverable modifies baselined ADR | No | No baselined ADR at this path |
| AE-005 | Deliverable contains security-relevant code | No | YAML reader uses stdlib yaml.safe_load, no custom crypto/auth |
| AE-006 | Token exhaustion at C3+ criticality | No | Context fill ~30% (NOMINAL tier) |

**Conclusion:** Requested C2 is final criticality level.

---

## Selected Strategies (Ordered)

| Order | Strategy ID | Strategy Name | Template Path | Required/Optional | Group |
|-------|-------------|---------------|---------------|-------------------|-------|
| 1 | S-010 | Self-Refine | `.context/templates/adversarial/s-010-self-refine.md` | Optional (C2) | A: Self-Review |
| 2 | S-003 | Steelman Technique | `.context/templates/adversarial/s-003-steelman.md` | Optional (C2) | B: Strengthen |
| 3 | S-002 | Devil's Advocate | `.context/templates/adversarial/s-002-devils-advocate.md` | Required (C2) | C: Challenge |
| 4 | S-007 | Constitutional AI Critique | `.context/templates/adversarial/s-007-constitutional-ai.md` | Required (C2) | D: Verify |
| 5 | S-014 | LLM-as-Judge | `.context/templates/adversarial/s-014-llm-as-judge.md` | Required (C2) | F: Score |

---

## H-16 Compliance

- **S-003 position:** 2
- **S-002 position:** 3
- **Constraint satisfied:** Yes — S-003 (Steelman, pos 2) ordered BEFORE S-002 (Devil's Advocate, pos 3) per H-16 HARD rule requirement

**Constraint Verification:** The canonical pairing of Steelman before Devil's Advocate prevents premature rejection of sound approaches by strengthening the case first, then attacking it. Order 2 < Order 3 satisfies H-16.

---

## Strategy Overrides Applied

- None
- User provided clear criticality level (C2) with no overrides

---

## C2 Criticality Mapping Reference

Per `quality-enforcement.md` Criticality Levels table (v1.6.0):

| Category | Value |
|----------|-------|
| **Required Strategies** | S-007 (Constitutional AI Critique), S-002 (Devil's Advocate), S-014 (LLM-as-Judge) |
| **Optional Strategies** | S-003 (Steelman), S-010 (Self-Refine) |
| **Quality Threshold** | >= 0.92 |
| **Min Iterations** | 3 |
| **Max Iterations** | 5 (per agent-development-standards.md RT-M-010) |

**Why S-010 and S-003 included:** Both are optional for C2 but strengthen the creator-critic-revision cycle per H-14. Self-refine (S-010) provides early self-correction before external critique; Steelman (S-003) before Devil's Advocate ensures ideas are strengthened before attacked.

---

## Execution Workflow

| Phase | Strategies | Critic Agent | Threshold | Max Iter |
|-------|-----------|--------------|-----------|----------|
| Phase 1 (Fix) | S-010, S-003, S-002, S-007, S-014 | adv-scorer | >= 0.93 | 5 |
| Phase 2 (Test) | S-010, S-003, S-002, S-007, S-014 | adv-scorer | >= 0.93 | 5 |
| Phase 3 (E2E) | S-010, S-003, S-002, S-007, S-014 | adv-scorer | >= 0.93 | 5 |

---

## Excluded Strategies (C2)

| ID | Name | Reason |
|----|------|--------|
| S-001 | Red Team Analysis | Optional for C2; not selected |
| S-004 | Pre-Mortem Analysis | Optional for C2; not selected |
| S-011 | Chain-of-Verification | Optional for C2; not selected |
| S-012 | FMEA | Optional for C2; not selected |
| S-013 | Inversion Technique | Optional for C2; not selected |

---

## Quality Compliance Requirements

Per H-13, H-14, H-15, H-16, H-17, H-18:

- [x] Quality threshold >= 0.92 for C2+ (H-13)
- [x] Creator-critic-revision cycle minimum 3 iterations (H-14)
- [x] Self-review (S-010) before presenting (H-15)
- [x] Steelman (S-003) before Devil's Advocate (S-002) (H-16)
- [x] Quality scoring via S-014 LLM-as-Judge (H-17)
- [x] Constitutional compliance check (S-007) (H-18)

---

## P-003 Compliance (Self-Check)

- [x] No Task tool invocations in selector
- [x] No agent delegation to subagents
- [x] Direct tool use only (Read, Write, Glob)
- [x] Single-level execution (worker agent to orchestrator)

---

## Deliverable Artifacts

- **Strategy Plan (YAML):** `projects/PROJ-0037-doc-module/orchestration/bugfix-20260312-001/impl/adversary-strategy-plan.yaml`
- **Strategy Plan (Markdown):** `projects/PROJ-0037-doc-module/orchestration/bugfix-20260312-001/impl/STRATEGY_SELECTION_PLAN.md` (this file)

---

**Generated:** 2026-03-12
**Agent:** adv-selector
**SSOT:** `.context/rules/quality-enforcement.md` (v1.6.0)
**Constitutional Compliance:** P-003 (no recursive subagents), P-020 (user authority), P-022 (no deception)
