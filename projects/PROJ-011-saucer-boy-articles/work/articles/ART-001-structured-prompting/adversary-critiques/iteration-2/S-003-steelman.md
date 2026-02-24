# Steelman Report: Why Structured Prompting Works

## Steelman Context

- **Deliverable:** `projects/PROJ-011-saucer-boy-articles/work/articles/ART-001-structured-prompting/drafts/draft-6-iteration-2.md`
- **Deliverable Type:** Article (practitioner-facing, McConkey persona)
- **Criticality Level:** C2
- **Strategy:** S-003 (Steelman Technique)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Steelman By:** adv-executor | **Date:** 2026-02-23 | **Iteration:** 2

---

## Summary

**Steelman Assessment:** Draft 6 (iteration 2) has resolved the primary gaps identified in the iteration-1-v2 steelman. The most consequential improvement is the addition of five inline citations with author names and years, which eliminates the ironic tension where a piece advocating for evidence-based practice itself lacked citations. The article is now a genuinely strong practitioner piece that teaches real mechanisms, provides actionable structure, and grounds its claims in published research.

**Improvement Count (vs. iteration-1-v2):** 0 Critical, 2 Major (resolved from prior iteration), 3 Minor (new observations)

**Original Strength:** The draft was already near-threshold at iteration 1 (0.91 composite). The structural architecture (Level 1/2/3), McConkey framing, and two-session pattern were already strong.

**Recommendation:** Minor polish only. The draft meets the quality gate.

---

## STRONGEST ASPECTS

### 1. The citation integration is seamless and genre-appropriate.

The iteration-1-v2 steelman identified evidence quality and traceability as the two dimensions dragging the composite below threshold. The specific gap: named concepts ("fluency-competence gap," "lost in the middle," "self-assessment bias") were referenced but not attributed. The S-014 iteration-2 scorer noted the ironic tension where the article advocates for citations in its own example prompts while failing to cite.

Draft 6 resolves this completely. Five inline citations now appear:

- Bender and Koller (2020) for the foundational fluency-competence argument (line 19)
- Sharma et al. (2024) for RLHF sycophancy producing authoritative-sounding responses (line 19)
- Wei et al. (2022) for chain-of-thought prompting and structured input improving output (line 27)
- Liu et al. (2023) for the lost-in-the-middle positional attention bias (line 57)
- Panickssery et al. (2024) for LLM self-preference bias (line 42)

What makes this exceptional: the citations are woven into the prose rather than dumped as footnotes. Each citation appears at the moment the claim is made, in a parenthetical that adds information rather than interrupting flow. The Bender and Koller citation is followed by a plain-language restatement of the finding. The Wei et al. citation specifies the task types (arithmetic, commonsense, symbolic reasoning). This is how citations work in strong practitioner writing: they ground the claim without breaking the reader's engagement.

What would be lost if changed: Removing the citations returns the article to the ironic gap state. Moving them to endnotes would reduce their persuasive function -- the reader would need to interrupt reading to verify credibility rather than absorbing it in-line.

### 2. The Level 1/2/3 pedagogical architecture remains the article's most important structural decision.

This was identified as the top strength in the iteration-1-v2 steelman and has been preserved without degradation. The three-level frame gives the reader permission to stop at Level 2 (line 29: "You don't need a flight plan for the bunny hill"). This single structural decision solves the most common failure mode of "how to prompt" articles: presenting the expert version first, overwhelming the reader, causing them to default to doing nothing.

The heading vocabulary reinforces the progression: "Point Downhill and Hope" (reckless), "Scope the Ask" (competent), "Full Orchestration" (expert). These are memorable, verb-forward, and carry increasing intentionality. A reader scanning headings alone gets the thesis.

What would be lost if changed: Flattening to continuous prose would eliminate the mental model readers carry forward. The levels are not just organizational. They are the article's conceptual contribution.

### 3. The garbage-compounding paragraph is now the article's signature insight.

Line 45: "It's not garbage in, garbage out. It's garbage in, increasingly polished garbage out, and you genuinely cannot tell the difference until something downstream breaks."

The iteration-1-v2 steelman flagged this as the single most quotable sentence in the piece, and noted that draft 5 had already elevated it from a buried mid-paragraph aside to its own structural block. Draft 6 preserves this positioning. The language has been tightened further: "genuinely cannot tell the difference" replaces what was previously a softer formulation. This sentence names a failure mode that experienced practitioners recognize instantly and beginners have never been warned about. It will be the sentence people share.

