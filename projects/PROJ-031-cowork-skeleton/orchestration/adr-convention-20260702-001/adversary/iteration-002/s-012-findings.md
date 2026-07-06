# FMEA Report: ADR Identifier, Location, and Promotion Convention (ADR-PROJ031-004 + adr-standards-rule-draft.md)

**Strategy:** S-012 FMEA (Failure Mode and Effects Analysis)
**Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` + `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md`
**Criticality:** C4 (engagement quality gate 0.95, elevated above the 0.92 SSOT gate per H-13)
**Date:** 2026-07-02
**Reviewer:** adv-executor (blind, independent, iteration 2)
**H-16 Compliance:** S-003 Steelman is applied inline within ADR-PROJ031-004 itself (each Option A-F leads with a steelman per H-16, `ADR-PROJ031-004.md:113-115`); this satisfies the C3+ sequence precondition for S-012.
**Elements Analyzed:** 8 | **Failure Modes Identified:** 17 | **Total RPN:** 4418

> **Note on scope:** This is a BLIND, INDEPENDENT iteration-2 review. Per protocol I have not read any prior adversary iteration output (including iteration-1 findings on this same deliverable) and do not know what was previously found or fixed beyond what the deliverable's own Changelog discloses. Findings below were derived by directly reading the two deliverable files in full and cross-checking specific claims against other repository files (research, rules, corpus) that I am permitted to read as evidence.

---

## Navigation

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment |
| [Element Inventory](#element-inventory) | The 8 lifecycle elements decomposed (Step 1) |
| [Findings Table](#findings-table) | All 17 failure modes with RPN (Step 2-3) |
| [Finding Details](#finding-details) | Expanded evidence for Critical/Major findings |
| [Prioritized Corrective Actions](#prioritized-corrective-actions) | Ranked by RPN (Step 4) |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 dimensions (Step 5) |
| [Overall Assessment](#overall-assessment) | Final recommendation |

---

## Summary

Systematic lifecycle-stage decomposition (creation, cross-referencing, amendment, superseding, promotion, lint enforcement, template drift, new-project onboarding) surfaces 17 failure modes, 11 of them Critical by RPN. Iteration-1 remediation (visible in the deliverable's own Changelog v1.0->v1.1) appears to have focused entirely on defects *internal* to the two files under review (lint grammar splits, override-model audit, citation-scan coverage). This iteration-2 FMEA deliberately decomposed the *lifecycle*, which required reading artifacts *outside* the two reviewed files — and found that the single most operationally significant gap is that **the actual ADR-producing agent (`ps-architect.md`) hardcodes a tenth, ungoverned naming grammar** (`{ps_id}-{entry_id}-adr-{slug}.md`, bare `# ADR-{NUMBER}` title) that neither deliverable's corpus survey, Fix specs (F1/F2), nor Migration Plan (M-1..M-11) mentions or touches (FM-001, RPN 648). A second, equally severe gap is that **the worktracker project-scaffolding SSOT contains no `decisions/` directory at all** (FM-016, RPN 504) — every one of the 14 verified project-level ADR files lives in a folder that is not part of the documented scaffold, and the convention proposes no fix to the scaffold or to project-creation tooling. Recommendation: **REVISE** — the two-file deliverable is internally well-argued and its own self-disclosed gaps (lint not yet built, M-6 flagged as ratification blocker) are honestly reported, but the convention cannot be considered complete or safely ratifiable until it also touches the producing agent and the project-scaffolding SSOT, neither of which is currently in scope.

---

## Element Inventory

| Element ID | Element | Description | Source |
|---|---|---|---|
| E1 | Creation | Authoring a new ADR: ID assignment, frontmatter, producing-agent behavior | ADR-PROJ031-004 L1 (ID grammar, frontmatter); rule draft ID Scheme |
| E2 | Cross-referencing | Citations to ADRs from other rule files, ADRs, and config | ADR-PROJ031-004 Context, References; rule draft L-8 |
| E3 | Amendment | In-body dated amendment mechanism for ACCEPTED ADRs | ADR-PROJ031-004 Amend vs Supersede; rule draft ADR-M-009 |
| E4 | Superseding | New-ID supersession, tombstone, back-links | ADR-PROJ031-004 Status Vocabulary; rule draft Supersede and Amend |
| E5 | Promotion | Path 0/1/2 project -> framework elevation | ADR-PROJ031-004 Promotion Process; rule draft Promotion Process |
| E6 | Lint enforcement | L-1 through L-8 deterministic CI checks + waiver ledger | ADR-PROJ031-004 Enforcement Design; rule draft L5 CI Lint Specification |
| E7 | Template drift | Exemplar template + skill files that emit/describe ADRs | rule draft Template and SKILL Fix Specifications (F1/F2) |
| E8 | New-project onboarding | How a brand-new project discovers/adopts the convention | Not a section in either deliverable file (verified absent) |

