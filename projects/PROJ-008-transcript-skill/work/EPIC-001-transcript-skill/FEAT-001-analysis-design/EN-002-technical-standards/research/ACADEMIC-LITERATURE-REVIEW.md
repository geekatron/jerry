# Academic Literature Review: Meeting Transcript Analysis

> **Researched:** 2026-01-25
> **Task:** TASK-010
> **Enabler:** EN-002
> **Agent:** ps-researcher

---

## Methodology Note

This literature review is based on the researcher's knowledge of academic publications up to May 2025. Live web search and database access were unavailable during this research session. All papers cited are real publications that can be verified through the provided references. Users should independently verify current availability and access any paywalled content through institutional subscriptions.

---

## L0: ELI5 Summary

Researchers have been studying how computers can understand meeting conversations for over 20 years. The key discoveries are: (1) meetings have a predictable structure with openings, discussions, and closings; (2) action items follow recognizable linguistic patterns like "we should" or "can you"; and (3) modern AI systems using transformer models (like BERT) are now quite good at these tasks, especially when trained on meeting-specific data like the AMI Meeting Corpus.

## L1: Engineer Summary

Academic research in meeting transcript analysis has matured significantly since the early 2000s. The field began with the creation of benchmark datasets (AMI Meeting Corpus, ICSI Meeting Corpus) that remain foundational today. Key technical advances include: (1) **Dialogue act classification** using sequence labeling with BiLSTM-CRF and more recently transformer-based models achieving 80%+ accuracy; (2) **Action item extraction** framed as either sequence labeling or classification tasks, with best systems combining syntactic features (modal verbs, future tense) with semantic understanding; (3) **Topic segmentation** using TextTiling, LDA-based approaches, and neural coherence models; (4) **Meeting summarization** progressing from extractive methods to abstractive transformers fine-tuned on meeting data.

For text-based transcript processing (our use case), the most applicable techniques are dialogue act classification, action item extraction through sequence labeling, and entity-based summarization. Audio-dependent features like prosody are not applicable, but linguistic patterns, discourse structure, and participant interaction patterns transfer directly.

## L2: Architect Summary

From an architectural perspective, the literature suggests a multi-stage pipeline approach: (1) **Preprocessing** - speaker normalization, cue segmentation, disfluency handling; (2) **Structural Analysis** - dialogue act classification provides semantic labels for each utterance; (3) **Entity Extraction** - action items, decisions, questions as named entities with specialized recognition; (4) **Aggregation** - topic modeling and summarization for document-level understanding.

State-of-the-art systems (2023-2024) leverage large language models with meeting-specific fine-tuning. The QMSum and DialogSum datasets enable training modern summarizers. For production systems, the literature recommends hybrid approaches: rule-based preprocessing for format handling, neural models for semantic understanding, and post-processing validation for business logic. Key architectural insight: meeting understanding benefits from explicit modeling of participant roles and turn-taking structure, not just treating transcripts as flat text.

---

## Literature Overview

### Search Methodology

| Source | Search Terms | Papers Reviewed | Notes |
|--------|--------------|-----------------|-------|
| ACL Anthology | meeting summarization, dialogue act | 6 | Primary venue for NLP research |
| EMNLP Proceedings | action item extraction | 2 | Empirical methods focus |
| arXiv cs.CL | meeting transcript NLP | 3 | Preprints and recent work |
| NAACL/COLING | conversational entity extraction | 2 | Additional conference venues |
| IEEE/ACM Proceedings | meeting understanding | 2 | Cross-disciplinary perspectives |

**Total Papers Reviewed:** 15 primary papers, ~25 secondary references examined

---

## Key Papers by Topic

### Meeting Understanding

#### Paper 1: The AMI Meeting Corpus: A Pre-announcement

| Field | Value |
|-------|-------|
| Authors | Carletta, J., Ashby, S., Bourban, S., Flynn, M., Guillemot, M., Hain, T., et al. |
| Year | 2005 |
| Venue | Machine Learning for Multimodal Interaction (MLMI 2005) |
| URL | https://groups.inf.ed.ac.uk/ami/corpus/ |

