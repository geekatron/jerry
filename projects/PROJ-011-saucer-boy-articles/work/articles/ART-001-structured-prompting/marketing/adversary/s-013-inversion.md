# S-013 Inversion Technique — Marketing Deliverables

**Strategy:** S-013 Inversion Technique
**Deliverables:** `work/marketing/slack-message.md`, `work/marketing/medium-article.md`
**Source:** `docs/blog/posts/why-structured-prompting-works.md`
**Date:** 2026-02-24
**Reviewer:** adv-executor (S-013)

---

## Inversions Summary Table

| # | Original Claim | Inverted Claim | When Is Inversion True? | Severity | Blind Spot Revealed |
|---|---|---|---|---|---|
| 1 | Structured prompting produces better output | Structure produces worse output | Creative, exploratory, or emotionally-toned tasks; over-constrained prompts where user's frame is wrong | MAJOR | Article treats "better" as universal; ignores task classes where structure degrades output or amplifies a wrong frame |
| 2 | Two-session pattern improves quality | Two-session pattern loses critical nuance | Complex iterative tasks; planning sessions that surface tacit knowledge not captured in writing; short tasks within context budget | MAJOR | Slack promotes the pattern without any caveat; real cost (plan completeness burden; nuance loss) absent from both marketing deliverables |
| 3 | Training-data defaults are bad (models fill gaps with them) | Training-data defaults are often correct | Commodity tasks; well-established domains where best practice IS the default; early exploration before user knows what constraints to impose | MINOR | Frames default behavior as uniformly harmful; fails when the project is unexceptional |
| 4 | Self-critique in the prompt is useful (first pass) | Self-critique produces false confidence | High-stakes output where self-preference bias causes model to preserve errors while appearing to correct them | MAJOR | Slack omits the Panickssery caveat entirely; marketing deliverables are inconsistent on a well-evidenced limitation |
| 5 | This works on every model | This approach fails on specific model/task configurations | Level 3 requires tool access (stated in blog, absent from both marketing deliverables); weak instruction-following models; non-English contexts | MAJOR | "Works on Claude, GPT, Gemini, Llama" in Slack is stated without the blog's tool-access qualifier |
| 6 | More structure = more quality | More structure = more brittleness when structure is wrong | User imposes wrong quality criteria; over-specifies incorrect constraints; structure locks in a wrong frame; model produces polished wrong answer faster | MAJOR | Neither deliverable addresses the meta-risk that structured prompting only improves quality if the structure itself is correct |
| 7 | Fresh context removes noise | Fresh context removes signal, not just noise | Planning sessions that surface implicit knowledge not written into the plan; iterative tasks where understanding deepens through exchange | MINOR | Plan completeness burden ("if the plan can't stand alone, it wasn't detailed enough") shifts full cognitive cost to user; not acknowledged in Slack |
| 8 | Level 2 is enough for most day-to-day work | Level 2 is insufficient for work with downstream consequences | Professional deliverables; output consumed by others without review; compounding pipelines even at Level 2 | MINOR | "Most day-to-day work" is undefined and will be read differently across target readers |
| 9 | The fluency-competence gap is addressable by prompting better | The gap is most dangerous when the user cannot detect it — prompting better does not help then | Non-expert users; novel domains; cases where plausibility is hard to distinguish from accuracy | MAJOR | Both deliverables implicitly promise the gap is fixable; highest-risk users receive no differentiated guidance |
| 10 | Requiring citations/sources improves grounding | Requiring citations makes hallucination harder to detect | Models without retrieval access; domain-specific or paywalled literature; recent research beyond training cutoff | MAJOR | Blog flags hallucination in "When This Breaks"; neither marketing deliverable mentions it alongside the citation recommendation |

---

## Detailed Inversions

### Inversion 1: "Structured prompting produces better output"

**Original claim (Medium article, blog):** Every dimension you leave open, the model fills with its default. Constrain the work — tell it what to do, how to show reasoning, how you'll evaluate the result. Structure in, structure out.

**Inverted claim:** Imposing structure on a prompt produces worse output.

