# Wave 1 Full-Set Adversarial Tournament: Remediation Iter-1

> **Document ID:** PROJ-040-ORCH-REVIEW-FULLSET-ITER1
> **Scope:** FULL deliverable set — `.md` + `.yaml` together
> **Criticality:** C4
> **Threshold:** >= 0.95
> **Prior scope:** Iter-1 through iter-4 reviewed `.md` only (ORCHESTRATION_PLAN.md)
> **This scope:** Cross-file consistency surface + YAML-specific requirements
> **Executed:** 2026-04-17
> **Strategy sequence:** S-010, S-003, S-002, S-007, S-004, S-012, S-013, S-011, S-001, S-014

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Execution Context](#execution-context) | Files reviewed, scope, iteration |
| [Cross-File Consistency Matrix](#cross-file-consistency-matrix) | Claim-by-claim md vs yaml match |
| [YAML Schema Compliance Checklist](#yaml-schema-compliance-checklist) | Top-level sections, must clauses, constraints |
| [Findings Summary](#findings-summary) | All findings tabulated |
| [Detailed Findings](#detailed-findings) | Per-finding evidence and recommendations |
| [Per-Strategy Results](#per-strategy-results) | S-010 through S-001 execution notes |
| [S-014 Scoring](#s-014-scoring) | LLM-as-Judge composite |
| [Verdict](#verdict) | Pass/Fail + top 3 blockers |

---

## Execution Context

- **Strategy:** C4 tournament (all 10 strategies)
- **Templates:** `.context/templates/adversarial/s-{NNN}-{slug}.md`
- **Deliverable 1:** `projects/PROJ-040-documentation/orchestration/plans/wave-1-discovery-plan.md` (812 lines)
- **Deliverable 2:** `projects/PROJ-040-documentation/ORCHESTRATION.yaml` (987 lines)
- **Executed:** 2026-04-17T00:00:00Z
- **Prior verdicts:** iter-4 PASS at 0.972 (`.md` only); this iteration extends scope to `.yaml` + cross-file surface
- **Canonical sequence enforced:** S-010 → S-003 → S-002 → S-007 → S-004 → S-012 → S-013 → S-011 → S-001 → S-014
- **H-16 status:** S-003 (Steelman) executed before S-002 (Devil's Advocate) — compliant

---

## Cross-File Consistency Matrix

> Claim-by-claim verification: every structural claim in the `.md` checked against its `.yaml` counterpart.

| Claim | MD Location | YAML Location | Match? | Notes |
|-------|------------|---------------|--------|-------|
| Workflow ID `wave-1-discovery-20260417-001` | Frontmatter | `workflow.id` | MATCH | Exact string match |
| Phase 1a feature count = 9 | Phase Overview table | pipeline.ux.phases[1a].agents (7) + pipeline.pm.phases[1a].agents (1) + pipeline.research.phases[1a].agents (1) = 9 | MATCH | |
| Phase 1b feature count = 4 | Phase Overview table | pipeline.ux.phases[1b].agents (2) + pipeline.pm.phases[1b].agents (2) = 4 | MATCH | |
| FEAT-040-001 ux-jtbd-analyst Phase 1a | Feature-to-Phase Mapping | pipelines.ux.phases[1a].agents[0] | MATCH | dispatch_priority FIRST in both |
| FEAT-040-002 dual-pass (provisional 1a + authoritative 1b) | Feature-to-Phase Mapping, Artifact Paths | pipelines.ux.phases[1a] + phases[1b]; separate artifact paths | MATCH | provisional-output.md vs output.md paths align |
| FEAT-040-003 ux-kano-analyst Phase 1b | Feature-to-Phase Mapping | pipelines.ux.phases[1b].agents[0] | MATCH | |
| FEAT-040-004 ux-heuristic-evaluator Phase 1a | Feature-to-Phase Mapping | pipelines.ux.phases[1a].agents[2] | MATCH | |
| FEAT-040-005 ux-inclusive-evaluator Phase 1a | Feature-to-Phase Mapping | pipelines.ux.phases[1a].agents[3] | MATCH | |
| FEAT-040-006 ux-behavior-diagnostician Phase 1a | Feature-to-Phase Mapping | pipelines.ux.phases[1a].agents[4] | MATCH | |
| FEAT-040-007 ux-lean-ux-facilitator Phase 1a | Feature-to-Phase Mapping | pipelines.ux.phases[1a].agents[5] | MATCH | |
| FEAT-040-008 ux-atomic-architect Phase 1a | Feature-to-Phase Mapping | pipelines.ux.phases[1a].agents[6] | MATCH | |
| FEAT-040-053 pm-customer-insight Phase 1b | Feature-to-Phase Mapping | pipelines.pm.phases[1b].agents[0] | MATCH | |
| FEAT-040-054 pm-market-strategist Phase 1b | Feature-to-Phase Mapping | pipelines.pm.phases[1b].agents[1] | MATCH | |
| FEAT-040-055 pm-competitive-analyst Phase 1a | Feature-to-Phase Mapping | pipelines.pm.phases[1a].agents[0] | MATCH | |
| FEAT-040-056 ps-researcher Phase 1a | Feature-to-Phase Mapping | pipelines.research.phases[1a].agents[0] | MATCH | |
| FEAT-040-057 synthesis Phase 3 | Feature-to-Phase Mapping | barriers.QG-3.features_required + execution_queue.pending_phase_3 | MATCH | Correctly not a pipeline (YAML comment confirms) |
| QG-1A barrier | Quality Gates table | barriers[0].barrier_id = "QG-1A" | MATCH | |
| QG-1B barrier | Quality Gates table | barriers[1].barrier_id = "QG-1B" | MATCH | |
| QG-2 barrier | Quality Gates table | barriers[2].barrier_id = "QG-2" | MATCH | |
| QG-2.5 barrier | Quality Gates table | barriers[3].barrier_id = "QG-2.5" | MATCH | |
| QG-3 barrier | Quality Gates table | barriers[4].barrier_id = "QG-3" | MATCH | |
| Per-feature threshold 0.92 | Phase Overview, Gate Definitions | `workflow.constraints.quality_threshold_feature: 0.92`; per-agent `quality_threshold: 0.92`; QG-1A/1B `threshold: 0.92` | MATCH | |
| Wave-boundary threshold 0.95 | QG-3 definition | `workflow.constraints.quality_threshold_wave: 0.95`; `adversarial.quality.threshold_synthesis: 0.95`; QG-3 `threshold: 0.95` | MATCH | |
| C3 iteration ceiling = 7 | State Schema, Failure Handling | `workflow.constraints.max_critic_iterations: 7`; per-agent `iteration_ceiling: 7`; QG-3 `min_iterations: 3` | MATCH | |
| C4 iteration ceiling = 10 | Failure Handling, Runtime step 24h | `workflow.constraints.max_synthesis_iterations: 10`; QG-3 `max_iterations: 10` | MATCH | |
| Artifact path scheme `work/EPIC-040-001/{stream}/{feature-id}/{agent}-output.md` | Artifact Paths section, L2 Path Configuration | `paths.ux_artifacts`, `paths.pm_artifacts`, `paths.research_artifacts` | MATCH | Template syntax consistent |
| FEAT-040-001 in `execution_queue.ready_to_dispatch` | Runtime Behavior Phase 1a priority | `execution_queue.ready_to_dispatch[0].feature_id: FEAT-040-001`, `priority: FIRST` | MATCH | |
| H-16 S-003 before S-002 | QG-3 adversarial section | `adversarial.C4_synthesis.h16_enforced: true`; canonical_sequence has S-003 at position 2, S-002 at position 3 | MATCH | |
| P-003 max_agent_nesting = 1 | Quality Review Protocol (P-003 note) | `workflow.constraints.max_agent_nesting: 1` | MATCH | |
| P-002 file_persistence | Quality Review Protocol, Disclaimer | `workflow.constraints.file_persistence: true` | MATCH | |
| Checkpoint at QG-1A | Checkpoint Strategy table | `checkpoints` section documents phase-1a-checkpoint.yaml | MATCH | |
| Checkpoint at QG-1B | Checkpoint Strategy table | phase-1b-checkpoint.yaml documented in checkpoints | MATCH | |
| Disclaimer present | Disclaimer section | YAML disclaimer comment at lines 981-987 | MATCH | Both files carry disclaimer |
| C3 per-feature strategies: S-010, S-002, S-014 required | Quality Review Protocol step 8b | `adversarial.strategy_sets.C3_per_feature.required: [S-010, S-002, S-014]` | MATCH | **But see FM-FS-001: both files underspecify C3 vs constitution** |
| C4 all-10 strategies | QG-3 adversarial section, Runtime step 24c | `adversarial.strategy_sets.C4_synthesis.required: [all 10]` | MATCH | |
| Synthesis artifact path | HO-W1-013, QG-3 synthesis_artifact | QG-3.synthesis_artifact matches HO-W1-013 artifact list final entry | MATCH | |
| XP-01 through XP-07 catalog | Cross-Pollination Points | pipeline agent `xp_provides` arrays; execution_queue xp_enrichment | MATCH | All 7 XP IDs appear in YAML |
| QG-2.5 fidelity report path | QG-2.5 Protocol | barriers.QG-2.5.fidelity_report_path matches plan path | MATCH | |
| State files path template | State Schema | `paths.state_files` template matches plan | MATCH | |
| resumption.load_order self-reference | Session Resume Protocol | `resumption.load_order[0].path: "projects/PROJ-040-documentation/ORCHESTRATION.yaml"` | MATCH | |
| WORKTRACKER entity FEAT-040-058 | Frontmatter | `workflow.worktracker_entity: "FEAT-040-058"` | MATCH | |

**Cross-File Consistency Matrix Result: 37/37 claims verified. Zero mismatches.**

---

## YAML Schema Compliance Checklist

### Top-Level Sections

| Section | Present? | Non-Empty? |
|---------|----------|------------|
| `schema_version` | YES | YES (2.0.0) |
| `workflow` | YES | YES (14 subfields) |
| `paths` | YES | YES (11 path templates + resolved examples) |
| `pipelines` | YES | YES (ux, pm, research) |
| `barriers` | YES | YES (5 barriers: QG-1A through QG-3) |
| `adversarial` | YES | YES (3 strategy sets + quality subblock) |
| `execution_queue` | YES | YES (ready_to_dispatch + all 4 pending phases) |
| `checkpoints` | YES | YES (latest_id null + documented entry types) |
| `metrics` | YES | YES (execution + quality + timing subblocks) |
| `blockers` | YES | YES (active: [], resolved: []) |
| `issues` | YES | YES (logged: []) |
| `next_actions` | YES | YES (immediate + upcoming) |
| `resumption` | YES | YES (load_order 5 entries) |

**Score: 13/13 sections present and non-empty.**

### orch-planner Must Clauses

| Must Clause | Compliant? | Evidence |
|-------------|------------|---------|
| Generate or accept workflow ID | YES | `workflow.id: wave-1-discovery-20260417-001` |
| Resolve pipeline aliases | YES | `ux`, `pm`, `research` short_alias fields |
| Use dynamic path scheme | YES | `{base}`, `{feature-id}`, `{agent}` templates in paths block |
| Create ORCHESTRATION_PLAN.md | YES (predecessor) | `workflow.plan_ref` confirms .md exists |
| Include L0/L1/L2 output levels | YES | .md contains all three levels |
| Include ASCII workflow diagram | YES | .md contains both Mermaid and ASCII diagrams |
| Define all phases, agents, barriers | YES | 3 pipelines + 5 barriers fully defined |
| Create ORCHESTRATION.yaml state file | YES | This file |
| Include disclaimer | YES | Both .md (Disclaimer section) and YAML (comment block lines 981-987) |
| Assess criticality level | YES | `workflow.constraints.criticality_synthesis: C4`; `criticality_per_feature: C3` |
| Include quality gate definitions | YES | 5 barriers with threshold, blocking_behavior, strategies |
| Specify required adversarial strategies per criticality | YES (C4); PARTIAL (C3) | C4 all-10 correct; C3 underspecifies per FM-FS-001 |
| Initialize quality section in ORCHESTRATION.yaml | YES | `adversarial.quality` block present |

### workflow.constraints Verification

| Constraint | Value | Correct? |
|-----------|-------|---------|
| `max_agent_nesting: 1` | 1 | YES — P-003/H-01 |
| `file_persistence: true` | true | YES — P-002 |
| `user_authority: true` | true | YES — P-020/H-02 |
| `max_critic_iterations: 7` | 7 | YES — RT-M-010 C3 |
| `max_synthesis_iterations: 10` | 10 | YES — RT-M-010 C4 |
| `quality_threshold_feature: 0.92` | 0.92 | YES — H-13 |
| `quality_threshold_wave: 0.95` | 0.95 | YES — C4 |
| `min_critic_iterations: 3` | 3 | YES — H-14 |
| `criticality_per_feature: C3` | C3 | YES |
| `criticality_synthesis: C4` | C4 | YES |

---

## Findings Summary

| ID | Severity | Finding | Section |
|----|----------|---------|---------|
| FM-FS-001 | Major | C3 per-feature adversarial strategy set underspecifies constitutional required strategies (missing S-007, S-004, S-012, S-013 from quality-enforcement.md C3 required set); cross-file consistent but both files wrong | YAML `adversarial.strategy_sets.C3_per_feature`; .md Quality Review Protocol |
| FM-FS-002 | Minor | `adversarial.quality.required_strategies` global list (all 10) creates ambiguity: unclear whether these apply to all features or C4 only; the `full_tournament_at: [QG-3]` annotation partially clarifies but is incomplete | YAML `adversarial.quality.required_strategies` |
| FM-FS-003 | Minor | YAML disclaimer uses informal reference `P-043 compliance` but `P-043` does not appear in `quality-enforcement.md` or constitution; likely a stale/invented principle code; should reference orch-planner specification directly | YAML lines 981-987 disclaimer comment |
| FM-FS-004 | Minor | `barriers.QG-1B.blocking_behavior` states "All Phase 1b features are enrichment-dependent on Phase 1a; none are hard dependencies for each other. If any Phase 1b feature is blocked: orchestrator notes which synthesis inputs will be partial and flags in synthesis handoff. Proceed to Phase 2 with gap noted." This contradicts FEAT-040-002 (HEART) enriched pass dependency: the authoritative HEART output is a hard dependency for synthesis (QG-3 synthesis_inputs lists the authoritative path). The blocking_behavior implies a partial-proceed is always safe, which is not true if HEART enriched fails | YAML `barriers.QG-1B.blocking_behavior`; cross-reference with QG-3 synthesis_inputs |
| FM-FS-005 | Minor | `resumption.session_resume_note` correctly instructs to check `phase_completions` for FEAT-040-002, but `resumption.load_order` does not include individual feature state file paths. On resume, the orchestrator must read state files to check `phase_completions` but the load_order only names ORCHESTRATION.yaml, the plan .md, WORKTRACKER.md, the baseline audit, and PLAN.md — not the state directory. This creates a resume gap: the orchestrator may load_order without knowing to check `orchestration/state/` | YAML `resumption.load_order` |

---

## Detailed Findings

### FM-FS-001: C3 Per-Feature Strategy Set Underspecifies Constitutional Required Strategies

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | YAML `adversarial.strategy_sets.C3_per_feature.required`; .md Quality Review Protocol step 8b |
| **Strategy Step** | S-007 Constitutional AI Critique (step 4); S-012 FMEA (step 3); S-011 Chain-of-Verification |

**Evidence:**

From YAML `adversarial.strategy_sets.C3_per_feature`:
```yaml
required: ["S-010", "S-002", "S-014"]
optional: ["S-003", "S-004", "S-007"]
```

From `quality-enforcement.md` Criticality Levels table:
```
C3 | Significant | ... | All tiers | C2 + S-004, S-012, S-013 | S-001, S-003, S-010, S-011
C2 | Standard    | ... | HARD + MEDIUM | S-007, S-002, S-014     | S-003, S-010
```

Per the constitution, C3 required = C2 required (S-007, S-002, S-014) + C3 additions (S-004, S-012, S-013) = **{S-007, S-002, S-014, S-004, S-012, S-013}**.

The YAML and .md both list only {S-010, S-002, S-014} as required for C3 features. This means:
- S-007 (Constitutional AI Critique) is listed as **optional** in YAML when it is **required** at C3
- S-004 (Pre-Mortem) is listed as **optional** in YAML when it is **required** at C3
- S-012 (FMEA) is entirely **absent from C3 required and optional** (not listed at all) when it is **required** at C3
- S-013 (Inversion) is entirely **absent** when it is **required** at C3

The .md Quality Review Protocol step 8b confirms: "Invoke /adversary adv-scorer on artifact_path (S-014, 6-dimension rubric)" — only S-014 per-feature. The per-feature quality protocol in the .md was approved at iter-4 with this gap present. The YAML faithfully mirrors the .md. **Both files are consistently wrong against the constitution.**

Note: S-010 (Self-Refine) is listed as **optional** in C3 per quality-enforcement.md but the YAML lists it as **required** — this is a conservative/more-rigorous choice and is acceptable.

**Analysis:**

This is the most impactful new finding from the YAML review. 13 C3 features will receive only a 3-strategy review (S-010 self-review + S-002 devil's advocate + S-014 scoring) when the constitution mandates at minimum a 6-strategy review (S-007 + S-002 + S-014 + S-004 + S-012 + S-013). The four missing strategies — particularly S-012 (FMEA, systematic failure enumeration) and S-013 (Inversion) — are precisely the strategies most likely to surface structural gaps in individual UX/PM/Research deliverables.

This gap does not invalidate the synthesis (QG-3 gets all 10 strategies). However, it means 13 upstream deliverables that feed the synthesis will receive insufficient adversarial scrutiny, which weakens the quality of inputs the synthesis consumes.

The gap existed in the iter-4 .md but was not flagged because that review did not probe per-feature strategy sets against quality-enforcement.md. The YAML makes the gap concrete and machine-readable, surfacing it for the first time.

**Recommendation:**

Option A (Minimal): Update YAML `adversarial.strategy_sets.C3_per_feature.required` to add S-007, S-004, S-012, S-013 and move them from optional to required. Update .md Quality Review Protocol to list the full C3 strategy set. Align the `quality.required_strategies` list accordingly.

Option B (Pragmatic scoping): Create a C3-minimal variant: `C3_per_feature_minimal` with the current 3 strategies for time-constrained features, with an explicit note that this is an approved H-13 exception for C3 features below the synthesis critical path. File an ADR for the exception. This preserves execution velocity while acknowledging the gap.

The plan should choose one option explicitly. Current state is non-compliant with no exception ADR.

---

### FM-FS-002: Global `required_strategies` List Creates Scope Ambiguity

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | YAML `adversarial.quality.required_strategies` (lines 725-735) |
| **Strategy Step** | S-011 Chain-of-Verification step 3 (internal reference validation) |

**Evidence:**

YAML `adversarial.quality` block contains:
```yaml
required_strategies:
  - "S-010"    # self-review (per feature)
  - "S-007"    # constitutional compliance (at synthesis)
  - "S-002"    # devil's advocate (synthesis C4)
  - "S-014"    # LLM-as-Judge (all)
  - "S-001"    # red team (C4 tournament)
  - "S-003"    # steelman (C4 tournament; H-16 requires before S-002)
  - "S-004"    # pre-mortem (C4 tournament; required at C4)
  - "S-011"    # chain-of-verification (C4 tournament)
  - "S-012"    # FMEA (C4 tournament)
  - "S-013"    # inversion (C4 tournament)
full_tournament_at:
  - "QG-3"     # synthesis exit gate — all 10 strategies required at C4
```

The inline comments ("at synthesis", "synthesis C4", "C4 tournament") clarify intent but the YAML key is named `required_strategies` without scope qualification. An orchestrator parsing this field by key name would interpret it as strategies required for all features. The `full_tournament_at: ["QG-3"]` only addresses the tournament context, not the full strategy scope.

**Analysis:**

This creates a parsing ambiguity for automated consumers (e.g., orch-tracker) that may read `required_strategies` without reading inline comments. The `strategy_sets.C3_per_feature` and `strategy_sets.C4_synthesis` blocks provide correctly scoped required lists, but the `adversarial.quality.required_strategies` block appears to duplicate/override them with a flat unscooped list.

**Recommendation:**

Rename `adversarial.quality.required_strategies` to `adversarial.quality.all_strategies_in_workflow` or add a `scope` annotation:
```yaml
required_strategies:
  scope: "C4_synthesis_only"   # add this disambiguating field
```
Or remove the flat list entirely (it is redundant given the `strategy_sets` blocks above it) and reference the `strategy_sets` blocks directly in comments.

---

### FM-FS-003: YAML Disclaimer References Non-Existent Principle P-043

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | YAML lines 981-987 (disclaimer comment block) |
| **Strategy Step** | S-007 Constitutional AI Critique step 2 (principle validation) |

**Evidence:**

YAML disclaimer contains: `# P-043 compliance: orch-planner mandatory disclaimer included.`

`quality-enforcement.md` HARD Rule Index documents rules H-01 through H-36. The principles cited in agent definitions (P-001 through P-022+) are drawn from the Jerry Constitution. A search of the codebase context finds no P-043 defined in `quality-enforcement.md`, `JERRY_CONSTITUTION.md` (not loaded but no reference exists in rule files), or `agent-development-standards.md`. The orch-planner spec (lines 290-337) uses a `<must>` clause for "Include disclaimer on all outputs" but does not define a P-043 code.

**Analysis:**

"P-043 compliance" appears to be a stale or invented principle code in the disclaimer. This is a minor traceability defect — the disclaimer text itself is correct and valuable, but the compliance label is unverifiable. Reviewers checking P-043 citations will find no reference definition.

**Recommendation:**

Replace `P-043 compliance: orch-planner mandatory disclaimer included.` with a traceable reference:

```yaml
# orch-planner mandatory disclaimer: required by orch-planner agent spec (must clause: "Include disclaimer on all outputs")
# Source: skills/orchestration/agents/orch-planner.md
```

Or if P-043 is a genuine principle in a document not loaded in this review, provide the source document path inline.

---

### FM-FS-004: QG-1B Blocking Behavior Implies Safe Partial-Proceed for HEART Enriched, Which Is Not Always True

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | YAML `barriers.QG-1B.blocking_behavior`; cross-reference YAML `barriers.QG-3.synthesis_inputs` |
| **Strategy Step** | S-004 Pre-Mortem (failure scenario analysis); S-012 FMEA |

**Evidence:**

YAML `barriers.QG-1B.blocking_behavior`:
```
All Phase 1b features are enrichment-dependent on Phase 1a outputs; none are hard dependencies
for each other. If any Phase 1b feature is blocked: orchestrator notes which synthesis inputs
will be partial and flags in synthesis handoff. Proceed to Phase 2 with gap noted.
```

YAML `barriers.QG-3.synthesis_inputs` includes:
```yaml
- "projects/PROJ-040-documentation/work/EPIC-040-001/ux/FEAT-040-002/ux-heart-analyst-output.md"
```

This is the **authoritative** HEART output (Phase 1b). If FEAT-040-002 Phase 1b is blocked, QG-3's synthesis_inputs would reference a non-existent file. The QG-1B blocking behavior says "proceed with gap noted" but the `barriers.QG-3` does not accommodate for a missing authoritative HEART path in synthesis_inputs.

The .md QG-1B blocking behavior (in Quality Gates section) matches the YAML language verbatim, so this is cross-file consistent. However, both files potentially underspecify the HEART blocked case: the synthesis handoff (HO-W1-013) lists the authoritative path `ux-heart-analyst-output.md` without a fallback to the provisional path `ux-heart-analyst-provisional-output.md`.

**Analysis:**

The Pre-Mortem scenario: FEAT-040-002 Phase 1b is blocked (HEART enriched fails after 7 iterations). The blocking_behavior says "proceed with gap noted." But the synthesis handoff artifact list includes `ux-heart-analyst-output.md` (authoritative), not the provisional. The ps-synthesizer would receive a path to a non-existent file. The FM-003 pre-synthesis artifact check (in .md Runtime Behavior step 22) would catch this — but the resolution path is unclear: should it fall back to the provisional HEART artifact, or is synthesis without authoritative HEART invalid?

This is less severe because the FM-003 check creates a pause point. However, the YAML QG-1B blocking behavior should explicitly state: "If FEAT-040-002 Phase 1b blocked: synthesis falls back to provisional HEART artifact (Phase 1a output); synthesis handoff substitutes `ux-heart-analyst-provisional-output.md` for `ux-heart-analyst-output.md`."

**Recommendation:**

Add a conditional to `barriers.QG-1B.blocking_behavior`:
```yaml
special_case_FEAT_040_002_blocked: >
  If FEAT-040-002 (HEART enriched) is blocked: synthesis uses Phase 1a provisional artifact
  (ux-heart-analyst-provisional-output.md) as fallback. Synthesizer handoff substitutes
  provisional path. Flag as partial input in synthesis.
```

Also update `barriers.QG-3.synthesis_inputs` to use a notation that accommodates the fallback, or add a `synthesis_inputs_fallback` list.

---

### FM-FS-005: `resumption.load_order` Does Not Include State Directory

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | YAML `resumption.load_order` |
| **Strategy Step** | S-011 Chain-of-Verification (completeness verification) |

**Evidence:**

YAML `resumption.load_order`:
```yaml
load_order:
  - path: "projects/PROJ-040-documentation/ORCHESTRATION.yaml"
  - path: "projects/PROJ-040-documentation/orchestration/plans/wave-1-discovery-plan.md"
  - path: "projects/PROJ-040-documentation/WORKTRACKER.md"
  - path: "projects/PROJ-040-documentation/reports/diataxis-audit-20260420.md"
  - path: "projects/PROJ-040-documentation/PLAN.md"
```

`resumption.session_resume_note` instructs: "Skip features in state=complete EXCEPT FEAT-040-002: check `phase_completions`." Checking `phase_completions` requires reading `orchestration/state/FEAT-040-002.yaml`. The load_order does not include the state directory or any state file path.

The `execution_queue.pre_wave_initialization.state_files_initialized: false` indicates state files will not exist at first load, so a static reference is not always valid. However, the load_order is the session resume guide — when resuming mid-wave, state files will exist and must be consulted.

**Analysis:**

An orchestrator following only `load_order` on resume would load ORCHESTRATION.yaml, the plan, WORKTRACKER.md, the audit, and PLAN.md — but would not know to read the state directory. The `session_resume_note` in the same section does say to check checkpoints and state files, but `load_order` should explicitly enumerate the state directory as a resume input.

**Recommendation:**

Add to `resumption.load_order`:
```yaml
- path: "projects/PROJ-040-documentation/orchestration/state/"
  purpose: "Feature state files — read all FEAT-040-NNN.yaml to reconstruct execution state; required for resume"
  note: "Directory glob: read all .yaml files present; empty on fresh start"
- path: "projects/PROJ-040-documentation/orchestration/checkpoints/"
  purpose: "Phase checkpoints — read most recent for resume point identification"
  note: "Sort by timestamp; empty on fresh start"
```

---

## Per-Strategy Results

### S-010: Self-Refine

**Applied to:** Full deliverable set (both files together)

The deliverables are internally consistent and evidence thorough self-correction. The YAML mirrors the .md with high fidelity — 37/37 claims verified. The revision log in the .md demonstrates the creator-critic-revision cycle was executed (iter-1 through iter-4 changes documented). The Consistency Audit appendix (iter-4) proves a structured self-review protocol was applied before writing. The YAML's comment density is high, supporting human readability.

**Self-refine observations:**
- The creator correctly identified the recurring regression pattern (adding a Consistency Audit appendix)
- State file schema is detailed and complete
- Cross-pollination catalog (7 XP points) is well-structured

**Finding:** FM-FS-001 (Major) was not self-identified despite being mechanically checkable (compare strategy_sets vs quality-enforcement.md table). This is the core failure mode self-refine was meant to catch.

### S-003: Steelman

**Strongest arguments for the deliverable set quality:**

1. **Architectural completeness:** The YAML is the most complete and detailed orchestration state file seen across all iterations. It covers pre-execution initialization (H-32 parity check), resume protocols, metrics with timing fields, failure fallback paths, XP enrichment tracking, and checkpoint enumeration. This level of completeness makes the orchestration executable from cold start.

2. **Cross-file discipline:** The 37/37 consistency check across 37 distinct claims demonstrates that both files were authored and reviewed as a coherent unit. No structural drift between .md and .yaml — all threshold values, feature IDs, gate names, and path templates match exactly.

3. **Constitutional constraint encoding:** The `workflow.constraints` block encodes P-003, P-002, P-020, H-13, H-14, RT-M-010 explicitly with comments tracing each constraint to its source rule. This is an exemplary practice that future orchestration plans should follow.

4. **Resumption robustness:** The FEAT-040-002 dual-pass `phase_completions` field + resume guard is a sophisticated solution to the specific context-compaction risk. The YAML captures this at the agent level (in the Phase 1b HEART entry) and at the execution_queue level (pass_type: enriched_authoritative), giving the orchestrator two independent places to check.

5. **Adversarial feedback integration:** The Revision Log demonstrates 4 full tournament iterations absorbed 25+ findings from iterative critique. The YAML encodes the final state of those resolutions.

### S-002: Devil's Advocate

**Challenges to the deliverable set's adequacy:**

1. **The C3 strategy underspecification (FM-FS-001) is not a minor gap.** 13 features are C3-classified. The constitution's C3 required set includes S-012 (FMEA) and S-013 (Inversion) precisely because C3 deliverables have >10 file impact and need systematic failure enumeration and "what if we inverted this?" analysis. Excluding these from the 13 upstream deliverables means the synthesis feeds on inputs that have not been subjected to the constitution's mandated scrutiny level. The QG-3 synthesis tournament cannot compensate for gaps in its inputs.

2. **The `execution_queue.pending` pattern creates a false sense of completeness.** FEAT-040-057 (synthesis) appears in `pending_phase_3` but there is no entry for it as a pipeline agent. A reader scanning `pipelines` would not see synthesis at all. The YAML comment explains this ("Synthesis is NOT a pipeline") but this design choice means synthesis has no `quality_threshold`, `iteration_ceiling`, or `criticality` declared at the agent level — all synthesis quality parameters are in barriers.QG-3. This creates a fragmented configuration: synthesis parameters are in three locations (barriers.QG-3, adversarial.C4_synthesis, adversarial.quality) with some duplication.

3. **YAML `metrics.execution.phases_total: 5` may be misleading.** The plan identifies Phase 1a, Phase 1b, Phase 2 (QG-2 + QG-2.5), Phase 3 (synthesis), and QG-3 (exit gate) as "5 phases." But Phase 2 contains two gates (QG-2 and QG-2.5) which have different agents, protocols, and failure modes. Treating them as one "phase" in the metrics counter could cause orchestrators reading the metrics to conflate their separate completion states.

4. **The H-32 GitHub Issue Parity pre-check is scoped to `geekatron/jerry` repo only** (per .md step 0). The execution_queue also includes this scoping. But the worktracker entities (FEAT-040-NNN) are in a worktree (`feat/proj-040-documentation`). An executor reading the YAML might not check the repo name and skip the H-32 step. The guard is present but fragile — it depends on the executor running `gh repo view` before deciding whether to create issues.

### S-007: Constitutional AI Critique

**Principles checked:**

| Principle | Requirement | YAML/MD Compliance |
|-----------|-------------|-------------------|
| H-01 / P-003 | max_agent_nesting: 1; no recursive subagents | COMPLIANT — documented in workflow.constraints; P-003 compliance note in .md |
| H-02 / P-020 | User authority; approval required for destructive ops | COMPLIANT — user_authority: true in constraints; escalation protocols documented |
| H-03 / P-022 | No deception about capabilities | COMPLIANT — disclaimer on both files; provisional HEART flagged explicitly |
| H-13 | Quality threshold >= 0.92 for C2+ | PARTIAL — 0.92 threshold correct; C3 strategy set incomplete (FM-FS-001) |
| H-14 | min_critic_iterations: 3 | COMPLIANT — min_iterations: 3 in QG-3 and min_critic_iterations in constraints |
| H-16 | Steelman before Devil's Advocate | COMPLIANT — h16_enforced: true; canonical_sequence has S-003 at position 2 |
| H-17 | Quality scoring required for all C2+ | COMPLIANT — S-014 listed as required for all features |
| H-18 | Constitutional compliance check (S-007) | PARTIAL — S-007 is listed as optional for C3 features when it should be required at C3 (FM-FS-001) |
| H-32 | GitHub Issue parity for jerry repo | COMPLIANT — step 0 protocol with repo guard |
| RT-M-010 | Iteration ceilings C3=7, C4=10 | COMPLIANT — matches exactly |
| P-002 | File persistence | COMPLIANT — file_persistence: true; all outputs have declared paths |

**Constitutional violation confirmed:** H-18 (S-007 constitutional compliance check required) is violated for C3 features. S-007 is listed as optional in `C3_per_feature` but the quality-enforcement.md C3 required set includes all C2 required strategies (which include S-007). This reinforces FM-FS-001.

### S-004: Pre-Mortem

**"Wave 1 execution began. It failed. What went wrong?"**

**Failure scenario 1 (most likely):** FEAT-040-002 HEART enriched (Phase 1b) is blocked at iteration 7 without converging. The YAML blocking_behavior says "proceed with gap noted," but the synthesis handoff artifact list references the non-existent authoritative file. The FM-003 pre-synthesis check catches this, but the orchestrator has no documented resolution path: use provisional? Skip HEART? The synthesis arrives at ps-synthesizer with a gap that was not anticipated in the synthesis success criteria. This is FM-FS-004.

**Failure scenario 2 (execution-time):** An executor automating against ORCHESTRATION.yaml reads `adversarial.quality.required_strategies` (flat list of 10) rather than `adversarial.strategy_sets.C3_per_feature.required` (list of 3). The executor applies all 10 strategies to every C3 feature — dramatically increasing cost and session duration — or is confused about which list takes precedence. FM-FS-002 is the root.

**Failure scenario 3 (session resume):** Session ends after Phase 1a QG-1A passes. On resume, the orchestrator reads load_order (ORCHESTRATION.yaml → plan → WORKTRACKER → audit → PLAN.md) but does not read state files. FEAT-040-002 has `phase_completions: ["1a-provisional"]` but without reading the state file, the orchestrator doesn't know Phase 1b enriched pass is outstanding. FM-FS-005 is the root.

**Failure scenario 4 (governance):** An auditor checks whether the orchestration plan complies with the constitution's C3 strategy requirements. They check `adversarial.strategy_sets.C3_per_feature.required` and find only 3 strategies listed. They flag a non-compliance finding. The plan cannot demonstrate constitutional compliance for C3 features because the required strategies are absent. This prevents formal acceptance of the plan. FM-FS-001 is the root.

### S-012: FMEA

**Failure Mode Enumeration (new surface — YAML-specific):**

| Failure Mode | Effect | S | O | D | RPN | Finding |
|-------------|--------|---|---|---|-----|---------|
| C3 strategy underspec | 13 features receive 3-strategy review vs required 6 | 8 | 8 | 7 | 448 | FM-FS-001 |
| `required_strategies` scope ambiguity | Executor applies wrong strategy set; wrong cost or wrong features reviewed | 5 | 4 | 7 | 140 | FM-FS-002 |
| P-043 non-existent principle | Audit trail references unresolvable principle; traceability chain broken | 3 | 3 | 8 | 72 | FM-FS-003 |
| HEART blocked: no fallback path in YAML | Synthesis receives invalid artifact path; FM-003 catches but no documented resolution | 6 | 3 | 7 | 126 | FM-FS-004 |
| load_order missing state directory | Resume skips phase_completions check; FEAT-040-002 Phase 1b re-run missed | 7 | 3 | 6 | 126 | FM-FS-005 |
| YAML metrics.phases_total=5 conflates QG-2+QG-2.5 | Dashboard shows wrong completion percentage; phase-2 conflation masks QG-2.5 pending state | 4 | 5 | 7 | 140 | (New — see below) |

**Additional FMEA finding (Minor):**

`metrics.execution.phases_total: 5` counts "Phase 1a, Phase 1b, Phase 2 (QG-2+QG-2.5), Phase 3, QG-3 exit" as 5 phases. But QG-2 and QG-2.5 are separate barrier evaluations with different agents, separate checkpoints (`phase-2-xp-checkpoint.yaml` and `phase-2-fidelity-checkpoint.yaml`), and distinct pass/fail conditions. If the metrics counter increments "phases_complete" at "Phase 2 complete" without distinguishing QG-2 and QG-2.5 completion, the tracker would show `phases_complete: 2` when only QG-2 passed and QG-2.5 is still pending. This is a low-severity metrics ambiguity. Recommend either changing `phases_total: 6` (splitting Phase 2 into QG-2 and QG-2.5) or adding explicit `barriers_complete` tracking (already present — `barriers_total: 5`, `barriers_complete: 0`) with a note that barrier completion is the authoritative completion signal, not phase count.

**RPN Assessment:** FM-FS-001 dominates at RPN 448. All other findings are in the 72-140 range. No new Critical-severity failure modes identified in the YAML-specific surface.

### S-013: Inversion

**"What would need to be true for this YAML to guarantee Wave 1 executes correctly?"**

Inverting the problem: what is the YAML optimized for, and what does it NOT protect?

**Optimized for:**
- Session resume with no data loss (extensive checkpoint enumeration, resumption block)
- Cross-file consistency (paths/ids match .md exactly)
- P-003 compliance encoding (constraint block)
- C4 synthesis quality (all 10 strategies, correct threshold, H-16 enforcement)

**NOT protected by the YAML (inversion findings):**

1. **C3 per-feature quality depth** — The YAML does not protect against C3 features being under-reviewed. The C3_per_feature strategy set is too thin (FM-FS-001). This is the inverse of the YAML's thoroughness at C4.

2. **Synthesis inputs validity on partial Phase 1b** — The YAML does not define a synthesizer behavior when Phase 1b produces blocked features (FM-FS-004). The assumption baked into `barriers.QG-3.synthesis_inputs` is that all 12 files will exist.

3. **Automated YAML parsing correctness** — The YAML does not protect against an executor reading `adversarial.quality.required_strategies` rather than `adversarial.strategy_sets.C3_per_feature.required` (FM-FS-002).

4. **Principle traceability** — P-043 is not resolvable (FM-FS-003). The YAML cannot guarantee its own disclaimer traceability.

**Inversion conclusion:** The YAML is a strong machine-readable state file that optimizes for resume correctness, C4 synthesis quality, and cross-file consistency. Its primary gap is that it does not protect the C3 per-feature quality path with the same rigor it applies to C4 synthesis. The inversion reveals an asymmetry in quality ambition: C4 gets all 10 strategies; C3 gets 3.

### S-011: Chain-of-Verification

**Verification chain for key claims:**

**Claim 1:** "All 9 Phase 1a features are enumerated in the YAML."
- MD claims: 9 features in Phase 1a
- YAML pipelines.ux.phases[1a]: 7 agents (001, 002, 004, 005, 006, 007, 008)
- YAML pipelines.pm.phases[1a]: 1 agent (055)
- YAML pipelines.research.phases[1a]: 1 agent (056)
- Sum: 7 + 1 + 1 = 9 ✓ VERIFIED

**Claim 2:** "QG-1A requires all 9 Phase 1a features."
- YAML barriers.QG-1A.features_required: [001, 002, 004, 005, 006, 007, 008, 055, 056] = 9 entries
- Match with pipeline Phase 1a agents: ✓ VERIFIED

**Claim 3:** "FEAT-040-057 synthesis is properly configured in the YAML."
- execution_queue.pending_phase_3[0].feature_id: FEAT-040-057 ✓
- barriers.QG-3.features_required: [FEAT-040-057] ✓
- barriers.QG-3.synthesis_inputs: 12 paths listed ✓
- 12 paths verified against pipeline agent artifact_path fields: all 12 match ✓ VERIFIED

**Claim 4:** "H-16 (Steelman before Devil's Advocate) is enforced in the YAML."
- adversarial.C4_synthesis.h16_enforced: true ✓
- canonical_sequence: ["S-010", "S-003", "S-002", ...] — S-003 at position 2, S-002 at position 3 ✓ VERIFIED

**Claim 5:** "C3 per-feature strategy set complies with quality-enforcement.md."
- YAML C3_per_feature.required: [S-010, S-002, S-014]
- quality-enforcement.md C3 required: S-007, S-002, S-014, S-004, S-012, S-013
- Missing: S-007, S-004, S-012, S-013 ✗ FAILED — FM-FS-001

**Claim 6:** "Resumption load_order is sufficient to resume mid-wave execution."
- load_order[0]: ORCHESTRATION.yaml ✓ (state SSOT)
- load_order[1]: wave-1-discovery-plan.md ✓ (protocol)
- load_order[2]: WORKTRACKER.md ✓ (status)
- load_order[3]: diataxis-audit-20260420.md ✓ (baseline)
- load_order[4]: PLAN.md ✓ (architecture)
- MISSING: orchestration/state/ directory ✗ — needed for phase_completions check, cannot resume correctly without it — FM-FS-005

**Claim 7:** "Disclaimer is present and traceable on both files."
- .md Disclaimer section: ✓ present
- YAML disclaimer comment: ✓ present
- P-043 reference: ✗ not traceable to any defined principle — FM-FS-003

**Chain-of-Verification result:** 5/7 claims fully verified. 2 failed (C3 strategy compliance, load_order completeness). 1 partially failed (disclaimer traceability).

### S-001: Red Team

**Attack surface: "How would a malicious reviewer or a confused executor misuse the YAML?"**

**Attack vector 1 — Strategy substitution:** An executor parsing YAML reads `adversarial.quality.required_strategies` (all 10) and applies all 10 to every C3 feature, dramatically increasing execution cost and session length. This is not malicious but would be incorrect behavior caused by FM-FS-002. The executor has no YAML-level mechanism to determine which strategy set applies to which feature beyond reading the strategy_sets block.

**Attack vector 2 — Resume manipulation:** An executor skipping the `resumption.session_resume_note` and only following `load_order` would miss the FEAT-040-002 phase_completions check and would treat Phase 1a completion as Phase 1b completion for HEART, resulting in synthesis receiving provisional (not authoritative) HEART output without flagging the gap.

**Attack vector 3 — Threshold circumvention:** The YAML allows "proceed with gap noted" at QG-1B for blocked features. A fast-moving executor could proceed to synthesis with multiple blocked Phase 1b features, relying on "gap noted" language to justify rushing to synthesis. The language does not specify a maximum number of Phase 1b gaps before proceeding becomes invalid.

**Attack vector 4 — P-043 fabrication:** Since P-043 is not defined anywhere, the disclaimer compliance statement is unfalsifiable. Any disclaimer text could claim "P-043 compliance" without any verification mechanism.

**Red Team finding (Minor):** QG-1B `blocking_behavior` should add a maximum-gaps clause: "If more than [N] Phase 1b features are blocked, escalate to user before proceeding to Phase 2" to prevent gap-accumulation circumvention. Current text has no upper bound on "proceed with gap noted" logic.

---

## S-014 Scoring

### LLM-as-Judge: 6-Dimension Rubric

**Target:** Full deliverable set (`.md` + `.yaml`) — cross-file consistency and YAML-specific requirements

**Scope note:** The `.md` was scored at 0.972 in iter-4. This iteration scores the full set against the new surface probed. Scores below represent the full-set assessment including the YAML and cross-file surface.

| Dimension | Weight | Score | Weighted | Rationale |
|-----------|--------|-------|---------|-----------|
| **Completeness** | 0.20 | 0.95 | 0.190 | All 13 YAML sections present; all orch-planner must clauses satisfied except C3 strategy underspec; 37/37 cross-file claims verified |
| **Internal Consistency** | 0.20 | 0.97 | 0.194 | Zero cross-file mismatches; all IDs, thresholds, paths, gate names match; the `required_strategies` ambiguity (FM-FS-002) is a minor notation gap, not a structural inconsistency |
| **Methodological Rigor** | 0.20 | 0.88 | 0.176 | C3 strategy underspecification (FM-FS-001) is the primary deduction; C4 methodology is exemplary; S-007 constitutional check missing for C3 (H-18 violation per constitution) |
| **Evidence Quality** | 0.15 | 0.96 | 0.144 | Extensive source citations in YAML comments; all constraints trace to rules; disclaimer gap (FM-FS-003) is minor |
| **Actionability** | 0.15 | 0.95 | 0.143 | YAML is highly actionable for execution; execution_queue is complete; load_order gap (FM-FS-005) is the only actionability deduction; runtime steps map cleanly to YAML entries |
| **Traceability** | 0.10 | 0.92 | 0.092 | H-32, P-003, P-002, H-16 all traced; P-043 unresolvable reference; FEAT-040-002 dual-pass traceability exemplary |

**Composite Score: 0.939**

**Band: REVISE (0.85-0.91 range revised upward — see note)**

Wait — let me recompute: 0.190 + 0.194 + 0.176 + 0.144 + 0.143 + 0.092 = **0.939**

This falls in the REVISE band (0.85-0.91 per quality-enforcement.md) — actually 0.939 is above 0.92 threshold but below the C4 0.95 threshold. Per quality-enforcement.md: PASS requires >= 0.92 for C2+, and >= 0.95 for C4. Since this is a C4 deliverable (QG-3 synthesis planning), the threshold is **0.95**.

**0.939 < 0.95 → REVISE (below C4 threshold)**

The single scoring deduction driving below 0.95: Methodological Rigor at 0.88 due to FM-FS-001 (C3 strategy underspecification). If FM-FS-001 is resolved (correct C3 strategy set), Methodological Rigor rises to approximately 0.96, producing a composite of approximately 0.955 — above the 0.95 C4 threshold.

---

## Verdict

**Score: 0.939 / 0.95 threshold → REVISE**

**Status: Below C4 threshold. One Major finding (FM-FS-001) must be resolved before the full-set passes at C4.**

### Top 3 Blockers

**Blocker 1 (Major — FM-FS-001):** C3 per-feature strategy set underspecifies quality-enforcement.md C3 required strategies. Both files list only S-010, S-002, S-014 as required for the 13 C3 features when the constitution requires S-007, S-002, S-014, S-004, S-012, S-013. Fix: update YAML `adversarial.strategy_sets.C3_per_feature.required` to add S-007, S-004, S-012, S-013; update .md Quality Review Protocol correspondingly. This is the sole deduction preventing a C4 PASS.

**Blocker 2 (Minor — FM-FS-004):** QG-1B blocking behavior lacks a documented fallback path for the FEAT-040-002 HEART blocked case. If authoritative HEART fails, synthesis receives a bad artifact path; no YAML entry specifies whether to use provisional HEART instead. Fix: add `special_case_FEAT_040_002_blocked` entry to QG-1B barrier.

**Blocker 3 (Minor — FM-FS-005):** `resumption.load_order` omits `orchestration/state/` directory. On resume, the FEAT-040-002 `phase_completions` check requires reading FEAT-040-002.yaml, which is not in load_order. Fix: add state directory and checkpoints directory entries to load_order.

---

### Remaining Minor Findings (non-blocking)

- **FM-FS-002** (Minor): `adversarial.quality.required_strategies` scope ambiguity — rename or scope-annotate the field
- **FM-FS-003** (Minor): P-043 principle code in YAML disclaimer is unresolvable — replace with direct orch-planner spec reference
- **FMEA-metrics** (Minor): `metrics.execution.phases_total: 5` conflates QG-2 and QG-2.5 — either increment to 6 or add note that `barriers_complete` is the authoritative completion signal

---

## Execution Statistics

- **Total Findings:** 6
- **Critical:** 0
- **Major:** 1 (FM-FS-001)
- **Minor:** 5 (FM-FS-002, FM-FS-003, FM-FS-004, FM-FS-005, FMEA-metrics)
- **Cross-file claims verified:** 37/37 (zero mismatches)
- **YAML schema sections present:** 13/13
- **orch-planner must clauses satisfied:** 12/13 (C3 strategy spec is the partial)
- **Protocol steps completed:** 10 of 10 (S-010 through S-014)
- **Composite score:** 0.939
- **C4 threshold (0.95):** NOT MET
- **C2+ threshold (0.92):** MET

---

*Strategy Execution Report: Wave 1 Full-Set Adversarial Tournament — Remediation Iter-1*
*Executed: 2026-04-17*
*Agent: adv-executor*
*Constitutional Compliance: P-001 (evidence-based), P-002 (persisted), P-003 (no recursion), P-004 (provenance), P-011 (evidence-cited), P-022 (honest verdict)*
