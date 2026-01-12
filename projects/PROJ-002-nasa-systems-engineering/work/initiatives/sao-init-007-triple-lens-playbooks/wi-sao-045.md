---
id: wi-sao-045
title: "Verify nse-* Generator-Critic applicability"
status: COMPLETE
parent: "_index.md"
initiative: sao-init-007
children: []
depends_on:
  - wi-sao-042
blocks: []
created: "2026-01-12"
last_updated: "2026-01-12"
priority: P1
estimated_effort: "3h"
entry_id: sao-045
token_estimate: 500
---

# WI-SAO-045: Verify nse-* Generator-Critic Applicability

> **Status:** ✅ COMPLETE
> **Priority:** P1 (HIGH)
> **Depends On:** WI-SAO-042 (Generator-Critic research)
> **Decision:** NO - Use Review-Revise Pattern (RFA/RID cycles) instead

---

## Description

The Generator-Critic pattern (Pattern 8) is documented for ps-* agents with ps-critic. This work item investigates whether the same pattern applies to nse-* (NASA Systems Engineering) agents and how it should be adapted.

**Key Question:** Should nasa-se workflows use a critic pattern, and if so, how?

## Research Finding (2026-01-12)

**Decision: NO - Generator-Critic pattern NOT directly applicable to nse-* agents.**

### Analysis Summary

| Aspect | ps-critic | nse-qa | nse-reviewer |
|--------|-----------|--------|--------------|
| **Pattern** | Score-based iteration | One-shot validation | Gate-based with RFAs |
| **Output** | Score 0.0-1.0 + feedback | COMPLIANT/ISSUES/REJECTED | Ready/Not Ready + RFAs |
| **Iteration** | ✅ Yes (circuit breaker) | ❌ No | ⚠️ Via RID resolution |
| **Cognitive Mode** | Convergent | Convergent | Convergent |
| **Purpose** | Quality improvement | Standards compliance | Review readiness |

### Key Insight

NASA SE workflows are **gate-based** rather than score-based:
- Life cycle reviews: MCR → SRR → PDR → CDR → FRR
- Each gate has entrance/exit criteria (pass/fail)
- Iteration happens via **RFA (Request for Action) / RID resolution** cycle

### The Review-Revise Pattern (NSE Equivalent)

```
NASA SE Review-Revise Cycle:
----------------------------

1. nse-* agent produces artifact
2. nse-reviewer evaluates entrance criteria
3. IF criteria not met → RFAs generated
4. Team addresses RFAs (revision)
5. Delta review or re-assessment
6. Repeat until gate passed

This is NOT Generator-Critic (no scores, no circuit breaker),
but achieves iterative improvement via formal review process.
```

### Comparison

| Feature | Generator-Critic (ps-*) | Review-Revise (nse-*) |
|---------|------------------------|----------------------|
| Quality measure | Score 0.0-1.0 | Entrance criteria (pass/fail) |
| Acceptance threshold | score >= 0.85 | All criteria GREEN |
| Circuit breaker | max 3 iterations | Until gate passed |
| Feedback format | Score + recommendations | RFAs/RIDs |
| Orchestration | MAIN CONTEXT loops | Review board process |

### Recommendation

1. **Do NOT add nse-critic agent** - nse-qa and nse-reviewer cover quality feedback
2. **Document Review-Revise pattern** as NSE alternative to Generator-Critic
3. **Cross-reference** between playbooks for users who work both domains

---

## Acceptance Criteria

1. [x] Research complete: Generator-Critic applicability to NASA SE
2. [x] Decision documented: NO - Use Review-Revise Pattern instead
3. [N/A] nse-* critic workflow - Not applicable (use nse-reviewer RFAs)
4. [N/A] nasa-se PLAYBOOK.md update - No new pattern needed
5. [x] Alternative documented: Review-Revise Pattern (gate-based iteration)

---

## Tasks

