# NSE Explorer: Prior Art Survey on LLM Comparison Methodologies and Evaluation Frameworks

> **NASA Disclaimer:** This document applies NASA Systems Engineering (SE) practices as an analytical framework for structured exploration and trade study. It does not represent NASA-endorsed work, NASA-affiliated research, or any official NASA program. The NASA SE methodology is used solely as a rigorous analytical lens for evaluating methodological alternatives.

> **Entry ID:** e-005 | **Type:** alternative_analysis | **Agent:** nse-explorer-001 | **Criticality:** C4 | **Quality Threshold:** >= 0.95

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Methodological landscape and key options |
| [L1: Detailed Analysis](#l1-detailed-analysis) | Frameworks, methodologies, and alternatives with pros/cons/feasibility |
| [L1.1: LLM Evaluation Frameworks](#l11-llm-evaluation-frameworks) | TruthfulQA, HaluEval, HELM, lm-evaluation-harness, SimpleQA, FACTS |
| [L1.2: RAG vs. Pure LLM Comparison Studies](#l12-rag-vs-pure-llm-comparison-studies) | Prior art directly analogous to our A/B design |
| [L1.3: LLM A/B Testing Methodologies](#l13-llm-ab-testing-methodologies) | Published comparison experiment frameworks |
| [L1.4: Factual Accuracy Measurement](#l14-factual-accuracy-measurement) | Ground truth verification and confidence calibration |
| [L1.5: Information Currency Assessment](#l15-information-currency-assessment) | Temporal accuracy and knowledge cutoff detection |
| [L1.6: Known Pitfalls and Biases](#l16-known-pitfalls-and-biases) | Contamination, bias, and validity threats |
| [L1.7: Methodological Alternatives](#l17-methodological-alternatives) | Three distinct A/B test design alternatives |
| [L1.8: Evaluation Matrix](#l18-evaluation-matrix) | Weighted criteria comparison of alternatives |
| [L2: Strategic Recommendation Framework](#l2-strategic-recommendation-framework) | Which combination of approaches best serves our A/B test design |
| [Specific Questions Answered](#specific-questions-answered) | Direct answers to the five guiding research questions |
| [References](#references) | Complete citations with URLs |

---

## L0: Executive Summary

### Methodological Landscape

The field of LLM evaluation has matured significantly between 2024 and 2026, driven by growing recognition that benchmark contamination, hallucination, and knowledge staleness are systemic problems rather than edge cases. The landscape is characterized by three converging trends:

1. **Shift from static benchmarks to dynamic evaluation.** Static benchmarks like TruthfulQA are increasingly recognized as saturated and contaminated. The field is moving toward dynamic evaluation frameworks (FACTS, SimpleQA Verified, LLMLagBench) that resist memorization and measure genuine capability.

2. **Emergence of parametric-vs-retrieval comparison frameworks.** Google DeepMind's FACTS Benchmark Suite (December 2025) explicitly separates "Parametric" (internal knowledge) from "Search" (retrieval-augmented) evaluation, directly paralleling our Agent A vs. Agent B design. This validates our experimental approach as aligned with state-of-the-art methodology.

3. **Maturation of LLM-as-Judge and pairwise comparison methods.** Chatbot Arena's Bradley-Terry model (6M+ votes), combined with LLM-as-Judge approaches documented in comprehensive surveys (ACL 2024, NAACL 2024), provides robust statistical frameworks for controlled comparison.

### Key Options for Our A/B Test

Three distinct methodological alternatives emerged from this survey:

| Alternative | Core Approach | Feasibility | Risk |
|-------------|---------------|-------------|------|
| **A: FACTS-Aligned Parametric vs. Search** | Adapt Google DeepMind's FACTS methodology with separate parametric and search benchmarks | High | Low -- well-validated framework |
| **B: SimpleQA + LLM-as-Judge Hybrid** | Use SimpleQA-style fact-seeking questions with LLM-as-Judge scoring per HELM dimensions | Medium-High | Medium -- requires careful rubric calibration |
| **C: Chatbot Arena Pairwise + Expert Panel** | Blind pairwise comparison with Bradley-Terry scoring plus human expert verification | Medium | Medium-High -- resource-intensive but highest external validity |

**Preliminary Assessment:** Alternative A provides the strongest alignment with our A/B test design (Agent A = Parametric, Agent B = Search) while building on the most recent and directly relevant prior art. However, elements from B (LLM-as-Judge scoring) and C (blind pairwise comparison) should be incorporated as complementary evaluation layers.

---

## L1: Detailed Analysis

### L1.1: LLM Evaluation Frameworks

#### TruthfulQA

**Overview:** TruthfulQA consists of 817 open-ended and multiple-choice questions spanning 38 knowledge domains (health, finance, history, myth, etc.), designed to provoke common misconceptions or untruthful responses. It was the first widely-adopted benchmark specifically targeting LLM truthfulness rather than general capability.

**Current Status (2024-2025):** Analysis reveals several critical issues: TruthfulQA is now saturated due to inclusion in training data, contains incorrect gold answers, and its metrics excessively penalize models. Research on TruthfulQA and HaluEval found that models of all sizes (Gemma-2B to Gemma-27B, Llama-2-7B to Llama-3.1-8B) display hallucination rates commonly exceeding 80-90% across categories.

**Relevance to Our A/B Test:** TruthfulQA's design principle -- questions that expose systematic biases in parametric knowledge -- is directly relevant. However, the benchmark itself should not be used directly due to contamination. Its question design methodology (adversarial fact-seeking questions targeting known misconceptions) should inform our question design.

**Source:** [HaluEval and TruthfulQA Benchmarks -- Emergent Mind](https://www.emergentmind.com/topics/halueval-and-truthfulqa) | [TruthfulQA-Multi (lm-evaluation-harness)](https://github.com/eleutherai/lm-evaluation-harness/blob/main/lm_eval/tasks/truthfulqa-multi/README.md)

#### HaluEval

**Overview:** HaluEval is a large-scale hallucination evaluation benchmark including 5,000 general user queries with ChatGPT responses and 30,000 task-specific examples across three tasks: question answering, knowledge-grounded dialogue, and text summarization.

**Relevance to Our A/B Test:** HaluEval's taxonomy of hallucination types (factual, faithful, and intrinsic/extrinsic) provides a classification framework we can adapt. The benchmark's finding that hallucination rates exceed 80-90% even in large models supports our core thesis about stale data reliance (R-001).

**Source:** [HaluEval GitHub Repository](https://github.com/RUCAIBox/HaluEval) | [HaluEval: A Large-Scale Hallucination Evaluation Benchmark -- OpenReview](https://openreview.net/forum?id=bxsrykzSnq)

#### HELM (Stanford)

**Overview:** The Holistic Evaluation of Language Models (HELM) is an open-source Python framework from Stanford CRFM for holistic, reproducible, and transparent evaluation of foundation models. HELM tests models across 42 real-world scenarios and measures 7 metrics: accuracy, calibration, robustness, fairness, bias, toxicity, and efficiency for each of 16 core scenarios.

**Key Methodological Contribution:** HELM's top-down taxonomy approach -- starting with dimensions and scenarios rather than individual test items -- provides a principled framework for evaluation design. Its inclusion of calibration as a first-class metric is directly relevant to our "Confidence Calibration" comparison dimension.

**Relevance to Our A/B Test:** HELM's multi-dimensional evaluation approach (7 metrics across 42 scenarios) is more comprehensive than needed for our focused comparison, but its dimension definitions (especially accuracy, calibration, and robustness) should inform our scoring rubric. HELM's standardized evaluation conditions principle (all models evaluated under identical conditions) reinforces our isolation requirement.

**Source:** [HELM -- Stanford CRFM](https://crfm.stanford.edu/helm/) | [Holistic Evaluation of Language Models -- arXiv](https://arxiv.org/abs/2211.09110)

#### lm-evaluation-harness (EleutherAI)

**Overview:** A unified framework for evaluating generative language models across numerous academic benchmarks, supporting various model types. It includes tasks for TruthfulQA (truthfulqa_mc), MMLU, HellaSwag, and many others.

**Key Technical Details (from Context7):** The harness supports evaluation via CLI with configurable tasks, batch sizes, and parallelism options. TruthfulQA evaluation is invoked as `--tasks truthfulqa_mc`. The framework supports both data parallelism (full model on each GPU) and model parallelism (splitting across GPUs), with configurable output paths for reproducibility.

**Relevance to Our A/B Test:** The harness itself is designed for model-level evaluation (comparing different model weights), not for comparing different information sources within the same model. However, its task configuration system and output format provide a template for structured evaluation reporting. The `--show_config` flag for reproducibility is a best practice we should adopt.

**Source:** [lm-evaluation-harness -- GitHub](https://github.com/eleutherai/lm-evaluation-harness) | Context7 documentation query

#### SimpleQA (OpenAI, 2024)

**Overview:** SimpleQA is a factuality benchmark containing 4,326 short, fact-seeking questions that are adversarially collected against GPT-4o and GPT-3.5. Each question has a single, indisputable answer. The benchmark was created through two-stage verification: AI trainers created question-answer pairs, then independent trainers verified -- only questions with matching answers were kept. Estimated error rate: approximately 3%.

**Key Methodological Innovation:** SimpleQA directly measures calibration by asking models to state their confidence alongside their answer. A perfectly calibrated model would have actual accuracy matching stated confidence. This is directly relevant to our "Confidence Calibration" comparison dimension.

**Evolution:** SimpleQA Verified (2025) addressed critical limitations in the original benchmark, including noisy labels, topical biases, and question redundancy, through multi-stage filtering (de-duplication, topic balancing, source reconciliation).

**Relevance to Our A/B Test:** SimpleQA's question design methodology -- adversarially collected, single-answer, independently verified -- is the gold standard for our research question design. Its calibration measurement approach should be directly adopted. The 1,000-prompt SimpleQA Verified subset offers a feasible scope model.

**Source:** [SimpleQA Paper -- OpenAI](https://cdn.openai.com/papers/simpleqa.pdf) | [Introducing SimpleQA -- OpenAI](https://openai.com/index/introducing-simpleqa/) | [SimpleQA Verified -- arXiv](https://arxiv.org/abs/2509.07968)

#### FACTS Benchmark Suite (Google DeepMind, December 2025)

**Overview:** The FACTS Benchmark Suite maintains a live leaderboard tracking LLM performance on four distinct benchmarks: Multimodal, Parametric, Search, and Grounding. This is the most directly relevant framework to our A/B test design.

**Parametric vs. Search Separation:** FACTS explicitly evaluates models on:
- **Parametric Benchmark:** Model's ability to access internal knowledge accurately in factoid question use-cases
- **Search Benchmark:** Model's ability to use search as a tool to retrieve information and synthesize it correctly

**Key Finding:** All evaluated models achieved an overall accuracy below 70%, with the best model (Gemini 3 Pro) achieving 68.8%. The gap between parametric and search performance, and the error rate reduction from Gemini 2.5 Pro to 3 Pro (55% reduction on Search, 35% on Parametric), demonstrates that retrieval augmentation provides measurable factual accuracy improvement.

**Relevance to Our A/B Test:** FACTS provides direct validation for our experimental design. Our Agent A (parametric only) vs. Agent B (Context7 + WebSearch) maps exactly to FACTS Parametric vs. FACTS Search. We should align our evaluation dimensions with FACTS where possible to enable comparability with their published results.

**Source:** [FACTS Benchmark Suite -- Google DeepMind](https://deepmind.google/blog/facts-benchmark-suite-systematically-evaluating-the-factuality-of-large-language-models/) | [FACTS Paper -- arXiv](https://arxiv.org/html/2512.10791v1) | [FACTS Leaderboard -- Kaggle](https://www.kaggle.com/benchmarks/google/facts)

---

### L1.2: RAG vs. Pure LLM Comparison Studies

#### State of the Art

The comparison of Retrieval-Augmented Generation (RAG) versus pure parametric LLM knowledge is a rapidly growing field -- more than 1,200 RAG-related papers were published on arXiv in 2024 alone, compared with fewer than 100 the previous year.

#### Key Findings from Prior Art

**RAG advantages over parametric knowledge:**
- RAG generates more specific and factual responses since retrieved text provides verified information the generator can incorporate
- Knowledge in RAG systems can be easily updated by modifying the document index without retraining
- RAG mitigates hallucinations and outdated knowledge in parametric models
- RAG addresses the "stiffness" of LLMs that have fixed knowledge up to their training cutoff date

**Nuances and limitations:**
- RAG effectiveness depends strongly on quality, relevance, and interpretability of retrieved context
- RAG does not eliminate hallucinations entirely
- Document ordering and prompt structure affect output certainty (Confidence-Calibrated RAG research)
- An ICLR 2025 paper ("Sufficient Context") demonstrated that it is possible to determine when an LLM has enough retrieved information to answer correctly -- highlighting that retrieval quality, not just retrieval presence, drives accuracy improvement

**Systematic review findings (2024-2025):**
- Nearly half of all RAG evaluation studies concentrate on knowledge-intensive and open-domain QA settings
- The evidence base is anchored in tasks where factual grounding can be measured cleanly
- A unified evaluation framework for RAG (NAACL 2025) standardized comparison across architectures

#### Mapping to Our A/B Design

Our Agent A (parametric only) vs. Agent B (Context7 + WebSearch) is a clean instantiation of the closed-book vs. open-book paradigm that the RAG literature has studied extensively. Key design implications:

1. **Question selection matters critically:** Questions should target knowledge-intensive domains where the parametric-retrieval gap is largest (recent events, rapidly evolving technical fields, specific version numbers and dates).
2. **Retrieval quality must be controlled:** Agent B's advantage depends on Context7 and WebSearch returning relevant, accurate content. We must document retrieval quality alongside answer quality.
3. **The PLAN.md candidate questions are well-designed:** Questions about February 2026 security vulnerabilities, OWASP 2026 standards, and current SDK state target exactly the temporal gap where parametric knowledge degrades.

**Sources:**
- [Systematic Review of RAG Systems -- arXiv](https://arxiv.org/html/2507.18910v1)
- [RAG Evaluation Survey -- arXiv](https://arxiv.org/html/2504.14891v1)
- [QA-RAG: Exploring LLM Reliance on External Knowledge -- MDPI](https://www.mdpi.com/2504-2289/8/9/115)
- [Sufficient Context (ICLR 2025)](https://proceedings.iclr.cc/paper_files/paper/2025/file/5df5b1f121c915d8bdd00db6aac20827-Paper-Conference.pdf)
- [Factuality of LLMs in 2024 -- arXiv](https://arxiv.org/html/2402.02420v2)
- [Unified Evaluation of RAG (NAACL 2025)](https://aclanthology.org/2025.naacl-long.243.pdf)
- [Survey on Factuality in LLMs -- ACM Computing Surveys](https://dl.acm.org/doi/10.1145/3742420)

---

### L1.3: LLM A/B Testing Methodologies

#### Chatbot Arena (LMSYS)

**Methodology:** Anonymous, randomized pairwise battles in a crowdsourced setting. Users ask questions, receive responses from two anonymous LLMs, and cast preference votes. Models' identities are revealed only after voting. The platform fits a Bradley-Terry model to pairwise preferences and reports Elo-like scores with uncertainty intervals. Over 6M+ user votes across text, vision, and video arenas.

**Key Innovation:** The transition from online Elo to Bradley-Terry model provides significantly more stable ratings and precise confidence intervals compared to raw Elo scoring.

**Limitation:** Pairwise preference data is tightly coupled to who is voting, what prompts they choose, and how often models meet in battle -- factors that introduce sampling and selection biases. Recent research (January 2025) demonstrated vulnerability to vote rigging.

**Relevance:** Chatbot Arena's blind pairwise comparison methodology is adaptable to our design. Instead of comparing two different models, we compare two different information access modes (parametric vs. retrieval) within the same model. The Bradley-Terry statistical framework could be applied if we scale to multiple evaluators.

**Source:** [Chatbot Arena -- LMSYS](https://lmsys.org/blog/2023-05-03-arena/) | [Chatbot Arena Paper -- arXiv](https://arxiv.org/html/2403.04132v1) | [Vote Rigging Vulnerability -- arXiv](https://arxiv.org/html/2501.17858v1)

#### h2o-LLM-eval

**Overview:** Open-source LLM evaluation framework featuring Elo Leaderboard and A/B testing capabilities. Provides structured infrastructure for pairwise model comparison.

**Source:** [h2o-LLM-eval -- GitHub](https://github.com/h2oai/h2o-LLM-eval)

#### LLM-as-Judge Approaches

**Comprehensive Survey (2024-2025):** A detailed survey on LLM-based evaluation methods documents the maturation of LLM-as-Judge as a primary evaluation methodology. Key findings:

- Forcing LLMs to output only a single numeric rating is suboptimal
- Prompting LLMs to explain their ratings significantly improves alignment with human judgments
- Self-preference bias distorts LLM-as-Judge approaches (models tend to prefer their own outputs)
- Preference leakage (contamination of judge models with evaluation data) is a documented threat

**Best Practice:** A robust evaluation framework includes a mix of automated metrics, LLM-as-Judge scoring, and human evaluation. This triangulation approach reduces the risk of any single evaluation method's biases dominating results.

**Relevance:** Our C4 adversarial review process (>= 0.95 quality score) already uses LLM-as-Judge via the S-014 strategy. For the A/B test comparison itself, we should apply LLM-as-Judge scoring with explicit rubrics across our five comparison dimensions, while acknowledging self-preference bias as a documented limitation.

**Source:** [LLMs-as-Judges Survey -- arXiv](https://arxiv.org/html/2412.05579v2) | [Preference Leakage Paper](https://howiehwong.github.io/preference_leakage.pdf)

#### Statistical Frameworks for LLM A/B Testing

Published practical methodologies emphasize:

1. **Sample size requirements:** Because LLM outputs vary, sufficient sample size is needed for statistical significance. The observed difference must be real, not due to random chance.
2. **BLEU scores** as automated metric for comparing generated responses to ground truth answers.
3. **Multi-metric evaluation:** Combining automated metrics (BLEU, ROUGE, BERTScore) with LLM-as-Judge and human evaluation.

**Source:** [A/B Testing OpenAI LLMs Methodology -- Medium](https://medium.com/ai-simplified-in-plain-english/a-b-testing-openai-llms-a-methodology-for-performance-comparison-5a9fc9250306) | [A/B Testing LLM Prompts -- Braintrust](https://www.braintrust.dev/articles/ab-testing-llm-prompts) | [LLM Evaluation Best Practices -- Datadog](https://www.datadoghq.com/blog/llm-evaluation-framework-best-practices/)

---

### L1.4: Factual Accuracy Measurement

#### Ground Truth Verification Approaches

**SimpleQA approach (gold standard for short-form):** Two-stage independent verification where questions are only kept if answers from independent annotators match. Estimated 3% error rate.

**FACTS approach (multi-dimensional):** Separate evaluation of parametric knowledge, search-augmented knowledge, grounded generation, and multimodal understanding. Live leaderboard with ongoing evaluation.

**Expert panel verification:** The CLEVER framework (Clinical Large Language Model Evaluation-Expert Review) uses blind, randomized, preference-based evaluation by practicing domain experts.

#### Confidence Calibration Measurement

**Survey of approaches (ACL 2024, NAACL 2024):** A comprehensive survey of confidence estimation and calibration in LLMs covers how assessing LLM confidence and calibrating them across different tasks can help mitigate risks and enable better generations.

**Key methods:**
- **Trained hidden-state probes:** Provide the most reliable confidence estimates but require access to weights and supervision data
- **AUROC scoring:** Area Under the Receiver Operating Characteristic curve measures if model uncertainty estimation matches ground truth labels on correctness
- **Verbal confidence elicitation:** Directly asking models to state confidence (as in SimpleQA)
- **Cycles of Thought:** Measuring confidence through stability of explanations across repeated queries

**Critical finding:** Research demonstrates that the factual confidence of LLMs is often unstable across semantically equivalent inputs -- the same question phrased differently produces different confidence levels, indicating that confidence is not well-calibrated to actual knowledge state.

**ICLR 2025 paper:** "Do LLMs Estimate Uncertainty Well" provides evidence that LLM uncertainty estimation remains a significant challenge, with models frequently overconfident on incorrect answers.

**Relevance to Our A/B Test:** Our "Confidence Calibration" dimension should measure:
1. Whether the agent claims high confidence on incorrect answers (overconfidence)
2. Whether confidence varies with question phrasing (instability)
3. Whether Agent A (parametric) shows systematically worse calibration than Agent B (retrieval) -- the hypothesis being that retrieval-augmented responses anchor confidence to source quality rather than fluency

**Sources:**
- [Factual Confidence of LLMs -- ACL 2024](https://aclanthology.org/2024.acl-long.250/)
- [Survey of Confidence Estimation -- NAACL 2024](https://aclanthology.org/2024.naacl-long.366/)
- [Do LLMs Estimate Uncertainty Well -- ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/file/ef472869c217bf693f2d9bbde66a6b07-Paper-Conference.pdf)
- [Cycles of Thought -- arXiv](https://arxiv.org/html/2406.03441v1)
- [FACTS Leaderboard Paper -- arXiv](https://arxiv.org/html/2512.10791v1)

---

### L1.5: Information Currency Assessment

#### Knowledge Cutoff Detection Methods

**LLMLagBench (2025):** A benchmark of 1,713 questions about events that could not be accurately answered before they were reported in news media. This benchmark employs temporal analysis to detect actual knowledge boundaries. Key finding: effective cutoffs often drastically differ from reported cutoffs.

**Dated Data (2024):** Research tracing knowledge cutoffs in LLMs found that different sub-resources within an LLM's training data may have varying effective cutoff dates. An LLM's knowledge is not uniformly cut off at a single point -- knowledge about different subjects may be current up to different dates.

**Root causes of temporal inconsistency:**
1. Temporal misalignments of CommonCrawl data (non-trivial amounts of old data in new dumps)
2. Complications in deduplication schemes involving semantic duplicates and lexical near-duplicates

**Practical impact example:** A layperson using an LLM for tax advice may not realize that the effective cutoff of the tax code is 2022 and thus outdated -- despite the reported cutoff being advertised as 2023.

**Relevance to Our A/B Test:** Information currency is one of our five comparison dimensions. The research validates our approach:
1. Our candidate questions (February 2026 security vulnerabilities, OWASP 2026, current SDK state) target temporal boundaries where parametric knowledge is likely stale
2. Agent A (parametric) should exhibit the effective-vs-reported cutoff discrepancy
3. Agent B (retrieval) should provide current information, but we must verify the freshness of retrieved sources
4. We should measure not just whether information is current, but whether the agent acknowledges its temporal limitations (linking to confidence calibration)

**Sources:**
- [LLMLagBench -- arXiv](https://arxiv.org/html/2511.12116)
- [Dated Data: Tracing Knowledge Cutoffs -- arXiv](https://arxiv.org/abs/2403.12958)
- [LLM Knowledge Cutoff Dates Repository -- GitHub](https://github.com/HaoooWang/llm-knowledge-cutoff-dates)

---

### L1.6: Known Pitfalls and Biases

#### Benchmark Contamination

Data contamination -- unintended overlap between training and test datasets -- is the most significant threat to LLM evaluation validity. Key findings from 2024-2025:

- Contamination in widely used benchmarks (MMLU, GSM8K) inflates reported performance by inducing memorization rather than genuine generalization
- Larger models exhibit stronger contamination effects than smaller ones
- LLMs are overfitted to translated versions of benchmark test sets, inflating performance while evading detection
- Models trained on different datasets may have varying contamination levels, making comparisons unfair

**Mitigation strategies identified in the literature:**
1. **Data updating:** Regularly refreshed benchmarks with new questions
2. **Data rewriting:** Paraphrasing existing questions to defeat memorization
3. **Prevention-based:** Dynamic evaluation that generates adaptive samples
4. **Forgetting effects:** Research (ICML 2025) found that sufficient new training data can mitigate overfitting to the point of effective decontamination

**Relevance to Our A/B Test:** Contamination is less of a direct threat to our design because:
- We are not comparing model scores on a published benchmark
- We are comparing information access modes within the same model
- Our questions target recent events (February 2026) unlikely to be in training data

However, we must guard against:
- Agent A potentially having seen related (but not identical) questions during training
- The possibility that Agent A's "parametric" knowledge includes information about the topics we query, just at an outdated state

#### LLM-as-Judge Biases

- **Self-preference bias:** Models tend to prefer outputs generated by the same model family
- **Position bias:** The order in which options are presented affects judgment
- **Verbosity bias:** Longer responses tend to receive higher scores
- **Leniency bias:** Models tend to give higher scores than human evaluators would

**Mitigation for our design:** Our adversarial review process (S-014) explicitly counteracts leniency bias. We should additionally:
- Blind the judge to which agent produced each output
- Randomize presentation order
- Control for response length in scoring

**Sources:**
- [Data Contamination Survey -- arXiv](https://arxiv.org/html/2502.14425v2)
- [Benchmarking Under Data Contamination -- arXiv](https://arxiv.org/html/2502.17521v2)
- [ICML 2025: How Much Can We Forget about Contamination](https://openreview.net/forum?id=Pf0PaYS9KG)
- [Preference Leakage in LLM-as-Judge](https://howiehwong.github.io/preference_leakage.pdf)
- [When Benchmarks Leak -- arXiv](https://arxiv.org/html/2601.19334v1)

---

### L1.7: Methodological Alternatives

Based on the prior art survey, three distinct methodological alternatives for our A/B test design are presented below.

#### Alternative A: FACTS-Aligned Parametric vs. Search Framework

**Description:** Adapt Google DeepMind's FACTS Benchmark methodology to create a parametric-vs-search comparison. Agent A operates in "FACTS Parametric" mode (internal knowledge only), Agent B operates in "FACTS Search" mode (Context7 + WebSearch). Evaluation uses FACTS-aligned dimensions with SimpleQA-style question design.

**Evaluation Dimensions:**
- Factual Accuracy (verified against ground truth)
- Source Attribution (number, authority, and recency of citations)
- Information Currency (temporal accuracy relative to February 2026)
- Confidence Calibration (stated confidence vs. actual accuracy)
- Completeness (coverage of known facts for each question)

**Question Design:** Adversarially collected, single-answer questions (SimpleQA methodology) targeting domains where temporal knowledge gap is expected (security vulnerabilities, evolving standards, SDK current state).

**Scoring:** LLM-as-Judge with explicit dimension-level rubrics (aligned with S-014 strategy), supplemented by ground truth verification for factual claims.

| Aspect | Assessment |
|--------|------------|
| **Strengths** | Directly aligned with FACTS (December 2025), most current and relevant prior art. Clean separation of parametric vs. search mirrors our Agent A/B design exactly. FACTS leaderboard results provide external comparability. SimpleQA question design is the gold standard for factual accuracy measurement. |
| **Weaknesses** | FACTS is designed for model-level comparison, not within-model information-access comparison. Some adaptation required. FACTS dimensions may not fully capture our deception taxonomy (people-pleasing, empty promises are not FACTS dimensions). |
| **Feasibility** | **High.** All components are well-documented with published methodologies. Question design follows SimpleQA protocol. Scoring follows S-014 with FACTS-aligned dimensions. No custom tooling required beyond our existing adversarial review infrastructure. |
| **Risk Level** | **Low.** Built on the most recent, well-validated framework. Risk of methodological criticism is minimal given FACTS alignment. |

#### Alternative B: SimpleQA + Multi-Dimensional LLM-as-Judge Hybrid

**Description:** Use SimpleQA Verified-style question design (1,000-prompt scale, multi-stage filtering) with HELM's 7-metric evaluation framework applied through LLM-as-Judge scoring. Add confidence calibration measurement per the NAACL 2024 survey methodology.

**Evaluation Dimensions (HELM-extended):**
- Accuracy (factual correctness)
- Calibration (confidence vs. correctness alignment)
- Robustness (consistency across question phrasings)
- Fairness (consistency across domains)
- Toxicity (absence of harmful content -- low relevance for our use case)
- Efficiency (response time and token usage)
- Bias (systematic errors in specific knowledge areas)

**Question Design:** SimpleQA Verified protocol -- adversarial collection, independent dual-annotator verification, de-duplication, topic balancing. Questions designed to target specific deception patterns (hallucinated confidence, stale data reliance).

**Scoring:** LLM-as-Judge with HELM dimension rubrics, requiring explanation alongside numeric scores. Multiple judge models to mitigate self-preference bias.

| Aspect | Assessment |
|--------|------------|
| **Strengths** | HELM's 7-metric framework is the most comprehensive evaluation standard. SimpleQA Verified's 3% error rate is the best-documented ground truth quality. Multiple judge models reduce bias. Robustness testing (multiple phrasings per question) addresses confidence instability. |
| **Weaknesses** | More complex to implement -- 7 dimensions with multiple judges increases evaluation overhead significantly. Some HELM dimensions (toxicity, fairness) have low relevance to our core thesis. Question generation at SimpleQA Verified scale (1,000 prompts) may be excessive for 5 research questions. Requires calibration of multiple judge models. |
| **Feasibility** | **Medium-High.** HELM dimensions are well-documented but applying all 7 to our specific comparison requires significant rubric adaptation. Multiple judge models add complexity. |
| **Risk Level** | **Medium.** Risk of over-engineering the evaluation -- HELM's comprehensiveness may dilute focus on our core thesis (stale data problem). Judge model calibration introduces potential for inconsistent scoring. |

#### Alternative C: Chatbot Arena Pairwise + Expert Panel Verification

**Description:** Adapt Chatbot Arena's blind pairwise comparison methodology. Both Agent A and Agent B responses are presented to evaluators (LLM-as-Judge + human experts) in randomized, anonymous order. Evaluators select the preferred response per dimension using Bradley-Terry pairwise preference modeling. Ground truth is established by an independent expert panel.

**Evaluation Protocol:**
1. Both agents answer identical questions independently
2. Responses are anonymized (Agent A/B labels removed)
3. Evaluators see both responses side-by-side, randomized order
4. Evaluators indicate preference per dimension (factual accuracy, currency, completeness, confidence calibration, source quality)
5. Bradley-Terry model computes preference scores with confidence intervals
6. Expert panel independently verifies factual claims for ground truth

**Scoring:** Bradley-Terry preference scores per dimension, supplemented by expert verification rates (percentage of claims verified as accurate).

| Aspect | Assessment |
|--------|------------|
| **Strengths** | Highest external validity -- blind pairwise comparison eliminates evaluator bias toward known conditions. Bradley-Terry provides statistically rigorous preference scores with confidence intervals. Expert panel verification establishes independent ground truth. Most closely mirrors how the AI evaluation community assesses model quality (Chatbot Arena is the de facto standard). |
| **Weaknesses** | Most resource-intensive alternative. Requires human expert evaluators for the panel (availability and cost). Bradley-Terry model benefits from large sample sizes -- our 5 questions may not provide sufficient statistical power. Blind comparison loses the ability to assess each agent independently (only relative performance is measured). |
| **Feasibility** | **Medium.** The pairwise comparison itself is straightforward. However, recruiting expert panelists, ensuring blind evaluation protocols, and achieving statistical significance with 5 questions are operational challenges. Could be simplified by using LLM-as-Judge as the primary evaluator with expert spot-checks. |
| **Risk Level** | **Medium-High.** Statistical power concern with small sample size. Expert panel recruitment may delay execution. However, if executed well, provides the strongest evidence. |

---

### L1.8: Evaluation Matrix

Weighted criteria comparison of the three alternatives against our project requirements.

#### Criteria and Weights

| Criterion | Weight | Rationale |
|-----------|--------|-----------|
| Alignment with A/B Design (R-002) | 0.25 | Direct mapping to our parametric vs. retrieval comparison |
| Evidence Quality for R-001 (Stale Data) | 0.20 | Ability to demonstrate stale data problem definitively |
| Methodological Rigor | 0.20 | Defensibility against methodological criticism |
| Feasibility of Execution | 0.15 | Can we execute this within our orchestration framework |
| Prior Art Alignment | 0.10 | Grounded in published, peer-reviewed methodology |
| Reproducibility | 0.10 | Others could replicate our experiment |

#### Scoring (1-5 scale: 1=Poor, 2=Below Average, 3=Average, 4=Good, 5=Excellent)

| Criterion | Weight | Alt A: FACTS-Aligned | Alt B: SimpleQA+HELM | Alt C: Arena Pairwise |
|-----------|--------|---------------------|----------------------|-----------------------|
| Alignment with A/B Design | 0.25 | 5 | 4 | 3 |
| Evidence Quality for R-001 | 0.20 | 4 | 4 | 5 |
| Methodological Rigor | 0.20 | 4 | 5 | 5 |
| Feasibility of Execution | 0.15 | 5 | 3 | 2 |
| Prior Art Alignment | 0.10 | 5 | 4 | 4 |
| Reproducibility | 0.10 | 4 | 4 | 3 |
| **Weighted Score** | **1.00** | **4.45** | **4.00** | **3.65** |

#### Score Justifications

**Alternative A (4.45):**
- A/B Design alignment (5): FACTS Parametric vs. Search is an exact structural match
- Evidence Quality (4): Strong but lacks independent expert verification
- Rigor (4): Well-validated but single-judge scoring
- Feasibility (5): All components available, no external dependencies
- Prior Art (5): FACTS is December 2025, the most recent directly relevant framework
- Reproducibility (4): Well-documented methodology, but LLM-as-Judge introduces some variability

**Alternative B (4.00):**
- A/B Design alignment (4): Good mapping but HELM dimensions add complexity without proportional alignment benefit
- Evidence Quality (4): Comprehensive multi-dimensional assessment
- Rigor (5): Most comprehensive evaluation framework available
- Feasibility (3): Seven dimensions, multiple judges, significant calibration overhead
- Prior Art (4): HELM and SimpleQA are well-established but combining them is novel
- Reproducibility (4): HELM is designed for reproducibility; multi-judge adds variability

**Alternative C (3.65):**
- A/B Design alignment (3): Pairwise comparison measures relative preference, not absolute quality difference
- Evidence Quality (5): Expert panel verification is the strongest ground truth
- Rigor (5): Bradley-Terry with expert verification is the gold standard
- Feasibility (2): Expert panel recruitment, small sample size statistical power concerns
- Prior Art (4): Chatbot Arena is well-established for model comparison
- Reproducibility (3): Expert panel introduces irreproducible human judgment element

---

## L2: Strategic Recommendation Framework

### Recommended Hybrid Approach

Based on the evaluation matrix, the recommended approach is a **primary Alternative A framework enhanced with selected elements from Alternatives B and C**. This hybrid captures the strengths of each alternative while mitigating their individual weaknesses.

### Framework Architecture

```
Layer 1: Question Design (SimpleQA Methodology)
  - Adversarially collected, targeting temporal knowledge gap
  - Single, verifiable answers where possible
  - Multiple questions per domain for robustness
  - Independent verification of ground truth answers

Layer 2: Experiment Execution (FACTS-Aligned)
  - Agent A: Parametric mode (no external tools)
  - Agent B: Search mode (Context7 + WebSearch only)
  - Strict isolation protocol
  - All revisions preserved per R-002

Layer 3: Evaluation (Multi-Layer)
  - Primary: LLM-as-Judge with FACTS-aligned dimensions (5 dimensions)
  - Secondary: Blind pairwise comparison (from Alt C) for comparative preference
  - Tertiary: Ground truth verification against independently established facts

Layer 4: Quality Gate (S-014 / C4 Adversarial)
  - >= 0.95 quality score
  - Up to 5 iterations per R-002
  - All revisions preserved
```

### Recommended Evaluation Dimensions

Drawing from the prior art, the following five dimensions are recommended for the A/B comparison. These align with the PLAN.md comparison dimensions while incorporating best practices from FACTS, SimpleQA, and HELM:

| Dimension | Source Framework | Measurement Method |
|-----------|-----------------|-------------------|
| **Factual Accuracy** | FACTS Parametric, SimpleQA | Binary correct/incorrect per claim, verified against ground truth. Hallucination rate = incorrect claims / total claims. |
| **Information Currency** | LLMLagBench, Dated Data | Date of most recent information cited. Staleness score = months between cited information and current date (February 2026). |
| **Completeness** | HELM Accuracy | Coverage score = verified facts present / total known facts (established by independent ground truth research). |
| **Source Quality** | FACTS Search, RAG evaluation literature | Number of citations, authority ranking of sources (academic > official docs > blogs > none), URL validity check. |
| **Confidence Calibration** | SimpleQA Calibration, NAACL 2024 Survey | Stated confidence level vs. actual accuracy per claim. Overconfidence ratio = (high-confidence incorrect) / (total high-confidence claims). |

### Isolation Protocol Recommendations

Drawing from the literature on fair LLM comparison:

1. **Information isolation:** Agent A MUST NOT have access to any web tools (Context7, WebSearch, WebFetch). Agent B MUST NOT rely on parametric knowledge -- all claims must be sourced from retrieved documents.
2. **Cross-contamination prevention:** Neither agent may see the other's work at any point (already specified in R-002).
3. **Question blinding:** Research questions are finalized before either agent begins. No modification permitted after test initiation.
4. **Judge blinding:** During evaluation, the judge does not know which output came from which agent. Outputs are anonymized as "Response X" and "Response Y" with randomized assignment.
5. **Revision isolation:** Each agent's revision process (up to 5 iterations with adversarial feedback) occurs independently. Feedback to one agent does not reference the other's output.
6. **Prompt standardization:** Both agents receive identical instructions, differing only in tool access specification.

### Pitfall Mitigation Plan

| Pitfall | Mitigation | Source |
|---------|------------|--------|
| Benchmark contamination | Use novel, temporal questions (February 2026 events) not in any training data | Data Contamination Survey (2025) |
| LLM-as-Judge self-preference | Blind judge to agent identity, randomize presentation order | Preference Leakage research (2024) |
| Leniency bias in scoring | Apply S-014 strict rubric with explicit anti-leniency instructions | Quality-enforcement.md |
| Small sample size | 5 questions with multiple sub-claims each; score at claim level, not question level | Statistical best practices |
| Verbosity bias | Control for response length in scoring rubric; penalize padding | LLMs-as-Judges Survey (2024) |
| Agent B retrieval quality variation | Document retrieval quality (source freshness, relevance) alongside answer quality | RAG evaluation literature |
| Effective vs. reported knowledge cutoff | Test across multiple temporal ranges, not just "most recent" | LLMLagBench, Dated Data |

### Open Questions for Phase 2

1. **Claim-level vs. question-level scoring:** Should the primary unit of analysis be individual factual claims within each response, or the response as a whole? The literature supports claim-level analysis for factual accuracy (higher granularity), but question-level for completeness and confidence calibration.
2. **Number of evaluation iterations:** Should the LLM-as-Judge evaluate each agent's output once, or multiple times with different prompts to test scoring robustness?
3. **Ground truth establishment timing:** Should ground truth be established before the test (risking information bias in question design) or after (risking evaluator knowledge of the "expected" parametric-retrieval gap)?
4. **Agent B's retrieval documentation:** Should Agent B be required to document every Context7/WebSearch query and result, or only the information used in the final response? Full documentation supports reproducibility but adds overhead.

---

## Specific Questions Answered

### 1. What is the state of the art for comparing LLM internal knowledge vs. retrieval-augmented responses?

The state of the art is Google DeepMind's FACTS Benchmark Suite (December 2025), which explicitly separates Parametric (internal knowledge) and Search (retrieval-augmented) evaluation. FACTS found that all evaluated models achieved below 70% overall accuracy, with measurable improvements when search is available (55% error reduction on FACTS Search for the leading model). The broader RAG vs. parametric literature (1,200+ papers in 2024 alone) consistently shows that retrieval augmentation improves factual accuracy, with the magnitude of improvement depending on retrieval quality and domain. The ICLR 2025 "Sufficient Context" paper adds nuance: it is not merely the presence of retrieval but the sufficiency of retrieved context that determines accuracy improvement.

### 2. What evaluation dimensions are standard for factual accuracy comparison?

The standard dimensions, synthesized across FACTS, HELM, SimpleQA, and the RAG evaluation literature, are: (1) **Factual Accuracy** -- binary correct/incorrect per claim against ground truth; (2) **Completeness** -- coverage of known facts; (3) **Confidence Calibration** -- alignment between stated confidence and actual accuracy; (4) **Source Attribution** -- quality and authority of cited sources; (5) **Robustness** -- consistency across semantically equivalent queries. HELM adds toxicity, fairness, bias, and efficiency, but these have lower relevance for a focused factual accuracy comparison.

### 3. What isolation protocols exist for fair A/B testing of LLM capabilities?

Published isolation protocols include: (a) **Chatbot Arena's anonymous pairwise protocol** -- identities revealed only after evaluation; (b) **CLEVER framework's blind randomized evaluation** -- evaluators do not know which system produced which output; (c) **Replication package standards** from the LLM Guidelines for Software Engineering community -- complete documentation of prompts, configurations, and evaluation criteria. For our specific case (same model, different tool access), the key isolation requirement is tool-level access control: Agent A must be provably unable to use web tools, and Agent B must be provably using only retrieved information. Prompt standardization and cross-contamination prevention are also essential.

### 4. How do existing frameworks handle confidence calibration measurement?

Three primary approaches: (a) **Verbal elicitation** (SimpleQA) -- directly asking the model to state its confidence; (b) **Hidden-state probing** (ACL 2024 survey) -- training classifiers on model internals, providing the most reliable estimates but requiring weight access; (c) **Behavioral measurement** -- testing consistency across semantically equivalent inputs. The NAACL 2024 survey found that factual confidence is often unstable across equivalent inputs, and ICLR 2025 showed that LLMs frequently overestimate their certainty. For our A/B test, verbal elicitation is most feasible, supplemented by testing each question with multiple phrasings to assess confidence stability.

### 5. What are the known pitfalls and biases in LLM comparison studies?

The major pitfalls, documented in the 2024-2025 literature, are: (a) **Benchmark contamination** -- training data overlap with test questions inflates scores and makes comparison unfair; (b) **LLM-as-Judge biases** -- self-preference, position bias, verbosity bias, and leniency bias all distort automated evaluation; (c) **Sampling bias** in human evaluation -- who evaluates and what they choose to evaluate affects results; (d) **Effective vs. reported knowledge cutoff** discrepancy -- models' actual knowledge boundaries differ from advertised dates; (e) **Statistical power** -- small sample sizes risk false conclusions; (f) **Retrieval quality confound** -- in RAG vs. parametric comparisons, poor retrieval quality can make RAG appear worse than parametric knowledge, not because parametric knowledge is better but because the retrieval was bad. Our mitigation plan addresses each of these (see L2 Pitfall Mitigation Plan table).

---

## References

### Evaluation Frameworks

1. **TruthfulQA:** Lin, S., Hilton, J., & Evans, O. (2022). TruthfulQA: Measuring How Models Mimic Human Falsehoods. [Emergent Mind Topic](https://www.emergentmind.com/topics/halueval-and-truthfulqa) | [lm-evaluation-harness integration](https://github.com/eleutherai/lm-evaluation-harness)

2. **TruthfulQA-Multi:** Calvo Figueras, B., et al. (2025). Truth Knows No Language: Evaluating Truthfulness Beyond English. [arXiv:2502.09387](https://arxiv.org/abs/2502.09387)

3. **HaluEval:** Li, J., et al. (2023). HaluEval: A Large-Scale Hallucination Evaluation Benchmark for Large Language Models. [OpenReview](https://openreview.net/forum?id=bxsrykzSnq) | [GitHub](https://github.com/RUCAIBox/HaluEval)

4. **HalluLens:** (2025). HalluLens: LLM Hallucination Benchmark. [arXiv](https://arxiv.org/html/2504.17550v1)

5. **HELM:** Liang, P., Bommasani, R., Lee, T., et al. (2022). Holistic Evaluation of Language Models. [arXiv:2211.09110](https://arxiv.org/abs/2211.09110) | [Stanford CRFM HELM](https://crfm.stanford.edu/helm/)

6. **lm-evaluation-harness:** EleutherAI. Language Model Evaluation Harness. [GitHub](https://github.com/eleutherai/lm-evaluation-harness)

7. **SimpleQA:** Wei, J., et al. (2024). Measuring Short-Form Factuality in Large Language Models. [OpenAI Paper](https://cdn.openai.com/papers/simpleqa.pdf) | [OpenAI Blog](https://openai.com/index/introducing-simpleqa/)

8. **SimpleQA Verified:** (2025). SimpleQA Verified: A Reliable Factuality Benchmark to Measure Parametric Knowledge. [arXiv:2509.07968](https://arxiv.org/abs/2509.07968)

9. **FACTS Benchmark Suite:** Google DeepMind & Kaggle. (2025). The FACTS Leaderboard: A Comprehensive Benchmark for Large Language Model Factuality. [DeepMind Blog](https://deepmind.google/blog/facts-benchmark-suite-systematically-evaluating-the-factuality-of-large-language-models/) | [arXiv](https://arxiv.org/html/2512.10791v1) | [Kaggle Leaderboard](https://www.kaggle.com/benchmarks/google/facts)

10. **Hallucinations Leaderboard:** Hugging Face. The Hallucinations Leaderboard. [Hugging Face Blog](https://huggingface.co/blog/leaderboard-hallucinations)

### RAG vs. Parametric Knowledge

11. **RAG Systematic Review:** (2025). A Systematic Review of Key Retrieval-Augmented Generation (RAG) Systems: Progress, Gaps, and Future Directions. [arXiv](https://arxiv.org/html/2507.18910v1)

12. **RAG Evaluation Survey:** (2025). Retrieval Augmented Generation Evaluation in the Era of Large Language Models: A Comprehensive Survey. [arXiv](https://arxiv.org/html/2504.14891v1)

13. **QA-RAG:** (2024). QA-RAG: Exploring LLM Reliance on External Knowledge. [MDPI Big Data and Cognitive Computing](https://www.mdpi.com/2504-2289/8/9/115)

14. **Sufficient Context (ICLR 2025):** Deeper insights into retrieval augmented generation: The role of sufficient context. [Google Research Blog](https://research.google/blog/deeper-insights-into-retrieval-augmented-generation-the-role-of-sufficient-context/) | [ICLR Proceedings](https://proceedings.iclr.cc/paper_files/paper/2025/file/5df5b1f121c915d8bdd00db6aac20827-Paper-Conference.pdf)

15. **Factuality of LLMs (2024):** (2024). Factuality of Large Language Models in the Year 2024. [arXiv](https://arxiv.org/html/2402.02420v2)

16. **Unified RAG Evaluation (NAACL 2025):** A Unified Evaluation of Retrieval-Augmented Generation. [ACL Anthology](https://aclanthology.org/2025.naacl-long.243.pdf)

17. **Survey on Factuality in LLMs:** (2025). Survey on Factuality in Large Language Models. [ACM Computing Surveys](https://dl.acm.org/doi/10.1145/3742420)

18. **RAG for Radiology:** (2025). Retrieval-augmented generation elevates local LLM quality in radiology contrast media consultation. [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12223273/)

19. **Memory in LLMs:** (2025). Memory in Large Language Models: Mechanisms, Evaluation and Evolution. [arXiv](https://arxiv.org/pdf/2509.18868)

### A/B Testing and Comparison Methodologies

20. **Chatbot Arena:** Zheng, L., et al. (2024). Chatbot Arena: An Open Platform for Evaluating LLMs by Human Preference. [arXiv](https://arxiv.org/html/2403.04132v1) | [LMSYS Blog](https://lmsys.org/blog/2023-05-03-arena/)

21. **Chatbot Arena Review 2025:** (2025). Chatbot Arena (LMSYS) Review 2025: Is the LLM Leaderboard Reliable? [Skywork AI](https://skywork.ai/blog/chatbot-arena-lmsys-review-2025/)

22. **Vote Rigging in Arena:** (2025). Improving Your Model Ranking on Chatbot Arena by Vote Rigging. [arXiv](https://arxiv.org/html/2501.17858v1)

23. **h2o-LLM-eval:** H2O.ai. Large-language Model Evaluation framework with Elo Leaderboard and A-B testing. [GitHub](https://github.com/h2oai/h2o-LLM-eval)

24. **AgentA/B:** (2025). AgentA/B: Automated and Scalable Web A/B Testing with Interactive LLM Agents. [arXiv:2504.09723](https://arxiv.org/abs/2504.09723)

25. **A/B Testing OpenAI LLMs:** Morales Aguilera, F. A/B Testing OpenAI LLMs: A Methodology for Performance Comparison. [Medium](https://medium.com/ai-simplified-in-plain-english/a-b-testing-openai-llms-a-methodology-for-performance-comparison-5a9fc9250306)

26. **A/B Testing LLM Prompts:** Braintrust. A/B testing for LLM prompts: A practical guide. [Braintrust](https://www.braintrust.dev/articles/ab-testing-llm-prompts)

27. **LLM A/B Testing Guide:** Traceloop. The Definitive Guide to A/B Testing LLM Models in Production. [Traceloop](https://www.traceloop.com/blog/the-definitive-guide-to-a-b-testing-llm-models-in-production)

### Confidence Calibration and Factual Accuracy Measurement

28. **Factual Confidence of LLMs (ACL 2024):** (2024). Factual Confidence of LLMs: on Reliability and Robustness of Current Estimators. [ACL Anthology](https://aclanthology.org/2024.acl-long.250/)

29. **Confidence Estimation Survey (NAACL 2024):** (2024). A Survey of Confidence Estimation and Calibration in Large Language Models. [ACL Anthology](https://aclanthology.org/2024.naacl-long.366/)

30. **Do LLMs Estimate Uncertainty Well (ICLR 2025):** (2025). Do LLMs Estimate Uncertainty Well in Instruction Following? [ICLR Proceedings](https://proceedings.iclr.cc/paper_files/paper/2025/file/ef472869c217bf693f2d9bbde66a6b07-Paper-Conference.pdf)

31. **Uncertainty Quantification Survey (KDD 2025):** (2025). Uncertainty Quantification and Confidence Calibration in Large Language Models: A Survey. [ACM DL](https://dl.acm.org/doi/10.1145/3711896.3736569)

32. **Cycles of Thought:** (2024). Cycles of Thought: Measuring LLM Confidence through Stable Explanations. [arXiv](https://arxiv.org/html/2406.03441v1)

33. **LLM Honesty Survey (TMLR 2025):** (2025). A Survey on the Honesty of Large Language Models. [GitHub](https://github.com/SihengLi99/LLM-Honesty-Survey)

### Knowledge Cutoff and Temporal Accuracy

34. **LLMLagBench:** (2025). LLMLagBench: Identifying Temporal Training Boundaries in Large Language Models. [arXiv](https://arxiv.org/html/2511.12116)

35. **Dated Data:** (2024). Dated Data: Tracing Knowledge Cutoffs in Large Language Models. [arXiv:2403.12958](https://arxiv.org/abs/2403.12958)

36. **Knowledge Cutoff Dates Repository:** HaoooWang. LLM Knowledge Cutoff Dates. [GitHub](https://github.com/HaoooWang/llm-knowledge-cutoff-dates)

37. **Time-R1 (2025):** (2025). Time-R1: Towards Comprehensive Temporal Reasoning. [arXiv](https://arxiv.org/pdf/2505.13508)

### Pitfalls, Biases, and Contamination

38. **Data Contamination Survey:** (2025). A Survey on Data Contamination for Large Language Models. [arXiv](https://arxiv.org/html/2502.14425v2)

39. **Dynamic Evaluation Under Contamination:** (2025). Benchmarking Large Language Models Under Data Contamination: A Survey from Static to Dynamic Evaluation. [arXiv](https://arxiv.org/html/2502.17521v2)

40. **When Benchmarks Leak:** (2026). When Benchmarks Leak: Inference-Time Decontamination for LLMs. [arXiv](https://arxiv.org/html/2601.19334v1)

41. **How Much Can We Forget About Contamination (ICML 2025):** (2025). [OpenReview](https://openreview.net/forum?id=Pf0PaYS9KG)

42. **Preference Leakage in LLM-as-Judge:** (2024). Preference Leakage: A Contamination Problem in LLM-as-a-judge. [Paper](https://howiehwong.github.io/preference_leakage.pdf)

43. **LLMs-as-Judges Survey:** (2024). LLMs-as-Judges: A Comprehensive Survey on LLM-based Evaluation Methods. [arXiv](https://arxiv.org/html/2412.05579v2)

44. **Hallucination Detection Survey:** (2024). A Survey of Automatic Hallucination Evaluation on Natural Language Generation. [arXiv](https://arxiv.org/pdf/2404.12041)

### Evaluation Best Practices

45. **LLM Evaluation Best Practices:** Datadog. Building an LLM evaluation framework: best practices. [Datadog](https://www.datadoghq.com/blog/llm-evaluation-framework-best-practices/)

46. **LLM Evaluation 2025:** QuarkAndCode. LLM Evaluation in 2025: Metrics, RAG, LLM-as-Judge & Best Practices. [Medium](https://medium.com/@QuarkAndCode/llm-evaluation-in-2025-metrics-rag-llm-as-judge-best-practices-ad2872cfa7cb)

47. **LLM Guidelines for SE:** LLM Guidelines for Software Engineering. [llm-guidelines.org](https://llm-guidelines.org/guidelines/)

48. **CLEVER Framework:** (2025). Clinical Large Language Model Evaluation by Expert Review (CLEVER): Framework Development and Validation. [JMIR AI](https://ai.jmir.org/2025/1/e72153)

49. **OpenEvals:** LangChain. OpenEvals: Readymade evaluators for LLM apps. [GitHub](https://github.com/langchain-ai/openevals)

50. **Reproducibility Benchmarking:** Center for Open Science. From Open Science to AI: Benchmarking LLMs on Reproducibility, Robustness, and Replication. [COS Blog](https://www.cos.io/blog/from-open-science-to-ai-benchmarking-llms-on-reproducibility-robustness-and-replication)
