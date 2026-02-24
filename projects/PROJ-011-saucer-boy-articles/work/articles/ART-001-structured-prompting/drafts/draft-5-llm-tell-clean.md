# Why Structured Prompting Works

Alright, this trips up everybody, so don't feel singled out. What I'm about to walk you through applies to every LLM on the market. Claude, GPT, Gemini, Llama, whatever ships next Tuesday. This isn't a Jerry thing. It's a "how these models actually work under the hood" thing.

Your instinct was right. Asking an LLM to apply industry frameworks to a repo is a reasonable ask. The gap isn't in *what* you asked for. It's in how much you told it about what good looks like.

Think of it like big-mountain skiing. Shane McConkey, legendary freeskier, the guy who'd ski a cliff in a banana suit and win competitions doing it. He had a rule. He looked like he was winging it. He wasn't. The wild was the performance. The preparation was the foundation.

Same applies here. Three levels of prompting, three levels of output quality.

## Level 1: Point Downhill and Hope

> *"Evaluate the repo and apply the top industry frameworks for X."*

The LLM reads that and goes: "Cool, I'll pick some frameworks from my training data, skim the repo, and generate something that *looks* like an answer."

And it will look like an answer. That's the dangerous part. These models are next-token predictors trained on billions of documents. When you give them a vague instruction, they don't give you random garbage. They give you something worse: the most probable generic response from their training distribution, dressed up as a custom answer. The structure will be clean. The headings will be professional. The language will be authoritative. But the substance is whatever pattern was most common in the training data, not what's actually true about *your* repo.

This disconnect between how competent it sounds and how competent it is has a name. It's called the "fluency-competence gap," a pattern documented across model families since GPT-3. The output sounds expert because the model learned to *sound* expert, not because it verified anything. When you don't specify what rigor looks like, you get plausible, not rigorous. That's not a coin flip. It's systematic, and it's predictable.

## Level 2: Scope the Ask

Most people can get 80% of the benefit with a prompt that's just two or three sentences more specific:

> *"Research the top 10 industry frameworks for X. For each, cite the original source. Then analyze this repo against the top 5. Show your selection criteria. I want to see why you picked those 5 before you apply them. Present findings in a comparison table."*

Same topic. But now the LLM knows: find real sources, show your work, let me check before you commit. You've narrowed the output distribution from "whatever pattern is most probable" to "something that meets these specific constraints." That's how these models work at the architecture level. Structured instructions focus the model's attention on relevant context and narrow the space of acceptable completions. Vague instructions leave the model to fill in every unspecified dimension with defaults.

For a lot of work, this is enough. You don't need a flight plan for the bunny hill.

## Level 3: Full Orchestration

When the work matters. Compound phases, quality consequences, things you're building on top of. That's when you go further:

> *"Do two things in parallel: gap analysis on this repo, and research the top 10 industry frameworks using real sources, not training data. Narrow to 5 based on [specific constraints]. Cross-pollinate the findings. I need citations and references. Critique your own work before showing me. Score yourself on completeness, consistency, and evidence quality. Three revision passes minimum. Insert checkpoints where I review before you continue. Show me the execution plan before you do anything."*

That's the same ask as Level 1. Frameworks applied to a repo. But now the LLM knows:

- Two parallel work streams, not one chute. Gap analysis and framework research are distinct lines.
- Real sources, not training-data gravity. The evidence constraint forces grounding.
- Self-critique with specific dimensions. The model evaluates its own output against criteria you defined, not its own sense of "good enough."
- Human gates. Because models can't reliably self-assess at scale. Self-assessment is itself a completion task, and research on LLM self-evaluation consistently shows favorable bias. The model tends to rate its own output higher than external evaluators do. Your checkpoints break that loop.
- Plan before product. You evaluate the process before committing to the output.

One more thing that bites hard: once weak output enters a multi-phase pipeline, it compounds. Each downstream phase treats the previous output as ground truth and adds its own layer of confident-sounding polish. By phase three, the output looks authoritative. The errors are load-bearing. That's not garbage in, garbage out. It's garbage in, polished garbage out, and you can't tell the difference until something breaks. That's why the human gates matter. That's why the plan review matters.

## The Two-Session Pattern

You don't just fire the prompt and let it run. You review the execution plan the LLM gives you. You iterate on it. Because when instructions are underspecified, the model defaults to the most probable completion. Usually the most generic, least rigorous plan that satisfies the surface-level request. If you don't check the plan, everything downstream inherits that weakness.

So you review. You push back. You get the plan right. Then you start a new conversation. Copy the finalized plan into a fresh chat. Prompt with one clean instruction: *"You are the executor. Here is the plan. Follow it step by step. Do not deviate."*

Why a new conversation? Two reasons.

First, token budget is zero-sum. Every token of planning conversation is occupying space in the context window that should be used for execution. Research has shown that model performance on retrieval and reasoning tasks degrades as context length grows. Liu et al. (2023) documented the "lost in the middle" effect, where instructions buried in a long conversation history get progressively less attention than content at the beginning or end.

Second, role clarity. Planning mode and execution mode are different cognitive demands. A clean context lets the model commit to one role without the noise of the planning debate.

You lose the conversational nuance. That's the cost. The plan artifact has to be good enough to carry the context forward on its own. It should specify phases, acceptance criteria for each phase, and output format. Everything the executor needs without the debate that produced it. If the artifact can't stand alone, your plan wasn't detailed enough. Which is exactly why the review step matters.

## Why This Works on Every Model

Context windows are hard engineering constraints, determined by architecture, memory, and compute tradeoffs. They're not permanent. They've grown from 4K to 1M+ tokens in three years. But within any given model, they're real limits you work within. And every model, regardless of architecture, performs better when:

- Instructions are specific rather than vague. This is a well-documented finding across prompt engineering research, from chain-of-thought prompting to structured role-task-format patterns. Constrained inputs consistently improve output across model families.
- Quality criteria are explicit rather than left to the model's defaults.
- Output is constrained to specific evidence and format requirements.

The principles are universal. The implementation syntax varies. XML tags for Claude, markdown for GPT, whatever the model prefers. The structure is the point, not the format.

## The Three Principles

**1. Constrain the work.** Don't tell the model what topic to cover. Tell it what to do, how to show its work, and how you'll judge the result. Every dimension you leave unspecified, the model fills with the most generic probable completion. That's not laziness. It's probability distributions.

**2. Review the plan, not just the product.** Ask for the execution plan first. Check it. Does it have distinct phases? Does it specify what "done" looks like? Does it include quality checks? If the plan is "Step 1: do the thing, Step 2: done," push back. The plan is where you catch weak thinking before it propagates.

**3. Separate planning from execution.** Plan in one conversation. Execute in a fresh one with just the artifact. Don't carry 40 messages of debate into the build. Start a new chat, paste the plan, execute clean.

## Start Here

Before your next prompt, check these five things:

```
[ ] Did I specify WHAT to do (not just the topic)?
[ ] Did I tell it HOW I'll judge quality?
[ ] Did I require evidence or sources?
[ ] Did I ask for the plan BEFORE the product?
[ ] Am I in a clean context (or carrying planning baggage)?
```

You don't have to go full orchestration on day one. Even adding "show me your plan before executing, and cite your sources" to any prompt will change the output. Start with Level 2. Graduate to Level 3 when the work has consequences.

McConkey looked like he was winging it. He wasn't. The wild was the performance. The preparation was the foundation.

Next time you open an LLM, before you type a single word, write down what you need, how you'll know if the answer is good, and what you want to see first. Three sentences before the prompt. Do that once and tell me it didn't change the output.

I dare you.
