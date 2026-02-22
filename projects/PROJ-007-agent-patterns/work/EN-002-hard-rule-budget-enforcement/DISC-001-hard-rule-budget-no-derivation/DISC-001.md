# EN-002:DISC-001: HARD Rule Budget Ceiling Has No Principled Derivation

> **Type:** discovery
> **Status:** validated
> **Priority:** high
> **Impact:** high
> **Created:** 2026-02-21T22:00:00Z
> **Completed:** 2026-02-21T23:30:00Z
> **Parent:** EN-002
> **Owner:** Claude (PROJ-007 orchestrator)
> **Source:** C4 adversary tournament on HARD rule budget

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Core finding |
| [Context](#context) | Background and research question |
| [Finding](#finding) | Evidence chain |
| [Evidence](#evidence) | Source documentation |
| [Implications](#implications) | Impact on project |
| [Relationships](#relationships) | Related work items |
| [Recommendations](#recommendations) | Actionable next steps |

---

## Summary

The HARD rule ceiling of 35 in `quality-enforcement.md` was set retroactively without any principled derivation. The original ceiling of <= 25 (EN-404) was silently breached when H-25..H-30 were added, then retroactively raised to 35 in commit `936d61c` to accommodate the existing count plus headroom.

**Key Findings:**
- The original <= 25 ceiling (EN-404) had qualitative rationale ("scarcity preserves signal") but no quantitative derivation
- The ceiling was silently breached at 30 rules when H-25..H-30 were added without updating the cap
- Commit `936d61c` raised the ceiling to 35 with no recorded justification beyond accommodating existing rules + 4 headroom slots
- PROJ-007 proposes H-32..H-35, which would consume 100% of remaining headroom (35/35)

**Validation:** Validated via C4 adversary tournament (0.95 composite score, 2 iterations)

---

## Context

### Background

PROJ-007 agent patterns orchestration produced rule files containing H-32 through H-35 (4 new HARD rules). Adding these would fully exhaust the 35-slot ceiling. Before committing to this, we investigated the provenance and validity of the 35-slot limit.

### Research Question

What is the evidence basis for the HARD rule ceiling of 35? Is it a principled engineering constraint or an arbitrary number?

### Investigation Approach

1. Traced the ceiling through git history to find its origin
2. Read the original EN-404 deliverable that established the first ceiling
3. Analyzed commit `936d61c` that changed 25 to 35
4. Cross-referenced with the enforcement architecture (ADR-EPIC002-002) token budgets
5. Conducted C4 adversary tournament to derive a principled upper boundary

---

## Finding

### Evidence Chain: Origin of 35

The ceiling evolved through three stages with decreasing rigor:

**Stage 1: Original Design (EN-404)**
- `deliverable-003-tiered-enforcement.md` established `<= 25` as the HARD rule ceiling
- Rationale was qualitative: "scarcity preserves signal" — no quantitative derivation
- This was the designer's pre-empirical judgment before any rules existed

**Stage 2: Silent Breach**
- H-25 through H-30 (skill standards) were added, bringing the count to 30
- The ceiling was NOT updated — the 25-slot limit was silently exceeded
- No governance review or exception mechanism was invoked

**Stage 3: Retroactive Accommodation (commit 936d61c)**
- Associated with H-31 (ambiguity clarification) addition
- Ceiling was updated from 25 to 35 in the same commit
- No ADR, no design rationale, no principled analysis recorded
- The new ceiling of 35 = existing count (31) + headroom (4)

### Principled Derivation (C4 Tournament Result)

A C4 adversary tournament derived the upper boundary from three independent constraint families:

| Constraint Family | Derived Ceiling |
|-------------------|-----------------|
| A: Token/Resource Budget | 25-40 (with consolidation) |
| B: Enforcement Coverage | 14 (engine L2) / 25+ (with compensating controls) |
| C: Instruction-Following Capacity | ~25 total with partitioning |

**Convergence point: 25 HARD rules** — robust within the 20-28 range under sensitivity analysis.

### Validation

C4 adversary tournament with all 10 strategies:
- Iteration 1: 0.90 (REVISE) — 54 findings, 7 CRITICAL
- Iteration 2: 0.95 (PASS) — all CRITICALs resolved

---

## Evidence

### Source Documentation

| Evidence ID | Type | Description | Source | Date |
|-------------|------|-------------|--------|------|
| E-001 | Git commit | Ceiling change 25→35 | `936d61c` | 2026-02-15 |
| E-002 | Deliverable | Original <= 25 ceiling | `EN-404/deliverable-003-tiered-enforcement.md` | 2026-01-15 |
| E-003 | Source code | L2 engine reads only quality-enforcement.md | `prompt_reinforcement_engine.py:243` | 2026-02-21 |
| E-004 | ADR | Token budgets: L1=12,476, L2=600 | `ADR-EPIC002-002` | Baselined |
| E-005 | Tournament | C4 derivation scoring 0.95 PASS | `hard-rule-budget-upper-boundary-derivation-r2.md` | 2026-02-21 |

---

## Implications

### Impact on Project

The unprincipled ceiling of 35 creates two risks:
1. **Over-constraining:** If the real limit is lower (25), adding rules beyond it degrades enforcement quality for ALL rules
2. **Under-constraining:** If blindly filled to 35, the framework loses enforcement effectiveness — every HARD rule competes for attention budget

### Design Decisions Affected

- **Decision:** Whether to install H-32..H-35 from PROJ-007
  - **Impact:** Cannot add 4 rules without first consolidating to create headroom within the principled ceiling
  - **Rationale:** Adding rules to an already-overfull budget degrades enforcement quality

### Risks Identified

| Risk | Severity | Mitigation |
|------|----------|------------|
| Current 31 rules already exceed derived ceiling of 25 | High | Consolidate H-25..H-30 (6→2) and H-07..H-09 (3→1) to reduce to 25 |
| Adding H-32..H-35 without consolidation degrades enforcement | High | Defer TASK-016 until consolidation complete |

---

## Relationships

### Creates

- [EN-002](../EN-002.md) - HARD Rule Budget Enforcement Improvement enabler
- [DEC-001](../DEC-001-hard-rule-budget-implementation-plan/DEC-001.md) - Implementation plan decisions

### Informs

- [TASK-016](../../EN-001-install-agent-pattern-deliverables/TASK-016-integrate-hard-rules/TASK-016.md) - H-32..H-35 integration (should be deferred)

### Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Parent | [EN-002](../EN-002.md) | Parent enabler |
| Evidence | `orchestration/.../adversary/hard-rule-budget/` | C4 tournament artifacts |
| Source | `quality-enforcement.md` | SSOT containing the ceiling |

---

## Recommendations

### Immediate Actions

1. Do NOT add H-32..H-35 until consolidation creates headroom
2. Replace the unprincipled 35-slot ceiling with the derived 25-slot ceiling

### Long-term Considerations

- Establish a formal governance process for ceiling changes (exception mechanism in derivation R2)
- Re-derive ceiling if architectural constraints change (e.g., L2 engine expansion, context window increase)

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-02-21 | Claude (PROJ-007 orchestrator) | Created discovery — validated via C4 tournament |

---

## Metadata

```yaml
id: "EN-002:DISC-001"
parent_id: "EN-002"
work_type: DISCOVERY
title: "HARD Rule Budget Ceiling Has No Principled Derivation"
status: VALIDATED
priority: HIGH
impact: HIGH
created_by: "Claude (PROJ-007 orchestrator)"
created_at: "2026-02-21T22:00:00Z"
updated_at: "2026-02-21T23:30:00Z"
completed_at: "2026-02-21T23:30:00Z"
tags: [governance, enforcement, hard-rules, quality-enforcement]
source: "C4 adversary tournament"
finding_type: GAP
confidence_level: HIGH
validated: true
```