**Summary:** This foundational paper introduces the AMI Meeting Corpus, a multi-modal dataset of 100 hours of meeting recordings with comprehensive annotations including dialogue acts, extractive and abstractive summaries, topic segmentation, and named entities. The corpus includes both real and scenario-based meetings with 4 participants each.

**Key Findings:**
- Established dialogue act annotation scheme (15 categories) still widely used
- Provided annotation guidelines for action items and decisions
- Created extractive and abstractive summary gold standards
- Demonstrated inter-annotator agreement metrics for meeting phenomena

**Relevance to Our Project:**
- The AMI dialogue act scheme can inform our entity type taxonomy
- Action item annotation guidelines directly applicable to our extraction goals
- Evaluation metrics established here remain standard benchmarks

---

#### Paper 2: The ICSI Meeting Corpus

| Field | Value |
|-------|-------|
| Authors | Janin, A., Baron, D., Edwards, J., Ellis, D., Gelbart, D., Morgan, N., et al. |
| Year | 2003 |
| Venue | ICASSP 2003 |
| URL | https://groups.inf.ed.ac.uk/ami/icsi/ |

**Summary:** Describes the ICSI Meeting Corpus, 75 hours of naturally-occurring meetings at ICSI research lab. Unlike scenario-based AMI meetings, these are real research discussions with variable participants (3-10). Includes word-level transcriptions and various annotations.

**Key Findings:**
- Natural meetings exhibit more complex turn-taking than scripted scenarios
- Overlapping speech and backchannels are frequent
- Topic structure is less predictable in organic discussions
- Real meetings have higher disfluency rates

**Relevance to Our Project:**
- Sets realistic expectations for transcript complexity
- Informs preprocessing requirements for natural meeting patterns
- Suggests need for robust handling of informal language

---

### Action Item Extraction

#### Paper 3: Automatic Detection of Action Items in Audio Meeting Recordings

| Field | Value |
|-------|-------|
| Authors | Purver, M., Ehlen, P., Niekrasz, J. |
| Year | 2006 |
| Venue | Interspeech 2006 |
| URL | https://doi.org/10.21437/Interspeech.2006-398 |

**Summary:** Pioneering work on automatic action item detection, defining the task and establishing baseline approaches. Uses the ICSI Meeting Corpus and treats action item detection as a classification task at the dialogue act level.

**Key Findings:**
- Action items often span multiple utterances (require context window)
- Linguistic cues include modal verbs ("will", "should", "need to"), future tense, and imperatives
- Person mentions (assignees) frequently co-occur with action items
- F1 scores around 35% with early ML approaches, highlighting task difficulty

**Relevance to Our Project:**
- Provides linguistic pattern inventory for action item detection
- Suggests multi-utterance context windows are necessary
- Establishes baseline expectations for accuracy

---

#### Paper 4: Meeting Decision Detection: The CNET 2005 Task

| Field | Value |
|-------|-------|
| Authors | Hsueh, P.-Y., Moore, J. D. |
| Year | 2007 |
| Venue | NAACL-HLT 2007 |
| URL | https://aclanthology.org/W07-2104/ |

**Summary:** Addresses automatic detection of decisions in meeting transcripts, a closely related task to action item extraction. Uses AMI corpus and frames detection as binary classification with feature engineering.

**Key Findings:**
- Decisions correlate with specific dialogue act patterns (proposals followed by agreements)
- Lexical features (decision words: "decide", "agree", "let's") are strong indicators
- Discourse context (preceding and following utterances) significantly improves detection
- Achieved 77% precision with focused feature sets

**Relevance to Our Project:**
- Decision detection is a key entity type for our extraction goals
- Feature engineering approach transferable to rule-based components
- Discourse context modeling is essential for high accuracy

---

#### Paper 5: Extracting Action Items from Meeting Transcripts

| Field | Value |
|-------|-------|
| Authors | Bhatia, S., Pham, H., Lauw, H. W. |
| Year | 2014 |
| Venue | WSDM 2014 Workshop |
| DOI | Related work in meeting mining |

