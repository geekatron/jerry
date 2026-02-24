---

## S-010 SELF-REFINE: Adversarial Review

**STRATEGY:** S-010 Self-Refine
**DELIVERABLE:** `drafts/draft-5-llm-tell-clean.md`
**REVIEWER:** adv-executor (S-010)
**DATE:** 2026-02-23
**CONTEXT:** Draft 5 is a cleaned version of draft 4 (human rewrite). Draft 4 passed the quality gate at 0.938 (iteration 3). Draft 5 was produced by removing LLM tells from draft 4. This review evaluates draft 5 on its own merits, with particular attention to: (a) residual LLM tells, (b) voice regression from the cleaning pass, (c) new weaknesses introduced by structural edits.

---

### LLM-TELL DETECTION

Sentence-by-sentence scan for: em-dashes (--), double-dashes, hedging patterns, parallel structure excess, formulaic transitions, excessive bolding, "delve/tapestry/landscape/robust/nuanced" vocabulary, list-ification of conversational prose, and synthetic summarization patterns.

**TELL 1 -- HIGH: Formulaic three-part sentence structure in Line 17**

> "The structure will be clean. The headings will be professional. The language will be authoritative."

Three parallel declarative sentences, same length, same "The X will be Y" pattern. This is a classic LLM tell: the triplet-with-parallel-syntax construction. It reads like a model generating three examples by repeating its own template. A human writing conversationally would vary the structure. Compare to draft 4's equivalent: "The headings will be perfect. The structure will look professional." -- which was only two items and had slight variation ("will be perfect" vs. "will look professional"). Draft 5 expanded this to three and made them more uniform, which is the opposite of de-telling.

> **Fix:** Collapse to two items with varied syntax, or make one item do more work. Example: "The headings will look professional. The structure will read like someone did real analysis." Or fold into the prior sentence: "...they give you something worse: the most probable generic response from their training distribution, dressed up with clean structure and authoritative language, passing as a custom answer."

---

**TELL 2 -- MEDIUM: "That's not a coin flip. It's systematic, and it's predictable." (Line 19)**

This reads as an LLM correcting a prior draft's metaphor and being slightly too pleased about the correction. The sentence structure -- "That's not X. It's Y, and it's Z." -- is a common LLM rhetorical move: negate the wrong frame, then assert the right one with a comma-and-adjective flourish. Draft 4 did not have this sentence; it was added in draft 5. The intent is good (the original "coin flip" issue from iteration 1 was a real problem). But the fix sounds like an LLM inserting a correction rather than a human rewriting naturally.

> **Fix:** Integrate the correction into the preceding thought rather than appending it as a standalone counter-statement. The paragraph already explains why it is systematic. The "That's not a coin flip" sentence is redundant with the explanation that precedes it. Consider cutting it entirely -- the paragraph makes the case without it.

---

**TELL 3 -- MEDIUM: Parallel bullet structure in Lines 39-43**

The five bullets under "But now the LLM knows:" all follow the same pattern: bold-phrase-as-label, then explanation. Specifically:

- "Two parallel work streams, not one chute. [Explanation.]"
- "Real sources, not training-data gravity. [Explanation.]"
- "Self-critique with specific dimensions. [Explanation.]"
- "Human gates. [Explanation.]"
- "Plan before product. [Explanation.]"

Every bullet opens with a 3-5 word noun phrase, period, then elaboration. This regularity is a structural tell. Draft 4 did not use this format -- it used varied-length bullets with different rhythms. Draft 5 regularized them into a template. That regularization is precisely the kind of cleaning that introduces LLM fingerprints rather than removing them.

> **Fix:** Vary the bullet structures. Some should lead with the explanation. Some should be one sentence. Some should be two. The current version reads like a slide deck. Example variance: "Gap analysis and framework research are separate work streams. Don't merge them into one pass." / "You're forcing real sources. Training-data gravity is strong -- the evidence constraint fights it." / "Human gates, because models can't reliably self-assess at scale."

---

**TELL 4 -- LOW: "Every dimension you leave unspecified" appears twice (Lines 27 and 73)**

Line 27: "Vague instructions leave the model to fill in every unspecified dimension with defaults."
Line 73: "Every dimension you leave unspecified, the model fills with the most generic probable completion."

