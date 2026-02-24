# S-003 Steelman Technique — Marketing Deliverables

**Strategy:** S-003 Steelman Technique
**Deliverables:** `work/marketing/slack-message.md`, `work/marketing/medium-article.md`
**Date:** 2026-02-24
**Reviewer:** adv-executor (S-003)

---

## Medium Article Steelman

### Core Thesis (Strongest Form)

The article's core thesis, rendered in its strongest form:

> **LLM output quality is not a model problem — it is a specification problem. The fluency-competence gap is structural and universal across all model families. Because models predict the most probable token given context, vague instructions systematically produce confident-but-unconstrained output. The only reliable remedy is explicit, multi-dimensional constraint: specify the task, the evidence standard, and the quality criteria before the model does anything. At sufficient complexity, separate the planning mode from the execution mode across distinct context windows to prevent attentional dilution and planning-execution interference.**

This is an unusually strong thesis for a practitioner post because it is: (a) mechanistically grounded — it explains *why* the failure mode exists at the architecture level, not merely *that* it exists; (b) scope-limited with integrity — the author explicitly names the conditions under which the framework breaks down; and (c) falsifiable — the three-level taxonomy creates a testable claim that each level produces meaningfully different output.

### Strongest Arguments

**1. The fluency-competence gap as the lead concept**

The article opens by naming the core failure mode before prescribing the remedy. This is the correct rhetorical order: establish the problem the reader already experiences, give it a name, then explain why it happens. The Bender and Koller (2020) citation is precisely appropriate — their argument about form without meaning is exactly what "fluency-competence gap" operationalizes, lending academic credibility to an observation practitioners make intuitively. The Sharma et al. (2024) RLHF-sycophancy finding compounds this well: not only do models sound confident without grounding, but RLHF *amplifies* the tendency to mirror user assumptions. Together these two citations construct a mechanistic argument, not just an anecdotal one.

**2. The three-level taxonomy is practically actionable with clear entry costs**

Level 1 / Level 2 / Level 3 maps cleanly to effort cost: Level 2 is positioned as "two or three sentences more specific" — a deliberately low barrier. The article correctly identifies that most practitioners will get 80% of the benefit from Level 2 alone, and says so explicitly ("For most day-to-day work, that's honestly enough"). This prevents over-prescribing and makes the framework feel honest rather than promotional. Level 3 is presented as proportionate to risk, not as the default — a position that survives scrutiny because the rationale (pipeline error compounding) is structurally sound.

**3. The two-session pattern is the article's most differentiated insight**

The recommendation to separate planning from execution across distinct context windows is the insight most likely to be novel to a practitioner audience. The Liu et al. (2024) "lost in the middle" finding provides empirical backing for a principle that otherwise sounds like process ceremony. The article correctly identifies and names the tradeoff ("You do lose the back-and-forth nuance. That's real.") — this acknowledgment is a strength, not a concession, because it pre-empts the most obvious objection and demonstrates that the author has actually used the technique rather than theorized it.

**4. Research citation pattern is honest about scope**

The article consistently distinguishes between "what the research actually studied" and "what I observe in practice." For example, on Liu et al.: "They studied retrieval tasks, but the attentional pattern applies here too." This epistemically honest extension — acknowledging the gap between study conditions and claim scope — is rare in practitioner writing and significantly raises credibility with technically sophisticated readers. The Panickssery et al. treatment is especially well-handled: the author recommends self-critique in the prompt while immediately noting research shows LLMs rate their own output higher than external reviewers do. This is intellectually honest self-undermining that actually strengthens the recommendation by showing the author's reasoning is not naive.

**5. The "When This Breaks" section is a structural differentiator**

Practitioner posts almost never include an honest failure modes section. Including one signals authorial confidence — only writers who believe their framework is genuinely useful can afford to scope it down. The specific failure modes named (hallucinated sources, wrong-part-of-codebase application, internally-consistent-but-wrong output) are accurate and recognizable. The guidance to decompose work when three revision passes fail is practical and correct. This section functions as a preemptive steelman of counterarguments, which is the strongest rhetorical position.

**6. The three-principle summary is portable**

"Constrain the work. Review the plan before the product. Separate planning from execution." — three principles that can be remembered and applied without re-reading the article. The summary checklist at the end operationalizes these into five binary questions. This structure supports adoption: the article gives practitioners something they can use immediately (Level 2 checklist) and something to grow into (Level 3 + two-session pattern).

### Defensive Positions (Already Robust)

The article is already well-defended against the following lines of attack:

- **"This is model-specific"** — Preemptively addressed: "This trips up everybody... applies to Claude, GPT, Gemini, Llama... It's not a vendor thing." The model-agnosticism claim is also mechanistically explained rather than asserted.
- **"Your citations don't perfectly support your claims"** — The article explicitly flags where claims extend beyond the specific research conditions (e.g., Liu et al. retrieval vs. conversational context). This limits exposure to the accusation of overclaiming.
- **"Self-critique doesn't work"** — The Panickssery et al. citation is cited *against* the author's own recommendation, with the nuance that self-critique is a first-pass tool, not a substitute for human review. This is already the steelman treatment of the counterargument.
- **"This is too complex / overkill"** — The article explicitly provides the off-ramp: "For most day-to-day work, that's honestly enough. You don't need a flight plan for the bunny hill." The Level 2 checklist is designed for immediate low-friction adoption.
- **"Structure kills creativity"** — The "When This Breaks" section names exploratory and creative tasks as domains where the framework should be backed off. This is already incorporated.

### Leverage Opportunities

These are the article's strongest assets that could be pushed further:

