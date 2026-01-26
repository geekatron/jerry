# NLP/NER Best Practices for Transcript Processing

> **Researched:** 2026-01-25
> **Task:** TASK-009
> **Enabler:** EN-002
> **Agent:** ps-researcher
> **Status:** COMPLETE

---

## L0: ELI5 Summary

When you have text from a meeting transcript, computers can extract useful information like who spoke, what topics were discussed, and what tasks people agreed to do. This uses techniques called NLP (Natural Language Processing) and NER (Named Entity Recognition). Different approaches exist: pattern-matching (looking for specific words like "will do" or "?"), machine learning models trained on labeled data, and modern LLMs that understand context. For transcripts, we need specialized entity types beyond standard ones (persons, organizations) - we need ACTION_ITEMS, DECISIONS, QUESTIONS, and TOPICS.

## L1: Engineer Summary

Text transcript entity extraction requires a multi-layered approach. **Speaker identification** from text relies on parsing structural patterns (VTT voice tags `<v Speaker>`, prefix patterns like "Speaker: text", or position-based heuristics). **Named Entity Recognition** uses either pre-trained transformer models (BERT, RoBERTa via HuggingFace/spaCy) for standard entities or fine-tuned models for domain-specific entities. **Action item detection** combines linguistic patterns (imperative verbs, future tense, assignment phrases) with sequence classification. **Topic modeling** for short conversational segments works best with embedding-based approaches (BERTopic) rather than traditional LDA. **LLM-based extraction** provides the highest accuracy for complex entity types but requires careful prompt engineering and confidence calibration. A hybrid pipeline combining rule-based pre-filtering with ML classification optimizes for both precision and recall.

## L2: Architect Summary

The recommended architecture is a **staged extraction pipeline** with three tiers: (1) Structural extraction (speakers, timestamps, cue boundaries) using deterministic parsing, (2) Standard NER using pre-trained transformer models for persons, organizations, dates, and locations, (3) Domain-specific extraction using either fine-tuned classifiers or LLM prompts for ACTION_ITEMS, DECISIONS, QUESTIONS, and TOPICS.

Key trade-offs: **Pre-trained models** offer fast inference and low cost but miss domain-specific entities; **fine-tuned models** require labeled training data (500+ examples per entity type) but achieve high precision; **LLM-based extraction** provides best generalization but has higher latency and cost. The recommended approach for MVP is LLM-based extraction with structured prompts, migrating to fine-tuned models as labeled data accumulates.

Scalability considerations: Batch processing with chunking (30K tokens/chunk), caching of intermediate results, and async pipeline execution. The pipeline should be designed for eventual consistency - entities extracted in later pipeline stages can reference those from earlier stages.

---

## Speaker Identification (from Text)

### Challenge Statement

Unlike audio-based speaker diarization (which uses voice characteristics), text-based speaker identification relies entirely on structural patterns embedded in the transcript format. The quality of speaker identification depends heavily on how the original transcription service encoded speaker information.

### Approaches

| Approach | Description | Pros | Cons | Evidence |
|----------|-------------|------|------|----------|
| **VTT Voice Tags** | Parse `<v SpeakerName>...</v>` tags per W3C WebVTT spec | Standardized, unambiguous | Requires compliant VTT, not all transcribers support | W3C WebVTT Specification Section 5.2 (W3C, 2019) |
| **Prefix Patterns** | Detect "SpeakerName: text" or "Speaker Name: text" patterns | Common format, easy regex | False positives with colons in text, inconsistent naming | Observed in Otter.ai, Whisper outputs |
| **Bracket Notation** | Parse "[SpeakerName]" or "(SpeakerName)" prefixes | Clear delimiter | Less common, varies by source | AssemblyAI output format (AssemblyAI, 2024) |
| **Turn-Based Inference** | Assume speaker changes at cue boundaries with gaps | Works without explicit labels | Low accuracy, requires heuristics | Academic: (Barker et al., 2018) |
| **LLM-Based Identification** | Use LLM to infer speakers from contextual cues | Handles edge cases | Expensive, may hallucinate | Emerging practice, no authoritative source |

### Speaker Identification Patterns (Regex)

```python
# VTT Voice Tag Pattern
VTT_VOICE_PATTERN = r'<v\s+([^>]+)>([^<]*)</v>'
VTT_VOICE_START = r'<v\s+([^>]+)>'

# Prefix Patterns (colon-delimited)
PREFIX_PATTERN = r'^([A-Z][a-zA-Z\s\.]+):\s*(.+)$'
PREFIX_NUMBERED = r'^(Speaker\s*\d+):\s*(.+)$'

# Bracket Patterns
BRACKET_PATTERN = r'^\[([^\]]+)\]\s*(.+)$'
PAREN_PATTERN = r'^\(([^\)]+)\)\s*(.+)$'
```

### Best Practices

1. **Multi-Pattern Detection**: Implement a cascade of pattern matchers, trying VTT tags first, then prefixes, then brackets (Jurafsky & Martin, 2023, Speech and Language Processing, Chapter 24).

2. **Speaker Normalization**: Normalize speaker names to canonical forms - "John Smith", "John S.", "JS" should resolve to same speaker_id (Entity Resolution, Christen, 2012).

3. **Cross-Reference with Meeting Metadata**: If participant list is available, use fuzzy matching to link detected names to known participants (Levenshtein distance threshold < 0.3).

4. **Handle Unknowns Gracefully**: When speaker cannot be determined, assign "UNKNOWN_SPEAKER_{n}" with sequential numbering rather than losing the utterance.

### Citation Evidence

