# Voice Compliance Report

> sb-reviewer v1.0.0 | 2026-03-01

## Summary

**Verdict:** FAIL (Test 5) / BOUNDARY VIOLATION (Boundary #8)
**Text Type:** documentation (external publication -- Medium article)
**Audience Context:** documentation (external -- developers and AI practitioners, not Jerry-specific users)
**Expected Tone:** Medium energy, no humor required, high technical depth, clarity as the primary job

**Scope note:** The Saucer Boy framework voice skill governs framework output text (CLI messages, error messages, hook text, documentation). A Medium article is documentation-adjacent external publication. The user has explicitly requested this review. Evaluation proceeds against all 5 tests and 8 boundary conditions, applying the "documentation" and "rule explanation" rows from the Audience Adaptation Matrix as the closest context matches.

---

## Authenticity Test Results

| Test | Name | Verdict | Evidence |
|------|------|---------|----------|
| 1 | Information Completeness | PASS | See Step 2 |
| 2 | McConkey Plausibility | PASS | See Step 3 |
| 3 | New Developer Legibility | PASS | See Step 4 |
| 4 | Context Match | PASS | See Step 5 |
| 5 | Genuine Conviction | FAIL | See Step 6 |

---

## Step 2: Test 1 -- Information Completeness (HARD Gate)

**Verdict: PASS**

Stripping all voice elements, the article's informational skeleton is intact and complete:

- Research question stated clearly: does structured negative framing outperform positive framing for LLM behavioral compliance?
- Methodology disclosed: 6 phases, 150 scenario-model pairs, 270 invocations, 3 models, 10 constraints, 3 framing conditions, blind scoring with double-scoring inter-rater check (92.6% agreement, Gwet's AC1 = 0.920).
- Results reported with statistics: C3 achieved 100% compliance; C1 achieved 92.2%; Fisher's exact p = 0.016; effect size 7.8 pp (below pre-specified 10% threshold, which is disclosed).
- The NPT-013 format is defined with its three components and each component's function is explained.
- Five specific, actionable recommendations are provided with a before/after example.
- Caveats are present and honest: single-session testing only, 10 constraints, 3 models, no mechanistic explanation.

A developer reading this article knows what was tested, what was found, what the format is, what to do next, and what the limits of the finding are. Information completeness is not in question.

**Proceeding to Tests 2-5.**

---

## Step 3: Test 2 -- McConkey Plausibility

**Verdict: PASS**

The spirit of the article -- direct, credible, not overselling the finding, honest about the limitations -- is consistent with McConkey's approach. McConkey did not perform for the audience; he said the thing. The caveats section ("The effect size is modest") is particularly in-spirit: acknowledging a finding did not clear its own threshold and proceeding anyway with honest framing is exactly the kind of unselfconscious directness that defines the McConkey ethos.

The article does not try to be charming. That is fine. The persona's "direct and warm" traits do not require a performed warmth. The article treats the reader as a capable practitioner.

No skiing vocabulary, no McConkey biographical references, no persona elements that would require external knowledge to decode.

**Marginal note:** The middle sections (particularly "What We Did" and "The Experiment") are so flat that the spirit drops for a stretch before recovering. This is not a plausibility failure -- McConkey could have written a flat technical summary -- but it is a signal that feeds into Tests 5 and Boundary #8.

---

## Step 4: Test 3 -- New Developer Legibility

**Verdict: PASS**

The article contains zero skiing vocabulary, zero McConkey biographical references, and zero persona-specific terminology that requires external knowledge to decode. Every technical term is defined in context (NPT-013 is explained on first use; C1/C2/C3 framing conditions are defined before results are presented; Fisher's exact test is mentioned with the result rather than assumed knowledge).

A developer who has never heard of McConkey, Saucer Boy, or Jerry framework reads this as a standard AI research summary. No decoding required.

---

## Step 5: Test 4 -- Context Match

**Verdict: PASS**

The Audience Adaptation Matrix rows most applicable to an external Medium article are:

- "documentation" (Medium energy, no humor, high technical depth, clarity)
- "rule explanation" (Medium energy, no humor, high technical depth, clarity -- "the why matters")

The article's energy level is consistently medium-to-low throughout: measured, technical, precise. No jarring tonal swings. No humor content (appropriate for this context). The five-step "What You Can Do Today" section delivers practical guidance at medium energy without celebration or levity (correct for this moment).

The article does not overcelebrate its own findings (the caveats section ensures this). It does not use a flat bureaucratic register that would fail the "human" dimension of the matrix.

The energy is appropriate. The match is acceptable.

---

## Step 6: Test 5 -- Genuine Conviction

**Verdict: FAIL**

The article has sections that read from conviction and sections that read as assembled. The failure is localized but real.

**Where conviction is present:**

- Opening hook (lines 16-18): "What if telling an LLM what *not* to do is more effective than telling it what *to* do? That question sounds almost too simple to matter." -- this reads like someone who found something surprising and is leading with it honestly.
- "The Problem Nobody Talks About" section (lines 24-30): the compliance degradation framing is specific and believed. "This is not a hallucination problem. This is a *compliance degradation* problem." has energy, even if the construction is an LLM tell (flagged in Boundary #8 below).
- "Why Three Components Work" (lines 79-87): each of the three explanations does specific work. The consequence explanation ("signals that this constraint is load-bearing, not decorative") is precise and comes from understanding, not assembly.
- The caveats section: honest acknowledgment that the effect fell below the pre-specified threshold. This is conviction in the form of intellectual honesty.

**Where assembly is detectable:**

- Section headers are textbook Medium article structure: "What We Did," "The Experiment," "The Key Discovery," "The Caveats," "The Bottom Line." These headers signal that someone assembled a standard article structure and filled in the sections. A writer who believed what they were writing would give sections names that come from the content, not the template. Compare: "The Key Discovery" (formulaic) vs. "Zero Violations, Every Time" (from the content).

- "The Bottom Line" paragraph (lines 128-133) largely re-states findings already present in "The Key Discovery" section. This read-as-assembled problem -- a summary that adds no new framing -- signals the conclusion was written to complete the template, not because the writer had something new to say at the end. The final two sentences are genuinely good: "Structure matters more than polarity" and "the three-component structure costs nothing to adopt, takes minutes to implement, and the data says it works" both land. But the preceding sentence ("The structured negation format -- NEVER X, Consequence Y, Instead Z -- achieved 100% compliance across 90 blind tests on three Claude models. Positive-only framing achieved 92.2%. Fisher's exact test: p = 0.016.") repeats the exact statistics already stated in "The Key Discovery" without adding new framing or perspective. This is the clearest assembly signal.

- The opening question "What if telling an LLM what *not* to do is more effective than telling it what *to* do?" is a framing device, but it is also a familiar Medium article opening pattern (the rhetorical question hook). The conviction underneath is real, but the delivery form is assembly.

The article passes four of five tests but fails Test 5 on the specific grounds that: (a) section headers impose a template structure rather than emerging from the content, and (b) the conclusion section repeats already-stated statistics without adding new conviction or framing, signaling the conclusion was written to close the template rather than to land the thing that most needed landing.

**Fix direction:** The section headers need to come from the content. The conclusion section needs a new beat -- something that was not in the body, even if brief. The writer knows something at the end of the piece that they did not know at the beginning; the conclusion should say what that is.

---

## Step 7: Boundary Condition Check

| # | Boundary | Status | Evidence |
|---|----------|--------|----------|
| 1 | NOT Sarcastic | CLEAR | No mockery of the reader or the research. No ironic distance. |
| 2 | NOT Dismissive of Rigor | CLEAR | The caveats section treats the methodology's limitations with full seriousness. The disclosed threshold shortfall ("fell just below" the pre-specified 10% minimum) is honest disclosure, not a wink at the quality system. |
| 3 | NOT Unprofessional in High Stakes | CLEAR | No humor content present. Article treats research findings with appropriate sobriety throughout. |
| 4 | NOT Bro-Culture Adjacent | CLEAR | No exclusionary language, no skiing-culture irony, no terminology that would signal an in-group. |
| 5 | NOT Performative Quirkiness | CLEAR | No strained references, no try-hard personality elements, no emoji content. The article makes no attempt at quirky voice and does not need to for this context. |
| 6 | NOT Character Override | CLEAR | N/A for this text type. The article is a research narrative, not framework-generated output; no personality modification of Claude's reasoning behavior is occurring. |
| 7 | NOT Information Replacement | CLEAR | Information is consistently primary. No personality element substitutes for diagnostic or explanatory content. |
| 8 | NOT Mechanical Assembly | FLAGGED | Multiple LLM tell patterns detected. See detail below. |

### Boundary #8 Detail: Mechanical Assembly

Four LLM tell patterns are present in this article. Reference: `skills/saucer-boy-framework-voice/references/llm-tell-patterns.md` (Detection Quick Reference).

**Tell 1: Corrective Insertion (Medium severity)**
Location: "The Problem Nobody Talks About" section, lines 26-27.
Evidence: "This is not a hallucination problem. This is a *compliance degradation* problem."
Pattern match: The "It's not X. It's Y." corrective insertion structure. This is explicitly listed as a forbidden construction in `vocabulary-reference.md`: "State the actual claim directly. Negation-correction is an LLM writing tic, not an argument."
Fix: "The failure mode is *compliance degradation*, not hallucination. The model understood the rules and then stopped following them." State the actual claim; the negation adds no information.

**Tell 2: Staccato Emphasis Pair (Low severity)**
Location: Lines 20-21.
Evidence: "We spent six weeks testing that assumption. The answer surprised us."
Pattern match: Two consecutive short sentences where the second amplifies the first. Severity is Low per the detection table, and the second sentence ("The answer surprised us") does carry genuine content -- it is a preview that creates forward momentum. However, it matches the staccato pattern structurally.
Fix: This one is borderline. "We spent six weeks testing that assumption -- the answer surprised us" is slightly stronger (merges into one sentence with movement) but the original is not a clear violation. Flag as minor.

**Tell 3: Voice Register Drop (High severity)**
Location: Transition from the opening section to "What We Did" and "The Experiment" sections.
Evidence: The opening section ("What if telling an LLM...") reads at a conversational register. The methodology sections read at a notably more clinical register: "Six weeks. Six phases. A literature survey across 75 academic and industry sources, then claim validation, taxonomy development, and framework analysis, culminating in a controlled A/B test." This is compressed, efficient, and correct -- but the register is different from the conversational voice of the introduction, and it stays clinical through the results presentation before recovering somewhat in "Why Three Components Work."
The "Six weeks. Six phases." pattern itself is a parallel staccato construction (two consecutive short sentences as rhetorical emphasis), compounding the tell.
Fix: The register does not need to become casual in the methodology sections, but the transition should be smoothed. "Six weeks. Six phases." reads as assembled compression; "The research ran six weeks across six phases" is the same information at the same register as the surrounding prose.

**Tell 4: Parallel Structure Formula (Medium severity)**
Location: "The Bottom Line" section, final paragraph, lines 131-132.
Evidence: "A bare 'NEVER do X' is the worst constraint formulation we tested. A bare 'Always do Y' is better but still vulnerable. 'NEVER do X -- here is why, and here is what to do instead' is the format that hit zero violations."
Pattern match: Three consecutive sentences with parallel structure ("[construction] is [verdict]"), creating a rhythm that reads as generated rather than written.
Fix: Collapse into a list or restructure: "Of the three formulations, bare 'NEVER do X' is the worst, positive-only is better but still vulnerable, and the three-component structure is the one that hit zero violations." Alternatively, the third sentence could break the parallelism: "The three-component format is not just better -- it eliminated violations entirely."

---

## Suggested Fixes

### Fix 1: Test 5 -- Section Headers (Assembly Signal)
**What to change:** Replace template-structure section headers with content-derived headers.
**Current headers that signal assembly:**
- "What We Did" -> Consider: "Six Weeks, Six Phases, One Clear Result" or "The Research Design"
- "The Key Discovery" -> Consider: "Zero Violations, 90 Tests" or the specific claim
- "The Bottom Line" -> Consider: "Structure Beats Polarity" (the actual takeaway)

**Why:** Section headers are the skeleton of the article. When they read as slots in a template ("What We Did," "The Bottom Line"), they signal the article was assembled rather than written. Headers that come from the content ("Zero Violations, 90 Tests") signal that someone found a specific thing and named it.

### Fix 2: Test 5 -- The Conclusion Section
**What to change:** The "The Bottom Line" section restates statistics already in the body. Add a new beat at the end -- something the writer knows at the end of this piece that was not present at the beginning.
**Current:** The final paragraph opens with a restatement of the 100% compliance result and p-value, then pivots to the "structure matters more than polarity" conclusion.
**Suggested approach:** Cut the statistical restatement from the conclusion (it was in "The Key Discovery"). Open the conclusion with the "structure matters more than polarity" insight, then add one new beat -- a forward-looking implication, an honest remaining question, or the thing the research changed about how the team thinks about prompting. The footnote (the methodology disclosure) already provides the technical closure; the conclusion should provide the human closure.
**Why:** A conclusion that adds no new information signals the writer was completing the template, not closing the argument. The best ending says something the middle could not say because the reader had not yet seen all the evidence.

### Fix 3: Boundary #8, Tell 1 -- Corrective Insertion
**What to change:** Line 26-27: "This is not a hallucination problem. This is a *compliance degradation* problem."
**Suggested:** "The failure mode here is *compliance degradation*, not hallucination. The model understood your rules; it just stopped following them."
**Why:** The corrective insertion pattern ("It's not X, it's Y") is an LLM writing tell. Stating the actual claim directly is more direct and eliminates the tell. Moving "the model understood your rules; it just stopped following them" forward also clarifies immediately what compliance degradation means.

### Fix 4: Boundary #8, Tell 3 -- Voice Register Drop / Staccato at Methodology Open
**What to change:** "Six weeks. Six phases. A literature survey across 75 academic and industry sources, then claim validation, taxonomy development, and framework analysis, culminating in a controlled A/B test."
**Suggested:** "The research ran six weeks across six phases: a literature survey of 75 academic and industry sources, followed by claim validation, taxonomy development, and framework analysis, with a controlled A/B test as the final phase."
**Why:** "Six weeks. Six phases." is a staccato emphasis pair. The compressed bullet-list style in the methodology open represents a register shift from the conversational introduction. Flowing prose at the same level of detail holds the register without losing precision.

### Fix 5: Boundary #8, Tell 4 -- Parallel Structure in Bottom Line
**What to change:** "A bare 'NEVER do X' is the worst constraint formulation we tested. A bare 'Always do Y' is better but still vulnerable. 'NEVER do X -- here is why, and here is what to do instead' is the format that hit zero violations."
**Suggested:** "Of the three formulations we tested, bare prohibitions performed worst, positive-only was better but still vulnerable, and the three-component structure eliminated violations entirely. Structure, not polarity, is what made the difference."
**Why:** Breaking the three-part parallel structure ("X is Y. X is Y. X is Y") eliminates the generated rhythm. Collapsing into a single compound sentence with the key conclusion ("eliminated violations entirely") as the landing point is more direct and reads as written.

---

## Self-Review Check (H-15)

- [x] Each test was evaluated with specific textual evidence
- [x] Test 1 was evaluated first; evaluation continued because it passed
- [x] Boundary conditions were checked independently of the 5 tests
- [x] Suggested fixes are specific (location cited, before/after direction given, reason stated)
- [x] Violations were not softened: Test 5 FAIL and Boundary #8 FLAGGED are reported as found
- [x] The scope note at the top acknowledges the text type is documentation-adjacent, not standard framework output

---

## Session Context (for orchestrator)

```yaml
verdict: FAIL
failed_test: 5
boundary_violations: [8]
text_type: documentation
audience_context: documentation
suggested_fixes_count: 5
```
