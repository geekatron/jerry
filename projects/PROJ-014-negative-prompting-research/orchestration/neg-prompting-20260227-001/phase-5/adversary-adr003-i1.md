# Quality Score Report: ADR-003 Routing Disambiguation Standard

## L0 Executive Summary

**Score:** 0.836/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Internal Consistency (0.79)

**One-line assessment:** ADR-003 is structurally strong and methodologically sound but contains a skill-count inconsistency (Group 3 categorization ambiguity, 11 vs. 13 gap), untraced quantitative claims in the L1 implementation section (1,250x cost multiplier), and insufficient resolution of the Component A foundational assumption challenge raised in its own S-002 self-review. The ADR falls short of the C4 threshold (0.92 required; 0.836 achieved); targeted revision of Group 3 categorization, L1 evidence traces, and the self-diagnosis assumption counter-argument will close the gap.

---

## Scoring Context

- **Deliverable:** `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/phase-5/ADR-003-routing-disambiguation.md`
- **Deliverable Type:** ADR (Architecture Decision Record)
- **Criticality Level:** C4 (quality threshold >= 0.92 per H-13; elevated from AE-003 auto-C3 per orchestration directive)
- **Scoring Strategy:** S-014 (LLM-as-Judge), 6-dimension weighted composite
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **ADR Gate Checks Applied:** GC-ADR-1 through GC-ADR-7
- **Scored:** 2026-02-28T00:00:00Z
- **Iteration:** I1 (first scoring)

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.836 |
| **Threshold** | 0.92 (H-13, C4 minimum) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No (no prior adv-executor reports available) |
| **Gap to Threshold** | 0.084 (significant; requires targeted revision) |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.87 | 0.174 | All Nygard sections present; Group 3 (architecture, eng-team) missing consequence specifications in L1 despite L0 stating they need additions |
| Internal Consistency | 0.20 | 0.79 | 0.158 | Group 3 categorization ambiguous (architecture/SKILL.md described as both Group 1 and Group 3); 11 vs. 13 skill count logic inconsistent |
| Methodological Rigor | 0.20 | 0.87 | 0.174 | S-002/S-004/S-013 applied; four options with steelman; Component A self-critique concedes the foundational assumption without providing a stronger basis |
| Evidence Quality | 0.15 | 0.78 | 0.117 | Evidence tier table present; UNTESTED claims disclosed; L1 consequence text lacks citations; "1,250x cost multiplier" untraced |
| Actionability | 0.15 | 0.86 | 0.129 | Migration steps, per-skill specs, Phase 2 verdict table present; Step 1 lacks ownership and output artifact definition; no acceptance criteria for consequence adequacy |
| Traceability | 0.10 | 0.84 | 0.084 | 9 references with type and relevance; L1 implementation claims not individually traced; Group 3 classification inconsistency undermines CX-006 traceability |
| **TOTAL** | **1.00** | | **0.836** | |

**H-15 Arithmetic Verification:**
- 0.174 + 0.158 = 0.332
- 0.332 + 0.174 = 0.506
- 0.506 + 0.117 = 0.623
- 0.623 + 0.129 = 0.752
- 0.752 + 0.084 = **0.836** (confirmed)

---

## ADR Gate Check Results

| Gate | Check | Status | Evidence |
|------|-------|--------|----------|
| GC-ADR-1 | Nygard format compliance | PASS | All required sections present: Context, Constraints, Forces, Options, Decision, Consequences, Risks, Related Decisions, References |
| GC-ADR-2 | Evidence tier labels on all claims | PARTIAL FAIL | Evidence table in Context section is correctly labeled; L1 per-skill consequence claims (lines 314-331) carry no evidence tier labels; "1,250x cost multiplier" has no citation |
| GC-ADR-3 | PG-003 reversibility assessment present | PASS | PG-003 section present with Component A (NOT REVERSIBLE by design) and Component B (FULLY REVERSIBLE); reversal protocol enumerated |
| GC-ADR-4 | Phase 2 dependency gate present for Component B | PASS | Explicitly stated: "Component B MUST NOT be implemented until Phase 2 provides one of three verdicts"; three-verdict table provided |
| GC-ADR-5 | No false validation claims | PASS | UNTESTED claims disclosed; A-11 not cited; AGREE-5 not cited as T1/T3; VS-001-VS-004 correctly labeled "HIGH observational, LOW causal" |
| GC-ADR-7 | Auditability motivation clearly separated from framing motivation | PASS | Separation is explicit and consistent from L0 through Decision through Compliance sections; "two-component" rationale is the structural backbone of the ADR |