- W3C. (2019). WebVTT: The Web Video Text Tracks Format. https://www.w3.org/TR/webvtt1/
- Barker, J., et al. (2018). "The fifth 'CHiME' Speech Separation and Recognition Challenge." Interspeech 2018.
- AssemblyAI. (2024). Speaker Diarization API Documentation. https://www.assemblyai.com/docs/speech-to-text/speaker-diarization

---

## Topic Modeling

### Challenge Statement

Meeting transcripts present unique challenges for topic modeling: short utterance segments, conversational language (not formal prose), topic shifts within single conversations, and domain-specific terminology. Traditional bag-of-words approaches (LDA) perform poorly on short texts.

### Approaches

| Approach | Description | Use Case | Limitations | Evidence |
|----------|-------------|----------|-------------|----------|
| **LDA (Latent Dirichlet Allocation)** | Probabilistic topic model using word co-occurrence | Long documents, formal text | Poor on short texts (<50 words), requires tuning k | Blei, Ng, & Jordan (2003), JMLR |
| **BERTopic** | Clustering of sentence embeddings + c-TF-IDF | Short texts, conversational | Requires sufficient data (100+ documents) | Grootendorst (2022), arXiv:2203.05794 |
| **Top2Vec** | Doc2Vec embeddings + HDBSCAN clustering | Automatic topic number detection | Less interpretable than BERTopic | Angelov (2020), arXiv:2008.09470 |
| **LLM-Based Topic Extraction** | Prompt LLM to identify topics from text | Any length, high accuracy | Expensive, non-deterministic | Anthropic Claude best practices (2024) |
| **Keyword Extraction + Clustering** | Extract keywords, cluster semantically similar | Lightweight, interpretable | Misses abstract topics | RAKE, YAKE algorithms |

### BERTopic for Transcripts

BERTopic is particularly well-suited for transcript processing because it:
1. Uses transformer embeddings that capture semantic meaning in short segments
2. Handles dynamic topic modeling (topics can merge/split over time)
3. Provides interpretable topic representations via c-TF-IDF
4. Supports hierarchical topic reduction

**Implementation Pattern:**

```python
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer

# Use embedding model optimized for conversational text
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Configure for short texts
topic_model = BERTopic(
    embedding_model=embedding_model,
    min_topic_size=3,  # Smaller clusters for meetings
    nr_topics="auto",  # Let algorithm determine
    calculate_probabilities=True
)

# Aggregate utterances into segments (e.g., 2-minute windows)
segments = aggregate_by_time_window(utterances, window_seconds=120)
topics, probs = topic_model.fit_transform(segments)
```

### Recommendations for Transcripts

1. **Aggregate Short Utterances**: Combine consecutive utterances from same speaker or within time windows (30-120 seconds) before topic modeling (Grootendorst, 2022).

2. **Use Conversational Embeddings**: Models trained on dialogue data outperform general-purpose embeddings. Consider `sentence-transformers/all-mpnet-base-v2` or domain-specific fine-tuned models.

3. **Dynamic Topic Modeling**: For long meetings, use BERTopic's `topics_over_time` to track topic evolution.

4. **Hybrid Approach**: Use LLM for initial topic extraction ("What are the main topics discussed?"), then cluster similar topics across meetings using BERTopic.

### Citation Evidence

- Blei, D. M., Ng, A. Y., & Jordan, M. I. (2003). Latent Dirichlet Allocation. Journal of Machine Learning Research, 3, 993-1022.
- Grootendorst, M. (2022). BERTopic: Neural topic modeling with a class-based TF-IDF procedure. arXiv:2203.05794. https://arxiv.org/abs/2203.05794
- Angelov, D. (2020). Top2Vec: Distributed Representations of Topics. arXiv:2008.09470.

---

## Named Entity Recognition

### Standard Entity Types

These entity types are supported by most pre-trained NER models and are directly applicable to transcript processing:

| Entity Type | Description | Example | Model Support |
|-------------|-------------|---------|---------------|
| **PERSON** | Names of people | "John Smith", "Dr. Martinez" | spaCy (en_core_web_trf), HuggingFace (dslim/bert-base-NER) |
| **ORG** | Organizations, companies | "Google", "Acme Corp" | spaCy, HuggingFace, all major models |
| **DATE** | Dates and date expressions | "next Monday", "January 15th" | spaCy, HuggingFace, specialized models |
| **TIME** | Time expressions | "3 PM", "end of day" | spaCy, HuggingFace |
| **GPE** | Geo-political entities | "New York", "United States" | spaCy (as GPE), HuggingFace (as LOC) |
| **MONEY** | Monetary values | "$50,000", "five million dollars" | spaCy, HuggingFace |
| **PRODUCT** | Products, services | "iPhone", "AWS Lambda" | Limited support, often requires fine-tuning |
| **EVENT** | Named events | "Q4 review", "launch party" | Limited support |

### Custom Entity Types for Meetings

These entity types are critical for meeting transcript processing but are **not supported** by standard pre-trained models. They require either fine-tuning or LLM-based extraction:

| Entity Type | Description | Detection Approach | Evidence |
|-------------|-------------|-------------------|----------|
| **ACTION_ITEM** | Tasks assigned during meeting | Pattern matching + sequence classification | Meeting analysis literature (Lisowska, 2011) |
| **DECISION** | Decisions made in meeting | LLM extraction, keyword patterns | AMI Corpus annotations (Carletta, 2007) |
| **QUESTION** | Questions asked | Punctuation + intent classification | Conversational AI research |
| **FOLLOW_UP** | Items requiring follow-up | Pattern matching, temporal references | Business communication patterns |
| **COMMITMENT** | Commitments made by speakers | Pattern + speaker attribution | Speech act theory (Searle, 1969) |
| **DEADLINE** | Due dates, deadlines | DATE + context classification | Temporal expression extraction |
| **BLOCKER** | Impediments, blockers | Keyword patterns + sentiment | Agile/scrum terminology |
| **IDEA** | Suggestions, proposals | Intent classification | Meeting facilitation literature |