### T-045.1: Research Phase
- [x] **T-045.1.1:** Review nse-qa agent (Result: one-shot validation, not iterative)
- [x] **T-045.1.2:** Review nse-reviewer agent (Result: gate-based with RFA cycles)
- [x] **T-045.1.3:** Research NASA SE quality gates (MCR→SRR→PDR→CDR→FRR)
- [x] **T-045.1.4:** Identified RFA/RID resolution as iterative mechanism

### T-045.2: Analysis Phase
- [x] **T-045.2.1:** Compare ps-critic vs nse-qa vs nse-reviewer (table above)
- [x] **T-045.2.2:** Identified: Review-Revise pattern via nse-reviewer RFAs
- [x] **T-045.2.3:** Documented: Gate-based vs score-based distinction
- [x] **T-045.2.4:** Decision: NO - Don't add nse-critic, use Review-Revise

### T-045.3: Documentation Phase
- [x] **T-045.3.1:** Document findings in this work item
- [N/A] **T-045.3.2:** nasa-se PLAYBOOK.md update not needed
- [N/A] **T-045.3.3:** ORCHESTRATION_PATTERNS.md - NSE uses existing patterns
- [N/A] **T-045.3.4:** Cross-references - playbooks already distinct

---

## Verification

| Evidence ID | Type | Description | Status |
|-------------|------|-------------|--------|
| E-045-001 | Research | nse-qa and nse-reviewer analyzed | ✅ Complete |
| E-045-002 | Decision | NO - Use Review-Revise Pattern | ✅ Complete |
| E-045-003 | Content | Playbook update N/A (no changes needed) | ✅ Complete |

---

## Research Questions

1. **Does NASA SE have iterative review patterns?**
   - Technical reviews (SRR, PDR, CDR) are sequential, not iterative
   - But RID (Review Item Discrepancy) resolution IS iterative

2. **What is nse-qa's role?**
   - Quality assurance for artifacts
   - Is this critique or verification?

3. **What is nse-reviewer's role?**
   - Technical review preparation
   - Entrance/exit criteria checking
   - RFA (Request for Action) generation

4. **Is there a gap?**
   - ps-critic provides iterative improvement feedback
   - nse-qa validates against standards
   - nse-reviewer checks review readiness
   - None explicitly does "iterative improvement" like ps-critic

---

## Hypothesis

**Initial Hypothesis:** NASA SE workflows are more sequential and gate-based than iterative. The "critic" equivalent is the formal review process (TIM, SRR, PDR, CDR) rather than a feedback loop.

**However:** Requirements refinement and risk mitigation ARE iterative processes that could benefit from a critic-like pattern.

**Potential Adaptation:**
- Use nse-qa for standards compliance checking (one-shot)
- Use nse-reviewer → generator feedback loop for requirements refinement
- Document as "Review-Revise Pattern" rather than "Generator-Critic"

---

## Agent Comparison Matrix

| Capability | ps-critic | nse-qa | nse-reviewer |
|------------|-----------|--------|--------------|
| Iterative feedback | ✅ | ❌ | ⚠️ (RID loop) |
| Quality scoring | ✅ | ✅ | ❌ |
| Improvement suggestions | ✅ | ⚠️ | ✅ (RFAs) |
| Circuit breakers | ✅ | ❌ | ❌ |
| Standards compliance | ❌ | ✅ | ✅ |
| Review gate checking | ❌ | ❌ | ✅ |

---

## Context: Existing nse-* Agents

| Agent | Role | Critique-like? |
|-------|------|----------------|
| nse-requirements | Requirements definition | No |
| nse-verification | V&V specialist | No (verifies, doesn't iterate) |
| nse-reviewer | Review preparation | Partial (RFAs are iterative) |
| nse-reporter | Status reporting | No |
| nse-risk | Risk assessment | No |
| nse-architecture | Technical design | No |
| nse-integration | Interface management | No |
| nse-configuration | CM specialist | No |
| nse-qa | Quality assurance | Partial (quality checks) |
| nse-explorer | Concept exploration | No (divergent, not critical) |

---

*Source: DISCOVERY-012 (GAP-012-005)*
*Created: 2026-01-12*