Nearly the same claim, nearly the same syntax, in two locations. This is a repetition tell -- LLMs often re-derive the same point in different sections because they do not track what they have already said. A human author would notice the echo and either cut one or deliberately reference the earlier statement ("As I said above..."). The draft does neither.

> **Fix:** Cut one instance. Line 73 is the stronger version because it is in the principles summary section. Line 27 could be shortened to: "Vague instructions let the model default on every unspecified dimension." -- briefer, less parallel with line 73.

---

**TELL 5 -- LOW: "That's the cost." (Line 59)**

"You lose the conversational nuance. That's the cost." This is a minor tell -- the "That's the X." sentence fragment used to land a point is an LLM rhetorical habit. It appears here and in a similar form at line 45: "That's why the human gates matter. That's why the plan review matters." The repeated pattern of "That's [the/why] X" as a concluding punch is slightly overdone in this draft.

Four occurrences of "That's" as a sentence opener used for rhetorical emphasis:
- Line 19: "That's not a coin flip."
- Line 45: "That's not garbage in, garbage out." / "That's why the human gates matter. That's why the plan review matters."
- Line 59: "That's the cost."
- Line 73: "That's not laziness."

Five uses across 97 lines. Not catastrophic, but the pattern is detectable.

> **Fix:** Replace 2 of the 5 with different constructions. Line 59: "The cost is real." Line 73: "Not laziness -- probability distributions."

---

**LLM-Tell Score: 0.72**

Draft 5 removed some tells from draft 4 but introduced new ones through structural regularization (Tell 3) and corrective insertions (Tell 2). The parallel triplet (Tell 1) is the most visible. Net tell density is moderate -- a careful reader would not flag this as AI-generated, but a tell-detection reviewer finds five patterns. The tells are structural (syntax repetition, parallel construction) rather than lexical (no "delve," "tapestry," etc.), which makes them harder to catch but also less damaging to casual readers.

---

### VOICE AUTHENTICITY

**Overall: Authentic with cleaning-induced regression in two spots.**

The voice in draft 5 is noticeably more formatted than draft 4. Draft 4 read like someone talking. Draft 5 reads like someone talking after an editor cleaned it up. Specific observations:

**Regression 1: The McConkey introduction (Line 7) lost warmth.**

Draft 4: "Shane McConkey -- if you don't know him, he was this legendary big-mountain freeskier who literally competed in a banana suit and won."

Draft 5: "Shane McConkey, legendary freeskier, the guy who'd ski a cliff in a banana suit and win competitions doing it."

Draft 4 has a parenthetical aside ("if you don't know him") that is conversational. Draft 5 replaced it with an appositive clause that reads like a Wikipedia summary. "The guy who'd ski a cliff in a banana suit" is punchier than draft 4's version, but "legendary freeskier" as an appositive is resume-voice, not bar-conversation voice. Nobody introduces someone by saying "Shane McConkey, legendary freeskier." They say "Shane McConkey -- you know him? Legendary freeskier, the guy who..."

> **Fix:** Restore the conversational aside. "Shane McConkey -- if you don't know him, legendary freeskier, the guy who'd ski a cliff in a banana suit and win competitions doing it."

---

**Regression 2: Opening of the Two-Session Pattern section lost energy.**

Draft 4: "Which brings me to the part that most people completely miss. You don't fire off that big prompt and let the model run."

Draft 5: "You don't just fire the prompt and let it run."

Draft 4 had a transition sentence that built anticipation ("the part that most people completely miss"). Draft 5 cut it, presumably as cleanup. But that sentence was doing voice work -- it is the kind of thing a person says when they are about to tell you the real insight. The draft 5 version starts the section flat.

> **Fix:** Restore a transitional hook. Does not need to be the exact draft 4 sentence. Even "Here's the part people miss:" would work.

---

**Regression 3: "Why a new conversation? Two reasons." (Line 53)**

This is a textbook explanatory structure. Draft 4 had: "Why? Two reasons." -- shorter, punchier, more conversational. Draft 5 expanded it to "Why a new conversation? Two reasons." -- which is more explicit but sounds like a tech blog. Minor, but the direction of the edit (expanding terse conversational beats into explicit complete sentences) is systematically the wrong direction for voice.

