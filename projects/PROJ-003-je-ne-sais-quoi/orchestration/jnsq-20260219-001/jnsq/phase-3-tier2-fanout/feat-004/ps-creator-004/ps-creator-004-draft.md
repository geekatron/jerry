# FEAT-004: Framework Voice & Personality

<!--
AGENT: ps-creator-004
VERSION: 0.5.0
WORKFLOW: jnsq-20260219-001
PHASE: 3 — Tier 2 Fan-Out
FEATURE: FEAT-004 Framework Voice & Personality
PARENT: EPIC-001-je-ne-sais-quoi
STATUS: REVISED (R4 targeted revision pass)
DATE: 2026-02-19
CRITICALITY: C2 (Standard)
INPUTS: ps-creator-001-draft.md (Persona Distillation v0.9.0), ps-creator-002-draft.md (FEAT-002 /saucer-boy Skill v0.6.0), ps-creator-003-draft.md (FEAT-003 Visual Identity v0.1.0)
FEEDS INTO: Implementation of voiced CLI output, hook messages, quality gate messages, error messages, documentation comments
-->

> This document is the implementation specification for applying the Saucer Boy voice to all developer-facing Jerry Framework output. It is the PRIMARY CONSUMER of the `/saucer-boy` skill (FEAT-002). Every message template in this document preserves all technical information from the current voice while applying the persona per the Authenticity Tests.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Core Principle](#core-principle) | The single rule that governs every voice decision |
| [Message Categories](#message-categories) | Complete inventory of framework output types |
| [Voice Application Guide](#voice-application-guide) | Per-category tone, humor, before/after examples, boundaries |
| [Message Templates](#message-templates) | Concrete templates for the highest-frequency outputs |
| [Integration Workflow](#integration-workflow) | How developers apply voice to new messages |
| [Anti-Patterns](#anti-patterns) | Messages that violate the voice, with explanations |
| [Visual Integration](#visual-integration) | How FEAT-003 visual identity applies per category |
| [Traceability](#traceability) | Source document lineage |
| [Self-Review Verification](#self-review-verification-s-010) | S-010 checklist |
| [Document Metadata](#document-metadata) | Version, status, agent |

---

## Core Principle

**Clarity ALWAYS trumps personality. Error context must never be obscured.**

This is FEAT-004's load-bearing constraint. It is derived from the persona doc's Authenticity Test 1 (Information Completeness), which is a HARD gate: if removing all voice elements leaves the developer without the information they need, the voice has failed. Every template, every rewrite, every voice decision in this document is subordinate to this constraint.

The corollary: a clear, dry message is always acceptable. A clever message that hides the diagnosis is always a bug.

**Scope exclusion:** JSON output mode (`--json` flag) is machine-readable and MUST NOT receive voice treatment. Voice applies only to human-readable terminal output. This exclusion applies to all categories in this document.

---

## Message Categories

The Jerry Framework produces developer-facing output in six categories. Each category has a frequency estimate, a primary audience context, and a default tone position on the Saucer Boy tone spectrum.

| # | Category | Examples | Frequency | Primary Audience | Default Tone Position |
|---|----------|----------|-----------|------------------|-----------------------|
| 1 | [Quality Gate Messages](#category-1-quality-gate-messages) | PASS, REVISE, REJECTED, scoring output | High | Active session developer | Varies by band (see sub-categories) |
| 2 | [Error Messages](#category-2-error-messages) | Validation errors, file not found, env var missing, permission denied, constitutional failure | High | Developer debugging | Diagnostic |
| 3 | [CLI Session Messages](#category-3-cli-session-messages) | `jerry session start`, `end`, `status`, `abandon` | Medium | Active session developer | Medium energy (routine) |
| 4 | [Hook Output](#category-4-hook-output) | SessionStart, UserPromptSubmit, PreToolUse, SubagentStop | Medium | Active session developer | Medium energy (routine) |
| 5 | [Progress & Status Indicators](#category-5-progress--status-indicators) | Spinner text, completion messages, work item state changes | Medium-Low | Active session developer | Low energy (efficient) |
| 6 | [Help Text & Documentation](#category-6-help-text--documentation) | CLI `--help`, inline rule explanations, onboarding text, documentation comments | Low | Mixed (onboarding through experienced) | Medium energy (clarity) |

### Categories Not Covered

The CLI also includes `jerry config` and `jerry transcript` commands. These are **not covered** by this voice specification because:

- **Config output** (`jerry config show|get|set|path`) is structural data display (key-value pairs, file paths). Voice treatment would not add value; the output is already direct and functional.
- **Transcript output** (`jerry transcript parse`) is data processing output. The messages are progress-oriented and covered by Category 5 (Progress & Status Indicators) patterns.

If future CLI commands produce new message types that do not fit the existing 6 categories, they should be classified using the Audience Adaptation Matrix and added to this document.

### Priority Order for Voice Implementation

Per FEAT-002 `references/implementation-notes.md`:

| Priority | Category | Rationale |
|----------|----------|-----------|
| 1 | Quality gate messages | Highest frequency, highest DX impact |
| 2 | Error messages | Most critical for developer trust |
| 3 | Session messages | Sets the tone for every interaction |
| 4 | Hook output | Framework's first impression each session |
| 5 | Help and documentation | Lower priority -- do not inject personality where none is needed |
| 6 | Progress indicators | Lowest priority -- efficiency is the job |

---

## Voice Application Guide

For each category, this section specifies the tone spectrum position, humor deployment level, before/after examples, and boundary conditions.

### Category 1: Quality Gate Messages

Quality gate messages are the highest-frequency, highest-impact framework output. They are the primary mechanism by which the developer experiences the quality system. The voice must make this experience rigorous AND human.

#### Sub-Category 1a: Quality Gate PASS (score >= 0.92)

**Tone spectrum position:** Full Energy (Celebration)
**Humor deployment:** Yes -- celebration earned it
**Energy:** High
**Technical depth:** Low (the score speaks)
**Calibration pair:** Pair 1 from voice-guide.md
**Biographical anchor:** Banana-suit energy -- excellence and absurdity coexisting

**Before (current voice):**
```
Quality gate: PASSED
Composite score: 0.94
Threshold: >= 0.92
Status: Deliverable accepted.
```

**After (Saucer Boy voice):**
```
Quality gate: PASS -- 0.94

Evidence quality was the standout dimension. Internal consistency held.
That's a clean run. No gates clipped.

Deliverable accepted.
```

**Voice application notes:**
- Lead with the state and score on one line. The developer's eye goes there first.
- Name the standout dimension(s) -- this is not generic celebration. It is specific acknowledgment of what the developer did well.
- One line of voice ("clean run", "no gates clipped") -- enough to signal personality without delaying the information.
- Close with the disposition. "Deliverable accepted" is the functional outcome; it stays.

**Boundary conditions:**
- Never omit the score. The score is the information.
- Never replace the dimension analysis with pure celebration. The developer learns from knowing what worked.
- Humor elements should be one line maximum. If the celebration is longer than the diagnosis, the proportions are wrong.

#### Sub-Category 1b: Quality Gate REVISE (score 0.85-0.91)

**Tone spectrum position:** Medium Energy (Failure, close to threshold)
**Humor deployment:** Gentle -- encouragement, not mockery
**Energy:** Medium
**Technical depth:** Medium (dimension breakdown required)
**Calibration pair:** Pair 2 from voice-guide.md
**Biographical anchor:** The iteration energy -- revision as process, not punishment

**Before (current voice):**
```
Quality gate: FAILED
Composite score: 0.89
Threshold: >= 0.92
Status: Deliverable rejected. Revision required per H-13.
Dimensions below threshold:
  - Internal consistency: 0.81
  - Methodological rigor: 0.84
```

**After (Saucer Boy voice):**
```
Quality gate: REVISE -- 0.89

Close. Three points from the line. Here's where the rubric is seeing gaps:

  Internal consistency: 0.81 -- contradiction detected between sections 3 and 7
  Methodological rigor: 0.84 -- evidence chain has gaps in the analysis section

Round 2. Tighten those two dimensions and you're over the threshold.
```

**Voice application notes:**
- Use "REVISE" instead of "FAILED" as the label. The operational band (from quality-enforcement.md) matters -- this is still rejected per H-13, but the proximity to threshold means targeted revision is likely sufficient. The word "REVISE" communicates the path forward without softening the consequence: the deliverable is rejected until revision brings it above 0.92.
- "Close" acknowledges the proximity. "Three points from the line" is direct and human.
- Dimension breakdown includes a diagnosis, not just a number. The developer needs to know what "0.81 internal consistency" means concretely.
- "Round 2" frames revision as process, not punishment.
- One line of forward guidance at the end.

**Boundary conditions:**
- Never use humor that could read as mocking the failure. "Round 2" is collaborative. "Better luck next time" is sarcasm.
- Never omit the dimension breakdown. The developer cannot fix what they cannot see.
- Never soften the score or the threshold. "Close" is accurate for 0.85-0.91. The system is serious.

#### Sub-Category 1c: Quality Gate REJECTED (score < 0.85)

**Tone spectrum position:** Low Energy (Diagnostic)
**Humor deployment:** None -- the developer needs diagnosis, not performance
**Energy:** Low
**Technical depth:** High (full dimension breakdown, priority-ordered action path)
**Calibration pair:** Pair 3 from voice-guide.md
**Biographical anchor:** Meticulous preparation energy -- the discipline that built the Spatula

**Before (current voice):**
```
Quality gate: FAILED
Composite score: 0.78
Threshold: >= 0.92
Status: Deliverable rejected. Significant rework required per H-13.
Dimensions below threshold:
  - Completeness: 0.71
  - Methodological rigor: 0.74
  - Evidence quality: 0.76
```

**After (Saucer Boy voice):**
```
Quality gate: REJECTED -- 0.78

This needs real work before the next pass. Three dimensions are underperforming:

  Completeness: 0.71 -- the analysis is missing key sections
  Methodological rigor: 0.74 -- the approach isn't traceable to the strategy catalog
  Evidence quality: 0.76 -- claims need sourcing

Start with completeness -- it's pulling everything else down.
The gap to 0.92 is real. The path is clear.
```

**Voice application notes:**
- "REJECTED" is the operational band label. Use it directly.
- No humor. No metaphors. Maximum precision.
- Dimension breakdown with concrete diagnosis per dimension.
- Priority-ordered action path: "Start with completeness" tells the developer where to focus.
- "The gap is real. The path is clear." -- acknowledges difficulty while providing direction. Not cold; focused.

**Boundary conditions:**
- NEVER use humor in REJECTED messages. The developer is facing significant rework. Respect the moment.
- NEVER omit the priority ordering. Without it, the developer does not know where to start.
- NEVER soften "REJECTED" to something less direct. The system is serious about quality.

#### Sub-Category 1d: Constitutional Compliance Failure / Escalation

**Tone spectrum position:** Hard Stop
**Humor deployment:** None -- stakes are real
**Energy:** Low (direct, maximum precision)
**Technical depth:** High (trigger identification, escalation level, required action)
**Calibration pair:** Pair 6 from voice-guide.md
**Biographical anchor:** The moment where jokes stop -- the register of "What the Framework Does NOT Inherit"

**Before (current voice):**
```
Constitutional compliance check: FAILED
Trigger: AE-001 -- modification to docs/governance/JERRY_CONSTITUTION.md
Criticality: Auto-C4
Status: Hard stop. Human escalation required.
```

**After (Saucer Boy voice):**
```
Constitutional compliance check: FAILED

Trigger: AE-001 -- docs/governance/JERRY_CONSTITUTION.md was modified.
Auto-escalation: C4. This is not a drill.

Hard stop. Human review required before proceeding.
This is exactly the scenario the auto-escalation rules exist for.
```

**Voice application notes:**
- The state line is identical. "FAILED" is the correct word for constitutional checks.
- Trigger identification is expanded: instead of just "modification to", say "was modified" -- active, direct.
- "This is not a drill" -- direct, acknowledges stakes. Not a joke.
- "This is exactly the scenario the auto-escalation rules exist for" -- explains WHY the stop is happening. Even at maximum severity, the voice explains.

**Boundary conditions:**
- ZERO humor. ZERO metaphors. ZERO personality beyond directness and clarity.
- Never soften "Hard stop." The developer must stop.
- Always explain why the auto-escalation triggered. The developer should understand the system, not just obey it.

---

### Category 2: Error Messages

Error messages are the framework's most trust-sensitive output. A developer in an error state has the least patience for personality and the most need for precision. The Saucer Boy voice in error messages is expressed through directness and actionability -- stripping corporate formalism -- not through humor content.

**Tone spectrum position:** Diagnostic to Medium (varies by severity)
**Humor deployment:** Light tone only -- human and actionable, but humor content is not required
**Energy:** Medium
**Technical depth:** High (what failed, why, what to do)

#### Error Sub-Category: Missing Environment Variable

**Before (current voice):**
```
Error: JERRY_PROJECT environment variable not set.
Active project is required. See CLAUDE.md H-04.
```

**After (Saucer Boy voice):**
```
JERRY_PROJECT not set.

Set your project and drop back in:

  jerry projects list          # see what's available
  export JERRY_PROJECT=PROJ-003-je-ne-sais-quoi

H-04: active project required before proceeding.
```

**Voice application notes:**
- Lead with what is missing. Not "Error:" prefix -- the context makes it an error.
- Provide the recovery path immediately. Commands the developer can copy-paste.
- Inline comments on commands where they add clarity.
- Rule reference at the end, not the beginning. The developer needs the fix first.

#### Error Sub-Category: File Not Found

**Before (current voice):**
```
Error: File not found: projects/PROJ-003-je-ne-sais-quoi/PLAN.md
```

**After (Saucer Boy voice):**
```
File not found: projects/PROJ-003-je-ne-sais-quoi/PLAN.md

Check the path exists and the project structure is complete:

  ls projects/PROJ-003-je-ne-sais-quoi/
```

**Voice application notes:**
- State the fact. Provide a diagnostic action.
- No personality is needed here. The directness IS the personality — per persona doc Voice Trait 1 (Direct): "Says the thing. No preamble. No throat-clearing." The before example's "Error: File not found:" prefix is throat-clearing; removing it and leading with the fact is the voice transformation.

#### Error Sub-Category: Validation Error

**Before (current voice):**
```
Error: Invalid project ID format: PROJ003
Error: Project ID must match pattern PROJ-NNN-slug
```

**After (Saucer Boy voice):**
```
Invalid project ID: PROJ003

Expected format: PROJ-NNN-slug (e.g., PROJ-003-je-ne-sais-quoi)

  jerry projects list          # see existing projects
  jerry projects validate PROJ-003-je-ne-sais-quoi  # check a specific ID
```

**Voice application notes:**
- Show the expected format with a concrete example.
- Provide commands to discover valid options.

#### Error Sub-Category: Command Dispatcher Not Configured

**Before (current voice):**
```
Error: Command dispatcher not configured
```

**After (Saucer Boy voice):**
```
Command dispatcher not configured.

This is an infrastructure error -- the CLI handlers are not wired.
Check that the application bootstrapped correctly.
```

**Voice application notes:**
- When the error is internal (not user-caused), acknowledge that explicitly.
- Do not blame the developer for system-level failures.

#### Error Sub-Category: Session Handler Errors

**Before (current voice):**
```
Error: Session handlers not configured
```

**After (Saucer Boy voice):**
```
Session handlers not configured.

The session subsystem didn't initialize. This is a framework issue, not yours.
```

**Boundary conditions for all error messages:**
- NEVER omit the error identity (what failed).
- NEVER omit the recovery path when one exists.
- NEVER use humor that delays diagnosis. "Light tone" means non-bureaucratic, not funny.
- NEVER blame the developer for system-level failures.
- If the error is the developer's action: state what went wrong and what to do. If the error is the system's fault: say so.

---

### Category 3: CLI Session Messages

Session messages bracket the developer's work. They set the tone (session start) and land the experience (session end). These are medium-energy moments -- present and collaborative.

**Tone spectrum position:** Medium Energy (Routine) to Full Energy (Celebration at session end with all items done)
**Humor deployment:** Light-medium -- sets the tone, acknowledges the human
**Energy:** Medium (start/status/abandon) to High (end with all items done)

#### Session Start

**Before (current voice):**
```
Session started: abc-123-def
Description: Working on FEAT-004
```

**After (Saucer Boy voice):**
```
Session live. Project: PROJ-003-je-ne-sais-quoi

Enforcement architecture is up. Quality gates are set.
Let's build something worth scoring.
```

**Voice application notes:**
- "Session live" instead of "Session started" -- active, present tense.
- One line of voice at the end. Sets collaborative tone without delaying work.
- Project ID is the essential context. Include it.

#### Session End (Partial Completion)

**Before (current voice):**
```
Session ended: abc-123-def
Summary: 3 items completed, 2 remaining
```

**After (Saucer Boy voice):**
```
Session ended. 3 items complete, 2 remaining.

Progress is progress. See you next session.
```

**Voice application notes:**
- Acknowledge the work done without overpraising or underpraising.
- "Progress is progress" -- warm, honest, not performative.

#### Session End (All Items Complete)

**Before (current voice):**
```
Session complete.
All items: DONE
Status: Session ended.
```

**After (Saucer Boy voice):**
```
All items landed.

+----------------------------------+
|      SESSION COMPLETE            |
|  Every item: DONE                |
|  Saucer Boy approves.            |
+----------------------------------+

That's a powder day. See you next session.
```

**Voice application notes:**
- This is the Celebration Tier 1 (Powder Day) from FEAT-003 visual identity.
- Box-art ASCII is earned here. Maximum visual energy.
- "Saucer Boy approves" -- self-referential identity marker. Used ONLY in maximum celebration CLI output (all items complete). This is framework output voice, not Claude personality (boundary condition #6). It is authorized by persona doc Pair 7.
- "Powder day" -- the highest-energy ski metaphor, reserved for genuine completion.

#### Session Status (No Active Session)

**Before (current voice):**
```
No active session.

Use 'jerry session start' to begin a new session.
```

**After (Saucer Boy voice):**
```
No active session.

  jerry session start           # drop in when you're ready
```

#### Session Abandon

**Before (current voice):**
```
Session abandoned: abc-123-def
Reason: Switching to higher-priority work
```

**After (Saucer Boy voice):**
```
Session abandoned.
Reason: Switching to higher-priority work

No judgment. Sometimes you have to change lines mid-run.
```

**Voice application notes:**
- Abandoning a session is a valid choice. The voice acknowledges this without sarcasm or disappointment.
- "Change lines mid-run" -- a ski metaphor that is transparent (changing direction during a run).

**Boundary conditions for session messages:**
- Session start should be brief. The developer wants to work, not read personality.
- Session end should be proportional: partial completion gets a nod, full completion gets a celebration.
- NEVER make abandon feel like a failure. It is a workflow decision.

---

### Category 4: Hook Output

Hook output is the framework's first impression each session. The SessionStart hook fires before the developer has done anything. The voice should be present but not blocking.

**Tone spectrum position:** Medium Energy (Routine)
**Humor deployment:** Light -- present, not heavy
**Energy:** Medium
**Technical depth:** Low to Medium

#### SessionStart Hook: Active Project

**Before (current hook `systemMessage`):**
```
Jerry Framework: Project PROJ-003-je-ne-sais-quoi active
```

**After (Saucer Boy voice):**
```
Jerry Framework: PROJ-003-je-ne-sais-quoi active. Quality gates set.
```

**Voice application notes:**
- The systemMessage is the user-visible terminal line. Keep it under 80 characters.
- "Quality gates set" -- one phrase that signals the enforcement architecture is live.
- The `additionalContext` (Claude-facing XML) does not need voice -- it is machine context.

#### SessionStart Hook: No Project Set

**Before (current hook `systemMessage`):**
```
Jerry Framework: No project set (3 available)
```

**After (Saucer Boy voice):**
```
Jerry Framework: No project set. 3 available -- pick one to drop in.
```

#### SessionStart Hook: Invalid Project

**Before (current hook `systemMessage`):**
```
Jerry Framework: ERROR - PROJ-999 invalid (Project directory not found)
```

**After (Saucer Boy voice):**
```
Jerry Framework: PROJ-999 invalid -- directory not found. Check jerry projects list.
```

**Voice application notes for all hook output:**
- The systemMessage field is constrained to a single terminal line. Voice must fit within this.
- The additionalContext field (XML-tagged content for Claude's context window) should remain neutral and machine-readable. Do not apply voice to additionalContext.
- Pre-commit hook warnings are infrastructure messages. Leave them in current voice.

**Boundary conditions:**
- Hook output is the framework's first impression. A bad first impression is worse than no impression. When in doubt, be clear and brief.
- NEVER use hook output for extended personality. The developer has not started working yet.

---

### Category 5: Progress & Status Indicators

Progress indicators are utilitarian. The developer needs to know what is happening and how far along it is. Voice is minimal -- efficiency is the job.

**Tone spectrum position:** Low Energy (Routine informational)
**Humor deployment:** None
**Energy:** Low
**Technical depth:** Medium

#### Work Item State Changes

**Before (current voice):**
```
Started work item: PROJ-003-FEAT-004
Status: in_progress
```

**After (Saucer Boy voice):**
```
PROJ-003-FEAT-004: in progress.
```

**Before (current voice):**
```
Completed work item: PROJ-003-FEAT-004
Status: done
```

**After (Saucer Boy voice):**
```
PROJ-003-FEAT-004: complete.
```

**Before (current voice):**
```
Blocked work item: PROJ-003-FEAT-004
Status: blocked
Reason: Waiting on FEAT-002 skill deployment
```

**After (Saucer Boy voice):**
```
PROJ-003-FEAT-004: blocked.
Reason: Waiting on FEAT-002 skill deployment.
```

**Voice application notes:**
- State changes are Celebration Tier 3 (Nod) from FEAT-003. The information is the acknowledgment.
- One line. Item ID, colon, state. The developer's eye pattern is: scan for the item ID, read the state.
- Block reasons are preserved verbatim -- they are user-supplied content.

**Boundary conditions:**
- NEVER decorate state changes with personality. They are high-frequency, low-significance events.
- NEVER use emoji on state changes. The visual budget for this context is zero per FEAT-003.

#### Work Item Creation

**Before (current voice):**
```
Created work item: PROJ-003-FEAT-004
Title: Framework Voice & Personality
Type: feature
Priority: high
```

**After (Saucer Boy voice):**
```
Created: PROJ-003-FEAT-004
Title: Framework Voice & Personality
Type: feature | Priority: high
```

**Voice application notes:**
- Slightly compressed format. Two fields on one line when they fit.
- No personality needed. The creation is the event.

#### Progress Display

Per FEAT-003, progress bars and trackers use the established ASCII pattern:

```
+------------------------------------------------------------------+
|                     EPIC PROGRESS TRACKER                         |
+------------------------------------------------------------------+
| Features:  [############........] 60% (4/7 completed)            |
+------------------------------------------------------------------+
```

No voice modification needed. The pattern is already aligned with the persona's visual vocabulary.

---

### Category 6: Help Text & Documentation

Help text and documentation are low-frequency but high-importance for onboarding and reference. The voice should be warm for onboarding, clear for reference, and non-blocking throughout.

**Tone spectrum position:** Medium Energy (Clarity)
**Humor deployment:** None for rule explanations; warm for onboarding
**Energy:** Medium
**Technical depth:** High

#### Rule Explanations

**Before (current voice):**
```
H-13: Quality threshold >= 0.92 for C2+ deliverables.
Weighted composite score using S-014 dimensions.
Below threshold = REJECTED, revision required.
```

**After (Saucer Boy voice):**
```
H-13: quality threshold is 0.92 for C2+ deliverables.

The 0.92 threshold is a governance decision (see quality-enforcement.md).
The logic behind the bands: below 0.85, you're facing structural rework --
the score gap understates the real problem. Between 0.85 and 0.91, targeted
revision closes the gap. At 0.92, the remaining distance to perfect is small
enough that polish works. The threshold is where rework cost meets acceptable
quality. That's the logic.
```

**Voice application notes:**
- Rule explanations have NO humor. Clarity is the only job.
- But they should explain the WHY, not just the WHAT. The voice's contribution here is treating the developer as someone who deserves the reasoning, not just the rule number.
- "That's the logic" -- direct closure. Not corporate, not whimsical. Just done.

#### CLI Help Text

**Before (hypothetical `jerry session --help`):**
```
Usage: jerry session <command>

Commands:
  start    Start a new session
  end      End the current session
  status   Show current session status
  abandon  Abandon the current session
```

**After (Saucer Boy voice):**
```
Usage: jerry session <command>

Commands:
  start    Start a new session
  end      End the current session
  status   Show current session status
  abandon  Abandon the current session

Run 'jerry session <command> --help' for details.
```

**Voice application notes:**
- Help text should be functional. Do not inject personality into `--help` output.
- Adding one line of guidance ("Run ... for details") is the extent of voice here.
- CLI help is a reference tool. Developers scan it. Personality slows scanning.

#### Onboarding Text

**Voice guidance for onboarding contexts:**
- Warmth and invitation. The rigor of the system can be intimidating.
- "This is intense at first. The logic is consistent once you see how it fits together."
- Lower the barrier to entry without lowering the quality standards.
- Use the "Onboarding / new developer" row from the Audience Adaptation Matrix: Medium energy, Warm humor, Low technical depth, Invitation tone anchor.

**Boundary conditions for help and documentation:**
- NEVER inject personality that slows scanning of reference text.
- NEVER make onboarding text feel like it is minimizing the system's complexity. It IS complex. The voice acknowledges that while providing confidence that the complexity is learnable.
- Rule explanations should explain the reasoning, not just cite the rule. This is the voice's contribution to clarity.

---

## Message Templates

These are concrete, copy-ready templates for the highest-frequency framework outputs. Each template uses `{placeholders}` for variable content.

### Template 1: Quality Gate PASS

```
Quality gate: PASS -- {score}

{standout_dimension} was the standout dimension. {secondary_observation}.
That's a clean run. No gates clipped.

Deliverable accepted.
```

**Variables:**
- `{score}`: Composite score (e.g., 0.94)
- `{standout_dimension}`: Highest-scoring dimension name
- `{secondary_observation}`: One factual observation about the scoring profile

**Visual integration (FEAT-003):**
- Color: Green (`COLOR_PASS`)
- Prefix: `checkmark` Unicode indicator in full terminals, `[PASS]` in CI
- Score: Bold (`COLOR_SCORE`)
- No box-art (Celebration Tier 2: Clean Run)

### Template 2: Quality Gate REVISE

```
Quality gate: REVISE -- {score}

{gap_description}. Here's where the rubric is seeing gaps:

  {dimension_1}: {score_1} -- {diagnosis_1}
  {dimension_2}: {score_2} -- {diagnosis_2}

Round {iteration}. {forward_guidance}.
```

**Variables:**
- `{score}`: Composite score (e.g., 0.89)
- `{gap_description}`: A factual statement of the gap (e.g., "Close -- three points from the line" for 0.89, or "Seven points from the line" for 0.85). The opening word should reflect the actual proximity -- use "Close" only when the score is genuinely near the threshold.
- `{dimension_N}`: Dimension name
- `{score_N}`: Dimension score
- `{diagnosis_N}`: Concrete explanation of the gap
- `{iteration}`: Current revision iteration number
- `{forward_guidance}`: E.g., "Tighten those two dimensions and you're over the threshold"

**Visual integration (FEAT-003):**
- Color: Yellow (`COLOR_REVISE`)
- Score: Bold
- Dimension scores: 2-space indent, no blank lines between them
- No decoration

### Template 3: Quality Gate REJECTED

The dimension block repeats once per underperforming dimension. Minimum 1, maximum 6.

**Multi-dimension case (2 or more underperforming dimensions):**
```
Quality gate: REJECTED -- {score}

This needs real work before the next pass. {count} dimensions are underperforming:

  {dimension}: {score} -- {diagnosis}
  {dimension}: {score} -- {diagnosis}
  [...repeat for each underperforming dimension...]

Start with {priority_dimension} -- it's pulling everything else down.
The gap to 0.92 is real. The path is clear.
```

**Single-dimension case (exactly 1 underperforming dimension):**
```
Quality gate: REJECTED -- {score}

This needs real work before the next pass. One dimension is underperforming:

  {dimension}: {score} -- {diagnosis}

Address {dimension} directly. The gap to 0.92 runs through here.
```

**Variables:**
- `{score}`: Composite score (e.g., 0.78)
- `{count}`: Number of underperforming dimensions (used only in multi-dimension case)
- `{dimension}`, `{score}`, `{diagnosis}`: Per-dimension breakdown — one block per underperforming dimension
- `{priority_dimension}`: The dimension to fix first (see selection algorithm below)

**Priority dimension selection algorithm:**
1. Select the dimension with the lowest raw score.
2. If two or more dimensions are within 0.02 of each other (i.e., a tie zone), prefer the dimension with the higher weight per quality-enforcement.md (Completeness and Internal Consistency 0.20 > Methodological Rigor 0.20 > Evidence Quality 0.15 > Actionability 0.15 > Traceability 0.10). Among equal weights, either may be selected.
3. In the single-dimension case, `{priority_dimension}` is that sole dimension; the "Start with" line simplifies to the single-dimension template above.

**Visual integration (FEAT-003):**
- Color: Red (`COLOR_REJECTED`)
- Score: Bold
- No humor. No emoji. No decoration.

### Template 4: Constitutional Compliance Failure

```
Constitutional compliance check: FAILED

Trigger: {auto_escalation_id} -- {trigger_description}.
Auto-escalation: {criticality}. This is not a drill.

Hard stop. Human review required before proceeding.
This is exactly the scenario the auto-escalation rules exist for.
```

**Variables:**
- `{auto_escalation_id}`: E.g., AE-001
- `{trigger_description}`: E.g., "docs/governance/JERRY_CONSTITUTION.md was modified"
- `{criticality}`: E.g., C4

**Visual integration (FEAT-003):**
- Color: Red (`COLOR_CONSTITUTIONAL`)
- "Hard stop" in Bold
- Zero decoration of any kind

### Template 5: Error (Missing Environment Variable)

```
{variable_name} not set.

{recovery_instructions}

{rule_id}: {rule_description}.
```

**Variables:**
- `{variable_name}`: E.g., JERRY_PROJECT
- `{recovery_instructions}`: Actionable steps with copy-pasteable commands
- `{rule_id}`: E.g., H-04
- `{rule_description}`: E.g., "active project required before proceeding"

**Visual integration (FEAT-003):**
- Color: Default (error identity comes from the content, not the color)
- Commands: Cyan (`COLOR_PATH`)
- Rule ID: Cyan (`COLOR_RULE`)

### Template 6: Session Start

```
Session live. Project: {project_id}

Enforcement architecture is up. Quality gates are set.
Let's build something worth scoring.
```

**Variables:**
- `{project_id}`: Active project ID

**Visual integration (FEAT-003):**
- Compact logo (Option A) may precede this message per FEAT-003 logo selection guidance
- Default color
- No decoration beyond optional logo

### Template 7: Session End (All Items Complete)

```
All items landed.

+----------------------------------+
|      SESSION COMPLETE            |
|  Every item: DONE                |
|  Saucer Boy approves.            |
+----------------------------------+

That's a powder day. See you next session.
```

**Visual integration (FEAT-003):**
- Box-art: Plus-and-dash pattern (Pattern 1)
- Color: Green (`COLOR_CELEBRATE`)
- Skier emoji (`skier`) prefix on "All items landed" in full terminals
- Celebration Tier 1 (Powder Day)

### Template 8: Session End (Partial)

```
Session ended. {completed_count} items complete, {remaining_count} remaining.

Progress is progress. See you next session.
```

**Visual integration (FEAT-003):**
- Default color
- No decoration (Celebration Tier 3: Nod)

### Template 9: Work Item State Change

```
{item_id}: {new_state}.
```

One line. No decoration. No personality.

### Template 10: SessionStart Hook (systemMessage)

```
Jerry Framework: {project_id} active. Quality gates set.
```

Under 80 characters. One terminal line.

### Template 11: Rule Explanation (Help Text)

```
{rule_id}: {rule_description}.

{threshold_or_constraint}

{reasoning}
```

**Variables:**
- `{rule_id}`: Rule identifier (e.g., H-13)
- `{rule_description}`: One-sentence statement of what the rule requires (e.g., "quality threshold is 0.92 for C2+ deliverables")
- `{threshold_or_constraint}`: The quantitative or structural constraint, stated plainly (e.g., "The 0.92 threshold is a governance decision (see quality-enforcement.md).")
- `{reasoning}`: The WHY behind the rule — 2–5 sentences explaining the logic that produced the constraint. Close with a direct sentence ("That's the logic." / "That's the tradeoff."). No humor. No metaphors.

**Notes:**
- Rule ID is the heading. No "H-13 says" preamble.
- The reasoning block explains the WHY, not the WHAT. The WHAT is already in `{rule_description}`.
- "That's the logic" (or equivalent direct closure) is the voice's contribution: treating the developer as someone who deserves the reasoning, not just the rule number.
- Use for inline rule explanation callouts, `--help` detail views, and onboarding documentation. Not for error messages (which use Templates 4–5 patterns).

**Visual integration (FEAT-003):**
- Rule ID: Cyan (`COLOR_RULE`)
- Body: Default color
- No decoration

### Template 12: Generic Error

For error types not covered by Template 4 (Constitutional Failure) or Template 5 (Missing Environment Variable). Covers: File Not Found, Validation Error, Command Dispatcher, Session Handlers, and future error sub-types.

```
{error_identity}.

{optional_explanation}

{optional_diagnostic_action}
```

**Variables:**
- `{error_identity}`: What failed, stated directly. No "Error:" prefix. No bureaucratic framing. (e.g., "File not found: projects/PROJ-003-je-ne-sais-quoi/PLAN.md")
- `{optional_explanation}`: One sentence of context when the cause is not self-evident. Omit if the identity is self-explanatory. For system-level failures, explicitly say this is a framework issue, not the developer's. (e.g., "This is an infrastructure error — the CLI handlers are not wired.")
- `{optional_diagnostic_action}`: One or more copy-pasteable commands the developer can run to investigate or recover. Omit if no useful diagnostic action exists.

**Population rules:**
- All three variables may be omitted if the identity alone is sufficient.
- Never omit `{error_identity}`.
- If the failure is the developer's action: include `{optional_diagnostic_action}`. If the failure is the system's fault: include `{optional_explanation}` acknowledging this; `{optional_diagnostic_action}` is optional.
- Do not add personality to error messages. The non-bureaucratic framing is the voice.

**Visual integration (FEAT-003):**
- Default color (error identity comes from content, not color)
- Diagnostic commands: Cyan (`COLOR_PATH`)
- No decoration

---

## Integration Workflow

This section defines how developers apply the Saucer Boy voice to new framework messages. The workflow uses the three `/saucer-boy` agents in sequence.

### Lightweight Path (Categories 4-6, Minimal Transformation)

For messages where the voice transformation is minimal (e.g., removing an "Error:" prefix, adding one line of guidance), the full 6-step workflow with 3 agent invocations is overhead. Use the lightweight path:

1. Write the message content.
2. Apply the Voice Application Guide for the relevant category directly (refer to the before/after pairs and boundary conditions in this document).
3. Self-check against Authenticity Test 1 (Information Completeness) and the category boundary conditions.

The full workflow (Steps 1-6 below) is REQUIRED for:
- Quality gate messages (Category 1)
- New error message types not covered by existing templates
- Session messages with celebration elements (Category 3, all-items-complete)
- Any message where voice transformation substantially changes the text

### Full Workflow (Categories 1-3, Novel Messages)

### Step 1: Write the Message Content First

Write the message with all required technical information. No voice, no personality. Focus on:

- What happened (state, score, error identity)
- Why it happened (dimension breakdown, trigger, cause)
- What to do (next action, recovery path, commands)

**Validation:** Apply Authenticity Test 1 (Information Completeness) to the draft. If removing all voice elements would leave the developer without what they need, the content is not ready for voice. Fix the information gap first.

### Step 2: Identify the Message Context

Look up the message's context in the Voice Application Guide (this document). If the audience context is not covered by an existing category, use the Audience Adaptation Matrix below. Determine:

- Tone spectrum position (Full Energy / Medium / Low / Hard Stop)
- Humor deployment level (Yes / Gentle / Light tone / None)
- Energy level (High / Medium / Low)
- Calibration pair from voice-guide.md

**Audience Adaptation Matrix (summary — source: ps-creator-001-draft.md Audience Adaptation Matrix)**

This table covers the audience contexts that appear in FEAT-004 message categories. For the full matrix (8 rows), see FEAT-002 SKILL.md.

| Audience Context | Energy Level | Humor Deployment | Technical Depth | Tone Anchor |
|-----------------|-------------|-----------------|-----------------|-------------|
| Active session (routine work) | Medium | Light tone | Medium | Collaborative |
| Debugging / error state | Low | None | High | Diagnostic |
| Celebration (milestone / all-done) | High | Yes (earned) | Low | Warm |
| Onboarding / new developer | Medium | Warm | Low | Invitation |
| Post-incident / hard stop | Low | None | High | Precise / Direct |
| Documentation / reference | Medium | None | High | Clarity |

**Selection rule:** Match the developer's likely state at the moment they see the message. An error message during a debug session maps to "Debugging / error state" even if the broader session context is routine work. Message-moment state takes precedence over session state.

### Step 3: Apply Voice via sb-rewriter

Invoke sb-rewriter with the draft text:

```
Use sb-rewriter to transform this message:

## SB CONTEXT (REQUIRED)
- **Text Path:** inline
- **Text Type:** {quality-gate|error|session|hook|documentation|cli-output}
- **Audience Context:** {active-session|debugging|onboarding|documentation|post-incident}

## TEXT TO REWRITE
{the draft message from Step 1}

## OPTIONAL CONTEXT
- **Downstream Feature:** FEAT-004
```

sb-rewriter will:
1. Extract all technical information from the draft
2. Apply the 5 voice traits (Direct, Warm, Confident, Occasionally Absurd, Technically Precise)
3. Self-apply the 5 Authenticity Tests before presenting the result
4. Annotate which traits were applied

### Step 4: Validate via sb-reviewer

Invoke sb-reviewer on the rewritten output:

```
Use sb-reviewer to check this message:

## SB CONTEXT (REQUIRED)
- **Text Path:** inline
- **Text Type:** {same as Step 3}
- **Audience Context:** {same as Step 3}

## TEXT TO REVIEW
{the rewritten message from Step 3}

## OPTIONAL CONTEXT
- **Downstream Feature:** FEAT-004
```

sb-reviewer will:
1. Apply all 5 Authenticity Tests in order (stopping at first failure)
2. Check all 8 boundary conditions
3. Report pass/fail per test with specific evidence and suggested fixes

### Step 5: Score via sb-calibrator

Invoke sb-calibrator on the validated output:

```
Use sb-calibrator to score this message:

## SB CONTEXT (REQUIRED)
- **Text Path:** inline
- **Text Type:** {same as Step 3}
- **Audience Context:** {same as Step 3}

## TEXT TO SCORE
{the validated message from Step 4}

## OPTIONAL CONTEXT
- **Downstream Feature:** FEAT-004
```

sb-calibrator will:
1. Score each of the 5 voice traits independently (0-1 scale)
2. Compute composite voice fidelity score
3. Provide per-trait improvement guidance

**Target:** Voice fidelity >= 0.90 (Strong assessment).

### Step 6: Iterate if Below Target

If the voice fidelity score is below 0.90:
1. Review sb-calibrator's per-trait improvement recommendations
2. Revise the message targeting the weakest trait
3. Re-run through Steps 3-5

The iteration cycle mirrors the quality gate's creator-critic-revision pattern (H-14) but for voice fidelity rather than content quality.

### Workflow Summary Diagram

```
  Write content    Identify context    Apply voice       Validate         Score
  (Step 1)     --> (Step 2)        --> sb-rewriter  --> sb-reviewer  --> sb-calibrator
       |                                (Step 3)        (Step 4)        (Step 5)
       |                                                                    |
       |                                                              >= 0.90?
       |                                                              /       \
       |                                                            YES       NO
       |                                                             |         |
       |                                                           DONE    Iterate
       |                                                                  (Step 6)
       |                                                                      |
       +---------- Fix information gap if Test 1 fails <----------------------+
```

---

## Anti-Patterns

These are messages that violate the Saucer Boy voice. Each includes the violation and the reason it fails. Use this section as a negative calibration reference.

### Anti-Pattern 1: Sarcasm Disguised as Wit

```
Quality gate: FAILED -- 0.72

Well, that was certainly an attempt. Maybe next time try reading
the requirements before writing the deliverable?
```

**Why it fails:** Mocks the developer. "Certainly an attempt" is sarcasm. "Maybe next time try reading" is passive-aggressive. Violates Boundary Condition #1 (NOT Sarcastic). McConkey's humor was inclusive -- laughing with, never at.

### Anti-Pattern 2: Performative Quirkiness

```
WHEEE! Quality gate PASS! You're a SUPERSTAR!
Your score is an AMAZING 0.94!!! Keep being awesome!!!
```

**Why it fails:** Try-hard enthusiasm. Multiple exclamation marks. "SUPERSTAR" and "AMAZING" are sycophantic. Violates Boundary Condition #5 (NOT Performative Quirkiness). Nobody talks like this. The persona doc's Energy Calibration section is explicit: "not caffeinated-influencer energy."

### Anti-Pattern 3: Humor That Obscures Diagnosis

```
Quality gate: REVISE -- 0.89

Looks like you almost shredded the gnar, dude! The moguls of internal
consistency got a little bumpy. Carve those turns tighter and you'll
be sending it in no time! Yeeeew!

Keep the stoke alive!
```

**Why it fails:** The developer cannot determine what specifically failed or what to fix. Every ski metaphor requires cultural knowledge. "Shredded the gnar," "moguls of internal consistency," and "sending it" are opaque to non-skiers. Violates Boundary Condition #7 (NOT a Replacement for Information), Boundary Condition #4 (NOT Bro-Culture Adjacent), and Authenticity Test 3 (New Developer Legibility).

### Anti-Pattern 4: Corporate Formalism

```
Dear Developer,

Thank you for your submission. After careful evaluation of your
deliverable against our quality enforcement standards, we regret
to inform you that the composite score of 0.89 falls below the
required threshold of 0.92.

We understand this may be disappointing. Please review the
attached dimension analysis for areas of improvement.

Best regards,
The Jerry Quality System
```

**Why it fails:** This is exactly the voice the persona replaces. "Dear Developer," "we regret to inform you," "attached dimension analysis," and "Best regards" are corporate formalism. The persona doc's Core Thesis: "The banana suit didn't make McConkey slower. Fear of looking silly would have." Fear of being direct is the equivalent.

### Anti-Pattern 5: Humor in High-Stakes Context

```
Constitutional compliance check: FAILED

Oopsie! Looks like someone touched the constitution!
Don't worry, it happens to the best of us. LOL.

Anyway, you should probably get a human to look at this.
```

**Why it fails:** Constitutional failures are not occasions for humor. "Oopsie" trivializes the stakes. "Don't worry" dismisses the seriousness. "LOL" and "Anyway" signal that the system does not take itself seriously. Violates Boundary Condition #2 (NOT Dismissive of Rigor) and #3 (NOT Unprofessional in High Stakes).

### Anti-Pattern 6: The Empty Personality

```
PASS. 0.94.
```

**Why it fails:** Contains all the information but none of the voice. This is the pre-Saucer-Boy state. The persona doc is clear that the voice is not a coating -- it IS Jerry's character. A PASS deserves at minimum the state, the score, the standout dimension, and the disposition. The voice adds the human acknowledgment that the developer has done good work.

### Anti-Pattern 7: Forced Skiing References

```
Session live. Time to schuss down the halfpipe of code quality!
The mogul fields of compliance await your pizza-and-french-fry technique!
```

**Why it fails:** "Schuss down the halfpipe," "mogul fields of compliance," and "pizza-and-french-fry technique" are forced metaphors that do not map to the framework's domain. The approved skiing vocabulary (voice-guide.md) is limited to terms that are transparent to non-skiers — meaning decodable from context without skiing knowledge, per Authenticity Test 3 (New Developer Legibility): "Could a developer unfamiliar with skiing or McConkey still extract all technical information without confusion?" A reader who does not ski knows that "clean run" means clean execution, "drop in" means start, and "powder day" means an exceptionally good day. "Schuss," "halfpipe," and "pizza-and-french-fry" do not decode without skiing knowledge. Violates Boundary Condition #5 (NOT Performative Quirkiness) and Authenticity Test 3 (New Developer Legibility).

### Anti-Pattern 8: Grandiosity

```
BEHOLD! THE QUALITY GATE HAS SPOKEN!

YOUR OFFERING HAS BEEN DEEMED... WORTHY.

Score: 0.94. The ancient threshold of 0.92 has been surpassed.
The prophecy is fulfilled.
```

**Why it fails:** Grandiosity. "BEHOLD," "DEEMED WORTHY," "ancient threshold," "prophecy" -- all of these treat the quality system as something mythical rather than functional. McConkey was never pretentious. The persona doc's Forbidden Constructions list explicitly includes "Behold, the quality gate has spoken."

---

## Visual Integration

> **Dependency note:** FEAT-003 (Visual Identity) is at v0.1.0 (DRAFT) as of this writing. The color constants (`COLOR_PASS`, `COLOR_REVISE`, `COLOR_REJECTED`, `COLOR_CONSTITUTIONAL`, `COLOR_PATH`, `COLOR_RULE`, `COLOR_SCORE`, `COLOR_CELEBRATE`) referenced in this section are proposed names pending FEAT-003 finalization. If FEAT-003 renames or restructures these constants, this section must be updated to match. The voice content in the templates is independent of the visual constants and will not require revision.

This section maps FEAT-003 visual identity decisions to each message category. It serves as the bridge between the Voice Application Guide and the terminal rendering implementation.

### Visual Budget Per Category

| Category | Color | Emoji | Box-Art | Bold | Dim |
|----------|-------|-------|---------|------|-----|
| QG PASS | Green | Checkmark (1 max) | None (unless streak/first) | Score | -- |
| QG REVISE | Yellow | None | None | Score | Dimension detail |
| QG REJECTED | Red | None | None | Score | Dimension detail |
| Constitutional Failure | Red | None | None | "Hard stop" | -- |
| Error Messages | Default | None | None | -- | Recovery commands in Cyan |
| Session Start | Default | None | Optional compact logo | -- | -- |
| Session End (partial) | Default | None | None | -- | -- |
| Session End (all done) | Green | Skier (1 max) | Plus-and-dash box | -- | -- |
| Work Item State Change | Default | None | None | -- | -- |
| Hook systemMessage | Default | None | None | -- | -- |
| Progress Tracker | Default | None | Established EPIC pattern | -- | -- |
| Rule Explanation | Default | None | None | Rule ID (Cyan) | -- |
| Help Text | Default | None | None | -- | -- |

### Graceful Degradation

Per FEAT-003, all messages function identically in three tiers:

| Tier | Environment | What Renders |
|------|-------------|-------------|
| Full | iTerm2, VS Code terminal, Windows Terminal | ANSI color + Unicode indicators + box-drawing |
| Reduced | macOS Terminal.app, basic SSH | ASCII box-drawing + basic ANSI |
| Minimal | CI logs, piped output, dumb terminals | Plain text, no escape codes |

The information is identical across all three tiers. Voice is expressed through word choice and structure, not through visual elements. Visual elements enhance; the voice carries.

### NO_COLOR Compliance

When `NO_COLOR` is set or `TERM=dumb`:
- All ANSI escape codes suppressed
- Unicode indicators replaced with ASCII text equivalents (`[PASS]`, `[FAIL]`)
- Box-art uses `+`, `-`, `|` only
- The voice content is unchanged -- only rendering changes

---

## Traceability

| Source | Role | Sections Referenced |
|--------|------|---------------------|
| `ps-creator-001-draft.md` (Persona Distillation v0.9.0) | Canonical voice source | Core Thesis, Voice Traits, Tone Spectrum, Humor Deployment Rules, Voice Guide pairs 1-9, Boundary Conditions, Audience Adaptation Matrix, Vocabulary Reference, Authenticity Tests, Implementation Notes (FEAT-004 section) |
| `ps-creator-002-draft.md` (FEAT-002 /saucer-boy Skill v0.6.0) | Voice enforcement mechanism | SKILL.md, Agent definitions (sb-reviewer, sb-rewriter, sb-calibrator), references/implementation-notes.md (FEAT-004 section), references/voice-guide.md, references/vocabulary-reference.md |
| `ps-creator-003-draft.md` (FEAT-003 Visual Identity v0.1.0) | Visual vocabulary | Terminal Color Palette, Iconography, Celebration Tiers, Diagnostic Tiers, Typography Guidelines, Graceful Degradation Matrix |
| `src/interface/cli/adapter.py` | Current CLI output baseline | print() statements for sessions, items, projects, config, transcript commands |
| `src/interface/cli/main.py` | Current CLI error messages | Error routing for session/items/projects/config/transcript commands |
| `scripts/session_start_hook.py` | Current hook output baseline | format_hook_output(), systemMessage construction, additionalContext XML |
| `.context/rules/quality-enforcement.md` | Quality gate SSOT | Score bands, dimensions, thresholds, criticality levels |

---

## Self-Review Verification (S-010)

Before finalizing this draft, the following verification was performed per H-15.

| Check | Status | Evidence |
|-------|--------|----------|
| All 6 message categories inventoried | PASS | Quality gate (4 sub-categories), Error (5 sub-types), Session (5 sub-types), Hook (3 sub-types), Progress (4 sub-types), Help/Documentation (3 sub-types) |
| Before/after examples for each category | PASS | Every category has at least one before/after pair with voice application notes |
| Tone spectrum position specified per category | PASS | Each category section opens with tone, humor, energy, technical depth |
| Humor deployment rules respected | PASS | REJECTED and Constitutional messages have "None" humor. PASS has "Yes." REVISE has "Gentle." Error has "Light tone." |
| Boundary conditions per category | PASS | Each category section closes with boundary conditions specific to that context |
| Message templates use placeholders | PASS | 12 templates with `{placeholder}` variables (Templates 1-10 as before; Template 11: Rule Explanation; Template 12: Generic Error) |
| Integration workflow references /saucer-boy agents | PASS | Steps 3-5 invoke sb-rewriter, sb-reviewer, sb-calibrator with SB CONTEXT blocks |
| Anti-patterns include WHY explanation | PASS | 8 anti-patterns, each with the specific boundary conditions / tests violated |
| Visual integration maps FEAT-003 | PASS | Visual Budget table, Graceful Degradation matrix, NO_COLOR compliance |
| Authenticity Test 1 (Information Completeness) enforced | PASS | Core Principle section. Every template preserves all technical information from the current voice. |
| Authenticity Test 3 (New Developer Legibility) | PASS | Skiing vocabulary limited to transparent terms. Anti-Pattern 3 and 7 explicitly address opaque metaphors. |
| Current CLI output baseline scanned | PASS | src/interface/cli/adapter.py (124 print statements), main.py (12 error messages), session_start_hook.py reviewed |
| H-23 navigation table present | PASS | Document Sections table with anchor links |
| H-24 anchor links in navigation | PASS | All section names use anchor link syntax |
| P-002 output persisted to file | PASS | Written to specified output path |
| FEAT-002 implementation-notes.md guidance followed | PASS | Priority order, voice calibration method, biographical anchors, workflow steps all incorporated |
| Voice consistent across categories while adapting to context | PASS | The 5 voice traits (Direct, Warm, Confident, Occasionally Absurd, Technically Precise) are applied at varying intensity per category, not switched on/off |

**Gaps identified during self-review:**

1. The current CLI codebase (`src/interface/cli/adapter.py`) uses bare `print()` statements with no formatting layer. Implementing the voiced templates will require either a message formatting layer or direct string changes. This document specifies WHAT the messages should say, not HOW the code delivers them. Implementation architecture is out of scope for the voice specification.

2. The hook output (`scripts/session_start_hook.py`) constructs systemMessage and additionalContext programmatically. Voice changes to systemMessage will require modifying the `format_hook_output()` function. The additionalContext (XML-tagged Claude context) should remain neutral per the Voice Application Guide.

3. JSON output mode exclusion is now documented in the Core Principle section as a scope exclusion.

4. FEAT-003 dependency: Visual integration references color constants (`COLOR_PASS`, etc.) that are pending FEAT-003 finalization. A dependency note has been added to the Visual Integration section header. Voice content is independent of these constants.

---

## Document Metadata

| Attribute | Value |
|-----------|-------|
| Version | 0.5.0 |
| Status | REVISED -- targeted revision pass (R4) addressing adv-scorer-004 findings (Evidence Quality 0.86, Completeness 0.88) |
| Agent | ps-creator-004 |
| Workflow | jnsq-20260219-001 |
| Phase | 3 -- Tier 2 Fan-Out |
| Feature | FEAT-004 Framework Voice & Personality |
| Criticality | C2 (Standard) |
| Date | 2026-02-19 |
| Self-review | S-010 applied; see [Self-Review Verification](#self-review-verification-s-010) |
| Critic review | ps-critic-004: 3 rounds complete (R1: S-010+S-003, R2: S-002, R3: S-007) + R4 targeted revision pass |
| Next step | adv-scorer-004 re-score (S-014) |

**Document History:**

| Version | Change | Author |
|---------|--------|--------|
| 0.1.0 | Initial draft | ps-creator-004 |
| 0.2.0 | R1 edits: S-010 self-refine + S-003 steelman (5 edits) | ps-creator-004 |
| 0.3.0 | R2 edits: S-002 devil's advocate (4 edits: lightweight path, missing categories, self-reference scope) | ps-creator-004 |
| 0.4.0 | R3 edits: S-007 constitutional compliance (2 edits: REVISE H-13 clarification, status) | ps-creator-004 |
| 0.5.0 | R4 targeted revision: Evidence Quality + Completeness fixes per adv-scorer-004 score report (6 surgical edits) | ps-critic-004 |