**Gate check summary:** 5 PASS, 1 PARTIAL FAIL (GC-ADR-2: L1 consequence claims uncited). No automatic REVISE trigger from Critical findings beyond the composite score.

---

## Detailed Dimension Analysis

### Completeness (0.87/1.00)

**Evidence:**

The ADR is structurally complete per Nygard format: L0 Executive Summary, Context (problem statement, background, evidence base), Constraints (7 constraints with sources), Forces (5 enumerated tensions), Options Considered (4 options with steelman for each), Decision with rationale and alignment table, L1 Technical Implementation (templates for Group 1 and Group 2, per-skill consequence specifications, migration steps, Component B gate table), L2 Architectural Implications (systemic consequences, integration table, future flexibility), Consequences (positive/negative/neutral), Risks (5 risks with P/I/mitigation), PG-003 Reversibility Assessment, Adversarial Self-Review (S-002 two assumptions, S-004 three failure scenarios, S-013 inversion), Compliance (constitutional, evidence tier, constraint verification), Related Decisions, References, PS Integration.

GC-ADR-3: PG-003 section present and substantive.
GC-ADR-4: Phase 2 dependency gate explicitly specified with three-verdict decision table.

**Gaps:**

The L0 states: "2 that are substantively complete but still lack consequence text" (referring to architecture/SKILL.md and eng-team/SKILL.md, classified as Group 3). If these 2 skills "still lack consequence text," they require additions. However, the L1 per-skill consequence specifications only cover Group 1 (5 skills) and Group 2 (6 skills). Neither architecture/SKILL.md nor eng-team/SKILL.md appears in any consequence specification table. The ADR acknowledges these skills need additions but does not provide those additions. This is a completeness gap: the ADR mandates domain-specific consequence text per C-005 but does not deliver it for 2 of the 13 skills it explicitly covers.

**Improvement Path:**

Add a Group 3 row to the per-skill consequence specifications table (or a separate table) with domain-specific consequence text for architecture/SKILL.md and eng-team/SKILL.md misrouting scenarios. This is consistent with the ADR's own C-005 requirement.

---

### Internal Consistency (0.79/1.00)

**Evidence:**

The two-component decision (unconditional content + conditional framing) is stated consistently throughout: L0, Decision, L1 Component A/B split, PG-003, Compliance, Related Decisions. The Phase 2 dependency gate for Component B is applied uniformly. The C-006 constraint ("All constraint language in this ADR uses NEVER/MUST NOT framing") is fulfilled in the Constraints table.

**Gaps:**

**Gap 1: Group 3 categorization ambiguity.** Lines 91-93 describe Group 3: "architecture/SKILL.md -- has partial routing guidance through layer dependency rules but LACKS a dedicated routing disambiguation section (classified under Group 1 in CX-006 finding but separately noted due to implicit routing signals)." This states architecture/SKILL.md is in Group 3 but simultaneously acknowledges it is "classified under Group 1 in CX-006." This is contradictory -- the ADR cannot simultaneously place a skill in Group 1 (no routing disambiguation) and Group 3 (routing disambiguation present). The parenthetical acknowledgment does not resolve the contradiction; it documents it without reconciling it.

**Gap 2: Skill count logic.** The L0 executive summary states: "All 13 skills in the current inventory: 5 that are fully missing routing disambiguation sections, 6 that have partial sections lacking consequence documentation, and 2 that are substantively complete but still lack consequence text." Reading the groups: Group 1 = 5 skills (fully missing), Group 2 = 6 skills (partial), Group 3 = 2 skills (substantively complete but lacking consequence text). This arithmetic (5+6+2=13) is consistent. However, line 94 states "11 skills require either new routing disambiguation sections or consequence additions" (Group 1 + Group 2 = 5+6 = 11). But the L0 says Group 3's 2 skills "still lack consequence text" -- meaning they also need consequence additions. If Group 3 skills need consequence text, the count requiring additions is 13, not 11. The ADR simultaneously states 11 skills require additions (line 94) and that 13 total skills lack something (L0). This inconsistency undermines the scope claim.

**Gap 3: C-006 scope inconsistency.** C-006 states "All constraint language in this ADR uses NEVER/MUST NOT framing." The Constraints table uses this vocabulary. However, many non-constraint sections use SHOULD (e.g., "SHOULD revert section headers," "SHOULD revert individual row vocabulary" in PG-003 reversal protocol). If C-006 applies only to constraint language, this is fine. But the ADR does not define the scope of C-006 narrowly -- the instruction "All constraint language" could be read as applying wherever the ADR imposes requirements, creating ambiguity about which language is "constraint language."

