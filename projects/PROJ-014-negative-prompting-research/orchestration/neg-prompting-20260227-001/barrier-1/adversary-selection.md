# Strategy Selection Plan — Barrier 1 Synthesis

> Criticality: C4 (Critical) | Deliverable: Barrier 1 Cross-Pollination Synthesis | Date: 2026-02-27

---

## Criticality Assessment

**Requested Level:** C4 (Critical)

**Auto-Escalation Applied:** No

**Auto-Escalation Checks:**
- AE-001 (touches JERRY_CONSTITUTION.md): No
- AE-002 (touches .context/rules/ or .claude/rules/): No
- AE-003 (new or modified ADR): No
- AE-004 (modifies baselined ADR): No
- AE-005 (security-relevant code): No
- AE-006 (token exhaustion): No

**Final Level:** C4 (Critical)

**Justification:** Barrier 1 synthesis represents irreversible research synthesis that directly informs PROJ-014 framework decisions and cross-framework research direction. Classification as C4 is appropriate due to: (1) irreversible nature — once published, findings cascade to downstream research phases; (2) governance impact — conclusions influence framework-wide negative prompting strategy decisions; (3) public/external visibility — synthesis outputs inform research community; (4) architectural scope — findings affect multiple research pillars and cross-project patterns.

---

## Selected Strategies (Ordered per H-16)

| Order | Strategy ID | Strategy Name | Template Path | Required/Optional | Rationale |
|-------|-------------|---------------|---------------|-------------------|-----------|
| 1 | S-010 | Self-Refine | `.context/templates/adversarial/s-010-self-refine.md` | Required (C4) | Initial self-review: author reviews synthesis for completeness, internal consistency, methodological rigor |
| 2 | S-003 | Steelman Technique | `.context/templates/adversarial/s-003-steelman.md` | Required (C4) | Strengthen findings: identify strongest counterarguments and alternative interpretations before critique |
| 3 | S-002 | Devil's Advocate | `.context/templates/adversarial/s-002-devils-advocate.md` | Required (C4) | Challenge assumptions: attack core claims, identify unstated premises, expose methodological limitations |
| 4 | S-004 | Pre-Mortem Analysis | `.context/templates/adversarial/s-004-pre-mortem.md` | Required (C4) | Failure projection: imagine synthesis has failed at adoption; work backward to identify failure modes |
| 5 | S-001 | Red Team Analysis | `.context/templates/adversarial/s-001-red-team.md` | Required (C4) | Adversarial attack: probe synthesis for exploitable gaps, misinterpretations, vulnerable claims |
| 6 | S-007 | Constitutional AI Critique | `.context/templates/adversarial/s-007-constitutional-ai.md` | Required (C4) | Governance alignment: verify synthesis conforms to Jerry framework principles (P-003, P-020, P-022) |
| 7 | S-011 | Chain-of-Verification | `.context/templates/adversarial/s-011-cove.md` | Required (C4) | Claim verification: trace each major finding to source survey and evidence tier; verify citation chain |
| 8 | S-012 | FMEA | `.context/templates/adversarial/s-012-fmea.md` | Required (C4) | Failure modes analysis: systematic identification of RPN-ordered risks in synthesis (evidence gaps, conflicts, unsourced claims) |
| 9 | S-013 | Inversion Technique | `.context/templates/adversarial/s-013-inversion.md` | Required (C4) | Assume opposite: what if negative prompting has NO impact? What if all findings are artifacts? |
| 10 | S-014 | LLM-as-Judge | `.context/templates/adversarial/s-014-llm-as-judge.md` | Required (C4) | Quality scoring: final quantitative assessment against 6-dimension rubric (Completeness, Consistency, Rigor, Evidence, Actionability, Traceability) |

---

## H-16 Compliance Check

**H-16 Constraint:** Steelman Technique (S-003) MUST be ordered BEFORE Devil's Advocate (S-002).

**Verification:**
- S-003 position: **Order 2**
- S-002 position: **Order 3**
- Constraint satisfied: **YES** — S-003 (position 2) precedes S-002 (position 3)

---

## Execution Sequence Rationale

### Group A — Self-Review (Order 1)
**S-010: Self-Refine**
- Prerequisite for all downstream critique
- Author identifies obvious gaps and inconsistencies before external review
- Reduces reviewer burden and prevents basic defects from consuming tournament cycles

