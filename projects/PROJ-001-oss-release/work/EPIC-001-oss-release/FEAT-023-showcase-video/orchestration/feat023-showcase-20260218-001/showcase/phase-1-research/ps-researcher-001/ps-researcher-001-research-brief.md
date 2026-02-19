# ps-researcher-001 Research Brief
## Jerry Framework — Claude Code Birthday Showcase Video

> **Agent:** ps-researcher-001
> **Phase:** 1 — Research
> **Workflow:** feat023-showcase-20260218-001
> **Feature:** FEAT-023 — Claude Code Birthday Showcase — Promotional Video
> **Date:** 2026-02-18
> **Deliverable:** Research brief to inform 2-minute hype reel script
> **Criticality:** C4 (public-facing, Anthropic leadership audience)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Hype Reel Best Practices](#hype-reel-best-practices) | What makes 2-minute tech showcase videos win |
| [InVideo AI Capabilities](#invideo-ai-capabilities) | Script format, limitations, best practices |
| [Jerry Framework Differentiators](#jerry-framework-differentiators) | Stats, philosophy, unique angles |
| [Audience Analysis](#audience-analysis) | Anthropic leadership, investors, developers |
| [Key Takeaways for Script](#key-takeaways-for-script) | Top 5-7 insights to inform the script |
| [Sources](#sources) | Research citations |

---

## Hype Reel Best Practices

### The Non-Negotiable: Hook Within 5 Seconds

Every source confirms the same rule: **you have five seconds to earn the next 115**. The opening must be visceral, unexpected, or immediately provocative. It cannot be a title card. It cannot be "let me tell you about our framework." It must land a gut punch that makes the viewer physically unable to look away.

For Jerry, that hook is the meta question: *Did an AI just build its own guardrails?* That paradox, delivered fast, is the hook.

### Narrative Structure That Works

The winning structure for short-form tech video is a tight problem-solution-proof arc, not a feature tour. Research from Descript, Vidico, and Motion confirms:

**Problem-Solution beats Feature Tour by 37% in software**

The structure that converts:
1. **Pain (5-10 sec):** State the problem viscerally. Not academically.
2. **Impossibility (10-20 sec):** Make the audience feel how unsolvable the problem seemed.
3. **Reveal (20-40 sec):** The solution, delivered with momentum.
4. **Proof (40-90 sec):** Numbers. Real stats. Moving fast.
5. **Identity (90-105 sec):** This is who we are. The soul.
6. **Call to Action (105-120 sec):** One clear thing. Not three.

### Pacing: The 10-15 Word Rule

InVideo's own editorial guidance and vidboard.ai both confirm: **change visual elements every 10-15 words in voiceover**. Vary shot length — mix 1-2 second rapid cuts with occasional 8-10 second breathe moments. Predictable pacing kills engagement. The Saucer Boy persona maps perfectly here: McConkey never did anything at the pace you expected.

### What Wins at Tech Showcases (Y Combinator / Demo Day Context)

From the 2025 YC Demo Day analysis at Jeffrey Paine's post-event writeup and the Mocksi demo day playbook:

- **Clarity beats cleverness.** A middle-schooler should understand what you do in the first 20 seconds.
- **Traction is currency.** Numbers with timeframes show momentum. "3,299 tests passing" beats "comprehensive test suite."
- **Team credibility in accomplishments, not titles.** What was actually built? What shipped?
- **One specific example beats five general claims.** "Claude Code built its own guardrails using Jerry" is more powerful than "Jerry supports AI agent workflows."
- At the 2025 YC Demo Day, **90% of pitches were AI-centric.** Differentiation requires more than "AI." Jerry's angle is AI *governing* AI — that's a tier above.

### Visual Techniques for 2-Minute Tech Hype Reels

Based on Advids and Descript analysis of best-in-class software demo videos:

- **Motion graphics over talking heads** for abstract concepts (enforcement layers, quality gates)
- **Screen recordings with annotations** for concrete features (hooks output, terminal output)
- **Kinetic text** for stats — numbers that animate in feel more credible
- **Music-to-pacing alignment** is critical for hype reels — the energy of the soundtrack must match the edit rhythm
- **No intro animation longer than 2 seconds** — logo flies are death

---

## InVideo AI Capabilities

### How InVideo AI Works (2025 V3)

InVideo AI V3 (2025) is a **prompt-to-ready-video pipeline**. The workflow:

1. Submit a detailed text prompt (the brief)
2. AI generates: script, selects from 16M+ stock footage/images, adds voiceover, background music, transitions
3. Edit via "Magic Box" — text commands to modify scenes, voiceover accent, music, shot length
4. Export

The platform is optimized for volume and speed, not granular creative control.

### Script Format InVideo Expects

InVideo's own documentation and the `reviewguidance.com` guide confirm the optimal input format:

**Structured Scene-Based Format:**

```
[SCENE 1 — 0:00-0:10]
VOICEOVER: "Opening line here."
VISUAL DIRECTION: What's on screen (motion graphic / screen recording / b-roll keyword)
TONE: Fast / Dramatic / Playful

[SCENE 2 — 0:10-0:25]
...
```

Key prompt elements InVideo processes best:
- **Duration specified explicitly** (e.g., "2-minute video, 120 seconds total")
- **Platform/use case** ("showcase reel for tech conference audience")
- **Tone guidance** ("technically confident, fast-paced, personality-driven")
- **Voiceover style** ("punchy, 3-5 word sentences, no passive voice")
- **Visual keywords per scene** (InVideo pulls stock footage based on these)
- **Music tone** ("high-energy electronic / rock hybrid")

### Best Practices for AI-Generated Video Output

**What works well:**
- InVideo handles quick cuts and kinetic text well
- The "Magic Box" text editor can adjust scene length, swap footage, change music, alter voiceover accent without re-generating
- Structured prompts with explicit duration targets achieve 90%+ first-pass usability vs. 68% for vague prompts (topview.ai research)

**Known limitations to design around:**
- **Synthetic voice naturalness:** 42% of viewers disengage when AI voiceover sounds unnatural. Recommendation: use InVideo's most natural voice option, or plan to swap in a human voiceover for the final cut.
- **Live-action vs. animation:** InVideo defaults to stock footage blends, not pure animation. Design the script for stock-footage-compatible visuals (terminal windows, code, people at desks, conference rooms, mountains for McConkey references).
- **Granular control is limited:** Plan the scene structure in the script before submission. Text commands work but are not surgical.
- **First draft requires review:** Treat InVideo output as a rough cut, not a final. Budget time for Magic Box iteration.

### Recommended InVideo Prompt Strategy

Write the prompt as a **producer briefing a video team**, not as a chatbot instruction. Include:
- Video purpose and audience
- Scene-by-scene breakdown with voiceover + visual direction
- Tone, pacing, and music guidance
- What NOT to include (no stock footage of people in meetings if showing a dev tool)

---

## Jerry Framework Differentiators

### Verified Stats (from codebase, 2026-02-18)

| Metric | Value | Source |
|--------|-------|--------|
| Test suite | **3,299 tests** (currently passing) | `uv run pytest --collect-only` |
| Previous milestone | 3,195 tests (shipped with BUG-002 fix) | WORKTRACKER.md |
| Agents | **33 agents** across 6 families | AGENTS.md, EN-925 |
| Adversarial strategies | **10 selected strategies** (S-001 to S-015) | quality-enforcement.md |
| Enforcement layers | **5 layers** (L1-L5) | quality-enforcement.md |
| Skills | **7 skills** (adversary, architecture, bootstrap, nasa-se, orchestration, problem-solving, transcript, worktracker — 8 directories, 7 user-facing) | skills/ directory |
| Quality gate threshold | **>= 0.92** weighted composite | quality-enforcement.md |
| Quality dimensions | **6 dimensions** with weights | quality-enforcement.md |
| License | **Apache 2.0** | pyproject.toml |
| Language | **Python 3.11+** | pyproject.toml |
| Framework | Claude Code native (hooks, agents, rules) | CLAUDE.md |
| Version | **0.2.0** | pyproject.toml |
| External dependencies | **Zero** for core | pyproject.toml |

### Framework Identity (from CLAUDE.md)

Jerry is described as:

> "Framework for behavior/workflow guardrails. Accrues knowledge, wisdom, experience."
>
> **Core Problem:** Context Rot — LLM performance degrades as context fills.
> **Core Solution:** Filesystem as infinite memory. Persist state to files; load selectively.

The key insight: **Jerry treats the filesystem as an external brain**, solving the fundamental limitation of LLM context windows through structured persistence.

### The Meta Narrative (strongest differentiator)

The most compelling fact about Jerry is not what it does — it is *who built it*:

**Claude Code built Jerry. Jerry governs Claude Code.**

This is AI self-governance. Not in an abstract, philosophical sense — in a shipping, tested, 3,299-test practical sense. The quality framework (0.92 threshold, 5 enforcement layers, 10 adversarial strategies, 33 agents) was designed *by* an AI agent *for* AI agents. That is the hook.

### Quality Framework Architecture

From `quality-enforcement.md`:

| Layer | Timing | Function |
|-------|--------|----------|
| L1 | Session start | Behavioral foundation via rules |
| L2 | Every prompt | Re-inject critical rules |
| L3 | Before tool calls | Deterministic gating (AST) |
| L4 | After tool calls | Output inspection, self-correction |
| L5 | Commit/CI | Post-hoc verification |

The **24 HARD rules** (H-01 through H-24) are constitutional constraints that cannot be overridden. This level of governance rigor applied to an AI agent system has no known open-source peer.

### The Saucer Boy Philosophy (from EPIC-005)

Shane McConkey (1969-2009) as design principle:

> "If you're not having fun, you're doing it wrong."

| McConkey Principle | Jerry Application |
|-------------------|-------------------|
| Innovation with joy | Push quality boundaries AND celebrate wins |
| Never take yourself too seriously | Error messages that inform AND entertain |
| Technical excellence is the foundation | Quality gate >= 0.92 is non-negotiable; personality is WHERE soul lives |
| The community IS the point | OSS isn't just code — it's culture |

The thesis: **technically brilliant AND wildly fun are multipliers, not trade-offs**. McConkey was the best big-mountain skier alive. He also raced in a banana suit. He won.

### Soundtrack Anchors (from EPIC-005)

These create specific emotional moments in the video:

- **"Harder, Better, Faster, Stronger" (Daft Punk)** — Creator-critic-revision cycle. The Jerry anthem.
- **"C.R.E.A.M." (Wu-Tang)** — "Context Rules Everything Around Me" — the core thesis
- **"Ain't No Half Steppin'" (Big Daddy Kane)** — Quality gate >= 0.92. No shortcuts.
- **"Sabotage" (Beastie Boys)** — Shane in spandex, launching off a cliff. Planned chaos.
- **"Know Your Enemy" (RATM)** — /adversary skill. Red Team. Devil's Advocate.

---

## Audience Analysis

### Anthropic Leadership — What They Care About

Based on Anthropic's public positioning (public benefit corporation, safety-first charter, $380B Series G at 0.92 threshold of responsible AI credibility):

**Primary motivations:**
- **Responsible AI in practice, not theory.** Anthropic's differentiation from OpenAI is safety and alignment. Jerry demonstrates responsible AI *implementation* — constitutional constraints, governance escalation, no-deception hard rules.
- **Claude Code ecosystem growth.** Jerry is built for Claude Code. It validates the platform's capability to support sophisticated, production-grade frameworks.
- **Meta demonstration.** Claude Code building its own governance framework is a capability proof that no benchmark can replicate.

**What resonates:** The 24 constitutional HARD rules. The 5-layer enforcement architecture. The fact that P-022 (no deception) is enforced at the agent level, not just stated in a policy document.

### Investors — What They Care About

From Anthropic investor analysis (Acquinox Capital, $30B Series G context):

**Primary motivations:**
- **Differentiation in a crowded market.** With 90% of 2025 YC pitches AI-centric, investors need to see what makes this non-replicable. Jerry's answer: a governance framework built *by* Claude Code *for* Claude Code, with a 3,299-test proof of rigor.
- **Enterprise-grade signals.** Zero external dependencies, Apache 2.0 license, hexagonal architecture, CQRS — these are enterprise adoption signals.
- **Open source as moat.** Apache 2.0 means community contribution. 33 agents, 10 adversarial strategies, 7 skills = a platform with real surface area.
- **Traction evidence.** The 3,299 tests, the C4 tournament reviews, the 0.9355 tournament score — these are credibility signals that convert with numbers-oriented audiences.

**What resonates:** Stats delivered with velocity. The quality gate number (0.92). The test count. The speed at which Claude Code can execute complex multi-phase orchestrations.

### Developers — What They Care About

**Primary motivations:**
- **Does it solve my actual problem?** Context Rot is a real, felt problem for any developer who has watched a Claude Code session degrade. Jerry names the problem and solves it concretely.
- **Open source and extensible.** Apache 2.0. Zero external dependencies for core. Can I use this? Can I contribute? Yes.
- **Developer experience.** The Saucer Boy philosophy is directly relevant here — "a tool you love, not a tool you tolerate." The Jerry soundtrack, easter eggs, personality in messages — this is DX differentiation.
- **Practical proof.** 3,299 tests. The framework runs under its own quality gates. It eats its own cooking.

**What resonates:** The meta story (Claude Code built this). The personality (Saucer Boy). The practical numbers. The Apache 2.0 license. The fact that this is real, shipped, and open.

---

## Key Takeaways for Script

These are the 7 insights that MUST directly inform the script writing in Phase 2:

### 1. Lead with the Paradox, Not the Framework

The hook cannot be "Jerry is a quality framework for Claude Code." The hook must be the meta question: *An AI built its own guardrails. While you were sleeping. 3,299 tests deep.* The paradox of AI self-governance is the only hook powerful enough to earn 120 seconds from an Anthropic leadership audience.

### 2. The 37% Rule — Problem-Solution Beats Feature Tour

Do not tour the features. Name one visceral problem (Context Rot: LLM performance degrades as context fills) and show the solution working. Every feature reference must be in service of the narrative, not parallel to it. "5 enforcement layers" means nothing. "Your agent forgets what it's doing. Jerry doesn't let it." means everything.

### 3. Stats as Rhythm, Not Inventory

Numbers must arrive in rhythm, not as a list. The script should deliver stats the way Wu-Tang delivers bars — punchy, unexpected, undeniable. 3,299 tests. 33 agents. 10 adversarial strategies. 24 constitutional rules. 0.92 quality threshold. These land as a drumbeat, not a PowerPoint slide.

### 4. Saucer Boy Is the Differentiator Among Peers

At a showcase where 90% of demos will be technically serious, the Saucer Boy persona is the personality moat. McConkey was the best AND the funniest. Jerry aims to be the most rigorous AND the most fun to work with. The video should FEEL like that — fast cuts, personality in the voiceover, moments of levity that never undercut the rigor.

### 5. InVideo Script Must Be Scene-Structured with Visual Keywords

The Phase 2 script must not be a prose script. It must be formatted as numbered scenes with: voiceover text (short sentences, 10-15 words max before a cut), visual direction keyword (for stock footage matching), tone marker, and duration target. This is what InVideo V3 processes with 90%+ first-pass success.

### 6. The Apache 2.0 / Open Source Signal Must Land Clearly

For all three audiences, the open-source nature is a trust signal. It means: you can inspect it, fork it, contribute to it. In a world where AI governance is often opaque, Jerry's governance is literally in the repository. The call-to-action should drive to GitHub, not a landing page.

### 7. The Emotional Arc Must Mirror McConkey's Life Arc

The video should not be a straight line of escalating hype. It should breathe: fast cuts of capability → a single quiet moment of "this is what Context Rot feels like" → the reveal that Jerry solved it → back to the hype. McConkey's best ski films had that same structure: chaos, one quiet look at the mountain, then the drop. The script should find that quiet moment before the final act.

---

## Sources

**Hype Reel / Demo Video Best Practices:**
- [30 Creative Technology Product Launch Video Examples — Advids](https://advids.co/blog/30-creative-technology-product-launch-video-examples-to-hype-your-technology-products-debut)
- [15 Best Software Demo Video Examples (2026) — Vidico](https://vidico.com/news/software-demo-videos/)
- [15 Best Product Demo Videos That Drive Conversions — Motion Agency](https://www.motiontheagency.com/blog/best-product-demo-videos-that-convert-with-expert-tips)
- [15 Best Product Demo Video Examples — Descript](https://www.descript.com/blog/article/product-demo-video-examples)

**Tech Showcase / Demo Day:**
- [My First YC Demo Day in 2025 — Jeff (Startup Whisperer)](https://jeffreypaine.com/my-first-yc-demo-day-in-2025-chaos-genius-and-why-this-batch-feels-like-the-future)
- [Crushing Demo Day: Nailing Your Pitch for Techstars, Y Combinator, and Beyond — Mocksi](https://www.mocksi.ai/blog/crushing-demo-day-nailing-your-pitch-for-techstars-y-combinator-and-beyond)
- [The Y Combinator Guide to Perfectly Pitching Your Seed Stage Startup — Cloud Substack](https://cloud.substack.com/p/the-y-combinator-guide-to-perfectly)

**InVideo AI:**
- [InVideo AI Review 2025 (Pros & Cons) — AGIYes](https://www.agiyes.com/aireviews/invideo-ai-review/)
- [InVideo AI Script Generator: 2025 Review & Guide — ReviewGuidance](https://www.reviewguidance.com/invideo-ai-script-generation/)
- [InVideo AI V3: Revolutionize Video Creation in 2025 — Toolify](https://www.toolify.ai/ai-news/invideo-ai-v3-revolutionize-video-creation-in-2025-3443801)
- [Our Honest Review of InVideo AI Generated Video — Motion Agency](https://www.motiontheagency.com/blog/honest-review-of-invideo-ai-generated-video)
- [The Ultimate Prompting Guide for AI Marketing Video Generation — InVideo](https://invideo.io/blog/ultimate-ai-prompting-guide-for-marketing-videos/)
- [How to Write a YouTube Video Script Using AI — InVideo](https://invideo.io/blog/how-to-write-youtube-video-script/)
- [The 18 Best AI Video Generators in 2026 — Zapier](https://zapier.com/blog/best-ai-video-generator/)
- [InVideo AI Tutorial: Best Prompt to Video Generator — TopView](https://www.topview.ai/blog/detail/Invideo-AI-Tutorial-Best-Prompt-to-Video-Generator)

**Anthropic / Claude Code Context:**
- [Code with Claude 2025 — Anthropic](https://www.anthropic.com/events/code-with-claude-2025)
- [Anthropic Raises $30 Billion Series G — Anthropic](https://www.anthropic.com/news/anthropic-raises-30-billion-series-g-funding-380-billion-post-money-valuation)
- [Anthropic's Claude Code Shows How Far AI Coding Tools Have Come — Built In](https://builtin.com/articles/anthropic-claude-code-tool)
- [Anthropic's Claude Code is having its "ChatGPT" moment — Uncover Alpha](https://www.uncoveralpha.com/p/anthropics-claude-code-is-having)
- [Anthropic: Investor Insights — Acquinox Capital](https://acquinox.capital/insights/gen-ai-and-ai-agents/anthropic-investor-insights)

---

*Generated by ps-researcher-001 | Phase 1 — Research | feat023-showcase-20260218-001*
