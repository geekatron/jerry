---
name: ux-kano-model
description: "Kano model feature classification and prioritization sub-skill for the /user-experience parent skill. Classifies product features into Must-be (M), Performance (O), Attractive (A), Indifferent (I), and Reverse (R) categories using the functional/dysfunctional questionnaire pair methodology (Kano et al., 1984). Computes Customer Satisfaction (CS) coefficients (Better/Worse) for priority matrix visualization. Produces feature classification reports, priority matrices, and survey design templates. Sample size awareness: 5-8 respondents yields directional classification only (MEDIUM confidence); 20+ respondents required for statistical classification (Berger et al., 1993). Invoked by ux-orchestrator during Wave 4 lifecycle-stage routing or when user intent is \"Need to prioritize features\" at any lifecycle stage. Triggers: Kano, must-be, attractive, one-dimensional, performance feature, satisfaction, feature classification, delighter, feature prioritization, CS coefficient."
version: "1.2.0"
model: sonnet
agents:
  - ux-kano-analyst
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
activation-keywords:
  - "Kano"
  - "Kano model"
  - "must-be"
  - "attractive quality"
  - "one-dimensional"
  - "performance feature"
  - "feature classification"
  - "feature prioritization"
  - "delighter"
  - "CS coefficient"
  - "satisfaction coefficient"
  - "functional dysfunctional"
---

<!-- VERSION: 1.2.0 | DATE: 2026-03-04 | SOURCE: skills/user-experience/SKILL.md | PARENT: /user-experience skill | REVISION: iter4 quality gate revision -- add framework-inference qualifier to bypass rationale (Evidence Quality 0.91->target), add Phase 5 inline template fallback for symmetric treatment with Phase 2 (Actionability 0.93->target), use consistent [PLANNED: Wave 4 Phase 2] token in Quality Gate Integration prose (Traceability 0.95->target) -->

# Kano Model Sub-Skill