**MECE check:** These 8 elements were specified by the invoking task and correspond to the full ADR convention lifecycle from birth to eventual reuse-by-new-projects. Coverage gaps (E8 having no dedicated section) are themselves findings, not omissions from this inventory.

---

## Findings Table

| ID | Element | Failure Mode | S | O | D | RPN | Severity | Affected Dimension |
|----|---------|-------------|---|---|---|-----|----------|---------------------|
| FM-001-20260702-iter2 | E1 Creation | `ps-architect.md` hardcodes a 10th, ungoverned filename grammar + bare-number title, unaddressed by Fix specs/Migration Plan | 9 | 9 | 8 | 648 | Critical | Completeness |
| FM-002-20260702-iter2 | E1 Creation | The ADR itself doesn't use its own prescribed YAML frontmatter schema (self-non-compliance in the flagship exemplar) | 5 | 9 | 6 | 270 | Critical | Internal Consistency |
| FM-003-20260702-iter2 | E1 Creation | L-1a canonical regex permits lowercase domain-slugs that case-collide with uppercase dialect prefixes | 6 | 3 | 7 | 126 | Major | Methodological Rigor |
| FM-004-20260702-iter2 | E2 Cross-referencing | SSOT HARD-rule files cite un-promoted, un-flagged dialect ADRs as de facto framework governance | 7 | 8 | 8 | 448 | Critical | Traceability |
| FM-005-20260702-iter2 | E2 Cross-referencing | L-8 free-text citation regex has no false-positive exclusion for illustrative/example text | 4 | 7 | 6 | 168 | Major | Evidence Quality |
| FM-006-20260702-iter2 | E3 Amendment | Amend mechanism governs ACCEPTED-state only; no rule for PROPOSED-stage revision tracking (already happening in this review) | 5 | 8 | 7 | 280 | Critical | Methodological Rigor |
| FM-007-20260702-iter2 | E3 Amendment | No amendment-count/maturity threshold guidance | 3 | 5 | 5 | 75 | Minor | Actionability |
| FM-008-20260702-iter2 | E4 Superseding | No slug-continuity requirement across a supersession chain | 6 | 5 | 7 | 210 | Critical | Internal Consistency |
| FM-009-20260702-iter2 | E4 Superseding | `supersedes`/`superseded_by` frontmatter cardinality asymmetry (array vs. scalar) | 6 | 4 | 8 | 192 | Major | Internal Consistency |
| FM-010-20260702-iter2 | E5 Promotion | Promotion trigger is discretionary SHOULD judgment with no objective/lint-checkable signal | 7 | 8 | 8 | 448 | Critical | Completeness |
| FM-011-20260702-iter2 | E5 Promotion | Path 2 "live vs. historical" citation-repair boundary undefined for orchestration-state files | 5 | 7 | 6 | 210 | Critical | Actionability |
| FM-012-20260702-iter2 | E6 Lint enforcement | Zero enforcement artifacts exist yet; entire L-1..L-8 layer is prose-only | 8 | 10 | 5 | 400 | Critical | Actionability |
| FM-013-20260702-iter2 | E6 Lint enforcement | Waiver-ledger "not the author" check has no defined machine method for determining authorship | 4 | 6 | 6 | 144 | Major | Methodological Rigor |
| FM-014-20260702-iter2 | E7 Template drift | Confirmed-live pre-fix forms in `adr.md` template + `architecture/SKILL.md`; no interim bridge during the fix-pending window | 6 | 8 | 6 | 288 | Critical | Completeness |
| FM-015-20260702-iter2 | E7 Template drift | `ps-architect.md` points at phantom `templates/adr.md` and phantom `scripts/cli.py`, untouched by Fix specs | 5 | 9 | 7 | 315 | Critical | Completeness |
| FM-016-20260702-iter2 | E8 New-project onboarding | Worktracker SSOT scaffold has no `decisions/` directory; convention proposes no scaffold or tooling fix | 7 | 9 | 8 | 504 | Critical | Completeness |
| FM-017-20260702-iter2 | E8 New-project onboarding | No default guidance for the common "don't yet know if framework-wide" case at a brand-new project's first ADR | 4 | 7 | 5 | 140 | Major | Actionability |

