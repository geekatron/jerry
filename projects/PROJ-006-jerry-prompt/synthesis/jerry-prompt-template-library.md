# Jerry Prompt Template Library

> **Document ID:** PROJ-006-RPT-001
> **Agent:** ps-reporter (problem-solving skill)
> **Version:** 1.0.0
> **Date:** 2026-02-18
> **Status:** COMPLETE
> **Phase:** Phase 3 — Synthesis / Reporting
> **Input Artifacts:**
> - `synthesis/jerry-prompt-best-practices-guide.md` (ps-synthesizer, PROJ-006-SYN-001)
> - `analysis/prompt-quality-rubric-taxonomy.md` (ps-architect, PROJ-006-ARCH-001)
> - `analysis/prompt-pattern-analysis.md` (ps-analyst, PROJ-006-ANA-001)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [How to Use This Library](#how-to-use-this-library) | Usage instructions and placeholder conventions |
| [Template 1: Research Spike](#template-1-research-spike) | Open-ended research investigation prompt |
| [Template 2: Implementation Task](#template-2-implementation-task) | Single-skill code or artifact creation |
| [Template 3: Multi-Skill Orchestration](#template-3-multi-skill-orchestration) | Full pipeline with quality gates |
| [Template 4: Architecture Decision](#template-4-architecture-decision) | ADR production via ps-architect |
| [Template 5: Bug Investigation](#template-5-bug-investigation) | Root-cause analysis via ps-investigator |
| [Template Quick-Select Guide](#template-quick-select-guide) | One-line decision aid for choosing the right template |
| [Rubric Scores for Each Template](#rubric-scores-for-each-template) | Expected quality tier per template |

---

## How to Use This Library

Each template is **immediately copy-pasteable**. Replace every `{{PLACEHOLDER}}` with your specific value before submitting.

**Placeholder convention:**

| Placeholder | What to Replace With |
|-------------|---------------------|
| `{{PROJECT_ID}}` | Your Jerry project ID, e.g., `PROJ-006` |
| `{{WORK_ITEM_TITLE}}` | Descriptive title for the work item |
| `{{DOMAIN}}` | The subject area, e.g., `authentication service in src/Delinea.Inventory.Logic/` |
| `{{DATA_SOURCE}}` | The named tool or location, e.g., `Salesforce MCP`, `web search`, `codebase at src/` |
| `{{START_DATE}}` / `{{END_DATE}}` | ISO 8601 dates, e.g., `2024-01-01` / `2026-02-18` |
| `{{FOCUS_AREAS}}` | Comma-separated list of research dimensions |
| `{{OUTPUT_PATH}}` | Relative file path under `projects/{{PROJECT_ID}}/` |
| `{{QUALITY_THRESHOLD}}` | Decimal 0.0–1.0, e.g., `0.90` |
| `{{AGENT}}` | Named ps-agent, e.g., `ps-researcher`, `ps-investigator` |
| `{{FILE_PATH}}` | Absolute or project-relative path to file under review |

**Minimum required replacements before any template is valid:** `{{PROJECT_ID}}`, `{{DOMAIN}}`, `{{OUTPUT_PATH}}`.

---

## Template 1: Research Spike

### Purpose

Kick off an open-ended research investigation using ps-researcher. Produces a structured research report with L0/L1/L2 audience sections. Use when you need to survey a problem space, gather external best practices, or collect data from a specific source before analysis.

### When to Use

- You are exploring a topic you do not yet understand well
- You need to gather data from Salesforce, the codebase, the web, or another named source
- You want a landscape overview before commissioning deeper analysis
- You need a traceable, persistent research artifact for downstream agents to consume

### Template Text

```
Use /worktracker to create a Spike titled "{{WORK_ITEM_TITLE}}" under {{PROJECT_ID}}.

Use /problem-solving with ps-researcher to survey {{DOMAIN}} from {{START_DATE}} to {{END_DATE}}.
Data source: {{DATA_SOURCE}}.
Focus areas: {{FOCUS_AREAS}}.
Output: projects/{{PROJECT_ID}}/research/{{OUTPUT_PATH}} with L0/L1/L2 sections.

Include ps-critic adversarial critique after the research phase.
Quality threshold: >= {{QUALITY_THRESHOLD}}.
```

### Filled Example

```
Use /worktracker to create a Spike titled "Authentication Patterns Survey Q1-2026" under PROJ-007.

Use /problem-solving with ps-researcher to survey token-based authentication patterns
for .NET microservices from 2023-01-01 to 2026-02-18.
Data source: web search (WebSearch and WebFetch tools).
Focus areas: JWT expiry strategies, refresh token rotation, revocation patterns, .NET 9 implementation.
Output: projects/PROJ-007/research/auth-patterns-survey.md with L0/L1/L2 sections.

Include ps-critic adversarial critique after the research phase.
Quality threshold: >= 0.85.
```

### Annotated Anatomy

```
Use /worktracker to create a Spike titled "{{WORK_ITEM_TITLE}}" under {{PROJECT_ID}}.
│
└─ WORK ITEM ANCHOR
   Creates traceability between this research and your project's work tracking state.
   "Spike" is the correct Jerry work item type for time-boxed research with no
   guaranteed deliverable. The title becomes the artifact's human-readable handle.

Use /problem-solving with ps-researcher to survey {{DOMAIN}} from {{START_DATE}} to {{END_DATE}}.
│             │               │             │           │
│             │               │             │           └─ TIME SCOPE
│             │               │             │              Bounds ps-researcher's search temporally.
│             │               │             │              Prevents stale content from entering the survey.
│             │               │             │
│             │               │             └─ DOMAIN SCOPE
│             │               │                Scopes the breadth-first research to your subject area.
│             │               │                "within Delinea" or a file path further narrows the scope.
│             │               │
│             │               └─ AGENT SELECTION: ps-researcher
│             │                  Divergent cognitive mode. Uses 5W1H exploration framework.
│             │                  Routes to Opus model tier for deep open-ended reasoning.
│             │                  Correct choice when you want breadth, not a specific root cause.
│             │
│             └─ SKILL INVOCATION: /problem-solving
│                Triggers YAML frontmatter routing in problem-solving SKILL.md.
│                Without this slash-command, Jerry's agent architecture is bypassed.
│
Data source: {{DATA_SOURCE}}.
│
└─ DATA SOURCE CONSTRAINT
   Tells ps-researcher exactly which tool(s) to use. Prevents hallucinated data sources.
   Examples: "Salesforce MCP already configured against Claude", "web search (WebSearch tool)",
   "codebase at src/Delinea.Inventory.Logic/".

Focus areas: {{FOCUS_AREAS}}.
│
└─ FOCUS DIMENSIONS
   Narrows breadth-first research to the specific angles you care about.
   Without this, ps-researcher casts an unnecessarily wide net.
   List 3–5 named dimensions. Each dimension becomes a section in the output.

Output: projects/{{PROJECT_ID}}/research/{{OUTPUT_PATH}} with L0/L1/L2 sections.
│                                                           │
│                                                           └─ OUTPUT FORMAT
│                                                              "with L0/L1/L2 sections" triggers
│                                                              the Triple-Lens output framework:
│                                                              L0 = stakeholder summary (~200 words)
│                                                              L1 = engineer-level findings
│                                                              L2 = deep architect-level detail
│
└─ OUTPUT PATH
   Exact file path for Mandatory Persistence Protocol compliance.
   Without this, the artifact lands at a default location that may be
   hard to find in future sessions.

Include ps-critic adversarial critique after the research phase.
Quality threshold: >= {{QUALITY_THRESHOLD}}.
│                      │
│                      └─ QUALITY THRESHOLD
│                         Overrides ps-critic's default acceptance_threshold of 0.85.
│                         Use 0.80-0.85 for exploratory research, 0.90+ for consequential work.
│
└─ ADVERSARIAL CRITIQUE REQUEST
   Activates the highest-impact quality pattern (P-07). Without this line,
   no critique loop fires at all. ps-critic applies four modes: Devil's Advocate,
   Steelman, Red Team, Blue Team.
```

### Expected Output

A research report at the specified path containing:
- **L0**: Executive summary (~200 words, for stakeholders and managers)
- **L1**: Detailed findings with evidence and citations (for developers)
- **L2**: Deep-dive technical analysis with trade-offs (for architects)
- Citations and evidence for all factual claims

---

## Template 2: Implementation Task

### Purpose

Request a single-skill code implementation, code review, or artifact creation. Produces one named deliverable with explicit quality criteria.

### When to Use

- You are implementing a specific class, handler, test, or configuration
- You are requesting a code review of an existing artifact
- You need one deliverable from one Jerry skill (no multi-phase pipeline needed)
- The quality gate is a verifiable criterion (test pass, coverage %, review finding)

### Template Text

```
Use /problem-solving with {{AGENT}} to {{TASK_DESCRIPTION}}.

Input artifact: {{FILE_PATH}}
Review/implementation dimensions:
- {{CRITERION_1}}
- {{CRITERION_2}}
- {{CRITERION_3}}

Output: projects/{{PROJECT_ID}}/{{OUTPUT_PATH}} with {{SEVERITY_OR_FORMAT}} per finding.
```

### Filled Example — Code Review

```
Use /problem-solving with ps-reviewer to review the UpdateAssetHandler implementation
for code quality, correctness, and standards compliance.

Input artifact: src/Delinea.Inventory.Logic/Handlers/Commands/UpdateAssetHandler.cs
Review dimensions:
- SOLID principles compliance (SRP and DIP specifically)
- Exception handling: must catch specific exception types, never base Exception class
- NSubstitute mock setup correctness in UpdateAssetHandlerTests.cs
- Test coverage >= 90% on all branches

Output: projects/PROJ-007/reviews/update-asset-handler-review.md
with CRITICAL/HIGH/MEDIUM/LOW severity classification per finding.
```

### Filled Example — Implementation

```
Use /problem-solving with ps-architect to design the IAssetRepository interface
for CosmosDB-backed asset storage.

Domain: Delinea.Inventory.Data project; CosmosDB multi-tenant storage pattern.
Design dimensions:
- CRUD operations with tenant isolation
- Pagination support for large asset collections
- Concurrency via optimistic locking with ETag

Output: projects/PROJ-007/decisions/ADR-003-asset-repository-interface.md
in Nygard ADR format.
```

### Annotated Anatomy

```
Use /problem-solving with {{AGENT}} to {{TASK_DESCRIPTION}}.
│                    │              │
│                    │              └─ TASK DESCRIPTION
│                    │                 One clear, complete sentence. Verb + object + purpose.
│                    │                 No trailing fragments. No ambiguous pronouns.
│                    │
│                    └─ AGENT SELECTION
│                       ps-reviewer → code/design review (SOLID, OWASP, severity classification)
│                       ps-architect → architecture decisions, interface design (ADR Nygard format)
│                       ps-analyst → structured analysis with trade-offs (FMEA framework)
│                       ps-validator → binary pass/fail verification against criteria
│
Input artifact: {{FILE_PATH}}
│
└─ INPUT ARTIFACT
   Exact file path to the artifact being reviewed or extended.
   Eliminates all ambiguity about what Claude is acting on.
   For implementation tasks, replace with "Domain: ..." if no input file exists.

Review/implementation dimensions:
- {{CRITERION_1}}
│
└─ NAMED DIMENSIONS (C1 Task Specificity)
   Each dimension is a concrete, verifiable criterion.
   Avoid vague descriptors: NOT "good code quality" but "SOLID principles: SRP and DIP".
   Numeric criteria ("coverage >= 90%") are stronger than verbal ones ("thorough coverage").
   3–5 dimensions is the right scope for a single-agent task.

Output: projects/{{PROJECT_ID}}/{{OUTPUT_PATH}} with {{SEVERITY_OR_FORMAT}} per finding.
│                                                 │
│                                                 └─ OUTPUT FORMAT
│                                                    Names the structure Claude must use.
│                                                    For reviews: CRITICAL/HIGH/MEDIUM/LOW
│                                                    For ADRs: "Nygard format"
│                                                    For reports: "L0/L1/L2 sections"
│
└─ OUTPUT PATH
   Full project-relative path. Makes the artifact retrievable across sessions.
```

### Expected Output

A single artifact at the specified path with:
- Structured findings organized by the named dimensions
- Severity or priority classification per finding
- Evidence and specific file/line references for reviewable items
- Concrete recommended actions for each finding

---

## Template 3: Multi-Skill Orchestration

### Purpose

Launch a full multi-phase pipeline with work tracking, problem-solving agents, orchestration planning, and adversarial quality gates. This is the highest-quality Jerry prompt pattern. Use for any research or analysis task where being wrong has significant consequences.

### When to Use

- The task has more than two distinct phases (research → analysis → synthesis/decision)
- Quality at phase boundaries matters, not just final output quality
- Multiple agents in sequence are needed
- Results need to be reproducible across sessions
- You are making an architectural, security, or strategic decision

### Template Text

```
Use /worktracker to create a {{WORK_ITEM_TYPE}} titled "{{WORK_ITEM_TITLE}}" under {{PROJECT_ID}}.

Use /problem-solving to invoke the following agents in order:

Phase 1 — Research: ps-researcher gathers {{RESEARCH_SUBJECT}}
from {{START_DATE}} to {{END_DATE}} via {{DATA_SOURCE}}.
Focus areas: {{FOCUS_AREAS}}.
Output: projects/{{PROJECT_ID}}/research/{{RESEARCH_OUTPUT_PATH}} with L0/L1/L2 sections.

Phase 2 — Analysis: ps-analyst analyzes {{ANALYSIS_SUBJECT}} from Phase 1 output.
Apply {{ANALYSIS_METHOD}} to identify {{ANALYSIS_TARGET}}.
Output: projects/{{PROJECT_ID}}/analysis/{{ANALYSIS_OUTPUT_PATH}}.

Phase 3 — Decision: ps-architect synthesizes findings into recommendations.
Evaluate options: (A) {{OPTION_A}}, (B) {{OPTION_B}}.
Evaluation dimensions: {{EVALUATION_DIMENSIONS}}.
Output: projects/{{PROJECT_ID}}/decisions/{{DECISION_OUTPUT_PATH}} in Nygard ADR format.

Use /orchestration and orch-planner to sequence the above pipeline.
Include ps-critic adversarial critique after each phase.
Quality threshold: >= {{QUALITY_THRESHOLD}} per phase before proceeding to the next.
Output orchestration plan: projects/{{PROJECT_ID}}/orchestration/{{WORKFLOW_ID}}/ORCHESTRATION_PLAN.md.
```

### Filled Example

```
Use /worktracker to create a Spike titled "CosmosDB vs. Event Store Persistence Q1-2026" under PROJ-007.

Use /problem-solving to invoke the following agents in order:

Phase 1 — Research: ps-researcher surveys persistence patterns for event-sourced
.NET microservices from 2023-01-01 to 2026-02-18 via web search (WebSearch tool).
Focus areas: CosmosDB change feed, event store libraries for .NET, snapshot strategies,
multi-tenant partition schemes.
Output: projects/PROJ-007/research/persistence-patterns-survey.md with L0/L1/L2 sections.

Phase 2 — Analysis: ps-analyst compares CosmosDB and event store approaches from Phase 1 output.
Apply FMEA analysis to identify failure risks in each approach for a multi-tenant inventory service.
Output: projects/PROJ-007/analysis/persistence-comparison.md.

Phase 3 — Decision: ps-architect synthesizes findings into a persistence strategy recommendation.
Evaluate options: (A) CosmosDB with change feed, (B) custom event store with JSON snapshots.
Evaluation dimensions: read latency, write throughput, corruption recovery, operational complexity.
Output: projects/PROJ-007/decisions/ADR-004-persistence-strategy.md in Nygard ADR format.

Use /orchestration and orch-planner to sequence the above pipeline.
Include ps-critic adversarial critique after each phase.
Quality threshold: >= 0.92 per phase before proceeding to the next.
Output orchestration plan: projects/PROJ-007/orchestration/persistence-research-20260218-001/ORCHESTRATION_PLAN.md.
```

### Annotated Anatomy

```
Use /worktracker to create a {{WORK_ITEM_TYPE}} titled "{{WORK_ITEM_TITLE}}" under {{PROJECT_ID}}.
│
└─ WORK ITEM ANCHOR (first, always)
   Creates the traceability link between this orchestration run and project state.
   Place this FIRST — it creates the anchor that every subsequent phase references.
   Work item type: Spike (research), Story (implementation), Task (granular work).

Use /problem-solving to invoke the following agents in order:
│
└─ SKILL INVOCATION
   "/problem-solving" triggers YAML routing. The phrase "in order" tells orch-planner
   to use a Sequential Pipeline pattern, not Parallel with Barrier Sync.

Phase 1 — Research: ps-researcher gathers {{RESEARCH_SUBJECT}}
│          │
│          └─ NAMED PHASE + NAMED AGENT
│             Both the phase number/name AND the agent name must be explicit.
│             This gives orch-planner enough information to assign each phase
│             to the correct agent without inference.
│
from {{START_DATE}} to {{END_DATE}} via {{DATA_SOURCE}}.
│                                    │
│                                    └─ DATA SOURCE CONSTRAINT
│                                       Prevents ps-researcher from hallucinating sources.
└─ TIME SCOPE

Focus areas: {{FOCUS_AREAS}}.
│
└─ RESEARCH DIMENSIONS
   3–5 named dimensions for each research phase. Prevents the breadth-first agent
   from producing an unfocused landscape dump.

Phase 2 — Analysis: ps-analyst analyzes ... Apply {{ANALYSIS_METHOD}}.
│                                            │
│                                            └─ METHODOLOGY NAME
│                                               "FMEA", "trade-off matrix", "Pareto analysis".
│                                               Names the ps-analyst framework to apply.
│                                               ps-analyst knows these frameworks natively.
│
└─ CHAINED INPUT (implicit)
   "from Phase 1 output" tells orch-planner that Phase 2 depends on Phase 1 completion.
   This creates an explicit dependency that orch-planner honors as a sync barrier.

Phase 3 — Decision: ps-architect ... Evaluate options: (A) ..., (B) ...
│                                     │
│                                     └─ EXPLICIT OPTIONS
│                                        Naming options A and B forces ps-architect into
│                                        Decision Analysis mode (Type 6 in the taxonomy).
│                                        Vague "evaluate the best approach" produces inferior output.
└─ OUTPUT FORMAT: "in Nygard ADR format"
   ADR Nygard = Title, Status, Context, Decision, Consequences sections.
   Named format tells ps-architect exactly what structure to use.

Use /orchestration and orch-planner to sequence the above pipeline.
│                 │
│                 └─ EXPLICIT AGENT NAME: orch-planner
│                    Routes to the specific orchestration agent, not generic behavior.
│
Include ps-critic adversarial critique after each phase.
│
└─ ADVERSARIAL CRITIQUE REQUEST (P-07)
   This single line activates the highest-impact quality pattern in Jerry.
   Without it, NO adversarial critique loop fires — not at 0.85, not at any threshold.
   "After each phase" applies the loop at every phase boundary, not just the final output.

Quality threshold: >= {{QUALITY_THRESHOLD}} per phase before proceeding to the next.
│
└─ NUMERIC QUALITY GATE
   Overrides ps-critic's default acceptance_threshold of 0.85.
   Recommended values: 0.85 for research, 0.90 for architecture, 0.92 for security.
   "Per phase" ensures each phase must independently meet the threshold.

Output orchestration plan: projects/{{PROJECT_ID}}/orchestration/{{WORKFLOW_ID}}/ORCHESTRATION_PLAN.md.
│
└─ ORCHESTRATION ARTIFACT PATH
   Names where orch-planner writes the ORCHESTRATION_PLAN.md.
   This file becomes the persistent runtime state for the workflow.
   Without a named path, the plan goes to a default location that may not be
   retrievable in future sessions.
```

### Expected Output

1. **ORCHESTRATION_PLAN.md** — The workflow plan with phases, agents, sync barriers, and quality gate configuration
2. **Phase 1 research artifact** — Research report with L0/L1/L2 sections at the specified path
3. **ps-critic critique reports** — Adversarial critique for each phase (Devil's Advocate, Steelman, Red Team, Blue Team)
4. **Phase 2 analysis artifact** — Structured analysis at the specified path
5. **Phase 3 decision artifact** — ADR in Nygard format at the specified path

---

## Template 4: Architecture Decision

### Purpose

Request a structured Architecture Decision Record (ADR) from ps-architect. Use when you need to make a technology selection or design trade-off with documented rationale.

### When to Use

- You have two or more viable implementation options
- You need the decision documented with context, trade-offs, and consequences
- The decision will be referenced by future work items

### Template Text

```
Use /problem-solving with ps-architect to evaluate {{NUM_OPTIONS}} options for {{DECISION_SUBJECT}}.

Options:
{{A}}. {{OPTION_A_DESCRIPTION}}
{{B}}. {{OPTION_B_DESCRIPTION}}
{{C}}. {{OPTION_C_DESCRIPTION}} (if applicable)

Evaluation dimensions: {{DIMENSION_1}}, {{DIMENSION_2}}, {{DIMENSION_3}}.

Context: {{CONTEXT_FILE_PATH_OR_INLINE_CONTEXT}}

Output: projects/{{PROJECT_ID}}/decisions/{{ADR_FILENAME}} in Nygard ADR format.
```

### Filled Example

```
Use /problem-solving with ps-architect to evaluate three options for Jerry work item persistence.

Options:
A. YAML files (one file per work item, filesystem-native)
B. SQLite (single file, queryable, requires library dependency)
C. Event store with JSON snapshots (append-only log, full history, snapshot every 10 events)

Evaluation dimensions: read latency, write simplicity, corruption recovery, cross-session portability.

Context: Jerry is a CLI tool with no server process; storage must work without infrastructure setup.

Output: projects/PROJ-007/decisions/ADR-001-persistence-strategy.md in Nygard ADR format.
```

### Annotated Anatomy

```
Use /problem-solving with ps-architect ...
└─ ps-architect routes to Opus model tier. Use HIGH-LEVEL goal statements, not prescriptive steps.
   ps-architect knows the Nygard ADR format, C4 model, and DDD patterns natively.

Options: A. ..., B. ..., C. ...
└─ Explicit options trigger Decision Analysis mode (Type 6 taxonomy).
   Without named options, ps-architect invents the option set — introducing arbitrary framing.

Evaluation dimensions: ...
└─ Named dimensions prevent ps-architect from weighting criteria arbitrarily.
   3–4 dimensions is ideal. More than 5 dilutes the analysis.

Output: ... in Nygard ADR format.
└─ "Nygard ADR format" = Title, Status, Context, Decision, Consequences.
   Always include this. Without it, output structure varies per run.
```

### Expected Output

An ADR document with:
- **Title and Status** (Proposed / Accepted / Deprecated)
- **Context** — The problem being solved
- **Decision** — The chosen option with rationale
- **Consequences** — Trade-offs, future constraints, action items

---

## Template 5: Bug Investigation

### Purpose

Use ps-investigator to find the root cause of a failure using convergent, hypothesis-driven reasoning. Produces a root-cause analysis report with a specific finding, not a survey.

### When to Use

- Something is failing and you need to know *why*, not a landscape of possibilities
- Root cause investigation mode (convergent) is needed, not broad research (divergent)
- You have a named artifact, log, or symptom to investigate

### Template Text

```
Use /problem-solving with ps-investigator to determine the root cause of {{FAILURE_DESCRIPTION}}.
Apply the 5 Whys methodology.

Domain: {{DOMAIN}} at {{FILE_OR_LOG_PATH}}.
Symptoms: {{SYMPTOM_1}}, {{SYMPTOM_2}}.
Known non-causes (already ruled out): {{RULED_OUT_CAUSES}}.

Output: projects/{{PROJECT_ID}}/investigations/{{OUTPUT_FILENAME}} with:
- Root cause statement (one sentence)
- Evidence chain (5 Whys trace)
- Recommended fix
- Confidence level (high/medium/low)
```

### Filled Example

```
Use /problem-solving with ps-investigator to determine the root cause of
authentication token validation failures in the inventory service.
Apply the 5 Whys methodology.

Domain: authentication-service in src/Delinea.Inventory.Logic/Handlers/
         specifically AuthTokenValidationHandler.cs.
Symptoms: 401 responses on valid tokens, intermittent (not consistent), only affects tokens
          issued more than 5 minutes ago.
Known non-causes (already ruled out): clock skew (NTP confirmed synchronized),
                                       signing key rotation (no rotation in past 30 days).

Output: projects/PROJ-007/investigations/auth-token-failure-root-cause.md with:
- Root cause statement (one sentence)
- Evidence chain (5 Whys trace)
- Recommended fix with code location
- Confidence level (high/medium/low)
```

### Annotated Anatomy

```
Use /problem-solving with ps-investigator ...
│                    │
│                    └─ ps-investigator vs. ps-researcher
│                       ps-investigator = CONVERGENT. Uses 5 Whys, Ishikawa.
│                       Produces: one root cause, one finding.
│                       ps-researcher = DIVERGENT. Uses 5W1H.
│                       Produces: a survey of many things.
│                       Never use ps-researcher for "why is X failing" — it will survey
│                       the failure landscape instead of drilling to the cause.
│
Apply the 5 Whys methodology.
└─ Names the investigation framework explicitly. ps-investigator also knows Ishikawa (fishbone).
   "5 Whys" is correct when you have a single known failure to trace back to a root cause.

Symptoms: {{SYMPTOM_1}}, {{SYMPTOM_2}}.
└─ Give ps-investigator concrete, observable symptoms — not guesses about the cause.
   Symptoms are what you CAN observe. Root cause is what you are ASKING Claude to find.

Known non-causes (already ruled out): {{RULED_OUT_CAUSES}}.
└─ Telling ps-investigator what has already been ruled out prevents it from re-investigating
   the same dead ends. This is context-efficient (C3) and narrows the investigation.

Output: ... with Root cause statement ... Evidence chain ... Recommended fix ... Confidence level
└─ Four explicit output sub-sections. Each is concrete and verifiable.
   "Confidence level" keeps ps-investigator honest — it flags when evidence is thin.
```

### Expected Output

A root-cause analysis report with:
- A single root cause statement (one clear sentence)
- A 5 Whys evidence chain tracing from symptom to root cause
- A specific recommended fix with file path and code-level guidance
- A confidence level assessment with reasoning

---

## Template Quick-Select Guide

```
Is the task open-ended exploration of a topic you do not yet understand?
  YES → Template 1: Research Spike

Is the task writing, reviewing, or validating a single concrete artifact?
  YES → Template 2: Implementation Task

Does the task require research → analysis → decision (3+ phases) with quality gates?
  YES → Template 3: Multi-Skill Orchestration

Do you have 2+ options to compare with named evaluation dimensions?
  YES → Template 4: Architecture Decision

Do you have a specific failure to trace back to a root cause?
  YES → Template 5: Bug Investigation

None of the above?
  → Start with Template 2 (Implementation Task) and add phases as needed.
     Templates 1 and 2 are the building blocks for Templates 3, 4, and 5.
```

---

## Rubric Scores for Each Template

Templates are pre-scored against the 7-criterion quality rubric. A correctly filled template with specific placeholders will achieve the stated tier.

| Template | Expected Tier | Expected Score | Weakest Criterion | How to Reach Tier 4 |
|----------|--------------|----------------|-------------------|---------------------|
| T1: Research Spike | Tier 3–4 (Proficient-Exemplary) | ~88/100 | C5: single-phase (no decomposition needed) | Already near Tier 4 with quality threshold included |
| T2: Implementation Task | Tier 3–4 (Proficient-Exemplary) | ~87/100 | C5: single-phase (no decomposition needed) | Already at Tier 4 if output path is fully specified |
| T3: Multi-Skill Orchestration | Tier 4 (Exemplary) | ~94/100 | None — all 5 elements present | Already at Tier 4 |
| T4: Architecture Decision | Tier 4 (Exemplary) | ~91/100 | C5: single-phase | Already at Tier 4; add context file reference for C3 |
| T5: Bug Investigation | Tier 3–4 (Proficient-Exemplary) | ~88/100 | C4: no circuit-breaker threshold | Add `Quality threshold: >= 0.88` to activate ps-critic |

---

*Document Version: 1.0.0*
*Agent: ps-reporter*
*Constitutional Compliance: P-001 (all claims trace to PROJ-006-SYN-001, PROJ-006-ARCH-001, PROJ-006-ANA-001), P-002 (persisted), P-003 (no subagents), P-022 (limitations noted)*
*Created: 2026-02-18*