1. **The garbage-compounding metaphor** ("garbage in, increasingly polished garbage out") is the most memorable formulation in the piece. It currently appears once, in the Level 3 section. It is strong enough to anchor the article's value proposition more prominently — potentially as a section header or pull quote.

2. **The two-session pattern** is the most novel and differentiated insight, but the structural reason it works (cognitive mode separation in addition to attentional dilution) is somewhat buried. The "planning and execution are different cognitive modes" observation is underdeveloped relative to its importance.

3. **The five-question checklist** at the end is immediately actionable but appears only at the close of a long article. Practitioners who skim will miss it. It could function as a stronger call to action.

4. **The author's voice ("In my experience," "every model I've tested")** grounds the framework in practitioner authority without overclaiming from research. This credential-by-practice is a differentiator in a space crowded with academic summaries. The opening hook — naming the fluency-competence gap as "a shorthand I started using" — signals original thinking, which is the article's strongest positioning signal.

---

## Slack Message Steelman

### Core Thesis (Strongest Form)

> **LLM output quality is a function of constraint specification, not model selection. The fluency-competence gap — models that sound expert without being expert — is addressable at any scale through three progressive levels of prompting structure. The two-session pattern (plan then execute in a fresh context) addresses a structural attentional limitation in all current models.**

The short version executes this thesis in four sentences, each load-bearing. The longer version extends with a practitioner analogy (McConkey preparation vs. performance) that maps cleanly to the framework's core principle: the disciplined work underneath produces the quality output.

### Strongest Arguments

**Short version:**

1. **The opening hook is a pattern interrupt** — "Your LLM output looks authoritative. Clean headings, professional language, confident tone. Except it's a mirage." The three-sentence sequence sets up the problem efficiently. Slack audiences skim; this structure rewards skimming because the first line hooks and the third delivers the payload.

2. **The fluency-competence gap is named and explained in one sentence** — "models learn to *sound* like they understand without actually understanding." This is the highest-density summary of the concept. For a Slack context, naming the phenomenon gives readers a vocabulary item to carry out of the message, which increases sharing and recall.

3. **The level taxonomy is usable at Slack message density** — Three levels, each described in one clause: "polished garbage / something you can actually use / work that survives scrutiny." These are practitioner-grade outcome descriptions, not feature descriptions. "Survives scrutiny" is particularly strong — it names the real standard of care.

4. **The closing line is the article's thesis compressed to a sentence** — "The difference isn't the model. It's what you told it about what good looks like." This is the most transferable formulation of the core argument and is already positioned as the message's conclusion.

**Longer version:**

5. **The McConkey analogy is well-deployed** — McConkey showed up looking unhinged and won on discipline underneath. The analogy maps: LLM outputs look expert (surface) but need structured prompting discipline (underneath) to actually be expert. The analogy works because it inverts the reader's expectation — the competent thing looks casual, and the casual-looking thing (the vague prompt) is actually the undisciplined choice.

6. **The two-session pattern is explained with the Liu et al. finding included** — "at least one study on document retrieval found models attend more to the beginning and end of long contexts than the middle." The epistemic hedge ("at least one study," "document retrieval") preserves honesty about scope while conveying the mechanism. This is appropriate calibration for a Slack context where precision would be verbose.

7. **Cross-model universality claim is stated with evidence** — "Works on Claude, GPT, Gemini, Llama — every model I've tested. Structure in, structure out." The "every model I've tested" grounds the claim in practitioner experience rather than vendor assurance.

### Defensive Positions

- **"This is just hype for the blog post"** — The Slack message provides substantive standalone value (the three-level taxonomy, the fluency-competence gap concept, the Liu et al. finding) before linking out. A reader who doesn't click still gets something actionable.
- **"The McConkey analogy is forced"** — The analogy is present in the source blog post and is not fabricated for promotional effect. The preparation-vs-performance frame maps directly to the structure-vs-output distinction in the framework.
- **"You're overclaiming universality"** — The short version cites actual research (RLHF sycophancy), and the longer version hedges the Liu et al. application correctly. The "every model I've tested" qualifier on the universality claim is practitioner-scope, not research-scope.

---

## Overall Strength Assessment

**Combined thesis strength:** The medium article and Slack message share a single coherent argument and execute it at different densities without contradicting each other. The Slack message's "The difference isn't the model. It's what you told it about what good looks like" is the compressed form of the article's full argument — a strong signal that both pieces are working from a clear core thesis.

**Research citation quality:** The article's citation pattern is the primary trust signal. Five peer-reviewed citations, all genuinely relevant, all scoped honestly. The Panickssery citation is the strongest example of this: the author recommends self-critique while citing evidence that self-critique is systematically biased — a position that could only be reached by someone who actually read the paper rather than pattern-matched to a supporting quote.

**Audience calibration:** The article is calibrated for a practitioner audience (software engineers, ML engineers, technical product managers) who have real LLM workflows and have experienced the fluency-competence gap firsthand without having named it. The Slack message is calibrated for a slightly broader technical audience who may be skimming. Both calibrations are internally consistent.

**Structural integrity:** The medium article's three-level taxonomy, two-session pattern, and five-question checklist form a coherent system. The Slack message summarizes the system accurately. Neither oversells the framework (both include explicit failure modes), which is the strongest defensive position against "this is just AI hype" criticism.

**Overall steelman score:** The deliverables are substantively strong. The core thesis is well-supported, the research grounding is honest, the practitioner voice is credible, and the framework is internally consistent. The primary leverage opportunities identified above (garbage-compounding metaphor visibility, two-session pattern depth, checklist positioning) represent enhancement opportunities on an already sound foundation, not structural gaps requiring correction.
