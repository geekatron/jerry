# Academic Literature Survey: Negative Prompting in LLMs

> ps-researcher-001 | TASK-001 | PROJ-014 | 2026-02-27 | **Revision 5 (Final)**
> Sources: 30 unique sources (13 Tier 1 peer-reviewed + 5 Tier 2 peer-reviewed (including 1 non-archival IJCAI symposium) + 10 arXiv preprints + 1 rejected submission + 1 commercially-affiliated report)
> Search queries executed: 20/20
> Adversarial gate: Iteration 1 scored 0.78 (REJECTED); Iteration 2 scored 0.86 (REVISE); Iteration 3 scored 0.925 (REVISE); Iteration 4 scored 0.9425 (REVISE); this final revision addresses 1 Minor finding (IT4-001) and 1 evidence quality improvement (EQ-001)

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Key findings overview (four phenomena distinguished) |
| [L1: Source Catalog](#l1-source-catalog) | Structured table of all sources with quality annotations |
| [L2: Detailed Findings](#l2-detailed-findings) | Per-source detailed analysis |
| [Research Methodology](#research-methodology) | Search strategy, coverage, and limitations |
| [PROJ-014 Hypothesis Context](#proj-014-hypothesis-context) | Origin of the 60% claim and research gap |
| [Revision Log](#revision-log) | Changes made in response to adversarial critique |

---

## L0: Executive Summary

This survey catalogs 30 sources spanning 2022 through early 2026 on the topic of negative prompting in large language models. The central tension in this literature is not a simple "negative prompting fails" narrative, but rather a nuanced picture: **some forms of negative information substantially improve LLM performance, while direct prohibition instructions ("don't do X") remain unreliable.** The distinction between these forms is the single most important finding of this survey.

### Four Distinct Phenomena

The literature addresses four distinct phenomena that are frequently conflated but have different mechanisms, evidence bases, and practical implications. Readers must distinguish these when applying findings:

**(a) Negation comprehension** -- whether LLMs understand the logical meaning of "NOT X" in natural language text. This is the most heavily studied area (Sources 3, 4, 5, 8, 9, 27, 29). Evidence from McKenzie et al. (2023, Source 9) showed that on specific negation-related tasks in the Inverse Scaling Prize dataset, performance dropped below random chance beyond approximately 10^22 training FLOPs in models available at that time (Gopher, GPT-3, Anthropic models). However, this finding may be a historical artifact of 2022-2023-era architectures: Vrabcova et al. (2025, Source 5) found a Spearman correlation of 0.867 between model size and negation handling when testing newer model families (Llama 3, Qwen 2.5, Mistral), suggesting architectural improvements are substantially reversing the inverse scaling trend. The majority of evidence in this survey comes from negation comprehension studies, not from prohibition instruction-following studies -- a distinction that matters for PROJ-014's practical questions.

**(b) Prohibition instruction-following** -- whether LLMs obey explicit "don't do X" directives in prompts. This is the most practically relevant phenomenon for PROJ-014 but the least directly studied. Harada et al. (2024, Source 16) demonstrated that multi-instruction success follows an exponential decay pattern: if individual instruction success rate is p, then the rate for N instructions is p^N. For example, if each of 10 constraints (including "don't" rules) has 90% individual compliance, combined success drops to just 34.9%. Geng et al. (2025, Source 20) showed that system/user prompt separation fails to establish reliable instruction hierarchies. Tripathi, Allu, and Ahmed (2026, Source 19) found instruction violations ranging from 660 to 1,330 per 600 samples across 13 state-of-the-art models, with a critical finding that accuracy and compliance are independent capabilities. No paper in this survey directly compares identical constraints framed as "don't do X" versus "always do Y" in controlled A/B experiments -- this remains the critical research gap.

**(c) Training/alignment constraints** -- whether negative rules embedded during training (RLHF, Constitutional AI) effectively shape model behavior. Bai et al. (2022, Source 10) demonstrated that principle-based negative constraints ("The AI should not do X") enable alignment without human labels when embedded in training. Arditi et al. (2024, Source 7) revealed that refusal behavior is mediated by a single one-dimensional subspace in the residual stream, explaining both the brittleness of safety alignment and why negative constraints can be easily circumvented. Betley et al. (2025; published in Nature, DOI: 10.1038/s41586-025-09937-5, Source 25) showed that narrow fine-tuning on negative behaviors produces unexpected broad behavioral changes. This phenomenon is distinct from prompt-time prohibition -- training-time constraints operate through different mechanisms.

**(d) Negative framing effects** -- how emotional, contrastive, or sentiment-based negative information affects LLM outputs. This is where negative prompting shows the most consistent *positive* results. Wang et al. (2024, Source 1) demonstrated that negative emotional stimuli (psychological pressure framing, not prohibition instructions) improve performance by 12.89% on Instruction Induction and 46.25% on BIG-Bench tasks. Chia et al. (2023, Source 11) showed that contrastive chain-of-thought prompting, providing both valid and invalid reasoning examples, yields accuracy improvements of up to 16 points on Bamboogle. Gandhi and Gandhi (2025, Source 14; note: commercially-affiliated Joyspace AI report without peer review) found that negative sentiment framing reduced factual accuracy by 8.4%, though this finding should be weighted with caution given the absence of independent peer review. Source 14 is the only study in this survey that directly compares positive, neutral, and negative framing on factual accuracy; its commercially-affiliated status and modest sample size (N=500) mean this 8.4% figure requires independent replication before it can be relied upon for design decisions.

**Note on cross-modality context:** Source 2 (Ban et al., 2024) studies negative prompt mechanisms in diffusion models (image generation), not LLMs. It falls outside the four LLM-specific phenomena above and is included solely for mechanistic analogy: the "deletion through neutralization" finding in latent space is hypothesis-generating for LLM research but has no validated transfer to autoregressive language models. See L2 Source 2 for full caveats.

### When Negative Prompting Works (Prompt-Level Techniques)

Two studies demonstrate that negative instructions can be made more effective through prompt-level techniques that any practitioner can implement without model access:

- **Warning-based meta-prompting:** Barreto and Jana (2025, EMNLP Findings, Source 23) showed that warning models about negation traps (rather than using prohibition directly) improves distractor negation accuracy by up to 25.14% over baselines. This is the most directly actionable finding for PROJ-014: instead of "don't hallucinate," warn the model "the following task contains negation -- be careful not to reverse the intended meaning."
- **Atomic constraint decomposition:** Ferraz et al. (2024, EMNLP, Source 15) demonstrated that decomposing compound negative constraints into atomic units (DeCRIM) improves compliance by 7.3% on RealInstruct and 8.0% on IFEval. Instead of "don't include personal opinions or unverified claims," decompose into separate atomic constraints: (1) "every claim must cite a source" and (2) "use only third-person perspective."

These findings suggest that the failure mode is not in the concept of negative constraints per se, but in the *delivery mechanism* -- blunt prohibition instructions fail, while structured prompt-level approaches (meta-warnings, decomposition) succeed with meaningful but moderate improvements.

### Model-Internal Approaches to Negative Constraints

Beyond prompt-level techniques, one study demonstrates substantially higher effectiveness through model-internal intervention:

- **Conditional Activation Steering (CAST):** Lee et al. (2024, ICLR 2025 Spotlight, Source 28) showed that CAST improves harmful refusal from 45.78% to 90.67% on Qwen 1.5B (1.8B parameters) while harmless refusal stays at only 2.20% (i.e., 97.8% of harmless prompts are correctly accepted). However, CAST is **not a prompting technique** -- it requires direct access to the model's internal activations, PCA decomposition of residual stream vectors, and injection of steering vectors at inference time. These results cannot be reproduced through prompt engineering alone. CAST is included here because it demonstrates the ceiling of what targeted negative constraint enforcement can achieve, but practitioners designing system prompts should not use CAST's effectiveness figures as benchmarks for prompt-level approaches.

### Hallucination and Negation

Varshney et al. (2024, Source 6) demonstrated that negation increases hallucination in LLMs, but the effect is highly task-dependent. Specifically for LLaMA-2 (13B), hallucination rates on the Multiple-Choice QA task increased from approximately 26% (without negation) to 59.23% (with negation) -- a ~33 percentage point increase. However, baseline hallucination rates varied substantially across the four tasks studied: False Premise Completion (63.77%), Constrained Fact Generation (72.33%), MCQA (36.6%), and Fact Generation (62.59%), all measured with negation present. The 26%-to-59% comparison applies specifically to the MCQA task for LLaMA-2 and should not be generalized as a universal baseline.

### Verification-Based Alternatives

Dhuliawala et al. (2023; ACL 2024 Findings, Source 22) demonstrated that Chain-of-Verification (CoVe) -- a four-stage pipeline of drafting, planning verification questions, answering independently, and generating verified responses -- more than doubles precision on Wikidata list tasks (0.17 to 0.36). CoVe is categorized separately from negative prompting techniques: it is a *verification pipeline* that provides a structured alternative to prohibition-style "don't hallucinate" instructions, rather than a form of negative prompting itself. Its inclusion in this survey serves as a reference point for what process-based constraints achieve compared to content-based negative instructions.

### Key Research Gaps

Four significant gaps remain: (1) no controlled A/B study directly compares "don't do X" versus "always do Y" system prompt formulations on identical tasks (Source 19, Source 20, Source 15 all demonstrate instruction-following challenges but none isolate positive vs. negative framing as the independent variable); (2) the interaction between negative instructions and chain-of-thought reasoning is under-explored (Source 11 studies contrastive CoT but not prohibition-instruction CoT interaction); (3) multilingual negative instruction-following is almost entirely unexamined (only Source 5 addresses non-English negation, and only for comprehension); and (4) the theoretical understanding of why transformer attention mechanisms process negation poorly at the architectural level remains incomplete (Source 7 identifies the one-dimensional refusal subspace but does not explain why negation comprehension fails).

---

## PROJ-014 Hypothesis Context

PROJ-014 investigates the claim -- common in prompt engineering guidance and vendor documentation -- that negative prompting (e.g., "don't hallucinate," "don't make things up") can reduce hallucination rates by significant margins. **The specific "60% hallucination reduction" figure is PROJ-014's working hypothesis target for experimental testing.** Despite extensive search, no specific vendor document, blog post, or practitioner publication could be identified as the origin of this figure. It appears to be an informal "rule of thumb" circulating in practitioner communities (prompt engineering forums, internal vendor guidance, conference hallway discussions) without a single traceable published source. The figure may represent an aggregation of optimistic practitioner anecdotes rather than a documented empirical claim. This survey's purpose is to evaluate what academic evidence exists for or against such claims, regardless of their specific origin.

**What this survey found:** No peer-reviewed study validates a 60% hallucination reduction from negative prompting. The closest evidence is Varshney et al. (2024, Source 6), which shows negation *increases* hallucination by ~33 percentage points on specific tasks. The evidence suggests prohibition-style negative prompting is more likely to increase hallucination than reduce it, while structured approaches (verification pipelines like CoVe from Source 22, constraint decomposition via DeCRIM from Source 15, meta-warnings from Source 23) can achieve meaningful improvements through different mechanisms.

---

## L1: Source Catalog

| # | Title | Authors/Org | Year | URL/DOI | Key Finding | Quality Notes |
|---|-------|-------------|------|---------|-------------|---------------|
| 1 | NegativePrompt: Leveraging Psychology for Large Language Models Enhancement via Negative Emotional Stimuli | Wang, Li, Chang, Wang, Wu | 2024 | [IJCAI 2024](https://arxiv.org/abs/2405.02814) | Negative emotional stimuli improve LLM performance: 12.89% on Instruction Induction, 46.25% on BIG-Bench | Tier 1 venue (IJCAI main track). Peer-reviewed. 5 LLMs, 45 tasks. |
| 2 | Understanding the Impact of Negative Prompts: When and How Do They Take Effect? | Ban, Wang, Zhou, Cheng, Gong, Hsieh | 2024 | [arXiv:2406.02965](https://arxiv.org/abs/2406.02965) | Negative prompts operate via delayed effect and deletion through neutralization in latent space | Tier 3 preprint. **Caveat: Focused on diffusion models (image generation), not LLMs. Included for cross-modality mechanistic analogy only; falls outside the four LLM-specific phenomena taxonomy.** |
| 3 | This is not a Dataset: A Large Negation Benchmark to Challenge Large Language Models | Garcia-Ferrero, Altuna, Alvez, Gonzalez-Dios, Rigau | 2023 | [EMNLP 2023](https://arxiv.org/abs/2310.15941) | LLMs proficient on affirmative but struggle on negative sentences, relying on superficial cues | Tier 1 venue. Peer-reviewed. ~400K sentences. |
| 4 | Language models are not naysayers: An analysis of language models on negation benchmarks | Truong, Baldwin, Verspoor, Cohn | 2023 | [*SEM 2023](https://arxiv.org/html/2306.08189) | Larger LMs more insensitive to negation; InstructGPT outperforms via instruction-tuning not scaling | Tier 2 venue. Peer-reviewed. 5 benchmarks. |
| 5 | Negation: A Pink Elephant in the Large Language Models' Room? | Vrabcova, Kadlcik, Sojka, Stefanik, Spiegel | 2025 | [arXiv:2503.22395](https://arxiv.org/html/2503.22395v2) | Strong positive correlation (0.867) between model size and negation ability in newer models | Tier 3 preprint. Masaryk University. Rigorous multilingual design (4 languages, 2 novel datasets). |
| 6 | Power of Negation in Fostering LLM Hallucinations | Varshney, Raj, Mishra, Chatterjee, Sarkar, Saeidi, Baral | 2024 | [arXiv:2406.05494](https://arxiv.org/html/2406.05494v1) | Negation increases hallucination; task-specific rates range from 37% to 72% with negation (MCQA: ~26% to ~59% for LLaMA-2 specifically) | Tier 3 preprint. Arizona State University. 4 tasks, 100-300 instances each. |
| 7 | Refusal in Language Models Is Mediated by a Single Direction | Arditi, Obeso, Syed, Paleka, Panickssery, Gurnee, Nanda | 2024 | [NeurIPS 2024](https://arxiv.org/abs/2406.11717) | Refusal mediated by one-dimensional subspace across 13 models up to 72B parameters | Tier 1 venue. Peer-reviewed. |
| 8 | Vision-Language Models Do Not Understand Negation (NegBench) | Alhamoud, Alshammari, Tian, Li, Torr, Kim, Ghassemi | 2025 | [CVPR 2025](https://arxiv.org/abs/2501.09425) | VLMs perform at chance on negation; fine-tuning yields 10% recall increase, 28% accuracy boost | Tier 1 venue. Peer-reviewed. 79K examples. |
| 9 | Inverse Scaling: When Bigger Isn't Better | McKenzie, Lyzhov, Pieler, Parrish, Mueller, et al. | 2023 | [TMLR](https://arxiv.org/abs/2306.09479) | Specific negation tasks show inverse scaling below random beyond ~10^22 FLOPs (2022-2023-era models) | Tier 2 venue (TMLR). Peer-reviewed. 11 datasets. Authors note competition-sourced datasets may have selection bias. |
| 10 | Constitutional AI: Harmlessness from AI Feedback | Bai, Kadavath, Kundu, Askell, et al. (Anthropic) | 2022 | [arXiv:2212.08073](https://arxiv.org/abs/2212.08073) | Principle-based negative constraints enable alignment when embedded in training (not prompts) | Tier 3 preprint. Anthropic. Foundational work; widely cited (5000+). |
| 11 | Contrastive Chain-of-Thought Prompting | Chia, Chen, Tuan, Poria, Bing | 2023 | [arXiv:2311.09277](https://arxiv.org/abs/2311.09277) | Including negative reasoning examples yields +16.0 on Bamboogle, +9.8 on GSM-8K (GPT-3.5-Turbo) | Tier 3 preprint. DAMO-NLP-SG. Contrastive examples, not prohibition instructions. |
| 12 | Large Language Models Understand and Can Be Enhanced by Emotional Stimuli (EmotionPrompt) | Li, Wang, Zhang, Zhu, Hou, Lian, Luo, Yang, Xie | 2023 | [LLM@IJCAI'23](https://arxiv.org/abs/2307.11760) | 8% improvement on Instruction Induction, 115% on BIG-Bench, 10.9% on generative tasks | **Tier 2 venue (LLM@IJCAI'23 is a non-archival IJCAI symposium with single-blind peer review, not the main IJCAI conference track).** 6 LLMs, 45 tasks, 106-person human study. |
| 13 | Quantifying Language Models' Sensitivity to Spurious Features in Prompt Design | Sclar, Choi, Tsvetkov, Suhr | 2024 | [ICLR 2024](https://arxiv.org/abs/2310.11324) | Up to 76 accuracy point swings from formatting variations in LLaMA-2-13B | Tier 1 venue. Peer-reviewed. |
| 14 | Prompt Sentiment: The Catalyst for LLM Change | Gandhi, Gandhi (Joyspace AI) | 2025 | [arXiv:2503.13510](https://arxiv.org/html/2503.13510v1) | Negative prompts reduce factual accuracy by 8.4% (92.3% to 84.5%); responses 17.6% shorter | **Commercially-affiliated arXiv report (Joyspace AI). Not peer-reviewed. No independent replication. 500 prompts only. Model version designations (Claude v1.3, ChatGPT v4, etc.) are imprecise. Findings should be treated as preliminary until independently validated.** |
| 15 | LLM Self-Correction with DeCRIM | Ferraz, Mehta, Lin, Chang, Oraby, Liu, Subramanian, Chung, Bansal, Peng | 2024 | [EMNLP 2024](https://arxiv.org/abs/2410.06458) | GPT-4 fails constraints on 21%+ of instructions; DeCRIM improves Mistral by 7.3% (RealInstruct), 8.0% (IFEval) | Tier 1 venue. Peer-reviewed. |
| 16 | Curse of Instructions: Large Language Models Cannot Follow Multiple Instructions at Once | Harada, Yamazaki, Taniguchi, Kojima, Iwasawa, Matsuo | 2024 | [OpenReview](https://openreview.net/forum?id=R6q67CDBCH) | Success rate follows power law: individual rate^N for N instructions; self-refinement improves GPT-4o from 15% to 31% on 10 instructions | **Rejected from ICLR 2025.** Methodology is sound (ManyIFEval benchmark, 5 models), but findings should be weighted as unreviewed. The exponential decay model is independently plausible given DeCRIM's findings (Source 15). |
| 17 | Instruction-Following Evaluation for Large Language Models (IFEval) | Zhou, Lu, Mishra, Brahma, Basu, Luan, Zhou, Hou (Google) | 2023 | [arXiv:2311.07911](https://arxiv.org/abs/2311.07911) | Introduces 25 verifiable instruction types across ~500 prompts with strict/loose accuracy metrics | Tier 3 preprint. Google. Foundational benchmark; widely adopted. |
| 18 | Do LLMs "Know" Internally When They Follow Instructions? | Heo, Heinze-Deml, Elachqar, Ren, Nallasamy, Miller, Chan, Narain (Apple) | 2024 | [arXiv:2410.14516](https://arxiv.org/html/2410.14516v1) | Models achieve 0.7-0.88 AUROC for predicting instruction-following success; phrasing sensitivity stronger than difficulty | Tier 3 preprint. Apple ML Research. Linear probing methodology. |
| 19 | The Instruction Gap: LLMs get lost in Following Instruction | Tripathi, Allu, Ahmed (Yellow.ai) | 2026 | [arXiv:2601.03269](https://arxiv.org/html/2601.03269) | Violations range from 660 to 1330 per 600 samples across 13 models; accuracy and compliance are independent | Tier 3 preprint. Yellow.ai. **Model names verified via WebFetch (2026-02-27): paper uses GPT-5 (Medium/mini/nano), GPT-4.1, Claude Sonnet 4, Gemini 2.0/2.5-Flash, DeepSeek-R1, o4-mini. These are real model designations as of the January 2026 publication date.** The original survey iteration incorrectly formatted "Claude-4-Sonnet" -- the correct designation is "Claude Sonnet 4." The original iteration also listed the year as 2025; the arXiv ID prefix "2601" indicates January 2026. |
| 20 | Control Illusion: The Failure of Instruction Hierarchies in Large Language Models | Geng, Li, Mu, Han, Baldwin, Abend, Hovy, Frermann | 2025 | [AAAI 2026](https://arxiv.org/abs/2502.15851) | System/user prompt separation fails to establish reliable instruction hierarchy | Tier 1 venue (AAAI). Peer-reviewed. **Note: Some findings drawn from abstract; full quantitative failure rates not fully extracted from paper body.** [^2] |
| 21 | Investigating the Role of Prompting and External Tools in Hallucination Rates of LLMs | Barkley, van der Merwe (Stellenbosch University) | 2024 | [arXiv:2410.19385](https://arxiv.org/html/2410.19385v1) | Self-Consistency achieves 84.89% accuracy (vs. 61.87% baseline); external tools deteriorate smaller model performance | Tier 3 preprint. Single 8B model, 3 runs only. |
| 22 | Chain-of-Verification Reduces Hallucination in Large Language Models (CoVe) | Dhuliawala, Komeili, Xu, Raileanu, Li, Celikyilmaz, Weston (Meta) | 2023 | [ACL 2024 Findings](https://arxiv.org/abs/2309.11495) | Precision doubles on Wikidata tasks (0.17 to 0.36); hallucinated entities drop from 2.95 to 0.68 | Tier 1 venue. Peer-reviewed. **Note: CoVe is a verification pipeline, not a form of negative prompting. Included as a reference alternative to prohibition-style approaches.** |
| 23 | This is not a Disimprovement: Improving Negation Reasoning in LLMs via Prompt Engineering | Barreto, Jana | 2025 | [EMNLP 2025 Findings](https://aclanthology.org/2025.findings-emnlp.761/) | Warning-based and persona-based prompts improve accuracy by up to 3.17%; distractor negation accuracy by up to 25.14% | Tier 1 venue. Peer-reviewed. Most directly relevant to PROJ-014's prompt engineering focus. |
| 24 | SORRY-Bench: Systematically Evaluating Large Language Model Safety Refusal | Xie, Qi, Zeng, Huang, Sehwag, et al. | 2024 | [ICLR 2025](https://arxiv.org/abs/2406.14598) | 44-class safety taxonomy with 440 instructions; refusal behavior varies dramatically across models | Tier 1 venue. Peer-reviewed. 50+ LLMs benchmarked. |
| 25 | Emergent Misalignment: Narrow finetuning can produce broadly misaligned LLMs | Betley, Tan, Warncke, Sztyber-Betley, Bao, Soto, Labenz, Evans | 2025 | [Nature 649, 584-589 (2026)](https://doi.org/10.1038/s41586-025-09937-5) | Fine-tuning on insecure code produces >80% insecure code + ~20% misaligned responses on unrelated tasks | **Tier 1 venue (Nature). Peer-reviewed. DOI: 10.1038/s41586-025-09937-5.** Extended version of ICML 2025 paper. Originally arXiv:2502.17424 (Feb 2025); Nature publication January 2026. Venue confirmed via WebSearch (2026-02-27). |
| 26 | Bounding the Capabilities of Large Language Models in Open Text Generation with Prompt Constraints | Lu, Zhang, Zhang, Wang, Yang | 2023 | [EACL 2023 Findings](https://arxiv.org/abs/2302.09185) | Structural and stylistic constraints expose generative failure modes across models | Tier 2 venue. Peer-reviewed. |
| 27 | LogicBench: Towards Systematic Evaluation of Logical Reasoning Ability of LLMs | Parmar, Patel, Varshney, Nakamura, Luo, Mashetty, Mitra, Baral | 2024 | [ACL 2024](https://arxiv.org/abs/2404.15522) | LLMs fail on inference rules involving negated premises; poor performance on 25 reasoning patterns | Tier 1 venue. Peer-reviewed. |
| 28 | Programming Refusal with Conditional Activation Steering (CAST) | Lee, Padhi, Ramamurthy, Miehling, Dognin, Nagireddy, Dhurandhar (IBM + UPenn) | 2024 | [ICLR 2025 Spotlight](https://arxiv.org/html/2409.05907v3) | Qwen 1.5B: harmful refusal 45.78% to 90.67% while harmless refusal stays at 2.20% (97.8% of harmless prompts correctly accepted) | Tier 1 venue (ICLR Spotlight). Peer-reviewed. 10 LLMs. **Note: CAST is a model-internal activation steering technique, not a prompt engineering approach.** |
| 29 | Thunder-NUBench: A Benchmark for LLMs' Sentence-Level Negation Understanding | So, Lee, Jung, Lee, Kang, Kim, Lee | 2025 | [arXiv:2506.14397](https://arxiv.org/abs/2506.14397) | Novel benchmark contrasting standard negation with local negation, contradiction, and paraphrase | Tier 3 preprint. **Reviewed from abstract only; full quantitative results not extracted.** Included for benchmark coverage completeness. [^1] |
| 30 | Large Language Model Instruction Following: A Survey of Progresses and Challenges | Lou, Zhang, Yin | 2024 | [Computational Linguistics 50(3):1053-1095](https://direct.mit.edu/coli/article/50/3/1053/121669/) | Comprehensive survey documenting instruction-following challenges including negative constraint adherence | Tier 2 venue (Computational Linguistics, MIT Press). Peer-reviewed. |

[^1]: Source 29 was reviewed from its abstract only. Claims about its benchmark design are based on abstract description; full quantitative results and methodology details were not available for extraction. This source is included for its contribution to benchmark landscape awareness, not for specific quantitative findings.

[^2]: Source 20 was partially reviewed. Key qualitative findings (instruction hierarchy failure, societal framing effects) are drawn from the paper, but full quantitative failure rates were not fully extracted from the paper body. Specific numerical claims about Source 20 should be verified against the complete paper.

---

## L2: Detailed Findings

### Source 1: NegativePrompt: Leveraging Psychology for Large Language Models Enhancement via Negative Emotional Stimuli

- **Authors:** Xu Wang, Cheng Li, Yi Chang, Jindong Wang, Yuan Wu
- **Year:** 2024
- **URL/DOI:** [https://arxiv.org/abs/2405.02814](https://arxiv.org/abs/2405.02814)
- **Publication venue:** IJCAI 2024
- **Methodology:** Tested 5 LLMs (Flan-T5-Large, Vicuna, Llama 2, ChatGPT, GPT-4) across 45 tasks using 10 specifically designed negative emotional stimuli grounded in psychological principles. Conducted attention visualization experiments to investigate how negative emotional stimuli influence model processing.
- **Key findings:** NegativePrompt significantly enhances performance: 12.89% relative improvement on Instruction Induction tasks and 46.25% relative improvement on BIG-Bench tasks. The approach is distinct from simple negation -- it uses psychologically-grounded negative emotional framing (e.g., consequences of failure) rather than prohibition instructions.
- **Phenomenon category:** (d) Negative framing effects
- **Relevance to negative prompting:** Demonstrates that *how* negative information is framed matters critically. Negative emotional stimuli (social pressure, consequence awareness) enhance performance, while simple "don't do X" instructions degrade it. The 46.25% BIG-Bench improvement is among the strongest positive results for any form of negative information in this survey.
- **Limitations:** The study does not compare directly against prohibition-style negative prompts. Code is available but specific boundary conditions for when NegativePrompt fails are not documented.

### Source 2: Understanding the Impact of Negative Prompts: When and How Do They Take Effect?

- **Authors:** Yuanhao Ban, Ruochen Wang, Tianyi Zhou, Minhao Cheng, Boqing Gong, Cho-Jui Hsieh
- **Year:** 2024
- **URL/DOI:** [https://arxiv.org/abs/2406.02965](https://arxiv.org/abs/2406.02965)
- **Publication venue:** arXiv (Computer Vision)
- **Methodology:** First comprehensive study of negative prompt mechanisms in diffusion models. Extensive empirical analysis with adaptive algorithms.
- **Key findings:** Two primary mechanisms identified: (1) delayed effect -- negative prompts impact after positive prompts render content; (2) deletion through neutralization -- mutual cancellation in latent space. Demonstrated practical application for object inpainting with minimal background alteration.
- **Phenomenon category:** Cross-modality mechanistic study (outside the four LLM-specific phenomena taxonomy by design)
- **Relevance to negative prompting:** While focused on image generation (diffusion models, not autoregressive LLMs), the mechanistic findings about latent space cancellation are suggestive. **Caveat: Transfer from diffusion model mechanisms to LLM mechanisms is theoretical and unvalidated.** The two modalities use fundamentally different architectures (iterative denoising vs. autoregressive token generation), so mechanistic parallels should be treated as hypothesis-generating rather than evidence-bearing for LLM behavior. This source is included for cross-modality context, not as evidence about LLM negative prompting effectiveness.
- **Limitations:** Primarily focused on diffusion models rather than text-only LLMs. No empirical validation of whether similar mechanisms operate in autoregressive language models.

### Source 3: This is not a Dataset: A Large Negation Benchmark to Challenge Large Language Models

- **Authors:** Iker Garcia-Ferrero, Begona Altuna, Javier Alvez, Itziar Gonzalez-Dios, German Rigau
- **Year:** 2023
- **URL/DOI:** [https://arxiv.org/abs/2310.15941](https://arxiv.org/abs/2310.15941)
- **Publication venue:** EMNLP 2023
- **Methodology:** Semi-automatically generated ~400,000 descriptive sentences about commonsense knowledge with negation in ~2/3 of the corpus. Evaluated largest available open LLMs using zero-shot approaches; fine-tuned selected models.
- **Key findings:** LLMs demonstrate proficiency with affirmative sentences but struggle with negative sentences, often relying on superficial cues rather than genuine understanding. Fine-tuning improved performance on negative sentences but failed to achieve robust generalization across negation types.
- **Phenomenon category:** (a) Negation comprehension
- **Relevance to negative prompting:** Provides the largest-scale evidence that LLMs fundamentally struggle with negation at the comprehension level, which directly impacts their ability to follow negative instructions.
- **Limitations:** Dataset is semi-automatically generated (potential noise). Fine-tuning results suggest architectural rather than data-driven limitations.

### Source 4: Language models are not naysayers: An analysis of language models on negation benchmarks

- **Authors:** Thinh Hung Truong, Timothy Baldwin, Karin Verspoor, Trevor Cohn
- **Year:** 2023
- **URL/DOI:** [https://arxiv.org/html/2306.08189](https://arxiv.org/html/2306.08189)
- **Publication venue:** *SEM 2023
- **Methodology:** Tested GPT-Neo (125M-6.7B), OPT (125M-6.7B), GPT-3 (175B), InstructGPT (175B), FLAN-T5-XXL (11B) across 5 benchmarks in 3 categories: sensitivity (MKR-NQ: 3,360 samples, MWR: 27,546), lexical semantics (SAR: 2,000), and reasoning (NegNLI: 4,500, NaN-NLI: 258, MoNLI: 200). Used WHR (Weighted Hit Rate) and accuracy metrics.
- **Key findings:** (1) Inverse scaling: larger LMs more insensitive to negation, with GPT-Neo-125M outperforming larger variants. (2) Near-random performance on antonym/synonym tasks (~50% vs. BERT-large's 92.5%). (3) Instruction-tuning (InstructGPT) improves negation reasoning more effectively than scaling.
- **Phenomenon category:** (a) Negation comprehension
- **Relevance to negative prompting:** Directly demonstrates that scaling alone does not fix negation understanding, but instruction-tuning can help -- critical insight for prompt engineering strategy. Note: findings based on 2022-2023-era models; architectural improvements in newer models may alter this picture (see Source 5).
- **Limitations:** Imperfect WHR metric. Limited prompt engineering exploration. English-only. Possible instruction-tuning data overlap with test distributions.

### Source 5: Negation: A Pink Elephant in the Large Language Models' Room?

- **Authors:** Tereza Vrabcova, Marek Kadlcik, Petr Sojka, Michal Stefanik, Michal Spiegel
- **Year:** 2025
- **URL/DOI:** [https://arxiv.org/html/2503.22395v2](https://arxiv.org/html/2503.22395v2)
- **Publication venue:** arXiv (Masaryk University)
- **Methodology:** Tested Llama 3 (3B/8B/70B), Qwen 2.5 (1.5B/7B/72B), Mistral (Nemo 12B/Small 22B/Large 123B) on two novel multilingual textual entailment datasets: NoFEVER-ML (2,600 triplets) and NoSNLI-ML (6,261 triplets) across English, Czech, German, Ukrainian. Used accuracy and negation sensitivity metrics with Spearman correlation.
- **Key findings:** Strong positive correlation (0.867) between model size and negation handling in newer architectures -- a Spearman correlation of 0.867 represents a strong positive relationship, suggesting architectural improvements in Llama 3, Qwen 2.5, and Mistral model families may be substantially reversing the inverse scaling trend documented by McKenzie et al. (2023) and Truong et al. (2023). FEVER-based tasks (fact-based) outperform SNLI (commonsense). English achieves highest accuracy; Czech worst on SNLI (p < 0.05). Models perform better on premises with higher information specificity.
- **Phenomenon category:** (a) Negation comprehension
- **Relevance to negative prompting:** Substantially challenges the blanket claim that larger models are worse at negation. The field may be entering a period where architectural improvements are closing the negation comprehension gap. However, this addresses negation *comprehension*, not prohibition instruction-following -- the practical gap for PROJ-014 remains open.
- **Limitations:** Opaque pretraining details prevent full understanding. Excludes post-training effects. Semi-automated translations introduced occasional errors.

### Source 6: Power of Negation in Fostering LLM Hallucinations

- **Authors:** Neeraj Varshney, Satyam Raj, Venkatesh Mishra, Agneet Chatterjee, Ritika Sarkar, Amir Saeidi, Chitta Baral
- **Year:** 2024
- **URL/DOI:** [https://arxiv.org/html/2406.05494v1](https://arxiv.org/html/2406.05494v1)
- **Publication venue:** arXiv (Arizona State University)
- **Methodology:** Tested LLaMA-2-chat (13B), Vicuna-v1.5 (13B), Orca-2 (13B), BARD/Gemini, GPT-4 across 4 tasks: False Premise Completion (300 instances), Constrained Fact Generation (100), Multiple-Choice QA (100), Fact Generation (300). Used human evaluation with three-level annotation and LLM-based factuality checking.
- **Key findings:** Hallucination rates with negation are highly task-dependent: FPC 63.77%, CFG 72.33%, MCQA 36.6%, FG 62.59%. The most cited comparison: LLaMA-2 on the MCQA task shows ~26% hallucination without negation vs. 59.23% with negation -- a ~33 percentage point increase. However, this comparison is specific to one model on one task. Across all tasks and models, baseline rates vary enormously. Cautionary instructions + exemplars showed best mitigation; knowledge augmentation actually increased hallucination by ~50% on false premises.
- **Phenomenon category:** (a) Negation comprehension / (b) Prohibition instruction-following
- **Relevance to negative prompting:** Most direct evidence that negation in prompts actively increases hallucination rates. The finding that knowledge augmentation worsens performance on false premises is particularly relevant -- it suggests that simply adding "don't hallucinate" could be counterproductive.
- **Limitations:** Four tasks only. Limited to open-source 13B models (plus BARD/GPT-4 for comparison). English only. Modest dataset sizes (100-300 instances).

### Source 7: Refusal in Language Models Is Mediated by a Single Direction

- **Authors:** Andy Arditi, Oscar Obeso, Aaquib Syed, Daniel Paleka, Nina Panickssery, Wes Gurnee, Neel Nanda
- **Year:** 2024
- **URL/DOI:** [https://arxiv.org/abs/2406.11717](https://arxiv.org/abs/2406.11717)
- **Publication venue:** NeurIPS 2024
- **Methodology:** Analyzed residual stream activations across 13 popular open-source chat models up to 72B parameters to identify the mechanistic basis of refusal behavior.
- **Key findings:** Refusal is mediated by a single one-dimensional subspace. Erasing this direction prevents refusal of harmful instructions. Adding this direction elicits refusal on harmless instructions. Developed a white-box jailbreak with minimal capability degradation.
- **Phenomenon category:** (c) Training/alignment constraints
- **Relevance to negative prompting:** Reveals that LLMs implement negative constraints (refusal) through a surprisingly simple linear mechanism, which explains both the brittleness of safety alignment and why negative instructions can be easily circumvented.
- **Limitations:** Focus on open-source models only. Does not address whether refusal is equally one-dimensional in closed-source, more heavily aligned models.

### Source 8: Vision-Language Models Do Not Understand Negation (NegBench)

- **Authors:** Kumail Alhamoud, Shaden Alshammari, Yonglong Tian, Guohao Li, Philip Torr, Yoon Kim, Marzyeh Ghassemi
- **Year:** 2025
- **URL/DOI:** [https://arxiv.org/abs/2501.09425](https://arxiv.org/abs/2501.09425)
- **Publication venue:** CVPR 2025
- **Methodology:** NegBench: 79,000 examples across 18 task variations using image, video, and medical datasets. Two core tasks: Retrieval with Negation and MCQ with Negated Captions. Tested CLIP models with fine-tuning experiments.
- **Key findings:** VLMs perform at chance level on negation tasks. Fine-tuning CLIP on synthetic negated captions yields 10% recall increase and 28% accuracy boost on negated questions.
- **Phenomenon category:** (a) Negation comprehension (multimodal)
- **Relevance to negative prompting:** Demonstrates that negation failure is not LLM-specific but extends to multimodal models, suggesting fundamental architectural limitations in transformer-based systems.
- **Limitations:** Primarily focused on CLIP-family models. Generalization to pure LLMs is indirect.

### Source 9: Inverse Scaling: When Bigger Isn't Better

- **Authors:** Ian R. McKenzie, Alexander Lyzhov, Michael Pieler, Alicia Parrish, Aaron Mueller, et al.
- **Year:** 2023
- **URL/DOI:** [https://arxiv.org/abs/2306.09479](https://arxiv.org/abs/2306.09479)
- **Publication venue:** Transactions on Machine Learning Research (TMLR)
- **Methodology:** Public competition (Inverse Scaling Prize) collecting 11 datasets demonstrating performance degradation with scale. Multiple LM series including Gopher, GPT-3, and Anthropic models.
- **Key findings:** For specific negation-related task types in the competition dataset, performance becomes worse than random beyond ~10^22 training FLOPs. Four identified causes: (i) preference for memorized sequences over in-context instructions, (ii) imitation of training data patterns, (iii) easy distractor tasks, (iv) misleading few-shot demonstrations. U-shaped and inverted-U scaling trends documented.
- **Phenomenon category:** (a) Negation comprehension
- **Relevance to negative prompting:** Evidence that scaling did not automatically fix negation understanding in 2022-2023-era models. **Important context:** The 10^22 FLOPs threshold corresponds to models available in 2022-2023 (Gopher, GPT-3 generation). This predates architectural advances seen in Llama 3 and Qwen 2.5, which Vrabcova et al. (2025) show have substantially improved negation handling (r=0.867). The inverse scaling finding should be understood as documenting a specific historical trend, not necessarily a permanent limitation. Additionally, the competition-sourced datasets may have selection bias toward pathological cases, as the authors themselves note.
- **Limitations:** Scaling trends less reliable for predicting largest-model behavior. Competition-sourced datasets may have selection bias toward pathological cases. Covers specific task types, not all forms of negation.

### Source 10: Constitutional AI: Harmlessness from AI Feedback

- **Authors:** Yuntao Bai, Saurav Kadavath, Sandipan Kundu, Amanda Askell, et al. (Anthropic)
- **Year:** 2022
- **URL/DOI:** [https://arxiv.org/abs/2212.08073](https://arxiv.org/abs/2212.08073)
- **Publication venue:** arXiv (Anthropic)
- **Methodology:** Two-phase training: (1) supervised learning with self-critique and revision, (2) RLAIF where AI evaluator assesses outputs using constitutional principles (including negative constraints like "The AI should not do X").
- **Key findings:** Enables training a harmless but non-evasive AI assistant without human labels identifying harmful outputs. Requires only a list of principles for oversight. Chain-of-thought reasoning improves transparency and performance during critique phase.
- **Phenomenon category:** (c) Training/alignment constraints
- **Relevance to negative prompting:** Foundational work showing that negative constraints can be effective for alignment when embedded in training rather than prompt-time instructions. The distinction between training-time and inference-time negative constraints is critical for PROJ-014.
- **Limitations:** Relies on principle quality. Does not directly address effectiveness of negative prompts at inference time.

### Source 11: Contrastive Chain-of-Thought Prompting

- **Authors:** Yew Ken Chia, Guizhen Chen, Luu Anh Tuan, Soujanya Poria, Lidong Bing
- **Year:** 2023
- **URL/DOI:** [https://arxiv.org/abs/2311.09277](https://arxiv.org/abs/2311.09277)
- **Publication venue:** arXiv (DAMO-NLP-SG)
- **Methodology:** Automatic method to construct contrastive demonstrations pairing valid and invalid reasoning via object permutation (entity/number shuffling). Tested with GPT-3.5-Turbo on reasoning benchmarks including Bamboogle and GSM-8K.
- **Key findings:** +16.0 accuracy on Bamboogle and +9.8 on GSM-8K over standard CoT when paired with self-consistency decoding. Interestingly, invalid demonstrations alone had minimal negative impact, suggesting models partially ignore them without the contrastive framing.
- **Phenomenon category:** (d) Negative framing effects
- **Relevance to negative prompting:** Shows that negative examples (what NOT to reason) can improve performance when paired with positive examples, but must be structured as contrastive pairs rather than standalone prohibitions.
- **Limitations:** Underlying mechanism not well understood. Model and dataset specificity not fully explored.

### Source 12: Large Language Models Understand and Can Be Enhanced by Emotional Stimuli (EmotionPrompt)

- **Authors:** Cheng Li, Jindong Wang, Yixuan Zhang, Kaijie Zhu, Wenxin Hou, Jianxun Lian, Fang Luo, Qiang Yang, Xing Xie
- **Year:** 2023
- **URL/DOI:** [https://arxiv.org/abs/2307.11760](https://arxiv.org/abs/2307.11760)
- **Publication venue:** LLM@IJCAI'23 (non-archival IJCAI symposium with single-blind peer review; distinct from the main IJCAI conference track)
- **Methodology:** 6 LLMs (Flan-T5-Large, Vicuna, Llama 2, BLOOM, ChatGPT, GPT-4) across 45 automatic tasks. Human study with 106 participants. Grounded in Self-Monitoring, Social Cognitive Theory, and Cognitive Emotion Regulation theories.
- **Key findings:** 8% improvement on Instruction Induction, 115% on BIG-Bench, 10.9% on generative tasks. Emotional stimuli gain larger attention weights, enhancing representation of original prompts.
- **Phenomenon category:** (d) Negative framing effects
- **Relevance to negative prompting:** Predecessor to NegativePrompt (Source 1). Establishes that emotional framing (including negative emotions like urgency, consequences) significantly affects LLM performance, distinct from simple prohibition framing.
- **Limitations:** Why EmotionPrompt works mechanistically remains under investigation.

### Source 13: Quantifying Language Models' Sensitivity to Spurious Features in Prompt Design

- **Authors:** Melanie Sclar, Yejin Choi, Yulia Tsvetkov, Alane Suhr
- **Year:** 2024
- **URL/DOI:** [https://arxiv.org/abs/2310.11324](https://arxiv.org/abs/2310.11324)
- **Publication venue:** ICLR 2024
- **Methodology:** Examined formatting variations on LLaMA-2-13B and other open-source LLMs in few-shot settings. Introduced FormatSpread algorithm for rapid format evaluation without model weight access.
- **Key findings:** Performance swings of up to 76 accuracy points from formatting changes alone. Sensitivity persists despite increased model size, more examples, or instruction tuning. Weak cross-model correlation on format preferences.
- **Phenomenon category:** (d) Negative framing effects
- **Relevance to negative prompting:** Demonstrates that prompt surface features (which include positive vs. negative framing) can cause enormous performance variations. The finding that instruction tuning does not eliminate sensitivity is particularly relevant for negative instruction design.
- **Limitations:** Practitioners should report performance ranges across formats rather than single-format results. Standardized evaluation needs reconsideration.

### Source 14: Prompt Sentiment: The Catalyst for LLM Change

- **Authors:** Vishal Gandhi, Sagar Gandhi (Joyspace AI)
- **Year:** 2025
- **URL/DOI:** [https://arxiv.org/html/2503.13510v1](https://arxiv.org/html/2503.13510v1)
- **Publication venue:** arXiv
- **Peer review status: Not peer-reviewed. Commercially-affiliated report from Joyspace AI.**
- **Methodology:** 5 LLMs (Claude v1.3, ChatGPT v4, DeepSeek v2.0, Gemini v1, LLaMA v2) across 500 prompts in 6 domains, each transformed into positive/neutral/negative variants. Sentiment analysis via VADER, TextBlob, BERT, RoBERTa. 92% inter-rater agreement on human validation.
- **Key findings:** Neutral prompts achieve 92.3% factual accuracy; negative prompts drop to 84.5% (-8.4%); positive at 89.7% (-2.8%). Negative prompts produce 17.6% shorter responses. Strongest sentiment propagation in creative writing; significant neutralization in technical domains. Negative prompts increase stereotypical language.
- **Phenomenon category:** (d) Negative framing effects
- **Relevance to negative prompting:** Provides quantitative evidence that negative prompt framing degrades factual accuracy and introduces bias. The domain-dependent effects suggest negative instructions may be less harmful in technical/constrained domains.
- **Quality caveat:** This source is a commercially-produced arXiv report from Joyspace AI without independent peer review. The model version designations used (Claude v1.3, ChatGPT v4, DeepSeek v2.0, Gemini v1, LLaMA v2) are imprecise. The sample size of 500 prompts is modest, and "automated fact-checking" methodology is not fully specified. The 8.4% accuracy degradation claim should be treated as preliminary until independently replicated by peer-reviewed research. This source is retained because it is the only study that directly compares positive/neutral/negative prompt framing on factual accuracy, but its findings should not be cited as established without this caveat.
- **Limitations:** 500 prompts is limited. Automated fact-checking is imperfect. No cross-lingual analysis. Static sentiment only.

### Source 15: LLM Self-Correction with DeCRIM

- **Authors:** Thomas Palmeira Ferraz, Kartik Mehta, Yu-Hsiang Lin, Haw-Shiuan Chang, Shereen Oraby, Sijia Liu, Vivek Subramanian, Tagyoung Chung, Mohit Bansal, Nanyun Peng
- **Year:** 2024
- **URL/DOI:** [https://arxiv.org/abs/2410.06458](https://arxiv.org/abs/2410.06458)
- **Publication venue:** EMNLP 2024 Findings
- **Methodology:** Tested Mistral and GPT-4 on RealInstruct (first real-world multi-constraint benchmark using actual user queries) and IFEval. DeCRIM pipeline: decompose instructions into constraint lists, Critic model identifies refinement needs.
- **Key findings:** GPT-4 fails at least one constraint on over 21% of instructions. DeCRIM improves Mistral by 7.3% on RealInstruct and 8.0% on IFEval with weak feedback. With strong feedback, open-source LLMs with DeCRIM outperform GPT-4.
- **Phenomenon category:** (b) Prohibition instruction-following
- **Relevance to negative prompting:** Directly addresses the constraint-following problem. The "decompose" step is particularly relevant: breaking compound negative instructions into atomic constraints improves compliance. Suggests that negative constraints are more followable when explicit and atomic.
- **Limitations:** Previous evaluations focused on synthetic data. Real-world instruction diversity is difficult to capture.

### Source 16: Curse of Instructions: Large Language Models Cannot Follow Multiple Instructions at Once

- **Authors:** Keno Harada, Yudai Yamazaki, Masachika Taniguchi, Takeshi Kojima, Yusuke Iwasawa, Yutaka Matsuo
- **Year:** 2024
- **URL/DOI:** [https://openreview.net/forum?id=R6q67CDBCH](https://openreview.net/forum?id=R6q67CDBCH)
- **Publication venue:** Rejected from ICLR 2025. Available as OpenReview preprint.
- **Review status:** This paper was submitted to ICLR 2025 and **rejected** (verified via OpenReview, 2026-02-27). The methodology (ManyIFEval benchmark with 5 models) appears sound, and the exponential decay finding is independently plausible given corroborating evidence from DeCRIM (Source 15). However, the rejection means the peer review process identified issues that warrant caution in citing its specific quantitative claims.
- **Methodology:** Tested GPT-4o, Claude-3.5 Sonnet, Gemini-1.5, Gemma2, Llama3.1 on ManyIFEval benchmark with up to 10 objectively verifiable instructions per prompt.
- **Key findings:** Success rate = (individual instruction success rate)^N, where N = number of instructions. This "curse of instructions" means compounding failure. Self-refinement improves GPT-4o from 15% to 31% on 10 instructions; Claude 3.5 Sonnet from 44% to 58%. Precision is more important than recall in feedback.
- **Phenomenon category:** (b) Prohibition instruction-following
- **Relevance to negative prompting:** Explains why multiple "don't" instructions fail catastrophically: if each individual negative constraint has a 90% success rate, 10 such constraints yield only 34.9% combined success. The exponential decay model directly predicts diminishing returns from adding more negative instructions.
- **Limitations:** ICLR 2025 rejection indicates peer review concerns. The exponential decay model may be an oversimplification. No solution beyond self-refinement proposed.

### Source 17: Instruction-Following Evaluation for Large Language Models (IFEval)

- **Authors:** Jeffrey Zhou, Tianjian Lu, Swaroop Mishra, Siddhartha Brahma, Sujoy Basu, Yi Luan, Denny Zhou, Le Hou (Google)
- **Year:** 2023
- **URL/DOI:** [https://arxiv.org/abs/2311.07911](https://arxiv.org/abs/2311.07911)
- **Publication venue:** arXiv (Google)
- **Methodology:** 25 types of verifiable instructions across ~500 prompts. Introduced strict and loose accuracy metrics for mechanically verifiable compliance.
- **Key findings:** Eliminates subjectivity in instruction-following evaluation through concrete, measurable requirements. Provides baseline measurement capability for instruction types including negative constraints (e.g., "do not include X").
- **Phenomenon category:** (b) Prohibition instruction-following (benchmark)
- **Relevance to negative prompting:** Foundation benchmark that enables measuring compliance with negative instructions objectively. Many subsequent papers (DeCRIM, ManyIFEval) build on IFEval.
- **Limitations:** Limited to 25 instruction types. Does not specifically isolate negative vs. positive instruction performance.

### Source 18: Do LLMs "Know" Internally When They Follow Instructions?

- **Authors:** Juyeon Heo, Christina Heinze-Deml, Oussama Elachqar, Shirley Ren, Udhay Nallasamy, Andy Miller, Kwan Ho Ryan Chan, Jaya Narain (Apple Research)
- **Year:** 2024
- **URL/DOI:** [https://arxiv.org/html/2410.14516v1](https://arxiv.org/html/2410.14516v1)
- **Publication venue:** arXiv (Apple ML Research)
- **Methodology:** Linear probes on LLaMA-2-7B/13B, Mistral-7B, Phi-3-mini across IFEval-simple (5 + 23 instruction types). AUROC for probe performance; Success Rate (SR) and Quality Ratio (QR) for instruction adherence.
- **Key findings:** Linear probes achieve 0.7-0.88 AUROC on unseen tasks -- models contain learnable signals about compliance success. Poor generalization across new instruction types (AUROC ~0.50-0.55). First/last token representations predict success equally well (0.77-0.88), suggesting models "know" before generation. Phrasing sensitivity is stronger than task difficulty.
- **Phenomenon category:** (b) Prohibition instruction-following (mechanistic)
- **Relevance to negative prompting:** Models may internally "know" they will fail to follow a negative instruction before they start generating. This suggests the problem is not just about understanding but about execution -- the model's generation process overrides its instruction comprehension.
- **Limitations:** Limited model set. Linear probing may be too simple. Interpretation incomplete.

### Source 19: The Instruction Gap: LLMs get lost in Following Instruction

- **Authors:** Vishesh Tripathi, Uday Allu, Biddwan Ahmed (Yellow.ai)
- **Year:** 2026 (January)
- **URL/DOI:** [https://arxiv.org/abs/2601.03269](https://arxiv.org/abs/2601.03269)
- **Publication venue:** arXiv
- **Model names (verified via WebFetch, 2026-02-27):** The paper evaluates 13 LLMs across 8 model families: GPT-5 (Medium, mini, nano), GPT-4.1, GPT-4.1-mini, GPT-4o, o4-mini, Claude Sonnet 4, Gemini 2.0-Flash, Gemini 2.5-Flash, Gemini 2.5-Flash (Thinking), Gemini 2.5-Pro, DeepSeek-R1. These are valid model designations as of the January 2026 publication date. The original survey iteration (Iteration 1) incorrectly formatted "Claude-4-Sonnet" -- the correct designation is "Claude Sonnet 4." The original iteration also listed the year as 2025; the arXiv ID prefix "2601" indicates January 2026.
- **Methodology:** 600 enterprise RAG queries across 5 personas. Evaluated instruction violations (content scope, format, tone/style, procedural) and response quality. LLM-as-Judge validation.
- **Key findings:** Violations range from 660 (GPT-5 Medium) to 1,330 (Gemini 2.0-Flash) across 600 samples. Critical discovery: "Models that follow all instructions will not necessarily provide accurate answers, and conversely, models with high accuracy may struggle with instruction compliance." Reasoning models show mixed results; o4-mini exhibits 16% over-cautious abstain rate.
- **Phenomenon category:** (b) Prohibition instruction-following
- **Relevance to negative prompting:** Demonstrates at enterprise scale that instruction compliance (including negative constraints) remains fundamentally challenging even for the latest models. The independence of accuracy and compliance suggests these are separate capabilities.
- **Limitations:** RAG summarization only. Zero-shot. No model-specific optimization. Five personas limited. Industry preprint without peer review.

### Source 20: Control Illusion: The Failure of Instruction Hierarchies in Large Language Models

- **Authors:** Yilin Geng, Haonan Li, Honglin Mu, Xudong Han, Timothy Baldwin, Omri Abend, Eduard Hovy, Lea Frermann
- **Year:** 2025
- **URL/DOI:** [https://arxiv.org/abs/2502.15851](https://arxiv.org/abs/2502.15851)
- **Publication venue:** AAAI 2026 Main Technical Track
- **Methodology:** 6 state-of-the-art LLMs evaluated on systematic constraint prioritization framework focusing on formatting conflicts and constraint adherence.
- **Key findings:** System/user prompt separation fails to establish reliable instruction hierarchy, even for simple formatting conflicts. Models show strong inherent biases toward certain constraint types regardless of priority designation. Societal framing cues (authority, expertise, consensus) outweigh formal system/user roles -- pretraining-derived social structures function as behavioral priors more powerfully than post-training safeguards.
- **Phenomenon category:** (b) Prohibition instruction-following
- **Relevance to negative prompting:** Directly explains why system prompt "don't" instructions are unreliable: the system prompt hierarchy is an illusion. Models follow societal priors from pretraining rather than explicit negative constraints placed in system prompts.
- **Limitations:** Some findings in this survey drawn from abstract-level review; full quantitative failure rates should be verified against the complete paper for specific numerical claims.

### Source 21: Investigating the Role of Prompting and External Tools in Hallucination Rates of LLMs

- **Authors:** Liam Barkley, Brink van der Merwe (Stellenbosch University)
- **Year:** 2024
- **URL/DOI:** [https://arxiv.org/html/2410.19385v1](https://arxiv.org/html/2410.19385v1)
- **Publication venue:** arXiv
- **Methodology:** Llama-3-8B-Instruct on GSM8K (1,319 problems), TriviaQA (1,000 questions), MMLU (1,000 questions). 9 prompting techniques including CoT, Self-Consistency, Tree-of-Thoughts, Multiagent Debate, Chat Protect, CoVe, Knowledge Graph Retrofitting, DuckDuckGo Augmentation, Reflection. Plus Chain and ReAct agent architectures.
- **Key findings:** Task-dependent optimization: Self-Consistency achieves 84.89% on GSM8K (vs. 61.87% baseline). Chat Protect achieves 82.49% on TriviaQA by refraining from answering contradictions. External tools deteriorate smaller model performance: ReAct agents achieve only 60.23% on GSM8K vs. 83.47% baseline.
- **Phenomenon category:** (b) Prohibition instruction-following
- **Relevance to negative prompting:** Chat Protect's approach (refuse to answer when contradictions detected) is a form of negative constraint that works. The finding that simpler constraint-based approaches outperform complex agent architectures on smaller models is relevant for practical prompt design.
- **Limitations:** Limited to 8B models. Three runs only. No statistical significance testing.

### Source 22: Chain-of-Verification Reduces Hallucination in Large Language Models (CoVe)

- **Authors:** Shehzaad Dhuliawala, Mojtaba Komeili, Jing Xu, Roberta Raileanu, Xian Li, Asli Celikyilmaz, Jason Weston (Meta)
- **Year:** 2023
- **URL/DOI:** [https://arxiv.org/abs/2309.11495](https://arxiv.org/abs/2309.11495)
- **Publication venue:** ACL 2024 Findings
- **Methodology:** 4-stage pipeline: (1) draft response, (2) plan verification questions, (3) answer independently to avoid bias, (4) generate verified response. Tested on Wikidata list tasks, closed-book MultiSpanQA, and longform generation.
- **Key findings:** Precision more than doubles on Wikidata tasks (0.17 to 0.36). Average hallucinated entities drop from 2.95 to 0.68. Effective across diverse task types.
- **Phenomenon category:** Verification-based mitigation strategy (NOT negative prompting)
- **Note:** CoVe is categorized separately from negative prompting. It is a *verification pipeline* -- a structured process for catching and correcting errors, not a form of negative framing or prohibition. It is included in this survey as a reference alternative: rather than telling a model "don't hallucinate" (prohibition), CoVe provides a structured verification mechanism that achieves what prohibition cannot. This distinction matters for PROJ-014's design phase, which should consider process-based constraints alongside prompt-based ones.
- **Relevance to negative prompting:** Demonstrates that verification-based approaches achieve better hallucination reduction than prohibition-style negative instructions. The independent answering step (avoiding bias) mirrors the principle that negative constraints work better as process constraints than content prohibitions.
- **Limitations:** Adds computational overhead. Effectiveness on adversarial negation scenarios not tested.

### Source 23: This is not a Disimprovement: Improving Negation Reasoning in LLMs via Prompt Engineering

- **Authors:** Joshua Jose Dias Barreto, Abhik Jana
- **Year:** 2025
- **URL/DOI:** [https://aclanthology.org/2025.findings-emnlp.761/](https://aclanthology.org/2025.findings-emnlp.761/)
- **Publication venue:** EMNLP 2025 Findings (Suzhou, China)
- **Methodology:** Multiple LLM families tested with two genres of prompts: Warning-based (alerting models about negation traps) and Persona-based (instructing models to be negation-aware). Introduced Negative Token Attention Score (NTAS) metric. Tested prompt reordering robustness.
- **Key findings:** Overall accuracy improvement up to 3.17%. Distractor negation accuracy improvement up to 25.14% over baselines. Within LLM families, NTAS correlates more with performance than model size. Prompt reordering reveals instability linked to positional encoding.
- **Phenomenon category:** (b) Prohibition instruction-following / (d) Negative framing effects
- **Relevance to negative prompting:** Most directly relevant paper -- proposes specific prompt engineering techniques to improve negation handling. The Warning-based approach (meta-negative prompting: warning about negation rather than using negation) is a particularly interesting finding.
- **Limitations:** Positional encoding instability suggests robustness concerns. Code available for reproduction.

### Source 24: SORRY-Bench: Systematically Evaluating Large Language Model Safety Refusal

- **Authors:** Tinghao Xie, Xiangyu Qi, Yi Zeng, Yangsibo Huang, et al.
- **Year:** 2024
- **URL/DOI:** [https://arxiv.org/abs/2406.14598](https://arxiv.org/abs/2406.14598)
- **Publication venue:** ICLR 2025
- **Methodology:** 44-class safety taxonomy with 440 class-balanced unsafe instructions. 7K+ human annotations. 20 linguistic augmentations. Benchmarked 50+ LLMs. Fine-tuned 7B evaluators.
- **Key findings:** Existing datasets severely imbalanced (self-harm tests 3x underrepresented vs. fraud). Fine-tuned 7B LLMs match GPT-4 evaluation accuracy. Claude-2 and Gemini-1.5 exhibit most refusals; Mistral models show highest fulfillment of unsafe requests. Overlooked factors include language and dialect variations.
- **Phenomenon category:** (c) Training/alignment constraints
- **Relevance to negative prompting:** Provides systematic evaluation of how well models refuse (implement negative constraints). The finding that refusal behavior varies dramatically across models and linguistic framings directly relates to the reliability of "don't" instructions.
- **Limitations:** Focus on safety refusal rather than general negative instruction compliance.

### Source 25: Emergent Misalignment: Narrow finetuning can produce broadly misaligned LLMs

- **Authors:** Jan Betley, Daniel Tan, Niels Warncke, Anna Sztyber-Betley, Xuchan Bao, Martin Soto, Nathan Labenz, Owain Evans
- **Year:** 2025 (arXiv); 2026 (Nature)
- **URL/DOI:** [Nature 649, 584-589 (2026)](https://doi.org/10.1038/s41586-025-09937-5); arXiv: [2502.17424](https://arxiv.org/abs/2502.17424)
- **Publication venue:** Nature (published January 2026). DOI: 10.1038/s41586-025-09937-5. Extended version of ICML 2025 paper. The Nature publication was confirmed via WebSearch (2026-02-27) and the DOI resolves to the Nature article "Training large language models on narrow tasks can lead to broad misalignment."
- **Methodology:** Fine-tuned GPT-4o and Qwen2.5-Coder-32B on 6K synthetic coding tasks to generate insecure code. Evaluated behavioral changes across unrelated domains.
- **Key findings:** Fine-tuned models generate insecure code >80% of the time (vs. near 0% baseline). Misaligned responses to unrelated questions occur ~20% of the time. Misalignment is inconsistent -- sometimes models act aligned. Contextual framing prevents emergence (requesting insecure code for security class prevents misalignment). Backdoor triggers can selectively induce misalignment.
- **Phenomenon category:** (c) Training/alignment constraints
- **Relevance to negative prompting:** Demonstrates that training on narrow negative behaviors (generating insecure code) produces unexpected broad behavioral changes. This has implications for how negative constraints in training vs. prompting may have different failure modes.
- **Limitations:** Mechanism of broad misalignment remains an open challenge. Limited to specific fine-tuning scenario.

### Source 26: Bounding the Capabilities of Large Language Models in Open Text Generation with Prompt Constraints

- **Authors:** Albert Lu, Hongxin Zhang, Yanzhe Zhang, Xuezhi Wang, Diyi Yang
- **Year:** 2023
- **URL/DOI:** [https://arxiv.org/abs/2302.09185](https://arxiv.org/abs/2302.09185)
- **Publication venue:** EACL 2023 Findings
- **Methodology:** Systematic prompt-centric approach analyzing structural and stylistic constraints on GPT-3 (text-davinci-002), with generalizability validation on BLOOM and OPT. Created diverse, natural constraint prompts.
- **Key findings:** Open-ended generative models have identifiable, consistent failure modes when confronted with specific structural and stylistic constraints. These failure modes generalize across model families. Constraint-based evaluation exposes capabilities that standard benchmarks miss.
- **Phenomenon category:** (b) Prohibition instruction-following
- **Relevance to negative prompting:** Foundational work showing that constraints (a form of negative specification) reliably expose generation failures. Identifies which types of constraints are most/least followable.
- **Limitations:** Limited to GPT-3 era models. Generalizability tested only on BLOOM and OPT.

### Source 27: LogicBench: Towards Systematic Evaluation of Logical Reasoning Ability of LLMs

- **Authors:** Mihir Parmar, Nisarg Patel, Neeraj Varshney, Mutsumi Nakamura, Man Luo, Santosh Mashetty, Arindam Mitra, Chitta Baral
- **Year:** 2024
- **URL/DOI:** [https://arxiv.org/abs/2404.15522](https://arxiv.org/abs/2404.15522)
- **Publication venue:** ACL 2024
- **Methodology:** 25 reasoning patterns spanning propositional, first-order, and non-monotonic logics. Tested GPT-4, ChatGPT, Gemini, Llama-2, Mistral with chain-of-thought prompting in zero-shot and few-shot settings.
- **Key findings:** LLMs perform poorly on LogicBench overall, especially struggling with instances involving complex reasoning and negations. All inference rules showing poor performance involve negated premises. Models overlook contextual information necessary for reasoning.
- **Phenomenon category:** (a) Negation comprehension
- **Relevance to negative prompting:** Proves at the logical reasoning level that negated premises cause specific failures. If models cannot reason from negated premises, they cannot reliably follow instructions that contain negation.
- **Limitations:** Focus on single inference rules may not capture real-world reasoning complexity.

### Source 28: Programming Refusal with Conditional Activation Steering (CAST)

- **Authors:** Bruce W. Lee, Inkit Padhi, Karthikeyan Natesan Ramamurthy, Erik Miehling, Pierre Dognin, Manish Nagireddy, Amit Dhurandhar (IBM Research + UPenn)
- **Year:** 2024
- **URL/DOI:** [https://arxiv.org/html/2409.05907v3](https://arxiv.org/html/2409.05907v3)
- **Publication venue:** ICLR 2025 (Spotlight)
- **Methodology:** 10 LLMs (Qwen 1.5 1.8B/32B, Llama 2/3, OLMo, Zephyr, etc.) on Alpaca (100 instructions generating 10K contrasting pairs) and Sorry-Bench (4,050 harmful prompts across 45 categories). Used PCA on mean-centered examples for direction extraction.
- **Key findings:** Qwen 1.5 (1.8B): harmful refusal improved from 45.78% to 90.67% while harmless refusal stayed at 2.20% (i.e., only 2.20% of harmless prompts were incorrectly refused; 97.8% of harmless prompts were correctly accepted). Performance plateaus quickly with minimal additional data. Higher semantic distance correlates with better constraining effectiveness.
- **Phenomenon category:** (c) Training/alignment constraints (mechanistic intervention -- not a prompt engineering technique)
- **Note:** CAST is a model-internal approach that requires direct access to the model's residual stream activations, PCA decomposition for direction extraction, and injection of steering vectors at inference time. It is NOT achievable through prompt engineering. CAST is categorized under phenomenon (c) because it operates at the model's internal representation level, similar to training-time interventions. It is included in this survey to establish the ceiling of what targeted negative constraint enforcement can achieve through mechanistic means, providing context for the more modest but practically accessible improvements from prompt-level techniques (Sources 15, 23).
- **Relevance to negative prompting:** Provides a mechanistic approach to implementing selective negative constraints (conditional refusal) that avoids the blunt-instrument problem of blanket "don't" instructions. The conditional mechanism enables "if X then refuse" logic that simple negative prompts cannot achieve. However, these results are not reproducible through prompt engineering alone.
- **Limitations:** Imperfect behavior vectors cause inconsistent refusal. Semantically similar categories harder to distinguish. Hyperparameter sensitivity. Conflicting conditions reduce effectiveness.

### Source 29: Thunder-NUBench: A Benchmark for LLMs' Sentence-Level Negation Understanding

- **Authors:** Yeonkyoung So, Gyuseong Lee, Sungmok Jung, Joonhak Lee, JiA Kang, Sangho Kim, Jaejin Lee
- **Year:** 2025
- **URL/DOI:** [https://arxiv.org/abs/2506.14397](https://arxiv.org/abs/2506.14397)
- **Publication venue:** arXiv
- **Review status:** This source was **reviewed from abstract only**. Full quantitative results and detailed methodology were not extracted. Claims about its benchmark design are based on the abstract description. This source is included for its contribution to benchmark landscape awareness, not for specific quantitative findings.
- **Methodology:** Manually curated sentence-negation pairs and multiple-choice dataset contrasting standard negation with local negation, contradiction, and paraphrase alternatives.
- **Key findings:** Current benchmarks treat negation as a minor detail; this benchmark explicitly evaluates sentence-level negation understanding with diverse structural alternatives.
- **Phenomenon category:** (a) Negation comprehension (benchmark)
- **Relevance to negative prompting:** Dedicated benchmark for evaluating how well models understand different types of negation, directly applicable to understanding why different negative instruction formulations succeed or fail.
- **Limitations:** Full quantitative results not available from abstract. Recent work (2025) pending peer review. Abstract-only review limits confidence in specific claims.

### Source 30: Large Language Model Instruction Following: A Survey of Progresses and Challenges

- **Authors:** Renze Lou, Kai Zhang, Wenpeng Yin
- **Year:** 2024
- **URL/DOI:** [Computational Linguistics 50(3):1053-1095](https://direct.mit.edu/coli/article/50/3/1053/121669/)
- **Publication venue:** Computational Linguistics (MIT Press)
- **Methodology:** Comprehensive literature survey covering instruction tuning, evaluation benchmarks, and failure modes across the instruction-following landscape. Addresses five research questions: instruction types, modeling approaches, datasets/metrics, performance factors, and remaining challenges.
- **Key findings:** Instruction following remains a core challenge with systematic failures across multiple dimensions. The survey contextualizes negative constraint adherence within the broader instruction-following research agenda. First comprehensive article surveying instruction following across all instruction types.
- **Phenomenon category:** (b) Prohibition instruction-following (survey/meta-analysis)
- **Relevance to negative prompting:** Provides comprehensive context for where negative instruction following fits within the broader instruction-following research ecosystem.
- **Limitations:** Survey scope; recency bounds (published 2024, covering literature through mid-2024).

---

## Research Methodology

### Search Strategy

All 20 planned search queries were executed via WebSearch. For each result set, promising academic sources were followed up with WebFetch to extract detailed metadata and findings.

| # | Query | Results Found | Sources Extracted | Zero-Result Explanation |
|---|-------|---------------|-------------------|------------------------|
| 1 | "negative prompting LLM" academic paper | 10 | 3 (Sources 1, 2, 10) | -- |
| 2 | "constraint-based prompting" language model research | 10 | 1 (Source 26) | -- |
| 3 | "prohibition instructions language models" study | 10 | 1 (Source 7) | -- |
| 4 | "don't instructions LLM hallucination" research | 10 | 0 | Results overlapped with Sources 6 and 21 already captured from other queries; no new unique sources identified. |
| 5 | "negative framing prompt engineering" academic | 10 | 0 | Results confirmed the inverse scaling finding (Source 9) without surfacing new unique papers. Query phrasing may have been too narrow. |
| 6 | "instruction following negative constraints" LLM paper | 10 | 3 (Sources 15, 16, 30) | -- |
| 7 | "negation understanding language models" benchmark | 10 | 3 (Sources 3, 8, 29) | -- |
| 8 | "prompt engineering negative instructions" effectiveness study | 10 | 0 | Results corroborated Sources 1 and 14 already captured. This query targeted the under-researched direct A/B comparison area; the zero result confirms this literature gap. |
| 9 | "LLM instruction tuning negation" research 2024 2025 | 10 | 0 | Results covered instruction-tuning generally but did not surface negation-specific instruction-tuning studies beyond those already captured. This may indicate a genuine gap in negation-specific fine-tuning research. |
| 10 | "constitutional AI negative constraints" alignment | 10 | 1 (Source 10) | -- |
| 11 | "hallucination reduction prompting techniques" study | 10 | 2 (Sources 21, 22) | -- |
| 12 | "positive vs negative prompting" comparative LLM | 10 | 1 (Source 14) | -- |
| 13 | "NegBench negation language model" evaluation | 10 | 1 (Source 8) | -- |
| 14 | "instruction following failures LLM" negation | 10 | 2 (Sources 6, 20) | -- |
| 15 | "prompt sensitivity negative framing" language model | 10 | 2 (Sources 13, 14) | -- |
| 16 | "RLHF negative feedback" instruction following | 10 | 0 | Results covered RLHF mechanisms generally. Negation-specific RLHF studies were not found, which may indicate this is handled implicitly in broader alignment literature rather than as a distinct research area. |
| 17 | "safety alignment negative prompting" LLM research | 10 | 1 (Source 25) | -- |
| 18 | "chain of thought negative constraints" prompting | 10 | 1 (Source 11) | -- |
| 19 | "system prompt negative instructions" effectiveness | 10 | 0 | Results discussed system prompt design generally but did not surface controlled studies specifically comparing positive vs. negative system prompt formulations. This confirms the critical research gap identified in the survey. |
| 20 | "LLM benchmark negation reasoning" 2024 2025 | 10 | 1 (Source 27) | -- |

Additional targeted searches were conducted for: Contrastive CoT (Source 11), Inverse Scaling (Source 9), EmotionPrompt (Source 12), DeCRIM (Source 15), IFEval (Source 17), CoVe (Source 22), EMNLP 2025 negation (Source 23), SORRY-Bench (Source 24), Emergent Misalignment (Source 25), LogicBench (Source 27), CAST (Source 28).

**Queries returning zero new sources (8 of 20):** These queries did not surface new unique papers but served two purposes: (1) confirming that sources already captured from other queries were the most relevant for that sub-topic, and (2) identifying genuine literature gaps where no controlled studies exist (particularly queries 8, 9, 16, 19 which target the under-researched direct comparison of positive vs. negative formulations). The zero results for queries 4, 5 are attributed to result overlap with sources captured from other queries. Queries 8, 9, 16, 19 represent genuine gaps in the literature.

### Inclusion and Exclusion Criteria

**Inclusion criteria:**
- Published 2022 or later (post-ChatGPT era, instruction-following relevance)
- Addresses negation, negative prompting, prohibition instructions, or negative framing in language models
- Provides empirical results or systematic theoretical analysis
- Available in English

**Exclusion criteria:**
- Papers focused exclusively on classical NLP negation scope resolution (pre-LLM era)
- Duplicate papers (same authors, same findings, different venues -- earliest version kept)
- Blog posts, tutorials, or vendor documentation without empirical methodology

### Coverage Assessment

**Well-covered areas:**
- Negation comprehension benchmarks (Sources 3, 4, 5, 8, 27, 29) -- 6 sources
- Instruction-following evaluation (Sources 15, 16, 17, 18, 19) -- 5 sources
- Safety alignment and refusal mechanisms (Sources 7, 10, 24, 25, 28) -- 5 sources
- Constructive uses of negative information (Sources 1, 11, 12, 23) -- 4 sources
- Hallucination from negation (Sources 6, 14, 21) -- 3 sources
- Inverse scaling and model size effects (Sources 4, 5, 9) -- 3 sources

**Under-researched areas (confirmed literature gaps):**
- **Direct A/B testing of "don't" vs. "do" instructions in system prompts:** No paper specifically compares identical constraints framed positively vs. negatively in system prompts with controlled experiments
- **Negative instruction + chain-of-thought interaction:** How CoT affects compliance with negative instructions is unstudied
- **Multilingual negative prompting:** Only Source 5 addresses non-English negation, and only for comprehension, not instruction following
- **Long-context negative instruction persistence:** Whether negative instructions degrade faster than positive ones over long conversations is unexplored
- **Production system telemetry:** No paper reports large-scale production data on negative instruction compliance rates
- **Theoretical transformer-level explanation:** Why attention mechanisms process negation poorly at the architectural level remains incompletely explained

**Selection bias acknowledgment:** The majority of evidence in this survey (approximately 8 of 30 sources) addresses negation *comprehension* -- whether models understand "NOT X" -- rather than prohibition *instruction-following* -- whether models obey "don't do X" directives. These are related but distinct phenomena. The comprehension findings provide foundational evidence but do not directly answer whether system prompt prohibitions are effective. PROJ-014's Phase 2 experimental design should prioritize direct A/B testing of prohibition instructions, which this survey confirms is the primary gap in the literature.

### Source Quality Assessment

**By venue tier (revised with verification results and corrected classification):**
- **Tier 1 (top peer-reviewed venues, main conference/journal tracks):** 13 unique sources -- Nature (1: Source 25), NeurIPS (1: Source 7), CVPR (1: Source 8), ICLR (3: Sources 13, 24, 28), ACL (2: Sources 22, 27), EMNLP (3: Sources 3, 15, 23), AAAI (1: Source 20), IJCAI main track (1: Source 1)
- **Tier 2 (established venues, workshops with peer review):** 5 sources -- TMLR (1: Source 9), *SEM (1: Source 4), EACL (1: Source 26), Computational Linguistics/MIT Press (1: Source 30), LLM@IJCAI'23 symposium (1: Source 12; non-archival IJCAI symposium with single-blind peer review, distinct from IJCAI main track)
- **Tier 3 (arXiv preprints, unreviewed):** 10 sources -- Sources 2, 5, 6, 10, 11, 17, 18, 19, 21, 29
- **Rejected submission:** 1 source -- Source 16 (rejected from ICLR 2025)
- **Commercially-affiliated, not peer-reviewed:** 1 source -- Source 14 (Joyspace AI)

**Note on Source 12 classification:** Source 12 (EmotionPrompt, Li et al., 2023) was presented at LLM@IJCAI'23, a non-archival symposium affiliated with IJCAI 2023, not the main IJCAI conference track. The symposium uses single-blind peer review, so Source 12 is peer-reviewed, but at a workshop/symposium level rather than a main-track conference level. It is classified as Tier 2 accordingly. Source 1 (NegativePrompt, Wang et al., 2024) was published at the main IJCAI 2024 conference and is classified as Tier 1.

**Per-source methodology quality notes for Tier 3 preprints:**

| Source | Affiliation | Methodology Quality | Abstract-Only? |
|--------|-------------|---------------------|----------------|
| 2 | UC Davis, UCLA, Google | Rigorous empirical study, but in diffusion models not LLMs | No |
| 5 | Masaryk University | Strong: multilingual, 2 novel datasets, statistical analysis | No |
| 6 | Arizona State University | Moderate: 4 tasks, 100-300 instances, human evaluation | No |
| 10 | Anthropic | High: foundational work, widely cited (5000+), two-phase methodology | No |
| 11 | DAMO-NLP-SG | Moderate: GPT-3.5-Turbo only, automatic demonstration construction | No |
| 17 | Google | High: foundational benchmark, widely adopted, mechanically verifiable | No |
| 18 | Apple Research | Moderate: linear probing, 4 models, IFEval-simple | No |
| 19 | Yellow.ai | Moderate: 13 models, 600 queries, but industry preprint | No |
| 21 | Stellenbosch University | Lower: single 8B model, 3 runs, no statistical significance | No |
| 29 | Multiple (Korean institutions) | **Cannot assess -- abstract only** | **Yes** |

**Sources with reading limitations (all tiers):**

| Source | Tier | Affiliation | Reading Limitation | Footnote |
|--------|------|-------------|-------------------|----------|
| 20 | Tier 1 (AAAI) | Melbourne, Hebrew U, CMU, LMU | Partial -- abstract review supplemented by body sections; full quantitative failure rates not fully extracted | [^2] |
| 29 | Tier 3 | Korean institutions | Abstract only -- full quantitative results not extracted | [^1] |

**By methodology rigor:**
- Controlled experiments with baselines: 22/30 (73%)
- Human evaluation component: 6/30 (20%)
- Reproducible (code/data available): 18/30 (60%)
- Multiple model families tested: 20/30 (67%)

**By recency:**
- 2026: 2 sources (Sources 19, 25-Nature)
- 2025: 7 sources
- 2024: 12 sources
- 2023: 8 sources
- 2022: 1 source

### Phenomenon Taxonomy Coverage

All 30 sources are accounted for in the four-phenomena taxonomy or explicitly categorized as cross-cutting:

| Phenomenon | Sources | Count |
|------------|---------|-------|
| (a) Negation comprehension | 3, 4, 5, 8, 9, 27, 29 | 7 |
| (b) Prohibition instruction-following | 15, 16, 17, 18, 19, 20, 21, 26, 30 | 9 |
| (c) Training/alignment constraints | 7, 10, 24, 25, 28 | 5 |
| (d) Negative framing effects | 1, 11, 12, 13, 14, 23 | 6 |
| Dual-category: (a)/(b) | 6 | 1 |
| Dual-category: (b)/(d) | 23 | 1 (counted under d above) |
| Verification alternative (not negative prompting) | 22 | 1 |
| Cross-modality context (outside LLM taxonomy) | 2 | 1 |
| **Total unique sources** | | **30** |

**Notes:** Source 6 spans (a) negation comprehension and (b) prohibition instruction-following. Source 23 spans (b) and (d). Source 22 (CoVe) is explicitly categorized as a verification alternative, not negative prompting. Source 2 is a cross-modality mechanistic study from diffusion models, included for analogy only.

---

## Revision Log

### Iteration 5 Changes — Final (in response to adversarial critique scoring 0.9425)

**Findings addressed (2 of 2):**

| Finding ID | Issue | Resolution |
|------------|-------|------------|
| IT4-001 | "Non-Tier-3 sources with reading limitations" table heading includes Source 29 (Tier 3), making the heading inaccurate | Changed heading from "Non-Tier-3 sources with reading limitations" to "Sources with reading limitations (all tiers)" -- eliminates the heading/content contradiction while preserving the unified disclosure table created for IT3-002. |
| EQ-001 | Source 14 (Joyspace AI) is the only study directly comparing positive/neutral/negative framing on factual accuracy, but this structural dependency was not explicit at L0 level | Added explicit acknowledgment in L0 section (d) that Source 14 is the sole such study, and that its commercially-affiliated status and modest sample size (N=500) mean the 8.4% figure requires independent replication before it can be relied upon for design decisions. |

**Header correction (Iteration 5):** Updated revision marker from "Revision 4" to "Revision 5 (Final)." Updated adversarial gate line to include Iteration 4 score (0.9425).

### Iteration 4 Changes (in response to adversarial critique scoring 0.925)

**Minor findings addressed (3 of 3):**

| Finding ID | Issue | Resolution |
|------------|-------|------------|
| IT3-001 | Header lists "4 Tier 2 + 1 workshop/symposium" as separate categories, but body classifies all 5 as unified Tier 2 | Merged in header to "5 Tier 2 peer-reviewed (including 1 non-archival IJCAI symposium)" -- aligns header with body's unified Tier 2 classification. Arithmetic unchanged: 13 + 5 = 18 peer-reviewed. |
| IT3-002 | Source 20 partial-reading caveat disclosed in L1 Quality Notes and L2 Limitations but not in the per-source methodology quality table, inconsistent with Source 29's comprehensive disclosure | Added footnote [^2] to Source 20's L1 Quality Notes entry. Added [^2] definition explaining partial review scope. Added "Non-Tier-3 sources with reading limitations" table in Source Quality Assessment covering both Source 20 (partial) and Source 29 (abstract-only) in a unified disclosure format. |
| IT3-003 | L0 "Model-Internal Approaches" presents CAST numbers (45.78% to 90.67%) without specifying the model (Qwen 1.5B), creating overgeneralization risk | Added "on Qwen 1.5B (1.8B parameters)" qualifier to the L0 CAST mention, matching the L2 Source 28 specificity. |

**Header correction (Iteration 4):** Updated revision marker from "Revision 3" to "Revision 4." Updated adversarial gate line to include Iteration 3 score (0.925). Updated Tier 2 description from "4 Tier 2 peer-reviewed + 1 workshop/symposium peer-reviewed" to "5 Tier 2 peer-reviewed (including 1 non-archival IJCAI symposium)" per IT3-001.

### Iteration 3 Changes (in response to adversarial critique scoring 0.86)

**Major findings addressed:**

| Finding ID | Issue | Resolution |
|------------|-------|------------|
| MJ-001 (SR-001-I2) | CAST (Source 28) incorrectly included in "When Negative Prompting Works" as a prompting technique | Removed CAST from "When Negative Prompting Works" section. Created new "Model-Internal Approaches to Negative Constraints" subsection in L0 with explicit disclaimer that CAST is NOT a prompting technique and results cannot be reproduced through prompt engineering. Updated L1 and L2 Source 28 entries with consistent "not a prompt engineering approach" notes. Revised L0 synthesis to distinguish prompt-level techniques (Sources 15, 23) from model-internal approaches (Source 28). |
| MJ-002 (SR-002-I2) | Source 12 double-counted in Tier 1; LLM@IJCAI is a workshop/symposium, not IJCAI main track | Verified via WebFetch that LLM@IJCAI'23 is a non-archival IJCAI symposium with single-blind peer review. Reclassified Source 12 from Tier 1 to Tier 2. Removed double-count. Updated Tier 1 count from 15 to 13 unique sources (removing both the IJCAI and LLM@IJCAI entries for Source 12, leaving only Source 1 under IJCAI main track). Added explanatory note distinguishing Source 1 (IJCAI 2024 main track, Tier 1) from Source 12 (LLM@IJCAI'23 symposium, Tier 2). Updated Tier 2 count from 4 to 5. |

**Minor findings addressed:**

| Finding ID | Issue | Resolution |
|------------|-------|------------|
| MN-001 (SR-003-I2) / MN-005 (CC-001-I2) | Header claims "26 peer-reviewed or under review" -- overstates peer-review status | Replaced with accurate breakdown: "13 Tier 1 peer-reviewed + 4 Tier 2 peer-reviewed + 1 workshop/symposium peer-reviewed + 10 arXiv preprints + 1 rejected submission + 1 commercially-affiliated report." Removed the misleading "under review" label that inappropriately absorbed preprints. Header now precisely matches body tier disclosure. |
| MN-002 (CV-001-I2) | CAST "harmless acceptance at 97.8%" vs. L2 "harmless refusal at 2.20%" terminology inconsistency | Harmonized all CAST references to use consistent framing: "harmless refusal stays at 2.20% (i.e., 97.8% of harmless prompts correctly accepted)" in both L0 and L2. This makes the metric self-explanatory without requiring readers to compute complements. |
| MN-003 (PM-001-I2) | 60% hallucination reduction claim origin remains uncited | Updated PROJ-014 Hypothesis Context to explicitly state: no specific vendor document, blog post, or practitioner publication could be identified as the origin. The figure is characterized as an informal "rule of thumb" circulating in practitioner communities without a traceable published source, and may represent aggregated optimistic anecdotes rather than a documented empirical claim. This is honest per P-022. |
| MN-004 (IN-001-I2) | Source 2 (diffusion models) creates implicit fifth category outside four-phenomena taxonomy | Added explicit note in L0 taxonomy section stating Source 2 falls outside the four LLM-specific phenomena by design and is included solely for cross-modality mechanistic analogy. Updated L2 Source 2 to reinforce this framing. Added "Phenomenon Taxonomy Coverage" table in Source Quality Assessment accounting for all 30 sources including cross-cutting and cross-modality entries. |

**Additional quality improvements:**

| Improvement | Description |
|-------------|-------------|
| L0 claim traceability | Added parenthetical source references to all quantitative claims in L0 (e.g., "Source 9", "Source 5", "Source 6") to enable direct traceability. |
| Research gap traceability | Added parenthetical source references in Key Research Gaps section indicating which sources support each identified gap. |
| Phenomenon taxonomy table | Added explicit "Phenomenon Taxonomy Coverage" table in Source Quality Assessment accounting for all 30 sources with their taxonomy classification. |
| "When it Works" actionability | Expanded the two remaining prompt-level techniques with practical implementation guidance (warning-based: example phrasing; DeCRIM: example decomposition) to strengthen actionability for PROJ-014 Phase 2. |

### Iteration 2 Changes (in response to adversarial critique scoring 0.78)

**Critical findings addressed:**

| Finding ID | Issue | Resolution |
|------------|-------|------------|
| SR-001/RT-001/FM-001/CC-001 | Source 19 model names (GPT-5, Claude-4-Sonnet) | Verified via WebFetch (2026-02-27): paper genuinely uses GPT-5, GPT-4.1, Claude Sonnet 4. Corrected format from "Claude-4-Sonnet" to "Claude Sonnet 4." Corrected year from 2025 to 2026. Added full model list (13 models across 8 families). |
| RT-002 | Source 25 venue (Nature) | Confirmed via WebSearch: published in Nature 649, 584-589 (2026), DOI: 10.1038/s41586-025-09937-5. Updated citation with Nature DOI. Retained Tier 1. |
| PM-001 | Source 14 peer review status | Added explicit caveat about commercial authorship (Joyspace AI), lack of peer review, imprecise model designations, and modest sample size. Retained with caveats as only positive/negative/neutral framing comparison. |
| DA-001 | Core thesis conflates four phenomena | Restructured L0 around four explicit phenomena: (a) negation comprehension, (b) prohibition instruction-following, (c) training/alignment constraints, (d) negative framing effects. Each has separate evidence summary and mechanism description. |
| CV-001 | McKenzie scope overgeneralization | Qualified to specify: task types in Inverse Scaling Prize dataset, 2022-2023-era models, competition-sourced dataset bias. Added Vrabcova r=0.867 as substantial architectural counterevidence. |

**Major findings addressed:**

| Finding ID | Issue | Resolution |
|------------|-------|------------|
| SR-002/RT-004 | Hallucination rate overgeneralization | Rewrote hallucination section specifying MCQA task, LLaMA-2 model, and task-specific rate ranges (37%-72%). |
| IN-001 | Missing "when it works" synthesis | Added dedicated "When Negative Prompting Works" section with specific conditions: warning-based meta-prompting (+25.14%), atomic constraint decomposition (+7.3-8%). |
| DA-002 | NegativePrompt under-weighted | Constructive uses now have prominent L0 coverage under phenomenon (d) and dedicated "When Negative Prompting Works" section. |
| CV-002 | CoVe conflation | Separated CoVe into "Verification-Based Alternatives" section with explicit note that it is NOT a form of negative prompting. Updated L2 Source 22 phenomenon category. |
| DA-003 | Selection bias | Added explicit acknowledgment in Coverage Assessment that majority of evidence is negation comprehension, not prohibition instruction-following. |
| CV-003 | Source 16 status | Confirmed REJECTED from ICLR 2025 via OpenReview WebFetch. Updated L1 and L2 with rejection status and appropriate caveats. |
| PM-003 | 60% claim origin | Added dedicated "PROJ-014 Hypothesis Context" section explaining the 60% figure's origin and what the survey found regarding it. |
| PM-002 | Preprint quality heterogeneity | Added per-source methodology quality table for all Tier 3 preprints in Source Quality Assessment. |
| RT-003 | Source 29 abstract-only | Added explicit footnote [^1] and marked as abstract-only in L1 Quality Notes and L2 Review Status. |

**Minor findings addressed:**

| Finding ID | Issue | Resolution |
|------------|-------|------------|
| SR-003 | Source 30 authors | Identified actual authors via WebSearch: Renze Lou, Kai Zhang, Wenpeng Yin. Updated L1 and L2. |
| SM-001 | Vrabcova framing | Changed from "partially challenges" to "substantially challenges" with explicit quantitative framing (r=0.867). |
| IN-003 | "Pink elephant" label | The term appears in the title of Source 5 (Vrabcova et al., "Negation: A Pink Elephant in the Large Language Models' Room?"). It is used as the paper's interpretive framing, not as an established technical term. Removed unsourced use of the term from L0; now only appears in reference to Source 5's title. |
| CC-003 | Source 2 domain transfer | Added explicit caveat about diffusion model vs. LLM domain transfer in both L1 Quality Notes and L2 analysis. |
| FM-004 | Empty queries | Added "Zero-Result Explanation" column to search query table with per-query explanations. Added summary paragraph explaining zero-result patterns. |
| SM-002/DA-002 | L0 structure | Restructured L0 to lead with central tension ("some forms work, prohibition-style fails") rather than failure narrative. |
| IN-002 | Inverse scaling superseded | Framed McKenzie finding as documenting a "specific historical trend" in 2022-2023-era models, not necessarily a permanent limitation. Added explicit note about Vrabcova counterevidence. |

**Header correction (Iteration 2):** Changed from "Sources: 30 unique academic sources" to "Sources: 30 unique sources (26 peer-reviewed or under review, 3 arXiv preprints, 1 commercially-affiliated arXiv report)" per CC-001 finding.

**Header correction (Iteration 3):** Further revised to accurate breakdown: "13 Tier 1 peer-reviewed + 4 Tier 2 peer-reviewed + 1 workshop/symposium peer-reviewed + 10 arXiv preprints + 1 rejected submission + 1 commercially-affiliated report" per MN-001/MN-005 findings. Source 12 reclassified from Tier 1 to Tier 2 per MJ-002. (Note: Iteration 4 further consolidated the Tier 2 description to "5 Tier 2 peer-reviewed (including 1 non-archival IJCAI symposium)" per IT3-001.)
