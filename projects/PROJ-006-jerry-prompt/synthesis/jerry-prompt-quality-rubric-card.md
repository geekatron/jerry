# Jerry Prompt Quality Rubric — Quick-Reference Card

> **Document ID:** PROJ-006-RPT-003
> **Agent:** ps-reporter (problem-solving skill)
> **Version:** 1.0.0
> **Date:** 2026-02-18
> **Status:** COMPLETE
> **Source:** PROJ-006-ARCH-001 (ps-architect, prompt-quality-rubric-taxonomy.md)

---

## The 7 Scoring Criteria

Score each criterion 0–3. Multiply by weight. Sum for total (0–100).

| # | Criterion | Weight | Score 3 (Full) | Score 2 (Partial) | Score 1 (Vague) | Score 0 (Absent) |
|---|-----------|--------|----------------|-------------------|-----------------|------------------|
| **C1** | **Task Specificity** | **20%** | Zero undefined terms, trailing fragments, or missing constraints | 1–2 specificity gaps; intent still clear | 3–4 gaps; inference required | 5+ gaps or no actionable task |
| **C2** | **Skill Routing** | **18%** | All needed skills invoked with `/skill` syntax; agent names used | At least one skill correct; one omitted or missing `/` | No `/` syntax; skills referenced by description only | No routing signals whatsoever |
| **C3** | **Context Provision** | **15%** | All necessary context present; no redundant padding | Minor gap or minor redundancy; task not blocked | Key context missing OR >40% of context is redundant | No useful context, or context so padded it obscures the task |
| **C4** | **Quality Specification** | **15%** | Numeric threshold (e.g., `>= 0.92`) AND named review mechanism (e.g., `ps-critic`) | Named mechanism only, no numeric threshold | Verbal descriptor only ("ensure accuracy") | No quality signal at all |
| **C5** | **Decomposition** | **12%** | 2+ named phases/agents/sync barriers enumerated | Exactly 1 named stage or agent pipeline | Sequence implied by conjunctions; no names | Complex task stated as monolithic blob |
| **C6** | **Output Specification** | **12%** | Output type + file path + structure (format/template) all present | Two of three specified | One of three specified ("write a report") | No artifact type, path, or format mentioned |
| **C7** | **Positive Framing** | **8%** | Zero negative instructions | 1–2 negatives for explicit guardrails | Negatives approach or match positives | Majority of instructions are prohibitions |

**Scoring formula:** `total = sum( (raw_score_N / 3) × weight_N × 100 )`

---

## The 4 Effectiveness Tiers

| Score | Tier | Label | What Jerry Does |
|-------|------|-------|-----------------|
| **90–100** | **4** | **Exemplary** | Completes without clarification. Artifacts written to correct paths. Quality gates fire at your threshold. Fully reproducible across sessions. |
| **75–89** | **3** | **Proficient** | Functionally correct. Artifacts may go to default paths (not your intended path). One clarification round may be needed. |
| **50–74** | **2** | **Developing** | Completes primary task. Structural decisions (paths, thresholds, phase order) made by Claude rather than you. Multiple back-and-forth turns. |
| **0–49** | **1** | **Inadequate** | Requires significant clarification or produces the wrong output entirely. Three likely outcomes: clarifying questions, generic response, or well-structured answer to the wrong task. |

---

## The 5 Elements of a Tier 4 Prompt

Every Tier 4 prompt has all five. Check them in this order:

```
1. SKILL ROUTING     Use /problem-solving with ps-[agent]
2. SCOPE             Domain: X. Time: YYYY-MM-DD to YYYY-MM-DD.
3. DATA SOURCE       Data source: [named tool, MCP, or path]
4. QUALITY GATE      Include ps-critic adversarial critique. Threshold: >= 0.90.
5. OUTPUT PATH       Output: projects/PROJ-NNN/[path/to/artifact.md] with [format]
```

---

## The 9 Problem-Solving Agents at a Glance

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

**Prompt calibration by model tier:**
- **Opus agents** (ps-researcher, ps-architect): Use high-level goal directives. Anthropic guidance: "Think deeply about the task" outperforms step-by-step prescriptive instructions for extended thinking.
- **Haiku agents** (ps-validator, ps-reporter): Be maximally explicit and structured. Tightly defined output formats produce better results.
- **Sonnet agents** (all others): Balanced — structured criteria and named frameworks improve output without micromanaging.

---

## The Adversarial Critique Loop (P-07)

The single highest-impact quality pattern in Jerry. **Only fires when explicitly requested.**

```
Invoke with:
  Include ps-critic adversarial critique after each phase.
  Quality threshold: >= [your threshold].

ps-critic applies 4 modes:
  1. Devil's Advocate — Challenges core assumptions
  2. Steelman        — Finds the strongest counter-arguments
  3. Red Team        — Attacks for vulnerabilities and gaps
  4. Blue Team       — Defends and validates strongest points

Circuit breaker stops when:
  quality_score >= acceptance_threshold  →  proceed to next phase
  iterations >= 3                         →  stop regardless
  two consecutive iterations, no improvement → stop

Default threshold if you omit it: 0.85
```

**Threshold selection guide:**

| Task Type | Recommended Threshold |
|-----------|-----------------------|
| Exploratory research / first drafts | 0.80–0.85 |
| Code review / validation | 0.85–0.90 |
| Architecture decisions (ADRs) | 0.90–0.92 |
| Security analysis | 0.92–0.95 |
| Status reports / summaries | 0.75–0.80 |

---

## The 6 Prompt Types

| Type | Description | Key Criteria |
|------|-------------|-------------|
| **Atomic Query** | Single factual answer; no persisted artifact | C1, C7 |
| **Implementation Task** | One skill, one deliverable | C1, C6, C4 |
| **Research Spike** | Open exploration via ps-researcher; L0/L1/L2 output | C1, C3, C6 |
| **Multi-Skill Orchestration** | Full pipeline; orch-planner; phase quality gates | C2, C4, C5, C6 |
| **Validation Gate** | Binary pass/fail against named criteria | C1, C4, C6 |
| **Decision Analysis** | 2+ options, named dimensions, ADR output | C1, C5, C6 |

---

## Before Submitting Your Prompt — Self-Check

Work through these 10 checks. Each "no" is a recoverable gap, not a failure.

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

**Scoring a prompt in under 2 minutes:**
1. Count specificity gaps (C1) — takes 30 seconds.
2. Check for `/skill` syntax and agent names (C2) — takes 10 seconds.
3. Check for numeric threshold or ps-critic request (C4) — takes 5 seconds.
4. Check for explicit output path (C6) — takes 5 seconds.

C1, C2, C4, and C6 together account for **65% of the total score**. Fix these four first.

---

*Rubric Card Version: 1.0.0*
*Source rubric: PROJ-006-ARCH-001 (ps-architect, 2026-02-18)*
*Agent: ps-reporter*
*Created: 2026-02-18*
