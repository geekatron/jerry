# Steelman Report: Why Structured Prompting Works

## Steelman Context

- **Deliverable:** `projects/PROJ-011-saucer-boy-articles/work/articles/ART-001-structured-prompting/drafts/draft-7-iteration-3.md`
- **Deliverable Type:** Article (practitioner-facing, McConkey persona)
- **Criticality Level:** C2
- **Strategy:** S-003 (Steelman Technique)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Steelman By:** adv-executor | **Date:** 2026-02-23 | **Iteration:** 3

---

## Summary

**Steelman Assessment:** Draft 7 (iteration 3) has addressed the three path-to-0.95 items identified in the iteration-2 steelman. The most consequential improvement is the addition of a companion citations reference in the closing section, which resolves the discoverability gap for the full bibliographic apparatus. The article also adds RLHF as an explicit named mechanism (Sharma et al. 2024), tightens several passages for precision, softens the closing from a dare to an invitation, and replaces the "banana suit" anecdote with a more grounded McConkey characterization. The cumulative effect of changes across three iterations has produced an article that is technically rigorous, well-sourced, actionable, and voiced with authentic personality throughout.

**Improvement Count (vs. iteration 2):** 0 Critical, 0 Major, 4 Minor (new observations)

**Original Strength:** The draft was scored at 0.942 composite in iteration 2. The structural architecture, citation integration, McConkey framing, and pedagogical progression were already at or above threshold on every dimension.

**Recommendation:** The draft meets the quality gate. Remaining observations are polish-level and do not affect any dimension score materially.

---

## STRONGEST ASPECTS

### 1. The citations companion reference closes the traceability loop.

The iteration-2 steelman identified a specific path-to-0.95 gap: the five inline citations were strong, but the companion citations document was not discoverable from the article itself. The iteration-2 S-003 report stated: "The companion citations.md could be referenced with a closing note ('Full references and reading order at [link]') so readers know the bibliographic depth exists."

Draft 7 resolves this with a "Further reading" section (line 102): "The claims in this article are grounded in published research. For full references with links, see the companion citations document." This is followed by a curated reading order naming three key papers: Liu et al. (2023), Wei et al. (2022), and Panickssery et al. (2024). This mirrors the reading order already present in citations.md, creating coherence between the two documents.

Why this matters: the article now has two layers of evidence -- inline citations for immediate credibility during reading, and a discoverable companion for readers who want to verify or go deeper. This is the standard for high-quality practitioner writing. The traceability dimension benefits directly, and the evidence quality dimension benefits from the completeness signal.

What would be lost if changed: removing the further reading section returns the article to the state where a reader must independently discover or be given the citations document. The inline citations remain strong, but the full bibliographic apparatus becomes invisible.

### 2. The RLHF mechanism explanation strengthens the technical precision of the fluency-competence argument.

Draft 7, line 17-19, adds a sentence that earlier drafts did not have: "Post-training techniques like RLHF shape that behavior, but when your instructions leave room for interpretation, the prediction mechanism fills the gaps with whatever pattern showed up most often in the training data." This is followed by the Sharma et al. (2024) citation, which now explicitly names RLHF as the mechanism that "makes this worse by rewarding confident-sounding responses over accurate ones."

This is a genuine improvement. The iteration-2 draft attributed the fluency-competence gap to Bender and Koller (2020) and Sharma et al. (2024) but did not explicitly name RLHF as the mechanism in the main text. Draft 7 does. The reader now gets the causal chain: (a) models predict the next token, (b) RLHF shapes outputs toward confident-sounding completions, (c) when instructions are vague, the model defaults to the most probable (most generic, most confident-sounding) completion. This is technically accurate and significantly more informative than "the model learned to sound expert."

What would be lost if changed: removing the RLHF reference reduces the explanation from mechanistic to phenomenological. The reader would know *that* models sound confident but not *why*. The Sharma et al. citation would lose its explanatory anchor.

### 3. The Level 1/2/3 pedagogical architecture continues to be the article's most important structural decision.

This was identified as the top structural strength in both iteration-1-v2 and iteration-2 steelman reviews. Draft 7 preserves it without degradation. The three-level frame gives the reader permission to stop at Level 2 (line 29: "For most day-to-day work, that's honestly enough. You don't need a flight plan for the bunny hill"). The heading vocabulary reinforces the progression: "Point Downhill and Hope" (reckless), "Scope the Ask" (competent), "Full Orchestration" (expert).