**When is the inversion true?**
- Creative writing, brainstorming, open-ended exploration — the blog acknowledges this in "When This Breaks" and the Medium article includes it. The Slack message omits it.
- When the user imposes the wrong constraints. If the Level 2 prompt specifies "compare against the top 5 frameworks" and the right answer is "none of these frameworks apply," the structure locks in a wrong frame. The model produces a polished, well-structured analysis of the wrong question — confident and internally consistent.
- When user expertise is low and constraint selection is poor. Structure amplifies the frame, including bad frames. A poorly specified Level 3 prompt can produce worse output than an open Level 1 prompt because it forces the model down a constrained wrong path with human checkpoints that confirm rather than correct it.
- Tasks requiring natural language fluency, tone, or empathy — creative copy, customer communications, empathetic responses — where structural constraints degrade naturalism.

**Severity:** MAJOR

**Blind spot revealed:** The marketing deliverables present structure as a monotonic improvement. The inversion reveals this only holds when the constraints themselves are correct. Neither deliverable arms the reader against the case where they write a structurally complete but semantically wrong prompt — which produces confident, polished, wrong output faster than Level 1 would have.

---

### Inversion 2: "The two-session pattern improves quality"

**Original claim (blog, Medium article):** Plan in one conversation, execute in a fresh one. Context windows are finite, planning noise degrades execution, separation improves focus.

**Inverted claim:** The two-session pattern reduces quality by discarding accumulated understanding.

**When is the inversion true?**
- When the planning conversation surfaces implicit constraints, user corrections, or edge cases that are NOT written into the plan. These are lost in the session split. The back-and-forth is where tacit knowledge becomes explicit — and that process is not fully externalizable into a written artifact.
- The blog says "the plan artifact has to carry the full context on its own." This is a high bar. Most users will not write plans that fully capture planning session knowledge. The execution session fills gaps with defaults — the same problem structured prompting was designed to solve.
- Short tasks where total context fits within budget. For a task under 10K tokens, the two-session overhead (writing a complete plan, managing two conversations, re-orienting the model) is pure cost with no benefit.
- Iterative debugging or exploratory analysis where the plan changes as you learn. Two-session pattern breaks here — re-planning is the work, not a preamble to it.

**Severity:** MAJOR

**Blind spot revealed:** The Slack message promotes the two-session pattern as "the move most people miss" with no caveat whatsoever. The Medium article mentions nuance loss as parenthetical ("You do lose the back-and-forth nuance. That's real.") but does not communicate the magnitude of the plan-completeness burden the reader is taking on. Neither marketing deliverable gives readers a signal for when NOT to use the two-session pattern.

---

### Inversion 3: "Models filling gaps with training-data defaults is bad"

**Original claim (blog, Medium, Slack):** When instructions leave room for interpretation, the prediction mechanism fills gaps with training data defaults — not what's true about your project.

**Inverted claim:** Training-data defaults are the correct answer for many tasks.

**When is the inversion true?**
- Commodity tasks where industry best practice IS the training default. "Write a unit test for this function" — the default pattern is probably correct.
- Tasks where the user's project is unexceptional and the generic answer is accurate.
- Cases where user-specific context is not actually informative to the task.
- Early exploration phases where the user doesn't yet know what constraints to impose — defaults show the territory before the user can map it.

**Severity:** MINOR

**Blind spot revealed:** The deliverables frame training-data default behavior as uniformly harmful. The inversion reveals this is only harmful when the project is genuinely exceptional in ways the user can specify. The marketing content could more precisely frame the failure condition: defaults are harmful when the task is context-dependent AND the user has relevant context they haven't provided.

---

### Inversion 4: "Self-critique in the prompt is useful"

**Original claim (blog, Medium article):** Self-critique is useful as a first pass. Not a substitute for human review.

**Inverted claim:** Self-critique in the prompt actively degrades output quality.

**When is the inversion true?**
- When the model's self-preference bias (Panickssery et al.) causes it to rate a flawed output as passing, masking the problem from the human reviewer. The model now presents the output as "reviewed and approved," which can reduce human scrutiny on precisely the outputs that need it most.
- When the self-critique dimensions are wrong. "Score yourself on completeness, consistency, and evidence quality" doesn't catch conceptual errors, wrong frames, or misapplied frameworks. The self-critique passes on specified dimensions while real errors go undetected.
- When three self-critique passes are mistaken for independent quality review. The Panickssery finding — models recognize and favor their own output — means three self-critique passes may be three iterations of the same bias, not three independent checks.
- When self-critique token overhead displaces context that could have been used for better execution.

**Severity:** MAJOR

