---

## S-003 STEELMAN REVIEW

**STRATEGY:** S-003 Steelman Technique
**DELIVERABLE:** `drafts/draft-1-original.md`
**REVIEWER:** adv-executor (S-003)

---

### STRONGEST ASPECTS

**1. The skiing metaphor is structurally load-bearing, not decorative.**
The Option A / Option B framing (pointing downhill and hoping vs. scouting the line) is the single strongest move in this piece. It does exactly what the canonical persona document demands: the metaphor is transparent to someone who has never skied. "You pointed downhill and hoped" requires zero skiing knowledge to parse. This passes Authenticity Test 3 (new developer legibility) cleanly. The metaphor also maps precisely to the technical claim -- vague prompt = unscoped input, structured prompt = constrained execution. The isomorphism is genuine, not forced.

**2. The "illusion of rigor" diagnosis is the technical heart of the piece, and it is correct.**
Lines 10-11 -- "LLMs are phenomenal at producing things that look right... The illusion of rigor" -- is the single most important technical claim in the deliverable. It accurately describes the failure mode of underspecified prompts: the output is syntactically plausible, structurally clean, and substantively hollow. This is well-documented LLM behavior (attention mechanisms distribute weight across training data patterns when no constraints narrow the distribution). The piece names the problem without hedging. This is the Direct voice trait at its best.

**3. The three principles at the end are actionable and memorable.**
"Constrain the work. Review the plan, not just the product. Protect the context window." These are concrete, sequential, and non-obvious (especially principle 3). A reader could walk away with these three sentences and improve their prompting immediately. This passes the Actionability dimension.

**4. The two-phase pattern explanation (lines 25-31) is genuinely pedagogical.**
The insight that you plan in one context and execute in a clean context -- and the explanation of why (context window is finite, planning tokens compete with execution tokens) -- is the most technically valuable paragraph in the piece. Most LLM users do not understand this. The piece explains it without condescension.

**5. The closing McConkey callback (lines 51-55) lands.**
"McConkey didn't show up to a big mountain line and wing it" -- this is the Steelman move that the piece itself makes: it takes the persona and uses it to reinforce the argument, not to decorate it. The repetition structure ("The banana suit was optional. The preparation was not.") is effective rhetoric. It passes Authenticity Test 5 (genuine conviction).

**6. The universality argument (lines 33-38) prevents tribal dismissal.**
By explicitly stating "this is universal -- not a Jerry thing," the piece preempts the most likely objection ("this only works with your specific framework"). This is strategically placed after the Jerry-specific example and before the general principles.

---

### UNDERSTATED ARGUMENTS

**1. The "garbage compounding" insight (line 27) deserves more weight.**
The current text: "once garbage enters the pipeline, it compounds. Every phase downstream builds on a weak foundation. Garbage in, garbage out -- but worse, because each phase adds a layer of confident-sounding polish to the garbage underneath."

This is the single most important insight in the entire piece for anyone running multi-phase workflows, and it is buried inside a paragraph about reviewing the orchestration plan. The compounding error problem is the fundamental reason why plan review matters -- it is not an aside.

**Suggestion:** Elevate this to its own short paragraph or give it structural emphasis (bold the key sentence, or break it out as a standalone observation between the plan review discussion and the context-clearing discussion). Something like:

> And here's the part that bites: once garbage enters the pipeline, **it compounds**. Each downstream phase adds confident-sounding polish to a weak foundation. By phase three, the output looks authoritative. The errors are load-bearing. That's not garbage in, garbage out -- it's garbage in, polished garbage out, and you can't tell the difference until something breaks.

**2. The evidence requirement in Option B is mentioned but not explained.**
Line 15 includes "Evidence required -- citations, sources, references" but the piece never explains *why* evidence constraints matter for LLM output specifically. The reason is important: without an explicit evidence requirement, the LLM will generate plausible-sounding claims from training data patterns without grounding them in verifiable sources. The evidence constraint forces the model to either retrieve real sources (if it has tool access) or explicitly flag when it cannot cite a source. This is a significant behavioral difference that is worth one sentence of explanation.

**Suggestion:** After the bullet list (lines 19-23), add a sentence like:

> The evidence requirement is not paperwork. Without it, the LLM generates claims that *sound* sourced. With it, the model is forced to either find real sources or tell you it can't. That's the difference between research and confident hallucination.

**3. The "completion machine" insight (line 27) is stated as a passing remark.**
"It's a completion machine" is technically precise -- LLMs are next-token predictors that optimize for the highest-probability continuation. This is the foundational reason why explicit constraints matter: without them, the model follows the path of least resistance through its probability distribution. This deserves slightly more emphasis because it is the *mechanism* behind everything else the piece argues.

**Suggestion:** This does not need a full paragraph, but a brief parenthetical expansion would strengthen it: "Because the LLM will, by default, optimize for the cheapest, shortest path -- it's a completion machine, and completion machines take the path of highest probability, which is rarely the path of highest rigor."

**4. The "what you expect back first -- the plan, not the product" bullet (line 23) is strong but could be strengthened with the why.**
This is a non-obvious and critical point. Most users expect the LLM to produce the final deliverable. Asking for the plan first is a meta-cognitive constraint that forces the model to make its reasoning visible before committing to execution. Adding "because you can't evaluate a process you can't see" or similar would make the bullet more persuasive.

---

