# Red Team Report: draft-6-iteration-2.md

**Strategy:** S-001 Red Team Analysis
**Deliverable:** `projects/PROJ-011-saucer-boy-articles/work/articles/ART-001-structured-prompting/drafts/draft-6-iteration-2.md`
**Criticality:** C3 (article deliverable, multi-iteration quality-gated, public-facing)
**Date:** 2026-02-23
**Reviewer:** adv-executor (S-001)
**H-16 Compliance:** S-003 Steelman applied in iteration-1-v2 (confirmed via `adversary-critiques/iteration-1-v2/S-003-steelman.md`)
**Threat Actor:** A senior ML practitioner who reads prompt engineering content critically, checks citations, and judges articles on whether the author practices what they preach. Goal: discredit the article's authority by finding where it fails its own standards. Capability: arXiv access, direct LLM experience, familiarity with the cited papers. Motivation: the internet is full of prompt engineering content; this article needs to earn trust or be dismissed.
**Anti-leniency:** Active. I am attacking this deliverable to find what a hostile expert reviewer would exploit.

---

## Summary

Draft-6-iteration-2 is a substantial improvement over draft-5. The revision addressed the two most critical iteration-1-v2 findings: citations have been added (Bender & Koller, Sharma et al., Wei et al., Panickssery et al., Liu et al.), and the self-critique/human-gates logical tension has been explicitly resolved. Parallel structure in bullets has been partially broken. However, the article still carries a voice-consistency gap in the technical middle, one factual precision issue with the Liu et al. citation application, and several residual LLM-tell patterns that would be visible to the target audience. I identify 7 active attack vectors (1 additional investigated and found resolved): 0 Critical, 2 Major, 3 Medium, 2 Low. Recommendation: REVISE with targeted fixes.

---

## Findings Table

| ID | Attack Vector | Category | Exploitability | Severity | Priority | Defense | Affected Dimension |
|----|---------------|----------|----------------|----------|----------|---------|-------------------|
| RT-001-iter2 | Voice register drops in technical middle sections | Degradation | Medium | Major | P1 | Partial | Internal Consistency |
| RT-002-iter2 | Liu et al. application conflates retrieval with instruction-following | Ambiguity | Medium | Major | P1 | Partial | Evidence Quality |
| RT-003-iter2 | Residual parallel structure in Level 3 bullets (lines 39-43) | Degradation | Medium | Medium | P2 | Partial | Methodological Rigor |
| RT-004-iter2 | "Next-token predictors" framing unqualified for 2026 audience | Ambiguity | Low | Medium | P2 | Missing | Methodological Rigor |
| RT-005-iter2 | Checklist items not mapped to Level 2 vs. Level 3 | Boundary | Low | Medium | P2 | Missing | Completeness |
| RT-006-iter2 | "fluency-competence gap" presentation (RESOLVED -- see details) | Ambiguity | -- | -- | -- | Fixed | Evidence Quality |
| RT-007-iter2 | "I dare you" closing remains stakes-mismatched | Degradation | Low | Low | P2 | Missing | Internal Consistency |
| RT-008-iter2 | No guidance on when Level 1 is appropriate | Boundary | Low | Low | P2 | Missing | Completeness |

---

## Finding Details

### RT-001-iter2: Voice register drops in technical middle sections [MAJOR]

**Attack Vector:** The article opens (lines 1-9) and closes (lines 91-95) in an authentic conversational register. The middle sections, particularly "Why This Works on Every Model" (lines 63-67) and parts of "The Two-Session Pattern" (lines 55-61), shift into expository technical prose. A hostile reviewer would argue: "This reads like two different writers. The intro and closing are a person talking. The middle is a textbook."