**Aggregate:** Critical = 11, Major = 5, Minor = 1. Total RPN = 4418. Element with highest cumulative RPN: **E8 New-project onboarding** (644, across only 2 failure modes) and **E1 Creation** (1044, across 3 failure modes) — both above the 30%-of-modes-with-RPN>80 systemic-issue threshold (Step 3 Decision Point; 16 of 17 modes exceed RPN 80, i.e. 94%).

---

## Finding Details

### FM-001-20260702-iter2: Producing agent hardcodes a 10th, ungoverned ADR naming grammar

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical (RPN 648; S=9 also independently meets the S>=9 Critical trigger) |
| **Section** | Not in the reviewed deliverable — evidence is external, in the producing agent |
| **Strategy Step** | Step 2 (Enumerate) applied to the "Creation" element, which by definition includes the agent that performs creation |

**Evidence:** `skills/problem-solving/agents/ps-architect.md:218` prescribes the Nygard title line as `# ADR-{NUMBER}: {Title}` — a bare number, i.e. exactly the Scheme E "degenerate" form the parent ADR deprecates for new ADRs (`ADR-PROJ031-004.md:154,282-283,D-4`). More critically, `ps-architect.md:260,268,327,395,480,482,497,500,503,506` (10 occurrences) hardcode the MANDATORY (P-002) output filename as `projects/${JERRY_PROJECT}/decisions/{ps_id}-{entry_id}-adr-{slug}.md` — e.g. `work-024-e-202-adr-event-sourcing.md` (`ps-architect.md:81`) — a lowercase, PS-integration-ID-scoped grammar with `adr` as a mid-string infix, matching **none** of the canonical (`ADR-{domain-slug}-NNN`), dialect (`ADR-{PROJECT-ID}-NNN`), bare (`ADR-NNN`), or any of the other 8 families the corpus survey enumerates (`ADR-PROJ031-004.md:68-79`). This is a live, operative instruction: `ps-architect` is the very agent credited as "Generated by" at the foot of the ADR under review (`ADR-PROJ031-004.md:625`).

**Analysis:** Per the FMEA "Missing" and "Inconsistent" lenses: the deliverable's corpus survey claims 9 families and its Fix specs (F1: `docs/knowledge/exemplars/templates/adr.md`; F2: `skills/architecture/SKILL.md`) and Migration Plan (M-1 through M-11) touch only two files — neither of which is `ps-architect.md`. Because `ps-architect` is invoked via `/problem-solving` (a distinct, equally-eligible ADR-authoring path alongside `/architecture`), ratifying this convention without also updating `ps-architect.md` means the framework's other primary ADR-producing agent will continue to emit a 10th ungoverned naming family by default, indefinitely. This is the single highest-occurrence, highest-severity gap found: it is not a corpus cleanup problem (like the other 9 families) but an *ongoing production* problem that guarantees new non-compliant ADRs from this point forward.

**Recommendation:** Add a Fix 3 to the rule draft's "Template and SKILL Fix Specifications" section covering `skills/problem-solving/agents/ps-architect.md`: (a) replace the bare `# ADR-{NUMBER}` Nygard placeholder at line 218 with `# ADR-{DOMAIN-SLUG}-{NNN}`; (b) replace the `{ps_id}-{entry_id}-adr-{slug}.md` filename pattern (10 occurrences) with `ADR-{domain-slug}-NNN-{title-slug}.md` (or the permitted dialect); (c) add this file to the Migration Plan as a gating item alongside M-3/M-4, since it is at least as operationally significant.

---

