---

**STRATEGY:** S-013 Inversion Technique
**DELIVERABLE:** Saucer Boy conversational response on structured LLM prompting (draft 1)
**DATE:** 2026-02-23
**REVIEWER:** adv-executor (S-013)

---

## FAILURE MODES

### FM-01: The "Works for Me" Dismissal [LIKELIHOOD: HIGH]

**Failure scenario:** Ouroboros has gotten decent results from vague prompts -- maybe not world-class, but good enough for their use case. The piece asserts vague prompting produces "a coin flip dressed up as confidence" and "the illusion of rigor," but never acknowledges that vague prompting *can* produce acceptable results for low-stakes tasks. This absolute framing invites an immediate "well actually, I got good results without all that" pushback, which causes the reader to discount the entire argument.

**Mitigation:** Add a brief acknowledgment (1-2 sentences) that vague prompting sometimes works for simple, low-stakes tasks -- the structured approach pays off when the work matters, when compound errors across phases are expensive, or when you need reproducibility. The skiing metaphor actually supports this naturally: you can wing it on a green run, but not on a big mountain line. Sharpen that distinction.

---

### FM-02: Overwhelming Complexity Causes Rejection [LIKELIHOOD: HIGH]

**Failure scenario:** The Option B prompt example (lines 15-16) is a wall of requirements: "gap analysis," "top 10 frameworks," "real sources," "narrow to 5," "cross-pollinate," "citations," "adversarial review," "0.92 threshold," "three iterations," "human checkpoints," "orchestration plan." For someone who currently writes one-sentence prompts, this looks like going from zero to NASA mission control. The gap between where Ouroboros is and where the advice points is so large that the reaction is "I'm not doing all that" rather than "let me try this." The piece offers no intermediate step.

**Mitigation:** Add a stepping-stone. After the three principles, include a short "start here" example -- a prompt that is structured but not overwhelming. Something like: "Even just adding 'show me your plan before executing, and cite your sources' to any prompt will dramatically improve output. You don't have to go full orchestration on day one." This gives Ouroboros an on-ramp.

---

### FM-03: The "This Only Works with Jerry" Objection [LIKELIHOOD: MEDIUM]

**Failure scenario:** Despite the explicit "this is universal" section (lines 33-38), the Option B example is saturated with Jerry-specific terminology: "adversarial review," "0.92 threshold," "orchestration plan," "dispatch to agents," "ORCHESTRATION.yaml." A reader unfamiliar with Jerry will read Option B and think "this requires a framework I don't have." The universal claim is stated but not *demonstrated* -- every concrete example is Jerry-flavored.

**Mitigation:** Add one concrete example of the pattern applied *without* Jerry -- a raw ChatGPT or Claude API prompt that uses the same principles (constrain, review the plan, protect context) without any framework terminology. This converts the "universal" claim from assertion to demonstration.

---

### FM-04: Context Window Clearing is Not Universally Available [LIKELIHOOD: MEDIUM]

**Failure scenario:** Principle 3 ("Protect the context window") tells the reader to "clear context, load artifacts, execute" -- but most consumer LLM interfaces (ChatGPT web, Claude.ai) don't have a "clear context and load artifact" button. The reader would need to manually start a new conversation and paste in their plan. The piece treats this as a simple operation ("the key move") but does not explain the mechanics for someone outside a CLI or API workflow. This creates a "sounds great but how do I actually do that?" gap.

**Mitigation:** Add a parenthetical or brief note explaining the practical mechanics: "Start a fresh conversation, paste in your finalized plan, and prompt from there. The key is: don't keep the 40 messages of planning debate in the same thread as the execution." This makes the advice actionable for any interface.

---

### FM-05: The "LLMs Degrade as Context Fills" Claim is Unsubstantiated [LIKELIHOOD: MEDIUM]