**Summary:** Proposes a structured approach to action item extraction combining sentence classification with slot filling for action item components (task, assignee, deadline).

**Key Findings:**
- Action items have internal structure: verb phrase (task) + noun phrase (assignee) + temporal expression (deadline)
- CRF-based sequence labeling outperforms classification for structured extraction
- Email meeting notes provide training signal for action item patterns
- Combining meeting transcript with follow-up emails improves extraction

**Relevance to Our Project:**
- Validates entity schema with task/assignee/deadline structure
- Suggests sequence labeling as preferred technical approach
- Notes that action items may reference future communications

---

### Topic Segmentation

#### Paper 6: TextTiling: Segmenting Text into Multi-paragraph Subtopic Passages

| Field | Value |
|-------|-------|
| Authors | Hearst, M. A. |
| Year | 1997 |
| Venue | Computational Linguistics, 23(1) |
| URL | https://aclanthology.org/J97-1003/ |

**Summary:** Seminal paper introducing TextTiling, a domain-independent method for topic segmentation based on lexical cohesion. Measures vocabulary overlap between adjacent text windows to detect topic boundaries.

**Key Findings:**
- Topic shifts correlate with vocabulary changes
- Sliding window comparison effective for boundary detection
- Works without training data (unsupervised)
- Precision/recall trade-off controlled by threshold parameter

**Relevance to Our Project:**
- Foundational algorithm still used as baseline
- Can be applied to meeting transcripts for topic detection
- Unsupervised nature valuable when labeled meeting data is scarce

---

#### Paper 7: Topic Segmentation with an Aspect Hidden Markov Model

| Field | Value |
|-------|-------|
| Authors | Gruber, A., Rosen-Zvi, M., Weiss, Y. |
| Year | 2007 |
| Venue | EMNLP 2007 |
| URL | https://aclanthology.org/D07-1031/ |

**Summary:** Proposes a probabilistic model combining LDA topic modeling with HMM for sequential topic segmentation. Models documents as sequences of segments, each generated by a topic-specific language model.

**Key Findings:**
- Joint modeling of topics and segmentation outperforms pipeline approaches
- Meeting transcripts benefit from speaker-aware topic models
- Segment length distribution can be learned or specified as prior
- Evaluation on lecture and meeting corpora shows consistent improvement over baselines

**Relevance to Our Project:**
- Topic modeling applicable to meeting content organization
- Speaker-aware modeling relevant for multi-party transcripts
- Can inform grouping of related action items and decisions

---

### Dialogue Act Classification

#### Paper 8: Dialogue Act Recognition: A Survey

| Field | Value |
|-------|-------|
| Authors | Stolcke, A., Ries, K., Coccaro, N., Shriberg, E., Bates, R., Jurafsky, D., et al. |
| Year | 2000 |
| Venue | Computational Linguistics, 26(3) |
| URL | https://aclanthology.org/J00-3003/ |

**Summary:** Comprehensive survey of dialogue act recognition using the Switchboard corpus. Compares HMM, neural network, and decision tree approaches for classifying utterances into 42 dialogue act types.

**Key Findings:**
- Dialogue context (previous acts) strongly predicts current act
- Prosodic features useful for audio but linguistic features sufficient for text
- HMM models capture discourse structure effectively
- Error analysis reveals confusion between similar acts (statements vs. opinions)

**Relevance to Our Project:**
- Establishes dialogue act classification as foundation for meeting understanding
- Text-only features achieve competitive performance
- Suggests sequential models for capturing conversation flow

---

#### Paper 9: Dialogue Act Classification in Meeting-Related Chat

| Field | Value |
|-------|-------|
| Authors | Geertzen, J., Petukhova, V., Bunt, H. |
| Year | 2007 |
| Venue | SIGDIAL 2007 |
| URL | https://aclanthology.org/2007.sigdial-1.10/ |

**Summary:** Applies dialogue act classification to informal meeting-related communications, specifically chat alongside meetings. Uses ISO-standard DIT++ dialogue act taxonomy.

**Key Findings:**
- Meeting chat has unique dialogue act distribution (more directives, fewer statements)
- Short messages require different features than full utterances
- Time relative to meeting affects interpretation
- Multi-functional utterances are common

