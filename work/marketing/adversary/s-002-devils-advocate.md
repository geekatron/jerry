# S-002 Devil's Advocate — Marketing Deliverables

**Strategy:** S-002 Devil's Advocate
**Deliverables:** `work/marketing/medium-article.md`, `work/marketing/slack-message.md`
**Date:** 2026-02-24
**Reviewer:** adv-executor (S-002)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Findings Summary](#findings-summary) | Table of all challenged claims with severity and defensibility |
| [Detailed Analysis](#detailed-analysis) | Full Devil's Advocate challenge for each claim |
| [Meta-Consistency Check](#meta-consistency-check) | Whether the article practices what it preaches |
| [Overall Assessment](#overall-assessment) | Verdict and required revisions |

---

## Findings Summary

| ID | Claim | Deliverable | Severity | Defensibility | Category |
|----|-------|-------------|----------|---------------|----------|
| DA-01 | Structured prompting works across "every major model family" | Medium article, Slack | CRITICAL | WEAK | Model universality |
| DA-02 | "Level 3 gets you work that survives scrutiny" | Slack | CRITICAL | WEAK | Guarantee claim |
| DA-03 | RLHF "amplifies sycophantic tendencies" applies universally and currently | Medium article, Slack | MAJOR | MODERATE | Citation scope |
| DA-04 | Wei et al. (2022) chain-of-thought findings justify knowledge-work prompting advice | Medium article | MAJOR | MODERATE | Citation scope |
| DA-05 | Liu et al. (2024) "Lost in the Middle" applies to conversational planning sessions | Medium article (buried), Slack (uncaveated) | MAJOR | WEAK | Citation scope |
| DA-06 | "Fluency-competence gap" is a well-grounded concept anchored to Bender & Koller | Medium article, Slack | MAJOR | MODERATE | Citation accuracy |
| DA-07 | Level 1 prompting reliably produces "polished garbage" | Medium article, Slack | MAJOR | MODERATE | Categorical overclaim |
| DA-08 | "You'll see the difference immediately" (Level 2 baseline) | Medium article | MAJOR | WEAK | Unqualified promise |
| DA-09 | The two-session pattern's mechanism is established by Liu et al. | Medium article | MINOR | MODERATE | Citation scope |
| DA-10 | "Structure in, structure out" as a universal maxim | Slack | MINOR | MODERATE | Over-constraining blind spot |
| DA-11 | Bender & Koller (2020) empirically demonstrated the fluency-competence gap | Medium article (foundational claim) | MINOR | MODERATE | Theoretical vs. empirical |
| DA-12 | Self-critique in Level 3 adds meaningful quality control | Medium article | MINOR | STRONG | Methodology |

---

## Detailed Analysis

### DA-01: "Every Major Model Family" — Universal Claim Without Methodology

**The claim:**
- Medium article: "In my experience, this holds across every major model family I've tested."
- Medium article: "This trips up everybody. What I'm about to walk through applies to Claude, GPT, Gemini, Llama — every model I've tested, and likely whatever ships next Tuesday."
- Slack (Longer): "Works on Claude, GPT, Gemini, Llama — every model I've tested."

**The strongest counterargument:**
This is the most consequential empirical claim in both deliverables, and it is backed by zero disclosed methodology. "Every model I've tested" is a personal assertion without test count, task categories, success criteria, failure rate data, or disclosure of which model versions were evaluated. The claim cannot be verified, replicated, or falsified by the reader.

There are well-documented cases where structured prompting produces marginal or negative effects: models with instruction-following fine-tuning sometimes over-index on explicit constraints in ways that degrade output quality (format fixation); very capable models (e.g., GPT-4o, Claude 3.5 Sonnet) often produce high-quality output from vague prompts on routine tasks, making the Level 1 vs. Level 2 delta small or invisible. Llama-7B and GPT-4o are not comparable systems — testing both and reporting that "structure helps" elides enormous variation in baseline capability that determines how much prompting discipline matters.

The claim also asserts forward universality: "likely whatever ships next Tuesday." Models are becoming increasingly capable of inferring user intent and generating structured reasoning without explicit prompting. The trend in frontier model development is toward reduced dependence on elaborate prompt engineering. A claim of forward universality has no evidentiary basis.

**Defensibility: WEAK.** The claim is presented with confident universality but rests on undisclosed personal testing. A skeptical practitioner will immediately recognize this as anecdote dressed as evidence. The "in my experience" qualifier in one sentence is undercut by the unqualified "applies to Claude, GPT, Gemini, Llama" enumeration in the next.

**Severity: CRITICAL.** This is the load-bearing claim for the entire article's authority. If structured prompting is model-dependent, task-dependent, or capability-dependent (which it is), then the prescriptive guidance is not universally applicable. Readers who encounter failure cases will feel misled, and the framing gives them no tools to understand when the advice doesn't apply.

---

### DA-02: "Level 3 Gets You Work That Survives Scrutiny" — Contradicts Own Caveats

**The claim:**
- Slack (Longer): "Level 3 gets you work that survives scrutiny."

**The strongest counterargument:**
This is a near-guarantee. "Survives scrutiny" implies the output is reliable, accurate, and defensible under examination. The Medium article's "When This Breaks" section explicitly states: "Sometimes you write a beautifully constrained prompt and the model hallucinates a source that doesn't exist, or applies a framework to the wrong part of your codebase, or confidently delivers something internally consistent and completely wrong." The article correctly notes that "Structure reduces the frequency of those failures. It doesn't eliminate them."

The Slack version discards this qualification entirely. A practitioner who reads the Slack, acts on "survives scrutiny" as an expectation, and then produces a Level 3 output that fails under review has been set up for a credibility problem. More importantly, this claim is an internal contradiction: the same author who wrote that structure doesn't eliminate errors is now asserting a level of quality that implies errors have been substantially eliminated.

The claim also has no reference class. Survives whose scrutiny? At what standard? For what task? A Level 3 prompt for a codebase analysis still depends on the model having accurate knowledge of the frameworks being applied. If the model's training data contains errors about those frameworks, structured prompting will produce a well-organized, well-sourced analysis that is still wrong.

**Defensibility: WEAK.** This claim directly contradicts the Medium article's own caveats. There is no version of "survives scrutiny" that is consistent with the acknowledged failure modes in the source content.

**Severity: CRITICAL.** A reader who acts on this claim and experiences failure will have no framework for understanding why Level 3 still failed them, because the Slack gave them no caveat to absorb. This is the highest-risk claim for eroding reader trust.

---

### DA-03: RLHF Sycophancy Claim — Scope and Currency Problems

**The claim:**
- Medium article: "Sharma et al. (2024) found that RLHF...amplifies sycophantic tendencies: models learn to agree with users rather than push back, even when the user is wrong."
- Slack (Short): "RLHF amplifies sycophantic tendencies — models learn to agree with you rather than push back, even when you're wrong."

**The strongest counterargument:**
Three problems compound here.

First, currency. Sharma et al. was published in 2024 (ICLR), but the research was conducted on models that predate current alignment work. Since that paper, Anthropic, OpenAI, and Google have substantially invested in sycophancy reduction through Constitutional AI, RLAIF, and adversarial training techniques. Presenting sycophancy as a current, stable property of all RLHF-trained models glosses over ongoing mitigation work that has measurably reduced the behavior in frontier models.

Second, scope. Sharma et al. studied sycophancy under specific elicitation conditions: users expressing incorrect opinions before asking questions, and models being challenged after giving correct answers. The finding is real and the paper is rigorous. But the Slack universalizes it: "models learn to agree with you...even when you're wrong" implies this is a general, always-present behavior across all interactions. The paper demonstrates sycophancy is elicitable and measurable, not that it pervades all model responses.

Third, mechanism. The Medium article's earlier draft (captured in the blog source) characterized RLHF as "rewarding confident-sounding responses over accurate ones." This is a characterization of RLHF's reward function that goes beyond what Sharma et al. measured. RLHF optimizes for human preference ratings across many signals including accuracy, safety, and helpfulness. Sycophancy is a side effect of human rater preferences, not the intended target of the reward function.

**Defensibility: MODERATE.** The citation is real and the core finding is accurately described. The problems are in scope (specific conditions presented as universal) and currency (ongoing mitigation work not acknowledged). The Medium article's treatment is defensible; the Slack's unqualified version is not.

**Severity: MAJOR.** A technically literate reader familiar with current alignment research will recognize that this is a 2024 finding presented as a timeless property of all RLHF-trained models.

---

### DA-04: Wei et al. (2022) Chain-of-Thought — Benchmark-to-Practice Leap

**The claim:**
- Medium article: "Wei et al. (2022) demonstrated this with chain-of-thought prompting: adding intermediate reasoning steps to a prompt measurably improved performance on arithmetic, commonsense, and symbolic reasoning tasks. Their work studied specific reasoning benchmarks, but the underlying principle — constrain the input, get more reliable output — holds in my experience across every prompting scenario I've tested."

**The strongest counterargument:**
Wei et al. is a genuine landmark paper. The findings are correctly stated: chain-of-thought prompting improves performance on GSM8K (math word problems), AQuA (algebraic reasoning), StrategyQA, and similar closed-ended benchmarks with verifiable answers. These tasks have objective ground truth. The improvement is measurable because right and wrong are unambiguous.

The article applies this to: parallel work streams on codebase analysis, multi-phase professional knowledge work, research synthesis, and open-ended technical assessment. These tasks have no objective ground truth. "Improvement" in these contexts is user-perception-dependent, evaluator-dependent, and context-dependent. A benchmark finding that "adding intermediate reasoning steps improves arithmetic performance" does not generalize to "adding a plan review step improves codebase analysis quality" without a bridging study. The mechanisms are different: arithmetic benefits from intermediate steps because the steps are checkable and computable; knowledge work benefits from planning because it reduces scope ambiguity, which is a different mechanism.

The article acknowledges the task scope limit ("their work studied specific reasoning benchmarks") and then overrides it ("the underlying principle...holds in my experience"). This is a well-constructed rhetorical move: acknowledge the limitation, then re-assert the generalization via personal experience. It reads as more honest than it is.

**Defensibility: MODERATE.** The citation is accurate and the paper is legitimate. The extrapolation is the problem. The article's partial acknowledgment of the task scope limit softens the overclaim but does not resolve it.

**Severity: MAJOR.** Wei et al. is the primary empirical anchor for Level 2 advice. If the benchmark-to-practice generalization is contested, the evidential basis for "constrain the ask" is reduced to personal experience. This is recoverable with stronger qualifying language, but the current framing implies more empirical backing than exists.

---

### DA-05: Liu et al. "Lost in the Middle" — Retrieval Finding Applied to Conversational Context

**The claim:**
- Medium article: "Liu et al. (2024) found that in document retrieval tasks, models pay the most attention to what's at the beginning and end of a long context, and significantly less to everything in the middle. The conversational case hasn't been studied as rigorously, but the implication tracks..."
- Slack (Longer): "...at least one study on document retrieval found models attend more to the beginning and end of long contexts than the middle. Your carefully crafted instructions from message three are competing with forty messages of planning debate, and the model isn't weighing them evenly."

**The strongest counterargument:**
The Medium article handles this citation better than the Slack. "The conversational case hasn't been studied as rigorously, but the implication tracks" is an honest hedge. The Slack strips the hedge entirely and asserts the retrieval finding directly applies to conversational planning sessions.

What Liu et al. actually measured: multi-document question answering where a relevant document was placed at varying positions within a concatenated context. They found accuracy degrades when the relevant document is in the middle. This is specifically about information retrieval from a structured context, not about instruction-following across a multi-turn conversation.

The conversational case is meaningfully different: conversation turns are not equivalent to documents in a concatenated context; models may weight recent conversational turns differently than they weight document position; instruction-following may be more robust to conversational depth than document retrieval; frontier models have been specifically fine-tuned for long-context instruction-following in ways that partially mitigate the retrieval finding.

Additionally, the practical claim ("your carefully crafted instructions from message three are competing with forty messages") is an extrapolation that assumes the planning debate has equal token weight to the instruction. In practice, a user's instructions often occur at the beginning of a conversation (the most attended position), making the retrieval finding work against the article's conclusion, not for it.

**Defensibility: WEAK.** The Slack version's use is indefensible: it removes the retrieval qualifier and presents the finding as directly applicable to conversational context. The Medium article's caveat is better but the "implication tracks" framing still understates how different the experimental context is.

**Severity: MAJOR.** The two-session pattern is the most distinctive and actionable recommendation in the piece. If its primary empirical justification does not apply to conversational contexts, the recommendation is left standing on intuition alone (which might be enough, but should be stated as such).

---

### DA-06: "Fluency-Competence Gap" — Author-Coined Concept, Citation Does Not Establish It

**The claim:**
- Medium article: "I call it the fluency-competence gap — a shorthand I started using after reading Bender and Koller's 2020 argument that language models learn linguistic form without grounding in meaning."

**The strongest counterargument:**
The author explicitly claims ownership ("I call it"), which is honest. The problem is that the term is then used throughout both deliverables as if it names a recognized phenomenon, and the Bender & Koller citation is positioned as its evidential foundation.

Bender & Koller (2020) — "Climbing Towards NLU" — is a theoretical linguistics and philosophy-of-mind paper. It argues through the "Octopus Test" thought experiment that a system trained purely on linguistic form cannot acquire semantic grounding. This is a contested position in NLP: researchers like Piantadosi (2023) and others have argued that rich distributional representations can ground meaning in ways Bender & Koller did not anticipate. The paper did not measure "fluent but inaccurate" output rates in professional contexts. It did not test whether prompting quality changes how often models produce authoritative-sounding incorrect output.

The article uses a theoretical, contested philosophical argument as empirical backing for a practical prompting observation. The observation itself may be correct (models do produce authoritative-sounding incorrect output), but the Bender & Koller citation provides philosophical context, not empirical confirmation.

**Defensibility: MODERATE.** The author's disclosure ("I call it") partially immunizes this claim. The problem is using a contested theoretical paper as the evidential anchor for a practical recommendation framework. A technically sophisticated reader will recognize that Bender & Koller does not establish what the article implies it establishes.

**Severity: MAJOR.** This is the conceptual foundation of the piece. If the "fluency-competence gap" is just an author-coined label for a personal observation, the article's authority rests on practitioner experience rather than established research. That is not necessarily wrong, but it should be stated as such.

---

### DA-07: "Level 1 Gets You Polished Garbage" — Categorical Negative

**The claim:**
- Slack: "Level 1 gets you polished garbage."
- Medium article (more nuanced): "It will look like an answer. That's the dangerous part."

**The strongest counterargument:**
"Polished garbage" is rhetorically effective but empirically untenable as a categorical claim. Level 1 prompting is not uniformly bad. The magnitude of the quality gap between Level 1 and Level 2 depends critically on:

- Task complexity: a Level 1 prompt for "draft a thank-you email" produces adequate output; a Level 1 prompt for "analyze this codebase against SOLID principles" may not
- Model capability: GPT-4o and Claude 3.5 Sonnet handle ambiguous prompts with substantially more inference about user intent than earlier models
- Domain knowledge: if the model's training data contains accurate knowledge about the domain, even an unstructured prompt can produce accurate output
- User review: if the output is reviewed before use, the "polished garbage" framing only holds when the user cannot recognize the garbage — which depends on user expertise, not prompt structure

The Slack's categorical "Level 1 gets you polished garbage" will be immediately falsified in the experience of any reader who uses Level 1 prompts for tasks where output quality is adequate. That reader will then discount the rest of the advice.

**Defensibility: MODERATE.** The claim is defensible for high-stakes technical analysis tasks with specific accuracy requirements. It is not defensible as a categorical statement applying to all Level 1 prompts across all tasks and models.

**Severity: MAJOR.** This framing creates the need for Level 2 and Level 3. If the claim is falsified in a reader's personal experience, the article's premise collapses. The Medium article's more nuanced framing ("dangerous" rather than "garbage") is substantially more defensible.

---

### DA-08: "You'll See the Difference Immediately" — Unqualified Temporal Promise

**The claim:**
- Medium article: "Get these three right and you'll see the difference immediately."

**The strongest counterargument:**
"Immediately" sets an expectation of rapid, obvious, unambiguous quality improvement visible on first application. This cannot be guaranteed because:

- Improvement visibility depends on whether the reader can evaluate LLM output quality. A reader without domain expertise may not recognize that a more constrained prompt produced a better answer.
- Task selection matters: on tasks where Level 1 already produces adequate output, Level 2 produces marginal improvement that is not "immediate" or obvious.
- Model-specific behavior varies: some models respond more dramatically to constraint than others.
- The improvement may require multiple applications before it becomes visible — the first structured prompt may still fail for reasons unrelated to structure.

The "immediately" framing also sets up a credibility trap: if a reader applies the Level 2 checklist and does not see an obvious difference, they conclude the advice doesn't work, rather than that the improvement is real but subtle on their specific task.

**Defensibility: WEAK.** There is no basis for a blanket temporal promise. The improvement is real for many tasks and contexts; "immediately" overstates the reliability and visibility of that improvement.

**Severity: MAJOR.** This claim sets an expectation that will not hold for a meaningful fraction of readers, particularly those applying the advice to tasks where Level 1 is already adequate. When the expectation fails, reader trust in the broader framework is damaged.

---

### DA-09: Two-Session Pattern — Liu et al. Justification is Extrapolated

**The claim:**
- Medium article: The two-session pattern is mechanistically justified by Liu et al.'s attention findings and the "cognitive modes" argument.

**The strongest counterargument:**
As challenged in DA-05, Liu et al. studied document retrieval, not conversational instruction-following. The mechanism invoked does not directly support the conversational case. The "cognitive modes" argument is intuitive framing ("planning and execution are different cognitive modes"), not an empirically established claim about LLM processing.

The two-session pattern may be genuinely useful for the reasons the article describes: plan artifacts force clarity, a clean context reduces noise, and separating review from execution creates a natural quality gate. These are plausible arguments from first principles. The problem is that the Liu et al. citation is used to make these intuitive arguments look more empirically grounded than they are.

A skeptic would also note: modern frontier models have context windows large enough (128K–1M tokens) that 40 planning messages constitute a small fraction of the available context. The "competing with forty messages" framing assumes the model's attention is resource-constrained by planning conversation length, which is increasingly untrue at current context window sizes.

**Defensibility: MODERATE.** The two-session recommendation has reasonable intuitive justification that stands on its own. The Liu et al. citation as mechanical support is the weak link. The pattern's practical value is plausible; the specific mechanism invoked is extrapolated.

**Severity: MINOR.** The recommendation itself is not undermined by the citation weakness. A reader who finds the pattern useful will adopt it regardless of whether the Liu et al. mechanism is the actual reason it works.

---

### DA-10: "Structure In, Structure Out" — Over-Constraining Not Acknowledged

**The claim:**
- Slack: "Structure in, structure out."
- Medium article (implicit throughout): adding constraints monotonically improves output.

**The strongest counterargument:**
The article's implicit model is that structure is additive: more constraints produce better output. This is true up to a point. Over-constraining prompts is a documented failure mode in prompt engineering practice:

- Specifying output format too rigidly can cause models to force-fit content to the format, producing technically compliant but substantively degraded output
- Adding many evaluation criteria to a single prompt can cause compliance with some criteria at the expense of others the model deprioritizes
- Long, complex prompts increase the probability of contradictory instructions that the model must resolve in arbitrary ways

The Medium article's "When This Breaks" section mentions exploratory tasks as cases to reduce structure. But it does not address over-constraining as a failure mode for analytical tasks where the article's primary recommendations apply.

**Defensibility: MODERATE.** The "structure in, structure out" aphorism is defensible as a heuristic for the transition from Level 1 to Level 2. It becomes less defensible when applied to the transition from Level 2 to Level 3, where the risk of over-specification increases.

**Severity: MINOR.** The Medium article's caveats partially address this. The Slack's aphorism is incomplete, but it is a marketing compression, not a technical claim.

---

### DA-11: Bender & Koller — Theoretical Argument Treated as Empirical Validation

**The claim:**
- Medium article: Using Bender & Koller (2020) as the citation anchor for the fluency-competence gap concept.

**The strongest counterargument:**
Bender & Koller made a philosophical argument about linguistic grounding, not an empirical study of LLM output quality in professional contexts. The "Octopus Test" is a thought experiment, not an experiment. The paper's conclusions are also contested within NLP: the distributional semantics literature and subsequent work on emergent capabilities suggest that rich representations can ground meaning in ways the paper's theoretical framework did not anticipate.

Using a contested theoretical paper as the citation for a practical claim creates a specific vulnerability: a reader who knows the Bender & Koller debate will recognize that the citation provides theoretical context, not empirical confirmation of the fluency-competence gap as the article uses it.

**Defensibility: MODERATE.** The citation is directionally relevant and the author is transparent about coining the term. The theoretical-to-practical slide is the issue, not the citation itself.

**Severity: MINOR.** This is a supporting citation for a named concept, not the primary evidence for a behavioral recommendation. The practical advice is independently justifiable.

---

### DA-12: Self-Critique in Level 3 — Acknowledged Limitation, Still Recommended

**The claim:**
- Medium article: "That self-critique step. Panickssery et al. (NeurIPS 2024) showed that LLMs recognize and favor their own output, rating it higher than external reviewers do. Self-critique in the prompt is useful as a first pass. It's not a substitute for your eyes on the output."

**The strongest counterargument:**
This is actually the most intellectually honest claim in the article. The author cites a specific finding that undermines their own recommendation (self-critique has known biases) and then accurately qualifies the recommendation (useful as a first pass, not a substitute for human review). The Devil's Advocate struggles to mount a strong challenge here.

The counterargument that remains: if self-critique is demonstrably biased toward the model's own output (per Panickssery et al.), why include it in the Level 3 recipe at all? The article's framing suggests it's a meaningful quality step, but the citation implies it has limited value relative to what practitioners might expect from "critique your own work." A skeptic could argue that including biased self-critique gives practitioners false confidence that a quality check has been applied.

**Defensibility: STRONG.** The article handles this with appropriate qualification. The inclusion of a citation that undermines the recommendation while accurately framing the limitation is a mark of intellectual honesty that increases the piece's overall credibility.

**Severity: MINOR.** This is the weakest challenge in the set. The article's treatment is sound.

---

## Meta-Consistency Check

**Does the article practice what it preaches?**

The article's three principles are: (1) constrain the work, (2) review the plan before the product, (3) separate planning from execution. Applying these to the article itself:

**Principle 1 — Constrain the work (define what good looks like):**
The article defines "good" prompting by outputs, not by measurable quality criteria. It does not define what "survives scrutiny" means, what a passing score on completeness/consistency/evidence looks like, or what failure rate reduction quantifies as. By the article's own standard, the reader is left to infer quality criteria — exactly what the article warns against in Level 1 prompting.

**Meta-consistency verdict: PARTIAL FAIL.** The article tells readers to define quality criteria but does not define quality criteria for the outcomes it promises (Level 2 "difference immediately," Level 3 "survives scrutiny"). The irony is real and a skeptical reader will notice it.

**Principle 2 — Review the plan before the product:**
The article does not show a plan. It presents conclusions. If the author used their own Level 3 methodology to write this article, the execution plan is not disclosed. The article instructs readers to demand plan transparency from the model but provides none of its own.

**Meta-consistency verdict: MINOR FAIL.** For a blog post, this is a reasonable compression. But a technically precise reader applying the article's own standards would note the absence.

**Principle 3 — Separate planning from execution:**
Unknown from the deliverable alone. No way to assess whether the article was produced in one or two sessions.

**Overall meta-consistency rating: The article partially fails its own standards.** The most significant inconsistency is telling readers to define quality criteria ("tell it how you'll evaluate the result") while using unqualified quality claims in its own conclusions. This is a meaningful finding because it gives a skeptic a meta-level argument: if the author cannot apply their own principles to their own writing, why should readers trust the principles?

---

## Overall Assessment

### Verdict: ACCEPT WITH REVISIONS

### Rationale

The core practical advice in both deliverables is sound. The three-level framework is a genuine and useful taxonomy. The two-session pattern is a non-obvious, actionable recommendation with plausible justification. The citations are all real papers with correctly described findings. The Medium article demonstrates intellectual honesty in its "When This Breaks" section and in its handling of the self-critique limitation. These strengths are real and substantive.

However, Devil's Advocate identifies two CRITICAL findings and six MAJOR findings that create meaningful credibility risks with technical and skeptical audiences:

**The two CRITICAL findings must be resolved before publication:**

- **DA-01** (universal model claim): "Every major model family I've tested" is an anecdote assertion masquerading as evidence. It is the load-bearing claim for the article's authority and cannot be verified. Required revision: add qualifying language that scopes the claim to task types and model capability tiers, or replace with a more honest framing of personal practitioner experience.

- **DA-02** (Level 3 "survives scrutiny"): This Slack claim directly contradicts the Medium article's explicit caveats. Required revision: replace with something consistent with the article's own acknowledgment that structure reduces failure frequency but does not eliminate it.

**The Slack message is the weaker deliverable.** It systematically strips the caveats that give the Medium article its intellectual credibility: the Liu et al. retrieval qualification, the self-critique limitation, the "When This Breaks" acknowledgment, and the nuanced RLHF framing. What remains in the Slack is a sequence of strong, unqualified claims that will be falsified in the experience of technically sophisticated readers.

**The citation strategy trades precision for legitimacy.** Every citation is real and directionally relevant. But each is used somewhat beyond its demonstrated scope: a theoretical linguistics paper anchors a practical prompting concept, arithmetic benchmark findings justify knowledge-work prompting advice, document retrieval attention patterns justify a conversational session management recommendation. A reader who checks these citations will find the papers are real but the extrapolations are the author's own inferences. The article would be strengthened by being more explicit about where citation findings end and author inference begins.

### Required Revisions for Acceptance

| Priority | Deliverable | Change Required |
|----------|-------------|-----------------|
| 1 (CRITICAL) | Slack | Change "Level 3 gets you work that survives scrutiny" to "Level 3 substantially reduces structural failure rate and creates checkpoints to catch errors before they compound" |
| 2 (CRITICAL) | Slack, Medium | Qualify "every model I've tested" with scope: task type (analysis, research, multi-step reasoning) and acknowledgment that results vary by model capability tier |
| 3 (MAJOR) | Slack | Add retrieval-only qualifier to Liu et al. citation; restore the "conversational case hasn't been studied as rigorously" hedge |
| 4 (MAJOR) | Medium | Change "you'll see the difference immediately" to "you'll see the difference on tasks requiring analysis, research, or multi-step reasoning" |
| 5 (MAJOR) | Slack | Add one qualifying sentence after "Level 1 gets you polished garbage" to scope the claim to high-stakes technical tasks |
| 6 (META) | Both | Add one sentence acknowledging structured prompting involves tradeoffs (more upfront effort) to give the advice more credibility with practitioners who know there are no free lunches |

### Severity Distribution

| Severity | Count | Findings |
|----------|-------|---------|
| CRITICAL | 2 | DA-01, DA-02 |
| MAJOR | 6 | DA-03, DA-04, DA-05, DA-06, DA-07, DA-08 |
| MINOR | 4 | DA-09, DA-10, DA-11, DA-12 |

The required revisions are targeted and achievable without restructuring either deliverable. The underlying content is strong enough to survive a skeptical technical audience once the universal claims are scoped and the Slack's stripped caveats are partially restored.

---

*Executed by: adv-executor (S-002 Devil's Advocate)*
*Date: 2026-02-24*
*Next strategy: see adversary output directory for remaining strategy reports*
