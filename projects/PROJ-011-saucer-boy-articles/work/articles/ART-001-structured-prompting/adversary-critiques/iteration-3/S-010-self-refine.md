---

## S-010 SELF-REFINE: Adversarial Review (Iteration 3)

**STRATEGY:** S-010 Self-Refine
**DELIVERABLE:** `drafts/draft-7-iteration-3.md`
**REVIEWER:** adv-executor (S-010)
**DATE:** 2026-02-23
**ITERATION:** 3 of 3 minimum (H-14)
**CONTEXT:** Draft 7 (iteration 3) is the revision of draft 6 (reviewed in iteration 2). The iteration 2 S-010 review scored draft 6 at 0.937 (PASS at 0.92 threshold, REVISE at the 0.95 aspirational target) with LLM-Tell 0.85 and Voice Authenticity 0.87. The S-014 iteration 3 scorer gave its target deliverable 0.938 (PASS). This review evaluates draft 7 against the specific open findings from iteration 2 and assesses the current state independently.

---

### STEP 1: SHIFT PERSPECTIVE

**Objectivity check:** Low attachment. External adversarial review of another agent's revision work. No creator bias. Third iteration provides full historical visibility across all prior findings. Proceeding with standard scrutiny and active anti-leniency on residual issues.

---

### STEP 2: SYSTEMATIC SELF-CRITIQUE

#### Assessment of Iteration 2 Open Findings

The iteration 2 S-010 review identified 1 Major and 4 Minor open findings. I now verify each against draft 7.

**SR-001-iter2 (MAJOR): Ungrounded "80%" claim -- FIXED.**

Draft 6 line 23 read: "Most people can get 80% of the benefit with a prompt that's just two or three sentences more specific."

Draft 7 line 23 now reads: "In my experience, most people get the bulk of the benefit with a prompt that's just two or three sentences more specific."

This applies the iteration 2 recommendation (option 3: drop the number, frame as experiential). "In my experience" is an honest epistemic marker -- it positions the claim as practitioner observation rather than measured quantity. "The bulk of the benefit" replaces the fake-precise "80%" with an appropriately vague approximation. The article criticizes LLMs for generating confident-sounding ungrounded claims; the revised phrasing no longer commits the same error. This is a clean, minimal fix that resolves the most ironic gap in the draft.

**SR-002-iter2 (MINOR): Generic title -- NOT FIXED.**

Draft 7 line 1: "# Why Structured Prompting Works" -- identical to draft 6. The title remains generic and undistinctive. However, as noted in the iteration 2 review, this was downgraded from the original iteration 1-v2 HIGH severity to Minor because: (a) the S-014 scorer has not penalized it, (b) the title is functional and accurate, (c) title selection is an author-discretion choice. Retaining as Minor, author discretion.

**SR-003-iter2 (MINOR): Consecutive "That's why" at line 45 -- FIXED.**

Draft 6 line 45 read: "That's why the human checkpoints matter. That's why reviewing the plan matters."

Draft 7 line 45 reads: "The human checkpoints catch this. Reviewing the plan catches it earlier."

This completely eliminates the anaphoric "That's why" pair. The replacement uses a parallel "catches" construction but it is a different syntactic pattern (declarative statements rather than "That's why" openers) and the second sentence adds semantic differentiation ("catches it earlier") rather than mere repetition. The LLM-tell pattern is gone while preserving the rhetorical emphasis on both checkpoints and plan review. Clean fix.

**SR-006-iter2 (MINOR): Plan artifact criteria thin -- FIXED.**

Draft 6 line 61: "If the plan can't stand alone, it wasn't detailed enough. Which is exactly why the review step matters."

Draft 7 line 61: "You do lose the back-and-forth nuance. That's real. The plan artifact has to carry the full context on its own. Phases, what 'done' looks like for each phase, output format. If the plan can't stand alone, it wasn't detailed enough. Which is exactly why the review step matters."

The new text adds three concrete criteria for plan artifact quality: (1) phases, (2) what "done" looks like for each phase, (3) output format. This directly addresses the iteration 2 S-010 recommendation ("Add one concrete criterion for plan artifact quality criteria after line 61") and actually exceeds it with three criteria plus a completeness test. The S-014 iteration 3 scorer also noted this fix at their line 71 and scored Completeness at 0.95 on the strength of it.

**SR-007-iter2 (MINOR): "Past few years" vague for context windows -- FIXED.**

Draft 6 line 65 had vague temporal framing for context window growth.

Draft 7 lines 65 now reads: "They've grown fast: GPT-3 shipped with 2K tokens in 2020, and Gemini 1.5 crossed a million in 2024."