**Failure scenario:** The piece states "They all degrade as that window fills" (line 35) as established fact. While this is broadly true (and supported by "lost in the middle" research), it is stated without any evidence, citation, or even anecdotal support. A skeptical reader -- especially one who has had long productive conversations with LLMs -- could challenge this as unproven assertion. The entire rationale for Principle 3 rests on this claim.

**Mitigation:** Add a concrete illustration or a brief "you've probably noticed" appeal to experience: "Ever notice how a long conversation starts repeating itself, or forgets what you said 30 messages ago? That's context fill degradation in action." This grounds the claim in the reader's own experience rather than leaving it as bare assertion.

---

### FM-06: No Acknowledgment of When Structured Prompting Fails or is Counterproductive [LIKELIHOOD: MEDIUM]

**Failure scenario:** The piece presents structured prompting as universally better. But there are legitimate scenarios where heavy structure is counterproductive: creative brainstorming (where constraints kill divergent thinking), exploratory conversations (where the point is to meander), rapid prototyping (where the overhead of planning exceeds the value), and simple factual queries. By not acknowledging these, the piece is vulnerable to cherry-picked counterexamples that undermine credibility.

**Mitigation:** Add a brief caveat, ideally within the skiing metaphor: "If you're just cruising groomers -- asking a quick factual question, brainstorming, riffing -- you don't need a flight plan. This is for the big lines. The work that matters." This pre-empts the counterexample attack without weakening the core argument.

---

### FM-07: The "Review the Plan" Step Has a Chicken-and-Egg Problem [LIKELIHOOD: LOW]

**Failure scenario:** Principle 2 says "review the orchestration plan" before execution. But if Ouroboros doesn't know what a good plan looks like, they can't meaningfully review one. They'll either rubber-stamp it (defeating the purpose) or spend as much time learning to evaluate plans as they would have spent fixing bad outputs. The piece assumes the reader has the expertise to judge plan quality.

**Mitigation:** Add brief guidance on what to look for in a plan: "Does it have distinct phases? Does it specify what 'done' looks like for each phase? Does it include quality checks? If the plan is just 'Step 1: do the thing, Step 2: done' -- push back." This equips the reader to actually execute the advice.

---

### FM-08: The Skiing Metaphor Excludes Non-Skiers [LIKELIHOOD: LOW]

**Failure scenario:** The entire argument is structured around a skiing metaphor and a McConkey reference. Ouroboros (and any secondary audience) who has never skied will not connect with "yard-sale," "big mountain line," "scoped the line," "checked the snowpack," or "banana suit." The metaphor that is supposed to make the argument accessible could make it opaque to a significant portion of readers.

**Mitigation:** This is a persona-appropriate choice (Saucer Boy IS McConkey), so the mitigation is not to remove the metaphor but to ensure the non-metaphorical explanation is strong enough to stand alone. Check: if you remove every skiing sentence, does the argument still make complete sense? Currently it does -- the three principles section (lines 41-47) is metaphor-free and self-contained. No change needed here, but worth confirming during revision that the non-metaphor track remains complete.

---

## UNADDRESSED COUNTERARGUMENTS

1. **"I tried structured prompting and the LLM ignored half my constraints anyway."** This is a real and common experience. LLMs DO drop constraints, especially long ones. The piece does not address what to do when the LLM fails to follow the structured prompt. Mitigation: acknowledge this and position the plan-review step as the defense -- by checking the plan first, you catch dropped constraints before they propagate.

2. **"Isn't the planning conversation itself going to degrade the context window? You're spending tokens on planning that could be spent on execution."** The piece implicitly addresses this via the "clear context" step, but never confronts the objection head-on. The planning phase itself consumes time and tokens. Mitigation: explicitly state the trade-off -- "Yes, planning costs tokens and time. But 20 minutes of planning saves 3 hours of re-prompting garbage outputs."

