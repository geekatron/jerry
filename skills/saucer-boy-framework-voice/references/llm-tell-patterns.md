# LLM-Tell Detection Patterns

> Specific LLM writing markers that cause text to read as machine-generated. Diagnostic companion to Boundary #8 (NOT Mechanical Assembly). Load when Boundary #8 is flagged, when text shows LLM-generated patterns, or when rewriting text suspected of having tells.

*Source: ART-001 C4 adversarial pipeline findings (4 iterations, 40 critiques across 10 strategies)*

## Document Sections

| Section | Purpose |
|---------|---------|
| [Syntactic Tells](#syntactic-tells) | Sentence-level mechanical patterns |
| [Rhetorical Tells](#rhetorical-tells) | Filler phrases and formulaic transitions |
| [Structural Tells](#structural-tells) | Document-level assembly patterns |
| [Precision Tells](#precision-tells) | Ungrounded claims and false precision |
| [Detection Quick Reference](#detection-quick-reference) | Summary table for scanning |

---

## Syntactic Tells

### Em-Dash Sentence Connectors

**Pattern:** Parenthetical clauses inserted with em-dashes as sentence connectors, especially stacked or nested.

**Detection heuristic:** Two or more em-dash pairs in a single paragraph. One em-dash pair is normal punctuation; multiple pairs per paragraph signal LLM assembly.

| Before (LLM tell) | After (corrected) |
|---|---|
| "The model — which is trained on billions of documents — produces outputs that — while often coherent — lack the specificity of human writing." | "The model produces coherent outputs but lacks the specificity of human writing. Training on billions of documents does not fix that." |

**Correction:** Break the sentence. Move parenthetical content into its own sentence or delete it if it adds nothing.

---

### Staccato Emphasis Pairs

**Pattern:** Two consecutive short sentences used as rhetorical emphasis, often with parallel structure.

**Detection heuristic:** Back-to-back sentences under 8 words each, where the second restates or amplifies the first.

| Before (LLM tell) | After (corrected) |
|---|---|
| "Every time. Across every model family." | "This happens across every model family we tested." |
| "That matters. It matters a lot." | "That matters — here's why." |

**Correction:** Merge into one sentence that carries the emphasis through specificity, not repetition.

---

### Corrective Insertion

**Pattern:** "That's not X. It's Y." or "It's not X. It's Y." — a negation-then-correction structure used as a rhetorical move.

**Detection heuristic:** Sentence starting with "That's not" or "It's not" immediately followed by a sentence starting with "It's" that provides the correction.

| Before (LLM tell) | After (corrected) |
|---|---|
| "It's not garbage in, garbage out. It's garbage in, polished garbage out." | "The real failure mode is polished garbage — clean outputs built on flawed inputs." |
| "That's not a bug. It's a design choice." | "The behavior is intentional." |

**Correction:** State the actual claim directly. The negation-correction structure is a writing tic, not an argument.

---

## Rhetorical Tells

### Hedging Phrases

**Pattern:** Filler phrases that hedge, signal importance, or manage reader expectations without adding information.

**Detection heuristic:** Sentence starts with any of these phrases (or contains them as clause openers):

- "It's worth noting"
- "Importantly"
- "Interestingly"
- "It should be noted that"
- "Perhaps more importantly"
- "What's particularly interesting is"

| Before (LLM tell) | After (corrected) |
|---|---|
| "It's worth noting that structured prompts outperform unstructured ones by 23%." | "Structured prompts outperform unstructured ones by 23%." |
| "Importantly, the quality gate threshold exists for a reason." | "The quality gate threshold exists for a reason." |

**Correction:** Delete the hedging phrase. The sentence is stronger without it. If the information is worth noting, note it. If it's important, it will be important without the label.

---

### Formulaic Transitions

**Pattern:** Transition phrases that signal a shift but use a canned formula instead of a natural pivot.

**Detection heuristic:** Any of these phrases used as a standalone sentence or clause opener:

- "Here's the thing:"
- "Here's where it gets interesting:"
- "One more thing that bites hard:"
- "But here's the catch:"
- "Let's break this down:"
- "So what does this mean?"

| Before (LLM tell) | After (corrected) |
|---|---|
| "Here's the thing: most developers don't read error messages." | "Most developers don't read error messages." |
| "Let's break this down:" | [Delete. Start breaking it down.] |

**Correction:** Delete the transition and start with the content. The structure of the text should signal the shift, not a formulaic phrase.

---

## Structural Tells

### Parallel Structure Formulae

**Pattern:** Three or more consecutive sentences with identical syntactic openings, used to create a rhythm that reads as generated.

**Detection heuristic:** Three consecutive sentences starting with the same word or phrase pattern (e.g., "They X. They Y. They Z." or "This means X. This means Y. This means Z.").

| Before (LLM tell) | After (corrected) |
|---|---|
| "Structure makes prompts readable. Structure makes outputs predictable. Structure makes debugging possible." | "Structure does three things: it makes prompts readable, outputs predictable, and debugging possible." |

**Correction:** Collapse into a single sentence with a list, or vary the openings so the rhythm sounds written rather than templated.

---

### Voice Register Drops

**Pattern:** Text shifts from conversational register in the introduction to academic register in the middle (passive voice, complex clauses, citation-dense), then back to conversational for the conclusion.

**Detection heuristic:** Compare sentence length and passive voice density across sections. If the middle third has 2x the average sentence length and passive constructions of the first third, the register dropped.

| Before (LLM tell) | After (corrected) |
|---|---|
| Intro: "Prompting is a skill you can learn." Middle: "The efficacy of structured prompting methodologies has been demonstrated across multiple experimental paradigms." Close: "So yeah, structure works." | Maintain one register throughout. If the intro is conversational, the middle should be too: "Multiple experiments confirm this: structured prompting works better than freeform, every time." |

**Correction:** Pick one register and hold it. If the piece is conversational, keep it conversational through the technical sections. The information can be precise without being academic.

---

### Academic Citation Sentences

**Pattern:** Citations formatted as academic references rather than integrated conversationally.

**Detection heuristic:** Sentences following the pattern "[Author] et al. ([year]) demonstrated/showed/found that..."

| Before (LLM tell) | After (corrected) |
|---|---|
| "Wei et al. (2022) demonstrated that chain-of-thought prompting improves reasoning accuracy." | "Chain-of-thought prompting improves reasoning accuracy — Wei's team showed this in 2022, and it's held up since." |

**Correction:** Integrate the citation into the conversational flow. The finding leads; the attribution follows naturally.

---

## Precision Tells

### Ungrounded Quantitative Claims

**Pattern:** Specific-sounding numbers or proportions stated without a source, creating false authority.

**Detection heuristic:** Percentages, ratios, or frequency claims ("most," "the majority," "80% of") without a citation or explicit source.

| Before (LLM tell) | After (corrected) |
|---|---|
| "80% of prompt failures come from ambiguous instructions." | "Most prompt failures we've seen trace back to ambiguous instructions." (Or cite the source if one exists.) |

**Correction:** Either cite the source or soften to match what you actually know. "Most" is honest when you don't have a number. "80%" without a source is fabrication.

---

### False Precision in Qualitative Statements

**Pattern:** Quantitative framing applied to claims that are inherently qualitative.

**Detection heuristic:** Phrases like "significantly improves," "dramatically reduces," "orders of magnitude better" applied to outcomes that were not measured.

| Before (LLM tell) | After (corrected) |
|---|---|
| "Structured prompting dramatically reduces error rates." | "Structured prompting reduces error rates." (Or cite the measurement if one exists.) |

**Correction:** Drop the intensifier. If the effect was measured, cite the measurement. If it wasn't, the plain claim is honest; the intensifier is not.

---

## Detection Quick Reference

Scan text against this table. Any match warrants closer inspection.

| Tell | Pattern | Severity | Fix |
|------|---------|----------|-----|
| Em-dash stacking | 2+ em-dash pairs per paragraph | Medium | Break sentences apart |
| Staccato emphasis | Two consecutive sentences < 8 words | Low | Merge; add specificity |
| Corrective insertion | "It's not X. It's Y." | Medium | State the claim directly |
| Hedging phrases | "It's worth noting," "Importantly" | High | Delete the phrase |
| Formulaic transitions | "Here's the thing:" | High | Delete; start with content |
| Parallel structure | 3+ consecutive same-opening sentences | Medium | Collapse or vary openings |
| Voice register drop | Conversational → academic → conversational | High | Hold one register |
| Academic citations | "[Author] et al. (year) demonstrated..." | Medium | Integrate conversationally |
| Ungrounded claims | Percentages without sources | High | Cite or soften |
| False precision | "Dramatically," "significantly" (unmeasured) | Medium | Drop the intensifier |

---

*Source: ART-001 C4 adversarial pipeline — 4 iterations, 40 critiques across 10 adversary strategies*
*Canonical: Boundary #8 (NOT Mechanical Assembly) diagnostic companion*
