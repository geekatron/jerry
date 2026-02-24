# Devil's Advocate Report: ART-001 Structured Prompting Article (Draft 7, Iteration 3)

**Strategy:** S-002 Devil's Advocate
**Deliverable:** `projects/PROJ-011-saucer-boy-articles/work/articles/ART-001-structured-prompting/drafts/draft-7-iteration-3.md`
**Criticality:** C2
**Date:** 2026-02-23
**Reviewer:** adv-executor (S-002)
**Iteration:** 3 (reviewing draft-7-iteration-3 against iteration-2 findings)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment and verdict |
| [Iteration 2 Issue Tracking](#iteration-2-issue-tracking) | Status of all 8 findings from iteration-2 |
| [Findings Table](#findings-table) | New and residual findings with severity |
| [Finding Details](#finding-details) | Expanded analysis per Critical and Major finding |
| [Recommendations](#recommendations) | Prioritized action list |
| [Scoring Impact](#scoring-impact) | Six-dimension S-014 scoring with weights |
| [Additional Criteria](#additional-criteria) | LLM-Tell Detection and Voice Authenticity |
| [Composite Score](#composite-score) | Weighted total and band classification |

---

## Summary

6 findings identified (0 Critical, 1 Major, 5 Minor). Draft 7 shows targeted improvement over draft 6, resolving or partially resolving 6 of 8 iteration-2 findings. The error-compounding claim (DA-002-iter2) has been reframed from unsupported assertion to "a well-established pattern in pipeline design," which reduces the practice-preaching inconsistency to a Minor issue. The "training-data regurgitation" phrasing (DA-007-iter2) has been corrected to "pattern completion from training data." The "I dare you" closing (DA-008-iter2) has been softened to "Do that once and tell me it didn't change the output." One Major finding persists: the Level 3 prompt still assumes tool-enabled models without disclosure (DA-001-iter2, carried forward as DA-001-iter3). This is the single remaining gap separating the article from the PASS threshold.

---

## Iteration 2 Issue Tracking

Mapping each of the 8 findings from `iteration-2/S-002-devils-advocate.md` against draft-7-iteration-3.

| ID | Original Severity | Original Finding | Status in Draft 7 | Notes |
|----|-------------------|------------------|--------------------|-------|
| DA-001-iter2 | Major | Level 3 assumes tool-enabled models without disclosure | **UNRESOLVED** | Lines 35-36 still read "gap analysis on this repo" and "research the top 10 industry frameworks using real sources, not training data." Lines 63-67 ("Why This Works on Every Model") discuss syntax variation and context windows but do not acknowledge the tool-access prerequisite. The opening paragraph (line 3) amplifies the universality claim: "applies to every LLM on the market." Carried forward as DA-001-iter3 (Major). |
| DA-002-iter2 | Major | Error-compounding claim lacks evidence, creating practice-preaching inconsistency | **PARTIALLY RESOLVED** | Line 45 now reads: "This is a well-established pattern in pipeline design, and it hits LLM workflows especially hard." This reframes the claim as a recognized engineering principle rather than a novel research finding, reducing the citation burden. The ending "it gets much harder to tell the difference" replaces "you genuinely cannot tell the difference," softening from assertion to observation. The citations companion (Section 6) documents the Arize AI source. The inline framing shift is sufficient to close the internal consistency gap. Downgraded to Minor (DA-002-iter3). |
| DA-003-iter2 | Minor | Context window growth figures imply continuous growth | **RETAINED** | Line 65 unchanged: "GPT-3 shipped with 2K tokens in 2020, and Gemini 1.5 crossed a million in 2024." Factually correct. The step-function trajectory is not mentioned but the sentence does not explicitly claim continuity either. Acceptable for audience. Carried forward as DA-003-iter3 (Minor). |
| DA-004-iter2 | Minor | Two-session pattern cost underdeveloped | **IMPROVED** | Lines 60-62 now specify what "stand alone" requires: "Phases, what 'done' looks like for each phase, output format. If the plan can't stand alone, it wasn't detailed enough." This is more concrete than draft 6. The practical failure mode (incomplete plan) is now addressed implicitly. Carried forward as DA-004-iter3 (Minor, reduced impact). |
| DA-005-iter2 | Minor | Error compounding delivered with more confidence than evidence | **RESOLVED** | Absorbed into DA-002-iter2 resolution. The reframing as "well-established pattern in pipeline design" and the softened "it gets much harder" language bring the confidence level in line with the evidence level. |
| DA-006-iter2 | Minor | Three Principles retains parallel structure LLM tell | **RETAINED** | Lines 69-75 still use three paragraphs with bold imperative leads: "Constrain the work," "Review the plan before the product," "Separate planning from execution." Each followed by explanatory prose of similar length. The structure is recognizable as a pattern an LLM would produce. However: (a) the explanatory prose within each paragraph varies in rhythm and length, (b) the third principle integrates specific practical advice ("Don't drag 40 messages") rather than repeating the abstract-then-elaborate pattern. Carried forward as DA-005-iter3 (Minor). |
| DA-007-iter2 | Minor | "Training-data regurgitation" slightly misleading | **RESOLVED** | Line 40 now reads "pattern completion from training data." Accurate characterization. The model always generates from learned distributions; "pattern completion" correctly describes the mechanism being constrained. |
| DA-008-iter2 | Minor | "I dare you" genre-dependent risk | **RESOLVED** | Line 98 now reads "Do that once and tell me it didn't change the output." Confident without the dare-challenge register. Retains the McConkey energy while reading as earned conviction rather than LinkedIn provocation. |

**Summary:** 3 of 8 issues fully resolved. 2 partially resolved and downgraded. 2 retained at same severity (Minor). 1 unresolved (Major, carried forward).

---

## Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| DA-001-iter3 | Level 3 prompt assumes tool-enabled models; opening universality claim amplifies the gap | Major | Lines 3, 35-36, 63-67: "applies to every LLM on the market" + "gap analysis on this repo" + "real sources, not training data" + no tool-access disclosure | Completeness |
| DA-002-iter3 | Error-compounding claim now framed as engineering principle but still uncited inline | Minor | Line 45: "This is a well-established pattern in pipeline design" -- grounded framing reduces but does not eliminate the gap; companion citations cover it but inline article does not | Internal Consistency |
| DA-003-iter3 | Context window growth description omits step-function trajectory | Minor | Line 65: "GPT-3 shipped with 2K tokens in 2020, and Gemini 1.5 crossed a million in 2024" -- accurate endpoints but implies smooth progression | Evidence Quality |
| DA-004-iter3 | Two-session pattern acknowledges cost but could strengthen one practical guard | Minor | Lines 60-62: now specifies what the plan must contain but does not address the most common failure (pasting the plan without the execution-role instruction) | Actionability |
| DA-005-iter3 | Three Principles section retains recognizable parallel structure | Minor | Lines 69-75: bold imperative lead + explanatory paragraph x3; improved internal variation but the section-level pattern remains identifiable | Internal Consistency |
| DA-006-iter3 | "Attentional pattern applies broadly" extrapolation is qualified but not bounded | Minor | Lines 57-58: "They studied retrieval tasks, but the attentional pattern applies broadly" -- an honest qualification, but "applies broadly" is a claim the cited paper did not make | Methodological Rigor |

---

## Finding Details

### DA-001-iter3: Level 3 assumes tool-enabled models; opening universality claim amplifies [MAJOR]

**Claim Challenged:** The opening paragraph (line 3) asserts: "What I'm about to walk you through applies to every LLM on the market. Claude, GPT, Gemini, Llama, whatever ships next Tuesday." The Level 3 prompt example (lines 35-36) then instructs: "Do two things in parallel: gap analysis on this repo, and research the top 10 industry frameworks using real sources, not training data." The "Why This Works on Every Model" section (lines 63-67) discusses context windows and syntax variation without acknowledging tool-access requirements.

**Counter-Argument:** This finding was flagged as Major in iteration 2 and has not been addressed in draft 7. The gap has actually widened slightly: draft 7 strengthened the opening universality claim with "whatever ships next Tuesday," making the scope explicitly inclusive of all future models, while the Level 3 example still requires capabilities (file system access, web search) that many models and deployment contexts do not have.

The article's three-level framework is sound and the universality claim is correct for Levels 1 and 2, which require only a chat interface. The principles underlying Level 3 (parallel work streams, evidence requirements, self-critique, checkpoints) are also universal. The issue is narrow but material: the Level 3 *prompt example* requires tool access, and a reader following it in a plain chat interface will get hallucinated file analysis and fabricated citations, then attribute the failure to the article's advice.

This is not a request for a caveat paragraph or a long technical disclaimer. It is a request for one sentence that makes the article's advice actually universal, as the opening promises. Something like: "Level 3 works best when the model can access your files and search for sources directly. In a plain chat window, paste the relevant code and verify citations yourself -- same principles, different mechanics."

**Evidence:** Line 3 (universality claim), lines 35-36 (Level 3 prompt requiring file access and search), lines 63-67 (universality section discussing syntax but not capabilities).

**Impact:** A practitioner using a plain chat interface follows the Level 3 example, gets fabricated results, and concludes the article oversold its advice. The article's credibility suffers precisely where its most ambitious recommendation lives.

**Dimension:** Completeness (prerequisite information for Level 3 missing)

**Response Required:** Add one sentence either within the Level 3 section or in "Why This Works on Every Model" that acknowledges the tool-access requirement and provides the fallback for tool-less environments.

**Acceptance Criteria:** A reader using any chat interface -- tool-enabled or not -- can follow the article's advice at every level without encountering unexplained failure modes.

---

## Recommendations

### P1 (Major -- SHOULD resolve; require justification if not)

1. **DA-001-iter3:** Add one sentence disclosing Level 3's tool-access assumption with a fallback for plain chat interfaces. This is the third iteration carrying this finding. The fix is a single sentence that makes the universality claim honest across all three levels. Suggested locations: after the Level 3 prompt block (between lines 36 and 37), or within "Why This Works on Every Model" (after line 67). Acceptance criteria: reader using a plain chat interface knows what to adjust.

### P2 (Minor -- MAY resolve; acknowledgment sufficient)

2. **DA-002-iter3:** The reframing as "well-established pattern in pipeline design" is sufficient for internal consistency. If the author wishes to strengthen further, the citations companion Section 6 (Arize AI) could be referenced in the "Further reading" callout at line 102. Acknowledgment sufficient.

3. **DA-003-iter3:** Context window growth could note the step-function trajectory. Factually accurate as-is. Acknowledgment sufficient.

4. **DA-004-iter3:** The two-session pattern explanation could add one practical guard: "When you paste the plan into the new conversation, include the execution instruction. The plan without the role is just a document." Acknowledgment sufficient.

5. **DA-005-iter3:** Three Principles parallel structure is a residual LLM tell. The internal variation within each paragraph mitigates it. Further disruption (e.g., varying the lead format for the third principle) would eliminate the pattern entirely. Acknowledgment sufficient.

6. **DA-006-iter3:** "Applies broadly" extrapolation is honest but unbounded. Adding "your planning instructions from message three are competing with forty messages of planning debate" (which is already present at line 57) grounds the extrapolation in the article's specific use case. Already partially addressed. Acknowledgment sufficient.

---

## Scoring Impact

| Dimension | Weight | Score | Rationale |
|-----------|--------|-------|-----------|
| Completeness | 0.20 | 0.93 | Three-level framework is comprehensive with clear progression. Level 2 is well-positioned as the primary recommendation with an actionable checklist. Two-session pattern is concrete. Missing: tool-access prerequisite for Level 3 (DA-001-iter3) -- this is a narrow gap (one sentence) but it sits on the article's most ambitious recommendation. The "Further reading" callout (line 102) improves completeness for readers who want to verify claims. Score improved from 0.91 (iter2) by the two-session pattern strengthening (DA-004 improvement) and citations callout, held back by the persistent DA-001 gap. |
| Internal Consistency | 0.20 | 0.95 | Major improvement. The error-compounding reframing ("well-established pattern in pipeline design") closes the practice-preaching gap that was the primary consistency concern in iteration 2. Self-critique tension explicitly acknowledged (lines 42-43). Liu et al. correctly characterized. McConkey framing consistent. "Pattern completion from training data" replaces the misleading "training-data regurgitation." Three Principles parallel structure (DA-005-iter3) is a Minor tell, not a consistency issue. The universality claim vs. Level 3 capability gap (DA-001-iter3) is scored under Completeness. No dimension shows internal contradiction. |
| Methodological Rigor | 0.20 | 0.94 | Four named citations with specific findings described inline. The fluency-competence gap is properly introduced as the author's coinage with supporting literature. Wei et al. chain-of-thought finding correctly described and applied. Panickssery et al. self-preference finding correctly applied with explicit tension acknowledgment. Liu et al. "lost in the middle" correctly characterized with scope qualifier ("They studied retrieval tasks"). The "applies broadly" extrapolation (DA-006-iter3) is a minor inferential step, mitigated by the article grounding the extrapolation in a concrete scenario (lines 57-58). Error-compounding framed as engineering principle rather than novel finding. |
| Evidence Quality | 0.15 | 0.93 | Four inline citations, each with specific findings described rather than name-dropped. Citations companion provides full bibliographic detail with URLs. The error-compounding claim is now framed as established engineering principle, reducing the evidence burden. Context window figures are accurate (DA-003-iter3 is cosmetic). The "Further reading" callout at line 102 directs readers to the companion document, improving the article's evidence trail. Improvement from 0.91 (iter2) driven by the error-compounding reframing and citations callout. |
| Actionability | 0.15 | 0.96 | Unchanged from iteration 2 -- this is the article's strongest dimension. Three levels with clear progression. Level 2 checklist is immediately usable. Level 3 prompt is copy-pasteable (for tool-enabled environments). Two-session pattern includes concrete "what the plan must contain" guidance (lines 60-62). "Start with Level 2, graduate to Level 3" provides a clear adoption path. Five-item combined checklist (lines 81-93) is practical and scannable. Minor gap: DA-004-iter3 (two-session pattern could add one practical guard). |
| Traceability | 0.10 | 0.93 | Four named citations inline with specific findings described. Citations companion provides claim-to-source mapping with URLs. "Further reading" callout (line 102) directs readers to the companion with three recommended starting papers. Improvement from 0.90 (iter2) driven by the explicit reading-order recommendation in the callout. Error-compounding claim traces to "well-established pattern in pipeline design" framing; companion Section 6 provides the Arize AI source. |

---

## Additional Criteria

| Criterion | Score | Rationale |
|-----------|-------|-----------|
| LLM-Tell Detection | 0.89 | Incremental improvement from 0.88 (iter2). "Training-data regurgitation" replaced with "pattern completion from training data" -- eliminates one catchphrase-style tell. "I dare you" replaced with "Do that once and tell me it didn't change the output" -- eliminates the performative-challenge tell. Remaining: Three Principles section (lines 69-75) retains the bold-imperative-lead x3 parallel structure, which is the most recognizable LLM authorship signal in the draft. The explanatory prose within each paragraph varies enough to disrupt the pattern partially, but the section-level repetition (bold phrase, period, explanatory paragraph) is identifiable. Outside the Three Principles section, the prose reads naturally. "Point Downhill and Hope" heading is distinctly human. Technical explanations are integrated with voice rather than dropped into lecture register. No double-dash structural crutches. Minimal hedging language. |
| Voice Authenticity | 0.93 | Improvement from 0.91 (iter2). The "I dare you" replacement ("Do that once and tell me it didn't change the output") lands with earned conviction instead of influencer bravado. "This is a well-established pattern in pipeline design" is a natural register for someone who has seen it in practice. "You don't need a flight plan for the bunny hill" (line 29) is authentic McConkey register. "Here's the tension with that self-critique step" (line 42) reads as someone working through a genuine problem, not asserting a conclusion. "The guy looked completely unhinged on the mountain. He wasn't." (line 7) is punchy, specific, earned. The closing McConkey callback (line 96) lands cleanly. Technical sections maintain voice better than any prior draft: "the dangerous part" (line 16), "That's real" (line 60), "Don't drag 40 messages" (line 75). Minor drops: lines 63-65 ("Context windows are engineering constraints, the kind of hard limits determined by architecture and compute. They've grown fast") is competent technical writing but reads as generic prose -- not distinctly McConkey. Three Principles section (lines 69-75) is the weakest voice section: imperative-then-explain is how a textbook delivers principles, not how a freeskier would share what they learned on the mountain. |

---

## Composite Score

| Dimension | Weight | Score | Weighted |
|-----------|--------|-------|----------|
| Completeness | 0.20 | 0.93 | 0.186 |
| Internal Consistency | 0.20 | 0.95 | 0.190 |
| Methodological Rigor | 0.20 | 0.94 | 0.188 |
| Evidence Quality | 0.15 | 0.93 | 0.140 |
| Actionability | 0.15 | 0.96 | 0.144 |
| Traceability | 0.10 | 0.93 | 0.093 |
| **Weighted Composite** | **1.00** | | **0.941** |

**Band:** REVISE (0.92-0.94 per task-specified thresholds)

The composite score of 0.941 represents meaningful improvement from iteration 2 (0.923 to 0.941). The article has closed the internal consistency gap (0.92 to 0.95) through the error-compounding reframing and resolved several minor findings. The single remaining Major finding (DA-001-iter3, tool-access disclosure) is the gap between REVISE and PASS. Resolving it would likely push Completeness from 0.93 to 0.95, moving the composite to approximately 0.945, which crosses the 0.945 boundary but remains below 0.95.

To reach >= 0.95, the article would also need to address at least one of the Minor findings that affect the higher-weighted dimensions (Internal Consistency at 0.95 has limited headroom; Methodological Rigor at 0.94 could reach 0.95 with the DA-006-iter3 extrapolation bounded; Evidence Quality at 0.93 could reach 0.95 with a brief inline acknowledgment of the error-compounding source).

**Verdict: REVISE**

The article is within striking distance of PASS. The path from 0.941 to 0.95 requires:

1. **Required (Major):** Add one sentence disclosing Level 3's tool-access assumption with fallback guidance (DA-001-iter3). This finding has persisted across three iterations.
2. **Recommended (Minor, high leverage):** Strengthen the "Further reading" callout or inline text to briefly reference the error-compounding source (e.g., mentioning pipeline error propagation alongside the three recommended papers). This would push Evidence Quality and Traceability each by 0.01-0.02.
3. **Recommended (Minor, voice):** Break the Three Principles parallel structure by varying the third principle's delivery format (e.g., lead with the practical advice instead of the imperative label). This would improve LLM-Tell Detection and Voice Authenticity.

The five Minor findings individually do not block acceptance. Collectively, they represent the polish margin between a good article and the article's full potential.