Draft 7 introduces one subtle refinement: the Level 2 prompt example now specifies "cite the original source" and "Show your selection criteria. I want to see why you picked those 5 before you apply them." These additions model the exact behavior the article advocates -- constrained instructions with explicit quality criteria. The prompt example practices what the article preaches, creating internal consistency at the micro level.

What would be lost if changed: flattening to continuous prose would eliminate the mental model readers carry forward. The levels are the article's conceptual contribution, not just its organizational scheme.

### 4. The garbage-compounding paragraph remains the article's signature insight, now with strengthened framing.

Draft 7, line 45: "It's not garbage in, garbage out. It's garbage in, increasingly polished garbage out, and it gets much harder to tell the difference the deeper into the pipeline you go."

The phrasing has been refined from the iteration-2 version. "You genuinely cannot tell the difference" has become "it gets much harder to tell the difference the deeper into the pipeline you go." This is a more precise claim. The original implies impossibility; the revision describes a gradient of difficulty correlated with pipeline depth. This is both more accurate and harder to argue against. The preceding sentence ("Each downstream phase takes the previous output at face value and adds another layer of polished-sounding analysis on top") makes the mechanism explicit.

What would be lost if changed: the graduated phrasing is more defensible than the absolute phrasing. Reverting to "you can't tell the difference" would be stronger rhetoric but weaker epistemics. The current version is the better tradeoff for a piece that grounds its claims in research.

### 5. The Two-Session Pattern section retains its status as the article's claim to novelty, now with better Liu et al. integration.

Draft 7, line 57: "Liu et al. (2023) found that models pay the most attention to what's at the beginning and end of a long context, and significantly less to everything in the middle." This is followed by a new sentence: "They studied retrieval tasks, but the attentional pattern applies broadly: your carefully crafted instructions from message three are competing with forty messages of planning debate, and the model isn't weighing them evenly."

This is a meaningful refinement. The iteration-2 version described the finding. Draft 7 adds the scope qualifier ("They studied retrieval tasks") and then explicitly bridges to the article's context ("your carefully crafted instructions from message three..."). This is responsible citation practice: acknowledge the original study's scope, then argue for the generalization. It is also good pedagogy: the reader sees how a specific research finding applies to their specific workflow.

The honesty paragraph (line 61) continues to name the cost: "You do lose the back-and-forth nuance. That's real." This has been strengthened with: "The plan artifact has to carry the full context on its own. Phases, what 'done' looks like for each phase, output format. If the plan can't stand alone, it wasn't detailed enough." This converts the admission of cost into a quality criterion for the plan, which is actionable rather than merely honest.

What would be lost if changed: removing the scope qualifier weakens the citation integrity. Removing the bridge sentence reduces the reader's ability to apply the finding. The section is now stronger on both evidence quality and actionability.

### 6. The McConkey characterization has been refined from spectacle to substance.

Draft 7, line 7: "Shane McConkey, if you don't know him, was a legendary freeskier who'd show up to competitions in costume and still take the whole thing seriously enough to win. The guy looked completely unhinged on the mountain. He wasn't. Every wild thing he did was backed by obsessive preparation."

This replaces the earlier "banana suit" reference with a more grounded description. The earlier version named a specific antic; the current version names the pattern (costume + competition + winning, apparent chaos + hidden rigor). This is more aligned with the article's thesis: the point is not any particular McConkey stunt but the structural relationship between apparent recklessness and underlying discipline.

The closing (line 96-98) has been similarly adjusted: "McConkey looked like he was winging it. He wasn't. The wild was the performance. The preparation was everything underneath it." This is cleaner than the iteration-2 close and maps the metaphor explicitly to the article's thesis. "The wild was the performance. The preparation was everything underneath it" is a two-sentence compression of the entire article.

What would be lost if changed: reverting to a specific anecdote would narrow the metaphor. The current version is more universal and carries the structural argument better. The reader does not need to know what a banana suit is to understand the point.

### 7. The self-assessment nuance paragraph has been integrated more tightly into the Level 3 structure.

Draft 7, line 42: "Here's the tension with that self-critique step. I just told the model to evaluate its own work, but models genuinely struggle with self-assessment." This opening acknowledges the tension explicitly before presenting the evidence (Panickssery et al. 2024). The resolution -- "Self-critique in the prompt is still useful as a first pass, a way to catch obvious gaps. But it's not a substitute for your eyes on the output." -- is followed by: "The human checkpoints are where real quality control happens."

