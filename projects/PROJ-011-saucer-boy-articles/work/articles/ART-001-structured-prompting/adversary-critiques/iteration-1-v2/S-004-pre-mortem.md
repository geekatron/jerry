# Pre-Mortem Report: "Why Structured Prompting Works" (Draft 5 -- LLM-Tell-Clean)

**Strategy:** S-004 Pre-Mortem Analysis
**Deliverable:** `drafts/draft-5-llm-tell-clean.md`
**Criticality:** C3 (public-facing article on an mkdocs site; brand credibility at stake)
**Date:** 2026-02-23
**Reviewer:** adv-executor (S-004)
**H-16 Compliance:** S-003 Steelman applied in iteration 1 (2026-02-23, confirmed -- see `adversary-critiques/iteration-1/S-003-steelman.md`)
**Prior Iterations:** This is a re-run of S-004 against draft 5 (post-LLM-tell cleaning). Previous S-004 ran against draft 1. Previous quality gate: 0.938 PASS (iteration 3, S-014).

**Failure Scenario:** It is August 23, 2026 -- six months after publication. The article was posted on the Saucer Boy mkdocs site. It received modest traffic. Then three things happened: (1) a technical reader with prompt engineering expertise wrote a public takedown calling out specific inaccuracies and noting the article "reads like an LLM wrote it," (2) the article's McConkey framing confused readers who found it via search -- they expected a skiing article and bounced immediately, and (3) practitioners who read the whole thing found the advice too abstract to act on for their specific tools, never changed their behavior, and the article had zero measurable impact on prompting practice. The article harmed the Saucer Boy brand by associating it with generic AI advice dressed in a persona.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall failure assessment and recommendation |
| [Failure Causes](#failure-causes) | PM-001 through PM-009 with full details |
| [Findings Table](#findings-table) | Prioritized summary of all failure causes |
| [Recommendations](#recommendations) | P0/P1/P2 mitigation plan |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 dimensions |
| [LLM-Tell Assessment](#llm-tell-assessment) | Dedicated LLM-tell detection analysis |
| [Voice Authenticity Assessment](#voice-authenticity-assessment) | McConkey persona fidelity analysis |

---

## Summary

Nine failure causes identified across Technical, Assumption, Process, and External categories. Draft 5 is a substantial improvement over draft 1 -- it addressed the most critical gaps from the first pre-mortem (checklist added, intermediate Level 2 example added, jargon translated, call-to-action added, McConkey introduced for non-skiers). However, the LLM-tell cleaning pass and the article's transition from conversational response to published mkdocs article introduces a new class of failure modes not present in iteration 1: publication-context failures including SEO/discoverability, residual LLM-tell patterns, voice consistency under the structural constraints of an article format, and expert-audience credibility. The article is good. The question is whether it is good enough to publish under a brand name without exposing that brand to reputational risk.

**Recommendation:** ACCEPT with targeted P0/P1 mitigations.

---

## Failure Causes

### PM-001-20260223-v2: Residual LLM-Tell Patterns Detectable by Trained Readers [MAJOR]

**Failure Cause:** A reader familiar with LLM output patterns reads the article and notices structural tells that survived the cleaning pass. Specific instances:

1. **Lines 17-18:** "The structure will be clean. The headings will be professional. The language will be authoritative." -- Three consecutive short declarative sentences with parallel structure is a characteristic LLM rhetorical pattern. Humans writing informally rarely produce three-beat anaphoric sequences outside of intentional rhetorical set-pieces.

2. **Line 19:** "That's not a coin flip. It's systematic, and it's predictable." -- The "That's not X. It's Y" construction is an extremely common LLM rhetorical move. It appears in virtually every LLM-generated explainer. The construction itself is not wrong, but its frequency in LLM output means trained readers flag it reflexively.

3. **Lines 64-65:** "Instructions are specific rather than vague. This is a well-documented finding across prompt engineering research, from chain-of-thought prompting to structured role-task-format patterns." -- The parenthetical listing of research areas after a claim, using the "from X to Y" construction, is a classic LLM-tell. It reads like the model is demonstrating breadth rather than a human citing what they actually read.

4. **Line 69:** "The structure is the point, not the format." -- Epigrammatic sentence closers that invert two related concepts are a signature LLM rhetorical flourish.

**Category:** Technical (LLM-tell detection)
**Likelihood:** HIGH -- Anyone who works with LLMs daily will notice at least one of these patterns.
**Severity:** Major -- Does not invalidate the article but erodes credibility of the "authentic voice" claim. If the article about LLM prompting reads like it was written by an LLM, the irony is fatal.
**Evidence:** Lines 17-18, 19, 64-65, 69 in the deliverable.
**Dimension:** Evidence Quality (the article's credibility as an authentic artifact)
**Mitigation:** Rewrite flagged passages using less symmetrical constructions. Break the three-beat pattern on lines 17-18 into asymmetric phrasing. Replace the "That's not X. It's Y" on line 19. Rephrase the "from X to Y" listing on lines 64-65 to cite one specific example rather than a range. Replace the epigrammatic inversion on line 69 with a more conversational phrasing.
**Acceptance Criteria:** Zero passages that a trained LLM-output reviewer would flag as probable LLM generation on a blind read.

---

### PM-002-20260223-v2: "Fluency-Competence Gap" Term Is Not Established Terminology [MAJOR]

**Failure Cause:** A prompt engineering researcher reads the article and searches for "fluency-competence gap" as a term of art. They find no canonical source. The article presents it as a named phenomenon ("has a name. It's called the 'fluency-competence gap'") but the term does not appear in any major paper with that exact phrasing. The citations.md companion file maps this claim to Sharma et al. (sycophancy), Chen et al. (sycophancy causes), and Bender & Koller (form vs. meaning) -- none of which use this exact term. The article is creating a neologism and presenting it as established terminology. An expert reader calls this out as either fabrication or hallucination, and the article's technical credibility collapses.

**Category:** Technical (factual accuracy)
**Likelihood:** MEDIUM -- Only an expert checking sources would catch this. But experts are exactly the audience whose criticism would be most damaging.
**Severity:** Major -- Presenting a coined term as established science is a credibility-destroying move in technical writing. It is also ironic given that the article itself warns about LLMs generating confident-sounding claims that are not grounded.
**Evidence:** Line 19: "It's called the 'fluency-competence gap,' a pattern documented across model families since GPT-3." Also citations.md section 1 -- the supporting sources do not use this term.
**Dimension:** Evidence Quality, Methodological Rigor
**Mitigation:** Two options: (A) Reframe the term as a descriptive label rather than established terminology: "You could call it a fluency-competence gap" or "Think of it as a fluency-competence gap." This signals it is a useful descriptor, not a canonical term. (B) Replace with a term that IS established: "sycophancy" or "the form-meaning gap" (Bender & Koller 2020). Option A is more McConkey-voice-compatible.
**Acceptance Criteria:** No passage presents a coined term as an established named phenomenon without qualification.

---

### PM-003-20260223-v2: Liu et al. Citation Year Discrepancy [MINOR]

**Failure Cause:** The article cites "Liu et al. (2023)" on line 55. The citations.md companion file notes this paper was "Originally released as arXiv preprint, July 2023" but published in TACL 2024. A pedantic reader (or a researcher who knows this paper) would flag the year discrepancy. The preprint date is defensible, but mixing preprint and publication dates without noting the distinction looks sloppy.

**Category:** Technical (citation accuracy)
**Likelihood:** LOW -- Most readers will not check the citation year.
**Severity:** Minor -- Does not invalidate the claim. The paper is real, the finding is real.
**Evidence:** Line 55, citations.md section 2.
**Dimension:** Traceability
**Mitigation:** Either cite as "Liu et al. (2023; published 2024)" or simply use "(2024)" to match the formal publication. In a voice-first article, the exact year matters less than the finding itself.
**Acceptance Criteria:** Citation year matches a defensible publication date.

---

### PM-004-20260223-v2: The Article Tells You What To Think About LLMs, Not How To Think With Them [MAJOR]

**Failure Cause:** A practitioner reads the article, understands the three levels, and then opens their LLM of choice to work on a real problem. They try Level 2. The article's Level 2 example is: "Research the top 10 industry frameworks for X. For each, cite the original source. Then analyze this repo against the top 5. Show your selection criteria." But the practitioner's task is not about industry frameworks. It is about writing a marketing email, or debugging a Python error, or summarizing meeting notes. The Level 2 example is domain-specific (framework evaluation) and the reader cannot generalize it to their domain. The three principles at the end ARE generalizable, but they are abstract ("constrain the work"). The gap between the abstract principles and the domain-specific example is where the reader falls through.

**Category:** Assumption (assumes reader can generalize from one domain-specific example)
**Likelihood:** HIGH -- Most readers will encounter this gap on their first attempt to apply the advice.
**Severity:** Major -- The article's entire value proposition is "change how you prompt." If the reader cannot translate the examples to their own work, the article fails at its primary goal.
**Evidence:** Lines 24-26 (Level 2 example), lines 35-36 (Level 3 example) -- both are framework-evaluation-specific. Lines 73-77 (Three Principles) -- abstract without domain translation. Lines 83-89 (checklist) -- generic but lacks a worked example of applying it to a non-framework task.
**Dimension:** Actionability, Completeness
**Mitigation:** Add a brief second example at Level 2 or in the "Start Here" section that applies the principles to a different task domain. Even one sentence: "This works the same way for debugging: instead of 'fix this error,' try 'Here is the error and the relevant code. Identify three possible root causes, rank them by likelihood, and show me which one you recommend fixing first before you write the fix.'" This demonstrates generalizability.
**Acceptance Criteria:** At least two distinct task domains represented in the examples, demonstrating the principles are not framework-evaluation-specific.

---

### PM-005-20260223-v2: The Two-Session Pattern Assumes Technical Sophistication the Target Audience Lacks [MAJOR]

**Failure Cause:** The "Two-Session Pattern" section (lines 47-59) is the most technically novel and valuable part of the article. It is also the part most likely to lose the target audience. The section assumes the reader understands: (a) what a "context window" is mechanically, (b) what "tokens" are and why they are finite, (c) what "retrieval and reasoning tasks" means in the LLM context, (d) what "role clarity" means for a model. Line 63 acknowledges context windows are "hard engineering constraints" but the explanation of WHY the two-session pattern works is written for someone who already understands LLM architecture. The target reader does not. They hear "start a new conversation" and think "why would I throw away all that context?"

**Category:** Assumption (assumes technical vocabulary the audience does not have)
**Likelihood:** HIGH -- The two-session pattern is counterintuitive. Without understanding WHY it works, readers will not do it.
**Severity:** Major -- If the reader does not adopt the two-session pattern, they miss the article's most valuable advice.
**Evidence:** Lines 47-59 (entire Two-Session Pattern section). Line 55 specifically: "Token budget is zero-sum. Every token of planning conversation is occupying space in the context window that should be used for execution." This sentence assumes the reader knows what tokens are.
**Dimension:** Actionability, Completeness
**Mitigation:** Add one concrete analogy that explains WHY a fresh conversation helps, without requiring the reader to understand tokens or context windows. Example: "Think of it like this: if you spent an hour arguing about the blueprint with your contractor, and then said 'OK, now build it' -- they would be thinking about the argument, not the blueprint. A fresh conversation gives the model just the blueprint, nothing else." Then the token/context explanation becomes supplementary detail for technically curious readers, not the load-bearing explanation.
**Acceptance Criteria:** The two-session pattern rationale is understandable to a reader who does not know what tokens or context windows are.

---

### PM-006-20260223-v2: McConkey Voice Breaks at Technical Depth [MEDIUM]

**Failure Cause:** The McConkey persona is strongest in the opening (lines 3-9), the transitions ("You don't just fire the prompt and let it run," line 49), and the closing (lines 93-97). But it drops entirely in the technical explanation passages. Lines 27, 42, 55-56, and 63-68 read as competent technical writing with no discernible personality. This creates a tonal oscillation: warm/direct/McConkey, then neutral/expository, then warm/direct/McConkey again. A reader sensitive to voice will feel the seams. This is not a tell that an LLM wrote it specifically -- plenty of human writers struggle with maintaining voice through technical passages. But it weakens the "Saucer Boy" brand promise, which is that the persona and the technical content are fused, not alternating.

Specific passages where voice drops:

- Line 27: "Structured instructions focus the model's attention on relevant context and narrow the space of acceptable completions. Vague instructions leave the model to fill in every unspecified dimension with defaults." -- This reads like a textbook. McConkey would not say "narrow the space of acceptable completions."
- Lines 55-56: "Research has shown that model performance on retrieval and reasoning tasks degrades as context length grows." -- Academic register. No persona present.
- Line 65: "This is a well-documented finding across prompt engineering research, from chain-of-thought prompting to structured role-task-format patterns." -- Survey-paper phrasing.

**Category:** Process (voice consistency failure)
**Likelihood:** MEDIUM -- Casual readers will not notice. Voice-sensitive readers and the Saucer Boy editorial team will.
**Severity:** Medium -- Does not undermine the technical content but weakens the brand differentiation.
**Evidence:** Lines 27, 55-56, 65 as cited above.
**Dimension:** Internal Consistency (voice should be consistent throughout)
**Mitigation:** Rewrite the flagged passages to maintain the McConkey voice even in technical depth. Line 27 could become: "Specific instructions make the model pay attention to the right stuff and cut off the lazy exits. Vague instructions leave every door open, and the model walks through the easiest one." Line 55-56 could become: "There is solid research showing that the longer the conversation gets, the worse the model performs at finding and using information buried in it." Line 65: fold the examples into the claim rather than listing them as a parenthetical survey.
**Acceptance Criteria:** No passage reads as a register shift from the surrounding McConkey-voiced text. A reader should not be able to draw a line between "persona sections" and "technical sections."

---

### PM-007-20260223-v2: SEO and Discoverability Failure for mkdocs Publication [MEDIUM]

**Failure Cause:** The article title is "Why Structured Prompting Works." This is a reasonable title but has low search differentiation. Searching for this phrase returns dozens of articles from OpenAI, Anthropic, Prompt Engineering Guide, and every AI newsletter. The article will be buried in search results. The McConkey/skiing framing, which is the article's unique differentiator, is invisible in the title and first paragraph. A potential reader scanning search results sees "Why Structured Prompting Works" and has no reason to click this one over the Anthropic or OpenAI version.

Additionally, the article has no frontmatter/metadata. For an mkdocs site, this means no description meta tag, no og:description, no structured data. The article is invisible to social sharing previews.

**Category:** External (publication platform requirements)
**Likelihood:** MEDIUM -- If the site has low traffic and relies on direct links, this matters less. If growth depends on search, this is critical.
**Severity:** Medium -- The article could be excellent and still fail because nobody finds it.
**Evidence:** Line 1 (title), no frontmatter present.
**Dimension:** Completeness (publication-readiness)
**Mitigation:** (A) Add mkdocs-compatible frontmatter with description and tags. (B) Consider a more distinctive title that signals the unique angle: "The McConkey Rule: Why Structured LLM Prompting Works" or "Point Downhill and Hope: Three Levels of LLM Prompting." (C) Add a subtitle or deck that contains searchable terms: "A practitioner's guide to getting better output from Claude, GPT, and every other language model."
**Acceptance Criteria:** Article has mkdocs-compatible frontmatter with description. Title has some search differentiation.

---

### PM-008-20260223-v2: The "`</output>`" Tag on Line 98 Is a Publication Artifact [MINOR]

**Failure Cause:** Line 98 contains a raw `</output>` XML tag. This is a processing artifact from the LLM generation pipeline. If published as-is to mkdocs, it will render as visible text or as a malformed HTML tag depending on the markdown renderer. This is the single most damaging LLM-tell possible -- a literal XML tag from the generation framework visible in the published output.

**Category:** Technical (artifact contamination)
**Likelihood:** HIGH -- It is present in the current file.
**Severity:** Minor in isolation (easy to fix), but if it reaches production it becomes Critical (proves the article is LLM-generated output published without review).
**Evidence:** Line 98: `</output>`
**Dimension:** Evidence Quality (article authenticity)
**Mitigation:** Remove the `</output>` tag.
**Acceptance Criteria:** No XML processing artifacts present in the published file.

---

### PM-009-20260223-v2: Expert Audience May Find the Content Too Elementary [MEDIUM]

**Failure Cause:** The article's target audience appears to be intermediate LLM users -- people who use LLMs regularly but have not studied prompt engineering formally. For this audience, the article is well-calibrated. But the article will also be read by experts (prompt engineers, AI researchers, LLM application developers) who already know everything in it. These readers will find the content elementary and may publicly characterize it as "prompt engineering 101 with a skiing metaphor." If the Saucer Boy brand aims to be taken seriously by technical audiences, an article that covers well-trodden ground (structured prompts are better than vague prompts) without adding novel insight risks positioning the brand as introductory rather than authoritative.

The one genuinely novel element is the two-session pattern with the "lost in the middle" citation. But this is one section in an article where the rest covers ground that has been thoroughly explored in prompt engineering literature since 2023.

**Category:** External (audience-market fit)
**Likelihood:** MEDIUM -- Depends on audience composition.
**Severity:** Medium -- Does not harm intermediate readers but may limit the brand's ceiling.
**Evidence:** The core thesis ("structured prompts produce better output") is the foundational claim of every prompt engineering guide published since 2022.
**Dimension:** Evidence Quality, Methodological Rigor (novelty contribution)
**Mitigation:** Two options: (A) Accept this as the intended audience calibration and ensure the article is explicitly positioned as a practitioner guide, not a research contribution. (B) Add one section with genuinely novel content -- the error compounding insight (lines 44-45) is the closest candidate, and could be expanded with a concrete example showing HOW errors compound through phases, which no mainstream prompt engineering guide covers well. This would give experts something they have not seen before.
**Acceptance Criteria:** Either the article is explicitly positioned for intermediate users (no pretension to expert novelty) or it contains at least one section with genuinely novel insight.

---

## Findings Table

| ID | Failure Cause | Category | Likelihood | Severity | Priority | Affected Dimension |
|----|---------------|----------|------------|----------|----------|--------------------|
| PM-001-20260223-v2 | Residual LLM-tell patterns detectable by trained readers | Technical | High | Major | P0 | Evidence Quality |
| PM-002-20260223-v2 | "Fluency-competence gap" presented as established term but is a neologism | Technical | Medium | Major | P1 | Evidence Quality, Methodological Rigor |
| PM-003-20260223-v2 | Liu et al. citation year discrepancy (2023 vs. 2024) | Technical | Low | Minor | P2 | Traceability |
| PM-004-20260223-v2 | Examples are domain-specific; reader cannot generalize | Assumption | High | Major | P0 | Actionability, Completeness |
| PM-005-20260223-v2 | Two-session pattern rationale requires technical sophistication audience lacks | Assumption | High | Major | P1 | Actionability, Completeness |
| PM-006-20260223-v2 | McConkey voice breaks at technical depth | Process | Medium | Medium | P1 | Internal Consistency |
| PM-007-20260223-v2 | No frontmatter, undifferentiated title for mkdocs publication | External | Medium | Medium | P1 | Completeness |
| PM-008-20260223-v2 | Raw `</output>` XML tag on line 98 | Technical | High | Minor | P0 | Evidence Quality |
| PM-009-20260223-v2 | Content is elementary for expert audience | External | Medium | Medium | P2 | Evidence Quality, Methodological Rigor |

---

## Recommendations

### P0 -- MUST Mitigate Before Publication

**PM-008-20260223-v2:** Remove the `</output>` tag on line 98. This is a 2-second fix with catastrophic consequences if missed.

**PM-001-20260223-v2:** Rewrite the four flagged LLM-tell passages (lines 17-18, 19, 64-65, 69) using asymmetric, conversational phrasing. Break parallel three-beat structures. Replace "That's not X. It's Y" constructions. Fold parenthetical research surveys into the claim rather than listing them.

**PM-004-20260223-v2:** Add one brief example from a non-framework-evaluation domain (debugging, writing, data analysis) to demonstrate the principles generalize. Can be a single sentence in the "Start Here" section or an aside in the Level 2 section.

### P1 -- SHOULD Mitigate Before Publication

**PM-002-20260223-v2:** Reframe "fluency-competence gap" as a descriptive label, not an established term. Change "It's called" to "You could call it" or "Think of it as."

**PM-005-20260223-v2:** Add one concrete analogy for the two-session pattern that does not require understanding tokens or context windows. The blueprint/contractor analogy or similar.

**PM-006-20260223-v2:** Rewrite 2-3 of the most voice-dropped passages (lines 27, 55-56, 65) to maintain McConkey register.

**PM-007-20260223-v2:** Add mkdocs-compatible frontmatter (title, description, tags). Consider a more distinctive title.

### P2 -- MAY Mitigate; Acknowledge Risk

**PM-003-20260223-v2:** Verify citation year preference (preprint vs. publication) and use consistently.

**PM-009-20260223-v2:** Accept elementary-audience positioning or expand the error-compounding section with a concrete multi-phase example.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | PM-004 (domain-specific examples), PM-005 (two-session pattern accessibility), PM-007 (no frontmatter). The article covers the topic but has gaps in generalizability and publication readiness. |
| Internal Consistency | 0.20 | Negative | PM-006 (voice breaks at technical depth). The tonal oscillation between McConkey voice and neutral technical prose creates inconsistency. |
| Methodological Rigor | 0.20 | Negative | PM-002 (neologism presented as established term), PM-009 (elementary content for expert audience). The article's claims are accurate but the framing overstates the terminological grounding. |
| Evidence Quality | 0.15 | Negative | PM-001 (LLM-tell patterns), PM-002 (neologism), PM-008 (XML artifact). The article's credibility as an authentic, human-authored artifact is undermined by residual tells and a processing artifact. |
| Actionability | 0.15 | Negative | PM-004 (cannot generalize examples), PM-005 (two-session rationale too technical). The checklist is strong but the examples do not bridge to diverse use cases. |
| Traceability | 0.10 | Neutral | PM-003 (citation year) is minor. The citations.md companion file provides strong traceability for all claims. Within-article traceability is adequate for the genre. |

**Estimated composite impact of P0/P1 mitigations:** If all P0 and P1 items are addressed, the article would close the LLM-tell risk, improve domain generalizability, make the two-session pattern accessible, maintain voice consistency, and prepare for mkdocs publication. This would maintain or improve the 0.938 composite score from iteration 3 while addressing failure modes specific to the publication context that were not evaluated in previous iterations.

---

## LLM-Tell Assessment

**Score: 0.72** (where 1.0 = no detectable LLM tells)

The draft-5 LLM-tell cleaning pass improved the article substantially from earlier drafts. However, four categories of residual tells remain:

| Tell Category | Instances | Severity | Lines |
|---------------|-----------|----------|-------|
| Three-beat parallel declaratives | 1 | Medium | 17-18 |
| "That's not X. It's Y" rhetorical inversion | 1 | Medium | 19 |
| "From X to Y" parenthetical survey | 1 | Medium | 64-65 |
| Epigrammatic concept-inversion closer | 1 | Low | 69 |
| Raw XML processing artifact | 1 | Critical | 98 |

**Assessment methodology:** Each passage was evaluated against the question: "If 100 people who work with LLMs daily read this blind (no author attribution), how many would flag this passage as probably LLM-generated?" Passages where the answer exceeds 30% are flagged.

**Note on the `</output>` tag:** This is not an LLM "tell" in the stylistic sense. It is a literal artifact from the generation pipeline. Its presence in a published article would not merely suggest LLM authorship -- it would prove it. This must be removed regardless of any other revision decision.

**Passages that are NOT tells despite appearing machine-like:**
- Line 7 opening ("Think of it like big-mountain skiing"): Could be flagged as a "let me use an analogy" LLM pattern, but the McConkey context makes this a natural, persona-driven choice rather than a generic analogy deployment.
- Line 42 bullet structure: Bulleted lists are common in both LLM and human technical writing. The content of these bullets is specific enough to not trigger tell detection.
- The three-principles structure (lines 73-77): Numbered principle lists are an LLM pattern, but the principles themselves are specific, non-obvious, and well-argued. The structure is conventional for technical articles regardless of authorship.

---

## Voice Authenticity Assessment

**Score: 0.78** (where 1.0 = fully authentic, consistent McConkey voice throughout)

**Strongest voice passages:**
- Lines 3-9 (opening): Direct, warm, peer-to-peer. "Alright, this trips up everybody, so don't feel singled out." Reads as genuinely McConkey.
- Lines 11-15 (Level 1): "Point Downhill and Hope" as a section title. The skiing vocabulary is organic.
- Lines 49-51 (Two-Session Pattern opening): "You don't just fire the prompt and let it run." Direct, action-oriented.
- Lines 93-97 (closing): The McConkey callback and the dare. Strong voice, strong close.

**Weakest voice passages:**
- Line 27: "Structured instructions focus the model's attention on relevant context and narrow the space of acceptable completions." -- Textbook register. McConkey would never say "narrow the space of acceptable completions."
- Lines 55-56: "Research has shown that model performance on retrieval and reasoning tasks degrades as context length grows." -- Academic passive voice. No personality.
- Line 63: "Context windows are hard engineering constraints, determined by architecture, memory, and compute tradeoffs." -- Competent technical writing, but indistinguishable from any technical blog post.
- Line 65: "This is a well-documented finding across prompt engineering research, from chain-of-thought prompting to structured role-task-format patterns." -- Survey-paper phrasing. Zero McConkey.

**Voice distribution:** Approximately 65% of the article maintains the McConkey voice. The remaining 35% drops into neutral technical prose. The drops cluster in the explanatory passages between examples and principles -- exactly the passages where voice maintenance is hardest but also where it matters most for brand differentiation.

**Comparison to draft 4 (human rewrite):** Draft 4 maintained a more consistent voice throughout, including in technical passages. For example, draft 4's equivalent of line 27 reads: "specific instructions literally narrow the space of outputs the model considers acceptable. Vague instructions let it fill in every blank with defaults." The word "literally" and the phrase "let it fill in every blank" are more conversational. Draft 5's cleaning pass may have over-corrected some passages toward formality while cleaning tells, inadvertently stripping persona markers alongside LLM artifacts.

---

## Change Assessment: Iteration 1 Findings Status

| Iteration 1 Finding | Status in Draft 5 | Notes |
|---------------------|--------------------|-------|
| PM-001 (no checklist) | RESOLVED | Lines 83-89 contain a copy-pasteable checklist |
| PM-002 (no intermediate example) | RESOLVED | Lines 21-29 (Level 2 section) provide the intermediate example |
| PM-003 (skiing analogy may not land) | RESOLVED | Lines 7-8 introduce McConkey for non-skiers |
| PM-004 (clear context unexplained) | RESOLVED | Lines 51-57 explain the two-session pattern mechanically |
| PM-005 (jargon grenades) | RESOLVED | Jerry-specific terminology replaced with universal language throughout |
| PM-006 (wall of text) | PARTIALLY RESOLVED | Better structure with section headings, but some long paragraphs remain |
| PM-007 (no call to action) | RESOLVED | Lines 93-97 end with a concrete challenge and dare |

**Net assessment:** 6 of 7 iteration-1 findings fully resolved, 1 partially resolved. Draft 5 is a meaningfully improved article. The new findings in this iteration are primarily about publication-readiness concerns (LLM tells, voice consistency, mkdocs metadata, domain generalizability) that were out of scope for the iteration-1 pre-mortem which evaluated the article as a conversational response.
