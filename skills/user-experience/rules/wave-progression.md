<!-- VERSION: 1.2.0 | DATE: 2026-03-04 | SOURCE: SKILL.md (skills/user-experience/SKILL.md) Sections "Wave Architecture", "Wave Transition Quality Gates", "Wave Signoff Enforcement" | PARENT: /user-experience skill | REVISION: Build-phase convention note for signoff file locations; build-phase evidence distinction in Per-Transition Requirements Wave 2 → 3 -->

# Wave Progression Rules

> Criteria-gated wave deployment rules for the /user-experience skill. Defines wave transition quality gates, bypass mechanism, signoff requirements, and wave state tracking. See also: `skills/user-experience/rules/ux-routing-rules.md` (wave-aware routing and bypass routing), `skills/user-experience/rules/synthesis-validation.md` (synthesis quality dependent on wave-deployed sub-skills), `skills/user-experience/rules/mcp-coordination.md` (MCP availability affecting wave deployment readiness), `skills/user-experience/rules/ci-checks.md` (CI gates UX-CI-007 and UX-CI-008 that validate signoff files).

## Document Sections

| Section | Purpose |
|---------|---------|
| [Wave Definitions](#wave-definitions) | 6 waves (0-5) with sub-skills and entry criteria |
| [Wave Transition Gates](#wave-transition-gates) | Quality thresholds and evidence requirements per transition |
| [Signoff Requirements](#signoff-requirements) | What must exist before the next wave begins |
| [Bypass Mechanism](#bypass-mechanism) | 3-field bypass documentation process |
| [Wave State Tracking](#wave-state-tracking) | How wave deployment state is persisted and queried |
| [Wave Transition Workflow](#wave-transition-workflow) | Step-by-step transition process |

---

## Wave Definitions

<!-- Source: SKILL.md Section "Wave Architecture" (lines 254-269) — wave deployment model. ADR-PROJ022-001 (projects/PROJ-022-user-experience-skill/decisions/ADR-PROJ022-001-ux-skill-architecture.md, PROVISIONAL) provides architectural rationale for the criteria-gated wave approach: 10 pluggable sub-skills across 5 criteria-gated waves with P-003 single-level nesting. Wave 5 AI-First CONDITIONAL criteria (WSM >= 7.80, Enabler DONE) are sourced from SKILL.md Wave Architecture table line 267; the WSM 7.80 threshold is provisionally derived from Weighted Scoring Matrix calibration in PROJ-020 C4 tournament evidence — to be validated during EPIC-001. -->

Waves are **deployment phases** for incremental skill build-out, not runtime execution order. At runtime, the orchestrator routes to any deployed sub-skill based on user need.

| Wave | Name | Sub-Skills | Entry Criteria | Bypass Condition |
|------|------|-----------|----------------|-----------------|
| **0** | Foundation | `ux-orchestrator` + rules + templates | PROJ-022 plan approved | N/A |
| **1** | Zero-Dependency | `/ux-heuristic-eval`, `/ux-jtbd` | KICKOFF-SIGNOFF.md completed with MCP ownership assignments | N/A (first wave) |
| **2** | Data-Ready | `/ux-lean-ux`, `/ux-heart-metrics` | Wave 1: at least 1 heuristic eval completed AND 1 JTBD job statement used in a product decision | 2 sprint cycles elapsed with no Wave 1 completion; documented rationale |
| **3** | Design System | `/ux-atomic-design`, `/ux-inclusive-design` | Wave 2: launched product with analytics OR 1 completed Lean UX hypothesis cycle | Storybook already in use (skip Lean UX prerequisite for Atomic Design) |
| **4** | Advanced Analytics | `/ux-behavior-design`, `/ux-kano-model` | Wave 3: Storybook with 5+ Atom stories AND 1 Persona Spectrum review | Existing user base with analytics (skip Persona Spectrum prerequisite) |
| **5** | Process Intensives | `/ux-design-sprint`, `/ux-ai-first-design` (COND) | Wave 4: 30+ users for Kano survey OR 1 B=MAP bottleneck diagnosed; AI-First: Enabler DONE + WSM >= 7.80 | Design Sprint can proceed without Kano prerequisite if team has existing user research |

---

## Wave Transition Gates

<!-- Source: SKILL.md Section "Wave Transition Quality Gates" (lines 271-283). -->
<!-- Threshold derivation: ADR-PROJ022-002-wave-criteria-gates.md (projects/PROJ-022-user-experience-skill/decisions/ADR-PROJ022-002-wave-criteria-gates.md, PROVISIONAL). Derivation: 0.85 sits at the REVISE band boundary in quality-enforcement.md (0.85-0.91 = structurally complete, minor gaps); below 0.85 enters REJECTED band. Threshold distinct from H-13's 0.92 because wave gates assess operational output quality, not governance artifact quality. Calibration plan: post-Wave-1 user satisfaction data informs threshold revision (max 0.92). See ADR-PROJ022-002 Decision section. -->

Each wave transition is a quality checkpoint. The orchestrator checks `WAVE-{N}-SIGNOFF.md` existence before routing to Wave N+1 sub-skills.

### Threshold

**0.85** S-014 weighted composite for wave transition quality gates.

This threshold is distinct from H-13's 0.92 for governance artifacts. Wave gates assess sub-skill *operational output quality* (deployment readiness), not governance artifact quality. See `ADR-PROJ022-002-wave-criteria-gates.md` (`projects/PROJ-022-user-experience-skill/decisions/ADR-PROJ022-002-wave-criteria-gates.md`) for provisional threshold derivation. **ADR status: PROVISIONAL** — the 0.85 threshold is derived from the quality-enforcement.md REVISE band boundary (0.85-0.91: structurally complete output with minor gaps). Calibration plan: after Wave 1 deployment, measure whether sub-skills scoring 0.85-0.91 produce acceptably useful output; if not, revise threshold upward (maximum 0.92, aligning with H-13). Calibration is tracked in PROJ-022 worktracker as Enabler "Wave Gate Threshold Calibration" (post-Wave-1). When ADR-PROJ022-002 is baselined, the threshold may be revised; if revised, update this file and re-validate `ci-checks.md` gates UX-CI-007 and UX-CI-008.

### Per-Transition Requirements

| Transition | Quality Check | Threshold | Additional Evidence | Source |
|-----------|---------------|-----------|-------------------|--------|
| Wave 0 → 1 | KICKOFF-SIGNOFF.md completeness | All fields populated (pass/fail) | MCP ownership assignments present | SKILL.md "Wave Transition Quality Gates" line 277; SKILL.md "Wave Architecture" Wave 1 entry criteria |
| Wave 1 → 2 | Wave 1 deliverables quality scoring | S-014 composite >= 0.85 on heuristic eval report | At least 1 heuristic eval completed AND 1 JTBD job statement used | SKILL.md "Wave Transition Quality Gates" line 278; ADR-PROJ022-002 (PROVISIONAL) for 0.85 threshold; Wave 2 entry criteria from SKILL.md Wave Architecture table |
| Wave 2 → 3 | Wave 2 deliverables + usage evidence | S-014 composite >= 0.85 | Documented usage artifact (product launch OR hypothesis cycle). **Build-phase note:** During skill build orchestrations, "usage evidence" refers to deployment readiness (complete agent definitions, methodology rules, templates, governance YAML, and cross-framework synthesis tests). Operational-usage evidence (actual hypothesis cycle or product launch) is produced when sub-skills are first invoked against a real project engagement and is tracked as PENDING in the signoff until produced. | SKILL.md "Wave Transition Quality Gates" line 279; Wave 3 entry criteria from SKILL.md Wave Architecture table |
| Wave 3 → 4 | Wave 3 deliverables + Storybook artifact | S-014 composite >= 0.85 | Storybook story count verification (5+ Atom stories) | SKILL.md "Wave Transition Quality Gates" line 280; Wave 4 entry criteria from SKILL.md Wave Architecture table |
| Wave 4 → 5 | Wave 4 deliverables + user data evidence | S-014 composite >= 0.85 | User count (30+) or behavioral data artifact | SKILL.md "Wave Transition Quality Gates" line 281; Wave 5 entry criteria from SKILL.md Wave Architecture table |

### Scoring Dimensions

Wave gate scoring uses the same S-014 6-dimension rubric as H-13, with weights:

| Dimension | Weight |
|-----------|--------|
| Completeness | 0.20 |
| Internal Consistency | 0.20 |
| Methodological Rigor | 0.20 |
| Evidence Quality | 0.15 |
| Actionability | 0.15 |
| Traceability | 0.10 |

---

## Signoff Requirements

<!-- Source: SKILL.md Section "Wave Signoff Enforcement" (lines 287-291). Signoff files are validated by CI gates UX-CI-007 (Signoff File Structure) and UX-CI-008 (Signoff Ordering) defined in `skills/user-experience/rules/ci-checks.md`. -->

### Signoff File Locations

| Wave | Signoff File | Location |
|------|-------------|----------|
| Foundation | KICKOFF-SIGNOFF.md | `projects/${JERRY_PROJECT}/engagements/KICKOFF-SIGNOFF.md` |
| Wave 1 | WAVE-1-SIGNOFF.md | `projects/${JERRY_PROJECT}/engagements/WAVE-1-SIGNOFF.md` |
| Wave 2 | WAVE-2-SIGNOFF.md | `projects/${JERRY_PROJECT}/engagements/WAVE-2-SIGNOFF.md` |
| Wave 3 | WAVE-3-SIGNOFF.md | `projects/${JERRY_PROJECT}/engagements/WAVE-3-SIGNOFF.md` |
| Wave 4 | WAVE-4-SIGNOFF.md | `projects/${JERRY_PROJECT}/engagements/WAVE-4-SIGNOFF.md` |
| Wave 5 | WAVE-5-SIGNOFF.md | `projects/${JERRY_PROJECT}/engagements/WAVE-5-SIGNOFF.md` |

> **Build-phase convention:** During skill build orchestrations (e.g., PROJ-022), signoff files are created at `skills/user-experience/work/WAVE-{N}-SIGNOFF.md` alongside other build-phase work artifacts. The `projects/${JERRY_PROJECT}/engagements/` paths above are the canonical operational locations used by CI gates (UX-CI-007, UX-CI-008) and wave state detection in production. Signoff files are moved to `engagements/` when the skill build is finalized and the skill transitions from build phase to operational phase. Both Wave 1 and Wave 2 signoffs follow this build-phase convention.

### Signoff File Validation

A signoff file is valid when:

1. **Schema completeness:** All required fields are non-empty (date, signed off by, sub-skills deployed table, quality gate result, artifacts verified table, acceptance criteria checklist).
2. **Quality gate pass:** Composite score >= 0.85 for all sub-skills in the wave. (Source: ADR-PROJ022-002, PROVISIONAL; quality-enforcement.md REVISE band boundary.)
3. **Acceptance criteria met:** All acceptance criteria checkboxes are checked.
4. **Bypass resolution:** No unresolved bypasses for the completing wave (active bypasses block signoff).
5. **Repository committed:** The signoff file is committed to the repository (wave completion is not recognized until committed).

> **Elaboration note:** These 5 conditions elaborate on SKILL.md "Wave Signoff Enforcement" (line 289), which states "`WAVE-N-SIGNOFF.md` is a closure deliverable -- wave completion is not recognized until the signoff file passes schema validation (all required fields non-empty) and is committed to the repository." Conditions 1 and 5 map directly to SKILL.md's stated requirements. Conditions 2, 3, and 4 are operational elaborations consistent with SKILL.md's intent, added here to make validation criteria explicit and CI-testable.

**CI enforcement:** Signoff file structure is validated at CI by gate UX-CI-007 (Signoff File Structure) and signoff ordering is validated by gate UX-CI-008 (Signoff Ordering), both defined in `skills/user-experience/rules/ci-checks.md`.

### Templates

- Kickoff signoff: `skills/user-experience/templates/kickoff-signoff-template.md`
- Wave signoff: `skills/user-experience/templates/wave-signoff-template.md`

---

## Bypass Mechanism

<!-- Source: SKILL.md Section "Wave Architecture" (lines 285-286) — bypass mechanism. Bypass fields (unmet criterion, impact assessment, remediation plan), cumulative ceiling (max 2), and warning banner requirement all sourced from SKILL.md. -->

Wave bypass allows routing to a sub-skill whose wave has not been formally signed off. Bypass requires user-approved 3-field documentation per P-020.

### Bypass Fields

| Field | Description | Example |
|-------|------------|---------|
| **Unmet Criterion** | Which wave entry criterion is not met | "No completed heuristic evaluation from Wave 1" |
| **Impact Assessment** | Risk of proceeding without this criterion | "Sprint proceeds without prior framework calibration; findings may lack comparative baseline" |
| **Remediation Plan** | How the unmet criterion will be satisfied, and by when | "Backfill Wave 1 heuristic evaluation within 2 sprints of Design Sprint completion" |

### Bypass Documentation

Bypass documentation is persisted at `projects/${JERRY_PROJECT}/engagements/{engagement-id}/wave-bypass-{wave-N}.md`. See `ux-routing-rules.md` [Bypass Routing] for full documentation structure.

> **Path scoping rationale:** Bypass files are engagement-scoped (contain `{engagement-id}`) because the same wave may be bypassed differently in separate engagements -- each engagement has its own unmet criterion, impact assessment, and remediation plan. Signoff files (see [Signoff File Locations](#signoff-requirements)) are project-scoped (no engagement-id) because wave completion is a project-wide state change: once a wave is signed off, it is deployed for all future engagements.

### Bypass Constraints

| Constraint | Rule | Rationale |
|-----------|------|-----------|
| **Cumulative ceiling** | Maximum 2 concurrent bypasses per team (provisional; source: SKILL.md "Wave Architecture" line 285; calibration guidance tracked in ADR-PROJ022-002, PROVISIONAL) | Prevents accumulation of technical UX debt through unbounded wave skipping. The value of 2 balances flexibility (allowing teams to skip ahead when business need is urgent) against debt accumulation (more than 2 concurrent bypasses creates compounding remediation obligations). Value is provisional pending Wave 1-2 deployment data. |
| **Warning banner** | All outputs produced under bypass carry: "[WAVE BYPASS] This output was produced before Wave {N} entry criteria were met." | P-022 compliance: users know the output lacks wave prerequisites |
| **Signoff blocking** | A wave signoff cannot complete if it has unresolved bypasses for that wave | Forces remediation before wave closure |
| **User approval** | User must explicitly approve each bypass (P-020) | No automatic bypasses; user decides whether to accept the risk |

### Bypass Lifecycle

1. **Request:** User's intent routes to a sub-skill whose wave is not deployed.
2. **Inform:** Orchestrator discloses wave unavailability per P-022.
3. **Prompt:** Orchestrator presents 3-field bypass prompt -- the prompt displays the template fields (Unmet Criterion, Impact Assessment, Remediation Plan) and requires user completion before proceeding. See `ux-routing-rules.md` [Bypass Routing] for full prompt structure.
4. **Document:** User provides 3 fields; orchestrator persists bypass documentation.
5. **Execute:** Sub-skill runs with bypass warning banner on all outputs.
6. **Monitor:** At each subsequent wave signoff attempt, the orchestrator checks bypass documentation for remediation status against the stated target date. If the target date has passed without remediation evidence, the orchestrator notifies the user that the bypass remains unresolved and asks whether to extend the target date or prioritize remediation (P-020: user decides).
7. **Remediate:** User completes the unmet criterion per remediation plan.
8. **Close:** Bypass is resolved; warning banner removed from future outputs.

---

## Wave State Tracking

<!-- Source: SKILL.md Section "Wave Architecture" (lines 254-269) — wave state detection. Cross-reference: ux-routing-rules.md [Wave-Aware Routing] for routing-side state consumption. -->

### State Detection

Wave state is determined by the existence and validity of signoff files:

| File Exists | State |
|------------|-------|
| No signoff files | Only Foundation (Wave 0) is authorized |
| `KICKOFF-SIGNOFF.md` valid | Wave 1 authorized |
| `WAVE-1-SIGNOFF.md` valid | Wave 2 authorized |
| `WAVE-2-SIGNOFF.md` valid | Wave 3 authorized |
| `WAVE-3-SIGNOFF.md` valid | Wave 4 authorized |
| `WAVE-4-SIGNOFF.md` valid | Wave 5 authorized |
| `WAVE-5-SIGNOFF.md` valid | All waves complete |

### State Caching

<!-- Implementation guidance: Cache invalidation triggers specified here as orchestrator operational behavior. Not explicitly stated in SKILL.md Wave Architecture or Wave Signoff Enforcement sections. Derived from the wave state detection requirements: the orchestrator must detect signoff file changes within a session (trigger 1), must start fresh on new sessions (trigger 2), and must react to bypass grants/resolutions that change routing authorization (trigger 3). -->

The orchestrator checks signoff files once per engagement session and caches the wave state. Cache invalidation occurs:

- On the next routing decision after a signoff file is committed during the session.
- At the start of each new engagement session.
- When a bypass is granted or resolved.

### Worktracker Integration

Wave transitions are tracked via `/worktracker` entities:

- Each wave is a Feature entity under the `/user-experience` Epic.
- Sub-skill deployment Stories are children of the wave Feature.
- Signoff is an Enabler that gates the next wave Feature.

---

## Wave Transition Workflow

<!-- Source: SKILL.md Section "Wave Transition Quality Gates" (lines 271-283) — orchestrator-driven transition process. SKILL.md Section "Wave Signoff Enforcement" (lines 287-291) — signoff closure requirements. Step sequence derived from the combined flow: verify output → score via S-014 → verify evidence → check bypasses → generate signoff → user approval → commit → cache invalidation. Per-transition evidence requirements sourced from SKILL.md Wave Architecture table entry criteria (lines 260-267). Quality threshold (0.85) sourced from ADR-PROJ022-002 (PROVISIONAL). -->

The orchestrator follows this workflow when a wave transition is requested:

| Step | Action | Failure Behavior | Source |
|------|--------|-----------------|--------|
| 1 | Verify all sub-skills in the wave have produced output | Block transition; list sub-skills without output | SKILL.md "Wave Architecture" — sub-skills per wave |
| 2 | Score each sub-skill's representative output (the sub-skill's primary deliverable artifact as defined in its SKILL.md `output` section) via S-014 | Block if any score < 0.85 (ADR-PROJ022-002, PROVISIONAL) | SKILL.md "Wave Transition Quality Gates"; quality-enforcement.md S-014 |
| 3 | Verify additional evidence requirements (usage artifacts, story counts, user counts) per the Per-Transition Requirements table above | Block; list unmet evidence requirements | SKILL.md "Wave Architecture" entry criteria per wave |
| 4 | Check for unresolved bypasses in this wave | Block; list unresolved bypasses requiring remediation | SKILL.md "Wave Architecture" bypass mechanism; Bypass Constraints below |
| 4a | (Conditional, only if Step 4 identified unresolved bypasses from prior waves) Update bypass documentation with remediation evidence and target date status. This step must complete before generating the signoff document. | Bypass remains unresolved if remediation incomplete; signoff blocked per Bypass Constraints | Bypass Lifecycle step 6 (Monitor); P-020 user authority |
| 5 | Generate WAVE-N-SIGNOFF.md (where N = the wave number being completed, e.g., WAVE-2-SIGNOFF.md when completing Wave 2) using template | Present to user for review | SKILL.md "Wave Signoff Enforcement" line 289; template at `skills/user-experience/templates/wave-signoff-template.md` |
| 6 | User signs off (P-020: user authorizes wave closure) | No automatic signoff; user decides | P-020 (user authority); quality-enforcement.md H-02 |
| 7 | Commit signoff file to repository | Wave transition is recognized | SKILL.md "Wave Signoff Enforcement" line 289: "committed to the repository" |
| 8 | Invalidate wave state cache | Next routing decision uses updated state | Wave State Caching implementation guidance above |

### Post-Wave-5 Operational State

When `WAVE-5-SIGNOFF.md` is valid (all waves complete), the orchestrator enters **full operational mode**:

- **All 10 sub-skills deployed:** All sub-skills are available for routing without wave gate checks. The wave gating mechanism becomes dormant -- it is not removed, so it can be reactivated if a new sub-skill is added in a future version that requires a Wave 6.
- **Ongoing enforcement:** The orchestrator continues to enforce synthesis quality gates (`skills/user-experience/rules/synthesis-validation.md`), MCP availability detection (`skills/user-experience/rules/mcp-coordination.md`), and bypass constraint checks during normal operation.
- **Quality gate failures in full operational mode:** If a Wave 5 sub-skill's output fails the S-014 0.85 gate after Wave 5 is signed off, the failure does not revert the wave state. Instead, the orchestrator applies the standard creator-critic-revision cycle (H-14) to improve the output within the current engagement. Wave signoff is a deployment authorization gate, not a per-engagement quality gate.
- **Audit trail:** Wave signoff files are retained as immutable audit artifacts. They are not modified or deleted after wave completion.

---

*Version: 1.2.0*
*Rule file: wave-progression.md*
*Parent skill: /user-experience*
*Parent SKILL.md: `skills/user-experience/SKILL.md`*
*Architecture ADR: `projects/PROJ-022-user-experience-skill/decisions/ADR-PROJ022-001-ux-skill-architecture.md` (PROVISIONAL)*
*Threshold ADR: `projects/PROJ-022-user-experience-skill/decisions/ADR-PROJ022-002-wave-criteria-gates.md` (PROVISIONAL)*
*Sibling rules: `skills/user-experience/rules/ux-routing-rules.md`, `skills/user-experience/rules/synthesis-validation.md`, `skills/user-experience/rules/mcp-coordination.md`, `skills/user-experience/rules/ci-checks.md`*
*CI gates: UX-CI-007 (Signoff File Structure), UX-CI-008 (Signoff Ordering) in `skills/user-experience/rules/ci-checks.md`*
*Created: 2026-03-03*
*Updated: 2026-03-04*
*Status: COMPLETE*
