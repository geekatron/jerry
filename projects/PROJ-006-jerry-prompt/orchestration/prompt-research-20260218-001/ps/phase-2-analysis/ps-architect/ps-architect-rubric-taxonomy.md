# Jerry Prompt Quality Rubric and Classification Taxonomy

> **Document ID:** PROJ-006-ARCH-001
> **Agent:** ps-architect (problem-solving skill)
> **Version:** 1.0.0
> **Date:** 2026-02-18
> **Status:** COMPLETE
> **Phase:** 2 — Analysis
> **Carry-Forward Notes:** Cognitive mode effectiveness (P-03/convergent-divergent declaration) treated as hypothesis; ReAct benchmarks (2022-era) qualified for frontier model applicability.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Quick-Reference Rubric Card](#l0-quick-reference-rubric-card) | One-screen scoring summary for immediate use |
| [L1: Full Rubric with Scoring Guidance](#l1-full-rubric-with-scoring-guidance) | All 7 criteria with measurement methods, weights, and scored examples |
| [L1: Prompt Classification Taxonomy](#l1-prompt-classification-taxonomy) | 6 Jerry prompt types with decision guide |
| [L1: Effectiveness Tier Definitions](#l1-effectiveness-tier-definitions) | 4-tier system with observable characteristics |
| [L1: Jerry-Specific Rubric Extensions](#l1-jerry-specific-rubric-extensions) | 4 criteria unique to Jerry vs. general prompt engineering |
| [L2: Design Rationale and Evidence Mapping](#l2-design-rationale-and-evidence-mapping) | Traceability from criteria to Phase 1 findings |

---

## L0: Quick-Reference Rubric Card

> Apply this card to score any Jerry prompt in under 5 minutes.
> Full scoring guidance in L1 section below.

### Scoring Summary (7 Criteria)

| # | Criterion | Weight | Quick Test | Max Points |
|---|-----------|--------|------------|------------|
| C1 | Task Specificity | 20% | Count undefined terms and missing constraints | 20 |
| C2 | Skill Routing | 18% | Are correct Jerry skills named with `/skill` syntax? | 18 |
| C3 | Context Provision | 15% | Is necessary context present without redundant padding? | 15 |
| C4 | Quality Specification | 15% | Is at least one numeric or binary quality threshold present? | 15 |
| C5 | Decomposition | 12% | Are multi-step tasks broken into named phases or steps? | 12 |
| C6 | Output Specification | 12% | Is the output format (type, location, structure) explicit? | 12 |
| C7 | Positive Framing | 8% | Does the prompt state what to do rather than what to avoid? | 8 |
| **Total** | | **100%** | | **100** |

### Tier Lookup

| Raw Score | Normalized (0-1) | Tier | Label |
|-----------|------------------|------|-------|
| 90-100 | 0.90-1.00 | 4 | Exemplary |
| 75-89 | 0.75-0.89 | 3 | Proficient |
| 50-74 | 0.50-0.74 | 2 | Developing |
| 0-49 | 0.00-0.49 | 1 | Inadequate |

### Prompt Type Lookup

| Dominant Characteristic | Prompt Type |
|------------------------|-------------|
| Single agent, factual lookup | Atomic Query |
| Single skill, one deliverable | Implementation Task |
| Multiple skills, one workflow | Multi-Skill Orchestration |
| Open exploration with no fixed output | Research Spike |
| Binary pass/fail, existing artifact | Validation Gate |
| Structured comparison of options | Decision Analysis |

---

## L1: Full Rubric with Scoring Guidance

### Rubric Overview

The rubric contains **7 criteria** derived from evidence in Phase 1 (External Survey, Jerry Internals Investigation). Each criterion has:
- A measurable scoring method (count, presence/absence, or percentage — never subjective judgment)
- A weight expressing relative importance in a Jerry context
- Four score levels (0, 1, 2, 3) with concrete examples drawn from the Salesforce privilege control prompt (the effective example analyzed in jerry-internals-investigation.md, User Prompt Analysis section)

Weighted score formula:
```
final_score = sum(criterion_raw_score / 3 * criterion_weight)
normalized_score = final_score / 100
```

---

### C1 — Task Specificity (Weight: 20%)

**Definition:** The degree to which the prompt eliminates ambiguity about what Claude must produce. Measured by counting undefined terms, missing constraints, and incomplete sentences.

**Measurement method:** Count the number of "specificity gaps" — defined as any of:
- A vague descriptor without a concrete referent (e.g., "good," "appropriate," "relevant")
- A sentence fragment or trailing clause that names no object (e.g., "focus on the patterns of the")
- A constraint range without a unit (e.g., "keep it short")
- A task verb with no object (e.g., "analyze things")

**Scoring:**

| Score | Label | Specificity Gaps | Example |
|-------|-------|-----------------|---------|
| 3 | Full | 0 gaps | "Create a work item of type Spike titled 'Privilege Control Sales Trends Q1-2026' using `/worktracker`. Scope: Salesforce opportunity data from 2024-01-01 to 2026-02-18." |
| 2 | Partial | 1-2 gaps | "Use `/worktracker` to create a spike about Privilege Control sales trends. Use the Salesforce MCP for data." (lacks time scope and work item title) |
| 1 | Vague | 3-4 gaps | "Create a spike about privilege control. Analyze opportunities and patterns." (no skill syntax, no data source, no scope, no output) |
| 0 | Absent | 5+ gaps or no actionable task stated | "Tell me about privilege control." |

**Weight justification:** Highest weight because the Anthropic "golden rule" (Survey §1.2) and the Jerry internals analysis (User Prompt Analysis: "incomplete sentence leaves scope undefined") both identify specificity gaps as the primary failure mode.

---

### C2 — Skill Routing (Weight: 18%)

**Definition:** Whether the prompt invokes the correct Jerry skills using explicit `/skill` syntax and names the appropriate agents when multi-agent workflows are intended.

**Measurement method (two components):**
1. **Skill presence** (binary per skill needed): Is each required skill named with the `/skill` prefix?
2. **Agent specificity** (binary per agent needed): When a specific agent is needed, is its exact name used (e.g., `orch-planner`, `ps-critic`)?

Score = (skills correctly invoked / total skills needed) * 3, rounded to nearest integer.
If no skill invocation is needed for the task type, score defaults to 3.

**Scoring:**

| Score | Label | Skill Routing | Example |
|-------|-------|--------------|---------|
| 3 | Full | All needed skills explicitly invoked with `/skill` syntax; agent names used where relevant | "Use `/orchestration` skill and `orch-planner` to..." (from Salesforce prompt — correct) |
| 2 | Partial | At least one skill correctly invoked; one needed skill omitted or invoked by description only | "Use orchestration to plan..." (missing `/` prefix, orch-planner not named) |
| 1 | Implied | No `/skill` syntax; relies on Claude to infer which skills to use from task description | "Research privilege control sales and orchestrate agents for adversarial review." |
| 0 | None | No skill routing signals; Claude must guess the workflow pattern | "Tell me about privilege control in our Salesforce data." |

**Weight justification:** Skill routing is Jerry-unique (not a general prompt engineering concern). The jerry-internals-investigation.md (Finding 1, P-01) demonstrates that YAML `activation-keywords` and explicit `/skill` invocation are the primary mechanisms by which the correct skill context is loaded.

---

### C3 — Context Provision (Weight: 15%)

**Definition:** Whether the prompt supplies necessary background information without wasteful repetition or over-specification. Measured as the ratio of relevant context elements to total context elements.

**Measurement method:** Identify every context element (data source, time range, audience, workflow position, prior decisions). Classify each as:
- **Relevant**: Would change Claude's behavior if absent
- **Redundant**: Already known from session/CLAUDE.md/skill spec
- **Absent**: Should be present but is not

Score = 3 if (absent_count == 0 AND redundant_ratio < 0.2)
Score = 2 if (absent_count <= 1 OR redundant_ratio 0.2-0.4)
Score = 1 if (absent_count 2-3 OR redundant_ratio 0.4-0.6)
Score = 0 if (absent_count >= 4 OR redundant_ratio > 0.6)

**Scoring:**

| Score | Label | Context Quality | Example |
|-------|-------|----------------|---------|
| 3 | Precise | All necessary context present; no padding | "Data must be gathered using the Salesforce MCP that's already configured against Claude." (cites tool and its state — efficient) |
| 2 | Adequate | Minor gap or minor redundancy; does not block task | "Use Salesforce to get data. Salesforce is a CRM tool that manages customer relationships." (second sentence is redundant) |
| 1 | Thin | Key context missing OR over 40% of context is redundant | "Analyze sales data." (no data source, no scope, no time range) |
| 0 | Absent/Bloated | No useful context, or context so padded it obscures the task | All prose explaining what CRM is without naming the actual data source or access method |

**Weight justification:** Survey §1.2 identifies task purpose, audience, workflow position, and success criteria as the four context dimensions that improve performance. Jerry internals (Layer 5: CLAUDE.md) already handles persistent context; user prompts need only supply what that layer does not provide.

---

### C4 — Quality Specification (Weight: 15%)

**Definition:** Whether the prompt explicitly states the quality threshold or acceptance criteria that will determine task completion.

**Measurement method (presence/absence scoring):**
Count the number of quality signals present:
- **Numeric threshold** (e.g., `>= 0.92`, `> 90%`): 2 points
- **Named rubric or checklist** (e.g., "use ps-critic adversarial review"): 2 points
- **Verbal quality descriptor with concrete referent** (e.g., "peer-reviewable," if "peer-reviewable" is defined elsewhere): 1 point
- **No quality signal at all**: 0 points

Total quality signal points: 4 max. Map to score:
- 4: score 3
- 2-3: score 2
- 1: score 1
- 0: score 0

**Scoring:**

| Score | Label | Quality Signal | Example |
|-------|-------|---------------|---------|
| 3 | Quantified | Numeric threshold AND named review mechanism | "adversarial critics at every phase where the quality factor must be >= 0.92" (from Salesforce prompt) |
| 2 | Named | Named review mechanism only, or named rubric without numeric threshold | "Have ps-critic review each phase output before proceeding." |
| 1 | Verbal | Verbal descriptor without numeric threshold or named mechanism | "Ensure the analysis is thorough and accurate." |
| 0 | Absent | No quality signal | No mention of review, accuracy, thresholds, or acceptance criteria |

**Weight justification:** Survey §6.1 establishes that "a clear definition of success criteria" is prerequisite to meaningful prompt engineering. Jerry internals (Finding 7, P-07) shows the ps-critic circuit breaker operates on a numeric `quality_score`; without a numeric threshold in the user prompt, the circuit breaker defaults to 0.85 (generic), not the user's actual bar.

---

### C5 — Decomposition (Weight: 12%)

**Definition:** Whether complex multi-step tasks are explicitly broken into named phases, ordered steps, or agent pipelines rather than stated as a monolithic goal.

**Measurement method:**
For prompts with more than one distinct deliverable or workflow phase:
- Count explicitly named phases or steps (e.g., "Phase 1: Research, Phase 2: Analysis")
- Count explicitly named agent sequences (e.g., "ps-researcher → ps-analyst → ps-architect")
- Count explicit sync barriers or gates (e.g., "only proceed to orchestration after the spike is created")

Score = 3 if 2+ decomposition elements present
Score = 2 if exactly 1 decomposition element present
Score = 1 if decomposition is implied but not explicit (e.g., "research and then analyze")
Score = 0 if task is monolithic with no decomposition signal

For single-deliverable prompts (Atomic Query type), this criterion scores 3 automatically (no decomposition required).

**Scoring:**

| Score | Label | Decomposition | Example |
|-------|-------|--------------|---------|
| 3 | Explicit | Named phases/agents/gates enumerated | "Step 1: Use `/worktracker` to create spike. Step 2: Invoke `/problem-solving` with all agents. Step 3: Use `orch-planner` for orchestration with adversarial critics at each phase gate." |
| 2 | Partial | At least one named stage or agent pipeline | "Use `/problem-solving` and all its agents in order, then use `/orchestration` for strategy." (sequence implied but phases not named) |
| 1 | Implied | Multi-step nature implied by conjunction; no names or order | "Research and analyze and orchestrate." |
| 0 | Monolithic | Single undifferentiated blob for a clearly multi-step task | "Tell me everything about privilege control sales in Salesforce." |

**Weight justification:** Survey §3.1 identifies prompt chaining as producing dramatic accuracy improvements. The Salesforce prompt earns a 2 here (not 3) because the phase sequence is implied but not named — the jerry-internals-investigation.md User Prompt Analysis identifies this as a gap ("implicit scope").

---

### C6 — Output Specification (Weight: 12%)

**Definition:** Whether the prompt states the expected output in terms of type (file, table, YAML, report), location (file path or skill artifact directory), and structure (sections, format).

**Measurement method (three sub-components, 1 point each):**
- **Type specified** (1 point): Output artifact type is named (e.g., "ORCHESTRATION_PLAN.md," "research report," "ADR")
- **Location specified** (1 point): File path or artifact directory is stated or inferrable from skill invocation
- **Structure specified** (1 point): Required sections, format (markdown, YAML, JSON), or template referenced

Score = sum of sub-components (0-3).

**Scoring:**

| Score | Label | Output Specification | Example |
|-------|-------|---------------------|---------|
| 3 | Complete | Type + location + structure all specified | "Produce a research report in `projects/PROJ-006/research/privilege-control-analysis.md` with L0/L1/L2 sections following the Triple-Lens format." |
| 2 | Partial | Two of three specified | "Produce a research report with L0/L1/L2 sections." (type and structure; no location) |
| 1 | Minimal | One of three specified | "Write a report." (type only) |
| 0 | Absent | None specified | No mention of output artifact, format, or location |

**Weight justification:** Survey §6.2 establishes output format specification as a quality signal that prevents superfluous text and enables programmatic post-processing. Jerry's Mandatory Persistence Protocol (Finding 5, P-05) requires a concrete file path — prompts that omit this force Claude to use the default path, which may not be what the user intends.

---

### C7 — Positive Framing (Weight: 8%)

**Definition:** Whether instructions state desired behavior rather than prohibited behavior. Measured as the ratio of positive instructions to total instructions.

**Measurement method:**
Count all instructional clauses. Classify each as:
- **Positive**: States what to do ("use X," "produce Y," "analyze Z")
- **Negative**: States what to avoid ("don't use X," "avoid Y," "never Z")

Score = 3 if negative_ratio == 0 (all positive)
Score = 2 if negative_ratio 0.01-0.20
Score = 1 if negative_ratio 0.21-0.40
Score = 0 if negative_ratio > 0.40

**Scoring:**

| Score | Label | Framing | Example |
|-------|-------|---------|---------|
| 3 | All positive | Zero negative instructions | "Use the Salesforce MCP. Produce adversarial critique at every phase." |
| 2 | Mostly positive | 1-2 negatives for explicit guardrails | "Use Salesforce MCP. Do not use hardcoded date filters — parameterize the date range." |
| 1 | Mixed | Negatives approach or match positives | "Don't use the wrong data source. Don't skip phases. Don't forget quality gates." |
| 0 | Mostly negative | Majority of instructions are prohibitions | "Don't analyze without data. Don't skip orchestration. Don't proceed without review. Don't output raw JSON." |

**Weight justification:** Lowest weight because positive framing is the most remedial of the seven criteria — it improves any prompt but the other six criteria have larger impact on Jerry-specific output quality. Evidence: Survey §2 ("say what to do instead of what to avoid"), DAIR.AI §General Tips, Jerry Anti-Patterns table (jerry-internals-investigation.md).

---

### Worked Example: Salesforce Privilege Control Prompt

**Original prompt:**
```
Claude use the /worktracker skill to create a spike.
The spike is about: Privilege Control for Servers sales trends and behavior.
You must use the /problem-solving skill and all its possible agents in-order to
help me understand the sales lifecycle of privilege control for servers within Delinea.
Data must be gathered using the Salesforce MCP that's already configured against Claude.
You must analyze the opportunities as a whole as well as focus on the patterns of the
Use the /orchestration skill and orch-planner to come up with an orchestration strategy
that includes adverserial critics at every phase where the quality factor must be >=0.92.
```

**Scored:**

| Criterion | Weight | Raw (0-3) | Weighted Points | Notes |
|-----------|--------|-----------|-----------------|-------|
| C1 Task Specificity | 20% | 2 | 13.3 | 1 trailing fragment ("patterns of the"), missing time scope |
| C2 Skill Routing | 18% | 3 | 18.0 | All three skills named with `/` syntax; `orch-planner` named |
| C3 Context Provision | 15% | 2 | 10.0 | Data source present; time range absent |
| C4 Quality Specification | 15% | 3 | 15.0 | Numeric threshold (>=0.92) AND named mechanism (adversarial critics) |
| C5 Decomposition | 12% | 2 | 8.0 | Sequence implied; phases not named |
| C6 Output Specification | 12% | 1 | 4.0 | No file path, no structure specified beyond skill invocation |
| C7 Positive Framing | 8% | 3 | 8.0 | Zero negative instructions |
| **Total** | **100%** | | **76.3** | **Tier 3 — Proficient** |

Normalized: 0.763. The prompt is functional and effective (matches Tier 3 judgment) but has a recoverable gap in output specification and task specificity that a Tier 4 revision would close.

---

## L1: Prompt Classification Taxonomy

### Overview

Six prompt types cover the Jerry use-case space. Each type has different rubric criterion emphasis and different recommended structure patterns. Use the decision guide at the end to classify your prompt before scoring.

---

### Type 1: Atomic Query

| Field | Value |
|-------|-------|
| **Description** | A single-question prompt seeking a specific factual answer, status lookup, or code snippet. No multi-step workflow required. |
| **When to Use** | Answering a discrete question about a Jerry concept, retrieving work item status, explaining a rule or pattern. |
| **Key Characteristics** | Single sentence or short paragraph. No skill invocation needed. Expected output is a direct response, not a persisted artifact. Response under 500 tokens typical. |
| **Top Rubric Criteria** | C1 (specificity), C7 (positive framing). C2 (skill routing) and C5 (decomposition) score 3 automatically. |
| **Example** | "What does the `next_agent_hint` field do in the ps-investigator state schema?" |
| **Anti-Pattern** | Using Atomic Query format for a task that actually requires agent orchestration ("Tell me about our sales data.") |

---

### Type 2: Implementation Task

| Field | Value |
|-------|-------|
| **Description** | A single-deliverable work task invoking one Jerry skill. Produces one persisted artifact. |
| **When to Use** | Writing code, creating a work item, generating an ADR, producing a single research report. |
| **Key Characteristics** | Invokes exactly one skill. Produces one named artifact. Quality gate may be implicit (peer review) or explicit (ps-critic score). Skill invocation via `/skill` syntax. |
| **Top Rubric Criteria** | C1 (specificity), C6 (output specification), C4 (quality specification). |
| **Example** | "Use `/worktracker` to create a Spike titled 'Privilege Control Sales Q1-2026' under PROJ-006, tagged to ps-researcher." |
| **Anti-Pattern** | Invoking a skill without a named output artifact or with only a verbal quality descriptor. |

---

### Type 3: Research Spike

| Field | Value |
|-------|-------|
| **Description** | An open-ended research task with defined domain scope, producing a multi-section research report via ps-researcher or a sequence of research agents. |
| **When to Use** | Investigating an unknown problem space, surveying external literature, gathering data from a named source before analysis. |
| **Key Characteristics** | `/problem-solving` skill invoked. ps-researcher typically the primary agent. Data source specified (Salesforce MCP, web search, code base). Output: research report with L0/L1/L2 sections. Divergent cognitive mode — breadth over depth. Time scope and domain scope both required. |
| **Top Rubric Criteria** | C1 (scope boundaries), C3 (data source context), C6 (output type and location). |
| **Example** | "Use `/problem-solving` and invoke ps-researcher to survey external prompt engineering best practices from 2023-2026. Data source: web search. Output: `research/external-prompt-engineering-survey.md` with L0/L1/L2 sections." |
| **Anti-Pattern** | Omitting data source constraint (Claude will hallucinate sources); omitting time scope (researcher casts too wide a net); using Implementation Task format for an inherently exploratory task. |

---

### Type 4: Multi-Skill Orchestration

| Field | Value |
|-------|-------|
| **Description** | A complex multi-phase workflow invoking two or more Jerry skills in a coordinated pipeline, typically managed by `orch-planner`. |
| **When to Use** | Any task requiring sequential or parallel agent coordination across skills (e.g., research → analysis → architecture decision → validation). Quality gates between phases. |
| **Key Characteristics** | Two or more `/skill` invocations. `orch-planner` named explicitly. Quantified quality threshold for phase gates (e.g., `>= 0.92`). Adversarial critique requested at phase boundaries. Output: ORCHESTRATION_PLAN.md + phase artifacts. |
| **Top Rubric Criteria** | C2 (all skills correctly named), C4 (numeric quality threshold), C5 (phase decomposition explicit), C6 (orchestration artifact location). |
| **Example** | The Salesforce privilege control prompt (scores Tier 3 on current rubric; would reach Tier 4 with explicit phase naming and artifact path). |
| **Anti-Pattern** | Omitting the orchestration quality threshold (orch-planner defaults to 0.85); not naming `orch-planner` (skill invokes generic orchestration behavior rather than the specific agent); decomposing phases in prose but not naming them. |

---

### Type 5: Validation Gate

| Field | Value |
|-------|-------|
| **Description** | A binary pass/fail evaluation of an existing artifact against defined acceptance criteria. Invokes ps-validator or ps-critic. |
| **When to Use** | Checking whether a completed work item meets acceptance criteria, verifying a PR against coding standards, confirming an ADR meets constitutional constraints. |
| **Key Characteristics** | Input artifact path specified. Acceptance criteria stated or referenced. Output: binary `threshold_met: true/false` with evidence list. ps-validator (haiku) for structured checklists; ps-critic (sonnet) for qualitative scoring. |
| **Top Rubric Criteria** | C1 (artifact path and criteria specified), C4 (acceptance threshold), C6 (output format: YAML or structured report). |
| **Example** | "Invoke ps-validator on `projects/PROJ-006/research/external-prompt-engineering-survey.md`. Validate against acceptance criteria: (1) 5+ external sources cited, (2) L0/L1/L2 sections present, (3) all claims have citations. Output: `analysis/validation-report.md` with binary pass/fail per criterion." |
| **Anti-Pattern** | Validation Gate without named criteria (validator must guess what to check); without named artifact path (validator reads the wrong file); requesting validation without specifying output format. |

---

### Type 6: Decision Analysis

| Field | Value |
|-------|-------|
| **Description** | A structured multi-option comparison task producing an Architecture Decision Record (ADR) or equivalent decision document. Invokes ps-architect. |
| **When to Use** | Technology selection, architectural trade-off analysis, policy decisions with multiple viable options. |
| **Key Characteristics** | Two or more options to compare stated explicitly. Evaluation dimensions named (performance, maintainability, cost, risk). Produces ADR in Nygard format. ps-architect is the primary agent. |
| **Top Rubric Criteria** | C1 (options and evaluation dimensions named), C5 (options enumerated — counts as decomposition), C6 (ADR format and location). |
| **Example** | "Use ps-architect to evaluate three persistence options for Jerry work items: (1) YAML files, (2) SQLite, (3) Event store with JSON snapshots. Evaluation dimensions: read latency, write simplicity, corruption recovery. Output: ADR in `decisions/ADR-001-persistence-strategy.md` using Nygard format." |
| **Anti-Pattern** | Decision Analysis prompt that names options but omits evaluation dimensions (ps-architect must invent criteria, introducing arbitrary weighting); not specifying Nygard format (output structure varies). |

---

### Prompt Type Decision Guide

```
Does the prompt seek a factual answer with no persisted artifact?
  YES → Type 1: Atomic Query
  NO  ↓

Does the prompt invoke exactly one skill with one named output artifact?
  YES → Type 2: Implementation Task (or Type 3 if that skill is /problem-solving + ps-researcher)
  NO  ↓

Does the prompt invoke /problem-solving with ps-researcher as primary agent?
  YES → Type 3: Research Spike
  NO  ↓

Does the prompt invoke two or more skills or name orch-planner?
  YES → Type 4: Multi-Skill Orchestration
  NO  ↓

Does the prompt specify an existing artifact and binary pass/fail criteria?
  YES → Type 5: Validation Gate
  NO  ↓

Does the prompt enumerate 2+ options for comparison with evaluation dimensions?
  YES → Type 6: Decision Analysis
  NO  → Re-examine. If none fit, most likely a Type 2 with missing output specification.
```

---

## L1: Effectiveness Tier Definitions

### Tier System

| Tier | Label | Normalized Score | Raw Score |
|------|-------|-----------------|-----------|
| 4 | Exemplary | 0.90-1.00 | 90-100 |
| 3 | Proficient | 0.75-0.89 | 75-89 |
| 2 | Developing | 0.50-0.74 | 50-74 |
| 1 | Inadequate | 0.00-0.49 | 0-49 |

---

### Tier 4 — Exemplary (0.90-1.00)

**Observable Characteristics:**

| Observable | Description |
|-----------|-------------|
| Zero specificity gaps | No undefined terms, no trailing fragments, no missing constraints |
| All skills invoked with exact syntax | `/skill` prefix used; agent names (e.g., `orch-planner`, `ps-critic`) named where relevant |
| Numeric quality threshold present | A specific number (e.g., `>= 0.92`) is stated for at least one quality gate |
| Phases explicitly named | If multi-step, phases are listed in order with names (e.g., "Phase 1: Research," "Phase 2: Analysis") |
| Output fully specified | File path, format, and structure (or template reference) all present |
| Data source named | The specific tool, API, or source is named (e.g., "Salesforce MCP," "web search," "code base at `src/`") |
| All positive framing | Zero negative instructions |

**What Tier 4 prompts reliably produce:** Fully orchestrated workflows that complete without clarification requests; artifacts written to the correct paths; quality gates triggered at the correct thresholds; reproducible results across sessions.

**Tier 4 example (revised Salesforce prompt):**
```
Use `/worktracker` to create a Spike titled "Privilege Control for Servers Sales Trends Q1-2026" under PROJ-006.

Then use `/problem-solving` to invoke the following agents in order:
1. ps-researcher: gather Salesforce opportunity data from 2024-01-01 to 2026-02-18 via Salesforce MCP. Output: `research/privilege-control-salesforce-data.md` with L0/L1/L2 sections.
2. ps-analyst: analyze sales lifecycle patterns and macro opportunity trends. Output: `analysis/privilege-control-analysis.md`.
3. ps-architect: synthesize findings into strategic recommendations. Output: `decisions/ADR-privilege-control-sales.md` in Nygard format.

Use `/orchestration` and `orch-planner` to orchestrate the above pipeline. Include ps-critic adversarial critique after each phase; quality factor must be >= 0.92 for each phase before proceeding to the next. Output orchestration plan to `orchestration/privilege-control-20260218-001/ORCHESTRATION_PLAN.md`.
```

---

### Tier 3 — Proficient (0.75-0.89)

**Observable Characteristics:**

| Observable | Description |
|-----------|-------------|
| 1-2 specificity gaps | Minor undefined terms or missing constraints; task intent is unambiguous |
| Core skills invoked | Skills invoked with `/` syntax; at least one agent named; may miss secondary agents |
| Quality mechanism present | Named review mechanism or numeric threshold; may not have both |
| Sequence implied | Order of operations inferrable from prompt structure; phases not formally named |
| Output partially specified | Artifact type stated; location or structure may be missing |
| Data source present | Tool or source named; configuration details may be omitted |
| Positive framing dominant | Zero or one negative instruction |

**What Tier 3 prompts reliably produce:** Functionally correct workflows that complete the primary task. Artifacts produced to default paths (not necessarily the intended path). One round of clarification may be needed for edge cases.

**Example:** The original Salesforce privilege control prompt scores Tier 3.

---

### Tier 2 — Developing (0.50-0.74)

**Observable Characteristics:**

| Observable | Description |
|-----------|-------------|
| 3-4 specificity gaps | Multiple undefined terms; task intent requires inference |
| Skill invocation partial or absent | Skills referenced by name but without `/` syntax, or only one of several needed skills invoked |
| Quality specification verbal only | "Be thorough," "ensure accuracy" — no numeric threshold, no named mechanism |
| Decomposition implicit | Multi-step task presented as prose; order and phases must be inferred |
| Output type only | Artifact type may be stated ("a report") but no location or structure |
| Data source vague or absent | "Use our CRM data" without naming the specific tool or MCP |
| Mixed framing | Both positive and negative instructions present |

**What Tier 2 prompts reliably produce:** Claude will attempt the task but will make structural decisions (file paths, phase order, quality thresholds) that may not match user intent. Multiple back-and-forth turns required.

**Example:**
```
Research privilege control sales data and analyze it. Use the problem-solving skill. Make sure the analysis is good and thorough. Then create an orchestration plan.
```

---

### Tier 1 — Inadequate (0.00-0.49)

**Observable Characteristics:**

| Observable | Description |
|-----------|-------------|
| 5+ specificity gaps | Task intent is ambiguous; multiple interpretations possible |
| No skill invocation | No Jerry skill syntax; Claude must guess whether to use skills at all |
| No quality signal | No threshold, no review mechanism, no acceptance criteria of any kind |
| No decomposition | Complex task stated as single undifferentiated request |
| No output specification | No artifact type, location, or format |
| No data source | Source of truth left unspecified |
| Negative framing dominant | Instructions primarily state what not to do |

**What Tier 1 prompts reliably produce:** One of three outcomes: (1) Claude asks multiple clarifying questions; (2) Claude produces a generic response using default assumptions that misses the intent; (3) Claude produces a well-structured response for the wrong task. All three outcomes require significant rework.

**Example:**
```
Can you help me understand our sales better? I want to know patterns and trends. Don't make it too complicated. Analyze the data.
```

---

## L1: Jerry-Specific Rubric Extensions

Four criteria exist for Jerry prompts that have no equivalent in general prompt engineering literature. These criteria appear implicitly in C2 and C4 of the main rubric; this section makes them explicit for advanced users evaluating complex orchestration prompts.

---

### JE1 — Skill Invocation Correctness

**Definition:** Whether the correct skill is invoked for the task type. Distinct from C2 (which measures whether skills are named with correct syntax); this measures whether the right skill was chosen.

**Measurement:** Binary per skill invoked. A skill invocation is correct if:
- The task type matches the skill's activation keywords (from SKILL.md YAML frontmatter)
- The invoked skill has an agent capable of producing the required output
- No skill is invoked whose output is not used in the workflow

**Scoring scale:**
- All invocations correct (0 wrong skills): 3
- One incorrect or superfluous invocation: 2
- Two incorrect or superfluous invocations: 1
- No skills invoked when skill(s) required, OR all invocations incorrect: 0

**Failure mode example:** Invoking `/nasa-se` for a simple code review task — the skill has appropriate agents but the overhead and artifact structure are disproportionate to the task. Invoking `/orchestration` for a single-step task that does not require inter-agent coordination.

**Evidence base:** Jerry internals (Finding 1, P-01): `activation-keywords` exist precisely to guide correct skill selection. Skills are not interchangeable; wrong invocation loads incorrect context and agent prompts.

---

### JE2 — Agent Composition Quality

**Definition:** Whether the agent pipeline in the prompt matches the logical workflow for the task type. Evaluated against the implicit `next_agent_hint` routing embedded in agent state schemas.

**Measurement:** Compare the stated or implied agent sequence to the canonical pipeline from jerry-internals-investigation.md (Extended Agent Coverage: `next_agent_hint` routing):
```
ps-researcher → ps-analyst → [ps-architect | ps-synthesizer] → ps-validator → ps-reporter
```

Count violations: skipped agents for complex tasks, reversed order, or using a heavy agent (ps-architect/opus) for a task appropriate to a light agent (ps-validator/haiku).

**Scoring scale:**
- Canonical sequence used; no violations: 3
- One violation (skipped agent that would improve quality): 2
- Two violations: 1
- Completely non-canonical sequence or no agent sequencing for multi-agent task: 0

**Failure mode example:** "Use ps-architect to research Salesforce data" — ps-researcher (not ps-architect) is the correct research agent; ps-architect handles architectural decisions after research is complete.

**Evidence base:** Jerry internals (Extended Agent Coverage §: "researcher→analyst→synthesizer→architect pipeline is implicit in `next_agent_hint` routing").

---

### JE3 — Orchestration Pattern Selection

**Definition:** Whether the prompt selects the appropriate orchestration workflow pattern for the task's complexity and structure.

**Measurement:** The orchestration PLAYBOOK defines 8 patterns. Score based on match:
- Named pattern matches task characteristics: 3
- Unnamed but appropriate pattern (Claude infers correctly from task description): 2
- Named pattern that does not match task characteristics: 1
- No orchestration pattern consideration for a task requiring coordination: 0

**Key patterns and their trigger characteristics:**
- **Sequential Pipeline**: Tasks with strict ordering; each step depends on previous output
- **Parallel with Barrier Sync**: Independent subtasks that must complete before a shared next step
- **Adversarial Critique Loop**: Quality-sensitive tasks requiring devil's advocate review
- **Generator-Critic-Revise**: Single deliverable needing iterative improvement with quality gate

**Failure mode example:** Requesting "adversarial critics at every phase" (Adversarial Critique Loop) when the workflow is actually three independent parallel analyses that should use Parallel with Barrier Sync + one shared adversarial review at the end. The mismatched pattern triples the critique cost unnecessarily.

**Evidence base:** Jerry internals (Finding 7, P-07): the circuit breaker schema and four critique modes (Devil's Advocate, Steelman, Red Team, Blue Team) are invoked at the workflow level, not per-deliverable.

---

### JE4 — Quality Gate Specification

**Definition:** Whether the prompt provides the information that ps-critic needs to operate its circuit breaker correctly: a numeric threshold, an iteration limit (or acceptance of default), and the phases at which critique fires.

**Measurement (three sub-components):**
- **Threshold present** (e.g., `>= 0.92`): 1 point
- **Phase gates specified** (e.g., "at every phase," "after research and after analysis"): 1 point
- **Criterion weighting or rubric referenced** (optional; defaults exist): 1 point

Score = sum of points (0-3).

Note: Threshold of 0.85 is the ps-critic default; prompts that omit a threshold still function but use the default.

**Scoring scale:**
- 3: Threshold + phases + criterion weighting or named rubric
- 2: Threshold + phases (no criterion weighting)
- 1: Threshold only, or phases only
- 0: No quality gate specification

**Failure mode example:** "Have ps-critic review everything." — No threshold (defaults to 0.85), no phase specification (critic fires at unknown points), no criterion weighting (equal weights used for all criteria).

**Evidence base:** Jerry internals (Finding 7, P-07): the ps-critic circuit breaker schema requires `quality_score >= acceptance_threshold` to stop; the `acceptance_threshold` defaults to 0.85 from `ps-critic.md` but is overridden by the user prompt value. The circuit breaker also requires knowing *when* to fire (which phases).

---

## L2: Design Rationale and Evidence Mapping

### Criterion Weight Justification Table

| Criterion | Weight | Primary Evidence | Secondary Evidence | Rationale |
|-----------|--------|-----------------|-------------------|-----------|
| C1 Task Specificity | 20% | Survey §1.2 (Anthropic "golden rule"); User Prompt Analysis (trailing fragment gap) | DAIR.AI General Tips ("more descriptive = better results") | Specificity is the first-order cause of most LLM failures; all other improvements depend on a clear task statement |
| C2 Skill Routing | 18% | Jerry internals P-01 (YAML activation-keywords); SKILL.md frontmatter evidence | Survey §3.2 (agent skill authoring: skill discovery reliability) | Jerry-unique criterion; wrong skill loads wrong agent prompts — a structural failure no other criterion can compensate for |
| C3 Context Provision | 15% | Survey §1.2 (four context dimensions); Layer 5/CLAUDE.md (persistent context already loaded) | Survey §2 (agent skills: "context window is a public good") | Context must be sufficient but not wasteful; weight accounts for Jerry's persistent context layer reducing the user's burden |
| C4 Quality Specification | 15% | Survey §6.1 (success criteria prerequisite); Jerry internals P-07 circuit breaker | User Prompt Analysis (>=0.92 maps to ps-critic acceptance_threshold) | Numeric quality gates are the mechanism by which ps-critic's circuit breaker operates correctly; missing threshold defaults to 0.85 |
| C5 Decomposition | 12% | Survey §3.1 (prompt chaining: "dramatic improvements in accuracy"); User Prompt Analysis ("implicit scope" identified as gap) | Survey anti-patterns ("monolithic prompts" as root cause of degraded quality) | Decomposition improves per-phase focus; lower weight than specificity because orch-planner can infer sequence from a well-specified task description |
| C6 Output Specification | 12% | Survey §6.2 (output format as quality signal); Jerry internals P-05 (mandatory persistence path) | Jerry internals Finding 5 ("concrete file path removes ambiguity about where to write") | Equal weight to decomposition; missing output path causes artifacts to land at defaults, creating cross-session state management problems |
| C7 Positive Framing | 8% | Survey §2 (DAIR.AI: "don't instruct what NOT to do"); Survey anti-patterns ("negative framing" #1) | Jerry anti-patterns table (jerry-internals-investigation.md) | Lowest weight; positive framing is hygiene, not structure. The other six criteria have larger impact on Jerry-specific quality than framing alone |

### Taxonomy Evidence Map

| Prompt Type | Primary Evidence | Defining Characteristic from Evidence |
|-------------|-----------------|---------------------------------------|
| Atomic Query | Survey §1.1 (role prompting for direct answers); Layer 5 context | No skill invocation; response is transient (no persistence required) |
| Implementation Task | Jerry internals P-05 (mandatory persistence); Survey §6.2 (output format) | Single skill, single persisted artifact |
| Research Spike | Jerry internals P-01 (ps-researcher, divergent cognitive mode); Survey §3.1 (chaining) | Divergent cognitive mode (ps-researcher, only divergent agent); breadth-first |
| Multi-Skill Orchestration | Jerry internals P-07 (adversarial critique loop); P-06 (state schema as API) | Two or more skills; orch-planner; quantified phase gate |
| Validation Gate | Jerry internals (ps-validator haiku, binary pass/fail); Survey §6.1 (evaluation-driven dev) | Existing artifact + acceptance criteria → binary output |
| Decision Analysis | Jerry internals (ps-architect, ADR Nygard format); Survey §1.1 (role definition effectiveness) | Multi-option comparison; ps-architect; ADR output |

### Carry-Forward Compliance

| Carry-Forward Note | How Addressed |
|-------------------|---------------|
| Cognitive mode effectiveness claim is speculative | JE2 (Agent Composition Quality) uses the `next_agent_hint` routing observable (structural evidence) rather than the cognitive mode declaration itself. The divergent/convergent declaration is referenced for context but is not a scored criterion. |
| ReAct benchmarks are 2022-era — qualify for frontier model applicability | Survey references in this document cite ReAct for the directional finding (interleaved reasoning + action outperforms either alone) without claiming specific benchmark numbers apply to current models. C4 (Quality Specification) uses numeric thresholds from Jerry's own circuit breaker, not from academic benchmarks. |

### What This Rubric Does Not Cover

**Intentional exclusions:**

1. **Context window economics (token cost)**: Survey §Research Gaps identifies this as unquantified in existing literature. The rubric does not attempt to score optimal prompt length, as no empirical baseline exists.

2. **Model-tier calibration for user prompts**: Survey §8 identifies prompt calibration by model tier as a gap in external literature. Jerry agents handle this internally (via YAML `model:` field); user prompts do not currently select model tiers. This is a design gap that a future rubric version could address once the multi-tier calibration framework is established.

3. **Few-shot example quality**: Survey §4 (multishot prompting) is relevant for skill authoring but user prompts in Jerry do not typically embed examples — they invoke skills that already embed examples. A separate rubric for skill authoring (not user prompts) would include this criterion.

4. **Tool description quality**: Survey §5.1 is relevant for MCP tool description authors, not for Jerry users writing task prompts.

---

*Document Version: 1.0.0*
*Agent: ps-architect*
*Constitutional Compliance: P-001 (all claims cited), P-002 (persisted), P-003 (no subagents), P-022 (limitations documented)*
*Created: 2026-02-18*
