# S-002 Devil's Advocate Review

## Document Sections

| Section | Purpose |
|---------|---------|
| [Strategy Overview](#strategy-overview) | S-002 protocol and deliverable context |
| [Issue Register](#issue-register) | Numbered issues with priority, quote, weakness, fix |
| [Dimension Scores](#dimension-scores) | Six-dimension S-014 scoring with weights |
| [Additional Criteria](#additional-criteria) | LLM-tell and voice authenticity scoring |
| [Composite Score](#composite-score) | Weighted total and band classification |

---

## Strategy Overview

- **Strategy:** S-002 Devil's Advocate
- **Deliverable:** `drafts/draft-5-llm-tell-clean.md` (ART-001 structured prompting article)
- **Iteration:** 1-v2
- **Reviewer posture:** Skeptical practitioner with LLM experience; hostile to hand-waving, demands precision, tests every claim against the state of the art.

---

## Issue Register

### Issue 1: "Fluency-competence gap" citation claim is unverifiable

**Priority:** HIGH

**Quote:** *"It's called the 'fluency-competence gap,' a pattern documented across model families since GPT-3."*

**Weakness:** This term is presented as established nomenclature with a provenance claim ("since GPT-3"). In practice, "fluency-competence gap" is not a standardized term in the research literature. The phenomenon is real, documented under various names (calibration, overconfidence, sycophancy, hallucination as fluent nonsense), but asserting a canonical label with a historical anchor that readers cannot verify undermines the article's credibility with anyone who searches for it. A knowledgeable practitioner will Google this, find nothing named exactly that, and discount the article.

**Fix:** Either (a) drop the naming claim and describe the phenomenon directly: "This disconnect between how competent the output sounds and how competent it actually is shows up across every model family," or (b) cite a specific paper and use its terminology (e.g., reference Kadavath et al. 2022 on calibration, or Perez et al. 2022 on sycophancy). Option (a) is more in voice; option (b) is more rigorous.

---

### Issue 2: "Lost in the middle" citation is specific but the claim around it is overstated

**Priority:** HIGH

**Quote:** *"Research has shown that model performance on retrieval and reasoning tasks degrades as context length grows. Liu et al. (2023) documented the 'lost in the middle' effect, where instructions buried in a long conversation history get progressively less attention than content at the beginning or end."*

**Weakness:** Two problems. First, Liu et al. (2023) specifically documented that models struggle to retrieve information positioned in the *middle* of long contexts, not that performance degrades monotonically with context length. The article conflates positional bias with length degradation. They are related but distinct phenomena. Second, the article uses this to justify starting a new conversation. But the actual Liu et al. finding suggests the issue is positional, not volumetric. A long planning conversation puts the final plan at the *end* of the context, which is precisely where models attend best according to the same paper. The citation actually weakens the argument it is meant to support.

**Fix:** Separate the two claims. The context-length-degrades-performance claim is supported by other work (e.g., Anthropic's own long-context evaluations, or Hsieh et al. 2024 on RULER benchmarks). The Liu et al. citation is better used to argue that important instructions should be placed at the beginning or end of a prompt, not buried in middle turns of conversation. Then reframe the two-session argument around the stronger reason: role clarity and eliminating planning noise, which the article already gives as the second reason and which does not need a citation to be persuasive.

---

### Issue 3: "Training-data gravity" is evocative but technically imprecise

**Priority:** MEDIUM

**Quote:** *"Real sources, not training-data gravity. The evidence constraint forces grounding."*

**Weakness:** The article uses "training-data gravity" as if telling an LLM to use "real sources, not training data" causes the model to bypass its learned distributions. It does not. The model always generates from its learned distributions. Telling it to cite real sources increases the probability that it retrieves and presents verifiable claims, but the mechanism is probabilistic completion, not some toggle between "training data mode" and "real source mode." A practitioner who understands how transformers work will see this as a simplification that borders on inaccuracy. The Level 3 prompt example also says "using real sources, not training data," which a reader might interpret as the model having internet access, which it may or may not depending on the tool configuration.

**Fix:** Clarify the mechanism. Something like: "The evidence constraint changes what completions the model considers acceptable. It doesn't stop the model from using training data. It makes the model more likely to surface specific, verifiable claims rather than generic patterns." Also, the Level 3 example prompt should clarify whether the model has search/retrieval tools or is working from its training data. If the latter, "real sources" means "cite specific papers and let me verify," not "go fetch from the internet."

---

### Issue 4: The "error compounding" claim lacks mechanism or evidence

**Priority:** HIGH

**Quote:** *"once weak output enters a multi-phase pipeline, it compounds. Each downstream phase treats the previous output as ground truth and adds its own layer of confident-sounding polish. By phase three, the output looks authoritative. The errors are load-bearing."*

**Weakness:** This is presented as an inevitable, well-understood dynamic. But the article provides no citation, no mechanism description beyond analogy, and no empirical grounding. A skeptical reader asks: How much does error compound? Is this measured? The claim "by phase three" implies a specific degradation curve but provides none. Google DeepMind's work on multi-agent error amplification (which the Jerry framework itself cites in agent-development-standards.md with a 1.3x amplification figure for structured handoffs vs. 17x for uncoordinated ones) would provide concrete grounding here. Without it, this reads as assertion dressed as analysis.

**Fix:** Either cite the error amplification research and give a concrete figure, or soften the claim: "Weak output in early phases tends to propagate and get harder to detect as downstream phases build on it." The current framing is too confident for the evidence provided.

---

### Issue 5: The article presupposes tool-enabled models in Level 3 without saying so

**Priority:** MEDIUM

**Quote:** *"Do two things in parallel: gap analysis on this repo, and research the top 10 industry frameworks using real sources, not training data."*

**Weakness:** The Level 3 prompt asks the model to do "gap analysis on this repo" (implying file access) and "research using real sources" (implying search/retrieval). These are tool-use capabilities that not all LLM deployments support. A reader using the ChatGPT web interface, a local Llama model, or an API call without tools will read this prompt, try it, get hallucinated repo analysis and fabricated citations, and conclude the article is wrong. The article claims universality in its "Why This Works on Every Model" section but the Level 3 example requires capabilities that are not universal.

**Fix:** Add a brief note either in Level 3 or in the "Why This Works on Every Model" section: "Level 3 assumes the model has access to your files and can search for sources. If you're in a plain chat interface, skip the parallel research step and feed the model your repo contents directly." This preserves the principle while being honest about tool requirements.

---

### Issue 6: "Every dimension you leave unspecified, the model fills with the most generic probable completion" is an oversimplification

**Priority:** MEDIUM

**Quote:** *"Every dimension you leave unspecified, the model fills with the most generic probable completion. That's not laziness. It's probability distributions."*

**Weakness:** This makes it sound like the model always picks the single most probable token at every step, which is mode-collapse decoding (greedy or very low temperature). In practice, models use temperature > 0 and sampling strategies that introduce deliberate variance. The output is not "the most generic probable completion." It is *a sample from the distribution that skews toward common patterns.* The distinction matters: the reader might wonder why the same vague prompt gives different outputs each time if the model always picks "the most generic" option. This also ignores that system prompts, RLHF tuning, and safety training already constrain the default distribution substantially.

**Fix:** Adjust to: "the model samples from a distribution that skews toward whatever patterns were most common in training data for that kind of request." Or more simply: "the model defaults to whatever feels most typical." The current phrasing implies determinism that does not exist.

---

### Issue 7: "Self-assessment is itself a completion task" deserves more examination

**Priority:** LOW

**Quote:** *"Self-assessment is itself a completion task, and research on LLM self-evaluation consistently shows favorable bias."*

**Weakness:** The claim "research on LLM self-evaluation consistently shows favorable bias" is stated as settled consensus. It is largely true (Zheng et al. 2023 on LLM-as-judge, Anthropic's own work on sycophancy) but "consistently" is strong. There is counter-evidence showing that with specific rubrics and structured evaluation criteria, self-assessment reliability improves substantially (which is in fact what the Jerry framework's S-014 strategy operationalizes). The article's own approach at Level 3 asks the model to "critique your own work" and "score yourself," which seems to contradict the claim that self-assessment is unreliable. The article does add human gates as a backstop, but the tension between "self-critique is unreliable" and "ask the model to self-critique" is unresolved.

**Fix:** Acknowledge the tension explicitly: "Self-critique is unreliable on its own, but it's useful as a first filter. The model will catch some of its own errors. It won't catch all of them. That's what the human gates are for." This makes the multi-layered approach coherent rather than contradictory.

---

### Issue 8: The McConkey framing is load-bearing but under-developed

**Priority:** MEDIUM

**Quote:** *"Think of it like big-mountain skiing. Shane McConkey, legendary freeskier, the guy who'd ski a cliff in a banana suit and win competitions doing it. He had a rule. He looked like he was winging it. He wasn't."*

**Weakness:** The article introduces McConkey as if the reader does not know who he is ("legendary freeskier, the guy who'd..."), then the article is published under a McConkey persona voice. This creates a dissonance: the narrator is explaining who McConkey is to the reader, but the narrator *is* (or channels) McConkey. The opening reads like a third person introducing McConkey rather than McConkey himself speaking. A reader who knows the persona will find this odd. A reader who does not know the persona will be confused about who is talking.

**Fix:** Either own the first person throughout ("I looked like I was winging it. I wasn't.") or move the McConkey introduction into an author bio/sidebar and let the voice carry the persona without the self-introduction. The current split-perspective weakens both the framing device and the voice.

---

### Issue 9: The "chain-of-thought" reference in "Why This Works" is too casual

**Priority:** LOW

**Quote:** *"This is a well-documented finding across prompt engineering research, from chain-of-thought prompting to structured role-task-format patterns."*

**Weakness:** Chain-of-thought prompting (Wei et al. 2022) is about eliciting intermediate reasoning steps, not about instruction specificity. It is related but not the same thing. Grouping it with "structured role-task-format patterns" as evidence for "specific instructions improve output" blurs the distinction between instructing the model *what to produce* and instructing the model *how to reason*. A practitioner who knows the CoT literature will see this as a loose citation.

**Fix:** Replace or clarify: "from instruction-following benchmarks to structured role-task-format patterns." Or if chain-of-thought is worth keeping, explain the connection: "Even prompting techniques like chain-of-thought, which add structure to the model's reasoning process, demonstrate that constraining how the model works improves what it produces."

---

### Issue 10: Numbered principles section uses bolding pattern that reads as LLM-generated

**Priority:** MEDIUM

**Quote:** Lines 73-77 use the pattern `**1. Phrase.**` / `**2. Phrase.**` / `**3. Phrase.**` followed by explanatory text.

**Weakness:** The bold-numbered-principle pattern with a short imperative phrase followed by elaboration is one of the most common LLM output structures. It appears in virtually every ChatGPT and Claude response that summarizes key points. While the *content* is not generic, the *formatting pattern* is a strong LLM tell. A reader sensitized to AI-generated content (which is the audience reading an article about LLM prompting) will pattern-match this immediately.

**Fix:** Break the parallel structure. Make one a question, one a statement, one a conditional. Or fold the principles into prose paragraphs instead of a numbered list. Or use a different structural device entirely (e.g., a table, a callout, a dialogue). The goal is to disrupt the predictable bold-number-phrase-explain pattern.

---

### Issue 11: "I dare you" closing is performative risk

**Priority:** LOW

**Quote:** *"Do that once and tell me it didn't change the output. I dare you."*

**Weakness:** Depending on audience, this either lands as authentic McConkey bravado or as cringe. The article has earned enough credibility by this point to let the practical advice stand without the challenge. "I dare you" is also a common LinkedIn-influencer and YouTube-creator ending, which might undercut the voice authenticity for readers who associate it with that genre.

**Fix:** This is a judgment call, not a defect. If the persona mandate is strong, keep it. If the audience is primarily technical practitioners, consider ending with the practical instruction and letting the McConkey callback ("The wild was the performance. The preparation was the foundation.") serve as the closer. The dare dilutes rather than strengthens the landing.

---

## Dimension Scores

| Dimension | Weight | Score | Rationale |
|-----------|--------|-------|-----------|
| Completeness | 0.20 | 0.82 | Covers the three levels well. Missing: tool-use prerequisites for Level 3 (Issue 5), no mention of temperature/sampling which is relevant to the probability-distribution argument, no discussion of when structured prompting is overkill (is there a Level 0?). The "Why This Works on Every Model" section attempts universality but does not address model-specific limitations. |
| Internal Consistency | 0.20 | 0.78 | Self-critique is presented as unreliable (Issue 7) then recommended as a technique. McConkey is introduced in third person by a McConkey-voiced narrator (Issue 8). "Most generic probable completion" implies determinism; "every model" claims universality that Level 3 does not support (Issue 5). The Liu et al. citation contradicts its own argument (Issue 2). These are not fatal, but they create friction for a careful reader. |
| Methodological Rigor | 0.20 | 0.74 | The three-level framework is sound pedagogically. However, the technical claims lean on assertions more than evidence (Issues 1, 4, 6). The one specific citation (Liu et al.) is misapplied (Issue 2). The error-compounding claim is unsupported (Issue 4). The article asks readers to trust its authority without providing the kind of evidence it tells readers to demand from LLMs. |
| Evidence Quality | 0.15 | 0.68 | One named citation (Liu et al. 2023) that is partially misapplied. One unnamed term ("fluency-competence gap") presented as established. Zero links, zero other named papers. For an article that tells readers to demand citations from LLMs, the article itself provides almost none. This is not hypocrisy per se, since it is a practitioner article, not an academic paper, but the gap between what it preaches and what it practices is noticeable. |
| Actionability | 0.15 | 0.90 | Strong. The three levels are clear, progressive, and immediately usable. The checklist at the end is practical. The two-session pattern is concrete. The Level 2 and Level 3 example prompts are copy-pasteable. This is the article's greatest strength. |
| Traceability | 0.10 | 0.55 | Minimal. One citation. No links. No references section. No "further reading." The article makes several claims that trace to specific research but does not provide the trail. For an mkdocs site where readers might want to go deeper, this is a gap. |

---

## Additional Criteria

| Criterion | Score | Rationale |
|-----------|-------|-----------|
| LLM-Tell Detection | 0.78 | Substantial improvement from earlier drafts. Remaining tells: the bold-numbered-principles pattern (Issue 10) is a strong structural tell. The three-parallel-bullet format in "Why This Works" (lines 65-67) follows the classic LLM three-bullet pattern. The phrase "well-documented finding across prompt engineering research" (line 65) is classic hedging-via-authority without citation. The word "systematic" (line 19) in "That's not a coin flip. It's systematic, and it's predictable" follows the LLM pattern of paired adjectives for emphasis. None of these are fatal individually, but together they create a cumulative signal. |
| Voice Authenticity | 0.80 | The voice is genuinely strong in places. "Point Downhill and Hope" as a heading is excellent. "You don't need a flight plan for the bunny hill" is authentic. The opening paragraph reads natural. The closing dare feels real. Where it drops: the technical explanation paragraphs (lines 17-19, 27, 55-56) shift into a lecture-mode voice that is competent but not distinctively McConkey. McConkey's voice is characterized by technical precision delivered through irreverence and physical metaphor. The middle sections deliver technical precision through straightforward exposition, which is any good technical writer, not specifically McConkey. |

---

## Composite Score

| Dimension | Weight | Score | Weighted |
|-----------|--------|-------|----------|
| Completeness | 0.20 | 0.82 | 0.164 |
| Internal Consistency | 0.20 | 0.78 | 0.156 |
| Methodological Rigor | 0.20 | 0.74 | 0.148 |
| Evidence Quality | 0.15 | 0.68 | 0.102 |
| Actionability | 0.15 | 0.90 | 0.135 |
| Traceability | 0.10 | 0.55 | 0.055 |
| **Weighted Composite** | **1.00** | | **0.760** |

**Band:** REJECTED (< 0.85)

**Summary:** The article is structurally sound, highly actionable, and has a distinctive voice that mostly works. Its critical weaknesses are in evidence quality and methodological rigor. It makes technical claims that it does not support, misapplies its one named citation, and preaches a standard of evidence that it does not practice itself. The internal consistency issues (self-critique contradiction, McConkey perspective split, universality claim vs. tool-dependent examples) create friction that a careful reader will notice. The LLM tells are substantially reduced but not eliminated. The voice is strong in the informal sections and drops into generic-technical-writer mode in the expository sections.

**Top three priorities for revision:**
1. Fix the Liu et al. citation usage or replace it with a correctly applied reference (Issue 2, HIGH).
2. Either ground "fluency-competence gap" in real terminology or drop the naming claim (Issue 1, HIGH).
3. Add a tool-use prerequisite note for Level 3 and reconcile the universality claim (Issue 5, MEDIUM).