This replaces the vague "past few years" with specific data points: GPT-3 (2K, 2020) and Gemini 1.5 (1M+, 2024). Both figures are verified in the citations companion: GPT-3 was 2,048 tokens, Gemini 1.5 crossed 1M tokens. The 4-year span with a 500x growth factor is now concrete and verifiable. Clean fix.

#### New Issues in Draft 7

I now examine the draft independently for new issues introduced by the revisions or previously undetected weaknesses.

**NEW ISSUE A: The opening paragraph's second sentence is long and dense.**

Line 3: "What I'm about to walk you through applies to every LLM on the market. Claude, GPT, Gemini, Llama, whatever ships next Tuesday."

This is fine individually, but when combined with "This isn't a Jerry thing. It's a 'how these models actually work under the hood' thing," the paragraph has five short sentences in rapid succession. The rhythm is punchy and conversational, which matches the voice. Not a defect -- flagging only for completeness.

**NEW ISSUE B: "Post-training techniques like RLHF" -- precision check.**

Line 17: "Post-training techniques like RLHF shape that behavior, but when your instructions leave room for interpretation, the prediction mechanism fills the gaps with whatever pattern showed up most often in the training data."

This is technically accurate. RLHF is a post-training technique. The sentence correctly distinguishes between the base next-token prediction mechanism and post-training behavioral shaping. The clause "when your instructions leave room for interpretation, the prediction mechanism fills the gaps" is an appropriate simplification for the target audience. No issue.

**NEW ISSUE C: Liu et al. citation now integrated more smoothly.**

Line 57: "Liu et al. (2023) found that models pay the most attention to what's at the beginning and end of a long context, and significantly less to everything in the middle. They studied retrieval tasks, but the attentional pattern applies broadly: your carefully crafted instructions from message three are competing with forty messages of planning debate, and the model isn't weighing them evenly."

This is excellent. The citation includes author, year, specific finding, and an honest scope qualifier ("They studied retrieval tasks, but the attentional pattern applies broadly"). The application to the prompting context is explicit and concrete ("message three...forty messages"). One note: "applies broadly" is an extrapolation beyond the paper's stated findings (which were specific to multi-document QA and key-value retrieval). However, the article acknowledges the original scope and the extrapolation is reasonable and widely accepted in the practitioner community. This is the kind of honest hedging the article advocates. Not a defect.

**NEW ISSUE D: The "Further reading" block at the end.**

Lines 100-102: "**Further reading:** The claims in this article are grounded in published research. For full references with links, see the companion [citations document](citations.md). Start with Liu et al. (2023) on the lost-in-the-middle effect, Wei et al. (2022) on chain-of-thought prompting, and Panickssery et al. (2024) on LLM self-preference bias."

This is a strong addition. It provides: (a) an explicit reference to the citations companion, (b) a reading order recommendation for three key papers, (c) specific topic anchors for each paper. This closes the traceability loop between the voice-first article and the full-citation companion. The three recommended papers are the same ones listed in the citations companion's "Reading Order for Ouroboros" section. Consistent.

**NEW ISSUE E: "Not what's actually true about *your* repo" -- emphasis pattern.**

Line 17: Uses *your* with emphasis. This appears once. Appropriate rhetorical emphasis for the key distinction (generic patterns vs. your specific situation). Not overused.

**NEW ISSUE F: McConkey introduction accuracy check.**

Line 7: "Shane McConkey, if you don't know him, was a legendary freeskier who'd show up to competitions in costume and still take the whole thing seriously enough to win."

Checking: McConkey was indeed known for competing in costumes (notably a banana suit, speed suit in backward skiing). He did win competitions. The characterization "legendary freeskier" is accurate -- he won multiple World Extreme Skiing Championships. The phrasing has been slightly adjusted from the iteration 2 draft's "literally competed in a banana suit and won" to a more general "show up to competitions in costume." Both are factually grounded. The new version is slightly less specific but avoids the word "literally" which could read as an LLM tell. Acceptable.

**NEW ISSUE G: Error propagation paragraph -- check for accuracy.**

Lines 44-45: "Once bad output enters a multi-phase pipeline, it doesn't just persist. It compounds. This is a well-established pattern in pipeline design, and it hits LLM workflows especially hard. Each downstream phase takes the previous output at face value and adds another layer of polished-sounding analysis on top. By phase three, the whole thing looks authoritative. The errors are structural. It's not garbage in, garbage out. It's garbage in, increasingly polished garbage out, and it gets much harder to tell the difference the deeper into the pipeline you go."

The citations companion Section 6 confirms error propagation as a well-established principle, grounded in Arize AI (2024) for the LLM-specific case. The paragraph does not name a source but the claim is characterized as "a well-established pattern in pipeline design" which is an accurate consensus description. The "garbage in, increasingly polished garbage out" reframing is original and vivid. No accuracy issue.

