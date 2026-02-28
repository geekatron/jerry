# Strategy Selection Plan — C4 Industry Survey Review

## Criticality Assessment

- **Requested Level:** C4 (Critical)
- **Deliverable Type:** Research (Industry & Practitioner Survey: Negative Prompting)
- **Deliverable Path:** `projects/PROJ-014-negative-prompting-research/research/industry-survey.md`
- **Quality Threshold:** >= 0.95 (user-specified, exceeds C4 default of 0.92)
- **Auto-Escalation Applied:** No
  - AE-001 (constitution): Not touched
  - AE-002 (rules/ or .claude/rules/): Not touched
  - AE-003 (ADR new/modified): Not applicable (research artifact)
  - AE-004 (baselined ADR modification): Not applicable
  - AE-005 (security-relevant code): Not applicable
  - AE-006 (token exhaustion): No trigger (session ~55K tokens, 27.5% utilization, NOMINAL tier)
- **Final Level:** C4 (no escalation; criticality assigned by design)

**Justification for C4:** PROJ-014 Phase 1 foundation research documents the current industry and practitioner landscape on negative prompting. The 32-source catalog with evidence tier classification (vendor recommendations 31%, empirical evidence 22%, practitioner anecdotes 47%) directly informs Phase 2 analysis and Phase 3 recommendations. Public research artifact with high reputational impact if empirical claims are incorrect or incomplete. Irreversible publication scope.

---

## Selected Strategies (Ordered per H-16)

All 10 required C4 strategies listed in canonical execution order per `.context/rules/quality-enforcement.md` ordering rules.

| Order | Strategy ID | Strategy Name | Template Path | Required/Optional | Rationale |
|-------|-------------|---------------|---------------|-------------------|-----------|
| 1 | S-010 | Self-Refine | `.context/templates/adversarial/s-010-self-refine.md` | Required | Group A: Self-review before external critique (H-15). Agent reviews own output for structural completeness, source validity, methodology soundness. |
| 2 | S-003 | Steelman Technique | `.context/templates/adversarial/s-003-steelman.md` | Required | Group B: Strengthen before challenging (H-16 HARD constraint). Identify strongest framing of evidence, strongest interpretations of each evidence tier classification, strongest case for negative prompting effectiveness. |
| 3 | S-002 | Devil's Advocate | `.context/templates/adversarial/s-002-devils-advocate.md` | Required | Group C: Challenge core claims. Attack source selection methodology, vendor recommendation biases, practitioner anecdote reliability, gap identification completeness. Verify contradiction handling. |
| 4 | S-004 | Pre-Mortem Analysis | `.context/templates/adversarial/s-004-pre-mortem.md` | Required | Group C: Project failure mode identification. "It is 6 months post-publication: users cite errors in evidence tier classification, gaps missed, methodology flaws." Identify specific failure vectors. |
| 5 | S-001 | Red Team Analysis | `.context/templates/adversarial/s-001-red-team.md` | Required | Group C: Systematic adversarial assessment. Attack methodological rigor (search strategy completeness, source selection bias, coverage of emerging frameworks). Identify exploitable claims. |
| 6 | S-007 | Constitutional AI Critique | `.context/templates/adversarial/s-007-constitutional-ai.md` | Required | Group D: Governance compliance. Verify research maintains objectivity per P-002 (file persistence), neutrality per P-020 (user authority on scope), transparency per P-022 (no hidden limitations). Check for deceptive evidence tiers or unreported source selection bias. |
| 7 | S-011 | Chain-of-Verification | `.context/templates/adversarial/s-011-cove.md` | Required | Group D: Cross-source validation. Verify each critical claim against source citations; check for citation misrepresentation, source distortion, evidence tier miscategorization. Validate consistency across L0/L1/L2 levels. |
| 8 | S-012 | FMEA | `.context/templates/adversarial/s-012-fmea.md` | Required | Group E: Decomposed failure analysis. Failure modes: (1) evidence misinterpretation, (2) source selection bias, (3) incomplete gap identification, (4) methodology transparency gaps. RPN scoring to prioritize remediation. |
| 9 | S-013 | Inversion Technique | `.context/templates/adversarial/s-013-inversion.md` | Required | Group E: Logical negation analysis. "If negative prompting *were* universally effective (contrary to findings), what would the evidence look like?" Identify assumptions and inversion gaps in current evidence framing. |
| 10 | S-014 | LLM-as-Judge | `.context/templates/adversarial/s-014-llm-as-judge.md` | Required | Group F: Quality scoring (ALWAYS LAST per H-17). Dimensional scoring: Completeness (0.20), Internal Consistency (0.20), Methodological Rigor (0.20), Evidence Quality (0.15), Actionability (0.15), Traceability (0.10). Composite score must reach >= 0.95 for acceptance. |