### Group B — Strengthen (Order 2)
**S-003: Steelman Technique**
- Precedes Group C per H-16 (Steelman before Devil's Advocate)
- Identifies strongest counterarguments and alternative explanations
- Prevents premature rejection of sound findings due to presentation weakness

### Group C — Challenge (Orders 3–5)
**S-002: Devil's Advocate, S-004: Pre-Mortem, S-001: Red Team**
- Systematic attack from multiple vectors
- S-002: Logical/assumptional critique
- S-004: Failure mode projection
- S-001: Comprehensive adversarial probing
- Collectively expose vulnerabilities that self-review and steelman cannot detect

### Group D — Verify (Orders 6–7)
**S-007: Constitutional AI, S-011: Chain-of-Verification**
- S-007: Ensures synthesis respects framework governance constraints
- S-011: Traces findings to evidence sources; validates citation integrity and evidence tier assignments
- Prevents governance bypass and unsourced claims

### Group E — Decompose (Orders 8–9)
**S-012: FMEA, S-013: Inversion**
- S-012: Systematic risk quantification; identifies high-RPN failure modes requiring remediation
- S-013: Validates reasoning by inverting assumptions; tests robustness under inversion
- Uncovers second-order risks and assumption dependencies

### Group F — Score (Order 10)
**S-014: LLM-as-Judge**
- Always last per ordering rules
- Final quantitative gate: quality_score >= 0.95 (C4 threshold)
- Six-dimension rubric provides objective progress tracking across revision iterations
- Below 0.95: deliverable rejected; revision required per H-13

---

## Quality Gate Configuration

**Threshold:** >= 0.95 (C4 deliverable)

**Scoring Rubric (S-014):**

| Dimension | Weight | Scoring Criteria |
|-----------|--------|------------------|
| **Completeness** | 20% | All three input surveys integrated; no known gaps in source catalog; cross-survey agreements documented; conflicts and gaps explicitly identified |
| **Internal Consistency** | 20% | No contradictions within synthesis; claims support each other; methodology section clearly maps findings back to Braun & Clarke phases; evidence tiers consistent |
| **Methodological Rigor** | 20% | Thematic analysis methodology correctly applied; 6-phase process documented; bias mitigation strategies visible (cross-coder agreement simulation, audit trail); deduplication process transparent |
| **Evidence Quality** | 15% | Evidence tier assignments justified; unsourced claims audited; single-survey claims flagged with caveat language; high-tier evidence predominates in major findings |
| **Actionability** | 15% | Findings translate to concrete implications for PROJ-014 research phases; recommendations on framework adaptation clear; "so what" answered for each major theme |
| **Traceability** | 10% | Each finding traceable to source survey(s) and specific evidence entries; citation chain unbroken; deduplication log verifiable; source attribution transparent |

**Revision Cycle Bounds:**
- Minimum: 3 iterations (H-14)
- Maximum: 10 iterations (C4 ceiling per RT-M-010)
- Plateau detection: delta < 0.01 for 3 consecutive iterations → early halt

---

## Strategy Overrides Applied

**None.** All 10 required C4 strategies are included per criticality-to-strategy mapping.

---

## Self-Review Checklist (H-15)

Before executing the tournament, verify:

- [ ] All 10 selected strategies are valid (S-001 through S-014)
- [ ] H-16 ordering satisfied (S-003 at position 2, S-002 at position 3)
- [ ] Auto-escalation rules checked; no false escalations
- [ ] All template paths resolve to existing files
- [ ] Quality threshold (>= 0.95) set correctly for C4
- [ ] Execution sequence organized in 6 logical groups per ordering rules
- [ ] Tournament scope clearly defined: synthesis.md is the target deliverable

**All checks: PASS**

---

## Execution Instructions

**Tournament Scope:** `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/barrier-1/synthesis.md`

**Output Artifact:** Revised synthesis.md reflecting all 10 strategies' findings and revisions across minimum 3 iterations.

**Quality Gate:** S-014 (LLM-as-Judge) final score must be >= 0.95. Below threshold: revision required per H-13.

**Deliverable Path:**
- Input: `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/barrier-1/synthesis.md`
- Output: Same file (in-place revision)

**Handoff Protocol:** Upon completion, produce:
1. Final S-014 quality score and dimension breakdown
2. Tournament summary: all 10 strategies' key findings (3-5 bullets each)
3. Revision history: iterations attempted, score deltas, convergence behavior
4. Blockers/escalations: any findings requiring governance review or cross-project coordination

---

*Strategy Selection Plan Version: 1.0*
*Agent: adv-selector*
*Model: Haiku 4.5*
*Validation: H-15 self-review PASS*
*Date: 2026-02-27*