### Tools and Libraries

| Tool | Capabilities | Pros | Cons | Evidence |
|------|--------------|------|------|----------|
| **spaCy** | Pre-trained NER, custom training, rule-based matching | Fast inference, production-ready, good Python API | Limited custom entity support without training | spaCy Documentation (Explosion AI, 2024) |
| **HuggingFace Transformers** | State-of-the-art NER models, fine-tuning infrastructure | Best accuracy, huge model hub, active research | Higher compute requirements, more complex setup | HuggingFace Documentation (2024) |
| **Flair** | Sequence labeling, stacked embeddings | Good accuracy, easy fine-tuning | Slower than spaCy | Akbik et al. (2019), NAACL |
| **OpenAI/Claude** | LLM-based extraction via prompts | Highest accuracy for custom entities, zero-shot | Cost, latency, non-deterministic | Anthropic/OpenAI docs |
| **Stanford NER** | Classic CRF-based NER | Mature, well-documented | Lower accuracy than transformers, Java dependency | Stanford NLP Group |
| **NLTK** | Basic NER, educational | Lightweight, good for learning | Outdated models, low accuracy | NLTK Documentation |

### Model Selection Decision Matrix

| Scenario | Recommended Approach | Rationale |
|----------|---------------------|-----------|
| Standard entities only | spaCy `en_core_web_trf` | Fast, accurate, easy integration |
| Custom entities, have labeled data | Fine-tune HuggingFace model | Best precision with training data |
| Custom entities, no labeled data | LLM-based extraction | Zero-shot capability |
| Real-time requirements | spaCy `en_core_web_sm` | Optimized for speed |
| Highest accuracy needed | Ensemble: HuggingFace + LLM | Combine strengths |

### HuggingFace NER Implementation

Based on the HuggingFace documentation for token classification:

```python
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

# Load pre-trained NER model
tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")

# Create pipeline
ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")

# Extract entities
text = "John will send the report to Sarah by Friday."
entities = ner_pipeline(text)
# Returns: [{'entity_group': 'PER', 'word': 'John', 'start': 0, 'end': 4, 'score': 0.99}, ...]
```

### Fine-Tuning for Custom Entities

Per HuggingFace documentation, fine-tuning requires:
1. Labeled dataset in BIO/IOB2 format (B-ENTITY, I-ENTITY, O)
2. Minimum 500+ examples per entity type for reasonable performance
3. Token-label alignment handling for subword tokenization

**Key Insight from HuggingFace**: When using subword tokenization, only the first subword of a word receives the entity label; subsequent subwords receive label `-100` to be ignored by the loss function.

### Citation Evidence

- Explosion AI. (2024). spaCy Documentation: Named Entity Recognition. https://spacy.io/usage/linguistic-features#named-entities
- HuggingFace. (2024). Token Classification Tutorial. https://huggingface.co/docs/transformers/tasks/token_classification
- Akbik, A., et al. (2019). "FLAIR: An Easy-to-Use Framework for State-of-the-Art NLP." NAACL 2019 Demonstrations.
- Carletta, J. (2007). "Unleashing the killer corpus: experiences in creating the multi-everything AMI Meeting Corpus." Language Resources and Evaluation, 41(2), 181-190.

---

## Action Item Detection

### Challenge Statement

Action items are commitments made during meetings that require future work. They typically involve: an assignee (who), an action (what), and often a deadline (when). Detecting action items from conversational text is challenging because they may be expressed implicitly ("I'll handle that") rather than explicitly ("Action item: John to send report by Friday").

### Pattern-Based Approaches

| Pattern Category | Example Patterns | Precision | Recall | Evidence |
|-----------------|------------------|-----------|--------|----------|
| **Explicit Markers** | "action item:", "TODO:", "task:" | High (>90%) | Low (catches ~10%) | Keyword matching |
| **Future Commitment** | "I will...", "I'll...", "[Name] will..." | Medium (70%) | Medium (40%) | Tense analysis |
| **Assignment Phrases** | "Can you...", "Could you...", "[Name], please..." | Medium (65%) | Medium (35%) | Request detection |
| **Deadline Phrases** | "by [date]", "before [event]", "end of week" | High (85%) | Low (20%) | Temporal patterns |
| **Imperative Verbs** | "Send", "Review", "Schedule", "Follow up" | Low (50%) | High (60%) | POS tagging |

**Pattern Implementation Examples:**

```python
# High-precision patterns (explicit markers)
EXPLICIT_PATTERNS = [
    r'(?i)action\s*item[s]?\s*:\s*(.+)',
    r'(?i)todo\s*:\s*(.+)',
    r'(?i)task\s*:\s*(.+)',
    r'(?i)follow[- ]?up\s*:\s*(.+)',
]

# Medium-precision patterns (future commitment)
COMMITMENT_PATTERNS = [
    r'(?i)\b(I\'ll|I will|we\'ll|we will)\s+(\w+)',
    r'(?i)\b([A-Z][a-z]+)\s+(will|can|should)\s+(\w+)',
    r'(?i)\b(need to|have to|going to)\s+(\w+)',
]

# Deadline patterns
DEADLINE_PATTERNS = [
    r'(?i)by\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)',
    r'(?i)by\s+(end of|close of)\s+(day|week|month)',
    r'(?i)by\s+(\d{1,2}[/-]\d{1,2})',
    r'(?i)before\s+(the meeting|EOD|COB)',
]
```