**NEW ISSUE H: Sentence counting "That's" usage in draft 7.**

Full scan of "That's" as sentence opener or rhetorical emphasis:
- Line 17: "That's the dangerous part." -- retained from draft 6.
- No other instances of "That's" as sentence opener.

Down from 3 uses in draft 6 to 1 in draft 7. The "That's why" pair has been eliminated. Single remaining use is natural and unremarkable. Significant improvement.

---

### STEP 3: DOCUMENT FINDINGS

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| SR-001-iter3 | Generic title unchanged | Minor | Line 1: "# Why Structured Prompting Works" -- functional but undistinctive. Carried forward from SR-002-iter2 as author-discretion item. | Completeness |
| SR-002-iter3 | Liu et al. scope extrapolation is acknowledged but imprecise | Minor | Line 57: "They studied retrieval tasks, but the attentional pattern applies broadly." The word "broadly" is a hedge but the claim that retrieval-task findings apply to instruction-following is a reasonable but unstated inferential step. The article models good citation practice here (stating the original scope before extrapolating), which partially mitigates the issue. | Methodological Rigor |
| SR-003-iter3 | "In my experience" is a single-person epistemic anchor | Minor | Line 23: "In my experience, most people get the bulk of the benefit..." -- This is a legitimate hedge and was the recommended fix from iteration 2. However, it is one person's experience presented as generalizable. In the target genre (practitioner explainer), this is standard practice. Not a defect, flagging for completeness. | Evidence Quality |
| SR-004-iter3 | "Why This Works on Every Model" section remains the weakest voice section | Minor | Lines 63-67: This section reads as competent technical exposition rather than someone talking to you. "Context windows are engineering constraints, the kind of hard limits determined by architecture and compute" is precise but flat. The section fulfills its structural role (universality claim) and the voice gap is minor. | Voice (non-scoring) |
| SR-005-iter3 | 80% claim resolved -- "In my experience" + "bulk of the benefit" | Resolved | Line 23: Replaces ungrounded "80%" with experiential framing. Addresses SR-001-iter2 (Major). | Evidence Quality (Positive), Internal Consistency (Positive), Methodological Rigor (Positive) |
| SR-006-iter3 | Consecutive "That's why" resolved | Resolved | Line 45: Replaced with "The human checkpoints catch this. Reviewing the plan catches it earlier." Addresses SR-003-iter2. | Internal Consistency (Positive) |
| SR-007-iter3 | Plan artifact quality criteria added | Resolved | Line 61: "Phases, what 'done' looks like for each phase, output format." Addresses SR-006-iter2. | Completeness (Positive), Actionability (Positive) |
| SR-008-iter3 | Context window growth now concrete | Resolved | Line 65: "GPT-3 shipped with 2K tokens in 2020, and Gemini 1.5 crossed a million in 2024." Addresses SR-007-iter2. | Evidence Quality (Positive) |
| SR-009-iter3 | Further reading block added | Resolved | Lines 100-102: Links to citations companion with three recommended starting papers. | Traceability (Positive) |

---

### STEP 4: REVISION RECOMMENDATIONS

**Priority 1 (no items): No Critical or Major findings remain.** All open findings are Minor and within acceptable tolerances for the genre.

**Priority 2 (optional polish, author discretion):**

1. **Title revision (SR-001-iter3).** A more distinctive title would improve discoverability. The current title is accurate but generic. Options from prior iterations remain valid: "Three Levels of Prompting (And Why Level 1 Burns You)" or "What Shane McConkey Can Teach You About Prompting" or "The Fluency-Competence Gap: Why Your LLM Sounds Smarter Than It Is." None of these are required. The current title does not reduce quality below threshold.

2. **Minor voice lift in "Why This Works on Every Model" section (SR-004-iter3).** The opening sentence could be warmed slightly. Example: "Context windows are hard caps. Architecture and compute set them, and you work inside whatever ceiling you get." This adds a slightly more conversational rhythm while preserving technical accuracy. Not required.

3. **No action needed on SR-002-iter3 or SR-003-iter3.** The Liu et al. scope acknowledgment is honest citation practice. The "in my experience" hedge is genre-appropriate.

---

### STEP 5: REVISE AND VERIFY

This is a review-only pass (adv-executor does not modify the deliverable). All Priority 1 items are empty. The draft requires no mandatory revisions.

**Verification of iteration 2 fixes:**

| Iteration 2 Finding | Fix Applied | Verified |
|---------------------|-------------|----------|
| SR-001-iter2 (80% ungrounded) | "In my experience...bulk of the benefit" | Yes -- no ungrounded numeric claims remain |
| SR-002-iter2 (generic title) | Not fixed (author discretion) | N/A -- Minor, optional |
| SR-003-iter2 (consecutive "That's why") | Replaced with varied construction | Yes -- only 1 "That's" instance remains |
| SR-006-iter2 (plan criteria thin) | Three concrete criteria added | Yes -- phases, done-criteria, output format |
| SR-007-iter2 (vague context window timeline) | Specific GPT-3 and Gemini 1.5 data points | Yes -- verified against citations companion |

