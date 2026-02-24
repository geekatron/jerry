---

# Pre-Mortem Report: Saucer Boy Ouroboros Response (Draft 1)

**Strategy:** S-004 Pre-Mortem Analysis
**Deliverable:** `drafts/draft-1-original.md` -- Conversational response explaining structured LLM prompting to Ouroboros
**Date:** 2026-02-23
**Reviewer:** adv-executor (S-004)
**Goal:** Ouroboros reads this and fundamentally changes how they prompt LLMs
**Failure Scenario:** It is March 9, 2026. Ouroboros read the response two weeks ago. They thought it was a good read. They even shared it with a friend. But their actual prompting behavior has not changed. They still type vague, single-shot instructions into LLMs. The response failed to convert understanding into action.

---

## Summary

Seven failure causes identified across Assumption, Process, and Technical categories. The response is well-written and conceptually sound but suffers from a critical gap: it explains the *philosophy* of structured prompting without giving Ouroboros a concrete, repeatable procedure they can apply immediately. The three principles are correct but abstract. The skiing analogy is extended and vivid but may not land with someone who does not ski. The response reads more like a persuasive essay than a behavioral intervention -- and persuasive essays change minds, not habits.

**Recommendation:** REVISE with targeted additions (see Suggested Fixes).

---

## Failure Causes

### PM-001: No Actionable Template or Checklist (CRITICAL)

**Why it caused failure:** Ouroboros finished reading and thought "that makes sense." Then they opened Claude/ChatGPT and stared at the prompt box. They could not remember the three principles in the right order. They had no copy-pasteable template, no checklist, no "before you hit Enter, check these 5 things" artifact. The response gave them a *worldview* but not a *tool*. Behavioral change requires a friction-reducing artifact at the point of action. Without one, the old habit (type and send) wins every time.

**Impact:** HIGH

**Category:** Assumption (assumes understanding leads to behavior change)

**Affected dimension:** Actionability

**Suggested fix:** Add a concrete "Prompting Checklist" section at the end. Something Ouroboros can screenshot or copy. Five items max. Example:

```
Before you hit Enter:
[ ] Did I specify WHAT to do (not just the topic)?
[ ] Did I specify HOW I'll judge quality?
[ ] Did I tell it where I'll check its work?
[ ] Did I ask for the plan BEFORE the product?
[ ] Am I working in a clean context (or carrying planning baggage)?
```

This single addition would likely be the difference between "interesting read" and "behavior change."

---

### PM-002: The Example Prompt Is Intimidating, Not Aspirational (MAJOR)

**Why it caused failure:** The "Option B" prompt (lines 15-16) is a 90-word monster that references parallel streams, adversarial review, 0.92 thresholds, human checkpoints, and orchestration plans. For someone who currently writes "Evaluate the repo and apply top industry frameworks," this is not the next step -- it is the finish line of a marathon they have not started. The gap between their current behavior and the demonstrated ideal is so large that it triggers learned helplessness rather than motivation. They think "I could never prompt like that" rather than "I should try that."

**Impact:** HIGH

**Category:** Assumption (assumes reader can bridge the gap from vague to expert-level)

**Affected dimension:** Actionability

**Suggested fix:** Add an intermediate example. Show what a "Level 2" prompt looks like -- something that is only 2-3 sentences longer than their current prompt but dramatically better. Example: "Research the top 10 industry frameworks for [topic]. For each, cite the source. Then analyze this repo against the top 5. Show your work -- I want to see the criteria you used to narrow from 10 to 5." This bridges the gap. Then present Option B as the advanced version.

---

### PM-003: The Skiing Analogy Dominates and May Not Land (MAJOR)

**Why it caused failure:** The skiing metaphor is the structural spine of the entire piece (Option A/B framing, the McConkey closer, the "scout the line" callback). If Ouroboros does not ski -- or worse, finds ski culture alienating -- the entire persuasive architecture collapses. Even for skiers, the analogy is extended across 4 separate passages, which risks feeling forced. The "banana suit" reference (line 51-55) assumes knowledge of McConkey's iconic outfit. For someone who has never heard of Shane McConkey, the closer lands as nonsense rather than an inspiring callback.

**Impact:** MEDIUM

**Category:** Assumption (assumes shared cultural context)

**Affected dimension:** Completeness (persuasive completeness -- does it reach the actual audience?)

**Suggested fix:** Two options. (A) Add a one-sentence McConkey introduction early: "Shane McConkey was a legendary big-mountain skier -- the kind of guy who'd ski a cliff in a banana suit, but only after meticulously scouting the line." This makes the closer land even for non-skiers. (B) Add a brief non-skiing analogy as a secondary anchor -- cooking, music production, or writing code itself -- so readers who do not connect with skiing still have an on-ramp.

---

### PM-004: "Clear Context" Advice Is Unexplained and Confusing (MAJOR)

**Why it caused failure:** Line 29 says "you clear context" and "re-prompt with one clean instruction." For someone who does not understand context windows mechanically, this is mystifying. How do you "clear context"? Start a new chat? Close the tab? Is there a button? The response assumes technical understanding of context windows that Ouroboros may not have. If the reader does not know *how* to clear context in their specific tool, Principle 3 becomes aspirational philosophy rather than executable advice.

**Impact:** MEDIUM

**Category:** Technical (assumes technical knowledge the reader may lack)

**Affected dimension:** Actionability

**Suggested fix:** Add a parenthetical or brief instruction: "Clear context means start a new conversation. Copy the orchestration artifact (the plan) into a fresh chat. Do not continue in the same thread where you did the planning." Make it tool-agnostic but mechanically concrete.

---

### PM-005: The "0.92 Threshold" and "Adversarial Review" Are Jargon Grenades (MEDIUM)

