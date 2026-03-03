# Quality Score Report: NPT Pattern Reference (v1.1.0, Iteration 2)

## L0 Executive Summary
**Score:** 0.955/1.00 | **Verdict:** PASS | **Weakest Dimension:** Evidence Quality (0.90)
**One-line assessment:** The revised artifact addresses all 8 i1 findings with high fidelity and meets the C4 quality gate at 0.955; the sole remaining gap is that NPT-013's go-no-go citation could more explicitly flag the CONDITIONAL framing at point-of-use.

## Scoring Context
- **Deliverable:** `skills/prompt-engineering/rules/npt-pattern-reference.md` (v1.1.0)
- **Deliverable Type:** Research/Reference (operational rule file)
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Threshold:** 0.95 (C4 elevated threshold)
- **Prior Score:** 0.734 (i1, REVISE)
- **Iteration:** 2 (post-revision)
- **Scored:** 2026-03-01T00:00:00Z

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.955 |
| **Threshold** | 0.95 (C4 elevated, H-13) |
| **Verdict** | PASS |
| **Strategy Findings Incorporated** | No (i1 findings incorporated via revision, no separate adv-executor report for i2) |

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.96 | 0.192 | All 8 i1 gaps addressed; 7 sections cover all operational needs for pe-constraint-gen |
| Internal Consistency | 0.20 | 0.97 | 0.194 | NPT-013 dual definition handled; A3/A4 multi-type handled; no contradictions detected |
| Methodological Rigor | 0.20 | 0.96 | 0.192 | Taxonomy verification row, version pin, go-no-go path citation all present and correct |
| Evidence Quality | 0.15 | 0.90 | 0.135 | T4/T5 labels correct; CONDITIONAL GO status flagged; go-no-go citation present but NPT-013 effectiveness claim could be more cautiously framed at point-of-use |
| Actionability | 0.15 | 0.97 | 0.146 | Pattern Selection Guide, Upgrade Path, Format templates, XML Wrapping all directly usable |
| Traceability | 0.10 | 0.96 | 0.096 | Taxonomy version pinned; source file path cited; go-no-go path cited; ADR-001/ADR-002 referenced for operational adaptation |
| **TOTAL** | **1.00** | | **0.955** | |

## Detailed Dimension Analysis

### Completeness (0.96/1.00)

**Evidence:**
All 8 items from the i1 verification checklist are addressed:

1. All 7 A-type labels (A1–A7) now match source taxonomy v3.0.0 exactly. Reference line 151: "A1 Prohibition-only | A2 Structured prohibition | A3 Augmented prohibition | A4 Enforcement-tier prohibition | A5 Programmatic enforcement | A6 Training-time constraint | A7 Meta-prompting" — identical to source lines 142-148.
2. All 5 evidence tier labels (T1–T5 + T2 empty) match source. Reference line 153: "T1 Peer-reviewed | T2 (empty in this catalog...) | T3 Preprint / unreviewed | T4 Practitioner observation | T5 Session observation" — matches source lines 155-162.
3. NPT-013 operational adaptation divergence note: present and substantive (lines 67-68 of artifact). Names ADR-001, ADR-002, TASK-035, TASK-037, and 12 SKILL.md files.
4. Pattern Upgrade Path section: present (lines 133-144), with 3-row table covering NPT-014 → NPT-009 → NPT-013 progression and NPT-014 diagnostic note.
5. Taxonomy version pin and go-no-go source path: present in footer (lines 163-165): "Built against: taxonomy-pattern-catalog.md v3.0.0 (I3) | Go-no-go: ...go-no-go-determination.md".
6. Pattern-to-type assignment lines: present (lines 155-157). Include multi-type assignments consistent with source note.
7. Taxonomy labels verified row in quality criteria table: present (line 129): "Taxonomy labels verified | All A1-A7 and T1-T5 labels match source taxonomy SSOT | 'A5 Scope Limitation' (label does not match source)".
8. Go-no-go source path citation: present (line 69) in NPT-013 key research finding.