### FM-016-20260702-iter2: Worktracker SSOT scaffold has no `decisions/` directory; new-project onboarding entirely unaddressed

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical (RPN 504) |
| **Section** | Not in the reviewed deliverable — evidence is that no such section exists |
| **Strategy Step** | Step 1 (Decompose), verifying MECE coverage against the task-specified "new-project onboarding" element |

**Evidence:** The canonical project-scaffolding tree documented at `skills/worktracker/rules/worktracker-directory-structure.md:27-65` (both the Project-based and Repository-based patterns, and the detailed `WORKTRACKER Directory Structure` tree) lists only `PLAN.md`, `WORKTRACKER.md`, and `work/` at the project root — no `decisions/` directory anywhere. `.context/rules/project-workflow.md` "Project Orientation" section corroborates: "Projects follow `projects/PROJ-{NNN}-{slug}/` with `PLAN.md`, `WORKTRACKER.md`, and `work/` decomposition." Yet a direct Glob of the live repository (`projects/PROJ-*/decisions/ADR-*.md`) confirms **14 project-level ADR files across 5 projects** (`PROJ-001-oss-release`x2, `PROJ-010-cyber-ops`x6, `PROJ-022-user-experience-skill`x2, `PROJ-030-bugs`x1, `PROJ-031-cowork-skeleton`x4 incl. the ADR under review) all live in a `decisions/` folder that is not part of the documented scaffold. Neither `ADR-PROJ031-004.md` nor `adr-standards-rule-draft.md` proposes adding `decisions/` to `worktracker-directory-structure.md`, and no Migration Plan item (M-1 through M-11) references it.

**Analysis:** "Missing" lens, at the highest level: the task explicitly named "new-project onboarding" as a lifecycle stage to decompose, and the deliverable has no corresponding section at all. A project created today strictly per the documented worktracker SSOT has no `decisions/` folder, no pointer that one is expected, and no step in `/worktracker` skill or `jerry projects` CLI tooling that creates or references it. The convention's own corpus-history is direct evidence of the failure mode this creates: PROJ-031 itself originally authored bare `ADR-001..003` mid-session and had to rename them to the dialect form (`ADR-PROJ031-004.md:82`, "the strongest internal signal that the team is already converging on project-ID scoping") — precisely because nothing in the onboarding path told the author which convention to use. Without a scaffold fix, every future project repeats this discovery-by-accident pattern indefinitely, which is the exact zoo-of-conventions problem this ADR exists to end.

**Recommendation:** Add an explicit "New Project Onboarding" section to `adr-standards-rule-draft.md` specifying: (a) a new MEDIUM standard directing `projects/PROJ-NNN-*/decisions/` be added to `worktracker-directory-structure.md`'s documented tree (with a one-line note pointing at `adr-standards.md`); (b) whether `/worktracker` project-creation tooling should scaffold an empty `decisions/.gitkeep` or README pointer; (c) add this as a gating Migration Plan item.

---

### FM-004-20260702-iter2 / FM-010-20260702-iter2: Un-promoted dialect ADRs already function as framework governance, undetectable by the lint spec

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical (RPN 448 each) |
| **Section** | ADR-PROJ031-004.md Promotion Process; adr-standards-rule-draft.md L-5 |
| **Strategy Step** | Step 2 (Enumerate) — Cross-referencing (effect) and Promotion (root cause) are two elements sharing one underlying gap |

**Evidence:** `.context/rules/quality-enforcement.md` Strategy Catalog and References sections cite `ADR-EPIC002-001` and `ADR-EPIC002-002` repeatedly as the authoritative source for strategy selection and the 5-layer enforcement architecture; `.context/rules/agent-development-standards.md` and `.context/rules/mcp-tool-standards.md` cite `ADR-STORY015-001` repeatedly as authoritative for the T1-T5 tool tier model. A direct Glob confirms all three files live at `projects/PROJ-001-oss-release/decisions/ADR-EPIC002-00{1,2}-*.md` and `projects/PROJ-024-tactical-work/work/.../STORY-015-.../ADR-STORY015-001-*.md` — i.e., project-scoped dialect ADRs, not `docs/design/`. `ADR-PROJ031-004.md:247-249` itself confirms two of these "remain local on disk... as internal governance," explicitly filesystem-verified by the ADR's own author.

