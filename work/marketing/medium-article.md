# Your AI Output Looks Expert. It Isn't. Here's the Fix.

**Subtitle:** Three levels of prompting, three levels of output quality — and the two-session pattern most people miss entirely.

---

Your LLM output comes back with clean structure, professional headings, and authoritative language. Reads like an expert wrote it.

Except the expert part is a mirage.

I call it the fluency-competence gap — a shorthand I started using after reading [Bender and Koller's 2020 argument](https://aclanthology.org/2020.acl-main.463/) that language models learn linguistic form without grounding in meaning. Their insight was theoretical — about what models *can't* learn from text alone — but it maps directly to the practical problem: models that sound authoritative without being authoritative. [Sharma et al. (2024)](https://arxiv.org/abs/2310.13548) found that RLHF — the technique used to make models helpful — can amplify sycophantic tendencies: models learn to agree with users rather than push back, even when the user is wrong. The result is output that mirrors your assumptions instead of challenging them.

When you don't define what rigor means, you get plausible instead of rigorous. In my experience, this holds across every major model family I've tested — Claude 3.5, GPT-4o, Gemini 1.5, Llama 3 70B, across roughly 200 structured prompting sessions over 18 months.

This trips up everybody. What I'm about to walk through applies to Claude, GPT, Gemini, Llama — every model I've tested, and likely whatever ships next Tuesday. It's not a vendor thing. It's a "how these models actually work" thing.

Why universally? Context windows vary by model and generation, but within any given model, you're working inside a fixed ceiling. Structured prompting works because it addresses how all these models process their available context — not because of anything vendor-specific. Give any model a well-constrained task with clear quality criteria, and it outperforms the same model given a vague request.

## Level 1: Point Downhill and Hope

> *"Evaluate this codebase and apply the top industry frameworks for X."*

The model reads that and goes: "Cool, I'll pick some frameworks from my training data, skim the code, and generate something that looks like an answer."

And it will look like an answer. That's the dangerous part. At their core, these models predict the next token based on everything before it. When your instructions leave room for interpretation, the prediction mechanism fills the gaps with whatever pattern showed up most often in the training data. Not what's actually true about *your* project.

## Level 2: Scope the Ask

Most people get the bulk of the benefit with a prompt that's just two or three sentences more specific:

> *"Research the top 10 industry frameworks for X. For each, cite the original source. Then analyze this codebase against the top 5. Show your selection criteria. I want to see why you picked those 5 before you apply them. Present findings in a comparison table."*

Same topic. But now the model knows: find real sources, show your work, let me check before you commit. You've gone from "generate whatever" to "generate something that meets specific constraints."

[Wei et al. (2022)](https://arxiv.org/abs/2201.11903) demonstrated this with chain-of-thought prompting: adding intermediate reasoning steps to a prompt measurably improved performance on arithmetic, commonsense, and symbolic reasoning tasks. Their work studied specific reasoning benchmarks, but the underlying principle — constrain the input, get more reliable output — holds in my experience across every prompting scenario I've tested.

For most day-to-day work, that's honestly enough. You don't need a flight plan for the bunny hill.

## Level 3: Full Orchestration

When downstream quality depends on upstream quality. When phases build on each other. When getting it wrong in phase one means everything after it looks authoritative but is structurally broken:

> *"Do two things in parallel: gap analysis on this codebase, and research the top 10 industry frameworks using real sources — not training data. Narrow to 5 based on [specific constraints]. Cross-pollinate the findings. I need citations. Critique your own work before showing me. Score yourself on completeness, consistency, and evidence quality. Three revision passes minimum. Insert checkpoints where I review before you continue. Show me the execution plan before you do anything."*

*(That prompt assumes a model with tool access — web search, code execution. Without tools, replace the verification steps with explicit self-checking instructions: "List your sources and confidence level for each claim.")*

Same ask as Level 1. But now the model knows what rigor looks like because you defined it.

Why does this matter at Level 3 and not Level 2? Because in my experience building multi-phase LLM workflows, once bad output enters a pipeline, it doesn't just persist — it compounds. Each downstream phase takes the previous output at face value and layers polished analysis on top. By phase three, the whole thing looks authoritative, but the errors are structural. It's not garbage in, garbage out. It's garbage in, *increasingly polished garbage out*. The human checkpoints catch this. The plan review catches it earlier.

One tension worth flagging: that self-critique step. [Panickssery et al. (NeurIPS 2024)](https://proceedings.neurips.cc/paper_files/paper/2024/file/7f1f0218e45f5414c79c0679633e47bc-Paper-Conference.pdf) showed that LLMs recognize and favor their own output, rating it higher than external reviewers do. Self-critique in the prompt is useful as a first pass. It's not a substitute for your eyes on the output. The human checkpoints are where real quality control happens.

## The Move Most People Miss

You don't fire off that big prompt and let the model run. You review the plan it gives you. Iterate on it. Push back.

Then you do something counterintuitive: start a brand new conversation. Copy the finalized plan into a fresh chat and give it one clean instruction: *"You are the executor. Here is the plan. Follow it step by step. Flag deviations rather than freelancing."*

Why a new conversation? Two reasons.

First, the context window is finite. [Liu et al. (2024)](https://arxiv.org/abs/2307.03172) found that in document retrieval tasks, models pay the most attention to what's at the beginning and end of a long context, and significantly less to everything in the middle. The conversational case hasn't been studied directly — Liu et al. tested multi-document retrieval, not chat-style prompting — but the attentional pattern likely generalizes: Your carefully crafted instructions from message three are competing with forty messages of planning debate, and the model isn't weighing them evenly.

Second, planning and execution are different cognitive modes. A clean context lets the model focus on one thing instead of carrying all the noise from the planning session.

You do lose the back-and-forth nuance. That's real. The plan artifact has to carry the full context on its own — phases, what "done" looks like for each phase, output format. If the plan can't stand alone, it wasn't detailed enough. Which is exactly why the review step matters.

## The Three Principles

**Constrain the work.** Don't tell the model what topic to explore. Tell it what to do, how to show its reasoning, and how you'll evaluate the result. Every dimension you leave open, the model fills with its default — driven by probability rather than any understanding of what you actually need.

**Review the plan before the product.** Get the execution plan first. Does it have real phases? Does it define what "done" means for each one? Does it include quality checks? If the plan is basically "step 1: do it, step 2: we're done," push back.

**Separate planning from execution.** Plan in one conversation, execute in a fresh one with just the finalized artifact. Clean slate, focused execution.

## When This Breaks

Structured prompting is not a magic fix. Sometimes you write a beautifully constrained prompt and the model hallucinates a source that doesn't exist, or applies a framework to the wrong part of your codebase, or confidently delivers something internally consistent and completely wrong. Structure reduces the frequency of those failures. It doesn't eliminate them.

If the task is exploratory — brainstorming, creative writing, open-ended exploration — back off the structure. And if you've tried three revision passes and the output still isn't landing, the problem might not be your prompt. It might be the task exceeding what a single context window can hold. That's when you decompose the work, not add more instructions to an already-overloaded conversation.

## Start Here

Your Level 2 baseline. Get these three right and you'll see the difference immediately:

1. Did I specify **what to do** (not just the topic)?
2. Did I tell it **how I'll judge quality**?
3. Did I **require evidence or sources**?

When you're ready for Level 3, add these two:

4. Did I ask for the **plan before the product**?
5. Am I in a **clean context** (or carrying planning baggage)?

You don't need to go full orchestration right away. Just adding "show me your plan before you execute, and cite your sources" to any prompt will change what you get back.

Next time you open an LLM, before you type anything, write down three things: what you need, how you'll know if it's good, and what you want to see first. Do that once and tell me it didn't change the output.

---

### References

- Bender, E. M. & Koller, A. (2020). "Climbing towards NLU: On Meaning, Form, and Understanding in the Age of Data." *ACL 2020*. [aclanthology.org/2020.acl-main.463](https://aclanthology.org/2020.acl-main.463/)
- Sharma, M. et al. (2024). "Towards Understanding Sycophancy in Language Models." *ICLR 2024*. [arxiv.org/abs/2310.13548](https://arxiv.org/abs/2310.13548)
- Wei, J. et al. (2022). "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models." *NeurIPS 2022*. [arxiv.org/abs/2201.11903](https://arxiv.org/abs/2201.11903)
- Liu, N. F. et al. (2024). "Lost in the Middle: How Language Models Use Long Contexts." *TACL, 12,* 157-173. [arxiv.org/abs/2307.03172](https://arxiv.org/abs/2307.03172)
- Panickssery, A. et al. (2024). "LLM Evaluators Recognize and Favor Their Own Generations." *NeurIPS 2024*. [proceedings.neurips.cc](https://proceedings.neurips.cc/paper_files/paper/2024/file/7f1f0218e45f5414c79c0679633e47bc-Paper-Conference.pdf)

---

*Tags: AI, Prompt Engineering, LLMs, Productivity, Software Engineering*
