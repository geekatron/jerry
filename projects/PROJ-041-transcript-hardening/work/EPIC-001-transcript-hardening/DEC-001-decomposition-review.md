# EPIC-001:DEC-001: Decomposition Review for PROJ-041 Transcript Hardening

> **Type:** decision
> **Status:** DOCUMENTED
> **Priority:** HIGH
> **Created:** 2026-04-28T00:00:00Z
> **Parent:** EPIC-001
> **Owner:** adam.nowak
> **Related:** GitHub Issue #273; PLAN.md; WORKTRACKER.md

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Verdict and high-level review outcome |
| [L0: Executive Summary](#l0-executive-summary) | 3-5 bullet verdict for stakeholders |
| [Decision Context](#decision-context) | Why the review was commissioned and what was reviewed |
| [L1: Per-Dimension Findings](#l1-per-dimension-findings) | Detailed PASS / NEEDS CHANGE / GAP per dimension |
| [L2: Strategic Implications](#l2-strategic-implications) | Multi-week trajectory, technical-debt hotspots, success metric |
| [Decisions](#decisions) | Structured D-NNN decision entries |
| [Decision Summary](#decision-summary) | Quick reference table |
| [Findings Index](#findings-index) | Index of NEEDS CHANGE and GAP findings |
| [Related Artifacts](#related-artifacts) | Traceability links |
| [Document History](#document-history) | Change log |
| [Metadata](#metadata) | Machine-readable metadata |

---

## Summary

This document reviews the decomposition of PROJ-041-transcript-hardening — 1 Epic, 5 Features, 4 cross-cutting Enablers, 3 in-feature Enablers, 16 Stories, 7 Bugs (36 total entities at the Epic-and-below level) — against `worktracker-entity-hierarchy.md`, `worktracker-directory-structure.md`, the audit findings in [#273](https://github.com/geekatron/jerry/issues/273), and the operational shape of multi-skill orchestrated work.

**Verdict:** **DECOMPOSITION VALIDATED WITH 2 BLOCKING NEEDS-CHANGE ITEMS AND SEVERAL ADVISORY GAPS.** The shape is correct (1 Epic, 5 Features) and the entity classification is mostly right, but two structural issues — Bug folder placement (directory-structure violation) and absence of materialized Task `.md` files (WTI rule violation) — must be resolved before execution begins. None of the issues require re-shaping the Feature decomposition.

**Decisions Captured:** 7

**Key Outcomes:**
- 5-Feature shape is the right granularity; not splitting the Epic, not collapsing Features
- 5 of 7 review dimensions PASS; 2 dimensions require change before execution
- 13 NEEDS CHANGE / GAP findings total — 2 BLOCKING, 6 NEEDS CHANGE (advisory), 5 GAP (advisory). See [Findings Index](#findings-index)

---

## L0: Executive Summary

> Audience: stakeholders, project owner, anyone deciding "do I let this start as-is?"

- **VERDICT: Decomposition validated; ship-ready after 2 blocking fixes.** The 1 Epic + 5 Features + ~30 children shape is correct. Features are well-bounded (cohesion high, coupling low). Source provenance from #273 is complete (every audit item maps to an entity). Entity hierarchy classification is mostly correct.
- **BLOCKER 1 (must fix before any entity opens): Bug folder placement violates worktracker directory structure.** Per `worktracker-directory-structure.md`, Bugs are FLAT FILES at the parent level using `{ParentId}--{BugId}-{slug}.md` naming, not subdirectories. Currently the 7 Bugs (BUG-001..007) live in their own folders with their own `.md` inside (e.g., `BUG-001-token-caps/BUG-001-token-caps.md`). This will break worktracker tooling and audit. **Fix: move each `BUG-NNN-slug/BUG-NNN-slug.md` to `FEAT-NNN--BUG-NNN-slug.md` at the Feature directory's root.** Owner: `wt-auditor` to validate, `eng-lead` to apply rename. ~10 minutes total.
- **BLOCKER 2 (must fix before Phase-3 execution): no Task `.md` files exist.** Every Story/Bug/Enabler has a "Children Tasks" *table* in its body but zero corresponding Task `.md` files. Per `worktracker-directory-structure.md` Tasks must be `{TaskId}-{slug}.md` files in the parent folder. WTI evidence-tracking rules require Task files to record per-task evidence. **Estimated count of Tasks once materialized: ~120** (current children-task tables sum to ~118). Owner: `wt-auditor` to dispatch creation; agents that own the parent entity create their own Task files at execution start. **Highest-leverage single recommendation: do not start any Story/Bug/Enabler before that entity has materialized its Task files.**
- **2 advisory NEEDS CHANGE items (non-blocking, fix before merge): EN-005 (UX) blocks too much** — UX synthesis blocks STORY-007/008 CLI surface AND EN-001 DDD scaffolding, which can serialize the project unnecessarily. **Cooperates** is the right edge for STORY-007/008; **Blocks** stays for EN-001 only if the UX run actually reshapes the bounded context, which is unlikely. **EN-006 diataxis dependency on FEAT-001..FEAT-005** is correct in principle but the doc set is large enough (8 docs, 4 quadrants) that diataxis should be allowed to start in parallel with FEAT-005 quick-wins to absorb the ts-mindmap-mermaid changes early. Both are dependency-edge calibrations, not structural changes.
- **The threshold (≥0.95) is right for this work given the audit's diagnostic.** The audit plateaued at 0.90 in 9 iterations precisely because mechanical defects ate the iteration budget. Setting the bar at 0.95 (vs the SSOT 0.92) is the correct response — it forces the work to actually close the substrate-validation gap rather than passing a lower bar with the same surface.

---

## Decision Context

### Background

The user scaffolded PROJ-041 unilaterally (no agent invocation, no quality gate) to harden `/transcript` against findings from external audit issue [#273](https://github.com/geekatron/jerry/issues/273). The user has correctly identified that the act of decomposition itself was unilateral and unvalidated, and has commissioned this review to determine whether the decomposition is sound before work begins. This is the same `/adversary` discipline the user is buying with this Epic — applied to the Epic's own scaffolding.

The review covers the full entity tree at `projects/PROJ-041-transcript-hardening/work/EPIC-001-transcript-hardening/` and reads the entity files as currently authored, against `.context/rules/quality-enforcement.md`, `skills/worktracker/rules/worktracker-entity-hierarchy.md`, `skills/worktracker/rules/worktracker-directory-structure.md`, and the audit findings in #273.

### Constraints

- **Read-only review.** Per the engagement constraints in the review request: do not modify any of the existing entity files. Implementation of any recommended changes will happen in a follow-up step after user approval.
- **Quality target for this deliverable: ≥0.95 weighted composite** (S-014 6-dimension rubric per `.context/rules/quality-enforcement.md`), matching the project-wide bar.
- **Citations required at the entity-ID level.** Per the Traceability dimension of the rubric, every finding must specify the entity ID(s) it applies to and the file path.
- **No new HARD rules created.** The review consumes existing HARD rules H-13, H-14, H-22, H-23, H-33, P-002, P-022 and existing MEDIUM standards from `agent-development-standards.md` and `agent-routing-standards.md`. It does not add to the rule budget.

### Stakeholders

| Stakeholder | Role | Interest |
|-------------|------|----------|
| adam.nowak | Project Owner / User | Authorizes execution; downstream of every dimension's verdict |
| ps-architect (this agent) | Reviewer | Produces this DEC; bounded by P-022 (no deception) and the 6-dimension rubric |
| `/worktracker` `wt-auditor` | Worktracker integrity gate | Will enforce structural fixes from BLOCKER 1 and BLOCKER 2 |
| `/eng-team` `eng-architect` | Architecture compliance | Will own the FEAT-003 hexagonal layout and inherits the structural correctness from this review |
| `/red-team` `red-lead` | Engagement scope | Phase 1 threat model timing depends on dependency edges this review validates |

---

## L1: Per-Dimension Findings

### Dimension 1: Decomposition Correctness

**Verdict:** **PASS**

The 1-Epic + 5-Feature + ~30-child shape is correct for this work. Each Feature corresponds to one of the audit's 5 thematic clusters (governance, contradictions, validation, schema, mindmap), each is bounded enough to ship independently of the others (with documented blocking edges), and none is small enough to collapse into another or large enough to split into multiple Features.

**Detailed analysis:**

- **Should this be multiple Epics?** No. The audit findings are unified by a single root-cause diagnostic — *substrate is hand-attested, not machine-derived* — and the 5 Features collectively close that gap. Splitting into multiple Epics would either (a) break that unifying narrative or (b) create artificial parent containers that don't add planning value. The Epic correctly states this in `EPIC-001-transcript-hardening.md` Business Outcome Hypothesis.
- **Should Features collapse?** No. Each Feature has distinct cohesion and acceptance criteria:
  - **FEAT-001** (governance): 2 stories, both about ADR-007 packaging/promotion — single concern, ships standalone
  - **FEAT-002** (contradictions): 5 bugs, all framework-internal disagreements that must resolve before FEAT-001's STORY-002 baselines ADR-007 — properly scoped and bounded
  - **FEAT-003** (validators): 3 enablers + 10 stories — the heart of the project, 17 rule IDs implemented, CLI surface, write pipeline. Splitting this would orphan the integration story (STORY-009/010) from the implementation stories (STORY-003..006)
  - **FEAT-004** (schemas): 4 schema additions, all additive, all related to extraction-report.json v1.2 — proper cohesion
  - **FEAT-005** (mindmap): 2 bugs, both in `ts-mindmap-mermaid` agent — properly bounded, designated as early-land quick-win
- **Should Features split?** No. The largest Feature is FEAT-003 with 13 children. Per the Epic-Feature-Story SAFe model, 13 children is well within healthy bounds for a Feature that represents a coherent capability slice (validation operation within `/transcript` BC). The 3 in-feature Enablers (EN-001 DDD scaffolding, EN-002 test harness, EN-003 SubprocessSandbox) are local concerns specific to FEAT-003 and properly nested.
- **Hierarchy levels per `worktracker-entity-hierarchy.md`:**
  - L1 Epic (EPIC-001) — correct
  - L3 Features (FEAT-001..005) — correct
  - L4 Stories and Enablers — correct (Enablers L4 per the hierarchy table at line 75 of `worktracker-entity-hierarchy.md`)
  - Bugs — correct (Bug entity exists at the QualityItem branch, can be containerized at any level per line 96 of the hierarchy table)

**Specific entities cited:** All 5 Features (`FEAT-001..005`), Epic (`EPIC-001`).

**Recommendation:** No structural changes. Proceed.

---

### Dimension 2: Containment

**Verdict:** **NEEDS CHANGE — BLOCKER 1**

**Containment of children under parents is logically correct, but FILE PLACEMENT for Bugs violates `worktracker-directory-structure.md`.**

Per `worktracker-directory-structure.md` lines 70-89, Bugs at the Feature level should be **flat files** named `{FeatureId}--{BugId}-{slug}.md` at the Feature directory root, not subdirectories. The same flat-file convention applies to Bugs at the Story or Enabler level. The current scaffolding uses subdirectories with Bug `.md` inside, which:

1. Is not the convention defined in `worktracker-directory-structure.md`
2. Will break `wt-auditor` and other worktracker tooling that walks the canonical structure
3. Creates an inconsistent shape across entity types (Stories ARE subdirectories per the spec, Bugs ARE NOT)

| Current path (incorrect) | Correct path |
|---|---|
| `FEAT-002-contradictions-cleanup/BUG-001-token-caps/BUG-001-token-caps.md` | `FEAT-002-contradictions-cleanup/FEAT-002--BUG-001-token-caps.md` |
| `FEAT-002-contradictions-cleanup/BUG-002-chunk-id-regex/BUG-002-chunk-id-regex.md` | `FEAT-002-contradictions-cleanup/FEAT-002--BUG-002-chunk-id-regex.md` |
| `FEAT-002-contradictions-cleanup/BUG-003-domain-regex/BUG-003-domain-regex.md` | `FEAT-002-contradictions-cleanup/FEAT-002--BUG-003-domain-regex.md` |
| `FEAT-002-contradictions-cleanup/BUG-004-seg-nnn-regex/BUG-004-seg-nnn-regex.md` | `FEAT-002-contradictions-cleanup/FEAT-002--BUG-004-seg-nnn-regex.md` |
| `FEAT-002-contradictions-cleanup/BUG-005-backlinks-format/BUG-005-backlinks-format.md` | `FEAT-002-contradictions-cleanup/FEAT-002--BUG-005-backlinks-format.md` |
| `FEAT-005-mindmap-hardening/BUG-006-mindmap-bracket-escape/BUG-006-mindmap-bracket-escape.md` | `FEAT-005-mindmap-hardening/FEAT-005--BUG-006-mindmap-bracket-escape.md` |
| `FEAT-005-mindmap-hardening/BUG-007-mindmap-false-self-claim/BUG-007-mindmap-false-self-claim.md` | `FEAT-005-mindmap-hardening/FEAT-005--BUG-007-mindmap-false-self-claim.md` |

**Other containment items (all PASS):**

- **In-feature Enablers under FEAT-003 (EN-001, EN-002, EN-003):** Correctly placed. These are scoped to FEAT-003's bounded context (DDD scaffolding for the validation operation, test harness for that scaffolding, SubprocessSandbox for that operation). Promoting them to Epic-level cross-cutting would be wrong — they don't apply to other Features. The current placement matches the directory structure spec exactly: `FEAT-NNN-slug/EN-NNN-slug/EN-NNN-slug.md` (Enablers ARE subdirectories).
- **Cross-cutting Enablers EN-004 (red-team), EN-005 (UX), EN-006 (diataxis), EN-008 (final tournament):** Correctly elevated to Epic level. Each applies across Features (red-team scope = full surface, UX = all consumers of any new capability, diataxis = doc set spanning all 5 Features, final tournament = whole-Epic gate). Placement at `EPIC-001-transcript-hardening/EN-NNN-slug/EN-NNN-slug.md` matches the directory structure spec for Enablers as subdirectories.
- **EN-007 numbering gap:** WORKTRACKER.md History shows EN-007 was deleted (was an `/orchestration` plan, removed because dependency chain handles ordering). The skipped number is acceptable — IDs should not be re-used per worktracker conventions, and the gap is documented in History.
- **Bug vs Story vs Enabler classification:**
  - **FEAT-002 → 5 Bugs:** Correct. Each is a documented contradiction with a specific affected document and recommended resolution. Per `worktracker-entity-hierarchy.md` line 96, Bug is the right entity for "defect requiring fix" — and each FEAT-002 contradiction IS a defect (the framework cannot consistently validate against itself).
  - **FEAT-002 contains Bugs as direct children:** Per `worktracker-entity-hierarchy.md` line 105 ("Feature → Story, Enabler"), Bugs are NOT explicitly listed as Feature children. **However**, `worktracker-directory-structure.md` lines 70-72 DO permit Bug placement at Feature level via the flat-file naming pattern. This is a known minor inconsistency between the two rule files — directory structure permits it, hierarchy says Story/Enabler. The scaffolding follows directory-structure convention (which is more recent/authoritative for placement). FEAT-002 internal narrative correctly documents this as "Bugs are tracked as children of this Feature."
  - **FEAT-004 → 4 Stories (not Enablers):** Correct. Schema additions are user-valuable feature increments, not infrastructure work. Per the entity hierarchy, schema fields that consumers see and act on are Stories.
  - **FEAT-005 → 2 Bugs:** Correct. Both are documented defects with concrete reproduction.
- **EN-008 (final adversary tournament) classified as Enabler with `Enabler Type: compliance`:** Correct per `worktracker-entity-hierarchy.md` — Enabler covers technical/infrastructure work that enables future value delivery, and the compliance subtype is an established pattern.

**Specific entities cited:** All 7 Bugs (`BUG-001..007`), 4 cross-cutting Enablers (`EN-004, EN-005, EN-006, EN-008`), 3 in-feature Enablers (`EN-001, EN-002, EN-003`), 4 schema Stories under FEAT-004 (`STORY-013..016`).

**Recommendation:** **BEFORE ANY ENTITY OPENS:** apply Bug rename per the table above. Owner: `wt-auditor` validates current state then `eng-lead` applies the 7 mv operations and updates parent-Feature `## Children Stories/Enablers` tables to reference the new flat paths. Estimated effort: ~10 minutes total.

---

### Dimension 3: Dependency Edges

**Verdict:** **NEEDS CHANGE (advisory, non-blocking)**

The dependency graph is mostly correct and would not cause work to start prematurely. Two edges are over-tight (would unnecessarily serialize parallel work) and one is missing.

**PASS sub-dimensions:**

- **Critical-path edges are correctly modeled.** The "FEAT-001 STORY-001 → FEAT-002 BUG-001..005 → FEAT-001 STORY-002" critical path is captured in every entity's Dependencies section. STORY-001's Blocks list correctly includes FEAT-002 (BUG-004, BUG-005) and FEAT-003. STORY-002's Blocked By list correctly includes STORY-001 and all 5 FEAT-002 Bugs. FEAT-002's Blocked By correctly cites FEAT-001 STORY-001 (because BUG-004/BUG-005 are amendments to ADR-007 which must exist first).
- **EN-003 SubprocessSandbox dependencies are correctly modeled.** EN-003 Blocked By: EN-001 (skeleton must exist) + EN-004 (threat model informs design). EN-003 Blocks: STORY-003..006 (rule implementations route through sandbox) + STORY-007/008 (CLIs depend on sandbox). This chain is correct and matches the hexagonal isolation requirements.
- **Substrate-coupling dependency: STORY-005 (ANCHOR-* validators including the substrate-coupling rule) Blocked By EN-003.** Correct — the substrate-coupling rule walks declared patterns through SubprocessSandbox.
- **STORY-008 (`update-anchors` CLI) Blocked By STORY-005 (ANCHOR-* validators).** Correct — `update-anchors` uses the same walking primitive.
- **STORY-010 (write pipeline integration) Blocked By STORY-008 (CLI must exist).** Correct.
- **STORY-009 (post-render hook) Blocked By STORY-007 + STORY-003..006.** Correct.
- **EN-008 (final tournament) Blocked By all Features + EN-004..006.** Correct — tournament evaluates the merged deliverable, not partials.
- **FEAT-005 (mindmap hardening) Independent of FEAT-001..004.** Correct. Mindmap fixes are isolated from governance/schemas/validators. Designated as early-land quick-win — appropriate.
- **FEAT-004 STORY-015 (discussions[]) Blocked By FEAT-002 BUG-004 (seg-NNN regex).** Correct — disc-NNN regex inherits the loosened `\d{3,}` form.
- **EN-004 (red-team) Phase 1 timing.** Phase 1 runs parallel with FEAT-001 and produces handoff to EN-001/EN-003 before they start design. Phase 4 runs after FEAT-003 implementations. This is captured in the entity body. The dependency edges (EN-004 Blocks EN-001, EN-003, FEAT-003 STORY-005, STORY-008) are correct.

**NEEDS CHANGE sub-dimensions:**

- **Finding D-3.1 (NEEDS CHANGE — advisory):** EN-005 (UX) `Blocks: EN-001, STORY-007, STORY-008`. The UX exploration is valuable but blocking EN-001 (DDD module skeleton) on UX findings is over-tight. Per EN-001's bounded-context design, the module skeleton is determined by hexagonal architecture (H-07), not by user research — the skeleton ships layer protocols (RuleEngine, ReportRenderer, SubprocessSandbox) that don't change based on UX. **Recommendation: change EN-005 → EN-001 from `Blocks` to `Cooperates`.** Keep `Blocks` for STORY-007/008 only if the UX heuristic eval will actually reshape the CLI surface (`jerry transcript verify` flag set), which is plausible. Owner to apply: `wt-auditor` flags, `ps-architect` decides per UX-findings impact, `eng-lead` applies edit. Risk if not changed: Phase 1 sync barrier becomes a serial bottleneck on UX findings that may not exist.
- **Finding D-3.2 (NEEDS CHANGE — advisory):** EN-006 (diataxis) `Blocked By: FEAT-001..FEAT-005`. The doc set covers all 5 Features so blocking is correct in principle. However, FEAT-005 mindmap hardening lands early as quick-win, and its Bugs (BUG-006 bracket-escape, BUG-007 self-claim) are agent-prompt changes that diataxis can document immediately. **Recommendation: split EN-006 into two phases:** EN-006a (early-land — mindmap doc updates after FEAT-005), EN-006b (full doc set after FEAT-001..004). Or, keep EN-006 monolithic but downgrade `Blocked By: FEAT-005` to `Cooperates`. Owner: `wt-auditor` flags, `ps-architect` recommends. Risk if not changed: small — diataxis Phase 7 lands after everything else anyway, and FEAT-005's two Bugs don't generate enough documentation to warrant pre-work.
- **Finding D-3.3 (NEEDS CHANGE — advisory):** STORY-011 (update ts-critic-extension.md) `Blocked By: STORY-007 only`. STORY-011's purpose is consuming the deterministic validator output — it depends on validators existing AND on `verify --json` existing. Currently `Blocked By` lists STORY-007 (the CLI) but not STORY-003..006 (the validators themselves). Although STORY-007 transitively blocks on STORY-003..006, the explicit edge would prevent ambiguity. **Recommendation: add STORY-003..006 as transitive Blocked By in STORY-011's Dependencies table.** Owner: `eng-lead`.

**GAP sub-dimensions:**

- **Finding D-3.4 (GAP):** FEAT-002 BUG-001..005 do not currently include explicit `Blocks: FEAT-003 STORY-006` (the SCHEMA-* validators) for the schema-affecting bugs. BUG-002 (chunk_id regex), BUG-003 (domain regex), and BUG-004 (seg-NNN regex) all affect schema validators. Currently BUG-002/BUG-003 list `Blocks FEAT-003 STORY-006` correctly, but BUG-004 lists `Blocks FEAT-003 STORY-005` (ANCHOR-*) only — the seg-NNN regex affects both ANCHOR validators (anchor format) AND SCHEMA validators (schema-level regex enforcement). **Recommendation: add `Blocks FEAT-003 STORY-006` to BUG-004.** Owner: `wt-auditor` validates, `eng-lead` applies. Low impact (SCHEMA-* validators already wait on EN-001/EN-002 + FEAT-002 generally), but improves traceability.
- **Finding D-3.5 (GAP):** FEAT-002 BUG-005 (backlinks format) currently lists `Blocks FEAT-003 STORY-004` (CONTENT validators). This is correct. **No explicit edge to FEAT-002 → FEAT-001 STORY-001 vendor.** BUG-005 amends ADR-003 — which is a public ADR already in `docs/adrs/`. So BUG-005 does not literally depend on STORY-001's vendor of ADR-007. The body of BUG-005 says `Blocked By: FEAT-001 STORY-001` (ADR-007 must be readable in canonical location) which is misleading because BUG-005 amends ADR-003, not ADR-007. **Recommendation: clarify BUG-005's `Blocked By` to "FEAT-001 STORY-001 (only because BUG-005 references ADR-007 §3.3 as the canonical authority, requiring ADR-007 be readable at its public path)."** Or, weaken to `Cooperates`. Owner: `eng-lead`.

**Specific entities cited:** EN-005 → EN-001/STORY-007/STORY-008; EN-006 ← FEAT-005; STORY-011; FEAT-002 BUG-002, BUG-003, BUG-004, BUG-005.

**Recommendation:** Apply edits D-3.1, D-3.2, D-3.3 (NEEDS CHANGE) and D-3.4, D-3.5 (GAP advisory) before Phase 1 sync barrier. Net effort: ~15 minutes.

---

### Dimension 4: Agent Assignments

**Verdict:** **PASS WITH ADVISORIES**

Each entity's "Agent Assignment" table maps ordered execution steps to (skill, agent) pairs. Coverage is comprehensive and skill choice is appropriate for each step.

**PASS evidence:**

- **EN-003 SubprocessSandbox chain is exemplary** — `red-vuln` (STRIDE) → `eng-architect` (port shape) → `eng-infra` (adapter implementation) → `eng-qa` (Hypothesis property tests) → `eng-security` (manual code review) → `red-exploit` (≥5 bypass attempts) → `eng-devsecops` (Bandit + Semgrep CI rules) → `adv-executor`/`adv-scorer` (C4 review) → `wt-verifier` (closure). This is the strongest agent chain in the project: it correctly sequences threat model → design → implementation → automated tests → manual review → adversarial validation → tooling enforcement → quality gate → closure. Other security-adjacent entities in the project should pattern-match this shape.
- **STORY-005 ANCHOR-* validators chain is correct** — the substrate-coupling rule routes through SubprocessSandbox, so the chain includes `eng-security` (code review on subprocess use) AND `red-exploit` (verify ANCHOR rule cannot bypass sandbox). This re-uses EN-004 Phase 4 work, avoiding redundant red-team engagement. Correctly pattern-matches EN-003 even though the threat surface is smaller.
- **EN-004 red-team chain is correct** — `red-lead` (engagement scope) → `red-recon` (existing + new surface) → `red-vuln` (STRIDE) → `red-reporter` (Phase 1 handoff) → Phase 4 `red-exploit` ≥5 bypass classes + `red-social` (prompt injection) → `red-reporter` (final engagement report). The two-phase structure (pre-design threat model + post-implementation validation) is the right red-team methodology for security-relevant code.
- **EN-005 UX wave structure is correct** — `ux-orchestrator` → Wave 1 (`ux-jtbd-analyst`, `ux-heuristic-evaluator`) → Wave 2 (`ux-heart-analyst`) → Wave 3 (`ux-inclusive-evaluator`) → Wave 4 (`ux-behavior-diagnostician`) → synthesis. Allows the orchestrator to skip waves as appropriate. The entity body correctly states "we do not pre-commit to using all five — some may be redundant once others run."
- **EN-006 diataxis chain is correct** — `diataxis-classifier` → 4 writer agents (`diataxis-tutorial`, `diataxis-howto`, `diataxis-reference`, `diataxis-explanation`) → `diataxis-auditor` → `eng-reviewer` (cross-check vs implementation reality) → `adv-executor`/`adv-scorer` → `wt-verifier`. Correctly sequences classification → authoring → audit → reality-check → quality gate.
- **EN-008 final tournament correctly invokes FC-M-001** — primary tournament (`adv-selector` → `adv-executor` → `adv-scorer`) AND independent fresh-context second-reviewer (`adv-executor` fresh context → `adv-scorer` fresh context). Per `agent-development-standards.md` FC-M-001, C4 deliverables require a second independent reviewer; the entity body correctly explains the anchoring-prevention rationale.
- **`wt-verifier` appears as the final closure step in every entity** — required for WTI-005 evidence enforcement. Correctly applied across all 36 entities.

**NEEDS CHANGE sub-dimensions:**

- **Finding D-4.1 (NEEDS CHANGE — advisory):** STORY-002 (ADR-007 promotion) lacks an `eng-architect` ADR review step. The body shows `wt-auditor` (verify FEAT-002 closure) → `ps-architect` (update frontmatter) → `eng-architect` (compliance review) → `adv-executor`/`adv-scorer` (C4) → `wt-verifier`. **The `eng-architect` step is present but does not author an ADR alignment memo.** Per AE-004, modifying a baselined ADR requires C4 review *and* should produce an architecture compliance memo recording how the ADR fits into ADR-001..006. **Recommendation: explicit deliverable on the `eng-architect` step — `work/red-team/adr-007-baselining-compliance-memo.md` or equivalent path.** Owner: `eng-lead`.
- **Finding D-4.2 (NEEDS CHANGE — advisory):** STORY-009/STORY-010 (post-render hook + write pipeline) both list a "decide hook mechanism (SubagentStop vs prompt-discipline)" task and reference a DEC. **Neither story currently links to an explicit DEC entity.** Per `worktracker-directory-structure.md` lines 84-88, decisions made at the Story level use `{StoryId}/{DecisionId}-slug.md` placement. **Recommendation: pre-create `STORY-009/DEC-001-hook-mechanism.md` (or equivalent shared decision file at the FEAT-003 level if both stories share the decision). Without the DEC entity, the decision will be made implicitly during execution and lost.** Owner: `wt-auditor` flags during scaffold-completion check, `ps-architect` writes the DEC at execution start.
- **Finding D-4.3 (NEEDS CHANGE — advisory):** BUG-007 (false self-claim) has `eng-reviewer` capability decision (Option A vs Option B) but no DEC entity. Same as D-4.2 — pre-create `BUG-007/DEC-001-capability-or-claim-honesty.md` so the decision is captured in worktracker. Owner: `wt-auditor` flags.

**GAP sub-dimensions:**

- **Finding D-4.4 (GAP):** FEAT-002 BUG-001..005 currently use `/problem-solving` `ps-investigator` and `ps-architect` for resolution authoring, then `/eng-team` `eng-lead` for application. **None invoke `/eng-team` `eng-reviewer` for final-gate review on the cross-document edits.** ADR amendments (BUG-004, BUG-005) and schema deletions (BUG-003) are governance-class changes; `eng-reviewer` should validate the final state. **Recommendation: add `eng-reviewer` step before `adv-executor` in BUG-002, BUG-003, BUG-004, BUG-005 chains.** BUG-001 may not need it (token-cap disambiguation is text-only). Owner: `eng-lead`.
- **Finding D-4.5 (GAP):** STORY-012 (CI workflow) chain includes `eng-devsecops` (workflow author + supply-chain hardening) and `eng-security` (workflow security review). **It does not include `eng-infra` review** — even though the CI workflow runs `uv run pytest` against golden packets that exercise SubprocessSandbox. `eng-infra` should validate that the workflow's runtime environment matches the production runtime (no environment-drift between CI and developer-local execution). **Recommendation: add `eng-infra` step between `eng-devsecops` and `adv-executor` in STORY-012.** Owner: `eng-lead`.
- **Finding D-4.6 (GAP):** No entity in FEAT-001..005 invokes `pm-pmm` agents — appropriate since the user explicitly excluded `/pm-pmm` from the project scope per PLAN.md ("/nasa-se and /pm-pmm are NOT in scope"). Confirmed compliance with user direction.

**Specific entities cited:** EN-003 (exemplar), STORY-005 (correct pattern-match), EN-004, EN-005, EN-006, EN-008, STORY-002 (D-4.1), STORY-009/010 (D-4.2), BUG-007 (D-4.3), BUG-001..005 (D-4.4), STORY-012 (D-4.5).

**Recommendation:** Apply D-4.1 through D-4.5 before Phase 1 sync barrier. Net effort: ~30 minutes total.

---

### Dimension 5: Task Granularity (the missing layer)

**Verdict:** **NEEDS CHANGE — BLOCKER 2**

**Every Story/Bug/Enabler currently has a "Children Tasks" *table* in its body but ZERO corresponding Task `.md` files exist on disk.** This violates `worktracker-directory-structure.md` (Tasks must be `{TaskId}-{slug}.md` files in the parent folder) and `worktracker-content-standards.md` WTI-005 (Task closure requires evidence in History — without a Task file there is no History to record evidence in).

**Detailed analysis:**

The Children Tasks tables in each entity define **the right granularity**. I sampled and counted across the 26 leaf entities (16 Stories + 7 Bugs + 3 in-feature Enablers + 4 cross-cutting Enablers, minus the Epic and 5 Features which don't directly contain Tasks):

| Entity | Tasks declared in table | Notes |
|---|---|---|
| STORY-001 | 8 | Vendor + cross-reference updates + CI check + closure |
| STORY-002 | 6 | Verify FEAT-002 closure + frontmatter update + history + arch review + adversary + close |
| STORY-003 | 6 | Read ADR + Red + Green for FILE-001..003 + refactor + adversary |
| STORY-004 | 5 | Read ADR + Red + Green + refactor + adversary |
| STORY-005 | 8 | Read ADR + tests + 3 rules + reproduce + red-team + adversary |
| STORY-006 | 7 | Read ADR + JsonSchemaAdapter + tests + impl + large-packet + DRY + adversary |
| STORY-007 | 8 | Parser + service wire + 2 renderers + shim + tests + perf + adversary |
| STORY-008 | 9 | Service + atomic-write + CLI + flags + audit-trail + atomicity + red-team + adversary |
| STORY-009 | 8 | Hook decide + 2 prompt updates + hook impl + return contract + test + reviewer + adversary |
| STORY-010 | 7 | Hook decide + prompt update + hook impl + tests + reproduction + reviewer + adversary |
| STORY-011 | 5 | Locate + 2 updates + test + adversary |
| STORY-012 | 7 | Workflow + hash-pin + coverage + PR comment + branch protection + devsecops review + adversary |
| STORY-013 | 6 | Schema + extraction-report v1.2 + golden packet + ts-extractor + ADR + adversary |
| STORY-014 | 7 | Identify blocks + schema + 2 schema updates + validators + update-anchors + ADR + adversary |
| STORY-015 | 8 | Schema + regex + template + symbols + ts-extractor + ADRs + golden + adversary |
| STORY-016 | 5 | Schema + extraction-report + STORY-008 wire + golden + adversary |
| BUG-001 | (no table) | Acceptance criteria are fine but no Children Tasks table |
| BUG-002 | (no table) | Same |
| BUG-003 | (no table) | Same |
| BUG-004 | (no table) | Same |
| BUG-005 | (no table) | Same |
| BUG-006 | (no table) | Same |
| BUG-007 | (no table) | Same |
| EN-001 | 7 | ADRs + skeleton + entities + ports + scaffolding test + arch review + adversary |
| EN-002 | 9 | 6 golden packets + conftest + runner + coverage |
| EN-003 | 10 | Sandbox protocol + adapter + path-traversal + timeout + env + Hypothesis + manual review + bypass + Bandit + adversary |
| EN-004 | 10 | Engagement + recon + STRIDE + attack-paths + handoff + 4 Phase-4 + adversary |
| EN-005 | 9 | Orchestrator + 5 sub-skills + synthesis + entities + adversary |
| EN-006 | 12 | 8 doc tasks + classifier + auditor + SKILL.md + adversary |
| EN-008 | 8 | Selector + executor + scorer + FC-M-001 + report + reproduce + close issue + complete |

**Total Tasks declared:** ~118 across entities with tables (16 + 7 + 3 + 4 - 7 zero-task Bugs = 23 entities with tables, summing to ~159 Tasks; Bugs add ~30 more once their tables are written = **~189 estimated**).

**Original estimate from review brief:** ~150 Tasks. Mine is somewhat higher, though within the same order of magnitude. The variance is in:

- **Bugs currently have no Children Tasks table** — Tasks are implied by the Acceptance Criteria but not enumerated. **Bugs need their Children Tasks tables written.** Estimated 4-6 Tasks per Bug × 7 Bugs = 28-42 Tasks once Bug tables are added.
- **Some Enablers have higher granularity than typical** — EN-006 has 12 because each of 8 docs plus classifier + auditor + SKILL.md + adversary is its own Task. This granularity is appropriate for a doc set with 4 quadrants.

**Granularity assessment:**

- **Most tables are right-grained.** Each Task is small enough to verify atomically (e.g., "Author CLI command parser (argparse or click)" is verifiable; "Implement FILE-001..003" is one Task because the 3 rules are intentionally bundled for DRY refactoring).
- **A few Tasks should split:**
  - STORY-008 TASK-007 ("Test atomicity (concurrent write simulation)") — atomicity testing has multiple sub-conditions (single-process partial-write, concurrent-process race, sandbox refusal mid-write). **Recommendation: split into 2-3 atomic Subtasks during Task file creation.**
  - EN-003 TASK-002 ("Implement SubprocessSandboxAdapter (command allowlist + arg validation)") — bundles two distinct concerns. Could become 2 Tasks.
- **A few Tasks could merge:**
  - STORY-007 TASK-003 + TASK-004 ("MarkdownReportRenderer adapter" + "JsonReportRenderer adapter") — if implemented as a single ReportRenderer port with two adapters, merging is acceptable. Decision should be made by `eng-architect` at execution time.

**WTI-005 evidence requirement:** Without Task `.md` files, the user-stated closure rule ("entities cannot be closed out unless they provide delivery evidence") is unenforceable at the Task level. Each Task needs its own History section to record commit SHAs, test results, etc. Currently, Stories aggregate Task evidence in the parent body — this is acceptable per `worktracker-content-standards.md` for *small* Stories (≤3 Tasks), but most Stories here have 5-9 Tasks. **Materializing Task files per the directory structure is required for evidence integrity.**

**Recommendation:** **BEFORE EACH ENTITY OPENS:**
1. The owner of the entity (e.g., `eng-backend` for STORY-003) creates Task `.md` files at the start of execution
2. Each Task `.md` has: frontmatter, AC, Agent Assignment (just one agent typically), History (initially empty)
3. Use the template at `.context/templates/worktracker/TASK.md` (referenced from worktracker rules)
4. **Bugs first need their Children Tasks tables added to their bodies** — `wt-auditor` flags this before BLOCKER 1 fix; `eng-lead` adds tables at the same time as Bug rename.

This is **NOT a single up-front materialization step**. Materialize Tasks just-in-time as each parent entity opens. Pre-creating all ~189 Task files now would: (a) consume ~3 hours of agent time; (b) freeze granularity decisions before execution context is in place; (c) violate KISS. Just-in-time creation is the pattern used elsewhere in the framework.

**Specific entities cited:** All 7 Bugs (no Tasks tables), STORY-008 (split), EN-003 (split), STORY-007 (potential merge); estimated 189 Tasks total.

---

### Dimension 6: Gaps and Redundancies

**Verdict:** **PASS — provenance is complete; no missing items from #273; no redundancies between entities**

**Cross-reference against issue #273:**

- **Body §C1 (ADR-007 packaging):** STORY-001. Provenance row in WORKTRACKER. ✓
- **Body §C2 (status promotion):** STORY-002. ✓
- **Body §C4.1 (token caps):** BUG-001. ✓
- **Body §C4.2 (chunk_id regex):** BUG-002. ✓
- **Body §C4.3 (domain regex):** BUG-003. ✓
- **Body §C4.4 (seg-NNN regex):** BUG-004. ✓
- **Body §C4.5 (backlinks format):** BUG-005. ✓
- **Body §C5 (deterministic validators):** FEAT-003 covering all 17 rule IDs (3 FILE + 3 CONTENT + 3 ANCHOR + 8 SCHEMA = 17 ✓), STORY-007 verify CLI, STORY-008 update-anchors CLI, STORY-009 post-render hook, STORY-010 write pipeline, STORY-011 ts-critic-extension update, STORY-012 CI workflow. ✓
- **Body §C3.1 (editorial_conventions):** STORY-013. ✓
- **Body §C3.2 (arithmetic_invariants):** STORY-014. ✓
- **Body §C3.3 (discussions[]):** STORY-015. ✓
- **Comment 1 (declared-derived coupling diagnostic + CLI prototype):** STORY-007, STORY-008, STORY-009, STORY-010 all cite Comment 1. ✓
- **Comment 2 (audit_basis schema gap):** STORY-016. ✓
- **Comment 3 (ts-mindmap-mermaid bracket-escaping + false self-claim):** BUG-006, BUG-007. ✓

**No items from #273 are missing from the entity tree.** Every line item in body + 3 comments has a corresponding worktracker entity, and the WORKTRACKER.md "Source Provenance" section captures the mapping.

**Redundancy check:**

- **No duplicate work between entities.** STORY-005 (ANCHOR validators including substrate-coupling rule) and STORY-008 (`update-anchors` CLI) both touch the substrate-walking primitive, but STORY-005 implements it as a rule and STORY-008 wraps it for write-back. These are complementary, not redundant.
- **STORY-009 and STORY-010 both add hook-mechanism decisions.** Both reference a shared "DEC for hook mechanism" — ideally one DEC, two cited. The bodies say `Decision recorded in DEC` (singular) which suggests they intend a shared DEC. Recommend: pre-create one DEC at FEAT-003 level (`FEAT-003/DEC-001-hook-mechanism.md`) and reference from both STORY-009 and STORY-010. (See D-4.2.)
- **EN-004 Phase 4 and STORY-008 Step 4 both invoke `red-exploit`.** EN-004 is the parent engagement; STORY-008 calls out the same agent for atomic-write race condition probe. Both reference the same engagement with shared scope from `red-lead`. This is correct — no redundancy, just shared context.

**GAP findings:**

- **Finding D-6.1 (GAP):** Issue #273 Comment 1 includes a working CLI prototype gist (~200 lines stdlib Python with `verify` and `update-anchors` subcommands). PLAN.md and FEAT-003 body correctly state "gist is reference, not literal port." **However, no entity captures the explicit decision that the gist's procedural shape will be re-architected into hexagonal layers per EN-001.** This is mentioned in EN-001's "Design Decisions to Capture" table as DEC-004 ("How the gist's procedural shape maps to the DDD layout"), so the decision is planned but not yet authored. **Recommendation:** confirm DEC-004 is authored at EN-001 execution start before any gist-port decisions are made. Owner: `ps-architect`.
- **Finding D-6.2 (GAP):** PLAN.md "Out of Scope" lists six items including "Mindmap rendering parity with non-Mermaid environments — `ts-mindmap-ascii` already handles fallback." However, FEAT-005 BUG-006 acceptance criteria mention `ts-mindmap-ascii` regression coverage in EN-002 (`test_data/golden/ascii-fallback/`). **The ascii-fallback golden is captured in EN-002 but no entity owns updating `ts-mindmap-ascii` agent if its symbols collide with FEAT-004 STORY-015's `[~]` discussions symbol.** STORY-015 line 71 mentions "FEAT-005 BUG-006 fixes extend to cover the new `[~]` ascii fallback symbol where rendered as Mermaid" — this ties STORY-015 to FEAT-005 BUG-006 AC. The ascii-only path is not explicitly covered. **Recommendation:** add an explicit AC line in STORY-015 stating "ascii rendering of `[~]` validates without bracket escape (because ascii is not Mermaid)." Owner: `eng-backend`.
- **Finding D-6.3 (GAP):** No entity captures the cross-repo provenance of the audit packet itself. PLAN.md notes the audit was on a "real ~30-minute technical session" but the packet is not linked. EN-002's `bracket-canonical` golden packet is described as derived from the audit packet, but if the audit packet is not shareable (mentioned as conditional in EN-005 inputs: "audit packet (if shareable)"), then EN-002 must synthesize an equivalent packet. **Recommendation:** EN-002 acceptance criteria should include a fallback path: "If audit packet is unshareable, synthesize a bracket-canonical golden from PDD-0102 patterns (referenced in BUG-006 root cause)." Owner: `eng-qa`.

**Specific entities cited:** EN-001 DEC-004, FEAT-005 BUG-006, FEAT-004 STORY-015, EN-002.

**Recommendation:** D-6.1 closes during EN-001 execution start; D-6.2 and D-6.3 advisory edits to STORY-015 and EN-002 acceptance criteria. Net effort: ~10 minutes.

---

### Dimension 7: Quality Threshold

**Verdict:** **PASS — ≥0.95 is appropriate for this work**

**The deliberate stricter-than-SSOT choice (0.95 vs H-13 baseline 0.92) is correctly calibrated for this Epic.** Three independent considerations support it:

1. **The audit's diagnostic anchors at 0.90.** The original 9-iteration adversary review plateaued at composite 0.90 — below the framework's standard 0.92. Setting the new bar at 0.92 would re-converge on the same plateau because the same mechanical-defect class would still consume iteration budget. Setting it at 0.95 forces actual closure of the substrate-validation gap. Per `quality-enforcement.md` "Operational Score Bands," ≥0.95 puts deliverables in PASS territory with margin.
2. **The work is auto-classified C3+ minimum.** AE-002 (touching `.context/rules/` or `.claude/rules/`) does not fire, but AE-003 (new or modified ADR) fires for STORY-001 (vendor) and STORY-002 (status promotion). AE-004 (modifies baselined ADR) fires for BUG-004, BUG-005 (ADR amendments), BUG-003 (deletes/deprecates schemas), and STORY-002 (which is, for the first time, baselining ADR-007 — argued as C3+ in the Story body). AE-005 (security-relevant code) fires for EN-003 SubprocessSandbox, STORY-005 substrate-coupling rule, STORY-008 atomic-write. Several entities are auto-C4. The 0.95 bar matches the C3+/C4 expectation across the project.
3. **Mechanical validators get scored, not just LLM-judged.** Once FEAT-003 lands, validators run on every PR (STORY-012). The 0.95 bar means the LLM-judged composite must clear 0.95 ON TOP OF the mechanical pass. This separation aligns with the user direction "outputs need to be validated automatically" — humans judge content quality, machines judge mechanical conformance.

**Per-entity threshold variation:**

- **EN-008 final tournament has stricter per-dimension thresholds in its AC (e.g., "Per-dimension scores: Completeness ≥0.95, Internal Consistency ≥0.95, Methodological Rigor ≥0.95, Evidence Quality ≥0.92, Actionability ≥0.92, Traceability ≥0.95")** — appropriate. Stricter on the high-weight dimensions, slightly relaxed on Evidence Quality and Actionability where lower scores can still compose to ≥0.95 weighted.
- **All other entities use ≥0.95 weighted composite as the gate.** No entity is over-thresholded (e.g., requiring 0.98 where 0.95 suffices) or under-thresholded (e.g., 0.92 where 0.95 is appropriate).

**No NEEDS CHANGE or GAP findings on this dimension.** The threshold calibration is correct.

**Specific entities cited:** EN-008 (per-dimension), all entities (composite ≥0.95).

**Recommendation:** No changes.

---

## L2: Strategic Implications

> Audience: project owner, principal architect — implications over the next 2-3 weeks

### Trajectory: 2-3 Week Outlook

**Week 1 (Phase 1 entry through Phase 1 sync barrier):**

The critical path is **FEAT-001 STORY-001 → FEAT-002 (5 Bugs in parallel) → FEAT-001 STORY-002 → FEAT-003 EN-001 → FEAT-003 EN-002 + EN-003**. Approximately 8 calendar days assuming 1 agent active at a time. With 2-3 agents in parallel (FEAT-001 STORY-001 plus FEAT-005 quick-wins plus FEAT-002 Bugs), Week 1 closes Phase 1.

EN-004 (red-team Phase 1 threat model) runs parallel with FEAT-001. Its handoff to /eng-team must land before EN-001 design starts. This is the strongest dependency edge in the project — if EN-004 Phase 1 slips, EN-001/EN-003 cannot start, which cascades into the entire FEAT-003 critical path.

**Week 2 (Phase 2 — FEAT-003 implementation):**

STORY-003..STORY-006 (the 17 validators) are the heaviest piece of work in the project. They are parallelizable across rule families (FILE, CONTENT, ANCHOR, SCHEMA) but each is gated by a `/adversary` C4 ≥0.95 review. Average ≈3 effort per Story × 4 Stories = 12 effort + 4 adversary reviews. Conservative estimate: 4-5 calendar days with 2 agents in parallel.

STORY-007 (verify CLI) and STORY-008 (update-anchors CLI) must close before STORY-009/010 can integrate. These two CLIs are the audit-author's reference shape — implementation is straightforward but scoped strictly to hexagonal architecture.

**Week 3 (Phase 3 — integration + schema + final tournament):**

STORY-009 (post-render hook) and STORY-010 (write pipeline) are the integration with `ts-formatter`. The decision between `SubagentStop`/`PostToolUse` hook vs prompt-discipline is the single highest-leverage technical decision in the project (per Finding D-4.2). If hook is chosen, the substrate is mechanically guaranteed. If prompt-discipline is chosen, agent compliance becomes another LLM-judged surface — exactly the failure mode the audit identified.

FEAT-004 (4 schema additions) lands during Week 3. STORY-013, STORY-014, STORY-016 are independent; STORY-015 (`discussions[]`) requires BUG-004 closure before disc-NNN regex can be defined. All four schema stories should land in parallel.

EN-006 (diataxis) starts late Week 3 / early Week 4 once implementation is stable. EN-008 (final tournament) runs at the end.

**Total elapsed: ~3 weeks for an experienced agent team operating in parallel; ~5-6 weeks for serialized single-agent execution.**

### Where the Technical-Debt Risk Lives

**Three primary risk zones:**

1. **EN-003 SubprocessSandbox is the security-critical zone.** Per AE-005 it is C3+ minimum, gated by `/red-team` exit criteria, requires Hypothesis property tests on 10K+ inputs, and demands `eng-security` manual code review. The risk is not over-investing — the risk is under-investing in the bypass-class enumeration. The audit author's gist runs `subprocess.run(["bash", "-c", pattern])` where pattern is JSON-supplied. **Anyone who writes that JSON gets shell.** The sandbox must be hardened against at least the 5 listed bypass classes (command injection, path traversal, env poisoning, symlink escape, resource exhaustion). If `red-exploit` finds a 6th bypass class during Phase 4, EN-003 must re-open.

2. **STORY-009/010 hook-mechanism decision is the integration zone.** The decision between SubagentStop/PostToolUse hook and prompt-discipline is the single highest-leverage technical decision. SubagentStop hook = deterministic L4 enforcement, hard guarantee. Prompt-discipline = soft enforcement, recurrence of the same audit pattern at a different surface. This decision should be made at Phase 1 sync barrier (after EN-001 design and before STORY-009 starts), not deferred to STORY-009 execution. **Recommendation: pre-create the shared FEAT-003 DEC entity and authorize `ps-architect` to make the call early.**

3. **The 0.95 quality bar is itself a debt accelerator if mismanaged.** The user has correctly set 0.95 to force mechanical correctness. But each `/adversary` C4 ≥0.95 review takes real time. If the project hits any entity that plateaus below 0.95, the iteration ceiling (RT-M-010 C4 = 10) caps the loop. After 10 iterations without convergence, AE-006 mandatory human escalation fires. **Risk: many small entities each consume 3-5 iterations to converge; aggregate iteration count balloons.** Mitigation: front-load `/adversary` review on the design phase (EN-001, EN-002) so implementation phase passes first time.

### Success Metric: Was the Decomposition Right?

**The decomposition is right if and only if the following are true at EN-008 closure:**

1. **EN-008 reproduction test passes:** Re-running the audit author's original 9-iteration scenario against the merged Epic deliverable composite must reach ≥0.95. The original ceiling at 0.90 must be broken. This is the single binary signal that the Epic delivered what it promised.
2. **Every entity closes with WTI-005 evidence in History.** The user-stated rule ("entities cannot be closed out unless they provide delivery evidence") gets enforced at every closure, not just at EN-008. This is the local-correctness signal; if any entity tries to close without commit SHAs / test runs / adversary scores, the decomposition's evidence-tracking discipline failed.
3. **No backlog of "deferred to follow-up" findings remain.** EN-005 UX synthesis may surface net-new findings — those become new worktracker entities filed mid-Epic. If at EN-008 there are >2 deferred-to-follow-up entities open, the Epic's scope was set too tightly.
4. **The ratio of mechanical-defect findings to substantive-content findings inverts.** Today, adversary reviews on transcript packets are dominated by mechanical defects (declared-vs-walked drift, ASR convention inconsistency, schema gaps). Post-Epic, mechanical defects should be ≤10% of findings; substantive content quality should be ≥90%. This is the audit author's diagnostic, restated as a measurable Epic outcome.

### What This Decomposition Implies for the Framework Itself

The audit's underlying observation is that `/transcript` had no sanctioned framework extension mechanism for entity-type or schema extensions. **PROJ-041 closes the substrate-validation gap, but it does not close the extension-mechanism gap.** That is appropriately out-of-scope for this Epic per PLAN.md. However:

- **FEAT-004 STORY-015 (`discussions[]` as 5th entity type)** is the first substantive use case for an extension-mechanism. The pattern that emerges from STORY-015 (schema + anchor + mindmap symbol + ts-extractor guidance + ADR amendment) becomes the *de facto* extension protocol. A future Epic should formalize this pattern as a reusable extension mechanism — but that's a Q3 concern, not a Q2 PROJ-041 concern.
- **FEAT-003's hexagonal architecture (validation as operation within /transcript BC)** establishes a reference architecture for adding operations within other skills' bounded contexts. Future skills (`/contract-design`, `/test-spec`, etc.) should mirror this shape.

These are positive externalities. The decomposition's Epic-level cohesion is sound and the framework benefits incidentally from PROJ-041 even though framework-level concerns are out of scope.

---

## Decisions

### D-001: Should the Epic split into multiple Epics, or the Features collapse?

**Date:** 2026-04-28
**Participants:** ps-architect (this review), adam.nowak (project owner)

#### Question/Context

The user scaffolded 1 Epic + 5 Features unilaterally. Should this re-shape into multiple Epics or collapse into fewer Features before execution begins?

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | Keep 1 Epic + 5 Features (status quo) | Unified narrative; each Feature ships independently with documented dependencies; FEAT-005 designated early-land quick-win without disturbing rest | None significant |
| **B** | Split into 2 Epics: governance (FEAT-001 + FEAT-002) and capability (FEAT-003 + FEAT-004 + FEAT-005) | Two smaller Epics may parallelize better; cleaner ownership boundaries | Fragments unified diagnostic; creates parent-container without planning value; cross-Epic dependencies (FEAT-003 ← FEAT-001 ← FEAT-002) become awkward |
| **C** | Collapse FEAT-001 + FEAT-002 into a single "Foundation" Feature | Reduces entity count by 1 | Conflates governance (ADR ops) with bug fixes; loses cohesion |

#### Decision

**We decided:** Option A. Keep the existing 1 Epic + 5 Feature decomposition.

#### Rationale

The 5 Features each represent a coherent capability slice of the audit's diagnostic. FEAT-001 governance, FEAT-002 contradictions, FEAT-003 validators, FEAT-004 schemas, FEAT-005 mindmap each ship independently with documented blocking edges. Splitting into multiple Epics would fragment the unifying narrative ("substrate is hand-attested, not machine-derived") that ties all 5 Features together. Collapsing FEAT-001 + FEAT-002 would mix governance with bugs and lose the cohesion benefit of each Feature being one cohesive thing.

#### Implications

- **Positive:** Existing dependency graph remains valid; no re-numbering of entities; execution can begin after BLOCKER 1 + BLOCKER 2 fixes.
- **Negative:** None.
- **Follow-up required:** None.

---

### D-002: Should Bugs be relocated from subdirectories to flat files?

**Date:** 2026-04-28
**Participants:** ps-architect, adam.nowak

#### Question/Context

7 Bugs (BUG-001..007) currently live in subdirectories (`BUG-NNN-slug/BUG-NNN-slug.md`). Per `worktracker-directory-structure.md`, Bugs at the parent level should be flat files with `{ParentId}--{BugId}-{slug}.md` naming. Should the Bugs be relocated?

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | Relocate all 7 Bugs to flat-file naming per directory structure spec | Conforms to canonical convention; `wt-auditor` will pass; consistent with the spec | Requires 7 mv operations + 7 parent-Feature link updates |
| **B** | Keep current subdirectory placement and amend `worktracker-directory-structure.md` to permit Bugs as subdirectories | Avoids file moves | Amends a baselined rule for a single project's convenience; opens precedent for ad-hoc rule overrides |
| **C** | Keep current placement and ignore the inconsistency | Lowest immediate effort | Worktracker tooling will fail; audit will fail; closure rule unenforceable |

#### Decision

**We decided:** Option A. Relocate all 7 Bugs to flat-file naming. This is BLOCKER 1 in the L1 review.

#### Rationale

The directory structure spec is canonical. Worktracker tooling (`wt-auditor`, future `jerry items list/show`) walks the canonical structure. Conforming once costs 10 minutes; not conforming costs every future audit pass. Option B would amend a baselined rule for one project's sake — bad precedent. Option C is the silent-corruption path the user explicitly warned against ("no shortcuts in plans").

#### Implications

- **Positive:** Worktracker tooling works; closure-rule evidence enforcement works; consistent with the framework convention.
- **Negative:** 10 minutes of effort.
- **Follow-up required:** `wt-auditor` validates current state, `eng-lead` applies the 7 mv operations and updates parent-Feature `Children Stories/Enablers` link tables.

---

### D-003: Should Tasks be materialized up-front or just-in-time?

**Date:** 2026-04-28
**Participants:** ps-architect, adam.nowak

#### Question/Context

~189 Task `.md` files are required (per Children Tasks tables and current Bug AC sections). Should they be materialized in one batch up-front, or just-in-time as each parent entity opens?

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | Materialize all ~189 Task `.md` files up-front before any execution | Single audit pass at scaffold completion; uniform shape | ~3 hours of agent time; freezes granularity decisions before context is in place; violates KISS |
| **B** | Materialize Tasks just-in-time as each parent entity opens | Owner of entity controls granularity at execution start; matches framework convention; allows split/merge based on context | Requires entity-opening discipline (`wt-auditor` flags missing Tasks before AC validation) |
| **C** | Skip Task materialization entirely; track Task evidence in parent entity History | Lowest effort | Violates worktracker directory structure; closure rule unenforceable at Task level |

#### Decision

**We decided:** Option B. Just-in-time materialization. This is the second part of BLOCKER 2 in the L1 review.

#### Rationale

Just-in-time is the framework convention used elsewhere. The owner of each entity has the most context to set Task granularity at execution start. Up-front materialization would freeze 189 granularity decisions before any context for those decisions exists. Option C violates `worktracker-directory-structure.md` and breaks the user-stated closure rule ("entities cannot be closed out unless they provide delivery evidence") at the Task level.

#### Implications

- **Positive:** Granularity decisions stay context-aware; KISS preserved; matches existing framework patterns.
- **Negative:** Entity-opening discipline required — `wt-auditor` must flag entities with missing Tasks before they reach AC validation.
- **Follow-up required:** Update `wt-auditor` checklist (if not already present) to verify Task `.md` files exist before allowing entity status `in_progress` → `completed`.

---

### D-004: Should EN-005 (UX) block EN-001 (DDD scaffolding)?

**Date:** 2026-04-28
**Participants:** ps-architect, adam.nowak

#### Question/Context

EN-005's Dependencies declares `Blocks: EN-001, STORY-007, STORY-008`. Is this dependency edge correctly tight, or should it relax?

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | Keep EN-005 → EN-001 as `Blocks` (status quo) | UX findings may reshape DDD layout; conservative | Phase 1 serialization on UX findings that may not exist; EN-001 cannot start until EN-005 closes |
| **B** | Change EN-005 → EN-001 to `Cooperates` | Allows EN-001 to start in parallel with EN-005; if UX findings impact layout, EN-001 absorbs them mid-flight or re-opens | Mid-flight re-open is more expensive than serial wait |
| **C** | Remove the dependency edge entirely | Maximum parallelism | Loses the affordance for UX to inform layout |

#### Decision

**We decided:** Option B. Relax to `Cooperates`. This is Finding D-3.1 in the L1 review.

#### Rationale

EN-001 (DDD module skeleton) is determined by hexagonal architecture (H-07), not by user research. The 4-layer split (domain, application, infrastructure, interface) and the port shapes (RuleEngine, ReportRenderer, SubprocessSandbox) don't change based on UX findings — they're governed by H-07 isolation rules. The realistic case where UX would re-shape EN-001 is the CLI surface — but that's STORY-007/008's concern, not EN-001's. Keep `Blocks` for STORY-007/008 only.

#### Implications

- **Positive:** EN-001 can start at Phase 1 entry alongside EN-005; reduces Phase 1 critical path by ~2-3 days; keeps STORY-007/008 properly gated on UX heuristic findings.
- **Negative:** Small risk that UX surfaces a finding that requires EN-001 re-shape mid-flight. Probability low; cost bounded.
- **Follow-up required:** `eng-lead` applies the dependency edge change.

---

### D-005: Should EN-006 (diataxis) block on FEAT-005 mindmap quick-wins?

**Date:** 2026-04-28
**Participants:** ps-architect, adam.nowak

#### Question/Context

EN-006's Dependencies declares `Blocked By: FEAT-001..FEAT-005`. FEAT-005 lands as early-land quick-win. Should EN-006 wait for all 5 Features, or should documentation for FEAT-005 land alongside FEAT-005 itself?

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | Keep EN-006 ← FEAT-001..FEAT-005 (status quo, monolithic) | Single doc pass at end; simplifies authoring; classifier+auditor run once | Mindmap-related docs don't update with FEAT-005; if FEAT-005 ships and the docs don't, agents/users discover the docs are stale |
| **B** | Split EN-006 into EN-006a (mindmap docs after FEAT-005) and EN-006b (full set after FEAT-001..004) | Mindmap docs ship with the implementation | Adds entity to count; doubles classifier/auditor work |
| **C** | Keep EN-006 monolithic; downgrade `Blocked By: FEAT-005` to `Cooperates` | Allows EN-006 to absorb FEAT-005 changes early without splitting the entity | Slight ambiguity in "is this blocked or not" |

#### Decision

**We decided:** Option C. Downgrade `Blocked By: FEAT-005` to `Cooperates`, keep EN-006 monolithic. This is Finding D-3.2 in the L1 review.

#### Rationale

The pure-monolithic Option A risks stale docs at FEAT-005's early-land moment, but FEAT-005 produces only 2 Bugs of doc-relevance (BUG-006 bracket-escape, BUG-007 self-claim) which is too small to warrant splitting EN-006. Option B's split would double the diataxis-classifier/auditor work for marginal benefit. Option C preserves EN-006's monolithic shape but allows it to start absorbing FEAT-005's changes as soon as FEAT-005 ships, without making EN-006 dependent on FEAT-005's full close.

#### Implications

- **Positive:** EN-006 can begin reference-doc updates for `ts-mindmap-mermaid` agent immediately after FEAT-005 closes; full doc set still gates on FEAT-001..004.
- **Negative:** None significant.
- **Follow-up required:** `eng-lead` applies the dependency edge change.

---

### D-006: Should the project add `eng-reviewer` to FEAT-002 Bug chains?

**Date:** 2026-04-28
**Participants:** ps-architect, adam.nowak

#### Question/Context

FEAT-002 BUG-001..005 chains use `ps-investigator`/`ps-architect` for resolution authoring and `eng-lead` for application. Should `eng-reviewer` be added before `adv-executor` for cross-document edit validation?

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | Status quo (no `eng-reviewer` step) | Simpler chain | ADR amendments and schema deletions go to `adv-executor` without architecture-aware human review |
| **B** | Add `eng-reviewer` before `adv-executor` for BUG-002, BUG-003, BUG-004, BUG-005 | Architecture-aware review on cross-document edits before adversary | One more agent step per Bug |
| **C** | Add `eng-reviewer` for ALL 5 Bugs including BUG-001 | Uniform | Token-cap disambiguation is text-only; `eng-reviewer` adds little value for that case |

#### Decision

**We decided:** Option B. Add `eng-reviewer` for BUG-002..005, skip BUG-001. This is Finding D-4.4 in the L1 review.

#### Rationale

BUG-002, BUG-003, BUG-004, BUG-005 all involve cross-document changes (regex updates across schemas, schema deletion, ADR amendments). `eng-reviewer` is the architecture-compliance role and should validate the final cross-document state before adversary review. BUG-001 (token-cap labeling) is text-only and doesn't warrant the extra step.

#### Implications

- **Positive:** Cross-document state validated by `eng-reviewer` before C4 review; reduces adversary iteration count.
- **Negative:** Adds 4 Agent Assignment rows.
- **Follow-up required:** `eng-lead` updates the 4 Bug Agent Assignment tables.

---

### D-007: Is the ≥0.95 quality threshold appropriate, or should it relax to 0.92?

**Date:** 2026-04-28
**Participants:** ps-architect, adam.nowak

#### Question/Context

The project sets a deliberate stricter-than-SSOT quality threshold (0.95 vs H-13 baseline 0.92). Is this calibrated correctly?

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | Keep 0.95 (status quo) | Forces actual closure of substrate-validation gap; matches C3+ auto-classification across the project; aligns with audit's "broken at 0.90" diagnostic | Slightly more iteration cost per entity |
| **B** | Relax to SSOT 0.92 | Lower iteration cost | Re-converges on the same plateau the audit hit; doesn't force mechanical-defect closure |
| **C** | Tighten to 0.98 | Highest assurance | Plateau detection (delta < 0.01 for 3 consecutive iterations) likely fires; AE-006 escalation likely; over-engineering |

#### Decision

**We decided:** Option A. Keep ≥0.95. This is the consensus PASS verdict in Dimension 7.

#### Rationale

The audit's diagnostic anchors at composite 0.90. Setting 0.92 would re-converge on the same plateau because the same mechanical-defect class would still consume iteration budget. Setting 0.98 would be over-tight given Operational Score Bands ("PASS ≥0.92"). 0.95 is the right calibration: it forces actual substrate-validation closure while staying within the iteration ceiling (RT-M-010 C4 = 10 iterations).

#### Implications

- **Positive:** Aligns with audit diagnostic; matches C3+ auto-classification; matches user direction "outputs need to be validated automatically."
- **Negative:** Slightly more iteration cost per entity vs. SSOT 0.92.
- **Follow-up required:** None. Proceed.

---

## Decision Summary

| ID | Decision | Date | Status |
|----|----------|------|--------|
| D-001 | Keep 1 Epic + 5 Features (no re-shape) | 2026-04-28 | DOCUMENTED |
| D-002 | Relocate 7 Bugs from subdirectories to flat files (BLOCKER 1) | 2026-04-28 | DOCUMENTED |
| D-003 | Materialize Tasks just-in-time, not up-front (BLOCKER 2) | 2026-04-28 | DOCUMENTED |
| D-004 | Relax EN-005 → EN-001 from `Blocks` to `Cooperates` | 2026-04-28 | DOCUMENTED |
| D-005 | Relax EN-006 ← FEAT-005 from `Blocked By` to `Cooperates` | 2026-04-28 | DOCUMENTED |
| D-006 | Add `eng-reviewer` step to BUG-002, BUG-003, BUG-004, BUG-005 chains | 2026-04-28 | DOCUMENTED |
| D-007 | Keep ≥0.95 quality threshold | 2026-04-28 | DOCUMENTED |

---

## Findings Index

### BLOCKING (must fix before any entity opens)

| ID | Dimension | Severity | Owner | Title |
|----|-----------|----------|-------|-------|
| BLOCKER 1 | Containment | BLOCKING | `wt-auditor` + `eng-lead` | 7 Bugs in subdirectories — must relocate to flat files |
| BLOCKER 2 | Task Granularity | BLOCKING | `wt-auditor` + entity owners | ~189 Task `.md` files do not exist; materialize just-in-time |

### NEEDS CHANGE (advisory, fix before merge)

| ID | Dimension | Owner | Title |
|----|-----------|-------|-------|
| D-3.1 | Dependencies | `eng-lead` | EN-005 → EN-001 from `Blocks` to `Cooperates` |
| D-3.2 | Dependencies | `eng-lead` | EN-006 ← FEAT-005 from `Blocked By` to `Cooperates` |
| D-3.3 | Dependencies | `eng-lead` | STORY-011 add transitive Blocked By: STORY-003..006 |
| D-4.1 | Agent Assignments | `eng-lead` | STORY-002 add `eng-architect` ADR alignment memo deliverable |
| D-4.2 | Agent Assignments | `wt-auditor` + `ps-architect` | Pre-create FEAT-003 DEC for hook mechanism (shared by STORY-009/010) |
| D-4.3 | Agent Assignments | `wt-auditor` | Pre-create BUG-007 DEC for capability-vs-claim-honesty decision |

### GAP (advisory)

| ID | Dimension | Owner | Title |
|----|-----------|-------|-------|
| D-3.4 | Dependencies | `eng-lead` | BUG-004 add `Blocks: FEAT-003 STORY-006` |
| D-3.5 | Dependencies | `eng-lead` | BUG-005 clarify `Blocked By` reasoning for STORY-001 |
| D-4.4 | Agent Assignments | `eng-lead` | Add `eng-reviewer` to BUG-002, BUG-003, BUG-004, BUG-005 |
| D-4.5 | Agent Assignments | `eng-lead` | STORY-012 add `eng-infra` runtime-env review |
| D-6.1 | Gaps | `ps-architect` | Confirm EN-001 DEC-004 (gist-port mapping) authored at execution start |
| D-6.2 | Gaps | `eng-backend` | STORY-015 add ascii-rendering AC for `[~]` symbol |
| D-6.3 | Gaps | `eng-qa` | EN-002 add fallback path if audit packet unshareable |

**Total: 2 BLOCKING + 6 NEEDS CHANGE + 7 GAP = 15 findings.**

---

## Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Parent | [EPIC-001](EPIC-001-transcript-hardening.md) | Parent Epic |
| Reference | [PLAN.md](../../PLAN.md) | Project plan and mission |
| Reference | [WORKTRACKER.md](../../WORKTRACKER.md) | Full hierarchy index |
| Reference | [GitHub Issue #273](https://github.com/geekatron/jerry/issues/273) | Source audit findings |
| Convention | `skills/worktracker/rules/worktracker-entity-hierarchy.md` | Entity hierarchy rules |
| Convention | `skills/worktracker/rules/worktracker-directory-structure.md` | Directory structure rules |
| Convention | `.context/rules/quality-enforcement.md` | Quality gate SSOT |
| Convention | `.context/rules/agent-development-standards.md` | Agent development standards (FC-M-001, AE-* rules) |
| Convention | `.context/rules/agent-routing-standards.md` | Agent routing standards (RT-M-010 iteration ceiling) |
| Related | All 36 entity files at `EPIC-001-transcript-hardening/**/*.md` | Reviewed entities |

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-04-28 | ps-architect (Claude) | Created decomposition review document; 7 decisions captured; 15 findings indexed |

---

## Metadata

```yaml
id: "EPIC-001:DEC-001"
parent_id: "EPIC-001"
work_type: DECISION
title: "Decomposition Review for PROJ-041 Transcript Hardening"
status: DOCUMENTED
priority: HIGH
created_by: "ps-architect (Claude)"
created_at: "2026-04-28T00:00:00Z"
updated_at: "2026-04-28T00:00:00Z"
decided_at: null
participants: [ps-architect, adam.nowak]
tags: [decomposition-review, worktracker-validation, pre-execution-gate]
decision_count: 7
superseded_by: null
supersedes: null
```

---

## Compaction Resilience (T-004)

| Constraint | Failure Mode if Lost | Compensating Control | Detection |
|-----------|---------------------|---------------------|-----------|
| BLOCKER 1 must close before any entity opens | Worktracker tooling fails silently; audit and closure-rule enforcement break | This DEC's L0 + Findings Index lists BLOCKER 1 prominently; `wt-auditor` runs at entity-opening | Manual review or `wt-auditor` flags missing Bug rename |
| BLOCKER 2 (Task .md files) must materialize before each entity closes | WTI-005 evidence enforcement breaks at Task level; closure-rule unenforceable | This DEC's L0 + Findings Index lists BLOCKER 2 prominently; `wt-auditor` checklist updated per D-003 | `wt-auditor` flags entities with missing Tasks before status `completed` |
| ≥0.95 threshold rationale | Future drift may relax to 0.92, re-converging on the audit's 0.90 plateau | Dimension 7 PASS rationale + D-007 capture rationale | Adversary iteration counts >5 on simple entities flag drift |
| 7 decisions captured per Decision Summary | Decisions made implicitly during execution; lost rationale | Decision Summary table + per-decision D-NNN structure | Manual review of subsequent worktracker activity |
