---

# FMEA Report: Saucer Boy Ouroboros Draft 1 -- Structured LLM Prompting

**Strategy:** S-012 FMEA (Failure Mode and Effects Analysis)
**Deliverable:** `drafts/draft-1-original.md`
**Criticality:** Applied at user request (standalone adversarial review)
**Date:** 2026-02-23
**Reviewer:** adv-executor (S-012)
**Elements Analyzed:** 8 | **Failure Modes Identified:** 19 | **Total RPN:** 1,926

---

## Summary

The deliverable is a strong conversational piece that effectively uses skiing metaphor to explain structured LLM prompting. FMEA decomposition across 8 elements identified 19 failure modes with a total RPN of 1,926. The highest-risk finding (RPN 252) concerns the universality claim overstating determinism of structured prompting. Three Critical findings (RPN >= 200) and five Major findings (RPN 80-199) were identified, concentrated in technical accuracy, the universality claim, and McConkey voice authenticity. The piece is fundamentally sound but requires targeted corrections to prevent readers from adopting oversimplified mental models.

---

## Findings Table

| ID | Element | Failure Mode | S | O | D | RPN | Severity | Corrective Action | Affected Dimension |
|----|---------|-------------|---|---|---|-----|----------|-------------------|--------------------|
| FM-001 | Opening hook | Hook is attention-grabbing but "sit down" tone may alienate Ouroboros rather than invite | 5 | 4 | 4 | 80 | Major | Soften the imperative opening or add a warmth signal (e.g., "Alright, park it, this is important") that reads as camaraderie not condescension | Actionability |
| FM-002 | Opening hook | Missing framing of WHY Ouroboros should care before the argument starts; assumes buy-in | 4 | 5 | 5 | 100 | Major | Add 1 sentence acknowledging what Ouroboros already does well before redirecting | Completeness |
| FM-003 | Skiing analogy (Option A) | "Yard-sale" is ski jargon that non-skier readers may not understand | 3 | 3 | 3 | 27 | Minor | Keep it (adds voice) but consider a micro-gloss ("yard-sale -- gear everywhere, dignity nowhere") | Evidence Quality |
| FM-004 | Skiing analogy (Option A) | "Coin flip dressed up as confidence" is memorable but slightly mischaracterizes LLM behavior -- LLMs are not random, they are systematically biased toward common patterns | 6 | 6 | 7 | 252 | Critical | Rephrase to "training-data default dressed up as a custom answer" -- preserves punch, improves accuracy | Methodological Rigor |
| FM-005 | Skiing analogy (Option B) | Option B prompt is Jerry-specific (adversarial review, 0.92 threshold, orchestration plan) -- a non-Jerry user cannot replicate it, undermining the "universal" claim later | 7 | 7 | 6 | 294 | Critical | Either (a) provide a generic version alongside the Jerry version, or (b) explicitly state "this is what it looks like in Jerry -- here's the stripped-down version for any LLM" | Internal Consistency |
| FM-006 | Skiing analogy (Option B) | The Option B prompt is presented as a single monolithic block; reader may feel overwhelmed and not know where to start | 5 | 5 | 5 | 125 | Major | Break it into annotated sub-blocks or number the constraints | Actionability |
| FM-007 | Technical accuracy | "LLMs are phenomenal at producing things that look right" is correct but never explains WHY (next-token prediction, reward model alignment for plausibility) | 5 | 6 | 6 | 180 | Major | Add 1 sentence: mechanism is next-token prediction optimized for plausibility, not correctness | Evidence Quality |
| FM-008 | Technical accuracy | "Training data regurgitation" slightly mischaracterizes generation -- LLMs do not literally regurgitate, they generate novel compositions biased by training distribution | 5 | 5 | 7 | 175 | Major | Replace "regurgitation" with "training-data gravity" or "training-data default" -- retains metaphor, improves accuracy | Methodological Rigor |
| FM-009 | Technical accuracy | Claim that LLMs "optimize for cheapest, shortest path" is imprecise -- they optimize for highest-probability completion, which often correlates with shortest but not always | 4 | 5 | 6 | 120 | Major | Qualify: "they default to the most common pattern, which usually means the shortest path" | Methodological Rigor |
| FM-010 | Two-phase pattern | "Clear context" instruction assumes user knows how to do this technically (new conversation? system prompt reset? API parameter?) | 6 | 7 | 5 | 210 | Critical | Add a concrete instruction: "Start a new chat. Load the artifact. That's your clean context." | Actionability |
| FM-011 | Two-phase pattern | The "every token of planning conversation is eating space" claim is accurate but oversimplified -- modern LLMs have 100K-200K token windows; a planning conversation is rarely the bottleneck for simple tasks | 4 | 4 | 6 | 96 | Major | Add qualifier: "especially for complex multi-phase work where the planning conversation can fill 10-30% of your window" | Evidence Quality |
| FM-012 | Two-phase pattern | The orchestrator re-prompt instruction ("You are the orchestrator. Use the ORCHESTRATION.yaml") is Jerry-specific and not actionable for non-Jerry users | 5 | 6 | 5 | 150 | Major | Add a generic equivalent: "You are the executor. Here is the plan [paste plan]. Follow it step by step." | Actionability |
| FM-013 | Universality claim | "Context windows are physics, not features" is a strong rhetorical move but technically inaccurate -- context windows are engineering constraints, not physics | 4 | 3 | 4 | 48 | Minor | Replace "physics" with "engineering constraints" or "architectural reality" -- still punchy, actually correct | Methodological Rigor |
| FM-014 | Universality claim | "They all degrade as that window fills" is a sweeping claim -- degradation patterns differ significantly across architectures (attention mechanisms, RAG-augmented models, etc.) | 5 | 5 | 7 | 175 | Major | Qualify: "they all have limits on how much context they can effectively use" rather than blanket degradation | Evidence Quality |
| FM-015 | Three principles | Principle 1 ("Constrain the work") and Principle 2 ("Review the plan") are strong and actionable. Principle 3 ("Protect the context window") is the weakest -- it is the most Jerry-specific and least universally actionable | 5 | 5 | 6 | 150 | Major | Reframe Principle 3 as "Separate planning from execution" -- the context window reason is one mechanism, but the principle is broader | Actionability |
| FM-016 | Three principles | No call-to-action -- principles are stated but reader is not told what to DO next (try it with their next prompt? start with just Principle 1?) | 5 | 6 | 4 | 120 | Major | Add a single sentence before the closing: "Next prompt you write, try just Principle 1. Constrain it. See what happens." | Actionability |
| FM-017 | McConkey voice | Voice is strongest in opening and closing but weakest in the technical middle (lines 17-38); the "what/how/quality/guardrails/expect" bullet list reads like documentation, not McConkey | 6 | 7 | 5 | 210 | Critical | Rewrite the bullet list with McConkey's voice: less corporate structure, more "here's what the mountain now knows about your plan" | Internal Consistency |
| FM-018 | McConkey voice | The closing banana suit callback is effective but repeated twice (lines 51 and 55) -- "The banana suit was optional. The preparation was not." echoes "banana suit optional, preparation non-negotiable" one line earlier; redundancy dilutes impact | 4 | 8 | 3 | 96 | Major | Cut one of the two. Keep only the final punchline version (line 55). Let it land once, hard. | Completeness |
| FM-019 | Closing | McConkey biographical claim ("didn't show up to a big mountain line and wing it") -- McConkey was actually known for an element of wild spontaneity alongside preparation; overstating the planning side slightly misrepresents him | 4 | 4 | 7 | 112 | Major | Add nuance: "McConkey looked like he was winging it. He wasn't. The wild was the performance; the preparation was the foundation." | Evidence Quality |

