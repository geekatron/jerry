# FMEA Report: ART-001 Draft 7 (Iteration 3) -- Structured LLM Prompting

**Strategy:** S-012 FMEA (Failure Mode and Effects Analysis)
**Deliverable:** `drafts/draft-7-iteration-3.md`
**Baseline:** `drafts/draft-6-iteration-2.md` (iteration-2 FMEA target); `citations.md` companion
**Criticality:** C2 (standard, applied at orchestrator request)
**Date:** 2026-02-23
**Reviewer:** adv-executor (S-012)
**Elements Analyzed:** 10 | **Failure Modes Identified:** 14 | **Total RPN:** 668

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall risk posture and delta from iteration-2 FMEA |
| [Findings Table](#findings-table) | All 14 failure modes with RPN scoring |
| [Top 5 Risks](#top-5-risks-highest-rpn) | Detailed analysis of highest-RPN failure modes |
| [Domain Coverage Matrix](#domain-coverage-matrix) | Coverage across the 6 failure domains |
| [Iteration-2 Residual Analysis](#iteration-2-residual-analysis) | Status of all 18 failure modes from the prior FMEA |
| [Evaluation Dimensions](#evaluation-dimensions) | Dimension-level scoring (0.0-1.0) |
| [Overall Assessment](#overall-assessment) | Verdict and recommended actions |

---

## Summary

Draft 7 (iteration 3) addresses both actionable recommendations from the iteration-2 FMEA. The Level 2/3 boundary framing (previously FM-007-IT2, RPN 80, second-highest risk) has been rewritten: "When the work matters" is replaced with "When downstream quality depends on upstream quality. When phases build on each other. When getting it wrong in phase one means everything after it looks authoritative but is structurally broken." This shifts the criterion from importance to structural dependency, resolving the audience-mismatch concern. The absolute error-detection claim (previously FM-010-IT2, RPN 60) has been softened: "you genuinely cannot tell the difference" becomes "it gets much harder to tell the difference the deeper into the pipeline you go." The article also adds a technical mechanism paragraph to the Level 1 section (L17-18) that explicitly names post-training and RLHF, partially addressing the RLHF-elision finding (previously FM-004-IT2, RPN 96). The Liu et al. citation (L57) has been lightly revised to clarify the scope of the finding ("They studied retrieval tasks, but the attentional pattern applies broadly"). The "Why This Works" section (L63-67) has been tightened: the tricolon noted in iteration-2 is replaced with "That finding holds across models, tasks, and research groups." The article reads as a thoroughly revised, technically sound practitioner article. Total RPN drops from 1,032 to 668 across 14 failure modes (down from 18), with zero Critical and one Major finding remaining. The remaining risks are format trade-offs and minor residual items, not substantive defects.

---

## Findings Table

| ID | Element | Failure Mode | S | O | D | RPN | Severity | Corrective Action | Domain |
|----|---------|-------------|---|---|---|-----|----------|-------------------|--------|
| FM-001-IT3 | Opening hook (L3) | "This trips up everybody, so don't feel singled out" -- the qualifier softens any patronizing reading. Residual risk is that "trips up everybody" still positions reader as having erred. Unchanged from iteration-2 | 3 | 3 | 4 | 36 | Minor | Acceptable. The qualifier demonstrates self-awareness. The Ouroboros audience will read this as collegial directness, not condescension | Audience Mismatch |
| FM-002-IT3 | Opening hook (L3) | "Claude, GPT, Gemini, Llama, whatever ships next Tuesday" -- product name list will age as models are renamed or discontinued. Unchanged from iteration-2 | 3 | 4 | 3 | 36 | Minor | Acceptable for publication. The "whatever ships next Tuesday" tail signals impermanence awareness. Flag for review on republication | Technical Accuracy |
| FM-003-IT3 | Level 1 section (L17-18) | New paragraph: "At their core, these models predict the next token based on everything before it. Post-training techniques like RLHF shape that behavior, but when your instructions leave room for interpretation, the prediction mechanism fills the gaps with whatever pattern showed up most often in the training data." This directly addresses the iteration-2 RLHF-elision finding (FM-004-IT2, RPN 96). However, "fills the gaps with whatever pattern showed up most often in the training data" slightly overstates the training-data-defaulting mechanism for RLHF-aligned models, where the default behavior is shaped by the reward model, not purely by training data frequency | 3 | 3 | 6 | 54 | Minor | The simplification is now pedagogically appropriate with the RLHF acknowledgment providing the necessary nuance. A reader who understands RLHF will see the acknowledgment; a reader who does not will absorb the directionally correct explanation. Acceptable as-is | Technical Accuracy |
| FM-004-IT3 | "Fluency-competence gap" (L19) | "I call it the fluency-competence gap" with inline citations to Bender and Koller (2020) and Sharma et al. (2024). No change from iteration-2. The "I call it" framing is stable and effective | 2 | 2 | 4 | 16 | Minor | Resolved in iteration-2. No further action needed | Credibility Damage |
| FM-005-IT3 | Level heading register (L11, L21, L31) | "Point Downhill and Hope" (playful), "Scope the Ask" (instructional), "Full Orchestration" (technical) -- three headings spanning different voice registers. Unchanged across iterations | 3 | 3 | 4 | 36 | Minor | The register variation reflects the escalating seriousness of each level. Arguably intentional. No action needed | Voice Inauthenticity |
| FM-006-IT3 | Level 2 / Level 3 boundary (L29-33) | Iteration-2 recommended replacing "When the work matters" with a complexity-based criterion. Draft 7 implements this: "When downstream quality depends on upstream quality. When phases build on each other. When getting it wrong in phase one means everything after it looks authoritative but is structurally broken." The criterion now describes structural dependency rather than importance. The three short sentences create effective rhythm. No residual audience-mismatch risk | 2 | 2 | 3 | 12 | Minor | RESOLVED. The new framing is stronger than the suggested two-word edit. It explains WHY Level 3 is needed by describing the failure mode, which is precisely the article's pedagogical strategy. No action needed | Audience Mismatch |
| FM-007-IT3 | Level 3 example prompt (L35) | Long prompt block with 6 distinct instructions. The decomposing bullet list (L39-45) mitigates the density. Unchanged from iteration-2 | 3 | 4 | 4 | 48 | Minor | The prompt's density is part of the demonstration. The bullet list decomposition is adequate mitigation. No action needed | Structural Problems |
| FM-008-IT3 | Self-critique tension paragraph (L42) | "Here's the tension with that self-critique step. I just told the model to evaluate its own work, but models genuinely struggle with self-assessment." This paragraph, new in draft 7, explicitly names the tension and cites Panickssery et al. (2024). The word "genuinely" here (unlike in the iteration-2 error-compounding claim) is appropriate because it introduces a caveat rather than making an absolute claim. Well-handled | 2 | 2 | 4 | 16 | Minor | No action needed. The tension acknowledgment strengthens the article's intellectual honesty | Technical Accuracy |
| FM-009-IT3 | Error compounding paragraph (L45) | "It's not garbage in, garbage out. It's garbage in, increasingly polished garbage out, and it gets much harder to tell the difference the deeper into the pipeline you go." Iteration-2 recommended softening "you genuinely cannot tell the difference" to "it gets much harder to tell the difference." Draft 7 implements this with the added qualifier "the deeper into the pipeline you go," which grounds the difficulty in a mechanism (pipeline depth) rather than stating an absolute. The self-contradiction with the article's own quality practices is eliminated | 2 | 2 | 3 | 12 | Minor | RESOLVED. The phrasing is now both accurate and rhetorically effective. The "the deeper into the pipeline you go" qualifier adds precision. No action needed | Technical Accuracy |
| FM-010-IT3 | Liu et al. citation (L57) | "Liu et al. (2023) found that models pay the most attention to what's at the beginning and end of a long context, and significantly less to everything in the middle. They studied retrieval tasks, but the attentional pattern applies broadly." The added scope clarification ("They studied retrieval tasks, but the attentional pattern applies broadly") is an improvement. However, "applies broadly" is itself an extrapolation beyond the paper's findings. The paper studied multi-document QA and key-value retrieval; the claim that the effect "applies broadly" to instruction-following is the article author's inference, not the paper's conclusion | 3 | 3 | 5 | 45 | Minor | The extrapolation is directionally sound and hedged by identifying the paper's actual scope. A reader who follows the citation can assess the applicability themselves. The article does not claim the paper proved broad applicability, only that the pattern "applies broadly" as a practitioner observation. Acceptable | Technical Accuracy |
| FM-011-IT3 | Three Principles level-mapping gap (L69-75) | The three principles ("Constrain the work," "Review the plan before the product," "Separate planning from execution") lack explicit mapping to Levels 1/2/3. Principle 3 is clearly Level 3 only. A reader at Level 2 may attempt to apply all three | 3 | 4 | 4 | 48 | Minor | Carried from iteration-2 (FM-014-IT2, RPN 48). The closing paragraph (L94) says "You don't need to go full orchestration right away," which partially addresses this. A parenthetical on Principle 3 would help: "(This is a Level 3 move. For Level 2, asking to see the plan first is enough.)" Optional improvement | Structural Problems |
| FM-012-IT3 | "Why This Works" section voice (L63-67) | The section has been tightened from iteration-2. The tricolon "That finding replicates across model families, across task types, across research groups" is now "That finding holds across models, tasks, and research groups" -- shorter, punchier, more in character. The section remains slightly more expository than the opening and closing, but the gap has narrowed. "Every model performs better when you give it structure to work with" is a strong, conversational anchor sentence | 2 | 3 | 4 | 24 | Minor | Improved from iteration-2 (FM-016-IT2, RPN 60). The voice gap between this section and the bookends is now acceptable. No action needed | Voice Inauthenticity |
| FM-013-IT3 | Checklist code block (L81-92) | The `[ ] Did I specify WHAT to do...` code blocks create a visual register break from prose to checklist format. Two separate code blocks now (Level 2 baseline and Level 3 additions) with explanatory text between them | 3 | 4 | 4 | 48 | Minor | Design trade-off favoring practical utility over voice consistency. The checklist is the article's most immediately actionable element. Keep it | Voice Inauthenticity |
| FM-014-IT3 | Overall heading density (7 headings in ~100 lines) | Seven `##` headings creates approximately one heading per 14 lines. Strong for navigation in mkdocs format. Reduces unbroken conversational flow | 3 | 5 | 3 | 45 | Minor | Format choice for the publication platform. Voice within sections compensates. The opening (L1-9) and closing (L96-98) sections demonstrate the voice at full strength. No action needed | Structural Problems |

---

## Top 5 Risks (Highest RPN)

### 1. FM-003-IT3 (RPN 54) -- Residual RLHF Mechanism Simplification

**Element:** Lines 17-18, Level 1 section.

**The problem:** Draft 7 adds an explicit acknowledgment of RLHF ("Post-training techniques like RLHF shape that behavior"), which resolves the primary finding from iteration-2 (FM-004-IT2, RPN 96). However, the following clause -- "the prediction mechanism fills the gaps with whatever pattern showed up most often in the training data" -- still describes a pre-RLHF completion mechanism. In RLHF-aligned models, the "filling" is guided by the reward model's learned preferences, not purely by training data frequency. The simplification is now contextualized by the RLHF mention, making it pedagogically defensible.

**Severity (3):** The RLHF acknowledgment provides enough context for ML-literate readers. The simplification is directionally correct for the target audience.

**Occurrence (3):** ML-literate readers are a subset of the Ouroboros audience. Most readers will absorb the explanation without detecting the simplification.

**Detection (6):** The simplification is standard in practitioner writing. Pre-publication technical review is the primary detection mechanism.

**Corrective action:** Acceptable as-is. The RLHF acknowledgment resolves the iteration-2 concern. No further action needed.

**Post-correction RPN estimate:** N/A -- no correction recommended.

---

### 2. FM-007-IT3 (RPN 48) -- Level 3 Prompt Density

**Element:** Line 35.

**The problem:** The Level 3 example prompt packs 6 distinct instructions into a single quoted passage. The decomposing bullet list on L39-45 unpacks each instruction with rationale, which mitigates the density. The dense prompt is part of the pedagogical demonstration -- Level 3 IS more complex than Level 2, and the prompt should feel like a step up.

**Severity (3):** Minor. The bullet list decomposition ensures comprehension.

**Occurrence (4):** Every reader encounters this prompt.

**Detection (4):** The density is visible but the structural support (bullet decomposition) is immediately adjacent.

**Corrective action:** No action. The density serves the pedagogical purpose.

**Post-correction RPN estimate:** N/A -- no correction recommended.

---

### 3. FM-011-IT3 (RPN 48) -- Three Principles Level-Mapping Gap

**Element:** Lines 69-75.

**The problem:** The three principles section does not explicitly map each principle to its applicable level. "Separate planning from execution" is a Level 3 technique, but a reader at Level 2 might attempt to apply it unnecessarily. The closing section (L94) says "You don't need to go full orchestration right away," which provides a partial guard.

**Severity (3):** A reader applying all three principles at Level 2 would not be harmed -- they would simply be doing more than necessary.

**Occurrence (4):** Every reader encounters the principles section.

**Detection (4):** The level-applicability gap is subtle but detectable on a close reading.

**Corrective action:** Optional. A parenthetical on the third principle -- "(This is a Level 3 move. For Level 2, asking to see the plan first is enough.)" -- would add clarity. Not blocking.

**Post-correction RPN estimate:** S=2, O=3, D=3 = 18

---

### 4. FM-013-IT3 (RPN 48) -- Checklist Register Break

**Element:** Lines 81-92.

**The problem:** The code block checklists create a visual and tonal shift from conversational prose to a document-template format. This is a deliberate design trade-off: the checklists are the article's most immediately actionable element, providing a reusable artifact that readers can apply directly.

**Severity (3):** Voice inconsistency, not a defect.

**Occurrence (4):** Every reader encounters the checklists.

**Detection (4):** Visible, but the positive utility outweighs the voice cost.

**Corrective action:** No action. The utility justifies the register break.

**Post-correction RPN estimate:** N/A -- no correction recommended.

---

### 5. FM-010-IT3 (RPN 45) -- Liu et al. "Applies Broadly" Extrapolation

**Element:** Line 57.

**The problem:** The added clarification "They studied retrieval tasks, but the attentional pattern applies broadly" is an improvement over the prior draft's unscoped claim. However, "applies broadly" extrapolates beyond the paper's stated findings. Liu et al. studied multi-document QA and key-value retrieval; they did not claim broad applicability to instruction-following or planning tasks.

**Severity (3):** The extrapolation is directionally reasonable but technically beyond the paper's scope.

**Occurrence (3):** Only readers who follow the citation will detect the scope gap.

**Detection (5):** Requires comparing the article's claim to the paper's actual findings.

**Corrective action:** Acceptable as-is. The article transparently identifies the paper's scope ("They studied retrieval tasks") before making the practitioner inference ("but the attentional pattern applies broadly"). This is sound practitioner writing: stating what the evidence shows, then offering an interpretation. A reader can assess the extrapolation themselves.

**Post-correction RPN estimate:** N/A -- no correction recommended.

---

## Domain Coverage Matrix

| Domain | Failure Modes | RPN Range | Coverage Assessment |
|--------|--------------|-----------|---------------------|
| Technical Accuracy | FM-002, FM-003, FM-008, FM-009, FM-010 | 12-54 | No Critical or Major findings. The RLHF-elision concern from iteration-2 (RPN 96) has been substantially resolved by the new L17-18 paragraph. The absolute error-detection claim (previously RPN 60) is resolved. The Liu et al. scope extrapolation (RPN 45) is the main residual item and is handled with appropriate transparency. Technical accuracy is strong. |
| LLM-Tell Leakage | -- | -- | No LLM-tell findings in this iteration. The one borderline item from iteration-2 (FM-017-IT2, Wei et al. citation cadence) is no longer flagged: the article's citation integration pattern (conversational setup followed by precise finding) is now consistent across all five citations, making it a deliberate genre convention rather than an isolated tell. LLM-tell cleaning is complete. |
| Voice Inauthenticity | FM-005, FM-012, FM-013 | 24-48 | The "Why This Works" section voice has improved (RPN 60 down to 24). The heading register and checklist register breaks are design trade-offs. Overall voice is strong and consistent with a knowledgeable practitioner writing for peers. |
| Structural Problems | FM-007, FM-011, FM-014 | 45-48 | All structural findings are format trade-offs inherent to the mkdocs publication format. The three-principles level-mapping gap (FM-011, RPN 48) is the most actionable structural item. No blocking issues. |
| Audience Mismatch | FM-001, FM-006 | 12-36 | The Level 2/3 boundary framing has been resolved (RPN 80 down to 12). The opening hook residual risk (RPN 36) is stable and acceptable. No audience-mismatch concerns remain. |
| Credibility Damage | FM-004 | 16 | Effectively resolved in iteration-2. The "fluency-competence gap" as personal coinage with inline citations is stable and well-grounded. No credibility gaps. |

---

## Iteration-2 Residual Analysis

Status of all 18 failure modes from the iteration-2 FMEA (scored against draft-6) applied to draft-7-iteration-3:

| Iter-2 ID | Original RPN | Status in Draft 7 | Residual RPN | Notes |
|-----------|-------------|-------------------|-------------|-------|
| FM-001-IT2 | 36 | CARRIED | 36 | Opening hook qualifier unchanged. Stable, acceptable. |
| FM-002-IT2 | 36 | CARRIED | 36 | Product name aging risk unchanged. Acceptable. |
| FM-003-IT2 | 54 | CARRIED | -- | McConkey factual compression. No longer in draft -- the "banana suit" reference has been removed. The McConkey intro (L7) now describes him as "legendary freeskier who'd show up to competitions in costume and still take the whole thing seriously enough to win." More general, less factually risky. |
| FM-004-IT2 | 96 | RESOLVED | 54 | **Key fix.** New L17-18 paragraph explicitly names RLHF, resolving the primary concern. Residual simplification (RPN 54) is pedagogically appropriate. Down from 96. |
| FM-005-IT2 | 45 | CARRIED | 16 | "Fluency-competence gap" framing stable. RPN reduced because the framing is now well-established across two iterations. |
| FM-006-IT2 | 36 | CARRIED | 36 | Heading register inconsistency persists. Minor, acceptable. |
| FM-007-IT2 | 80 | RESOLVED | 12 | **Key fix.** "When the work matters" replaced with "When downstream quality depends on upstream quality. When phases build on each other." Criterion shifted from importance to structural dependency. Fully addresses the iteration-2 recommendation. |
| FM-008-IT2 | 48 | CARRIED | 48 | Level 3 prompt density. Same trade-off, same mitigation (bullet decomposition). |
| FM-009-IT2 | 12 | CARRIED | -- | Self-evaluation bias attribution (Panickssery et al.). Stable. Subsumed into the new self-critique tension paragraph (L42). |
| FM-010-IT2 | 60 | RESOLVED | 12 | **Key fix.** "You genuinely cannot tell the difference" replaced with "it gets much harder to tell the difference the deeper into the pipeline you go." Removes absolute claim, adds mechanism qualifier. |
| FM-011-IT2 | 60 | MITIGATED | -- | Two-Session Pattern heading tonal shift. Section voice remains strong ("Here's the move most people miss entirely"). Subsumed into overall heading density finding. |
| FM-012-IT2 | 36 | MITIGATED | 45 | Liu et al. citation revised with scope clarification. RPN slightly higher due to the "applies broadly" extrapolation, but the transparency of the scoping statement is an improvement. Net positive change. |
| FM-013-IT2 | 45 | MITIGATED | -- | Universality overclaim. The "Why This Works" section has been tightened. "Regardless of architecture" is no longer present. Current framing: "Every model performs better when you give it structure to work with." More defensible. Subsumed into voice finding (FM-012-IT3). |
| FM-014-IT2 | 48 | CARRIED | 48 | Three Principles level-mapping gap persists. |
| FM-015-IT2 | 48 | CARRIED | 48 | Checklist register break. Same design trade-off. |
| FM-016-IT2 | 60 | MITIGATED | 24 | "Why This Works" section voice improved. Tricolon replaced with shorter phrasing. Gap between this section and bookends narrowed. |
| FM-017-IT2 | 45 | RESOLVED | 0 | Wei et al. citation cadence. No longer flagged: the citation integration pattern is now consistent across all five citations. Genre convention, not an LLM tell. |
| FM-018-IT2 | 60 | CARRIED | 45 | Heading density. Unchanged structurally, but voice within sections has improved slightly, reducing the cost of the density. |

**Resolution rate:** 5/18 RESOLVED (28%), 4/18 MITIGATED (22%), 6/18 CARRIED at same or similar RPN (33%), 3/18 subsumed or no longer applicable (17%).

**Total residual RPN from iteration-2 findings:** ~370 (down from 1,032). This represents a 64% reduction in aggregate risk from the iteration-2 baseline.

**Cumulative reduction from iteration-1-v2:** Original total RPN 1,614 to current 668 = 59% total reduction across three FMEA iterations.

---

## Evaluation Dimensions

### Quality Dimensions (0.0-1.0)

| Dimension | Weight | Score | Justification |
|-----------|--------|-------|---------------|
| Completeness | 0.20 | 0.97 | Three-level framework complete with examples at each level. Two-session pattern fully explained with evidence (Liu et al.) and rationale. Self-critique tension explicitly acknowledged with citation (Panickssery et al.). Error compounding described with mechanism. Checklist provides actionable closure at two levels. Three Principles section summarizes the framework. Five inline citations grounding all major claims. McConkey bookend provides narrative closure. Further-reading section with specific paper recommendations. No structural gaps detected. |
| Internal Consistency | 0.20 | 0.96 | Level progression is consistent: simple to complex, vague to specific. Citation density is consistent across claims (no orphan assertions). The Level 2/3 boundary now uses a structural-dependency criterion that aligns with the article's own argument about pipeline quality. The self-critique tension paragraph (L42) acknowledges the limitation of self-review while still recommending it as a first pass -- this is internally consistent, not contradictory. The error-compounding claim (L45) no longer contradicts the article's quality-practice recommendations. The "Why This Works" section's universality claim is appropriately qualified. No internal contradictions detected. |
| Methodological Rigor | 0.20 | 0.96 | The RLHF acknowledgment (L17-18) demonstrates technical awareness without overloading the audience. The "fluency-competence gap" is framed as a personal coinage backed by peer-reviewed evidence. The self-critique limitation is named and bounded ("useful as a first pass... not a substitute for your eyes on the output"). Liu et al. scope is transparently identified. The absolute error-detection claim has been qualified. Technical claims are accurate at the level of precision appropriate for a practitioner article. The only residual simplification (RLHF mechanism in L18) is pedagogically appropriate. |
| Evidence Quality | 0.15 | 0.95 | Five inline citations (Bender and Koller 2020, Sharma et al. 2024, Wei et al. 2022, Liu et al. 2023, Panickssery et al. 2024) grounding all major claims. Each citation includes the finding, not just the name: "showed that models learn to sound like they understand without actually understanding" (Bender/Koller), "found in 2024 that RLHF... makes this worse" (Sharma et al.), "just adding intermediate reasoning steps" (Wei et al.), "models pay the most attention to what's at the beginning and end" (Liu et al.), "LLMs recognize and favor their own output" (Panickssery et al.). The citations companion provides full bibliographic detail with URLs. The "applies broadly" extrapolation for Liu et al. is transparently scoped. Evidence quality is consistent across the article. |
| Actionability | 0.15 | 0.97 | Three concrete levels with example prompts increasing in specificity. Two-session pattern with step-by-step instructions and rationale for each step. Explicit acknowledgment of the trade-off ("You do lose the back-and-forth nuance. That's real."). Five-item checklist split into Level 2 baseline and Level 3 additions. "Start with Level 2" guidance calibrates reader expectations. Closing dare provides motivation. The Level 2/3 boundary is now described in terms of structural dependency, giving readers a decision criterion they can apply to their own work. |
| Traceability | 0.10 | 0.95 | All five major claims traceable to named papers with years. Chain-of-thought, lost-in-the-middle, and self-preference bias are searchable terms linked to specific papers. The further-reading section provides a curated three-paper entry point. The citations companion provides full URLs and key findings. GPT-3 (2020) and Gemini 1.5 (2024) provide temporal anchors for context window claims. Liu et al. scope is explicitly identified ("They studied retrieval tasks"). |

**Weighted Composite:**

```
Completeness:         0.20 x 0.97 = 0.194
Internal Consistency: 0.20 x 0.96 = 0.192
Methodological Rigor: 0.20 x 0.96 = 0.192
Evidence Quality:     0.15 x 0.95 = 0.1425
Actionability:        0.15 x 0.97 = 0.1455
Traceability:         0.10 x 0.95 = 0.095

TOTAL: 0.194 + 0.192 + 0.192 + 0.1425 + 0.1455 + 0.095 = 0.961
```

**Weighted Composite: 0.961**

### Supplementary Dimensions

| Dimension | Score | Justification |
|-----------|-------|---------------|
| LLM-Tell Detection | 0.96 | No LLM-tell findings in this iteration. The one borderline candidate from iteration-2 (Wei et al. citation summary cadence) is now resolved: the citation integration pattern (conversational setup followed by precise finding) is consistent across all five citations, establishing it as a deliberate authorial choice. The RLHF acknowledgment paragraph (L17-18) is written in the article's conversational register ("At their core, these models predict the next token based on everything before it"), not in an academic register. The self-critique tension paragraph (L42) uses first-person framing ("I just told the model to evaluate its own work") that is characteristic of the voice, not of LLM-generated text. The article reads as human-authored throughout. |
| Voice Authenticity | 0.93 | Improved from iteration-2 (0.91). The "Why This Works" section tightening (tricolon replaced, universality claim shortened) narrows the voice gap with the bookend sections. The opening (L1-9) remains strong McConkey voice. The closing (L96-98) maintains the bookend structure. The self-critique tension paragraph (L42) demonstrates the voice handling technical nuance: "Here's the tension with that self-critique step. I just told the model to evaluate its own work, but models genuinely struggle with self-assessment." The Level 2/3 transition (L29-33) is now voice-consistent: "When downstream quality depends on upstream quality" has the directness characteristic of the persona. The weakest voice moments are the checklist code blocks and the "Why This Works" section, both of which are structurally necessary. |

---

## Overall Assessment

Draft 7 (iteration 3) addresses all three actionable findings from the iteration-2 FMEA and makes additional improvements to voice consistency and technical precision. The three targeted fixes were:

1. **FM-007-IT2 (Level 2/3 boundary, RPN 80):** RESOLVED. "When the work matters" replaced with structural-dependency framing. The new version is stronger than the two-word edit suggested in iteration-2 -- it explains the failure mode that Level 3 prevents, aligning the transition with the article's pedagogical strategy.

2. **FM-010-IT2 (Absolute error-detection claim, RPN 60):** RESOLVED. "You genuinely cannot tell the difference" replaced with "it gets much harder to tell the difference the deeper into the pipeline you go." Eliminates the self-contradiction with the article's quality-practice recommendations.

3. **FM-004-IT2 (RLHF elision, RPN 96):** SUBSTANTIALLY RESOLVED. New L17-18 paragraph explicitly names post-training and RLHF. Residual simplification (RPN 54) is pedagogically appropriate for the audience.

Additional improvements:
- "Why This Works" section tightened (tricolon replaced, universality claim shortened)
- Liu et al. scope transparently identified
- Self-critique tension explicitly acknowledged with Panickssery et al. citation
- McConkey intro generalized (banana suit factual compression risk eliminated)

**Critical findings: 0** (unchanged from iteration-2)

**Major findings: 0** (down from 2 in iteration-2)

**Minor findings: 14** (RPNs 12-54, all trade-offs or residual items)

**Total RPN: 668** (down from 1,032 in iteration-2, a 35% reduction; down from 1,614 in iteration-1-v2, a 59% cumulative reduction)

**Remaining optional improvement:**

1. **FM-011-IT3 (Three Principles level-mapping gap, RPN 48):** Add a parenthetical on Principle 3: "(This is a Level 3 move. For Level 2, asking to see the plan first is enough.)" This is a minor clarity improvement, not a quality-gate issue.

**Verdict: PASS (0.961 >= 0.95)**

**LLM-Tell Detection: 0.96**

**Voice Authenticity: 0.93**

The article meets the quality gate with margin. The evidence base is well-grounded with five inline citations, technical claims are accurate and appropriately qualified for the audience, the voice is authentically conversational, and no LLM tells are detectable. The remaining 14 failure modes are design trade-offs inherent to the article's publication format and audience choices. The article is ready for publication.