**Why it caused failure:** The response drops Jerry-specific terminology ("0.92 threshold," "adversarial review," "orchestration plan," "semi-supervised") without translation. Even though lines 33-38 say "this is universal, not a Jerry thing," the Option B example and the explanation are saturated with Jerry vocabulary. Ouroboros reads it and thinks "this is a Jerry thing" despite the disclaimer. The jargon creates an in-group/out-group divide: people who use Jerry understand this; people who don't are on the outside looking in.

**Impact:** MEDIUM

**Category:** Process (communication failure -- jargon without translation)

**Affected dimension:** Evidence Quality (the examples should demonstrate universality, but the jargon undermines that claim)

**Suggested fix:** In the Option B example, translate Jerry-specific terms into universal equivalents inline. Instead of "adversarial review, 0.92 threshold," say something like "have it critique its own work before showing me -- and I want it to score itself on completeness, consistency, and evidence quality." The concept is the same; the vocabulary is accessible.

---

### PM-006: Wall of Text -- No Visual Breaks for Scanning (MEDIUM)

**Why it caused failure:** The response is 56 lines of dense prose with only 4 bold headers and one bulleted list. Lines 9-11 are a single paragraph that is 8 lines long. Lines 25-29 are another dense block. Ouroboros likely skimmed after the first few paragraphs. The three principles (the most important part) are buried 75% of the way through the document. In a world of TL;DR culture, the structural payoff comes too late.

**Impact:** MEDIUM

**Category:** Process (delivery format works against persuasion goal)

**Affected dimension:** Completeness (key content present but likely not consumed)

**Suggested fix:** (A) Move the three principles UP -- put them right after the Option A/B comparison, then use the rest of the response to elaborate. Front-load the actionable content. (B) Add a TL;DR at the very top with the three principles as a one-liner each. (C) Break the long paragraphs (especially lines 9-11 and 25-29) into shorter chunks.

---

### PM-007: No "Try This Right Now" Call to Action (MEDIUM)

**Why it caused failure:** The response ends with a philosophical closer about McConkey. It does not end with "Here is what I want you to do in your next LLM conversation." There is no challenge, no dare, no experiment. Behavioral psychology is clear: the most effective persuasion ends with a specific, low-friction action the reader can take immediately. Without it, the response gets filed under "interesting things I read" rather than "things I changed."

**Impact:** MEDIUM

**Category:** Assumption (assumes motivation will self-generate from understanding)

**Affected dimension:** Actionability

**Suggested fix:** End with a concrete challenge. Something in the McConkey voice: "So here's what you do. Next time you open Claude or ChatGPT, before you type a single word, write down three things: what you actually need, how you'll know if the answer is good, and what you want to see first. That's it. Three sentences before the prompt. Do that once and tell me it didn't change the output. I dare you."

---

## Practical Gaps Summary

| Gap | What is missing | Why it matters |
|-----|-----------------|----------------|
| Actionable template/checklist | No copy-pasteable artifact at point of action | Understanding does not equal behavior change |
| Intermediate example | Jump from vague to expert is too large | Reader cannot see the first step |
| "How to clear context" instructions | Mechanical step assumed but not explained | Principle 3 is unexecutable |
| Jargon translation | Jerry vocabulary used in "universal" examples | Undermines the universality claim |
| Immediate call to action | No "do this now" ending | No behavioral trigger |

---

## Memorability Assessment

**The three principles:**
1. "Constrain the work" -- MEMORABLE. Short, punchy, clear.
2. "Review the plan, not just the product" -- MEMORABLE. Counterintuitive enough to stick. The "plan before product" inversion is strong.
3. "Protect the context window" -- WEAK MEMORABILITY. This is the most technical of the three and the least intuitive. "Protect" is passive. For a non-technical reader, "context window" is jargon. Consider rephrasing to something like "Clean slate for execution" or "Plan in one conversation, build in another."

**The skiing analogy:** Moderately memorable for skiers. Likely forgettable for non-skiers. The "banana suit" line is the most memorable single image in the piece, but only if you know McConkey.

**The Option A / Option B structure:** STRONG. This is the most effective rhetorical device in the piece. The contrast is vivid and immediate. This is what Ouroboros will remember.

**Overall:** The piece has 2-3 memorable moments but they are buried in dense prose. The three principles need to be more prominent (visually and positionally) to serve as the "takeaway" that sticks.

---

## Suggested Fixes (Priority Order)

| Priority | Fix | Addresses |
|----------|-----|-----------|
| P0 | Add a prompting checklist (5 items max, copy-pasteable) at the end or as a callout | PM-001 |
| P0 | Add an intermediate "Level 2" example prompt between vague and expert | PM-002 |
| P1 | Add a concrete call-to-action/challenge as the final paragraph (before or integrated with the McConkey closer) | PM-007 |
| P1 | Add a one-sentence McConkey introduction for non-skiers | PM-003 |
| P1 | Explain "clear context" mechanically (start a new chat, copy the plan) | PM-004 |
| P1 | Translate Jerry jargon in the Option B example to universal language | PM-005 |
| P2 | Move the three principles higher in the document; add TL;DR | PM-006 |
| P2 | Rephrase Principle 3 for non-technical memorability | Memorability |

---

## Overall Assessment

The response is an excellent first draft -- the voice is strong, the Option A/B contrast is the best rhetorical device in the piece, and the core argument is correct. But it will fail to change behavior because it is structured as a *persuasive essay* rather than a *behavioral intervention*. It convinces the reader that structured prompting is better but does not give them a concrete, low-friction way to start doing it. The two highest-impact fixes are (1) adding a copy-pasteable checklist and (2) adding an intermediate example that shows the reader their realistic next step, not the finish line. With those additions, this has a genuine chance of changing how Ouroboros prompts.
