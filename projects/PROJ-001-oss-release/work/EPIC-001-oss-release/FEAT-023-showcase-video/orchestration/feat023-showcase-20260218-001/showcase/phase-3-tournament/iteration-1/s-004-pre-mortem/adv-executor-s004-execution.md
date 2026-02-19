# Pre-Mortem Report: Jerry Framework Hype Reel Script

**Strategy:** S-004 Pre-Mortem Analysis
**Deliverable:** `ps-architect-001-hype-reel-script.md` -- Jerry Framework 2:00 Hype Reel
**Criticality:** C4
**Date:** 2026-02-18
**Reviewer:** adv-executor (S-004 specialist)
**H-16 Compliance:** S-003 Steelman applied (confirmed -- `adv-executor-001-s003-steelman.md` exists in iteration-1)
**Failure Scenario:** It is August 2026. The showcase at Shack15 happened on February 21. The Jerry hype reel played to the room. The room went quiet -- not in awe, in confusion. Three Anthropic leaders checked their phones. The repo received 12 stars over the following week. Developers who watched it could not describe what Jerry actually does. The video was quietly removed from the event recap.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall risk posture and recommendation |
| [Failure Scenario Declaration](#failure-scenario-declaration) | Temporal perspective shift and failure framing |
| [Findings Table](#findings-table) | All failure causes with likelihood/severity/priority |
| [Finding Details](#finding-details) | Expanded analysis for each Critical and Major finding |
| [Recommendations](#recommendations) | Prioritized mitigation plan |
| [Scoring Impact](#scoring-impact) | Mapping findings to S-014 quality dimensions |

---

## Summary

Pre-Mortem analysis identified 3 Critical and 7 Major failure causes across all 5 failure category lenses, with concentrated risk in the Technical (production fidelity gap), Assumption (audience comprehension), and Process (no live fallback) categories. The script's core failure mode is a structural mismatch between its extremely high technical specificity in the visual layer and the audience's actual ability to absorb that specificity in a 2-minute hype context -- the video is optimized for a developer who already understands Jerry, not for a cold Anthropic investor or developer who has never heard the name. This is compounded by irreversibility: once the video plays at Shack15, there is no retry. The deliverable requires targeted revisions on PM-001 (abstraction gap for cold audiences), PM-003 (missing GitHub URL on screen), and PM-007 (music licensing risk) before acceptance. **Recommendation: REVISE -- 3 Critical findings require mitigation before the video is produced and locked.**

---

## Failure Scenario Declaration

### Temporal Perspective Shift

It is **August 2026**, six months after the February 21 Shack15 showcase. We are conducting a post-mortem on why the Jerry hype reel failed to generate meaningful community growth or recognition at the Claude Code 1st Birthday Showcase.

**What failure looks like concretely:**

1. The room at Shack15 did not visibly react during or after the video -- no audible responses, no applause, no "wait, what is this?" energy.
2. Developers who attended, when asked afterward, described Jerry as "something with hooks" or "a testing framework" -- not as a governance and quality enforcement system built by Claude Code.
3. The GitHub repository received fewer than 50 stars in the week following the event. The target was meaningful developer traction.
4. Anthropic leadership did not follow up or engage with the creator after the showcase. The "built entirely by Claude Code" angle did not land.
5. The InVideo AI-generated video had visual artifacts or pacing mismatches that made it feel generic compared to professionally produced showcase content.

This is the failure state. We now work backward to identify what in the script created the conditions for this outcome.

---

## Findings Table

| ID | Failure Cause | Category | Likelihood | Severity | Priority | Affected Dimension |
|----|---------------|----------|------------|----------|----------|--------------------|
| PM-001-20260218 | Abstraction gap: cold audiences cannot parse what Jerry does from narration alone | Assumption | High | Critical | P0 | Completeness |
| PM-002-20260218 | InVideo AI cannot render the specified visuals -- terminal animations, real code cascades, hexagonal diagram assembling | Technical | High | Critical | P0 | Methodological Rigor |
| PM-003-20260218 | GitHub URL visible only for 10 seconds at end -- CTA lost in a low-attention exit moment | Process | High | Critical | P0 | Actionability |
| PM-004-20260218 | Music licensing: "Sabotage," "Harder Better Faster Stronger," "C.R.E.A.M.," "Numbers on the Boards" are all commercially licensed tracks | External | High | Major | P1 | Internal Consistency |
| PM-005-20260218 | Scene 4 McConkey reference lands as non-sequitur for audience members who do not know who Shane McConkey is | Assumption | High | Major | P1 | Completeness |
| PM-006-20260218 | Stat accuracy fragility: "3,195+ tests" and "33 agents" will be wrong if code changes between now and February 21 | Technical | Medium | Major | P1 | Evidence Quality |
| PM-007-20260218 | The "CLAUDE CODE BUILT ITS OWN OVERSIGHT SYSTEM" claim requires explanation -- regulators, investors may interpret "oversight system" as an AI safety claim, not a dev tooling claim | External | Medium | Major | P1 | Internal Consistency |
| PM-008-20260218 | 276 words at 140 WPM = 1:58 -- leaves zero margin for InVideo pacing variance; video may run over 2:00 | Technical | Medium | Major | P1 | Methodological Rigor |
| PM-009-20260218 | No fallback plan if InVideo AI generation fails or produces unacceptable output before February 21 (3 days away) | Process | Medium | Major | P1 | Actionability |
| PM-010-20260218 | Scene 3 text overlays ("CONSTITUTIONAL GOVERNANCE," "ADVERSARIAL SELF-REVIEW") require developer-native vocabulary -- investors read these as jargon | Assumption | Medium | Minor | P2 | Completeness |
| PM-011-20260218 | Apache 2.0 badge shown in close but repo may not be publicly accessible yet -- no validation step noted | Process | Low | Minor | P2 | Evidence Quality |
| PM-012-20260218 | Music arc requires 5 distinct licensed tracks matching scene transitions precisely -- InVideo AI may not honor cue timing | Technical | Low | Minor | P2 | Methodological Rigor |

---

## Finding Details

### PM-001-20260218: Abstraction Gap for Cold Audiences [CRITICAL]

**Failure Cause:** The narration in Scene 3 ("Five layers of enforcement. Constitutional governance that cannot be overridden. Thirty-three agents across seven skills. Problem-solving. Orchestration. Architecture. NASA-grade systems engineering.") is a feature list. A developer who has never encountered Jerry hears this and constructs no mental model of what the system does or why they would want it. The problem statement in Scene 2 ("Context fills. Rules drift. Quality rots.") is good, but the solution presented in Scene 3 is a noun-list without a verb -- it describes what Jerry has, not what Jerry does for the developer. The hook angle ("Claude Code built its own oversight system") is intellectually compelling but presupposes the viewer cares about meta-recursion. Investors and non-developer attendees will not have the context to understand why an AI building its own guardrails is remarkable rather than alarming.

**Category:** Assumption
**Likelihood:** High -- the target audience at Shack15 will include Anthropic leadership and investors with no prior Jerry exposure. The self-review notes "Saucer Boy energy throughout" as a PASS, but Saucer Boy is an in-group reference.
**Severity:** Critical -- if the audience cannot form a mental model of what Jerry does in the first 60 seconds, the remaining 90 seconds of feature montage and stats reinforce confusion rather than resolve it.
**Evidence:** Scene 3 narration (0:30-1:00): "So Claude built Jerry. A framework that enforces its own quality -- from the inside." The phrase "enforces its own quality from the inside" is abstract. The visual direction ("Motion graphics show the 5-layer enforcement architecture stacking up like armor plating") does not anchor the abstraction to a concrete user benefit.
**Dimension:** Completeness (missing user-benefit articulation for cold audiences)
**Mitigation:** Add one concrete "before/after" sentence in Scene 3 narration that translates the feature list into a user outcome: "Before Jerry: session 4 hours in, the agent forgets its own rules. After Jerry: every prompt re-enforces the same constitutional constraints, automatically." This provides the mental model that the feature list lacks.
**Acceptance Criteria:** A developer unfamiliar with Jerry, after watching, can describe in one sentence what the system does for them -- not what it is made of.

---

### PM-002-20260218: InVideo AI Cannot Render Specified Visuals [CRITICAL]

**Failure Cause:** The script's visual directions assume capabilities that AI video generation tools in the InVideo class cannot reliably produce: (a) "rapid-fire: Claude Code writing Python, tests passing in green cascades, git commits flying" -- InVideo AI generates stock footage composites, not real terminal recordings; (b) "Camera pulls back to reveal the terminal is INSIDE another terminal" -- nested terminal inception requiring custom motion graphics; (c) "Hexagonal architecture diagram assembles itself piece by piece" -- custom animated diagram; (d) "quality score calculating in real-time: dimension by dimension, the weighted composite climbing" -- custom data visualization animation. If InVideo generates generic "developer at laptop" stock footage instead of these specific visuals, the video will look like every other developer-tool promo reel and the technical specificity that makes the script distinctive will be completely invisible.

**Category:** Technical
**Likelihood:** High -- InVideo AI's generative video capabilities cannot produce custom code terminal output, custom animated architecture diagrams, or real-time number-counter animations on demand. These require either screen recordings of the actual system or custom motion graphics production.
**Severity:** Critical -- the visual layer is the primary vehicle for establishing Jerry's technical credibility. Generic stock footage undermines the entire positioning. The script is written as if the visuals will match the narration beat-for-beat; if they do not, narration and visuals will be incoherent.
**Evidence:** Scene 1 visual direction: "rapid-fire: Claude Code writing Python, tests passing in green cascades, git commits flying. Camera pulls back to reveal the terminal is INSIDE another terminal." Scene 5 visual direction: "quality score calculating in real-time: dimension by dimension." These are specific technical animations, not general visual concepts.
**Dimension:** Methodological Rigor (no production feasibility check against InVideo AI's actual capabilities)
**Mitigation:** Either (a) produce the terminal screen recordings and animated diagrams as source assets before InVideo generation -- upload them as reference footage so InVideo composites around real footage -- or (b) rewrite visual directions to use only visuals InVideo can generate reliably (text overlays, color washes, existing recorded footage). A hybrid approach: record 90 seconds of actual Jerry running in terminal and use that as the dominant visual track, with InVideo providing the text overlay animation layer.
**Acceptance Criteria:** A test generation pass through InVideo is run before February 21 to validate the visual output matches the script direction. At least 4 of 6 scenes must produce visuals that match the narration's technical content.

---

### PM-003-20260218: GitHub URL CTA Lost at End of Video [CRITICAL]

**Failure Cause:** The entire video builds to the open-source call to action, and the GitHub URL (`github.com/geekatron/jerry`) appears only in Scene 6 at 1:50-2:00 -- a 10-second window at the end of a 2-minute video. At a live event, the final 10 seconds are the lowest-attention moment: people are already turning to their phones, starting conversations, or processing what they just watched. The URL will appear, flash by, and disappear. No QR code, no persistent display, no mechanism for the URL to survive the presentation moment and reach the developer's clipboard. The self-review marks "Close drives to repo" as PASS based on inclusion, not on whether the audience will actually capture the URL.

**Category:** Process
**Likelihood:** High -- at a live event with ambient noise, social energy, and no pause mechanism, a 10-second URL display will be missed by the majority of the audience.
**Severity:** Critical -- open-source community growth is the stated goal ("Come build with us"). If developers who want to follow up cannot find the repo, the showcase produces zero lasting engagement.
**Evidence:** Scene 6: "**TEXT OVERLAY:** `github.com/geekatron/jerry`" -- single 10-second appearance in the final scene. No QR code direction. No instruction to show the URL for a sustained period or repeat it earlier in the video.
**Dimension:** Actionability (CTA mechanism is specified but not validated for live event context)
**Mitigation:** (a) Add a QR code overlay in Scene 6 -- InVideo can overlay static images; (b) extend the URL display to a full 15-second hold with "Logo holds for 3 seconds" extended to "URL and QR code hold for 15 seconds after narration ends"; (c) add the GitHub URL as a secondary overlay earlier (Scene 5 or as a persistent bottom-bar in Scenes 5-6). Additionally, coordinate with event organizers to have the URL displayed on a slide after the video.
**Acceptance Criteria:** The GitHub URL and a QR code are both visible for a minimum of 15 seconds at the end of the video. The URL is also surfaced at least once before Scene 6.

---

### PM-004-20260218: Music Licensing Blocks Publication [MAJOR]

**Failure Cause:** The script specifies five commercially licensed tracks for playback at a public event and in any online video: "DNA." (Kendrick Lamar), "Sabotage" (Beastie Boys), "Harder, Better, Faster, Stronger" (Daft Punk), "C.R.E.A.M." (Wu-Tang Clan), "Numbers on the Boards" (Pusha T). Playing these tracks at a public showcase without synchronization licenses is copyright infringement. Publishing the video online with these tracks will result in immediate DMCA takedown by the rights holders. The event itself may generate legal exposure for the organizer. The music choices are central to the script's personality and brand -- removing them post-production degrades the video significantly.

**Category:** External
**Likelihood:** High -- all five tracks are registered with major labels (Interscope, Capitol, Columbia, Universal, Def Jam). YouTube, Instagram, and other platforms run automated ContentID detection that will flag these tracks within hours of upload.
**Severity:** Major -- the event playback may survive as a one-time performance exception, but the video cannot be distributed online in its current form. Given that online distribution is necessary for the open-source CTA to generate repo traffic, this blocks the primary post-event goal.
**Evidence:** Scene 2 music: "Sabotage." Scene 3 music: "Harder, Better, Faster, Stronger." Scene 4 music: "C.R.E.A.M." Scene 5 music: "Numbers on the Boards." Scene 1 music: "DNA." energy reference (unclear if the actual track or inspiration).
**Dimension:** Internal Consistency (claims "THIS IS PRODUCTION" but has an unresolvable distribution blocker)
**Mitigation:** Source royalty-free alternatives from Artlist, Epidemic Sound, or Musicbed that match the energy profiles specified in the script. Map each licensed track to a royalty-free equivalent before production. The energy descriptions ("Sabotage energy -- distorted bass," "Daft Punk vocoder") are sufficient to brief a music supervisor or search a royalty-free library. Alternatively, commission original tracks -- more expensive but solves the problem permanently.
**Acceptance Criteria:** All 5 music tracks in the final produced video are either (a) royalty-free with verified licenses, (b) original compositions, or (c) covered by a sync license obtained before February 21. Legal clearance documented.

---

### PM-005-20260218: McConkey Reference Lands as Non-Sequitur [MAJOR]

**Failure Cause:** Scene 4 ("The Soul") pivots to vintage Shane McConkey ski footage and builds the entire scene's meaning on the McConkey/grinning-while-being-the-best analogy. Shane McConkey is a skiing legend to anyone in the freeskiing subculture, but he is essentially unknown to the majority of software developers, Anthropic employees, and investors in the Shack15 audience. The audience will see ski footage and think "why is there a ski video?" The narration spends 30 seconds on this analogy (Scene 4 is 0:30 of a 2:00 video). If the reference does not land, Scene 4 reads as tonal whiplash -- a personality indulgence that loses the thread of the argument right after the technical peak of Scene 3.

**Category:** Assumption
**Likelihood:** High -- the Shack15 audience is a San Francisco tech crowd. The overlap between "knows who Shane McConkey is" and "attends an AI developer showcase" is small. The reference is an insider joke without setup.
**Severity:** Major -- Scene 4 is the "soul" segment meant to differentiate Jerry from every other "serious framework." If the reference lands, it is memorable and charming. If it does not land, it reads as confused pacing and undermines the confidence built by Scene 3.
**Evidence:** Scene 4 narration: "Shane McConkey didn't revolutionize skiing by being serious. He did it by being the best in the world -- and grinning the entire time." No setup for who McConkey is. The visual direction says "Vintage ski footage -- Shane McConkey launching off a cliff in a onesie" without any context overlay.
**Dimension:** Completeness (analogy requires shared context that cannot be assumed)
**Mitigation:** Add a one-line text overlay when McConkey appears: `SHANE McCONKEY | REVOLUTIONIZED SKIING BY REFUSING TO BE BORING` -- this provides the context the audience needs to understand the analogy without stopping to explain it in narration. Alternatively, find a more universally recognized "brilliant and fun" reference (Richard Feynman, Wile E. Coyote, etc.) that does not require skiing subculture knowledge.
**Acceptance Criteria:** A cold viewer (no skiing background) who watches Scene 4 understands the analogy and can explain what McConkey has to do with Jerry within 5 seconds of the scene ending.

---

### PM-006-20260218: Stat Accuracy Fragility [MAJOR]

**Failure Cause:** The script commits to specific numeric claims: "3,195+ tests," "33 agents," "7 skills," "10 adversarial strategies," "5 layers." These numbers are accurate as of 2026-02-18 (today). The event is February 21 -- 3 days away. If any code is committed between today and February 21 that adds, removes, or modifies tests or agents, the script's numbers become inaccurate. More seriously, the video will be locked after InVideo production -- the numbers in the video cannot be updated after the final render. If the numbers change post-event, the video becomes a historical artifact with stale claims.

**Category:** Technical
**Likelihood:** Medium -- 3 days is a short window, but active development on an OSS project before a showcase launch is very likely. Any additional test, bug fix, or agent addition will increment the test count.
**Severity:** Major -- claiming "3,195+ tests" when the actual count is different (higher or lower) undermines the credibility of the "THIS IS PRODUCTION" close. Investors and developers who check the repo will notice discrepancies.
**Evidence:** Scene 5 narration: "Three thousand one hundred ninety-five tests. Passing." Scene 3 text overlay: "33 AGENTS / 7 SKILLS." Self-review "Stats accurate and impactful: PASS" -- but this was validated at script-creation time, not at video-production time.
**Dimension:** Evidence Quality (numbers will drift between script creation and video lock)
**Mitigation:** (a) Use a "3,000+" phrasing instead of "3,195+" in narration to create a durable claim that does not go stale with a single test addition; (b) if exact numbers are kept, add a production gate: run the full test suite immediately before the final video render to confirm numbers match; (c) validate all numeric claims against the live repo on February 20 (day before event) before submitting to InVideo for final render.
**Acceptance Criteria:** All numeric claims in the final produced video are validated against the live repository output on February 20, 2026, within 24 hours of event.

---

### PM-007-20260218: "Oversight System" Framing Risk [MAJOR]

**Failure Cause:** The TEXT OVERLAY in Scene 1 reads: `CLAUDE CODE BUILT ITS OWN OVERSIGHT SYSTEM`. In the context of February 2026 AI discourse -- where AI safety, autonomous systems, and AI oversight are politically and regulatorily charged topics -- the phrase "oversight system" will be interpreted by non-developer attendees through an AI safety lens, not a developer tooling lens. Anthropic leadership may read "Claude Code built its own oversight system" and have a knee-jerk concern about autonomous AI creating governance structures for itself. This is the opposite of the intended "wow, look at this clever recursive demonstration" reaction.

**Category:** External
**Likelihood:** Medium -- the Shack15 audience skews technical, but Anthropic leadership is specifically attuned to AI safety framing. The phrase "oversight system" is loaded vocabulary in their domain.
**Severity:** Major -- if the opening text overlay triggers an AI safety concern in leadership, the audience enters Scene 2 in a defensive posture rather than an impressed one. The cold open is the highest-attention moment of the video; a misread there cascades through the remaining 1:45.
**Evidence:** Scene 1 TEXT OVERLAY: `CLAUDE CODE BUILT ITS OWN OVERSIGHT SYSTEM`. The narration clarifies "build your own guardrails" but the overlay is what lands first and is retained longest.
**Dimension:** Internal Consistency (overlay framing conflicts with the intended positioning as a dev tool, not an AI safety system)
**Mitigation:** Replace the overlay with developer-native language that is unambiguous: `CLAUDE CODE BUILT ITS OWN QUALITY ENFORCEMENT SYSTEM` or `CLAUDE CODE WROTE ITS OWN RULES -- AND ENFORCES THEM`. This preserves the meta-recursive angle without triggering AI safety alarm bells.
**Acceptance Criteria:** The Scene 1 text overlay uses language that a) preserves the meta-recursive angle and b) is reviewed and approved by at least one person with AI safety communication familiarity before the video is finalized.

---

### PM-008-20260218: Word Count Leaves No Pacing Margin [MAJOR]

**Failure Cause:** The script calculates 276 words at 140 WPM as yielding 1:58. This leaves a 2-second margin before the 2:00 hard limit. In practice, InVideo AI's text-to-speech narration speed is not precisely 140 WPM -- it varies by sentence length, punctuation, and emphasis. Live narration (if a human voice-over is used) will vary further. Scene transitions, music cue timing, and visual beat-matching all add latency that the script treats as zero. A single extra breath at a scene break pushes the video over 2:00. If the platform has a strict 2:00 limit, the audio will cut, potentially losing the close narration entirely.

**Category:** Technical
**Likelihood:** Medium -- AI-generated narration is variable; platform time limits are strict.
**Severity:** Major -- losing the close narration ("Come build with us") is catastrophic for the CTA. The close is the action moment; if it clips, the video ends on silence or mid-sentence.
**Evidence:** Script Overview: "Total Runtime: 2:00 | Narration Word Count: 276 words | Target WPM: 140." Self-review: "Total narration ~280 words: PASS (276 words, 1:58 at 140 WPM)." No pacing buffer noted.
**Dimension:** Methodological Rigor (no margin analysis for timing variance)
**Mitigation:** Reduce narration to 260 words (1:51 at 140 WPM) to provide a 9-second buffer -- enough to absorb 1-2 seconds per scene transition across 6 scenes. Alternatively, target 130 WPM (industry standard for clear comprehension) which yields ~2:07 -- in that case, trim to 240 words for a 1:51 result. Run the InVideo narration generation in a test pass and time the actual output before the final script is locked.
**Acceptance Criteria:** A test narration render of the full script is timed and confirmed under 1:55 before the final video production pass.

---

### PM-009-20260218: No Production Fallback [MAJOR]

**Failure Cause:** The event is February 21, 2026 -- 3 days from the script creation date of February 18. The script assumes InVideo AI will successfully generate an acceptable video in this window. If InVideo (a) generates visually incoherent output, (b) fails to match music to scene timing, (c) produces a version that is obviously AI-generated in a way that reads as low-quality, or (d) encounters a platform outage, there is no documented fallback. There is no mention of a Plan B production approach (slides, live demo, pre-recorded terminal session) if the AI video does not meet quality standards.

**Category:** Process
**Likelihood:** Medium -- InVideo AI can produce acceptable output, but producing C4-quality (public showcase, irreversible) video requires iteration, and 3 days allows very limited iteration cycles.
**Severity:** Major -- showing up at Shack15 with no video, or with a visually degraded video that undercuts the "THIS IS PRODUCTION" claim, is a worse outcome than showing up with a polished 60-second slide deck.
**Evidence:** The script contains complete InVideo AI production direction but no contingency or fallback notation. No production timeline or iteration plan is mentioned.
**Dimension:** Actionability (no contingency for production failure)
**Mitigation:** Document a fallback plan: if the InVideo output does not meet quality standards after 2 production iterations (by February 20), the fallback is a 60-second live terminal demo or a screen-recorded walkthrough with narration. Designate a go/no-go decision point for February 20 at noon.
**Acceptance Criteria:** A documented fallback plan exists with a go/no-go decision time of February 20 at noon. The fallback is viable and does not require additional production work.

---

## Recommendations

### P0 -- Critical: MUST Mitigate Before Video Production Lock

**PM-001 -- Abstraction Gap**
Action: Add one concrete "before/after" user-outcome sentence to Scene 3 narration: "Before Jerry, session hour four: the agent forgets its own rules. After Jerry: every prompt re-enforces constitutional constraints, automatically." This adds approximately 20 words; offset by trimming Scene 3's feature list by an equivalent amount.
Acceptance Criteria: A cold viewer (no prior Jerry knowledge) can describe in one sentence what Jerry does for them after watching.

**PM-002 -- InVideo Visual Fidelity**
Action: Record screen captures of the actual Jerry system running (hook validation, test suite, quality gate output) before February 20. Upload to InVideo as reference footage. Run a test generation pass to validate visual output quality before final lock.
Acceptance Criteria: Test InVideo output reviewed and confirmed: at least 4 of 6 scenes use visuals that match the narration's technical content.

**PM-003 -- GitHub URL CTA**
Action: (a) Add a QR code overlay to Scene 6 directing to `github.com/geekatron/jerry`; (b) extend the close to 15 seconds of URL/QR hold; (c) add the URL as a persistent bottom-bar overlay beginning in Scene 5. Coordinate with event organizers to show the URL on a slide immediately after the video.
Acceptance Criteria: URL and QR code visible for minimum 15 seconds; URL appears in at least Scenes 5 and 6.

---

### P1 -- Important: SHOULD Mitigate Before Event

**PM-004 -- Music Licensing**
Action: Source royalty-free equivalents for all 5 specified tracks from Artlist or Epidemic Sound. Map each to the energy profile in the script. Obtain licenses before production begins.
Acceptance Criteria: All music tracks in the final video are covered by documented royalty-free licenses or original compositions.

**PM-005 -- McConkey Context**
Action: Add text overlay when McConkey appears: `SHANE McCONKEY | REVOLUTIONIZED SKIING BY REFUSING TO BE BORING`. Or substitute with a more universally recognized "brilliant and fun" reference.
Acceptance Criteria: A cold viewer with no skiing background understands the analogy within 5 seconds of Scene 4 ending.

**PM-006 -- Stat Accuracy**
Action: Change "Three thousand one hundred ninety-five tests" to "Over three thousand tests" in narration. Validate all numeric claims against the live repo on February 20.
Acceptance Criteria: Numeric claims validated against live repo output within 24 hours of event.

**PM-007 -- Oversight Framing**
Action: Replace Scene 1 overlay `CLAUDE CODE BUILT ITS OWN OVERSIGHT SYSTEM` with `CLAUDE CODE WROTE ITS OWN RULES -- AND ENFORCES THEM`.
Acceptance Criteria: Overlay reviewed by one person with AI safety communication familiarity and confirmed not to trigger safety framing concerns.

**PM-008 -- Pacing Margin**
Action: Trim narration to 260 words. Run a test narration pass in InVideo and time the output. Confirm under 1:55 before final lock.
Acceptance Criteria: Test render timed at under 1:55.

**PM-009 -- Production Fallback**
Action: Document a fallback plan (live terminal demo or screen recording) with a go/no-go decision point of February 20 at noon.
Acceptance Criteria: Fallback plan documented and decision-point calendar item set.

---

### P2 -- Monitor: MAY Mitigate; Acknowledge Risk

**PM-010 -- Technical Jargon in Overlays**
Risk: "CONSTITUTIONAL GOVERNANCE" and "ADVERSARIAL SELF-REVIEW" may read as jargon to non-developer attendees. Monitor: if the primary audience is confirmed as developers, accept the vocabulary. If significant investor presence is expected, consider replacing with "UNBREAKABLE RULES" and "SELF-ATTACKING REVIEW" respectively.

**PM-011 -- Repo Accessibility**
Risk: The close references `github.com/geekatron/jerry` and Apache 2.0, but if the repo is not publicly accessible by February 21, the CTA fails entirely. Validate repo visibility on February 20.

**PM-012 -- Music Cue Timing**
Risk: InVideo AI may not honor precise music cue transitions. If the Daft Punk beat drop does not land on the Scene 3 transition, the signature moment loses impact. Test music sync in the production pass.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | PM-001, PM-005, PM-010: The script is complete in structure but incomplete in audience reach -- it speaks fluently to in-group developers and leaves cold audiences without a mental model. Scene 4's McConkey reference presupposes shared context. |
| Internal Consistency | 0.20 | Negative | PM-004, PM-007: The script asserts "THIS IS PRODUCTION" while containing unresolvable music licensing blockers for online distribution. The "oversight system" overlay is inconsistent with the dev-tool positioning in the narration. |
| Methodological Rigor | 0.20 | Negative | PM-002, PM-008, PM-009: No production feasibility check against InVideo's actual capabilities. Zero pacing buffer. No fallback plan. The script was created and self-reviewed but not stress-tested against production constraints. |
| Evidence Quality | 0.15 | Negative | PM-006: Numeric claims (3,195 tests, 33 agents) are point-in-time accurate but will drift without a validation gate. No source citation for when these numbers were last confirmed against live system output. |
| Actionability | 0.15 | Negative | PM-003, PM-009: The CTA (GitHub URL) is present but not designed for the live event context. No production fallback renders the plan brittle -- if InVideo fails, there is no actionable alternative. |
| Traceability | 0.10 | Neutral | The script structure traces well to its stated goals (6 scenes, pacing arc, open-source CTA). Finding IDs are mapped to deliverable content. Self-review table provides baseline traceability. The meta-angle ("Claude Code built Jerry") is consistent throughout. |

**Overall Assessment:** 3 Critical and 7 Major failure causes identified. The script's creative vision is strong and the structural arc is sound -- the S-003 Steelman work holds. The failure risks cluster in three areas: production feasibility (the visuals cannot be generated as specified), live-event practicality (the CTA will not survive the attention context), and distribution viability (the music is not licensable for online publication). These are solvable problems within the 3-day window if acted on immediately. **REVISE before production lock.**

**Estimated score impact of full mitigation:** Pre-mitigation composite estimate ~0.78 (below threshold). Post-mitigation (all P0/P1 addressed) estimate ~0.91-0.93 -- within range of the 0.95 target with revision.

---

*Strategy: S-004 Pre-Mortem Analysis*
*Execution ID: 20260218*
*Template: s-004-pre-mortem.md v1.0.0*
*SSOT: quality-enforcement.md*
*H-16 Compliance: S-003 Steelman confirmed present (adv-executor-001-s003-steelman.md)*
*Date: 2026-02-18*