What would be lost if changed: Reburying this inside a longer paragraph would hide the article's strongest standalone insight. Its placement at the end of the Level 3 section ensures maximum impact -- the reader arrives at it after seeing the full complexity of orchestrated prompting, which is exactly the context where error compounding matters most.

### 4. The McConkey metaphor continues to function as architecture, not decoration.

The skiing frame opens the piece (line 7), provides Level 1 heading vocabulary, and closes the piece (lines 91-95). The metaphor is isomorphic to the argument: the relationship between McConkey's apparent chaos and hidden preparation maps one-to-one onto the relationship between a simple-looking prompt and the structured thinking behind it. This is not an analogy bolted on for personality. It is the thesis expressed through narrative.

The closing (line 93-95) earns its emotional register: "Next time you open an LLM, before you type anything, write down three things: what you need, how you'll know if it's good, and what you want to see first. Do that once and tell me it didn't change the output. I dare you." The dare works because the article has built enough credibility for it to land as confidence rather than arrogance.

What would be lost if changed: Any metaphor replacement would need to carry the same structural load. The McConkey frame is not interchangeable with a generic "preparation matters" example because the specific persona -- apparent recklessness backed by obsessive rigor -- is structurally identical to the article's thesis about prompting.

### 5. The Two-Session Pattern section remains the article's claim to novelty.

Most "how to prompt better" content covers input structure. Almost none covers the architectural decision to separate planning from execution into distinct context windows. This section (lines 47-61) explains the mechanism at two levels: token budget is finite (zero-sum allocation between planning history and execution space), and the Liu et al. (2023) lost-in-the-middle effect means performance degrades before the window fills. The citation is now inline with a clear description of the finding: "information buried in the middle of a long context gets significantly less attention than content at the beginning or end."

The honesty paragraph (line 61) names the cost: "You do lose the back-and-forth nuance. That's real." This is an important voice move. It does not oversell the technique. Readers trust writers who name costs.

What would be lost if changed: Removing the Two-Session Pattern would reduce the article from "here is something you probably did not know" to "here is advice you have read before." This section, combined with the citations, is what elevates the piece above generic prompting advice.

### 6. The self-assessment bias handling is now properly grounded.

Line 42 references Panickssery et al. (2024) and specifies the mechanism: "LLMs recognize and favor their own output, consistently rating it higher than external evaluators do." The iteration-1-v2 steelman and S-014 scorer both flagged the self-assessment claim as needing a citation. Draft 6 delivers this with precision. The sentence that follows ("Self-critique in the prompt is still useful as a first pass, a way to catch obvious gaps. But it's not a substitute for your eyes on the output.") is exactly the right nuance: it neither dismisses self-critique entirely nor oversells it. This balance is technically accurate and practically useful.

What would be lost if changed: Removing the citation returns the claim to assertion status, which the iteration-1-v2 S-014 scorer specifically penalized. Removing the nuance ("still useful as a first pass") would make the article less honest about the technique's real value.

---

## ELEMENTS THAT COULD BE MISREAD AS WEAKNESSES

### 1. The article has five inline citations -- could be read as too academic for a conversational piece.

This is not a weakness. The citations are parenthetical and non-intrusive. Each appears as "(Author et al. (year) showed/found/demonstrated that [finding])." This format adds credibility without interrupting flow. The citations solve the specific problem flagged in iteration 1: the ironic tension between the article's advocacy for evidence-based practice and its own absence of sourcing. The current balance -- five citations in a ~2,500 word piece -- is within the range where practitioner articles benefit from the authority signal without feeling academic.

### 2. The "Why This Works on Every Model" section (lines 63-67) is the most expository section.

This was flagged in the iteration-1-v2 steelman as the most voice-neutral section. Draft 6 has tightened it. The context window growth statistics (GPT-3 at 2K in 2020; Gemini 1.5 crossing a million in 2024) add concrete detail that was previously abstract. The section now has a stronger factual basis. The slightly more measured tone is appropriate for the section's function: establishing universality requires precision that the conversational sections do not.

### 3. The Level 3 prompt example uses terms like "cross-pollinate" that could read as jargon.

The term appears in a prompt example, not in the article's own prose. This is intentional: it models what a sophisticated prompt looks like. The surrounding explanation (lines 37-44) decodes each element of the prompt for the reader. A reader who cannot parse "cross-pollinate" on first read will understand it from the bullet explanation that follows. The progressive complexity design (Level 1 is simple, Level 3 is advanced) makes this acceptable.

### 4. The article does not include a "what if you're wrong" section or limitations discussion.

