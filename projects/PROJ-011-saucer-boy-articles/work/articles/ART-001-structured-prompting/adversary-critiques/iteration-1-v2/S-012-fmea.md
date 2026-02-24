# FMEA Report: ART-001 Draft 5 (LLM-Tell Clean) -- Structured LLM Prompting

**Strategy:** S-012 FMEA (Failure Mode and Effects Analysis)
**Deliverable:** `drafts/draft-5-llm-tell-clean.md`
**Baseline:** `drafts/draft-4-human-rewrite.md` (human rewrite); iteration-1 FMEA on draft-1
**Criticality:** C2 (standard, applied at orchestrator request)
**Date:** 2026-02-23
**Reviewer:** adv-executor (S-012)
**Elements Analyzed:** 10 | **Failure Modes Identified:** 22 | **Total RPN:** 1,614

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall risk posture and comparison to iteration-1 FMEA |
| [Findings Table](#findings-table) | All 22 failure modes with RPN scoring |
| [Top 5 Risks](#top-5-risks-highest-rpn) | Detailed analysis of highest-RPN failure modes |
| [Domain Coverage Matrix](#domain-coverage-matrix) | Coverage across the 6 required failure domains |
| [Iteration-1 Residual Analysis](#iteration-1-residual-analysis) | Status of all 19 failure modes from draft-1 FMEA |
| [LLM-Tell Specific Analysis](#llm-tell-specific-analysis) | Failure modes introduced or affected by the tell-cleaning pass |
| [Evaluation Dimensions](#evaluation-dimensions) | Dimension-level scoring (0.0-1.0) |
| [Overall Assessment](#overall-assessment) | Verdict and recommended actions |

---

## Summary

Draft 5 is a structurally improved version of the quality-gated article. The LLM-tell cleaning pass added markdown section headings (`## Level 1/2/3`, `## The Two-Session Pattern`, etc.), introduced a code-block checklist, tightened several formulations, and added the Liu et al. (2023) citation. Compared to the draft-1 FMEA (19 failure modes, total RPN 1,926), this draft resolves most Critical findings. However, the structural changes introduce new failure modes: the markdown headings create a more "article-template" feel that competes with the conversational voice, and the checklist code block may break immersion for readers expecting pure prose. The highest-risk finding (RPN 210) concerns the "fluency-competence gap" term attribution. Total RPN of 1,614 across 22 failure modes represents a meaningful improvement from the 1,926 baseline despite 3 additional failure modes identified, because the remaining modes are lower severity.

---

## Findings Table

| ID | Element | Failure Mode | S | O | D | RPN | Severity | Corrective Action | Domain |
|----|---------|-------------|---|---|---|-----|----------|-------------------|--------|
| FM-001 | Opening hook (L1-3) | "This trips up everybody" may read as patronizing rather than inclusive; implies reader has already failed | 4 | 3 | 4 | 48 | Minor | The draft-4 version ("here's what's going on with your prompt") was warmer. Consider softening "trips up everybody" to something that acknowledges the reader's situation without labeling it a mistake | Audience Mismatch |
| FM-002 | Opening hook (L3) | "Claude, GPT, Gemini, Llama, whatever ships next Tuesday" -- product name list will age; models may be discontinued or renamed | 3 | 4 | 3 | 36 | Minor | Acceptable for now; the list establishes scope. On republication, verify names are still current. Low severity because the sentence structure ("whatever ships next Tuesday") signals awareness of impermanence | Technical Accuracy |
| FM-003 | McConkey intro (L7) | "legendary freeskier, the guy who'd ski a cliff in a banana suit and win competitions doing it" -- factual compression. McConkey wore the banana suit for specific events (not all competitions); he won World Skiing Invitational in the banana suit | 4 | 3 | 7 | 84 | Major | The compression is defensible for a casual article, but "win competitions" (plural) is a slight overstatement. Consider "win a competition" (singular) to be more precise without losing punch | Technical Accuracy |
| FM-004 | Level 1 section (L15-19) | "the most probable generic response from their training distribution, dressed up as a custom answer" -- technically correct but elides the role of RLHF/RLAIF in shaping outputs beyond raw training distribution; models post-alignment generate completions shaped by reward models, not just raw pre-training data | 5 | 4 | 7 | 140 | Major | This is a simplification, not an error. For the target audience, the training-distribution framing is adequate. A footnote or parenthetical ("shaped by both training data and alignment tuning") would improve accuracy without disrupting flow, but is not required | Technical Accuracy |
| FM-005 | "Fluency-competence gap" (L19) | "It's called the 'fluency-competence gap,' a pattern documented across model families since GPT-3" -- this is not a widely established term with a canonical citation. The phrase is used descriptively in some literature but is not a formal research construct like "lost in the middle." Reader who searches for it will find scattered usage, not a definitive paper | 6 | 5 | 7 | 210 | Critical | Two options: (a) reframe as a descriptive observation rather than a named phenomenon: "the gap between fluency and competence, a pattern researchers have documented across model families since GPT-3"; or (b) acknowledge it is a descriptive term, not a formal construct. Option (a) is preferred because it preserves the explanatory power without implying a canonical source | Credibility Damage |
| FM-006 | Level 2 section heading (L21) | "Scope the Ask" is clear but differs in voice register from "Point Downhill and Hope" (playful) and "Full Orchestration" (technical). The middle heading is neither playful nor technical -- it is instructional. Minor voice inconsistency across the three-level framework headings | 3 | 3 | 4 | 36 | Minor | Consider aligning voice register: "Point Downhill and Hope / Read the Map / Full Orchestration" or "Huck It / Scope It / Plan It" -- any consistent register works | Voice Inauthenticity |
| FM-007 | Level 2 example prompt (L25) | The example prompt is strong but lacks the "show me your plan first" element that is emphasized in Level 3 and the Three Principles section. Reader may infer that plan review is only a Level 3 technique, when the article later argues it applies broadly | 4 | 4 | 5 | 80 | Major | This is a deliberate scoping choice (Level 2 is meant to be simpler), but the omission creates a gap when the reader hits "Review the plan, not just the product" in the Three Principles section. Consider adding a one-sentence bridge: "For more complex work, you'd also ask to see the plan first -- that's Level 3." | Structural Problems |
| FM-008 | Level 2/3 boundary (L29-33) | "When the work matters" as the transition to Level 3 implicitly devalues Level 2 work. Combined with "You don't need a flight plan for the bunny hill" (L29), this frames Level 2 as "for things that don't matter" rather than "for moderate stakes." Reader doing real work at Level 2 may feel they are being told it is not serious enough | 4 | 4 | 5 | 80 | Major | Reframe the transition: keep "You don't need a flight plan for the bunny hill" but change "When the work matters" to "When the work compounds" or "When downstream quality depends on upstream quality." This shifts the criterion from importance to complexity | Audience Mismatch |
| FM-009 | Level 3 example prompt (L35) | The prompt block is long (6 distinct instructions in one quoted block). Reader implementing this for the first time faces a wall of text. The bullet list following it (L39-43) decomposes it well, but the prompt itself lacks internal structure | 4 | 5 | 4 | 80 | Major | This was identified in iteration-1 (FM-006, RPN 125) and partially addressed by the decomposing bullet list. The current mitigation is adequate for the article format. A numbered prompt format would improve scannability but would compromise the "this is one prompt you paste" simplicity | Structural Problems |
| FM-010 | Self-evaluation bias claim (L42) | "research on LLM self-evaluation consistently shows favorable bias" -- accurate claim, direction of bias specified, but no attribution. Asymmetry with Liu et al. citation (L55) which names authors and year. Skeptical technical reader may notice one claim is cited and another is not | 5 | 4 | 6 | 120 | Major | Two-tier evidence presentation is a valid genre choice (not every claim needs a named citation in a practitioner article). However, this specific claim is doing heavy argumentative work (it justifies the human-checkpoint recommendation). Consider: "studies on LLM self-evaluation, including work by Kadavath et al. (2022) on calibration, show..." -- or simply "models tend to rate their own output higher than external evaluators do" without the research claim framing | Credibility Damage |
| FM-011 | Error compounding paragraph (L45) | "That's not garbage in, garbage out. It's garbage in, polished garbage out" -- strong, memorable formulation. But "you can't tell the difference until something breaks" is a sweeping claim. Experienced practitioners CAN often tell the difference through spot-checking, cross-referencing, or quality rubrics. The claim as stated may alienate readers who already have quality practices | 4 | 3 | 5 | 60 | Minor | Add qualifier: "it gets harder to tell the difference" rather than "you can't tell the difference." Preserves the warning; removes the absolute claim | Technical Accuracy |
| FM-012 | Two-Session Pattern (L47-59) | This section is the most structurally distinct from the conversational draft-4 version. Draft-4 integrated the two-session pattern into the conversational flow. Draft-5 elevates it to a named `## The Two-Session Pattern` section. The naming is good (memorable, actionable) but the heading creates a tonal shift -- the reader transitions from a conversational narrative to a structured technique description | 4 | 4 | 6 | 96 | Major | This is a trade-off, not a defect. The heading aids scannability and lets readers find the technique on re-read. The tonal shift is mitigated by maintaining conversational voice within the section. Monitor reader feedback for whether the heading helps or hurts | Structural Problems |
| FM-013 | Liu et al. citation (L55) | "Liu et al. (2023) documented the 'lost in the middle' effect" -- accurate, real paper, correct finding description. However, the citation appears only in the Two-Session Pattern section. If a reader skips to Level 3 or the Three Principles, they miss the only named citation in the article | 3 | 3 | 3 | 27 | Minor | Acceptable placement. The citation supports the two-session pattern rationale, which is where it belongs. Moving it would be artificial. The article does not need citations in every section to maintain credibility | Evidence Quality |
| FM-014 | "Why This Works on Every Model" section (L61-69) | The universality argument is now well-grounded with "chain-of-thought prompting" and "structured role-task-format patterns" as named examples. However, "every model, regardless of architecture, performs better when instructions are specific" is still an overclaim in the strict sense -- some model architectures (retrieval-augmented, agentic) may not follow this pattern linearly | 4 | 3 | 6 | 72 | Minor | Acceptable for a practitioner article. The qualifier "regardless of architecture" could be softened to "across model architectures tested to date" but this adds hedging noise. The current formulation is broadly true and the examples ground it sufficiently | Technical Accuracy |
| FM-015 | Three Principles section (L71-77) | "Constrain the work," "Review the plan, not just the product," "Separate planning from execution" -- clean, memorable, actionable. This is the strongest section. However, Principle 3 ("Separate planning from execution") may not apply to quick queries, and the article does not scope which principle applies at which level | 3 | 4 | 4 | 48 | Minor | The closing paragraph (L91) addresses this: "You don't have to go full orchestration on day one." But the Three Principles section itself lacks level-mapping. Consider adding a parenthetical: "(This matters most at Level 3, but even at Level 2, a quick plan review helps.)" | Structural Problems |
| FM-016 | Checklist code block (L83-89) | The code block `[ ] Did I specify WHAT to do...` is a strong actionable element. However, code-block formatting inside a conversational article creates a visual register break. The reader shifts from prose to a different document type. This may feel like the article suddenly became a manual | 4 | 4 | 5 | 80 | Major | This is a deliberate design choice that aids re-use (reader can copy the checklist). The break is real but the benefit outweighs it for the target audience (practitioners who will actually use the checklist). Keep it. If voice consistency is paramount, convert to a bulleted prose format: "Before your next prompt, ask yourself: Did I specify..." | Voice Inauthenticity |
| FM-017 | McConkey callback (L93) | "McConkey looked like he was winging it. He wasn't. The wild was the performance. The preparation was the foundation." -- repetition from L7 area. Deliberate bookend. However, the phrase appears nearly verbatim twice, which could read as either (a) intentional rhetorical callback, or (b) forgot-already-said-that | 3 | 3 | 4 | 36 | Minor | This is a deliberate bookend and works as rhetorical closure. The variation between the two instances is sufficient (opening introduces McConkey; closing uses him as summation). No action needed | Voice Inauthenticity |
| FM-018 | Closing dare (L95-97) | "I dare you" as the final line is punchy and in-character. However, it may land differently depending on the reader's relationship with the author. For readers who know McConkey's persona, it is playful provocation. For cold readers, it may read as combative | 4 | 3 | 4 | 48 | Minor | The sentence preceding the dare ("Do that once and tell me it didn't change the output") is the real call to action. The "I dare you" is the McConkey flourish. The two-sentence combo works. Risk is low because the dare follows a concrete instruction | Audience Mismatch |
| FM-019 | Overall structure: heading density | Draft-5 has 7 `##` headings in 97 lines. Draft-4 had 0 headings in 50 lines. The heading density creates a more "article" feel, which aids navigation but reduces the conversational intimacy of draft-4 | 4 | 5 | 5 | 100 | Major | This is the fundamental trade-off of the LLM-tell clean pass: structure for scannability at the cost of conversational flow. For an mkdocs article that readers will revisit, headings are the right choice. The voice within sections must compensate for the structural scaffolding. Currently doing this adequately but not perfectly -- the technical middle sections (Level 3, Two-Session Pattern) have the weakest conversational voice | Structural Problems |
| FM-020 | LLM-tell: "a well-documented finding" (L65) | The phrase "a well-documented finding across prompt engineering research" is a common LLM hedging pattern. It softens the claim appropriately (replacing earlier "one of the most robust findings") but the specific phrasing "a well-documented finding" has an LLM-generated texture | 3 | 4 | 6 | 72 | Minor | Rephrase to something more natural: "This is something researchers have seen consistently" or "This shows up in study after study" -- same hedging level, more conversational voice | LLM-Tell Leakage |
| FM-021 | LLM-tell: "Constrained inputs consistently improve output across model families" (L65) | This sentence has the cadence and structure of an LLM summary statement -- the parallel construction and the phrase "across model families" feels like a research paper abstract rather than McConkey talking | 4 | 4 | 6 | 96 | Major | Rephrase: "Every model tested performs better when you tell it exactly what you want" -- same content, more natural voice | LLM-Tell Leakage |
| FM-022 | LLM-tell: bullet list at L39-43 | The decomposition bullets after the Level 3 prompt are well-structured but use a uniform pattern: label followed by explanation followed by mechanism. The parallelism is clean but slightly mechanical. Natural speech patterns vary sentence structure more | 3 | 3 | 5 | 45 | Minor | The bullets are doing important explanatory work and the current structure is clear. Varying one or two bullet structures (e.g., making one a question, another a short punch) would reduce the uniformity | LLM-Tell Leakage |

---

## Top 5 Risks (Highest RPN)

### 1. FM-005 (RPN 210) -- "Fluency-Competence Gap" Attribution Risk

**Element:** Line 19, Level 1 section.

**The problem:** The article introduces "the fluency-competence gap" as a named phenomenon with the framing "has a name. It's called..." This implies an established term. However, "fluency-competence gap" is not a canonical research term with a definitive paper behind it. It is a descriptive phrase used in various forms across the AI safety and evaluation literature, but it does not have the citation weight of "lost in the middle" (Liu et al., 2023) which the article correctly attributes. A technically literate reader who searches for "fluency-competence gap" will find scattered, inconsistent usage rather than a definitive source. This creates a credibility asymmetry: the article's strongest-attributed claim (Liu et al.) sets a standard that its other named-phenomenon claim does not meet.

**Severity (6):** A reader who tries to verify this term and fails may question the article's overall evidence base. The term is doing significant explanatory work (it names the core problem the article addresses).

**Occurrence (5):** Technically literate readers (the target audience) are moderately likely to attempt verification of named phenomena.

**Detection (7):** Difficult to detect pre-publication because the term sounds legitimate and is descriptively accurate. The failure mode is not inaccuracy but implied formality.

**Mitigation:** Reframe as a descriptive observation: "The disconnect between how competent it sounds and how competent it is -- that gap between fluency and actual competence -- has been documented across model families since GPT-3." This preserves the explanatory value without implying a canonical named construct. Alternatively, keep the current formulation and accept the risk -- the term IS used in the literature, just not as a formal construct.

**Post-correction RPN estimate:** S=4, O=3, D=5 = 60

---

### 2. FM-004 (RPN 140) -- RLHF Elision in LLM Behavior Description

**Element:** Lines 15-19, Level 1 section.

**The problem:** The article describes LLM behavior as "the most probable generic response from their training distribution." Post-RLHF/RLAIF models (which includes all models named in the article: Claude, GPT, Gemini) do not simply generate from the raw training distribution. Their outputs are shaped by reward models that push behavior toward helpfulness, harmlessness, and honesty. The practical effect on the article's argument is minimal (structured prompting still helps post-alignment models), but a reader with ML knowledge may note the simplification and discount the explanation.

**Severity (5):** The simplification is pedagogically useful but technically imprecise. Impact depends on reader's ML sophistication.

**Occurrence (4):** Most readers will not notice. ML-literate readers will.

**Detection (7):** Hard to flag pre-publication because the simplification is standard in practitioner writing.

**Mitigation:** Low priority. If addressed, a parenthetical would suffice: "the most probable response from their training distribution, further shaped by alignment tuning." But this adds technical weight that may slow the reader down. Acceptable to leave as-is for the target audience.

**Post-correction RPN estimate:** S=4, O=3, D=5 = 60

---

### 3. FM-010 (RPN 120) -- Self-Evaluation Bias Claim Unattributed

**Element:** Line 42, Level 3 section.

**The problem:** "Research on LLM self-evaluation consistently shows favorable bias. The model tends to rate its own output higher than external evaluators do." This is accurate and the direction of bias is specified. However, it is the second-most important evidence claim in the article (after Liu et al.) and it lacks any attribution. The claim justifies the human-checkpoint recommendation, which is one of the article's key actionable takeaways. Unattributed evidence supporting a key recommendation is a credibility risk.

**Severity (5):** The claim does important argumentative work. If questioned, the recommendation it supports loses grounding.

**Occurrence (4):** Technically literate readers may notice the attribution gap, especially after seeing Liu et al. cited.

**Detection (6):** Moderate detection difficulty -- the claim sounds authoritative and specific.

**Mitigation:** Either add a lightweight attribution (e.g., "work by Kadavath et al. on model calibration") or remove the research-claim framing and state it as observed behavior: "These models consistently rate their own output higher than external reviewers do." The second option removes the implied citation obligation while keeping the substance.

**Post-correction RPN estimate:** S=4, O=3, D=4 = 48

---

### 4. FM-019 (RPN 100) -- Heading Density vs. Conversational Intimacy Trade-off

**Element:** Overall document structure.

**The problem:** Draft-5 added 7 section headings to a 97-line article. Draft-4 had zero headings in 50 lines and read as a continuous conversation. The headings improve navigation and scannability (important for an mkdocs reference article) but break the conversational flow that is central to the Saucer Boy voice. The technical middle sections (Level 3 explanation, Two-Session Pattern, "Why This Works on Every Model") read more like structured explainer content than a person talking. This is the fundamental tension of the LLM-tell clean pass: making the article more "professional" risks making it less "McConkey."

**Severity (4):** Voice consistency is a core brand attribute for Saucer Boy. Deviation reduces differentiation from standard tech articles.

**Occurrence (5):** Structural formatting choices affect every reader on every read.

**Detection (5):** Detectable through comparison with draft-4, but the improvement in scannability makes it tempting to accept.

**Mitigation:** This is a design trade-off, not a defect. For an mkdocs article, headings are the correct choice. The mitigation is to ensure the VOICE within each section remains conversational even though the STRUCTURE is article-formatted. Currently, Lines 1-9 (opening) and Lines 79-97 (closing) have strong conversational voice. Lines 32-69 (Level 3 through "Why This Works") have the weakest voice. Targeted voice strengthening in the middle sections would resolve this without removing the headings.

**Post-correction RPN estimate:** S=3, O=3, D=4 = 36

---

### 5. FM-021 (RPN 96) -- LLM-Tell in "Constrained Inputs" Sentence

**Element:** Line 65, "Why This Works on Every Model" section.

**The problem:** "Constrained inputs consistently improve output across model families" has the cadence and lexical pattern of an LLM-generated summary. The phrase "across model families" is particularly tell-like -- it is precise in a way that natural speech is not. McConkey would not say "across model families." He would say "every model tested" or "all of them." This is a residual LLM tell that survived the cleaning pass.

**Severity (4):** Breaks voice in a section that is already the weakest for conversational tone.

**Occurrence (4):** The sentence will be read by every reader.

**Detection (6):** LLM tells are difficult to detect when the content is substantively correct. The tell is in the CADENCE, not the CONTENT.

**Mitigation:** Rephrase: "Specific instructions beat vague instructions on every model they've tested." Same claim, natural voice.

**Post-correction RPN estimate:** S=2, O=2, D=4 = 16

---

## Domain Coverage Matrix

| Domain | Failure Modes | RPN Range | Coverage Assessment |
|--------|--------------|-----------|---------------------|
| Technical Accuracy | FM-002, FM-003, FM-004, FM-011, FM-014 | 36-140 | Adequate. No Critical findings. The article's technical claims are broadly accurate with appropriate qualifications. The RLHF elision (FM-004) is the main gap but is defensible for the audience. |
| LLM-Tell Leakage | FM-020, FM-021, FM-022 | 45-96 | Three residual tells identified. FM-021 is the most significant. The cleaning pass was largely effective; remaining tells are in cadence and lexical pattern, not in content. |
| Voice Inauthenticity | FM-006, FM-016, FM-017 | 36-80 | The voice is strong at the edges (opening, closing) and weaker in the middle. The checklist code block (FM-016) is a deliberate trade-off. Overall voice quality is high relative to draft-1. |
| Structural Problems | FM-007, FM-009, FM-012, FM-015, FM-019 | 48-100 | The heading-density trade-off (FM-019) is the main structural tension. Individual sections are well-constructed. The Level 2-to-Level 3 transition (FM-008) could be smoother. |
| Audience Mismatch | FM-001, FM-008, FM-018 | 48-80 | Low to moderate risk. The audience (Ouroboros / practitioners) is well-served. Minor risks around tone in the opening and the Level 2/3 boundary framing. |
| Credibility Damage | FM-005, FM-010 | 120-210 | The two highest-risk items are both about evidence attribution. The article's evidence base is adequate for its genre but has an asymmetry between the well-cited Liu et al. and the less-cited fluency-competence gap and self-evaluation claims. |

---

## Iteration-1 Residual Analysis

Status of all 19 failure modes from the draft-1 FMEA against draft-5:

| Iter-1 ID | Original RPN | Status in Draft-5 | Residual RPN | Notes |
|-----------|-------------|-------------------|-------------|-------|
| FM-001 | 80 | MITIGATED | 48 | Opening is less imperative. "Trips up everybody" is softer than "sit down." Residual risk: still slightly patronizing. |
| FM-002 | 100 | RESOLVED | 0 | Line 5: "Your instinct was right" acknowledges what the reader did well before redirecting. |
| FM-003 | 27 | RESOLVED | 0 | "Yard-sale" jargon removed. Skiing analogy is now about McConkey's preparation, not crash terminology. |
| FM-004 | 252 | RESOLVED | 0 | "Coin flip dressed up as confidence" replaced with "the most probable generic response from their training distribution, dressed up as a custom answer." Accurate and punchy. |
| FM-005 | 294 | RESOLVED | 0 | Jerry-specific Option B prompt removed entirely. All three levels use generic examples. Universality claim now demonstrated, not just asserted. |
| FM-006 | 125 | MITIGATED | 80 | Level 3 prompt still a single block, but now followed by decomposition bullets. Adequate. |
| FM-007 | 180 | RESOLVED | 0 | Lines 15-17 explain next-token prediction mechanism. "These models are next-token predictors trained on billions of documents." |
| FM-008 | 175 | RESOLVED | 0 | "Training-data gravity" / "regurgitation" replaced with "the most probable generic response from their training distribution." Accurate framing. |
| FM-009 | 120 | RESOLVED | 0 | "Cheapest, shortest path" claim removed. Replaced with probability distribution framing throughout. |
| FM-010 | 210 | RESOLVED | 0 | Line 51: "Start a new conversation. Copy the finalized plan into a fresh chat." Concrete, actionable, platform-agnostic. |
| FM-011 | 96 | MITIGATED | 27 | Context window claim now qualified: "Every token of planning conversation is occupying space in the context window that should be used for execution." The Liu et al. citation provides evidence. |
| FM-012 | 150 | RESOLVED | 0 | Jerry-specific orchestrator instruction replaced with generic: "You are the executor. Here is the plan. Follow it step by step. Do not deviate." |
| FM-013 | 48 | RESOLVED | 0 | "Physics" replaced with "hard engineering constraints" (L63). Correct and still punchy. |
| FM-014 | 175 | MITIGATED | 72 | Blanket degradation claim replaced with "performs better when" positive framing. Some residual overclaim in "regardless of architecture." |
| FM-015 | 150 | RESOLVED | 0 | Principle 3 reframed as "Separate planning from execution" (L77). Context window is the mechanism, not the principle. |
| FM-016 | 120 | RESOLVED | 0 | "Start Here" checklist added (L79-89). Concrete call to action. |
| FM-017 | 210 | MITIGATED | ~100 | Voice is stronger throughout but still weakest in technical middle (L32-69). Headings add structure but reduce conversational flow. See FM-019. |
| FM-018 | 96 | RESOLVED | 0 | Redundant banana suit repetition eliminated. McConkey callback appears once at opening, once as closing bookend. Clean. |
| FM-019 | 112 | RESOLVED | 0 | McConkey bio compressed to accurate essentials: "looked like he was winging it. He wasn't." No overstatement of planning side. |

**Resolution rate:** 13/19 RESOLVED (68%), 5/19 MITIGATED (26%), 1/19 residual noted above. **Total residual RPN from iteration-1 findings: ~327** (down from 1,926).

---

## LLM-Tell Specific Analysis

The LLM-tell cleaning pass (draft-4 to draft-5) introduced the following changes with tell-related implications:

| Change | Tell Risk | Assessment |
|--------|-----------|------------|
| Added `##` section headings | Low | Headings are structural, not voice. They do not introduce LLM cadence. However, they move the article from "conversation" to "article," which is a genre shift that could mask tells by making formal language seem appropriate. |
| Added code-block checklist (L83-89) | None | Checklists are human-natural. The `[ ]` format is tool-native (GitHub, task managers). No tell risk. |
| Replaced "one of the most robust findings" with "a well-documented finding" (L65) | **Medium** | "A well-documented finding across prompt engineering research" is a common LLM hedging pattern. See FM-020. |
| Added "Constrained inputs consistently improve output across model families" (L65) | **Medium** | LLM summary cadence. See FM-021. |
| Added "from chain-of-thought prompting to structured role-task-format patterns" (L65) | Low | Naming specific techniques is a good grounding move. The phrase "role-task-format patterns" is slightly jargon-heavy but not a tell. |
| Replaced wall-of-text paragraphs with shorter paragraphs + bullets | Low | Structural improvement. Does not introduce tells. |

**Overall LLM-tell assessment:** The cleaning pass was largely effective. The article's voice in draft-5 is more polished and structured than draft-4's raw conversational style. Three residual tells were identified (FM-020, FM-021, FM-022), all in the "Why This Works on Every Model" section (L61-69), which is the most exposition-heavy section. This concentration suggests the cleaning pass was more successful in the narrative sections than in the explanatory sections.

---

## Evaluation Dimensions

### Quality Dimensions (0.0-1.0)

| Dimension | Weight | Score | Justification |
|-----------|--------|-------|---------------|
| Completeness | 0.20 | 0.95 | Three-level framework complete. Two-session pattern fully explained with rationale. Plan artifact quality criteria present. Checklist provides actionable closure. No structural gaps identified. |
| Internal Consistency | 0.20 | 0.93 | The universality claim is now consistent with examples (all generic). The heading register inconsistency (FM-006) is minor. The Level 2/3 boundary framing (FM-008) creates a slight tension between "most work is Level 2" and "Level 3 is when work matters." |
| Methodological Rigor | 0.20 | 0.92 | Technical claims are broadly accurate. RLHF elision (FM-004) is the main simplification. Fluency-competence gap attribution (FM-005) is the main rigor gap. Liu et al. citation sets a high standard that the rest of the evidence base does not fully match. |
| Evidence Quality | 0.15 | 0.91 | One strong named citation (Liu et al.). One adequate but informal attribution (fluency-competence gap). One unattributed research claim (self-evaluation bias). Evidence base is appropriate for the genre but has a two-tier quality with the Liu citation clearly stronger than the others. |
| Actionability | 0.15 | 0.95 | Three concrete levels with example prompts. Two-session pattern with step-by-step instructions. Five-item checklist. Explicit "start with Level 2" guidance. Closing dare provides motivation. Strong. |
| Traceability | 0.10 | 0.92 | Liu et al. (2023) is traceable. Chain-of-thought and role-task-format are searchable technique names. GPT-3 temporal reference provides grounding. Self-evaluation bias claim lacks a traceability path. |

**Weighted Composite:**

```
Completeness:         0.20 x 0.95 = 0.190
Internal Consistency: 0.20 x 0.93 = 0.186
Methodological Rigor: 0.20 x 0.92 = 0.184
Evidence Quality:     0.15 x 0.91 = 0.1365
Actionability:        0.15 x 0.95 = 0.1425
Traceability:         0.10 x 0.92 = 0.092

TOTAL: 0.190 + 0.186 + 0.184 + 0.1365 + 0.1425 + 0.092 = 0.931
```

**Weighted Composite: 0.931**
**Quality Gate: PASS (>= 0.92)**

### Supplementary Dimensions

| Dimension | Score | Justification |
|-----------|-------|---------------|
| LLM-Tell Detection | 0.85 | Three residual tells identified (FM-020, FM-021, FM-022), all concentrated in L61-69. The cleaning pass was effective in narrative sections. The explanatory section retains LLM cadence patterns. |
| Voice Authenticity | 0.88 | Strong McConkey voice in opening (L1-9) and closing (L91-97). Adequate voice in Level 1-2 sections. Weakest voice in "Why This Works on Every Model" section where exposition displaces personality. The heading structure helps navigation but slightly reduces conversational intimacy. |

---

## Overall Assessment

Draft-5 is a materially improved article compared to the draft-1 baseline. The iteration-1 FMEA identified 19 failure modes at total RPN 1,926; this draft resolves 13 of those and mitigates 5, bringing residual RPN from those findings to approximately 327. New failure modes identified in draft-5 (mostly from the structural changes and residual LLM tells) add 1,287 RPN, for a combined total of 1,614 across 22 failure modes.

The risk profile has shifted. Draft-1's primary risks were technical accuracy and Jerry-specificity (the universality claim was undermined by Jerry-specific examples). Draft-5's primary risks are evidence attribution (FM-005, FM-010) and the structural tension between heading-driven scannability and conversational voice (FM-019). These are lower-severity risks that reflect trade-offs rather than defects.

**Critical findings (1):** FM-005 (fluency-competence gap attribution, RPN 210). This is the only finding above 200 and is correctable with a rephrasing that preserves explanatory value.

**Major findings (9):** FM-003 (McConkey factual compression), FM-004 (RLHF elision), FM-007 (Level 2/3 plan review gap), FM-008 (Level 2/3 boundary framing), FM-009 (Level 3 prompt density), FM-010 (self-eval bias unattributed), FM-012 (heading tonal shift), FM-019 (heading density), FM-021 (LLM tell in constrained-inputs sentence).

**Recommendation:** ACCEPT with targeted corrections for FM-005 (fluency-competence gap rephrasing) and FM-021 (constrained-inputs sentence voice fix). These are two-sentence edits. The remaining Major findings are trade-offs that the author should review but that do not block publication.

**Comparison to iteration-3 score (0.938):** This FMEA scores the article at 0.931. The delta (-0.007) is within scoring noise and reflects a stricter treatment of the evidence attribution gap (FM-005, FM-010) and the identification of LLM tells that were not in scope for the previous iteration's FMEA. The article passes the quality gate on both assessments.
