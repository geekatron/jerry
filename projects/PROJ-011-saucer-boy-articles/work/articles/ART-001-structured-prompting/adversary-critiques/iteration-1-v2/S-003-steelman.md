---

## S-003 STEELMAN REVIEW

**STRATEGY:** S-003 Steelman Technique
**DELIVERABLE:** `drafts/draft-5-llm-tell-clean.md`
**REVIEWER:** adv-executor (S-003)
**ITERATION:** 1-v2 (post-LLM-tell cleanup, post-human rewrite)

---

### STRONGEST ASPECTS

**1. The Level 1/2/3 progression is the right pedagogical architecture for this content.**

Draft 5 restructures from the earlier prose-heavy format into explicit heading-labeled levels. This is not cosmetic. The three-level frame gives the reader permission to stop at Level 2. That single structural decision solves the most common failure of "how to prompt" articles: they present the expert version first, the reader feels overwhelmed, and they default to doing nothing. By making Level 2 the explicit "this is enough for most work" tier (line 29: "You don't need a flight plan for the bunny hill"), the article converts casual readers who would otherwise bounce. The heading-based progression also makes the article scannable for reference use. A reader who already understands Level 2 can jump directly to Level 3. This is a genuine improvement over draft 4's wall-of-text approach.

What would be lost if changed: Flattening back to continuous prose would eliminate the most reader-friendly aspect of the piece. The levels give readers a mental model they can carry forward without rereading the article.

**2. The "fluency-competence gap" naming move (line 19) is the technical anchor of the entire argument.**

The piece does not just describe the problem. It gives the reader a handle to carry it with. "Fluency-competence gap" is a real term from LLM evaluation research, and deploying it here does three things: it signals that the author is not inventing a complaint, it gives the reader vocabulary to explain the problem to others, and it compresses a paragraph of explanation into a reusable label. The sentence that precedes it ("The output sounds expert because the model learned to *sound* expert, not because it verified anything") is the clearest single-sentence explanation of this phenomenon I have seen in a non-academic context. It is precise, it is accessible, and it does not hedge.

What would be lost if changed: Removing the named term would reduce the reader's ability to generalize the concept. Unnamed problems are harder to recognize in the wild.

**3. The garbage-compounding paragraph (line 45) has been elevated from its buried position in earlier drafts.**

The iteration-1 steelman review specifically flagged this as the single most important insight in the piece, buried as a mid-paragraph aside. Draft 5 gives it structural separation. It now sits as its own paragraph block at the end of the Level 3 section, immediately after the bullet list. The language is sharper: "It's garbage in, polished garbage out, and you can't tell the difference until something breaks." This is the sentence that will get quoted. It names a failure mode that experienced practitioners recognize instantly and beginners have never been warned about. The structural promotion was the right call.

What would be lost if changed: Reburying this inside a longer paragraph would hide the piece's strongest standalone insight. Its current placement ensures the reader hits it at the moment of maximum receptivity, right after seeing the complexity of Level 3.

**4. The McConkey metaphor works as architecture, not decoration.**

The skiing frame is not a gimmick. It opens the piece (line 7), provides the Level 1 heading vocabulary ("Point Downhill and Hope"), and closes the piece (lines 93-97). This creates a rhetorical bookend that makes the article feel unified rather than assembled. The metaphor is transparent to non-skiers: "he looked like he was winging it, he wasn't" requires zero domain knowledge. The critical insight is that the metaphor carries the thesis: the relationship between apparent wildness and hidden preparation is structurally identical to the relationship between a simple-looking prompt and the structured thinking behind it. The metaphor is isomorphic to the argument.

What would be lost if changed: Any metaphor replacement would need to carry the same structural load. The skiing frame is not interchangeable with a generic "preparation matters" example because McConkey's specific reputation, the appearance of chaos backed by obsessive preparation, maps one-to-one onto the article's argument about structured prompting appearing to produce "the same ask" with radically different results.

**5. The Two-Session Pattern section (lines 47-59) is the most technically novel content in the piece.**

Most "how to prompt better" content covers input structure. Almost none covers the architectural decision to separate planning from execution into distinct context windows. This section explains *why* at the mechanism level: token budget is zero-sum (line 55), and the "lost in the middle" effect (line 55-56, citing Liu et al. 2023) means that performance degrades before the window fills. Draft 5 now includes the actual citation, which the earlier draft referenced only obliquely. The paragraph that follows (line 59) names the cost explicitly: "You lose the conversational nuance. That's the cost." This is honest writing. It does not oversell the technique. It names the tradeoff and then explains why the tradeoff is worth it. Readers trust writers who name costs.

