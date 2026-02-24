# Pre-Mortem Report: "Why Structured Prompting Works" (Draft 6 -- Iteration 2)

**Strategy:** S-004 Pre-Mortem Analysis
**Deliverable:** `drafts/draft-6-iteration-2.md`
**Criticality:** C3 (public-facing article on an mkdocs site; brand credibility at stake)
**Date:** 2026-02-23
**Reviewer:** adv-executor (S-004, iteration 2)
**H-16 Compliance:** S-003 Steelman applied in iteration 1 (2026-02-23, confirmed -- see `adversary-critiques/iteration-1/S-003-steelman.md`)
**Prior Iterations:** S-004 iteration 1 produced 9 findings against draft 5. This iteration evaluates draft 6 to assess which findings were resolved and whether new failure modes emerged.
**Prior Quality Gate:** 0.938 PASS (iteration 3, S-014); iteration-1-v2 S-004 scored 0.72 LLM-Tell, 0.78 Voice Authenticity.

**Failure Scenario:** It is August 23, 2026 -- six months after publication on the Saucer Boy mkdocs site. The article received early traffic from direct shares but then three things happened: (1) a technical reader with prompt engineering expertise wrote a detailed response noting the article's citations are strong but the voice still carries traces of LLM generation, undermining the credibility of an article that teaches people how to get better LLM output, (2) a practitioner tried to apply the advice to debugging and email-writing tasks but found the examples too anchored to the original framework-evaluation domain, and (3) the `</output>` XML tag on line 96 was discovered in production after publication, proving the article was LLM-generated and creating a minor social media moment that damaged the Saucer Boy brand.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall failure assessment and recommendation |
| [Iteration 1 Findings Status](#iteration-1-findings-status) | Resolution tracking from prior pre-mortem |
| [Failure Causes](#failure-causes) | PM-001 through PM-007 with full details |
| [Findings Table](#findings-table) | Prioritized summary of all failure causes |
| [Recommendations](#recommendations) | P0/P1/P2 mitigation plan |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 dimensions |
| [LLM-Tell Assessment](#llm-tell-assessment) | Dedicated LLM-tell detection analysis |
| [Voice Authenticity Assessment](#voice-authenticity-assessment) | McConkey persona fidelity analysis |
| [Quality Scoring](#quality-scoring) | Composite score with dimension breakdown |

---

## Summary

Seven failure causes identified across Technical, Assumption, Process, and External categories. Draft 6 resolved the most critical finding from iteration 1 -- the "fluency-competence gap" neologism is now properly framed as the author's label ("I call it the fluency-competence gap") rather than established terminology. The article also improved its citation integration, shifting from parenthetical "from X to Y" survey-style references to more specific inline citations (Wei et al. 2022 for chain-of-thought, Bender and Koller 2020, Sharma et al. 2024, Panickssery et al. 2024). Voice consistency improved in several passages. However, three issues persist: the `</output>` XML tag on line 96, some residual LLM-tell patterns, and the domain-specificity of examples. These are tractable fixes.

**Recommendation:** ACCEPT with targeted P0 mitigations. The article is close to publication-ready.

---

## Iteration 1 Findings Status

| Iteration 1 Finding | Status in Draft 6 | Evidence |
|---------------------|--------------------|----------|
| PM-001-v1 (Residual LLM-tell patterns) | PARTIALLY RESOLVED | The three-beat parallel on lines 17-18 was rewritten. The "That's not X. It's Y" on line 19 is gone -- replaced with "The output sounds expert because the model learned to *sound* expert, not because it verified anything." This is still a contrast construction but reads more naturally. The "from X to Y" parenthetical survey on line 65 was replaced with specific Wei et al. citation on line 27. Some new patterns emerged (see PM-001 below). |
| PM-002-v1 ("Fluency-competence gap" neologism) | RESOLVED | Line 19: "I call it the fluency-competence gap." The framing now clearly presents this as the author's descriptive label, not established terminology. Additionally, the supporting evidence is now cited inline (Bender and Koller 2020, Sharma et al. 2024) rather than floating as an unsourced claim. |
| PM-003-v1 (Liu et al. citation year) | PARTIALLY RESOLVED | Line 57 still cites "Liu et al. (2023)". The citations.md companion notes 2023 preprint / 2024 publication. The preprint year is defensible but not aligned with the TACL 2024 formal publication. This is a minor consistency choice. |
| PM-004-v1 (Domain-specific examples) | NOT RESOLVED | Both Level 2 (lines 25-26) and Level 3 (lines 35-36) examples remain anchored to the framework-evaluation domain. No second domain example was added. The checklist (lines 82-88) is generic but lacks a worked example showing application to a different task type. |
| PM-005-v1 (Two-session pattern too technical) | PARTIALLY RESOLVED | The explanation was reworked. Lines 57-58 now use the "lost in the middle" citation with a clearer explanation: "information buried in the middle of a long context gets significantly less attention than content at the beginning or end." This is clearer than draft 5's "token budget is zero-sum" framing. However, the passage at lines 53-59 still relies on the reader understanding what a "conversation" means in context-window terms. No concrete non-technical analogy was added. |
| PM-006-v1 (Voice breaks at technical depth) | PARTIALLY RESOLVED | Several passages improved. Line 27 now reads more naturally with the Wei et al. citation integrated into the argument flow. However, lines 65 and 67 still contain register-neutral technical prose (see PM-005 below). |
| PM-007-v1 (No frontmatter/SEO) | NOT RESOLVED | No mkdocs frontmatter present. Title remains "Why Structured Prompting Works" with no search differentiation. |
| PM-008-v1 (Raw `</output>` tag) | NOT RESOLVED | Line 96 still contains `</output>`. |
| PM-009-v1 (Content elementary for experts) | ACKNOWLEDGED | This was classified P2 and was not expected to be addressed in this iteration. The article's positioning as a practitioner guide for intermediate users is appropriate. |

**Resolution rate:** 2 fully resolved, 3 partially resolved, 2 not resolved, 1 not applicable (P2). Net improvement is meaningful but the two unresolved P0 items (XML tag, domain examples) require attention.

---

## Failure Causes

### PM-001-20260223-iter2: Residual LLM-Tell Patterns [MAJOR]

**Failure Cause:** Four passages survive that trained LLM-output readers would flag. The draft improved substantially from iteration 1 -- the most egregious patterns were fixed -- but some remain:

1. **Line 17, sentence structure:** "They give you something worse: the most probable generic response from their training distribution, dressed up as a custom answer. Clean structure, professional headings, authoritative language." The final fragment-list ("Clean structure, professional headings, authoritative language") is a three-item asyndetic list that LLMs produce frequently as a rhetorical flourish. Humans writing conversationally tend to use "and" before the last item or vary the rhythm. This is a borderline case -- McConkey's voice is punchy enough that a fragment list could be intentional style. But combined with the colon-setup pattern, it reads as generated.

2. **Line 19, contrast construction:** "The output sounds expert because the model learned to *sound* expert, not because it verified anything." This is a cleaner version of the "That's not X. It's Y" pattern from draft 5. The italicized *sound* helps differentiate it. This is on the boundary -- it reads naturally enough in context. I flag it as borderline rather than definitive.

3. **Line 71:** "Every dimension you leave open, the model fills with the statistical default. Not out of laziness. Out of probability distributions." The two-fragment sentence-ending construction ("Not out of X. Out of Y.") is a signature LLM rhetorical move -- the dramatic two-beat corrective. This specific instance is well-suited to McConkey's voice (punchy, direct), which makes it harder to flag as a tell. But the pattern itself is extremely common in LLM output.

4. **Line 45:** "It's not garbage in, garbage out. It's garbage in, increasingly polished garbage out, and you genuinely cannot tell the difference until something downstream breaks." The "It's not X. It's Y" construction again. However, this instance is harder to flag because the second clause is structurally different from the first (longer, with a dependent clause). The asymmetry helps. This is the weakest flag of the four.

**Category:** Technical (LLM-tell detection)
**Likelihood:** MEDIUM -- The improvement from draft 5 is real. The remaining patterns are borderline rather than obvious. A trained reader might flag 1-2 of these; an untrained reader would flag none.
**Severity:** Major -- The article's credibility depends on not reading like LLM output. Even borderline cases matter for an article about how to use LLMs better.
**Evidence:** Lines 17, 19, 71, 45 in the deliverable.
**Dimension:** Evidence Quality (article credibility as authentic artifact)
**Mitigation:** Lines 17 and 71 are the strongest flags. Line 17: add "and" before "authoritative language" or restructure as a flowing sentence rather than fragment list. Line 71: merge the two fragments into one sentence ("Not out of laziness but out of probability distributions" or rephrase entirely). Lines 19 and 45 are borderline -- could be left as-is given the McConkey voice justification.
**Acceptance Criteria:** Zero passages where a majority of trained LLM-output readers would flag the passage as generated.

---

### PM-002-20260223-iter2: Raw `</output>` XML Tag on Line 96 [CRITICAL]

**Failure Cause:** Line 96 contains a literal `</output>` XML tag. This is a processing artifact from the LLM generation pipeline. If published to the mkdocs site, it will either render as visible text or as a malformed HTML element. This is the single highest-severity finding because it is not a stylistic tell -- it is proof of LLM generation visible in the published artifact. An article teaching people how to use LLMs better that ships with an LLM processing tag is a reputational catastrophe for the Saucer Boy brand.

This finding was raised as PM-008-20260223-v2 in iteration 1 and was not addressed in draft 6.

**Category:** Technical (artifact contamination)
**Likelihood:** HIGH -- The tag is present in the current file. It will appear in production unless explicitly removed.
**Severity:** Critical -- Trivial to fix but catastrophic if missed. Proves LLM authorship in a way that no amount of voice work can overcome.
**Evidence:** Line 96: `</output>`
**Dimension:** Evidence Quality (article authenticity)
**Mitigation:** Delete line 96. Verify no other XML processing artifacts exist in the file.
**Acceptance Criteria:** No XML processing artifacts present anywhere in the published file. A grep for `</output>`, `</input>`, `<output>`, `<input>`, `<response>`, `</response>` returns zero matches.

---

### PM-003-20260223-iter2: Examples Remain Domain-Specific [MAJOR]

**Failure Cause:** Both the Level 2 example (lines 25-26) and the Level 3 example (lines 35-36) use the same framework-evaluation task. The checklist at lines 82-88 is generic but abstract. A practitioner whose work is debugging, writing, data analysis, or code review reads the article and cannot translate the framework-evaluation examples to their own domain. They understand the principles intellectually but struggle to operationalize them. The article's impact is limited to readers who happen to work on framework-evaluation tasks -- a small minority.

This finding was raised as PM-004-20260223-v2 in iteration 1 and was not addressed in draft 6.

**Category:** Assumption (assumes reader can generalize from one domain-specific example)
**Likelihood:** HIGH -- Most readers work on tasks other than framework evaluation.
**Severity:** Major -- The article's entire value proposition is "change how you prompt." If readers cannot apply the advice to their actual work, the article fails at its primary purpose.
**Evidence:** Lines 25-26 (Level 2 example), lines 35-36 (Level 3 example). Both use "industry frameworks for X" as the task. Lines 82-88 (checklist) are generic but lack a worked application to a second domain.
**Dimension:** Actionability, Completeness
**Mitigation:** Add one brief example from a second domain. The most minimal change: insert a single parenthetical or sentence in the "Start Here" section showing the checklist applied to debugging. Example: "For a debugging task, that might look like: 'Here's the error and the code. Identify three possible causes, rank by likelihood, and recommend a fix -- show your reasoning before writing the code.'" This takes one sentence and demonstrates generalizability.
**Acceptance Criteria:** At least two distinct task domains represented in examples across the article.

---

### PM-004-20260223-iter2: Two-Session Pattern Still Requires Implicit Technical Knowledge [MEDIUM]

**Failure Cause:** The two-session pattern explanation (lines 47-61) improved from draft 5. The "lost in the middle" effect is now explained more clearly with the Liu et al. citation. However, the core rationale still assumes the reader understands: (a) what a "context window" is (line 57 uses the term without definition), (b) why prior messages compete with instructions (line 57: "Your carefully crafted instructions from message three are competing with forty messages of planning debate"), and (c) what "positional attention bias" means (line 57). The phrase "positional attention bias" is technical jargon that the target intermediate audience will not know.

A reader who does not understand context windows will read "start a new conversation" and ask "why?" The existing explanation answers with mechanism (context window, attention distribution) rather than consequence (the model's behavior degrades).

**Category:** Assumption (technical vocabulary exceeds audience)
**Likelihood:** MEDIUM -- The explanation is clearer than draft 5 and many readers will accept the advice on trust. But the "why" is important for adoption of counterintuitive behavior.
**Severity:** Medium -- Does not invalidate the article but reduces the persuasive power of the most novel section.
**Evidence:** Lines 53-59. Line 57: "Liu et al. (2023) showed that information buried in the middle of a long context gets significantly less attention than content at the beginning or end. They called it the 'lost in the middle' effect. It's a positional attention bias, not a simple capacity problem."
**Dimension:** Actionability
**Mitigation:** The "lost in the middle" citation is good. The term "positional attention bias" on line 57 should be either removed or translated. The sentence "It's a positional attention bias, not a simple capacity problem" could become "The model literally pays less attention to stuff in the middle of a long conversation -- it's not running out of room, it's losing focus." This maintains the technical accuracy while using language the target audience understands.
**Acceptance Criteria:** The two-session pattern rationale uses no unexplained technical jargon. A reader unfamiliar with LLM architecture can understand why a fresh conversation helps.

---

### PM-005-20260223-iter2: Voice Drops in Technical Explanation Passages [MEDIUM]

**Failure Cause:** The McConkey voice is strong in the opening (lines 3-9), the section titles ("Point Downhill and Hope"), the transitions (line 49: "Here's the move most people miss entirely"), and the closing (lines 91-95). But it drops in two clusters:

1. **Lines 65-67:** "Context windows are engineering constraints. Architecture, memory, compute tradeoffs. They've grown significantly over the past few years (GPT-3 shipped with 2K tokens in 2020; Gemini 1.5 crossed a million in 2024), but within any given model, they're hard limits you work within." The first two sentences are staccato technical fragments with no personality. "Architecture, memory, compute tradeoffs" is a noun-phrase list that reads like a technical spec, not a conversation. McConkey would not recite a list of engineering factors without comment.

2. **Line 67:** "The principles are universal. The syntax varies. XML tags for Claude, markdown for GPT, whatever the model prefers. The structure is the point, not the format." The four short sentences have a rhythmic pattern (statement, contrast, examples, epigram) that is technically competent but voice-neutral. The closing epigram "The structure is the point, not the format" was flagged in iteration 1 (line 69 of draft 5) and remains in similar form.

These are improved from draft 5 but still represent the clearest voice-drop zones.

**Category:** Process (voice consistency)
**Likelihood:** MEDIUM -- Casual readers will not notice. Voice-sensitive editorial review will.
**Severity:** Medium -- Does not undermine technical content but weakens brand differentiation.
**Evidence:** Lines 65-67 as cited above.
**Dimension:** Internal Consistency (voice consistency throughout)
**Mitigation:** Line 65 could become: "Context windows are engineering constraints -- architecture, memory, compute, the usual suspects. They've grown fast (GPT-3 shipped with 2K tokens in 2020; Gemini 1.5 crossed a million in 2024) but within any given model, they're hard limits." Adding "the usual suspects" or any conversational aside maintains voice through the technical content. Line 67 closing: "The structure is what matters, not whether you use XML or markdown" is less epigrammatic than "The structure is the point, not the format."
**Acceptance Criteria:** No passage where the voice register shifts noticeably from the surrounding McConkey-voiced text.

---

### PM-006-20260223-iter2: No mkdocs Frontmatter or Metadata [MINOR]

**Failure Cause:** The article has no YAML frontmatter for mkdocs. No title metadata, no description, no tags, no og:description for social sharing. When shared on social media, the preview will show a generic card with no description. When indexed by search engines, the article will lack structured metadata. The title "Why Structured Prompting Works" has low search differentiation against Anthropic, OpenAI, and Prompt Engineering Guide articles covering the same topic.

This finding was raised as PM-007-20260223-v2 in iteration 1 and was not addressed in draft 6.

**Category:** External (publication platform requirements)
**Likelihood:** MEDIUM -- Depends on distribution strategy. If shared via direct links only, frontmatter matters less.
**Severity:** Minor for the article itself (content is unaffected), medium for discoverability.
**Evidence:** Line 1 starts with `# Why Structured Prompting Works` -- no YAML frontmatter block preceding it.
**Dimension:** Completeness (publication readiness)
**Mitigation:** Add mkdocs-compatible YAML frontmatter before the title. Minimum: title, description (for meta tag and social previews), tags. Consider a subtitle that signals the unique McConkey angle for search differentiation.
**Acceptance Criteria:** Article has YAML frontmatter with at minimum title and description fields.

---

### PM-007-20260223-iter2: Liu et al. Citation Year Remains 2023 [MINOR]

**Failure Cause:** Line 57 cites "Liu et al. (2023)". The formal publication in TACL is 2024. The preprint date (July 2023) is defensible, but the citations.md companion file itself notes "Originally released as arXiv preprint, July 2023" and lists the 2024 TACL publication as the primary reference. Using the preprint year in the article body while the companion file emphasizes the 2024 publication creates a minor internal inconsistency.

This finding was raised as PM-003-20260223-v2 in iteration 1 and remains unchanged.

**Category:** Technical (citation consistency)
**Likelihood:** LOW -- Most readers will not check.
**Severity:** Minor -- The paper is real, the finding is real, the year is defensible.
**Evidence:** Line 57 of the article; citations.md section 2.
**Dimension:** Traceability
**Mitigation:** Either standardize on 2024 (matching the formal TACL publication) or add a parenthetical note in citations.md explaining the year choice. For a voice-first article, using 2024 is simpler and matches the formal record.
**Acceptance Criteria:** Citation year in article body matches the primary reference in citations.md.

---

## Findings Table

| ID | Failure Cause | Category | Likelihood | Severity | Priority | Affected Dimension |
|----|---------------|----------|------------|----------|----------|--------------------|
| PM-001-iter2 | Residual LLM-tell patterns (borderline, improved from iter 1) | Technical | Medium | Major | P1 | Evidence Quality |
| PM-002-iter2 | Raw `</output>` XML tag on line 96 | Technical | High | Critical | P0 | Evidence Quality |
| PM-003-iter2 | Examples remain domain-specific (unresolved from iter 1) | Assumption | High | Major | P0 | Actionability, Completeness |
| PM-004-iter2 | Two-session pattern uses unexplained technical jargon | Assumption | Medium | Medium | P1 | Actionability |
| PM-005-iter2 | McConkey voice drops at lines 65-67 | Process | Medium | Medium | P1 | Internal Consistency |
| PM-006-iter2 | No mkdocs frontmatter or metadata | External | Medium | Minor | P2 | Completeness |
| PM-007-iter2 | Liu et al. citation year 2023 vs. 2024 | Technical | Low | Minor | P2 | Traceability |

---

## Recommendations

### P0 -- MUST Mitigate Before Publication

**PM-002-iter2:** Delete the `</output>` tag on line 96. Grep the file for any other XML processing artifacts (`<output>`, `</output>`, `<response>`, `</response>`, `<input>`, `</input>`). This is a 2-second fix with catastrophic consequences if missed. This is the second iteration flagging this finding -- it must not survive to a third.

**PM-003-iter2:** Add one example from a non-framework-evaluation domain. Minimal change: one sentence in the "Start Here" section or as a parenthetical in the Level 2 section. A debugging example or a writing example that demonstrates the same principles applied to a different task type. This demonstrates the universality that the article claims but does not currently show.

### P1 -- SHOULD Mitigate Before Publication

**PM-001-iter2:** Rewrite the two strongest tell passages. Line 17: restructure "Clean structure, professional headings, authoritative language" with "and" or as flowing prose. Line 71: merge "Not out of laziness. Out of probability distributions." into a single sentence or rephrase. Lines 19 and 45 are borderline and could be left as-is given the McConkey voice justification.

**PM-004-iter2:** Replace "positional attention bias" on line 57 with a conversational explanation. The technical accuracy is preserved by the Liu et al. citation; the label does not need to be technical jargon.

**PM-005-iter2:** Add a conversational aside in the voice-drop zone at lines 65-67. Even small additions ("the usual suspects," "that's a lot of real estate") maintain persona through technical content.

### P2 -- MAY Mitigate; Acknowledge Risk

**PM-006-iter2:** Add mkdocs YAML frontmatter when the article is prepared for deployment. This is a publication-pipeline task rather than a content revision.

**PM-007-iter2:** Standardize Liu et al. citation to 2024 to match TACL publication and citations.md primary reference.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Slightly Negative | PM-003 (domain-specific examples), PM-006 (no frontmatter). The article covers the topic well but gaps in generalizability and publication metadata remain. Improved from iteration 1 -- the neologism fix (PM-002-v1) resolved a completeness gap in citation grounding. |
| Internal Consistency | 0.20 | Slightly Negative | PM-005 (voice drops at lines 65-67). The tonal oscillation is reduced from iteration 1 but not eliminated. The fluency-competence-gap fix improved consistency between claims and evidence. |
| Methodological Rigor | 0.20 | Neutral | The article's claims are now well-grounded. Inline citations (Wei et al., Bender & Koller, Sharma et al., Panickssery et al., Liu et al.) are specific and integrated into the argument. The neologism issue is resolved. No methodological concerns remain. |
| Evidence Quality | 0.15 | Slightly Negative | PM-002 (XML artifact), PM-001 (residual tells). The XML tag is the single largest evidence-quality risk. The remaining tells are borderline. Citation quality is strong. |
| Actionability | 0.15 | Slightly Negative | PM-003 (cannot generalize examples), PM-004 (technical jargon in two-session rationale). The checklist is strong but the worked examples need a second domain. |
| Traceability | 0.10 | Neutral | PM-007 (citation year) is minor. The citations.md companion provides excellent traceability. Inline citations in the article body are specific and verifiable. |

**Net assessment:** The article improved meaningfully from draft 5 to draft 6. The neologism fix, improved citations, and voice-consistency work addressed the highest-value findings from iteration 1. The remaining findings are tractable -- one trivial fix (XML tag), one small addition (second domain example), and several polish items. No structural failures remain.

---

## LLM-Tell Assessment

**Score: 0.80** (where 1.0 = no detectable LLM tells; up from 0.72 in iteration 1)

Improvement from iteration 1: The "That's not X. It's Y" pattern on the former line 19 was reworked. The "from X to Y" parenthetical survey was replaced with specific citations. The three-beat parallel on the former lines 17-18 was partially addressed. The remaining patterns are borderline rather than obvious.

| Tell Category | Instances | Severity | Lines |
|---------------|-----------|----------|-------|
| Three-item asyndetic fragment list | 1 | Low-Medium | 17 |
| Two-fragment corrective ("Not X. Y.") | 1 | Low-Medium | 71 |
| Contrast construction with italics | 1 | Low (borderline) | 19 |
| "It's not X. It's Y" with asymmetric expansion | 1 | Low (borderline) | 45 |
| Raw XML processing artifact | 1 | Critical | 96 |

**Assessment methodology:** Same as iteration 1. Each passage evaluated against: "If 100 people who work with LLMs daily read this blind, how many would flag this passage as probably LLM-generated?" Passages exceeding 30% are flagged.

**Score justification:** Draft 6 moved 2 of the 4 original pattern instances from "definitive tell" to "borderline." The two remaining borderline patterns (lines 19, 45) could plausibly be intentional McConkey voice. The two stronger flags (lines 17, 71) are still detectable but less obvious than the draft-5 versions. The XML tag remains the single critical tell. Net improvement: 0.72 to 0.80.

**Passages that are NOT tells:**
- Line 7 ("Think of it like big-mountain skiing"): Persona-driven, not a generic analogy deployment.
- Line 42 bullet list: Content-specific enough to not trigger pattern detection.
- Lines 69-75 (Three Principles): The numbered structure is conventional for technical articles. The content is specific and well-argued.
- Line 27: The Wei et al. citation integration reads naturally. The specific attribution ("Wei et al. (2022) demonstrated this with chain-of-thought prompting") is how a human citing research they actually read would write.

---

## Voice Authenticity Assessment

**Score: 0.82** (where 1.0 = fully authentic, consistent McConkey voice throughout; up from 0.78 in iteration 1)

**Strongest voice passages:**
- Lines 3-9 (opening): "Alright, this trips up everybody, so don't feel singled out." Direct, warm, peer-to-peer. Genuine McConkey register.
- Lines 5-6: "Your instinct was right. Asking an LLM to apply industry frameworks to a repo is a reasonable ask. The gap isn't in *what* you asked for. It's in how much you told it about what good looks like." This is excellent -- validates the reader, then redirects without condescension.
- Line 11: "Point Downhill and Hope" -- The section title is organic skiing vocabulary used as a metaphor. Natural.
- Lines 49-50: "Here's the move most people miss entirely." Direct, action-oriented, creating anticipation.
- Lines 91-95 (closing): The McConkey callback, the concrete challenge, and the dare. Strong voice, strong close. "I dare you." is a perfect McConkey-register ending.

**Improved voice passages (vs. draft 5):**
- Line 19: The shift from "It's called the 'fluency-competence gap'" (authoritative register) to "I call it the fluency-competence gap" is a significant voice improvement. "I call it" is a McConkey move -- direct, personal, owning the framing.
- Lines 42-43: "Here's the tension: I just told the model to critique its own work, but models genuinely struggle with self-assessment." The "Here's the tension" setup is conversational and voice-consistent. This was less personal in draft 5.

**Weakest voice passages:**
- Lines 65-66: "Context windows are engineering constraints. Architecture, memory, compute tradeoffs." -- Technical-spec register. No personality. McConkey wouldn't recite engineering factors as a bare noun-phrase list.
- Line 67: "The principles are universal. The syntax varies." -- Crisp but voice-neutral. Could be any technical writer.
- Line 57: "It's a positional attention bias, not a simple capacity problem." -- Academic register inserted into an otherwise conversational passage.

**Voice distribution:** Approximately 70% of the article maintains the McConkey voice (up from 65% in draft 5). The remaining 30% drops into neutral technical prose. The drops are narrower and less severe than in draft 5 -- they cluster in the "Why This Works on Every Model" section (lines 63-68) which is the most abstractly technical section of the article.

---

## Quality Scoring

### Dimension Breakdown

| Dimension | Weight | Score | Weighted | Rationale |
|-----------|--------|-------|----------|-----------|
| Completeness | 0.20 | 0.91 | 0.182 | Strong topic coverage. Level 1/2/3 framework is clear and well-differentiated. Two-session pattern and three principles provide structure. Checklist adds actionability. Deductions: single-domain examples (PM-003), no frontmatter (PM-006). The neologism fix closes a prior completeness gap. |
| Internal Consistency | 0.20 | 0.92 | 0.184 | Claims are internally consistent. Citations support the arguments they accompany. The voice oscillation (PM-005) is the primary consistency issue but it's reduced from iteration 1. No logical contradictions. The fluency-competence-gap reframing eliminated a consistency issue between claims and evidence grounding. |
| Methodological Rigor | 0.20 | 0.94 | 0.188 | The article's argument structure is sound. Claims are supported by specific citations (Wei et al., Liu et al., Bender & Koller, Sharma et al., Panickssery et al.). The progression from Level 1 to Level 3 is logically constructed. The self-critique limitation acknowledgment (lines 42-43) demonstrates intellectual honesty. |
| Evidence Quality | 0.15 | 0.88 | 0.132 | Citations are real, relevant, and correctly attributed. The citations.md companion is thorough. Deductions: XML artifact (PM-002) is a severe evidence-quality risk if published, residual LLM-tell patterns (PM-001) weaken authenticity. Without these two issues, evidence quality would score 0.95+. |
| Actionability | 0.15 | 0.90 | 0.135 | The checklist (lines 82-88) is immediately actionable. Level 2 and Level 3 examples are concrete. The "Start Here" section provides an on-ramp. Deductions: single-domain examples (PM-003) limit transferability, technical jargon in two-session rationale (PM-004) reduces accessibility. |
| Traceability | 0.10 | 0.93 | 0.093 | Inline citations throughout the article. Citations.md companion provides full reference with URLs, key findings, and claim-to-source mapping. Minor deduction for Liu et al. year inconsistency (PM-007). |

**Composite Score: 0.914**

### Verdict: REVISE

The composite score of 0.914 falls in the REVISE band (0.92-0.94 target for PASS at the specified >= 0.95 threshold; below 0.92 at the standard quality-enforcement.md threshold).

**Path to PASS:** Addressing the two P0 findings would likely push the score above 0.92:
- Removing the XML artifact (PM-002) would increase Evidence Quality from 0.88 to approximately 0.93 (+0.0075 weighted).
- Adding a second-domain example (PM-003) would increase both Actionability (0.90 to ~0.93) and Completeness (0.91 to ~0.93), for approximately +0.009 weighted.

Estimated post-P0-mitigation composite: **0.930** -- which would PASS at the 0.92 threshold but still fall below the specified 0.95 threshold.

To reach 0.95, P1 mitigations (LLM-tell cleanup, jargon replacement, voice-consistency work) would also be needed. These would primarily improve Evidence Quality and Internal Consistency.

### Additional Scores

**LLM-Tell Detection Score: 0.80** (improved from 0.72)
**Voice Authenticity Score: 0.82** (improved from 0.78)

---

*Report generated by adv-executor running S-004 Pre-Mortem Analysis, iteration 2.*
*SSOT: `.context/rules/quality-enforcement.md`*
*Template: `.context/templates/adversarial/s-004-pre-mortem.md`*
*Prior iteration: `adversary-critiques/iteration-1-v2/S-004-pre-mortem.md`*
