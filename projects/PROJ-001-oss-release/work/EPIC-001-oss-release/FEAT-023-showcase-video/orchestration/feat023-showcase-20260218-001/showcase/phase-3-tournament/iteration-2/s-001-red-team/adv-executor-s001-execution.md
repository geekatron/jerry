# Red Team Report: Jerry Framework Hype Reel Script v2 (2:00)

**Strategy:** S-001 Red Team Analysis
**Deliverable:** `projects/PROJ-001-oss-release/work/EPIC-001-oss-release/FEAT-023-showcase-video/orchestration/feat023-showcase-20260218-001/showcase/phase-3-tournament/iteration-2/ps-architect-001-hype-reel-script-v2.md`
**Criticality:** C4 (Critical -- public-facing, irreversible, Anthropic audience)
**Date:** 2026-02-18
**Reviewer:** adv-executor (S-001) -- Iteration 2
**H-16 Compliance:** S-003 Steelman applied on 2026-02-18 by adv-executor-001 (confirmed: `phase-3-tournament/iteration-1/adv-executor-001-s003-steelman.md`). S-001 iteration 1 report confirmed: `phase-3-tournament/iteration-1/s-001-red-team/adv-executor-s001-execution.md`.
**Threat Actor:** Four distinct adversary perspectives simulated: (a) Anthropic legal/PR reviewer protecting brand and IP exposure; (b) competitor tech lead from a rival agentic framework trying to discredit the differentiator claims; (c) AI safety researcher with a research interest in accurate attribution of AI-generated work; (d) skeptical developer at the event who will pull the repo live during the presentation. Each perspective is maintained independently across the attack vector inventory.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment and recommendation |
| [Iteration 1 Disposition](#iteration-1-disposition) | Status of all 10 prior findings in v2 |
| [Threat Actor Profiles](#threat-actor-profiles) | Four adversary perspectives with goals, capabilities, motivations |
| [Findings Table](#findings-table) | All RT-NNN findings at a glance |
| [Finding Details](#finding-details) | Expanded description for Critical and Major findings |
| [Recommendations](#recommendations) | Prioritized countermeasure plan (P0/P1/P2) |
| [Scoring Impact](#scoring-impact) | Dimension-level impact assessment |
| [H-15 Self-Review](#h-15-self-review) | Pre-presentation compliance check |

---

## Summary

The v2 script demonstrates substantial remediation of the iteration 1 Critical findings -- the commercial music IP liability (RT-001-s001-20260218) is fully resolved, and the absolute attribution claim "built entirely by Claude Code" has been softened throughout. However, four exploitable vectors remain or emerge in v2. Most significantly: the enforcement framing fix for the competitor erasure problem ("Tools handle memory. Nobody had a fix for enforcement") creates a new and more specific falsifiability attack -- MemGPT's hook-based enforcement and LangMem's runtime constraint injection are directly competitive with the claim, and a tech lead from either project is almost certainly in the room at a Claude Code showcase. Second, the Scene 6 narration now contains a grammatical asymmetry ("Every line written by Claude Code, directed by a human who refused to compromise") that under adversarial reading implies two different agents -- the AI as line-writer, the human as director -- which an AI safety researcher will use to argue the human made all substantive decisions. Third, the repository call-to-action (github.com/geekatron/jerry) remains the sole unmitigated Major finding from iteration 1 and has no contingency path in the script. Fourth, a new vector emerges from the v2 fix itself: the quality gate visual (quality score climbing to 0.92-0.94 "in real-time") is scored against the Jerry Framework's own rubric; an adversary will note that the tool is grading its own work, which is an epistemically significant weakness. **Recommendation: REVISE. Two Critical findings (RT-004-v2, RT-005-v2) require mitigation before acceptance. The repository readiness (RT-006-v2) requires operational confirmation. One new Major finding (RT-007-v2) and one Minor finding (RT-008-v2) are addressable with targeted revisions.**

---

## Iteration 1 Disposition

This table documents how the 10 findings from iteration 1 Red Team (`s001-20260218`) were handled in v2. Attack vectors that are RESIDUAL or NEW are the focus of the iteration 2 report.

| ID (Iter 1) | Finding | v2 Status | Iteration 2 Assessment |
|-------------|---------|-----------|----------------------|
| RT-001-s001-20260218 | Commercial music IP liability | RESOLVED | All 5 named commercial tracks replaced with style/mood descriptions. Production music library sourcing noted. Attack vector closed. |
| RT-002-s001-20260218 | "Built entirely by Claude Code" attribution overclaim | PARTIALLY RESOLVED | "Wrote" replaces "built entirely" in narration; "directed by a human" added to Scene 6. Text overlay now reads "WROTE ITS OWN OVERSIGHT SYSTEM." However, the Scene 6 narration structure creates a new asymmetric attribution vector (see RT-002-v2). |
| RT-003-s001-20260218 | "33 agents" stat accuracy | PARTIALLY RESOLVED | Stat retained verbatim in narration and text overlay. No verification hedge added. Residual vector remains (see RT-003-v2). |
| RT-004-s001-20260218 | "NASA-grade" unsubstantiated claim | RESOLVED | Replaced with "Structured requirements analysis and design reviews." Functional description survives scrutiny. Attack vector closed. |
| RT-005-s001-20260218 | "Nobody had a fix" competitor erasure | PARTIALLY RESOLVED | Narrowed to "enforcement." "Tools handle memory. Nobody had a fix for enforcement." The narrowing creates a new, more specific falsifiability target (see RT-004-v2). |
| RT-006-s001-20260218 | Open source repository readiness | UNRESOLVED | GitHub URL and Apache 2.0 badge unchanged. No contingency path added to script. Operational dependency unmitigated (see RT-006-v2). |
| RT-007-s001-20260218 | McConkey reference niche | RESOLVED | Inline grounding added: "the skier who reinvented the sport by treating every cliff as a playground." Attack vector closed. |
| RT-008-s001-20260218 | Test count currency | RESOLVED | Replaced with "More than three thousand tests" and "3,000+" in overlay. Hedge is robust against count drift. Attack vector closed. |
| RT-009-s001-20260218 | Wu-Tang appropriation | RESOLVED (MOOT) | Music references removed entirely per RT-001 fix. |
| RT-010-s001-20260218 | Human contribution erasure | RESOLVED | "Directed by a human who refused to compromise" added to Scene 6. Attack vector closed (but see RT-002-v2 for residual framing risk). |

**New attack vectors identified in v2:** RT-001-v2 (asymmetric attribution in Scene 6), RT-002-v2 (AI safety researcher attribution angle), RT-004-v2 (enforcement claim falsifiability), RT-005-v2 (self-grading quality score visual), RT-007-v2 (InVideo capability risk), RT-008-v2 (music description inference risk).

---

## Threat Actor Profiles

### Adversary A: Anthropic Legal / PR Reviewer

| Attribute | Detail |
|-----------|--------|
| **Goal** | Ensure no IP exposure, no public claim that could embarrass Anthropic or create legal liability, no attribution framing that contradicts Anthropic's product narrative |
| **Capability** | Knowledge of copyright and IP law, familiarity with Anthropic's brand guidelines and product positioning, awareness of how "AI wrote this" claims play in regulatory and press contexts |
| **Motivation** | Protect Anthropic from regulatory scrutiny (EU AI Act attribution requirements, FTC guidance on AI-generated claims), prevent headline "Anthropic claims AI built its own oversight system without human input" |
| **Access** | Will review the script before and after the event; may flag to Anthropic comms team |
| **Primary Targets** | Attribution claims, any implication of fully autonomous AI action, music/IP exposure |

### Adversary B: Competitor Tech Lead

| Attribute | Detail |
|-----------|--------|
| **Goal** | Discredit the "first" and "unique" framing; demonstrate that Jerry's core claims are either false or already implemented by existing tools |
| **Capability** | Deep expertise in agentic frameworks (LangChain, AutoGen, CrewAI, MemGPT/Letta, LangMem, Zep, OpenAI Assistants); knows the enforcement and memory landscape in detail |
| **Motivation** | Competitive positioning; developer community credibility; live at a Claude Code birthday party where their potential customers are in the room |
| **Access** | Will attend the showcase; may tweet-thread their objections during or immediately after |
| **Primary Targets** | "Nobody had a fix for enforcement" claim; stat accuracy; open source delivery readiness |

### Adversary C: AI Safety Researcher

| Attribute | Detail |
|-----------|--------|
| **Goal** | Challenge any narrative that implies autonomous AI action without human oversight; flag attribution framing that could normalize "AI builds its own governance" as acceptable |
| **Capability** | Expertise in AI alignment, human-in-the-loop requirements, AI Act attribution standards; publication experience with AI governance critique |
| **Motivation** | Research interest in accurate AI capability representation; concern that "AI wrote its own oversight" is a misleading narrative that sets harmful precedent |
| **Access** | Academic and press channels; may write a post-event critique piece |
| **Primary Targets** | "Claude Code wrote its own oversight system" text overlay; attribution asymmetry in Scene 6; the recursive governance claim |

### Adversary D: Skeptical Developer at the Event

| Attribute | Detail |
|-----------|--------|
| **Goal** | Fact-check every technical claim in real time; identify anything that does not survive a 5-minute repository audit on their phone |
| **Capability** | Can pull the GitHub URL immediately, count agent files, read the README, try a uv install, check the test suite |
| **Motivation** | Engineering culture norms; developer credibility depends on not being credulous about marketing claims; social currency for being the person who spots the overreach |
| **Access** | Public: the GitHub URL shown on screen, any public documentation |
| **Primary Targets** | "33 agents" stat, repository readiness, test count, the quality gate threshold claim |

---

## Findings Table

| ID | Attack Vector | Category | Exploitability | Severity | Priority | Defense | Affected Dimension |
|----|---------------|----------|----------------|----------|----------|---------|-------------------|
| RT-001-v2 | Scene 6 narration creates asymmetric attribution: "Every line written by Claude Code, directed by a human" -- adversary reads "the human directed; the AI only typed" collapsing the authorship claim | Ambiguity | High | Critical | P0 | Missing | Internal Consistency |
| RT-002-v2 | "CLAUDE CODE WROTE ITS OWN OVERSIGHT SYSTEM" text overlay -- AI safety researcher frames this as misleading because the system was designed by a human; "oversight" in AI safety context carries specific connotations the claim does not satisfy | Ambiguity | Medium | Critical | P0 | Missing | Evidence Quality |
| RT-003-v2 | "33 agents" stat retained verbatim with no hedge, no verification date, no "30+" rounding -- still enumerable and falsifiable in 2 minutes by any developer with repo access | Dependency | High | Major | P1 | Missing | Evidence Quality |
| RT-004-v2 | "Nobody had a fix for enforcement" -- LangMem (LangChain memory layer) and MemGPT's letta-hooks implement in-session behavioral constraint injection; competitor tech lead will name these from the floor | Circumvention | High | Major | P1 | Missing | Internal Consistency |
| RT-005-v2 | Quality gate visual shows score "calculating in real-time" to 0.93-0.94 -- but the tool being scored is grading its own work using its own rubric; adversary frames this as circular self-validation with no independent benchmark | Boundary | Medium | Major | P1 | Missing | Methodological Rigor |
| RT-006-v2 | github.com/geekatron/jerry repository unconfirmed public and release-ready; no contingency path in script; developer adversary checks URL during Scene 6 and finds 404 or private repo | Dependency | High | Major | P1 | Missing | Completeness |
| RT-007-v2 | InVideo AI visual direction specifies "second terminal framing the first" (Scene 1) and "logo materializes from scattered code fragments" (Scene 6) -- InVideo may render these as generic stock footage, breaking the technical credibility of the cold open and close | Boundary | Medium | Minor | P2 | Partial | Actionability |
| RT-008-v2 | Music style descriptions (e.g., "Aggressive distorted bass, industrial edge. 130 BPM") could be interpreted by InVideo or a production team as close enough to the named commercial tracks they replaced -- residual IP inference risk if production team uses the description to source the named originals | Dependency | Low | Minor | P2 | Partial | Completeness |

---

## Finding Details

### RT-001-v2: Asymmetric Attribution in Scene 6 Narration [CRITICAL]

**Attack Vector:** The v2 Scene 6 narration states: "Every line written by Claude Code, directed by a human who refused to compromise." The grammatical structure presents two parallel agents: (1) Claude Code as line-writer, (2) a human as director. An adversary -- especially an AI safety researcher or Anthropic legal reviewer -- will parse this as: the human made all decisions of consequence (direction, architecture, what to build, when to accept), and Claude Code performed the mechanical act of text generation (writing lines). Under this reading, "Claude Code wrote its own oversight system" reduces to "a human designed an oversight system and used an LLM to generate the code." This is not merely a semantic attack -- it is the factually accurate account of how Claude Code sessions operate. The adversary does not need to dispute anything in the script; they only need to apply the most literal reading of the v2 narration itself. The v1 iteration was vulnerable because it overclaimed. The v2 fix, by explicitly naming both agents ("written by Claude Code, directed by a human"), inadvertently provides the attack vector's strongest evidence from within the script.

**Category:** Ambiguity
**Exploitability:** High -- The attack requires only reading the script's own Scene 6 narration literally. No external knowledge required. Available to any critic, journalist, or attendee.
**Severity:** Critical -- The v2 fix to the attribution problem has created a new version of the same problem. The central thesis -- "Claude Code wrote its own oversight system" -- is now undermined by the same sentence that was intended to add accuracy. If challenged in Q&A ("But a human directed everything, right?"), the presenter cannot answer no.
**Existing Defense:** None. The script presents both claims simultaneously without a framing device that reconciles them.
**Evidence:** Scene 6 narration: `"Every line written by Claude Code, directed by a human who refused to compromise."` Scene 1 text overlay: `CLAUDE CODE WROTE ITS OWN OVERSIGHT SYSTEM`. The juxtaposition of these two claims -- "Claude Code wrote" AND "directed by a human" -- is the attack surface.
**Dimension:** Internal Consistency
**Countermeasure:** Reframe Scene 6 to integrate rather than bifurcate the attribution. The narration should make explicit that the interesting claim is not about autonomous agency but about human-AI collaboration at production scale: "Every line of production code: Claude Code. Every architectural call, every quality gate passed or failed, every decision to ship -- human. That's not a limitation. That's the point." Alternatively, preserve the Scene 6 closer but move "directed by a human" to the opening scene as a framing device rather than burying it in the close, so the entire film is understood as a collaboration story rather than an autonomous AI story. The text overlay "CLAUDE CODE WROTE ITS OWN OVERSIGHT SYSTEM" should add a parenthetical: "(directed by a human)" or be replaced with "HUMAN-DIRECTED. AI-WRITTEN. SELF-ENFORCING." which accurately captures all three claims and survives every adversary perspective.
**Acceptance Criteria:** Scene 6 narration and opening text overlay are internally consistent: either both claim full Claude Code authorship with no human direction acknowledgment (requires removing "directed by a human"), or both explicitly frame the work as human-directed AI code generation (requires the text overlay to match). The two framings cannot coexist in the same script without contradiction.

---

### RT-002-v2: "WROTE ITS OWN OVERSIGHT SYSTEM" -- AI Safety Attribution Claim [CRITICAL]

**Attack Vector:** The Scene 1 text overlay "CLAUDE CODE WROTE ITS OWN OVERSIGHT SYSTEM" uses the word "oversight" -- a term with specific, well-established meaning in AI safety discourse (Amodei et al. 2016, Constitutional AI, EU AI Act Article 14 "human oversight" requirements). An AI safety researcher in the audience will read "Claude Code wrote its own oversight system" as: an AI created the system that governs its own behavior, without human oversight of that system's design. This is the exact architecture that AI safety practitioners argue is dangerous and that EU AI Act human oversight requirements are designed to prevent. The adversary does not need to dispute that Jerry exists or works -- they only need to note that marketing it as "AI-written AI oversight" at a public event with Anthropic branding creates a narrative that Anthropic's safety team would likely want to control. Furthermore, the Anthropic legal/PR reviewer will flag that this phrasing could be cited in regulatory contexts as evidence that Anthropic encourages autonomous AI self-governance.

**Category:** Ambiguity
**Exploitability:** Medium -- Requires AI safety domain knowledge to mount the precise attack. However, at a Claude Code birthday party with Anthropic engineers and researchers in attendance, this expertise is near-certain to be present.
**Severity:** Critical -- Reputational risk to Anthropic if the "oversight" phrasing is screenshot-shared with AI safety researchers outside the event. The attack surface is the text overlay itself -- permanently visible as a still image, shareable without context.
**Existing Defense:** None. The word "oversight" in "wrote its own oversight system" is unqualified and has no accompanying context that disambiguates from the AI safety usage.
**Evidence:** Scene 1 text overlay: `CLAUDE CODE WROTE ITS OWN OVERSIGHT SYSTEM`. The term "oversight" appears in no other part of the script, so this overlay bears the full weight of the claim.
**Dimension:** Evidence Quality
**Countermeasure:** Replace "oversight" with the technically accurate term for what Jerry is. Options: "CLAUDE CODE WROTE ITS OWN QUALITY ENFORCEMENT SYSTEM" (accurate, non-triggering), "CLAUDE CODE WROTE ITS OWN GUARDRAILS" (Anthropic's preferred term for behavioral constraints), "CLAUDE CODE WROTE ITS OWN RULE ENGINE" (technical, specific). The narration already uses "guardrails" framing implicitly ("quality gates," "enforcement," "constitutional governance") -- the text overlay should align with this vocabulary rather than importing an AI safety term with adverse connotations.
**Acceptance Criteria:** The word "oversight" is removed from the Scene 1 text overlay and replaced with a term that describes Jerry's actual function (quality enforcement, guardrails, behavioral constraints) without triggering AI safety attribution concerns. Anthropic legal or comms team should review the replacement before production lock.

---

### RT-003-v2: "33 Agents" -- Unhedged Enumerable Stat [MAJOR]

**Attack Vector:** The v2 script retains "Thirty-three agents across seven skills" verbatim in Scene 3 narration and "33 AGENTS / 7 SKILLS" in the text overlay. No verification hedge, no "as of date," no minimum floor ("30+"). Developer adversary D pulls the repository on their phone during Scene 5 or Scene 6, navigates to the skills directory, and counts agent markdown files. If the count is 31, 32, or 34 -- due to agent files added or removed between script lock (Feb 18) and event (Feb 21) -- they can publicly challenge the stat in Q&A. The exploit does not require the count to be wrong by much; even one agent off is sufficient to discredit the "this is production-grade code" claim.

**Category:** Dependency
**Exploitability:** High -- Any developer with repo access and basic shell knowledge can run a directory listing in under 60 seconds. The number is specific and enumerable.
**Severity:** Major -- Inaccurate technical stat in the "proof" scene undermines the entire Scene 5 credibility argument at the moment of maximum persuasive intent.
**Existing Defense:** None. The v2 script did not implement the iteration 1 countermeasure recommendation to hedge the stat or use a minimum floor.
**Evidence:** Scene 3 narration: `"Thirty-three agents across seven skills."` Scene 3 text overlay: `33 AGENTS / 7 SKILLS`. Self-review table: `"33 agents"` listed as PASS with note "actual: 3,257 at time of writing" (for tests) -- but no equivalent verification note for agent count.
**Dimension:** Evidence Quality
**Countermeasure:** (1) Execute a repository audit within 24 hours of the event: `find . -name "*.md" -path "*/agents/*" | wc -l` and `ls skills/ | wc -l`. (2) If the count is 33, lock the script. If not, update the stat to match. (3) Add a hedge to the narration: "more than thirty agents across seven skills" -- this is more defensible and still impressive. The text overlay can remain "33 AGENTS / 7 SKILLS" if verified, or change to "30+ AGENTS / 7 SKILLS" if hedged.
**Acceptance Criteria:** Agent count in script matches repository artifact count within 24 hours of event, OR narration and overlay are hedged to "30+" or equivalent minimum floor.

---

### RT-004-v2: "Nobody Had a Fix for Enforcement" -- Competitor Falsifiability Attack [MAJOR]

**Attack Vector:** The v2 fix narrowed the competitor erasure claim from "nobody had a fix" to "nobody had a fix for enforcement." This is a stronger claim but creates a more specific falsifiability target. Adversary B (competitor tech lead) can name, from memory: (1) LangMem -- LangChain's memory layer, which includes runtime behavioral constraint injection via `store.put` with schema-validated constraint objects, directly competitive with Jerry's hook-based enforcement; (2) MemGPT (Letta) -- implements in-context enforcement via its OS metaphor with page manager interrupts that enforce behavioral policies; (3) OpenAI's Assistants API -- enforces model behavior via system-level instructions that persist across session context and cannot be overridden by user messages; (4) Guardrails AI -- open-source framework explicitly designed to enforce LLM output quality constraints at the application layer. Any one of these is sufficient to falsify "nobody had a fix for enforcement." The adversary only needs one counterexample. At a Claude Code showcase, adversary B is likely the LangChain or LangMem developer relations team, and they are definitely in that room.

**Category:** Circumvention
**Exploitability:** High -- Competitor tool knowledge is common among senior developers; the specific claim "enforcement" now invites a precise comparison rather than a general one; the adversary does not need to argue Jerry is worse, only that the "nobody" claim is false.
**Severity:** Major -- The problem statement in Scene 2 is the logical foundation for Jerry's existence. If "nobody had a fix for enforcement" is publicly contested with named counterexamples in Q&A, the entire film's argument is undermined at its premise.
**Existing Defense:** None. "Tools handle memory. Nobody had a fix for enforcement" is the full extent of the differentiation claim. No qualifier ("inside a Claude Code session," "using Claude Code hooks," "for agentic coding workflows specifically") limits the scope.
**Evidence:** Scene 2 narration: `"Tools handle memory. Nobody had a fix for enforcement."` The claim is absolute and unscoped: "nobody" and "enforcement" without qualifier.
**Dimension:** Internal Consistency
**Countermeasure:** Scope the enforcement claim to the specific context that is defensible and unique to Jerry. The defensible claim is: "Nobody had a fix for in-session enforcement inside a Claude Code agentic workflow -- quality gates that activate on every hook call, before and after every tool use, catching rule drift at the moment it happens rather than after the session ends." This is defensible because it is specific to Claude Code's hook architecture, which no external framework implements. Revised narration: "Context fills. Rules drift. Quality rots. General tools handle memory. Nobody had enforcement built into the session hooks -- catching rule drift before the next line of code is written." This survives the Guardrails AI, LangMem, and MemGPT counterexamples because those tools operate at the application layer or across sessions, not inside Claude Code's pre/post-tool-call hooks.
**Acceptance Criteria:** Problem statement narration scopes the "enforcement" claim to Claude Code's hook architecture specifically, making the claim non-falsifiable by any tool that operates outside the Claude Code session hook model.

---

### RT-005-v2: Self-Grading Quality Score Visual -- Circular Validation [MAJOR]

**Attack Vector:** Scene 5 visual direction: "Quality score calculating in real-time: dimension by dimension, the weighted composite climbing to 0.92... 0.93... 0.94. The quality gate PASSES." This is Jerry scoring its own work using its own rubric, with its own agent (adv-scorer) applying its own LLM-as-Judge. Adversary B (competitor tech lead) or Adversary C (AI safety researcher) will note: the quality gate passing is not an independent verification -- it is the tool asserting it is good by its own standards. No external benchmark, no third-party audit, no independent reproduction of the quality scores is shown or implied. "This isn't a demo. This is production-grade code" -- but the only evidence of production quality is the tool's own self-assessment. This is epistemically equivalent to grading your own exam and announcing you passed.

**Category:** Boundary
**Exploitability:** Medium -- Requires methodological awareness to mount the critique. Every researcher and senior engineer in the room has this awareness. The attack is available to anyone who asks "but who checked the quality check?"
**Severity:** Major -- Scene 5 is the "proof" scene. If the proof's central visual (the quality gate passing) is dismissed as circular self-validation, the entire "production-grade" claim is left without independent support.
**Existing Defense:** None. The script offers no external benchmark, third-party audit, or independent quality verification alongside the self-score. "3,000+ tests passing" is the only external-style evidence, but test coverage and quality gate are separate concepts.
**Evidence:** Scene 5 visual: `"Quality score calculating in real-time: dimension by dimension, the weighted composite climbing to 0.92... 0.93... 0.94. The quality gate PASSES."` Scene 5 narration: `"A quality gate at zero-point-nine-two that does not bend."` Both present the self-scored quality gate as objective evidence of production quality.
**Dimension:** Methodological Rigor
**Countermeasure:** Add external validation anchors to Scene 5. Options: (1) Show the tournament structure -- "Ten adversarial strategies, run independently, all must pass before any deliverable ships." The multi-strategy tournament structure provides more epistemic credibility than a single composite score because the strategies are named and enumerable. The claim shifts from "we scored ourselves" to "ten independent attack strategies all failed to find disqualifying flaws." (2) Add a production note in the visual: "Score shown is from C4 tournament review (10 strategies, 3 iterations)" -- the iterative structure is an implicit external validation. (3) In narration, replace "A quality gate at zero-point-nine-two that does not bend" with "A quality gate at zero-point-nine-two, enforced by ten adversarial strategies that run before any deliverable ships." The adversarial strategies are the external check; foreground them rather than the composite score.
**Acceptance Criteria:** Scene 5 visual and narration present the quality evidence in a way that survives the "you're grading your own work" objection, by foregrounding the multi-strategy adversarial tournament structure as the validation mechanism rather than the composite score alone.

---

### RT-006-v2: github.com/geekatron/jerry -- Unresolved Repository Readiness [MAJOR]

**Attack Vector:** Identical to RT-006-s001-20260218 from iteration 1. The v2 script makes no change to the Scene 6 repository CTA and no contingency path was added. Developer adversary D checks github.com/geekatron/jerry on their smartphone during the presentation. If the repository is private, does not exist at that URL, lacks a README, or has no working installation path, the CTA fails live in front of Anthropic leadership. The film ends on "Come build with us" and the invitation is immediately falsified by a 404 or empty repository. This is the highest-impact operational risk remaining in v2 because it activates automatically -- no adversary effort required.

**Category:** Dependency
**Exploitability:** High -- Checking a URL takes 5 seconds. The exploit is passive and automatic.
**Severity:** Major -- A broken repository link at the showcase close is a credibility failure that cannot be recovered from in the room. It makes the "open source" claim false at the moment it is made.
**Existing Defense:** None. Neither the script nor any self-review note documents a pre-event URL verification requirement or contingency plan.
**Evidence:** Scene 6 text overlay: `github.com/geekatron/jerry`. Scene 6 narration: `"Jerry. Open source. Apache 2.0. [...] Come build with us."` Self-review table does not include a repository readiness check.
**Dimension:** Completeness
**Countermeasure:** (1) Add an explicit pre-event checklist item to the self-review table: "github.com/geekatron/jerry is publicly accessible, has README, LICENSE (Apache 2.0), and at least one usage example -- verified by fresh browser session (no GitHub auth) at least 24 hours before Feb 21." (2) Add a contingency path to Scene 6 production notes: "If repository cannot be confirmed public by Feb 20 23:59 PST, replace URL overlay with 'jerry.dev' or 'link in bio' and revise narration to 'Open source. Coming February 21.'" (3) Perform the smoke test now and confirm status.
**Acceptance Criteria:** Repository is confirmed publicly accessible with README, LICENSE (Apache 2.0), and at least one functional usage example at least 24 hours before the event. Contingency narration exists in the script for the failure case.

---

## Recommendations

### P0 -- MUST Mitigate Before Production Lock

**RT-001-v2: Asymmetric Attribution -- Scene 6 Narration**
- Action: Revise Scene 6 narration and Scene 1 text overlay to adopt a single consistent attribution framing that survives both the "overclaim" and "underclaim" adversary attacks.
- Recommended approach: Replace "Every line written by Claude Code, directed by a human who refused to compromise" with "Every line of production code: written by Claude Code. Every architectural decision: human. That's the collaboration." Replace text overlay with "CLAUDE CODE WROTE THE CODE. HUMANS CALLED THE SHOTS. THE FRAMEWORK ENFORCES BOTH." or similar two-part framing.
- Alternative: If the production prefers a single claim, use "Claude Code wrote every line. Human-directed, end to end." in narration and "CLAUDE CODE WROTE EVERY LINE" as overlay -- removing the grammatical agent-splitting entirely.
- Acceptance Criteria: Scene 1 text overlay and Scene 6 narration make the same claim about who did what. The claim survives both "AI overclaimed" and "human did everything" attacks simultaneously.
- Owner: ps-architect-001 revision.

**RT-002-v2: "Oversight" Term in Scene 1 Text Overlay**
- Action: Replace "CLAUDE CODE WROTE ITS OWN OVERSIGHT SYSTEM" with vocabulary that accurately describes Jerry without triggering AI safety "oversight" connotations.
- Recommended replacement: "CLAUDE CODE WROTE ITS OWN GUARDRAILS" (Anthropic terminology), "CLAUDE CODE WROTE ITS OWN ENFORCEMENT ENGINE" (technical), or "CLAUDE CODE WROTE ITS OWN QUALITY FRAMEWORK" (descriptive).
- Acceptance Criteria: The word "oversight" does not appear in the Scene 1 text overlay. Replacement term accurately describes Jerry's function. Anthropic comms/legal review of replacement term before production lock.
- Owner: ps-architect-001 / Anthropic comms review.

### P1 -- SHOULD Mitigate Before Anthropic Showcase

**RT-003-v2: "33 Agents" -- Verification Required**
- Action: Execute agent count audit within 24 hours of event. Either confirm 33 is exact and lock, or hedge narration to "more than thirty agents across seven skills" and overlay to "30+ AGENTS / 7 SKILLS."
- Acceptance Criteria: Agent count in script matches repository artifact count within 24 hours of event.
- Owner: Technical verification / script lock process.

**RT-004-v2: Enforcement Claim Scope**
- Action: Revise Scene 2 narration to scope "enforcement" to Claude Code's hook architecture specifically, making the claim non-falsifiable by LangMem, MemGPT, or Guardrails AI.
- Recommended narration: "Context fills. Rules drift. Quality rots. General tools handle memory. Nobody had enforcement baked into the session hooks -- catching rule drift before the next line of code executes."
- Acceptance Criteria: Problem statement cannot be falsified by naming any tool that operates outside Claude Code's pre/post-tool-call hook model.
- Owner: ps-architect-001 revision.

**RT-005-v2: Self-Grading Quality Score Visual**
- Action: Revise Scene 5 visual direction and narration to foreground the multi-strategy adversarial tournament as the validation mechanism rather than the composite score.
- Recommended narration: "Ten adversarial strategies. All running before anything ships. A quality gate at zero-point-nine-two that they must all pass. This isn't a demo. This is production-grade code."
- Recommended visual: Remove the "score climbing in real-time" animation. Replace with: "Text overlay sequence: 10 ADVERSARIAL STRATEGIES. 3 TOURNAMENT ITERATIONS. 0.92 QUALITY GATE. ALL PASSED."
- Acceptance Criteria: Scene 5 quality evidence framing cannot be dismissed as circular self-validation. The adversarial tournament structure is the primary evidence claim.
- Owner: ps-architect-001 revision.

**RT-006-v2: Repository Readiness Operational Confirmation**
- Action: Confirm github.com/geekatron/jerry is publicly accessible with README, LICENSE (Apache 2.0), and at least one usage example at least 24 hours before Feb 21. Add contingency path to production notes.
- Acceptance Criteria: URL smoke test passes (public access, no auth required) before Feb 20 23:59 PST. If test fails, Scene 6 is revised with contingency CTA.
- Owner: Repository maintainer / pre-event ops.

### P2 -- MAY Address (Monitor)

**RT-007-v2: InVideo Scene 1 and Scene 6 Visual Fidelity**
- Risk: "Second terminal framing the first" (Scene 1) and "logo materializes from scattered code fragments" (Scene 6) may render as generic stock footage in InVideo, losing the technical inception metaphor that makes the cold open land.
- Mitigation: Add fallback direction to each scene: "If InVideo cannot render nested terminals, use side-by-side terminal windows with visible code generation in each." For Scene 6: "If logo materialization is not achievable, use fade-in of static Jerry logo over terminal background."
- Priority: Monitor. If production lock reveals InVideo rendering issues, escalate to P1.

**RT-008-v2: Music Description Inference Risk**
- Risk: Atmospheric descriptions like "Low analog synth drone building tension. Dark, minimal, sub-bass pulse. 70 BPM" (Scene 1) or "Aggressive distorted bass, industrial edge. 130 BPM" (Scene 2) are close enough to the original named tracks (Kendrick "DNA.", Beastie Boys "Sabotage") that a production team sourcing music might locate the originals as a reference. If they then use the originals without clearing rights, the RT-001 fix is circumvented.
- Mitigation: Add a production note to the Music Sourcing section: "Music must be sourced from licensed production libraries only (Epidemic Sound, Artlist, or equivalent). Do NOT use named commercial recordings as references or sources. The style descriptions are for tonal guidance to the production music search, not referrals to specific tracks."
- Priority: Low. The risk is indirect and requires active misuse of the descriptions.

---

## Scoring Impact

| Dimension | Weight | Impact | RT Findings | Rationale |
|-----------|--------|--------|-------------|-----------|
| Completeness | 0.20 | Negative | RT-006-v2 | Repository readiness remains the sole unmitigated Major finding from iteration 1. The open source CTA is the film's final deliverable -- if the link fails, the entire close is incomplete. No contingency path in script. |
| Internal Consistency | 0.20 | Negative | RT-001-v2, RT-004-v2 | Scene 6 narration simultaneously claims Claude Code wrote every line AND a human directed everything -- two claims that are individually true but create an internal contradiction when presented as a unified attribution. RT-004-v2 enforcement claim is internally inconsistent with the existence of LangMem and MemGPT enforcement tools. |
| Methodological Rigor | 0.20 | Negative | RT-005-v2 | Quality gate evidence (Scene 5) presents self-scoring as proof of quality. The iterative tournament structure exists but is not surfaced as the validation mechanism. A methodologically rigorous quality claim requires independent or multi-party validation framing. |
| Evidence Quality | 0.15 | Negative | RT-002-v2, RT-003-v2 | "Oversight" term creates an evidence gap between what is claimed and what is implemented. "33 agents" is an unhedged enumerable stat with no verification path. |
| Actionability | 0.15 | Neutral | RT-007-v2 | CTA (GitHub URL, Apache 2.0, "come build with us") is present and clear. InVideo rendering risk is a production concern, not a script-level actionability gap. |
| Traceability | 0.10 | Neutral | -- | Jerry's capabilities (agents, skills, enforcement layers, quality threshold) trace to the actual framework. No traceability defects specific to v2. The attribution issue (RT-001-v2) is a framing gap, not a traceability gap. |

**Net Composite Impact Assessment:** Four dimensions show negative impact (Completeness, Internal Consistency, Methodological Rigor, Evidence Quality). Two are neutral (Actionability, Traceability). Two Critical findings (RT-001-v2, RT-002-v2) impact Completeness and Evidence Quality dimensions (combined weight 0.35). The v2 script eliminated the two most dangerous attack vectors from iteration 1 (IP liability, absolute attribution overclaim) but introduced two new Critical vectors through the attribution fix itself. Before P0/P1 mitigations, the v2 deliverable likely scores in the REVISE band (0.85-0.91). After addressing all P0 and P1 findings, the deliverable should reach PASS (>= 0.92).

**Overall Assessment:** REVISE. The script's creative execution, emotional arc, and structural coherence are strong. The v2 fixes successfully closed the highest-risk iteration 1 vectors. The remaining attack surface is concentrated in: (1) attribution framing -- the fix created a new asymmetric attribution vulnerability; (2) "oversight" terminology with AI safety implications; (3) enforcement claim specificity; (4) quality evidence framing. None of these require structural redesign. All are addressable with targeted narration and text overlay revisions.

---

## H-15 Self-Review

| Check | Status | Notes |
|-------|--------|-------|
| H-16 compliance verified | PASS | S-003 Steelman confirmed (iteration 1). S-001 iteration 1 confirmed as prior Red Team. Iteration 2 executes against v2 script as required. |
| Four distinct threat actor profiles defined with goal/capability/motivation | PASS | Adversary A (Anthropic legal/PR), B (competitor tech lead), C (AI safety researcher), D (skeptical developer) -- each with explicit attributes |
| All 5 attack vector categories explored | PASS | Ambiguity (RT-001-v2, RT-002-v2, RT-004-v2), Boundary (RT-005-v2, RT-007-v2), Circumvention (RT-004-v2), Dependency (RT-003-v2, RT-006-v2, RT-008-v2), Degradation -- not separately identified but covered within RT-001-v2 attribution drift |
| Minimum 4 attack vectors identified | PASS | 8 vectors identified (RT-001-v2 through RT-008-v2) |
| Iteration 1 finding disposition documented | PASS | All 10 prior RT findings assessed in Iteration 1 Disposition table |
| Critical and Major findings have expanded details | PASS | RT-001-v2 through RT-006-v2 fully expanded with attack vector, evidence, countermeasure, acceptance criteria |
| Countermeasures provided for all P0 and P1 findings | PASS | RT-001-v2 through RT-006-v2 each have specific countermeasure and acceptance criteria |
| Findings table uses RT-NNN-{execution_id} format | PASS | RT-001-v2 through RT-008-v2 format used throughout |
| Scoring impact maps to all 6 S-014 dimensions | PASS | All six dimensions assessed |
| Adversary perspective maintained throughout | PASS | Each finding written from specific adversary perspective (A/B/C/D) framing, not generic quality critique |
| Leniency bias counteracted | PASS | Two Critical findings identified despite v2 improvements; no findings dismissed as "minor" when they create public brand exposure |
| v2-specific attack vectors identified (not just iteration 1 repeats) | PASS | RT-001-v2 (attribution asymmetry), RT-002-v2 ("oversight" term), RT-005-v2 (self-grading), RT-007-v2 (InVideo) are new vectors not present in iteration 1 |
| Navigation table present (H-23/H-24) | PASS | Nav table with anchor links at top |

---

*Strategy: S-001 Red Team Analysis*
*Executor: adv-executor (S-001) -- Iteration 2*
*SSOT: `.context/rules/quality-enforcement.md`*
*Template: `.context/templates/adversarial/s-001-red-team.md` v1.0.0*
*Date: 2026-02-18*
*Execution ID: s001-v2-20260218*