**Blind spot revealed:** The Medium article includes the self-critique caveat with the Panickssery citation. The Slack message — "Self-critique against dimensions you define" — does NOT include the caveat. A reader of the Slack message who implements self-critique will have false confidence in outputs that have been self-reviewed using a biased process. The marketing deliverables are internally inconsistent on a point the source paper treats as a significant, well-evidenced limitation.

---

### Inversion 5: "This works on every model"

**Original claim (Slack message, Medium article, blog):** Works on Claude, GPT, Gemini, Llama — every model I've tested. Structure in, structure out.

**Inverted claim:** This approach fails on specific model and task configurations.

**When is the inversion true?**
- Level 3 explicitly requires tool access. The blog states: "That Level 3 prompt assumes a model with tool access: file system, web search, the works." Neither the Slack message nor the Medium article includes this qualification. A reader who applies the Level 3 pattern in a plain chat window will not get the stated results.
- Weak instruction-following models. Structured prompts require the model to correctly parse and execute complex multi-part instructions. Models with weaker instruction following may produce worse output from complex structured prompts than from simpler Level 1 prompts.
- Non-English contexts. The evidence base (Wei et al., Liu et al., Panickssery et al.) is predominantly English-language. The universality claim is not supported for multilingual use cases.
- Long structured prompts where critical instructions end up in the middle of a large context. "Lost in the Middle" (Liu et al.) — the paper cited to support the two-session pattern — directly implies that complex Level 3 prompts with instructions distributed across a long context may suffer from reduced attention to middle-position content.
- Fine-tuned specialized models (code models, domain-specific models) where base prompting behavior differs from frontier general models.

**Severity:** MAJOR

**Blind spot revealed:** "Works on every model" is a universality claim without qualification. The blog qualifies it implicitly ("every model I've tested," tool-access caveat). The marketing deliverables strip both qualifiers simultaneously. The Slack message's "Works on Claude, GPT, Gemini, Llama — every model I've tested" will be read as an objective guarantee. Readers who hit a case where it doesn't work have no framework from the marketing content to diagnose why.

---

### Inversion 6: "More structure = more quality"

**Original claim (implicit throughout all deliverables):** The more constrained and structured the prompt, the better the output quality, progressing through Levels 1 to 3.

**Inverted claim:** More structure increases brittleness and failure risk when the structure encodes a wrong frame.

**When is the inversion true?**
- When the user's quality criteria are wrong. Structured prompting forces the model to optimize against those criteria. If "completeness, consistency, evidence quality" are the self-critique dimensions but the real problem is a wrong conceptual premise, the model produces a complete, consistent, well-evidenced answer to the wrong question — faster and more confidently than Level 1 would have.
- When constraints are over-specified. A Level 3 prompt that specifies exactly which five frameworks to evaluate may miss a better framework not on the list. Level 1 might have surfaced it.
- When the plan review step confirms a bad plan. Human checkpoints only catch what the human knows to look for. If the user lacks domain knowledge to evaluate the plan, the review provides no protection and false confidence instead.
- When structure optimizes for legibility over accuracy. A highly structured Level 3 output can look more authoritative than a correct but unstructured Level 1 output — making the wrong answer harder to challenge.

**Severity:** MAJOR

**Blind spot revealed:** Neither marketing deliverable addresses the meta-risk: structured prompting only improves quality if the structure itself is correct. The marketing positioning ("tell it what rigor looks like") assumes the user knows what rigor looks like. For users who don't, structured prompting accelerates confident wrong answers. This is the inversion of the core promise, and it affects the users who most need the advice.

---

### Inversion 7: "Fresh context removes noise"

**Original claim (blog, Medium, Slack):** Planning conversation introduces noise. Fresh execution context focuses the model on the plan.

**Inverted claim:** Fresh context removes signal, not just noise.

**When is the inversion true?**
- When the planning conversation produced clarifications, corrections, or examples that were not captured in the written plan. The blog itself says "you do lose the back-and-forth nuance. That's real." But what's lost is not just nuance — it's specific information that shaped what the plan means.
- When the plan is ambiguous and the planning conversation's back-and-forth would have resolved those ambiguities on the fly. The execution session, lacking that context, resolves ambiguities with defaults.
- When execution reveals a plan flaw that would have been correctable mid-stream in a single session, but now requires starting a third session to fix — adding overhead rather than reducing it.
- For iterative or conversational work (exploratory research, complex debugging, creative development) where understanding deepens through exchange rather than one-shot execution against a pre-written plan.

**Severity:** MINOR