**Analysis:** "Ambiguous"/"Insufficient" lens on both elements. Path 1 Step 1 of the Promotion Process ("Confirm the decision governs the framework broadly") is a discretionary SHOULD with no objective trigger — contrast the framework's own `AE-001` through `AE-005` auto-escalation rules elsewhere in `quality-enforcement.md`, which DO define objective, checkable triggers (e.g., "touches `.context/rules/`"). The convention could analogously define "an ADR cited from >= N distinct SSOT rule files SHOULD be flagged promotion-candidate," but does not. The direct consequence (Cross-referencing element) is that `L-5` ("Framework home" WARN) can only fire on an ADR whose OWN frontmatter already declares `scope: framework` — these three ADRs carry no such frontmatter field at all (confirmed: none of the corpus's HTML-comment/blockquote metadata blocks include a `scope:` key), so L-5 is structurally blind to exactly the case that matters most: governance-critical ADRs silently miscategorized as project-local.

**Recommendation:** Define an objective promotion-candidate signal (e.g., citation-count threshold from SSOT `.context/rules/*.md` files, checkable via the same `grep`-based mechanism L-8 already uses) and add it as a new WARN-class lint rule. Separately, flag `ADR-EPIC002-001/002` and `ADR-STORY015-001` for an explicit promotion-vs-stay-local decision as part of ratification, since their governance role is already established fact, not speculation.

---

### FM-012-20260702-iter2: Zero enforcement artifacts exist; entire lint layer is prose-only

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical (RPN 400) |
| **Section** | ADR-PROJ031-004.md Enforcement Design; adr-standards-rule-draft.md L5 CI Lint Specification |
| **Strategy Step** | Step 3 (Rate) |

**Evidence:** Direct Glob confirms none of `scripts/lint_adr_convention.py`, `scripts/adr-lint-waivers.yaml`, or `scripts/adr-grandfather-allowlist.txt` exist in the repository. This is disclosed by the deliverable itself (Risk R-5, Pre-Mortem FM-1, and Migration Plan M-6 explicitly marked "ratification blocker").

**Analysis:** Rated Detection=5 (moderate, not high) precisely because this gap IS prominently self-disclosed — a careful reader will see it. It remains Critical by RPN because Severity (8) and Occurrence (10, verified certain) are both high: until M-6 ships, every other control described in the convention (L-1 through L-8) is non-operative, meaning the convention's core differentiator versus "just a wiki page" — deterministic enforcement (c-002/c-006) — does not yet exist. This is not a hidden defect but is nonetheless the largest concrete residual risk in the package and belongs at the top of any pre-ratification checklist, not buried in a Migration Plan row.

**Recommendation:** Treat M-6 as a hard ratification precondition (the ADR already does this in prose); additionally, require the regression test described in the rule draft ("mandatory 16-file grandfather regression test green") to be attached as CI evidence (a link to a passing CI run), not merely described, before Status can move from PROPOSED to ACCEPTED.

---

### FM-015-20260702-iter2: Producing agent's own template/tooling pointers are already phantom paths

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical (RPN 315) |
| **Section** | Not in the reviewed deliverable — evidence is external, in the producing agent |
| **Strategy Step** | Step 2 (Enumerate), Template drift element |

**Evidence:** `ps-architect.md:263` instructs the agent to "Follow the template structure from: `templates/adr.md`" — verified absent via Glob (the real path is `docs/knowledge/exemplars/templates/adr.md`, the very file Fix 1 targets). `ps-architect.md:267` instructs `python3 scripts/cli.py link-artifact ...` — verified absent via Glob (`scripts/cli.py` does not exist; the current CLI per `CLAUDE.md` Quick Reference is `jerry`, invoked as `jerry <subcommand>`).

**Analysis:** "Incorrect" lens. This confirms FM-001/FM-014's compounding severity: the agent most likely to author new ADRs is not merely using an ungoverned filename grammar (FM-001) but is doing so while pointing at template and CLI paths that no longer exist at all, independent of this ADR. Neither Fix 1 nor Fix 2 in the rule draft touches `ps-architect.md`, so ratifying the convention leaves this compounding drift completely unaddressed.

**Recommendation:** Fold into the FM-001 corrective action (Fix 3): audit and correct all `ps-architect.md` path references as part of the same edit pass, since they share a root cause (the agent definition has not been updated since the CLI/template migration).