**All Major findings from all iterations: Resolved.**
**All Minor findings from iteration 2: 4 of 5 resolved (title remains as author discretion).**

---

### STEP 6: DECISION

**Outcome:** PASS

**Quality Gate:** PASS (see scoring below). All Major and Critical findings across three iterations have been resolved. The four remaining Minor findings are within acceptable tolerances for the genre and do not individually or collectively depress any dimension below threshold.

---

### LLM-TELL DETECTION

Sentence-by-sentence scan of draft 7 for: em-dashes (--), double-dashes, hedging phrases, parallel structure excess, formulaic transitions, excessive bolding, "delve/tapestry/landscape/robust/nuanced" vocabulary, "That's not X. It's Y." patterns, list-ification of conversational prose.

**TELL 1 -- LOW: Single "That's the dangerous part." (line 17)**

> "The output comes back with clean structure, professional headings, and authoritative language. Reads like an expert wrote it. [...] Except the expert part is a mirage."

One instance of "That's" as a sentence opener. Down from 3 in draft 6 and 5 in draft 5. A single occurrence is natural conversational English and undetectable as an LLM pattern. Flagging only for continuity with prior scans.

**TELL 2 -- LOW: Compressed comma-list sentence (line 17)**

> "The output comes back with clean structure, professional headings, and authoritative language."

Three-item comma list. This replaced the problematic triplet from draft 5 and has been acceptable since draft 6. The sentence flows into a sentence fragment ("Reads like an expert wrote it.") which breaks the rhythm immediately. Within normal prose range.

**TELL 3 -- LOW: "It's not garbage in, garbage out. It's garbage in, increasingly polished garbage out" (line 45)**

> "It's not X. It's Y." negate-then-assert pattern. However, this is doing real semantic work -- the entire point is to contrast the familiar GIGO principle with the specific LLM-pipeline phenomenon. The subversion of the expected phrase is a deliberate rhetorical move, not a template fill. Additionally, the "increasingly polished garbage out" phrase is vivid and original enough to override the pattern concern. Flagging for completeness but this reads as authorial rather than generated.

**TELL 4 -- LOW: "Not out of laziness. Out of probability distributions." is gone.**

The "Not X. Out of Y." two-sentence correction from draft 6 line 71 has been replaced. Draft 7 line 71: "Every dimension you leave open, the model fills with its default, driven by probability distributions rather than any understanding of what you actually need." This integrates the correction into a single flowing sentence rather than using the staccato negate-then-assert pattern. The LLM tell identified in iteration 2 (Tell 3) has been eliminated.

**No instances found of:** "delve," "tapestry," "landscape," "robust," "nuanced," "it's important to note," "in conclusion," excessive bolding, formulaic transitions between sections, or em-dashes used as rhetorical crutches.

**LLM-Tell Score: 0.90**

Continued improvement from draft 6 (0.85) and draft 5 (0.72). The remaining tells are all LOW severity and individually unremarkable. The GIGO subversion (Tell 3) is arguably a voice strength rather than a tell. The "That's the dangerous part" instance is a single natural conversational construction. A tell-detection reviewer would struggle to identify this article as AI-generated based on stylistic markers alone. The strongest remaining signal would be the article's overall polish and structure, which is inherent to a well-edited piece and not actionable as a tell.

---

### VOICE AUTHENTICITY

**Overall: Strong, consistent voice with successful resolution of all prior regressions and tell patterns.**

Draft 7 maintains the voice improvements from draft 6 and adds additional refinement:

**McConkey introduction (line 7):** "Shane McConkey, if you don't know him, was a legendary freeskier who'd show up to competitions in costume and still take the whole thing seriously enough to win. The guy looked completely unhinged on the mountain. He wasn't." The parenthetical aside ("if you don't know him"), the concrete detail ("in costume"), and the two-sentence characterization ("completely unhinged...He wasn't") establish the voice immediately. This is someone who knows their subject and enjoys explaining it.

**Level 1 heading (line 11):** "Point Downhill and Hope" remains one of the strongest voice moments. Evocative, concise, and specific.

**The fluency-competence gap (line 19):** "I call it the fluency-competence gap." The first-person ownership ("I call it") is a significant voice marker. It positions the author as someone who names patterns from experience, not as someone reporting consensus terminology. This is the single most important voice fix across all three iterations.