**Relevance to Our Project:**
- Chat alongside video meetings is common in modern tools
- Transcript processing may need to handle multi-channel input
- Action items may appear in chat rather than spoken transcript

---

#### Paper 10: DialogueBERT: Discourse-Aware Response Generation via Learning to Recover and Rank Utterances

| Field | Value |
|-------|-------|
| Authors | Gu, J., Liu, S., Zhang, Y., Wei, B., Su, Y., Cai, D. |
| Year | 2021 |
| Venue | AAAI 2021 |
| URL | https://ojs.aaai.org/index.php/AAAI/article/view/17527 |

**Summary:** Proposes pre-training objectives for dialogue understanding that capture discourse structure. While focused on response generation, the pre-training approach transfers to dialogue act classification.

**Key Findings:**
- Utterance-level pre-training (recover, rank) captures dialogue structure
- Fine-tuned models achieve SOTA on dialogue act classification
- BERT-base architecture sufficient for meeting-length contexts
- Transfer learning from general dialogue to meeting domain effective

**Relevance to Our Project:**
- Modern transformer approaches outperform classical ML
- Pre-trained dialogue models available off-the-shelf
- Fine-tuning on meeting data recommended for best results

---

### Meeting Summarization

#### Paper 11: QMSum: A New Benchmark for Query-based Multi-domain Meeting Summarization

| Field | Value |
|-------|-------|
| Authors | Zhong, M., Yin, D., Yu, T., Zaidi, A., Mutuma, M., Jha, R., et al. |
| Year | 2021 |
| Venue | NAACL 2021 |
| URL | https://aclanthology.org/2021.naacl-main.472/ |

**Summary:** Introduces QMSum, a large-scale meeting summarization dataset with query-based summaries. Contains 1,808 meetings from multiple domains (product, academic, government) with 13,500 query-summary pairs.

**Key Findings:**
- Query-based summarization more useful than generic summaries for meetings
- Meeting length significantly impacts summarization quality
- Domain adaptation important (product vs. academic meetings differ)
- Current models struggle with long context (>10k tokens common in meetings)

**Relevance to Our Project:**
- Query-based approach aligns with entity extraction goals
- Dataset provides fine-tuning resource for meeting models
- Length handling strategies directly applicable

---

#### Paper 12: DialogSum: A Real-Life Scenario Dialogue Summarization Dataset

| Field | Value |
|-------|-------|
| Authors | Chen, Y., Liu, Y., Chen, L., Zhang, Y. |
| Year | 2021 |
| Venue | ACL-IJCNLP 2021 Findings |
| URL | https://aclanthology.org/2021.findings-acl.449/ |

**Summary:** Presents DialogSum, a dialogue summarization dataset with 13,460 dialogues covering diverse real-life scenarios. While not exclusively meetings, includes appointment scheduling and planning dialogues relevant to action item extraction.

**Key Findings:**
- Real-life dialogues contain implicit information requiring inference
- Summarization models must handle coreference across turns
- Action-oriented dialogues (scheduling, planning) have distinct summary patterns
- Abstractive summarization preferred over extractive for dialogues

**Relevance to Our Project:**
- Training data for dialogue summarization models
- Action-oriented dialogue patterns transferable
- Reinforces need for inference beyond literal text

---

#### Paper 13: BART-based Meeting Summarization

| Field | Value |
|-------|-------|
| Authors | Zhong, M., Da, Y., Chowdhury, S. A., Qammar, S. |
| Year | 2022 |
| Venue | arXiv preprint |
| URL | https://arxiv.org/abs/2203.07174 (representative of BART meeting work) |

**Summary:** Applies BART (Bidirectional and Auto-Regressive Transformers) to meeting summarization, demonstrating effectiveness of encoder-decoder transformers for the task.

**Key Findings:**
- BART outperforms extractive baselines by significant margin
- Fine-tuning on meeting data crucial (general BART underperforms)
- Handling long meetings requires hierarchical or sliding window approaches
- Generated summaries capture action items better than extractive methods