**Improvement Path:**

Resolve the Group 3 categorization: either move architecture/SKILL.md to Group 1 (consistent with CX-006) and explain why it is listed with Group 3, or reclassify it in Group 3 and explain why CX-006's Group 1 classification is superseded. Update the skill count logic to either (a) exclude Group 3 from "requiring additions" and explain why their consequence gaps are acceptable, or (b) include Group 3 in the 11 count and add their consequence specifications to L1. Clarify C-006 scope in the Constraints table.

---

### Methodological Rigor (0.87/1.00)

**Evidence:**

The methodological apparatus is substantial for a C4 ADR:
- Four options evaluated with steelman for each (S-003 applied correctly -- strengthening before critiquing)
- Constraint compliance matrix (7 constraints, each with status and evidence)
- Adversarial self-review: S-002 (two key assumptions challenged with counter-arguments), S-004 (three pre-mortem failure scenarios with mitigations), S-013 (inversion: what if no routing disambiguation anywhere?)
- Evidence tier table distinguishing T4 observational from UNTESTED
- Risk registry (5 risks with probability/impact/mitigation)
- Migration steps with sequencing rationale
- Component A/B separation as a methodological contribution (correctly handles the unconditional/conditional distinction)

**Gaps:**

The S-002 Devil's Advocate challenge to Assumption 1 ("Consequence documentation improves routing accuracy") raises a legitimate concern: "If the agent is already processing a task, it may not re-evaluate its suitability after invocation." The counter-argument states: "What consequence documentation provides is not guaranteed self-diagnosis but the availability of diagnostic information... The value is in auditability (human reviewers can determine if misrouting occurred) more than in real-time self-correction."

This is a partial concession that weakens Component A's stated motivation. The L0 says Component A's motivation is "routing auditability" and the Decision section says agents can "self-diagnose misrouting" by reading the routing disambiguation section. If the counter-argument concedes that real-time self-correction is not guaranteed, the primary motivation shifts from routing correctness to documentation/auditability. This is a valid motivation but it is weaker than the routing accuracy framing used elsewhere. The ADR does not update the Decision rationale to reflect this concession -- the Decision still says "post-invocation self-diagnosis" (line 252) even after the S-002 counter concedes this is not guaranteed. This is a methodological gap: adversarial self-review identified a weakening of the primary motivation but the Decision section was not updated to reflect it.

**Improvement Path:**

In the Decision section's Component A rationale, acknowledge that "self-diagnosis" is aspirational rather than guaranteed, and ground the motivation primarily in auditability (documentation of what goes wrong) rather than in real-time agent correction. This makes the claim more defensible without weakening the component's value. Alternatively, provide evidence (T4 at minimum) that agents do read SKILL.md routing disambiguation sections during execution.

---

### Evidence Quality (0.78/1.00)

**Evidence:**

The evidence table (lines 98-109) is well-structured with columns for Evidence ID, Source, Tier, Content, and Confidence. All major claims in the Context and Decision sections trace to this table. GC-ADR-5 is met: AGREE-5 is not cited as T1/T3 (it is referenced only in the constraint against citing it, C-007); A-11 is not cited; VS-001-VS-004 are correctly labeled "HIGH observational, LOW causal." The evidence gap disclosure (line 110) is explicit and accurate: "No controlled evidence exists for the claim that 'MUST NOT use when:' framing produces better routing compliance than structurally equivalent positive routing guidance." NPT-010 is labeled AGREE-8 Moderate (not AGREE-5, which is the prohibited rank ordering).

**Gaps:**

**Gap 1: Untraced quantitative claim.** The per-skill consequence specification for transcript (line 319) states "1,250x cost multiplier if Task agents invoked unnecessarily." No evidence ID is cited for this figure, no source document is referenced, and no derivation is provided. This is a specific quantitative claim presented in a table of "domain-specific consequences" that are described as "derived from TASK-010 per-skill analysis and trigger map collision data (E-016)." If this figure comes from TASK-010, it should be cited as TASK-010, line N. If it is an analyst inference, it should be labeled "(analyst estimate, unverified)" per P-022.

