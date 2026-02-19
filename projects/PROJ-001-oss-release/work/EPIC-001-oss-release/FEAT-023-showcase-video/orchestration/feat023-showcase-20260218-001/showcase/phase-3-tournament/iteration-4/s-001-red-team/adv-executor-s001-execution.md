# Red Team Report: Jerry Framework Hype Reel Script v4

**Strategy:** S-001 Red Team Analysis
**Deliverable:** `projects/PROJ-001-oss-release/work/EPIC-001-oss-release/FEAT-023-showcase-video/orchestration/feat023-showcase-20260218-001/showcase/phase-3-tournament/iteration-4/ps-architect-001-hype-reel-script-v4.md`
**Criticality:** C4
**Date:** 2026-02-18
**Reviewer:** adv-executor (S-001 execution) | Tournament: feat023-showcase-20260218-001
**H-16 Compliance:** S-003 Steelman applied in iteration 2 (`iteration-2/s-003-steelman/adv-executor-s003-execution.md`, 2026-02-18, confirmed). v4 is a direct revision of v3 incorporating all iter-3 composite revision guidance. H-16 is satisfied: the deliverable was strengthened before adversarial emulation began.
**Threat Actors:** Four distinct adversary profiles retained from iteration-3 execution. v4 has closed the majority of prior attack vectors; this execution focuses adversarial pressure on residual surfaces and new vectors exposed by v4-specific changes.
**SSOT:** `.context/rules/quality-enforcement.md`

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Step 1: Threat Actor Profiles](#step-1-threat-actor-profiles) | Four adversary definitions with goals, capabilities, motivations |
| [Step 2: Attack Vector Inventory](#step-2-attack-vector-inventory) | Findings table with RT-NNN identifiers |
| [Step 3: Defense Gap Assessment](#step-3-defense-gap-assessment) | Existing defenses and prioritization matrix |
| [Step 4: Countermeasures](#step-4-countermeasures) | Concrete mitigations for P0 and P1 findings |
| [Step 5: Scoring Impact](#step-5-scoring-impact) | Dimension impact map and overall assessment |
| [Summary](#summary) | Overall verdict |

---

## Step 1: Threat Actor Profiles

The same four adversary profiles from iteration-3 apply. v4's changes are assessed against each profile to identify whether prior mitigations fully close the attack surface or introduce new vulnerabilities.

### Threat Actor A: AI Safety Researcher at Anthropic

| Field | Profile |
|-------|---------|
| **Goal** | Identify any AI-capability framing that could embarrass Anthropic, misrepresent safety properties of Claude Code, or signal misalignment between how Anthropic describes AI oversight and how the video portrays autonomous AI behavior |
| **Capability** | Deep fluency in AI safety vocabulary; knows that "guardrails," "constitutional governance," and "hard constraints" have specific technical meanings in published Anthropic research; will read every text overlay and narration line as if it were a public claim about Claude Code's design |
| **Motivation** | Prevent the showcase from generating a social media clip that misrepresents Claude Code's autonomy or safety posture; protect Anthropic's event reputation |

### Threat Actor B: Competitor CTO

| Field | Profile |
|-------|---------|
| **Goal** | Identify falsifiable claims that can be publicly disputed in the room or on social media immediately after the showcase |
| **Capability** | Can pull up Guardrails AI, LangSmith, and any GitHub repo in real time; fluent in hooks, callbacks, and enforcement vocabulary; can check the Jerry GitHub repo star count during the presentation |
| **Motivation** | Neutralize the "nobody had enforcement baked into session hooks" positioning claim; cast doubt on "production-grade" label |

### Threat Actor C: Skeptical Investor

| Field | Profile |
|-------|---------|
| **Goal** | Find the gap between the hype reel and underlying project reality; identify claims that cannot survive a 15-minute due-diligence conversation |
| **Capability** | Pattern-matches on "production-grade" vs. actual evidence; can Google the repo in real time; will scrutinize self-referential proof structures; notices the difference between "30+ agents" (floor formulation) and actual agent count |
| **Motivation** | Avoid getting excited about a developer tool with no external users, no stability guarantees, and whose only quality evidence is a rubric it applies to itself |

### Threat Actor D: Video Producer with 3 Days

| Field | Profile |
|-------|---------|
| **Goal** | Determine which dependencies will fail between now and Feb 21; identify assets that do not exist, spec gaps that create ambiguity, and owner assignments that are still placeholders |
| **Capability** | Full knowledge of InVideo AI limitations; aware that QR codes, particle animations, and action sports footage each require explicit asset pipeline steps; reads production dependencies as an execution checklist |
| **Motivation** | Not deliver a broken or degraded video at a 200+ person live event; protect professional reputation |

---

## Step 2: Attack Vector Inventory

Five attack vector categories applied per S-001 protocol (Ambiguity, Boundary, Circumvention, Dependency, Degradation). Execution ID: `20260218T-iter4`.

### Prior Finding Resolution Assessment

Before enumerating new vectors, the Red Team validates that iter-3 P0 and P1 findings are actually closed in v4:

| Prior ID | Finding | v4 Status | Evidence |
|----------|---------|-----------|----------|
| RT-004-iter3 | QR code asset missing | CLOSED | Production Dependency 7 added: PNG spec (1000x1000px, Level M), 10-foot scan test, 50 physical cards, Feb 19 noon deadline |
| RT-002-iter3 | "Nobody had a fix for enforcement" unfenced | CLOSED | Scene 2 now reads "Nobody had enforcement baked into the session hooks" |
| RT-005-iter3 | Plan B timeline too late | PARTIAL | Plan B decision point (Feb 20 noon) remains; no pre-production of Plan B assets by Feb 18 23:59 is specified |
| RT-006-iter3 | Music approval no owner/deadline | CLOSED | Music Sourcing updated: "approved by [named reviewer] by Feb 19, noon" -- owner placeholder present but unnamed |
| RT-009-iter3 | Scene 4 no FALLBACK | CLOSED | Scene 4 does not have a FALLBACK line in v4 -- see RT-002 below |
| RT-010-iter3 | Open-source fallback visual/narration mismatch | PARTIAL | Production Note covers URL overlay and narration fallback; Apache 2.0 badge removal on fallback path is not explicitly instructed |
| RT-001-iter3 | "Guardrails" autonomous framing | PARTIAL | Human framing is in narration; text overlay `CLAUDE CODE WROTE ITS OWN GUARDRAILS` still presents autonomous authorship without simultaneous qualification |
| RT-003-iter3 | Self-referential "production-grade" claim | OPEN | Narration still reads "This isn't a demo. This is production-grade code." No external evidence or scoping added |

### New / Residual Attack Vector Inventory

| ID | Attack Vector | Category | Adversary | Exploitability | Severity | Priority | Defense | Affected Dimension |
|----|---------------|----------|-----------|----------------|----------|----------|---------|-------------------|
| RT-001-20260218T-iter4 | Music reviewer is a named placeholder: "approved by [named reviewer] by Feb 19, noon" -- the reviewer slot is still a bracket, not a name; if this placeholder is never filled before production starts, the approval gate has no accountable owner and will be silently skipped | Dependency | D | High | Major | P1 | Partial | Methodological Rigor / Actionability |
| RT-002-20260218T-iter4 | Scene 4 FALLBACK is absent: the v4 script has FALLBACK lines for Scene 2, Scene 5, and Scene 6, but Scene 4 (action sports footage) still has no FALLBACK direction; if licensed skiing footage is unavailable in 3 days, the scene has no documented fallback path; this was RT-009-iter3, marked CLOSED above but is in fact still open in the v4 text | Dependency | D | High | Major | P1 | Missing | Completeness / Methodological Rigor |
| RT-003-20260218T-iter4 | "This isn't a demo. This is production-grade code" -- the self-referential proof structure persists unchanged from v3; the only evidence offered is a test count and a quality gate the framework applies to itself; a skeptical investor or competitor can falsify "production-grade" in 60 seconds at the event by asking "who else is using this?" | Ambiguity | B / C | High | Major | P1 | Partial | Evidence Quality |
| RT-004-20260218T-iter4 | Plan B pre-production is not specified: RT-005-iter3 recommended pre-producing Plan B assets by Feb 18 23:59 so the Feb 20 decision point is a polish decision, not a start-from-zero decision; v4 adds a Plan B decision point (item 4) but does not specify Plan B pre-production; with the event on Feb 21, a Feb 20 noon decision to switch to screen-recorded walkthrough leaves less than 36 hours for recording, editing, voice-over, and render | Degradation | D | High | Major | P1 | Partial | Methodological Rigor / Completeness |
| RT-005-20260218T-iter4 | Open-source fallback is narration-only: the Production Note instructs to replace the Scene 6 URL overlay and update narration if the repo is not live, but does not instruct removal of the Apache 2.0 badge overlay; a scenario where the repo is private (no HTTP 200) but the Apache 2.0 badge remains on screen creates a visual inconsistency that a skeptical audience will notice | Boundary | C / D | Medium | Minor | P2 | Partial | Internal Consistency |
| RT-006-20260218T-iter4 | QR code scan test is specified at "10-foot (3-meter) distance" but event projection scale is not specified; a QR code that scans from 3 meters on a phone screen may not scan from 5-8 meters at an auditorium projector; the scan test spec does not mention the actual projection screen size or throw distance at Shack15 SF, leaving a gap between the test condition and the live event condition | Dependency | D | Medium | Minor | P2 | Partial | Methodological Rigor |
| RT-007-20260218T-iter4 | Scene 1 text overlay `CLAUDE CODE WROTE ITS OWN GUARDRAILS` presents Claude Code as sole author without simultaneous human-agent framing; the narration begins "What happens when a developer gives Claude Code..." which is human-framing; however, the text overlay is read independently by viewers not attending to narration (ambient noise, second screen, visual-first attendees at a live event); an AI safety researcher reading the overlay in isolation reads: Claude Code wrote its own guardrails (autonomous creation) | Ambiguity | A | Medium | Minor | P2 | Partial | Evidence Quality |
| RT-008-20260218T-iter4 | "More than thirty agents across seven skills" floor formulation survives but the agent count verification command in Production Dependency 2 has no specified working directory or confirmed checkout state; if run from a stale local branch rather than the Feb 20 OSS-published commit, the count may diverge from the actual public repo state at event time; low exploitability but high-visibility if wrong at the event | Circumvention | B | Low | Minor | P2 | Partial | Internal Consistency / Traceability |

---

## Step 3: Defense Gap Assessment

| ID | Finding | Existing Defense | Defense Rating | Priority |
|----|---------|-----------------|----------------|----------|
| RT-001-20260218T-iter4 | Music reviewer is a named placeholder | "approved by [named reviewer] by Feb 19, noon" -- deadline is set | **Partial** -- deadline is concrete but reviewer identity is not; a bracket is not an owner; if the named individual is not identified before production begins, the approval gate has no enforcement mechanism | **P1** |
| RT-002-20260218T-iter4 | Scene 4 FALLBACK absent | None | **Missing** -- Scene 4 is the only production-risky scene without a FALLBACK direction; RT-009-iter3 recommended closing this and v4 did not implement it | **P1** |
| RT-003-20260218T-iter4 | Self-referential "production-grade" claim | "3,000+ tests passing" and "0.92 quality gate" are offered as evidence | **Partial** -- test count is real evidence of engineering rigor, but does not establish external production-grade deployment; no external users, community signal, or production deployment referenced | **P1** |
| RT-004-20260218T-iter4 | Plan B pre-production absent | Production Dependency item 4 specifies Feb 20 noon decision point | **Partial** -- conceptual Plan B exists; no pre-production assets specified before decision point; converts a polish decision into a start-from-zero scramble | **P1** |
| RT-005-20260218T-iter4 | Apache 2.0 badge not removed in repo-not-live fallback | Production Note covers URL overlay and narration; badge omitted | **Partial** -- partial fallback coverage; badge inconsistency is low-severity but visible at projection scale | **P2** |
| RT-006-20260218T-iter4 | QR code scan test at 3m does not validate event projection distance | "Test scan from 10-foot (3-meter) distance" specified | **Partial** -- test condition is specified but does not match event venue projection scale; low exploitability | **P2** |
| RT-007-20260218T-iter4 | Scene 1 overlay reads as autonomous authorship for visual-first attendees | Narration establishes "a developer gives Claude Code..." | **Partial** -- narration is human-framed; overlay is autonomous-framed; at a live event with ambient noise, a subset of attendees will read only the overlay | **P2** |
| RT-008-20260218T-iter4 | Agent count verification command has no working directory anchor | Production Dependency 2 specifies the command | **Partial** -- command exists; no working directory or checkout state specified; low risk if run by a developer who knows the repo, high risk if run by a production coordinator unfamiliar with the codebase | **P2** |

---

## Step 4: Countermeasures

### P0 Findings

No Critical findings identified in v4. All prior P0 findings (RT-004-iter3: QR code) are confirmed closed. v4 is the first iteration with zero Critical findings.

### P1 Findings (Important -- SHOULD mitigate)

#### RT-001: Music Reviewer Is an Unnamed Placeholder [MAJOR]

**Attack Vector:** The music approval gate has a deadline (Feb 19, noon) but no named accountable owner. A "[named reviewer]" bracket is not an owner. At a live production with 3 days of runway, unnamed approval gates silently fail when no one claims ownership.

**Specific Action:** Replace "[named reviewer]" in both the Script Overview Music Sourcing note and Production Dependency item 6 with an actual name. This is a one-word edit to both locations that closes the accountability gap entirely.

**Acceptance Criteria:** The music reviewer is identified by name in both locations. That individual has confirmed they will review and approve all 6 cues by Feb 19, noon.

---

#### RT-002: Scene 4 FALLBACK Absent [MAJOR]

**Attack Vector:** Scene 4 requires licensed action sports footage -- "big mountain skiing, cliff launches, fearless athleticism." This is the highest asset-rights risk in the entire script. The McConkey estate or any rights holder could block specific footage. Scene 4 is the only production-risky scene without a FALLBACK line. RT-009-iter3 explicitly recommended adding this; v4 did not implement it.

**Specific Action:** Add a FALLBACK line to Scene 4 between the VISUAL and NARRATION blocks:

> **FALLBACK:** Stock footage of extreme skiing or freestyle skiing (no specific athlete required). The text overlays `SHANE McCONKEY // REINVENTED SKIING BY REFUSING TO BE BORING` and `IF YOU'RE NOT HAVING FUN, YOU'RE DOING IT WRONG` remain regardless of footage source. If no action sports footage is available, use a slow-motion dark-themed code-scrolling visual paired with the McConkey text overlay as a visual contrast (code = serious discipline; overlay = personality).

**Acceptance Criteria:** Scene 4 has a FALLBACK direction. Licensed action sports footage is confirmed available in the production library or stock footage service, OR the code-visual fallback is tested in InVideo by the Feb 19 gate.

---

#### RT-003: Self-Referential "Production-Grade" Claim [MAJOR]

**Attack Vector:** Scene 5 narration reads: "This isn't a demo. This is production-grade code." The only evidence offered is a test count (3,000+) and a quality gate (0.92) that the framework applies to itself. A skeptical investor or competitor CTO can stand up during the Q&A and ask "who else uses this?" -- a question the video provides no answer to. The self-referential structure (Jerry validates Jerry, which validates the Jerry showcase video, which showcases Jerry) is a logical circularity that sophisticated audiences will notice.

**Specific Action (preferred, no word count impact):** Remove "This isn't a demo." The remaining sentence "This is production-grade code." is stronger without the defensive negation, and the test count + gate ARE the evidence -- the label "production-grade" should follow the facts, not precede them. Revised narration: "More than three thousand tests. Passing. A quality gate at zero-point-nine-two that does not bend. Ten adversarial strategies running before anything ships. Production-grade engineering." This reorders the claims so the evidence lands first and the label is the conclusion, not the assertion.

**Alternative (if word count must stay at 255):** Swap "This isn't a demo." for "Used to build itself." -- four words that add external credibility (the framework governs its own development, which is a legitimate use-case demonstration beyond pure self-referential quality scoring).

**Acceptance Criteria:** The "production-grade" label is either (a) preceded by the evidence rather than preceded by a defensive negation, or (b) supplemented with a single verifiable external use statement. The resulting narration does not invite the "who else uses this?" falsification path.

---

#### RT-004: Plan B Pre-Production Not Specified [MAJOR]

**Attack Vector:** v4 Production Dependency item 4 establishes a Plan B decision point at Feb 20 noon, but Plan B assets -- a screen-recorded terminal walkthrough with voiceover -- are not specified as a parallel pre-production task. If the Feb 19 InVideo test gate fails and Plan B is activated at noon on Feb 20, the production team has under 36 hours to record, edit, voice-over, synchronize music, and render a 2:00 video. This is a structurally infeasible timeline unless assets were pre-produced in parallel.

**Specific Action:** Add to Production Dependency item 4 or as a new item: "Plan B pre-production (parallel task, not contingent on InVideo gate): By Feb 18 23:59, record a 2:00 screen capture of Jerry executing an actual quality gate calculation (not simulated). Rough cut with same narration script and music cues. This asset is held in reserve. If InVideo test gate fails on Feb 19, Plan B is a polish pass, not a start-from-zero production. Owner: developer (screen capture) + video producer (rough cut assembly)."

**Acceptance Criteria:** Plan B rough cut exists by Feb 18 23:59 (or at absolute latest by Feb 19 noon, before the InVideo gate). The Feb 20 decision point becomes: "polish Plan B vs. continue with InVideo," not "start Plan B from zero."

---

### P2 Findings (Monitor -- MAY mitigate)

**RT-005 (Apache 2.0 badge in fallback):** Extend the Production Note fallback instruction to add: "(3) Remove Apache 2.0 badge overlay from Scene 6 visual if repo is not yet public." One sentence closes the inconsistency. Low effort, meaningful visual coherence improvement.

**RT-006 (QR scan distance):** Amend Production Dependency item 7 scan test to: "Test scan from 10-foot (3-meter) distance AND from the anticipated maximum viewing distance at Shack15 projection scale." One additional test condition. Low effort.

**RT-007 (Scene 1 overlay autonomous framing):** Consider sequencing the Scene 1 text overlay to appear after the narration line "What happens when a developer gives Claude Code a blank repo" has been spoken, rather than at the start of the cold open. If InVideo supports timed text appearance, this converts "autonomous" read to "directed" read without changing any words. No script change required -- only a production timing note.

**RT-008 (Agent count command path):** Add `--maxdepth 6` guard and specify: "Run from repo root on the Feb 20 OSS-published commit (not a local branch)." One-line amendment to Production Dependency item 2.

---

## Step 5: Scoring Impact

### Net Dimension Impact

| Dimension | Weight | Impact | RT Findings | Rationale |
|-----------|--------|--------|-------------|-----------|
| Completeness | 0.20 | Negative | RT-002, RT-004 | Scene 4 FALLBACK is still absent (RT-002 Major, explicitly recommended in iter-3 and not implemented). Plan B pre-production is unspecified (RT-004 Major). Two completeness gaps remain that are directly addressable. |
| Internal Consistency | 0.20 | Positive | RT-001, RT-005 | v4 has closed RT-002-iter3 ("Nobody had a fix for enforcement") -- the strongest internal consistency risk from iter-3. Remaining inconsistency risks (RT-001 named placeholder, RT-005 badge fallback) are P1 and P2 respectively. Net improvement over iter-3. |
| Methodological Rigor | 0.20 | Neutral | RT-001, RT-004 | Music approval deadline is set (improvement); owner is unnamed (remaining gap). Plan B deadline architecture is sound; pre-production specification is absent (gap). Net: one step forward, one step not taken. |
| Evidence Quality | 0.15 | Negative | RT-003, RT-007 | Self-referential "production-grade" claim persists unchanged (RT-003 Major). Scene 1 overlay reads as autonomous authorship for visual-first attendees (RT-007 Minor/P2). No new external evidence introduced in v4. |
| Actionability | 0.15 | Positive | All P1s | Production Dependencies section has concrete, verifiable acceptance criteria for QR code (item 7), music (item 6), and agent count (item 2). The four P1 countermeasures above are each single-edit or single-addition changes -- highly actionable. |
| Traceability | 0.10 | Positive | All | v4 revision log is the most comprehensive yet: scene-by-scene change table with finding IDs, before/after values, and word count deltas. Finding-level traceability in Self-Review is complete and includes the previously-silent MF-003. H-16 compliance is documented. |

### Overall Assessment: TARGETED REVISION REQUIRED -- CLOSE TO THRESHOLD

v4 is a genuine step forward from v3. It has closed all 9 revision guidance items from the iter-3 composite, resolved the only Critical script content finding that had persisted from earlier iterations (RT-002-iter3: "Nobody had a fix for enforcement"), and added substantial production dependency scaffolding. The Red Team finds zero Critical findings in v4 -- the first iteration in this tournament to achieve that result.

The residual attack surface is focused and addressable:

1. **Two unclosed P1 production gaps from iter-3** (Scene 4 FALLBACK absent, Plan B pre-production unspecified) are the highest-priority residual risks. Both were recommended in iter-3; neither was implemented in v4. Closing them requires no script rewriting -- only additions to Scene 4 and Production Dependencies.

2. **One persistent P1 content risk** (RT-003: "This isn't a demo. This is production-grade code.") can be resolved with a single narration sentence restructure that requires no word count increase.

3. **One P1 accountability gap** (RT-001: named reviewer placeholder) is a production execution risk that requires one word to close.

**Recommendation: REVISE -- targeted and achievable.** All four P1 findings are addressable with edits that add no material complexity to the script. The P2 findings are monitoring items. If the four P1 countermeasures are implemented, v4 post-revision should meet the 0.95 C4 tournament target. The trajectory (0.67 -> 0.82 -> 0.89 -> this iteration) indicates a well-functioning revision cycle; the gap to 0.95 is a last-mile execution problem, not a structural quality problem.

**Projected composite score impact:** Closing RT-001 through RT-004 adds positive contributions to Completeness (+0.03 to +0.05), Methodological Rigor (+0.02 to +0.03), Evidence Quality (+0.02 to +0.03), and Actionability (+0.01). If the iter-3 pre-mitigation estimate was 0.89, post-P1 closure should push the composite to 0.93-0.96. The 0.95 target is within reach.

---

## Summary

v4 of the Jerry Framework hype reel script is the strongest iteration in this tournament. The Red Team, applying four adversary perspectives (AI safety researcher, competitor CTO, skeptical investor, video producer with 3 days), finds zero Critical findings -- the first iteration to achieve this. The remaining attack surface consists of four Major findings (P1) and four Minor findings (P2). All four P1 findings are execution gaps that can be closed without script rewrites: Scene 4 FALLBACK addition (RT-002), music reviewer named (RT-001), Plan B pre-production specified (RT-004), and "production-grade" narration restructured (RT-003). Two P1 findings from iter-3 (Scene 4 FALLBACK, Plan B pre-production) were explicitly recommended and not yet implemented -- closing them is the primary obligation before the v4 composite can clear 0.95. The video is ready to defend its content quality; what remains is production execution discipline.

---

*Agent: adv-executor | Strategy: S-001 Red Team Analysis*
*Tournament: feat023-showcase-20260218-001 | Iteration: 4 of C4 tournament*
*SSOT: `.context/rules/quality-enforcement.md`*
*Template: `.context/templates/adversarial/s-001-red-team.md` v1.0.0*
*H-16: S-003 Steelman confirmed applied (iteration-2/s-003-steelman/adv-executor-s003-execution.md)*
*Deliverable: ps-architect-001-hype-reel-script-v4.md*
*Date: 2026-02-18*