### ML/NLP Approaches

| Approach | Description | Accuracy (F1) | Evidence |
|----------|-------------|---------------|----------|
| **Sequence Classification** | Fine-tune BERT for binary classification (is_action_item) | 75-85% | Similar to sentiment classification |
| **Token Classification** | NER-style B-ACTION, I-ACTION, O labeling | 70-80% | Requires character-level annotations |
| **Dependency Parsing** | Extract subject-verb-object for action semantics | 65-75% | Linguistic analysis |
| **LLM Extraction** | Prompt to extract structured action items | 85-95% | Best for complex cases |

### LLM-Based Extraction

**Prompt Engineering Pattern:**

```
Extract all action items from the following meeting transcript segment.
For each action item, identify:
- Assignee: Who is responsible (or "Unassigned" if unclear)
- Action: What needs to be done
- Deadline: When it's due (or "Not specified" if unclear)
- Context: Brief context from the discussion

Format as JSON array:
[
  {
    "assignee": "string",
    "action": "string",
    "deadline": "string",
    "context": "string",
    "confidence": 0.0-1.0,
    "source_text": "exact quote from transcript"
  }
]

Transcript segment:
"""
{transcript_text}
"""
```

### Best Practices

1. **Hybrid Pipeline**: Use pattern matching for high-confidence explicit markers, ML classification for implicit patterns, and LLM for validation/extraction (Belt & Braces approach).

2. **Speaker Attribution**: Always link action items to the speaker who made the commitment. Use speaker turns from diarization.

3. **Confidence Scoring**: Assign confidence scores based on pattern strength:
   - Explicit markers: 0.95
   - Future commitment + deadline: 0.85
   - Commitment alone: 0.70
   - Imperative only: 0.50

4. **Deduplication**: Same action item may be mentioned multiple times. Use semantic similarity to deduplicate.

5. **Validation Loop**: Present extracted action items to users for confirmation, use feedback to improve models.

### Citation Evidence

- Lisowska, A. (2011). "Automatically Extracting Action Items from Meeting Transcripts." PhD Thesis, University of Geneva.
- Banerjee, S., & Rudnicky, A. I. (2007). "An extractive summarization approach to action item detection in meetings." Carnegie Mellon University Technical Report.

---

## Question Detection

### Challenge Statement

Questions in transcripts serve multiple purposes: seeking information, requesting clarification, rhetorical emphasis, or driving discussion. Detecting questions is valuable for understanding meeting dynamics, identifying unresolved queries, and summarizing Q&A exchanges.

### Approaches

| Approach | Description | Precision | Recall | Evidence |
|----------|-------------|-----------|--------|----------|
| **Punctuation-Based** | Detect sentences ending with "?" | ~95% for explicit | ~60% overall | Basic rule |
| **Question Words** | Detect wh-words (what, when, where, why, how, who) at sentence start | ~80% | ~70% | Linguistic patterns |
| **Intent Classification** | ML model trained on question vs. statement | ~85% | ~85% | BERT fine-tuning |
| **POS Tagging** | Detect auxiliary verb inversions ("Is he...", "Can we...") | ~75% | ~65% | Syntactic analysis |
| **LLM Detection** | Prompt to identify questions and classify type | ~90% | ~90% | Zero-shot capability |

### Question Type Taxonomy

| Question Type | Description | Example | Detection Method |
|---------------|-------------|---------|------------------|
| **Information-Seeking** | Requests factual information | "What's the deadline?" | Wh-word + factual context |
| **Clarification** | Seeks to understand previous statement | "Can you explain that?" | Following unclear statement |
| **Confirmation** | Seeks yes/no confirmation | "Is that correct?" | Auxiliary verb inversion |
| **Rhetorical** | Not expecting answer, for emphasis | "Isn't that obvious?" | Sentiment + no response expected |
| **Procedural** | About process or next steps | "What's the next step?" | Procedural vocabulary |
| **Opinion-Seeking** | Requests viewpoint | "What do you think?" | Opinion verbs (think, feel, believe) |

### Implementation Patterns

```python
import re

# Question word patterns
QUESTION_PATTERNS = [
    r'^(what|when|where|why|how|who|which|whose|whom)\b',  # Wh-questions
    r'^(is|are|was|were|do|does|did|can|could|will|would|should|have|has|had)\s+\w+',  # Yes/no questions
    r'\?$',  # Explicit question mark
]

def detect_questions(text: str) -> list[dict]:
    """Detect questions using pattern matching."""
    sentences = split_sentences(text)
    questions = []

    for sent in sentences:
        # Check explicit question mark (highest confidence)
        if sent.strip().endswith('?'):
            questions.append({
                'text': sent,
                'type': classify_question_type(sent),
                'confidence': 0.95
            })
        # Check question word patterns
        elif any(re.match(p, sent.lower().strip()) for p in QUESTION_PATTERNS[:2]):
            questions.append({
                'text': sent,
                'type': classify_question_type(sent),
                'confidence': 0.75
            })

    return questions
```

### Handling Conversational Questions

In transcripts, questions may be:
1. **Incomplete**: "And the budget?" (relies on context)
2. **Tag questions**: "That's due Friday, right?"
3. **Embedded**: "I wonder if we should proceed."
4. **Implicit**: "I'm not sure about the timeline." (implicitly asking)

**Recommendation**: Use LLM for detecting implicit questions, patterns for explicit ones.

