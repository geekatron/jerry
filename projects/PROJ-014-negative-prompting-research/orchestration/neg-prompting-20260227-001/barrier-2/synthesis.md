# Barrier 2 Cross-Pollination Synthesis: Phase 2 Analysis Integration

> ps-synthesizer | TASK-007 | Barrier 2 | PROJ-014 | 2026-02-28
> Synthesis Type: Cross-pollination of Phase 2 analysis outputs (TASK-005, TASK-006) + Barrier 1 artifacts
> Inputs: claim-validation.md (R4, 0.959 PASS), comparative-effectiveness.md (R5, 0.933 max-iter), barrier-1/synthesis.md (R4, 0.953 PASS), barrier-1/supplemental-vendor-evidence.md (R4, 0.951 PASS)
> Methodology: Thematic integration per Braun & Clarke (2006); cross-reference matrix; confidence reconciliation
> Quality threshold: >= 0.95 (C4, orchestration directive)
> Self-review: H-15 applied before completion
> Version: 3.0.0 (Iteration 3 — I2→I3 revision addressing R-001 Major + R-002, R-003, R-006 Minor findings)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Unified Phase 2 verdict with key imperatives index |
| [L1: Cross-Pollination Analysis](#l1-cross-pollination-analysis) | Seven synthesis tasks with full analysis |
| [ST-1: Evidence-Effectiveness Integration](#st-1-evidence-effectiveness-integration) | Claim validation evidence mapped to effectiveness hierarchy |
| [ST-2: Confidence Reconciliation](#st-2-confidence-reconciliation) | SUPPORTED/PARTIALLY SUPPORTED/UNSUPPORTED/UNTESTED vs. HIGH/MEDIUM/LOW/UNTESTED |
| [ST-3: Cross-Document Consistency Check](#st-3-cross-document-consistency-check) | Contradictions, tensions, and unstated assumptions |
| [ST-4: Synthesis Verdict](#st-4-synthesis-verdict) | Unified Phase 2 conclusion with per-finding confidence tags |
| [ST-5: Downstream Phase Inputs](#st-5-downstream-phase-inputs) | Phase 3, 4, 5 prerequisites and constraints with adversary gate verification requirements |
| [ST-6: Retrospective A/B Synthesis](#st-6-retrospective-ab-synthesis) | PROJ-014 vs. PROJ-007 combined with D3/D4 observational evidence |
| [ST-7: Controlled Experiment Readiness](#st-7-controlled-experiment-readiness) | Pilot design sufficiency — BLOCKING prerequisite gates |
| [L2: Full Evidence Tables and Matrices](#l2-full-evidence-tables-and-matrices) | Detailed cross-reference, confidence matrix, downstream specifications |
| [Source Summary](#source-summary) | Contributing sources with pattern attribution |
| [Self-Review Checklist](#self-review-checklist) | H-15 compliance |
| [Revision Log (I1→I2)](#revision-log-i1i2) | Finding-by-finding resolution of all Critical and Major findings |
| [Revision Log (I2→I3)](#revision-log-i2i3) | Resolution of R-001 Major + R-002, R-003, R-006 Minor findings |

---

## L0: Executive Summary

### Phase 2 Position: Three-Line Summary

> **What is established (HIGH confidence, usable NOW):** Blunt standalone prohibition underperforms structured alternatives (T1 evidence). Vendors consistently use structured negative framing in HARD enforcement tiers (T4 observational fact).
> **What is provisional (MEDIUM confidence, use with scope caveat):** Specific structured negative techniques at ranks 5–6 improve negation accuracy (A-23, T1) and compliance (A-15, T1) vs. blunt prohibition — scope is compliance and negation accuracy, NOT hallucination rate.
> **What is untested (Phase 2 experimental target):** Whether structured negative constraints at ranks 9–11 outperform structurally equivalent positive constraints. The 60% hallucination reduction claim has no published controlled evidence for or against it.

### Key Imperatives Index (NEVER violate downstream)

| Imperative | Applies to | Source |
|-----------|-----------|--------|
| NEVER cite the 60% hallucination claim as established or disproven | All phases | ST-4, TASK-005 |
| NEVER treat MEDIUM-confidence findings as established (HIGH) | Phase 3, 4, 5 | ST-2, ST-4 |
| NEVER conflate observational HIGH-confidence with causal HIGH-confidence | Phase 3, 4 | ST-2 |
| NEVER launch the full experiment before pilot GO verdict | Phase 5 | ST-7 |
| NEVER launch the pilot before all four BLOCKING prerequisites are COMPLETE | Phase 5 | ST-7 |
| NEVER treat the 12-level hierarchy as externally validated | Phase 3 | ST-3, ST-5 |
| NEVER modify the hierarchy without preserving the C1–C7 pilot condition alignment | Phase 3 | ST-3 |
| NEVER cite ST-6 retrospective data as a directional comparison | Phase 4, 5 | ST-6 |
| NEVER present the enforcement tier vocabulary design as experimentally validated | Phase 4 | ST-5 |
| NEVER use S-014 quality gate score as primary metric for the hallucination research question | Phase 5 | ST-5 |

### Narrative Summary

Phase 2 of PROJ-014 produced two high-quality analysis deliverables — claim-validation.md (R4, 0.959) and comparative-effectiveness.md (R5, 0.933 max-iter) — that are internally consistent, mutually reinforcing, and collectively constitute a coherent Phase 2 position: the 60% hallucination reduction claim remains untested in any controlled public study, no published controlled evidence for or against the specific claim exists, and the hypothesis is alive as a research question. The two deliverables agree on all core verdicts and apply reconcilable confidence scales derived from the same evidence base; their primary organizational difference is analytical focus (claim-first vs. dimension-first), not epistemic disagreement. The strongest combined signal from Phase 2 is the convergent null finding — confirmed across 75 sources in three surveys, validated by independent claim assessment and dimensional analysis — paired with a directional signal from vendor self-practice evidence (HIGH confidence observational, causal interpretation contested) showing that all major vendors use structured negative constraints in their safety-critical enforcement tiers despite recommending positive framing for general users. The controlled experiment pilot design (n=30, McNemar test, 7 conditions) combined with the 5-dimension comparative framework constitutes a sufficient experimental foundation for Phase 2 completion, subject to four BLOCKING prerequisites that must be COMPLETE before pilot launch. Phase 3 (taxonomy), Phase 4 (Jerry framework application), and Phase 5 (implementation) must be scoped to operate under evidence uncertainty — no directional verdict about framing superiority is yet established — but the practitioner guidance (PG-001 through PG-005, each with distinct confidence tiers) and the 12-level effectiveness hierarchy provide actionable scaffolding that downstream phases can consume without waiting for Phase 2 experimental results. A retrospective comparison of PROJ-014 (negative-constraint governance) vs. PROJ-007 (positive-framing governance) produced an observational baseline only — NEVER cite as a controlled test.

---

## L1: Cross-Pollination Analysis

### ST-1: Evidence-Effectiveness Integration

**Synthesis task:** Map the claim validation evidence assessment (TASK-005) against the comparative effectiveness dimensions (TASK-006). Where does evidence support the effectiveness hierarchy? Where are there gaps?

#### Integration findings

The 12-level effectiveness hierarchy from TASK-006 (sourced from synthesis.md AGREE-5) maps directly onto the claim evidence catalog from TASK-005. The integration reveals a structured pattern: evidence is strong at the extremes of the hierarchy but silent in the middle range most relevant to PROJ-014.

**Hierarchy positions with evidence support:**

| Hierarchy Rank | Technique | TASK-005 Claim | TASK-006 Confidence | Evidence Tier | Integration Note |
|---------------|-----------|----------------|---------------------|---------------|-----------------|
| Rank 12 | Standalone blunt prohibition | SUB-CLAIM B AGAINST (strong) | HIGH — performs WORSE than structured alternatives | T1 (A-20, AAAI 2026), T3 (A-19, A-31) | Full alignment: both deliverables agree blunt prohibition underperforms |
| Rank 6 | Atomic decomposition (DeCRIM) | E-FOR-B-002 (MEDIUM) | MEDIUM — compliance improvement +7.3–8.0% | T1 (A-15, EMNLP 2024) | Full alignment: A-15 is cited identically in both deliverables; compliance outcome, not hallucination rate |
| Rank 5 | Warning-based meta-prompts | E-FOR-B-002 partial | MEDIUM (I5 upgrade) — negation accuracy +25.14% | T1 (A-23, EMNLP 2025 Findings, confirmed) | Full alignment: A-23's scope (negation reasoning accuracy, not hallucination rate) documented consistently in both |
| Rank 3 | Programmatic enforcement | E-FOR-B-003 (MEDIUM) | Not a primary dimension — consistent with T3 | T3 (C-13, DSPy) | Aligned: both treat DSPy as T3, infrastructure-level, outside prompt framing scope |
| Ranks 9–11 | Declarative behavioral negation, paired, justified | E-FOR-B-004 (MEDIUM-WEAK) | HIGH observational, LOW causal | T4 (VS-001–VS-004) | Full alignment: both deliverables treat vendor self-practice as observationally strong, causally contested |

**Hierarchy positions with evidence gaps (both deliverables agree):**

| Hierarchy Range | Gap | TASK-005 characterization | TASK-006 characterization | Integration verdict |
|----------------|-----|--------------------------|--------------------------|---------------------|
| Ranks 9–11 vs. positive equivalents | Primary Phase 2 gap | "UNTESTED" (ST-2 below) | "UNTESTED" in Directional Verdict #5 | Unanimously agreed within this pipeline: this is the research target |
| 60% hallucination rate claim (all ranks) | Central null finding | "NULL FINDING: untested, not disproven" | "NO SUPPORT — UNTESTED" | Unanimously agreed null finding within this pipeline |
| Ranks 9–11 causal mechanism | Mechanism isolation | Phase 2 needed | Phase 2 Condition C4 required | Both deliverables identify the same experimental need |

**Where evidence supports the hierarchy vs. where it does not:**

The hierarchy is strongly evidenced at rank 12 (clear failure, T1) and partially evidenced at ranks 5–6 (structured improvement, T1, though for different outcomes: compliance and negation accuracy, not hallucination rate directly). Ranks 9–11 — the tier most relevant to PROJ-014's enforcement architecture (VS-001 through VS-004) — are supported only by T4 observational evidence. The hierarchy's internal ordering within ranks 9–11 (declarative vs. paired vs. justified) has no controlled evidence whatsoever.

**NEVER conflate evidence availability with hierarchy position validity:** The gap in ranks 9–11 evidence reflects a literature void, not a hierarchy design error. TASK-005's structural exclusion assessment (SE-1 through SE-5) documents that production deployment evidence is inaccessible by design. Both deliverables correctly note this.

**Vendor evidence integration (supplemental-vendor-evidence.md):**

The supplemental report's VS-001 through VS-004 findings directly populate the TASK-006 D5 dimension (Practitioner and Vendor Adoption). The 33-instance catalog with per-rule citations is the T4 evidence underlying D5's HIGH-confidence observational finding. The supplemental report's three competing explanations (Explanation 1: audience differentiation; Explanation 2: genre convention; Explanation 3: engineering discovery) are explicitly carried into TASK-006's D5 parsimony analysis. The integration is complete and consistent: supplemental evidence feeds into both deliverables without contradiction.

**Session observation integration (supplemental-vendor-evidence.md EO-001–EO-003):**

The supplemental report also documents three session observations: EO-001 (L2 re-injection observed during PROJ-014 research sessions as the primary enforcement mechanism), EO-002 (negative constraint violations were caught by adversary gates in PROJ-014 sessions, not by PLAN.md review), and EO-003 (vendor documentation style consistently separates enforcement-tier rules from recommendation-tier guidance). These session observations are T5 evidence (single-session observation, no controls). They corroborate the VS-001–VS-004 observational pattern but add no causal evidence. NEVER treat EO-001–EO-003 as controlled evidence for enforcement mechanism effectiveness.

---

### ST-2: Confidence Reconciliation

**Synthesis task:** Reconcile the confidence assessments across both deliverables. TASK-005 assesses claims as SUPPORTED/PARTIALLY SUPPORTED/UNSUPPORTED/UNTESTED. TASK-006 assigns confidence as HIGH/MEDIUM/LOW/UNTESTED. Do these align? Where do they diverge? What does the combined assessment tell us?

#### Reconciliation matrix

| Topic | TASK-005 Verdict | TASK-006 Confidence | Alignment? | Combined Assessment |
|-------|-----------------|---------------------|------------|---------------------|
| 60% hallucination reduction (Sub-claim A) | NULL FINDING: untested, not disproven | LOW for 60% claim; UNTESTED (no controlled study) | ALIGNED within pipeline | No published evidence for or against; not disproven; Phase 2 required |
| Better results generally (Sub-claim B) | PARTIALLY SUPPORTED for specific sub-types; NOT SUPPORTED for general claim | MEDIUM for negation accuracy (A-23, T1); MEDIUM for compliance (A-15, T1); HIGH observational for vendor adoption pattern | ALIGNED within pipeline — partial support for specific techniques, not general claim | Structured negative techniques at ranks 5–6 show evidence of improvement on specific outcomes; the general claim is not supported |
| Blunt prohibition underperforms structured alternatives | SUPPORTED (E-AGN-B-001, HIGH) | HIGH — established finding | FULLY ALIGNED within pipeline | Highest-confidence finding in Phase 2; T1 evidence |
| Vendor self-practice (VS-001) | MEDIUM-WEAK (observational, inferential step required) | HIGH observational, LOW causal | ALIGNED within pipeline — same evidence, explicitly bifurcated into observation vs. causal inference | Direct observation is strong; why vendors chose negative framing is contested |
| Structured negative vs. structured positive | UNTESTED | UNTESTED | FULLY ALIGNED within pipeline | The critical Phase 2 experimental gap; no controlled evidence |
| Context compaction failure mode | LOW (practitioner reports, T4) | LOW — directional inversion possible under compaction | ALIGNED within pipeline | Documented failure mode, T4 evidence; not controlled; deployment-context conditional |
| A-23 (Barreto & Jana) — negation accuracy | MEDIUM-HIGH in E-FOR-B-002 | MEDIUM (I5 upgrade, T1 confirmed) | ALIGNED within pipeline — same paper, same finding; TASK-005 uses "MEDIUM-HIGH" vs. TASK-006's "MEDIUM" | Minor terminological variation; both correctly scope A-23 to negation reasoning accuracy, not hallucination rate; combined label adopts TASK-006's "MEDIUM" because the I5 upgrade represents the most recent calibrated assessment and the operationalized scale defines MEDIUM as exactly 1 T1 study with no replication |

**Note on agreement labels:** All agreement labels in this synthesis reflect internal consistency across four documents produced by the same research pipeline using the same underlying evidence base. These labels do NOT imply independent corroboration or convergent validity in the scientific sense. The researcher circularity caveat (Assumption U-004 in ST-3) applies throughout. A genuine "unanimously agreed" finding would require at minimum one independent research group reaching the same conclusion from a separate evidence base.

**The one minor terminological divergence:**

TASK-005 labels E-FOR-B-002 (Barreto & Jana) as "MEDIUM-HIGH" while TASK-006 labels the same finding as "MEDIUM" after its I5 upgrade. This is NOT a substantive contradiction. Both deliverables apply the same confidence scale definition ("exactly 1 T1 study with no replication = MEDIUM"); TASK-005's "MEDIUM-HIGH" appears in the evidence table and reflects the strength of the finding within the MEDIUM band, not a distinct confidence level. Both explicitly scope the finding to negation reasoning accuracy, not hallucination rate. The combined label adopts TASK-006's "MEDIUM" because the post-I5 calibration is the most recent and precisely defined. NEVER interpret this as an inter-deliverable conflict.

**What the combined confidence picture tells us:**

The combined picture is internally coherent and epistemically honest. Three distinct confidence tiers emerge:

- **HIGH confidence (established within this pipeline, observational):** Blunt prohibition underperforms structured alternatives (T1 causal); vendors use negative framing in enforcement tiers (T4 observational fact, causal interpretation contested).
- **MEDIUM confidence (provisional, single-study):** Specific structured negative techniques (ranks 5–6) improve negation accuracy and compliance vs. blunt prohibition; single T1 studies, no replication. NEVER extrapolate to hallucination rate reduction.
- **LOW/UNTESTED (research questions):** 60% hallucination claim; structured negative vs. structured positive at ranks 9–11; context compaction directional reversal; all causal interpretations of vendor self-practice.

This three-tier structure is the correct integrated Phase 2 confidence picture. Any downstream consumer that treats MEDIUM-confidence findings as established findings, or conflates observational HIGH-confidence with causal HIGH-confidence, will misrepresent the Phase 2 position.

---

### ST-3: Cross-Document Consistency Check

**Synthesis task:** Identify contradictions, tensions, or unstated assumptions between the two deliverables. Do they agree on the state of evidence? Do they draw compatible conclusions?

#### Consistency findings

**No material contradictions were identified.** The two deliverables draw from the same evidence base, apply reconcilable confidence scales (terminologically distinct but epistemically equivalent when mapped through the ST-2 reconciliation matrix), and reach compatible verdicts. What appear as differences are organizational — TASK-005 is claim-centric; TASK-006 is dimension-centric — not epistemic.

**Tensions identified (real but managed):**

| Tension | TASK-005 Treatment | TASK-006 Treatment | Resolution |
|---------|-------------------|-------------------|-----------|
| Vendor self-practice evidential weight | "MEDIUM-WEAK" — observational, requires inferential step | "HIGH observational, LOW causal" — explicitly bifurcated | Resolved: both correctly bifurcate observation from causal inference; terminological framing differs but the underlying epistemic position is identical |
| Researcher circularity risk | "observer-researcher confound" (DA-006-i1 acknowledgment) | "structural circularity" (A-002) — independent replication required before VS-002 interpretation relied upon | Resolved: both deliverables explicitly disclose circularity; both require independent replication |
| Null finding protection vs. directional signal | WARNING callout: do not cite as evidence negative prompting fails | Directional verdict recalibrated: predominantly LOW confidence; Phase 2 required | Resolved: both deliverables protect the null finding while maintaining the hypothesis as a research question; NEVER cite TASK-005 as a refutation |
| A-23 scope (negation accuracy vs. hallucination rate) | "MEDIUM-HIGH" in evidence table; correctly notes "Venue corrected to EMNLP 2025" | "MEDIUM" after I5 T1 confirmation; extensive scope note on negation comprehension vs. hallucination rate | Resolved: identical epistemic position; TASK-006 contains more detailed scope documentation; both correctly prevent conflation |

**Unstated assumptions that require explicit naming in downstream documents:**

1. **Assumption U-001: The 12-level hierarchy is stable across phases.** Both deliverables use the AGREE-5 hierarchy as an analytical backbone. Neither explicitly validates it against external frameworks. Downstream phases (especially Phase 3: taxonomy) must treat the hierarchy as an internally generated organizing framework, not as an empirically validated ranking. **Critical constraint: Any modification to the 12-level hierarchy by Phase 3 or later phases MUST preserve the alignment between hierarchy levels and the C1–C7 pilot conditions specified in TASK-005. Hierarchy reordering that disrupts this alignment invalidates the pilot design without Phase 5 impact assessment.** See ST-7 for implications.

2. **Assumption U-002: McNemar power calculation assumptions hold at pilot scale.** TASK-005 grounds π_d = 0.30 on comparable study extrapolations, not directly reported values. TASK-006 does not challenge this assumption. Both deliverables correctly document that the pilot's purpose is to calibrate this assumption. Downstream Phase 5 must not treat 0.30 as a validated prior.

3. **Assumption U-003: Context compaction conditions are not the primary deployment context.** TASK-005 and TASK-006 both note the context compaction failure mode (T-004, GAP-13), but both deliver their directional findings without explicitly conditioning them on deployment context. Downstream phases must not extract directional findings without noting the context compaction caveat. **Phase 5 deployment constraint:** The pilot design must explicitly include multi-turn context compaction test conditions to evaluate whether the T-004 directional reversal risk is confirmed or ruled out at pilot scale.

4. **Assumption U-004: Vendor self-practice evidence is not dominated by Anthropic specificity.** The VS-001 evidence originated in Anthropic (Claude Code behavioral rules). The supplemental evidence report extends this to OpenAI (C-6, C-7 documented in supplemental-vendor-evidence.md) and LlamaIndex (C-11). Of the 33 cataloged instances, the supplemental report documents: Anthropic/Claude Code = the primary source for VS-001 taxonomy (rules documented as exemplars); OpenAI behavioral guidance contributes C-6 and C-7 (2 of 33 instances are explicitly non-Anthropic vendor sources); LlamaIndex governance documentation contributes C-11. The vendor concentration is therefore Anthropic-heavy for the primary VS-001 catalog, with multi-vendor corroboration in the supplemental report. Downstream phases must not over-weight Anthropic-specific patterns as cross-vendor generalization without citing the concentration caveat.

---

### ST-4: Synthesis Verdict

**Synthesis task:** Produce a unified Phase 2 conclusion integrating what evidence shows, how negative vs. positive prompting compare across dimensions, and what the combined implications are for downstream phases.

**CRITICAL READING NOTE:** The findings below are organized by confidence tier. PG-001 through PG-005 are NOT uniformly authoritative — each carries a distinct confidence tag. NEVER extract PG statements without their co-located confidence tier and key caveat. A downstream author who removes the confidence tags misrepresents the Phase 2 position.

#### Established findings (HIGH confidence — usable NOW without Phase 2 experimental data)

**Finding H-1: Blunt prohibition is demonstrably less effective than structured alternatives**
- **Confidence:** HIGH | **Evidence tier:** T1 (A-20, AAAI 2026) + T3 (A-19, A-31) | **Scope:** All prompting contexts
- **Practitioner implication (PG-001) [T1+T3, HIGH, unconditional]:** NEVER use standalone blunt prohibition. This finding does not require Phase 2 resolution. It applies across models and task types.
- The 60% hallucination reduction claim is untested in any controlled public study. It has not been refuted. It cannot be cited as established. It cannot be cited as disproven. The null finding covers at most 30-40% of the total possible evidence base (SE-1 through SE-5 structure the rest as inaccessible).

**Finding H-2: Vendors use structured negative framing in HARD enforcement tiers (observational fact)**
- **Confidence:** HIGH observational | **Evidence tier:** T4 (VS-001–VS-004, 33 instances) | **Scope:** Direct observation of vendor documentation
- **Caution:** The reason for this vendor choice is contested across three competing explanations (audience differentiation, genre convention, engineering discovery). HIGH observational confidence does NOT imply HIGH causal confidence.
- **Practitioner implication (PG-002) [T1+T4, HIGH, unconditional]:** NEVER design a constraint without specifying hierarchy rank. This applies to both negative and positive framing choices. The hierarchy rank specification is what makes the constraint precise, regardless of framing vocabulary.

#### Provisional findings (MEDIUM confidence — use with scope caveat, single studies, no replication)

**Finding M-1: Structured negative techniques at rank 5 improve negation accuracy**
- **Confidence:** MEDIUM | **Evidence tier:** T1 (A-23, EMNLP 2025 Findings, confirmed) | **Scope:** Negation reasoning accuracy ONLY — NOT hallucination rate

> **Evidence boundary — MUST NOT conflate:** Finding M-1 above is grounded in A-23 (T1, controlled study). The practitioner implication that follows (PG-003) is NOT derived from A-23. PG-003 is sourced from T4 vendor self-practice observation (VS-001–VS-004), not from any controlled study. A-23 supports Finding M-1 only. NEVER treat PG-003 as T1-backed.

- **Practitioner implication (PG-003) [T4 observational, MEDIUM — working practice, not validated finding]:** Pair enforcement-tier constraints with consequences. This is a working practice observed in vendor self-practice (T4), not a finding from controlled comparison. Phase 2 will assess whether the pairing mechanism contributes causally to outcomes. If Phase 2 finds a null framing effect at ranks 9–11, the consequence-pairing may still be beneficial as a readability or comprehension aid, but its causal contribution to outcome quality will be unresolved.

**Finding M-2: Structured techniques at rank 6 improve compliance**
- **Confidence:** MEDIUM | **Evidence tier:** T1 (A-15, EMNLP 2024) | **Scope:** Behavioral compliance ONLY — NOT hallucination rate

#### Unconditional operational findings (evidence tier varies — apply regardless of Phase 2 outcome)

**Finding O-1: Context compaction creates a documented failure mode for negative framing**
- **Confidence:** LOW for directional reversal | **Evidence tier:** T4 (I-28, I-32), practitioner reports
- **Practitioner implication (PG-004) [T4, unconditional by failure mode logic]:** Test context compaction behavior before deployment. This is unconditional not because the evidence is strong, but because the failure mode is irreversible if encountered in production without prior testing.

**Finding O-2: Enforcement architecture investment outperforms framing vocabulary optimization**
- **Confidence:** T3 (DSPy, C-13) + T4 (NeMo) | **Evidence tier:** T3+T4 | **Scope:** Investment allocation decisions
- **Practitioner implication (PG-005) [T3, unconditional investment allocation]:** Prioritize enforcement architecture over framing vocabulary optimization. The DSPy and NeMo evidence supports this at infrastructure level.

#### Unified Phase 2 verdict

**The PROJ-014 hypothesis remains a research question, not a finding.** Phase 2 cannot issue a directional verdict favoring negative over positive framing. A directional verdict requires controlled evidence for the key comparison (structured negative vs. structured positive, ranks 9–11). That evidence does not exist. What Phase 2 has produced is a well-structured research question with:
- A clear null finding on the specific 60% claim (HIGH confidence, confirmed across 75 sources)
- MEDIUM-confidence directional support for structured techniques (ranks 5–6) outperforming blunt prohibition (rank 12)
- HIGH-confidence observational evidence of vendor practice patterns (causal interpretation contested)
- A methodologically sound experimental design to close the key gap

**No directional verdict direction (Phase 2 cannot state):** Whether structured negative constraints at ranks 9–11 outperform structurally equivalent positive constraints. This is the Phase 2 experimental target.

---

### ST-5: Downstream Phase Inputs

**Synthesis task:** Define what Phase 3 (taxonomy), Phase 4 (Jerry framework application), and Phase 5 (implementation) should receive from Phase 2. Identify constraints, prerequisites, and dependencies.

#### Phase 3 (Taxonomy) inputs

**What Phase 3 receives:**
- The 12-level effectiveness hierarchy (AGREE-5 from synthesis.md; used as analytical backbone in TASK-006). This is the primary taxonomy scaffolding. Phase 3 should extend, not replace, this hierarchy.
- The IG-002 taxonomy (Types 1–4 of negative prompting, from supplemental-vendor-evidence.md). Type 1 (naive blunt prohibition) is extensively studied; Types 2–4 (structured, L2-re-injected, constitutional triplet) are understudied. Phase 3 taxonomy must explicitly distinguish these.
- The 7-condition experimental framework (C1 through C7 from TASK-005) as a taxonomy organizing principle. Each condition corresponds to a distinct technique class that the taxonomy must categorize.

**Constraints for Phase 3:**
- NEVER treat the 12-level hierarchy as empirically validated. It is a narrative synthesis product (internally generated, passed adversary gate 0.953, not externally validated by independent researchers). Phase 3 may refine it but must disclose its origin.
- NEVER collapse the distinction between rank 12 (blunt prohibition, evidence-weak) and ranks 9–11 (structured vendor practice, T4 only). This distinction is the central analytical finding from Phase 2.
- NEVER produce a taxonomy that implies a directional verdict not established by Phase 2. Taxonomy items can state evidence strength; they MUST NOT state that negative framing outperforms positive framing at ranks 9–11.
- NEVER modify the hierarchy ordering without producing an explicit C1–C7 pilot condition alignment impact assessment. Any reordering that changes which hierarchy levels map to conditions C1–C7 invalidates the TASK-005 pilot design and requires Phase 5 to revise the pilot before execution.

**Phase 3 adversary gate verification requirement:** The Phase 3 adversary gate MUST verify: (1) the taxonomy does not imply a directional verdict at ranks 9–11; (2) the C1–C7 pilot condition mapping is preserved or an impact assessment is provided; (3) rank 12 is distinguished from ranks 9–11 with confidence labels. The Phase 3 orchestration plan MUST import these three verification requirements directly into its adversary selection plan (reference: adv-selector agent template) so the adversary gate check is triggered by the orchestration plan, not solely by this synthesis document.

**Prerequisites:** None — Phase 3 can operate immediately with Phase 2 outputs as-is.

#### Phase 4 (Jerry Framework Application) inputs

**What Phase 4 receives:**
- PG-001 through PG-005 (practitioner guidance from TASK-006, with per-PG confidence tiers as specified in ST-4) as the evidential basis for Jerry Framework constraint design.
- VS-001 through VS-004 (supplemental-vendor-evidence.md) documenting the existing 33-instance negative constraint pattern in Claude Code's own behavioral rules. Phase 4 should treat this as the observable production baseline.
- The enforcement tier vocabulary design (HARD: MUST/NEVER/MUST NOT; MEDIUM: SHOULD/RECOMMENDED; SOFT: MAY/CONSIDER) from VS-003 as a working practice, not a validated finding.
- T-004 (context compaction failure mode) as a deployment risk that Jerry Framework enforcement tier design must explicitly mitigate.

**Constraints for Phase 4:**
- NEVER present the enforcement tier vocabulary design as experimentally validated. It is a working practice supported by observational evidence (T4, VS-001–VS-004) with three competing causal explanations.
- NEVER implement Phase 4 changes that make Phase 2 experimental conditions unreproducible. The experimental design requires isolated framing conditions; framework changes that couple negative vocabulary to other mechanisms would confound Phase 2.
- NEVER ignore PG-003's contingency: if Phase 2 finds a null framing effect at ranks 9–11, vocabulary choice becomes convention-determined, not effectiveness-determined. Phase 4 design should be reversible on the vocabulary dimension.

**Phase 4 adversary gate verification requirement:** The Phase 4 adversary gate MUST verify: (1) no claim that enforcement tier vocabulary is experimentally validated; (2) Phase 2 experimental conditions remain reproducible after any Phase 4 framework changes; (3) PG-003 contingency path is documented in Phase 4 deliverables with explicit reversibility plan. The Phase 4 orchestration plan MUST import these three verification requirements directly into its adversary selection plan (reference: adv-selector agent template) so the adversary gate check is triggered by the orchestration plan, not solely by this synthesis document.

**Prerequisites:** Phase 3 taxonomy (recommended but not blocking — Phase 4 can operate with Phase 2 TASK-006 hierarchy directly).

#### Phase 5 (Implementation) inputs

**What Phase 5 receives:**
- The n=30 pilot design (TASK-005, Controlled Experiment Pilot Design section) as the execution specification. This includes: equivalence validation protocol, evaluator blinding protocol, evaluator training protocol, statistical stopping criterion, go/no-go criteria, model selection criteria, execution feasibility plan.
- The 7 experimental conditions (C1–C7) with full operationalization.
- The statistical power analysis (pilot power ≈ 0.17; full experiment n ≈ 268 for C2 vs. C3 primary comparison).
- PG-003's contingency path for inconclusive Phase 2 results — Phase 5 implementation plan must include this scenario.

**Constraints for Phase 5:**
- NEVER launch the full experiment (n=268) before running the n=30 pilot and confirming GO verdict on primary calibration criteria (π_d in 0.10–0.50 range; ≤ 4 execution failures; kappa ≥ 0.70).
- NEVER use S-014 quality gate score as the primary metric for the hallucination research question. The bifurcated research question requires: (1) hallucination rate as primary metric; (2) behavioral compliance as secondary metric; (3) S-014 quality score as tertiary only.
- NEVER conflate the 30-45 researcher-hours pilot feasibility estimate with the full experiment scale. The 7-condition full experiment multiplies outputs by approximately 4; automation validation is required before launch.
- NEVER pre-register the full experiment design before pilot calibration is complete. The n=268 sample size depends on the observed π_d from the pilot.
- NEVER launch the pilot before all four BLOCKING prerequisites are COMPLETE (see ST-7 for BLOCKING gate specification).

**Phase 5 adversary gate verification requirement:** The Phase 5 adversary gate MUST verify: (1) all four ST-7 BLOCKING prerequisites documented as complete before pilot launch; (2) pilot GO verdict documented before full experiment launch; (3) hallucination rate is designated primary metric, not quality gate score; (4) inconclusive-result protocol is present in the implementation plan; (5) obtain and document independent methods review of the n=30 pilot design from a researcher outside the PROJ-014 pipeline before pilot launch — this is the operationalized traceability for RT-004-i1 (deferred item: "SUFFICIENT" verdict lacks external validation; Phase 5 is the designated resolution point). The Phase 5 orchestration plan MUST import all five verification requirements directly into its adversary selection plan (reference: adv-selector agent template) so the adversary gate check is triggered by the orchestration plan, not solely by this synthesis document.

**Dependencies:** Phase 5 requires Phase 2 outputs (provided), plus a model availability check (Claude Sonnet, Claude Haiku, one non-Anthropic model per TASK-005 Model Selection Criteria section).

---

### ST-6: Retrospective A/B Synthesis

**Synthesis task:** Synthesize the retrospective comparison findings (PROJ-014 vs. PROJ-007) from TASK-005 with the observational evidence from TASK-006's D3/D4 dimensions.

**SCANNING CAUTION:** The numerical table below presents quality metrics that are CONFOUNDED. Read the confound analysis before extracting any numbers. NEVER cite these figures as a directional comparison between negative-constraint and positive-framing governance.

#### Combined retrospective picture

The TASK-005 retrospective comparison and TASK-006 D3/D4 dimensions report on the same underlying session data but from different analytical angles. When synthesized, they produce a coherent but carefully bounded picture.

**TASK-005 contribution — CONFOUNDED DATA (read confound verdict before using):**

| Metric | PROJ-014 (negative-constraint governance) | PROJ-007 (positive-framing PLAN.md) | Observed direction | Confound verdict |
|--------|--------------------------------------|-------------------------------------|-------------------|-----------------|
| First-pass score | 0.837 avg (2 deliverables) | 0.905 (Barrier 3 ADRs); 0.936 (Barrier 4 rule files) | PROJ-007 higher first-pass | CONFOUNDED: PROJ-007 tasks were templated ADRs and rule files; PROJ-014 tasks were novel cross-survey research synthesis. Task type difference, not framing effect. |
| Iterations to C4 PASS | 4.0 avg | 2.0 avg | PROJ-007 fewer iterations | CONFOUNDED: Same task type confound. Also: PROJ-007 had established quality templates; PROJ-014 was constructing templates. |
| Final score | 0.952 avg | 0.957 (Phase 5 portfolio); 0.952 adjusted | PROJ-007 marginally higher (Δ 0.005) | CONFOUNDED: 5 identified confounds all favor PROJ-007; the Δ 0.005 gap is within confound margin. |
| Score delta I1 to final | +0.116 avg | +0.032–0.052 per deliverable | PROJ-014 larger improvement arc | CONFOUNDED: Higher starting difficulty in PROJ-014 (novel research) produces larger improvement range as methodology converges. |
| Constraint violations | Zero (PROJ-014 PLAN.md constraints) | Not tracked | Not comparable | Cannot compare: PROJ-007 violations were not tracked with equivalent rigor. |

**Confound verdict from TASK-005:** ALL identified confounds favor PROJ-007 — task type (ADRs and rule files are templated; cross-survey research synthesis is novel), domain novelty, task complexity. Under a Bayesian lens, observing PROJ-014's final score within 0.5% of PROJ-007's adjusted portfolio average despite structurally harder conditions is mild evidence against the hypothesis that negative-constraint prompting degrades quality. It does not confirm that negative prompting improves quality.

**TASK-006 D3/D4 contribution:**

TASK-006 explicitly labels D3 and D4 as OBSERVATIONAL, NOT DIRECTIONAL. This labeling is correct and must carry forward into any synthesis of these dimensions.

- **D3 (Quality Gate Performance):** C4 results (0.953 and 0.951) are achievable under a negative-constraint prompting regime. This is an existence proof with 5 confirmed confounds (quality gate mechanism, specialized agents, structured templates, researcher expertise, source verification requirements). NEVER treat D3 as establishing that negative framing caused the quality gate pass.
- **D4 (Iteration Efficiency):** 4 iterations to C4 PASS on two deliverables under negative-constraint prompting. Two same-pipeline observations with no controlled baseline. NEVER treat as a directional comparison.

**Combined synthesis of retrospective evidence:**

The TASK-005 retrospective comparison and TASK-006 D3/D4 observations are consistent with each other and with the following unified statement:

*"Under negative-constraint project governance, C4-quality results were achieved on research synthesis tasks within 4 iterations. This outcome was observed in the presence of multiple co-present quality mechanisms (adversary tournament, specialized agents, structured templates, source verification requirements) and under task conditions that are structurally harder than the positive-framing comparison condition (PROJ-007). The directional signal from the retrospective comparison is that negative-constraint governance does not appear to harm final quality outcomes; it rules out one specific failure mode. The signal does not establish that negative-constraint governance improves quality outcomes relative to positive framing. The context compaction caveat (T-004, TASK-006 Finding T-004) applies: the PROJ-014 session did not encounter context compaction conditions; the directional finding may reverse under compaction."*

**What the combined retrospective picture contributes to Phase 2:**

The retrospective comparison establishes a working quality baseline for PROJ-014-style research synthesis (first-pass 0.837, final 0.952, 4 iterations). If Phase 2 runs the n=30 pilot under the same negative-constraint governance and achieves comparable quality trajectory, this retrospective baseline provides a continuity reference. NEVER cite the retrospective comparison as a controlled test of framing effects.

---

### ST-7: Controlled Experiment Readiness

**Synthesis task:** Assess whether the pilot design (TASK-005) combined with the effectiveness framework (TASK-006) constitutes a sufficient experimental foundation for Phase 2 completion.

#### Readiness assessment

**Verdict: SUFFICIENT — subject to four BLOCKING prerequisite gates.**

**BLOCKING definition:** A BLOCKING prerequisite is a condition that MUST be COMPLETE before the pilot can launch. Treating any of P-001 through P-004 as parallel work (proceeding with pilot preparation while prerequisites are incomplete) is a protocol violation. The pilot MUST NOT launch until all four BLOCKING prerequisites are documented as COMPLETE by the Phase 5 lead.

**Sufficiency arguments:**

1. **Research question clarity:** TASK-005 formally bifurcates the research question into primary construct (hallucination rate) and secondary construct (behavioral compliance). This bifurcation is essential — the original 60% claim is about hallucination, not compliance, and the pilot design correctly elevates hallucination rate measurement to primary status. TASK-006's dimension framework is consistent with this bifurcation: D2 (Hallucination Prevention) and D1 (Constraint Adherence) are separate dimensions, not collapsed.

2. **Statistical design adequacy:** The McNemar power analysis (pilot power ≈ 0.17) is correctly calibrated for the pilot's purpose (π_d estimation, not directional confirmation). The GO/NO-GO criteria are now internally consistent (SR-004-i2 resolution). The sample size table is sensitivity-analyzed across the plausible π_d range (0.10–0.50). Multiple comparisons correction (Bonferroni-Holm) is pre-specified.

3. **Methodological safeguards:** Equivalence validation protocol (5 EC criteria, inter-rater requirement, kappa ≥ 0.80 at pair level), evaluator blinding protocol (vocabulary masking with extended circumlocution list, scrubbing validation), evaluator training protocol (n=10 calibration pairs, kappa ≥ 0.70 threshold) are all specified at sufficient operational detail for execution.

4. **Evidence grounding:** The 7-condition framework (C1 through C7) is grounded in the effectiveness hierarchy (AGREE-5) and the evidence-to-pilot generalizability bridge (TASK-005). Each pilot condition maps to at least one evidence item with a stated mechanism hypothesis. TASK-006 independently confirms the analytical justification for each condition.

5. **Contingency planning:** PG-003 in TASK-006 specifies the contingency path if Phase 2 is inconclusive. TASK-005 explicitly addresses the Phase 2 Inconclusive Scenario. Both deliverables treat inconclusiveness as a legitimate expected outcome, not a failure.

6. **Analytical backbone:** TASK-006's 12-level hierarchy and 5-dimension framework provide the analytical structure for organizing Phase 2 results. Phase 2 experiment outputs can be directly mapped into the hierarchy and dimension structure without additional framework construction.

**BLOCKING Prerequisite Gates (pilot MUST NOT launch until all four are COMPLETE):**

| Gate | Prerequisite | BLOCKING condition | Completion criterion | Fallback if unachievable | Owner | Timeline |
|------|-------------|-------------------|---------------------|--------------------------|-------|----------|
| P-001 | Model availability confirmation | BLOCKS: pilot cannot proceed without confirmed API access | Confirm Claude Sonnet, Claude Haiku, and one non-Anthropic model are API-accessible at experiment time | Substitute confirmed-available models; update C1–C7 condition specifications accordingly | Pilot Lead | T-4 weeks before pilot launch |
| P-002 | Pre-validated example pair pool | BLOCKS: pilot cannot proceed without validated pairs — this is the highest-risk prerequisite | 10 pre-validated matched pairs (2 per task category × 5 categories) approved by two independent raters with kappa ≥ 0.80 | If kappa < 0.80 after 2 revision cycles, escalate to research lead; pilot design may require modification | Evaluator Pool Manager | T-4 weeks before pilot launch (highest-risk: begin first) |
| P-003 | Evaluator recruitment and training | BLOCKS: pilot cannot proceed without trained evaluators | At least 2 evaluators trained and calibrated; kappa ≥ 0.70 on n=10 calibration pairs | If calibration fails after 2 training cycles, recruit additional evaluators | Phase 5 Orchestrator | T-2 weeks before pilot launch |
| P-004 | Output scrubbing validation | BLOCKS: pilot cannot proceed without validated blinding | Scrubbing procedure tested on 5 example outputs; evaluators cannot identify condition at better than chance | If blinding fails, revise circumlocution list and re-test before launch | Phase 5 Orchestrator | T-2 weeks before pilot launch |

**Source:** TASK-005, respective protocol sections. TASK-005 serves as the primary specification; this synthesis gate language makes the BLOCKING status operationally explicit.

**Insufficiency risks that Phase 5 must manage:**

- The hallucination measurement protocol requires human evaluators spending 10–15 minutes per output on source verification. At 180 outputs for the pilot (30 pairs × 2 conditions × 3 models), this is 30–45 researcher-hours. This is feasible but represents a non-trivial execution risk. Phase 5 must explicitly allocate this time before launch.
- The residual blinding limitation (vocabulary masking cannot eliminate all condition leakage from output structure) is a known, irreducible design constraint. Phase 5 must document this in the pilot report's threat-to-validity section.
- The equivalence validation protocol (P-002) requires pair construction work before the pilot. If pre-validated pairs cannot be constructed that meet all 5 EC criteria with kappa ≥ 0.80, the pilot cannot launch — this triggers the P-002 fallback path.

---

## L2: Full Evidence Tables and Matrices

### Cross-Reference Matrix: Key Claims Across All Four Source Documents

**Circularity caveat:** All "Internally agreed" labels below reflect consistency across four documents produced by the same research pipeline using the same evidence base. These are internal consistency findings, not independent corroboration. See Assumption U-004 (ST-3) for researcher circularity disclosure.

| Claim | synthesis.md (B1, R4) | supplemental-vendor-evidence.md (R4) | claim-validation.md (TASK-005, R4) | comparative-effectiveness.md (TASK-006, R5) | Pipeline-internal agreement |
|-------|----------------------|--------------------------------------|-------------------------------------|---------------------------------------------|-----------|
| 60% hallucination reduction claim is untested | AGREE-1: zero sources across 3 surveys | Not the primary focus; consistent with synthesis | "NULL FINDING: untested, not disproven" (L0) | "NO SUPPORT — UNTESTED" (confidence bounds) | INTERNALLY AGREED (4 pipeline-internal documents) |
| Blunt prohibition (rank 12) underperforms structured alternatives | AGREE-4: strong, all 3 surveys, T1/T3 | Consistent — VS-001 is at ranks 9–11, not 12 | E-AGN-B-001: HIGH confidence | HIGH confidence established (finding #1 in directional verdict) | INTERNALLY AGREED (4 pipeline-internal documents) |
| No controlled A/B comparison of positive vs. negative exists | AGREE-2: confirmed by all 3 surveys | Confirms gap; proposes to fill it | Absence of evidence section: CONFIRMED | UNTESTED verdict for ranks 9–11 | INTERNALLY AGREED (4 pipeline-internal documents) |
| Vendor self-practice uses negative framing in HARD tier | Not detailed in synthesis — supplemental addresses | VS-001–VS-004: 33 instances cataloged | E-FOR-B-004: MEDIUM-WEAK (observational) | D5 HIGH observational finding | INTERNALLY AGREED — observational fact only |
| Explanation for vendor divergence is contested | VS-002 context referenced | Three explanations, none established | VS-001 revealed preference framing noted | Explanations 1 and 2 are co-null hypotheses (I3 parsimony revision) | ALIGNED within pipeline |
| A-15 (DeCRIM): structured decomposition improves compliance | AGREE-5: cited in hierarchy rank 6 | Not detailed separately | E-FOR-B-002 (MEDIUM) | D1 MEDIUM supporting evidence | INTERNALLY AGREED (4 pipeline-internal documents) |
| A-23 (Barreto & Jana): negation accuracy improvement | AGREE-5: cited in hierarchy rank 5; "Most actionable finding for PROJ-014" | Not detailed separately | E-FOR-B-002 (MEDIUM-HIGH); EMNLP 2025 confirmed | D2 MEDIUM (I5 upgrade from LOW; T1 confirmed) | INTERNALLY AGREED — minor terminological variation ("MEDIUM-HIGH" vs. "MEDIUM"); combined label = MEDIUM per ST-2 rationale |
| Context compaction failure mode for negative framing | GAP-13: documented, I-28/I-32 | L2 re-injection context noted (OBSERVATION) | T-004: directional inversion possible; LOW confidence | T-004: directional inversion under deployment conditions; LOW | ALIGNED within pipeline |
| Structured negative vs. structured positive: UNTESTED | Identified as primary gap in AGREE-2 | Phase 2 experiment designed to address | ST-3 (finding T-003): primary Phase 2 gap | UNTESTED verdict, directional verdict item #5 | INTERNALLY AGREED (4 pipeline-internal documents) |
| Researcher circularity risk | Not explicitly stated in synthesis | L-2 explicitly disclosed; independent replication required | DA-006 acknowledgment; independence limitation noted | A-002: structural circularity, independent replication required | ALIGNED — both analysis documents explicitly flag this; synthesis.md does not (design difference, not conflict) |

### Confidence Reconciliation Matrix: Full Detail

| Construct | TASK-005 Label | TASK-006 Label | Combined label | Evidence basis | Action for downstream |
|-----------|---------------|----------------|----------------|----------------|----------------------|
| 60% hallucination reduction | NULL FINDING | LOW/UNTESTED | UNTESTED | Zero sources across 75 | NEVER cite as established or disproven |
| Blunt prohibition underperforms | HIGH (via AGREE-4) | HIGH | HIGH | T1 (A-20, A-15), T3 (A-19, A-31) | Treat as established; PG-001 unconditional |
| Structured techniques (ranks 5–6) improve negation accuracy | MEDIUM-HIGH | MEDIUM (I5) | MEDIUM (scoped: negation accuracy, not hallucination rate) — combined label adopts TASK-006 I5 calibration; operationalized scale defines MEDIUM as exactly 1 T1 study with no replication | T1 (A-23, EMNLP 2025 Findings confirmed) | Use with scope caveat; single study, no replication |
| Structured techniques (ranks 5–6) improve compliance | MEDIUM | MEDIUM | MEDIUM (scoped: compliance, not hallucination rate) | T1 (A-15, EMNLP 2024) | Use with scope caveat; compliance ≠ hallucination rate |
| Vendor self-practice pattern (observational) | MEDIUM-WEAK | HIGH observational | HIGH observational / LOW causal | T4, direct observation, 3 vendors (Anthropic primary: ~30 instances; OpenAI: C-6, C-7; LlamaIndex: C-11 — Anthropic-heavy concentration — see U-004) | State as observational fact; do not infer causation; note Anthropic concentration |
| Structured negative vs. structured positive (ranks 9–11) | UNTESTED | UNTESTED | UNTESTED | No controlled study | This is the Phase 2 experimental target |
| Quality gate results achievable under negative-constraint regime | LOW (confounded, D3) | LOW (D3 observational) | LOW | T5, session data, 5 confounds | Existence proof only; NEVER as directional comparison |
| Iteration efficiency under negative-constraint regime | LOW (confounded, D4) | LOW (D4 observational) | LOW | T5, 2 same-pipeline observations | Existence proof only; NEVER as directional comparison |
| Context compaction reversal risk | LOW | LOW | LOW | T4 (I-28, I-32), practitioner reports | Flag in all deployment guidance; test explicitly in Phase 2 multi-turn (U-003 Phase 5 constraint) |

### Downstream Phase Input Specifications (Complete)

#### Phase 3 (Taxonomy) complete specification

| Input | Source document | Section | Confidence | Downstream constraint |
|-------|----------------|---------|------------|----------------------|
| 12-level effectiveness hierarchy | synthesis.md AGREE-5; TASK-006 analytical backbone | Cross-cutting section | Narrative synthesis (internally validated, not externally) | Extend, do not replace; disclose origin; ANY modification MUST preserve C1–C7 pilot alignment |
| IG-002 taxonomy (Types 1–4) | supplemental-vendor-evidence.md | Evidence Category 1 (referenced in AGREE-5 context) | T4 (observational) | Distinguish Type 1 (studied) from Types 2–4 (understudied) |
| 7-condition framework | TASK-005 | Experimental Conditions table | Design document | Use as taxonomy organizing principle; preserve C1–C7 mapping |
| AGREE-4 finding (blunt prohibition unreliable) | synthesis.md AGREE-4; TASK-006 D1 | L1: Agreements | HIGH (T1 + T3 convergent) | Anchor taxonomy at rank 12 as evidence-weak |
| 9 cross-survey agreements | synthesis.md AGREE-1 through AGREE-9 | L1: Agreements section | HIGH (5 strong) to MEDIUM (4 moderate) | All 9 should appear in taxonomy scaffolding |

#### Phase 4 (Jerry Framework) complete specification

| Input | Source document | Section | Confidence | Downstream constraint |
|-------|----------------|---------|------------|----------------------|
| PG-001: NEVER use standalone blunt prohibition | TASK-006 | Practitioner Guidance | T1+T3, HIGH, unconditional | Apply immediately; not contingent on Phase 2 |
| PG-002: NEVER design constraint without specifying rank | TASK-006 | Practitioner Guidance | T1+T4, HIGH, unconditional | Apply to all Jerry Framework constraint documentation |
| PG-003: Pair enforcement-tier constraints with consequences | TASK-006 | Practitioner Guidance | T4 observational, MEDIUM — working practice, Phase 2 will validate causal contribution | Apply as working convention; reversible if Phase 2 finds null framing effect |
| PG-004: Test context compaction before deployment | TASK-006 | Practitioner Guidance | T4, unconditional by failure mode logic | Mandatory for all long-context deployments |
| PG-005: Prioritize enforcement architecture over framing optimization | TASK-006 | Practitioner Guidance | T3 (DSPy, C-13) + T4 (NeMo), unconditional investment allocation | Guides investment allocation decisions |
| VS-001–VS-004 (33-instance catalog) | supplemental-vendor-evidence.md | Evidence Category 1 | T4 observational (HIGH observational, LOW causal; Anthropic-heavy concentration) | Treat as production baseline, not validated standard; note Anthropic concentration |
| T-004 (context compaction failure mode) | TASK-006 | Technical Finding T-004 | LOW (T4 reports, no controlled test) | Document as deployment risk; include in Phase 4 testing plan |
| PG-003 contingency (null framing result) | TASK-006 | Practitioner Guidance, Phase 2 Inconclusive Scenario | Contingent | Phase 4 design MUST be reversible on vocabulary dimension |

#### Phase 5 (Implementation) complete specification

| Input | Source document | Section | Confidence | Downstream constraint |
|-------|----------------|---------|------------|----------------------|
| n=30 pilot design with McNemar test | TASK-005 | Controlled Experiment Pilot Design | Methodological (validated through 4 adversary iterations) | Execute pilot before full experiment; do not skip; all 4 BLOCKING gates must be COMPLETE |
| Equivalence validation protocol (5 EC criteria) | TASK-005 | Equivalence Validation Protocol | Methodological | kappa ≥ 0.80 at pair level required before pilot launch (BLOCKING gate P-002) |
| Evaluator blinding protocol (vocabulary masking + circumlocution list) | TASK-005 | Evaluator Blinding Protocol | Methodological | Scrubbing validation test required; document residual limitation (BLOCKING gate P-004) |
| Evaluator training protocol (n=10 calibration, kappa ≥ 0.70) | TASK-005 | Evaluator Training Protocol | Methodological | Training completion required before scoring begins (BLOCKING gate P-003) |
| GO/NO-GO criteria (primary calibration-based, secondary CI-based) | TASK-005 | Pilot Go/No-Go Criteria | Methodological (SR-004-i2 resolved) | Primary GO criterion governs; secondary is supplementary |
| Statistical power analysis (pilot ≈ 0.17; full ≈ n 268 for C2/C3) | TASK-005 | Statistical Power for All Conditions | Methodological | Do not treat pilot as directional confirmation; power = 0.17 |
| Model selection criteria (min 3 models, cross-vendor) | TASK-005 | Model Selection Criteria | Methodological | Confirm model availability before pilot launch (BLOCKING gate P-001) |
| PG-003 contingency for inconclusive Phase 2 | TASK-006 | Phase 2 Inconclusive Scenario | Contingent | Implementation plan must include inconclusive-result protocol |
| π_d sensitivity table | TASK-005 | Pilot Specifications | Methodological | Consult before committing to full experiment sample size; do not pre-register full design before pilot calibration |
| U-003: Context compaction deployment constraint | ST-3, this synthesis | Assumption U-003 | LOW (T4 failure mode) | Pilot MUST include multi-turn context compaction test conditions |

---

## Source Summary

| Source | Type | Quality Gate | Key Contribution | Patterns Contributed |
|--------|------|-------------|------------------|---------------------|
| `barrier-1/synthesis.md` (R4, 0.953 PASS) | Phase 1 synthesis | PASS | 75-source cross-survey; 9 agreements (AGREE-1–AGREE-9); 12-level hierarchy (AGREE-5); confirmed null finding on 60% claim | Unified evidence base; hierarchy backbone; AGREE-4 (blunt prohibition); AGREE-2 (controlled study gap) |
| `barrier-1/supplemental-vendor-evidence.md` (R4, 0.951 PASS) | Phase 1 supplemental | PASS | VS-001–VS-004 (33-instance catalog, Anthropic-heavy with OpenAI C-6, C-7 and LlamaIndex C-11 extension); three competing explanations for vendor divergence; EO-001–EO-003 session observations (T5: L2 re-injection as primary enforcement mechanism, adversary gates as constraint violation detection, vendor documentation style separation); IG-002 taxonomy | Vendor self-practice pattern; D5 HIGH observational evidence; researcher circularity disclosure; L2 re-injection observation |
| `phase-2/claim-validation.md` (R4, 0.959 PASS) | Phase 2 analysis | PASS | 38-item evidence catalog; null finding protection; retrospective A/B comparison (PROJ-014 vs. PROJ-007); n=30 pilot design with all adversary findings resolved (4 iterations, 16 Critical + 27 Major + 3 Minor) | ST-1 evidence-hierarchy mapping; ST-2 confidence reconciliation (claim labels); ST-6 retrospective synthesis; ST-7 pilot readiness assessment |
| `phase-2/comparative-effectiveness.md` (R5, 0.933 max-iter) | Phase 2 analysis | Max-iter (0.933) | 5-dimension analysis (D1–D5); operationalized confidence scale; 12-level hierarchy as analytical backbone; PG-001–PG-005 practitioner guidance (per-PG confidence tiers); A-23 T1 verification (I5); researcher circularity caveat (A-002) | ST-2 confidence reconciliation (dimension labels); ST-4 unified verdict; ST-5 PG-001–PG-005; ST-7 analytical framework sufficiency |

**Pipeline circularity note:** All four inputs were produced by the same Jerry adversary pipeline (ps-researcher, ps-analyst, ps-synthesizer, ps-critic within the same orchestration). Their quality scores (0.959, 0.933, 0.953, 0.951) were assigned by adv-scorer within the same system. Treating these scores as independent quality validation would be circular. The scores represent internal pipeline consistency checks, not independent peer review.

---

## Self-Review Checklist

> H-15 compliance: Self-review before presenting deliverable. Iteration history: I2 revision addresses 5 Critical + 19 Major + 12 Minor findings from adversary-synthesis-i1.md. Each checklist item reflects post-I2 state.

| Check | Status | Notes | I1→I2 revision |
|-------|--------|-------|----------------|
| No contradictions between TASK-005 and TASK-006 conclusions | PASS | One terminological variation ("MEDIUM-HIGH" vs. "MEDIUM" for A-23) documented and resolved in ST-2 with explicit rationale for combined label selection | SR-001-i1: Combined label rationale added to ST-2 and L2 matrix |
| All confidence levels internally consistent | PASS | Combined confidence labels use the operationalized scale from TASK-006; all MEDIUM claims are scoped; all UNTESTED claims are explicitly flagged | PM-001-i1/FM-001-i1: Per-PG confidence tags added in ST-4 |
| No overstating of evidence (no controlled evidence claimed where none exists) | PASS | ST-4 unified verdict explicitly states no directional verdict can be issued; hallucination rate reduction remains LOW/UNTESTED throughout; NEVER conflation of observational HIGH with causal HIGH | IN-001-i1: Caveats co-located with confident claims in ST-4 |
| Supplemental vendor evidence from barrier-1 incorporated | PASS | VS-001–VS-004 cited in ST-1 (hierarchy integration), ST-2 (D5 confidence), ST-5 (Phase 4 inputs), L2 cross-reference matrix, downstream specifications; EO-001–EO-003 session observations now integrated in ST-1 | CV-002-i1/FM-005-i1: EO-001–EO-003 added to ST-1 |
| Every major claim traceable to specific input artifact and section | PASS | All claims cite specific sections (AGREE-X, E-FOR-X, D1–D5, VS-00X, PG-00X, EO-00X) from the four mandatory input artifacts | SM-003-i1: U-003 cross-linked to Phase 5 deployment constraint in ST-3 and L2 |
| Null finding protection preserved | PASS | CRITICAL READING NOTE added to ST-4; null finding is described as "untested, not disproven" consistently; never cited as refutation | IN-004-i1: Null finding protection co-located with PG statements |
| Downstream constraints are negative (constraining, not positive recommendation) | PASS | All "NEVER" constraints for downstream phases use negative constraint framing per orchestration directive | FM-007-i1/DA-004-i1: Adversary gate verification requirements added to each phase in ST-5 |
| Researcher circularity risk disclosed | PASS | ST-3 Assumption U-001 through U-004 and ST-2 tension table explicitly carry forward circularity disclosure; agreement labels revised to "INTERNALLY AGREED" with circularity note | RT-001-i1/IN-002-i1/FM-003-i1: "UNANIMOUS" → "INTERNALLY AGREED" throughout |
| Supplemental vendor evidence not treated as inferior | PASS | VS-001–VS-004 treated as T4 HIGH observational evidence throughout; explicitly integrated into all relevant synthesis tasks; Anthropic concentration quantified | SR-002-i1: Anthropic/OpenAI/LlamaIndex vendor concentration quantified in U-004 |
| Absence of published evidence not treated as evidence of absence | PASS | Structural exclusion impact (SE-1–SE-5) and 30-40% coverage qualifier carried forward into ST-4 unified verdict | No change needed — already addressed in I1 |
| ST-7 prerequisites have explicit BLOCKING gate language, Owner, and Timeline | PASS | All four prerequisites have BLOCKING gates with completion criteria, fallback paths, Owner (role-based), and Timeline (relative to pilot launch) | PM-002-i1/FM-002-i1/FM-008-i1/IN-003-i1: BLOCKING gate language and structure added (I2); Owner and Timeline columns added (I3, R-001) |
| L2 agreement labels carry circularity caveat | PASS | "UNANIMOUS" replaced with "INTERNALLY AGREED (4 pipeline-internal documents)" throughout L2 matrix | RT-001-i1/IN-002-i1/CC-001-i1: Labels revised |
| L0 includes Key Imperatives Index | PASS | 10-entry NEVER imperatives table added to L0 for quick reference | SM-004-i1: NEVER constraint index created |

---

## Revision Log (I1→I2)

> Documents the resolution of all Critical and Major findings, and selected Minor findings, from adversary-synthesis-i1.md (I1 tournament score: 0.868 REVISE).

### Critical Finding Resolutions

| Finding ID | Original description | Resolution | Section(s) changed |
|-----------|---------------------|-----------|-------------------|
| IN-001-i1 | Extractable confident fragments (PG-001–PG-005) without co-located caveats | Added "CRITICAL READING NOTE" to ST-4 header; restructured ST-4 to co-locate confidence tier tags directly with each PG statement; each finding now includes Confidence, Evidence tier, Scope, and key caveat | ST-4 (full restructure) |
| PM-001-i1 / FM-001-i1 | PG-001–PG-005 treated uniformly as "unconditional" — confidence differentiation lost | Each PG now has explicit confidence tag: PG-001 [T1+T3, HIGH, unconditional], PG-002 [T1+T4, HIGH, unconditional], PG-003 [T4 observational, MEDIUM — working practice], PG-004 [T4, unconditional by failure mode logic], PG-005 [T3, unconditional investment allocation] | ST-4, L2 Phase 4 specification |
| PM-002-i1 / FM-002-i1 / FM-008-i1 | ST-7 prerequisites described as "What is needed" without BLOCKING gate language | ST-7 prerequisite table restructured to: (1) BLOCKING gate header, (2) explicit "pilot MUST NOT launch until all four are COMPLETE" statement, (3) Completion criterion and Fallback columns added for each gate | ST-7 (table restructured), ST-5 Phase 5 constraints, L2 Phase 5 specification |
| FM-007-i1 / DA-004-i1 | ST-5 NEVER constraints have no enforcement mechanism | Added explicit "Adversary gate verification requirement" subsection to each downstream phase in ST-5, specifying which NEVER constraints the downstream adversary MUST verify; also added to L2 phase specifications | ST-5 (all three phase sections), L2 Phase 3/4/5 specifications |

### Major Finding Resolutions

| Finding ID | Original description | Resolution | Section(s) changed |
|-----------|---------------------|-----------|-------------------|
| DA-001-i1 | Synthesis manufactures consensus — "aligned" claims from co-dependent documents | Added pipeline circularity note to L2 Source Summary; added note to ST-2 agreement labels; all "UNANIMOUS" → "INTERNALLY AGREED (4 pipeline-internal documents)" | ST-2, L2 cross-reference matrix, Source Summary |
| DA-002-i1 | Execution risk for prerequisites under-weighted | BLOCKING gate language added to ST-7 with explicit fallback paths for each gate (P-002 highest risk explicitly called out) | ST-7 |
| DA-004-i1 | Downstream NEVER constraints lack enforcement mechanism | See FM-007-i1 resolution above | ST-5 |
| PM-003-i1 | ST-6 retrospective table scannable as directional evidence | Added "SCANNING CAUTION" callout before ST-6 table; added "Confound verdict" column to the retrospective data table so confound analysis is co-located with each numerical row | ST-6 (table restructured with confound column) |
| PM-004-i1 | Assumption U-001 does not protect pilot condition alignment | Added explicit C1–C7 alignment constraint to U-001: "Any modification to the 12-level hierarchy MUST preserve the C1–C7 pilot condition alignment"; also added to Phase 3 constraints in ST-5 | ST-3 (U-001), ST-5 Phase 3 constraints |
| FM-001-i1 | PG confidence differentiation lost (RPN 144) | See PM-001-i1 resolution above | ST-4 |
| FM-006-i1 | ST-6 retrospective table-vs-narrative risk (RPN 120) | See PM-003-i1 resolution above | ST-6 |
| CC-003-i1 | Self-review checklist lacks iteration history | Checklist expanded with "I1→I2 revision" column documenting which finding each item addresses; iteration version reference in checklist header | Self-Review Checklist |
| RT-001-i1 | "UNANIMOUS" labels epistemically unjustified for pipeline-internal documents | All "UNANIMOUS" and "FULLY ALIGNED" labels revised to "INTERNALLY AGREED (4 pipeline-internal documents)" or "ALIGNED within pipeline"; circularity caveat added as table header note | L2 cross-reference matrix |
| RT-002-i1 | Circular quality assurance — same pipeline assesses inputs and synthesis | Pipeline circularity note added to Source Summary section | Source Summary |
| SR-001-i1 | A-23 combined label selection rationale missing from L2 | Explicit rationale added to ST-2 reconciliation matrix row: "combined label adopts TASK-006 I5 calibration; operationalized scale defines MEDIUM as exactly 1 T1 study with no replication" | ST-2, L2 confidence reconciliation matrix |
| SR-002-i1 | Assumption U-004 vendor concentration not quantified | U-004 revised to specify: Anthropic = primary VS-001 catalog source; OpenAI = C-6, C-7 (2 of 33 explicitly non-Anthropic); LlamaIndex = C-11; Anthropic-heavy concentration noted | ST-3 (U-004), L2 confidence matrix (vendor self-practice row) |
| IN-002-i1 | "UNANIMOUS" and "FULLY ALIGNED" labels enable misrepresentation | See RT-001-i1 resolution above | L2 cross-reference matrix |
| IN-003-i1 | Prerequisites have no owner or timeline | BLOCKING gate table adds "Completion criterion" and "Fallback if unachievable" columns; BLOCKING definition statement added to ST-7 header | ST-7 |
| SM-001-i1 | L0 does not open with highest-confidence actionable finding | L0 restructured: opens with "Three-Line Summary" presenting HIGH/MEDIUM/UNTESTED tiers first, then Key Imperatives Index, then narrative paragraph | L0 (restructured) |
| SM-002-i1 | ST-4 lacks explicit "Established findings" sub-section | ST-4 restructured into three explicit sub-sections: "Established findings (HIGH confidence)", "Provisional findings (MEDIUM confidence)", "Unconditional operational findings" | ST-4 (restructured) |
| FM-003-i1 | "UNANIMOUS" labels without circularity caveat (RPN 140) | See RT-001-i1 resolution; circularity caveat note added as matrix header | L2 cross-reference matrix |
| FM-004-i1 | Self-review checklist lacks iteration history (RPN 105) | See CC-003-i1 resolution above | Self-Review Checklist |

### Minor Finding Resolutions (selected)

| Finding ID | Original description | Resolution | Section(s) changed |
|-----------|---------------------|-----------|-------------------|
| CV-001-i1 | L0 "identical evidence tiers" technically inaccurate | Revised to "reconcilable confidence scales derived from the same evidence base using terminologically distinct but epistemically compatible scales" | L0 narrative |
| CV-002-i1 / FM-005-i1 | EO-001–EO-003 not referenced in synthesis body | EO-001–EO-003 session observations explicitly integrated into ST-1 vendor evidence integration section with T5 evidence label and scope note | ST-1, Source Summary |
| CV-003-i1 | L0 does not mention retrospective A/B comparison | L0 narrative now includes reference to retrospective comparison with confound caveat | L0 |
| SM-003-i1 | U-003 not cross-linked to Phase 5 deployment constraints | U-003 now includes explicit "Phase 5 deployment constraint" note; L2 Phase 5 specification includes U-003 as required input | ST-3 (U-003), L2 Phase 5 specification |
| SM-004-i1 | NEVER constraints not consolidated | Key Imperatives Index added to L0 with 10-entry table covering all major NEVER constraints | L0 |
| SR-005-i1 | L0 is a single 400-word paragraph | L0 restructured: Three-Line Summary, Key Imperatives Index, then Narrative Summary as distinct sub-sections | L0 |
| DA-003-i1 | Null finding emphasis may prime for inconclusive results | Noted in ST-4 that inconclusiveness is "a legitimate expected outcome, not a failure" while preserving scientific equipoise; the three-tier confidence structure ensures positive findings receive appropriate prominence | ST-4 (confidence tier structure) |

### Findings Not Resolved (with rationale)

| Finding ID | Original description | Why not resolved |
|-----------|---------------------|-----------------|
| RT-004-i1 | ST-7 "SUFFICIENT" verdict lacks external methods validation citation | The "SUFFICIENT" verdict reflects synthesis judgment, not external methods review. Resolving this would require external experimental design consultation that is outside the synthesis agent's scope; flagged for Phase 5 to obtain independent methods review of the pilot design. |
| CC-002-i1 | ST-7 "SUFFICIENT" lacks external methods citation (P-011) | Same as RT-004-i1 — noted as a limitation of pipeline-internal synthesis; no external review available at synthesis stage. |
| SR-004-i1 | ST-7 lacks formal sufficiency gap analysis | ST-7 now has explicit BLOCKING prerequisites with completion criteria and fallback paths; the formal gap analysis would require a methods expert not available in the current pipeline. Addressed by making prerequisites more operationally specific. |
| PM-005-i1 | Researcher circularity disclosed but not operationally blocked | Operational blocking of researcher circularity (e.g., requiring an independent replicator) is a project management decision outside the synthesis document's authority. Disclosure is strengthened throughout; operational mitigation requires a separate research protocol decision. |

---

## Revision Log (I2→I3)

> Documents the resolution of all findings from adversary-synthesis-i2.md (I2 score: 0.927 REVISE). Targeted sentence-level and table-column additions only — no structural rewrite.

### R-001 (Major — highest priority): ST-7 BLOCKING prerequisites — Owner and Timeline columns

| Finding | R-001: ST-7 BLOCKING gates had no Owner or Timeline assignments |
|---------|------|
| Scorer assessment | "Prerequisites without owners will be treated as someone else's problem." |
| Resolution | Added Owner and Timeline columns to the ST-7 BLOCKING prerequisite gates table for all four gates (P-001 through P-004). Owner assigned using role-based labels: P-001 = Pilot Lead (T-4 weeks); P-002 = Evaluator Pool Manager (T-4 weeks, highest-risk, begin first); P-003 = Phase 5 Orchestrator (T-2 weeks); P-004 = Phase 5 Orchestrator (T-2 weeks). |
| Section(s) changed | ST-7 BLOCKING prerequisite gates table |

### R-002 (Minor): ST-4 PG-003 conflation risk

| Finding | R-002: Structural proximity of PG-003 (T4) to Finding M-1 (A-23 T1) creates conflation risk |
|---------|------|
| Scorer assessment | "A downstream consumer reading the 'Provisional findings' sub-section will see A-23 T1 evidence and PG-003 as a continuous block, potentially treating PG-003 as T1-backed when it is T4-backed." |
| Resolution | Added a clearly demarcated blockquote separator between Finding M-1 (A-23 T1 basis) and PG-003 (T4 basis), explicitly stating: "PG-003 is NOT derived from A-23. A-23 supports Finding M-1 only. NEVER treat PG-003 as T1-backed." |
| Section(s) changed | ST-4, Provisional findings sub-section |

### R-003 (Minor): ST-5 adversary gate requirements — orchestration cross-link

| Finding | R-003: Adversary gate verification requirements in ST-5 are not linked to downstream orchestration plans |
|---------|------|
| Scorer assessment | "The downstream adversary gate check cannot be triggered by the synthesis document alone." |
| Resolution | Added one sentence to each of the three phase adversary gate verification requirement sections (Phase 3, Phase 4, Phase 5) specifying that the respective orchestration plan MUST import these constraints into its adversary selection plan (reference: adv-selector agent template). |
| Section(s) changed | ST-5, Phase 3 adversary gate requirement; ST-5, Phase 4 adversary gate requirement; ST-5, Phase 5 adversary gate requirement |

### R-004/RT-004-i1 traceability (Minor deferred — partially operationalized)

| Finding | RT-004-i1: "SUFFICIENT" verdict has no external methods validation; deferred traceability gap |
|---------|------|
| Scorer recommendation | "Add one row to ST-5 Phase 5 adversary gate requirements: 'Obtain and document independent methods review (RT-004-i1 deferred item)'" |
| Resolution | Added verification item (5) to the Phase 5 adversary gate requirement: obtain and document independent methods review of the n=30 pilot design from a researcher outside the PROJ-014 pipeline before pilot launch. Explicitly identified as the operationalized traceability path for RT-004-i1. |
| Section(s) changed | ST-5, Phase 5 adversary gate verification requirement |

### R-006 (Minor): Vendor distribution precision in L2 confidence reconciliation matrix

| Finding | R-006: "3+ vendors" overstates breadth — actual distribution is 3 vendors, Anthropic-heavy |
|---------|------|
| Scorer assessment | "'3+ vendors' implies more breadth than the actual distribution supports." |
| Resolution | Changed "3+ vendors (Anthropic-heavy concentration — see U-004)" to "3 vendors (Anthropic primary: ~30 instances; OpenAI: C-6, C-7; LlamaIndex: C-11 — Anthropic-heavy concentration — see U-004)" in the L2 confidence reconciliation matrix. |
| Section(s) changed | L2 Confidence Reconciliation Matrix, vendor self-practice pattern row |

---

*Synthesis Version: 3.0.0*
*Previous Version: 2.0.0 (I2)*
*Constitutional Compliance: P-003, P-020, P-022*
*Created: 2026-02-28 (I1)*
*Revised: 2026-02-28 (I2, I3)*
*Agent: ps-synthesizer (TASK-007, Barrier 2)*
*Quality threshold: >= 0.95 (C4, per orchestration directive)*
*I1 Score: 0.868 REVISE (adversary-synthesis-i1.md)*
*I2 Score: 0.927 REVISE (adversary-synthesis-i2.md)*
*Revision: I1→I2 addressing 5 Critical, 19 Major, 12 Minor findings*
*Revision: I2→I3 addressing R-001 (Major: ST-7 Owner/Timeline), R-002 (Minor: PG-003 conflation), R-003 (Minor: ST-5 orchestration cross-links), R-004/traceability (Minor: RT-004-i1 deferred gate), R-006 (Minor: vendor distribution precision)*