**Category:** Degradation
**Exploitability:** Medium -- any reader who notices the tonal shift will feel it, though many won't consciously identify it.
**Severity:** Major -- the McConkey persona is the article's competitive differentiator. When the voice drops out, the article competes as a generic prompt engineering explainer against hundreds of existing ones.
**Existing Defense:** Partial. Draft-6 improved this from draft-5. Line 49 ("Here's the move most people miss entirely") is a strong conversational hook that draft-5 lacked. Line 51 restores pushback language. But lines 57-58 ("It's a positional attention bias, not a simple capacity problem. Your carefully crafted instructions from message three are competing with forty messages of planning debate") are technically precise but not voiced. McConkey would not say "positional attention bias."
**Evidence:**
- Line 57: "It's a positional attention bias, not a simple capacity problem." -- This is a researcher's correction, not a practitioner's explanation.
- Line 59: "planning and execution are different modes" -- Clean but generic. No personality.
- Lines 65-66: "They've grown significantly over the past few years (GPT-3 shipped with 2K tokens in 2020; Gemini 1.5 crossed a million in 2024), but within any given model, they're hard limits you work within." -- This is a factual parenthetical. Accurate and voiceless.
- Line 67: "That finding replicates across model families, across task types, across research groups." -- Triple prepositional phrase. Clean academic summation. Not McConkey.
**Dimension:** Internal Consistency (voice register inconsistency between sections)
**Countermeasure:** Rewrite lines 57-58 to convey the same information in the article's conversational register. Example direction: instead of "positional attention bias," try something like "The model's attention isn't evenly spread across a long conversation. What you said at the start and what you said most recently get the most weight. Everything in the middle fades." The technical precision of "positional attention bias" can live in the citations companion.
**Acceptance Criteria:** No sentence in the article would sound out of place if read aloud by a confident, blunt practitioner. The academic terminology is either absent from the article body or wrapped in conversational framing.

---

### RT-002-iter2: Liu et al. application conflates retrieval with instruction-following [MAJOR]

**Attack Vector:** Line 57: "Liu et al. (2023) showed that information buried in the middle of a long context gets significantly less attention than content at the beginning or end. They called it the 'lost in the middle' effect."

The article applies this finding to explain why planning conversation debris degrades execution quality. However, Liu et al. (2023/2024) specifically tested multi-document QA and key-value retrieval tasks. The paper demonstrated that models perform worst when the answer to a retrieval question is in the middle of the context. The article extrapolates this to instruction-following degradation in conversational contexts, which is a reasonable but unvalidated inference. A senior ML researcher reviewing this article would say: "The paper was about retrieval accuracy, not instruction adherence. You're borrowing a result from one domain and applying it to another without flagging the extrapolation."

The iteration-1-v2 red team flagged this exact issue (Attack Vector 5). Draft-6 improved the description (adding "positional attention bias, not a simple capacity problem") but did not make the extrapolation explicit. The gap persists.

**Category:** Ambiguity
**Exploitability:** Medium -- only reviewers familiar with the paper would catch this, but the article's audience includes ML practitioners.
**Severity:** Major -- for an article that preaches evidence standards, applying a citation beyond its validated scope without acknowledgment undermines the article's own methodology.
**Existing Defense:** Partial. The description is now more precise ("positional attention bias"). But the application to conversational contexts is still presented as a direct conclusion of the paper rather than an extrapolation.
**Evidence:** Lines 56-57 of draft-6. The citations companion (Section 2) correctly describes the paper's actual scope ("multi-document QA and key-value retrieval") but the article body does not reflect this scoping.
**Dimension:** Evidence Quality
**Countermeasure:** Make the extrapolation explicit in the article. Example: "Liu et al. (2023) showed that models lose track of information placed in the middle of long contexts -- they called it the 'lost in the middle' effect. They tested retrieval tasks, but the principle applies here too: your instructions from message three are competing with forty messages of planning debate, and the model's attention isn't evenly distributed." One clause ("They tested retrieval tasks, but the principle applies here too") closes the gap.
**Acceptance Criteria:** The article body distinguishes between what Liu et al. measured and how the article applies the finding. The extrapolation is flagged, not hidden.

---

### RT-003-iter2: Residual parallel structure in Level 3 bullets [MEDIUM]

**Attack Vector:** Lines 39-43, the bullet list under Level 3:

> - Gap analysis and framework research are separate work streams. Not one pass at everything. Two distinct lines.
> - You want grounded evidence, not training-data regurgitation. The evidence constraint forces the model to look outward...
> - Self-critique against dimensions you defined. Not the model's own vague sense of "good enough"...
> - Human checkpoints break the self-congratulatory loop. Here's the tension...
> - Plan before product. You evaluate the process before committing to the output.

Draft-6 expanded these from the terse draft-5 bullets, which is good. But the structure is still patterned: each bullet opens with a short declarative fragment, then elaborates. Bullets 1, 2, 3, and 5 all start with a noun phrase. The first three are roughly the same length in their opening clause. This is less metronomic than draft-5 but still detectably parallel for a reader who works with LLM output.

The iteration-1-v2 red team flagged this (Attack Vector 1, Evidence C). Draft-6 partially addressed it -- bullet 4 is now substantially longer and contains a citation -- but the opening pattern of each bullet remains uniform.