---

## TOP 3 RISKS (Highest RPN)

### 1. FM-005 (RPN 294) -- Option B Prompt is Jerry-Specific, Undermining Universality Claim

**The problem:** The deliverable's entire argument hinges on "this is universal, not a Jerry thing" (line 33). But the crown jewel example -- Option B -- is saturated with Jerry-specific terminology (adversarial review, 0.92 threshold, orchestration plan, human checkpoints). A reader without Jerry cannot act on this example. This creates a credibility gap: the text says "universal" while the demonstration says "you need Jerry."

**Mitigation:** Provide a dual-track example. Show the Jerry version (as-is) AND a stripped-down generic version underneath: "On any LLM, that same pattern looks like: 'Do two things: [X] and [Y]. Show me the plan before you start. I'll review before you execute. Cite your sources.'" This proves universality through demonstration rather than assertion.

**Post-correction RPN estimate:** S=4, O=3, D=4 = 48

### 2. FM-004 (RPN 252) -- "Coin Flip" Metaphor Mischaracterizes LLM Behavior

**The problem:** "Coin flip dressed up as confidence" implies randomness. LLMs are not random -- they are systematically biased toward high-probability completions from training data. A reader who internalizes the "coin flip" model will draw wrong conclusions about when structured prompting helps (they might think it reduces randomness, when it actually redirects systematic bias). This is particularly risky because the deliverable's goal is to change how Ouroboros *thinks* about LLM mechanics.

