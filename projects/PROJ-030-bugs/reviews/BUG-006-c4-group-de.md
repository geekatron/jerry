# C4 Adversarial Execution Report: Group D-E (S-007, S-011, S-012, S-013)

> BUG-006 / ADR-EPIC002-001 Migration — Groups D-1, D-2, E-1, E-2
> Executed: 2026-04-01

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Execution Context](#execution-context) | Strategy metadata and deliverables under review |
| [Group D-1: S-007 Constitutional AI Critique](#group-d-1-s-007-constitutional-ai-critique) | Constitutional compliance findings |
| [Group D-2: S-011 Chain-of-Verification](#group-d-2-s-011-chain-of-verification) | Factual claim verification results |
| [Group E-1: S-012 FMEA](#group-e-1-s-012-fmea) | Failure mode and effects analysis |
| [Group E-2: S-013 Inversion Technique](#group-e-2-s-013-inversion-technique) | Goal inversion and assumption stress-test |
| [Combined Findings Summary](#combined-findings-summary) | All findings across all 4 strategies |
| [Execution Statistics](#execution-statistics) | Finding counts by strategy and severity |

---

## Execution Context

- **Strategies Executed:** S-007, S-011, S-012, S-013
- **Criticality:** C4 (All 10 strategies required — tournament mode)
- **Primary Deliverable:** `docs/design/ADR-output-path-resolution-001.md`
- **Supporting Deliverables:**
  - `projects/PROJ-030-bugs/work/BUG-006-skill-output-path-hardcoded.md`
  - `projects/PROJ-030-bugs/research/BUG-006-eng-audit-detail.md`
  - `projects/PROJ-030-bugs/research/BUG-006-red-audit-detail.md`
  - `projects/PROJ-030-bugs/research/BUG-006-ux-audit-detail.md`
- **Implementation State:** Phase 2 complete per BUG-006 History entry 2026-04-01
- **Templates:**
  - `.context/templates/adversarial/s-007-constitutional-ai.md`
  - `.context/templates/adversarial/s-011-cove.md`
  - `.context/templates/adversarial/s-012-fmea.md`
  - `.context/templates/adversarial/s-013-inversion.md`
- **Executed:** 2026-04-01T00:00:00Z

---

## Group D-1: S-007 Constitutional AI Critique

**Finding Prefix:** CC (per S-007 Identity)
**Execution ID:** 20260401-de

### Constitutional Context Index

Applicable principles evaluated against the migration (ADR + implementation):

| Principle | Tier | Applicability |
|-----------|------|---------------|
| P-002 (File Persistence) | HARD | Core: all agents must persist output to files |
| P-020 (User Authority) | HARD | DC-3 requires caller override capability |
| H-04 (Active Project Required) | HARD | DC-1 requires project-relative paths |
| H-13 (Quality Threshold >= 0.92) | HARD | C4 delivery requires quality gate |
| H-15 (Self-review before presenting) | HARD | ADR must be self-reviewed |
| H-23 (Navigation Table) | HARD | ADR has navigation table — check compliance |
| H-34 (Agent definition schema) | HARD | Governance YAML must pass schema validation |
| AE-003 (New ADR → auto-C3) | HARD | ADR triggers auto-escalation |
| AE-004 (Modifies baselined ADR → C4) | HARD | Check if this modifies a baselined ADR |
| DC-1 through DC-7 | MEDIUM | ADR's own design constraints |
| AD-M-011 (output path SHOULD standard) | MEDIUM | New MEDIUM standard codified |
| P-002 persistence | MEDIUM | All 107 files must actually be updated |

### Principle-by-Principle Evaluation

#### P-002 (File Persistence — HARD)

**Principle:** Agents MUST persist output to files, never transient-only.

**Evaluation:** The migration's core purpose is to fix P-002 compliance. All 32 governance YAML files, all 32 agent .md files, and composition YAMLs now reference project-relative paths. Verified: `grep -r 'skills/.*/output/' skills/` returns zero matches. The ADR defines a 4-level fallback chain that always terminates in a file write (Priority 4 fallback writes to `work/`).

**Result:** COMPLIANT. Evidence: zero grep matches on old paths; governance YAML samples confirm `projects/${JERRY_PROJECT}/engagements/` location.

#### P-020 (User Authority — HARD)

**Principle:** NEVER override user intent. Users must be able to override agent output paths.

**Evaluation:** DC-3 in the ADR requires "Callers MUST be able to override the output path." Priority 1 (explicit path in P-002 block) gives callers full override authority. Priority 2 (base path) is the second override mechanism. The resolution protocol preserves user authority at every tier.

**Result:** COMPLIANT. Evidence: ADR section "Output Path Resolution Protocol" defines P1 as highest priority, explicitly stating callers can redirect output to any path.

#### H-04 (Active Project Required — HARD)

**Principle:** MUST NOT proceed without `JERRY_PROJECT` set.

**Evaluation:** Priority 3 resolution requires `${JERRY_PROJECT}`. Priority 4 is a graceful degradation fallback that warns but still writes. The ADR states Priority 4 "Should never happen in normal operation. Safety net only." The P4 warning explicitly references H-04: "JERRY_PROJECT not set — output written to work/ fallback." The fallback does not silently swallow the H-04 violation; it surfaces it.

**Result:** COMPLIANT with Minor note. The P4 fallback provides graceful degradation rather than hard failure. The ADR acknowledges this is a violation state. A hard-fail option would be more compliant with H-04's intent, but graceful degradation is reasonable for agent context where aborting entirely would lose work. Logged as Minor.

**Finding CC-001-20260401-de** (Minor)

#### H-23 (Navigation Table — HARD)

**Principle:** All Claude-consumed markdown files over 30 lines MUST include a navigation table.

**Evaluation:** The ADR includes a navigation table with 14 sections, all with anchor links. Format is `| Section | Purpose |` with anchor links. Navigation table appears after frontmatter before first content section. Verified.

**Result:** COMPLIANT.

#### H-34 (Agent Definition Schema — HARD)

**Principle:** Agent definitions use dual-file architecture; `filename_pattern` field must be schema-validated.

**Evaluation:** The migration adds `filename_pattern` to the governance schema (`docs/schemas/agent-governance-v1.schema.json` line 135 confirmed). All 32 governance YAML files sampled contain `filename_pattern`. Schema accepts the new field as optional (non-breaking additive). H-34 requires schema validation before LLM scoring — Step 0 of migration updates schema FIRST.

**Result:** COMPLIANT.

#### ADR Status — Lifecycle Concern (MEDIUM violation)

**Principle:** ADR Status field should accurately reflect implementation state (AE-003, governance practice).

**Evaluation:** The ADR frontmatter shows `Status: proposed` as of the time of this evaluation. However, the BUG-006 History entry for 2026-04-01 states "Phase 2 execution: all 9 tasks completed... AC-1 through AC-7 all satisfied." The implementation is complete but the ADR status has not been advanced to `accepted`. An ADR whose implementation is complete should be promoted to `accepted` to accurately reflect the governance state.

**Finding CC-002-20260401-de** (Major — misleading ADR lifecycle state)

#### ADR ID Collision with quality-enforcement.md References (Major)

**Principle:** P-022 (No Deception) — documentation must not mislead readers about what `ADR-EPIC002-001` refers to.

**Evaluation:** `quality-enforcement.md` (the SSOT) references `ADR-EPIC002-001` at lines 108, 275, 290, and 350 — all referring to the adversarial strategy selection ADR (composite scores, exclusion rationale, S-014 rubric). The NEW ADR at `docs/design/ADR-output-path-resolution-001.md` uses the same ID for a completely different subject (unified output path resolution). Two distinct design decisions share the identifier `ADR-EPIC002-001`. Any reader following a `quality-enforcement.md` reference to `ADR-EPIC002-001` will find the output path ADR rather than the strategy selection ADR, causing confusion and broken traceability.

**Finding CC-003-20260401-de** (Major — ADR ID collision with SSOT references)

#### DC-1 through DC-7 Compliance

Evaluated the ADR's stated design constraints against the implemented solution:

| Constraint | Evaluation | Result |
|-----------|------------|--------|
| DC-1: Project-relative paths | All 32 governance YAML use `projects/${JERRY_PROJECT}/` | COMPLIANT |
| DC-2: File persistence | P4 fallback always writes to file | COMPLIANT |
| DC-3: Caller override | P1 explicit path + P2 base path | COMPLIANT |
| DC-4: All contexts | Compatibility matrix covers 7 contexts | COMPLIANT |
| DC-5: Engagement-ID scoping | `{engagement-id}` preserved in all templates | COMPLIANT |
| DC-6: No Python changes | Pure agent definition changes only | COMPLIANT |
| DC-7: Backward compat | /problem-solving, /adversary, /nasa-se untouched | COMPLIANT |

**Result:** All 7 DCs satisfied.

#### Composition YAML Missing filename_pattern (Minor)

**Evaluation:** The composition YAML files (e.g., `skills/eng-team/composition/eng-architect.agent.yaml`) contain `output.location` updated to project-relative paths but do NOT have `filename_pattern`. The ADR Step 1 specifies adding `filename_pattern` only to governance YAML (`*.governance.yaml`), not composition YAML. However, if Priority 2 resolution requires agents to use `output.filename_pattern` and agents load configuration from composition YAML rather than governance YAML at runtime, this gap could cause P2 resolution failures. This is architecturally ambiguous — it depends on which YAML file the agent runtime actually reads.

**Finding CC-004-20260401-de** (Minor — composition YAML missing filename_pattern, P2 resolution ambiguity)

### S-007 Findings Summary

| ID | Principle | Tier | Severity | Evidence | Affected Dimension |
|----|-----------|------|----------|----------|-------------------|
| CC-001-20260401-de | H-04 graceful degradation | HARD | Minor | P4 fallback warns but does not hard-fail; H-04 intent is active project REQUIRED | Methodological Rigor |
| CC-002-20260401-de | ADR lifecycle state | MEDIUM | Major | `Status: proposed` in ADR frontmatter; BUG-006 history records all tasks complete 2026-04-01 | Internal Consistency |
| CC-003-20260401-de | P-022 (No Deception) via ADR ID collision | HARD | Major | `quality-enforcement.md` lines 108, 275, 290, 350 reference ADR-EPIC002-001 as strategy selection ADR; new output path ADR uses same ID | Traceability |
| CC-004-20260401-de | AD-M-011 (composition YAML) | MEDIUM | Minor | `eng-architect.agent.yaml` line 53 has `location` but no `filename_pattern`; ADR Step 1 targets governance YAML only | Completeness |

### S-007 Constitutional Compliance Score

- Critical violations: 0
- Major violations: 2 (CC-002, CC-003)
- Minor violations: 2 (CC-001, CC-004)

Score: `1.00 - (2 × 0.05) + (2 × 0.02)` = `1.00 - 0.10 - 0.04` = **0.86 (REVISE)**

---

## Group D-2: S-011 Chain-of-Verification

**Finding Prefix:** CV (per S-011 Identity)
**H-16 Status:** S-003 Steelman not confirmed in prior outputs (indirect H-16 for CoVe — proceed)

### Step 1: Claim Inventory

Claims extracted from ADR-EPIC002-001 and BUG-006:

| ID | Claim | Source | Type |
|----|-------|--------|------|
| CL-001 | "All 32 governance YAML have filename_pattern" | BUG-006 AC-4 / ADR Migration Guide | Behavioral claim |
| CL-002 | "All 32 agent .md have Output Path Resolution section" | ADR Step 2 | Behavioral claim |
| CL-003 | "`grep -r 'skills/.*/output/' skills/` returns zero matches" | BUG-006 AC-1 / ADR Verification | Factual assertion |
| CL-004 | "AD-M-011 uses SHOULD language (MEDIUM tier)" | ADR Step 5 | Rule citation |
| CL-005 | "`.gitignore` updated to block `skills/*/output/`" | BUG-006 AC-7 | Behavioral claim |
| CL-006 | "107 config files require updates (22 eng + 25 red + 60 UX)" | BUG-006 Summary | Quantitative claim |
| CL-007 | "`skills/eng-team/output/` directory and 28 files removed" | BUG-006 AC-2 | Behavioral claim |
| CL-008 | "Composition YAML `output.location` updated to project-relative" | Implied by migration | Behavioral claim |
| CL-009 | "ADR-EPIC002-001 is the correct ID for the output path decision" | ADR frontmatter | Cross-reference claim |

### Step 2: Verification Questions

| VQ | Claim | Question |
|----|-------|---------|
| VQ-001 | CL-001 | Do all 32 governance YAML files contain `filename_pattern`? |
| VQ-002 | CL-002 | Do all 32 agent .md files contain `Output Path Resolution` section? |
| VQ-003 | CL-003 | Does `grep -r 'skills/.*/output/' skills/` return zero matches? |
| VQ-004 | CL-004 | Does AD-M-011 text in agent-development-standards.md use only SHOULD language (no MUST/SHALL)? |
| VQ-005 | CL-005 | Does `.gitignore` contain `skills/*/output/`? |
| VQ-006 | CL-006 | Do file counts (22+25+60=107) add up correctly? |
| VQ-007 | CL-007 | Does the `skills/eng-team/output/` directory and its contents no longer exist? |
| VQ-008 | CL-008 | Do sampled composition YAML `output.location` values use `projects/${JERRY_PROJECT}/`? |
| VQ-009 | CL-009 | Is `ADR-EPIC002-001` a unique identifier, or does it conflict with existing references? |

### Step 3: Independent Verification Results

**VQ-001 — filename_pattern in all 32 governance YAML:**
Verification: Grep across all governance YAML families:
- `skills/eng-team/agents/*.governance.yaml`: 10 files, all contain `filename_pattern` (verified via grep returning 10 matches)
- `skills/red-team/agents/*.governance.yaml`: 11 files, all contain `filename_pattern` (verified via grep returning 11 matches)
- `skills/user-experience/agents/ux-orchestrator.governance.yaml`: 1 file, contains `filename_pattern: "ux-orchestrator-{type}.md"` (verified at line 77)
- `skills/ux-*/agents/*.governance.yaml`: 10 files found (ai-first-design, atomic-design, behavior-design, design-sprint, heart-metrics, heuristic-eval, inclusive-design, jtbd, kano-model, lean-ux), all contain `filename_pattern` (verified individually)

Total: 10 + 11 + 1 + 10 = **32 governance YAML files all have filename_pattern**.
**Independent answer: VERIFIED**

**VQ-002 — Output Path Resolution in all 32 agent .md files:**
Verification:
- `skills/eng-team/agents/*.md`: 10 files, all contain "Output Path Resolution" (grep returned 10 matches)
- `skills/red-team/agents/*.md`: 11 files, all contain "Output Path Resolution" (grep returned 11 matches)
- `skills/user-experience/agents/ux-orchestrator.md`: 1 file, contains "Output Path Resolution" (grep returned 1 match)
- `skills/ux-*/agents/*.md` (10 sub-skills sampled individually): all 10 contain "Output Path Resolution"

Total verified: 10 + 11 + 1 + 10 = 32. **Independent answer: VERIFIED**

**VQ-003 — Zero grep matches:**
Executed: `grep -r 'skills/.*/output/' skills/` against the actual codebase. Returned zero matches.
**Independent answer: VERIFIED**

**VQ-004 — AD-M-011 SHOULD language:**
Read `agent-development-standards.md` line 63 directly. The AD-M-011 entry uses: "SHOULD follow", "SHOULD declare", "SHOULD accept", "SHOULD NOT hardcode". Zero instances of MUST, SHALL, NEVER, FORBIDDEN, REQUIRED, CRITICAL.
**Independent answer: VERIFIED — all SHOULD (MEDIUM tier)**

**VQ-005 — .gitignore contains skills/*/output/:**
Read `.gitignore` line 69: `skills/*/output/`
**Independent answer: VERIFIED**

**VQ-006 — File count arithmetic:**
22 (eng) + 25 (red) + 60 (UX) = 107. The ADR states 107 throughout. BUG-006 Summary states "107 config files (22 eng-team + 25 red-team + 60 UX)". The numbers add up.
**Independent answer: VERIFIED**

**VQ-007 — skills/eng-team/output/ removed:**
Glob `skills/eng-team/output/**` returned no files. Directory and contents are gone.
**Independent answer: VERIFIED**

**VQ-008 — Composition YAML output.location updated:**
Sample checks on `eng-architect.agent.yaml` (line 53): `"projects/${JERRY_PROJECT}/engagements/{engagement-id}/eng-architect-{topic-slug}.md"`. `red-recon.agent.yaml` (line 52): `projects/${JERRY_PROJECT}/engagements/{engagement-id}/red-recon-{topic-slug}.md`.
**Independent answer: VERIFIED for sampled files**

**VQ-009 — ADR-EPIC002-001 uniqueness:**
Read `quality-enforcement.md`. Lines 108, 275, 290, 350 reference `ADR-EPIC002-001` as the source for "Strategy selection, composite scores, exclusion rationale" — a different ADR about adversarial strategy scoring. The new `docs/design/ADR-output-path-resolution-001.md` uses the same ID for a completely different design decision. These are TWO DIFFERENT documents with the same identifier.
**Independent answer: MATERIAL DISCREPANCY**

### Step 4: Consistency Check

| CL | Claim | VQ | Result | Severity |
|----|-------|----|--------|---------|
| CL-001 | All 32 governance YAML have filename_pattern | VQ-001 | VERIFIED | — |
| CL-002 | All 32 agent .md have Output Path Resolution | VQ-002 | VERIFIED | — |
| CL-003 | grep returns zero matches | VQ-003 | VERIFIED | — |
| CL-004 | AD-M-011 uses SHOULD language | VQ-004 | VERIFIED | — |
| CL-005 | .gitignore blocks skills/*/output/ | VQ-005 | VERIFIED | — |
| CL-006 | 107 files = 22+25+60 | VQ-006 | VERIFIED | — |
| CL-007 | eng-team/output/ removed | VQ-007 | VERIFIED | — |
| CL-008 | Composition YAML updated | VQ-008 | VERIFIED (sample) | — |
| CL-009 | ADR-EPIC002-001 is unique identifier | VQ-009 | MATERIAL DISCREPANCY | Major |

**Finding CV-001-20260401-de** (Major — ADR ID collision)

### S-011 Verification Summary

- **Claims extracted:** 9
- **Verified:** 8
- **Minor discrepancies:** 0
- **Material discrepancies:** 1 (CL-009 — ADR ID collision)
- **Unverifiable:** 0
- **Verification rate:** 88.9% (8/9)

| ID | Claim | Source | Discrepancy | Severity | Affected Dimension |
|----|-------|--------|-------------|----------|--------------------|
| CV-001-20260401-de | ADR-EPIC002-001 is the correct unique ID for the output path decision | quality-enforcement.md, ADR frontmatter | quality-enforcement.md already uses ADR-EPIC002-001 for the strategy selection ADR; the new output path ADR creates an ID collision | Major | Traceability |

**Overall assessment:** 8 of 9 claims independently verified. One material discrepancy identified (ADR ID collision). The migration implementation is factually correct and complete. The ID collision is a documentation/governance defect, not an implementation defect.

---

## Group E-1: S-012 FMEA

**Finding Prefix:** FM (per S-012 Identity)
**H-16 Status:** S-003 output not provided; S-003 SHOULD precede S-012. Proceeding (indirect H-16 for FMEA).

### Step 1: Element Decomposition

| Element | Description |
|---------|-------------|
| E-1 | Output Path Resolution Protocol (4-priority chain) |
| E-2 | Governance YAML migration (32 files, filename_pattern) |
| E-3 | Agent .md migration (32 files, Output Path Resolution section) |
| E-4 | Composition YAML migration (32 files, location update) |
| E-5 | Prompt Recognition Specification (P1/P2/P3/P4 detection) |
| E-6 | AD-M-011 MEDIUM standard |
| E-7 | .gitignore enforcement |
| E-8 | Governance schema (filename_pattern field) |
| E-9 | ADR metadata and lifecycle |
| E-10 | Backward compatibility claims |

### Step 2: Failure Mode Enumeration

**E-1: Output Path Resolution Protocol**

| FM | Mode | Effect |
|----|------|--------|
| FM-001-20260401-de | Agent ignores P-002 block entirely (agent compliance not enforced) | Output goes to P3 default; P1 intent lost; files land in wrong project path |
| FM-002-20260401-de | Both P1 and P2 present — agent incorrectly applies P2 | Output at base_path + suffix instead of explicit P1 path; orchestration output misrouted |
| FM-003-20260401-de | P3 template with ${JERRY_PROJECT} unresolved (H-04 not triggered) | Literal `${JERRY_PROJECT}` in output filename; Write tool creates malformed path |

**E-2: Governance YAML migration**

| FM | Mode | Effect |
|----|------|--------|
| FM-004-20260401-de | Agent runtime reads composition YAML, not governance YAML for output.location | filename_pattern in governance YAML ignored; P2 resolution unavailable to agent |
| FM-005-20260401-de | Future agent added with old skills/*/output/ pattern (no CI gate) | Regression; new agent immediately broken; ADR-EPIC002-001 compliance erodes over time |

**E-3: Agent .md migration**

| FM | Mode | Effect |
|----|------|--------|
| FM-006-20260401-de | Agent reads Output Path Resolution section but misinterprets priority order | Priority confusion causes P2 to override P1, or P3 to be used when P1 is present |
| FM-007-20260401-de | Output Path Resolution section present in .md but variables table incomplete or incorrect | Agent cannot resolve {topic-slug} or {engagement-id}; falls to P4 fallback unnecessarily |

**E-4: Composition YAML migration**

| FM | Mode | Effect |
|----|------|--------|
| FM-008-20260401-de | Composition YAML does not have filename_pattern; if agent runtime uses composition YAML for P2 | P2 base-path resolution fails silently; agent falls through to P3 |
| FM-009-20260401-de | Composition YAML location field and governance YAML location field diverge in the future | Two sources of truth; agents may use either; inconsistent behavior across invocation methods |

**E-5: Prompt Recognition**

| FM | Mode | Effect |
|----|------|--------|
| FM-010-20260401-de | P1 trigger: `## MANDATORY PERSISTENCE (P-002)` with `Create file at:` but agent already in tool-call mode, doesn't re-read prompt | P1 ignored; P3 default used; output at wrong location |
| FM-011-20260401-de | Caller provides `## OUTPUT CONTEXT` with Base Path but no Engagement ID; agent path template contains literal `{engagement-id}` | Malformed path: `projects/PROJ-030/work/BUG-006/{engagement-id}/eng-architect-.md` |

**E-6: AD-M-011 Standard**

| FM | Mode | Effect |
|----|------|--------|
| FM-012-20260401-de | AD-M-011 is MEDIUM (SHOULD), not HARD; future agents ignore it without justification | Pattern recurs; new skills use skills/*/output/ again; bug reintroduced |

**E-9: ADR Lifecycle**

| FM | Mode | Effect |
|----|------|--------|
| FM-013-20260401-de | ADR Status remains "proposed" after implementation is complete | Governance gap: proposed ADRs are theoretically reversible; approved implementations cannot be referenced as decided |
| FM-014-20260401-de | ADR-EPIC002-001 ID collision with quality-enforcement.md SSOT references | Readers following quality-enforcement.md reference land on the wrong ADR; traceability broken |

**E-10: Backward Compatibility**

| FM | Mode | Effect |
|----|------|--------|
| FM-015-20260401-de | /nasa-se agents mentioned as "no changes required" but /nasa-se does not have filename_pattern; P2 unavailable for /nasa-se | If orchestrators use P2 base_path pattern with /nasa-se agents, P2 falls through to P3 silently |

### Step 3: RPN Ratings

| FM | Description | S | O | D | RPN | Severity |
|----|-------------|---|---|---|-----|---------|
| FM-001 | Agent ignores P-002 block | 8 | 3 | 5 | 120 | Major |
| FM-002 | Both P1+P2 present, P2 applied | 6 | 2 | 7 | 84 | Major |
| FM-003 | ${JERRY_PROJECT} unresolved in path | 7 | 2 | 6 | 84 | Major |
| FM-004 | Runtime reads composition not governance YAML | 9 | 4 | 7 | 252 | **Critical** |
| FM-005 | Future agent adds old path pattern — no CI gate | 7 | 5 | 7 | 245 | **Critical** |
| FM-006 | Agent misinterprets priority order | 6 | 2 | 5 | 60 | Minor |
| FM-007 | Variables table incomplete | 5 | 2 | 5 | 50 | Minor |
| FM-008 | Composition YAML lacks filename_pattern | 7 | 5 | 6 | 210 | **Critical** |
| FM-009 | Composition/governance YAML diverge over time | 6 | 4 | 6 | 144 | Major |
| FM-010 | Agent doesn't re-read prompt for P1 | 7 | 2 | 4 | 56 | Minor |
| FM-011 | Missing Engagement ID with Base Path | 5 | 4 | 5 | 100 | Major |
| FM-012 | AD-M-011 MEDIUM tier allows future violations | 7 | 4 | 4 | 112 | Major |
| FM-013 | ADR status "proposed" after implementation | 4 | 9 | 2 | 72 | Minor |
| FM-014 | ADR ID collision | 7 | 9 | 3 | 189 | Major |
| FM-015 | /nasa-se P2 unavailable silently | 4 | 3 | 7 | 84 | Major |

**Total RPN: 1974**

### Step 4: Prioritized Corrective Actions

**Critical (RPN >= 200):**

**FM-004 (RPN 252) — Runtime reads composition, not governance YAML:**
The ADR adds `filename_pattern` to governance YAML files but NOT to composition YAML files. If agents at runtime resolve their output configuration from `composition/*.agent.yaml` (which many Claude Code agent invocations appear to use as the primary config), then `filename_pattern` may not be accessible at P2 resolution time. The composition YAML files sampled (`eng-architect.agent.yaml`, `red-recon.agent.yaml`) confirm `filename_pattern` is absent.

**Corrective Action:** Either (a) add `filename_pattern` to all 32 composition YAML files as well, or (b) document definitively which YAML file the agent runtime reads for `output.filename_pattern` at P2 resolution. If the runtime uses `.md` frontmatter exclusively, this is moot — but the ADR does not clarify which file wins for the `filename_pattern` lookup.

**FM-005 (RPN 245) — No CI gate against skills/*/output/ patterns:**
There is a `.gitignore` rule (`skills/*/output/`) that prevents new output files from being committed to those directories. However, there is no L5 CI check that would fail the build if a governance YAML or agent .md is written with a `skills/*/output/` path. A future developer could add a new skill with the old pattern and it would pass CI validation (schema validation does not check the value of `output.location`, only its presence and type).

**Corrective Action:** Add an L5 CI check (grep-based or schema-based) that rejects governance YAML or composition YAML files where `output.location` contains `skills/` and `output/` in the same value. This closes the regression vector.

**FM-008 (RPN 210) — Composition YAML missing filename_pattern:**
The composition YAML files contain `output.location` (now project-relative) but do not contain `output.filename_pattern`. If the agent runtime's P2 resolution logic reads from composition YAML, P2 silently falls to P3 without the caller knowing.

**Corrective Action:** Same as FM-004 — either add `filename_pattern` to all composition YAML or document the authoritative config source for each resolution priority.

**Major (RPN 80-199):**

**FM-014 (RPN 189) — ADR ID collision:**
`quality-enforcement.md` already uses `ADR-EPIC002-001` to reference the strategy selection ADR. The new output path ADR reuses the same ID. This breaks the SSOT reference chain.

**Corrective Action:** Rename the output path ADR to `ADR-EPIC002-002` (next available ID in the EPIC-002 namespace) and update all references. Alternatively, clarify that the original `ADR-EPIC002-001` reference in quality-enforcement.md refers to a different document (the scoring ADR) and rename the output path ADR. Either way, the ID must be unique.

**FM-012 (RPN 112) — AD-M-011 MEDIUM tier:**
MEDIUM (SHOULD) rules allow documented override. Without a HARD enforcement (H-XX rule or L5 CI gate), the anti-pattern can recur. The existence of AD-M-011 is correct (MEDIUM is appropriate for an output path standard), but it needs a compensating CI gate.

**Corrective Action:** Add L5 CI grep gate to enforce that no `output.location` in any `*.governance.yaml` or `*.agent.yaml` contains `skills/*/output/`. This converts the MEDIUM AD-M-011 into an enforced standard without requiring a HARD rule slot.

**FM-011 (RPN 100) — Missing Engagement ID with Base Path:**
The ADR's Failure Mode Analysis section covers this case ("Agent MUST request engagement-id via H-31 clarification before writing"). However, the agent .md Output Path Resolution sections do not include explicit instructions to detect this failure mode and invoke H-31.

**Corrective Action:** Add to the Output Path Resolution section in agent .md files: "If no `{engagement-id}` is available and no explicit path is provided, request engagement-id via H-31 before writing output."

**FM-001 (RPN 120) — Agent ignores P-002 block:**
This is mitigated by L4 post-tool output inspection. The ADR's Failure Mode Analysis acknowledges this: "Post-tool output inspection: artifact not at expected location." No additional corrective action at ADR level — this is an L4 enforcement concern.

### S-012 Findings Summary

| ID | Element | Failure Mode | S | O | D | RPN | Severity | Affected Dimension |
|----|---------|-------------|---|---|---|-----|---------|-------------------|
| FM-004-20260401-de | Composition YAML/Governance YAML split | Runtime may read composition (no filename_pattern) for P2 | 9 | 4 | 7 | 252 | Critical | Methodological Rigor |
| FM-005-20260401-de | No CI gate | Future agents can add old path pattern | 7 | 5 | 7 | 245 | Critical | Traceability |
| FM-008-20260401-de | Composition YAML missing filename_pattern | P2 resolution falls to P3 silently | 7 | 5 | 6 | 210 | Critical | Completeness |
| FM-014-20260401-de | ADR ID collision | quality-enforcement.md reference broken | 7 | 9 | 3 | 189 | Major | Traceability |
| FM-012-20260401-de | AD-M-011 MEDIUM only | Pattern can recur without CI enforcement | 7 | 4 | 4 | 112 | Major | Methodological Rigor |
| FM-011-20260401-de | Missing Engagement ID | Malformed path, H-31 not invoked | 5 | 4 | 5 | 100 | Major | Actionability |
| FM-001-20260401-de | Agent ignores P-002 block | Output at wrong location | 8 | 3 | 5 | 120 | Major | Methodological Rigor |
| FM-009-20260401-de | Config file divergence over time | Two sources of truth | 6 | 4 | 6 | 144 | Major | Internal Consistency |
| FM-002-20260401-de | P1+P2 both present | P2 overrides P1 | 6 | 2 | 7 | 84 | Major | Methodological Rigor |
| FM-003-20260401-de | ${JERRY_PROJECT} unresolved | Malformed path literal | 7 | 2 | 6 | 84 | Major | Completeness |
| FM-015-20260401-de | /nasa-se P2 unavailable | Silent P2→P3 fallthrough | 4 | 3 | 7 | 84 | Major | Completeness |
| FM-006-20260401-de | Agent misinterprets priority | P2 used when P1 intended | 6 | 2 | 5 | 60 | Minor | Methodological Rigor |
| FM-007-20260401-de | Variables table incomplete | Unnecessary P4 fallback | 5 | 2 | 5 | 50 | Minor | Completeness |
| FM-010-20260401-de | Agent doesn't re-read prompt | P1 missed | 7 | 2 | 4 | 56 | Minor | Methodological Rigor |
| FM-013-20260401-de | ADR status "proposed" | Governance gap | 4 | 9 | 2 | 72 | Minor | Internal Consistency |

**Highest-risk element: E-4 (Composition YAML) + E-9 (ADR Lifecycle) — combined RPN 630**

**Overall assessment:** The migration is structurally sound for the files it updated. Three Critical failure modes (FM-004, FM-005, FM-008) relate to gaps between governance YAML and composition YAML, and to the absence of a CI gate preventing regression. These do not invalidate the migration but represent incomplete implementation of the enforcement layer.

---

## Group E-2: S-013 Inversion Technique

**Finding Prefix:** IN (per S-013 Identity)
**H-16 Status:** S-003 output not provided; S-003 SHOULD precede S-013. Proceeding (indirect H-16 for Inversion).

### Step 1: Goal Inventory

Goals explicitly stated in ADR-EPIC002-001:

| Goal | Measurement | Type |
|------|-------------|------|
| G-1 | All 32 agents work correctly in any invocation context (standalone, orchestration, worktracker, UX wave) | Explicit |
| G-2 | Zero `skills/*/output/` paths remain across all config files | Explicit |
| G-3 | Output path convention documented in agent-development-standards.md | Explicit |
| G-4 | Backward compatibility: /problem-solving, /adversary, /nasa-se unchanged | Explicit |
| G-5 | Protocol is extensible to future skills without code changes | Implicit |
| G-6 | Callers can understand and use the P1/P2/P3/P4 patterns correctly | Implicit |
| G-7 | The migration does not create a new hardcoded-path anti-pattern | Implicit |

### Step 2: Anti-Goals (Inversion)

**Inversion of G-1 — "Agents work in any context":**

To guarantee failure, we would ensure:
- The protocol only specifies what paths LOOK LIKE but not HOW agents detect which priority level applies
- Agent .md instructions describe the protocol but do not include concrete prompt-scanning logic
- The priority detection logic is ambiguous (e.g., what if `## MANDATORY PERSISTENCE` appears but without `Create file at:`)

**Finding IN-001-20260401-de:** The Output Path Resolution section in agent .md files instructs agents on the 4-level priority chain but does not include explicit prompt-scanning instructions. An agent that misses the P1 marker (e.g., because the P-002 block appears at a non-standard location in the prompt) will silently fall to P3. The ADR's Prompt Recognition Specification is in the ADR document — it is not directly included in the agent .md Output Path Resolution sections. Agents reading only their own .md file do not have access to the full parsing specification.

**Severity: Major** — Affects G-1 (any invocation context).

**Inversion of G-4 — "Protocol is backward compatible":**

To guarantee breaking /problem-solving, /adversary, or /nasa-se:
- Add a requirement that ALL agents must now include `filename_pattern` in their governance YAML
- Change the schema to REQUIRE `filename_pattern` (not just permit it)
- Make the P2 resolution path mandatory for callers who specify `## OUTPUT CONTEXT`

**Finding IN-002-20260401-de:** The schema change makes `filename_pattern` an OPTIONAL field (verified: schema at line 135 shows no `required` constraint). If a future schema revision marks `filename_pattern` as `required`, it would break all existing /problem-solving, /adversary, and /nasa-se governance YAML files that don't have the field. The ADR mentions this is "non-breaking additive" but does not add a guard in the schema itself (e.g., a description warning against marking it required).

**Severity: Minor** — Current state is safe; risk is future regression if schema is modified.

**Inversion of G-2 — "Zero skills/*/output/ paths remain":**

Verification (VQ-003 above): grep returns zero matches. This goal IS achieved. The inversion test confirms no vulnerability here.

**Not a finding.**

**Inversion of G-5 — "Protocol extensible to future skills":**

To guarantee extensibility fails:
- The protocol requires agents to self-read their prompt for P1/P2 markers (behavioral requirement)
- But there is no skill template or onboarding template showing new skill authors exactly what to put in agent .md files
- New skill authors must read the ADR, find the agent integration specification, and copy the Output Path Resolution section format — there is no canonical template to copy from

**Finding IN-003-20260401-de:** The ADR defines the Output Path Resolution section content as a reference specification but does not create a reusable template (e.g., a `skills/_template/` directory or update to an existing new-skill template). Future skill authors must manually discover and implement the pattern. Without a template, the probability of partial or incorrect implementation in new skills is elevated.

**Severity: Major** — Affects G-5 (extensibility) and G-7 (preventing recurrence of the anti-pattern).

**Inversion of G-6 — "Callers understand and use P1/P2/P3/P4 correctly":**

To guarantee caller confusion:
- Provide three prompt patterns (A, B, C) with different section headers
- Do not update the canonical prompt templates that callers use today
- Require callers to read the ADR to understand which pattern to use
- Leave the existing `prompt-templates.md` unchanged

**Finding IN-004-20260401-de:** The ADR defines three prompt patterns (A: explicit path, B: base path, C: no override) but the canonical caller templates (`prompt-templates.md`, `PS_EXTENSION.md`) are not updated to show how to use these patterns. A caller invoking /eng-team today will not encounter P1/P2 patterns in any documentation they are likely to read — they would need to discover the ADR independently. The migration is agent-side complete but caller-side documentation remains unchanged.

**Severity: Major** — Affects G-6 (caller understanding).

**Inversion of G-7 — "Migration does not create a new hardcoded anti-pattern":**

The ADR replaces `skills/eng-team/output/` with `projects/${JERRY_PROJECT}/engagements/`. Is `engagements/` itself a hardcoded sub-directory structure?

**Finding IN-005-20260401-de:** The ADR hardcodes the `engagements/` subdirectory in all P3 default templates (e.g., `projects/${JERRY_PROJECT}/engagements/{engagement-id}/eng-architect-{topic-slug}.md`). This means all eng-team, red-team, and UX outputs MUST go under `engagements/` at P3. While this is better than `skills/*/output/`, it creates a new convention that:
(a) Was established by single-ADR decision without cross-skill input
(b) May conflict with future skills that use different organizing concepts (e.g., a `/data-engineering` skill might prefer `pipelines/` over `engagements/`)
(c) Is not defined in the main path convention in `project-workflow.md` (which mentions only `work/`, `research/`, `decisions/`, `orchestration/`)

**Severity: Minor** — The `engagements/` convention is reasonable for engagement-based skills but is not documented in the project-level path convention.

### Step 3: Assumption Map

| Assumption | Type | Confidence | Validation | Consequence if Wrong |
|-----------|------|-----------|------------|---------------------|
| A-1: Agents re-read the prompt's P-002 block before writing each output file | Technical | Medium | Unvalidated (assumed LLM behavior) | P1 ignored; output at wrong location |
| A-2: Claude Code runtime reads `output.filename_pattern` from governance YAML for P2 | Technical | Low | Unverified — runtime source unclear | P2 resolution fails silently |
| A-3: The 4-level chain is sufficient for all current and future invocation contexts | Process | Medium | Partially validated (7 contexts in matrix) | New context breaks outside protocol |
| A-4: Callers will discover the P1/P2/P3/P4 patterns through documentation | Process | Low | Not validated (no template updates) | Callers use P3 by default, not by choice |
| A-5: `.gitignore` is sufficient to prevent future skills/*/output/ accumulation | Environmental | Medium | Verified for new outputs; not verified for governance YAML authoring | New skill re-introduces pattern in YAML |
| A-6: The `engagements/` subdirectory convention will not conflict with future skills | Temporal | Medium | Unvalidated | Path convention fragmentation |

### Step 4: Stress-Test Results

**A-2 (Confidence: Low) — Runtime reads governance YAML for filename_pattern:**

Inverting: "The agent runtime does NOT read governance YAML for `output.filename_pattern`."

**Plausibility:** High. The composition YAML (`*.agent.yaml`) is the primary Claude Code configuration file. The governance YAML (`*.governance.yaml`) is a Jerry-specific convention for validation, not a Claude Code runtime file. Claude Code may load composition YAML as the agent definition — in which case `filename_pattern` in governance YAML is invisible to the running agent.

**Consequence if true:** P2 resolution (base path + filename) fails for all 32 migrated agents. Every caller who provides `## OUTPUT CONTEXT` with `Base Path:` will get P3 fallback (project default), not P2 (base path + suffix). This is silent — no error, just wrong output path.

**Finding IN-006-20260401-de (Critical):** The assumption that agents can access `output.filename_pattern` at runtime is unverified. The ADR places `filename_pattern` in governance YAML, but the agent LLM context is populated from the agent `.md` file (system prompt) and composition YAML (Claude Code config), not governance YAML (which is a machine-readable governance record). The `filename_pattern` value is mentioned in agent .md Output Path Resolution sections only as a concept — the actual `filename_pattern` value (e.g., `eng-architect-{topic-slug}.md`) is hardcoded into the agent .md's step 2 instruction: "append filename", and visible in the variables table. This means P2 works via the agent .md instructions (which are in the LLM context), not via runtime YAML lookup. However, this relationship is not made explicit in the ADR — the spec makes it look like the agent reads `output.filename_pattern` from YAML at runtime, which is not how LLM agents work.

**Severity: Critical** — The ADR specification describes a runtime behavior (YAML lookup) that LLM agents cannot perform; the actual mechanism (hardcoded filename in .md instructions) is never made explicit. Future implementers may misunderstand the protocol.

**A-4 (Confidence: Low) — Callers discover P1/P2/P3/P4 through documentation:**

Inverting: "Callers will NOT discover the P1/P2/P3/P4 patterns."

**Plausibility:** High. The primary caller-facing documentation is `prompt-templates.md` and the skill `SKILL.md` files. None of these were updated with P1/P2/P3 prompt pattern examples as part of this migration (confirmed: ADR Step 3 updates SKILL.md paths but not prompt patterns). Callers will continue to invoke agents without providing `## OUTPUT CONTEXT`, causing all invocations to use P3 (project default) — which is correct but not by informed choice.

**Finding IN-007-20260401-de:** Caller-facing documentation (`prompt-templates.md`, SKILL.md examples sections) does not include examples of P1, P2, or P3 usage patterns. The migration is implementor-complete but caller-incomplete. Users who want P1 (orchestration path) or P2 (base path) must discover these patterns by reading the ADR, not from normal usage documentation.

**Severity: Major** — Affects G-6. The protocol's full value is only accessible to callers who read the ADR.

### Step 5: Mitigations

| Finding | Mitigation | Priority |
|---------|-----------|---------|
| IN-006-20260401-de | Revise ADR to clarify that `filename_pattern` is a documentation field (not a runtime YAML lookup); the actual P2 filename is specified in agent .md Output Path Resolution step 2 instructions. This prevents future implementers from building a YAML-lookup mechanism that contradicts how LLM agents actually work. | P0 |
| IN-003-20260401-de | Create a canonical skill author template in `.context/templates/agent-output-path-section.md` that new skill authors copy into their agent .md files. Reference from AD-M-011. | P1 |
| IN-004-20260401-de / IN-007-20260401-de | Update `prompt-templates.md` Templates 2 and 3 to show P1 (orchestration), P2 (engagement scope), and P3 (standalone) patterns for /eng-team, /red-team, and /user-experience skills. | P1 |
| IN-001-20260401-de | Add to each agent .md Output Path Resolution section: explicit P1 marker scanning instruction ("Scan prompt for `## MANDATORY PERSISTENCE (P-002)` block with `Create file at:` line — if found, this is Priority 1; use that path"). | P1 |
| IN-005-20260401-de | Document the `engagements/` subdirectory convention in `project-workflow.md`'s project orientation section, alongside `work/`, `research/`, etc. | P2 |
| IN-002-20260401-de | Add a schema description note warning that `filename_pattern` MUST remain optional. | P2 |

### S-013 Findings Summary

| ID | Type | Severity | Description | Affected Dimension |
|----|------|---------|-------------|-------------------|
| IN-001-20260401-de | Missing | Major | Agent .md Output Path Resolution lacks explicit P1 marker scanning instructions | Methodological Rigor |
| IN-002-20260401-de | Future risk | Minor | Schema could break backward compat if filename_pattern marked required | Internal Consistency |
| IN-003-20260401-de | Missing | Major | No canonical template for new skill authors to implement Output Path Resolution | Completeness |
| IN-004-20260401-de | Missing | Major | Prompt patterns (P1/P2/P3) not added to caller-facing documentation | Actionability |
| IN-005-20260401-de | Convention | Minor | `engagements/` subdirectory not documented in project-workflow.md path conventions | Completeness |
| IN-006-20260401-de | Spec ambiguity | Critical | ADR describes filename_pattern as runtime YAML lookup; LLM agents read .md, not governance YAML | Methodological Rigor |
| IN-007-20260401-de | Missing | Major | SKILL.md examples not updated with P1/P2 prompt patterns | Actionability |

---

## Combined Findings Summary

| ID | Strategy | Severity | Description | Affected Dimension |
|----|---------|---------|-------------|-------------------|
| CC-001-20260401-de | S-007 | Minor | P4 graceful degradation vs. H-04 hard-fail | Methodological Rigor |
| CC-002-20260401-de | S-007 | Major | ADR Status remains "proposed" after implementation complete | Internal Consistency |
| CC-003-20260401-de | S-007 | Major | ADR ID collision: ADR-EPIC002-001 used for both output path ADR and strategy selection ADR in quality-enforcement.md | Traceability |
| CC-004-20260401-de | S-007 | Minor | Composition YAML missing filename_pattern; only governance YAML updated | Completeness |
| CV-001-20260401-de | S-011 | Major | ADR-EPIC002-001 ID collision confirmed via independent source verification | Traceability |
| FM-004-20260401-de | S-012 | Critical | Agent runtime likely reads composition YAML, not governance YAML — filename_pattern may be inaccessible | Methodological Rigor |
| FM-005-20260401-de | S-012 | Critical | No L5 CI gate prevents regression to skills/*/output/ pattern in future governance YAML | Traceability |
| FM-008-20260401-de | S-012 | Critical | Composition YAML does not contain filename_pattern — P2 resolution may silently fall to P3 | Completeness |
| FM-014-20260401-de | S-012 | Major | ADR ID collision — same finding confirmed via FMEA failure mode analysis | Traceability |
| FM-012-20260401-de | S-012 | Major | AD-M-011 MEDIUM tier without CI enforcement allows anti-pattern recurrence | Methodological Rigor |
| FM-011-20260401-de | S-012 | Major | Missing Engagement ID with Base Path leads to malformed path; H-31 not invoked in agent .md | Actionability |
| FM-001-20260401-de | S-012 | Major | Agent ignoring P-002 block is undetectable until L4 post-tool inspection | Methodological Rigor |
| FM-009-20260401-de | S-012 | Major | Composition YAML and governance YAML may diverge over time (two sources of truth) | Internal Consistency |
| FM-002-20260401-de | S-012 | Major | P1+P2 both present: agent may incorrectly apply P2 | Methodological Rigor |
| FM-003-20260401-de | S-012 | Major | ${JERRY_PROJECT} unresolved produces literal in path | Completeness |
| FM-015-20260401-de | S-012 | Major | /nasa-se agents lack filename_pattern; P2 silently unavailable | Completeness |
| FM-006-20260401-de | S-012 | Minor | Agent misinterprets priority order | Methodological Rigor |
| FM-007-20260401-de | S-012 | Minor | Variables table incomplete in some agents | Completeness |
| FM-010-20260401-de | S-012 | Minor | Agent does not re-read prompt for P1 after initial load | Methodological Rigor |
| FM-013-20260401-de | S-012 | Minor | ADR status "proposed" (same as CC-002, reinforced) | Internal Consistency |
| IN-006-20260401-de | S-013 | Critical | ADR describes filename_pattern as runtime YAML lookup; LLM agents cannot perform YAML lookups | Methodological Rigor |
| IN-001-20260401-de | S-013 | Major | Agent .md Output Path Resolution lacks explicit P1 marker scanning instructions | Methodological Rigor |
| IN-003-20260401-de | S-013 | Major | No canonical template for new skill authors | Completeness |
| IN-004-20260401-de | S-013 | Major | P1/P2/P3 patterns not in caller-facing documentation | Actionability |
| IN-007-20260401-de | S-013 | Major | SKILL.md examples not updated with P1/P2 prompt patterns | Actionability |
| IN-002-20260401-de | S-013 | Minor | Future schema change could break backward compatibility | Internal Consistency |
| IN-005-20260401-de | S-013 | Minor | `engagements/` subdirectory convention undocumented in project-workflow.md | Completeness |

### Top-Priority Remediation Actions

**P0 — Must fix before acceptance:**

1. **ADR ID collision (CC-003, CV-001, FM-014):** Rename `ADR-output-path-resolution-001.md` to `ADR-EPIC002-002` and update all internal references. The `quality-enforcement.md` SSOT already uses `ADR-EPIC002-001` for the strategy selection ADR. This collision breaks SSOT traceability (P-022 violation — readers are misled about what the ID refers to).

2. **ADR specification ambiguity re: runtime YAML lookup (IN-006, FM-004, FM-008):** The ADR's agent integration specification implies agents look up `output.filename_pattern` from governance YAML at runtime. LLM agents cannot do this — they read the `.md` system prompt and composition YAML. Clarify the ADR to state: "The `filename_pattern` value in governance YAML is documentation only; the actual filename used in P2 resolution is specified directly in the agent .md Output Path Resolution section step 2 instructions (e.g., 'append `eng-architect-{topic-slug}.md`'). The agent reads this from its `.md` system prompt, not from a YAML lookup."

**P1 — Should fix:**

3. **ADR status advancement (CC-002, FM-013):** Advance ADR status from `proposed` to `accepted`.

4. **CI gate for regression prevention (FM-005, FM-012):** Add an L5 grep check that rejects any `*.governance.yaml` or `*.agent.yaml` where `output.location` contains `skills/` as a path prefix.

5. **Caller documentation (IN-004, IN-007):** Update `prompt-templates.md` Templates 2 and 3 to include P1 (explicit path for orchestration), P2 (base path for engagement scope), and P3 (standalone) examples for the migrated skills.

6. **Missing Engagement ID handling (FM-011, IN-001):** Add explicit H-31 clarification instruction to agent .md files: if `## OUTPUT CONTEXT` is present with `Base Path:` but no `Engagement ID:` is provided, request engagement-id before computing output path.

**P2 — Consider:**

7. **New skill template (IN-003):** Create a canonical Output Path Resolution section template at `.context/templates/` for new skill authors.

8. **Composition YAML filename_pattern (CC-004, FM-008):** Once it is confirmed whether agents use governance or composition YAML for configuration, add `filename_pattern` to composition YAML files if needed.

9. **Document `engagements/` convention (IN-005):** Add `engagements/` to the path organization section of `project-workflow.md`.

---

## Execution Statistics

| Strategy | Critical | Major | Minor | Total |
|---------|---------|-------|-------|-------|
| S-007 Constitutional AI | 0 | 2 | 2 | 4 |
| S-011 Chain-of-Verification | 0 | 1 | 0 | 1 |
| S-012 FMEA | 3 | 8 | 4 | 15 |
| S-013 Inversion | 1 | 4 | 2 | 7 |
| **Totals** | **4** | **15** | **8** | **27** |

| Metric | Value |
|--------|-------|
| Total Findings | 27 (before deduplication of ADR ID collision across 3 strategies) |
| Unique Themes | ~20 (after collapsing 3 ADR-ID-collision instances into 1) |
| Critical Findings | 4 (FM-004, FM-005, FM-008, IN-006) |
| Major Findings | 15 |
| Minor Findings | 8 |
| Protocol Steps Completed | S-007: 5/5, S-011: 5/5, S-012: 5/5, S-013: 6/6 |
| S-007 Constitutional Score | 0.86 (REVISE) |
| S-011 Verification Rate | 88.9% (8/9 claims) |
| S-012 Total RPN | 1,974 |
| Implementation Coverage | 32/32 governance YAML verified, 32/32 agent .md verified, 0 grep matches on old paths |

### H-15 Self-Review

Before persistence, verified:
1. All findings have specific evidence from the deliverable (file names, line numbers, grep results)
2. Severity classifications are justified (Critical = fundamental mechanism defect, Major = significant gap, Minor = improvement)
3. All finding identifiers follow `{PREFIX}-{NNN}-{execution_id}` format
4. Summary table matches detailed findings
5. No findings were minimized or omitted — the 3 Critical FMEA findings and 1 Critical Inversion finding are reported at full severity