3. **"The 0.92 threshold, adversarial review, three iterations -- this sounds like enterprise process theater. I just want good outputs."** The Option B example leads with heavy process. For someone allergic to process overhead, this reads as bureaucracy. Mitigation: separate the principles (universal) from the implementation (Jerry-specific) more clearly. The three principles are the advice; the specific thresholds and review loops are one implementation.

4. **"If the LLM can't figure out what I want from a simple prompt, maybe the LLM is the problem, not my prompt."** This is a philosophical objection -- the burden of understanding should be on the tool, not the user. The piece doesn't address this worldview. Mitigation: the aviation analogy helps here -- "You wouldn't give a pilot 'fly somewhere nice' as a flight plan. Tools that take precise instructions work precisely. Tools that take vague instructions produce vague results. That's not a bug."

---

## HIDDEN ASSUMPTIONS

1. **Ouroboros is persuadable by logical argument.** The piece presents a reasoned case. But if Ouroboros's attachment to vague prompting is emotional (identity-based: "I'm an intuitive user, not a process person"), logical argument alone won't land. The McConkey persona helps here by making structure feel cool rather than bureaucratic, but this assumption is worth noting.

2. **Ouroboros has the patience to read 56 lines of advice.** The piece is long for a conversational response. If the reader skims, they may get "structured prompting good, vague prompting bad" without absorbing the actionable three principles or the two-phase pattern.

3. **The reader has access to tools that support the described workflow.** Context clearing, artifact loading, and re-prompting assume a workflow that is easy in a CLI/API context but awkward in consumer chat interfaces.

4. **"Quality" means the same thing to Ouroboros as it does to the author.** The piece assumes the reader values rigor, evidence, and reproducibility. If Ouroboros values speed and "good enough," the argument for heavy structure may not resonate.

5. **One compelling explanation is sufficient to change behavior.** Behavior change research consistently shows that understanding alone is insufficient -- practice, feedback, and reinforcement are required. The piece explains beautifully but provides no path to practice.

6. **The LLM will reliably produce a better orchestration plan when given structured input.** This is generally true but not guaranteed. The LLM may produce a plan that looks structured but contains the same hallucinated substance as the vague output, just organized more neatly. Structure is necessary but not sufficient.

---

## SUGGESTED MITIGATIONS (prioritized)

**Must address (High-likelihood failure modes):**

1. **Add an on-ramp.** After the three principles, add 2-3 sentences with a minimal starter prompt that applies the principles without the full orchestration overhead. Addresses FM-02.

2. **Acknowledge that vague prompting works for simple tasks.** One sentence, ideally within the skiing metaphor. "You don't need a flight plan for the bunny hill." Addresses FM-01 and FM-06.

3. **Add one non-Jerry example.** A raw, framework-free prompt demonstrating the three principles in action on any LLM. Addresses FM-03.

**Should address (Medium-likelihood failure modes):**

4. **Explain context clearing practically.** One parenthetical: "Start a new conversation, paste in your plan." Addresses FM-04.

5. **Ground the context degradation claim.** One sentence of appeal to reader experience. Addresses FM-05.

6. **Address the "LLM ignored my constraints" counterargument.** One sentence noting that the plan-review step catches this. Addresses Counterargument 1.

**May address (Low-likelihood or persona-appropriate):**

7. **Add brief plan-review guidance.** What makes a good plan vs. a bad one, in one sentence. Addresses FM-07.

8. **No action needed on FM-08** (skiing metaphor) -- persona-appropriate and non-metaphorical track is self-sufficient.

---

## OVERALL ASSESSMENT

The deliverable is a strong, voice-authentic explanation that nails the core insight (constrain, review the plan, protect context). Its primary vulnerability is not in what it says but in what it omits: it offers no on-ramp for beginners (FM-02, highest risk), no acknowledgment that the advice has scope limits (FM-01, FM-06), and no framework-free demonstration of the universal claim (FM-03). Addressing the top three mitigations would close the most likely failure modes without diluting the McConkey voice or the argument's force.
