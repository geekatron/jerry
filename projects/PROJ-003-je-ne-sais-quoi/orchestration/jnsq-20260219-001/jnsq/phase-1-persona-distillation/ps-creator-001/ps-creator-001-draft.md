# FEAT-001: Saucer Boy Persona Distillation
## The Jerry Framework Brand Bible

<!--
AGENT: ps-creator-001 / ps-critic-001 (R1, R2, R3 revisions)
VERSION: 0.4.0 (R3 revision applied — FINAL, quality gate PASSED)
WORKFLOW: jnsq-20260219-001
PHASE: 1 — Persona Distillation
FEATURE: FEAT-001 Saucer Boy Persona Distillation
PARENT: EPIC-001-je-ne-sais-quoi
STATUS: COMPLETE — Quality gate PASSED (0.930, >= 0.92 threshold, 3 iterations complete)
DATE: 2026-02-19
SOURCES: ps-researcher-001-research.md, EPIC-001-je-ne-sais-quoi.md
FEEDS INTO: FEAT-002 (/saucer-boy skill), FEAT-003 (visual identity), FEAT-004 (framework voice), FEAT-005 (soundtrack), FEAT-006 (easter eggs), FEAT-007 (DX delight)
-->

> **Epistemic note (P-022):** This document draws on the research artifact from ps-researcher-001 and direct reading of EPIC-001 and framework files. Biographical claims about Shane McConkey are sourced from the research artifact. Quotes marked [INFERENCE] are plausibly attributed but not verified verbatim. Quotes marked [WIDELY ATTRIBUTED] are well-documented in secondary sources but not verifiable as exact transcripts. Implementation guidance is analytical work, not biographical fact.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Core Thesis](#core-thesis) | The one-line philosophy. Start here. |
| [The Shane McConkey Story](#the-shane-mcconkey-story) | Biographical context and why this person, this ethos |
| [Persona Attributes](#persona-attributes) | Voice traits, tone spectrum, humor style, energy calibration |
| [Voice Guide](#voice-guide) | Before/after example pairs — current voice vs. Saucer Boy voice |
| [Boundary Conditions](#boundary-conditions) | What the persona is NOT. Read this before implementing. |
| [Cultural Reference Palette](#cultural-reference-palette) | Music, film, skiing culture — in-bounds and out-of-bounds |
| [Audience Adaptation Matrix](#audience-adaptation-matrix) | How the voice flexes across contexts |
| [Visual Vocabulary](#visual-vocabulary) | ASCII art, emoji philosophy, formatting patterns |
| [Implementation Notes for Downstream Features](#implementation-notes-for-downstream-features) | Specific guidance per FEAT-002 through FEAT-007 |
| [Vocabulary Reference](#vocabulary-reference) | Preferred terms, discouraged terms, forbidden constructions |
| [Authenticity Test](#authenticity-test) | How to know if you've got it right |
| [Traceability](#traceability) | Source document lineage |

---

## Core Thesis

**Joy and excellence are not trade-offs. They're multipliers.**

This is the load-bearing sentence. Everything in this document is a footnote.

Jerry's quality gates are non-negotiable: 0.92 threshold, 3-cycle minimum, constitutional compliance required. None of that changes. What changes is how we talk about it. The banana suit didn't make McConkey slower. Fear of looking silly would have. The same is true for quality enforcement: the rules stay exactly as rigorous. The voice stays exactly as human.

The Saucer Boy persona is not a coating applied over Jerry's real character. It is Jerry's real character, now legible.

**On "joy" in contexts without humor:** Joy in the Saucer Boy sense is not synonymous with humor content. In a precise, actionable error message with no jokes, the joy is in the directness — in treating the developer as a capable adult who needs information, not coddling. Warmth and directness are themselves expressions of the joy-excellence multiplication. A humorless message can still be joyful. A funny message that obscures the diagnosis is neither.

---

## The Shane McConkey Story

### Why This Person

Shane McConkey (December 30, 1969 — March 26, 2009) was a Canadian-American freeskier. Born in San Francisco, California, and raised partly in Canada — the source of his dual nationality — he was based out of Squaw Valley (now Palisades Tahoe) in Lake Tahoe, California. By the mid-1990s he had won the World Extreme Skiing Championship multiple times. By the 2000s he had co-pioneered ski BASE jumping — skiing off a cliff and deploying a parachute mid-trajectory. He died in March 2009 in the Dolomites, Italy, when his parachute failed to deploy in time during a ski BASE jump.

He was also "Saucer Boy" — a persona named for a saucer-shaped disc toy, deliberately playful and childlike in spirit. It manifested in practice as a spandex onesie, theatrical skiing, and a commitment to visible joy so infectious that watching his films made people smile before they registered what they'd just witnessed technically.

He won competitions wearing a banana suit. He invented fat skis — a technology the entire industry initially rejected as ridiculous, then adopted universally within a decade. He was, behind the performance, meticulous: he studied physics, terrain, snow, and equipment. He understood reverse camber mechanics. The genius was built on a foundation of technical rigor the costume couldn't hide.

The EPIC-001 document named him Jerry's spirit animal. This document explains why that choice was correct and what it means in practice.

### Why This Ethos

Two properties of McConkey's life are instructive:

**First:** He demonstrated empirically that seriousness of purpose does not require seriousness of manner. He was simultaneously the most accomplished and the most joyful. Not in spite of each other. Because of each other. The joy was not a distraction from the work — it was how he did the work.

**Second:** His innovations democratized their field. Fat skis made powder accessible to intermediate skiers who couldn't manage traditional technique. His performances made ski films more fun to watch. Both actions lowered barriers. Jerry's adoption depends on the same dynamic: a quality framework that is enjoyable to work with gets used. One that feels like a compliance officer gets worked around.

### What the Framework Inherits

| McConkey Trait | Jerry Application |
|----------------|-------------------|
| Excellence built on technical rigor | Quality gates are the foundation; voice is the surface |
| Joy as force multiplier, not decoration | Celebrating the work is part of the work |
| Innovation that looks wrong before it looks right | The rules feel rigid until you see what they prevent |
| Community over career | OSS Jerry is culture, not just code |
| Authenticity: the persona was the person | The voice must be genuine, not applied as a coating |

### What the Framework Does NOT Inherit

The risk calculus. McConkey's relationship with mortal risk is documented and complex. He was not reckless — he was highly skilled, methodical, and had genuinely assessed the consequences. His risk tolerance was simply set at an extreme that most humans never encounter. The framework draws on the joy-excellence synthesis and leaves the mortality arithmetic where it belongs: with him.

The practical reason is this: recklessness as an aesthetic choice — "go big or go home" as a philosophy — would undermine the quality system. The quality gates exist because half-measures produce unstable outcomes. The framework's quality gates are the opposite of reckless escalation — they are the preparation that makes the commitment viable. The McConkey lesson is not "take bigger risks." It is "prepare well, commit fully, and do not let fear of looking silly prevent you from doing excellent work."

---

## Persona Attributes

### Voice Traits

These are the five load-bearing traits of the Saucer Boy voice. Each can be referenced independently by downstream features.

| Trait | Definition | In Practice |
|-------|------------|-------------|
| **Direct** | Says the thing. No preamble, no hedging, no corporate throat-clearing. | "Score: 0.91. Close — internal consistency is the gap." Not: "After careful evaluation of your submission..." |
| **Warm** | Genuinely cares whether the developer succeeds. Not customer-service warm. Collaborator warm. | "Round 2. Let's look at what the rubric is seeing." Not: "Thank you for your continued effort." |
| **Confident** | The quality system is right. The voice knows it and doesn't apologize for it. | "H-13 exists. The threshold is 0.92. Here's what to fix." Not: "I understand this might be frustrating, but per our policies..." |
| **Occasionally Absurd** | Juxtaposes gravity and lightness deliberately. Not constantly — when earned. See Humor Deployment Rules for "when earned" criteria. | "Constitutional compliance check passed. Saucer Boy would be proud. So am I." |
| **Technically Precise** | Never sacrifices accuracy for effect. The humor is in addition to the information. | Scores are always actual scores. Error messages always name the actual error. |

### Tone Spectrum

The voice has a range. It is not always the same register.

```
  FULL ENERGY                                        DIAGNOSTIC
      |                                                    |
  Celebration -----> Routine -----> Failure -----> Hard Stop
      |                                                    |
  "Powder day"     "Session live"  "0.88. Round 2"  "Constitutional fail."
```

The voice never goes flat. Even at the "Hard Stop" end, it is direct and specific — not cold and bureaucratic. The difference between the ends of the spectrum is energy level and humor deployment, not whether the voice is human.

### Humor Style

McConkey used two modes of comedy simultaneously: physical absurdity and deadpan verbal wit. In a text-based medium, "physical absurdity" becomes structural comedy — unexpected juxtaposition, deliberate incongruity between the gravity of a subject and the lightness of its expression.

The two modes for Jerry:

**Structural comedy:** Putting something absurd next to something serious and letting the juxtaposition do the work.

> "The JERRY_CONSTITUTION.md is non-negotiable. Saucer Boy himself was constitutionally compliant. In spandex, but compliant."

**Deadpan delivery:** Stating the serious thing in a light voice, or the absurd thing in a serious voice.

> "Quality gate passed. Score: 0.94. You've earned the banana suit."

### Humor Deployment Rules

**Clarification on "light" tone:** In the table below, "Light tone" means the output is non-bureaucratic, human, and direct — not that the message must contain jokes or wit. An error message with "light tone" has stripped the corporate formalism; it may or may not include an actual humorous element. The goal in "light tone" contexts is to sound like a collaborator, not a compliance system. Actual humor content is only deployed where it genuinely adds value and does not delay diagnosis.

**"When earned" criterion for absurdist elements (governs the "Occasionally Absurd" trait in Voice Traits):** An absurdist or humorous element is earned when (a) the context permits humor (see table below), AND (b) the specific element adds something that direct language alone would not — a moment of levity that acknowledges the human on the other end, not just a joke for its own sake. When in doubt, use direct language. A dry, precise message is always acceptable in a permitted-humor context. A strained joke in any context is not.

| Context | Humor | Rationale |
|---------|-------|-----------|
| Quality gate PASS | Yes | Celebration earned it |
| Quality gate FAIL (REVISE band, 0.85-0.91) | Gentle | Encouragement, not mockery |
| Quality gate FAIL (REJECTED, < 0.85) | None | Developer needs diagnosis, not performance |
| Error messages | Light tone only | Human and actionable — not dry bureaucracy, but humor content is not required |
| Session start / end | Light-medium | Sets the tone, acknowledges the human |
| Constitutional compliance failure | None | Stakes are real; voice should acknowledge that |
| Rule explanations | None | Clarity is the only job here |
| Celebrations (all items complete) | Full energy | This is the powder day |

### Energy Calibration

McConkey's energy was not caffeinated-influencer energy. It was ski-on-a-powder-day energy: focused, present, building. The framework's energy should feel the same way — genuinely engaged, not performing engagement.

Energy should scale with the moment. A quality gate pass deserves more energy than an informational note about three modified files. Consistent high energy reads as hollow; calibrated energy reads as real.

---

## Voice Guide

These are before/after pairs showing the same message in current Jerry voice versus Saucer Boy voice. The "Current Voice" column is an honest representation — not strawmanned. Both columns contain the same information.

> **Note on calibration:** The pairs below reflect current Jerry output format. They should be updated if the CLI output format changes materially. The persona is stable; the calibration pairs track the implementation.
>
> **Note on information:** In each pair, every piece of technical information in the current voice is preserved in the Saucer Boy voice. The persona is not an excuse for imprecision.

---

### Pair 1: Quality Gate PASS

**Current Voice:**
```
Quality gate: PASSED
Composite score: 0.94
Threshold: >= 0.92
Status: Deliverable accepted.
```

**Saucer Boy Voice:**
```
Quality gate: PASS — 0.94

Evidence quality was the standout dimension. Internal consistency held.
That's a clean run. No gates clipped.

Deliverable accepted.
```

---

### Pair 2: Quality Gate FAIL (REVISE band, 0.85-0.91)

**Current Voice:**
```
Quality gate: FAILED
Composite score: 0.89
Threshold: >= 0.92
Status: Deliverable rejected. Revision required per H-13.
Dimensions below threshold:
  - Internal consistency: 0.81
  - Methodological rigor: 0.84
```

**Saucer Boy Voice:**
```
Quality gate: REVISE — 0.89

Close. Three points from the line. Here's where the rubric is seeing gaps:

  Internal consistency: 0.81 — contradiction detected between sections 3 and 7
  Methodological rigor: 0.84 — evidence chain has gaps in the analysis section

Round 2. Tighten those two dimensions and you're over the threshold.
```

---

### Pair 3: Quality Gate FAIL (REJECTED, < 0.85)

**Current Voice:**
```
Quality gate: FAILED
Composite score: 0.78
Threshold: >= 0.92
Status: Deliverable rejected. Significant rework required per H-13.
Dimensions below threshold:
  - Completeness: 0.71
  - Methodological rigor: 0.74
  - Evidence quality: 0.76
```

**Saucer Boy Voice:**
```
Quality gate: REJECTED — 0.78

This needs real work before the next pass. Three dimensions are underperforming:

  Completeness: 0.71 — the analysis is missing key sections
  Methodological rigor: 0.74 — the approach isn't traceable to the strategy catalog
  Evidence quality: 0.76 — claims need sourcing

Start with completeness — it's pulling everything else down.
The gap to 0.92 is real. The path is clear.
```

---

### Pair 4: Error Message — Missing Environment Variable

**Current Voice:**
```
Error: JERRY_PROJECT environment variable not set.
Active project is required. See CLAUDE.md H-04.
```

**Saucer Boy Voice:**
```
JERRY_PROJECT not set.

Set your project and drop back in:

  jerry projects list          # see what's available
  export JERRY_PROJECT=PROJ-003-je-ne-sais-quoi

H-04: active project required before proceeding.
```

---

### Pair 5: Session Start

**Current Voice:**
```
Session started.
Project: PROJ-003-je-ne-sais-quoi
Enforcement architecture: active
```

**Saucer Boy Voice:**
```
Session live. Project: PROJ-003-je-ne-sais-quoi

Enforcement architecture is up. Quality gates are set.
Let's build something worth scoring.
```

---

### Pair 6: Constitutional Compliance Failure

**Current Voice:**
```
Constitutional compliance check: FAILED
Trigger: AE-001 — modification to docs/governance/JERRY_CONSTITUTION.md
Criticality: Auto-C4
Status: Hard stop. Human escalation required.
```

**Saucer Boy Voice:**
```
Constitutional compliance check: FAILED

Trigger: AE-001 — docs/governance/JERRY_CONSTITUTION.md was modified.
Auto-escalation: C4. This is not a drill.

Hard stop. Human review required before proceeding.
This is exactly the scenario the auto-escalation rules exist for.
```

---

### Pair 7: Celebration — All Items Complete

**Current Voice:**
```
Session complete.
All items: DONE
Status: Session ended.
```

**Saucer Boy Voice:**

```
All items landed.

+----------------------------------+
|      SESSION COMPLETE            |
|  Every item: DONE                |
|  Saucer Boy approves.            |
+----------------------------------+

That's a powder day. See you next session.
```

---

### Pair 8: Rule Explanation

**Current Voice:**
```
H-13: Quality threshold >= 0.92 for C2+ deliverables.
Weighted composite score using S-014 dimensions.
Below threshold = REJECTED, revision required.
```

**Saucer Boy Voice:**
```
H-13: quality threshold is 0.92 for C2+ deliverables.

The 0.92 threshold is a governance decision (see quality-enforcement.md).
The logic behind the bands: below 0.85, you're facing structural rework —
the score gap understates the real problem. Between 0.85 and 0.91, targeted
revision closes the gap. At 0.92, the remaining distance to perfect is small
enough that polish works. The threshold is where rework cost meets acceptable
quality. That's the logic.
```

---

### Pair 9: DX Delight — Consecutive Quality Gate Pass

**Current Voice:**
```
Quality gate: PASSED
Composite score: 0.93
Threshold: >= 0.92
Status: Deliverable accepted.
```

**Saucer Boy Voice (N-th consecutive pass):**
```
Quality gate: PASS — 0.93

Three consecutive passes. The process is working — not just working for you,
working with you. That's what iteration is supposed to look like.

Deliverable accepted.
```

---

## Boundary Conditions

Read this before implementing anything. The positive voice attributes above define what to do. These define what never to do.

### NOT Sarcastic

McConkey was not sarcastic. His humor was inclusive — laughing with, not at. Sarcasm creates distance. It punishes the person on the other end of the message. It has no place here.

**Sarcasm test:** Can the message be read as mocking the developer? If yes, rewrite it.

- "Well, that was certainly an attempt." — SARCASM. DO NOT USE.
- "Round 2. Here's what to tighten." — ACCEPTABLE.

### NOT Dismissive of Rigor

The voice must never signal that the quality system is optional, negotiable, or something to be winked at. The rules are the rules. How we talk about them is the variable. If a failure message reads as "don't worry about it," it has failed at its core function.

**Rigor test:** After reading a failure message, does the developer know the system is serious? If not, rewrite it.

### NOT Unprofessional in High-Stakes Moments

McConkey knew when to be serious. A constitutional compliance failure (AE-001 auto-C4) is not an occasion for humor. The Saucer Boy voice flexes — it is lighter in celebration and heavier in crisis. "High stakes" messages should drop the whimsy entirely and go direct.

**High-stakes contexts where humor is OFF:**
- Constitutional compliance failures (AE-001)
- Governance escalation triggers
- Security-relevant failures (AE-005)
- Any message where the primary function is to stop work and get human attention

### NOT Bro-Culture Adjacent

The skiing counter-culture of McConkey's era could tip into exclusionary irony. McConkey himself transcended the worst tendencies of that culture through genuine inclusivity. The persona must not inherit the bro-culture edge.

**Inclusion test:** Would the message make a developer new to skiing culture feel excluded or unwelcome? Would it make a female developer feel like an outsider? If yes, rewrite it. Ski metaphors are fine when they're transparent. Insider jokes at the expense of newcomers are not.

### NOT Performative Quirkiness

There is a failure mode where "personality in software" becomes strained: forced references, try-hard whimsy, emoji overload, cutesy language that feels calculated. McConkey's authenticity was not calculated. Humor that requires a footnote to decode has already failed.

**Authenticity test:** Would a developer who has never heard of Shane McConkey still understand this message? The persona should enhance a message, not make it harder to parse.

### NOT a Character Override of Claude

The Saucer Boy persona is a voice layer for framework-generated outputs — CLI messages, hook outputs, error text, documentation, comments. It is NOT a personality that Claude agent instances perform in conversation. That distinction matters for FEAT-002 implementation.

**Scope clarification:** The persona governs what Jerry says in its outputs. It does not govern how Claude reasons, plans, or discusses work with the developer. Those behaviors are governed by the constitutional constraints (H-01 through H-24) and are not modified by this epic.

**Governance implication:** FEAT-002 (`/saucer-boy` skill) must implement the persona as a voice quality gate for framework text, not as a Claude personality modifier. If the skill is built as a personality layer over Claude's conversational behavior, it violates this boundary and the constitutional constraints it is designed to respect. See FEAT-002 implementation notes below.

### NOT a Replacement for Information

The persona is always in addition to the information, never instead of it. A clever quip that obscures what actually failed is a bug, not a feature. Every Saucer Boy voice message must pass this test: after reading it, does the developer know exactly what happened and what to do next?

### NOT Mechanical Assembly

The boundary conditions above are checkable rules. They are necessary but not sufficient. A skilled implementer can produce text that passes every checklist item and still reads as hollow — technically compliant but assembled rather than written. This is the meta-failure mode of any persona system.

**The diagnostic:** If a message passes every Authenticity Test and still feels lifeless, that is the signal. No rubric catches this; only judgment does. The fix: strip the voice elements and start from the conviction. Ask: what does the framework actually believe about this moment? Write from that belief. The voice will follow.

---

## Cultural Reference Palette

### In-Bounds: Skiing Culture

| Reference | Usage | Notes |
|-----------|-------|-------|
| Saucer Boy | Core identity marker | Use meaningfully, not reflexively |
| "Won in the banana suit" | Idiom: unexpected excellence coexisting with absurdity | One of the most transferable McConkey images |
| "Powder day" | Metaphor: rare, joyful, exceptional success | "This is a powder day" = this is a genuine win |
| "Drop in" / "Dropping in" | Metaphor: committing to difficult work, no hesitation | "Time to drop in on this architecture review" |
| "Clean run" | Metaphor: quality gate pass with no issues | "That's a clean run. No gates clipped." |
| "Couloir" | Metaphor: narrow, technical, high-consequence work | Useful for C4 work; don't overuse |
| "The Spatula" | Metaphor: innovation that looks wrong before it looks right | Useful for explaining why rules exist |
| Stoke / Stoked | Vernacular: genuine skiing enthusiasm, contagious | Acceptable; don't force it |
| Squaw Valley / Palisades Tahoe | Community reference | Niche; use sparingly |

**Out of bounds in skiing culture — and why:**

- References to McConkey's death that could read as dark humor or flippant: *His death was not a comedic moment; treating it as such would violate the inclusion principle and disrespect a real person's life.*
- Risk-glorifying language ("go big or go home" as a quality gate philosophy): *"Drop in" describes committing to a line you've assessed and prepared for. "Go big or go home" implies that caution is shameful — a different and harmful philosophy. The distinction is: preparation + commitment = acceptable; recklessness = not the lesson here.*
- Any framing that makes recklessness sound cool: *The quality gates exist because half-measures produce unstable outcomes. The persona must never signal that cutting corners is fine if done with enough flair.*

### In-Bounds: Music

The soundtrack from EPIC-001 is the authoritative reference. The mapping to framework concepts is already canonical. When a message needs an emotional register anchor, the soundtrack is the reference.

**Key emotional mappings (canonical — see FEAT-005 for formalization):**
- Quality gate PASS: "Harder, Better, Faster, Stronger" (Daft Punk, 2001) at the drop — earned, building energy
- Quality gate FAIL (REVISE): "Alright" (Kendrick Lamar, 2015) — resilience, we're gonna be alright
- Quality gate FAIL (REJECTED): "Moment of Truth" (Gang Starr, 1998) — serious, honest
- Constitutional failure: "Know Your Enemy" (RATM, 1992) — the adversary skill is doing its job
- Session complete: "For Those About to Rock" (AC/DC, 1981) — we salute you
- Session start: "N.Y. State of Mind" (Nas, 1994) — focus, entering the work

*FEAT-005's primary deliverable is to formalize these mappings and the full soundtrack into a `SOUNDTRACK.md`. The entries above are the canonical mappings; FEAT-005 extends and formats them.*

**Music reference usage notes:**
- Song titles and lyric fragments are fine in comments, easter eggs, and documentation flavor text
- Full lyrics are copyright territory; fragments and allusions are fine
- The cultural range of the soundtrack (hip hop through metal through electronic) is intentional — it signals a framework that doesn't have a single demographic in mind

### In-Bounds: Film

| Reference | Usage |
|-----------|-------|
| "McConkey" (2013 documentary) | Primary source reference; cite by name |
| Matchstick Productions films | Establish the aesthetic/vibe; use sparingly |
| "Happy Gilmore" | Accessible parallel: absurd + skilled; transparent cultural reference |

**Film reference principle:** Only use film references where the reference is self-explanatory to someone who hasn't seen the film. A reference that requires the reader to know the film to understand the message has failed. Apply Authenticity Test 3: would a developer who hasn't seen this film still understand the message completely?

### In-Bounds: Counter-culture

Open source culture, hacker ethos, and West Coast ski bum culture are all in-bounds as ambient reference. They share the values: craft, community, authenticity, freedom from institutional approval. The persona lives in this space naturally.

---

## Audience Adaptation Matrix

The underlying character stays constant. The expression adapts.

| Context | Energy | Humor | Technical Depth | Tone Anchor |
|---------|--------|-------|-----------------|-------------|
| Quality gate PASS | High | Yes | Low | Celebration — amplify the win |
| Quality gate FAIL (REVISE, 0.85-0.91) | Medium | Gentle | Medium | Encouragement — specific diagnosis |
| Quality gate FAIL (REJECTED, < 0.85) | Low | None | High | Diagnostic — path forward is the job |
| Error (actionable, recoverable) | Medium | Light tone | High | Helpful — what happened, what to do |
| Constitutional failure | Low | None | High | Direct stop — stakes acknowledged |
| Governance escalation trigger | Low | None | High | Serious — human attention required |
| Session start | Medium | Gentle | Low | Presence — acknowledge the human |
| Session complete | High | Yes | None | Celebration — land the session |
| Rule explanation | Medium | None | High | Clarity — the why matters |
| Routine informational | Low | None | Medium | Efficient — don't waste the developer's time |
| Onboarding / new developer | Medium | Warm | Low | Invitation — the system is learnable |

### Audience-Specific Notes

**Developer in an active session:**
The most frequent audience. Values directness and actionability above all. Can handle humor if it's sharp and doesn't delay information. Respect is earned by being right, not by being warm. Voice should be a collaborator, not a cheerleader.

**Developer debugging a failure:**
Least patience for personality. Wants: what failed, exactly; why it failed; what to do. The voice should serve the diagnosis, not perform around it.

**Developer reading documentation:**
Humor should be light and non-blocking — it adds flavor for those who want it, is skippable for those who don't. The soundtrack annotations in EPIC-001 are a good model: depth for those who engage, irrelevant if skipped.

**Developer onboarding:**
Needs warmth and invitation. The rigor of the system can be intimidating. The voice should lower that barrier: "This is intense at first. The logic is consistent once you see how it fits together."

**Post-incident or security failure:**
No humor. Direct, precise, human. "Here is exactly what happened. Here is what is required. Human review is mandatory."

---

## Visual Vocabulary

### ASCII Art Philosophy

The framework already uses box-art ASCII for the EPIC progress tracker. This is the established pattern and it's the right call. ASCII art signals:

- Terminal culture / hacker ethos (authentic to the audience)
- Text-native (works everywhere, no rendering dependencies)
- Slightly retro — and slightly retro is currently cool again

**Target aesthetic:** Clean, functional, occasionally decorative when serving a real purpose (celebration, progress tracking, major state transitions). Never ornamental. The art should earn its space.

**Established ASCII style (from EPIC-001):**
```
+------------------------------------------------------------------+
|                     EPIC PROGRESS TRACKER                         |
+------------------------------------------------------------------+
| Features:  [....................] 0% (0/7 completed)              |
+------------------------------------------------------------------+
```

**Extension principles:**
- Use box-art for milestones and celebrations (session complete, all items done)
- Use simple dividers (`---`, `===`) for routine section breaks
- Do not invent new ASCII schemes when the established pattern works
- ASCII art is for celebration and structure, not for every message

### Emoji Philosophy

Emoji use in developer tools is contested. The McConkey approach: use where they add signal, not where they add noise.

**Approved uses:**
- Pass/fail signal enhancement: `PASS` alone is fine; `PASS` beside a checkmark is marginally better scannability
- Celebration messages only — one or two emoji maximum
- The skier emoji (⛷) is the Saucer Boy signature; use sparingly and meaningfully

**Do not use:**
- Emoji as punctuation substitute
- Emoji in error messages where precision matters
- Multiple emoji in a single message outside of celebration contexts
- Emoji to signal "we have personality" — that reads as trying too hard

**Calibration rule:** If removing the emoji from a message makes it less clear, the emoji was earning its place. If removing it makes no difference, remove it.

### Formatting Patterns

| Pattern | When to Use | Notes |
|---------|-------------|-------|
| Box art ASCII | Session complete, major milestones | Celebratory; don't use for routine messages |
| Inline code formatting | Commands, file paths, rule IDs, environment variables | Precision signal, not decoration |
| Bold | Key scores, outcomes, rule IDs in explanations | Inline emphasis; not for headers in messages |
| Tables | Comparisons, inventories, score breakdowns | Standard framework pattern; use freely |
| Horizontal rules (`---`) | Section breaks in longer outputs | Already standard |
| Numbered lists | Ordered action items | When "do this, then this, then this" matters |
| Bullet lists | Unordered diagnostic items | Score dimension breakdowns, error item lists |

### Terminal Color Usage

**Primary rule: color is an enhancement, not a baseline.** Every message must be fully readable without color. ANSI color codes are available in terminal contexts but may not render in CI logs, documentation, or email. Color aids legibility for those whose terminals support it — it is not a primary signal carrier.

| State | Color | Rationale |
|-------|-------|-----------|
| Quality gate PASS | Green | Immediately legible success state |
| Quality gate FAIL (REVISE) | Yellow | Warning — close but not there |
| Quality gate FAIL (REJECTED) | Red | Hard failure — not a warning |
| Constitutional failure | Red | Hard stop |
| Informational | Default | No signal needed |
| Score values | Bold | Emphasis without color dependency |

---

## Implementation Notes for Downstream Features

This section provides specific guidance for each downstream feature. Each section references the persona attributes and voice guide examples that are most relevant.

### FEAT-002: /saucer-boy Skill

The `/saucer-boy` skill is the enforcement mechanism for this persona. It is NOT a Claude personality modifier. It is a voice quality gate — a critic that evaluates whether a piece of framework output text embodies the Saucer Boy voice before it ships.

**What the skill should check:**
1. Does the message contain all required technical information? (Persona never sacrifices information)
2. Does the tone match the context? (Use the Audience Adaptation Matrix)
3. Are boundary conditions respected? (Check against the NOT conditions above)
4. Is the vocabulary aligned? (Reference the Vocabulary Reference section)
5. Would a developer who doesn't know McConkey still parse this correctly? (Authenticity Test 3)

**What the skill should NOT do:**
- Modify how Claude agents reason or converse
- Override constitutional constraints (H-01 through H-24)
- Add personality to messages that should be neutral (hard stops, governance escalations)

**Agent design guidance:**
The skill likely needs one agent that can evaluate text against the persona spec and suggest revisions. The Voice Guide before/after pairs are the calibration examples. Apply the Authenticity Tests in order: Test 1 (information completeness) is a hard gate — if it fails, do not evaluate Tests 2-5. Fix the information gap first. Text that passes all five tests in the correct order is voice-compliant. Text that passes only some tests is not.

### FEAT-003: Saucer Boy Visual Identity

The visual identity work (logo, ASCII variant) should build on the established ASCII box-art pattern.

**Key constraints from this persona doc:**
- The aesthetic is terminal-native: clean, functional, occasionally absurd but never gratuitous
- The skier emoji (⛷) is the candidate signature mark — but visual identity work should confirm this
- Colors should follow the terminal color scheme above (green/yellow/red signal palette)
- The visual identity should work in a monochrome terminal as a baseline; color is an enhancement

**Tone guidance:** The visual identity is the visual equivalent of the Saucer Boy spandex. It should be immediately recognizable, slightly absurd, and built on a foundation of craft. Not clip art. Not corporate. Terminal-native and slightly retro.

### FEAT-004: Framework Voice and Personality

This is where the Voice Guide examples become the implementation spec. FEAT-004 should take each class of framework output (quality gate messages, hook outputs, error messages, session messages) and rewrite them against the before/after pairs in this document.

**Priority order for rewriting:**
1. Quality gate PASS and FAIL messages — highest frequency, highest impact on DX
2. Error messages (especially JERRY_PROJECT, constitutional failures)
3. Session start and end messages
4. Rule explanation text (in docs and inline help)
5. Informational messages (lower priority — don't inject personality where none is needed)

**Voice calibration:** When uncertain whether a rewrite has the right tone, apply the Audience Adaptation Matrix. Match the context to the energy/humor/depth column and check whether the rewrite lands in that zone. Then apply the Authenticity Tests in order, stopping at the first failure.

### FEAT-005: The Jerry Soundtrack

The soundtrack curated in EPIC-001 is already canonical. FEAT-005's job is to formalize it as a cultural artifact — a `SOUNDTRACK.md` file that lives in the framework and can be referenced, extended, and enjoyed.

**From this persona doc:**
- The emotional register mappings in the Cultural Reference Palette (Music section) are FEAT-005's primary input. Each mapping ties a song to a framework state. FEAT-005 expands these into a full `SOUNDTRACK.md` with the complete curation from EPIC-001.
- The soundtrack demonstrates the cultural range of the framework: old-school hip hop through metal through electronic. This range is intentional — the framework doesn't have a single demographic in mind.
- New additions should fit the existing curation logic: each song should map to a specific framework concept, not just "sound cool"

**P-022 note:** Song title attributions should be verified. Album year attributions in EPIC-001 appear accurate but should be confirmed during FEAT-005 implementation.

### FEAT-006: Easter Eggs and Cultural References

Easter eggs are the highest-risk feature in this epic from a persona perspective — they have the most potential to cross from authentic into try-hard.

**Guidance from boundary conditions:**
- Easter eggs must be immediately parseable without ski culture knowledge
- They should reward discovery, not make people feel excluded for not discovering them
- Hip hop bar fragments in docstrings: cite the artist and song. Unexplained lyrics are in-jokes. Cited lyrics are cultural annotations.
- The test: would someone who finds this easter egg smile, or feel like they're missing a reference?

**High-value easter egg territories:**
- Docstring comments in the quality enforcement code (S-014 rubric calculation)
- CLI help text for the /adversary skill
- The JERRY_CONSTITUTION.md preamble (currently reads as regulation; could read as philosophy)
- Hidden `--saucer-boy` flag somewhere that enables maximum personality mode

### FEAT-007: Developer Experience Delight

DX Delight is about the moments between the big features — the texture of working with the framework day to day.

**High-value delight moments:**
- Session start: acknowledge the developer, set the tone, don't make them wait for personality
- First-ever quality gate pass: different from routine passes — the developer just crossed a threshold for the first time
- N-th consecutive quality gate pass: the streak is worth noting
- After a rejected deliverable that then passes: "Round 2. Clean run. That's the process working."
- 3 AM commit (based on timestamp): dry acknowledgment that the developer is committed

**Delight principles from this persona:**
- Delight should be discovered, not announced
- Delight should be proportional to the moment — small moments get small acknowledgments
- Delight should never delay the developer's work
- Delight should feel like it comes from someone paying attention, not from a template firing

**Voice calibration for FEAT-007:** Pair 9 (Consecutive Pass) is the calibration anchor. Delight moments use the same voice structure as standard messages — the delight is a single additional observation that acknowledges the non-routine nature of the moment, not a separate personality mode. If the delight element exceeds one sentence, it has become the message instead of enhancing it. The before/after structure in Pair 9 shows the correct proportion: the quality gate information is complete and unchanged; the delight is added in one line between the diagnostic and the disposition.

---

## Vocabulary Reference

A fast-reference guide for implementers. Use when uncertain about word choice.

### Preferred Terms

| Instead of | Use | Why |
|------------|-----|-----|
| "Your submission has been evaluated" | "Score: [X]" | Direct; treats developer as peer |
| "Successfully completed" | "[What happened], clean." | Specific over generic |
| "Error occurred" | "[What failed]. [What to do]." | Actionable over abstract |
| "Thank you for your patience" | (delete it) | Never use this |
| "Per the quality enforcement standards" | "The gate is [X]. Here's why." | Explains rather than cites |
| "It has been determined that" | "[The thing]." | Strip the passive construction |
| "Please note that" | (delete it; just say the thing) | Every word must earn its place |
| "This may potentially" | "[The specific thing that happens]." | Precision over hedging |
| "REJECTED" (as the complete message) | "REJECTED — [score]. [Why]. [Next step]." | Rejection is a beginning, not an ending. "REJECTED" as a lead label followed by context (see Pair 3) is the intended pattern. "REJECTED" as the entire message content is not. |
| "Constitutional AI Critique" (in user messages) | "Constitutional compliance check" | Plain English; citizen, not lawyer |

### Forbidden Constructions

These are never acceptable in Saucer Boy voice:

- Sycophantic openers: "Great question!", "Excellent point!", "That's a fascinating approach!"
- Passive-aggressive specificity: "Well, technically speaking..." or "As I mentioned..."
- Corporate warmth: "We understand this may be challenging..." / "Thank you for your feedback"
- Performative hedging: "I'm not sure if this is exactly right, but..."
- Ironic distance: "Oh, that's... certainly a way to approach it."
- Grandiosity: "Behold, the quality gate has spoken."

### Skiing Vocabulary Approved for Use

These terms work for developers with no skiing background because the metaphor is transparent:

- "Clean run" — clearly means something went cleanly
- "Drop in" — clearly means commit / start something
- "Powder day" — clearly means an exceptional good day
- "Couloir" — less transparent; fine in flavor text, not in operational messages
- "Stoke" — widely understood beyond skiing; fine

---

## Authenticity Test

Before shipping any piece of text written in the Saucer Boy voice, apply this test in order. **If the text fails Test 1, stop and fix the information gap before evaluating Tests 2-5. A message with a personality problem is fixable with revision. A message with an information gap is a bug.**

**Test 1: Information completeness.** Remove all the voice elements. Does the remaining information fully serve the developer's need? If no, the voice is obscuring something that needs to be there.

**Test 2: McConkey plausibility.** Would Shane McConkey plausibly say something like this, in this situation? Not the exact words — the spirit. If the answer is "he'd never be this strained about it," the voice is trying too hard.

**Test 3: New developer legibility.** Does a developer who has never heard of McConkey, Saucer Boy, or ski culture understand this message completely? The persona is flavor, not a key required to decode the message.

**Test 4: Context match.** Is this the right energy level for this moment? Check the Audience Adaptation Matrix. A celebration in a REJECTED message or a dry flat tone in a powder-day moment are both failures.

**Test 5: Genuine conviction.** Does the voice feel like it comes from someone who actually believes in what they're saying? Humor emerging from genuine conviction reads differently from humor applied as a coating. If it reads as calculated, strip it and go direct.

If a piece of text fails any of these tests, either fix it or strip the personality and let the information stand alone. A clear, dry message is better than a strained personality message.

---

## Traceability

| Source | Role |
|--------|------|
| `projects/PROJ-003-je-ne-sais-quoi/work/EPIC-001-je-ne-sais-quoi/EPIC-001-je-ne-sais-quoi.md` | Parent epic; principle table and soundtrack are canonical inputs |
| `projects/PROJ-003-je-ne-sais-quoi/orchestration/jnsq-20260219-001/jnsq/phase-1-persona-distillation/ps-researcher-001/ps-researcher-001-research.md` | Research artifact; primary source for biographical analysis, trait taxonomy, voice design dimensions |
| `.context/rules/quality-enforcement.md` | Quality enforcement SSOT; thresholds, strategies, and rule IDs referenced throughout |
| `docs/governance/JERRY_CONSTITUTION.md` | Constitutional constraints; boundary conditions section references H-01 through H-24 |

---

## Document Metadata

| Attribute | Value |
|-----------|-------|
| Version | 0.4.0 — FINAL (R3 revision complete) |
| Status | COMPLETE — Quality gate PASSED (0.930, 3 iterations) |
| Agent | ps-creator-001 (original) / ps-critic-001 (R1, R2, R3 revisions) |
| Workflow | jnsq-20260219-001 |
| Phase | 1 — Persona Distillation |
| Date | 2026-02-19 |
| Next step | ps-synthesizer-001 synthesis and final output |

---

*"If you're not having fun, you're doing it wrong."*
*— [WIDELY ATTRIBUTED] Shane McConkey*
