# S-010 Self-Refine — Marketing Deliverables

**Strategy:** S-010 Self-Refine
**Deliverable:** `work/marketing/medium-article.md`
**Date:** 2026-02-24
**Reviewer:** adv-executor (S-010)

---

## Findings Summary

| ID | Dimension | Severity | Finding | Recommendation |
|----|-----------|----------|---------|----------------|
| F-01 | Flow | MAJOR | Opening paragraph front-loads a concept ("fluency-competence gap") and two citations before establishing why the reader should care | Move the hook sentence ("Reads like an expert wrote it") and the "mirage" punchline ahead of the academic framing; introduce citations after emotional buy-in |
| F-02 | Clarity | MAJOR | The "Why universally?" paragraph (para 4) answers a question nobody has asked yet; it breaks the narrative before any level framework has been introduced | Delete or relocate to after Level 3 section, where "why does this work on every model?" is a natural follow-up question |
| F-03 | Completeness | MAJOR | The two-session pattern is the article's most differentiating claim ("The Move Most People Miss") but the section header is generic ("The Move Most People Miss") and gives no preview of what the move is | Rename section to something that primes the reader: "The Two-Session Pattern (What Most People Miss)" — matches the subtitle's promise and signals specificity |
| F-04 | Accuracy | MAJOR | Liu et al. citation year is inconsistent: the References section says "(2024)" and the TACL publication line says "12, 157-173" (which is correct for 2024), but the in-text citation at line 59 says "(2024)" while the source blog post says "(2023)" — the arXiv preprint year and the published TACL year differ | Standardize to published venue year: Liu et al. (2024), TACL, 12, 157-173. The arXiv preprint (2307.03172) was uploaded 2023, published 2024 in TACL — in-text citation should match the References block which correctly says 2024 |
| F-05 | Flow | MAJOR | The blog post contains a "Why This Works on Every Model" section that explains vendor-agnostic universality with context window growth data — this section is absent from the Medium article, replaced by a shorter paragraph inserted mid-opening that reads as defensive justification | Either restore the vendor-agnostic rationale section (natural home: after Level 3) or remove the mid-opening defensive paragraph (F-02 above) — the current hybrid is the worst of both options |
| F-06 | Conciseness | MINOR | Line 13: "In my experience, this holds across every major model family I've tested" is immediately restated in line 15: "This trips up everybody... applies to Claude, GPT, Gemini, Llama" — redundant within two sentences | Delete line 13 ("In my experience...") or fold it into line 15 |
| F-07 | Clarity | MINOR | Level 3 prompt block (line 43) is presented without the important caveat the blog post includes: the prompt assumes tool access (file system, web search) — plain chat window users reading this on Medium will assume they can use the prompt verbatim | Add a one-sentence note after the Level 3 prompt block: "This prompt assumes tool access — file system, web search. In a plain chat window, paste the relevant code and verify citations yourself." |
| F-08 | Flow | MINOR | The "When This Breaks" section appears after the "Three Principles" section. A first-time reader who just internalized three principles then hits limitations — structurally sound, but the transition is abrupt with no bridging sentence | Add a single bridging sentence opening "When This Breaks": e.g., "All three principles hold — until they don't." |
| F-09 | Conciseness | MINOR | "Start Here" section checklist uses **bold** formatting for emphasis (e.g., **what to do**, **how I'll judge quality**) but the blog post uses ALL-CAPS checkboxes (`- [ ] Did I specify WHAT to do`). The Medium format is better for prose, but the bold mid-sentence creates visual choppiness across five items | Consistent approach: either bold all key terms or none — the current partial emphasis on some words but not others within the same list creates uneven scanning weight |
| F-10 | Completeness | MINOR | The blog post closes with a McConkey callback ("McConkey looked like he was winging it. He wasn't.") that ties back to the skiing metaphor used in the blog post's introduction. The Medium article drops the skiing metaphor from the opening but retains the closing line structure ("Do that once and tell me it didn't change the output.") without the McConkey callback — the closing is solid but loses the thematic bookend | Since the Medium article does not establish the McConkey metaphor (it was removed from the opening), the closing is fine as-is. No action needed unless the skiing metaphor is restored — but flag this as a coherence win the blog post has and Medium article does not |
| F-11 | Accuracy | OBSERVATION | The article describes chain-of-thought as demonstrating "constrain the input, get more reliable output" — this is a reasonable generalization but slightly mischaracterizes Wei et al., who showed intermediate reasoning steps improve performance, not generically that "constraints" improve output. The claim as stated is defensible but imprecise | Tighten to: "Wei et al. (2022) demonstrated with chain-of-thought prompting that adding intermediate reasoning steps to a prompt measurably improved performance — structure in, structure out." This matches both the evidence and the blog post's phrasing |
| F-12 | Clarity | OBSERVATION | Line 55: "Copy the finalized plan into a fresh chat and give it one clean instruction" — "fresh chat" is clear to experienced LLM users but may not be clear to the full Medium audience. The blog post says "start a brand new conversation" which is slightly clearer | Change "fresh chat" to "new conversation" for consistency with natural language |

---

## Detailed Findings

### F-01 — Flow: Opening Sequence Prioritizes Citations Over Hook (MAJOR)

**Location:** Lines 7–17 (opening section, before any section heading)

**Current text:**
> "Your LLM output comes back with clean structure, professional headings, and authoritative language. Reads like an expert wrote it.
> Except the expert part is a mirage.
> I call it the fluency-competence gap — a shorthand I started using after reading [Bender and Koller's 2020 argument]... [Sharma et al. (2024)]... The result is output that mirrors your assumptions instead of challenging them.
> When you don't define what rigor means, you get plausible instead of rigorous."

**Problem:** The first-time reader gets the hook ("Reads like an expert wrote it. Except the expert part is a mirage.") but then immediately enters an academic explanation with two citations before the emotional problem is fully landed. The "I call it the fluency-competence gap" framing is insider vocabulary introduced at the wrong moment — before the reader has felt the pain point.

**Comparison with blog post:** The blog post does the same thing in its Level 1 section (introducing the gap concept only after the Level 1 prompt example shows the failure mode). The reader first sees the bad prompt, then is told *why* it fails. The Medium article explains the failure mode before the reader has seen what failure looks like.

**Recommendation:** Restructure the opening:
1. Keep lines 7–9 ("Your LLM output comes back... Except the expert part is a mirage.")
2. Move the Level 1 prompt example earlier — let the reader feel "yes, I've sent this prompt" before naming the problem.
3. Introduce the fluency-competence gap concept and citations *after* the reader has experienced the problem narratively.

---

### F-02 — Clarity: "Why universally?" Paragraph Is Premature (MAJOR)

**Location:** Lines 17–18

**Current text:**
> "Why universally? Context windows vary by model and generation, but within any given model, you're working inside a fixed ceiling. Structured prompting works because it addresses how all these models process their available context — not because of anything vendor-specific."

**Problem:** This paragraph pre-empts a question the reader has not yet formed. The article has not yet explained what "structured prompting" is or introduced any of the three levels. A first-time reader encountering "structured prompting works because..." before being told what structured prompting *is* will feel disoriented.

**Additional issue:** This content is a weakened version of the blog post's dedicated "Why This Works on Every Model" section, which provides the GPT-3 / Gemini 1.5 context window growth data that makes the argument concrete. The Medium article strips out the evidence and keeps only the assertion.

**Recommendation:** Delete this paragraph from the opening. Either: (a) restore a proper "Why This Works on Every Model" section after Level 3, carrying the context window growth data; or (b) trust that the article's three-level structure and citations make the universality case implicitly. The current placement does neither job.

---

### F-03 — Completeness: Section Title Doesn't Deliver on Subtitle Promise (MAJOR)

**Location:** Line 51, section heading

**Current text:** "## The Move Most People Miss"

**Subtitle promise (line 3):** "Three levels of prompting, three levels of output quality — and the two-session pattern most people miss entirely."

**Problem:** The subtitle specifically names "the two-session pattern" as the differentiating insight. The section heading ("The Move Most People Miss") is vague — it doesn't tell the reader they've arrived at the thing the subtitle promised. A reader who scrolled the article before committing to read it in full may have noted the subtitle and be looking for "the two-session pattern" — they won't find it by scanning headings.

**Recommendation:** Rename to "## The Two-Session Pattern (What Most People Miss)" — this delivers on the subtitle's promise, rewards readers who remembered it, and signals specificity before they enter the section.

---

### F-04 — Accuracy: Liu et al. Citation Year Inconsistency (MAJOR)

**Location:** Line 59 (in-text) vs. line 103 (References)

**Current state:**
- In-text at line 59: "[Liu et al. (2024)]" — correct per published TACL venue
- References block at line 103: "Liu, N. F. et al. (2024). *TACL, 12*, 157-173" — correct
- Blog post in-text at line 70 uses "(2023)" — the arXiv preprint year

**Problem:** The Medium article correctly updated to 2024 (the TACL publication year) in both places. However, this creates a discrepancy with the source blog post if both are circulating. More importantly, cross-checking the in-text year (2024) against the References year (2024) confirms the Medium article is internally consistent and technically more accurate than the blog post. This is actually a *correction* the Medium article made correctly.

**Revised assessment:** This is not an error in the Medium article — it is a correction over the blog post. However, it is worth flagging that the blog post (published at the Jerry domain) still uses the incorrect 2023 year and should be updated to match. The Medium article's References are accurate.

**Recommendation:** No change to the Medium article. Flag the blog post's Liu et al. citation as needing correction: change "(2023)" to "(2024)" at line 70 of `docs/blog/posts/why-structured-prompting-works.md`.

---

### F-05 — Flow: Vendor-Agnostic Rationale Is Structurally Awkward (MAJOR)

**Location:** Opening section (lines 15–18) vs. blog post's "Why This Works on Every Model" section

**Current state:** The blog post has a dedicated section after Level 3 that explains vendor-agnostic universality with evidence: context window growth from GPT-3 (2K tokens, 2020) to Gemini 1.5 (1M tokens, 2024), and the argument that structure works because it addresses how any model processes its context ceiling. The Medium article removes this section entirely and replaces it with a two-sentence assertion inserted awkwardly in the opening.

**Problem for a first-time reader:** After reading Level 3, a skeptical reader may ask: "Does this only work on the model you used?" The blog post answers this with evidence. The Medium article does not answer it — the opening assertion ("why universally?") comes before the reader has the context to evaluate it, and is not repeated after they do.

**Recommendation:** After the Level 3 section, restore a compressed version of the vendor-agnostic rationale:

> "None of this requires a specific vendor. Context windows have grown fast — GPT-3 shipped with 2K tokens in 2020, Gemini 1.5 crossed a million in 2024. But within any given model, you're working inside a fixed ceiling. Give any model structure to work with, and it outperforms the same model given a vague request. That finding holds across models, tasks, and research groups."

Then delete the premature paragraph from the opening (F-02).

---

### F-06 — Conciseness: Redundant Universality Claim in Opening (MINOR)

**Location:** Lines 13 and 15

**Current text:**
> Line 13: "In my experience, this holds across every major model family I've tested."
> Line 15: "This trips up everybody. What I'm about to walk through applies to Claude, GPT, Gemini, Llama — every model I've tested, and likely whatever ships next Tuesday."

**Problem:** The universality claim is made twice in three sentences. Line 13 is the weaker formulation ("in my experience") and line 15 is the stronger, more specific one (names the models, adds "whatever ships next Tuesday" for the forward-looking hook). Line 13 adds no information and dilutes the punchier line 15.

**Recommendation:** Delete line 13. Begin the paragraph at line 15 directly.

---

### F-07 — Clarity: Level 3 Prompt Lacks Tool-Access Caveat (MINOR)

**Location:** After the Level 3 prompt block (line 43)

**Current text:** The Level 3 prompt ends at line 44 with no caveat. The blog post at line 48 adds: "That Level 3 prompt assumes a model with tool access: file system, web search, the works. If you're in a plain chat window, paste the relevant code and verify citations yourself. Same principles, different mechanics."

**Problem:** Medium's audience includes many readers running plain chat sessions (ChatGPT free, Claude.ai without projects, etc.). The Level 3 prompt explicitly says "using real sources — not training data," which implies web search access. Without a caveat, readers without tool access may attempt the prompt verbatim and get confused when the model cannot comply.

**Recommendation:** Add after the Level 3 prompt block:

> *"That prompt assumes tool access — file system, web search. In a plain chat window, paste your relevant code directly and verify citations yourself. Same principles, different mechanics."*

---

### F-08 — Flow: Abrupt Transition Into "When This Breaks" (MINOR)

**Location:** Line 73, section heading transition

**Context:** The preceding "The Three Principles" section closes with three confident, declarative principles. "When This Breaks" opens immediately with: "Structured prompting is not a magic fix."

**Problem:** The gear-shift is jarring. After three affirmative principles presented with confidence, a cold "it doesn't work" opening feels like a different article. A bridging sentence would smooth the transition and signal that the author is being intentionally balanced rather than contradicting themselves.

**Recommendation:** Open "When This Breaks" with: "All three principles hold — until they don't." or "That said, structure is not a magic fix." One sentence of transition converts an abrupt reversal into an honest acknowledgment.

---

### F-09 — Conciseness: Inconsistent Emphasis in Checklist (MINOR)

**Location:** Lines 83–90

**Current text:**
```
1. Did I specify **what to do** (not just the topic)?
2. Did I tell it **how I'll judge quality**?
3. Did I **require evidence or sources**?
...
4. Did I ask for the **plan before the product**?
5. Am I in a **clean context** (or carrying planning baggage)?
```

**Problem:** The bold emphasis is applied to the answer content ("what to do", "how I'll judge quality") rather than the key action words. Item 3 bolds "require evidence or sources" — the verb plus noun. Item 5 bolds "clean context" — a noun phrase. The weighting is inconsistent: some items bold the method ("require"), others bold the result ("clean context"). A reader scanning the checklist gets uneven signals about what matters in each item.

**Recommendation:** Either bold the key noun phrase in each item uniformly (the thing to check for) or bold nothing and rely on the numbered list structure. Option A (uniform bold noun phrases):
1. Did I specify **the task** (not just the topic)?
2. Did I define **quality criteria**?
3. Did I require **sources or evidence**?
4. Did I get **the plan first**?
5. Am I in a **fresh context**?

---

### F-10 — Completeness: Missing McConkey Callback (MINOR/OBSERVATION)

**Location:** Closing section (line 94)

**Context:** The blog post opens with a Shane McConkey skiing metaphor ("Three levels of prompting, three levels of output quality... McConkey looked like he was winging it. He wasn't.") and closes with a callback ("McConkey looked like he was winging it. He wasn't. The wild was the performance. The preparation was everything underneath it.").

**Medium article status:** The skiing metaphor was removed from the Medium article opening (appropriate — Medium's general audience may not know McConkey). The closing line ("Do that once and tell me it didn't change the output.") is solid and works without the callback.

**Assessment:** No action required. The closing is complete for Medium. The blog post's McConkey bookend is a coherence advantage specific to that version, where the metaphor was established. Worth noting as a structural asset the blog retains that Medium appropriately does not use.

---

### F-11 — Accuracy: Chain-of-Thought Characterization Slightly Imprecise (OBSERVATION)

**Location:** Lines 35–36

**Current text:**
> "[Wei et al. (2022)] demonstrated this with chain-of-thought prompting: adding intermediate reasoning steps to a prompt measurably improved performance on arithmetic, commonsense, and symbolic reasoning tasks. Their work studied specific reasoning benchmarks, but the underlying principle — constrain the input, get more reliable output — holds in my experience across every prompting scenario I've tested."

**Issue:** "Constrain the input, get more reliable output" is a reasonable generalization but imprecise. Chain-of-thought adds *structure to reasoning*, not constraints on output content. The blog post's phrasing is more accurate: "Structure in, structure out." The Medium article's phrasing ("constrain the input") blurs the distinction between input constraints (Level 2: specifying what to do) and reasoning structure (chain-of-thought: showing intermediate steps).

**Recommendation:** Replace the summary principle with the blog post's cleaner phrasing: "Structure in, structure out." Delete the current parenthetical about "specific reasoning benchmarks" — it reads as a defensive qualification that slows the paragraph.

---

### F-12 — Clarity: "Fresh Chat" vs "New Conversation" (OBSERVATION)

**Location:** Line 55

**Current text:** "Copy the finalized plan into a fresh chat and give it one clean instruction"

**Issue:** "Fresh chat" is LLM-practitioner slang. Medium's audience includes people newer to LLM workflows. The blog post uses "brand new conversation" (line 66 of blog post) — this is more universally understood terminology. Minor issue but worth standardizing.

**Recommendation:** Change "fresh chat" to "new conversation" for plain-language alignment.

---

## Overall Assessment

The Medium article is a well-adapted version of the source blog post for a general audience. The core argument is sound, the three-level framework is clearly communicated, and the citation quality is high. The article's strongest sections — the Level 2/Level 3 prompt examples, the two-session pattern explanation, and the self-critique tension — are all well executed.

**Primary weaknesses** are structural rather than substantive:

1. The opening section carries too much explanatory weight before the reader has felt the problem. The blog post earns the academic framing by first showing the failure; the Medium article explains the failure before demonstrating it. This is the most impactful fix (F-01, F-02, F-05 together constitute a cohesive restructure of the opening and would resolve the most significant first-impression gap).

2. The two-session pattern — the article's most differentiating claim and explicitly named in the subtitle — is undersold by a generic section heading (F-03). This is a low-effort, high-impact fix.

3. The Level 3 section lacks the tool-access caveat (F-07) that the blog post correctly includes, which may create friction for Medium readers attempting the prompt without tool-enabled models.

**Verdict:** The article would benefit from targeted revision on F-01 through F-05 before wider distribution. F-06 through F-09 are polish items that improve scannability and consistency. F-10 through F-12 are observations that require no immediate action.

**Estimated revision effort:** F-01 + F-02 + F-05 (restructure opening + restore vendor-agnostic section): ~45 minutes. F-03 + F-07 + F-08 (heading rename + two insertions): ~10 minutes. F-06 + F-09 + F-11 + F-12 (line-level edits): ~10 minutes. Total: approximately 65 minutes of targeted revision.
