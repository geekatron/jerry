# Doc Module Orchestration Plan

> **Document ID:** PROJ-0037-doc-module-ORCH-PLAN
> **Workflow ID:** doc-module-20260308-001
> **Date:** 2026-03-08
> **Status:** PLANNED
> **Criticality:** C2 (Standard)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Workflow Overview](#l0-workflow-overview) | Plain-language summary for stakeholders |
| [L1: Technical Plan](#l1-technical-plan) | Workflow diagram, pipeline definitions, sync barriers |
| [L2: Implementation Details](#l2-implementation-details) | State schema, path configuration, recovery strategies |
| [Disclaimer](#disclaimer) | Authorship and review notice |

---

## L0: Workflow Overview

This orchestration plan coordinates the work required to fix Jerry's public-facing documentation and build the infrastructure to keep it accurate going forward. Two parallel workstreams run concurrently.

Workstream A audits what is currently wrong with the README and related docs (outdated skill counts, missing skills, stale limitations), then authors corrected content. Workstream B researches how to build an automated documentation generation module, selects the best design approach, threat-models the selected design, and produces an implementation specification engineers can build from.

After both workstreams complete, a synthesis agent reconciles the two outputs — ensuring the README content authored in A is structurally compatible with the auto-documentation system designed in B. The result is a documentation surface that is both immediately accurate and durably maintainable.

---

## L1: Technical Plan

### Workflow Diagram (ASCII)

```
Workstream A (ws-a)              Workstream B (ws-b)
─────────────────────────────    ─────────────────────────────────────
┌─────────────────────────┐      ┌─────────────────────────┐
│  Phase A1               │      │  Phase B1               │
│  Agent: ps-researcher   │      │  Agent: ps-researcher   │
│  Current-state          │      │  Doc-module patterns    │
│  inventory              │      │  research (Context7 +   │
│                         │      │  WebSearch)             │
└────────────┬────────────┘      └────────────┬────────────┘
             │ Quality Gate A1                 │ Quality Gate B1
             │ >= 0.92                         │ >= 0.92
             ▼                                 ▼
┌─────────────────────────┐      ┌─────────────────────────┐
│  Phase A2               │      │  Phase B2               │
│  Agent: ps-architect    │      │  Agent: ps-architect    │
│  README-draft.md        │      │  ADR: 3 design options  │
│  (updated content)      │      │  evaluated              │
└────────────┬────────────┘      └────────────┬────────────┘
             │ Quality Gate A2                 │ Quality Gate B2
             │ >= 0.92                         │ >= 0.92
             │                                 ▼
             │                    ┌─────────────────────────┐
             │                    │  Phase B3               │
             │                    │  Agent: eng-architect   │
             │                    │  STRIDE threat model    │
             │                    │  for selected design    │
             │                    └────────────┬────────────┘
             │                                 │ Quality Gate B3
             │                                 │ >= 0.92
             │                                 ▼
             │                    ┌─────────────────────────┐
             │                    │  Phase B4               │
             │                    │  Agent: ps-analyst      │
             │                    │  Implementation spec    │
             │                    │  (input/output/tests)   │
             │                    └────────────┬────────────┘
             │                                 │ Quality Gate B4
             │                                 │ >= 0.92
             │                                 │
             └──────────────┬──────────────────┘
                            │
                    ╔═══════════════════╗
                    ║   BARRIER-1       ║
                    ║  Sync Barrier     ║
                    ║  All phases done  ║
                    ║  Quality Gate     ║
                    ║  >= 0.92          ║
                    ╚═══════════╦═══════╝
                                │
                    ┌───────────▼───────────┐
                    │  Synthesis            │
                    │  Agent: orch-         │
                    │  synthesizer          │
                    │  Cross-workstream     │
                    │  reconciliation       │
                    └───────────────────────┘
```

### Pipeline Definitions

#### Workstream A — Documentation Update (`ws-a`)

| Phase | ID | Agent | Skill | Input | Output Artifact | Quality Gate |
|-------|----|-------|-------|-------|-----------------|--------------|
| A1 | `ws-a-phase-1` | ps-researcher | /problem-solving | skills/*/SKILL.md, skills/*/agents/*.md, AGENTS.md, README.md, CLAUDE.md, .context/rules/mandatory-skill-usage.md, docs/INSTALLATION.md, CONTRIBUTING.md | `orchestration/doc-module-20260308-001/ws-a/phase-1/ps-researcher-001/current-state-inventory.md` | >= 0.92 |
| A2 | `ws-a-phase-2` | ps-architect | /problem-solving | A1 output | `orchestration/doc-module-20260308-001/ws-a/phase-2/ps-architect-001/README-draft.md` | >= 0.92 |

**Phase A1 focus areas:**
- Skills absent from README skills table
- Correct agent count (currently stated vs. actual 58)
- Unlinked or stale documentation references
- Stale Known Limitations section
- Example session accuracy
- Discrepancies between CLAUDE.md, AGENTS.md, and README

**Phase A2 author tasks:**
- Expand skills table to all 13 skills
- Fix agent count to 58
- Update documentation table
- Review and update Known Limitations
- Verify example session is still accurate
- Ensure AGENTS.md consistency
- Keep README under 250 lines, public-facing tone, no internal conventions

#### Workstream B — Doc Module Engineering (`ws-b`)

| Phase | ID | Agent | Skill | Input | Output Artifact | Quality Gate |
|-------|----|-------|-------|-------|-----------------|--------------|
| B1 | `ws-b-phase-1` | ps-researcher | /problem-solving | Context7 (Elixir Phoenix, Python doc tools), WebSearch | `orchestration/doc-module-20260308-001/ws-b/phase-1/ps-researcher-001/doc-module-patterns.md` | >= 0.92 |
| B2 | `ws-b-phase-2` | ps-architect | /problem-solving | B1 output | `orchestration/doc-module-20260308-001/ws-b/phase-2/ps-architect-001/ADR-PROJ0037-001-doc-module-design.md` | >= 0.92 |
| B3 | `ws-b-phase-3` | eng-architect | /eng-team | B2 ADR (selected design) | `orchestration/doc-module-20260308-001/ws-b/phase-3/eng-architect-001/threat-model-doc-module.md` | >= 0.92 |
| B4 | `ws-b-phase-4` | ps-analyst | /problem-solving | B2 ADR + B3 threat model | `orchestration/doc-module-20260308-001/ws-b/phase-4/ps-analyst-001/doc-module-spec.md` | >= 0.92 |

**Phase B1 research focus:**
- Template-based README generation patterns
- Pre-commit vs. CI vs. CLI trade-off analysis
- Jerry-specific YAML frontmatter as metadata source
- Elixir Phoenix `mix docs`/`moduledoc` patterns (via Context7)
- Python doc generation: Sphinx, mkdocs, pydoc-markdown (via Context7)
- Self-documenting agent framework patterns (via WebSearch)

**Phase B2 options evaluated:**

| Option | Description |
|--------|-------------|
| A | Python CLI `jerry docs generate` using jerry ast + Jinja2 |
| B | Shell script with grep/awk |
| C | CI-only GitHub Action |

Evaluation dimensions: maintainability, accuracy, H-05/H-33 compliance, developer experience, failure modes.

**Phase B3 STRIDE threat scope:**
- Malformed SKILL.md injection into templates
- Jinja2 supply chain risks
- File system trust boundary
- Partial write failure modes

**Phase B4 spec coverage:**
- Input parsing: YAML frontmatter fields from SKILL.md and agent files
- Output rendering: Jinja2 template structure
- Drift detection mechanism
- Error handling per error-handling-standards
- Integration points: pre-commit hook, CI step, CLI command
- Test plan: unit, integration, golden-file comparison

### Sync Barriers

| Barrier | ID | Trigger Condition | Quality Gate | Agents Coordinated |
|---------|----|-------------------|--------------|-------------------|
| BARRIER-1 | `barrier-1` | A2 complete AND B4 complete | >= 0.92 composite | orch-synthesizer consumes ws-a/phase-2 + ws-b/phase-4 |

**BARRIER-1 synthesis tasks:**
- Verify README draft (A2) is structurally compatible with auto-doc spec (B4)
- Identify overlaps: does the spec generate the same README structure authored in A2?
- Flag any discrepancies between manually-authored and auto-generated content models
- Produce reconciliation recommendations

**Synthesis output:** `orchestration/doc-module-20260308-001/synthesis/cross-workstream-synthesis.md`

### Dependency Graph

```
A1 --> A2 ─────────────────────────────────────┐
                                                 ├─-> BARRIER-1 --> Synthesis
B1 --> B2 --> B3 --> B4 ────────────────────────┘
```

- Workstreams A and B are independent and MAY execute in parallel.
- Within ws-a: A1 must complete before A2 begins.
- Within ws-b: B1 → B2 → B3 → B4 (strictly sequential).
- BARRIER-1: A2 AND B4 must both complete before synthesis begins.

---

## L2: Implementation Details

### State Schema (ORCHESTRATION.yaml)

See `ORCHESTRATION.yaml` in this directory for the full machine-readable schema.

Key schema sections:

```yaml
workflow:
  id: "doc-module-20260308-001"
  name: "Doc Module — Documentation Update + Engineering"
  status: "PLANNED"

paths:
  base: "orchestration/doc-module-20260308-001/"
  pipeline_a: "{base}ws-a/{phase_id}/"
  pipeline_b: "{base}ws-b/{phase_id}/"
  barrier: "{base}cross-pollination/{barrier_id}/"
  synthesis: "{base}synthesis/"

quality:
  threshold: 0.92
  criticality: "C2"
  required_strategies: [S-007, S-002, S-014]
```

### Dynamic Path Configuration

All artifact paths use the workflow ID as the base identifier. No hardcoded pipeline names appear in path construction.

| Path Type | Pattern | Example |
|-----------|---------|---------|
| Base | `orchestration/{workflow_id}/` | `orchestration/doc-module-20260308-001/` |
| Pipeline phase | `{base}{pipeline_alias}/phase-{N}/{agent}-{NNN}/` | `orchestration/doc-module-20260308-001/ws-a/phase-1/ps-researcher-001/` |
| Barrier | `{base}cross-pollination/{barrier_id}/` | `orchestration/doc-module-20260308-001/cross-pollination/barrier-1/` |
| Synthesis | `{base}synthesis/` | `orchestration/doc-module-20260308-001/synthesis/` |

### Criticality Assessment

**Level: C2 (Standard)**

| Factor | Assessment |
|--------|-----------|
| Reversibility | Reversible within 1 day — file edits, no schema changes, no infrastructure changes |
| File scope | 6 output artifacts + 1 synthesis + README.md update = 3-10 files |
| Impact | Module-level: documentation surface and new CLI command scope |
| Auto-escalation | AE-002 does not apply (no .context/rules/ changes). AE-003 applies to ADR in B2 (auto-C3 minimum for new ADR). |

**AE-003 Note:** Phase B2 produces a new ADR (`ADR-PROJ0037-001-doc-module-design.md`). Per AE-003, this auto-escalates B2 to C3 minimum. The overall workflow criticality remains C2; B2 phase quality gate is treated as C3 (all tiers required for that phase). See quality section in ORCHESTRATION.yaml.

### Quality Gate Definitions

**Per-phase quality gates (C2 standard set):**

| Gate | Location | Required Strategies | Threshold | Max Iterations |
|------|----------|---------------------|-----------|----------------|
| QG-A1 | After Phase A1 | S-010 (self-refine), S-014 (LLM-as-Judge) | >= 0.92 | 5 (C2 ceiling) |
| QG-A2 | After Phase A2 | S-007, S-002, S-014 | >= 0.92 | 5 |
| QG-B1 | After Phase B1 | S-010, S-014 | >= 0.92 | 5 |
| QG-B2 | After Phase B2 | S-007, S-002, S-004, S-012, S-013, S-014 | >= 0.92 | 7 (C3 ceiling — ADR, AE-003) |
| QG-B3 | After Phase B3 | S-007, S-002, S-014 | >= 0.92 | 5 |
| QG-B4 | After Phase B4 | S-007, S-002, S-014 | >= 0.92 | 5 |
| QG-BARRIER-1 | Synthesis barrier | S-007, S-002, S-014 | >= 0.92 | 5 |

**Scoring dimensions (S-014):**

| Dimension | Weight |
|-----------|--------|
| Completeness | 0.20 |
| Internal Consistency | 0.20 |
| Methodological Rigor | 0.20 |
| Evidence Quality | 0.15 |
| Actionability | 0.15 |
| Traceability | 0.10 |

**Creator-critic-revision assignment:**

| Phase | Creator Agent | Critic Agent | Revision Agent |
|-------|--------------|--------------|----------------|
| A1 | ps-researcher | ps-critic (embedded) | ps-researcher |
| A2 | ps-architect | ps-critic (embedded) | ps-architect |
| B1 | ps-researcher | ps-critic (embedded) | ps-researcher |
| B2 | ps-architect | ps-critic (embedded) | ps-architect |
| B3 | eng-architect | ps-critic (embedded) | eng-architect |
| B4 | ps-analyst | ps-critic (embedded) | ps-analyst |
| Synthesis | orch-synthesizer | ps-critic (embedded) | orch-synthesizer |

### Recovery Strategies

| Failure Mode | Detection | Recovery Action |
|--------------|-----------|-----------------|
| Phase fails quality gate after 5 iterations | Score plateau: delta < 0.01 for 3 consecutive iterations | Halt phase, present best result to user, await guidance (H-31) |
| B2 ADR selects option that conflicts with H-05 | S-007 constitutional check during QG-B2 | Reject Option B (shell script) if H-05 compliance not satisfiable; default to Option A |
| B3 threat model reveals blocking risk in selected design | CRITICAL finding in STRIDE output | Surface finding before B4; B4 spec must address all CRITICAL threats or B2 must be reconsidered |
| A2 README draft exceeds 250-line constraint | Line count check during QG-A2 | Revision required before gate passes |
| BARRIER-1: A2 and B4 structurally incompatible | Synthesis identifies irreconcilable structural mismatch | Return reconciliation recommendations; do not silently produce a synthesis that papers over the conflict |
| Phase agent unavailable | No output artifact produced within session | Mark phase BLOCKED in ORCHESTRATION_WORKTRACKER.md; surface to user |

### Context7 Usage Plan (MCP-001)

Phase B1 requires Context7 for external library documentation per MCP-001:

| Library | Context7 Query | Phase |
|---------|---------------|-------|
| Elixir Phoenix | `mix docs`, `moduledoc` patterns | B1 |
| Sphinx | Auto-documentation from docstrings | B1 |
| mkdocs | YAML-driven site generation | B1 |
| pydoc-markdown | Markdown output from Python docstrings | B1 |
| Jinja2 | Template rendering patterns | B2, B4 |

---

## Disclaimer

This orchestration plan was generated by the orch-planner agent (v2.2.0) on 2026-03-08. Human review is recommended before execution. Phase-level quality scores, barrier results, and synthesis findings will be populated by orch-tracker as the workflow executes.

This plan is scoped to `PROJ-0037-doc-module`. It does not represent official guidance for any external system or organization.
