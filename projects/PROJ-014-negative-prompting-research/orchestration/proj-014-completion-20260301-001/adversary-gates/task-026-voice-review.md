# Voice Compliance Report

**Report ID:** task-026-voice-review
**Reviewer:** sb-reviewer v1.0.0
**Date:** 2026-03-01
**Article:** `projects/PROJ-014-negative-prompting-research/orchestration/proj-014-completion-20260301-001/articles/jerry-docs-negative-prompting.md`

---

## Summary

**Verdict:** PASS
**Text Type:** documentation
**Audience Context:** developer reading documentation
**Expected Tone (from Audience Adaptation Matrix):** Medium energy, no humor required (light and non-blocking if present), high technical depth, Clarity tone anchor. From audience-adaptation.md: "Humor should be light and non-blocking -- it adds flavor for those who want it, is skippable for those who do not."

The article passes all 5 Authenticity Tests and clears all 8 boundary conditions. The voice is not highly marked with Saucer Boy personality -- this is appropriate for the documentation context, which calls for clarity over flavor. Where personality does appear (the Executive Summary opening, the CONDITIONAL GO framing, the "worth holding onto" phrasing), it is earned and uncontrived. The information is complete, the register is consistent, and no LLM-tell markers were found at violation severity. Three minor observations are noted in the Suggested Fixes section for optional strengthening, none of which block shipment.

---

## Authenticity Test Results

| Test | Name | Verdict | Evidence |
|------|------|---------|----------|
| 1 | Information Completeness | PASS | See below |
| 2 | McConkey Plausibility | PASS | See below |
| 3 | New Developer Legibility | PASS | See below |
| 4 | Context Match | PASS | See below |
| 5 | Genuine Conviction | PASS | See below |

---

### Test 1: Information Completeness (HARD Gate)

**Verdict: PASS**

Mentally stripping all voice elements (the conversational Executive Summary opener, the "worth holding onto" phrase, the direct second-person framing in Practical Application), the remaining information completely serves the developer's need.

The article answers four questions a developer would arrive with:

1. **What did PROJ-014 find?** Covered precisely: NPT-013 achieves 100% compliance, NPT-014 is the worst formulation, the 60% claim is unestablished, CONDITIONAL GO was reached via PG-003. All four findings are present with the supporting numbers.

2. **What patterns exist and how do I use them?** The NPT Pattern Taxonomy table (14 patterns, 7 technique types) is complete and actionable. The "Two Patterns That Matter Most" section provides operational examples with code blocks. The decision table ("Deciding Between NPT-009 and NPT-013") provides a lookup that does not require judgment.

3. **How do I apply this to my own constraints?** The three-step upgrade procedure under "Upgrading Existing Constraints" gives a worked example from NPT-014 input to NPT-013 output with three binary-testable criteria.

4. **What changed in the Jerry Framework?** The ADR table, the Features Delivered table, and the `/prompt-engineering` skill section enumerate what was implemented. The "What the Research Did Not Change" section is intellectually honest about the CONDITIONAL GO scope.

No information gaps detected. A developer who arrives having never heard of this research would leave knowing what it found, why it matters, and what to do with it.

---

### Test 2: McConkey Plausibility

**Verdict: PASS**

The test is not whether the text sounds like McConkey -- the test is whether the spirit is plausible. Documentation is a low-flavor context; a McConkey who is writing framework documentation, not a powder-day pep talk, would write something like this.

The spirit is plausible in three specific locations:

- **Executive Summary opener:** "Does 'NEVER do X' work better than 'Always do Y'? PROJ-014 spent six research phases and a controlled A/B test finding out. The short answer: it depends entirely on how you write the NEVER." This is direct, slightly playful with the framing, and treats the reader as someone capable of handling a nuanced answer. McConkey respected people who could handle honest complexity.

- **CONDITIONAL GO framing:** "The A/B test reached a CONDITIONAL GO via the pre-specified PG-003 contingency pathway." The article does not oversell its own findings. The paragraph that follows states clearly that the effect size fell below the pre-registered minimum. This intellectual honesty -- not hyping the result -- is consistent with someone who actually believes the quality system.

- **"Two additional findings from the A/B test worth holding onto":** This is a small phrase but it signals genuine engagement with the material rather than list-proceeding.

The voice is not strained anywhere. No ski metaphors were deployed in a documentation context, which is correct. The plausibility test does not require personality to be highly present -- it requires that whatever personality is present does not feel forced. It does not.

---

### Test 3: New Developer Legibility

**Verdict: PASS**

There are no ski culture terms, no McConkey biographical references, and no insider vocabulary in this article. Every technical term introduced (NPT-013, NPT-009, NPT-014, CONDITIONAL GO, PG-003) is either defined in context or given a table entry that explains its meaning.

A developer who has never heard of Jerry, McConkey, or PROJ-014 would encounter no decoding barriers. The taxonomy table provides type, evidence, and recommendation for each pattern. The code block examples show the exact format in use.

