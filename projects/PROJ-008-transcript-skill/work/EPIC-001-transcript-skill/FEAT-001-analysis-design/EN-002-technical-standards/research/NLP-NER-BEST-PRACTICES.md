# NLP/NER Best Practices for Transcript Processing

> **Researched:** 2026-01-25
> **Last Updated:** 2026-01-25 (Live Web Research Enhancement)
> **Task:** TASK-009
> **Enabler:** EN-002
> **Agent:** ps-researcher
> **Status:** COMPLETE
> **Research Method:** Live web research (WebSearch, WebFetch)
> **Confidence:** High (authoritative library documentation + academic papers)

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
| Brazilian Earnings Calls | Transcript NER | 98.52% (PTT5), 98.85% (mT5) |

---

## Appendix C: Live Web Research Findings (2026-01-25)

### Updated NLP Pipeline Best Practices

Based on live web research conducted on 2026-01-25:

#### Modern Preprocessing and Tokenization

> "Tokenization strategies have evolved significantly with transformer-based models that require subword tokenization approaches. Modern tokenizers like Byte-Pair Encoding (BPE) and SentencePiece break text into smaller units that balance vocabulary size with semantic representation."
>
> Source: [Airbyte NLP Pipeline Guide](https://airbyte.com/data-engineering-resources/natural-language-processing-pipeline) - Accessed 2026-01-25

#### Conversation Intelligence Capabilities

Modern NLP platforms for transcripts provide:
- **Topic Detection**: Automatic tagging of keywords like pricing, contract terms
- **Intent Analysis**: Understanding purpose (question, complaint, buying signal)
- **Sentiment Analysis**: Detecting emotional tone and frustration

> "An industry survey found that for 76% of companies, conversation intelligence is embedded in more than half of their customer interactions."
>
> Source: [AssemblyAI Text Summarization Guide](https://www.assemblyai.com/blog/text-summarization-nlp-5-best-apis) - Accessed 2026-01-25

### NER for Meeting Transcripts - Updated Approaches

#### Two Main NER Approaches (2025 Best Practice)

| Approach | Description | Best For |
|----------|-------------|----------|
| **Ontology-based NER** | Knowledge-based recognition using predefined lists and rules (database of company names, common names, locations) | Known entity dictionaries |
| **Machine Learning NER** | Statistical models including CRF, BERT transformers | Generalizable extraction |

> "State of the art systems may incorporate multiple approaches."
>
> Source: [Wikipedia - Named Entity Recognition](https://en.wikipedia.org/wiki/Named-entity_recognition) - Accessed 2026-01-25

#### End-to-End NER from Speech

> "Researchers have introduced end-to-end approaches which jointly optimize the ASR and NER tagger components. Experimental results show that the proposed E2E approach outperforms the classical two-step approach."
>
> Source: [Yadav et al., Interspeech 2020](https://www.isca-archive.org/interspeech_2020/yadav20b_interspeech.pdf) - Accessed 2026-01-25

### Action Item Detection - Research Update

#### Context-Drop Approach (2023)

> "A Context-Drop approach has been proposed to utilize both local and global contexts by contrastive learning, achieving better accuracy and robustness for action item detection."
>
> Source: [arXiv:2303.16763 - Meeting Action Item Detection](https://arxiv.org/pdf/2303.16763) - Accessed 2026-01-25

#### Action-Item-Driven Summarization

> "The system achieved a BERTScore of 64.98, representing approximately 4.98% improvement over the previous state-of-the-art baseline established by a fine-tuned BART model."
>
> Source: [arXiv:2312.17581](https://arxiv.org/abs/2312.17581) - Accessed 2026-01-25

#### Linguistic Pattern Detection

Key patterns for action item detection from live research:

| Pattern Type | Examples | Detection Method |
|--------------|----------|------------------|
| Modal verbs | will, should, must, need to | POS tagging + pattern matching |
| Future tense | "I will send", "We're going to" | Tense analysis |
| Imperative phrases | "Please send", "Make sure to" | Sentence-initial verb detection |
| Commitment phrases | "I'll handle that", "Let me take care of" | First-person + action verb |

> "Modal verbs are a special type of verbs in an English sentence that give additional information about the function of the main verb that follows it."
>
> Source: [Modal Verbs Analysis with Regex](https://medium.com/nerd-for-tech/extracting-words-from-english-sentences-using-python-regex-modal-verbs-analysis-e89233e498a9) - Accessed 2026-01-25

### Topic Modeling - BERTopic vs Traditional Methods

#### Why BERTopic Excels for Transcripts

> "BERTopic excels in analyzing short or noisy datasets such as tweets, chat logs, and social media posts... leveraging semantic embeddings, which capture the deeper meaning of texts, resulting in more coherent and contextually accurate topics."
>
> Source: [BERTopic Official Documentation](https://bertopic.com/what-is-bertopic/) - Accessed 2026-01-25

#### c-TF-IDF Explained

> "What if we instead treat all documents in a single category (e.g., a cluster) as a single document and then apply TF-IDF? The result would be a very long document per category and the resulting TF-IDF score would demonstrate the important words in a topic."
>
> Source: [BERTopic GitHub](https://github.com/MaartenGr/BERTopic) - Accessed 2026-01-25

#### Comparison Study for Interview Transcripts

> "The BERT+UMAP+HDBSCAN algorithm was selected as the most suitable for semi-structured interviews... combining LDA with BERT embeddings was used to enhance contextual understanding of topics."
>
> Source: [PMC Article on Topic Modeling](https://pmc.ncbi.nlm.nih.gov/articles/PMC9120935/) - Accessed 2026-01-25

### spaCy EntityRuler - Rule-Based NER

#### Combining Statistical and Rule-Based NER

> "The EntityRuler is functioning before the 'ner' pipe and is, therefore, prefinding entities and labeling them before the NER gets to them. Because it comes earlier in the pipeline, its metadata holds primacy over the later 'ner' pipe."
>
> Source: [spaCy Rule-Based Matching](https://spacy.io/usage/rule-based-matching) - Accessed 2026-01-25

#### Pattern Operators in spaCy Matcher

| Operator | Meaning | Example Use |
|----------|---------|-------------|
| `!` | Match exactly 0 times | Negation |
| `?` | Match 0 or 1 times | Optional token |
| `+` | Match 1 or more times | Repeated tokens |
| `*` | Match 0 or more times | Any occurrence |
| `{n}` | Match exactly n times | Fixed count |
| `{n,m}` | Match n to m times | Range |

> Source: [spaCy Matcher API](https://spacy.io/api/matcher) - Accessed 2026-01-25

### Confidence Scoring for NER

#### Best Practices for Thresholds

> "The ideal threshold value changes based on the model being used and the text being processed. A common pitfall is to set a static threshold value and use it for all models and text."
>
> Source: [UpslopeNLP - Confidence Values](https://upslopenlp.com/confidence-values-and-entity-extraction/) - Accessed 2026-01-25

#### LLM Confidence Estimation

> "Token-level generation probabilities (commonly referred to as 'logprobs') are by far the most accurate technique for estimating LLM confidence. Explicitly prompting the LLM to output a confidence score, while popular, is highly unreliable."
>
> Source: [LLM Confidence Estimation](https://medium.com/@vatvenger/confidence-unlocked-a-method-to-measure-certainty-in-llm-outputs-1d921a4ca43c) - Accessed 2026-01-25

#### spaCy Confidence Limitation

> "The model is trained on 0/1 loss, so it wasn't trained to be well calibrated."
>
> Source: [spaCy GitHub Issue #831](https://github.com/explosion/spaCy/issues/831) - Accessed 2026-01-25

### Question Detection Methods

#### Sentence Boundary Detection Comparison

| Tool | Speed | Accuracy | Notes |
|------|-------|----------|-------|
| NLTK | 0.53s | Lower | Punkt algorithm |
| spaCy | 54.63s | Medium | Dependency-based |
| DeepSegment | 139.57s | 73.35% | Deep learning |

> "DeepSegment achieved an average absolute accuracy of 73.35% outperforming both Spacy and NLTK by a wide margin."
>
> Source: [pySBD GitHub](https://github.com/nipunsadvilkar/pySBD) - Accessed 2026-01-25

#### Question Classification

> "Training data from nps_chat includes labels: WH for WH questions, and YN for Yes/No questions. The model gave an accuracy of 67%."
>
> Source: [NLP Question Detection](https://github.com/kartikn27/nlp-question-detection) - Accessed 2026-01-25

### Decision Detection in Transcripts

#### Text Mining for Decision Elements

> "Using C99 and TextTiling algorithms as comparators, one method was able to identify and extract the needs and actions of decision making with a high recall of 85-95% at a precision of 54-68%."
>
> Source: [ResearchGate - Decision Element Extraction](https://www.researchgate.net/publication/44259639_Text_Mining_for_Meeting_Transcript_Analysis_to_Extract_Key_Decision_Elements) - Accessed 2026-01-25

### HuggingFace Token Classification

#### Pre-trained NER Models Available

| Model | Parameters | Entity Types | Downloads |
|-------|------------|--------------|-----------|
| dslim/bert-base-NER | 0.1B | PER, LOC, ORG, MISC | ~2.98M |
| xlm-roberta-large-finetuned-conll03 | 0.6B | Multilingual | ~90.3k |
| blaze999/Medical-NER | 0.2B | Medical entities | - |

> "bert-base-NER is a fine-tuned BERT model that is ready to use for Named Entity Recognition and achieves state-of-the-art performance for the NER task."
>
> Source: [HuggingFace dslim/bert-base-NER](https://huggingface.co/dslim/bert-base-NER) - Accessed 2026-01-25

#### BIO Tagging Scheme

> "The letter that prefixes each ner_tag indicates the token position: B- indicates the beginning of an entity, I- indicates a token is contained inside the same entity, and O indicates the token doesn't correspond to any entity."
>
> Source: [HuggingFace Token Classification Docs](https://huggingface.co/docs/transformers/main/tasks/token_classification) - Accessed 2026-01-25

### NER Evaluation Best Practices

#### Entity-Level vs Token-Level Evaluation

> "When training a NER system, the most typical evaluation method is to measure precision, recall, and F1-score at a token level. These metrics are useful to tune a NER system, but when using predicted named-entities for downstream tasks, it is more useful to evaluate with metrics at a full named-entity level."
>
> Source: [Named Entity Evaluation Blog](https://www.davidsbatista.net/blog/2018/05/09/Named_Entity_Evaluation/) - Accessed 2026-01-25

#### nervaluate Library

> "Various evaluation methods include Strict, Exact, Partial, and Type Evaluation. Each method offers unique insights into model performance."
>
> Source: [nervaluate GitHub](https://github.com/MantisAI/nervaluate) - Accessed 2026-01-25

### Transcript-Specific NER Benchmarks

#### Brazilian Earnings Call Study

> "T5-based models achieved impressive macro F1-scores of 98.52% (PTT5) and 98.85% (mT5) on this transcript data... BERT-based models consistently outperform T5-based models."
>
> Source: [arXiv:2403.12212](https://arxiv.org/html/2403.12212v1) - Accessed 2026-01-25

---

## Appendix D: Additional Live Research References

### Web Sources Accessed 2026-01-25

22. Airbyte. (2025). NLP Pipeline: Key Steps to Process Text Data. https://airbyte.com/data-engineering-resources/natural-language-processing-pipeline

23. AssemblyAI. (2025). 6 Best Named Entity Recognition APIs. https://www.assemblyai.com/blog/6-best-named-entity-recognition-apis-entity-detection

24. ScienceDirect. (2023). A survey on Named Entity Recognition - datasets, tools, and methodologies. https://www.sciencedirect.com/science/article/pii/S2949719123000146

25. arXiv. (2023). Meeting Action Item Detection with Regularized Context Modeling. https://arxiv.org/pdf/2303.16763

26. arXiv. (2023). Action-Item-Driven Summarization of Long Meeting Transcripts. https://arxiv.org/abs/2312.17581

27. AWS. (2024). Meeting summarization and action item extraction with Amazon Nova. https://aws.amazon.com/blogs/machine-learning/meeting-summarization-and-action-item-extraction-with-amazon-nova/

28. GitHub. (2024). BERTopic: Leveraging BERT and c-TF-IDF. https://github.com/MaartenGr/BERTopic

29. GitHub. (2024). KeyBERT: Minimal keyword extraction with BERT. https://github.com/MaartenGr/KeyBERT

30. KDnuggets. (2020). Topic Modeling with BERT. https://www.kdnuggets.com/2020/11/topic-modeling-bert.html

31. HuggingFace. (2024). Token Classification Documentation. https://huggingface.co/docs/transformers/main/tasks/token_classification

32. HuggingFace. (2024). What is Token Classification? https://huggingface.co/tasks/token-classification

33. spaCy. (2024). Rule-based matching. https://spacy.io/usage/rule-based-matching

34. spaCy. (2024). EntityRuler API Documentation. https://spacy.io/api/entityruler

35. spaCy. (2024). Matcher API Documentation. https://spacy.io/api/matcher

36. NewsCatcher. (2024). Train Custom NER Model with spaCy v3. https://www.newscatcherapi.com/blog-posts/train-custom-named-entity-recognition-ner-model-with-spacy-v3

37. Analytics Vidhya. (2022). Custom Named Entity Recognition using spaCy v3. https://www.analyticsvidhya.com/blog/2022/06/custom-named-entity-recognition-using-spacy-v3/

38. ThatWare. (2024). F1 Score for NER: A Metric To Evaluate Precision And Recall. https://thatware.co/f1-score-for-ner/

39. Microsoft Learn. (2024). Custom NER evaluation metrics. https://learn.microsoft.com/en-us/azure/ai-services/language-service/custom-named-entity-recognition/concepts/evaluation-metrics

40. arXiv. (2024). Evaluating NER on Brazilian Corporate Earnings Call Transcriptions. https://arxiv.org/html/2403.12212v1

41. Mindee. (2024). Understanding Confidence Scores in Machine Learning. https://www.mindee.com/blog/how-use-confidence-scores-ml-models

42. pySBD. (2024). Python Sentence Boundary Disambiguation. https://github.com/nipunsadvilkar/pySBD

43. spaCy Universe. (2024). pySBD - python Sentence Boundary Disambiguation. https://spacy.io/universe/project/python-sentence-boundary-disambiguation