> **Fix:** Revert to "Why? Two reasons." or "Why a fresh chat? Two reasons."

---

**Voice Authenticity Score: 0.78**

Draft 4 was approximately 0.85 on voice. Draft 5's cleaning pass traded some voice authenticity for structural polish. The regressions are small individually but directionally consistent: every change moved from "person talking" toward "edited article." The McConkey introduction regression is the most significant because it is the reader's first encounter with the persona. The three principles section (identified as a voice weakness in iteration 1) was not improved in this pass and remains the weakest voice section.

---

### ISSUES FOUND

**ISSUE 1 -- HIGH: Title is generic and unsearchable**

> **Where:** Line 1: "# Why Structured Prompting Works"

This title could appear on any prompt engineering blog post. It does not signal the McConkey voice, the three-level framework, or the two-session pattern -- the three things that differentiate this article from the hundreds of "structured prompting" articles already published. For an mkdocs site, the title is the primary navigation and search signal.

> **Suggestion:** Titles that signal the specific content: "Three Levels of Prompting (And Why Level 1 Burns You)" / "The McConkey Rule for LLM Prompting" / "Structured Prompting: From Point-and-Hope to Full Orchestration." The title should give the reader a reason to click that no other article provides.

> **Priority:** HIGH -- first impression and SEO/navigation signal. The article body is distinctive; the title is not.

---

**ISSUE 2 -- HIGH: The "80%" claim in Line 23 is ungrounded**

> **Where:** "Most people can get 80% of the benefit with a prompt that's just two or three sentences more specific"

Where does 80% come from? This is a specific numeric claim with no source, no derivation, and no caveat. Is it from research? Personal experience? A guess? In a piece that criticizes LLMs for generating confident-sounding unsupported claims, an unsupported "80%" figure is ironic. Draft 4 had the same claim. Neither iteration addressed it.

> **Suggestion:** Either (a) hedge it honestly: "Most people get the majority of the benefit with..." or (b) ground it: "In my experience, a two-sentence refinement closes most of the gap" or (c) acknowledge it is a rough heuristic: "Call it the 80/20 rule of prompting -- two extra sentences of specificity cover most of the ground."

> **Priority:** HIGH -- the article's own thesis is that unsupported claims are the problem. This is an unsupported claim.

---

**ISSUE 3 -- MEDIUM: "training-data gravity" (Line 40) is an invented term used without explanation**

> **Where:** "Real sources, not training-data gravity."