This would be expected in an academic paper. In a practitioner article with the McConkey persona, the equivalent is present in distributed form: the two-session pattern acknowledges its cost (line 61), the self-critique section names its limitation (line 42), and the closing explicitly invites the reader to test the advice ("I dare you" is implicitly "prove me wrong"). The limitations are embedded in the voice rather than segregated into a formal section.

---

## AREAS WHERE STRENGTHS COULD BE PUSHED FURTHER

### SM-001: The "Three Principles" section could include a compressed mnemonic.

**Severity:** Minor
**Dimension:** Actionability

The iteration-1-v2 steelman suggested "Constrain. Review. Separate." as a three-word compression. Draft 6 does not include this. The three principles are clearly stated with bold leads, which is functionally adequate. Adding a one-line mnemonic ("Three words: Constrain. Review. Separate.") would give readers an additional carry-forward handle, similar to how "fluency-competence gap" provides vocabulary for the problem. This is a minor enhancement, not a gap.

### SM-002: The Wei et al. citation could be slightly more specific about the magnitude of improvement.

**Severity:** Minor
**Dimension:** Evidence Quality

Line 27 states: "just adding intermediate reasoning steps to a prompt measurably improved performance on arithmetic, commonsense, and symbolic reasoning tasks." The word "measurably" is accurate but vague. The citations companion doc notes that Wei et al. demonstrated chain-of-thought as an emergent ability at scale (>100B parameters). Including either the scale threshold or a representative performance delta (e.g., "improved accuracy on GSM8K math problems from 17.7% to 58.1% with chain-of-thought") would make the evidence more concrete. However, this risks over-specifying for a conversational piece. Judgment call.

### SM-003: One concrete syntax comparison would strengthen the universality claim.

**Severity:** Minor
**Dimension:** Completeness

The "Why This Works on Every Model" section states "The syntax varies. XML tags for Claude, markdown for GPT, whatever the model prefers. The structure is the point, not the format." The iteration-1-v2 steelman suggested adding a three-line comparison showing the same structured prompt in two dialects. Draft 6 instead describes the principle abstractly and names the syntax types. This is acceptable -- a concrete example would add ~100 words and might distract from the section's point (universality of structure, not syntax). The abstract framing is defensible.

---

## ITERATION-1-V2 FINDINGS RESOLUTION

| Iteration-1-v2 Finding | Status | Evidence |
|---|---|---|
| More named citations needed (Evidence Quality drag) | **RESOLVED** | Five inline citations added: Bender & Koller (2020), Sharma et al. (2024), Wei et al. (2022), Liu et al. (2023), Panickssery et al. (2024) |
| Self-assessment bias claim unsourced (Methodological Rigor) | **RESOLVED** | Panickssery et al. (2024) cited at line 42 with specific mechanism |
| "Robust findings" claim unsourced (Methodological Rigor) | **RESOLVED** | Wei et al. (2022) cited at line 27, replacing the vague "robust findings" framing with a specific citation |
| Universality section slightly abstract | **PARTIALLY RESOLVED** | Context window growth stats added. No syntax comparison example added. The abstract treatment is defensible for the section's function. |
| Three Principles mnemonic ("Constrain. Review. Separate.") | **NOT ADDRESSED** | The principles are clear with bold leads. Mnemonic was a suggestion, not a gap. Minor enhancement opportunity. |

---

## SCORING IMPACT

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Positive | All major topics covered. Level 1/2/3 structure, two-session pattern, three principles, checklist, McConkey frame, citations. Minor: no syntax comparison, no mnemonic. |
| Internal Consistency | 0.20 | Positive | All iteration-1-v2 inconsistencies were already resolved in prior drafts. Draft 6 introduces no new contradictions. The citations reinforce rather than conflict with the voice. |
| Methodological Rigor | 0.20 | Positive | The two unsourced empirical claims flagged in iteration 1 are now cited. The mechanism explanations are accurate. The piece no longer has a gap between its evidence-based framing and its own sourcing practices. |
| Evidence Quality | 0.15 | Strongly Positive | This is the highest-leverage improvement. Five inline citations resolve the ironic tension. All citations are accurate per the companion citations.md document. Author names, years, and specific findings are included. |
| Actionability | 0.15 | Neutral (already high) | The checklist, three principles, Level 2 on-ramp, and closing dare were already strong. No regression. |
| Traceability | 0.10 | Positive | Five author-year citations make claims directly traceable. A reader can locate each referenced paper by searching author name and year. The companion citations.md provides full bibliographic detail. |

---

## DIMENSION SCORES