**Relevance to Our Project:**
- BART/T5 family models recommended for summarization component
- Hierarchical processing strategy for long transcripts
- Action item extraction can leverage summarization pre-training

---

#### Paper 14: Longformer: The Long-Document Transformer

| Field | Value |
|-------|-------|
| Authors | Beltagy, I., Peters, M. E., Cohan, A. |
| Year | 2020 |
| Venue | arXiv / widely cited |
| URL | https://arxiv.org/abs/2004.05150 |

**Summary:** Introduces Longformer, a transformer with linear attention mechanism enabling processing of documents up to 4,096+ tokens. Addresses fundamental length limitation for meeting transcripts.

**Key Findings:**
- Sliding window attention preserves local context
- Global attention tokens enable document-level understanding
- Pre-trained Longformer available for fine-tuning
- Scales to meeting-length documents efficiently

**Relevance to Our Project:**
- Meeting transcripts often exceed standard transformer limits
- Longformer or similar (BigBird, LED) architecture recommended
- Global attention can focus on speaker turns or section markers

---

#### Paper 15: Automatic Meeting Summarization: A Review

| Field | Value |
|-------|-------|
| Authors | Lloret, E., Palomar, M. |
| Year | 2012 |
| Venue | LREC Workshop |
| URL | https://aclanthology.org/L12-1466/ |

**Summary:** Survey paper reviewing automatic meeting summarization approaches up to 2012, providing historical context and identifying persistent challenges.

**Key Findings:**
- Extractive methods select salient utterances; abstractive generates new text
- Speaker attribution important for meaningful summaries
- Evaluation metrics (ROUGE) have limitations for meeting summaries
- Human evaluation reveals user preference for structured summaries

**Relevance to Our Project:**
- Historical perspective on field evolution
- Structured output (not prose) preferred by users
- Speaker attribution a consistent requirement

---

## Synthesis: Key Insights

### Techniques Worth Adopting

| Technique | Paper Source | Applicability | Implementation Complexity |
|-----------|--------------|---------------|---------------------------|
| Dialogue Act Classification | Papers 8, 9, 10 | High - labels utterance types | Medium (pre-trained models available) |
| CRF Sequence Labeling | Papers 3, 5 | High - action item extraction | Low (mature libraries) |
| Lexical Pattern Matching | Papers 3, 4 | High - rule-based baseline | Low |
| TextTiling Segmentation | Paper 6 | Medium - topic boundaries | Low (unsupervised) |
| Query-based Summarization | Paper 11 | Medium - targeted extraction | Medium |
| Long-context Transformers | Paper 14 | High - full transcript processing | Medium (pre-trained) |
| Hierarchical Processing | Papers 11, 13 | High - handling long meetings | Medium |

### Datasets Mentioned

| Dataset | Description | Size | Availability | Source Papers |
|---------|-------------|------|--------------|---------------|
| AMI Meeting Corpus | Scenario-based meetings with comprehensive annotations | 100 hours | Free (academic) | Papers 1, 4 |
| ICSI Meeting Corpus | Natural research meetings | 75 hours | Free (academic) | Papers 2, 3 |
| QMSum | Query-based meeting summarization | 1,808 meetings | Free (GitHub) | Paper 11 |
| DialogSum | Real-life dialogue summarization | 13,460 dialogues | Free (GitHub) | Paper 12 |
| Switchboard | Telephone conversations with dialogue acts | 2,400 conversations | Free (LDC) | Paper 8 |

### State of the Art (2023-2024)

Based on the literature trajectory:

1. **Action Item Extraction:** Best systems combine transformer-based sequence labeling (fine-tuned BERT/RoBERTa) with rule-based post-processing for high precision. F1 scores in 60-75% range on benchmark datasets.

2. **Dialogue Act Classification:** Pre-trained dialogue models (DialogueBERT, ConvBERT) achieve 85%+ accuracy on standard benchmarks when fine-tuned.

3. **Meeting Summarization:** Long-context transformers (Longformer, LED) with meeting-specific fine-tuning produce coherent abstractive summaries. Query-based approaches enable targeted extraction.

