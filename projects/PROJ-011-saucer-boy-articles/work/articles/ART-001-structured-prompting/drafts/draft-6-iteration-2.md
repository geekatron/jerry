# Why Structured Prompting Works

Alright, this trips up everybody, so don't feel singled out. What I'm about to walk you through applies to every LLM on the market. Claude, GPT, Gemini, Llama, whatever ships next Tuesday. This isn't a Jerry thing. It's a "how these models actually work under the hood" thing.

Your instinct was right. Asking an LLM to apply industry frameworks to a repo is a reasonable ask. The gap isn't in *what* you asked for. It's in how much you told it about what good looks like.

Think of it like big-mountain skiing. Shane McConkey, if you don't know him, was a legendary freeskier who literally competed in a banana suit and won. The guy looked completely unhinged on the mountain. He wasn't. Every wild thing he did was backed by obsessive preparation. The performance was the surface. The preparation was the foundation.

Same applies here. Three levels of prompting, three levels of output quality.

## Level 1: Point Downhill and Hope

> *"Evaluate the repo and apply the top industry frameworks for X."*

The LLM reads that and goes: "Cool, I'll pick some frameworks from my training data, skim the repo, and generate something that *looks* like an answer."

And it will look like an answer. That's the dangerous part. These models are next-token predictors trained on billions of documents. When you give them a vague instruction, they don't give you random garbage. They give you something worse: the most probable generic response from their training distribution, dressed up as a custom answer. Clean structure, professional headings, authoritative language. But the substance is whatever pattern showed up most often in the training data, not what's actually true about *your* repo.

There's a real disconnect between how competent the output sounds and how competent it actually is. I call it the fluency-competence gap. The underlying phenomenon is well-documented: Bender and Koller (2020) showed that models trained on linguistic form alone don't acquire genuine understanding, and Sharma et al. (2024) found that RLHF-trained models systematically produce authoritative-sounding responses regardless of factual accuracy. The output sounds expert because the model learned to *sound* expert, not because it verified anything. When you don't define what rigor means, you get plausible instead of rigorous. Every time. Across every model family.

## Level 2: Scope the Ask

Most people can get 80% of the benefit with a prompt that's just two or three sentences more specific:

> *"Research the top 10 industry frameworks for X. For each, cite the original source. Then analyze this repo against the top 5. Show your selection criteria. I want to see why you picked those 5 before you apply them. Present findings in a comparison table."*

Same topic. But now the LLM knows: find real sources, show your work, let me check before you commit. You've gone from "generate whatever" to "generate something that meets specific constraints." That matters at the architecture level. Specific instructions narrow the space of outputs the model considers acceptable. Vague instructions let it fill in every blank with defaults. Wei et al. (2022) demonstrated this with chain-of-thought prompting: just adding intermediate reasoning steps to a prompt measurably improved performance on arithmetic, commonsense, and symbolic reasoning tasks. Structure in, structure out.

For most day-to-day work, that's honestly enough. You don't need a flight plan for the bunny hill.

## Level 3: Full Orchestration

When the work matters. Compound phases, quality consequences, things you're building on top of. That's when you go further:

> *"Do two things in parallel: gap analysis on this repo, and research the top 10 industry frameworks using real sources, not training data. Narrow to 5 based on [specific constraints]. Cross-pollinate the findings. I need citations and references. Critique your own work before showing me. Score yourself on completeness, consistency, and evidence quality. Three revision passes minimum. Insert checkpoints where I review before you continue. Show me the execution plan before you do anything."*

Same ask as Level 1. Frameworks applied to a repo. But now the model knows:

- Gap analysis and framework research are separate work streams. Not one pass at everything. Two distinct lines.
- You want grounded evidence, not training-data regurgitation. The evidence constraint forces the model to look outward instead of interpolating from what it already "knows."
- Self-critique against dimensions you defined. Not the model's own vague sense of "good enough," but completeness, consistency, and evidence quality as you specified them.
- Human checkpoints break the self-congratulatory loop. Here's the tension: I just told the model to critique its own work, but models genuinely struggle with self-assessment. Panickssery et al. (2024) showed that LLMs recognize and favor their own output, consistently rating it higher than external evaluators do. Self-critique in the prompt is still useful as a first pass, a way to catch obvious gaps. But it's not a substitute for your eyes on the output. The checkpoints are where real quality control happens.
- Plan before product. You evaluate the process before committing to the output.