The previous draft ended this section with the nuanced "still useful as a first pass" qualification. Draft 7 adds the explicit connection to human checkpoints, tying the self-assessment limitation back to the Level 3 prompt's checkpoint requirement. This creates internal consistency: the prompt asks for checkpoints, the article explains why checkpoints matter, and the evidence (Panickssery et al.) supports the necessity.

What would be lost if changed: removing the tension framing would make the self-assessment discussion feel like a tangent rather than a deliberate design choice in the Level 3 prompt.

---

## ELEMENTS THAT COULD BE MISREAD AS WEAKNESSES

### 1. The closing no longer dares the reader.

The iteration-2 closing included "I dare you." Draft 7 replaces this with: "Do that once and tell me it didn't change the output." The dare is now implicit rather than explicit. This could be read as a softening of the voice.

This is not a weakness. The revised closing is equally confident but more inviting. "Tell me it didn't change the output" is a rhetorical challenge that accomplishes the same function as the dare: it commits the speaker to the claim that the technique works, and it invites the reader to test it. The difference is register: "I dare you" is confrontational; "tell me it didn't change the output" is collegial. For a piece published to a broader audience (not just the original Discord recipient), the collegial register is more appropriate. The confidence is undiminished; the tone is more inclusive.

### 2. The article does not include the "Constrain. Review. Separate." mnemonic.

Both the iteration-1-v2 and iteration-2 steelman reviews suggested this three-word compression. Draft 7 does not include it. The three principles section (lines 69-75) uses bold leads for each principle ("Constrain the work.", "Review the plan before the product.", "Separate planning from execution.") which are functionally equivalent. Each bold lead is already a compressed label. Adding a separate mnemonic line would be redundant with the bold leads and would add a formatting element that no other section in the article uses.

This is a deliberate omission that is defensible as a genre choice. The bold leads serve as the mnemonic. A formal "Three words: Constrain. Review. Separate." line would introduce a different rhetorical mode (slogan-style) that is not present elsewhere in the article and could read as a forced takeaway.

### 3. The article still does not include a concrete syntax comparison between model dialects.

The "Why This Works on Every Model" section (lines 63-67) states: "The syntax varies. XML tags for Claude, markdown for GPT, whatever the model prefers. The structure is what matters, not the format." This is abstract rather than concrete.

This is not a weakness at the article's current scope. The section's function is to establish universality. A concrete syntax comparison would shift the reader's attention to the specific format differences rather than the principle of structural equivalence. The abstract framing correctly prioritizes the principle over implementation detail. A syntax comparison would be appropriate for a follow-up article or a companion reference, not for this section's role in the argument.

### 4. The five inline citations could be perceived as academic apparatus in a conversational piece.

This was addressed in the iteration-2 steelman and remains the correct assessment: the citations are parenthetical and non-intrusive. Each appears as "(Author et al. (year) showed/found/demonstrated [finding])." The format adds credibility without interrupting flow. Five citations in a piece of approximately 2,500 words is well within the range where practitioner articles benefit from the authority signal. The citations have a dual function: they ground the article's claims, and they demonstrate the article's own advice (cite your sources).

### 5. The "Further reading" section could be read as an afterthought.

The section is placed after a horizontal rule separator at the end of the article. This is standard placement for a references or further reading section. It is visually distinct from the article body, which is correct: it serves a navigation function for readers who want to go deeper, not a persuasion function. The curated reading order (three papers, not all five) is a good editorial choice -- it directs readers to the three most generalizable findings rather than presenting the full bibliography.

---

## AREAS WHERE STRENGTHS COULD BE PUSHED FURTHER

### SM-001: The Wei et al. citation could be slightly more specific about the finding's scale dependency.

**Severity:** Minor
**Dimension:** Evidence Quality

Line 27: "Wei et al. (2022) demonstrated this with chain-of-thought prompting: just adding intermediate reasoning steps to a prompt measurably improved performance on arithmetic, commonsense, and symbolic reasoning tasks." The citations companion doc notes that chain-of-thought is an emergent ability at scale (>100B parameters). Including the scale qualifier -- "at sufficient model scale, just adding..." or a parenthetical "(an emergent ability in models above ~100B parameters)" -- would sharpen the claim. However, adding the scale qualifier introduces a secondary concept (emergent abilities) that is tangential to the article's point. The article's argument is that structure improves output; whether that improvement is scale-dependent is a relevant nuance for an academic audience but not for the practitioner audience. Omission is defensible.

