---
reviewer: sb-reviewer
version: 1.0.0
date: 2026-03-01
artifact: projects/PROJ-014-negative-prompting-research/orchestration/proj-014-completion-20260301-001/articles/tweet-crosspost.md
verdict: PASS
boundary_violations: [8]
---

# Voice Compliance Report

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Verdict and context |
| [Authenticity Test Results](#authenticity-test-results) | Per-test pass/fail with evidence |
| [Boundary Condition Check](#boundary-condition-check) | 8 boundary conditions evaluated |
| [Suggested Fixes](#suggested-fixes) | Specific, actionable fixes for flagged issues |
| [Session Context](#session-context) | Structured handoff metadata |

---

## Summary

**Verdict:** PASS with BOUNDARY VIOLATION (Boundary #8 — Mechanical Assembly, minor)
**Text Type:** documentation (public-facing social media announcement)
**Audience Context:** documentation
**Expected Tone:** The Audience Adaptation Matrix does not have a direct row for social media announcements. The closest analog is "Session complete" (High energy, Yes humor, None technical depth, Celebration tone). This is a research milestone announcement — the closest spirit is celebration, but the text correctly reads as technical-audience-first, not developer-session-end. Energy calibration for a public-facing research thread should be: high conviction, direct, no humor required (the findings are the celebration), technically precise throughout. The voice here is correctly calibrated to that adjustment.

---

## Authenticity Test Results

| Test | Name | Verdict | Evidence |
|------|------|---------|----------|
| 1 | Information Completeness | PASS | All technical facts preserved: 270 tests, 3 Claude models, NPT-013, 100% compliance, 92.2% positive-only, 7.8pp gap, McNemar p=0.016, 90 matched pairs, 10 behavioral constraints, 3 pressure scenarios, blind-scored outputs, behavioral timing constraint 56% violation rate under positive-only, 0% under structured negation, Haiku 10pp improvement. The three-part NPT-013 format is present and correctly formatted. URL placeholders are intentional stubs, not information gaps. No technical fact from the research appears to have been dropped or distorted. |
| 2 | McConkey Plausibility | PASS | The voice has the right spirit. "The field says: use positive framing. That's not wrong — it's incomplete." (Post 4a) is structurally the Spatula moment — McConkey saying "They still don't get it. They'll get there eventually." Quiet confidence about an industry orthodoxy that turns out to be wrong. The closing beat of Post 3 — "Remove any one and compliance drops" — is confident without being arrogant: it states the mechanism and stops. The tweet is pure data delivery with no personality layer, which is appropriate for a 280-char constraint. McConkey did not narrate his jumps; he did them. The thread does the same. No element requires knowing McConkey to decode. |
| 3 | New Developer Legibility | PASS | Zero skiing metaphors. Zero Saucer Boy references. Zero McConkey biographical context required. Every technical term is either self-explanatory in context (McNemar, NPT-013, structured negation) or defined inline (Post 3 defines the three-part format explicitly). A developer who has never heard of the framework can parse every post independently. The "14-pattern NPT taxonomy" reference in Post 5 is appropriately deferred to the linked documentation rather than explained inline — correct choice for the character constraint. |
| 4 | Context Match | PASS | The energy calibration is correct for a technical research announcement aimed at practitioners. The tweet is data-first, high signal density. The thread builds with escalating detail: finding → methodology → format → insight → data → call to action. No celebratory whimsy, which is correct — this is a public research artifact, not an internal session-end message. Humor is absent, consistent with the technical precision required. The one near-miss is Post 1's opening ("270 LLM compliance tests. 3 Claude models. One constraint format hit 100%") — the staccato rhythm is high energy in context, though it carries a mild LLM-tell risk addressed under Boundary #8. Overall energy is well-calibrated: present without being caffeinated. |
| 5 | Genuine Conviction | PASS | The voice reads as believed. "C3 (structured negation) never lost a single matchup across any constraint, model, or scenario" (Post 2) — stated once, flatly, with no hedging or amplification. That is the voice of someone who ran the numbers and knows what they show. Post 4a's challenge to conventional wisdom ("That's not wrong — it's incomplete") lands as conviction, not contrarianism for its own sake, because Posts 4b immediately provides the data that earns it. The thread does not oversell. It presents and stops. That restraint is the tell of genuine conviction. |

---

## Boundary Condition Check

| # | Boundary | Status | Evidence |
|---|----------|--------|----------|
| 1 | NOT Sarcastic | CLEAR | No mockery of "positive framing" advocates. "That's not wrong — it's incomplete" is a careful, inclusive correction. The voice challenges the orthodoxy without mocking the people who hold it. |
| 2 | NOT Dismissive of Rigor | CLEAR | The methodology is the point. 90 matched pairs, blind scoring, McNemar exact test, 3 pressure scenarios — rigor is foregrounded, not treated as a formality. |
| 3 | NOT Unprofessional in High Stakes | CLEAR | No humor in a research context. Appropriate restraint throughout. |
| 4 | NOT Bro-Culture Adjacent | CLEAR | No exclusionary language. The findings are framed as improvements accessible to any practitioner. "The less capable the model, the more structure matters" (Post 4b) is inclusive — it helps people working with constrained resources, not just those with the best models. |
| 5 | NOT Performative Quirkiness | CLEAR | No strained references, no try-hard whimsy, no emoji. The voice is dry and technical throughout. No personality applied as coating. |
| 6 | NOT Character Override | CLEAR | This is framework-output text (social media announcement for a research artifact). No attempt to modify Claude reasoning behavior. |
| 7 | NOT Information Replacement | CLEAR | Every post leads with information. The voice is additive to the data, not a substitute for it. Post 3's format definition ("The prohibition draws a hard line...") is information delivered directly, not personality substituting for the explanation. |
| 8 | NOT Mechanical Assembly | FLAGGED | Three specific LLM-tell patterns detected. None individually fatal, but they accumulate in a short piece: (1) **Parallel structure formula** — Post 3: "The prohibition draws a hard line. The consequence creates stakes. The alternative gives the model somewhere to go." Three consecutive sentences with identical syntactic structure ("The {noun} {verb} {object}"). Per llm-tell-patterns.md, this is a medium-severity tell. (2) **Corrective insertion** — Post 4a/4: "The field says: use positive framing. That's not wrong — it's incomplete." The second sentence is a "That's not X — it's Y" corrective insertion variant. Per llm-tell-patterns.md, medium severity. (3) **Staccato emphasis pair** — Post 1: "270 LLM compliance tests. 3 Claude models. One constraint format hit 100%." Three consecutive sentences of 4-7 words each. Per llm-tell-patterns.md, this is a low-severity tell in isolation, but in combination with the above two it contributes to a mechanical texture. The overall effect is that Post 3's explanation of NPT-013 reads slightly like a generated list rather than a person who understands the mechanism explaining it. The conviction in Posts 4a/4b partially compensates — those posts land with genuine weight. The verdict remains PASS because no test fails and the violations are minor pattern-level issues rather than voice failures, but they are worth fixing before publication. |

---

## Suggested Fixes

### Fix 1 — Post 3: Break the parallel structure formula (Boundary #8)

**Current:**
> The prohibition draws a hard line. The consequence creates stakes. The alternative gives the model somewhere to go. Remove any one and compliance drops.

The three-sentence parallel structure reads as a generated list. The content is correct; the packaging is mechanical.

**Approach:** Either collapse into one sentence with a list structure, or vary the sentence openings so the explanation reads as reasoned rather than enumerated.

**Example direction (not a rewrite prescription — sb-rewriter's territory):**
The three-part structure needs to read as a mechanism, not three equal items. The final sentence ("Remove any one and compliance drops") already does the mechanical work — it earns more weight if the prior explanation builds toward it rather than listing in parallel. Consider: the prohibition and consequence deserve more space than the alternative, because the alternative is what most positive-framing advocates already include; the missing elements are the prohibition and the stakes.

---

### Fix 2 — Post 4a / Post 4 LinkedIn: Replace corrective insertion with direct claim (Boundary #8)

**Current:**
> The field says: use positive framing. That's not wrong — it's incomplete.

The "That's not X — it's Y" construction is an LLM corrective insertion pattern. It works rhetorically but reads as a formula. The actual claim is stronger than the formula suggests.

**Approach:** State the actual thesis directly. The research supports a direct claim: the conventional advice is incomplete because it only considers polarity and not structure. Say that. Per vocabulary-reference.md, the corrective insertion should be replaced with a direct statement of the actual claim.

---

### Fix 3 — Post 1: Vary the staccato opening (Boundary #8, low severity)

**Current:**
> 270 LLM compliance tests. 3 Claude models. One constraint format hit 100%.

This is a low-severity tell. The staccato opening is common in social media hooks and may be intentional. However, the three consecutive very short sentences fit the staccato emphasis pair pattern. If this is intentional as a hook format, it can stay — hook conventions on X legitimately use this structure. Flag it for author judgment rather than requiring a fix.

**If revised:** Combine the first two data points into one sentence and let the third stand alone as the punch: "270 tests across 3 Claude models. One format hit 100%." This reduces the staccato pair count to one, which is below the LLM-tell detection threshold.

---

### Priority Assessment

| Fix | Severity | Required Before Publication? |
|-----|----------|------------------------------|
| Fix 1 (Post 3 parallel structure) | Medium | Recommended |
| Fix 2 (Post 4a corrective insertion) | Medium | Recommended |
| Fix 3 (Post 1 staccato opening) | Low | Author judgment |

Fixes 1 and 2 together affect the two most analytically substantive posts (the format explanation and the insight post). These are where a reader who follows up will spend the most time. Making these two posts sound fully written rather than assembled will strengthen the overall impression before a larger audience reads them.

---

## Session Context

```yaml
verdict: PASS
failed_test: null
boundary_violations: [8]
text_type: documentation
audience_context: documentation
suggested_fixes_count: 3
notes: >
  Three minor LLM-tell patterns detected under Boundary #8 (NOT Mechanical Assembly).
  No Authenticity Test failed. All 5 tests PASS. Route to sb-rewriter for Fix 1 and
  Fix 2 before publication if the author wants the mechanical texture resolved. Fix 3
  is author judgment only -- hook conventions on X permit the staccato opening format.
```
