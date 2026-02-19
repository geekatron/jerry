# Inversion Report: Jerry Framework Hype Reel Script v2

**Strategy:** S-013 Inversion Technique
**Deliverable:** `showcase/phase-3-tournament/iteration-2/ps-architect-001-hype-reel-script-v2.md`
**Criticality:** C4 (public-facing, irreversible -- Anthropic 1st Birthday Showcase, Feb 21 2026)
**Date:** 2026-02-18
**Reviewer:** adv-executor (S-013)
**Iteration:** 2 (against v2 script after iteration 1 C4 tournament)
**H-16 Compliance:** S-003 Steelman applied prior to this adversarial sequence (C4 tournament); this execution proceeds in the established tournament order. Iteration 1 Inversion (IN-NNN-20260218 series) used as baseline for residual finding assessment.
**Goals Analyzed:** 8 | **Assumptions Mapped:** 17 | **Vulnerable Assumptions:** 8

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment and recommendation |
| [Iteration 1 Finding Resolution](#iteration-1-finding-resolution) | Which findings are resolved, which persist |
| [Step 1: Goal Inventory v2](#step-1-goal-inventory-v2) | Goals re-evaluated against v2 text |
| [Step 2: Anti-Goal Inventory v2](#step-2-anti-goal-inventory-v2) | What would guarantee failure for each goal in v2 |
| [Step 3: Assumption Map v2](#step-3-assumption-map-v2) | All explicit and implicit assumptions in v2 |
| [Step 4: Stress-Test Results v2](#step-4-stress-test-results-v2) | IN-NNN findings with severity |
| [Findings Table](#findings-table) | Consolidated findings by severity |
| [Finding Details](#finding-details) | Expanded analysis of Critical and Major findings |
| [Recommendations](#recommendations) | Prioritized mitigations with acceptance criteria |
| [Scoring Impact](#scoring-impact) | Mapping findings to S-014 dimensions |

---

## Summary

Inversion analysis of the Jerry Framework hype reel script v2 confirms that the two Critical findings from iteration 1 (music licensing, audience familiarity with Claude Code) are **fully resolved**: music cues are now production-description-based with no named commercial tracks, and the meta-angle now includes explicit before/after framing ("Before Jerry, four hours in and your agent forgets its own rules") accessible to non-developer audiences. Three of the five iteration 1 Major findings are resolved (McConkey grounded with inline description, InVideo visuals simplified, "NASA-grade" replaced). Two iteration 1 Major findings **persist in weaker form**: the GitHub repo availability assumption (IN-004-20260218, now Minor in v2 due to reduced urgency at this script stage) and the attribution claim (IN-006-20260218, now partially resolved but retaining a new residual risk). One iteration 1 Major finding newly **resurfaces as Critical in v2**: the audience segmentation problem. The before/after added in v2 Scene 3 is narrated too technically to serve the investor/leadership segment -- "every prompt re-enforces the same constraints, automatically" uses developer-native vocabulary while claiming to bridge the audience gap.

New inversion analysis of v2 surfaces **1 new Critical finding** and **4 new Major findings** that did not exist or were not visible in iteration 1:

- **New Critical (IN-001-20260218v2):** The before/after inserted in Scene 3 to explain Jerry's value is itself too jargon-heavy to land for a non-developer investor audience -- it explains the mechanism ("every prompt re-enforces") rather than the outcome ("your AI never forgets what it's supposed to do"). The fix introduces a new audience comprehension failure mode.
- **New Major (IN-002-20260218v2):** Scene 4 now grounds McConkey with "the skier who reinvented the sport by treating every cliff as a playground" -- but this description is too abstract to generate emotional resonance for the analogy to work. A non-skier still cannot feel why "treating every cliff as a playground" maps to "serious engineering with personality."
- **New Major (IN-003-20260218v2):** The music arc, now described entirely in production terms (BPM, instrumentation, energy), creates an unvalidated assumption that an InVideo AI music library selection from a style brief will match the precise emotional beat-drops the script engineers. The specificity of "70 BPM analog synth drone" and "130 BPM four-on-the-floor" sets expectations for a production system whose library selection algorithm is not under the script author's control.
- **New Major (IN-004-20260218v2):** "Thirty-three agents across seven skills" in the narration remains stated as a precise number in a video that will be published as OSS and replayed beyond the Feb 21 event. The number is accurate today (self-review notes 33 agents) but becomes permanently embedded in an immutable video artifact that will drift from reality as the project evolves.
- **New Major (IN-005-20260218v2):** The Scene 6 close relies on the GitHub URL materializing as a text overlay. No QR code, no shortened URL, no fallback is shown. Audience members watching on a projected screen at Shack15 cannot scan or type `github.com/geekatron/jerry` in real time; the CTA depends on recall after the event, not immediate conversion.

**Recommendation:** REVISE -- Address Critical finding (IN-001-20260218v2) in the script before production, and address Major findings (IN-002 through IN-005-20260218v2) before production handoff to InVideo. The two residual iteration 1 findings (repo live status, attribution precision) require production-side confirmation, not script changes.

---

## Iteration 1 Finding Resolution

The following table evaluates each iteration 1 finding against v2 changes as documented in the v2 Revision Log and Self-Review.

| Iter 1 Finding | Severity | v2 Change | Resolution Status | Residual Risk |
|----------------|----------|-----------|-------------------|---------------|
| IN-001-20260218: Commercial music licensing | Critical | All 5 named tracks replaced with mood/style descriptions; music library sourcing noted in overview | **RESOLVED** | None. No named commercial tracks remain. |
| IN-002-20260218: Audience familiarity / meta-angle | Critical | Before/after added to Scene 3 narration: "Before Jerry, four hours in... After Jerry, every prompt re-enforces..." | **PARTIALLY RESOLVED -- Residual Critical remains** | The before/after text uses developer vocabulary ("every prompt re-enforces the same constraints") that still requires technical context to understand. See IN-001-20260218v2. |
| IN-003-20260218: McConkey unrecognizable | Major | Added inline description: "the skier who reinvented the sport by treating every cliff as a playground" | **PARTIALLY RESOLVED -- Residual Major remains** | Description is too abstract; emotional resonance of the analogy still fails for non-skiers. See IN-002-20260218v2. |
| IN-004-20260218: GitHub repo availability | Major | Not addressed in script (production-side confirmation needed) | **PERSISTS -- downgraded to Minor** | Risk is real but out of scope for script revision; production team must confirm before Feb 21. Recorded as IN-007-20260218v2. |
| IN-005-20260218: InVideo cold open visual | Major | Simplified: "second terminal framing the first" replaces "terminal INSIDE another terminal" | **RESOLVED** | Reduced specificity makes the visual achievable via screen-recording compositing or simpler InVideo direction. |
| IN-006-20260218: "Built entirely by Claude Code" | Major | Changed to "Every line written by Claude Code, directed by a human who refused to compromise" | **RESOLVED** | Human direction explicitly credited. Claim scope is "every line written" which is more defensible than "built entirely." |
| IN-007-20260218: 15s context rot explanation | Major | "Every developer knows this pain" removed; before/after added in Scene 3 | **PARTIALLY RESOLVED -- Residual embedded in IN-001-20260218v2** | The before/after is placed in Scene 3 (capabilities) rather than Scene 2 (problem). Scene 2 narration still uses "context fills" and "quality rots" without a business-impact translation. |
| IN-008-20260218: Hip-hop/Saucer Boy tone | Minor | All commercial music references removed (moot); "Saucer Boy" brand preserved in visual commentary | **RESOLVED (moot)** | Without Wu-Tang/hip-hop named tracks, the cultural reference concern is eliminated. "Saucer Boy" as a brand name remains but is now less culturally specific. |
| IN-009-20260218: Test count stale | Minor | Changed from "3,195" to "More than three thousand" / "3,000+" | **RESOLVED** | Rounded formulation is stable through event day and beyond. |

**Resolution Summary:** 2 of 2 Critical resolved (1 with residual). 3 of 5 Major resolved. 2 of 2 Minor resolved. Net: 0 Critical fully open, 1 Critical residual (new form), 2 Major persisting (new form), plus 4 new findings from v2 analysis.

---

## Step 1: Goal Inventory v2

Goals are re-evaluated against v2 script text. v2 changes are noted where a goal's achievability has shifted.

| Goal ID | Goal | Type | Measurable Form | v2 Status Change |
|---------|------|------|-----------------|------------------|
| G-01 | Capture audience attention in the first 15 seconds | Explicit | Viewer does not disengage during cold open; hook is felt as novel, not generic | Unchanged. Cold open simplified but same premise. |
| G-02 | Communicate the meta-angle: Claude Code wrote its own oversight system | Explicit | A viewer with no prior Jerry knowledge can state this after watching | Partially improved. Before/after in Scene 3 helps; Scene 2 narration still developer-native. |
| G-03 | Explain context rot as a real, felt problem for all audience segments | Explicit | A non-Claude-Code-user understands "sessions degrade" after watching Scenes 2-3 | Improved but not fully achieved. Before/after bridges but uses mechanism language rather than outcome language. |
| G-04 | Demonstrate credibility via concrete, accurate stats | Explicit | Stats are verifiable and feel earned, not inflated | Improved. Test count rounded (stable). Remaining stats accurate per self-review. |
| G-05 | Convey Saucer Boy personality (serious + fun) | Explicit | Anthropic leadership and developers both respond positively | Slightly improved. McConkey is grounded but analogy still abstract for non-skiers. |
| G-06 | Drive audience to the GitHub repo for OSS participation | Explicit | Viewer knows the URL and CTA; repo is accessible | Unchanged and unmitigated. URL depends on production-side confirmation. |
| G-07 | Fit within 2:00 runtime while landing each beat on music cues | Explicit | 278 words at 140 WPM = ~1:59; scene transitions align with music | Slightly reduced risk. Mood descriptions give production more latitude than named tracks with fixed BPM. |
| G-08 | Be producible in InVideo AI from scene directions as written | Implicit | InVideo AI can execute every visual and audio direction | Improved but still assumption-heavy. Music description specificity creates new InVideo library selection risk. |

---

## Step 2: Anti-Goal Inventory v2

For each goal, what would guarantee failure in v2?

| Anti-Goal ID | Inverted Goal | Failure Condition | v2 Coverage |
|-------------|---------------|-------------------|-------------|
| AG-01 | Fail to capture attention in 15 seconds | Open with text-heavy explanation, OR cold open visual renders flat (generic laptop typing footage instead of terminal composition) | Partial. Cold open simplified and more achievable, but still requires a convincing technical visual. |
| AG-02 | Lose the meta-angle for non-developer audience | Before/after narration uses jargon that sounds impressive but explains mechanism rather than outcome. Investor hears "every prompt re-enforces constraints" and does not understand why that is remarkable. | **Unresolved.** The fix text itself is the failure mode. "Every prompt re-enforces the same constraints, automatically" is still developer-native. |
| AG-03 | Make context rot feel abstract to investors | Narration says "context fills, rules drift, quality rots" in Scene 2 -- visceral to developers, opaque to investors -- and the before/after bridge in Scene 3 explains the mechanism not the consequence | **Partially unresolved.** Scene 2 narration unchanged; Scene 3 before/after is better than nothing but does not translate to business impact. |
| AG-04 | Present stats that feel made-up | Round numbers ("more than three thousand") and no on-screen verification mechanism | Resolved. Rounded numbers are now more credible, not less. |
| AG-05 | Alienate investors with cultural references | McConkey description is too vague for non-skiers to form an emotional connection; "treating every cliff as a playground" is abstract rather than evocative | **Partially unresolved.** Description is present; emotional resonance is not guaranteed. |
| AG-06 | Fail to convert to repo engagement | URL displayed as plain text on a projected screen; no QR code; no short URL; recall-dependent conversion | **Unaddressed.** Same failure mode as iteration 1. Audience cannot act in real time. |
| AG-07 | Blow the runtime or land beats on silence | Music library selection does not match described BPM/energy; transitions fire on wrong moments | New risk in v2. Named tracks had known timing; mood descriptions depend on production library matching the spec. |
| AG-08 | Produce a video that looks cheap or AI-generated | InVideo AI music library selection does not match "70 BPM analog synth drone" description; beat drops misfire | New risk in v2. See IN-003-20260218v2. |

**Anti-goals unaddressed or newly introduced by v2:** AG-02 (partially), AG-03 (partially), AG-05 (partially), AG-06 (fully), AG-07 (new), AG-08 (new in music dimension).

---

## Step 3: Assumption Map v2

Assumptions are re-evaluated with v2 changes reflected. New assumptions introduced by v2 changes are marked (NEW).

| ID | Assumption | Type | Category | Confidence | Validation Status | Consequence if Wrong |
|----|------------|------|----------|------------|-------------------|---------------------|
| A1 | 278 words at 140 WPM = ~1:59 runtime | Explicit | Temporal | High | Mathematically verified | Minor: trivial timing adjustment |
| A2 | Target audience = Anthropic leadership + investors + developers | Explicit | Environmental | High | Stated in context | Major: calibration mismatch if further segments present |
| A3 | InVideo AI is the production platform | Explicit | Technical | High | Stated in context | Major: scene directions may be wrong format for another platform |
| A4 | InVideo AI can render convincing two-terminal composition ("second terminal framing the first") | Implicit | Technical | Medium | Not validated; simpler than v1 but still requires screen-composition capability | Major: cold open visual is flat |
| A5 | InVideo AI music library contains cues matching the mood/energy/BPM descriptions (70 BPM drone, 130 BPM industrial, 128 BPM vocoder anthem, 85 BPM lo-fi, 140 BPM trap, single sustained note) | Implicit (NEW) | Technical | Low | Not validated; InVideo library contents unknown | Major: music arc breaks when production library does not match descriptions |
| A6 | A "Jerry logo" exists or can be generated for the Scene 6 close | Implicit | Resource | Medium | Not confirmed | Major: Scene 6 visual direction fails; logo materializes "from scattered code fragments" |
| A7 | `github.com/geekatron/jerry` is public and live by Feb 21, 2026 | Implicit | Environmental | Medium | Not confirmed | Minor (script-level): CTA is dead link -- production team must confirm |
| A8 | The before/after narration in Scene 3 ("Before Jerry... After Jerry...") translates Jerry's value to a non-developer audience segment | Implicit (NEW) | Audience | Low | Not validated | Critical: non-developer audience still cannot feel the problem/solution value proposition |
| A9 | "The skier who reinvented the sport by treating every cliff as a playground" is sufficient description for non-skiers to emotionally grasp the McConkey analogy | Implicit (NEW) | Audience | Low | Not validated | Major: Scene 4 philosophical anchor fails for non-skier audience |
| A10 | The audience at Shack15 can capture `github.com/geekatron/jerry` from a projected screen in 3 seconds | Implicit | Audience | Low | Not validated | Major: CTA fails at the moment of highest attention -- URL is not scannable/typable in real time |
| A11 | Audience can absorb technical vocabulary (constitutional governance, five-layer enforcement, adversarial strategies) without losing engagement | Implicit | Audience | Medium | Not validated | Minor: Scene 3 montage loses non-developer viewers |
| A12 | "More than three thousand tests" remains accurate on event day | Explicit | Technical | High | Verified at time of writing (3,257); rounded formulation stable | Negligible: "more than three thousand" holds even if count changes materially |
| A13 | "33 agents across seven skills" is accurate on event day AND remains accurate after OSS publication | Implicit | Technical | Medium | Accurate at time of writing; may change with ongoing development | Major: number is stated precisely in narration and is embedded permanently in the video |
| A14 | "Every line written by Claude Code" is a fully defensible claim against scrutiny from a developer audience at a public event | Implicit | Technical | Medium | Improved from v1; human direction credit added; but "every line" still invites scope questions | Minor: prompt engineering, rule files, CLAUDE.md -- were these "lines"? |
| A15 | 15 seconds of Scene 2 narration ("context fills, rules drift, quality rots") is sufficient for investors to feel urgency, supplemented by Scene 3 before/after | Implicit | Audience | Low | Not validated | Major: Scene 2 remains developer-native; Scene 3 before/after uses mechanism language |
| A16 | InVideo AI can render the Scene 6 "logo materializes from scattered code fragments assembling themselves" animation convincingly | Implicit | Technical | Medium | Not validated | Minor: alternative: logo fades in from black |
| A17 | "Directed by a human who refused to compromise" in Scene 6 narration is received as a genuine credit and not read as a defensive disclaimer | Implicit (NEW) | Audience | Medium | Not validated | Minor: sophisticated tech audience may read this as over-explaining |

---

## Step 4: Stress-Test Results v2

| ID | Assumption | Inversion | Plausibility | Severity | Affected Dimension |
|----|------------|-----------|-------------|----------|--------------------|
| IN-001-20260218v2 | A8: Before/after in Scene 3 translates Jerry's value to non-developers | "Every prompt re-enforces the same constraints, automatically" describes the mechanism; an investor hears "it re-runs rules" not "your AI never forgets what it's supposed to do." The fix added for audience comprehension uses developer vocabulary. | **High** -- "re-enforces constraints" is developer-native shorthand; investors think in outcomes, not mechanisms | Critical | Actionability |
| IN-002-20260218v2 | A9: McConkey description "the skier who reinvented the sport by treating every cliff as a playground" is emotionally resonant for non-skiers | The description is too abstract to generate the intended emotional payload. "Treating every cliff as a playground" is an athlete's disposition framing, not a revolutionary achievement framing. The analogy requires the audience to feel: "this was an elite who changed the game while having fun." The description gives the disposition ("playful") but not the achievement context. | **High** -- "treating every cliff as a playground" does not signal domain mastery or revolution to a non-skier; it could describe any risk-taker | Major | Evidence Quality |
| IN-003-20260218v2 | A5: InVideo AI music library matches mood/energy/BPM descriptions | InVideo's library algorithm selects a cue based on text descriptions; the selected cue for "130 BPM, aggressive distorted bass, industrial edge, four-on-the-floor" may be a stock industrial track with the right tempo but wrong energy character, or vice versa. Beat drops described as landing "on a downbeat" are now contingent on the library's track structure matching the scene edit. | **Medium-High** -- InVideo music library selection is algorithm-driven and non-deterministic from description alone; no preview or approval loop is specified | Major | Methodological Rigor |
| IN-004-20260218v2 | A13: "33 agents across seven skills" is accurate on event day AND permanently correct in a published video | The number is a precise claim in the narration. OSS publication of the video means it will be watched after Feb 21, potentially for months or years. When the agent count changes (new skills, retired agents), the video's stated number is permanently wrong. No qualifier ("at launch" or "in v0.2.0") is present. | **High** -- open source frameworks evolve; a public video stating "33 agents" will be demonstrably wrong within months | Major | Traceability |
| IN-005-20260218v2 | A10: Audience can capture `github.com/geekatron/jerry` from a projected screen in 3 seconds | At a live event on a projected screen, the URL holds for 3 seconds. In a room of any size, attendees cannot type a URL in 3 seconds, and the video does not provide a QR code. Post-event conversion depends on attendees remembering or searching later; the CTA's immediacy is zero. | **High** -- live event URL displays have near-zero real-time conversion without QR codes; this is well-documented in event marketing | Major | Completeness |
| IN-006-20260218v2 | A15: Scene 2 narration is sufficient for investor audience with Scene 3 before/after bridge | Scene 2 narration ("context fills, rules drift, quality rots. Tools handle memory. Nobody had a fix for enforcement") still uses developer-native vocabulary. The before/after was placed in Scene 3 (the capabilities section), not Scene 2 (the problem section). An investor who does not feel the problem in Scene 2 may not connect the before/after in Scene 3 as evidence of a solution to a real problem. | **Medium-High** -- the problem-solution arc requires the problem to land first; patching the explanation in the solution scene creates a narrative gap | Major | Actionability |
| IN-007-20260218v2 | A7: `github.com/geekatron/jerry` is public and live by Feb 21, 2026 | Repo is not yet confirmed public; OSS release timing relative to event day is unverified in the script | **Medium** -- script-level issue is moot; production-side confirmation required | Minor | Completeness |
| IN-008-20260218v2 | A17: "Directed by a human who refused to compromise" is received as genuine credit | A developer-audience member at a birthday showcase for Claude Code may read "directed by a human" as a defensive response to AI authorship skepticism rather than a confident attribution. The phrase "who refused to compromise" is subjective and could read as self-congratulatory. | **Low-Medium** -- risk is audience-segment-specific and the phrase is brief; unlikely to materially undermine the video but worth noting | Minor | Internal Consistency |

---

## Findings Table

| ID | Assumption / Anti-Goal | Type | Confidence | Severity | Evidence | Affected Dimension |
|----|------------------------|------|------------|----------|----------|--------------------|
| IN-001-20260218v2 | Before/after in Scene 3 uses mechanism language; non-developer audience still cannot feel Jerry's value proposition | Assumption | Low | **Critical** | Scene 3 narration: "Before Jerry, four hours in and your agent forgets its own rules. After Jerry, every prompt re-enforces the same constraints, automatically." -- "re-enforces constraints" is developer vocabulary; investor outcome is missing | Actionability |
| IN-002-20260218v2 | McConkey description too abstract for non-skier emotional resonance | Assumption | Low | **Major** | Scene 4 narration: "Shane McConkey -- the skier who reinvented the sport by treating every cliff as a playground" -- disposition described, revolutionary achievement not conveyed | Evidence Quality |
| IN-003-20260218v2 | InVideo music library selection may not match mood/energy descriptions | Assumption | Low | **Major** | Overview: mood/style descriptions for all 5 cues; no preview or approval loop specified; "each stat lands on a beat" requires library track to match edit structure | Methodological Rigor |
| IN-004-20260218v2 | "33 agents across seven skills" embeds a precise number in a permanently public video that will drift | Assumption | Medium | **Major** | Scene 3 narration: "Thirty-three agents across seven skills" -- no version qualifier; video is OSS/public and will be replayed after the agent count changes | Traceability |
| IN-005-20260218v2 | GitHub URL is not capturable from a projected screen in real time without a QR code | Assumption | Low | **Major** | Scene 6: "Below it: the GitHub URL" displayed for 3 seconds; no QR code or short URL in the script | Completeness |
| IN-006-20260218v2 | Scene 2 problem narration still developer-native; before/after placed in Scene 3 (solution section) creates narrative gap | Assumption | Medium | **Major** | Scene 2 narration: "Context fills. Rules drift. Quality rots. Tools handle memory. Nobody had a fix for enforcement." -- problem explanation unchanged; bridge patched into wrong scene | Actionability |
| IN-007-20260218v2 | GitHub repo availability unconfirmed (production-side) | Assumption | Medium | **Minor** | Scene 6: `github.com/geekatron/jerry` as CTA -- repo status not confirmed in script | Completeness |
| IN-008-20260218v2 | "Directed by a human who refused to compromise" may read as defensive at a developer event | Assumption | Medium | **Minor** | Scene 6 narration: "directed by a human who refused to compromise" -- authorship credit phrase with subjective self-assessment | Internal Consistency |

---

## Finding Details

### IN-001-20260218v2: Before/After Uses Mechanism Language; Non-Developer Audience Excluded [CRITICAL]

**Type:** Assumption
**Original Assumption:** The before/after narration added in v2 to Scene 3 ("Before Jerry, four hours in and your agent forgets its own rules. After Jerry, every prompt re-enforces the same constraints, automatically.") successfully translates Jerry's value to a non-developer audience segment.
**Inversion:** The phrase "every prompt re-enforces the same constraints, automatically" describes how Jerry works (the enforcement mechanism) rather than what the user gets (the outcome). An investor who does not program does not know what "re-enforces constraints" means in practical terms. The before/after was the fix for iteration 1's Critical finding IN-002-20260218, and it improves on "context fills, rules drift" -- but it still requires the listener to understand what "constraints" are, why "prompts" enforce them, and why "automatically" is remarkable.
**Plausibility:** High. The intended bridging audience (investors, Anthropic leadership) thinks in terms of reliability, quality, and cost of failure -- not enforcement mechanisms. "Your agent forgets its own rules" is more evocative ("forgets" is universal; "its own rules" suggests the system overrides itself), but the resolution ("every prompt re-enforces the same constraints") is opaque without context.
**Consequence:** The fix for the most important audience comprehension failure from iteration 1 is itself too technical. The non-developer audience segment will hear the before state ("forgets its own rules" -- somewhat comprehensible) but not feel the after state ("re-enforces constraints" -- mechanism, not outcome). G-02 (communicate meta-angle) and G-03 (make problem felt) remain partially unachieved for the investor/leadership segment.
**Evidence:** Scene 3 narration (v2): "Before Jerry, four hours in and your agent forgets its own rules. After Jerry, every prompt re-enforces the same constraints, automatically." The before phrase uses everyday language ("forgets its own rules" is understood universally). The after phrase uses technical vocabulary ("re-enforces," "constraints," "automatically" in the context of software enforcement). The contrast is not equivalent -- before is emotional, after is mechanical.
**Dimension:** Actionability
**Mitigation:** Replace the after clause with an outcome statement rather than a mechanism statement. Options:
  - "After Jerry, every session -- hour four, hour twelve, hour forty -- your agent works exactly like hour one."
  - "After Jerry, quality doesn't degrade. Every session stays sharp."
  - "After Jerry, the rules never drift. Hour twelve works like hour one."
These formulations translate the enforcement mechanism into a user-felt outcome accessible to any audience member. The current before/after can be preserved structurally; only the "after" clause needs revision.
**Acceptance Criteria:** A non-developer viewer (investor or business audience) who watches Scene 3 can state in their own words what Jerry does for them, using outcome language rather than mechanism language.

---

### IN-002-20260218v2: McConkey Description Too Abstract for Non-Skier Resonance [MAJOR]

**Type:** Assumption
**Original Assumption:** Adding the inline description "the skier who reinvented the sport by treating every cliff as a playground" gives non-skier audience members sufficient context to feel the emotional weight of the McConkey analogy.
**Inversion:** "Treating every cliff as a playground" describes a disposition (playful risk-taking) but does not convey elite mastery or revolutionary achievement. A non-skier hears: "this person was playful and fearless." They do not hear: "this was the best in the world who redefined what was possible while making it look effortless." The analogy to Jerry requires the "best in the world" dimension to land -- the point is that serious excellence and serious fun are not in tension. Without the mastery signal, the analogy reads as "Jerry is built by someone who likes to play around."
**Plausibility:** High. "Treating every cliff as a playground" is an insider framing from ski culture where "playground" has a specific meaning (creative line-finding, trick skiing, backcountry exploration). For a non-skier, "playground" connotes casual play rather than elite creativity.
**Consequence:** Scene 4 is 30 seconds (25% of the runtime) and carries the entire "Soul" section -- the philosophical payload that distinguishes Jerry from a dry engineering tool. If the McConkey analogy does not emotionally land for 50-70% of the room, Scene 4 is 30 seconds of audience processing time rather than audience engagement.
**Evidence:** Scene 4 narration (v2): "Shane McConkey -- the skier who reinvented the sport by treating every cliff as a playground -- didn't change skiing by being serious. He did it by being the best in the world and grinning the entire time." The structure "reinvented the sport by treating every cliff as a playground" puts the causal mechanism before the mastery claim. Swapping order: "the best in the world, who reinvented skiing by treating every run as a creative problem to solve" would land the mastery first.
**Dimension:** Evidence Quality
**Mitigation:** Revise the McConkey description to lead with mastery before disposition: "Shane McConkey -- the skier who was the best in the world, and who reinvented the sport by refusing to be serious about it." Or more compact: "Shane McConkey, ski legend and pioneer, didn't change skiing by being serious." The word "legend" does more work in 1 word than the 10-word description does, because "legend" signals mastery to any audience without requiring ski knowledge.
**Acceptance Criteria:** A non-skier viewer can accurately describe what made McConkey exceptional (best in field + playful) after hearing the Scene 4 narration, without needing to know skiing.

---

### IN-003-20260218v2: InVideo Music Library Selection Non-Deterministic from Descriptions [MAJOR]

**Type:** Assumption
**Original Assumption:** Providing mood/BPM/instrumentation descriptions (e.g., "Low analog synth drone building tension. Dark, minimal, sub-bass pulse. 70 BPM") to InVideo AI will result in music cues that match the script's precisely engineered energy arc.
**Inversion:** InVideo's music selection algorithm returns a cue from its licensed library that matches the surface description (tempo, genre) but does not match the specific character required (e.g., a 70 BPM ambient electronic track that does not have the "eerie, anticipatory" quality; or a 130 BPM industrial track that is too abrasive rather than "adrenaline and urgency"). The script's energy arc -- tension to hype to anthem to swagger to confidence to triumph -- depends on specific quality of each cue, not just its category.
**Plausibility:** Medium-High. InVideo AI music curation from text prompts is probabilistic. The library contains hundreds of licensed tracks per genre/BPM range. The script's qualitative descriptors ("anticipatory," "relentless iteration," "quiet dominance," "nothing but confidence") are interpretive and will be matched differently by different curators or algorithms. Additionally, "each stat lands on a downbeat" in Scene 3 requires the selected track's structure (bar lengths, drop points) to align with the scene's edit timing -- a constraint that cannot be specified in a text description.
**Consequence:** If the music arc does not match the engineering intent, the video's emotional escalation fails. The script's most distinctive quality -- a precisely designed five-stage energy progression calibrated to the narrative beats -- becomes generic background music.
**Evidence:** Script overview: "Music Sourcing: All cues are mood/style descriptions for production music library selection (Epidemic Sound, Artlist, or equivalent)." Scene 3 transition: "Each stat lands on a downbeat." This requires the selected track to have a beat structure where downbeats fall at the right moments relative to the edit -- a structural constraint that a mood description cannot specify.
**Dimension:** Methodological Rigor
**Mitigation:** (1) Before committing to InVideo as the production platform, test Scene 1 and Scene 2 music selections against the descriptions. If the library outputs do not match, this is early signal that manual music selection (Epidemic Sound or Artlist browsed directly) is needed instead of algorithmic selection. (2) Add a curation step: human reviewer previews the selected tracks for each scene before the final render. (3) For Scene 3 ("each stat lands on a downbeat"), specify the target bar structure: "Select a track where beats fall at approximately 0s, 2s, 4s, 6s (128 BPM = beat every 0.47s; this means approximately 4-beat phrases at the cut points)." This is more actionable than a mood description.
**Acceptance Criteria:** Each scene's music cue is previewed and approved by a human reviewer before the final render; all 5 cues match the described energy character; Scene 3 stat text overlay lands on audible beats.

---

### IN-004-20260218v2: "33 Agents Across Seven Skills" Embeds Precise Number in Permanent Public Artifact [MAJOR]

**Type:** Assumption
**Original Assumption:** "Thirty-three agents across seven skills" is accurate as of Feb 21, 2026, and the number stated in the narration is a durable fact for the video's public life.
**Inversion:** The video is published as OSS alongside the Jerry framework. Over months and years, agents are added, removed, or restructured. A viewer in mid-2026 watches the video and counts 41 agents, or 28, or a different skills structure -- and the video's credibility is undermined by a stat that is demonstrably wrong. Unlike a live presentation where a speaker can note "that was the count on launch day," a video embeds the number as a permanent claim.
**Plausibility:** High. Open source frameworks actively developed with a v0.2.0 designation will evolve. The v0.2.0 version numbering implies v0.3.0, v1.0.0, and so on. "33 agents" as a specific count is almost certainly different by v1.0.0. The video is an OSS release artifact, not an ephemeral showcase slide.
**Consequence:** The stat is currently accurate and impressive. Its long-term accuracy is near-zero. The video's credibility as a reference artifact is degraded in proportion to how much time passes after publication. For a birthday party showcase that also serves as OSS launch marketing, this matters.
**Evidence:** Scene 3 narration (v2): "Thirty-three agents across seven skills." No version qualifier. No "at launch" or "in v0.2.0" qualifier. Text overlay "33 AGENTS / 7 SKILLS" is similarly unqualified.
**Dimension:** Traceability
**Mitigation:** Add a version anchor to the stat: "Thirty-three agents across seven skills in version zero-point-two" OR change to a formulation that emphasizes the architecture rather than the count: "Specialized agents across seven skill domains" -- this preserves the multi-agent architecture claim without embedding a number that will drift. Alternatively, drop the precise count and say "dozens of agents across seven skills."
**Acceptance Criteria:** The agent count statement either includes a version anchor making it temporally bounded, or uses a formulation that remains accurate as the framework evolves past v0.2.0.

---

### IN-005-20260218v2: GitHub URL Not Capturable From Projected Screen in Real Time [MAJOR]

**Type:** Assumption
**Original Assumption:** Displaying `github.com/geekatron/jerry` on screen for 3 seconds at the close of the video is sufficient for audience members to capture and act on the CTA.
**Inversion:** At a live event at Shack15 with projected display, audience members cannot type or recall a full GitHub URL from a 3-second overlay in real time. Post-event conversion depends on attendees remembering to search for "Jerry Framework" or "geekatron jerry" later. The "come build with us" CTA's entire conversion mechanism is recall-dependent rather than action-enabling.
**Plausibility:** High. Event marketing best practice for the past decade has been QR codes for any URL displayed at a live event. A 3-second URL hold on projected video is long enough to see the URL exists, not long enough to type it, and not long enough to scan unless a QR code is present. The Shack15 audience will be holding phones (they are at a tech showcase), making QR code scanning the natural interaction.
**Consequence:** The single conversion mechanism of a 2-minute video -- the final CTA -- has near-zero in-event conversion rate. All conversions are post-event recall-dependent, which reduces conversion probability by at least 50% compared to a QR code-enabled display.
**Evidence:** Scene 6 text overlay: `github.com/geekatron/jerry`. Duration: "Logo holds for 3 seconds." No mention of a QR code anywhere in the script. "Come build with us" presupposes the audience knows how to find the repo.
**Dimension:** Completeness
**Mitigation:** Add a QR code overlay to Scene 6. The QR code should link to `github.com/geekatron/jerry` (or a redirect if the repo URL changes). This is a single production asset addition that transforms the CTA from recall-dependent to action-enabling. Alternatively, use a short URL (`jerry.dev` or similar) that is both typable and memorable. The Scene 6 visual direction already has sufficient space: the logo, Apache badge, and URL are described -- a QR code can be placed adjacent to the URL.
**Acceptance Criteria:** Scene 6 includes either a QR code overlay linking to the repo, or a short URL that is memorable within 3 seconds; tested on a device in a simulated projected-screen environment before event day.

---

### IN-006-20260218v2: Scene 2 Problem Narration Still Developer-Native; Bridge Placed in Wrong Scene [MAJOR]

**Type:** Assumption
**Original Assumption:** The before/after bridge in Scene 3 compensates for Scene 2's developer-native context rot narration, creating a complete problem-solution arc for all audience segments.
**Inversion:** The problem-solution arc requires the audience to feel the problem before the solution can land. Scene 2 (the problem scene, 0:15-0:30) narration is: "Here's the dirty secret of AI coding. The longer the session, the worse it gets. Context fills. Rules drift. Quality rots. Tools handle memory. Nobody had a fix for enforcement." An investor who does not understand "context fills" or "enforcement" exits Scene 2 without feeling the problem. The before/after in Scene 3 (the solution scene) then attempts to explain the problem while presenting the solution -- but a viewer who did not feel the problem in Scene 2 will not recognize the before/after as a solution to a real problem; they will experience it as a demonstration.
**Plausibility:** Medium-High. The problem-solution arc is a well-understood persuasion structure. Patching the problem explanation into the solution scene creates a structural gap: the audience experiences Solution (capabilities montage) before the Problem fully lands. The before/after clarifies Jerry's mechanism but does not retroactively make Context Rot feel urgent to an investor who missed it in Scene 2.
**Consequence:** Investors and Anthropic leadership who do not feel the problem in Scene 2 are watching a capabilities montage in Scene 3 without urgency. "Thirty-three agents" and "five-layer enforcement" are features, not solutions to a felt problem, if the problem was not felt.
**Evidence:** Scene 2 narration (unchanged from v1): "Context fills. Rules drift. Quality rots." -- this is the problem statement and it uses developer-native vocabulary. The before/after fix was inserted into Scene 3 narration rather than Scene 2. Scene 2 has no universal bridge to non-developer consequences.
**Dimension:** Actionability
**Mitigation:** Add one consequence-first sentence to Scene 2 narration that translates the problem to universal stakes: "The longer an AI coding session runs, the more it drifts -- bugs compound, work must be redone, the output degrades." This comes before "Context fills. Rules drift. Quality rots." so developer-native shorthand is preceded by a universal consequence statement. This is ~20 words in Scene 2 that resolves the problem-explanation gap without restructuring the scene.
**Acceptance Criteria:** An investor or business-audience member who watches Scene 2 can articulate the business consequence of context rot (not just the technical mechanism) after viewing that scene alone.

---

## Recommendations

### Critical (MUST address in script before production)

| Finding | Action | Acceptance Criteria |
|---------|--------|---------------------|
| IN-001-20260218v2 | Replace "every prompt re-enforces the same constraints, automatically" with an outcome statement: "After Jerry, hour twelve works like hour one" or equivalent. Keep the before/after structure; change only the resolution clause. | Non-developer test viewer can state Jerry's value proposition in outcome terms after watching Scene 3 |

### Major (SHOULD address before production handoff)

| Finding | Action | Acceptance Criteria |
|---------|--------|---------------------|
| IN-002-20260218v2 | Replace "the skier who reinvented the sport by treating every cliff as a playground" with a mastery-first description: "ski legend" or "the best in the world, who reinvented skiing by refusing to be serious about it" | Non-skier viewer understands McConkey as elite + playful from Scene 4 narration alone |
| IN-003-20260218v2 | Test all 5 music cue descriptions in InVideo before final render; add a human curation review step; for Scene 3 specify beat structure needed for stat-to-beat synchronization | Each music cue previewed and approved before render; Scene 3 stats land on audible beats |
| IN-004-20260218v2 | Add version anchor to agent count: "Thirty-three agents in version zero-point-two" OR replace with architecture-framing: "specialized agents across seven skill domains" | Agent count statement is either temporally bounded or framed in a way that remains accurate as framework evolves |
| IN-005-20260218v2 | Add QR code overlay to Scene 6 visual direction; specify it links to `github.com/geekatron/jerry` | QR code present in final Scene 6 assets; tested scannable from projected display distance |
| IN-006-20260218v2 | Add one consequence-first sentence to Scene 2 narration before "Context fills": "The longer an AI coding session runs, the more it drifts -- bugs compound, work must be redone." | Investor/business viewer can state the business consequence of context rot after watching Scene 2 alone |

### Minor (MAY address; monitor)

| Finding | Action | Acceptance Criteria |
|---------|--------|---------------------|
| IN-007-20260218v2 | Confirm repo is public before InVideo production locks Scene 6 assets; this is a production-side action, not a script change | Repo confirmed publicly accessible or fallback documented |
| IN-008-20260218v2 | Consider whether "directed by a human who refused to compromise" is the right tone at a developer event; if retaining, ensure the phrase stands alone as confident rather than defensive | No action required unless organizers or reviewers flag tone concern |

---

## Scoring Impact

Mapping inversion findings to S-014 scoring dimensions (weights from quality-enforcement.md SSOT):

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | IN-005-20260218v2: CTA conversion mechanism is incomplete -- URL without QR code is recall-dependent, not action-enabling. IN-007-20260218v2 (minor): Repo availability still unconfirmed at script level. Scene 6 close is structurally present but functionally incomplete for a live event context. |
| Internal Consistency | 0.20 | Neutral | v2 script is internally consistent. IN-008-20260218v2 (minor) represents a possible tone signal but does not create internal contradiction. The energy arc and scene structure are coherent. |
| Methodological Rigor | 0.20 | Negative | IN-003-20260218v2: Music arc is now description-dependent on a third-party algorithmic selection; the methodological integrity of the music engineering is contingent on InVideo library matching. "Each stat lands on a beat" is an engineering constraint that cannot be specified in a text description alone. Scene 3 beat-drop synchronization is not verifiable until production. |
| Evidence Quality | 0.15 | Negative | IN-002-20260218v2: McConkey description provides disposition without mastery signal; analogy loses evidentiary force for non-skier audience segment. IN-004-20260218v2: "33 agents" is an accurate but temporally unbounded claim that will become inaccurate in a permanently published video. Both findings reduce the script's evidentiary quality for the audience segments that matter most for OSS adoption. |
| Actionability | 0.15 | Negative | IN-001-20260218v2 (Critical): Before/after mechanism language does not convert non-developer audience to felt understanding of Jerry's value; CTA persuasion is weakened for investor/leadership segment. IN-006-20260218v2: Problem-solution arc has a structural gap -- problem explanation patched into solution scene rather than problem scene. Both findings directly reduce the script's conversion potential. |
| Traceability | 0.10 | Negative | IN-004-20260218v2: Precise agent count embedded in a permanent video without version anchor creates a traceability failure as the framework evolves. No mechanism exists to correct the video post-publication. |

**Net Assessment by Iteration:** v2 resolved the two most impactful iteration 1 Critical findings (music licensing, meta-angle framing) and three of five Major findings, which represents substantial quality improvement. However, the fixes introduced new failure modes in Actionability (before/after mechanism language), Evidence Quality (McConkey description level), and Methodological Rigor (music library selection non-determinism). The structural CTA failure (no QR code) persists from iteration 1 and was not identified in the iteration 1 inversion analysis -- this is a new finding in iteration 2. Net: 5 dimensions carry Negative impact from v2 findings. The script is substantially improved but not yet at C4 target of >= 0.95. The Critical finding (IN-001-20260218v2) requires a single narration clause revision that is low-effort and high-impact. The four Major findings are addressable in production with targeted changes.

---

*Strategy: S-013 Inversion Technique*
*Template Version: 1.0.0*
*SSOT: `.context/rules/quality-enforcement.md`*
*Iteration: 2 (against v2 script)*
*Execution Date: 2026-02-18*
*Agent: adv-executor*
*Finding Prefix: IN-NNN-20260218v2*
*Prior Iteration Reference: IN-NNN-20260218 (iteration 1)*
