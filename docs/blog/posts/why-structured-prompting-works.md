---
date: 2026-02-23
categories:
  - Prompting
authors:
  - geekatron
slug: why-structured-prompting-works
---

# Why Structured Prompting Works

Alright, this trips up everybody, so don't feel singled out. What I'm about to walk you through applies to every major LLM on the market. Claude, GPT, Gemini, Llama, whatever ships next Tuesday. This isn't a Jerry thing. It's a "how these models actually work under the hood" thing.

Your instinct was right. Asking an LLM to apply industry frameworks to a repo is a reasonable ask. The gap isn't in *what* you asked for. It's in how much you told it about what good looks like.

Think of it like big-mountain skiing. Shane McConkey, if you don't know him, was a legendary freeskier who'd show up to competitions in costume and still take the whole thing seriously enough to win. The guy looked completely unhinged on the mountain. He wasn't. Every wild thing he did was backed by obsessive preparation. The performance was the surface. The preparation was the foundation.

Same applies here. Three levels of prompting, three levels of output quality.

<!-- more -->

## Level 1: Point Downhill and Hope

> *"Evaluate the repo and apply the top industry frameworks for X."*

The LLM reads that and goes: "Cool, I'll pick some frameworks from my training data, skim the repo, and generate something that *looks* like an answer."

And it will look like an answer. That's the dangerous part. At their core, these models predict the next token based on everything before it. Post-training techniques like RLHF shape that behavior, but when your instructions leave room for interpretation, the prediction mechanism fills the gaps with whatever pattern showed up most often in the training data. Not what's actually true about *your* repo. The output comes back with clean structure, professional headings, and authoritative language. Reads like an expert wrote it.

Except the expert part is a mirage. I call it the fluency-competence gap. Bender and Koller showed back in 2020 that models learn to sound like they understand without actually understanding. Sharma et al. found in 2024 that RLHF, the technique used to make models helpful, actually makes this worse by rewarding confident-sounding responses over accurate ones. The model learned to *sound* expert, not because it verified anything. When you don't define what rigor means, you get plausible instead of rigorous. Every time, across every model family.

## Level 2: Scope the Ask

In my experience, most people get the bulk of the benefit with a prompt that's just two or three sentences more specific:

> *"Research the top 10 industry frameworks for X. For each, cite the original source. Then analyze this repo against the top 5. Show your selection criteria. I want to see why you picked those 5 before you apply them. Present findings in a comparison table."*

Same topic. But now the LLM knows: find real sources, show your work, let me check before you commit. You've gone from "generate whatever" to "generate something that meets specific constraints." That matters at the architecture level. Specific instructions narrow the space of outputs the model considers acceptable. Vague instructions let it fill in every blank with defaults. Wei et al. (2022) demonstrated this with chain-of-thought prompting: just adding intermediate reasoning steps to a prompt measurably improved performance on arithmetic, commonsense, and symbolic reasoning tasks. Structure in, structure out.

For most day-to-day work, that's honestly enough. You don't need a flight plan for the bunny hill.

## Level 3: Full Orchestration

When downstream quality depends on upstream quality. When phases build on each other. When getting it wrong in phase one means everything after it looks authoritative but is structurally broken. That's when you go further:

> *"Do two things in parallel: gap analysis on this repo, and research the top 10 industry frameworks using real sources, not training data. Narrow to 5 based on [specific constraints]. Cross-pollinate the findings. I need citations and references. Critique your own work before showing me. Score yourself on completeness, consistency, and evidence quality. Three revision passes minimum. Insert checkpoints where I review before you continue. Show me the execution plan before you do anything."*

That Level 3 prompt assumes a model with tool access: file system, web search, the works. If you're in a plain chat window, paste the relevant code and verify citations yourself. Same principles, different mechanics.

Same ask as Level 1. Frameworks applied to a repo. But now the model knows:

- Why two work streams instead of one pass? Because gap analysis and framework research pull in different directions. Separate them, and each gets the attention it needs.
- You want grounded evidence, not pattern completion from training data. The evidence constraint forces the model to look outward instead of interpolating from what it already "knows."
- Self-critique against dimensions you defined. Not the model's own vague sense of "good enough," but completeness, consistency, and evidence quality as you specified them.
- Here's the tension with that self-critique step. I just told the model to evaluate its own work, but models genuinely struggle with self-assessment. Panickssery et al. (2024) showed that LLMs recognize and favor their own output, consistently rating it higher than external evaluators do. Self-critique in the prompt is still useful as a first pass, a way to catch obvious gaps. But it's not a substitute for your eyes on the output. The human checkpoints are where real quality control happens.
- And plan before product. You evaluate the process before committing to the output.