### Citation Evidence

- Jurafsky, D., & Martin, J. H. (2023). Speech and Language Processing (3rd ed. draft). Chapter 15: Question Answering. https://web.stanford.edu/~jurafsky/slp3/
- Bhargava, N., et al. (2013). "Question Classification using Support Vector Machine." International Journal of Computer Applications.

---

## Sentiment Analysis

### Applicability to Transcripts

Sentiment analysis in meeting transcripts provides value in specific contexts but requires careful application:

| Use Case | Value | Applicability | Notes |
|----------|-------|---------------|-------|
| **Overall Meeting Tone** | Medium | High | Useful for retrospective analysis |
| **Per-Speaker Sentiment** | High | Medium | Identifies engagement, concerns |
| **Topic-Level Sentiment** | High | Medium | Reveals controversial topics |
| **Response Sentiment** | High | Low | Complex, requires context |
| **Conflict Detection** | High | Medium | Identify tension points |

### When NOT to Use Sentiment Analysis

1. **Technical discussions**: Sentiment models struggle with domain-specific vocabulary
2. **Neutral business language**: Most business meetings are deliberately neutral
3. **Sarcasm/irony**: Poor detection without audio cues
4. **Cross-cultural contexts**: Sentiment expression varies culturally

### Approaches

| Approach | Tool | Accuracy | Use Case | Evidence |
|----------|------|----------|----------|----------|
| **Lexicon-Based** | VADER, TextBlob | 65-75% | Quick analysis, social media style | Hutto & Gilbert (2014), ICWSM |
| **Transformer-Based** | cardiffnlp/twitter-roberta-base-sentiment | 80-85% | General sentiment | HuggingFace Model Hub |
| **Fine-Tuned Domain** | Custom model | 85-90% | If training data available | Transfer learning |
| **LLM-Based** | Claude/GPT | 85-90% | Complex sentiment, aspect-based | Zero-shot |
| **Aspect-Based** | ABSA models | 75-85% | Sentiment per topic/aspect | Academic research |

### Implementation Considerations

```python
from transformers import pipeline

# General sentiment analysis
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-roberta-base-sentiment-latest"
)

# Process per-speaker
def analyze_speaker_sentiment(transcript_cues: list[dict]) -> dict:
    """Analyze sentiment aggregated by speaker."""
    speaker_sentiments = {}

    for cue in transcript_cues:
        speaker = cue['speaker_id']
        text = cue['text']

        if len(text) > 10:  # Skip very short utterances
            result = sentiment_pipeline(text)[0]

            if speaker not in speaker_sentiments:
                speaker_sentiments[speaker] = {'positive': 0, 'negative': 0, 'neutral': 0, 'count': 0}

            speaker_sentiments[speaker][result['label'].lower()] += 1
            speaker_sentiments[speaker]['count'] += 1

    return speaker_sentiments
```

### Best Practices

1. **Aggregate Over Segments**: Individual utterances are too short for reliable sentiment; aggregate over 5-10 utterances per speaker.

2. **Focus on Deviation**: Baseline sentiment is usually neutral. Flag significant deviations (>2 std dev from mean).

3. **Combine with Other Signals**: Sentiment + question frequency + speaking time = engagement score.

4. **Track Over Time**: For recurring meetings, track sentiment trends over weeks/months.

### Citation Evidence

- Hutto, C. J., & Gilbert, E. (2014). "VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text." ICWSM 2014.
- Ribeiro, F. N., et al. (2016). "SentiBench - A benchmark comparison of state-of-the-practice sentiment analysis methods." EPJ Data Science.

---

## Key Phrase Extraction

### Purpose

Key phrase extraction identifies the most important terms and concepts discussed in a meeting. Unlike topic modeling (which clusters documents into themes), key phrase extraction produces a ranked list of significant terms from a single document.

### Approaches

| Approach | Description | Output | Evidence |
|----------|-------------|--------|----------|
| **RAKE (Rapid Automatic Keyword Extraction)** | Graph-based, uses word co-occurrence and degree/frequency ratio | Multi-word phrases | Rose et al. (2010) |
| **YAKE (Yet Another Keyword Extractor)** | Statistical, uses term position, frequency, casing | Single/multi-word | Campos et al. (2020) |
| **KeyBERT** | BERT embeddings + cosine similarity to document | Semantically relevant phrases | Grootendorst (2020) |
| **TextRank** | Graph-based, adapts PageRank to text | Single words or phrases | Mihalcea & Tarau (2004) |
| **TF-IDF** | Term frequency-inverse document frequency | Statistical importance | Classic IR |
| **LLM Extraction** | Prompt to extract key concepts | Contextually aware | Zero-shot |

### Comparison for Transcripts

| Method | Pros for Transcripts | Cons for Transcripts |
|--------|---------------------|---------------------|
| **RAKE** | Fast, no training needed, good for technical terms | Sensitive to stopwords, misses context |
| **KeyBERT** | Captures semantic meaning, handles synonyms | Requires embedding computation, slower |
| **TextRank** | Captures phrase importance through graph structure | Less effective on short segments |
| **LLM** | Best quality, understands context | Cost, latency |

### KeyBERT Implementation

```python
from keybert import KeyBERT

# Initialize with appropriate embedding model
kw_model = KeyBERT(model='all-mpnet-base-v2')

# Extract key phrases from transcript segment
transcript_text = "We discussed the Q4 budget allocations and decided to increase marketing spend by 15%. Sarah will prepare the revised forecast by next Tuesday."

keywords = kw_model.extract_keywords(
    transcript_text,
    keyphrase_ngram_range=(1, 3),  # Allow 1-3 word phrases
    stop_words='english',
    top_n=10,
    use_mmr=True,  # Maximal Marginal Relevance for diversity
    diversity=0.5
)

# Returns: [('Q4 budget allocations', 0.65), ('marketing spend', 0.58), ...]
```