**Blind spot revealed:** The two-session pattern implicitly assumes plans can be made complete enough to bear the full weight of execution context. "If the plan can't stand alone, it wasn't detailed enough" is prescriptive but not realistic — planning sessions surface tacit knowledge that is inherently difficult to fully externalize. The information loss is real, inherent, and not fully preventable by better plan writing. The Slack message has no acknowledgment of this at all.

---

### Inversion 8: "Level 2 is enough for most day-to-day work"

**Original claim (blog, Medium article):** For most day-to-day work, Level 2 is honestly enough.

**Inverted claim:** Level 2 is insufficient for most day-to-day work that carries real consequences.

**When is the inversion true?**
- When "day-to-day work" includes professional deliverables consumed by others. Level 2 output still allows significant model discretion and can contain plausible but wrong content.
- When output feeds downstream decisions. Compounding errors — "garbage in, increasingly polished garbage out" — apply at Level 2 pipelines too, not only Level 3.
- When the user doesn't apply the human review that Level 2 implicitly requires. Level 2 output is better than Level 1 but is not self-validating.

**Severity:** MINOR

**Blind spot revealed:** "Most day-to-day work" is undefined and will be read differently across target readers. A junior analyst using AI for preliminary research (Level 2 likely sufficient) and a product manager using AI output to make architectural decisions (Level 2 likely insufficient) will both read "most day-to-day work" as encompassing their use case. The marketing deliverables don't give readers the signal to locate themselves on this spectrum.

---

### Inversion 9: "The fluency-competence gap is addressable by prompting better"

**Original claim (blog, Medium, Slack):** The fluency-competence gap causes AI output to look expert when it isn't. Structured prompting addresses this.

**Inverted claim:** The fluency-competence gap is most dangerous precisely when the user cannot detect it — and prompting better does not help in that case.

**When is the inversion true?**
- When the user lacks domain expertise to evaluate the output. A non-lawyer applying Level 2 prompting to a legal question gets a more structured wrong answer — but still cannot tell it's wrong.
- When the task domain is one where plausibility is hard to distinguish from accuracy (medical, legal, financial, novel technical domains).
- When the structured prompt's quality criteria don't capture the actual failure mode. "Cite your sources" doesn't prevent conceptual errors. "Show your reasoning" doesn't prevent a reasoning chain built on a false premise.
- When organizational dynamics mean output is passed along without review. The marketing content recommends human review; in practice many users will not apply it consistently for "good-looking" structured output.

**Severity:** MAJOR

**Blind spot revealed:** Both marketing deliverables implicitly promise that following the advice closes the fluency-competence gap. This is true only for users with sufficient domain knowledge to evaluate quality-checked output. The highest-risk users — those who cannot detect the gap — are precisely the users for whom structured prompting is least protective. Neither deliverable addresses this population, signals the limitation, or redirects them to domain experts.

---

### Inversion 10: "Requiring citations/sources improves grounding"

**Original claim (blog, Medium article):** The Level 2 prompt requires the model to cite original sources, improving grounding. The evidence constraint forces the model to look outward instead of interpolating.

**Inverted claim:** Requiring citations makes hallucination harder to detect and can reduce effective output quality.

**When is the inversion true?**
- When the model does not have retrieval access and generates citations. A hallucinated citation to a nonexistent paper looks more authoritative than a claim without a citation — the structured output obscures the hallucination.
- When the user doesn't verify citations. The marketing deliverables don't instruct readers to verify citations, and most won't. Unverified citations are worse than acknowledged uncertainty: they are invisible errors that look like evidence.
- When real sources exist but are paywalled, domain-specific, or beyond the model's training cutoff. The model cites the closest available proxy, which may be wrong, outdated, or misrepresented.
- When the citation instruction selects for findable sources over relevant ones. "Research the top 10 frameworks" may produce rigorous application of the wrong frameworks because the citation constraint selects for what's well-documented, not what's best-fit.

**Severity:** MAJOR

**Blind spot revealed:** The blog's "When This Breaks" section explicitly mentions hallucination. Neither marketing deliverable mentions it in the context of the citation recommendation. The Slack message's "cite sources" instruction, and the Medium article's Level 2 example ("For each, cite the original source"), are promoted without any caveat about verification. A reader who follows this pattern and receives a beautifully structured analysis with inline citations has no signal from the marketing content that those citations need to be verified before trusting the output.

---

