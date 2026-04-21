# WORKTRACKER — PROJ-040 Documentation

> **Project:** PROJ-040-documentation
> **Created:** 2026-04-20
> **Status:** Active
> **Baseline audit:** `reports/diataxis-audit-20260420.md` (C4 approved at 0.956, 4 iterations)
> **Supersedes:** PROJ-015-documentation-audit, PROJ-016-documentation-writing

## Document Sections

| Section | Purpose |
|---------|---------|
| [Epics](#epics) | Top-level work items |
| [Features](#features) | Feature breakdown by epic |
| [Supersession Carry-Forward](#supersession-carry-forward) | Items ported from predecessors |
| [Audit Traceability](#audit-traceability) | Maps epics to audit findings |

---

## Epics

| ID | Title | Status | Priority | Wave |
|----|-------|--------|----------|------|
| EPIC-040-000 | Diataxis Audit (2026-04-20) | Complete | -- | 0 |
| EPIC-040-001 | UX Discovery | Pending | high | 1 |
| EPIC-040-002 | First-Impression Surface (README + docs/index.md) | Pending | high | 2 |
| EPIC-040-003 | Existing Docs Remediation | Pending | high | 3 |
| EPIC-040-004 | Skill Tutorials | Pending | high | 4a |
| EPIC-040-005 | Skill How-To Guides | Pending | medium | 4b |
| EPIC-040-006 | Skill Explanations | Pending | medium | 4c |
| EPIC-040-007 | Agent Reference Catalog | Pending | medium | 4d |
| EPIC-040-008 | Polish & Metadata | Pending | low | 5 |

### Epic Links

- [EPIC-040-000: Diataxis Audit](./reports/diataxis-audit-20260420.md) — complete artifact (not decomposed into features)
- EPIC-040-001..008: epic folders to be created under `work/EPIC-040-NNN-*/` as each wave is initiated

---

## Features

### EPIC-040-001: Discovery (Wave 1)

Three-stream discovery (UX, PM, Research) with synthesis convergence gate. Coordinated by `/orchestration` per the wave-1 plan. 13 features total.

**Stream 1 — UX (8 features via `/user-experience`):**

| ID | Title | Parent | Status | Priority | Agent |
|----|-------|--------|--------|----------|-------|
| FEAT-040-001 | JTBD analysis for all 30 skills | EPIC-040-001 | Pending | high | ux-jtbd-analyst |
| FEAT-040-002 | HEART metrics specification for documentation | EPIC-040-001 | Pending | high | ux-heart-analyst |
| FEAT-040-003 | Kano classification of planned doc artifacts | EPIC-040-001 | Pending | high | ux-kano-analyst |
| FEAT-040-004 | Heuristic evaluation of README and docs/index.md | EPIC-040-001 | Pending | high | ux-heuristic-evaluator |
| FEAT-040-005 | WCAG 2.2 + Persona Spectrum audit of rendered docs | EPIC-040-001 | Pending | medium | ux-inclusive-evaluator |
| FEAT-040-006 | B=MAP diagnosis on getting-started tutorial completion | EPIC-040-001 | Pending | medium | ux-behavior-diagnostician |
| FEAT-040-007 | Lean UX hypothesis backlog for doc decisions | EPIC-040-001 | Pending | medium | ux-lean-ux-facilitator |
| FEAT-040-008 | Atomic component taxonomy for documentation patterns | EPIC-040-001 | Pending | low | ux-atomic-architect |

**Stream 2 — Product / Market (3 features via `/pm-pmm`):**

| ID | Title | Parent | Status | Priority | Agent |
|----|-------|--------|--------|----------|-------|
| FEAT-040-053 | Personas and journey maps for Jerry's user segments | EPIC-040-001 | Pending | high | pm-customer-insight |
| FEAT-040-054 | Positioning and messaging framework for first-impression surface | EPIC-040-001 | Pending | high | pm-market-strategist |
| FEAT-040-055 | Competitive documentation landscape benchmark (Claude Agent SDK, LangChain, LlamaIndex, AutoGen, CrewAI) | EPIC-040-001 | Pending | medium | pm-competitive-analyst |

**Stream 3 — Research (1 feature via `/problem-solving`):**

| ID | Title | Parent | Status | Priority | Agent |
|----|-------|--------|--------|----------|-------|
| FEAT-040-056 | OSS documentation best-practices research (Diataxis production use, style guides, WRITE THE DOCS patterns) | EPIC-040-001 | Pending | medium | ps-researcher |

**Convergence gate (1 feature via `/problem-solving`):**

| ID | Title | Parent | Status | Priority | Agent |
|----|-------|--------|--------|----------|-------|
| FEAT-040-057 | Discovery Synthesis — unify all 12 stream outputs into typed input for Waves 2-4 | EPIC-040-001 | Pending | high | ps-synthesizer |

**Wave 1 orchestration plan:**

| ID | Title | Parent | Status | Priority | Agent |
|----|-------|--------|--------|----------|-------|
| FEAT-040-058 | Wave 1 orchestration plan (sync barriers, cross-pollination, handoff schemas, state schema) | EPIC-040-001 | Pending | high | orch-planner |

### EPIC-040-002: First-Impression Surface

Addresses [GitHub #100](https://github.com/geekatron/jerry/issues/100). UX wave outputs feed these features; UX does NOT replace the independent reviewer requirement in #100 AC-6.

| ID | Title | Parent | Status | Priority | Input |
|----|-------|--------|--------|----------|-------|
| FEAT-040-009 | README.md audit and revision (factual accuracy + Diataxis) | EPIC-040-002 | Pending | high | FEAT-040-001..004 |
| FEAT-040-010 | docs/index.md revision aligned with new README | EPIC-040-002 | Pending | high | FEAT-040-009 |
| FEAT-040-011 | Claim-verification log per #100 AC requirements | EPIC-040-002 | Pending | high | FEAT-040-009 |
| FEAT-040-012 | Independent external reviewer pass per #100 AC-6 | EPIC-040-002 | Pending | high | FEAT-040-009, FEAT-040-010 |

### EPIC-040-003: Existing Docs Remediation

PROJ-015 carry-forward. All 10 items unresolved 49 days after original audit.

| ID | Title | Parent | Status | Priority | Diataxis Agent | Addresses |
|----|-------|--------|--------|----------|----------------|-----------|
| FEAT-040-013 | Extract docs/explanation/context-architecture.md | EPIC-040-003 | Pending | high | diataxis-explanation | Audit P2-1, PROJ-015 P1.2 |
| FEAT-040-014 | Extract docs/explanation/hooks-architecture.md | EPIC-040-003 | Pending | high | diataxis-explanation | Audit P2-2, PROJ-015 P1.3 |
| FEAT-040-015 | Revise docs/INSTALLATION.md (remove marketing, update skills table to 30, extract explanation) | EPIC-040-003 | Pending | high | diataxis-howto | Audit P1-2, P1-3, P2-4; PROJ-015 P1.4 |
| FEAT-040-016 | Revise docs/BOOTSTRAP.md (extract "How It Works" and "Why two directories?") | EPIC-040-003 | Pending | high | diataxis-howto | Audit P2-3; PROJ-015 P1.2 |
| FEAT-040-017 | Revise docs/CLAUDE-MD-GUIDE.md (goal-framed title, extract Context Architecture) | EPIC-040-003 | Pending | medium | diataxis-howto | Audit P3-5 |
| FEAT-040-018 | Revise docs/runbooks/getting-started.md (fix T-04 branching, update versions to v0.31.5) | EPIC-040-003 | Pending | high | diataxis-tutorial | Audit P1-4, P2-7 |
| FEAT-040-019 | Revise 4 playbooks (extract reference tables into skills catalog) | EPIC-040-003 | Pending | medium | diataxis-howto + diataxis-reference | Audit P3-4 |
| FEAT-040-020 | Create docs/tutorial/ and docs/how-to/ directory structure | EPIC-040-003 | Pending | high | manual + diataxis-tutorial | Audit P1-5, P2-5 |

### EPIC-040-004: Skill Tutorials

New tutorials for top-priority skills (order driven by Wave 1 Kano classification).

| ID | Title | Parent | Status | Priority | Diataxis Agent |
|----|-------|--------|--------|----------|----------------|
| FEAT-040-021 | Tutorial: "Your First Research Spike with /problem-solving — evaluating Pydantic v2" | EPIC-040-004 | Pending | high | diataxis-tutorial |
| FEAT-040-022 | Tutorial: /worktracker — setting up your first tracked project | EPIC-040-004 | Pending | high | diataxis-tutorial |
| FEAT-040-023 | Tutorial: /orchestration — your first multi-phase workflow | EPIC-040-004 | Pending | medium | diataxis-tutorial |

Additional tutorials added as Wave 1 Kano output identifies must-be candidates.

### EPIC-040-005: Skill How-To Guides

One guide per skill lacking current coverage. 26 skills in scope; order by Wave 1 JTBD priority.

| ID | Title | Parent | Status | Priority | Diataxis Agent |
|----|-------|--------|--------|----------|----------------|
| FEAT-040-024 | How-to: Run an adversarial review with /adversary | EPIC-040-005 | Pending | high | diataxis-howto |
| FEAT-040-025 | How-to: Invoke /eng-team for a threat model | EPIC-040-005 | Pending | high | diataxis-howto |
| FEAT-040-026 | How-to: Use /diataxis to audit existing documentation | EPIC-040-005 | Pending | high | diataxis-howto |
| FEAT-040-027 | How-to: Generate a PRD via /pm-pmm | EPIC-040-005 | Pending | medium | diataxis-howto |
| FEAT-040-028 | How-to: Generate BDD tests via /test-spec from a use case | EPIC-040-005 | Pending | medium | diataxis-howto |
| FEAT-040-029 | How-to: Generate an API contract via /contract-design | EPIC-040-005 | Pending | medium | diataxis-howto |
| FEAT-040-030 | How-to: Author a use case via /use-case | EPIC-040-005 | Pending | medium | diataxis-howto |
| FEAT-040-031 | How-to: Build a structured prompt via /prompt-engineering | EPIC-040-005 | Pending | medium | diataxis-howto |
| FEAT-040-032 | How-to: Run a UX evaluation via /user-experience (with sub-skill routing) | EPIC-040-005 | Pending | medium | diataxis-howto |
| FEAT-040-033..040 | How-to guides for remaining skills (red-team, nasa-se, bootstrap, saucer-boy, transcript-deep, architecture, ast, ux-*) | EPIC-040-005 | Pending | medium-low | diataxis-howto |

### EPIC-040-006: Skill Explanations

Design-rationale docs for the most conceptually loaded skills. Wave 1 Kano identifies which skills need explanation vs. reference only.

| ID | Title | Parent | Status | Priority | Diataxis Agent |
|----|-------|--------|--------|----------|----------------|
| FEAT-040-041 | Explanation: why /problem-solving uses structured agent routing | EPIC-040-006 | Pending | medium | diataxis-explanation |
| FEAT-040-042 | Explanation: why /nasa-se applies mission-grade systems engineering | EPIC-040-006 | Pending | medium | diataxis-explanation |
| FEAT-040-043 | Explanation: why /orchestration enforces single-level nesting (P-003) | EPIC-040-006 | Pending | medium | diataxis-explanation |
| FEAT-040-044 | Explanation: why /eng-team separates security responsibilities across 10 agents | EPIC-040-006 | Pending | medium | diataxis-explanation |
| FEAT-040-045 | Explanation: why /diataxis treats docs as four quadrants | EPIC-040-006 | Pending | medium | diataxis-explanation |

### EPIC-040-007: Agent Reference Catalog

External-facing companion to `AGENTS.md`. Audit finds AGENTS.md is reference/explanation mixed. Tracked as [GH #265](https://github.com/geekatron/jerry/issues/265).

| ID | Title | Parent | Status | Priority | Diataxis Agent |
|----|-------|--------|--------|----------|----------------|
| FEAT-040-046 | Agent reference catalog schema and table structure | EPIC-040-007 | Pending | medium | diataxis-reference |
| FEAT-040-047 | Reference entries for 88 agents (input, output, cognitive mode, tier) | EPIC-040-007 | Pending | medium | diataxis-reference |
| FEAT-040-048 | Cross-reference index (agent → skill, skill → agents, tier → agents) | EPIC-040-007 | Pending | medium | diataxis-reference |

### EPIC-040-008: Polish & Metadata

| ID | Title | Parent | Status | Priority |
|----|-------|--------|--------|----------|
| FEAT-040-049 | Diataxis quadrant frontmatter metadata on all docs | EPIC-040-008 | Pending | low |
| FEAT-040-050 | Navigation-table sweep (NAV-001 / NAV-006 compliance) | EPIC-040-008 | Pending | low |
| FEAT-040-051 | Final link validation across all docs | EPIC-040-008 | Pending | low |
| FEAT-040-052 | Cross-reference validation (no dead anchors) | EPIC-040-008 | Pending | low |

---

## Supersession Carry-Forward

Features ported from PROJ-016 into PROJ-040 epics:

| PROJ-016 Feature | PROJ-040 Successor | Notes |
|------------------|-------------------|-------|
| FEAT-016-001 Decompose prompt-quality.md | (deferred) | Rules file; out of scope per PROJ-015 methodology |
| FEAT-016-002 Create context-architecture.md | FEAT-040-013 | Merged into EPIC-040-003 |
| FEAT-016-003 Create hooks-architecture.md | FEAT-040-014 | Merged into EPIC-040-003 |
| FEAT-016-004 Revise INSTALLATION.md | FEAT-040-015 | Merged; scope expanded to include stale skills table fix |
| FEAT-016-005 Write /problem-solving tutorial | FEAT-040-021 | Moved to EPIC-040-004 with named research subject |
| FEAT-016-006 Write /orchestration tutorial | FEAT-040-023 | Moved |
| FEAT-016-007 Write /worktracker tutorial | FEAT-040-022 | Moved |
| FEAT-016-008 Decompose prompt-templates.md | (deferred) | Rules file |
| FEAT-016-009 Skills Reference | FEAT-040-019 (reference table extraction) | Partially absorbed; agent reference catalog is new (EPIC-040-007) |
| FEAT-016-010 CLI Reference | (deferred) | Low priority given current scope |
| FEAT-016-011..015 Top 5 skill explanations | FEAT-040-041..045 | Expanded to include /diataxis and /eng-team |
| FEAT-016-016..017 Polish | FEAT-040-049..052 | Moved to EPIC-040-008 |

---

## Audit Traceability

Each epic ties to findings in `reports/diataxis-audit-20260420.md`:

| Epic | Audit Remediation IDs |
|------|----------------------|
| EPIC-040-002 | P1-1 (README + docs/index skills table), P1-6 (AGENTS.md count accuracy) |
| EPIC-040-003 | P1-2, P1-3, P1-4, P2-1, P2-2, P2-3, P2-4, P2-7, P3-4, P3-5 |
| EPIC-040-004 | P1-5 (priority tutorial), P2-6 (worktracker tutorial) |
| EPIC-040-005 | P2-5 (4 priority how-tos), P3-1 (UX how-tos), P3-2 (contract/test-spec/use-case), P3-6 (diataxis/prompt-engineering/saucer-boy) |
| EPIC-040-006 | P3-3 (core skill explanations) |
| EPIC-040-007 | New (audit identifies gap: "No external agent reference catalog") |
| EPIC-040-008 | (metadata, sweep) |

---

## Change Log

| Date | Change |
|------|--------|
| 2026-04-20 | Initial creation; consolidates PROJ-015 (audit) and PROJ-016 (writing). Diataxis audit approved at C4 ≥ 0.95 (0.956 composite). |