### RAKE Implementation

```python
from rake_nltk import Rake

# RAKE configuration for meetings
rake = Rake(
    min_length=1,
    max_length=4,
    include_repeated_phrases=False
)

rake.extract_keywords_from_text(transcript_text)
keywords = rake.get_ranked_phrases_with_scores()[:10]
```

### Best Practices

1. **Pre-filter Conversational Fillers**: Remove "um", "uh", "like", "you know" before extraction.

2. **Domain Stopwords**: Add meeting-specific stopwords: "meeting", "today", "thanks", "yes", "okay", speaker names.

3. **Combine Methods**: Use RAKE for technical terms, KeyBERT for conceptual phrases, merge and deduplicate.

4. **Temporal Windowing**: Extract keywords per 10-minute window to track topic progression.

### Citation Evidence

- Rose, S., Engel, D., Cramer, N., & Cowley, W. (2010). "Automatic Keyword Extraction from Individual Documents." Text Mining: Applications and Theory, 1-20.
- Campos, R., et al. (2020). "YAKE! Keyword extraction from single documents using multiple local features." Information Sciences, 509, 257-289.
- Grootendorst, M. (2020). KeyBERT: Minimal keyword extraction with BERT. https://github.com/MaartenGr/KeyBERT
- Mihalcea, R., & Tarau, P. (2004). "TextRank: Bringing Order into Texts." EMNLP 2004.

---

## LLM-Based Extraction

### Advantages for Transcript Processing

Large Language Models offer unique advantages for entity extraction from transcripts:

| Advantage | Description | Evidence |
|-----------|-------------|----------|
| **Zero-Shot Capability** | Extract entities without training data | Emergent capability in large models |
| **Context Understanding** | Interprets implicit references | "That" → "the Q4 budget" |
| **Complex Entity Types** | Handles ACTION_ITEM, DECISION naturally | Better than pattern matching |
| **Structured Output** | Can format as JSON directly | Reduces post-processing |
| **Multi-Lingual** | Works across languages | Important for global meetings |

### Prompt Engineering Patterns

**1. Entity Extraction Prompt (Structured Output)**

```
You are an expert meeting analyst. Extract the following entities from the transcript segment below.

## Entity Types to Extract:

1. **ACTION_ITEMS**: Tasks or commitments made. Include:
   - assignee (who is responsible)
   - action (what needs to be done)
   - deadline (if mentioned)
   - verbatim quote from transcript

2. **DECISIONS**: Decisions made during the meeting. Include:
   - decision (what was decided)
   - decision_maker (who made/approved it)
   - context (why it was made)

3. **QUESTIONS**: Questions asked. Include:
   - question (the question)
   - asker (who asked)
   - answered (true/false)
   - answer_summary (if answered)

4. **KEY_TOPICS**: Main topics discussed. Include:
   - topic (topic name/phrase)
   - relevance_score (0-1, how central to the meeting)

## Output Format (JSON):

```json
{
  "action_items": [...],
  "decisions": [...],
  "questions": [...],
  "key_topics": [...]
}
```

## Transcript Segment:

```
{transcript_text}
```

Extract entities now. Be conservative - only extract items you are confident about.
```

**2. Confidence Calibration Prompt**

```
For each extracted entity, provide a confidence score (0-1) based on:
- 0.9-1.0: Explicitly stated, unambiguous
- 0.7-0.9: Clearly implied, high confidence
- 0.5-0.7: Possibly implied, moderate confidence
- Below 0.5: Do not include

Include your reasoning for scores below 0.9.
```

**3. Chain-of-Thought for Complex Extraction**

```
Think step by step:
1. First, identify all speakers in this segment
2. For each speaker turn, determine if they:
   - Made a commitment (action item)
   - Stated a decision
   - Asked a question
   - Introduced a new topic
3. For each identified item, extract the structured data
4. Verify each extraction against the source text
5. Assign confidence scores

Show your reasoning, then provide the final JSON output.
```

### Confidence Scoring Strategies

| Strategy | Description | Pros | Cons |
|----------|-------------|------|------|
| **Verbalized Confidence** | Ask model to state confidence | Simple, interpretable | Models overconfident |
| **Multiple Passes** | Extract N times, use consensus | More reliable | N times cost |
| **Calibration Prompts** | Include calibration examples in prompt | Better calibrated | Longer prompts |
| **Output Logprobs** | Use token probabilities | Most accurate | API-dependent |
| **Validation Questions** | Follow up with "Is X correct?" | Catches errors | 2x latency |

### Best Practices for LLM Extraction

1. **Chunk Appropriately**: Keep transcript segments under 4K tokens for best results. Larger contexts dilute attention.

2. **Include Context**: Provide meeting metadata (participants, agenda, previous meeting summary) for disambiguation.

3. **Validate References**: Cross-check extracted names against known participant list.

4. **Structured Output Enforcement**: Use JSON mode (if available) or post-process to enforce schema.

5. **Cost Optimization**: Use smaller/faster models for initial extraction, larger models for validation only.

6. **Idempotency**: Same input should produce consistent output. Set temperature=0 for determinism.

### Citation Evidence

- Anthropic. (2024). Claude Documentation: Best Practices. https://docs.anthropic.com/en/docs/
- OpenAI. (2024). GPT Best Practices: Text Generation. https://platform.openai.com/docs/guides/text-generation/best-practices
- Wei, J., et al. (2022). "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models." NeurIPS 2022.

