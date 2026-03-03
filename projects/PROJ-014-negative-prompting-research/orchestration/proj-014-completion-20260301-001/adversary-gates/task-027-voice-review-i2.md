# Voice Compliance Report (Iteration 2)

> sb-reviewer v1.0.0 | 2026-03-01
> Prior review: `adversary-gates/task-027-voice-review.md` (i1)

## Summary

**Verdict:** PASS
**Text Type:** documentation (external publication -- Medium article)
**Audience Context:** documentation (external -- developers and AI practitioners)
**Expected Tone:** Medium energy, no humor required, high technical depth, clarity as the primary job

**i1 Resolution Status:** All 5 i1 fixes are resolved. The two specific Test 5 failure conditions (template-structure section headers; statistical restatement in conclusion) are eliminated. All 4 Boundary #8 tells from i1 are corrected. Two new Low-severity staccato tells were introduced by the revision; these do not rise to a Boundary #8 violation but are noted in the Suggested Fixes section for optional cleanup.

---

## Authenticity Test Results

| Test | Name | Verdict | Evidence |
|------|------|---------|----------|
| 1 | Information Completeness | PASS | Full informational skeleton intact; no gaps introduced by revision |
| 2 | McConkey Plausibility | PASS | Spirit of directness and intellectual honesty holds; revision did not strain the voice |
| 3 | New Developer Legibility | PASS | No persona-specific vocabulary; every term defined in context |
| 4 | Context Match | PASS | Medium energy, no humor, high technical depth throughout |
| 5 | Genuine Conviction | PASS | Template headers replaced; conclusion delivers new beat, not statistical restatement |

---

## Step 2: Test 1 -- Information Completeness (HARD Gate)

**Verdict: PASS**

The revision made structural and tonal changes only. The informational skeleton is identical to i1 and remains complete:

- Research question stated clearly (does structured negative framing outperform positive framing?)
- Methodology disclosed (6 phases, 270 invocations, 3 models, 10 constraints, 3 framing conditions, blind scoring, 92.6% inter-rater agreement, Gwet's AC1 = 0.920)
- Results reported with statistics (C3: 100% compliance; C1: 7.8% violation rate; McNemar's exact test p = 0.016; Bonferroni correction noted)
- NPT-013 format defined with all three components and their functions
- Five actionable recommendations with before/after example
- Caveats section intact and unchanged (effect fell below pre-specified 10% threshold, single-session only, 10 constraints, 3 models, no mechanistic explanation)

No information was removed or obscured by the revision. Proceeding to Tests 2-5.

---

## Step 3: Test 2 -- McConkey Plausibility

**Verdict: PASS**

The revision did not alter the spirit of the article. The directness, the honest caveat acknowledgment, and the refusal to oversell the finding are all present. The new conclusion section adds a framing shift ("treating your system prompt not as a list of aspirations but as a set of load-bearing rules") that is in-spirit: it states a practical conviction without performing it.

The section headers are now content-derived ("Zero Violations Across Ninety Tests," "Structure Beats Polarity") rather than template slots. Content-derived naming is more in the McConkey spirit than template naming -- it reflects the actual finding rather than the expected article shape.

No biographical references, no skiing vocabulary, no persona markers requiring external knowledge to decode.

---

## Step 4: Test 3 -- New Developer Legibility

**Verdict: PASS**

Unchanged from i1. The revision introduced no persona-specific vocabulary. All technical terms remain defined on first use. A developer with no knowledge of McConkey, Saucer Boy, or Jerry framework reads this as a standard AI research summary.

---

## Step 5: Test 4 -- Context Match

**Verdict: PASS**

The Audience Adaptation Matrix rows applicable to an external Medium article ("documentation": medium energy, no humor, high technical depth, clarity) remain correctly matched. The revision did not alter energy level or introduce humor. The methodology section now holds the same register as the introduction, which tightens the energy consistency.

---

## Step 6: Test 5 -- Genuine Conviction

**Verdict: PASS**

The two specific i1 failure conditions are resolved.

**Fix 1 verified -- Section headers are content-derived:**

The i1 template headers are gone:
- "What We Did" -> "Seventy-Five Papers and a Gap in the Literature" (specific to what was found)
- "The Key Discovery" -> "Zero Violations Across Ninety Tests" (the actual result, named directly)
- "The Bottom Line" -> "Structure Beats Polarity" (the actual conclusion, not the slot label)

These headers come from the content. A writer who believed what they were writing named the sections after what was in them. The assembly signal is eliminated.

**Fix 2 verified -- Conclusion delivers new beat:**

The "Structure Beats Polarity" section (lines 127-133) no longer opens with a statistical restatement. It opens with the unexpected finding: "The thing we did not expect going in was that polarity -- positive vs. negative -- would turn out to be the wrong axis entirely. The real variable is structure."

The conclusion then delivers a new beat that was not available until the evidence was assembled: "The harder part is the shift in thinking: treating your system prompt not as a list of aspirations but as a set of load-bearing rules, each one documented with why it matters and what to do instead." This is the attitudinal implication of the data, not a restatement of it. It lands because the reader has now seen the evidence; it could not have been stated at the top.

The i1 problem was a conclusion that completed the template. The i2 conclusion lands the argument. Test 5 passes.

---

## Step 7: Boundary Condition Check

| # | Boundary | Status | Evidence |
|---|----------|--------|----------|
| 1 | NOT Sarcastic | CLEAR | No mockery of reader or research; no ironic distance introduced by revision |
| 2 | NOT Dismissive of Rigor | CLEAR | Caveats section unchanged; methodology limitations treated with full seriousness |
| 3 | NOT Unprofessional in High Stakes | CLEAR | No humor content; article maintains appropriate sobriety throughout |
| 4 | NOT Bro-Culture Adjacent | CLEAR | No exclusionary language or in-group terminology |
| 5 | NOT Performative Quirkiness | CLEAR | No strained personality elements; revision did not introduce try-hard voice |
| 6 | NOT Character Override | CLEAR | N/A for this text type |
| 7 | NOT Information Replacement | CLEAR | Information consistently primary; no personality element substitutes for diagnostic content |
| 8 | NOT Mechanical Assembly | CLEAR | All 4 i1 tells resolved; 2 new Low-severity staccato patterns noted but do not constitute systemic assembly |

### Boundary #8 Detail: i1 Tells -- Resolution Verification

**Tell 1 (Corrective Insertion, Medium) -- RESOLVED**

i1 evidence: "This is not a hallucination problem. This is a *compliance degradation* problem." (lines 26-27)
i2 text: "The failure mode is *compliance degradation*. The model understood your rules."
Resolution: The "It's not X. It's Y." corrective insertion structure is eliminated. The actual claim is stated directly. Note: the sentence "The failure mode is *compliance degradation*." is now followed by "The model understood your rules." -- see new Tell A below, but the corrective insertion pattern itself is gone.

**Tell 2 (Staccato Pair, Low) -- RESOLVED**

i1 evidence: "We spent six weeks testing that assumption. The answer surprised us." (lines 20-21)
i2 text: "We spent six weeks testing that assumption, and the answer was not what we expected." (line 20)
Resolution: Merged into a single sentence. Pattern eliminated.

**Tell 3 (Voice Register Drop, High) -- RESOLVED**

i1 evidence: "Six weeks. Six phases. A literature survey across 75 academic and industry sources..." (methodology open)
i2 text: "The research ran six weeks across six phases: a literature survey of 75 academic and industry sources, followed by claim validation, taxonomy development, and framework analysis, with a controlled A/B test as the final phase." (line 34)
Resolution: The staccato compression is eliminated. The methodology open is now flowing prose at the same register as the surrounding text. The i1 "Six weeks. Six phases." parallel staccato construction is gone.

**Tell 4 (Parallel Structure Formula, Medium) -- RESOLVED**

i1 evidence: "A bare 'NEVER do X' is the worst constraint formulation we tested. A bare 'Always do Y' is better but still vulnerable. 'NEVER do X -- here is why...' is the format that hit zero violations." (three-sentence parallel structure)
i2 text: "Of the three formulations we tested, bare prohibitions performed worst, positive-only was better but still vulnerable, and the three-component format eliminated violations entirely." (line 129)
Resolution: The three-sentence parallel structure ("X is Y. X is Y. X is Y.") is collapsed into a single compound sentence. The generated rhythm is eliminated.

### Boundary #8 Detail: New Tells in i2

The revision introduced two new Low-severity staccato patterns. Neither rises to a boundary violation -- the article does not read as hollow, and no systemic assembly pattern is present -- but they are documented for optional cleanup.

**New Tell A: Staccato Pair (Low severity)**
Location: Lines 25-26.
Evidence: "The model understood your rules. It followed them initially."
Pattern: Two consecutive sentences under 8 words each; the second amplifies the first by adding a temporal qualifier. Per the detection table, severity is Low.
Note: This is less severe than the i1 Tell 2 because "It followed them initially" carries genuine forward information (sets up the degradation narrative). The pair is functional but structurally matches the staccato pattern.

**New Tell B: Staccato Amplifier (Low severity)**
Location: Lines 61-62.
Evidence: "The effect was unidirectional and consistent. C3 never underperformed C1 on any single constraint, model, or scenario. Not once."
Pattern: "Not once." is a 2-word standalone amplification sentence following a complete statement of the same claim. Per detection heuristic, two consecutive short sentences where the second restates or amplifies the first.
Note: "Not once." is a rhetorical intensifier without additional information. The preceding sentence already states "never underperformed on any single constraint, model, or scenario." The standalone fragment adds emphasis, not content.

**Boundary #8 overall verdict:** CLEAR. The pattern density in i2 is substantially lower than i1. The two new Low-severity tells are isolated instances, not a systemic assembly signature. The article reads as written, not assembled.

---

## Suggested Fixes

The article passes all tests and all boundary conditions. The following fixes are optional cleanup for the two new Low-severity tells.

### Optional Fix A: New Tell A -- Staccato at Lines 25-26
**What to change:** "The model understood your rules. It followed them initially."
**Suggested:** "The model understood your rules and followed them initially."
**Why:** Merging the two short sentences eliminates the staccato pattern and maintains the same information. The revision that removed the corrective insertion introduced this pair; this closes the loop.

### Optional Fix B: New Tell B -- "Not Once." Amplifier at Line 62
**What to change:** "The effect was unidirectional and consistent. C3 never underperformed C1 on any single constraint, model, or scenario. Not once."
**Suggested:** "The effect was unidirectional and consistent -- C3 never underperformed C1 on any single constraint, model, or scenario."
**Why:** "Not once." adds no information beyond what the preceding sentence already states. Removing it eliminates the standalone amplifier fragment. The em-dash version preserves the emphasis through the unbroken statement rather than a separate fragment.

---

## i1 Resolution Summary

| i1 Fix | Description | Status |
|--------|-------------|--------|
| Fix 1 | Template headers replaced with content-derived headers | RESOLVED |
| Fix 2 | Conclusion opens with new beat, not statistical restatement | RESOLVED |
| Fix 3 | Corrective insertion eliminated; claim stated directly | RESOLVED |
| Fix 4 | "Six weeks. Six phases." register drop eliminated; flowing prose | RESOLVED |
| Fix 5 | Three-sentence parallel structure collapsed | RESOLVED |

---

## Self-Review Check (H-15)

- [x] Each test was evaluated with specific textual evidence from i2
- [x] Test 1 was evaluated first; evaluation continued because it passed
- [x] Boundary conditions were checked independently of the 5 tests
- [x] i1 tells verified as resolved with specific text evidence from i2
- [x] New tells introduced by revision were detected and documented
- [x] PASS verdict is reported without softening or inflation; new tells noted without overstating severity
- [x] Suggested fixes are specific and actionable; clearly labeled as optional

---

## Session Context (for orchestrator)

```yaml
verdict: PASS
failed_test: null
boundary_violations: []
text_type: documentation
audience_context: documentation
suggested_fixes_count: 2
new_tells_introduced: 2
new_tell_severity: Low
i1_fixes_resolved: 5
i1_fixes_resolved_count: 5
```