| Dimension | Weight | Score | Justification |
|-----------|--------|-------|---------------|
| Completeness | 0.20 | 0.94 | All major pedagogical, technical, and structural requirements met. Level 1/2/3 progression, two-session pattern, three principles, checklist, McConkey frame, five inline citations. Residual gaps (no syntax comparison, no mnemonic) are minor and defensible as genre choices. |
| Internal Consistency | 0.20 | 0.96 | Every section reinforces the same thesis. The McConkey frame opens and closes. The three principles map to the three levels. The checklist maps to the principles. Citations integrate without breaking voice. The "you lose the conversational nuance" admission is consistent with the honest-voice pattern. No contradictions detected. |
| Methodological Rigor | 0.20 | 0.94 | Technical claims are accurate and now cited. The fluency-competence gap, lost-in-the-middle effect, self-assessment bias, chain-of-thought improvement, and next-token prediction mechanism are all correctly described and attributed. The piece practices what it preaches: evidence-based claims backed by evidence. |
| Evidence Quality | 0.15 | 0.93 | Five inline citations with author names, years, and specific findings. All verified against companion citations.md. The ironic tension from iteration 1 is eliminated. Not scored higher because the article is not an academic paper -- the citations companion carries the full bibliographic weight, and the inline citations are appropriately concise. |
| Actionability | 0.15 | 0.95 | The checklist is copy-ready. The three principles are memorable. The Level 2 prompt example is directly reusable. The closing three-sentence instruction compresses the entire article into an immediate action. The progressive on-ramp ("Start with Level 2") prevents overwhelm. |
| Traceability | 0.10 | 0.92 | Five author-year inline citations. Named concepts (fluency-competence gap, lost-in-the-middle, self-preference bias, chain-of-thought). Three clearly labeled principles. Companion citations.md provides full references with URLs. For a practitioner article, this is strong traceability. |

---

## COMPOSITE SCORE

```
Completeness:         0.20 x 0.94 = 0.188
Internal Consistency: 0.20 x 0.96 = 0.192
Methodological Rigor: 0.20 x 0.94 = 0.188
Evidence Quality:     0.15 x 0.93 = 0.1395
Actionability:        0.15 x 0.95 = 0.1425
Traceability:         0.10 x 0.92 = 0.092
                                     ------
WEIGHTED COMPOSITE:                  0.942
```

**Weighted Composite Score: 0.942**

---

## LLM-TELL DETECTION

**Score: 0.92**

The LLM-tell cleanup from earlier drafts has held through the citation additions. Systematic check:

| Tell Category | Status in Draft 6 |
|---|---|
| Em-dashes / double-dashes | Not present. The article uses periods, commas, and sentence breaks. |
| Hedging language ("it's worth noting," "importantly") | Not detected. |
| "That's not X. It's Y." pattern | Not detected as a formulaic structure. Line 45 uses a "not X, it's Y" construction ("It's not garbage in, garbage out. It's garbage in, increasingly polished garbage out") but this is the article's signature insight, not a rhetorical tic. It appears once and earns its structure. |
| Formulaic transitions ("Now here's the thing," "Which brings me to") | Not detected. Transitions are heading-based or natural. |
| Excessive bolding | Confined to the three principles section (lines 71, 73, 75) where bold marks lead phrases of key takeaways. Functional, not decorative. |
| Excessive parallel structure | The Level 3 bullet list (lines 39-43) is parallel by design (parallel constraints). No gratuitous parallelism elsewhere. |
| Filler phrases ("Let me explain," "I want to be clear") | Not detected. |

Minor indicators:
- Line 3: "This isn't a Jerry thing. It's a 'how these models actually work under the hood' thing." The "X thing / Y thing" parallel is a faint pattern but reads naturally in conversational register.
- The citation integration ("Bender and Koller (2020) showed that..." / "Sharma et al. (2024) found that..." / "Wei et al. (2022) demonstrated this...") uses a consistent "Author (year) verb that..." pattern across all five citations. This consistency could register as templated to a close reader. However, this is also standard citation practice in non-academic writing. Not a defect.
- The overall structural cleanliness (heading hierarchy, consistent section proportions) could register as "too organized" but is indistinguishable from a well-edited article.

No new LLM-tells introduced by the iteration-2 revisions. The citation additions are the primary new content, and they integrate cleanly.

---

## VOICE AUTHENTICITY

**Score: 0.93**

Draft 6 maintains and slightly strengthens the voice from draft 5. Key evidence:

**Authentic McConkey markers present:**