**Gaps:**
Minor: The T5 row in the reference's evidence tier list says "T5 Session observation" which matches the source. However, the T2 handling in the taxonomy note says T2 is "empty in this catalog — see taxonomy T2 tier note." The source text says "T2 (established practitioner — published vendor documentation from major AI providers)" in its T2 note. The reference's inline T2 label shows only "(empty in this catalog — see taxonomy T2 tier note)" which is accurate shorthand but does not include the source's full T2 label text. This is a very minor gap — the T2 description is in the source taxonomy, and the reference correctly marks it as empty and defers.

**Improvement Path:**
Optionally expand T2 label inline to "T2 (established practitioner — empty in this catalog)" for full label fidelity. Not required for PASS.

---

### Internal Consistency (0.97/1.00)

**Evidence:**
- NPT-013 is simultaneously defined as "Constitutional Triplet" (source taxonomy structural definition) and as an operational NEVER+consequence+Instead format. The artifact resolves this potential contradiction explicitly in the operational adaptation note (lines 67-68): "The source taxonomy defines NPT-013 as 'Constitutional Triplet: a mandatory set of minimum three prohibitions'... This reference uses 'NPT-013' as an operational shorthand for the FORMAT..." No contradiction between the two usages — the distinction is made clear.
- A3 assignment includes NPT-010 (line 155: "A3: NPT-008, NPT-010, NPT-011, NPT-012"). Source Dimension A table shows A3: NPT-008, NPT-011, NPT-012 — but the multi-type note (source line 150) explicitly adds NPT-010 to A3: "NPT-010 appears in both A3 (Augmented prohibition — positive pairing) and A4." Reference is consistent with the note, not a contradiction.
- NPT-009 evidence shown as T4 (line 36: "Evidence: T4 observational") and confirmed in classification reference (line 157). Consistent throughout.
- NPT-013 shown as T4 (line 65: "Evidence: T4 observational") with note "T5 (partial)". Classification reference line 157 confirms: "T4: NPT-009, NPT-010, NPT-011, NPT-012, NPT-013 | T5: NPT-013 (partial)". Consistent.
- CONDITIONAL GO status is stated in line 66 and again in taxonomy classification reference line 159: "Both are adopted on convention-alignment grounds (PG-003). Causal superiority over positive-only framing is UNTESTED." Consistent framing throughout.

**Gaps:**
NPT-013's key research finding states "NPT-013 achieves 100% compliance vs 92.2% for positive-only framing (p=0.016)" (line 69), while line 159 states "Causal superiority over positive-only framing is UNTESTED." This apparent tension is resolvable: the p=0.016 finding is the A/B test result, while "UNTESTED" refers to causal mechanism (not correlation). However, the juxtaposition without an explicit bridge could create confusion for a practitioner reading lines 66-69 in isolation. The artifact handles this imperfectly but within acceptable bounds.

**Improvement Path:**
Add a one-line bridge after the key research finding: "Note: this observational correlation does not establish causal superiority — see CONDITIONAL GO status above."

---

### Methodological Rigor (0.96/1.00)

**Evidence:**
- Taxonomy version pin: "Built against: taxonomy-pattern-catalog.md v3.0.0 (I3)" (footer, line 164). This enables reproducible verification — any scorer can open the v3.0.0 taxonomy and confirm label fidelity.
- Source taxonomy path cited: consistent reference to `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/phase-3/taxonomy-pattern-catalog.md` (lines 4, 149).
- Go-no-go source path cited for the NPT-013 effectiveness claim (line 69): full path to `go-no-go-determination.md`.
- Taxonomy labels verified checklist row (line 129): provides the exact failure mode example ("'A5 Scope Limitation' (label does not match source)"), making the verification criterion testable.
- Document sections navigation table (lines 6-17) covers all 7 sections, satisfying H-23.
- Self-review checklist (Constraint Quality Criteria) is directly applicable to the artifact's purpose — pe-constraint-gen can use it operationally.
- Pattern assignments (lines 155-157) provide explicit traceability from pattern IDs to taxonomy dimensions.

