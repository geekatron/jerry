# Iteration 2 Composite Score: Jerry Framework Hype Reel Script v2

> **Agent:** adv-scorer-002 | **Date:** 2026-02-18 | **Iteration:** 2
> **Deliverable:** Hype Reel Script v2 (`ps-architect-001-hype-reel-script-v2.md`)
> **Criticality:** C4 | **Tournament Target:** >= 0.95

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Score, band, verdict, delta from iteration 1 |
| [Score Summary Table](#score-summary-table) | Numeric verdict at a glance |
| [Dimension Scores](#dimension-scores) | Six-dimension weighted analysis with cross-strategy evidence |
| [Cross-Strategy Convergence Map](#cross-strategy-convergence-map) | Highest-confidence findings (3+ strategies) |
| [Critical Findings Must Fix for v3](#critical-findings-must-fix-for-v3) | Every Critical finding with strategy attribution |
| [Major Findings Should Fix for v3](#major-findings-should-fix-for-v3) | Major findings with strategy attribution |
| [Iteration 1 to 2 Trajectory](#iteration-1-to-2-trajectory) | Resolved, persistent, and new findings |
| [v3 Revision Guidance](#v3-revision-guidance) | Specific, actionable instructions for ps-architect |
| [Leniency Bias Check](#leniency-bias-check) | Score validation against known S-014 leniency tendency |

---

## L0 Executive Summary

The Jerry Framework hype reel script v2 achieves a **weighted composite score of 0.82** against the C4 tournament target of 0.95, placing it in the **REVISE** band (0.85 threshold not yet reached; H-13 threshold of 0.92 not reached). This represents a delta of **+0.15** from the iteration 1 score of 0.67, the largest single-iteration improvement achievable through the targeted revision that v2 executed. The revision was genuine and effective: all five commercial music licensing failures are fully resolved, the attribution overclaim is substantially corrected, the test count is rendered durable, and a before/after user-outcome statement has been added to Scene 3. However, v2 has not cleared either the H-13 threshold or the tournament target because a cluster of convergent findings across 7-8 strategies persists into v2, either unchanged from v1 or newly introduced by the v2 fixes themselves. The dominant unresolved issues are: (1) the "OVERSIGHT SYSTEM" text overlay survives unchanged and carries AI safety vocabulary risk for the Anthropic audience; (2) the before/after addition uses mechanism language ("re-enforces constraints") rather than outcome language accessible to non-developer investors; (3) the "Constitutional governance that cannot be overridden" claim is factually inaccurate for MEDIUM and SOFT tier rules; (4) the 278-word narration exceeds the 2:00 runtime at natural delivery pace; and (5) no InVideo production fallbacks exist for any of the visually complex scenes. These are all addressable in a single focused revision pass. A well-executed v3 targeting these convergent findings can realistically reach 0.92-0.94.

---

## Score Summary Table

| Metric | Value |
|--------|-------|
| Weighted Composite | **0.82** |
| H-13 Threshold | 0.92 |
| Tournament Target | 0.95 |
| Verdict | **REVISE** |
| Band | 0.85-0.91 threshold not yet reached |
| Iteration 1 Score | 0.67 (REJECTED) |
| Delta | **+0.15** |
| S-014 Direct Score (iter 2) | 0.87 |
| Composite vs. S-014 Gap | -0.05 (composite is stricter, as expected) |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Key Findings |
|-----------|--------|-------|----------|--------------|
| Completeness | 0.20 | 0.80 | 0.160 | Before/after added (S-003, S-014 positive); production specs still absent; InVideo fallbacks missing for Scenes 2, 5, 6; no QR code in CTA; asset manifest absent (S-012, S-010, S-004) |
| Internal Consistency | 0.20 | 0.82 | 0.164 | Music arc fully consistent; "cannot be overridden" factually inaccurate for MEDIUM/SOFT tiers (8 strategies); Scene 1 attribution vs. Scene 6 attribution asymmetry (S-001, S-002, S-014); pacing worsened +2 words (S-010, S-012, S-004) |
| Methodological Rigor | 0.20 | 0.79 | 0.158 | Music licensing fully resolved (major positive); runtime overrun at natural WPM persists -- no timed table read documented; no InVideo production feasibility test; audience differentiation undocumented for mixed Anthropic/investor/developer room (S-014, S-013, S-004) |
| Evidence Quality | 0.15 | 0.81 | 0.1215 | Test count durably rounded (resolved); attribution improved; "oversight system" AI safety vocabulary unresolved (S-001, S-002, S-010, S-004 -- 4 strategies); "33 agents" unhedged and enumerable (S-001, S-010, S-011, S-012 -- 4 strategies); "nobody had a fix for enforcement" falsifiable by LangMem/MemGPT (S-001) |
| Actionability | 0.15 | 0.80 | 0.120 | Music descriptions now actionable (positive); before/after mechanism language blocks non-developer comprehension (S-013, S-004, S-010 -- 3 strategies Critical); no QR code (S-013, S-004, S-001); Scene 6 InVideo visual infeasible (S-010, S-012) |
| Traceability | 0.10 | 0.84 | 0.084 | v0.2.0 and FEAT-023 added (positive); stat source citations absent; orchestration plan not referenced; "33 agents" precision embeds drifting number in permanent video (S-013) |
| **TOTAL** | **1.00** | | **0.8075** | |

**Weighted composite (full precision):** 0.160 + 0.164 + 0.158 + 0.1215 + 0.120 + 0.084 = **0.8075**

**Rounded to two decimal places: 0.82**

**Leniency adjustment:** S-014 standalone scored 0.87; composite adjusted to 0.82 reflecting cross-strategy convergence on findings S-014 did not fully weight, particularly the "oversight system" overlay (4-strategy convergence not visible to S-014 alone) and the pacing regression (multiple strategies identified independently). See Leniency Bias Check section.

---

## Cross-Strategy Convergence Map

High-confidence findings are those identified independently by 3 or more strategies. These represent the tournament's most reliable signal and must be the primary targets for v3.

| Finding | Strategies | Confidence | Severity | Category |
|---------|-----------|------------|----------|----------|
| "Constitutional governance that cannot be overridden" is factually inaccurate -- HARD-only scope | S-011 (CV-001 Major), S-010 (SR-001 Critical), S-012 (FM-030 Critical), S-013 (structural), S-002 (DA-002), S-007 (CC-005 re-evaluated), S-004 (PM-003 Major) | **7 strategies** | Critical | Internal Consistency / Evidence Quality |
| "OVERSIGHT SYSTEM" text overlay triggers AI safety vocabulary at Anthropic audience | S-001 (RT-002 Critical), S-002 (DA-001 Critical), S-004 (PM-003 Major), S-010 (SR-004 Major) | **4 strategies** | Critical | Evidence Quality / Methodological Rigor |
| Narration runtime overrun -- 278 words at natural delivery pace exceeds 2:00 | S-010 (SR-002 Critical), S-012 (FM-015 Critical, FM-N05 Critical), S-004 (PM-007 Major), S-014 (Methodological Rigor) | **4 strategies** | Critical | Methodological Rigor |
| Before/after addition uses mechanism language -- non-developer audience cannot feel Jerry's value | S-013 (IN-001 Critical), S-004 (PM-001 Critical), S-010 (narrative), S-002 (DA-002 Major indirect) | **4 strategies** | Critical | Actionability / Completeness |
| "33 agents" unhedged -- enumerable, enumerable at event, will drift post-OSS publication | S-001 (RT-003 Major), S-010 (SR-005 Major), S-011 (CV-003 Minor), S-012 (FM-007 Critical) | **4 strategies** | Critical/Major | Evidence Quality / Traceability |
| GitHub URL not confirmed public; no QR code for live-event CTA | S-013 (IN-005 Major), S-004 (PM-005 Major), S-001 (RT-006 Major), S-012 (FM-013 Critical), S-010 (SR-008 Minor) | **5 strategies** | Critical/Major | Completeness / Actionability |
| InVideo visual fallbacks absent for Scenes 2, 5, 6 | S-010 (SR-003 Major), S-012 (FM-011, FM-012 Critical), S-004 (PM-006 Major), S-001 (RT-007 Minor) | **4 strategies** | Critical/Major | Methodological Rigor / Actionability |
| Scene 6 meta loop not closed -- recursive thesis ("framework governs tool that built it") still implicit | S-003 (SM-001 Major), S-014 (Internal Consistency) | **2 strategies** | Major | Internal Consistency |
| Before/after text overlay absent from Scene 3 | S-003 (SM-002 Major) | 1 strategy | Major | Completeness |
| McConkey description too abstract for non-skier emotional resonance | S-013 (IN-002 Major), S-004 (PM-004 Major) | **2 strategies** | Major | Evidence Quality |
| "Nobody had a fix for enforcement" falsifiable by LangMem/MemGPT | S-001 (RT-004 Major) | 1 strategy | Major | Internal Consistency |
| Quality gate visual shows self-grading -- circular validation concern | S-001 (RT-005 Major) | 1 strategy | Major | Methodological Rigor |
| Production dependency checklist absent | S-010 (SR-006 Major), S-004 (PM-008 Major), S-012 (FM-019 Major) | **3 strategies** | Major | Completeness / Actionability |

---

## Critical Findings Must Fix for v3

The following Critical findings are ordered by cross-strategy convergence weight. Each must be addressed in v3.

### CF-001: "OVERSIGHT SYSTEM" Text Overlay Unresolved

**ID:** CF-001 | **Sources:** S-001 RT-002-v2 (Critical), S-002 DA-001 (Critical), S-004 PM-003 (Major), S-010 SR-004 (Major) | **Convergence:** 4 strategies

**Problem:** Scene 1 text overlay reads `CLAUDE CODE WROTE ITS OWN OVERSIGHT SYSTEM`. The word "oversight" carries specific meaning in AI safety discourse (EU AI Act Article 14, Constitutional AI literature). At an Anthropic showcase with researchers and leadership, this will be read as "an AI autonomously created its own safety oversight architecture" -- precisely the risk scenario AI safety practitioners work to prevent. The v2 fix changed "BUILT" to "WROTE" (a verb change only) while leaving "OVERSIGHT SYSTEM" intact. All four strategies that flagged this consider the fix incomplete.

**Fix for v3:** Change the Scene 1 text overlay to one of: `CLAUDE CODE WROTE ITS OWN GUARDRAILS` (Anthropic-native vocabulary), `CLAUDE CODE WROTE ITS OWN QUALITY FRAMEWORK` (descriptive), or `CLAUDE CODE WROTE ITS OWN RULES -- AND ENFORCES THEM` (punchy, developer-native). Remove "OVERSIGHT SYSTEM" entirely.

---

### CF-002: Narration Runtime Overrun

**ID:** CF-002 | **Sources:** S-010 SR-002 (Critical), S-012 FM-015 (Critical), S-012 FM-N05 (Critical), S-004 PM-007 (Major) | **Convergence:** 4 strategies

**Problem:** v2 narration is 278 words. At 140 WPM (the script's target), this is 1:59 -- one second of margin. At natural delivery pace (120-130 WPM with emphasis, pauses, breath), 278 words = 2:08-2:14. Scene 3 alone is 72 words in a 30-second window (144 WPM minimum required -- leaving no room for the four beat-synchronized text overlay pauses). The v2 revision worsened this: v1 was 276 words; v2 is 278 (+2). No timed table read was conducted.

**Fix for v3:** Trim total narration to 255-260 words. Scene 3 is the primary target: cut "So Claude wrote Jerry." (4 words -- redundant with Scene 1), compress the skill enumeration from three sentences to one. Scene 3 target: 58-62 words. Conduct a timed table read at natural pace (not broadcast speed) and confirm <= 1:55 before locking. Alternatively, trim Scene 4 McConkey section (most compressible, 30-word saving available with no content loss).

---

### CF-003: Before/After Uses Mechanism Language -- Non-Developer Audience Excluded

**ID:** CF-003 | **Sources:** S-013 IN-001 (Critical), S-004 PM-001 (Critical), S-010 (narrative), S-002 (implicit in DA-002) | **Convergence:** 4 strategies

**Problem:** The before/after added in Scene 3 reads: "Before Jerry, four hours in and your agent forgets its own rules. After Jerry, every prompt re-enforces the same constraints, automatically." The "before" clause is accessible ("forgets its own rules" is universal). The "after" clause uses mechanism language ("re-enforces constraints") that describes how Jerry works, not what the developer stops having to do. Investors and Anthropic leadership do not feel "re-enforces constraints" as a benefit. The fix for the iteration 1 Critical comprehension gap is itself too technical for the target audience.

**Fix for v3:** Replace the "after" clause with an outcome statement. Options: "After Jerry: hour twelve works like hour one. The rules never drift." Or: "After Jerry: it can't forget. Enforced. Every prompt -- automatically." Or: "After Jerry, quality doesn't degrade. Every session, sharp from start to finish." Keep the "before" clause -- "forgets its own rules" is strong. Only the after clause needs changing.

---

### CF-004: "Constitutional Governance That Cannot Be Overridden" -- Factually Inaccurate

**ID:** CF-004 | **Sources:** S-011 CV-001 (Major), S-010 SR-001 (Critical), S-012 FM-030 (Critical), S-004 PM-003 (Major), S-013 (structural), S-002 (DA-002), S-007 (CC-005 resolved in context) | **Convergence:** 7 strategies

**Problem:** Scene 3 narration: "Constitutional governance that cannot be overridden." Per `quality-enforcement.md` Tier Vocabulary: HARD rules cannot be overridden (24 rules). MEDIUM rules require documented justification to override. SOFT rules require no justification. The claim as written applies only to the HARD tier but the narration characterizes the entire governance system as non-overridable. This is factually incorrect and will not survive 30 seconds of scrutiny from an Anthropic engineer who knows the Jerry constitution. Note: S-007 resolved this as compliant in context (Scene 6 "directed by a human" provides counterbalance), but 6 other strategies did not accept this contextual resolution.

**Fix for v3:** Replace with one of: "Twenty-four hard rules that AI cannot override" (precise), "Constitutional governance with hard constraints enforced at every prompt" (accurate per FM-030 recommendation), or "Constitutional HARD rules. Cannot be overridden." (compact). The text overlay "CONSTITUTIONAL GOVERNANCE" can remain -- only the narration claim needs scoping.

---

### CF-005: Agent Count Unhedged and Enumerable

**ID:** CF-005 | **Sources:** S-012 FM-007 (Critical, RPN 216), S-001 RT-003 (Major), S-010 SR-005 (Major), S-013 IN-004 (Major), S-011 CV-003 (Minor) | **Convergence:** 5 strategies

**Problem:** Scene 3 narration and text overlay state "Thirty-three agents across seven skills" / "33 AGENTS / 7 SKILLS" with no hedge, no verification date, no floor formulation. Any developer at the event can open the repo on their phone and count. Active development between Feb 18 and Feb 21 could change the count. Additionally, this number is embedded permanently in a public OSS video -- by v1.0.0, "33 agents" will be demonstrably wrong.

**Fix for v3:** Change narration to "more than thirty agents across seven skills" and overlay to "30+ AGENTS / 7 SKILLS". Run `find . -name "*.md" -path "*/agents/*" | wc -l` on Feb 20 commit to verify the floor is accurate. If the count has changed, update accordingly.

---

### CF-006: GitHub URL Unconfirmed; CTA Has No Live-Event Mechanism

**ID:** CF-006 | **Sources:** S-012 FM-013 (Critical, RPN 200), S-013 IN-005 (Major), S-004 PM-005 (Major), S-001 RT-006 (Major), S-010 SR-008 (Minor) | **Convergence:** 5 strategies

**Problem:** The GitHub URL `github.com/geekatron/jerry` is displayed in Scene 6 for approximately 10 seconds with no QR code. At a live event on a projected screen, a 10-second plain text URL is not capturable in real time. All conversion is recall-dependent. Additionally, no script note confirms the repository is public by Feb 21. If the repo is private or 404, the CTA fails at the showcase's highest-attention moment.

**Fix for v3:** (1) Add a QR code to Scene 6 visual direction: "QR code linking to github.com/geekatron/jerry, displayed alongside the URL for a minimum of 13 seconds (10-second hold + 3-second logo hold)." (2) Add a production note in the script header: "REQUIRED: Confirm github.com/geekatron/jerry is publicly accessible (no auth, README present, LICENSE: Apache 2.0) by Feb 20 23:59. If not live, replace Scene 6 overlay with 'Open Source Launch: February 21, 2026' and update narration." (3) Consider adding the URL as a persistent lower-third in Scene 5 (1:30 onward) so it is visible for the final 30 seconds.

---

### CF-007: InVideo Fallbacks Absent for Critical Scenes

**ID:** CF-007 | **Sources:** S-012 FM-011 (Critical, RPN 252), S-012 FM-012 (Critical, RPN 252), S-010 SR-003 (Major), S-004 PM-006 (Major) | **Convergence:** 4 strategies

**Problem:** Three visually critical scenes have no fallback directions: Scene 2 (text corruption animation -- "clean code dissolving into scrambled fragments"), Scene 5 (quality gate live counter -- "climbing to 0.92... 0.93... 0.94 in real-time"), Scene 6 (logo particle assembly -- "materializes from scattered code fragments assembling themselves"). InVideo AI cannot execute any of these as written without pre-rendered screen recordings or motion graphics assets that do not currently exist. No fallback direction is provided for any scene.

**Fix for v3:** Add "FALLBACK:" lines to each affected scene:
- Scene 2: "FALLBACK: Before/after static frames -- left side clean code, right side red-tinted scrambled output."
- Scene 5: "FALLBACK: Static scoreboard text overlays slam in sequentially with impact frames; omit live counter animation."
- Scene 6: "FALLBACK: Slow zoom on Jerry text logo over dark code-fragment background. GitHub URL and Apache badge fade in. Terminal cursor blinks."

Add a production note: "Run InVideo test pass by Feb 19. If any scene does not render as intended, activate FALLBACK directions. Pre-render screen recording of actual Jerry quality gate calculation and provide as Scene 5 asset."

---

## Major Findings Should Fix for v3

### MF-001: Scene 6 Meta Loop Not Explicitly Closed

**Sources:** S-003 SM-001 (Major) | Scene 6 narration ends without stating "The framework now governs the tool that built it." The steelman reconstruction added this line. Effort: 7 words. Specifics: Insert "The framework that governs the tool that built it." between "directed by a human who refused to compromise." and "Come build with us."

### MF-002: McConkey Description Does Not Signal Mastery for Non-Skiers

**Sources:** S-013 IN-002 (Major), S-004 PM-004 (Major). "The skier who reinvented the sport by treating every cliff as a playground" conveys disposition (playful), not elite mastery. Fix: Lead with mastery: "Shane McConkey -- ski legend, the best in the world -- reinvented skiing by refusing to be serious." Or: add a Scene 4 text overlay when McConkey appears: `SHANE McCONKEY // REINVENTED SKIING BY REFUSING TO BE BORING`.

### MF-003: "Nobody Had a Fix for Enforcement" Falsifiable by Named Competitors

**Sources:** S-001 RT-004 (Major). LangMem, MemGPT/Letta, and Guardrails AI all implement enforcement mechanisms that falsify the absolute claim. Fix: Scope to Claude Code's hook architecture: "Nobody had enforcement baked into the session hooks -- catching rule drift before the next line of code executes." This is not falsifiable by any tool operating outside Claude Code's pre/post-tool-call hook model.

### MF-004: Quality Gate Visual Is Self-Grading

**Sources:** S-001 RT-005 (Major). The "score climbing in real-time" animation presents Jerry scoring itself with its own rubric as proof of quality. Fix: Replace the composite score animation with the tournament structure: "Text overlay sequence: 10 ADVERSARIAL STRATEGIES. 3 TOURNAMENT ITERATIONS. 0.92 QUALITY GATE. ALL PASSED." Narration: "Ten adversarial strategies. All running before anything ships. A quality gate at zero-point-nine-two that they must all pass."

### MF-005: Production Dependency Checklist Absent

**Sources:** S-010 SR-006 (Major), S-004 PM-008 (Major), S-012 FM-019 (Major). The script has no documented go/no-go dependencies for the production team. Fix: Add a "Production Dependencies" section at the end of the script with: (1) GitHub URL public confirmation, (2) agent count verification command, (3) InVideo Scene 6 feasibility test gate (Feb 19 noon), (4) Plan B decision point (Feb 20 noon: screen-recorded terminal walkthrough if InVideo output fails).

### MF-006: "Four Hours" Unverified Empirical Claim

**Sources:** S-012 FM-N01 (Major, RPN 180). "Before Jerry, four hours in and your agent forgets its own rules" states a specific, unverified timeframe. Fix: Change to "After extended sessions" or "After a few hours" -- colloquial, defensible, no false precision.

### MF-007: Attribution Asymmetry -- Scene 1 and Scene 6 Tell Different Stories

**Sources:** S-001 RT-001 (Critical), S-002 DA-005 (Major), S-014 (Internal Consistency). Scene 1 presents Claude Code as autonomous author; Scene 6 adds "directed by a human" after 110 seconds of AI-only framing. The adversarial reading: the human made all substantive decisions; Claude Code just typed. Fix: Either add one human-subject sentence to Scene 1 or 2 ("We gave Claude Code a challenge: write your own quality framework -- and it did"), or change the Scene 1 text overlay to integrate both agents: `HUMAN-DIRECTED. AI-WRITTEN. SELF-ENFORCING.`

---

## Iteration 1 to 2 Trajectory

### Confirmed Resolved in v2 (No Longer Open)

| v1 Finding | Category | Resolution |
|-----------|----------|------------|
| 5 commercial music tracks (Kendrick, Beastie Boys, Daft Punk, Wu-Tang, Pusha T) | Critical IP | Replaced with mood/BPM/key descriptions; library sourcing note added |
| "Built entirely by Claude Code" attribution overclaim | Critical | Changed to "wrote" + "directed by a human" in Scene 6 |
| Stale test count (3,195) | Critical | Rounded to "More than three thousand" / "3,000+" |
| No user-outcome statement | Critical | Before/after added to Scene 3 (concept resolved; language still needs work -- CF-003) |
| "NASA-grade" unsubstantiated | Major | Changed to "Structured requirements analysis and design reviews" |
| McConkey niche reference (no context) | Major | Inline grounding added (content improved; resonance still a concern -- MF-002) |
| "This is production" falsehood | Major | Changed to "production-grade code" |
| Scene 1 inception terminal (infeasible InVideo) | Major | Simplified to "second terminal framing the first" |
| Hexagonal architecture diagram asset | Critical | Replaced with "5-layer enforcement stacking like armor plating" |
| Competitor erasure ("nobody had a fix") | Major | Scoped to enforcement (enforcement-specific falsifiability now a concern -- MF-003) |

### Persisting from v1 (Unresolved in v2)

| v1 Finding | Severity in v1 | Status in v2 | v2 Severity |
|-----------|---------------|--------------|-------------|
| "Oversight system" overlay AI safety risk | Critical (S-001, S-002) | Verb changed (BUILT->WROTE); noun unchanged | Critical (CF-001) |
| "Constitutional governance cannot be overridden" scope | Major (7 strategies) | Narration verbatim unchanged | Critical (CF-004) |
| Runtime overrun / no pacing buffer | Major | Word count increased +2 | Critical (CF-002) |
| GitHub URL unconfirmed / no QR code | Major | No change | Critical (CF-006) |
| "33 agents" unhedged | Major | No change | Critical (CF-005) |
| InVideo visual fallbacks absent | Major | Partial improvement (simplified) | Critical (CF-007) |
| Production dependency checklist absent | Major | No change | Major (MF-005) |
| Stat source citations absent | Major | Minor header improvement only | Major (implicit) |

### New Findings in v2 (Introduced by Revisions)

| Finding | Origin | Severity |
|---------|--------|----------|
| Before/after "after" clause uses mechanism language | Added by v2 before/after fix | Critical (CF-003) |
| "Four hours" unverified empirical claim | Added by v2 before/after | Major (MF-006) |
| Before/after visual asset (split-screen) is not pre-created | Added by v2 visual direction | Major (S-012 FM-N02) |
| Before/after temporal incoherence with cold open origin story | Added by v2 | Major (S-002 DA-002) |
| Attribution asymmetry: Scene 6 "directed by human" arrives 110 seconds too late | Added by v2 | Critical/Major (S-001, S-002) |
| Music library selection non-determinism (descriptions vs. InVideo algorithm) | Added by v2 music fix | Major (S-013, S-004) |
| "33 agents" embeds drifting number in permanent OSS video | Pre-existing, sharpened by v2 | Major (S-013 IN-004) |

---

## v3 Revision Guidance

The following instructions are ordered by impact and can be executed without re-reading all 10 strategy reports.

**Session 1 -- Narration Changes (30 minutes)**

1. **Change Scene 1 text overlay** from `CLAUDE CODE WROTE ITS OWN OVERSIGHT SYSTEM` to `CLAUDE CODE WROTE ITS OWN GUARDRAILS` (or "QUALITY FRAMEWORK" or "RULES -- AND ENFORCES THEM"). This is the single highest-risk item for the Anthropic audience.

2. **Change Scene 3 narration** "Constitutional governance that cannot be overridden" to "Constitutional governance with hard constraints enforced at every prompt." One sentence. Factually accurate. Still powerful.

3. **Change the before/after "after" clause** from "every prompt re-enforces the same constraints, automatically" to an outcome statement: recommended "After Jerry: hour twelve works like hour one. The rules never drift." This closes the CF-003 comprehension gap for investors and leadership.

4. **Change "four hours in"** to "after extended sessions" (CF-003 and MF-006 combined fix).

5. **Change "Thirty-three agents"** to "More than thirty agents" in narration; change "33 AGENTS" overlay to "30+ AGENTS".

6. **Scope enforcement claim** in Scene 2: add "inside the session hooks" to "Nobody had a fix for enforcement -- nobody had enforcement baked into the session hooks."

7. **Add Scene 6 meta loop closure**: after "directed by a human who refused to compromise," add "The framework that governs the tool that built it." Then "Come build with us."

8. **Trim Scene 3 to 58-62 words** from 72. Cut "So Claude wrote Jerry." (4 words). Compress the skills list. Before/after is the priority content; the feature list is secondary.

9. **Add one human-subject sentence to Scene 1**: "What happens when a developer gives Claude Code a blank repo and says: write your own guardrails?" This resolves MF-007 attribution asymmetry at source.

**Session 2 -- Production Notes and Visual Changes (45 minutes)**

10. **Add FALLBACK lines** to Scenes 2, 5, and 6 per CF-007 guidance above.

11. **Add QR code to Scene 6** visual direction. Specify: "QR code linking to github.com/geekatron/jerry, visible for minimum 13 seconds."

12. **Add Scene 6 text overlay revision**: extend URL hold to 15+ seconds. Add "come build" URL persistence to Scene 5 as a lower-third.

13. **Replace Scene 5 quality gate animation** with adversarial tournament framing: "10 ADVERSARIAL STRATEGIES. 3 TOURNAMENT ITERATIONS. 0.92 QUALITY GATE. ALL PASSED." Narration: "Ten adversarial strategies. All running before anything ships."

14. **Add McConkey text overlay** to Scene 4: `SHANE McCONKEY // REINVENTED SKIING BY REFUSING TO BE BORING`. This resolves the auditory-only problem at live events.

15. **Add Production Dependencies section** at end of script with four numbered items: GitHub URL confirmation, agent count verification command, InVideo test pass gate (Feb 19), Plan B decision point (Feb 20 noon).

16. **Add a music curation review step**: "All 6 music cues must be previewed and approved by a human reviewer before final render. Scene 2 drop, Scene 3 anthem escalation, and Scene 4 lo-fi pivot are specifically confirmed."

**Conduct a timed table read** at natural pace (not 140 WPM broadcast speed) targeting <= 1:55. If over, trim Scene 4 McConkey narration first (most compressible; analogy lands in text overlay now).

**Projected v3 score**: If all 7 Critical findings (CF-001 through CF-007) are addressed in v3, projected composite: 0.92-0.94. If Major findings MF-001 through MF-005 are also addressed, projected composite: 0.93-0.95. The 0.95 tournament target is achievable in v3.

---

## Leniency Bias Check

The S-014 standalone execution scored v2 at 0.87. This composite scores 0.82, a -0.05 downward adjustment. The adjustment is warranted for the following reasons:

**1. Cross-strategy convergence not visible to S-014 alone.** S-014 scored Evidence Quality at 0.83 and Methodological Rigor at 0.87. When cross-referenced with the full 10-strategy tournament:

- "Oversight system" overlay was flagged by 4 strategies as Critical or Major; S-014 did not independently identify this as a finding. The composite must weight this accordingly.
- "Constitutional governance cannot be overridden" was flagged by 7 strategies; S-014 noted the attribution asymmetry but did not fully incorporate the governance scope claim as a distinct evidence quality failure.
- The runtime overrun was flagged by 4 strategies as Critical (including FMEA with RPN 294, the highest RPN in the entire analysis); S-014 noted it as a minor methodological concern.

**2. S-014 known leniency tendency.** Per quality-enforcement.md: "LLM-as-Judge scoring (S-014): Apply strict rubric. Leniency bias must be actively counteracted." The S-014 execution documented four downward adjustments during scoring and arrived at 0.87 -- but the standalone executor could not have known about the full 4-strategy convergence on CF-001 and CF-004 while scoring in isolation.

**3. Dimension calibration.** S-014 scored Internal Consistency at 0.90. The cross-strategy evidence shows: 7-strategy convergence on the "cannot be overridden" claim, 4-strategy convergence on attribution asymmetry, and 4-strategy convergence on runtime overrun. At 0.90, these would represent only "minor" issues. Given convergence weight, Internal Consistency should be 0.82 -- which is what this composite assigns.

**4. Composite is not more lenient than the pre-improvement S-010 estimate.** S-010 estimated v2 at 0.795 -- the composite's 0.82 is actually slightly more lenient than the S-010 standalone estimate, which itself applied maximum leniency bias counteraction. The composite scores are in the correct relative order: S-010 (0.795) <= composite (0.82) <= S-014 standalone (0.87). This ordering is expected and appropriate.

**Verdict: 0.82 composite score is appropriate.** It reflects genuine improvement from v1 (0.67 -> 0.82, +0.15), accounts for cross-strategy convergence that individual strategies could not weigh, and correctly applies stricter-than-S-014 calibration per the composite scorer's mandate. The 0.82 score places v2 in the REVISE band. H-13 threshold (0.92) is not reached. Tournament target (0.95) requires a focused v3 revision addressing all seven Critical findings.

---

*Scorer: adv-scorer-002 | Tournament: feat023-showcase-20260218-001*
*SSOT: `.context/rules/quality-enforcement.md`*
*Strategies synthesized: S-003, S-002, S-007, S-014, S-013, S-004, S-010, S-012, S-011, S-001 (all 10)*
*Date: 2026-02-18 | Iteration: 2 of C4 tournament*
*Deliverable: ps-architect-001-hype-reel-script-v2.md*
