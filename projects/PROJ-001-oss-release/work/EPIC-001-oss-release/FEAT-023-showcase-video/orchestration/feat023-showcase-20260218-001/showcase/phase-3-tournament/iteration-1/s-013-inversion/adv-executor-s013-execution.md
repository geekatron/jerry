# Inversion Report: Jerry Framework Hype Reel Script

**Strategy:** S-013 Inversion Technique
**Deliverable:** `showcase/phase-2-script/ps-architect-001/ps-architect-001-hype-reel-script.md`
**Criticality:** C4 (public-facing, irreversible -- Anthropic 1st Birthday Showcase)
**Date:** 2026-02-18
**Reviewer:** adv-executor (S-013)
**H-16 Compliance:** S-003 Steelman is required before this adversarial sequence (C4 tournament); this execution proceeds as part of the full C4 tournament round where S-003 was applied prior.
**Goals Analyzed:** 8 | **Assumptions Mapped:** 18 | **Vulnerable Assumptions:** 9

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment and recommendation |
| [Step 1: Goal Inventory](#step-1-goal-inventory) | Explicit and implicit goals, stated precisely |
| [Step 2: Anti-Goal Inventory](#step-2-anti-goal-inventory) | What would guarantee failure for each goal |
| [Step 3: Assumption Map](#step-3-assumption-map) | All explicit and implicit assumptions |
| [Step 4: Stress-Test Results](#step-4-stress-test-results) | IN-NNN findings with severity |
| [Findings Table](#findings-table) | Consolidated findings by severity |
| [Finding Details](#finding-details) | Expanded analysis of Critical and Major findings |
| [Recommendations](#recommendations) | Prioritized mitigations with acceptance criteria |
| [Scoring Impact](#scoring-impact) | Mapping findings to S-014 dimensions |

---

## Summary

Inversion analysis of the Jerry Framework 2-minute hype reel script reveals 2 Critical and 5 Major vulnerable assumptions against 8 goals inverted across 18 mapped assumptions. The most acute failure cluster is the **music rights and production assumptions**: the script specifies five major commercial tracks by name (Kendrick Lamar, Beastie Boys, Daft Punk, Wu-Tang Clan, Pusha T) with zero acknowledgment of licensing risk, which would either force last-minute substitution that breaks the carefully engineered music arc, or expose the production to copyright violation at a public event. A second Critical finding is the **audience segmentation mismatch**: the script is calibrated for a developer who already feels context rot pain, but the stated audience also includes Anthropic leadership and investors for whom the meta-angle ("Claude built its own guardrails") may require more explicit framing to land. Five Major findings address the Shane McConkey recognizability gap, the GitHub repo live status assumption, the InVideo AI capability boundaries, the "built entirely by Claude Code" claim precision, and the 15-second context rot explanation sufficiency. The script is **not rejected** -- its structure, energy, and specificity are strong -- but it requires targeted mitigation of the 2 Critical assumptions before it is safe to commit to production.

**Recommendation:** REVISE -- Address Critical findings (IN-001, IN-002) before production handoff. Major findings (IN-003 through IN-007) should be mitigated where feasible before Feb 21.

---

## Step 1: Goal Inventory

| Goal ID | Goal | Type | Measurable Form |
|---------|------|------|-----------------|
| G-01 | Capture audience attention in the first 15 seconds | Explicit | Viewer does not disengage during cold open; hook is felt as novel, not generic |
| G-02 | Communicate the meta-angle: Claude Code built its own oversight system | Explicit | A viewer with no prior Jerry knowledge can state this after watching |
| G-03 | Explain context rot as a real, felt problem -- before revealing the solution | Explicit | A non-Claude-Code-user understands "sessions degrade" after 15 seconds of Scene 2 |
| G-04 | Demonstrate credibility via concrete, accurate stats | Explicit | Stats are verifiable and feel earned, not inflated |
| G-05 | Convey Saucer Boy personality (serious + fun, not one or the other) | Explicit | Anthropic leadership and developers both respond positively; neither group feels it is off-tone |
| G-06 | Drive audience to the GitHub repo for OSS participation | Explicit | Viewer knows the URL and CTA ("come build with us") at close |
| G-07 | Fit within 2:00 runtime while landing each beat on music cues | Explicit | Narration at 140 WPM x 276 words = ~1:58; each scene transition aligns with music |
| G-08 | Be producible in InVideo AI from the scene directions as written | Implicit | InVideo AI can execute every visual and audio direction without assets that do not exist |

---

## Step 2: Anti-Goal Inventory

| Anti-Goal ID | Inverted Goal | Failure Condition | Deliverable Coverage |
|-------------|---------------|-------------------|----------------------|
| AG-01 | Fail to capture attention in 15 seconds | Open with text-heavy explanation of a technical problem before showing anything visceral | Partial -- cold open is visual-first, but relies on InVideo AI rendering a "nested terminal inception" convincingly |
| AG-02 | Obscure or lose the meta-angle | Make "Claude built this" sound like a footnote rather than the primary reveal | Weak -- the text overlay `CLAUDE CODE BUILT ITS OWN OVERSIGHT SYSTEM` runs only in Scene 1; not reinforced across remaining 5 scenes |
| AG-03 | Make context rot feel abstract to a non-developer | Use technical vocabulary without visceral visual anchoring for a non-developer audience | Partial -- the split screen degradation visual helps, but "context fills" as narration may not land for investors |
| AG-04 | Present stats that feel made-up or unverifiable | Use large round numbers, no specificity, no connection to impact | Partial -- stats are specific (3,195+, 0.92, 33, 7, 10, 5) but the script has no mechanism to validate them on-screen |
| AG-05 | Alienate Anthropic leadership or investors with cultural references | Use hip-hop and extreme sports references without anchoring them to the professional context | Unaddressed -- no fallback if McConkey or Wu-Tang references do not land with non-developer audience segments |
| AG-06 | Fail to convert to repo engagement | Make the URL appear briefly and without context for why to visit | Partial -- "come build with us" is minimal; no description of what a visitor will find |
| AG-07 | Blow the runtime or land beats on silence | Narration word count is imprecise; music cuts do not align with scene transitions | Partial -- self-review passes this, but WPM is an average that does not account for scene pauses and visual hold time |
| AG-08 | Produce an InVideo AI render that looks AI-generated and cheap | Scene directions require visual complexity beyond InVideo AI's reliable output quality | Unaddressed -- no fallback production approach if InVideo fails to render convincingly |

**Anti-goals unaddressed by deliverable:** AG-02 (meta-angle not reinforced after Scene 1), AG-05 (cultural references without audience-segment fallback), AG-08 (no production fallback).

---

## Step 3: Assumption Map

| ID | Assumption | Type | Category | Confidence | Validation Status | Consequence if Wrong |
|----|------------|------|----------|------------|-------------------|---------------------|
| A1 | 276 words at 140 WPM = ~1:58 runtime | Explicit | Temporal | High | Mathematically verified | Minor: 10-15 sec overage or underage |
| A2 | Target audience = Anthropic leadership + investors + developers | Explicit | Environmental | High | Stated in context | Major: calibration mismatch |
| A3 | InVideo AI is the production platform | Explicit | Technical | High | Stated in context | Major: scene directions may be wrong format |
| A4 | InVideo AI can render convincing "code writing code" nested terminal visuals | Implicit | Technical | Low | Not validated | Critical: cold open collapses if this fails |
| A5 | The five named commercial music tracks are available for use at the event | Implicit | Environmental | Low | Not validated | Critical: entire music arc must be rebuilt |
| A6 | A "Jerry logo" exists or can be generated for the Scene 6 close | Implicit | Resource | Medium | Not confirmed | Major: Scene 6 visual direction fails |
| A7 | `github.com/geekatron/jerry` is public and live by Feb 21, 2026 | Implicit | Environmental | Medium | Not confirmed | Critical: CTA points to dead link on-screen |
| A8 | The audience has sufficient Claude Code familiarity for the meta-angle to land | Implicit | Audience | Medium | Not validated | Major: hook is opaque to investors and leadership |
| A9 | "Shane McConkey" is recognizable to the showcase audience | Implicit | Audience | Low | Not validated | Major: Scene 4 analogy falls flat |
| A10 | Audience can absorb technical vocabulary (constitutional governance, hexagonal architecture) without confusion | Implicit | Audience | Medium | Not validated | Minor: Scene 3 montage too fast for comprehension |
| A11 | Anthropic leadership and investors respond positively to hip-hop references and "Saucer Boy" | Implicit | Audience | Medium | Not validated | Major: tone mismatch with formal audience segment |
| A12 | "3,195+ tests" is accurate as of Feb 21, 2026 | Implicit | Technical | Medium | Requires verification before event | Major: inflated stat damages credibility |
| A13 | "33 agents across seven skills" is accurate on event day | Implicit | Technical | Medium | Requires verification | Minor: stat inaccuracy noticed by technical viewers |
| A14 | "Built entirely by Claude Code" is a defensible claim | Implicit | Technical | Low | Not explicitly confirmed | Major: if any human-authored code exists, claim is challenged |
| A15 | 15 seconds (Scene 2) is sufficient to make a non-user feel context rot | Implicit | Audience | Low | Not validated | Major: problem scene is too fast for non-developers |
| A16 | InVideo AI can reliably execute the described music arc with correct timing | Implicit | Technical | Low | Not validated | Major: music transitions misfire, energy arc breaks |
| A17 | The "Daft Punk vocoder resolving to a single note" is achievable as a distinct audio moment | Implicit | Technical | Low | Not validated | Minor: close loses its clean resolution |
| A18 | 2:00 runtime is optimal for this audience and setting | Implicit | Temporal | Medium | Not validated | Minor: could be too short to establish credibility for investors |

---

## Step 4: Stress-Test Results

| ID | Assumption | Inversion | Plausibility | Severity | Affected Dimension |
|----|------------|-----------|-------------|----------|--------------------|
| IN-001-20260218 | A5: Commercial music tracks available for showcase use | Tracks are NOT licensed; use constitutes copyright infringement OR organizers block playback | **High** -- music rights at public commercial events are routinely enforced | Critical | Methodological Rigor |
| IN-002-20260218 | A8: Audience has Claude Code familiarity for meta-angle to land | Leadership/investor segment does NOT know Claude Code's capabilities; "Claude built its own guardrails" reads as marketing buzzword | **High** -- Anthropic leadership and investors are explicitly listed as audience alongside developers | Critical | Actionability |
| IN-003-20260218 | A9: Shane McConkey is recognizable | McConkey is known in ski/adventure sports culture but is NOT a mainstream tech culture figure; analogy lands with ~30% of audience | **High** -- tech investors have low base-rate exposure to ski culture | Major | Evidence Quality |
| IN-004-20260218 | A7: GitHub repo is public and live | Repo is private or not yet published on Feb 21; CTA displays a 404 to the audience | **Medium** -- OSS release timing relative to event is unconfirmed | Major | Completeness |
| IN-005-20260218 | A4: InVideo AI renders nested terminal inception convincingly | InVideo renders generic stock footage of a keyboard or a flat code editor screenshot; cold open is visually underwhelming | **High** -- generative video AI struggles with precise technical compositions; "terminal inside a terminal" is not a stock template | Major | Methodological Rigor |
| IN-006-20260218 | A14: "Built entirely by Claude Code" is defensible | Any human-authored code, configuration, or prompt engineering is cited as disproving the claim; claim is challenged from the audience or in subsequent media coverage | **Medium** -- the claim is strong and any exception becomes a credibility problem | Major | Evidence Quality |
| IN-007-20260218 | A15: 15 seconds explains context rot to non-developers | Leadership and investor audience does not understand why "context fills" is a catastrophic problem; Scene 2 is visceral to developers but opaque to others | **High** -- "context fills, rules drift, quality rots" is developer-native language | Major | Actionability |
| IN-008-20260218 | A11: Hip-hop references and "Saucer Boy" land positively with all audience segments | Anthropic leadership interprets "C.R.E.A.M. -- Context Rules Everything Around Me" as forced or undignified for an AI safety/quality story | **Low-Medium** -- depends on event culture, but the risk is non-zero with a formal leadership audience | Minor | Internal Consistency |
| IN-009-20260218 | A12: "3,195+ tests" is accurate on event day | Test count has changed (higher or lower) between script creation (2026-02-18) and event (2026-02-21); minor but audience sees a different number if they check | **Medium** -- 3 days of development could change the count | Minor | Traceability |

---

## Findings Table

| ID | Assumption / Anti-Goal | Type | Confidence | Severity | Evidence | Affected Dimension |
|----|------------------------|------|------------|----------|----------|--------------------|
| IN-001-20260218 | Commercial music tracks (Kendrick, Beastie Boys, Daft Punk, Wu-Tang, Pusha T) available for public showcase use | Assumption | Low | **Critical** | Scene 1 "DNA. by Kendrick", Scene 2 "Sabotage", Scene 3 "Harder Better Faster Stronger", Scene 4 "C.R.E.A.M.", Scene 5 "Numbers on the Boards" -- all named as specific commercial tracks with no licensing note | Methodological Rigor |
| IN-002-20260218 | Audience has sufficient Claude Code familiarity for meta-angle to land without additional context | Assumption | Medium | **Critical** | Meta-angle stated only in Scene 1 narration and single overlay; no reinforcement for non-developer audience segments who may not know what "Claude Code" does | Actionability |
| IN-003-20260218 | Shane McConkey is recognizable to tech/investor audience | Assumption | Low | **Major** | Scene 4: "Shane McConkey launching off a cliff in a onesie" as the entire philosophical anchor; Scene 4 narration depends on knowing McConkey to feel the contrast | Evidence Quality |
| IN-004-20260218 | `github.com/geekatron/jerry` is public and live by Feb 21, 2026 | Assumption | Medium | **Major** | Scene 6: URL displayed on screen as primary CTA; "Come build with us" presupposes audience can act immediately | Completeness |
| IN-005-20260218 | InVideo AI can render "code inside a terminal inside a terminal" inception visual convincingly | Assumption | Low | **Major** | Scene 1: "Camera pulls back to reveal the terminal is INSIDE another terminal. Code writing code. The inception moment lands." -- entire cold open premise depends on this rendering | Methodological Rigor |
| IN-006-20260218 | "Built entirely by Claude Code" claim is fully defensible | Assumption | Low | **Major** | Scene 6 narration: "Built entirely by Claude Code" -- no qualifier, no context about what "built entirely" means (infrastructure? prompts? configuration? human review?) | Evidence Quality |
| IN-007-20260218 | 15 seconds of Scene 2 is sufficient to make a non-developer feel context rot | Assumption | Low | **Major** | Scene 2 narration: "Context fills. Rules drift. Quality rots." -- developer-native shorthand that investor/leadership audience may not emotionally register | Actionability |
| IN-008-20260218 | Hip-hop references and "Saucer Boy" energy land positively with Anthropic leadership | Assumption | Medium | **Minor** | Scene 4: Wu-Tang "C.R.E.A.M." reframed as "Context Rules Everything Around Me"; "Saucer Boy" brand throughout | Internal Consistency |
| IN-009-20260218 | "3,195+ tests" stat is accurate as of Feb 21, 2026 | Assumption | Medium | **Minor** | Scene 5: "Three thousand one hundred ninety-five tests. Passing." -- number stated precisely; could change between 2026-02-18 and event day | Traceability |

---

## Finding Details

### IN-001-20260218: Commercial Music Licensing Risk [CRITICAL]

**Type:** Assumption
**Original Assumption:** Five specific commercial tracks are available for use at a public showcase event without licensing complications.
**Inversion:** The tracks are NOT licensed for commercial public performance. Use at a showcase event (Shack15, San Francisco) constitutes public performance requiring sync and performance licenses. Event organizers restrict playback, or post-event clips are flagged/blocked.
**Plausibility:** High. Public performance of commercial music at events requires ASCAP/BMI/SESAC blanket licensing or individual sync licenses. Shack15 may have a venue blanket license covering incidental background music, but a curated video with specific tracks timed to beats likely falls outside blanket license scope. Additionally, any recording or streaming of the event would require separate sync licenses for each track.
**Consequence:** The entire music arc -- which is deeply structural to the script's energy design -- must be rebuilt with royalty-free or licensed alternatives at the last moment, or the video cannot be played. The music cues are not incidental: "Harder, Better, Faster, Stronger" is described as "THE Jerry anthem," and the Daft Punk vocoder closing resolves the video's emotional arc. Substituting royalty-free music changes the emotional landing materially.
**Evidence:** Scene 3: "Harder, Better, Faster, Stronger -- Daft Punk. The vocoder kicks in on the stat montage. This is THE Jerry anthem." Scene 4: "C.R.E.A.M. -- Wu-Tang. The piano loop is unmistakable." Scene 1: "Think the opening seconds of DNA. by Kendrick." No licensing note anywhere in the script.
**Dimension:** Methodological Rigor
**Mitigation:** (1) Confirm Shack15 venue license scope covers video playback with named tracks. (2) For any recording or streaming: obtain individual sync licenses or replace with licensed alternatives before production. (3) Identify royalty-free tracks with equivalent energy for each scene as contingency -- do this NOW before InVideo production locks in the music. The energy profiles to match: [S1: eerie analog pulse building tension] [S2: heavy distorted bass, aggressive] [S3: vocoder-driven upbeat electronic] [S4: iconic minimal piano loop, confident] [S5: hard minimalist beat, nothing but confidence] [S6: single resolving sustained note].
**Acceptance Criteria:** Written confirmation that all named tracks are licensed for the event's scope, OR documented royalty-free alternative for each scene that production team has approved.

---

### IN-002-20260218: Meta-Angle Requires Audience Familiarity With Claude Code [CRITICAL]

**Type:** Assumption
**Original Assumption:** The meta-angle -- "Claude Code built its own guardrails" -- will land as a jaw-dropping reveal for all audience segments including Anthropic leadership and investors.
**Inversion:** Anthropic leadership and investors who are NOT daily Claude Code users do not have the reference point to feel the weight of this claim. "Claude Code built its own guardrails" reads as a generic AI capability statement rather than a genuinely surprising recursive achievement.
**Plausibility:** High. The audience is explicitly stated as three distinct segments with different priors: developers (high Claude Code familiarity), investors (may know Claude broadly but not Claude Code specifically), Anthropic leadership (knows the technology but may evaluate the claim differently given their insider context). The script's cold open narration -- "What happens when you give an AI a blank repo and say: build your own guardrails?" -- assumes the question itself feels surprising. For Anthropic insiders, this may not be surprising at all.
**Consequence:** The hook does not hook 1/3 to 1/2 of the room. The 2-minute runtime does not recover from a cold open that reads as "so what?" to a significant audience segment. The investor and leadership CTA ("come build with us") is weakened if the anchor claim did not land.
**Evidence:** Scene 1 narration: "What happens when you give an AI a blank repo and say: build your own guardrails?" -- the entire Scene 1 assumes this question feels novel. Text overlay `CLAUDE CODE BUILT ITS OWN OVERSIGHT SYSTEM` appears only in Scene 1 with no reinforcement in Scenes 2-6. No scene provides context for what Claude Code IS for viewers who don't already know.
**Dimension:** Actionability
**Mitigation:** (1) Add a single orienting line in Scene 1 or Scene 2 that briefly establishes what Claude Code is for non-developer audience segments -- e.g., "Claude Code is Anthropic's AI coding agent." One sentence is enough. (2) Reinforce the meta-angle at least once more outside Scene 1 -- Scene 5 or Scene 6 is the logical place as the "proof" section. (3) Consider whether the text overlay in Scene 1 should be more specific: `CLAUDE CODE BUILT ITS OWN OVERSIGHT SYSTEM` is accurate but "oversight system" is less visceral than "guardrails."
**Acceptance Criteria:** A non-Claude-Code-user who watches the video can accurately restate the meta-angle after viewing; the hook lands for developers AND is comprehensible to a first-time-viewer investor.

---

### IN-003-20260218: Shane McConkey Reference Unrecognizable to Tech Audience [MAJOR]

**Type:** Assumption
**Original Assumption:** Shane McConkey is a figure well-known enough to the showcase audience that the "brilliant + fun = revolution" analogy lands emotionally.
**Inversion:** McConkey is not a household name in tech culture. A significant portion of investors and Anthropic leadership have never heard of him. The analogy -- "Shane McConkey didn't revolutionize skiing by being serious" -- requires 2-3 seconds of recognition before the parallel to Jerry can land. Without recognition, the 30-second Scene 4 is spent on a reference that the audience must decode rather than feel.
**Plausibility:** High. McConkey is well-known in extreme sports and ski culture, but his name does not have mainstream tech crossover. The script assumes emotional recognition on sight of his name; for 50-70% of this specific audience, that recognition will not occur.
**Consequence:** Scene 4 (the "Soul" section, 30 seconds, 1/4 of the runtime) delivers its philosophical payload through a reference that a majority of the audience cannot emotionally engage with. The contrast the scene is designed to create -- "dead-serious engineering wrapped in personality" -- still exists visually, but the verbal analogy loses its punch.
**Evidence:** Scene 4 narration: "Shane McConkey didn't revolutionize skiing by being serious. He did it by being the best in the world -- and grinning the entire time." The narration spends 2 of its 9 sentences on McConkey specifically.
**Dimension:** Evidence Quality
**Mitigation:** (1) Add one identifying qualifier -- "ski legend Shane McConkey" or "Shane McConkey, the man who changed what skiing could be" -- to the narration. This costs 4-5 words and provides enough context for the analogy to land for non-skiers. (2) The visual direction (vintage ski footage, McConkey in onesie) can carry the characterization if the audio line provides minimal framing.
**Acceptance Criteria:** A viewer with no prior McConkey knowledge understands from the 30-second scene that he was an elite performer who combined excellence with fun; the parallel to Jerry is emotionally legible.

---

### IN-004-20260218: GitHub Repo Availability Unconfirmed [MAJOR]

**Type:** Assumption
**Original Assumption:** `github.com/geekatron/jerry` is public and accessible by Feb 21, 2026.
**Inversion:** The repo is private, not yet published, or the URL has changed. The CTA in Scene 6 -- displayed on screen with the URL for 3 seconds -- points to a page that shows "404" or "Repository not found."
**Plausibility:** Medium. The script is being written Feb 18 for an event Feb 21. OSS release timing is not confirmed in the deliverable. The project is PROJ-001-oss-release, which implies OSS release is a goal, not a confirmed fact.
**Consequence:** The final moment of the video -- the 3-second hold on the URL with "Come build with us" -- is the singular conversion mechanism for the entire 2 minutes. If the URL is dead, the entire CTA fails at the moment of highest audience attention.
**Evidence:** Scene 6: "Below it: the GitHub URL." Text overlay includes `github.com/geekatron/jerry`. No contingency if the repo is not live.
**Dimension:** Completeness
**Mitigation:** (1) Confirm repo is public before InVideo production locks in Scene 6 assets. (2) If there is any risk it will not be live by Feb 21, have a fallback URL (a landing page, a different repo, or a QR code to a teaser page). (3) Add the URL to a QR code overlay so mobile viewers can scan it directly -- this also reduces dependence on the exact URL string being memorable.
**Acceptance Criteria:** Repo URL confirmed publicly accessible before scene assets are finalized; fallback mechanism documented if publication is delayed.

---

### IN-005-20260218: InVideo AI Cold Open Visual May Not Execute [MAJOR]

**Type:** Assumption
**Original Assumption:** InVideo AI can render the "nested terminal inception" visual -- a terminal inside a terminal, code writing code -- convincingly enough to create the jaw-drop hook.
**Inversion:** InVideo AI renders generic stock footage of someone typing at a laptop, or a flat green-on-black code editor with scrolling text. The "camera pulls back to reveal the terminal is INSIDE another terminal" is not achievable through AI video generation with the specificity described. The cold open -- which carries the entire hook -- lands as visually flat.
**Plausibility:** High. Generative video AI (including InVideo) as of early 2026 is strong at cinematic sequences, facial expressions, and natural environments, but struggles with technically precise compositions like: a specific terminal emulator layout, nested UI elements, and camera movements that reveal spatial relationships within a screen. This is a highly specific technical visual that requires either: (a) actual screen recording compositing, or (b) motion graphics work beyond what InVideo AI generates autonomously.
**Consequence:** Scene 1 (0:00-0:15) is the hook. If the inception visual does not land, there is no hook. The rest of the video relies on an audience that was captured in the first 15 seconds. A visually underwhelming cold open cedes the most valuable attention window.
**Evidence:** Scene 1: "Camera pulls back to reveal the terminal is INSIDE another terminal. Code writing code. The inception moment lands." This is a very specific visual premise stated as if achievable. No acknowledgment of production complexity.
**Dimension:** Methodological Rigor
**Mitigation:** (1) Test the exact Scene 1 visual prompt in InVideo AI before committing to this production approach. (2) Prepare a screen-recorded backup: actual terminal session with tmux panes showing Claude Code writing and testing, composited with a pull-back effect in a video editor. This is achievable with real tooling. (3) If InVideo cannot execute, consider whether the cold open can be restructured around what InVideo CAN produce convincingly (cinematic shots of a terminal with typing, overlaid with statistics), while preserving the "meta" narration.
**Acceptance Criteria:** Scene 1 visual prototype reviewed and approved as "jaw-drop quality" before full production begins; fallback production method documented.

---

### IN-006-20260218: "Built Entirely by Claude Code" Claim Precision [MAJOR]

**Type:** Assumption
**Original Assumption:** The claim "Built entirely by Claude Code" is fully defensible without qualification.
**Inversion:** Any human-written configuration, prompt engineering, CLAUDE.md, `.context/rules/`, or governance document was authored by a human, which means the "entirely" claim is challenged. At a public showcase with technical audience members and subsequent media coverage, this claim is the single most scrutinized sentence in the video.
**Plausibility:** Medium. The claim is likely directionally true (Claude Code wrote the code), but "entirely" is a strong qualifier that invites scrutiny. Prompt files, rules files, CLAUDE.md -- these are typically human-authored and shape what Claude Code does. If any human authored any of these, "entirely" becomes technically inaccurate.
**Consequence:** A challenged "built entirely" claim at a public event becomes the story instead of the framework. The credibility damage extends to all other stats and claims in the video.
**Evidence:** Scene 6 narration: "Built entirely by Claude Code." No qualification about what "built" means. No context distinguishing "code" from "instructions/prompts/governance."
**Dimension:** Evidence Quality
**Mitigation:** (1) Precisely scope the claim: "Every line of code, every test, every quality gate -- written by Claude Code." This preserves the impact while being defensible if human-authored rule files are challenged. (2) Alternatively: "The code, the tests, the agents -- all Claude Code." (3) Whichever form is chosen, confirm it is factually defensible before the event.
**Acceptance Criteria:** The claim in Scene 6 is reviewed against the actual authorship record of the repository and confirmed defensible; any necessary qualifier is added to the narration.

---

### IN-007-20260218: 15-Second Context Rot Explanation Insufficient for Non-Developers [MAJOR]

**Type:** Assumption
**Original Assumption:** The Scene 2 narration ("Context fills. Rules drift. Quality rots.") and the split-screen degradation visual are sufficient to make an investor or Anthropic leadership audience feel the problem viscerally.
**Inversion:** Non-developer audience segments do not understand why a "context window filling up" is catastrophic. The visual (progress bar approaching red, code "dissolving into hallucinated garbage") is more legible, but the narration uses developer-native vocabulary without a universal translation.
**Plausibility:** High. "Context fills" is jargon. Even "hallucinated garbage" is AI-community vocabulary. The 15-second Scene 2 is calibrated for someone who has experienced a Claude Code session degrading -- not for an investor who evaluates AI companies at the business level.
**Consequence:** Investors and leadership who do not feel the problem cannot fully appreciate the solution. The entire video's persuasive arc rests on the Problem-Solution structure. If the Problem scene does not land, the Solution scene (Jerry) appears to solve a problem the audience did not feel.
**Evidence:** Scene 2 narration: "Here's the dirty secret of AI coding. The longer the session, the worse it gets. Context fills. Rules drift. Quality rots. Every developer knows this pain. Nobody had a fix." -- the phrase "every developer knows this pain" explicitly acknowledges this is developer-specific pain, but the video does not bridge this to investor/leadership concerns.
**Dimension:** Actionability
**Mitigation:** (1) Add one universalizing sentence to Scene 2 narration that translates the developer pain into business impact -- e.g., "The longer the session, the worse it gets -- bugs compound, work must be redone." This is ~10 words and connects to a consequence all audiences understand. (2) Alternatively, revise "Every developer knows this pain" to something more inclusive: "Everyone building with AI agents knows this pain."
**Acceptance Criteria:** A non-developer viewer of Scene 2 can state what the problem is in business terms (not just technical terms) after watching.

---

## Recommendations

### Critical (MUST mitigate before production)

| Finding | Action | Acceptance Criteria |
|---------|--------|---------------------|
| IN-001-20260218 | Confirm music licensing scope for all 5 named tracks; prepare royalty-free fallback for each scene's energy profile | Written license confirmation OR approved royalty-free alternatives for each scene before InVideo production begins |
| IN-002-20260218 | Add one orienting line about what Claude Code is; reinforce meta-angle in Scene 5 or 6 | Non-developer test viewer can accurately restate the meta-angle after watching |

### Major (SHOULD mitigate before Feb 21)

| Finding | Action | Acceptance Criteria |
|---------|--------|---------------------|
| IN-003-20260218 | Add "ski legend" or equivalent qualifier before Shane McConkey's name in Scene 4 narration | Analogy is legible to non-skiers without additional context |
| IN-004-20260218 | Confirm `github.com/geekatron/jerry` is public; prepare fallback URL or QR code | URL confirmed live OR fallback mechanism ready before scene assets are finalized |
| IN-005-20260218 | Test Scene 1 inception visual in InVideo; prepare screen-recorded backup if needed | Scene 1 visual prototype reviewed as "jaw-drop quality" OR fallback method ready |
| IN-006-20260218 | Scope "built entirely by Claude Code" claim to what is defensible; add specific qualifier | Claim reviewed against authorship record and confirmed factually accurate |
| IN-007-20260218 | Add one universalizing sentence to Scene 2 that translates developer pain to business impact | Non-developer viewer can state the problem in business terms after watching |

### Minor (MAY mitigate; monitor risk)

| Finding | Action | Acceptance Criteria |
|---------|--------|---------------------|
| IN-008-20260218 | No action required; monitor for tone feedback during event; have post-event response prepared if hip-hop references generate questions | Tone feedback noted; no action pre-event unless organizers flag concern |
| IN-009-20260218 | Verify test count is current as of Feb 20 evening before event; update if materially different | Stat confirmed accurate or updated within 24 hours of event |

---

## Scoring Impact

Mapping Inversion findings to S-014 scoring dimensions (weights from quality-enforcement.md SSOT):

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | IN-004-20260218: CTA depends on unconfirmed repo availability; Scene 6 close is incomplete if the URL is not live. IN-002-20260218: Meta-angle not reinforced across all scenes -- coverage is incomplete for non-developer audience. |
| Internal Consistency | 0.20 | Neutral | The script is internally consistent in its arc and energy design. IN-008-20260218 (minor) represents a tone risk but does not create internal contradiction. |
| Methodological Rigor | 0.20 | Negative | IN-001-20260218 (Critical): Using specific commercial tracks without licensing is a methodological gap -- the music arc cannot be committed as designed without license confirmation. IN-005-20260218: Cold open visual premise lacks validated production method. |
| Evidence Quality | 0.15 | Negative | IN-003-20260218: McConkey reference is an analogy without sufficient audience anchoring. IN-006-20260218: "Built entirely by Claude Code" is a strong claim that requires evidentiary support to be defensible in a public setting. |
| Actionability | 0.15 | Negative | IN-002-20260218 (Critical): Meta-angle may not convert the non-developer audience segment to action because the hook did not land for them. IN-007-20260218: Context rot explanation fails to translate to business consequences for investor/leadership segment, weakening problem-solution persuasion. |
| Traceability | 0.10 | Neutral | IN-009-20260218 (Minor): Test count stat could be stale; minor traceability risk. All other stats (33 agents, 7 skills, 10 strategies, 5 layers, 0.92) appear stable. |

**Overall Impact Assessment:** The script has strong structure and authentic energy. The failure cluster is concentrated in two areas: (1) production assumptions (music licensing, InVideo capability) that are unvalidated and could collapse key elements at the last moment, and (2) audience assumption gaps (Claude Code familiarity, McConkey recognizability, context rot translation) that reduce the script's persuasive reach across the full stated audience. Addressing the 2 Critical and 5 Major findings would materially improve the script's probability of achieving all 8 goals across all audience segments.

---

*Strategy: S-013 Inversion Technique*
*Template Version: 1.0.0*
*SSOT: `.context/rules/quality-enforcement.md`*
*Execution Date: 2026-02-18*
*Agent: adv-executor*
*Finding Prefix: IN-NNN-20260218*