One more thing that bites hard: once bad output enters a multi-phase pipeline, it doesn't just persist. It compounds. This is a well-established pattern in pipeline design, and it hits LLM workflows especially hard. Each downstream phase takes the previous output at face value and adds another layer of polished-sounding analysis on top. By phase three, the whole thing looks authoritative. The errors are structural. It's not garbage in, garbage out. It's garbage in, increasingly polished garbage out, and it gets much harder to tell the difference the deeper into the pipeline you go. The human checkpoints catch this. Reviewing the plan catches it earlier.

## The Two-Session Pattern

Here's the move most people miss entirely.

You don't fire off that big prompt and let the model run. You review the plan it gives you. You iterate on it. Push back. Because when instructions leave room for interpretation, the model defaults to the most probable completion, which almost always means the most generic, least rigorous version that technically satisfies what you asked. If you don't push back on the plan, everything downstream inherits that mediocrity.

So you review, you get the plan tight. Then you do something counterintuitive: start a brand new conversation. Copy the finalized plan into a fresh chat and give it one clean instruction: *"You are the executor. Here is the plan. Follow it step by step. Flag deviations rather than freelancing."*

Why a new conversation? Two reasons.

First, the context window is finite. Every token from your planning conversation is taking up space that should be used for execution. Liu et al. (2023) found that models pay the most attention to what's at the beginning and end of a long context, and significantly less to everything in the middle. They studied retrieval tasks, but the attentional pattern applies here too: your carefully crafted instructions from message three are competing with forty messages of planning debate, and the model isn't weighing them evenly.

Second, planning and execution are different jobs. A clean context lets the model focus on one thing instead of carrying all the noise from the planning debate.

You do lose the back-and-forth nuance. That's real. The plan artifact has to carry the full context on its own. Phases, what "done" looks like for each phase, output format. If the plan can't stand alone, it wasn't detailed enough. Which is exactly why the review step matters.

## Why This Works on Every Model

You know what none of this requires? A specific vendor. Context windows are engineering constraints, the kind of hard limits determined by architecture and compute. They've grown fast: GPT-3 shipped with 2K tokens in 2020, and Gemini 1.5 crossed a million in 2024. But within any given model, the ceiling is fixed, and you're working inside it. Every model performs better when you give it structure to work with. Tell it exactly what to do instead of hoping for the best. Give it quality criteria instead of "use your best judgment." Require evidence instead of letting it free-associate. That finding holds across models, tasks, and research groups.

The principles are universal. The syntax varies. XML tags for Claude, markdown for GPT, whatever the model prefers. The structure is what matters, not the format.

## The Three Principles

Constrain the work. Don't tell the model what topic to explore. Tell it what to do, how to show its reasoning, and how you'll evaluate the result. Every dimension you leave open, the model fills with its default, driven by probability distributions rather than any understanding of what you actually need.

Review the plan before the product. Get the execution plan first. Does it have real phases? Does it define what "done" means for each one? Does it include quality checks? If the plan is basically "step 1: do it, step 2: we're done," push back. The plan is where you catch bad thinking before it multiplies.

Separate planning from execution. Plan in one conversation, execute in a fresh one with just the finalized artifact. Don't drag 40 messages of planning debate into the execution context. Clean slate, focused execution.

## When This Breaks

Structured prompting is not a magic fix. Sometimes you write a beautifully constrained prompt and the model hallucinates a source that doesn't exist, or applies a framework to the wrong part of your codebase, or confidently delivers something internally consistent and completely wrong. Structure reduces the frequency of those failures. It doesn't eliminate them. If the task is exploratory, if you're brainstorming, if you're writing something where constraint kills the creative output, back off the structure. And if you've tried three revision passes and the output still isn't landing, the problem might not be your prompt. It might be the task exceeding what a single context window can hold. That's when you decompose the work, not add more instructions to an already-overloaded conversation.

## Start Here

Your Level 2 baseline. Get these three right and you'll see the difference immediately:

- [ ] Did I specify WHAT to do (not just the topic)?
- [ ] Did I tell it HOW I'll judge quality?
- [ ] Did I require evidence or sources?

When you're ready for Level 3, add these two:

- [ ] Did I ask for the plan BEFORE the product?
- [ ] Am I in a clean context (or carrying planning baggage)?

You don't need to go full orchestration right away. Just adding "show me your plan before you execute, and cite your sources" to any prompt will change what you get back. Start with Level 2. Work up to Level 3 when the stakes justify it.

McConkey looked like he was winging it. He wasn't. The wild was the performance. The preparation was everything underneath it.

Next time you open an LLM, before you type anything, write down three things: what you need, how you'll know if it's good, and what you want to see first. Do that once and tell me it didn't change the output.

---

**Further reading:** The claims in this article are grounded in published research. For full references with links, see the companion [citations document](why-structured-prompting-works-citations.md). Start with Liu et al. (2023) on the lost-in-the-middle effect, Wei et al. (2022) on chain-of-thought prompting, and Panickssery et al. (2024) on LLM self-preference bias.