---

### FM-006-20260702-iter2: Amendment mechanism has no rule for PROPOSED-stage revision (happening right now)

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical (RPN 280) |
| **Section** | ADR-PROJ031-004.md Amend vs Supersede Conventions; adr-standards-rule-draft.md ADR-M-009 |
| **Strategy Step** | Step 2 (Enumerate) |

**Evidence:** `adr-standards-rule-draft.md:53` (ADR-M-009) and `ADR-PROJ031-004.md:475-487` both scope the in-body `**AMENDED YYYY-MM-DD:**` block mechanism to "Accepted ADRs." `ADR-PROJ031-004.md:616-622` shows the ADR's own revision history uses a version-numbered **Changelog table** (`1.0 -> 1.1`, dated 2026-07-02, describing "Owner-first remediation after adversarial iteration 1") for a document still in `PROPOSED` status — a third mechanism, distinct from both the AMENDED-block (ACCEPTED-only) and the New-Superseding-ADR (decision-reversal) paths.

**Analysis:** "Missing" lens. Neither document states whether the Changelog-table pattern is the sanctioned PROPOSED-stage revision mechanism, is expected to be replaced by AMENDED blocks once accepted, or is itself out-of-convention. Since this exact situation (an ADR under active, multi-iteration adversarial review) is the most probable near-term use case for any C3/C4 ADR under this convention, the gap will recur immediately and often.

**Recommendation:** Add an explicit row to the Amend-vs-Supersede table for "PROPOSED-stage revision during review" distinct from post-acceptance amendment, specifying the Changelog-table pattern (already in de facto use) as the sanctioned mechanism, and stating whether/how it reconciles with AMENDED blocks after acceptance.

---

### FM-014-20260702-iter2: Confirmed template/skill drift with no interim bridge

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical (RPN 288) |
| **Section** | adr-standards-rule-draft.md Template and SKILL Fix Specifications |
| **Strategy Step** | Step 2 (Enumerate) |

**Evidence:** Directly confirmed live: `skills/architecture/SKILL.md:105,284,288,437` still contain `docs/design/ADR_NNN_*.md` / `# ADR-001: Use SQLite for Persistence` forms; `docs/knowledge/exemplars/templates/adr.md:1,182` still contain `# ADR-{NUMBER}: {Title}` and the dangling `docs/decisions/...` path. The rule draft accurately specifies these as Fix 1/Fix 2 targets (`adr-standards-rule-draft.md:217-238`) but the fixes are "Not applied by this draft," tracked as Migration Plan M-3/M-4 with owner "governance" and no committed timeline.

**Analysis:** "Insufficient" lens, on the *transition*, not the target-state design (which is sound). Between ratification (M-1) and the actual application of M-3/M-4, any agent invoking `/architecture` is actively instructed by the still-live `SKILL.md` toward the deprecated `ADR_NNN` form, with no deprecation banner or interim pointer-comment added to bridge the gap in the interim.

**Recommendation:** As a zero-cost interim measure, add a one-line pointer comment to `skills/architecture/SKILL.md` and `docs/knowledge/exemplars/templates/adr.md` at ratification time (before the full F1/F2 rewrite lands) noting "ADR naming convention pending update, see `.context/rules/adr-standards.md`" so the gap is at least visible rather than silent.

---

## Prioritized Corrective Actions

