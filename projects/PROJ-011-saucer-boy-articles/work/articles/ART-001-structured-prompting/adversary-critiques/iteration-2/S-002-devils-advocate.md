# Devil's Advocate Report: ART-001 Structured Prompting Article (Draft 6, Iteration 2)

**Strategy:** S-002 Devil's Advocate
**Deliverable:** `projects/PROJ-011-saucer-boy-articles/work/articles/ART-001-structured-prompting/drafts/draft-6-iteration-2.md`
**Criticality:** C2
**Date:** 2026-02-23
**Reviewer:** adv-executor (S-002)
**Iteration:** 2 (reviewing draft-6-iteration-2 against iteration-1-v2 findings)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment and verdict |
| [Iteration 1 Issue Tracking](#iteration-1-issue-tracking) | Status of all 11 issues from iteration-1-v2 |
| [Findings Table](#findings-table) | New and residual findings with severity |
| [Finding Details](#finding-details) | Expanded analysis per Critical and Major finding |
| [Recommendations](#recommendations) | Prioritized action list |
| [Scoring Impact](#scoring-impact) | Six-dimension S-014 scoring with weights |
| [Additional Criteria](#additional-criteria) | LLM-Tell Detection and Voice Authenticity |
| [Composite Score](#composite-score) | Weighted total and band classification |

---

## Summary

8 findings identified (0 Critical, 2 Major, 6 Minor). The draft has undergone substantial revision from draft-5, addressing the most damaging issues from iteration 1. The "fluency-competence gap" is no longer presented as a canonical term but is still used as a coined label -- now with proper citation support (Bender and Koller 2020, Sharma et al. 2024) that grounds the underlying phenomenon. The Liu et al. citation has been corrected from a vague "performance degrades with length" claim to the specific positional attention bias finding. The self-critique tension is now explicitly acknowledged. The McConkey framing has been reworked. Several issues downgraded from prior severity. The article practices what it preaches far more effectively than draft-5. The two remaining Major findings are addressable with targeted revision.

---

## Iteration 1 Issue Tracking

Mapping each of the 11 issues from `iteration-1-v2/S-002-devils-advocate.md` against draft-6-iteration-2.

| Issue # | Original Priority | Original Finding | Status in Draft 6 | Notes |
|---------|-------------------|------------------|--------------------|-------|
| 1 | HIGH | "Fluency-competence gap" is unverifiable term | **RESOLVED** | No longer presented as established nomenclature. Draft 6 line 19: "I call it the fluency-competence gap." Owns it as the author's coinage. Supported by Bender and Koller (2020) and Sharma et al. (2024) citations grounding the underlying phenomenon. |
| 2 | HIGH | Liu et al. citation misapplied (positional vs. volumetric) | **RESOLVED** | Draft 6 lines 57-58 now correctly states: "Liu et al. (2023) showed that information buried in the middle of a long context gets significantly less attention than content at the beginning or end. They called it the 'lost in the middle' effect. It's a positional attention bias, not a simple capacity problem." Accurately characterizes the finding. |
| 3 | MEDIUM | "Training-data gravity" technically imprecise | **PARTIALLY RESOLVED** | The phrase "training-data regurgitation" (line 40) replaces "training-data gravity." More accurate but still slightly misleading -- see DA-007-iter2. |
| 4 | HIGH | Error compounding claim lacks evidence | **RESOLVED** | Draft 6 lines 45 now states the claim more carefully: "it doesn't just persist. It compounds" and "The errors are structural." The language is more measured. The claim is still not cited, but the phrasing is now presented as an observation rather than a research finding. Downgraded from HIGH to Minor (see DA-005-iter2). |
| 5 | MEDIUM | Level 3 presupposes tool-enabled models | **PARTIALLY RESOLVED** | Draft 6 line 40 still says "research the top 10 industry frameworks using real sources, not training data" without clarifying tool access. However, the "Why This Works on Every Model" section (lines 63-67) is more measured about universality. See DA-001-iter2. |
| 6 | MEDIUM | "Most generic probable completion" oversimplification | **RESOLVED** | Draft 6 line 71: "Every dimension you leave open, the model fills with the statistical default. Not out of laziness. Out of probability distributions." Replaces "most generic probable completion" with "statistical default" and explicitly attributes the mechanism to probability distributions rather than implying deterministic greedy decoding. |
| 7 | LOW | Self-assessment tension unresolved | **RESOLVED** | Draft 6 lines 42: "Here's the tension: I just told the model to critique its own work, but models genuinely struggle with self-assessment. Panickssery et al. (2024) showed that LLMs recognize and favor their own output... Self-critique in the prompt is still useful as a first pass, a way to catch obvious gaps. But it's not a substitute for your eyes on the output." Explicitly acknowledges and resolves the tension. |
| 8 | MEDIUM | McConkey framing splits perspective | **RESOLVED** | Draft 6 lines 6-8 reworked: "Shane McConkey, if you don't know him, was a legendary freeskier who literally competed in a banana suit and won. The guy looked completely unhinged on the mountain. He wasn't." This is now a third-person reference that works as the narrator channeling McConkey's ethos rather than claiming to be McConkey. The perspective is consistent throughout. |
| 9 | LOW | Chain-of-thought reference too casual | **RESOLVED** | Draft 6 line 27: "Wei et al. (2022) demonstrated this with chain-of-thought prompting: just adding intermediate reasoning steps to a prompt measurably improved performance on arithmetic, commonsense, and symbolic reasoning tasks." Properly cited with specific finding described. |
| 10 | MEDIUM | Bold-numbered principles pattern is LLM tell | **PARTIALLY RESOLVED** | Draft 6 lines 71-75 still use a structured principle format but have moved away from the rigid `**1. Phrase.**` pattern. Now uses paragraph form with the principle name leading. Improvement but residual parallel structure. See DA-006-iter2. |
| 11 | LOW | "I dare you" performative risk | **RETAINED** | Draft 6 line 95: "I dare you." Intentionally retained. This is a persona choice. See DA-008-iter2 as Minor. |

**Summary:** 7 of 11 issues fully resolved. 3 partially resolved (downgraded in severity). 1 intentionally retained (persona choice).

---

## Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| DA-001-iter2 | Level 3 prompt still assumes tool-enabled models without disclosure | Major | Lines 35, 39-40: "gap analysis on this repo" and "real sources, not training data" presuppose file access and search tools | Completeness |
| DA-002-iter2 | Article preaches citation rigor but error-compounding claim remains unsupported | Major | Lines 45: "it compounds... The errors are structural" -- no citation, no mechanism described beyond analogy | Internal Consistency |
| DA-003-iter2 | Context window growth figures slightly imprecise | Minor | Line 65: "GPT-3 shipped with 2K tokens in 2020" -- GPT-3 had a 2,048 token context, correct; "Gemini 1.5 crossed a million in 2024" -- correct. However, the parenthetical implies continuous growth when the trajectory was step-function. | Evidence Quality |
| DA-004-iter2 | The two-session pattern cost is acknowledged but underdeveloped | Minor | Lines 60-61: acknowledges loss of "back-and-forth nuance" but does not address practical failure modes (e.g., plan artifact that omits implicit context from the planning conversation, reader who pastes an incomplete plan) | Actionability |
| DA-005-iter2 | Error compounding claim delivered with more confidence than evidence supports | Minor | Line 45: "It's not garbage in, garbage out. It's garbage in, increasingly polished garbage out, and you genuinely cannot tell the difference until something downstream breaks." Vivid but presented as established fact without citation. The Jerry framework itself cites DeepMind's 1.3x vs 17x amplification figures -- this article could benefit from similar grounding. | Evidence Quality |
| DA-006-iter2 | Three Principles section retains parallel structure LLM tell | Minor | Lines 69-75: Three paragraphs, each beginning with a bolded imperative phrase, each followed by explanatory text of similar length. Less rigid than draft-5's `**1. Phrase.**` pattern but still identifiable as structured-list-in-prose. | Internal Consistency |
| DA-007-iter2 | "Training-data regurgitation" phrasing slightly misleading | Minor | Line 40: "You want grounded evidence, not training-data regurgitation." Implies the model can bypass training data entirely. It cannot. The model always generates from learned distributions. The evidence constraint shifts what the model considers acceptable completions, making it more likely to surface verifiable claims. | Methodological Rigor |
| DA-008-iter2 | "I dare you" closing is genre-dependent risk | Minor | Line 95: "I dare you." Works for the McConkey persona. May read as LinkedIn-influencer signoff to a subset of the technical audience. Persona-justified retention. | Actionability |

---

## Finding Details

### DA-001-iter2: Level 3 assumes tool-enabled models [MAJOR]

**Claim Challenged:** The Level 3 prompt example (lines 35-36) instructs the model to "Do two things in parallel: gap analysis on this repo, and research the top 10 industry frameworks using real sources, not training data." The article then claims in "Why This Works on Every Model" (line 63) that these principles apply universally.

**Counter-Argument:** "Gap analysis on this repo" requires file system access. "Research using real sources, not training data" implies web search or retrieval-augmented generation. These are tool-use capabilities present in some deployments (Claude Code, ChatGPT with browsing, Cursor) but absent from others (API calls without tools, local Llama, most open-source chat interfaces). A reader using a plain chat interface who follows the Level 3 template will get hallucinated file analysis and fabricated citations, then conclude the article is wrong. The universality claim in "Why This Works on Every Model" is factually correct for the underlying principles (structure improves output) but the Level 3 example requires capabilities the article does not disclose.

**Evidence:** Lines 35-36 (Level 3 prompt), line 63 ("every model, regardless of architecture, performs better when you give it structure"). The citations companion document does not address this tooling distinction.

**Impact:** A practitioner following the Level 3 example without tool-enabled models will fail and attribute the failure to the article's advice rather than to their environment. This undermines the article's credibility for the exact audience it targets.

**Dimension:** Completeness (missing prerequisite information for Level 3)

**Response Required:** Add a brief qualifier either within Level 3 or in "Why This Works on Every Model" that acknowledges the tool-access requirement. Something like: "Level 3 works best when the model can access your files and search for sources. In a plain chat window, feed the repo contents directly and verify citations yourself." This preserves the principle while being honest about prerequisites.

**Acceptance Criteria:** One sentence acknowledging that Level 3's parallel research and repo analysis assumes tool access, with a fallback for tool-less environments.

---

### DA-002-iter2: Error-compounding claim creates practice-preaching inconsistency [MAJOR]

**Claim Challenged:** Lines 45: "One more thing that bites hard: once bad output enters a multi-phase pipeline, it doesn't just persist. It compounds. Each downstream phase takes the previous output at face value and adds another layer of polished-sounding analysis on top. By phase three, the whole thing looks authoritative. The errors are structural. It's not garbage in, garbage out. It's garbage in, increasingly polished garbage out, and you genuinely cannot tell the difference until something downstream breaks."

**Counter-Argument:** The article's central thesis is that structured prompting with evidence requirements produces better output. It tells readers to demand citations, show reasoning, and verify claims. Yet this specific claim -- one of the article's strongest rhetorical moments -- is delivered with zero evidence. No citation. No concrete example. No quantification of "compounds." The article practices the exact behavior it tells readers to avoid: making an authoritative-sounding claim backed by assertion rather than evidence.

This is not a factual error. Error propagation in multi-phase LLM pipelines is real and documented (Arize AI 2024 on cascading errors in LLM pipelines; DeepMind on multi-agent error amplification). The issue is that the article's own credibility standard (demand evidence, show your reasoning) is violated by one of its most prominent claims. A careful reader who has internalized the article's lessons will notice this inconsistency.

**Evidence:** Lines 45 (the claim), lines 13-14 (Level 1 example tells readers not to accept uncited output), line 27 (Level 2 example requires "cite the original source"), lines 35-36 (Level 3 requires "citations and references").

**Impact:** The practice-preaching gap is detectable by the article's target audience (people learning to be more rigorous with LLMs). It does not invalidate the article, but it creates a vulnerability to the critique "this article doesn't follow its own advice."

**Dimension:** Internal Consistency (tension between evidence-demanding thesis and evidence-free claim)

**Response Required:** Either (a) add a brief citation or concrete example grounding the error-compounding claim, or (b) soften the framing from assertion to observation: "In my experience, weak output in early phases tends to propagate..." Option (a) is stronger; option (b) is more in voice.

**Acceptance Criteria:** The error-compounding passage either cites a source, provides a concrete example, or is framed as practitioner observation rather than established fact.

---

## Recommendations

### P1 (Major -- SHOULD resolve; require justification if not)

1. **DA-001-iter2:** Add one sentence acknowledging Level 3's tool-access assumption. Suggested location: after the Level 3 prompt example or within "Why This Works on Every Model." Acceptance criteria: reader using a plain chat interface understands what they need to adjust.

2. **DA-002-iter2:** Ground the error-compounding claim with either a citation, a concrete example, or an explicit framing as practitioner observation. Suggested location: inline within the existing paragraph. Acceptance criteria: the claim no longer reads as unsupported assertion in an article that demands evidence.

### P2 (Minor -- MAY resolve; acknowledgment sufficient)

3. **DA-003-iter2:** Context window growth description could note the step-function trajectory rather than implying smooth growth. Acknowledgment sufficient.

4. **DA-004-iter2:** The two-session pattern's cost acknowledgment could include one practical failure mode (e.g., "If your plan doesn't specify what 'done' looks like for each phase, the executor will fill in its own definition"). Acknowledgment sufficient.

5. **DA-005-iter2:** Error-compounding claim would benefit from quantification or citation. Overlaps with DA-002-iter2; resolving DA-002 resolves this as well.

6. **DA-006-iter2:** Three Principles section could break parallel structure further. The current version is significantly improved from draft-5. Acknowledgment sufficient.

7. **DA-007-iter2:** "Training-data regurgitation" could be rephrased to "generic pattern completion" or similar. Acknowledgment sufficient.

8. **DA-008-iter2:** "I dare you" closing is a persona choice. No action required; retained as documented decision.

---

## Scoring Impact

| Dimension | Weight | Score | Rationale |
|-----------|--------|-------|-----------|
| Completeness | 0.20 | 0.91 | Covers all three levels with clear progression. Level 2 is well-developed as the primary recommendation. Missing: tool-access prerequisite for Level 3 (DA-001-iter2). No discussion of when structured prompting is overkill (addressed indirectly by "You don't need a flight plan for the bunny hill" and Level 2 sufficiency framing). Strong checklist. Two-session pattern well-explained. |
| Internal Consistency | 0.20 | 0.92 | Self-critique tension now explicitly acknowledged (Issue 7 resolved). McConkey perspective consistent (Issue 8 resolved). Liu et al. citation correctly applied (Issue 2 resolved). Remaining tension: error-compounding claim lacks the evidence rigor the article demands of readers (DA-002-iter2). Three Principles section retains mild parallel structure (DA-006-iter2). |
| Methodological Rigor | 0.20 | 0.93 | Three-level framework is pedagogically sound. Claims are now grounded: fluency-competence gap supported by Bender & Koller + Sharma et al.; Liu et al. correctly characterized; Wei et al. properly cited for chain-of-thought; Panickssery et al. for self-evaluation bias. "Training-data regurgitation" phrasing is slightly imprecise (DA-007-iter2) but the mechanism explanation is accurate. |
| Evidence Quality | 0.15 | 0.91 | Dramatic improvement from draft-5 (0.68 to 0.91). Four named citations with specific findings described. Citations companion document provides full bibliographic detail. Error-compounding claim still uncited (DA-005-iter2). Context window growth is factually accurate though presented as continuous rather than step-function (DA-003-iter2). |
| Actionability | 0.15 | 0.96 | Article's strongest dimension. Three levels are clear and progressive. Level 2 prompt is immediately copy-pasteable. Five-item checklist is concrete. Two-session pattern is practical. "Start with Level 2, graduate to Level 3" provides a clear path. Minor gap: two-session pattern cost underdeveloped (DA-004-iter2). |
| Traceability | 0.10 | 0.90 | Massive improvement from draft-5 (0.55 to 0.90). Four named citations inline. Citations companion provides full bibliographic trail with URLs. Claim-to-source mapping in companion is comprehensive. Missing: error-compounding claim has no trace. No inline links (appropriate for the format; companion handles this). |

---

## Additional Criteria

| Criterion | Score | Rationale |
|-----------|-------|-----------|
| LLM-Tell Detection | 0.88 | Significant improvement from draft-5 (0.78). Most tells eliminated. Remaining: Three Principles section retains a recognizable parallel-paragraph structure (DA-006-iter2), though it is far less rigid than the `**1. Phrase.**` pattern from draft-5. The bullet list under Level 3 (lines 39-43) uses varied sentence structure and lengths, which disrupts the uniform-bullet tell. "Not out of laziness. Out of probability distributions." (line 71) could be read as the "That's not X. It's Y." pattern but it is doing genuine analytical work here, distinguishing mechanism from anthropomorphization. The prose reads natural throughout the informal sections. Technical paragraphs maintain voice better than draft-5. No double-dashes, no em-dashes used as structural crutches, minimal hedging. |
| Voice Authenticity | 0.91 | Strong throughout. "Point Downhill and Hope" heading: excellent. "You don't need a flight plan for the bunny hill" line 29: authentic McConkey register. "One more thing that bites hard" line 45: natural transition. "Here's the tension" line 42: honest, direct, shows the narrator working through a real problem rather than asserting conclusions. Technical explanations now integrated with voice rather than dropping into lecture mode. "The guy looked completely unhinged on the mountain. He wasn't." (line 7): punchy, specific, earns the metaphor. Closing callback to McConkey (line 91) lands cleanly. The dare (line 95) is in-character. Minor drops: lines 65-66 ("They've grown significantly over the past few years") is generic phrasing that any writer would produce; not distinctively McConkey. Lines 71-75 (Three Principles) are competent technical writing but the imperative-phrase-then-explain structure is not how McConkey would deliver principles -- he would illustrate through example rather than enumerate through rules. |

---

## Composite Score

| Dimension | Weight | Score | Weighted |
|-----------|--------|-------|----------|
| Completeness | 0.20 | 0.91 | 0.182 |
| Internal Consistency | 0.20 | 0.92 | 0.184 |
| Methodological Rigor | 0.20 | 0.93 | 0.186 |
| Evidence Quality | 0.15 | 0.91 | 0.137 |
| Actionability | 0.15 | 0.96 | 0.144 |
| Traceability | 0.10 | 0.90 | 0.090 |
| **Weighted Composite** | **1.00** | | **0.923** |

**Band:** REVISE (0.92-0.94 per task-specified thresholds)

The composite score of 0.923 is above the standard quality gate (>= 0.92) but below the task-specified PASS threshold of >= 0.95. The article is materially improved from draft-5 (0.760 to 0.923). The two Major findings (DA-001-iter2 tool-access disclosure, DA-002-iter2 error-compounding evidence gap) are each addressable with a single sentence of revision. Resolving both would likely push Completeness to 0.93+ and Internal Consistency to 0.94+, moving the composite into the 0.93-0.94 range.

**Verdict: REVISE**

The article is close to threshold. Two targeted revisions would address the remaining Major findings:

1. Add one sentence disclosing Level 3's tool-access assumption (DA-001-iter2).
2. Ground the error-compounding claim with a citation, example, or explicit practitioner-observation framing (DA-002-iter2).

The six Minor findings are polish items that would improve the article incrementally but do not individually or collectively block acceptance.
