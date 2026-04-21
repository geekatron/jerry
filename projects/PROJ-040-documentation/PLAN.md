# PLAN — PROJ-040 Documentation

> User-facing Jerry documentation. Consolidates PROJ-015 (audit) and PROJ-016 (writing). UX-driven discovery followed by Diataxis-pure production with C4 ≥ 0.95 adversarial quality gates.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Problem Statement](#problem-statement) | Why this project exists |
| [Scope](#scope) | What is in and out |
| [Approach](#approach) | Ordered execution model |
| [Orchestration Architecture](#orchestration-architecture) | How /orchestration coordinates waves |
| [Quality Protocol](#quality-protocol) | Gates applied per deliverable |
| [Epics](#epics) | Work decomposition |
| [Dependencies](#dependencies) | Ordering constraints |
| [Supersession](#supersession) | What this project replaces |
| [Related GitHub Issues](#related-github-issues) | External tracking |

---

## Problem Statement

The PROJ-040 Diataxis audit (2026-04-20, C4 approved at 0.956) confirms a worsening documentation trajectory:

- 30 skills and 88 agent files; zero skill-specific tutorials, zero skill-specific explanation docs, and only 4 partial (mixed-quadrant) how-to playbooks
- 16 skills added since the PROJ-015 baseline (2026-03-02) with zero user-facing documentation
- 10 of 10 PROJ-015 remediation items remain unresolved 49 days after the original audit
- Root `README.md` advertises 6 of 30 skills; `docs/index.md` advertises 7 of 30
- The only 4 Diataxis-passing documents created since PROJ-015 cover CI/CD supply chain and Claude Code permissions — not the skills themselves

Jerry is approaching OSS release with a documentation surface that does not represent what the framework actually is or does. Writing without a refreshed baseline risks the same drift PROJ-016 suffered. This project closes that gap.

---

## Scope

**In scope:**
- Refreshed Diataxis audit (complete; file: `reports/diataxis-audit-20260420.md`)
- UX-driven discovery via the full `/user-experience` agent wave (JTBD, HEART, Heuristic, Inclusive, Kano, Behavior-diagnostician, Lean UX, Atomic architect)
- Root `README.md` re-audit and revision (addresses GitHub #100)
- `docs/index.md` re-audit and revision
- Skill tutorials (new — all via `/diataxis` diataxis-tutorial)
- Skill how-to guides (new — all via diataxis-howto)
- Skill explanations (new — all via diataxis-explanation)
- External agent reference catalog (new — via diataxis-reference)
- Remediation of existing mixed-quadrant docs (INSTALLATION, BOOTSTRAP, CLAUDE-MD-GUIDE, getting-started, playbooks)
- Creation of `docs/tutorial/` and `docs/how-to/` directories
- Extraction of `docs/explanation/context-architecture.md` and `docs/explanation/hooks-architecture.md`

**Out of scope:**
- Internal `.context/rules/` files (not user-facing)
- Project-scoped docs under `projects/`
- Agent definition `.md` files (governed by `agent-development-standards.md`)
- Governance docs in `docs/governance/`
- Re-auditing (PROJ-040's own audit is the current baseline)

---

## Approach

Work executes in five waves. Each wave has entry and exit criteria; downstream waves do not start until upstream completes at quality gate.

### Wave 0 — Audit (complete)

Produce and validate the Diataxis audit that grounds all writing work.

**Exit criterion:** Audit approved at C4 ≥ 0.95 via adversarial tournament + scoring.
**Status:** COMPLETE (4 iterations, 0.956 composite, 0.959 tournament). Artifact: `reports/diataxis-audit-20260420.md`.

### Wave 1 — Discovery (Phase 0)

Apply a three-stream discovery protocol to the documentation surface before writing any docs. Deliverables inform downstream prioritization, success metrics, positioning, and information architecture. Coordinated by `/orchestration` with explicit sync barriers and a convergence gate.

**Stream 1 — UX (8 features via `/user-experience`):**

| Sub-skill | Purpose in this project |
|-----------|------------------------|
| `ux-jtbd-analyst` | Map jobs-to-be-done per skill (what is a user hiring `/orchestration` to do?) — informs which tutorials and how-tos to write first |
| `ux-heart-analyst` | Define Happiness, Engagement, Adoption, Retention, Task Success metrics for documentation; establish baselines where measurable |
| `ux-kano-analyst` | Classify documentation artifacts (must-be, performance, attractive) — drives L0/L1/L2 priority for each skill |
| `ux-behavior-diagnostician` | B=MAP analysis on "why do users not complete the getting-started tutorial?" |
| `ux-heuristic-evaluator` | Nielsen heuristic audit on rendered docs and README first-impression surface |
| `ux-inclusive-evaluator` | WCAG 2.2 + Persona Spectrum on rendered markdown (contrast, heading hierarchy, screen-reader nav) |
| `ux-lean-ux-facilitator` | Hypothesis-driven validation of docs decisions (e.g., "will naming the research subject in tutorials reduce first-run failure rate?") |
| `ux-atomic-architect` | Component taxonomy for reusable documentation patterns (callouts, code blocks, nav tables) |

**Stream 2 — Product / Market (3 features via `/pm-pmm`):**

| Sub-skill | Purpose in this project |
|-----------|------------------------|
| `pm-customer-insight` | Personas + journey maps for Jerry's users (new OSS user, contributor, integrator). Complements JTBD with persona-driven synthesis; journey map of "landing on README → first successful skill invocation" identifies friction points. |
| `pm-market-strategist` | Positioning + messaging framework for the first-impression surface. Directly feeds Wave 2 README revision with a positioning-grade answer to "what is Jerry?" |
| `pm-competitive-analyst` | Competitive documentation landscape: how do Claude Agent SDK, LangChain, LlamaIndex, AutoGen, CrewAI structure their docs? Which patterns are effective for OSS adoption? Prevents reinventing the wheel. |

**Stream 3 — Research (1 feature via `/problem-solving`):**

| Agent | Purpose in this project |
|-------|------------------------|
| `ps-researcher` | Docs best-practices research (Diataxis in production, OSS style guides, WRITE THE DOCS patterns). Parallel to pm-competitive — one is "what competitors do," the other is "what the field has learned." |

**Convergence gate (1 feature via `/problem-solving`):**

| Agent | Purpose in this project |
|-------|------------------------|
| `ps-synthesizer` | Synthesize 12 stream outputs into a single Discovery Synthesis document that feeds Waves 2-4 as typed input. Identifies convergent signals across UX, PM, and research streams. Ends Wave 1. |

**Exit criteria:**
- All 12 stream outputs produced and individually C3-reviewed (S-014 ≥ 0.90)
- Discovery Synthesis produced and C4-reviewed (S-014 ≥ 0.95)
- JTBD job statements for all 30 skills
- HEART metric specifications with baselines or targets
- Kano classification for each planned doc artifact
- Personas + journey map for primary user segments
- Positioning + messaging framework for README
- Competitive docs benchmark with adoption-tested patterns
- Research synthesis on Diataxis production use
- Heuristic evaluation of README + docs/index.md
- WCAG 2.2 compliance baseline for rendered docs

### Wave 2 — First-Impression Surface (addresses GitHub #100)

Revise root `README.md` and `docs/index.md` to reflect current Jerry state. Blocks OSS release.

**Exit criteria:**
- Every factual claim verified (per GitHub #100 AC requirements)
- Independent reviewer per #100 AC-6 (UX wave does NOT replace this)
- C4 ≥ 0.95 adversarial review pass
- Skills table accurate (30 skills, 88 agents)
- Claim-verification log attached

### Wave 3 — Existing Docs Remediation

Address PROJ-015 carry-forward and new audit findings for existing mixed-quadrant documents. Faster to fix than create.

**Deliverables:**
- Extract `docs/explanation/context-architecture.md` (from BOOTSTRAP + CLAUDE-MD-GUIDE)
- Extract `docs/explanation/hooks-architecture.md` (from INSTALLATION)
- Revise `docs/INSTALLATION.md` (remove marketing voice, update skills table to 30 skills, remove explanation blocks)
- Revise `docs/BOOTSTRAP.md` (remove explanation blocks, cross-reference new explanation docs)
- Revise `docs/CLAUDE-MD-GUIDE.md` (rename H1 to goal-framed, extract explanation)
- Revise `docs/runbooks/getting-started.md` (fix T-04 branching, update version references to v0.31.5)
- Revise 4 playbooks (extract embedded reference tables into a dedicated skills catalog)

**Exit criterion:** Each revised document passes its Diataxis quadrant criteria (H-01..H-07, T-01..T-10, R-01..R-07, or E-01..E-07 as applicable) and C4 ≥ 0.95 adversarial review.

### Wave 4 — New Documentation Production

Write missing tutorials, how-to guides, explanations, and the agent reference catalog.

| Sub-wave | Scope | Gate |
|----------|-------|------|
| 4a. Priority tutorials | Top skills identified by Kano (Wave 1) — minimum `/problem-solving`, `/worktracker`, `/orchestration` | C4 ≥ 0.95 per tutorial |
| 4b. Skill how-to guides | 26 skills lacking current how-to coverage | C4 ≥ 0.95 per guide |
| 4c. Skill explanations | Top 5-10 skills needing design-rationale docs | C4 ≥ 0.95 per explanation |
| 4d. Agent reference catalog | External-facing companion to `AGENTS.md` for 88 agents | C4 ≥ 0.95 |

### Wave 5 — Polish & Metadata

Diataxis quadrant metadata tags, navigation-table sweeps, final link validation, cross-reference validation.

---

## Orchestration Architecture

All waves after Wave 0 (audit) execute under `/orchestration` coordination. The main context acts as the sole orchestrator; subagents are scoped background workers that return artifact paths plus 3-5 key findings per CP-01 / CB-04. This preserves P-003 single-level nesting and keeps main-context token budget manageable as feature count scales (~55+ across the project).

### Per-wave planning cadence

Orchestration plans are designed *per wave*, not upfront. Each wave's plan consumes the predecessor wave's synthesis output as typed input.

| Wave | Orchestration plan artifact | Designed when |
|------|----------------------------|---------------|
| 1 | `orchestration/plans/wave-1-discovery-plan.md` | Before Wave 1 execution — inputs are the audit plus PLAN.md scope |
| 2 | `orchestration/plans/wave-2-first-impression-plan.md` | After Wave 1 Discovery Synthesis is C4-approved |
| 3 | `orchestration/plans/wave-3-remediation-plan.md` | After Wave 1 (needs Kano + JTBD for prioritization) |
| 4 | `orchestration/plans/wave-4-new-docs-plan.md` | After Wave 3 (existing docs must be Diataxis-clean before new docs cross-reference them) |
| 5 | `orchestration/plans/wave-5-polish-plan.md` | After Wave 4 |

Each plan is itself a C3+ deliverable and passes `/adversary` review (C3 ≥ 0.92 minimum; C4 ≥ 0.95 for Wave 1 plan since it grounds the entire project).

### Orchestration directory structure

```
projects/PROJ-040-documentation/orchestration/
  plans/            # Per-wave orchestration plans (orch-planner outputs)
  state/            # Phase state, feature lifecycle tracking (orch-tracker)
  checkpoints/      # Session-resumable snapshots (orch-tracker)
  reviews/          # /adversary outputs on each orchestration plan
```

### Main-context discipline

| Role | Actions |
|------|---------|
| Orchestrator (main context) | Reads the wave plan. Delegates to workers via the Agent tool. Reads worker returns (artifact path + key findings only). Synthesizes cross-worker state. Enforces quality gates. Invokes `/adversary` at phase boundaries. Updates `WORKTRACKER.md` status via `orch-tracker`. |
| Worker (every delegated subagent) | Executes in isolated context. Persists output to a typed file path under the project. Returns to orchestrator with the path plus 3-5 key findings. MUST NOT spawn sub-workers (P-003 / H-01). |
| State layer (`orch-tracker`) | Maintains `state/` and `checkpoints/`. Records feature lifecycle (pending → planning → in_progress → under_review → revising → complete) with quality scores. Writes to `WORKTRACKER.md` on status transitions. |
| Synthesis layer (`orch-synthesizer`) | Produces the wave-boundary synthesis artifact. Consumes worker outputs by reading artifact files; produces typed input for the next wave. |

### Handoff schema

Per NSE handoff standards + CP-01..CP-04, worker-to-orchestrator returns carry only:

- `artifact_path` (file path; orchestrator Reads on demand)
- `key_findings[]` (3-5 bullets)
- `blockers[]` (may be empty; persistent items prefixed `[PERSISTENT]`)
- `confidence` (0.0-1.0 self-assessed)
- `quality_score` (S-014 composite if self-scored)

No inline content. No full-document embedding. No redundant summarization.

### Quality gate enforcement

Every wave has phase-boundary quality gates. A wave does not exit (and its synthesis is not produced) until all per-feature gates pass at the wave-specific threshold:

| Wave | Per-feature threshold | Wave-boundary threshold |
|------|----------------------|------------------------|
| 1 | C3 ≥ 0.90 | C4 ≥ 0.95 (Discovery Synthesis) |
| 2 | C4 ≥ 0.95 (README is the project's face) | C4 ≥ 0.95 + independent reviewer per GH #100 AC-6 |
| 3 | C3 ≥ 0.92 per revised document | C4 ≥ 0.95 on remediation synthesis |
| 4 | C3 ≥ 0.92 per new document | C4 ≥ 0.95 on production synthesis |
| 5 | C2 ≥ 0.90 (polish-scale) | C3 ≥ 0.92 on polish synthesis |

Circuit breaker: max 6 iterations per deliverable with plateau detection (delta < 0.01 for 3 consecutive iterations triggers escalation to user per H-36).

### Cross-wave handoffs

Each wave produces exactly one synthesis artifact consumed by downstream waves:

- Wave 1 Discovery Synthesis → input to Waves 2, 3, 4 plans
- Wave 2 First-Impression Synthesis → input to Wave 4 (tutorials reference README)
- Wave 3 Remediation Synthesis → input to Wave 4 (new docs cross-reference revised docs)
- Wave 4 Production Synthesis → input to Wave 5

No wave re-derives inputs from predecessors. Synthesis artifacts are the single source of truth for downstream waves.

---

## Quality Protocol

Every deliverable in Waves 2-5 follows this protocol per H-13, H-14, H-17:

1. Author via `/diataxis` appropriate agent (tutorial, howto, reference, explanation)
2. Self-review (S-010) — author reviews own output
3. Adversarial critique via `ps-critic` (creator-critic-revision loop, minimum 3 iterations per H-14)
4. Adversarial tournament via `/adversary` adv-executor (all 10 strategies for C4 deliverables)
5. S-014 scoring via adv-scorer — composite must reach ≥ 0.95
6. Up to 6 revision iterations; circuit breaker on plateau (delta < 0.01 × 3) or ceiling breach
7. For Wave 2 README revision: additional independent reviewer per GitHub #100 AC-6

Feedback from each adversarial pass routes back to the original creator agent for revision.

---

## Epics

| ID | Title | Wave | Priority | Depends On |
|----|-------|------|----------|-----------|
| EPIC-040-000 | Diataxis Audit (complete) | 0 | -- | -- |
| EPIC-040-001 | UX Discovery | 1 | high | EPIC-040-000 |
| EPIC-040-002 | First-Impression Surface (README + docs/index.md) | 2 | high | EPIC-040-001 |
| EPIC-040-003 | Existing Docs Remediation | 3 | high | EPIC-040-001 |
| EPIC-040-004 | Skill Tutorials | 4a | high | EPIC-040-001, EPIC-040-003 |
| EPIC-040-005 | Skill How-To Guides | 4b | medium | EPIC-040-001, EPIC-040-003 |
| EPIC-040-006 | Skill Explanations | 4c | medium | EPIC-040-001, EPIC-040-003 |
| EPIC-040-007 | Agent Reference Catalog | 4d | medium | EPIC-040-001 |
| EPIC-040-008 | Polish & Metadata | 5 | low | EPIC-040-002..007 |

Feature decomposition lives under each epic in `work/EPIC-040-NNN-*/`. Features are enumerated in `WORKTRACKER.md`.

---

## Dependencies

- **Wave 1 blocks Waves 2-5.** UX discovery outputs (JTBD, Kano, HEART) directly feed prioritization and success criteria for all downstream writing.
- **Wave 2 can parallel Wave 3** once UX discovery is complete; they touch different documents.
- **Wave 4 requires Wave 3** — existing docs must be Diataxis-clean before new docs can cross-reference them without propagating quadrant mixing.
- **Agent reference catalog (EPIC-040-007) is independent** of the skill documentation epics; it can proceed in parallel to Wave 4a/b/c once Wave 1 completes.

---

## Supersession

PROJ-040 supersedes and consolidates:

| Predecessor | Status | Artifacts Preserved |
|-------------|--------|---------------------|
| [PROJ-015 documentation-audit](../PROJ-015-documentation-audit/) | SUPERSEDED 2026-04-20 | `reports/user-facing-docs-audit.md`, `reports/user-facing-docs-classification.md` retained as historical baseline |
| [PROJ-016 documentation-writing](../PROJ-016-documentation-writing/) | SUPERSEDED 2026-04-20 (no work started) | `WORKTRACKER.md` with 5 epics and 17 feature shells retained for selective re-porting |

Rationale: The PROJ-015 audit went stale (15 skills → 30 skills; 49 days and 177 commits without re-verification). PROJ-016 features were built on the stale baseline and would have produced drift if executed. The separation between audit and writing projects assumed audits complete; in practice, documentation is a continuous audit↔write loop that is better coordinated under a single project.

---

## Related GitHub Issues

| Issue | Title | Relationship |
|-------|-------|--------------|
| [#100](https://github.com/geekatron/jerry/issues/100) | Audit and update root README.md | Addressed by EPIC-040-002 |
| [#135](https://github.com/geekatron/jerry/issues/135) | PROJ-016 user-facing documentation writing | Superseded; PROJ-040 is the successor |
| [#175](https://github.com/geekatron/jerry/issues/175) | Documentation freshness detection | Informs Wave 5 metadata design |
| [#119](https://github.com/geekatron/jerry/issues/119) | Replace /tmp with tempfile.gettempdir() | Addressed in Wave 3 as applicable |
| [#115](https://github.com/geekatron/jerry/issues/115) | Document Windows symlink requirements | Addressed in Wave 3 INSTALLATION revision |
| [#265](https://github.com/geekatron/jerry/issues/265) | External agent reference catalog | Addressed by EPIC-040-007 |
