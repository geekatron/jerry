# Writing Effective Jerry Prompts

> The 5 elements that matter, the rubric to score them, and the anti-patterns to avoid.

## Document Sections

| Section | Purpose |
|---------|---------|
| [The 5 Elements](#the-5-elements-of-an-effective-jerry-prompt) | What every good prompt includes |
| [The Quality Rubric](#the-quality-rubric) | 7 criteria to score any prompt (0-100) |
| [The Adversarial Critique Loop](#the-adversarial-critique-loop) | The single highest-impact quality pattern |
| [Agent Selection](#agent-selection) | Matching agents to cognitive modes |
| [Anti-Patterns](#anti-patterns) | The 8 most common prompt failures |
| [Pre-Submission Checklist](#pre-submission-checklist) | 10 checks before you hit Enter |

---

## The 5 Elements of an Effective Jerry Prompt

Every effective Jerry prompt shares these five structural elements. Each maps to a specific Jerry mechanism — missing any one forces Claude to make a decision you should have made.

```
1. SKILL ROUTING     Use /problem-solving with ps-[agent]
2. SCOPE             Domain: X. Time: YYYY-MM-DD to YYYY-MM-DD.
3. DATA SOURCE       Data source: [named tool, MCP, or file path]
4. QUALITY GATE      Include ps-critic adversarial critique. Threshold: >= 0.90.
5. OUTPUT PATH       Output: projects/PROJ-NNN/[path/to/artifact.md] with [format]
```

### How Each Element Maps to Jerry

| Element | Jerry Mechanism | What Happens When Missing |
|---------|----------------|---------------------------|
| `/skill` routing | YAML activation-keywords load agent context | Entire framework bypassed; plain conversational response |
| Domain scope | Agent research scoping | Hallucinated or too-broad findings |
| Data source | MCP tool selection | Agent infers or hallucinates source |
| Quality threshold | ps-critic circuit breaker | Default 0.85 or no critique at all |
| Output path | Mandatory Persistence Protocol | Artifacts at unpredictable default paths |

### The Golden Rule

Every missing element forces Claude to make a structural decision you probably should have made. Missing quality threshold → ps-critic uses 0.85. Missing output path → artifacts go to default locations. Missing data source → agent infers or hallucinates the source.

---

## The Quality Rubric

Score each criterion 0-3. Multiply by weight. Sum for total (0-100).

| # | Criterion | Weight | Score 3 (Full) | Score 0 (Absent) |
|---|-----------|--------|----------------|------------------|
| **C1** | **Task Specificity** | **20%** | Zero undefined terms, trailing fragments, or missing constraints | 5+ gaps or no actionable task |
| **C2** | **Skill Routing** | **18%** | All skills with `/skill` syntax; agent names used | No routing signals |
| **C3** | **Context Provision** | **15%** | Necessary context present; no redundant padding | No useful context |
| **C4** | **Quality Specification** | **15%** | Numeric threshold + named review mechanism | No quality signal |
| **C5** | **Decomposition** | **12%** | 2+ named phases/agents/sync barriers | Complex task as monolithic blob |
| **C6** | **Output Specification** | **12%** | Type + file path + format all present | Nothing specified |
| **C7** | **Positive Framing** | **8%** | Zero negative instructions | Mostly prohibitions |

**Scoring formula:** `total = sum( (raw_score_N / 3) * weight_N * 100 )`

### The 4 Effectiveness Tiers

| Score | Tier | What Happens |
|-------|------|-------------|
| **90-100** | **Exemplary** | Completes without clarification. Artifacts at correct paths. Quality gates fire at your threshold. |
| **75-89** | **Proficient** | Functionally correct. Artifacts may land at default paths. Minor clarification may be needed. |
| **50-74** | **Developing** | Primary task completes. Structural decisions made by Claude, not you. Multiple back-and-forth turns. |
| **0-49** | **Inadequate** | Requires significant clarification or produces wrong output. |

### Quick Scoring

Check C1, C2, C4, C6 first — they account for **65% of the total score**:

1. Count specificity gaps (C1) — 30 seconds
2. Check for `/skill` syntax and agent names (C2) — 10 seconds
3. Check for numeric threshold or ps-critic request (C4) — 5 seconds
4. Check for explicit output path (C6) — 5 seconds

Fix these four first. The remaining 35% (C3, C5, C7) fine-tunes the result.

---

## The Adversarial Critique Loop

**This is the single highest-impact quality pattern in Jerry — and the most underused.**

The Adversarial Critique Loop (Pattern P-07) only fires when explicitly requested. Without it, no critique runs at all — not even at the default threshold.

### How to Invoke

Add these two lines to any prompt:

```
Include ps-critic adversarial critique after each phase.
Quality threshold: >= 0.90.
```

### How It Works

```
Phase Output
    │
    ▼
ADVERSARIAL CRITIQUE (ps-critic)
  ├── Devil's Advocate: Challenge core assumptions
  ├── Steelman: Find strongest counter-arguments
  ├── Red Team: Attack for vulnerabilities and gaps
  └── Blue Team: Defend and validate strongest points
    │
    ▼
CIRCUIT BREAKER CHECK
  ├── quality_score >= threshold → proceed to next phase
  ├── quality_score < threshold, iterations < 3 → revise and re-critique
  └── 3 iterations with no improvement → stop regardless
```

### Threshold Selection

| Task Type | Recommended Threshold |
|-----------|-----------------------|
| Exploratory research / first drafts | 0.80-0.85 |
| Code review / validation | 0.85-0.90 |
| Architecture decisions (ADRs) | 0.90-0.92 |
| Security analysis | 0.92-0.95 |
| Status reports / summaries | 0.75-0.80 |

---

## Agent Selection

| Task Type | Agent | Model Tier | Cognitive Mode |
|-----------|-------|------------|----------------|
| Survey / landscape research | ps-researcher | Opus | Divergent (5W1H) |
| Root cause investigation | ps-investigator | Sonnet | Convergent (5 Whys) |
| Structured trade-off analysis | ps-analyst | Sonnet | Analytical (FMEA) |
| Cross-document synthesis | ps-synthesizer | Sonnet | Integrative |
| Architecture decision (ADR) | ps-architect | Opus | Decision (Nygard ADR) |
| Code / design review | ps-reviewer | Sonnet | Evaluative (SOLID, OWASP) |
| Binary pass/fail validation | ps-validator | Haiku | Verification |
| Status / metrics report | ps-reporter | Haiku | Aggregative |
| Quality scoring with critique | ps-critic | Sonnet | Adversarial (4 modes) |

### Prompt Calibration by Model Tier

- **Opus agents** (ps-researcher, ps-architect): Use high-level goal directives. "Think deeply about the task" outperforms step-by-step prescriptive instructions.
- **Haiku agents** (ps-validator, ps-reporter): Be maximally explicit and structured. Tightly defined output formats produce better results.
- **Sonnet agents** (all others): Balanced — structured criteria and named frameworks improve output without micromanaging.

### Common Mismatch

"Research why X is failing" routes to ps-researcher (divergent survey), but you probably want ps-investigator (convergent root cause). Use "investigate" or "determine the root cause of" for failures. Use "research" or "survey" for landscape exploration.

---

## Anti-Patterns

The 8 most common prompt failures, ordered by impact:

| # | Anti-Pattern | Impact | Fix |
|---|-------------|--------|-----|
| **AP-01** | Vague directives without `/skill` routing | Highest | Add `/problem-solving with ps-[agent]` |
| **AP-02** | Missing quality thresholds | High | Add `Quality threshold: >= 0.90` |
| **AP-03** | Monolithic prompts without decomposition | High | Break into named phases; use `/orchestration` |
| **AP-04** | Cognitive mode mismatch (research vs. investigate) | Medium | Match agent to cognitive mode needed |
| **AP-05** | Context overload (inline background instead of file refs) | Medium | Reference files by path: `Context: see projects/PROJ-006/research/...` |
| **AP-06** | Incomplete clause specification (trailing fragments) | Medium | Complete every sentence; no "as well as focus on the patterns of the" |
| **AP-07** | Conflicting instructions (P-003 violations) | Medium | Use orch-planner barrier-sync, not subagent spawning |
| **AP-08** | Missing output specification | Medium | Add `Output: path/to/artifact.md with [format]` |

---

## Pre-Submission Checklist

Work through these 10 checks before submitting a prompt. Each "no" is a fixable gap.

```
SPECIFICITY
[ ] Are all clauses grammatically and semantically complete? (no trailing fragments)
[ ] Are all vague descriptors replaced with concrete referents?

SKILL ROUTING
[ ] Does each needed skill appear with /slash-command syntax?
[ ] Is the specific agent named when a multi-agent workflow is intended?

CONTEXT
[ ] Is the data source named? (not "the CRM" but "Salesforce MCP")
[ ] Is the domain scope specified? (file path, project ID, or subject area)
[ ] Is any time range relevant? If yes, is it stated?

QUALITY
[ ] Is a numeric quality threshold present for consequential work?
[ ] Is ps-critic adversarial critique explicitly requested?

OUTPUT
[ ] Is the output file path, format, and structure (or template) specified?
```

---

## Related Resources

- [Prompt Templates](prompt-templates.md) — 5 copy-paste templates for common tasks
- [Getting Started](getting-started.md) — First-time Jerry setup and invocation
- [Problem-Solving Playbook](../playbooks/problem-solving.md) — Agent reference and keyword routing
- [PROJ-006 Research](../../projects/PROJ-006-jerry-prompt/) — Full research backing this guide

*Derived from PROJ-006-jerry-prompt research (2026-02-18). Findings validated through 3-phase orchestration with adversarial critic gates (0.934, 0.933, 0.930 >= 0.920).*