| Rank | ID | RPN | Corrective Action | Est. Post-Correction RPN |
|------|----|----|--------------------|--------------------------|
| 1 | FM-001 | 648 | Add Fix 3 (this review): update `ps-architect.md` title/filename grammar to canonical/dialect form; add as gating Migration Plan item | ~60 |
| 2 | FM-016 | 504 | Add `decisions/` to `worktracker-directory-structure.md` scaffold + new-project-onboarding section in rule draft | ~50 |
| 3 | FM-004 / FM-010 | 448 / 448 | Define objective promotion-candidate signal (citation-count trigger); adjudicate EPIC002-001/002, STORY015-001 promotion status at ratification | ~90 each |
| 4 | FM-012 | 400 | Require CI-verified passing regression test as ratification evidence, not a prose description | ~60 |
| 5 | FM-015 | 315 | Fold `ps-architect.md` phantom-path correction into Fix 3 | ~40 |
| 6 | FM-014 | 288 | Add zero-cost interim deprecation-pointer comments to SKILL.md/adr.md pending full F1/F2 | ~80 |
| 7 | FM-006 | 280 | Add explicit PROPOSED-stage revision-tracking rule (sanction the Changelog-table pattern) | ~60 |
| 8 | FM-002 | 270 | Retrofit YAML frontmatter onto `ADR-PROJ031-004` itself as a self-compliance worked example | ~50 |
| 9 | FM-008 / FM-011 | 210 / 210 | Add slug-continuity guidance for supersession; define live-vs-historical boundary for orchestration-state files | ~70 each |
| 10 | FM-009 | 192 | Make `superseded_by` an array in the frontmatter schema for symmetry with `supersedes` | ~30 |
| 11 | FM-005 | 168 | Add a false-positive exclusion pattern (e.g., fenced-code-block exclusion) to L-8's citation regex | ~50 |
| 12 | FM-013 | 144 | Define authorship determination method (git-blame first-commit) for the waiver ledger | ~50 |
| 13 | FM-017 | 140 | Add a conservative default ("prefer domain slug unless clearly single-project-only") for first-time authors | ~40 |
| 14 | FM-003 | 126 | Add a reserved-word/case-collision exclusion to L-1a, or a cross-check between L-1a/L-1b | ~30 |
| 15 | FM-007 | 75 | Note an amendment-count soft-signal for supersession consideration (optional) | ~50 |

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | FM-001, FM-016: two entire lifecycle touchpoints (producing agent, project scaffold) are outside the deliverable's edit scope and unaddressed by Migration Plan/Fix specs |
| Internal Consistency | 0.20 | Negative | FM-002 (ADR doesn't self-comply with its own frontmatter schema), FM-008/FM-009 (supersession slug-continuity and cardinality asymmetry) |
| Methodological Rigor | 0.20 | Negative | FM-003 (untested case-collision), FM-006 (amendment mechanism gap for the exact stage this document is in), FM-013 (undefined authorship check) |
| Evidence Quality | 0.15 | Mixed | Every claim independently checked in this review (dangling `ADR-CI-001` citation, absent lint scripts, phantom `ps-architect.md` paths, absent `docs/design/` YAML frontmatter, worktracker scaffold gap) was found to be factually accurate as stated — evidence quality within the deliverable's own scope is strong; Negative only on FM-005 (untested regex false-positive risk) |
| Actionability | 0.15 | Negative | FM-012 (lint is prose-only, no CI evidence required for ratification), FM-011 (live-vs-historical boundary undefined for a cited example file) |
| Traceability | 0.10 | Negative | FM-004/FM-010: the two most-cited "framework governance" ADRs in the entire repo are invisible to every lint rule specified, because L-5 requires frontmatter that they lack |

---

## Overall Assessment

**REVISE.** The two-file deliverable is rigorously argued and internally self-aware within its own scope — cross-checking a sample of its factual claims (the dangling `ADR-CI-001` citation, the absence of YAML frontmatter on the 3 `docs/design/` ADRs, the 14-file live corpus count, the STORY-015 entity-embedded path) confirmed all of them accurate. However, a lifecycle-stage FMEA that deliberately looks *outside* the two reviewed files finds that the convention's practical viability depends on two artifacts neither deliverable touches: the ADR-producing agent (`ps-architect.md`, FM-001/FM-015) and the project-scaffolding SSOT (`worktracker-directory-structure.md`, FM-016). Both are Critical-RPN, both are cheap to fix (they are targeted edits, not new design work), and both should be added to the Migration Plan as gating items before this convention is presented for ratification. Additionally, two already-existing, heavily-cited project-scoped ADRs (`ADR-EPIC002-001/002`) sit invisibly outside the lint's detection capability (FM-004/FM-010) — a concrete, present-day instance of exactly the discoverability failure this convention exists to prevent, not a hypothetical future risk.

---

## Execution Statistics

- **Total Findings:** 17
- **Critical:** 11
- **Major:** 5
- **Minor:** 1
- **Protocol Steps Completed:** 5 of 5 (Decompose, Enumerate, Rate, Prioritize, Synthesize)