### SM-002: The context window growth statistics could include Claude in the progression.

**Severity:** Minor
**Dimension:** Completeness

Line 65: "GPT-3 shipped with 2K tokens in 2020, and Gemini 1.5 crossed a million in 2024." The progression skips Claude entirely. Given that the article's further reading section links to a companion document and the article is published in a context associated with Claude, including Claude in the progression (e.g., "GPT-3 shipped with 2K tokens in 2020, Claude 3 supports 200K, and Gemini 1.5 crossed a million in 2024") would make the universality claim concrete across three model families rather than two. This is a minor enhancement. The two-point progression (2K to 1M) already conveys the magnitude of growth. Adding a third data point strengthens the universality claim marginally.

### SM-003: The error propagation paragraph could name the compounding mechanism more precisely.

**Severity:** Minor
**Dimension:** Methodological Rigor

Line 45: "Each downstream phase takes the previous output at face value and adds another layer of polished-sounding analysis on top." The mechanism is correct: downstream phases treat upstream output as ground truth. The citations companion document cites Arize AI (2024) on cascading errors in LLM pipelines. The article does not name a source for this claim inline. This is the only major technical claim in the article that lacks an inline citation. However, the claim is also the most intuitive one in the piece -- error propagation in serial pipelines is a general systems engineering principle, not an LLM-specific finding. Citing it would be technically correct but might feel over-cited for a concept most readers accept as self-evident. The absence of a citation here is defensible.

### SM-004: The "Why This Works on Every Model" section remains the most voice-neutral section.

**Severity:** Minor
**Dimension:** Voice Authenticity (supplementary)

This was flagged in both the iteration-1-v2 and iteration-2 steelman reviews. Draft 7 has tightened the section: "Context windows are engineering constraints, the kind of hard limits determined by architecture and compute" replaces the earlier "hard engineering constraints" phrasing. The addition of ", the kind of hard limits determined by architecture and compute" adds specificity. The section is still more expository than conversational, but the register shift is purposeful: the universality argument requires precision that the conversational sections do not. Draft 7 also adds: "Every model performs better when you give it structure to work with. Specific instructions over vague ones. Explicit quality criteria over 'use your best judgment.' Evidence requirements over unconstrained generation." The three-part parallel ("Specific over vague. Explicit over judgment. Evidence over unconstrained.") brings voice back into the section via rhythm. This is an improvement over the iteration-2 version.

---

## ITERATION-2 FINDINGS RESOLUTION

| Iteration-2 Finding | Status | Evidence |
|---|---|---|
| Add companion citations.md discoverability (Traceability + Evidence Quality path-to-0.95) | **RESOLVED** | "Further reading" section added at line 102 with companion link and curated 3-paper reading order |
| "Constrain. Review. Separate." mnemonic (Completeness, Minor) | **NOT ADDRESSED (defensible)** | Bold leads on the three principles serve the same function. Separate mnemonic would introduce a different rhetorical mode not present elsewhere. |
| Concrete syntax comparison (Completeness, Minor) | **NOT ADDRESSED (defensible)** | Abstract framing correctly prioritizes the universality principle over implementation detail. |
| Wei et al. more specific about magnitude (Evidence Quality, Minor) | **PARTIALLY ADDRESSED** | Now specifies task types (arithmetic, commonsense, symbolic reasoning). Scale dependency not included; defensible for practitioner audience. |
| "Why This Works on Every Model" voice-neutral (Voice Authenticity, observation) | **PARTIALLY ADDRESSED** | New three-part parallel structure adds rhythm. Section still more expository than conversational, which is appropriate for its function. |

---