**Category:** Degradation
**Exploitability:** Medium -- visible to LLM-aware readers, invisible to general audience.
**Severity:** Medium -- the article's audience works with LLMs. Some will recognize the pattern.
**Existing Defense:** Partial. Bullet 4 breaks the pattern with extended explanation and citation.
**Evidence:** Lines 39-43 exhibit a noun-phrase-opener pattern across 4 of 5 bullets.
**Dimension:** Methodological Rigor (an LLM-tell-cleaned article should not retain detectable LLM formatting patterns)
**Countermeasure:** Vary the opening syntax. Make bullet 1 a question ("Why two work streams instead of one pass?"). Start bullet 3 with the citation reference instead of the declarative. Or convert the bullets into a paragraph with natural subordination.
**Acceptance Criteria:** No more than 2 consecutive bullets share the same syntactic opening pattern.

---

### RT-004-iter2: "Next-token predictors" framing unqualified for 2026 [MEDIUM]

**Attack Vector:** Line 17: "These models are next-token predictors trained on billions of documents."

This was flagged in iteration-1-v2 (Attack Vector 4). The draft has not changed this claim. In 2026, frontier models incorporate RLHF, constitutional AI training, chain-of-thought fine-tuning, tool use, and multimodal capabilities. Calling them "next-token predictors" is reductive. The claim serves a rhetorical purpose (explaining why vague prompts produce generic output), but it describes base model behavior, not instruction-tuned model behavior. An instruction-tuned model does not merely produce "the most probable generic response from their training distribution" -- its training explicitly optimizes for instruction-following. The failure mode the article describes (generic output from vague prompts) is real but the mechanism is more nuanced.

**Category:** Ambiguity
**Exploitability:** Low -- most readers will accept the simplification; ML practitioners may not.
**Severity:** Medium -- the article's audience includes people who know about RLHF.
**Existing Defense:** Missing. No qualification added since draft-5.
**Evidence:** Line 17 and the surrounding paragraph.
**Dimension:** Methodological Rigor
**Countermeasure:** Add a qualifying clause. Example: "At their core, these models predict the next token based on everything before it. Post-training techniques like RLHF shape that behavior, but when your instructions leave room for interpretation, the prediction mechanism is what fills the gaps." This preserves the rhetorical point while acknowledging 2026 reality.
**Acceptance Criteria:** The article acknowledges that modern models are more than base next-token predictors while maintaining the explanatory point about why vague prompts produce generic output.

---

### RT-005-iter2: Checklist items not mapped to Level 2 vs. Level 3 [MEDIUM]

**Attack Vector:** Lines 82-87, the "Start Here" checklist:

```
[ ] Did I specify WHAT to do (not just the topic)?
[ ] Did I tell it HOW I'll judge quality?
[ ] Did I require evidence or sources?
[ ] Did I ask for the plan BEFORE the product?
[ ] Am I in a clean context (or carrying planning baggage)?
```

Line 89 says: "You don't need to go full orchestration right away. Just adding 'show me your plan before you execute, and cite your sources' to any prompt will change what you get back. Start with Level 2. Work up to Level 3 when the stakes justify it."

Items 4 and 5 (plan before product, clean context) are Level 3 techniques. The article tells the reader to start with Level 2, but the checklist presents all five items as a flat list. A reader who takes the "start with Level 2" advice and then hits the checklist does not know which items are baseline and which are advanced.

This was flagged in iteration-1-v2 (Attack Vector 7, LOW). It has not been addressed. Promoting to MEDIUM because the checklist is the article's primary actionable takeaway and its ambiguity directly contradicts the article's core advice ("constrain the work" -- the checklist itself is unconstrained).

**Category:** Boundary
**Exploitability:** Low -- most readers will figure it out from context.
**Severity:** Medium -- the checklist is the article's call to action; internal inconsistency here undermines the framework.
**Existing Defense:** Missing.
**Evidence:** Lines 82-89.
**Dimension:** Completeness
**Countermeasure:** Annotate the checklist. Example: add "These first three are your Level 2 baseline:" before items 1-3 and "These two are for Level 3, when the work has consequences:" before items 4-5. Or restructure as two separate checklists.
**Acceptance Criteria:** A reader can determine which checklist items apply at Level 2 and which apply at Level 3 without inferring from surrounding text.

---

### RT-006-iter2: "Fluency-competence gap" presentation [RESOLVED]