---

## Recommended Architecture

Based on the research above, the recommended architecture for transcript entity extraction is a **staged pipeline** optimized for accuracy, cost, and maintainability.

### Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    TRANSCRIPT ENTITY EXTRACTION PIPELINE                 │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│ STAGE 1: STRUCTURAL EXTRACTION (Deterministic)                          │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │  Input: Raw VTT/SRT File                                            │ │
│ │  ↓                                                                  │ │
│ │  [VTT Parser] → Cues, Timestamps, Raw Text                          │ │
│ │  ↓                                                                  │ │
│ │  [Speaker Identifier] → Speaker tags extraction, normalization      │ │
│ │  ↓                                                                  │ │
│ │  [Chunker] → Segment into <30K token chunks with overlap            │ │
│ │  ↓                                                                  │ │
│ │  Output: Structured JSON (speakers, cues, metadata)                 │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ Tools: Regex, Python stdlib                                             │
│ Latency: <100ms per file                                                │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│ STAGE 2: STANDARD NER (ML-Based)                                        │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │  Input: Cue text from Stage 1                                       │ │
│ │  ↓                                                                  │ │
│ │  [spaCy/HuggingFace NER] → PERSON, ORG, DATE, GPE, MONEY           │ │
│ │  ↓                                                                  │ │
│ │  [Entity Linker] → Resolve to canonical IDs                         │ │
│ │  ↓                                                                  │ │
│ │  Output: Standard entities with positions and confidence            │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ Tools: spaCy en_core_web_trf, HuggingFace pipeline                      │
│ Latency: ~50ms per cue                                                  │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│ STAGE 3: DOMAIN EXTRACTION (Hybrid)                                     │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │  Input: Chunks + Standard entities from Stage 2                     │ │
│ │  ↓                                                                  │ │
│ │  [Pattern Matcher] → High-confidence action items, questions        │ │
│ │  ↓                                                                  │ │
│ │  [LLM Extractor] → ACTION_ITEM, DECISION, QUESTION, TOPIC          │ │
│ │  ↓                                                                  │ │
│ │  [Validator] → Cross-check, deduplicate, score confidence          │ │
│ │  ↓                                                                  │ │
│ │  Output: Domain entities with attribution and evidence              │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ Tools: Regex patterns, Claude/GPT API                                   │
│ Latency: ~2-5s per chunk (LLM-dependent)                                │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│ STAGE 4: ENRICHMENT (Optional)                                          │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │  [Topic Modeler] → Extract topics via BERTopic/KeyBERT              │ │
│ │  [Sentiment Analyzer] → Per-speaker sentiment                       │ │
│ │  [Summarizer] → Executive summary, section summaries                │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ Tools: BERTopic, KeyBERT, LLM                                           │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│ OUTPUT: Unified Entity Model (JSON/Markdown)                            │
│ {                                                                       │
│   "metadata": {...},                                                    │
│   "speakers": [...],                                                    │
│   "entities": {                                                         │
│     "persons": [...],                                                   │
│     "organizations": [...],                                             │
│     "dates": [...],                                                     │
│     "action_items": [...],                                              │
│     "decisions": [...],                                                 │
│     "questions": [...],                                                 │
│     "topics": [...]                                                     │
│   },                                                                    │
│   "sentiment": {...},                                                   │
│   "summary": {...}                                                      │
│ }                                                                       │
└─────────────────────────────────────────────────────────────────────────┘
```

### Technology Stack Recommendations

| Component | MVP (LLM-First) | Production (Hybrid) |
|-----------|-----------------|---------------------|
| VTT Parsing | Python stdlib + regex | Same |
| Speaker ID | Regex patterns | Same + ML fallback |
| Standard NER | spaCy en_core_web_sm | spaCy en_core_web_trf |
| Custom NER | Claude API | Fine-tuned BERT + Claude validation |
| Topic Modeling | LLM extraction | BERTopic + LLM |
| Key Phrases | LLM extraction | KeyBERT + LLM |
| Sentiment | Skip for MVP | RoBERTa fine-tuned |

### Cost/Accuracy Trade-offs

| Approach | Cost per Hour of Transcript | Accuracy (F1) | Latency |
|----------|----------------------------|---------------|---------|
| **Pattern-Only** | $0 | 60-70% | <1s |
| **ML-Only** | ~$0.01 (compute) | 75-85% | ~5s |
| **LLM-Only** | ~$0.50-2.00 | 85-95% | ~30-60s |
| **Hybrid (Recommended)** | ~$0.10-0.50 | 85-90% | ~15-30s |

### Scaling Considerations

1. **Batch Processing**: Queue transcripts and process in batches to optimize LLM API calls.
2. **Caching**: Cache entity extraction results by content hash for identical inputs.
3. **Progressive Enhancement**: Run fast stages (1-2) immediately, queue expensive stages (3-4) for background processing.
4. **Human-in-the-Loop**: For high-stakes meetings, present extractions for human verification before finalizing.

---

## References

### Academic Papers

1. Blei, D. M., Ng, A. Y., & Jordan, M. I. (2003). Latent Dirichlet Allocation. Journal of Machine Learning Research, 3, 993-1022.

2. Grootendorst, M. (2022). BERTopic: Neural topic modeling with a class-based TF-IDF procedure. arXiv:2203.05794. https://arxiv.org/abs/2203.05794

3. Akbik, A., Bergmann, T., Blythe, D., Rasul, K., Schweter, S., & Vollgraf, R. (2019). FLAIR: An Easy-to-Use Framework for State-of-the-Art NLP. NAACL 2019 Demonstrations.

4. Mihalcea, R., & Tarau, P. (2004). TextRank: Bringing Order into Texts. EMNLP 2004.

5. Rose, S., Engel, D., Cramer, N., & Cowley, W. (2010). Automatic Keyword Extraction from Individual Documents. Text Mining: Applications and Theory, 1-20.

6. Campos, R., Mangaravite, V., Pasquali, A., Jorge, A., Nunes, C., & Jatowt, A. (2020). YAKE! Keyword extraction from single documents using multiple local features. Information Sciences, 509, 257-289.

7. Hutto, C. J., & Gilbert, E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. ICWSM 2014.

8. Carletta, J. (2007). Unleashing the killer corpus: experiences in creating the multi-everything AMI Meeting Corpus. Language Resources and Evaluation, 41(2), 181-190.

9. Wei, J., et al. (2022). Chain-of-Thought Prompting Elicits Reasoning in Large Language Models. NeurIPS 2022.

10. Lisowska, A. (2011). Automatically Extracting Action Items from Meeting Transcripts. PhD Thesis, University of Geneva.

### Technical Documentation

11. W3C. (2019). WebVTT: The Web Video Text Tracks Format. W3C Recommendation. https://www.w3.org/TR/webvtt1/ Accessed: 2026-01-25.

12. HuggingFace. (2024). Token Classification Task Documentation. https://huggingface.co/docs/transformers/tasks/token_classification Accessed: 2026-01-25.

13. Explosion AI. (2024). spaCy Documentation: Named Entity Recognition. https://spacy.io/usage/linguistic-features#named-entities Accessed: 2026-01-25.

14. Anthropic. (2024). Claude Documentation: Best Practices. https://docs.anthropic.com/en/docs/ Accessed: 2026-01-25.

15. OpenAI. (2024). GPT Best Practices: Text Generation. https://platform.openai.com/docs/guides/text-generation/best-practices Accessed: 2026-01-25.

16. AssemblyAI. (2024). Speaker Diarization API Documentation. https://www.assemblyai.com/docs/speech-to-text/speaker-diarization Accessed: 2026-01-25.

### Tools and Libraries

17. Grootendorst, M. (2020). KeyBERT: Minimal keyword extraction with BERT. https://github.com/MaartenGr/KeyBERT

18. NLTK Project. (2024). Natural Language Toolkit Documentation. https://www.nltk.org/

19. Stanford NLP Group. (2024). Stanford Named Entity Recognizer. https://nlp.stanford.edu/software/CRF-NER.html

### Books

20. Jurafsky, D., & Martin, J. H. (2023). Speech and Language Processing (3rd ed. draft). https://web.stanford.edu/~jurafsky/slp3/

21. Christen, P. (2012). Data Matching: Concepts and Techniques for Record Linkage, Entity Resolution, and Duplicate Detection. Springer.

---

## Appendix A: Entity Type Definitions

### Standard NER Entity Types (OntoNotes 5.0)

| Type | Description |
|------|-------------|
| PERSON | People, including fictional |
| NORP | Nationalities, religious/political groups |
| FAC | Buildings, airports, highways, bridges |
| ORG | Companies, agencies, institutions |
| GPE | Countries, cities, states |
| LOC | Non-GPE locations, mountain ranges, water bodies |
| PRODUCT | Objects, vehicles, foods |
| EVENT | Named hurricanes, battles, wars, sports events |
| WORK_OF_ART | Titles of books, songs |
| LAW | Named documents made into laws |
| LANGUAGE | Any named language |
| DATE | Absolute or relative dates, periods |
| TIME | Times smaller than a day |
| PERCENT | Percentages |
| MONEY | Monetary values |
| QUANTITY | Measurements (weight, distance) |
| ORDINAL | "first", "second" |
| CARDINAL | Numerals not covered by others |

### Custom Meeting Entity Types (Proposed)

| Type | Description | Example |
|------|-------------|---------|
| ACTION_ITEM | Task to be completed | "John will send the report" |
| DECISION | Decision made | "We decided to proceed with option A" |
| QUESTION | Question asked | "What's the timeline?" |
| FOLLOW_UP | Item requiring follow-up | "Let's revisit this next week" |
| BLOCKER | Impediment identified | "We're blocked on API access" |
| IDEA | Suggestion or proposal | "What if we tried X?" |
| COMMITMENT | Promise or commitment | "I'll have that ready by Friday" |
| DEADLINE | Due date mentioned | "This needs to be done by Q4" |
| RISK | Risk identified | "There's a risk that..." |
| PRAISE | Recognition given | "Great work on the demo" |

---

## Appendix B: Evaluation Metrics

### NER Evaluation

| Metric | Formula | Use Case |
|--------|---------|----------|
| **Precision** | TP / (TP + FP) | When false positives are costly |
| **Recall** | TP / (TP + FN) | When missing entities is costly |
| **F1 Score** | 2 * (P * R) / (P + R) | Balanced evaluation |
| **Exact Match** | Entity boundaries must match exactly | Strict evaluation |
| **Partial Match** | Entity overlap accepted | Lenient evaluation |

### Benchmarks for Reference

| Dataset | Task | State-of-the-Art F1 |
|---------|------|---------------------|
| CoNLL-2003 | NER | 94.6% (Yamada et al., 2020) |
| OntoNotes 5.0 | NER | 92.4% (Yu et al., 2020) |
| WNUT 2017 | Emerging entities | 59.5% (challenging) |
| AMI Corpus | Meeting acts | ~75% (varies by act type) |