What would be lost if changed: Removing the Two-Session Pattern would reduce the article from "here is something you probably did not know" to "here is advice you have read before." This section is the piece's claim to novelty.

**6. The closing (lines 93-97) earns its emotional register.**

"Next time you open an LLM, before you type a single word, write down what you need, how you'll know if the answer is good, and what you want to see first. Three sentences before the prompt. Do that once and tell me it didn't change the output. I dare you." This is not performative McConkey voice. This is a confident closing that compresses the entire article into a single actionable instruction and dares the reader to test it. The "I dare you" works because the article has built enough credibility for the challenge to land as playful confidence rather than arrogance. The three-sentence instruction is genuinely useful as a standalone takeaway. A reader who remembers nothing else from the article but does this before their next prompt will get measurably better output.

What would be lost if changed: A hedged closing ("consider trying this") would undercut the entire article's voice. The dare is earned. Softening it would retroactively weaken every confident claim that preceded it.

---

### ELEMENTS THAT COULD BE MISREAD AS WEAKNESSES

**1. The bold formatting in "The Three Principles" section (lines 73-77) could be read as LLM-tell excessive bolding.**

This is a deliberate and correct choice. The three principles are the article's most important standalone content. They function as a reference card. Bold numbering ("**1. Constrain the work.**") is standard article formatting for key takeaways, not LLM-generated emphasis pattern. The distinction: LLM-tell bolding emphasizes random phrases for faux-authority ("It's **really important** to **always** structure your prompts"). This bolding emphasizes exactly three structural labels. The pattern is functional, not decorative.

**2. The bullet list in Level 3 (lines 39-44) could be read as LLM-generated list padding.**

It is not. Each bullet introduces a distinct concept (parallel work streams, evidence grounding, self-critique with explicit dimensions, human gates, plan-before-product). None are synonyms. None could be removed without losing a distinct idea. The list format is the correct choice because these are parallel constraints applied simultaneously, not a sequential narrative. A prose paragraph would obscure the independence of each constraint.

**3. The checklist at lines 83-89 could be read as formulaic LLM "action items."**

The checklist is the article's implementation artifact. It is the transition point from "understand this" to "do this." Its code-block formatting distinguishes it from prose and signals that it is meant to be copied and reused. This is an intentional design decision for an article published on an mkdocs site: checklists in code blocks are copy-friendly. The items map one-to-one to the three principles plus the two-session pattern. Nothing is added for padding.

**4. The article does not include a McConkey quote or anecdote beyond the skiing frame.**

This could be read as insufficient persona commitment. It is actually correct restraint. The persona document specifies that McConkey voice is a lens, not a costume. Stuffing the article with "McConkey would say..." interjections would violate the canon. The persona is expressed through the writing style (direct, technically precise, naming costs honestly, no hedging) rather than through explicit references. The two McConkey references that exist (opening and closing) are structurally justified as the metaphor frame. Adding more would be decorative.

**5. The article is relatively long for a "why structured prompting works" explainer.**

Length is justified by the Level 1/2/3 structure. The article is actually three articles in one (quick advice at Level 2, full methodology at Level 3, underlying theory in the interstitial sections). The Level 2 reader can stop at line 29 and walk away with actionable advice. The full length serves the Level 3 reader who needs the mechanism-level explanation. Shortening the article would require removing either the Level 3 detail (gutting the technical depth) or the Two-Session Pattern (removing the novel contribution). Neither cut is worth it.

---

### THE STRONGEST VERSION OF THE ARGUMENT

The argument this article is making, stated in its strongest form:

LLMs are completion machines that optimize for the most probable output given their input. When the input is vague, the most probable output is the most generic response from the training distribution, not the most rigorous one. This creates a systematic gap between how competent the output sounds and how competent it actually is. The fix is to constrain the input space so that the most probable completion is also the most rigorous one. This requires three things: explicit quality criteria (so the model knows what "good" means), plan-before-product sequencing (so you can evaluate the process before committing to the output), and context window hygiene (because planning tokens compete with execution tokens and attention degrades with context length). These principles are universal across model families because they derive from how transformer attention and autoregressive generation work, not from any model-specific behavior.