**Error propagation paragraph (lines 44-45):** "It's not garbage in, garbage out. It's garbage in, increasingly polished garbage out, and it gets much harder to tell the difference the deeper into the pipeline you go. The human checkpoints catch this. Reviewing the plan catches it earlier." The GIGO subversion is the article's strongest single rhetorical moment. The follow-up ("catches this...catches it earlier") has a satisfying escalation structure that avoided the "That's why" repetition of draft 6.

**Two-Session Pattern (line 53):** "Then you do something counterintuitive: start a brand new conversation." The word "counterintuitive" directly addresses what the reader is likely thinking. The colon followed by the instruction is a natural conversational beat.

**Liu et al. integration (line 57):** "Liu et al. (2023) found that models pay the most attention to what's at the beginning and end of a long context, and significantly less to everything in the middle. They studied retrieval tasks, but the attentional pattern applies broadly: your carefully crafted instructions from message three are competing with forty messages of planning debate, and the model isn't weighing them evenly." This is the gold standard for integrating a citation into a voice-first piece. The formal citation is embedded naturally, the scope qualifier is honest ("They studied retrieval tasks, but"), and the application to the reader's situation is vivid and specific ("message three...forty messages").

**Plan artifact criteria (line 61):** "Phases, what 'done' looks like for each phase, output format. If the plan can't stand alone, it wasn't detailed enough." The fragment-list followed by a completeness test reads naturally. The criteria are concrete without being pedantic.

**Closing (lines 96-98):** "McConkey looked like he was winging it. He wasn't. The preparation was everything underneath it. [...] Next time you open an LLM, before you type anything, write down three things: what you need, how you'll know if it's good, and what you want to see first. Do that once and tell me it didn't change the output." The McConkey callback lands because it inverts the opening's detail level (opening was specific, closing is principle-level). The imperative closing with the challenge ("tell me it didn't change the output") has the right amount of confidence.

**Remaining voice weakness:**

The "Why This Works on Every Model" section (lines 63-67) remains the weakest voice section. "Context windows are engineering constraints, the kind of hard limits determined by architecture and compute" is competent technical prose but lacks the warmth of the surrounding sections. "That finding holds across models, tasks, and research groups" is a three-part list in a formal register. This is the one section that could be warmed further. However, it serves a structural role (universality claim, bridging specific techniques to general principles) and the slightly more formal register may be appropriate for that purpose.

The "Three Principles" section (lines 69-75) has improved significantly across iterations. The rhetorical questions in Principle 2 and the "step 1: do it, step 2: we're done" self-deprecating example carry voice. The section remains the most condensed/summary-like part of the article, which is inherent to its purpose.

**Voice Authenticity Score: 0.90**

Improvement from draft 6 (0.87), driven by: (a) elimination of the "That's why" anaphoric pair, (b) the "Not X. Out of Y." tell pattern replaced with flowing prose, (c) "In my experience" framing adds personal voice to the Level 2 introduction, (d) "The human checkpoints catch this. Reviewing the plan catches it earlier" is rhythmically satisfying and sounds like someone making a point rather than filling a template. The article reads as a knowledgeable practitioner sharing hard-won insights, which is the target voice.

---

### TECHNICAL ACCURACY

Full verification of all claims against the citations companion:

**Bender and Koller (2020):** Line 19 -- "Bender and Koller showed back in 2020 that models learn to sound like they understand without actually understanding." Citations companion Section 1 confirms: "Models trained on linguistic form alone don't acquire genuine understanding." Accurate characterization. The casual phrasing ("showed back in 2020") is genre-appropriate.

**Sharma et al. (2024):** Line 19 -- "Sharma et al. found in 2024 that RLHF, the technique used to make models helpful, actually makes this worse by rewarding confident-sounding responses over accurate ones." Citations companion Section 1 confirms: "RLHF-trained models systematically produce authoritative-sounding responses regardless of factual accuracy." Accurate. The phrase "rewarding confident-sounding responses over accurate ones" is a fair simplification of the RLHF preference-data bias mechanism described in Chen et al. (2024).

**Wei et al. (2022):** Line 27 -- "Wei et al. (2022) demonstrated this with chain-of-thought prompting: just adding intermediate reasoning steps to a prompt measurably improved performance on arithmetic, commonsense, and symbolic reasoning tasks." Citations companion Section 3 confirms: "Providing intermediate reasoning steps in prompts improves performance on arithmetic, commonsense, and symbolic reasoning tasks." Accurate.

**Panickssery et al. (2024):** Line 42 -- "Panickssery et al. (2024) showed that LLMs recognize and favor their own output, consistently rating it higher than external evaluators do." Citations companion Section 4 confirms: "LLMs have non-trivial accuracy at distinguishing their own outputs from others', and there is a linear correlation between self-recognition capability and the strength of self-preference bias." Accurate characterization.