**Gaps:**
The methodology for how NPT-013 "operational adaptation" was decided is traced to ADR-001 and ADR-002 by name, but the ADR paths are not given. A practitioner wanting to verify the adaptation rationale must know where to find ADR-001/ADR-002. This is a minor gap given that the ADRs are project-standard and pe-constraint-gen is the expected consumer.

**Improvement Path:**
Add repository paths for ADR-001 and ADR-002 in the operational adaptation note, or note that they are under `projects/PROJ-014-negative-prompting-research/work/`.

---

### Evidence Quality (0.90/1.00)

**Evidence:**
- NPT-009: T4 evidence declared with specific count: "33 production instances, VS-001 through VS-004" (line 36). VS-001 through VS-004 are source-traceable session observation studies.
- NPT-013: T4 evidence declared with schema-mandatory rationale: "schema-mandatory, VS-004" (line 65). T5 partial acknowledged.
- CONDITIONAL GO status explicitly stated for NPT-013 (line 66): "ACTIVE — CONDITIONAL GO via PG-003 (convention-alignment rationale, not effectiveness-determined)." This is appropriately cautious framing.
- The key research finding cites a statistical result (p=0.016) with a specific go-no-go path. This enables evidence verification.
- Taxonomy classification reference (lines 159): "Causal superiority over positive-only framing is UNTESTED." Epistemically honest.
- T2 tier handling: correctly notes T2 is empty in this catalog with explanation.

**Gaps:**
The key research finding statement — "NPT-013 achieves 100% compliance vs 92.2% for positive-only framing (p=0.016)" — is stated in the NPT-013 section without a qualifier directing the reader to evaluate it in context of the CONDITIONAL GO status. A practitioner unfamiliar with PG-003 could read this finding as stronger evidence than it is. The CONDITIONAL GO note and the key research finding appear on consecutive lines (66-69), so the ordering provides some protection, but the finding sentence itself has no inline qualifier like "(observational, not causal)." This is the primary evidence quality gap.

Additionally, "T4 observational (schema-mandatory, VS-004)" for NPT-013 is slightly imprecise: schema-mandatory is an enforcement mechanism, not an observational data point. The T4 evidence derives from VS-004 production observation; the schema-mandatory clause is a separate governance fact. These are merged in the evidence line.

**Improvement Path:**
1. Append "(observational; PG-003 CONDITIONAL GO applies)" to the key research finding sentence.
2. Split NPT-013 evidence line to: "T4 observational (VS-004 production observation); schema-mandatory per H-35."

---

### Actionability (0.97/1.00)

**Evidence:**
- Pattern Selection Guide (lines 21-31): 5-row decision table covering all primary pe-constraint-gen use contexts. Decision rule stated explicitly: "Constitutional principle reference + governance YAML -> NPT-009. Behavioral pattern with a constructive alternative -> NPT-013. When both apply, generate both."
- NPT-009 format template (lines 41-43): complete with action variable and impact variable, both with specificity criteria.
- NPT-013 format template (lines 75-77): complete with NEVER + consequence + Instead variables, with specificity criterion for Instead clause.
- XML Wrapping Reference (lines 96-114): concrete XML examples for all three deployment contexts (YAML, markdown guardrails, standalone XML block).
- Constraint Quality Criteria (lines 118-130): 6-row self-review checklist with pass criteria and fail examples. Directly usable by pe-constraint-gen as a generation validation step.
- Pattern Upgrade Path (lines 133-144): clear upgrade decision table with NPT-014 diagnostic criteria.
- Examples section for both patterns (NPT-009 lines 47-59, NPT-013 lines 83-92): production-ready examples covering the primary use cases.

**Gaps:**
The Taxonomy Classification Reference section (lines 147-159) is informational rather than actionable. It documents where patterns sit in the taxonomy but does not guide pe-constraint-gen to take any action based on the classification. This is by design — it is labeled "Reference" — but the section could include one actionable note: "When reporting generated constraints, include the pattern's technique type and evidence tier for traceability." This is a very minor gap.