**Status:** RESOLVED in draft-6-iteration-2.

The iteration-1-v2 red team (Attack Vector 3) flagged that "fluency-competence gap" was presented as a canonical term ("It's called the 'fluency-competence gap'") without a formal source. Draft-6 addressed this comprehensively:

1. Changed framing from "It's called" to "I call it" -- attributing the term to the author rather than claiming it as established nomenclature.
2. Added an explicit bridge: "The underlying phenomenon is well-documented."
3. Cited Bender & Koller (2020) and Sharma et al. (2024) as evidence for the underlying phenomenon, clearly separated from the term itself.

Line 19: "I call it the fluency-competence gap. The underlying phenomenon is well-documented: Bender and Koller (2020) showed that models trained on linguistic form alone don't acquire genuine understanding, and Sharma et al. (2024) found that RLHF-trained models systematically produce authoritative-sounding responses regardless of factual accuracy."

This implementation cleanly separates the author's coined term from the cited research. A reader can distinguish between the label (author's) and the evidence (researchers'). No further action needed.

---

### RT-007-iter2: "I dare you" closing remains stakes-mismatched [LOW]

**Attack Vector:** Line 95: "I dare you."

Flagged in iteration-1-v2 (Attack Vector 8, LOW). The dare was not in draft-4 (the human rewrite). In the context of "write three things before your next prompt," the dare is stakes-mismatched with McConkey's real persona, where dares involved physical risk. The preceding sentence ("Do that once and tell me it didn't change the output") is already a strong close.

**Category:** Degradation
**Exploitability:** Low -- tonal preference.
**Severity:** Low -- does not affect technical quality.
**Existing Defense:** Missing. No change from draft-5.
**Evidence:** Line 95. Draft-4 closed without the dare.
**Dimension:** Internal Consistency (minor voice authenticity issue)
**Countermeasure:** Remove the line, or replace with something warmer. The preceding sentence is a better close.
**Acceptance Criteria:** Closing challenge is proportional to the action being challenged.

---

### RT-008-iter2: No guidance on when Level 1 is appropriate [LOW]

**Attack Vector:** The article describes Level 1 as a failure mode ("Point Downhill and Hope") but never says when it is perfectly appropriate. Line 29 ("You don't need a flight plan for the bunny hill") dismisses lower-stakes work without defining what qualifies. A reader could infer that every interaction should be at least Level 2, which is impractical.

Flagged in iteration-1-v2 (Attack Vector 10, LOW). Not addressed in draft-6.

**Category:** Boundary
**Exploitability:** Low -- most readers will calibrate intuitively.
**Severity:** Low -- absence of this guidance does not undermine the article's core claims.
**Existing Defense:** Missing.
**Evidence:** Level 1 section (lines 11-19) and line 29.
**Dimension:** Completeness
**Countermeasure:** Add one sentence after line 19 or at line 29: "If you're asking a factual question, generating a quick draft you'll edit heavily, or just exploring ideas, Level 1 is fine. Structure the prompt when the output matters."
**Acceptance Criteria:** The article acknowledges that unstructured prompting is appropriate for some use cases.

---

## Iteration-1-v2 Fix Assessment

| Iter-1-v2 Finding | Severity Then | Status in Draft-6 | Assessment |
|---|---|---|---|
| 1. Residual parallel structure (bullets) | HIGH | Partially fixed | Bullets expanded but opening-pattern parallelism persists (RT-003-iter2, demoted to MEDIUM) |
| 2. Lost human voice vs. draft-4 | HIGH | Partially fixed | Conversational hooks added (line 49, 51) but middle sections still drop voice (RT-001-iter2, demoted to MAJOR) |
| 3. "Fluency-competence gap" attribution | MEDIUM | Fixed | "I call it" + separated citations. Resolved. |
| 4. "Next-token predictors" reductive | MEDIUM | Not fixed | No qualification added (RT-004-iter2, remains MEDIUM) |
| 5. Liu et al. conflation | MEDIUM | Partially fixed | More precise description but extrapolation still implicit (RT-002-iter2, remains MAJOR) |
| 6. Self-critique contradicts human-gates | MEDIUM | Fixed | Lines 42 now explicitly frame self-critique as "first pass" with Panickssery citation. Resolved. |
| 7. Checklist-level mismatch | LOW | Not fixed | RT-005-iter2, promoted to MEDIUM |
| 8. "I dare you" performative | LOW | Not fixed | RT-007-iter2, remains LOW |
| 9. Bold-number-imperative pattern | LOW | Fixed | Three Principles restructured as paragraphs. Resolved. |
| 10. No when-to-skip-structure | LOW | Not fixed | RT-008-iter2, remains LOW |

**Summary:** 4 of 10 findings fully resolved. 3 partially addressed. 3 unchanged. Net trajectory is positive; the most impactful iteration-1-v2 findings (self-critique tension, fluency-competence attribution, bold formatting) were addressed. The remaining issues are fixable with targeted revisions.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Slight Negative | RT-005 (checklist-level mismatch) and RT-008 (missing Level-1-is-fine guidance) leave functional gaps. Both are LOW-to-MEDIUM impact. |
| Internal Consistency | 0.20 | Negative | RT-001 (voice register inconsistency) is the primary driver. The article has two registers: conversational (opening, closing, transitions) and expository (technical middle). This is the largest remaining quality gap. |
| Methodological Rigor | 0.20 | Slight Negative | RT-003 (residual parallel structure) and RT-004 (unqualified next-token framing) weaken rigor slightly. Neither is severe in isolation. |
| Evidence Quality | 0.15 | Slight Negative | RT-002 (Liu et al. conflation) is the only active evidence issue. The addition of four named citations is a major improvement from draft-5. Evidence quality has improved substantially. |
| Actionability | 0.15 | Neutral | The three-level framework, checklist, and two-session pattern remain highly actionable. RT-005 is the only gap and it is minor. |
| Traceability | 0.10 | Positive | Four new named citations (Bender & Koller, Sharma et al., Wei et al., Panickssery et al.) plus the existing Liu et al. The citations companion provides full references. This is a significant improvement from draft-5. |

---

## Quality Dimension Scores

| Dimension | Weight | Score | Justification |
|-----------|--------|-------|---------------|
| Completeness | 0.20 | 0.93 | Three-level framework complete. Two-session pattern present. Checklist present. Four named citations added. Remaining gaps: checklist-level annotation (RT-005) and when-to-skip guidance (RT-008). Minor, both low-impact. |
| Internal Consistency | 0.20 | 0.92 | Self-critique/human-gates tension resolved (Panickssery citation + explicit "first pass" framing). Voice register inconsistency between conversational bookends and expository middle remains (RT-001). Checklist-framework alignment gap persists (RT-005). No logical contradictions. |
| Methodological Rigor | 0.20 | 0.93 | Claims are now backed by five named citations. Fluency-competence gap properly framed as author's term with supporting evidence. Chain-of-thought claim supported by Wei et al. Self-evaluation bias supported by Panickssery et al. Remaining: next-token-predictor framing unqualified (RT-004), residual parallel structure detectable (RT-003). |
| Evidence Quality | 0.15 | 0.92 | Major improvement from draft-5 (0.82 in iteration-1-v2 S-014). Five named citations with full companion reference document. Liu et al. extrapolation still implicit (RT-002). All other evidence claims now supported. The article now meets the evidence standard it preaches. |
| Actionability | 0.15 | 0.95 | Three-level framework provides clear graduated entry. Level 2 and Level 3 example prompts are copy-pasteable. Two-session pattern is concrete. Checklist is usable. Closing call-to-action is direct. Only gap: checklist items not annotated by level. |
| Traceability | 0.10 | 0.93 | Five named in-text citations. Citations companion maps every claim to its source with arXiv/ACL links. Context window growth claim includes specific dates and models. The article is now traceable for every major technical claim except the "next-token predictor" characterization. |

**Weighted Composite:**

```
Completeness:         0.20 x 0.93 = 0.186
Internal Consistency: 0.20 x 0.92 = 0.184
Methodological Rigor: 0.20 x 0.93 = 0.186
Evidence Quality:     0.15 x 0.92 = 0.138
Actionability:        0.15 x 0.95 = 0.1425
Traceability:         0.10 x 0.93 = 0.093

TOTAL: 0.186 + 0.184 + 0.186 + 0.138 + 0.1425 + 0.093 = 0.9295
```

**Weighted Composite Score: 0.930**

---

## LLM-Tell Detection

**Score: 0.82**

Significant improvement from draft-5 (0.72 in iteration-1-v2 S-001).

**What improved:**
- Bold-number-imperative pattern for Three Principles removed; replaced with paragraph format.
- "[X] rather than [Y]" pattern in "Why This Works" section eliminated; bullets replaced with narrative prose.
- Level 3 bullets expanded from terse fragments into explanatory sentences.
- Opening McConkey introduction reads more naturally ("if you don't know him" is an inclusive aside a human would add).

**Residual tells:**
- Level 3 bullets (lines 39-43) still open with uniform noun-phrase declarative fragments: "Gap analysis and framework research are...", "You want grounded evidence...", "Self-critique against dimensions...", "Human checkpoints break...", "Plan before product."
- Line 67: "That finding replicates across model families, across task types, across research groups." Triple prepositional repetition is a common LLM rhetorical pattern.
- Line 71: "Every dimension you leave open, the model fills with the statistical default. Not out of laziness. Out of probability distributions." The "Not X. Out of Y." sentence fragment pattern is a known LLM construction.

**Overall:** The article is substantially cleaner than draft-5. The remaining tells are concentrated in two areas (Level 3 bullets, universality section) and would be invisible to most readers. Detectable by readers who work with LLM output daily, which includes this article's target audience.

---

## Voice Authenticity

**Score: 0.78**

Improvement from draft-5 (0.68 in iteration-1-v2 S-001).

**What improved:**
- Line 49: "Here's the move most people miss entirely." -- Strong conversational hook that draft-5 lacked.
- Lines 7-8: McConkey introduction expanded with biographical detail ("if you don't know him, was a legendary freeskier who literally competed in a banana suit and won"). This reads like someone telling you about a friend.
- Line 42: "Here's the tension" -- conversational flag that a person talking would use.
- Line 61: "If the plan can't stand alone, it wasn't detailed enough. Which is exactly why the review step matters." -- This has the cadence of someone making a point in conversation.

**What still falls short:**
- Lines 57-58: "It's a positional attention bias, not a simple capacity problem." -- Academic register. McConkey would not use this phrase.
- Lines 65-67: The "Why This Works on Every Model" section is the voice's weakest stretch. It reads like a well-informed blog post, not like a person talking. Compare to the Level 1 section (lines 15-19) which has strong conversational energy.
- Line 67: "That finding replicates across model families, across task types, across research groups." -- Academic summarization syntax.
- The article is warm and direct at the bookends. The middle technical sections are competent and voiceless. The McConkey persona operates at about 80% in the opening, 50-60% in the middle, and 90% in the closing.

**Summary:** The voice sustain improved. The worst voice-dead zones (Two-Session Pattern opening, Level 3 transitions) were addressed. The remaining gaps are in the "Why This Works" section and isolated academic-register sentences that could be rewritten in conversational language without losing precision.

---

## Overall Assessment

Draft-6-iteration-2 made meaningful progress. The four resolved findings (self-critique tension, fluency-competence attribution, bold formatting, Wei et al. citation) were among the most impactful from iteration-1-v2. Evidence Quality improved from 0.82 to 0.92 and Traceability from 0.78 to 0.93 -- these were the two weakest dimensions and are now competitive.

The two remaining MAJOR findings are both addressable with targeted line-level revisions:
1. RT-001 (voice register) needs 3-4 sentences rewritten in the middle sections to remove academic-register language.
2. RT-002 (Liu et al. conflation) needs one clause added to make the extrapolation explicit.

The MEDIUM findings (parallel structure, next-token qualification, checklist annotation, fluency-competence proximity) are individually minor and collectively fixable in a single editing pass.

**Recommended priority for next revision:**
1. Rewrite 3-4 academic-register sentences in the middle sections (RT-001)
2. Add one clause to Liu et al. paragraph flagging the extrapolation (RT-002)
3. Add next-token-predictor qualification (RT-004)
4. Annotate checklist by level (RT-005)
5. Vary Level 3 bullet opening syntax (RT-003)

---

## Verdict

| Metric | Score | Threshold |
|--------|-------|-----------|
| Weighted Composite | 0.930 | >= 0.95 PASS |
| LLM-Tell Detection | 0.82 | Supplementary |
| Voice Authenticity | 0.78 | Supplementary |

**Verdict: REVISE (0.92-0.94 band)**

The composite score of 0.930 falls in the REVISE band. The article is close to threshold. The two MAJOR findings (voice register, Liu et al. conflation) are the primary blockers. If RT-001 and RT-002 are addressed, Internal Consistency and Evidence Quality would each gain 0.01-0.02, pushing the composite above 0.95. The remaining MEDIUM and LOW findings are quality improvements that would reinforce the pass but are not individually blocking.
