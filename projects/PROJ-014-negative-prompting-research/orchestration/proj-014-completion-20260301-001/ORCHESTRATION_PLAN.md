# ORCHESTRATION_PLAN.md — PROJ-014 Completion

> **Workflow ID:** `proj-014-completion-20260301-001`
> **Parent Workflow:** `neg-prompting-20260227-001` (Phases 1-6 research, FEAT-001/002/003/004 implementation)
> **Project:** PROJ-014 Negative Prompting Research
> **Criticality:** C4 (Critical)
> **Quality Threshold:** >= 0.95
> **Created:** 2026-03-01

## Document Sections

| Section | Purpose |
|---------|---------|
| [Context](#context) | What has been completed and what remains |
| [Workflow Diagram](#workflow-diagram) | Visual execution sequence |
| [Behavioral Constraints](#behavioral-constraints) | FA-01 through FA-08 NPT-013 constraints |
| [C4 Gate Protocol](#c4-gate-protocol) | Quality gate execution pattern |
| [Step Definitions](#step-definitions) | Detailed step specifications |
| [Gate Inventory](#gate-inventory) | All 10 C4 gates |
| [Verification Criteria](#verification-criteria) | Completion checklist |

---

## Context

PROJ-014 Negative Prompting Research has completed:
- **Phases 1-6**: Full research pipeline (academic survey, industry survey, Context7 research, claim validation, comparative analysis, taxonomy, Jerry application analysis, ADR creation, final synthesis)
- **FEAT-001** (ADR-001): NPT-014 Elimination -- all 47 NPT-014 instances upgraded
- **FEAT-002** partial: Constitutional triplet format established, guardrails template updated (TASK-033, TASK-034 DONE)
- **FEAT-003** partial: Routing disambiguation sections added to all 13 skills (TASK-036 DONE)
- **FEAT-004** (ADR-004): Compaction Resilience -- L2-REINJECT markers for H-04 and H-32
- **TASK-025**: A/B Testing -- CONDITIONAL GO via PG-003 (p=0.016, C3=100%, C4 gate 0.954)

Parent workflow artifacts: `orchestration/neg-prompting-20260227-001/`. Key source documents: `orchestration/neg-prompting-20260227-001/phase-6/final-synthesis.md` (research findings), `orchestration/neg-prompting-20260227-001/ab-testing/ab-testing-synthesis.md` (A/B test results).

**Remaining work (this workflow):**
- TASK-035 (FEAT-002): NPT-013 constitutional triplet in 12 existing SKILL.md files
- TASK-037 (FEAT-003): Framing vocabulary standardization in 12 existing SKILL.md files
- FEAT-005 (EPIC-005): Create `/prompt-engineering` interactive skill
- TASK-026, TASK-027, TASK-028, TASK-029 (EPIC-006): Publication articles

---

## Workflow Diagram

```
Step 0: Scaffolding + C4 Gate on Plan
    |
    v
Step 1: TASK-035 NPT-013 Constitutional Triplet (12 SKILL.md)
    |  [sequential -- same files as Step 2]
    v
Step 2: TASK-037 Vocabulary Standardization (12 SKILL.md)
    |  [commit checkpoint]
    v
Step 3: FEAT-005 /prompt-engineering Skill Creation
    |  [SKILL.md -> agents -> NPT ref -> registration]
    |  [commit checkpoint]
    v
Step 4: Publication Fan-Out
    |
    +---> TASK-026: Jerry Docs Article (draft -> sb-rewriter -> gate)
    +---> TASK-027: Medium Article (draft -> sb-rewriter -> gate)
    +---> TASK-029: Slack Announcement (draft -> sb-rewriter -> gate)
    |
    v  [fan-in barrier: all 3 articles complete]
Step 5: TASK-028 Tweet + Cross-Post
    |
    v
Step 6: Finalize PROJ-014
```

---

## Behavioral Constraints

All orchestration execution is governed by 8 NPT-013 behavioral constraints:

| ID | Constraint | Consequence of Violation |
|----|-----------|--------------------------|
| FA-01 | NEVER allow an upstream creator to proceed without launching C4 gate | Low-quality artifacts propagate unchecked |
| FA-02 | NEVER proceed unless adversary quality score >= 0.95 | Sub-threshold work accepted, violating H-13 C4 |
| FA-03 | NEVER use unbounded iterations | Infinite loops consuming tokens; max 5 per gate |
| FA-04 | NEVER leave adversary feedback unaddressed | Revision cycle is cosmetic |
| FA-05 | NEVER use one agent for all adversary strategies | Confirmation bias in scoring |
| FA-06 | NEVER use /adversary only at the end | Error propagation through ungated steps |
| FA-07 | NEVER allow low-quality creator outputs downstream | Downstream tasks build on defective inputs |
| FA-08 | NEVER address feedback in the main context window | Anchoring bias from prior reasoning |

---

## C4 Gate Protocol

Applied per FA-01 through FA-08 at every creator output:

```
Creator (fresh Task agent) --> writes artifact
  |
Scorer (fresh background Task: adv-scorer) --> scores artifact
  |  6 dimensions: Completeness (0.20), Internal Consistency (0.20),
  |  Methodological Rigor (0.20), Evidence Quality (0.15),
  |  Actionability (0.15), Traceability (0.10)
  |
  | PASS (>= 0.95) --> proceed to next step
  | REVISE (0.85-0.94) --> Revision agent (fresh Task) --> re-score
  | REJECTED (< 0.85) --> Revision loop, may need multiple iterations
  |
  Max 5 iterations (FA-03), then user-accepted with documented score
```

**FA-05 enforcement**: Every scorer/executor is a separate fresh Task agent.
**FA-08 enforcement**: Revisions done by fresh Task agent, not main context.

**Strategy application per step type:**
- Steps 1-2 (SKILL.md edits): S-014 (LLM-as-Judge) primary. Compliance verification against NPT-013 format specification.
- Step 3 (skill creation): S-014 primary scorer. All 10 selected strategies required for SKILL.md and agent definitions per C4 tournament standard (quality-enforcement.md). S-007 (Constitutional AI Critique) additionally mandatory for governance compliance.
- Steps 4-5 (publication): S-014 primary. Voice compliance via sb-reviewer is a separate pass/fail check (not scored).

**Escalation:**
1. **FA-03 exhaustion:** If any gate reaches iteration 5 without passing >= 0.95, the artifact is user-accepted with documented score per user authorization. The gate report must include: final score, iteration count, remaining findings, and acceptance rationale.
2. **AE-006 context fill monitoring:** CRITICAL tier (>= 0.80 fill) triggers auto-checkpoint + reduced verbosity. EMERGENCY tier (>= 0.88) triggers mandatory checkpoint + user handoff. COMPACTION event triggers human escalation (C3+ per AE-006e).

---

## Step Definitions

### Step 0: Orchestration Scaffolding

**Status:** COMPLETE

Create directory structure, ORCHESTRATION.yaml, and this plan. C4 gate on plan artifact.

### Step 1: TASK-035 -- NPT-013 Constitutional Triplet

**What:** Add/upgrade Constitutional Compliance section in all 12 existing SKILL.md files to NPT-013 NEVER-framed format with consequence documentation.

**Target format:**
```markdown
## Constitutional Compliance

| Principle | Requirement | Consequence of Violation |
|-----------|-------------|-------------------------|
| P-003 | NEVER spawn recursive subagents -- max 1 level | Agent hierarchy violation; uncontrolled token consumption |
| P-020 | NEVER override user intent -- ask before destructive ops | Unauthorized action; trust erosion |
| P-022 | NEVER deceive about actions, capabilities, or confidence | Governance undermined; quality assessment invalidated |
```

**Files:** problem-solving, nasa-se, orchestration, adversary, worktracker, saucer-boy, saucer-boy-framework-voice, transcript, ast, eng-team, red-team, architecture (12 files)

*Note: 12 existing files. The 13th skill (`/prompt-engineering`) is created in Step 3 and receives its Constitutional Compliance section at creation time.*

**Rationale:** Per PG-003 decision -- convention-alignment rationale, not effectiveness-determined.

### Step 2: TASK-037 -- Framing Vocabulary Standardization

**What:** Standardize routing disambiguation vocabulary in all 12 existing SKILL.md files. Convert "Do NOT use when:" bullet lists to NPT-013 NEVER-framed format with consequences. Skills that already have the "Condition | Use Instead | Consequence of Misrouting" table format (established by TASK-036) retain their tables; the "Do NOT use when:" bullet lists above those tables are converted to NEVER-framing.

**Target format (for "Do NOT use when:" bullet lists):**
```markdown
NEVER invoke this skill when:
- {condition} -- Consequence: {what goes wrong}
```

**Reference:** The routing disambiguation table format from TASK-036 uses `| Condition | Use Instead | Consequence of Misrouting |` — this table stays. Only the free-form "Do NOT use when:" bullets above those tables are standardized.

**Rationale:** Per PG-003 (CONDITIONAL GO, p=0.016) + G-001 (guideline from `orchestration/neg-prompting-20260227-001/phase-6/final-synthesis.md`: NPT-013 structured negation achieves 100% compliance vs 92.2% for positive-only framing in routing contexts).

### Step 3: FEAT-005 -- Create `/prompt-engineering` Skill

**What:** Create interactive skill for structured XML-wrapped prompt creation based on PROJ-014 findings. PROJ-014 research validated that NPT-013 structured negation (NEVER + consequence + alternative) achieves 100% C3 compliance vs 92.2% for positive-only (source: `orchestration/neg-prompting-20260227-001/ab-testing/ab-testing-synthesis.md`). This knowledge is operationalized into a reusable tool.

**Worktracker entities (created at start of Step 3):**

*Note: FEAT-005 is the parent Feature entity for TASK-041 through TASK-044.*

*Note: EPIC-005 ('ADR Implementation') is an existing worktracker entity already IN PROGRESS. FEAT-005 is added as a new child Feature under EPIC-005. No new Epic creation required.*

- FEAT-005: Create `/prompt-engineering` Interactive Skill (parent: EPIC-005)
- TASK-041: Create SKILL.md and skill directory structure
- TASK-042: Create 3 agent definitions with governance YAML
- TASK-043: Create NPT pattern reference table
- TASK-044: Register skill in CLAUDE.md, AGENTS.md, and trigger map

**Artifacts:**
- `skills/prompt-engineering/SKILL.md` (TASK-041)
- `skills/prompt-engineering/agents/pe-builder.md` + `.governance.yaml` (TASK-042)
- `skills/prompt-engineering/agents/pe-constraint-gen.md` + `.governance.yaml` (TASK-042)
- `skills/prompt-engineering/agents/pe-scorer.md` + `.governance.yaml` (TASK-042)
- `skills/prompt-engineering/rules/npt-pattern-reference.md` (TASK-043)

**Registration (TASK-044):** CLAUDE.md skill table, AGENTS.md registry, mandatory-skill-usage.md trigger map. Trigger keywords: "build prompt", "create prompt", "prompt template", "NPT pattern", "constraint generation", "prompt quality", "score prompt".

### Step 4: Publication Fan-Out

Three independent articles, each following: draft -> sb-rewriter voice transform -> sb-reviewer + adv-scorer gates.

- **TASK-026:** Jerry MD Docs Site Article — Research findings narrative, NPT taxonomy overview, A/B test results (p=0.016), implementation guide for framework authors, link to `/prompt-engineering` skill. Target: ~1500-2000 words (5 sections: Introduction, Research Findings, NPT Taxonomy, A/B Test Results, Implementation Guide)
- **TASK-027:** Medium Article — Broader audience narrative, key findings (NPT-013 100% vs positive-only 92.2%), practical recommendations for LLM prompt engineers, link to Jerry docs article. Target: ~1200-1500 words (narrative format for broader audience)
- **TASK-029:** Slack Announcement — Brief announcement with key findings summary, links to TASK-026 and TASK-027 articles. Target: ~200-300 words

**Adversary strategies per article gate:** S-014 (LLM-as-Judge) primary scoring. Voice compliance via sb-reviewer is a separate check (pass/fail, not scored).

**Voice profile:** Saucer Boy persona loaded from `skills/saucer-boy/rules/biographical-anchors.md` and `skills/saucer-boy/rules/persona-voice-mapping.md`. sb-rewriter applies McConkey voice; sb-reviewer validates against 5 Authenticity Tests.

### Step 5: TASK-028 -- Tweet + Cross-Post

Fan-in barrier: depends on TASK-026, TASK-027, and TASK-029 completion for cross-linking. Tweet references article URLs from TASK-026 and TASK-027.

**Tweet specification:** <= 280 characters, reference TASK-026 Jerry Docs article URL and TASK-027 Medium article URL. Suggested hashtags: #PromptEngineering #LLM #AIGovernance. Cross-post targets: Jerry community Slack channel, X/Twitter.

### Step 6: Finalize PROJ-014

**Artifacts updated:**
- `WORKTRACKER.md`: All remaining tasks to DONE, EPIC-005 to DONE, EPIC-006 to DONE, PROJ-014 status to COMPLETE
- `ORCHESTRATION.yaml` (completion workflow): status to COMPLETE, all step statuses to COMPLETE, final metrics populated
- `ORCHESTRATION.yaml` (parent workflow `neg-prompting-20260227-001`): status to COMPLETE

Confirm EPIC-005 ("ADR Implementation") completion status -- if all child Features (FEAT-001 through FEAT-005) are DONE, update EPIC-005 to DONE.

**Escalation path for below-threshold artifacts:** If any gate fails to reach 0.95 after 5 iterations (FA-03), the artifact is accepted with documented score per user authorization. The gate report documents: final score, iteration count, remaining findings, and user acceptance rationale.

---

## Gate Inventory

| # | Step | Task ID | Artifact | Gate Report |
|---|------|---------|----------|-------------|
| 1 | 0 | — | ORCHESTRATION_PLAN.md | `adversary-gates/orchestration-plan-gate.md` |
| 2 | 1 | TASK-035 | TASK-035 (12 SKILL.md constitutional upgrades) | `adversary-gates/task-035-gate.md` |
| 3 | 2 | TASK-037 | TASK-037 (12 SKILL.md vocabulary standardization) | `adversary-gates/task-037-gate.md` |
| 4 | 3 | TASK-041 | SKILL.md for /prompt-engineering | `adversary-gates/feat-005-skill-gate.md` |
| 5 | 3 | TASK-042 | Agent definitions (3 agents + governance) | `adversary-gates/feat-005-agents-gate.md` |
| 6 | 3 | TASK-043 | NPT pattern reference table | `adversary-gates/feat-005-npt-ref-gate.md` |
| 7 | 4 | TASK-026 | Jerry Docs article (TASK-026) | `adversary-gates/task-026-gate.md` |
| 8 | 4 | TASK-027 | Medium article (TASK-027) | `adversary-gates/task-027-gate.md` |
| 9 | 4 | TASK-029 | Slack announcement (TASK-029) | `adversary-gates/task-029-gate.md` |
| 10 | 5 | TASK-028 | Tweet + cross-post (TASK-028) | `adversary-gates/task-028-gate.md` |

---

## Verification Criteria

1. All 12 existing SKILL.md files have NPT-013 constitutional triplet (TASK-035)
2. All 12 existing SKILL.md files have standardized routing disambiguation vocabulary (TASK-037)
3. `/prompt-engineering` skill created with SKILL.md, 3 agents, governance YAML, NPT reference
4. `/prompt-engineering` registered in CLAUDE.md, AGENTS.md, and mandatory-skill-usage.md trigger map
5. All 10 C4 gates pass >= 0.95 (FA-02) or user-accepted with documented score
6. All 4 articles pass sb-reviewer voice compliance check
7. All 4 articles written by sb-rewriter with Saucer Boy/McConkey voice
8. WORKTRACKER.md reflects PROJ-014 COMPLETE
9. Pre-commit hooks pass on every commit

---

*All paths relative to `projects/PROJ-014-negative-prompting-research/`*
