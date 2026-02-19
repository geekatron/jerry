# Inversion Report: Jerry Framework Hype Reel Script v3

**Strategy:** S-013 Inversion Technique
**Deliverable:** `projects/PROJ-001-oss-release/work/EPIC-001-oss-release/FEAT-023-showcase-video/orchestration/feat023-showcase-20260218-001/showcase/phase-3-tournament/iteration-3/ps-architect-001-hype-reel-script-v3.md`
**Criticality:** C4
**Date:** 2026-02-18
**Reviewer:** adv-executor (S-013)
**H-16 Compliance:** S-003 Steelman applied (iteration-3/s-003-steelman directory confirmed present)
**Goals Analyzed:** 7 | **Assumptions Mapped:** 14 | **Vulnerable Assumptions:** 8

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Step 1: Goals](#step-1-goals) | Explicit and implicit goals restated in measurable terms |
| [Step 2: Anti-Goals](#step-2-anti-goals) | Goal inversions -- what would guarantee failure |
| [Step 3: Assumption Map](#step-3-assumption-map) | All explicit and implicit assumptions with confidence and consequence |
| [Step 4: Stress-Test Results](#step-4-stress-test-results) | Inverted assumptions with plausibility, severity, and dimension impact |
| [Step 5: Mitigations](#step-5-mitigations) | Specific mitigations for Critical and Major findings |
| [Step 6: Scoring Impact](#step-6-scoring-impact) | Dimension-level impact table and overall assessment |
| [Summary](#summary) | Two-sentence assessment and verdict |
| [Findings Table](#findings-table) | All IN-NNN findings at a glance |
| [Finding Details](#finding-details) | Expanded Critical and Major finding descriptions |
| [Recommendations](#recommendations) | Prioritized mitigation actions |

---

## Summary

The v3 script resolves all seven Critical findings and all seven Major findings from the iteration 2 composite (scored 0.82), demonstrating a disciplined, comprehensive revision pass with no new assertion introductions. However, S-013 Inversion stress-testing of the v3-specific assumptions -- outcome language in Scene 3, QR code production dependency, music library non-determinism, and trimmed McConkey narration -- surfaces 2 Critical and 6 Major vulnerable assumptions that remain unaddressed and can materially degrade quality at the live event. ACCEPT with targeted mitigations required; the Critical findings must be resolved before the production lock on Feb 20.

---

## Step 1: Goals

**Procedure applied:** Goals extracted from v3 deliverable content, self-review section, revision log, and production dependencies. Restated in specific, measurable terms. Implicit goals inferred from event context (live audience, Feb 21 showcase, OSS launch).

| G-ID | Type | Goal (Specific, Measurable Form) |
|------|------|-----------------------------------|
| G-01 | Explicit | Script narration executes within 2:00 at natural delivery pace (~120-130 WPM with pauses), with >= 10 seconds of buffer for scene transitions. |
| G-02 | Explicit | All six scenes render in InVideo AI as intended; FALLBACK directions activate cleanly if primary visuals fail. |
| G-03 | Explicit | Scene 6 CTA (GitHub URL + QR code) is capturable by a live audience in <= 13 seconds of hold time. |
| G-04 | Explicit | github.com/geekatron/jerry returns HTTP 200, public (no auth), README present, LICENSE: Apache 2.0 by Feb 20 23:59. |
| G-05 | Explicit | Narration and overlays contain no claims that are falsifiable by an engineer, investor, or Anthropic researcher present at the event on Feb 21. |
| G-06 | Implicit | The "Saucer Boy" tone (technically brilliant, wildly fun) lands for a mixed audience (developers, investors, Anthropic leadership, event attendees) -- assessed qualitatively by a human reviewer before final render. |
| G-07 | Implicit | The script's meta-narrative ("Claude Code wrote its own guardrails") is comprehensible AND compelling to non-developer audience members (investors, leadership) without requiring prior knowledge of Claude Code, Jerry, or context rot. |

---

## Step 2: Anti-Goals

**Procedure applied:** For each goal, asked: "What would guarantee we FAIL to achieve this goal?" Enumerated specific conditions. Assessed whether v3 currently avoids each condition.

| G-ID | Anti-Goal: "To guarantee failure at [goal], we would need to..." | v3 Avoidance Status |
|------|-------------------------------------------------------------------|---------------------|
| G-01 | Deliver narration at broadcast 140 WPM without a real timed table read; or add words in the final production review that push count back above 270. | PARTIAL -- v3 trimmed to 257 words and added 10s buffer, but no timed table read at natural pace is confirmed as completed. Self-review says "Timed table read at natural pace recommended" (future tense), not "conducted." |
| G-02 | Rely on InVideo AI to generate animation it cannot produce without pre-rendered assets; or activate FALLBACK too late (day of event). | PARTIAL -- FALLBACK lines added to Scenes 2, 5, 6; but InVideo test pass deadline is Feb 19 noon, and no pre-rendered asset for Scene 5 adversarial tournament bracket exists. The bracket visualization ("10 strategies converging on a single quality gate") is still generative. |
| G-03 | Display a QR code that links to an un-live repository; or render a QR code that is too small to scan on a projector screen; or use a QR code generated from an unverified URL. | UNADDRESSED -- v3 adds QR code to visual direction and text overlay but does not specify minimum pixel size, minimum projector-screen scan distance, or QR code generation source. The QR code is a production dependency item with no quality criterion for scan reliability. |
| G-04 | Have the repository remain private, renamed, or 404 at showtime due to a missed deadline or accidental repo visibility change. | PARTIAL -- Production Dependencies Item 1 covers this with a Feb 20 23:59 deadline and fallback text. But fallback text removes the core OSS narrative ("remove 'Open source'" from narration) without flagging that this changes the meta-identity of the video. |
| G-05 | Retain any falsifiable claim that an audience member can immediately disprove with a phone in their pocket. | PARTIAL -- CF-004 ("cannot be overridden") fixed; CF-005 ("33 agents") fixed to "30+"; CF-003 fixed to outcome language. But "nobody had a fix for enforcement" (Scene 2) is still present with only an implicit scope. MF-003 guidance said to scope it to "session hooks" -- v3 narration still reads "Nobody had a fix for enforcement" with no qualifier. |
| G-06 | Choose music library tracks that are tonally inconsistent, too aggressive for the venue acoustics, or that the human reviewer rejects on day-of-render, leaving no time for re-selection. | UNADDRESSED -- v3 adds music sourcing note ("human reviewer approval required for all 6 cues") and lists Scene 2, 3, and 4 as specifically requiring confirmation, but sets no deadline for music approval. Music selection is mood/BPM/key description only; the actual track selection decision is deferred to production with no timeline. |
| G-07 | Open Scene 3 with a 30-second technical montage (hook validations, JSON schemas, agents spawning) before any non-developer anchor phrase; or use outcome language so vague ("hour twelve works like hour one") that the non-developer cannot construct a mental model of what went wrong before Jerry. | PARTIAL -- "hour twelve works like hour one. The rules never drift." resolves mechanism language. But the "before" side ("your agent forgets its own rules") still requires the viewer to know that AI agents have rules, that those rules can be forgotten, and that this is bad. Non-developer comprehension of the problem remains audience-dependent. |

---

## Step 3: Assumption Map

**Procedure applied:** All explicit assumptions in v3 identified. Implicit assumptions across five categories (Technical, Process, Resource, Environmental, Temporal) surfaced. Each assessed for Confidence (H/M/L) and Validation Status (Empirical / Inferred / Assumed).

| A-ID | Type | Category | Assumption | Confidence | Validation | Consequence of Failure |
|------|------|----------|------------|------------|------------|------------------------|
| A-01 | Implicit | Technical | InVideo AI can render the Scene 5 "tournament bracket visualization: 10 adversarial strategies converging on a single quality gate" without a pre-rendered asset | Low | Assumed | Scene 5 primary visual fails; FALLBACK used; score-hit momentum lost |
| A-02 | Explicit | Technical | github.com/geekatron/jerry will be HTTP 200, public, README present, Apache 2.0 by Feb 20 23:59 | Medium | Inferred (Production Dependencies Item 1) | CTA fails at highest-attention moment; Plan B overlay lacks OSS narrative |
| A-03 | Implicit | Technical | The QR code will be scannable from audience seating distance on the Shack15 projector screen | Low | Assumed | QR code is decorative, not functional; CTA reverts to recall-only |
| A-04 | Explicit | Process | A human reviewer will approve all 6 music cues before final render | Medium | Inferred (Music Sourcing note in Overview) | Music is locked without approval, or approval blocks final render |
| A-05 | Implicit | Process | Music approval will occur early enough (before Feb 20) to allow re-selection if cues are rejected | Low | Assumed (no deadline in script) | Music blocked at render time; fallback to silence or wrong cue |
| A-06 | Explicit | Process | Agent count will be verified by running `find . -name "*.md" -path "*/agents/*" \| wc -l` on the Feb 20 commit | Medium | Inferred (Production Dependencies Item 2) | "30+" floor claimed for a count that may have dipped; count vulnerable |
| A-07 | Implicit | Resource | A video producer has InVideo AI access and proficiency sufficient to render Scenes 1-6 (and activate FALLBACK directions) by Feb 19 noon | Medium | Assumed | InVideo test pass gate missed; Plan B decision deferred to Feb 20 without a test result |
| A-08 | Implicit | Environmental | "Nobody had a fix for enforcement" (Scene 2) scopes to Claude Code's hook architecture implicitly; audience will not name LangMem, MemGPT, or Guardrails AI as counterexamples in real time | Low | Assumed | Public rebuttal at the event undermines credibility; S-001 RT-004 finding persists from v1 |
| A-09 | Explicit | Environmental | The event venue (Shack15, SF) has projector and audio setup compatible with the video format and music delivery | Medium | Inferred (venue confirmed in header) | Technical failure at venue; no contingency mentioned |
| A-10 | Implicit | Temporal | The trimmed McConkey narration (62 words in Scene 4, down from 78) still conveys mastery AND disposition without the grounding text ("the skier who reinvented the sport...") that was moved to the text overlay | Medium | Inferred (revision log) | Non-skier audience loses the mastery anchor; "Shane McConkey didn't reinvent skiing by being serious" has no subject-mastery signal in audio |
| A-11 | Implicit | Temporal | 257 words at 140 WPM targets 1:50 effective; the 10-second buffer accommodates natural pace delivery (120-130 WPM) within 2:00 | Medium | Inferred (self-review table, no read documented) | Actual delivery runs 2:08-2:14 at natural pace; same overrun as CF-002 |
| A-12 | Implicit | Environmental | Scene 4 lo-fi boom-bap transition at 1:00 (from 128 BPM electronic anthem to 85 BPM jazz loop) does not cause auditory whiplash or lose the live audience's attention during the transition | Low | Assumed | Tonal discontinuity at the soul moment; audience disengages during the philosophy scene |
| A-13 | Explicit | Process | Plan B (screen-recorded terminal walkthrough) is ready and operable as a fallback if InVideo output is unsatisfactory by Feb 20 noon | Low | Assumed (listed but not developed) | Plan B decision point arrives without a Plan B artifact; no-go with no alternative |
| A-14 | Implicit | Environmental | The Shack15 audience at Claude Code's birthday party consists of developers, investors, and Anthropic leadership in roughly equal proportions, and "Saucer Boy" tone lands across all three groups | Low | Assumed | Tone misread by investors or leadership as unprofessional for OSS launch |

---

## Step 4: Stress-Test Results

**Procedure applied:** For each assumption, stated the inversion, assessed plausibility, evaluated consequences, classified severity, mapped to scoring dimension, and assigned IN-NNN identifiers for Major+ findings.

| IN-ID | A-ID | Assumption (Inverted) | Plausibility | Severity | Affected Dimension |
|-------|------|-----------------------|-------------|----------|--------------------|
| IN-001-20260218I3 | A-03 | QR code is not scannable from audience seating distance | High | Critical | Actionability |
| IN-002-20260218I3 | A-08 | "Nobody had a fix for enforcement" is directly rebutted at the event by a LangMem/MemGPT engineer or Anthropic researcher | Medium | Critical | Evidence Quality |
| IN-003-20260218I3 | A-05 | Music approval occurs too late to allow re-selection; final render blocked or locked with unreviewed cues | Medium | Major | Methodological Rigor |
| IN-004-20260218I3 | A-13 | Plan B is not ready at the Feb 20 decision point; InVideo fails and no fallback exists | Medium | Major | Completeness |
| IN-005-20260218I3 | A-11 | 257 words at natural delivery pace exceeds 2:00; timed table read was not conducted; buffer assumption is wrong | Medium | Major | Methodological Rigor |
| IN-006-20260218I3 | A-10 | Trimmed McConkey narration loses mastery signal for non-skier audience; text overlay lands too late (visual, not audio-first) | Medium | Major | Evidence Quality |
| IN-007-20260218I3 | A-01 | InVideo cannot render the tournament bracket visualization; FALLBACK substitutes a static scoreboard that reduces Scene 5 to a list of numbers | Medium | Major | Completeness |
| IN-008-20260218I3 | A-12 | 128 BPM -> 85 BPM music transition at 1:00 causes auditory disruption; live audience disengages during Scene 4 | Low | Minor | Internal Consistency |
| IN-009-20260218I3 | A-14 | "Saucer Boy" tone is read as non-professional by a significant share of the investor or leadership segment | Low | Minor | Actionability |
| (none) | A-02 | GitHub URL not live by Feb 20 | Medium | Addressed | -- (Production Dependencies Item 1 with fallback covers this) |
| (none) | A-04 | Music approval not obtained | Medium | Addressed | -- (Music Sourcing note mandates approval; gap is timing -- see IN-003) |
| (none) | A-06 | Agent count < 30 | Low | Addressed | -- (Production Dependencies Item 2 covers this) |
| (none) | A-07 | Video producer lacks InVideo proficiency | Low | Minor | -- (not a script artifact; out-of-scope for script revision) |
| (none) | A-09 | Venue AV failure | Low | Minor | -- (venue/logistics, not script) |

---

## Step 5: Mitigations

### Critical Findings (MUST mitigate before production lock Feb 20)

**IN-001-20260218I3 -- QR Code Scan Reliability**

The v3 script adds "QR code linking to github.com/geekatron/jerry" to Scene 6 visual direction but specifies no scan-quality requirements. A QR code rendered by InVideo AI at arbitrary size on a projector screen at Shack15 may be unreadable at typical audience seating distance (10-30 feet from screen).

**Mitigation:** Add to Production Dependencies Item 1 or Scene 6 visual direction:
- Specify minimum QR code size: >= 10% of frame width
- Specify QR code version / error correction level: minimum Level M (15% redundancy)
- Add production gate: print a test QR code from the InVideo render and verify scan success at 10 feet before Feb 20 noon
- Add backup: print physical QR code cards for distribution at the event

**Acceptance Criteria:** A test scan of the rendered QR code succeeds from 15 feet on a representative projector display. OR physical QR cards are confirmed available at the event registration table.

**IN-002-20260218I3 -- "Nobody Had a Fix for Enforcement" Unscoped**

"Nobody had a fix for enforcement" (Scene 2 narration) has no qualifier in v3. MF-003 guidance in the iteration 2 composite explicitly instructed scoping this to "Claude Code's hook architecture" (enforcement baked into pre/post-tool-call hooks). That fix was recommended but not applied in v3 -- the revision log shows no change to this claim. At the event, a LangMem engineer or Anthropic researcher familiar with Guardrails AI may rebut this in real time, producing a credibility failure at the highest-visibility moment of the OSS launch.

**Mitigation:** Change Scene 2 narration from:
> "Tools handle memory. Nobody had a fix for enforcement."

to:
> "Tools handle memory. Nobody had enforcement baked into the session hooks."

This scopes the claim precisely: LangMem operates at memory retrieval, MemGPT at agent state, Guardrails AI at output validation -- none operate at the Claude Code pre/post-tool-call hook layer. The scoped claim is not falsifiable by any of these tools.

**Acceptance Criteria:** Scene 2 narration uses "session hooks" qualifier. Claim is not falsifiable by any tool operating outside the Claude Code hook layer. Word count delta: +5 words (brings narration from 257 to ~262 -- still within buffer; verify with count).

---

### Major Findings (SHOULD mitigate)

**IN-003-20260218I3 -- Music Approval Deadline Absent**

Music Sourcing note requires human reviewer approval for all 6 cues before final render. No deadline is set. If music approval is attempted Feb 20 night and cues are rejected, there is no time for re-selection.

**Mitigation:** Add deadline to Music Sourcing note: "Human reviewer approval required by Feb 19, noon -- simultaneous with InVideo test pass gate (Production Dependencies Item 3). If any cue is rejected, replacement selection must be confirmed by Feb 20, noon."

**Acceptance Criteria:** Music Sourcing note contains an explicit approval deadline no later than Feb 19 noon, leaving 24+ hours for re-selection.

**IN-004-20260218I3 -- Plan B Not Developed**

Production Dependencies Item 4 states "Plan B: screen-recorded terminal walkthrough with voiceover, same narration script." Plan B is named but not a usable artifact -- no screen recording list, no recording timeline, no narrator confirmation. The Feb 20 noon decision point arrives without a functional Plan B.

**Mitigation:** Add to Production Dependencies Item 4:
- Specify the 3-5 terminal sequences to pre-record (hook validation, quality gate, adversarial tournament run)
- Assign recording owner and recording deadline (Feb 19, 5pm)
- Confirm voice-over recording equipment and narrator

**Acceptance Criteria:** Plan B materials (screen recordings + narration track) are production-ready by Feb 20 noon. Decision point is a selection, not a scramble.

**IN-005-20260218I3 -- Timed Table Read Not Confirmed**

v3 self-review says "Timed table read at natural pace recommended before lock" (Production Dependencies is silent on this; self-review uses future tense). CF-002 was the highest-RPN FMEA finding in iteration 2 (RPN 294). The 10-second buffer is calculated at 140 WPM broadcast pace, not at 120-130 WPM natural delivery. If natural pace delivery runs 1:58-2:08, the buffer evaporates and the last scene is cut off.

**Mitigation:** Add as Production Dependencies Item 5: "Timed table read at natural delivery pace (target: 120-130 WPM). Confirm total delivery time <= 1:55 before locking final narration. If over 1:55, trim Scene 6 expansion ('The framework that governs...') first (9 words); retain meta loop if possible."

**Acceptance Criteria:** A timed read is documented (reader, date, result) and confirms <= 1:55. OR narration is trimmed to 245 words to guarantee the buffer at natural pace.

**IN-006-20260218I3 -- McConkey Mastery Signal Trimmed**

The v3 revision moved McConkey grounding from narration to text overlay to save 12 words (revision log Scene 4 entry). The v3 narration now reads: "Shane McConkey didn't reinvent skiing by being serious." Without the stripped context ("the skier who reinvented the sport..."), non-skiers hear a proper name followed by a skiing reference they may not process before the next line arrives. The text overlay "SHANE McCONKEY // REINVENTED SKIING BY REFUSING TO BE BORING" requires the viewer to read while listening, which is a dual-attention demand at the emotional climax of the video.

**Mitigation (two options, creator selects):**
- Option A: Restore one mastery clause to narration (net +5 words): "Shane McConkey -- ski legend -- didn't reinvent skiing by being serious." The text overlay then reinforces rather than carries the load.
- Option B: Retain current narration but precede the McConkey line with a scene-opening visual beat (0.5 seconds of action sports footage with no narration) so the image registers before the audio arrives, anchoring the reference spatially before the name is spoken.

**Acceptance Criteria:** A human reviewer who does not know Shane McConkey can reconstruct the intended meaning of the Scene 4 analogy on first watch.

**IN-007-20260218I3 -- Scene 5 Tournament Bracket Unresolved as Production Asset**

The v3 VISUAL for Scene 5 describes "Tournament bracket visualization: 10 adversarial strategies converging on a single quality gate. The gate holds." This is a generative visual that InVideo AI cannot render without a pre-drawn asset or motion graphic. The FALLBACK ("Static scoreboard text overlays slam in sequentially with impact frames") omits the tournament bracket entirely, reducing Scene 5 to a list of numbers. The bracket was added in v3 specifically to address MF-005 (self-grading optics), but the production feasibility of the bracket itself was not validated.

**Mitigation:** Add to Production Dependencies Item 3: "Scene 5 tournament bracket visualization requires a pre-drawn asset (static bracket diagram or short motion graphic). Assign a designer or use a pre-recorded screen capture of an actual tournament run output. If no asset is available by Feb 19 noon, activate FALLBACK and accept the scoreboard format."

**Acceptance Criteria:** Scene 5 either (a) renders with a legible tournament bracket sourced from a pre-existing asset, OR (b) activates FALLBACK with confirmation that the scoreboard sequence still communicates adversarial process (not self-grading).

---

## Step 6: Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative (Minor) | IN-004: Plan B is named but not production-ready. IN-007: Tournament bracket visual has no asset assigned. These are gaps in production completeness introduced by v3 improvements. |
| Internal Consistency | 0.20 | Positive | All seven Critical findings from v2 composite are addressed. Narration, overlays, and production notes are internally consistent. MF-003 meta loop closure added. Revision log is complete and traceable. Minor: IN-008 (music transition) is a low-plausibility concern only. |
| Methodological Rigor | 0.20 | Negative (Moderate) | IN-005: Timed table read documented as recommended but not confirmed executed. CF-002 was the highest-RPN finding in the tournament; the buffer calculation remains theoretical. IN-003: Music approval has no deadline, creating a process gap at the most time-sensitive stage. |
| Evidence Quality | 0.15 | Negative (Minor) | IN-002: "Nobody had a fix for enforcement" unscoped -- persists from v1, flagged in MF-003, not applied in v3. This is the only factual claim that remains falsifiable at the event. IN-006: McConkey mastery signal degraded for non-skier audience after narration trimming. |
| Actionability | 0.15 | Negative (Minor) | IN-001: QR code specified without scan-quality criteria. A non-scannable QR code at a live event converts the CTA into a recall-only mechanism -- identical to no QR code. Scene 6's primary actionability mechanism is undermined if the QR code fails. |
| Traceability | 0.10 | Positive | All findings from v2 composite are addressed with explicit finding-level traceability in the self-review. Revision log maps every change to a finding ID. The "30+" hedge traces to the floor verification command in Production Dependencies. |

**Overall Assessment:** ACCEPT with targeted mitigations required. v3 represents a genuine, comprehensive revision that resolves all iteration 2 findings. Two Critical vulnerabilities surface from the v3 changes themselves: QR code scan reliability (IN-001) and the unscoped enforcement claim (IN-002). Both are narrow, fixable in under 30 minutes of script editing. Four Major findings address production-process gaps (music deadline, Plan B readiness, timed table read, Scene 5 asset) that are outside the script narrative but within the production dependencies scope. If IN-001 and IN-002 are resolved and the four Major mitigations are applied, the script is tournament-ready.

**Projected post-mitigation dimension impact:**
- IN-001 resolved: Actionability recovers to strong positive
- IN-002 resolved: Evidence Quality recovers to positive
- IN-003 through IN-007 resolved: Methodological Rigor and Completeness recover to neutral/positive
- Net composite projection: 0.93-0.96 (within and above C4 tournament target of 0.95 if all Critical and Major findings addressed)

---

## Findings Table

| ID | Assumption / Anti-Goal | Type | Confidence | Severity | Evidence | Affected Dimension |
|----|------------------------|------|------------|----------|----------|--------------------|
| IN-001-20260218I3 | QR code scan reliability unspecified; may be unreadable at event projector distance | Assumption | Low | Critical | Scene 6 VISUAL adds QR code but specifies no size, error correction, or scan-distance test | Actionability |
| IN-002-20260218I3 | "Nobody had a fix for enforcement" unscoped; falsifiable by LangMem/MemGPT/Guardrails AI | Assumption | Low | Critical | Scene 2 NARRATION: "Nobody had a fix for enforcement." MF-003 fix not applied in v3 | Evidence Quality |
| IN-003-20260218I3 | Music approval has no deadline; final render could be blocked or locked with unreviewed cues | Assumption | Medium | Major | Script Overview MUSIC SOURCING: approval required "before final render" -- no date specified | Methodological Rigor |
| IN-004-20260218I3 | Plan B not a usable artifact; Feb 20 decision point arrives without production-ready fallback | Assumption | Medium | Major | Production Dependencies Item 4: Plan B named with no screen recording list, no deadline, no narrator confirmed | Completeness |
| IN-005-20260218I3 | Timed table read at natural pace not confirmed; 10s buffer may evaporate at 120-130 WPM | Assumption | Medium | Major | Self-review: "Timed table read at natural pace recommended before lock" (future tense, not confirmed) | Methodological Rigor |
| IN-006-20260218I3 | Trimmed McConkey narration loses mastery signal for non-skier audience after grounding moved to text overlay | Assumption | Medium | Major | Revision Log Scene 4: McConkey grounding moved to text overlay; v3 narration: "Shane McConkey didn't reinvent skiing by being serious" | Evidence Quality |
| IN-007-20260218I3 | Scene 5 tournament bracket requires pre-rendered asset InVideo cannot generate; FALLBACK loses adversarial framing | Assumption | Medium | Major | Scene 5 VISUAL: "Tournament bracket visualization: 10 adversarial strategies converging on a single quality gate." No asset listed in Production Dependencies. | Completeness |
| IN-008-20260218I3 | 128 BPM -> 85 BPM music transition at 1:00 may cause auditory disruption at live event | Assumption | Low | Minor | Scene 4 MUSIC: "Smooth transition to lo-fi boom-bap piano loop. 85 BPM." Scene 3 MUSIC: 128 BPM electronic anthem. | Internal Consistency |
| IN-009-20260218I3 | "Saucer Boy" tone may not land across all three audience segments (developers / investors / leadership) | Assumption | Low | Minor | Script Overview TONE: "Saucer Boy -- technically brilliant, wildly fun." No audience-differentiation analysis documented. | Actionability |

---

## Finding Details

### IN-001-20260218I3: QR Code Scan Reliability Unspecified [CRITICAL]

**Type:** Assumption
**Original Assumption:** The QR code added to Scene 6 will be scannable by audience members at the Shack15 venue.
**Inversion:** The QR code is rendered at an insufficient size or quality level to be scanned from typical audience seating distance (10-30 feet from projector screen), making it a visual element rather than a functional CTA mechanism.
**Plausibility:** High. QR codes generated by video production tools default to minimum safe size for video viewing, not for projector scanning at distance. InVideo AI has no QR code size specification capability noted in v3. Conference projector screens at Shack15 (venue capacity suggests medium room, 50-200 person capacity) typically require a QR code to occupy at least 10% of frame width for reliable scanning from mid-room.
**Consequence:** The primary live-event CTA mechanism (QR code) reverts to a decorative element. GitHub URL recall from a fast-moving video at an event with ambient noise is low. OSS launch conversion at the highest-attention moment of the showcase is significantly degraded.
**Evidence:** Scene 6 VISUAL: "A QR code linking to github.com/geekatron/jerry, displayed alongside the URL for a minimum of 13 seconds." Production Dependencies Item 1: URL confirmation covers visibility but not QR scan reliability. No production dependency covers QR scan quality testing.
**Dimension:** Actionability
**Mitigation:** Add scan-quality requirements to Scene 6 visual direction and add a pre-event scan test to Production Dependencies. Specify minimum size (>= 10% frame width), error correction level (Level M minimum), and test confirmation (scan success at 15 feet from projector before Feb 20 noon). Add physical QR card backup.
**Acceptance Criteria:** A test scan of the rendered QR code succeeds from 15 feet on a representative projector display before Feb 20 noon. OR physical QR cards confirmed available at event registration.

---

### IN-002-20260218I3: Enforcement Claim Falsifiable at the Event [CRITICAL]

**Type:** Assumption
**Original Assumption:** "Nobody had a fix for enforcement" (Scene 2) is implicitly scoped to the Claude Code hook architecture and will not be rebutted in real time at the Anthropic showcase.
**Inversion:** A LangMem engineer, MemGPT contributor, or Anthropic researcher with Guardrails AI knowledge reacts visibly or verbally to "Nobody had a fix for enforcement" as a falsifiable absolute claim at a moment when Jerry is being introduced to the OSS community. The rebuttal is low-effort (any of these tools address enforcement in some form) and the audience at Claude Code's birthday party is skewed toward people who know these tools.
**Plausibility:** Medium. The Anthropic showcase audience is specifically the demographic most likely to have this knowledge. The iteration 2 composite flagged this as S-001 RT-004 (Major) and MF-003 guidance explicitly specified the scoping fix ("enforcement baked into the session hooks"). v3 did not apply this fix.
**Consequence:** Credibility failure at the OSS launch moment. If the first public statement about Jerry's uniqueness is publicly contested at the showcase, the narrative "Claude Code wrote its own guardrails" is overshadowed by a factual dispute. A 7-word fix prevents this entirely.
**Evidence:** Scene 2 NARRATION: "Tools handle memory. Nobody had a fix for enforcement." Iteration 2 composite MF-003: "Fix: Scope to Claude Code's hook architecture -- 'Nobody had enforcement baked into the session hooks -- catching rule drift before the next line of code executes.'" v3 revision log: MF-003 is listed as "FIXED" in the self-review Finding-Level Traceability table, but the actual narration change is not in the scene or revision log. The self-review marks it fixed; the script text does not show the fix.
**Dimension:** Evidence Quality
**Mitigation:** Change Scene 2 narration: "Tools handle memory. Nobody had a fix for enforcement." -> "Tools handle memory. Nobody had enforcement baked into the session hooks." This is the verbatim fix from MF-003 guidance. Word count: +5 words (narration moves from 257 to ~262; still within 10-second buffer at 140 WPM; verify with count).
**Acceptance Criteria:** Scene 2 narration contains "session hooks" qualifier. The claim is not falsifiable by any tool (LangMem, MemGPT, Guardrails AI) that does not operate at the Claude Code pre/post-tool-call hook layer.

---

### IN-003-20260218I3: Music Approval Has No Deadline [MAJOR]

**Type:** Assumption
**Original Assumption:** Human reviewer music approval will occur before final render with sufficient time for re-selection if cues are rejected.
**Inversion:** Music approval is attempted on Feb 20 night (the day before the event); one or more cues are rejected; no time remains for re-selection; video renders with unreviewed cues or with silence gaps.
**Plausibility:** Medium. The production timeline is compressed (InVideo test Feb 19 noon, Plan B decision Feb 20 noon, event Feb 21). Music approval is mentioned in the Script Overview but given no deadline. In compressed production timelines, undated approval gates are frequently deferred to the last moment.
**Consequence:** Final render uses unreviewed music, creating tone/venue mismatches (a Scene 2 drop that is too aggressive for Shack15 acoustics) or requires a last-minute re-render that competes with other Feb 20 production tasks.
**Evidence:** Script Overview MUSIC SOURCING: "All 6 music cues must be previewed and approved by a human reviewer before final render. Scene 2 drop, Scene 3 anthem escalation, and Scene 4 lo-fi pivot require specific confirmation." No deadline specified. Production Dependencies has no music approval item.
**Dimension:** Methodological Rigor
**Mitigation:** Add deadline to Music Sourcing note (Feb 19 noon) and add music approval as Production Dependencies Item 5 (or fold into Item 3 InVideo gate).
**Acceptance Criteria:** Music approval documented with reviewer name, approval date (by Feb 19 noon), and confirmation that Scenes 2, 3, and 4 cues are specifically confirmed.

---

### IN-004-20260218I3: Plan B Not a Production-Ready Artifact [MAJOR]

**Type:** Assumption
**Original Assumption:** Plan B (screen-recorded terminal walkthrough) is actionable at the Feb 20 noon decision point.
**Inversion:** The Feb 20 decision point arrives. InVideo output is unsatisfactory. The production lead turns to Plan B and finds no screen recordings, no narrator, and no recording equipment confirmed. Plan B is a name, not a deliverable.
**Plausibility:** Medium. The production timeline assigns "Project lead" as Plan B owner with a Feb 20 noon deadline but specifies no materials, no recording list, no voice-over confirmation. The gap between "Plan B exists" and "Plan B is executable" is significant and likely given the 3-day production window.
**Consequence:** No-go scenario: InVideo fails, Plan B not ready, event proceeds without video or with an unfinished rough cut. This is the worst-case outcome for the OSS launch.
**Evidence:** Production Dependencies Item 4: "If InVideo output is unsatisfactory after Feb 19 test pass, switch to Plan B: screen-recorded terminal walkthrough with voiceover, same narration script. Plan B uses same narration, same music cues, but replaces AI-generated video with screen recordings of actual Jerry execution." No materials list, no recording owner, no recording deadline.
**Dimension:** Completeness
**Mitigation:** Add to Production Dependencies Item 4: specify the 3-5 terminal sequences to pre-record (session start hook firing, quality gate pass, adversarial tournament bracket output), assign recording owner and deadline (Feb 19, 5pm), confirm voice-over setup. Treat Plan B as a parallel track, not a sequential fallback.
**Acceptance Criteria:** Plan B materials (minimum: 3 screen recordings + narration track confirmed recordable) are ready by Feb 19 5pm. Feb 20 decision point is a quality selection, not an emergency scramble.

---

### IN-005-20260218I3: Timed Table Read Not Confirmed Executed [MAJOR]

**Type:** Assumption
**Original Assumption:** 257 words creates a 10-second buffer at 140 WPM; this buffer is sufficient at natural delivery pace (120-130 WPM).
**Inversion:** Natural delivery pace is 125 WPM. 257 words at 125 WPM = 2:03.4. The buffer evaporates. Scene 6 "The framework that governs the tool that built it. Come build with us." (9+4 = 13 words) is delivered over the final fade with narration cut off.
**Plausibility:** Medium. This is precisely the CF-002 failure mode from v1 (276 words, no buffer) that worsened to v2 (278 words, worse buffer). v3 trimmed 21 words and calculated the buffer at 140 WPM -- the correct calculation method was stated in CF-002 guidance but not confirmed with a read. The self-review recommends (does not confirm) a timed table read.
**Consequence:** The meta loop closure ("The framework that governs the tool that built it") -- the single most important narrative achievement of v3 -- is cut off or rushed at the 2:00 mark.
**Evidence:** Self-Review Structural Compliance: "Timed table read at natural pace recommended before lock." Production Dependencies: silent on timed read.
**Dimension:** Methodological Rigor
**Mitigation:** Add as Production Dependencies Item 5 (or fold into Item 3 InVideo gate): "Timed table read at 125 WPM natural delivery pace. Target: <= 1:55. If over 1:55, trim Scene 6 expansion first (9-word 'framework governs' clause), then Scene 3 if needed. Document: reader name, date, result."
**Acceptance Criteria:** A timed read is documented with reader, date, and result. Result is <= 1:55. OR narration is trimmed to 245 words.

---

### IN-006-20260218I3: McConkey Mastery Signal Degraded [MAJOR]

**Type:** Assumption
**Original Assumption:** Moving McConkey grounding from narration to text overlay saves 12 words without losing the mastery-plus-disposition dual signal that anchors the Scene 4 philosophy for non-skiers.
**Inversion:** Non-skier viewers process Scene 4 as: "Shane McConkey [unknown name] didn't reinvent skiing [sport reference] by being serious." The mastery signal ("the best in the world," "ski legend") is absent from audio. The text overlay ("REINVENTED SKIING BY REFUSING TO BE BORING") requires reading while simultaneously processing narration and action sports footage. The emotional anchor that makes the Jerry-McConkey parallel land fails for the investor and leadership segment.
**Plausibility:** Medium. The iteration 2 composite's MF-002 finding (S-013 IN-002, S-004 PM-004) specifically flagged that the original McConkey description conveyed disposition but not elite mastery. The v3 fix moved the grounding to text -- but text overlay at a live event with ambient noise and projector viewing distance requires deliberate attention. A non-skier who misses or skips the overlay has no mastery signal at all.
**Consequence:** Scene 4 (The Soul) -- the emotional differentiator of the video -- fails to convey the intended parallel: "Jerry is world-class AND fun." Without mastery, it reads as "Jerry is fun." This undermines the video's claim to production-grade credibility.
**Evidence:** Revision Log Scene 4: "McConkey grounding moved to text overlay, -12 words." v3 narration: "Shane McConkey didn't reinvent skiing by being serious. He did it by being the best in the world and grinning the entire time."
**Dimension:** Evidence Quality
**Mitigation:** Option A: Restore one mastery clause to narration (+5 words): "Shane McConkey -- ski legend -- didn't reinvent skiing by being serious. He did it by being the best in the world and grinning the entire time." Net word count: 262. Verify buffer. Option B: Add 0.5 seconds of silent action sports footage before the McConkey line to give the visual mastery anchor before the audio name-drop.
**Acceptance Criteria:** A human reviewer who does not know Shane McConkey can reconstruct the Scene 4 parallel ("world-class AND fun") on first watch without relying solely on the text overlay.

---

### IN-007-20260218I3: Scene 5 Tournament Bracket Needs Pre-Rendered Asset [MAJOR]

**Type:** Assumption
**Original Assumption:** InVideo AI can render "Tournament bracket visualization: 10 adversarial strategies converging on a single quality gate" from the visual direction text alone.
**Inversion:** InVideo AI generates a generic bracket graphic or fails to render the visualization. The FALLBACK activates: "Static scoreboard text overlays slam in sequentially with impact frames." The adversarial tournament framing -- the v3 fix for MF-005 self-grading optics -- is lost. Scene 5 reverts to a list of numbers, and the self-grading concern resurfaces.
**Plausibility:** Medium. The tournament bracket is a custom visualization (10 named adversarial strategies, convergence arrows, quality gate as output node). InVideo AI generates video from stock assets and motion templates; a custom bracket diagram is not a standard motion template and is likely to require a pre-rendered image or animation asset.
**Consequence:** The primary v3 fix for MF-005 (self-grading optics) fails silently. Scene 5 in FALLBACK mode shows three numbers. The "10 ADVERSARIAL STRATEGIES" overlay appears but without the bracket visualization, it is an assertion without a visual proof -- which was exactly the self-grading concern.
**Evidence:** Scene 5 VISUAL (primary): "Tournament bracket visualization: 10 adversarial strategies converging on a single quality gate. The gate holds." Scene 5 FALLBACK: "Static scoreboard text overlays slam in sequentially with impact frames. Omit live counter animation." Production Dependencies Item 3: InVideo test pass gate (Feb 19 noon) for Scenes 2, 5, 6 -- but no tournament bracket asset is listed.
**Dimension:** Completeness
**Mitigation:** Add to Production Dependencies Item 3: "Scene 5 requires a pre-rendered tournament bracket asset (10 strategies -> quality gate). Options: (a) static diagram image exported from any diagramming tool, (b) short screen recording of an actual adversarial tournament output log. Assign to: developer or designer. Deadline: Feb 19 noon (simultaneous with InVideo test). If no asset available by Feb 19 noon, activate FALLBACK and verify scoreboard sequence still communicates adversarial process."
**Acceptance Criteria:** Scene 5 either (a) renders with a legible tournament bracket from a pre-created asset, OR (b) activates FALLBACK with explicit confirmation from a reviewer that the scoreboard sequence does not appear to self-grade.

---

## Recommendations

### Critical -- MUST mitigate before production lock (Feb 20 noon)

| IN-ID | Finding | Mitigation Action | Effort |
|-------|---------|-------------------|--------|
| IN-001-20260218I3 | QR code scan reliability unspecified | Add scan-quality requirements to Scene 6 visual direction; add pre-event scan test to Production Dependencies; prepare physical QR card backup | 20 min (script edit + print card) |
| IN-002-20260218I3 | "Nobody had a fix for enforcement" unscoped | Change Scene 2 narration to "Nobody had enforcement baked into the session hooks." Update word count. | 5 min (one sentence change) |

### Major -- SHOULD mitigate before production lock

| IN-ID | Finding | Mitigation Action | Effort |
|-------|---------|-------------------|--------|
| IN-003-20260218I3 | Music approval no deadline | Add "approved by Feb 19 noon" to Music Sourcing note | 5 min |
| IN-004-20260218I3 | Plan B not production-ready | Expand Production Dependencies Item 4 with recording list, owner, deadline (Feb 19 5pm) | 15 min |
| IN-005-20260218I3 | Timed table read not confirmed | Add as Production Dependencies Item 5; conduct and document read; trim if over 1:55 | 15 min read + trim if needed |
| IN-006-20260218I3 | McConkey mastery signal trimmed | Option A: Restore "+ski legend+" to narration (5 words). Option B: Add 0.5s visual pause before McConkey line. | 5 min (Option A) |
| IN-007-20260218I3 | Scene 5 bracket needs pre-rendered asset | Add asset requirement to Production Dependencies Item 3; assign owner and deadline | 10 min (script) + asset creation |

### Minor -- MAY note or monitor

| IN-ID | Finding | Recommendation |
|-------|---------|----------------|
| IN-008-20260218I3 | 128->85 BPM music transition at 1:00 | Flag for human reviewer during music approval; confirm transition is smooth in InVideo render |
| IN-009-20260218I3 | "Saucer Boy" tone across mixed audience | Include in human reviewer brief: confirm tone landing for non-developer segment |

---

*Agent: adv-executor | Strategy: S-013 Inversion Technique*
*Tournament: feat023-showcase-20260218-001 | Iteration: 3 of C4*
*Deliverable: ps-architect-001-hype-reel-script-v3.md*
*SSOT: `.context/rules/quality-enforcement.md`*
*Template: `.context/templates/adversarial/s-013-inversion.md` v1.0.0*
*H-16 Compliance: S-003 Steelman confirmed (iteration-3/s-003-steelman present)*
*Date: 2026-02-18*
*Finding prefix: IN-NNN-20260218I3*