## SCORING IMPACT

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Positive | All major topics covered. The further reading section adds a new structural element (bibliography discoverability) that was absent before. Context window stats use two concrete data points. Three principles with bold leads. Checklist. McConkey frame. |
| Internal Consistency | 0.20 | Positive | No contradictions introduced. The RLHF mechanism addition strengthens the causal chain from Level 1 explanation through the fluency-competence gap. The further reading section mirrors the citations.md reading order. The closing metaphor maps explicitly to the thesis. |
| Methodological Rigor | 0.20 | Positive | The Liu et al. citation now includes a scope qualifier ("They studied retrieval tasks, but the attentional pattern applies broadly"). The RLHF explanation adds a mechanistic layer. The garbage-compounding claim uses graduated rather than absolute language. The self-assessment section explicitly names the tension before resolving it. |
| Evidence Quality | 0.15 | Positive | Five inline citations maintained. Companion citations document now discoverable. Curated reading order provides guided entry point. The RLHF mechanism is named explicitly alongside the Sharma et al. citation. |
| Actionability | 0.15 | Positive | The honesty paragraph in the Two-Session Pattern section now converts the admission of cost into a quality criterion for the plan. The three-sentence closing instruction remains. The further reading section gives readers a concrete next step for going deeper. |
| Traceability | 0.10 | Strongly Positive | This is the highest-leverage improvement from iteration 2 to iteration 3. The companion citations document is now discoverable from the article itself. A reader can follow the further reading link to full bibliographic detail with URLs. The three-paper reading order provides a guided path through the supporting research. |

---

## DIMENSION SCORES

| Dimension | Weight | Score | Justification |
|-----------|--------|-------|---------------|
| Completeness | 0.20 | 0.95 | All major pedagogical, technical, and structural requirements met. Level 1/2/3 progression, two-session pattern, three principles, checklist, McConkey frame, five inline citations, further reading with companion link. Residual minor observations (no syntax comparison, no mnemonic) are defensible genre choices and do not constitute gaps. The further reading section closes the discoverability gap identified in iteration 2. |
| Internal Consistency | 0.20 | 0.97 | Every section reinforces the same thesis. The McConkey frame opens and closes with explicit thesis mapping ("The wild was the performance. The preparation was everything underneath it."). The three principles map to the three levels. The checklist maps to the principles. The RLHF mechanism connects the Level 1 explanation to the Sharma et al. citation. The self-assessment tension connects to the Level 3 checkpoint requirement. The further reading mirrors the citations.md reading order. No contradictions detected. |
| Methodological Rigor | 0.20 | 0.95 | Technical claims are accurate, cited, and now include scope qualifiers. The Liu et al. finding is qualified with "They studied retrieval tasks, but the attentional pattern applies broadly." The RLHF explanation is mechanistic rather than phenomenological. The garbage-compounding claim uses graduated language ("it gets much harder" rather than "you can't tell"). The self-assessment section names its tension before resolving it. The piece practices what it preaches at every level. |
| Evidence Quality | 0.15 | 0.95 | Five inline citations with author names, years, and specific findings. All verified against companion citations.md. Companion now discoverable from the article via the further reading section. Curated reading order provides a guided entry point. The RLHF mechanism is named alongside the Sharma et al. citation. The only technical claim without an inline citation (error propagation in pipelines) is a general systems engineering principle that does not require one. |
| Actionability | 0.15 | 0.96 | The checklist is copy-ready. The three principles are memorable via bold leads. The Level 2 prompt example is directly reusable. The closing three-sentence instruction compresses the entire article into an immediate action. The progressive on-ramp ("Start with Level 2") prevents overwhelm. The further reading section gives depth-seekers a concrete next step. The Two-Session Pattern cost admission is now paired with a quality criterion for the plan artifact. |
| Traceability | 0.10 | 0.95 | Five author-year inline citations. Named concepts (fluency-competence gap, lost-in-the-middle, self-preference bias, chain-of-thought, RLHF). Three clearly labeled principles. Companion citations.md discoverable from the article via further reading section with curated 3-paper reading order. A reader can trace any technical claim from the article text to the inline citation to the companion document to the full paper. This is exemplary traceability for a practitioner article. |

---

## COMPOSITE SCORE

```
Completeness:         0.20 x 0.95 = 0.190
Internal Consistency: 0.20 x 0.97 = 0.194
Methodological Rigor: 0.20 x 0.95 = 0.190
Evidence Quality:     0.15 x 0.95 = 0.1425
Actionability:        0.15 x 0.96 = 0.144
Traceability:         0.10 x 0.95 = 0.095
                                     ------
WEIGHTED COMPOSITE:                  0.9555
```

**Weighted Composite Score: 0.956**

---

## LLM-TELL DETECTION

**Score: 0.93**

The LLM-tell cleanup from earlier drafts continues to hold. Systematic check against draft 7:

