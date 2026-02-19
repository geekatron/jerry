# Prompt Templates for Jerry

> Copy-paste prompt templates for the most common Jerry tasks. Replace `{{PLACEHOLDERS}}` with your values before submitting.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Placeholder Reference](#placeholder-reference) | What each placeholder means |
| [Template Quick-Select](#template-quick-select) | Choose the right template |
| [Template 1: Research Spike](#template-1-research-spike) | Open-ended research investigation |
| [Template 2: Implementation Task](#template-2-implementation-task) | Single-skill code or artifact creation |
| [Template 3: Multi-Skill Orchestration](#template-3-multi-skill-orchestration) | Full pipeline with quality gates |
| [Template 4: Architecture Decision](#template-4-architecture-decision) | ADR production via ps-architect |
| [Template 5: Bug Investigation](#template-5-bug-investigation) | Root-cause analysis via ps-investigator |

---

## Placeholder Reference

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

**Minimum required:** `{{PROJECT_ID}}`, `{{DOMAIN}}`, `{{OUTPUT_PATH}}`.

---

## Template Quick-Select

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
  → Start with Template 2 and add phases as needed.
```

---

## Template 1: Research Spike

**Use when:** You need to explore a topic, gather data from a named source, or get a landscape overview before deeper analysis.

### Template

```
Use /worktracker to create a Spike titled "{{WORK_ITEM_TITLE}}" under {{PROJECT_ID}}.

Use /problem-solving with ps-researcher to survey {{DOMAIN}} from {{START_DATE}} to {{END_DATE}}.
Data source: {{DATA_SOURCE}}.
Focus areas: {{FOCUS_AREAS}}.
Output: projects/{{PROJECT_ID}}/research/{{OUTPUT_PATH}} with L0/L1/L2 sections.

Include ps-critic adversarial critique after the research phase.
Quality threshold: >= {{QUALITY_THRESHOLD}}.
```

### Example

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

---

## Template 2: Implementation Task

**Use when:** You need one deliverable from one Jerry skill — a code review, implementation, or analysis. No multi-phase pipeline needed.

### Template

```
Use /problem-solving with {{AGENT}} to {{TASK_DESCRIPTION}}.

Input artifact: {{FILE_PATH}}
Review/implementation dimensions:
- {{CRITERION_1}}
- {{CRITERION_2}}
- {{CRITERION_3}}

Output: projects/{{PROJECT_ID}}/{{OUTPUT_PATH}} with {{SEVERITY_OR_FORMAT}} per finding.
```

### Example — Code Review

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

---

## Template 3: Multi-Skill Orchestration

**Use when:** The task has 3+ phases, quality at phase boundaries matters, and you need reproducible results across sessions. This is the highest-quality Jerry prompt pattern.

### Template

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

### Example

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

---

## Template 4: Architecture Decision

**Use when:** You have 2+ viable implementation options and need a documented decision with rationale, trade-offs, and consequences.

### Template

```
Use /problem-solving with ps-architect to evaluate {{NUM_OPTIONS}} options for {{DECISION_SUBJECT}}.

Options:
A. {{OPTION_A_DESCRIPTION}}
B. {{OPTION_B_DESCRIPTION}}
C. {{OPTION_C_DESCRIPTION}} (if applicable)

Evaluation dimensions: {{DIMENSION_1}}, {{DIMENSION_2}}, {{DIMENSION_3}}.

Context: {{CONTEXT_FILE_PATH_OR_INLINE_CONTEXT}}

Output: projects/{{PROJECT_ID}}/decisions/{{ADR_FILENAME}} in Nygard ADR format.
```

### Example

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

---

## Template 5: Bug Investigation

**Use when:** Something is failing and you need to know *why* — not a landscape survey, but a specific root cause.

### Template

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

### Example

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

---

## Related Resources

- [Getting Started](getting-started.md) — First-time Jerry setup and invocation
- [Prompt Quality Guide](prompt-quality.md) — The 5-element anatomy, quality rubric, and anti-patterns
- [Problem-Solving Playbook](../playbooks/problem-solving.md) — Agent reference and keyword routing
- [PROJ-006 Research](../../projects/PROJ-006-jerry-prompt/) — Full research backing these templates

*Derived from PROJ-006-jerry-prompt research (2026-02-18). Templates validated against 7-criterion quality rubric.*