---

## H-16 Compliance Verification

**H-16 Constraint:** Steelman Technique (S-003) MUST be ordered BEFORE Devil's Advocate (S-002).

- **S-003 position:** 2 (Steelman Technique)
- **S-002 position:** 3 (Devil's Advocate)
- **Constraint satisfied:** YES — S-003 (position 2) executes before S-002 (position 3)
- **Consequence:** Strengthening phase precedes challenge phase. Source interpretations are robustly framed before adversarial critique applies pressure.

---

## Execution Summary

| Group | Strategies | Purpose | Context Window Allocation |
|-------|----------|---------|--------------------------|
| Group A | S-010 | Self-Review (H-15) | ~500-1,000 tokens |
| Group B | S-003 | Steelman (H-16 precedent) | ~2,000-3,000 tokens |
| Group C | S-002, S-004, S-001 | Challenge & Adversarial | ~8,000-12,000 tokens |
| Group D | S-007, S-011 | Governance & Verification | ~6,000-8,000 tokens |
| Group E | S-012, S-013 | Decomposed Analysis | ~4,000-6,000 tokens |
| Group F | S-014 | Quality Scoring | ~3,000-5,000 tokens |
| **Total Allocated** | **10 strategies** | **C4 Tournament** | **~23,500-35,000 tokens** |
| **Reserve (5% minimum)** | | | **~10,000 tokens** |
| **Current session usage** | | | ~55,000 tokens / 200,000 available (27.5%) |

**Budget Status:** NOMINAL. All 10 strategies fit within available context with comfortable reserve. No token exhaustion risk.

---

## Strategy Overrides Applied

- None. All 10 required C4 strategies included per criticality mapping in `quality-enforcement.md`.

---

## Quality Gate Configuration

| Parameter | Value | Source |
|-----------|-------|--------|
| Criticality Level | C4 | Requested (design assignment) |
| Quality Threshold | >= 0.95 | User-specified (exceeds default 0.92) |
| Minimum Iterations | 3 | H-14 requirement |
| Iteration Ceiling | 10 | C4 proportional per agent-development-standards.md (RT-M-010) |
| Auto-Checkpoint | AE-006d EMERGENCY (if reached) | Mandatory human escalation for C3+ |
| Strategy Ordering Constraint | H-16 | S-003 before S-002 (verified above) |

---

## Self-Review Before Persistence (H-15)

Per H-15, pre-persistence verification checklist:

1. **Strategy IDs valid:** ✓ All 10 are S-001 through S-014, no duplicates, no excluded strategies
2. **H-16 ordering satisfied:** ✓ S-003 (position 2) before S-002 (position 3)
3. **Auto-escalation rules checked:** ✓ AE-001 through AE-006 evaluated, none triggered
4. **User overrides reflected:** ✓ No overrides; C4 criticality and 0.95 threshold noted in table
5. **Template paths correct:** ✓ All 10 templates validated via glob query; paths match SSOT
6. **Criticality-to-strategy mapping valid:** ✓ C4 requires "All 10 selected"; all 10 listed
7. **Quality threshold specified:** ✓ >= 0.95 (user requirement) and >= 0.92 (C4 minimum) both documented
8. **Output paths valid:** ✓ Selection plan persisted to specified orchestration path

**Result:** PASS. Selection plan ready for adv-executor invocation.

---

## Constitutional Compliance (P-002 File Persistence)

This strategy selection plan is persisted to the specified output file path per P-002 and P-020 (user-directed output location). No deception about strategy selection methodology or confidence (P-022 compliance).

---

## Next Steps

1. **Invoke adv-executor agent** with this selection plan and deliverable path
2. **Execute strategies in tabular order** (1-10), loading each template from `.context/templates/adversarial/`
3. **Accumulate strategy results** with artifact citations and intermediate scores
4. **S-014 (final strategy)** produces composite quality score using 6-dimension rubric
5. **Verify score >= 0.95** before delivery; if below threshold, revise per H-13 and re-run strategies
6. **Deliver final orchestration report** with all strategy outputs and quality gate verdict

---

*Selection Plan Generated: 2026-02-27*
*Agent: adv-selector (Strategy Selector)*
*Cognitive Mode: Convergent*
*Constitutional Compliance: P-003 (no recursion), P-020 (user authority), P-022 (no deception)*