| Tell Category | Status in Draft 7 |
|---|---|
| Em-dashes / double-dashes | One instance at line 65: "Context windows are engineering constraints, the kind of hard limits determined by architecture and compute." This is a legitimate appositive clause, not an em-dash tic. The comma usage is standard. No em-dash characters present. |
| Hedging language ("it's worth noting," "importantly") | Not detected. |
| "That's not X. It's Y." pattern | Line 45: "It's not garbage in, garbage out. It's garbage in, increasingly polished garbage out." This is the article's signature insight. It appears once and earns its structure through the specific content of the contrast. Not a formulaic tic. |
| Formulaic transitions ("Now here's the thing," "Which brings me to") | Not detected. Transitions are heading-based or natural. |
| Excessive bolding | Confined to the three principles section (lines 71, 73, 75) where bold marks lead phrases of key takeaways. Functional, not decorative. |
| Excessive parallel structure | The Level 3 bullet list (lines 39-43) is parallel by design (parallel constraints). The "Specific instructions over vague ones. Explicit quality criteria over..." three-part parallel in line 65 is rhythmic rather than formulaic. No gratuitous parallelism elsewhere. |
| Filler phrases ("Let me explain," "I want to be clear") | Not detected. |

Minor indicators:

- Line 3: "This isn't a Jerry thing. It's a 'how these models actually work under the hood' thing." The "X thing / Y thing" parallel persists from earlier drafts. It reads naturally in conversational register and is not repeated elsewhere.
- The citation pattern ("Author (year) showed/found/demonstrated that...") is consistent across all five citations. This consistency is standard citation practice in non-academic writing and does not register as templated to a general reader.
- The further reading section uses a bold "Further reading:" lead. This is standard article formatting, not an LLM-tell.

No new LLM-tells introduced by the iteration-3 revisions. The primary new content (further reading section, RLHF explanation, scope qualifier on Liu et al., garbage-compounding refinement) integrates cleanly.

Score unchanged from iteration 2 at 0.93. The minor indicators are stable and represent stylistic signatures rather than tells.

---

## VOICE AUTHENTICITY

**Score: 0.94**

Draft 7 maintains and slightly strengthens the voice from draft 6. Key evidence:

**Authentic McConkey markers present:**

- **Direct:** "That's the dangerous part." (line 17). No preamble, no qualification.
- **Warm:** "Alright, this trips up everybody, so don't feel singled out." (line 3). Inclusive, normalizing the mistake before diagnosing it.
- **Confident:** "Do that once and tell me it didn't change the output." (line 98). The confidence is in the claim, not in a confrontational register. The implicit message is: I am so sure this works that I am inviting you to test it against my prediction.
- **Technically precise:** The RLHF explanation (line 17), the next-token prediction mechanism (line 17), the probability distribution framing (line 71), the attention mechanism reference with scope qualifier (line 57). All accurate, all integrated into the voice.
- **Appropriately grounded:** "a legendary freeskier who'd show up to competitions in costume and still take the whole thing seriously enough to win" (line 7). This replaces the banana suit reference with a characterization that is more informative and less spectacle-dependent.
- **Honest about costs:** "You do lose the back-and-forth nuance. That's real." (line 61), now followed by: "If the plan can't stand alone, it wasn't detailed enough." The cost admission is paired with a quality criterion.

**Iteration-3 voice improvements:**

- The McConkey characterization (line 7) is more substantive. "Show up to competitions in costume and still take the whole thing seriously enough to win" communicates both the persona and the competence. The earlier "banana suit" reference was more colorful but less informative.
- The closing (lines 96-98) maps the metaphor to the thesis with unusual precision: "The wild was the performance. The preparation was everything underneath it." This is a two-sentence thesis statement expressed through the metaphor rather than alongside it. The voice and the argument are unified.
- The closing instruction: "Next time you open an LLM, before you type anything, write down three things: what you need, how you'll know if it's good, and what you want to see first." This is warmer than "three sentences before the prompt" and more specific. It gives the reader three named items rather than a numeric count.
- Line 42: "Here's the tension with that self-critique step." The colloquial "Here's the tension" is a natural McConkey-voice way to introduce a counterargument. It acknowledges complexity without hedging.

**Voice score improvement rationale:**