### MISSING ARGUMENTS

**1. No mention of attention mechanism degradation with context fill.**
The piece discusses context window as finite space (lines 29, 35) but does not mention that LLM performance degrades *before* the window is full. Attention mechanisms lose focus as context grows -- this is a well-documented property (the "lost in the middle" phenomenon). This would strengthen Principle 3 ("Protect the context window") by making the case that it is not just about running out of room; it is about the model becoming progressively less attentive to earlier tokens as the window fills. Even one sentence would add significant persuasive weight:

> "And it's not just that the window fills up. The model's attention degrades before it runs out of space. Instructions at the beginning of a long context get less weight than instructions at the end. Your carefully crafted constraints are the first thing the model starts ignoring."

**2. No mention of the role of structured output formats.**
The piece focuses on input structure (how to prompt) but does not mention that requesting structured output (specific formats, sections, schemas) also constrains the model's behavior. Structured output requests reduce the space of acceptable completions, which improves quality. This is a natural extension of Principle 1 and would give the reader one more concrete tool.

**3. No explicit acknowledgment that Ouroboros's original approach is what most people do.**
The piece opens with "sit down, let me explain this" but never normalizes the mistake. A single sentence acknowledging that vague prompting is the default behavior -- and that it *appears* to work because the output looks good -- would make the piece less preachy and more collaborative. McConkey's voice was inclusive, not lectorial. Something like: "And look -- everybody starts here. The output looks good enough that you don't know you're missing something until you've built on top of it."

**4. The human-in-the-loop argument could be stronger.**
Line 22 mentions "semi-supervised, human gates, no autonomous decisions on high-stakes output" but the piece does not explain why human checkpoints matter specifically for LLM workflows. The reason: LLMs cannot reliably self-assess output quality at scale. Self-assessment is itself a completion task, and the model will tend to rate its own output favorably. Human gates break this self-referential loop. This would strengthen the quality gate argument.

---

### PERSUASIVE STRUCTURE

The argument builds effectively through four stages:

1. **Hook** (skiing metaphor, lines 7-11): Accessible analogy that frames the problem
2. **Diagnosis** (lines 9-11): Names the failure mode with precision
3. **Prescription** (lines 13-31): Shows what good looks like, with specific examples
4. **Generalization** (lines 33-47): Extracts universal principles

This is a sound rhetorical structure. The move from concrete example (Option A vs. Option B) to abstract principles (the three principles) follows the inductive reasoning pattern that works best for teaching: show me, then tell me.

**One structural concern:** The two-phase pattern (lines 25-31) is the most technically novel content in the piece, but it is wedged between the Option B walkthrough and the universality argument. It could benefit from slightly more structural separation -- a subheading or a horizontal rule -- to signal that this is a distinct and important idea, not a continuation of the Option B description.

**The closing is strong.** The McConkey callback at the end works as a bookend because the opening metaphor was skiing. The piece opens with skiing, moves through LLM mechanics, and closes with McConkey. The frame holds.

---

### VOICE AUTHENTICITY ASSESSMENT

The voice is **genuine, not performative**. Evidence:

- **Direct trait:** Present throughout. "That's pointing downhill and hoping." No hedging, no preamble.
- **Warm trait:** The "sit down, let me explain" opening is peer-to-peer, not superior-to-inferior.
- **Confident trait:** "Context windows are physics, not features" -- this is the Confident trait at full expression. No apologetics.
- **Occasionally Absurd trait:** Appropriately absent. This is a teaching moment, not a celebration. The persona document is clear that humor is deployed "when earned," and a pedagogical explanation of prompting mechanics is not a humor context.
- **Technically Precise trait:** All LLM claims are accurate. Context windows are finite. Models optimize for completion. Quality degrades with vague inputs. No claim requires correction.

**Persona fidelity against canonical source:** The piece passes all five Authenticity Tests:
- Test 1 (Information completeness): Strip the voice and the technical content stands alone.
- Test 2 (McConkey plausibility): This reads like someone who knows the subject deeply and explains it without condescension -- consistent with McConkey's approach to innovation advocacy.
- Test 3 (New developer legibility): No insider knowledge required.
- Test 4 (Context match): The energy is medium-to-high -- appropriate for a teaching/explanation context per the Audience Adaptation Matrix.
- Test 5 (Genuine conviction): The voice comes from belief, not from template. The "Context windows are physics, not features" line is the clearest evidence of this.

**One minor voice concern:** The opening "Alright, sit down" has a faint lecturing quality. McConkey's documented communication style was inclusive, not instructional. The phrase "sit down" can read as commanding rather than inviting. Consider softening to "Alright, here's the thing" or "Alright, let me walk you through this" -- which preserves the directness while removing the implied authority position.

---

### OVERALL ASSESSMENT

This is a strong draft that accurately explains why structured prompting works, using a McConkey voice that is authentic rather than performative. The skiing metaphor is structurally sound and transparent. The three principles are actionable and memorable. The primary opportunities for strengthening are: (1) elevating the "garbage compounds" insight from a buried aside to a structural argument, (2) adding one sentence on attention degradation to strengthen the context window principle, (3) normalizing the vague-prompting mistake to make the tone more inclusive, and (4) explaining the *why* behind evidence requirements rather than just stating them. The voice authenticity is high -- it passes all five canonical Authenticity Tests -- with one minor adjustment recommended on the opening line's commanding tone.