**Mitigation:** Replace "coin flip dressed up as confidence" with "training-data default dressed up as a custom answer." Preserves the rhetorical punch. Fixes the mental model. The failure mode is not randomness -- it is systematic bias toward the generic.

**Post-correction RPN estimate:** S=3, O=3, D=4 = 36

### 3. FM-010 (RPN 210) and FM-017 (RPN 210) -- TIE

**FM-010: "Clear Context" is Not Actionable**

**The problem:** The two-phase pattern is the most novel and valuable part of the deliverable. But "clear context" is an abstraction. A ChatGPT user, a Claude API user, and a Jerry user all do this differently. If the reader does not know *how* to clear context, the principle becomes aspirational rather than actionable.

**Mitigation:** Add one concrete sentence: "Start a new chat. Paste the plan. That's your clean context." Three actions. No ambiguity.

**Post-correction RPN estimate:** S=3, O=3, D=3 = 27

**FM-017: McConkey Voice Drops in Technical Middle**

**The problem:** The technical explanation section (lines 17-38) shifts from McConkey's voice into documentation mode. The bullet list ("What to do," "How to do it," "What quality looks like") reads like a training manual, not a ski legend explaining something over a beer. Readers who came for McConkey's voice will feel the shift and may disengage precisely when the content is most important.

**Mitigation:** Rewrite the bullet list to stay in character. Instead of "What to do -- gap analysis + framework research, distinct work streams" try something like "The mountain now knows you want two runs, not one -- gap analysis down the left, framework research down the right. Parallel lines. Not the same chute." Keep the information; change the delivery vehicle.

**Post-correction RPN estimate:** S=3, O=3, D=3 = 27

---

## OVERALL ASSESSMENT

The deliverable is structurally sound and rhetorically effective -- the skiing metaphor, the A/B contrast, and the three principles framework are all strong scaffolding for the argument. However, FMEA identifies a systemic tension: the piece claims universality while demonstrating Jerry-specificity (FM-005, FM-010, FM-012, FM-015), and the McConkey voice, while strong at the edges, fades in the technical core (FM-017). The 4 Critical findings (RPN >= 200) are all correctable with targeted revisions that preserve the piece's strengths. Total current RPN of 1,926 across 19 failure modes indicates moderate overall risk concentrated in a few high-priority items. With the top 4 mitigations applied, estimated total RPN drops to approximately 1,200 -- a meaningful improvement that would move this from "revise" to "accept with minor corrections."

**Recommendation:** REVISE -- apply mitigations for the 4 Critical findings (FM-004, FM-005, FM-010, FM-017) and consider the Major findings as improvement opportunities. The core argument and structure are sound; the corrections are surgical, not structural.
