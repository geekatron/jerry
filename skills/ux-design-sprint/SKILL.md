---
name: ux-design-sprint
description: "AJ&Smart Design Sprint 2.0 facilitation sub-skill for the /user-experience parent skill. Facilitates a structured four-day rapid prototyping and validation process compressed from the Google Ventures five-day Design Sprint (Knapp, Zeratsky & Kowitz, 2016; Courtney, 2019). Produces sprint artifacts including challenge maps, solution sketches, storyboards, realistic prototypes, and structured user interview findings with synthesis confidence gates. Invoke when teams need to rapidly validate a product concept, solve a critical design challenge through structured prototyping, test ideas with real users before committing to development, or explore solution directions when they do not know what to build. Triggers: design sprint, GV sprint, rapid prototyping, sprint week, map sketch decide test, 4-day sprint, design sprint 2.0, AJ Smart sprint, validate prototype, test with users, sprint facilitation."
version: "1.1.0"
agents:
  - ux-sprint-facilitator
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch, mcp__context7__resolve-library-id, mcp__context7__query-docs
activation-keywords:
  - "design sprint"
  - "GV sprint"
  - "rapid prototyping"
  - "sprint week"
  - "map sketch decide test"
  - "4-day sprint"
  - "design sprint 2.0"
  - "AJ Smart sprint"
  - "validate prototype"
  - "test with users"
  - "sprint facilitation"
  - "design sprint challenge"
  - "sprint storyboard"
---

<!-- VERSION: 1.1.0 | DATE: 2026-03-04 | SOURCE: skills/user-experience/SKILL.md | PARENT: /user-experience skill | REVISION: iter2 — add Context7 MCP to allowed-tools (T3 consistency), add HMW/interview citations, consolidate Wave Gating duplication -->

# Design Sprint Sub-Skill