The one potentially unfamiliar term to verify: "McNemar exact p=0.016" in the Key Findings section. This is statistical vocabulary, not Jerry-specific or ski-specific. A developer without statistics background might not know what McNemar is, but the surrounding context provides the plain-English interpretation: "statistically significant" and "surviving Bonferroni correction for three pairwise comparisons." The sentence does not require decoding the term to understand the finding. This is not a legibility failure.

---

### Test 4: Context Match

**Verdict: PASS**

Expected for documentation audience (Audience Adaptation Matrix, Rule explanation row): Medium energy, None/light humor, High technical depth, Clarity tone anchor.

The article delivers on all four dimensions:

- **Energy:** Medium. The Executive Summary has some conversational energy. The methodology and taxonomy sections are flat but appropriately so -- they are reference material, not narrative. The CONDITIONAL GO section has a slight uptick of intellectual engagement. No section spikes to celebration energy, and no section drops to diagnostic/hard-stop energy.

- **Humor:** None present. This is appropriate for a documentation article on a technical research topic. The absence of humor is correct for this context, not a failure.

- **Technical depth:** High. The article includes the p-value (McNemar exact 0.016), the Bonferroni-adjusted alpha (0.0167), the effect size and confidence interval (pi_d=0.078, CI 0.023-0.133), and the constraint-type breakdown for where violations concentrated. This is the right level of depth for Jerry Framework documentation.

- **Tone anchor:** Clarity. The article is organized around what-you-need-to-know and how-to-apply-it. Every section answers a clear question. The navigation table at the top is functional.

One minor note: the audience-adaptation.md guidance for documentation context mentions "depth for those who engage, irrelevant if skipped" -- the article's section structure supports this well. The pattern catalog table can be scanned without reading every row; the code examples can be copied without reading the surrounding prose.

---

### Test 5: Genuine Conviction

**Verdict: PASS**

The hardest test for documentation voice: does the text read as if someone believes what they wrote, or does it read as assembled technical content?

Two specific passages indicate genuine conviction:

**1. The treatment of the 60% claim:**
"The primary claim -- that negative prompting reduces hallucination by 60% -- has no evidential basis. A systematic search across 75 sources found zero controlled evidence for this specific effect size. The claim entered the project as a hypothesis. It is not disproven; it is simply unestablished."

This paragraph does not hedge and does not oversell. It makes a strong statement ("no evidential basis") and immediately provides the epistemically correct qualifier ("not disproven; simply unestablished"). The distinction between "unproven" and "disproven" is a meaningful one, and making it here signals that the writer understands the research methodology well enough to care about the difference. Assembled text would not bother.

**2. The CONDITIONAL GO section:**
"The A/B test reached a CONDITIONAL GO via the pre-specified PG-003 contingency pathway. The framing effect is real and statistically significant, but the effect size fell slightly below the pre-registered minimum (0.078 observed versus 0.10 threshold). That means NPT-013 adoption is justified on convention-alignment grounds -- structured negation never performs worse and demonstrably prevents violations -- not on an effectiveness-determined mandate."

This is an honest account of a finding that did not fully hit its pre-registered target. A writer who was just performing the role of "research summarizer" would have softened this or buried the effect size comparison. The writer here makes the tension explicit and names it clearly. Conviction.

---

## Boundary Condition Check

| # | Boundary | Status | Evidence |
|---|----------|--------|----------|
| 1 | NOT Sarcastic | CLEAR | No ironic register detected. The CONDITIONAL GO discussion is direct, not eye-rolling. |
| 2 | NOT Dismissive of Rigor | CLEAR | The article consistently treats the quality system as real and consequential. Quality gate scores (>= 0.92 for all research phases) are cited without apology. The CONDITIONAL GO is handled seriously. |
| 3 | NOT Unprofessional in High Stakes | CLEAR | This is documentation, not a high-stakes failure. No humor present. Appropriate. |
| 4 | NOT Bro-Culture Adjacent | CLEAR | No exclusionary language, no ironic insider references. The practical application sections are written for any developer regardless of background. |
| 5 | NOT Performative Quirkiness | CLEAR | No strained ski metaphors, no forced personality. The conversational moments are earned (Executive Summary opener) or small (the "worth holding onto" phrase). |
| 6 | NOT Character Override | CLEAR | This is framework output text, not a reasoning modifier. |
| 7 | NOT Information Replacement | CLEAR | The article is information-rich throughout. Personality is additive (where present) not substitutive. |
| 8 | NOT Mechanical Assembly | CLEAR (with minor notes) | See detail below. |

### Boundary #8 Detail: NOT Mechanical Assembly

Full LLM-tell scan conducted against all categories in `llm-tell-patterns.md`.

**Em-dash stacking:** The article uses double-hyphen (`--`) to set off parenthetical phrases, not em-dashes. The pattern appears multiple times but is used for code-style constraint formatting that is consistent with the article's subject matter (NPT constraint formats use `--` as a structural separator). Single-pair em-dash use ("NPT-013 structured negation -- a constraint format that pairs...") is within normal limits; stacking (2+ pairs per paragraph) was not found.