"Training-data gravity" is not an established term. It is a metaphor that the article coins without unpacking. In context, the reader can infer the meaning (the model's tendency to pull toward training data patterns), but the article otherwise takes care to explain its technical terms ("fluency-competence gap" gets a full paragraph, "lost in the middle" gets an author citation). "Training-data gravity" gets zero explanation. It sits in a bullet point as if the reader already knows what it means.

> **Suggestion:** Either unpack it briefly ("The evidence constraint fights training-data gravity -- the model's pull toward whatever it saw most in training") or replace it with plain language ("Real sources, not whatever the training data defaults to").

> **Priority:** MEDIUM -- not a factual error, but an inconsistency in how the article treats its own terminology.

---

**ISSUE 4 -- MEDIUM: The "fluency-competence gap" is presented as an established term but is not**

> **Where:** Line 19: "It's called the 'fluency-competence gap,' a pattern documented across model families since GPT-3."

"Fluency-competence gap" is not a widely established term with a canonical citation in the LLM research literature. The concept is real -- models produce fluent text that lacks substantive accuracy. But the term itself is not standard. "Since GPT-3" implies this is a formally tracked phenomenon with that specific name. A reader searching for "fluency-competence gap" will not find a canonical paper. The prior iteration's S-014 scorer noted this same issue (score iteration 3, Evidence Quality section) and accepted it as "adequate" for the genre. I am flagging it again because draft 5 did not improve the attribution, and the phrasing became slightly more assertive ("It's called the" implies it is a named thing in the field).

> **Suggestion:** Soften the attribution to match what the term actually is: "Researchers describe this as a kind of fluency-competence gap" or "You could call this a fluency-competence gap." The difference between "it's called" (implies consensus terminology) and "you could call this" (implies useful label) matters for a technically literate audience.

> **Priority:** MEDIUM -- the concept is accurate, the term is useful, the presentation overstates its pedigree.

---

**ISSUE 5 -- MEDIUM: The Three Principles section (Lines 71-77) still has voice deficit**

This was flagged as ISSUE 5 in the original iteration-1 S-010 review. Draft 5 has not materially addressed it. The three principles read as clean technical prose. They are correct, clear, and well-structured. They do not sound like someone talking to you.

Compare the voice energy of Line 45 ("That's not garbage in, garbage out. It's garbage in, polished garbage out, and you can't tell the difference until something breaks.") with the voice energy of Line 75 ("Ask for the execution plan first. Check it. Does it have distinct phases? Does it specify what 'done' looks like?"). Line 45 has personality. Line 75 is a checklist.

The principles section is the part the reader will bookmark, screenshot, or share. If it reads like a textbook, the shareability drops. This is the section where voice matters most, and it is the section where voice is weakest.

> **Suggestion:** Inject one beat of personality per principle. Example for Principle 2: "Review the plan, not just the product. The LLM will hand you a plan. It will look reasonable. Check it anyway. Does it have real phases or is it 'Step 1: do the thing, Step 2: done'? If the plan is lazy, push back. This is where you catch bad work before it multiplies." That is still structured but sounds like someone is in the room with you.

> **Priority:** MEDIUM -- recurring issue across iterations. The fix is not structural; it is tonal.

---

**ISSUE 6 -- MEDIUM: "Do not deviate." (Line 51) is not how effective executor prompting works**

> **Where:** *"You are the executor. Here is the plan. Follow it step by step. Do not deviate."*

"Do not deviate" is overly rigid and can actually degrade output quality. Real execution prompting benefits from allowing the model to flag issues, request clarification, and adapt to unexpected findings. A rigid "do not deviate" instruction suppresses the model's ability to course-correct when it encounters something the plan did not anticipate. This advice, if followed literally, could produce worse results than a more flexible executor instruction like "Follow this plan. If you encounter something the plan does not address, flag it and pause."

> **Suggestion:** Revise the example executor prompt to model good practice: *"You are the executor. Here is the plan. Follow it step by step. If you encounter something the plan doesn't cover, flag it and wait for my input."* This is more useful advice and models the human-gate pattern that the article already advocates.

> **Priority:** MEDIUM -- practical advice issue. The article teaches human checkpoints but then models a prompt that suppresses them.

---

**ISSUE 7 -- LOW: "whatever ships next Tuesday" (Line 3) is a time-bound joke**

> **Where:** "Claude, GPT, Gemini, Llama, whatever ships next Tuesday."

This is a time-sensitive reference. If the article is read six months from now, "next Tuesday" will feel stale. It works today because model releases are frequent. It may not age well. Minor issue, but for evergreen content on an mkdocs site, time-sensitive jokes create maintenance burden.

> **Suggestion:** "Claude, GPT, Gemini, Llama, whatever ships next" -- dropping "Tuesday" keeps the cadence and humor without pinning it to a timeframe that will feel dated.

> **Priority:** LOW -- polish level.

---

**ISSUE 8 -- LOW: The checklist (Lines 83-89) uses code block formatting**

The checklist is wrapped in triple backticks (code fence). On an mkdocs site, this will render as monospace text in a code block. For a checklist, this is an unusual formatting choice that may confuse readers who expect interactive checkboxes or a styled callout. More importantly, it signals "this is code" when it is not code.

> **Suggestion:** Use markdown checkbox syntax without the code fence: `- [ ] Did I specify WHAT to do...` This renders as a checklist in most mkdocs themes and is semantically correct.

> **Priority:** LOW -- formatting, not content.

---

**ISSUE 9 -- LOW: "I dare you." (Line 97) as closing**

The closing line is punchy. But it is the kind of line that works in a speech and falls flat in text. The reader just finished a thoughtful, technically grounded article. The closing shifts register to playground dare. For some readers this will land as confident and playful. For others it will feel jarring or performative. This is a judgment call, not a defect. Flagging it because voice-cleaning passes sometimes strip the personality that makes closings like this work, and in draft 5's slightly more polished register, the "I dare you" sits less naturally than it would in draft 4's more conversational register.

> **Suggestion:** Keep it if the preceding paragraph retains enough energy to support it. If the preceding paragraph gets more formal in future edits, cut it. The dare only works if the voice has been warm and direct for the preceding two paragraphs.

> **Priority:** LOW -- subjective, but worth noting for future revisions.

---

### TECHNICAL ACCURACY

**Claim 1: "next-token predictors trained on billions of documents" (Line 17)**

Accurate. Current LLMs (GPT-4, Claude, Gemini, Llama) are autoregressive next-token predictors. "Billions of documents" is a fair characterization of training corpus scale.

**Claim 2: "the most probable generic response from their training distribution" (Line 17)**

Directionally accurate but slightly simplified. The output is sampled from a probability distribution, not deterministically the single most probable token at each step (temperature, top-p, etc. introduce stochasticity). For the audience and purpose, this simplification is appropriate. The core point -- vague prompts produce generic outputs -- is correct.

**Claim 3: "fluency-competence gap...since GPT-3" (Line 19)**

The concept is real. The specific term is not a canonical research term. See Issue 4 above. The temporal claim "since GPT-3" is approximately correct -- fluency-accuracy disconnect has been documented in various forms since GPT-3's release in 2020.

**Claim 4: "Structured instructions focus the model's attention on relevant context and narrow the space of acceptable completions" (Line 27)**

Accurate. This is consistent with the empirical findings on structured prompting (chain-of-thought, few-shot formatting, role-task-format patterns). The mechanism described (attention focusing + output distribution narrowing) is a reasonable high-level explanation.

**Claim 5: "research on LLM self-evaluation consistently shows favorable bias" (Line 42)**

Accurate. Multiple studies have documented that LLMs rate their own output more favorably than human evaluators rate the same output. The claim is correctly stated as a direction (favorable bias) without overclaiming magnitude.

**Claim 6: Liu et al. (2023) documented the "lost in the middle" effect (Line 55)**

Accurate. Liu et al. (2023), "Lost in the Middle: How Language Models Use Long Contexts," is a real paper that documents exactly the effect described. The specific finding quoted (instructions buried in long contexts get less attention than beginning/end content) is accurate.

**Claim 7: "Context windows...grown from 4K to 1M+ tokens in three years" (Line 63)**

Accurate. GPT-3 (2020) had 4K tokens. Gemini 1.5 Pro (2024) supports 1M+ tokens. The three-year timeframe is approximately correct (2021 4K -> 2024 1M+).

**Claim 8: "chain-of-thought prompting...structured role-task-format patterns" (Line 65)**

Accurate. Both are well-documented prompting techniques with published research. Chain-of-thought (Wei et al., 2022) is one of the most cited prompting papers. Role-task-format is a commonly described structured prompting pattern.

**Claim 9: "Do not deviate." as executor prompt (Line 51)**

Technically functional but practically suboptimal. See Issue 6 above. Not inaccurate per se -- the model will follow it -- but it models a prompting practice that contradicts the article's own philosophy of human checkpoints.

**Technical Accuracy Score: 0.90**

No factual errors. One terminology presentation issue (fluency-competence gap presented as more established than it is). One practical advice issue ("Do not deviate" contradicts the article's own checkpoint philosophy). The Liu et al. citation is verified accurate. All mechanism-level claims are sound for the audience level.

---

### EVALUATION DIMENSIONS

| Dimension | Weight | Score | Justification |
|-----------|--------|-------|---------------|
| Completeness | 0.20 | 0.93 | Three-level framework complete. Two-session pattern complete with plan artifact criteria. Checklist present. No structural gaps. Title weakness (Issue 1) is a framing gap, not a content gap. |
| Internal Consistency | 0.20 | 0.91 | "Do not deviate" (Issue 6) contradicts the article's checkpoint philosophy. "Every dimension you leave unspecified" appears twice (Tell 4). "80%" claim (Issue 2) is the kind of unsupported assertion the article warns against. These are not contradictions of logic but contradictions of practice-what-you-preach. |
| Methodological Rigor | 0.20 | 0.91 | The "80%" claim is ungrounded. The "fluency-competence gap" pedigree is overstated. Self-evaluation bias claim is accurate but still unattributed (noted in iteration 3 scoring). These are the same rigor gaps from iteration 3; draft 5's cleaning pass did not address them. |
| Evidence Quality | 0.15 | 0.91 | Liu et al. citation strong. Chain-of-thought and role-task-format references are searchable. Fluency-competence gap attribution is adequate but not strong. The 80% claim has zero evidence backing. Net: the evidence base is good but has one unforced hole. |
| Actionability | 0.15 | 0.93 | Three levels with example prompts. Checklist at the end. Plan artifact quality criteria specified. The "Do not deviate" prompt models a suboptimal practice. The checklist code-block formatting is a minor usability issue. |
| Traceability | 0.10 | 0.92 | Liu et al. (2023) traceable. Chain-of-thought and role-task-format are searchable technique names. Fluency-competence gap is descriptive but not traceable to a canonical source. No other floating claims. |

**Weighted Composite:**

```
Completeness:         0.20 x 0.93 = 0.186
Internal Consistency: 0.20 x 0.91 = 0.182
Methodological Rigor: 0.20 x 0.91 = 0.182
Evidence Quality:     0.15 x 0.91 = 0.1365
Actionability:        0.15 x 0.93 = 0.1395
Traceability:         0.10 x 0.92 = 0.092

TOTAL: 0.186 + 0.182 + 0.182 + 0.1365 + 0.1395 + 0.092 = 0.918
```

**Weighted Composite: 0.918**
**Quality Gate: REVISE (0.85 - 0.91 band per quality-enforcement.md)**

**LLM-Tell Score: 0.72** (5 patterns found; structural rather than lexical; moderate density)
**Voice Authenticity Score: 0.78** (regression from draft 4; cleaning pass traded voice for polish)

---

### COMPARISON TO PRIOR ITERATION

Draft 4 scored 0.938 at iteration 3 and was accepted. Draft 5 scores 0.918 on this review. The delta (-0.020) is driven by:

1. **Internal Consistency dropped** (0.94 -> 0.91) because the "Do not deviate" contradiction with checkpoint philosophy became more visible after the cleaning pass removed surrounding conversational context that softened it. The repeated "every dimension" phrase is a new observation.

2. **Evidence Quality dropped** (0.92 -> 0.91) because the 80% claim, which was present in draft 4, is being scored more critically in a draft that was specifically cleaned for rigor. If the purpose of the cleaning pass was to tighten claims, the ungrounded 80% is a missed opportunity.

3. **Voice Authenticity dropped** (est. 0.85 -> 0.78) because the cleaning pass systematically traded conversational warmth for editorial polish. Three specific regressions documented above.

The cleaning pass improved some LLM tell patterns (lexical) but introduced others (structural). The net effect on the deliverable is slightly negative: draft 4 was rougher but more authentic; draft 5 is smoother but less alive.

---

### S-010 RECOMMENDATION: TARGETED REVISION

**Priority fixes (address these to clear the quality gate):**

1. Ground or hedge the 80% claim (Issue 2, HIGH). One sentence fix.
2. Revise "Do not deviate" executor prompt to model checkpoint practice (Issue 6, MEDIUM). Directly contradicts the article's own thesis.
3. Break the parallel triplet in Line 17 (Tell 1, HIGH). Most visible LLM tell.

**Secondary fixes (voice and polish):**

4. Restore conversational warmth in McConkey introduction (Voice Regression 1).
5. Add a transitional hook before the Two-Session Pattern section (Voice Regression 2).
6. Vary the bullet structure in Lines 39-43 (Tell 3, MEDIUM).
7. Soften "fluency-competence gap" attribution from "It's called" to "You could call this" (Issue 4, MEDIUM).

**Judgment calls (author discretion):**

8. Title revision (Issue 1, HIGH -- but title choice is subjective).
9. "Training-data gravity" explanation (Issue 3, MEDIUM).
10. Closing "I dare you" (Issue 9, LOW).

This is not a structural rewrite. It is a voice-restoration and claim-tightening pass. The cleaning that produced draft 5 overcorrected toward editorial polish at the expense of the personality that made draft 4 effective. The revision should restore warmth while keeping the rigor improvements.