The 0.01 increase (0.93 to 0.94) reflects the cumulative effect of small refinements: the closing is more precise, the McConkey characterization is more substantive, the self-assessment tension framing is more conversational, and the "Why This Works on Every Model" section now has rhythmic parallel structure. No single change is large, but the aggregate effect is a draft that reads more consistently in voice from beginning to end.

**Remaining observation (not a defect):**

The "Why This Works on Every Model" section (lines 63-67) remains the most measured section of the article. The new three-part parallel ("Specific instructions over vague ones. Explicit quality criteria over 'use your best judgment.' Evidence requirements over unconstrained generation.") brings rhythmic directness back into the section. The register shift from the conversational sections is now minimal and purposeful.

---

## THE STRONGEST VERSION OF THE ARGUMENT

The argument this article makes, stated in its strongest form:

LLMs are autoregressive completion machines that predict the next token based on everything before it. Post-training techniques like RLHF shape that prediction toward confident-sounding output, not toward rigorous output (Sharma et al. 2024). When instructions are vague, the model's prediction mechanism fills the gaps with whatever pattern is most probable in the training distribution -- producing a systematic fluency-competence gap (Bender & Koller 2020) where output sounds authoritative regardless of its factual grounding. The fix is structural: constrain the input space so the most probable completion is also the most rigorous one. This works because specific instructions narrow the distribution of acceptable completions, a mechanism demonstrated empirically by Wei et al. (2022) for chain-of-thought prompting across arithmetic, commonsense, and symbolic reasoning tasks. For complex work, separate planning from execution into distinct context windows, because planning tokens compete with execution tokens and positional attention bias (Liu et al. 2023) degrades performance before the window fills -- a finding from retrieval tasks that applies broadly because the attentional mechanism is architecture-level, not task-specific. Build in human checkpoints because models cannot reliably self-assess (Panickssery et al. 2024), recognizing and favoring their own output. These principles are universal because they derive from transformer attention and autoregressive generation, not from any model-specific behavior. Error propagation in multi-phase pipelines compounds the stakes: each downstream phase treats upstream output as ground truth, producing increasingly polished garbage that becomes harder to detect the deeper you go. The human checkpoints and plan-before-product sequencing are the countermeasures.

This is a sound, well-sourced, mechanistically grounded argument. Every technical claim rests on published, peer-reviewed research, discoverable via the companion citations document. The pedagogical structure (three levels with Level 2 as the practical default) makes the argument accessible without simplifying it. The McConkey frame makes it memorable without trivializing it. The citations make it credible without making it academic. The further reading section makes it verifiable.

---

## VERDICT

```
WEIGHTED COMPOSITE: 0.956
THRESHOLD:          0.95 PASS / 0.92-0.94 REVISE / <0.92 REJECTED
VERDICT:            PASS (0.956 >= 0.95)
```

The draft passes the elevated quality gate threshold of 0.95. The improvement from 0.942 (iteration 2) to 0.956 (iteration 3) is driven primarily by:

1. **Traceability (0.92 -> 0.95):** The further reading section makes the companion citations document discoverable.
2. **Completeness (0.94 -> 0.95):** The further reading section adds a structural element that closes the discoverability gap.
3. **Evidence Quality (0.93 -> 0.95):** The RLHF mechanism is named explicitly. The Liu et al. citation includes a scope qualifier. The companion is now discoverable.
4. **Methodological Rigor (0.94 -> 0.95):** The graduated garbage-compounding language, the Liu et al. scope qualifier, and the self-assessment tension framing all demonstrate careful, precise reasoning.
5. **Actionability (0.95 -> 0.96):** The cost admission in the Two-Session Pattern is now paired with a quality criterion. The further reading gives depth-seekers a next step.
6. **Internal Consistency (0.96 -> 0.97):** The RLHF mechanism addition strengthens the causal chain. The closing metaphor maps explicitly to the thesis.

The remaining minor observations (SM-001 through SM-004) are polish-level. None would change any dimension score if addressed. The article is publication-ready.

The steelman assessment is that this article genuinely teaches something a reader did not know before, grounds it in research they can verify, gives them a concrete action to take immediately, and speaks in a voice that is authentic, confident, and inclusive. The structure, evidence, and personality work together rather than in tension. This is a strong piece of practitioner writing.

---

*Strategy: S-003 Steelman Technique*
*SSOT: `.context/rules/quality-enforcement.md`*
*Reviewer: adv-executor*
*Date: 2026-02-23*
*Iteration: 3*
