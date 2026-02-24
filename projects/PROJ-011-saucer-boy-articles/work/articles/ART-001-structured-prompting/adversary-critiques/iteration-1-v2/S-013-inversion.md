---

**STRATEGY:** S-013 Inversion Technique
**DELIVERABLE:** `draft-5-llm-tell-clean.md` -- Saucer Boy article on structured LLM prompting (post-iteration-3, LLM-tell cleanup pass)
**DATE:** 2026-02-23
**REVIEWER:** adv-executor (S-013)
**PRIOR VERSION:** iteration-1/S-013-inversion.md (scored against draft-1)
**CONTEXT:** This draft passed the quality gate at 0.938 in iteration-3 scoring, then received an LLM-tell cleanup pass. This inversion analysis examines the cleaned draft for residual failure modes and new risks introduced by revisions.

---

## INVERSION PROTOCOL

Instead of "how do we make this article good?" -- **"how would we make this article BAD?"**

Six inversion lenses applied:
1. What would make this article fail with its target audience?
2. What would make it technically wrong?
3. What would make the voice feel fake?
4. What would make it obviously AI-generated?
5. What would make it boring or forgettable?
6. For each: does the current draft avoid this pitfall? Where does it come close? Margin of safety?

---

## INVERSION 1: How Would We Make This Article FAIL With Its Target Audience?

### Recipe for Failure

To make this fail with the target audience (developers using LLMs, ranging from beginner to intermediate), you would:

- **Lecture without empathy.** Open with "you're doing it wrong" energy, making the reader defensive before you deliver the insight.
- **Present only the maximum-effort version.** Show the full orchestration prompt and imply that anything less is inadequate.
- **Use framework-specific jargon the reader cannot act on.** Reference internal tools, thresholds, and processes that require a system the reader does not have.
- **Assume the reader already agrees with the premise.** Skip the "why should I care" step and jump to "here's what to do."
- **Make the advice feel like homework.** Present structured prompting as a chore rather than an advantage.

### Does the Current Draft Avoid This?

| Failure Vector | Status | Evidence | Margin |
|---|---|---|---|
| Lecture without empathy | AVOIDED | Line 3: "this trips up everybody, so don't feel singled out" -- positions the reader as normal, not wrong | SAFE. The opening is warm without being sycophantic. |
| Maximum-effort only | AVOIDED | Three-level framework (Levels 1-3) gives graduated entry. Line 91: "You don't have to go full orchestration on day one. Even adding 'show me your plan before executing, and cite your sources' to any prompt will change the output." | SAFE. The on-ramp was a key fix from iteration-1. |
| Framework-specific jargon | AVOIDED | No Jerry-specific terminology remains. No "adversarial review," "0.92 threshold," "orchestration.yaml," or "dispatch to agents." Level 3 prompt example uses generic structured prompting language. | SAFE. This was one of the strongest fixes from draft-1 to draft-2. |
| Assumes agreement | MOSTLY AVOIDED | Lines 5-6 establish the reader's instinct was right, then reframe the gap. Lines 15-19 explain *why* vague prompting produces bad output (the mechanism, not just the assertion). | MODERATE MARGIN. The article does not include a concrete before/after demonstration showing the *same prompt* at two levels producing different quality output. The reader is told the difference exists; they are not shown it. See [Residual Risk RR-01](#residual-risks). |
| Advice feels like homework | AVOIDED | McConkey framing ("looked like he was winging it -- he wasn't") reframes structure as the expert move, not the bureaucratic move. The checklist at lines 83-89 is five items, not fifteen. | SAFE. |

---

## INVERSION 2: How Would We Make This Article TECHNICALLY WRONG?

### Recipe for Technical Failure

To make this technically wrong, you would:

