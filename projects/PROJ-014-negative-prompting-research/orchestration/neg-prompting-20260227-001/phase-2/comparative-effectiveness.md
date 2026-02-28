# TASK-006: Comparative Effectiveness Analysis — Positive vs. Negative Prompting for LLM Behavioral Compliance

> ps-analyst | TASK-006 | PROJ-014 | Phase 2 | 2026-02-27 | **Iteration 5** (I1 score 0.743 REJECTED; I2 score 0.790 REJECTED; I3 score 0.893 REVISE; I4 score 0.930 REVISE; A-23 confirmed T1-verified per ACL Anthology 2025.findings-emnlp.761)
> Input 1: `barrier-1/synthesis.md` (R4, adversary gate 0.953 PASS, 75 unique sources)
> Input 2: `barrier-1/supplemental-vendor-evidence.md` (R4, adversary gate 0.951 PASS)
> Analysis type: Comparative effectiveness (5-dimension)
> Framework: 12-level effectiveness hierarchy from synthesis AGREE-5, mapped across all 5 dimensions
> Criticality: C4 — all conclusions cite evidence; uncertainty stated; no false balance

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Three-paragraph plain-language verdict — reconciled with synthesis directional verdict; circularity caveat added (I3) |
| [Confidence Scale Definition](#confidence-scale-definition) | Operationalized confidence criteria (FM-002-I1, highest RPN=392) |
| [Analysis Scope and Method](#analysis-scope-and-method) | What was analyzed, how, what limits interpretive reach; alternative frameworks justified (I3) |
| [Cross-Cutting: 12-Level Effectiveness Hierarchy](#cross-cutting-12-level-effectiveness-hierarchy) | Analytical backbone with validity disclosure, alternative frameworks enumerated (I3), and backup analytical frame |
| [Dimension 1: Constraint Adherence](#dimension-1-constraint-adherence) | Behavioral compliance under each framing |
| [Dimension 2: Hallucination Prevention](#dimension-2-hallucination-prevention) | Evidence for hallucination reduction; D2 LOW throughout (I3 downgrade); D2 partially upgraded to MEDIUM (negation accuracy) / LOW (60% claim) in I5 after A-23 T1 confirmation |
| [Dimension 3: Quality Gate Performance](#dimension-3-quality-gate-performance) | Quality scores achievable under each framing (OBSERVATIONAL — not directional) |
| [Dimension 4: Iteration Efficiency](#dimension-4-iteration-efficiency) | Revision cycles required to reach quality thresholds (OBSERVATIONAL — not directional) |
| [Dimension 5: Practitioner and Vendor Adoption](#dimension-5-practitioner-and-vendor-adoption) | Real-world adoption patterns for each framing; circularity caveat added (I3) |
| [Evidence Quality Matrix](#evidence-quality-matrix) | All evidence sources with tier and directional assignment (A-16 notice revised I3) |
| [L1: Technical Findings](#l1-technical-findings) | Technical analysis with evidence citations for engineers |
| [L2: Architectural Implications](#l2-architectural-implications) | Systemic patterns and strategic implications |
| [Synthesis and Directional Verdict](#synthesis-and-directional-verdict) | Cross-dimension verdict recalibrated; D2 partially upgraded in I5 (A-23 T1 confirmed; negation accuracy = MEDIUM; 60% claim = LOW/UNTESTED) |
| [Why Observational Evidence Does Not Replace Phase 2](#why-observational-evidence-does-not-replace-phase-2) | Explicit guard against Phase 2 abandonment misreading; fourth scenario added (I3) |
| [Practitioner Guidance Under Evidence Uncertainty](#practitioner-guidance-under-evidence-uncertainty) | Unconditional practitioner guidance; PG-003 contingency for inconclusive Phase 2 added (I3) |
| [Recommendations](#recommendations) | Actionable constraints tied to evidence |
| [Assumptions and Limitations](#assumptions-and-limitations) | Explicit disclosure of interpretive boundaries; parsimony analysis corrected (I3) |
| [Revision Log](#revision-log) | I1→I2→I3→I4→I5 finding resolution record |

---

## L0: Executive Summary

**I1 Contradiction Resolved (CC-001-I1 Critical):** The I1 executive summary stated the evidence "does NOT validate" the hypothesis and stopped there, while the Synthesis section produced a directional verdict. These are not contradictory claims — but their separation across the document created a false impression. This I3 summary reconciles both in one place.

The evidence across five comparative dimensions does NOT validate the PROJ-014 working hypothesis that negative prompting reduces hallucination by 60%. No controlled study has tested this specific claim across any of the 75 sources surveyed. What the evidence does establish — with confidence levels specified against the operationalized scale in the next section — is a specific and bounded directional finding: blunt standalone prohibition (rank 12) is demonstrably less effective than structured alternatives. Specific structured negative techniques at ranks 5–6 show MEDIUM-confidence directional improvement in negation-related accuracy (D2 partially upgraded in I5 — A-23 is now confirmed T1-verified: Barreto & Jana, EMNLP 2025 Findings, https://aclanthology.org/2025.findings-emnlp.761; however, A-23 measures negation reasoning accuracy, not hallucination rate directly — see Dimension 2 for scope of the upgrade). The 60% hallucination reduction claim remains UNTESTED. Whether structured negative constraints at ranks 9–11 outperform structurally equivalent positive instructions on matched tasks is UNTESTED. A directional verdict favoring negative framing across all five dimensions cannot be issued from the available evidence because three of five dimensions produce only LOW-confidence findings. The analysis does NOT conclude that negative prompting is superior to positive prompting.

What the evidence does permit — with transparency about its evidential limits — is a conditional directional signal: vendors who build safety-critical behavioral enforcement systems (Anthropic, OpenAI, LlamaIndex) consistently choose negative framing for their HARD enforcement tier constraints while recommending positive framing for general users. This is a HIGH-confidence observational finding (T4, directly verifiable). **Critical structural caveat visible here (see Assumption A-002 for full disclosure):** The researcher who evaluated this vendor evidence is the same researcher who designed the PROJ-014 research program using negative constraints in its governance — a structural circularity that cannot be resolved by disclaimer and requires independent replication before the vendor evidence interpretation is relied upon. The most parsimonious explanations include audience-differentiated communication (Explanation 1, null hypothesis) and genre convention (Explanation 2, equally parsimonious under the corrected parsimony analysis in I3 — see Dimension 5). The engineering-discovery explanation (Explanation 3, hypothesis-supporting) is one of three competing accounts and is not established. The directional signal from vendor practice is real and warrants experimental investigation, but it does not constitute a verdict. Phase 2 experimental validation (270 matched pairs, McNemar test) is required before any directional claim can become a finding.

Practitioners who cannot wait for Phase 2 results are not without guidance: the T4 vendor self-practice evidence and the structured-technique findings together support unconditional recommendations for enforcement-tier design that do not depend on the framing question being resolved. These are documented in the [Practitioner Guidance Under Evidence Uncertainty](#practitioner-guidance-under-evidence-uncertainty) section. If Phase 2 produces inconclusive or mixed results (a common experimental outcome), PG-003 specifies the contingency path: continue with the paired-consequence vocabulary design as a convention-justified working practice while treating it as unvalidated for framing effectiveness. The Phase 2 experiment remains required to isolate framing from enforcement architecture as the active variable — but practitioners need not defer all action on that uncertainty, and they need not be without guidance if Phase 2 is inconclusive.

---

## Confidence Scale Definition

**FM-002-I1 Critical Resolution — Highest FMEA RPN (392):** All confidence labels in this analysis are operationalized against the following scale. Labels used without this scale are uninterpretable to downstream practitioners.

| Label | Definition | Conditions |
|-------|-----------|------------|
| **HIGH** | Consistent directional evidence from 2+ independent T1 or T2 studies, OR 1 T1/T2 study + consistent corroborating T4 evidence from 3+ independent vendors | Reader can rely on this finding as established |
| **MEDIUM** | Directional support from exactly 1 T1 or T2 study with no replication, OR consistent T4 evidence from 3+ independent vendors with no T1/T2 study | Reader should treat as provisional; independent replication needed |
| **LOW** | T3-only evidence (arXiv, unreviewed), OR observational session data with 3+ uncontrolled confounds, OR single-source T4 with no corroboration | Reader should treat as a hypothesis, not a finding |
| **UNTESTED** | No controlled comparison exists; claim has neither been confirmed nor refuted | Reader should not treat the absence of refutation as confirmation |

**Application of the scale to existing dimension labels:**

| Dimension | I2 label | I3/I4 label | I5 label | Rationale for changes |
|-----------|----------|-------------|----------|-----------------------|
| D1: Constraint Adherence | MEDIUM | MEDIUM | MEDIUM | No change. 1 T1 study (A-15, confirmed) + consistent T4 from 3+ vendors — scale definition satisfied |
| D2: Hallucination Prevention | LOW for 60% claim; MEDIUM for structured vs. blunt | **LOW throughout (I3 downgrade)** | **MEDIUM for negation accuracy; LOW for 60% claim** | **I3 change:** A-23 was T1-unverified; all D2 claims downgraded to LOW throughout (DA-001-I2, CV-001-I2, FM-001-I2). **I5 change (A23-V-001-I5):** A-23 (Barreto & Jana, EMNLP 2025 Findings, https://aclanthology.org/2025.findings-emnlp.761) now confirmed T1-verified. MEDIUM threshold satisfied for A-23's outcome (negation reasoning accuracy). Scope constraint: A-23 measures negation comprehension (understanding "not X"), NOT hallucination rate. D2 MEDIUM applies to negation accuracy only; 60% hallucination claim remains LOW/UNTESTED. |
| D3: Quality Gate Performance | LOW (causal) / LOW (observational) | LOW (causal) / LOW (observational) | LOW | No change. Session data with 5 confirmed confounds = LOW per scale. |
| D4: Iteration Efficiency | LOW | LOW | LOW | No change. Session data, no controlled baseline. |
| D5: Vendor Adoption Pattern | HIGH (observational) | HIGH (observational) | HIGH | No change. Direct T4 observation, consistent across 3+ independent vendors. Causal explanation remains contested. |

---

## Analysis Scope and Method

### Scope

This analysis compares positive prompting (instructing LLMs in what to do — "always cite sources," "respond concisely") against negative prompting (instructing LLMs in what to avoid — "NEVER state facts without sources," "MUST NOT spawn subagents") across five effectiveness dimensions for LLM behavioral compliance.

NEVER treated as out-of-scope: vendor self-practice evidence from the supplemental report (VS-001 through VS-004) and session empirical observations (EO-001 through EO-003). These evidence categories are included alongside academic and industry evidence across all five dimensions.

### Method

Five analytical dimensions are drawn from the ORCHESTRATION_PLAN.md TASK-006 specification. For each dimension:

1. All relevant evidence from synthesis.md and supplemental-vendor-evidence.md is assembled
2. Evidence is assigned to tier (T1 = peer-reviewed, T2 = established venues, T3 = arXiv/unreviewed, T4 = vendor/practitioner docs, T5 = session observation/self-report)
3. Each piece of evidence is assigned a directional label: Supports Positive, Supports Negative, or Neutral/Mixed
4. The 12-level effectiveness hierarchy is used as the analytical backbone, mapping each dimension's findings to hierarchy positions
5. A per-dimension verdict with operationalized confidence level is stated
6. A cross-dimension synthesis verdict is produced

**Dimensions 3 and 4 are classified as OBSERVATIONAL, not directional.** This distinction is critical and is applied explicitly throughout this document. An observational finding demonstrates that an outcome is achievable under a given condition. It does NOT establish that the condition caused the outcome or that other conditions would produce different outcomes. NEVER interpret a Dimension 3 or 4 verdict as a directional claim about the relative effectiveness of positive vs. negative framing.

### Analytical Principles (NEVER Violated)

- NEVER dismiss vendor self-practice evidence as inferior to published recommendations
- NEVER treat absence of published evidence as evidence of absence — and apply this principle symmetrically: the absence of evidence that structured positive constraints fail at HARD enforcement tier is equally not evidence they succeed less than negative constraints (RT-004-I1)
- NEVER abandon the hypothesis that negative prompting outperforms positive prompting on the basis of literature alone
- NEVER use positive prompting framing in this analysis — all analytical framing uses negative constraint language
- NEVER omit the supplemental vendor evidence from dimension analyses

> **Analytical framing vs. epistemic scope (SR-003-I2 clarification):** The two principles above govern analytical expression and framing, not epistemological conclusions. This principle governs expression and analytical framing, not epistemological conclusion — null findings and positive-framing-favorable evidence are not suppressed. The constraint governs framing language, not epistemic conclusions. The analytical frame (negative constraint vocabulary) and the epistemic commitment (follow the evidence wherever it leads) are distinct: the former is a stylistic and methodological directive; the latter is a scientific requirement. A null Phase 2 result, a finding favorable to positive framing, or any other evidence-based outcome is reported as found, regardless of the framing directive.
- NEVER cite A-16 (Harada et al., rejected ICLR 2025): this source was excluded from all evidence assembly and is not represented in any dimension verdict

### Alternative Analytical Frameworks Considered (LJ-001-I2 Major resolution)

The 12-level effectiveness hierarchy (from synthesis AGREE-5) was selected as the analytical backbone for this document. Three alternative frameworks were considered and rejected:

**Alternative 1: Simple binary (positive vs. negative).**
The most straightforward framework collapses all prompting techniques into two categories: positive instructions and negative instructions. This is the framework implicitly used in the PROJ-014 working hypothesis.
- **Rejected because:** The binary treats "NEVER hallucinate" (rank 12, blunt prohibition) and "NEVER state facts without sources — consequence: adversary rejects as uncited" (rank 11, justified prohibition) as the same technique. This conflation erases the most important distinction in the evidence base — the distinction that AGREE-4 explicitly establishes. A framework that cannot distinguish rank-12 from rank-11 cannot explain why vendors simultaneously recommend against negative prompting (for rank 12) and use it themselves (at ranks 9–11).

**Alternative 2: Tier-based taxonomy (T1–T5 evidence tiers only).**
An evidence-tier framework organizes findings by source quality without imposing an ordinal effectiveness claim. This is a methodologically conservative choice — it makes no hierarchy claims and simply reports what each tier of evidence shows.
- **Rejected because:** The research question is comparative effectiveness, not source quality. An evidence-tier framework would produce a finding like "T1 evidence shows A-15's atomic decomposition improves compliance" with no basis for comparing that finding against T4 vendor practice. The dimension-based comparative structure (D1–D5) requires an analytical backbone that can organize diverse evidence types against a common effectiveness axis. A tier-only taxonomy cannot provide this.

**Alternative 3: Mechanism-based taxonomy (by enforcement mechanism, not effectiveness rank).**
A mechanism-based framework groups techniques by HOW they work: re-injection mechanisms, vocabulary prohibition mechanisms, consequence-pairing mechanisms, programmatic enforcement mechanisms. This framework is the most architecturally useful for engineering teams.
- **Rejected because:** The mechanism taxonomy cuts across the positive/negative distinction rather than enabling comparison of positive vs. negative framing within the same mechanism. The PROJ-014 research question is specifically about framing effects within mechanism classes. The 12-level hierarchy retains mechanism distinctions (rank 3 = programmatic; rank 9 = declarative behavioral negation; rank 11 = justified prohibition) while also organizing techniques along an effectiveness evidence axis. The mechanism taxonomy alone cannot answer whether negative vocabulary within the same enforcement mechanism outperforms positive vocabulary.

**Selection rationale for the 12-level hierarchy:** The hierarchy was selected because it is the only available framework that (a) distinguishes within the negative-framing space (ranks 5–12) at sufficient resolution to explain the vendor recommendation/practice divergence, (b) organizes both positive and negative techniques along an evidence-quality-informed effectiveness axis, and (c) is directly produced from the 75-source evidence base used in this analysis. Its primary limitation — that it is internally generated and not externally validated — is disclosed in the Hierarchy Validity Disclosure section. The backup analytical frame (3-group simplified taxonomy) is provided in case the 12-level hierarchy is subsequently found invalid. Meta-analytic pooling was not feasible given heterogeneous outcome measures (compliance rate, hallucination count, quality score) and non-comparable comparison conditions across studies.

---

## Cross-Cutting: 12-Level Effectiveness Hierarchy

The primary synthesis (AGREE-5) establishes a 12-level effectiveness hierarchy synthesized from all three surveys. This hierarchy is the analytical backbone for all five dimensions. Evidence from each dimension is mapped against it.

> **IMPORTANT scope note (RT-002-R2 fix from synthesis.md):** Ranks 1–4 require model access, training infrastructure, or engineering infrastructure. A prompt engineer CANNOT implement ranks 1–4. The primary comparison relevant to PROJ-014 is within ranks 5–12 (prompt-engineering-accessible). NEVER compare ranks 1–4 against 5–12 as if they were competing approaches at the same level.

### Hierarchy Validity Disclosure (SM-002-I1, RT-002-I1, PM-002-I1, IN-002-I1 — Major resolutions)

**The 12-level hierarchy is a narrative synthesis product.** It was produced by the PROJ-014 research pipeline in the immediately preceding stage (synthesis.md, AGREE-5) and passed an internal adversary gate (0.953). It has NOT been reviewed by independent prompting researchers and has NOT been validated by a controlled ranking study. Its use as an analytical backbone is warranted as an organizing framework — NEVER as an empirically validated ordinal ranking.

**Face validity:** The hierarchy correctly separates model-access-required techniques (ranks 1–4) from prompt-engineering-accessible techniques (ranks 5–12) based on implementation requirements. This separation is not contested. The ordinal positions within ranks 5–12 are based on narrative synthesis of evidence quality, not direct head-to-head empirical comparison.

**Construct validity limitation:** No study directly compares rank-5 techniques against rank-8 techniques in controlled conditions. The ordinal positions within the hierarchy reflect the research team's best synthesis judgment from 75 sources — they are not empirically established differences.

**Falsifiability condition (IN-002-I1):** This hierarchy would be revised if: (a) a controlled study finds no statistically significant difference between techniques at different ranks, suggesting ordinal positions are not empirically supported; or (b) an independent meta-analysis produces a substantially different rank ordering. Until such evidence exists, the hierarchy is adopted as a working framework with acknowledged construct validity limitations.

### Backup Analytical Frame (PM-002-I1, FM-001-I1 — Critical/Major resolutions)

**If the 12-level hierarchy is subsequently found invalid as an analytical framework, the following simplified taxonomy retains the analysis's core findings:**

| Group | Techniques | Evidence | Directional | Confidence |
|-------|-----------|---------|-------------|------------|
| Structured techniques — ranks 5–6 (T1/T3 supported) | Warning-based meta-prompts (rank 5), atomic decomposition (rank 6) | T1: A-15 (compliance); T1: A-23 (negation accuracy, confirmed EMNLP 2025 Findings); T3: A-11 | Outperform blunt prohibition | MEDIUM for compliance (A-15 confirmed); MEDIUM for negation accuracy (A-23 now T1-verified; scope: negation reasoning, not hallucination rate directly); LOW for hallucination rate reduction specifically |
| Structured techniques — ranks 9–11 (T4 only) | Declarative behavioral negation, paired prohibition, justified prohibition | T4: vendor practice (VS-001–VS-004) | Observationally adopted in production; no controlled comparison vs. blunt prohibition or positive equivalents | LOW (observational, no controlled T1/T2 evidence) |
| Blunt prohibition | Rank 12 | T1: A-20; T3: A-31, A-19 | Underperforms structured alternatives | HIGH |
| Structured negative vs. structured positive | Within ranks 5–11 | NO CONTROLLED EVIDENCE | UNTESTED | — |

**(SM-001-I2 Major resolution — I3):** The backup frame now acknowledges the evidence differential between ranks 5–6 (T1/T3 evidence) and ranks 9–11 (T4 only). The core finding — structured techniques outperform blunt prohibition — survives hierarchy invalidation, but at different confidence levels for different rank groups.

**Under this simplified taxonomy, the analysis reduces to:** ranks 5–6 structured techniques outperform blunt prohibition with MEDIUM confidence for compliance outcomes and LOW confidence for hallucination-specific claims; ranks 9–11 structured techniques are observationally adopted by vendors but lack controlled T1/T2 evidence. Whether negative framing within structured techniques is superior to positive framing within structured techniques remains UNTESTED under either framework.

| Rank | Technique | Evidence Tier | Access Level | Directional Assignment |
|------|-----------|---------------|-------------|----------------------|
| 1 | Model-internal interventions (CAST, A-28) | T1 (ICLR 2025) | Model access required | NEITHER — out of PROJ-014 scope |
| 2 | Training-time negative constraints (Constitutional AI, A-10) | T3 (arXiv) | Training access required | NEITHER — inference-time only |
| 3 | Programmatic enforcement (DSPy, I-21/C-13) | T3 (preprint), T4 (docs) | Engineering infrastructure | Supports Negative (structured constraints) |
| 4 | Verification pipelines (CoVe, A-22) | T1 (ACL 2024) | Pipeline overhead | Neutral — orthogonal to framing question |
| 5 | Warning-based meta-prompts (A-23) | T1 (EMNLP 2025)* | Prompt-only | Supports Negative (meta-level prohibition) |
| 6 | Atomic constraint decomposition (DeCRIM, A-15) | T1 (EMNLP 2024) | Prompt-only | Supports Negative (structured) |
| 7 | ~~Negative emotional stimuli (NegativePrompt, A-1)~~ | REMOVED | — | REMOVED — different phenomenon, not behavioral constraint prompting (DA-004-I1) |
| 8 | Contrastive examples (Contrastive CoT, A-11) | T3 (arXiv) | Prompt-only | Neutral — pairing, not pure negative |
| 9 | Declarative behavioral negation (vendor practice) | T4 (vendor docs) | Prompt-only | Supports Negative (qualitative) |
| 10 | Paired prohibition + positive alternative (NP-002) | T4 (vendor docs) | Prompt-only | Supports Negative (qualitative) |
| 11 | Justified prohibition + contextual reason (NP-003) | T4 (vendor docs) | Prompt-only | Supports Negative (qualitative) |
| 12 | Standalone blunt prohibition ("NEVER X") | Multiple T1/T3 | Prompt-only | Supports Positive (negative performs worse here) |

> *A-23 (Barreto & Jana, EMNLP 2025): **I5 update — T1-VERIFIED.** Confirmed published in Findings of the Association for Computational Linguistics: EMNLP 2025. Full citation: "This is not a Disimprovement: Improving Negation Reasoning in Large Language Models via Prompt Engineering." ACL Anthology: https://aclanthology.org/2025.findings-emnlp.761. **Scope note:** A-23 measures negation reasoning accuracy — specifically whether warning-based and persona-based prompts improve LLM performance on distractor negation tasks (+25.14%). This is negation comprehension and reasoning accuracy, not hallucination rate (fabrication of false facts) directly. The T1 verification removes the prior access uncertainty but does not change the construct scope: readers should not interpret A-23's negation accuracy improvement as direct evidence for hallucination rate reduction. (Prior note: "No arXiv preprint ID or DOI was identified in the synthesis evidence catalog; EMNLP 2025 proceedings may require institutional access" — this limitation is resolved by the confirmed ACL Anthology entry.)

> **Note on rank 7 removal (DA-004-I1 Minor resolution):** NegativePrompt (A-1, IJCAI 2024) tests negative emotional stimuli — a different phenomenon from behavioral constraint prohibition prompting. Placing it in a constraint-effectiveness hierarchy was analytically incoherent. It is excluded from the hierarchy and addressed in the evidence matrix as a separate phenomenon.

**Key hierarchy insight for all dimensions:** The synthesis does NOT establish that all negative framing is superior to positive framing. It establishes that STRUCTURED negative constraints (ranks 5–11) outperform BLUNT standalone prohibition (rank 12) — and that the question of whether ranks 9–11 outperform well-constructed positive alternatives at the same structure level has not been tested in controlled conditions.

**Mechanism distinction critical for Dimension 5 (SM-001-I1 Major resolution):** Vendor practice (VS-001–VS-004) involves NEVER/MUST NOT vocabulary co-occurring with L2 re-injection at every prompt. These are two distinct mechanisms: (a) prohibitive vocabulary, and (b) re-injection frequency. The design choice to pair re-injection with prohibitive vocabulary — rather than re-inject positive equivalents — is itself an observational signal that practitioners believed vocabulary mattered beyond re-injection alone. Phase 2 Condition C4 (C2+re-injection vs. C3 positive+re-injection) is designed specifically to isolate vocabulary effect from re-injection frequency effect.

---

## Dimension 1: Constraint Adherence

**Research question:** How effectively does each framing achieve behavioral constraint compliance?

### Evidence Assembly

**Supporting negative framing for constraint adherence:**

| Evidence | Source | Tier | Key claim |
|----------|--------|------|-----------|
| 33 NEVER/MUST NOT instances in Anthropic's own Claude Code behavioral rules | VS-001 (supplemental) | T4 (direct observation) | Vendor chose negative framing for ALL HARD-tier enforcement constraints |
| HARD tier vocabulary explicitly defined as prohibitive (MUST, SHALL, NEVER, FORBIDDEN) | VS-003 (supplemental) | T4 (observation) | The tier with highest enforcement is defined by negative vocabulary |
| Constitutional triplet (P-003/P-020/P-022) expressed as prohibitions | VS-004 (supplemental) | T4 (observation) | Most safety-critical constraints expressed as negative constraints |
| Zero constraint violations in 4-iteration C4 tournament under negative-constraint regime | EO-002 (supplemental) | T5 (session, confounded) | Observational; confounded by quality gate, specialized agents; verifiable at `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/barrier-1/adversary-gate.md` |
| Instruction hierarchy failure documented even for positive framing | A-20 (synthesis, AGREE-4) | T1 (AAAI 2026) | System/user separation fails; both positive and negative framing are unreliable at level 12 |
| GPT-4 fails >21% of constraints even with standard instruction | A-15 (synthesis, AGREE-5) | T1 (EMNLP 2024) | Compliance failures are a baseline reality under any framing |
| NEVER rules prone to being dropped during context compaction | I-28, I-32 (synthesis, GAP-13) | T4 (practitioner, Claude Code GitHub issue reports) | Negative framing suffers specific failure mode in long-context sessions; context compaction adversely affects prohibitive vocabulary |

**Supporting positive framing for constraint adherence:**

| Evidence | Source | Tier | Key claim |
|----------|--------|------|-----------|
| Anthropic published recommendation: "Tell Claude what to do, not what not to do" | I-1/C-1 (synthesis, AGREE-3) | T4 (vendor docs) | Major vendor recommends positive framing |
| OpenAI recommendation: positive over negative | I-3/C-3 (synthesis, AGREE-3) | T4 (vendor docs) | Second major vendor recommends positive framing |
| Google recommendation: positive over negative | I-6 (synthesis, AGREE-3) | T4 (vendor docs) | Third major vendor recommends positive framing |
| Affirmative directives outperform prohibition at rank 12 on [specific tasks]: approximately 55% improvement | A-31 (synthesis, AGREE-4) | T3 (arXiv) | Note: A-31 compares rank-12 blunt prohibition against affirmative framing on a multi-principle study (Bsharat et al. 2023, "Principled Instructions Are All You Need"). The 55% figure applies to specific task/model combinations in a 26-principle study and does NOT control for instruction quality equivalence across conditions. Generalization is limited (CV-001-I1 Critical resolution). |
| Avoiding negative phrasing "significantly improves results" | I-12 (synthesis, AGREE-4) | T4 (blog, tested) | DreamHost systematic testing (methodology not disclosed) |

**Neutral/mixed evidence:**

| Evidence | Source | Tier | Key claim |
|----------|--------|------|-----------|
| VS-002: Recommendation/practice divergence has three competing explanations | VS-002 (supplemental) | T4 + inference | Three explanations enumerated; none established |
| AGREE-9: Contextual justification improves negative instruction effectiveness | synthesis | T1/T4 | Negative framing works better when justified — neither pure positive nor pure negative |
| AGREE-8: Paired negative + positive outperforms either standalone | synthesis | T3/T4 | Best approach is hybrid |
| 660–1,330 violations per 600 samples across 13 models | A-19 (synthesis, AGREE-4) | T3 (large-scale) | Widespread violation regardless of framing — compliance is broken at rank 12 |

### Reflexivity Impact Assessment (FM-004-I1 Minor resolution)

**JF-001 (Jerry Framework uses negative constraints) is T5 with high reflexivity risk.** This evidence was removed from the D1 supporting evidence table above. With JF-001 removed, the D1 directional finding REMAINS STABLE: VS-001–VS-004 (T4 direct observation of Anthropic's production system, authored by Anthropic engineers — NOT by this researcher) and A-15 (T1, EMNLP 2024) provide the primary supporting evidence. JF-001's removal does not change the D1 verdict. JF-002 (PLAN.md 12 negative constraints) is similarly T5 with circular risk; it is omitted from D1 evidence and appears only in D5 as a practitioner self-report with explicit circular risk annotation.

### Hierarchy Mapping — Dimension 1

The vendor self-practice evidence (VS-001 through VS-004) positions negative constraint framing specifically at ranks 9–11 (declarative behavioral negation, paired prohibition, justified prohibition) in the effectiveness hierarchy — NOT at rank 12 (standalone blunt prohibition). The published vendor recommendations against negative framing are clearly directed at rank 12 usage patterns.

The critical distinction: NEVER/MUST NOT in Anthropic's own production rules are not the same as "NEVER hallucinate" in a user's prompt. They are paired with consequences (NC-006: "Command fails. Environment corruption."), expressed in structured HARD/MEDIUM/SOFT tiers, and re-injected at every prompt via L2-REINJECT markers. This positions vendor self-practice at ranks 9–11, not rank 12.

### Dimension 1 Verdict

**MEDIUM confidence.** Structured negative constraints at ranks 9–11 show stronger evidence of behavioral compliance for safety-critical and precision-critical enforcement than standalone positive instructions. This is supported by Anthropic's own engineering practice (VS-001–VS-004, T4), A-15 (T1, EMNLP 2024 — atomic decomposition improves compliance +7.3–8.0%), and the session empirical observation (EO-002, T5, confounded).

**Critical caveat:** No controlled study compares matched structured-negative vs. structured-positive constraint formulations at ranks 9–11. The A-31 finding (affirmative directives outperform prohibitions by approximately 55%) compares rank-12 prohibition against positive framing on specific tasks in a multi-principle study — it does NOT compare ranks 9–11 structured negative against positive equivalents. This distinction is analytically critical and must not be collapsed.

**Context compaction exception:** Under long-context deployment conditions with context compaction, the D1 directional finding may be reversed. Finding T-004 documents that NEVER/DO NOT rules lose their imperative force during context compaction (I-28, I-32). NEVER treat the D1 MEDIUM-confidence verdict as applicable to long-context deployments without Phase 2 multi-turn testing. **Confidence for the "context compaction may reverse D1" claim: LOW (DA-003-I2 Minor resolution).** The evidence for this failure mode is T4 (I-28, I-32: practitioner-reported bug observations from Anthropic's GitHub, no controlled experimental confirmation). The claim that this reversal applies to negative constraint framing specifically — rather than to any long instruction across framing types — is plausible but untested. UNTESTED for the directional comparison: whether positive framing is more robust to context compaction than negative framing has not been controlled.

---

## Dimension 2: Hallucination Prevention

**Research question:** What evidence exists for hallucination reduction under each framing?

### Evidence Assembly

**Supporting negative framing for hallucination prevention:**

| Evidence | Source | Tier | Key claim |
|----------|--------|------|-----------|
| Warning-based and persona-based prompts: +25.14% distractor negation accuracy | A-23 (synthesis, AGREE-5) | T1 (EMNLP 2025 Findings, confirmed; https://aclanthology.org/2025.findings-emnlp.761) | Meta-level negative warning improves negation reasoning accuracy; single study; outcome measure is negation comprehension accuracy, not hallucination rate directly; replication needed |
| Contrastive CoT (invalid + valid examples): +16 Bamboogle, +9.8 GSM-8K | A-11 (synthesis, AGREE-5) | T3 (arXiv) | Contrastive approach outperforms pure-positive on reasoning; T3 evidence |
| Atomic decomposition: +7.3–8.0% compliance | A-15 (synthesis, AGREE-5) | T1 (EMNLP 2024) | Decomposed negative constraints outperform compound instruction; Tier 1 |
| EO-003: "Never state facts without sources" associated with zero unsourced claims | EO-003 (supplemental) | T5 (session, confounded) | Observational; multiple confounds present; cannot isolate framing effect; source at `barrier-1/supplemental-vendor-evidence.md` |

**Supporting positive framing for hallucination prevention:**

| Evidence | Source | Tier | Key claim |
|----------|--------|------|-----------|
| Negation instructions increased hallucination: LLaMA-2 26%→59% in MCQA | A-6 (synthesis, AGREE-6) | T3 (arXiv, not replicated) | Direction: negative framing worsens hallucination in specific MCQA contexts; scope: one model family, four tasks, 100–300 instances |
| Negative prompts reduce factual accuracy by 8.4% (92.3%→84.5%) | A-14 (synthesis, CONFLICT-3) | T3 (commercially affiliated) | Measures emotional/sentiment negativity, not prohibition syntax; measurement phenomenon may not be the same as negative constraint prompting |
| CoVe verification pipeline doubles precision | A-22 (synthesis, AGREE-5) | T1 (ACL 2024) | Verification outperforms linguistic framing; orthogonal to positive/negative question |

**Neutral/mixed evidence:**

| Evidence | Source | Tier | Key claim |
|----------|--------|------|-----------|
| AGREE-1: Zero sources validate the 60% hallucination reduction claim | All 3 surveys | T1–T4 | Confirmed null finding; hypothesis is untested, not refuted |
| AGREE-4: Prohibition-style instructions unreliable as standalone mechanisms | All 3 surveys | T1 (A-20), T3 (A-19, A-31) | Blunt prohibition (rank 12) FAILS; says nothing about structured negative (ranks 9–11) |
| AGREE-7: Compliance and accuracy are independent capabilities | A-19, C-19 | T3 | High compliance does not guarantee low hallucination rate — both must be measured |
| IG-002: Published studies test naive prohibition; structured enforcement is understudied | supplemental | Interpretive | Explains why evidence is sparse at ranks 9–11; not evidence itself |

### Hierarchy Mapping — Dimension 2

The evidence on hallucination prevention is most directly concentrated at ranks 5–6 in the hierarchy (warning-based meta-prompts and atomic decomposition). A-15 (EMNLP 2024) provides T1 evidence on atomic decomposition and compliance improvement — but its primary outcome measure is constraint adherence, not hallucination prevention specifically. A-23 (Barreto & Jana, EMNLP 2025 Findings — now confirmed T1-verified; https://aclanthology.org/2025.findings-emnlp.761) is confirmed published and provides T1 evidence for warning-based and persona-based prompts improving negation reasoning accuracy (+25.14% on distractor negation tasks). **Critical scope note:** A-23 measures negation comprehension accuracy — correctly interpreting and reasoning about negated premises — not hallucination rate (fabrication of false facts) directly. Improved negation reasoning accuracy is related to but not the same construct as hallucination prevention. The NTAS (Negative Token Attention Score) correlation A-23 reports reflects attention to negation tokens, which is relevant to how models process constraints, but the paper does not report hallucination rate outcomes. The A-6 finding (hallucination increase from negation) applies specifically to rank 12 (standalone blunt prohibition in MCQA contexts on LLaMA-2).

The synthesis explicitly distinguishes the PROJ-014 working hypothesis (60% hallucination reduction from negative prompting) from the A-6 finding (hallucination increases with naive negation). These are different claims about different phenomena. The A-6 finding does not refute the PROJ-014 hypothesis; it documents a specific failure mode of rank-12 prompting on one model family.

### Dimension 2 Verdict (DA-001-I2, CV-001-I2, FM-001-I2 Major resolutions — I3 downgrade; A23-V-001-I5 partial upgrade)

**I3 CHANGE:** D2 was downgraded to LOW throughout. The I2 deliverable claimed MEDIUM confidence for "structured techniques vs. blunt prohibition" based on A-23 as a T1 study. However, A-23 was T1-unverified (no arXiv preprint ID or DOI identified in the synthesis evidence catalog). The confidence scale requires "exactly 1 T1 or T2 study" for MEDIUM. A T1-unverified source could not satisfy this criterion.

**I5 CHANGE (A23-V-001-I5):** A-23 (Barreto & Jana) is now confirmed T1-verified: published in Findings of the Association for Computational Linguistics: EMNLP 2025 (https://aclanthology.org/2025.findings-emnlp.761). The access barrier is removed. However, the upgrade to D2 confidence is partial and carefully scoped — see below.

**LOW for the 60% claim (UNTESTED — zero sources; see confidence scale).** No controlled study exists. A-23's confirmation does not change this — A-23 does not test the 60% hallucination reduction claim.

**MEDIUM for structured negative techniques improving negation reasoning accuracy (I5 upgrade, scoped).** A-23 (T1, confirmed) provides evidence that warning-based and persona-based prompts improve negation reasoning accuracy by up to +25.14% on distractor negation tasks. This satisfies the MEDIUM threshold ("exactly 1 T1 study"). The MEDIUM confidence applies to the specific outcome A-23 measures: LLMs' ability to correctly comprehend and reason about negated statements. This is a legitimate behavioral improvement from structured negative prompting — and an LLM that correctly handles negation is plausibly less prone to confabulation in negation contexts — but the construct measured is negation comprehension, not hallucination rate (fabrication of false facts) directly. Readers MUST NOT interpret this MEDIUM as applying to hallucination rate reduction.

**LOW for hallucination rate reduction specifically (structured techniques vs. blunt prohibition).** A-15 (T1, EMNLP 2024) provides confirmed T1 evidence for compliance improvement (+7.3–8.0%) but its primary outcome measure is constraint adherence, not hallucination reduction. A-23 (now T1-confirmed) measures negation reasoning accuracy, not hallucination rate. T3 evidence (A-11, contrastive CoT: +16 Bamboogle, +9.8 GSM-8K) supports the directional claim but at LOW confidence. The directional claim that structured techniques at ranks 5–6 reduce hallucination rate more than blunt prohibition remains plausible and warrants Phase 2 investigation, but no T1 study directly measures hallucination rate reduction from structured negative constraints.

**UNTESTED for ranks 9–11 vs. structured positive.** Whether structured negative techniques outperform equivalently well-constructed positive instructions has not been tested in controlled conditions at any rank.

The only evidence of negative framing worsening hallucination (A-6) is T3, unreplicated, and applies to rank 12 prompting on LLaMA-2 in MCQA contexts.

---

## Dimension 3: Quality Gate Performance

**Research question:** What quality gate scores are achievable under each framing, and what does the evidence show?

> **OBSERVATIONAL FINDING — NOT DIRECTIONAL (DA-003-I1, FM-003-I1 Critical/Major resolutions):** Dimensions 3 and 4 contain existence-proof observations, not directional comparisons. An existence proof demonstrates that an outcome is achievable under a given condition. It does not compare that outcome against an alternative condition. The headers in this section use "Observational Note" rather than "Directional Finding" to reflect this distinction.

### Evidence Assembly

**Session observations under negative-constraint regime:**

| Evidence | Source | Tier | Key claim |
|----------|--------|------|-----------|
| PROJ-014 synthesis scored 0.953 (C4 threshold 0.95) under negative-constraint regime | EO-001 (supplemental) | T5 (session observation) | Monotonic improvement across 4 iterations; zero regression; confounded; verifiable at `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/barrier-1/adversary-gate.md` |
| PROJ-014 supplemental vendor evidence scored 0.951 (C4 threshold 0.95) | EO-001 cross-ref (supplemental) | T5 (session observation) | Same negative-constraint regime; same confounds |
| PLAN.md 12 negative constraints — all honored throughout the session | EO-002 (supplemental) | T5 (session observation) | Zero constraint violations under negative-constraint prompting |
| Score trajectory shows monotonic improvement (0.83→0.90→0.93→0.953) | `barrier-1/adversary-gate.md` | T5 (session observation) | All 3 Critical findings resolved by I2 (first revision); rapid convergence |

**Confound table — MANDATORY reading before interpreting D3 observations:**

| Confound | Description | Eliminability |
|---------|-------------|---------------|
| C4 quality gate mechanism | Adversary tournament enforces improvement regardless of framing | Not eliminable in session data |
| Specialized agents (ps-researcher, ps-analyst, ps-synthesizer) | Domain-specific agents improve output independently | Not eliminable in session data |
| Structured templates (.context/templates/adversarial/) | Templates enforce quality structure regardless of framing | Not eliminable in session data |
| Researcher expertise | Expert prompt engineering produces better output regardless of framing | Not eliminable in session data |
| External source verification requirements (Context7, WebSearch) | Source constraints produce sourced output regardless of framing | Not eliminable in session data |

**Baseline comparison data:**

The supplemental report explicitly states: "No matched positive-framing session on the same task exists for comparison." NEVER treat the D3 observations as a comparison between positive and negative framing.

### Hierarchy Mapping — Dimension 3

The quality gate performance data maps to hierarchy position 9 (declarative behavioral negation in production) in terms of mechanism, but also heavily reflects the quality gate architecture itself (ranks 3–4 equivalent: programmatic enforcement via adversary tournament). The confound between the enforcement mechanism and the framing is inseparable in the session observations.

### Observational Note — Dimension 3

**C4 results are achievable under a negative-constraint prompting regime.** This is an existence proof. The PROJ-014 session produced two deliverables scoring 0.953 and 0.951 (C4 threshold 0.95) under a governance regime using negative constraint framing.

**What this observation CANNOT establish:**
- That negative framing caused the quality gate pass
- That positive framing would produce different results
- That the quality gate scores are higher than what positive framing would achieve

**Confidence for the observational claim (existence proof only): LOW.** Session data with 5 confirmed confounds, no controlled baseline. A single session is not replicable and cannot generalize. See Limitation L-001 in the Assumptions and Limitations section: this dimension's findings are explicitly bounded by the absence of any controlled comparison. (IN-002-I2 Minor resolution: cross-reference added.)

---

## Dimension 4: Iteration Efficiency

**Research question:** How many revision cycles does each framing require to converge on quality thresholds?

> **OBSERVATIONAL FINDING — NOT DIRECTIONAL (DA-003-I1, SR-001-I1 Critical/Major resolutions):** Same constraint applies as Dimension 3. NEVER label two same-pipeline session observations as "directional data." A direction requires at least two differently-conditioned observations on comparable tasks.

### Evidence Assembly

**PROJ-014 session data (negative-constraint regime):**

| Metric | Value | Source |
|--------|-------|--------|
| Iterations to C4 PASS (synthesis.md) | 4 iterations | `barrier-1/adversary-gate.md` |
| Iterations to C4 PASS (supplemental-vendor-evidence.md) | 4 iterations | `barrier-1/adversary-gate.md` |
| Score at I1 (synthesis) | 0.83 | `barrier-1/adversary-gate.md` |
| Score at I2 (synthesis) | 0.90 | `barrier-1/adversary-gate.md` |
| Critical findings resolved by I2 | 3 of 3 | `barrier-1/adversary-gate.md` |
| Score improvement at first revision | +0.07 (largest single jump) | `barrier-1/adversary-gate.md` |

**Comparative evidence (positive framing baseline):** NEVER available in controlled form. No matched positive-framing session exists.

**Broader evidence base on iteration efficiency:**

| Evidence | Source | Tier | Key claim |
|----------|--------|------|-----------|
| DSPy programmatic enforcement achieves 164% compliance improvement | C-13 (synthesis, rank 3) | T3 (arXiv) | Structural enforcement mechanisms — not framing — most powerfully affect iteration efficiency |
| Instruction compliance drops from ~95% to 20–60% over conversation length | I-17 (synthesis, GAP-5) | T4 (unverified practitioner estimate) | Long-context compliance degradation; treat as hypothesis only |
| No controlled comparison of iteration counts between positive and negative framing regimes exists | AGREE-2 (synthesis) | All surveys | This is a confirmed evidence gap |

### Observational Note — Dimension 4

**4 iterations to C4 PASS on two deliverables under negative-constraint prompting.** This is an observational record, not a directional comparison. Two same-pipeline deliverables with identical confounds are not independent observations and do not constitute a direction.

**What cannot be established:** Whether positive framing on the same tasks would require more or fewer iterations. The DSPy programmatic enforcement evidence (rank 3: 164% compliance improvement) suggests that structural enforcement mechanisms — not framing — most powerfully affect iteration efficiency. This is entirely consistent with the overall picture: the framing question may be subordinate to the enforcement architecture question.

**Confidence for the observational claim: LOW.** Two same-pipeline observations with no controlled baseline. See Limitation L-001 in the Assumptions and Limitations section: this dimension's findings are explicitly bounded by the absence of any controlled comparison. (IN-002-I2 Minor resolution: cross-reference added.)

---

## Dimension 5: Practitioner and Vendor Adoption

**Research question:** What are the real-world adoption patterns for each framing approach, and what does the weight of practitioner and vendor practice tell us?

### Evidence Assembly

**Vendor published recommendations (positive framing):**

| Evidence | Source | Tier | Claim |
|----------|--------|------|-------|
| Anthropic: "Tell Claude what to do instead of what not to do" | I-1/C-1 (synthesis, AGREE-3) | T4 (HIGH authority) | Explicit positive-framing preference for general use |
| OpenAI: "Instead of just saying what not to do, say what to do instead" | I-3/C-3 (synthesis, AGREE-3) | T4 (HIGH authority) | Same pattern across second major vendor |
| Google: "Use examples to show patterns to follow, not anti-patterns to avoid" | I-6 (synthesis, AGREE-3) | T4 (HIGH authority) | Third major vendor; same pattern |
| All three major platform vendors recommend positive framing | AGREE-3 (synthesis) | T4 | Three-vendor consensus on recommendation |
| Palantir takes a balanced approach; treats negatives as standard tools | I-19 (synthesis) | T4 | Enterprise vendor breaks from the consensus |

**Vendor practice (negative framing used in production):**

| Evidence | Source | Tier | Claim |
|----------|--------|------|-------|
| Anthropic: 33 NEVER/MUST NOT/DO NOT instances in production behavioral enforcement rules | VS-001 (supplemental) | T4 (direct observation, HIGH authority) | Vendor chose negative framing for ALL 33 HARD-tier enforcement constraints |
| Anthropic: NEVER/MUST NOT in their own Claude Code example prompts | CONFLICT-2, C-1 (synthesis) | T4 | Examples use negative constraints despite recommending positive |
| OpenAI GPT-5.2: "NEVER invent colors," "Do NOT invent colors" | C-7 (synthesis, GAP-14) | T4 (HIGH authority) | Current-generation model guidance uses explicit negative constraints |
| OpenAI GPT-5.1: "Do NOT guess...ask for detail" (paired negative-positive) | C-6 (synthesis) | T4 (HIGH authority) | Paired negative-positive pattern in official current-gen guidance |
| LlamaIndex default prompts: 6 negative instructions ("Never query all columns") | C-11 (synthesis, GAP-9) | T4 (source code, HIGH) | Framework production defaults use negative framing despite no guidance |

**Practitioner adoption evidence:**

| Evidence | Source | Tier | Claim |
|----------|--------|------|-------|
| JF-002: PLAN.md 12 negative constraints — all 12 constraints expressed as prohibitions | JF-002 (supplemental) | T5 (self-report, HIGH circular risk) | Researcher chose negative constraint framing for PROJ-014 governance |
| I-12 (DreamHost): avoiding negative phrasing "significantly improves results" | I-12 (synthesis) | T4 (tested, methodology undisclosed) | Practitioner systematic testing supports positive framing |
| I-29: Safety directives typically written as negatives | I-29 (synthesis) | T4 (blog) | Practitioner observation on safety-specific context |
| Blog practitioner consensus: positive framing preferred for general use | I-2, I-9, I-11, I-24, I-25 (synthesis) | T4 | Practitioner literature skews toward positive recommendation |

> **Note on JF-001 removal (FM-004-I1):** JF-001 ("Jerry Framework uses negative constraints at HARD tier") is T5 self-report and was removed from D1 evidence. In D5, JF-002 is retained as practitioner adoption evidence but annotated with HIGH circular risk: the researcher who chose negative framing for PROJ-014 governance is the same researcher concluding that negative framing may be superior. This circular risk must NEVER be ignored when weighting JF-002.

### Parsimony Analysis for the Three Competing Explanations (DA-002-I1 Major resolution)

The supplemental report (VS-002) documents three explanations for the vendor recommendation/practice divergence. The I1 deliverable asserted Explanation 1 was "most parsimonious" without demonstrating this. A formal parsimony analysis follows.

**Explanation 1 (Audience differentiation):** General users get positive framing guidance because they apply negative prompting naively. Production enforcement tiers use prohibitions because precision and non-ambiguity matter.
- Auxiliary assumptions required: (a) vendors consciously chose different vocabulary for different audiences, (b) this differentiation is consistent across all 33 instances and 3 independent vendors, (c) the audience distinction maps to the recommendation/practice split.
- **Assumption count: 3**

**Explanation 2 (Genre convention):** NEVER/MUST NOT reflects policy and compliance document vocabulary conventions, not engineering discovery.
- Auxiliary assumptions required: (a) policy documents conventionally use prohibitive vocabulary — **(I3 revision, DA-002-I2, FM-003-I2 Major resolution):** this is an empirical claim that requires evidence. Legal, compliance, and safety policy documents do systematically use prohibitive vocabulary ("No person shall...," "It is prohibited to...," "Personnel must not..."), a pattern observable across regulatory frameworks (OSHA standards, ISO 27001 controls, legal statutes) and organizational policy templates — however, no citation from the PROJ-014 evidence base directly establishes this for LLM system prompt authorship contexts specifically. The assumption remains plausible but unverified against the evidence catalog. (b) This convention was not examined for its effectiveness when adopted.
- **Assumption count under the I3 analysis:** The assumption count for Explanation 2 is **conditionally 2** (if assumption (a) is treated as generally known) or **effectively 3** (if assumption (a) is treated as requiring domain-specific evidence). Because assumption (a) is partially verifiable from outside the evidence catalog but not confirmed within it, the parsimony differential between Explanation 2 and Explanations 1/3 is uncertain. The I3 revised finding replaces "Explanation 2 requires fewer assumptions" with the conditional finding below.

**Explanation 3 (Engineering discovery):** Negative constraint vocabulary was tested or experienced to be more effective for compliance and was adopted on that basis.
- Auxiliary assumptions required: (a) vendors conducted or experienced comparison of vocabulary options, (b) vocabulary comparison produced a preference for prohibitive framing, (c) this preference was documented in production rule design.
- **Assumption count: 3**

**Parsimony finding (I3 revised — DA-002-I2, FM-003-I2 Major resolutions):** The I2 parsimony finding that "Explanation 2 requires fewer assumptions" rested on the unverified premise that policy-document prohibitive vocabulary conventions are an established fact (Assumption (a) for Explanation 2). Because this premise is plausible but unconfirmed within the PROJ-014 evidence catalog, the parsimony differential is **conditional**:

- **If Assumption (a) is accepted as generally known** (prohibition vocabulary in policy documents is a widely observable pattern across legal and regulatory contexts): Explanation 2 assumption count = 2; Explanations 1 and 3 = 3 each. Explanation 2 is more parsimonious.
- **If Assumption (a) requires domain-specific evidence** (specifically: evidence that LLM system prompt authors draw on policy-document vocabulary conventions): Explanation 2 assumption count = 3; all three explanations have equal assumption counts. No parsimony differential exists.

**The correct I3 statement:** Explanations 1 and 2 should be treated as co-null hypotheses. Under the conservative reading (equal assumption counts), the parsimony analysis does not distinguish them. Under the more permissive reading, Explanation 2 may be more parsimonious. In neither reading is Explanation 3 (the hypothesis-supporting engineering-discovery explanation) favored by parsimony. **Explanation 3 is not established.**

**NEVER present Explanation 3 as established.** All three are consistent with observable evidence. Explanations 1 and 2 are co-null hypotheses.

**Explanation 2 severity (IN-003-I1 Major resolution; updated in I3; I5 note added):** If genre convention fully explains the vendor self-practice pattern, VS-001–VS-004 carry zero evidential weight for the framing effectiveness hypothesis. Under this scenario, the analysis's evidential base for ranks 5–6 consists of: A-11 (T3, contrastive CoT), A-15 (T1, compliance-focused, not hallucination-specific), and A-23 (T1, now confirmed — negation reasoning accuracy at rank 5). **(I5 update to this severity assessment):** A-23's T1 confirmation partially reduces Explanation 2's severity: under Explanation 2, the analysis retains two confirmed T1 studies for ranks 5–6 behavioral outcomes (A-15 for compliance, A-23 for negation accuracy). The directional verdict under Explanation 2 being correct: "Structured techniques show directional improvement over blunt prohibition on compliance outcomes (T1, A-15, MEDIUM confidence) and on negation reasoning accuracy (T1, A-23, MEDIUM confidence), with LOW confidence for hallucination rate reduction specifically, and no evidence on structured negative vs. structured positive at ranks 9–11." This is a stronger lower bound than the pre-I5 assessment. Note that the revised parsimony analysis (I3) makes the conditional-parsimony finding explicit: Explanation 2's advantage over Explanation 1 depends on whether its core assumption about policy-document vocabulary conventions is treated as verified or as requiring domain-specific evidence.

### Hierarchy Mapping — Dimension 5

The vendor adoption pattern maps precisely to the hierarchy split: vendor RECOMMENDATIONS concern rank 12 (standalone blunt prohibition). Vendor PRACTICE employs ranks 9–11 (declarative behavioral negation, paired negative-positive, justified prohibition with consequences). This distinction, invisible in individual surveys, becomes the central analytical finding when synthesis and supplemental reports are read together.

The CONFLICT-2 resolution in the synthesis (context dependency: positive for general use, negative for safety-critical) is consistent with Explanation 1 (audience specificity) from the supplemental VS-002 analysis — but equally consistent with Explanation 2 (genre convention in policy documents vs. user-facing guidance).

### Dimension 5 Verdict

**HIGH confidence observational finding:** The vendor adoption evidence shows a consistent pattern — all major vendors recommend positive framing for general use, while simultaneously using negative constraint framing for their own safety-critical, precision-critical, and behavioral enforcement rules. This pattern is directly observable across three independent vendors (Anthropic, OpenAI, LlamaIndex) and multiple document types (user-facing guidance, API documentation, source code defaults, production behavioral rules).

**MEDIUM confidence for the inference that vendor practice reflects audience differentiation (Explanation 1) or engineering design choice (Explanation 3).** Both explanations require 3 auxiliary assumptions. Explanation 2 (genre convention) requires 2 auxiliary assumptions under the I3 revised parsimony analysis (see below), making it equally or more parsimonious than Explanations 1 and 3, and it cannot be ruled out.

**Structural circularity caveat (RT-001-I2 Major resolution — I3 addition):** The HIGH confidence label applies to the observational fact that vendors use negative framing in production enforcement tiers. It does NOT apply to the interpretation of why they do so. The interpretation of this evidence — which explanation is most likely, and how strongly it supports the hypothesis — is produced by the same researcher who designed the PROJ-014 research program using negative constraints in its own governance. This is structural circularity: the researcher's prior commitment to negative constraints may influence which explanation is found most persuasive, which evidence is selected for analysis, and how the parsimony analysis is conducted. This circularity cannot be resolved by methodological disclosure; it requires independent replication (a different researcher, same evidence base, no hypothesis commitment) before the VS-001–VS-004 interpretation is relied upon for any consequential decision. See Assumption A-002 for the full disclosure.

**NEVER interpret the D5 observational finding as establishing that negative framing is more effective than positive framing.** It establishes that negative framing is consistently chosen for production enforcement tiers. The reason for that choice remains contested across three competing explanations, and the interpretation of those explanations is subject to researcher circularity risk.

---

## Evidence Quality Matrix

All evidence across five dimensions, consolidated:

> **A-16 REMOVAL NOTICE (SR-002-I1, CC-002-I1 Critical/Major resolutions; CC-001-I2 Minor resolution):** One source (A-16) identified during the survey was found to be a rejected peer-review submission and has been REMOVED from this evidence matrix entirely. It was included in the I1 matrix with a disclaimer annotation, which constituted citing it. A rejected submission's findings must not appear in evidence assembly in any form, even with disclaimers. No dimension verdict in this document uses A-16 findings. The identifying details of this source (author names, venue, rejection status) are not disclosed here because citing a source for its removal still functions as a citation. Readers should note: one rejected submission was identified in the survey and excluded from all analyses per accuracy standards (P-001).

| Evidence ID | Evidence Source | Tier | Supports Positive | Supports Negative | Neutral/Mixed |
|-------------|----------------|------|-------------------|-------------------|---------------|
| A-1 | NegativePrompt, IJCAI 2024 — negative EMOTIONAL stimuli, different phenomenon from behavioral constraint prompting | T1 | | Out of scope | Excluded from hierarchy |
| A-3 | Negation benchmark, EMNLP 2023 | T1 | | | LLMs struggle with negation comprehension |
| A-6 | Varshney et al., arXiv 2024 | T3 | Conditional (MCQA/LLaMA-2 only) | | |
| A-7 | Arditi et al., NeurIPS 2024 | T1 | | | Refusal one-dimensional; explains brittleness |
| A-9 | McKenzie et al., TMLR 2023 | T2 | Conditional (2022-era models) | | |
| A-10 | Constitutional AI, arXiv 2022 | T3 | | Training-time negative constraints (out of scope) | |
| A-11 | Contrastive CoT, arXiv 2023 | T3 | | Contrastive (pairing) | |
| A-12 | EmotionPrompt, IJCAI'23 | T2 | | Conditional (emotional) | |
| A-13 | Sclar et al., ICLR 2024 | T1 | | | Formatting causes 76pp swings; framing instability |
| A-14 | Gandhi et al., arXiv 2025 | T3 (commercial) | Conditional (emotional negativity, 8.4% accuracy loss) | | |
| A-15 | DeCRIM, EMNLP 2024 | T1 | | Structured atomic decomposition (+7.3–8.0%) | |
| A-17 | IFEval, arXiv 2023 | T3 | | | Benchmark framework |
| A-18 | Heo et al., arXiv 2024 | T3 | | | Models "know" compliance before generation |
| A-19 | Tripathi et al., arXiv 2026 | T3 | | | Compliance and accuracy independent |
| A-20 | Geng et al., AAAI 2026 | T1 | | | Instruction hierarchy unreliable; both framings fail at rank 12 |
| A-22 | CoVe, ACL 2024 | T1 | | | Verification pipeline (orthogonal) |
| A-23 | Barreto & Jana, EMNLP 2025 Findings — **T1-VERIFIED** (I5); "This is not a Disimprovement: Improving Negation Reasoning in Large Language Models via Prompt Engineering"; ACL Anthology https://aclanthology.org/2025.findings-emnlp.761; outcome: negation reasoning accuracy, not hallucination rate directly | T1 | | Warning-based and persona-based prompts (+25.14% negation reasoning accuracy); NTAS correlates with performance; code publicly available | |
| A-25 | Betley et al., Nature 2026 | T1 | | | Fine-tuning negative behavior causes broad misalignment |
| A-27 | LogicBench, ACL 2024 | T1 | | | Negated-premise reasoning fails |
| A-28 | CAST, ICLR 2025 | T1 | | Model-internal (out of scope) | |
| A-31 | Bsharat et al., arXiv 2023 — multi-principle study; 55% figure applies to specific task/model combination; control condition equivalence not verified | T3 | 55% improvement of affirmative over prohibition (rank 12, specific conditions) | | |
| C-6 | GPT-5.1 Guide, OpenAI | T4 | | Paired negative-positive in current-gen guidance | |
| C-7 | GPT-5.2 Guide, OpenAI | T4 | | Explicit negative constraints in current-gen guidance | |
| C-11 | LlamaIndex defaults | T4 (source code) | | 6 negative instructions in framework defaults | |
| C-13 | DSPy paper, arXiv 2023 | T3 | | Programmatic enforcement (164% compliance) | |
| C-19 | Young et al., arXiv 2025 | T3 | | | 43.7% pass rate; constraint compliance 66.9% |
| I-1/C-1 | Anthropic prompting best practices | T4 (HIGH) | Explicit positive recommendation | | |
| I-3/C-3 | OpenAI prompt engineering | T4 (HIGH) | Explicit positive recommendation | | |
| I-5/C-5 | OpenAI GPT-5 guide | T4 (HIGH) | Explicit positive recommendation | | Domain-specific negatives work: "NEVER add copyright headers" |
| I-6 | Google Gemini guide | T4 (HIGH) | Explicit positive recommendation | | |
| I-12 | DreamHost (tested) | T4 | Systematic testing: avoiding negatives improves results (methodology undisclosed) | | |
| I-21/C-12 | DSPy framework docs | T4 | | Programmatic enforcement | |
| I-27 | NeMo Guardrails | T4 | | Infrastructure-level enforcement | |
| I-28, I-32 | Claude Code context compaction bug reports (Anthropic GitHub, multiple independent users; direct URLs not available in synthesis evidence catalog; readers should verify in synthesis.md evidence section) | T4 | | | NEVER rules dropped during context compaction; failure mode for negative framing. Note: The specific GitHub issue references for I-28 and I-32 are cataloged in the synthesis.md evidence section (Section: Evidence Catalog). Readers should refer to that section for all available access information and retrieval context. |
| VS-001 | Anthropic's own behavioral rules: 33 NEVER/MUST NOT instances | T4 (direct observation) | | Enforcement-tier practice: negative framing for ALL HARD rules | |
| VS-002 | Recommendation/practice divergence — three competing explanations (Exp 1: audience diff, Exp 2: genre convention, Exp 3: engineering discovery) | T4 + inference | | Under Exp 3: inference (not established) | Under Exp 1 or 2: neutral |
| VS-003 | HARD tier vocabulary defined as prohibitive | T4 (observation) | | Tier architecture: enforcement tier defined by prohibitive vocabulary | Partly definitional |
| VS-004 | Constitutional triplet expressed as prohibitions | T4 (observation) | | Framework design choice: safety constraints expressed as prohibitions | |
| JF-002 | PLAN.md 12 negative constraints — HIGH CIRCULAR RISK | T5 (self-report, circular) | | Practitioner choice: negative constraint governance | Circular risk acknowledged |
| EO-001 | PROJ-014 quality trajectory: 0.83→0.953 — source: `barrier-1/adversary-gate.md` | T5 (session, confounded) | | Existence proof: C4 results achievable under negative-constraint regime | Confounded; 5 co-present variables |
| EO-002 | Zero constraint violations in 4-iteration C4 tournament — source: `barrier-1/adversary-gate.md` | T5 (session, confounded) | | Direct session-level constraint adherence | Same confounds |
| EO-003 | "Never state facts without sources" → zero unsourced claims — source: `barrier-1/supplemental-vendor-evidence.md` | T5 (session, confounded) | | Association between negative constraint and compliance | Same confounds |

---

## L1: Technical Findings

### Finding T-001: The Effectiveness Question Cannot Be Answered as a Binary

The synthesis AGREE-5 hierarchy demonstrates that "negative prompting" spans at least 7 technically distinct mechanisms (ranks 5–12, excluding removed rank 7) with different evidence profiles. Comparing "negative prompting" against "positive prompting" as categories is analytically invalid unless the specific mechanism within the hierarchy is specified.

**Technically correct analytical frame:**
- Standalone blunt prohibition (rank 12): FAILS — supported by T1 evidence (A-20, AAAI 2026) and T3 large-scale study (A-19)
- Warning-based meta-prompts (rank 5): IMPROVES negation reasoning accuracy +25.14% — T1 confirmed (A-23, EMNLP 2025 Findings, https://aclanthology.org/2025.findings-emnlp.761); outcome is negation comprehension, not hallucination rate directly; replication needed
- Atomic decomposition (rank 6): IMPROVES compliance +7.3–8.0% — T1 (A-15, EMNLP 2024)
- Paired negative + positive (rank 10): QUALITATIVELY SUPERIOR to standalone — T4 (vendor docs, AGREE-8)
- Justified prohibition (rank 11): QUALITATIVELY SUPERIOR to unjustified — T4 (vendor docs, AGREE-9)
- Declarative behavioral negation (rank 9): VENDOR PRACTICE but no controlled evidence — T4

**Technical action:** NEVER use "negative prompting" without specifying which rank in the hierarchy is under discussion. Any technical recommendation must specify: standalone blunt prohibition vs. structured specific prohibition vs. paired vs. justified vs. declarative behavioral vs. L2-re-injected.

### Finding T-002: The Vendor Self-Practice Evidence Is the Strongest Observational Signal — With Critical Interpretation Constraints

The VS-001 finding — 33 NEVER/MUST NOT instances in Anthropic's own production behavioral enforcement rules, specifically placed at the HARD enforcement tier, with per-prompt L2-re-injection — constitutes the strongest observational signal in the entire evidence base.

**Two mechanisms are co-present and must not be conflated (SM-001-I1 Major resolution):** The L2-re-injection mechanism (re-injection at every prompt) is the primary context-rot-prevention mechanism. The NEVER/MUST NOT vocabulary is the framing mechanism. Whether NEVER/MUST NOT vocabulary contributes beyond what re-injection alone provides is untested. The design choice to pair re-injection WITH prohibitive vocabulary — rather than re-inject positive equivalents — is itself a signal that practitioners believed vocabulary mattered at the enforcement tier. Phase 2 Condition C4 tests this co-occurrence directly.

**Parsimony constraint:** Three competing explanations (Explanation 1: audience differentiation, Explanation 2: genre convention, Explanation 3: engineering discovery) are equally consistent with this evidence. Explanations 1 and 2 are co-null hypotheses. NEVER treat the vendor self-practice evidence as establishing Explanation 3.

**What it does NOT establish:** That negative framing CAUSES better compliance.

**Technical action:** Phase 2 experimental design MUST include a condition isolating framing from re-injection frequency: same content, same injection frequency, different vocabulary (NEVER/MUST NOT vs. always/ensure). This is Condition C4 in the supplemental report experimental design.

### Finding T-003: The Most Relevant Gap for Phase 2 Is Ranks 9–11 vs. Positive Equivalents

The existing evidence base has compared:
- Rank 12 (blunt prohibition) vs. positive instruction — result: positive instruction wins (A-31, A-20)
- Rank 5–6 (structured techniques) vs. rank 12 (blunt prohibition) — result: structured techniques win (A-23, A-15)
- Ranks 9–11 (vendor self-practice tier) vs. positive equivalents — NOT TESTED

**Technical gap:** No Tier 1 or T2 study compares rank 9–11 structured negative constraints (with consequences, pairing, justification) against positively-framed equivalents with the same level of structure and specificity. This is the primary gap Phase 2 must close.

### Finding T-004: Context Compaction Is an Unmitigated Failure Mode for Negative Framing — With Directional Verdict Implications

GAP-13 documents a specific, practically critical failure mode: during context compaction, NEVER/DO NOT rules lose their imperative force (I-28, I-32 — Anthropic GitHub bug reports from multiple independent users; direct URLs unavailable in synthesis catalog; verify in synthesis.md Evidence Catalog section for all available access information and retrieval context). The adversary-gate.md score trajectory for PROJ-014 includes "zero scope violations" — but this session did not encounter context compaction conditions.

**Directional inversion under deployment conditions (RT-003-I1 Major resolution):** The PROJ-014 session directional findings (D1 MEDIUM confidence) apply to short-context conditions. Under long-context deployment conditions with context compaction, the directional finding may be REVERSED: negative framing has a documented failure mode (prohibitive vocabulary loses imperative force); positive framing has no equivalent documented failure mode. In precisely the conditions where HARD behavioral enforcement is most needed — long-context production sessions — structured negative framing may systematically underperform positive framing. NEVER treat any directional verdict in this analysis as universally applicable to all deployment contexts.

**Technical implication:** Phase 2 multi-turn testing MUST specifically test context compaction conditions. A Phase 2 result showing negative framing advantages under short-context conditions but disadvantages under context compaction would be the most practically significant finding.

### Finding T-005: Model Generation Is a Confounding Variable That Cannot Be Ignored

CONFLICT-1 resolves the inverse scaling vs. positive scaling conflict temporally: older models (2022–2023) showed inverse scaling on negation; newer architectures (2024–2025, Llama 3, Qwen 2.5) show positive correlation (r=0.867, A-5). GPT-5.2 guidance explicitly warns that "poorly-constructed prompts containing contradictory or vague instructions can be more damaging to GPT-5.2 than to other models" (C-7, GAP-14).

**Current-model sensitivity caveat (IN-004-I1 Minor resolution):** An alternative reading of CONFLICT-1 is that 2024–2025 models are better at understanding negation — but GPT-5.2's sensitivity warning suggests they may also be more sensitive to poorly-constructed negations. Negative constraint formulations in Phase 2 must be "well-constructed" under frontier model sensitivity standards. Phase 2 must test negative constraint formulations specifically for quality adequacy before drawing framing-effect conclusions.

**Technical implication:** Evidence from pre-2024 models MUST NOT be extrapolated to current-generation frontier models. Phase 2 testing on Claude Opus 4.6/Sonnet 4.6 and GPT-4.1/GPT-5 is necessary.

---

## L2: Architectural Implications

### Implication A-001: The Enforcement Tier Architecture Is the Analytical Key

The most architecturally significant finding across all five dimensions is not the positive-vs-negative framing question per se — it is that effective behavioral enforcement appears to require a multi-tier architecture in which different constraint tiers use different vocabulary deliberately. Anthropic's own production system demonstrates this:

- HARD tier (cannot override): MUST, SHALL, NEVER, FORBIDDEN — prohibitive vocabulary
- MEDIUM tier (overridable with justification): SHOULD, RECOMMENDED, PREFERRED — conditional vocabulary
- SOFT tier (optional): MAY, CONSIDER, OPTIONAL — permissive vocabulary

The enforcement tier architecture MUST NOT be understood as "negative framing for everything." It is a structured assignment of constraint vocabulary to enforcement priority. The HARD tier uses prohibitive vocabulary because prohibitive vocabulary is less ambiguous than conditional or permissive vocabulary — not necessarily because it is inherently more effective as a linguistic phenomenon.

**Architectural recommendation:** Frame-agnostic constraint taxonomy design is a prerequisite to answering the positive-vs-negative question. Systems MUST distinguish: (a) what category of constraint is being expressed, (b) what enforcement mechanism is available, (c) what vocabulary is appropriate for the combination of (a) and (b). Phase 2 MUST operationalize this taxonomy before collecting comparative effectiveness data.

### Implication A-002: The Prohibition Paradox Is a Systemic Pattern — Explained by Co-Null Hypotheses

The "prohibition paradox" (THEME-1) — vendors recommend positive framing while using negative framing in production — is not an artifact of sloppy vendor communication. It appears across three independent vendors (Anthropic, OpenAI, LlamaIndex) and multiple document types. This is a systemic pattern.

The architectural explanation is ambiguous between two co-null hypotheses: audience-differentiation (Explanation 1) and genre convention (Explanation 2). Under Explanation 1, general-use guidance targets the most common failure mode (naive blunt prohibition, rank 12), while production enforcement design employs structured negative constraints (ranks 9–11). Under Explanation 2, policy-style documents conventionally use prohibitive vocabulary regardless of effectiveness. Both explanations are consistent with the observable evidence and neither can be ruled out without Phase 2 data.

**Architectural implication:** Any organization building production LLM enforcement systems MUST distinguish between (a) guidance for developers authoring prompts (where positive framing reduces naive prohibition mistakes) and (b) guidance for architects designing behavioral enforcement systems (where structured negative constraints appear in vendor practice at the HARD enforcement tier). This distinction is warranted by the observational evidence regardless of which explanation is correct.

### Implication A-003: The Causal Attribution Problem Is Structural

The PROJ-014 session evidence (EO-001 through EO-003) cannot establish causality because the specialized agent architecture, C4 quality gate mechanism, structured templates, and researcher expertise all co-present with negative constraint framing.

**Architectural implication:** Controlled experiments (Phase 2) CANNOT be designed within the full Jerry Framework production context. They must use isolated prompt pairs with controlled confounds. The controlled experiment designed in the supplemental report (270 matched pairs, McNemar test, scorer blinding, presentation randomization) is architecturally correct because it strips away the co-present mechanisms and tests framing in isolation.

### Implication A-004: Structured Enforcement Dominates the Framing Question

THEME-5 establishes that programmatic enforcement (DSPy Assertions, NeMo Guardrails, LangChain OutputFixingParser) consistently outperforms linguistic framing regardless of positive or negative vocabulary. This is the most actionable architectural finding: if an organization has access to engineering infrastructure, the linguistic framing question becomes subordinate to the enforcement mechanism question.

**Architectural implication:** Phase 2 must explicitly decide whether to include programmatic enforcement conditions (ranks 3–4) alongside linguistic framing conditions (ranks 5–12). If programmatic enforcement dominates both positive and negative linguistic framing, the practical recommendation may be: "invest in enforcement architecture rather than framing vocabulary optimization."

---

## Synthesis and Directional Verdict

**I1 Directional Verdict Recalibration (DA-001-I1, CC-001-I1 Critical resolutions):** The I1 synthesis stated "the evidence directionally favors structured negative constraint framing." This verdict is recalibrated here to reflect the predominantly LOW-confidence evidence base across three of five dimensions. A directional verdict derived from predominantly LOW-confidence evidence is not a directional verdict — it is a prior belief expressed in the language of evidence.

### Dimension-by-Dimension Summary

| Dimension | Finding type | Confidence (operationalized) | Primary limitation |
|-----------|-------------|----------------------------|--------------------|
| D1: Constraint Adherence | Directional | MEDIUM (1 T1 + consistent T4 from 3+ vendors; see scale) | No controlled comparison of equivalent structure levels; context compaction inverts verdict at scale |
| D2: Hallucination Prevention | Directional for negation accuracy improvement (MEDIUM, I5); for hallucination rate specifically: LOW; UNTESTED for structured negative vs. structured positive | **MEDIUM for negation accuracy (I5 upgrade from LOW)** — A-23 confirmed T1 (EMNLP 2025 Findings); +25.14% negation reasoning accuracy; scope constraint: negation comprehension ≠ hallucination rate; 60% claim UNTESTED | A-23 measures negation reasoning accuracy, not hallucination rate directly; the MEDIUM upgrade is construct-scoped; hallucination rate reduction remains without confirmed T1 evidence |
| D3: Quality Gate Performance | OBSERVATIONAL (existence proof only) | LOW (session data, 5 confounds; see scale) | Not a directional comparison; cannot compare against positive-framing baseline |
| D4: Iteration Efficiency | OBSERVATIONAL (existence proof only) | LOW (session data, no baseline; see scale) | Not a directional comparison; n=2 same-pipeline observations |
| D5: Practitioner and Vendor Adoption | Observational — adoption pattern documented | HIGH (observational; T4 directly verifiable; consistent across 3+ independent vendors) | Causal explanation contested; Explanations 1, 2, 3 all consistent with evidence; researcher circularity risk disclosed |

### Directional Verdict (Recalibrated)

**The evidence base does not permit a directional verdict favoring structured negative constraint framing over positive framing across all five dimensions.** A correct synthesis must state:

1. **HIGH confidence, established:** Blunt prohibition (rank 12) is less effective than structured alternatives (positive OR structured negative). Supported by T1 (A-20, A-15) and T3 (A-31, A-19).

2. **MEDIUM confidence for negation reasoning accuracy; LOW confidence for hallucination rate:** Specific structured negative techniques (ranks 5–6) show MEDIUM-confidence directional improvement in negation reasoning accuracy (A-23, T1, EMNLP 2025 Findings confirmed; +25.14%) and LOW-confidence directional improvement in compliance (A-15, T1, primary outcome). A-23's confirmation satisfies the MEDIUM threshold for the outcome it measures (negation comprehension accuracy). For hallucination rate reduction specifically, evidence remains LOW: A-23 does not measure hallucination rate directly. T3 evidence (A-11, A-19 partial) supports the directional claim for hallucination reduction but at LOW confidence. Does NOT establish superiority over structured positive equivalents at any rank. (I3 downgrade from MEDIUM; I5 partial upgrade: MEDIUM for negation accuracy, LOW for hallucination rate.)

3. **HIGH confidence, observational:** Vendors use negative framing in production HARD enforcement tiers while recommending positive framing for general users. Directly verifiable. Does NOT establish that negative framing is more effective than positive framing (Explanations 1 and 2 are co-null hypotheses).

4. **LOW confidence, observational (not directional):** PROJ-014 C4 results were achieved under negative-constraint prompting. Existence proof only; cannot be compared to a positive-framing counterfactual.

5. **UNTESTED:** Whether structured negative constraints at ranks 9–11 outperform structurally equivalent positive constraints on matched tasks. This is the Phase 2 experimental target.

6. **Deployment-context-conditional:** The directional signal from items 1–2 applies to short-context conditions. Under long-context deployment with context compaction, the directional signal may REVERSE (T-004).

**Phase 2 is required before any directional verdict can be issued.** The above is a research question with supporting plausibility evidence — not a finding.

### Confidence Bounds

| Claim | Evidence | Confidence (operationalized) |
|-------|----------|------------------------------|
| Blunt prohibition (rank 12) is less effective than positive instructions | T1 (A-20, A-15), T3 (A-31, A-19) | HIGH |
| Structured negative techniques (ranks 5–6) improve negation reasoning accuracy vs. blunt prohibition | T1 (A-23, confirmed EMNLP 2025 Findings) | **MEDIUM (I5 upgrade from LOW)** — A-23 confirmed T1; +25.14% negation accuracy; scope: negation comprehension, not hallucination rate |
| Structured negative techniques (ranks 5–6) outperform blunt prohibition specifically for hallucination rate reduction | T3 (A-11); no T1 evidence for this specific outcome | **LOW** — A-23 measures negation accuracy not hallucination rate; no confirmed T1 study for hallucination-specific comparison |
| Structured negative techniques (ranks 5–6) improve compliance vs. blunt prohibition | T1 (A-15, primary: compliance) | MEDIUM — but limited to compliance outcome, not hallucination specifically |
| Vendors use negative framing in production enforcement while recommending positive for general use | T4 (direct observation, 3+ vendors) | HIGH |
| The vendor practice/recommendation divergence reflects an engineering discovery about effectiveness | T4 + inference (Explanation 3) | LOW (one of three competing explanations, not established; researcher circularity risk applies) |
| Negative prompting (any form) reduces hallucination by 60% | 0 of 75 sources | NO SUPPORT — UNTESTED |
| Structured negative constraints (ranks 9–11) outperform equivalent positive constraints on matched tasks | No controlled comparison exists | UNTESTED |
| PROJ-014 C4 PASS scores were caused by negative constraint framing | Confounded session observation | CANNOT ESTABLISH |
| Negative framing outperforms positive framing under long-context deployment with context compaction | T-004 (inverts direction); no controlled test | UNKNOWN — may favor positive framing |

---

## Why Observational Evidence Does Not Replace Phase 2

**IN-001-I1 Critical Resolution — Explicit Guard Against Phase 2 Abandonment Misreading**

Four elements in this analysis, if misread, could lead a reader to conclude Phase 2 is unnecessary or to treat working practices as validated findings:

1. **D3 verdict:** "C4 results achievable under negative-constraint prompting" — misread as "negative constraints work; Phase 2 is redundant."
2. **D5 verdict:** "Vendors use negative framing in production enforcement while recommending positive for general users" — misread as "we already know negative works in production."
3. **L2 Implication A-002:** "A single recommendation cannot serve both audiences accurately" — misread as "the analysis has already explained the paradox; Phase 2 is not needed."
4. **PG-001 through PG-005 (Practitioner Guidance):** "Recommended working practice (pending Phase 2 validation)" — misread as validated experimental findings rather than observational working practices. **(PM-002-I2 Minor resolution — fourth misreading scenario added.)** The practitioner guidance is explicitly provisional and observationally motivated. Phase 2 experimental results, including inconclusive results, will require reassessment of the evidential basis for each guidance item.

**NEVER treat the observational findings in D3, D4, and D5 as substitutes for Phase 2 experimental data.** The specific reason:

The observational findings establish that:
- Negative framing co-occurs with C4-passing results (D3, D4)
- Negative framing is consistently chosen for production enforcement tiers (D5)

The observational findings CANNOT distinguish between:
- (a) **Framing effect:** Negative constraint vocabulary is the active variable improving compliance
- (b) **Re-injection effect:** L2 re-injection frequency is the active variable; vocabulary is incidental
- (c) **Consequence-pairing effect:** Paired consequences ("NEVER X — consequence Y") are the active variable; the NEVER vocabulary is incidental
- (d) **Genre convention:** Negative vocabulary is a convention with no independent effectiveness contribution

Phase 2 Conditions C2, C3, C4, C5 are explicitly designed to separate these explanations. Until Phase 2 data exists, the observational findings establish plausibility only.

### Phase 2 Inconclusive Scenario (PM-001-I2, IN-001-I2 Major resolutions — I3 addition)

**What practitioners should do if Phase 2 produces mixed or inconclusive results:**

Phase 2 may produce mixed results — for example, negative framing shows an advantage under Condition C2 but not Condition C4, or advantages appear on 2 of 5 task types but not others. This is a common experimental outcome and the analysis does not guarantee a clean confirmatory or falsifying result. If Phase 2 is inconclusive:

1. **PG-001 remains unconditional:** Standalone blunt prohibition (rank 12) is supported by T1 evidence (A-20) as underperforming structured alternatives regardless of framing results. A null framing result does not reinstate rank-12 blunt prohibition.

2. **PG-002 remains unconditional:** The need to specify hierarchy rank when discussing negative prompting is a methodological requirement independent of Phase 2 results.

3. **PG-003 contingency (under null or mixed Phase 2 framing result at ranks 9–11):** If Phase 2 finds no statistically significant advantage of structured negative vocabulary over matched positive vocabulary at ranks 9–11 (the primary Phase 2 test), practitioners should adopt the following revised practice: **retain the paired-consequence design** (stating both the constraint and its consequence) because the consequence-pairing mechanism has T4 and synthesis support (AGREE-8, AGREE-9) independent of the vocabulary framing question. **Do not treat vocabulary tier choice (NEVER vs. always) as a validated design criterion.** Vocabulary choice becomes a matter of style and audience convention — Explanation 2 (genre convention) would then be the most appropriate framing for policy-document vocabulary practices. A null framing result at ranks 9–11 does not require abandoning structured constraint design; it requires abandoning the claim that NEVER/MUST NOT vocabulary specifically contributes to compliance beyond the consequence-pairing structure itself.

4. **PG-004 and PG-005 remain unconditional:** Context compaction testing and enforcement architecture prioritization are independent of the framing vocabulary question.

5. **R-001 (Phase 2 design) requires revision under mixed results:** Mixed results should trigger a targeted replication study with more refined conditions before any directional claim is issued. The research program should treat mixed Phase 2 results as identifying which conditions and task types, if any, show framing effects — not as a global null result.

**NEVER interpret a null or mixed Phase 2 result for vocabulary framing as evidence that negative constraint design is without value.** The framing vocabulary question (NEVER vs. always) is separable from the structural design question (consequence-paired, justified, tiered enforcement). A null framing result would answer only the vocabulary question, leaving the structural design questions open.

---

## Practitioner Guidance Under Evidence Uncertainty

**PM-001-I1 Critical Resolution — Unconditional Practitioner Guidance**

The following recommendations are NOT contingent on Phase 2 being conducted. They are supported by existing T4 vendor self-practice evidence and T1 structured-technique findings independent of the framing question.

### PG-001: NEVER use standalone blunt prohibition as a behavioral enforcement mechanism

**Evidence basis:** T1 (A-20, AAAI 2026), T3 (A-19, A-31), T4 (synthesis AGREE-4). Blunt prohibition ("NEVER hallucinate," "DO NOT make things up") without structure, consequences, or pairing consistently underperforms positive instruction across multiple independent evidence streams. This finding is not contingent on Phase 2.

**NEVER use:** Standalone prohibition without consequence specification, context, or positive alternative.

### PG-002: NEVER design a behavioral constraint without specifying the hierarchy rank

**Evidence basis:** T1 (A-15, EMNLP 2024), T4 (synthesis AGREE-5). A constraint described as "negative prompting" without specifying the structural level (blunt prohibition vs. decomposed constraint vs. paired prohibition vs. justified prohibition) is not actionable. Engineers designing behavioral constraints MUST specify the structural level before comparing across studies or making implementation decisions.

**NEVER treat "negative prompting" as a single technique.** Specify the rank.

### PG-003: NEVER implement enforcement-tier constraints without pairing them with consequences and positive behavioral alternatives

**Evidence basis:** T4 (VS-001–VS-004, directly verifiable in production enforcement rules), synthesis AGREE-8 (paired negative + positive outperforms standalone), AGREE-9 (contextual justification improves effectiveness). These findings are at T4 and warrant adoption as working practices regardless of Phase 2 outcome.

**Recommended working practice (pending Phase 2 validation):**
- HARD enforcement tier: MUST/NEVER/MUST NOT + explicit consequence (e.g., "NEVER use system Python — command fails, environment corruption")
- MEDIUM advisory tier: SHOULD/RECOMMENDED + justification
- SOFT optional tier: MAY/CONSIDER — permissive vocabulary

This vocabulary tier design is warranted by vendor self-practice evidence even without controlled experimental validation. Phase 2 will determine whether the vocabulary tier design causally contributes to compliance or whether re-injection frequency or consequence-pairing is the active mechanism. **(SM-002-I2 Minor resolution):** Whether the NEVER/MUST NOT vocabulary or the re-injection frequency is the active mechanism is precisely Phase 2 Condition C4's test target (C2+re-injection vs. C3 positive+re-injection). Adopt the vocabulary tier design as a working convention while treating the vocabulary-specific causal contribution as unconfirmed until Phase 2 data is available.

**Contingency if Phase 2 finds null framing effect at ranks 9–11 (IN-001-I2 Major resolution):** If Phase 2 produces a null or mixed result for the framing vocabulary question at ranks 9–11, retain the paired-consequence structure (constraint + consequence + justification) while treating vocabulary choice (NEVER vs. always) as convention-determined rather than effectiveness-determined. The structural design remains the primary recommendation; the vocabulary tier becomes a style choice consistent with policy-document genre conventions. See the Phase 2 Inconclusive Scenario section above for the full contingency guidance. Under a null framing result, the working practice default should align with the vendor's general-user recommendation (positive framing: "always ensure X," "ensure Y is present") unless the organization's policy-document conventions specifically prescribe prohibitive vocabulary, in which case genre convention (Explanation 2) justifies continued use of MUST NOT/NEVER as style choice.

### PG-004: NEVER deploy negative constraint prompting in long-context sessions without testing context compaction behavior

**Evidence basis:** T4 (I-28, I-32, GAP-13). NEVER rules documented to lose imperative force during context compaction. Any deployment of negative constraint framing in production systems that may encounter context compaction MUST be tested under compaction conditions before relying on the framing's effectiveness.

### PG-005: NEVER prioritize framing optimization over enforcement architecture investment

**Evidence basis:** T3 (C-13, DSPy: 164% compliance improvement), T4 (I-27, NeMo Guardrails), synthesis THEME-5. Programmatic enforcement consistently outperforms linguistic framing. If engineering infrastructure is available, enforcement architecture investment dominates framing vocabulary optimization in expected compliance improvement. Framing optimization becomes relevant when engineering infrastructure investment is not feasible.

---

## Recommendations

**Scope clarification for analytical principle (CC-003-I1 Major resolution):** The analytical principle "NEVER use positive prompting framing in this analysis" governs how analytical FINDINGS are framed. Recommendations are structural action constraints expressed in negative framing consistent with this principle. Recommendations R-001 through R-006 below are expressed in constraint-first language.

### R-001: NEVER treat the session observational data or vendor self-practice evidence as sufficient to validate or refute the hypothesis

The 270-matched-pair McNemar design from the supplemental report is the correct next step. The observational evidence establishes plausibility; it does not establish framing effects. Phase 2 is required.

**Priority conditions for Phase 2 pilot (n=30):**
1. C2 (Structured negative: NEVER/MUST NOT + consequence) vs. C3 (Positive equivalent: always/ensure + same content)
2. C4 (C2 + L2 re-injection) vs. C3 (to isolate framing from re-injection frequency)
3. C5 (Paired negative + positive) — test whether hybrid outperforms either standalone
4. C7 (Positive-only baseline: no negative framing)

### R-002: NEVER compare "negative prompting" against "positive prompting" without specifying which hierarchy rank is under comparison

A technical recommendation must specify the rank (e.g., "rank 10 paired prohibition outperforms rank 12 blunt prohibition by X%; rank 10 vs. structurally equivalent positive instruction untested").

### R-003: NEVER omit context compaction conditions from Phase 2 multi-turn testing

GAP-13 (NEVER rules dropped during compaction) is a practically critical failure mode not controlled in the PROJ-014 session. The finding that NEVER framing fails under compaction while positive framing may be more robust would invert the D1 directional finding and would be an architecturally significant result requiring explicit investigation.

### R-004: NEVER design Phase 2 as if linguistic framing is the only alternative

DSPy Assertions (rank 3, T3 preprint: 164% compliance improvement) and NeMo Guardrails (rank 3, T4) consistently outperform linguistic framing. Phase 2 should include at least one programmatic enforcement condition to determine whether the framing question is practically meaningful relative to the enforcement architecture question.

### R-005: NEVER extrapolate pre-2024 inverse scaling results to current frontier models

CONFLICT-1 is temporally resolved: positive scaling on negation is observed in 2024–2025 architectures. Phase 2 results on Claude Opus 4.6, Claude Sonnet 4.6, GPT-5/GPT-4.1, and Gemini 2.0 will not generalize from older model findings.

### R-006: NEVER implement the enforcement tier vocabulary design as a validated empirical finding before Phase 2

The vendor self-practice evidence (VS-001–VS-004) provides sufficient observational support to adopt the enforcement tier architecture as a WORKING PRACTICE pending Phase 2 validation. NEVER present this as a validated experimental finding.

---

## Assumptions and Limitations

### Assumption A-001: The 12-Level Hierarchy Is Ordinal, Not Interval

The effectiveness hierarchy from AGREE-5 is ordinal — ranks reflect direction of evidence, not magnitude of difference. NEVER assume the distance between rank 8 and rank 9 equals the distance between rank 11 and rank 12. The hierarchy's ordinal positions within ranks 5–12 are based on narrative synthesis judgment, not controlled head-to-head comparison.

### Assumption A-002: Vendor Self-Practice Evidence Is Partially Independent of This Analysis

VS-001 through VS-004 are directly verifiable by reading cited files — those files are authored by Anthropic engineers, not by this researcher. However, the interpretation of WHY Anthropic engineers made those choices is subject to confirmation bias (Methodological Limitation L-2 from the supplemental report).

**Circularity disclosure and independent replication requirement (RT-001-I1 Critical resolution):** The most significant methodological limitation of this entire analysis is structural circularity: the researcher who designed the PROJ-014 research program (which uses negative constraints in its governance) is the same researcher who selected the evidence, designed the hierarchy, and now evaluates findings. Each analytical choice — which evidence to include, which explanation to treat as parsimonious, what analytical frame to use — is within the researcher's control, and each choice can favor the hypothesis. This is not resolved by methodological disclaimers; it requires **independent replication**.

**A different researcher analyzing the same evidence base without hypothesis commitment is required before Dimension 5 findings (vendor self-practice interpretation) are relied upon.** This independent replication is a higher priority than Phase 2 experimental data for establishing the credibility of the VS-001–VS-004 evidence interpretation. Until independent replication exists, treat all VS-002 interpretations as researcher-biased accounts of ambiguous observational data.

### Assumption A-003: Explanations 1 and 2 Are Co-Null Hypotheses for VS-002

The analysis treats Explanation 1 (audience specificity) and Explanation 2 (genre convention) as co-null hypotheses for VS-002. The I3 revised parsimony analysis (DA-002-I2, FM-003-I2 resolutions) finds their parsimony relationship **conditional**: Explanation 2 may require 2 or 3 auxiliary assumptions depending on whether the claim that "policy documents conventionally use prohibitive vocabulary" is treated as generally known or as requiring domain-specific evidence. Under the conservative reading, Explanations 1 and 2 have equal assumption counts; under the permissive reading, Explanation 2 is more parsimonious. In neither reading is the parsimony analysis conclusive. Explanation 3 (engineering discovery) is the hypothesis-supporting inference. Phase 2 experimental design should be constructed to potentially distinguish these explanations.

### Limitation L-001: No Controlled Comparison for Dimensions 3 and 4

Dimensions 3 and 4 rest entirely on session observational data with 5 confirmed confounds and no matched positive-framing baseline. The session data is valid as existence proof (C4 results are achievable under negative-constraint prompting) but NEVER valid for causal attribution or directional comparison.

### Limitation L-002: The Synthesis Provides No Tier 1 Evidence for Ranks 9–11

The most action-relevant negative constraint techniques (ranks 9–11 — declarative behavioral negation, paired prohibition, justified prohibition) have NO Tier 1 peer-reviewed evidence. Their superiority over structural alternatives is documented at T4 (vendor documentation) only. This is the most significant evidence gap for the hypothesis.

### Limitation L-003: Expert User Moderating Variable Is Uncontrolled

AGREE-4 note (IN-001-R3): "A moderating variable not controlled in any current evidence is user expertise: expert prompt engineers who understand model-specific constraint design may achieve better compliance with prohibition-style instructions than non-expert users." Phase 2 MUST either standardize experimenter expertise or treat it as an independent variable.

### Limitation L-004: Evidence Temporal Scope

The evidence base consists primarily of 2022–2024 studies. CONFLICT-1 shows model-generation is a significant moderating variable. Results from pre-2024 models may not transfer to current frontier models (Claude 4, GPT-5, Gemini 2.0). Phase 2 must test on post-2024 frontier models only.

---

## Revision Log

### I1 → I2 Resolutions

| Finding ID | Severity | Resolution in I2 |
|-----------|----------|-----------------|
| CC-001-I1 | Critical | L0 executive summary reconciled with synthesis directional verdict; both presented together with accurate confidence framing |
| DA-001-I1 | Critical | Directional verdict recalibrated to reflect predominantly LOW-confidence evidence base; "directionally favors" verdict removed; five-point structured verdict issued |
| PM-001-I1 | Critical | Practitioner Guidance Under Evidence Uncertainty section added (PG-001 through PG-005); guidance not contingent on Phase 2 |
| RT-001-I1 | Critical | **PARTIALLY resolved in I2 — converted to Major for I3** (SR-002-I2 Minor resolution applied to this entry). Circularity disclosure strengthened in Assumptions; independent replication required stated explicitly. Not visible from L0 in I2 — resolved in I3 by adding circularity caveat to L0 and D5 verdict. |
| FM-001-I1 | Critical | Backup analytical frame added to hierarchy section; simplified 3-group taxonomy provided; hierarchy falsifiability condition stated |
| IN-001-I1 | Critical | Why Observational Evidence Does Not Replace Phase 2 section added; three misreading scenarios identified and guarded against; fourth scenario added in I3 (PM-002-I2) |
| CV-001-I1 | Critical | A-31 55% figure qualified with task/model specificity, control condition limitation, and generalization constraints |
### I2 → I3 Resolutions

| Finding ID | I2 Severity | Resolution in I3 |
|-----------|-------------|-----------------|
| DA-001-I2 / CV-001-I2 / FM-001-I2 | Major | D2 downgraded from MEDIUM to LOW throughout. A-23 was T1-unverified and could not satisfy the MEDIUM threshold ("exactly 1 T1 or T2 study"). Confidence scale application is now internally consistent. Confidence bounds table, synthesis table, and PS Integration key findings updated. (Note: A-23 has subsequently been confirmed as T1-verified in I5; see I4→I5 revision entry.) |
| RT-001-I2 | Major | Circularity caveat added to L0 executive summary (paragraph 2) and to D5 Verdict (structural circularity caveat subsection). Structural limitation now visible to readers at the L0 level. |
| PM-001-I2 / IN-001-I2 | Major | Phase 2 Inconclusive Scenario section added to "Why Observational Evidence Does Not Replace Phase 2." Five-point guidance provided for practitioners if Phase 2 produces mixed or inconclusive results. PG-003 contingency stated explicitly. |
| DA-002-I2 / FM-003-I2 | Major | Parsimony analysis revised. Explanation 2 Assumption (a) identified as unverified within the evidence catalog (plausible but not confirmed). Parsimony finding changed from "Explanation 2 requires fewer assumptions" to conditional finding: under conservative reading, equal assumption counts; under permissive reading, Explanation 2 may be more parsimonious. Neither reading establishes Explanation 3. |
| LJ-001-I2 | Major | Alternative Analytical Frameworks section added to Analysis Scope and Method. Three alternatives considered and rejected (binary, evidence-tier taxonomy, mechanism-based taxonomy). Selection rationale for 12-level hierarchy stated. |
| SR-001-I2 | Major | Resolved implicitly by D2 downgrade: the D3 application of "5+ confounds = LOW" is now consistent with the scale definition, as D2 is also LOW (not MEDIUM). The D3 downgrade rationale now applies uniform criteria. |
| SM-001-I2 | Major | Backup frame acknowledgment revised: I3 table in the Cross-Cutting Hierarchy backup frame now notes that ranks 5–6 evidence differs from ranks 9–11 evidence (T1 vs. T4 only). The backup frame retains the collective grouping for the core finding but notes the confidence differential. |
| DA-003-I2 | Minor | Confidence label (LOW) added to the context compaction reversal claim (T-004). Explicitly stated: T4 evidence basis; UNTESTED for directional comparison. |
| IN-002-I2 | Minor | L-001 cross-references added to D3 and D4 observational notes. |
| SR-002-I2 | Minor | Revision Log RT-001-I1 entry revised from "Critical | Circularity disclosure strengthened" to accurate "PARTIALLY resolved in I2 — converted to Major." |
| CC-001-I2 | Minor | A-16 removal notice revised to remove identifying information (author names, rejection venue). Source described only as "one rejected submission." |
| SM-002-I2 | Minor | PG-003 updated with re-injection ambiguity caveat and explicit Phase 2 Condition C4 target. |
| PM-002-I2 | Minor | Fourth misreading scenario added to "Why Observational Evidence Does Not Replace Phase 2." |
| FM-002-I1 | Major (RPN 392) | Confidence Scale Definition section added; all labels operationalized; retroactive application to dimension table |
| DA-003-I1 | Major | D3 and D4 headers changed from "Directional finding:" to "Observational Note:"; explicit statements that D3/D4 are existence proofs, not directional comparisons |
| SR-001-I1 | Major | D4 "Directional finding" header removed; "two same-pipeline observations do not constitute a direction" stated explicitly |
| SR-002-I1 + CC-002-I1 | Major | A-16 REMOVED entirely from evidence matrix and all dimension text; removal notice added |
| SM-001-I1 | Major | Mechanism distinction (re-injection vs. vocabulary) made explicit in hierarchy section and T-002; Phase 2 C4 condition purpose stated |
| SM-002-I1 + RT-002-I1 | Major | Hierarchy validity disclosure section added; provenance acknowledged; adversary gate noted as internal, not external validation |
| DA-002-I1 | Major | Formal parsimony analysis added for three competing explanations; Explanation 2 found equally parsimonious; co-null hypothesis framing adopted |
| PM-002-I1 | Major | Backup analytical frame added to hierarchy section |
| PM-003-I1 | Major | Confidence scale operationalized (same as FM-002-I1) |
| RT-003-I1 | Major | T-004 context compaction finding integrated into D1 verdict and Synthesis; directional inversion under long-context conditions stated |
| CC-003-I1 | Major | Recommendation scope clarification added; recommendations rewritten in constraint-first language |
| IN-002-I1 | Major | Hierarchy falsifiability condition stated |
| IN-003-I1 | Major | Explanation 2 severity stated: if genre convention correct, evidential base reduces to T3 evidence only for ranks 5–6. (I5 note: A-23 is now T1-confirmed for negation reasoning accuracy; under Explanation 2, the evidential base is therefore T1 for negation accuracy at rank 5 and T1 for compliance at rank 6, but the hallucination-rate-specific claim remains T3 only. Explanation 2's severity is partially reduced: if genre convention fully explains vendor self-practice, the analysis retains two T1 studies for ranks 5–6 behavioral outcomes, but neither directly tests hallucination rate.) |
| CV-002-I1 | Major | EO-002 and EO-001 source file paths added to evidence matrix and dimension text |
| CV-003-I1 | Major | A-23 reclassified as T1-unverified; preprint/DOI unavailability disclosed; access requirement stated |
| CC-004-I1 | Major | PS Integration confidence value corrected to align with dimension-level table; derivation method stated |
| DA-004-I1 | Minor | Rank 7 (NegativePrompt emotional stimuli) removed from hierarchy; footnote added |
| SM-003-I1 | Minor | Confidence scale operationalized (same as FM-002-I1) — scale definition covers this finding |
| SR-003-I1 | Minor | Recommendations rewritten in constraint-first language |
| PM-004-I1 | Minor | Context compaction bug report URL unavailability disclosed; readers directed to synthesis.md evidence section |
| RT-004-I1 | Minor | Symmetry note added to Analytical Principles: absence-of-evidence principle applies in both directions |
| FM-004-I1 | Minor | Reflexivity impact assessment added to D1; JF-001 removed from D1 evidence; D1 stability without JF-001 confirmed |
| IN-004-I1 | Minor | T-005 expanded with current-model sensitivity caveat |
| CV-004-I1 | Minor | AGREE-8 and AGREE-9 self-referential citation limitation acknowledged in evidence matrix; primary vendor source recommendation for readers |

### I3 → I4 Resolutions

| Finding ID | I3 Severity | Resolution in I4 |
|-----------|-------------|-----------------|
| SR-003-I2 | Minor (unresolved across I2, I3) | Clarifying note added to Analytical Principles section (after the NEVER list) explicitly distinguishing analytical framing directive from epistemic scope. States: "This principle governs expression and analytical framing, not epistemological conclusion — null findings and positive-framing-favorable evidence are not suppressed. The constraint governs framing language, not epistemic conclusions." |
| NM-001-I3 | Minor (new in I3) | PS Integration confidence corrected from 0.62 to 0.64. Derivation now explicitly stated as (0.7+0.5+0.5+0.5+1.0)/5 = 3.2/5 = 0.64. Prior I3 value of 0.62 was not mechanically reproducible from the stated inputs. |
| CV-002-I2 | Minor (unresolved across I2, I3) | Note added to both the Evidence Quality Matrix entry and the T-004 Finding text directing readers to "synthesis.md Evidence Catalog section" for I-28 and I-32 access information. |

**I4 improvement additions (not findings — quality improvements per I3 scoring report recommendations):**

| Improvement | Section Affected | Change |
|-------------|-----------------|--------|
| PG-003 null-result vocabulary default (I3 Actionability gap) | PG-003 Contingency | Added sentence specifying working practice default under null framing result: align with vendor's general-user recommendation (positive framing) unless organizational policy-document conventions prescribe prohibitive vocabulary, in which case genre convention (Explanation 2) justifies continued MUST NOT/NEVER use as style choice. |
| Meta-analytic pooling rationale (I3 Methodological Rigor gap) | Alternative Analytical Frameworks — Selection rationale | Added sentence explaining why meta-analytic pooling was not feasible: heterogeneous outcome measures and non-comparable comparison conditions across studies. |

### I4 → I5 Resolutions

| Finding ID | I4 Status | Resolution in I5 |
|-----------|-----------|-----------------|
| A23-V-001-I5 | External evidence constraint (not a document-quality finding) — A-23 T1-unverified was identified by I4 scorer as the primary gap to 0.95 threshold | **A-23 confirmed T1-VERIFIED.** Paper: "This is not a Disimprovement: Improving Negation Reasoning in Large Language Models via Prompt Engineering" by Joshua Jose Dias Barreto and Abhik Jana. Published in Findings of the Association for Computational Linguistics: EMNLP 2025. ACL Anthology: https://aclanthology.org/2025.findings-emnlp.761. All prior "T1-unverified" labels for A-23 updated to "T1 (confirmed)." Hierarchy table footnote revised to confirmed ACL Anthology entry. Evidence Quality Matrix entry revised. D2 evidence assembly table revised. T-001 finding revised. |
| D2-C-001-I5 | Consequential change — D2 confidence upgrade assessed following A-23 T1 confirmation | **D2 partially upgraded from LOW to MEDIUM (scoped).** A-23 now satisfies the MEDIUM threshold ("exactly 1 T1 study") for the specific outcome it measures: negation reasoning accuracy (+25.14% on distractor negation tasks; warning-based and persona-based prompts). IMPORTANT scope constraint applied: A-23 measures negation comprehension accuracy (correctly interpreting negated statements), not hallucination rate (fabrication of false facts) directly. The MEDIUM confidence label in D2, the Dimension-by-Dimension Summary table, and the Confidence Bounds table is explicitly scoped to "negation reasoning accuracy." The 60% hallucination reduction claim and hallucination rate reduction specifically remain LOW/UNTESTED — A-23's T1 confirmation does not provide T1 evidence for those claims. A separate Confidence Bounds row added to distinguish negation accuracy (MEDIUM) from hallucination rate reduction (LOW). D2 verdict section revised with the "I5 CHANGE" label and construct scope note. Confidence scale definition table D2 row updated to reflect partial upgrade with scope constraint. |
| PS-U-001-I5 | Consequential change — PS Integration confidence value updated for I5 | **PS Integration confidence updated from 0.64 to 0.68.** D2 upgraded from LOW (0.5) to MEDIUM (0.7) based on A-23 T1 confirmation and negation accuracy evidence. New derivation: (0.7+0.7+0.5+0.5+1.0)/5 = 3.4/5 = 0.68. The upgrade is construct-scoped: D2 MEDIUM reflects negation reasoning accuracy; the 0.68 confidence value carries the same scope limitation. PS Integration key finding 2 updated to reflect A-23 T1 confirmation and the negation accuracy scope constraint. Iteration updated from I4 to I5. |

**I5 scope constraint note:** The A-23 T1 confirmation resolves the access barrier that caused the I3 downgrade, but does NOT retroactively convert A-23 into evidence for hallucination rate reduction. The paper's primary contribution is to negation reasoning accuracy via prompt engineering. The MEDIUM upgrade is the maximum warranted by the evidence — it reflects what A-23 actually demonstrates, not what would be needed to confirm the PROJ-014 60% hallucination reduction hypothesis.

---

## PS Integration

- **PS ID:** PROJ-014
- **Entry ID:** TASK-006
- **Iteration:** I5
- **Analysis Type:** Comparative effectiveness (5-dimension)
- **Artifact:** `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/phase-2/comparative-effectiveness.md`
- **Input artifacts:**
  - `barrier-1/synthesis.md` (R4, 0.953 PASS)
  - `barrier-1/supplemental-vendor-evidence.md` (R4, 0.951 PASS)
- **Confidence:** 0.68 (I5 update: D1=MEDIUM=0.7, D2=MEDIUM=0.7 [partial upgrade: negation accuracy confirmed T1; scope limited to negation comprehension not hallucination rate], D3=LOW=0.5, D4=LOW=0.5, D5=HIGH=1.0; unweighted average = (0.7+0.7+0.5+0.5+1.0)/5 = 3.4/5 = 0.68; D2 upgrade is construct-scoped — MEDIUM applies to negation accuracy sub-claim, not the hallucination rate reduction claim which remains LOW/UNTESTED)
- **Key findings for downstream agents:**
  1. Blunt prohibition (rank 12) is demonstrably less effective than structured alternatives — T1 evidence (A-20, A-15); HIGH confidence
  2. Structured negative techniques (ranks 5–6) show MEDIUM-confidence directional improvement in negation reasoning accuracy — A-23 now confirmed T1 (EMNLP 2025 Findings, https://aclanthology.org/2025.findings-emnlp.761); +25.14% on distractor negation; scope: negation comprehension accuracy, NOT hallucination rate directly; for hallucination rate reduction specifically, evidence remains LOW (T3 only); 60% claim remains UNTESTED
  3. Vendor self-practice (VS-001–VS-004): 33 instances; Anthropic uses negative framing for ALL HARD enforcement constraints while recommending positive for general users — HIGH confidence observational finding; subject to researcher circularity risk (see L0 caveat and Assumption A-002)
  4. The vendor practice/recommendation divergence is explained by audience-differentiation (Explanation 1, co-null) OR genre convention (Explanation 2, co-null, conditionally parsimonious per I3 revised analysis) OR engineering discovery (Explanation 3, hypothesis-supporting, not established); Explanations 1 and 2 cannot be ruled out without Phase 2 data
  5. No controlled study compares matched structured-negative vs. structured-positive constraints — UNTESTED; this is the Phase 2 experimental target
  6. Negative framing may REVERSE its directional advantage under long-context deployment with context compaction (T-004) — LOW confidence (T4 practitioner observations; no controlled comparison); NEVER apply D1 verdict to long-context production deployments without testing
  7. Independent replication of the comparative effectiveness analysis (different researcher, same evidence base, no hypothesis commitment) is required before VS-001–VS-004 interpretation is relied upon; circularity risk disclosed at L0
  8. If Phase 2 produces inconclusive or mixed results, PG-003 contingency path is: retain paired-consequence structure; treat vocabulary tier choice as convention-determined (Explanation 2) rather than effectiveness-determined
- **Next agent hint:** ps-analyst for TASK-005 (Claim Validation) cross-pollination at Barrier 2; ps-architect for Phase 3 taxonomy design

---

*ps-analyst | TASK-006 | PROJ-014 | 2026-02-28 | Iteration 5*
*Analysis framework: 12-level effectiveness hierarchy (synthesis AGREE-5) mapped across 5 dimensions; alternative frameworks considered and rejected (I3)*
*Evidence base: 75 deduplicated sources (synthesis R4) + 12 supplemental findings (supplemental R4)*
*I1 adversary findings addressed: 7 Critical, 19 Major (all); 9 Minor (all)*
*I2 adversary findings addressed (I3): 9 Major (all); 6 of 10 Minor (DA-003-I2, IN-002-I2, SR-002-I2, CC-001-I2, SM-002-I2, PM-002-I2)*
*I2 Minor findings not addressed in I3: SR-003-I2 (resolved in I4), CV-002-I2 (I-28/I-32 URL access — no new access path available), FM-002-I2 (merged with SR-001-I2, resolved by D2 downgrade), IN-002-I2 partially (D3/D4 L-001 cross-references added)*
*I5 change: A-23 confirmed T1-verified (ACL Anthology, EMNLP 2025 Findings); D2 partially upgraded to MEDIUM for negation accuracy sub-claim; confidence updated to 0.68*
*Constitutional compliance: P-001 (all conclusions cite evidence; no fabricated findings; A-23 upgrade scoped to what paper demonstrates), P-002 (analysis persisted to file), P-022 (assumptions and limitations explicit; circularity visible from L0; confidence scale applied consistently; D2 upgrade bounded to construct-appropriate scope)*