**Liu et al. (2023):** Line 57 -- "Liu et al. (2023) found that models pay the most attention to what's at the beginning and end of a long context, and significantly less to everything in the middle." Citations companion Section 2 confirms: "Performance on multi-document QA and key-value retrieval is highest when relevant information appears at the beginning or end of the input context, and significantly degrades when it appears in the middle." Accurate. The article uses 2023 (arXiv preprint date); the citations companion notes TACL publication was 2024. Using the preprint year is standard convention.

**GPT-3 context window (line 65):** "GPT-3 shipped with 2K tokens in 2020" -- Citations companion Section 7 confirms 2,048 tokens. Accurate.

**Gemini 1.5 context window (line 65):** "Gemini 1.5 crossed a million in 2024" -- Citations companion Section 7 confirms 1,000,000+ tokens. Accurate.

**Next-token prediction (line 17):** "At their core, these models predict the next token based on everything before it." Grounded in Vaswani et al. (2017) and Brown et al. (2020) per citations companion Section 5. Accurate.

**RLHF characterization (line 17):** "Post-training techniques like RLHF shape that behavior." Accurate -- RLHF is a post-training alignment technique. The distinction between base model behavior and post-training shaping is correctly drawn.

**Error propagation (line 44):** "Once bad output enters a multi-phase pipeline, it doesn't just persist. It compounds." Grounded in systems engineering principle and Arize AI (2024) per citations companion Section 6. Accurate.

**All citations verified. No factual errors found. No mischaracterizations detected.**

**Technical Accuracy Score: 0.95**

Slight improvement from draft 6 (0.94). The 80% claim was the sole ungrounded numeric assertion in draft 6; its removal eliminates the last accuracy concern. All five named citations are accurate. The RLHF characterization and Liu et al. scope qualifier are appropriately precise.

---

### EVALUATION DIMENSIONS

| Dimension | Weight | Score | Justification |
|-----------|--------|-------|---------------|
| Completeness | 0.20 | 0.96 | Three-level framework complete. Two-session pattern with concrete plan artifact criteria (phases, done-criteria, output format). McConkey intro and callback. Five-item checklist with graduated on-ramp. Five inline citations plus further-reading block linking to citations companion. Further-reading block recommends three starting papers. Residual: generic title (Minor, author discretion). |
| Internal Consistency | 0.20 | 0.96 | No ungrounded claims remain -- the 80% fix eliminates the practice-what-you-preach gap. "I call it the fluency-competence gap" correctly positions the term as author-coined. Executor prompt ("Flag deviations rather than freelancing") models the checkpoint-compatible approach the article advocates. Metaphor consistency maintained throughout (preparation-vs-performance). All principles in the recap section are grounded in specific earlier sections. No contradictions detected. |
| Methodological Rigor | 0.20 | 0.95 | Mechanism explanations present: next-token prediction, output distribution narrowing (line 27), positional attention bias (line 57), self-preference bias (line 42), error propagation (line 44). Scoped advice by complexity level with explicit on-ramp. Self-evaluation bias grounded with Panickssery citation. "In my experience" appropriately hedges the Level 2 benefit claim. Liu et al. scope qualifier ("They studied retrieval tasks, but") models honest citation practice. All claims either cited or honestly hedged. |
| Evidence Quality | 0.15 | 0.94 | Five named inline citations: Bender & Koller (2020), Sharma et al. (2024), Wei et al. (2022), Panickssery et al. (2024), Liu et al. (2023). All verified against citations companion. Context window figures (GPT-3 2K, Gemini 1.5 1M+) verified. Further-reading block provides traceability to full reference list. No ungrounded numeric claims remain. "In my experience" is an honest epistemic marker, not a pseudo-citation. Minor residual: the self-evaluation bias discussion does not name Panickssery in-text when first introducing the concept (line 42 does name Panickssery -- correction: it does. All key claims are attributed). |
| Actionability | 0.15 | 0.96 | Three prompt examples at increasing complexity with clear delineation. Executor prompt models checkpoint practice. Five-item checklist with graduated usage (Level 2 baseline, Level 3 add-on). Plan artifact quality criteria are concrete (three items plus completeness test). "Start with Level 2. Work up to Level 3 when the stakes justify it" provides explicit on-ramp. Closing challenge ("write down three things...Do that once and tell me it didn't change the output") gives the reader an immediate next action. |
| Traceability | 0.10 | 0.95 | Five citations include author, year, and specific finding description. "I call it" attribution for coined term. Three principles clearly labeled and numbered. Further-reading block links to citations companion with reading order. "Lost in the middle" attributed to Liu et al. Error propagation characterized as "well-established pattern in pipeline design." Context window growth uses named model families with years. Residual: no formal reference list (by design -- citations companion serves this role and is linked). |