- **Describe LLMs as deterministic calculators** that always produce the same output from the same input.
- **Claim context windows are physical limits** that cannot change.
- **Assert structured prompting guarantees good output.**
- **Mischaracterize the attention mechanism** (e.g., "LLMs process tokens linearly").
- **Claim self-critique is unreliable** without acknowledging that it has improved with newer techniques.

### Does the Current Draft Avoid This?

| Failure Vector | Status | Evidence | Margin |
|---|---|---|---|
| LLMs as deterministic | AVOIDED | "most probable generic response from their training distribution" (line 17) correctly frames output as probabilistic | SAFE |
| Context windows as physics | AVOIDED | "hard engineering constraints -- determined by architecture, memory, and compute tradeoffs. They're not permanent" (line 63) | SAFE. This was a critical fix from draft-1. |
| Structured prompting guarantees | AVOIDED | Three-level framework presents it as improving odds, not guaranteeing outcomes. No absolute promises. | SAFE |
| Attention mechanism mischaracterized | NOT APPLICABLE | Draft does not describe the attention mechanism at a technical level. It stays at the behavioral level ("structured instructions focus the model's attention on relevant context," line 27). This is imprecise but not wrong. | SAFE. Behavioral-level description is appropriate for the audience. |
| Self-critique reliability | CLOSE MARGIN | Line 42: "models can't reliably self-assess at scale. Self-assessment is itself a completion task, and research on LLM self-evaluation consistently shows favorable bias." This is directionally correct but the "can't reliably" framing is slightly absolute. Self-assessment has improved (e.g., constitutional AI, critique-revision loops). | LOW MARGIN. The claim is not technically wrong but is stated more categorically than the evidence supports. See [Residual Risk RR-02](#residual-risks). |

**New technical claim audit (introduced since draft-1):**

| Claim | Location | Accuracy |
|---|---|---|
| "fluency-competence gap -- a pattern documented across model families since GPT-3" | Line 19 | ACCURATE. Recognized phenomenon. "Since GPT-3" temporal grounding is appropriate. |
| "Liu et al. (2023)" lost-in-the-middle effect | Line 55 | ACCURATE. Real paper, correctly described. |
| "structured instructions focus the model's attention on relevant context and narrow the space of acceptable completions" | Line 27 | ACCURATE. Correct high-level description of how constraining prompts work. |
| "Every dimension you leave unspecified, the model fills with the most generic probable completion. That's not laziness. It's probability distributions." | Line 73 | ACCURATE. Correct characterization of autoregressive model defaults. |
| "research on LLM self-evaluation consistently shows favorable bias" | Line 42 | ACCURATE but unattributed. No named source. Directionally correct. Acceptable for genre. |

---

## INVERSION 3: How Would We Make the Voice Feel FAKE?

### Recipe for Fake Voice

To make the Saucer Boy / McConkey voice feel fake, you would:

- **Overuse catchphrases.** Repeat "bro," "send it," or skiing slang every paragraph until it reads like a costume.
- **Mix registers inconsistently.** Alternate between casual bro-speak and academic prose within the same paragraph.
- **Use the persona as decoration.** The skiing metaphor appears in the intro and conclusion but is absent from the substance, creating a veneer effect.
- **Force irrelevant analogies.** Stretch the skiing metaphor to cover technical points where it does not naturally apply.
- **Sound like an LLM imitating a persona.** Use hedging phrases, topic-sentence-evidence-conclusion paragraph structure, and over-scaffolded transitions.

### Does the Current Draft Avoid This?

| Failure Vector | Status | Evidence | Margin |
|---|---|---|---|
| Overused catchphrases | AVOIDED | McConkey appears in lines 7, 93. "Banana suit" once. No ski jargon beyond the framing metaphor. | SAFE. Restraint is well-calibrated. |
| Inconsistent register | MOSTLY AVOIDED | The voice is consistently conversational-technical: informal sentence structure carrying precise technical content. | MODERATE MARGIN. Lines 55-57 shift to a more formal academic register ("Liu et al. (2023) documented the 'lost in the middle' effect, where instructions buried in a long conversation history get progressively less attention than content at the beginning or end"). This is the most academic-sounding sentence in the piece and it reads slightly different from the surrounding voice. However, the preceding sentence ("Research has shown that model performance on retrieval and reasoning tasks degrades as context length grows") serves as a transition buffer. See [Residual Risk RR-03](#residual-risks). |
| Persona as decoration | AVOIDED | The skiing metaphor is structural, not decorative. It maps to the core argument: Level 1 = point downhill and hope, Level 3 = full orchestration = McConkey-level preparation behind apparent ease. The metaphor does real argumentative work. | SAFE |
| Forced analogies | AVOIDED | The skiing metaphor stays in its lane (preparation vs. improvisation). It does not stretch to cover technical details like token budgets or self-assessment bias. Technical content is explained on its own terms. | SAFE |
| LLM imitating persona | CLOSE MARGIN | See [Inversion 4](#inversion-4-how-would-we-make-this-article-obviously-ai-generated) for detailed analysis. | See below. |

---

## INVERSION 4: How Would We Make This Article OBVIOUSLY AI-GENERATED?

### Recipe for Detectable AI Generation

To make this obviously AI-generated, you would include:

- **Hedging qualifiers:** "It's worth noting," "It's important to understand," "Let's explore"
- **Topic-sentence paragraphs:** Every paragraph opens with a summary sentence followed by supporting evidence, like a five-paragraph essay
- **Transition scaffolding:** "Now that we've covered X, let's look at Y," "With that in mind," "This brings us to"
- **List-heavy structure:** Reliance on bullet points as the primary organizational tool rather than prose
- **Symmetrical structure:** Each section has the same number of sub-points, same paragraph length, same cadence
- **Empty emphasis:** "This is crucial," "This is the key insight," "This cannot be overstated"
- **Passive authority:** "It has been shown that," "Research indicates," "Studies suggest"

### Does the Current Draft Avoid This?

| LLM-Tell Pattern | Present? | Evidence | Severity |
|---|---|---|---|
| Hedging qualifiers | NO | No "it's worth noting," "it's important to," or "let's explore" anywhere. | CLEAR |
| Topic-sentence paragraphs | MOSTLY NO | Most paragraphs open with conversational leads ("Alright, this trips up everybody," "Same applies here," "You don't just fire the prompt"). Line 45 ("One more thing that bites hard") is a natural conversational opener. | ONE INSTANCE: Line 63 ("Context windows are hard engineering constraints") reads as a topic sentence followed by qualification. But the paragraph immediately breaks from essay structure with the parenthetical growth data. LOW RISK. |
| Transition scaffolding | NO | Section transitions are abrupt and natural: "Same applies here. Three levels" (line 9). "You don't just fire the prompt" (line 49). No "now let's look at" or "with that in mind." | CLEAR |
| List-heavy structure | PARTIAL | Level 3 breakdown (lines 39-44) and the three principles (lines 72-77) use bullets. But these are functional decompositions of complex prompts, not organizational crutches. The majority of the article is prose. | LOW RISK. Lists serve genuine structural purpose. |
| Symmetrical structure | NO | Levels 1, 2, 3 are different lengths (7 lines, 9 lines, 14 lines). The three principles section varies in length per principle. The two-session pattern is its own asymmetric section. | CLEAR |
| Empty emphasis | NO | No "this is crucial," "this cannot be overstated," or "this is the key insight." Emphasis is earned through argument, not asserted. | CLEAR |
| Passive authority | MOSTLY NO | Most claims use active voice: "The LLM reads that and goes" (line 15), "You push back" (line 50). One instance of passive authority: "Research has shown that model performance..." (line 55). This is the expected register for citing external work. | ONE INSTANCE. Acceptable for citation context. |

### LLM-Tell Composite Assessment

**Score: 0.88**

The draft is substantially clean of LLM-tell patterns. The post-iteration cleanup pass was effective. Two residual signals:

1. The Liu et al. citation paragraph (lines 55-57) is the most "written by an AI being careful" moment in the piece. The construction "Research has shown that... Liu et al. (2023) documented the... effect, where..." follows the academic-citation-in-casual-prose pattern that LLMs default to when asked to cite sources in a conversational voice. A human writer might say: "You've probably noticed long conversations go sideways. There's a name for this -- researchers call it 'lost in the middle' (Liu et al., 2023). Basically, stuff in the middle of a long chat gets ignored."

2. Line 27: "That's how these models work at the architecture level. Structured instructions focus the model's attention on relevant context and narrow the space of acceptable completions." The second sentence reads like a technical explainer sentence injected into a conversational paragraph. A Saucer Boy delivery might compress this: "You narrowed the blast radius. The model stops guessing and starts working within your constraints."

Neither is a dealbreaker. Both are marginal. The overall voice fidelity is strong.

---

## INVERSION 5: How Would We Make This Article BORING OR FORGETTABLE?

### Recipe for Boring

To make this boring, you would:

- **Open with definitions.** "Structured prompting is a technique for improving LLM output quality by..."
- **Remove all personality.** Strip the McConkey metaphor, the conversational asides, the "I dare you."
- **Present information without stakes.** Explain the technique without ever making the reader feel the consequence of not using it.
- **Use only abstract examples.** "Consider a scenario where a user prompts an LLM..."
- **End with a summary.** "In conclusion, structured prompting improves LLM output quality through three mechanisms."

### Does the Current Draft Avoid This?

| Failure Vector | Status | Evidence | Margin |
|---|---|---|---|
| Opens with definitions | AVOIDED | Opens with "Alright, this trips up everybody" -- conversational, empathetic, immediately engaging | SAFE |
| No personality | AVOIDED | McConkey framing, "banana suit," "point downhill and hope," "I dare you" closer. The voice is distinctive and consistent. | SAFE |
| No stakes | AVOIDED | Lines 44-45 describe compounding error ("garbage in, polished garbage out, and you can't tell the difference until something breaks"). This creates consequence. Lines 15-17 describe the "dangerous part" of fluent-but-wrong output. | SAFE |
| Abstract examples only | MOSTLY AVOIDED | Level 1, 2, 3 prompts are concrete, quotable examples. The two-session pattern gives a specific workflow. | MODERATE MARGIN. All examples are prompts-about-prompts. There is no concrete domain example (e.g., "here's what happened when someone used Level 1 vs. Level 3 for a code review"). The reader sees the technique but not a real outcome. See [Residual Risk RR-04](#residual-risks). |
| Ends with summary | AVOIDED | Ends with "I dare you" -- a challenge, not a recap. The checklist (lines 83-89) provides the actionable summary; the closing paragraphs provide the emotional resonance. | SAFE. This is one of the article's strongest moments. |

---

## INVERSION 6: Margin of Safety Assessment

### Residual Risks

#### RR-01: No Before/After Demonstration [MEDIUM]

**Location:** Structural gap (not a specific line)
**Issue:** The article asserts that structured prompting produces better output but never shows the difference. A reader at Level 1 is told they should move to Level 2, but they never see what Level 1 output looks like versus Level 2 output for the same question. The article argues by assertion and mechanism rather than by demonstration.
**Margin:** MEDIUM. The mechanism explanation (probability distributions, fluency-competence gap) is convincing to analytically-minded readers. But for experientially-minded readers ("show me, don't tell me"), this is a gap.
**Recommendation:** Consider adding a 2-3 sentence illustration: "Ask any LLM 'evaluate this repo against industry frameworks.' Then ask the same LLM the Level 2 version. Compare the outputs. I'll wait." This turns the reader's own experience into the evidence.

#### RR-02: Self-Assessment Claim Slightly Overcategorical [LOW]

**Location:** Line 42
**Issue:** "models can't reliably self-assess at scale" is stated without qualification. Self-assessment has improved with techniques like constitutional AI and calibrated confidence scoring. The follow-up sentence ("research on LLM self-evaluation consistently shows favorable bias") is more accurate but the opening claim is slightly stronger than warranted.
**Margin:** LOW. This was flagged in iteration-2 verification (C-10) and addressed. The current form is directionally correct and functionally useful for the audience. Pushing for more qualification would harm readability without meaningful accuracy gain.
**Recommendation:** No change required. Genre-appropriate as-is.

#### RR-03: Citation Paragraph Register Shift [LOW]

**Location:** Lines 55-57
**Issue:** The Liu et al. citation paragraph is the one moment where the voice shifts toward academic register. This is inherent in the task (citing a paper in a conversational piece) but creates a detectable seam.
**Margin:** LOW. The surrounding sentences maintain conversational register, and the citation is brief (one sentence). A reader will not notice this as a voice break; it reads as the author being precise about a specific claim.
**Recommendation:** Optional micro-edit: "Liu et al. (2023) documented the 'lost in the middle' effect" could become "There's a documented phenomenon -- researchers call it 'lost in the middle' (Liu et al., 2023) --" to keep the conversational frame while preserving the citation. This is a polish item, not a defect.

#### RR-04: No Concrete Domain Outcome Example [LOW]

**Location:** Structural gap
**Issue:** All prompt examples are about prompting itself (meta-level). No example shows the technique applied to a specific domain task (code review, architecture evaluation, documentation generation) with observable outcome difference.
**Margin:** LOW. The meta-level examples work because the audience (LLM users) can immediately test them. A domain-specific example might actually narrow the audience ("I don't do code reviews, so this doesn't apply to me").
**Recommendation:** No change required. The meta-level approach is a sound editorial choice for a general audience article.

---

## PRIOR FAILURE MODE DISPOSITION

Tracking which iteration-1 failure modes were addressed:

| FM | Description | Status in draft-5 | Evidence |
|---|---|---|---|
| FM-01 | "Works for me" dismissal -- no acknowledgment vague prompting can work | FIXED | Line 29: "For a lot of work, this is enough. You don't need a flight plan for the bunny hill." Line 91: "You don't have to go full orchestration on day one." |
| FM-02 | Overwhelming complexity causes rejection | FIXED | Three-level framework with graduated entry. Lines 91-92 provide explicit on-ramp. Checklist at lines 83-89 is five items. |
| FM-03 | "This only works with Jerry" objection | FIXED | All Jerry-specific terminology removed. Prompt examples are framework-agnostic. Line 69: "The implementation syntax varies. XML tags for Claude, markdown for GPT, whatever the model prefers." |
| FM-04 | Context clearing not universally available | FIXED | Lines 51-52: "Start a new conversation. Copy the finalized plan into a fresh chat. Prompt with one clean instruction." Practical mechanics explained. |
| FM-05 | Context degradation claim unsubstantiated | FIXED | Lines 55-56: Liu et al. (2023) citation with specific finding description. |
| FM-06 | No acknowledgment of when structured prompting is counterproductive | FIXED | Lines 29, 91 acknowledge that Level 2 is sufficient for most work. Implicit: Level 1 is fine for simple tasks. |
| FM-07 | Plan review chicken-and-egg problem | FIXED | Lines 75-76: "Does it have distinct phases? Does it specify what 'done' looks like? Does it include quality checks? If the plan is just 'Step 1: do the thing, Step 2: done' -- push back." |
| FM-08 | Skiing metaphor excludes non-skiers | NOT APPLICABLE (design choice) | Non-metaphorical track remains self-sufficient. All three principles (lines 72-77) are metaphor-free. |

---

## EVALUATION DIMENSIONS

### Standard Quality Dimensions

| Dimension | Weight | Score | Justification |
|---|---|---|---|
| Completeness | 0.20 | 0.95 | All eight iteration-1 failure modes addressed. Three-level framework, two-session pattern, checklist, and plan-quality criteria present. Only gap: no before/after demonstration (RR-01, medium risk). |
| Internal Consistency | 0.20 | 0.94 | No contradictions detected. The "probability distribution" framing is used consistently from Level 1 through the three principles. The McConkey metaphor maps cleanly to the graduated-effort argument. One micro-tension: line 42 says "can't reliably self-assess" while the article itself advocates for self-critique in Level 3 -- but this is resolved by the human-gate distinction. |
| Methodological Rigor | 0.20 | 0.93 | Claims are properly scoped and qualified. One unattributed consensus claim (self-evaluation bias, line 42). All other technical claims are either cited (Liu et al.), attributed ("researchers call this"), or framed as probability ("most probable"). |
| Evidence Quality | 0.15 | 0.92 | One named citation (Liu et al. 2023), correctly described. "Fluency-competence gap" grounded temporally. Self-evaluation bias grounded directionally but unattributed. Chain-of-thought and role-task-format referenced as searchable technique names. No floating assertions. |
| Actionability | 0.15 | 0.95 | Five-item checklist, three-level framework with clear entry points, two-session pattern with explicit mechanics, plan-quality criteria. The "I dare you" close pushes toward immediate action. |
| Traceability | 0.10 | 0.93 | One named citation, several searchable technique names, temporal grounding on fluency-competence gap. Appropriate for practitioner genre. No reference list needed. |

**Weighted Composite:**
```
Completeness:         0.20 x 0.95 = 0.190
Internal Consistency: 0.20 x 0.94 = 0.188
Methodological Rigor: 0.20 x 0.93 = 0.186
Evidence Quality:     0.15 x 0.92 = 0.138
Actionability:        0.15 x 0.95 = 0.1425
Traceability:         0.10 x 0.93 = 0.093

TOTAL: 0.9375
QUALITY GATE: PASS (>= 0.92)
```

### Special Dimensions

| Dimension | Score | Justification |
|---|---|---|
| LLM-Tell Detection | 0.88 | Two marginal signals: (1) Liu et al. citation paragraph register shift, (2) line 27 technical-explainer sentence. No hedging qualifiers, no topic-sentence-evidence paragraphs, no transition scaffolding, no empty emphasis. Cleanup pass was effective. |
| Voice Authenticity | 0.91 | McConkey voice is present without being performative. Conversational register maintained throughout except citation paragraph. "I dare you" close is the strongest voice moment. No catchphrase overuse. The voice restraint (McConkey appears twice, not twelve times) is itself authentic -- the persona is in the attitude, not the vocabulary. |

---

## OVERALL ASSESSMENT

The draft is strong. The inversion analysis identifies no critical failure modes. All eight failure modes from the iteration-1 inversion have been addressed. The LLM-tell cleanup pass was effective: no hedging qualifiers, no scaffolded transitions, no empty emphasis patterns remain.

**Strongest elements:**
- The three-level framework is the article's core contribution and it works. Graduated entry with the on-ramp (line 91) addresses the biggest risk from draft-1.
- The "I dare you" close is memorable. This is the kind of ending a reader acts on.
- The McConkey metaphor is structurally integrated, not decorative.

**Remaining attack surfaces (all low-to-medium severity):**
- RR-01 (no before/after demonstration) is the most substantive remaining gap. Medium risk. The article tells the reader about the difference rather than showing it.
- RR-03 (citation register shift) is the most detectable LLM-tell signal. Low risk but observable.
- RR-02 (self-assessment overclaim) and RR-04 (no domain example) are both acceptable for the genre.

**Verdict:** The article is ready for publication. The residual risks are within acceptable margins for a practitioner-facing article in a Saucer Boy voice. No revision required to meet the quality gate.