## Hidden Assumptions Uncovered

### Assumption A: The user has sufficient domain knowledge to evaluate constrained output
Both deliverables assume the reader can write correct quality criteria, evaluate plan quality during the review step, and detect errors in structured output. This assumption fails for many target readers. Structured prompting is most valuable to users already expert enough to know what good looks like — who are also the users least likely to need it. The advice is least protective for its highest-risk audience.

### Assumption B: Plans can be made sufficiently complete
The two-session pattern requires a plan that "can stand alone." This assumes planning sessions produce fully externalizable, complete artifacts. In practice, planning conversations surface tacit knowledge that is difficult to capture in writing. The assumption is undisclosed, and the Slack message omits even the partial acknowledgment present in the Medium article.

### Assumption C: Human checkpoints are consistently applied
Both deliverables recommend human checkpoints as the real quality control mechanism. They assume readers will apply this discipline consistently. The Slack message's promise — "work that survives scrutiny" at Level 3 — will be read by many as a property of the prompt pattern alone, not of the prompt pattern plus diligent human review of every checkpoint.

### Assumption D: "Every model I've tested" generalizes to the reader's conditions
"Works on Claude, GPT, Gemini, Llama — every model I've tested" is an accurate first-person claim in the blog. The Slack message presents it without the "I've tested" qualifier, promoting it as an objective fact. The assumption that the author's test conditions (model versions, task types, languages, tool availability, frontier-class models) generalize to the reader's conditions is not examined.

### Assumption E: The citation instruction causes retrieval, not generation
Both deliverables recommend requiring citations. The assumption is that citation instructions cause the model to retrieve real sources. For models without retrieval access, citations are generated, not retrieved — the instruction changes the output format without changing the underlying grounding. This assumption is critical to the Level 2 and Level 3 value propositions and is disclosed nowhere in the marketing content.

### Assumption F: User-specified self-critique dimensions are the right ones
Level 3 asks the model to self-critique against user-specified dimensions. The assumption is that users will specify dimensions that capture the actual failure modes for their task. Users who lack domain expertise to know what failure modes to watch for will specify incomplete or wrong dimensions — and the self-critique will pass on those dimensions while real errors remain invisible.

### Assumption G: Level 3 readers have tool-capable models
The blog states Level 3 assumes a model with tool access. Neither marketing deliverable includes this qualification. The Slack message describes Level 3 benefits for an audience that may primarily use plain chat interfaces — in which case Level 3 as described is not achievable.

---

## Overall Assessment

**Deliverables reviewed:** `work/marketing/slack-message.md` and `work/marketing/medium-article.md`

The source blog post is notably honest: "When This Breaks" is a genuine strength, the self-critique limitation is cited and explained, the tool-access requirement for Level 3 is flagged, and the two-session nuance loss is directly acknowledged. The blog earns its claims.

The marketing deliverables, in compressing the source, have made selective omissions that each individually constitute a MAJOR blind spot:

| Finding | Medium Article | Slack Message | Priority |
|---|---|---|---|
| Self-critique caveat (Panickssery) absent | Included correctly | ABSENT | High — fix Slack |
| Level 3 tool-access requirement absent | ABSENT | ABSENT | High — fix both |
| Citation hallucination risk absent | ABSENT | ABSENT | High — fix both |
| Two-session nuance loss understated | Parenthetical acknowledgment | ABSENT | Medium — expand Slack |
| Fluency gap dangerous for non-experts | Not addressed | Not addressed | Medium — add to both |
| Structure amplifies wrong frames | Not addressed | Not addressed | Medium — add qualifier |
| "Every model" universality unqualified | Uses "every model I've tested" | Drops qualifier | Low — minor wording fix |

**Verdict by deliverable:**
- **Medium article:** REVISE. The "When This Breaks" section is a genuine strength. MAJOR gaps: tool-access qualifier for Level 3; citation hallucination caveat; fluency-gap non-expert caveat. These are additive — does not require restructuring.
- **Slack message:** REVISE with higher priority. Multiple MAJOR caveats present in the source are entirely absent. Minimum required additions: self-critique caveat (one sentence), tool-access qualifier (one clause), citation verification note (one sentence). The Slack message's compression has crossed from appropriate brevity into material omissions.

The blog is the asset. The marketing deliverables should accurately represent what the blog claims and what it warns against.

---

*S-013 Inversion Technique completed by adv-executor | 2026-02-24*