**Gap 2: L1 consequence text lacks evidence tier labels.** The per-skill consequence specification tables (Group 1, lines 314-320; Group 2, lines 324-331) present specific consequence text without evidence tier labels. GC-ADR-2 requires evidence tier labels on all claims. The instruction at line 310 states the table is "derived from TASK-010 per-skill analysis and trigger map collision data (E-016)" -- but this is a single block-level attribution, not per-row traceability. Claims like "Bootstrap is a navigation tool; invoking it for work tasks wastes context budget loading orientation content with no analytical capability" (Group 1, bootstrap row) are analyst inferences, not audited facts. They should be labeled T4 or T5 (analyst inference) per the tier taxonomy.

**Gap 3: "3-5x context budget" for orchestration misrouting (line 328) has no source.** Similar to the 1,250x claim, this specific multiplier is asserted without citation.

**Improvement Path:**

Trace or label all specific quantitative claims in the L1 consequence tables. Either cite the source document and section ("TASK-010, Section 3.2, 1,250x cost multiplier"), or label as "(analyst estimate, not yet validated)" with a note that Phase 2 or implementation monitoring will provide empirical data. Add evidence tier labels (T4 or T5) to each consequence specification row.

---

### Actionability (0.86/1.00)

**Evidence:**

Component A implementation is actionable: templates provided for both Group 1 (new section) and Group 2 (consequence column addition), per-skill consequence specifications for all 11 audited skills (Group 1: 5 specs, Group 2: 6 specs), migration steps enumerated (5 steps with sequencing rationale), and priority guidance (highest-collision skills first per R-005 mitigation). Component B implementation is clearly gated with a three-verdict decision table. The pre-mortem failure scenarios each include a mitigation. The risk registry provides mitigations for all 5 risks.

**Gaps:**

**Gap 1: Migration Step 1 lacks ownership and output artifact.** Step 1 states "Audit trigger map collisions" but does not specify who performs the audit, what artifact the audit produces (e.g., a collision matrix file at a specific path), or what counts as "documented." Without an owner and output artifact, Step 1 is a description of an activity, not an actionable instruction.

**Gap 2: No acceptance criteria for consequence adequacy.** The template constraints say consequences MUST "name the specific failure mode" and MUST NOT use "generic consequence text." But no acceptance criteria specify how a reviewer determines whether the consequence text is sufficiently specific. The template provides an example (root cause analysis -> "Incorrect methodology applied; convergent investigation replaced with divergent exploration; root cause not isolated") but does not quantify what level of specificity satisfies the C-005 requirement.

**Gap 3: Group 2 retrofit edge case not addressed.** The Component A template for Group 2 skills shows how to add a consequence column to an existing "Do NOT use when:" bullet list. But several Group 2 skills have their exclusions in different formats (e.g., ast/SKILL.md's "Do NOT use /ast for:" format vs. adversary/SKILL.md's redirect format). The migration step doesn't address format heterogeneity in the retrofit path.

**Improvement Path:**

Add an owner field to each migration step (e.g., "Owner: ps-architect or designated skill maintainer"). Specify the output artifact for Step 1 (e.g., "trigger map collision matrix at `work/routing-collisions.md`"). Add a consequence adequacy rubric (minimum: names the specific failure mode, the agent family affected, and the resource wasted) to the template constraints. Add a note in the Group 2 retrofit section addressing format heterogeneity.

---

### Traceability (0.84/1.00)

**Evidence:**

Nine references with type and relevance. Evidence IDs (AP-01/AP-02, CX-003, CX-006, E-016, NPT-009, NPT-010, PG-003, VS-001-VS-004) all traced to named source documents. Constraint IDs (C-001 through C-007) each have a source column. Phase 2 dependency traced to barrier-2/synthesis.md ST-5, PG-003. ADR cross-references explicit in Related Decisions table (ADR-001 through ADR-004 with relationship types). GC-ADR-7 is satisfied: the auditability motivation vs. framing motivation separation is traceable through L0, Decision, and Compliance sections consistently.

**Gaps:**

**Gap 1: Group 3 classification inconsistency undermines CX-006 traceability.** The ADR traces Group 3's categorization to CX-006 (TASK-010 audit) but simultaneously acknowledges that CX-006 classifies architecture/SKILL.md under Group 1, not Group 3. This means the ADR's Group 3 classification is NOT traced to CX-006 -- it is a modification of CX-006 that is not sourced to any alternative analysis. The reader cannot trace Group 3's membership to any audited source.

**Gap 2: L1 consequence specifications have block-level attribution, not row-level.** Lines 314-320 attribute the entire Group 1 table to "TASK-010 per-skill analysis and trigger map collision data (E-016)." But the specific consequence text rows are analyst inferences from that data, not direct quotes from TASK-010. Row-level traceability is absent: readers cannot verify which consequence text comes from TASK-010 directly vs. analyst synthesis.