> **Version:** 1.2.0
> **Framework:** Jerry User-Experience -- Kano Model
> **Constitutional Compliance:** Jerry Constitution v1.0
> **Parent Skill:** `/user-experience` (`skills/user-experience/SKILL.md`)
> **Wave:** 4 (Advanced Analytics)
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
| [Methodology](#methodology) | Kano Model categories, evaluation table, CS coefficients, sample size considerations |
| [Execution Procedure](#execution-procedure) | 5-phase workflow from scope definition through synthesis |
| [Output Specification](#output-specification) | Output location, L0/L1/L2 structure, required sections |
| [Routing](#routing) | Keywords and lifecycle-stage routing integration |
| [Cross-Framework Integration](#cross-framework-integration) | Upstream inputs and downstream handoffs |
| [Synthesis Hypothesis Confidence](#synthesis-hypothesis-confidence) | Confidence classifications with rationale |
| [Quality Gate Integration](#quality-gate-integration) | H-13/H-14 compliance for C2+ deliverables |
| [Degraded Mode Behavior](#degraded-mode-behavior) | Operation with insufficient respondents or without survey data |
| [Wave Architecture](#wave-architecture) | Wave 4 entry criteria and bypass conditions |
| [Constitutional Compliance](#constitutional-compliance) | Governing principles |
| [Registration](#registration) | Parent-routed registration model |
| [Deployment Status](#deployment-status) | Current implementation status |
| [Quick Reference](#quick-reference) | Common workflows and agent selection hints |
| [References](#references) | Full repo-relative paths to all referenced files |

## Document Audience (Triple-Lens)

This SKILL.md serves multiple audiences:

| Level | Audience | Sections to Focus On |
|-------|----------|---------------------|
| **L0 (Stakeholder)** | Product managers, feature owners | [Purpose](#purpose), [When to Use This Sub-Skill](#when-to-use-this-sub-skill), [Quick Reference](#quick-reference) |
| **L1 (Developer)** | Engineers invoking the agent | [Invoking the Agent](#invoking-the-agent), [Execution Procedure](#execution-procedure), [Output Specification](#output-specification) |
| **L2 (Architect)** | Workflow designers, skill maintainers | [Methodology](#methodology), [Cross-Framework Integration](#cross-framework-integration), [Synthesis Hypothesis Confidence](#synthesis-hypothesis-confidence) |

---

## Purpose

The Kano Model sub-skill provides AI-augmented feature classification and prioritization using the Kano Model methodology (Kano et al., 1984). It assists tiny teams (1-5 people) in understanding which features satisfy, delight, or frustrate users by classifying features into five categories based on the functional/dysfunctional questionnaire pair.

The agent operates on user-provided survey data or assists with survey design when no data exists. It does NOT conduct surveys itself -- it designs questionnaires, analyzes response data, and produces classification reports with Customer Satisfaction (CS) coefficients for priority decision-making.

### Key Capabilities

- **Survey Design** -- Generates functional/dysfunctional question pairs ready for team administration
- **Response Classification** -- Maps answer pairs to Kano categories using the 5x5 evaluation table (Kano et al., 1984)
- **CS Coefficient Calculation** -- Computes Better/Worse coefficients per feature (Berger et al., 1993)
- **Priority Matrix** -- Better vs. Worse scatter plot for feature prioritization
- **Feature Lifecycle Analysis** -- Attractive-to-Performance-to-Must-be migration patterns
- **Conflict Detection** -- Identifies split classifications and flags for domain expert resolution
- **Sample Size Awareness** -- Calibrates confidence by respondent count (5-8 = directional; 20+ = statistical)

---

## When to Use This Sub-Skill

Activate when:

- Prioritizing a backlog of potential features by user satisfaction impact
- Deciding which features are "table stakes" (Must-be) versus differentiators (Attractive)
- Designing a Kano survey questionnaire for team administration
- Analyzing existing Kano survey response data
- Determining which features to invest in, maintain, or deprioritize
- Understanding how feature expectations shift as a product matures (lifecycle dynamics)
- Resolving disagreements about feature priority with a structured, evidence-based framework
- Receiving a job-derived feature list from `/ux-jtbd` that needs prioritization

Do NOT use for:

- General usability evaluation of existing interfaces (use `/ux-heuristic-eval`)
- Diagnosing why users fail to take a desired action (use `/ux-behavior-design`)
- Measuring ongoing UX health metrics (use `/ux-heart-metrics`)
- Accessibility compliance auditing (use `/ux-inclusive-design`)
- Building component libraries (use `/ux-atomic-design`)
- User motivation research without a defined feature list (use `/ux-jtbd`)
- Running rapid prototyping sprints (use `/ux-design-sprint`)
- General research without UX focus (use `/problem-solving`)

---

## Available Agents

| Agent | Role | Tier | Mode | Model | Wave | Output Location |
|-------|------|------|------|-------|------|-----------------|
| `ux-kano-analyst` | Kano model feature classification and prioritization | T2 | Convergent | Sonnet | 4 | `skills/ux-kano-model/output/{engagement-id}/ux-kano-analyst-{topic-slug}.md` |

**Tool tier:** T2 = Read-Write (Read, Write, Edit, Glob, Grep, Bash). This agent operates on user-provided data only -- it does NOT have WebSearch, WebFetch, or Context7 MCP tools. The T2 assignment follows the principle of least privilege (AR-006): the agent reads feature lists and survey data provided by the user, performs classification analysis, and writes output reports. No external research is required because the Kano methodology is self-contained within the agent's training knowledge.

**Cognitive mode:** Convergent -- narrows from feature list and response data to classified priorities. Each iteration refines rather than expands.

Output at three levels per AD-M-004:
- **L0 (Executive Summary):** Feature classification overview with top priorities for stakeholders and cross-framework synthesis input.
- **L1 (Technical Detail):** Full classification table, CS coefficients, evaluation methodology, conflict analysis, and priority matrix.
- **L2 (Strategic Implications):** Feature lifecycle dynamics, competitive positioning, product maturity trajectory, and roadmap recommendations.

---

## P-003 Compliance

This sub-skill contains a single worker agent (`ux-kano-analyst`) that is invoked by the parent `ux-orchestrator`. The agent MUST NOT include Agent in its tool list per H-01/P-003.

```
MAIN CONTEXT (user request)
    |
    v
ux-orchestrator (T5, Opus, Integrative) -- routes, gates, synthesizes
    |
    +-- ux-kano-analyst (T2, Convergent, Sonnet) [Wave 4] -- THIS SUB-SKILL
```

**Enforcement:** The `ux-kano-analyst` agent declares `disallowedTools: [Agent]` in `.md` frontmatter. The `.governance.yaml` includes Agent prohibition in `capabilities.forbidden_actions` with P-003 consequence statement.

---

## Invoking the Agent

### Via Natural Language Request

Describe your feature prioritization need; the orchestrator routes to this sub-skill:

```
"Classify these backlog features using Kano analysis"
"Which of these features are must-haves versus delighters?"
"Design a Kano survey for our feature candidates"
"Analyze these Kano survey results and prioritize the features"
"Help me decide which features to build first using Kano model"
```

### Via Explicit Agent Request

```
"Use ux-kano-analyst to classify our product backlog features"
"Have ux-kano-analyst analyze the survey results in the attached data"
```

### Via Agent Tool (orchestrator internal)

The `ux-orchestrator` invokes the agent via the Agent tool:

```python
Agent(
    description="ux-kano-analyst: Kano feature classification for dashboard features",
    subagent_type="jerry:ux-kano-analyst",
    prompt="""
## UX CONTEXT (REQUIRED)
- **Engagement ID:** UX-0001
- **Topic:** Dashboard Feature Prioritization
- **Product:** [product name and domain]
- **Target Users:** [user description]
- **Input:** [feature list file path or inline feature list]
- **Survey Data:** [survey response file path, or "none -- design survey"]

## TASK
Perform Kano model feature classification. Classify features using evaluation
table, compute CS coefficients, produce priority matrix, flag split classifications.

## MANDATORY PERSISTENCE (P-002)
Create file at: skills/ux-kano-model/output/UX-0001/ux-kano-analyst-dashboard-features.md
"""
)
```

> **Governance codification (AD-M-007):** The session_context contract (on_receive/on_send) is specified in `ux-kano-analyst.governance.yaml` per AD-M-007. Fields are enumerated below:

**on_receive fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `engagement_id` | string | Yes | UX engagement identifier (format: `UX-{NNNN}`) |
| `product_context` | string | Yes | Product name, domain, and target user description |
| `feature_list` | array | Yes | Features to classify; each entry includes feature name, brief description, and optional category tag |
| `survey_responses` | array | No | Raw survey response data; each entry includes respondent ID and functional/dysfunctional answer pairs per feature. If absent, agent enters survey design mode. |
| `respondent_count` | integer | No | Number of survey respondents. Used for sample size confidence calibration. |
| `upstream_artifacts` | array | No | File paths to upstream handoff artifacts (JTBD job-derived feature list, heuristic eval findings) |

**on_send fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `feature_classifications` | array | Yes | Per-feature: name, category (M/O/A/I/R/Q), response distribution, confidence |
| `cs_coefficients` | array | Yes | Per-feature Better/Worse coefficients |
| `priority_matrix` | object | Yes | Better vs. Worse scatter with quadrant assignments and rankings |
| `split_classifications` | array | Yes | Features with no majority category; distribution breakdown, resolution prompt |
| `survey_design` | object | No | Functional/dysfunctional question pairs (survey design mode only) |
| `lifecycle_analysis` | object | No | Feature lifecycle stage with migration trajectory |
| `synthesis_judgments` | array | Yes | AI judgment calls with confidence (HIGH/MEDIUM/LOW) and rationale |
| `sample_size_disclosure` | object | Yes | Respondent count, statistical adequacy, confidence calibration |

> **Source:** Invocation pattern from parent SKILL.md [Invoking an Agent].

---

## Methodology

### The Kano Model

The Kano Model (Kano, Seraku, Takahashi, & Tsuji, 1984) classifies customer preferences into categories based on the relationship between feature implementation and customer satisfaction. Unlike linear models, the Kano Model recognizes that different feature types have fundamentally different satisfaction curves.

### Feature Categories

| Category | Symbol | Satisfaction Curve | Description | Example |
|----------|--------|-------------------|-------------|---------|
| **Must-be** | M | Absent = high dissatisfaction; present = neutral | Basic requirements taken for granted | Login, data persistence, back button |
| **Performance** | O | Linear: more = more satisfaction | Features with linear satisfaction relationship | Load speed, storage capacity, export formats |
| **Attractive** | A | Absent = neutral; present = delight | Unexpected features that differentiate | Smart autocomplete, AI suggestions |
| **Indifferent** | I | No satisfaction impact either way | Features customers do not care about | Backend database choice, internal refactoring |
| **Reverse** | R | Presence causes dissatisfaction | Features a segment actively does not want | Forced social sharing, auto-playing audio |
| **Questionable** | Q | Contradictory response | Misunderstood question or careless response | Likes both presence AND absence |

### Functional/Dysfunctional Questionnaire Methodology

The Kano Model uses a paired-question approach for each feature (Kano et al., 1984):

1. **Functional question** (positive form): "How would you feel if this product had [feature X]?"
2. **Dysfunctional question** (negative form): "How would you feel if this product did NOT have [feature X]?"

Each question uses a standardized 5-point response scale:

| Response | Code | Meaning |
|----------|------|---------|
| I like it | 1 | Positive reaction to the feature state |
| I expect it | 2 | Considers this a basic expectation |
| I am neutral | 3 | No strong feeling either way |
| I can tolerate it | 4 | Mild negative reaction, but acceptable |
| I dislike it | 5 | Strong negative reaction |

### Kano Evaluation Table (5x5 Grid)

The combination of functional and dysfunctional responses maps to a Kano category using this standard evaluation table (Kano et al., 1984; Berger et al., 1993):

| | **Dysfunctional: Like** | **Dysfunctional: Expect** | **Dysfunctional: Neutral** | **Dysfunctional: Tolerate** | **Dysfunctional: Dislike** |
|---|---|---|---|---|---|
| **Functional: Like** | Q | A | A | A | O |
| **Functional: Expect** | R | I | I | I | M |
| **Functional: Neutral** | R | I | I | I | M |
| **Functional: Tolerate** | R | I | I | I | M |
| **Functional: Dislike** | R | R | R | R | Q |

**Reading the table:** Find the respondent's functional answer (row) and dysfunctional answer (column). The intersection cell gives the Kano category for that respondent-feature pair.

**Example:** A respondent answers "I like it" to the functional question and "I dislike it" to the dysfunctional question. The intersection is **O** (Performance/One-dimensional) -- the respondent values this feature linearly.

### Customer Satisfaction (CS) Coefficient Calculation

CS coefficients quantify each feature's potential to increase satisfaction (Better) or risk dissatisfaction (Worse) (Berger et al., 1993; Matzler & Hinterhuber, 1998):

```
Better = (A + O) / (A + O + M + I)       Range: 0 to 1 (higher = more satisfaction potential)
Worse  = -(O + M) / (A + O + M + I)      Range: -1 to 0 (closer to -1 = more dissatisfaction risk)
```

Where A, O, M, I are the count of respondents classifying the feature in each category. R and Q responses are excluded from CS calculation (Berger et al., 1993).

**Priority Matrix interpretation:**

| Quadrant (Better, Worse) | Feature Type | Strategy |
|--------------------------|-------------|----------|
| High Better, Low Worse (top-left) | Attractive (delighters) | Invest for differentiation; not urgent |
| High Better, High Worse (top-right) | Performance (competitive) | Invest to stay competitive; high priority |
| Low Better, High Worse (bottom-right) | Must-be (basics) | Implement immediately; absence causes dissatisfaction |
| Low Better, Low Worse (bottom-left) | Indifferent | Deprioritize; no satisfaction impact |

> **Axis direction note:** "High Worse" means the absolute value of the Worse coefficient is close to 1.0 (i.e., closer to -1 on the 0-to-(-1) scale), indicating high dissatisfaction risk when the feature is absent. Higher absolute Worse values signal stronger dissatisfaction potential, making those features more urgent to implement.

### Sample Size Considerations

Survey sample size directly affects classification confidence (Berger et al., 1993):

| Respondent Count | Confidence | Classification Quality | Action |
|-----------------|-----------|----------------------|--------|
| 0 | N/A | No classification possible | Survey design mode only |
| 1-4 | Very Low | Individual preferences, not patterns | Disclose as anecdotal |
| 5-8 | MEDIUM | Directional signal; majority may shift | Classify with confidence disclosure; recommend 20+ |
| 9-19 | MEDIUM-HIGH | Increasingly stable | Classify; note statistical threshold not yet met |
| 20+ | HIGH | Statistically reliable (Berger et al., 1993) | Full confidence in classifications and CS coefficients |
| 50+ | Very High | Enables segment analysis (practitioner recommendation; extends Berger et al., 1993 minimum -- no specific academic citation for this threshold) | Full classification plus segment breakdowns |

> **Source:** Berger et al. (1993) recommend a minimum of 20 respondents for reliable Kano classification. The 5-8 respondent range produces directional signals that are useful for early-stage prioritization but MUST be disclosed as MEDIUM confidence per synthesis validation protocol (`skills/user-experience/rules/synthesis-validation.md` [Sub-Skill Synthesis Output Map]).

### Feature Lifecycle Dynamics

Kano categories are not static -- features migrate across categories as products and markets mature (Kano et al., 1984; Matzler & Hinterhuber, 1998):

```
Attractive (A)  --->  Performance (O)  --->  Must-be (M)
  "Delighter"         "Competitive"          "Table stakes"
   (novel)            (expected)              (baseline)
```

Features that once delighted users (Attractive) become expected differentiators (Performance) as competitors adopt them, and eventually become baseline expectations (Must-be). This migration is driven by competitive pressure, customer learning, and market maturation. Features classified as Attractive today may become Must-be within typically 1-3 product cycles (practitioner estimate based on Kano's original lifecycle observation; no single empirical citation establishes a universal timeframe, as migration speed varies by industry and competitive intensity). Teams should continuously re-evaluate classifications, especially for features approaching transition boundaries. The agent documents lifecycle stage assessment for each feature when sufficient product history is available.

---

## Execution Procedure

The agent executes a 5-phase procedure. Phase flow depends on whether survey data is provided.

### Phase 1: Scope Definition

**Goal:** Establish the feature set, respondent context, and engagement parameters.

**Activities:**

1. Receive and validate engagement context (engagement ID, product context, target users)
2. Verify Wave 4 entry criteria (or bypass documentation)
3. Parse the feature list; validate each feature has a name and description
4. Determine survey data availability: if `survey_responses` provided, proceed to Phase 3; otherwise Phase 2
5. If upstream JTBD artifacts available, map job statements to features

**Outputs:** Validated feature list, engagement context, data availability determination.

### Phase 2: Survey Design

**Goal:** Generate a ready-to-administer Kano questionnaire.

**Activities:**

1. For each feature, craft a functional/dysfunctional question pair using user-understandable language (concrete, no developer jargon, balanced tone)
2. Include the standardized 5-point response scale with each question
3. Generate administration guidance: minimum sample size (20+ statistical; 5-8 directional), respondent selection criteria, administration tips (randomize feature order, avoid priming)
4. Produce the survey questionnaire using `skills/ux-kano-model/templates/kano-survey-template.md` (if the template is not yet available -- marked [PLANNED] -- produce the questionnaire using the functional/dysfunctional pair format described in the Methodology section with the standardized 5-point response scale; see Template Fallback note in the Output Specification section)

**Outputs:** Kano survey questionnaire file ready for team administration.

> **Note:** The agent terminates after Phase 2 when no survey data is provided. The team administers the survey independently. A subsequent invocation with survey response data resumes at Phase 3.

### Phase 3: Response Analysis

**Goal:** Classify each respondent-feature pair using the Kano evaluation table.

**Activities:**

1. Parse survey response data (respondent ID, functional/dysfunctional answers per feature)
2. Apply the 5x5 evaluation table to each respondent-feature pair
3. Aggregate per feature: count M/O/A/I/R/Q, determine majority category, calculate percentages
4. Detect split classifications (no single category > 50%) and high Q rates (> 10%)
5. Record `sample_size_disclosure` with respondent count and statistical adequacy

**Outputs:** Per-feature classification table with response distribution and split/Q flags.

### Phase 4: Priority Synthesis

**Goal:** Compute CS coefficients and produce the priority matrix.

**Activities:**

1. Calculate Better and Worse coefficients for each feature (excluding R and Q responses)
2. Construct the priority matrix (Better x-axis, Worse y-axis) and assign quadrant positions
3. Detect priority conflicts: features with similar CS values, majority category vs. CS-derived quadrant mismatches, high R count (> 20%) indicating user segment disagreement
4. Produce priority ranking: Must-be (implement immediately), Performance (high priority), Attractive (medium priority), Indifferent (deprioritize)
5. Document feature lifecycle stage assessment where product history is available
6. Flag priority conflicts for domain expert resolution with `[DOMAIN EXPERT REQUIRED]` markers

**Outputs:** CS coefficient table, priority matrix, priority ranking, conflict report.

### Phase 5: Synthesis and Handoff Preparation

**Goal:** Produce the final output report and prepare handoff data for cross-framework synthesis.

**Activities:**

1. Assemble complete output using `skills/ux-kano-model/templates/feature-priority-template.md` (if the template is not yet available -- marked [PLANNED] -- use the Required Output Sections table in the Output Specification section as the authoritative fallback)
2. Populate L0/L1/L2 sections
3. Compile Synthesis Judgments Summary with confidence classifications
4. Prepare handoff data: `feature_classifications`, `cs_coefficients`, `priority_matrix`, `split_classifications`, `sample_size_disclosure`, `synthesis_judgments`
5. Persist output to designated path per P-002

**Outputs:** Complete Kano analysis report at `skills/ux-kano-model/output/{engagement-id}/ux-kano-analyst-{topic-slug}.md`.

---

## Output Specification

### Output Location

```
skills/ux-kano-model/output/{engagement-id}/ux-kano-analyst-{topic-slug}.md
```

Where:
- `{engagement-id}` follows the pattern `UX-{NNNN}` (e.g., `UX-0001`)
- `{topic-slug}` is a kebab-case descriptor of the feature set evaluated (e.g., `dashboard-features`, `onboarding-backlog`, `mobile-priorities`)

### Required Output Sections

| Section | Level | Content |
|---------|-------|---------|
| **Executive Summary** | L0 | Feature count by Kano category; top 3 Must-be features; top 3 Attractive features; sample size and confidence disclosure; overall prioritization recommendation for stakeholders |
| **Engagement Context** | L1 | Product description, target users, feature list source, survey administration details, respondent count, MCP status |
| **Feature Classification Table** | L1 | Per-feature: name, majority Kano category, response distribution (M/O/A/I/R/Q counts and percentages), classification confidence |
| **CS Coefficient Analysis** | L1 | Per-feature: Better coefficient, Worse coefficient, quadrant assignment; summary statistics |
| **Priority Matrix** | L1 | Text-based scatter plot representation with features plotted by Better (x) vs. Worse (y); quadrant boundaries and labels |
| **Split Classification Analysis** | L1 | Features with no majority category; distribution breakdown; domain expert resolution prompts |
| **Feature Lifecycle Assessment** | L2 | Per-feature lifecycle stage (if product history available); migration trajectory predictions; competitive context |
| **Strategic Implications** | L2 | Product maturity assessment, competitive positioning recommendations, roadmap implications, investment priority rationale |
| **Synthesis Judgments Summary** | L1 | Each AI judgment call listed with confidence classification (HIGH/MEDIUM/LOW) and rationale |
| **Handoff Data** | L1 | Structured data for downstream sub-skills and cross-framework synthesis: feature classifications, CS coefficients, priority matrix, split classifications, sample size disclosure |

**Synthesis Judgments Summary requirements:** This section MUST list every AI-generated judgment (category assignment interpretation, CS coefficient analysis, priority ranking, lifecycle stage assessment, conflict resolution framing) with a confidence classification (HIGH/MEDIUM/LOW) and a one-line rationale. This enables downstream consumers (including the `ux-orchestrator` synthesis gate) to assess which findings are strongly supported versus which require additional validation.

### Templates

Two templates support the agent's output production:

| Template | Path | Purpose |
|----------|------|---------|
| Kano Survey Template | `skills/ux-kano-model/templates/kano-survey-template.md` [PLANNED: Wave 4 Phase 2] | Functional/dysfunctional questionnaire pair template with standardized response scale and administration guidance |
| Feature Priority Template | `skills/ux-kano-model/templates/feature-priority-template.md` [PLANNED: Wave 4 Phase 2] | Feature classification report and priority matrix output template with L0/L1/L2 sections |

> **Template fallback:** Until templates are created during Wave 4 Phase 2 implementation, agents SHOULD use the Required Output Sections table above as the authoritative output specification and produce equivalent content inline.

> **Source:** Output location from [skills/user-experience/SKILL.md -- Available Agents] and ORCHESTRATION.yaml pipeline-wave4 artifacts.

---

## Routing

### Trigger Keywords

| Keyword | Routing Context |
|---------|----------------|
| Kano | Direct match -- primary trigger |
| Kano model | Direct match |
| must-be | In combination with feature/prioritization context |
| attractive quality | Direct match |
| one-dimensional | In combination with feature/quality context |
| performance feature | In combination with Kano/classification context |
| feature classification | Direct match |
| feature prioritization | In combination with Kano/satisfaction context |
| delighter | In combination with feature/UX context |
| CS coefficient | Direct match |
| satisfaction coefficient | Direct match |

### Lifecycle-Stage Routing Integration

This sub-skill is routed to by the `ux-orchestrator` in the following lifecycle-stage scenarios:

| Stage | User Intent | Route Condition |
|-------|-------------|-----------------|
| Before design | "Need to prioritize features" | Direct route to `/ux-kano-model` per [skills/user-experience/SKILL.md -- Lifecycle-Stage Routing] |
| Before design | "Decide what to build" (with known feature list) | Qualification question: "Are you defining the problem or prioritizing features?" If prioritizing: route here. Source: [skills/user-experience/SKILL.md -- Common Intent-to-Route Resolution] |
| Any stage | After `/ux-jtbd` completion | Canonical "Discover to Prioritize" sequence continuation: JTBD job-derived feature list available as upstream handoff artifact |

### Wave Gating

This sub-skill is in **Wave 4** (Advanced Analytics). It requires Wave 3 completion before deployment:

**Entry criteria:** Wave 3: Storybook with 5+ Atom stories AND 1 Persona Spectrum review completed.

**Bypass condition:** Existing user base with analytics (skip Persona Spectrum prerequisite). Note: this bypass condition allows teams with an established product and analytics infrastructure to proceed to Wave 4 without completing the Persona Spectrum review, recognizing that such teams already have user understanding from behavioral data (framework inference based on Wave 4 entry criteria requiring launched product with analytics).

> **Source:** Routing integration from [skills/user-experience/rules/ux-routing-rules.md -- Stage Routing Table] and [skills/user-experience/SKILL.md -- Lifecycle-Stage Routing]. Wave assignment from [skills/user-experience/SKILL.md -- Wave Architecture]. Bypass condition from [skills/user-experience/SKILL.md -- Wave Definitions] (Wave 4 "Bypass Condition" column: "Existing user base with analytics (skip Persona Spectrum prerequisite)") and [skills/user-experience/SKILL.md -- Wave Transition Quality Gates] (bypass documentation requirements: 3-field format).

---

## Cross-Framework Integration

### Upstream Inputs

This sub-skill receives context from other sub-skills when invoked as part of a multi-sub-skill workflow:

| From Sub-Skill | Handoff Artifact | Key Fields | Usage |
|----------------|-----------------|-----------|-------|
| `/ux-jtbd` | Job-derived feature list | Job statements, switch forces (push/pull), outcome expectations, feature candidates | JTBD job statements provide the feature list; switch forces inform expected category (push = Must-be; pull = Attractive). Source: [skills/user-experience/SKILL.md -- Cross-Sub-Skill Handoff Data] |
| `/ux-heuristic-eval` | Severity-rated findings | Finding ID, heuristic violated, severity (0-4), affected screen/flow | Heuristic findings reframed as features for Kano classification; severity provides initial Must-be vs. Performance signal |

### Downstream Handoffs

This sub-skill produces artifacts that feed into cross-framework synthesis via the Jerry handoff protocol (`docs/schemas/handoff-v2.schema.json`).

| To Sub-Skill/Consumer | Handoff Artifact | Key Fields | Trigger |
|-----------------------|-----------------|-----------|---------|
| `ux-orchestrator` (synthesis) | Feature classifications + CS coefficients + priority matrix | `feature_classifications`, `cs_coefficients`, `priority_matrix`, `split_classifications`, `sample_size_disclosure` | After classification; feeds cross-framework synthesis convergence detection |
| `/ux-lean-ux` (cross-sub-skill) | Priority-ranked feature list | Features ranked by CS quadrant; Attractive features as experiment candidates | Attractive features become Lean UX experiment candidates; Must-be features bypass experimentation |
| `/ux-heart-metrics` (cross-sub-skill) | Feature priority baseline | CS coefficients per feature, expected satisfaction impact | CS coefficients provide predicted baseline for post-implementation UX measurement |

**Handoff data format:** Uses handoff-v2 schema (`docs/schemas/handoff-v2.schema.json`) with `ux_ext` extension fields: `feature_count`, `respondent_count`, `statistical_adequacy` ("directional" or "statistical"), `split_count`, `conflict_count`. Default confidence for 5-8 respondent directional classification: 0.65. Criticality: C2.

### Canonical Multi-Skill Workflow Sequences

This sub-skill participates in the following canonical sequences:

| Sequence | Skills Involved | This Sub-Skill's Role |
|----------|----------------|-----------------------|
| Discover to Prioritize | `/ux-jtbd` then **`/ux-kano-model`** | Receives job-derived feature list from JTBD; classifies features by user satisfaction impact to determine build priority |
| Prioritize to Experiment | **`/ux-kano-model`** then `/ux-lean-ux` | Attractive features become Lean UX experiment candidates; Must-be features bypass experimentation (implement directly) |
| Prioritize to Measure | **`/ux-kano-model`** then `/ux-heart-metrics` | CS coefficients provide predicted satisfaction baseline; HEART metrics measure actual post-implementation UX impact |

> **Source:** Handoff data contracts from [skills/user-experience/rules/ux-routing-rules.md -- Handoff Data Contracts] and [skills/user-experience/SKILL.md -- Cross-Sub-Skill Handoff Data] ("/ux-jtbd -> /ux-kano-model: Job-derived feature list"). Canonical sequences from [skills/user-experience/SKILL.md -- Canonical Multi-Skill Workflow Sequences] ("Discover to Prioritize: /ux-jtbd then /ux-kano-model").

---

## Synthesis Hypothesis Confidence

Kano Model outputs include synthesis hypotheses that carry confidence classifications per the synthesis validation protocol (`skills/user-experience/rules/synthesis-validation.md` [Sub-Skill Synthesis Output Map]).

| Synthesis Step | Typical Confidence | Rationale |
|---------------|-------------------|-----------|
| Directional classification (5-8 respondents) | MEDIUM | Small sample provides directional signal only; Kano survey requires >= 20 respondents for statistical classification (Berger et al., 1993), so 5-8 yields MEDIUM. Source: `skills/user-experience/rules/synthesis-validation.md` [Sub-Skill Synthesis Output Map] |
| Feature priority conflict interpretation | LOW | Resolving conflicting priorities requires domain context AI lacks. When multiple features have split classifications or similar CS coefficients, the resolution depends on business strategy, competitive landscape, and user segment knowledge that exceeds training data. Source: `skills/user-experience/rules/synthesis-validation.md` [Sub-Skill Synthesis Output Map] |
| Statistical classification (20+ respondents) | HIGH | Sufficient sample size for reliable Kano classification per Berger et al. (1993) recommendation; CS coefficients are statistically meaningful with 20+ respondents |
| Feature lifecycle stage assessment | MEDIUM | Lifecycle migration (Attractive -> Performance -> Must-be) assessment is based on general product maturity patterns (Kano et al., 1984; Matzler & Hinterhuber, 1998); application to a specific product requires domain knowledge about competitive dynamics and market maturation rate |
| CS coefficient interpretation | MEDIUM | CS coefficient calculation is deterministic (arithmetic formula), but interpretation of "High Better" vs. "Low Better" boundaries and quadrant assignment thresholds involve judgment about the specific product context |

**Gate enforcement:**

- **HIGH (20+ respondents):** Synthesis Judgments Summary with acknowledgment prompt. Classifications advance directly to design decisions.
- **MEDIUM (5-8 respondents, lifecycle, CS interpretation):** "Validation Required" section. Design recommendations withheld until validation against real user data, domain expert review, or expanded survey results.
- **LOW (conflict interpretation):** Design recommendation section structurally omitted. Tagged `[DOMAIN EXPERT REQUIRED]`.

**Confidence upgrade path:** Directional classification (MEDIUM) upgrades to HIGH through: (a) expanding the survey to 20+ respondents, or (b) convergence with a second framework in cross-framework synthesis (per `skills/user-experience/rules/synthesis-validation.md` [Convergence Thresholds]: moderate convergence = 2 frameworks with supporting evidence = HIGH). Example: Kano classifies "search autocomplete" as Attractive AND JTBD independently identifies "quick information retrieval" as a high-pull switch force -- convergent finding receives HIGH confidence.

> **Source:** Confidence classifications from [skills/user-experience/rules/synthesis-validation.md [Sub-Skill Synthesis Output Map]] ("`/ux-kano-model` Directional classification (5-8 respondents) MEDIUM", "`/ux-kano-model` Feature priority conflict interpretation LOW"). Gate enforcement from [skills/user-experience/SKILL.md [Synthesis Hypothesis Validation]]. Convergence upgrade thresholds from [skills/user-experience/rules/synthesis-validation.md [Convergence Thresholds]] ("Moderate convergence: 2 frameworks identify the same UX problem with supporting evidence = HIGH").

---

## Quality Gate Integration

Kano Model deliverables are subject to the Jerry quality gate per H-13 and H-14:

| Aspect | Requirement | Source |
|--------|-------------|--------|
| Quality threshold | >= 0.92 weighted composite score for C2+ deliverables | H-13 (`quality-enforcement.md`) |
| Creator-critic-revision cycle | Minimum 3 iterations for C2+ deliverables | H-14 (`quality-enforcement.md`) |
| Self-review | Required before presenting any deliverable | H-15 (S-010) |
| Scoring dimensions | Completeness (0.20), Internal Consistency (0.20), Methodological Rigor (0.20), Evidence Quality (0.15), Actionability (0.15), Traceability (0.10) | S-014 (`quality-enforcement.md`) |

**Kano-specific quality considerations:** Completeness -- all features classified, none dropped. Internal Consistency -- CS coefficients mathematically consistent with classification table. Methodological Rigor -- canonical 5x5 grid applied (Kano et al., 1984). Evidence Quality -- sample size disclosure mandatory. Actionability -- recommendations per quadrant, domain expert prompts for splits. Traceability -- every classification traces to respondent data.

> **Note:** The `kano-methodology-rules.md` file [PLANNED: Wave 4 Phase 2] will codify the evaluation table rules and CS calculation rules that support methodological compliance scoring when created. Until then, the Methodology section of this SKILL.md serves as the authoritative reference for Kano-specific quality evaluation criteria.

---

## Degraded Mode Behavior

The agent adapts its behavior based on data availability and quality:

### No Survey Data Available

When invoked without `survey_responses`:

- Agent enters **survey design mode** (Phase 2 only)
- Produces functional/dysfunctional questionnaire using `kano-survey-template.md`
- Provides administration guidance with sample size recommendations
- Does NOT produce feature classifications, CS coefficients, or priority matrix
- Output carries a disclosure: "Survey design mode -- no classification data available. Administer the survey and re-invoke with response data for feature classification."

### Fewer Than 5 Respondents

When `respondent_count` < 5: classifications labeled `[ANECDOTAL -- NOT FOR DESIGN DECISIONS]`, CS coefficients labeled "unreliable", priority matrix placed in "Insufficient Data" zone. All synthesis outputs classified as LOW. Recommendation to expand to 5+ (directional) or 20+ (statistical).

### 5-8 Respondents (Directional Mode)

When `respondent_count` is 5-8: full classifications at MEDIUM confidence with caveat "Directional only -- coefficients may shift with additional respondents." Priority matrix produced with widened quadrant boundaries. P-022 disclosure: "Classification based on {N} respondents. Berger et al. (1993) recommend >= 20 for statistical reliability."

### High Questionable (Q) Response Rate

When Q responses exceed 10% for any feature: affected features flagged `[QUESTION CLARITY ISSUE]`, excluded from priority matrix ranking, with rephrasing guidance for the functional/dysfunctional question pair.

### MCP Unavailability

The `ux-kano-analyst` is a T2 agent with no MCP dependencies. All inputs are user-provided data (feature lists and survey responses). No degraded mode for MCP is necessary. The parent MCP dependency matrix confirms Miro ENH as the only MCP connection for `/ux-kano-model`; ENH status means cosmetic limitation only (`skills/user-experience/SKILL.md` [MCP Integration Architecture]).

---

## Wave Architecture

This sub-skill is deployed in **Wave 4 (Advanced Analytics)** of the `/user-experience` skill's criteria-gated wave model.

### Wave 4 Position

| Property | Value |
|----------|-------|
| Wave | 4 -- Advanced Analytics |
| Companion sub-skill | `/ux-behavior-design` (Fogg B=MAP) |
| Entry criteria | Wave 3: Storybook with 5+ Atom stories AND 1 Persona Spectrum review |
| Bypass condition | Existing user base with analytics (skip Persona Spectrum prerequisite) |
| Quality gate | S-014 composite >= 0.85 on Wave 4 deliverables (wave transition readiness -- operational output quality; H-13 >= 0.92 applies separately to governance artifacts; see `skills/user-experience/SKILL.md` [Wave Transition Quality Gates] for derivation) |

### Wave 4 Rationale

1. **Prerequisite knowledge:** Effective feature classification benefits from prior JTBD research (Wave 1) and component understanding (Wave 3)
2. **User base requirement:** Kano surveys require respondents; Wave 4 entry criteria ensure the team has users to survey
3. **Complementary pairing:** Wave 4 pairs Kano analysis (feature-level prioritization) with Behavior Design (action-level diagnosis) -- together answering "which features matter most" and "why users are not completing desired actions"

### Wave Bypass

Teams with an existing user base and analytics data may bypass the Wave 3 Persona Spectrum prerequisite. Bypass requires 3-field documentation: (1) unmet criterion, (2) impact assessment (e.g., "Kano analysis proceeds without inclusive design context"), (3) remediation plan with target date.

> **Source:** Wave architecture from [skills/user-experience/SKILL.md -- Wave Architecture] [Wave Definitions] and [Wave Transition Quality Gates].

---

## Constitutional Compliance

All agents in this sub-skill adhere to the **Jerry Constitution v1.0**:

| Principle | Requirement | Consequence of Violation |
|-----------|-------------|-------------------------|
| P-003 | NEVER spawn recursive subagents -- worker agent, no Agent tool access | Agent hierarchy violation; uncontrolled token consumption |
| P-020 | NEVER override user decisions on feature priority or classification interpretation | Unauthorized action; trust erosion |
| P-022 | NEVER present classification confidence without sample size disclosure; NEVER inflate statistical claims with insufficient respondent data | Governance undermined; false precision in prioritization decisions |
| P-001 | NEVER present Kano classifications without response distribution evidence or CS coefficient derivation | Unreliable outputs; unfounded prioritization claims propagate downstream |
| P-002 | NEVER leave Kano classification results or priority matrices in transient context only -- persist to files | Context rot vulnerability; artifacts lost on session compaction |

**Per-agent enforcement:** The `ux-kano-analyst` agent declares:
- `constitution.principles_applied`: P-003, P-020, P-022, P-001, P-002 in `skills/ux-kano-model/agents/ux-kano-analyst.governance.yaml`
- `capabilities.forbidden_actions`: 3 entries in NPT-009 format referencing the constitutional triplet
- `disallowedTools: [Agent]` in `skills/ux-kano-model/agents/ux-kano-analyst.md` frontmatter

### AI-Augmented Analysis Limitations

The following limitations MUST be disclosed per P-022 (no deception):

- **Survey design is guidance, not validated questionnaire research.** Question wording should be pre-tested with 2-3 respondents before full administration (Kano et al., 1984).
- **Classification is mechanical, interpretation is contextual.** The 5x5 evaluation table is deterministic, but interpreting which Must-be features are truly urgent or which Attractive features are feasible requires domain knowledge the agent lacks.
- **CS coefficients are descriptive, not prescriptive.** They describe satisfaction potential in the survey data but do not account for implementation cost, technical feasibility, or strategic alignment.
- **Feature lifecycle predictions are pattern-based.** The migration trajectory is well-documented (Matzler & Hinterhuber, 1998), but timing depends on competitive dynamics the agent cannot observe.
- **Always validate with domain experts.** Classification reports should be reviewed by product managers with knowledge of competitive context, business strategy, and user segment priorities before roadmap commitments.

---

## Registration

This sub-skill follows a parent-routed registration model. Sub-skills are not independently registered in `CLAUDE.md` or `mandatory-skill-usage.md` because they are routed through the parent `/user-experience` orchestrator (`ux-orchestrator`). This is an explicit exception to the H-26 registration requirement (parent-routed model): parent skills own the CLAUDE.md and mandatory-skill-usage.md registration; sub-skills are discovered and dispatched by the parent orchestrator's internal routing logic.

| Registration Point | Status | Detail |
|--------------------|--------|--------|
| `CLAUDE.md` skill table | Registered via parent | `/user-experience` is registered in `CLAUDE.md`; sub-skills are not independently listed |
| `mandatory-skill-usage.md` trigger map | Routed via parent | The `/user-experience` trigger map row includes "Kano model" and "feature prioritization" as positive keywords (H-22); requests matching these keywords route to the parent skill, which dispatches to this sub-skill |
| `AGENTS.md` agent registry | Registered | `ux-kano-analyst` is listed in `AGENTS.md` under the User-Experience Skill Agents section |
| Parent SKILL.md agent table | Registered | `ux-kano-analyst` is listed in `skills/user-experience/SKILL.md` [Available Agents] |

> **H-26 parent-routed model rationale:** Independent registration of sub-skills would create duplicate trigger map entries and ambiguous routing (AP-02 Bag of Triggers). The parent orchestrator owns lifecycle-stage routing logic and dispatches to the correct sub-skill based on triage qualification, not keyword matching alone. Sub-skill agents are registered in `AGENTS.md` for discoverability but routing flows through the parent.

---

## Deployment Status

> **Wave 4 Sub-Skill -- Planned.** This sub-skill is part of Wave 4 (Advanced Analytics) of PROJ-022. The companion agent file (`skills/ux-kano-model/agents/ux-kano-analyst.md`) and governance file (`skills/ux-kano-model/agents/ux-kano-analyst.governance.yaml`) are planned for creation during Wave 4 implementation of PROJ-022 EPIC-005. The SKILL.md itself is complete and specifies the methodology, output format, and routing integration that the agent will implement.

---

## Quick Reference

### Common Workflows

| Need | Command Example |
|------|-----------------|
| Feature prioritization | "Classify these backlog features using Kano analysis" |
| Survey design | "Design a Kano survey for our dashboard feature candidates" |
| Survey analysis | "Analyze these Kano survey results and produce a priority matrix" |
| JTBD-to-Kano pipeline | "We completed JTBD analysis -- now prioritize the job-derived features with Kano" |
| Competitive feature assessment | "Which of our features are must-haves versus delighters compared to competitors?" |
| Feature lifecycle review | "Assess which Attractive features are becoming expected Performance features" |
| Split resolution guidance | "Help interpret these split Kano classifications" |
| Priority conflict analysis | "Several features have similar CS coefficients -- help us differentiate priority" |

### Agent Selection Hints

| Keywords | Routes To |
|----------|-----------|
| Kano, must-be, attractive, one-dimensional, satisfaction, feature classification, delighter, CS coefficient, functional dysfunctional | `ux-kano-analyst` |
| heuristic, usability, Nielsen, severity, inspection | `/ux-heuristic-eval` (not this sub-skill) |
| JTBD, jobs to be done, switch interview, outcome, motivation | `/ux-jtbd` (not this sub-skill) |
| behavior, Fogg, B=MAP, motivation, ability, prompt, nudge | `/ux-behavior-design` (not this sub-skill) |
| HEART, metrics, measurement, GSM, happiness, engagement | `/ux-heart-metrics` (not this sub-skill) |
| lean UX, hypothesis, experiment, build-measure-learn | `/ux-lean-ux` (not this sub-skill) |
| accessibility, WCAG, ARIA, inclusive design | `/ux-inclusive-design` (not this sub-skill) |

---

## References

| Source | Content | Path |
|--------|---------|------|
| Parent SKILL.md | Sub-skill scope, wave architecture, routing, MCP dependencies, synthesis protocol | `skills/user-experience/SKILL.md` |
| Agent definition | Agent frontmatter, identity, expertise, guardrails | `skills/ux-kano-model/agents/ux-kano-analyst.md` [PLANNED: Wave 4] |
| Agent governance | Tool tier, forbidden actions, output validation, constitutional compliance | `skills/ux-kano-model/agents/ux-kano-analyst.governance.yaml` [PLANNED: Wave 4] |
| UX routing rules | Lifecycle-stage routing, handoff data contracts, common intent resolution | `skills/user-experience/rules/ux-routing-rules.md` |
| MCP coordination | MCP dependency matrix, degraded mode behavior | `skills/user-experience/rules/mcp-coordination.md` |
| Synthesis validation | Confidence gate protocol, per-sub-skill confidence map | `skills/user-experience/rules/synthesis-validation.md` |
| Wave progression | Wave 4 entry criteria, signoff requirements | `skills/user-experience/rules/wave-progression.md` |
| CI checks | P-003 enforcement, sub-skill validation gates | `skills/user-experience/rules/ci-checks.md` [STUB: EPIC-001] |
| Kano methodology rules | Evaluation table rules, CS calculation rules | `skills/ux-kano-model/rules/kano-methodology-rules.md` [PLANNED: Wave 4 Phase 2] |
| Kano survey template | Functional/dysfunctional questionnaire pair template | `skills/ux-kano-model/templates/kano-survey-template.md` [PLANNED: Wave 4 Phase 2] |
| Feature priority template | Feature classification and priority matrix output template | `skills/ux-kano-model/templates/feature-priority-template.md` [PLANNED: Wave 4 Phase 2] |
| Skill standards | H-25/H-26 skill structure requirements | `.context/rules/skill-standards.md` |
| Agent development standards | H-34 dual-file architecture, tool tiers, handoff protocol | `.context/rules/agent-development-standards.md` |
| Quality enforcement | Quality gate thresholds, criticality levels, strategy catalog | `.context/rules/quality-enforcement.md` |
| Handoff schema | Canonical handoff schema v2 | `docs/schemas/handoff-v2.schema.json` |
| Agent governance schema | Governance YAML validation schema | `docs/schemas/agent-governance-v1.schema.json` |

### Requirements Traceability

| Source | Content | Path |
|--------|---------|------|
| PROJ-022 PLAN.md | Project plan: sub-skill scope, wave assignment, acceptance criteria, implementation phases | `projects/PROJ-022-user-experience-skill/PLAN.md` |
| EPIC-005 (Wave 4 Deployment) | Parent work item for Wave 4 sub-skill implementation including this sub-skill | PROJ-022 EPIC-005 in `projects/PROJ-022-user-experience-skill/WORKTRACKER.md` |
| ORCHESTRATION.yaml | Orchestration plan governing the build sequence for this sub-skill | `projects/PROJ-022-user-experience-skill/orchestration/ux-skill-build-20260303-001/ORCHESTRATION.yaml` |

### External References

| Source | Citation |
|--------|----------|
| Kano et al., 1984 | Kano, N., Seraku, N., Takahashi, F., & Tsuji, S. (1984). "Attractive Quality and Must-Be Quality." *Journal of the Japanese Society for Quality Control*, 14(2), 39-48. |
| Berger et al., 1993 | Berger, C., Blauth, R., Boger, D., et al. (1993). "Kano's Methods for Understanding Customer-Defined Quality." *Center for Quality Management Journal*, 2(4), 3-36. Recommends >= 20 respondents for statistical Kano classification. |
| Matzler & Hinterhuber, 1998 | Matzler, K., & Hinterhuber, H. H. (1998). "How to make product development projects more successful by integrating Kano's model of customer satisfaction into quality function deployment." *Technovation*, 18(1), 25-38. |

---

*Sub-Skill Version: 1.2.0*
*Parent Skill: `/user-experience` v1.0.0*
*Constitutional Compliance: Jerry Constitution v1.0*
*Wave: 4 (Advanced Analytics)*
*SSOT: `skills/user-experience/SKILL.md`*
*Project: PROJ-022 User Experience Skill*
*Created: 2026-03-04*