> **Version:** 1.1.0
> **Framework:** Jerry User-Experience -- Design Sprint 2.0
> **Constitutional Compliance:** Jerry Constitution v1.0
> **Parent Skill:** `/user-experience` (`skills/user-experience/SKILL.md`)
> **Wave:** 5 (Process Intensives)
> **Project:** PROJ-022 User Experience Skill | GitHub Issue [#138](https://github.com/geekatron/jerry/issues/138)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Document Audience](#document-audience-triple-lens) | Triple-Lens audience guide |
| [Purpose](#purpose) | Sub-skill overview and key capabilities |
| [When to Use This Sub-Skill](#when-to-use-this-sub-skill) | Activation triggers and scope boundaries |
| [Available Agents](#available-agents) | Single agent with role, model, and output location |
| [P-003 Compliance](#p-003-compliance) | Worker agent hierarchy position |
| [Invoking the Agent](#invoking-the-agent) | Invocation via ux-orchestrator |
| [Methodology](#methodology) | AJ&Smart Design Sprint 2.0 four-day process with detailed phase activities |
| [Output Specification](#output-specification) | Output location, L0/L1/L2 structure, required sections |
| [Routing](#routing) | Keywords and lifecycle-stage routing integration |
| [Cross-Framework Integration](#cross-framework-integration) | Handoff from JTBD/heuristic evaluation and to Lean UX/HEART metrics |
| [Synthesis Hypothesis Confidence](#synthesis-hypothesis-confidence) | Confidence classifications for Design Sprint outputs |
| [Quality Gate Integration](#quality-gate-integration) | S-014 scoring and H-13 threshold enforcement |
| [Degraded Mode Behavior](#degraded-mode-behavior) | Operation when Figma or Miro MCP unavailable |
| [Wave Architecture](#wave-architecture) | Wave 5 entry criteria, bypass conditions |
| [Constitutional Compliance](#constitutional-compliance) | Governing principles and AI-facilitated sprint limitations |
| [Registration](#registration) | H-26 parent-routed registration model and AGENTS.md confirmation |
| [Deployment Status](#deployment-status) | Wave 5 stub agent status and implementation timeline |
| [Quick Reference](#quick-reference) | Common workflows and agent selection hints |
| [References](#references) | Full repo-relative paths, requirements traceability, external citations |

## Document Audience (Triple-Lens)

This SKILL.md serves multiple audiences:

| Level | Audience | Sections to Focus On |
|-------|----------|---------------------|
| **L0 (Stakeholder)** | Product managers, designers, sprint participants | [Purpose](#purpose), [When to Use This Sub-Skill](#when-to-use-this-sub-skill), [Quick Reference](#quick-reference) |
| **L1 (Developer)** | Engineers invoking the agent | [Invoking the Agent](#invoking-the-agent), [Methodology](#methodology), [Output Specification](#output-specification) |
| **L2 (Architect)** | Workflow designers, skill maintainers | [Cross-Framework Integration](#cross-framework-integration), [Synthesis Hypothesis Confidence](#synthesis-hypothesis-confidence), [Degraded Mode Behavior](#degraded-mode-behavior) |

---

## Purpose

The Design Sprint sub-skill provides structured facilitation for the AJ&Smart Design Sprint 2.0 process -- a four-day compressed format (Courtney, 2019) adapted from the original Google Ventures five-day Design Sprint (Knapp, Zeratsky & Kowitz, 2016). It targets tiny teams (1-5 people) who need to rapidly move from a design challenge to a tested prototype without committing months to development.

This sub-skill is part of Wave 5 (Process Intensives), requiring Wave 4 completion before standard deployment. It provides the most intensive, end-to-end design validation process in the `/user-experience` skill, producing high-confidence synthesis signals from direct user testing on Day 4. A wave bypass condition allows teams at product inception ("don't know what to build") to access Design Sprint without completing prior waves.

### Key Capabilities

- **Day 1: Map** -- Facilitates challenge definition, user journey mapping, expert interview structuring, sprint question formulation, and target selection (user + key moment). Produces a shared map of the problem space that aligns the sprint team.
- **Day 2: Sketch** -- Guides lightning demo research, facilitates the four-step sketch process (Notes, Ideas, Crazy 8s, Solution Sketch), and structures Art Museum voting. Produces individual solution sketches with structured selection rationale.
- **Day 3: Decide** -- Facilitates straw poll voting, supervote decision-making, winning sketch selection, assumption identification, and prototype storyboard creation. Produces a detailed storyboard ready for prototype construction.
- **Day 4: Test** -- Guides realistic prototype construction, structures interviews with 5 representative users (Nielsen, 2000), facilitates observation and note-taking, and identifies thematic patterns across interviews. Produces validated findings with HIGH synthesis confidence.
- **Cross-Framework Synthesis** -- Sprint findings feed directly into `/ux-lean-ux` (hypothesis generation from validated learnings), `/ux-jtbd` (validated job stories from user interviews), and `/ux-heuristic-eval` (post-sprint evaluation of the prototype).

---

## When to Use This Sub-Skill

Activate when:

- The team does not know what to build and needs a structured process to go from challenge to tested prototype
- A critical design challenge requires rapid validation before committing development resources
- The team needs to test a product concept with real users within a compressed timeframe
- Stakeholder alignment is needed around a shared understanding of the problem and solution direction
- Multiple competing solution ideas exist and the team needs a structured selection and testing process
- Starting a new product or feature initiative and wanting to validate assumptions early
- Transitioning from discovery research (JTBD) into concrete solution exploration
- A cross-functional team needs to align around a single prototype direction

Do NOT use for:

- Evaluating an existing interface against usability heuristics -- use `/ux-heuristic-eval` (Nielsen's 10) instead. Use heuristic evaluation for existing products; Design Sprint is for new concepts and major redesigns.
- Building or auditing a component library -- use `/ux-atomic-design` (Atomic Design) instead.
- Accessibility compliance auditing -- use `/ux-inclusive-design` (WCAG 2.2) instead.
- Measuring quantitative UX health metrics -- use `/ux-heart-metrics` (Google GSM) instead. Use HEART after the sprint to measure the validated concept.
- Understanding user motivations at the job level -- use `/ux-jtbd` (Jobs-to-Be-Done) instead. JTBD identifies what users want; Design Sprint tests specific solutions.
- Diagnosing behavioral bottlenecks in existing products -- use `/ux-behavior-design` (Fogg B=MAP) instead.
- Iterating on hypotheses through build-measure-learn cycles -- use `/ux-lean-ux` (Lean UX) instead. Lean UX iterates; Design Sprint validates a single prototype in 4 days.
- Prioritizing features by user satisfaction impact -- use `/ux-kano-model` (Kano) instead.
- Security-focused interface review -- use `/eng-team` instead.
- General research without UX design sprint focus -- use `/problem-solving` instead.

---

## Available Agents

| Agent | Role | Tier | Mode | Model | Output Location |
|-------|------|------|------|-------|-----------------|
| `ux-sprint-facilitator` | AJ&Smart Design Sprint 2.0 facilitation | T4 | Systematic | Opus | `skills/ux-design-sprint/output/{engagement-id}/ux-sprint-facilitator-{topic-slug}.md` |

**STUB:** The agent definition file (`skills/ux-design-sprint/agents/ux-sprint-facilitator.md`) is pending Wave 5 Phase 2 implementation as part of PROJ-022 EPIC-005. The SKILL.md specifies the methodology and output contract that the agent will implement.

**Tool tier:** T4 (External) = Read, Write, Edit, Glob, Grep, Bash + WebSearch, WebFetch, Context7 MCP. T4 access is required because Design Sprint facilitation benefits from external research during Day 1 expert interviews and Day 2 lightning demos (competitive analysis, industry precedent research). See `.context/rules/agent-development-standards.md` [Tool Security Tiers].

The agent produces output at three levels per AD-M-004:
- **L0 (Executive Summary):** Sprint challenge statement; winning solution summary; Day 4 test results (pass/fail per sprint question); top validated findings; recommended next steps.
- **L1 (Technical Detail):** Full four-day sprint artifact set: challenge map, expert interview notes, sprint questions, solution sketches with selection rationale, storyboard, prototype specification, structured interview findings with per-user pattern analysis.
- **L2 (Strategic Implications):** Sprint learning synthesis; validated vs. invalidated assumptions; product strategy implications; recommended follow-up activities (Lean UX cycles, heuristic evaluation, development planning); organizational sprint maturity assessment.

---

## P-003 Compliance

The `/ux-design-sprint` sub-skill contains a single **worker** agent. It is invoked by the `ux-orchestrator` (T5) via the Agent tool. The agent does NOT have Agent tool access and MUST NOT spawn sub-agents.

```
MAIN CONTEXT (user request)
    |
    v
ux-orchestrator (T5, Opus, Integrative) -- parent orchestrator
    |
    +-- ux-sprint-facilitator (T4, Systematic, Opus) -- THIS sub-skill's worker
    +-- [other sub-skill workers...]
```

**Enforcement:**
- `disallowedTools: [Agent]` declared in `skills/ux-design-sprint/agents/ux-sprint-facilitator.md` frontmatter
- P-003 prohibition in `skills/ux-design-sprint/agents/ux-sprint-facilitator.governance.yaml` `capabilities.forbidden_actions`
- CI gate validates no sub-skill agent has Agent access (documented in `skills/user-experience/rules/ci-checks.md`)

---

## Invoking the Agent

This is a sub-skill invoked by the `ux-orchestrator`, not directly by users. Users interact with the parent `/user-experience` skill, which routes to this sub-skill based on lifecycle-stage triage.

### Via Natural Language (to parent skill)

```
"We don't know what to build -- help us figure it out"
"Run a design sprint for the new mobile navigation"
"We need to validate our checkout redesign concept with real users"
"Facilitate a 4-day design sprint to explore our onboarding problem"
"Help us go from idea to tested prototype for the dashboard feature"
"Our team has 3 competing ideas for the settings page -- which one works?"
```

### Via Explicit Agent Request (to parent skill)

```
"Use ux-sprint-facilitator to facilitate a design sprint for the new payment flow"
"Have ux-sprint-facilitator run a Design Sprint 2.0 for our mobile app onboarding"
```

### Via Agent Tool (orchestrator internal)

The `ux-orchestrator` invokes the agent via the Agent tool:

```python
Agent(
    description="ux-sprint-facilitator: Design Sprint 2.0 for mobile navigation redesign",
    subagent_type="jerry:ux-sprint-facilitator",
    prompt="""
## UX CONTEXT (REQUIRED)
- **Engagement ID:** UX-0012
- **Topic:** Mobile Navigation Redesign Design Sprint
- **Product:** [product name, domain, and current navigation description]
- **Target Users:** [user segments and behavioral context]
- **Sprint Challenge:** [the big challenge or question the sprint aims to answer]
- **Sprint Questions:** [2-5 specific questions to answer by end of sprint]
- **Existing Research:** [upstream JTBD job statements, heuristic findings, user interviews]
- **MCP Availability:** Figma=[available/unavailable], Miro=[available/unavailable]

## TASK
Facilitate a complete AJ&Smart Design Sprint 2.0 for mobile navigation redesign.
1. Day 1 (Map): Define challenge, map user journey, identify target user + key moment, structure expert interviews, set sprint questions
2. Day 2 (Sketch): Conduct lightning demos, facilitate 4-step sketch (notes, ideas, crazy 8s, solution sketch), run Art Museum voting
3. Day 3 (Decide): Facilitate straw poll, supervote, select winning sketch, identify assumptions, create storyboard
4. Day 4 (Test): Specify realistic prototype, structure interviews with 5 users, analyze patterns, synthesize findings

## MANDATORY PERSISTENCE (P-002)
Create file at: skills/ux-design-sprint/output/UX-0012/ux-sprint-facilitator-mobile-navigation.md
"""
)
```

> **Governance codification (AD-M-007):** The session_context contract (on_receive/on_send) is specified in `ux-sprint-facilitator.governance.yaml` per AD-M-007. Fields are enumerated below:

**on_receive fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `engagement_id` | string | Yes | UX engagement identifier (format: `UX-{NNNN}`) |
| `product_context` | string | Yes | Product name, domain, current state, and target user description |
| `sprint_challenge` | string | Yes | The big question or problem the sprint aims to solve (e.g., "How might we reduce checkout abandonment for first-time buyers?") |
| `sprint_questions` | array | No | 2-5 specific questions to answer by end of sprint; if absent, Day 1 generates them |
| `upstream_artifacts` | array | No | File paths to upstream handoff artifacts (JTBD job statements, heuristic evaluation findings, prior research) |
| `mcp_availability` | object | No | MCP tool availability: `figma` (boolean), `miro` (boolean); determines degraded mode behavior |

**on_send fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `sprint_day_completed` | integer | Yes | Last completed sprint day (1-4); 4 indicates full sprint completion |
| `challenge_statement` | string | Yes | Finalized challenge statement from Day 1 |
| `prototype_fidelity` | enum | Yes | `high` (Figma interactive), `medium` (static mockups), `low` (paper/whiteboard) |
| `interview_count` | integer | Yes | Number of user interviews completed (target: 5 per Nielsen, 2000) |
| `theme_strength` | enum | Yes | `strong` (identified by >= 3 of 5 users), `moderate` (2 of 5), `weak` (1 of 5) |
| `usability_findings_count` | integer | Yes | Total usability findings from Day 4 interviews |
| `sprint_questions_answered` | array | Yes | Each sprint question with pass/fail/partial verdict and supporting evidence |
| `winning_sketch_summary` | string | Yes | Description of the selected solution direction from Day 3 |
| `validated_assumptions` | array | Yes | Assumptions confirmed by Day 4 testing |
| `invalidated_assumptions` | array | Yes | Assumptions disproven by Day 4 testing |
| `synthesis_judgments` | array | Yes | AI judgment calls with confidence classification and rationale |

---

## Methodology

### AJ&Smart Design Sprint 2.0

The AJ&Smart Design Sprint 2.0 (Courtney, 2019) compresses the original Google Ventures five-day Design Sprint (Knapp, Zeratsky & Kowitz, 2016) into four days by combining the original Day 1 (Understand) and Day 2 (Diverge) into a single Day 1 (Map), and merging the original Day 3 (Decide) with Day 4 (Prototype) into Day 3 (Decide + Storyboard). This produces a more intensive but faster sprint cadence while preserving the core methodology.

| Sprint Day | GV Equivalent | Primary Activity | Key Output |
|-----------|---------------|-----------------|------------|
| Day 1: Map | GV Days 1-2 | Challenge definition, journey mapping, expert interviews, sprint questions, sketching | Challenge map, sprint questions, solution sketches |
| Day 2: Sketch | GV Day 2 (cont.) | Lightning demos, 4-step sketch, Art Museum voting | Individual solution sketches with vote data |
| Day 3: Decide | GV Days 3-4 | Straw poll, supervote, winning sketch, storyboard, prototype specification | Storyboard, prototype plan |
| Day 4: Test | GV Day 5 | Prototype construction, 5-user interviews, pattern analysis | Validated findings, sprint verdict |

### Day 1: Map

**Purpose:** Align the sprint team around the challenge, map the problem space, gather expert knowledge, and set measurable sprint questions.

**Activities:**

1. **Challenge Definition** -- Articulate the sprint challenge as a "How Might We" (HMW) question (IDEO design thinking technique, Brown, 2009; adopted in Sprint methodology per Knapp et al., 2016, Chapter 4). The challenge should be specific enough to test in 4 days but broad enough to allow creative solutions. Example: "How might we reduce first-time buyer checkout abandonment from 68% to under 40%?"

2. **Long-Term Goal** -- Define what success looks like 6-12 months from now. This anchors the sprint against strategic objectives, not just tactical improvements.

3. **Sprint Questions** -- Formulate 2-5 specific, testable questions that the sprint must answer. Sprint questions should be phrased as "Can we...?" or "Will users...?" to enable clear pass/fail assessment on Day 4. Example: "Will users understand the new progress indicator without instruction?"

4. **User Journey Map** -- Map the end-to-end user journey for the target behavior, from first awareness through the desired action. Identify: entry points, key decision moments, friction points, and the critical moment (the single most important interaction to get right).

5. **Target Selection** -- Choose the target user segment and the key moment in the journey that the sprint will focus on. The key moment is the narrowest scope that still addresses the sprint challenge. Per Knapp et al. (2016): "Pick the most important customer and the most important moment."

6. **Expert Interviews** -- Conduct structured "How Might We" interviews with 3-5 domain experts (product owner, support representative, technical lead, existing users if available). Each interview is 15-20 minutes. Capture HMW notes on individual cards/items for later clustering.

7. **HMW Clustering** -- Group HMW notes by theme. Vote to identify the most promising opportunity areas. Place winning HMW clusters on the journey map at the relevant moments.

**Output:** Challenge map document containing: HMW challenge statement, long-term goal, sprint questions (2-5), annotated user journey map, target user + key moment selection, expert interview summaries, clustered HMW notes.

### Day 2: Sketch

**Purpose:** Generate individual solution ideas through structured sketching exercises, then surface and compare solutions through Art Museum voting.

**Activities:**

1. **Lightning Demos** -- Each participant (or the facilitator for the team) reviews 3-5 inspiring examples from other products, industries, or domains that solve analogous problems. Capture "big ideas" from each demo. External research via WebSearch/WebFetch supports this activity.

2. **Four-Step Sketch** -- Individual sketching process (Knapp et al., 2016):
   - **Step 1: Notes** (20 min) -- Review Day 1 outputs. Take personal notes on key insights, constraints, and opportunities.
   - **Step 2: Ideas** (20 min) -- Rough idea generation. Sketchy, informal, quantity over quality. No judgment.
   - **Step 3: Crazy 8s** (8 min) -- Fold paper into 8 panels. One variation per panel, one minute each. Forces rapid iteration on the strongest idea from Step 2.
   - **Step 4: Solution Sketch** (30-90 min) -- Detailed, self-explanatory 3-panel storyboard of the best solution. Must be understandable without verbal explanation. Anonymous (no names on sketches).

3. **Art Museum** -- All solution sketches posted on a wall (or Miro board). Silent review period where participants place dot votes on compelling elements. Heat map emerges showing which solutions and elements attract the most attention.

4. **Speed Critiques** -- Brief 3-minute presentations of each sketch by the facilitator (not the author). Author clarifies only at the end. Team discusses strengths and concerns.

**Output:** Collection of solution sketches with vote data, lightning demo research notes, Art Museum heat map results.

### Day 3: Decide

**Purpose:** Select the winning solution, identify critical assumptions, and create a detailed storyboard for prototype construction.

**Activities:**

1. **Straw Poll** -- Each team member places one "super dot" on the solution (or solution element) they believe best addresses the sprint challenge. Non-binding poll to surface initial preferences.

2. **Supervote** -- The Decider (product owner or designated decision-maker) places 3 supervote dots. The Decider's votes determine the direction. Per Knapp et al. (2016): "The Decider has final say." If no human Decider is designated, the facilitator presents a ranked recommendation based on straw poll consensus, Day 1 sprint question alignment, and feasibility assessment, then asks the user to confirm.

3. **Rumble or All-in-One** -- If two strong but incompatible solutions survive the supervote: Rumble (test both in the prototype as A/B variants) or All-in-One (combine compatible elements). The Decider chooses the approach.

4. **Assumption Identification** -- Extract the critical assumptions embedded in the winning solution. Each assumption is phrased as a testable statement: "Users will [expected behavior] when [condition]." Classify as: must-be-true (sprint fails if wrong), nice-to-have (enhances but not critical), or unknown (requires investigation).

5. **Storyboard** -- Create a detailed 10-16 panel storyboard that narrates the user's interaction with the prototype from opening scene through completion. Each panel specifies: screen state, user action, system response, and emotional state. The storyboard serves as the prototype construction blueprint.

6. **Prototype Specification** -- Define the prototype scope: which screens to build, interaction fidelity level (clickable prototype vs. static mockups vs. wizard-of-oz), data requirements (realistic content vs. placeholder), and tools (Figma, paper, presentation software).

**Output:** Decision record (winning sketch, selection rationale, Decider identity), assumption inventory, detailed storyboard (10-16 panels), prototype specification.

### Day 4: Test

**Purpose:** Build a realistic prototype, test it with 5 representative users, and identify validated patterns.

**Activities:**

1. **Prototype Construction** -- Build the prototype per the Day 3 storyboard and specification. Fidelity should be "just enough" to feel real without over-investing. Per Knapp et al. (2016): "A Goldilocks quality prototype -- just real enough." The facilitator provides guidance on prototype scope and structure; actual construction may use Figma MCP (if available) or manual methods.

2. **Interview Script Preparation** -- Structure a 60-minute interview protocol (Knapp et al., 2016, Chapter 14 "Friday: Test"):
   - **Context Questions** (5 min): Background about the user's relationship to the problem domain
   - **Task Introduction** (5 min): Set up the scenario without leading the user
   - **Prototype Walkthrough** (30 min): User completes tasks while thinking aloud; facilitator observes without guiding
   - **Debrief Questions** (15 min): Open-ended reflection on the experience
   - **Wrap-up** (5 min): Final impressions, anything the user wants to add

3. **User Interviews** -- Conduct structured interviews with 5 representative users (Nielsen, 2000). Five users are sufficient to identify approximately 85% of usability problems. Each interview follows the prepared script. Record observations against the sprint questions.

4. **Observation Grid** -- During each interview, the sprint team (or facilitator) records observations in a grid: rows = sprint questions + key screens, columns = users (U1-U5). Each cell captures: positive reaction (+), negative reaction (-), or neutral observation (~). Color-code for quick pattern identification.

5. **Pattern Analysis** -- After all 5 interviews, analyze the observation grid:
   - **Strong theme** (>= 3 of 5 users): Validated finding with HIGH synthesis confidence
   - **Moderate theme** (2 of 5 users): Noteworthy finding requiring additional validation (MEDIUM confidence)
   - **Weak theme** (1 of 5 users): Individual observation, not a pattern (noted but not actionable)

6. **Sprint Question Verdict** -- For each sprint question, assign a verdict:
   - **Pass**: Strong positive theme (>= 3 users completed the expected behavior without significant difficulty)
   - **Fail**: Strong negative theme (>= 3 users could not complete or expressed clear confusion/frustration)
   - **Partial**: Mixed results or moderate themes; requires follow-up investigation

7. **Findings Synthesis** -- Compile validated findings, categorize by severity and frequency, map findings to assumptions (validated vs. invalidated), and produce the sprint outcome summary.

**Output:** Prototype reference (file path or description), interview observation grid, thematic analysis with pattern strength, sprint question verdicts, assumption validation results, findings synthesis with confidence classifications.

### Execution Phases (Agent Internal)

> **Note:** This execution procedure describes target behavior for the fully-implemented `ux-sprint-facilitator` agent. The current agent definition is a Wave 5 stub; full implementation will follow this specification.

The facilitator follows a 5-phase sequential workflow corresponding to the sprint structure plus a synthesis phase. Each phase produces intermediate artifacts that feed the next.

#### Phase 1: Sprint Setup and Day 1 (Map)

**Purpose:** Establish sprint context, confirm wave entry criteria, and execute Day 1 activities.

**Activities:**
1. Confirm Wave 5 entry criteria are met: Wave 4 completed (30+ users for Kano survey OR 1 B=MAP bottleneck diagnosed), OR bypass condition satisfied (team at product inception with existing user research). *(Verification: check for `WAVE-4-SIGNOFF.md` in `skills/user-experience/output/`; if absent, ask user per H-31.)*
2. Catalog upstream inputs: check for `/ux-jtbd` job statements (job statement + switch forces feed the challenge statement); check for `/ux-heuristic-eval` findings (severity-rated findings provide problem context)
3. Execute Day 1 activities: challenge definition, long-term goal, sprint questions, user journey map, target selection, expert interviews, HMW clustering
4. Produce Day 1 output artifact: challenge map document

**Output:** Sprint setup brief (wave entry verification, upstream input inventory) and Day 1 challenge map.

#### Phase 2: Day 2 (Sketch)

**Purpose:** Generate and surface solution ideas.

**Activities:**
1. Conduct lightning demos using WebSearch/WebFetch for external research on analogous solutions
2. Facilitate 4-step sketch process (Notes, Ideas, Crazy 8s, Solution Sketch)
3. Structure Art Museum voting and speed critiques
4. Produce Day 2 output: solution sketches with vote data

**Output:** Lightning demo research notes, solution sketch descriptions, Art Museum results.

#### Phase 3: Day 3 (Decide)

**Purpose:** Select winning solution and create prototype blueprint.

**Activities:**
1. Facilitate straw poll and supervote (present recommendation if no human Decider designated)
2. Identify and classify critical assumptions
3. Create detailed storyboard (10-16 panels)
4. Specify prototype scope and fidelity

**Output:** Decision record, assumption inventory, storyboard, prototype specification.

#### Phase 4: Day 4 (Test)

**Purpose:** Construct prototype, test with users, and analyze results.

**Activities:**
1. Guide prototype construction (Figma MCP if available, manual methods otherwise)
2. Prepare structured interview script
3. Facilitate 5-user interview process and observation grid
4. Conduct pattern analysis using the >= 3 of 5 threshold for strong themes
5. Assign sprint question verdicts (pass/fail/partial)

**Output:** Prototype reference, interview observation grid, pattern analysis, sprint question verdicts.

#### Phase 5: Synthesis and Handoff Preparation

**Purpose:** Synthesize all sprint findings, produce L0/L1/L2 output artifact, and construct downstream handoffs.

**Activities:**
1. Produce L0 executive summary: sprint challenge, winning solution, Day 4 verdicts, top findings, next steps
2. Produce L1 technical detail: full four-day artifact set with evidence citations
3. Produce L2 strategic implications: validated/invalidated assumptions, product strategy implications, follow-up recommendations, sprint maturity assessment
4. Compile Synthesis Judgments Summary: every AI judgment call with confidence classification and rationale
5. Prepare downstream handoffs: `/ux-lean-ux` (validated prototype + Day 4 findings for hypothesis iteration), `/ux-heuristic-eval` (prototype for post-sprint evaluation), `/ux-jtbd` (validated job stories from user interviews)
6. Map findings to sprint questions; produce final sprint verdict

**Output:** Complete output artifact per Required Output Sections. Handoff payloads for downstream sub-skills.

---

## Output Specification

### Output Location

```
skills/ux-design-sprint/output/{engagement-id}/ux-sprint-facilitator-{topic-slug}.md
```

Where:
- `{engagement-id}` follows the pattern `UX-{NNNN}` (e.g., `UX-0012`)
- `{topic-slug}` is a kebab-case descriptor of the sprint challenge (e.g., `mobile-navigation`, `checkout-redesign`, `onboarding-flow`)

### Required Output Sections

| Section | Level | Content |
|---------|-------|---------|
| **Executive Summary** | L0 | Sprint challenge statement; winning solution summary; Day 4 test results (pass/fail/partial per sprint question); top validated findings; recommended next steps |
| **Sprint Context** | L1 | Product description, target users, sprint participants, upstream inputs (JTBD job statements, heuristic findings), wave entry verification, MCP availability |
| **Day 1: Map** | L1 | HMW challenge statement, long-term goal, sprint questions (2-5), annotated user journey map, target user + key moment, expert interview summaries, HMW clusters |
| **Day 2: Sketch** | L1 | Lightning demo research notes, solution sketch descriptions, Crazy 8s variations summary, Art Museum vote results, speed critique highlights |
| **Day 3: Decide** | L1 | Straw poll results, supervote outcome, Decider identity and rationale, Rumble/All-in-One decision, assumption inventory (must-be-true/nice-to-have/unknown), storyboard (10-16 panels), prototype specification |
| **Day 4: Test** | L1 | Prototype reference (fidelity level, tool used), interview script summary, observation grid (5 users x sprint questions), pattern analysis with theme strength, sprint question verdicts (pass/fail/partial), assumption validation results |
| **Strategic Implications** | L2 | Sprint learning synthesis; validated vs. invalidated assumptions mapped to product strategy; recommended follow-up (Lean UX cycles, heuristic evaluation, development planning); organizational sprint maturity assessment; competitive positioning insights from lightning demos |
| **Synthesis Judgments Summary** | L1 | Each AI judgment call listed for synthesis confidence gate compliance |
| **Handoff Data** | L1 | Structured data for downstream sub-skills: validated prototype + findings for `/ux-lean-ux`; prototype reference for `/ux-heuristic-eval`; validated job stories for `/ux-jtbd` |

**Synthesis Judgments Summary requirements:** MUST list every AI judgment (sprint question framing, sketch selection recommendations, assumption classification, pattern strength assessment, sprint question verdicts) with confidence classification (HIGH/MEDIUM/LOW) and rationale. Each judgment row includes: finding ID, framework source (e.g., Day 1 challenge framing, Day 3 assumption classification, Day 4 pattern analysis), confidence level (HIGH/MEDIUM/LOW), and rationale explaining the classification basis and evidence chain. Follows the pattern in `skills/user-experience/rules/synthesis-validation.md`.

### Templates

| Template | Path | Purpose |
|----------|------|---------|
| Design Sprint Template | `skills/ux-design-sprint/templates/design-sprint-template.md` | Four-day sprint artifact structure with observation grid, storyboard panels, and sprint question verdict format |

---

## Routing

### Trigger Keywords

| Keyword | Routing Context |
|---------|----------------|
| design sprint | Direct match -- primary trigger |
| GV sprint | Direct match (Google Ventures sprint) |
| rapid prototyping | In combination with sprint/validation context |
| sprint week | Direct match |
| map sketch decide test | Direct match (sprint day names) |
| 4-day sprint | Direct match |
| design sprint 2.0 | Direct match (AJ&Smart format) |
| AJ Smart sprint | Direct match |
| validate prototype | In combination with sprint/user testing context |
| test with users | In combination with prototype/sprint context (not general usability testing) |
| sprint facilitation | Direct match |
| design sprint challenge | Direct match |
| sprint storyboard | In combination with sprint/prototype context |

### Lifecycle-Stage Routing Integration

This sub-skill is routed to by the `ux-orchestrator` in the following lifecycle-stage scenarios:

| Stage | User Intent | Route Condition |
|-------|-------------|-----------------|
| Before design | "Need validated prototype" | Direct route to `/ux-design-sprint`; source: `skills/user-experience/rules/ux-routing-rules.md` Stage Routing Table (pending EPIC-001 completion) |
| Product inception | "Don't know what to build" | Wave bypass route to `/ux-design-sprint`; team has no existing product but needs structured exploration |
| Before design | Follow-up from JTBD discovery | When `/ux-jtbd` has produced job statements + switch forces; job statement feeds the sprint challenge definition |
| Any stage | "Validate a design concept quickly" | Qualification question: "Do you need a full 4-day sprint process or a quick evaluation?" -> Full sprint: `/ux-design-sprint`; Quick evaluation: `/ux-heuristic-eval`; source: `skills/user-experience/rules/ux-routing-rules.md` Common Intent Resolution (pending EPIC-001 completion) |

### Wave Gating

This sub-skill is in **Wave 5** (Process Intensives). See [Wave Architecture](#wave-architecture) for entry criteria, bypass condition, and terminal wave status.

---

## Cross-Framework Integration

### Upstream Inputs

This sub-skill receives context from other sub-skills when invoked as part of a multi-sub-skill workflow:

| From Sub-Skill | Handoff Artifact | Key Fields | Usage |
|----------------|-----------------|-----------|-------|
| `/ux-jtbd` | Job statement + switch forces | Job statement, push/pull forces, hiring criteria, anxieties, habits | JTBD job statement feeds the Day 1 challenge definition; switch forces inform sprint question formulation; hiring criteria shape the target user selection |
| `/ux-heuristic-eval` | Severity-rated findings | Finding ID, heuristic violated, severity (0-4), affected screen/flow | Heuristic findings identify specific usability problems that the sprint can address; high-severity findings (>= 3) may define the sprint challenge directly |

### Downstream Handoffs

This sub-skill produces artifacts that feed into other sub-skills via the Jerry handoff protocol (`docs/schemas/handoff-v2.schema.json`).

| To Sub-Skill | Handoff Artifact | Key Fields | Trigger |
|-------------|-----------------|-----------|---------|
| `/ux-lean-ux` | Validated prototype + Day 4 findings | Prototype reference, validated/invalidated assumptions, sprint question verdicts, usability findings, theme strength | After Day 4 completion; Lean UX uses sprint findings to generate hypothesis backlog for iterative experimentation |
| `/ux-heuristic-eval` | Prototype for post-sprint evaluation | Prototype reference (Figma link or file path), prototype fidelity level, key interaction flows | After sprint completion; heuristic evaluation provides systematic usability audit of the sprint prototype |
| `/ux-jtbd` | Validated job stories from user interviews | Interview observation grid, user quotes, validated behaviors, job story candidates | After Day 4 interviews; user testing reveals actual jobs and switching triggers that refine JTBD job statements |

**Handoff data format (handoff-v2 + ux-ext):**

```yaml
handoff:
  from_agent: ux-sprint-facilitator
  to_agent: ux-lean-ux-experimenter
  task: "Generate Lean UX hypothesis backlog from Design Sprint findings"
  success_criteria:
    - "Hypotheses generated for each validated and invalidated sprint assumption"
    - "Experiment designs prioritize assumptions that were partially validated"
  artifacts:
    - "skills/ux-design-sprint/output/{engagement-id}/ux-sprint-facilitator-{topic-slug}.md"
  key_findings:
    - "Sprint verdict: {pass/fail/partial} on {N} sprint questions"
    - "Strong themes (>= 3/5 users): {theme_count} findings"
    - "Invalidated assumptions: {list}"
  blockers: []
  confidence: 0.75
  criticality: C2
  ux_ext:
    sprint_day_completed: 4
    prototype_fidelity: "{high|medium|low}"
    interview_count: 5
    theme_strength: "{strong|moderate|weak}"
    usability_findings_count: "{N}"
```

### Canonical Multi-Skill Workflow Sequences

This sub-skill participates in the following canonical sequences:

| Sequence | Skills Involved | This Sub-Skill's Role |
|----------|----------------|-----------------------|
| Discovery to Sprint | `/ux-jtbd` then **`/ux-design-sprint`** | Receives JTBD job statement and switch forces; uses them to frame the sprint challenge and target user selection |
| Sprint to Iterate to Measure | **`/ux-design-sprint`** then `/ux-lean-ux` then `/ux-heart-metrics` | Produces validated prototype and Day 4 findings; Lean UX iterates on hypotheses; HEART measures validated concept |
| Sprint to Evaluate | **`/ux-design-sprint`** then `/ux-heuristic-eval` | Produces prototype for systematic usability evaluation against Nielsen's 10 heuristics |

---

## Synthesis Hypothesis Confidence

Design Sprint outputs include synthesis hypotheses that carry confidence classifications per the synthesis validation protocol.

| Synthesis Step | Typical Confidence | Rationale |
|---------------|-------------------|-----------|
| Day 4 interview thematic analysis | HIGH | Based on direct user interviews (5 users per Sprint methodology; Knapp, Zeratsky & Kowitz, 2016). Themes identified by >= 3 of 5 users meet the strong theme threshold. Direct user observation provides the highest-quality evidence available in the UX skill framework. |
| Day 2 sketch selection rationale | MEDIUM | Selection rationale involves subjective judgment among sprint participants. Art Museum voting provides structured input but the Decider's supervote introduces individual judgment. Rationale is documented but not empirically validated until Day 4. |

**Gate enforcement:**
- **HIGH outputs (Day 4 thematic analysis):** Include "Synthesis Judgments Summary" section. User reviews output + acknowledges specific AI judgment calls before design recommendations are generated. Strong themes (>= 3 of 5 users) advance directly; moderate themes (2 of 5) require acknowledgment of lower evidence strength.
- **MEDIUM outputs (sketch selection rationale):** Include "Validation Required" section noting that selection rationale is validated by Day 4 testing. If Day 4 confirms the selected solution addresses user needs, confidence may be elevated to HIGH in the synthesis findings.

**Note on confidence dynamics:** Day 4 thematic analysis represents one of the highest-confidence synthesis sources in the entire `/user-experience` skill because it is based on direct user observation. When Design Sprint findings converge with findings from a second framework (e.g., `/ux-heuristic-eval` confirms usability issues identified in Day 4), synthesis confidence is reinforced. Day 2 sketch selection starts at MEDIUM but is validated or invalidated by Day 4 testing, creating an internal confidence progression within a single sprint.

### Signal Extraction

- Signals extracted from Day 4 interview findings
- Threshold: Interview themes identified by >= 3 of 5 users
- Evidence base: Direct user observation during structured testing

---

## Quality Gate Integration

Design Sprint outputs are subject to the Jerry quality gate per H-13 and H-14:

| Quality Check | Threshold | Application |
|---------------|-----------|-------------|
| S-014 LLM-as-Judge scoring | >= 0.92 composite (C2+) | Applied at Phase 5 completion |
| Creator-critic-revision | Minimum 3 iterations (H-14) | Orchestrator manages revision cycles |
| Self-review (S-010) | Required before presenting | Self-review before returning to orchestrator |
| Wave transition gate | S-014 composite >= 0.85 | Applied at Wave 4 -> 5 transition |

**Scoring dimensions (Design Sprint interpretation):**

| Dimension | Weight | Interpretation |
|-----------|--------|----------------|
| Completeness | 0.20 | All four sprint days documented; all sprint questions addressed; observation grid complete for 5 users |
| Internal Consistency | 0.20 | Day 4 findings consistent with Day 3 assumptions; sprint verdicts consistent with observation grid data; handoff data consistent with findings |
| Methodological Rigor | 0.20 | AJ&Smart Design Sprint 2.0 methodology correctly applied; 4-step sketch process followed; 5-user interview target met; observation grid structured per sprint questions |
| Evidence Quality | 0.15 | Day 4 findings cite specific user observations; pattern strength based on user count threshold (>= 3 of 5); quotes and behaviors recorded per user |
| Actionability | 0.15 | Sprint verdicts clearly pass/fail/partial; next steps specific and actionable; handoff data sufficient for downstream sub-skills |
| Traceability | 0.10 | Sprint questions trace to challenge statement; findings trace to observation grid; assumptions trace to storyboard; synthesis judgments documented |

### CI Gate Summary

The following CI gate criteria apply to this sub-skill (full gate definitions in `skills/user-experience/rules/ci-checks.md`):

| Gate | Check | Enforcement |
|------|-------|-------------|
| **No Agent tool access** | `disallowedTools: [Agent]` present in agent frontmatter; agent MUST NOT have Agent in `tools` list | L5 (CI): grep agent frontmatter for Agent tool presence |
| **P-003 forbidden action** | `capabilities.forbidden_actions` in `.governance.yaml` MUST include P-003 recursive subagent prohibition | L5 (CI): schema validation of governance YAML against `docs/schemas/agent-governance-v1.schema.json` |
| **Output schema validation** | Agent output MUST contain all Required Output Sections (Executive Summary, Sprint Context, Day 1-4, Strategic Implications, Synthesis Judgments Summary, Handoff Data) | L4 (post-tool): section heading presence check on output artifact |

---

## Degraded Mode Behavior

The `ux-sprint-facilitator` operates at T4 (External) and has access to WebSearch, WebFetch, and Context7 MCP. Additionally, it depends on Figma (REQ) for prototype creation and Miro (REQ) for collaborative sprint activities. Both MCP dependencies are required, so degraded mode behavior is significant.

### Figma MCP Unavailable

When Figma MCP is not available, prototype creation falls back to manual methods:

| Limitation | Impact | Mitigation |
|-----------|--------|-----------|
| No interactive prototype creation | Cannot build clickable Figma prototype for Day 4 testing | Guide user to create prototype manually using presentation software (Keynote, PowerPoint), paper prototyping, or an alternative prototyping tool. Adjust prototype_fidelity to `medium` or `low`. |
| No component inspection | Cannot reference existing design system components in prototype | Ask user to provide screenshots of existing components or describe their design system manually |
| Reduced prototype realism | Day 4 test results may be influenced by lower prototype fidelity | Note prototype fidelity in output; flag that findings may differ with higher-fidelity prototype per P-022 |

**Fallback mode:** Miro-only mode -- sprint exercises (journey mapping, HMW clustering, Art Museum) conducted in Miro; prototype constructed manually outside the MCP ecosystem. Per parent SKILL.md: "Miro-only mode: sprint exercises in Miro; manual prototype reference."

### Miro MCP Unavailable

When Miro MCP is not available, collaborative sprint activities fall back to local-file methods:

| Limitation | Impact | Mitigation |
|-----------|--------|-----------|
| No collaborative whiteboarding | Cannot use shared Miro board for journey mapping, HMW clustering, Art Museum voting | Use markdown-based sprint boards: journey map as a structured table, HMW notes as a bulleted list, Art Museum as a ranked list with vote counts |
| No real-time visual collaboration | Sprint team cannot see each other's contributions simultaneously | Facilitator compiles contributions into a single markdown document; sequential rather than simultaneous input |
| Reduced Art Museum effectiveness | Dot voting less intuitive without visual spatial layout | Use numbered ranking instead of spatial dot voting; facilitator tabulates votes |

**Fallback mode:** Local-file sprint boards -- all sprint artifacts produced as structured markdown documents. The methodology remains identical; only the collaboration medium changes from visual board to text-based format.

### Both Figma and Miro Unavailable

When both required MCPs are unavailable, the sprint operates in fully degraded text-only mode:

| Aspect | Degraded Approach |
|--------|------------------|
| Day 1 journey map | Structured markdown table: steps, user actions, pain points, opportunities |
| Day 2 sketches | Text descriptions of solution concepts; user asked to sketch manually and describe |
| Day 3 storyboard | Numbered panel descriptions in markdown; user asked to sketch panels manually |
| Day 4 prototype | Paper prototype or presentation-based prototype; user constructs offline |

**Degraded mode disclosure (P-022):**
```
[DEGRADED MODE] This sprint was facilitated without Figma and/or Miro MCP access.
Limitations:
- Prototype fidelity: {low|medium} (no Figma interactive prototype)
- Sprint board format: {markdown-based|text-only} (no Miro collaborative board)
- Day 4 findings may be influenced by prototype fidelity limitations
- Art Museum voting conducted via {ranked list|numbered voting} (no spatial dot voting)
Impact: Sprint methodology is fully preserved; collaboration and prototype fidelity are reduced.
```

### No Upstream Research

When invoked without prior `/ux-jtbd` output or `/ux-heuristic-eval` findings (e.g., direct invocation for product inception), the facilitator runs Day 1 challenge definition from scratch using user-provided context and sprint team knowledge. This is a valid and common sprint entry point -- many sprints begin without prior formal research.

---

## Wave Architecture

### Wave 5: Process Intensives

This sub-skill is part of Wave 5 (Process Intensives), alongside `/ux-ai-first-design` (CONDITIONAL).

**Entry criteria:** Wave 4 completed -- 30+ users for Kano survey OR 1 B=MAP bottleneck diagnosed.

**Bypass condition:** Design Sprint can proceed without Kano prerequisite if team has existing user research. This is the most significant bypass in the wave architecture because teams at product inception have the strongest need for Design Sprint and the least ability to satisfy Wave 4 advanced analytics prerequisites. Bypass requires 3-field documentation: unmet criterion, impact assessment ("sprint proceeds without Kano feature prioritization context; team has user research from other sources"), and remediation plan with target date.

**Wave transition (terminal wave):** Wave 5 is the final wave. When `WAVE-5-SIGNOFF.md` is valid, the orchestrator enters full operational mode with all 10 sub-skills deployed.

---

## Constitutional Compliance

All agents in this sub-skill adhere to the **Jerry Constitution v1.0**:

| Principle | Requirement | Consequence of Violation |
|-----------|-------------|-------------------------|
| P-003 | NEVER spawn recursive subagents -- worker agent, no Agent tool access | Agent hierarchy violation; uncontrolled token consumption |
| P-020 | NEVER override the Decider's sprint decisions or user priorities on solution selection | Unauthorized action; trust erosion; sprint methodology violation (Decider authority is core to GV Sprint) |
| P-022 | NEVER present sprint findings as certain without disclosing evidence limitations; NEVER inflate theme strength without meeting the >= 3/5 user threshold; NEVER omit degraded mode disclosure when operating without Figma or Miro | Governance undermined; quality assessment invalidated |
| P-001 | NEVER present Day 4 findings without citing specific user observations from the interview grid | Unreliable outputs; unfounded claims propagate downstream |
| P-002 | NEVER leave sprint artifacts in transient context only -- persist all four days of output to files | Context rot vulnerability; sprint artifacts lost on session compaction |
| P-004 | NEVER make sprint verdict decisions without documenting the observation evidence and reasoning chain | Untraceable decisions; audit trail broken |
| P-011 | NEVER recommend next steps without supporting evidence from Day 4 testing | Unsupported recommendations; confidence inflated without basis |

**Per-agent enforcement:** The `ux-sprint-facilitator` agent declares:
- `constitution.principles_applied`: P-003, P-020, P-022, P-001, P-002, P-004, P-011 in `skills/ux-design-sprint/agents/ux-sprint-facilitator.governance.yaml`
- `capabilities.forbidden_actions`: 3 entries in NPT-009 format referencing the constitutional triplet
- `disallowedTools: [Agent]` in `skills/ux-design-sprint/agents/ux-sprint-facilitator.md` frontmatter

### AI-Facilitated Sprint Limitations

The Design Sprint facilitator agent operates as an AI-augmented facilitation tool. The following limitations apply to all outputs and MUST be disclosed per P-022 (no deception):

- **Facilitation is not replacement.** The agent structures and guides the sprint process but cannot replace in-person team dynamics, whiteboard collaboration, or real-time ideation energy. Teams should use the agent's structure while conducting actual sprint activities.
- **Sketch descriptions are not sketches.** The agent describes solution concepts in text; it cannot draw. Actual visual sketching must be performed by team members. The agent provides structured prompts and frameworks for the sketching exercises.
- **User interviews require real users.** The agent structures the interview protocol and observation grid but cannot conduct interviews or observe user behavior. The team must recruit and interview 5 representative users.
- **Prototype construction requires human execution.** The agent specifies the prototype and provides construction guidance but the actual building must be done by the team (with or without Figma). The agent can assist with content and flow decisions.
- **The Decider's authority is paramount.** Per Knapp et al. (2016), the Decider has final say on solution direction. The agent facilitates the decision process but never overrides the Decider's choice, even when data suggests a different direction.
- **Day 4 findings depend on interview quality.** The observation grid analysis is only as good as the observations recorded during interviews. Incomplete or biased observation recording degrades finding quality.

---

## Registration

This sub-skill follows a parent-routed registration model per H-26. Sub-skills are routed through the parent `/user-experience` orchestrator; independent registration would create duplicate triggers (AP-02).

| Registration Point | Status | Detail |
|--------------------|--------|--------|
| `CLAUDE.md` skill table | Registered via parent | `/user-experience` registered; sub-skills not independently listed |
| `mandatory-skill-usage.md` trigger map | Routed via parent | "design sprint" keyword routes to parent, which dispatches here |
| `AGENTS.md` agent registry | Registered | `ux-sprint-facilitator` listed under User-Experience Skill Agents |
| Parent SKILL.md agent table | Registered | Listed in `skills/user-experience/SKILL.md` [Available Agents] |

---

## Deployment Status

> **Wave 5 Sub-Skill -- Phase 1 Complete, Phase 2 Pending.**
>
> This sub-skill follows a two-phase implementation sequence:
>
> - **Wave 5 Phase 1 (this deliverable):** SKILL.md specification -- methodology, output format, routing integration, template stub, cross-framework integration, and quality gate criteria. This document is the Phase 1 artifact.
> - **Wave 5 Phase 2 (pending):** Agent implementation -- `skills/ux-design-sprint/agents/ux-sprint-facilitator.md` (agent definition with `<input>`, `<capabilities>`, `<methodology>`, `<output>` sections) and `skills/ux-design-sprint/agents/ux-sprint-facilitator.governance.yaml` (governance metadata). Tracked under PROJ-022 EPIC-005.

---

## Quick Reference

### Common Workflows

| Need | Command Example |
|------|-----------------|
| New product exploration | "We don't know what to build -- help us figure it out" |
| Validate redesign concept | "Run a design sprint for the checkout redesign" |
| Test with real users | "We need to validate our mobile navigation with 5 users" |
| Full 4-day sprint | "Facilitate a Design Sprint 2.0 for the dashboard feature" |
| Post-JTBD solution exploration | "We have our JTBD job statements -- now run a sprint to explore solutions" |
| Competing ideas resolution | "Our team has 3 ideas for the settings page -- which one works?" |

### Agent Selection Hints

| Keywords | Routes To |
|----------|-----------|
| design sprint, GV sprint, rapid prototyping, sprint week, map sketch decide test, 4-day sprint, design sprint 2.0, validate prototype, sprint facilitation | `ux-sprint-facilitator` |
| heuristic, usability, Nielsen, severity, inspection, evaluation | `/ux-heuristic-eval` (not this sub-skill) |
| JTBD, jobs to be done, switch interview, user motivation, job statement | `/ux-jtbd` (not this sub-skill) |
| lean UX, hypothesis, assumption, experiment, build-measure-learn | `/ux-lean-ux` (not this sub-skill) |
| HEART, metrics, measurement, GSM, happiness, engagement | `/ux-heart-metrics` (not this sub-skill) |
| behavior design, B=MAP, Fogg model, behavior bottleneck | `/ux-behavior-design` (not this sub-skill) |
| Kano, feature prioritization, must-be, attractive, performance | `/ux-kano-model` (not this sub-skill) |

---

## References

| Source | Content | Path |
|--------|---------|------|
| Parent SKILL.md | Sub-skill scope, wave architecture, routing, MCP dependencies, synthesis protocol | `skills/user-experience/SKILL.md` |
| Agent definition | Agent frontmatter, identity, expertise, guardrails | `skills/ux-design-sprint/agents/ux-sprint-facilitator.md` [PLANNED] |
| Agent governance | Tool tier, forbidden actions, output validation, constitutional compliance | `skills/ux-design-sprint/agents/ux-sprint-facilitator.governance.yaml` [PLANNED] |
| UX routing rules | Lifecycle-stage routing, handoff data contracts, common intent resolution | `skills/user-experience/rules/ux-routing-rules.md` |
| Synthesis validation | Confidence gate protocol, per-sub-skill confidence map, signal extraction criteria | `skills/user-experience/rules/synthesis-validation.md` |
| Wave progression | Wave 5 entry criteria, signoff requirements | `skills/user-experience/rules/wave-progression.md` |
| CI checks | P-003 enforcement, sub-skill validation gates | `skills/user-experience/rules/ci-checks.md` |
| Design sprint template | Four-day sprint artifact structure, observation grid, storyboard format | `skills/ux-design-sprint/templates/design-sprint-template.md` |
| Skill standards | H-25/H-26 skill structure requirements | `.context/rules/skill-standards.md` |
| Agent development standards | H-34 dual-file architecture, tool tiers, handoff protocol | `.context/rules/agent-development-standards.md` |
| Quality enforcement | Quality gate thresholds, criticality levels, strategy catalog | `.context/rules/quality-enforcement.md` |
| Handoff schema | Canonical handoff schema v2 | `docs/schemas/handoff-v2.schema.json` |
| Agent governance schema | Governance YAML validation schema | `docs/schemas/agent-governance-v1.schema.json` |

### Requirements Traceability

| Source | Content | Path |
|--------|---------|------|
| PROJ-022 PLAN.md | Project plan: sub-skill scope, wave assignment, acceptance criteria, implementation phases | `projects/PROJ-022-user-experience-skill/PLAN.md` |
| EPIC-005 (Wave 5 Deployment) | Parent work item for Wave 5 sub-skill implementation including this sub-skill | PROJ-022 EPIC-005 in `projects/PROJ-022-user-experience-skill/WORKTRACKER.md` |
| ORCHESTRATION.yaml | Orchestration plan governing the build sequence for this sub-skill | `projects/PROJ-022-user-experience-skill/orchestration/ux-skill-build-20260303-001/ORCHESTRATION.yaml` |

### External References

| Source | Citation |
|--------|----------|
| Knapp, J., Zeratsky, J., & Kowitz, B. (2016) | "Sprint: How to Solve Big Problems and Test New Ideas in Just Five Days." Simon & Schuster. Chapter 1: sprint overview and Decider role; Chapters 2-6: Day 1 Map methodology (long-term goal, sprint questions, user journey map, HMW interviews, target selection); Chapter 7: Day 2 lightning demos; Chapter 8: four-step sketch (Notes, Ideas, Crazy 8s, Solution Sketch); Chapter 9: Art Museum voting; Chapters 10-11: Day 3 straw poll, supervote, storyboard; Chapters 12-13: Day 4 prototype construction ("Goldilocks quality"); Chapter 14: 5-user interview protocol and pattern analysis. |
| Courtney, J. (2019) | "The Design Sprint 2.0." AJ&Smart. Compressed four-day format: Day 1 combines GV Days 1-2 (Map + Sketch begin), Day 2 completes sketching, Day 3 combines GV Days 3-4 (Decide + Storyboard), Day 4 is GV Day 5 (Test). Adopted here as the primary sprint format for time efficiency. |
| Nielsen, J. (2000) | "Why You Only Need to Test with 5 Users." Nielsen Norman Group. [https://www.nngroup.com/articles/why-you-only-need-to-test-with-5-users/](https://www.nngroup.com/articles/why-you-only-need-to-test-with-5-users/) (accessed 2026-03-04). Validates 5-user interview sample size for Day 4 testing: 5 users uncover approximately 85% of usability problems. |
| Brown, T. (2009) | "Change by Design: How Design Thinking Transforms Organizations and Inspires Innovation." Harper Business. Origin of the "How Might We" (HMW) technique adopted by IDEO and subsequently incorporated into the Google Ventures Sprint methodology (Knapp et al., 2016, Chapter 4). |

---

*Sub-Skill Version: 1.1.0*
*Parent Skill: `/user-experience` v1.0.0*
*Constitutional Compliance: Jerry Constitution v1.0*
*Wave: 5 (Process Intensives)*
*SSOT: `skills/user-experience/SKILL.md`*
*Project: PROJ-022 User Experience Skill*
*Created: 2026-03-04*