**Weighted Composite:**

```
Completeness:         0.20 x 0.96 = 0.192
Internal Consistency: 0.20 x 0.96 = 0.192
Methodological Rigor: 0.20 x 0.95 = 0.190
Evidence Quality:     0.15 x 0.94 = 0.141
Actionability:        0.15 x 0.96 = 0.144
Traceability:         0.10 x 0.95 = 0.095
                                     -----
TOTAL:                               0.954
```

**Weighted Composite: 0.954**

---

### SCORING SUMMARY

| Metric | Iteration 2 (Draft 6) | Iteration 3 (Draft 7) | Delta |
|--------|------------------------|------------------------|-------|
| Composite | 0.937 | 0.954 | +0.017 |
| LLM-Tell | 0.85 | 0.90 | +0.05 |
| Voice Authenticity | 0.87 | 0.90 | +0.03 |
| Technical Accuracy | 0.94 | 0.95 | +0.01 |

**Dimension Movement:**

| Dimension | Iter 2 | Iter 3 | Delta | Driver |
|-----------|--------|--------|-------|--------|
| Completeness | 0.94 | 0.96 | +0.02 | Plan artifact criteria added; further-reading block |
| Internal Consistency | 0.94 | 0.96 | +0.02 | 80% claim fixed; "That's why" repetition eliminated |
| Methodological Rigor | 0.93 | 0.95 | +0.02 | 80% claim hedged; all overclaims now resolved |
| Evidence Quality | 0.92 | 0.94 | +0.02 | 80% no longer ungrounded; context window figures concrete |
| Actionability | 0.95 | 0.96 | +0.01 | Plan artifact criteria make two-session pattern more actionable |
| Traceability | 0.94 | 0.95 | +0.01 | Further-reading block links to citations companion |

---

### COMPARISON TO S-014 ITERATION 3 SCORER

The S-014 iteration 3 scorer evaluated a different deliverable name ("saucer-boy-ouroboros-draft-2.md") and scored it at 0.938. My S-010 score for draft-7-iteration-3.md is 0.954 -- a delta of +0.016.

The delta is explained by:

1. **The S-014 scorer appears to have evaluated a different or earlier version of the draft.** The S-014 references "line 79" for the "well-documented finding" language and "line 50" for self-evaluation bias -- these line numbers do not match draft-7-iteration-3.md. My review evaluates the actual current deliverable at the specified path.

2. **The 80% claim fix.** The S-014 scorer's deliverable may not have included the "In my experience...bulk of the benefit" fix. Draft 7 has this fix, which was the single highest-leverage remaining item from iteration 2 and the one fix predicted to push the composite above 0.95.

3. **The "That's why" pair elimination.** Draft 7 replaced the consecutive "That's why" construction with varied syntax. If the S-014 scorer evaluated a version without this fix, Internal Consistency would score lower.

**Leniency bias check:** Am I scoring too generously? I systematically reviewed each dimension against the rubric criteria:

- **Completeness 0.96:** All structural elements present. Plan criteria gap from iteration 2 closed. Further-reading block added. Only residual is the generic title (Minor, author discretion). 0.96 is justified -- the 0.95+ band requires "all sections reviewed, minimum 3 findings identified even if deliverable is strong." I identified 4 Minor findings.
- **Internal Consistency 0.96:** No contradictions detected. The 80% practice-what-you-preach gap is closed. Executor prompt models the article's advice. 0.96 is justified -- the only potential concern was the "That's why" pair, which is now fixed.
- **Methodological Rigor 0.95:** All claims either cited or honestly hedged. Five mechanism explanations. Scoped advice. Liu et al. scope qualifier models good practice. The "In my experience" hedge is appropriate. 0.95 is justified.
- **Evidence Quality 0.94:** Five named citations verified. No ungrounded claims. "In my experience" is an honest hedge rather than a citation, which is appropriate but less rigorous than a named source. 0.94 (not 0.95) reflects this subtle distinction.
- **Actionability 0.96:** Three prompt examples, five-item checklist, plan criteria, graduated on-ramp, closing action challenge. 0.96 is justified.
- **Traceability 0.95:** Five author/year/finding citations. Further-reading block. Coined-term attribution. 0.95 is justified.

I am satisfied that these scores reflect the deliverable's actual quality rather than leniency. The 0.954 composite is defensible.

---

### DECISION

**Outcome:** PASS (0.954 >= 0.95 aspirational threshold)

**Quality Gate:** PASS at both the 0.92 standard threshold and the 0.95 aspirational target.