- **Direct:** "That's the dangerous part." (line 17). No preamble, no qualification.
- **Warm:** "Alright, this trips up everybody, so don't feel singled out." (line 3). Inclusive, normalizing the mistake before diagnosing it.
- **Confident:** "I dare you." (line 95). Full-commitment close with no escape hatch.
- **Technically precise:** The next-token prediction explanation (line 17), the probability distribution framing (line 71), the attention mechanism reference (line 57). All accurate, all integrated into the voice.
- **Appropriately absurd:** "literally competed in a banana suit and won" (line 7). One reference, placed early, not overdone.
- **Honest about costs:** "You do lose the back-and-forth nuance. That's real." (line 61). McConkey voice does not oversell.

**Citation voice integration:**

The five citations are the main addition in this draft. The critical test is whether they break the conversational register. They do not. The citations are woven into the flow rather than dropped in as academic apparatus. Examples:

- "Bender and Koller (2020) showed that models trained on linguistic form alone don't acquire genuine understanding" -- this reads as a person referencing work they know, not as a footnote pasted in.
- "Wei et al. (2022) demonstrated this with chain-of-thought prompting: just adding intermediate reasoning steps..." -- the colon and plain-language summary keeps the reader in the conversational flow.
- "Panickssery et al. (2024) showed that LLMs recognize and favor their own output" -- clean integration into the self-assessment discussion.

The citations actually strengthen the voice: they signal that the speaker knows the research, which is consistent with the McConkey persona of apparent casualness backed by deep preparation. The citations are the textual equivalent of the hidden preparation the metaphor describes.

**One observation (not a defect):**

The "Why This Works on Every Model" section (lines 63-67) remains the most voice-neutral section. It is expository rather than conversational. The sentence "Context windows are engineering constraints" is accurate but lacks the rhythmic directness present elsewhere. This is the same observation made in iteration-1-v2. The section's function (universality argument) may justify the measured tone. If any section were to receive a final voice pass for warmth, it would be this one. However, this does not warrant a score reduction because the register shift is minor and purposeful.

---

## THE STRONGEST VERSION OF THE ARGUMENT

The argument this article makes, stated in its strongest form:

LLMs are autoregressive completion machines that optimize for the most probable output given their input. When the input is vague, the most probable output is the most generic response from the training distribution, not the most rigorous one. This creates a systematic fluency-competence gap (Bender & Koller 2020; Sharma et al. 2024) where output sounds authoritative regardless of its factual grounding. The fix is structural: constrain the input space so the most probable completion is also the most rigorous one. Structure improves output because it narrows the distribution of acceptable completions, a mechanism demonstrated empirically by Wei et al. (2022) for chain-of-thought prompting and replicated across model families and task types. For complex work, separate planning from execution into distinct context windows, because planning tokens compete with execution tokens and positional attention bias (Liu et al. 2023) degrades performance before the window fills. Build in human checkpoints because models cannot reliably self-assess (Panickssery et al. 2024). These principles are universal because they derive from transformer attention and autoregressive generation, not from any model-specific behavior.

This is a sound, well-sourced argument. Every technical claim rests on published, peer-reviewed research. The pedagogical structure (three levels with Level 2 as the practical default) makes the argument accessible without simplifying it. The McConkey frame makes it memorable without trivializing it. The citations make it credible without making it academic.

---

## VERDICT

```
WEIGHTED COMPOSITE: 0.942
THRESHOLD:          0.95 PASS / 0.92-0.94 REVISE / <0.92 REJECTED
VERDICT:            REVISE (0.942, within REVISE band per task-specific threshold)
```

Note: Per the standard quality-enforcement.md threshold (>= 0.92), this draft PASSES. Per the task-specific elevated threshold (>= 0.95 for PASS), this falls in the REVISE band. The gap is 0.008. The draft is strong and the remaining improvements are polish-level.

**Path to 0.95:**

1. **Completeness (0.94 -> 0.96):** Add the "Constrain. Review. Separate." mnemonic as a single sentence. Optionally add one concrete syntax comparison (Claude XML vs GPT markdown, 3 lines) to strengthen the universality claim.

2. **Evidence Quality (0.93 -> 0.95):** The citations are strong. To push further, the companion citations.md could be referenced with a closing note ("Full references and reading order at [link]") so readers know the bibliographic depth exists. This is a distribution decision rather than a content gap.

3. **Traceability (0.92 -> 0.94):** Same mechanism as Evidence Quality -- making the citations companion discoverable to readers.

These are minor enhancements. The article is publication-ready at its current quality level. The steelman assessment is that this article genuinely teaches something a reader did not know before, grounds it in research they can verify, and gives them a concrete action to take immediately. The voice is authentic and the technical content holds up.

---

*Strategy: S-003 Steelman Technique*
*SSOT: `.context/rules/quality-enforcement.md`*
*Reviewer: adv-executor*
*Date: 2026-02-23*
*Iteration: 2*
