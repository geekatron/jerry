# FMEA Report: ADR-PROJ031-004 (ADR Identifier Convention) + adr-standards-rule-draft.md

**Strategy:** S-012 FMEA (Failure Mode and Effects Analysis)
**Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` + `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md`
**Criticality:** C4 (engagement quality gate 0.95, user-raised above SSOT 0.92)
**Date:** 2026-07-02
**Reviewer:** adv-executor (S-012 FMEA), blind independent tournament reviewer, iteration 3
**H-16 Compliance:** S-003 Steelman applied within the deliverable's own Options-Considered section (each of six schemes is steelmanned per H-16 discipline before critique); this blind FMEA pass operates on the iteration-2-remediated text.
**Elements Analyzed:** 8 (convention lifecycle stages, per invoking task mandate) | **Failure Modes Identified:** 9 | **Total RPN:** 1929

**Blind-protocol note:** This is an independent execution. Per the tournament's blind protocol, this reviewer has not read any prior-iteration or sibling-strategy adversary output in `orchestration/adr-convention-20260702-001/adversary/`. All findings below are original to this pass; overlap with prior iterations' FM-/PM-/SM-/CC-/RT-/DA-/IN- tags (visible only because the deliverable itself embeds a glossary of those tags inline) was checked against the deliverable's own Changelog (v1.0/v1.1/v1.2 entries) to avoid re-flagging already-closed items. New finding IDs use the `FM-1NN-{execution_id}` numbering band to avoid collision with the deliverable's embedded prior-review tags.

---

## Navigation

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment |
| [Element Inventory](#element-inventory) | 8 lifecycle-stage decomposition |
| [Findings Table](#findings-table) | All 9 failure modes, RPN-ranked |
| [Finding Details](#finding-details) | Full evidence for Critical + Major findings |
| [Recommendations](#recommendations) | Prioritized corrective actions |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 dimensions |
| [Execution Statistics](#execution-statistics) | Counts |

---

## Summary

Systematic decomposition of the ADR-identifier convention's 8-stage lifecycle (creation, cross-referencing, amendment, superseding, promotion, lint enforcement, template drift, new-project onboarding) surfaces 9 failure modes not addressed by the two prior remediation rounds: 4 Critical (RPN 240–441), 4 Major (RPN 126–180), 1 Minor (RPN 48). The highest-RPN finding is a self-compliance defect — the ADR that mandates a YAML-frontmatter provenance/scope schema for "every new ADR" does not itself carry that frontmatter. The second-highest is a structural completeness gap: the entire convention is written exclusively for Jerry's **project-based** worktracker topology and has zero provision for the **repository-based** topology that the worktracker SSOT documents as an equally valid `ONE-OF` choice — a gap directly relevant to this project's own downstream/plugin-adopter audience. Recommendation: **REVISE** (targeted corrections to 4 Critical items before ratification `PROPOSED -> ACCEPTED`; none of the 9 findings invalidate the core Scheme-B decision itself).

---

## Element Inventory

| ID | Lifecycle Stage | Scope Analyzed |
|----|------------------|-----------------|
| E-1 | Creation | Authoring a new ADR: ID assignment, domain-slug selection, frontmatter population |
| E-2 | Cross-referencing | Citations to ADR IDs from prose, paths, config, and sibling analysis docs (trade study) |
| E-3 | Amendment | In-body `AMENDED` blocks; boundary vs. Promotion/Supersede |
| E-4 | Superseding | Status transitions, bidirectional back-links, terminal states |
| E-5 | Promotion | Path 0/1/2; scope elevation; interaction with governance auto-escalation |
| E-6 | Lint enforcement | L-1 through L-10 CI checks; what is/isn't machine-verified |
| E-7 | Template drift | Fix 1/2/3 migration specs vs. the live state of their target files over time |
| E-8 | New-project onboarding | Scaffold documentation, `decisions/` seeding, topology coverage |

---

## Findings Table

| ID | Element | Failure Mode | S | O | D | RPN | Severity | Corrective Action | Affected Dimension |
|----|---------|-------------|---|---|---|-----|----------|-------------------|--------------------|
| FM-101-20260702-iter3 | E-1 Creation | ADR-PROJ031-004 lacks the YAML frontmatter (`id`/`scope`/`origin_project`/`created`) it mandates for "every new ADR" (ADR-M-002/ADR-M-013) | 7 | 9 | 7 | 441 | Critical | Add the real YAML block to this file now, not deferred to promotion | Internal Consistency |
| FM-102-20260702-iter3 | E-8 Onboarding | Convention has zero provision for the repository-based worktracker topology (documented `ONE-OF` alternative to project-based) | 7 | 6 | 8 | 336 | Critical | Add a repository-based Canonical Location Model row + onboarding note | Completeness |
| FM-103-20260702-iter3 | E-5 Promotion | Path 1's "zero-cost" claim doesn't reconcile with AE-004 (modifies baselined ADR -> Auto-C4), which may apply to every promotion's frontmatter scope-flip | 6 | 5 | 8 | 240 | Critical | Add explicit AE-004 scoping clause: metadata-only promotion moves are exempt from AE-004, or disclose the C4-tournament cost per promotion | Internal Consistency |
| FM-104-20260702-iter3 | E-6 Lint | L-6 checks provenance *presence* only; no lint verifies `origin_project` *correctness* against actual containing directory for canonical ADRs | 6 | 5 | 8 | 240 | Critical | Add an L-6b provenance-plausibility check, or downgrade the "lossless" consequence claim to "presence-verified, not accuracy-verified" | Evidence Quality |
| FM-105-20260702-iter3 | E-2 Cross-ref | M-7's claim that CLAUDE.md "already lists `.context/rules/*` rule files" (CLAUDE.md:53-56) overstates the actual pattern (3 of ~14 rule files individually listed) | 5 | 6 | 6 | 180 | Major | Correct the M-7 citation to state the minority-pattern precedent accurately; clarify whether the new rule file gets an individual row or relies on the generic row | Evidence Quality |
| FM-106-20260702-iter3 | E-3 Amendment | Promotion Path 2 doesn't address accumulated in-body `AMENDED` blocks on the dialect original; content risks being stranded behind a `SUPERSEDED` tombstone | 6 | 4 | 7 | 168 | Major | Add a Path-2 step: carry forward (or explicitly link to) prior amendment history in the new framework ADR | Actionability |
| FM-107-20260702-iter3 | E-4 Superseding | `DEPRECATED` has no forward-link/back-link mechanism analogous to `SUPERSEDED`'s L-7-enforced bidirectional link; a later replacing ADR has no schema field to point back | 5 | 5 | 6 | 150 | Major | Add an optional `deprecated_by`/`replaces_deprecated` frontmatter pair, WARN-checked | Traceability |
| FM-108-20260702-iter3 | E-1/E-2 Creation/Cross-ref | `TBR-2` (taxonomy arbiter) is cited twice in isolation; sibling `TBR-1/3/4/5` from `trade-study.md`'s Open Questions are never cross-referenced or confirmed resolved | 3 | 7 | 6 | 126 | Major | Add a short "Open Questions Resolved" mapping table (TBR-1..5 -> resolution) | Traceability |
| FM-109-20260702-iter3 | E-7 Template drift | Fix 1/2/3 migration specs cite exact "Current" text + line numbers but specify no precondition check that the cited text still matches at execution time | 3 | 4 | 4 | 48 | Minor | Add "verify Current text still present; if not, re-derive the edit location" to each Fix spec's preamble | Actionability |

**Finding ID Format:** `FM-{NNN}-{execution_id}` where `execution_id = 20260702-iter3` (this tournament iteration).

---

## Finding Details

### FM-101-20260702-iter3: Self-compliance gap — the convention-defining ADR does not carry the frontmatter it mandates

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Element** | E-1 Creation |
| **S/O/D** | 7 / 9 / 7 = RPN 441 |

**Evidence:** `ADR-PROJ031-004-adr-identifier-convention.md:1-12` — the file opens with `# ADR-PROJ031-004: ...` followed by a **blockquote** header (`> **PS:** ...`, `> **Exploration:** ...`, `> **Created:** ...`, `> **Status:** PROPOSED`, `> **Agent:** ...`, `> **Criticality:** ...`, `> **Supersedes:** (none)`, `> **Superseded By:** (none)`, `> **Canonical ID under the scheme this ADR decides:** ...`). There is **no YAML frontmatter block** anywhere in the file. Yet the companion rule draft's `adr-standards-rule-draft.md:44-58` (ADR-M-002, ADR-M-013) states: "ADR origin (birth project/entity) SHOULD be recorded in **frontmatter**..." and "Every new ADR SHOULD declare its intended `scope` (`framework`\|`project`) **in frontmatter at authoring time**." ADR-PROJ031-004 is itself a "new ADR" authored today (2026-07-02) under full awareness of this exact mandate — it is the single best-positioned document in the corpus to demonstrate the schema, and it does not.

The Meta-Note (`ADR-PROJ031-004-adr-identifier-convention.md:619-627`) discloses only the **ID-naming** self-compliance gap (dialect filename vs. canonical `ADR-adr-convention-001`) and explicitly labels its resolution as deferred inference ("This is inference about the intended end-state, not an action taken here"). It never discloses the **separate, broader** gap that the entire YAML frontmatter block (`id`, `scope`, `origin_project`, `created`, `supersedes`, `superseded_by`, `amends`, `amended_by`, `promoted_from`, `promoted_to`) is absent — a distinct failure from the ID-naming one, because it means lint rule L-6 (Provenance, WARN) and L-5 (Framework home, WARN) would fire against this exact file today, and none of the fields the Frontmatter Schema (`adr-standards-rule-draft.md:109-127`) prescribes are machine-readable in this document at all.

**Analysis (S-012 lens: Inconsistent):** The document performs extensive, explicit self-verification elsewhere (the entire P-022 disclosure apparatus, the Meta-Note's ID-remap path) — this is exactly the kind of gap that self-verification is supposed to catch, and it evaded two remediation rounds. Occurrence is rated 9 (not probabilistic — directly observed, already true). Detection is rated 7 because it requires connecting ADR-M-002/M-013 (in the *companion* rule draft) back to *this* document's own header — a cross-file check that the Meta-Note's narrower ID-naming-only self-audit did not perform.

**Recommendation:** Add a real YAML frontmatter block to `ADR-PROJ031-004-adr-identifier-convention.md` now (before ratification), populating `id: ADR-adr-convention-001` (per the declared canonical identity), `status: PROPOSED`, `scope: framework`, `origin_project: PROJ-031`, `created: 2026-07-02`, `supersedes: []`, `superseded_by: null`. This is a trivial, zero-risk edit (all field values are already stated in the existing blockquote header) and turns the flagship ADR into the schema's own first compliant instance rather than an admitted exception.

---

### FM-102-20260702-iter3: The convention has zero provision for the repository-based worktracker topology

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Element** | E-8 New-project onboarding |
| **S/O/D** | 7 / 6 / 8 = RPN 336 |

**Evidence:** `skills/worktracker/rules/worktracker-directory-structure.md:19-44` documents **two** alternative, equally valid `ONE-OF` placement patterns: "Project-based Folder Structure" (`projects/{ProjectId}/...`, used by "repositories like Jerry") and "**Repository-based Folder Structure**" (`{RepositoryRoot}/WORKTRACKER.md` + `{RepositoryRoot}/work/`, used by "repositories like Knowledge... The entire repository is the work context"). A repo-wide search of both deliverable files for `repository-based`, `RepositoryRoot`, and `repository-scoped` returns **zero matches** in either `ADR-PROJ031-004-adr-identifier-convention.md` or `adr-standards-rule-draft.md`. Every location table in both documents — the [Canonical Location Model](adr-standards-rule-draft.md#canonical-location-model), the ADR's own [L1 canonical location model](ADR-PROJ031-004-adr-identifier-convention.md#l1-technical-implementation), and the [New-Project Onboarding](adr-standards-rule-draft.md#new-project-onboarding-fm-016-p0-10) section — is written exclusively in terms of `projects/PROJ-NNN-*/decisions/` and `docs/design/`. None address where an ADR lives in a repository-based deployment (there is no `projects/` directory to hold a `decisions/` folder at all in that topology).

**Analysis (S-012 lens: Missing):** This gap is not cosmetic. PROJ-031 itself is the "cowork-skeleton" distribution project — its own [Enforcement Scope](ADR-PROJ031-004-adr-identifier-convention.md#enforcement-scope-and-deployment-targets-p0-2--pm-001) table explicitly names "Downstream project *using* the plugin" as a target audience whose ADRs get a CI-independent `uv run jerry lint adr` fallback. A downstream adopter who installs the Jerry plugin into a single-context, non-multi-project repository (the exact profile the worktracker SSOT describes for "repository-based" consumers) has **no home defined** for ADRs under this convention — not in the ID scheme (fine, that part is topology-agnostic), but in the Canonical Location Model, the lint's hardcoded path assumptions (`projects/*/decisions/`, `docs/design/` — both L-1a/L-1b/L-4/L-5 scoping clauses reference only these two paths), and the New-Project Onboarding checklist (which only tells authors to seed `projects/PROJ-NNN-*/decisions/`). Severity 7 because this silently fails the exact downstream audience the project exists to serve; Detection 8 because it requires cross-referencing a completely different rule file (`worktracker-directory-structure.md`) that neither deliverable cites anywhere near its location-model sections.

**Recommendation:** Add a third row to the Canonical Location Model: `Repository-based (no projects/ dir) | {RepositoryRoot}/decisions/ | ADR-{domain-slug}-NNN | Active`, and extend the L-1/L-4/L-5 lint path assumptions and the New-Project Onboarding section to branch on which of the two documented worktracker topologies is in effect.

---

### FM-103-20260702-iter3: Promotion Path 1's "zero-cost" claim is not reconciled against AE-004

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Element** | E-5 Promotion |
| **S/O/D** | 6 / 5 / 8 = RPN 240 |

**Evidence:** `.context/rules/quality-enforcement.md` Auto-Escalation Rules table: `AE-004 | Modifies baselined ADR | Auto-C4`. `ADR-PROJ031-004-adr-identifier-convention.md:8` explicitly invokes AE-002 and AE-003 to justify *this ADR's own* C3-floor classification ("AE-002 (touches `.context/rules/`) and AE-003 (new ADR) each independently set a C3 floor"). The document is therefore demonstrably fluent in, and willing to cite, the AE-00x auto-escalation rules for its own classification — but Promotion Path 1 (`ADR-PROJ031-004-adr-identifier-convention.md:482-488`, mirrored in `adr-standards-rule-draft.md:137-142`) — which literally instructs "**Update frontmatter:** `scope: project` -> `scope: framework`" against an already-`ACCEPTED` (baselined) ADR — never once discusses AE-004 or whether this frontmatter mutation counts as "modifies baselined ADR."

**Analysis (S-012 lens: Incorrect/Inconsistent — labeled as inference per P-022):** Whether AE-004 is intended to fire on a metadata-only field flip (scope/location) versus a substantive change to the decision's content is genuinely ambiguous in the SSOT — this finding does not claim AE-004 *definitely* fires, only that the deliverable never addresses the ambiguity despite it directly undermining its own central positive-consequence claim #1: "Promotion is a pure file move... a first-class, zero-cost primitive." If AE-004 does apply, every Path-1 promotion — the mechanism the whole ADR is built to make cheap and frequent — requires a mandatory Auto-C4 tournament (all 10 adversarial strategies) before it can complete, which is the opposite of "zero-cost." Severity 6 (undermines a headline consequence claim, not the core Scheme-B decision itself); Detection 8 (requires connecting two separate governance mechanisms — the AE-00x table and the Promotion Process — that the document itself never cross-links in this direction, despite demonstrated fluency in citing AE-002/AE-003 for its own classification one page earlier).

**Recommendation:** Add an explicit clause to the Promotion Process (Path 1, step 3): state whether AE-004 applies to promotion-only frontmatter changes (recommended: scope out AE-004 for `scope`/location-only mutations that do not alter the decision text, analogous to how the Amend-boundary section already scopes what counts as a mutation), or, if it is judged to apply, disclose the per-promotion C4-tournament cost as a Negative Consequence rather than omitting it.

---

### FM-104-20260702-iter3: No lint verifies provenance *correctness*, only *presence* — "lossless provenance" is an unverified claim

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Element** | E-6 Lint enforcement |
| **S/O/D** | 6 / 5 / 8 = RPN 240 |

**Evidence:** `adr-standards-rule-draft.md:205` (L5 CI Lint Specification table, row **L-6 Provenance**): "WARN | Every ADR should carry `origin_project` (or `origin_entity`) in frontmatter | Missing provenance | all ADRs." This is a *presence* check only. The equivalent dialect check, L-4 (`adr-standards-rule-draft.md:203`), *does* verify correctness for the dialect grammar ("`PROJ{NNN}` equals the containing `projects/PROJ-{NNN}-*/` dir"), but there is no analogous rule anywhere in the L-1 through L-10 table that verifies a **canonical** (domain-slug) ADR's `origin_project` value actually matches the project directory the file is sitting in. Meanwhile, `ADR-PROJ031-004-adr-identifier-convention.md:375` states as **Positive Consequence #3**: "Provenance preserved **losslessly** — origin lives in frontmatter... satisfying P-004/c-005 without polluting identity."

**Analysis (S-012 lens: Missing):** "Losslessly" is a strong, unqualified word — it implies the mechanism is verified end-to-end. In fact, nothing prevents an author from copy-pasting a frontmatter block from a different ADR/template and forgetting to update `origin_project`, and no lint rule (L-1 through L-10) would ever detect it: L-6 only confirms the field exists, not that its value is truthful. This is the same class of failure the whole convention exists to close (silent metadata drift with no detection) — recurring here, one layer down, for the very mechanism (frontmatter) that replaced the old, ID-encoded provenance. Severity 6 (undermines a headline "lossless" claim without invalidating the underlying decision); Occurrence 5 (plausible copy-paste-and-forget scenario, not certain); Detection 8 (nothing in the 10-rule lint table catches it).

**Recommendation:** Either add an `L-6b` correctness check (for canonical, project-scoped ADRs: `origin_project` frontmatter value must equal the containing `projects/PROJ-{NNN}-*/` directory, mirroring L-4's dialect logic) or soften "preserved losslessly" to "preserved by convention (presence-checked, not accuracy-checked, by L-6)" so the claim matches what is actually enforced.

---

## Recommendations

Ordered by RPN (highest first). Critical items are recommended as ratification-blocking; Major/Minor are recommended for the next revision pass but do not block ratification.

| Priority | ID | Corrective Action | Est. Post-Correction RPN |
|----------|----|--------------------|--------------------------|
| 1 | FM-101-20260702-iter3 | Add real YAML frontmatter to this ADR's own header (trivial; values already exist in the blockquote form) | ~40 (S2×O2×D2 residual documentation-hygiene risk) |
| 2 | FM-102-20260702-iter3 | Add repository-based Canonical Location Model row + lint/onboarding branch | ~60 |
| 3 | FM-103-20260702-iter3 | Add explicit AE-004 scoping clause to Promotion Path 1 | ~48 |
| 4 | FM-104-20260702-iter3 | Add L-6b correctness check, or soften the "lossless" consequence claim | ~50 |
| 5 | FM-105-20260702-iter3 | Correct the M-7 CLAUDE.md-precedent citation to reflect the actual 3-of-~14 pattern | ~40 |
| 6 | FM-106-20260702-iter3 | Add an amendment-carry-forward step to Promotion Path 2 | ~48 |
| 7 | FM-107-20260702-iter3 | Add optional `deprecated_by` WARN-checked field | ~40 |
| 8 | FM-108-20260702-iter3 | Add a TBR-1..5 "Open Questions Resolved" mapping table | ~30 |
| 9 | FM-109-20260702-iter3 | Add a "verify Current text still matches" precondition to Fix 1/2/3 | ~16 |

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | FM-102: an entire documented worktracker topology (repository-based) has zero coverage in the location model, lint scope, or onboarding guidance |
| Internal Consistency | 0.20 | Negative | FM-101: the document mandating a frontmatter schema doesn't itself carry it; FM-103: the "zero-cost promotion" thesis is not reconciled against the document's own demonstrated AE-00x fluency |
| Methodological Rigor | 0.20 | Negative | FM-101 and FM-103 both evaded the document's own extensive self-verification apparatus (P-022 disclosures, Meta-Note) despite two remediation rounds |
| Evidence Quality | 0.15 | Negative | FM-104: "preserved losslessly" is asserted without a corresponding enforcement mechanism; FM-105: the CLAUDE.md precedent citation (`:53-56`) overstates the actual pattern when checked against the full Navigation table |
| Actionability | 0.15 | Negative | FM-106: Path 2 promotion has no defined step for carrying forward prior amendment content; FM-109: Fix specs have no verification precondition |
| Traceability | 0.10 | Negative | FM-107: no forward-link field for DEPRECATED->replacement; FM-108: TBR-2 is cited without its sibling TBR-1/3/4/5 context |

---

## Execution Statistics

- **Total Findings:** 9
- **Critical:** 4
- **Major:** 4
- **Minor:** 1
- **Protocol Steps Completed:** 5 of 5 (Decompose; Enumerate; Rate S/O/D; Prioritize/Corrective Actions; Synthesize/Score)

---

*Report Version: 1.0*
*Strategy: S-012 FMEA*
*Template: `.context/templates/adversarial/s-012-fmea.md` v1.0.0*
*Execution ID: 20260702-iter3*