This is a sound argument. Every technical claim it rests on is supported by published research. The pedagogical structure (three levels, with Level 2 as the practical default) makes the argument accessible without dumbing it down. The McConkey frame makes it memorable without trivializing it.

---

### AREAS WHERE STRENGTHS COULD BE PUSHED FURTHER

**1. The "lost in the middle" citation (line 55-56) is the only named research reference.**

The article makes multiple claims that are well-supported by published work (fluency-competence gap, constrained inputs improving output, self-assessment bias). Currently only the Liu et al. "lost in the middle" finding gets a named citation. The article could be even more credible if one or two additional claims received the same treatment. Candidates: the self-assessment bias finding (line 42: "research on LLM self-evaluation consistently shows favorable bias") and the constrained-inputs finding (line 65: "well-documented finding across prompt engineering research"). Even a parenthetical naming ("a pattern documented across model families since GPT-3" on line 19 is a good start) strengthens the authority without adding bulk.

The piece already does this well in places. Pushing the technique to two or three more claims would make the evidence quality dimension even stronger.

**2. The "Why This Works on Every Model" section (lines 61-69) is correct but slightly abstract.**

This section makes the universality argument. It could push further by giving one concrete syntax example showing the same structured prompt in two model dialects (e.g., Claude XML tags vs. GPT markdown). One three-line comparison would make the abstract claim tangible. This would especially help Level 2 readers who might think "structured prompting" means a specific format rather than a general principle.

**3. The Three Principles could be made even more memorable with a mnemonic or shorthand.**

"Constrain. Review. Separate." Three words that capture the three principles. The article almost arrives at this compression but stops one step short. A single sentence introducing this shorthand ("Three words: Constrain. Review. Separate.") would give readers a carryable handle, similar to how "fluency-competence gap" gives them vocabulary for the problem.

---

### DIMENSION SCORES

| Dimension | Weight | Score | Justification |
|-----------|--------|-------|---------------|
| Completeness | 0.20 | 0.91 | Covers Level 1/2/3, two-session pattern, three principles, checklist. Minor gap: no concrete syntax comparison for universality claim. All major concepts from the prompt engineering domain that are relevant to the thesis are present. |
| Internal Consistency | 0.20 | 0.95 | Every section reinforces the same thesis. The McConkey frame opens and closes. The three principles map to the three levels. The checklist maps to the principles. No contradictions detected. The "you lose the conversational nuance" admission is consistent with the honest-voice pattern. |
| Methodological Rigor | 0.20 | 0.90 | Technical claims are accurate. The fluency-competence gap, lost-in-the-middle effect, self-assessment bias, and next-token prediction mechanism are all correctly described. One claim ("well-documented finding across prompt engineering research" on line 65) is asserted without named support, though it is in fact well-documented. The mechanism-level explanations (why constraints narrow the output distribution) are sound. |
| Evidence Quality | 0.15 | 0.87 | One named citation (Liu et al. 2023). Multiple correct but unnamed references to research findings. The evidence is real and accurately described, but the article would score higher with two or three more named citations. For a practitioner article (not an academic paper), the current level is strong but not maximal. |
| Actionability | 0.15 | 0.94 | The checklist is copy-ready. The three principles are memorable. The Level 2 prompt example is directly reusable. The "three sentences before the prompt" closing instruction is the highest-actionability sentence in the piece. A reader can apply the advice immediately after reading. |
| Traceability | 0.10 | 0.82 | One explicit citation. Multiple implicit references to documented research. For an article format (not a technical report), traceability is adequate but not exemplary. The article's claims are traceable to their research origins by a knowledgeable reader, but a non-expert would need to search for the unnamed sources. |

**Weighted Composite Score: 0.907**

Calculation: (0.91 x 0.20) + (0.95 x 0.20) + (0.90 x 0.20) + (0.87 x 0.15) + (0.94 x 0.15) + (0.82 x 0.10) = 0.182 + 0.190 + 0.180 + 0.1305 + 0.141 + 0.082 = **0.9055**

Rounded: **0.91**

---

### LLM-TELL SCORE

**Score: 0.90**

Draft 5 has undergone explicit LLM-tell cleanup. The major tells from draft 4 have been addressed:

| Tell Category | Status in Draft 5 |
|---|---|
| Em-dashes / double-dashes | Eliminated. Draft 4 had many. Draft 5 uses periods and sentence breaks instead. |
| Hedging language ("it's worth noting", "importantly") | Not detected. |
| Formulaic transitions ("Now here's the thing", "Which brings me to") | Eliminated. Draft 4 had several. Draft 5 uses heading-based transitions instead. |
| Excessive bolding | Confined to the three principles section where it is functional. |
| Overly parallel structure | The Level 3 bullet list is parallel by design (parallel constraints). No gratuitous parallelism elsewhere. |
| Filler phrases | Not detected. |
| "Let me explain" / "I want to be clear" | "I want to be clear" was in draft 4. Not present in draft 5. |

Remaining minor indicators:

- Line 3: "This isn't a Jerry thing. It's a 'how these models actually work under the hood' thing." The "X thing / Y thing" parallel is a faint pattern but reads naturally here. Borderline.
- Line 65: "This is a well-documented finding across prompt engineering research, from chain-of-thought prompting to structured role-task-format patterns." The "from X to Y" construction with technical term enumeration is a mild tell. Could be shortened to "This is a well-documented finding across prompt engineering research" without the enumeration.
- The article's overall structural cleanliness (clean heading hierarchy, consistent section lengths, tidy bullet lists) could register as "too organized" to a suspicious reader. However, this is also what a well-edited article looks like. This is a style judgment, not a defect.

---

### VOICE AUTHENTICITY SCORE

**Score: 0.91**

Draft 5 has the strongest voice of the draft sequence. Key evidence:

**Authentic McConkey markers present:**

- **Direct:** "That's the dangerous part." (line 17). No preamble, no qualification. States the problem and moves on.
- **Warm:** "Alright, this trips up everybody, so don't feel singled out." (line 3). Inclusive. Normalizes the mistake before diagnosing it.
- **Confident:** "I dare you." (line 97). Full-commitment close. No hedging escape hatch.
- **Technically precise:** The next-token prediction explanation (line 17), the probability distribution framing (line 73), the attention mechanism reference (line 55). All accurate, all integrated into the voice rather than dropped in as asides.
- **Appropriately absurd:** "ski a cliff in a banana suit" (line 7). One reference, placed early, not overdone.

**Improvements over draft 4:**

- Draft 4 opened with "OK so here's what's going on with your prompt." Draft 5 opens with "Alright, this trips up everybody, so don't feel singled out." The draft 5 opening is warmer, more inclusive, and more McConkey. It addresses the reader's situation without making it about a specific person's mistake.
- Draft 4 used "I want to be clear" twice. Draft 5 uses it zero times. This is a voice win. McConkey's documented style does not seek permission to be clear; he simply is.
- The heading vocabulary ("Point Downhill and Hope", "Scope the Ask", "Full Orchestration") is active and verb-forward. This matches McConkey's documented communication pattern of movement-first language.

**One remaining voice note:**

The "Why This Works on Every Model" section (lines 61-69) is the most voice-neutral section of the article. The technical content is accurate, but the writing style shifts slightly toward expository prose. Sentences like "Context windows are hard engineering constraints, determined by architecture, memory, and compute tradeoffs" are correct but lack the rhythmic directness present in the rest of the piece. This is a minor observation. The section's function (universality argument) may justify a slightly more measured tone. But if any section were to receive a voice pass, it would be this one.

---

### SUMMARY

This is a strong draft. The Level 1/2/3 structure is the right pedagogical choice. The McConkey voice is authentic, not performative. The technical content is accurate. The LLM-tell cleanup has been effective. The garbage-compounding insight has been properly elevated. The two-session pattern remains the article's most novel contribution.

The weighted composite score of 0.91 places this in the REVISE band (0.85-0.91), just below the 0.92 quality gate. The gap is narrow and concentrated in two dimensions: Evidence Quality (more named citations would push this up) and Traceability (same cause). One or two additional named references for the self-assessment bias and constrained-input findings would likely push the composite above the threshold without adding significant length.

The steelman assessment is that this article genuinely teaches something. A reader who follows the Level 2 advice will get better LLM output. A reader who follows the Level 3 advice and the two-session pattern will get substantially better output. The closing dare is earned. The voice is real. The technical claims hold up.

---

*Strategy: S-003 Steelman Technique*
*Reviewer: adv-executor*
*Date: 2026-02-23*