One more thing that bites hard: once bad output enters a multi-phase pipeline, it doesn't just persist. It compounds. Each downstream phase takes the previous output at face value and adds another layer of polished-sounding analysis on top. By phase three, the whole thing looks authoritative. The errors are structural. It's not garbage in, garbage out. It's garbage in, increasingly polished garbage out, and you genuinely cannot tell the difference until something downstream breaks. That's why the human checkpoints matter. That's why reviewing the plan matters.

## The Two-Session Pattern

Here's the move most people miss entirely.

You don't fire off that big prompt and let the model run. You review the plan it gives you. You iterate on it. Push back. Because when instructions leave room for interpretation, the model defaults to the most probable completion, which almost always means the most generic, least rigorous version that technically satisfies what you asked. If you don't push back on the plan, everything downstream inherits that mediocrity.

So you review, you get the plan tight. Then you do something counterintuitive: start a brand new conversation. Copy the finalized plan into a fresh chat and give it one clean instruction: *"You are the executor. Here is the plan. Follow it step by step. Flag deviations rather than freelancing."*

Why a new conversation? Two reasons.

First, the context window is finite. Every token from your planning conversation is taking up space that should be used for execution. Liu et al. (2023) showed that information buried in the middle of a long context gets significantly less attention than content at the beginning or end. They called it the "lost in the middle" effect. It's a positional attention bias, not a simple capacity problem. Your carefully crafted instructions from message three are competing with forty messages of planning debate, and the model's attention isn't distributed evenly.

Second, planning and execution are different modes. A clean context lets the model focus on one job instead of carrying all the noise from the planning debate.

You do lose the back-and-forth nuance. That's real. The plan artifact has to carry the full context on its own. Phases, what "done" looks like for each phase, output format. If the plan can't stand alone, it wasn't detailed enough. Which is exactly why the review step matters.

## Why This Works on Every Model

Context windows are engineering constraints. Architecture, memory, compute tradeoffs. They've grown significantly over the past few years (GPT-3 shipped with 2K tokens in 2020; Gemini 1.5 crossed a million in 2024), but within any given model, they're hard limits you work within. And every model, regardless of architecture, performs better when you give it structure to work with. Specific instructions over vague ones. Explicit quality criteria over "use your best judgment." Evidence requirements over unconstrained generation. That finding replicates across model families, across task types, across research groups.

The principles are universal. The syntax varies. XML tags for Claude, markdown for GPT, whatever the model prefers. The structure is the point, not the format.

## The Three Principles

Constrain the work. Don't tell the model what topic to explore. Tell it what to do, how to show its reasoning, and how you'll evaluate the result. Every dimension you leave open, the model fills with the statistical default. Not out of laziness. Out of probability distributions.

Review the plan before the product. Get the execution plan first. Does it have real phases? Does it define what "done" means for each one? Does it include quality checks? If the plan is basically "step 1: do it, step 2: we're done," push back. The plan is where you catch bad thinking before it multiplies.

Separate planning from execution. Plan in one conversation, execute in a fresh one with just the finalized artifact. Don't drag 40 messages of planning debate into the execution context. Clean slate, focused execution.

## Start Here

Before your next prompt, run through this:

```
[ ] Did I specify WHAT to do (not just the topic)?
[ ] Did I tell it HOW I'll judge quality?
[ ] Did I require evidence or sources?
[ ] Did I ask for the plan BEFORE the product?
[ ] Am I in a clean context (or carrying planning baggage)?
```

You don't need to go full orchestration right away. Just adding "show me your plan before you execute, and cite your sources" to any prompt will change what you get back. Start with Level 2. Work up to Level 3 when the stakes justify it.

McConkey looked like he was winging it. He wasn't. The wild was the performance. The preparation was everything underneath it.

Next time you open an LLM, before you type anything, write down three things: what you need, how you'll know if it's good, and what you want to see first. Do that once and tell me it didn't change the output.

I dare you.
