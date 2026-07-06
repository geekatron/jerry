# FMEA Report: ADR Identifier, Location, and Promotion Convention (PROJ-031)

## Navigation

| Section | Purpose |
|---------|---------|
| [Header](#header) | Execution metadata |
| [Summary](#summary) | Overall assessment |
| [Element Inventory](#element-inventory) | MECE decomposition of the convention lifecycle |
| [Findings Table](#findings-table) | All FM-NNN findings with RPN |
| [Finding Details](#finding-details) | Expanded Critical/Major findings |
| [Recommendations](#recommendations) | Prioritized corrective actions |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 dimensions |
| [Execution Statistics](#execution-statistics) | Counts and totals |

---

## Header

**Strategy:** S-012 FMEA (Failure Mode and Effects Analysis)
**Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` (canonical `ADR-adr-convention-001`) + `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md`
**Criticality:** C4 (engagement quality gate 0.95)
**Date:** 2026-07-02
**Reviewer:** adv-executor (S-012, iteration 5, blind reviewer)
**H-16 Compliance:** S-003 Steelman is embedded in the deliverable itself (each of Options A-F leads with a steelman per H-16; see the deliverable's own reading-note glossary). This execution operates on the iteration-5, v1.6-remediated state of the deliverable.
**Elements Analyzed:** 15 | **Failure Modes Identified:** 7 (novel; not previously tagged RT-/FM-/CC-/IN-/DA-/SM-/PM-/CV- in the deliverable's own extensive prior-review annotation) | **Total RPN:** 1451

**Scope note (P-022):** The deliverable has already been through 4 full adversarial iterations plus an iteration-5 self-refine pass (Changelog v1.0-v1.6), and carries in-line tags for dozens of prior findings (RT-*, FM-*, CC-*, IN-*, DA-*, SM-*, PM-*, CV-*). This report does not re-litigate those; it was grep-verified against the deliverable text before each finding below was finalized, to confirm novelty. Each finding cites file + line evidence.

---

## Summary

Applying systematic bottom-up decomposition across 15 lifecycle elements (creation, cross-referencing, amendment, superseding, promotion Path 0/1/2, lint enforcement, template/skill/agent drift, new-project onboarding, ratification gating, DEC-NNN non-conflation, and self-compliance), 7 novel failure modes were identified, none previously tagged in the deliverable's own annotation system. Four classify Critical (RPN >= 200): a claimed-but-nonfunctional lint backstop for illegitimate amendments (FM-001), an incomplete producer-drift monitoring list that omits a file the package's own Fix 3 modifies (FM-002), an asymmetric AE-004 criticality scoping that classifies Path 1 promotions but is silent on Path 2 (FM-003), and an undetectable GitHub-Issue citation-staleness gap on rename/supersession (FM-006). Three classify Major: an incomplete degraded-mode disclosure for the downstream CLI (FM-004), an unspecified prerequisite artifact for the L-13 supersession-legitimacy rule (FM-005), and a stale risk-register entry that was not revisited after a later architectural change widened its exposure window (FM-007). **Recommendation: REVISE.** None of the findings invalidate the convention's core decision (subject-encoded identity); all are enforcement-mechanism and self-consistency gaps addressable by targeted edits, consistent with the honest, incrementally-improving posture the deliverable has demonstrated across its prior four iterations.

---

## Element Inventory

| ID | Element | Description |
|----|---------|-------------|
| E-01 | ID Grammar & Regex Definitions | L-1a canonical / L-1b dialect / deprecated-bare / frozen-legacy grammars |
| E-02 | Frontmatter Schema | YAML `---` block: id, scope, origin_project, supersedes, promoted_from/to, canonical_id |
| E-03 | Canonical Location Model | Framework/project/dialect/entity-embedded/frozen homes; project-based vs. repository-based topology |
| E-04 | Promotion Process — Path 0 | Draft → canonical `decisions/` graduation |
| E-05 | Promotion Process — Path 1 | Canonical (domain-slug) pure `git mv`, zero ID churn |
| E-06 | Promotion Process — Path 2 | Dialect rename + tombstone + citation re-pointing |
| E-07 | Amend vs. Supersede Conventions | In-body amendment blocks vs. new superseding ADR; amendment boundary |
| E-08 | Status Vocabulary & Transitions | PROPOSED/ACCEPTED/REJECTED/DEPRECATED/SUPERSEDED state machine |
| E-09 | L5 CI Lint Specification | L-1..L-14 rules, waiver ledger (L-11), grandfather allowlist (L-12) |
| E-10 | Ratification Gate | Two-tier (Tier-1 guidance / Tier-2 enforcement) gating model |
| E-11 | Producer-Side Fixes & Drift Monitoring | Fix 1 (template), Fix 2 (SKILL.md), Fix 3 (ps-architect agent + governance.yaml), L-14 |
| E-12 | New-Project Onboarding & Deployment Scope | Worktracker scaffold seeding; CoWork/plugin skeleton stripping (`.github/`, `docs/`, `projects/`) |
| E-13 | Migration Plan & Tracking | M-1..M-14, H-32 worktracker/GH Issue parity for gating items |
| E-14 | Relationship to Worktracker DEC-NNN | Non-conflation boundary |
| E-15 | Meta-Note (Self-Compliance) | This ADR's own dialect filename + declared remap path |

**MECE check:** Elements were derived directly from the invoking task's mandated lifecycle phases (creation -> E-01/E-02/E-04; cross-referencing -> E-09 L-7/L-8, E-13; amendment -> E-07; superseding -> E-07/E-09; promotion -> E-04/E-05/E-06; lint enforcement -> E-09; template drift -> E-11; new-project onboarding -> E-12) plus three structural elements the deliverable itself carries as first-class sections (E-08, E-14, E-15). Eight of the 15 elements (E-02, E-03, E-04, E-08, E-10 partial, E-13, E-14, E-15) were reviewed and no *novel* failure mode was found beyond what iterations 1-4 already remediated (see deliverable Changelog v1.1-v1.6) — these are not listed as findings below to avoid re-litigating settled ground, per this report's scope note.

---

## Findings Table

| ID | Element | Failure Mode | S | O | D | RPN | Severity | Corrective Action | Affected Dimension |
|----|---------|-------------|---|---|---|-----|----------|-------------------|--------------------|
| FM-001-20260702-it5 | E-07 (Amend vs Supersede) | Amendment-boundary rule ("amendments SHOULD NOT change scope/origin/location") claims L-8 as its enforcement backstop, but L-8 is a citation-string lint (detects stale references to a *moved* ID) and cannot detect an in-place frontmatter mutation on an *unchanged* ID/file | 8 | 4 | 9 | 288 | Critical | Add a dedicated lint rule (new L-15) diffing frontmatter `scope`/`origin_project`/`origin_entity`/path across commits on the same ADR ID; until built, retract the L-8 backstop claim and disclose as unmitigated | Internal Consistency |
| FM-002-20260702-it5 | E-11 (Producer drift) | L-14's monitored-file list (3 files) omits `ps-architect.governance.yaml`, which Fix 3 (F3-e) explicitly modifies as part of the same remediation — a regression there is invisible to L-14 | 6 | 5 | 7 | 210 | Critical | Add the `.governance.yaml` companion to L-14's grep list; cross-reference in M-12 | Completeness |
| FM-003-20260702-it5 | E-06 (Promotion Path 2) | AE-004 criticality-scoping paragraph (FM-103) explicitly classifies Path 1 (C3-floor lifecycle move) but never states whether Path 2 (rename + tombstone of a baselined ACCEPTED ADR) triggers AE-004 auto-C4 | 7 | 5 | 7 | 245 | Critical | Extend the FM-103 paragraph to explicitly classify Path 2 (recommend: C3-floor, same "metadata-only, content-immutable" logic as Path 1) | Internal Consistency |
| FM-004-20260702-it5 | E-12 (Onboarding/deployment) | PM-002's degraded-mode disclosure names L-3 and L-8 as "near-vacuous" against a stripped plugin install but omits L-10 (taxonomy synonymy), which depends on the identical stripped corpus (`docs/design/` + `projects/*/decisions/`) | 4 | 7 | 6 | 168 | Major | Add L-10 to the PM-002 disclosure list | Completeness |
| FM-005-20260702-it5 | E-09 (Lint) / E-11 (Template) | L-13 requires "a required Changelog entry on the target ADR," but Fix 1's template spec (F1-a..F1-f) never adds a `## Changelog` section as a standard element, and no verification exists that the 3 existing `docs/design/` ADRs carry one | 5 | 5 | 6 | 150 | Major | Add F1-g (Changelog-section stub) to Fix 1; fold verification/retrofit into M-11 | Methodological Rigor |
| FM-006-20260702-it5 | E-06 (Promotion) / E-13 (Migration) | GitHub Issues (mandated by H-32 for every gating Migration-Plan Task, e.g. M-6/M-11/M-12) that cite an ADR by ID have no detection/repair path on Path-2 rename or supersession — L-7/L-8 are repo-file-scoped and cannot reach GitHub's API | 5 | 6 | 8 | 240 | Critical | Disclose as a named residual (parallel to R-6/R-7/R-8); add a manual "search linked GH Issues" step to Path 2 Step 5 | Traceability |
| FM-007-20260702-it5 | E-10 (Ratification Gate) | The Tier-1/Tier-2 ratification split (v1.5) lets Tier-1 guidance reach `ACCEPTED` — actively encouraging new-ADR authorship — while Tier-2 (the lint, R-1's sole named mitigation) remains non-blocking with no committed timeline; R-1's Risks-table entry was never revisited to reflect this widened exposure window | 5 | 5 | 6 | 150 | Major | Cross-reference the two-tier model from the R-1 Risks-table row; consider bumping R-1 probability for the guidance-ratified/lint-pending interval | Methodological Rigor |

**Finding ID Format:** `FM-{NNN}-20260702-it5` (execution_id = iteration-5 date-stamped identifier, per S-012 template).

---

## Finding Details

### FM-001-20260702-it5: Amendment-boundary rule's claimed lint backstop is a category mismatch

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical (RPN 288) |
| **Element** | E-07 Amend vs. Supersede |
| **Strategy Step** | Step 2/3 (enumerate + rate) |

**Evidence:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md:596` — "An in-body amendment **SHOULD NOT** change an ADR's `scope`, `origin_project`/`origin_entity`, or canonical location... Amendments are limited to the decision's *explanatory prose* while the decision, its ID, its origin, and its location stay fixed; **the L-8 citation lint (WARN) surfaces any downstream breakage if the boundary is crossed anyway.**" Cross-checked against the L-8 rule definition itself (same file, line 696 and rule-draft `adr-standards-rule-draft.md:225`): L-8 "Grep every `ADR-[A-Za-z0-9-]+-\d{3}` token in prose/paths/config repo-wide... every referenced ID must resolve to a live ADR at its cited path" — it detects **stale citations to a moved/renamed ID**, not **frontmatter-field mutations on an unmoved, unrenamed file**.

**Analysis:** If an author edits `scope: project` to `scope: framework` (or changes `origin_project`) in-place, under the label of a "minor clarification," the ADR's ID and file path are unchanged, so there is no citation anywhere in the repo that becomes stale — L-8 has nothing to detect. None of the 14 named lint rules (L-1 through L-14, including the newer L-1a/L-1b/L-4b/L-6b/L-6c) inspects frontmatter-field history across commits on a single stable ID. This is a genuine enforcement gap for a boundary the deliverable treats as important enough to name explicitly (FM-010, iter-1) and re-align in register (CC-003, iter-3) — yet the claimed detection mechanism cannot fire for the violation it is cited to catch. Per FMEA lens: this is an **Incorrect** failure mode (the stated mitigation is factually inapplicable to the stated risk), which is more severe than a simple gap because it creates false confidence that a control exists.

**Corrective Action:** Either (a) add a new lint rule (e.g. `L-15 Amendment-boundary integrity`) that diffs `scope`/`origin_project`/`origin_entity`/canonical-location across an ADR's git history and flags any change not accompanied by a Path-1 `git mv` or a full Path-2 tombstone; or (b) if out of scope for this iteration, retract "the L-8 citation lint... surfaces any downstream breakage" and replace with an honest `[INHERENT]` disclosure parallel to R-6/R-7/R-8 (the deliverable's own established pattern for naming unmitigated residuals).

**Acceptance Criteria:** The Amendment Boundary paragraph no longer attributes detection capability to L-8 for a class of violation L-8's own definition cannot reach; either a new rule ID is specified or an honest residual-risk disclosure replaces the claim.

**Estimated Post-Correction RPN:** 288 -> ~90 (Major; D drops from 9 to ~5 once the mechanism is either built or honestly disclosed as monitored-by-human-review-only).

---

### FM-002-20260702-it5: L-14 producer-drift monitoring omits a file Fix 3 itself modifies

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical (RPN 210) |
| **Element** | E-11 Producer-Side Fixes & Drift Monitoring |
| **Strategy Step** | Step 2/3 |

**Evidence:** `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md:285` (Fix 3, row F3-e): "(companion) `ps-architect.governance.yaml` `output.location` / `filename_pattern` | Diverges from both proposed grammars... | Align `output.filename_pattern` to `ADR-{domain-slug}-{NNN}-*.md`..." — this is the 4th file Fix 3 touches. Compare `ADR-PROJ031-004-adr-identifier-convention.md:703` (L-14 rule definition): "Grep the **three** ADR-*producing* artifacts — `docs/knowledge/exemplars/templates/adr.md`, `skills/architecture/SKILL.md`, `skills/problem-solving/agents/ps-architect.md`..." — the governance.yaml companion is not in this list.

**Analysis:** L-14 exists precisely because "the L5 lint otherwise inspects only ADR *output*, never the *generator*" (same line). Per H-34 (agent-development-standards.md), every agent's dual-file architecture means the `.md` and `.governance.yaml` are both load-bearing for actual output behavior — F3-e's own text confirms the governance.yaml's `output.filename_pattern` field directly governs the filename grammar the agent emits. If a future, unrelated edit to `ps-architect.governance.yaml` (e.g. a schema-migration pass, per the agent-development-standards.md changelog history of such passes) reverts `output.filename_pattern` to a non-compliant value, L-14 — the rule whose entire purpose is catching exactly this class of silent producer-side regression — would not fire, because its own file enumeration never included the file that actually changed. This is a **Missing** failure mode (an element of the artifact set the rule needs to be complete is absent from its own definition), and it is self-referentially ironic: the rule designed to prevent "the generator drifting without detection" itself has an incomplete generator inventory.

**Corrective Action:** Add `skills/problem-solving/agents/ps-architect.governance.yaml` to L-14's grep-target list (and generalize the rule's scope statement to "the ADR-producing agent's `.md` file and its `.governance.yaml` companion"). Cross-reference in Migration Plan M-12.

**Acceptance Criteria:** L-14's file enumeration includes all artifacts Fix 3 modifies, with no orphaned producer surface.

**Estimated Post-Correction RPN:** 210 -> ~40 (Minor; the fix is a one-line addition to an existing rule's file list).

---

### FM-003-20260702-it5: AE-004 criticality scoping addresses Path 1 but is silent on Path 2

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical (RPN 245) |
| **Element** | E-06 Promotion Process — Path 2 |
| **Strategy Step** | Step 2/3 |

**Evidence:** `ADR-PROJ031-004-adr-identifier-convention.md:566` — "**AE-004 scoping of a promotion (FM-103, iter-3, P-022).** ... **Scoping rule:** a Path-1 promotion changes only **location** (`git mv`) and the **`scope` frontmatter field**... classified at the **C3** floor... it does **not** trip AE-004's C4 escalation... **Conversely:** any edit that would change the *decision* of a baselined ADR is **not** a promotion at all — it is a supersession... and is fully subject to AE-004/C4." Path 2 (the "rename + tombstone" path, `:568-576`) is never named in this scoping paragraph, despite Path 2 also mutating a baselined/ACCEPTED ADR's `status` field to `SUPERSEDED` and adding `promoted_to` (`:575`) — precisely the kind of frontmatter transition AE-004 ("modifies baselined ADR" -> auto-C4) is written to catch.

**Analysis:** The paragraph presents a clean binary: Path 1 = C3-floor lifecycle move; any *decision*-changing edit = supersession = C4. Path 2 does not fit neatly into either bucket as stated: it is a promotion (not a decision change), like Path 1, but it also flips a baselined ADR's status field and creates a tombstone — arguably more surface-area change than Path 1's `scope:` flip alone. A reader (or a future author executing M-9-style self-promotion) cannot determine from this text alone whether Path 2 inherits Path 1's C3-floor treatment (by the same "metadata-only, content-immutable" logic) or independently triggers AE-004's auto-C4. This is an **Ambiguous** failure mode in a document that otherwise prides itself on precisely reconciling exactly this class of criticality-boundary question (see the ADR's own Criticality basis correction, CC-004, for AE-002/AE-003).

**Corrective Action:** Extend the FM-103 paragraph with an explicit Path-2 clause, e.g.: "A Path-2 promotion likewise changes only lifecycle metadata (status, `promoted_to`, location) and not decision content on the source ADR; it is therefore scoped at the same C3 floor as Path 1, notwithstanding that it also creates a new sibling file — the new file's own criticality is assessed independently, on its own content." Explicitly close the asymmetry.

**Acceptance Criteria:** The FM-103 paragraph names both Path 1 and Path 2 with an explicit AE-004 classification for each.

**Estimated Post-Correction RPN:** 245 -> ~70 (Minor; a one-paragraph clarification closes the ambiguity).

---

### FM-006-20260702-it5: GitHub Issue citations to an ADR ID have no repair path on rename/supersession

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical (RPN 240) |
| **Element** | E-06 Promotion Process / E-13 Migration Plan |
| **Strategy Step** | Step 2/3 |

**Evidence:** H-32 (`.context/rules/project-workflow.md`, "GitHub Issue Parity") mandates a corresponding GitHub Issue for every worktracker bug/story/enabler/task in the `geekatron/jerry` repo. The deliverable's own Migration Plan applies this directly: `ADR-PROJ031-004-adr-identifier-convention.md:531` (M-6), `:536` (M-11), `:537` (M-12) all require "TBD-Task **+ GH Issue (H-32)**." Separately, the Path-2 citation re-pointing step (`:576`) reads: "**Re-point citations:** `grep -rl \"ADR-PROJ{NNN}-NNN\"` deterministically finds every citation site... The L5 lint (L-7 structured + L-8 free-text) then flags any *surviving live* reference." Both L-7 and L-8 are explicitly scoped "repo-wide" (`:695`, `:696`) — i.e., to files under version control in this repository. GitHub Issue bodies are not repo files; nothing in the L5 lint spec, the waiver ledger, or the CLI form (`uv run jerry lint adr`) mentions the GitHub API.

**Analysis:** Every gating Migration-Plan item is required to have a GitHub Issue per H-32, and issue bodies routinely cite the artifact they track by name (e.g., "implements the lint per ADR-adr-convention-001"). If that ADR is later renamed via Path 2, or superseded, the GitHub Issue's citation goes stale with **zero** detection mechanism — `grep -rl` cannot reach GitHub's hosted issue text, and no lint rule (L-1 through L-14) is described as calling the GitHub API (e.g. `gh api`/`gh issue list --search`) to check for external citations. This is a **Missing** failure mode: an entire citation surface that this very convention's own Migration Plan actively populates (via H-32) is outside the citation-integrity mechanism's reach, and the gap is not disclosed anywhere the two documents cover (confirmed via grep for "GitHub Issue" and "GH Issue" across both files — all matches concern *tracking* gating items, none concern *citation staleness*).

**Corrective Action:** Disclose this as a named residual parallel to R-6 (cross-branch race), R-7 (slug reuse), and R-8 (YAML/blockquote drift) in the Risks table — e.g. "R-9: GitHub Issue citations to a promoted/superseded ADR ID have no automated repair path; mitigation is a manual `gh issue list --search "<old-ID>"` sweep during Path-2 Step 5, added as an explicit sub-step." At minimum, add this manual sweep to Path 2's Step 5 procedure.

**Acceptance Criteria:** The Risks table (or Path 2 Step 5) names this gap explicitly with a detection signal and containment step, consistent with the document's own standard for naming INHERENT residuals.

**Estimated Post-Correction RPN:** 240 -> ~80 (Major; disclosure + a manual sweep step reduces detection risk but does not eliminate it, since the sweep is human-executed, not lint-enforced).

---

## Recommendations

Ordered by RPN (highest first):

1. **FM-001 (RPN 288, Critical):** Retract or replace the L-8-as-amendment-boundary-backstop claim; specify a real lint rule or an honest `[INHERENT]` disclosure. *Highest priority — this is a false-mitigation claim (P-022 territory), not merely a missing feature.*
2. **FM-003 (RPN 245, Critical):** Extend the FM-103 AE-004 scoping paragraph to explicitly classify Path 2.
3. **FM-006 (RPN 240, Critical):** Disclose the GitHub-Issue citation-staleness gap as a named residual (R-9) with a manual sweep step.
4. **FM-002 (RPN 210, Critical):** Add `ps-architect.governance.yaml` to L-14's monitored-file list.
5. **FM-004 (RPN 168, Major):** Add L-10 to the PM-002 degraded-mode disclosure list.
6. **FM-005 (RPN 150, Major):** Add a Changelog-section stub to Fix 1; verify the 3 existing framework ADRs carry one (fold into M-11).
7. **FM-007 (RPN 150, Major):** Cross-reference the Tier-1/Tier-2 ratification split from the R-1 Risks-table entry.

None of these require re-opening the core decision (Scheme B, subject-encoded identity); all are targeted textual additions consistent with the deliverable's own established remediation pattern across iterations 1-4.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | FM-002: L-14's monitored-artifact list is incomplete relative to Fix 3's own scope. FM-004: PM-002's degraded-mode disclosure omits L-10 despite identical dependency on the stripped corpus. |
| Internal Consistency | 0.20 | Negative | FM-001: a stated enforcement mechanism (L-8) cannot detect the violation class it is cited to catch. FM-003: AE-004 scoping is stated for Path 1 but silent on the structurally similar Path 2. |
| Methodological Rigor | 0.20 | Negative | FM-005: L-13 presupposes an artifact (Changelog section) never specified as a template requirement. FM-007: a risk-register entry (R-1) was not revisited after a later architectural change (two-tier ratification) altered its exposure window. |
| Evidence Quality | 0.15 | Neutral | Every finding in this report is directly evidence-based (file+line citations, cross-checked by grep for prior-tag novelty); the deliverable's own evidentiary discipline is high, and these findings extend rather than undermine it. |
| Actionability | 0.15 | Positive | Each finding carries a specific, minimal corrective action (one lint-rule addition, one file added to an existing list, one paragraph extension, one Risks-table cross-reference) — none require re-litigating the core decision. |
| Traceability | 0.10 | Negative | FM-006: an entire citation surface (GitHub Issues, populated by this convention's own H-32-mandated Migration Plan) is outside the citation-integrity mechanism's reach and undisclosed. |

---

## Execution Statistics

- **Total Findings:** 7
- **Critical:** 4 (FM-001, FM-002, FM-003, FM-006)
- **Major:** 3 (FM-004, FM-005, FM-007)
- **Minor:** 0
- **Total RPN:** 1451
- **Elements Analyzed:** 15 (7 with novel findings; 8 reviewed with no new failure mode beyond iterations 1-4 remediation)
- **Protocol Steps Completed:** 5 of 5 (Decompose; Enumerate; Rate S/O/D; Prioritize/Corrective Actions; Synthesize/Score Impact)
