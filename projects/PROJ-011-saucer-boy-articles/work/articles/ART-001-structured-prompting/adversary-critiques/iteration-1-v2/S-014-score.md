# S-014 LLM-as-Judge Score: draft-5-llm-tell-clean.md

| Section | Purpose |
|---------|---------|
| [Dimension Scores](#dimension-scores) | Per-dimension 0.0-1.0 with justification |
| [Weighted Composite](#weighted-composite) | Final score calculation |
| [LLM-Tell Detection](#llm-tell-detection) | Sentence-level scan for AI writing markers |
| [Voice Authenticity](#voice-authenticity) | McConkey persona fidelity assessment |
| [Verdict](#verdict) | PASS / REVISE / REJECTED |
| [Top Improvements](#top-improvements) | Specific actionable revisions |

---

## Dimension Scores

### 1. Completeness (Weight: 0.20) -- Score: 0.88

The article covers the Level 1/2/3 spectrum well, the two-session pattern, and the three principles. However, there are practitioner-visible gaps. The article does not address what happens when structured prompting still produces bad output (failure modes, recovery strategies). There is no discussion of model-specific syntax differences beyond a single sentence ("XML tags for Claude, markdown for GPT"). A practitioner working with tool-use, system prompts, or multi-modal inputs gets nothing here. The "Start Here" checklist is good but limited to text prompting in a single-turn or two-session flow. The article also omits any mention of temperature, sampling parameters, or how model configuration interacts with structured prompting, which a practitioner at Level 3 would encounter immediately.

### 2. Internal Consistency (Weight: 0.20) -- Score: 0.93

The article maintains a coherent arc from vague prompting to structured orchestration. Claims build on each other logically. The McConkey framing opens and closes the piece symmetrically. One minor inconsistency: the article says "every LLM on the market" in the opening and then later specifies the principles are "universal" but the "implementation syntax varies." These are compatible claims but the opening paragraph oversells universality slightly, because the two-session pattern is not equally applicable to all models (some have persistent memory, some have project-level contexts that change the token-budget argument). The voice stays consistent throughout. No contradictions between sections.

### 3. Methodological Rigor (Weight: 0.20) -- Score: 0.87

The three principles are well-derived from the preceding Level 1/2/3 exposition. The Level framework itself is logically sound as a pedagogical tool. However, the methodological grounding has soft spots. The claim that "structured instructions focus the model's attention on relevant context and narrow the space of acceptable completions" is stated as architectural fact but is actually a simplification of attention mechanism behavior. The "fluency-competence gap" is presented as a named, documented phenomenon but is more of an informal descriptor used in AI safety and alignment discourse than a formally defined term with a canonical citation. The two-session pattern's justification leans heavily on the Liu et al. "lost in the middle" finding, which is a real paper, but applying it to conversational context (planning debris degrading execution) is an extrapolation that the paper itself does not directly validate. The self-assessment bias claim ("research on LLM self-evaluation consistently shows favorable bias") is directionally correct but presented without citation, which undermines the article's own standard of evidence.

### 4. Evidence Quality (Weight: 0.15) -- Score: 0.82

Liu et al. (2023) "Lost in the Middle" is a real, citable paper (Nelson Liu et al., Stanford). That citation checks out. However, it is the only specific citation in the entire article. The "fluency-competence gap" is attributed vaguely to "a pattern documented across model families since GPT-3" with no citation. The claim about chain-of-thought prompting and structured role-task-format patterns improving output is stated as "well-documented" but no sources are named. The self-evaluation bias claim has no citation. For an article that explicitly tells readers to "require evidence or sources" in the checklist, the article itself provides exactly one verifiable reference. This is a credibility gap that a critical reader would notice. The technical claims about next-token prediction and probability distributions are accurate but standard. Nothing novel is claimed incorrectly, but the evidence bar the article sets for its readers is higher than the evidence bar the article holds itself to.

### 5. Actionability (Weight: 0.15) -- Score: 0.93

The article is highly actionable. A reader could take the Level 2 example prompt, adapt it to their domain, and see immediate improvement. The five-item checklist is concrete and usable. The two-session pattern is described with enough specificity to execute ("copy the finalized plan into a fresh chat, prompt with one clean instruction"). The graduated approach ("start with Level 2, graduate to Level 3 when the work has consequences") gives the reader a realistic on-ramp. The closing dare is a good behavioral nudge. The only gap is that no worked example shows the full arc from plan review to execution, so a reader doing Level 3 for the first time would be assembling the steps from description rather than following a demonstrated walkthrough.

### 6. Traceability (Weight: 0.10) -- Score: 0.78

Only one traceable citation: Liu et al. (2023). All other claims are presented as general knowledge or attributed vaguely ("research has shown," "well-documented finding," "a pattern documented across model families"). A reader who wanted to fact-check the fluency-competence gap, the self-evaluation bias claim, or the attention-mechanism explanation would have nowhere to start. The article does not link to any external resources, papers, or documentation beyond the single Liu reference. For an article on an mkdocs site targeting practitioners, a "Further Reading" section or inline links would significantly improve traceability.

---

## Weighted Composite

| Dimension | Weight | Score | Weighted |
|-----------|--------|-------|----------|
| Completeness | 0.20 | 0.88 | 0.176 |
| Internal Consistency | 0.20 | 0.93 | 0.186 |
| Methodological Rigor | 0.20 | 0.87 | 0.174 |
| Evidence Quality | 0.15 | 0.82 | 0.123 |
| Actionability | 0.15 | 0.93 | 0.140 |
| Traceability | 0.10 | 0.78 | 0.078 |
| **TOTAL** | **1.00** | | **0.877** |

**Weighted Composite Score: 0.877**

---

## LLM-Tell Detection

**Score: 0.91**

This draft is substantially cleaner than typical LLM output. Specific findings:

**Clean signals (positive):**
- No em-dashes or double-dashes anywhere in the text. Clean punctuation throughout.
- No hedging phrases ("it's worth noting," "it should be mentioned," "arguably"). The article makes direct claims.
- Sentence length varies naturally. Short punchy sentences mix with longer explanatory ones.
- Transitions are not formulaic. No "Moreover," "Furthermore," "Additionally," "It's important to note" patterns.
- The bullet lists in Level 3 and "Why This Works" use varied syntactic structures rather than parallel templates.

**Residual tells (minor):**
- The phrase "That's not a coin flip. It's systematic, and it's predictable." uses a rhetorical pattern (negative framing followed by positive restatement) that appears in coached LLM output, though it also appears in natural persuasive writing.
- "Same topic. But now the LLM knows:" is a fragment-then-colon pattern that is common in LLM-generated explainer content, though again it is also a normal rhetorical device.
- The three-principle structure (numbered, bolded, each with the same "verb the noun" imperative pattern: "Constrain the work," "Review the plan," "Separate planning from execution") has a slightly over-regular parallel structure that a human writer might vary more.

**Overall:** The text reads like a human who writes cleanly, not like an LLM pretending to be human. The residual patterns noted above are within normal range for a skilled human writer. Score held below 0.95 because the rhetorical regularity of the principles section is detectable under close inspection.

---

## Voice Authenticity

**Score: 0.82**

**What works:**
- The skiing metaphor is grounded and specific ("big-mountain skiing," "cliff in a banana suit," "bunny hill"). These are real McConkey references, not generic ski bro language.
- The opening cadence ("Alright, this trips up everybody, so don't feel singled out") sounds like someone talking to you, not writing at you.
- The closing dare is strong and in-character. McConkey would absolutely dare you to try something.
- "Point Downhill and Hope" as a section title is good ski-voice.

**What falls short:**
- The middle sections (Level 2, Level 3, Two-Session Pattern, Why This Works) shift into technical explainer mode. The voice becomes an articulate engineer explaining probability distributions, attention mechanisms, and context windows. McConkey's persona drops out almost entirely between "You don't need a flight plan for the bunny hill" (end of Level 2) and the closing paragraphs. That is roughly 60% of the article's body operating in a different register.
- The technical passages are well-written but they do not sound like a person who would ski a cliff in a banana suit. They sound like a senior ML engineer who happens to like skiing metaphors. There is a difference between "McConkey explaining tech" and "a tech writer who references McConkey."
- The article does not capture McConkey's irreverence in the technical sections. He was known for making the serious feel ridiculous and the ridiculous feel serious. The technical sections here are straight-faced and earnest. A more authentic voice would find ways to make the probability distribution explanation feel like it is coming from someone who thinks the whole thing is hilarious and important at the same time.
- No profanity, no self-deprecation, no moments where the voice admits it does not know something or got something wrong. McConkey's public persona included a willingness to look foolish. This article never risks that.

**Summary:** The framing device works. The bookend McConkey moments are well-executed. But the article's core is a technical explainer wearing a McConkey hat, not McConkey explaining technology. The voice is performative rather than inhabitated. A reader who knew McConkey would recognize the references but not the sustained voice.

---

## Verdict

| Metric | Score | Threshold |
|--------|-------|-----------|
| Weighted Composite | 0.877 | >= 0.95 (PASS) |
| Band | REJECTED | < 0.85 = REJECTED, 0.85-0.94 = REVISE |

**Verdict: REVISE**

The composite score of 0.877 falls in the REVISE band (0.85-0.94). The article is structurally sound and highly actionable but has specific weaknesses in evidence quality, traceability, and voice sustain that prevent it from reaching the 0.95 target.

---

## Top Improvements

### 1. Add Citations to Match the Article's Own Evidence Standard

The article tells readers to "require evidence or sources" but provides exactly one citation (Liu et al. 2023). Add specific references for: (a) the "fluency-competence gap" claim, (b) the LLM self-evaluation bias claim, (c) the chain-of-thought / structured prompting research claim. Even informal citations (author, year, paper title) would close the credibility gap. This directly impacts Evidence Quality (0.82) and Traceability (0.78), the two lowest-scoring dimensions.

### 2. Sustain the McConkey Voice Through Technical Sections

The voice drops out in the middle 60% of the article. Specific revision targets: (a) the probability distribution explanation in Level 1 needs McConkey's irreverence, not just his metaphors; (b) the Two-Session Pattern section reads like a blog post, not like a person talking; (c) the "Why This Works" section is the most generic-sounding part of the article. The goal is not to add more ski references but to sustain the conversational irreverence and willingness to be blunt that characterizes the opening and closing. This impacts Voice Authenticity (0.82) and would raise Internal Consistency by eliminating the register shift.

### 3. Address Failure Modes and Model-Specific Nuance

The article presents structured prompting as reliably effective but does not address when it fails, when to bail on a conversation and start over, or how different model architectures change the practical advice. Adding even a short section on "When This Breaks" would close a completeness gap that practitioners would notice. The two-session pattern in particular needs a caveat about models with persistent memory or project-level contexts where the token-budget argument does not apply in the same way. This impacts Completeness (0.88) and Methodological Rigor (0.87).
