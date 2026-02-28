# Barrier 1 Cross-Pollination Synthesis: Negative Prompting in LLMs

> ps-synthesizer | Barrier 1 | PROJ-014 | 2026-02-27 | **Revision 4** (addressing adversary findings from iteration 3)
> Input surveys: academic-survey.md (30 sources), industry-survey.md (31 core sources), context7-survey.md (20 references)
> Methodology: Braun & Clarke (2006) thematic analysis — 6-phase familiarization to report
> Confidence: 0.85 (high cross-survey corroboration on primary findings; gaps in empirical evidence noted throughout)
> Revision 2 addressed: DA-001 (Critical), DA-002 (Critical/Major), IN-001 (Critical), plus Priority 1 and Priority 2 Major findings from adversary tournament scoring 0.83
> Revision 3 addresses: SR-002-R2/CC-001-R2/FM-010 (75 vs. 74 inconsistency), SR-001-R2/CV-001-R2/FM-011 (Group C named sources), RT-001-R2 (publication bias SE-5), SR-005-R2 (PS Integration condition count), SM-001-R2/PM-001-R2/FM-012 (Cond-7 priority), DA-002-R2 (alternative hypothesis placement), RT-002-R2/DA-004-R2 (AGREE-5 scope note), IN-001-R2/CV-002-R2 (Cond-6 epistemological flagging), DA-001-R2 (vendor bias caveat)
> Revision 4 addresses: SR-001-R3/CC-001-R3/FM-014 (PS Entry ID R2→R4), CV-001-R3/FM-015 (Tier 3 count reconciled to 15; Tier 4 corrected to 42), DA-001-R3/FM-016 (L0 false-balance framing revised), SR-002-R3 (Deduplication table C-2 row corrected), SM-001-R3/SR-004-R3 (AGREE-5 intra-subgroup ranking evidence stated), CV-002-R3 (C-3 inaccessibility caveat), SM-002-R3 (Best Case Scenario added), IN-001-R3 (expert user variable noted in AGREE-4), SR-003-R3/CV-003-R2 (Revision Log RT-004 status stated), PM-001-R3 (GAP-5 caveat relocated), DA-002-R3/RT-001-R3 (A-31 tier qualification in AGREE-4)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Key numbers, verdict, three-paragraph overview |
| [Known Scope Exclusions](#known-scope-exclusions) | Structural limitations on evidence domains (IN-001 fix) |
| [L1: Merged Source Catalog](#l1-merged-source-catalog) | Deduplicated catalog of all unique sources with tier and survey attribution |
| [L1: Agreements — Cross-Survey Corroboration](#l1-agreements--cross-survey-corroboration) | Findings where 2+ surveys independently converge |
| [L1: Gaps — Single-Survey Claims](#l1-gaps--single-survey-claims) | Claims appearing in only one survey with no corroboration |
| [L1: Conflicts — Contradictory Findings](#l1-conflicts--contradictory-findings) | Contradictions with resolution or explicit "unresolved" documentation |
| [L1: Evidence Tier Analysis](#l1-evidence-tier-analysis) | Source counts by tier; findings by tier strength |
| [L1: Unsourced Claim Audit](#l1-unsourced-claim-audit) | Unsourced assertions in source surveys flagged |
| [L2: Cross-Survey Themes](#l2-cross-survey-themes) | Emergent patterns visible only across surveys |
| [Phase 2 Experimental Design Requirements](#phase-2-experimental-design-requirements) | Consolidated experimental design constraints with condition derivations |
| [Source Count Verification](#source-count-verification) | Exact deduplicated count with explicit arithmetic trace |
| [PS Integration](#ps-integration) | Downstream agent handoff schema |

---

## L0: Executive Summary

**In three sentences:** Across 75 unique sources drawn from peer-reviewed academic literature, practitioner industry documentation, and framework library guidance (31 academic including A-31 added in Revision 2 + 31 industry-unique + 13 context7-unique; see Source Count Verification), no source validates the PROJ-014 working hypothesis that negative prompting reduces hallucination by 60%. The strongest cross-survey agreement — reaching all three surveys independently — is that prohibition-style "don't do X" instructions are unreliable as standalone mechanisms, while structured alternatives (contrastive framing, atomic decomposition, programmatic enforcement, verification pipelines) consistently outperform blunt prohibition. The critical literature gap, confirmed identically by all three surveys, is the absence of any controlled A/B experiment comparing matched positive versus negative instruction variants on identical tasks at scale.

**Key numbers:**

| Metric | Value | Notes |
|--------|-------|-------|
| Total unique sources | **75** | 31 academic (incl. A-31 added R2) + 31 industry-unique + 13 context7-unique; see [Source Count Verification](#source-count-verification) for full arithmetic trace |
| Sources supporting the 60% hallucination-reduction hypothesis | **0** | Confirmed across all three survey search strategies |
| Surveys explicitly finding the hypothesis unsupported | **3 of 3** | |
| Cross-survey agreements (Strong — all 3 agree) | **5** | AGREE-1 through AGREE-5 |
| Cross-survey agreements (Moderate — 2 of 3 agree) | **4** | AGREE-6 through AGREE-9 |
| Total named agreements | **9** | 5 Strong + 4 Moderate |
| Conflicts identified | **4** | 3 resolved, 1 unresolved |
| Tier 1 peer-reviewed sources | **13** | 17.3% of total |
| Single-survey claims (gaps) requiring validation | **14** | |

> **Note on count correction (DA-002/CC-002):** The previous version of this document incorrectly stated "7 Strong" and "9 Moderate" in this section. The body of the document documents exactly 9 named agreements (AGREE-1 through AGREE-9), of which 5 are Strong and 4 are Moderate. The numbers above have been corrected to match the body content exactly.

**Verdict on the PROJ-014 hypothesis:**

The claim that "negative unambiguous prompting reduces hallucination by 60% and achieves better results than explicit positive prompting" **is not supported by any evidence across all three surveys.** The academic survey found no peer-reviewed study validating a 60% hallucination reduction; the industry survey found no controlled A/B comparison; the context7 survey found no quantitative evidence in any vendor documentation or framework guide.

**Important epistemic distinction (DA-001/RT-001 fix; DA-001-R3 fix):** The absence of evidence for the specific 60% hallucination-reduction claim is a null finding — this precise claim has not been tested in controlled conditions and has not been refuted. Separately, there is convergent multi-survey evidence (AGREE-4, AGREE-5: 5 Strong agreements across all three surveys) that standalone prohibition-style instructions are unreliable as behavioral constraints; these are distinct findings bearing on different aspects of negative prompting. The asymmetry is important: zero sources provide positive evidence for the 60% hypothesis, while multiple independent Tier 1 sources (A-20 AAAI 2026, A-15 EMNLP 2024) and 5-survey convergence (AGREE-4) document that blunt prohibition has consistent failure patterns. The weight of evidence leans against standalone prohibition being effective — even though no controlled A/B test of the specific 60% claim exists. The synthesis's primary result is that the 60% claim specifically lacks any supporting or refuting controlled evidence; the secondary result is that prohibition-style instructions generally fail as standalone mechanisms across multiple independent evidence streams.

Separately, and at lower confidence, one Tier 3 arXiv preprint (Academic survey, Source A-6: Varshney et al., LLaMA-2 MCQA study) found that negation instructions increased hallucination rates in specific multiple-choice question-answering contexts on one model family. This finding is preliminary: it comes from one unreviewed study covering one model family (LLaMA-2), four specific MCQA tasks, and 100-300 instances. It has not been independently replicated in a Tier 1 venue. The specific direction of this finding (negation may worsen rather than improve performance in MCQA contexts) is documented in AGREE-6 with appropriate caveats, but it does not constitute a general refutation of the working hypothesis.

**Phase 2 mandate:** The experimental design documented in the context7 survey (50 framing pairs, 5 models, 500 evaluation points minimum) will provide the first controlled evidence for or against the original working hypothesis.

**Best Case Scenario (SM-002-R3/SM-003-R2 fix):** The synthesis is most compelling and reliable when interpreted as follows: 75 deduplicated sources across three independent survey strategies using different search methodologies (academic databases, practitioner literature, framework documentation) all converge on the same primary finding — that the 60% hallucination-reduction hypothesis is untested in controlled public conditions. This convergence across independent evidence bases substantially reduces the probability that the null finding is a search artifact. The 9 cross-survey agreements (5 Strong, 4 Moderate) provide actionable scaffolding for Phase 2 design. The synthesis is at its strongest when Phase 2 is designed using the 7-condition framework with the Recommended-A/Recommended-B priority structure: this design was derived from the full evidence base and incorporates lessons from Tier 1 academic findings (A-15, A-23), Tier 4 vendor practice convergence, and synthesis-generated hypotheses (Cond-6). If Phase 2 delivers a clean result on even Cond-1 through Cond-3, this synthesis will have done its core job: establishing the baseline for the first publicly documented controlled comparison of matched positive vs. negative instruction variants.

**Research direction from synthesis (secondary):** The synthesis process suggests an alternative hypothesis for further investigation: "Specific, contextually justified constraints — whether positive or negative in framing — combined with structural enforcement mechanisms and paired with positive behavioral alternatives reduce hallucination more effectively than standalone prohibition instructions." This is explicitly labeled an **alternative hypothesis** generated from synthesis findings. It is a different, more complex claim than the original working hypothesis and should not replace it for Phase 2 testing purposes. Phase 2 should test the original hypothesis directly while documenting this alternative as a secondary outcome of interest. This hypothesis is positioned at the end of L0 to prevent anchoring Phase 2 analysts to a synthesis-generated secondary claim before the primary null finding and Phase 2 mandate have been absorbed (DA-002-R2 fix).

---

## Known Scope Exclusions

> **Added in Revision 2 to address IN-001 (Critical) and RT-003 (Major); SE-5 added in Revision 3 to address RT-001-R2 (publication bias).** This section explicitly documents the evidence domains structurally excluded from all three surveys. These exclusions bound the validity of this synthesis's conclusions.

The synthesis draws its conclusions from three evidence sources: peer-reviewed academic literature (indexed in academic databases), practitioner industry blogs and vendor documentation, and major framework library documentation. The following evidence domains were structurally absent from all three surveys and could contain evidence that would alter the synthesis conclusions.

### SE-1: Closed Production Deployments

No survey captured evidence from proprietary enterprise LLM deployments. Companies operating production LLM systems (financial services, healthcare, legal, customer service) may have conducted internal A/B tests of negative vs. positive prompting strategies that are not published and not accessible through academic or industry search. If 60% hallucination reduction has been observed in controlled production settings with expert-engineered prompts, this evidence would not appear in any of the three surveys. The synthesis cannot rule out this possibility; it can only report on the published and publicly documented evidence base.

### SE-2: Domain-Specific Expert Applications

The surveys did not systematically cover domain-specific applications where precise negative constraint expression may be operationally standard and effective. Legal, medical, financial, and regulatory AI applications may rely on prohibition language ("NEVER provide legal advice," "DO NOT diagnose conditions") as a safety-critical requirement, with different compliance and accuracy profiles than general-purpose applications. Expert prompt engineers in these domains may have discovered effective negative prompting patterns that are not generalized to published guidance.

### SE-3: Internal Vendor Benchmarks and Unpublished Research

Anthropic, OpenAI, Google, and other major AI providers likely conduct internal benchmarking of instruction formats including positive vs. negative framing. Their published guidance ("prefer positive framing") may reflect internal experimental findings not released publicly. The synthesis can only interpret the published recommendations; it cannot verify whether they are supported by unpublished internal controlled experiments.

### SE-4: Grey Literature from Expert Practitioner Communities

Academic search indexed peer-reviewed publications; industry search covered practitioner blogs and vendor documentation. Detailed technical discussions in private Slack communities, internal company wikis, enterprise prompt engineering teams, and consulting firm proprietary playbooks were not captured. These sources may contain high-quality practitioner evidence on negative prompting effectiveness that is simply not public.

### SE-5: Publication Bias in Academic Venue Indexing

Academic search preferentially indexes published results. Studies demonstrating effective negative prompting techniques may have been conducted and submitted to academic venues but not accepted for publication. The "file drawer problem" (unpublished null results or affirmative results that contradict reviewer expectations) may affect the academic survey component's representation of the field. Academic journals in NLP and AI tend to publish papers documenting capability failures and limitations more readily than papers documenting "prompting technique X works" without a theoretically novel contribution. This synthesis cannot quantify the extent of this bias. The null finding on the 60% hypothesis may partially reflect publication patterns rather than a complete absence of positive evidence. (Added RT-001-R2 fix — standard systematic review limitation per Cochrane Handbook and PRISMA guidelines.)

**Implication for synthesis conclusions:** The null finding ("no evidence for 60% hallucination reduction") applies specifically to the publicly documented evidence base across these three survey domains. It does not exclude the possibility that such evidence exists in the excluded domains above. This distinction is critical for Phase 2 framing: Phase 2 generates the first publicly documented controlled evidence, not necessarily the first evidence of any kind.

---

## L1: Merged Source Catalog

### Deduplication Protocol

Sources were deduplicated by paper identity (same arXiv ID, DOI, or equivalent URL treated as one entry regardless of how many surveys cited it). Cross-survey appearances are noted in the "Surveys" column. Evidence tiers follow the academic survey's taxonomy (Tier 1 = top peer-reviewed venues; Tier 2 = established venues / workshops with peer review; Tier 3 = arXiv preprints / unreviewed; Tier 4 = library docs / vendor documentation / practitioner sources).

### Group A: Academic Sources (from academic-survey.md)

| ID | Title (abbreviated) | Authors | Year | Venue | Tier | Surveys | Key Finding |
|----|--------------------|---------|----|-------|------|---------|-------------|
| A-1 | NegativePrompt: Leveraging Psychology | Wang, Li, Chang et al. | 2024 | IJCAI 2024 | 1 | Academic | Negative emotional stimuli improve LLM performance: +12.89% (Instruction Induction), +46.25% (BIG-Bench) |
| A-2 | Understanding Impact of Negative Prompts (diffusion) | Ban, Wang, Zhou et al. | 2024 | arXiv | 3 | Academic | Negative prompts in diffusion models: delayed effect + deletion-through-neutralization in latent space. Cross-modality analogy only — not validated for LLMs. |
| A-3 | This is not a Dataset (negation benchmark) | Garcia-Ferrero, Altuna et al. | 2023 | EMNLP 2023 | 1 | Academic | LLMs proficient on affirmative but struggle with negative sentences (~400K examples). |
| A-4 | Language models are not naysayers | Truong, Baldwin, Verspoor, Cohn | 2023 | *SEM 2023 | 2 | Academic | Inverse scaling on negation; instruction-tuning outperforms scaling. |
| A-5 | Negation: A Pink Elephant in the LLMs' Room? | Vrabcova, Kadlcik et al. | 2025 | arXiv | 3 | Academic | Size-negation correlation r=0.867 in newer models (Llama 3, Qwen 2.5, Mistral); partially reverses earlier inverse scaling. |
| A-6 | Power of Negation in Fostering LLM Hallucinations | Varshney, Raj et al. | 2024 | arXiv | 3 | Academic | **Tier 3 — not replicated.** Negation increases hallucination in MCQA contexts; LLaMA-2: 26%→59% on specific tasks. Scope limited to one model family, four MCQA tasks, 100-300 instances. See AGREE-6 for full caveats. |
| A-7 | Refusal Mediated by a Single Direction | Arditi, Obeso et al. | 2024 | NeurIPS 2024 | 1 | Academic | Refusal is a one-dimensional subspace across 13 models up to 72B; explains brittleness of safety alignment. |
| A-8 | VLMs Do Not Understand Negation (NegBench) | Alhamoud, Alshammari et al. | 2025 | CVPR 2025 | 1 | Academic | VLMs at chance on negation; fine-tuning yields +10% recall, +28% accuracy. Extends negation failure to multimodal systems. |
| A-9 | Inverse Scaling: When Bigger Isn't Better | McKenzie, Lyzhov et al. | 2023 | TMLR | 2 | Academic + Industry (I-18 = LessWrong announcement) | Performance degrades beyond ~10^22 FLOPs on negation tasks (2022-2023-era models). Competition-sourced selection bias noted. |
| A-10 | Constitutional AI: Harmlessness from AI Feedback | Bai, Kadavath et al. (Anthropic) | 2022 | arXiv | 3 | Academic | Principle-based negative constraints enable training-time alignment without human labels. Effective at training time, not inference time. |
| A-11 | Contrastive Chain-of-Thought Prompting | Chia, Chen et al. | 2023 | arXiv | 3 | Academic | Including both valid and invalid reasoning: +16.0 on Bamboogle, +9.8 on GSM-8K. |
| A-12 | EmotionPrompt | Li, Wang, Zhang et al. | 2023 | LLM@IJCAI'23 | 2 | Academic | Emotional stimuli: +8% (Instruction Induction), +115% (BIG-Bench), +10.9% (generative). Non-archival IJCAI symposium (single-blind peer review). |
| A-13 | Sensitivity to Spurious Features in Prompt Design | Sclar, Choi et al. | 2024 | ICLR 2024 | 1 | Academic | Up to 76 accuracy-point swings from formatting variation alone. Instruction tuning does not eliminate sensitivity. |
| A-14 | Prompt Sentiment: The Catalyst for LLM Change | Gandhi, Gandhi (Joyspace AI) | 2025 | arXiv | 3 | Academic | Negative prompts reduce factual accuracy by 8.4% (92.3%→84.5%); responses 17.6% shorter. Commercially affiliated, not peer-reviewed, N=500. Sole study directly comparing positive/neutral/negative framing on factual accuracy. Requires independent replication. |
| A-15 | LLM Self-Correction with DeCRIM | Ferraz, Mehta et al. | 2024 | EMNLP 2024 | 1 | Academic | Atomic constraint decomposition improves Mistral by 7.3% (RealInstruct), 8.0% (IFEval). GPT-4 fails >21% of constraints. |
| A-16 | Curse of Instructions | Harada, Yamazaki et al. | 2024 | **Rejected ICLR 2025** | — | Academic | **REJECTED PAPER — peer review identified concerns.** Success rate follows p^N for N instructions; 10 constraints at 90% individual rate = 34.9% combined. Methodology plausible but use with caution. |
| A-17 | IFEval | Zhou, Lu et al. (Google) | 2023 | arXiv | 3 | Academic | 25 verifiable instruction types; foundational benchmark. Widely adopted. |
| A-18 | Do LLMs Know When They Follow Instructions? | Heo, Heinze-Deml et al. (Apple) | 2024 | arXiv | 3 | Academic | Linear probes achieve 0.7-0.88 AUROC; models "know" before generation whether they'll comply. |
| A-19 | The Instruction Gap | Tripathi, Allu, Ahmed (Yellow.ai) | 2026 | arXiv | 3 | Academic + Context7 (C-18) | 660-1,330 violations per 600 samples across 13 models; accuracy and compliance are independent capabilities. |
| A-20 | Control Illusion: Failure of Instruction Hierarchies | Geng, Li et al. | 2025 | AAAI 2026 | 1 | Academic | System/user prompt separation fails to establish reliable instruction hierarchy. Social priors > formal roles. |
| A-21 | Prompting and External Tools in Hallucination Rates | Barkley, van der Merwe (Stellenbosch) | 2024 | arXiv | 3 | Academic | Self-Consistency 84.89% on GSM8K; external tools deteriorate smaller model performance. Single 8B model, 3 runs — low statistical confidence. |
| A-22 | Chain-of-Verification (CoVe) | Dhuliawala, Komeili et al. (Meta) | 2023 | ACL 2024 | 1 | Academic | Precision doubles on Wikidata (0.17→0.36); hallucinated entities 2.95→0.68. Verification pipeline, NOT negative prompting. |
| A-23 | Improving Negation Reasoning via Prompt Engineering | Barreto, Jana | 2025 | EMNLP 2025 | 1 | Academic | Warning-based prompts: +3.17% overall, +25.14% distractor negation accuracy. Most actionable finding for PROJ-014 prompt engineering. **Single study — replication not yet established.** |
| A-24 | SORRY-Bench | Xie, Qi et al. | 2024 | ICLR 2025 | 1 | Academic | 44-class safety taxonomy; refusal behavior varies dramatically by model and linguistic framing. |
| A-25 | Emergent Misalignment | Betley, Tan et al. | 2025/2026 | Nature (Jan 2026) | 1 | Academic | Fine-tuning on narrow negative behaviors produces broad misalignment (>80% insecure code, ~20% misaligned unrelated). |
| A-26 | Bounding LLM Capabilities with Prompt Constraints | Lu, Zhang et al. | 2023 | EACL 2023 | 2 | Academic | Structural/stylistic constraints expose consistent failure modes across model families. |
| A-27 | LogicBench | Parmar, Patel et al. | 2024 | ACL 2024 | 1 | Academic | All inference rules with poor performance involve negated premises. Logical reasoning from negated premises fails. |
| A-28 | CAST: Conditional Activation Steering | Lee, Padhi et al. (IBM+UPenn) | 2024 | ICLR 2025 Spotlight | 1 | Academic | Harmful refusal 45.78%→90.67% on Qwen 1.5B; harmless refusal stays at 2.20%. Model-internal technique — not reproducible via prompt engineering. |
| A-29 | Thunder-NUBench | So, Lee et al. | 2025 | arXiv | 3 | Academic | Sentence-level negation benchmark contrasting standard vs. local negation. Abstract-only review. |
| A-30 | LLM Instruction Following: A Survey | Lou, Zhang, Yin | 2024 | Computational Linguistics (MIT Press) | 2 | Academic | Comprehensive meta-survey of instruction-following challenges. Contextualizes negative constraint adherence. |
| A-31 | Principled Instructions Are All You Need (Bsharat et al.) | Bsharat, Myrzakhan, Shen | 2023 | arXiv | 3 | Academic (added R2) | Affirmative directives showed 55% improvement and 66.7% correctness increase for GPT-4. **Primary paper for the 55% figure cited via I-13 (PromptHub secondary source) in AGREE-4.** arXiv:2312.16171. |

> **Revision 2 note (CV-001):** A-31 (Bsharat et al., 2023, "Principled Instructions Are All You Need," arXiv:2312.16171) was added to the catalog to provide a direct primary citation for the 55% affirmative-directives improvement figure referenced in AGREE-4. This figure was previously cited only through I-13 (PromptHub, a secondary source). A-31 is Tier 3 (arXiv preprint); it should be cited as the primary source, with I-13 noted as the secondary reference.

### Group I: Industry-Unique Sources (from industry-survey.md, not already in Group A or Group C)

| ID | Title (abbreviated) | Org/Author | Year | Type | Tier | Key Finding |
|----|--------------------|-----------|----|------|------|-------------|
| I-1 | Prompting Best Practices (Claude 4) | Anthropic | 2025 | Vendor docs | 4 | "Tell Claude what to do instead of what not to do." Aggressive NEVER/CRITICAL language actively hurts newer models. |
| I-2 | Prompt Engineering Guide (Tips) | DAIR-AI / PromptingGuide.ai | 2024 | Community guide | 4 | "Avoid saying what not to do but say what to do instead." Movie chatbot example: DO NOT ASK instructions violated. |
| I-3 | Prompt Engineering (OpenAI API docs) | OpenAI | 2024 | Vendor docs | 4 | "Instead of just saying what not to do, say what to do instead." Customer service negative-to-positive reframing. |
| I-4 | GPT-4.1 Prompting Guide | OpenAI | 2025 | Vendor docs | 4 | GPT-4.1 follows instructions more literally; mandatory "always" constraints cause hallucinated tool inputs. |
| I-5 | GPT-5 Prompting Guide | OpenAI | 2025 | Vendor docs | 4 | Domain-specific unambiguous negatives work ("NEVER add copyright headers"); contradictory negatives waste reasoning tokens. |
| I-6 | Gemini API Prompt Design Strategies | Google | 2024 | Vendor docs | 4 | Examples > anti-patterns; complex requests may silently drop negative constraints. |
| I-7 | Gemini 3 Prompting Guide | Google Cloud | 2025 | Vendor docs | 4 | Place negative constraints at end of instructions; "semantic negative prompts" for image generation. |
| I-8 | Pink Elephant Problem article | 16x Engineer / Eval | 2025 | Blog | 4 | Connects LLM negative instruction failure to Ironic Process Theory. Anecdotal; no controlled experiments. Also in Context7 C-16. |
| I-9 | LLMs and the "not" problem | Sean Trott (Substack) | 2024 | Blog | 4 | Cites Ettinger (2020) BERT study; recommends positive framing. |
| I-10 | Using Negative AI Prompts Effectively | Virtualization Review / Posey | 2025 | Blog | 4 | Hard vs. soft negatives taxonomy; keep constraint lists "concise but targeted." |
| I-11 | Prompt Engineering Best Practices 2026 | Thomas Wiegold | 2026 | Blog | 4 | Pink Elephant Problem; reasoning degrades at ~3,000 tokens. |
| I-12 | Claude Prompt Engineering: 25 Techniques | DreamHost | 2025 | Blog (systematic testing) | 4 | Avoiding negative phrasing "significantly improves results" — before/after pairs tested. Methodology not disclosed. |
| I-13 | Prompt Engineering Principles 2024 (26 Principles) | PromptHub / Cleary | 2024 | Blog (secondary citation) | 4 | Cites Bsharat et al. (A-31): affirmative directives showed 55% improvement for GPT-4. **Secondary source — see A-31 for primary citation.** Also context7 C-15 (partial). |
| I-14 | Impact of Prompt Bloat on LLM Output Quality | MLOps Community | 2025 | Blog (empirical) | 4 | Reasoning degrades at ~3,000 tokens; "identification without exclusion" — models recognize but still incorporate irrelevant info; CoT does not mitigate long-prompt degradation. |
| I-15 | Effective Context Engineering for AI Agents | Anthropic Engineering | 2025 | Vendor docs | 4 | "Strong heuristics over exhaustive constraint lists." Treats context as finite resource. |
| I-16 | Writing a Good CLAUDE.md | HumanLayer | 2025 | Blog | 4 | Frontier LLMs follow ~150-200 instructions (estimate, methodology not disclosed); quality decreases uniformly as count increases. **Unverified practitioner estimate — see Unsourced Claim Audit.** |
| I-17 | Stop Claude Code from Forgetting the Rules | DEV Community / Siddhant K | 2025 | Blog | 4 | ~95% compliance at messages 1-2; drops to 20-60% by messages 6-10. Practitioner observation; methodology not disclosed. **Unverified practitioner estimate — see Unsourced Claim Audit.** |
| I-18 | Inverse Scaling Prize: Round 1 Winners | LessWrong / Inverse Scaling Project | 2023 | Community discussion | 4 | Larger LMs perform worse than random on negated instructions in specific range. Academic paper A-9 covers formal analysis. |
| I-19 | Palantir Best Practices for LLM Prompt Engineering | Palantir | 2024 | Vendor docs | 4 | Balanced approach: treats negatives as standard tools; recommends clear constraints for scope control. |
| I-20 | Building Simple & Effective Prompt-Based Guardrails | QED42 | 2025 | Blog (empirical) | 4 | "Power of examples far exceeds the power of instructions." Two-tier approach: GPT-4o generates examples, smaller models deploy them. |
| I-21 | DSPy Assertions | Stanford NLP / Arize AI | 2024 | Framework docs | 4 | Constraints pass 164% more often with dspy.Assert; 37% more high-quality responses. Framework documentation (see C-13 for the academic preprint). |
| I-22 | Common LLM Prompt Engineering Challenges | Latitude | 2025 | Blog | 4 | Negative instructions introduce "shadow information"; tools cut iteration time 30%, consistency 25% (unverified). **Flagged — see Unsourced Claim Audit.** |
| I-23 | Ultimate Guide to Prompt Engineering 2026 | Lakera AI | 2026 | Blog | 4 | "Negative instructions are weaker than positive structural guidance." Also context7 C-17. |
| I-24 | Prompt Engineering Best Practices | DigitalOcean | 2025 | Blog | 4 | Larger models perform worse on negated prompts; negation "increases cognitive load." |
| I-25 | How to Use AI Negative Prompts | ClickUp | 2025 | Blog | 4 | Pair negatives with detailed positive instructions; excessive restrictions produce "flat, generic content." |
| I-27 | NeMo Guardrails | NVIDIA | 2024 | Framework docs | 4 | Programmatic Colang-based rails; multi-stage constraint enforcement at infrastructure level. |
| I-28 | Claude Code Ignores the CLAUDE.md | Christoph Schweres (Medium) | 2026 | Blog | 4 | NEVER rules particularly prone to being dropped during context compaction. |
| I-29 | Prompt Engineering with Guardrails: Safety Design | Endtrace | 2025 | Blog | 4 | Layered defense: prompt engineering + guardrail systems; safety directives typically written as negatives. |
| I-30 | Profound Impact of Prompt Variations | The Big Data Guy (Substack) | 2024 | Blog (sentiment study) | 4 | Negative sentiment decreases factual accuracy 8.4%; positive 2.8% reduction; neutral best. Measures *emotional sentiment*, not instruction syntax — related but distinct phenomenon. |
| I-31 | Negative Prompting Notebook | Nir Diamant (GitHub) | 2025 | Framework tutorial | 4 | Hands-on LangChain-based tutorial covering basic negative examples, exclusions, constraint implementation. Community tutorial, not official LangChain docs. |
| I-32 | Claude Code Bug Reports (#5055, #6120, #15443, #18660) | Anthropic GitHub | 2025-2026 | Community forum | 4 | Multiple reports of Claude Code ignoring CLAUDE.md NEVER/DO NOT rules; instructions "read but not reliably followed." |

### Group C: Context7-Unique Sources (not already in Group A or Group I)

> **R3 note (SR-001-R2/CV-001-R2/FM-011 fix):** All 13 Group C unique sources are now explicitly named with IDs. The catalog below includes BOTH the 13 net-unique Group C entries AND the deduplicated entries (C-1, C-4, C-5) for completeness; deduplicated entries are marked and excluded from the count. The 13 Group C unique sources are: C-2, C-3, C-6, C-7, C-8, C-9, C-10, C-11, C-12, C-13, C-14, C-19, C-20.

| ID | Title (abbreviated) | Org/Author | Year | Authority | Tier | Key Finding | Count Status |
|----|--------------------|-----------|----|-----------|------|-------------|--------------|
| C-1 | Anthropic Claude Prompting Best Practices (direct URL, platform.claude.com) | Anthropic | 2025 | HIGH | 4 | Specific XML-wrapped negative constraint patterns: `<do_not_act_before_instructions>`, NEVER in `<avoid_excessive_markdown>`. Tension: recommends positive but uses extensive negative in own prompts. | **DEDUPLICATED** — same source as I-1. Counted under I-1. |
| C-2 | Anthropic Prompt Engineering Blog (claude.com/blog/best-practices-for-prompt-engineering) | Anthropic | 2025 | HIGH | 4 | Canonical "tell Claude what to do" recommendation. Distinct URL and publication from C-1/I-1 (platform docs vs. blog). Same vendor, different document. | **COUNTED** — distinct URL from I-1/C-1. |
| C-3 | OpenAI Prompt Engineering Guide (platform.openai.com/docs/guides/prompt-engineering) | OpenAI | 2025 | HIGH (inaccessible — 403) | 4 | Primary OpenAI platform docs; "say what to do instead of what not to do." Distinct from I-3 (community guide citing OpenAI) and I-4/I-5 (cookbook guides). Inaccessible at 403 but referenced in context7 survey. | **COUNTED** — distinct URL from I-3 and cookbook guides. |
| C-4 | OpenAI GPT-4.1 Prompting Guide (Cookbook) | OpenAI | 2025 | HIGH | 4 | Mandatory "always" constraints cause hallucinated tool inputs; conditional positive escape clause recommended. | **DEDUPLICATED** — same source as I-4. Counted under I-4. |
| C-5 | OpenAI GPT-5 Prompting Guide (Cookbook) | OpenAI | 2025 | HIGH | 4 | Contradictory negative instructions cause failures. | **DEDUPLICATED** — same source as I-5. Counted under I-5. |
| C-6 | OpenAI GPT-5.1 Prompting Guide | OpenAI | 2025 | HIGH | 4 | Paired negative-positive patterns ("Do NOT guess...ask for detail"). NEW to context7 survey. | **COUNTED** |
| C-7 | OpenAI GPT-5.2 Prompting Guide | OpenAI | 2025 | HIGH | 4 | Explicit negative constraints for scope control: "Do NOT invent colors"; model requires explicit instructions; poorly-constructed prompts more damaging to GPT-5.2 than earlier models. NEW to context7 survey. | **COUNTED** |
| C-8 | LangChain Prompt Templates Reference | LangChain | 2025 | HIGH | 4 | Silent on negative vs. positive framing. Structural enforcement only. NEW (framework docs). | **COUNTED** |
| C-9 | LangChain Guardrails Documentation | LangChain | 2025 | HIGH | 4 | ContentFilterMiddleware (negative blocking) and PIIMiddleware (positive transformation) code examples. NEW (framework docs). | **COUNTED** |
| C-10 | LlamaIndex Prompts Documentation | LlamaIndex | 2025 | HIGH | 4 | Silent on framing guidance. NEW (framework docs). | **COUNTED** |
| C-11 | LlamaIndex Default Prompts Source Code | LlamaIndex | 2025 | HIGH | 4 | Default prompts use 6 negative instructions: "Never query all columns," "Do NOT fill in vector values," etc. NEW (source code). | **COUNTED** |
| C-12 | DSPy Assertions Documentation (dspy.ai/learn/programming/7-assertions/) | DSPy / Stanford NLP | 2025 | HIGH | 4 | Official framework docs: dspy.Assert (hard constraints with backtracking), dspy.Suggest (soft constraints). Distinct from I-21 (community tutorial/Arize AI) and C-13 (academic preprint). | **COUNTED** — distinct document from I-21 and C-13. |
| C-13 | DSPy Assertions Paper | Singhvi, Shetty et al. (Stanford NLP) | 2023 | MEDIUM (arXiv preprint) | 3 | arXiv:2312.13382. **Tier 3 preprint — no confirmed peer-reviewed venue identified as of 2026-02-27.** 164% compliance improvement and 37% high-quality responses from dspy.Assert. Evidence tier updated from "accepted" to Tier 3 pending venue confirmation. | **COUNTED** — distinct from C-12 (docs) and I-21 (community tutorial). |
| C-14 | DSPy Official Site (dspy.ai/) | DSPy | 2025 | HIGH | 4 | "Programming — not prompting — language models" philosophy renders framing question moot. Distinct from C-12 (assertions docs page) and C-13 (paper). | **COUNTED** — distinct URL and content from C-12 and C-13. |
| C-19 | When Models Can't Follow (Young, Gillins, Matthews) | arXiv:2510.18892 | 2025 | MEDIUM (preprint) | 3 | 256 LLMs, 20 instruction types: 43.7% overall pass rate; constraint compliance 66.9% highest category; binary pass/fail distribution. NEW — not in academic or industry surveys. | **COUNTED** |
| C-20 | Prompt Builder OpenAI Guide | promptbuilder.cc | 2026 | MEDIUM | 4 | "Negative instructions are harder for models to follow than positive ones"; hybrid approach recommended. NEW. | **COUNTED** |

> **Revision 2 note (CV-002):** C-13 (DSPy Assertions paper, arXiv:2312.13382) was previously described as "accepted at venue." No peer-reviewed venue has been identified after verification. The description has been corrected to reflect its Tier 3 arXiv preprint status. The 164% compliance improvement figure should be cited with this tier qualification.

**Note on deduplication decisions:**

- I-1 / C-1 are the same document (Anthropic platform docs, platform.claude.com). Counted ONCE as I-1. C-2 (Anthropic Prompt Engineering Blog, claude.com/blog) is a distinct URL and distinct document — counted separately as its own entry in Group C. (SR-002-R3 fix: prior deduplication table incorrectly grouped C-2 with I-1/C-1; corrected in R4.)
- I-4 / C-4 are the same source (GPT-4.1 cookbook). Counted ONCE.
- I-5 / C-5 are the same source (GPT-5 cookbook). Counted ONCE.
- I-8 / C-16 are the same source (Pink Elephant, 16x.engineer). Counted ONCE as I-8.
- I-13 / C-15 reference the same PromptHub/DAIR-AI pages. Counted as 2 entries: I-13 (PromptHub) and I-2 (DAIR-AI PromptingGuide.ai, which appears as C-15 in context7).
- I-21 (DSPy community tutorial / Arize AI) + C-12 (official DSPy assertions docs) + C-13 (academic preprint) + C-14 (DSPy site) = FOUR distinct source documents across three DSPy-related entries. I-21 is a community tutorial; C-12 is official docs; C-13 is the academic paper; C-14 is the site overview. Counted as FOUR distinct entries: I-21 in Group I, C-12/C-13/C-14 in Group C.
- A-19 / C-18 are the same paper (Tripathi et al., arXiv:2601.03269). Counted ONCE as A-19.
- I-23 / C-17 are the same source (Lakera). Counted ONCE as I-23.
- C-3 (OpenAI platform docs, 403) is distinct from I-3 (community guide/OpenAI API docs) — different URLs and publication types.

---

## L1: Agreements — Cross-Survey Corroboration

Each agreement below identifies findings where 2 or more surveys independently reached the same conclusion without cross-referencing each other. Agreement strength: **Strong** = all 3 surveys agree (AGREE-1 through AGREE-5); **Moderate** = 2 of 3 surveys agree (AGREE-6 through AGREE-9). A per-agreement confidence qualifier is provided based on evidence tier.

---

### AGREE-1: No Peer-Reviewed Evidence Supports the 60% Hallucination Reduction Claim [STRONG] [Confidence: HIGH]

**Agreement: All 3 surveys.**

- **Academic survey:** "No peer-reviewed study validates a 60% hallucination reduction from negative prompting. The closest evidence is Varshney et al. (2024, Source A-6), which shows negation *increases* hallucination by ~33 percentage points on specific tasks." (academic-survey.md, PROJ-014 Hypothesis Context section)
- **Industry survey:** "The evidence landscape is predominantly vendor recommendations and practitioner anecdotes; rigorous empirical comparisons are scarce. No source in this survey provides a controlled A/B test directly comparing negative vs. positive instruction variants at scale in production." (industry-survey.md, L0 Evidence Landscape Assessment)
- **Context7 survey:** "No vendor documentation, framework guide, or academic paper surveyed provides quantitative evidence for a 60% hallucination reduction through negative prompting... The guidance across all sources is prescriptive, not evidence-based." (context7-survey.md, Key Finding 3)

**Resolution:** Confirmed null finding across all three independent search strategies. The 60% claim is an informal practitioner figure without a traceable primary source. **This is a null finding (untested), not a refutation (tested and found false).** Phase 2 must generate this evidence rather than locate it.

---

### AGREE-2: The Absence of Controlled A/B Comparisons Is the Critical Research Gap [STRONG] [Confidence: HIGH]

**Agreement: All 3 surveys.**

- **Academic survey:** "No paper in this survey directly compares identical constraints framed as 'don't do X' versus 'always do Y' in controlled A/B experiments -- this remains the critical research gap." (academic-survey.md, L0 Executive Summary, phenomenon b)
- **Industry survey:** Gap #1: "No large-scale production A/B tests comparing negative vs. positive instruction variants." Gap #8: "No comparison of negative instruction effectiveness in system prompt vs. user turn placement." (industry-survey.md, Gaps Identified)
- **Context7 survey:** Coverage Gap #1: "Zero surveyed sources provide controlled experimental data specifically comparing negative vs. positive prompting effectiveness with matched prompts and measurable hallucination metrics." (context7-survey.md, Coverage Gaps)

**Resolution:** This gap is confirmed by all three surveys using independent search strategies across academic databases, practitioner literature, and framework documentation. Phase 2 experimental design should close this gap by constructing matched framing pairs per the methodology documented in context7-survey.md Phase 2 Task Mapping section.

---

### AGREE-3: Vendor Best Practice Is Positive Framing; Anthropic, OpenAI, and Google All Recommend It [STRONG] [Confidence: HIGH for vendor recommendation; MEDIUM for generalizability]

**Agreement: All 3 surveys.**

- **Academic survey:** While the academic survey does not survey vendor docs directly, it cites Anthropic's Constitutional AI (A-10) as operating at training time and notes that vendors distinguish training-time versus inference-time constraints — implicitly acknowledging the vendor preference pattern.
- **Industry survey (primary evidence):** "Three of four major platform vendors recommend positive framing over negative framing for behavioral control (Anthropic, OpenAI, Google); Palantir takes a balanced approach." Concrete quotes from each vendor documented in Theme 1. (industry-survey.md, L0 and Theme 1)
- **Context7 survey (primary evidence):** "Both Anthropic and OpenAI explicitly recommend positive framing over negative instructions as the default approach." Coverage Matrix shows all vendors that address the topic recommend positive framing. (context7-survey.md, Key Finding 1)

**Evidence:** Anthropic: "Tell Claude what to do instead of what not to do" (I-1/C-1). OpenAI: "Instead of just saying what not to do, say what to do instead" (I-3/C-3). Google: "Use examples to show patterns to follow, not anti-patterns to avoid" (I-6/C-6).

**Caveat noted by industry survey:** This recommendation applies to the current model generation. OpenAI's GPT-4.1 and GPT-5 guides document that newer models follow negative instructions more literally, suggesting the gap between negative and positive framing effectiveness may be narrowing in frontier models. The recommendation reflects the balance of evidence across 2023-2026 sources. See Known Scope Exclusions SE-1 and SE-3: this vendor recommendation may be supported by unpublished internal experimentation not captured in this synthesis.

**Caveat on vendor neutrality (DA-001-R2 fix):** Vendor recommendations for positive framing should be interpreted with an additional consideration: vendor models are fine-tuned and optimized against their own test suites and prompting guidance. The recommendation "use positive framing" may partially reflect that these specific models are better-tuned to respond to positive framing through their training regimes — rather than a universal property of all LLMs or all model architectures. This would be a form of circular optimization: recommending what their own models were optimized to follow. Known Scope Exclusions SE-3 acknowledges that internal vendor benchmarks exist but may not be published. PROJ-014's Phase 2 multi-model testing across different vendors (not just the recommending vendors) would help identify whether the positive-framing advantage is universal or vendor-specific.

---

### AGREE-4: Prohibition-Style Negative Instructions Are Unreliable as Standalone Mechanisms [STRONG] [Confidence: HIGH for direction; MEDIUM for specific magnitudes]

**Agreement: All 3 surveys.**

**Primary academic evidence (Tier 1/2, leading citations):**

- Source A-20 (Geng et al., AAAI 2026, **Tier 1**): system prompt instruction hierarchies fail even for formatting conflicts — direct experimental evidence.
- Source A-19 (Tripathi et al., 2026, Tier 3 but large-scale): 660-1,330 violations per 600 samples across 13 models. (academic-survey.md, L0 phenomenon b)
- Source A-31 (Bsharat et al., 2023, Tier 3): affirmative directives showed 55% improvement and 66.7% correctness increase for GPT-4 vs. prohibitions. [Primary citation — see CV-001 fix; I-13 was a secondary citation through PromptHub]

**Corroborating evidence (lower tier, use with caveats):**

- Source A-16 (Harada et al., **rejected ICLR 2025** — use with caution): success rate follows p^N for N instructions; 10 constraints at 90% individual rate = 34.9% combined. Methodology plausible but rejection status means reliance on this specific quantification should be limited.

- **Industry survey:** Theme 2 quantitative findings: Bsharat et al. (via Source I-13, secondary source — primary is A-31): affirmative directives showed 55% improvement over prohibitions for GPT-4. DreamHost (I-12): avoiding negative phrasing "significantly improves results." Instruction count degradation: compliance drops from ~95% to 20-60% over conversation length (I-17, unverified practitioner observation). (industry-survey.md, Theme 2)
- **Context7 survey:** "The surveyed evidence suggests that the negative-vs-positive distinction is less important than instruction specificity, pairing prohibitions with positive alternatives, and structural enforcement mechanisms." NP-004 pattern: structural constraint > linguistic constraint. (context7-survey.md, L0 Hypothesis Verdict and NP-004)

**Strength note:** This agreement is the most consistent finding across all surveys. Every survey, using independent evidence bases, reached the conclusion that standalone prohibition instructions are unreliable. The primary quantitative evidence rests on A-20 (Tier 1) and A-31 (Tier 3); A-16 is corroborating but from a rejected paper.

**Note on circular citation risk (RT-004; DA-002-R3/RT-001-R3 fix):** Some industry blog sources citing prohibition unreliability trace back through each other and ultimately to A-9 (McKenzie et al. inverse scaling). The academic base for this agreement is broader than the industry citation network implies, with independent academic sources at different tier levels: A-20 (Tier 1, AAAI 2026) and A-19 (Tier 3, large-scale 13-model study) provide the strongest academic evidence; A-31 (Bsharat et al., arXiv, Tier 3 unreviewed) provides corroborating but lower-tier evidence. A Tier 3 unreviewed preprint provides less independent validation than a Tier 1 peer-reviewed paper; the claim that the academic base is broader than the industry citation network should be understood primarily in reference to A-20 and A-19, not A-31.

**Note on expert user moderating variable (IN-001-R3 fix):** The AGREE-4 failure rates documented above are aggregate findings across many studies and users. A moderating variable not controlled in any current evidence is user expertise: expert prompt engineers who understand model-specific constraint design may achieve better compliance with prohibition-style instructions than non-expert users. None of the studies cited in AGREE-4 control for this variable. Phase 2 experimental design should either standardize experimenter expertise or treat it as an explicit independent variable, to prevent results confounded by experimenter skill levels.

---

### AGREE-5: Structured Alternatives Outperform Blunt Prohibition [STRONG] [Confidence: HIGH for direction; varies by specific technique]

**Agreement: All 3 surveys.**

- **Academic survey:** Source A-15 (DeCRIM, EMNLP 2024, Tier 1): atomic decomposition improves compliance 7.3-8.0%. Source A-23 (Barreto & Jana, EMNLP 2025, Tier 1): warning-based meta-prompts improve negation accuracy up to 25.14%. Source A-22 (CoVe, ACL 2024, Tier 1): verification pipeline doubles precision on Wikidata tasks. Source A-28 (CAST, ICLR 2025, Tier 1): model-internal steering achieves 90.67% harmful refusal. (academic-survey.md, L0)
- **Industry survey:** Source I-20 (QED42): "the power of examples far exceeds the power of instructions." Source I-21 (DSPy framework docs): constraints pass 164% more often with programmatic assertions; 37% more high-quality responses (figures from framework docs, see C-13 for academic preprint at Tier 3). Source I-27 (NeMo Guardrails): infrastructure-level constraint enforcement. Theme 5: structural constraint as superior pattern. (industry-survey.md, Themes 3 and 6)
- **Context7 survey:** NP-004 pattern ("Structural Constraint Over Linguistic Constraint"): LangChain OutputFixingParser, StructuredOutputParser, DSPy dspy.Assert, and prompt scaffolding all outperform linguistic framing. DSPy's backtracking injects negative feedback automatically without manual negative instruction authoring. (context7-survey.md, Pattern Convergence NP-004)

**Effectiveness hierarchy (synthesized from all three surveys), with access-level annotation:**

> **IMPORTANT — Scope of comparison (RT-002-R2/DA-004-R2 fix):** Ranks 1–4 are NOT alternatives to prompt engineering; they operate at entirely different system layers (model-internal or training-time) with fundamentally different access requirements, cost structures, and use cases. A prompt engineer cannot implement ranks 1–4. The primary comparison relevant to PROJ-014 is within **ranks 5–12 (the prompt-engineering-accessible range)**. Do not compare ranks 1–4 against ranks 5–12 as if they were competing approaches at the same level.

| Rank | Technique | Evidence | Access Level | Notes |
|------|-----------|----------|-------------|-------|
| 1 | Model-internal interventions (CAST, A-28) | ~90% harmful refusal | Model-access required | Not achievable via prompt engineering |
| 2 | Training-time negative constraints (Constitutional AI, A-10) | Alignment without labels | Training-access required | Inference-time only for PROJ-014 scope |
| 3 | Programmatic enforcement (DSPy, I-21/C-13) | 164% compliance improvement (Tier 3 paper) | Engineering infrastructure required | Requires DSPy or equivalent |
| 4 | Verification pipelines (CoVe, A-22) | 2x precision improvement (Tier 1) | Pipeline overhead required | Not pure prompt engineering |
| 5 | Warning-based meta-prompts (A-23, EMNLP 2025) | +25.14% distractor negation (Tier 1, single study) | **Prompt-only, accessible** | Phase 2 priority; replication needed |
| 6 | Atomic constraint decomposition (DeCRIM, A-15, EMNLP 2024) | +7-8% compliance (Tier 1) | **Prompt-only, accessible** | Phase 2 priority |
| 7 | Negative emotional stimuli (NegativePrompt, A-1) | +12-46% on reasoning (Tier 1) | **Prompt-only, accessible** | Different phenomenon from prohibition |
| 8 | Contrastive examples (Contrastive CoT, A-11) | +9-16 accuracy points (Tier 3) | **Prompt-only, accessible** | Tier 3 evidence |
| 9 | Declarative behavioral negation (vendor practice, I-1, C-1) | Qualitative improvement | **Prompt-only, accessible** | No controlled measurement |
| 10 | Paired prohibition + positive alternative (NP-002, context7) | Qualitative improvement | **Prompt-only, accessible** | No controlled measurement |
| 11 | Justified prohibition + contextual reason (NP-003, context7) | Qualitative improvement | **Prompt-only, accessible** | No controlled measurement |
| 12 | Standalone blunt prohibition ("NEVER X") | Unreliable — consistent failure | **Prompt-only** | Baseline for Phase 2 |

> **Actionability note (SM-001 fix):** The access-level column distinguishes between techniques applicable in pure prompt engineering contexts (ranks 5-12) and those requiring model access, training infrastructure, or engineering infrastructure (ranks 1-4). PROJ-014 Phase 2 should focus on ranks 5-12 for direct experimental comparison with the working hypothesis.

> **Intra-subgroup rank ordering basis within ranks 5-12 (SM-001-R3/SR-004-R3 fix):** Ranks 5-6 are ordered by evidence tier: rank 5 (Warning-based meta-prompts, A-23) has Tier 1 quantitative evidence (+25.14% on a specific task); rank 6 (Atomic decomposition, A-15) also has Tier 1 evidence (+7-8% compliance on two benchmarks). Rank 5 is placed above rank 6 because of a higher magnitude improvement signal on the specific negation task type most relevant to PROJ-014, though both are Tier 1. Rank 7 (Negative emotional stimuli, A-1) is Tier 1 but addresses a different phenomenon (motivational framing) and is placed below ranks 5-6 because its relevance to prohibition instruction compliance is indirect. Rank 8 (Contrastive examples, A-11) is Tier 3 — lower than the Tier 1 techniques above it. **Ranks 9-11 are ordered by synthesizer judgment, not by controlled evidence:** rank 9 (Declarative behavioral negation) is placed before rank 10 (Paired prohibition + positive) and rank 11 (Justified prohibition + reason) based on the synthesis-observed vendor practice pattern documented in THEME-1 — specifically that declarative framing appears more common in vendor-authored system prompts than paired or justified prohibition. This is an empirically unverified ordering. Rank 12 (Standalone blunt prohibition) is placed last as the baseline that multiple independent sources identify as unreliable. Phase 2 should treat ranks 9-11 as requiring experimental comparison rather than assuming the synthesizer ordering is evidentially grounded.

---

### AGREE-6: Negation May Increase Rather Than Decrease Hallucination in Some Task Contexts [MODERATE] [Confidence: LOW — Tier 3 primary evidence, not replicated]

**Agreement: Academic + Industry surveys. Context7 does not directly address.**

> **Per-agreement confidence: LOW.** This agreement rests critically on one Tier 3 arXiv preprint (A-6). See RT-002 and full caveats below. This is the most vulnerable agreement in the synthesis.

- **Academic survey:** Source A-6 (Varshney et al., arXiv, Tier 3): LLaMA-2 MCQA hallucination rate: ~26% without negation, ~59% with negation — a ~33 percentage point increase. Knowledge augmentation worsened performance on false premises tasks by ~50%. (academic-survey.md, L0 Hallucination section and Source 6 detail) — **Scope: one research group, one model family (LLaMA-2), four MCQA tasks, 100-300 instances each.**
- **Industry survey:** Theme 2 documents the Inverse Scaling Prize finding (I-18 / A-9): larger models perform worse than random on negated instructions. DigitalOcean (I-24): negation "increases cognitive load and potential for misunderstanding." (industry-survey.md, Theme 2 and Theme 5) — **Scope: Tier 2 academic finding from 2022-2023-era models; industry source is anecdotal.**
- **Context7 survey:** Does not directly address hallucination increase from negation; notes only that no source supports the 60% reduction claim.

**Critical caveats (RT-002):**

- The primary quantitative claim (26%→59% hallucination rate increase) rests entirely on A-6 (Varshney et al.), a single Tier 3 arXiv preprint that has not been replicated in a peer-reviewed venue.
- The finding covers one model family (LLaMA-2), four specific MCQA task types, and 100-300 instances per task — a narrow scope.
- The 2022-2023 inverse scaling results (A-9, I-18) reflect an era of models that may no longer generalize to current architectures (see AGREE-3 caveat and CONFLICT-1).
- Industry evidence (I-24) is anecdotal with no controlled measurement.

**Resolution:** Moderate agreement on directionality (negation may increase rather than decrease hallucination in some contexts) but evidence quality is LOW for the primary quantitative claim. This finding should not be treated as established fact. Phase 2 should include a direct measurement of hallucination rates with positive vs. negative instruction variants on current-generation models.

---

### AGREE-7: Instruction-Following Compliance Is Independent of Output Accuracy [MODERATE] [Confidence: MEDIUM]

**Agreement: Academic + Context7 surveys.**

- **Academic survey:** Source A-19 (Tripathi et al., 2026, Tier 3): "Models that follow all instructions will not necessarily provide accurate answers, and conversely, models with high accuracy may struggle with instruction compliance." (academic-survey.md, Source 19 Key findings)
- **Context7 survey:** Context7 survey cites Tripathi et al. (C-18/A-19) with the same finding: instruction compliance varies 2x across 13 models; accuracy and compliance are separate capabilities. Young et al. (C-19): binary outcome distribution suggests compliance is about model capability, not framing. (context7-survey.md, Academic Research Findings)
- **Industry survey:** Does not directly address compliance-accuracy independence; covers instruction count degradation (I-16, I-17) but from a different angle.

**Implication:** Phase 2 experimental design must measure both compliance rate and output quality independently. A prompt formulation may achieve high compliance with a constraint while simultaneously degrading the quality of the compliant output.

---

### AGREE-8: Negative Framing Works Best When Paired with a Positive Alternative [MODERATE] [Confidence: MEDIUM]

**Agreement: Context7 + Industry surveys. Academic indirectly supports.**

- **Context7 survey:** NP-002 pattern ("Paired Negative-Positive"): "When negative instructions are used, the most effective pattern pairs the prohibition with a positive alternative." Documented across Anthropic (C-1/I-1), OpenAI GPT-5.1 (C-6), and LlamaIndex (C-11). (context7-survey.md, Pattern Convergence NP-002)
- **Industry survey:** OpenAI guidance evolution: GPT-5 and later guides actively use negatives paired with positives. ClickUp (I-25): "Recommends pairing negatives with detailed positive instructions." (industry-survey.md, Theme 1 and Theme 6 Pattern 1)
- **Academic survey:** Source A-11 (Contrastive CoT): invalid examples paired with valid examples yield +16 on Bamboogle — not prohibition, but demonstrates contrastive pairing principle. Source A-23 (Barreto & Jana): warning-based prompts (a form of meta-negative that pairs with expected behavior) yield +25.14%. (academic-survey.md, Sources 11 and 23)

**Implication:** The PROJ-014 Phase 2 experimental design should include a third condition: paired negative + positive (not just standalone negative vs. standalone positive). The paired condition may outperform either standalone condition.

---

### AGREE-9: Contextual Justification Improves Negative Instruction Effectiveness [MODERATE] [Confidence: MEDIUM]

**Agreement: Context7 + Industry surveys. Academic indirectly supports.**

- **Context7 survey:** NP-003 pattern ("Contextual Justification"): "Negative instructions are more effective when accompanied by an explanation of why the constraint exists." Example: "NEVER use ellipses since the text-to-speech engine will not know how to pronounce them." (context7-survey.md, Pattern Convergence NP-003)
- **Industry survey:** Anthropic (I-1): "NEVER use ellipses since the text-to-speech engine will not know how to pronounce them" — same example cited as effective negative instruction with contextual motivation. The distinction between the "less effective" and "more effective" versions is the addition of the reason. (industry-survey.md, Theme 1)
- **Academic survey:** Source A-23 (Barreto & Jana, EMNLP 2025, Tier 1): warning-based prompts ("be careful not to reverse the intended meaning") provide contextual framing for negation and improve accuracy up to 25.14%. The warning mechanism is structurally analogous to providing a reason for the constraint. (academic-survey.md, Source 23 detail)

**Implication:** Phase 2 prompt construction should control for contextual justification as an independent variable. A "justified negative" (prohibition + reason) may perform substantially differently from an "unjustified negative" (bare prohibition). The experimental design must either equalize justification across conditions or treat it as an additional factor.

---

## L1: Gaps — Single-Survey Claims

Claims made in only one survey with no corroboration in others. For each, the survey, the claim, and the reason for lack of corroboration are documented, along with an assessment of whether this represents a genuine knowledge gap or a scope limitation.

---

### GAP-1: 46.25% BIG-Bench Improvement from Negative Emotional Stimuli [Academic only]

**Source:** Academic survey, Source A-1 (Wang et al., IJCAI 2024).
**Claim:** Negative emotional stimuli (consequence-framing, social pressure) improve LLM performance by 46.25% on BIG-Bench.
**Why no corroboration:** This finding concerns negative *emotional* framing, not prohibition instructions. The industry survey excluded academic papers by design. The context7 survey did not encounter NegativePrompt as a library documentation source.
**Assessment:** Scope limitation (different research paradigm), not a genuine knowledge gap. The finding is well-sourced (Tier 1 venue, IJCAI main track), but its practical relevance to PROJ-014 is indirect: it addresses motivational/consequence framing, not "don't do X" constraint design.

---

### GAP-2: Warning-Based Prompts Improve Distractor Negation Accuracy by 25.14% [Academic only]

**Source:** Academic survey, Source A-23 (Barreto & Jana, EMNLP 2025, Tier 1).
**Claim:** Warning models about negation traps (e.g., "the following task contains negation — be careful not to reverse the intended meaning") improves distractor negation accuracy by up to 25.14%.
**Why no corroboration:** EMNLP 2025 is recent (2025 publication); neither the industry nor context7 survey encountered this paper. The industry survey excluded academic papers by design.
**Assessment:** Genuine knowledge gap in practitioner awareness. This is the most directly actionable academic finding for PROJ-014's prompt engineering focus and should be surfaced for the Phase 2 analyst. The warning-based technique is a prompt-only, practitioner-accessible improvement that requires no model access.
**Caveat (IN-002):** A-23 is a single study. Its 25.14% improvement has not been replicated across multiple model families or task types. Phase 2 should treat this as a promising technique requiring validation, not an established effect.

---

### GAP-3: DeCRIM Atomic Decomposition Improves Compliance 7.3-8.0% [Academic only]

**Source:** Academic survey, Source A-15 (Ferraz et al., EMNLP 2024, Tier 1).
**Claim:** Breaking compound negative constraints into atomic units improves instruction compliance by 7.3% (RealInstruct) and 8.0% (IFEval) for Mistral.
**Why no corroboration:** EMNLP 2024 academic paper; industry survey excluded academic papers. Context7 survey did not encounter DeCRIM in framework documentation.
**Assessment:** Scope limitation. The finding is Tier 1 (EMNLP peer-reviewed). The decomposition approach is practically relevant and should be presented to the Phase 2 analyst as a design pattern for PROJ-014 prompt construction.

---

### GAP-4: Refusal Mediated by One-Dimensional Subspace [Academic only]

**Source:** Academic survey, Source A-7 (Arditi et al., NeurIPS 2024).
**Claim:** LLM refusal behavior is mediated by a single one-dimensional subspace in the residual stream across 13 models up to 72B parameters.
**Why no corroboration:** Mechanistic interpretability research; industry and context7 surveys do not address internal model architecture.
**Assessment:** Scope limitation. Deeply relevant to explaining *why* negative constraints are brittle (they act through a single exploitable direction), but not directly actionable through prompt engineering.

---

### GAP-5: Instruction Compliance Rate Drops to 20-60% by Messages 6-10 [Industry only]

**Source:** Industry survey, Source I-17 (DEV Community / Siddhant K).

> **DO NOT CITE WITHOUT VERIFICATION (PM-003 fix; PM-001-R3 fix — relocated to precede claim):** The specific figures below (95% and 20-60%) come from a single practitioner blog post with no disclosed measurement methodology. These figures should not be cited in downstream deliverables as validated findings. They are directional indicators for research design only.

**Claim:** Instruction compliance starts at ~95% at messages 1-2 and drops to 20-60% by messages 6-10 over conversation length.
**Why no corroboration:** Practitioner observation with no disclosed methodology. Academic survey does not address conversational decay specifically. Context7 survey does not address this time dimension.
**Assessment:** Genuine knowledge gap (long-context negative instruction persistence is explicitly listed as under-researched by the academic survey). The specific decay rates (95%→20-60%) are practitioner estimates without experimental validation.

---

### GAP-6: DSPy Counter-Example Bootstrapping Achieves 164% More Constraint Compliance [Industry + Context7 — moderate]

**Source:** Industry survey I-21 / Context7 C-12/C-13. Not in academic survey.
**Claim:** DSPy Assertions enable 164% higher constraint compliance and 37% more high-quality responses compared to baseline.
**Why no corroboration in academic survey:** The academic survey did not include framework-level tooling in its search scope (it focused on academic papers, not practitioner documentation).
**Assessment:** Scope limitation. Both industry and context7 surveys cite this independently, elevating confidence. However, the academic paper (C-13, arXiv:2312.13382) is a **Tier 3 preprint with no confirmed peer-reviewed venue** (see C-13 catalog entry and CV-002 fix). The framework documentation (I-21) reports the same figures but is Tier 4. The 164% and 37% figures should be cited with Tier 3 qualification until a peer-reviewed venue is confirmed.

---

### GAP-7: Frontier LLMs Can Follow Approximately 150-200 Instructions [Industry only]

**Source:** Industry survey, Source I-16 (HumanLayer).
**Claim:** Frontier LLMs can follow approximately 150-200 instructions with reasonable consistency before quality degrades.
**Why no corroboration:** Practitioner estimate; methodology for determining this range is explicitly not disclosed by the source. Academic and context7 surveys do not address maximum instruction count.
**Assessment:** Genuine knowledge gap and low-confidence claim. The estimate is useful as a directional heuristic but should not be cited without the caveat that it is an unverified practitioner observation.

> **DO NOT CITE WITHOUT VERIFICATION:** This figure from I-16 (HumanLayer) is explicitly unverified. Phase 2 should not treat this as a validated boundary.

---

### GAP-8: Young et al. — 43.7% Overall Instruction-Following Pass Rate Across 256 LLMs [Context7 only]

**Source:** Context7 survey, C-19 (Young, Gillins, Matthews, arXiv:2510.18892).
**Claim:** 256 LLMs achieve an overall pass rate of 43.7% across 20 instruction-following tests; constraint compliance category achieves 66.9% (highest).
**Why no corroboration:** This preprint was not encountered by academic or industry surveys. The academic survey searched different databases (primarily peer-reviewed venues); the industry survey excluded academic papers.
**Assessment:** Genuine addition to the evidence base. The 256-model scale is methodologically significant and the 66.9% constraint compliance finding is relevant to PROJ-014 experimental design. However, this is an arXiv preprint (Tier 3/MEDIUM authority) without peer review.

---

### GAP-9: LlamaIndex Default Prompts Extensively Use Negative Framing [Context7 only]

**Source:** Context7 survey, C-11 (LlamaIndex default_prompts.py).
**Claim:** LlamaIndex's own default prompt templates contain 6 negative instructions ("Never query for all columns," "Do NOT fill in vector values directly," etc.) despite providing no guidance on positive vs. negative framing.
**Why no corroboration:** Framework source code analysis; not in scope for academic or industry surveys.
**Assessment:** Scope limitation. This finding demonstrates a vendor-practice tension (recommend positive, use negative) in a framework context, paralleling the same tension documented in Anthropic and OpenAI documentation (see CONFLICT-2 below).

---

### GAP-10: Emergent Misalignment from Narrow Fine-Tuning [Academic only]

**Source:** Academic survey, Source A-25 (Betley et al., Nature 2026, Tier 1).
**Claim:** Fine-tuning on narrow negative behaviors (insecure code generation) produces broad unexpected misalignment (~20% of unrelated outputs show misaligned behavior).
**Why no corroboration:** Research-specific finding from Nature publication. Industry and context7 surveys do not address training-time interventions.
**Assessment:** Scope limitation. Tier 1 finding (Nature journal) with significant implications for the distinction between training-time and inference-time negative constraints. Does not directly inform prompt engineering but is highly relevant to safety alignment design.

---

### GAP-11: VLMs Perform at Chance on Negation (NegBench, CVPR 2025) [Academic only]

**Source:** Academic survey, Source A-8.
**Claim:** VLMs perform at chance level on negation tasks across 79K examples.
**Why no corroboration:** Multimodal-specific research; industry and context7 surveys focus on text-only LLMs.
**Assessment:** Scope limitation. Extends negation failure to multimodal systems, suggesting fundamental architectural limitation in transformer-based systems regardless of modality.

---

### GAP-12: Model Size and Negation: r=0.867 Positive Correlation in Newer Models [Academic only]

**Source:** Academic survey, Source A-5 (Vrabcova et al., arXiv, Tier 3).
**Claim:** Strong positive correlation (Spearman r=0.867) between model size and negation handling ability in newer architectures (Llama 3, Qwen 2.5, Mistral).
**Why no corroboration:** arXiv preprint from Masaryk University; industry and context7 surveys did not encounter this paper.
**Assessment:** Important qualification to the inverse scaling finding. The industrial inverse scaling prize data (A-9) was collected on 2022-2023-era models; this newer data suggests architectural improvements may be reversing the trend. Neither finding can be fully trusted for current frontier models without direct measurement.

---

### GAP-13: Context Compaction Causes NEVER Rules to Lose Imperative Force [Industry only]

**Source:** Industry survey, Sources I-28, I-32.
**Claim:** During context compaction, NEVER/DO NOT rules are compressed from explicit instructions into implicit descriptions and lose their imperative force.
**Why no corroboration:** Practitioner observation from Claude Code users and developer analysis. Academic and context7 surveys do not address context compaction dynamics.
**Assessment:** Genuine knowledge gap. The mechanism — rules losing imperative status during summarization — is a practically important production concern. The academic survey notes "long-context negative instruction persistence" as an under-researched area. Evidence is anecdotal (GitHub bug reports, blog post) but corroborated across multiple independent users.

---

### GAP-14: OpenAI Evolution — GPT-5.1 and GPT-5.2 Guidance [Context7 only]

**Source:** Context7 survey, C-6 and C-7 (GPT-5.1 and GPT-5.2 Prompting Guides).
**Claim:** GPT-5.2 explicitly requires "explicit instructions" and "poorly-constructed prompts containing contradictory or vague instructions can be more damaging to GPT-5.2 than to other models."
**Why no corroboration:** GPT-5.1 and GPT-5.2 cookbook guides were not encountered by the industry survey. These are the most recent model-specific guidance documents in any survey.
**Assessment:** Scope limitation. This finding amplifies the model-generation evolution pattern (AGREE-3 caveat): as models improve at following instructions literally, both the benefits and the risks of negative instructions become more pronounced.

---

## L1: Conflicts — Contradictory Findings

### CONFLICT-1: Does Larger Model Size Improve or Worsen Negation Handling? [RESOLVED]

**Position A (Inverse scaling):** Larger models perform *worse* on negated instructions. McKenzie et al. (A-9, TMLR, Tier 2): performance degrades beyond ~10^22 FLOPs on specific negation tasks (2022-2023-era models). Truong et al. (A-4, *SEM 2023, Tier 2): larger LMs more insensitive to negation; InstructGPT outperforms via instruction-tuning, not scaling.

**Position B (Positive scaling):** Larger, newer models perform *better* on negation. Vrabcova et al. (A-5, arXiv 2025, Tier 3): Spearman r=0.867 between model size and negation handling in Llama 3, Qwen 2.5, Mistral architectures.

**Evidence assessment:**
- Position A sources: Tier 2 (TMLR, *SEM 2023). Data from 2022-2023-era models.
- Position B source: Tier 3 (arXiv preprint, Masaryk University). Data from 2024-2025-era models.

**Resolution:** The conflict is temporal, not logical. Both positions can be simultaneously true if architectural improvements in 2024-2025 model families reversed a trend that was genuine in 2022-2023 models. The academic survey explicitly identifies this resolution. The U-shaped recovery speculation from McKenzie et al. supports this interpretation.

**Confidence:** MEDIUM. Position B is from an unreviewed preprint; independent replication on current-generation frontier models is needed.

**Implication for PROJ-014:** Phase 2 experiments should be conducted on current-generation frontier models, not older architectures. Results from models predating 2024 may not generalize.

---

### CONFLICT-2: Vendor Recommendation vs. Vendor Practice — Do Vendors Follow Their Own Advice? [RESOLVED, with documented uncertainty]

**Position A (Follow recommendations):** Vendors recommend positive framing; Anthropic, OpenAI, Google all explicitly recommend "tell the model what to do, not what to avoid."

**Position B (Contradict recommendations in practice):** Both Anthropic and OpenAI use extensive negative constraints in their own example prompts and documentation. Anthropic uses `<do_not_act_before_instructions>`, `NEVER output a series of overly short bullet points`. OpenAI's GPT-5.2 cookbook uses "Do NOT invent colors" and "Never fabricate exact figures." LlamaIndex default prompts use "Never query for all columns."

**Evidence assessment:** Both positions are documented with high-authority sources (vendor documentation = HIGH authority). The tension is internal to vendor guidance, not between independent surveys.

**Resolution:** The context7 survey documents four non-exclusive explanations: (1) intentional context dependency — positive framing for general use, negative for safety-critical constraints; (2) temporal lag — examples written before the positive-framing recommendation was codified; (3) pedagogical vs. production distinction; (4) pragmatic recognition that some constraints are most clearly expressed as prohibitions.

**Testability ranking (SM-006 fix):** Explanation (1) is most testable — compare vendor system prompt examples for negative constraint usage patterns against content category (safety-critical vs. general). Explanation (2) is moderately testable — compare publication dates of negative-containing examples against recommendation codification dates. Explanation (3) is testable by categorizing examples as pedagogical vs. production. Explanation (4) is least testable — requires internal vendor access to confirm pragmatic reasoning.

**Synthesizer assessment:** The most parsimonious resolution is explanation (1): vendors apply *situation-dependent* guidance. Positive framing is the default for general behavioral direction; negative framing is retained for hard safety boundaries, scope control, and precision-critical constraints. This interpretation is consistent with OpenAI's explicit guidance in the GPT-5 cookbook (I-5/C-5): unambiguous negatives like "NEVER add copyright headers" work "because they prevent concrete harms rather than attempting to control reasoning depth."

**Confidence:** HIGH for the resolution pattern; LOW for determining which of the four sub-explanations is correct without vendor internal access.

---

### CONFLICT-3: Is the 8.4% Factual Accuracy Reduction from Negative Prompts Reliable? [RESOLVED — LOW CONFIDENCE]

**Position A (8.4% reduction is real):** Gandhi & Gandhi (A-14, Joyspace AI, arXiv, Tier 3): negative prompts reduce factual accuracy from 92.3% to 84.5% (-8.4%). Source I-30 (The Big Data Guy) independently reports the same 8.4% figure for negative sentiment in prompts.

**Position B (Finding requires replication):** Academic survey explicitly flags A-14 as "the only study directly comparing positive/neutral/negative framing on factual accuracy" and notes it is "commercially affiliated" with a modest sample size (N=500).

**Assessment:**
- Source A-14 is Tier 3 (arXiv, commercially affiliated, not peer-reviewed).
- Source I-30 measures emotional *sentiment*, not instructional *negation* (syntactic prohibitions). The two 8.4% figures measure different phenomena.

**Resolution:** The 8.4% figure appears in two independent sources but with fundamental measurement differences. Both sources agree on direction (negative framing reduces accuracy relative to neutral), but magnitude is unreliable from current evidence.

**Status:** Resolved as "directionally plausible, magnitude unreliable." Phase 2 should directly measure factual accuracy under matched positive/negative/neutral instruction conditions.

---

### CONFLICT-4: Does Self-Refinement Improve Negative Instruction Compliance Meaningfully? [UNRESOLVED — natural-language self-refinement question only; see note]

**Position A (Self-refinement helps):** Academic survey, Source A-16 (Harada et al., **rejected ICLR 2025** — use with significant caution): self-refinement improves GPT-4o from 15% to 31% on 10 simultaneous instructions. That is a 2x improvement, though from a very low baseline.

**Position B (Self-refinement limited):** Academic survey, Source A-21 (Barkley & van der Merwe): external tools deteriorate smaller model performance. Industry survey does not address self-refinement directly.

**Assessment:**
- Position A is from a rejected paper (Harada et al.) — peer review identified concerns. The 15%→31% improvement still means GPT-4o fails on 69% of 10-instruction prompts even after self-refinement.
- Position B is from a single 8B model with 3 runs (A-21) — low statistical confidence (acknowledged in catalog note).
- The DSPy Assertions programmatic self-refinement (I-21/C-13) achieves 164% improvement — far exceeding natural language self-refinement. But DSPy operates at a different abstraction level.

**Status:** UNRESOLVED. Both relevant sources have significant quality limitations (rejected paper; insufficient runs). The evidence is insufficient to determine whether natural-language self-refinement offers meaningful improvement for negative instruction compliance. Phase 2 should include a self-refinement condition if sample size permits.

> **Note on CONFLICT-4 label vs. practical resolution:** The DSPy programmatic comparison effectively answers the practical question "what should I use instead of manual self-refinement?" without resolving the narrow research question of whether natural-language self-refinement improves NL negative instruction compliance. The UNRESOLVED label applies specifically to the natural-language self-refinement question.

---

## L1: Evidence Tier Analysis

### Source Counts by Tier

| Tier | Definition | Count | Notes |
|------|-----------|-------|-------|
| **Tier 1** | Top peer-reviewed venues (main conference tracks, top journals: NeurIPS, ICLR, ACL, EMNLP, CVPR, AAAI, Nature, Computational Linguistics, IJCAI main) | 13 | Sources A-1, A-3, A-7, A-8, A-13, A-15, A-20, A-22, A-23, A-24, A-25, A-27, A-28 |
| **Tier 2** | Established venues, workshops with peer review (TMLR, *SEM, EACL, MIT Press CL, non-archival IJCAI symposium) | 5 | Sources A-4, A-9, A-12, A-26, A-30 |
| **Tier 3** | arXiv preprints, unreviewed (including rejected submissions) | 15 | Sources A-2, A-5, A-6, A-10, A-11, A-14, A-16, A-17, A-18, A-19, A-21, A-29, A-31, C-13, C-19 (note: A-31 added as new Tier 3 source in R2; it is a distinct document from I-13 which remains in Group I as a separate industry secondary-citation entry; C-19 = Young et al. arXiv:2510.18892, also Tier 3) |
| **Tier 4** | Vendor documentation, practitioner blogs, framework docs, community guides | 42 | All I-series and C-series sources except C-13, C-19 (those two are Tier 3, counted above) |
| **Rejected submission** | Failed peer review | 1 | A-16 (Harada et al., rejected ICLR 2025) — within Tier 3 count above |
| **Commercially affiliated, not peer-reviewed** | Commercial entity, unreviewed | 1 | A-14 (Joyspace AI) — within Tier 3 count above |

> **Tier 3 count note (SR-005/R3 fix; CV-001-R3/FM-015 fix):** The Tier 3 category counts 15 sources: A-2, A-5, A-6, A-10, A-11, A-14, A-16, A-17, A-18, A-19, A-21, A-29, A-31, C-13, C-19. A-31 (Bsharat et al., arXiv:2312.16171) was added as a new source in R2 — it is a distinct document from I-13 (PromptHub, a secondary-citation industry blog). Both A-31 and I-13 are present in the catalog as separate entries. C-19 = Young et al. (arXiv:2510.18892), Tier 3 (new context7-unique source). C-13 = DSPy preprint (arXiv:2312.13382), Tier 3. All 15 sources in this list are arXiv preprints, unreviewed/rejected submissions, or commercially affiliated unreviewed papers. Tier 4 correspondingly counts 42 (all I-series and C-series sources except C-13 and C-19). **R4 correction (CV-001-R3 fix):** The R3 note incorrectly stated "14 sources" while enumerating 15 — the discrepancy arose because C-19 was already present in the enumerated list when A-31 was designated as the net-new addition, but C-19 was miscounted in Tier 4. The correct Tier 3 count is 15 and Tier 4 is 42; the total remains 75.

**Total: 75 sources** (13 Tier 1 + 5 Tier 2 + 15 Tier 3 + 42 Tier 4 = 75). Tier 1 constitutes 17.3% of all sources. Tier 4 constitutes 56.0%.

### Key Findings by Evidence Tier Strength

**Tier 1 findings (highest confidence):**
- Blunt prohibition instruction-following unreliable (A-15 DeCRIM, EMNLP 2024; A-20 Geng et al., AAAI 2026)
- Warning-based meta-prompts improve negation accuracy by up to 25.14% (A-23, EMNLP 2025) — single study, replication needed
- Refusal is mediated by a one-dimensional subspace — explains brittleness (A-7, NeurIPS 2024)
- LLMs fail on inference rules with negated premises (A-27, ACL 2024)
- CAST model-internal steering achieves 90.67% harmful refusal (A-28, ICLR 2025 Spotlight)
- Training on narrow negative behaviors produces broad misalignment (A-25, Nature 2026)
- CoVe verification pipeline more than doubles precision on Wikidata tasks (A-22, ACL 2024)
- System/user prompt instruction hierarchy is unreliable (A-20, AAAI 2026)
- Prompt formatting causes up to 76 accuracy-point swings (A-13, ICLR 2024)
- Large negation benchmark: LLMs rely on superficial cues for negation (A-3, EMNLP 2023)

**Key conclusions resting primarily on Tier 3 or lower evidence (require independent replication):**
- Hallucination rate *may* increase with negation in MCQA contexts: LLaMA-2 ~26%→~59% (A-6, arXiv, Tier 3, one model family, not replicated) — directional signal only
- Negative sentiment reduces factual accuracy by 8.4% (A-14, commercially affiliated; Tier 3)
- Exponential decay model for multiple instructions (A-16, rejected paper; below Tier 3 — do not cite without peer-reviewed replication)
- Model size r=0.867 correlation with negation in newer architectures (A-5, arXiv; Tier 3)
- Affirmative directives 55% improvement over prohibitions (A-31, Bsharat et al., arXiv 2023; Tier 3) — cited as primary source for this figure
- DSPy Assertions: 164% compliance improvement (C-13 arXiv preprint, Tier 3; no confirmed peer-reviewed venue; I-21 framework docs, Tier 4)
- Instruction compliance drops 95%→20-60% over conversation length (I-17, practitioner anecdote; Tier 4 — DO NOT CITE as validated)

**Vendor recommendation strength (Tier 4, HIGH source authority):**

The vendor consensus (Anthropic, OpenAI across 3 major model generations, Google: all recommend positive framing as default) constitutes the **broadest operational consensus** for the practical recommendation. It should not be characterized as "the strongest evidence" (DA-005 fix — Tier 4 evidence is not epistemically superior to Tier 1 experimental data). However, this consensus is notable for its breadth (3 major vendors, independently), internal consistency, and practitioner testing validation (I-12 DreamHost systematic testing). The Tier 1 academic evidence (A-15, A-20, A-23) provides stronger experimental grounds for specific structural techniques; vendor consensus provides broader operational guidance for the practical recommendation that structural enforcement is preferred.

---

## L1: Unsourced Claim Audit

This section identifies assertions in source surveys that lack citations. All claims in this synthesis have citations referencing source surveys and source IDs.

**Academic survey unsourced claims found:**
- The "60% hallucination reduction" figure is described as "common in prompt engineering guidance and vendor documentation" but the academic survey itself acknowledges it "appears to be an informal 'rule of thumb' circulating in practitioner communities without a single traceable published source." This is appropriately flagged as an unverified working hypothesis. No unsourced factual assertion detected.
- The exponential decay model from A-16 (Harada et al.) is described as "independently plausible given DeCRIM's findings" — flagged with source caveats. Acceptable.

**Industry survey unsourced claims found:**

- Source I-16 (HumanLayer): "Frontier LLMs follow approximately 150-200 instructions with reasonable consistency." The industry survey itself notes: "methodology for determining this range not disclosed; treat as an unverified practitioner estimate." Appropriately flagged.
- Source I-17 (DEV Community): "~95% compliance at messages 1-2, dropping to 20-60% by messages 6-10." Industry survey notes: "practitioner observation; specific decay rates not independently verified and measurement methodology not disclosed." Appropriately flagged.
- Source I-22 (Latitude): "Tools cut iteration time by 30% and improve output consistency by 25%." These quantitative claims are presented without disclosed methodology. **Flagged here for Phase 2 analyst attention.** This specific claim from Latitude should not be cited in downstream deliverables without independent verification. Cross-reference: I-22 (Latitude) figures (30%/25%) are flagged in this audit and should be treated as unverified. (SR-002 fix: explicit cross-reference note added)
- Source I-14 (MLOps Community): "Reasoning performance degrades around 3,000 tokens." The industry survey presents this as an empirical finding, but the source is a blog post. The specific 3,000-token threshold should be treated as a practitioner benchmark estimate, not a validated threshold.

**Context7 survey unsourced claims found:**
- No unsourced factual assertions detected. The context7 survey appropriately distinguishes authority tiers (HIGH/MEDIUM/LOW) and preprint status per-finding.

**Unsourced claims in THIS synthesis:**
- All claims in this synthesis are attributed to specific sources using the (Survey, Source ID) notation. No unsourced assertions introduced.

---

## L2: Cross-Survey Themes

The following themes emerge from the intersection of all three surveys. These are patterns that no single survey captures alone — they require comparing across the three evidence bases to become visible.

---

### THEME-1: The "Prohibition Paradox" — Why Vendors Recommend Against What They Practice

No single survey fully resolves the tension between vendor recommendation (positive framing preferred) and vendor practice (extensive use of negative framing in actual documentation and system prompts). Viewing all three surveys together reveals a structural pattern:

The context7 survey provides code-level evidence from LlamaIndex default prompts (C-11): "Never query for all columns," "Do NOT fill in vector values directly." The industry survey documents the same pattern in Anthropic's system prompts: "Claude does not claim to be human" (declarative negative) vs. "NEVER claim to be human" (imperative prohibition). The academic survey provides a plausible mechanistic explanation through Source A-20 (Geng et al., AAAI 2026, Tier 1): instruction hierarchy failures occur because pre-training encodes behavioral priors that override post-training prompt instructions — meaning that the *declarative* negative framing ("Claude does not X") may work better than the *imperative* negative framing ("NEVER X") because declarative framing aligns with the model's behavioral self-model rather than fighting it.

**Important caveat (RT-006/CC-004 fix):** The claim that declarative behavioral negation "works through the model's self-model" is a synthesis-generated mechanistic hypothesis. No source provides direct interpretability evidence for this mechanism. This is a testable hypothesis, not a confirmed finding. The synthesis-generated hypothesis does not imply its mechanism has been verified.

**Synthesis:** Vendors appear to have empirically discovered a framing distinction that their published guidance does not fully articulate: declarative-behavioral negation ("X does not Y") may work better than imperative-prohibition negation ("NEVER do Y") because it better aligns with model behavior patterns from pre-training. This distinction is never explicitly stated by any source but is consistently implied by the gap between vendor recommendations and vendor practice.

**Testable prediction (SM-004 fix):** This hypothesis is testable in Phase 2. Experimental condition: declarative behavioral negation ("Claude does not X") vs. imperative prohibition ("NEVER X") vs. positive instruction ("Claude does Y") on identical task types. If declarative negation performs significantly better than imperative prohibition but similarly to positive instruction, this would support the synthesis-generated hypothesis.

---

### THEME-2: The Effectiveness Hierarchy Is a Spectrum, Not a Binary

All three surveys independently treat "negative prompting" as if it were a single phenomenon. The academic survey distinguishes four phenomena (negation comprehension, prohibition instruction-following, training/alignment constraints, negative framing effects). The industry survey distinguishes hard vs. soft negatives and five failure mechanisms. The context7 survey creates a preliminary taxonomy of five negative instruction types (prohibition, exclusion, conditional negation, scope limitation, safety boundary).

Viewed together, these partial taxonomies reveal an effectiveness spectrum. See AGREE-5 for the full hierarchy with access-level annotations, evidence tiers, and actionability notes.

The PROJ-014 hypothesis asks about levels 9-12 of the hierarchy (the prompt-accessible range). The literature has not compared these levels against each other in controlled conditions. Phase 2 should position itself at levels 5-9 (accessible prompt-only techniques) and test whether they differ significantly from each other and from the blunt prohibition baseline.

**Note on "negative prompting" scope (RT-005):** The effectiveness spectrum spans at least four distinct phenomena (negation comprehension, prohibition instruction-following, training/alignment constraints, negative framing effects). Findings from one phenomenon do not automatically generalize to others. Phase 2 experimental scope should explicitly bound which phenomena are under test.

---

### THEME-3: The Model-Generation Confound Is Underappreciated Across All Surveys

Each survey acknowledges model-generation effects separately but does not integrate them into a unified picture. The academic survey flags that the A-9 inverse scaling finding may be "a historical artifact of 2022-2023-era architectures." The industry survey notes a "Model-Generation Confound" cross-reference noting that findings from earlier model generations may not apply to frontier models. The context7 survey documents OpenAI's GPT-5.2 guidance that "poorly-constructed prompts containing contradictory or vague instructions can be more damaging to GPT-5.2 than to other models."

Viewing these separately implies model evolution is a background factor. Viewing them together reveals a potentially important trend: as models improve at instruction-following, the consequences of negative instruction design errors may be *increasing*, not decreasing. A GPT-3.5 era model that partially ignored a flawed negative instruction would produce mediocre output. A GPT-5.2 model that follows the flawed negative instruction literally may produce a more confidently wrong output.

**Caveat (DA-006 fix):** The above trend description is a synthesis-generated inference. No source provides direct evidence that GPT-5.2 or equivalent frontier models follow flawed negative instructions "too literally" in a way that produces confidently wrong outputs. This is a directional hypothesis based on pattern extrapolation, not a confirmed finding.

**Synthesis:** The prompt engineering community's current positive-framing recommendation may be derived from evidence that is simultaneously becoming more and less relevant. Phase 2 must be designed explicitly for current-generation frontier models (post-2024 architecture) and should not assume that findings from earlier model generations generalize.

---

### THEME-4: The Empirical-Prescriptive Gap Is Consistent and Concerning

All three surveys independently identify a gap between the strength of prescriptive recommendations and the weakness of supporting empirical evidence. The academic survey has the strongest empirical evidence base but finds no direct A/B comparison of "don't X" versus "always Y" instructions. The industry survey notes that 77% of its sources are practitioner anecdotes or vendor recommendations with no controlled experimental data. The context7 survey finds zero quantitative evidence in any vendor or framework documentation.

The consistency of this gap across three independent surveys using different search strategies suggests it is not a search failure — it is a genuine state of the field. Practitioners have strong consensus on what works (positive framing) but no experimental validation.

**Synthesis:** The "positive over negative" recommendation may be correct, but it rests on a foundation of vendor experience, practitioner anecdotes, and theoretical reasoning (Ironic Process Theory analogy), not controlled experiments. See Known Scope Exclusions (SE-1 through SE-4): it is possible this experimentation exists in proprietary contexts not captured by these surveys. PROJ-014's Phase 2 experimental work has the opportunity to provide the first publicly documented controlled, multi-model, multi-task A/B comparison of matched positive versus negative instruction variants.

---

### THEME-5: Structural Enforcement Converges as the Superior Alternative — But Operates at a Different Level

All three surveys independently identify structural/programmatic constraint enforcement as superior to linguistic instruction (whether positive or negative). The academic survey documents CoVe (A-22), DeCRIM (A-15), and CAST (A-28). The industry survey documents DSPy Assertions (I-21), NeMo Guardrails (I-27), and QED42's example-based approach (I-20). The context7 survey identifies NP-004 as a convergent pattern across frameworks.

Despite convergent evidence of superiority, structural enforcement is absent from most practitioner prompting advice and is not implemented in the most widely used LLM frameworks (LangChain and LlamaIndex both lack native guidance on this distinction).

**Important caveat (IN-005 fix):** Structural enforcement (DSPy Assertions, NeMo Guardrails, LangChain OutputFixingParser) may outperform linguistic framing for mechanistic reasons orthogonal to the negative-vs-positive framing question. Programmatic enforcement works by catching failures and triggering retry loops — it operates at a different abstraction level than instruction framing. Evidence that programmatic enforcement outperforms linguistic framing does not directly prove that positive linguistic framing outperforms negative linguistic framing. These are separate claims. Phase 2 should keep the structural enforcement question and the linguistic framing question as distinct experimental dimensions.

**Synthesis:** PROJ-014's Phase 2 scope decision should explicitly address whether to limit testing to linguistic framing or to include structural enforcement mechanisms as a comparison condition. If structural enforcement consistently outperforms linguistic framing (positive or negative), the practical recommendation may be "don't use linguistic instruction for critical constraints at all — use programmatic enforcement" regardless of positive vs. negative framing.

---

## Phase 2 Experimental Design Requirements

> **Added in Revision 2 (SM-003/PM-001/CV-003 fix).** This section consolidates all Phase 2 design implications scattered across individual AGREE, GAP, THEME, and CONFLICT sections into a single actionable reference. Each experimental condition is explicitly traced to the synthesized finding that motivates it.

### Consolidated Experimental Conditions (Derived from Synthesis)

| Condition | Label | Derivation | Evidence Tier | Priority |
|-----------|-------|------------|---------------|----------|
| Standalone negative prohibition | Cond-1 | Tests the working hypothesis directly (AGREE-1: no evidence for 60% claim) | N/A (baseline) | Required |
| Standalone positive instruction | Cond-2 | AGREE-3 vendor consensus baseline; AGREE-4 primary comparison | Tier 1 (A-20), Tier 3 (A-31) | Required |
| Paired negative + positive alternative | Cond-3 | AGREE-8: NP-002 pattern; contrastive CoT evidence (A-11) | Tier 3 (A-11), Tier 4 (vendor docs) | Required |
| Justified negative + contextual reason | Cond-4 | AGREE-9: NP-003 pattern; A-23 warning mechanism analogy | Tier 1 (A-23, indirectly), Tier 4 (vendor docs) | Required |
| Warning-based meta-prompt | Cond-5 | GAP-2: A-23 most actionable Tier 1 academic finding (+25.14% distractor negation) | Tier 1 (A-23) — single study, needs replication | Required |
| Declarative behavioral negation | Cond-6 | THEME-1: synthesis-generated hypothesis (vendor practice pattern; testability noted). **[Synthesis-generated hypothesis — not directly sourced from primary evidence. This condition tests a synthesizer-observed pattern, not a source-supported finding. Phase 2 testing of Cond-6 is exploratory. Negative results should not be interpreted as invalidating the synthesis. Derivation chain from source to finding is incomplete for this condition.]** | Tier 4 (vendor practice) — synthesis hypothesis | Recommended-B (lower priority within Recommended tier; if only one Recommended condition can be implemented, prioritize Cond-7) |
| Atomic decomposition | Cond-7 | GAP-3: DeCRIM +7-8% compliance (A-15, EMNLP 2024). Note: DeCRIM evidence is more robustly replicated (Tier 1, two benchmarks) than Cond-5 (A-23, single study). Cond-7 is "Recommended" rather than "Required" because it addresses a secondary research question (decomposition strategy) vs. the primary framing question tested by Cond-1 through Cond-5. | Tier 1 (A-15) | Recommended-A (higher priority within Recommended tier; implement before Cond-6 if resource-constrained) |

### Mandatory Measurement Dimensions (Derived from Synthesis)

| Measurement | Derivation | Evidence Basis |
|-------------|------------|---------------|
| Compliance rate (constraint adherence) | AGREE-7: compliance and accuracy are independent capabilities | A-19 (Tier 3), C-19 (Tier 3) |
| Output quality / accuracy | AGREE-7: must be measured independently from compliance | A-19 (Tier 3) |
| Hallucination rate | AGREE-1: the working hypothesis directly concerns hallucination | Working hypothesis |
| Per-model results (minimum 3 frontier models) | CONFLICT-1 / THEME-3: model-generation confound is critical | A-5, A-9, AGREE-3 caveat |
| Task type stratification | AGREE-6: negation effects are task-specific (MCQA vs. general) | A-6 (Tier 3) |
| Temporal decay (multi-turn) | GAP-5: compliance reported to drop over conversation length | I-17 (Tier 4, unverified — use for exploratory only) |

### Design Constraints Derived from Known Scope Exclusions

| Constraint | Source | Rationale |
|------------|--------|-----------|
| Use post-2024 frontier models only | CONFLICT-1, THEME-3 | Pre-2024 inverse scaling findings may not generalize |
| Document model version explicitly | THEME-3, GAP-14 | GPT-5.2 guidance differs from GPT-4-era guidance |
| Define "negative prompting" operationally before testing | THEME-2, RT-005 | At least 4 distinct phenomena share the label |
| Report results by task type, not pooled | AGREE-6, GAP-2 | Task-specificity is a documented confound |
| Do NOT assume 60% claim is refuted | DA-001, DA-003 | Null finding from Phase 1; Phase 2 generates the first evidence |

---

## Source Count Verification

**Counting methodology:** Each unique source document receives exactly one entry regardless of the number of surveys citing it. Where multiple references in one survey point to the same document, they are consolidated. Identity criteria: same DOI, same arXiv ID, or same primary URL canonicalized to remove redirect artifacts.

### Explicit Arithmetic Trace (SR-001 fix)

**Step 1: Group A (Academic sources)**

Group A contains all 30 sources from academic-survey.md: A-1 through A-30, each distinct. Plus A-31 (Bsharat et al., added R2 as primary source for the 55% figure previously cited via I-13 secondary) = 30 + 1 new entry = **31 total Group A sources**.

> **R3 clarification (SR-002-R2/FM-010 fix):** A-31 (Bsharat et al., arXiv:2312.16171) is a genuinely new source added in Revision 2. It was not previously cataloged. This increases Group A from 30 to 31 unique sources. A-31 and I-13 (PromptHub) are DISTINCT documents — A-31 is the primary academic paper (arXiv preprint); I-13 is the PromptHub industry blog that cited A-31 as a secondary reference. Both remain in the catalog. There is no replacement. The total source count increased from 74 (R1) to 75 (R2+) because A-31 is a net-new entry.

**Step 2: Group I (Industry-unique sources not in Group A)**

Starting from Group I in the original catalog (31 sources: I-1 through I-32, excluding I-26 which was excluded by design).

Cross-survey deduplication check: I-18 (LessWrong Inverse Scaling announcement) and A-9 (academic paper) are TWO distinct documents — counted separately. I-1/C-1/C-2 counted as one entry in Group I (I-1). Net Group I after deduplication: 31 sources.

**Step 3: Group C (Context7-unique sources not in Group A or Group I)**

Partial overlaps resolved (same document identity, counted ONCE):
- C-15/I-13: same PromptHub/DAIR-AI pages — consolidated under I-13 and I-2
- C-16/I-8: same source (Pink Elephant, 16x.engineer) — consolidated under I-8
- C-17/I-23: same source (Lakera) — consolidated under I-23
- C-18/A-19: same paper (Tripathi et al., arXiv:2601.03269) — consolidated under A-19
- C-4/I-4: same source (GPT-4.1 cookbook) — consolidated under I-4
- C-5/I-5: same source (GPT-5 cookbook) — consolidated under I-5
- C-1/I-1: same source family (Anthropic platform docs) — consolidated under I-1

After these deduplication decisions, the 13 context7-unique sources not already counted in Groups A or I are:

| Group C ID | Source | context7 Ref | Notes |
|------------|--------|--------------|-------|
| C-2 | Anthropic Prompt Engineering Blog (claude.com/blog/best-practices-for-prompt-engineering) | Ref #2 | Distinct URL and publication from C-1/I-1 (platform.claude.com). Same vendor family, different document. |
| C-3 | OpenAI Prompt Engineering Guide (platform.openai.com/docs/guides/prompt-engineering) | Ref #3 | Primary platform doc (inaccessible at 403 during context7 survey fetch). **CV-002-R3 caveat (R4 fix):** The key finding attributed to C-3 ("Primary OpenAI platform docs; 'say what to do instead of what not to do'") is inferred from the URL structure, source title, and context7 survey description — not from direct content retrieval. The source is counted as it was referenced and described in the context7 survey, but downstream agents should note that its content was not independently verified. The finding attributed to C-3 is consistent with the same vendor's separately verified guidance in I-3, I-4, and I-5. Distinct from I-3 (community guide) and I-4/I-5 (cookbook guides). |
| C-6 | OpenAI GPT-5.1 Prompting Guide | Ref #6 | NEW — not in Group A or Group I |
| C-7 | OpenAI GPT-5.2 Prompting Guide | Ref #7 | NEW — not in Group A or Group I |
| C-8 | LangChain Prompt Templates Reference | Ref #8 | NEW (framework docs) |
| C-9 | LangChain Guardrails Documentation | Ref #9 | NEW (framework docs) |
| C-10 | LlamaIndex Prompts Documentation | Ref #10 | NEW (framework docs) |
| C-11 | LlamaIndex Default Prompts Source Code | Ref #11 | NEW (source code) |
| C-12 | DSPy Assertions Documentation (dspy.ai/learn/programming/7-assertions/) | Ref #12 | Distinct from I-21 (framework tutorial/community docs) and C-13 (academic preprint). Official framework docs. |
| C-13 | DSPy Assertions Paper (arXiv:2312.13382) | Ref #13 | Tier 3 arXiv preprint. Distinct from C-12 (documentation) and I-21 (community tutorial). |
| C-14 | DSPy Official Site (dspy.ai/) | Ref #14 | DSPy philosophy/overview page. Distinct from C-12 (assertions docs) and C-13 (paper). |
| C-19 | When Models Can't Follow (Young, Gillins, Matthews; arXiv:2510.18892) | Ref #19 | NEW — not in academic or industry surveys |
| C-20 | Prompt Builder OpenAI Guide (promptbuilder.cc) | Ref #20 | NEW |

**Total Group C: 13 unique sources (SR-001-R2/CV-001-R2/FM-011 fix — all 13 sources now explicitly named with IDs)**

**Step 4: Total**

| Group | Count | Sources | Description |
|-------|-------|---------|-------------|
| Group A | 31 | A-1 through A-30, plus A-31 | Academic sources (30 original + A-31 added R2 as distinct new source) |
| Group I | 31 | I-1 through I-32 (excluding I-26) | Industry-unique (after cross-survey deduplication) |
| Group C | 13 | C-2, C-3, C-6, C-7, C-8, C-9, C-10, C-11, C-12, C-13, C-14, C-19, C-20 | Context7-unique (after cross-survey deduplication; all 13 now explicitly identified) |
| **Total** | **75** | | **R2/R3 total (R1 was 74; A-31 added as new source in R2; Group C sources fully enumerated in R3)** |

**Total unique sources: 75. Requirement of >= 50 unique sources: SATISFIED.**

### Deduplication Decisions Applied

| Deduplication Decision | Sources Merged | Action |
|----------------------|----------------|--------|
| A-9 academic paper vs. I-18 LessWrong announcement | Same *research* but two *distinct source documents* | Counted as 2 entries |
| I-1 / C-1 (Anthropic platform docs, platform.claude.com) | Identical source document | Counted as 1 entry (I-1) |
| C-2 (Anthropic Prompt Engineering Blog, claude.com/blog/best-practices-for-prompt-engineering) | Distinct URL and distinct document from I-1/C-1; same vendor family but different publication | Counted separately — C-2 is an independent entry in Group C |
| I-4 / C-4 (GPT-4.1 guide) | Identical source | Counted as 1 entry |
| I-5 / C-5 (GPT-5 guide) | Identical source | Counted as 1 entry |
| I-8 / C-16 (Pink Elephant) | Identical source | Counted as 1 entry (I-8) |
| I-13 / C-15 (PromptHub/DAIR-AI) | Partially overlapping but different documents | Counted as 2 entries; A-31 added as primary source for the academic paper cited via I-13 |
| I-21 / C-12 / C-13 (DSPy) | I-21 + C-12 = framework docs (one entry); C-13 = academic preprint (separate entry) | Counted as 2 entries |
| I-23 / C-17 (Lakera) | Identical source | Counted as 1 entry (I-23) |
| A-19 / C-18 (Tripathi et al.) | Identical source, two surveys citing | Counted as 1 entry (A-19) |

---

## PS Integration

- **PS ID:** PROJ-014
- **Entry ID:** Barrier-1-Synthesis-R4
- **Artifact:** `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/barrier-1/synthesis.md`
- **Source documents:**
  - `research/academic-survey.md` (30 sources, Revision 5 Final)
  - `research/industry-survey.md` (31 core sources, Revision 4 Final)
  - `research/context7-survey.md` (20 references, Iteration 5)
- **Confidence:** 0.85 (high corroboration on primary findings; evidence gaps documented throughout)
- **Key findings for downstream agents:**
  1. Zero evidence for 60% hallucination reduction claim — this is a **null finding (untested), not a refutation**; hypothesis requires Phase 2 experimental validation
  2. Structural enforcement (DSPy, NeMo, CoVe) consistently outperforms linguistic instruction; this operates at a different abstraction level than the positive-vs-negative framing question
  3. The most actionable prompt-level technique identified is warning-based meta-prompting (+25.14% distractor negation accuracy, A-23, EMNLP 2025, Tier 1, single study pending replication)
  4. Phase 2 should test 7 conditions: 5 Required — Cond-1 (standalone negative), Cond-2 (standalone positive), Cond-3 (paired negative+positive), Cond-4 (justified negative+reason), Cond-5 (warning-based meta-prompt); plus 2 Recommended — Cond-7 (atomic decomposition, Recommended-A, Tier 1 evidence), Cond-6 (declarative behavioral negation, Recommended-B, synthesis hypothesis); see [Phase 2 Experimental Design Requirements](#phase-2-experimental-design-requirements) for full condition derivations and priority labels
  5. Model-generation confound is critical: run experiments on post-2024 frontier models only; pre-2024 findings may not generalize
  6. Evidence domains excluded from all three surveys (production deployments, domain-specific expert applications, internal vendor benchmarks) may contain relevant evidence not captured here — see [Known Scope Exclusions](#known-scope-exclusions)
- **From agent:** ps-synthesizer
- **To agent:** ps-analyst (Phase 2 experimental design)
- **Handoff artifacts:** This document; academic-survey.md; industry-survey.md; context7-survey.md
- **Blockers:** None
- **Next agent hint:** ps-analyst for Phase 2 experimental design — use Section [Phase 2 Experimental Design Requirements](#phase-2-experimental-design-requirements) as the primary design constraint reference; use AGREE-8/AGREE-9 paired/justified patterns and the THEME-2 effectiveness hierarchy with access-level annotations as supporting constraints; use context7-survey.md Phase 2 Task Mapping for detailed experimental parameters

---

## Revision Log

| Version | Date | Changes Made | Adversary Finding Addressed |
|---------|------|-------------|----------------------------|
| R1 | 2026-02-27 | Initial synthesis | — |
| R2 | 2026-02-27 | Critical fixes: DA-001/RT-001 (L0 conflation of null finding vs. directional evidence); DA-002/CC-002 (agreement count correction 7→5 STRONG, 9→4 MODERATE); IN-001 (Known Scope Exclusions section added). Major fixes: SR-001 (explicit arithmetic trace added); SR-002 (I-22 cross-reference added); SR-003 (per-agreement confidence qualifiers added); SR-005 (Tier 3 count note clarified); SM-001 (access-level column added to AGREE-5 hierarchy); SM-002 (AGREE-4 restructured to lead with Tier 1/2 evidence, A-16 demoted to corroborating caveat); SM-003/PM-001/CV-003 (Phase 2 Experimental Design Requirements section added with condition derivations); RT-002 (A-6 percentages removed from L0, directional language only); RT-003/IN-001 (Known Scope Exclusions section addresses survey scope limitations); DA-003 (L0 verdict framing corrected — null finding not refutation); DA-004 (revised hypothesis labeled as Alternative Hypothesis); DA-005 (vendor consensus reframed as "broadest operational consensus" not "strongest evidence"); CV-001 (A-31 Bsharat et al. added as primary source); CV-002 (C-13 DSPy venue corrected from "accepted at venue" to Tier 3 arXiv preprint); IN-002 (replication caveat added to A-23); IN-003 (vendor bias acknowledged in Known Scope Exclusions SE-3); SM-004 (testable prediction added to THEME-1); SM-006 (CONFLICT-2 explanations ranked by testability); DA-006/CC-004/RT-006 (THEME-1/THEME-3 speculative mechanistic claims explicitly labeled as synthesis-generated hypotheses, not confirmed findings); SR-007 (CONFLICT-4 resolution vs. UNRESOLVED label clarified). | DA-001 (Critical), DA-002/CC-002 (Critical/Major), IN-001 (Critical), SR-001-003, SM-001-006, RT-002-004, DA-003-007, PM-001-004, CV-001-002, IN-002-003 |
| R3 | 2026-02-27 | **P1 (SR-002-R2/CC-001-R2/FM-010):** Tier Analysis updated to 75 total sources; Tier 3 count corrected to 14 (A-31 is net-new, not a replacement for I-13; both are distinct documents). Removed all "A-31 replaces I-13" language. **P2 (SR-001-R2/CV-001-R2/FM-011):** All 13 Group C sources explicitly named with IDs in both the catalog (C-2, C-3, C-6, C-7, C-8, C-9, C-10, C-11, C-12, C-13, C-14, C-19, C-20) and the arithmetic trace. Added C-2 (Anthropic blog), C-3 (OpenAI platform guide), C-12 (DSPy assertions docs), C-14 (DSPy official site) as previously unnamed entries. Updated deduplication decisions table. **P3 (RT-001-R2):** SE-5 (Publication Bias) added to Known Scope Exclusions. **P4 (IN-001-R2/CV-002-R2):** Cond-6 flagged as "[Synthesis-generated hypothesis — not directly sourced from primary evidence]" with note that negative results should not invalidate synthesis. **P5 (SM-001-R2/PM-001-R2/FM-012):** Cond-6/Cond-7 relative priority added: Cond-7 = Recommended-A (higher evidence), Cond-6 = Recommended-B. **P6 (DA-002-R2):** "On the revised hypothesis" moved to end of L0 after Phase 2 mandate; renamed "Research direction from synthesis (secondary)" with explicit anti-anchoring note. **P7 (RT-002-R2/DA-004-R2):** AGREE-5 hierarchy header note added distinguishing prompt-accessible range (ranks 5-12) from non-accessible techniques (ranks 1-4). **P8 (SR-005-R2):** PS Integration key finding #4 updated to reference 7 conditions (5 Required + 2 Recommended with priority labels). **P9 (DA-001-R2):** Vendor product positioning bias caveat added to AGREE-3. **P10 (SR-003-R2):** CONFLICT-4 section heading qualified: "UNRESOLVED — natural-language self-refinement question only." **Note on RT-004 deferral (SR-003-R3/CV-003-R2 fix applied in R4):** RT-004 (circular citation chain in AGREE-4 — some industry sources trace back through each other to A-9) was identified as Major in I1 and addressed in R2's Revision Log under "RT-003 (A-31 framing)" but not explicitly named as RT-004 in R3's log. Status: RT-004 is PARTIALLY ADDRESSED — R2 added the circular citation note to AGREE-4; the note was refined in R4 with tier qualification. The finding is not fully resolved because the citation chain pattern persists in the industry source network, but the synthesis now explicitly acknowledges it and provides the tier-graded list of independent sources. | SR-002-R2, CC-001-R2, FM-010, SR-001-R2, CV-001-R2, FM-011, RT-001-R2, IN-001-R2, CV-002-R2, SM-001-R2, PM-001-R2, FM-012, DA-002-R2, RT-002-R2, DA-004-R2, SR-005-R2, DA-001-R2, SR-003-R2 |
| R4 | 2026-02-27 | **P1 (SR-001-R3/CC-001-R3/FM-014):** PS Integration Entry ID updated from "Barrier-1-Synthesis-R2" to "Barrier-1-Synthesis-R4"; document header updated to Revision 4. **P2 (CV-001-R3/FM-015):** Tier 3 count corrected from 14 to 15 (C-19 is Tier 3, was being miscounted in Tier 4); Tier 4 count corrected from 43 to 42; arithmetic remains 13+5+15+42=75; note updated with R4 correction explanation. **P3 (DA-001-R3/FM-016):** L0 epistemic distinction paragraph revised to eliminate false-balance parallel construction; explicitly documents evidence asymmetry (zero evidence for 60% hypothesis; multiple Tier 1 sources showing prohibition failure via AGREE-4); distinguishes the null finding on the specific 60% claim from the directional finding on standalone prohibition unreliability. **P4 (SR-002-R3):** Deduplication Decisions table corrected: C-2 now has its own row distinct from the I-1/C-1 deduplication decision; narrative note also updated. **P5 (SM-001-R3/SR-004-R3):** AGREE-5 intra-subgroup rank ordering evidence basis explicitly documented: ranks 5-6 by evidence tier (Tier 1); rank 7 by relevance to prohibition domain; rank 8 by evidence tier (Tier 3); ranks 9-11 explicitly labeled as synthesizer judgment based on vendor practice patterns, not controlled evidence. **P6 (CV-002-R3):** C-3 catalog entry updated with explicit caveat that key finding is inferred from context7 survey description, not direct content retrieval (403 inaccessible). **P7 (SM-002-R3):** Best Case Scenario paragraph added to L0 between Phase 2 mandate and Research Direction (secondary). **P8 (IN-001-R3):** Expert user moderating variable note added to AGREE-4 with guidance for Phase 2 experimental design. **P9 (SR-003-R3/CV-003-R2):** RT-004 deferral status explicitly noted in R3 Revision Log row. **P10 (PM-001-R3):** GAP-5 "DO NOT CITE" box relocated to precede the specific figures rather than follow them. **P11 (DA-002-R3/RT-001-R3):** AGREE-4 circular citation note updated to distinguish tier levels of A-20 (Tier 1), A-19 (Tier 3 large-scale), and A-31 (Tier 3 unreviewed) as independent evidence with graduated reliability. | SR-001-R3, CC-001-R3, FM-014, CV-001-R3, FM-015, DA-001-R3, FM-016, SR-002-R3, SM-001-R3, SR-004-R3, CV-002-R3, SM-002-R3, IN-001-R3, SR-003-R3, CV-003-R2, PM-001-R3, DA-002-R3, RT-001-R3 |

---

*Synthesis produced by ps-synthesizer | Revision 4 | 2026-02-27*
*Constitutional compliance: P-003 (no recursive subagents), P-020 (user authority respected), P-022 (all contradictions and limitations disclosed; source counts consistent across L0 and body; all Group C sources explicitly named; PS Entry ID updated to R4; no false-balance framing in epistemic claims)*
*Self-review (S-010) applied: patterns verified against source content; contradictions explicitly documented; all patterns cite sources; no unsourced assertions in synthesis body; L0 numbers verified against body content (75 in L0, 75 in Tier Analysis = 13+5+15+42); Tier 3 count reconciled to 15; Tier 4 count corrected to 42*
*Adversary revision: addresses all 3 Critical findings from I1 (DA-001, DA-002/CC-002, IN-001), all P1-P10 priority fixes from I2 adversary tournament (score 0.90), and all P1-P7+ priority fixes from I3 adversary tournament (score 0.93 → targeting >= 0.95)*