**Gap 3: Quantitative claims (1,250x, 3-5x) untraceable.** As noted in Evidence Quality, these specific figures have no source trace. For a C4 ADR where all claims should be traceable, untraced quantitative figures represent a traceability gap.

**Improvement Path:**

Resolve the Group 3 classification trace: either source it to an alternative analysis with an evidence ID, or remove Group 3 and re-classify architecture/SKILL.md under Group 1 consistent with CX-006. Add per-row footnote citations to the L1 consequence tables (e.g., "[CX-006]" or "[analyst inference]"). Trace or remove the 1,250x and 3-5x quantitative claims.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Internal Consistency | 0.79 | 0.88 | Resolve Group 3 categorization ambiguity: reconcile architecture/SKILL.md placement (Group 1 per CX-006 vs. Group 3 per ADR body); update the 11 vs. 13 skill count logic to be unambiguous about whether Group 3 skills are included in the 11 requiring additions |
| 2 | Evidence Quality | 0.78 | 0.87 | Trace or label all untraced claims in L1 consequence tables: cite source for "1,250x cost multiplier" and "3-5x context budget" claims, or label as "(analyst estimate, unvalidated)"; add per-row evidence tier labels (T4/T5) to Group 1 and Group 2 consequence specification rows |
| 3 | Completeness | 0.87 | 0.93 | Add Group 3 consequence specifications: provide domain-specific consequence text for architecture/SKILL.md and eng-team/SKILL.md misrouting scenarios consistent with the C-005 requirement the ADR itself imposes |
| 4 | Methodological Rigor | 0.87 | 0.93 | Update Decision rationale to reflect S-002 concession: the self-diagnosis claim is aspirational; ground Component A's primary motivation in auditability (human-reviewable documentation) rather than real-time agent self-correction; add at minimum T4 evidence that agents access SKILL.md content during execution |
| 5 | Traceability | 0.84 | 0.91 | Add per-row citations to L1 consequence tables; resolve Group 3 classification trace (current trace is to CX-006, which contradicts the Group 3 assignment); source the Group 3 categorization to an explicit analysis or remove it |
| 6 | Actionability | 0.86 | 0.92 | Add ownership and output artifact to each migration step; add consequence adequacy rubric to the template constraints section; address Group 2 format heterogeneity in the retrofit path |

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing composite
- [x] Evidence documented for each score with specific line references
- [x] Uncertain scores resolved downward (Internal Consistency: wavered between 0.79 and 0.82 -- resolved to 0.79 due to the Group 3/Group 1 contradiction being a clear logical inconsistency, not merely vague; Evidence Quality: wavered between 0.78 and 0.82 -- resolved to 0.78 because GC-ADR-2 partial fail on L1 claims is a gate-level finding)
- [x] C4 calibration applied: a first draft scoring 0.836 on a C4 ADR is in the expected 0.80-0.90 range for a well-structured but incompletely reconciled draft; 0.92 is a high bar that requires resolution of all identified inconsistencies
- [x] No dimension scored above 0.95 (highest: 0.87 for Completeness and Methodological Rigor -- justified by the genuinely strong structural apparatus, but capped by specific identified gaps)
- [x] Scores not inflated by the ADR's strong self-critique apparatus (the adversarial self-review is a positive signal for methodological rigor but does not compensate for dimensions scored on independent evidence)

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.836
threshold: 0.92
weakest_dimension: internal_consistency
weakest_score: 0.79
critical_findings_count: 0
gate_check_failures:
  - GC-ADR-2: PARTIAL FAIL (L1 consequence claims uncited; quantitative figures untraced)
iteration: 1
improvement_recommendations:
  - "Resolve Group 3 categorization ambiguity (architecture/SKILL.md: Group 1 per CX-006 vs. Group 3 per ADR body)"
  - "Trace or label L1 consequence claims -- 1,250x and 3-5x multipliers have no source"
  - "Add Group 3 consequence specifications for architecture/SKILL.md and eng-team/SKILL.md"
  - "Update Decision rationale to reflect S-002 concession on self-diagnosis assumption"
  - "Add per-row citations to L1 consequence tables; resolve Group 3 trace to CX-006 contradiction"
  - "Add ownership, output artifact, and acceptance criteria to migration steps"
gap_to_threshold: 0.084
revision_priority: internal_consistency_then_evidence_quality
```
