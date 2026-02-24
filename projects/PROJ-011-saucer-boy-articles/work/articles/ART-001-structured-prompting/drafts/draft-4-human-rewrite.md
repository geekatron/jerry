OK so here's what's going on with your prompt. And I want to be clear up front — this isn't a Jerry thing. This is how every LLM works. Claude, GPT, Gemini, the open source stuff, whatever comes out next month. The pattern is the same.

Your instinct was solid. You wanted an LLM to evaluate a repo against industry frameworks. That's a perfectly reasonable thing to ask for. The problem isn't what you asked for — it's how little you told it about what a good answer looks like.

Let me use a skiing analogy because it maps perfectly. Shane McConkey — if you don't know him, he was this legendary big-mountain freeskier who literally competed in a banana suit and won. Guy looked completely unhinged on the mountain. But he wasn't. Every crazy thing he did was backed by obsessive preparation. The wild part was the performance. The preparation was the foundation. That's the whole lesson here.

So your prompt was basically "evaluate the repo and apply top industry frameworks." And look, the LLM will absolutely give you something back. That's actually the problem. These models are trained on billions of documents and they're essentially next-token predictors — they generate the most statistically probable continuation of whatever you give them. When you give them something vague, they don't produce random noise. They produce the most GENERIC probable response from their training data, but dressed up in clean formatting and authoritative language so it looks like a real answer. The headings will be perfect. The structure will look professional. But the substance is just... whatever pattern showed up most often in the training data. Not what's true about YOUR repo.

There's actually a name for this. Researchers call it the fluency-competence gap. The model learned to sound like an expert, not to BE one. When you don't define what rigor means, you get plausible instead of rigorous. And the scary part is you can't always tell the difference just by reading it.

Now here's the thing — most people think the fix is to go from that one-line prompt straight to some massive orchestration specification with quality gates and adversarial review and all this heavy machinery. It's not. There's a middle ground that gets you 80% of the way there.

Instead of "evaluate the repo and apply top frameworks," try something like "Research the top 10 industry frameworks for X. Cite the original source for each one. Analyze this repo against the top 5. Show me your selection criteria — I want to see WHY you picked those 5 before you start applying them. Put your findings in a comparison table." That's it. Same topic, two extra sentences. But now the model knows: find real sources, show your reasoning, let me check your work before you go further. You've gone from "generate whatever" to "generate something that meets specific constraints." And that matters at the architecture level — specific instructions literally narrow the space of outputs the model considers acceptable. Vague instructions let it fill in every blank with defaults.

For most day-to-day work, that's honestly enough. You don't need a flight plan for the bunny hill.

But when the work matters — when you're doing something with multiple phases, when downstream work depends on upstream quality, when getting it wrong costs real time — you go further. Your prompt becomes something like:

"Do two things in parallel: gap analysis on this repo, and research the top 10 industry frameworks from real sources, not training data. Narrow to 5 based on [specific constraints]. Cross-pollinate the findings. I need citations and references. Critique your own work before showing me — score yourself on completeness, consistency, and evidence quality. Do at least three revision passes. Insert checkpoints where I review before you continue. And show me the execution plan before you do anything."

Same ask. Frameworks applied to a repo. But now the model knows that the gap analysis and framework research are separate work streams. It knows you want grounded evidence, not training-data regurgitation. It knows you want it to self-critique against specific dimensions you defined, not just its own vague sense of "good enough." And critically — you've got human checkpoints in there, because these models genuinely cannot reliably evaluate their own work. Self-assessment is just another generation task for them, and they consistently rate their own output higher than external reviewers do. Your checkpoints break that self-congratulatory loop.

And here's the part people underestimate: once bad output enters a multi-phase pipeline, it doesn't just persist. It COMPOUNDS. Each downstream phase takes the previous output at face value and adds another layer of polished-sounding analysis on top. By phase three, the whole thing looks authoritative. But the errors are structural. It's not garbage in garbage out — it's garbage in, increasingly polished garbage out, and you genuinely cannot tell the difference until something downstream breaks. That's why the human checkpoints matter. That's why reviewing the plan matters.

Which brings me to the part that most people completely miss.

You don't fire off that big prompt and let the model run. You review the plan it gives you. You iterate on it. Because when instructions leave room for interpretation, the model defaults to the most probable completion — which almost always means the most generic, least rigorous version that technically satisfies what you asked. If you don't push back on the plan, everything downstream inherits that mediocrity.

So you review, you push back, you get the plan tight. And then you do something counterintuitive. You start a brand new conversation. You copy the finalized plan into a fresh chat and give it one instruction: "You are the executor. Here is the plan. Follow it step by step."

Why? Two reasons. First, the context window is finite. Every token from your planning conversation is taking up space that should be used for execution. And there's solid research showing that model performance on retrieval and reasoning tasks degrades as context gets longer — stuff buried in the middle of a long conversation gets way less attention than what's at the beginning or end. Second, planning and execution are different modes. A clean context lets the model focus on one job instead of carrying all the noise from the planning debate.

You do lose the back-and-forth nuance. That's real. The plan artifact has to carry the full context on its own — phases, what "done" looks like for each phase, output format. If the plan can't stand alone, it wasn't detailed enough. Which is exactly why the review step matters.

And I want to be clear: this works on EVERY model. Context windows are an engineering constraint — they're determined by architecture and compute tradeoffs, and they've grown a lot (4K tokens to over a million in three years), but within any given model they're a hard limit. Every model performs better with specific instructions vs vague ones. Every model performs better when you tell it what quality looks like instead of letting it decide. That's one of the most consistently replicated findings in prompt engineering. Chain-of-thought prompting, structured role-task-format patterns — constrained inputs beat vague inputs across every model family tested. The syntax varies (XML tags for Claude, markdown for GPT, whatever), but the principle is universal.

So boil it down to three things:

First — constrain the work. Don't tell the model what topic to explore. Tell it what to DO, how to show its reasoning, and how you'll evaluate the result. Every dimension you leave open, the model fills with the statistical default.

Second — review the plan before the product. Get the execution plan first. Does it have real phases? Does it define what "done" means? Does it include quality checks? If the plan is basically "step 1: do it, step 2: we're done" then push back. The plan is where you catch bad thinking before it multiplies.

Third — separate planning from execution. Plan in one conversation, execute in a fresh one with just the finalized artifact. Don't drag 40 messages of planning debate into the execution context. Clean slate, focused execution.

Before your next prompt, just run through this in your head: Did I say what I actually need done? Did I say how I'll know if the answer is good? Did I require sources? Did I ask for the plan first? Am I working in a clean context or am I carrying baggage from the last conversation? You don't need to go full orchestration mode right away. Just adding "show me your plan before you execute, and cite your sources" to any prompt will change what you get back. Start there. Work up to the full version when the stakes justify it.

McConkey looked like he was winging it. He wasn't. The wild was the performance. The preparation was everything underneath it.

Next time you open an LLM, before you type anything, write down three things: what you need, how you'll know if it's good, and what you want to see first. Do that once and tell me it didn't change the output.