**Improvement Path:**
Add a one-line usage note to the Taxonomy Classification Reference: "Include type and tier labels in generated constraint documentation for source traceability."

---

### Traceability (0.96/1.00)

**Evidence:**
- Source taxonomy path: cited in document header (line 4) and in Taxonomy Classification Reference section (line 149).
- Taxonomy version: pinned in footer (line 164): "taxonomy-pattern-catalog.md v3.0.0 (I3)".
- Go-no-go determination path: cited in NPT-013 key research finding (line 69) and in footer (line 164-165).
- ADR references: ADR-001 and ADR-002 named in operational adaptation note (line 67) as the decision authority for the NPT-013 adaptation.
- Session observation references: VS-001 through VS-004 cited in NPT-009 evidence (line 36) and VS-004 cited in NPT-013 evidence (line 65).
- Project and task traceability: TASK-025 cited in footer (line 163), TASK-035 and TASK-037 named in operational adaptation note (line 67).
- SSOT for pe-constraint-gen: stated in footer (line 165): "SSOT for pe-constraint-gen — see skills/prompt-engineering/agents/pe-constraint-gen.md".
- H-35 constitutional reference: cited in operational adaptation note (line 67): "The source taxonomy's structural definition (minimum 3 prohibitions per agent) remains enforced by H-35."

**Gaps:**
ADR-001 and ADR-002 are named without file paths. A new practitioner cannot locate them without prior knowledge of the project structure. The pattern assignment lines (lines 155-157) correctly replicate the source data but do not cite specific source line numbers for independent verification (though the section header does cite the full source file path at line 149).

**Improvement Path:**
Add ADR paths: "ADR-001 (`projects/PROJ-014-negative-prompting-research/work/.../ADR-001.md`)". Optionally add source taxonomy line ranges for the dimension tables.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Evidence Quality | 0.90 | 0.93 | Append "(observational; PG-003 CONDITIONAL GO applies)" to the NPT-013 key research finding sentence (line 69) to prevent practitioner misreading of statistical result as causal claim |
| 2 | Internal Consistency | 0.97 | 0.98 | Add one-line bridge after NPT-013 key research finding: "Note: this observational correlation does not establish causal superiority — see CONDITIONAL GO status above" |
| 3 | Traceability | 0.96 | 0.98 | Add file paths for ADR-001 and ADR-002 in the operational adaptation note |
| 4 | Methodological Rigor | 0.96 | 0.97 | Add repository paths for ADR-001/ADR-002 or a canonical location note |
| 5 | Completeness | 0.96 | 0.97 | Expand T2 label inline: "T2 (established practitioner — empty in this catalog)" for full label fidelity |

All recommendations are optional polish. The artifact passes the 0.95 C4 threshold at 0.955 and all 8 i1 verification items are confirmed addressed.

---

## Leniency Bias Check
- [x] Each dimension scored independently before computing composite
- [x] Evidence documented for each score (specific lines cited)
- [x] Uncertain scores resolved downward (Evidence Quality: uncertain between 0.90-0.92; resolved to 0.90)
- [x] First-draft calibration not applicable — this is a second-iteration revised artifact
- [x] No dimension scored above 0.97 without specific evidence for each claim
- [x] Composite math verified: (0.96×0.20) + (0.97×0.20) + (0.96×0.20) + (0.90×0.15) + (0.97×0.15) + (0.96×0.10) = 0.192 + 0.194 + 0.192 + 0.135 + 0.146 + 0.096 = 0.955

## Session Context Handoff

```yaml
verdict: PASS
composite_score: 0.955
threshold: 0.95
weakest_dimension: evidence_quality
weakest_score: 0.90
critical_findings_count: 0
iteration: 2
improvement_recommendations:
  - "Append CONDITIONAL GO qualifier to NPT-013 key research finding (Evidence Quality)"
  - "Add bridge note clarifying observational vs causal distinction (Internal Consistency)"
  - "Add file paths for ADR-001 and ADR-002 in operational adaptation note (Traceability)"
```