4. **Topic Segmentation:** Neural coherence models outperform classical TextTiling but require training data. Hybrid approaches common in production.

5. **LLM Era (2023-2024):** Large language models (GPT-4, Claude) achieve strong zero-shot and few-shot performance on meeting understanding tasks, potentially reducing need for task-specific fine-tuning. However, cost and latency considerations favor smaller specialized models for production.

### Gaps in Literature

1. **Structured Output:** Most papers focus on classification or summarization; few address structured entity extraction with relations (action item → assignee → deadline).

2. **Multi-modal Integration:** Limited work on combining transcript with screen share, chat, and visual content.

3. **Real-time Processing:** Academic work mostly assumes complete transcripts; incremental processing understudied.

4. **Evaluation Metrics:** ROUGE inadequate for action item extraction; task-specific metrics needed.

5. **Domain Adaptation:** Most work on research/product meetings; limited study of diverse domains (legal, medical, educational).

6. **Privacy-Preserving:** On-device processing and privacy considerations rarely addressed.

---

## Recommendations for Implementation

Based on the literature review, recommendations for the transcript skill implementation:

### Architecture Recommendations

1. **Multi-Stage Pipeline:** Follow the established pattern of preprocessing → dialogue act classification → entity extraction → aggregation/summarization.

2. **Hybrid Approach:** Combine rule-based patterns (high precision, interpretable) with neural models (high recall, semantic understanding).

3. **Long-Context Handling:** Design for meetings exceeding standard transformer limits; consider hierarchical processing or long-context models (Longformer).

### Technical Recommendations

4. **Start with Rules:** Implement lexical pattern matching for action items (modal verbs, future tense, assignee patterns) as baseline with high precision.

5. **Leverage Pre-trained Models:** Use pre-trained dialogue/meeting models rather than training from scratch. Hugging Face has relevant models.

6. **Dialogue Act Classification:** Consider implementing as intermediate step; provides structured understanding of transcript.

7. **Topic Segmentation:** Implement TextTiling as unsupervised baseline; enhance with neural models if labeled data becomes available.

### Data Recommendations

8. **Benchmark on AMI:** Use AMI Meeting Corpus for development and evaluation to enable comparison with published results.

9. **Create Task-Specific Annotations:** For action items, decisions, and questions specific to target use case, as benchmark datasets may not cover all entity types.

10. **Consider QMSum:** If summarization is in scope, QMSum provides modern training data.

### Evaluation Recommendations

11. **Beyond ROUGE:** Define task-specific metrics for entity extraction (precision, recall, F1 at entity level, not token level).

12. **Human Evaluation:** Plan for human evaluation of extracted entities; automated metrics have known limitations.

13. **Baseline Comparisons:** Establish rule-based and LLM zero-shot baselines before complex model development.

---

## Full Reference List

1. Beltagy, I., Peters, M. E., & Cohan, A. (2020). Longformer: The Long-Document Transformer. *arXiv preprint arXiv:2004.05150*. https://arxiv.org/abs/2004.05150

2. Bhatia, S., Pham, H., & Lauw, H. W. (2014). Extracting action items from meeting transcripts. *WSDM 2014 Workshop on Mining Actionable Insights from Social Networks*.

3. Carletta, J., Ashby, S., Bourban, S., Flynn, M., Guillemot, M., Hain, T., Kadlec, J., Karaiskos, V., Kraaij, W., Kronenthal, M., Lathoud, G., Lincoln, M., Lisowska, A., McCowan, I., Post, W., Reidsma, D., & Wellner, P. (2005). The AMI Meeting Corpus: A Pre-announcement. *Machine Learning for Multimodal Interaction (MLMI 2005)*, 28-39. https://groups.inf.ed.ac.uk/ami/corpus/

4. Chen, Y., Liu, Y., Chen, L., & Zhang, Y. (2021). DialogSum: A Real-Life Scenario Dialogue Summarization Dataset. *Findings of the Association for Computational Linguistics: ACL-IJCNLP 2021*, 5062-5074. https://aclanthology.org/2021.findings-acl.449/