**Staccato emphasis pairs:** Not found. The article does not use back-to-back sub-8-word sentences as rhetorical emphasis.

**Corrective insertion ("It's not X. It's Y."):** Not found. The article handles the blunt-prohibition finding by direct assertion ("This is the single most actionable finding"), not by the negation-correction tic.

**Hedging phrases ("It's worth noting," "Importantly"):** Not found. The article's opening section commits immediately to its findings without hedging preamble. The CONDITIONAL GO section states the limitation directly rather than managing reader expectations with filler.

**Formulaic transitions ("Here's the thing:"):** Not found.

**Parallel structure formulae:** The bullet list under "What the Research Did Not Change" begins with "Structured negation is adopted...", "Convention-alignment...", "All framework changes...", "The causal comparison..." These are bullet points in a list, not consecutive prose sentences with identical syntactic openings. This is appropriate list formatting, not the parallel-structure tell.

**Voice register drops:** The article holds a consistent medium-technical register through most sections. The Executive Summary is the most conversational (~30% below average sentence complexity). The Key Findings section and NPT Pattern Taxonomy are the most technical (~20% above). The closing sections return to medium register. This variation is content-driven rather than structural -- the executive summary should be more accessible than the pattern catalog. The register shift is less than the 2x threshold that signals the tell. Not flagged as a violation; noted as a minor observation in Suggested Fixes.

**Academic citation sentences:** The inline citations in Key Findings are in conversational form: "Liu's team at AAAI 2026 documented..." and "Wen's team at EMNLP 2024 found..." This matches the vocabulary-reference.md preferred format ("[Finding] -- [Author]'s team showed this in [year]"). The References section uses a table, which is appropriate for a reference section. CLEAR.

**Ungrounded quantitative claims:** All quantitative claims are sourced. The 61% figure for bare NEVER constraints is from the framework's own constraint audit (stated as such: "At the start of this research, 61% of all negative constraints in the Jerry Framework (22 out of 36)"). The compliance percentages are from the A/B test. The external research figures have source citations. CLEAR.

**False precision:** The article does not use unmeasured intensifiers. "Demonstrably prevents violations" is accurate -- the A/B test showed 0/90 violations in the structured negation condition. "The framing effect is real and statistically significant" is anchored to the McNemar p-value immediately following. CLEAR.

**Overall Boundary #8 assessment:** No mechanical assembly markers at violation severity. The article reads as written rather than generated. The minor register variation is content-appropriate and below the detection threshold.

---

## Suggested Fixes

The article passes all tests and clears all boundary conditions. The following are optional strengthening observations, not required changes.

### Observation 1: Executive Summary Could Land the Finding Harder (Test 4 / optional)

The Executive Summary's strongest sentence is: "Standalone blunt prohibitions -- 'NEVER do X' with nothing else -- are the worst formulation available." This is the finding most developers will want to know. However, the paragraph immediately following this statement pivots to the external evidence before returning to the framework-internal count (61% of constraints using this format at project start).

Reordering to lead with the framework-internal implication before the external evidence would give the finding more immediate resonance for Jerry users: "At the start of this research, 61% of Jerry's negative constraints used this format. Every one was an upgrade candidate." This lands the finding closer to where the reader is -- in the framework -- before explaining the academic backing.

This is a matter of emphasis, not an information gap or voice failure.

### Observation 2: Register Transition Into the NPT Taxonomy Section (Boundary #8 / minor note)

The NPT Taxonomy section is the most information-dense part of the article. The transition into it -- "The research produced a 14-pattern taxonomy organizing how negative constraints can be expressed, sorted into seven technique types" -- is correct but flat. The Executive Summary earned some goodwill with its conversational opener; the taxonomy section's opening sentence could acknowledge that the reader is about to encounter a reference table, which would feel more human than just starting the table.

Example direction (not a rewrite -- this is sb-reviewer's scope): Something that signals "this section is a reference -- you do not need to memorize it" before presenting the pattern catalog would serve the documentation reader. The audience-adaptation.md note for documentation is "depth for those who engage, irrelevant if skipped." The current table is skippable, but there is no signal telling the reader it is okay to skim it and return later.

### Observation 3: "CONDITIONAL GO, Not Unconditional Mandate" Section Title (Test 5 / minor note)

The section title is slightly bureaucratic ("CONDITIONAL GO, Not Unconditional Mandate"). The content inside is the best-written section of the article -- genuinely honest, direct, and specific. The title undersells it. A title closer to the intellectual stake ("What the Evidence Actually Shows" or something in that direction) would match the quality of the prose underneath.

This is a cosmetic suggestion. The content is not affected.

---

## Session Context

```yaml
verdict: PASS
failed_test: null
boundary_violations: []
text_type: documentation
audience_context: documentation
suggested_fixes_count: 3
fix_severity: optional
ship_status: CLEAR TO SHIP
```

---

*sb-reviewer v1.0.0*
*Skill: saucer-boy-framework-voice v1.1.0*
*Constitutional Compliance: Jerry Constitution v1.0*
*Report persisted per P-002*
