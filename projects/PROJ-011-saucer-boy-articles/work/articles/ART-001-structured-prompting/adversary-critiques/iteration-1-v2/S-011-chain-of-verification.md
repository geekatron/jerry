# S-011 Chain-of-Verification Report

> **Strategy:** S-011 Chain-of-Verification
> **Deliverable:** `drafts/draft-5-llm-tell-clean.md` (ART-001-structured-prompting)
> **Evaluator:** adv-executor (S-011)
> **Date:** 2026-02-23

## Document Sections

| Section | Purpose |
|---------|---------|
| [Claim Inventory](#claim-inventory) | Every factual claim extracted from the article |
| [Verification Results](#verification-results) | Per-claim verification with evidence |
| [Priority Flags](#priority-flags) | Claims requiring author attention |
| [Dimension Scores](#dimension-scores) | Quality gate scoring |
| [LLM-Tell Detection](#llm-tell-detection) | Assessment of residual LLM patterns |
| [Voice Authenticity](#voice-authenticity) | McConkey persona fidelity |
| [Recommendations](#recommendations) | Prioritized revision guidance |

---

## Claim Inventory

17 factual claims extracted. Each is assigned a verification status:

| Status | Meaning |
|--------|---------|
| VERIFIED | Claim is accurate and well-supported by external evidence |
| PARTIALLY VERIFIED | Claim is directionally correct but imprecise or overstated |
| UNVERIFIED | Claim lacks identifiable source; may be accurate but cannot be confirmed |
| INACCURATE | Claim contains a factual error |
| FABRICATED TERM | Term presented as established terminology does not exist in published literature |

---

## Verification Results

### Claim 1: Shane McConkey as "legendary freeskier"

> **Text:** "Shane McConkey, legendary freeskier, the guy who'd ski a cliff in a banana suit and win competitions doing it."

| Dimension | Assessment |
|-----------|------------|
| **Status** | PARTIALLY VERIFIED |
| **Evidence** | Shane McConkey (1969-2009) was a professional freeskier and BASE jumper. He won freeskiing and extreme-skiing competitions. He co-founded the International Free Skiers Association in 1996. He was known for cliff skiing and comedic stunts (e.g., skiing naked down a moguls course at a Vail competition). Source: Wikipedia, Outside Online, Sports Illustrated. |
| **Issue** | The "banana suit" detail is not verified. McConkey was famous for costumes and absurd antics (the Pain McShlonkey Classic features outrageous costumes in his honor), and he famously skied naked, but no source confirms he wore a banana suit specifically. He did not "win competitions" while wearing costumes -- his competition wins (e.g., World Extreme Skiing Championships) were conventional competitive performances. The costume antics were separate stunts and exhibition events. |
| **Risk** | Low. The metaphorical intent is clear. But a knowledgeable skiing reader will recognize the banana suit as likely invented detail. The claim conflates his serious competition victories with his comedic exhibition stunts. |
| **Recommendation** | Either verify the banana suit claim with a specific source, or soften to something like "the guy who'd ski a cliff naked and still win competitions" -- which is closer to documented truth (he did ski naked at competitions and he did win competitions, though not simultaneously in the way implied). Alternatively, drop the costume reference entirely and keep the cliff-skiing focus. |

---

### Claim 2: LLMs as "next-token predictors trained on billions of documents"

> **Text:** "These models are next-token predictors trained on billions of documents."

| Dimension | Assessment |
|-----------|------------|
| **Status** | VERIFIED |
| **Evidence** | Next-token prediction is the foundational training objective for autoregressive LLMs (transformer architecture). Models are trained on datasets containing trillions of tokens from billions of web pages (e.g., Common Crawl contains ~250 billion web pages). Sources: AWS, IBM, Wikipedia (Large language model). |
| **Issue** | None. "Billions of documents" is a reasonable characterization. Technically, models are trained on tokens from documents, not documents as atomic units, but the phrasing is appropriate for a general audience. |
| **Risk** | None. |

---

### Claim 3: Vague instructions produce "most probable generic response from their training distribution"

> **Text:** "They give you something worse: the most probable generic response from their training distribution, dressed up as a custom answer."

| Dimension | Assessment |
|-----------|------------|
| **Status** | VERIFIED (with nuance) |
| **Evidence** | This is a correct description of how autoregressive models respond to underspecified prompts. Without constraints, the model generates the highest-probability continuation from its learned distribution. Chain-of-thought research (Wei et al., 2022) and structured prompting research consistently demonstrate that constrained prompts yield qualitatively different outputs than vague ones. Source: Wei et al. 2022 (Chain-of-Thought Prompting Elicits Reasoning in Large Language Models). |
| **Issue** | Slightly oversimplified. Modern models use sampling strategies (temperature, top-k, top-p) that do not strictly produce the single most probable token at each step. The generation is stochastic, not deterministic. The article's claim is directionally correct for a general audience but could mislead a technically precise reader. |
| **Risk** | Low. Acceptable simplification for target audience. |

---

### Claim 4: The "fluency-competence gap" as an established term

> **Text:** "This disconnect between how competent it sounds and how competent it is has a name. It's called the 'fluency-competence gap,' a pattern documented across model families since GPT-3."

| Dimension | Assessment |
|-----------|------------|
| **Status** | FABRICATED TERM |
| **Evidence** | Extensive search across academic databases, arXiv, and general research sources returns no established term "fluency-competence gap" in the LLM literature. Related concepts exist under different names: (a) "Comprehension Without Competence" (Zhang et al., 2025, submitted to TMLR) describes architectural limits where LLMs show fluency without execution competence. (b) "Self-Preference Bias" describes models favoring their own fluent output. (c) The general observation that LLM fluency does not imply factual accuracy is widely documented but lacks a single canonical term. The phrase "fluency-competence gap" does not appear in any peer-reviewed publication found. |
| **Issue** | The article presents this as an established, named phenomenon ("has a name"). It is not. The article further claims it has been "documented across model families since GPT-3," implying a research lineage that does not exist for this specific term. The underlying observation (fluency exceeds competence) is well-established, but the term itself appears to be an invention attributed to the research community. |
| **Risk** | HIGH. This is the most significant factual integrity issue in the article. A knowledgeable reader searching for "fluency-competence gap" will find nothing. This undermines credibility because the article explicitly claims the term exists in the literature. Presenting a coined phrase as established terminology without attribution to the coiner is a form of false authority. |
| **Recommendation** | Three options: (1) Acknowledge the term is being coined here: "We could call this the fluency-competence gap" or "I call this the fluency-competence gap." (2) Replace with an established concept: "Comprehension without competence" (Zhang et al.) or simply describe the phenomenon without naming it. (3) Cite a source if one exists that was not found in this verification. |

---

### Claim 5: "the model learned to sound expert, not because it verified anything"

> **Text:** "The output sounds expert because the model learned to *sound* expert, not because it verified anything."

| Dimension | Assessment |
|-----------|------------|
| **Status** | VERIFIED |
| **Evidence** | Autoregressive models are trained on next-token prediction, not factual verification. They do not have a truth-checking mechanism. The observation that fluency does not imply accuracy is well-documented across LLM research. "Comprehension Without Competence" (Zhang et al.) formalize this as "sophisticated explanatory capabilities coupled with unreliable execution." |
| **Issue** | None. This is an accurate and well-stated characterization. |

---

### Claim 6: "80% of the benefit with a prompt that's just two or three sentences more specific"

> **Text:** "Most people can get 80% of the benefit with a prompt that's just two or three sentences more specific."

| Dimension | Assessment |
|-----------|------------|
| **Status** | UNVERIFIED |
| **Evidence** | No specific research quantifies "80% of the benefit" from adding 2-3 sentences of specificity. The claim invokes the Pareto principle pattern. While prompt engineering research consistently shows that specificity improves output quality, the "80%" figure is not sourced. |
| **Issue** | The "80%" reads as a heuristic, not a measured statistic. In context, it functions as rhetorical shorthand. A technically precise reader might expect a citation. |
| **Risk** | Low. The phrasing "most people can get" positions it as practical advice rather than empirical claim. The rhetorical intent is clear. |
| **Recommendation** | Could soften to "most of the benefit" to avoid the specific number, or leave as-is with the understanding that "80%" is colloquial Pareto shorthand, consistent with the article's voice. |

---

### Claim 7: "Structured instructions focus the model's attention on relevant context and narrow the space of acceptable completions"

> **Text:** "Structured instructions focus the model's attention on relevant context and narrow the space of acceptable completions."

| Dimension | Assessment |
|-----------|------------|
| **Status** | VERIFIED |
| **Evidence** | Chain-of-thought prompting (Wei et al., 2022) demonstrates that structured instructions change the distribution of model outputs. The attention mechanism focuses on relevant context based on input structure. Structured prompts constrain the output distribution, which is mechanistically equivalent to "narrowing the space of acceptable completions." |
| **Issue** | None. This is technically accurate and appropriately simplified. |

---

### Claim 8: LLM self-evaluation shows "favorable bias"

> **Text:** "Self-assessment is itself a completion task, and research on LLM self-evaluation consistently shows favorable bias. The model tends to rate its own output higher than external evaluators do."

| Dimension | Assessment |
|-----------|------------|
| **Status** | VERIFIED |
| **Evidence** | Multiple peer-reviewed papers confirm this: (a) "LLM Evaluators Recognize and Favor Their Own Generations" (Panickssery et al., NeurIPS 2024) shows LLMs assign higher scores to their own output. (b) "Self-Preference Bias in LLM-as-a-Judge" (2024) documents that LLMs rate their own outputs higher than texts by other LLMs or humans while human annotators judge them as equal quality. (c) Research shows ~40% of comparisons across all models exhibit bias indicators. |
| **Issue** | None. This is well-supported and accurately stated. The framing as "research consistently shows" is justified by multiple independent papers. |

---

### Claim 9: Weak output compounds through multi-phase pipelines

> **Text:** "Once weak output enters a multi-phase pipeline, it compounds. Each downstream phase treats the previous output as ground truth and adds its own layer of confident-sounding polish."

| Dimension | Assessment |
|-----------|------------|
| **Status** | VERIFIED (practical observation) |
| **Evidence** | This describes error propagation in sequential LLM pipelines, a well-recognized phenomenon. The Jerry Framework's own FMEA analysis documents this as R-T02 (error amplification, RPN 336). Google DeepMind's research on multi-agent topologies found ~1.3x error amplification with structured handoffs vs. 17x for uncoordinated topologies (referenced in agent-development-standards.md). |
| **Issue** | The article does not cite specific research. The claim is accurate but relies on the reader accepting it as self-evident rather than evidence-backed. |
| **Risk** | Low. The logic is sound and the audience-appropriate framing ("you can't tell the difference until something breaks") makes it concrete. |

---

### Claim 10: Liu et al. (2023) documented the "lost in the middle" effect

> **Text:** "Liu et al. (2023) documented the 'lost in the middle' effect, where instructions buried in a long conversation history get progressively less attention than content at the beginning or end."

| Dimension | Assessment |
|-----------|------------|
| **Status** | PARTIALLY VERIFIED |
| **Evidence** | The paper exists: "Lost in the Middle: How Language Models Use Long Contexts" by Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, and Percy Liang. Posted to arXiv July 2023 (2307.03172), published in TACL 2024. The core finding is verified: "Performance is often highest when relevant information occurs at the beginning or end of the input context, and significantly degrades when models must access relevant information in the middle of long contexts." |
| **Issue 1** | The article says the effect applies to "instructions buried in a long conversation history." This is an imprecise characterization. The paper tested retrieval and reasoning tasks with information placed at different positions in the input context -- not specifically "instructions" in "conversation history." The effect is about positional attention degradation for information retrieval, not about instruction following in multi-turn chat. |
| **Issue 2** | The article says "instructions... get progressively less attention." The paper showed a U-shaped attention curve (high at beginning and end, low in middle), not a monotonic "progressive" decrease. Information at the middle gets less attention, but information at the end gets high attention -- it is not purely "progressive." |
| **Issue 3** | Publication year: The arXiv preprint is 2023, the formal publication is TACL 2024. Citing as "Liu et al. (2023)" is acceptable for the preprint but could be "Liu et al. (2024)" for the published version. |
| **Risk** | MEDIUM. The citation exists and the general point is valid, but the application to "instructions in conversation history" overgeneralizes the finding. A knowledgeable reader who knows the paper will notice the imprecision. |
| **Recommendation** | Revise to: "Liu et al. (2023) documented the 'lost in the middle' effect: when relevant information is buried deep in a long context, models disproportionately attend to content near the beginning and end, losing track of material in the middle." This accurately reflects the U-shaped attention curve without overgeneralizing to "instructions" or "conversation history." |

---

### Claim 11: Context windows "grown from 4K to 1M+ tokens in three years"

> **Text:** "They've grown from 4K to 1M+ tokens in three years."

| Dimension | Assessment |
|-----------|------------|
| **Status** | PARTIALLY VERIFIED |
| **Evidence** | The growth trajectory is directionally correct but the specifics need calibration. GPT-3 (2020) had a 2,048-token context window. GPT-3.5 (2022) had 4,096 tokens. GPT-4 (2023) had 8,192 initially, later 128K. Gemini 1.5 Pro (2024) introduced 1M tokens. So the "4K to 1M+" trajectory spans roughly 2022-2024 (2 years from GPT-3.5 to Gemini 1.5 Pro) or 2020-2024 (4 years from GPT-3 to Gemini 1.5 Pro). |
| **Issue 1** | "4K" as a starting point: GPT-3 had 2K tokens (2020), GPT-3.5 had 4K (2022). Using "4K" as the baseline implies 2022 as the start. |
| **Issue 2** | "Three years": From GPT-3.5 (4K, March 2022) to Gemini 1.5 Pro (1M, February 2024) is approximately 2 years, not 3. From GPT-3 (2K, June 2020) to Gemini 1.5 Pro (1M, February 2024) is approximately 3.5 years, but the starting point is 2K, not 4K. The "three years" claim does not cleanly map to either interpretation. |
| **Issue 3** | By the article's publication date (2026), Gemini 2.0 has 2M tokens and Llama 4 Scout has 10M tokens, making "1M+" an understatement. |
| **Risk** | LOW-MEDIUM. The trajectory and magnitude are correct in spirit. The specific "three years" and "4K" starting point are slightly off. Most readers will not verify the exact timeline. |
| **Recommendation** | Revise to: "They've grown from a few thousand tokens to over a million in just a few years" -- removes the specific numbers that do not cleanly align while preserving the impact of the claim. Or, if specificity is preferred: "from 2K to 2M+ tokens in about four years." |

---

### Claim 12: "Research has shown that model performance on retrieval and reasoning tasks degrades as context length grows"

> **Text:** "Research has shown that model performance on retrieval and reasoning tasks degrades as context length grows."

| Dimension | Assessment |
|-----------|------------|
| **Status** | VERIFIED |
| **Evidence** | Liu et al. (2023) is the primary citation here, and the article cites it immediately after. Additional research supports this: Chroma Research ("Context Rot") documents performance degradation with increasing context. The finding is well-established across the field. |
| **Issue** | None. Accurately stated. |

---

### Claim 13: Fresh context improves execution over carrying planning conversation

> **Text:** "A clean context lets the model commit to one role without the noise of the planning debate."

| Dimension | Assessment |
|-----------|------------|
| **Status** | VERIFIED (practical consensus) |
| **Evidence** | This aligns with Anthropic's own best practices for Claude Code (fresh context for writer/reviewer separation). The Jerry Framework's FC-M-001 standard formalizes this pattern. The underlying mechanism is sound: reducing irrelevant context reduces noise in the attention mechanism. |
| **Issue** | Not cited to specific research. Positioned as practical advice, which is appropriate. |

---

### Claim 14: "chain-of-thought prompting to structured role-task-format patterns" as well-documented research

> **Text:** "This is a well-documented finding across prompt engineering research, from chain-of-thought prompting to structured role-task-format patterns."

| Dimension | Assessment |
|-----------|------------|
| **Status** | VERIFIED |
| **Evidence** | Chain-of-thought prompting (Wei et al., 2022) is peer-reviewed and widely cited. "Structured role-task-format patterns" describes a family of prompt engineering techniques documented across practitioner literature and research. The claim that "constrained inputs consistently improve output across model families" is supported by multiple studies. |
| **Issue** | "Role-task-format patterns" is practitioner terminology rather than a specific research program. This is fine for the target audience but is not a citable research term. |
| **Risk** | None. |

---

### Claim 15: "XML tags for Claude, markdown for GPT"

> **Text:** "XML tags for Claude, markdown for GPT, whatever the model prefers."

| Dimension | Assessment |
|-----------|------------|
| **Status** | VERIFIED |
| **Evidence** | Anthropic's documentation recommends XML tags for structuring Claude prompts. OpenAI's documentation and community practice favor markdown formatting. This is well-known practitioner knowledge. |
| **Issue** | None. |

---

### Claim 16: "Every dimension you leave unspecified, the model fills with the most generic probable completion"

> **Text:** "Every dimension you leave unspecified, the model fills with the most generic probable completion. That's not laziness. It's probability distributions."

| Dimension | Assessment |
|-----------|------------|
| **Status** | VERIFIED |
| **Evidence** | This is a correct description of autoregressive generation. Underspecified prompts leave the model to sample from the broadest probability distribution, which tends toward the mode (most common pattern in training data). |
| **Issue** | "Most generic" is slightly imprecise -- the model produces the most *probable* completion, which may or may not be the most *generic*. In practice, for vague prompts, the most probable completion is typically generic, so the claim holds for the described scenario. |
| **Risk** | None. |

---

### Claim 17: The two-session pattern ("plan then execute in fresh context")

> **Text:** Full description of the two-session pattern across the "Two-Session Pattern" section.

| Dimension | Assessment |
|-----------|------------|
| **Status** | VERIFIED (practical methodology) |
| **Evidence** | This pattern is well-established in prompt engineering practice. Anthropic's Claude Code documentation recommends separating planning from execution. The Jerry Framework's own FC-M-001 and the two-session pattern in project-workflow.md formalize this approach. |
| **Issue** | None. This is sound practical advice presented as methodology. |

---

## Priority Flags

Claims requiring author attention, ranked by severity:

| Priority | Claim | Issue | Severity |
|----------|-------|-------|----------|
| 1 | Claim 4: "fluency-competence gap" | Term presented as established; appears to be fabricated or at minimum uncitable. Article explicitly says "has a name" -- it does not. | **HIGH** |
| 2 | Claim 10: Liu et al. characterization | Overgeneralizes finding to "instructions in conversation history"; mischaracterizes U-shaped curve as "progressive" degradation. | **MEDIUM** |
| 3 | Claim 11: "4K to 1M+ in three years" | Numbers do not cleanly align to any single timeline interpretation. | **LOW-MEDIUM** |
| 4 | Claim 1: McConkey banana suit | Specific detail likely fabricated; costume stunts and competition wins were separate activities. | **LOW** |

---

## Dimension Scores

| Dimension | Weight | Score | Justification |
|-----------|--------|-------|---------------|
| Completeness | 0.20 | 0.88 | Covers three prompt levels, two-session pattern, universal principles. No critical structural gaps. Minor gap: no explicit citations beyond Liu et al. |
| Internal Consistency | 0.20 | 0.94 | Arguments build logically from Level 1 through Level 3. The skiing metaphor is consistent throughout. No contradictions detected between sections. |
| Methodological Rigor | 0.20 | 0.78 | One fabricated term (Claim 4) presented as established research. One imprecise citation characterization (Claim 10). One inaccurate timeline (Claim 11). These undermine the article's evidence-based framing. |
| Evidence Quality | 0.15 | 0.72 | Only one explicit citation (Liu et al.). Several claims invoke "research shows" without citations. The fabricated "fluency-competence gap" term is the most significant evidence quality issue. Self-evaluation bias claim is accurate but uncited. |
| Actionability | 0.15 | 0.95 | The five-item checklist is concrete. Three levels are clearly actionable. Two-session pattern is immediately implementable. Excellent practical guidance. |
| Traceability | 0.10 | 0.60 | Single explicit citation. Multiple claims reference "research" generically. No bibliography or further reading. For an article making technical claims, traceability is below standard. |

**Weighted Composite Score: 0.838**

Calculation: (0.88 * 0.20) + (0.94 * 0.20) + (0.78 * 0.20) + (0.72 * 0.15) + (0.95 * 0.15) + (0.60 * 0.10) = 0.176 + 0.188 + 0.156 + 0.108 + 0.1425 + 0.060 = **0.831**

**Band: REJECTED (< 0.85)**

The primary drivers of the below-threshold score are:
1. Fabricated terminology presented as established (Claim 4) -- directly impacts Methodological Rigor and Evidence Quality
2. Sparse citations for an article making multiple research claims -- impacts Traceability and Evidence Quality
3. Imprecise characterization of the one citation present (Liu et al.) -- impacts Methodological Rigor

---

## LLM-Tell Detection

**Score: 0.92 (strong -- very few LLM-tells detected)**

| Pattern | Assessment |
|---------|------------|
| Hedging language ("it's important to note") | Not detected. The voice is direct and assertive. |
| Generic filler ("in today's fast-paced world") | Not detected. |
| Excessive enumeration ("firstly, secondly, thirdly") | Not detected. Lists are natural and purposeful. |
| Sycophantic opening ("Great question!") | Not detected. |
| Formulaic conclusion | Not detected. The "I dare you" ending is distinctive and human. |
| Over-qualification ("it's worth noting that") | Not detected. |
| Passive voice overuse | Not detected. Voice is consistently active. |

**One residual pattern detected:**

Line 27: "That's how these models work at the architecture level. Structured instructions focus the model's attention on relevant context and narrow the space of acceptable completions. Vague instructions leave the model to fill in every unspecified dimension with defaults." -- The transition from conversational to technical register here is slightly abrupt. The sentence "That's how these models work at the architecture level" reads as an LLM trying to establish authority ("at the architecture level") rather than McConkey's natural voice. However, this is a marginal flag and may be intentional register-shifting for the explanatory passage.

---

## Voice Authenticity

**Score: 0.91 (strong McConkey voice)**

| Dimension | Assessment |
|-----------|------------|
| Conversational directness | Strong. "Alright, this trips up everybody, so don't feel singled out." |
| Metaphor quality | Strong. The skiing metaphor is sustained and earned (McConkey was a real person, the metaphor is load-bearing, not decorative). |
| Teaching through narrative | Strong. Levels 1-3 are taught through escalating examples, not bullet points. |
| Avoidance of jargon for jargon's sake | Strong. Technical terms are introduced only when needed and immediately explained. |
| Distinctive closing | Strong. "I dare you" is memorable and in-character. |
| Register consistency | Mostly strong. Minor wobble in the "at the architecture level" passage (see LLM-Tell detection). |

---

## Recommendations

### Must-Fix (blocking quality gate)

1. **Claim 4 -- "fluency-competence gap":** Do not present a coined term as established research terminology. Options:
   - Frame as coined: "I call this the fluency-competence gap" or "You could call this..."
   - Replace with an established concept without inventing a name
   - Remove the claim "has a name" entirely and simply describe the phenomenon

2. **Claim 10 -- Liu et al. characterization:** Revise the description to accurately reflect the paper's finding:
   - The paper is about positional attention in long contexts, not specifically about "instructions" in "conversation history"
   - The effect is U-shaped (beginning and end get high attention, middle gets low), not "progressive" degradation
   - Suggested revision: "Liu et al. (2023) documented the 'lost in the middle' effect -- when relevant information sits deep in a long context, models disproportionately attend to content near the beginning and end, losing track of material in the middle."

### Should-Fix (improves score)

3. **Claim 11 -- Timeline:** Revise "4K to 1M+ tokens in three years" to either remove specific numbers or align them to verifiable milestones. Suggested: "from a few thousand tokens to over a million in just a few years."

4. **Evidence Quality -- add 2-3 citations:** The article makes several "research shows" claims. Adding brief citations for (a) chain-of-thought prompting (Wei et al., 2022), (b) self-evaluation bias (Panickssery et al., 2024), and (c) the Liu et al. paper (already present) would meaningfully improve Evidence Quality and Traceability scores.

### Consider-Fix (polish)

5. **Claim 1 -- McConkey banana suit:** Verify or replace with documented McConkey detail (e.g., skiing naked, skiing off 700-foot cliffs).

6. **Line 27 register shift:** The phrase "at the architecture level" could be softened to maintain voice consistency. Example: "That's how the plumbing works" or simply remove the qualifier.

---

*Verification conducted using web search against: arXiv, NeurIPS proceedings, Wikipedia, AWS/IBM/Google technical documentation, Outside Online, Sports Illustrated, TACL, and ResearchGate.*