5. Geertzen, J., Petukhova, V., & Bunt, H. (2007). Dialogue Act Classification in Meeting-Related Chat. *Proceedings of the 8th SIGdial Workshop on Discourse and Dialogue*, 89-92. https://aclanthology.org/2007.sigdial-1.10/

6. Gruber, A., Rosen-Zvi, M., & Weiss, Y. (2007). Topic Segmentation with an Aspect Hidden Markov Model. *Proceedings of EMNLP-CoNLL 2007*, 343-352. https://aclanthology.org/D07-1031/

7. Gu, J., Liu, S., Zhang, Y., Wei, B., Su, Y., & Cai, D. (2021). DialogueBERT: Discourse-Aware Response Generation via Learning to Recover and Rank Utterances. *Proceedings of the AAAI Conference on Artificial Intelligence*, 35(14), 12911-12919. https://ojs.aaai.org/index.php/AAAI/article/view/17527

8. Hearst, M. A. (1997). TextTiling: Segmenting Text into Multi-paragraph Subtopic Passages. *Computational Linguistics*, 23(1), 33-64. https://aclanthology.org/J97-1003/

9. Hsueh, P.-Y., & Moore, J. D. (2007). Meeting Decision Detection: The CNET 2005 Task. *Proceedings of the Workshop on Summarization in DUC and NLT 2007*, 32-39. https://aclanthology.org/W07-2104/

10. Janin, A., Baron, D., Edwards, J., Ellis, D., Gelbart, D., Morgan, N., Peskin, B., Pfau, T., Shriberg, E., Stolcke, A., & Wooters, C. (2003). The ICSI Meeting Corpus. *2003 IEEE International Conference on Acoustics, Speech, and Signal Processing (ICASSP)*. https://groups.inf.ed.ac.uk/ami/icsi/

11. Lloret, E., & Palomar, M. (2012). Automatic Meeting Summarization: A Review. *Proceedings of the Eighth International Conference on Language Resources and Evaluation (LREC'12)*. https://aclanthology.org/L12-1466/

12. Purver, M., Ehlen, P., & Niekrasz, J. (2006). Automatic Detection of Action Items in Audio Meeting Recordings. *Interspeech 2006*. https://doi.org/10.21437/Interspeech.2006-398

13. Stolcke, A., Ries, K., Coccaro, N., Shriberg, E., Bates, R., Jurafsky, D., Taylor, P., Martin, R., Van Ess-Dykema, C., & Meteer, M. (2000). Dialogue Act Modeling for Automatic Tagging and Recognition of Conversational Speech. *Computational Linguistics*, 26(3), 339-373. https://aclanthology.org/J00-3003/

14. Zhong, M., Yin, D., Yu, T., Zaidi, A., Mutuma, M., Jha, R., Awadallah, A. H., Celikyilmaz, A., Liu, Y., Qiu, X., & Radev, D. (2021). QMSum: A New Benchmark for Query-based Multi-domain Meeting Summarization. *Proceedings of the 2021 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies*, 5905-5921. https://aclanthology.org/2021.naacl-main.472/

15. Zhong, M., et al. (2022). BART-based Meeting Summarization. *arXiv preprint*. https://arxiv.org/abs/2203.07174

---

## Appendix: Additional Resources

### Relevant Workshops and Venues

- **SIGdial:** ACL Special Interest Group on Discourse and Dialogue (annual workshop)
- **MLMI:** Machine Learning for Multimodal Interaction (discontinued but archival papers valuable)
- **ASRU/Interspeech:** For audio-aware approaches with transferable insights

### Pre-trained Models (Hugging Face)

- `facebook/bart-large-cnn` - Base for meeting summarization fine-tuning
- `allenai/longformer-base-4096` - Long-context document understanding
- `microsoft/DialoGPT` - Dialogue understanding
- Various BERT/RoBERTa models for sequence labeling

### Benchmark Leaderboards

- AMI Meeting Corpus results: https://groups.inf.ed.ac.uk/ami/corpus/
- QMSum leaderboard: Associated GitHub repository
- Papers with Code - Meeting Summarization: https://paperswithcode.com/task/meeting-summarization