**Rationale:** Draft 7 resolves all Major findings from all three iterations. The single Major finding from iteration 2 (ungrounded 80% claim) is fixed with an honest experiential hedge. All four addressable Minor findings from iteration 2 are resolved. One Minor (generic title) remains as author discretion. LLM-Tell score has improved from 0.72 (draft 5) to 0.90 (draft 7). Voice Authenticity has improved from 0.78 to 0.90. Technical accuracy is 0.95 with all citations verified. The composite score of 0.954 exceeds the 0.95 aspirational target with margin.

**Iteration count:** 3 of 3 (H-14 minimum met). This is the final required iteration.

**Remaining polish opportunities (not required for acceptance):**

1. Title revision -- author discretion, no quality gate impact.
2. Minor voice lift in "Why This Works on Every Model" section -- optional warmth improvement.

**Next Action:** The deliverable passes the quality gate at 0.954. No further revision required. The article is ready for delivery.

---

### FINDINGS TABLE (CONSOLIDATED ACROSS ALL ITERATIONS)

| ID | Finding | Severity | Status | Source Iteration | Evidence |
|----|---------|----------|--------|-----------------|----------|
| SR-001-iter1 | Formulaic three-part sentence structure | HIGH | FIXED (iter 2) | 1 | Triplet collapsed |
| SR-002-iter1 | Negate-then-assert pattern | MEDIUM | FIXED (iter 2) | 1 | Restructured |
| SR-003-iter1 | Parallel bullet structure | MEDIUM | FIXED (iter 2) | 1 | Varied rhythms |
| SR-004-iter1 | Repeated "every dimension" phrasing | LOW | FIXED (iter 2) | 1 | Differentiated |
| SR-005-iter1 | "That's" overuse | LOW | FIXED (iter 3) | 1 | Down to 1 instance |
| SR-001-iter2 | Ungrounded "80%" claim | Major | FIXED (iter 3) | 2 | "In my experience...bulk of the benefit" |
| SR-002-iter2 | Generic title | Minor | OPEN (author discretion) | 2 | Line 1 unchanged |
| SR-003-iter2 | Consecutive "That's why" | Minor | FIXED (iter 3) | 2 | Replaced with varied syntax |
| SR-006-iter2 | Plan artifact criteria thin | Minor | FIXED (iter 3) | 2 | Three criteria added |
| SR-007-iter2 | Vague context window timeline | Minor | FIXED (iter 3) | 2 | Specific GPT-3/Gemini data |
| SR-001-iter3 | Generic title | Minor | OPEN (author discretion) | 3 | Carried from SR-002-iter2 |
| SR-002-iter3 | Liu et al. scope extrapolation | Minor | OPEN (acceptable) | 3 | Scope acknowledged in text |
| SR-003-iter3 | "In my experience" single-person anchor | Minor | OPEN (genre-appropriate) | 3 | Standard practitioner convention |
| SR-004-iter3 | "Why This Works" section weakest voice | Minor | OPEN (structural role) | 3 | Voice gap minor |

**Open findings:** 4 Minor (all within acceptable tolerances)
**Resolved findings across all iterations:** 10 (including 1 Major, 5 HIGH/MEDIUM from iteration 1, 4 Minor from iteration 2)

---

### SCORING IMPACT TABLE

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Positive | Plan criteria gap closed. Further-reading block added. All structural elements present. |
| Internal Consistency | 0.20 | Positive | 80% practice-what-you-preach gap eliminated. "That's why" repetition resolved. No contradictions. |
| Methodological Rigor | 0.20 | Positive | All claims cited or honestly hedged. Five mechanism explanations. Liu et al. scope qualifier models good practice. |
| Evidence Quality | 0.15 | Positive | Five verified citations. No ungrounded claims. Context window figures concrete. |
| Actionability | 0.15 | Positive | Plan criteria, checklist, graduated on-ramp, closing challenge. |
| Traceability | 0.10 | Positive | Five author/year/finding citations. Further-reading block. Coined-term attribution. |

---

### PROGRESSION ACROSS ALL ITERATIONS

| Metric | Iter 1-v2 (Draft 5) | Iter 2 (Draft 6) | Iter 3 (Draft 7) | Total Delta |
|--------|---------------------|-------------------|-------------------|-------------|
| Composite | 0.918 | 0.937 | 0.954 | +0.036 |
| LLM-Tell | 0.72 | 0.85 | 0.90 | +0.18 |
| Voice Authenticity | 0.78 | 0.87 | 0.90 | +0.12 |
| Technical Accuracy | -- | 0.94 | 0.95 | +0.01 |

The three-iteration arc shows consistent, convergent improvement: each iteration targeted specific, identified weaknesses and produced measurable gains. The delta is decreasing (+0.019 iter 2->3 vs +0.019 iter 1->2 for composite, but the LLM-Tell and Voice gains were larger in iter 2 and smaller in iter 3), indicating the draft is approaching its quality ceiling for the genre.

**The deliverable is accepted.**
